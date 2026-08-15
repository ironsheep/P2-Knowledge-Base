#!/usr/bin/env python3
"""
audit-guide-conformance.py — the guide layer's first automated gate.

WHAT THIS GUARDS
----------------
The *guide layer* is what an author reads before writing a word: the house
voice canon, the app-note class guides, and each manual's own voice / creation /
style guides. Nothing has ever checked it. The 2026-08 propagation study read
all ten guides by hand and found roughly a hundred defects across five classes —
every one of which would have misdirected an author, and four of which a hand
count got wrong at least once.

This script replaces the hand count. Each detection below corresponds to a
defect class that study found by reading.

THE FIVE DETECTIONS
-------------------
  D1  RESTATED VOICE RULE
      A hedging or cadence rule stated ANYWHERE outside the catalog. The
      catalog is the single home of R1-R4; a guide states its local
      ADOPT/ADAPT/REJECT decision, never the rule itself.

      Worst form, and never exempt: a WORD BLACKLIST naming
      may / might / probably / typically / usually. Those words are R1
      compliance ("calibrated confidence") as often as they are defects, so a
      blacklist orders an author to strip exactly the qualifiers R1 requires.
      A checklist carrying one is a counter-order that wins, because a
      checklist is what an auditor runs mechanically.

      A prose hedging rule IS exempt when it is already reconciled the way the
      Assembly guide models it: scoped to *vague* hedging AND carrying a
      cross-reference to the local calibrated-confidence section.

  D2  TOOL NAME
      The underscore forms `pnut_ts` / `pnut_term_ts`, which DO NOT EXIST.
      /usr/local/bin holds only `pnut-ts`; an author or reader who types the
      underscore form gets "command not found". Product names are PNut-TS and
      PNut-Term-TS; invocations are pnut-ts and pnut-term-ts.

  D3  DEAD CITED PATH
      A repo path cited as a source or authority that does not resolve on
      disk. Two of these were PRIMARY-authority citations: an author following
      them finds nothing where the trust chain's authority should be.

  D4  CODENAME
      "Green Book" / "Blue Book" / "Silicon Doc" against the official-titles
      rule. A codename is unsearchable to a newcomer.

  D5  RETIRED-DOC REFERENCE
      A roster-Abandoned document presented as a live, current sibling manual.
      The retired set is read from PUBLICATION-ROSTER.md, not hard-coded.

DELIBERATE MENTIONS ARE NOT DEFECTS
-----------------------------------
Some guides name the wrong form ON PURPOSE in order to declare it wrong — those
passages are the AUTHORITY for the D2 sweep, and "fixing" them would delete the
rule. Likewise a guide may cite a retired document as lineage ("adopted from
...") or history, which is true and stays. D2, D4 and D5 therefore recognise
declared-wrong / lineage phrasing, and every such exemption is PRINTED with its
location — an exemption you cannot see is indistinguishable from a miss.

THE FILE SET IS GLOBBED, NEVER HAND-MAINTAINED
----------------------------------------------
A hand-maintained file list drifts behind the files and then reads green because
it simply did not run. Every scanned file is discovered by glob. Exclusions are
derived from the publication roster (retired elements) plus one named private
document, and ALL of them are printed by name, so "clean" never quietly means
less than it says.

USAGE
    audit-guide-conformance.py [--inventory]

    --inventory   also print the per-file, per-detection matrix (the
                  authoritative replacement for the study's hand count)

    exit 0  clean
    exit 1  findings (locations printed)
    exit 2  bad invocation / the guide layer could not be located

EXPECT THIS TO GO RED THE DAY IT IS WRITTEN. Switching detection on surfaces the
latent instances; the repair tasks clear them. Red here is the instrument
working, not a regression — and it is never to be quieted by weakening a
detection.
"""

import argparse
import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# Locating the repo and the guide layer
# --------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[3]

CATALOG = REPO_ROOT / "engineering/standards/documentation-standards/documentation-voices-catalog.md"
ROSTER = REPO_ROOT / "engineering/document-production/PUBLICATION-ROSTER.md"
APP_NOTE_GLOB = "engineering/document-production/app-notes/APP-NOTE-*.md"
MANUAL_GUIDE_GLOB = "engineering/document-production/manuals/*/*guide*.md"

