# Propeller 2 (P2X8C4M64P) Datasheet (2022/11/01) — All Structural Tables

**Source PDF:** `engineering/ingestion/external-inputs/archive/Propeller2-P2X8C4M64P-Datasheet-20221101.pdf`
— 50 pages, 612x792 pt letter, Skia/PDF m109 Google Docs Renderer (`pdfinfo`, 2026-08-24).
**Extraction:** 2026-08-24, **four** independent paths run and reconciled cell-by-cell. No OCR was needed
or used — the PDF carries a complete text layer.

| Path | Tool | What it gives |
|---|---|---|
| **A** | `camelot lattice -p all -f csv` | **45 ruled tables**; true cell/row/column structure, including multi-line cells |
| **B** | `pdf-layout` (`pdftotext -layout`) → `p2-datasheet-text.txt` | x-position-preserving plain text; correct **vertical** alignment and superscript separation |
| **C** | `pdftoppm` page render, read visually | tie-breaker of record for every disputed cell |
| **D** | `pdf2md` (docling) | a fourth, ML-layout path; also recovers the document's **own Table of Contents**, which is what settles the page-number dispute below |

**Every reconciliation below was decided by at least three of the four paths agreeing**, and every
one of the four agrees on the DC and AC Characteristics content.

**Page numbers below are the PDF's own printed page numbers**, which equal the physical page index
in this document (verified: p.47's footer reads "Page 47").

**The datasheet's own Table of Contents settles where the electrical tables are** (recovered by
path D, verbatim):

```
| SYSTEM CHARACTERISTICS               | 47 |
| Absolute Maximum Electrical Ratings  | 47 |
| DC Characteristics                   | 47 |
| AC Characteristics                   | 48 |
| PACKAGING                            | 49 |
| CHANGE LOG                           | 50 |
```

That is the document telling you, not an extractor guessing. **DC = pp.47-48, AC = p.48.**

Pages **36-46** are the PASM2 instruction listing; those tables live in
`pasm2-complete-instruction-tables.md` and are not duplicated here.
Pages **26-32** are the I/O pin circuit and its equivalent schematics — **figures, not tables** — and
are catalogued in `assets/images-20250906/`. See §*Pages 26-32* below.

---

## Where the paths disagreed — every reconciliation, named

**This section is the point of the exercise.** Path A alone would have shipped ten wrong smart-pin
mode numbers. Path B alone would have lost the column structure. Neither is trustworthy unsupervised.

| # | Table | Path A (`camelot lattice`) produced | What the other paths show | Adopted |
|---|---|---|---|---|
| R1 | **(S) Smart Pin Modes**, pp.34-35 | 6-digit values `001001` `001011` `001101` `001111` `010001` `010011` `110111` `111001` `111101` | **5-bit value + superscript footnote `¹`**: `00100¹` `00101¹` `00110¹` `00111¹` `01000¹` `01001¹` `11011¹` `11100¹` `11110¹` | **B/C/D.** `%SSSSS` is a 5-bit field; footnote 1 reads *"OUT signal overridden"*. Confirmed by reading the rendered pp.34-35 (path C) and independently by `pdf2md`, which emits `00100 1` etc. with the marker separated (path D). |
| R2 | **(S) Smart Pin Modes**, p.34 | `01010  1` split across two output lines | `01010¹` — PWM switch-mode power supply | **B/C** |
| R3 | **PLL Setting `%PPPP`**, p.18 | value column linearized to `0 1 2 3 4 5 6 7 8 9 1 / 0 / 11 / 12 …` | 16 values `0`..`15` paired to `VCO / 2` .. `VCO / 1` | **B** |
| R4 | **AC Characteristics `Cin` Typ**, p.48 | `2 2 / 15 / 30` (3 lines for 4 modes) | `2 / 2 / 15 / 30` — one per mode | **B/C/D** |
| R5 | **AC Characteristics `Freq` Typ**, p.48 | `20 / 24 / - - / 180 2` | `20 / 24 / - / - / 180²` — Direct-drive and Crystal have no Typ | **B/C/D** |
| R6 | **Pin Mode Legend**, p.24 | three sub-legends interleaved into one cell | three separate legends (C · I/O · HHH/LLL) plus a definitions column | **B** |
| R7 | **(M) Pin Mode**, p.24 | single-value columns space-joined (`0 0 0 0 0 0 0 0`) inside one cell | 24 discrete rows | **A structure + B values**, then machine-verified: all 204 non-empty cells (of 24x9) found verbatim in path B's independent text (negative control: a fabricated value `ADC, Pin 7x` is correctly reported absent). |
| R8 | **Special-purpose Registers**, p.14 | `INA1` and `INB2` in the Name column | `INA` and `INB` with superscript footnotes ¹ ² | **B/C.** Same fused-superscript class as R1. Page 14 was rendered and read: the cells are `INA¹` / `INB²`, and the page's own footnotes are ¹ *"Also debug interrupt call address"* · ² *"Also debug interrupt return address"*. The Hardware Manual's DOCX (Table 9) carries the identical fusion, so this reconciliation applies to both sources. |

