#!/usr/bin/env python3
"""ui-arsenal catalogue tool: find / fetch / verify / refresh / stats / audit.

TSV schema (sources/<id>.tsv, no header, 9 tab-separated columns):
  source  item_id  name  category  description  fetch_human  access  usage  spec
access: free | login | pro | broken
usage:  install | source | prompt | reference
spec:   space-separated adapter tokens, each "<adapter>:<arg>":
        registry:<url>  url:<url>  doc:<url>  prompt:<page-url>
        script:<adapter> <arg>  browser:<url>  manual  none
Every fetch is read-only: files go to an output directory, nothing is installed or executed
except the bundled adapter scripts in scripts/adapters/.
"""
import hashlib
import html
import json
import os
import random
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'sources')
ADAPTERS = os.path.join(ROOT, 'scripts', 'adapters')
STATE = os.path.join(SRC, '_state.json')
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36'
ACCESS = ('free', 'login', 'pro', 'broken')
USAGE = ('install', 'source', 'prompt', 'reference')
USAGE_ZH = {'install': '可安装', 'source': '取源码', 'prompt': '提示词', 'reference': '仅参考'}
ADAPTER_KINDS = ('registry', 'url', 'doc', 'prompt', 'script', 'browser', 'manual', 'none')
COLS = ('source', 'id', 'name', 'category', 'desc', 'fetch', 'access', 'usage', 'spec')


# ---------- data ----------

def load_rows(source=None):
    rows = []
    for fn in sorted(os.listdir(SRC)):
        if not fn.endswith('.tsv') or fn.startswith('_'):
            continue
        if source and fn != source + '.tsv':
            continue
        with open(os.path.join(SRC, fn), encoding='utf-8') as f:
            for n, line in enumerate(f, 1):
                if line.strip():
                    r = dict(zip(COLS, line.rstrip('\n').split('\t')))
                    r['_file'], r['_line'] = fn, n
                    rows.append(r)
    if source and not rows:
        sys.exit('unknown source: %s (see: ua.py stats)' % source)
    return rows


def parse_spec(spec):
    """Split spec into [(kind, arg)]; 'script:bencho id' keeps its argument."""
    out, toks = [], spec.split()
    i = 0
    while i < len(toks):
        t = toks[i]
        kind, _, arg = t.partition(':')
        if kind == 'script':
            arg = arg + (' ' + toks[i + 1] if i + 1 < len(toks) and ':' not in toks[i + 1] else '')
            i += 1 if ' ' in arg else 0
        out.append((kind, arg))
        i += 1
    return out


def frontmatter(source):
    p = os.path.join(SRC, source + '.md')
    fm = {}
    if os.path.exists(p):
        txt = open(p, encoding='utf-8').read()
        m = re.match(r'---\n(.*?)\n---', txt, re.S)
        if m:
            for line in m.group(1).splitlines():
                k, _, v = line.partition(':')
                fm[k.strip()] = v.strip()
    return fm


def sources():
    return sorted(fn[:-3] for fn in os.listdir(SRC) if fn.endswith('.md') and not fn.startswith('_'))


# ---------- http ----------

def http(url, data_limit=None, tries=2, timeout=40):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read(data_limit) if data_limit else r.read()
                return r.status, r.headers.get('content-type', ''), body
        except urllib.error.HTTPError as e:
            return e.code, e.headers.get('content-type', '') if e.headers else '', b''
        except Exception as e:  # network error: retry once
            last = e
            time.sleep(1.5)
    return 0, '', str(last).encode()


def sha(b):
    return hashlib.sha256(b).hexdigest()


# ---------- find ----------

def load_groups():
    p = os.path.join(ROOT, 'scripts', 'aliases.json')
    groups = json.load(open(p, encoding='utf-8'))['groups']
    return [[t.lower() for t in g] for g in groups]


def concepts(token, groups, corpus):
    """Turn one query token into concepts: [(original_term, {alias terms})]."""
    t = token.lower()
    if any(t in c for c in corpus):
        alts = set()
        for g in groups:
            if t in g:
                alts.update(g)
        alts.discard(t)
        return [(t, alts)]
    # Compound Chinese like "磁吸选择": split into the group terms it contains.
    found = []
    for g in groups:
        hits = [m for m in g if len(m) >= 2 and m in t]
        if hits:
            found.append((max(hits, key=len), set(g) - {max(hits, key=len)}))
    return found or [(t, set())]


