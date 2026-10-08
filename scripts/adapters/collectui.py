#!/usr/bin/env python3
"""List the latest published Collect UI posts in one category (read-only GET on the public anon API).

usage: collectui.py <category-slug> [limit]

The site is a SvelteKit app; the public anon key the app itself uses is read from its JS chunks as text (nothing
is executed). Every request has its own timeout and the whole run has a deadline. Each failure names the step that
failed (site page, bundle, key, API status, API payload) and never prints the key. A category the API returns no
posts for is a normal result ("# 0 posts"), not an error.
"""
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

SITE = 'https://collectui.com'
API = 'https://tuzpqmdnxvlzwqthgseg.supabase.co/rest/v1'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36'
REQUEST_TIMEOUT = 20
DEADLINE = 150  # seconds for the whole run; ua.py kills adapters after 180
FALLBACK = 'open https://collectui.com/designs/%s-ui-design-inspiration in a browser (see sources/collectui.md)'
KEY = re.compile(r'eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*')


class Failure(Exception):
    pass


def get(url, headers=None, started=None):
    """GET a URL; returns (status, content_type, text). Raises Failure on network errors and timeouts."""
    if started is not None and time.monotonic() - started > DEADLINE:
        raise Failure('gave up after %ds without finishing (site or network slow)' % DEADLINE)
    req = urllib.request.Request(url, headers=dict({'User-Agent': UA, 'Accept': '*/*'}, **(headers or {})))
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as r:
            return r.status, r.headers.get('content-type', ''), r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get('content-type', '') if e.headers else '', e.read().decode('utf-8', 'replace')
    except Exception as e:  # URLError, socket.timeout, connection reset
        raise Failure('network error fetching %s: %s' % (url.split('?')[0], getattr(e, 'reason', e)))


def site_text(path, started):
    st, ct, body = get(SITE + path, started=started)
    if st != 200:
        raise Failure('HTTP %d fetching %s%s' % (st, SITE, path))
    return body


def find_key(started):
    """The public anon key the web app ships, found by walking entry -> nodes -> chunks."""
    app = re.search(r'_app/immutable/entry/app\.[A-Za-z0-9_-]+\.js', site_text('/', started))
    if not app:
        raise Failure('app bundle not found on the home page (site changed?)')
    nodes = sorted(set(re.findall(r'nodes/[0-9]+\.[A-Za-z0-9_-]+\.js', site_text('/' + app.group(0), started))))
    if not nodes:
        raise Failure('no route chunks found in the app bundle (site changed?)')
    seen = set()
    for n in nodes:
        for c in re.findall(r'chunks/[A-Za-z0-9_-]+\.js', site_text('/_app/immutable/' + n, started)):
            if c in seen:
                continue
            seen.add(c)
            m = KEY.search(site_text('/_app/immutable/' + c, started))
            if m:
                return m.group(0)
    raise Failure('anon key not found in %d chunks (site changed?)' % len(seen))


def api_posts(slug, limit, key, started):
    q = urllib.parse.urlencode({
        'select': 'title,media_type,media_url,thumbnail,source_url,categories,created_at',
        'status': 'eq.Published', 'categories': 'cs.{%s}' % slug, 'order': 'created_at.desc,id.desc', 'limit': limit})
    st, ct, body = get('%s/collectui_posts?%s' % (API, q), {'apikey': key, 'Authorization': 'Bearer ' + key}, started)
    try:
        data = json.loads(body) if body.strip() else None
    except ValueError:
        data = None
        if st == 200:
            raise Failure('API returned something that is not JSON (HTTP 200, %s)' % (ct or 'no content type'))
    if st != 200:
        msg = data.get('message') or data.get('error') if isinstance(data, dict) else ''
        raise Failure('API refused the request (HTTP %d%s)' % (st, ': ' + str(msg)[:160] if msg else ''))
    if isinstance(data, dict):  # PostgREST reports permission and query errors as an object
        raise Failure('API returned an error object instead of posts: %s' % str(
            data.get('message') or data.get('error') or data)[:160])
    if not isinstance(data, list):
        raise Failure('API returned %s instead of a list of posts' % type(data).__name__)
    return data


def main(argv):
    if len(argv) < 2:
        raise SystemExit(__doc__)
    slug = argv[1]
    limit = int(argv[2]) if len(argv) > 2 else 20
    started = time.monotonic()
    try:
        posts = api_posts(slug, limit, find_key(started), started)
    except Failure as e:
        sys.stderr.write('collectui: %s; fallback: %s\n' % (e, FALLBACK % slug))
        return 1
    if not posts:
        print('# 0 posts: the API returned an empty list for category %r (empty or renamed category; '
              'counts per category: https://collectui.com/categories)' % slug)
        return 0
    for p in posts:
        title = ' '.join(str(p.get('title') or '').split())  # titles are tweets: may hold newlines and tabs
        print('%s\t%s\t%s\t%s' % (p.get('media_type'), title, p.get('media_url'), p.get('source_url') or ''))
    print('# %d posts. 图片 avif→png: sips -s format png x.avif --out x.png ; '
          '视频抽帧: ffmpeg -i x.mp4 -vf fps=1/3,scale=960:-1,tile=2x2 -frames:v 1 grid.png' % len(posts))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
