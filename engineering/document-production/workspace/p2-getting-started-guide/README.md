# Getting Started with the Propeller 2 — Workspace

PDF-production workspace for *Getting Started with the Propeller 2 — Meet the Chip,
Read Its Code, Put It to Work*. It rides the shared `p2kb-platform-*` `.sty` and lua
filters and adds
only a thin per-manual skin, per
`engineering/document-production/methodology/presentation-platform-unification-STUDY.md`
and the manual front-matter / code-coloring standard
(`engineering/document-production/standards/manual-front-matter-and-code-coloring-standard.md`).

## Source of truth

The canonical content lives in the manual's `opus-master/`, NOT in this workspace:

```
../../manuals/p2-getting-started-guide/opus-master/
  ├── front-matter.md            # banner, title, organization panel, copyright, how-to-use, conventions
  └── getting-started-body.md    # Ch1–3 + Appendix A/B + Glossary + Where-to-Next (single-file, DD3)
```

`assemble-manual.sh` concatenates `front-matter.md + getting-started-body.md` into
the workspace `P2-Getting-Started-Guide.md` (front matter prepended at assembly).

## Three-stage pipeline

1. **Edit** `opus-master/*.md` (canonical source)
2. **Assemble + escape** here: `bash assemble-manual.sh`, then `latex-escape-all.sh`
   (the `prepare-manual` skill does both)
3. **Stage CHANGED files only** to `../../outbound/p2-getting-started-guide/` for PDF Forge

The master filename `P2-Getting-Started-Guide.md` is sacred — never rename or suffix it.

## Template stack (platform-unified)

| File | Role |
|------|------|
| `templates/p2kb-getting-started-reference.latex` | Main template (11pt book); loads the two shared platform `.sty` + the two local `.sty` |
| *(shared)* `platform/templates/p2kb-platform-foundation.sty` | geometry, penalties, titlespacing, hyperref |
| *(shared)* `platform/templates/p2kb-platform-content.sty` | code/reference box family (Spin2 blue / PASM2 green; syntax / layout / formula), contmarkers, keep-together |
| `templates/p2kb-getting-started-local.sty` | per-manual skin — adds **`P1NoteBlock`** for the "P1 note:" sidebars (DD1) |
| `templates/p2kb-getting-started-diagrams.sty` | TikZ stub (inert — no `\Diag*` macros for v0.1.0; DD5) |
| *(shared)* `platform/filters/p2kb-platform-{figures,tables,mnemonic-bold,code-coloring,pagination}.lua` | family filters |
| `filters/p2kb-getting-started-local.lua` | maps `::: p1note` → `P1NoteBlock` (registered LAST, after the platform filters; DD1) |
| `request.json` | PDF Forge build request (template + filter list + metadata) |

> **Platform files are referenced by bare name** in `request.json` and
> `p2kb-getting-started-reference.latex`; the Forge stage step stages them from
> `../../platform/` only if the manual store lacks them. Only the
> `p2kb-getting-started-*` locals + the local filter are per-manual.

## Conventions fixed at scaffold

- **`::: p1note` … `:::`** fenced div → `P1NoteBlock` (the P1→P2 migration sidebar).
- Code is fenced ` ```spin2 ` / ` ```pasm2 ` and **pnut_ts-verified** (never code-divisions).
- Figures deferred (DD5): mark intended locations as `> **[Figure — …]**` and log to `PUNCH-LIST.md`.

## Document Status

| Item | Status |
|------|--------|
| Charter / creation-guide / voice-guide | **Complete** — `../../manuals/p2-getting-started-guide/{PLANNING,creation-guide,voice-guide}.md` |
| Workspace + opus-master skeleton (this scaffold) | **Complete** (task #93) |
| Chapters 1–3 | pending (tasks #94–#96) |
| Back matter (Appendix A/B, glossary, where-to-next) | pending (task #97) |
| Front matter (house standard) | pending (task #98) |
| First Forge build + first-draft review (DoD) | pending (task #99) |

Sprint plan: `engineering/planning/P2-ARCHITECT-GUIDE-FIRSTDRAFT-SPRINT-PLAN.md`.
