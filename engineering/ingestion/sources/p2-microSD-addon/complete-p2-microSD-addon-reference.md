# P2 microSD Add-on Board (#64009) — Complete Reference

**Source:** `64009-P2-microSD-AddOn-Guide-v1.0.pdf` (Parallax Inc.)
**Edition:** v1.0, dated 22/02/2021 (cover) / 3/08/2021 (pp.2–3 footers)
**Pages:** 3
**Ingested:** 2026-06-27 (addon-wave-2026-06, pass 1–5, stage-only)
**Type:** Hardware accessory product guide (no firmware/code listings)

---

## Overview

Adapter board that connects a standard microSD card to the Parallax Propeller 2 (P2)
microcontroller, or optionally to any other microcontroller / breadboard project.

- Connects a microSD card to any P2 development board with a **standard 2x6-way accessory header**.
- On a general accessory header → general data read/write (data logging, reading program data).
- On the **special P2 programming header (IO pins 56–63)** → also allows **booting from a
  firmware image stored on the microSD card**.
- Seven 0.1" pitch through-hole SIP pads expose all microSD card signals; accept a standard
  vertical or right-angle pin header (not supplied) for breadboard / other-MCU use
  (e.g. Parallax FLiP try-it kit).

## Features

- Connects a microSD card (not included) to the Propeller 2 Accessory Header.
- Allows booting from a binary firmware file saved on the microSD card when connected to the
  P2 programming header (IOs 56–63).
- Connect to any 2x6-way accessory header for general data reading and writing.
- Unpopulated pads expose all microSD card power and control signals — handy for attaching
  logic probes, or connecting to a breadboard / other microcontroller.

## Specifications

| Spec | Value |
|------|-------|
| Accessory connector | 2x6 female socket, 0.1" spacing, compatible with standard Parallax P2 Accessory sockets |
| Breakout | Unpopulated 7-pin SIP through-hole pads, 0.1" spacing |
| Breakout signals | 3V3, DET, MISO, MOSI, CS, CLK, GND |
| PCB dimensions | 0.8 x 1.05 in (20.32 x 26.67 mm) |
| Operating temperature | -40 to +185 °F (-40 to +85 °C) |

## Pin Connections (the load-bearing table)

`Accessory header pin` → `SIP breakout pad` → `Function`.
(Camelot-extracted CSV also staged at `assets/pin-connections-table.csv`.)

| Accessory header pin | SIP breakout pad | Function / Notes |
|----------------------|------------------|------------------|
| VIO3V3 | 3V3 | Supply voltage to microSD card. 3.3V required to power the card. **Do not supply power to both the accessory-header pin and the SIP breakout pad at the same time.** |
| 5V | N/C | Supply voltage from P2 accessory header — **Not Connected and Not Labelled** on this board. |
| +7, +6, +0 | N/C | Not Connected. |
| +5 | CLK | Connects to SD-CLK. |
| +4 | CS | Connects to SD-CS (CD/DAT3/CS). |
| +3 | MOSI | Connects to SD-DI (CMD/MOSI). |
| +2 | MISO | **Series 240R** from SD-DO (MISO). Resistor provided for **P2 boot compatibility**. |
| +1 | DET | Card detect. **Internal 470K pull-up to 3V3, active low when card inserted.** |
| GND | GND | Common ground reference connection. |

**Notes on the `+N` accessory-header notation:** the `+N` form denotes the P2 accessory
header's per-board base-pin offset (the standard Parallax 2x6 accessory convention). On the
P2 programming header (base pin 56) the offsets map to absolute IOs 56–63; e.g. CLK=+5,
CS=+4, MOSI=+3, MISO=+2, DET=+1 — used for microSD boot. The exact base depends on which
accessory header the board is seated in.

**SIP pad order (left→right, confirmed by the page-3 dimension drawings via OCR):**
`GND  CLK  CS  MOSI  MISO  DET  3V3`.

## SPI signal mapping (cross-reference summary)

| SD card signal | SPI role | Board pad |
|----------------|----------|-----------|
| SD-CLK | SCK (clock) | CLK |
| SD-CS (CD/DAT3/CS) | CS / chip-select | CS |
| SD-DI (CMD/MOSI) | MOSI (host→card) | MOSI |
| SD-DO (DAT0/MISO) | MISO (card→host), via 240R series | MISO |
| Card-detect switch | — (470K pull-up to 3V3, active-low) | DET |
| 3.3V / GND | power | 3V3 / GND |

## Dimensions

PCB 0.8 x 1.05 in (20.32 x 26.67 mm). Two mechanical dimension drawings appear on page 3
(see image catalog). The dimension-line numerals OCR as garbled (mechanical-drawing leader
text); the overall in/mm figures above come from the clean text-layer Specifications.

## Resources and Downloads

Latest version of this document + schematic diagram: Parallax 64009 product page
(www.parallax.com, search "64009").

## Revision History

- **Version 1.0** — Original release.
