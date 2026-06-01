# P2 Streamer Programming Guide — Workspace

PDF-production workspace for the P2 Streamer Programming Guide. The template stack
mirrors the live IOSP User Guide family (front matter, code-block coloring, reference
blocks) per `engineering/document-production/standards/manual-front-matter-and-code-coloring-standard.md`.

## Source of truth

The canonical content lives in the manual's `opus-master/`, NOT in this workspace:

```
../../manuals/p2-streamer-programming-guide/opus-master/
  ├── front-matter.md     # banner, title, organization panel, copyright, how-to-use, conventions
  └── streamer-body.md    # Parts I–V (Chapters 1–18 + Appendices A–D + Index)
```

`assemble-manual.sh` concatenates `front-matter.md + streamer-body.md` into the
workspace `P2-Streamer-Programming-Guide.md` (front matter prepended at assembly).

## Three-stage pipeline

1. **Edit** `opus-master/*.md` (canonical source)
2. **Assemble + escape** here: `bash assemble-manual.sh`, then `latex-escape-all.sh` (the `prepare-manual` skill does both)
3. **Stage CHANGED files only** to `../../outbound/p2-streamer-programming-guide/` for PDF Forge

The master filename `P2-Streamer-Programming-Guide.md` is sacred — never rename or suffix it.

## Template stack

| File | Role |
|------|------|
| `templates/p2kb-streamer-reference.latex` | Main template (11pt book, loads the three `.sty`) |
| `templates/p2kb-streamer-foundation.sty` | Pandoc compatibility + core packages |
| `templates/p2kb-streamer-content.sty` | Colors, code blocks (Spin2 blue / PASM2 green), reference blocks (syntax slate / layout bronze / formula indigo), part handling |
| `templates/p2kb-streamer-diagrams.sty` | TikZ stub (inert — no `\Diag*` macros used yet) |
| `filters/p2kb-streamer-code-coloring.lua` | Colors `` ```pasm2 ``/`` ```spin2 `` + `` ```syntax/layout/formula `` blocks |
| `filters/p2kb-streamer-{figures,tables,mnemonic-bold,pagination}.lua` | Family filters |
| `request.json` | PDF Forge build request |

## Document Status

| Item | Status |
|------|--------|
| Content audit (vs KB + Silicon Doc v35) | **Complete** — see `../../manuals/p2-streamer-programming-guide/audit/` |
| Template stack (cloned from live IOSP) | **Complete** |
| Front matter (house standard) | **Complete** |
| Code/reference-block tagging | **Complete** |
| LaTeX escaping + outbound staging | run `prepare-manual` |
| First Forge build | pending (verify checklist in the audit doc) |

## Notes for first build

- One open content item: the §15.1 VGA `$F080_0000` sync mode-long is unverified (cited from OBEX) — see the audit doc.
- Emoji markers (⚠️ 💡 🔧) match the live PASM2 manual; confirm rendering on first build.
- Eight upstream KB defects found during the audit are staged in `engineering/operations/P2KB-CORRECTION-FINDINGS.md` (F-016…F-021) for a separate YAML pass.
