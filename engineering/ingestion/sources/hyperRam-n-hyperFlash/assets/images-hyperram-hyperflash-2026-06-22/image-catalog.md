# HyperRAM/HyperFlash Add-on (#64004-ES) — Image Catalog

**Source:** `64004-ES P2-ES Eval HyperRAM_Flash Memory Board Product Guide.pdf` (9pp, Google-Docs export)
**Extracted:** 2026-06-22 · **Method:** `pdfimages -png` (raster) + `image-tools-mcp` quality gate
**Count:** 7 raster images (all quality-PASS — non-zero dims, healthy filesizes, no black/full-page mis-captures)

> **Why pdfimages, not DOCX-media:** this is a PDF-only source (no `.docx`). The text
> layer is corrupt (ciphered ToUnicode CMap), so pass-1 content used **forced OCR**
> (`docling --force-ocr`); images were pulled directly with `pdfimages`.

| File | WxH | Purpose / content | Fact-bearing? |
|------|-----|-------------------|---------------|
| img-000.png | 1600×276 | Parallax page-header banner (near-blank variant) | no — boilerplate |
| img-001.png | 1600×276 | Parallax page-header banner (logo + contact strip) | no — boilerplate |
| img-002.png | 893×760 | Product photo — assembled board / P2-ES Eval context (PARALLAX, "P2 EVAL", HyperFlash/HyperRAM silk) | illustrative |
| img-003.png | 408×744 | Board photo — tall view (edge / passthrough-header detail) | illustrative |
| img-004.png | 326×752 | Board photo — tall view (config-pad edge detail) | illustrative |
| img-005.png | 671×557 | Board top-view / configuration-area illustration | illustrative |
| **img-006.png** | 978×1336 | **Mechanical dimensions + pad-layout drawing** — FACT-BEARING | **yes (verified)** |

## img-006 — pad layout & dimensions (verified content)

The mechanical drawing **independently confirms the Pin Definitions table** (pass-6 cross-check):

- **Dual 2×6 passthrough headers (left side), pads numbered 0–15** in two blocks:
  upper block 8–15, lower block 0–7. Each header block has **VIO3V3** and **5V** pads
  at top and **GND / GND** at bottom.
- **Right-side configuration pads (top→bottom):** `RES` / `GND`; `INT`; `RSTO`;
  `CSx BR` / `CSx AF`; `FLS B RAM` (device-B memory-type shunt); the `+ R C`
  configuration-resistor pads (device B); `C R +` (device A); `FLS A RAM`
  (device-A memory-type shunt).
- **Mounting hole** bottom-center (plated, tied to GND).
- **Dimensions (drawn):** 1.0 in (25.4 mm) W × 1.9 in (48.3 mm) H; header span
  0.65 in (16.5 mm); 0.825 in (20.95 mm); mounting-hole offsets 0.325 in (8.25 mm)
  & 0.1 in (2.54 mm) — agree with the spec text ("PCB dimensions: 1.0 × 1.9 in").

## Enhancement debt
- img-003/004/005 are illustrative board photos; per-image callout OCR not performed
  (low value — all fact-bearing data is in the text + img-006). Queued as low-priority
  image-enhancement debt; not blocking.
