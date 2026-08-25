#!/usr/bin/env python3
"""
audit-constant-fidelity.py - does the KB's DESCRIPTION of a named constant match
the source's, and does the KB agree with itself?

WHY THIS EXISTS
    On 2026-08-24 an agent consuming the published KB could not work out how to
    use pull-ups and pull-downs. The reason was not that the KB was vague. The
    KB said, in every file that mentioned them:

        P_HIGH_15K: "15kOhm pull-up (medium)"

    while the source it was extracted from says:

        | P_HIGH_15K | %..._0000000010000_..._0 | Drive high 15kOhm |

    The P2 has no pull-up resistors. `P_HIGH_*` selects DRIVE STRENGTH -- how
    hard the pin drives WHILE IT DRIVES -- and the KB reframed a whole family of
    them as always-on bias resistors. Sixteen constants, plus every worked
    example built on top of them (F-321..F-326).

    THE 2026-07-01 `P_*` AUDIT DID NOT CATCH THIS, AND COULD NOT HAVE.
    That audit asked "is this constant NAME legal in v55?" -- arbiter `pnut-ts`,
    enumeration the v55 manual -- and its answer still holds: every name here is
    legal. It never asked whether the DESCRIPTION attached to the name matches
    the source. `P_HIGH_15K` is a legal name carrying a wrong definition, and a
    name audit is blind to that by construction.

        Name coverage is not semantic coverage.

    This instrument audits the half that was never audited.

WHY A CONFLICT CHECK ALONE WOULD NOT HAVE FOUND IT
    Of the six findings that motivated this tool, exactly ONE was a conflict
    (two files giving contradictory mechanisms). The other five were UNANIMOUS
    ERROR: every file agreed with every other file, and they were all wrong
    together. A conflict detector finds disagreement; it is structurally blind
    to consensus. So this tool runs BOTH check families -- drift between files
    (conflict) and drift from the truth (fidelity) -- and the fidelity half is
    the one that would have saved the agent.

TWO TIERS, SPLIT BY WHAT EACH CAN BE CERTAIN ABOUT
  Tier 1 -- MECHANICAL, and it blocks. No judgement involved:
      UNDEFINED   the KB uses a constant the source defines, and no KB file
                  defines it. The reader has no way to learn what it means.
      ORPHAN      a KB file defines a constant NO source table carries. Either
                  the source set is incomplete or the definition is invented;
                  both need a human.
      DIVERGENT   two KB files define the same constant differently. One of
                  them is wrong and a consumer cannot tell which.
      QUANTITY    source and KB both state a magnitude for the same constant
                  and the magnitudes do not match (15kOhm vs 150kOhm).

  Tier 2 -- ADVISORY, and it does NOT block:
      CONTRADICT  source and KB assert concepts that cannot both be true of the
                  same constant (source "drive high", KB "pull-up").

    Tier 2 is advisory DELIBERATELY. Deciding whether two English phrases
    describe the same electrical behaviour is not something a regex can be
    trusted to settle, and a gate that cries wolf gets disabled during the first
    urgent release -- after which it detects nothing, forever. Advisory means a
    human adjudicates it, not that it is ignored. Note the consequence honestly:
    the pull-up defect that motivated this whole tool lands in TIER 2. Tier 1
    would not have caught it, because "15kOhm" and "15kOhm" agree perfectly --
    only the verb differs.

SCOPE
    Truth side  : pipe tables, bullet lines, and heading-form entries in the
                  ingestion tree that DEFINE constants (heading form is a
                  fallback -- see harvest_source). Auto-discovered; printed
                  by name under --inventory. Never hand-maintained, so it
                  cannot silently stop covering a file.
    Claim side  : every .yaml under deliverables/ai/P2/.

    A constant is "defined" by the KB only in Form A (a YAML mapping whose KEY
    is the constant). Form B (an end-of-line comment in a code example) is
    collected as a CLAIM but never as a definition -- a comment teaches the
    reader without ever declaring itself authoritative, which is precisely how
    the wrong examples in F-322 spread.

UNICODE
    Ohm and micro signs are LEGITIMATE here and are not defects. They are
    normalised (NFKC, then folded to ASCII tokens) before comparison, so the
    tool never reports a false difference between "15kOhm" and "15k-ohm" and
    never flags the characters themselves. That is a different gate's job.

KNOWN LIMITATIONS -- stated, because a silent one reads as coverage
    1. Source definitions written as a HEADING (`### P_DAC_DITHER_PWM`, with the
       description in following prose under a **Description**: label) ARE now
       harvested, but only as a FALLBACK -- used solely when no pipe-table or
       bullet form defines the same name anywhere in the truth tree. Fixed
       2026-08-24; the known instance was P_DAC_DITHER_PWM, at
       smart-pins-catalog/ingestionSources/mode-00011-.../spin2-v51-extract.md:11.
       Closing this gap also retired the silence around every OTHER
       constant defined only this way: nine more (P_STATE_TICKS, P_HIGH_TICKS,
       P_EVENTS_TICKS, P_PERIODS_TICKS, P_PERIODS_HIGHS, P_COUNTER_TICKS,
       P_COUNTER_HIGHS, P_COUNTER_PERIODS, P_DAC_DITHER_RND) turned out to be
       used by the KB and never formally defined by it -- real [UNDEFINED],
       not a fix side effect.
    2. Tier 2's concept lexicon is a fixed list. It catches the drive-vs-bias and
       invert-vs-true confusions it was built from; it is not a general semantic
       comparator and does not claim to be. A constant passing Tier 2 is NOT
       certified correct -- it is only "not caught by these checks".
    3. Coverage is per-CONSTANT. Prose ABOUT a constant that never names it --
       "the pin can be configured as an input with a bias resistor" -- is
       invisible to this tool. Name coverage is not semantic coverage, and that
       cuts both ways.
    4. CLOSED 2026-08-25, on the way to arming this as a blocking release gate.
       It read `*.md` only, and required the constant in COLUMN 1 of a line
       beginning with `|` -- so the CURRENT-EDITION Spin2 v55 symbol table was
       not on the truth side at all (a `.txt`, tab-indented, `%value` in column
       1 and the NAME in column 2). The instrument compared the KB against the
       SUPERSEDED v51 edition and could not say so. Fixed by reading `.txt` as
       well and parsing pipe rows BY CELL (see NAME_CELL_RE), with edition
       precedence (see EDITION_RE) so a later edition of the same source family
       supersedes an earlier one. NOT by widening TRUTH_ROOTS -- see the note on
       TRUTH_ROOTS for why that would have disarmed the check instead.

       What it actually cost, measured rather than estimated:
         * the v55 table carries 116 distinct P_ constants over 114 rows -- two
           rows name a constant AND its brevity alias (P_TRUE_OUTPUT/P_TRUE_OUT,
           P_INVERT_OUTPUT/P_INVERT_OUT). An earlier draft of this note said 100;
           that number was wrong (F-339).
         * ADDED: **0**. Every one of the 116 was already on the truth side.
         * RE-DESCRIBED: **20**, and that is the entire exposure the gap carried.
           19 of them change visibly; P_OR_AB is the twentieth and changes
           invisibly, because `strip_desc` keeps the last pipe-delimited cell and
           "Select A | B, B" truncates identically in both editions. That
           truncation self-cancels and is NOT a defect to fix -- the shipped KB
           record is correct as written; do not align it to the displayed "B, B".
         * Tier 1 and Tier 2 both stayed at 0: the KB side was already moved to
           the v55 wording, so adopting the current edition moved no count.
         * Four v51-only names (P_COMPARATOR, P_COMPARATOR_FB, P_FLOAT, P_PASS)
           are absent from v55. The KB neither defines nor references any of them,
           so they are carried but inert.

EXIT STATUS
    0  no Tier 1 violations (Tier 2 advisories may still be printed)
    1  one or more Tier 1 violations
    2  no source truth table could be built -- the tool has nothing to audit,
       which is a tooling failure, never a pass

USAGE
    audit-constant-fidelity.py [--inventory] [--advisory-only] [--prefix P_]
    audit-constant-fidelity.py --negative-control
"""

