# Image Catalog — P2 microSD Add-on Board (#64009)

Extracted via `pdfimages -j` from `64009-P2-microSD-AddOn-Guide-v1.0.pdf` on 2026-06-27.
Quality gate: `image_dimensions` + `image_dominant_colors` (healthy = not #000000-dominant);
text-bearing figures OCR'd with `image_ocr_full`.

| File | Page | Dimensions | Dominant color | Quality | Purpose / OCR content |
|------|------|-----------|----------------|---------|------------------------|
| `microsd-001-000.jpg` | 1 | 1600x1227 | #101050 (Parallax blue PCB) | PASS | Product photo — board top with microSD socket and labeled SIP breakout pads. |
| `microsd-001-001.jpg` | 1 | 904x152 | (banner) | PASS | Page-1 header/banner graphic (Parallax branding strip). |
| `microsd-003-002.jpg` | 3 | 1281x1600 | — | PASS | Mechanical dimension drawing (view A). SIP pad labels OCR clean: `GND CLK CS MOSI MISO DET 3V3`. Dimension numerals garbled (drawing leader lines) — overall dims taken from text Specs. |
| `microsd-003-003.jpg` | 3 | 1269x1600 | — | PASS | Mechanical dimension drawing (view B). SIP pad labels OCR clean: `GND CLK CS MOSI MISO DET 3V3`. Same garbled-numeral note. |

**OCR-risk flag:** dimension-line numerals on the page-3 drawings are NOT reliably OCR'd
(rotated/leader-line text). The authoritative PCB dimensions are the text-layer Specs
(0.8 x 1.05 in / 20.32 x 26.67 mm). Pad-label order is reliably confirmed by both drawings.

**Consumer references:** none yet (greenfield). Candidate consumer = a hardware/SD-boot
reference page (board pinout + SPI signal map).
