# Parallax WX ESP8266 Wi-Fi Module — Curated Reference (Pass-1)

**Source:** `32420-Parallax-WX-WiFi-Module-Guide-v1.0.pdf` (Parallax Inc.)
**Edition:** v1.0, 05/12/2016 — 12 pages — Revision History: "Version 1.0: Original release"
**Part numbers:** #32420D (DIP), #32420S (SIP)
**Re-extraction:** 2026-06-27 (replaces lossy PDF-era capture; clears 12+-image debt)
**Extraction tooling:** `pdftotext -layout` (text), `docling`/`camelot lattice` (pin table), `pdfimages -png` + `image-tools-mcp` (images)

> This is a **hardware product guide** for an ESP8266-WROOM-02-based Wi-Fi module
> (serial-bridge / web-config device). It contains **no PASM2/Spin2 code** — it is
> a board/peripheral reference. Its P2 relevance is as the Wi-Fi module behind the
> Propeller Activity Board WX socket and wireless-programming workflow.

---

## Overview

The Parallax WX Wi-Fi module adds 2.4 GHz Wi-Fi to a microcontroller project. It can run
as its own access point (**AP**), as a station on another network (**STA**), or **STA+AP**
(briefly, for joining another network). It serves its own configuration pages plus
user-uploaded web pages, enabling devices to interact with a host microcontroller over Wi-Fi.
On Internet-connected networks it can send/receive TCP/IP messages for IoT projects, and it
self-hosts a firmware-upgrade page for OTA updates.

**Two form factors:**
- **#32420S (SIP)** — breadboard-friendly, 5 V and 3.3 V compatible, 0.1" right-angle SIP;
  works with BASIC Stamp, Arduino, Propeller.