def term_re(term):
    # ASCII alias terms match whole words (plus plural), so "plan" does not hit "plane".
    if re.match(r'^[a-z0-9 -]+$', term):
        return re.compile(r'(?<![a-z0-9])' + re.escape(term) + r'(?:e?s)?(?![a-z0-9])')
    return re.compile(re.escape(term))


ICON_TERMS = {'图标', 'icon', 'glyph', 'svg'}


def score_row(r, cons, icon_query):
    fields = ((3, (r['id'] + ' ' + r['name']).lower()), (2, r['category'].lower()), (1, r['desc'].lower()))
    s, hit = 0.0, 0
    for orig, alts in cons:
        best = 0.0
        for w, text in fields:
            if orig in text:
                best = max(best, w + 1.0)
            elif any(rx.search(text) for rx in alts):
                best = max(best, w * 0.6)
        if best:
            hit += 1
            s += best
    if not hit:
        return None, 0
    s += {'install': 4, 'source': 3.5, 'prompt': 3, 'reference': 0}.get(r['usage'], 0)
    s += {'free': 1, 'login': 0, 'pro': -5, 'broken': -6}.get(r['access'], 0)
    if r['source'] == 'lucide' and not icon_query:
        s -= 4
    return s, hit


def cmd_find(args):
    src, limit, mode, terms = None, 25, 'default', []
    it = iter(args)
    for a in it:
        if a == '-s':
            src = next(it)
        elif a == '--limit':
            limit = int(next(it))
        elif a in ('--all', '--free', '--code', '--ref'):
            mode = a[2:]
        else:
            terms.append(a)
    rows = load_rows(src)
    if mode == 'all':
        pass
    elif mode == 'free':
        rows = [r for r in rows if r['access'] == 'free']
    else:
        rows = [r for r in rows if r['access'] in ('free', 'login')]
    if mode == 'code':
        rows = [r for r in rows if r['usage'] != 'reference']
    if mode == 'ref':
        rows = [r for r in rows if r['usage'] == 'reference']
    groups = load_groups()
    corpus = [(r['id'] + ' ' + r['name'] + ' ' + r['category'] + ' ' + r['desc']).lower() for r in rows]
    cons = [(o, [term_re(a) for a in alts]) for t in terms for o, alts in concepts(t, groups, corpus)]
    icon_query = any(o in ICON_TERMS or ICON_TERMS & {a.pattern for a in alts} for o, alts in cons) or any(
        t.lower() in ICON_TERMS for t in terms)
    scored = []
    for r in rows:
        s, hit = score_row(r, cons, icon_query) if cons else (0, 0)
        if s is not None:
            scored.append((hit, s, r))
    note = ''
    if cons and scored:
        top = max(h for h, _, _ in scored)
        if top < len(cons):
            note = '（没有条目同时命中全部 %d 个词，以下是命中 %d 个的结果）' % (len(cons), top)
        scored = [x for x in scored if x[0] == top]
    scored = [(s, r) for _, s, r in sorted(scored, key=lambda x: (-x[0], -x[1]))]
    if not scored:
        print('no match. 试试更短的词、英文词，或加 --all 包含 Pro')
        return 1
    by_src = {}
    for _, r in scored:
        by_src[r['source']] = by_src.get(r['source'], 0) + 1
    print('%d matches (%s)  filter=%s %s' % (len(scored), ', '.join('%s %d' % kv for kv in sorted(by_src.items(), key=lambda x: -x[1])), mode, note))
    for s, r in scored[:limit]:
        tag = USAGE_ZH.get(r['usage'], r['usage']) + ('' if r['access'] == 'free' else '·' + r['access'])
        print('[%s] %s:%s — %s (%s)' % (tag, r['source'], r['id'], r['name'], r['category']))
        print('    %s' % r['desc'][:160])
    if len(scored) > limit:
        print('... %d more (--limit N)' % (len(scored) - limit))
    print('\n下一步: ua.py fetch <source:id>   （仅参考类条目会给出打开方式）')
    return 0


# ---------- fetch ----------

