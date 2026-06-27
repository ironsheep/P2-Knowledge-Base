# Image Catalog — P2 WX Adapter Guide (#64007) v1.0

**Extracted**: 2026-06-27 via `pdfimages -all` (11 embedded JPEGs, all RGB/8bpc).
**Quality gate**: every image passed — dominant color is the light page background
(`#F0F0F0`), none are `#000000`-dominant (no black/failed captures); all 11 md5-unique
(no duplicates, no full-page mis-captures). Filenames encode `page-objnum`.
**OCR note**: board photos and the pin diagram OCR noisily (rotated silkscreen, photographic
text); authoritative labels come from the document text layer (clean), so OCR is used only to
confirm a figure's content class, not as a fact source. Web-screenshot text is legible in-figure.

| File | Page | Dim (px) | Type | Purpose / content | Consumer |
|---|---|---|---|---|---|
| wxadapter-001-000.jpg | 1 | 904×152 | banner | Parallax header/contact banner (logo strip) | decorative |
| wxadapter-001-001.jpg | 1 | 1000×1000 | product photo | WX Adapter board, top view (dark-blue PCB traces) | hardware ID |
| wxadapter-001-002.jpg | 1 | 1000×1000 | product photo | WX Adapter board, alternate view | hardware ID |
| wxadapter-002-003.jpg | 2 | 1000×1000 | assembly photo | WX WiFi module seated on adapter (Connecting the Hardware) | assembly guide |
| wxadapter-002-004.jpg | 2 | 267×214 | detail photo | RES-logo header / metal-can orientation marking detail | assembly guide |
| wxadapter-002-005.jpg | 2 | 219×361 | detail photo | Adapter plugged into 2×6 RES header (portrait) | assembly guide |
| wxadapter-003-006.jpg | 3 | 1158×581 | web screenshot | Parallax Wireless Module webpage — Firmware menu / .ota upload | firmware workflow |
| wxadapter-004-007.jpg | 4 | 1175×921 | web screenshot | Settings menu — reset dropdown set to "CTS"; SAVE / SAVE to FLASH | firmware workflow |
| wxadapter-005-008.jpg | 5 | 1214×622 | web screenshot | P2 Drop Loader drag/drop area ("Done!" on success) | programming workflow |
| wxadapter-006-009.jpg | 6 | 1093×913 | pin diagram | Pin-connection diagram — top dark-blue / bottom light-blue PCB traces | **pin map (high-value)** |
| wxadapter-007-010.jpg | 7 | 1600×1541 | mechanical drawing | Dimensions + 8-pin SIP control-signal pad silkscreen (PGM DBG ASC CTS RTS DO DI RES) | mechanical / probe ref |

## Prior-vs-now (image debt)

Prior 2025-08-29 capture logged **"8+ images" as unresolved technical debt** (none extracted).
This re-extraction clears it in full: **11 figures extracted, 11 quality-passed, 0 black/failed**,
each cataloged with purpose + consumer. Debt → **0**.
