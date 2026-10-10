#!/usr/bin/env python3
"""Fail on a NEW provenance-shaped key name in the shipped YAML (F-545).

WHY THIS EXISTS. The delivery filter removes a fixed list of key names before an
agent reads a page. Provenance that is written under any OTHER name ships to every
consumer, and no gate noticed: F-545 measured `extraction_status`, `last_verified`,
`last_author_extraction`, `authority_tier`, `provenance`, `rescrape_source`, ... on the
shipped payload, each invented one at a time. The rule (Stephen, 2026-10-04) is that
provenance goes in the existing keys, and the filter's list does not grow to chase it.
This gate makes the rule executable: it walks every key name in deliverables/ai/P2
and fails on any provenance-shaped name that has not been reviewed and listed here.

WHAT "PROVENANCE-SHAPED" MEANS. A key name is split into words on `_`, `-` and `.`. A
word is a hit if it starts with  source / extract / scrape / verif / authorit /
provenance / tracking, or ends in `source(s)` (`datasource`). `resource(s)` is NOT a
hit -- it merely contains the letters (`resources` is a content key on 53 pages). A key
that is prose rather than an identifier (it contains a space or `?`, e.g. the
boot-ROM decision-tree questions) is content and is not examined.

THE ALLOW-LIST is held in this script, one line per name, each with a kind and a reason:
    filtered  the delivery filter removes it. Checked against the rule in
              generate-p2kb-index.py: a name listed here but absent from the rule fails.
    tracking  scraper bookkeeping. Every occurrence must sit under a key the filter
              removes (today: scrape_tracking), or it reaches the agent -- fails.
    content   a real content key; its name only happens to read like provenance.
    open      provenance that DOES reach consumers today and is awaiting a decision.
              Listed so the gate is green, and counted in the summary line so it is never
              silent. Resolving one means moving it into a filtered key or deleting it,
              and then deleting its line here.
Adding a name here is a review decision, never a way to turn the gate green.

Usage:
    audit-yaml-provenance-key-names.py [path ...]    # default: deliverables/ai/P2
    audit-yaml-provenance-key-names.py --self-test   # alias: --negative-control

Exit 0 clean, 1 an unlisted name (or a listed name misused), 2 nothing measured.
"""
import importlib.util
import os
import re
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML not available", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[3]

