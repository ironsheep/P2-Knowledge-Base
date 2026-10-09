#!/usr/bin/env python3
"""Does the term that names a KB directory reach all of its files, or only some?

WHY THIS EXISTS (F-389 / S-387). The index generator abbreviates or drops path components
in the key (`debug-commands/c-z.yaml` -> `p2kbSpin2DbgCZ`), so the term that names a subtree
reaches only SOME files of it: a search for "debug" returns four files and silently omits
the other four. "Partial results" is the failure mode, and no other gate looks at it.

What is decidable. Reachability of a path term through the three things the index offers a
searcher: the KEY, the ALIASES that point at it, and its CATEGORY names. (Whether
`p2kb_find` searches category names is not checked here; if it does not, drop the category
from the haystack and re-measure.) What is NOT decidable by a gate: which directory names
are topic words (`debug-commands`) and which are structural (`methods`, `obex`, `keywords`).
That needs a reviewed list -- the baseline below.

Rule. For each directory D with >= 3 files directly in it and at least two path levels below
deliverables/ai/P2: term = the normalised tokens (split on `-`/`_`, length >= 3) of D's leaf
name. reach(file) = any token occurs (lower-cased, alphanumerics only, substring) in
key + aliases-of-key + category-names-of-key. FAIL when 0 < reached < all, for a directory not
in the reviewed baseline `engineering/tools/validation/baselines/index-findability.json`
(`{directory: reviewed reason}`; a missing file is an empty baseline). A baseline entry with an
empty reason is itself a failure. Directories reached by NONE are listed as advisory -- they
are structural by design today.

Usage:
    audit-index-findability.py [--index PATH] [--baseline PATH]
    audit-index-findability.py --negative-control

Exit 0 clean, 1 partial-reach directories found, 2 the tool could not audit.

A green does NOT certify: that a searcher finds the right file for a real query
(`p2kb_find "debug data too long"` returning 0 is a vocabulary gap, invisible to a path-term
test); that the baseline's reasons are right; or that `p2kb_find` ranks the file. It certifies
only that no directory's own name reaches some of its files and not others without a recorded
reason.
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import PurePosixPath

KB_PREFIX = "deliverables/ai/P2/"
DEFAULT_INDEX = "deliverables/ai/p2kb-index.json"
DEFAULT_BASELINE = "engineering/tools/validation/baselines/index-findability.json"


def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())


def tokens(leaf):
    return [norm(t) for t in re.split(r'[-_]', leaf) if len(t) >= 3 and norm(t)]


def analyse(idx, min_files=3, min_depth=2):
    """Return list of dicts: dir, n, reached, unreached(list of keys), tokens."""
    files = idx.get("files") or {}
    aliases = idx.get("aliases") or {}
    cats = idx.get("categories") or {}
    key_alias = defaultdict(list)
    for a, targets in aliases.items():
        if isinstance(targets, str):
            targets = [targets]
        for k in targets:
            key_alias[k].append(a)
    key_cat = defaultdict(list)
    for c, ks in cats.items():
        for k in ks:
            key_cat[k].append(c)
    by_dir = defaultdict(list)
    for k, e in files.items():
        p = e.get("path", "")
        if p.startswith(KB_PREFIX):
            p = p[len(KB_PREFIX):]
        parts = PurePosixPath(p).parts
        if len(parts) - 1 >= min_depth:
            by_dir["/".join(parts[:-1])].append(k)
    out = []
    for d, keys in sorted(by_dir.items()):
        if len(keys) < min_files:
            continue
        toks = tokens(d.rsplit("/", 1)[-1])
        if not toks:
            continue
        reached, unreached = 0, []
        for k in keys:
            hay = norm(k) + "|" + "|".join(norm(a) for a in key_alias.get(k, [])) + "|" \
                + "|".join(norm(c) for c in key_cat.get(k, []))
            if any(t in hay for t in toks):
                reached += 1
            else:
                unreached.append(k)
        out.append({"dir": d, "n": len(keys), "reached": reached,
                    "unreached": sorted(unreached), "tokens": toks})
    return out


def evaluate(idx, baseline):
    """Return (partial_not_baselined, baselined_partial, none_reached, bad_baseline, total_dirs)."""
    rows = analyse(idx)
    partial, based, none = [], [], []
    for r in rows:
        if r["reached"] == 0:
            none.append(r)
        elif r["reached"] < r["n"]:
            (based if r["dir"] in baseline else partial).append(r)
    bad = [d for d, why in baseline.items() if not (isinstance(why, str) and why.strip())]
    return partial, based, none, bad, len(rows)


def load_baseline(path):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        return {}
    if not isinstance(data, dict):
        raise ValueError("baseline must be a JSON object {directory: reason}")
    return data


def negative_control():
    def mk(dirname, n_files, reached_idx=(), key_fmt="p2kbSpin2Dbg{}", alias_for=None):
        files, aliases = {}, {}
        for i in range(n_files):
            k = key_fmt.format("Item%d" % i)
            files[k] = {"path": f"{KB_PREFIX}{dirname}/f{i}.yaml"}
        for i in reached_idx:
            k = key_fmt.format("Item%d" % i)
            aliases[alias_for or "debug"] = aliases.get(alias_for or "debug", []) + [k]
        return {"files": files, "aliases": aliases, "categories": {}}

    cases = []
    # must FIRE
    cases.append(("4 files under x/debug-commands, keys ...Dbg..., one alias `debug` -> partial",
                  mk("x/debug-commands", 4, reached_idx=(0,)), {}, "fire"))
    # must NOT fire
    cases.append(("all files reachable (aliases on every file)",
                  mk("x/debug-commands", 4, reached_idx=(0, 1, 2, 3)), {}, "clean"))
    cases.append(("zero files reachable -> advisory only",
                  mk("x/debug-commands", 4), {}, "clean"))
    cases.append(("a partial directory present in the baseline with a reason",
                  mk("x/debug-commands", 4, reached_idx=(0,)), {"x/debug-commands": "structural; reviewed"}, "clean"))
    cases.append(("fewer than 3 files",
                  mk("x/debug-commands", 2, reached_idx=(0,)), {}, "clean"))
    # must FIRE: bad baseline
    cases.append(("a baseline entry with an EMPTY reason is a failure",
                  mk("x/debug-commands", 4, reached_idx=(0, 1, 2, 3)), {"x/debug-commands": "  "}, "fire"))
    # reach via category name
    cat = mk("x/debug-commands", 4, reached_idx=())
    cat["categories"] = {"debug_commands": list(cat["files"])}
    cases.append(("reached through the category name for every file", cat, {}, "clean"))
    # reach via key
    keyed = mk("x/debug-commands", 3, key_fmt="p2kbDebug{}")
    cases.append(("reached through the key itself", keyed, {}, "clean"))

    ok = True
    for label, idx, base, want in cases:
        partial, based, none, bad, total = evaluate(idx, base)
        got = "fire" if (partial or bad) else "clean"
        good = got == want
        ok = ok and good
        print(f"  [{'PASS' if good else '**FAIL**'}] {label}: {got} (want {want})")
    print()
    if ok:
        print("Negative control PASSED -- a directory whose term reaches some but not all files fires; full,")
        print("zero, baselined, tiny and category/key-reached directories stay clean; an empty baseline")
        print("reason fires.")
    else:
        print("Negative control FAILED.")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--index", default=DEFAULT_INDEX)
    ap.add_argument("--baseline", default=DEFAULT_BASELINE)
    ap.add_argument("--negative-control", action="store_true")
    a = ap.parse_args()
    if a.negative_control:
        sys.exit(negative_control())
    try:
        with open(a.index, encoding="utf-8") as fh:
            idx = json.load(fh)
        baseline = load_baseline(a.baseline)
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: cannot read input: {e} -- nothing audited, not a pass.")
        sys.exit(2)
    partial, based, none, bad, total = evaluate(idx, baseline)
    if total == 0:
        print("ERROR: no qualifying directory found in the index -- nothing audited, not a pass.")
        sys.exit(2)
    for r in partial:
        print(f"  PARTIAL-REACH {r['dir']}: term {'/'.join(r['tokens'])!r} reaches {r['reached']}/{r['n']}; "
              f"unreachable: {', '.join(r['unreached'][:6])}{' ...' if len(r['unreached']) > 6 else ''}")
    for d in bad:
        print(f"  BASELINE-NO-REASON {d}: a baseline entry needs a reviewed reason")
    for r in based:
        print(f"  (baselined) {r['dir']}: {r['reached']}/{r['n']}")
    print(f"  advisory: {len(none)} directories ({sum(r['n'] for r in none)} files) reached by none -- "
          f"structural unless reviewed otherwise")
    print(f"\n  qualifying directories: {total}   partial (not baselined): {len(partial)} "
          f"({sum(len(r['unreached']) for r in partial)} files unreachable)   baselined: {len(based)}   "
          f"reached by none: {len(none)}   baseline entries without a reason: {len(bad)}")
    if partial or bad:
        print(f"  FAIL: {len(partial)} directory(ies) reached partially by their own name, {len(bad)} bad baseline entries.")
        sys.exit(1)
    print("  PASS. NOTE: this certifies only that no directory's own name reaches some of its files and not")
    print("  others without a recorded reason; it does not certify that a real query finds the right file.")
    sys.exit(0)


if __name__ == "__main__":
    main()
