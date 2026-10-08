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
import posixpath
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'sources')
GUIDES = os.path.join(ROOT, 'guides')
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
SOURCE_STATUS = ('active', 'degraded', 'parser-broken', 'offline', 'closed')
FOUNDATIONS = ('own-tokens', 'host-tokens', 'shadcn-compatible', 'none', 'n/a')
DARK_MODES = ('class', 'data-theme', 'media', 'prop', 'none', 'n/a', 'unknown')
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
#
# Matching contract (summarised in scripts/aliases.json and `find.sh --help`; tests in scripts/tests/test_search.py):
# - ASCII words, typed or coming from an alias group, match whole words in ids, names, categories, descriptions
#   and tags, ignoring case. Hyphens and punctuation separate words ("table" hits "data-table"). A regular
#   English plural also matches (plan→plans, bus→buses, gallery→galleries), but a longer word with the same
#   start does not: "plan" does not hit "plane", "tab" does not hit "table", "ai" does not hit "detail".
# - Chinese terms match as substrings. A Chinese token that is not itself an alias term is split greedily into
#   the longest alias terms it contains; leftover runs of two or more characters are kept as their own concepts
#   when they occur in the catalogue and are not filler words, so 侧边栏可折叠 becomes 侧边栏 + 折叠.
# - Adjacent words that form an alias phrase ("dark mode" → dark-mode, "tool call") are read as one concept.
# - A concept matches when its own term or any term of its alias groups matches; concepts from the same group
#   are merged. Results keep the rows that match the most concepts.

CJK = re.compile(r'[㐀-鿿豈-﫿]')
# single characters that only glue a Chinese request together, and words too generic to search for
FUNC_CHARS = set('的地得了着和与及或在把被给让带用个一我你要想做加请帮将')
FILLER = {'一个', '一些', '一下', '一种', '这个', '那个', '这种', '那种', '可以', '需要', '我要', '我想', '想要', '怎么',
          '如何', '什么', '页面', '效果', '组件', '样式', '功能', '实现', '使用', '支持', '带有', '具有', '以及', '还有',
          '类似', '能够', '用于', '适合', '东西', '部分', '区域', '地方', '时候', '界面', '风格', '好看', '漂亮', '简单',
          '现代', '高级', '合适', '一点', '喜欢', '可能', '应该', '进行', '输出', '显示', '展示', '内容', '模式', '整个',
          '所有', '各种', '多个'}
ICON_TERMS = {'图标', 'icon', 'glyph', 'svg'}
PRIMARY_BASES = ('shadcn', 'uiarc')


def load_groups():
    with open(os.path.join(ROOT, 'scripts', 'aliases.json'), encoding='utf-8') as f:
        groups = json.load(f)['groups']
    return [[t.lower() for t in g] for g in groups]


def term_re(term):
    """Whole-word matcher for ASCII terms (with a regular English plural); substring matcher otherwise."""
    if not re.match(r'^[a-z0-9 ._+#/-]+$', term):
        return re.compile(re.escape(term))
    if re.search(r'(?:s|x|z|ch|sh)$', term):
        stem, plural = term, '(?:es)?'
    elif re.search(r'[^aeiou]y$', term):
        stem, plural = term[:-1], '(?:y|ies)'
    else:
        stem, plural = term, 's?'
    return re.compile(r'(?<![a-z0-9])' + re.escape(stem) + plural + r'(?![a-z0-9])')


def singular(term, vocab, corpus_text):
    """A typed English plural becomes its singular (buttons→button, boxes→box, galleries→gallery) when the singular
    is an alias term or a word of at least four letters in the catalogue; the singular's matcher covers both forms.
    Words that only look plural stay as typed (glass, status, canvas)."""
    if not re.match(r'^[a-z]{4,}$', term) or not term.endswith('s'):
        return term
    cands = ([term[:-3] + 'y'] if term.endswith('ies') else []) + (
        [term[:-2]] if re.search(r'(?:s|x|z|ch|sh)es$', term) else []) + [term[:-1]]
    for c in cands:
        if term_re(c).fullmatch(term) and (c in vocab or (len(c) >= 4 and re.search(
                r'(?<![a-z0-9])%s(?![a-z0-9])' % re.escape(c), corpus_text))):
            return c
    return term


def split_cjk(token, groups, corpus):
    """Greedy longest-match split of a Chinese token into alias terms plus meaningful leftover runs."""
    terms = sorted({m for g in groups for m in g if len(m) >= 2}, key=len, reverse=True)
    segs, run, i = [], '', 0

    def flush(run):
        for piece in re.split('[%s]' % ''.join(FUNC_CHARS), run):
            start = 0
            while len(piece) - start >= 2:
                # longest substring starting here that the catalogue actually contains
                end = next((e for e in range(len(piece), start + 1, -1)
                            if piece[start:e] not in FILLER and piece[start:e] in corpus_text), None)
                if end:
                    segs.append(piece[start:end])
                    start = end
                else:
                    start += 1

    corpus_text = '\n'.join(corpus)
    while i < len(token):
        m = next((t for t in terms if token.startswith(t, i)), None)
        if m:
            flush(run)
            run = ''
            segs.append(m)
            i += len(m)
        else:
            run += token[i]
            i += 1
    flush(run)
    return segs


def concepts(tokens, groups, corpus):
    """Turn query tokens into concepts: [(term, {alias terms})], merging concepts that share an alias group."""
    vocab = {t for g in groups for t in g}
    toks = [t.lower().strip('.,;:!?，。；：！？、"\'“”‘’()（）') for t in tokens]
    toks = [t for t in toks if t]
    merged, i = [], 0
    while i < len(toks):  # adjacent words that form an alias phrase: "dark mode" -> dark-mode, "tool call"
        for j in range(min(len(toks), i + 3), i + 1, -1):
            phrase = next((p for p in (' '.join(toks[i:j]), '-'.join(toks[i:j])) if p in vocab), None)
            if phrase:
                merged.append(phrase)
                i = j
                break
        else:
            merged.append(toks[i])
            i += 1
    terms, corpus_text = [], '\n'.join(corpus)
    for t in merged:
        if t in vocab or not CJK.search(t):
            terms.append(singular(t, vocab, corpus_text))
        else:
            terms.extend(split_cjk(t, groups, corpus) or [t])
    out = []
    for t in terms:
        alts = set()
        for g in groups:
            if t in g:
                alts.update(g)
        alts.discard(t)
        for c in out:
            if t == c[0] or t in c[1] or c[0] in alts:  # same group as an earlier concept: one concept
                c[1].update(alts | {t})
                c[1].discard(c[0])
                break
        else:
            out.append((t, alts))
    return out


def compile_concepts(cons):
    """[(term, matcher, aliases, alias matchers in sorted(aliases) order)]"""
    return [(t, term_re(t), alts, [term_re(a) for a in sorted(alts)]) for t, alts in cons]



def norm(s):
    return re.sub(r'[\s_-]+', '', s.lower())


def specific(term):
    """Terms precise enough that a match in a description alone is a real hit, not a coincidence."""
    return len(term) >= 3 if CJK.search(term) else (' ' in term or '-' in term or len(term) >= 6)


