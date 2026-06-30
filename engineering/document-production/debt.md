# Document Production Technical Debt

> **This tracker has moved.** Cross-cutting document-production debt and cleanup is
> now maintained in **[`PUNCH-LIST.md`](PUNCH-LIST.md)** (the active, skill-maintained
> list); per-manual debt lives in each `workspace/<slug>/PUNCH-LIST.md`.

This file remains as the document-production node referenced by the repo debt index
([`../knowledge-base-debt.md`](../knowledge-base-debt.md)) — follow the link above for
current items.

The original 2025 content (template-synchronization chaos, per-document fork
inconsistencies, scattered template/filter copies) is **resolved**: the 2026-06-10
**platform unification** retired the bespoke `p2kb-<slug>-*` forks in favor of the
single shared `p2kb-platform-*` stack, collapsing the template-sync, naming, and
Lua-filter-duplication debt it described. That history is preserved in git.

## Where current debt lives

| Scope | Tracker |
|-------|---------|
| Cross-cutting doc-production cleanup | [`PUNCH-LIST.md`](PUNCH-LIST.md) |
| Per-manual issues | `workspace/<slug>/PUNCH-LIST.md` |
| Visual-asset / image-extraction debt | [`../ingestion/visual-assets-catalog/INGESTION-IMAGE-EXTRACTION-MATRIX.md`](../ingestion/visual-assets-catalog/INGESTION-IMAGE-EXTRACTION-MATRIX.md) |
| KB / YAML content debt | [`../knowledge-base-debt.md`](../knowledge-base-debt.md) |

---
*Superseded 2026-06-30 by `PUNCH-LIST.md`. Originally consolidated 2025-08-31.*
