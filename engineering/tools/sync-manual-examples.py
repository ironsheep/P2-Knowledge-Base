#!/usr/bin/env python3
"""
sync-manual-examples.py — generate example-file headers, and keep the file body
byte-identical to the manual's printed code block.

WHY THIS EXISTS
---------------
`central:spin2-authoring-guide` requires every .spin2 to carry a file header
(§4.2) and a licence footer (§4.2.1). A manual's example corpus could not
satisfy that, because each file must also be byte-identical to the listing
printed in the manual, and ~20 lines of boilerplate cannot appear in a teaching
code block. The two gates were individually satisfiable and jointly impossible,
so the whole fleet quietly ran without headers (93 files, 13 documents).

The resolution is to stop hand-maintaining the thing that conflicts. The FILE is
the source of truth; its header is GENERATED from what the repo already knows,
and the manual's block holds the BODY only. Identity is then asserted between
the block and the file's body, which is the promise readers were always given:
the code you read is the code that builds.

Deriving the header is also what makes `Appears in.` maintainable. It is read
back out of the heading that encloses the matched block, so renumbering a
manual's chapters costs nothing -- the next sync absorbs it. A hand-typed
location would have been stale the moment chapters moved, which is exactly what
happened to this manual on 2026-08-18.

PAIRING
-------
Same convention as verify-example-corpus-identity.py: a file is paired to its
block by the fence caption, ```{.spin2 caption="<name>.spin2"}.

ADOPTION IS PER-DOCUMENT
------------------------
A document is "adopted" once its files carry generated headers. Un-adopted
documents are left exactly as they are -- this tool never rewrites a file that
has no generated header unless --adopt is passed. That is what lets the fleet
move one release at a time instead of churning 12 published corpora at once.

USAGE
    sync-manual-examples.py --doc DIR [--check] [--adopt]

    --doc DIR   Document dir containing opus-master/ and examples-library/.
    --check     Verify only; write nothing. Exit 1 if anything is out of sync.
                This is the release/prepare gate.
    --adopt     Add generated headers to a document that has none yet.
                Requires each file to already carry a Purpose line (see below).

PURPOSE IS THE ONE HUMAN FIELD
    Everything else is derived. On adoption, provide it either as an existing
    "Purpose...." line in a file's header, or via examples-library/PURPOSES.md
    as "<filename>: <one-line purpose>". The tool refuses to invent one.

Exit: 0 clean / 1 out of sync or missing input / 2 usage error.
"""

import argparse
import re
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

MARK_BEGIN = "'' ==========================================================================="
# Adoption is detected by this exact sentence, never by the banner rule: other
# hand-written headers in the fleet open with their own '' ==== banner (e.g.
# P2AN006's isp_stack_check.spin2, a shipped utility object, not an example),
# and a prefix match on the banner pulls un-adopted documents into checks they
# should not face.
ADOPT_SENTINEL = "This file is an EXAMPLE from the manual above."
AUTHORS = "Iron Sheep Productions, LLC"
EMAIL = "stephen@ironsheep.biz"

# The repo is dual-licensed: MIT for code, CC BY-SA 4.0 for the documents.
# An example is CODE. It must not claim the manual's terms.
LICENSE_FOOTER = """{{
 ---------------------------------------------------------------------------
  MIT License -- Copyright (c) @YEAR@ Iron Sheep Productions, LLC

  Permission is hereby granted, free of charge, to any person obtaining a
  copy of this software and associated documentation files (the "Software"),
  to deal in the Software without restriction, including without limitation
  the rights to use, copy, modify, merge, publish, distribute, sublicense,
  and/or sell copies of the Software, and to permit persons to whom the
  Software is furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED. See the repository LICENSE file for the full text.
 ---------------------------------------------------------------------------
}}"""


# Derived fields come from Markdown, which legitimately uses typographic
# punctuation; the header they land in is .spin2 source, where guide §1.1
# forbids every codepoint above 127. Transliterate what has an ASCII meaning
# and refuse the rest -- a derived field cannot be policed by hand.
ASCII_MAP = {
    "\u2014": " - ", "\u2013": "-", "\u2018": "'", "\u2019": "'",
    "\u201c": '"', "\u201d": '"', "\u2026": "...", "\u00a0": " ",
    "\u00b7": "-", "\u2192": "->", "\u2264": "<=", "\u2265": ">=",
    "\u00d7": "x", "\u00a7": "sec ", "\u2212": "-",
}


