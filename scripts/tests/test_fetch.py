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



class ResultContract(unittest.TestCase):
    """#6: what a caller can rely on from the exit code, the status and the messages."""
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.out = os.path.join(self.tmp, 'out')

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def fetch(self, r, response=None, run=None):
        opts = {'out': self.out}
        with patch.object(ua, 'http', return_value=response), patch.object(ua, 'load_claims', return_value=[]):
            if run:
                with patch.object(ua.subprocess, 'run', side_effect=run):
                    return ua.fetch_one(r, opts, quiet=True), opts['_result']
            return ua.fetch_one(r, opts, quiet=True), opts['_result']

    def test_html_page_is_not_saved_as_source(self):
        r = row(spec='url:https://example.invalid/source.tsx', usage='source')
        rc, res = self.fetch(r, (200, 'text/html; charset=utf-8', b'<!DOCTYPE html><html>Login</html>'))
        self.assertEqual((rc, res['status'], res['files']), (1, 'failed', 0))

    def test_html_without_content_type_is_still_caught(self):
        r = row(spec='doc:https://example.invalid/DESIGN.md', usage='prompt')
        rc, _ = self.fetch(r, (200, '', b'\n  <html><body>Sign in</body></html>'))
        self.assertEqual(rc, 1)

    def test_media_and_svg_types(self):
        video = row(spec='url:https://example.invalid/clip.mp4', usage='reference')
        self.assertEqual(self.fetch(video, (200, 'text/plain', b'not a video'))[0], 1)
        self.assertEqual(self.fetch(video, (200, 'video/mp4', b'\x00\x00ftyp'))[0], 0)
        svg = row(spec='url:https://example.invalid/icon.svg', usage='install')
        self.assertEqual(self.fetch(svg, (200, 'text/plain', b'oops'))[0], 1)
        self.assertEqual(self.fetch(svg, (200, 'image/svg+xml', b'<svg xmlns="x"/>'))[0], 0)

    def test_browser_only_is_exit_5_without_files(self):
        r = row(spec='browser:https://example.invalid/page', usage='reference')
        rc, res = self.fetch(r)
        self.assertEqual((rc, res['status'], res['files']), (5, 'browser', 0))

    def test_partial_when_one_step_fails(self):
        r = row(spec='registry:https://example.invalid/r/x.json doc:https://example.invalid/x.md')
        responses = iter([registry([{'path': 'x.tsx', 'content': '1'}]), (404, 'text/html', b'')])
        with patch.object(ua, 'http', side_effect=lambda *a, **k: next(responses)), \
                patch.object(ua, 'load_claims', return_value=[]):
            opts = {'out': self.out}
            rc = ua.fetch_one(r, opts, quiet=True)
        self.assertEqual((rc, opts['_result']['status'], opts['_result']['files']), (1, 'partial', 2))

    def test_batch_exit_is_the_most_urgent_code_not_a_bit_or(self):
        self.assertEqual(ua.batch_exit([1, 2]), 1)  # bit-or gave 3, which means Pro
        self.assertEqual(ua.batch_exit([2, 4]), 4)  # bit-or gave 6, which means nothing
        self.assertEqual(ua.batch_exit([0, 5]), 5)
        self.assertEqual(ua.batch_exit([3, 0]), 3)
        self.assertEqual(ua.batch_exit([0, 0]), 0)

    def test_install_hint_does_not_inherit_previous_ref_url(self):
        first = row(id='a', spec='registry:https://ui.example/r/styles/base-nova/a.json')
        second = row(id='b', source='loadingui', spec='url:https://example.invalid/b.tsx', usage='install',
                     fetch='npx shadcn@latest add @loading-ui/b')
        rows = {'demo:a': first, 'loadingui:b': second}
        printed = []
        with patch.object(ua, 'find_row', side_effect=lambda ref: rows[ref]), \
                patch.object(ua, 'http', side_effect=[registry([{'path': 'a.tsx', 'content': '1'}]),
                                                     (200, 'text/plain', b'export const B = 1')]), \
                patch.object(ua, 'load_claims', return_value=[]), \
                patch('builtins.print', side_effect=lambda *a, **k: printed.append(' '.join(map(str, a)))):
            ua.cmd_fetch(['demo:a', 'loadingui:b', '--style', 'radix-nova', '--out', self.out])
        hint_b = [l for l in printed if '安装' in l][-1]
        self.assertIn('@loading-ui/b', hint_b)
        self.assertNotIn('/a.json', hint_b)

    def test_adapter_timeout_and_error_lines(self):
        r = row(spec='script:bencho thing', usage='source')

        def timeout(*a, **k):
            raise ua.subprocess.TimeoutExpired(a[0], ua.ADAPTER_TIMEOUT)
        rc, res = self.fetch(r, run=timeout)
        self.assertEqual((rc, res['status']), (1, 'failed'))

        class Done:
            returncode, stdout = 1, b''
            stderr = b'Traceback...\nbencho: HTTP 404 fetching https://bencho.dev/\n'
        with patch('builtins.print') as p, patch.object(ua.subprocess, 'run', return_value=Done()), \
                patch.object(ua, 'load_claims', return_value=[]):
            ua.fetch_one(r, {'out': self.out})
        fail = [c.args[0] for c in p.call_args_list if c.args and str(c.args[0]).startswith('FAIL')][0]
        self.assertIn('exit 1', fail)
        self.assertIn('HTTP 404', fail)
        self.assertNotIn('Traceback', fail)

    def test_source_entries_print_their_dependencies(self):
        r = row(spec='script:bencho thing', usage='source')

        class Done:
            returncode, stderr = 0, b''
            stdout = b'--- Thing.tsx ---\ncode\n\n# deps: npm i framer-motion\n'
        with patch('builtins.print') as p, patch.object(ua.subprocess, 'run', return_value=Done()), \
                patch.object(ua, 'load_claims', return_value=[]):
            ua.fetch_one(r, {'out': self.out})
        self.assertTrue(any('npm i framer-motion' in str(c.args[0]) for c in p.call_args_list if c.args))