# Excluded by identity, not by lifecycle: a private, non-KB manuscript that
# shares the tree but is governed by nothing in this layer.
PRIVATE_ELEMENTS = {"Donna-Manuscript"}


def load_retired_elements():
    """Read the roster's '## Abandoned' section.

    Returns (slugs, names). `slugs` are folder names to exclude from the scan;
    `names` are the titles/aliases D5 looks for in the guides that remain.
    """
    slugs, names = set(), set()
    if not ROSTER.exists():
        return slugs, names

    in_section = False
    for line in ROSTER.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            in_section = line.startswith("## Abandoned")
            continue
        if not in_section or not line.startswith("|"):
            continue
        cell = line.split("|")[1].strip() if line.count("|") >= 2 else ""
        if not cell or set(cell) <= {"-", ":", " "} or cell == "Document":
            continue
        # e.g.  Smart Pins Tutorial ("Green Book") · `p2-smart-pins-tutorial`
        slugs.update(re.findall(r"`([^`]+)`", cell))
        names.update(re.findall(r"[\"“]([^\"”]+)[\"”]", cell))
        title = re.split(r"[·`(]", cell)[0].strip().rstrip("*").strip()
        if title:
            names.add(title)
    return slugs, names


# The DeSilva creation guide refers to the retired tutorial as the "Smart Pins
# Manual". No live document carries that name (the live one is the I/O & Smart
# Pins User Guide), so the phrase can only mean the retired document.
EXTRA_RETIRED_ALIASES = {"Smart Pins Manual"}


def collect_files(excluded_slugs):
    """Glob the guide layer. Returns (scanned, excluded) as sorted path lists."""
    candidates = []
    if CATALOG.exists():
        candidates.append(CATALOG)
    candidates.extend(REPO_ROOT.glob(APP_NOTE_GLOB))
    candidates.extend(REPO_ROOT.glob(MANUAL_GUIDE_GLOB))

    scanned, excluded = [], []
    for path in sorted(set(candidates)):
        parts = set(path.relative_to(REPO_ROOT).parts)
        if parts & excluded_slugs or parts & PRIVATE_ELEMENTS:
            excluded.append(path)
        else:
            scanned.append(path)
    return scanned, excluded


# --------------------------------------------------------------------------
# Detector results
#
# Every result carries the column the match started at, so the report can
# excerpt AROUND the match. A report that truncates at a fixed width hides the
# very phrase it is complaining about, which reads as a false positive and
# trains the reader to distrust the gate.
# --------------------------------------------------------------------------

def finding(why, pos=0):
    return ("FIND", why, pos)


def exempt(why, pos=0):
    return ("EXEMPT", why, pos)


# --------------------------------------------------------------------------
# D1 — restated voice rule
# --------------------------------------------------------------------------

BLACKLIST_WORDS = ("may", "might", "probably", "typically", "usually",
                   "possibly", "perhaps")
QUOTED_BLACKLIST = re.compile(
    r"['\"`‘’“”]\s*(" + "|".join(BLACKLIST_WORDS) + r")\s*[,;]?\s*['\"`‘’“”]",
    re.I)
HEDGE_RULE = re.compile(r"\b(never|avoid|don't|do not|no|banned?)\b[^.\n]{0,60}?hedg", re.I)
HEDGE_CELL = re.compile(r"hedg\w*\s*[:|]\s*(never|none|no)\b", re.I)
RESTATED_CADENCE = re.compile(
    r"(half of (?:the )?section closings|(?:more than\s*)?~?\s*4 in a row|cadence budget of)", re.I)


SCOPED_HEDGE = re.compile(r"hedg\w*\s+(?:on|in)\s+(?:facts?|factual|stable)", re.I)


def reconciled(line):
    """A hedging statement is conformant when it names the DEFECT rather than a
    word class. Three accepted shapes, all drawn from guides that already do it
    right:

      - scoped to the target: "no hedging ON FACTS" / "in factual statements"
        (the Architect + Getting Started checklists — the declared template)
      - scoped to *vague* hedging, carrying a pointer (the Assembly §4.2 row)
      - pointing at calibrated confidence by name

    Note this can never rescue a word blacklist: a list of may/might/probably
    names words, not the defect, so detect_d1 checks it before coming here.
    """
    low = line.lower()
    if "calibrated" in low or SCOPED_HEDGE.search(line):
        return True
    return "vague" in low and ("§" in line or "see " in low)


