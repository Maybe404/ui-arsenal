"""Offline tests for the Bencho literal parser (no network, no remote code)."""
import importlib.util
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('bencho', os.path.join(HERE, '..', 'adapters', 'bencho.py'))
bencho = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bencho)


def parse(src):
    return bencho.Parser(src, 0).value()


class LiteralValues(unittest.TestCase):
    def test_keywords(self):
        for src, want in (('true', True), ('false', False), ('!0', True), ('!1', False),
                          ('null', None), ('void 0', None)):
            with self.subTest(src=src):
                self.assertIs(parse(src), want)

    def test_numbers(self):
        for src, want in (('0', 0), ('42', 42), ('-7', -7), ('3.14', 3.14), ('-0.5', -0.5), ('.5', 0.5),
                          ('1e3', 1000.0), ('2.5E-2', 0.025), ('-1e+2', -100.0)):
            with self.subTest(src=src):
                got = parse(src)
                self.assertEqual(got, want)
                self.assertIs(type(got), type(want))

    def test_strings(self):
        self.assertEqual(parse('"a\\nb"'), 'a\nb')
        self.assertEqual(parse("'it\\'s'"), "it's")
        self.assertEqual(parse('`multi\nline`'), 'multi\nline')
        self.assertEqual(parse('"\\u00e9\\x41\\u{1F600}"'), 'éA\U0001F600')

    def test_nested(self):
        src = '{a:1,"b":[true,!1,null,{c:"x",d:[.5,-2]}],e:void 0,f:{}}'
        self.assertEqual(parse(src), {'a': 1, 'b': [True, False, None, {'c': 'x', 'd': [0.5, -2]}], 'e': None, 'f': {}})

    def test_keyword_needs_word_boundary(self):
        # an identifier that starts like a keyword must not be read as the keyword
        with self.assertRaises(bencho.LiteralError):
            parse('{a:trueish}')


class RefusesCode(unittest.TestCase):
    def test_rejects_non_literals(self):
        for src in ('{a:foo}', '{a:()=>1}', '{a:function(){}}', '[1+1]', '{a:new Date}', '{a:`x${y}`}'):
            with self.subTest(src=src):
                with self.assertRaises(bencho.LiteralError) as ctx:
                    parse(src)
                self.assertRegex(str(ctx.exception), r'at \d+')

    def test_deep_nesting_is_refused_not_recursed(self):
        with self.assertRaises(bencho.LiteralError) as ctx:
            parse('[' * 500 + ']' * 500)
        self.assertIn('nesting deeper than', str(ctx.exception))
        want = 1
        for _ in range(50):
            want = [want]
        self.assertEqual(parse('[' * 50 + '1' + ']' * 50), want)

    def test_truncated_input_reports_position(self):
        p = bencho.Parser('{a:[1,2', 0)
        with self.assertRaises(IndexError):
            p.value()
        self.assertEqual(p.i, 7)


if __name__ == '__main__':
    unittest.main()