class Robustness(unittest.TestCase):
    """#24: size limits, @latest versions, state file writes."""
    class Resp:
        def __init__(self, body, length=None, url='https://example.invalid/x', ct='text/plain'):
            self.body, self.status, self._url = body, 200, url
            self.headers = {'content-type': ct, 'content-length': str(length if length is not None else len(body))}

        def read(self, n=-1):
            return self.body[:n] if n and n > 0 else self.body

        def geturl(self):
            return self._url

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def test_declared_size_over_limit_is_not_read(self):
        with patch.object(ua.urllib.request, 'urlopen', return_value=self.Resp(b'x', length=ua.MAX_TEXT + 1)):
            st, ct, body = ua.http('https://example.invalid/big.json')
        self.assertEqual(st, -1)
        self.assertIn('response too large', ua.http_fail(st, body, 'u'))

    def test_undeclared_size_over_limit_is_cut(self):
        with patch.object(ua.urllib.request, 'urlopen', return_value=self.Resp(b'x' * 11, length='')):
            st, ct, body = ua.http('https://example.invalid/stream.txt', max_bytes=10)
        self.assertEqual(st, -1)

    def test_media_gets_a_larger_limit(self):
        resp = self.Resp(b'x', length=ua.MAX_TEXT + 1, ct='video/mp4')
        with patch.object(ua.urllib.request, 'urlopen', return_value=resp):
            st, ct, body = ua.http('https://example.invalid/clip.mp4')
        self.assertEqual(st, 200)

    def test_latest_url_reports_resolved_version(self):
        url = 'https://unpkg.com/lucide-static@latest/icons/house.svg'
        resp = self.Resp(b'<svg/>', url='https://unpkg.com/lucide-static@1.52.0/icons/house.svg', ct='image/svg+xml')
        tmp = tempfile.mkdtemp()
        try:
            opts = {}
            with patch.object(ua.urllib.request, 'urlopen', return_value=resp):
                ok, msg = ua.do_url(url, tmp, 'url', opts)
            self.assertTrue(ok)
            self.assertIn('lucide-static@1.52.0', msg)
            self.assertEqual(opts['_resolved'], 'lucide-static@1.52.0')
            r = row(source='lucide', id='house', name='House')
            self.assertIn('lucide-static@1.52.0', ua.install_hint(r, opts))
        finally:
            shutil.rmtree(tmp)

    def test_state_updates_merge_and_write_atomically(self):
        tmp = tempfile.mkdtemp()
        try:
            with patch.object(ua, 'STATE', os.path.join(tmp, '_state.json')):
                ua.update_state(lambda s: s.setdefault('verify', {}).update({'a': 1}))
                ua.update_state(lambda s: s.setdefault('refresh', {}).update({'b': 2}))
                ua.update_state(lambda s: s.setdefault('verify', {}).update({'c': 3}))
                self.assertEqual(ua.load_state(), {'verify': {'a': 1, 'c': 3}, 'refresh': {'b': 2}})
            self.assertEqual(sorted(os.listdir(tmp)), ['_state.json', '_state.json.lock'])  # no temp file left
        finally:
            shutil.rmtree(tmp)


if __name__ == '__main__':
    unittest.main()
