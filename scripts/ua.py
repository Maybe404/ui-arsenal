#!/usr/bin/env python3
"""ui-arsenal catalogue tool: find / fetch / verify / refresh / stats / audit.

Data model (per source, no headers, tab-separated):
  sources/<id>.tsv        machine-managed, written only by an approved refresh/apply (15 columns):
    source item_id title category official_url fetch_human spec access usage
    framework deps item_status alias_of last_seen fingerprint
  sources/<id>.notes.tsv  human-curated, never touched by refresh (8 columns):
    item_id desc_zh task layer visual_tags interaction_tags risk notes
access: free | login | pro | broken          usage: install | source | prompt | reference
item_status: active | needs-review | removed layer: foundation | specialized | reference | icons | design-spec
spec:   space-separated adapter tokens, each "<adapter>:<arg>":
        registry:<url>  url:<url>  doc:<url>  prompt:<page-url>
        script:<adapter> <arg>  browser:<url>  manual  none
Every fetch is read-only: files go to an output directory and nothing is installed.
Remote content is never executed: adapters in scripts/adapters/ (*.py or *.sh) only download
text and parse it (bencho.py parses the site bundle as a pure literal and refuses anything else).
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
COLS = ('source', 'id', 'name', 'category', 'url', 'fetch', 'spec', 'access', 'usage',
        'framework', 'deps', 'status', 'alias_of', 'last_seen', 'fingerprint')
NOTE_COLS = ('id', 'desc', 'task', 'layer', 'vtags', 'itags', 'risk', 'notes')
STATUS = ('active', 'needs-review', 'removed')
LAYERS = ('foundation', 'specialized', 'reference', 'icons', 'design-spec')
TASKS = ('icon', 'design-system', 'template', 'auth', 'pricing', 'chart', 'table', 'ai-ux', 'loading', 'text-effect',
         'background', 'cursor-effect', 'overlay', 'navigation', 'feedback', 'search-command', 'date-time', 'upload',
         'select', 'toggle-slider', 'form-input', 'button', 'media', 'avatar-user', 'marketing-section',
         'empty-onboarding', 'layout-card', 'motion-transition', 'micro-interaction', 'fun-3d', 'page-inspiration',
         'other')
RISKS = ('gradient-text', 'marquee', 'glow', 'grid-background', 'typewriter', 'bounce', 'glass', 'pulse-dot')


# ---------- data ----------

def load_notes(source):
    notes = {}
    p = os.path.join(SRC, source + '.notes.tsv')
    if os.path.exists(p):
        for line in open(p, encoding='utf-8'):
            if line.strip():
                c = line.rstrip('\n').split('\t')
                notes[c[0]] = dict(zip(NOTE_COLS, c))
    return notes


def load_rows(source=None, include_removed=False):
    """Machine rows joined with human notes. Removed items are hidden unless asked for."""
    rows = []
    for fn in sorted(os.listdir(SRC)):
        if not fn.endswith('.tsv') or fn.startswith('_') or fn.endswith('.notes.tsv'):
            continue
        sid = fn[:-4]
        if source and sid != source:
            continue
        notes = load_notes(sid)
        with open(os.path.join(SRC, fn), encoding='utf-8') as f:
            for n, line in enumerate(f, 1):
                if line.strip():
                    r = dict(zip(COLS, line.rstrip('\n').split('\t')))
                    r.update({k: v for k, v in notes.get(r['id'], {}).items() if k != 'id'})
                    for k in NOTE_COLS[1:]:
                        r.setdefault(k, '')
                    r['_file'], r['_line'] = fn, n
                    if include_removed or r.get('status') != 'removed':
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


def relevance(r, cons):
    """Field-weighted match score; returns (score, concepts hit)."""
    primary, _, secondary = r['task'].partition(',')
    fields = ((3, (r['id'] + ' ' + r['name']).lower()), (2, (r['category'] + ' ' + primary).lower()),
              (1, ' '.join((r['desc'], secondary, r['vtags'], r['itags'])).lower()))
    s, hit = 0.0, 0
    for orig, alts in cons:
        scores = []
        for w, text in fields:
            if orig in text:
                scores.append(w + 1.0)
            elif any(rx.search(text) for rx in alts):
                scores.append(w * 0.6)
        if scores:
            hit += 1
            # Best field counts fully; corroborating fields (e.g. category "Backgrounds" + desc "背景") add a bonus.
            s += max(scores) + 0.5 * (len(scores) - 1)
    return s, hit


def tier(r, icon_query):
    """Availability tier: directly obtainable code first, inspiration and gated items later."""
    if r['source'] == 'lucide' and not icon_query:
        return 0.5
    if r['access'] == 'free':
        if r['category'].startswith('example'):  # demo variants of a component rank below the components themselves
            return 3
        return {'install': 4, 'source': 4, 'prompt': 3, 'reference': 1}.get(r['usage'], 1)
    return {'login': 2, 'pro': 0.2, 'broken': 0}.get(r['access'], 0)


def label(r):
    base = USAGE_ZH.get(r['usage'], r['usage'])
    return {'free': base, 'login': '需登录·' + base, 'pro': 'Pro·不获取', 'broken': '失效'}.get(r['access'], base)


FIND_MODES = {
    'default': ('免费 + 需登录（标注），排除 Pro 和失效', lambda r: r['access'] in ('free', 'login')),
    'code': ('只要现在就能直接拿到代码或提示词的（免费，且非仅参考）',
             lambda r: r['access'] == 'free' and r['usage'] != 'reference'),
    'free': ('只要免费的（含仅参考）', lambda r: r['access'] == 'free'),
    'ref': ('只要灵感参考', lambda r: r['access'] == 'free' and r['usage'] == 'reference'),
    'all': ('全部，含 Pro 和失效', lambda r: True),
}


def search(terms, src=None, mode='default', task=None, layer=None):
    """Rank catalogue rows for a query. Returns ([(score, row)], note)."""
    rows = [r for r in load_rows(src) if FIND_MODES[mode][1](r)
            and (not task or task in r['task'].split(',')) and (not layer or r['layer'] == layer)]
    groups = load_groups()
    corpus = [' '.join((r['id'], r['name'], r['category'], r['task'], r['desc'], r['vtags'], r['itags'])).lower()
              for r in rows]
    cons = [(o, [term_re(a) for a in alts]) for t in terms for o, alts in concepts(t, groups, corpus)]
    icon_query = any(o in ICON_TERMS or ICON_TERMS & {a.pattern for a in alts} for o, alts in cons) or any(
        t.lower() in ICON_TERMS for t in terms)
    scored = []
    for r in rows:
        rel, hit = relevance(r, cons) if cons else (0.0, 0)
        if cons and not hit:
            continue
        # Strong = matched concepts average a name/category-level hit; weak = description-level only.
        band = 1 if not cons or rel >= 2.5 * hit else 0
        scored.append((hit, band, tier(r, icon_query), rel, r))
    note = ''
    if cons and scored:
        top = max(x[0] for x in scored)
        if top < len(cons):
            note = '（没有条目同时命中全部 %d 个词，以下是命中 %d 个的结果）' % (len(cons), top)
        scored = [x for x in scored if x[0] == top]
    ranked = sorted(scored, key=lambda x: (-x[0], -x[1], -x[2], -x[3]))
    if cons and ranked and (ranked[0][1] == 0 or ranked[0][0] < len(cons)):
        note += ('\n低置信度：没有名称或分类级的强相关候选（只有描述沾边或只命中部分词）。'
                 '先换词或用 --task 再搜；仍然没有合适的，就说明"收藏库无合适候选"并自己实现。')
    return [(x[3], x[4]) for x in ranked], note


def cmd_find(args):
    src, limit, mode, terms, task, layer = None, 25, 'default', [], None, None
    it = iter(args)
    for a in it:
        if a == '-s':
            src = next(it)
        elif a == '--task':
            task = next(it)
        elif a == '--layer':
            layer = next(it)
        elif a == '--limit':
            limit = int(next(it))
        elif a in ('-h', '--help'):
            print('usage: find.sh [-s source] [--task T] [--layer L] [--limit N] [--code|--free|--ref|--all] [keyword...]')
            print('  --task   UI 任务：' + ' '.join(TASKS))
            print('  --layer  层级：' + ' '.join(LAYERS))
            for k, (d, _) in FIND_MODES.items():
                print('  %-9s %s' % ('(默认)' if k == 'default' else '--' + k, d))
            return 0
        elif a.startswith('--') and a[2:] in FIND_MODES:
            mode = a[2:]
        else:
            terms.append(a)
    if task and task not in TASKS:
        sys.exit('unknown task %r. choose from: %s' % (task, ' '.join(TASKS)))
    if layer and layer not in LAYERS:
        sys.exit('unknown layer %r. choose from: %s' % (layer, ' '.join(LAYERS)))
    scored, note = search(terms, src, mode, task, layer)
    if not scored:
        print('no match：收藏库里没有相关条目。换更短的词、英文词或 --task 再搜；仍然没有，就说明"收藏库无合适候选"并自己实现。')
        return 1
    by_src = {}
    for _, r in scored:
        by_src[r['source']] = by_src.get(r['source'], 0) + 1
    print('%d matches (%s)  filter=%s %s' % (len(scored), ', '.join('%s %d' % kv for kv in sorted(by_src.items(), key=lambda x: -x[1])), mode, note))
    for s, r in scored[:limit]:
        tag = label(r)
        print('[%s] %s:%s — %s  (%s · %s)%s' % (tag, r['source'], r['id'], r['name'], r['task'], r['layer'],
                                               '  ⚠ ' + r['risk'] if r['risk'] else ''))
        print('    %s' % r['desc'][:160])
    if len(scored) > limit:
        print('... %d more (--limit N)' % (len(scored) - limit))
    if any(r['risk'] for _, r in scored[:limit]):
        print('\n⚠ = 场景化审美风险（不禁止，用的话要在选型理由里说明适用场景，见 SKILL.md「质量分级」）')
    print('下一步: fetch.sh <source:id>   （仅参考类条目会给出打开方式）')
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
    opts['_final_url'] = url
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


def adapter_path(name):
    for ext, runner in (('.py', sys.executable), ('.sh', 'sh')):
        p = os.path.join(ADAPTERS, name + ext)
        if os.path.exists(p):
            return p, runner
    return None, None


def do_script(arg, out, opts):
    name, _, a = arg.partition(' ')
    path, runner = adapter_path(name)
    if not path:
        return False, 'missing adapter %s' % name
    cmd = [runner, path, a] + ([str(opts['limit'])] if opts.get('limit') else [])
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
        elif a in ('-h', '--help'):
            print(FETCH_HELP)
            return 0
        else:
            refs.append(a)
    if not refs:
        print(FETCH_HELP)
        return 2
    rc = 0
    for ref in refs:
        rc |= fetch_one(find_row(ref), opts)
    return rc


FETCH_HELP = """usage: fetch.sh <source:item_id> [...] [options]     （只读：下载到临时目录，不安装、不执行）

