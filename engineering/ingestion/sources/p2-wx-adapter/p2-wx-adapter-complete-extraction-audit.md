# P2 WX Adapter (#64007) — Extraction Audit (re-extraction)

**Source**: 64007-P2-WX-Adapter-Guide-v1.0.pdf — v1.0, 11/12/2020, 7 pp, 924 KB
**Mode**: re-extraction (prior 2025-08-29 PDF-era capture; 8+-image debt) — STAGE-ONLY
**Extraction date**: 2026-06-27
**Tooling**: `pdftotext` (text-layer sanity) · `pdf2md`/docling (content+tables) ·
`camelot lattice` (pin table) · `pdfimages -all` (images) · `image-tools-mcp` (quality gate + OCR)

## Pre-flight: text-layer integrity

`pdftotext -f 1 -l 1` returned clean, well-formed English (NOT ciphered) → **digitally-generated
text layer, no forced-OCR needed.** Content extracted from the real text stream; OCR reserved for
in-figure labels only.

## Section-by-section completeness (5-pass audit protocol)

| Page | Section | Captured | Notes |
|---|---|---|---|
| 1 | Banner, intro, Features, Specifications | ✅ | full |
| 2 | Quick-Start: Items required, Connecting the Hardware | ✅ | full |
| 3 | Update Firmware A (connect) + B (one-time setup 1–3) | ✅ | full |
| 4 | One-time setup 4–6; Using P2 Loader 1–3 | ✅ | full |
| 5 | P2 Loader 4–5; LED demo tip | ✅ | full |
| 6 | Pin Connections table + diagram caption | ✅ | table clean (camelot-confirmed) |
| 7 | Dimensions, Resources/Downloads, Revision History | ✅ | full |

**Coverage: 100%** of prose, the pin table, and all figures. No section dropped.

## Pin table fidelity (the prior defect)

Prior `*-narrative.txt` rendered the pin table **column-interleaved** (header pin / WiFi pin /
function fields split across separate lines — readable only with effort). This re-extraction's
`pdf2md` produced a correctly-structured Markdown table, **independently confirmed by
`camelot lattice`** (1 table found, identical cell values). Pin map is now clean and
cross-check-ready against `parallax-wx-wifi`.

## Per-pass counts

- **Pass 1 (content)**: ~40 prose paragraphs/list-items + 1 table (8 data rows). Clean text → `p2-wx-adapter-text.txt` (74 lines), curated → `complete-p2-wx-adapter-reference.md`.
- **Pass 2 (code)**: **0 code examples** — passive adapter; doc references only a prebuilt `LED57.binary`/`P2_httpd_xxxx.ota` (no source). Nothing to validate with `pnut_ts`. `assets/code-2026-06-27/` left empty (no code in source).
- **Pass 3 (images)**: 11 extracted / 11 quality-passed / 0 black-failed; key figures OCR-probed (noisy on photos, used for content-class confirmation only). Catalog written.

## Trust

GREEN — official Parallax hardware guide; part numbers, specs, and pin map internally
consistent and corroborated by the document's own diagram. No fabrications.