def find_row(ref):
    if ':' not in ref:
        sys.exit('use <source>:<item_id>, e.g. bencho:magnet-select')
    source, iid = ref.split(':', 1)
    for r in load_rows(source):
        if r['id'] == iid:
            return r
    cands = [r['id'] for r in load_rows(source) if iid.lower() in r['id'].lower()][:10]
    sys.exit('not found: %s%s' % (ref, ('  close: ' + ', '.join(cands)) if cands else ''))


def save(out, name, body):
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, name)
    with open(p, 'wb') as f:
        f.write(body)
    return p


def do_registry(url, out, opts):
    if opts.get('variant'):
        url = re.sub(r'-(TS|JS)-(TW|CSS)(\.json)?$', '-%s.json' % opts['variant'], url)
    if opts.get('style'):
        url = re.sub(r'/styles/[^/]+/', '/styles/%s/' % opts['style'], url)
    st, ct, body = http(url)
    if st != 200:
        return False, 'HTTP %s %s' % (st, url)
    try:
        d = json.loads(body)
    except ValueError:
        return False, 'not JSON (HTML fallback?) %s' % url
    files = d.get('files') or []
    if not files and d.get('type') not in ('registry:style', 'registry:theme', 'registry:font', 'registry:base'):
        return False, 'registry item has no files %s' % url
    save(out, 'registry-item.json', body)
    lines = []
    for f in files:
        content = f.get('content')
        if content is None:
            return False, 'file without content: %s (%s)' % (f.get('path'), url)
        p = save(out, os.path.basename(f.get('path') or 'file'), content.encode())
        lines.append('    %s (%d lines) <- %s' % (p, content.count('\n') + 1, f.get('path')))
    info = ['registry  %s' % url, '  sha256 %s' % sha(body)[:16]]
    for k in ('dependencies', 'devDependencies', 'registryDependencies'):
        if d.get(k):
            info.append('  %s: %s' % (k, ' '.join(d[k])))
    if d.get('cssVars') or d.get('css'):
        info.append('  注意: 含 cssVars/css，需要合并进全局样式（见 registry-item.json）')
    return True, '\n'.join(info + ['  files:'] + lines)


def do_url(url, out, label='url'):
    st, ct, body = http(url)
    if st != 200 or not body:
        return False, 'HTTP %s %s' % (st, url)
    if label == 'doc' and 'text/html' in ct and not url.endswith('.html'):
        return False, 'got HTML instead of a document %s' % url
    name = os.path.basename(url.split('?')[0]) or 'index'
    name = urllib.request.unquote(name)
    if label == 'doc' and '.' not in name:
        name += '.md'
    p = save(out, ('doc-' if label == 'doc' else '') + name, body)
    return True, '%-9s %s\n  -> %s (%d bytes, sha256 %s)' % (label, url, p, len(body), sha(body)[:16])


def do_prompt(url, out):
    st, ct, body = http(url)
    m = re.search(r'<pre id="agent-prompt"[^>]*>(.*?)</pre>', body.decode('utf-8', 'replace'), re.S) if st == 200 else None
    if not m:
        return False, 'prompt block not found (HTTP %s) %s' % (st, url)
    txt = html.unescape(m.group(1)).strip()
    p = save(out, 'prompt.md', txt.encode())
    return True, 'prompt    %s\n  -> %s (%d chars)' % (url, p, len(txt))


def do_script(arg, out, opts):
    name, _, a = arg.partition(' ')
    path = os.path.join(ADAPTERS, name + '.sh')
    if not os.path.exists(path):
        return False, 'missing adapter %s' % path
    cmd = ['sh', path, a] + ([str(opts['limit'])] if opts.get('limit') else [])
    r = subprocess.run(cmd, capture_output=True, timeout=180)
    if r.returncode != 0 or not r.stdout.strip():
        return False, 'adapter %s failed: %s' % (name, r.stderr.decode()[-300:])
    p = save(out, '%s-%s.txt' % (name, re.sub(r'[^A-Za-z0-9_-]', '_', a)), r.stdout)
    return True, 'script    %s %s\n  -> %s (%d bytes, sha256 %s)' % (name, a, p, len(r.stdout), sha(r.stdout)[:16])