def asciify(text):
    for k, v in ASCII_MAP.items():
        text = text.replace(k, v)
    return re.sub(r"\s{2,}", " ", text).strip()


class GitUnavailable(RuntimeError):
    """git could not be RUN. Distinct from git running and having no answer."""


def git(*args, default=""):
    """Run a git query. A git that CANNOT RUN is a hard error, not a default.

    WHY THIS IS NOT A try/except-return-default (learned the expensive way,
    2026-08-22). Every header field below `Purpose` is DERIVED from git --
    Started, Updated, the licence year. The previous form swallowed every
    exception and substituted the default, which conflated two situations that
    must never be conflated:

      git ran, and has no answer   -> legitimate. A never-committed file has no
                                      first-commit date. `default` is correct.
      git could not run at all     -> the environment is broken. `default` is a
                                      LIE, and it gets written into the file.

    In this devcontainer git intermittently fails with "dubious ownership", so
    the second case is real, not theoretical. Observed consequence: `--check`
    reported the ONE adopted document RED six times, then GREEN twelve times,
    with nothing on disk changing -- reproduced deterministically by stubbing
    git to exit 128. The verdict of a release gate depended on whether git
    happened to work that second.

    The unshipped half is worse. Under `--adopt` the same substitution would
    have written `Started.... unknown` / `Updated.... unknown` into the header
    of every file it touched -- 88 files across 11 documents were queued for
    exactly that sweep -- and the next run, with git working, would have called
    them all out of sync.

    So: raise. A caller that genuinely wants a fallback can catch it.
    """
    # Declare THIS repo safe for the duration of the call, via environment
    # rather than a config file. Not a workaround hiding a risk: the ownership
    # genuinely matches (checked 2026-08-22 -- repo, .git and the running user
    # are all vscode:vscode), the "dubious ownership" refusal comes from the
    # sandbox wrapper, and ~/.gitconfig is not writable here to fix it the usual
    # way. GIT_CONFIG_COUNT/KEY/VALUE is git's own supported no-file mechanism,
    # so this asserts something true and leaves the user's config untouched.
    env = dict(os.environ)
    n0 = int(env.get("GIT_CONFIG_COUNT", "0"))
    env["GIT_CONFIG_COUNT"] = str(n0 + 1)
    env[f"GIT_CONFIG_KEY_{n0}"] = "safe.directory"
    env[f"GIT_CONFIG_VALUE_{n0}"] = str(REPO)
    try:
        out = subprocess.run(["git", "-C", str(REPO), *args],
                             capture_output=True, text=True, env=env)
    except OSError as e:                      # git missing / not executable
        raise GitUnavailable(f"cannot execute git: {e}") from e
    if out.returncode != 0:
        raise GitUnavailable(
            f"git {' '.join(args)} exited {out.returncode}: "
            f"{(out.stderr or '').strip()}")
    # Ran fine and simply had nothing to say -- THAT is what `default` is for.
    return out.stdout.strip() or default


def blocks_with_context(md: Path):
    """Yield (caption, body_text, enclosing_heading) per captioned fence.

    The enclosing heading is the nearest preceding '## N.M Title' (falling back
    to '# Chapter N: Title'), with its {#anchor} stripped. This is what makes
    the header's 'Appears in.' line free to maintain.
    """
    lines = md.read_text(encoding="utf-8").split("\n")
    heading = ""
    chapter = ""
    i, n = 0, len(lines)
    while i < n:
        ln = lines[i]
        if re.match(r"^# (Chapter|Appendix) ", ln):
            chapter = re.sub(r"\s*\{#[^}]*\}\s*$", "", ln[2:]).strip()
            heading = ""
        elif ln.startswith("## "):
            heading = re.sub(r"\s*\{#[^}]*\}\s*$", "", ln[3:]).strip()
        s = ln.strip()
        if s.startswith("```") and 'caption="' in s and ".spin2" in s:
            a = s.index('caption="') + len('caption="')
            cap = s[a:s.index('"', a)]
            body, j = [], i + 1
            while j < n and lines[j].strip() != "```":
                body.append(lines[j]); j += 1
            where = chapter + (" -- " + heading if heading else "")
            yield cap, "\n".join(body) + "\n", where
            i = j + 1
        else:
            i += 1


