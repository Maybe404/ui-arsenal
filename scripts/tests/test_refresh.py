"""Offline tests for refresh/apply: proposals are built from mocked indexes and written to a temp directory."""
import copy
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
        with open(os.path.join(self.src, 'demo.md'), 'w', encoding='utf-8') as f:
            f.write('---\nid: demo\nsource_status: active\n---\n')
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
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(d, f)
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



class Proposals(Access):
    """#9: a proposal is checked against its source and base before anything is written, the two files change
    together or not at all, and refreshing again keeps what a human filled in."""
    def new_item_refresher(self):
        return lambda: ua.index({'house': {}, 'tent': {}}, lambda r: r['id'], 'h',
                                lambda k, m: {'spec': 'url:https://x.invalid/%s.svg' % k, 'usage': 'install'})

    def fill(self, d, **fields):
        for a in d['added']:
            a.update(fields)
        return d

    def snapshot(self):
        out = []
        for n in ('demo.tsv', 'demo.notes.tsv'):
            with open(os.path.join(self.src, n), encoding='utf-8') as f:
                out.append(f.read())
        return out

    def test_new_source_starts_from_empty_files(self):
        with open(os.path.join(self.src, 'demo.md'), 'w', encoding='utf-8') as f:
            f.write('---\nid: demo\nsource_status: active\n---\n')
        for n in ('demo.tsv', 'demo.notes.tsv'):
            open(os.path.join(self.src, n), 'w').close()
        rc, d = self.refresh('demo', self.new_item_refresher(), [])
        self.assertEqual(self.apply(self.fill(d, desc_zh='房子', task='icon', layer='icons')), 0)
        tsv, notes = self.snapshot()
        self.assertEqual([l.split('\t')[0] for l in notes.splitlines()], ['house', 'tent'])  # no leading blank line
        self.assertEqual(sorted(self.read_source()), ['house', 'tent'])
    def test_malformed_changed_entry_leaves_both_files_untouched(self):
        """A changed entry is checked like a new item: tab in spec, a spec that is not https, an unknown id, a
        fingerprint that fp() could not have produced, or a missing or malformed field is refused with a message
        before anything is written (the tab used to produce a 17-column row, a missing field a KeyError)."""
        rows = [row('button', access='pro', spec='none', fetch='docs only', fingerprint='old')]
        self.write_source(rows)
        rc, proposal = self.refresh('demo', self.uiarc_like('free'), rows)
        for mutate in (lambda c: c.update(spec='registry:https://x.invalid/r/button.json\tx'),
                       lambda c: c.update(spec='registry:http://x.invalid/r/button.json'),
                       lambda c: c.update(id='ghost'),
                       lambda c: c.update(fingerprint=['old', 'not a hash']),
                       lambda c: c.update(fingerprint=['old', '0']),
                       lambda c: c.pop('deps'),
                       lambda c: c.pop('access'),
                       lambda c: c.update(access='free')):
            d = copy.deepcopy(proposal)
            mutate(d['changed'][0])
            before = self.snapshot()
            self.assertEqual(self.apply(d), 1)
            self.assertEqual(self.snapshot(), before)
        for drop in ('init', 'changed'):  # a hand-edited proposal without one of its lists
            d = copy.deepcopy(proposal)
            del d[drop]
            self.assertEqual(self.apply(d), 1)
            self.assertEqual(self.snapshot(), before)

    def test_empty_fingerprint_is_still_accepted(self):
        """fp() returns '' for an item without metadata (React Bits variants), so '' stays a valid new value."""
        rows = [row('button', access='pro', spec='none', fetch='docs only', fingerprint='old')]
        self.write_source(rows)
        rc, d = self.refresh('demo', self.uiarc_like('free'), rows)
        d['changed'][0]['fingerprint'][1] = ''
        self.assertEqual(self.apply(d), 0)

    def test_wrong_source_refused(self):
        self.write_source([row('house')])
        rc, d = self.refresh('demo', self.new_item_refresher(), [row('house')])
        d['source'] = 'other'
        with self.assertRaises(SystemExit):
            self.apply(d)

    def test_base_changed_after_refresh_refused(self):
        self.write_source([row('house')])
        rc, d = self.refresh('demo', self.new_item_refresher(), [row('house')])
        self.write_source([row('house', desc='edited by hand')])  # the machine file moves on
        with open(os.path.join(self.src, 'demo.tsv'), 'a', encoding='utf-8') as f:
            f.write(tsv_line(row('extra')) + '\n')
        with self.assertRaises(SystemExit):
            self.apply(self.fill(d, desc_zh='帐篷', task='icon', layer='icons'))

    def test_invalid_new_item_leaves_both_files_untouched(self):
        self.write_source([row('house')])
        rc, d = self.refresh('demo', self.new_item_refresher(), [row('house')])
        before = self.snapshot()
        self.assertEqual(self.apply(self.fill(d, desc_zh='帐篷', task='camping', layer='icons')), 1)
        self.assertEqual(self.snapshot(), before)

    def test_failure_while_swapping_files_rolls_back(self):
        self.write_source([row('house')])
        rc, d = self.refresh('demo', self.new_item_refresher(), [row('house')])
        before = self.snapshot()
        real_replace, calls = os.replace, []

        def flaky(src, dst):
            calls.append(dst)
            if dst.endswith('demo.notes.tsv') and src.endswith('.apply-tmp'):
                raise OSError('disk full (simulated)')
            return real_replace(src, dst)
        with patch.object(ua.os, 'replace', side_effect=flaky):
            with self.assertRaises(OSError):
                self.apply(self.fill(d, desc_zh='帐篷', task='icon', layer='icons'))
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(sorted(os.listdir(self.src)), ['demo.md', 'demo.notes.tsv', 'demo.tsv'])  # no temp/backup files

    def test_refresh_again_keeps_human_fields_in_a_new_revision(self):
        self.write_source([row('house')])
        rc, first = self.refresh('demo', self.new_item_refresher(), [row('house')])
        p1 = ua.latest_pending('demo')
        self.fill(first, desc_zh='帐篷图标', task='icon', layer='icons')
        with open(p1, 'w', encoding='utf-8') as f:
            json.dump(first, f)
        with patch.object(ua.time, 'strftime', side_effect=lambda fmt, *a: {'%H%M%S': '235959'}.get(fmt, TODAY)):
            rc, second = self.refresh('demo', self.new_item_refresher(), [row('house')])
        p2 = ua.latest_pending('demo')
        self.assertNotEqual(p1, p2)
        self.assertEqual(second['added'][0]['desc_zh'], '帐篷图标')
        with open(p1, encoding='utf-8') as f:
            self.assertEqual(json.load(f)['added'][0]['desc_zh'], '帐篷图标')  # first revision untouched

    def test_applied_proposal_is_not_applied_twice(self):
        self.write_source([row('house')])
        rc, d = self.refresh('demo', self.new_item_refresher(), [row('house')])
        p = ua.latest_pending('demo')
        self.fill(d, desc_zh='帐篷', task='icon', layer='icons')
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(d, f)
        with redirect_stdout(StringIO()):
            self.assertEqual(ua.cmd_apply(['demo', '--file', p]), 0)
        self.assertIn('tent', self.read_source())
        self.assertIsNone(ua.latest_pending('demo'))
        with self.assertRaises(SystemExit), redirect_stdout(StringIO()):
            ua.cmd_apply(['demo', '--file', p])