def cmd_fetch(args):
    opts, refs = {}, []
    it = iter(args)
    for a in it:
        if a == '--out':
            opts['out'] = next(it)
        elif a == '--variant':
            opts['variant'] = next(it)
        elif a == '--style':
            opts['style'] = next(it)
        elif a == '--limit':
            opts['limit'] = int(next(it))
        else:
            refs.append(a)
    if not refs:
        sys.exit('usage: ua.py fetch <source:id> [--out DIR] [--variant JS-CSS] [--style base-nova] [--limit N]')
    rc = 0
    for ref in refs:
        rc |= fetch_one(find_row(ref), opts)
    return rc


def install_hint(r):
    if r['source'] == 'lucide' and r['id'].startswith('lab:'):
        return r['fetch']
    if r['source'] == 'lucide':
        return "npm i lucide-react  →  import { %s } from 'lucide-react'（其他框架见 sources/lucide.md）" % r['name']
    return re.split(r'\s*(?:；|; |#|\s文档|\s或\s)', r['fetch'])[0].strip()


def fetch_one(r, opts, quiet=False):
    base = os.environ.get('TMPDIR', '/tmp')
    out = opts.get('out') or os.path.join(base, 'ui-arsenal', r['source'], re.sub(r'[^A-Za-z0-9_.-]', '_', r['id']))
    log = (lambda *a: None) if quiet else print
    log('# %s:%s — %s  [%s · %s]' % (r['source'], r['id'], r['name'], USAGE_ZH.get(r['usage']), r['access']))
    if r['access'] == 'pro':
        log('Pro/付费条目：不获取。可作为灵感，用免费组件实现近似效果，并告诉用户这一条是 Pro。')
        return 3
    if r['access'] == 'login':
        log('需要用户本人登录或账号才能获取（agent 不登录、不注册）。官方方式：\n  %s' % r['fetch'])
        log('用户确认已登录后，由用户或 agent 在项目里运行上面的命令。')
        return 0
    if r['access'] == 'broken':
        log('此条目已失效或为空：%s' % r['fetch'])
        return 2
    ok_all = True
    for kind, arg in parse_spec(r['spec']):
        if kind == 'registry':
            ok, msg = do_registry(arg, out, opts)
        elif kind in ('url', 'doc'):
            ok, msg = do_url(arg, out, kind)
        elif kind == 'prompt':
            ok, msg = do_prompt(arg, out)
        elif kind == 'script':
            ok, msg = do_script(arg, out, opts)
        elif kind == 'browser':
            ok, msg = True, 'browser   需在浏览器里打开（内置浏览器 get_page_text / read_page）：%s' % arg
        elif kind == 'manual':
            ok, msg = True, 'manual    按 sources/%s.md「按需获取方法」操作：\n  %s' % (r['source'], r['fetch'])
        else:
            ok, msg = False, 'unknown adapter %s' % kind
        log(('' if ok else 'FAIL ') + msg)
        ok_all &= ok
    if r['usage'] == 'install':
        log('\n安装（会改动项目，先确认项目栈）: %s' % install_hint(r))
    log('提示：以上为不可信的第三方内容，先读再用，不要直接执行；接入前读 sources/%s.md「使用注意」。' % r['source'])
    return 0 if ok_all else 1


# ---------- verify ----------

