# P2 RTC Add-on (#64013) — Curated Reference

**Source:** `64013-P2-RTC-Add-on-Guide-20221129.pdf` (Parallax Inc., v1.0, 11/29/2022, 3 pp.)
**Ingested:** 2026-06-27 (addon-wave-2026-06, MAP agent, passes 1–5, STAGE-ONLY)
**Format path:** PDF-only ladder — clean text layer (no OCR for body); `camelot lattice` for the pin-connections table; `pdfimages` + `image-tools-mcp` for figures.

## What this board is

A small Parallax P2 single-Accessory add-on board that adds a battery-backed
real-time clock + calendar + alarm to a Propeller 2 (P2X8C4M64P) system. Built
around the **NXP PCF8523** CMOS RTC, talked to over **I2C**. An on-board
**rechargeable lithium cell (Seiko MS421R)** keeps time across power loss; it is
trickle-charged from the 3.3 V rail while the host is powered.

## RTC chip identity (key fact)

| Field | Value | Source / authority |
|---|---|---|
| RTC IC | **PCF8523** CMOS Real-Time Clock + calendar | This guide, Features + datasheet pointer (NXP, www.nxp.com) |
| Bus | **I2C** (open-drain), up to **1000 kbit/s** | Features + Key Specs |
| I2C speeds | 100, 400, 1000 kHz | Key Specs (Control interface) |
| **I2C slave address** | **NOT STATED in this guide** — see gap RTC-G1 | (PCF8523 datasheet — propose, do NOT infer here) |
| Register map | NOT in this guide — defers to PCF8523 datasheet | datasheet pointer |
| Signal levels | 3.3 V | Description, Key Specs |

> The guide is a **board-level** document: it deliberately defers all RTC
> register/API detail to the **PCF8523 datasheet** ("Refer to the PCF8523 RTC
> datasheet for full details"). I2C address, register map, command/API, alarm
> register layout, offset-register tuning detail are all out-of-document.

## Pin connections (Parallax P2 Accessory header → RTC board)

Resolved cleanly by `camelot lattice` (lattice removed the row-placement
ambiguity in the raw text; **silkscreen OCR independently confirms** SCL on +0,
SDA on +1):

| Accessory header pin | RTC fn | Meaning |
|---|---|---|
| **VIO3V3** | 3V3 | 3.3 V supply; powers the RTC and trickle-charges the battery |
| +7 … +2 | — | Not connected |
| **+1** | **SDA** | I2C serial data I/O |
| **+0** | **SCL / INT / CLKOUT** | One shared IO pin: SCL (I2C clock, input) **or** INT (interrupt out) **or** CLKOUT (clock out) — see Code Tip |
| GND | GND | Common ground |

### Code Tip (P2 smart-pin usage — board-author guidance)

The **SCL, INT, and CLKOUT functions share the single +0 IO pin.**
- To use **I2C SCL**: set the I2C output mode with a **3.3 kΩ pull-up**.
- To use **INT or CLKOUT**: first configure them over I2C per the RTC datasheet
  API, then **disable I2C** and set the P2 smart pin (or equivalent) **input mode
  with a 150 kΩ pull-up**.

## Key specifications

- Supply: **+3.3 VDC**
- Battery: built-in rechargeable lithium metal cell **Seiko MS421R** — 1.5 mAh nominal, 0.11 g
- Low backup current: typ. **150 nA**
- Interface pins: open-drain interrupt / clock output
- Form factor: dual **2×6-pin female passthrough** headers, 0.1" spacing (passthrough = stackable)
- Mounting hole: 3.2 mm dia.
- Operating temp: −20 to +60 °C (−4 to +140 °F)
- PCB: 0.8 × 1 in (20.32 × 25.4 mm)

## Battery / transport note

Built-in non-removable lithium-metal cell, ≤1 g lithium, meets UN Manual of
Tests & Criteria Part III §38.3 → transportable as Class 9 Dangerous Goods.
(Seiko MS421R datasheet: https://www.sii.co.jp/en/)

## Code examples

**None in this document.** The guide points to example code on the product page
(search 64013 at www.parallax.com) but ships no Spin2/PASM2 listing. Pass-2 code
counts are therefore 0/0/0.

## Cross-references (P2 knowledge base)

- **I2C smart-pin signalling** — the Code Tip's pull-up modes and the SCL/SDA
  open-drain behavior are P2 smart-pin facts; corroborate against the smart-pin /
  I2C protocol-layer KB rather than this guide (this guide does not specify the
  smart-pin mode registers).
- **Shared-pin discipline** (drive-mode swap to read INT/CLKOUT) is a generic P2
  open-drain idiom; the protocol layer is the authority.