class Lifecycle(Access):
    """#4: online presence and human review are tracked apart; removal counts from the first confirmed absence;
    removed items that come back are proposed for review, aliases resolve safely."""
    def refresh_on(self, day, refresher, rows):
        with patch.object(ua.time, 'strftime', side_effect=lambda fmt, *a: {
                '%Y-%m-%d': day, '%H%M%S': '1%05d' % len(os.listdir(self.tmp)), '%Y-%m-%d %H:%M': day + ' 10:00',
                '%Y-%m-%d %H:%M:%S': day + ' 10:00:00'}.get(fmt, day)):
            rc, d = self.refresh('demo', refresher, rows)
            self.apply(d)
        return d

    def only(self, *keys):
        return lambda: ua.index({k: {} for k in keys}, lambda r: r['id'], 'h', lambda k, m: {})

    def test_removal_clock_starts_at_first_confirmed_absence(self):
        rows = [row('house', last_seen='2026-01-01'), row('tent')]  # last seen long ago: refresh did not run
        self.write_source(rows)
        d1 = self.refresh_on('2026-10-08', self.only('tent'), list(self.read_source().values()))
        self.assertEqual(d1['missing'][0]['proposal'], 'needs-review')
        self.assertEqual(self.read_source()['house']['review'], 'missing:2026-10-08')
        d2 = self.refresh_on('2026-10-08', self.only('tent'), list(self.read_source().values()))
        self.assertEqual(d2['missing'][0]['proposal'], 'needs-review')  # same day: not removed
        d3 = self.refresh_on('2026-11-08', self.only('tent'), list(self.read_source().values()))
        self.assertEqual(d3['missing'][0]['proposal'], 'removed')
        self.assertEqual(self.read_source()['house']['status'], 'removed')

    def test_seen_clears_missing_but_not_a_pending_review(self):
        rows = [row('house', status='needs-review', review='missing:2026-10-01'),
                row('tent', status='needs-review', review='new:2026-10-01,missing:2026-10-02')]
        self.write_source(rows)
        self.refresh_on('2026-10-08', self.only('house', 'tent'), rows)
        got = self.read_source()
        self.assertEqual((got['house']['status'], got['house']['review']), ('active', ''))
        self.assertEqual((got['tent']['status'], got['tent']['review']), ('needs-review', 'new:2026-10-01'))

    def test_removed_item_that_comes_back_is_proposed_for_review(self):
        rows = [row('house', status='removed', review='missing:2026-08-01')]
        self.write_source(rows)
        d = self.refresh_on('2026-10-08', self.only('house'), rows)
        self.assertEqual(d['seen'], [])
        self.assertEqual([b['id'] for b in d['revived']], ['house'])
        got = self.read_source()['house']
        self.assertEqual((got['status'], got['review']), ('needs-review', 'back:2026-10-08'))

    def test_dates_in_the_future_never_count_as_old(self):
        self.assertEqual(ua.days_since('2026-10-08', '2026-10-01'), -7)
        self.assertIsNone(ua.days_since('', '2026-10-01'))

    def test_review_done_keeps_missing(self):
        self.write_source([row('house', status='needs-review', review='new:2026-10-01'),
                           row('tent', status='needs-review', review='changed:2026-10-01,missing:2026-10-02')])
        with redirect_stdout(StringIO()):
            ua.cmd_review(['--done', 'demo:house', 'demo:tent'])
        got = self.read_source()
        self.assertEqual((got['house']['status'], got['house']['review']), ('active', ''))
        self.assertEqual((got['tent']['status'], got['tent']['review']), ('needs-review', 'missing:2026-10-02'))


