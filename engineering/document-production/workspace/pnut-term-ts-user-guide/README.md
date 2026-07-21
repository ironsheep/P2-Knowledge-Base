# Workspace — PNut-Term-TS User Guide

Build-staging tree for the PNut-Term-TS User Guide. Source of truth is
`../../manuals/pnut-term-ts-user-guide/opus-master/`; this workspace assembles,
escapes, and stages CHANGED files to `../../outbound/pnut-term-ts-user-guide/`.

## Build flow

1. `./assemble-manual.sh` — concatenates `opus-master/front-matter.md` +
   `pnut-term-ts-body.md` into `PNut-Term-TS-User-Guide.md`.
2. `latex-escape-all.sh` — escape LaTeX characters.
3. Stage ONLY changed files to `outbound/` (Sacred Rule #6), then Stephen
   deploys to PDF Forge.

Normally run via the `prepare-manual` skill, not by hand.

## Open wiring (TBD before first render)

- **`request.json` `template` is a placeholder** (`TEMPLATE-TBD-see-PLANNING`).
  Decide at first render whether to create a dedicated `p2kb-pnut-term-ts-guide`
  template or map to an existing `p2kb-platform` template. See
  `../../manuals/pnut-term-ts-user-guide/PLANNING.md`.
- `templates/` and `assets/` are staged empty pending that decision + screenshot
  capture.