def detect_d1(path, lineno, line, is_catalog):
    if is_catalog:
        return None
    hits = list(QUOTED_BLACKLIST.finditer(line))
    if len({m.group(1).lower() for m in hits}) >= 2:
        return finding("word blacklist (never exempt — those words are R1 compliance)",
                       hits[0].start())
    m = HEDGE_CELL.search(line)
    if m and not reconciled(line):
        return finding("voice-comparison cell states a blanket hedging verdict", m.start())
    m = HEDGE_RULE.search(line)
    if m and not reconciled(line):
        return finding("unreconciled hedging rule (scope it to *vague* + cross-reference R1)",
                       m.start())
    m = RESTATED_CADENCE.search(line)
    if m:
        return finding("R4 cadence budget restated (state the local decision, not the rule)",
                       m.start())
    return None


# --------------------------------------------------------------------------
# D2 — tool name
# --------------------------------------------------------------------------

BAD_TOOL = re.compile(r"\bpnut_(?:term_)?ts\b", re.I)
DECLARED_WRONG = re.compile(
    r"(not\s+[`'\"]?pnut_|underscore|command not found|(?:do(?:es)?n?'?t?|not)\s+exist"
    r"|no such|\bwrong\b|incorrect|❌|never write)", re.I)

# `pnut_ts-usage-guide.md` is a REAL file on disk. Flagging a filename would
# invite a "fix" that breaks the citation — the D3 defect, manufactured.
REAL_FILENAMES = re.compile(r"pnut_ts-usage-guide")


def detect_d2(path, lineno, line, is_catalog, context=()):
    m = BAD_TOOL.search(line)
    if not m:
        return None
    if REAL_FILENAMES.search(line) and not BAD_TOOL.search(REAL_FILENAMES.sub("", line)):
        return exempt("real on-disk filename, not a tool invocation", m.start())
    # The declaration and the forms it declares wrong routinely span a wrapped
    # sentence, so judge the neighbourhood, not the line.
    if any(DECLARED_WRONG.search(c) for c in context):
        return exempt("deliberate mention — declares the underscore form wrong", m.start())
    return finding("the underscore form does not exist (use pnut-ts / pnut-term-ts)", m.start())


# --------------------------------------------------------------------------
# D3 — dead cited path
# --------------------------------------------------------------------------

BACKTICKED = re.compile(r"`([^`\n]+)`")
PLACEHOLDER = re.compile(r"[<>{}|\"']|\.\.\.|\s")

# Segments an author is expected to substitute. A template's skeleton path is
# not a broken citation — it is a blank waiting to be filled.
PLACEHOLDER_SEGMENTS = {"folder-name", "manual-name", "document-name",
                        "element-name", "name", "your-manual", "NNN"}

# A path belonging to some OTHER repository is not a claim about this one. The
# guides mark these explicitly when they cite an upstream project's tree.
FOREIGN_REPO = re.compile(r"(←\s*repo|\brepo\s*[`'\"]|github\.com|upstream repo)", re.I)


def looks_like_repo_path(token):
    """A repo path claim: has a separator and a first segment that is a real
    top-level directory. Deriving 'repo-ish' from the tree itself keeps this
    from needing a hand-maintained prefix list."""
    if "/" not in token or "://" in token or PLACEHOLDER.search(token):
        return False
    segments = token.lstrip("/").split("/")
    first = segments[0]
    if not first or first.startswith("."):
        return False
    if PLACEHOLDER_SEGMENTS & set(segments):
        return False
    return (REPO_ROOT / first).is_dir()


def path_resolves(token):
    cleaned = token.lstrip("/").rstrip(".,;:)")
    if "*" in cleaned or "?" in cleaned:
        return any(REPO_ROOT.glob(cleaned))
    return (REPO_ROOT / cleaned).exists()


