#!/usr/bin/env python3
"""
audit-spin2-ascii.py - enforce spin2-authoring-guide Sec 1.1 on AUTHORED .spin2 source.

WHY THIS EXISTS
    `pnut-ts` is an ASCII-only compiler. A non-ASCII character in code, a string
    or a signature causes silent corruption or a compile error -- and the guide
    forbids the punctuation set (em dash, en dash, curly quotes, ellipsis) in
    COMMENTS too, because those are the characters an editor or a paste silently
    substitutes.

    Until this script existed the rule was documented at strength `gate` with no
    instrument behind it, which the guide itself calls out: "conform to the style
    guide" with nothing enforcing it "degrades into reading it and hoping." A
    clean `pnut-ts` compile proves legality only -- it has never proven style, and
    an em dash inside a comment compiles perfectly.

WHAT IT ENFORCES (Sec 1.1, exactly as the guide states it)
    Any codepoint above 127 is a FAIL, wherever it appears, EXCEPT the two
    box-drawing ranges the guide explicitly preserves:

        U+2500-U+257F  box drawing
        U+2580-U+259F  block elements

    That exception is ecosystem compatibility, not decoration: those characters
    ship with the Propeller Tool and a large part of the published P1/P2 code base
    draws diagrams with them. The guide says do not propose removing it. They are
    permitted ONLY inside comments; in code they are a FAIL like anything else.

SCOPE -- authored source only, and the exclusions are printed by name
    The repo holds ~2400 .spin2 files and we WROTE a small fraction of them.
    Restyling the rest would be both wrong and meaningless, so the default roots
    are the trees this project actually authors:

        manuals/<slug>/examples-library/         shipped to readers in a .zip
        manuals/<slug>/audit/verification-tests/ the hardware-rig source
        manuals/<slug>/figure-generators/        authored to produce figures
        app-notes/<n>/examples-library/          same contract as a manual's

    Deliberately NOT audited, and why:
        code-validation/   extracted FROM the manuals by a script, then compiled;
                           regenerated on demand, never hand-edited
        REF/ REF-NO-COMMIT/ NO-COMMIT/  third-party or vendor reference material
        engineering/ingestion/          ingested sources -- not ours to restyle
        OBEX/                           community objects, published as received
        archive/ .backups/              frozen records
        extracted_examples/             lifted out of PDFs by tooling

FURTHER T1 RULES -- ADVISORY unless armed  («#360», 2026-09-26)
    The instrument also runs the other script-checkable rules of the guide
    (the list is printed every run under T1 COVERAGE, by Sec number, with the
    rules it does NOT check and why). Every one of them only REPORTS: none
    changes the exit status unless named in --blocking, which arms a chosen
    set for one run -- so a rule can block for one manual's code while the
    fleet stays advisory. Measure a rule's population before arming it.

USAGE
    audit-spin2-ascii.py [--quiet] [--list-files] [--show-all]
                         [--blocking SEC[,SEC...]] [<path> ...]

    With no path, audits the default roots above. A path may be a file or a
    directory (searched recursively).

    --show-all   print every advisory site, not the first 15 per rule
    --blocking   arm rules for this run, e.g. `--blocking 3.2,5.2,5.3 <dir>`;
                 an armed rule prints every site even under --quiet

EXIT STATUS
    0  every audited file is conformant (Sec 1.1, plus any armed rule)
    1  one or more violations (gate failure)
    2  usage error (includes an unknown rule named in --blocking)

FIX
    Replace with the ASCII form the guide names: `-` for an em or en dash, `'`
    and `"` for curly quotes, `...` for an ellipsis. If the character is carrying
    meaning that ASCII cannot (a real diagram), use the box-drawing ranges, which
    are permitted in comments.
"""

import argparse
import bisect
import pathlib
import re
import sys
import unicodedata

# The two ranges Sec 1.1 preserves, permitted in COMMENTS only.
BOX_RANGES = [(0x2500, 0x257F), (0x2580, 0x259F)]

# The substitutions an editor makes silently, with the replacement the guide names.
SUGGEST = {
    0x2014: "-",    0x2013: "-",    0x2012: "-",   0x2010: "-",   0x2011: "-",
    0x2018: "'",    0x2019: "'",    0x201A: "'",   0x201B: "'",
    0x201C: '"',    0x201D: '"',    0x201E: '"',   0x201F: '"',
    0x2026: "...",  0x2212: "-",    0x00A0: " ",   0x2007: " ",   0x202F: " ",
    0x00D7: "*",    0x00F7: "/",    0x2192: "->",  0x2190: "<-",  0x21D2: "=>",
    0x00B0: " deg", 0x00B5: "u",    0x03BC: "u",   0x2264: "<=",  0x2265: ">=",
    0x2260: "<>",   0x00B1: "+/-",  0x2022: "*",   0x00AB: '"',   0x00BB: '"',
}

DEFAULT_GLOBS = [
    "engineering/document-production/manuals/*/examples-library/**/*.spin2",
    "engineering/document-production/manuals/*/audit/verification-tests/**/*.spin2",
    "engineering/document-production/manuals/*/figure-generators/**/*.spin2",
    "engineering/document-production/app-notes/*/examples-library/**/*.spin2",
]

# A path containing any of these is never audited, whatever root reached it.
EXCLUDE_PARTS = ("/archive/", "/.backups/", "/REF/", "/REF-NO-COMMIT/",
                 "/NO-COMMIT/", "/code-validation/", "/extracted_examples/")


def in_box_range(cp):
    return any(lo <= cp <= hi for lo, hi in BOX_RANGES)


CODE, COMMENT, STRING, DEBUG_STRING = 0, 1, 2, 3

CONTEXT_NAME = {
    CODE:         "in CODE",
    COMMENT:      "in a comment",
    STRING:       "in a STRING LITERAL",
    DEBUG_STRING: "in a DEBUG() STRING",
}

# Why the context matters, and why a clean compile does not settle it.
#
#   DEBUG_STRING  the byte goes out the debug link at RUNTIME. A codepoint above
#                 127 arrives as multi-byte UTF-8, so the terminal can take the
#                 stream as BINARY rather than ASCII, mis-render, or act on an
#                 escape it was never sent. The expected output is destroyed and
#                 nothing in the build says so.
#   STRING        same class wherever the string is finally emitted.
#   CODE          identifier / operator position: the compiler's problem.
#   COMMENT       never reaches the P2; the cost is the reader's own editor, and
#                 byte-identity with the printed block in the manual.
#
# `pnut-ts` exiting 0 proves NONE of the first three are harmless -- it proves the
# file parsed. Severity is a runtime property, so the report states the context
# and lets the reader weigh it.
CONTEXT_SEVERITY = {
    DEBUG_STRING: "RUNTIME - corrupts debug output / terminal state",
    STRING:       "RUNTIME - corrupts emitted text",
    CODE:         "COMPILE / semantics",
    COMMENT:      "portability - reader's editor + printed-block identity",
}


