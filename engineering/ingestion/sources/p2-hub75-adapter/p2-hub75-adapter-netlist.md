# P2 Eval HUB75 Adapter (#64032, H/W Rev 1.4) — schematic netlist

**Source**: `hub75-adaptor-v1.4-schematic.pdf` — title block: **"HUB75E Adapter for P2 Eval"**,
Iron Sheep Productions, LLC, file `hub75-adaptor.sch`, Size A, **Date 2020-11-25, Rev H/W 1.4**,
Id 1/1, KiCad E.D.A. 5.1.7. One page, US Letter landscape (792 x 612 pt), 581,634 bytes,
md5 `f497ec00ca8bb923df886d76537c5c92`. PDF author field: Stephen M Moraco.

**Authority**: the board's designer and manufacturer. Stephen M Moraco (Iron Sheep Productions,
LLC) designed, built and sells this board through the Parallax store; his documents for it are a
golden source (Stephen, 2026-10-10; `AUTHORITATIVE-SOURCES.md`).

**Extraction date**: 2026-10-10
**Extraction path**: rendered-page visual read, with OCR as the second leg (below).

---

## Why not text extraction

The PDF has **no text layer at all**: `pdftotext` returns 1 byte and `pdffonts` lists **no fonts**.
KiCad's output was printed through macOS Quartz with every glyph drawn as a path. The page holds
two raster images (the HUB75 connector pin-label picture and a photo of the P2 Eval's accessory
header pair); everything else is vector art.

So the sheet was read twice, independently:

1. **OCR leg**: `image-tools-mcp image_ocr_full` on the page rendered at 400 dpi. Raw output in
   `p2-hub75-adapter-text.txt`. Schematic OCR is noisy (pin numbers merge with net names), so it
   corroborates labels and the title block and is never the reading of record.
2. **Visual leg (of record)**: the whole sheet at 200 dpi, then each region at 400 dpi. All the
   images are committed under `assets/images-p2-hub75-adapter-2026-10-10/`, so every row below
   can be checked against the archived image without re-rendering the PDF:

| Image | Shows |
|---|---|
| `schematic-page1-200dpi.png` | whole sheet |
| `crop-400dpi-hdr.png` | J1, J2 (P2 side headers) and the 3.3 V note |
| `crop-400dpi-u1.png` | U1 74HCT244, C1 |
| `crop-400dpi-u2.png` | U2 74HCT244, C2 |
| `crop-400dpi-conn.png` | J3 (LA probe header) and J7 (HUB75 connector) |
| `crop-400dpi-idc.png` | the DATA-IN connector picture and its annotation |
| `crop-400dpi-spare.png` | J4, J5, J6 through-holes |
| `embedded-p2-eval-header-photo.png` | raster: P2 Eval header pair with silkscreen I/O numbers |
| `embedded-hub75-data-in-connector.png` | raster: HUB75 DATA-IN connector pin labels |

Every value below was confirmed on both the 200 dpi sheet and the 400 dpi crop.

---

## Title block (verbatim)

```
Iron Sheep Productions, LLC
Sheet: /
File: hub75-adaptor.sch
Title: HUB75E Adapter for P2 Eval
Size: A    Date: 2020-11-25    Rev: H/W 1.4
KiCad E.D.A.  kicad (5.1.7-0-10_14)    Id: 1/1
```

## Notes printed on the sheet (verbatim)

- Box heading: **"P2 Eval Edge Expansion Socket (dual)"**
- **"3.3v pins (both connectors) are not connected."**
- **"Through Holes so can populate and connect unused pins if need be."**
- Beside the DATA-IN picture, at the pin labelled GND below G2: **"GND here is Really E"**
- Above J7: **"IDC 2x8 Shrouded Header, Keyed"**

## Components