def detect_d3(path, lineno, line, is_catalog):
    if FOREIGN_REPO.search(line):
        return None
    for m in BACKTICKED.finditer(line):
        token = m.group(1).strip()
        if looks_like_repo_path(token) and not path_resolves(token):
            return finding(f"cited path does not resolve: {token}", m.start())
    return None


# --------------------------------------------------------------------------
# D4 — codename
# --------------------------------------------------------------------------

CODENAMES = re.compile(r"\b(Green Book|Blue Book|Silicon Doc(?:ument)?)\b", re.I)
CODENAME_DECLARED_WRONG = re.compile(
    r"(never (?:say|write|use)|not the|official title|codename|nickname|❌|instead of)", re.I)


def detect_d4(path, lineno, line, is_catalog, context=()):
    m = CODENAMES.search(line)
    if not m:
        return None
    if any(CODENAME_DECLARED_WRONG.search(c) for c in context):
        return exempt(f"deliberate mention — {m.group(1)} named in order to forbid it", m.start())
    return finding(f"codename \"{m.group(1)}\" — use the official title a newcomer can search",
                   m.start())


# --------------------------------------------------------------------------
# D5 — retired-doc reference
# --------------------------------------------------------------------------

LINEAGE = re.compile(
    r"(adopted from|derived from|inherited|originally|formerly|superseded|retired"
    r"|abandoned|histor|legacy|predecessor|no longer|used to |was the )", re.I)


def make_detect_d5(retired_names, retired_slugs):
    needles = sorted(
        (n for n in set(retired_names) | set(retired_slugs) | EXTRA_RETIRED_ALIASES if n),
        key=len, reverse=True)
    if not needles:
        return None
    pattern = re.compile("|".join(re.escape(n) for n in needles), re.I)

    def detect_d5(path, lineno, line, is_catalog, context=()):
        m = pattern.search(line)
        if not m:
            return None
        if any(LINEAGE.search(c) for c in context):
            return exempt(f"lineage/history reference to {m.group(0)} — true, keep", m.start())
        return finding(f"retired document \"{m.group(0)}\" presented as live/current", m.start())

    return detect_d5


# --------------------------------------------------------------------------
# Scan + report
# --------------------------------------------------------------------------

DETECTION_TITLES = {
    "D1": "RESTATED VOICE RULE — the rule belongs in the catalog, the decision belongs here",
    "D2": "TOOL NAME — pnut_ts / pnut_term_ts do not exist",
    "D3": "DEAD CITED PATH — an authority that does not resolve on disk",
    "D4": "CODENAME — against the official-titles rule",
    "D5": "RETIRED-DOC REFERENCE — a roster-Abandoned document shown as live",
}


EXCERPT_WIDTH = 118

# Detectors whose exemption test is about AUTHORIAL INTENT rather than the text
# of one line; these are handed the surrounding lines as well.
INTENT_DETECTORS = {"D2", "D4", "D5"}


def scan(files, detectors):
    """Returns (findings, exemptions); each entry is (code, path, lineno, why, excerpt)."""
    findings, exemptions = [], []
    for path in files:
        is_catalog = path == CATALOG
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for lineno, line in enumerate(lines, 1):
            # A rule and the wording that scopes it often wrap across lines, so
            # the detectors that judge INTENT (is this named in order to declare
            # it wrong? is this lineage rather than a live pointer?) read the
            # neighbourhood. The alternative — reflowing prose so each statement
            # fits one line — would be shaping the documents to suit the tool.
            context = lines[max(0, lineno - 3):lineno + 2]
            for code, detect in detectors:
                result = (detect(path, lineno, line, is_catalog, context)
                          if code in INTENT_DETECTORS else detect(path, lineno, line, is_catalog))
                if result is None:
                    continue
                kind, why, pos = result
                entry = (code, path, lineno, why, excerpt(line, pos))
                (exemptions if kind == "EXEMPT" else findings).append(entry)
    return findings, exemptions


