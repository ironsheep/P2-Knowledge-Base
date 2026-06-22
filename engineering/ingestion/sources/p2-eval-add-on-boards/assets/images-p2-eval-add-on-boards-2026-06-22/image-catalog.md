# P2 Eval Add-on Boards (#64006) — Image Catalog

**Source:** `64006-P2-Eval-Add-on-Boards-Product-Guide.pdf` (v2.0, 2025 edition — clean Skia export)
**Extracted:** 2026-06-22 · **Method:** `pdfimages -png` + `image-tools-mcp` quality gate · all healthy JPEGs (no black/mis-captures)
**Count:** 17 figures (img-000..017; **img-001 is the alpha mask of the img-000 banner**, not a separate figure)

> Board photos carry **silk labels + pin numbers**, so several **corroborate the pin maps** (a 4th signal
> beside 2025 text ∩ 2020 OCR ∩ the document tables). The PCB-dimension drawings are fact-bearing (sizes/pad layout).

| File | Page | WxH | Board / purpose | Value |
|------|------|-----|-----------------|-------|
| img-000 (+001 smask) | 1 | 1600×276 | Parallax page-header banner | boilerplate |
| img-002 | 1 | 397×394 | **Hero shot** — all 8 boards plugged into the P2 EVAL board | illustrative |
| img-003 | 2 | 823×408 | **Control (A)** — secondary photo | illustrative |
| img-004 | 2 | 1535×767 | **Control (A)** — labeled photo (buttons 4–7, LEDs 0–3, silk "CONTROL") | **corroborates pin map** |
| img-005 | 3 | 990×463 | **Serial Host (B)** — twin USB-A photo | illustrative |
| img-006 | 4 | 920×458 | **LED Matrix (C)** — 8×7 Charlieplex grid photo | illustrative |
| img-007 | 5 | 1000×1000 | **Digital Video Out (D)** — HDMI-type board photo | illustrative |
| img-008 | 6 | 920×459 | **Mini Prototyping (E)** — top-side grid photo | illustrative |
| img-009 | 6 | 950×471 | **Mini Prototyping (E)** — bottom-side (ground strip) photo | illustrative |
| img-010 | 7 | 945×463 | **Serial Device (F)** — twin microUSB photo | illustrative |
| img-011 | 8 | 1000×1000 | **Goertzel (G)** — Rev B touch-pad board photo | illustrative |
| img-012 | 9 | 1320×490 | **A/V Breakout (H)** — board photo | illustrative |
| img-013 | 10 | 884×190 | **A/V (H)** — microphone socket wiring diagram (Tip=signal, Sleeve=gnd) | fact-bearing |
| img-014 | 10 | 884×190 | **A/V (H)** — headphone socket wiring diagram (Tip=L, Ring=R, Sleeve=gnd) | fact-bearing |
| img-015 | 11 | 1600×841 | **PCB dimensions — A/V module** (large): 3.2×1.3 in + pad layout | **fact-bearing** |
| img-016 | 11 | 1600×851 | **PCB dimensions — Goertzel module** (medium) | **fact-bearing** |
| img-017 | 12 | 1173×695 | **PCB dimensions — small modules** (the other six boards) | **fact-bearing** |

## Notes
- 2025 (clean) edition used for image extraction; the 2020 `#64006-ES` edition's images are equivalent
  (older Goertzel shows probe-posts rather than touch-pads — see the Goertzel board doc). Not separately extracted.
- Each per-board doc (`../../boards/addon-*.md`) references its image(s) by file name above.
