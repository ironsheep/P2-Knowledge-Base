# Extraction Audit — P2 microSD Add-on Board (#64009)

**Source:** `64009-P2-microSD-AddOn-Guide-v1.0.pdf`
**Mode:** new (greenfield)
**Wave:** addon-wave-2026-06 (parallel MAP agent, passes 1–5, STAGE-ONLY)
**Date:** 2026-06-27
**Tooling:** `pdftotext` (clean text layer — no OCR needed), `pdf2md` (docling),
`camelot lattice` (pin table CSV), `pdfimages -j` + `image-tools-mcp` (image gate + OCR).

## Pre-flight: text-layer integrity
`pdftotext -f 1 -l 1` returned clean, readable English (not ciphered) → **no forced OCR**.
3-page digitally-generated product guide.

## Pass 1 — Content
- Full text → `p2-microSD-addon-text.txt` (151 lines, complete; all 3 pages).
- Curated → `complete-p2-microSD-addon-reference.md`.
- **Paragraphs/sections:** Overview, Features (4 bullets), Specifications (4 bullets),
  Pin Connections (1 table, 9 rows), Dimensions, Resources/Downloads, Revision History.
- **Tables:** 1 ruled table (Pin Connections) — extracted cleanly by camelot lattice →
  `assets/pin-connections-table.csv`. Cross-checks 1:1 with the text-layer rendering.

## Pass 2 — Code examples
- **Extracted: 0 / Validated: 0 / Failed: 0.** This is a hardware accessory guide; it carries
  **no Spin2/PASM2 listings** (no driver snippets, no boot code). `pnut_ts` not invoked.
  `assets/code-2026-06-27/` created but empty (expected).

## Pass 3 — Images
- **Extracted: 4** (`pdfimages -j`): p1 product photo (1600x1227), p1 banner (904x152),
  p3 dimension drawing A (1281x1600), p3 dimension drawing B (1269x1600).
- **Quality-passed: 4/4.** Dominant colors healthy (e.g. product photo #101050 Parallax-blue,
  not #000000 → no black-capture failure).
- **OCR'd: 2** (the two dimension drawings). Pad labels read clean and consistent across both:
  `GND CLK CS MOSI MISO DET 3V3` — corroborates the Pin Connections table & SIP order.
- Catalog → `assets/images-p2-microSD-addon-2026-06-27/image-catalog.md`.

## Pass 4 — Post-processing
- SPI signal-map summary table derived (SD signal ↔ SPI role ↔ board pad) for cross-source use.
- `+N` accessory-header offset notation explained against the standard Parallax 2x6 convention
  and the IO 56–63 programming-header boot mapping.

## Pass 5 — Validation (completeness)
- All 3 pages accounted for; every section captured; the single table extracted two ways
  (text + camelot) and reconciled; image pad-labels cross-confirm the table.
- **Completeness: ~95%** of extractable content. The residual 5% = page-3 dimension-drawing
  numeric leader text (garbled under OCR); overall dims recovered from clean text Specs, so no
  fact is lost — only the per-feature drawing callouts are not transcribed (low value;
  schematic is an external download anyway).

## Proposed dashboard cells (NOT applied — proposals only)
- **Authority tier:** PRIMARY (vendor/Parallax hardware product guide — authoritative for this
  board's electrical/pinout facts).
- **C·K·I·A·X** (Content / Code / Images / Audit / Cross-source):
  - **C (Content):** 100% — all prose/specs/table captured.
  - **K (Code):** N/A — no code in source (0 examples; not a gap).
  - **I (Images):** 100% — 4/4 extracted + gated + 2 OCR'd.
  - **A (Audit):** complete (this doc).
  - **X (Cross-source):** see pass-6 proposals below (not executed in stage-only mode).
- **Completeness %:** 95% (content-complete; only non-load-bearing drawing numerals deferred).
- **Gates:** content ✓, code N/A, images ✓, audit ✓ — pass 6/7 deferred to reduce step.

## OCR-risk flags
- Page-3 dimension-drawing numerals: unreliable (rotated/leader text). **Do not** harvest PCB
  dimensions from image OCR — use text Specs (0.8 x 1.05 in / 20.32 x 26.67 mm).
- No part-number/pin-map OCR risk: all fact-bearing fields came from the clean text layer +
  camelot, with image OCR as a corroborating second signal (pad-label order matched).