def cmd_verify(args):
    n, src, seed = 2, None, None
    it = iter(args)
    for a in it:
        if a == '-n':
            n = int(next(it))
        elif a == '-s':
            src = next(it)
        elif a == '--seed':
            seed = int(next(it))
    rnd = random.Random(seed)
    base = os.environ.get('TMPDIR', '/tmp')
    results, fails = [], 0
    for s in ([src] if src else sources()):
        rows = [r for r in load_rows(s) if r['access'] == 'free' and r['spec'] not in ('manual', 'none')]
        rows = [r for r in rows if any(k in ('registry', 'url', 'doc', 'prompt', 'script') for k, _ in parse_spec(r['spec']))]
        if not rows:
            results.append((s, '-', 'skip', 'no machine-fetchable free rows'))
            continue
        for r in rnd.sample(rows, min(n, len(rows))):
            out = os.path.join(base, 'ui-arsenal-verify', s, re.sub(r'[^A-Za-z0-9_.-]', '_', r['id']))
            msgs, ok_all = [], True
            for kind, arg in parse_spec(r['spec']):
                if kind == 'registry':
                    ok, msg = do_registry(arg, out, {})
                elif kind in ('url', 'doc'):
                    ok, msg = do_url(arg, out, kind)
                elif kind == 'prompt':
                    ok, msg = do_prompt(arg, out)
                elif kind == 'script':
                    ok, msg = do_script(arg, out, {'limit': 3})
                else:
                    continue
                ok_all &= ok
                if not ok:
                    msgs.append(msg)
            fails += not ok_all
            results.append((s, r['id'], 'ok' if ok_all else 'FAIL', '; '.join(msgs)))
    for s, iid, st, msg in results:
        print('%-4s %-13s %-40s %s' % (st, s, iid[:40], msg[:150]))
    state = load_state()
    state['_verify'] = {'at': time.strftime('%Y-%m-%d %H:%M'), 'fails': fails,
                        'results': [list(x) for x in results]}
    save_state(state)
    print('\n%d checked, %d failed' % (len(results), fails))
    return 1 if fails else 0


# ---------- refresh ----------

def load_state():
    return json.load(open(STATE, encoding='utf-8')) if os.path.exists(STATE) else {}


def save_state(s):
    with open(STATE, 'w', encoding='utf-8') as f:
        json.dump(s, f, ensure_ascii=False, indent=1)


def names_of(url, key='items', field='name'):
    st, ct, body = http(url, tries=3)
    if st != 200:
        raise RuntimeError('HTTP %s %s' % (st, url))
    d = json.loads(body)
    return {x[field] for x in d[key]}, sha(body)


def reg_local(s, strip=None, must=None):
    out = set()
    for r in load_rows(s):
        for k, a in parse_spec(r['spec']):
            if k == 'registry' and (not must or must in a):
                n = os.path.basename(a)[:-5] if a.endswith('.json') else os.path.basename(a)
                out.add(re.sub(strip, '', n) if strip else n)
    return out


def ids_local(s, access=None):
    return {r['id'] for r in load_rows(s) if not r['id'].startswith('category:') and (not access or r['access'] in access)}


def r_shadcn():
    names, h = set(), []
    for st in ('base-nova', 'radix-nova', 'aria-nova', 'new-york-v4'):
        n, x = names_of('https://ui.shadcn.com/r/styles/%s/registry.json' % st)
        names |= n
        h.append(x)
    return names - {'index', 'style'}, reg_local('shadcn', must='/styles/'), sha(''.join(h).encode())


def r_simple(source, url, strip=None, ignore=()):
    def f():
        n, h = names_of(url)
        n -= set(ignore)
        if strip:
            n = {re.sub(strip, '', x) for x in n}
        return n, reg_local(source, strip), h
    return f


def r_lucide():
    st, ct, body = http('https://unpkg.com/lucide-static@latest/tags.json', tries=3)
    if st != 200:
        raise RuntimeError('HTTP %s' % st)
    remote = set(json.loads(body))
    st2, _, meta = http('https://unpkg.com/@lucide/lab@latest/?meta', tries=3)
    if st2 == 200:
        def walk(n):
            for f in n.get('files', []):
                yield from (walk(f) if f.get('type') == 'directory' else [f['path']])
        remote |= {'lab:' + os.path.basename(f)[:-3] for f in walk(json.loads(meta))
                   if f.startswith('/dist/esm/icons/') and f.endswith('.js')}
    local = {r['id'] for r in load_rows('lucide') if r['access'] == 'free'}
    return remote, local, sha(body + meta)


def r_originkit():
    n, h = names_of('https://mcp.originkit.dev/v1/registry', key='components')
    return n, {r['id'] for r in load_rows('originkit') if r['category'] != 'template'}, h


def r_bencho():
    st, ct, body = http('https://bencho.dev/llms.txt', tries=3)
    if st != 200:
        raise RuntimeError('HTTP %s' % st)
    ids = set(re.findall(r'bencho\.dev/blocks/([a-z0-9-]+)', body.decode()))
    st2, _, sm = http('https://bencho.dev/sitemap.xml', tries=3)
    if st2 == 200:
        ids |= {'find:' + x for x in re.findall(r'bencho\.dev/finds/([A-Za-z0-9_-]+)<', sm.decode())}
        body += sm
    parked = {r['id'] for r in load_rows('bencho') if '未在站点上架' in r['desc'] or 'parked' in r['desc']}
    return ids, ids_local('bencho') - parked, sha(body)