class RegistryOptions(unittest.TestCase):
    """r_registry for the sources added on 2026-10-08: item filters, a custom index path, and paid items listed
    next to free ones (Tailark)."""
    def index_of(self, items, **kw):
        body = json.dumps({'items': items}).encode()
        with patch.object(ua, 'get_json', return_value=(json.loads(body), body)) as g:
            ix = ua.r_registry('https://x.invalid', **kw)()
        return ix, g.call_args[0][0]

    def test_keep_and_custom_index(self):
        items = [{'name': 'card', 'type': 'registry:ui'}, {'name': 'card-demo', 'type': 'registry:example'}]
        ix, url = self.index_of(items, keep=lambda it: it['type'] == 'registry:ui',
                                index_url='https://x.invalid/registry.json', item_url='https://x.invalid/%s.json')
        self.assertEqual(url, 'https://x.invalid/registry.json')
        self.assertEqual(list(ix['remote']), ['card'])
        self.assertEqual(ix['new_row']('card', ix['remote']['card'])['spec'], 'registry:https://x.invalid/card.json')

    def test_paid_items_get_no_fetch_route(self):
        items = [{'name': 'hero-1', 'type': 'registry:block'}, {'name': 'core-x', 'type': 'registry:component'}]
        ix, _ = self.index_of(items, tier=lambda it: 'free' if it['name'].startswith('core-') else 'pro',
                              pro_fetch=lambda k, m: 'https://x.invalid/%s.png' % k)
        pro = ix['new_row']('hero-1', ix['remote']['hero-1'])
        self.assertEqual((pro['spec'], pro['access'], pro['fetch']), ('none', 'pro', 'https://x.invalid/hero-1.png'))
        self.assertEqual(ix['new_row']('core-x', ix['remote']['core-x'])['access'], 'free')
        self.assertIn('access', ix['detects'])
        # pro rows (spec none) are matched by id; rows fetched from elsewhere are not this index's business
        self.assertEqual(ix['key_of']({'id': 'hero-1', 'spec': 'none'}), 'hero-1')
        self.assertIsNone(ix['key_of']({'id': 'oss-x', 'spec': 'url:https://raw.invalid/x.tsx'}))


class Aliases(unittest.TestCase):
    def rows(self, *spec):
        return [row(i, alias_of=a, status=st) for i, a, st in spec]

    def test_chain_resolves(self):
        r, path = ua.resolve_alias(self.rows(('old', 'mid', 'removed'), ('mid', 'new', 'removed'),
                                             ('new', '', 'active')), 'old')
        self.assertEqual((r['id'], path), ('new', ['old', 'mid', 'new']))

    def test_cycle_and_dead_ends(self):
        with self.assertRaisesRegex(LookupError, 'cycle'):
            ua.resolve_alias(self.rows(('a', 'b', 'removed'), ('b', 'a', 'removed')), 'a')
        with self.assertRaisesRegex(LookupError, 'has been removed'):
            ua.resolve_alias(self.rows(('a', 'b', 'removed'), ('b', '', 'removed')), 'a')
        with self.assertRaisesRegex(LookupError, 'not in the catalogue'):
            ua.resolve_alias(self.rows(('a', 'zzz', 'removed')), 'a')


if __name__ == '__main__':
    unittest.main()
