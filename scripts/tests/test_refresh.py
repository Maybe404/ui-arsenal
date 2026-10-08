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
        return rc, json.load(open(ua.latest_pending(source), encoding='utf-8'))


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


if __name__ == '__main__':
    unittest.main()