import argparse
import html
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
KB_ROOT = REPO / "deliverables" / "ai" / "P2"
INGEST_ROOT = REPO / "engineering" / "ingestion"

# Printed on EVERY run, pass or fail. This gate is armed and blocking in
# `release-yamls` and in `validate-dod-release.py`, and a green from a blocking
# gate gets read as a guarantee unless the gate says what it did not look at.
SCOPE_NOTE = (
    "WHAT THIS GREEN DOES NOT CERTIFY\n"
    "  This instrument checks NAMED CONSTANTS. Prose that describes a behaviour\n"
    "  without naming a constant passes untouched -- which is exactly how F-327's\n"
    "  fabricated drive ladder sat in a released file until a human read it.\n"
    "  Guide rules R6, R7 and R9 have no instrument and are held by review.\n"
    "  Name coverage is not semantic coverage. A clean run means NOT CAUGHT BY\n"
    "  THESE CHECKS -- never `correct`.")

# The truth side is AUTHORITY-SCOPED, and this is not a detail.
# {{DOMAIN_AUTHORITY}} ranks Parallax documentary sources under
# `ingestion/sources/`; `ingestion/external-inputs/` is upstream INPUT material
# -- handoff packages, vendor fact sheets, reviewer bundles -- and is explicitly
# NOT authority here.
#
# The first working version of this tool walked all of ingestion/, and an
# external-inputs fact sheet describing P_HIGH_15K as "15 kOhm equivalent"
# shadowed the real source's "Drive high 15kOhm". "Equivalent" carries no
# drive-high concept, so it did not clash with the KB's "pull-up" -- and the
# gate went SILENT on the exact defect it was built to catch. An unauthoritative
# source did not add a wrong answer; it DISARMED the check. Scope the truth side
# or the gate audits whatever it happens to find first.
TRUTH_ROOTS = [
    INGEST_ROOT / "sources",                 # Parallax documentary sources
    INGEST_ROOT / "smart-pins-catalog",      # doc extracts, per smart-pin mode
]
TRUTH_EXCLUDED = [
    (INGEST_ROOT / "external-inputs", "upstream input material, not authority"),
    (INGEST_ROOT / "external-sources", "empirical ledger — outranks docs, but not a "
                                       "constant-definition table"),
    (INGEST_ROOT / "extracted-documentation", "raw extraction staging, superseded by sources/"),
]

