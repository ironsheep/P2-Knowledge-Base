#!/usr/bin/env python3
"""
audit-kb-code-compiles.py -- the KB compile gate (ENH-03).

THE QUESTION
    Does every block of code the shipped P2KB YAML carries compile, in the
    context its manifest entry declares?

LEGALITY ONLY
    A pass means `pnut-ts` ACCEPTS the block in the declared context. It does NOT
    mean the code does what the surrounding text says, or that any P2 fact it
    states is right (F-381: correct = compiles AND agrees with sourced facts; this
    gate answers the first half only. F-312: fixing `qvector y_val` so it
    assembles would have left X and Y swapped, and this gate would have passed it).

DESIGN
    engineering/analysis/2026-10-08-enh-03-compile-gate-design.md (APPROVED). This
    file implements sections 2-8 of it and re-decides nothing. Section numbers in
    comments below refer to that document.

THE MODEL
    The finder (3.1) casts a net. EVERY candidate must carry a manifest decision,
    including the decision that it is not code.
      net 1  every string scalar under a code-named key  (kb-compile-manifest/
             _code-keys.yaml -- DATA, seeded from the census, reviewed);
      net 2  every multi-line string the COMPILER recognises as code-bearing: the
             string is elementized (`pnut-ts --pass elementize --log elementizer`)
             and taken when a line opens with a block keyword, an instruction
             (an `if_*` condition prefix is allowed), an assembler directive or
             DEBUG, or any line holds an assignment operator (`:=`, `+=`, ...).
             The compiler's own token classes do the recognising: there is no
             keyword list in this script.
    The manifest decides what each candidate IS (the gate does not search for
    context at gate time: the manifest PINS it, 4.2).

ADDRESS (3.2)
    <kb-relative file> + <YAML path>, e.g. language/pasm2/qvector.yaml +
    examples[1].code. Mapping keys are joined with `.`, a sequence index is `[n]`,
    a key not matching ^[A-Za-z0-9_-]+$ is written ["key"]. A multi-document file
    prefixes `#n:` (n counts documents from 1).

FINGERPRINT AND RECONCILIATION (3.3)
    fp = first 16 hex digits of SHA-256 of the PARSED scalar value. Per file the
    entries are matched to the candidates, fingerprint first, path settling ties:
      MATCH         fp and at both current
      MOVED         fp found at a different path
      CHANGED       same at, new fp (the carried class is asserted on the new text)
      UNCLASSIFIED  a candidate with no entry                          always FAIL
      ORPHAN        an entry whose block, or whole KB file, is gone    always FAIL
    MOVED / CHANGED fail in release strictness (full sweep, --since) and are only
    reported by the edit-time check (--files). `--refresh` rewrites at/fp.

MANIFEST SCHEMA
    One sidecar per KB file that has candidates, mirroring the tree:
        engineering/tools/validation/kb-compile-manifest/<kb-relative path>
    plus the net-1 key list  kb-compile-manifest/_code-keys.yaml:
        code_keys: [code, example, ...]
    A sidecar:
        blocks:
          - at: examples[1].code          # address (3.2)
            fp: "3f2a9c0d1e5b7a44"        # always quoted by the tool: an all-digit
                                          #   fingerprint would parse as an integer
            compile: fragment             # program | fragment | never | not-code
            wrap: pasm2-dat               # fragment / never only (below)
            assumes: [x_coord, y_coord]   # fragment / never only (below)
            reason: ...                   # REQUIRED for never and not-code
            fails_at: 3                   # never only: block-relative line (5)
            spin2_version: 45             # optional, wraps only: {Spin2_v45} line 1
            with: [examples[0].code]      # optional, wraps only: prepend siblings
            finding: F-381                # optional, reporting only; NEVER changes
                                          #   the verdict (a known-broken block stays
                                          #   program/fragment and stays red)
    compile:
      program   compiles BYTE FOR BYTE as shown; no wrap, no assumes.
      fragment  compiles inside `wrap` with exactly `assumes` declared.
      never     the KB teaches the compile error: the gate asserts it FAILS at
                `fails_at` (NEVER-COMPILES / NEVER-WRONG-REASON otherwise).
      not-code  prose, notation, shell command, listing... not compiled.
    wrap (4.2):  spin2-top | spin2-method | pasm2-dat | pasm2-hub | pasm2-inline
    assumes (the names the wrap declares, 4.2 / 4.4):
      NAME              operand: trailing `DAT NAME long 0`; for pasm2-inline a
                        LOCAL of the wrapper method (hub DAT longs fail there)
      NAME=con          trailing `CON NAME = 0`
      NAME()->R/N       callee stub `PRI NAME(p1..pN) : r1..rR`  (R, N optional)
      OBJ.METHOD(N)     method of a generated stub object; the object FILE is the
                        one the block's own `OBJ OBJ : "file"` line names
      file:NAME         an empty file NAME in the compile directory (FILE/#include)
    A program never gets a wrap, an assumes list or a language directive: it must
    compile as shown. The manifest carries NO compiler version (PL-004).

DEBUG (6)
    `pnut-ts -d` is applied IFF the wrapped block holds a `type_debug` token
    (asked of the elementizer). Without -d, garbage inside debug() compiles; with
    a blanket -d, legal low-clock programs fail.

MODES (7.1)
    (no args)                       full sweep, release strictness
    --files F...                    the same checks on those KB files (edit-time)
    --since REV                     files changed in REV..HEAD, release strictness;
                                    also prints the manifest diff stat over the range
    --propose [--files F...]        proposals (wrap, assumes, flagged callees,
                                    outcome); NEVER writes the manifest
    --refresh --files F... [--accept-assumes NAME...]
                                    rewrite at/fp for blocks that still hold their
                                    class; a new assumed name only if named here
    --negative-control              the 11 synthetic controls (7.3)
    --census                        the finder's census only (no manifest, no compile)
    --json PATH                     machine-readable result to a scratch path

EXIT (7.2)
    0  every block holds its declared class; nothing stale, unclassified, orphaned
    1  any problem line
    2  cannot audit: pnut-ts not on PATH, KB tree / manifest unreadable, YAML parse
       failure, the proposer self-check, or ZERO candidates ("nothing audited" is
       never a pass)

The repo root is the WORKING DIRECTORY, never this script's path. Build outputs go
to a temp directory outside the repo that is removed afterwards.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
from collections import Counter, defaultdict

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR: audit-kb-code-compiles: PyYAML is required (import yaml failed)", file=sys.stderr)
    sys.exit(2)


KB_DIR = os.path.join("deliverables", "ai", "P2")
MANIFEST_DIR = os.path.join("engineering", "tools", "validation", "kb-compile-manifest")
CODE_KEYS_FILE = "_code-keys.yaml"
MAIN_NAME = "kb.spin2"
WRAPS = ("spin2-top", "spin2-method", "pasm2-dat", "pasm2-hub", "pasm2-inline")
CLASSES = ("program", "fragment", "never", "not-code")
ENTRY_KEYS = {"at", "fp", "compile", "wrap", "assumes", "reason", "fails_at",
              "spin2_version", "with", "finding"}
NWORK = max(1, os.cpu_count() or 4)
COMPILE_TIMEOUT = 30       # a compile takes ~0.1 s; PNut-TS has inputs it never finishes on
ELEMENTIZE_TIMEOUT = 20    # (see with_final_newline): a hung run also grows to GBs, so stay short

LEGALITY_NOTE = (
    "LEGALITY ONLY: a pass means pnut-ts accepts each block in its declared context. It does not\n"
    "mean the code does what its text says, or that any P2 fact in it is right (F-381: correct =\n"
    "compiles AND agrees with sourced facts; this gate answers the first half only)."
)

ERR_RE = re.compile(r"^(.*?):(\d+):error:(.*)$", re.M)
TOK_RE = re.compile(r'\[Ln#(\d+)\((\d+)\) (type_\w+)(?:, ("[^"]*"|[^\]]*?))? COL\([\d-]+\)\]')
ELEM_LINE_RE = re.compile(r"get (?:EARLY|IN-LOOP) elements\(\d+\)=")
NAME_RE = r"[A-Za-z_][A-Za-z0-9_]*"
UNIQUE_MARKERS = ("already defined", "unique")
OPEN_TYPES = ("type_block", "type_asm_inst", "type_asm_dir", "type_debug")

TMP_ROOT = None


class CannotAudit(Exception):
    """Exit 2: the gate cannot say pass or fail."""


# ============================================================ running pnut-ts

def tmp_root():
    global TMP_ROOT
    if TMP_ROOT is None:
        TMP_ROOT = tempfile.mkdtemp(prefix="kbgate-")
    return TMP_ROOT


def cleanup_tmp():
    global TMP_ROOT
    if TMP_ROOT:
        shutil.rmtree(TMP_ROOT, ignore_errors=True)
        TMP_ROOT = None


def run_cmd(cmd, cwd, timeout=COMPILE_TIMEOUT):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=timeout)
    except FileNotFoundError:
        raise CannotAudit("pnut-ts not found on PATH") from None
    except subprocess.TimeoutExpired:
        return -9, "TIMEOUT after %ds" % timeout
    out = (p.stdout + b"\n" + p.stderr).decode("utf-8", "replace")
    return p.returncode, out


def with_final_newline(text):
    """PNut-TS hangs (unbounded CPU and memory) on some sources that end WITHOUT a
    final newline -- e.g. the one-line text `0..9 expands to 0, 1, 2, ..., 9`
    (`pnut-ts -q f.spin2` on that exact file, no trailing newline: never returns).
    Every file this gate hands the compiler therefore ends with a newline. The
    code is otherwise byte for byte."""
    return text if text.endswith("\n") else text + "\n"


def check_pnut():
    tmp_root()  # created here, single-threaded, before any worker asks for it
    if shutil.which("pnut-ts") is None:
        raise CannotAudit("pnut-ts not found on PATH")


def pnut_version():
    rc, out = run_cmd(["pnut-ts", "--version"], cwd=tmp_root(), timeout=30)
    lines = [l.strip() for l in out.splitlines() if l.strip()]
    for l in lines:
        if "PNut-TS" in l or "pnut" in l.lower():
            return l
    return lines[0] if lines else "(unknown)"


class Tok:
    __slots__ = ("line", "col", "typ", "name")

    def __init__(self, line, col, typ, name):
        self.line, self.col, self.typ, self.name = line, col, typ, name


def parse_elementizer_log(out, src_lines):
    """Tokens from `--log elementizer` output. Names are upper-cased by the
    compiler; the original spelling is recovered from the source by column."""
    toks = []
    for raw in out.splitlines():
        if not ELEM_LINE_RE.search(raw):
            continue
        for m in TOK_RE.finditer(raw):
            ln, col, typ, payload = int(m.group(1)), int(m.group(2)), m.group(3), m.group(4)
            name = None
            if typ == "type_undefined" and payload and payload.startswith('"'):
                name = payload[1:-1]
                if 0 < ln <= len(src_lines):
                    seg = src_lines[ln - 1][col:col + len(name)]
                    if seg.upper() == name.upper():
                        name = seg
                    else:
                        name = name.lower()
            toks.append(Tok(ln, col, typ, name))
    return toks


def elementize(text, files=None):
    """-> (tokens, output, aborted). The elementize pass exits 1 with
    `LOOP EXCEEDED EMPTY BUFFER` AFTER a complete token dump: that status is ignored
    (design 1.2 b / 4.3); the log is what is read. `files` are the stub files the
    block's #include / FILE / OBJ lines need (the pass reads them too)."""
    text = with_final_newline(text)
    with tempfile.TemporaryDirectory(dir=tmp_root()) as d:
        with open(os.path.join(d, "el.spin2"), "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
        for name, content in (files or {}).items():
            p = safe_join(d, name)
            if p is not None:
                os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(p, "w", encoding="utf-8", newline="") as fh:
                    fh.write(content)
        rc, out = run_cmd(["pnut-ts", "--pass", "elementize", "--log", "elementizer", "--", "el.spin2"],
                          cwd=d, timeout=ELEMENTIZE_TIMEOUT)
    toks = parse_elementizer_log(out, text.split("\n"))
    aborted = rc == -9 or (not toks and "type_end_file" not in out)
    return toks, out, aborted


def has_type_debug(toks):
    return any(t.typ == "type_debug" for t in toks)


def needs_debug(text, files=None):
    """6: -d iff the wrapped block holds a type_debug token. The substring test is
    a SOUND pre-filter (a type_debug token has to spell the word), it only spares
    the elementize pass where DEBUG cannot be present."""
    if "debug" not in text.lower():
        return False
    toks, _out, _ab = elementize(text, files)
    return has_type_debug(toks)


def code_bearing(toks):
    """Net 2: does the compiler class this string as code-bearing? (3.1)"""
    by_line = defaultdict(list)
    for t in toks:
        by_line[t.line].append(t)
    for _ln, ts in by_line.items():
        ts = sorted([t for t in ts if t.typ != "type_end"], key=lambda t: t.col)
        i = 0
        while i < len(ts) and ts[i].typ == "type_asm_cond":
            i += 1
        if i < len(ts) and ts[i].typ in OPEN_TYPES:
            return True
        for j, t in enumerate(ts):
            if t.typ == "type_assign":
                return True
            if t.typ == "type_equal" and j > 0 and ts[j - 1].typ == "type_op":
                return True  # compound assignment: `x += 1`
    return False


# ================================================================== the finder

class Cand:
    __slots__ = ("file", "addr", "fp", "text", "line", "key", "style", "net", "multi", "debug")

    def __init__(self, file, addr, text, line, key, style, net):
        self.file, self.addr, self.text, self.line = file, addr, text, line
        self.key, self.style, self.net = key, style, net
        self.fp = fingerprint(text)
        self.multi = len([l for l in text.splitlines() if l.strip()]) >= 2
        self.debug = bool(re.search(r"\bdebug\s*\(", text, re.I))


def fingerprint(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def fmt_path(path):
    out = ""
    for p in path:
        if isinstance(p, int):
            out += "[%d]" % p
        elif re.fullmatch(r"[A-Za-z0-9_-]+", p):
            out += ("." if out else "") + p
        else:
            out += "[%s]" % json.dumps(p)
    return out


def walk(node, path, key, items, prefix, active):
    if id(node) in active:
        return
    active = active | {id(node)}
    if isinstance(node, yaml.MappingNode):
        for k, v in node.value:
            kn = k.value if isinstance(k, yaml.ScalarNode) else "?"
            walk(v, path + [kn], kn, items, prefix, active)
    elif isinstance(node, yaml.SequenceNode):
        for i, v in enumerate(node.value):
            walk(v, path + [i], key, items, prefix, active)
    elif isinstance(node, yaml.ScalarNode) and node.tag.endswith(":str"):
        if node.value.strip():
            items.append((prefix + (fmt_path(path) or "<root>"), key, node.value,
                          node.start_mark.line + 1, node.style or ""))


def scan_file(path, rel):
    try:
        with open(path, encoding="utf-8") as fh:
            docs = list(yaml.compose_all(fh))
    except Exception as e:  # noqa: BLE001 -- any parse failure means "cannot audit"
        raise CannotAudit("YAML parse failure: %s: %s: %s" % (
            rel, e.__class__.__name__, str(e).splitlines()[0] if str(e) else "")) from None
    live = [(i, d) for i, d in enumerate(docs, 1) if d is not None]
    items = []
    for i, d in live:
        walk(d, [], None, items, ("#%d:" % i) if len(live) > 1 else "", frozenset())
    return items


def load_code_keys(root):
    p = os.path.join(root, MANIFEST_DIR, CODE_KEYS_FILE)
    try:
        with open(p, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        keys = data["code_keys"]
        if not isinstance(keys, list) or not all(isinstance(k, str) for k in keys):
            raise ValueError("code_keys must be a list of strings")
    except Exception as e:  # noqa: BLE001
        raise CannotAudit("manifest unreadable: %s (%s)" % (p, e)) from None
    return set(keys)


def kb_files(root):
    base = os.path.join(root, KB_DIR)
    if not os.path.isdir(base):
        raise CannotAudit("KB tree not found: %s (run from the repo root)" % KB_DIR)
    out = []
    for dp, dn, fn in os.walk(base):
        dn[:] = sorted(d for d in dn if not d.startswith("."))
        for f in sorted(fn):
            if f.endswith(".yaml"):
                out.append(os.path.relpath(os.path.join(dp, f), base).replace(os.sep, "/"))
    return out


def find_candidates(root, rels, code_keys):
    """-> ({rel: [Cand]}, census dict). Net 1 + net 2 (3.1)."""
    base = os.path.join(root, KB_DIR)
    per_file = {}
    pending = []  # net-2 jobs: (rel, tuple(item))
    census = Counter()
    host_keys = set()
    for rel in rels:
        p = os.path.join(base, rel)
        if not os.path.isfile(p):
            per_file[rel] = []
            continue
        census["files"] += 1
        items = scan_file(p, rel)
        cs = []
        for addr, key, value, line, style in items:
            if key in code_keys:
                cs.append(Cand(rel, addr, value, line, key, style, "key"))
            elif len([l for l in value.splitlines() if l.strip()]) >= 2:
                pending.append((rel, (addr, key, value, line, style)))
        per_file[rel] = cs
    aborted = 0
    if pending:
        with cf.ThreadPoolExecutor(max_workers=NWORK) as ex:
            results = list(ex.map(lambda pj: elementize(pj[1][2]), pending))
        for (rel, (addr, key, value, line, style)), (toks, _out, ab) in zip(pending, results):
            if ab:
                aborted += 1
            if code_bearing(toks):
                per_file[rel].append(Cand(rel, addr, value, line, key, style, "shape"))
    for rel, cs in per_file.items():
        cs.sort(key=lambda c: (c.line, c.addr))
    allc = [c for cs in per_file.values() for c in cs]
    census["candidates"] = len(allc)
    census["files_with_candidates"] = len({c.file for c in allc})
    census["net_key"] = sum(1 for c in allc if c.net == "key")
    census["net_shape_only"] = sum(1 for c in allc if c.net == "shape")
    census["key_single_line"] = sum(1 for c in allc if c.net == "key" and not c.multi)
    census["key_multi_line"] = sum(1 for c in allc if c.net == "key" and c.multi)
    census["multi_line_candidates"] = sum(1 for c in allc if c.multi)
    census["multi_line_files"] = len({c.file for c in allc if c.multi})
    census["multi_line_with_debug"] = sum(1 for c in allc if c.multi and c.debug)
    census["multi_line_under_code_key"] = sum(1 for c in allc if c.multi and c.key in code_keys)
    census["multi_line_other_key"] = sum(1 for c in allc if c.multi and c.key not in code_keys)
    census["distinct_host_keys"] = len({c.key for c in allc if c.key})
    census["distinct_host_keys_multi_line"] = len({c.key for c in allc if c.multi and c.key})
    census["multi_strings_elementized"] = len(pending)
    census["elementize_aborted"] = aborted
    return per_file, dict(census)


# ============================================================ manifest + reconcile

def parse_assume(s):
    """-> dict(kind, ...) or None when malformed."""
    if not isinstance(s, str):
        return None
    m = re.fullmatch(r"(%s)" % NAME_RE, s)
    if m:
        return {"kind": "var", "name": s, "raw": s}
    m = re.fullmatch(r"(%s)=con" % NAME_RE, s)
    if m:
        return {"kind": "con", "name": m.group(1), "raw": s}
    m = re.fullmatch(r"(%s)\(\)(?:->(\d+))?(?:/(\d+))?" % NAME_RE, s)
    if m:
        return {"kind": "stub", "name": m.group(1), "nret": int(m.group(2) or 0),
                "nparam": int(m.group(3) or 0), "raw": s}
    m = re.fullmatch(r"(%s)\.(%s)\((\d+)\)" % (NAME_RE, NAME_RE), s)
    if m:
        return {"kind": "objm", "inst": m.group(1), "name": m.group(2), "n": int(m.group(3)), "raw": s}
    m = re.fullmatch(r"file:(.+)", s)
    if m:
        return {"kind": "file", "name": m.group(1), "raw": s}
    return None


def validate_entry(e, where):
    errs = []
    if not isinstance(e, dict):
        return ["%s: entry is not a mapping" % where]
    for k in e:
        if k not in ENTRY_KEYS:
            errs.append("%s: unknown key %r" % (where, k))
    if not isinstance(e.get("at"), str) or not e.get("at"):
        errs.append("%s: `at` must be a non-empty string" % where)
    fp = e.get("fp")
    if not isinstance(fp, str) or not re.fullmatch(r"[0-9a-f]{16}", fp):
        errs.append("%s: `fp` must be a quoted 16-hex-digit string" % where)
    c = e.get("compile")
    if c not in CLASSES:
        errs.append("%s: `compile` must be one of %s" % (where, "|".join(CLASSES)))
        return errs
    if c in ("never", "not-code") and not (isinstance(e.get("reason"), str) and e["reason"].strip()):
        errs.append("%s: `reason` is required for %s" % (where, c))
    wrap = e.get("wrap")
    if c in ("fragment", "never"):
        if wrap not in WRAPS:
            errs.append("%s: `wrap` must be one of %s" % (where, "|".join(WRAPS)))
    elif wrap is not None and c == "program":
        errs.append("%s: a program compiles as shown: no `wrap`" % where)
    assumes = e.get("assumes", [])
    if not isinstance(assumes, list):
        errs.append("%s: `assumes` must be a list" % where)
    else:
        if c in ("program",) and assumes:
            errs.append("%s: a program compiles as shown: `assumes` must be empty" % where)
        for a in assumes:
            if parse_assume(a) is None:
                errs.append("%s: malformed assumes entry %r" % (where, a))
    if c == "never":
        fa = e.get("fails_at")
        if not (isinstance(fa, int) and not isinstance(fa, bool) and fa >= 1):
            errs.append("%s: `fails_at` (block-relative line, >= 1) is required for never" % where)
    elif "fails_at" in e:
        errs.append("%s: `fails_at` is for never only" % where)
    if "spin2_version" in e:
        v = e["spin2_version"]
        if c not in ("fragment", "never"):
            errs.append("%s: `spin2_version` is for wrapped blocks only (a program never gets a directive)" % where)
        elif not (isinstance(v, int) and not isinstance(v, bool) and v > 0):
            errs.append("%s: `spin2_version` must be a positive integer" % where)
    if "with" in e:
        w = e["with"]
        if c not in ("fragment", "never"):
            errs.append("%s: `with` is for wrapped blocks only" % where)
        elif not (isinstance(w, list) and all(isinstance(x, str) for x in w)):
            errs.append("%s: `with` must be a list of addresses" % where)
    if "finding" in e and not isinstance(e["finding"], str):
        errs.append("%s: `finding` must be a string" % where)
    return errs


def load_manifest(root, only=None):
    """-> {rel: [entry dict]} for every sidecar (or just `only`). Malformed ->
    CannotAudit (the manifest is unreadable)."""
    base = os.path.join(root, MANIFEST_DIR)
    if not os.path.isdir(base):
        raise CannotAudit("manifest tree not found: %s" % MANIFEST_DIR)
    rels = []
    for dp, dn, fn in os.walk(base):
        dn[:] = sorted(d for d in dn if not d.startswith("."))
        for f in sorted(fn):
            if f.endswith(".yaml"):
                rel = os.path.relpath(os.path.join(dp, f), base).replace(os.sep, "/")
                if rel != CODE_KEYS_FILE:
                    rels.append(rel)
    out, errs = {}, []
    for rel in rels:
        if only is not None and rel not in only:
            continue
        try:
            with open(os.path.join(base, rel), encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
        except Exception as e:  # noqa: BLE001
            errs.append("%s: %s" % (rel, e.__class__.__name__))
            continue
        blocks = (data or {}).get("blocks") if isinstance(data, dict) or data is None else None
        if blocks is None:
            blocks = []
        if not isinstance(blocks, list):
            errs.append("%s: `blocks` must be a list" % rel)
            continue
        seen = set()
        for i, e in enumerate(blocks):
            errs.extend(validate_entry(e, "%s blocks[%d]" % (rel, i)))
            if isinstance(e, dict) and e.get("at") in seen:
                errs.append("%s blocks[%d]: duplicate `at` %r" % (rel, i, e.get("at")))
            if isinstance(e, dict):
                seen.add(e.get("at"))
        out[rel] = blocks
    if errs:
        raise CannotAudit("manifest unreadable: " + "; ".join(errs[:12]) +
                          (" (+%d more)" % (len(errs) - 12) if len(errs) > 12 else ""))
    return out


class Rec:
    """One reconciled pair (3.3)."""
    __slots__ = ("state", "cand", "entry", "index")

    def __init__(self, state, cand, entry, index=None):
        self.state, self.cand, self.entry, self.index = state, cand, entry, index


def reconcile(cands, entries):
    """-> (recs, orphan entries). Fingerprint first; the path settles ties."""
    recs = []
    free_c = list(range(len(cands)))
    free_e = list(range(len(entries)))
    # 1. fp and at both current
    for ei in list(free_e):
        for ci in list(free_c):
            if entries[ei]["at"] == cands[ci].addr and entries[ei]["fp"] == cands[ci].fp:
                recs.append(Rec("MATCH", cands[ci], entries[ei], ei))
                free_e.remove(ei)
                free_c.remove(ci)
                break
    # 2. fp found at a different path (fp first)
    for ei in list(free_e):
        for ci in list(free_c):
            if entries[ei]["fp"] == cands[ci].fp:
                recs.append(Rec("MOVED", cands[ci], entries[ei], ei))
                free_e.remove(ei)
                free_c.remove(ci)
                break
    # 3. same at, new fp
    for ei in list(free_e):
        for ci in list(free_c):
            if entries[ei]["at"] == cands[ci].addr:
                recs.append(Rec("CHANGED", cands[ci], entries[ei], ei))
                free_e.remove(ei)
                free_c.remove(ci)
                break
    for ci in free_c:
        recs.append(Rec("UNCLASSIFIED", cands[ci], None))
    orphans = [(ei, entries[ei]) for ei in free_e]
    return recs, orphans


# ============================================================ wrappers (4.2, 4.4)

class Built:
    pass


def dedent_lines(text):
    return textwrap.dedent(text).rstrip("\n").split("\n")


def count_args(s, pos):
    """Number of top-level arguments of the call whose '(' is s[pos]."""
    depth, n, seen, i, instr = 0, 0, False, pos, False
    while i < len(s):
        ch = s[i]
        if instr:
            if ch == '"':
                instr = False
        elif ch == '"':
            instr = True
            seen = True
        elif ch in "([{":
            depth += 1
            if depth > 1:
                seen = True
        elif ch in ")]}":
            depth -= 1
            if depth == 0:
                return (n + 1) if seen else 0
        elif ch == "," and depth == 1:
            n += 1
            seen = True
        elif not ch.isspace() and depth >= 1:
            seen = True
        i += 1
    return (n + 1) if seen else 0


def obj_decls(text):
    """{instance(lower): literal} from the OBJ sections of `text`."""
    out, inobj = {}, False
    for line in text.split("\n"):
        m = re.match(r"(CON|VAR|OBJ|PUB|PRI|DAT)\b(.*)$", line, re.I)
        rest = line
        if m:
            inobj = m.group(1).upper() == "OBJ"
            rest = m.group(2)
        if inobj:
            m2 = re.match(r"\s*(%s)\s*(?:\[[^\]]*\])?\s*:\s*\"([^\"]+)\"" % NAME_RE, rest)
            if m2:
                out[m2.group(1).lower()] = m2.group(2)
    return out


def obj_filename(lit):
    return lit if re.search(r"\.spin2?$", lit, re.I) else lit + ".spin2"


def build(wrap, body, assumes, version=None, withs=(), append_pub=False):
    """The text the gate compiles, with the line map needed to read an error."""
    b = Built()
    b.error = None
    b.files = {}
    b.decl = {}
    b.wrap = wrap
    if wrap is None:  # a program: the block, byte for byte (plus a final newline, see with_final_newline)
        b.text = with_final_newline(body)
        b.src_lines = body.split("\n")
        b.segs = [("body", None, 1, len(b.src_lines))]
        return b
    parsed = [parse_assume(a) for a in assumes]
    lines, segs = [], []

    def add(kind, label, ls):
        s = len(lines) + 1
        lines.extend(ls)
        segs.append((kind, label, s, len(lines)))

    def adddecl(text, name, kind):
        lines.append(text)
        b.decl[len(lines)] = (name, kind)

    inline = wrap == "pasm2-inline"
    bl = dedent_lines(body)
    b.src_lines = bl
    if version:
        add("wrap", "version", ["{Spin2_v%d}" % version])
    for label, t in withs:
        add("with", label, dedent_lines(t))
    ind = lambda n: ["%s%s" % (" " * n, l) if l.strip() else l for l in bl]  # noqa: E731
    if wrap == "spin2-top":
        add("body", None, bl)
        if append_pub:
            add("wrap", "pub", ["PUB __kbgate()"])
    elif wrap == "spin2-method":
        add("wrap", "head", ["PUB __kbgate()"])
        add("body", None, ind(2))
    elif wrap in ("pasm2-dat", "pasm2-hub"):
        add("wrap", "head", ["DAT", "\t\torg\t0" if wrap == "pasm2-dat" else "\t\torgh"])
        add("body", None, bl)
    elif inline:
        locs = [p["name"] for p in parsed if p and p["kind"] == "var"]
        add("wrap", "head", ["PUB __kbgate()" + (" | " + ", ".join(locs) if locs else ""), "  org"])
        add("body", None, ind(4))
        add("wrap", "tail", ["  end"])
    # trailing declarations, one per line (4.3 collision attribution)
    varn = [p for p in parsed if p and p["kind"] == "var"] if not inline else []
    conn = [p for p in parsed if p and p["kind"] == "con"]
    stubs = [p for p in parsed if p and p["kind"] == "stub"]
    if varn:
        add("wrap", "hdr", ["", "DAT"])
        for p in varn:
            adddecl("%s\tlong\t0" % p["name"], p["raw"], "var")
    if conn:
        add("wrap", "hdr", ["", "CON"])
        for p in conn:
            adddecl("%s = 0" % p["name"], p["raw"], "con")
    if stubs:
        add("wrap", "hdr", [""])
        for p in stubs:
            params = ", ".join("p%d" % i for i in range(1, p["nparam"] + 1))
            rets = ", ".join("r%d" % i for i in range(1, p["nret"] + 1))
            adddecl("PRI %s(%s)%s" % (p["name"], params, (" : " + rets) if rets else ""), p["raw"], "stub")
    b.text = "\n".join(lines) + "\n"
    # stub objects and files (generated into the compile directory)
    objm = [p for p in parsed if p and p["kind"] == "objm"]
    if objm:
        omap = obj_decls(b.text)
        byfile = defaultdict(dict)
        for p in objm:
            lit = omap.get(p["inst"].lower())
            if lit is None:
                b.error = "assumes %r but the block declares no OBJ instance %r" % (p["raw"], p["inst"])
                continue
            meths = byfile[obj_filename(lit)]
            k = p["name"].lower()  # Spin2 names are case-insensitive: one stub method per name
            if k not in meths or meths[k][1] < p["n"]:
                meths[k] = (p["name"], p["n"])
        for fn, meths in byfile.items():
            b.files[fn] = "".join(
                "PUB %s(%s) : r\n" % (m, ", ".join("p%d" % i for i in range(1, n + 1)))
                for m, n in meths.values())
    for p in parsed:
        if p and p["kind"] == "file":
            b.files.setdefault(p["name"], "")
    b.segs = segs
    return b


def locate(b, efile, eline):
    """Where an error line falls: ('body', n) | ('with', label, n) | ('decl', name) |
    ('wrap', label) | ('other', file)."""
    if efile != MAIN_NAME:
        return ("other", efile)
    if eline in b.decl:
        return ("decl", b.decl[eline][0])
    for kind, label, s, e in b.segs:
        if s <= eline <= e:
            if kind == "body":
                return ("body", eline - s + 1)
            if kind == "with":
                return ("with", label, eline - s + 1)
            return ("wrap", label)
    return ("wrap", "eof")


class CRes:
    __slots__ = ("ok", "efile", "eline", "emsg", "raw", "harness")

    def __init__(self, ok, efile=None, eline=None, emsg="", raw="", harness=False):
        self.ok, self.efile, self.eline, self.emsg, self.raw, self.harness = ok, efile, eline, emsg, raw, harness


def safe_join(d, rel):
    p = os.path.normpath(os.path.join(d, rel))
    if not (p == d or p.startswith(d + os.sep)):
        return None
    return p


def compile_built(b, dbg):
    if b.error:
        return CRes(False, emsg=b.error, harness=True)
    with tempfile.TemporaryDirectory(dir=tmp_root()) as d:
        with open(os.path.join(d, MAIN_NAME), "w", encoding="utf-8", newline="") as fh:
            fh.write(b.text)
        for name, content in b.files.items():
            p = safe_join(d, name)
            if p is None:
                return CRes(False, emsg="stub file %r escapes the compile directory" % name, harness=True)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8", newline="") as fh:
                fh.write(content)
        cmd = ["pnut-ts", "-q"] + (["-d"] if dbg else []) + [MAIN_NAME]
        rc, out = run_cmd(cmd, cwd=d)
    if rc == 0:
        return CRes(True, raw=out)
    m = ERR_RE.search(out)
    if m:
        return CRes(False, efile=m.group(1).strip(), eline=int(m.group(2)), emsg=m.group(3).strip(), raw=out)
    tail = out.strip().splitlines()[-1] if out.strip() else "(no output)"
    return CRes(False, emsg="no parseable compiler error (rc=%d): %s" % (rc, tail), raw=out, harness=True)


# ============================================================ gate: assert a class

class Verdict:
    __slots__ = ("kind", "detail", "echo")

    def __init__(self, kind, detail, echo=None):
        self.kind, self.detail, self.echo = kind, detail, echo


def describe(b, res, cand, withlabels=()):
    """Human reading of a compile error + the source line to echo."""
    if res.eline is None:
        return res.emsg, None, ("harness",)
    loc = locate(b, res.efile, res.eline)
    if loc[0] == "body":
        n = loc[1]
        extra = ""
        if cand is not None and cand.style == "|":
            extra = " (YAML line %d)" % (cand.line + n)
        echo = b.src_lines[n - 1] if 0 < n <= len(b.src_lines) else None
        return "block line %d%s: %s" % (n, extra, res.emsg), echo, loc
    if loc[0] == "with":
        return "prerequisite block %s line %d: %s" % (loc[1], loc[2], res.emsg), None, loc
    if loc[0] == "decl":
        return "inside the wrapper's declaration of %s: %s" % (loc[1], res.emsg), None, loc
    if loc[0] == "other":
        return "inside %s: %s" % (loc[1], res.emsg), None, loc
    return "inside the wrapper (%s, line %s): %s" % (loc[1], res.eline, res.emsg), None, loc


def at_eof(b, res):
    """An error the compiler reports one line past the end of the file: it checks the
    file as a whole there (`No PUB method or DAT block found`, and for an OBJ-only
    file `Expected a unique object name`). spin2-top then appends `PUB __kbgate()`
    and compiles again."""
    return res.efile == MAIN_NAME and res.eline is not None and res.eline > b.text.count("\n")


def assert_entry(cand, entry, withs):
    """-> None when the block holds its declared class, else a Verdict."""
    cls = entry["compile"]
    if cls == "not-code":
        return None
    wrap = None if cls == "program" else entry["wrap"]
    assumes = [] if cls == "program" else list(entry.get("assumes", []))
    version = None if cls == "program" else entry.get("spin2_version")
    b = build(wrap, cand.text, assumes, version, withs)
    dbg = needs_debug(b.text, b.files)
    res = compile_built(b, dbg)
    if not res.ok and wrap == "spin2-top" and at_eof(b, res):
        b = build(wrap, cand.text, assumes, version, withs, append_pub=True)
        res = compile_built(b, dbg)
    if cls in ("program", "fragment"):
        if res.ok:
            return None
        detail, echo, _loc = describe(b, res, cand)
        return Verdict("FAIL", detail, echo)
    # never: asserted to fail, at fails_at
    if res.ok:
        return Verdict("NEVER-COMPILES", "expected to fail at block line %d; it compiles" % entry["fails_at"])
    detail, echo, loc = describe(b, res, cand)
    if loc[0] == "body" and loc[1] == entry["fails_at"]:
        return None
    return Verdict("NEVER-WRONG-REASON",
                   "expected to fail at block line %d; %s" % (entry["fails_at"], detail), echo)


# ============================================================ the proposer (4.3)

def uniq(msg):
    return any(m in msg for m in UNIQUE_MARKERS)


def fmt_decl(d):
    if d["kind"] == "var":
        return d["name"]
    if d["kind"] == "con":
        return d["name"] + "=con"
    return "%s()->%d/%d" % (d["name"], d["nret"], d["nparam"])


def stub_for_missing(body, missing, extra):
    """The assumes entries that supply a file the compiler could not find."""
    omap = obj_decls(body)
    want = missing.lower()
    insts = [i for i, lit in omap.items() if obj_filename(lit).lower() == want]
    uses = {}  # (inst, method lower) -> [method, max args]
    for inst in insts:
        for m in re.finditer(r"\b%s\s*(?:\[[^\]]*\])?\s*\.\s*(%s)\s*(\()?" % (re.escape(inst), NAME_RE),
                             body, re.I):
            n = count_args(body, m.end() - 1) if m.group(2) else 0
            k = (inst, m.group(1).lower())
            if k not in uses:
                uses[k] = [m.group(1), n]
            else:
                uses[k][1] = max(uses[k][1], n)
    if insts and not uses:
        # an object file must hold at least one method: ask for the inert one
        uses[(insts[0], "__kbstub")] = ["__kbstub", 0]
    new = []
    for (inst, _l), (meth, n) in uses.items():
        a = "%s.%s(%d)" % (inst, meth, n)
        if a not in extra:
            new.append(a)
    if new:
        return new
    if insts:
        return []
    a = "file:%s" % missing
    return [] if a in extra else [a]


def harness(body, wrap, exclude=frozenset(), seed_dbg=None):
    """Propose the context for one block under one wrap. Returns a dict:
    result PASS | FAIL | HARNESS, assumes, flagged, dropped, version, append_pub,
    compiles, error."""
    st = {"version": None, "append_pub": False, "extra": [], "decls": [], "dropped": [],
          "known": False, "info": {}}
    compiles = 0
    dbg = None
    last = None
    maxit = 12
    it = 0
    while it < maxit:
        it += 1
        assumes = [fmt_decl(d) for d in st["decls"]] + st["extra"]
        b = build(wrap, body, assumes, st["version"], (), st["append_pub"])
        if dbg is None:
            d0 = build(wrap, body, [], st["version"], (), st["append_pub"])
            dbg = needs_debug(d0.text, d0.files)
        res = compile_built(b, dbg)
        compiles += 1
        last = (b, res)

        def result(kind):
            return {"result": kind, "assumes": assumes, "dropped": list(st["dropped"]),
                    "flagged": [fmt_decl(d) for d in st["decls"] if d["kind"] == "stub"] + list(st["extra"]),
                    "version": st["version"], "append_pub": st["append_pub"], "compiles": compiles,
                    "error": describe(b, res, None)[0] if not res.ok else None,
                    "names": sorted(st["info"])}
        if res.ok:
            return result("PASS")
        if res.harness or res.eline is None:
            return result("HARNESS")
        msg = res.emsg
        loc = locate(b, res.efile, res.eline)
        # (a) fixes the compiler itself names
        if wrap == "spin2-top" and not st["append_pub"] and at_eof(b, res):
            st["append_pub"] = True
            maxit += 1
            continue
        m = re.search(r"requires \{Spin2_v(\d+)\}", msg)
        if m and st["version"] is None:
            st["version"] = int(m.group(1))
            maxit += 1
            continue
        m = re.match(r"Cannot find (.+?)\s*$", msg) or re.search(r"File \[(.+?)\] not found", msg)
        if m:
            new = stub_for_missing(body, m.group(1), st["extra"])
            if new:
                st["extra"].extend(new)
                maxit += 1
                continue
        # (b) ask the compiler which names are undeclared
        if not st["known"]:
            base = build(wrap, body, st["extra"], st["version"], (), st["append_pub"])
            toks, out, _ab = elementize(base.text, base.files)
            undef = [t for t in toks if t.typ == "type_undefined"]
            # Self-check (4.3): a log that names nothing while the compiler says
            # `Undefined symbol` means the debug-log format changed. One legitimate
            # source of an unnameable undefined symbol exists: a `.local` label
            # reference lexes as type_dot + a keyword-class token, never type_undefined,
            # so a log that holds a type_dot is not evidence of a format change.
            if msg.startswith("Undefined symbol") and not undef and (
                    not toks or not any(t.typ == "type_dot" for t in toks)):
                raise CannotAudit("proposer self-check: the compiler reported `Undefined symbol` but the "
                                  "elementizer log holds no type_undefined token -- the debug-log format "
                                  "changed (design 4.3 / 11 Q4)")
            body_start = next((s for k, _l, s, _e in base.segs if k == "body"), 1)
            body_end = next((e for k, _l, _s, e in base.segs if k == "body"), 0)
            omap = obj_decls(base.text)
            info = {}
            order = []
            for i, t in enumerate(toks):
                if t.typ != "type_undefined" or not (body_start <= t.line <= body_end):
                    continue
                if i > 0 and toks[i - 1].typ == "type_dot":
                    continue  # member of an object: not an operand
                key = t.name.lower()
                if key in exclude or key == "__kbgate":
                    continue
                nxt = toks[i + 1] if i + 1 < len(toks) else None
                d = info.get(key)
                if d is None:
                    d = {"name": t.name, "lines": set(), "callee": False, "nparam": 0}
                    info[key] = d
                    order.append(key)
                d["lines"].add(t.line - body_start + 1)
                if nxt is not None and nxt.typ == "type_left" and nxt.line == t.line:
                    d["callee"] = True
                    srcl = base.text.split("\n")[t.line - 1]
                    d["nparam"] = max(d["nparam"], count_args(srcl, t.col + len(t.name)))
            st["info"] = info
            st["known"] = True
            for key in order:
                d = info[key]
                if d["callee"]:
                    st["decls"].append({"name": d["name"], "kind": "stub", "nret": 1, "nparam": d["nparam"]})
                elif key in omap:
                    continue  # an OBJ instance the block declares itself
                else:
                    st["decls"].append({"name": d["name"], "kind": "var"})
            if st["decls"]:
                maxit = max(maxit, 2 * len(st["decls"]) + 8)
                continue
        # (c)-(f) read the error by what it attributes to
        if loc[0] == "decl":
            lname = loc[1]
            gone = [d for d in st["decls"] if fmt_decl(d) == lname]
            if gone and uniq(msg):
                st["decls"].remove(gone[0])
                st["dropped"].append(gone[0]["name"])
                continue
            return result("HARNESS")
        if loc[0] == "body":
            n = loc[1]
            here = [d for d in st["decls"] if n in st["info"].get(d["name"].lower(), {"lines": ()})["lines"]]
            if uniq(msg):
                if here:
                    for d in here:
                        st["decls"].remove(d)
                        st["dropped"].append(d["name"])
                    continue
                return result("FAIL")
            movable = [d for d in here if d["kind"] == "var"]
            if movable:
                for d in movable:
                    d["kind"] = "con"
                continue
            return result("FAIL")
        if loc[0] == "with":
            return result("FAIL")
        return result("HARNESS")
    b, res = last
    return {"result": "HARNESS", "assumes": [fmt_decl(d) for d in st["decls"]] + st["extra"],
            "dropped": list(st["dropped"]), "flagged": [], "version": st["version"],
            "append_pub": st["append_pub"], "compiles": compiles,
            "error": "loop bound reached (last: %s)" % describe(b, res, None)[0], "names": []}


def shape_order(toks):
    """Wrap order from what the compiler saw in the bare block."""
    top = pasm = False
    for t in toks:
        if t.typ == "type_block" and t.col == 0:
            top = True
        if t.typ in ("type_asm_inst", "type_asm_dir"):
            pasm = True
    if top:
        return ["spin2-top", "pasm2-dat"]
    if pasm:
        return ["pasm2-dat", "pasm2-inline", "spin2-method", "pasm2-hub"]
    return ["spin2-method", "pasm2-dat", "spin2-top"]


def propose_one(cand):
    """-> dict(outcome PASS|FAIL|HARNESS, compile program|fragment|None, ...)."""
    b = build(None, cand.text, [])
    dbg = needs_debug(b.text)
    res = compile_built(b, dbg)
    compiles = 1
    if res.ok:
        return {"outcome": "PASS", "compile": "program", "wrap": None, "assumes": [], "flagged": [],
                "dropped": [], "compiles": compiles, "tried": [("program", "PASS")], "error": None}
    prog_err = describe(b, res, cand)[0]
    toks, _out, _ab = elementize(cand.text)
    tried = [("program", "FAIL")]
    attempts = []
    for wrap in shape_order(toks):
        if wrap == "pasm2-inline":
            pre = harness(cand.text, "pasm2-dat")
            compiles += pre["compiles"]
            h = harness(cand.text, wrap, exclude=frozenset(n.lower() for n in pre["dropped"]))
        else:
            h = harness(cand.text, wrap)
        compiles += h["compiles"]
        tried.append((wrap, h["result"]))
        attempts.append((wrap, h))
        if h["result"] == "PASS":
            return {"outcome": "PASS", "compile": "fragment", "wrap": wrap, "assumes": h["assumes"],
                    "flagged": h["flagged"], "dropped": h["dropped"], "version": h["version"],
                    "append_pub": h["append_pub"], "compiles": compiles, "tried": tried, "error": None}
    real = [(w, h) for w, h in attempts if h["result"] == "FAIL"]
    if real:
        w, h = real[0]
        return {"outcome": "FAIL", "compile": None, "wrap": w, "assumes": h["assumes"], "flagged": h["flagged"],
                "dropped": h["dropped"], "compiles": compiles, "tried": tried,
                "error": "as a program: %s | as %s: %s" % (prog_err, w, h["error"])}
    w, h = attempts[0]
    return {"outcome": "HARNESS", "compile": None, "wrap": w, "assumes": h["assumes"], "flagged": h["flagged"],
            "dropped": h["dropped"], "compiles": compiles, "tried": tried,
            "error": "as a program: %s | as %s: %s" % (prog_err, w, h["error"])}


# ============================================================ evaluate (the gate)

class Problem:
    __slots__ = ("kind", "file", "line", "addr", "cls", "detail", "echo")

    def __init__(self, kind, file, line, addr, cls, detail, echo=None):
        self.kind, self.file, self.line, self.addr = kind, file, line, addr
        self.cls, self.detail, self.echo = cls, detail, echo

    def as_dict(self):
        return {k: getattr(self, k) for k in self.__slots__}


def cls_label(entry):
    c = entry["compile"]
    return c if c in ("program", "not-code") else "%s/%s" % (c, entry["wrap"])


def evaluate(root, files=None, strict=True):
    """The gate. -> dict(problems, counts, census, scope). Raises CannotAudit."""
    check_pnut()
    code_keys = load_code_keys(root)
    kb_all = kb_files(root)
    if files is None:
        manifest = load_manifest(root)
        scope = sorted(set(kb_all) | set(manifest))
    else:
        scope = sorted(set(files))
        manifest = load_manifest(root, only=set(scope))
    per_file, census = find_candidates(root, scope, code_keys)
    if census.get("candidates", 0) == 0 and not any(manifest.get(r) for r in scope):
        raise CannotAudit("nothing audited: zero candidates and zero manifest entries in scope")
    problems, notes = [], []
    jobs = []  # (rec, withs-or-None)
    counts = Counter()
    for rel in scope:
        cands = per_file.get(rel, [])
        entries = manifest.get(rel, [])
        recs, orphans = reconcile(cands, entries)
        byat = {r.entry["at"]: r for r in recs if r.entry is not None}
        for r in recs:
            c = r.cand
            if r.state == "UNCLASSIFIED":
                problems.append(Problem("UNCLASSIFIED", rel, c.line, c.addr, None,
                                        "candidate with no manifest entry"))
                continue
            e = r.entry
            counts[e["compile"]] += 1
            if r.state in ("MOVED", "CHANGED"):
                how = ("fp changed; the carried class is asserted on the new text; run --refresh after review"
                       if r.state == "CHANGED" else "fp found at a different path (was %s); run --refresh" % e["at"])
                if strict:
                    problems.append(Problem("STALE (%s)" % r.state, rel, c.line, c.addr, cls_label(e), how))
                else:  # edit-time: reported, not failed (3.3)
                    notes.append(Problem("STALE (%s)" % r.state, rel, c.line, c.addr, cls_label(e),
                                         how + " (edit-time check: reported, not failed)"))
            withs, bad = [], None
            for w in e.get("with", []) or []:
                tr = byat.get(w)
                if tr is None:
                    bad = "`with` target %s has no matching block" % w
                    break
                withs.append((w, tr.cand.text))
            if bad:
                problems.append(Problem("FAIL", rel, c.line, c.addr, cls_label(e), bad))
                continue
            jobs.append((r, withs))
        for _ei, e in orphans:
            problems.append(Problem("ORPHAN", rel, 0, e["at"], cls_label(e),
                                    "entry whose block is gone; delete it (that records the removal)"))
    with cf.ThreadPoolExecutor(max_workers=NWORK) as ex:
        verdicts = list(ex.map(lambda j: assert_entry(j[0].cand, j[0].entry, j[1]), jobs))
    for (r, _w), v in zip(jobs, verdicts):
        if v is not None:
            c = r.cand
            problems.append(Problem(v.kind, c.file, c.line, c.addr, cls_label(r.entry), v.detail, v.echo))
    problems.sort(key=lambda p: (p.file, p.line, p.addr))
    notes.sort(key=lambda p: (p.file, p.line, p.addr))
    return {"problems": problems, "notes": notes, "counts": dict(counts), "census": census, "scope": scope}


# ============================================================ output

def print_report(rep, mode_label):
    problems = rep["problems"]
    for p in rep.get("notes", []):
        print("%-17s %s:%s  %s  [%s]  %s" % (p.kind, p.file, p.line, p.addr, p.cls, p.detail))
    for p in problems:
        loc = "%s:%s" % (p.file, p.line) if p.line else p.file
        cls = "  [%s]" % p.cls if p.cls else ""
        print("%-17s %s  %s%s  %s" % (p.kind, loc, p.addr, cls, p.detail))
        if p.echo is not None:
            print("%-17s |   %s" % ("", p.echo.strip()))
    c = rep["counts"]
    total = sum(c.values())
    tail = "(%d blocks: %d program, %d fragment, %d never asserted to fail, %d not-code)" % (
        total, c.get("program", 0), c.get("fragment", 0), c.get("never", 0), c.get("not-code", 0))
    if problems:
        kinds = Counter(p.kind.split(" ")[0] for p in problems)
        files = len({p.file for p in problems})
        order = ["FAIL", "NEVER-COMPILES", "NEVER-WRONG-REASON", "STALE", "UNCLASSIFIED", "ORPHAN"]
        parts = ["%d %s" % (kinds[k], k) for k in order if kinds.get(k)]
        print("FAIL: %d problems in %d files -- %s %s" % (len(problems), files, ", ".join(parts), tail))
    else:
        print("PASS: every block holds its declared class %s" % tail)
    print(LEGALITY_NOTE)


def print_census(census):
    c = census
    print("census (finder, real): %d YAML files in scope; %d candidates in %d files "
          "(net 1 code-named key: %d, of which %d single-line; net 2 compiler-recognised shape only: %d)"
          % (c.get("files", 0), c.get("candidates", 0), c.get("files_with_candidates", 0),
             c.get("net_key", 0), c.get("key_single_line", 0), c.get("net_shape_only", 0)))
    print("census: multi-line candidates %d in %d files; %d with debug(; under a code-named key %d, "
          "under another key %d; distinct host keys %d (%d among multi-line)"
          % (c.get("multi_line_candidates", 0), c.get("multi_line_files", 0), c.get("multi_line_with_debug", 0),
             c.get("multi_line_under_code_key", 0), c.get("multi_line_other_key", 0),
             c.get("distinct_host_keys", 0), c.get("distinct_host_keys_multi_line", 0)))
    print("census: %d multi-line strings elementized by the net-2 finder; %d elementize passes aborted early"
          % (c.get("multi_strings_elementized", 0), c.get("elementize_aborted", 0)))


def rep_exit(rep):
    return 1 if rep["problems"] else 0


# ============================================================ propose / refresh / since

def yq(s):
    return s if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.\[\]-]*", s) and s not in ("true", "false", "null", "yes", "no") \
        else json.dumps(s)


def yitem(s):
    """An assumes item as a YAML flow-sequence scalar: quoted unless plainly safe."""
    return s if re.fullmatch(r"[A-Za-z0-9_.()>/=:-]+", s) else json.dumps(s)


def assumes_flow(items):
    return "[%s]" % ", ".join(yitem(a) for a in items)


def entry_text(c, prop):
    out = ["  - at: %s" % yq(c.addr), '    fp: "%s"' % c.fp]
    if prop["compile"] == "program":
        out.append("    compile: program")
    else:
        out.append("    compile: fragment")
        out.append("    wrap: %s" % prop["wrap"])
        if prop["assumes"]:
            out.append("    assumes: %s" % assumes_flow(prop["assumes"]))
        if prop.get("version"):
            out.append("    spin2_version: %d" % prop["version"])
    return "\n".join(out)


def do_propose(root, files):
    check_pnut()
    code_keys = load_code_keys(root)
    scope = files if files is not None else kb_files(root)
    per_file, census = find_candidates(root, sorted(scope), code_keys)
    cands = [c for rel in sorted(per_file) for c in per_file[rel]]
    if not cands:
        raise CannotAudit("nothing audited: zero candidates in scope")
    def safe(c):
        try:
            return propose_one(c)
        except CannotAudit as e:
            raise CannotAudit("%s (at %s:%s %s)" % (e, c.file, c.line, c.addr)) from None
    with cf.ThreadPoolExecutor(max_workers=NWORK) as ex:
        props = list(ex.map(safe, cands))
    n = Counter()
    for c, p in zip(cands, props):
        key = p["outcome"] if p["outcome"] != "PASS" else p["compile"]
        n[key] += 1
        loc = "%s:%s" % (c.file, c.line)
        if p["outcome"] == "PASS":
            fl = ("  FLAGGED for review: %s" % ", ".join(p["flagged"])) if p["flagged"] else ""
            note = []
            if p.get("append_pub"):
                note.append("the gate appends `PUB __kbgate()` itself")
            if p.get("dropped"):
                note.append("block-defined names dropped: %s" % ", ".join(p["dropped"]))
            print("PROPOSE %-9s %s  %s%s%s" % (p["compile"], loc, c.addr, fl,
                                              ("  (" + "; ".join(note) + ")") if note else ""))
            print(entry_text(c, p))
        else:
            print("PROPOSE %-9s %s  %s  %s" % (p["outcome"], loc, c.addr, p["error"]))
    summary = "PROPOSE: %d candidates -- %d program, %d fragment, %d unresolved (FAIL), %d HARNESS" % (
        len(cands), n["program"], n["fragment"], n["FAIL"], n["HARNESS"])
    print(summary)
    print_census(census)
    print("(proposals only: this mode never writes the manifest)")
    print(LEGALITY_NOTE)
    return {"summary": summary, "counts": dict(n), "census": census,
            "proposals": [{"file": c.file, "addr": c.addr, "line": c.line, **{k: v for k, v in p.items()
                           if k != "tried"}} for c, p in zip(cands, props)]}


def sidecar_path(root, rel):
    return os.path.join(root, MANIFEST_DIR, rel)


def rewrite_sidecar(path, edits):
    """Line-level edits keep the sidecar's comments and layout. edits:
    {entry index: {"at":..., "fp":..., "assumes": [...]}}"""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    starts = [i for i, l in enumerate(lines) if re.match(r"\s*-\s+at:", l)]
    for idx, ch in edits.items():
        if idx >= len(starts):
            raise CannotAudit("cannot locate entry %d in %s to refresh" % (idx, path))
        s = starts[idx]
        e = starts[idx + 1] if idx + 1 < len(starts) else len(lines)
        while e > s + 1 and not lines[e - 1].strip():
            e -= 1
        for key in ("at", "fp"):
            if key in ch:
                pat = re.compile(r"^(\s*(?:-\s+)?)%s:.*$" % key)
                val = yq(ch[key]) if key == "at" else '"%s"' % ch[key]
                for i in range(s, e):
                    m = pat.match(lines[i])
                    if m:
                        lines[i] = "%s%s: %s" % (m.group(1), key, val)
                        break
                else:
                    raise CannotAudit("cannot find `%s:` in entry %d of %s" % (key, idx, path))
        if "assumes" in ch:
            val = assumes_flow(ch["assumes"])
            for i in range(s, e):
                m = re.match(r"^(\s+)assumes:.*$", lines[i])
                if m:
                    lines[i] = "%sassumes: %s" % (m.group(1), val)
                    break
            else:
                ind = re.match(r"^(\s*)-", lines[s]).group(1) + "    "
                lines.insert(e, "%sassumes: %s" % (ind, val))
                starts = [i + (1 if i >= e else 0) for i in starts]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(lines))


def do_refresh(root, files, accept):
    check_pnut()
    code_keys = load_code_keys(root)
    scope = sorted(set(files))
    manifest = load_manifest(root, only=set(scope))
    per_file, _census = find_candidates(root, scope, code_keys)
    refused = 0
    changed = 0
    for rel in scope:
        recs, _orph = reconcile(per_file.get(rel, []), manifest.get(rel, []))
        byat = {r.entry["at"]: r for r in recs if r.entry is not None}
        edits = {}
        for r in recs:
            if r.state not in ("MOVED", "CHANGED"):
                continue
            e, c = r.entry, r.cand
            moving = {id(x.entry) for x in recs if x.state in ("MOVED", "CHANGED")}
            holder = [x for x in manifest.get(rel, []) if id(x) not in moving and x["at"] == c.addr]
            if holder:
                refused += 1
                print("REFUSED  %s:%s  %s  the path is held by another entry (fp %s): resolve that ORPHAN "
                      "first (delete it, or hand-edit its `at`)" % (rel, c.line, c.addr, holder[0]["fp"]))
                continue
            withs = [(w, byat[w].cand.text) for w in (e.get("with") or []) if w in byat]
            v = assert_entry(c, e, withs)
            new_assumes = None
            if v is not None and accept and e["compile"] in ("fragment", "never"):
                add = [a for a in accept if a not in e.get("assumes", [])]
                e2 = dict(e)
                e2["assumes"] = list(e.get("assumes", [])) + add
                if add and assert_entry(c, e2, withs) is None:
                    v, new_assumes = None, e2["assumes"]
            if v is not None:
                refused += 1
                print("REFUSED  %s:%s  %s  [%s]  %s -- the carried class no longer holds; not refreshed"
                      % (rel, c.line, c.addr, cls_label(e), v.detail))
                continue
            ch = {"at": c.addr, "fp": c.fp}
            if new_assumes is not None:
                ch["assumes"] = new_assumes
            edits[r.index] = ch
            changed += 1
            print("REFRESHED %s:%s  %s -> %s  fp %s -> %s%s" % (
                rel, c.line, e["at"], c.addr, e["fp"], c.fp,
                ("  assumes += %s" % ", ".join(a for a in new_assumes if a not in e.get("assumes", [])))
                if new_assumes is not None else ""))
        if edits:
            rewrite_sidecar(sidecar_path(root, rel), edits)
    print("%s: %d refreshed, %d refused" % ("FAIL" if refused else "PASS", changed, refused))
    print(LEGALITY_NOTE)
    return 1 if refused else 0


def since_scope(root, rev):
    rc, out = run_cmd(["git", "diff", "--name-only", "%s..HEAD" % rev, "--", KB_DIR, MANIFEST_DIR], cwd=root, timeout=60)
    if rc != 0:
        raise CannotAudit("git diff failed for --since %s: %s" % (rev, out.strip().splitlines()[-1] if out.strip() else ""))
    scope = set()
    for l in out.splitlines():
        l = l.strip().replace(os.sep, "/")
        if l.startswith(KB_DIR.replace(os.sep, "/") + "/") and l.endswith(".yaml"):
            scope.add(l[len(KB_DIR) + 1:])
        elif l.startswith(MANIFEST_DIR.replace(os.sep, "/") + "/") and l.endswith(".yaml"):
            rel = l[len(MANIFEST_DIR) + 1:]
            if rel != CODE_KEYS_FILE:
                scope.add(rel)
    rc, stat = run_cmd(["git", "diff", "--stat", "%s..HEAD" % rev, "--", MANIFEST_DIR], cwd=root, timeout=60)
    return sorted(scope), stat.strip()


def norm_files(root, files):
    out = []
    base = os.path.join(root, KB_DIR)
    for f in files:
        cands = [os.path.join(base, f), os.path.join(root, f), f]
        for p in cands:
            ap = os.path.abspath(p)
            if os.path.isfile(ap) and ap.startswith(os.path.abspath(base) + os.sep):
                out.append(os.path.relpath(ap, base).replace(os.sep, "/"))
                break
        else:
            rel = f.replace(os.sep, "/")
            pre = KB_DIR.replace(os.sep, "/") + "/"
            rel = rel[len(pre):] if rel.startswith(pre) else rel
            if os.path.isfile(os.path.join(root, MANIFEST_DIR, rel)):
                out.append(rel)  # a deleted KB file whose sidecar remains
            else:
                raise CannotAudit("not a KB YAML file: %s" % f)
    return out


# ============================================================ negative controls (7.3)

GOOD_PROG = "CON\n  _clkfreq = 200_000_000\n\nPUB main()\n  pinh(56)\n"
BAD_PROG = "CON\n  _clkfreq = 200_000_000\n  BUTTON = 3\n\nPUB main()\n  DIRL #BUTTON\n"
NC_ROOT_FILES = None


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def nc_yaml(blocks):
    out = ["examples:"]
    for t in blocks:
        out.append("  - code: |")
        out.extend(("      " + l) if l else "" for l in t.rstrip("\n").split("\n"))
    return "\n".join(out) + "\n"


def nc_root(blocks, entries_fn):
    """A synthetic repo: one scratch KB YAML + one scratch sidecar. entries_fn gets the
    real finder's candidates (so every fp is the real one) and returns the sidecar
    entries as dicts."""
    root = tempfile.mkdtemp(dir=tmp_root())
    write(os.path.join(root, KB_DIR, "nc.yaml"), nc_yaml(blocks))
    write(os.path.join(root, MANIFEST_DIR, CODE_KEYS_FILE), "code_keys: [code]\n")
    per_file, _c = find_candidates(root, ["nc.yaml"], {"code"})
    cands = per_file["nc.yaml"]
    ents = entries_fn(cands)
    if ents is not None:
        write(os.path.join(root, MANIFEST_DIR, "nc.yaml"),
              "blocks:\n" + "".join(emit_entry(e) for e in ents))
    return root


def emit_entry(e):
    out = ["  - at: %s\n" % yq(e["at"]), '    fp: "%s"\n' % e["fp"], "    compile: %s\n" % e["compile"]]
    for k in ("wrap", "reason", "fails_at", "spin2_version"):
        if k in e:
            out.append("    %s: %s\n" % (k, json.dumps(e[k]) if isinstance(e[k], str) else e[k]))
    if e.get("assumes"):
        out.append("    assumes: %s\n" % assumes_flow(e["assumes"]))
    return "".join(out)


def ent(c, **kw):
    d = {"at": c.addr, "fp": c.fp}
    d.update(kw)
    return d


def nc_run(blocks, entries_fn, strict=True):
    root = nc_root(blocks, entries_fn)
    rep = evaluate(root, files=None, strict=strict)
    return rep


def nc_summary(rep):
    if not rep["problems"]:
        return "PASS"
    p = rep["problems"][0]
    return "%s (%s)" % (p.kind, p.detail[:100])


def run_negative_controls():
    check_pnut()
    results = []  # (id, description, expected, observed, ok)

    def rec(nid, desc, expected, observed, ok):
        results.append((nid, desc, expected, observed, ok))

    def single(blocks, mk, kinds, strict=True):
        rep = nc_run(blocks, mk, strict)
        got = [p.kind for p in rep["problems"]]
        return rep, got

    # NC1 known-bad program: PASM `DIRL #PIN` written as a Spin2 statement
    rep, got = single([BAD_PROG], lambda cs: [ent(cs[0], compile="program")], None)
    rec(1, "known-bad program (DIRL as a Spin2 statement)", "FAIL", nc_summary(rep), got == ["FAIL"])
    # NC2 known-good program
    rep, got = single([GOOD_PROG], lambda cs: [ent(cs[0], compile="program")], None)
    rec(2, "known-good program", "PASS", nc_summary(rep), got == [])
    # NC3 never that compiles
    rep, got = single([GOOD_PROG], lambda cs: [ent(cs[0], compile="never", wrap="spin2-top", reason="nc", fails_at=3)], None)
    rec(3, "never block that compiles", "NEVER-COMPILES", nc_summary(rep), got == ["NEVER-COMPILES"])
    # NC4 never failing on another line than fails_at (error is on block line 6; fails_at says 4)
    rep, got = single([BAD_PROG], lambda cs: [ent(cs[0], compile="never", wrap="spin2-top", reason="nc", fails_at=4)], None)
    rec(4, "never fails on a line other than fails_at", "NEVER-WRONG-REASON", nc_summary(rep),
        got == ["NEVER-WRONG-REASON"])
    # NC4b (control of NC4's arithmetic): the same block with the RIGHT fails_at must pass
    rep, got = single([BAD_PROG], lambda cs: [ent(cs[0], compile="never", wrap="spin2-top", reason="nc", fails_at=6)], None)
    rec("4b", "never fails exactly at fails_at (the case NC4 must differ from)", "PASS", nc_summary(rep), got == [])
    # NC5 collision shape: own label + method parameters, correct assumes
    frag5 = ("PUB scale(value, factor) : r\n  r := value * factor * gain\n\n"
             "DAT\n  org 0\nloop  add acc, #1\n      djnz cnt, #loop\n")
    rep, got = single([frag5], lambda cs: [ent(cs[0], compile="fragment", wrap="spin2-top",
                                               assumes=["gain", "acc", "cnt"])], None)
    ok5 = got == []
    # the proposer must find exactly this context, with the collisions attributed (4.3)
    root5 = nc_root([frag5], lambda cs: None)
    per, _c = find_candidates(root5, ["nc.yaml"], {"code"})
    prop = propose_one(per["nc.yaml"][0])
    want = {"gain", "acc", "cnt"}
    ok5p = (prop["outcome"] == "PASS" and set(prop["assumes"]) == want and
            {"loop", "value", "factor", "scale"} <= {n.lower() for n in prop["dropped"]})
    rec(5, "fragment defining its own label and parameters, correct assumes (gate + proposer)", "PASS",
        "gate %s; proposer %s assumes=%s dropped=%s" % (nc_summary(rep), prop["outcome"],
                                                        sorted(prop["assumes"]), sorted(prop["dropped"])),
        ok5 and ok5p)
    # NC6 P1 cognew(...) in a fragment, nothing assumed
    rep, got = single(["cognew(@driver, @params)"],
                      lambda cs: [ent(cs[0], compile="fragment", wrap="spin2-method")], None)
    rec(6, "fragment calling P1 cognew(), nothing assumed", "FAIL", nc_summary(rep), got == ["FAIL"])
    # NC7 debug() holding a garbage term
    dbg7 = "PUB main() | x\n  x := 5\n  debug(udec(x), nonsense_token_here(x))\n"
    rep, got = single([dbg7], lambda cs: [ent(cs[0], compile="program")], None)
    rec(7, "debug() holding a garbage term (proves -d is applied)", "FAIL", nc_summary(rep), got == ["FAIL"])
    # NC8 legal low-clock program, no DEBUG
    low8 = "CON\n  _rcslow = TRUE\n\nPUB main()\n  pinh(56)\n"
    rep, got = single([low8], lambda cs: [ent(cs[0], compile="program")], None)
    rec(8, "legal _rcslow program with no DEBUG (proves -d is not blanket)", "PASS", nc_summary(rep), got == [])
    # NC8b (the other side of NC8): the same clock WITH debug() must fail -- its DEBUG can never run (6)
    rep, got = single([low8 + "  debug(udec(1))\n"], lambda cs: [ent(cs[0], compile="program")], None)
    rec("8b", "the same _rcslow program WITH debug() (-d is applied iff type_debug)", "FAIL", nc_summary(rep),
        got == ["FAIL"])
    # NC9 fragment edited to use a new undeclared operand (entry fp is current, assumes stale)
    frag9 = "PUB main()\n  alpha := beta + gamma\n"
    rep, got = single([frag9], lambda cs: [ent(cs[0], compile="fragment", wrap="spin2-top", assumes=["alpha", "beta"])],
                      None)
    rec(9, "fragment uses a new undeclared operand (proves assumes is pinned)", "FAIL", nc_summary(rep),
        got == ["FAIL"])
    # NC9b (the other side of NC9): the same block with the name accepted into assumes passes
    rep, got = single([frag9], lambda cs: [ent(cs[0], compile="fragment", wrap="spin2-top",
                                               assumes=["alpha", "beta", "gamma"])], None)
    rec("9b", "the same fragment with the new name accepted in assumes", "PASS", nc_summary(rep), got == [])
    # NC10 candidate with no entry / stale fp (release) / orphan entry
    rep, got = single([GOOD_PROG, GOOD_PROG.replace("56", "57")],
                      lambda cs: [ent(cs[0], compile="program")], None)
    rec("10a", "candidate with no entry", "UNCLASSIFIED", nc_summary(rep), got == ["UNCLASSIFIED"])
    rep, got = single([GOOD_PROG], lambda cs: [dict(ent(cs[0], compile="program"), fp="0" * 16)], None)
    rec("10b", "entry with stale fp (release mode)", "STALE (CHANGED)", nc_summary(rep), got == ["STALE (CHANGED)"])
    rep2 = nc_run([GOOD_PROG], lambda cs: [dict(ent(cs[0], compile="program"), fp="0" * 16)], strict=False)
    rec("10b'", "the same stale fp at edit time is reported, not failed", "PASS", nc_summary(rep2),
        [p.kind for p in rep2["problems"]] == [])
    rep, got = single([GOOD_PROG], lambda cs: [ent(cs[0], compile="program"),
                                               {"at": "examples[9].code", "fp": "1" * 16, "compile": "program"}], None)
    rec("10c", "orphan entry", "ORPHAN", nc_summary(rep), got == ["ORPHAN"])
    # NC11 pnut-ts replaced by an empty PATH -> exit 2
    root11 = nc_root([GOOD_PROG], lambda cs: [ent(cs[0], compile="program")])
    emptydir = tempfile.mkdtemp(dir=tmp_root())
    env = dict(os.environ, PATH=emptydir)
    p = subprocess.run([sys.executable, os.path.abspath(__file__)], cwd=root11, env=env,
                       capture_output=True, text=True, timeout=120)
    rec(11, "pnut-ts replaced by an empty PATH", "exit 2", "exit %d: %s" % (p.returncode, (p.stdout + p.stderr).strip()[:100]),
        p.returncode == 2)
    ok = all(r[4] for r in results)
    for nid, desc, expected, observed, good in results:
        print("NC%-4s %-4s %s | expected %s | observed %s" % (nid, "ok" if good else "BAD", desc, expected, observed))
    print("NEGATIVE CONTROL: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


# ============================================================ main

def main(argv=None):
    ap = argparse.ArgumentParser(description="ENH-03 KB compile gate (LEGALITY ONLY).", add_help=True)
    ap.add_argument("--files", nargs="+", metavar="F")
    ap.add_argument("--since", metavar="REV")
    ap.add_argument("--propose", action="store_true")
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--accept-assumes", nargs="+", metavar="NAME", default=[])
    ap.add_argument("--negative-control", action="store_true")
    ap.add_argument("--census", action="store_true")
    ap.add_argument("--json", metavar="PATH")
    args = ap.parse_args(argv)
    root = os.getcwd()  # the repo root is the working directory, never the script path
    try:
        if args.negative_control:
            return run_negative_controls()
        if args.refresh:
            if not args.files:
                raise CannotAudit("--refresh needs --files")
            return do_refresh(root, norm_files(root, args.files), args.accept_assumes)
        if args.propose:
            files = norm_files(root, args.files) if args.files else None
            print("pnut-ts: %s (run context; never written to the manifest or the KB)" % pnut_version())
            out = do_propose(root, files)
            if args.json:
                write(args.json, json.dumps(out, indent=1))
            return 0
        if args.census:
            check_pnut()
            code_keys = load_code_keys(root)
            _pf, census = find_candidates(root, kb_files(root), code_keys)
            print_census(census)
            if args.json:
                write(args.json, json.dumps(census, indent=1))
            return 0 if census.get("candidates") else 2
        stat = None
        if args.since:
            files, stat = since_scope(root, args.since)
            strict = True
            if not files:
                raise CannotAudit("nothing audited: no KB or manifest file changed in %s..HEAD" % args.since)
        elif args.files:
            files, strict = norm_files(root, args.files), False
        else:
            files, strict = None, True
        print("pnut-ts: %s (run context; never written to the manifest or the KB)" % (check_pnut() or pnut_version()))
        rep = evaluate(root, files=files, strict=strict)
        if stat:
            print("manifest diff over %s..HEAD (audit every hunk like YAML: into never/not-code, new assumes, deleted entries):\n%s"
                  % (args.since, stat))
        print_census(rep["census"])
        print_report(rep, "")
        if args.json:
            write(args.json, json.dumps({"census": rep["census"], "counts": rep["counts"],
                                         "problems": [p.as_dict() for p in rep["problems"]]}, indent=1))
        return rep_exit(rep)
    except CannotAudit as e:
        print("ERROR: cannot audit -- %s" % e)
        return 2
    finally:
        cleanup_tmp()


if __name__ == "__main__":
    sys.exit(main())