def excerpt(line, pos):
    """A window centred on the match, so the report always shows what it found."""
    line = line.rstrip()
    if len(line) <= EXCERPT_WIDTH:
        return line.strip()
    start = max(0, pos - EXCERPT_WIDTH // 3)
    end = min(len(line), start + EXCERPT_WIDTH)
    start = max(0, end - EXCERPT_WIDTH)
    return ("…" if start else "") + line[start:end].strip() + ("…" if end < len(line) else "")


def rel(path):
    return path.relative_to(REPO_ROOT)


def print_inventory(files, findings, codes):
    print("\nPER-FILE INVENTORY (authoritative — replaces every hand count)")
    header = f"  {'file':<62} " + " ".join(f"{c:>4}" for c in codes) + "   tot"
    print(header)
    print("  " + "-" * (len(header) - 2))
    grand = dict.fromkeys(codes, 0)
    for path in files:
        counts = {c: sum(1 for f in findings if f[0] == c and f[1] == path) for c in codes}
        total = sum(counts.values())
        for c in codes:
            grand[c] += counts[c]
        name = str(rel(path))
        if len(name) > 62:
            name = "..." + name[-59:]
        cells = " ".join(f"{counts[c] or '.':>4}" for c in codes)
        print(f"  {name:<62} {cells} {total:>5}")
    print("  " + "-" * (len(header) - 2))
    cells = " ".join(f"{grand[c]:>4}" for c in codes)
    print(f"  {'TOTAL':<62} {cells} {sum(grand.values()):>5}")


def main(argv):
    parser = argparse.ArgumentParser(add_help=True, description=__doc__.strip().splitlines()[0])
    parser.add_argument("--inventory", action="store_true",
                        help="print the per-file, per-detection matrix")
    args = parser.parse_args(argv[1:])

    if not CATALOG.exists():
        print(f"ERROR: guide layer not found — no catalog at {rel(CATALOG)}", file=sys.stderr)
        return 2

    retired_slugs, retired_names = load_retired_elements()
    if not retired_slugs:
        print("WARNING: no '## Abandoned' rows parsed from the publication roster — "
              "D5 has nothing to look for and the retired element is NOT excluded. "
              "Check the roster's section heading and table shape.", file=sys.stderr)

    scanned, excluded = collect_files(retired_slugs)
    if not scanned:
        print("ERROR: the glob matched no guide files — the guide layer moved?", file=sys.stderr)
        return 2

    detectors = [("D1", detect_d1), ("D2", detect_d2), ("D3", detect_d3), ("D4", detect_d4)]
    d5 = make_detect_d5(retired_names, retired_slugs)
    if d5:
        detectors.append(("D5", d5))
    codes = [c for c, _ in detectors]

    findings, exemptions = scan(scanned, detectors)

    print("=" * 78)
    print("GUIDE-LAYER CONFORMANCE AUDIT")
    print("=" * 78)
    print(f"scanned   {len(scanned)} guide file(s), discovered by glob")
    if excluded:
        print(f"EXCLUDED  {len(excluded)} file(s) — named, so 'clean' never means less than it says:")
        for path in excluded:
            reason = ("private non-KB manuscript"
                      if set(rel(path).parts) & PRIVATE_ELEMENTS
                      else "roster-Abandoned element — never swept")
            print(f"            {rel(path)}   ({reason})")
    if retired_names:
        print(f"retired set (from the roster): {', '.join(sorted(retired_names))}")
    if "D5" not in codes:
        print("D5 DISABLED — no retired documents parsed from the roster")

    if args.inventory:
        print_inventory(scanned, findings, codes)

    if exemptions:
        print(f"\nEXEMPT — {len(exemptions)} deliberate mention(s), NOT defects:")
        for code, path, lineno, why, text in exemptions:
            print(f"  [{code}] {rel(path)}:{lineno}  {why}")
            print(f"        {text}")

    if not findings:
        print(f"\nPASS  guide layer conformant across {len(scanned)} file(s)")
        return 0

    print(f"\nFAIL  {len(findings)} finding(s) across {len({f[1] for f in findings})} file(s)")
    for code in codes:
        group = [f for f in findings if f[0] == code]
        if not group:
            continue
        print(f"\n{code} — {DETECTION_TITLES[code]}   [{len(group)}]")
        for _, path, lineno, why, text in group:
            print(f"  {rel(path)}:{lineno}")
            print(f"      {why}")
            print(f"      | {text}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
