# Extraction Audit — PE Kit Labs: Fundamentals v1.2 (#122-32305)

**Source:** Parallax #122-32305 *Propeller Education Kit Labs: Fundamentals* v1.2 (web release 2), Andy Lindsay
**Platform:** Propeller 1 (P8X32A) · Spin1/PASM1 · 40-Pin DIP PE Platform
**Ingestion mode:** `new` (single-source serial ingest; passes 1–5 by this agent; passes 6–7 + P1-quad registration by the head)
**Date:** 2026-06-27 · **Method:** PDF-only ladder (no DOCX available)
**Dashboard row:** `p1-pe-labs-fundamentals-v1.2`

---

## Pass-by-pass completeness

### Pass 1 — Content ✅ complete
- **Raw extract:** `122-32305-PE-Labs-Fundamentals-text.txt` — `pdftotext -layout`, **12,010 lines**, all
  **233 pages** (form-feed verified). Text layer is **clean** (no ToUnicode cipher — `pdftotext -f1 -l1`
  sampled readable; no OCR needed). A structured `docling`/`pdf2md` pass was also run as a cross-check
  (held as a scratch intermediate, not a canonical artifact).
- **Curated reference:** `complete-PE-Labs-Fundamentals-reference.md` — document map (all 7 chapters +
  5 appendices + index), platform/hardware facts, per-lab content summaries, P1-idiom→P2-reshape table,
  and the headline **Document Pattern Profile**.
- **Coverage:** TOC, preface, all chapters/labs, all appendices, all 15 tables identified, 115 figure
  captions located. Front/back-matter boilerplate captured. **No content gaps.**

### Pass 2 — Code ✅ captured + cataloged (NOT validated)
- **89 `.spin` files** copied **verbatim** into `assets/code-2026-06-27/`, **preserving the 5 per-lab
  subfolders** (Setup=2, I/O & Timing=21, Methods & Cogs=7, Objects=27, Counter Modules=32).
- `assets/code-2026-06-27/code-catalog.md` — organized **by lab**; each file → LOC, top-object vs
  library/driver role, what it demonstrates, lab teaching-point mapping; progressive-refinement lineages
  and `Test…`↔library pairings noted.
- **`code_validated: false`** — `pnut_ts` is P2-only and cannot build Spin1; no P1 compiler (flexspin)
  installed (P1 charter §3). Files are **captured + cataloged, not compiled.** No edits/normalization.
- **Encoding finding:** ~half the files are **UTF-16-LE (with BOM)** as authored by the Propeller Tool;
  left untouched. `.DS_Store` cruft stripped from the copy only.
- **External library objects referenced but not in the archive:** `Parallax Serial Terminal.spin`,
  `Float`/`FloatString` (Propeller Library, ship with the Propeller Tool; PST is printed in full in the
  book's Appendix A). Recorded as a knowledge note — not missing-file defects.

### Pass 3 — Images ✅ cataloged (all) + extracted (selective per policy)
- `assets/images-PE-Labs-Fundamentals-2026-06-27/image-catalog.md` — **complete inventory of all 115
  figures** (per-chapter tables) with TYPE + per-figure extract/skip decision + rationale; 139 total
  embedded raster images noted.
- **7 images extracted** (`pdfimages` + PyMuPDF/PIL; quality-gated with `image_dimensions` +
  `image_dominant_colors` — all healthy, varied palettes, none `#000000`-dominant):
  - 5 **breadboard/wiring-photos** (1-10a, 1-10b, 3-1, 3-2, 3-9) — the high-reuse class (reference for
    the P2 manual's new photo shoots).
  - 2 **representative terminal screenshots** (6-12 PST messages, 7-5 RC-decay output).
- **Catalog-only (not extracted) per policy:** ~22 schematics (redrawn in TikZ/circuitikz), ~24
  conceptual/architecture diagrams, ~18 IDE/code screenshots, ~7 counter-mode table images, remaining
  scope/terminal captures. Rationale recorded per figure.

### Pass 4 — Post-processing ✅
- Lab structure folded into the curated reference; P1→P2 idiom-reshape matrix built; the per-lab
  template, cross-lab arc, voice, media-usage, and example-naming patterns synthesized into the
  **Document Pattern Profile** (the downstream-purpose deliverable).

### Pass 5 — Validation ✅ (this document)
- Section-by-section completeness confirmed below. No truncation; all pages accounted for.

---

## Section-by-section completeness checklist
| Section | Pages | Text | Code mapped | Figures cataloged | Notes |
|---|---|---|---|---|---|
| Front matter + Preface | i–6 | ✅ | n/a | n/a | warranty/copyright/disclaimer/TOC/preface |
| Ch 1 Overview | 7–16 | ✅ | n/a | 1-1…1-11 ✅ | architecture + hardware tour |
| Ch 2 Software/Resources | 17–18 | ✅ | n/a | 2-1…2-3 ✅ | |
| Ch 3 Setup & Testing | 19–44 | ✅ | 2 files ✅ | 3-1…3-12 ✅ | 5 photos extracted from here/Ch1 |
| Ch 4 I/O & Timing | 45–68 | ✅ | 21 files ✅ | 4-1…4-3 ✅ | Study Time 28Q/14E/5P |
| Ch 5 Methods & Cogs | 69–82 | ✅ | 7 files ✅ | 5-1…5-6 ✅ | |
| Ch 6 Objects | 83–124 | ✅ | 27 files ✅ | 6-1…6-20 ✅ | PST terminal 6-12 extracted |
| Ch 7 Counter Modules | 125–190 | ✅ | 32 files ✅ | 7-1…7-31 ✅ | RC-decay 7-5 extracted |
| Appx A Object Listings | 191–200 | ✅ | (PST/SquareWave printed) | n/a | SquareWave also in code tree |
| Appx B Study Solutions | 201–223 | ✅ | n/a | n/a | answer key for all labs |
| Appx C Components | 224–225 | ✅ | n/a | tables | parts master |
| Appx D Block Diagram | 226 | ✅ | n/a | D ✅ | P8X32A reference |
| Appx E Regulator Calc | 227–228 | ✅ | n/a | n/a | LM2940CT-5.0 math |
| Index | 229–233 | ✅ | n/a | n/a | |

## Image extract-vs-catalog policy applied
Per the task brief: breadboard/wiring-photos EXTRACTED (cannot be regenerated; reference for new P2
photo shoots); schematics & conceptual diagrams CATALOG-ONLY (redrawn in TikZ/circuitikz);
terminal/scope screenshots cataloged with a few representative extractions; code screenshots
catalog-only (real `.spin` held). Result: 115 cataloged / 7 extracted.

## Trust / authority (proposed — head confirms in pass 7)
**🏆 Parallax official tutorial** (first-party, authored by Parallax engineer Andy Lindsay, ISBN'd,
copyright Parallax). Authoritative for P1 pedagogy, PE Kit hardware, and Spin1 teaching idioms. For
hard P1 silicon facts it is a tutorial (secondary) — defer to the P1 Datasheet / Propeller Manual where
they exist in the corpus.

## Known limitations
- **Code not compile-validated** (no P1 compiler) — `code_validated:false`.
- A few figure captions were merged into running prose by the PDF text layer (6-13, 7-12, 7-22, 7-26);
  figures exist and are counted; exact caption wording approximate.
- External Propeller-Library objects (PST, Float, FloatString) are referenced, not bundled.
