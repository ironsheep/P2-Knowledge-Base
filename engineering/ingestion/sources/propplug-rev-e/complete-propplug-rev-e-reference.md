# Prop Plug Rev E (#32201) — Complete Reference

**Source:** `32201-PropPlugRev-Guide-RevE.pdf` (Parallax Inc.)
**Edition:** Document v3.0, 2/03/2021 — 4 pages — "Version 3.0: original release for Rev E."
**Hardware revision:** Rev E
**Part number:** #32201
**Re-extraction:** 2026-06-29 (addon-wave-2026-06 follow-on; **re-extraction** — supersedes the lossy 2025-08-29 PDF-era capture)
**Extraction tooling:** `pdftotext -layout` (text — clean text layer), `pdf2md` (docling), `pdftoppm`+visual read for the figure-only "Interface to Propeller Chip" pinout (page 3).
**Type:** Hardware programming-adapter product guide (no firmware / no code listings).
**Trust:** 🏆 / GREEN — official Parallax hardware documentation.

> This is a **USB-to-serial programming adapter**, not a header add-on board. It is the
> standard in-system programming/communication tool for Propeller circuits (P1 and P2) that
> expose the 4-pin programming header. Cross-corroborated as a P2 programming requirement by
> the #64010 Universal Motor Driver and #64007 WX-Adapter guides ("a Prop Plug … is typically
> required for programming the P2 Edge module").

---

## Overview

The Prop Plug provides a USB-to-serial port connection convenient for microcontroller
programming and communication. It slips onto a **4-pin, 0.1″-spaced male header**, providing
in-system programming of Propeller circuits in breadboard, perf-board, and permanent projects
that carry the four-pin header. Capable of asynchronous communication at up to **3 Mbaud** with
both **3.3 V and 5.0 V** devices (such as the Propeller 1 and BASIC Stamp).

Rev E uses the **FTDI FT231X** USB bridge IC (USB 2.0 Full Speed) and therefore requires FTDI
USB drivers.

### What's new in Rev E
- Pin labelling on **both sides** of the board.
- 2-sided **TX / RX activity LEDs**, visible from either side of the board.
- **Buffered inputs and outputs** to improve isolation between the Prop Plug and the target
  board when either is powered down.
- **Customer Reset Option** option-pad (DTR / RTS / none — see below), with a white silk area
  for marking units configured differently.

## Specifications

| Spec | Value |
|------|-------|
| Power requirements | Powered by USB port (5 VDC) |
| Current requirements | ~15 mA (typical) |
| USB communication interface | USB 2.0 Full Speed |
| UART communication interface | True 3.3 V CMOS drive output and TTL input |
| RX input | Buffered; compatible with 3.3 V and 5 V signals; tolerant to 5.5 V |
| Activity LEDs | TX and RX, visible from either side of the board |
| Communication speed | Asynchronous serial, 300 baud to 3 Mbps |
| Reset pulse width | ~20 µs typical (varies with target circuit; 15–25 µs) |
| Connection | USB micro-B; 4-pin female SIP socket, 0.1″ spacing |
| USB bridge IC | FTDI FT231X |
| Operating temperature | −40 to +185 °F (−40 to +85 °C) |
| PCB dimensions | 0.93 × 0.48 in (23.5 × 12.1 mm) |
| Dimensions with connectors | ~1.3 × 0.48 in (~33 × 12.1 mm) |

## 4-pin header / Interface to Propeller Chip (the load-bearing pinout)

The Prop Plug's 4-pin female SIP socket mates with a 4-pin male header on the target. Board
silk labels (top → bottom), with the connection to a Propeller from the page-3 figure:

| Board pad (silk) | Direction | Connects to (Propeller) | Notes |
|------------------|-----------|-------------------------|-------|
| **RX** ◄ | input to Prop Plug | Propeller **TX** = **P30** | PropPlug RX / Propeller TX |
| **TX** ► | output from Prop Plug | Propeller **RX** = **P31** | PropPlug TX / Propeller RX |
| **RES** | output from Prop Plug | Propeller **RESn** (reset) | DTR-controlled reset pulse by default (see Reset Option) |
| **VSS** | — | **GND** | Common ground |

> The page-3 "Interface to Propeller Chip" schematic is a **figure only** (no text layer); the
> signal labels above were read directly from the rendered figure (`assets/images-propplug-rev-e-2026-06-29/page-3.png`).
> The figure illustrates a **Propeller 1 (DIP-40)** target with boot EEPROM (P28/SCL, P29/SDA)
> and crystal; P2 programming uses the same four signals against the P2's serial programming pins.

## Customer Reset Option (new in Rev E)

The Prop Plug ships with the serial **DTR** signal connected to control the reset pulse at the
RES output (as in all previous versions). Rev E adds an option pad:

- **DTR-controlled reset** (default): keep the component to the **left**, connecting RES and DTR.
- **RTS-controlled reset**: move the component to the **right**, connecting RES and RTS.
- **No reset pulse**: remove the component.

The reset circuitry generates a short pulse (~20 µs typical) when the USB **DTR** signal toggles
low → high.

## PC Drivers Installation

Rev E requires FTDI USB drivers. Obtain them from `https://www.parallax.com/usbdrivers` (Windows
downloads + install instructions, plus a link to the Mac drivers page). For **macOS 10.15
"Catalina" and later, no installation is necessary** — drivers ship with the OS. Parallax
software that relies on the FTDI drivers normally installs them automatically.

## Required / related parts

| Part | Role |
|------|------|
| **#32201** | Prop Plug Rev E (this product) |
| **#805-00016** | USB A → micro-B cable — **required, not included** |
| **#32200** | Prop Clip — predecessor / related product |
| Prop Plug Rev D and earlier | Prior hardware revisions (see earlier editions of this guide). Earlier revisions used a USB A → **mini-B** cable, which **was** included. |

## Resources and Downloads

Device schematic, documentation for previous device versions, and other resources: the Downloads
and Additional Resources tabs on the **32201** product page (www.parallax.com, search "32201").

## Code examples

**None in this document.** This is a hardware adapter guide — no Spin2/PASM2 listings. Pass-2
code counts are 0/0/0.

## Cross-references (P2 knowledge base)

- **P2 programming workflow** — the Prop Plug is the USB-to-serial adapter behind P2 board
  programming; the #64010 (Universal Motor Driver) and #64007 (WX Adapter) guides both name
  "Prop Plug (#32201)" as the typical programmer for the P2 Edge module. Corroborate the P2
  serial-programming pin assignment against the P2 board guides / Silicon Doc rather than this
  P1-illustrated figure.
- **WX Wi-Fi module (#32420)** — its breadboard (SIP) header's first four pins GND/RES/DI/DO are
  documented as compatible with the Prop Plug (#32201) for firmware reprogramming.

## Revision History (document)

- **Version 3.0** — original release for Rev E (2/03/2021).
