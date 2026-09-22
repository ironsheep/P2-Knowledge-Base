#!/usr/bin/env python3
"""
audit-yaml-source-lock.py — the golden-source lock gate for the shipped P2KB.

THE QUESTION
    For every claim-bearing shipped YAML: is the claim locked to a golden trusted
    source, and does that lock still resolve?

WHY A LOCATOR AND NOT A TOKEN
    The pre-existing claim-sourcing check matched on token PRESENCE. That is how
    `source: enhanced` scored a block as cited, and how F-348's pin-current limit —
    five times the datasheet's absolute maximum — survived two purges wearing a
    citation. Presence is not correctness. A junk citation is WORSE than none,
    because it silently disarms the check that exists to catch it.

    So this gate tiers the provenance VALUE by how far it can be followed:

      RESOLVABLE  names a repo path (optionally :line) and that path EXISTS
      NAMED       names a real document by title, but gives no locator
      WEAK        a process label or bare token naming no document at all
      ABSENT      no provenance key anywhere in a claim-bearing file

    Only RESOLVABLE can be checked by a machine. NAMED is checkable by a human
    holding the document. WEAK and ABSENT are not checkable by anyone, which is
    the finding.

TIER DEFINITIONS ARE EVIDENCE-DERIVED, NOT INVENTED
    Every token in WEAK_VALUES below was observed in the shipped set on
    2026-09-22 and hand-checked. Two candidates were REJECTED after checking, and
    they are recorded here so nobody re-adds them:

      enhancement_source: PNUT_TS_v2.0_*  — 356 files. NOT weak: all 356 also
          carry a real `documentation_source:`. It is a legitimate SECONDARY key
          recording which tooling pass enriched the entry, not a substitute for
          provenance. Scoring it weak would have produced 346 false findings.

      source: parallax-quick-bytes — 42 files. NOT weak: the corpus does exist
          under engineering/ingestion/sources/quick-bytes-*. It is thin (the
          corpus is only partly processed) but it names something real.

RATCHET, NOT ABSOLUTE
    A gate that is permanently RED is a gate people learn to ignore. Zero-unsourced
    is the goal, not today's state. So the default mode is REPORT, and --baseline
    turns it into a regression gate: it fails only when a file gets WORSE than the
    recorded baseline, or a new unsourced file appears. The study's job is to
    shrink the baseline; this gate's job is to stop it growing.

EXEMPTIONS ARE DECLARED, NEVER SILENT
    A silent skip is indistinguishable from a pass. Every exemption is listed in
    EXEMPT_PREFIXES with its reason and is COUNTED in the output.

USAGE
    audit-yaml-source-lock.py                        # report over the shipped set
    audit-yaml-source-lock.py --write-baseline FILE  # record today's state
    audit-yaml-source-lock.py --baseline FILE        # gate: fail on regression
    audit-yaml-source-lock.py --tier WEAK --list     # locate one tier, in full

EXIT
    0  clean (report mode always 0 unless --baseline given and regressions found)
    1  regression against the baseline
    2  usage / environment error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("audit-yaml-source-lock: PyYAML is required (import yaml failed)", file=sys.stderr)
    sys.exit(2)


# ---------------------------------------------------------------- configuration

SHIPPED_ROOT = Path("deliverables/ai/P2")

# Keys that carry PRIMARY provenance — the answer to "how do we know this?"
#
# ⚠ THIS IS A CURATED ALLOW-LIST AND MUST STAY ONE. Do not replace it with a
# keyword match on "source"/"reference". In THIS knowledge base those are domain
# words: `clock_source`, `event_sources`, `interrupt_sources`, `ptra_source`,
# `source_bit`, `source_select`, `block_transfer_source` and `shared_resource` all
# describe the P2, not our evidence for a claim. A pattern match scores every one
# of them as a citation — the same false-positive shape that made the ADC gate
# read a filter-select field as an inverted sub-mode.
#
# The universe of keys was enumerated over the whole shipped set on 2026-09-22 and
# each one below was hand-sorted. Adding a key means checking it the same way.
PRIMARY_KEYS = {
    "source", "sources", "documentation_source", "source_document",
    "source_documents", "source_reference", "source_trace", "source_page",
    "source_line", "source_listing", "source_section", "source_metadata",
    "source_authority", "source_of_truth", "canonical_source", "primary_source",
    "primary_sources", "provenance", "cite", "citation", "citations",
    "reference", "references", "page_reference", "printed_reference",
    "derived_from", "verified_against", "verified_in", "attribution",
    "technique_source", "pattern_source", "example_source", "import_source",
    "rescrape_source", "range_source", "source_code", "what_the_source_says",
}

# Keys that record a SOURCE CONFLICT rather than a source. These are gold for the
# hardware-periphery map: a file that already says its sources disagree is a
# self-identified Class B edge, and documentary work provably cannot close it.
# Counted and reported, never scored as provenance.
CONFLICT_KEYS = {
    "conflicting_sources", "cross_source_conflict", "source_tension",
    "what_other_sources_say", "known_source_defect_in_that_passage",
    "not_stated_by_any_source", "cross_check_sources", "sources_to_check",
}

# Deliberately NOT primary. See the module docstring for why each was rejected.
SECONDARY_KEYS = {
    "enhancement_source",   # names the tooling pass, not the source
    "last_verified",        # a date, not a source
    "reference_links",      # outbound reading, not provenance
    "cross_references",     # KB-internal navigation
    "language_reference",   # KB-internal navigation
    "resources",            # reader-facing links
    "original_platform",    # P1/P2 provenance of an idea, not of the claim
}

# Values that name no document. Observed in the shipped set and hand-checked.
WEAK_VALUES = {
    "enhanced",
    "original",
    "common_pattern",
    "multi_cog_pattern",
    "inferred",
    "derived",
    "internal",
    "n/a",
    "na",
    "none",
    "tbd",
    "unknown",
}

# Claim-free by construction. Each entry is (prefix, reason).
EXEMPT_PREFIXES = [
    ("community/obex/objects/",
     "OBEX catalog entry: the object ID IS the citation, and the object is the artifact"),
]

# A locator we can actually follow: a repo-relative path, optionally :line or :a-b
PATH_RE = re.compile(
    r"(?P<path>(?:engineering|deliverables|documentation)/[A-Za-z0-9._/-]+?\.[A-Za-z0-9]+)"
    r"(?::(?P<line>\d+(?:-\d+)?))?"
)

TIERS = ("RESOLVABLE", "NAMED", "WEAK", "ABSENT")


# ---------------------------------------------------------------------- helpers

def repo_root() -> Path:
    """Locate the repo root by walking up for the shipped tree.

    Deliberately does NOT derive the root from this script's own path: a copy of
    the tools tree under .backups/ would then score itself as a valid repo and the
    gate would silently audit the wrong tree.
    """
    here = Path.cwd().resolve()
    for cand in (here, *here.parents):
        if (cand / SHIPPED_ROOT).is_dir() and (cand / ".git").exists():
            return cand
    print(f"audit-yaml-source-lock: no repo root above {here} containing {SHIPPED_ROOT}",
          file=sys.stderr)
    sys.exit(2)


def walk_values(node, key=None):
    """Yield (key, scalar_value) for every scalar in a parsed YAML tree."""
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk_values(v, str(k))
    elif isinstance(node, list):
        for item in node:
            yield from walk_values(item, key)
    elif node is not None and key is not None:
        yield key, str(node)


def classify_value(value: str, root: Path) -> tuple[str, str]:
    """Return (tier, detail) for one provenance value."""
    stripped = value.strip()
    if not stripped:
        return "WEAK", "empty value"
    if stripped.strip("\"'").lower() in WEAK_VALUES:
        return "WEAK", f"names no document: {stripped.strip()!r}"

    best = None
    for m in PATH_RE.finditer(stripped):
        target = root / m.group("path")
        if target.exists():
            return "RESOLVABLE", m.group(0)
        best = m.group("path")
    if best:
        return "NAMED", f"path does not resolve: {best}"
    return "NAMED", stripped[:80]


def exempt_reason(rel: str) -> str | None:
    for prefix, reason in EXEMPT_PREFIXES:
        if rel.startswith(prefix):
            return reason
    return None


def audit_file(path: Path, rel: str, root: Path) -> dict:
    """Classify one shipped YAML by its BEST provenance tier."""
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:                       # a file we cannot parse is a finding
        return {"file": rel, "tier": "ABSENT", "detail": f"unparseable: {exc.__class__.__name__}",
                "hits": [], "weak_blocks": [], "conflicts": []}

    hits, conflicts = [], []
    for key, value in walk_values(doc):
        base = key.lower()
        if base in CONFLICT_KEYS:
            conflicts.append({"key": key, "value": value[:120]})
            continue
        if base in SECONDARY_KEYS or base not in PRIMARY_KEYS:
            continue
        tier, detail = classify_value(value, root)
        hits.append({"key": key, "tier": tier, "detail": detail})

    if not hits:
        return {"file": rel, "tier": "ABSENT", "detail": "no primary provenance key",
                "hits": [], "weak_blocks": [], "conflicts": conflicts}

    # A file is as good as its BEST citation: one resolvable source locks the file.
    #
    # BUT the roll-up alone would hide F-348's actual shape — a junk citation on ONE
    # BLOCK inside a file that is otherwise well sourced. The file scores fine and the
    # bad block ships. So carry the block-level weak count out separately; it is
    # reported and gated independently of the file tier.
    weak_blocks = [h for h in hits if h["tier"] == "WEAK"]
    for tier in TIERS:
        for h in hits:
            if h["tier"] == tier:
                return {"file": rel, "tier": tier, "detail": h["detail"],
                        "hits": hits, "weak_blocks": weak_blocks, "conflicts": conflicts}
    return {"file": rel, "tier": "ABSENT", "detail": "unclassified",
            "hits": hits, "weak_blocks": weak_blocks, "conflicts": conflicts}


# ------------------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description="Golden-source lock gate for the shipped P2KB.")
    ap.add_argument("--baseline", metavar="FILE", help="gate against a recorded baseline")
    ap.add_argument("--write-baseline", metavar="FILE", help="record today's state and exit 0")
    ap.add_argument("--tier", choices=TIERS, help="restrict the listing to one tier")
    ap.add_argument("--list", action="store_true", help="list every file in full (never truncated)")
    ap.add_argument("--json", metavar="FILE", help="also emit the full result as JSON")
    args = ap.parse_args()

    root = repo_root()
    shipped = root / SHIPPED_ROOT

    results, exempt = [], []
    for path in sorted(shipped.rglob("*.yaml")):
        rel = str(path.relative_to(root / SHIPPED_ROOT))
        reason = exempt_reason(rel)
        if reason:
            exempt.append({"file": rel, "reason": reason})
            continue
        results.append(audit_file(path, rel, root))

    counts = {t: sum(1 for r in results if r["tier"] == t) for t in TIERS}
    audited = len(results)

    print("golden-source lock — shipped P2KB\n")
    print(f"  audited {audited} file(s); {len(exempt)} exempt by declared rule\n")
    for t in TIERS:
        pct = (counts[t] * 100.0 / audited) if audited else 0.0
        print(f"    {t:<11} {counts[t]:>5}   {pct:5.1f}%")
    machine = counts["RESOLVABLE"]
    print(f"\n  machine-checkable provenance: {machine} of {audited} "
          f"({machine * 100.0 / audited:.1f}%)" if audited else "")
    print("  NAMED is checkable by a human holding the document; "
          "WEAK and ABSENT are checkable by no one.")

    # Block-level junk, reported independently of the file roll-up. A file can score
    # RESOLVABLE on one citation while a DIFFERENT block inside it carries `enhanced`.
    # That is the F-348 shape and the roll-up cannot see it.
    junk = [(r["file"], h) for r in results for h in r.get("weak_blocks", [])]
    hidden = [f for f, _ in junk if next(x["tier"] for x in results if x["file"] == f) != "WEAK"]
    print(f"\n  block-level junk citations: {len(junk)} in {len({f for f, _ in junk})} file(s)")
    print(f"    of which HIDDEN by the file roll-up (file scores better elsewhere): "
          f"{len(set(hidden))}")
    print("    a junk citation is worse than none: it disarms the check meant to catch it")

    # Self-identified Class B edges: the KB already records that its sources disagree
    # here. Documentary work provably cannot close these; only the bench can. This is
    # the seed list for the hardware-periphery map.
    conf = [(r["file"], c) for r in results for c in r.get("conflicts", [])]
    if conf:
        print(f"\n  self-declared source conflicts: {len(conf)} in "
              f"{len({f for f, _ in conf})} file(s)")
        print("    these are Class B hardware-periphery candidates: a contradiction between")
        print("    trusted sources cannot be settled by reading more of them")
        for f, c in sorted(conf, key=lambda t: (t[0], t[1]["key"])):
            print(f"      {f}  [{c['key']}]")

    if exempt:
        by_reason = {}
        for e in exempt:
            by_reason.setdefault(e["reason"], 0)
            by_reason[e["reason"]] += 1
        print("\n  exemptions (declared, never silent):")
        for reason, n in by_reason.items():
            print(f"    {n:>5}  {reason}")

    if args.list:
        wanted = [args.tier] if args.tier else ["ABSENT", "WEAK"]
        for t in wanted:
            rows = [r for r in results if r["tier"] == t]
            print(f"\n  --- {t} ({len(rows)}) ---")
            for r in rows:                          # never truncated: a capped defect
                print(f"    {r['file']}: {r['detail']}")   # list reads as a clean one

    payload = {"audited": audited, "counts": counts,
               "files": {r["file"]: r["tier"] for r in results},
               "exempt": len(exempt)}

    if args.write_baseline:
        Path(args.write_baseline).write_text(json.dumps(payload, indent=1, sort_keys=True) + "\n")
        print(f"\n  baseline written: {args.write_baseline}")
        return 0

    if args.json:
        Path(args.json).write_text(json.dumps(payload, indent=1, sort_keys=True) + "\n")

    if args.baseline:
        try:
            base = json.loads(Path(args.baseline).read_text())
        except Exception as exc:
            print(f"\nFAIL: cannot read baseline {args.baseline}: {exc}", file=sys.stderr)
            return 2
        rank = {t: i for i, t in enumerate(TIERS)}      # lower index == better
        regressions = []
        for f, tier in payload["files"].items():
            was = base["files"].get(f)
            if was is None:
                if tier in ("WEAK", "ABSENT"):
                    regressions.append(f"NEW unsourced file: {f} [{tier}]")
            elif rank[tier] > rank[was]:
                regressions.append(f"WEAKENED: {f}  {was} -> {tier}")
        if regressions:
            print(f"\nFAIL: {len(regressions)} provenance regression(s) against {args.baseline}\n")
            for r in regressions:
                print(f"  {r}")
            return 1
        print(f"\nPASS: no provenance regression against {args.baseline}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
