#!/usr/bin/env python3
"""
obex-catalog-mirror.py -- make each OBEX object YAML mirror its OBEX catalog page.

WHY THIS EXISTS (F-573, 2026-10-11)
    The KB's OBEX entries are a mirror of the Parallax OBEX catalog: we provide what the catalog
    says and pass no verdict on an object (doctrine overlay: "An OBEX entry carries what the catalog
    says, never our verdict on it"). The earlier scrapers did not mirror: they cut descriptions at
    100 characters, fell back to a placeholder ("Utility object for P2 development.") when a page
    did not parse, and filled category and tags from their own classifier. This tool reads the
    catalog fields straight from each object's page and writes OBEX's own values.

WHAT IT READS (per page)
    <ul id="obexinformation">  -- Object ID (date), Author, Content, Microcontroller, Language(s),
                                  Category, Licence, Tag(s)
    <div class="markdown-content"> -- the description, as text (paragraphs, list items)
    <title>                     -- "<object title> – Propeller OBEX"

WHAT IT WRITES (object_metadata.*)
    title, author                         <- page title, Author
    functionality.description_full        <- the description
    functionality.category                <- Category (a list when the page lists several)
    functionality.tags                    <- Tag(s) ([] when none)
    technical_details.languages           <- Language(s)
    technical_details.microcontroller     <- Microcontroller
    technical_details.content_type        <- Content (e.g. Code, PCB files)
    technical_details.licence             <- Licence
    metadata.created_date                 <- the Object ID line's date (YYYY-MM-DD)
    It never writes description_short: that is an authored one-liner (F-573), not catalog text.

USAGE
    obex-catalog-mirror.py fetch  --pages DIR            # polite: one page every 2.5 s
    obex-catalog-mirror.py report --pages DIR [--json F] # what would change; writes nothing
    obex-catalog-mirror.py apply  --pages DIR            # write the YAMLs
    A page that is missing, or whose field list does not parse, is reported and its YAML is left
    untouched -- never a fallback value.
"""
import argparse
import glob
import html
import json
import os
import re
import sys
import time
import urllib.request
from html.parser import HTMLParser

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OBJ_DIR = os.path.join(ROOT, "deliverables", "ai", "P2", "community", "obex", "objects")
USER_AGENT = "P2-Knowledge-Base catalog mirror (github.com/ironsheep/P2-Knowledge-Base)"
TITLE_SUFFIX = re.compile(r"\s+[–-]\s+Propeller OBEX\s*$")


def object_files():
    return sorted(glob.glob(os.path.join(OBJ_DIR, "[0-9]*.yaml")))


def page_url(data):
    return data["object_metadata"]["urls"]["obex_page"]


def fetch(pages):
    os.makedirs(pages, exist_ok=True)
    for f in object_files():
        oid = os.path.splitext(os.path.basename(f))[0]
        dest = os.path.join(pages, oid + ".html")
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            continue
        with open(f) as fh:
            url = page_url(yaml.safe_load(fh))
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as out:
            out.write(r.read())
        print(oid, os.path.getsize(dest))
        time.sleep(2.5)


def text_of(fragment):
    """Inline HTML -> text: tags dropped, entities decoded, whitespace collapsed."""
    t = re.sub(r"<br\s*/?>", "\n", fragment)
    t = html.unescape(re.sub(r"<[^>]+>", "", t))
    return "\n".join(" ".join(line.split()) for line in t.split("\n")).strip()