- **#32420D (DIP)** — 3.3 V, 2 mm DIP designed for the Propeller Activity Board socket
  (original #32910 and WX #32912). **NOTE: not compatible with Parallax XBee adapter boards.**

## Features

- 2.4 GHz Wi-Fi via ESP8266-WROOM-02 (FCC and CE approved).
- **Transparent serial mode** — wireless microcontroller programming and debugging (Activity Board WX).
- **Command serial mode** — exchange information with the host microcontroller.
- **3 Wi-Fi modes:** AP (up to four devices join), STA, STA+AP.
- Micro web server (config + user pages) in STA or AP mode.
- ~1 MB user file system for web pages / content.
- Built-in config web pages: settings, networks, file uploads, OTA firmware updates.
- OTA web-page uploads via web interface; OTA firmware upgrades (.ota files).
- Supports HTTP (server), WebSocket (server), and TCP (client) connections.
- Power, Associate, Data-In, Data-Out LEDs visible from both sides of the PCB.

## Specifications

| Spec | Value |
|---|---|
| Wi-Fi protocols | 802.11 b/g/n |
| Network protocols | IPv4, TCP/HTTP |
| Security | WPA/WPA2 |
| Encryption | WEP/TKIP/AES |
| Wi-Fi range | 30 meters LOS |
| Voltage (SIP/breadboard) | +3.3 to +5 VDC |
| Voltage (DIP/WX 2×10×2 mm) | +3.3 VDC |
| Logic levels (SIP) | output high = Vin (3.3 or 5.0 V), low 0 V; input high > Vin/2, input low < Vin/2 |
| Logic levels (DIP) | output high 3.3 V, low 0 V; input high > 1.5 V, input low < 1.5 V |
| Current | typical 75 mA; Wi-Fi transmit peaks up to 360 mA |
| Form factor (SIP) | 0.1" (2.54 mm) row of 10 right-angle pins |
| Form factor (DIP WX) | 0.078" (2 mm) dual row of 10 straight pins |
| PCB dimensions | ~1.0 × 1.5 in (26 × 37.5 mm) |
| Operating temp | +32 to +158 °F (0 to +70 °C) |

**ESP8266-WROOM-02 core:** low-power 32-bit MCU Wi-Fi module, embedded TCP/IP stacks,
16 Mbits SPI flash, low-power modes (e.g. DTIM10 at 1.2 mW). Certified FCC, CE, KCC, TELEC,
LCIE, IC.

## Functional components (labeled 1–10 in the functional-description figure)

1. **ESP8266-WROOM-02 Wi-Fi module** — core (see above).
2. **WX compatible headers** — DIP plugs into the Activity Board WX 2×10×2 mm socket.
3. **Linear 3.3 V regulator** — LDO powers the ESP8266 and sets WX IO-port logic-level voltage.
4. **Reverse-polarity protection** — on the SIP/breadboard header, a P-channel MOSFET gives
   reverse-polarity protection with near-zero VIN drop.
5. **Power LED** — on while correct-polarity voltage is supplied (WX/XBee socket or SIP);
   visible from both sides.
6. **ASC "Associate" LED** — see LED-behavior table below.
7. **DI "Data-In" LED** — blinks while serial data is received (WX or SIP header).
8. **DO "Data-Out" LED** — blinks while serial data is transmitted (WX or SIP header).
9. **Level shifters / buffers** — SIP IO logic levels are set by VIN (3.3 V VIN → 3.3 V IO; 5 V VIN → 5 V IO).
10. **SIP "Breadboard" header** — standard 0.1" male header; cables e.g. 800-00048, 751-00010.
    First four pins **GND, RES, DI, DO** are compatible with the Parallax Prop Plug (#32201)
    for firmware reprogramming/development.

### ASC "Associate" LED behavior

Notation: **bold** = wireless mode, small text = connectivity, after "-" = LED behavior/timing.

| Mode / state | LED behavior |
|---|---|
| **AP** (has IP) [wirelessly accessible] | ON constantly |
| **STA+AP** (no IP on STA, IP on AP) [accessible] | OFF 2000 ms, ON 2000 ms |
| **STA+AP** (IP on STA and AP) [accessible] | OFF 2000 ms, ON 25 ms, OFF 150 ms, ON 2000 ms |
| **STA** (has IP) [accessible] | OFF 4000 ms, ON 25 ms |
| **STA** (no IP) [not accessible] | OFF constantly |

## Pin Descriptions (authoritative — docling table, p11; cross-checked vs camelot lattice + text)

| Module Pin | Direction | SIP Pin | DIP Pin | ESP8266 | Function |
|---|---|---|---|---|---|
| VIN | Power input | 1 | 1 | — | (SIP) 3.3 V or 5 V power input; (DIP) 3.3 V power input |
| /PGM | Input | 2 | 20 | IO0 | If held low during power-up, ESP8266 boots ready for serial firmware load. Can also be pulled low rapidly, 4× in a row, to put module into AP+STA mode. |
| DBG | Output | 3 | 9 | IO2 | Transmits information about exchanges with the host microcontroller. |
| ASC | Output | 4 | 15 | IO5 | Associate — high/low patterns indicating Wi-Fi mode and connection. |
| /CTS | Input / Output | 5 | 12 | IO13 | User configurable pin. |
| /RTS | Output | 6 | 16 | IO15 | User configurable pin. |
| DO | Output | 7 | 2 | TXD | Transmits serial data to microcontroller host. |
| DI | Input | 8 | 3 | RXD | Receives serial data from microcontroller host. |
| /RES | Input | 9 | 5 | EN | Active-low reset line. |
| GND | Power input | 10 | 10 | GND | Ground. |
| PS | Output | — | 7 | IO4 | May be used in future to remotely switch a WX carrier board's programming source from USB to Wi-Fi. |
| DTR | Output | — | 18 | IO12 | Toggles microcontroller reset line in WX carrier board. |

> Note: the schematic pinout figure (image wx-016) OCR'd to noisy labels (e.g. `/ESPIO14`,
> `i6`=IO16) — the **table above is authoritative**; the figure is illustrative only.

## Configuration (web UI)

- Ships pre-configured as an AP. Join the SSID starting `wx-` followed by 6 alphanumerics
  (e.g. `wx-dba23b`).
- To re-enter AP mode after joining another network: rapidly ground/release **/PGM four times**
  (Activity Board WX: press/release **RST** rapidly 4×; breadboard: a pushbutton from GND to /PGM).
- After joining, browse to **http://192.168.4.1** for the Configuration home page.
- **4 sub-pages** (Chrome recommended):
  - **Networks** — set Wi-Fi mode and join another network.
  - **Files** — upload web pages / files (~1 MB store; serves most-recent upload; "Empty" clears the file system; no full file manager in this firmware).
  - **Settings** — module name + serial-comm settings; defaults suit the Propeller Activity Board (also enables loading programs into a Propeller in an Activity Board WX through the module). BASIC Stamp 2 settings are in that product's Getting Started Guide.
  - **Firmware** — OTA upgrade: download firmware from parallax.com, unzip, choose the `.ota` file, load.
- **Joining a network (STA+AP → STA):** click Networks, set mode **STA+AP**, pick the network,
  enter password, Connect. Then **(1)** note the assigned IP immediately, and **(2)** immediately
  set mode back to **STA** — leaving STA+AP can introduce a **security vulnerability** to the
  joined network. Example assigned IP `10.10.11.145` replaces `192.168.4.1` (which only works in AP mode).
- Uploaded file `web-page.html` is served at `http://192.168.4.1/files/web-page.html` (AP) or
  `http://<assignedIP>/files/web-page.html` (STA).

## Application ideas

- Host/serve control & monitoring pages over Wi-Fi; module acts as a serial intermediary
  between the microcontroller and HTTP/WebSocket clients (e.g. a Boe-Bot reporting Ping)))
  distance and taking commands from a phone web page).
- Program the Propeller Activity Board WX over Wi-Fi with the DIP module; view remote sensor
  data live in the SimpleIDE Terminal without a USB tether (reprogram an ActivityBot mid-maze).
- Make TCP client connections to Internet web pages; send messages to services that trigger
  emails, Twitter feeds, etc.

## Firmware lineage (from config-home screenshot, image wx-010 — NEW evidence)

The config home page identifies the firmware as **"Remora"**, version **v1.0 (2016-11-02 18:04:30)**,
and credits **"LINK by Thorsten von Eicken"** — i.e. the module's firmware derives from the
open-source **esp-link** project (Thorsten von Eicken). Document body calls it "the latest open
source firmware revision … contributed by Parallax and the open source community."

## Contacts (cover)

www.parallax.com · forums.parallax.com · sales@parallax.com · support@parallax.com ·
Office (916) 624-8333 · Sales (888) 512-1024 · Tech Support (888) 997-8267.