---

## Page 1 — Part Number Legend

| Part Number Legend |  |  |  |
|---|---|---|---|
| P2X | 8C | 4M | 64P |
| Propeller 2 | 8 cogs (processors) | 4 Mbit Hub RAM (512 KB) | 64 smart I/O pins |

## Page 1 — RAM Memory Configuration  ‹broken-table #1 "Memory Configuration"›

| Propeller 2 (P2X8C4M64P) RAM Memory Configuration |  |  |  |  |
|---|---|---|---|---|
| Region | Depth | Width | Program Counter<br>Address Range (Hex) | PASM Instruction D/S<br>Address Range (Hex) |
| Cog "Register" RAM | 512 | 32 bits | $00000..$001FF | $000..$1FF |
| Cog "Lookup" RAM | 512 | 32 bits | $00200..$003FF | $000..$1FF |
| Hub RAM | 524,288 | 8 bits | $00400..$7FFFF | $00000..$7FFFF |

## Page 6 — Pin Descriptions  ‹broken-table #2›

> The prior note filed this as "Page 5". The **section** *Pin Descriptions* begins on p.5 (the TOC
> agrees: `Pin Descriptions | 5`) and carries three bullets about the pinout; the **table** is on
> p.6. Both statements are right about different things — recorded so the discrepancy is not
> re-opened.

| Pin Descriptions |  |  |  |
|---|---|---|---|
| Pin Name | Direction | V (typ) | Description |
| GND | - | 0 | Exposed Pad (underside of chip); ground for core and smart pins –  internally<br>connected to exposed pad. Connect to ground plane for thermal dissipation. |
| TEST | I | 0 | Tied to ground |
| VDD | - | 1.8 | Core power |
| P0-63 | I/O | 0 to 3.3 | Smart pins.  P58-P63 serve in the boot process, then general purpose after. |
| Vxxyy | - | 3.3 | Power for smart pins in groups of 4: Pxx through Pyy |
| XO | O | - | Crystal Output. Provides feedback for an external crystal, or may be left<br>disconnected depending on CLK Register settings. No external resistors or<br>capacitors are required. |
| XI | I | - | Crystal Input. Can be connected to the output of crystal/oscillator pack (with XO<br>left disconnected), or to one leg of crystal (with XO connected to the other leg of<br>crystal or resonator) depending on CLK Register settings. No external resistors<br>or capacitors are required. |
| RESN | I | 0 | Reset (active low). When low, resets the Propeller: all cogs disabled and I/O<br>pins floating. Propeller restarts 3 ms after RESn transitions from low to high.<br>Connect to a resistor to pull up to 3.3 V. |

## Page 13 — Special-purpose Registers $1F0..$1F7

| Address | Name | Purpose |
|---|---|---|
| $1F0<br>$1F1<br>$1F2<br>$1F3<br>$1F4<br>$1F5<br>$1F6<br>$1F7 | RAM / IJMP3<br>RAM / IRET3<br>RAM / IJMP2<br>RAM / IRET2<br>RAM / IJMP1<br>RAM / IRET1<br>RAM / PA<br>RAM / PB | Interrupt call address for INT3<br>Interrupt return address for INT3<br>Interrupt call address for INT2<br>Interrupt return address for INT2<br>Interrupt call address for INT1<br>Interrupt return address for INT1<br>CALLD-imm return, CALLPA parameter, or LOC address<br>CALLD-imm return, CALLPB parameter, or LOC address |

## Page 14 — Special-purpose Registers $1F8..$1FF

| Address | Name | Purpose |
|---|---|---|
| $1F8<br>$1F9<br>$1FA<br>$1FB<br>$1FC<br>$1FD<br>$1FE<br>$1FF | PTRA<br>PTRB<br>DIRA<br>DIRB<br>OUTA<br>OUTB<br>INA1<br>INB2 | Pointer A to Hub RAM<br>Pointer B to Hub RAM<br>Output enables for P31..P0<br>Output enables for P63..P32<br>Output states for P31..P0<br>Output states for P63..P32<br>Input states for P31..P0<br>Input states for P63..P32 |

> The extracted names `INA1` / `INB2` are **`INA` / `INB` with a superscript footnote marker fused
> on** (reconciliation R8 below). Page 14's footnotes read, verbatim:
> ¹ *"Also debug interrupt call address"* · ² *"Also debug interrupt return address"*.