def context_mask(text):
    """Per-character context code for the WHOLE file (CODE/COMMENT/STRING/DEBUG_STRING).

    Spin2 comments come in two shapes and only one of them is line-bounded:
        '  ''        to end of line
        { } {{ }}    BRACE form -- nests, and SPANS LINES

    The brace form is the one that matters here: a box-drawing diagram is almost
    always a multi-line { } block, which is exactly the shape the guide's own
    example uses. A single-line approximation rejected every such diagram --
    caught by the negative control, not by reading the code.

    Strings are tracked so a brace inside "..." cannot open a phantom comment --
    and so a non-ASCII byte inside one can be reported as the runtime defect it is
    rather than lumped in with comment prose.

    A string counts as a DEBUG string when it sits inside a `debug(...)` call.
    `debug()` cannot be continued across lines, so its span is found per line.
    """
    mask = bytearray(len(text))     # default CODE (0)
    debug_spans = []
    pos = 0
    for line in text.splitlines(keepends=True):
        low = line.lower()
        k = 0
        while True:
            k = low.find("debug", k)
            if k < 0:
                break
            j = k + 5
            while j < len(line) and line[j] in " \t":
                j += 1
            # `debug(` or `debug[n](` both count
            if j < len(line) and line[j] in "([":
                depth, m = 0, j
                while m < len(line):
                    if line[m] in "([":
                        depth += 1
                    elif line[m] in ")]":
                        depth -= 1
                        if depth == 0:
                            break
                    m += 1
                debug_spans.append((pos + k, pos + min(m + 1, len(line))))
            k += 5
        pos += len(line)

    def in_debug(idx):
        return any(lo <= idx < hi for lo, hi in debug_spans)

    i, n = 0, len(text)
    depth = 0                       # brace-comment nesting depth
    while i < n:
        ch = text[i]
        if depth:
            mask[i] = COMMENT
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            i += 1
            continue
        if ch == "'":               # line comment, to end of line
            j = text.find("\n", i)
            j = n if j < 0 else j
            for k in range(i, j):
                mask[k] = COMMENT
            i = j
            continue
        if ch == "{":
            depth = 1
            mask[i] = COMMENT
            i += 1
            continue
        if ch == '"':               # string literal -- single line in Spin2
            kind = DEBUG_STRING if in_debug(i) else STRING
            j = i + 1
            while j < n and text[j] != '"' and text[j] != "\n":
                mask[j] = kind
                j += 1
            mask[i] = kind
            if j < n and text[j] == '"':
                mask[j] = kind
                i = j + 1
            else:
                i = j
            continue
        i += 1

    # INSIDE debug(...) NOTHING IS A COMMENT ({{USER_NAME}}, 2026-08-22).
    # Everything between the parens is payload bound for the debug link, so text
    # that merely LOOKS like commentary is transmitted, not stripped. Marking the
    # whole span DEBUG_STRING does two things at once: it raises the severity to
    # runtime, and it withdraws the box-drawing exception there -- a diagram is
    # fine in a comment and is multi-byte UTF-8 down the wire in a debug().
    for lo, hi in debug_spans:
        for idx in range(lo, min(hi, n)):
            mask[idx] = DEBUG_STRING
    return mask


# ---------------------------------------------------------------------------
# Sec 2.1 -- No single-letter variable names.  ADVISORY, not blocking.  («#217»)
#
# WHY ADVISORY AND NOT A GATE.  Measured 2026-09-21 before arming: **168
# single-letter identifiers across 79 of 145 audited files**, and 77 of those
# sit in `examples-library/` -- a tree whose files are BYTE-IDENTICAL to the
# code blocks printed in released PDFs (the identity gate asserts it). Arming
# this as blocking would therefore either break that identity or force renames
# inside published manual pages. That is a scope decision Stephen owns, not one
# an instrument makes for him, so the check REPORTS and the exit code ignores it
# until he rules.
#
# The guide's own exceptions need no code: PASM2 register names (`pa`, `pb`,
# `ptra`), type-prefixed shorts (`pStr`, `pBuf`) and `idx` are all longer than
# one character, so "length == 1" is the whole mechanical rule.
#
# This project also carries a recorded carve-out (`skill-conventions.md`): Sec 2.1
# yields to cross-chapter continuity where a later chapter grows an earlier
# chapter's program. A file may declare that with a waiver comment:
#     ' {spin2-2.1-waiver: <reason>}
SIG_RE = re.compile(
    r"^(PUB|PRI)\s+(\w+)\s*\(([^)]*)\)\s*(?::\s*([^|]*))?\s*(?:\|(.*))?$")
WAIVER_RE = re.compile(r"\{spin2-2\.1-waiver:", re.IGNORECASE)


def audit_single_letter_names(path: pathlib.Path):
    """Return [(lineno, name, signature)] for Sec 2.1. Advisory."""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    if WAIVER_RE.search(text):
        return []
    out = []
    for lineno, line in enumerate(text.splitlines(), 1):
        m = SIG_RE.match(line.strip())
        if not m:
            continue
        names = []
        for grp in (m.group(3), m.group(4), m.group(5)):
            if grp:
                names += [n.strip() for n in grp.split(",")]
        for n in names:
            n = n.split("[")[0].strip()
            if len(n) == 1 and n.isalpha():
                out.append((lineno, n, line.strip()[:88]))
    return out


# ---------------------------------------------------------------------------
# FURTHER T1 RULES -- every one ADVISORY until armed.  («#360», 2026-09-26)
#
# Each rule below REPORTS. None touches the exit status unless it is named in
# `--blocking`, which lets a rule be armed for one scope (a manual's rigs) while
# the fleet stays advisory. The Sec 2.1 lesson holds for every one of them:
# measure the population first, arm after, and let the owner rule on scope.
#
# PRECISION OVER RECALL. A detector that flags legitimate code trains its reader
# to ignore it, so every heuristic here errs toward silence, and each one says
# in its docstring what it does NOT see.
#
# They share one reading of the file, the SPIN VIEW: live source with comments
# and string-literal contents blanked to spaces, columns preserved, built from
# context_mask. The one wrinkle is debug(): context_mask marks a whole debug(...)
# span DEBUG_STRING for Sec 1.1's sake, but the names passed to it are real USES
# -- udec_(slotIdx) reads slotIdx -- so the spin view restores a live span's
# payload and blanks only its "..." literals. A debug span that sits inside a
# comment stays blank.

BLOCK_RE = re.compile(r"^(CON|VAR|OBJ|DAT|PUB|PRI)(?![\w])", re.IGNORECASE)
IDENT_RE = re.compile(r"[A-Za-z_]\w*")
METHOD_SIG_RE = re.compile(
    r"^(PUB|PRI)\s+(\w+)\s*\(([^)]*)\)\s*(?::([^|]*))?\s*(?:\|(.*))?\s*$",
    re.IGNORECASE | re.DOTALL)
VERSION_DIRECTIVE_RE = re.compile(r"^\{Spin2_v\d+\}", re.IGNORECASE)
RETURN_RE = re.compile(r"\breturn\b", re.IGNORECASE)
RETURN_EXPR_RE = re.compile(r"\breturn\b\s*\S", re.IGNORECASE)
REPEAT_RE = re.compile(r"^\s*repeat\b", re.IGNORECASE)
DOC_PARAM_RE = re.compile(r"^\s*''?\s*@param\s+(\w+)\s*(?:-|:)?\s*(.*?)\s*$")

# Assignment forms a return value can receive (Sec 5.1). Every one of these
# errs toward "assigned": a name wrongly counted assigned costs a missed
# finding; a name wrongly counted UNassigned is a false accusation.
INCDEC_POST_RE = re.compile(r"([A-Za-z_]\w*)\s*(?:\+\+|--|~~|~)")
INCDEC_PRE_RE = re.compile(r"(?:\+\+|--)\s*([A-Za-z_]\w*)")
OPASSIGN_RE = re.compile(
    r"([A-Za-z_]\w*)(?:\s*\[[^\]]*\]|\.\[[^\]]*\]|\.\w+)*\s*"
    r"(?:\+//|\+/|//|<<|>>|->|<-|#>|<#|[-+*/&|^])=(?!=)")
WORDOPASSIGN_RE = re.compile(
    r"([A-Za-z_]\w*)\s+(?:sar|ror|rol|rev|zerox|signx|sca|scas|frac|and|or|xor|"
    r"addbits|addpins)=", re.IGNORECASE)
ADDRESS_OF_RE = re.compile(r"@\s*([A-Za-z_]\w*)")
REPEAT_VAR_RE = re.compile(r"\brepeat\s+([A-Za-z_]\w*)\s+from\b", re.IGNORECASE)

# Sec 5.4.1 -- a boolean is recognised by the NAME the guide requires of it.
BOOLNAME = r"(?:b[A-Z]\w*|is[A-Z]\w*|has[A-Z]\w*)"
BOOL_CMP01_RE = re.compile(
    r"\b(" + BOOLNAME + r")\b(?:\s*\([^()]*\))?\s*(==|<>)\s*([01])\b(?!\.\d)")
BOOL_CMP01_REV_RE = re.compile(
    r"(?<![\w$%.])([01])\s*(==|<>)\s*(" + BOOLNAME + r")\b")
BOOL_SET1_RE = re.compile(
    r"\b(" + BOOLNAME + r")\s*:=\s*1\b(?!\.\d)(?!\s*[-+*/<>&|^#])")
