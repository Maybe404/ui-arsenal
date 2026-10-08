"""Offline tests for refresh/apply: proposals are built from mocked indexes and written to a temp directory."""
import importlib.util
import json
import os
import shutil
import tempfile
import unittest
from contextlib import ExitStack, redirect_stdout
from io import StringIO
from unittest.mock import patch

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('ua', os.path.join(HERE, '..', 'ua.py'))
ua = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ua)

TODAY = '2026-10-08'


def row(rid, **kw):
    r = {'source': 'demo', 'id': rid, 'name': rid, 'category': 'icon', 'url': 'https://x.invalid/' + rid,
         'fetch': 'x', 'spec': 'url:https://x.invalid/%s.svg' % rid, 'access': 'free', 'usage': 'install',
         'framework': 'multi', 'deps': '', 'status': 'active', 'alias_of': '', 'last_seen': TODAY,
         'fingerprint': '', 'desc': rid, 'task': 'icon', 'layer': 'icons', 'vtags': '', 'itags': '', 'risk': '',
         'notes': ''}
    r.update(kw)
    return r


class Harness(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.stack = ExitStack()
        self.stack.enter_context(patch.object(ua, 'PENDING', os.path.join(self.tmp, '_pending')))
        self.stack.enter_context(patch.object(ua, 'STATE', os.path.join(self.tmp, '_state.json')))

    def tearDown(self):
        self.stack.close()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def refresh(self, source, refresher, rows):
        with patch.dict(ua.REFRESH, {source: refresher}), \
                patch.object(ua, 'load_rows', side_effect=lambda s=None, include_removed=False: rows), \
                redirect_stdout(StringIO()):
            rc = ua.cmd_refresh([source])
        with open(ua.latest_pending(source), encoding='utf-8') as f:
            return rc, json.load(f)


class PartialIndexes(Harness):
    def test_lucide_lab_failure_is_not_a_removal(self):
        responses = iter([(200, 'application/json', b'{"house": ["home"]}'), (503, 'text/plain', b'')])
        rows = [row('house', fingerprint='x'), row('lab:avocado', category='lab', fingerprint='')]
        with patch.object(ua, 'http', side_effect=lambda *a, **k: next(responses)):
            rc, d = self.refresh('lucide', ua.r_lucide, rows)
        self.assertEqual(d['status'], 'degraded')
        self.assertEqual(d['missing'], [])
        self.assertEqual(d['unverified'], ['lab:avocado'])
        self.assertIn('Lucide Lab', d['degraded'][0])

    def test_bencho_finds_failure_is_not_a_removal(self):
        responses = iter([(200, 'text/plain', b'https://bencho.dev/blocks/magnet-select\n'),
                          (500, 'text/html', b'')])
        rows = [row('magnet-select', source='bencho'), row('find:someone-thing', source='bencho')]
        with patch.object(ua, 'http', side_effect=lambda *a, **k: next(responses)):
            rc, d = self.refresh('bencho', ua.r_bencho, rows)
        self.assertEqual((d['status'], d['missing'], d['unverified']), ('degraded', [], ['find:someone-thing']))

    def test_empty_index_is_an_error(self):
        with patch.object(ua, 'http', return_value=(200, 'text/plain', b'nothing here')):
            rc, d = self.refresh('bencho', ua.r_bencho, [row('magnet-select', source='bencho')])
        self.assertEqual((rc, d['status']), (1, 'error'))

    def test_html_fallback_is_an_error(self):
        with patch.object(ua, 'http', return_value=(200, 'text/html', b'<!doctype html><html>maintenance</html>')):
            rc, d = self.refresh('lucide', ua.r_lucide, [row('house')])
        self.assertEqual((rc, d['status']), (1, 'error'))

    def test_suspicious_shrink_holds_removals_back(self):
        rows = [row('icon-%02d' % i, fingerprint='') for i in range(60)]
        few = ua.index({'icon-00': {}, 'icon-01': {}}, lambda r: r['id'], 'h', lambda k, m: {})
        rc, d = self.refresh('demo', lambda: few, rows)
        self.assertEqual(d['status'], 'degraded')
        self.assertEqual(d['missing'], [])
        self.assertEqual(len(d['suspect_missing']), 58)

    def test_real_removal_still_proposed(self):
        rows = [row('icon-%02d' % i, fingerprint='') for i in range(60)]
        most = ua.index({'icon-%02d' % i: {} for i in range(1, 60)}, lambda r: r['id'], 'h', lambda k, m: {})
        rc, d = self.refresh('demo', lambda: most, rows)
        self.assertEqual(d['status'], 'ok')
        self.assertEqual([m['id'] for m in d['missing']], ['icon-00'])



def tsv_line(r):
    return '\t'.join(r.get(k, '') for k in ua.COLS)


class Access(Harness):
    """#8: access changes are reported even before a fingerprint exists; leaving Pro restores the official route;
    dependency lists can be cleared, and an index that lists none leaves them alone."""
    def setUp(self):
        super().setUp()
        self.src = os.path.join(self.tmp, 'sources')
        os.makedirs(self.src)
        self.stack.enter_context(patch.object(ua, 'SRC', self.src))

    def write_source(self, rows):
        with open(os.path.join(self.src, 'demo.tsv'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(tsv_line(r) for r in rows) + '\n')
        with open(os.path.join(self.src, 'demo.notes.tsv'), 'w', encoding='utf-8') as f:
            f.write('\n'.join('\t'.join([r['id'], r['desc'], r['task'], r['layer'], '', '', '', '']) for r in rows) + '\n')

    def read_source(self):
        with open(os.path.join(self.src, 'demo.tsv'), encoding='utf-8') as f:
            return {r['id']: r for r in (dict(zip(ua.COLS, l.rstrip('\n').split('\t'))) for l in f if l.strip())}

    def uiarc_like(self, tier, deps=()):
        def refresher():
            def new(k, m):
                pro = m['tier'] != 'free'
                return {'spec': 'none' if pro else 'registry:https://x.invalid/r/%s.json' % k,
                        'fetch': 'docs only' if pro else 'npx shadcn@latest add https://x.invalid/r/%s.json' % k,
                        'access': 'pro' if pro else 'free'}
            return ua.index({'button': {'tier': tier, 'deps': sorted(deps)}}, lambda r: r['id'], 'h', new,
                            detects=('access', 'deps'))
        return refresher

    def apply(self, d):
        p = os.path.join(self.tmp, 'proposal.json')
        json.dump(d, open(p, 'w', encoding='utf-8'))
        with redirect_stdout(StringIO()):
            return ua.cmd_apply(['demo', '--file', p])

    def test_free_to_pro_reported_without_fingerprint(self):
        rows = [row('button', access='free', fingerprint='', spec='registry:https://x.invalid/r/button.json')]
        rc, d = self.refresh('demo', self.uiarc_like('pro'), rows)
        self.assertEqual(d['init'], [])
        self.assertEqual(d['changed'][0]['access'], ['free', 'pro'])

    def test_pro_to_free_restores_the_fetch_route_and_clears_deps(self):
        rows = [row('button', access='pro', spec='none', fetch='docs only', deps='old-dep', fingerprint='old')]
        self.write_source(rows)
        rc, d = self.refresh('demo', self.uiarc_like('free'), rows)
        self.apply(d)
        r = self.read_source()['button']
        self.assertEqual((r['access'], r['spec'], r['deps'], r['status']),
                         ('free', 'registry:https://x.invalid/r/button.json', '', 'needs-review'))
        self.assertIn('npx shadcn@latest add', r['fetch'])

    def test_unlisted_deps_are_kept(self):
        rows = [row('house', deps='lucide-react', fingerprint='old')]
        self.write_source(rows)
        plain = lambda: ua.index({'house': {'tags': ['home']}}, lambda r: r['id'], 'h', lambda k, m: {})
        rc, d = self.refresh('demo', plain, rows)
        self.assertIsNone(d['changed'][0]['deps'][1])
        self.apply(d)
        self.assertEqual(self.read_source()['house']['deps'], 'lucide-react')

    def test_unknown_tier_is_no_access_claim(self):
        rows = [row('button', access='free', fingerprint='')]
        rc, d = self.refresh('demo', self.uiarc_like('enterprise'), rows)
        self.assertEqual(d['changed'], [])
        self.assertEqual(len(d['init']), 1)

    def test_leaving_pro_without_a_route_is_refused(self):
        rows = [row('button', access='pro', spec='none', fingerprint='old')]
        self.write_source(rows)
        d = {'source': 'demo', 'status': 'ok', 'format': ua.PROPOSAL_FORMAT, 'generated_at': TODAY + ' 10:00',
             'seen': ['button'], 'init': [], 'missing': [], 'added': [],
             'changed': [{'id': 'button', 'fingerprint': ['old', 'new'], 'deps': ['', None], 'access': ['pro', 'free']}]}
        with self.assertRaises(SystemExit):
            self.apply(d)
        self.assertEqual(self.read_source()['button']['access'], 'pro')

    def test_old_proposal_format_is_refused(self):
        self.write_source([row('button')])
        with self.assertRaises(SystemExit):
            self.apply({'source': 'demo', 'status': 'ok', 'generated_at': TODAY, 'seen': [], 'init': [],
                        'changed': [], 'missing': [], 'added': []})


if __name__ == '__main__':
    unittest.main()
