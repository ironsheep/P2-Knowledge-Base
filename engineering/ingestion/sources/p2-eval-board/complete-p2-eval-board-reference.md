# P2 Eval Board Rev C (#64000) — Complete Reference

**Source:** `64000 Propeller 2 Eval Board Rev C Guide.pdf` (Parallax Inc.)
**Edition:** Document v2.0, 29/6/2020 — 17 pages. (Revision History on p.17 labels the Rev C
document "Version 3.0"; the page footer on every page reads "v2.0 29/6/2020". Both strings are
in the source — see *Source errata* below.)
**Hardware revision:** Eval Board Rev C · P2X8C4M64P**ES** Rev C silicon engineering sample
**Part number:** #64000
**Re-extraction:** 2026-08-24 — **re-extraction** (F-250): supersedes the lossy 2025-08-29 /
2025-09-02 PDF-era capture, which lost every numeral. Prior artifacts archived in `archive/`.
**Extraction tooling:** `pdf-ocr --force-ocr --deskew` (ocrmypdf/tesseract) → `pdftotext -layout`
for the body text; `camelot lattice` for the two ruled tables; **`pdf2md` (docling) run
page-by-page** over the OCR'd PDF (`pdf2md-stripped.md`); `pdftoppm` + visual page read for
every numeral-bearing page and for the figure-only pin maps.
**Type:** Hardware evaluation-board product guide (no firmware / no code listings).
**Trust:** 🏆 / GREEN — official Parallax hardware documentation.