def split_file(text):
    """Return (header_or_None, body, footer_or_None) for an example file."""
    header = None
    if ADOPT_SENTINEL in text and text.startswith(MARK_BEGIN):
        end = text.find(MARK_BEGIN, len(MARK_BEGIN))
        if end != -1:
            cut = text.index("\n", end + len(MARK_BEGIN)) + 1
            header, text = text[:cut], text[cut:]
            text = text.lstrip("\n")
    footer = None
    m = re.search(r"\n\{\{\n(?:.|\n)*?\n\}\}\s*$", text)
    if m:
        footer, text = text[m.start():].strip("\n"), text[:m.start()]
    return header, text.rstrip("\n") + "\n", footer


def existing_purpose(header):
    if not header:
        return None
    got = []
    for ln in header.split("\n"):
        m = re.match(r"''\s+Purpose\.+\s*(.*)$", ln)
        if m:
            got.append(m.group(1).strip()); continue
        if got and re.match(r"''\s{15,}\S", ln) and "...." not in ln:
            got.append(ln.strip("' ").strip())
        elif got:
            break
    return " ".join(x for x in got if x) or None


def wrap(label, text, width=74):
    text = asciify(text)
    """'   Label..... text' with continuation lines aligned under the text."""
    lead = f"''   {label}"
    pad = " " * len(lead[2:])
    words, out, cur = text.split(), [], lead + " "
    for w in words:
        if len(cur) + len(w) > width and cur.strip() != lead.strip():
            out.append(cur.rstrip()); cur = "''" + pad + " " + w + " "
        else:
            cur += w + " "
    out.append(cur.rstrip())
    return "\n".join(out)


def build_header(fname, purpose, doc_title, version, where, started, updated):
    L = [MARK_BEGIN, "''"]
    L.append(wrap("File....... ", fname))
    L.append(wrap("Purpose.... ", purpose))
    L.append(wrap("Manual..... ", doc_title))
    if version:
        L.append(wrap("Version.... ", version))
    if where:
        L.append(wrap("Appears in. ", where))
    L.append(wrap("Authors.... ", AUTHORS))
    L.append(wrap("E-mail..... ", EMAIL))
    L.append(wrap("Started.... ", started))
    L.append(wrap("Updated.... ", updated))
    # Reader-facing only. The header is shipped in the src ZIP, so it carries
    # what serves the person who opens the file and nothing that serves us --
    # no generated-by banner, no do-not-edit warning. Drift is caught by
    # `sync-manual-examples.py --check` in the release gate, which is a stronger
    # guarantee than a comment asking politely.
    L += ["''",
          f"''   {ADOPT_SENTINEL} Everything below",
          "''   this header is byte-identical to the listing printed there --",
          "''   what you read in the manual is what builds here.",
          "''", MARK_BEGIN, ""]
    return "\n".join(L)