RETURN_ONE_RE = re.compile(r"\breturn\s+1\b(?!\.\d)(?!\s*[-+*/<>&|^#])",
                           re.IGNORECASE)

# Numeric literals: $hex, %%quaternary, %binary, decimal, float.
NUM_RE = re.compile(
    r"(?<![\w$%])(\$[0-9A-Fa-f][0-9A-Fa-f_]*|%%[0-3][0-3_]*|%[01][01_]*|"
    r"\d[\d_]*(?:\.\d+)?(?:[eE][+-]?\d+)?)(?!\w)(?!\.\d)")
NUM_FULL_RE = re.compile(r"^\s*(" + NUM_RE.pattern + r")\s*$")
FILLMOVE_RE = re.compile(
    r"\b(bytefill|wordfill|longfill|bytemove|wordmove|longmove)\s*\(",
    re.IGNORECASE)
ARRAY_LIT_RE = re.compile(r"\[\s*(\d[\d_]*|\$[0-9A-Fa-f_]+|%[01_]+)\s*\]")

# Sec 4.9 -- a horizontal line is ONE character repeated. A box-drawing diagram
# row (corners, tees) is documentation, not a separator, and is not flagged.
HLINE_CHARS = set("-=_*~#")
HLINE_MIN = 4

# Symbols the compiler reads from the TOP file only. Defining one beside an
# object that also defines it is not a copied object constant (Sec 2.4).
COMPILER_SYMBOL_PREFIXES = ("_", "debug_", "download_baud")

DATA_KEYWORDS = {"byte", "word", "long", "alignw", "alignl", "file", "org",
                 "orgh", "orgf", "fit", "res"}
HEADER_FIELDS = (("File", r"\bFile\b"), ("Purpose", r"\bPurpose\b"),
                 ("Author", r"\bAuthors?\b"), ("E-mail", r"\bE-?mail\b"),
                 ("Started", r"\bStarted\b"), ("Updated", r"\bUpdated\b"))


def spin_view(text, mask):
    """Live source only: comments and string-literal contents -> spaces.

    Keeps every CODE character and, inside a debug(...) span that is itself
    live (not inside a comment), the payload outside its "..." literals.
    Newlines are kept, so the view splits into the same lines as the text.
    """
    out = list(text)
    n, i = len(text), 0
    while i < n:
        if text[i] == "\n" or mask[i] == CODE:
            i += 1
            continue
        if mask[i] == DEBUG_STRING:
            j = i
            while j < n and mask[j] == DEBUG_STRING:
                j += 1
            live = i == 0 or mask[i - 1] != COMMENT
            in_quote = False
            for k in range(i, j):
                ch = text[k]
                if ch == "\n":
                    continue
                if not live:
                    out[k] = " "
                elif ch == '"':
                    in_quote = not in_quote
                    out[k] = " "
                elif in_quote:
                    out[k] = " "
            i = j
            continue
        out[i] = " "                        # COMMENT or STRING
        i += 1
    return "".join(out)


def code_view(text, mask):
    """CODE characters only -- debug() payloads blanked too."""
    return "".join(ch if (ch == "\n" or mask[i] == CODE) else " "
                   for i, ch in enumerate(text))


def comment_starts(text, mask):
    """[(index, kind)] where each comment OPENS.

    kind: "line" (') "doc-line" ('') "brace" ({) "doc-brace" ({{).
    A comment that opens in the very next character after another comment
    closes (`}'`) is not seen -- rare, and it can only cost recall.
    """
    out = []
    for i, ch in enumerate(text):
        if mask[i] != COMMENT or (i and mask[i - 1] == COMMENT):
            continue
        if ch == "'":
            out.append((i, "doc-line" if text[i + 1:i + 2] == "'" else "line"))
        elif ch == "{":
            out.append((i, "doc-brace" if text[i + 1:i + 2] == "{" else "brace"))
    return out


def split_top(s, sep=","):
    """Split on `sep` at bracket depth 0."""
    parts, depth, cur = [], 0, []
    for ch in s:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == sep and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return parts


def decl_names(group):
    """Names declared in a signature group: `a, BYTE b[4], ^point c` -> a b c."""
    out = []
    for item in split_top(group or ""):
        item = re.sub(r"\[[^\]]*\]", "", item)
        toks = [t for t in IDENT_RE.findall(item)
                if t.lower() not in ("alignw", "alignl")]
        if toks:
            out.append(toks[-1])
    return out


def indent_of(line):
    expanded = line.expandtabs(8)
    return len(expanded) - len(expanded.lstrip())


def lit_value(tok):
    t = tok.replace("_", "")
    try:
        if t.startswith("$"):
            return int(t[1:], 16)
        if t.startswith("%%"):
            return int(t[2:], 4)
        if t.startswith("%"):
            return int(t[1:], 2)
        if "." in t or "e" in t.lower():
            return float(t)
        return int(t)
    except ValueError:
        return None


def after_open_paren(region):
    """The part of `region` after its last still-open `(` (assignment inside
    an expression: `if (found := search())`)."""
    stack = []
    for i, ch in enumerate(region):
        if ch == "(":
            stack.append(i)
        elif ch == ")" and stack:
            stack.pop()
    return region[stack[-1] + 1:] if stack else region


def parse_spin(path, text):
    """One structural reading of a .spin2 file, shared by every T1 rule."""
    mask = context_mask(text)
    raw = text.split("\n")
    svl = spin_view(text, mask).split("\n")
    cvl = code_view(text, mask).split("\n")
    starts, pos = [], 0
    for ln in raw:
        starts.append(pos)
        pos += len(ln) + 1

    def line_of(idx):
        return bisect.bisect_right(starts, idx) - 1

    # Blocks: a block keyword in column 0 of live source.
    blocks = []
    for k, ln in enumerate(svl):
        m = BLOCK_RE.match(ln)
        if m:
            blocks.append({"kind": m.group(1).upper(), "start": k})
    for i, b in enumerate(blocks):
        b["end"] = blocks[i + 1]["start"] if i + 1 < len(blocks) else len(svl)
        b["content"] = [k for k in range(b["start"], b["end"])
                        if (svl[k][3:] if k == b["start"] else svl[k]).strip()]

    comments = comment_starts(text, mask)
    comment_start_set = {i for i, _ in comments}

    # Licence footer: the LAST {{ }} block, with nothing but whitespace after.
    license_start, license_lines = None, set()
    for i, kind in reversed(comments):
        if kind != "doc-brace":
            continue
        j = i
        while j < len(text) and mask[j] == COMMENT:
            j += 1
        if not text[j:].strip():
            license_start = i
            license_lines = set(range(line_of(i), line_of(max(j - 1, i)) + 1))
        break

    # File header: the contiguous '' run at the top (after a version directive).
    k = 1 if raw and VERSION_DIRECTIVE_RE.match(raw[0].strip()) else 0
    while k < len(raw) and not raw[k].strip():
        k += 1
    header = set()
    while k < len(raw) and raw[k].lstrip().startswith("''"):
        header.add(k)
        k += 1

    methods = []
    for b in blocks:
        if b["kind"] not in ("PUB", "PRI"):
            continue
        j = b["start"]
        sig = svl[j].strip()
        while sig.endswith("...") and j + 1 < b["end"]:
            j += 1
            sig = sig[:-3] + " " + svl[j].strip()
        m = METHOD_SIG_RE.match(sig)
        if not m:
            continue                    # a signature we cannot read: say nothing
        body = list(range(j + 1, b["end"]))
        pasm, in_pasm = set(), False
        for k in body:
            toks = svl[k].split()
            first = toks[0].lower() if toks else ""
            if not in_pasm and first in ("org", "orgh"):
                in_pasm = True
            elif in_pasm and first == "end":
                in_pasm = False
            elif in_pasm:
                pasm.add(k)
        stmts, cont = [], False
        for k in body:
            s = svl[k]
            if not s.strip():
                continue
            was_cont, cont = cont, s.rstrip().endswith("...")
            if was_cont or k in pasm:
                continue
            stmts.append((k, indent_of(s)))
        doc = []
        k = j + 1
        while k < b["end"] and not raw[k].strip():
            k += 1
        while k < b["end"] and raw[k].lstrip().startswith("''"):
            doc.append(k)
            k += 1
        uses = set()
        for k in body:
            uses |= {t.lower() for t in IDENT_RE.findall(svl[k])}
        methods.append({
            "kind": m.group(1).upper(), "name": m.group(2), "line": b["start"],
            "sig_end": j, "end": b["end"], "body": body, "pasm": pasm,
            "stmts": stmts, "doc": doc, "uses": uses,
            "params": decl_names(m.group(3)), "returns": decl_names(m.group(4)),
            "locals": decl_names(m.group(5)),
        })

    return {"path": path, "text": text, "mask": mask, "raw": raw, "svl": svl,
            "cvl": cvl, "starts": starts, "line_of": line_of, "blocks": blocks,
            "methods": methods, "comments": comments,
            "comment_start_set": comment_start_set,
            "license_start": license_start, "license_lines": license_lines,
            "header": header}