## Page 15 — PASM2 Execution Regions

| PC Address | Instruction Source | Memory Width | PC Increment |
|---|---|---|---|
| $00000..$001FF | Cog Register RAM | 32 bits | 1 |
| $00200..$003FF | Cog Lookup RAM | 32 bits | 1 |
| $00400..$7FFFF | Hub RAM | 8 bits | 4 |

## Page 18 — Clock Mode Settings  ‹broken-table #8›

The system clock is configured by the running application with `HUBSET`:

```
HUBSET     ##%0000_000E_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS      'set clock mode
```

*(verbatim from p.18; this line plus the three tables below **is** broken-table #10 "HUBSET Bit Fields")*

### %E / %DDDDDD / %MMMMMMMMMM / %PPPP — PLL Setting

| PLL Setting | Value | Effect | Notes |
|---|---|---|---|
| %E | 0/1 | PLL off/on | XI input must be enabled by %CC. Allow 10ms for<br>crystal+PLL to stabilize before switching over to PLL clock<br>source. |
| %DDDDDD | 0..63 | 1..64 division of XI pin<br>frequency | This divided XI frequency feeds into the phase-frequency<br>comparator's 'reference' input. |
| %MMMMMMMMMM | 0..1023 | 1..1024 division of<br>VCO frequency | This divided VCO frequency feeds into the<br>phase-frequency comparator's 'feedback' input. This<br>frequency division has the effect of multiplying the divided<br>XI frequency (per %DDDDDD) inside the VCO. The VCO<br>frequency should be kept within 100 MHz to 200 MHz. |
| %PPPP | 0<br>1<br>2<br>3<br>4<br>5<br>6<br>7<br>8<br>9<br>10<br>11<br>12<br>13<br>14<br>15 | VCO / 2<br>VCO / 4<br>VCO / 6<br>VCO / 8<br>VCO / 10<br>VCO / 12<br>VCO / 14<br>VCO / 16<br>VCO / 18<br>VCO / 20<br>VCO / 22<br>VCO / 24<br>VCO / 26<br>VCO / 28<br>VCO / 30<br>VCO / 1 | This divided VCO frequency is selectable as the system clock when SS = %11. |

### %CC — Crystal / XI-XO configuration

| %CC | XI status | XO status | XI / XO impedance | XI / XO loading caps |
|---|---|---|---|---|
| %00 | ignored | float | Hi-Z | OFF |
| %01 | input | 600-ohm drive | 1M-ohm | OFF |
| %10 | input | 600-ohm drive | 1M-ohm | 15pF per pin |
| %11 | input | 600-ohm drive | 1M-ohm | 30pF per pin |

### %SS — Clock source select

| %SS | Clock Source | Notes |
|---|---|---|
| %11 | PLL | CC != %00 and E=1, allow 10ms for crystal+PLL to stabilize before switching to PLL |
| %10 | XI | CC != %00, allow 5ms for crystal to stabilize before switching to XI pin |
| %01 | RCSLOW | ~20 kHz, can be switched to at any time, low-power |
| %00 | RCFAST | 20+ MHz (nominally ~24 MHz) can be switched to at any time— used on boot up. |

## Page 21 — I/O Pin Registers

| Register | Cog Address | Purpose |
|---|---|---|
| DIRA | $1FA | Output enable bits for P0..P31 (active high) |
| DIRB | $1FB | Output enable bits for P32..P63 (active high) |
| OUTA | $1FC | Output state bits for P0..P31 (corresponding DIRA bit must be high to enable output) |
| OUTB | $1FD | Output state bits for P32..P63 (corresponding DIRB bit must be high to enable output) |
| INA | $1FE | Input state bits for P0..P31 |
| INB | $1FF | Input state bits for P32..P63 |

## Page 21 — Special Pin Instructions

| Instructions | Purpose |
|---|---|
| DIRL/DIRH/DIRC/DIRNC/DIRZ/DIRNZ/DIRRND/DIRNOT {#}D | Affect pin D bit in DIRx |
| OUTL/OUTH/OUTC/OUTNC/OUTZ/OUTNZ/OUTRND/OUTNOT {#}D | Affect pin D bit in OUTx |
| FLTL/FLTH/FLTC/FLTNC/FLTZ/FLTNZ/FLTRND/FLTNOT {#}D | Affect pin D bit in OUTx, clear bit in DIRx |
| DRVL/DRVH/DRVC/DRVNC/DRVZ/DRVNZ/DRVRND/DRVNOT {#}D | Affect pin D bit in OUTx, set bit in DIRx |
| TESTP {#}D WC/WZ/ANDC/ANDZ/ORC/ORZ/XORC/XORZ | Read pin D bit in INx and affect C or Z |
| TESTPN {#}D WC/WZ/ANDC/ANDZ/ORC/ORZ/XORC/XORZ | Read pin D bit in !INx and affect C or Z |

## Page 23 — (A) PIN or (B) ADJ Input Selector

| %AAAA<br>%BBBB | Selection |
|---|---|
| 0xxx | true (default) |
| 1xxx | inverted |
| x000 | this pin's read state (default) |
| x001 | relative +1 pin's read state |
| x010 | relative +2 pin's read state |
| x011 | relative +3 pin's read state |
| x100 | this pin's OUT bit from cogs |
| x101 | relative -3 pin's read state |
| x110 | relative -2 pin's read state |
| x111 | relative -1 pin's read state |

## Page 23 — (F) PIN and ADJ Logic/Filtering

| %FFF | Logic/Filter |
|---|---|
| 000 | A, B (default) |
| 001 | A AND B, B |
| 010 | A OR  B, B |
| 011 | A XOR B, B |
| 100 | A, B, both filtered using global filt0 settings |
| 101 | A, B, both filtered using global filt1 settings |
| 110 | A, B, both filtered using global filt2 settings |
| 111 | A, B, both filtered using global filt3 settings |

## Page 24 — (M) Pin Mode  ‹broken-table #3 "Smart Pin Mode Configuration"›

`WRPIN` D-operand format (p.23): `%AAAA_BBBB_FFF_MMMMMMMMMMMMM_TT_SSSSS_0`

| M[12:0] | Input | Pin Output ¹ | CIOHHHLLL | OE ² | DAC | ADC | ADC Mode | Comparator |
|---|---|---|---|---|---|---|---|---|
| 0000_CIOHHHLLL | Pin Logic | OUT | CIOHHHLLL | DIR | 0 | 0 |  | 0 |
| 0001_CIOHHHLLL | Pin Logic | Input | CIOHHHLLL | DIR | 0 | 0 |  | 0 |
| 0010_CIOHHHLLL | Adj Logic | Input | CIOHHHLLL | DIR | 0 | 0 |  | 0 |
| 0011_CIOHHHLLL | Pin Schmitt | OUT | CIOHHHLLL | DIR | 0 | 0 |  | 0 |
| 0100_CIOHHHLLL | Pin Schmitt | Input | CIOHHHLLL | DIR | 0 | 0 |  | 0 |
| 0101_CIOHHHLLL | Adj Schmitt | Input | CIOHHHLLL | DIR | 0 | 0 |  | 0 |
| 0110_CIOHHHLLL | Pin > Adj | OUT | CIOHHHLLL | DIR | 0 | 0 |  | Pin > Adj |
| 0111_CIOHHHLLL | Pin > Adj | Input | CIOHHHLLL | DIR | 0 | 0 |  | Pin > Adj |
| 100000_OHHHLLL | ADC, GND | OUT | 10OHHHLLL | DIR | 0 | 1 | 000 | 0 |
| 100001_OHHHLLL | ADC, Vxxyy | OUT | 10OHHHLLL | DIR | 0 | 1 | 001 | 0 |
| 100010_OHHHLLL | ADC, float | OUT | 10OHHHLLL | DIR | 0 | 1 | 010 | 0 |
| 100011_OHHHLLL | ADC, Pin 1x | OUT | 10OHHHLLL | DIR | 0 | 1 | 011 | 0 |
| 100100_OHHHLLL | ADC, Pin 3.16x | OUT | 10OHHHLLL | DIR | 0 | 1 | 100 | 0 |
| 100101_OHHHLLL | ADC, Pin 10x | OUT | 10OHHHLLL | DIR | 0 | 1 | 101 | 0 |
| 100110_OHHHLLL | ADC, Pin 31.6x | OUT | 10OHHHLLL | DIR | 0 | 1 | 110 | 0 |
| 100111_OHHHLLL | ADC, Pin 100x | OUT | 10OHHHLLL | DIR | 0 | 1 | 111 | 0 |
| 10100_DDDDDDDD | ADC, Pin 1x 3 | DAC 990 Ω, 3.3 V | 10xxxxxxx | 0 | DIR | OUT | 011 | 0 |
| 10101_DDDDDDDD | ADC, Pin 1x 3 | DAC 600 Ω, 2.0 V | 10xxxxxxx | 0 | DIR | OUT | 011 | 0 |
| 10110_DDDDDDDD | ADC, Pin 1x 3 | DAC 123.75 Ω, 3.3 V | 10xxxxxxx | 0 | DIR | OUT | 011 | 0 |
| 10111_DDDDDDDD | ADC, Pin 1x 3 | DAC 75 Ω, 2.0 V | 10xxxxxxx | 0 | DIR | OUT | 011 | 0 |
| 1100_CDDDDDDDD | Pin > D | OUT, 1.5 kΩ | C00001001 | DIR | 0 | 0 |  | Pin > D |
| 1101_CDDDDDDDD | Pin > D | !Input, 1.5 kΩ | C01001001 | DIR | 0 | 0 |  | Pin > D |
| 1110_CDDDDDDDD | Adj > D | Input, 1.5 kΩ | C00001001 | DIR | 0 | 0 |  | Adj > D |
| 1111_CDDDDDDDD | Adj > D | !Input, 1.5 kΩ | C01001001 | DIR | 0 | 0 |  | Adj > D |

¹ `OUT` means output latch bit drives output; `Input` means the 'Input' column's item drives output
² `OE` is digital logic output enable only; analog output is indicated in the DAC column
³ if OUT bit = 1

### Page 24 — Pin Mode Legend

**C — IN/OUT sampling**

| C | Meaning |
|---|---|
| 0 | Live ¹ |
| 1 | Clocked ² |

**I — IN polarity** and **O — Output polarity**

| Bit | I (IN) | O (Output) |
|---|---|---|
| 0 | True | True |
| 1 | Not (inverted) | Not (inverted) |

**HHH / LLL — Drive**  ‹the pin drive ladder; the same ladder appears on the equivalent-schematic figures, pp.27-32›

| HHH / LLL | Drive |
|---|---|
| 000 | Fast |
| 001 | 1.5 kΩ |
| 010 | 15 kΩ |
| 011 | 150 kΩ |
| 100 | 1 mA |
| 101 | 100 µA |
| 110 | 10 µA |
| 111 | Float |

**Field definitions (right-hand column of the legend block)**

| Symbol | Definition |
|---|---|
| OE | digital output enable (when DIR bit high) |
| DAC | digital to analog converter enable (when DIR bit high) |
| ADC | analog to digital converter enable (fixed, or when OUT bit high) |
| OUT | output latch bit; 0: low, 1: high. **Exception:** DAC modes use OUT as 0: disable, 1: enable. |
| DIR | direction bit; 0: input (float), 1: output (drive). **Exception:** DAC modes use DIR as 0: disable, 1: enable. |
| DDDDDDDD and D | DAC Level |

¹ used for feedback operations; provides continuous (non-clocked) signal
² signal updates on clock edge only


## Page 25 — (T) Pin DIR/OUT Control

| Default (%TT = 00) |  |  |
|---|---|---|
| for odd pins |  | 'OTHER' = even pin's NOT (inverted) output state (diff source) |
| for even pins |  | 'OTHER' = unique pseudo-random bit (noise source) |
| for all pins |  | 'SMART' = smart pin output which overrides OUT/OTHER |
| 'DAC_MODE' is enabled when M[12:10] = %101 |  |  |
| 'BIT_DAC' outputs {2{M[7:4]}} for 'high' or {2{M[3:0]}} for 'low' in DAC_MODE |  |  |
| for smart pin mode "off" (%SSSSS = %00000) |  |  |
|  | DIR enables output |  |
|  | for non-DAC_MODE |  |
|  | 0x | OUT drives output |
|  | 1x | OTHER drives output |
|  | for DAC_MODE |  |
|  | 00 | DIR enables DAC, M[7:0] sets DAC level |
|  | 01 | OUT enables ADC, M[3:0] selects cog DAC channel |
|  | 10 | OUT drives BIT_DAC |
|  | 11 | OTHER drives BIT_DAC |
| for smart pin mode "on" (%SSSSS > %00000) |  |  |
|  | x0 | output disabled, regardless of DIR |
|  | x1 | output enabled, regardless of DIR |
| for DAC smart pin modes (%SSSSS = %00001..%00011) |  |  |
|  | 0x | OUT enables DAC in DAC_MODE, M[7:0] overridden |
|  | 1x | OTHER enables DAC in DAC_MODE, M[7:0] overridden |
| for non-DAC smart pin modes (%SSSSS = %00100..%11111) |  |  |
|  | 0x | SMART/OUT drives output, or BIT_DAC if DAC_MODE |
|  | 1x | SMART/OTHER drives output, or BIT_DAC if DAC_MODE |

## Pages 26-32 — I/O Pin Circuit and Equivalent Schematics  ‹broken-table #6 "I/O Pin Equivalent Circuit"›

**These are figures, not tables.** Page 26 carries one full I/O-pin circuit diagram; pages 27-32
carry 24 equivalent schematics, one per unique pin configuration, four to a page. Both mechanical
table paths correctly find nothing: `camelot lattice` reports no table on pp.26-32, and
`camelot stream` returns only the page footer. The text layer on those pages is the heading and
the footer, nothing more — the content is entirely raster.

They are already captured as images in
`assets/images-20250906/Propeller2-P2X8C4M64P-Datasheet-20221101_page{26..32}_img*.png`
(25 files; catalogued in that folder's `image-catalog.md`).

**Read off the figures (page 27, `page27_img01.png`, read 2026-08-24):** each schematic carries the
same on-diagram drive legend, and it is **resistive**, matching the p.24 Pin Mode Legend exactly:

| H/L | DRIVE |
|---|---|
| 000 | Digital |
| 001 | 1.5k |
| 010 | 15k |
| 011 | 150k |
| 100 | 1mA |
| 101 | 100uA |
| 110 | 10uA |
| 111 | Float |

**No nanosecond quantity appears on any of these figures.**

## Page 33 — Smart Pin Registers

| 32-bit Register | Purpose |
|---|---|
| Mode | smart pin mode, as well as low-level I/O pin mode (write-only) |
| X | mode-specific parameter (write-only) |
| Y | mode-specific parameter (write-only) |
| Z | mode-specific result (read-only) |

## Pages 34-35 — (S) Smart Pin Modes  ‹broken-table #7 "Smart Pin Mode Summary"›

| %SSSSS | Mode | Note |
|---|---|---|
| 00000 | smart pin off; normal operation (default) |  |
| 00001 | long repository | M[12:10] != %101 (not DAC_MODE) |
| 00010 | long repository | M[12:10] != %101 (not DAC_MODE) |
| 00011 | long repository | M[12:10] != %101 (not DAC_MODE) |
| 00001 | DAC noise | M[12:10] = %101 (DAC_MODE) |
| 00010 | DAC 16-bit dither, noise | M[12:10] = %101 (DAC_MODE) |
| 00011 | DAC 16-bit dither, PWM | M[12:10] = %101 (DAC_MODE) |
| 00100&nbsp;¹ | pulse/cycle output |  |
| 00101&nbsp;¹ | transition output |  |
| 00110&nbsp;¹ | NCO frequency |  |
| 00111&nbsp;¹ | NCO duty |  |
| 01000&nbsp;¹ | PWM triangle |  |
| 01001&nbsp;¹ | PWM sawtooth |  |
| 01010&nbsp;¹ | PWM switch-mode power supply, V and I feedback |  |
| 01011 | periodic/continuous: A-B quadrature encoder |  |
| 01100 | periodic/continuous: inc on A-rise & B-high |  |
| 01101 | periodic/continuous: inc on A-rise & B-high / dec on A-rise & B-low |  |
| 01110 | periodic/continuous: inc on A-rise {/ dec on B-rise} |  |
| 01111 | periodic/continuous: inc on A-high {/ dec on B-high} |  |
| 10000 | time A-states |  |
| 10001 | time A-highs |  |
| 10010 | time X A-highs/rises/edges -or- timeout on X A-high/rise/edge |  |
| 10011 | for X periods, count time |  |
| 10100 | for X periods, count states |  |
| 10101 | for periods in X+ clocks, count time |  |
| 10110 | for periods in X+ clocks, count states |  |
| 10111 | for periods in X+ clocks, count periods |  |
| 11000 | ADC sample/filter/capture, internally clocked |  |
| 11001 | ADC sample/filter/capture, externally clocked |  |
| 11010 | ADC scope with trigger |  |
| 11011&nbsp;¹ | USB host/device | even/odd pin pair = DM/DP |
| 11100&nbsp;¹ | sync serial transmit | A-data, B-clock |
| 11101 | sync serial receive | A-data, B-clock |
| 11110&nbsp;¹ | async serial transmit | baud rate |
| 11111 | async serial receive | baud rate |

¹ OUT signal overridden

## Page 47 — Absolute Maximum Ratings

| Absolute Maximum Ratings |  |
|---|---|
| Ambient temperature under bias | -40 °C to +125 °C |
| Storage temperature | -40 °C to +150 °C |
| Voltage on VDD with respect to GND | -0.3 V to +2.2 V |
| Voltage on Vxxyy with respect to GND | -0.3 V to +4.0 V |
| Voltage on all other pins with respect to GND1 | -0.3 V to (Vxxyy + 0.3 V) |
| Total power dissipation | 2.5 W |
| Max. current out of GND | 4 A |
| Max. current into VDD pins | 120 mA per pin |
| Max. current into Vxxyy pins | 120 mA per pin |
| Max DC current into an input pin with internal protection diode forward biased | ±10 mA |
| Max. allowable current per I/O pin | ±30 mA |
| ESD Human Body Model (JS-001) | 4 kV |
| ESD Charged Device Model (JS-002) | 1 kV |

> Note ¹ (p.47): *"I/O pin voltages in respect to GND may be exceeded if the internal protection
> diode forward bias current is not exceeded."*

## Pages 47-48 — DC Characteristics  ‹broken-table #4 — the prior note said "Page 34"; it is **pages 47-48**›

Operating temperature range: -40 °C to +105 °C unless otherwise noted.

| Symbol | Parameter | Conditions | Min | Typ1 | Max | Units |
|---|---|---|---|---|---|---|
| Vdd | Core Supply Voltage |  | 1.7 | 1.8 | 1.9 | V |
| Vxxyy | VIO Supply Voltage |  | 3.15 | 3.3 | 3.45 | V |
| Vih | Input Logic Threshold |  | Vxxyy * 0.3 | Vxxyy * 0.5 | Vxxyy * 0.7 | V |
| Iil | Input Leakage Current | IO pin Vin = GND or Vio |  | ±0.1 | ±10 | μA |

*(table continues on page 48)*

| Symbol | Parameter | Conditions | Min | Typ ¹ | Max | Units |
|---|---|---|---|---|---|---|
| Vol | Output Low Voltage<br>(relative to GND) | VDD=3.3V, sinking 1mA<br>VDD=3.3V, sinking 10mA<br>VDD=3.3V, sinking 30mA |  | 15<br>160<br>510 |  | mV |
| Voh | Output High Voltage<br>(relative to Vxxyy) | VDD=3.3V, sourcing 1mA<br>VDD=3.3V, sourcing 10mA<br>VDD=3.3V, sourcing 30mA |  | -6<br>-170<br>-580 |  | mV |
| Iq Vdd | VDD Quiescent Current | RESn = TEST = P0..P64 = 0V,<br>Vxxyy = 3.3V, VDD = 1.8V |  | 40 |  | μA |
| Iq Vxxyy | Vxxyy Quiescent Current | RESn = TEST = P0..P64 = 0V,<br>Vxxyy = 3.3V, VDD = 1.8V |  | 0.5 |  | μA |

¹ Data in the Typical "Typ" column is T = 25 °C unless otherwise stated.

**The DC table is complete as shown.** It ends with `Iq Vxxyy`; the remainder of page 48 above the
AC heading is the footnote. Its highest characterised drive current is **30 mA**, consistent with the
Absolute Maximum Ratings' **±30 mA per I/O pin**.

## Page 48 — AC Characteristics  ‹broken-table #5 — the prior note said "Page 35"; it is **page 48**›

Operating temperature range: -40 °C to +105 °C unless otherwise noted.

| Symbol | Parameter | Conditions | Min | Typ ¹ | Max | Units |
|---|---|---|---|---|---|---|
| Freq | Oscillator Frequency | RCSLOW (internal)<br>RCFAST (internal)<br>Direct drive (into XI)<br>Crystal (between XI and XO)<br>PLL (fed by direct drive or crystal) | 12<br>20<br>DC<br>1<br>3.33 | 20<br>24<br>-<br>-<br>180 ² | 30<br>30<br>200<br>50<br>320 | kHz<br>MHz<br>MHz<br>MHz<br>MHz |
| Cin | XI and XO pin Capacitance | Mode 0 : Disabled (1MΩ feedback resistor off)<br>Mode 1 : Direct drive<br>Mode 2 : Crystal ≥ 16MHz<br>Mode 3 : Crystal < 16MHz |  | 2<br>2<br>15<br>30 |  | pF<br>pF<br>pF<br>pF |

¹ Data in the Typical "Typ" column is T = 25 °C unless otherwise stated.
² Nominal PLL frequency (system clock speed) is 180 MHz at up to 105 °C.

> 🔴 **MEASURED, NOT INFERRED — this table has exactly two symbols.** `Freq` and `Cin`, nine data
> lines total. All three extraction paths agree, including a visual read of the rendered page: the
> table ends at `Cin` mode 3 and the rest of page 48 is white space and two footnotes. **There is no
> propagation-delay row, no rise-time row, no input-timing row, and no nanosecond quantity anywhere
> in the AC Characteristics table.** This is the source being silent, not the extractor failing —
> the distinction was established by opening the page, per the rule that a mangled table looks
> exactly like a number that was never there.
>
> **The one `ns` in this document, so a grep does not mislead:** page 3's FEATURES bullet reads
> *"8-bit, 120-ohm (**3ns**) and 1k-ohm DACs with 16-bit oversampling, noise, and high/low digital
> modes"*. That is the **only** nanosecond quantity in all 50 pages
> (`grep -nEo '[0-9]+(\.[0-9]+)? ?n[sS]([^a-zA-Z]|$)'` → exactly one hit), the datasheet does not
> say what it measures, and it is attached to a **DAC**, not to pin timing.

## Page 50 — Change Log

| Date | Notes |
|---|---|
| 2021-05-05 | First public release. |
| 2021-05-27 | Added Cog RAM, Locks, CORDIC Solver, and Smart I/O Pins sections.  Updated all Hardware<br>Connections diagrams.  Corrected Hub RAM size type and clariﬁed address type in Propeller 2<br>(P2X8C4M64P) RAM Memory Conﬁguration table. |
| 2021-07-09 | Changed "Additional Documentation and Resources" to "Preface" and described this document's<br>intention.  Added Cog Attention section.  In the Smart I/O Pins section, revised descriptions,<br>included direction and state, pin registers and special<br>instructions, added an I/O Pin Timing<br>section, replaced the Pin Mode table with an enhanced version, and enhanced all I/O pin circuits<br>to improve clarity.  Clariﬁed CORDIC Solver pipeline stream and throughput capability.  Added<br>Host Communication, P2 Monitor, TAQOZ, and Rebooting sections. |
| 2022-11-01 | Replaced I/O Pin Timing diagrams and enhanced related descriptions.  Updated Internal fast<br>oscillator speed from ~20 MHz to 20+ MHz.  Amended Cog RAM diagram with note about<br>debug interrupt call/return address.  Clariﬁed 20-bit address "don't care" bits statement.  Fixed<br>VCO's max frequency in ﬁrst System Clock table. Fixed typo in Lock Usage.  Enhanced naming<br>of CORDIC Solver functions.  Corrected and enhanced description of the special microSD boot<br>ﬁle. |

---

## Tables the prior note expected that the datasheet does not contain

| Expected | Verdict | Evidence |
|---|---|---|
| **Boot Source Selection** (broken-table #9) | **NOT IN THIS DOCUMENT** — recorded as a determination, not a gap | The datasheet's whole boot treatment is p.11 prose — *"The Bootloader checks the boot pattern (configuration) on pins P59-P61"* — closing with *"See Propeller 2 Hardware Manual's Boot Up procedure section for more information."* Boot-mode selection is shown on p.10 as a **switch in a schematic** plus two bullets (switch closed = SPI Flash, open = microSD), read from the rendered page. `camelot lattice` finds no table on pp.8-11; `camelot stream` on those pages returns only the bullet prose. The 9-row **Boot Pattern** table exists in the **P2 Hardware Manual** (Table 5 of `sources/p2-hardware-manual/complete-tables-reference.md`), which is where the datasheet points. |

## Cross-check against the P2 Hardware Manual (2022/11/01)

The hardware manual was re-ingested DOCX-primary on 2026-08-24; its 53 tables are the strongest
available corroborator because a DOCX carries real table structure.

| Table | Datasheet | Hardware Manual | Agreement |
|---|---|---|---|
| Part Number Legend | p.1 | Table 3 | **identical**, cell for cell |
| Pin Descriptions | p.6 | Table 4 | **identical** on Pin Name / Direction / V(typ); manual's GND row adds "[not shown here]" wording |
| Clock source `%SS` | p.18 | Table 26 area (`%00 RCFAST` etc.) | agrees |
| Pin drive ladder | p.24 legend **and** pp.27-32 figures | Table 18's nested legend + figs 10-33 | **identical and resistive**: `000 Fast/Digital · 001 1.5 kΩ · 010 15 kΩ · 011 150 kΩ · 100 1 mA · 101 100 µA · 110 10 µA · 111 Float` |
| Max current per I/O pin | p.47, **±30 mA** | Table 2, `Max current per I/O  +/- 30mA` | **agrees** |
| Boot Pattern | *absent* — defers to the manual | Table 5 (9 rows) | not a conflict; a deliberate cross-reference |
| DC / AC Characteristics | pp.47-48 | *absent* — the manual has no electrical-characteristics section at all | datasheet is the sole documentary authority for these |

**One cross-source conflict found and filed — F-330.** The manual's Table 10 says the VCO
*"should be kept within 100 MHz to **350** MHz"*; the datasheet (p.18 **and** p.19) and the
Propeller 2 Documentation v35 Rev B/C both say **200 MHz** in the same sentence, and the Silicon
Doc separately identifies 350 MHz as the *overclock* ceiling (`%PPPP = 15`, VCO/1). The manual
substituted the overclock ceiling into the recommendation. See
`engineering/operations/P2KB-CORRECTION-FINDINGS.md`, F-330. Every other comparison above agrees
cell for cell.
