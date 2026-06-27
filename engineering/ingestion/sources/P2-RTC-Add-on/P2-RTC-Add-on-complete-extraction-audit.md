# Extraction Audit — P2 RTC Add-on (#64013)

**Source:** `64013-P2-RTC-Add-on-Guide-20221129.pdf` — Parallax Inc., v1.0, 11/29/2022, **3 pages**
**Mode:** new (greenfield) · **Passes run:** 1–5 (STAGE-ONLY; no pass 6/7, no canonical writes, no ID allocation)
**Date:** 2026-06-27 · **Agent:** addon-wave-2026-06 MAP

## Pass 1 — Content
- Text layer: **clean** (`pdftotext -f 1 -l 1` sample readable — NOT ciphered; no forced OCR needed).
- Extraction tools: `pdftotext -layout` (body) + `pdf2md`/docling (cross-check) + `camelot lattice` (pin table).
- Sections captured (3/3 pages, 100%): Description · Features (8 bullets) · Key Specifications (10 items) · **Pin Connections table** · Code Tip · Board Dimensions (figure) · Resources/Downloads · Lithium Battery notice · Revision History.
- Paragraphs/blocks: ~16 prose blocks + 2 bulleted lists + 1 spec list. **Tables: 1** (Pin Connections — recovered via lattice, ambiguity resolved).
- **No section dropped.** Only deferred-out content is the PCF8523 register/API detail, which the guide itself defers to the NXP datasheet (out of document by design).

## Pass 2 — Code examples
- **0 code blocks in document.** No Spin2/PASM2 listing ships in the PDF (example code is referenced on the product page only).
- extracted 0 / validated 0 / failed 0. `pnut_ts` not invoked (nothing to compile).

## Pass 3 — Images / visual catalog
- Extracted **4** images (`pdfimages -all`): 1 header banner, 2 board photos, 1 dimension drawing.
- Quality gate (`image_dominant_colors`): **4/4 PASS** (light backgrounds dominant; zero black/failed captures).
- OCR'd **1** (dimension drawing) → silkscreen `SCL+0 / SDA+1 / VIO3V3 / GND` — corroborates pin map.
- Catalog: `assets/images-P2-RTC-Add-on-2026-06-27/image-catalog.md`.

## Pass 4 — Post-processing
- Pin-connections table normalized to CSV (`assets/p2-rtc-pin-connections-table.csv`) and to a clean markdown table in the reference.
- Cross-signal corroboration recorded: lattice table ↔ silkscreen OCR agree on SCL=+0, SDA=+1.

## Pass 5 — Validation (completeness)
- **Structural completeness: 100%** of the 3-page document captured (all sections, the one table, all 4 figures).
- **Knowledge completeness (board-level): HIGH.** Board identity, chip identity, electrical/mechanical specs, pin map, shared-pin discipline, battery, transport — all captured with source citations.
- **Knowledge completeness (RTC programming): LOW by design** — I2C address, register map, alarm/timer/offset register detail are not in this guide (datasheet-deferred). This is a property of the source, not an extraction loss. See gaps.

## Self-check vs Sacred Rules
- Wrote ONLY under staging. Canonical `sources/P2-RTC-Add-on/` left with the PDF only (the stray `pdf2md` output produced in-place was moved out to scratch).
- No F-/G-/Q- IDs allocated; all findings below are PROPOSALS for the reduce step.
- No `deliverables/ai/P2/` YAML touched.
