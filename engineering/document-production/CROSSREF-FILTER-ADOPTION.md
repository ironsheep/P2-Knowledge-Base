# Cross-Reference Filter — Adoption & Audit Tracker

**Filter:** `platform/filters/p2kb-platform-crossref.lua` (added 2026-06-26)
**What it does:** auto-links in-prose structure references — "Chapter N", "Appendix X",
"Section N.N", "§N.N" — to their section anchors, so they become clickable in the PDF.
Opt-in per manual via that manual's `request.json` `lua_filters`.

## Why this tracker exists (the out-of-date flag)

The filter is **new shared behavior**. Auto-linking is heuristic and can mis-fire on a
given manual (e.g. a manual that writes "Chapter 3" meaning *another document*, a stray
"Section 1.2" inside prose that isn't a real cross-ref, or an appendix-letter collision).
So adoption is deliberately **gated per manual**:

- **We do NOT force a re-release** of any already-published manual just to gain this.
- The **next time each manual is released** (for any reason), its release MUST:
  1. add `p2kb-platform-crossref` to that manual's `request.json` `lua_filters`, and
  2. **visually audit** the rendered PDF for cross-ref behavior — every auto-link points
     where it should, and nothing got wrongly linked — before promoting.
- Until both are done, the manual's status below stays **PENDING AUDIT**.

`release-manual` Phase 1/Phase 4 should consult this tracker; flip a row to ADOPTED ✅
only after the per-manual visual audit passes.

## ⚠️ REQUIRED: crossref must be listed BEFORE the tables filter

**Ordering is not optional.** `p2kb-platform-tables.lua` rewrites every markdown table
into a `RawBlock` of LaTeX — flattening each cell's inlines to a plain string. Any filter
that runs **after** tables can no longer see (or link) references inside table cells. So in
each manual's `request.json` `lua_filters`, **`p2kb-platform-crossref` MUST come before
`p2kb-platform-tables`**, or table-borne refs (e.g. a "Quick Mode Selection" matrix's
"Ch N" cells) render as dead text while only body-prose refs link.

```jsonc
"lua_filters": [
  "p2kb-platform-figures",
  "p2kb-platform-crossref",   // ← BEFORE tables
  "p2kb-platform-tables",
  "p2kb-platform-mnemonic-bold",
  "p2kb-platform-code-coloring",
  "p2kb-platform-pagination"
]
```

The filter's header carries a matching FILTER-ORDER note, and it has an explicit `Table`
cell-walker that only fires while the Table AST still exists (i.e. when crossref runs first);
if a manual mistakenly lists crossref after tables, that handler is a harmless no-op and the
table refs silently stay dead — so the visual audit MUST include at least one table-borne
ref. (Discovered 2026-07-02 on the IOSP pilot: matrix cells were dead while 78 body-prose
`\hyperlink`s worked; root cause was tables-before-crossref ordering.)

## Status

| Manual | Cross-ref filter | Notes |
|--------|------------------|-------|
| `p2-io-and-smart-pins-user-guide` | 🔧 **ADOPTING (pilot)** | First adopter; wired into request.json 2026-06-26. 2026-07-02: fixed the filter-ordering bug (crossref now BEFORE tables) so table-cell refs link; awaiting Stephen's regen + visual audit of the Quick Mode Matrix links |
| `p2-assembly-language-manual` | ⏳ PENDING AUDIT | released v3.1.0; adopt + audit on next release |
| `p2-pasm-desilva-style` | ⏳ PENDING AUDIT | released v3.0.1; adopt + audit on next release |
| `p2-debug-window-manual` | ⏳ PENDING AUDIT | released v1.0.1; adopt + audit on next release |
| `p2-streamer-programming-guide` | ⏳ PENDING AUDIT | released v1.0.2; adopt + audit on next release |
| `p2-single-step-debugger-manual` | ⏳ PENDING AUDIT | in tech review; adopt + audit when first released |
| `p2-getting-started-guide` | ⏳ PENDING AUDIT | released v1.0.0; adopt + audit on next release |
| `p2-architect-guide` | ⏳ PENDING AUDIT | in development; adopt + audit when first released |
| `p2-layout-torture-test` | — N/A (instrument) | not a publication |
| `ai-privacy-guide` | — N/A | presentation-class, not on the shared platform stack |

**Legend:** 🔧 adopting/proving · ⏳ pending per-manual audit on next release (NOT a forced release) · ✅ adopted + audited.
