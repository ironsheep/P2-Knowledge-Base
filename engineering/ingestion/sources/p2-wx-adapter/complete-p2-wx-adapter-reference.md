# P2 WX Adapter Add-on Board (#64007) — Curated Reference

**Source**: 64007-P2-WX-Adapter-Guide-v1.0.pdf (Parallax, official)
**Version**: v1.0 — 11/12/2020 — 7 pages
**Extraction**: 2026-06-27 (re-extraction; supersedes 2025-08-29 PDF-era capture)
**Trust**: GREEN — official Parallax hardware documentation

---

## Purpose

Passive adapter board that hosts a **Parallax WX WiFi ESP8266 SIP module (#32420S)**
on any Propeller 2 board's standard **2×6 accessory header**, adding:
- **Serial-over-WiFi** from *any* accessory header (any ESP8266 firmware version), and
- **Wireless programming** when plugged into the **P56–P63 header marked with the "RES" logo**
  (requires the special P2 WiFi firmware `P2_httpd_xxxx.ota`, which hosts a drag/drop
  P2 loader on its web page that accepts a P2 binary compiled in any language).

The board itself contains **no programmable logic and ships with no P2 code** — it is a
signal-routing adapter between the 2×6 header and the 10-pin WiFi-module SIP socket.

## Specifications

- 10-pin SIP socket, 0.1" spacing, for the Parallax WX WiFi ESP8266 SIP Module (#32420S)
- Unpopulated 8-pin SIP through-hole pads, 0.1" spacing, exposing the WiFi module control
  signals **PGM, DBG, ASC, CTS, RTS, DO, DI, RES** (for logic probes)
- 2×6 female socket, 0.1" spacing, compatible with standard Parallax P2 Accessory sockets
- PCB dimensions: **1.2 × 1.0 in (30.48 × 25.4 mm)**
- Operating temperature: **−40 to +185 °F (−40 to +85 °C)**
- Golden-Egg-shaped Access Point (AP) enable pads (short 4× quickly with a metal object
  to force the module back into AP-discovery mode)

## Pin Connections (authoritative — from text layer, camelot-confirmed)

This adapter and the Parallax WX WiFi module **share these signals**, so this map is
high-value cross-check fodder against the `parallax-wx-wifi` module ingestion.

| Accessory header pin | WiFi module pin | Function |
|---|---|---|
| GND     | GND  | Common ground |
| 0       | RES  | WiFi module reset signal |
| 1       | PGM  | WiFi module configure (ESP IO0) |
| 2 – 5   | –    | Not Connected |
| 6       | DI   | WiFi module RXD |
| 7       | DO   | WiFi module TXD |
| RES     | CTS  | Target board reset signal for Propeller microprocessor (ESP IO13) |
| VIO3V3  | 3.3V | Supply voltage to WiFi module |

> Pin-diagram caption: "Dark blue traces on top of PCB, light blue on bottom of PCB."
>
> Note the signal-name swap across the connector: the adapter's header **pin 0 → module RES**
> and header **pin 1 → module PGM**, while header label **RES → module CTS** (the *target P2*
> reset, driven from ESP IO13). "RES" thus names two different nets depending on side — the
> header's RES-logo position vs. the WiFi module's RES input.

## Firmware / Workflow (summary)

1. Seat the WX module on the adapter (white silkscreen marks metal-can orientation); plug the
   adapter into the **RES-logo** 2×6 header (must wire P56–P63 + power + ground).
2. Power up; the module's blue **ASC** LED blinks. Join its WiFi network `WX-123456`
   (touch the AP golden-egg pads 4× quickly if the network isn't visible).
3. One-time setup at `http://192.168.4.1`: upload `P2_httpd_xxxx.ota` via the **Firmware** menu;
   under **Settings** set the reset dropdown to **"CTS"** (may default to DTR), then SAVE +
   SAVE to FLASH. A new **"P2 Loader"** menu appears.
4. Use the **P2 Drop Loader** drag/drop area to upload P2 `.binary` files; success reports "Done!".
   (Example `LED57.binary` blinks an LED on P57; enable the P2 Edge "LED" dip-switch for the demo.)

Browsers: Chrome or Edge recommended. Resources/schematic: parallax.com, search **64007**.

## Required companions

- Propeller 2 board with the 2×6 **P56–P63 RES-logo** header
- Parallax WX ESP8266 WiFi Module — SIP, **#32420S**
- P2 programming software emitting binaries (e.g. Propeller Tool 2.3)
- Latest P2 firmware + example binary from the 64007 product page

## Revision History

- v1.0: Original release (11/12/2020).
