# Image Catalog — Parallax WX Wi-Fi Module (#32420) v1.0

**Source PDF:** `32420-Parallax-WX-WiFi-Module-Guide-v1.0.pdf` (12 pp)
**Extraction:** 2026-06-27, `pdfimages -png` (lossless from PDF objects)
**Quality gate:** `image-tools-mcp` `image_dimensions` + `image_dominant_colors`; `image_ocr_full` on text-bearing figures
**Re-extraction note:** prior baseline declared "12+ images expected" as **debt, never extracted**. This pass clears it: **15 content images extracted + cataloged** (plus 3 transparency soft-masks).

## Inventory

18 raster objects extracted. 15 are content images; 3 are transparency **soft-masks** (alpha
channels paired with the page-1/2 product photos — not standalone figures).

| File | Obj | Page | W×H | Dominant colors | Type / Purpose | Quality |
|---|---|---|---|---|---|---|
| wx-000.png | 0 | 1 | 230×40 | (JPEG logo) | Parallax company logo (header) | PASS |
| wx-001.png | 1 | 1 | 1000×1093 | #304070 blue PCB (#000000 = transparent bg via smask) | Product photo — **#32420S SIP** module (right) | PASS |
| wx-002.png | 2 | 1 | 1000×1093 | grayscale | **soft-mask** (alpha for wx-001) | — |
| wx-003.png | 3 | 1 | 1000×1170 | blue PCB (#000000 = transparent bg) | Product photo — **#32420D DIP** module (left) | PASS |
| wx-004.png | 4 | 1 | 1000×1170 | grayscale | **soft-mask** (alpha for wx-003) | — |
| wx-005.png | 5 | 2 | 1418×1000 | #F0F0F0 / #000040 | Application photo — robot/Boe-Bot controlled via Wi-Fi web page | PASS |
| wx-006.png | 6 | 2 | 1418×1000 | grayscale | **soft-mask** (alpha for wx-005) | — |
| wx-007.png | 7 | 3 | 422×393 | #F0F0F0 / #B0C0E0 | Application photo — Activity Board WX / wireless programming | PASS |
| wx-008.png | 8 | 4 | 900×895 | #F0F0F0 / #404040 | **Functional-description diagram** — numbered callouts 1–10 (ESP module, headers, regulator, LEDs, level shifters, SIP header) | PASS |
| wx-009.png | 9 | 6 | 288×211 | (small figure) | AP SSID / join-the-`wx-` network illustration | PASS |
| wx-010.png | 10 | 6 | 594×601 | UI screenshot | **Config home page** (http://192.168.4.1) — OCR: name `wx-dba23b`, "Remora", "v1.0 (2016-11-02 18:04:30)", "LINK by Thorsten von Eicken" | PASS (OCR'd) |
| wx-011.png | 11 | 7 | 596×614 | UI screenshot | **Networks page** — join network, STA+AP→STA, IP-address note | PASS |
| wx-012.png | 12 | 8 | 594×601 | UI screenshot | **Files page** — upload web pages/files | PASS |
| wx-013.png | 13 | 8 | 594×601 | UI screenshot | **Files page** (second view) | PASS |
| wx-014.png | 14 | 9 | 594×601 | UI screenshot | **Settings page** — module name + serial-comm settings | PASS |
| wx-015.png | 15 | 10 | 594×601 | UI screenshot | **Firmware page** — OTA `.ota` upload | PASS |
| wx-016.png | 16 | 10 | 985×766 | #F0F0F0 / #405070 | **Pin-map / pinout schematic** — OCR confirms 3.3V, /PGM, /RTS, ESP8266-WROOM-02, 32420, GND, pins 1–20 (noisy; see note) | PASS (OCR'd) |
| wx-017.png | 17 | 12 | 768×827 | #F0F0F0 / #000040 | **PCB mechanical drawing** — board dimensions | PASS |

## OCR evidence extracted

- **wx-010 (config home):** module name `wx-dba23b`; firmware **"Remora"**; **v1.0 (2016-11-02 18:04:30)**;
  **"LINK by Thorsten von Eicken"** → firmware lineage = open-source **esp-link**. (High-confidence OCR
  on the version/credit lines.)
- **wx-016 (pinout schematic):** labels 3.3V, /PGM, /RTS, IO16, ESP8266-WROOM-02, 32420, DBG, RES, GND,
  pin numbers 1–20. **Low confidence** on several schematic labels — the **pin table** in
  `complete-wx-wifi-reference.md` is the authoritative pin source; this figure is illustrative.

## Quality assessment

- All 15 content images extracted losslessly and passed the quality gate (discrete figures, not
  full-page mis-captures; no genuine `#000000`-dominant failed captures).
- The 3 page-1/2 product photos (wx-001/003/005) report `#000000` as a top color — this is the
  **transparent background** (each has a paired grayscale soft-mask, wx-002/004/006), NOT a failed
  black capture; the PCB-blue secondary color confirms healthy content. To composite for display,
  apply the smask (or `image_unbake_transparency`).

## Enhancement debt (deferred)

- None blocking. Optional: composite smasks onto white for clean display thumbnails; high-res
  re-OCR of UI screenshots (wx-011..015) if their exact field labels are later needed by a manual.
