# Workspace — P2AN006 (Application Note)

Production-preparation workspace for the **P2AN006** application note. This is the
first app note to go through PDF production; it establishes the app-note production
path, which is the **same Three-Folder Rule the manuals use** (see
`../../PDF-PRODUCTION-ARCHITECTURE.md`):

```
app-notes/P2AN006/opus-master/   ← CONTENT AUTHORING (front-matter.md + P2AN006.md)   authoritative
workspace/P2AN006/               ← PRODUCTION PREPARATION (this folder)
outbound/P2AN006/                ← STAGING FOR PDF FORGE
```

## Canonical name

`P2AN006` — used identically for the workspace folder, the outbound folder, the
assembled `.md`, and the output PDF.

## Files

| File | Purpose |
|------|---------|
| `assemble-manual.sh` | Concatenates `front-matter.md` (cover) + `P2AN006.md` (body) from the app-note opus-master into `P2AN006.md` here. |
| `P2AN006.md` | The assembled working copy (generated — do not edit; edit opus-master). |
| `templates/p2kb-appnote-reference.latex` | Class template — loads the shared platform stack + the app-note override. |
| `templates/p2kb-appnote-local.sty` | App-note class override (thin: unnumbered short-doc headings). |
| `assets/book-artwork.png` | Shared cover artwork (identical md5 across the document family). |
| `request.json` | PDF Forge configuration. |

## Production stack

- **Shared platform** — `p2kb-platform-foundation.sty` + `p2kb-platform-content.sty`
  (geometry, code/reference box family, K=76 code budget) live in `../../platform/`
  and are staged to the Forge manual store once, shared by all documents.
- **App-note class layer** — `p2kb-appnote-reference.latex` + `p2kb-appnote-local.sty`
  (here). Future app notes clone these.
- **Lua filters** — the platform set (figures, tables, mnemonic-bold, code-coloring,
  pagination). The cross-reference filter (`p2kb-platform-crossref`) is the planned
  next adoption (opt-in, with a visual audit per `../../CROSSREF-FILTER-ADOPTION.md`).

## Build

```
./assemble-manual.sh
../../../tools/conversion/latex-escape-all.sh P2AN006.md      # or via prepare-manual
# stage changed files to ../../outbound/P2AN006/ ; user moves outbound -> Forge
```

Prefer the `prepare-manual` skill, which runs assemble → escape → stage-only-changed.
On the **first** manual build, the complete stack is staged (templates + filters +
request.json + md) because the Forge manual store does not yet have this document.