def relevance(r, cons):
    """Field-weighted match. Returns (score, concepts hit, concepts hit strongly, exact name hits); a concept hits
    strongly at name or category level, or in the description through a specific term (工具调用, confetti)."""
    primary, _, secondary = r['task'].partition(',')
    fields = ((3, (r['id'] + ' ' + r['name']).lower()), (2, (r['category'] + ' ' + primary).lower()),
              (1, ' '.join((r['desc'], secondary, r['vtags'], r['itags'])).lower()))
    names = {norm(r['id']), norm(r['id'].rsplit(':', 1)[-1]), norm(r['name'])}
    s, hit, strong, exact = 0.0, 0, 0, 0
    for term, rx, alts, alt_rxs in cons:
        scores, sure = [], False
        for w, text in fields:
            if rx.search(text):
                scores.append(w + 1.0)
                sure = sure or w >= 2 or specific(term)
            else:
                matched = next((a for a, arx in zip(sorted(alts), alt_rxs) if arx.search(text)), None)
                if matched is None:
                    continue
                scores.append(w * 0.6)  # a typed word in the description outranks an alias in the name
                sure = sure or w >= 2 or specific(matched)
        if scores:
            hit += 1
            strong += sure
            exact += bool(names & {norm(x) for x in alts | {term}})
            # Best field counts fully; corroborating fields (e.g. category "Backgrounds" + desc "背景") add a bonus.
            s += max(scores) + 0.5 * (len(scores) - 1)
    return s, hit, strong, exact


def klass(r):
    """What an agent can do with a row now: 3 take code or prompt, 2 needs the user's login, 1 look only, 0 none."""
    if r['access'] == 'free':
        return 1 if r['usage'] == 'reference' else 3
    return 2 if r['access'] == 'login' else 0


def tier(r):
    """Within the same class, components before their demo variants and prompts."""
    return 1 if r['category'].startswith('example') or r['usage'] == 'prompt' else 2


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


def compat_matrix():
    """{(a, b): verdict text} from the compatibility matrix in sources/_styles.md; '*' stands for 任意 / 任意底座."""
    out, inside = {}, False
    with open(os.path.join(SRC, '_styles.md'), encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith('## '):
            inside = line.startswith('## 兼容矩阵')
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')] if inside and line.startswith('|') else []
        if len(cells) < 2 or '+' not in cells[0]:
            continue
        left, right = (re.sub(r'（[^）]*）', '', s).strip() for s in cells[0].split('+', 1))
        for a in left.split('/'):
            for b in right.split('/'):
                out[('*' if a.strip().startswith('任意') else a.strip(), b.strip())] = cells[1]
    return out


def compat_verdict(base, source, matrix):
    """same | ok | conditional | no | unknown, for putting `source` on a page whose primary base is `base`."""
    if source == base:
        return 'same'
    v = matrix.get((base, source)) or matrix.get((source, base)) or matrix.get(('*', source))
    if v is None:
        return 'unknown'
    if '不建议' in v:
        return 'no'
    if '有条件' in v and ('；' not in v or base in v.split('；', 1)[1]):  # "可以；uiarc 底座有条件"
        return 'conditional'
    return 'ok'


def flagged(claims, r):
    """Engineering problems recorded for a row: ledger rows of kind defect/demo, plus the human note."""
    return [c for c in claims.get('%s:%s' % (r['source'], r['id']), []) if c['kind'] in ('defect', 'demo')]


def claims_by_ref():
    out = {}
    for c in load_claims():
        out.setdefault(c['ref'], []).append(c)
    return out


def search(terms, src=None, mode='default', task=None, layer=None, info=None, base=None):
    """Rank catalogue rows for a query. Returns ([(score, row)], note); `info`, if given, receives details
    (hidden_icons, base_hidden, low_confidence) for callers that need more than the note text. With `base`, rows
    the compatibility matrix rules out for that primary base are dropped and the rest carry r['_compat']."""
    info = {} if info is None else info
    terms = [x for t in terms for x in t.split()]  # "多选 筛选" passed as one quoted argument
    rows = [r for r in load_rows(src) if FIND_MODES[mode][1](r)
            and (not task or task in r['task'].split(',')) and (not layer or r['layer'] == layer)]
    info['base_hidden'] = 0
    if base:
        matrix = compat_matrix()
        for r in rows:
            r['_compat'] = compat_verdict(base, r['source'], matrix)
    claims = claims_by_ref()
    groups = load_groups()
    corpus = [' '.join((r['id'], r['name'], r['category'], r['task'], r['desc'], r['vtags'], r['itags'])).lower()
              for r in rows]
    cons = compile_concepts(concepts(terms, groups, corpus))
    icon_query = (src == 'lucide' or task == 'icon' or layer == 'icons'
                  or any(ICON_TERMS & ({t} | alts) for t, _, alts, _ in cons))
    scored, icons = [], []
    for r in rows:
        rel, hit, strong, exact = relevance(r, cons) if cons else (0.0, 0, 0, 0)
        if cons and not hit:
            continue
        if r.get('_compat') == 'no':  # the matrix says not on the same page as this base
            info['base_hidden'] += 1
            continue
        band = 1 if not cons or strong * 2 >= hit else 0  # at least half the matched concepts hit strongly
        primary = r['source'] in PRIMARY_BASES
        clean = not flagged(claims, r) and not r['notes']  # known demo-only or defective rows go after equal peers
        row = (hit, klass(r), band, clean, exact, bool(exact) and primary, tier(r), rel, primary,
               r['layer'] == 'foundation', r)
        # Icon names and tags match almost any English word, so icons only show when asked for, or when nothing
        # else matched (a query like "avocado").
        (icons if r['source'] == 'lucide' and not icon_query else scored).append(row)
    hidden_icons = len(icons) if scored else 0
    scored = scored or icons
    note = ''
    if cons and scored:
        top = max(x[0] for x in scored)
        if top < len(cons):
            note = '（没有条目同时命中全部 %d 个词，以下是命中 %d 个的结果）' % (len(cons), top)
        scored = [x for x in scored if x[0] == top]
    ranked = sorted(scored, key=lambda x: tuple(-v for v in x[:10]))
    info['hidden_icons'] = hidden_icons
    info['low_confidence'] = bool(cons and ranked and (ranked[0][2] == 0 or ranked[0][0] < len(cons)))
    if info['low_confidence']:
        note += ('\n低置信度：最靠前的结果只在描述里沾边，或只命中了部分词。先换更具体的词或用 --task 再搜；'
                 '仍然没有合适的，就说明"收藏库无合适候选"并自己实现。')
    if ranked and not any(x[1] == 3 for x in ranked):
        note += '\n没有现在就能取码的免费候选：以下只有需登录、灵感参考或 Pro / 失效条目。'
    return [(x[7], x[10]) for x in ranked], note


def guide_task(scored):
    """Guess the guide from what an agent would actually use: the main task of the top obtainable rows, or of the
    top rows when nothing obtainable matched. Hidden icons never take part."""
    pool = [r for _, r in scored if klass(r) == 3][:10] or [r for _, r in scored][:10]
    counts = {}
    for r in pool:
        t = r['task'].split(',')[0]
        counts[t] = counts.get(t, 0) + 1
    return max(counts, key=counts.get) if counts else None


def guide_index():
    """{ref: [(guide file, line, section)]} for every `source:id` written in the guides."""
    out = {}
    for fn in (sorted(os.listdir(GUIDES)) if os.path.isdir(GUIDES) else []):
        if fn.endswith('.md') and not fn.startswith('_'):
            section = ''
            with open(os.path.join(GUIDES, fn), encoding='utf-8') as f:
                lines = f.readlines()
            for n, line in enumerate(lines, 1):
                if line.startswith('## '):
                    section = line[3:].strip()
                for ref in GUIDE_REF.findall(line):
                    out.setdefault(ref, []).append((fn, n, section))
    return out


COMPAT_ZH = {'conditional': '有条件', 'unknown': '兼容性未登记'}


def cmd_find(args):
    src, limit, mode, terms, task, layer, base = None, 25, 'default', [], None, None, None
    it = iter(args)
    for a in it:
        if a == '-s':
            src = next(it)
        elif a == '--base':
            base = next(it)
        elif a == '--task':
            task = next(it)
        elif a == '--layer':
            layer = next(it)
        elif a == '--limit':
            limit = int(next(it))
        elif a in ('-h', '--help'):
            print('usage: find.sh [-s source] [--base B] [--task T] [--layer L] [--limit N] [--code|--free|--ref|--all] [keyword...]')
            print('  --base   项目的主底座（如 shadcn、uiarc）：按 sources/_styles.md 的兼容矩阵去掉"不建议"同页的来源，标出"有条件"的')
            print('  --task   UI 任务：' + ' '.join(TASKS))
            print('  --layer  层级：' + ' '.join(LAYERS))
            for k, (d, _) in FIND_MODES.items():
                print('  %-9s %s' % ('(默认)' if k == 'default' else '--' + k, d))
            print('匹配：英文按整词（不分大小写，带规则复数：plan 命中 plans，不命中 plane）；中文按子串，长词按同义词表拆开；\n'
                  '      相邻词能组成同义词短语时合在一起（dark mode）。同义词表：scripts/aliases.json。\n'
                  '排序：能直接取码的免费条目 → 需登录 → 灵感参考；Lucide 图标只在查询带 icon/图标、--task icon 或 -s lucide 时列出。')
            return 0
        elif a.startswith('--') and a[2:] in FIND_MODES:
            mode = a[2:]
        else:
            terms.append(a)
    if task and task not in TASKS:
        sys.exit('unknown task %r. choose from: %s' % (task, ' '.join(TASKS)))
    if layer and layer not in LAYERS:
        sys.exit('unknown layer %r. choose from: %s' % (layer, ' '.join(LAYERS)))
    if base and base not in sources():
        sys.exit('unknown base %r. choose from: %s' % (base, ' '.join(sources())))
    info = {}
    scored, note = search(terms, src, mode, task, layer, info, base)
    icons = ('（另有 %d 个 Lucide 图标也匹配，默认不显示：查询里加 icon / 图标，或用 --task icon）' % info['hidden_icons']
             if info.get('hidden_icons') else '')
    if info.get('base_hidden'):
        icons += ('\n' if icons else '') + '（按 %s 底座去掉了 %d 个兼容矩阵里"不建议"同页的来源的条目，见 compat.sh %s）' % (
            base, info['base_hidden'], base)
    if not scored:
        print('no match：收藏库里没有相关条目。换更短的词、英文词或 --task 再搜；仍然没有，就说明"收藏库无合适候选"并自己实现。'
              + ('\n' + icons if icons else ''))
        return 1
    by_src = {}
    for _, r in scored:
        by_src[r['source']] = by_src.get(r['source'], 0) + 1
    print('%d matches (%s)  filter=%s %s%s' % (len(scored), ', '.join('%s %d' % kv for kv in sorted(by_src.items(), key=lambda x: -x[1])),
                                              mode, note, ('\n' + icons) if icons else ''))
    claims, guides, any_flag = claims_by_ref(), guide_index(), False
    for s, r in scored[:limit]:
        tag = label(r)
        compat = COMPAT_ZH.get(r.get('_compat'))
        print('[%s] %s:%s — %s  (%s · %s)%s%s' % (tag, r['source'], r['id'], r['name'], r['task'], r['layer'],
                                                 '  ⚠ ' + r['risk'] if r['risk'] else '',
                                                 '  · 与 %s：%s' % (base, compat) if compat else ''))
        print('    %s' % r['desc'][:160])
        ref = '%s:%s' % (r['source'], r['id'])
        flags = ['%s（%s %s）：%s' % (CLAIM_KINDS[c['kind']], CLAIM_DEPTHS[c['depth']], c['checked'], c['claim'])
                 for c in flagged(claims, r)] + (
            ['备注：' + r['notes']] if r['notes'] else [])
        for f in flags:
            print('    ⚑ %s' % (f if len(f) <= 120 else f[:118] + '…'))
        if flags:
            any_flag = True
            where = guides.get(ref, [])
            where = [w for w in where if w[2] == '慎用'] or where
            print('      详情：claims.sh %s%s' % (ref, '；guides/%s:%d' % where[0][:2] if where else ''))
    if len(scored) > limit:
        print('... %d more (--limit N)' % (len(scored) - limit))
    shown_task = task or guide_task(scored)
    if shown_task and os.path.exists(os.path.join(GUIDES, shown_task + '.md')):
        print('\n选型指南：guides/%s.md（先读默认推荐和慎用，再定组件；效果预算见 guides/_scenes.md）' % shown_task)
    print('排序只反映和查询的相关度、能不能现在取码，不代表组件成熟或适合你的项目。')
    if any_flag:
        print('⚑ = 已登记的工程问题（演示数据或定时器、缺回调、键盘不可用等），接真实业务前要改，或换同类候选；同等相关时排在没有问题的候选之后。')
    if any(r['risk'] for _, r in scored[:limit]):
        print('⚠ = 场景化审美风险（不禁止，用的话要在选型理由里说明适用场景，见 SKILL.md「质量分级」）')
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


class UnsafePath(ValueError):
    pass


def safe_rel(path):
    """A remote file path as a relative path that stays inside the output directory, or UnsafePath."""
    rel = posixpath.normpath(urllib.request.unquote(path).replace('\\', '/')).lstrip('/')
    if rel in ('', '.') or rel == '..' or rel.startswith('../') or '\0' in rel:
        raise UnsafePath('unsafe file path %r' % path)
    return rel


def save(out, name, body):
    """Write a file under `out`; `name` may contain sub-directories but must not leave `out`."""
    root = os.path.realpath(out)
    p = os.path.realpath(os.path.join(root, name))
    if not p.startswith(root + os.sep):
        raise UnsafePath('refusing to write outside %s: %r' % (out, name))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'wb') as f:
        f.write(body)
    return p