def block_at(P, k):
    for b in P["blocks"]:
        if b["start"] <= k < b["end"]:
            return b
    return None


def comment_text_of_line(P, k):
    s, line = P["starts"][k], P["raw"][k]
    return "".join(ch for c, ch in enumerate(line) if P["mask"][s + c] == COMMENT)


def block_lines(P, b, view="cvl"):
    """Yield (line, text) for each line of block b in the given view, with the
    block keyword (first 3 columns of the opening line) cut off."""
    for k in range(b["start"], b["end"]):
        yield k, P[view][k][3:] if k == b["start"] else P[view][k]


def var_names(P, b):
    """[(line, name)] declared in a VAR block."""
    out = []
    for k, code in block_lines(P, b):
        if not code.strip():
            continue
        for item in split_top(code):
            item = re.sub(r"\[[^\]]*\]", "", item)
            toks = [t for t in IDENT_RE.findall(item)
                    if t.lower() not in ("alignw", "alignl")]
            if toks and not (len(toks) == 1 and toks[0].lower() in DATA_KEYWORDS):
                out.append((k, toks[-1]))
    return out


def dat_labels(P, b):
    """[(line, label)] of a DAT block: the first token of a line when it is not
    a data keyword. Meant for DATA-only blocks (a PASM mnemonic would be taken
    for a label, which is why the callers exempt blocks containing ORG)."""
    out = []
    for k, code in block_lines(P, b):
        toks = code.split()
        if toks and toks[0].lower() not in DATA_KEYWORDS \
                and IDENT_RE.fullmatch(toks[0]):
            out.append((k, toks[0]))
    return out


def block_has_org(P, b):
    """True when the DAT holds PASM: an ORG/ORGH as the first token of a line,
    or as the first token after the keyword on the DAT line (`DAT  org 0`),
    or after a label (`entry  org`)."""
    for _, code in block_lines(P, b, "svl"):
        toks = [t.lower() for t in code.split()[:2]]
        if "org" in toks or "orgh" in toks:
            return True
    return False


def con_names(P):
    """{lower: (line, Name)} for every constant a file declares in CON."""
    out = {}
    for b in P["blocks"]:
        if b["kind"] != "CON":
            continue
        for k, code in block_lines(P, b):
            if not code.strip():
                continue
            for item in split_top(code):
                item = item.strip()
                m = re.match(r"^STRUCT\s+([A-Za-z_]\w*)", item, re.IGNORECASE)
                if not m:
                    m = re.match(r"^([A-Za-z_]\w*)\s*(?:=|\[|$)", item)
                if m and m.group(1).lower() != "struct":
                    out.setdefault(m.group(1).lower(), (k, m.group(1)))
    return out


# --- the rules --------------------------------------------------------------
# Each takes the parsed file and returns [(lineno, message)].

def rule_2_1_4(P):
    """Letter+digit names (`h1`, `h2`) -- Sec 2.1.4 forbids them outright.
    Signatures and VAR only; DAT labels are left out because PASM register
    naming follows hardware conventions (the Sec 2.1 exception)."""
    out = []
    for m in P["methods"]:
        for role, names in (("parameter", m["params"]),
                            ("return value", m["returns"]),
                            ("local", m["locals"])):
            for nm in names:
                if re.fullmatch(r"[A-Za-z]\d+", nm):
                    out.append((m["line"] + 1,
                                f"{role} '{nm}' of {m['name']}() -- a letter "
                                f"and a digit do not say what it holds"))
    for b in P["blocks"]:
        if b["kind"] == "VAR":
            for k, nm in var_names(P, b):
                if re.fullmatch(r"[A-Za-z]\d+", nm):
                    out.append((k + 1, f"VAR '{nm}' -- a letter and a digit "
                                       f"do not say what it holds"))
    return out


def rule_2_4(P):
    """A local CON name that the OBJ's own file also declares. The object is
    resolved beside this file only (`name.spin2` in the same folder); an
    object found nowhere there is skipped, not guessed at. A copy under a
    DIFFERENT name (MAX_FILES for MAX_OPEN_FILES) is invisible to it."""
    out = []
    local = con_names(P)
    if not local:
        return out
    for b in P["blocks"]:
        if b["kind"] != "OBJ":
            continue
        for k in range(b["start"], b["end"]):
            line = P["raw"][k][3:] if k == b["start"] else P["raw"][k]
            m = re.match(r'^\s*([A-Za-z_]\w*)\s*(?:\[[^\]]*\])?\s*:\s*"([^"]+)"',
                         line)
            if not m:
                continue
            fname = m.group(2)
            child = P["path"].parent / (fname if fname.lower().endswith(".spin2")
                                        else fname + ".spin2")
            if not child.is_file():
                continue
            try:
                ctext = child.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            theirs = con_names(parse_spin(child, ctext))
            for key, (ln, name) in sorted(local.items(), key=lambda x: x[1][0]):
                if key.startswith(COMPILER_SYMBOL_PREFIXES) or key not in theirs:
                    continue
                out.append((ln + 1, f"CON {name} duplicates {m.group(1)}."
                                    f"{theirs[key][1]} (\"{fname}\") -- "
                                    f"reference it through the object"))
    return out


def rule_2_5(P):
    """One @param name documented more than one way in the same file. T1+T2:
    the script finds the variants, a reader decides whether the two names are
    the same parameter. Whitespace is normalised; wording is not."""
    seen = {}
    for k, line in enumerate(P["raw"]):
        m = DOC_PARAM_RE.match(line)
        if not m:
            continue
        idx = P["starts"][k] + (len(line) - len(line.lstrip()))
        if P["mask"][idx] != COMMENT:
            continue
        seen.setdefault(m.group(1).lower(), []).append(
            (k, m.group(1), " ".join(m.group(2).split())))
    out = []
    for sites in seen.values():
        first = sites[0]
        for k, nm, desc in sites[1:]:
            if desc != first[2]:
                out.append((k + 1, f"@param {nm} described differently from "
                                   f"line {first[0] + 1}"))
    return out


def rule_3_1(P):
    """The parts of Sec 3.1's order that survive Sec 3.4 (which lets CON, DAT
    and VAR recur later): a {Spin2_v##} directive sits on line 1; the first
    CON that declares anything comes before every other block; OBJ comes
    before the first method. The header and footer are Sec 4.2 / 4.2.1."""
    out = []
    for k, line in enumerate(P["raw"]):
        lead = len(line) - len(line.lstrip())
        if k and VERSION_DIRECTIVE_RE.match(line.lstrip()) \
                and P["starts"][k] + lead in P["comment_start_set"]:
            out.append((k + 1, "{Spin2_v##} directive is not on line 1"))
    blocks = P["blocks"]
    first_con = next((b for b in blocks
                      if b["kind"] == "CON" and b["content"]), None)
    if first_con:
        before = [b for b in blocks if b["start"] < first_con["start"]]
        if before:
            out.append((first_con["start"] + 1,
                        f"first CON block follows {before[0]['kind']} at line "
                        f"{before[0]['start'] + 1} -- constants open the file"))
    first_method = next((b for b in blocks if b["kind"] in ("PUB", "PRI")), None)
    if first_method:
        for b in blocks:
            if b["kind"] == "OBJ" and b["start"] > first_method["start"]:
                out.append((b["start"] + 1,
                            f"OBJ block follows the first method (line "
                            f"{first_method['start'] + 1})"))
    return out