# ...AND THE SAME DISARM CAN HAPPEN INSIDE A CORRECT ROOT. F-341: six of OUR OWN
# derived analysis documents sit at the TOP LEVEL of `ingestion/sources/` --
# `p2-complete-signal-flow-matrix.md`, `p2-board-power-analysis-matrix.md` and
# four more -- self-describing as generated cross-references, naming no Parallax
# publication, and repeating the very pull-up mislabel this tool exists to kill.
# They contributed 0 truth entries under the old row shape, so the disarm was
# LATENT: a row shape away, not a policy away. Widening the harvest woke it up.
# Measured 2026-08-25 with the repaired row parser and this rule OFF:
# `p2-complete-signal-flow-matrix.md:100` -- a SIGNAL-FLOW table whose last cell
# happens to be a constant name -- defined `P_PWM_SAWTOOTH` as "P38".
#
# The discriminator is structural, not a hand-kept list: an INGESTED SOURCE IS A
# DIRECTORY. Every real source under `sources/` lives in its own folder
# (`spin2-v55/`, `p2-datasheet/`, `silicon-doc/`, ...) because that is what the
# ingestion process creates. A loose file sitting at the root of a truth root was
# put there by something else, and it is not an ingested source document. So the
# rule catches the next stray file too, which a list of six names cannot.
MIN_DEPTH_BELOW_ROOT = 1

# Rows/lines that DEFINE a constant. FIVE shapes live in the tree, and the
# first pass of this tool only handled the first two -- which manufactured
# false ORPHANs for every constant defined in the other two. An incomplete
# truth side does not read as "unknown", it reads as "the KB invented this".
#   | NAME | Description |                    2-col symbol table
#   | NAME | %value | Description |           3-col catalog extract
#   | `NAME` | Description |                  backticked (pnut_ts fact sheets)
#   - **NAME**: Description                   bullet form
#   ### NAME                                  heading form (desc on a later line)
_N = r"[`*]{0,2}\s*([A-Z][A-Z0-9_]{2,})\s*[`*]{0,2}"
BULLET_RE = re.compile(rf"^\s*[-*]\s*{_N}\s*:\s*(.+?)\s*$")

# A pipe row is parsed BY CELL, not by a fixed column. The first version pinned
# the constant to COLUMN 1 of a line that begins with `|`, and the CURRENT
# authority edition satisfies neither half: the Spin2 v55 symbol table is
# TAB-INDENTED (so `^\|` misses it) with the `%value` in column 1 and the NAME in
# column 2 (so column 1 misses it). Consequence, measured: the truth side was
# built entirely from v51-era extracts and audited the KB against the SUPERSEDED
# edition without being able to say so.
#
# The NAME CELL is the first cell that is WHOLLY a constant name -- optionally
# carrying `(default)` / `(alias)` / `(for brevity)`, and optionally naming a
# second, brevity-alias constant (v55 does this twice). The DESCRIPTION is the
# last other non-empty cell, which is what `strip_desc` already did.
#
# The name cell must be one of the FIRST TWO cells, and that bound is load-
# bearing rather than cosmetic. A DEFINITION table names the symbol and then
# describes it; a table that mentions a constant in its LAST column is using it,
# not defining it. Without the bound, `p2-complete-signal-flow-matrix.md`'s
# signal-flow table (Function | Source | Conditioning | ... | Smart Pin Config)
# defined `P_PWM_SAWTOOTH` as "P38" -- the pin number in the neighbouring cell.
NAME_CELL_RE = re.compile(
    r"^[`*]{0,2}\s*([A-Z][A-Z0-9_]{2,})\s*[`*]{0,2}"
    r"(?:\s*\((?:default|alias|for brevity)\))?"
    r"(?:\s+[`*]{0,2}([A-Z][A-Z0-9_]{2,})[`*]{0,2}\s*\((?:default|alias|for brevity)\))?$",
    re.IGNORECASE)