| Ref | Value / part | Role |
|---|---|---|
| U1 | 74HCT244 | 8-bit buffer: the six colour signals and the two spare P2 pins |
| U2 | 74HCT244 | 8-bit buffer: OEb, CLK, LATCH and address A–E |
| C1, C2 | 0.1 uF | one decoupling capacitor per buffer, +5VA to GND |
| J1 | 2x6 header, "P2 Eval p8-15" | P2 side, upper I/O block (offsets 8–15) |
| J2 | 2x6 header, "P2 Eval p0-p7" | P2 side, lower I/O block (offsets 0–7); the board's only power input |
| J3 | 2x8 header, "LA Probe Header - HUB75 signals" | logic-analyser access to the buffered outputs |
| J4 | 3-pin through-hole, "Unused P2 Pins 14, 15" | the two spare pins, unbuffered |
| J5 | 3-pin through-hole, "Unused P2 Pins 14, 15 level shifted to 5v" | the two spare pins, buffered |
| J6 | 1-pin through-hole, "Unused HUB75 Pin" | the HUB75 connector's pin 4 |
| J7 | 2x8 shrouded keyed IDC, "2x8 Shrouded Header IDC" | the HUB75 panel connector |

## Power

- **+5VA** comes from **J2 pin 7** only (the P2 Eval header's 5V pin, per the photo). It feeds
  **U1 pin 20 and U2 pin 20 (VCC)** and C1/C2. Nothing else on the sheet uses +5VA.
- **J1 pin 7** (the upper header's 5V pin) is drawn **no-connect**.
- **J1 pin 1 and J2 pin 1** (the VIO3V3 pins) are drawn **no-connect**, matching the printed note.
- **GND**: J1 pins 6, 12; J2 pins 6, 12; U1/U2 pin 10; J3 pin 16; J7 pin 16; J4 pin 1; J5 pin 1.
- **J7, the panel connector, carries no +5 V.** Its only non-signal pin is GND (pin 16).

## Buffer enables

U1 and U2 have **1OE (pin 1) and 2OE (pin 19) tied to GND**: both buffers drive their outputs
permanently. The board has no output-enable of its own; panel blanking is the OEb signal, which the
P2 drives.

## P2 header pin -> I/O offset

The header symbols number pins 1–6 down one column and 7–12 down the other. The embedded photo
(`embedded-p2-eval-header-photo.png`) gives the Eval header's silkscreen: row 1 = `VIO3V3` / `5V`;
rows 2–5 = I/O `7/6, 5/4, 3/2, 1/0` (lower header) and `15/14, 13/12, 11/10, 9/8` (upper);
row 6 = `GND` / `GND`. J1's own net labels `IO+15` at pin 2 and `IO+14` at pin 8 agree with that
reading.

| Header pin | J2 (p0–p7) offset | J2 net | J1 (p8–15) offset | J1 net |
|---|---|---|---|---|
| 1 | VIO3V3 | no-connect | VIO3V3 | no-connect |
| 2 | 7 | E | 15 | IO+15 |
| 3 | 5 | C | 13 | B2 |
| 4 | 3 | A | 11 | R2 |
| 5 | 1 | OEb | 9 | G1 |
| 6 | GND | GND | GND | GND |
| 7 | 5V | **+5VA** | 5V | no-connect |
| 8 | 6 | D | 14 | IO+14 |
| 9 | 4 | B | 12 | G2 |
| 10 | 2 | LATCH | 10 | B1 |
| 11 | 0 | CLK | 8 | R1 |
| 12 | GND | GND | GND | GND |

**Offset map (derived from the table, offset order):** 0 CLK · 1 OEb · 2 LATCH · 3 A · 4 B ·
5 C · 6 D · 7 E · 8 R1 · 9 G1 · 10 B1 · 11 R2 · 12 G2 · 13 B2 · 14 spare (IO+14) ·
15 spare (IO+15).

## Signal path: P2 offset -> buffer -> HUB75 connector

| Offset | Net | Buffer in (pin) | Buffer out (pin) | Output net | J7 pin | J3 pin |
|---|---|---|---|---|---|---|
| 0 | CLK | U2 1A1 (4) | U2 1Y1 (16) | CLK_OUT | 13 | 13 |
| 1 | OEb | U2 1A0 (2) | U2 1Y0 (18) | OEb_OUT | 15 | 15 |
| 2 | LATCH | U2 1A3 (8) | U2 1Y3 (12) | LATCH_OUT | 14 | 14 |
| 3 | A | U2 1A2 (6) | U2 1Y2 (14) | A_OUT | 9 | 9 |
| 4 | B | U2 2A2 (13) | U2 2Y2 (7) | B_OUT | 10 | 10 |
| 5 | C | U2 2A3 (11) | U2 2Y3 (9) | C_OUT | 11 | 11 |
| 6 | D | U2 2A0 (17) | U2 2Y0 (3) | D_OUT | 12 | 12 |
| 7 | E | U2 2A1 (15) | U2 2Y1 (5) | E_OUT | 8 | 8 |
| 8 | R1 | U1 1A1 (4) | U1 1Y1 (16) | R1_OUT | 1 | 1 |
| 9 | G1 | U1 1A0 (2) | U1 1Y0 (18) | G1_OUT | 2 | 2 |
| 10 | B1 | U1 1A3 (8) | U1 1Y3 (12) | B1_OUT | 3 | 3 |
| 11 | R2 | U1 1A2 (6) | U1 1Y2 (14) | R2_OUT | 5 | 5 |
| 12 | G2 | U1 2A2 (13) | U1 2Y2 (7) | G2_OUT | 6 | 6 |
| 13 | B2 | U1 2A3 (11) | U1 2Y3 (9) | B2_OUT | 7 | 7 |
| 14 | IO+14 | U1 2A0 (17) | U1 2Y0 (3) | IO+14_OUT | — | — |
| 15 | IO+15 | U1 2A1 (15) | U1 2Y1 (5) | IO+15_OUT | — | — |

All sixteen offsets drive **into** a buffer input; every signal reaching the panel is a P2
output buffered to 5 V.

## J7 — HUB75 connector (and J3, wired identically)

| Pin | Net | Pin | Net |
|---|---|---|---|
| 1 | R1_OUT | 2 | G1_OUT |
| 3 | B1_OUT | 4 | **H75_UNUSED_OUT** (to J6 only) |
| 5 | R2_OUT | 6 | G2_OUT |
| 7 | B2_OUT | 8 | **E_OUT** |
| 9 | A_OUT | 10 | B_OUT |
| 11 | C_OUT | 12 | D_OUT |
| 13 | CLK_OUT | 14 | LATCH_OUT |
| 15 | OEb_OUT | 16 | GND |

- **Pin 8 is E.** The DATA-IN picture labels that position GND, and the sheet annotates it
  "GND here is Really E": on a HUB75E (five-address-line) panel the position a plain HUB75 pinout
  calls GND carries E.
- **Pin 4 is not grounded.** It is the net `H75_UNUSED_OUT`, whose only other connection is the
  J6 through-hole. No buffer drives it.
- J3 repeats J7 pin for pin, including pin 4 (`H75_UNUSED_OUT`) and pin 16 (GND).

## The spare offsets (14, 15)

- **J4**: pin 1 GND, pin 2 IO+14, pin 3 IO+15 — the P2 pins themselves, unbuffered.
- **J5**: pin 1 GND, pin 2 IO+14_OUT, pin 3 IO+15_OUT — the same pins after U1, at 5 V.
- Neither spare is wired to J7 or J3. J4/J5/J6 are through-holes "so can populate and connect
  unused pins if need be."

## What the sheet does not state

Board dimensions, current draw, maximum clock rate, mounting holes, the host boards it fits beyond
its own title ("for P2 Eval") and the box heading ("P2 Eval Edge Expansion Socket (dual)"), and
any panel type, size or scan rate. The board size, current and clock figures are the designer's
own statement: `p2-hub75-adapter-designer-statement-2026-10-10.md`.