def rule_3_2(P):
    """Every PUB before every PRI."""
    out, first_pri = [], None
    for b in P["blocks"]:
        if b["kind"] not in ("PUB", "PRI"):
            continue
        m = re.match(r"^(?:PUB|PRI)\s+(\w+)", P["svl"][b["start"]], re.IGNORECASE)
        name = m.group(1) if m else "?"
        if b["kind"] == "PRI" and first_pri is None:
            first_pri = (b["start"], name)
        elif b["kind"] == "PUB" and first_pri is not None:
            out.append((b["start"] + 1, f"PUB {name}() follows PRI "
                                        f"{first_pri[1]}() at line "
                                        f"{first_pri[0] + 1}"))
    return out


def rule_3_4(P):
    """A VAR block, or a DATA-only DAT block, whose names are used only by
    methods ABOVE it -- the state is declared after all of its accessors. A
    DAT holding PASM (it contains ORG) is exempt: it is code, and the P1/P2
    convention places it last. Names used by no method are not this rule."""
    out = []
    for b in P["blocks"]:
        if b["kind"] not in ("VAR", "DAT"):
            continue
        if b["kind"] == "DAT" and block_has_org(P, b):
            continue
        names = var_names(P, b) if b["kind"] == "VAR" else dat_labels(P, b)
        keys = {n.lower() for _, n in names}
        if not keys:
            continue
        before = [m for m in P["methods"]
                  if m["line"] < b["start"] and m["uses"] & keys]
        after = [m for m in P["methods"]
                 if m["line"] > b["start"] and m["uses"] & keys]
        if before and not after:
            shown = ", ".join(n for _, n in names[:3])
            more = f" +{len(names) - 3}" if len(names) > 3 else ""
            out.append((b["start"] + 1,
                        f"{b['kind']} ({shown}{more}) is declared after every "
                        f"method that uses it -- last user {before[-1]['name']}() "
                        f"at line {before[-1]['line'] + 1}"))
    return out


def rule_4_1(P):
    """`''` only in the file header and in a PUB's doc block after its
    signature; never for @local. `{{ }}` only as the licence footer. The
    declaration line itself belongs to Sec 4.5 and is skipped here."""
    out = []
    allowed = set(P["header"])
    for m in P["methods"]:
        if m["kind"] == "PUB":
            allowed |= set(m["doc"])
    decl_lines = {b["start"] for b in P["blocks"]}
    text = P["text"]
    for i, kind in P["comments"]:
        k = P["line_of"](i)
        if k in decl_lines:
            continue
        if kind == "doc-line":
            full = not P["raw"][k][:i - P["starts"][k]].strip()
            eol = text.find("\n", i)
            body = text[i:eol if eol >= 0 else len(text)]
            if "@local" in body.lower():
                out.append((k + 1, "'' @local -- locals are internal; use '"))
                continue
            if full and k in allowed:
                continue
            b = block_at(P, k)
            where = b["kind"] if b else "before the first block"
            if not full:
                why = "trailing '' on a code line"
            elif where == "PRI":
                why = "'' in a PRI block -- PRI documentation uses '"
            elif where == "PUB":
                why = "'' inside a PUB body, away from its doc block"
            elif where in ("CON", "DAT", "VAR", "OBJ"):
                why = f"'' in a {where} block -- declarations use '"
            else:
                why = "'' outside the file header -- notes go in { }"
            out.append((k + 1, why + " (it is extracted into the API document)"))
        elif kind == "doc-brace" and i != P["license_start"]:
            out.append((k + 1, "{{ }} outside the licence footer -- it is "
                               "extracted into the API document"))
    return out


def rule_4_5(P):
    """The comment on a CON/VAR/OBJ/DAT/PUB/PRI line: never '', never {{,
    never {Spin2_Doc_CON}, and not a bare border with no label text. The
    guide's `---- Label ----` dash format is NOT enforced: the guide's own
    REQUIRED example (`VAR ' per-instance state`) does not use it."""
    out = []
    for b in P["blocks"]:
        k = b["start"]
        s, line = P["starts"][k], P["raw"][k]
        col = next((c for c in range(len(line))
                    if P["mask"][s + c] == COMMENT), None)
        if col is None:
            continue
        ctext = line[col:]
        if ctext.startswith("''"):
            out.append((k + 1, f"'' on the {b['kind']} line -- the Outline "
                               f"label uses '"))
        elif ctext.startswith("{{"):
            out.append((k + 1, f"{{{{ on the {b['kind']} line -- the Outline "
                               f"label uses '"))
        if re.search(r"\{\s*Spin2_Doc_CON\s*\}", ctext, re.IGNORECASE):
            out.append((k + 1, "{Spin2_Doc_CON} on the declaration line -- put "
                               "it on the first line inside the block"))
        if ctext.startswith("'") and not ctext.startswith("''"):
            label = ctext.lstrip("'").strip()
            if label and not re.search(r"[A-Za-z0-9]", label):
                out.append((k + 1, f"{b['kind']} label is a border with no "
                                   f"label text"))
    return out


def rule_4_9(P):
    """A horizontal line (one character, repeated >= 4 times) in a comment
    between a CON line and that block's LAST declaration. A separator that
    trails the last declaration -- a divider before the next block -- is
    not flagged; nor is the licence footer."""
    out = []
    for b in P["blocks"]:
        if b["kind"] != "CON":
            continue
        code = [k for k in range(b["start"] + 1, b["end"]) if P["svl"][k].strip()]
        if not code:
            continue
        for k in range(b["start"] + 1, code[-1] + 1):
            if k in P["license_lines"]:
                continue
            t = re.sub(r"[\s'{}]", "", comment_text_of_line(P, k))
            if len(t) >= HLINE_MIN and len(set(t)) == 1 and \
                    (t[0] in HLINE_CHARS or in_box_range(ord(t[0]))):
                out.append((k + 1, f"horizontal line inside CON (block at line "
                                   f"{b['start'] + 1})"))
    return out


def rule_5_0(P):
    """A parameter, return value or local never MENTIONED in the body (live
    code, inline PASM, and debug() payloads all count as mentions). A name
    that is only ever written is counted as used -- recall is given up there
    for precision. A return value is exempt when the body uses `return <expr>`."""
    out = []
    for m in P["methods"]:
        ret_expr = any(RETURN_EXPR_RE.search(P["svl"][k]) for k, _ in m["stmts"])
        for role, names in (("parameter", m["params"]),
                            ("local", m["locals"]),
                            ("return value", m["returns"])):
            for nm in names:
                if nm.lower() in m["uses"]:
                    continue
                if role == "return value" and ret_expr:
                    continue
                out.append((m["line"] + 1, f"{role} '{nm}' of {m['name']}() is "
                                           f"never used in the body"))
    return out


def assigned_names(P, m):
    """Lowercased names the body can have written to. Errs toward 'yes'."""
    got = set()
    for k in m["body"]:
        s = P["svl"][k]
        if not s.strip():
            continue
        if k in m["pasm"]:                  # a PASM operand may be a write
            got |= {t.lower() for t in IDENT_RE.findall(s)}
            continue
        prev = 0
        for mm in re.finditer(r":=", s):
            region = after_open_paren(s[prev:mm.start()])
            got |= {t.lower() for t in IDENT_RE.findall(region)}
            prev = mm.end()
        for rx in (INCDEC_POST_RE, INCDEC_PRE_RE, OPASSIGN_RE, WORDOPASSIGN_RE,
                   ADDRESS_OF_RE, REPEAT_VAR_RE):
            got |= {g.lower() for g in rx.findall(s)}
    return got