NAME_CELL_MAX_INDEX = 1

# A LATER EDITION OF THE SAME SOURCE SUPERSEDES AN EARLIER ONE, and the harvest
# has to say so or the gate audits the KB against a retired document. Parsed
# from the path (`spin2-v51/...`, `spin2-v55/...`, `spin2-v51-extract.md`), so it
# needs no per-file configuration. Scoped to the SAME FAMILY on purpose: `v55`
# beating `v51` is an edition statement, and it must not become `spin2-v55`
# silently outranking an unrelated source that happens to carry a lower number.
EDITION_RE = re.compile(r"(?:^|[/\-])([a-z0-9]+)-v(\d+)(?:[/\-.]|$)")

# Heading form -- `### NAME` on its own line, definition in the prose that
# follows under a **Description**: label, before the next heading or a rule.
# THIS IS A FALLBACK, harvested in a pass that runs only after every
# row/bullet definition has already claimed its name (see harvest_source) --
# a table or bullet always outranks a heading, regardless of which file the
# scan visits first. Without this a constant defined ONLY this way reads as
# source-silent: [ORPHAN] when the KB defines it too (P_DAC_DITHER_PWM,
# smart-pins-catalog/.../mode-00011-.../spin2-v51-extract.md:11), or simply
# invisible when the KB uses it without ever defining it.
HEADING_RE = re.compile(rf"^#{{1,6}}\s*{_N}\s*$")
HEADING_DESC_RE = re.compile(r"^\*\*Description\*\*:\s*(.+?)\s*$")
HEADING_BOUNDARY_RE = re.compile(r"^(#{1,6}\s|-{3,}\s*$)")

# Form A: a YAML mapping whose key IS the constant.
DEF_RE = re.compile(r'^\s*"?([A-Z][A-Z0-9_]{2,})"?\s*:\s*(.+?)\s*$')

# Form C: a record catalogue -- `symbol_name: "P_X"` ... `description: "..."`.
RECORD_RE = re.compile(r'^\s*-?\s*symbol_name\s*:\s*"?([A-Z][A-Z0-9_]{2,})"?\s*$')
RECORD_DESC_RE = re.compile(r'^\s*description\s*:\s*(.+?)\s*$')

# ...but ONLY outside a per-mode PARAMETER table. `mode_specific_x_values:` maps
# each mode to what X means IN that mode -- "Bit period for receive" is a facet
# of P_ASYNC_RX, not a rival definition of it. Treating those as definitions
# made every mode look like it had 3 contradictory meanings. They are claims.
FACET_PARENT_RE = re.compile(
    r"^\s*(mode_specific_\w+|[xy]_(?:values|parameters?|meanings?)"
    r"|\w*parameters?|\w*_per_mode|\w*_by_mode)\s*:\s*$")

# Form B: an end-of-line comment in an embedded code example -> a CLAIM only.
COMMENT_RE = re.compile(r"^(?P<code>.*\b(?P<const>[A-Z][A-Z0-9_]{2,})\b.*?)'\s*(?P<text>.+?)\s*$")

# Magnitudes the descriptions actually carry.
QTY_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(k?ohm|kohm|ohm|ma|ua|na|mhz|khz|hz|v|bit|pin)\b")

# Concepts that cannot both be true of one constant. Tier 2.
CONCEPTS = {
    "drive_high": (r"\bdrive[s]?\s+high\b",),
    "drive_low": (r"\bdrive[s]?\s+low\b",),
    "float": (r"\bfloat(?:s|ing)?\b",),
    "bias_up": (r"\bpull[\s_-]?up\b",),
    "bias_down": (r"\bpull[\s_-]?down\b",),
    "invert": (r"\binvert(?:ed|s)?\b",),
    "true": (r"\btrue\b",),
}
INCOMPATIBLE = [
    ("drive_high", "bias_up"),
    ("drive_low", "bias_down"),
    ("drive_high", "drive_low"),
    ("bias_up", "bias_down"),
    ("float", "drive_high"),
    ("float", "drive_low"),
    ("invert", "true"),
]


