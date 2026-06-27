# AN001 P8X32A Counters — Image Catalog

**Source:** Parallax Application Note AN001 *Propeller P8X32A Counters* v2.0 (19-page PDF).
**Extraction:** `pdfimages -png` (raster) + `image-tools-mcp` quality gate (`image_dimensions`, `image_dominant_colors`, `image_ocr_full`).
**Date:** 2026-06-27.

## Raster figures extracted (4 — all quality-PASSED)

All four are oscilloscope screen captures (433×363 px, light-gray scope background). Quality gate: dominant color `#F0F0F0` ≈ 93–97% (NOT `#000000`-dominant → healthy extraction, no black-capture failure). Waveform traces render as `#0000F0` (blue = APIN), and `#F00000` (red = BPIN) appears only in the differential figure — corroborating the prose. OCR returns no meaningful text (waveform photos carry no labels), confidence ≈ 0 → no OCR evidence to catalog (expected for scope captures).

| File | PDF page | Figure | Depicts | Quality | Trace colors (corroboration) |
|------|----------|--------|---------|---------|------------------------------|
| `fig03-nco-mode-00100-scope-p5.png` | 5 | Figure 3 | NCO mode `%00100` output — 40 MHz square wave (½ system clock), 6.25 ns/div | PASS | blue only (single-ended → APIN only) ✓ |
| `fig04-nco-mode-00101-scope-p6.png` | 6 | Figure 4 | NCO mode `%00101` differential output, 6.25 ns/div | PASS | blue (APIN) + red (BPIN) ✓ matches "blue=APIN, red=BPIN" caption |
| `fig06-scaling-pwm-scope-p8.png` | 8 | Figure 6 | Scaling-PWM output sawtooth, 20 ms/div | PASS | blue (highest blue % — dense PWM edges) ✓ |
| `fig11-scaling-duty-scope-p13.png` | 13 | Figure 11 | Scaling Duty-Cycle DAC output ramp, 20 ms/div | PASS | blue only ✓ |

## Vector figures NOT raster-extractable — IMAGE DEBT (10)

These are vector drawings (block diagrams / schematics / plots) embedded as PDF vector content; `pdfimages` does not recover them (it only sees the 4 embedded rasters above). Per established KB practice they require **page-render + crop** (render the page to PNG at high DPI, then crop the figure region) — deferred as image-enhancement debt; their content is fully captured in the curated reference's prose/ASCII renderings.

| Figure | PDF page | Depicts |
|--------|----------|---------|
| Figure 1 | 1 | Counter block diagram (general, all modes) |
| Figure 2 | 4 | NCO mode block diagram |
| Figure 5 | 6 | Output frequency vs. FRQA value plot (½ clk peak at 2³¹) |
| Figure 7 | 9 | Generic PLL block diagram (phase-compare, VCO, ÷2) |
| Figure 8 | 10 | PLL mode block diagram |
| Figure 9 | 11 | Duty-cycle mode block diagram |
| Figure 10 | 11 | Duty-cycle output waveform examples (FRQA $C000_0000…$1000_0000) |
| Figure 12 | 14 | Logic mode block diagram |
| Figure 13 | 15 | Pin-state-detection mode block diagram |
| Figure 14 | 16 | Σ∆-ADC external circuit schematic (3.3V, 1nF×2, 100kΩ, sense component) |

## Ruled tables — surgical CSV extraction (camelot lattice)

`camelot lattice` found 7 ruled tables; CSVs are in `camelot-tables-csv/` as a cross-check against the `pdftotext -layout` capture in `../../AN001-P8X32ACounters-text.txt`. The authoritative curated rendering of each table lives in `../../complete-AN001-reference.md`.

| CSV | Maps to |
|-----|---------|
| `an001-page-2-table-1.csv` | Table 1 (CTRA/CTRB register bit-field layout) |
| `an001-page-3-table-1.csv` | Table 2 (32 CTRMODE values) |
| `an001-page-3` (Table 3 in prose) | Table 3 (mode→application examples) — see text/curated md |
| `an001-page-5-table-1.csv` | Table 4 (NCO state progression) |
| `an001-page-9-table-1.csv` / `-table-2.csv` | Table 5 (PLLDIV field) region |
| `an001-page-14-table-1.csv` | Table 6 (Logic mode equations) |
| `an001-page-15-table-3.csv` | Table 7 (Pin-state equations) |
