# Workspace: P2 Layout Torture Test

Engineering harness for the manual layout-standards effort. Built on a clone of the
Streamer (Tier-1 twin) stack, slug `torture`. **Not a real manual.**

- **Canonical source:** `../../manuals/p2-layout-torture-test/opus-master/`
- **Case index / how to use:** `../../manuals/p2-layout-torture-test/creation-guide.md`
- **Authority for "correct":** `../../methodology/manual-layout-standards-USER-PREFERENCES.md`

## Build inputs (this workspace)

| File | Role |
|------|------|
| `P2-Layout-Torture-Test.md` | document body (engineered torture cases) |
| `request.json` | Forge build config (template + 5 lua filters) |
| `templates/p2kb-torture-reference.latex` | main template |
| `templates/p2kb-torture-foundation.sty` | foundation layer (page-break logic lives here) |
| `templates/p2kb-torture-content.sty` | content layer (`\manualpart`, code/table styling) |
| `templates/p2kb-torture-diagrams.sty` | TikZ diagram macros (`\DiagDataFlow`, …) |
| `filters/p2kb-torture-*.lua` | figures, tables, mnemonic-bold, code-coloring, pagination |

## Outbound workflow

Stage to the shared `engineering/document-production/outbound/` (escape LaTeX, copy
**only changed** files — Sacred Rule #6), then deploy to PDF Forge. Because the stack is a
faithful slug-rename of the known-good Streamer stack, the first generation should compile.

## Iteration loop

1. Change a rule (foundation / content / filter).
2. Stage changed files → outbound → Forge → PDF.
3. Check each case in the creation-guide index; record pass/fail.
4. Repeat until all cases pass; then port proven changes to the live manuals.
