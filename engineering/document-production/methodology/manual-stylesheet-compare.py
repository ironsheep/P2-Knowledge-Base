#!/usr/bin/env python3
"""Deterministic cross-document comparison of P2KB manual stylesheets/filters.

Measures, for every *used* template/filter file in each of the 6 active manuals:
  - meaningful (non-blank) line count
  - % of its lines shared with at least one OTHER document's same-role file
  - both RAW (literal) and SLUG-NORMALIZED (rename noise removed)
Plus an N-way "fracture map" of the 6 foundation files (where layout logic lives).
"""
import os, re, json
from collections import defaultdict

BASE = "/workspaces/P2-Knowledge-Base/engineering/document-production/workspace"

# doc -> (slug, {role: [relative file paths actually USED]})
DOCS = {
    "p2-assembly-language-manual": ("pasm2", {
        "main.latex": ["templates/p2kb-pasm2-reference.latex"],
        "foundation": ["templates/p2kb-pasm2-foundation.sty"],
        "content":    ["templates/p2kb-pasm2-content.sty"],
        "diagrams":   ["templates/p2kb-pasm2-diagrams.sty"],
        "lua.figures":["filters/p2kb-pasm2-figures.lua"],
        "lua.tables": ["filters/p2kb-pasm2-tables.lua"],
        "lua.mnemonic-bold":["filters/p2kb-pasm2-mnemonic-bold.lua"],
        "lua.code-coloring":["filters/p2kb-pasm2-code-coloring.lua"],
        "lua.entry-format": ["filters/p2kb-pasm2-entry-format.lua"],
        "lua.entry-headers":["filters/p2kb-pasm2-entry-headers.lua"],
        "lua.pagination":   ["filters/p2kb-pasm2-pagination.lua"],
    }),
    "p2-debug-window-manual": ("debugwin", {
        "main.latex": ["templates/p2kb-debugwin.latex"],
        "foundation": ["templates/p2kb-debugwin-foundation.sty"],
        "content":    ["templates/p2kb-debugwin-content.sty"],
        "lua.code-coloring":["filters/p2kb-debugwin-code-coloring.lua"],
    }),
    "p2-io-and-smart-pins-user-guide": ("iosp", {
        "main.latex": ["templates/p2kb-iosp-reference.latex"],
        "foundation": ["templates/p2kb-iosp-foundation.sty"],
        "content":    ["templates/p2kb-iosp-content.sty"],
        "diagrams":   ["templates/p2kb-iosp-diagrams.sty"],
        "lua.figures":["filters/p2kb-iosp-figures.lua"],
        "lua.tables": ["filters/p2kb-iosp-tables.lua"],
        "lua.mnemonic-bold":["filters/p2kb-iosp-mnemonic-bold.lua"],
        "lua.code-coloring":["filters/p2kb-iosp-code-coloring.lua"],
        "lua.pagination":   ["filters/p2kb-iosp-pagination.lua"],
    }),
    "p2-pasm-desilva-style": ("desilva", {
        "main.latex": ["templates/p2kb-desilva.latex"],
        "foundation": ["templates/p2kb-desilva-foundation.sty"],
        "content":    ["templates/p2kb-desilva-content.sty"],
        "diagrams":   ["templates/p2kb-desilva-diagrams.sty"],
        "lua.mnemonic-bold":["filters/p2kb-desilva-mnemonic-bold.lua"],
        "lua.code-coloring":["filters/p2kb-desilva-code-coloring.lua"],
        "lua.semantic":     ["filters/p2kb-desilva-semantic.lua"],
        "lua.pagination":   ["filters/p2kb-desilva-pagination.lua"],
    }),
    "p2-single-step-debugger-manual": ("ssdbg", {
        "main.latex": ["templates/p2kb-ssdbg.latex"],
        "foundation": ["templates/p2kb-ssdbg-foundation.sty"],
        "content":    ["templates/p2kb-ssdbg-content.sty"],
        "lua.code-coloring":["filters/p2kb-ssdbg-code-coloring.lua"],
    }),
    "p2-streamer-programming-guide": ("streamer", {
        "main.latex": ["templates/p2kb-streamer-reference.latex"],
        "foundation": ["templates/p2kb-streamer-foundation.sty"],
        "content":    ["templates/p2kb-streamer-content.sty"],
        "diagrams":   ["templates/p2kb-streamer-diagrams.sty"],
        "lua.figures":["filters/p2kb-streamer-figures.lua"],
        "lua.tables": ["filters/p2kb-streamer-tables.lua"],
        "lua.mnemonic-bold":["filters/p2kb-streamer-mnemonic-bold.lua"],
        "lua.code-coloring":["filters/p2kb-streamer-code-coloring.lua"],
        "lua.pagination":   ["filters/p2kb-streamer-pagination.lua"],
    }),
}

