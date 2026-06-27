# Image Catalog — P2 HD Audio Add-on Set (#64014)

**Source PDF:** `64014-P2-HD-Audio-Add-on-Set-Guide.pdf` (primary board guide)
**Extraction:** `pdfimages -png` (PyMuPDF/poppler raster path — PDF-only source) · 2026-06-27
**Quality gate:** `image-tools-mcp` `image_dominant_colors` (health) + `image_ocr_full` (labels). All images healthy (no black/full-page-mis-capture failures; dominant colors are light grays + dark-blue PCB silkscreen, never `#000000`-dominant).
**Extracted:** 7 raster images · **6 unique** (board-001 == board-003, identical md5 `a18aa6f…`).

| File | Page | Dims (px) | Content | Quality | OCR notes |
|---|---|---|---|---|---|
| board-000.png | 1 | 904×152 | Parallax company logo (header banner) | OK | (logo, not OCR'd) |
| board-001.png | 1 | 1854×1124 | Product photo — board(s) on white | OK | healthy |
| board-002.png | 1 | 1981×1402 | Product photo — board(s) on white (cover, both boards) | OK (#F0F0F0 + #000050 silkscreen) | healthy |
| board-003.png | 2 | 1854×1124 | **Duplicate of board-001** (same image reused on p.2) | OK | dedupe note |
| board-004.png | 3 | 1925×1251 | **ADC board photo** with silkscreen labels | OK | OCR confirms silkscreen: "ADC", "VIO3V3", "WINTN", "GND", "GND", "HD Audio", "32b 5s", "C1" — matches ADC pin table. OCR noisy (silkscreen on PCB) but pin-label legible. |
| board-005.png | 4 | 2022×1845 | **Mechanical dimension drawing** (ADC, largest image) | OK (53% white bg) | OCR = rotated-dimension noise (low confidence) → **OCR-risk flag**: dimension callouts not machine-readable; visually a mechanical drawing matching "1.6 x 1 in / 40.64 x 25.4 mm, 3.2 mm hole" spec. |
| board-006.png | 6 | 1951×1256 | **DAC board photo / dimension** (DAC page) | OK (#F0F0F0 + #000040 silkscreen) | healthy; DAC board image |

## Notes / image-enhancement debt
- **board-005** dimension drawing: dimension-line text is rotated and does not OCR cleanly. The numeric dimensions are corroborated by the board guide's Key Specifications ("1.6 x 1 in (40.64 x 25.4 mm)", "3.2 mm mounting hole"), so no fact is lost — flagged only as an OCR-risk on the drawing itself.
- **board-001 / board-003** are byte-identical; consumers should reference one (board-001). Kept both for page-fidelity of the extraction.
- Page numbers are from `pdfimages -list` object→page mapping; a large drawing on the ADC "Board Dimensions" section spans the page boundary (heading p.3, drawing rendered p.4).
- No bit-field / register diagrams in the board guide (those live in the AK5704 datasheet, not extracted as images — cross-check tier).