# name -> (kind, one-line reason). Built from the census of 1,135 shipped files, 2026-10-10.
ALLOW = {
    # ---- removed by the delivery filter (kind 'filtered') -------------------------------
    "source":                 ("filtered", "provenance; the filter's primary field"),
    "sources":                ("filtered", "provenance; the filter's list form"),
    "documentation_source":   ("filtered", "provenance; per-file citation of the ingested document"),
    "verified_against":       ("filtered", "provenance; what a claim was checked against"),
    "manual_extraction_date": ("filtered", "provenance; process date of the extraction"),
    "scrape_tracking":        ("filtered", "OBEX / Quick Bytes scraper bookkeeping (Stephen, 2026-10-10)"),
    # ---- scraper bookkeeping; only valid inside a filtered key (kind 'tracking') --------
    "scraped":                ("tracking", "Quick Bytes scrape date, inside scrape_tracking"),
    "import_source":          ("tracking", "OBEX import origin, inside scrape_tracking"),
    "rescrape_source":        ("tracking", "OBEX re-scrape label, inside scrape_tracking"),
    "last_author_extraction":    ("tracking", "OBEX author-extraction timestamp, inside scrape_tracking"),
    "last_author_re_extraction": ("tracking", "OBEX author re-extraction timestamp, inside scrape_tracking"),
    "last_complete_extraction":  ("tracking", "OBEX complete-extraction timestamp, inside scrape_tracking"),
    # ---- real content whose name reads like provenance (kind 'content') -----------------
    "authority_tier":         ("content", "decomposition pages: how authoritative a statement is; F-545 decided it stays; the sourcing gate reads EXAMPLE"),
    "authority_tier_legend":  ("content", "decomposition glossary: the legend for authority_tier"),
    "canonical_source":       ("content", "inline_pasm2: pointer to the KB page that is canonical for the topic"),
    "event_sources":          ("content", "hardware event sources a cog can wait on"),
    "interrupt_sources":      ("content", "the P2 interrupt sources"),
    "interrupt_sources_detail": ("content", "table of the P2 interrupt sources"),
    "source_types":           ("content", "kinds of interrupt source"),
    "total_sources":          ("content", "count of interrupt sources"),
    "source_id":              ("content", "interrupt source identifier"),
    "clock_source":           ("content", "the clock source of a clock mode"),
    "clock_sources":          ("content", "the clock sources of the P2"),
    "clock_source_modes":     ("content", "CLKMODE clock-source field modes"),
    "source_select":          ("content", "clock-source select field"),
    "source_selection":       ("content", "WRPIN source-selection field behaviour"),
    "source_bit":             ("content", "smart-pin source-bit behaviour"),
    "source_switch_flush":    ("content", "ADC: samples to discard after a source switch"),
    "pattern_source":         ("content", "SKIPF: where the skip pattern comes from"),
    "ptra_source":            ("content", "COGINIT: where PTRA gets its value"),
    "ptrb_source":            ("content", "COGINIT: where PTRB gets its value"),
    "source_statement":       ("content", "p2an003: the application note's own sentence, quoted as data"),
    "source_code":            ("content", "Quick Bytes: the downloadable source code of the object"),
    "source_chip":            ("content", "P1 ROM font page: the P1 chip the font was read from"),
    "source_package":         ("content", "AV breakout: the named zip of the driver source"),
    "open_source":            ("content", "a marker that a fact is not stated by any Parallax source (a content note, not a citation)"),
    "version_tracking":       ("content", "OBEX version, upload date and repository flag of the object (also holds last_scraped, see open)"),
    "source_document":        ("content", "code-example schema (optional field; F-545 2026-10-10 kept it)"),
    "source_metadata":        ("content", "code-example schema block that holds source_document / source_page / source_section"),
    "source_page":            ("content", "code-example schema field"),
    "source_section":         ("content", "code-example schema field"),
    "authoritative_content_list": ("content", "boot-ROM page: the one statement of what the ROM contains"),
    "verification":           ("content", "how a reader checks something: SETQ count checklist, compile-with--m method"),
    "frequency_verification": ("content", "clkfreq: example code that checks the clock is in range"),
    "pin_verification":       ("content", "click-module page: example debug code that prints the pin assignments"),
    "read_back_verification": ("content", "DIRA/DIRB debugging tip: read the register back"),
    # ---- self-declared source conflicts, read by audit-yaml-source-lock (kind 'content') --
    "conflicting_sources":    ("content", "declared conflict between sources (source-lock Class B marker)"),
    "cross_source_conflict":  ("content", "declared conflict between sources (source-lock Class B marker)"),
    "known_source_defect_in_that_passage": ("content", "declared source defect (source-lock Class B marker)"),
    "not_stated_by_any_source": ("content", "declared silence of the sources (source-lock Class B marker)"),
    "source_tension":         ("content", "declared conflict between sources (source-lock Class B marker)"),
    "what_other_sources_say": ("content", "declared conflict between sources (source-lock Class B marker)"),
    "what_the_source_says":   ("content", "pitfall: what a source says, set against the verified behaviour"),
    "consequence_source":     ("content", "smart_pins: the statement the consequence rests on (declared-conflict note)"),
    "verification_status":    ("content", "streamer/pin-capture.yaml: what was measured on silicon (the facts themselves), each sub-block with its own EF source: line"),
    # ---- provenance that reaches consumers today (kind 'open') --------------------------
    "base_pin_options_provenance": ("open", "hardware/addon-click-adapter: provenance note under an unlisted key (hardware pages are owned by another pass)"),
    "combinations_are_compiler_verified": ("open", "pasm2-getting-started: a compile-verification claim under an unlisted key; the CP register is the home for it"),
    "last_scraped":           ("open", "OBEX: scraper timestamp, 130 files in version_tracking (outside scrape_tracking) -- reaches the agent; needs a decision"),
}

