# Image Catalog — Universal Motor Driver P2 Add-on Board (#64010, RevB v2.0)

**Extraction date:** 2026-06-27
**Source PDF:** `64010-UniversalMotorDriverP2AddOnGuide-RevB-v2.0.pdf` (12 pp, 4.0 MB)
**Tooling:** `pdfimages -png` (raster extract) + `image-tools-mcp` (quality gate + OCR) + `pdftoppm` page renders.
**Prior baseline had ZERO images** — this is the first visual catalog for this source.

## Quality gate
All meaningful figures pass the gate (no `#000000`-dominant failures; discrete figures, not full-page mis-captures).
- `umd-001` board photo: dominant `#101050` (Parallax navy) 37% — healthy.
- `umd-005` wiring diagram: dominant `#F0F0F0` 70% — healthy line art.

## Catalog (8 unique images; 6 duplicate warning icons collapsed to 1)

| ID | Page | Dimensions | Type | Purpose / Content | Consumer |
|----|------|-----------|------|-------------------|----------|
| umd-000 | 1 | 904×152 | Decorative | Parallax contact-info banner strip (web/sales/support) | none |
| umd-001 | 1 | 1282×1215 | **Product photo** | Hero photo of the #64010 board (top view, spring terminals, headers) | product page / manual cover candidate |
| umd-002 | 2,7 | 225×225 | Icon | WARNING triangle icon (⚠). **6 identical copies** in PDF (pp.2 ×3, p.7 ×3) — deduped to this one representative | inline warning callouts |
| umd-005 | 3 | 1000×1000 | **Wiring diagram** | Typical connections for Motor Mount & Wheel Kit (#28962): P2 Edge Mini Breakout + #64010 + fuse/VIN cabling | quick-start wiring |
| umd-006 | 4 | 1564×982 | **Wiring diagram** | Typical connections for 6.5″ Hub Motor w/ Encoder (#27860). Shows hall-sensor connector + **motor-lead color map: X=Not Connected, W=GREEN, V=BLUE, U=YELLOW**; hall connector RED/BLACK | quick-start wiring (BLDC) |
| umd-007 | 5 | 652×525 | **Annotated board** | Feature-description board photo with numbered callouts 1–9 (headers, 12V/5V supplies, MOSFET drivers, MOSFETs, VIN/motor connectors, hall header, current-sense, mounting holes) | Feature Descriptions §1–9 |
| umd-008 | 6 | 1000×1000 | Product photo | Board photo (front, RevA silk) used near the MOSFET-driver section | feature section |
| umd-012 | 12 | 1600×1447 | **Mechanical/layout** | Module dimensions + silkscreen/connector-label drawing (OUT-W/V/U, 5V U V W GND, VIO3V3, PARALLAX) — board layout reference | mechanical/dimensions |

## OCR notes
- `umd-007` numbered callouts (1–9) align 1:1 with the prose Feature Descriptions list — diagram corroborates prose.
- `umd-012` OCR is noisy (board render, not a clean line drawing): legible tokens `ADD-ON`, `OUT-W`, `OUT-U`, `VIO3V3`, `5V U V W GND`, `PARALLAX`. Treat measurement values as not-OCR-recovered; the figure is a layout/dimensions illustration (numeric dimensions live in the Specifications prose: PCB 2.75×2.75 in / 70×70 mm).

## Image-enhancement debt
- None blocking. `umd-012` could be re-rendered from a vector source if precise mechanical dimensions are ever needed as text (currently only the PCB outline size is given in prose).
