# Extraction Audit — Universal Motor Driver P2 Add-on Board (#64010, RevB v2.0)

- **Source:** `64010-UniversalMotorDriverP2AddOnGuide-RevB-v2.0.pdf` (12 pp, 4.0 MB, digitally generated — Skia/PDF m110, clean text layer)
- **Extraction date:** 2026-06-27
- **Mode:** RE-EXTRACTION (replaces 2025-08-28 raw-txt-only capture)
- **Tooling:** `pdftotext` (raw text) + `pdf2md`/docling (content + tables) + `pdfimages`/`image-tools-mcp` (images). No code in document → no `pnut_ts` pass.
- **Staging only** — nothing canonical touched; no F-/G-/Q- IDs allocated.

## What this re-extraction adds over the prior capture
The 2025-08-28 baseline was a single hand-summarized markdown from a raw `pdftotext` dump: **no images, no recovered table structure, no figure evidence.** This run adds:
1. **8 cataloged images** (1 product hero, 2 wiring diagrams, 1 annotated feature board, 1 board photo, 1 mechanical/layout drawing, 1 banner, 1 warning icon) — quality-gated + OCR'd. Prior = 0 images.
2. **Clean recovered tables** (docling): both 2×6 header pinout tables, the full Specifications table (Symbol/Min/Typ/Max/Units), Absolute Maximum Ratings, and the two long Pin-Definition tables with full per-pin description prose.
3. **A new hardware fact not in the prior audit:** the Hub-Motor (#27860) **lead-color map — X=Not Connected, W=GREEN, V=BLUE, U=YELLOW** (from wiring figure umd-006).
4. **Component-level precision** confirmed from clean tables: Pmax typical **240 W** / max **800 W**; current-sense chain `Vsense = 3 mΩ × 50 V/V = 150 mV/A`.

## Pass-by-pass results

### Pass 1 — Content / tables
- **Paragraphs/sections:** full document captured (~306 content lines, 12 pp). Sections: intro, Features, Specifications, Quick Start (2 wiring scenarios + warnings), Feature Descriptions §1–9, Specifications table, Absolute Maximum Ratings, two Pin-Definition tables, Hall Sensor Header pin table, Module Dimensions, Revision History.
- **Tables recovered (clean):** 7 — upper header pinout, lower header pinout, Specifications, Absolute Maximum Ratings, Pin-Definitions 15–8, Pin-Definitions 7–0, Hall Sensor Header.
- **Text layer:** clean (not ciphered) — `pdftotext -f1 -l1` sample readable; OCR not required for body text.

### Pass 2 — Code
- **Code examples: 0 extracted / 0 validated / 0 failed.** This is a hardware product guide; it contains **no Spin2/PASM2 listings** (verified by grep for `PUB|PRI|DAT|CON|VAR|OBJ|wrpin|wxpin|repeat|org`). The doc only *refers the reader* to the Smart Pins documentation for PWM/ADC/input programming. Nothing to compile.

### Pass 3 — Images
- **Extracted:** 13 raster images via `pdfimages`. **Deduped:** 6 identical 225×225 warning icons → 1 representative (5 removed). **Net unique: 8.**
- **Quality-passed:** 8/8 (no black/full-page failures; dominant-color gate healthy).
- **OCR'd:** umd-007 (callouts 1–9, corroborates Feature Descriptions), umd-012 (board-label drawing, noisy — layout figure not a text source).
- 12 full-page renders retained under `page-renders/` for layout context.

### Pass 5 — Completeness validation
| Check | Result |
|-------|--------|
| All 12 pages represented | ✅ |
| Both header pinouts captured | ✅ (clean tables) |
| Electrical spec table complete | ✅ Symbol/Qty/Min/Typ/Max/Units |
| Sensing formulas captured | ✅ current (150 mV/A) + voltage (13.1:1 ±5%) |
| Figures cataloged | ✅ 8 unique |
| Revision history captured | ✅ v2.0/RevB, v1.1, v1.0 |

**Completeness estimate: ~98%** (up from prior ~85%). The only residual is precise numeric mechanical dimensions inside the umd-012 drawing (PCB outline size IS in prose: 2.75×2.75 in / 70×70 mm; finer pad/hole geometry would need the schematic/mechanical download referenced by the doc).

## OCR-risk / extraction-defect flags
- **F-CANDIDATE (docling table copy-error):** In the recovered "Pin Definitions … Block 15-8" table, the rows for **pin 9 and pin 8** are mislabeled `PWM_XH` / `PWM_XL`; the authoritative **header pinout table** (and the prior baseline) give **pin 9 = PWM_UH, pin 8 = PWM_UL**. Docling duplicated the X-channel label across the table break. **Use the header pinout values (U channel on 9/8).** Not a source error — an extraction artifact; flagged so downstream never adopts the wrong label.
- **Minor OCR noise:** stray `- ●` bullet in Specifications list; `0.1'`/`0.1"` quote substitution; `BDLC` appears in source for BLDC (source typo, preserved). None fact-bearing.
- **umd-012** numeric dimensions NOT recovered by OCR (drawing, not text) — flagged as a gap if mechanical CAD values are ever needed.

## Trust
Authoritative tier proposed: **🏆 Parallax primary (vendor product guide)** — unchanged from prior. This is the manufacturer's own RevB v2.0 guide; it is the ground-truth board spec for #64010.
