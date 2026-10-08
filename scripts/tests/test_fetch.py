"""Offline tests for fetch output handling (network mocked, files written only under a temp dir)."""
import importlib.util
import json
import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('ua', os.path.join(HERE, '..', 'ua.py'))
ua = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ua)


def registry(files, **extra):
    return (200, 'application/json', json.dumps(dict({'type': 'registry:block', 'files': files}, **extra)).encode())


def row(**kw):
    r = {'source': 'demo', 'id': 'thing', 'name': 'Thing', 'category': 'block', 'url': '', 'fetch': 'npx shadcn add x',
         'spec': 'registry:https://example.invalid/r/thing.json', 'access': 'free', 'usage': 'install',
         'framework': 'react', 'deps': '', 'status': 'active', 'alias_of': '', 'last_seen': '', 'fingerprint': '',
         'desc': '', 'task': 'other', 'layer': 'specialized', 'vtags': '', 'itags': '', 'risk': '', 'notes': ''}
    r.update(kw)
    return r


class FetchOutput(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.out = os.path.join(self.tmp, 'out')

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def fetch(self, response, r=None, **opts):
        opts.setdefault('out', self.out)
        if opts['out'] is None:  # use the default output directory
            del opts['out']
        with patch.object(ua, 'http', return_value=response), patch.object(ua, 'load_claims', return_value=[]):
            return ua.fetch_one(r or row(), opts, quiet=True)

    def files(self, d=None):
        return ua.list_files(d or self.out)

    def test_same_basename_in_different_folders_both_kept(self):
        rc = self.fetch(registry([{'path': 'a/index.tsx', 'content': 'A'}, {'path': 'b/index.tsx', 'content': 'B'}]))
        self.assertEqual(rc, 0)
        self.assertEqual(self.files(), ['a/index.tsx', 'b/index.tsx', 'registry-item.json'])
        self.assertEqual(open(os.path.join(self.out, 'b/index.tsx')).read(), 'B')

    def test_single_folder_lands_flat(self):
        self.fetch(registry([{'path': 'registry/x/x.tsx', 'content': '1'}, {'path': 'registry/x/x.css', 'content': '2'}]))
        self.assertEqual(self.files(), ['registry-item.json', 'x.css', 'x.tsx'])

    def test_upstream_deleted_file_does_not_linger(self):
        self.fetch(registry([{'path': 'p/x.tsx', 'content': '1'}, {'path': 'q/y.tsx', 'content': '2'}]))
        self.fetch(registry([{'path': 'p/x.tsx', 'content': '1b'}]))
        self.assertEqual(self.files(), ['registry-item.json', 'x.tsx'])
        self.assertFalse(os.path.exists(os.path.join(self.out, 'q')))  # emptied folder pruned

    def test_failure_publishes_nothing_and_removes_previous_result(self):
        self.fetch(registry([{'path': 'x.tsx', 'content': 'old'}]))
        rc = self.fetch(registry([{'path': 'x.tsx', 'content': 'new'}, {'path': 'y.tsx'}]))  # y has no content
        self.assertEqual(rc, 1)
        self.assertEqual(self.files(), [])
        self.assertEqual(ua.read_manifest(self.out)['status'], 'failed')

    def test_user_out_dir_keeps_unrelated_files(self):
        os.makedirs(self.out)
        open(os.path.join(self.out, 'mine.txt'), 'w').write('keep me')
        self.fetch(registry([{'path': 'x.tsx', 'content': '1'}]))
        self.fetch(registry([{'path': 'z.tsx', 'content': '2'}]))
        self.assertEqual(self.files(), ['mine.txt', 'registry-item.json', 'z.tsx'])

    def test_registry_path_escape_refused(self):
        rc = self.fetch(registry([{'path': 'ok.tsx', 'content': '1'}, {'path': '../../evil.tsx', 'content': 'x'}]))
        self.assertEqual(rc, 1)
        self.assertFalse(os.path.exists(os.path.join(self.tmp, 'evil.tsx')))
        self.assertEqual(self.files(), [])

    def test_url_with_encoded_traversal_stays_inside(self):
        r = row(spec='url:https://example.invalid/files/..%2F..%2Fescape.svg', usage='source')
        rc = self.fetch((200, 'image/svg+xml', b'<svg/>'), r)
        self.assertEqual(rc, 0)
        self.assertEqual(self.files(), ['escape.svg'])
        self.assertFalse(os.path.exists(os.path.join(self.tmp, 'escape.svg')))

    def test_manifest_from_disk_cannot_delete_outside(self):
        os.makedirs(self.out)
        victim = os.path.join(self.tmp, 'victim.txt')
        open(victim, 'w').write('x')
        json.dump({'files': [{'path': '../victim.txt'}]}, open(os.path.join(self.out, ua.MANIFEST), 'w'))
        self.fetch(registry([{'path': 'x.tsx', 'content': '1'}]))
        self.assertTrue(os.path.exists(victim))

    def test_style_and_variant_get_their_own_directories(self):
        r = row()
        self.assertTrue(ua.default_out(r, {}).endswith(os.path.join('demo', 'thing')))
        self.assertTrue(ua.default_out(r, {'style': 'radix-nova'}).endswith('thing@radix-nova'))
        self.assertTrue(ua.default_out(r, {'variant': 'JS-CSS'}).endswith('thing@JS-CSS'))

    def test_batch_out_gets_one_directory_per_ref(self):
        rows = {'demo:a': row(id='a'), 'demo:b': row(id='b')}
        with patch.object(ua, 'find_row', side_effect=lambda ref: rows[ref]), \
                patch.object(ua, 'http', return_value=registry([{'path': 'x.tsx', 'content': '1'}])), \
                patch.object(ua, 'load_claims', return_value=[]), patch('builtins.print'):
            ua.cmd_fetch(['demo:a', 'demo:b', '--out', self.out])
        self.assertEqual(self.files(), ['demo/a/registry-item.json', 'demo/a/x.tsx',
                                        'demo/b/registry-item.json', 'demo/b/x.tsx'])

    def test_legacy_default_dir_without_manifest_is_cleared(self):
        with patch.dict(os.environ, {'TMPDIR': self.tmp}):
            legacy = ua.default_out(row(), {})
            os.makedirs(legacy)
            open(os.path.join(legacy, 'Stale.tsx'), 'w').write('from an older run')
            self.fetch(registry([{'path': 'x.tsx', 'content': '1'}]), out=None)
            self.assertEqual(ua.list_files(legacy), ['registry-item.json', 'x.tsx'])

    def test_manifest_records_source_and_hashes(self):
        self.fetch(registry([{'path': 'x.tsx', 'content': 'hello'}]))
        m = ua.read_manifest(self.out)
        self.assertEqual(m['ref'], 'demo:thing')
        self.assertEqual(m['status'], 'ok')
        self.assertIn({'path': 'x.tsx', 'bytes': 5, 'sha256': ua.sha(b'hello')[:16]}, m['files'])


if __name__ == '__main__':
    unittest.main()
