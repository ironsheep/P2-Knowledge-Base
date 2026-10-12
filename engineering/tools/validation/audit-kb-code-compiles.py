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
      net 3  (S-256) every SINGLE-LINE string scalar under a key of the reviewed list
             kb-compile-manifest/_oneline-code-keys.yaml (`oneline_code_keys: [...]`): real
             one-line programs (`correct: result := value * 2`, `con_symbols: CON _clkfreq =
             ...`) that live under non-code keys. Chosen BY KEY, never by shape: admitting
             every one-line string the compiler classes as code would pull in `syntax:`
             notation and prose. Many will be decided `not-code` (with a reason) or `fragment`.
      net 2  every multi-line string the COMPILER recognises as code-bearing: the
             string is elementized (`pnut-ts --pass elementize --log elementizer`)
             and taken when a line opens with a block keyword, an instruction
             (an `if_*` condition prefix is allowed), an assembler directive,
             DEBUG, or a Spin2 flow-statement token (IF/ELSE/CASE/OTHER/REPEAT and
             the `type_i_*` family: RETURN, ABORT, NEXT/QUIT, built-in method
             statements), or any line holds an assignment operator (`:=`, `+=`, ...).
             An elementize pass that ABORTS (e.g. a missing #INCLUDE file) makes the
             string a candidate: when the compiler cannot tell, the finder includes.
             The compiler's own token TYPES do the recognising: there is no keyword
             spelling list in this script.
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
            fails_at: 3                   # never only: block-relative line (5), or `eof`:
                                          #   the error lands AFTER the block's last line,
                                          #   in wrapper text (tail / past end of file),
                                          #   for whole-file checks the compiler reports
                                          #   one line past EOF (S-150)
            spin2_version: 45             # optional, wraps only: {Spin2_v45} line 1
            with: [examples[0].code]      # optional, wraps only: prepend siblings
            finding: F-381                # optional, reporting only; NEVER changes
                                          #   the verdict (a known-broken block stays
                                          #   program/fragment and stays red)
            bare_const_ok: [NAME]         # optional, with a mandatory `reason:` (D3, below)
    compile:
      program   compiles BYTE FOR BYTE as shown; no wrap, no assumes.
      fragment  compiles inside `wrap` with exactly `assumes` declared.
      never     the KB teaches the compile error: the gate asserts it FAILS at
                `fails_at` (NEVER-COMPILES / NEVER-WRONG-REASON otherwise).
      not-code  prose, notation, shell command, listing... not compiled.
    wrap (4.2):  spin2-top | spin2-method | spin2-method-result | pasm2-dat | pasm2-hub
                 | pasm2-inline
      spin2-method-result  as spin2-method, but the wrapper declares one result
                           (`PUB __kbgate() : __kbres`), for a method BODY that does
                           `return <value>` (spin2-method declares none: S-022)
      spin2-var            `VAR` + the block indented + a trailing `PUB __kbgate()`: for
                           VAR-section declaration lines (`BYTE flag`, `^LONG pValues`,
                           `LONG buf[16]`) shown without their VAR header (S-136)
    assumes (the names the wrap declares, 4.2 / 4.4):
      NAME              operand: trailing `DAT NAME long 0`; for pasm2-inline a
                        LOCAL of the wrapper method (hub DAT longs fail there)
      NAME=con          trailing `CON NAME = 0`
      NAME=con:V        trailing `CON NAME = V` (V an integer, may be negative): for a
                        constant whose VALUE matters, e.g. an array / object count
                        (`pca[NBUS]` needs `NBUS=con:4`; a 0 count is a different error)
      NAME()->R/N       callee stub `PRI NAME(p1..pN) : r1..rR`  (R, N optional)
      OBJ.METHOD(N)     method of a generated stub object; the object FILE is the
                        one the block's own `OBJ OBJ : "file"` line names
      OBJ.METHOD(N)->T  the same, its result typed T (a structure the object exports)
      file:NAME         an empty file NAME in the compile directory (FILE/#include)
      struct:NAME(MEMBERS)       a leading `CON` + `  STRUCT NAME(MEMBERS)` (BEFORE the block:
                                a method header may use the type): a structure type the
                                block uses but does not define (S-123)
      OBJ.struct:NAME(MEMBERS)   a structure the generated stub object OBJ EXPORTS, so the
                                block can say `OBJ.NAME` in a VAR / parameter (the object
                                file gets `CON` + `STRUCT NAME(MEMBERS)`)
      label:NAME        (pasm2-dat / pasm2-hub) a label line `NAME` right AFTER the block: a
      label:.NAME       label the excerpt jumps to but does not define. `.NAME` is a local
                        (PNut accepts a `.local` with no global label above it, so no
                        anchor line is added; probed with the label-less excerpts) (S-198)
      lead:N            (pasm2-dat / pasm2-hub) N `nop` lines BEFORE the block (1..16), for
                        an excerpt whose first line says `$-1` (a relative address) (S-199)
      NAME:TYPE         trailing `VAR` + `  TYPE NAME`: a variable of a declared
                        structure type (TYPE may be `^TYPE` or `OBJ.TYPE`)
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
    --apply DECISIONS.json          write REVIEWED decisions to the sidecars. DECISIONS is a
                                    JSON list of {"file": <kb-relative path, as --propose
                                    prints it>, "at": <address>, "compile": program|fragment|
                                    never|not-code, + optional wrap, assumes, with, fails_at,
                                    reason, finding, spin2_version}. `fp` is computed from the
                                    live candidate (supplying one is refused). ALL-OR-NOTHING:
                                    every decision is validated (validate_entry) before any
                                    file is written; refused, with nothing written, when an
                                    address is not a live candidate, the sidecar already has
                                    an entry there (no overwrite), an address is decided twice,
                                    or an entry is invalid. Then the gate runs on exactly the
                                    touched files and its report is printed. Writes the file
                                    header (LEGALITY ONLY) on a new sidecar; extends an
                                    existing one by appending.
    --negative-control              the synthetic controls (7.3, plus --apply and the
                                    REGISTERED/UNREGISTERED split)
    --census                        the finder's census only (no manifest, no compile)
    --json PATH                     machine-readable result to a scratch path

EXIT (7.2)
    0  every block holds its declared class; nothing stale, unclassified, orphaned
    1  any problem line
    2  cannot audit: pnut-ts not on PATH, KB tree / manifest unreadable, YAML parse
       failure, the proposer self-check, or ZERO candidates ("nothing audited" is
       never a pass); for --apply also an unreadable decisions file
    3  --apply only: the decisions were REFUSED and nothing was written (--apply
       otherwise exits with the gate's code, 0 or 1, on the touched files)

BARE-CONST (D3 / S-389)
    `mov flag, TRUE` assembles (TRUE is just the number -1) but reads the REGISTER at address
    -1 & $1FF instead of loading the value: the author meant `#TRUE`. Legality cannot see it,
    so for every program / fragment / never block that holds its class the built text is
    elementized and, for each `type_asm_inst` line inside the block body (a leading
    `type_asm_cond` skipped), operands D and S are examined, split on top-level `type_comma`.
    An operand that is a single token with NO `type_pound` FAILs (`BARE-CONST`) when
      (a) its type starts `type_con` and the source text at its column is an identifier
          (so `mov x, 5` is not flagged, `mov x, TRUE` is), or
      (b) it is `type_undefined` and its lower-cased name is in the CONSTANT SET: the entry's
          `assumes: NAME=con[:V]` names + names the block's own CON section declares
          (`type_undefined` followed by `type_equal`).
    Directives (`long TRUE`, `res`, `orgh`) are `type_asm_dir`, not instructions, and are not
    examined. Escape: a manifest entry may list `bare_const_ok: [NAME]` with a mandatory
    `reason:` (an intentional read of the register at address NAME). BLIND TO: a constant the
    author declared as a plain operand (`assumes: [limit]` without `=con` -- the manifest SAYS it
    is a register), a constant from an `#include`d file or another object, blocks classed
    `not-code`, the non-PASM Spin2 blocks, and one-liners outside the net. Spin2-side misuse is
    a different class. It does not check that a `#` operand is the RIGHT constant or that the
    value fits 9 bits (the compiler does that).

REGISTERED / UNREGISTERED (reporting only)
    A failing block (FAIL / NEVER-COMPILES / NEVER-WRONG-REASON / BARE-CONST) whose entry carries
    `finding:` is printed `REGISTERED(F-NNN)`; without one, `UNREGISTERED`. The summary
    line counts both, and `--json` carries `finding` and `registered` per problem.
    The exit code is 1 for ANY problem: a finding never changes the verdict (4.1).
    UNCLASSIFIED, STALE and ORPHAN are never REGISTERED.

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
import threading
from collections import Counter, defaultdict

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR: audit-kb-code-compiles: PyYAML is required (import yaml failed)", file=sys.stderr)
    sys.exit(2)


KB_DIR = os.path.join("deliverables", "ai", "P2")
MANIFEST_DIR = os.path.join("engineering", "tools", "validation", "kb-compile-manifest")
CODE_KEYS_FILE = "_code-keys.yaml"
ONELINE_KEYS_FILE = "_oneline-code-keys.yaml"     # net 3 (S-256)
NET_DATA_FILES = (CODE_KEYS_FILE, ONELINE_KEYS_FILE)
MAIN_NAME = "kb.spin2"
WRAPS = ("spin2-top", "spin2-method", "spin2-method-result", "spin2-var", "pasm2-dat", "pasm2-hub",
         "pasm2-inline")
CLASSES = ("program", "fragment", "never", "not-code")
ENTRY_KEYS = {"at", "fp", "compile", "wrap", "assumes", "reason", "fails_at",
              "spin2_version", "with", "finding", "bare_const_ok"}
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


FLOW_TYPES = ("type_if", "type_ifnot", "type_elseif", "type_elseifnot", "type_else", "type_case",
              "type_case_fast", "type_other", "type_repeat")


def is_flow_type(typ):
    """A Spin2 statement-opening token class: the compiler's own flow-statement classes
    (IF/ELSE/CASE/OTHER/REPEAT) and its `type_i_*` family (RETURN, ABORT, NEXT/QUIT and the
    built-in method statements). Read from the elementizer's token TYPES, never from keyword
    spellings -- the compiler decides what a word is."""
    return typ in FLOW_TYPES or typ.startswith("type_i_")


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
        if i < len(ts) and (ts[i].typ in OPEN_TYPES or is_flow_type(ts[i].typ)):
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


def load_oneline_keys(root):
    """Net 3 (S-256): the reviewed list of keys whose SINGLE-LINE strings are candidates.
    A missing or malformed file is CannotAudit: deleting it would silently narrow the net."""
    p = os.path.join(root, MANIFEST_DIR, ONELINE_KEYS_FILE)
    try:
        with open(p, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        keys = data["oneline_code_keys"]
        if not isinstance(keys, list) or not keys or not all(isinstance(k, str) for k in keys):
            raise ValueError("oneline_code_keys must be a non-empty list of strings")
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
                rel = os.path.relpath(os.path.join(dp, f), base).replace(os.sep, "/")
                # OBEX objects mirror the OBEX catalog: their text is the authors', code examples
                # included. Compiling it would pass a verdict on someone else's object, which the KB
                # does not do (doctrine: an OBEX entry carries what the catalog says; F-573). The
                # claim-sourcing gate skips them for the same reason (S-308c).
                if rel.startswith("community/obex/objects/"):
                    continue
                out.append(rel)
    return out


def find_candidates(root, rels, code_keys, oneline_keys=frozenset()):
    """-> ({rel: [Cand]}, census dict). Net 1 + net 2 (3.1) + net 3 (S-256): a single-line
    string under a key of `oneline_keys` (the real flows pass load_oneline_keys(root))."""
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
            elif key in oneline_keys:
                cs.append(Cand(rel, addr, value, line, key, style, "oneline"))
        per_file[rel] = cs
    aborted = 0
    if pending:
        with cf.ThreadPoolExecutor(max_workers=NWORK) as ex:
            results = list(ex.map(lambda pj: elementize(pj[1][2]), pending))
        for (rel, (addr, key, value, line, style)), (toks, _out, ab) in zip(pending, results):
            if ab:
                aborted += 1
            if ab or code_bearing(toks):  # fail safe: when the compiler cannot tell, the finder includes
                per_file[rel].append(Cand(rel, addr, value, line, key, style, "shape"))
    for rel, cs in per_file.items():
        cs.sort(key=lambda c: (c.line, c.addr))
    allc = [c for cs in per_file.values() for c in cs]
    census["candidates"] = len(allc)
    census["files_with_candidates"] = len({c.file for c in allc})
    census["net_key"] = sum(1 for c in allc if c.net == "key")
    census["net_shape_only"] = sum(1 for c in allc if c.net == "shape")
    census["net_oneline"] = sum(1 for c in allc if c.net == "oneline")
    census["net_oneline_files"] = len({c.file for c in allc if c.net == "oneline"})
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
    m = re.fullmatch(r"(%s)=con(?::(-?[0-9]+))?" % NAME_RE, s)
    if m:
        return {"kind": "con", "name": m.group(1), "raw": s, "value": int(m.group(2) or 0)}
    m = re.fullmatch(r"(%s)\(\)(?:->(\d+))?(?:/(\d+))?" % NAME_RE, s)
    if m:
        return {"kind": "stub", "name": m.group(1), "nret": int(m.group(2) or 0),
                "nparam": int(m.group(3) or 0), "raw": s}
    m = re.fullmatch(r"(%s)\.(%s)\((\d+)\)(?:->(%s))?" % (NAME_RE, NAME_RE, NAME_RE), s)
    if m:
        return {"kind": "objm", "inst": m.group(1), "name": m.group(2), "n": int(m.group(3)),
                "rtype": m.group(4), "raw": s}
    m = re.fullmatch(r"file:(.+)", s)
    if m:
        return {"kind": "file", "name": m.group(1), "raw": s}
    m = re.fullmatch(r"label:(\.?%s)" % NAME_RE, s)
    if m:
        return {"kind": "label", "name": m.group(1), "raw": s}
    m = re.fullmatch(r"lead:([0-9]+)", s)
    if m and 1 <= int(m.group(1)) <= 16:
        return {"kind": "lead", "n": int(m.group(1)), "raw": s}
    m = re.fullmatch(r"struct:(%s)\((.+)\)" % NAME_RE, s)
    if m:
        return {"kind": "struct", "name": m.group(1), "members": m.group(2), "raw": s}
    m = re.fullmatch(r"(%s)\.struct:(%s)\((.+)\)" % (NAME_RE, NAME_RE), s)
    if m:
        return {"kind": "objstruct", "inst": m.group(1), "name": m.group(2), "members": m.group(3), "raw": s}
    m = re.fullmatch(r"(%s(?:\[[0-9]+\])?):(\^?%s(?:\.%s)?)" % (NAME_RE, NAME_RE, NAME_RE), s)
    if m:
        return {"kind": "typed", "name": m.group(1), "type": m.group(2), "raw": s}
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
        if not (fa == "eof" or (isinstance(fa, int) and not isinstance(fa, bool) and fa >= 1)):
            errs.append("%s: `fails_at` (block-relative line >= 1, or `eof`) is required for never" % where)
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
    if "bare_const_ok" in e:
        bo = e["bare_const_ok"]
        if c == "not-code":
            errs.append("%s: `bare_const_ok` is for compiled blocks only" % where)
        elif not (isinstance(bo, list) and bo and all(isinstance(x, str) and x.strip() for x in bo)):
            errs.append("%s: `bare_const_ok` must be a non-empty list of constant names" % where)
        if not (isinstance(e.get("reason"), str) and e["reason"].strip()):
            errs.append("%s: `reason` is required with `bare_const_ok` (why the register read is intended)" % where)
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
                if rel not in NET_DATA_FILES:
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
    # structure types the block uses but does not define come FIRST: a method header such as
    # `PUB m() | ^point ptr` needs the type before it is read
    structs = [p for p in parsed if p and p["kind"] == "struct"]
    if structs:
        add("wrap", "hdr", ["CON"])
        for p in structs:
            adddecl("  STRUCT %s(%s)" % (p["name"], p["members"]), p["raw"], "struct")
        add("wrap", "hdr", [""])
    ind = lambda n: ["%s%s" % (" " * n, l) if l.strip() else l for l in bl]  # noqa: E731
    if wrap == "spin2-top":
        add("body", None, bl)
        if append_pub:
            add("wrap", "pub", ["PUB __kbgate()"])
    elif wrap in ("spin2-method", "spin2-method-result"):
        add("wrap", "head", ["PUB __kbgate()" + (" : __kbres" if wrap == "spin2-method-result" else "")])
        add("body", None, ind(2))
    elif wrap == "spin2-var":
        add("wrap", "head", ["VAR"])
        add("body", None, ind(2))
        add("wrap", "pub", ["", "PUB __kbgate()"])
    elif wrap in ("pasm2-dat", "pasm2-hub"):
        add("wrap", "head", ["DAT", "\t\torg\t0" if wrap == "pasm2-dat" else "\t\torgh"])
        labels = [p for p in parsed if p and p["kind"] == "label"]
        leads = sum(p["n"] for p in parsed if p and p["kind"] == "lead")
        if leads:  # instructions BEFORE the block, for a first line that reads `$-1` (relative address)
            add("wrap", "lead", ["\t\tnop"] * leads)
        add("body", None, bl)
        if labels:  # labels the block references but does not define, placed right after it
            add("wrap", "labels", [p["name"] for p in labels])
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
            adddecl("%s = %d" % (p["name"], p["value"]), p["raw"], "con")
    if stubs:
        add("wrap", "hdr", [""])
        for p in stubs:
            params = ", ".join("p%d" % i for i in range(1, p["nparam"] + 1))
            rets = ", ".join("r%d" % i for i in range(1, p["nret"] + 1))
            adddecl("PRI %s(%s)%s" % (p["name"], params, (" : " + rets) if rets else ""), p["raw"], "stub")
    typed = [p for p in parsed if p and p["kind"] == "typed"]
    if typed:
        add("wrap", "hdr", ["", "VAR"])
        for p in typed:
            adddecl("  %s %s" % (p["type"], p["name"]), p["raw"], "typed")
    b.text = "\n".join(lines) + "\n"
    # stub objects and files (generated into the compile directory)
    objm = [p for p in parsed if p and p["kind"] in ("objm", "objstruct")]
    if objm:
        omap = obj_decls(b.text)
        byfile = defaultdict(dict)
        structs_in = defaultdict(list)  # object file -> [struct decl line]
        for p in objm:
            lit = omap.get(p["inst"].lower())
            if lit is None:
                b.error = "assumes %r but the block declares no OBJ instance %r" % (p["raw"], p["inst"])
                continue
            meths = byfile[obj_filename(lit)]
            if p["kind"] == "objstruct":  # a structure the stub object EXPORTS (`obj.NAME` types)
                structs_in[obj_filename(lit)].append("  STRUCT %s(%s)" % (p["name"], p["members"]))
                continue
            k = p["name"].lower()  # Spin2 names are case-insensitive: one stub method per name
            if k not in meths or meths[k][1] < p["n"]:
                meths[k] = (p["name"], p["n"], p.get("rtype"))
        for fn, meths in byfile.items():
            text = ""
            if structs_in.get(fn):  # the exporting object needs the block's language version too
                text = ("{Spin2_v%d}\n" % version if version else "") + "CON\n" + "\n".join(structs_in[fn]) + "\n\n"
            if structs_in.get(fn) and not meths:
                meths = {"__kbstub": ("__kbstub", 0, None)}  # an object file must hold a method
            b.files[fn] = text + "".join(
                "PUB %s(%s) : %sr\n" % (m, ", ".join("p%d" % i for i in range(1, n + 1)),
                                        (rt + " ") if rt else "")
                for m, n, rt in meths.values())
    for p in parsed:
        if p and p["kind"] == "file":
            b.files.setdefault(p["name"], "")
        if p and p["kind"] in ("label", "lead") and wrap not in ("pasm2-dat", "pasm2-hub"):
            b.error = "assumes %r needs a pasm2-dat / pasm2-hub wrap (not %s)" % (p["raw"], wrap)
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
    __slots__ = ("kind", "detail", "echo", "extra")

    def __init__(self, kind, detail, echo=None):
        self.kind, self.detail, self.echo = kind, detail, echo
        self.extra = None    # a second verdict on the same block (BARE-CONST beside a FAIL)


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


def error_past_block(b, res, loc):
    """`fails_at: eof`: the compiler's error lands in the main file strictly AFTER the block's
    last line and in wrapper text (the wrapper tail, or past the end of the file) -- a whole-
    file check such as 'Conflicting or deficient _CLKFREQ/_XTLFREQ/... symbols found', which
    PNut-TS reports one line past EOF. An error on a block line, in a prerequisite `with`
    block, in an assumed declaration or in another file does NOT count."""
    if res.efile != MAIN_NAME or res.eline is None or loc[0] != "wrap":
        return False
    body_end = max((e for k, _l, _s, e in b.segs if k == "body"), default=0)
    return res.eline > body_end


PASM_CONTEXT_RE = re.compile(r"(?i)\b(?:dat|orgh?)\b")


def bare_const_sites(b, entry):
    """D3 (S-389): operand sites where a CONSTANT is used as a bare D/S operand of a PASM
    instruction (`mov flag, TRUE`). -> [(block line, "D"|"S", name, source line)].
    Read from the compiler's own token types; see the BARE-CONST section of the docstring.
    An elementize pass that aborts leaves the block unread (no sites): the gate is blind there."""
    if not PASM_CONTEXT_RE.search(b.text):   # PASM lives only in DAT or inline ORG/ORGH: skip the pass
        return []
    toks, _out, ab = elementize(b.text, b.files)
    if ab:
        return []
    body = [(s, e) for k, _l, s, e in b.segs if k == "body"]
    if not body:
        return []
    s0, e0 = body[0]
    src = b.text.split("\n")
    consts = set()
    for a in entry.get("assumes", []) or []:
        p = parse_assume(a)
        if p and p["kind"] == "con":
            consts.add(p["name"].lower())
    for i, t in enumerate(toks):          # the block's own CON declarations: `NAME =`
        if t.typ == "type_undefined" and t.name and i + 1 < len(toks) \
                and toks[i + 1].typ == "type_equal" and toks[i + 1].line == t.line:
            consts.add(t.name.lower())
    ok = {n.lower() for n in (entry.get("bare_const_ok") or [])}
    by_line = defaultdict(list)
    for t in toks:
        if t.typ not in ("type_end", "type_end_file"):
            by_line[t.line].append(t)
    sites = []
    for ln in sorted(by_line):
        if not (s0 <= ln <= e0):
            continue
        ts = sorted(by_line[ln], key=lambda t: t.col)
        i = 0
        while i < len(ts) and ts[i].typ == "type_asm_cond":
            i += 1
        if i >= len(ts) or ts[i].typ != "type_asm_inst":
            continue
        rest = ts[i + 1:]
        while rest and rest[-1].typ == "type_asm_effect":
            rest.pop()
        operands, cur, depth = [], [], 0
        for t in rest:
            if t.typ == "type_left":
                depth += 1
            elif t.typ == "type_right":
                depth -= 1
            if t.typ == "type_comma" and depth == 0:
                operands.append(cur)
                cur = []
            else:
                cur.append(t)
        operands.append(cur)
        text = src[ln - 1] if 0 < ln <= len(src) else ""
        for opi, op in enumerate(operands[:2]):
            if len(op) != 1:             # a `#` / `##` prefix, an expression or a register list: not bare
                continue
            t = op[0]
            ident = re.match(NAME_RE, text[t.col:])
            if t.typ.startswith("type_con") and ident:
                name = ident.group(0)
            elif t.typ == "type_undefined" and t.name and t.name.lower() in consts:
                name = t.name
            else:
                continue
            if name.lower() in ok:
                continue
            sites.append((ln - s0 + 1, "D" if opi == 0 else "S", name, text.strip()))
    return sites


def bare_const_verdict(b, entry):
    sites = bare_const_sites(b, entry)
    if not sites:
        return None
    detail = "; ".join("block line %d, %s operand: bare constant %s reads the register at address %s -- "
                       "to load the value write #%s (or ##%s)" % (n, w, name, name, name, name)
                       for n, w, name, _t in sites)
    return Verdict("BARE-CONST", detail, sites[0][3])


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
            return bare_const_verdict(b, entry)
        detail, echo, _loc = describe(b, res, cand)
        v = Verdict("FAIL", detail, echo)
        v.extra = bare_const_verdict(b, entry)   # D3 is independent of legality: report both
        return v
    # never: asserted to fail, at fails_at
    fa = entry["fails_at"]
    where = "the end of the block (`eof`)" if fa == "eof" else "block line %d" % fa
    if res.ok:
        return Verdict("NEVER-COMPILES", "expected to fail at %s; it compiles" % where)
    detail, echo, loc = describe(b, res, cand)
    if fa == "eof":
        if error_past_block(b, res, loc):
            return bare_const_verdict(b, entry)
    elif loc[0] == "body" and loc[1] == fa:
        return bare_const_verdict(b, entry)
    return Verdict("NEVER-WRONG-REASON", "expected to fail at %s; %s" % (where, detail), echo)


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


RETURN_VALUE_RE = re.compile(r"\s*return\s+[^\s']", re.I)   # `return <value>` (not a bare return / comment)
_ACCEPTED = None
_ACCEPTED_LOCK = threading.Lock()
DIRECTIVE_PROBE = range(1, 100)


def accepted_versions():
    """The {Spin2_vNN} directives THIS compiler accepts, ascending, found by probing
    (never hardcoded: PNut-TS accepts a sparse set, and moves). Cached."""
    global _ACCEPTED
    with _ACCEPTED_LOCK:
        if _ACCEPTED is None:
            ok = []
            for n in DIRECTIVE_PROBE:
                b = build(None, "{Spin2_v%d}\nPUB __kbprobe()\n" % n, [])
                if compile_built(b, False).ok:
                    ok.append(n)
            _ACCEPTED = ok
        return _ACCEPTED


def undefined_names(wrap, body, extra, version, append_pub):
    """Lower-cased names the elementizer leaves type_undefined in the wrapped block, or
    None when the elementize pass aborted."""
    b = build(wrap, body, extra, version, (), append_pub)
    toks, _out, ab = elementize(b.text, b.files)
    if ab:
        return None
    return {t.name.lower() for t in toks if t.typ == "type_undefined" and t.name}


def keyword_version(wrap, body, extra, append_pub):
    """Language-version-gated built-ins (BYTECOMP, ...). The compiler lexes them as
    undefined names until the right {Spin2_vNN} is given, so the proposer would stub them
    as user methods and report a fake PASS. -> the LOWEST accepted N at which every name
    that resolves under the HIGHEST accepted N resolves, or None when no name does."""
    acc = accepted_versions()
    if not acc:
        return None
    base = undefined_names(wrap, body, extra, None, append_pub)
    top = undefined_names(wrap, body, extra, acc[-1], append_pub)
    if not base or top is None:
        return None
    kw = base - top
    if not kw:
        return None
    for n in acc:
        u = undefined_names(wrap, body, extra, n, append_pub)
        if u is not None and not (kw & u):
            return n
    return acc[-1]


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
            fail_text = None
            if not res.ok and res.eline is not None:
                lc = locate(b, res.efile, res.eline)
                if lc[0] == "body" and 0 < lc[1] <= len(b.src_lines):
                    fail_text = b.src_lines[lc[1] - 1]
            return {"result": kind, "fail_text": fail_text, "assumes": assumes, "dropped": list(st["dropped"]),
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
            if st["version"] is None:
                kv = keyword_version(wrap, body, st["extra"], st["append_pub"])
                if kv is not None:
                    st["version"] = kv
                    maxit += 1
                    continue  # recompile under the directive before naming any undeclared name
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
            if wrap == "spin2-method" and 0 < n <= len(b.src_lines) and RETURN_VALUE_RE.match(b.src_lines[n - 1]):
                return result("FAIL")  # no assume can make `return <value>` legal here (S-022): the caller tries the result wrap
            here =[d for d in st["decls"] if n in st["info"].get(d["name"].lower(), {"lines": ()})["lines"]]
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


def var_only(toks):
    """True when EVERY code line of the bare block is a VAR-section declaration, read from
    the compiler's token types: each comma-separated part opens with an optional `^`
    (type_op) then a size token (BYTE/WORD/LONG, type_size) then the declared name
    (type_undefined). Executable statements never open that way."""
    by_line = defaultdict(list)
    for t in toks:
        if t.typ not in ("type_end", "type_end_file"):
            by_line[t.line].append(t)
    if not by_line:
        return False
    for _ln, ts in by_line.items():
        ts = sorted(ts, key=lambda t: t.col)
        parts, cur = [], []
        for t in ts:
            if t.typ == "type_comma":
                parts.append(cur)
                cur = []
            else:
                cur.append(t)
        parts.append(cur)
        for p in parts:
            i = 1 if p and p[0].typ == "type_op" else 0
            if not (len(p) > i + 1 and p[i].typ == "type_size" and p[i + 1].typ == "type_undefined"):
                return False
    return True


def shape_order(toks):
    """Wrap order from what the compiler saw in the bare block."""
    if var_only(toks):  # a VAR declaration read as DAT data is a false pass (S-136): VAR first
        return ["spin2-var", "pasm2-dat", "spin2-method"]
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
        if (wrap == "spin2-method" and h["result"] == "FAIL"
                and RETURN_VALUE_RE.match(h.get("fail_text") or "")):
            # the only error is a `return <value>` in a wrapper that declares no result (S-022)
            h2 = harness(cand.text, "spin2-method-result")
            compiles += h2["compiles"]
            tried.append(("spin2-method-result", h2["result"]))
            attempts.append(("spin2-method-result", h2))
            if h2["result"] == "PASS":
                wrap, h = "spin2-method-result", h2
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

REGISTRABLE = ("FAIL", "NEVER-COMPILES", "NEVER-WRONG-REASON", "BARE-CONST")


class Problem:
    __slots__ = ("kind", "file", "line", "addr", "cls", "detail", "echo", "finding")

    def __init__(self, kind, file, line, addr, cls, detail, echo=None, finding=None):
        self.kind, self.file, self.line, self.addr = kind, file, line, addr
        self.cls, self.detail, self.echo = cls, detail, echo
        self.finding = finding

    @property
    def registered(self):
        """REGISTERED: a verdict failure (FAIL / NEVER-*) whose entry carries `finding:`.
        Reporting only -- the exit code does not read this. UNCLASSIFIED, STALE and
        ORPHAN are never registered (a finding cannot excuse a missing, stale or
        orphaned entry)."""
        return bool(self.finding) and self.kind in REGISTRABLE

    def as_dict(self):
        d = {k: getattr(self, k) for k in self.__slots__}
        d["registered"] = self.registered
        return d


def cls_label(entry):
    c = entry["compile"]
    return c if c in ("program", "not-code") else "%s/%s" % (c, entry["wrap"])


def evaluate(root, files=None, strict=True):
    """The gate. -> dict(problems, counts, census, scope). Raises CannotAudit."""
    check_pnut()
    code_keys = load_code_keys(root)
    oneline_keys = load_oneline_keys(root)
    kb_all = kb_files(root)
    if files is None:
        manifest = load_manifest(root)
        scope = sorted(set(kb_all) | set(manifest))
    else:
        scope = sorted(set(files))
        manifest = load_manifest(root, only=set(scope))
    per_file, census = find_candidates(root, scope, code_keys, oneline_keys)
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
                    problems.append(Problem("STALE (%s)" % r.state, rel, c.line, c.addr, cls_label(e), how,
                                            finding=e.get("finding")))
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
                problems.append(Problem("FAIL", rel, c.line, c.addr, cls_label(e), bad,
                                        finding=e.get("finding")))
                continue
            jobs.append((r, withs))
        for _ei, e in orphans:
            problems.append(Problem("ORPHAN", rel, 0, e["at"], cls_label(e),
                                    "entry whose block is gone; delete it (that records the removal)",
                                    finding=e.get("finding")))
    with cf.ThreadPoolExecutor(max_workers=NWORK) as ex:
        verdicts = list(ex.map(lambda j: assert_entry(j[0].cand, j[0].entry, j[1]), jobs))
    for (r, _w), v in zip(jobs, verdicts):
        if v is not None:
            c = r.cand
            problems.append(Problem(v.kind, c.file, c.line, c.addr, cls_label(r.entry), v.detail, v.echo,
                                    finding=r.entry.get("finding")))
            if v.extra is not None:
                problems.append(Problem(v.extra.kind, c.file, c.line, c.addr, cls_label(r.entry), v.extra.detail,
                                        v.extra.echo, finding=r.entry.get("finding")))
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
        reg = ""
        if p.kind in REGISTRABLE:
            reg = ("  REGISTERED(%s)" % p.finding) if p.registered else "  UNREGISTERED"
        print("%-17s %s  %s%s%s  %s" % (p.kind, loc, p.addr, cls, reg, p.detail))
        if p.echo is not None:
            print("%-17s |   %s" % ("", p.echo.strip()))
    c = rep["counts"]
    total = sum(c.values())
    tail = "(%d blocks: %d program, %d fragment, %d never asserted to fail, %d not-code)" % (
        total, c.get("program", 0), c.get("fragment", 0), c.get("never", 0), c.get("not-code", 0))
    if problems:
        kinds = Counter(p.kind.split(" ")[0] for p in problems)
        files = len({p.file for p in problems})
        order = ["FAIL", "NEVER-COMPILES", "NEVER-WRONG-REASON", "BARE-CONST", "STALE", "UNCLASSIFIED", "ORPHAN"]
        parts = ["%d %s" % (kinds[k], k) for k in order if kinds.get(k)]
        nreg = sum(1 for p in problems if p.registered)
        nunreg = sum(1 for p in problems if p.kind in REGISTRABLE and not p.registered)
        print("FAIL: %d problems in %d files -- %s; %d REGISTERED (carry a finding), %d UNREGISTERED %s"
              % (len(problems), files, ", ".join(parts), nreg, nunreg, tail))
    else:
        print("PASS: every block holds its declared class %s" % tail)
    print(LEGALITY_NOTE)


def print_census(census):
    c = census
    print("census (finder, real): %d YAML files in scope; %d candidates in %d files "
          "(net 1 code-named key: %d, of which %d single-line; net 2 compiler-recognised shape only: %d; "
          "net 3 one-line key: %d in %d files)"
          % (c.get("files", 0), c.get("candidates", 0), c.get("files_with_candidates", 0),
             c.get("net_key", 0), c.get("key_single_line", 0), c.get("net_shape_only", 0),
             c.get("net_oneline", 0), c.get("net_oneline_files", 0)))
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
    oneline_keys = load_oneline_keys(root)
    scope = files if files is not None else kb_files(root)
    per_file, census = find_candidates(root, sorted(scope), code_keys, oneline_keys)
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
    oneline_keys = load_oneline_keys(root)
    scope = sorted(set(files))
    manifest = load_manifest(root, only=set(scope))
    per_file, _census = find_candidates(root, scope, code_keys, oneline_keys)
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


class Refused(Exception):
    """Exit 3: --apply refused the decisions file; nothing was written."""


SIDECAR_HEADER = (
    "# engineering/tools/validation/kb-compile-manifest/%s\n"
    "# ENH-03 compile manifest. LEGALITY ONLY: a pass proves pnut-ts accepts the block in the\n"
    "# context declared here, never that the code is correct (F-381, F-312).\n"
    "blocks:\n")


def apply_decisions(root, decisions):
    """Validate EVERY decision, then write. -> sorted list of touched KB-relative files.
    Raises Refused (nothing written) on any problem. A decision is
    {"file", "at", "compile", + optional wrap, assumes, with, fails_at, reason, finding,
    spin2_version}; `fp` is computed from the live candidate and may not be supplied."""
    check_pnut()
    code_keys = load_code_keys(root)
    oneline_keys = load_oneline_keys(root)
    errs = []
    if not isinstance(decisions, list) or not decisions:
        raise Refused("decisions must be a non-empty JSON list")
    by_file = defaultdict(list)  # rel -> [(index, decision)]
    for i, d in enumerate(decisions):
        if not isinstance(d, dict):
            errs.append("decision %d: not an object" % i)
        elif not isinstance(d.get("file"), str) or not d["file"] or not isinstance(d.get("at"), str):
            errs.append("decision %d: `file` and `at` must be non-empty strings" % i)
        elif "fp" in d:
            errs.append("decision %d: `fp` is computed from the live candidate; do not supply it" % i)
        else:
            by_file[d["file"]].append((i, d))
    if errs:
        raise Refused("; ".join(errs))
    base = os.path.join(root, KB_DIR)
    new_text = {}  # rel -> full new sidecar text
    for rel in sorted(by_file):
        where = "decision file %s" % rel
        if safe_join(base, rel) is None or not rel.endswith(".yaml") or not os.path.isfile(os.path.join(base, rel)):
            errs.append("%s: not an existing KB YAML file" % where)
            continue
        per_file, _c = find_candidates(root, [rel], code_keys, oneline_keys)
        live = {c.addr: c for c in per_file[rel]}
        try:
            existing = load_manifest(root, only={rel}).get(rel, [])
        except CannotAudit as e:
            errs.append("%s: existing sidecar unreadable (%s)" % (where, e))
            continue
        have = {e["at"] for e in existing}
        seen = set()
        add = []
        for i, d in by_file[rel]:
            at = d["at"]
            tag = "decision %d (%s %s)" % (i, rel, at)
            if at not in live:
                errs.append("%s: not a live candidate address" % tag)
                continue
            if at in have:
                errs.append("%s: the sidecar already has an entry at this address (no overwrite)" % tag)
                continue
            if at in seen:
                errs.append("%s: address decided twice in this run" % tag)
                continue
            seen.add(at)
            e = {"at": at, "fp": live[at].fp}
            e.update({k: v for k, v in d.items() if k not in ("file", "at")})
            ee = validate_entry(e, tag)
            if ee:
                errs.extend(ee)
                continue
            add.append(e)
        if add:
            body = "".join(emit_entry(e) for e in add)
            p = sidecar_path(root, rel)
            if os.path.isfile(p):
                with open(p, encoding="utf-8") as fh:
                    old = fh.read()
                if not re.search(r"^blocks:\s*(\[\s*\])?\s*$", old, re.M):
                    errs.append("%s: existing sidecar has no plain `blocks:` line to extend" % where)
                    continue
                old = re.sub(r"^blocks:\s*(\[\s*\])?\s*$", "blocks:", old, count=1, flags=re.M)
                if not old.endswith("\n"):
                    old += "\n"
                new_text[rel] = old + body
            else:
                new_text[rel] = SIDECAR_HEADER % rel + body
    if errs:
        raise Refused("%d problem(s), nothing written:\n  " % len(errs) + "\n  ".join(errs))
    for rel, text in new_text.items():
        write(sidecar_path(root, rel), text)
    return sorted(new_text)


def do_apply(root, path):
    try:
        with open(path, encoding="utf-8") as fh:
            decisions = json.load(fh)
    except Exception as e:  # noqa: BLE001
        raise CannotAudit("decisions file unreadable: %s (%s)" % (path, e)) from None
    try:
        touched = apply_decisions(root, decisions)
    except Refused as e:
        print("REFUSED: %s" % e)
        return 3, None
    print("APPLIED: %d entries written to %d sidecars" % (len(decisions), len(touched)))
    print("pnut-ts: %s (run context; never written to the manifest or the KB)" % pnut_version())
    rep = evaluate(root, files=touched, strict=True)
    print_census(rep["census"])
    print_report(rep, "")
    return rep_exit(rep), rep


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
            if rel not in NET_DATA_FILES:
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
    return nc_finish(root, entries_fn)


def nc_finish(root, entries_fn, oneline=("correct", "prose")):
    """Write the scratch net-data files, run the real finder on nc.yaml and write the sidecar
    entries_fn(candidates) returns (None = no sidecar)."""
    write(os.path.join(root, MANIFEST_DIR, CODE_KEYS_FILE), "code_keys: [code]\n")
    write(os.path.join(root, MANIFEST_DIR, ONELINE_KEYS_FILE),
          "oneline_code_keys: [%s]\n" % ", ".join(oneline))
    per_file, _c = find_candidates(root, ["nc.yaml"], {"code"}, set(oneline))
    cands = per_file["nc.yaml"]
    ents = entries_fn(cands)
    if ents is not None:
        write(os.path.join(root, MANIFEST_DIR, "nc.yaml"),
              "blocks:\n" + "".join(emit_entry(e) for e in ents))
    return root


def nc_root_text(yaml_text, entries_fn):
    """Like nc_root, but with the scratch KB YAML given verbatim (net-3 controls)."""
    root = tempfile.mkdtemp(dir=tmp_root())
    write(os.path.join(root, KB_DIR, "nc.yaml"), yaml_text)
    return nc_finish(root, entries_fn)


def emit_entry(e):
    out = ["  - at: %s\n" % yq(e["at"]), '    fp: "%s"\n' % e["fp"], "    compile: %s\n" % e["compile"]]
    for k in ("wrap", "reason", "fails_at", "spin2_version"):
        if k in e:
            plain = k == "wrap" and e[k] in WRAPS  # the same unquoted form --propose prints
            out.append("    %s: %s\n" % (k, json.dumps(e[k]) if isinstance(e[k], str) and not plain else e[k]))
    if e.get("assumes"):
        out.append("    assumes: %s\n" % assumes_flow(e["assumes"]))
    if e.get("with"):
        out.append("    with: [%s]\n" % ", ".join(json.dumps(w) for w in e["with"]))
    if e.get("bare_const_ok"):
        out.append("    bare_const_ok: [%s]\n" % ", ".join(json.dumps(w) for w in e["bare_const_ok"]))
    if "finding" in e:
        out.append("    finding: %s\n" % json.dumps(e["finding"]))
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
    # NC12 --apply (B3 step 0): every refusal writes NOTHING; a valid decision lands with the live fp
    def try_apply(root, decisions):
        try:
            return "applied", apply_decisions(root, decisions)
        except Refused as ex:
            return "refused", str(ex)

    def sidecar_state(root):
        p = sidecar_path(root, "nc.yaml")
        if not os.path.isfile(p):
            return None
        with open(p, encoding="utf-8") as fh:
            return fh.read()

    root = nc_root([GOOD_PROG], lambda cs: None)
    how, msg = try_apply(root, [{"file": "nc.yaml", "at": "examples[9].code", "compile": "program"}])
    rec("12a", "--apply refuses an address that is not a live candidate; nothing written", "refused, no sidecar",
        "%s; sidecar %s" % (how, "absent" if sidecar_state(root) is None else "WRITTEN"),
        how == "refused" and "live candidate" in msg and sidecar_state(root) is None)
    root = nc_root([GOOD_PROG], lambda cs: [ent(cs[0], compile="program")])
    before = sidecar_state(root)
    how, msg = try_apply(root, [{"file": "nc.yaml", "at": "examples[0].code", "compile": "not-code", "reason": "nc"}])
    rec("12b", "--apply refuses to overwrite an existing entry; sidecar unchanged", "refused, unchanged",
        "%s; sidecar %s" % (how, "unchanged" if sidecar_state(root) == before else "CHANGED"),
        how == "refused" and "no overwrite" in msg and sidecar_state(root) == before)
    root = nc_root([GOOD_PROG, GOOD_PROG.replace("56", "57")], lambda cs: None)
    how, msg = try_apply(root, [
        {"file": "nc.yaml", "at": "examples[0].code", "compile": "program"},
        {"file": "nc.yaml", "at": "examples[1].code", "compile": "never", "wrap": "spin2-top", "reason": "nc"}])
    rec("12c", "--apply refuses an invalid entry (never without fails_at); the valid one is not written either",
        "refused, no sidecar", "%s; sidecar %s" % (how, "absent" if sidecar_state(root) is None else "WRITTEN"),
        how == "refused" and "fails_at" in msg and sidecar_state(root) is None)
    root = nc_root([GOOD_PROG], lambda cs: None)
    how, touched = try_apply(root, [{"file": "nc.yaml", "at": "examples[0].code", "compile": "program"}])
    txt = sidecar_state(root) or ""
    rep12 = evaluate(root, files=["nc.yaml"], strict=True)
    want_fp = fingerprint(GOOD_PROG)  # the parsed `|` scalar is GOOD_PROG (one trailing newline)
    per12, _c = find_candidates(root, ["nc.yaml"], {"code"})
    rec("12d", "--apply writes a program entry with the finder's fp, and the gate then PASSes it", "PASS",
        "%s; fp in sidecar %s; gate %s" % (how, 'fp: "%s"' % want_fp in txt, nc_summary(rep12)),
        how == "applied" and touched == ["nc.yaml"] and 'fp: "%s"' % want_fp in txt
        and per12["nc.yaml"][0].fp == want_fp and not rep12["problems"]
        and "LEGALITY ONLY" in txt and rep12["counts"].get("program") == 1)
    # NC13 REGISTERED vs UNREGISTERED: reporting only, the verdict and the exit code do not move
    import contextlib
    import io

    def report_text(rep):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            print_report(rep, "")
        return buf.getvalue()

    repR = nc_run([BAD_PROG], lambda cs: [ent(cs[0], compile="fragment", wrap="spin2-top", finding="F-999")])
    tR = report_text(repR)
    rec("13a", "failing fragment WITH finding: REGISTERED(F-999), exit code still 1", "REGISTERED, exit 1",
        "kinds %s; exit %d" % ([p.kind for p in repR["problems"]], rep_exit(repR)),
        [p.kind for p in repR["problems"]] == ["FAIL"] and repR["problems"][0].registered
        and "REGISTERED(F-999)" in tR and "UNREGISTERED" not in tR.replace("0 UNREGISTERED", "")
        and "1 REGISTERED (carry a finding), 0 UNREGISTERED" in tR and rep_exit(repR) == 1)
    repU = nc_run([BAD_PROG], lambda cs: [ent(cs[0], compile="fragment", wrap="spin2-top")])
    tU = report_text(repU)
    rec("13b", "the same failing fragment WITHOUT finding: UNREGISTERED, exit code 1", "UNREGISTERED, exit 1",
        "kinds %s; exit %d" % ([p.kind for p in repU["problems"]], rep_exit(repU)),
        [p.kind for p in repU["problems"]] == ["FAIL"] and not repU["problems"][0].registered
        and "  UNREGISTERED" in tU and "REGISTERED(" not in tU
        and "0 REGISTERED (carry a finding), 1 UNREGISTERED" in tU and rep_exit(repU) == 1)
    repS = nc_run([GOOD_PROG], lambda cs: [dict(ent(cs[0], compile="program", finding="F-999"), fp="0" * 16)])
    rec("13c", "a finding never registers a STALE entry", "STALE, not registered",
        "kinds %s; registered %s" % ([p.kind for p in repS["problems"]], [p.registered for p in repS["problems"]]),
        [p.kind for p in repS["problems"]] == ["STALE (CHANGED)"] and not repS["problems"][0].registered
        and rep_exit(repS) == 1)
    # NC14 a version-gated built-in (BYTECOMP, {Spin2_v45}+) is a keyword, never a stubbed callee
    frag14 = "PUB go() : r\n  r := BYTECOMP(@a, @b, 4)\n"
    root14 = nc_root([frag14], lambda cs: None)
    per14, _c = find_candidates(root14, ["nc.yaml"], {"code"})
    cand14 = per14["nc.yaml"][0]
    prop14 = propose_one(cand14)
    # an oracle that shares no code with keyword_version: the lowest accepted directive under
    # which the block compiles with BYTECOMP undeclared and only the operands assumed
    oracle = None
    for n in accepted_versions():
        b14 = build("spin2-top", frag14, ["a", "b"], n)
        if compile_built(b14, False).ok:
            oracle = n
            break
    stubbed14 = [a for a in prop14["assumes"] if a.upper().startswith("BYTECOMP")]
    gate14 = None
    if prop14["outcome"] == "PASS" and prop14["compile"] == "fragment":
        e14 = {"compile": "fragment", "wrap": prop14["wrap"], "assumes": prop14["assumes"]}
        if prop14.get("version"):
            e14["spin2_version"] = prop14["version"]
        gate14 = assert_entry(cand14, e14, [])
    rec(14, "fragment calling version-gated BYTECOMP: proposes spin2_version, no stub, and the gate passes it",
        "PASS, spin2_version=%s, no BYTECOMP stub" % oracle,
        "%s; version=%s; assumes=%s; gate %s" % (prop14["outcome"], prop14.get("version"), prop14["assumes"],
                                                 "PASS" if gate14 is None else gate14.kind),
        oracle is not None and prop14["outcome"] == "PASS" and prop14.get("version") == oracle
        and not stubbed14 and gate14 is None)
    # NC15 the finder's net (S-109): flow statements under a NON-code key, and an aborted elementize
    def nc_find_text(yaml_text):
        r = tempfile.mkdtemp(dir=tmp_root())
        write(os.path.join(r, KB_DIR, "nc.yaml"), yaml_text)
        write(os.path.join(r, MANIFEST_DIR, CODE_KEYS_FILE), "code_keys: [code]\n")
        per, _c = find_candidates(r, ["nc.yaml"], {"code"})
        return [(c.addr, c.net) for c in per["nc.yaml"]]

    f15 = nc_find_text("a:\n  correct: |\n    REPEAT\n      IF done\n        QUIT\n"
                       "  wrong: |\n    CASE x\n      1: foo()\n"
                       "  prose: |\n    Some plain words here\n    and more plain words follow\n")
    rec("15a", "multi-line REPEAT/IF/CASE under non-code keys are netted; prose is not", "correct, wrong netted only",
        str(f15), sorted(a for a, _n in f15) == ["a.correct", "a.wrong"])
    f15b = nc_find_text('a:\n  note: |\n    plain words\n    #INCLUDE "no_such_file_kb"\n')
    rec("15b", "a string whose elementize pass ABORTS (missing #INCLUDE) is a candidate (fail safe)", "netted",
        str(f15b), [a for a, _n in f15b] == ["a.note"])
    # NC16 a method BODY with `return <value>` (S-022)
    frag16 = "x := 5\nreturn x\n"
    root16 = nc_root([frag16], lambda cs: None)
    per16, _c = find_candidates(root16, ["nc.yaml"], {"code"})
    cand16 = per16["nc.yaml"][0]
    prop16 = propose_one(cand16)
    gate16 = None
    errs16 = ["not proposed"]
    if prop16["outcome"] == "PASS" and prop16["compile"] == "fragment":
        e16 = {"at": cand16.addr, "fp": cand16.fp, "compile": "fragment", "wrap": prop16["wrap"],
               "assumes": prop16["assumes"]}
        errs16 = validate_entry(e16, "nc16")
        gate16 = assert_entry(cand16, e16, [])
    rec(16, "method body `return x`: proposer picks spin2-method-result; entry validates and the gate passes it",
        "PASS, wrap spin2-method-result", "%s wrap=%s assumes=%s; validate %s; gate %s" % (
            prop16["outcome"], prop16.get("wrap"), prop16["assumes"], errs16,
            "PASS" if gate16 is None else gate16.kind),
        prop16["outcome"] == "PASS" and prop16.get("wrap") == "spin2-method-result" and not errs16 and gate16 is None)
    # NC17 NAME=con:V gives the constant its value (an array count of 0 is a different error)
    frag17 = 'OBJ\n  pca[NBUS] : "nc_pca"\n\nPUB go()\n  pca[0].run()\n'
    r0 = nc_run([frag17], lambda cs: [ent(cs[0], compile="fragment", wrap="spin2-top",
                                          assumes=["NBUS=con", "pca.run(0)"])])
    r4 = nc_run([frag17], lambda cs: [ent(cs[0], compile="fragment", wrap="spin2-top",
                                          assumes=["NBUS=con:4", "pca.run(0)"])])
    rec(17, "`NBUS=con` (0) fails as an object count; `NBUS=con:4` passes", "plain FAIL, valued PASS",
        "plain %s; valued %s" % (nc_summary(r0), nc_summary(r4)),
        [p.kind for p in r0["problems"]] == ["FAIL"] and not r4["problems"])
    # NC18 VAR declaration lines (S-136): the proposer picks spin2-var, never DAT-data pasm2-dat
    def propose_text(text):
        r = nc_root([text], lambda cs: None)
        pr, _c = find_candidates(r, ["nc.yaml"], {"code"})
        return pr["nc.yaml"][0], propose_one(pr["nc.yaml"][0])

    c18, p18 = propose_text("BYTE flag\nLONG buf[16]\n")
    gate18 = None
    if p18["outcome"] == "PASS" and p18["compile"] == "fragment":
        gate18 = assert_entry(c18, {"compile": "fragment", "wrap": p18["wrap"], "assumes": p18["assumes"]}, [])
    rec(18, "block of VAR declaration lines: proposer picks spin2-var (not pasm2-dat), gate passes it", "PASS, spin2-var",
        "%s wrap=%s; gate %s" % (p18["outcome"], p18.get("wrap"), "PASS" if gate18 is None else gate18.kind),
        p18["outcome"] == "PASS" and p18.get("wrap") == "spin2-var" and gate18 is None)
    v_stmt = var_only(elementize("x := 5\nbuf[1] := x\n")[0])
    v_data = var_only(elementize("BYTE 1, 2, 3\n")[0])    # DAT data: a size token then a constant
    v_decl = var_only(elementize("LONG a, BYTE b[4]\n^LONG p\n")[0])
    rec("18b", "executable statements and DAT data are NOT VAR declarations; a declaration list is",
        "False / False / True", "%s / %s / %s" % (v_stmt, v_data, v_decl),
        v_stmt is False and v_data is False and v_decl is True)
    # NC19 structure types the block does not define (S-123)
    def run_entry(text, **entry):
        r = nc_root([text], lambda cs: None)
        pr, _c = find_candidates(r, ["nc.yaml"], {"code"})
        e = dict(compile="fragment", **entry)
        errs = validate_entry(dict(e, at="x", fp="0" * 16), "nc19")
        v = assert_entry(pr["nc.yaml"][0], e, [])
        return errs, v

    sdef = "struct:point_t(LONG x, LONG y)"
    errs, v_with = run_entry("p.x := 100\n", wrap="spin2-method", spin2_version=45, assumes=[sdef, "p:point_t"])
    _e, v_wo = run_entry("p.x := 100\n", wrap="spin2-method", spin2_version=45, assumes=["p:point_t"])
    rec("19a", "local structure type: `struct:` + `NAME:TYPE` passes; without the struct it fails", "PASS / FAIL",
        "with %s %s; without %s" % ("PASS" if v_with is None else v_with.kind, errs,
                                    "PASS" if v_wo is None else v_wo.kind),
        v_with is None and not errs and v_wo is not None and v_wo.kind == "FAIL")
    imp = 'OBJ\n  sens : "sensor"\n\nVAR\n  sens.reading_t r\n\nPUB main()\n  r := sens.get()\n'
    errs, v_obj = run_entry(imp, wrap="spin2-top", spin2_version=45,
                            assumes=["sens.get(0)->reading_t", "sens.struct:reading_t(LONG a, LONG b)"])
    _e, v_noobj = run_entry(imp, wrap="spin2-top", spin2_version=45, assumes=["sens.get(0)->reading_t"])
    rec("19b", "imported structure type: `OBJ.struct:` exported by the stub object passes; without it fails",
        "PASS / FAIL", "with %s %s; without %s" % ("PASS" if v_obj is None else v_obj.kind, errs,
                                                    "PASS" if v_noobj is None else v_noobj.kind),
        v_obj is None and not errs and v_noobj is not None and v_noobj.kind == "FAIL")
    # NC20 fails_at: eof (S-150)
    clk = "CON\n  _rcfast = TRUE\n  _clkfreq = 200_000_000\n"
    def never_verdict(text, fails_at, **extra):
        r = nc_root([text], lambda cs: None)
        pr, _c = find_candidates(r, ["nc.yaml"], {"code"})
        e = {"compile": "never", "wrap": "spin2-top", "reason": "nc", "fails_at": fails_at, **extra}
        v = assert_entry(pr["nc.yaml"][0], e, [])
        return validate_entry(dict(e, at="x", fp="0" * 16), "nc20"), v
    e1, v_eof = never_verdict(clk, "eof")
    _e, v_line = never_verdict(clk, 3)
    _e, v_body = never_verdict(BAD_PROG, "eof")     # fails on a BLOCK line: not an eof failure
    _e, v_ok = never_verdict(GOOD_PROG, "eof")
    _e, v_decl = never_verdict("CON\n  x = 5\n", "eof", assumes=["x=con"])      # error in an ASSUMED declaration
    _e, v_head = never_verdict(GOOD_PROG, "eof", spin2_version=56)           # error in the wrapper HEAD (bad directive)
    kinds = lambda v: "PASS" if v is None else v.kind
    rec("20", "never `fails_at: eof`: whole-file error past the block passes; a body-line error, a pinned line "
        "that is not the error, a block that compiles, an error in an assumed declaration and one in the "
        "wrapper head all fail", "PASS / WRONG / WRONG / NEVER-COMPILES / WRONG / WRONG",
        "%s %s / %s / %s / %s / %s / %s" % (kinds(v_eof), e1, kinds(v_line), kinds(v_body), kinds(v_ok),
                                            kinds(v_decl), kinds(v_head)),
        v_eof is None and not e1 and kinds(v_line) == "NEVER-WRONG-REASON"
        and kinds(v_body) == "NEVER-WRONG-REASON" and kinds(v_ok) == "NEVER-COMPILES"
        and kinds(v_decl) == "NEVER-WRONG-REASON" and kinds(v_head) == "NEVER-WRONG-REASON")
    # NC21 labels the PASM excerpt references but does not define (S-198)
    def pasm_verdict(text, assumes):
        r = nc_root([text], lambda cs: None)
        pr, _c = find_candidates(r, ["nc.yaml"], {"code"})
        e = {"compile": "fragment", "wrap": "pasm2-dat", "assumes": assumes}
        return validate_entry(dict(e, at="x", fp="0" * 16), "nc21"), assert_entry(pr["nc.yaml"][0], e, [])
    loc21 = ".a\n        nop\n        djnz counter, #.a\n        jmp #.out\n"
    e_a, v_a = pasm_verdict(loc21, ["counter", "label:.out"])
    _e, v_a0 = pasm_verdict(loc21, ["counter"])
    e_g, v_g = pasm_verdict("jmp #target\n", ["label:target"])
    _e, v_g0 = pasm_verdict("jmp #target\n", [])
    rec("21", "PASM excerpt jumping to a label defined outside it: `label:.out` / `label:target` pass; without fail",
        "PASS / FAIL / PASS / FAIL", "%s %s / %s / %s %s / %s" % (kinds(v_a), e_a, kinds(v_a0), kinds(v_g), e_g, kinds(v_g0)),
        v_a is None and not e_a and kinds(v_a0) == "FAIL" and v_g is None and not e_g and kinds(v_g0) == "FAIL")
    # NC22 an excerpt whose FIRST line is `$`-relative (S-199)
    e_l, v_l = pasm_verdict("jmp #$-1\n", ["lead:1"])
    _e, v_l0 = pasm_verdict("jmp #$-1\n", [])
    rec("22", "first line `jmp #$-1`: `lead:1` (one nop before) passes; without it fails", "PASS / FAIL",
        "%s %s / %s" % (kinds(v_l), e_l, kinds(v_l0)), v_l is None and not e_l and kinds(v_l0) == "FAIL")
    # NC23 net 3 (S-256): one-line code under a reviewed non-code key
    def kinds_of(rep):
        return [p.kind for p in rep["problems"]]

    line23 = "a:\n  correct: result := value * 2\n"
    r23a = evaluate(nc_root_text(line23, lambda cs: None), files=None, strict=True)
    rec("23a", "one-line `correct: result := value * 2` under a net-3 key with no manifest entry", "UNCLASSIFIED",
        str(kinds_of(r23a)), kinds_of(r23a) == ["UNCLASSIFIED"])
    r23b = evaluate(nc_root_text(line23, lambda cs: [ent(cs[0], compile="fragment", wrap="spin2-method",
                                                          assumes=["result", "value"])]),
                    files=None, strict=True)
    rec("23b", "the same line decided `fragment` with its assumes", "PASS", nc_summary(r23b), kinds_of(r23b) == [])
    r23c = nc_root_text("a:\n  syntax: result := value * 2\n", lambda cs: [])
    pf23, _c = find_candidates(r23c, ["nc.yaml"], {"code"}, {"correct", "prose"})
    rec("23c", "the same string under `syntax:` (not a net-3 key) is not a candidate", "no candidate",
        str([c.addr for c in pf23["nc.yaml"]]), pf23["nc.yaml"] == [])
    prose23 = "a:\n  prose: Some plain words here\n"
    r23d = evaluate(nc_root_text(prose23, lambda cs: None), files=None, strict=True)
    r23e = evaluate(nc_root_text(prose23, lambda cs: [ent(cs[0], compile="not-code", reason="nc: prose")]),
                    files=None, strict=True)
    rec("23d", "prose under a net-3 key is UNCLASSIFIED until a `not-code` entry with a reason is added",
        "UNCLASSIFIED / PASS", "%s / %s" % (kinds_of(r23d), nc_summary(r23e)),
        kinds_of(r23d) == ["UNCLASSIFIED"] and kinds_of(r23e) == [])
    # NC24 D3 (S-389): a bare constant as a PASM D/S operand
    d3_con = "CON\n  myc = 5\n\nDAT\n        org 0\n        mov flag, myc\nflag    long 0\n"
    r24a = nc_run([d3_con], lambda cs: [ent(cs[0], compile="program")])
    rec("24a", "`mov flag, myc` with `CON myc = 5` in the block", "BARE-CONST", nc_summary(r24a),
        kinds_of(r24a) == ["BARE-CONST"])
    r24b = nc_run(["mov flag, TRUE\n"], lambda cs: [ent(cs[0], compile="fragment", wrap="pasm2-dat", assumes=["flag"])])
    rec("24b", "`mov flag, TRUE` (built-in constant)", "BARE-CONST", nc_summary(r24b), kinds_of(r24b) == ["BARE-CONST"])
    r24c = nc_run(["mov flag, limit\n"], lambda cs: [ent(cs[0], compile="fragment", wrap="pasm2-dat",
                                                         assumes=["flag", "limit=con"])])
    rec("24c", "`mov flag, limit` with `assumes: limit=con` and no CON in the block", "BARE-CONST",
        nc_summary(r24c), kinds_of(r24c) == ["BARE-CONST"])
    clean24 = ("CON\n  myc = 5\n\nDAT\n        org 0\n        mov flag, #myc\n        mov flag, #FALSE\n"
               "        mov flag, ##TRUE\n        mov flag, ##myc\n        mov flag, buf\n        mov flag, 5\n"
               "flag    long TRUE\nbuf     long 0\n")
    r24d = nc_run([clean24, "mov flag, limit\n"],
                  lambda cs: [ent(cs[0], compile="program"),
                              ent(cs[1], compile="fragment", wrap="pasm2-dat", assumes=["flag", "limit"])])
    rec("24d", "`#myc`, `#FALSE`, `##TRUE`, `##myc`, a label, a numeral, a `long TRUE` directive and a plain-operand "
        "assume are NOT bare constants", "PASS", nc_summary(r24d), kinds_of(r24d) == [])
    r24e = nc_run(["mov flag, TRUE\n"], lambda cs: [ent(cs[0], compile="fragment", wrap="pasm2-dat", assumes=["flag"],
                                                         bare_const_ok=["TRUE"], reason="nc: intended register read")])
    rec("24e", "`bare_const_ok: [TRUE]` with a reason is the escape", "PASS", nc_summary(r24e), kinds_of(r24e) == [])
    bad24 = validate_entry({"at": "x", "fp": "0" * 16, "compile": "fragment", "wrap": "pasm2-dat",
                            "bare_const_ok": ["TRUE"]}, "nc24")
    rec("24f", "`bare_const_ok` without a `reason` is an invalid entry", "validate_entry error",
        str(bad24[:1]), any("reason" in m for m in bad24))
    r24g = nc_run(["mov flag, TRUE\nmov flag, #9999\n"],
                  lambda cs: [ent(cs[0], compile="fragment", wrap="pasm2-dat", assumes=["flag"], finding="F-999")])
    rec("24g", "a block that FAILS to compile and also holds a bare constant reports both, each REGISTERED",
        "FAIL + BARE-CONST", "%s; registered %s" % (kinds_of(r24g), [p.registered for p in r24g["problems"]]),
        sorted(kinds_of(r24g)) == ["BARE-CONST", "FAIL"] and all(p.registered for p in r24g["problems"]))
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
    ap.add_argument("--apply", metavar="DECISIONS.json")
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
        if args.apply:
            code, rep = do_apply(root, args.apply)
            if args.json and rep is not None:
                write(args.json, json.dumps({"census": rep["census"], "counts": rep["counts"],
                                             "problems": [p.as_dict() for p in rep["problems"]]}, indent=1))
            return code
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
            _pf, census = find_candidates(root, kb_files(root), code_keys, load_oneline_keys(root))
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