class _Text(HTMLParser):
    """The catalog's description HTML as plain text: a blank line between blocks, '- ' per list
    item (one line each), <br> as a line break, <pre>/<code> blocks verbatim."""
    BLOCK = {"p", "div", "ul", "ol", "table", "tr", "blockquote",
             "h1", "h2", "h3", "h4", "h5", "h6", "hr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.pre, self.line_start = [], 0, False

    def _brk(self, s):
        self.out.append(s)

    def handle_starttag(self, tag, attrs):
        if tag == "pre":
            self.pre += 1
            self._brk("\x00P")
        elif tag == "li":
            self._brk("\x00L")
        elif tag == "br":
            self._brk("\n")
            self.line_start = True
        elif tag in self.BLOCK:
            self._brk("\x00P")

    def handle_endtag(self, tag):
        if tag == "pre":
            self.pre -= 1
            self._brk("\x00P")
        elif tag in self.BLOCK or tag == "li":
            self._brk("\x00P" if tag != "li" else "\x00E")

    def handle_data(self, data):
        if self.pre:
            self.out.append(data)
            return
        text = re.sub(r"\s+", " ", data)
        if self.line_start:  # the newline after a <br> is source formatting, not a space
            text = text.lstrip()
            self.line_start = not text
        self.out.append(text)

    def text(self):
        s = "".join(self.out)
        s = re.sub(r"[ \t]*\x00E[ \t]*", "\x00E", s)
        # paragraph break; list item = newline + "- "; item end only separates items;
        # a <p> directly inside an <li> belongs to the item, not a new paragraph
        s = re.sub(r"(?:\s*\x00[PE])*\s*\x00L(?:\s*\x00P)*\s*", "\n- ", s)
        s = re.sub(r"\x00E(?:\s*\x00E)*", "\x00E", s)
        s = re.sub(r"\s*\x00E\s*(?=\n- )", "", s)
        s = re.sub(r"\s*(?:\x00[PE]\s*)+", "\n\n", s)
        lines = [ln.rstrip() for ln in s.split("\n")]
        s = "\n".join(lines)
        s = re.sub(r"\n{3,}", "\n\n", s)
        s = re.sub(r"(\n\n)(- )", r"\1\2", s)
        return s.strip()


def description_text(block):
    p = _Text()
    p.feed(block)
    p.close()
    return p.text()


ARCHIVER_MARK = re.compile(r"\s*\|\s*added by Archiver\s*$", re.I)
EMAIL_PAREN = re.compile(r"\s*\([^)]*@[^)]*\)")


def author_name(raw):
    """The catalog's Author text without OBEX's archive marker or a contact email.

    "| added by Archiver" is OBEX bookkeeping for objects moved from the old OBEX, not part of the
    name. An author line can carry a personal email in parentheses; a KB answer has no use for it,
    so the parenthetical is dropped (Stephen reviews this rule with F-573)."""
    return EMAIL_PAREN.sub("", ARCHIVER_MARK.sub("", raw)).strip()


def parse(page_html):
    """Return the catalog fields, or None when the field list is not on the page."""
    ul = re.search(r'<ul id="obexinformation"[^>]*>(.*?)</ul>', page_html, re.S)
    if not ul:
        return None
    fields = {}
    for li in re.findall(r"<li>(.*?)</li>", ul.group(1), re.S):
        if " : " not in text_of(li):
            continue
        label, _ = text_of(li).split(" : ", 1)
        links = [text_of(a) for a in re.findall(r"<a\b[^>]*>(.*?)</a>", li, re.S)]
        value = text_of(li).split(" : ", 1)[1]
        fields[label.strip()] = (value.strip(), links)
    out = {}
    oid = fields.get("Object ID", ("", []))[0]
    m = re.match(r"(\d+)\s*\((\d{4}-\d{2}-\d{2})", oid)
    out["object_id"] = m.group(1) if m else oid.split()[0] if oid else ""
    out["created_date"] = m.group(2) if m else ""
    out["author"] = author_name(fields.get("Author", ("", []))[0])
    # OBEX labels a field in the plural when it holds several values ("Categories :",
    # "Microcontrollers :", "Languages :", "Tags :"); read either form, every field.
    plural = {"Category": "Categories", "Content": "Contents", "Licence": "Licences",
              "Language": "Languages", "Microcontroller": "Microcontrollers", "Tag": "Tags"}

    def field(label):
        return fields.get(label) or fields.get(plural[label])

    for label, key in (("Content", "content_type"), ("Microcontroller", "microcontroller"),
                       ("Category", "category"), ("Licence", "licence"),
                       ("Language", "languages")):
        v = field(label)
        out[key] = (v[1] or [v[0]]) if v else []
    tags = field("Tag")
    out["tags"] = (tags[1] or [t.strip() for t in tags[0].split(",")]) if tags else []
    t = re.search(r"<title>(.*?)</title>", page_html, re.S)
    out["title"] = TITLE_SUFFIX.sub("", text_of(t.group(1))) if t else ""
    d = re.search(r'<div class="markdown-content">(.*?)</div>\s*<hr', page_html, re.S)
    out["description"] = description_text(d.group(1)) if d else ""
    return out


def one(v):
    """A single catalog value stays a string; several stay a list."""
    return v[0] if len(v) == 1 else v


def planned(om, cat):
    """(path, old, new) for every field this tool owns that differs from the catalog."""
    fn = om.setdefault("functionality", {})
    td = om.setdefault("technical_details", {})
    md = om.get("metadata", {})
    pairs = [
        (("title",), om.get("title"), cat["title"]),
        (("author",), om.get("author"), cat["author"]),
        (("functionality", "description_full"), fn.get("description_full"), cat["description"]),
        (("functionality", "category"), fn.get("category"), one(cat["category"]) if cat["category"] else ""),
        (("functionality", "tags"), fn.get("tags"), cat["tags"]),
        (("technical_details", "languages"), td.get("languages"), cat["languages"]),
        (("technical_details", "microcontroller"), td.get("microcontroller"), cat["microcontroller"]),
        (("technical_details", "content_type"), td.get("content_type"), cat["content_type"]),
        (("technical_details", "licence"), td.get("licence"), one(cat["licence"]) if cat["licence"] else ""),
        (("metadata", "created_date"), md.get("created_date"), cat["created_date"]),
    ]
    # A field the page leaves empty is written empty: keeping our old value would present our own
    # classification as the catalog's (32 objects carry no OBEX category). Only the description and
    # the date are never blanked -- a page without them is a parse problem, reported in run().
    keep_if_empty = {("functionality", "description_full"), ("metadata", "created_date"),
                     ("title",), ("author",)}
    return [(p, o, n) for p, o, n in pairs
            if o != n and not (p in keep_if_empty and n in ("", None))]


def set_path(om, path, value):
    node = om
    for k in path[:-1]:
        node = node.setdefault(k, {})
    node[path[-1]] = value


def run(pages, write, json_out=None):
    changes, problems = {}, []
    for f in object_files():
        oid = os.path.splitext(os.path.basename(f))[0]
        page = os.path.join(pages, oid + ".html")
        if not os.path.exists(page):
            problems.append((oid, "no saved page"))
            continue
        with open(page, encoding="utf-8", errors="replace") as fh:
            cat = parse(fh.read())
        if not cat:
            problems.append((oid, "field list not found on page"))
            continue
        if cat["object_id"] != oid:
            problems.append((oid, "page is for object %r" % cat["object_id"]))
            continue
        if not cat["description"]:
            problems.append((oid, "no description on page (other fields still mirrored)"))
        with open(f) as fh:
            data = yaml.safe_load(fh)
        om = data["object_metadata"]
        diffs = planned(om, cat)
        if diffs:
            changes[oid] = [{"field": ".".join(p), "old": o, "new": n} for p, o, n in diffs]
        if write and diffs:
            for p, _, n in diffs:
                set_path(om, p, n)
            with open(f, "w") as fh:
                yaml.dump(data, fh, sort_keys=False, allow_unicode=True, default_flow_style=False)
    if json_out:
        with open(json_out, "w") as fh:
            json.dump({"changes": changes, "problems": problems}, fh, indent=1, ensure_ascii=False)
    by_field = {}
    for rows in changes.values():
        for r in rows:
            by_field[r["field"]] = by_field.get(r["field"], 0) + 1
    print("objects changed:", len(changes), "of", len(object_files()))
    for k, v in sorted(by_field.items()):
        print("  %-36s %d" % (k, v))
    for oid, why in problems:
        print("PROBLEM", oid, why)
    return 1 if problems and write else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("mode", choices=("fetch", "report", "apply"))
    ap.add_argument("--pages", required=True)
    ap.add_argument("--json")
    a = ap.parse_args()
    if a.mode == "fetch":
        fetch(a.pages)
        return 0
    return run(a.pages, write=(a.mode == "apply"), json_out=a.json)


if __name__ == "__main__":
    sys.exit(main())