def registry_paths(files):
    """Relative output paths for registry files: the directory part all of them share is dropped, the rest is kept,
    so a/index.tsx and b/index.tsx stay apart while a single-folder item lands flat as before."""
    rels = [safe_rel(f.get('path') or 'file') for f in files]
    dirs = [r.split('/')[:-1] for r in rels]
    common = 0
    while dirs and all(len(d) > common for d in dirs) and len({d[common] for d in dirs}) == 1:
        common += 1
    out = ['/'.join(r.split('/')[common:]) for r in rels]
    if len(set(out)) != len(out):
        raise UnsafePath('registry lists the same file path twice: %s' % ', '.join(rels))
    return out


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
    missing = [f.get('path') for f in files if f.get('content') is None]
    if missing:  # validate everything before writing anything
        return False, 'file without content: %s (%s)' % (', '.join(map(str, missing)), url)
    try:
        rels = registry_paths(files)
    except UnsafePath as e:
        return False, '%s (%s)' % (e, url)
    save(out, 'registry-item.json', body)
    lines = []
    for f, rel in zip(files, rels):
        save(out, rel, f['content'].encode())
        lines.append('    %s (%d lines) <- %s' % (rel, f['content'].count('\n') + 1, f.get('path')))
    info = ['registry  %s' % url, '  sha256 %s' % sha(body)[:16]]
    for k in ('dependencies', 'devDependencies', 'registryDependencies'):
        if d.get(k):
            info.append('  %s: %s' % (k, ' '.join(d[k])))
    if d.get('registryDependencies'):
        info.append('  （只取了这一项本身；registryDependencies 没有一起下载，需要时用 fetch.sh 分别取，'
                    '或用安装命令让 shadcn CLI 解析）')
    if d.get('cssVars') or d.get('css'):
        info.append('  注意: 含 cssVars/css，需要合并进全局样式（见 registry-item.json）')
    return True, '\n'.join(info + ['  files:'] + lines)


MEDIA_EXT = ('.mp4', '.webm', '.mov', '.gif', '.png', '.jpg', '.jpeg', '.webp', '.avif')


