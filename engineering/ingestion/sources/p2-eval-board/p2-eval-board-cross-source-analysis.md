# P2 Eval Board Cross-Source Analysis

**Source Document**: 64000 Propeller 2 Eval Board Rev C Guide  
**Author**: Parallax Inc.  
**Version**: Rev C  
**Created**: 2025-09-02 · **Corrected against the repaired source 2026-08-24 (F-250)**
**Purpose**: Connect p2-eval-board source to central analysis hub

> ⚠️ **This document was written on a digit-free extraction.** It was drafted from an
> extraction in which `pdftotext` had silently dropped every numeral, and several of its
> hardware claims turned out to describe a board the #64000 guide does not describe. The
> unsupported claims are struck through and corrected in place below, against the 2026-08-24
> forced-OCR re-extraction. **The authority for this source is now
> `complete-p2-eval-board-reference.md`**, not this file.

---

## 📊 Source Contribution Summary

### Primary Value
- **Integrated development platform** - Complete P2 system
- **Built-in peripherals** - buffered LED bank (P56–P63), reset button, 4-position mode dip
  switch, eight 2×6 I/O breakout edge headers
- **Programming** - built-in FTDI USB-serial over the PC micro-USB port; the P56–P63 edge
  header also accepts the Parallax WX WiFi SIP module (#32420S, not included) for wireless
  programming. ~~"Dual programming — USB and Prop Plug support"~~ — the #64000 guide **never
  mentions a Prop Plug**
- **Part number**: #64000
- **Alternative to Edge** ecosystem

### Coverage Assessment
- **Re-extracted 2026-08-24** (forced OCR). ~~"100% Complete"~~ — that figure was asserted over
  an extraction with no numerals in it. Measured coverage is in
  `p2-eval-board-rev-c-complete-extraction-audit.md`.
- **Trust Level**: 🟢 GREEN - Official Parallax documentation

---

## 🔄 Cross-Source Connections

### Development Platform Comparison
*Eval Board vs Edge Ecosystem*

| Feature | P2 Eval Board (THIS) | Edge + Breakout |
|---------|---------------------|-----------------|
| **Integration** | All-in-one | Modular |
| **P2 Chip** | Soldered | Edge Module |
| **Peripherals** | Built-in LEDs/switches | External |
| **Cost** | Single purchase | Module + carrier |
| **Flexibility** | Fixed configuration | Swappable |

### Questions This Source Answers
*From central-analysis/cross-source-qa/*

1. **Integrated Development Choice**
   - Quick start option? → P2 Eval Board
   - Built-in peripherals? → **8 buffered LEDs on P56–P63**, a reset button, and a 4-position
     mode dip switch (USB RES · FLASH · P59 △ · P59 ▽). There are **no general-purpose user
     pushbuttons** on this board
   - Programming options? → PC micro-USB (built-in FTDI), or WX WiFi module on the P56–P63
     header. ~~"or Prop Plug"~~ — not in this source

2. **Learning Platform**
   - Best for education? → Eval board simplicity
   - Example circuits? → Built-in demonstrations
   - Expansion options? → Add-on boards available

### Questions This Source Raises
*Contributed to central-analysis*

1. **Platform Selection**
   - When Eval vs Edge? → Fixed vs modular needs
   - Upgrade path? → From Eval to Edge
   - Production transition? → Eval to custom PCB

2. **Peripheral Utilization**
   - LED/switch pin conflicts?
   - Peripheral disable options?
   - Power consumption with all active?

---

## 📈 Knowledge Gaps Analysis

### Gaps This Source FILLS
✅ **Complete Development Solution**:
- Integrated platform specifications
- Built-in peripheral documentation
- Power supply requirements
- Programming interface details
- Physical layout and dimensions

✅ **Educational Platform**:
- LED indicators for debugging (buffered, P56–P63; the buffer drives the LED when the P2 pin is
  **low**)
- ~~Switch inputs for interaction~~ — the only switches are the reset button and the 4-position
  **mode selection** dip bank; they are not general-purpose inputs
- Header access to all 64 I/O pins, in eight 2×6 edge-header groups of eight
- ~~VGA/HDMI capability mentioned~~ — **not in this source.** The #64000 guide never mentions
  VGA, HDMI, video, or resistor DACs

### Gaps This Source REVEALS
❌ **Software Examples**:
- No demo code for built-in peripherals
- LED/switch example code missing
- Peripheral test programs absent
- Board validation code not provided

---

## 🎯 Trust Zone Assessment

### Trust Level: 🟢 GREEN (ABSOLUTE)
- **Publisher**: Parallax Inc.
- **Type**: Official hardware guide
- **Version**: Rev C (current)
- **Status**: Active product

### Conflicts
- ✅ P2 chip specs match Silicon Doc
- ✅ Pin assignments documented
- ✅ Compatible with add-on boards
- ✅ Programming specs standard
- ⚠️ **Internal to the source:** §18 and the p.15 table disagree on microSD P58/P59 direction;
  "58 fully free" (p.2) vs "P0–P55 fully free" (p.15). Full list in the extraction audit,
  Pass 3. Routed to the corrections register as **F-328**.

---

## 📋 Technical Specifications

_Corrected 2026-08-24 against the forced-OCR re-extraction. Struck-through lines are what this
file asserted from the digit-free capture._

### Board Features
- **P2 Chip**: Soldered **P2X8C4M64PES** — Rev C silicon **engineering sample**, "approved for
  production" but explicitly "not a production chip"
- **LEDs**: 8, buffered, on **P56–P63**. Only **P56 and P57 are free by default**; P58–P63 are
  shared with the microSD/flash and PC-USB signals, so those LEDs are active at power-up and
  after reset. ~~"8 user-controllable"~~ overstates it
- **Switches**: reset button; 4-position **mode selection** dip bank (USB RES · FLASH · P59 △ ·
  P59 ▽). ~~"user inputs"~~ — there are none
- **Headers**: eight **2×6** edge headers, 8 I/O + 2 GND + 1 Vxxxx + one of {5 V / unconnected
  (P24–P31) / RES (P56–P63)}
- **Power**: ~~"Barrel jack or USB"~~ — **there is no barrel jack.** Two **micro-USB** sockets
  (PC-USB 500 mA, AUX-USB 2000 mA), plus optional 5V/GND AUX header **pads** (0.1″ spaced,
  4.5–5.5 V, never simultaneously with the AUX-USB socket)

### Expansion Capability
- **Add-on boards**: #64006 series; the guide names **#64006-ES(b)** as an example that needs
  the ACC HDR 5 V jumper
- ~~**Proto area**: Breadboard section~~ — **fabricated.** The #64000 has no prototyping area
- **Headers**: 2×6 edge headers for add-ons; the AUX power **pads** are the 0.1″-spaced feature
- ~~**VGA/HDMI**: Supported with resistor DACs~~ — **fabricated.** Not in this source

### Part Numbers (as stated in the #64000 guide)
- **#64000** - this eval board
- **#64006-ES(b)** - the USB accessory example that requires 5 V at the edge headers
- **#32420S** - Parallax WX WiFi SIP Module (not included)
- **W25Q128JVSIM** - the 16 MB (128 Mbit) SPI flash device
- ~~#32201 - Prop Plug (optional)~~ / ~~USB cable included~~ — **neither appears in this
  source.** The guide says a USB charger is "not supplied"

---

## 🔗 Related Sources

### Platform Alternatives
1. **Integrated** → P2 Eval Board (THIS)
2. **Modular** → Edge + Breakout
3. **Compact** → Edge + Mini Breakout
4. **Prototype** → Edge + Breadboard

### Complements
- **p2-eval-add-on-boards** - Expansion options
- **Smart Pins** - I/O capabilities
- **PASM2/Spin2** - Programming guides

### Unique Documentation
- ~~**p2-hardware-manual-complete-extraction-audit.md** also in this directory~~ — **stale.**
  That file was mis-filed here and was relocated to `sources/p2-hardware-manual/` on
  2026-06-22. It never implied anything about the #64000 guide's scope.

---

## 📊 Unique Insights

1. **Characterization-first design** - the guide's own framing is "experimentation and
   characterization": ground test posts at all four edges, breakout headers for current
   measurement and external supply injection, subsystems spaced apart for probes
2. **Educational Focus** - Built-in learning aids
3. **Fixed Configuration** - Predictable development
4. **Rev C Maturity** - Refined design (BOD now hard-wired to the 1.8 V regulator PG line;
   P0–P15 / P32–P47 trace-length matched)
5. **Programming** - built-in FTDI USB-serial, or WX WiFi on the P56–P63 header
   ~~"USB convenience or Prop Plug"~~ — no Prop Plug in this source

---

## ⚠️ Documentation Notes

### Content Coverage
- **Hardware specs** - Complete
- **Board layout** - Documented
- **Peripheral details** - LEDs, switches defined
- **Power requirements** - Specified

### Missing Software Context
- Demo programs not included
- Peripheral test code absent
- Board validation routines missing
- Example projects not provided

---

## ✅ Verification Status

### Hardware Documentation
- Board specifications: ✅ Complete
- Peripheral mapping: ✅ Documented
- Power details: ✅ Provided
- Physical layout: ✅ Illustrated
- Expansion options: ✅ Referenced

### Software Support
- Example code: ❌ None provided
- Test programs: ❌ Missing
- Peripheral demos: ❌ Absent
- Validation suite: ❌ Not included

---

## 🔴 Platform Selection Guide

**Choose P2 Eval Board when:**
- Starting P2 development
- Teaching/learning environment
- Built-in peripherals needed
- Single-board simplicity preferred
- Quick prototyping required

**Choose Edge Ecosystem when:**
- Modular flexibility needed
- Production path planned
- Custom carrier design intended
- Multiple configurations required
- Component reuse important

---

*Cross-source analysis completed: 2025-09-02*  
*The integrated alternative to Edge ecosystem for P2 development*