STEMS = ("extract", "scrape", "verif", "authorit", "provenance", "tracking")
IDENT_RE = re.compile(r"^[A-Za-z0-9_\-.%]+$")
NOT_HITS = {"resource", "resources"}


def hit_words(key):
    """The words of `key` that make it provenance-shaped; [] if it is not examined or clean."""
    if not IDENT_RE.match(key):
        return []                       # a prose key (spaces, '?') is content
    words = [w for w in re.split(r"[_\-.]", key.lower()) if w]
    out = []
    for w in words:
        if w in NOT_HITS:
            continue
        if w.startswith("source") or w.endswith("source") or w.endswith("sources") \
                or any(w.startswith(s) for s in STEMS):
            out.append(w)
    return out


def load_filter_fields():
    """The delivery filter's remove_fields, from the one place the rule is defined."""
    spec = importlib.util.spec_from_file_location("gen_index", ROOT / "engineering/tools/generate-p2kb-index.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return set(mod.DELIVERY_FILTER["remove_fields"])


def walk(node, ancestors, out):
    """Collect (key, ancestors, line) for every mapping key under node."""
    if isinstance(node, yaml.MappingNode):
        for k, v in node.value:
            key = str(getattr(k, "value", k))
            out.append((key, tuple(ancestors), k.start_mark.line + 1))
            walk(v, ancestors + [key], out)
    elif isinstance(node, yaml.SequenceNode):
        for v in node.value:
            walk(v, ancestors, out)


def analyse(files, filtered):
    """Return (unlisted, misplaced, parse_fail, seen) for the given files."""
    unlisted, misplaced, parse_fail = {}, [], []
    seen = {}                                    # name -> occurrence count
    for f in files:
        keys = []
        try:
            with open(f, encoding="utf-8") as fh:
                walk(yaml.compose(fh), [], keys)
        except Exception as exc:                 # a file we cannot parse is a finding
            parse_fail.append((f, str(exc).splitlines()[0]))
            continue
        for key, anc, line in keys:
            if not hit_words(key):
                continue
            seen[key] = seen.get(key, 0) + 1
            entry = ALLOW.get(key)
            if entry is None:
                unlisted.setdefault(key, []).append((f, line))
            elif entry[0] == "tracking" and not (set(anc) & filtered):
                misplaced.append((f, line, key, ".".join(anc)))
    return unlisted, misplaced, parse_fail, seen


def collect(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            for dp, _, fns in os.walk(p):
                files += [os.path.join(dp, fn) for fn in fns if fn.endswith(".yaml")]
        elif p.endswith(".yaml"):
            files.append(p)
    return sorted(set(files))


def audit(paths):
    filtered = load_filter_fields()
    problems = 0
    for name, (kind, reason) in sorted(ALLOW.items()):
        if kind == "filtered" and name not in filtered:
            print(f"  ALLOW-LIST ERROR  '{name}' is listed as filtered but is not in the delivery "
                  f"filter's remove_fields ({sorted(filtered)})")
            problems += 1
    files = collect(paths)
    if not files:
        print("NOTHING MEASURED -- no .yaml files found under the given path(s). This is not a pass.")
        return 2
    unlisted, misplaced, parse_fail, seen = analyse(files, filtered)
    for f, why in parse_fail:
        print(f"  PARSE-FAIL  {f}: {why}")
        problems += 1
    for key, where in sorted(unlisted.items()):
        problems += 1
        f, line = where[0]
        print(f"  UNLISTED  '{key}'  x{len(where)}  first at {f}:{line}\n"
              f"            a provenance-shaped key name that has not been reviewed. Put the provenance in\n"
              f"            source: / sources: (the filter removes them) or, if it is real content, add it\n"
              f"            to ALLOW in this script with a reason.")
    for f, line, key, anc in misplaced[:50]:
        problems += 1
        print(f"  MISPLACED  '{key}' at {f}:{line} (under {anc or '<root>'}) is scraper bookkeeping "
              f"outside any key the delivery filter removes")
    if len(misplaced) > 50:
        print(f"  ... and {len(misplaced) - 50} more misplaced")
    open_n = sum(n for k, n in seen.items() if ALLOW.get(k, ("",))[0] == "open")
    open_names = sorted(k for k in seen if ALLOW.get(k, ("",))[0] == "open")
    unused = sorted(k for k in ALLOW if k not in seen)
    print(f"\n  files scanned: {len(files)}   distinct provenance-shaped names: {len(seen)}   "
          f"unlisted: {len(unlisted)}   misplaced: {len(misplaced)}")
    print(f"  OPEN (reaches consumers, awaiting a decision): {open_n} occurrence(s) of "
          f"{len(open_names)} name(s): {', '.join(open_names) or 'none'}")
    if unused:
        print(f"  allow-list names no longer present (delete their lines): {', '.join(unused)}")
    if problems == 0:
        print("  CLEAN. NOTE: this compares key NAMES only. It does not say a listed key's VALUE is")
        print("  correct, and it cannot see provenance written into a value or a prose sentence.")
    return 1 if problems else 0


def self_test():
    """A gate that cannot fail has not been verified, it has been RUN."""
    filtered = load_filter_fields()
    cases = [
        ("a NEW key `last_verified_by` -- MUST FAIL", "a:\n  last_verified_by: x\n", True),
        ("a NEW key `extraction_status` -- MUST FAIL", "a: 1\nextraction_status: done\n", True),
        ("a NEW key `datasource` -- MUST FAIL", "a: 1\ndatasource: x\n", True),
        ("a NEW key nested in a list item -- MUST FAIL", "a:\n  - provenance_note: x\n", True),
        ("a listed filtered key `source` -- MUST PASS", "a: 1\nsource: x\n", False),
        ("a listed content key `authority_tier` -- MUST PASS", "a:\n  authority_tier: EXAMPLE\n", False),
        ("`resources` is not provenance-shaped -- MUST PASS", "resources:\n  - x\n", False),
        ("a prose key with a space -- MUST PASS", "'Where is the flash loader source?': x\n", False),
        ("tracking key INSIDE scrape_tracking -- MUST PASS",
         "m:\n  scrape_tracking:\n    last_author_extraction: x\n", False),
        ("tracking key OUTSIDE scrape_tracking -- MUST FAIL",
         "m:\n  metadata:\n    last_author_extraction: x\n", True),
    ]
    ok = True
    for label, body, want_fail in cases:
        d = tempfile.mkdtemp()
        p = os.path.join(d, "t.yaml")
        with open(p, "w") as fh:
            fh.write(body)
        unlisted, misplaced, parse_fail, _ = analyse([p], filtered)
        got_fail = bool(unlisted or misplaced or parse_fail)
        good = got_fail == want_fail
        ok = ok and good
        print(f"  [{'PASS' if good else '**FAIL**'}] {label}: got {'FAIL' if got_fail else 'clean'}")
    bad_allow = [n for n, (k, _) in ALLOW.items() if k == "filtered" and n not in filtered]
    if bad_allow:
        ok = False
        print(f"  [**FAIL**] allow-list 'filtered' names missing from the delivery filter: {bad_allow}")
    print()
    print("Self-test PASSED -- the gate fires on a new provenance-shaped key and on bookkeeping outside\n"
          "scrape_tracking, and passes listed names, `resources` and prose keys." if ok else "Self-test FAILED.")
    return 0 if ok else 1


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--self-test" in argv or "--negative-control" in argv:
        sys.exit(self_test())
    sys.exit(audit(argv or [str(ROOT / "deliverables/ai/P2")]))