options:
  --out DIR          输出目录（默认 $TMPDIR/ui-arsenal/<source>/<id>/）
  --variant V        React Bits 变体：TS-TW（默认）| TS-CSS | JS-TW | JS-CSS
  --style S          shadcn style，要和项目 components.json 一致：
                     {base,radix,aria}-{vega,nova,maia,lyra,mira,luma,rhea,sera}，图表/主题只有 new-york-v4
  --limit N          列表类 adapter 的条数（collectui）

不同条目的输出：
  可安装 / 取源码   源码文件 + 依赖 + 安装命令（安装会改动项目，先确认项目栈）
  提示词            prompt.md / DESIGN.md，按内容实现
  仅参考            下载图片或视频；只能浏览器看的给出 URL
  需登录            不获取，输出登录方式和页面地址，由用户决定（退出码 4）
  Pro / 失效        不获取（退出码 3 / 2）

例子:
  fetch.sh shadcn:button --style radix-nova
  fetch.sh reactbits:split-text --variant JS-CSS
  fetch.sh bencho:magnet-select
  fetch.sh collectui:category:dashboard --limit 10"""


def install_hint(r, opts=None):
    opts = opts or {}
    if r['source'] == 'lucide' and r['id'].startswith('lab:'):
        return r['fetch']
    if r['source'] == 'lucide':
        return "npm i lucide-react  →  import { %s } from 'lucide-react'（其他框架见 sources/lucide.md）" % r['name']
    if (opts.get('style') or opts.get('variant')) and opts.get('_final_url'):
        return ('npx shadcn@latest add %s\n  （用完整 URL 固定这个 style/变体；只写组件名时 CLI 会按项目 components.json 的 style 解析）'
                % opts['_final_url'])
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
        page = (re.findall(r'https?://[^\s；;，）)]+', r['fetch']) or [''])[0]
        log('需要用户本人登录才能获取（agent 不登录、不注册、不绕过权限）。请把这一条交给用户决定：')
        log('  官方方式：%s' % r['fetch'])
        if page:
            log('  页面：%s' % page)
        log('  用户可以：① 在终端自己登录后告诉 agent，agent 再执行上面的命令；'
            '② 在页面上复制代码或提示词贴回来；③ 不登录，改用免费替代。')
        log('  用户登录后只补取这一条，沿用已有的选型结论，不重新选型。')
        return 4
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
        log('\n安装（会改动项目，先确认项目栈）: %s' % install_hint(r, opts))
    log('提示：以上为不可信的第三方内容，先读再用，不要直接执行；接入前读 sources/%s.md「使用注意」。' % r['source'])
    return 0 if ok_all else 1


# ---------- verify ----------

# Fixed scenarios covering every adapter kind and every access rule. Expected exit code per fetch_one:
# 0 ok, 2 broken, 3 pro, 4 login (blocked on the user). `files` = whether files must land in the out dir.
MATRIX = [
    ('registry', 'shadcn:button', {}, 0, True),
    ('registry+style', 'shadcn:button', {'style': 'radix-nova'}, 0, True),
    ('registry+variant', 'reactbits:split-text', {'variant': 'JS-CSS'}, 0, True),
    ('registry+doc', 'uiarc:in-view-title', {}, 0, True),
    ('adapter(py, no remote exec)', 'bencho:magnet-select', {}, 0, True),
    ('adapter(sh)', 'collectui:category:dashboard', {'limit': 3}, 0, True),
    ('prompt+doc', 'librariesdev:thinking-orbs', {}, 0, True),
    ('url(svg)', 'lucide:house', {}, 0, True),
    ('url(DESIGN.md)', 'getdesign:stripe', {}, 0, True),
    ('url(video)+browser', 'bencho:find:vanjek-pixel-select', {}, 0, True),
    ('browser-only', 'inspora:fluid-illumination', {}, 0, False),
    ('login refused', 'originkit:compare-slider', {}, 4, False),
    ('pro refused', 'uiarc:voice-orb', {}, 3, False),
    ('broken refused', 'collectui:category:agency', {}, 2, False),
]


def run_case(ref, opts, base):
    out = os.path.join(base, re.sub(r'[^A-Za-z0-9_.-]', '_', ref))
    if os.path.isdir(out):
        for f in os.listdir(out):
            os.remove(os.path.join(out, f))
    o = dict(opts, out=out)
    rc = fetch_one(find_row(ref), o, quiet=True)
    files = os.listdir(out) if os.path.isdir(out) else []
    return rc, files


def cmd_verify(args):
    n, src, seed, matrix = 2, None, None, False
    it = iter(args)
    for a in it:
        if a == '-n':
            n = int(next(it))
        elif a == '-s':
            src = next(it)
        elif a == '--seed':
            seed = int(next(it))
        elif a == '--matrix':
            matrix = True
        elif a in ('-h', '--help'):
            print('usage: verify.sh [--matrix] [-s source] [-n 2] [--seed N]\n'
                  '  --matrix  固定场景：每种获取方式 + login/pro/broken 拒绝逻辑\n'
                  '  默认      每个来源随机抽 n 条免费、可机器获取的条目实取一次\n'
                  '说明：verify 通过只代表"现在能取到"（验证层级③），不代表组件成熟或适合项目。')
            return 0
    base = os.path.join(os.environ.get('TMPDIR', '/tmp'), 'ui-arsenal-verify')
    state, now, fails = load_state(), time.strftime('%Y-%m-%d %H:%M'), 0
    vs = state.setdefault('verify', {})
    if matrix:
        rows = []
        for name, ref, opts, want_rc, want_files in MATRIX:
            try:
                rc, files = run_case(ref, opts, os.path.join(base, 'matrix'))
                ok = rc == want_rc and bool(files) == want_files
                detail = 'rc=%s files=%d' % (rc, len(files))
            except SystemExit as e:
                ok, detail = False, 'row missing: %s' % e
            fails += not ok
            rows.append((name, ref, ok, detail))
            print('%-4s %-28s %-40s %s' % ('ok' if ok else 'FAIL', name, ref[:40], detail))
        vs['_matrix'] = {'at': now, 'fails': fails, 'results': [list(r) for r in rows]}
    else:
        rnd = random.Random(seed)
        for s in ([src] if src else sources()):
            rows = [r for r in load_rows(s) if r['access'] == 'free' and any(
                k in ('registry', 'url', 'doc', 'prompt', 'script') for k, _ in parse_spec(r['spec']))]
            if not rows:
                print('skip %-13s no machine-fetchable free rows' % s)
                vs[s] = {'at': now, 'skipped': True}
                continue
            res = []
            for r in rnd.sample(rows, min(n, len(rows))):
                rc, files = run_case('%s:%s' % (s, r['id']), {'limit': 3}, os.path.join(base, s))
                ok = rc == 0 and bool(files)
                fails += not ok
                res.append([r['id'], ok, 'rc=%s files=%d' % (rc, len(files))])
                print('%-4s %-13s %-40s %s' % ('ok' if ok else 'FAIL', s, r['id'][:40], res[-1][2]))
            vs[s] = {'at': now, 'fails': sum(not x[1] for x in res), 'results': res}
    save_state(state)
    print('\n%d failed. 结果按来源保存在 sources/_state.json 的 verify 下（不覆盖其他来源的记录）。' % fails)
    return 1 if fails else 0


# ---------- refresh / diff / apply ----------
#
# refresh  pulls each source's public index and writes a proposal to sources/_pending/<date>/<source>.json.
#          It never touches the catalogue.
# diff     prints the latest proposals.
# apply    writes approved machine fields into sources/<id>.tsv (and notes rows for new items that already
#          have a Chinese description in the proposal). Run audit afterwards and commit with git; git revert
#          is the rollback.

PENDING = os.path.join(SRC, '_pending')
REMOVE_AFTER_DAYS = 30  # an item missing in two refreshes at least this far apart is proposed as removed


def load_state():
    return json.load(open(STATE, encoding='utf-8')) if os.path.exists(STATE) else {}


def save_state(s):
    with open(STATE, 'w', encoding='utf-8') as f:
        json.dump(s, f, ensure_ascii=False, indent=1)


def fp(meta):
    """Short fingerprint of the metadata an index exposes (deps, files, type, tier, tags...)."""
    return hashlib.sha1(json.dumps(meta, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:10] if meta else ''


def get_json(url):
    st, ct, body = http(url, tries=3)
    if st != 200:
        raise RuntimeError('HTTP %s %s' % (st, url))
    return json.loads(body), body


def reg_meta(item):
    return {'type': item.get('type', ''), 'deps': sorted(item.get('dependencies') or []),
            'rdeps': sorted(item.get('registryDependencies') or []),
            'files': sorted(f.get('path', '') for f in item.get('files') or [])}


def spec_key(r, strip=None, must=None):
    for k, a in parse_spec(r['spec']):
        if k == 'registry' and (not must or must in a):
            n = os.path.basename(a)
            n = n[:-5] if n.endswith('.json') else n
            return re.sub(strip, '', n) if strip else n
    return None


def kebab(name):
    return re.sub(r'(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', '-', name).lower()


# Each refresher returns (remote: {key: meta}, key_of(row) -> key|None, index_sha, new_row(key, meta) -> dict).
def r_shadcn():
    remote, h = {}, []
    for st in ('base-nova', 'radix-nova', 'aria-nova', 'new-york-v4'):
        d, body = get_json('https://ui.shadcn.com/r/styles/%s/registry.json' % st)
        h.append(sha(body))
        for it in d['items']:
            if it['name'] in ('index', 'style'):
                continue
            m = remote.setdefault(it['name'], {'styles': [], **reg_meta(it)})
            m['styles'].append(st)
    new = lambda k, m: {'spec': 'registry:https://ui.shadcn.com/r/styles/%s/%s.json' % (
        'base-nova' if 'base-nova' in m['styles'] else m['styles'][0], k),
        'fetch': 'npx shadcn@latest add %s' % k, 'url': 'https://ui.shadcn.com/docs/components/' + k,
        'framework': 'react', 'category': m['type']}
    return remote, lambda r: spec_key(r, must='/styles/'), sha(''.join(h).encode()), new


def r_registry(base, add_cmd=None, strip=None, ignore=(), url_tpl=None):
    def f():
        d, body = get_json(base + '/r/registry.json')
        remote = {}
        for it in d['items']:
            if it['name'] in ignore:
                continue
            k = re.sub(strip, '', it['name']) if strip else it['name']
            if strip and not it['name'].endswith('-TS-TW'):
                remote.setdefault(k, {})
                continue
            remote[k] = reg_meta(it)
        def new(k, m):
            name = k + ('-TS-TW' if strip else '')
            return {'spec': 'registry:%s/r/%s.json' % (base, name),
                    'fetch': (add_cmd % name) if add_cmd else 'npx shadcn@latest add %s/r/%s.json' % (base, name),
                    'url': (url_tpl % k) if url_tpl else base, 'framework': 'react', 'category': m.get('type', '')}
        return remote, lambda r: spec_key(r, strip), sha(body), new
    return f


def r_uiarc():
    d, body = get_json('https://uiarc.dev/r/catalog.json')
    items = next(v for v in d.values() if isinstance(v, list))
    remote = {it['name']: {'tier': it.get('tier', ''), 'category': it.get('category', ''),
                           'deps': sorted(it.get('dependencies') or [])} for it in items}
    def new(k, m):
        pro = m['tier'] != 'free'
        return {'spec': 'none' if pro else 'registry:https://uiarc.dev/r/%s.json' % k,
                'fetch': 'https://uiarc.dev/components/%s/markdown' % k if pro else 'npx shadcn@latest add https://uiarc.dev/r/%s.json' % k,
                'url': 'https://uiarc.dev/components/' + k, 'framework': 'react', 'category': m['category'],
                'access': 'pro' if pro else 'free'}
    # foundation, agent skill and templates are not part of the component catalog
    key = lambda r: None if r['category'] in ('Templates', 'Skill', 'Foundation') else r['id']
    return remote, key, sha(body), new


def r_lucide():
    st, ct, body = http('https://unpkg.com/lucide-static@latest/tags.json', tries=3)
    if st != 200:
        raise RuntimeError('HTTP %s' % st)
    remote = {k: {'tags': sorted(v)} for k, v in json.loads(body).items()}
    st2, _, meta = http('https://unpkg.com/@lucide/lab@latest/?meta', tries=3)
    if st2 == 200:
        def walk(n):
            for f in n.get('files', []):
                yield from (walk(f) if f.get('type') == 'directory' else [f['path']])
        for f in walk(json.loads(meta)):
            if f.startswith('/dist/esm/icons/') and f.endswith('.js'):
                remote['lab:' + os.path.basename(f)[:-3]] = {}
    def new(k, m):
        lab = k.startswith('lab:')
        n = k[4:] if lab else k
        return {'spec': ('url:https://unpkg.com/@lucide/lab@latest/dist/esm/icons/%s.js' if lab else
                         'url:https://unpkg.com/lucide-static@latest/icons/%s.svg') % n,
                'fetch': 'npm i @lucide/lab' if lab else 'https://unpkg.com/lucide-static@latest/icons/%s.svg' % n,
                'url': 'https://lucide.dev/icons/' + (('lab/' + n) if lab else n), 'framework': 'multi',
                'category': 'lab' if lab else 'icon'}
    return remote, lambda r: r['id'] if r['access'] == 'free' else None, sha(body + meta), new


def r_originkit():
    d, body = get_json('https://mcp.originkit.dev/v1/registry')
    remote = {c['name']: {'category': c.get('category', ''), 'kind': c.get('kind', ''),
                          'deps': sorted(c.get('dependencies') or []),
                          'rdeps': sorted(c.get('registryDependencies') or [])} for c in d['components']}
    new = lambda k, m: {'spec': 'manual', 'fetch': 'npx originkit add %s（需 originkit login）；页面 https://www.originkit.dev/components/%s' % (k, k),
                        'url': 'https://www.originkit.dev/components/' + k, 'framework': 'react',
                        'category': m['category'], 'access': 'login'}
    return remote, lambda r: r['id'] if r['category'] != 'template' else None, sha(body), new


def r_bencho():
    st, ct, body = http('https://bencho.dev/llms.txt', tries=3)
    if st != 200:
        raise RuntimeError('HTTP %s' % st)
    remote = {k: {} for k in re.findall(r'bencho\.dev/blocks/([a-z0-9-]+)', body.decode())}
    st2, _, sm = http('https://bencho.dev/sitemap.xml', tries=3)
    if st2 == 200:
        remote.update({'find:' + x: {} for x in re.findall(r'bencho\.dev/finds/([A-Za-z0-9_-]+)<', sm.decode())})
        body += sm
    parked = {r['id'] for r in load_rows('bencho') if '未在站点上架' in r['desc'] or 'parked' in r['desc']}
    def new(k, m):
        if k.startswith('find:'):
            return {'spec': 'browser:https://bencho.dev/finds/' + k[5:], 'fetch': 'https://bencho.dev/finds/' + k[5:],
                    'url': 'https://bencho.dev/finds/' + k[5:], 'usage': 'reference', 'category': 'finds'}
        return {'spec': 'script:bencho ' + k, 'fetch': 'scripts/fetch.sh bencho:' + k,
                'url': 'https://bencho.dev/blocks/' + k, 'framework': 'react', 'usage': 'source'}
    key = lambda r: None if r['id'] in parked or r['id'].startswith('category:') else r['id']
    return remote, key, sha(body), new


def r_getdesign():
    st, ct, body = http('https://getdesign.md/sitemap.xml', tries=3)
    if st != 200:
        raise RuntimeError('HTTP %s' % st)
    txt = body.decode()
    remote = {x: {} for x in re.findall(r'https://getdesign\.md/([^/<]+)/design-md<', txt)}
    remote.update({'site:' + x: {} for x in re.findall(r'https://getdesign\.md/design-md/([^/<]+)<', txt)})
    def new(k, m):
        if k.startswith('site:'):
            n = k[5:]
            return {'spec': 'browser:https://getdesign.md/design-md/' + n, 'fetch': 'https://getdesign.md/design-md/' + n,
                    'url': 'https://getdesign.md/design-md/' + n, 'usage': 'reference', 'category': 'catalog'}
        return {'spec': 'url:https://getdesign.md/design-md/%s/DESIGN.md' % k,
                'fetch': 'curl -s https://getdesign.md/design-md/%s/DESIGN.md -o DESIGN.md' % k,
                'url': 'https://getdesign.md/%s/design-md' % k, 'usage': 'prompt', 'category': 'design-md'}
    key = lambda r: r['id'] if r['usage'] == 'prompt' or r['id'].startswith('site:') else None
    return remote, key, sha(body), new


REFRESH = {
    'shadcn': r_shadcn,
    'reactbits': r_registry('https://reactbits.dev', 'npx shadcn@latest add @react-bits/%s', strip=r'-(JS|TS)-(CSS|TW)$'),
    'uiarc': r_uiarc,
    'obsidianui': r_registry('https://www.obsidianui.dev', url_tpl='https://www.obsidianui.dev/docs/%s'),
    'beautifului': r_registry('https://www.beautifului.dev', url_tpl='https://www.beautifului.dev/#%s'),
    'loadingui': r_registry('https://loading-ui.com', 'npx shadcn@latest add @loading-ui/%s',
                            ignore=('index', 'style', 'utils'), url_tpl='https://loading-ui.com/docs/components/%s'),
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


def days_between(a, b):
    try:
        return abs((time.mktime(time.strptime(a, '%Y-%m-%d')) - time.mktime(time.strptime(b, '%Y-%m-%d'))) / 86400)
    except ValueError:
        return 0


def cmd_refresh(args):
    if '-h' in args or '--help' in args:
        print('usage: refresh.sh [source...]   拉取线上清单，生成 sources/_pending/<日期>/<source>.json 待审变更，不改正式数据')
        return 0
    targets = [a for a in args if not a.startswith('-')] or sources()
    today = time.strftime('%Y-%m-%d')
    outdir = os.path.join(PENDING, today)
    os.makedirs(outdir, exist_ok=True)
    rc = 0
    for s in targets:
        if s not in REFRESH:
            print('%-13s skip   %s' % (s, NO_REFRESH.get(s, 'no refresh adapter')))
            continue
        prop = {'source': s, 'generated_at': time.strftime('%Y-%m-%d %H:%M'), 'status': 'ok'}
        try:
            remote, key_of, h, new_row = REFRESH[s]()
            if not remote:
                raise RuntimeError('index returned 0 items (parser broken or site changed)')
        except Exception as e:
            prop.update(status='error', error=str(e)[:300])
            json.dump(prop, open(os.path.join(outdir, s + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            print('%-13s ERROR  %s  → 不产生任何条目变更（不会当作全部下线）' % (s, prop['error']))
            rc = 1
            continue
        local = {}
        for r in load_rows(s, include_removed=True):
            k = key_of(r)
            if k:
                local[k] = r
        seen, init, changed, missing, added = [], [], [], [], []
        for k, r in local.items():
            if k in remote:
                seen.append(r['id'])
                newfp, m = fp(remote[k]), remote[k]
                deps = ' '.join(m.get('deps', []))
                acc = {'pro': 'pro', 'free': 'free'}.get(m.get('tier', ''), None)
                if not r['fingerprint']:
                    init.append({'id': r['id'], 'fingerprint': newfp, 'deps': deps})
                elif r['fingerprint'] != newfp or (acc and acc != r['access']):
                    changed.append({'id': r['id'], 'fingerprint': [r['fingerprint'], newfp], 'deps': [r['deps'], deps],
                                    'access': [r['access'], acc or r['access']]})
            elif r['status'] != 'removed':
                stale = r['status'] == 'needs-review' and days_between(r['last_seen'], today) >= REMOVE_AFTER_DAYS
                missing.append({'id': r['id'], 'status': r['status'], 'last_seen': r['last_seen'],
                                'proposal': 'removed' if stale else 'needs-review'})
        for k in sorted(set(remote) - set(local)):
            row = new_row(k, remote[k])
            added.append(dict(row, key=k, id=kebab(k) if s == 'reactbits' else k, title=k,
                              fingerprint=fp(remote[k]), deps=' '.join(remote[k].get('deps', [])),
                              desc_zh='', task='', layer=''))
        prev = load_state().get('refresh', {}).get(s, {})
        prop.update(index_sha=h, index_changed=bool(prev.get('index_sha')) and prev.get('index_sha') != h,
                    remote=len(remote), local=len(local), seen=seen, init=init, changed=changed,
                    missing=missing, added=added)
        json.dump(prop, open(os.path.join(outdir, s + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        st = load_state()
        st.setdefault('refresh', {})[s] = {'at': prop['generated_at'], 'index_sha': h}
        save_state(st)
        print('%-13s remote %4d  local %4d  init %4d  changed %3d  missing %3d  new %3d' % (
            s, len(remote), len(local), len(init), len(changed), len(missing), len(added)))
    print('\n待审变更已写入 %s/（不改正式数据）。看详情：diff.sh；批准后：apply.sh <source>，再 audit.sh 并 git commit。' % outdir)
    return rc


def latest_pending(s):
    if not os.path.isdir(PENDING):
        return None
    for d in sorted(os.listdir(PENDING), reverse=True):
        p = os.path.join(PENDING, d, s + '.json')
        if os.path.exists(p):
            return p
    return None


def cmd_diff(args):
    targets = [a for a in args if not a.startswith('-')] or sources()
    for s in targets:
        p = latest_pending(s)
        if not p:
            continue
        d = json.load(open(p, encoding='utf-8'))
        if d['status'] != 'ok':
            print('## %s  ERROR %s' % (s, d.get('error')))
            continue
        print('## %s  (%s)  init %d  changed %d  missing %d  new %d' % (
            s, d['generated_at'], len(d['init']), len(d['changed']), len(d['missing']), len(d['added'])))
        for c in d['changed'][:20]:
            print('  changed  %-36s deps %r → %r  access %s → %s' % (c['id'], c['deps'][0], c['deps'][1], *c['access']))
        for m in d['missing'][:20]:
            print('  missing  %-36s %s → %s (last seen %s)' % (m['id'], m['status'], m['proposal'], m['last_seen']))
        for a in d['added'][:20]:
            print('  new      %-36s %s%s' % (a['id'], a.get('category', ''), '' if a['desc_zh'] else '  （待补 desc_zh/task/layer 才能写入）'))
        more = sum(max(0, len(d[k]) - 20) for k in ('changed', 'missing', 'added'))
        if more:
            print('  ... %d more, see %s' % (more, p))
    return 0


def cmd_apply(args):
    if not args or args[0] in ('-h', '--help'):
        print('usage: apply.sh <source> [--file pending.json]   把已审的待审变更写入 sources/<source>.tsv（只写机器字段）')
        return 0
    s = args[0]
    p = args[args.index('--file') + 1] if '--file' in args else latest_pending(s)
    if not p:
        sys.exit('no pending proposal for %s; run refresh.sh %s first' % (s, s))
    d = json.load(open(p, encoding='utf-8'))
    if d['status'] != 'ok':
        sys.exit('proposal is an error report, nothing to apply: %s' % d.get('error'))
    today = d['generated_at'][:10]
    mp, np_ = os.path.join(SRC, s + '.tsv'), os.path.join(SRC, s + '.notes.tsv')
    rows = [dict(zip(COLS, l.rstrip('\n').split('\t'))) for l in open(mp, encoding='utf-8') if l.strip()]
    by_id = {r['id']: r for r in rows}
    n = {'seen': 0, 'init': 0, 'changed': 0, 'missing': 0, 'added': 0, 'skipped_new': 0}
    for i in d['seen']:
        r = by_id.get(i)
        if r:
            r['last_seen'] = today
            if r['status'] == 'needs-review' and not any(c['id'] == i for c in d['changed']):
                r['status'] = 'active'
            n['seen'] += 1
    for c in d['init']:
        if c['id'] in by_id:
            by_id[c['id']]['fingerprint'] = c['fingerprint']
            if c['deps']:
                by_id[c['id']]['deps'] = c['deps']
            n['init'] += 1
    for c in d['changed']:
        r = by_id.get(c['id'])
        if r:
            r['fingerprint'], r['deps'], r['access'] = c['fingerprint'][1], c['deps'][1] or r['deps'], c['access'][1]
            if r['access'] == 'pro':
                r['spec'] = 'none'
            r['status'] = 'needs-review'
            n['changed'] += 1
    for m in d['missing']:
        r = by_id.get(m['id'])
        if r:
            r['status'] = m['proposal']
            n['missing'] += 1
    new_notes = []
    for a in d['added']:
        if not (a.get('desc_zh') and a.get('task') and a.get('layer')):
            n['skipped_new'] += 1
            continue
        if a['id'] in by_id:
            continue
        row = {k: '' for k in COLS}
        row.update(source=s, id=a['id'], name=a['title'], category=a.get('category', ''), url=a.get('url', ''),
                   fetch=a.get('fetch', ''), spec=a.get('spec', 'manual'), access=a.get('access', 'free'),
                   usage=a.get('usage', 'install'), framework=a.get('framework', ''), deps=a.get('deps', ''),
                   status='needs-review', last_seen=today, fingerprint=a.get('fingerprint', ''))
        rows.append(row)
        by_id[row['id']] = row
        new_notes.append('\t'.join([a['id'], a['desc_zh'], a['task'], a['layer'], a.get('visual_tags', ''),
                                    a.get('interaction_tags', ''), a.get('risk', ''), '']))
        n['added'] += 1
    with open(mp, 'w', encoding='utf-8') as f:
        f.write('\n'.join('\t'.join(r.get(k, '') for k in COLS) for r in rows) + '\n')
    if new_notes:
        with open(np_, 'a', encoding='utf-8') as f:
            f.write('\n'.join(new_notes) + '\n')
    print('applied %s: %s' % (os.path.relpath(p, ROOT), ', '.join('%s %d' % kv for kv in n.items())))
    if n['skipped_new']:
        print('有 %d 个新条目缺 desc_zh/task/layer，没有写入：在 %s 里补全后再 apply。' % (n['skipped_new'], p))
    print('下一步：audit.sh，确认无误后 git commit（回滚用 git revert）。')
    return 0


# ---------- stats / audit ----------

def cmd_stats(args):
    md = '--md' in args or '--write-skill' in args
    buf = []
    out = buf.append if '--write-skill' in args else print
    rows_all = load_rows()
    # Buckets are mutually exclusive, so the numbers mean "what an agent can actually do with it".
    buckets = (('free-install', lambda r: r['access'] == 'free' and r['usage'] == 'install'),
               ('free-source', lambda r: r['access'] == 'free' and r['usage'] == 'source'),
               ('free-prompt', lambda r: r['access'] == 'free' and r['usage'] == 'prompt'),
               ('reference', lambda r: r['access'] == 'free' and r['usage'] == 'reference'),
               ('login', lambda r: r['access'] == 'login'),
               ('pro', lambda r: r['access'] == 'pro'),
               ('broken', lambda r: r['access'] == 'broken'))
    hdr = ('source', 'items', 'categories') + tuple(b for b, _ in buckets)
    table = []
    for s in sources():
        rs = [r for r in rows_all if r['source'] == s]
        cat = sum(r['id'].startswith('category:') for r in rs)
        table.append((s, len(rs) - cat, cat) + tuple(sum(f(r) for r in rs) for _, f in buckets))
    if md:
        out('| 来源 | 名称 | 类型 | 条目 | 分类行 | 免费可装 | 免费取源码 | 免费提示词 | 仅参考 | 需登录 | Pro | 失效 |')
        out('|---|---|---|---|---|---|---|---|---|---|---|---|')
        for t in table:
            fm = frontmatter(t[0])
            out('| %s | [%s](%s) | %s | %s |' % (t[0], fm.get('name', t[0]), fm.get('url', ''), fm.get('kind', ''),
                                              ' | '.join(str(v) if v else '' for v in t[1:])))
        tot = tuple(sum(t[i] for t in table) for i in range(1, len(hdr)))
        out('| **合计** | | | %s |' % ' | '.join('**%d**' % v for v in tot))
    else:
        out(('%-13s' + ' %12s' * (len(hdr) - 1)) % hdr)
        for t in table:
            out(('%-13s' + ' %12d' * (len(hdr) - 1)) % t)
        tot = tuple(sum(t[i] for t in table) for i in range(1, len(hdr)))
        out(('%-13s' + ' %12d' * (len(hdr) - 1)) % (('TOTAL',) + tot))
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
        for ext in ('.tsv', '.notes.tsv'):
            if not os.path.exists(os.path.join(SRC, s + ext)):
                errs.append('%s: missing %s' % (s, ext))
    total = 0
    for s in sources():
        mp, np_ = os.path.join(SRC, s + '.tsv'), os.path.join(SRC, s + '.notes.tsv')
        if not (os.path.exists(mp) and os.path.exists(np_)):
            continue
        ids = {}
        for n, line in enumerate(open(mp, encoding='utf-8'), 1):
            if not line.strip():
                continue
            c = line.rstrip('\n').split('\t')
            where = '%s.tsv:%d' % (s, n)
            if len(c) != len(COLS):
                errs.append('%s: %d columns (need %d)' % (where, len(c), len(COLS)))
                continue
            r = dict(zip(COLS, c))
            total += 1
            if r['source'] != s:
                errs.append('%s: source column %r != %r' % (where, r['source'], s))
            if r['id'] in ids:
                errs.append('%s: duplicate id %s (also line %d)' % (where, r['id'], ids[r['id']]))
            ids[r['id']] = n
            if r['access'] not in ACCESS:
                errs.append('%s: access %r' % (where, r['access']))
            if r['usage'] not in USAGE:
                errs.append('%s: usage %r' % (where, r['usage']))
            if r['status'] not in STATUS:
                errs.append('%s: item_status %r' % (where, r['status']))
            if r['url'] and not r['url'].startswith('http'):
                errs.append('%s: official_url %r' % (where, r['url']))
            for k, a in parse_spec(r['spec']):
                if k not in ADAPTER_KINDS:
                    errs.append('%s: spec adapter %r' % (where, k))
                elif k in ('registry', 'url', 'doc', 'prompt', 'browser') and not a.startswith('https://'):
                    errs.append('%s: spec %s needs https url' % (where, k))
                elif k == 'script' and not adapter_path(a.split()[0])[0]:
                    errs.append('%s: missing adapter %s' % (where, a))
            if r['access'] == 'pro' and r['spec'] != 'none':
                errs.append('%s: pro row must have spec none' % where)
        for n, line in enumerate(open(mp, encoding='utf-8'), 1):
            c = line.rstrip('\n').split('\t')
            if len(c) == len(COLS) and c[12] and c[12] not in ids:
                errs.append('%s.tsv:%d: alias_of %r does not exist' % (s, n, c[12]))
        seen_notes = set()
        for n, line in enumerate(open(np_, encoding='utf-8'), 1):
            if not line.strip():
                continue
            c = line.rstrip('\n').split('\t')
            where = '%s.notes.tsv:%d' % (s, n)
            if len(c) != len(NOTE_COLS):
                errs.append('%s: %d columns (need %d)' % (where, len(c), len(NOTE_COLS)))
                continue
            r = dict(zip(NOTE_COLS, c))
            if r['id'] not in ids:
                errs.append('%s: note for unknown id %s' % (where, r['id']))
            if r['id'] in seen_notes:
                errs.append('%s: duplicate note id %s' % (where, r['id']))
            seen_notes.add(r['id'])
            if not r['desc']:
                errs.append('%s: empty desc_zh' % where)
            for t in filter(None, r['task'].split(',')):
                if t not in TASKS:
                    errs.append('%s: task %r' % (where, t))
            if r['layer'] not in LAYERS:
                errs.append('%s: layer %r' % (where, r['layer']))
            for t in filter(None, r['risk'].split(',')):
                if t not in RISKS:
                    errs.append('%s: risk %r' % (where, t))
        for missing in sorted(set(ids) - seen_notes)[:5]:
            errs.append('%s: id %s has no notes row' % (s, missing))
    for e in errs[:200]:
        print(e)
    print('%d rows checked, %d problems' % (total, len(errs)))
    return 1 if errs else 0


def cmd_searchtest(args):
    """Run search relevance regression cases from scripts/search_cases.json."""
    cases = json.load(open(os.path.join(ROOT, 'scripts', 'search_cases.json'), encoding='utf-8'))['cases']
    fails = 0
    for c in cases:
        res, _ = search(c['q'], c.get('src'), c.get('mode', 'default'))
        ids = ['%s:%s' % (r['source'], r['id']) for _, r in res]
        k = c.get('k', 1)
        top = [r for _, r in res[:k]]
        if c.get('empty'):
            ok = not res
        elif 'top1' in c:
            ok = bool(ids) and ids[0] == c['top1']
        elif 'topk_any' in c:
            ok = any(i in ids[:k] for i in c['topk_any'])
        elif 'topk_all_category' in c:
            ok = bool(top) and all(re.search(c['topk_all_category'], r['category']) for r in top)
        elif 'topk_all_id' in c:
            ok = bool(top) and all(re.search(c['topk_all_id'], r['id'] + ' ' + r['name'], re.I) for r in top)
        elif 'topk_all_task_primary' in c:
            ok = bool(top) and all(r['task'].split(',')[0] == c['topk_all_task_primary'] for r in top)
        elif 'topk_no_usage' in c:
            ok = bool(top) and all(r['usage'] != c['topk_no_usage'] for r in top)
        else:
            ok = False
        fails += not ok
        print('%-4s %-28s %s' % ('ok' if ok else 'FAIL', ' '.join(c['q']) + (' --' + c['mode'] if c.get('mode') else ''),
                                 ', '.join(ids[:k]) or '(empty)'))
    print('\n%d/%d passed' % (len(cases) - fails, len(cases)))
    return 1 if fails else 0


CMDS = {'find': cmd_find, 'fetch': cmd_fetch, 'verify': cmd_verify, 'refresh': cmd_refresh,
        'stats': cmd_stats, 'audit': cmd_audit, 'searchtest': cmd_searchtest,
        'diff': cmd_diff, 'apply': cmd_apply}

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print(__doc__)
        print('commands: ' + ' '.join(CMDS))
        sys.exit(2)
    sys.exit(CMDS[sys.argv[1]](sys.argv[2:]))