def rule_5_1(P):
    """A declared return value that nothing assigns. Counted as assigned: any
    `:=` target (including multi-assign and chains), ++ -- ~ ~~, op-assign,
    `@name` (its address escapes), a `repeat name from` loop variable, and any
    mention in inline PASM. A method with `return <expr>` supplies its value
    explicitly and is not flagged."""
    out = []
    for m in P["methods"]:
        if not m["returns"]:
            continue
        if any(RETURN_EXPR_RE.search(P["svl"][k]) for k, _ in m["stmts"]):
            continue
        got = assigned_names(P, m)
        for nm in m["returns"]:
            if nm.lower() not in got:
                out.append((m["line"] + 1, f"return value '{nm}' of {m['name']}()"
                                           f" is never assigned -- it returns "
                                           f"the implicit 0"))
    return out


def rule_5_2(P):
    """`return` anywhere but as the method's LAST statement at body level.
    Inline-PASM RET is not counted: it leaves the ORG block, not the method.
    ABORT is not counted either; the guide does not name it."""
    out = []
    for m in P["methods"]:
        if not m["stmts"]:
            continue
        base = m["stmts"][0][1]
        last_k = m["stmts"][-1][0]
        for k, ind in m["stmts"]:
            s = P["svl"][k]
            if not RETURN_RE.search(s):
                continue
            if k == last_k and ind == base and s.strip().lower().startswith("return"):
                continue
            out.append((k + 1, f"early return in {m['name']}() -- route every "
                               f"path to the method's end"))
    return out


def rule_5_3(P):
    """`return` inside a `repeat` body (found by indentation: the nearest
    shallower statements above the return, walked outward)."""
    out = []
    for m in P["methods"]:
        stmts = m["stmts"]
        for pos, (k, ind) in enumerate(stmts):
            if not RETURN_RE.search(P["svl"][k]):
                continue
            level = ind
            for k2, ind2 in reversed(stmts[:pos]):
                if ind2 >= level:
                    continue
                level = ind2
                if REPEAT_RE.match(P["svl"][k2]):
                    out.append((k + 1, f"return inside the repeat at line "
                                       f"{k2 + 1} in {m['name']}() -- set the "
                                       f"result and quit"))
                    break
    return out


def rule_5_4_1(P):
    """A boolean -- recognised by the b / is / has name Sec 5.4.1 requires --
    compared with 1 or 0, set to 1, or returned as `return 1`. A boolean with
    any other name is invisible to it."""
    out = []
    for m in P["methods"]:
        boolish = bool(re.match(BOOLNAME, m["name"])) or any(
            re.fullmatch(BOOLNAME, r) for r in m["returns"][:1])
        for k, _ in m["stmts"]:
            s = P["svl"][k]
            for mm in BOOL_CMP01_RE.finditer(s):
                out.append((k + 1, f"{mm.group(1)} {mm.group(2)} {mm.group(3)} -- "
                                   f"compare a boolean with TRUE / FALSE"))
            for mm in BOOL_CMP01_REV_RE.finditer(s):
                out.append((k + 1, f"{mm.group(1)} {mm.group(2)} {mm.group(3)} -- "
                                   f"compare a boolean with TRUE / FALSE"))
            for mm in BOOL_SET1_RE.finditer(s):
                out.append((k + 1, f"{mm.group(1)} := 1 -- 1 is truthy but is "
                                   f"not TRUE (-1)"))
            if boolish and RETURN_ONE_RE.search(s):
                out.append((k + 1, f"return 1 from boolean {m['name']}() -- "
                                   f"return TRUE"))
    return out


def rule_5_7(P):
    """CANDIDATES only (T1+T2): numeric literals in method code, outside
    inline PASM, debug() and strings. Not candidates: 0, a unary -1, and 4
    beside `*` -- the guide's three exceptions -- and a 1 that is added or
    subtracted (`N - 1`, `x + 1`, `x -= 1`), because the guide's own REQUIRED
    examples write exactly that (`repeat idx from 0 to MAX_COGS - 1` in 5.7,
    `driver.MAX_OPEN_FILES - 1` in 2.4, `SECTOR_SIZE + 1` in 6.4); flagging
    it would flag the guide. CON is where literals belong; DAT, VAR and PASM
    are not scanned. A reader judges each site."""
    out = []
    for m in P["methods"]:
        for k in m["body"]:
            if k in m["pasm"]:
                continue
            s = P["cvl"][k]
            if not s.strip():
                continue
            for mm in NUM_RE.finditer(s):
                val = lit_value(mm.group(1))
                if val == 0:
                    continue
                before = s[:mm.start()].rstrip()
                after = s[mm.end():].lstrip()
                if val == 1 and before.endswith(("+", "-", "+=", "-=")):
                    continue            # unary -1, or the +/-1 the guide writes
                if val == 4 and (before.endswith("*") or after.startswith("*")):
                    continue
                out.append((k + 1, f"literal {mm.group(1)} in {m['name']}(): "
                                   f"{s.strip()[:60]}"))
    return out


def rule_6_4(P):
    """A literal count in bytefill/wordfill/longfill/bytemove/wordmove/longmove,
    and a literal array size (>= 2) declared in VAR, in a data-only DAT, or as
    a method local. Part 6 is CONDITIONAL on a regression harness this
    project does not have, so this rule is not binding here; it overlaps Sec
    5.7's 'buffer and array sizes'."""
    out = []
    for m in P["methods"]:
        for k in m["body"]:
            if k in m["pasm"]:
                continue
            s = P["cvl"][k]
            for mm in FILLMOVE_RE.finditer(s):
                depth, j = 1, mm.end()
                while j < len(s) and depth:
                    depth += {"(": 1, ")": -1}.get(s[j], 0)
                    j += 1
                args = split_top(s[mm.end():j - 1])
                if len(args) == 3:
                    lm = NUM_FULL_RE.match(args[2])
                    if lm and lit_value(lm.group(1)):
                        out.append((k + 1, f"{mm.group(1)} count {args[2].strip()} "
                                           f"is a literal"))
        sig_locals = P["svl"][m["line"]]
        for lm in ARRAY_LIT_RE.finditer(sig_locals.split("|", 1)[1]
                                        if "|" in sig_locals else ""):
            if (lit_value(lm.group(1)) or 0) >= 2:
                out.append((m["line"] + 1, f"local array size [{lm.group(1)}] in "
                                           f"{m['name']}() is a literal"))
    for b in P["blocks"]:
        if b["kind"] == "VAR" or (b["kind"] == "DAT" and not block_has_org(P, b)):
            for k, code in block_lines(P, b):
                for lm in ARRAY_LIT_RE.finditer(code):
                    if (lit_value(lm.group(1)) or 0) >= 2:
                        out.append((k + 1, f"{b['kind']} array size "
                                           f"[{lm.group(1)}] is a literal"))
    return out


def rule_4_2(P):
    """The file opens (after an optional {Spin2_v##} line) with a '' header
    that names the file (matching its real name), purpose, author(s),
    e-mail, started and updated dates."""
    if not P["header"]:
        return [(1, "no '' header block at the top of the file")]
    k0 = min(P["header"])
    block = "\n".join(P["raw"][k] for k in sorted(P["header"]))
    missing = [label for label, rx in HEADER_FIELDS if not re.search(rx, block)]
    out = [(k0 + 1, f"header lacks field(s): {', '.join(missing)}")] \
        if missing else []
    m = re.search(r"\bFile\b\.*\s*([^\s]+)", block)
    if m and m.group(1) != P["path"].name:
        out.append((k0 + 1, f"header names the file {m.group(1)!r}, but it is "
                            f"{P['path'].name!r}"))
    return out


def rule_4_2_1(P):
    """The file ends with a {{ }} licence footer that carries a copyright and
    the holder the repo LICENSE names. The YEAR is not compared -- see the
    coverage note."""
    if P["license_start"] is None:
        last = len(P["raw"]) - (1 if P["raw"] and not P["raw"][-1] else 0)
        return [(max(last, 1), "no {{ }} licence footer at the end of the file")]
    k = P["line_of"](P["license_start"])
    body = "\n".join(P["raw"][j] for j in sorted(P["license_lines"]))
    if not re.search(r"copyright", body, re.IGNORECASE):
        return [(k + 1, "licence footer carries no copyright line")]
    if LICENSE_HOLDER and LICENSE_HOLDER not in body:
        return [(k + 1, f"licence footer does not name {LICENSE_HOLDER!r}, the "
                        f"holder in the repo LICENSE")]
    return []


