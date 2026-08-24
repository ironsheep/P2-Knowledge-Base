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
    4. THE TRUTH SIDE READS `*.md` ONLY, and ROW_RE additionally requires the
       constant in COLUMN 1 of a line beginning with `|`. Measured consequence,
       2026-08-24: the CURRENT-EDITION Spin2 v55 symbol table is not on the
       truth side at all. It lives in `sources/spin2-v55/spin2-v55-text.txt`
       (a .txt, so never globbed) and its rows are TAB-indented with the %value
       in column 1 and the NAME in column 2 (so ROW_RE would not match it even
       if the glob did). That table carries 100 distinct P_ constants; the truth
       side currently merges 120, drawn from v51-era .md extracts. So wherever
       v55 ADDED or RE-DESCRIBED a constant, this instrument is auditing the KB
       against the SUPERSEDED edition and cannot say so.
       This is a FILE-TYPE and ROW-SHAPE gap -- emphatically NOT a TRUTH_ROOTS
       question. The roots are correct and must not be widened (see above).
       Left unfixed by the §10a detector pass deliberately: out of that task's
       stated scope, and widening the harvest moves the counts. Closing it is a
       scope decision that belongs with §10b, because arming this as a blocking
       gate certifies a harvest that never read the current authority edition.

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
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
KB_ROOT = REPO / "deliverables" / "ai" / "P2"
INGEST_ROOT = REPO / "engineering" / "ingestion"

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
    INGEST_ROOT / "smart-pins-catalog",      # v51 doc extracts, per smart-pin mode
]
TRUTH_EXCLUDED = [
    (INGEST_ROOT / "external-inputs", "upstream input material, not authority"),
    (INGEST_ROOT / "external-sources", "empirical ledger — outranks docs, but not a "
                                       "constant-definition table"),
    (INGEST_ROOT / "extracted-documentation", "raw extraction staging, superseded by sources/"),
]

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
ROW_RE = re.compile(rf"^\|\s*{_N}\s*(?:\((?:default|alias)\))?\s*\|(.+)$")
BULLET_RE = re.compile(rf"^\s*[-*]\s*{_N}\s*:\s*(.+?)\s*$")

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
    return raw.strip()


def harvest_source(prefix):
    """Build the truth table from ingestion pipe tables. Auto-discovered."""
    truth, files = {}, []
    pending_headings = {}        # heading-form defs, merged after the walk (see below)
    candidates = sorted({p for root in TRUTH_ROOTS if root.is_dir()
                         for p in root.rglob("*.md")})
    for path in candidates:
        rows = {}
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for n, line in enumerate(lines, 1):
            m = ROW_RE.match(line) or BULLET_RE.match(line)
            if not m:
                continue
            name, rest = m.group(1), m.group(2)
            if not name.startswith(prefix):
                continue
            desc = strip_desc(rest)
            if not desc or set(desc) <= set("-: "):
                continue
            rows[name] = (desc, f"{path.relative_to(REPO)}:{n}")
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
                        heading_rows[hm.group(1)] = (desc, f"{path.relative_to(REPO)}:{n}")
                    break

        if rows or heading_rows:
            files.append((path.relative_to(REPO), len(rows) + len(heading_rows)))
        for name, val in rows.items():
            truth.setdefault(name, val)
        for name, val in heading_rows.items():
            pending_headings.setdefault(name, val)

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
    print("\n" + ("Negative control PASSED -- the tool discriminates."
                  if ok else "Negative control FAILED -- do not trust this run."))
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
    print(f"PASS  no Tier 1 violations across {len(truth)} source-defined constant(s); "
          f"{len(tier2)} Tier 2 advisory/-ies to adjudicate")
    return 0


if __name__ == "__main__":
    sys.exit(main())
