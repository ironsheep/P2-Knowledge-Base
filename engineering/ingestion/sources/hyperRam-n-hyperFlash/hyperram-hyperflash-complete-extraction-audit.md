# HyperRAM/HyperFlash Add-on (#64004-ES) — Complete Extraction Audit

**Source:** `64004-ES P2-ES Eval HyperRAM_Flash Memory Board Product Guide.pdf` (9 pp) + `…-SCHEMATIC-OS.pdf` (3 sheets, cross-check)
**Ingested:** 2026-06-22 · **Skill:** `ingest-source` (7-pass) · **Auth tier:** 🏆 (Parallax primary product doc)
**Edition:** Product Guide v1.0 · board Rev A (2019). Greenfield (no prior edition).
**Notable:** first PDF-only source through the new **PDF-only ladder**; certified a refinement (corrupt text layer → forced OCR).

## Pass-by-pass

| # | Pass | Result |
|---|------|--------|
| 1 | **Content** | ✅ **Forced OCR** (`docling --force-ocr`, RapidOCR). The PDF's embedded text layer is **corrupt** (ciphered ToUnicode CMap — e.g. "BXV WUanVacWionV"=="Bus transactions", "FHDWXUHV"=="FEATURES") on part of the doc; both `pdftotext` and default `pdf2md` returned garbled text. Forced OCR reads rendered pixels and produced clean content. Output: `complete-hyperram-hyperflash-reference.md` + `hyperram-hyperflash-text.txt`. |
| 2 | **Code examples** | ✅ **None in source** (0 examples). The guide directs users to the Parallax product/developer page for code. `pnut_ts` N/A. `assets/code-2026-06-22/` empty. |
| 3 | **Images** | ✅ 7 raster images via `pdfimages` + `image-tools-mcp` quality gate (all PASS). 1 fact-bearing (img-006 mechanical/pad-layout drawing); 2 header banners; 4 product photos. Catalog: `assets/images-hyperram-hyperflash-2026-06-22/image-catalog.md`. |
| 4 | **Post-processing** | ✅ Pin-map matrix folded into the reference (triple-validated, see pass 6). |
| 5 | **Validation** | ✅ Completeness below. All sections of the 9-page guide captured: Overview, Features, Specifications, Quick Start, Feature Descriptions §1–§9, Optional Configuration Pad Functions table, Pin Definitions & Ratings table, Resources & Downloads, Module Dimensions, Revision History. |
| 6 | **Cross-source Q&A + conflicts** | ✅ See below. |
| 7 | **Registration** | ✅ Dashboard row updated; `AUTHORITATIVE-SOURCES` tier set; `DOCUMENT-LINEAGE` recorded; F-122 handed to YAML head; G-009 logged. |

## Pass-6 — cross-source Q&A + conflicts
- **Coverage gap CLOSED (data side):** prior open finding **F-122** — "64004-ES has no standalone YAML." The verified
  extraction now exists. **Routed to the YAML head** (F-122 updated) to author `hardware/addon-hyperram-hyperflash.yaml`.
- **No conflicts.** The only prior published reference is a bare name in `hardware/p2-eval-board.yaml:145`
  (`individual_addons` list) — no facts to contradict. This ingestion *adds* coverage; it corrects nothing.
- **Pin map triple-validated** (the board YAML's crown jewel): the Pin Definitions table agrees across
  (a) the ciphered text-layer extraction (decoded), (b) the forced-OCR extraction, and (c) the mechanical
  pad-layout drawing (img-006, pads 0–15 + power/GND + config pads). High confidence.
- **New gap raised → G-009:** datasheet part numbers + URLs are OCR-transcribed (transcription risk); flagged
  `[VERIFY]` in the reference; must be confirmed against ISSI datasheets / the product page before publishing.
- **Compatibility nuance:** board is "designed specifically for" the **#64000-ES** limited-edition Eval Board —
  the YAML should state ES-board targeting, not generic eval-board compatibility.

## Completeness: **95%**  — gates
- **C** ✅ content (forced-OCR; clean) · **K** — n/a (no code) · **I** ✅ images (7, cataloged; per-photo callout OCR = low-value debt)
  · **A** ✅ audit (this doc) · **X** ✅ cross-source (vs p2-eval-board.yaml; pin map triple-validated)
- **Why not 100%:** G-009 part-number/URL strings unverified (OCR), and per-product-photo callout OCR deferred as
  low-value debt. Neither blocks the YAML authoring; both are tracked.

## Methodology learning (process fix shipped same pass — skill §8)
A **corrupt/ciphered text layer is functionally a scanned page** — the "skip OCR unless scanned" rule must treat
it that way. Detection: `pdftotext -f 1 -l 1` sample looks garbled (dropped/substituted glyphs). Fix:
`docling --force-ocr`. This refinement was folded into the `ingest-source` skill's PDF-only ladder this session.