# The copyright holder of the repo LICENSE, read once (Sec 4.2.1).
LICENSE_HOLDER = None
_lic = pathlib.Path(__file__).resolve().parents[3] / "LICENSE"
if _lic.is_file():
    _m = re.search(r"Copyright \(c\)\s*[\d\s,-]+\s+(.+)", _lic.read_text(
        encoding="utf-8", errors="replace"))
    LICENSE_HOLDER = _m.group(1).strip() if _m else None


# (sec, title, detector). Order = the guide's order.
T1_RULES = [
    ("2.1.4", "letter+digit names (T1+T2 detector)", rule_2_1_4),
    ("2.4", "object constant copied into a local CON", rule_2_4),
    ("2.5", "one @param name, several descriptions (T1+T2 detector)", rule_2_5),
    ("3.1", "file layout order", rule_3_1),
    ("3.2", "PUB before PRI", rule_3_2),
    ("3.4", "state declared after every method that uses it", rule_3_4),
    ("4.1", "doc comments only where extraction is intended", rule_4_1),
    ("4.2", "'' file header", rule_4_2),
    ("4.2.1", "licence footer", rule_4_2_1),
    ("4.5", "block declaration labels", rule_4_5),
    ("4.9", "no horizontal lines inside CON", rule_4_9),
    ("5.0", "no unused parameters, return values or locals", rule_5_0),
    ("5.1", "return values explicitly assigned", rule_5_1),
    ("5.2", "single exit point", rule_5_2),
    ("5.3", "quit, never return, from a loop", rule_5_3),
    ("5.4.1", "booleans are TRUE / FALSE, never 1 / 0", rule_5_4_1),
    ("5.7", "magic-number CANDIDATES (T1+T2 detector)", rule_5_7),
    ("6.4", "buffer sizes as named constants (Part 6: conditional)", rule_6_4),
]
T1_RULE_IDS = [sec for sec, _, _ in T1_RULES]


def audit_t1_rules(path: pathlib.Path):
    """{sec: [(lineno, message)]} for every rule in T1_RULES."""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return {}
    P = parse_spin(path, text)
    return {sec: sorted(fn(P)) for sec, _, fn in T1_RULES}


# ---------------------------------------------------------------------------
# T1 COVERAGE -- what this instrument does NOT check, said out loud.
#
# `central:spin2-authoring-guide` tiers every rule on its own heading: 26 are
# T1 (script-checkable) and 5 are T1+T2 (a script DETECTS, an agent JUDGES).
# Central v12's ruling is that a gate reports three things -- what passed, what
# it did not check, and **which assigned-T1 rules are still unimplemented** --
# because that third one hides: an unimplemented T1 rule looks exactly like a
# rule with nothing to say.
#
# Every rule below except Sec 1.1 is ADVISORY by default; `--blocking` arms a
# chosen set for one run. Findings from probing pnut-ts 1.55.8 (2026-09-26,
# scratch fixtures, «#360»): five "T1" rules are compile errors today, and in
# three of them the guide's stated premise is contradicted by the compiler.
T1_IMPLEMENTED = {
    "1.1": "ASCII only -- BLOCKING, always",
    "2.1": "no single-letter names (signatures only)",
    "2.4": "local CON copying an object's constant (object resolved beside the file)",
    "3.1": "{Spin2_v##} on line 1; first CON first; OBJ before methods",
    "3.2": "PUB before PRI",
    "3.4": "VAR / data-only DAT after every method using it (PASM DATs exempt)",
    "4.1": "'' only in the header and PUB doc blocks; {{ }} only as the footer",
    "4.2": "'' header with File/Purpose/Author/E-mail/Started/Updated; File = name",
    "4.2.1": "{{ }} licence footer last, with copyright + the LICENSE holder "
             "(year NOT compared: LICENSE says 2024-2026, footers say 2026)",
    "4.5": "declaration-line label: no '', no {{, no {Spin2_Doc_CON}, no bare "
           "border (dash format NOT enforced: the guide's own example omits it)",
    "4.9": "no one-character-repeated line between a CON line and its last "
           "declaration (trailing dividers not flagged)",
    "5.0": "every parameter, return value and local mentioned in the body",
    "5.1": "every return value assigned, or a `return <expr>`",
    "5.2": "`return` only as the last statement, at body level",
    "5.3": "no `return` inside a `repeat` body",
    "5.4.1": "b/is/has booleans never compared with, set to, or returned as 1/0",
    "6.4": "literal fill/move counts and array sizes (Part 6 is conditional -- "
           "no harness here, so not binding)",
}
T1T2_DETECTORS = {
    "2.1.4": "letter+digit names (h1, h2) in signatures and VAR",
    "2.5": "one @param name documented several ways in a file",
    "5.7": "numeric literals in method code, less 0, -1, 4 beside *, and the "
           "+/-1 the guide's own REQUIRED examples write",
}
T1_NOT_IMPLEMENTED = {
    "1.3": "compile-enforced: 8 of the 9 table names fail as locals (m241); "
           "`bool` COMPILES as a local and a CON -- FINDING: the row is false",
    "1.4": "compile-enforced ('Expected a unique method name') -- T0 in fact",
    "1.5": "compile-enforced (m242) -- FINDING: the guide says the compiler "
           "does not warn",
    "1.8": "compile-enforced (`@\"\"` -> 'Empty string') -- T0 in fact",
    "1.9": "compile-enforced (m190) -- FINDING: the guide says it fails silently",
    "3.1.1": "{Spin2_v##} directive -- the compiler contradicts the rule, so "
             "it is a finding, not a check (central nomination filed, «#359»/«#360»)",
    "5.4": "needs 'operation vs query' judgement; the guide's own eofHandle() "
           "example defeats an is/has naming proxy",
    "6.2": "Part 6 is conditional (no harness here); it is Sec 2.4 applied to "
           "tests, and Sec 2.4's detector finds the same thing",
    "6.7": "tests must pass -- a run result, not a property of the source; "
           "no harness here",
    "4.6 (T1+T2)": "no mechanical signal beyond Sec 4.1's '' check; which "
                   "descriptions are 'important' is judgement",
    "6.1 (T1+T2)": "Part 6 is conditional; no harness here",
}


def audit_file(path: pathlib.Path):
    """Return a list of (lineno, col, char, context, reason, suggestion)."""
    hits = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # Same 6-field shape as every other hit; the 5-field form crashed main()'s
        # unpacking with a traceback instead of reporting the file.
        return [(0, 0, "", CODE, "file is not valid UTF-8 -- cannot be ASCII either", "")]
    mask = context_mask(text)
    lineno, col = 1, 1
    for idx, ch in enumerate(text):
        if ch == "\n":
            lineno, col = lineno + 1, 1
            continue
        cp = ord(ch)
        if cp >= 128:
            ctx = mask[idx]
            if in_box_range(cp):
                # Permitted ONLY in a comment. In a string it still reaches the
                # terminal as multi-byte UTF-8, so the exception does not apply.
                if ctx != COMMENT:
                    hits.append((lineno, col, ch, ctx,
                                 "box-drawing character " + CONTEXT_NAME[ctx], ""))
            else:
                hits.append((lineno, col, ch, ctx,
                             unicodedata.name(ch, "unnamed codepoint"),
                             SUGGEST.get(cp, "")))
        col += 1
    return hits


