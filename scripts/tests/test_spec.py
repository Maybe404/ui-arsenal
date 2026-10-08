"""The documented source format (sources/_SPEC.md) must stay what audit enforces: a minimal source written from
the spec passes audit, and every field audit requires is in the spec's template."""
import contextlib
import importlib.util
import io
import os
import re
import shutil
import tempfile
import unittest
from unittest.mock import patch

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('ua', os.path.join(HERE, '..', 'ua.py'))
ua = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ua)
SPEC = os.path.join(HERE, '..', '..', 'sources', '_SPEC.md')


def template_fields():
    with open(SPEC, encoding='utf-8') as f:
        text = f.read()
    block = re.search(r'```\n---\n(.*?)\n---', text, re.S).group(1)
    return [l.split(':', 1)[0] for l in block.splitlines() if re.match(r'^[a-z_]+:', l)]


class SpecMatchesAudit(unittest.TestCase):
    def test_every_required_field_is_documented(self):
        self.assertEqual(sorted(set(ua.FRONTMATTER) - set(template_fields())), [])

    def test_minimal_source_from_the_spec_passes_audit(self):
        tmp = tempfile.mkdtemp()
        try:
            src, guides = os.path.join(tmp, 'sources'), os.path.join(tmp, 'guides')
            os.makedirs(src)
            os.makedirs(guides)
            values = {'id': 'demo', 'name': 'Demo', 'url': 'https://demo.invalid', 'kind': 'component-library',
                      'stack': 'React', 'license': 'MIT', 'pro': 'none', 'fetch': 'shadcn-registry',
                      'coverage': '全量：官方 registry', 'catalog_checked': '2026-10-08', 'source_status': 'active',
                      'visual_style': 'plain', 'foundation': 'none', 'styling': 'css-only', 'motion_lib': 'css',
                      'dark_mode': 'none', 'mixing_notes': '无'}
            with open(os.path.join(src, 'demo.md'), 'w', encoding='utf-8') as f:
                f.write('---\n%s\n---\n## 是什么\n示例\n' % '\n'.join('%s: %s' % (k, values[k]) for k in template_fields()))
            row = dict.fromkeys(ua.COLS, '')
            row.update(source='demo', id='button', name='Button', category='ui', url='https://demo.invalid/button',
                       fetch='npx shadcn add x', spec='registry:https://demo.invalid/r/button.json', access='free',
                       usage='install', framework='react', status='needs-review', last_seen='2026-10-08',
                       review='new:2026-10-08')
            with open(os.path.join(src, 'demo.tsv'), 'w', encoding='utf-8') as f:
                f.write('\t'.join(row[k] for k in ua.COLS) + '\n')
            with open(os.path.join(src, 'demo.notes.tsv'), 'w', encoding='utf-8') as f:
                f.write('\t'.join(['button', '按钮', 'button', 'foundation', '', '', '', '']) + '\n')
            out = io.StringIO()
            with patch.object(ua, 'SRC', src), patch.object(ua, 'GUIDES', guides), \
                    patch.object(ua, 'CLAIMS', os.path.join(src, '_claims.tsv')), contextlib.redirect_stdout(out):
                rc = ua.cmd_audit([])
            self.assertEqual(rc, 0, out.getvalue())
        finally:
            shutil.rmtree(tmp)


if __name__ == '__main__':
    unittest.main()