def doc_meta(doc: Path):
    """(title, version) for the document. CHANGELOG.md lives under opus-master/
    in this fleet, with the doc root as a fallback."""
    title, version = doc.name, ""
    for ch in (doc / "opus-master" / "CHANGELOG.md", doc / "CHANGELOG.md"):
        if not ch.is_file():
            continue
        txt = ch.read_text(encoding="utf-8")
        m = re.search(r"^#\s+(.+?)[\s\-\u2013\u2014]*[Cc]hangelog\s*$", txt, re.M)
        if m:
            title = m.group(1).strip(" -")
        v = re.search(r"^##\s*\[?v?(\d+\.\d+\.\d+)\]?\s*(?:\(([^)]*)\))?", txt, re.M)
        if v:
            version = "v" + v.group(1)
            if v.group(2):
                version += " (%s)" % v.group(2).strip()
        break
    return title, version


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("USAGE")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--doc", required=True)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--adopt", action="store_true")
    a = ap.parse_args()

    doc = Path(a.doc).resolve()
    opus, lib = doc / "opus-master", doc / "examples-library"
    if not opus.is_dir():
        print(f"ERROR: no opus-master/ under {doc}", file=sys.stderr); return 2
    if not lib.is_dir():
        print(f"GREEN: {doc.name} has no examples-library/ — nothing to sync."); return 0

    blocks = {}
    for md in sorted(opus.rglob("*.md")):
        for cap, body, where in blocks_with_context(md):
            blocks[cap] = (body, where)

    purposes = {}
    pf = lib / "PURPOSES.md"
    if pf.is_file():
        for ln in pf.read_text(encoding="utf-8").split("\n"):
            m = re.match(r"^\s*[-*]?\s*`?([\w.\-]+\.spin2)`?\s*[:—-]\s*(.+?)\s*$", ln)
            if m:
                purposes[m.group(1)] = m.group(2)

    title, version = doc_meta(doc)
    files = sorted(lib.glob("*.spin2"))
    if not files:
        print(f"GREEN: {doc.name} has no example files."); return 0

    adopted = any(ADOPT_SENTINEL in f.read_text(encoding="utf-8") for f in files)
    if not adopted and not a.adopt:
        print(f"INFO: {doc.name} has not adopted generated headers "
              f"({len(files)} files) — whole-file identity still gated by "
              f"verify-example-corpus-identity.py. Pass --adopt to adopt.")
        return 0

    problems, wrote = [], 0
    for f in files:
        raw = f.read_text(encoding="utf-8")
        header, body, footer = split_file(raw)
        if f.name not in blocks:
            problems.append(f"{f.name}: no captioned block in opus-master"); continue
        blk_body, where = blocks[f.name]

        if body != blk_body:
            problems.append(f"{f.name}: BODY differs from its printed code block")

        purpose = existing_purpose(header) or purposes.get(f.name)
        if purpose and not purpose.isascii():
            bad = sorted({c for c in purpose if not c.isascii()})
            problems.append(f"{f.name}: Purpose contains non-ASCII {bad} — the "
                            f"header is .spin2 source and guide §1.1 is absolute")
            continue
        if not purpose:
            problems.append(f"{f.name}: no Purpose — add a Purpose line or a "
                            f"PURPOSES.md entry (the tool will not invent one)")
            continue

        # Match on basename: a `git mv` changes the path but never the name, and
        # --follow cannot trace a rename that is not committed yet.
        hist = git("log", "--diff-filter=A", "--format=%ad", "--date=format:%b %Y",
                   "--", f"*/{f.name}", default="")
        started = hist.split("\n")[-1] if hist else "Aug 2026"
        # Month granularity on purpose. A day-precise mtime would advance every
        # time the header itself was regenerated and committed, so the tool
        # would not be idempotent across a commit; a month changes rarely and
        # only when the body actually changed in a new month.
        updated = git("log", "-1", "--format=%ad", "--date=format:%b %Y",
                      "--", f"*/{f.name}", default="") or started
        new = build_header(f.name, purpose, title, version, where,
                           started or "unknown", updated or "unknown")
        if not new.isascii():
            bad = sorted({c for c in new if not c.isascii()})
            problems.append(f"{f.name}: generated header holds non-ASCII {bad} "
                            f"— extend ASCII_MAP"); continue
        year = git("log", "-1", "--format=%ad", "--date=format:%Y", default="2026")
        out = new + "\n" + blk_body.rstrip("\n") + "\n\n" + LICENSE_FOOTER.replace("@YEAR@", year) + "\n"
        if out != raw:
            if a.check:
                problems.append(f"{f.name}: header/footer out of sync")
            else:
                f.write_text(out, encoding="utf-8"); wrote += 1

    for p in problems:
        print(f"  FAIL  {p}")
    if problems:
        print(f"RED: {doc.name} — {len(problems)} problem(s)."); return 1
    verb = "verified" if a.check else f"synced ({wrote} rewritten)"
    print(f"GREEN: {doc.name} — {len(files)} example(s) {verb}.")
    return 0


if __name__ == "__main__":
    # A broken git must stop the run with an explanation, never degrade into a
    # verdict. Exit 2 = "could not determine", distinct from 1 = "out of sync".
    try:
        sys.exit(main())
    except GitUnavailable as e:
        print(f"ERROR: {e}")
        print("  Every derived header field (Started / Updated / licence year) "
              "comes from git,")
        print("  so this tool cannot report a verdict while git is failing -- "
              "and MUST NOT")
        print("  write a header built from placeholder values. Fix git, re-run.")
        sys.exit(2)
