# Document Production — Punch List

Cross-cutting document-production cleanup items that are **not** specific to a single
manual. Per-manual items live in each `workspace/<slug>/PUNCH-LIST.md`.

---

## Platform-migration doc drift (cross-manual) — OPEN

**Status:** ⏳ Open — surfaced 2026-06-25 during the assembly-manual v3.1.0 dead-filter cleanup.

The 2026-06-10 platform migration retired the bespoke `p2kb-<slug>-{foundation,content}.sty`
forks and the per-manual fork Lua filters in favor of the shared `p2kb-platform-*` stack, but
several docs still reference the retired fork pipeline as if it were current:

- **`methodology/manual-production-working-set.md`** (~L111–122) — the "parts" coverage table
  lists fork filters/sty for **assembly, iosp, and streamer** (`p2kb-pasm2-pagination.lua` /
  `p2kb-pasm2-content.sty`, plus the iosp/streamer equivalents). Reconcile each migrated
  manual's row to its current platform pipeline (or its surviving local overlay).
- **`manuals/p2-single-step-debugger-manual/creation-guide.md`** (~L100) — uses a now-removed
  `workspace/p2-assembly-language-manual/filters/p2kb-pasm2-code-coloring.lua` path as an
  example; repoint to a current filter.
- **General sweep:** grep the doc tree for retired `p2kb-<slug>-{foundation,content}.sty` and
  per-manual fork-filter names across **all** migrated manuals (not just assembly) and
  reconcile any *current-state* claims to the platform stack. Leave dated snapshots and
  "adapted from …" provenance comments frozen — they correctly describe a past state.

**Routing note:** manual-specific instances of this drift are tracked in the relevant manual's
own punch list (e.g. the assembly manual's `TEMPLATE-THEORY-OF-OPERATIONS.md` rewrite and
`style-guide.md` §7.4.2 filter-name fix live in
`workspace/p2-assembly-language-manual/PUNCH-LIST.md`).

---
