# P1 App Notes → Capability Spine Mapping

> **Status:** v1 (2026-06-29), *Capability Coverage & App-Note Roster* sprint,
> Phase 5 (task #136). Classifies the 17 P1 app notes onto the capability spine
> (`engineering/standards/p2-capability-taxonomy.md`) with a **P2-equivalent
> capability** note for each — many P1 topics *transform* rather than map 1:1.
> This is the **P1 column** input to the coverage matrix (Phase 6, #137).

## Sources
- Titles + the 17 source PDFs: `engineering/ingestion/external-inputs/P1/AppNotes/`.
- Full extractions (5): `engineering/ingestion/sources/P1-App-Notes/` (AN001,
  004, 008, 013, 014).
- **P2-equivalent edges:** the P1↔P2 cross-corpus table in
  `engineering/ingestion/P1-DOCUMENT-LINEAGE.md` (counters→smart pins, video
  gen→streamer, ROM sine/log→CORDIC, no-interrupts→interrupts+events, etc.).

## Mapping

| P1 App Note | Spine domain · leaf | P1→P2 | P2-equivalent capability |
|---|---|---|---|
| **AN001** P8X32A Counters | **B** · counters-equivalents | **transform** | P1 CTRA/CTRB counter modules + PLL → **P2 smart pins** (counter/NCO/measurement modes moved into the pins). |
| **AN002** Real-time GPS Data Reception & Parsing | **F** · gps | map | NMEA parsing is platform-neutral; P2 covered by Quick Byte "NMEA GPS String Parsing". |
| **AN003** Abstract Data Structures with Spin Objects | **A** · data-structures | evolve | Same OOP-in-Spin pattern; **Spin2** objects (evolved language). |
| **AN004** GUI Graphics — Getting Started with VGA & Terminal *(series 1/3)* | **G** · vga-text / terminal | **transform** | P1 VGA via the per-cog video generator → **P2 VGA/DVI/HDMI via streamer + smart pins** (changed mechanism). |
| **AN005** GUI Graphics — Simple VGA Menus *(series 2/3)* | **G** · gui-menus | **transform** | UI/menu layer atop P2 video generation. |
| **AN006** FAT16/FAT32 Full File System Driver | **I** · sd-fat | map | P2 **already covered in OBEX** — Chris Gadd "FAT32 SD card driver" (4269), Ray Allen "FRSW and FAT32" (4894). *Not a P2 gap.* |
| **AN007** Soft-loading an App Image via XBee | **K** · programming-loading *(2° E·wireless)* | map | Wireless code-load; P2 Quick Bytes "Wireless Programming ESP8266 WX", "XBee RF". |
| **AN008** Sigma-delta Analog-to-Digital Conversion | **B** · adc | **transform** | P1 sigma-delta ADC built from counters + R/C → **P2 smart-pin native ADC** (SINC/sigma-delta modes built in). *P2AN000 (ADC) in flight.* |
| **AN009** Execution Time | **A** · execution-timing | evolve | Cycle-accurate timing; P2 `GETCT`/`CNT`, deterministic egg-beater hub. |
| **AN010** Mixed Voltage Interface | **B** · pin-modes *(electrical)* | transform | Level/voltage interfacing; P2 different I/O scheme + smart-pin electricals. *(Judgment: electrical-design topic, nearest spine home is B; flag for review.)* |
| **AN011** Simple Multicore Template | **A** · cogs-multicore | evolve | 8 cogs (P2 adds LUT RAM); structural template for parallel work. **Strong app-note candidate** (core P2 topic, no QB demo). |
| **AN012** Interfacing to External SRAM with SPI | **I** · external-ram | **transform** | P1 SPI SRAM → **P2 HyperRAM/PSRAM** on Edge modules (different external memory). |
| **AN013** GUI Graphics — Window Manager Framework *(series 3/3)* | **G** · gui-window-manager | **transform** | Full windowing/messaging framework atop P2 video. |
| **AN014** Coroutines in Propeller Assembly Language | **A** · coroutines-multitasking | **transform** | P1 PASM coroutine idiom → **P2 native multitasking + inline PASM** (P2 has hardware task support). **Strong app-note candidate.** |
| **AN015** Creating Schmitt-Triggered Inputs | **B** · schmitt-comparator | **transform** | P1 software/discrete Schmitt → **P2 smart-pin Schmitt/comparator modes** (built in natively). |
| **AN018** Communication with a PC Application | **E** · pc-host-comm | evolve | Host↔chip serial protocol; P2 serial/host comms (same concept). |
| **AN019** Stack Space | **A** · stack | evolve | Stack sizing/management; P2 Spin2 stack model. |

## Roll-up by domain (P1 app-note coverage)

| Domain | P1 app notes | Count |
|---|---|---|
| **A. Core compute model** | AN003, AN009, AN011, AN014, AN019 | **5** |
| **B. Smart Pins & I/O** | AN001, AN008, AN010, AN015 | 4 |
| **G. Displays & graphics** | AN004, AN005, AN013 *(one GUI series)* | 3 |
| **I. Storage & memory** | AN006, AN012 | 2 |
| **E. Comms & protocols** | AN018 *(AN007 2°)* | 1 |
| **F. Sensors & environment** | AN002 | 1 |
| **K. Dev tools & workflow** | AN007 | 1 |

## Signals for the roster (Phase 6)

- **Domain A is the densest P1 vein (5 notes), and it's transform-heavy** —
  coroutines→multitasking, counters→smart pins, plus multicore/timing/stack/data-
  structures. These are exactly the P2's steepest learning curve and have **no
  Quick Byte "show it" tier**, which makes them the strongest *guided-composition
  app-note* candidates. (Confirm against the QB + OBEX columns in #137.)
- **AN006 (FAT filesystem) is NOT a P2 gap** — OBEX already carries FAT32/SD
  drivers (Gadd 4269, Allen 4894) plus Stephen's flash filesystem (4261). The
  matrix must reflect this; it would otherwise false-flag a filesystem app note.
- **The GUI series (AN004/005/013)** is one multi-part arc, not three rows — if
  it becomes a P2 candidate it's a *series*, and it's ambitious (window manager
  on P2 video).
- **AN010 (mixed-voltage)** is an electrical-design topic with no clean spine
  home — parked at B·pin-electrical pending review; it may route to a *manual*
  hardware section rather than an app note.

> Feeds the coverage matrix (#137); routing each into its correct *form* (app
> note / manual / OBEX adoption / QB suggestion) happens in the roster (#138)
> via `artifact-placement-rubric.md`.