def r_getdesign():
    st, ct, body = http('https://getdesign.md/sitemap.xml', tries=3)
    if st != 200:
        raise RuntimeError('HTTP %s' % st)
    free = set(re.findall(r'https://getdesign\.md/([^/<]+)/design-md<', body.decode()))
    catalog = {'site:' + x for x in re.findall(r'https://getdesign\.md/design-md/([^/<]+)<', body.decode())}
    local = {r['id'] for r in load_rows('getdesign') if r['usage'] == 'prompt' or r['id'].startswith('site:')}
    return free | catalog, local, sha(body)


REFRESH = {
    'shadcn': r_shadcn,
    'reactbits': r_simple('reactbits', 'https://reactbits.dev/r/registry.json', strip=r'-(JS|TS)-(CSS|TW)$'),
    'uiarc': r_simple('uiarc', 'https://uiarc.dev/r/registry.json'),
    'obsidianui': r_simple('obsidianui', 'https://www.obsidianui.dev/r/registry.json'),
    'beautifului': r_simple('beautifului', 'https://www.beautifului.dev/r/registry.json'),
    'loadingui': r_simple('loadingui', 'https://loading-ui.com/r/registry.json', ignore=('index', 'style', 'utils')),
    'lucide': r_lucide,
    'originkit': r_originkit,
    'bencho': r_bencho,
    'getdesign': r_getdesign,
}
NO_REFRESH = {
    'designspells': '站点有 Vercel 反爬，只能在浏览器里更新（见 designspells.md）',
    'inspora': 'robots.txt 禁止 /api/，不自动刷新；人工快照',
    'collectui': '按分类实时查询（script:collectui），清单只到分类级，无需刷新条目',
    'jakubantalik': '个人站 + GitHub，条目少，人工维护',
    'librariesdev': '固定 7 个库，人工维护',
}


def cmd_refresh(args):
    targets = [a for a in args if not a.startswith('-')] or sorted(set(sources()))
    state, rc = load_state(), 0
    for s in targets:
        if s not in REFRESH:
            print('%-13s skip  %s' % (s, NO_REFRESH.get(s, 'no refresh adapter')))
            continue
        try:
            remote, local, h = REFRESH[s]()
        except Exception as e:
            print('%-13s ERROR %s' % (s, e))
            rc = 1
            continue
        prev = state.get(s, {})
        added, removed = sorted(remote - local), sorted(local - remote)
        changed = prev.get('sha256') not in (None, h)
        state[s] = {'checked_at': time.strftime('%Y-%m-%d %H:%M'), 'sha256': h, 'remote': len(remote),
                    'local': len(local), 'added': added, 'removed': removed}
        print('%-13s remote %4d  local %4d  new %3d  gone %3d%s' % (
            s, len(remote), len(local), len(added), len(removed), '  (index changed since last refresh)' if changed else ''))
        if added:
            print('    new:  ' + ' '.join(added[:30]) + (' ...' if len(added) > 30 else ''))
        if removed:
            print('    gone: ' + ' '.join(removed[:30]) + (' ...' if len(removed) > 30 else ''))
    save_state(state)
    print('\nrefresh 只报告差异，不改 TSV。新条目要补中文描述后按 _ADDING.md 写入。')
    return rc


# ---------- stats / audit ----------

