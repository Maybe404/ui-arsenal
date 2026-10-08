"""Offline tests for command-line handling: bad arguments are usage errors (exit 2), never tracebacks."""
import contextlib
import importlib.util
import io
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('ua', os.path.join(HERE, '..', 'ua.py'))
ua = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ua)


def quiet(fn, *args):
    with contextlib.redirect_stdout(io.StringIO()) as out:
        rc = fn(*args)
    return rc, out.getvalue()


class Arguments(unittest.TestCase):
    def test_missing_or_bad_values(self):
        for cmd, args in ((ua.cmd_find, ['--limit', 'x']), (ua.cmd_find, ['背景', '-s']), (ua.cmd_find, ['--task']),
                          (ua.cmd_find, ['按钮', '--cod']), (ua.cmd_find, ['--task', 'nope']),
                          (ua.cmd_find, ['x', '-s', 'nope']), (ua.cmd_fetch, ['shadcn:button', '--limit', '0']),
                          (ua.cmd_fetch, ['shadcn:button', '--style']), (ua.cmd_verify, ['-n', 'x']),
                          (ua.cmd_apply, ['shadcn', '--file']), (ua.cmd_compat, ['nope'])):
            with self.subTest(args=args):
                with self.assertRaises(ua.UsageError):
                    quiet(cmd, args)

    def test_find_without_arguments_prints_help(self):
        rc, out = quiet(ua.cmd_find, [])
        self.assertEqual(rc, 2)
        self.assertIn('usage: find.sh', out)

    def test_seed_may_be_zero(self):
        self.assertEqual(ua.take_int(iter(['0']), '--seed', low=0), 0)


class Compat(unittest.TestCase):
    def test_single_source_matches_the_first_column_only(self):
        rc, out = quiet(ua.cmd_compat, ['shadcn'])
        rows = [l for l in out.splitlines() if l.startswith('|')]
        self.assertTrue(any(l.startswith('| shadcn + uiarc ') for l in rows))
        # the uiarc and obsidianui summary rows mention shadcn only in their notes
        self.assertFalse(any(l.startswith('| uiarc |') or l.startswith('| obsidianui |') for l in rows))
        self.assertIn('任意底座都适用的组合', out)

    def test_pair(self):
        rc, out = quiet(ua.cmd_compat, ['shadcn', 'bencho'])
        rows = [l for l in out.splitlines() if l.startswith('|')]
        self.assertEqual(len(rows), 1)
        self.assertTrue(rows[0].startswith('| shadcn + bencho '))


if __name__ == '__main__':
    unittest.main()