def collect(paths, root: pathlib.Path):
    files, roots_used = [], []
    if paths:
        for p in paths:
            q = pathlib.Path(p)
            if q.is_file():
                files.append(q)
            elif q.is_dir():
                files.extend(sorted(q.rglob("*.spin2")))
            else:
                print(f"ERROR: not a file or directory: {q}")
                return None, None
        roots_used = [str(p) for p in paths]
    else:
        for g in DEFAULT_GLOBS:
            files.extend(sorted(root.glob(g)))
        roots_used = DEFAULT_GLOBS
    keep = [f for f in files
            if not any(part in str(f) for part in EXCLUDE_PARTS)]
    return sorted(set(keep)), roots_used


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", metavar="PATH",
                    help="file or directory; default = the authored roots")
    ap.add_argument("--quiet", action="store_true",
                    help="print only violations and the summary line")
    ap.add_argument("--list-files", action="store_true",
                    help="print every audited path, then exit")
    ap.add_argument("--show-all", action="store_true",
                    help="print every advisory site, not the first 15 per rule")
    ap.add_argument("--blocking", metavar="SECS", default="",
                    help="comma-separated rule numbers (e.g. 5.2,5.3,3.2) whose "
                         "sites count toward the exit status for THIS run; "
                         "default: none beyond Sec 1.1, which always blocks")
    args = ap.parse_args()

    # Rules armed for this run. Sec 1.1 always blocks and needs no naming.
    blocking = {s.strip() for s in args.blocking.split(",") if s.strip()}
    blocking.discard("1.1")
    unknown = sorted(blocking - set(T1_RULE_IDS) - {"2.1"})
    if unknown:
        print(f"ERROR: --blocking names no such rule: {', '.join(unknown)}. "
              f"Known: 2.1, {', '.join(T1_RULE_IDS)}")
        return 2

    root = pathlib.Path(__file__).resolve().parents[3]
    files, roots_used = collect(args.paths, root)
    if files is None:
        return 2

    if args.list_files:
        for f in files:
            print(f.resolve().relative_to(root) if root in f.resolve().parents else f)
        print(f"\n{len(files)} file(s)")
        return 0

    if not files:
        print("ERROR: no .spin2 files matched -- check the path or the roots")
        return 2

    def relp(f):
        return f.resolve().relative_to(root) if root in f.resolve().parents else f

    total = 0
    by_ctx = {}
    advisory = []          # Sec 2.1 -- reported, never added to `total`
    t1_hits = {sec: [] for sec in T1_RULE_IDS}   # (file, lineno, message)
    unparsed = []          # files the T1 rules could not read -- said, not hidden
    for f in files:
        advisory += [(f,) + h for h in audit_single_letter_names(f)]
        # The advisory rules must never be able to break the Sec 1.1 gate: a
        # detector defect is reported against the file and the run goes on.
        try:
            for sec, sites in audit_t1_rules(f).items():
                t1_hits[sec] += [(f, ln, msg) for ln, msg in sites]
        except Exception as exc:                        # noqa: BLE001
            unparsed.append((f, f"{type(exc).__name__}: {exc}"))
        hits = audit_file(f)
        if not hits:
            continue
        total += len(hits)
        rel = f.resolve().relative_to(root) if root in f.resolve().parents else f
        for lineno, col, ch, ctx, why, fix in hits:
            if not ch:                      # file-level problem (bad encoding)
                print(f"{rel}: {why}")
                continue
            by_ctx[ctx] = by_ctx.get(ctx, 0) + 1
            tail = f"  ->  use {fix!r}" if fix else ""
            print(f"{rel}:{lineno}:{col}: U+{ord(ch):04X} {ch!r} {why} "
                  f"[{CONTEXT_NAME[ctx]}]{tail}")

    # Say what was audited. A gate whose coverage is invisible is a gate that can
    # silently stop covering the thing most likely to be wrong.
    if not args.quiet:
        print()
        if not args.paths:
            print("roots audited:")
            for g in roots_used:
                print(f"  {g}")
            print("excluded by rule: " + ", ".join(p.strip('/') for p in EXCLUDE_PARTS))
    # Sec 2.1 -- ADVISORY. Printed in full, counted separately, and deliberately
    # NOT folded into `total`: it must not flip this gate red until Stephen has
    # ruled on arming it (see the note beside audit_single_letter_names).
    # `--blocking 2.1` arms it for one run (a scope the owner has ruled on);
    # every site is then printed, even under --quiet, because it is a violation.
    armed21 = "2.1" in blocking
    if armed21 or (advisory and not args.quiet):
        shown = advisory if (args.show_all or armed21) else advisory[:15]
        state = "BLOCKING this run (--blocking)." if armed21 else "NOT blocking."
        print(f"\n{'BLOCKING' if armed21 else 'ADVISORY'} -- Sec 2.1 "
              f"single-letter names: {len(advisory)} site(s) across "
              f"{len({a[0] for a in advisory})} file(s). {state}")
        for f, lineno, name, sig in shown:
            print(f"  {relp(f)}:{lineno}: {name!r}  |  {sig}")
        if len(shown) < len(advisory):
            print(f"  ... {len(advisory) - len(shown)} more "
                  f"(use --show-all to see every site)")
        if not armed21:
            print("  Arming this as blocking is a scope decision: most sites are "
                  "in examples-library/,")
            print("  whose files are byte-identical to code printed in released "
                  "PDFs.")

    # The further T1 rules. Advisory unless named in --blocking; an armed rule
    # prints every site, even under --quiet, because each one is a violation.
    for sec, title, _fn in T1_RULES:
        armed = sec in blocking
        if args.quiet and not armed:
            continue
        sites = t1_hits[sec]
        nfiles = len({s[0] for s in sites})
        state = "BLOCKING this run (--blocking)." if armed else "NOT blocking."
        print(f"\n{'BLOCKING' if armed else 'ADVISORY'} -- Sec {sec} {title}: "
              f"{len(sites)} site(s) across {nfiles} file(s). {state}")
        shown = sites if (args.show_all or armed) else sites[:15]
        for f, lineno, msg in shown:
            print(f"  {relp(f)}:{lineno}: [{sec}] {msg}")
        if len(shown) < len(sites):
            print(f"  ... {len(sites) - len(shown)} more "
                  f"(use --show-all to see every site)")
    if unparsed:
        print(f"\nWARNING -- the T1 rules could not read {len(unparsed)} file(s); "
              f"none of their rules ran there:")
        for f, why in unparsed:
            print(f"  {relp(f)}: {why}")

    # Coverage. A gate that reports only what it caught invites the reader to
    # believe it looked at everything.
    if not args.quiet:
        print("\nT1 COVERAGE (central:spin2-authoring-guide tiers its own rules: "
              "26 T1 + 5 T1+T2):")
        for sec, what in T1_IMPLEMENTED.items():
            mode = "BLOCKING" if (sec == "1.1" or sec in blocking) else "advisory"
            print(f"  implemented    Sec {sec:<6} [{mode}] {what}")
        for sec, what in T1T2_DETECTORS.items():
            mode = "BLOCKING" if sec in blocking else "advisory"
            print(f"  T1+T2 detector Sec {sec:<6} [{mode}] {what}")
        for sec, what in T1_NOT_IMPLEMENTED.items():
            print(f"  NOT checked    Sec {sec:<6} {what}")

    # Sites in rules armed by --blocking. A file the rules could not read
    # cannot be certified, so it counts as a blocked failure when anything
    # is armed.
    blocked = sum(len(t1_hits[s]) for s in blocking if s in t1_hits)
    blocked += len(advisory) if armed21 else 0
    blocked += len(unparsed) if blocking else 0

    def blocking_verdict():
        if not blocking:
            return
        armed_list = ", ".join(sorted(blocking, key=lambda s: [int(p) for p in
                                                               s.split(".")]))
        if blocked:
            print(f"FAIL  {blocked} site(s) in rule(s) armed by --blocking "
                  f"(Sec {armed_list}) across {len(files)} audited file(s)")
        else:
            print(f"PASS  0 sites in rule(s) armed by --blocking "
                  f"(Sec {armed_list}) across {len(files)} audited file(s)")

    if total:
        # Severity is a property of WHERE the byte sits, not of the count. A
        # debug string reaches the terminal at runtime; a comment never leaves
        # the repo. Break the total out so the reader can triage.
        print(f"\nFAIL  {total} violation(s) across {len(files)} audited file(s)")
        for ctx in (DEBUG_STRING, STRING, CODE, COMMENT):
            if by_ctx.get(ctx):
                print(f"      {by_ctx[ctx]:4d}  {CONTEXT_NAME[ctx]:<22} "
                      f"{CONTEXT_SEVERITY[ctx]}")
        blocking_verdict()
        return 1
    print(f"PASS  {len(files)} file(s) conformant "
          f"(spin2-authoring-guide Sec 1.1: ASCII only, "
          f"box drawing U+2500-257F / U+2580-259F permitted in comments)")
    blocking_verdict()
    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main())
