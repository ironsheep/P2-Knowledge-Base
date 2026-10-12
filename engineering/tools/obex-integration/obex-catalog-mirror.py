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

    It is the ONLY tool that writes an object YAML (KB v1.24.4, Stephen 2026-10-12: "pure mirror"):
    it writes each object whole, so nothing of ours -- classification, compatibility, scraper
    bookkeeping, placeholders -- can ride beside the catalog's fields.

WHAT IT READS (per page)
    <ul id="obexinformation">  -- Object ID (date), Author, Content, Microcontroller, Language(s),
                                  Category, Licence, Tag(s)
    <div class="markdown-content"> -- the description, as text (paragraphs, list items; a link
                                  keeps its URL, written after its text)
    <title>                     -- "<object title> – Propeller OBEX"
    the Downloads section       -- the ZIP download (see download_link)

WHAT IT WRITES -- the whole object, in this order (object_metadata.*)
    object_id                             <- the file's id (checked against the page's Object ID)
    title, author                         <- page title, Author
    functionality.category                <- Category (a list when the page lists several)
    functionality.tags                    <- Tag(s) ([] when none)
    functionality.description_short       <- kept as it is: the authored one-liner (F-573)
    functionality.description_full        <- the description
    technical_details.content_type        <- Content (e.g. Code, PCB files)
    technical_details.microcontroller     <- Microcontroller
    technical_details.languages           <- Language(s)
    technical_details.licence             <- Licence
    metadata.created_date                 <- the Object ID line's date (YYYY-MM-DD)
    urls.obex_page                        <- kept as it is: the page this was read from
    urls.download_direct                  <- the ZIP download; no key when OBEX offers none

USAGE
    obex-catalog-mirror.py discover --pages DIR          # object pages on the listing with no YAML
    obex-catalog-mirror.py add --url URL --pages DIR     # start a YAML for a new object page
    obex-catalog-mirror.py fetch  --pages DIR            # save every object's page
    obex-catalog-mirror.py report --pages DIR [--json F] # what would change; writes nothing
    obex-catalog-mirror.py apply  --pages DIR            # write the YAMLs
    Every request is polite: one every 2.5 s, a neutral User-Agent, and a saved page is reused.
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
import urllib.parse
import urllib.request
from html.parser import HTMLParser

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OBJ_DIR = os.path.join(ROOT, "deliverables", "ai", "P2", "community", "obex", "objects")
USER_AGENT = "P2-Knowledge-Base catalog mirror (github.com/ironsheep/P2-Knowledge-Base)"
OBEX_SITE = "https://obex.parallax.com/"
ZIP_LINK = "wp-admin/admin-ajax.php?action=download_obex_zip&popcorn=salty&obuid=OB%s"
TITLE_SUFFIX = re.compile(r"\s+[–-]\s+Propeller OBEX\s*$")


def object_files():
    return sorted(glob.glob(os.path.join(OBJ_DIR, "[0-9]*.yaml")))


def page_url(data):
    return data["object_metadata"]["urls"]["obex_page"]


def fetch(pages):
    os.makedirs(pages, exist_ok=True)
    for f in object_files():
        oid = os.path.splitext(os.path.basename(f))[0]
        with open(f) as fh:
            get(page_url(yaml.safe_load(fh)), os.path.join(pages, oid + ".html"))
        print(oid, os.path.getsize(os.path.join(pages, oid + ".html")))


def link_target(href):
    """An absolute http(s) link the reader can follow, or "" for one they cannot: a relative link
    points into the object's own ZIP (the page renders its README), and mailto: would publish a
    personal address."""
    href = html.unescape(href or "").strip()
    return href if re.match(r"https?://", href, re.I) else ""


def norm_url(s):
    """For "is this URL already in the link text": scheme, www. and a trailing slash ignored."""
    s = re.sub(r"https?://(www\.)?", "", s.strip().lower())
    return re.sub(r"/(?=\s|$|\))", "", s)


LISTING = OBEX_SITE + "microcontroller/propeller-2/"


