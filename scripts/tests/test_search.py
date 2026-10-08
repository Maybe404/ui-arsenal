"""Offline tests for the find matching contract (synthetic rows, no catalogue or network needed)."""
import importlib.util
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('ua', os.path.join(HERE, '..', 'ua.py'))
ua = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ua)

GROUPS = [['定价', 'pricing', 'plan', '套餐'], ['标签页', 'tabs', 'tab'], ['按钮', 'button', 'btn'],
          ['侧边栏', '侧栏', 'sidebar'], ['折叠', 'accordion', 'collapsible'], ['日期', 'date', 'calendar'],
          ['选择器', '选择', 'select', 'picker'], ['主题', 'theme', 'dark', 'dark-mode'], ['开关', 'switch', 'toggle'],
          ['工具调用', 'tool call', 'function call'], ['图片', 'image', 'gallery']]


def row(rid, name='', category='', task='other', desc='', vtags='', itags=''):
    return {'id': rid, 'name': name or rid, 'category': category, 'task': task, 'desc': desc, 'vtags': vtags,
            'itags': itags}


def corpus_of(*rows):
    return [' '.join((r['id'], r['name'], r['category'], r['task'], r['desc'], r['vtags'], r['itags'])).lower()
            for r in rows]


def matches(term, text):
    return bool(ua.term_re(term).search(text))


class WordMatching(unittest.TestCase):
    def test_whole_words_not_prefixes(self):
        self.assertFalse(matches('plan', 'plane'))
        self.assertFalse(matches('plan', 'planet'))
        self.assertFalse(matches('tab', 'table'))
        self.assertFalse(matches('ai', 'detail'))
        self.assertFalse(matches('nav', 'canvas'))

    def test_regular_plurals(self):
        self.assertTrue(matches('plan', 'plans'))
        self.assertFalse(matches('plan', 'planes'))  # planes is the plural of plane
        self.assertTrue(matches('bus', 'buses'))
        self.assertTrue(matches('box', 'boxes'))
        self.assertTrue(matches('gallery', 'galleries'))
        self.assertTrue(matches('key', 'keys'))

    def test_hyphens_and_punctuation_break_words(self):
        self.assertTrue(matches('table', 'data-table'))
        self.assertTrue(matches('table', 'records table, sortable'))
        self.assertTrue(matches('dark-mode', 'a dark-mode toggle'))
        self.assertTrue(matches('tool call', 'shows each tool call inline'))

    def test_chinese_is_substring(self):
        self.assertTrue(matches('骨架', '骨架屏加载'))
        self.assertTrue(matches('ai', '用 ai 生成'))  # ASCII next to Chinese still has word breaks

    def test_typed_plurals_fold_to_singular(self):
        vocab = {t for g in GROUPS for t in g}
        text = 'button gallery status glass canvas'
        self.assertEqual(ua.singular('buttons', vocab, text), 'button')
        self.assertEqual(ua.singular('galleries', vocab, text), 'gallery')
        self.assertEqual(ua.singular('glass', vocab, text), 'glass')
        self.assertEqual(ua.singular('status', vocab, text), 'status')
        self.assertEqual(ua.singular('canvas', vocab, text), 'canvas')


class Concepts(unittest.TestCase):
    def concepts(self, tokens, *rows):
        return [(t, sorted(a)) for t, a in ua.concepts(tokens, GROUPS, corpus_of(*rows))]

    def test_compound_chinese_splits_by_longest_alias(self):
        got = self.concepts(['侧边栏可折叠'])
        self.assertEqual([t for t, _ in got], ['侧边栏', '折叠'])
        got = self.concepts(['日期选择器'])
        self.assertEqual([t for t, _ in got], ['日期', '选择器'])

    def test_leftover_words_kept_only_if_catalogue_has_them(self):
        r = row('stream', desc='流式输出的文字')
        self.assertEqual([t for t, _ in self.concepts(['日期输入'], r)], ['日期'])  # 输入 is not in the catalogue
        r2 = row('x', desc='支持键盘输入')
        self.assertEqual([t for t, _ in self.concepts(['日期输入'], r2)], ['日期', '输入'])
        self.assertEqual([t for t, _ in self.concepts(['我要一个日期组件'], r2)], ['日期'])  # filler dropped

    def test_phrases_and_same_group_merge(self):
        got = self.concepts(['dark', 'mode', 'toggle'])
        self.assertEqual([t for t, _ in got], ['dark-mode', 'toggle'])
        got = self.concepts(['tool', 'call'])
        self.assertEqual([t for t, _ in got], ['tool call'])
        got = self.concepts(['pricing', 'plan'])  # same group: one concept
        self.assertEqual(len(got), 1)

    def test_case_punctuation_and_plural(self):
        # lower-cased, trailing punctuation dropped, and the plural folded to the alias term it belongs to
        self.assertEqual([t for t, _ in self.concepts(['Tabs,'])], ['tab'])


class Relevance(unittest.TestCase):
    def score(self, tokens, r):
        cons = ua.compile_concepts(ua.concepts(tokens, GROUPS, corpus_of(r)))
        return ua.relevance(r, cons)

    def test_alias_in_name_is_strong(self):
        s, hit, strong, exact = self.score(['按钮'], row('button', 'Button', desc='通用按钮'))
        self.assertEqual((hit, strong, exact), (1, 1, 1))

    def test_generic_word_only_in_description_is_weak(self):
        s, hit, strong, exact = self.score(['按钮'], row('card', 'Card', desc='卡片，右上角有按钮'))
        self.assertEqual((hit, strong), (1, 0))

    def test_specific_term_in_description_is_strong(self):
        s, hit, strong, exact = self.score(['tool', 'call'], row('chips', 'Chips', desc='紧凑显示工具调用'))
        self.assertEqual((hit, strong), (1, 1))



class Stack(unittest.TestCase):
    def test_react_code_only_for_react(self):
        for fw, vue, react in (('react', False, True), ('css', True, True), ('multi', True, True),
                               ('any', True, True), ('', True, True)):
            r = row('x')
            r['framework'] = fw
            self.assertEqual((ua.fits_stack(r, 'vue'), ua.fits_stack(r, 'react')), (vue, react), fw)


class CompatMatrix(unittest.TestCase):
    """Reads the real matrix in sources/_styles.md (a repository file, no network)."""
    def setUp(self):
        self.m = ua.compat_matrix()

    def verdict(self, base, source):
        return ua.compat_verdict(base, source, self.m)

    def test_pairs_both_directions(self):
        self.assertEqual(self.verdict('shadcn', 'uiarc'), 'no')
        self.assertEqual(self.verdict('uiarc', 'shadcn'), 'no')
        self.assertEqual(self.verdict('shadcn', 'reactbits'), 'ok')
        self.assertEqual(self.verdict('shadcn', 'bencho'), 'conditional')

    def test_wildcards_and_base_specific_conditions(self):
        self.assertEqual(self.verdict('shadcn', 'lucide'), 'ok')
        self.assertEqual(self.verdict('shadcn', 'jakubantalik'), 'ok')
        self.assertEqual(self.verdict('uiarc', 'jakubantalik'), 'conditional')
        self.assertEqual(self.verdict('uiarc', 'inspora'), 'ok')

    def test_same_and_unknown(self):
        self.assertEqual(self.verdict('shadcn', 'shadcn'), 'same')
        self.assertEqual(self.verdict('uiarc', 'obsidianui'), 'unknown')


if __name__ == '__main__':
    unittest.main()
