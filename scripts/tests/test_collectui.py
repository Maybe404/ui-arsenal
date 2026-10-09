"""Offline tests for the Collect UI adapter: every failure names its step, an empty category is not an error,
and the key never appears in the output. Network calls are replaced by a fake `get`."""
import importlib.util
import io
import json
import os
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('collectui', os.path.join(HERE, '..', 'adapters', 'collectui.py'))
cu = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cu)

KEY = 'eyJfixture.eyJfixture.fixturesig'


def site(path_to_text):
    def fake_get(url, headers=None, started=None):
        if url.startswith(cu.API):
            return path_to_text['API']
        for suffix, value in path_to_text.items():
            if suffix != 'API' and url.endswith(suffix):
                if isinstance(value, Exception):
                    raise value
                return value
        return 404, 'text/html', 'not found'
    return fake_get


def pages(api, key=KEY):
    return {'collectui.com/': (200, 'text/html', 'x _app/immutable/entry/app.F1.js x'),
            'entry/app.F1.js': (200, 'text/javascript', 'import "nodes/1.N1.js"'),
            'nodes/1.N1.js': (200, 'text/javascript', 'import "chunks/C1.js"'),
            'chunks/C1.js': (200, 'text/javascript', 'const k="%s"' % key if key else 'nothing here'),
            'API': api}


def run(fake, slug='dashboard'):
    out, err = io.StringIO(), io.StringIO()
    with patch.object(cu, 'get', side_effect=fake), redirect_stdout(out), redirect_stderr(err):
        rc = cu.main(['collectui.py', slug, '3'])
    return rc, out.getvalue(), err.getvalue()


class CollectUI(unittest.TestCase):
    def test_posts(self):
        posts = [{'media_type': 'image', 'title': 'line one\nline two', 'media_url': 'https://cdn/x.avif',
                  'source_url': 'https://x.com/p'}]
        rc, out, err = run(site(pages((200, 'application/json', json.dumps(posts)))))
        self.assertEqual(rc, 0)
        self.assertIn('image\tline one line two\thttps://cdn/x.avif\thttps://x.com/p', out)

    def test_empty_category_is_a_result_not_an_error(self):
        rc, out, err = run(site(pages((200, 'application/json', '[]'))))
        self.assertEqual(rc, 0)
        self.assertIn('# 0 posts', out)

    def test_permission_error_with_status(self):
        rc, out, err = run(site(pages((401, 'application/json', '{"message":"permission denied for table"}'))))
        self.assertEqual((rc, out), (1, ''))
        self.assertIn('API refused the request (HTTP 401: permission denied', err)

    def test_error_object_with_200(self):
        rc, out, err = run(site(pages((200, 'application/json', '{"message":"JWT expired"}'))))
        self.assertEqual(rc, 1)
        self.assertIn('error object instead of posts: JWT expired', err)

    def test_html_or_bad_json_from_api(self):
        for body, ct in (('<!doctype html><html></html>', 'text/html'), ('{"broken": ', 'application/json')):
            rc, out, err = run(site(pages((200, ct, body))))
            self.assertEqual(rc, 1)
            self.assertIn('not JSON', err)

    def test_key_not_found(self):
        rc, out, err = run(site(pages((200, 'application/json', '[]'), key=None)))
        self.assertEqual(rc, 1)
        self.assertIn('anon key not found', err)

    def test_site_http_error_and_timeout(self):
        p = pages((200, 'application/json', '[]'))
        p['collectui.com/'] = (503, 'text/html', '')
        rc, out, err = run(site(p))
        self.assertIn('HTTP 503 fetching https://collectui.com/', err)
        p = pages((200, 'application/json', '[]'))
        p['entry/app.F1.js'] = cu.Failure('network error fetching https://collectui.com/x: timed out')
        rc, out, err = run(site(p))
        self.assertEqual(rc, 1)
        self.assertIn('timed out', err)

    def test_key_never_printed(self):
        for api in ((401, 'application/json', '{"message":"no"}'), (200, 'application/json', '[]')):
            rc, out, err = run(site(pages(api)))
            self.assertNotIn(KEY, out + err)

    def test_failures_point_to_the_browser_fallback(self):
        rc, out, err = run(site(pages((500, 'text/plain', 'x'))))
        self.assertIn('fallback: open https://collectui.com/designs/dashboard-ui-design-inspiration', err)


if __name__ == '__main__':
    unittest.main()
