# The P2 Architect's Guide — Workspace

PDF-production workspace for *The P2 Architect's Guide — Thinking in Cogs, Pins, and
Forces*. This is the **first manual born directly on the unified presentation
platform** — it rides the shared `p2kb-platform-*` `.sty` and lua filters and adds
only a thin per-manual skin, per
`engineering/document-production/methodology/presentation-platform-unification-STUDY.md`
and the manual front-matter / code-coloring standard
(`engineering/document-production/standards/manual-front-matter-and-code-coloring-standard.md`).

## Source of truth

The canonical content lives in the manual's `opus-master/`, NOT in this workspace:

```
../../manuals/p2-architect-guide/opus-master/
  ├── front-matter.md            # banner, title, organization panel, copyright, how-to-use, conventions
  └── architect-guide-body.md    # Parts I-III / Ch1-14 + In Closing + Appendix A/B + Glossary + Where-to-Next (single-file, DD3)
```

`assemble-manual.sh` concatenates `front-matter.md + architect-guide-body.md` into
the workspace `P2-Architect-Guide.md` (front matter prepended at assembly).

## Three-stage pipeline

1. **Edit** `opus-master/*.md` (canonical source)
2. **Assemble + escape** here: `bash assemble-manual.sh`, then `latex-escape-all.sh`
   (the `prepare-manual` skill does both)
3. **Stage CHANGED files only** to `../../outbound/p2-architect-guide/` for PDF Forge

The master filename `P2-Architect-Guide.md` is sacred — never rename or suffix it.

## Template stack (platform-unified)

| File | Role |
|------|------|
| `templates/p2kb-architect-reference.latex` | Main template (11pt book); loads the two shared platform `.sty` + the two local `.sty` |
| *(shared)* `platform/templates/p2kb-platform-foundation.sty` | geometry, penalties, titlespacing, hyperref |
| *(shared)* `platform/templates/p2kb-platform-content.sty` | code/reference box family (Spin2 blue / PASM2 green; syntax / layout / formula), contmarkers, keep-together |
| `templates/p2kb-architect-local.sty` | per-manual skin — adds **`P1NoteBlock`** for the "P1 note:" sidebars (DD1) |
| `templates/p2kb-architect-diagrams.sty` | TikZ diagram macros — 4 figures: `\SpaceTimeSpectrumDiagram`, `\FourPhaseSpineDiagram`, `\RobotDecompositionDiagram`, `\StreamingPipelineDiagram` |
| *(shared)* `platform/filters/p2kb-platform-{figures,tables,mnemonic-bold,code-coloring,pagination}.lua` | family filters |
| `filters/p2kb-architect-local.lua` | maps `::: p1note` → `P1NoteBlock` (registered LAST, after the platform filters; DD1) |
| `request.json` | PDF Forge build request (template + filter list + metadata) |

> **Platform files are referenced by bare name** in `request.json` and
> `p2kb-architect-reference.latex`; the Forge stage step stages them from
> `../../platform/` only if the manual store lacks them. Only the
> `p2kb-architect-*` locals + the local filter are per-manual.

## Conventions fixed at scaffold

- **`::: p1note` … `:::`** fenced div → `P1NoteBlock` (the P1→P2 migration sidebar).
- Code is fenced ` ```spin2 ` / ` ```pasm2 ` and **pnut_ts-verified** (never code-divisions).
- Figures are TikZ macros in `p2kb-architect-diagrams.sty`, invoked via a ` ```{=latex} ` block + a `::: {.figurecaption}` div (chapter-scoped numbering, e.g. Figure 9.1).

## Document Status

| Item | Status |
|------|--------|
| Charter / creation-guide / voice-guide | **Complete** (re-scoped to the three-act design/realization book) — `../../manuals/p2-architect-guide/{PLANNING,creation-guide,voice-guide}.md` |
| Body — Parts I–III / Chapters 1–14 + In Closing | **Complete** |
| Back matter (Appendix A/B, glossary, where-to-next) | **Complete** |
| Front matter (house standard) | **Complete** |
| Figures (4 TikZ) | **Complete** |
| **RELEASED** | **v1.0.0 — 2026-07-08 (maiden, 53pp)** |

History: the first-draft sprint plan is `engineering/planning/P2-ARCHITECT-GUIDE-FIRSTDRAFT-SPRINT-PLAN.md`; the design-book re-cut is in `../../manuals/p2-architect-guide/PLANNING.md` §5.
