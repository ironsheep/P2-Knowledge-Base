# P2 XBYTE Programming Guide — Workspace

PDF-production workspace for the P2 XBYTE Programming Guide. The template stack
is the shared `p2kb-platform-*` family (front matter, code-block coloring, reference
blocks) per `engineering/document-production/standards/manual-front-matter-and-code-coloring-standard.md`.
This manual is a **twin** that consumes the platform stack with a thin local override.

## Source of truth

The canonical content lives in the manual's `opus-master/`, NOT in this workspace:

```
../../manuals/p2-xbyte-programming-guide/opus-master/
  ├── front-matter.md   # banner, title, organization panel, copyright, how-to-use, conventions
  └── xbyte-body.md      # Parts I–IV (Chapters 1–14 + Appendices A–D + Index)
```

`assemble-manual.sh` concatenates `front-matter.md + xbyte-body.md` into the
workspace `P2-XBYTE-Programming-Guide.md` (front matter prepended at assembly).

## Three-stage pipeline

1. **Edit** `opus-master/*.md` (canonical source)
2. **Assemble + escape** here: `bash assemble-manual.sh`, then `latex-escape-all.sh` (the `prepare-manual` skill does both)
3. **Stage CHANGED files only** to `../../outbound/p2-xbyte-programming-guide/` for PDF Forge

The master filename `P2-XBYTE-Programming-Guide.md` is sacred — never rename or suffix it.

## Template stack

| File | Role |
|------|------|
| `templates/p2kb-xbyte-reference.latex` | Main template (11pt book, loads platform foundation + content, then the two locals) |
| `templates/p2kb-xbyte-local.sty` | Per-manual override (thin — empty for this twin) |
| `templates/p2kb-xbyte-diagrams.sty` | Per-manual TikZ figures (`\DiagXbyteLoop`, `\DiagLutEntry`, `\DiagDispatchCycle`, `\DiagModeOperand`) on the platform diagram base |
| `request.json` | PDF Forge build request — references the **platform** lua filters by name (already on the Forge) |

The shared `p2kb-platform-{foundation,content,diagrams}.sty` and the
`p2kb-platform-*.lua` filters are NOT in this workspace — the Forge already holds
them from the rest of the manual family.

## Document Status

| Item | Status |
|------|--------|
| Content grounding (vs KB + Silicon Doc v35) | digest in `../../manuals/p2-xbyte-programming-guide/audit/` |
| Template stack (twin on platform) | **Complete** |
| Front matter (house standard) | **Complete** |
| LaTeX escaping + outbound staging | run `prepare-manual` |
| First Forge build (v0.1.0 review draft) | pending |

## Notes for first build

- Single-image cover `assets/book-artwork.png` — identical md5 across the manual family.
- Emoji markers (⚠️ 💡 🔧) match the live manual family; confirm rendering on first build.
- Four TikZ figures (Ch 1/4/5/7) on the platform diagram base; daemon-verified rendering
  in the v0.1.0 round-trip (clean compile, chapter-numbered, List of Figures present).