def wrong_type(url, ct, body):
    """Why a downloaded body is not what the URL promised (an HTML login or fallback page, a page instead of
    media, an SVG URL without SVG), or '' when it looks right."""
    path = url.split('?')[0].split('#')[0].lower()
    head = body[:512].lstrip().lower()
    if not path.endswith(('.html', '.htm')) and ('text/html' in ct or head.startswith((b'<!doctype html', b'<html'))):
        return 'got an HTML page (login wall or fallback page?)'
    if path.endswith(MEDIA_EXT) and ct and not ct.startswith(('image/', 'video/', 'application/octet-stream', 'binary/')):
        return 'expected media, got %s' % ct.split(';')[0]
    if path.endswith('.svg') and b'<svg' not in body[:4096].lower():
        return 'expected SVG markup'
    return ''


def do_url(url, out, label='url'):
    st, ct, body = http(url)
    if st != 200 or not body:
        return False, 'HTTP %s %s' % (st, url)
    bad = wrong_type(url, ct, body)
    if bad:
        return False, '%s instead of the expected file: %s' % (bad, url)
    try:  # decode %2F and friends before taking the last segment, then refuse anything that is not a plain name
        name = posixpath.basename(safe_rel(url.split('?')[0].split('#')[0].split('://', 1)[-1]))
    except UnsafePath:
        name = ''
    if not name or name in ('.', '..'):
        name = 'index'
    if label == 'doc' and '.' not in name:
        name += '.md'
    save(out, ('doc-' if label == 'doc' else '') + name, body)
    return True, '%-9s %s\n  -> %s (%d bytes, sha256 %s)' % (label, url, ('doc-' if label == 'doc' else '') + name,
                                                            len(body), sha(body)[:16])


def do_prompt(url, out):
    st, ct, body = http(url)
    m = re.search(r'<pre id="agent-prompt"[^>]*>(.*?)</pre>', body.decode('utf-8', 'replace'), re.S) if st == 200 else None
    if not m:
        return False, 'prompt block not found (HTTP %s) %s' % (st, url)
    txt = html.unescape(m.group(1)).strip()
    save(out, 'prompt.md', txt.encode())
    return True, 'prompt    %s\n  -> prompt.md (%d chars)' % (url, len(txt))


def adapter_path(name):
    for ext, runner in (('.py', sys.executable), ('.sh', 'sh')):
        p = os.path.join(ADAPTERS, name + ext)
        if os.path.exists(p):
            return p, runner
    return None, None


ADAPTER_TIMEOUT = 180


def do_script(arg, out, opts):
    name, _, a = arg.partition(' ')
    path, runner = adapter_path(name)
    if not path:
        return False, 'missing adapter %s' % name
    cmd = [runner, path, a] + ([str(opts['limit'])] if opts.get('limit') else [])
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=ADAPTER_TIMEOUT)
    except subprocess.TimeoutExpired:
        return False, ('adapter %s timed out after %ds (site or network slow): retry once, then use the browser '
                       'route in sources/<source>.md' % (name, ADAPTER_TIMEOUT))
    if r.returncode != 0 or not r.stdout.strip():
        # adapters print one line naming the failed step and the HTTP status when there is one
        lines = [l for l in r.stderr.decode('utf-8', 'replace').splitlines() if l.strip()]
        return False, 'adapter %s failed (exit %d): %s' % (name, r.returncode, (lines[-1] if lines else 'no output')[:300])
    fn = '%s-%s.txt' % (name, re.sub(r'[^A-Za-z0-9_-]', '_', a))
    save(out, fn, r.stdout)
    return True, 'script    %s %s\n  -> %s (%d bytes, sha256 %s)' % (name, a, fn, len(r.stdout), sha(r.stdout)[:16])


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
    results = []
    for ref in refs:
        r = find_row(ref)
        o = dict(opts)  # each ref gets its own options: no URL or output dir leaks from the previous one
        if len(refs) > 1 and opts.get('out'):
            o['out'] = default_out(r, o, root=opts['out'])
        rc = fetch_one(r, o)
        results.append((ref, rc, o.get('_result', {})))
        if len(refs) > 1:
            print()
    if len(refs) > 1:
        print('## 汇总（逐条状态；整体退出码取最需要处理的一条：%s）' % ' > '.join(map(str, EXIT_PRIORITY)))
        for ref, rc, res in results:
            print('  %-44s %-8s exit %d  %s' % (ref, res.get('status', '?'), rc,
                                               '%d 个文件 → %s' % (res['files'], res['out']) if res.get('files') else ''))
    return batch_exit([rc for _, rc, _ in results])


# Exit codes of one fetch: 0 files fetched, 1 fetch failed (or only partly), 2 broken entry, 3 Pro, 4 needs the
# user's login, 5 nothing to download (open in a browser / follow the manual steps). A batch returns the code that
# most needs attention, in this order; the per-ref summary has the details.
EXIT_PRIORITY = (1, 4, 3, 2, 5, 0)


def batch_exit(codes):
    return next((c for c in EXIT_PRIORITY if c in codes), 0)


