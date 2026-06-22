# P2 Eval Add-on Boards (#64006 Series) — Overview & Index

**Authoritative edition:** `64006-P2-Eval-Add-on-Boards-Product-Guide.pdf` — **v2.0, 1/12/2021** (Skia/PDF, clean text layer; pdf2md / pdftotext-layout).
**Cross-check edition:** `64006-ES P2-ES Eval Board Accessory Set Guide-OLD.pdf` — 2020 limited-edition **#64006-ES** set (Quartz export, **corrupt text layer → forced OCR**).
**Re-ingested:** 2026-06-22 (cross-edition redo; **supersedes the fabricated Aug-2025 extraction** — see audit & F-121).

> **⚠️ Why this redo exists.** The prior (Aug-2025) extraction **fabricated all eight board names**
> (LED Array / Switch Array / Potentiometer / Servo Header / Sensor / Prototyping / Digital I/O /
> Analog I/O) — none appear in the actual document. The real lineup is below, verified against the PDF.
> The fabrications leaked into published YAML → routed to the YAML head as **F-121**.

## The eight boards (#64006A–H) + the set
Each board has its **own source document** in `boards/` (per-board pin map + specs + cross-edition notes):

| # | Board | Part | Source doc |
|---|-------|------|-----------|
| A | **Control** — 4 push-buttons + 4 blue LEDs | #64006A | `boards/addon-control-64006a.md` |
| B | **Serial Host** — twin USB-A host (current-limited) | #64006B | `boards/addon-serial-host-64006b.md` |
| C | **LED Matrix** — 8×7 Charlieplexed green LEDs (56) | #64006C | `boards/addon-led-matrix-64006c.md` |
| D | **Digital Video Out** — HDMI-type connector | #64006D | `boards/addon-digital-video-out-64006d.md` |
| E | **Mini Prototyping** — 8×12 plated thru-hole grid | #64006E | `boards/addon-mini-prototyping-64006e.md` |
| F | **Serial Device** — twin microUSB (P2 as USB device) | #64006F | `boards/addon-serial-device-64006f.md` |
| G | **Goertzel** — touch/position sense pads (Rev B) | #64006G | `boards/addon-goertzel-64006g.md` |
| H | **A/V Breakout** — audio + video (VGA/RCA/composite) | #64006H | `boards/addon-av-breakout-64006h.md` |
| — | **Complete Accessory Set** | #64006-ES | (the set SKU containing all eight) |

## Shared facts (all boards unless noted)
- **Connector:** each board has a **2×6 pass-through socket**, compatible with any P2 development board carrying a 2×6 accessory header.
- **Compatible systems:** P2 Eval Board (**#64000**); P2 Edge Module Breadboard (**#64020**) or P2 Edge Mini Breakout Board (**#64019**) with a P2 Edge Module (**#P2-EC**).
- **Pins:** each board uses the **8 I/O pins (0–7)** of one 2×6 header block (relative offsets).
- **Power:** strongly recommended to connect the auxiliary supply to the P2-EVAL **P2-USB** socket — accessory current may exceed PC-USB.
- **Mounting hole** (all **except Mini Prototyping**): connected to GND, suits M3 (UNC 4-40); hole 3.2 mm (126 mil), pad ring 5 mm (200 mil); fits a 9.5 mm standoff as a leg.
- **PCB sizes:** three (A/V module = large; Goertzel = medium; the rest = small). Two small, or one large + one small, fit side-by-side per P2-EVAL edge.

## Edition history (from the v2.0 Revision History)
- **v1.0** — original release as the **#64006-ES** limited-edition *set* (2020 Google Doc, commenting-enabled).
- **v1.1** — added the P2-ES Eval Board **Rev B** note (connect ACC HDR/5V pins with a shunt jumper to supply 5V to the I/O Pin Breakout Edge Headers — needed by the Serial boards).
- **v2.0** (1/12/2021) — **Goertzel PCB revised: touch switch pads replace the probe posts**; boards now available **individually** as well as the set.

## Cross-edition reconciliation (F-121)
The 2020 **#64006-ES** is the *set-only* edition; the 2025 **#64006** sells the same eight boards individually (+ the set SKU). The per-board part numbers (A–H) and pin maps are the agent-relevant facts; the bundle SKU is not. Per-board deltas (e.g. Goertzel probe-posts→touch-pads) are noted in each board's doc. _[2020 forced-OCR cross-check folded in per board.]_

## Provenance
Copyright © Parallax Inc. · "P2 Eval Add-on Boards (#64006 Series)" · v2.0 1/12/2021 · 12 pp.
2020 edition: "64006-ES P2-ES Eval Board Accessory Set Guide" · 13 pp.