def cmd_stats(args):
    md = '--md' in args or '--write-skill' in args
    buf = []
    out = buf.append if '--write-skill' in args else print
    rows_all = load_rows()
    hdr = ('source', 'items', 'categories', 'free', 'login', 'pro', 'broken', 'install', 'source', 'prompt', 'reference')
    table = []
    for s in sources():
        rs = [r for r in rows_all if r['source'] == s]
        cat = sum(r['id'].startswith('category:') for r in rs)
        c = lambda k, v: sum(r[k] == v for r in rs)
        table.append((s, len(rs) - cat, cat) + tuple(c('access', a) for a in ACCESS) + tuple(c('usage', u) for u in USAGE))
    if md:
        out('| 来源 | 名称 | 类型 | 条目 | 分类行 | 免费 | 需登录 | Pro | 失效 | 用法分布 |')
        out('|---|---|---|---|---|---|---|---|---|---|')
        for t in table:
            fm = frontmatter(t[0])
            mix = ' '.join('%s %d' % (USAGE_ZH[u], t[7 + i]) for i, u in enumerate(USAGE) if t[7 + i])
            out('| %s | [%s](%s) | %s | %d | %s | %d | %d | %d | %d | %s |' % (
                t[0], fm.get('name', t[0]), fm.get('url', ''), fm.get('kind', ''), t[1], t[2] or '', t[3], t[4], t[5], t[6], mix))
    else:
        out(('%-13s' + ' %9s' * (len(hdr) - 1)) % hdr)
        for t in table:
            out(('%-13s' + ' %9d' * (len(hdr) - 1)) % t)
        tot = tuple(sum(t[i] for t in table) for i in range(1, len(hdr)))
        out(('%-13s' + ' %9d' * (len(hdr) - 1)) % (('TOTAL',) + tot))
    if '--write-skill' in args:
        p = os.path.join(ROOT, 'SKILL.md')
        txt = open(p, encoding='utf-8').read()
        txt = re.sub(r'<!-- STATS:BEGIN -->.*?<!-- STATS:END -->',
                     lambda m: '<!-- STATS:BEGIN -->\n' + '\n'.join(buf) + '\n<!-- STATS:END -->', txt, flags=re.S)
        open(p, 'w', encoding='utf-8').write(txt)
        sys.stdout.write('SKILL.md stats table updated (%d sources)\n' % len(table))
    return 0


def cmd_audit(args):
    errs = []
    for s in sources():
        fm = frontmatter(s)
        for k in ('id', 'name', 'url', 'kind', 'pro', 'fetch', 'verified'):
            if k not in fm:
                errs.append('%s.md: missing frontmatter %s' % (s, k))
        if not os.path.exists(os.path.join(SRC, s + '.tsv')):
            errs.append('%s: missing tsv' % s)
    seen = {}
    for fn in sorted(os.listdir(SRC)):
        if not fn.endswith('.tsv'):
            continue
        s = fn[:-4]
        for n, line in enumerate(open(os.path.join(SRC, fn), encoding='utf-8'), 1):
            if not line.strip():
                continue
            c = line.rstrip('\n').split('\t')
            where = '%s:%d' % (fn, n)
            if len(c) != 9:
                errs.append('%s: %d columns (need 9)' % (where, len(c)))
                continue
            if c[0] != s:
                errs.append('%s: source column %r != %r' % (where, c[0], s))
            if c[6] not in ACCESS:
                errs.append('%s: access %r' % (where, c[6]))
            if c[7] not in USAGE:
                errs.append('%s: usage %r' % (where, c[7]))
            key = (s, c[1])
            if key in seen:
                errs.append('%s: duplicate id %s (also line %d)' % (where, c[1], seen[key]))
            seen[key] = n
            for k, a in parse_spec(c[8]):
                if k not in ADAPTER_KINDS:
                    errs.append('%s: spec adapter %r' % (where, k))
                elif k in ('registry', 'url', 'doc', 'prompt', 'browser') and not a.startswith('https://'):
                    errs.append('%s: spec %s needs https url' % (where, k))
                elif k == 'script' and not os.path.exists(os.path.join(ADAPTERS, a.split()[0] + '.sh')):
                    errs.append('%s: missing adapter %s' % (where, a))
            if c[6] == 'pro' and c[8] != 'none':
                errs.append('%s: pro row must have spec none' % where)
    for e in errs[:200]:
        print(e)
    print('%d rows checked, %d problems' % (len(seen), len(errs)))
    return 1 if errs else 0


CMDS = {'find': cmd_find, 'fetch': cmd_fetch, 'verify': cmd_verify, 'refresh': cmd_refresh,
        'stats': cmd_stats, 'audit': cmd_audit}

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print(__doc__)
        print('commands: ' + ' '.join(CMDS))
        sys.exit(2)
    sys.exit(CMDS[sys.argv[1]](sys.argv[2:]))
