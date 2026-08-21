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

**This manual is the platform-unification pilot**, so most of the stack is shared and lives in
`../../platform/`, not here. Only three files in this workspace belong to this manual alone.

| File | Where it lives | Role |
|------|----------------|------|
| `templates/p2kb-streamer-reference.latex` | here | Main template (11pt book). Loads the two platform `.sty` plus the two local ones, and defines `\DocTitle`/`\DocSubtitle`/`\DocVersion`/`\DocDate`/`\DocAuthor` from the `request.json` metadata |
| `templates/p2kb-streamer-local.sty` | here | Per-manual skins / local tail — thin for this twin |
| `templates/p2kb-streamer-diagrams.sty` | here | **Live TikZ content, not a stub.** Defines `\DiagVgaTiming`, `\DiagRgbFormats`, `\DiagDdsGoertzel`, `\DiagDataFlow`. **This manual has no `opus-master/templates/` copy, so a diagram edit exists only here — and a changed diagram MUST be staged to outbound or the PDF renders the previous picture.** |
| `p2kb-platform-foundation.sty`, `p2kb-platform-content.sty` | `../../platform/templates/` | Shared geometry, penalties, hyperref, code/reference box family, and the document-metadata macros |
| `p2kb-platform-{figures,crossref,tables,mnemonic-bold,code-coloring,pagination}.lua` | `../../platform/filters/` | The six filters `request.json` actually names |
| `request.json` | here | PDF Forge build request. `metadata.version` is the **single** home of the version — bare number, no `v`, because the cover supplies the word "Version" |

The `filters/p2kb-streamer-*.lua` directory holds the **pre-unification** forks. `request.json`
names none of them; they are kept as history and are never staged.

## Document Status

| Item | Status |
|------|--------|
| Content audit (vs KB + Silicon Doc v35) | **Complete** — see `../../manuals/p2-streamer-programming-guide/audit/` |
| Template stack (cloned from live IOSP) | **Complete** |
| Front matter (house standard) | **Complete** |
| Code/reference-block tagging | **Complete** |
| LaTeX escaping + outbound staging | run `prepare-manual` |
| Forge builds | **released through v1.0.9** (2026-08-19, 76pp); v1.1.0 staged 2026-08-21 |

## Notes for first build

- §15.1 VGA sync/blank mode-long: **resolved 2026-06-03** (commit `bdddd12`) — verified against the OBEX VGA driver (Eric R. Smith / Total Spectrum, OBEX #2847, `vga_tile_driver.spin2`); corrected `$F080_0000` → `$7F01_0000` (`X_IMM_1X32_4DAC8 | X_DACS_3_2_1_0`) with VSYNC as a separate `DRVNOT` pin toggle. See `PUNCH-LIST.md`.
- Emoji markers (⚠️ 💡 🔧) match the live PASM2 manual; confirm rendering on first build.
- Eight upstream KB defects found during the audit are staged in `engineering/operations/P2KB-CORRECTION-FINDINGS.md` (F-016…F-021) for a separate YAML pass.