def fold(text):
    """Normalise for comparison. Unicode here is legitimate, never a finding."""
    t = unicodedata.normalize("NFKC", text)
    t = (t.replace("Ω", "ohm").replace("Ω", "ohm").replace("μ", "u")
          .replace("µ", "u").replace("−", "-"))
    t = t.lower()
    t = re.sub(r"[‐-―]", "-", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def quantities(text):
    """Magnitudes stated in a description, unit-normalised."""
    out = set()
    for num, unit in QTY_RE.findall(fold(text).replace("k ohm", "kohm")):
        unit = {"kohm": "ohm_k", "ohm": "ohm"}.get(unit, unit)
        val = float(num)
        if unit == "ohm_k":
            val, unit = val * 1000, "ohm"
        out.add((val, unit))
    return out


def concepts_in(text):
    t = fold(text)
    return {name for name, pats in CONCEPTS.items() if any(re.search(p, t) for p in pats)}


def strip_desc(raw):
    """Last cell of a pipe row, or the value half of a YAML mapping."""
    cells = [c.strip() for c in raw.split("|") if c.strip()]
    if cells:
        raw = cells[-1]
    raw = raw.strip().strip('"').strip("'")
    raw = re.sub(r"\s*#.*$", "", raw)
    # The v55 text extract carries HTML entities (`Select A &amp; B, B`,
    # `A &gt; Level`). They are an artifact of the extraction, not a difference
    # from the v51 wording, and leaving them in would report 6 spurious
    # description changes the moment the current edition joined the truth side.
    return html.unescape(raw).strip()


def source_edition(rel):
    """(family, edition) parsed from a path, or (None, None)."""
    m = EDITION_RE.search(str(rel).lower())
    return (m.group(1), int(m.group(2))) if m else (None, None)


def parse_row(line, prefix):
    """(names, description) for a pipe row that DEFINES a constant, else None."""
    s = line.strip()
    if not s.startswith("|"):
        return None
    cells = [c.strip() for c in s.strip("|").split("|")]
    if len(cells) < 2:
        return None
    for i, cell in enumerate(cells[:NAME_CELL_MAX_INDEX + 1]):
        m = NAME_CELL_RE.match(cell)
        if not m:
            continue
        names = [g for g in m.groups() if g and g.startswith(prefix)]
        if not names:
            continue
        rest = [c for j, c in enumerate(cells) if j != i and c]
        if not rest:
            return None
        return names, rest[-1]
    return None


def truth_candidates():
    """Every file the truth side is allowed to read, and why.

    Two filters, both structural: the FILE TYPE (a source extract is `.md` or
    `.txt` -- the current-edition Spin2 symbol table is the latter), and the
    DEPTH (an ingested source is a directory under a truth root; a loose file at
    the root is not one -- see MIN_DEPTH_BELOW_ROOT)."""
    out = []
    for root in TRUTH_ROOTS:
        if not root.is_dir():
            continue
        for pattern in ("*.md", "*.txt"):
            for p in root.rglob(pattern):
                if len(p.relative_to(root).parts) > MIN_DEPTH_BELOW_ROOT:
                    out.append(p)
    return sorted(set(out))


def _edition_wins(cur, new):
    """Does `new` (family, edition) supersede `cur`? Same family, higher number."""
    cur_fam, cur_ed = cur
    new_fam, new_ed = new
    return bool(new_fam and new_fam == cur_fam and new_ed and cur_ed and new_ed > cur_ed)


def _claim(table, name, val):
    """First definition wins -- EXCEPT that a later edition of the same source
    family supersedes an earlier one. Without the exception the walk order
    decides which edition the gate audits against, which is not a decision a
    filesystem should be making."""
    cur = table.get(name)
    if cur is None:
        table[name] = val
        return
    if _edition_wins((cur[2], cur[3]), (val[2], val[3])):
        table[name] = val


def harvest_source(prefix):
    """Build the truth table from ingestion definition tables. Auto-discovered."""
    truth, files = {}, []
    pending_headings = {}        # heading-form defs, merged after the walk (see below)
    candidates = truth_candidates()
    for path in candidates:
        rows = {}
        fam, ed = source_edition(path.relative_to(REPO))
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for n, line in enumerate(lines, 1):
            names, rest = None, None
            r = parse_row(line, prefix)
            if r:
                names, rest = r
            else:
                m = BULLET_RE.match(line)
                if m and m.group(1).startswith(prefix):
                    names, rest = [m.group(1)], m.group(2)
            if not names:
                continue
            desc = strip_desc(rest)
            if not desc or set(desc) <= set("-: "):
                continue
            for name in names:
                rows[name] = (desc, f"{path.relative_to(REPO)}:{n}", fam, ed)
        heading_rows = {}
        for n, line in enumerate(lines, 1):
            hm = HEADING_RE.match(line)
            if not hm or not hm.group(1).startswith(prefix):
                continue
            for look in lines[n:n + 20]:
                if HEADING_BOUNDARY_RE.match(look):
                    break
                dm = HEADING_DESC_RE.match(look)
                if dm:
                    desc = strip_desc(dm.group(1))
                    if desc and not set(desc) <= set("-: "):
                        heading_rows[hm.group(1)] = (
                            desc, f"{path.relative_to(REPO)}:{n}", fam, ed)
                    break

        if rows or heading_rows:
            files.append((path.relative_to(REPO), len(rows) + len(heading_rows)))
        for name, val in rows.items():
            _claim(truth, name, val)
        for name, val in heading_rows.items():
            _claim(pending_headings, name, val)

    # Heading form is a FALLBACK, and this is where that is enforced: the merge
    # runs only after EVERY row/bullet definition in the whole truth tree has
    # claimed its name above, so a heading can fill a name still missing but can
    # never override one. Deliberate, and independent of which directory the
    # filesystem walk happens to visit first -- which is exactly why the merge
    # lives out here rather than inside the loop.
    for name, val in pending_headings.items():
        truth.setdefault(name, val)
    return truth, files


def harvest_kb(prefix):
    """Definitions (Form A) and claims (Form B) from the shipped YAML."""
    defs, claims, used = defaultdict(list), defaultdict(list), defaultdict(set)
    for path in sorted(KB_ROOT.rglob("*.yaml")):
        rel = path.relative_to(REPO)
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        facet_indent = None          # inside a per-mode parameter table?
        for n, line in enumerate(lines, 1):
            indent = len(line) - len(line.lstrip())
            if line.strip() and facet_indent is not None and indent <= facet_indent:
                facet_indent = None
            if FACET_PARENT_RE.match(line):
                facet_indent = indent
            for name in re.findall(rf"\b({prefix}[A-Z0-9_]+)\b", line):
                used[name].add(str(rel))
            m = DEF_RE.match(line)
            if m and m.group(1).startswith(prefix):
                desc = strip_desc(m.group(2))
                if desc and not desc.startswith(("|", ">", "&", "*")) and len(desc) > 2:
                    # Inside a facet table this is a per-mode parameter meaning,
                    # not a definition of the constant. Record it as a claim so
                    # fidelity still checks it, but never as a rival definition.
                    bucket = claims if facet_indent is not None else defs
                    bucket[m.group(1)].append((desc, f"{rel}:{n}"))
            # Record form: a list-of-records symbol catalogue, where the
            # constant is the VALUE of `symbol_name:` and its definition is the
            # `description:` field of the same record -- not a key anywhere.
            # Missing this form made 60+ correctly-defined constants read as
            # UNDEFINED, i.e. the tool reported the KB's BEST file as its worst.
            r = RECORD_RE.match(line)
            if r and r.group(1).startswith(prefix):
                for look in lines[n:n + 12]:
                    if RECORD_RE.match(look):
                        break
                    d = RECORD_DESC_RE.match(look)
                    if d:
                        desc = strip_desc(d.group(1))
                        if desc and len(desc) > 2:
                            defs[r.group(1)].append((desc, f"{rel}:{n}"))
                        break

            c = COMMENT_RE.match(line)
            if c and c.group("const").startswith(prefix):
                txt = c.group("text").strip()
                if txt and len(txt) > 2:
                    claims[c.group("const")].append((txt, f"{rel}:{n}"))
    return defs, claims, used


def audit(prefix):
    truth, src_files = harvest_source(prefix)
    if not truth:
        return None, None, None, src_files, truth
    defs, claims, used = harvest_kb(prefix)
    tier1, tier2 = [], []

    for name in sorted(set(defs) | set(used) | set(truth)):
        kb_defs = defs.get(name, [])
        src = truth.get(name)

        # Tier 1 -- DIVERGENT: the KB CONTRADICTS itself. Differing is not
        # diverging. Two files can describe one constant from different angles
        # and both be right; that is complementary coverage, and firing on it
        # buries the real conflicts. So require an actual clash -- incompatible
        # concepts, or two different magnitudes for the same thing.
        for i in range(len(kb_defs)):
            for j in range(i + 1, len(kb_defs)):
                (d1, l1), (d2, l2) = kb_defs[i], kb_defs[j]
                if fold(d1) == fold(d2):
                    continue
                c1, c2 = concepts_in(d1), concepts_in(d2)
                q1, q2 = quantities(d1), quantities(d2)
                clash = [(a, b) for a, b in INCOMPATIBLE
                         if (a in c1 and b in c2) or (b in c1 and a in c2)]
                if clash or (q1 and q2 and not (q1 & q2)):
                    why = (", ".join(f"{a}/{b}" for a, b in sorted(set(clash)))
                           if clash else "different magnitudes")
                    tier1.append(("DIVERGENT", name,
                                  f"{l1} -> \"{d1}\"  VS  {l2} -> \"{d2}\"  [{why}]"))

        # Tier 1 -- ORPHAN: defined by the KB, carried by no source table.
        if kb_defs and not src:
            tier1.append(("ORPHAN", name,
                          f"defined at {kb_defs[0][1]} but no source table defines it"))

        # Tier 1 -- UNDEFINED: source defines it, KB uses it, KB never defines it.
        if src and not kb_defs and used.get(name):
            n_files = len(used[name])
            tier1.append(("UNDEFINED", name,
                          f"used in {n_files} KB file(s), defined in none; "
                          f"source has it at {src[1]} -> \"{src[0]}\""))

        if not src:
            continue

        # Tier 1 -- QUANTITY, and Tier 2 -- CONTRADICT, over every KB assertion.
        src_q, src_c = quantities(src[0]), concepts_in(src[0])
        for desc, loc in kb_defs + claims.get(name, []):
            kb_q = quantities(desc)
            if src_q and kb_q and not (src_q & kb_q):
                tier1.append(("QUANTITY", name,
                              f"{loc}: KB says \"{desc}\"; source says \"{src[0]}\" ({src[1]})"))
            clash = [(a, b) for a, b in INCOMPATIBLE
                     if (a in src_c and b in concepts_in(desc))
                     or (b in src_c and a in concepts_in(desc))]
            if clash:
                pair = ", ".join(f"{a}/{b}" for a, b in sorted(set(clash)))
                tier2.append(("CONTRADICT", name,
                              f"{loc}: KB says \"{desc}\"; source says \"{src[0]}\" "
                              f"[{pair}] ({src[1]})"))
    return tier1, tier2, (defs, claims, used), src_files, truth


def negative_control(prefix):
    """A check that cannot fail has not been verified, it has been run."""
    print("NEGATIVE CONTROL -- proving the tool can fail and can pass\n")
    ok = True
    src = "Drive high 15kOhm"
    for label, kb, want in [
        ("known-bad  (the F-321 shape)", "15kΩ pull-up (medium)", True),
        ("known-good (source wording)", "Drive high 15kΩ", False),
        ("known-bad  (wrong magnitude)", "Drive high 150kΩ", "qty"),
    ]:
        clash = any((a in concepts_in(src) and b in concepts_in(kb))
                    or (b in concepts_in(src) and a in concepts_in(kb))
                    for a, b in INCOMPATIBLE)
        qty = bool(quantities(src) and quantities(kb) and not (quantities(src) & quantities(kb)))
        fired = "CONTRADICT" if clash else ("QUANTITY" if qty else "-")
        expect = {True: "CONTRADICT", False: "-", "qty": "QUANTITY"}[want]
        good = fired == expect
        ok &= good
        print(f"  [{'PASS' if good else 'FAIL'}] {label}: fired={fired:<10} expected={expect}")
    # ---- THE HARVEST HALF ----------------------------------------------------
    # The comparator cases above prove the tool can tell a wrong description from
    # a right one. They say NOTHING about whether it read the right document, and
    # that is the half that failed: for its whole life this instrument compared
    # the KB against the SUPERSEDED v51 edition while the current v55 symbol
    # table sat unread in a `.txt`. A comparator that works perfectly on the
    # wrong truth is a gate that cannot fail.
    print("\nHARVEST -- proving the truth side reads the right rows, and only those\n")
    row_cases = [
        ("v55 shape: tab-indented, %value col 1, NAME col 2",
         "\t| %0000_0000_000_0000000010000_00_00000_0 | P_HIGH_15K | Drive high 15kOhm",
         (["P_HIGH_15K"], "Drive high 15kOhm")),
        ("v51 shape: NAME col 1, 2 cells",
         "| P_HIGH_15K | Drive high 15kOhm |", (["P_HIGH_15K"], "Drive high 15kOhm")),
        ("v51 shape: NAME col 1, 3 cells",
         "| P_HIGH_15K | %0001 | Drive high 15kOhm |", (["P_HIGH_15K"], "Drive high 15kOhm")),
        ("backticked NAME (pnut_ts fact sheets)",
         "| `P_HIGH_15K` | Drive high 15kOhm |", (["P_HIGH_15K"], "Drive high 15kOhm")),
        ("(default) annotation is not part of the name",
         "\t| %0000 | P_TT_00 (default) | TT = %00", (["P_TT_00"], "TT = %00")),
        ("a brevity-alias row defines BOTH names",
         "\t| %0000 | P_TRUE_OUTPUT (default) P_TRUE_OUT (for brevity) | Select true output",
         (["P_TRUE_OUTPUT", "P_TRUE_OUT"], "Select true output")),
        ("a section header row defines nothing",
         "\t| Drive-High Strength | (pick one) | (for Logic modes)", None),
        ("a bit-field row with no name defines nothing",
         "\t| %xxxx_xxxx_xxx_xxxxxxxHHHxxx_xx_xxxxx_x |  | Drive-high selector bits", None),
        ("F-341 SHAPE: a constant in the LAST cell is a USE, not a definition "
         "— MUST NOT DEFINE",
         "| Filter Control | Digital | RC Filter | Pin 7 | P6 | P38 | P_PWM_SAWTOOTH |",
         None),
    ]
    for label, line, want in row_cases:
        got = parse_row(line, prefix)
        if got is not None:
            got = (got[0], strip_desc(got[1]))
        good = got == want
        ok &= good
        print(f"  [{'PASS' if good else 'FAIL'}] {label}\n"
              f"         got={got!r}")

    print()
    struct_cases = [
        ("HTML entities in the v55 extract are unescaped, not a difference",
         strip_desc("Select A &amp; B, B") == "Select A & B, B"),
        ("a loose file at a truth root is NOT an ingested source (F-341)",
         all(len(p.relative_to(r).parts) > MIN_DEPTH_BELOW_ROOT
             for r in TRUTH_ROOTS if r.is_dir() for p in truth_candidates()
             if str(p).startswith(str(r)))),
        ("a later edition of the SAME family supersedes an earlier one",
         _edition_wins(("spin2", 51), ("spin2", 55)) is True),
        ("an earlier edition does NOT supersede a later one",
         _edition_wins(("spin2", 55), ("spin2", 51)) is False),
        ("a DIFFERENT family never supersedes on edition number alone",
         _edition_wins(("spin2", 51), ("silicon", 35)) is False),
    ]
    for label, good in struct_cases:
        ok &= bool(good)
        print(f"  [{'PASS' if good else 'FAIL'}] {label}")

    # ...and the live harvest, because a control that only runs on constructed
    # strings proves the parser, never the run. "Nothing audited" is never a pass.
    print()
    truth, files = harvest_source(prefix)
    live = [
        (f"the truth side is non-empty ({len(truth)} constants)", bool(truth)),
        (f"the truth side includes the CURRENT edition ({sum(1 for r, _ in files if 'v55' in str(r))} v55 file(s))",
         any("v55" in str(r) for r, _ in files)),
        ("no derived analysis document contributes a definition",
         not any(("matrix" in r.name or "knowledge" in r.name or "checklist" in r.name)
                 for r, _ in files)),
    ]
    for label, good in live:
        ok &= bool(good)
        print(f"  [{'PASS' if good else 'FAIL'}] {label}")

    print("\n" + ("Negative control PASSED -- the tool discriminates, and it "
                  "discriminates against the CURRENT edition."
                  if ok else "Negative control FAILED -- do not trust this run."))
    print("\n" + SCOPE_NOTE)
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--inventory", action="store_true",
                    help="print the source tables and coverage, then audit")
    ap.add_argument("--advisory-only", action="store_true",
                    help="print Tier 2 only; always exits 0")
    ap.add_argument("--prefix", default="P_", help="constant prefix to audit (default P_)")
    ap.add_argument("--negative-control", action="store_true",
                    help="prove the tool can fail; audits nothing")
    args = ap.parse_args()

    if args.negative_control:
        return negative_control(args.prefix)

    tier1, tier2, harvest, src_files, truth = audit(args.prefix)
    if tier1 is None:
        print("ERROR  no source definition table found under "
              f"{INGEST_ROOT.relative_to(REPO)} for prefix {args.prefix!r}.")
        print("       The tool has nothing to audit. This is a tooling failure, not a pass.")
        return 2

    defs, claims, used = harvest
    if args.inventory:
        print("SOURCE TABLES (auto-discovered -- the truth side)")
        for rel, n in src_files:
            print(f"  {n:>4} definitions   {rel}")
        print(f"  {len(truth):>4} distinct constants after merge\n")
        print("KB COVERAGE (the claim side)")
        print(f"  {len(defs):>4} constants defined in the KB")
        print(f"  {sum(len(v) for v in claims.values()):>4} in-example comment claims")
        print(f"  {len(used):>4} constants referenced anywhere in the KB\n")

    if not args.advisory_only:
        if tier1:
            print(f"TIER 1 -- MECHANICAL ({len(tier1)}) -- these block\n")
            for kind, name, detail in sorted(tier1):
                print(f"  [{kind}] {name}\n        {detail}")
            print()
        else:
            print("TIER 1 -- MECHANICAL: none\n")

    if tier2:
        print(f"TIER 2 -- ADVISORY ({len(tier2)}) -- a human adjudicates these\n")
        for kind, name, detail in sorted(tier2):
            print(f"  [{kind}] {name}\n        {detail}")
        print()
    else:
        print("TIER 2 -- ADVISORY: none\n")

    if args.advisory_only:
        return 0
    if tier1:
        print(f"FAIL  {len(tier1)} Tier 1 violation(s); "
              f"{len(tier2)} Tier 2 advisory/-ies to adjudicate")
        return 1
    editions = sorted({f"{fam}-v{ed}" for _, _, fam, ed in truth.values() if fam})
    print(f"PASS  no Tier 1 violations across {len(truth)} source-defined constant(s); "
          f"{len(tier2)} Tier 2 advisory/-ies to adjudicate")
    print(f"      truth side built from {len(src_files)} source file(s), "
          f"edition(s): {', '.join(editions) or 'unversioned'}")
    print()
    print(SCOPE_NOTE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