ALL_SLUGS = ["pasm2", "debugwin", "iosp", "desilva", "streamer", "ssdbg"]

def normalize_line(line, slug):
    """Strip the document slug so renamed-but-identical lines match."""
    s = line.rstrip()
    # neutralize every slug token (longest-first; sp last) in p2kb- and macro contexts
    s = s.replace("p2kb-%s" % slug, "p2kb-X")
    # word-boundary replace of the slug token itself
    s = re.sub(r'(?<![A-Za-z0-9])%s(?![A-Za-z0-9])' % re.escape(slug), "X", s)
    return s

def load(path, slug, doc):
    full = os.path.join(BASE, doc, path)
    if not os.path.exists(full):
        return None, None
    with open(full, encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    meaningful_raw, meaningful_norm = [], []
    for ln in lines:
        st = ln.rstrip()
        if st.strip() == "":
            continue
        meaningful_raw.append(st)
        meaningful_norm.append(normalize_line(ln, slug))
    return meaningful_raw, meaningful_norm

# ---- load every used file
files = {}   # (doc, role) -> dict
for doc, (slug, roles) in DOCS.items():
    for role, paths in roles.items():
        for p in paths:
            raw, norm = load(p, slug, doc)
            if raw is None:
                print("MISSING:", p); continue
            files[(doc, role)] = {
                "doc": doc, "slug": slug, "role": role, "path": p,
                "raw": raw, "norm": norm,
                "n": len(raw),
                "raw_set": set(raw), "norm_set": set(norm),
            }

def pct(part, whole):
    return 0.0 if whole == 0 else round(100.0 * part / whole, 1)

# ---- per-file commonality: same-role and any-role, raw + normalized
role_groups = defaultdict(list)
for (doc, role), info in files.items():
    role_groups[role].append(info)

report = []
report.append("# Stylesheet / Filter Cross-Document Comparison (deterministic)\n")
report.append("Generated by `/tmp/stylesheet_compare.py`. Metric = fraction of a file's "
              "**non-blank lines** that appear **identically** in at least one other document's file.\n")
report.append("- **RAW** = literal line match. **NORM** = after stripping the document slug "
              "(`pasm2`/`ssdbg`/`desilva`/`iosp`/`streamer`/`debugwin`) so renamed-identical lines count as shared.\n")
report.append("- **same-role** = compared only against the same kind of file in other docs "
              "(foundation↔foundation, lua.tables↔lua.tables, …). **any** = against every other used file.\n")

# precompute global pools
all_norm_by_doc = defaultdict(set)
for (doc, role), info in files.items():
    all_norm_by_doc[doc] |= info["norm_set"]

for doc, (slug, roles) in DOCS.items():
    report.append("\n## %s  (slug: `%s`)\n" % (doc, slug))
    report.append("| file | role | lines | same-role RAW%% | same-role NORM%% | any-doc NORM%% |")
    report.append("|------|------|------:|------:|------:|------:|")
    for role in roles:
        info = files.get((doc, role))
        if not info: continue
        # same-role others
        others = [o for o in role_groups[role] if o["doc"] != doc]
        other_raw = set().union(*[o["raw_set"] for o in others]) if others else set()
        other_norm = set().union(*[o["norm_set"] for o in others]) if others else set()
        sr_raw = pct(sum(1 for l in info["raw"] if l in other_raw), info["n"])
        sr_norm = pct(sum(1 for l in info["norm"] if l in other_norm), info["n"])
        # any-doc (normalized) — against union of all OTHER docs' all lines
        anypool = set().union(*[all_norm_by_doc[d] for d in DOCS if d != doc])
        any_norm = pct(sum(1 for l in info["norm"] if l in anypool), info["n"])
        present = "—" if not others else ("%d other%s" % (len(others), "" if len(others)==1 else "s"))
        report.append("| `%s` | %s | %d | %s | %s | %s |" % (
            os.path.basename(info["path"]), role, info["n"], sr_raw, sr_norm, any_norm))

# ---- foundation N-way fracture map (normalized)
report.append("\n## Foundation files — N-way fracture map (slug-normalized)\n")
fnd = [files[(d, "foundation")] for d in DOCS if (d, "foundation") in files]
line_doc_count = defaultdict(set)
for info in fnd:
    for l in info["norm_set"]:
        line_doc_count[l].add(info["doc"])
buckets = defaultdict(int)
for l, ds in line_doc_count.items():
    buckets[len(ds)] += 1
total_distinct = len(line_doc_count)
report.append("Distinct normalized lines across all 6 foundations: **%d**\n" % total_distinct)
report.append("| shared by N docs | distinct lines | note |")
report.append("|---:|---:|------|")
notes = {6:"universal core (identical in all 6)", 1:"unique to a single doc (true divergence)"}
for n in range(6, 0, -1):
    report.append("| %d | %d | %s |" % (n, buckets.get(n,0), notes.get(n,"")))

# per-foundation: how much is universal vs unique
report.append("\n### Each foundation: universal vs unique composition\n")
report.append("| doc | lines | %% in ALL-6 core | %% unique to it |")
report.append("|-----|------:|------:|------:|")
universal = {l for l,ds in line_doc_count.items() if len(ds)==6}
unique = {l for l,ds in line_doc_count.items() if len(ds)==1}
for info in fnd:
    u = sum(1 for l in info["norm"] if l in universal)
    q = sum(1 for l in info["norm"] if l in info["norm_set"] and l in unique)
    report.append("| %s | %d | %s | %s |" % (info["doc"], info["n"], pct(u, info["n"]), pct(q, info["n"])))

out = "\n".join(report) + "\n"
with open("/tmp/stylesheet_compare_report.md", "w") as f:
    f.write(out)
print(out)

# ---- supplementary: exact divergence among the 4 near-twin foundations
print("\n\n===== TWIN FOUNDATION DIVERGENCE (pasm2/debugwin/iosp/streamer, normalized) =====")
twins = ["p2-assembly-language-manual","p2-debug-window-manual",
         "p2-io-and-smart-pins-user-guide","p2-streamer-programming-guide"]
tw = {d: files[(d,"foundation")]["norm_set"] for d in twins}
common4 = set.intersection(*tw.values())
print("lines common to ALL 4 twins: %d" % len(common4))
for d in twins:
    extra = tw[d] - common4
    print("\n-- %s : %d line(s) NOT in the common-4 core:" % (d, len(extra)))
    for l in sorted(extra):
        print("     | %s" % l[:110])

print("\n\n===== TABLE LUA divergence (pasm2 vs iosp vs streamer, normalized) =====")
for d in ["p2-assembly-language-manual","p2-io-and-smart-pins-user-guide","p2-streamer-programming-guide"]:
    print("  %-40s lua.tables lines: %d" % (d, files[(d,"lua.tables")]["n"]))
ts = {d: files[(d,"lua.tables")]["norm_set"] for d in
      ["p2-assembly-language-manual","p2-io-and-smart-pins-user-guide","p2-streamer-programming-guide"]}
print("  common to all 3 table.lua: %d distinct lines" % len(set.intersection(*ts.values())))
print("  iosp vs streamer symmetric diff: %d lines" % len(ts["p2-io-and-smart-pins-user-guide"] ^ ts["p2-streamer-programming-guide"]))
