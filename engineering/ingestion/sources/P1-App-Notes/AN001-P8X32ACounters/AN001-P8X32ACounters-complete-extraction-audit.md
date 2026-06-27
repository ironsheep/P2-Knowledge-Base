# AN001 P8X32A Counters v2.0 — Extraction Audit (Pass 5)

**Source:** Parallax App Note AN001 *Propeller P8X32A Counters* v2.0 — Propeller 1 (P8X32A), 19 pp.
**Mode:** new (greenfield). **Passes run here:** 1–5 (STAGE-ONLY). Passes 6 (cross-source) + 7 (registration) belong to the wave reduce.
**Auth tier (proposed):** 🏆 Parallax official application note (primary documentary source for P1 counter hardware).

## Tooling ladder used (PDF-only source)
- Text-layer probe `pdftotext -f 1 -l 1` → **clean** (no cipher; header has cosmetic letter-spacing only). No OCR forced.
- Pass 1 content/tables: `pdftotext -layout` (raw, complete 945-line extract) + `camelot lattice` (7 ruled tables → cross-check CSVs) + `pdf2md` (docling, full-doc, ran to completion — used as a secondary signal; the layout extract is authoritative).
- Pass 2 code: companion `.spin` archive **captured verbatim**; **NOT compiled** (no P1 compiler — see below).
- Pass 3 images: `pdfimages -png` (4 raster scope captures) + `image-tools-mcp` quality gate. Vector figures logged as image-debt.

## Pass 1 — Content (COMPLETE)
- **Paragraphs:** all body prose captured across the 11 sections (Intro → Resources/Revision/Disclaimer). Curated, voice-preserving rendering in `complete-AN001-reference.md`.
- **Tables:** **7 of 7** captured and rendered:
  - Table 1 — CTRA/CTRB bit-field layout (bits 31 / 30..26 CTRMODE / 25..23 PLLDIV / 22..15 / 14..9 BPIN / 8..6 / 5..0 APIN).
  - Table 2 — all **32** CTRMODE values (description, accumulate condition, APIN/BPIN output). Footnote notation A¹/A²/B¹ preserved.
  - Table 3 — mode-group → application examples.
  - Table 4 — NCO state progression (FRQA=$8000_0000).
  - Table 5 — PLLDIV field (8 taps, VCO÷128…÷1).
  - Table 6 — Logic mode accumulate equations (14 rows).
  - Table 7 — Pin-state equations (8 rows, accumulate + feedback).
- **Equations:** Equation 1 (NCO frequency `f = FRQA/2³² × Fsys`) and Equation 2 (DAC `V = 3.3 × FRQA/2³²`) captured as inline math (PDF rendered them as layout-art; text reconstructed from context).
- **Front/back matter:** abstract, resources, revision history (v2.0 delta from v1.0), disclaimer, © 2011 captured.

## Pass 2 — Code examples (CAPTURED + CATALOGED, NOT VALIDATED)
- **5 companion `.spin` files** copied verbatim into `assets/code-2026-06-27/` + `code-catalog.md`.
- **`code_validated: false`** — `pnut_ts` is a **P2** compiler and does not build P1 Spin1/PASM1; the P1 validator (flexspin) is not installed. P1 charter §3: P1 code is **documentary-extracted, not compiled**. No edits/normalization.
- 2 files (`ADC.spin`, `ScalingDuty(DAC).spin`) are UTF-16 (extended chars Ω/μ) — copied byte-for-byte.
- In-PDF teaching listings (NCO inline, PWM, Duty/DAC, ADC, FreqCount) also transcribed into the curated reference; minor naming differences vs companion files noted in `code-catalog.md`.
- External library deps **referenced, not in archive**: `VGA_Text.spin` (used by 2 examples), `CTR.spin` (mentioned in Resources). Both ship with Propeller Tool — logged, not fetched (gap candidate).

## Pass 3 — Images (4 extracted / 4 quality-PASSED / 0 useful OCR / 10 image-debt)
- 4 raster scope captures (Figs 3,4,6,11) extracted, renamed meaningfully, quality-gated PASS (dominant `#F0F0F0` ≈93–97%, not black; blue/red traces corroborate prose; Fig4 differential shows the red BPIN trace). OCR returns no meaningful text (waveform photos) — expected, no evidence harvested.
- **10 vector figures** (Figs 1,2,5,7,8,9,10,12,13,14 — block diagrams, the FRQA-vs-output plot, the Σ∆-ADC schematic) are PDF vector content; `pdfimages` does not recover them → **image-debt (page-render+crop)**. Their content IS captured in prose/ASCII in the curated reference. Cataloged in `image-catalog.md`.

## Pass 4 — Post-processing (within-source)
- Mode taxonomy normalized into one 32-row matrix + an application cross-walk (Table 3) + a P1→P2 smart-pin mapping (see HANDBACK cross-corpus note). Equivalences captured (`%01000`≡`%11010`; `%01100`≡`%10101`; `%10000`≡`%00000`). No cross-SOURCE matrices built here (reduce/pass-6 owns those).

## Pass 5 — Completeness verdict
- **Content completeness: ~95%.** All sections, all 7 tables, all 32 modes, both equations, all 5 code examples, and the 4 photographic figures fully captured. The 5% shortfall is entirely **vector-figure raster debt** (10 block diagrams not yet cropped) — content-equivalent prose is captured, so no information is lost, only the rendered images.
- **Gates:** content ✅ · code ✅ captured (validation N/A on P1) · images ⚠️ raster-debt open (vector figures) · cross-source (pass 6) and registration (pass 7) **deferred to reduce**.
- No corrupt-text-layer issues; no OCR risk strings.

## Proposed dashboard cells (reduce to confirm)
- **C** (Content) ✅ ~95% · **K** (Code) ⚠️ captured-not-validated (P1, no compiler) · **I** (Images) ⚠️ 4/14 raster, 10 vector-debt · **A** (Audit) ✅ pass-5 done · **X** (cross-source) ⏳ pass-6 reduce.
