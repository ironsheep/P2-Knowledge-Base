# Image Catalog — P2 RTC Add-on (#64013)

Extracted with `pdfimages -all`; quality-gated with `image-tools-mcp`
(`image_dimensions` + `image_dominant_colors`). All 4 images PASS the quality
gate (light ~#F0F0F0 backgrounds dominant; none are black/failed captures). One
figure OCR'd for silkscreen labels.

| File | Src page | Dimensions | Type / content | Quality | OCR | Consumer use |
|---|---|---|---|---|---|---|
| `p2-rtc-page1-header-banner.png` | 1 | 904×152 | Parallax contact-info header banner | PASS (#F0F0F0 bg, teal text) | n/a | boilerplate; not a technical figure |
| `p2-rtc-board-photo-1.jpg` | 1 | 1000×1000 | Product photo of the RTC board (Parallax-blue PCB) | PASS | n/a | marketing / board-ID figure |
| `p2-rtc-board-photo-2.jpg` | 1 | 1000×1000 | Product photo, second angle | PASS | n/a | marketing / board-ID figure |
| `p2-rtc-board-dimensions.png` | 3 | 2011×1709 | Mechanical dimension drawing + silkscreen pin labels | PASS (navy lines, gold dims, red callout on white) | yes | **pin map + mechanical** corroboration |

## OCR — `p2-rtc-board-dimensions.png` (silkscreen / callouts)

High-confidence tokens (RapidOCR): `REAL TIME CLOCK AND CALENDAR`, `SCL+0`,
`SDA+1`, `GND`, `VIO3V3` (read as "VI03v3", low conf — the literal silkscreen is
**VIO3V3**). **This independently confirms the pin map**: SCL on Accessory pin
**+0**, SDA on pin **+1** — agreeing with the `camelot lattice` pin-connections
table. Numeric dimension callouts are present on the drawing but the precise
values are authoritative in the text Key-Specs (PCB 20.32 × 25.4 mm; mounting
hole 3.2 mm) — drawing used as corroboration, not the primary number source.

## Image-enhancement debt
None required. The dimensions drawing is high-resolution and legible; no
crop/vectorize/transparency-unbake needed for catalog use.