> **Why this source needed forced OCR.** The #64000 PDF's *body* font does not map numerals:
> `pdftotext` returns the prose with every digit silently deleted ("The Propeller has cores, KB
> of hub RAM, and Smart I/O pins"). Its *table* font is complementary — it keeps digits and
> drops many lowercase letters. Every quantitative claim below is therefore **triple-validated**:
> OCR text ∩ the original text layer (whichever side it preserves) ∩ the rendered page image.
> Where the three disagree, the rendered page wins and the disagreement is recorded.

---

## Overview

The Propeller 2 Eval Board is designed for **experimentation and characterization** of the
Propeller 2 multicore microcontroller. Multiple ground points, power supplies, and power-enable
& breakout headers are included for testing and interfacing with standard test equipment. The
PCB is organized to keep each subsystem clearly defined in groups and spaced well apart, making
room for test probes.

The **eight I/O Pin Breakout Edge Headers** accommodate the 2×6 pass-through headers on eight
different accessory add-ons.

Source note: the guide describes an **engineering sample**, not a production chip ("Be aware
that this is an engineering sample and not a production chip").

---

## Key Specifications (p.2, verbatim values)

| Spec | Value |
|------|-------|
| Voltage input requirements | USB **5 VDC**, absolute maximum **5.5 VDC** |
| USB protection | current-limiter and short-circuit detection |
| Propeller 2 chip | **P2X8C4M64PES** (8 cogs, 512 KB hub RAM, 64 smart pins) |
| Non-volatile memory | **16 MB (128 Mb) SPI Flash** |
| Crystal | **20 MHz** SMT |
| Smart I/O pins | **64 accessible, 58 fully free**, grouped in **8 sets of 8** via headers |
| Smart I/O pin supply voltage | **3.3 V** |
| Core supply voltage | **1.8 V** |
| Input current limit — PC USB port | **500 mA** |
| Input current limit — AUX USB port | **2000 mA** |
| VDD power supply | **1.8 V up to 2 A**, **1 MHz** nominal switching frequency |
| VIO power supplies | **3.3 V up to 300 mA per 8 I/O pins** |
| Programming | Serial over micro-USB |
| USB programming / serial data speed | user selectable up to **3 Mbps** |
| Operating temperature | **−40 to +185 °F (−40 to +85 °C)** |
| PCB dimensions | **3.55″ × 3.55″** *(the source then prints "(90 x 90 cm)" — see errata)* |

### Feature list (p.2, verbatim)
- Propeller 2 multicore microcontroller engineering sample, **Rev C silicon approved for production**
- **20 MHz** crystal
- Adjustable operating frequency; **recommended maximum 180 MHz** clock
- **Overclocking possible beyond 300 MHz**
- **16 MB** SPI Flash memory
- **64** Smart I/O pins brought out to edge headers, with **58 fully free**
- Buffered LEDs on top **eight** I/O pins
- Onboard **1.8 V 2-Amp** switching regulator with short-circuit and over-current fault
  protection for P2 VDD, and brownout detection connected to Propeller reset
- Onboard LDO **3.3 V** regulators for P2 VIOs
- Power headers for current measurement and alternative voltage source injection
- Dual power inputs via **micro-USB** sockets; suitable for USB charger (not supplied) or host
  computer USB port connection
- Built-in **FTDI**-to-USB programming interface, with TX/RX activity indicator LED
- USB current limiters with short-circuit and over-current fault protection
- USB active and USB fault LEDs
- MicroSD card socket with power-cycle function when reset button is pressed
- WX compatible for programming the P2 over WiFi with the **WX WiFi SIP Module (#32420S —
  not included)**

---

## What's New for Rev C (p.3, verbatim)

- Production-approved P2X8C4M64P Engineering Sample Rev C silicon.
- **P0–P15 and P32–P47 are trace-length matched** for high-speed data experiments (such as HyperRAM).
- BOD (Brown Out Detection) is removed from the dip switch; instead Propeller **RESn is permanently
  connected to the 1.8 V regulator PG (Power Good) signal**, which holds the P2 in reset if the
  regulator voltage drops below **~1.5 V**.
- **USB RES is on the dip switch**, letting the user disconnect the USB reset (DTR) signal from RESn.
- The **5 V pin which was next to P30 has been removed**, and that pin is now unconnected.
- The **5 V pin which was next to P62 has been replaced with a RESET input** to the Propeller RESn.
- The unpopulated DTR/RESn pads which Rev B had (near the SD socket) have been removed.
- Improvements to the USB power circuit for edge-case fault protection.
- **WX WiFi compatible** — the **P56–P63** edge header works with the Parallax SIP WiFi module.

---

## The 20 numbered features (pp.4–13)

| # | Feature | Quantitative content |
|---|---------|----------------------|
| 1 | Propeller 2 P2X8C4M64P — Engineering Sample (Rev C Silicon) | 3rd edition; **8 cores, 512 KB hub RAM, 64 Smart I/O pins**; PNUT P2 **v34s** or greater recommended |
| 2 | LDO VIN Male Header | **2-pin**; connects the common **5 V** USB supply to the **3.3 V** LDO regulators powering VIO, microSD and flash. Power MUST be connected here for the P2 to operate |
| 3 | ACC HDR Male Header | **2-pin**; routes the common **5 V** USB supply to every 5 V pin on the edge headers. Shipped in the "OFF" position (jumper on the 5 V pin only). Certain accessory boards require 5 V, e.g. the USB accessory **#64006-ES(b)** |
| 4 | PC USB Port | microUSB; loads programs, serial-over-USB, supplies **5 V**. Protection disables the supply above **500 mA**. ACT (blue) LED blinks on traffic |
| 5 | USB Logic & Protection | Source auto-selected; **PC-USB limit 500 mA, AUX-USB limit 2000 mA** |
| 6 | VDD Power Supply | Switching buck regulator, **2 A at 1.8 V**; brown-out detection holds the P2 in reset while VDD is below **~1.5 V**. **VDD Male Header** is **2-pin**. *Important!* absolute maximum voltage set/connected to P2 VDD is **2.2 V** |
| 7 | Ground Test Posts | **Four**, one at each edge of the board |
| 8 | Crystal | **20 MHz** crystal + XO/XI pads. On-chip oscillator internal **9 pF** load capacitance. XO = **physical pin 50**, XI = **physical pin 51**. Overclocking: early unsupported experiments ran at **390 MHz** without significant heat rise; recommended maximum is **180 MHz**. Bottom layer is a continuous **4 oz** copper ground plane; **four mounting holes spaced 40 mm apart**, which could accommodate a **50 mm** fan or heatsink |
| 9 | AUX Power Header Pads (Customer Option) | 5V + GND, **0.1″** spaced; when used as an input the supply range is **4.5 V to 5.5 V** and **MUST NOT exceed 5.5 V**. Do NOT connect a source to both the USB socket and the 5 V pads at once |
| 10 | AUX USB Port | microUSB, **power input only**; a **2-Amp** rated device is recommended; protection disables the supply above **2 A**. Takes priority over PC-USB. The auxiliary pads sit *before* the protection circuit and keep sourcing power during a fault |
| 11 | I/O Pin Breakout Edge Headers (with 5 V output) | Each of the **64** smart I/O pins reaches an edge header in **groups of eight**. Each header also carries **two GND**, one **Vxxxx** output (from the corresponding **3.3 V** LDO) and optionally a **5 V** output (gated by the ACC HDR jumper) |
| 11a | I/O Pin Breakout Edge Headers (without 5 V output) | **Two** headers have no 5 V. **P24–P31**: the pin beside Vxxxx is **unconnected** (white silk square). **P56–P63**: that pin is **RES**, active low, wired to the P2 RESn circuit — ideal for a WiFi module (Parallax WX, `parallax.com/product/32420s`) |
| 12 | LED Bank | **Eight** LEDs via an LED buffer on **P56–P63**. P56–P63 LEDs are connected to the USB data and P2 memory signals, so they are especially active at power-up and after reset. **P56 and P57 are free by default** |
| 13 | Reset Button | Restarts the program and power-cycles the flash memory and microSD socket |
| 14 | LDO regulators for I/O Pin Voltage | Fixed **3.3 V** low-noise regulators. At the chip, each **4** I/O's have a dedicated supply connection (**V0003, V0407, V0811**, …). On the PCB these are brought out in groups of **8** (e.g. **V0815** = VIO for I/O pins 8 to 15) |
| 15 | Mounting Holes | **Four** plated holes attached to the ground plane |
| 16 | Mode Selection Switch Bank | **Four** dip switches: **USB RES**, **FLASH**, **P59 △**, **P59 ▽**. Usually all OFF on a new board. Only switch **one** of the P59 dip-switches ON |
| 17 | Flash Memory | SPI, **16 MB (128 Mbit)**, **W25Q128JVSIM** |
| 18 | microSD Card Socket | Hardwired to four P2 I/O pins — see *Source errata* for the P58/P59 conflict. Powered by the Common LDO, with an optional connection to **P57** to toggle power |
| 19 | Common LDO regulator | Fixed **3.3 V** low-noise; powers microSD + SPI flash and provides the common pull-up voltage for boot-mode features. **R803** is an unpopulated pad that would connect **P57** to the Common LDO enable pin; one option is to move **R802** to **R803** and install an **0402 100 kΩ** resistor at **R801**. Do not keep both R802 and R803 installed |
| 20 | LED Buffer | Octal line driver, high-impedance connections to **P56–P63**; drives the status LED **on when the P2 I/O signal line is low**. Because P2 I/O is high-impedance by default the LEDs are sensitive to objects near the top-left edge header. Those **8** I/O pins are not impacted by the LEDs by default |

---

## Boot Mode Selection table (p.12 — camelot lattice ∩ OCR ∩ page image)

The three switches are **FLASH**, **P59 △** (up-triangle) and **P59 ▽** (down-triangle).
*(The triangle glyphs are silkscreen symbols; OCR reads them as the letters "A" and "V".
The page image and the p.17 board silkscreen both show triangles.)*

| Boot Mode Selection | FLASH | P59 △ | P59 ▽ |
|---|---|---|---|
| Serial window of 60 seconds, default. (When SD card is NOT inserted) | OFF | OFF | OFF |
| Serial window of 60 seconds, overrides SPI Flash and SD card. | ON or OFF | ON | OFF |
| Serial window of 100 ms, then SPI flash. If SPI flash fails then serial window of 60 seconds. | ON | OFF | OFF |
| SPI flash only (fast boot), no serial window. If SPI flash fails then shutdown. | ON | OFF | ON |
| SD card with serial window on failure. If SD card fails then serial window of 60 seconds. | OFF | OFF | OFF |
| SD card only, no serial window. If SD card fails then shutdown. | OFF | OFF | ON |

Note (source): *"A switch is in the 'off' position when the actuator is pointing toward the
corresponding pcb label."*

---

## I/O Pin Assignments (pp.15–16 — camelot lattice ∩ OCR ∩ page image)

Source statement (p.15): *"Smart I/O pins P0–P55 are fully free; P56–P63 are routed to
peripheral circuits and/or have special functions related to Propeller 2 boot sequence
options."*

Every group carries the same electrical description:

> Smart I/O pins, **3.3 V** logic level, source or sink **30 mA per I/O pin**. On-board LDO
> regulator supplies **300 mA total**, shared by this I/O pin group and edge header pin Vxxxx.

| I/O Pin group | Edge-header VIO pin |
|---|---|
| P0-P7   | **V0007** |
| P8-P15  | **V0815** |
| P16-P23 | **V1623** |
| P24-P31 | **V2431** |
| P32-P39 | **V3239** |
| P40-P47 | **V4047** |
| P48-P55 | **V4855** |
| P56-P63 | **V5663** |

### Alternative functions for P56-P63

| Pin | microSD | SPI Flash | LED |
|---|---|---|---|
| P56 | No alternative function | — | Buffered LED |
| P57 | Routed to Common LDO enable pin (not connected by default, user option) | — | Buffered LED |
| P58 | microSD MISO (SDO) | Flash SPI DO | Buffered LED |
| P59 | microSD MOSI (SDI) | Flash SPI DI | Buffered LED |
| P60 | microSD CS | Flash SPI CLK | Buffered LED |
| P61 | microSD CLK | Flash SPI CS | Buffered LED |
| P62 | PC-USB RXD (P2 TXD) | — | Buffered LED |
| P63 | PC-USB TXD (P2 RXD) | — | Buffered LED |

### Other pins

| Pin | Description |
|---|---|
| TEST | MUST be connected to Ground for P2 to operate correctly. |
| XO | Xtal Out for clock source. (Connected to **20 MHz** crystal oscillator and XO header pad) |
| XI | Xtal In for clock source. (Connected to **20 MHz** crystal oscillator and XI header pad) |
| RESn | MUST be pulled up, typically with **10 K** resistor. P2 will reset when RESn driven low. |
| GND | Ground pad is under the chip and must be connected to PCB ground. Provides common signal and supply-voltage ground, and an important path for heat dissipation. Connection to a solid ground plane under the P2 chip and on an external layer recommended. |

---

## Figure-carried pin maps (page images — the only place these appear)

These are **read from the rendered page**, not from any text layer. Recorded here because the
edge-header pin *order* exists nowhere else in the document.

**P56–P63 edge header (p.10 photo)** — 2×6, as silkscreened:

| left | right |
|---|---|
| GND | GND |
| P56 | P57 |
| P58 | P59 |
| P60 | P61 |
| P62 | P63 |
| **RES** | **V5663** |

**P40–P47 edge header (p.9 photo)** — the "with 5 V output" pattern:

| left | right |
|---|---|
| V4047 | 5V |
| P47 | P46 |
| P45 | P44 |
| P43 | P42 |
| P41 | P40 |
| GND | GND |

**P24–P31 edge header (p.9 photo)** — the "without 5 V output" pattern:

| left | right |
|---|---|
| V2431 | *(white silk square — unconnected)* |
| P31 | P30 |
| P29 | P28 |
| P27 | P26 |
| P25 | P24 |
| GND | GND |

Header orientation varies by position on the board — the p.17 silkscreen shows the P0–P7 header
as GND/GND · P0/P1 · P2/P3 · P4/P5 · P6/P7 · 5V/V0007, i.e. the same 12 pins with the GND end
and the power end swapped. The invariant per header is: **2 × GND, 8 × I/O, 1 × Vxxxx, and one
of {5 V, unconnected (P24–P31), RES (P56–P63)}**.

**Propeller 2 Physical Pins (p.14 diagram)** — the 100-pin chip pinout is reproduced in this
guide. Chip-level pin numbering is a *silicon* fact and the silicon sources are its authority;
recorded here only as corroboration. Read from the page: pin 1 = TEST, 2 = VDD, 3 = P0, 4 = P1,
5 = **V0003**, 6 = P2, 7 = P3, 8 = VDD, 9 = P4, 10 = P5, 11 = **V0407**, 12 = P6, 13 = P7,
14 = VDD, 15 = P8, 16 = P9, 17 = **V0811**, 18 = P10, 19 = P11, 20 = VDD, 21 = P12, 22 = P13,
23 = **V1215**, 24 = P14, 25 = P15 …; 89 = P56, 90 = P57, 91 = **V5659**, 92 = P58, 93 = P59,
94 = VDD, 95 = P60, 96 = P61, 97 = **V6063**, 98 = P62, 99 = P63, 100 = RESN. This corroborates
§14's statement that the *silicon* groups VIO per **four** I/O pins, while the *board* brings
them out in groups of eight.

---

## PCB Dimensions (p.17 drawing)

The board outline is an **octagon** (a square with chamfered corners). Labelled dimensions on
the drawing, read from the page:

| Label | What it dimensions |
|---|---|
| **3.55 in** | overall board width (matches the p.2 key spec) |
| **2.75 in** | length of the flat top edge (between the two chamfers) |
| **2.75 in** | length of the flat left edge |
| **0.5657 in** | bottom-left chamfer |
| **1.5748 in** | bottom-right chamfer (= 40.00 mm) |
| **2.2271 in** | vertical location dimension on the right-hand side |
| **0.126 in** | vertical offset between the two right-hand hole centres |

The **40 mm mounting-hole spacing** is stated in §8 body text only; the drawing does not carry a
labelled hole-to-hole dimension, so the 40 mm figure rests on the prose, not on the drawing.

---

## Source errata — internal inconsistencies in the #64000 guide itself

These are the source contradicting itself, verified on the rendered pages. They are **not**
extraction defects and must not be silently "cleaned up" downstream.

1. **microSD data-pin direction: §18 and the p.15 table disagree.**
   §18 (p.12) lists *"P58 - DI/CD (data in and card detect); P59 - DO (data out); P60 - /CS
   (active low chip select); P61 - CLK (clock)"*. The p.15 alternative-function table lists
   *"P58 microSD MISO (SDO); P59 microSD MOSI (SDI); P60 microSD CS; P61 microSD CLK"*.
   P60/P61 agree; **P58 and P59 are swapped in direction between the two places**. Both readings
   are confirmed against the rendered pages and against the original text layer (whose table
   font preserved the fragments " D MI O ( DO)" / " D MO I ( DI)"). The guide does not resolve
   it. → filed as **F-328**.
2. **"58 fully free" vs "P0–P55 are fully free".** p.2 says 64 accessible / **58** fully free
   (twice). p.15 says **P0–P55** are fully free, with P56–P63 routed to peripherals. §12 adds a
   third statement: *"P56 and P57 are free by default"*. *(Observation, not the source's: the
   arithmetic 56 + 2 = 58 would reconcile them; the guide never says so.)* State the source's
   own wording; do not settle on a single number here.
3. **"3.55″ × 3.55″ (90 x 90 cm)".** The parenthetical unit is wrong in the source — 3.55 in is
   90 mm, not 90 cm. Quote the inch figure; the metric parenthetical is a source typo.
4. **Document version string.** Every page footer reads "v2.0 29/6/2020"; the Revision History
   on p.17 reads *"Version 3.0: Supports the P2-ES Rev C silicon and the Eval Board Rev C."*
5. **Chip part number.** The p.2 key spec and the p.4 diagram callout read **P2X8C4M64PES**;
   the p.4 section heading and the p.3 bullet read **P2X8C4M64P**. The board silkscreen (p.17)
   reads **P2X8C4M64P**.
6. **"Rev B" vs "Rev B/C" Google Document.** §8 refers the reader to the "Propeller 2 (Rev B
   Silicon) Google Document"; §1, p.14 and p.15 refer to the "(Rev B/C Silicon)" one.
7. **OCR-only artefact, recorded so it is not mistaken for source text:** the p.16 RESn row
   OCR'd as "wnen"; the page reads "when".

---

## Extraction gaps

**None for text, tables, or the quantitative content of the figures.** All 17 pages were read
against the rendered page image; every numeral-bearing page (1–13, 15–17) matched the OCR text,
and the two ruled tables matched `camelot lattice`.

Not attempted / not present:
- **No code listings** in this guide — nothing for `pnut_ts` to validate.

**`pdf2md` (docling) — the fourth leg, and how it was obtained.** Whole-document runs were
OOM-killed (exit 137) on the OCR'd PDF, on the original PDF, and even on a single extracted
page, with ~10 GB of the container's 12.9 GB committed by other work. **Splitting the PDF with
`pdfseparate` and running docling one page at a time succeeded for all 17 pages** — output at
`pdf2md-stripped.md` (base64 image payloads stripped). It agrees with the OCR text and the
camelot tables throughout, including the p.15 alternative-function table and the p.12 boot-mode
table, and reproduces the same OCR artefacts (`P59 A`/`P59 V` for the triangles, "wnen"),
confirming those as OCR-side and not source-side. *Recorded because the first attempt's failure
was a capability limit, not a content gap — and because "split the document" is what got past
it.*
