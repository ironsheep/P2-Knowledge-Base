# P2-ES Eval HyperRAM & HyperFlash Add-on (#64004-ES) — Complete Reference

**Source of record:** `64004-ES P2-ES Eval HyperRAM_Flash Memory Board Product Guide.pdf` (9 pp; Google-Docs export)
**Cross-check source:** `64004-ES-REVA-HyperRAM_FLASH-0721-SCHEMATIC-OS.pdf` (3 sheets; clean text layer — title block only)
**Extraction:** 2026-06-22 · pass-1 content via **forced OCR** (`docling --force-ocr`, RapidOCR) — the PDF's embedded
text layer is corrupt (ciphered ToUnicode CMap on part of the doc); OCR bypasses it. See the extraction audit.
**Doc version:** 1.0 (Revision History: "Version 1.0: Original Release") · **Board rev:** A (schematic "Last Update 21 Jul 2019")

> **Trust note.** This is the Parallax primary product document for the board → 🏆 authoritative for the
> board's specs/pins/configuration. OCR-derived fields that carry transcription risk (part numbers, URLs) are
> flagged **[VERIFY]** below and must be confirmed against the ISSI datasheets / the 64004-ES product page
> before they propagate to published YAML. **Do not fabricate from the raw CAD/schematic.**

## Overview
Limited-edition **16 MB HyperRAM + 32 MB HyperFlash** add-on board, designed for the (also limited-edition)
**Propeller 2 ES Evaluation Board (#64000-ES)**. Features **dual 2×6 pass-through sockets** that stack on top of
two P2-ES Eval Board IO-pin breakout edge headers; up to four add-on boards can be stacked (one per side).
Comes fully assembled (surface-mount) but supports all combinations of hyper-memory devices (de-/re-soldering
required) or build-your-own from the open-source design files.

- **Device A** (lower position): pre-installed **HyperRAM, 16 MB**.
- **Device B** (upper position): pre-installed **HyperFlash, 32 MB**.
- Each device may be a RAM, Flash, or dual-memory; the PCB carries configuration options for each type.

## Specifications
| Spec | Value |
|------|-------|
| RAM | 16 MB / 128 Mb (16 Mb × 8) Parallel PSRAM |
| Flash | 32 MB / 256 Mb (32 Mb × 8) Parallel NOR Flash |
| Voltage | +3.3 VDC (supplied by P2-ES Eval Board I/O LDO regulator) |
| Max clock rate | 100 MHz (200 MB/s) at 3.0 Vcc |
| RAM current | 60 mA peak burst, 600 µA standby (CS# = High) |
| Flash current | 100 mA peak burst, 25 µA standby (CS# = High) |
| Flash endurance | 100,000 program/erase cycles |
| Flash retention | 20-year data retention |
| Form factor | dual 2×6-pin female passthrough headers, 0.1" spacing |
| Mounting hole | 2.5 mm (100 mil) hole, pad ring 4.5 mm (180 mil), connected to GND |
| Operating temp | −40 to +185 °F (−40° to +85° C) |
| PCB dimensions | 1.0 × 1.9 in (25.4 × 48.3 mm) |

## Pin Definitions and Ratings — **triple-validated** (ciphered text ∩ OCR ∩ mechanical drawing img-006)
Pins are **relative offsets `IO+0..IO+15`** from the base pin of whichever 16-pin P2 header block the board is
mounted on. "Type" is the P2-side pin role: **MOSI** = P2 output, **MISO** = P2 input, **In/Out** = bidirectional.

| Pin | Type | HyperBUS function | Device | Description |
|-----|------|-------------------|--------|-------------|
| IO+0 … IO+7 | In / Out | DQ[0..7] | Both | 8-bit data bus — Command, Address, and Data transferred on these during read/write |
| IO+8 | MOSI | CK | A | Single-ended clock |
| IO+9 | MOSI | CK | B | Single-ended clock |
| IO+10 | In / Out | RWDS | A | Read/Write Data Strobe (slave output during command/address; edge-aligned with read data; data-mask on write) |
| IO+11 | In / Out | RWDS | B | (as IO+10, device B) |
| IO+12 | MOSI | CS# | A | Chip Select — bus transaction starts High→Low, ends Low→High |
| IO+13 | MOSI | CS# | B | Chip Select (device B) |
| IO+14 | MISO | INT# (Flash only) | B | Interrupt output (open-drain) — Low indicates an internal event occurred |
| IO+15 | MOSI | RESET# | Both | Hardware reset. Low (default) = device self-initializes to Standby; assert High to enable HyperBUS. Includes a user-selectable 10K pull-down so HyperRAM clears on Propeller reset. |

## Configuration pads & resistors (Feature Descriptions §3–§8)
- **Optional RES / GND pads (§3):** access to the HyperBUS reset signal. *Standard:* shunt resistor across the
  **center-and-right** pads keeps the module held in reset until IO+15 is asserted High. *Alternate:* move the
  shunt to **left-and-center** → module normally active; assert IO+15 **or** the RES pad **Low** to reset.
- **Optional Configuration Pads (§4): `INT / RSTO / CSx-BR / CSx-AF`** — extra HyperBUS signals for users
  experimenting with alternate memory types. (Open in the spirit of openness; not supported/warrantied by Parallax.)

  | Pad | Type | HyperBUS function | Device | Notes |
  |-----|------|-------------------|--------|-------|
  | INT *1 | MISO | INT# (Flash only) | A | Interrupt output (open-drain) |
  | RSTO *2 | MISO | RSTO# (Flash only) | B | POR (Power-On-Reset) indicator, open-drain; high-Z after internal POR timeout → external pull-up drives High → Standby |
  | RSTO *2 | MISO | RSTO# (Flash only) | A | (as above, device A) |
  | CSx BR | MOSI | CS# | B | Applies when device **B** is a **HyperRAM** |
  | CSx AF | MOSI | CS# | A | Applies when device **A** is a **HyperFlash** |

  *\*2:* In the standard Parallax config the RSTO# signals are split — device A RSTO# → right-RSTO pad,
  device B RSTO# → left-RSTO pad; can be joined via the unpopulated 0603 resistor pad under the RSTO pads.
- **Memory-Type Configuration Resistor B (§5):** below the **"FLS B RAM"** label; 2-position shunt sets device-B
  memory type. Connects CS# to the appropriate pin (HyperRAM vs HyperFlash use a different CS# pin). `FLS`=Flash,
  `RAM`=RAM. Pre-installed device B = HyperFlash → shunt pre-set to **FLS**.
- **Memory-Type Configuration Resistor A (§7):** above the **"FLS A RAM"** label; 2-position shunt sets device-A
  memory type. Pre-installed device A = HyperRAM → shunt pre-set to **RAM**.
- **`+ R C` Configuration resistors (§6):** each HyperBUS device has three, on the right side:
  - **`+`** 10 kΩ pull-up connecting CS# to 3.3 V
  - **`R`** 10 Ω series resistor connecting RWDS to IO+10 (device A) or IO+11 (device B)
  - **`C`** 10 Ω series resistor connecting CK to IO+8 (device A) or IO+9 (device B)
- **Decoupling capacitors (§8):** each HyperBUS memory has four — a 100 nF and a 1 µF per VccQ pin (per the
  HyperBUS memory chip datasheet).
- **Mounting hole (§9):** plated, attached to the ground plane.

## Quick Start
1. Place the add-on PCB **chip-side-up** over a pair of P2-ES EVAL board edge headers; align pins, press gently.
2. **Strongly recommended:** connect the auxiliary power supply to the P2-EVAL board's **AUX USB** port — power
   needs may exceed what PC-USB supplies.
3. To enable the HyperBUS memory, **assert RESET# (IO+15) High.** Module can be cleared/disabled in user code by
   asserting RESET# Low.
4. Code examples: Parallax product/developer page — https://propeller.parallax.com/

> The board does **not** source power via the passthrough header's 5V socket, so the P2-ES Eval Board Rev B's
> **ACC HDR jumper can remain in the default off position.**

## Resources & Downloads  — **[VERIFY: OCR-transcribed, confirm before publishing]**
- HyperRAM datasheet: **ISSI `IS66WVH16M8BLL-100B1LI`** [VERIFY] — `http://www.issi.com/WW/pdf/66-67WVH16M8ALL-BLL.pdf` [VERIFY]
- HyperFlash datasheet: **ISSI `IS26KL256S-DABL100`** [VERIFY] — `http://www.issi.com/WW/pdf/26KS-KL128S-256S-512S.pdf` [VERIFY]
- Schematic / design files / latest doc / example programs: 64004-ES product page at www.parallax.com (Downloads / Details & Additional Resources tabs).

## Provenance
- **Part number:** 64004-ES · **Board revision:** A (schematic "Last Update 21 Jul 2019")
- **Copyright** 2019 Parallax Incorporated · **Open Source Hardware**, licensed **CC BY-SA 4.0**
- Schematic sheets (3): *HyperRAM and HyperFLASH* · *Decoupling and Breakouts* · *BOM*
- Product Guide document **Version 1.0 — Original Release**
