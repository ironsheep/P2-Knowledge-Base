#!/usr/bin/env python3
"""Walk a .docx in DOCUMENT ORDER, emitting paragraphs and tables.

Why this exists: a naive DOCX table walk iterates `//w:tbl` at the body level and
silently drops a table nested inside a table CELL. On the P2 Hardware Manual, 4 of
53 tables were nested that way -- and the pin drive ladder was in one of them. So
this walker recurses into cells and reports nesting depth.

It also preserves DOCUMENT ORDER (a paragraph between two tables stays between
them), which a two-pass "all paragraphs then all tables" extraction destroys.
"""
import sys, zipfile, re
from xml.etree import ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

def text_of(el):
    """Concatenate w:t runs, honouring tabs and breaks."""
    out = []
    for n in el.iter():
        if n.tag == W+'t':
            out.append(n.text or '')
        elif n.tag == W+'tab':
            out.append('\t')
        elif n.tag in (W+'br', W+'cr'):
            out.append('\n')
    return ''.join(out)

def style_of(p):
    ps = p.find(W+'pPr')
    if ps is None: return ''
    s = ps.find(W+'pStyle')
    return (s.get(W+'val') or '') if s is not None else ''

def heading_level(style):
    m = re.match(r'(?:Heading|heading)(\d)', style or '')
    return int(m.group(1)) if m else None

def is_monospace(p):
    """A run in a monospace face is a code signal."""
    for r in p.iter(W+'rPr'):
        f = r.find(W+'rFonts')
        if f is not None:
            for a in ('ascii','hAnsi','cs'):
                v = f.get(W+a) or ''
                if any(k in v.lower() for k in ('courier','consolas','mono','lucida console')):
                    return True
    return False

def walk_table(tbl, depth=0):
    """Yield ('table', rows, depth) for this table AND every table nested in a cell."""
    rows, nested = [], []
    for tr in tbl.findall(W+'tr'):
        cells = []
        for tc in tr.findall(W+'tc'):
            # cell text = its direct paragraphs only
            ct = ' '.join(text_of(p).strip() for p in tc.findall(W+'p'))
            cells.append(re.sub(r'\s+', ' ', ct).strip())
            # a table INSIDE this cell -- the case a naive walk loses
            for inner in tc.findall(W+'tbl'):
                nested.append(inner)
        rows.append(cells)
    yield ('table', rows, depth)
    for inner in nested:
        yield from walk_table(inner, depth+1)

def walk(docx):
    z = zipfile.ZipFile(docx)
    root = ET.fromstring(z.read('word/document.xml'))
    body = root.find(W+'body')
    for child in body:
        if child.tag == W+'p':
            yield ('para', text_of(child), style_of(child), is_monospace(child))
        elif child.tag == W+'tbl':
            yield from walk_table(child, 0)

if __name__ == '__main__':
    src = sys.argv[1]
    paras = tables = nested = mono = 0
    for item in walk(src):
        if item[0] == 'para':
            paras += 1
            if item[3]: mono += 1
        else:
            tables += 1
            if item[2] > 0: nested += 1
    print(f"  paragraphs      : {paras:,}")
    print(f"  monospace paras : {mono:,}")
    print(f"  tables TOTAL    : {tables}")
    print(f"  of which NESTED : {nested}")