def get(url, dest):
    """Fetch url into dest once; a saved non-empty copy is reused."""
    if not (os.path.exists(dest) and os.path.getsize(dest) > 0):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as out:
            out.write(r.read())
        time.sleep(2.5)
    with open(dest, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def discover(pages):
    """Print every P2 object page on the OBEX listing that has no object YAML yet.

    The listing (LISTING, then page/2/ ... page/N/) shows ten entries a page. An entry that links
    outside /obex/<slug>/ (a Chips & Tips article) is not an object. A new object is one whose page
    URL no object YAML carries; add it with `add --url`, then `apply`. Listing pages are saved under
    <pages>/listing/ and reused, so delete that folder to see the catalog afresh."""
    os.makedirs(os.path.join(pages, "listing"), exist_ok=True)
    first = get(LISTING, os.path.join(pages, "listing", "1.html"))
    last = max([int(n) for n in re.findall(r'/microcontroller/propeller-2/page/(\d+)/', first)] or [1])
    found = re.findall(r'href="(%sobex/[^"/]+/)"' % re.escape(OBEX_SITE), first)
    for n in range(2, last + 1):
        t = get(LISTING + "page/%d/" % n, os.path.join(pages, "listing", "%d.html" % n))
        found += re.findall(r'href="(%sobex/[^"/]+/)"' % re.escape(OBEX_SITE), t)
    have = set()
    for f in object_files():
        with open(f) as fh:
            have.add(page_url(yaml.safe_load(fh)))
    listed = sorted(set(found))
    new = [u for u in listed if u not in have]
    print("listing pages:", last, " object pages listed:", len(listed), " with a YAML:",
          len(listed) - len(new), " new:", len(new))
    for u in new:
        print("NEW", u)
    gone = sorted(have - set(listed))
    for u in gone:
        print("NOT LISTED", u)
    return 0


def add(url, pages):
    """Start an object YAML for a new catalog page: its id and page URL only. `apply` then
    writes every catalog field; description_short is authored afterwards (F-573 gate)."""
    saved = os.path.join(pages, "new-%s.html" % re.sub(r"\W+", "-", url.rstrip("/").rsplit("/", 1)[-1]))
    cat = parse(get(url, saved))
    if not cat or not cat["object_id"].isdigit():
        print("PROBLEM", url, "no Object ID on the page")
        return 1
    oid = cat["object_id"]
    f = os.path.join(OBJ_DIR, oid + ".yaml")
    if os.path.exists(f):
        print("PROBLEM", url, "object", oid, "already has a YAML")
        return 1
    os.replace(saved, os.path.join(pages, oid + ".html"))  # where fetch/apply look for it
    with open(f, "w") as fh:
        yaml.dump({"object_metadata": {"object_id": oid, "urls": {"obex_page": url}}}, fh,
                  sort_keys=False, default_flow_style=False)
    print("added", oid, url)
    return 0


def text_of(fragment):
    """Inline HTML -> text: tags dropped, entities decoded, whitespace collapsed."""
    t = re.sub(r"<br\s*/?>", "\n", fragment)
    t = html.unescape(re.sub(r"<[^>]+>", "", t))
    return "\n".join(" ".join(line.split()) for line in t.split("\n")).strip()


class _Text(HTMLParser):
    """The catalog's description HTML as plain text: a blank line between blocks; one line per
    list item, '- ' for <ul> and 'N. ' for <ol>, indented two spaces per nesting level; <br> as a
    line break; table cells joined with ' | ', one row per line; <pre> kept byte-for-byte
    (indentation, blank lines and trailing spaces included)."""
    BLOCK = {"p", "div", "ul", "ol", "table", "blockquote",
             "h1", "h2", "h3", "h4", "h5", "h6", "hr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.pre, self.line_start = [], 0, False
        self.lists, self.pres, self.buf, self.first_cell, self.mark = [], [], [], False, ""
        self.anchors = []

    def _brk(self, s):
        self.out.append(s)

    def handle_starttag(self, tag, attrs):
        if self.pre and tag != "pre":
            return  # markup inside <pre> (e.g. <code>) adds nothing to the text
        if tag == "a":
            self.anchors.append((dict(attrs).get("href") or "", len(self.out)))
        elif tag == "pre":
            self.pre += 1
            if self.pre == 1:
                self.buf = []
        elif tag in ("ul", "ol"):
            self.lists.append([tag, 0])
            self._brk("\x00P")
        elif tag == "li":
            kind = self.lists[-1] if self.lists else ["ul", 0]
            kind[1] += 1
            indent = "\x05" * max(len(self.lists) - 1, 0)  # two spaces each, placed in text()
            # the marker waits for the item's first text, so a <p> inside the <li> cannot split
            # the marker from its words
            self.mark = indent + ("%d. " % kind[1] if kind[0] == "ol" else "- ")
            self._brk("\x00L")
        elif tag == "br":
            self._brk("\n")
            self.line_start = True
        elif tag == "tr":
            self._brk("\n")
            self.first_cell = True
        elif tag in ("td", "th"):
            if not self.first_cell:
                self.out.append("\x04")  # cell separator, tidied in text()
            self.first_cell = False
        elif tag in self.BLOCK:
            self._brk("\x00P")

    def handle_endtag(self, tag):
        if self.pre and tag != "pre":
            return
        if tag == "a":
            if self.anchors:
                href, start = self.anchors.pop()
                url = link_target(href)
                words = "".join(x for x in self.out[start:] if not x.startswith("\x00")).strip()
                if url and norm_url(url) not in norm_url(words):
                    # "the repo." -> "the repo (URL)." : the URL belongs to the words, not the stop
                    end = len(self.out) - 1
                    while end >= start and not self.out[end].strip():
                        end -= 1
                    m = re.search(r"[.,;:!?]+\s*$", self.out[end]) if end >= start else None
                    if m:
                        self.out[end] = self.out[end][:m.start()] + " (%s)" % url + self.out[end][m.start():]
                    else:
                        self.out.append(" (%s)" % url if words else url)
        elif tag == "pre":
            self.pre -= 1
            if self.pre == 0:
                self.pres.append("".join(self.buf).strip("\n"))
                self._brk("\x00P\x02%d\x03\x00P" % (len(self.pres) - 1))
        elif tag in ("ul", "ol"):
            if self.lists:
                self.lists.pop()
            self._brk("\x00P")
        elif tag == "li":
            self._brk("\x00E")
        elif tag in self.BLOCK:
            self._brk("\x00P")

    def handle_data(self, data):
        if self.pre:
            self.buf.append(data)
            return
        text = re.sub(r"\s+", " ", data)
        if self.line_start:  # the newline after a <br> is source formatting, not a space
            text = text.lstrip()
            self.line_start = not text
        if self.mark and text.strip():
            text, self.mark = self.mark + text.lstrip(), ""
        self.out.append(text)

    def text(self):
        s = "".join(self.out)
        item = r"(?=\n\x05*(?:- |\d+\. ))"
        s = re.sub(r"[ \t]*\x00E[ \t]*", "\x00E", s)
        # a <p> directly inside an <li> belongs to the item, not a new paragraph
        s = re.sub(r"(?:\s*\x00[PE])*\s*\x00L(?:\s*\x00P)*\s*", "\n", s)
        s = re.sub(r"\x00E(?:\s*\x00E)*", "\x00E", s)
        s = re.sub(r"\s*\x00E\s*" + item, "", s)
        s = re.sub(r"\s*(?:\x00[PE]\s*)+", "\n\n", s)
        s = re.sub(r"[ \t]*\x04[ \t]*", " | ", s)
        s = "\n".join(ln.strip() if " | " in ln and "\x02" not in ln else ln.rstrip()
                      for ln in s.split("\n"))
        s = re.sub(r"\n{3,}", "\n\n", s)
        s = s.strip().replace("\x05", "  ")  # nested-list indent, after whitespace clean-up
        # restore each <pre> block exactly as written
        return re.sub(r"\x02(\d+)\x03", lambda m: self.pres[int(m.group(1))], s)


def description_text(block):
    p = _Text()
    p.feed(block)
    p.close()
    return p.text()


ARCHIVER_MARK = re.compile(r"\s*\|\s*added by Archiver\b")
EMAIL = r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"
EMAIL_PAREN = re.compile(r"\s*\([^)]*" + EMAIL + r"[^)]*\)")
KNOWN_LABELS = {"Object ID", "Author", "Content", "Contents", "Microcontroller", "Microcontrollers",
                "Category", "Categories", "Licence", "Licences", "Language", "Languages", "Tag", "Tags"}
REQUIRED_LABELS = (("Object ID",), ("Author",), ("Content", "Contents"),
                   ("Microcontroller", "Microcontrollers"), ("Category", "Categories"),
                   ("Licence", "Licences"))


def author_name(raw):
    """The catalog's Author text without OBEX's archive marker or a contact email.

    "| added by Archiver" is OBEX bookkeeping for objects moved from the old OBEX, not part of the
    name. An author line can carry a personal email in parentheses; a KB answer has no use for it,
    so the parenthetical is dropped (Stephen reviews this rule with F-573). Only a parenthetical
    holding an email address goes; any other text is kept. An email outside parentheses is left
    for the reviewer -- run() reports it as a problem rather than guess where the name ends."""
    return EMAIL_PAREN.sub("", ARCHIVER_MARK.sub("", raw)).strip()


def parse(page_html):
    """Return the catalog fields, or None when the field list is not on the page. A page whose
    field list has an unknown label, lacks a required one, or has an Object ID line without a
    YYYY-MM-DD date comes back with `problems` set; run() then leaves its YAML untouched rather
    than write an empty value over a real one."""
    ul = re.search(r'<ul id="obexinformation"[^>]*>(.*?)</ul>', page_html, re.S)
    if not ul:
        return None
    fields, problems = {}, []
    for li in re.findall(r"<li\b[^>]*>(.*?)</li>", ul.group(1), re.S):
        m = re.match(r"\s*([^:]+?)\s*:\s*(.*)$", text_of(li), re.S)
        if not m:
            problems.append("field line without a label: %r" % text_of(li)[:60])
            continue
        label = m.group(1)
        if label not in KNOWN_LABELS:
            problems.append("unknown field label %r" % label)
        links = [x for x in (text_of(a) for a in re.findall(r"<a\b[^>]*>(.*?)</a>", li, re.S)) if x]
        fields[label] = (m.group(2).strip(), links)
    for alternatives in REQUIRED_LABELS:
        if not any(a in fields for a in alternatives):
            problems.append("no %s field" % alternatives[0])
    out = {"problems": problems}
    oid = fields.get("Object ID", ("", []))[0]
    m = re.match(r"(\d+)\s*\((\d{4}-\d{2}-\d{2})", oid)
    out["object_id"] = m.group(1) if m else oid.split()[0] if oid else ""
    out["created_date"] = m.group(2) if m else ""
    if not m:
        problems.append("Object ID line has no YYYY-MM-DD date: %r" % oid)
    out["author"] = author_name(fields.get("Author", ("", []))[0])
    if re.search(EMAIL, out["author"]):
        problems.append("author line still holds an email address: %r" % out["author"])
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
        out[key] = (v[1] or ([v[0]] if v[0] else [])) if v else []  # an empty field is [], never ['']
    tags = field("Tag")
    out["tags"] = (tags[1] or [t.strip() for t in tags[0].split(",") if t.strip()]) if tags else []
    t = re.search(r"<title>(.*?)</title>", page_html, re.S)
    out["title"] = TITLE_SUFFIX.sub("", text_of(t.group(1))) if t else ""
    d = re.search(r'<div class="markdown-content">(.*?)</div>\s*<hr', page_html, re.S)
    out["description"] = description_text(d.group(1)) if d else ""
    out["download"] = download_link(page_html, out["object_id"], problems)
    return out


def download_link(page_html, oid, problems):
    """The page's ZIP download, or "" when OBEX offers none.

    A page shows its download in one of three ways (checked 2026-10-12 against OBEX):
      - a "Zip archive download" button -> its link;
      - only a folder browser ("Download folder") -> OBEX's ZIP link for the object, which serves
        the same folder as one ZIP (it redirects to the folder's file; 2822, 4800, 4883);
      - "There are no downloads available for this object." -> none: the ZIP link answers
        "invalid!" (4442, 4571, 4581, 4616, 4617 point the reader to GitHub in the description).
    Anything else is a page shape we have not seen: reported, YAML left untouched."""
    dl = sorted(set(re.findall(r'href="([^"]*action=download_obex_zip[^"]*)"', page_html)))
    if len(dl) == 1:
        return urllib.parse.urljoin(OBEX_SITE, html.unescape(dl[0]))
    if len(dl) > 1:
        problems.append("%d ZIP download links on the page" % len(dl))
    elif "There are no downloads available for this object" in page_html:
        return ""
    elif "all-files-to-zip" in page_html:
        return OBEX_SITE + ZIP_LINK % oid
    else:
        problems.append("no download section of a known shape")
    return ""


def one(v):
    """A single catalog value stays a string; several stay a list."""
    return v[0] if len(v) == 1 else v


def mirrored(om, cat):
    """The whole object as the catalog gives it -- the only shape an object YAML has.

    Every field is the catalog's, except two that are not catalog fields but are kept: the
    object's own page URL (how we found it) and description_short, the authored one-liner
    (F-573). Nothing of ours rides beside them -- no classification, no compatibility, no scraper
    bookkeeping, no placeholder (Stephen, 2026-10-12: "pure mirror")."""
    fn = om.get("functionality") or {}
    md = om.get("metadata") or {}

    def got(new, old):
        # Title, author, description and date are never blanked: a page without them is a parse
        # problem, reported in run(). Every other field the page leaves empty is written empty --
        # keeping our old value would present our own classification as the catalog's.
        return new if new not in ("", None) else (old or "")

    urls = {"obex_page": om["urls"]["obex_page"]}
    if cat["download"]:  # no key at all when OBEX offers no download -- never a dead link
        urls["download_direct"] = cat["download"]
    return {
        "object_id": str(om["object_id"]),
        "title": got(cat["title"], om.get("title")),
        "author": got(cat["author"], om.get("author")),
        "functionality": {
            "category": one(cat["category"]) if cat["category"] else "",
            "tags": cat["tags"],
            "description_short": fn.get("description_short", ""),
            "description_full": got(cat["description"], fn.get("description_full")),
        },
        "technical_details": {
            "content_type": cat["content_type"],
            "microcontroller": cat["microcontroller"],
            "languages": cat["languages"],
            "licence": one(cat["licence"]) if cat["licence"] else "",
        },
        "metadata": {"created_date": got(cat["created_date"], md.get("created_date"))},
        "urls": urls,
    }


def flat(d, prefix=""):
    out = {}
    for k, v in d.items():
        p = prefix + "." + k if prefix else k
        if isinstance(v, dict) and v:
            out.update(flat(v, p))
        else:
            out[p] = v
    return out


def planned(om, new):
    """(field, old, new) for every value that changes; a removed field has new = REMOVED."""
    a, b = flat(om), flat(new)
    return [(k, a.get(k, "ABSENT"), b.get(k, "REMOVED"))
            for k in list(a) + [k for k in b if k not in a] if a.get(k, "ABSENT") != b.get(k, "REMOVED")]


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
        if cat["problems"]:  # leave the YAML untouched: never blank a value on a shape we don't know
            problems.extend((oid, p + " (YAML left untouched)") for p in cat["problems"])
            continue
        if not cat["description"]:
            problems.append((oid, "no description on page (other fields still mirrored)"))
        with open(f) as fh:
            data = yaml.safe_load(fh)
        om = data["object_metadata"]
        new = mirrored(om, cat)
        diffs = planned(om, new)
        if diffs:
            changes[oid] = [{"field": p, "old": o, "new": n} for p, o, n in diffs]
        out = yaml.dump({"object_metadata": new}, sort_keys=False, allow_unicode=True,
                        default_flow_style=False)
        with open(f) as fh:
            current = fh.read()
        if write and out != current:  # also lays out a file whose values already match
            tmp = f + ".tmp"
            with open(tmp, "w") as fh:  # write whole, then swap in: an interrupt leaves the original
                fh.write(out)
            os.replace(tmp, f)
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
    ap.add_argument("mode", choices=("discover", "add", "fetch", "report", "apply"))
    ap.add_argument("--pages", required=True)
    ap.add_argument("--json")
    ap.add_argument("--url", help="add: the new object's OBEX page URL, as discover printed it")
    a = ap.parse_args()
    if a.mode == "discover":
        return discover(a.pages)
    if a.mode == "add":
        if not a.url:
            ap.error("add needs --url")
        return add(a.url, a.pages)
    if a.mode == "fetch":
        fetch(a.pages)
        return 0
    return run(a.pages, write=(a.mode == "apply"), json_out=a.json)


if __name__ == "__main__":
    sys.exit(main())
