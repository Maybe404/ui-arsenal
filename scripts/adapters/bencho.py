#!/usr/bin/env python3
"""Print a Bencho block's source without executing any remote JavaScript.

The site ships every block as a string literal inside one lazy chunk
(`/assets/blocks-<hash>.js`, `export{e as BLOCKS}`). This adapter downloads the
chunk as text and parses the object literal with a tiny literal-only parser:
objects, arrays, strings, numbers, true/false/null. Anything else (a function,
an identifier, a `${...}` interpolation) aborts instead of being evaluated.

usage: bencho.py <block-id> [prompt|tsx|css|meta]
"""
import json
import re
import sys
import urllib.request

UA = {'User-Agent': 'Mozilla/5.0'}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read().decode('utf-8')


class LiteralError(ValueError):
    pass


class Parser:
    ESC = {'n': '\n', 't': '\t', 'r': '\r', 'b': '\b', 'f': '\f', 'v': '\v', '0': '\0'}
    # Minifiers write true/false as !0/!1 and undefined as void 0. Keywords are matched before numbers and must end
    # at a word boundary, so `trueish` is rejected as an identifier instead of being read as true + garbage.
    KEYWORDS = {'!0': True, '!1': False, 'true': True, 'false': False, 'null': None, 'void 0': None}
    KEYWORD = re.compile(r'(?:!0|!1|true|false|null|void 0)(?![\w$])')
    NUMBER = re.compile(r'-?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?(?![\w$.])')  # minifiers also write .5

    def __init__(self, s, i):
        self.s, self.i = s, i

    def ws(self):
        while self.i < len(self.s) and self.s[self.i] in ' \t\r\n':
            self.i += 1

    def value(self):
        self.ws()
        c = self.s[self.i]
        if c == '{':
            return self.obj()
        if c == '[':
            return self.arr()
        if c in '"\'`':
            return self.string()
        m = self.KEYWORD.match(self.s, self.i)
        if m:
            self.i = m.end()
            return self.KEYWORDS[m.group(0)]
        m = self.NUMBER.match(self.s, self.i)
        if m:
            self.i = m.end()
            t = m.group(0)
            return float(t) if any(ch in t for ch in '.eE') else int(t)
        raise LiteralError('non-literal value at %d: %r' % (self.i, self.s[self.i:self.i + 40]))

    def key(self):
        self.ws()
        if self.s[self.i] in '"\'`':
            return self.string()
        m = re.compile(r'[A-Za-z_$][\w$]*|\d+').match(self.s, self.i)
        if not m:
            raise LiteralError('bad key at %d' % self.i)
        self.i = m.end()
        return m.group(0)

    def obj(self):
        out = {}
        self.i += 1
        while True:
            self.ws()
            if self.s[self.i] == '}':
                self.i += 1
                return out
            k = self.key()
            self.ws()
            if self.s[self.i] != ':':
                raise LiteralError('expected : at %d' % self.i)
            self.i += 1
            out[k] = self.value()
            self.ws()
            if self.s[self.i] == ',':
                self.i += 1

    def arr(self):
        out = []
        self.i += 1
        while True:
            self.ws()
            if self.s[self.i] == ']':
                self.i += 1
                return out
            out.append(self.value())
            self.ws()
            if self.s[self.i] == ',':
                self.i += 1

    def string(self):
        q = self.s[self.i]
        self.i += 1
        buf = []
        while True:
            c = self.s[self.i]
            if c == q:
                self.i += 1
                return ''.join(buf)
            if q == '`' and c == '$' and self.s[self.i + 1] == '{':
                raise LiteralError('template interpolation at %d (refusing to evaluate)' % self.i)
            if c == '\\':
                n = self.s[self.i + 1]
                if n == 'u':
                    if self.s[self.i + 2] == '{':
                        j = self.s.index('}', self.i)
                        buf.append(chr(int(self.s[self.i + 3:j], 16)))
                        self.i = j + 1
                    else:
                        buf.append(chr(int(self.s[self.i + 2:self.i + 6], 16)))
                        self.i += 6
                    continue
                if n == 'x':
                    buf.append(chr(int(self.s[self.i + 2:self.i + 4], 16)))
                    self.i += 4
                    continue
                if n == '\n':  # line continuation
                    self.i += 2
                    continue
                buf.append(self.ESC.get(n, n))
                self.i += 2
                continue
            buf.append(c)
            self.i += 1


def load_blocks():
    idx = re.search(r'/assets/index-[A-Za-z0-9_-]+\.js', get('https://bencho.dev/'))
    if not idx:
        raise SystemExit('bencho: index bundle not found')
    chunk = re.search(r'blocks-[A-Za-z0-9_-]+\.js', get('https://bencho.dev' + idx.group(0)))
    if not chunk:
        raise SystemExit('bencho: blocks chunk not found')
    src = get('https://bencho.dev/assets/' + chunk.group(0))
    m = re.search(r'export\s*\{\s*([A-Za-z_$][\w$]*)\s+as\s+BLOCKS\s*\}', src)
    if not m:
        raise SystemExit('bencho: BLOCKS export not found (site changed?)')
    decl = re.search(r'\b(?:var|let|const)\s+' + re.escape(m.group(1)) + r'\s*=\s*\{', src)
    if not decl:
        raise SystemExit('bencho: BLOCKS declaration not found (site changed?)')
    p = Parser(src, decl.end() - 1)
    try:
        return p.value()
    except LiteralError as e:
        raise SystemExit('bencho: cannot parse BLOCKS as a pure literal: %s' % e)
    except IndexError:
        raise SystemExit('bencho: cannot parse BLOCKS as a pure literal: unexpected end of input at %d' % p.i)


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    bid, part = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else 'prompt')
    blocks = load_blocks()
    b = blocks.get(bid)
    if not b:
        raise SystemExit('unknown id; available: ' + ' '.join(sorted(blocks)))
    if part == 'tsx':
        print(b['tsx'])
    elif part == 'css':
        print(b['css'])
    elif part == 'meta':
        print(json.dumps({k: b.get(k) for k in ('name', 'deps', 'tokens', 'stubs', 'props')}, indent=1))
    else:
        print('--- %s.tsx ---\n%s\n\n--- css ---\n%s\n\n# deps: npm i %s\n# css tokens to map: %s\n# stubs (replace with own assets): %s' % (
            b['name'], b['tsx'].strip(), b['css'].strip(), ' '.join(b.get('deps') or []),
            ', '.join(b.get('tokens') or []), ', '.join(b.get('stubs') or [])))


if __name__ == '__main__':
    main()
