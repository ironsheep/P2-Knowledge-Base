# AN008 Sigma-delta ADC — Extraction Audit (pass 5 validation)

**Source:** Parallax Semiconductor Application Note AN008 v1.0 (2011), 10 pp.
**Platform:** Propeller 1 / P8X32A (Spin1 + PASM1).
**Mode:** new (greenfield). **Wave:** p1-appnotes-2026-06 (MAP, passes 1-5 stage-only).
**Extraction date:** 2026-06-27.

## Tooling provenance
- **Text layer probe:** `pdftotext -f 1 -l 1` → clean, intact (P2-corpus spacing quirks only, NOT ciphered). **No OCR forced.**
- **Pass 1 content:** `pdf-layout` → `AN008-Sigma-delta-ADC-text.txt` (582 lines, layout-preserving). Curated → `complete-AN008-reference.md`. (`pdf2md`/docling intermediate produced then discarded — 1.1 MB base64 blob, fully superseded by text.txt + page renders.)
- **Pass 2 code:** in-PDF listings transcribed verbatim from the text layer into `assets/code-2026-06-27/`. **NOT compiled** — no P1 compiler in environment (`pnut_ts` is P2-only; `flexspin`/`bstc` absent). `code_validated: false`.
- **Pass 3 images:** `pdftoppm -r 150` page renders (vector schematics) + `pdfimages` for 2 embedded raster photos; quality-gated via `image_dominant_colors`.

## Section-by-section completeness

| Section | Pages | Captured? | Notes |
|---|---|---|---|
| Masthead / Abstract | 1 | ✅ | Verbatim abstract in reference. |
| Introduction | 1 | ✅ | |
| Sigma-Delta Principle (Figs 1-2) | 1 | ✅ | Full op-amp→flip-flop derivation + worked duty-cycle example. |
| Counter Registers (Fig 3) | 2 | ✅ | CNT/CTRx/FRQx/PHSx; positive-w/-feedback mode; CTRx bit-field. |
| Hardware Configuration (Fig 4) | 3 | ✅ | Standard RC circuit; 83.33%/16.67% margins; dual-cap rationale. |
| Layout Considerations (Fig 5) | 4 | ✅ | Photo extracted (2 resolutions). |
| Software Procedure + Listing 1 | 4-5 | ✅ | 5-step sequence + PASM listing + cognew. |
| Calibration (Figs 6-7) + Listing 2 | 5-8 | ✅ | Both HW options + both SW options + binary-search listing. |
| Variations (Figs 8-10, Eqs 1-2) | 8-9 | ✅ | Multiple inputs / AC / extended range + bias-resistor math. |
| Resources / References / Revision / legal | 9-10 | ✅ | |

**Structural completeness: 100%** — all 10 pages, all 10 figures, both listings, all inline fragments, all 4 equations accounted for.

## Pass counts
- **Paragraphs / prose:** all body sections captured (≈ 30 prose paragraphs + 2 numbered procedures).
- **Tables:** 0 true ruled tables in the document (no `camelot` needed). Figure 3 is a bit-field diagram, cataloged as an image.
- **Code (in-PDF only):** 2 listings captured (Listing 1 ~38 lines; Listing 2 ~55 lines) + 3 inline fragments (cognew, Spin scaling expr, maxs/mins clamp). **0 compiled / 0 validated** — "NOT validated, no P1 compiler." External code-archive ZIP referenced (an008) but not provided → gap.
- **Images:** 12 files extracted = 10 page renders + 2 embedded photos; **all 12 quality-passed**; **0 OCR'd** (text layer supplied all labels). 10 logical figures cataloged.

## Known extraction caveats (→ gaps)
1. **Equations 1a/1b/2a/2b** — the text layer mangles fraction bars (e.g. `100VHI  VLO / 3.3`). The variable/constant set and the worked results (R1≈455k, R2≈224k) are reliable; exact operator grouping in Eq 1a/1b should be re-verified against `page-09.png` before any downstream reuse.
2. **Listing 2 CON symbols** — references `ADC_INTERVAL0`, `ADC_RANGE`, `CALIB_PIN` not re-declared in the printed listing (assumed from Listing 1's CON). Captured verbatim, not patched.
3. **Figure 3 exact bit boundaries** — the field positions (feedback pin in the "Destination" field, input pin in bits 8..0) are read from the diagram; precise bit ranges of the Destination/Feedback field should be corroborated against AN001 (Counters) / P1 datasheet at YAML-build time.

## Trust
- **Authority tier:** 🏆 primary (Parallax first-party application note; authoritative for P1 counter sigma-delta technique).
- **code_validated:** false (P1, no compiler) — captured-not-processed.
- All facts single-source (this note) pending P1-corpus corroboration (AN001 counters, P1 datasheet) at a later cross-source pass.