FETCH_HELP = """usage: fetch.sh <source:item_id> [...] [options]     （只读：下载到临时目录，不安装、不执行）

options:
  --out DIR          输出目录。默认 $TMPDIR/ui-arsenal/<source>/<id>[@style][@变体]/，不同 style、变体分开放；
                     一次取多个条目时，每条放在 DIR/<source>/<id>…/ 下
  --variant V        React Bits 变体：TS-TW（默认）| TS-CSS | JS-TW | JS-CSS
  --style S          shadcn style，要和项目 components.json 一致：
                     {base,radix,aria}-{vega,nova,maia,lyra,mira,luma,rhea,sera}，图表/主题只有 new-york-v4
  --limit N          列表类 adapter 的条数（collectui）

输出目录：先下载到临时暂存目录，全部校验通过才放进输出目录；目录里的 .ui-arsenal.json 记录这次取到的文件、
  来源和 hash。再次获取同一条目时只替换上一次写入的文件，上游删掉的文件不会残留；获取失败时上一次的结果也会移除，
  不会被当成新结果。registry 文件保留相对目录（去掉公共前缀），同名文件不会互相覆盖。

不同条目的输出：
  可安装 / 取源码   源码文件 + 依赖 + 安装命令（安装会改动项目，先确认项目栈）
  提示词            prompt.md / DESIGN.md，按内容实现
  仅参考            下载图片或视频；只能浏览器看的给出 URL
  需登录            不获取，输出登录方式和页面地址，由用户决定（退出码 4）
  Pro / 失效        不获取（退出码 3 / 2）

退出码：0 取到文件；1 获取失败或只取到一部分（看 FAIL 行：HTTP 码、超时、HTML 回落页、adapter 的出错步骤）；
  2 失效条目；3 Pro；4 需要用户登录；5 没有可下载的文件（只能在浏览器里看，或按来源文档手动操作）。
  一次取多个条目时末尾有逐条汇总，整体退出码取最需要处理的一条：1 > 4 > 3 > 2 > 5 > 0。

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
    if r['source'] == 'shadcn' and r['category'].startswith(('util', 'headless', 'helper')):
        return r['fetch'] + '\n  （项目已装 shadcn 时，先确认版本里是否已包含这个工具类或包，再决定是否升级）'
    if (opts.get('style') or opts.get('variant')) and opts.get('_final_url'):
        return ('npx shadcn@latest add %s\n  （用完整 URL 固定这个 style/变体；只写组件名时 CLI 会按项目 components.json 的 style 解析）'
                % opts['_final_url'])
    return re.split(r'\s*(?:；|; |#|\s文档|\s或\s)', r['fetch'])[0].strip()


MANIFEST = '.ui-arsenal.json'
DOWNLOAD_KINDS = ('registry', 'url', 'doc', 'prompt', 'script')


def default_out(r, opts, root=None):
    """<root>/<source>/<id>[@style][@variant]: different styles and variants never share a directory."""
    root = root or os.path.join(os.environ.get('TMPDIR', '/tmp'), 'ui-arsenal')
    name = re.sub(r'[^A-Za-z0-9_.-]', '_', r['id']) + ''.join(
        '@' + re.sub(r'[^A-Za-z0-9_.-]', '_', opts[k]) for k in ('style', 'variant') if opts.get(k))
    return os.path.join(root, r['source'], name)


def list_files(d):
    out = []
    for dp, _, fns in os.walk(d):
        out += [os.path.relpath(os.path.join(dp, f), d).replace(os.sep, '/') for f in fns]
    return sorted(x for x in out if posixpath.basename(x) != MANIFEST)


def read_manifest(out):
    try:
        with open(os.path.join(out, MANIFEST), encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def publish(staging, out, record):
    """Swap the previous result in `out` for the staged files and write the manifest. Only paths listed in the
    previous manifest are removed, so a user-chosen --out keeps whatever else it contains. A directory under the
    default root without a manifest was written by an older version of this tool and is cleared as a whole."""
    root = os.path.realpath(out)
    previous = (read_manifest(out) or {}).get('files', [])
    default_root = os.path.realpath(os.path.join(os.environ.get('TMPDIR', '/tmp'), 'ui-arsenal'))
    if not previous and root.startswith(default_root + os.sep) and os.path.isdir(root):
        previous = [{'path': rel} for rel in list_files(root)]
    for f in previous:
        try:
            p = os.path.realpath(os.path.join(root, safe_rel(f.get('path', ''))))
        except UnsafePath:
            continue
        if p.startswith(root + os.sep) and os.path.isfile(p):
            os.remove(p)
            d = os.path.dirname(p)
            while d != root and d.startswith(root + os.sep) and not os.listdir(d):
                os.rmdir(d)
                d = os.path.dirname(d)
    files = []
    for rel in list_files(staging):
        with open(os.path.join(staging, rel), 'rb') as f:
            body = f.read()
        save(out, rel, body)
        files.append({'path': rel, 'bytes': len(body), 'sha256': sha(body)[:16]})
    record['files'] = files
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, MANIFEST), 'w', encoding='utf-8') as f:
        json.dump(record, f, ensure_ascii=False, indent=1)
    return files


def fetch_one(r, opts, quiet=False):
    out = opts.get('out') or default_out(r, opts)
    log = (lambda *a: None) if quiet else print
    log('# %s:%s — %s  [%s · %s]' % (r['source'], r['id'], r['name'], USAGE_ZH.get(r['usage']), r['access']))
    if r['access'] == 'pro':
        log('Pro/付费条目：不获取。可作为灵感，用免费组件实现近似效果，并告诉用户这一条是 Pro。')
        opts['_result'] = {'status': 'pro'}
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
        opts['_result'] = {'status': 'login'}
        return 4
    if r['access'] == 'broken':
        log('此条目已失效或为空：%s' % r['fetch'])
        opts['_result'] = {'status': 'broken'}
        return 2
    ok_all, fetched, kinds = True, False, []
    staging = tempfile.mkdtemp(prefix='ui-arsenal-')  # nothing reaches `out` until every step has been checked
    try:
        for kind, arg in parse_spec(r['spec']):
            try:
                if kind == 'registry':
                    ok, msg = do_registry(arg, staging, opts)
                elif kind in ('url', 'doc'):
                    ok, msg = do_url(arg, staging, kind)
                elif kind == 'prompt':
                    ok, msg = do_prompt(arg, staging)
                elif kind == 'script':
                    ok, msg = do_script(arg, staging, opts)
                elif kind == 'browser':
                    ok, msg = True, 'browser   需在浏览器里打开（内置浏览器 get_page_text / read_page）：%s' % arg
                elif kind == 'manual':
                    ok, msg = True, 'manual    按 sources/%s.md「按需获取方法」操作：\n  %s' % (r['source'], r['fetch'])
                else:
                    ok, msg = False, 'unknown adapter %s' % kind
            except UnsafePath as e:
                ok, msg = False, str(e)
            log(('' if ok else 'FAIL ') + msg)
            ok_all &= ok
            fetched |= ok and kind in DOWNLOAD_KINDS
            kinds.append(kind)
        if not ok_all:
            status = 'partial' if fetched else 'failed'
        elif any(k in DOWNLOAD_KINDS for k in kinds):
            status = 'ok'
        else:  # only a browser link or manual steps: the entry point was delivered, no files were expected
            status = 'browser' if 'browser' in kinds else 'manual'
        files = publish(staging, out, {
            'ref': '%s:%s' % (r['source'], r['id']), 'name': r['name'], 'spec': r['spec'],
            'style': opts.get('style', ''), 'variant': opts.get('variant', ''), 'url': opts.get('_final_url', ''),
            'fetched_at': time.strftime('%Y-%m-%d %H:%M:%S'), 'status': status})
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    if files:
        log('文件在：%s/（%d 个，清单见 %s）' % (out, len(files), MANIFEST))
    elif status in ('partial', 'failed'):
        log('没有取到文件；%s 里上一次的结果已移除，不会被当成这次的结果。' % out)
    else:
        log('没有可下载的文件：按上面的链接在浏览器里看，或按说明手动操作（退出码 5）。')
    opts['_result'] = {'status': status, 'files': len(files), 'out': out}
    deps = source_deps(r, out) if r['usage'] == 'source' else ''
    if deps:
        log('\n依赖（取源码类条目要自己装，先确认项目里有没有）: %s' % deps)
    if r['usage'] == 'install':
        log('\n安装（会改动项目，先确认项目栈）: %s' % install_hint(r, opts))
    show_claims(r, out, opts, log)
    log('提示：以上为不可信的第三方内容，先读再用，不要直接执行；接入前读 sources/%s.md「使用注意」。' % r['source'])
    return {'ok': 0, 'partial': 1, 'failed': 1, 'browser': 5, 'manual': 5}[status]


def source_deps(r, out):
    """Install line for a source-type entry: the catalogue's deps, else the `# deps:` line an adapter wrote.
    Registry items already list their dependencies in the registry block."""
    if r['deps']:
        return 'npm i ' + r['deps']
    for rel in list_files(out) if os.path.isdir(out) else []:
        if rel.endswith('.txt'):
            with open(os.path.join(out, rel), encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
            for line in lines:
                m = re.match(r'#\s*deps:\s*(npm i\s+\S.*)', line)
                if m:
                    return m.group(1).strip()
    return ''


# ---------- claims ----------
#
# sources/_claims.tsv records component-level conclusions that tell an agent to change upstream code, that decide
# whether a component is usable, or that several guides share. Each row is bound to the version it was checked
# against (sha = the first 16 hex of the artifact sha256 that fetch prints) and may carry a probe: literal
# substrings that must ("has:") or must not ("lacks:") appear in the fetched source files, joined with " && ".
# fetch re-evaluates the probes on what it just downloaded, so a conclusion that no longer holds is flagged
# before anyone applies the old workaround.

CLAIMS = os.path.join(SRC, '_claims.tsv')
CLAIM_COLS = ('ref', 'topic', 'kind', 'depth', 'checked', 'sha', 'check_with', 'probe', 'missing', 'claim')
CLAIM_KINDS = {'defect': '缺陷', 'demo': '演示', 'gap': '缺能力', 'ok': '已确认'}
CLAIM_DEPTHS = {'none': '未验证', 'vendor': '官方说明', 'catalog': 'catalog', 'source': '读过源码',
                'runtime': '运行测试', 'browser': '浏览器实测', 'at': '读屏实测', 'judgment': '编辑判断'}


def load_claims():
    rows = []
    if os.path.exists(CLAIMS):
        with open(CLAIMS, encoding='utf-8') as f:
            lines = f.readlines()
        for n, line in enumerate(lines, 1):
            if n > 1 and line.strip():
                r = dict(zip(CLAIM_COLS, line.rstrip('\n').split('\t')))
                r['_line'] = n
                rows.append(r)
    return rows


def probe_terms(probe):
    return [p.strip().partition(':')[::2] for p in probe.split(' && ') if p.strip()]


def probe_texts(out):
    """Fetched source files as text; the registry wrapper, documentation pages and the manifest are left out."""
    texts = []
    for rel in (list_files(out) if os.path.isdir(out) else []):
        if rel == 'registry-item.json' or posixpath.basename(rel).startswith('doc-'):
            continue
        try:
            with open(os.path.join(out, rel), encoding='utf-8') as f:
                texts.append(f.read())
        except UnicodeDecodeError:
            pass
    return texts


def probe_eval(probe, texts):
    """Returns the probe terms that do not hold (empty list = the probe holds)."""
    return ['%s:%s' % (k, t) for k, t in probe_terms(probe) if (k == 'has') != any(t in x for x in texts)]


def artifact_sha(out):
    """sha of the main artifact in a fetch directory, matching the sha256 prefix fetch prints."""
    names = list_files(out) if os.path.isdir(out) else []
    pick = 'registry-item.json' if 'registry-item.json' in names else next(
        (n for n in names if not posixpath.basename(n).startswith('doc-')), None)
    if not pick:
        return ''
    with open(os.path.join(out, pick), 'rb') as f:
        return sha(f.read())[:16]


def claim_status(c, texts, now_sha):
    """(symbol, text) comparing a ledger row with freshly fetched files."""
    failed = probe_eval(c['probe'], texts) if c['probe'] else []
    if failed:
        return '✗', '版本%s，probe 不成立（%s）：这条结论已失效，不要照做基于它的修改，按拉到的源码重新判断' % (
            '已变' if c['sha'] and c['sha'] != now_sha else '未记录', '；'.join(failed))
    if c['sha'] and c['sha'] == now_sha:
        return '✓', '版本与核对时一致'
    if c['probe']:
        return '?', '版本%s（核对时 %s，现在 %s），probe 仍成立；结论里 probe 没覆盖的部分，照做前在源码里确认' % (
            '已变' if c['sha'] else '未记录', c['sha'] or '-', now_sha or '-')
    return '?', '版本%s（核对时 %s，现在 %s），没有 probe：照做前先在拉到的源码里确认' % (
        '已变' if c['sha'] else '未记录', c['sha'] or '-', now_sha or '-')


def claim_line(c):
    return '[%s·%s %s] %s：%s%s' % (CLAIM_KINDS.get(c['kind'], c['kind']), CLAIM_DEPTHS.get(c['depth'], c['depth']),
                                   c['checked'] or '-', c['topic'], c['claim'],
                                   '（未验证：%s）' % c['missing'] if c['missing'] else '')


def check_opts(c):
    o, it = {}, iter(c['check_with'].split())
    for a in it:
        if a in ('--style', '--variant'):
            o[a[2:]] = next(it, '')
    return o


def show_claims(r, out, opts, log):
    rows = [c for c in load_claims() if c['ref'] == '%s:%s' % (r['source'], r['id'])]
    if not rows:
        return
    texts, now = probe_texts(out), artifact_sha(out)
    log('\n已登记的结论（sources/_claims.tsv；✓ 仍适用  ? 需要确认  ✗ 已失效）：')
    for c in rows:
        mark, status = claim_status(c, texts, now)
        same_opts = check_opts(c) == {k: opts[k] for k in ('style', 'variant') if opts.get(k)}
        log('  %s %s\n    → %s%s' % (mark, claim_line(c), status,
                                     '' if same_opts else '（核对时用的是 %s）' % (c['check_with'] or '默认 style/变体')))


def guide_mentions(ref):
    hits = []
    for fn in (sorted(os.listdir(GUIDES)) if os.path.isdir(GUIDES) else []):
        if fn.endswith('.md'):
            with open(os.path.join(GUIDES, fn), encoding='utf-8') as f:
                lines = f.readlines()
            for n, line in enumerate(lines, 1):
                if '`%s`' % ref in line:
                    hits.append('guides/%s:%d' % (fn, n))
    return hits


def fetch_for_check(c, base):
    """Fetch what a ledger row was checked against into a fresh directory; returns (ok, out, error)."""
    out = os.path.join(base, re.sub(r'[^A-Za-z0-9_.-]', '_', c['ref'] + ' ' + c['check_with']))
    shutil.rmtree(out, ignore_errors=True)  # our own scratch directory under $TMPDIR
    if c['check_with'].startswith('https://'):
        ok, msg = do_url(c['check_with'], out)
        return ok, out, '' if ok else msg
    if c['ref'].startswith('npm:'):
        return False, out, 'npm ref needs a https:// check_with URL'
    try:
        row = find_row(c['ref'])
    except SystemExit as e:
        return False, out, str(e)
    rc = fetch_one(row, dict(check_opts(c), out=out), quiet=True)
    if rc == 1 and artifact_sha(out):  # e.g. a dead doc: link next to a registry item that did download
        return True, out, '部分获取失败（fetch exit 1），用已取到的文件复核'
    return rc == 0, out, '' if rc == 0 else 'fetch exit %d' % rc


GUIDE_REF = re.compile(r'`([a-z0-9]+:[A-Za-z0-9:._-]+)`')
EVIDENCE = (('pos', re.compile(r'已拉源码|已读源码|源码确认|已核对|已拉文档')), ('neg', re.compile(r'未拉源码|未读源码')),
            ('unverified', re.compile(r'未验证|未实测|未核对')), ('catalog', re.compile(r'catalog')))
SECTION_RANK = {'默认推荐': 0, '按场景换': 1, '接入要点': 2, '慎用': 3, '页面模式约束': 4, '候选清单': 5}


def narrow(subject, clause):
    """Pick the subject components a clause talks about: by bare id ("sidebar 731 行"), then by source name
    ("uiarc 版本…"). Returns (refs, ambiguous)."""
    named = [r for r in subject if re.search(r'(?<![\w-])%s(?![\w-])' % re.escape(r.split(':', 1)[1]), clause)]
    if named:
        return named, False
    by_src = [r for r in subject if r.split(':', 1)[0] in clause]
    pick = by_src or subject
    return pick, len(pick) > 1


def guide_evidence():
    """Heuristic scan of the evidence notes written in guides: each marker is attributed to the nearest component
    named before it in the same clause, else to the row's subject (the recommended column of a table row, or the
    components before the first '：' / ' — ' of a bullet), narrowed by the names the clause mentions.
    Returns [(guide, line, section, ref, kind, clause, ambiguous)]."""
    found = []
    for fn in (sorted(os.listdir(GUIDES)) if os.path.isdir(GUIDES) else []):
        if not fn.endswith('.md') or fn.startswith('_'):
            continue
        section = ''
        with open(os.path.join(GUIDES, fn), encoding='utf-8') as f:
            lines = f.readlines()
        for n, line in enumerate(lines, 1):
            if line.startswith('## '):
                section = line[3:].strip()
                continue
            if line.startswith('|'):
                cells = line.strip().strip('|').split('|')
                subject = GUIDE_REF.findall(cells[1]) if len(cells) > 2 else []
            else:
                cells = [line]
                head = re.split(r'：| — ', line, maxsplit=1)[0]
                subject = GUIDE_REF.findall(head)
            for cell in cells:
                for clause in re.split(r'[；。]', cell):
                    for kind, rx in EVIDENCE:
                        for m in rx.finditer(clause):
                            before = GUIDE_REF.findall(clause[:m.start()])
                            refs, amb = ([before[-1]], False) if before else narrow(subject, clause)
                            for ref in refs:
                                found.append((fn, n, section, ref, kind, clause.strip(), amb))
    return found


def cmd_claims(args):
    if not args or args[0] in ('-h', '--help'):
        print('usage: claims.sh <source:id>...      该组件登记的结论，以及哪些指南提到它\n'
              '       claims.sh --check [ref...]    重新拉取，用 probe 复核结论是否仍成立（只读，不改台账）\n'
              '       claims.sh --pending           待复核报告：台账里证据不足的结论 + 指南里标了未验证/catalog 的条目\n'
              '台账：sources/_claims.tsv，格式见 sources/_SPEC.md「结论台账」。')
        return 0
    claims = load_claims()
    if args[0] == '--check':
        refs = set(args[1:])
        rows = [c for c in claims if not refs or c['ref'] in refs]
        base = os.path.join(os.environ.get('TMPDIR', '/tmp'), 'ui-arsenal-claims')
        bad, cache = 0, {}
        for c in rows:
            key = (c['ref'], c['check_with'])
            if key not in cache:
                cache[key] = fetch_for_check(c, base)
            ok, out, err = cache[key]
            if not ok:
                bad += 1
                print('FAIL  %-34s %-24s 取不到：%s' % (c['ref'], c['topic'], err[:120]))
                continue
            now = artifact_sha(out)
            mark, status = claim_status(c, probe_texts(out), now)
            bad += mark == '✗'
            print('%-5s %-34s %-24s sha %s  %s%s' % ({'✓': 'same', '?': 'drift', '✗': 'STALE'}[mark], c['ref'], c['topic'],
                                                  now, '' if mark == '✓' else status[:90], ('  ' + err) if err else ''))
        print('\n%d rows checked, %d stale or unreachable. 台账不会被自动改写：确认后手动更新 sha、checked，失效的结论连同引用它的指南一起改。'
              % (len(rows), bad))
        return 1 if bad else 0
    if args[0] == '--pending':
        return claims_pending(claims)
    for ref in args:
        rows = [c for c in claims if c['ref'] == ref]
        print('## %s' % ref)
        if not ref.startswith('npm:'):
            r = find_row(ref)
            print('  官方页面：%s   取码规格：%s' % (r['url'] or '-', r['spec']))
        for c in rows:
            print('  ' + claim_line(c) + ('  [核对取法 %s]' % c['check_with'] if c['check_with'] else '') +
                  ('  sha %s' % c['sha'] if c['sha'] else ''))
        if not rows:
            print('  （台账里没有登记）')
        mentions = guide_mentions(ref)
        if mentions:
            print('  指南提到：' + ', '.join(mentions))
    return 0


def claims_pending(claims):
    weak = [c for c in claims if c['depth'] in ('none', 'vendor', 'catalog', 'judgment') or c['missing']]
    print('# 台账里证据不足或缺验证项的结论（%d）' % len(weak))
    for c in sorted(weak, key=lambda c: (c['kind'] != 'defect', c['kind'] != 'demo', c['checked'])):
        print('- %s %s' % (c['ref'], claim_line(c)))
    ev = guide_evidence()
    by_ref = {}
    for g, n, sec, ref, kind, clause, amb in ev:
        by_ref.setdefault(ref, []).append((SECTION_RANK.get(sec, 9), g, n, sec, kind, clause, amb))
    pending = {ref: [x for x in xs if x[4] in ('neg', 'unverified', 'catalog')] for ref, xs in by_ref.items()}
    pending = {ref: xs for ref, xs in pending.items() if xs}
    print('\n# 指南里只有 catalog / 未拉源码 / 未验证 依据的条目（%d 个组件，按最靠前的章节排序：默认推荐优先）' % len(pending))
    print('# 启发式：按"同一分句里前面最近的组件"归属，表格行和多组件句子要回原文确认。')
    for ref, xs in sorted(pending.items(), key=lambda kv: (min(x[0] for x in kv[1]), kv[0])):
        xs.sort()
        print('- %s  [%s]' % (ref, '、'.join(sorted({x[3] for x in xs}, key=lambda s: SECTION_RANK.get(s, 9)))))
        for _, g, n, sec, kind, clause, amb in xs[:4]:
            print('    guides/%s:%d %s%s：%s' % (g, n, kind, '（归属不确定）' if amb else '', clause[:90]))
    clear = {ref: [x for x in xs if not x[6]] for ref, xs in by_ref.items()}
    conflicts = {ref: xs for ref, xs in clear.items()
                 if {x[4] for x in xs} >= {'pos', 'neg'} and len({x[1] for x in xs}) > 1}
    print('\n# 不同指南对"是否读过源码"说法不一致（%d；只统计归属明确的标注）' % len(conflicts))
    for ref, xs in sorted(conflicts.items()):
        print('- %s' % ref)
        for _, g, n, sec, kind, clause, amb in sorted(xs):
            if kind in ('pos', 'neg'):
                print('    guides/%s:%d %s：%s' % (g, n, kind, clause[:90]))
    return 0


# ---------- verify ----------

# Fixed scenarios covering every adapter kind and every access rule. Expected exit code per fetch_one:
# 0 ok, 2 broken, 3 pro, 4 login (blocked on the user), 5 browser/manual only. `files` = whether files must land.
MATRIX = [
    ('registry', 'shadcn:button', {}, 0, True),
    ('registry+style', 'shadcn:button', {'style': 'radix-nova'}, 0, True),
    ('registry+variant', 'reactbits:split-text', {'variant': 'JS-CSS'}, 0, True),
    ('registry+doc', 'uiarc:in-view-title', {}, 0, True),
    ('adapter(bencho, literal parse)', 'bencho:magnet-select', {}, 0, True),
    ('adapter(collectui, anon API)', 'collectui:category:dashboard', {'limit': 3}, 0, True),
    ('prompt+doc', 'librariesdev:thinking-orbs', {}, 0, True),
    ('url(svg)', 'lucide:house', {}, 0, True),
    ('url(DESIGN.md)', 'getdesign:stripe', {}, 0, True),
    ('url(video)+browser', 'bencho:find:vanjek-pixel-select', {}, 0, True),
    ('browser-only', 'inspora:fluid-illumination', {}, 5, False),
    ('login refused', 'originkit:compare-slider', {}, 4, False),
    ('pro refused', 'uiarc:voice-orb', {}, 3, False),
    ('broken refused', 'collectui:category:agency', {}, 2, False),
]


def run_case(ref, opts, base):
    out = os.path.join(base, re.sub(r'[^A-Za-z0-9_.-]', '_', ref))
    shutil.rmtree(out, ignore_errors=True)  # our own scratch directory under $TMPDIR
    rc = fetch_one(find_row(ref), dict(opts, out=out), quiet=True)
    return rc, [f['path'] for f in (read_manifest(out) or {}).get('files', [])]


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
        for k in ('id', 'name', 'url', 'kind', 'pro', 'fetch', 'verified', 'source_status', 'visual_style',
                  'foundation', 'styling', 'motion_lib', 'dark_mode', 'mixing_notes'):
            if k not in fm:
                errs.append('%s.md: missing frontmatter %s' % (s, k))
        for k, allowed in (('source_status', SOURCE_STATUS), ('foundation', FOUNDATIONS), ('dark_mode', DARK_MODES)):
            if k in fm and fm[k] not in allowed:
                errs.append('%s.md: %s %r (allowed: %s)' % (s, k, fm[k], ' '.join(allowed)))
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
    # guides must only reference catalogue items that exist
    known = {(r['source'], r['id']) for r in load_rows(include_removed=True)}
    srcs = set(sources())
    warns = []
    if os.path.isdir(GUIDES):
        for fn in sorted(os.listdir(GUIDES)):
            if not fn.endswith('.md') or fn.startswith('_'):
                continue
            if fn[:-3] not in TASKS:
                errs.append('guides/%s: file name is not a task id' % fn)
            for m in re.finditer(r'`([a-z0-9]+):([A-Za-z0-9:._-]+)`', open(os.path.join(GUIDES, fn), encoding='utf-8').read()):
                if m.group(1) in srcs and (m.group(1), m.group(2)) not in known:
                    errs.append('guides/%s: unknown item `%s:%s`' % (fn, m.group(1), m.group(2)))
        missing = [t for t in TASKS if t != 'other' and not os.path.exists(os.path.join(GUIDES, t + '.md'))]
        if missing:
            warns.append('no guide yet for: ' + ' '.join(missing))
    errs += audit_claims(known)
    for e in errs[:200]:
        print(e)
    for w in warns:
        print('warning: ' + w)
    print('%d rows checked, %d problems' % (total, len(errs)))
    return 1 if errs else 0


def audit_claims(known):
    """Format checks for sources/_claims.tsv. Unverified conclusions are allowed; they are reported by
    `claims --pending`, not treated as format errors."""
    errs, seen = [], set()
    if not os.path.exists(CLAIMS):
        return errs
    lines = open(CLAIMS, encoding='utf-8').read().split('\n')
    if lines[0].split('\t') != list(CLAIM_COLS):
        errs.append('_claims.tsv:1: header must be: ' + ' '.join(CLAIM_COLS))
    for n, line in enumerate(lines[1:], 2):
        if not line.strip():
            continue
        c = line.split('\t')
        where = '_claims.tsv:%d' % n
        if len(c) != len(CLAIM_COLS):
            errs.append('%s: %d columns (need %d)' % (where, len(c), len(CLAIM_COLS)))
            continue
        r = dict(zip(CLAIM_COLS, c))
        src, _, iid = r['ref'].partition(':')
        if src == 'npm':
            if not iid:
                errs.append('%s: empty npm package' % where)
            if (r['probe'] or r['sha']) and not r['check_with'].startswith('https://'):
                errs.append('%s: npm ref with probe/sha needs a https:// check_with' % where)
        elif (src, iid) not in known:
            errs.append('%s: unknown ref %s' % (where, r['ref']))
        if (r['ref'], r['topic']) in seen:
            errs.append('%s: duplicate topic %s for %s' % (where, r['topic'], r['ref']))
        seen.add((r['ref'], r['topic']))
        if not re.match(r'^[a-z0-9-]+$', r['topic']):
            errs.append('%s: topic %r (lowercase kebab-case)' % (where, r['topic']))
        if r['kind'] not in CLAIM_KINDS:
            errs.append('%s: kind %r (allowed: %s)' % (where, r['kind'], ' '.join(CLAIM_KINDS)))
        if r['depth'] not in CLAIM_DEPTHS:
            errs.append('%s: depth %r (allowed: %s)' % (where, r['depth'], ' '.join(CLAIM_DEPTHS)))
        if r['depth'] != 'none' and not re.match(r'^\d{4}-\d{2}-\d{2}$', r['checked']):
            errs.append('%s: checked %r must be YYYY-MM-DD' % (where, r['checked']))
        if r['sha'] and not re.match(r'^[0-9a-f]{16}$', r['sha']):
            errs.append('%s: sha %r must be the 16 hex chars fetch prints' % (where, r['sha']))
        for k, text in probe_terms(r['probe']):
            if k not in ('has', 'lacks') or not text:
                errs.append('%s: probe term %r (use has:<text> or lacks:<text>, joined with " && ")' % (where, k + ':' + text))
        if r['check_with'] and not (r['check_with'].startswith('https://') or
                                    re.match(r'^(--(style|variant) \S+ ?)+$', r['check_with'])):
            errs.append('%s: check_with %r (an https URL, or --style/--variant options)' % (where, r['check_with']))
        if not r['claim']:
            errs.append('%s: empty claim' % where)
    return errs


def cmd_searchtest(args):
    """Run search relevance regression cases from scripts/search_cases.json."""
    cases = json.load(open(os.path.join(ROOT, 'scripts', 'search_cases.json'), encoding='utf-8'))['cases']
    fails = 0
    for c in cases:
        info = {}
        res, _ = search(c['q'], c.get('src'), c.get('mode', 'default'), c.get('task'), info=info, base=c.get('base'))
        ids = ['%s:%s' % (r['source'], r['id']) for _, r in res]
        k = c.get('k', 1)
        top = [r for _, r in res[:k]]
        checks = []  # every assertion present in the case must hold
        if c.get('empty'):
            checks.append(not res)
        if 'top1' in c:
            checks.append(bool(ids) and ids[0] == c['top1'])
        if 'topk_any' in c:
            checks.append(any(i in ids[:k] for i in c['topk_any']))
        if 'topk_any_id' in c:
            checks.append(any(re.search(c['topk_any_id'], r['id']) for r in top))
        if 'topk_all_category' in c:
            checks.append(bool(top) and all(re.search(c['topk_all_category'], r['category']) for r in top))
        if 'topk_all_id' in c:
            checks.append(bool(top) and all(re.search(c['topk_all_id'], r['id'] + ' ' + r['name'], re.I) for r in top))
        if 'topk_all_task_primary' in c:
            checks.append(bool(top) and all(r['task'].split(',')[0] == c['topk_all_task_primary'] for r in top))
        if 'topk_no_usage' in c:
            checks.append(bool(top) and all(r['usage'] != c['topk_no_usage'] for r in top))
        if 'topk_any_obtainable' in c:
            checks.append(any(klass(r) == 3 for r in top))
        if 'topk_all_access' in c:
            checks.append(bool(top) and all(r['access'] == c['topk_all_access'] for r in top))
        if 'none_id' in c:
            checks.append(not any(re.search(c['none_id'], r['id']) for _, r in res))
        if 'none_source' in c:
            checks.append(bool(res) and not any(r['source'] == c['none_source'] for _, r in res))
        if 'confident' in c:
            checks.append(bool(res) and info['low_confidence'] != c['confident'])
        if 'guide' in c:
            checks.append(guide_task(res) == c['guide'])
        if 'top1_clean' in c:
            checks.append(bool(res) and (not flagged(claims_by_ref(), res[0][1]) and not res[0][1]['notes']) == c['top1_clean'])
        ok = bool(checks) and all(checks)
        fails += not ok
        print('%-4s %-34s %s' % ('ok' if ok else 'FAIL', ' '.join(c['q']) + ''.join(
            {'mode': ' --%s', 'src': ' -s %s', 'task': ' --task %s', 'base': ' --base %s'}[x] % c[x]
            for x in ('mode', 'src', 'task', 'base') if c.get(x)), ', '.join(ids[:k]) or '(empty)'))
    print('\n%d/%d passed' % (len(cases) - fails, len(cases)))
    return 1 if fails else 0


def cmd_compat(args):
    """Look up rows of the compatibility matrix in sources/_styles.md that mention all given sources."""
    if not args or args[0] in ('-h', '--help'):
        print('usage: compat.sh <source> [source...]   例：compat.sh shadcn uiarc；只给一个来源时列出它的全部组合')
        return 0
    p = os.path.join(SRC, '_styles.md')
    lines = open(p, encoding='utf-8').read().splitlines()
    names = [a.lower() for a in args]
    hits = [l for l in lines if l.startswith('|') and all(n in l.lower() for n in names) and ('+' in l or len(names) == 1)]
    if not hits:
        print('兼容矩阵里没有同时提到 %s 的行；看 sources/_styles.md 的「混用规则」。' % ' + '.join(args))
        return 1
    for l in hits:
        print(l)
    for a in args:
        fm = frontmatter(a)
        if fm:
            print('\n%s: foundation=%s styling=%s motion=%s dark=%s\n  %s' % (
                a, fm.get('foundation'), fm.get('styling'), fm.get('motion_lib'), fm.get('dark_mode'), fm.get('mixing_notes', '')))
    return 0


CMDS = {'find': cmd_find, 'fetch': cmd_fetch, 'verify': cmd_verify, 'refresh': cmd_refresh,
        'stats': cmd_stats, 'audit': cmd_audit, 'searchtest': cmd_searchtest,
        'diff': cmd_diff, 'apply': cmd_apply, 'compat': cmd_compat, 'claims': cmd_claims}

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print(__doc__)
        print('commands: ' + ' '.join(CMDS))
        sys.exit(2)
    sys.exit(CMDS[sys.argv[1]](sys.argv[2:]))
