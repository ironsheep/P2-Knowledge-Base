# Propeller 2 Hardware Manual (2022/11/01) — All Tables, DOCX-extracted

Source: `Propeller 2 Hardware Manual - 20221101.docx` (`word/document.xml`).
53 tables total (49 top-level in body order; the remainder are nested inside a cell and referenced as `[[SEE TABLE n]]`).

## Table 1 — 2 rows × 2 cols

| Hardware | Firmware |
|---|---|
| P2X8C4M64P | Rev B/C |

## Table 2 — 21 rows × 2 cols

| Propeller 2 Specifications |  |
|---|---|
| Feature | Specification |
| Model | P2X8C4M64P |
| Power | 1.8 V Core, 3.3 V I/O |
| Internal Oscillator | ~24 MHz or ~20 kHz |
| External Clock | 10 - 20 MHz crystal (P2 Clock PLL enabled) or 0 to 180 MHz (nominal) clock oscillator |
| Nominal System Clock Speed | 180 MHz @ 105 ℃ |
| Number of clock modes | 6 + PLL ÷/× & 2 OSC load options |
| Cogs (cores) | 8 identical |
| Internal execution speed | 0 to 720 MIPS (90 MIPS/cog) @ 180 MHz |
| Cog RAM | 512 longs (Register RAM) + 512 longs (Lookup RAM) |
| Hub RAM | 512 KB (byte/word/long-addressable) |
| ROM | 16 KB (Bootloader, P2 Monitor debug interface, and TAQOZ (Forth) command interface) |
| I/O Pins | 64; each featuring digital and analog signalling plus internal smart circuits |
| Max current per I/O | +/- 30mA |
| Inter-cog communication | Hub RAM, Lookup RAM, Attention Signal, or External I/O |
| Assembly language (PASM2) | 358 instructions |
| Interpreted languages | Spin2 (Propeller Tool), TAQOZ (built-in), MicroPython, or Forth via community tools |
| Compiled languages | Spin (FlexGUI community Tool), BASIC, C/C++ (community tools) |
| PASM2 execution memory | Register RAM + Lookup RAM + Hub RAM |
| Spin2 execution memory | Hub RAM |

## Table 3 — 3 rows × 4 cols

| Part Number Legend |  |  |  |
|---|---|---|---|
| P2X | 8C | 4M | 64P |
| Propeller 2 | 8 cogs (processors) | 4 Mbit Hub RAM (512 KB) | 64 smart I/O pins |

## Table 4 — 10 rows × 4 cols

| Pin Descriptions |  |  |  |
|---|---|---|---|
| Pin Name | Direction | V (typ) | Description |
| GND / [not shown] | - | 0 | Ground for core and smart pins; [not shown here] internally connected to underside exposed pad.  Connect to ground plane for thermal dissipation. |
| TEST | I | 0 | Tied to ground |
| VDD | - | 1.8 | Core power |
| P0-63 | I/O | 0 to 3.3 | Smart pins; P58-P63 serve in the boot process, then general purpose after. |
| Vxxyy | - | 3.3 | Power for smart pins in groups of 4: Pxx through Pyy |
| XO | O | - | Crystal Output. Provides feedback for an external crystal, or may be left disconnected depending on CLK Register settings. No external resistors or capacitors are required. |
| XI | I | - | Crystal Input. Can be connected to output of crystal/oscillator pack (with XO left disconnected), or to one leg of crystal (with XO connected to the other leg of crystal or resonator) depending on CLK Register settings. No external resistors or capacitors are required. |
| RESN | I | 0 | Reset (active low). When low, resets the Propeller: all cogs disabled and I/O pins floating. Propeller restarts 3 ms after RESn transitions from low to high.  Connect to a resistor to pull up to 3.3 V. |

## Table 5 — 9 rows × 4 cols

| Boot Pattern |  |  |  |
|---|---|---|---|
| Set by floating connection 'ƒ', pull-up resistor '⇧', or pull-down resistor '⇩'.  Don't care is '⨯'. |  |  |  |
| P611 | P601 | P591 | Procedure |
| ƒ | ƒ | ƒ | Program from serial within 60 s window |
| ⨯ | ⨯ | ⇧ | Program from serial within 60 s window; no flash or microSD card boot |
| ⇧ | ⨯ | ƒ | Program from serial within 100 ms or boot from flash.  If fails, program from serial within 60 s window. |
| ⇧ | ⨯ | ⇩ | Fast boot from flash; no serial.  If it fails, shutdown. |
| ƒ / ⇩ | ⇧2 | ƒ | Boot from microSD card.  If fails, program from serial within 60 s window. |
| ƒ / ⇩ | ⇧2 | ⇩ | Boot from microSD card.  If it fails, shutdown. |

## Table 6 — 5 rows × 7 cols

| Host Serial and Boot Memory Connections |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| Type | P63 (in) | P62 (out) | P61 (out) | P60 (out) | P59 (out) | P58 (in) |
| Host Serial | TX (out) | RX (in) |  |  |  |  |
| Flash SPI |  |  | CSn (in) | CLK (in) | DI (in) | DO (out) |
| SD SPI |  |  | CLK (in) | CSn (in) | DI (in) | DO (out) |

## Table 7 — 5 rows × 6 cols

| Propeller 2 (P2X8C4M64P) RAM Memory Configuration |  |  |  |  |  |
|---|---|---|---|---|---|
| Region | Depth | Width | Address Range / (Hex) | PASM Instruction D/S / Address Range (Hex) | PC Increment 1 |
| Cog "Register" RAM | 512 | 32 bits | $00000..$001FF | $000..$1FF | 1 |
| Cog "Lookup" RAM | 512 | 32 bits | $00200..$003FF | $000..$1FF | 1 |
| Hub RAM | 524,288 | 8 bits | $00400..$7FFFF | $00000..$7FFFF | 4 |

## Table 8 — 2 rows × 3 cols

| Address | Name | Purpose |
|---|---|---|
| $1F0 / $1F1 / $1F2 / $1F3 / $1F4 / $1F5 / $1F6 / $1F7 | RAM / IJMP3 / RAM / IRET3 / RAM / IJMP2 / RAM / IRET2 / RAM / IJMP1 / RAM / IRET1 / RAM / PA    / RAM / PB | Interrupt call address for INT3                    / Interrupt return address for INT3                  / Interrupt call address for INT2                    / Interrupt return address for INT2                  / Interrupt call address for INT1                    / Interrupt return address for INT1                  / CALLD-imm return, CALLPA parameter, or LOC address / CALLD-imm return, CALLPB parameter, or LOC address |

## Table 9 — 2 rows × 3 cols

| Address | Name | Purpose |
|---|---|---|
| $1F8 / $1F9 / $1FA / $1FB / $1FC / $1FD / $1FE / $1FF | PTRA   / PTRB   / DIRA   / DIRB   / OUTA   / OUTB   / INA1  / INB2 | Pointer A to Hub RAM        / Pointer B to Hub RAM        / Output enables (direction bits) for P31..P0  / Output enables (direction bits) for P63..P32 / Output states for P31..P0   / Output states for P63..P32  / Input states for P31..P0    / Input states for P63..P32 |

## Table 10 — 5 rows × 4 cols

| PLL Setting | Value | Effect | Notes |
|---|---|---|---|
| %E | 0/1 | PLL off/on | XI input must be enabled by %CC. Allow 10 ms for crystal+PLL to stabilize before switching over to PLL clock source. |
| %DDDDDD | 0..63 | 1..64 division of XI pin frequency | This divided XI frequency feeds into the phase-frequency comparator's 'reference' input. |
| %MMMMMMMMMM | 0..1023 | 1..1024 division of VCO frequency | This divided VCO frequency feeds into the phase-frequency comparator's 'feedback' input. This frequency division has the effect of multiplying the divided XI frequency (per %DDDDDD) inside the VCO. The VCO frequency should be kept within 100 MHz to 350 MHz. |
| %PPPP | 0 / 1 / 2 / 3 / 4 / 5 / 6 / 7 / 8 / 9 / 10 / 11 / 12 / 13 / 14 / 15 | VCO / 2 / VCO / 4 / VCO / 6 / VCO / 8 / VCO / 10 / VCO / 12 / VCO / 14 / VCO / 16 / VCO / 18 / VCO / 20 / VCO / 22 / VCO / 24 / VCO / 26 / VCO / 28 / VCO / 30 / VCO / 1 | This divided VCO frequency is selectable as the system clock when SS = %11. |

## Table 11 — 5 rows × 5 cols

| %CC | XI status | XO status | XI / XO impedance | XI / XO loading caps |
|---|---|---|---|---|
| %00 | ignored | float | Hi-Z | OFF |
| %01 | input | 600-ohm drive | 1M-ohm | OFF |
| %10 | input | 600-ohm drive | 1M-ohm | 15pF per pin |
| %11 | input | 600-ohm drive | 1M-ohm | 30pF per pin |

## Table 12 — 5 rows × 3 cols

| %SS | Clock Source | Notes |
|---|---|---|
| %11 | PLL | CC != %00 and E=1, allow 10ms for crystal+PLL to stabilize before switching to PLL |
| %10 | XI | CC != %00, allow 5ms for crystal to stabilize before switching to XI pin |
| %01 | RCSLOW | ~20 kHz, can be switched to at any time, low-power |
| %00 | RCFAST | 20 MHz+1, can be switched to at any time, used on boot up |

## Table 13 — 1 rows × 1 cols

|  |
|---|

## Table 14 — 8 rows × 3 cols

| I/O Pin Registers |  |  |
|---|---|---|
| Register | Cog Address | Purpose |
| DIRA | $1FA | Output enable bits for P0..P31 (active high) |
| DIRB | $1FB | Output enable bits for P32..P63 (active high) |
| OUTA | $1FC | Output state bits for P0..P31 (corresponding DIRA bit must be high to enable output) |
| OUTB | $1FD | Output state bits for P32..P63 (corresponding DIRB bit must be high to enable output) |
| INA | $1FE | Input state bits for P0..P31 |
| INB | $1FF | Input state bits for P32..P63 |

## Table 15 — 8 rows × 2 cols

| Special Pin Instructions |  |
|---|---|
| Instructions | Purpose |
| DIRL / DIRH / DIRC / DIRNC / DIRZ / DIRNZ / DIRRND / DIRNOT {#}D | Affect pin D bit in DIRx |
| OUTL / OUTH / OUTC / OUTNC / OUTZ / OUTNZ / OUTRND / OUTNOT {#}D | Affect pin D bit in OUTx |
| FLTL / FLTH / FLTC / FLTNC / FLTZ / FLTNZ / FLTRND / FLTNOT {#}D | Affect pin D bit in OUTx, clear bit in DIRx |
| DRVL / DRVH / DRVC / DRVNC / DRVZ / DRVNZ / DRVRND / DRVNOT {#}D | Affect pin D bit in OUTx, set bit in DIRx |
| TESTP {#}D WC / WZ / ANDC / ANDZ / ORC / ORZ / XORC / XORZ | Read pin D bit in INx and affect C or Z |
| TESTPN {#}D WC / WZ / ANDC / ANDZ / ORC / ORZ / XORC / XORZ | Read pin D bit in !INx and affect C or Z |

## Table 16 — 12 rows × 2 cols

| (A) PIN or (B) ADJ Input Selector |  |
|---|---|
| %AAAA / %BBBB | Selection |
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

## Table 17 — 10 rows × 2 cols

| (F) PIN and ADJ Logic/Filtering |  |
|---|---|
| %FFF | Logic/Filter |
| 000 | A, B (default) |
| 001 | A AND B, B |
| 010 | A OR  B, B |
| 011 | A XOR B, B |
| 100 | A, B, both filtered using global filt0 settings |
| 101 | A, B, both filtered using global filt1 settings |
| 110 | A, B, both filtered using global filt2 settings |
| 111 | A, B, both filtered using global filt3 settings |

## Table 18 — 10 rows × 10 cols

| (M) Pin Mode |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|
| WRPIN D[20:8] Configuration |  |  |  | Resulting Internal Configuration |  |  |  |  |  |
| M[12:0] | Input | Pin Output1 |  | CIOHHHLLL | OE2 | DAC | ADC | ADC Mode | Comparator |
| 0000_CIOHHHLLL / 0001_CIOHHHLLL / 0010_CIOHHHLLL / 0011_CIOHHHLLL / 0100_CIOHHHLLL / 0101_CIOHHHLLL / 0110_CIOHHHLLL / 0111_CIOHHHLLL | Pin Logic / Pin Logic / Adj Logic / Pin Schmitt / Pin Schmitt / Adj Schmitt / Pin > Adj / Pin > Adj | OUT / Input / Input / OUT / Input / Input / OUT / Input |  | CIOHHHLLL / CIOHHHLLL / CIOHHHLLL / CIOHHHLLL / CIOHHHLLL / CIOHHHLLL / CIOHHHLLL / CIOHHHLLL | DIR / DIR / DIR / DIR / DIR / DIR / DIR / DIR | 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 |  | 0 / 0 / 0 / 0 / 0 / 0 / Pin > Adj / Pin > Adj |
| 100000_OHHHLLL / 100001_OHHHLLL / 100010_OHHHLLL / 100011_OHHHLLL / 100100_OHHHLLL / 100101_OHHHLLL / 100110_OHHHLLL / 100111_OHHHLLL | ADC, GND / ADC, Vxxyy / ADC, float / ADC, Pin 1x / ADC, Pin 3.16x / ADC, Pin 10x / ADC, Pin 31.6x / ADC, Pin 100x | OUT / OUT / OUT / OUT / OUT / OUT / OUT / OUT |  | 10OHHHLLL / 10OHHHLLL / 10OHHHLLL / 10OHHHLLL / 10OHHHLLL / 10OHHHLLL / 10OHHHLLL / 10OHHHLLL | DIR / DIR / DIR / DIR / DIR / DIR / DIR / DIR | 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 | 1 / 1 / 1 / 1 / 1 / 1 / 1 / 1 | 000 / 001 / 010 / 011 / 100 / 101 / 110 / 111 | 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 |
| 10100_DDDDDDDD / 10101_DDDDDDDD / 10110_DDDDDDDD / 10111_DDDDDDDD | ADC, Pin 1x 3 / ADC, Pin 1x 3 / ADC, Pin 1x 3 / ADC, Pin 1x 3 | DAC 990 Ω, 3.3 V / DAC 600 Ω, 2.0 V / DAC 123.75 Ω, 3.3 V / DAC 75 Ω, 2.0 V |  | 10xxxxxxx / 10xxxxxxx / 10xxxxxxx / 10xxxxxxx | 0 / 0 / 0 / 0 | DIR / DIR / DIR / DIR | OUT / OUT / OUT / OUT | 011 / 011 / 011 / 011 | 0 / 0 / 0 / 0 |
| 1100_CDDDDDDDD / 1101_CDDDDDDDD / 1110_CDDDDDDDD / 1111_CDDDDDDDD | Pin > D / Pin > D / Adj > D / Adj > D | OUT, 1.5 kΩ / !Input, 1.5 kΩ / Input, 1.5 kΩ / !Input, 1.5 kΩ |  | C00001001 / C01001001 / C00001001 / C01001001 | DIR / DIR / DIR / DIR | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |  | Pin > D / Pin > D / Adj > D / Adj > D |
| 1 OUT means output latch bit drives output; Input means the 'Input' column's item drives output / 2 OE is digital logic output enable only; analog output is indicated in the DAC column / 3 if OUT bit = 1 |  |  |  |  |  |  |  |  |  |
| Pin Mode Legend |  |  |  |  |  |  |  |  |  |
| [[SEE TABLE 19]] |  |  |  |  |  |  |  |  |  |

## Table 19 — 1 rows × 3 cols  _(nested inside a cell of another table)_

| [[SEE TABLE 20]] | [[SEE TABLE 21]] | [[SEE TABLE 22]] |
|---|---|---|

## Table 20 — 8 rows × 2 cols  _(nested inside a cell of another table)_

| C | IN / OUT |
|---|---|
| 0 / 1 | Live 1 / Clocked 2 |
|  |  |
| I | IN |
| 0 / 1 | True / Not (inverted) |
|  |  |
| O | Output |
| 0 / 1 | True / Not (inverted) |

## Table 21 — 3 rows × 2 cols  _(nested inside a cell of another table)_

| HHH / LLL | Drive |
|---|---|
| 000 / 001 / 010 / 011 / 100 / 101 / 110 / 111 | Fast / 1.5 kΩ / 15 kΩ / 150 kΩ / 1 mA / 100 µA / 10 µA / Float |
|  |  |

## Table 22 — 6 rows × 1 cols  _(nested inside a cell of another table)_

| OE = digital output enable (when DIR bit high) |
|---|
| DAC = digital to analog converter enable (when DIR bit high) |
| ADC = analog to digital converter enable (fixed, or when OUT bit high) |
| OUT = output latch bit; 0: low, 1: high. / Exception: DAC modes use OUT as 0: disable, 1: enable. |
| DIR = direction bit; 0: input (float), 1: output (drive) / Exception: DAC modes use DIR as 0: disable, 1: enable. |
| DDDDDDDD and D = DAC Level |

## Table 23 — 26 rows × 3 cols

| (T) Pin DIR/OUT Control |  |  |
|---|---|---|
| Default (%TT = 00) |  |  |
| for odd pins |  | 'OTHER' = even pin's NOT (inverted) output state (diff source) |
| for even pins |  | 'OTHER' = unique pseudo-random bit (noise source) |
| for all pins |  | 'SMART' = smart pin output which overrides OUT / OTHER |
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
|  | 0x | SMART / OUT drives output, or BIT_DAC if DAC_MODE |
|  | 1x | SMART / OTHER drives output, or BIT_DAC if DAC_MODE |

## Table 24 — 6 rows × 2 cols

| Smart Pin Registers |  |
|---|---|
| 32-bit Register | Purpose |
| Mode | smart pin mode, as well as low-level I/O pin mode (write-only) |
| X | mode-specific parameter (write-only) |
| Y | mode-specific parameter (write-only) |
| Z | mode-specific result (read-only) |

## Table 25 — 37 rows × 3 cols

| (S) Smart Pin Modes |  |  |
|---|---|---|
| %SSSSS | Mode | Note |
| 00000 | smart pin off; normal operation (default) |  |
| 00001 | long repository | M[12:10] != %101 (not DAC_MODE) |
| 00010 | long repository | M[12:10] != %101 (not DAC_MODE) |
| 00011 | long repository | M[12:10] != %101 (not DAC_MODE) |
| 00001 | DAC noise | M[12:10]  = %101 (DAC_MODE) |
| 00010 | DAC 16-bit dither, noise | M[12:10]  = %101 (DAC_MODE) |
| 00011 | DAC 16-bit dither, PWM | M[12:10]  = %101 (DAC_MODE) |
| 001001 | pulse/cycle output |  |
| 001011 | transition output |  |
| 001101 | NCO frequency |  |
| 001111 | NCO duty |  |
| 010001 | PWM triangle |  |
| 010011 | PWM sawtooth |  |
| 010101 | PWM switch-mode power supply, V and I feedback |  |
| 01011 | periodic/continuous: A-B quadrature encoder |  |
| 01100 | periodic/continuous: inc on A-rise & B-high |  |
| 01101 | periodic/continuous: inc on A-rise & B-high / dec on A-rise & B-low |  |
| 01110 | periodic/continuous: inc on A-rise {/ dec on B-rise} |  |
| 01111 | periodic/continuous: inc on A-high {/ dec on B-high} |  |
| 10000 | time A-states |  |
| 10001 | time A-highs |  |
| 10010 | time X A-highs/rises/edges -or- timeout on X A-high/rise/edge |  |
| 10011 | count time for X periods |  |
| 10100 | count state for X periods |  |
| 10101 | count time for periods in X+ clocks |  |
| 10110 | count states for periods in X+ clocks |  |
| 10111 | count periods for periods in X+ clocks |  |
| 11000 | ADC sample/filter/capture, internally clocked |  |
| 11001 | ADC sample/filter/capture, externally clocked |  |
| 11010 | ADC scope with trigger |  |
| 110111 | USB host/device | even/odd pin pair = DM/DP |
| 111001 | sync serial transmit | A-data, B-clock |
| 11101 | sync serial receive | A-data, B-clock |
| 111101 | async serial transmit | baud rate |
| 11111 | async serial receive | baud rate |

## Table 26 — 19 rows × 6 cols

| Sample/Filter/Capture Configurations |  |  |  |  |  |
|---|---|---|---|---|---|
|  | X[5:4]	➡ / 			Mode	➡ | %00 / SINC2 Sampling | %01 / SINC2 Filtering | %10 / SINC3 Filtering | %11 / Bitstream Capturing |
| X[3:0] | Sample Period | Sample Resolution | Post-diff ENOB1 | Post-diff ENOB1 | (LSB = oldest bit) |
| %0000 | 1 clock | impractical | impractical | impractical | 1 new bit |
| %0001 | 2 clocks | 2 bits | impractical | impractical | 2 new bits |
| %0010 | 4 clocks | 3 bits | impractical | impractical | 4 new bits |
| %0011 | 8 clocks | 4 bits | 4 | impractical | 8 new bits |
| %0100 | 16 clocks | 5 bits | 5 | 8 | 16 new bits |
| %0101 | 32 clocks | 6 bits | 6 | 10 | 32 new bits |
| %0110 | 64 clocks | 7 bits | 7 | 12 | overflow |
| %0111 | 128 clocks | 8 bits | 8 | 14 | overflow |
| %1000 | 256 clocks | 9 bits | 9 | 16 | overflow |
| %1001 | 512 clocks | 10 bits | 10 | 18 | overflow |
| %1010 | 1,024 clocks | 11 bits | 11 | overflow | overflow |
| %1011 | 2,048 clocks | 12 bits | 12 | overflow | overflow |
| %1100 | 4,096 clocks | 13 bits | 13 | overflow | overflow |
| %1101 | 8,192 clocks | 14 bits | 14 | overflow | overflow |
| %1110 | 16,384 clocks | overflow | overflow | overflow | overflow |
| %1111 | 32,768 clocks | overflow | overflow | overflow | overflow |

## Table 27 — 3 rows × 3 cols

| A and B / relationship | Arming Event / (initial / after trigger) | Trigger Event / (after arming) |
|---|---|---|
| A > B | sample[7:2] => A | sample[7:2] < B |
| A <= B | sample[7:2] < A | sample[7:2] => B |

## Table 28 — 2 rows × 1 cols

| Whitespace Characters in Serial Loading Protocol |
|---|
| TAB ($09), LF ($0A), CR ($0D), SPACE ($20), = ($3D)1 |

## Table 29 — 11 rows × 2 cols

| Serial Loading Protocol Commands |  |
|---|---|
| Request Propeller Type |  |
|  | Prop_Chk <INAmask> <INAdata> <INBmask> <INBdata> |
| Change Clock Setting |  |
|  | Prop_Clk <INAmask> <INAdata> <INBmask> <INBdata> <HUBSETclocksetting> |
| Load and Execute Hex Data, With and Without Checksum Verification |  |
|  | Prop_Hex <INAmask> <INAdata> <INBmask> <INBdata> <hexdatabytes> ? |
|  | Prop_Hex <INAmask> <INAdata> <INBmask> <INBdata> <hexdatabytes> ~ |
| Load and Execute Base64 Data, With and Without Checksum Verification |  |
|  | Prop_Txt <INAmask> <INAdata> <INBmask> <INBdata> <base64chrs> ? |
|  | Prop_Txt <INAmask> <INAdata> <INBmask> <INBdata> <base64chrs> ~ |

## Table 30 — 1 rows × 1 cols

| Sender:  "> Prop_Chk 0 0 0 0"+CR / Loader:  CR+LF+"Prop_Ver G"+CR+LF |
|---|

## Table 31 — 1 rows × 1 cols

| Sender:  "> Prop_Clk 0 0 0 0 19D28F8"+CR / Loader:  "." / Sender:  (wait ≈10ms) / Sender:  "> Prop_Clk 0 0 0 0 19D28FB"+CR / Loader:  "." |
|---|

## Table 32 — 1 rows × 1 cols

| Sender:  "> Prop_Clk 0 0 0 0 F0"+CR / Loader:  "." |
|---|

## Table 33 — 1 rows × 1 cols

| Sender: "> Prop_Hex 0 0 0 0 FB F7 23 F6 FD FB 23 F6 25 26 80 FF 1F 80 66 FD F0 FF 9F FD ~" |
|---|

## Table 34 — 1 rows × 1 cols

| Sender: "> Prop_Hex 0 0 0 0 FB F7 23 F6 FD FB 23 F6 25 26 80 FF 1F 80 66 FD F0 FF 9F FD 24 D8 A0 89 ?" / Loader: "." |
|---|

## Table 35 — 3 rows × 2 cols

| Base64 Characters and Values |  |
|---|---|
| Characters | Index Values |
| A–Z, a–z, 0–9, +, / | $00–$19, $1A–$33, $34–$3D, $3E, $3F |

## Table 36 — 1 rows × 1 cols

| Sender: "> Prop_Txt 0 0 0 0 +/cj9v37I/YlJoD/H4Bm/fD/n/0 ~" |
|---|

## Table 37 — 1 rows × 1 cols

| Sender: "> Prop_Txt 0 0 0 0 +/cj9v37I/YlJoD/H4Bm/fD/n/0k2KCJ ?" / Loader: "." |
|---|

## Table 38 — 6 rows × 8 cols

| Assembled "Code" Data to Base64 Stream Conversion |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|
| Code Hex | FB |  | F7 |  | 23 |  | ... |
| Code (8-bit) Binary | 11111011 |  | 11110111 |  | 00100011 |  | ... |
| Code (6-bit) Binary | 111110 | 11 | 1111 | 0111 | 00 | 100011 | ... |
| Code (6-bit) Hex | 3E | 3F |  | 1C |  | 23 | ... |
| Base64 Character | + | / |  | c |  | j | ... |

## Table 39 — 1 rows × 9 cols

| _C / _C_AND_NZ / _C_AND_Z / _C_EQ_Z | _C_NE_Z / _C_OR_NZ / _C_OR_Z / _CLR | _E / _GE / _GT / _LE | _LT / _NC / _NC_AND_NZ / _NC_AND_Z | _NC_OR_NZ / _NC_OR_Z / _NE / _NZ | _NZ_AND_C / _NZ_AND_NC / _NZ_OR_C / _NZ_OR_NC | _RET_ / _SET / _Z / _Z_AND_C | _Z_AND_NC / _Z_EQ_C / _Z_NE_C / _Z_OR_C | _Z_OR_NC |
|---|---|---|---|---|---|---|---|---|

## Table 40 — 1 rows × 12 cols

| ABORT / ABS / ADD / ADDBITS / ADDCT1 | ADDCT2 / ADDCT3 / ADDPINS / ADDPIX / ADDS | ADDSX / ADDX / AKPIN / ALIGNL / ALIGNW | ALLOWI / ALT / ALTB / ALTD / ALTGB | ALTGN / ALTGW / ALTI / ALTR / ALTS | ALTSB / ALTSN / ALTSW / AND / ANDC | ANDN / ANDZ / ARCHIVE / ASMCLK / AUGD | AUGS / BACKCOLOR / BITC / BITH / BITL | BITMAP / BITNC / BITNOT / BITNZ / BITRND | BITZ / BLACK / BLNPIX / BLUE / BMASK | BOX / BRK / BYTE / BYTEFILL / BYTEMOVE | BYTES_1BIT / BYTES_2BIT / BYTES_4BIT |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Table 41 — 1 rows × 9 cols

| CALL / CALLA / CALLB / CALLD / CALLPA / CALLPB / CARTESIAN / CASE / CASE_FAST / CHANNEL | CIRCLE / CLEAR / CLKFREQ / CLKMODE / CLKSET / CLOSE / CMP / CMPM / CMPR / CMPS | CMPSUB / CMPSX / CMPX / COGATN / COGBRK / COGCHK / COGEXEC / COGEXEC_NEW / COGEXEC_NEW_PAIR / COGID | COGINIT / COGSPIN / COGSTOP / COLOR / CON / CRCBIT / CRCNIB / CYAN / DAT / DEBUG | DEBUG_BAUD / DEBUG_COGS / DEBUG_DELAY / DEBUG_DISPLAY_LEFT / DEBUG_DISPLAY_TOP / DEBUG_HEIGHT / DEBUG_LEFT / DEBUG_LOG_SIZE / DEBUG_PIN / DEBUG_TIMESTAMP | DEBUG_TOP / DEBUG_WIDTH / DEBUG_WINDOWS_OFF / DECMOD / DECOD / DEPTH / DEV / DIRA / DIRB / DIRC | DIRH / DIRL / DIRNC / DIRNOT / DIRNZ / DIRRND / DIRZ / DJF / DJNF / DJNZ | DJZ / DLY / DOT / DOTSIZE / DRVC / DRVH / DRVL / DRVNC / DRVNOT | DRVRND / DRVZ |
|---|---|---|---|---|---|---|---|---|

## Table 42 — 1 rows × 11 cols

| ELSE / ELSEIF / ELSEIFNOT / ENCOD / END | EVENT_ATN / EVENT_CT1 / EVENT_CT2 / EVENT_CT3 / EVENT_FBW | EVENT_INT / EVENT_PAT / EVENT_QMT / EVENT_SE1 / EVENT_SE2 | EVENT_SE3 / EVENT_SE4 / EVENT_XFI / EVENT_XMT / EVENT_XRL | EVENT_XRO / EXECF / FABS / FALSE / FBLOCK | FDEC / FDEC_ / FDEC_ARRAY / FDEC_ARRAY_ / FDEC_REG_ARRAY | FDEC_REG_ARRAY_ / FFT / FGE / FGES / FILE | FIT / FLE / FLES / FLOAT / FLTC | FLTH / FLTL / FLTNC / FLTNOT / FLTNZ | FLTRND / FLTZ / FRAC / FROM / FSQRT | FVAR / FVARS |
|---|---|---|---|---|---|---|---|---|---|---|

## Table 43 — 1 rows × 10 cols

| GETBRK / GETBYTE / GETCT | GETMS / GETNIB / GETPTR | GETQX / GETQY / GETREGS | GETRND / GETSCP / GETSEC | GETWORD / GETXACC / GREEN | GREY / HIDEXY / HOLDOFF | HSV16 / HSV16W / HSV16X | HSV8 / HSV8W / HSV8X | HUBEXEC / HUBEXEC_NEW / HUBEXEC_NEW_PAIR | HUBSET |
|---|---|---|---|---|---|---|---|---|---|

## Table 44 — 1 rows × 10 cols

| IF / IF_00 / IF_0000 / IF_0001 / IF_0010 / IF_0011 / IF_01 / IF_0100 / IF_0101 / IF_0110 / IF_0111 / IF_0X | IF_10 / IF_1000 / IF_1001 / IF_1010 / IF_1011 / IF_11 / IF_1100 / IF_1101 / IF_1110 / IF_1111 / IF_1X / IF_A | IF_AE / IF_ALWAYS / IF_B / IF_BE / IF_C / IF_C_AND_NZ / IF_C_AND_Z / IF_C_EQ_Z / IF_C_NE_Z / IF_C_OR_NZ / IF_C_OR_Z / IF_DIFF | IF_E / IF_GE / IF_GT / IF_LE / IF_LT / IF_NC / IF_NC_AND_NZ / IF_NC_AND_Z / IF_NC_OR_NZ / IF_NC_OR_Z / IF_NE / IF_NOT_00 | IF_NOT_01 / IF_NOT_10 / IF_NOT_11 / IF_NZ / IF_NZ_AND_C / IF_NZ_AND_NC / IF_NZ_OR_C / IF_NZ_OR_NC / IF_SAME / IF_X0 / IF_X1 / IF_Z | IF_Z_AND_C / IF_Z_AND_NC / IF_Z_EQ_C / IF_Z_NE_C / IF_Z_OR_C / IF_Z_OR_NC / IFNOT / IJMP1 / IJMP2 / IJMP3 / IJNZ / IJZ | INA / INB / INCMOD / INT_OFF / IRET1 / IRET2 / IRET3 / JATN / JCT1 / JCT2 / JCT3 / JFBW | JINT / JMP / JMPREL / JNATN / JNCT1 / JNCT2 / JNCT3 / JNFBW / JNINT / JNPAT / JNQMT / JNSE1 | JNSE2 / JNSE3 / JNSE4 / JNXFI / JNXMT / JNXRL / JNXRO / JPAT / JQMT / JSE1 / JSE2 / JSE3 | JSE4 / JXFI / JXMT / JXRL / JXRO |
|---|---|---|---|---|---|---|---|---|---|

## Table 45 — 1 rows × 11 cols

| LINE / LINESIZE / LOC / LOCKCHK / LOCKNEW | LOCKREL / LOCKRET / LOCKTRY / LOGIC / LOGSCALE | LONG / LONGFILL / LONGMOVE / LONGS_16BIT / LONGS_1BIT | LONGS_2BIT / LONGS_4BIT / LONGS_8BIT / LOOKDOWN / LOOKDOWNZ | LOOKUP / LOOKUPZ / LSTR / LSTR_ / LUMA8 | LUMA8W / LUMA8X / LUT1 / LUT2 / LUT4 | LUT8 / LUTCOLORS / MAG / MAGENTA / MERGEB | MERGEW / MIDI / MIXPIX / MODC / MODCZ | MODZ / MOV / MOVBYTS / MUL / MULDIV64 | MULPIX / MULS / MUXC / MUXNC / MUXNIBS | MUXNITS / MUXNZ / MUXQ / MUXZ |
|---|---|---|---|---|---|---|---|---|---|---|

## Table 46 — 1 rows × 10 cols

| NAN / NEG / NEGC / NEGNC | NEGNZ / NEGX / NEGZ / NEWCOG | NEXT / NIXINT1 / NIXINT2 / NIXINT3 | NOP / NOT / OBJ / OBOX | ONES / OPACITY / OR / ORANGE | ORC / ORG / ORGF / ORGH | ORIGIN / ORZ / OTHER / OUTA | OUTB / OUTC / OUTH / OUTL | OUTNC / OUTNOT / OUTNZ / OUTRND | OUTZ / OVAL |
|---|---|---|---|---|---|---|---|---|---|

## Table 47 — 1 rows × 9 cols

| P_ADC / P_ADC_100X / P_ADC_10X / P_ADC_1X / P_ADC_30X / P_ADC_3X / P_ADC_EXT / P_ADC_FLOAT / P_ADC_GIO / P_ADC_SCOPE / P_ADC_VIO / P_AND_AB / P_ASYNC_IO / P_ASYNC_RX / P_ASYNC_TX / P_BITDAC / P_CHANNEL / P_COMPARE_AB / P_COMPARE_AB_FB / P_COUNT_HIGHS | P_COUNT_RISES / P_COUNTER_HIGHS / P_COUNTER_PERIODS / P_COUNTER_TICKS / P_DAC_124R_3V / P_DAC_600R_2V / P_DAC_75R_2V / P_DAC_990R_3V / P_DAC_DITHER_PWM / P_DAC_DITHER_RND / P_DAC_NOISE / P_EVENTS_TICKS / P_FILT0_AB / P_FILT1_AB / P_FILT2_AB / P_FILT3_AB / P_HIGH_100UA / P_HIGH_10UA / P_HIGH_150K / P_HIGH_15K | P_HIGH_1K5 / P_HIGH_1MA / P_HIGH_FAST / P_HIGH_FLOAT / P_HIGH_TICKS / P_INVERT_A / P_INVERT_B / P_INVERT_IN / P_INVERT_OUT / P_INVERT_OUTPUT / P_LEVEL_A / P_LEVEL_A_FBN / P_LEVEL_B_FBN / P_LEVEL_B_FBP / P_LOCAL_A / P_LOCAL_B / P_LOGIC_A / P_LOGIC_A_FB / P_LOGIC_B_FB / P_LOW_100UA | P_LOW_10UA / P_LOW_150K / P_LOW_15K / P_LOW_1K5 / P_LOW_1MA / P_LOW_FAST / P_LOW_FLOAT / P_MINUS1_A / P_MINUS1_B / P_MINUS2_A / P_MINUS2_B / P_MINUS3_A / P_MINUS3_B / P_NCO_DUTY / P_NCO_FREQ / P_NORMAL / P_OE / P_OR_AB / P_OUTBIT_A / P_OUTBIT_B | P_PASS_AB / P_PERIODS_HIGHS / P_PERIODS_TICKS / P_PLUS1_A / P_PLUS1_B / P_PLUS2_A / P_PLUS2_B / P_PLUS3_A / P_PLUS3_B / P_PULSE / P_PWM_SAWTOOTH / P_PWM_SMPS / P_PWM_TRIANGLE / P_QUADRATURE / P_REG_UP / P_REG_UP_DOWN / P_REPOSITORY / P_SCHMITT_A / P_SCHMITT_A_FB / P_SCHMITT_B_FB | P_STATE_TICKS / P_SYNC_IO / P_SYNC_RX / P_SYNC_TX / P_TRANSITION / P_TRUE_A / P_TRUE_B / P_TRUE_IN / P_TRUE_OUT / P_TRUE_OUTPUT / P_TT_00 / P_TT_01 / P_TT_10 / P_TT_11 / P_USB_PAIR / P_XOR_AB / PA / PB / PC_KEY / PC_MOUSE | PI / PINCLEAR / PINF / PINFLOAT / PINH / PINHIGH / PINL / PINLOW / PINR / PINREAD / PINSTART / PINT / PINTOGGLE / PINW / PINWRITE / PLOT / POLAR / POLLATN / POLLCT / POLLCT1 | POLLCT2 / POLLCT3 / POLLFBW / POLLINT / POLLPAT / POLLQMT / POLLSE1 / POLLSE2 / POLLSE3 / POLLSE4 / POLLXFI / POLLXMT / POLLXRL / POLLXRO / POLXY / POP / POPA / POPB / POS / POSX | PR0 / PR1 / PR2 / PR3 / PR4 / PR5 / PR6 / PR7 / PRECISE / PRECOMPILE / PRI / PTRA / PTRB / PUB / PUSH / PUSHA / PUSHB |
|---|---|---|---|---|---|---|---|---|

## Table 48 — 1 rows × 11 cols

| QCOS / QDIV / QEXP / QFRAC / QLOG / QMUL | QROTATE / QSIN / QSQRT / QUIT / QVECTOR / RANGE | RATE / RCL / RCR / RCZL / RCZR / RDBYTE | RDFAST / RDLONG / RDLUT / RDPIN / RDWORD / RECV | RED / REG / REGEXEC / REGLOAD / REP / REPEAT | RES / RESI0 / RESI1 / RESI2 / RESI3 / RET | RETA / RETB / RETI0 / RETI1 / RETI2 / RETI3 | RETURN / REV / RFBYTE / RFLONG / RFVAR / RFVARS | RFWORD / RGB16 / RGB24 / RGB8 / RGBEXP / RGBI8 | RGBI8W / RGBI8X / RGBSQZ / ROL / ROLBYTE / ROLNIB | ROLWORD / ROR / ROTXY / ROUND / RQPIN |
|---|---|---|---|---|---|---|---|---|---|---|

## Table 49 — 1 rows × 8 cols

| SAL / SAMPLES / SAR / SAVE / SBIN / SBIN_ / SBIN_BYTE_ / SBIN_BYTE_ARRAY / SBIN_BYTE_ARRAY_ / SBIN_LONG / SBIN_LONG_ / SBIN_LONG_ARRAY / SBIN_LONG_ARRAY_ / SBIN_REG_ARRAY / SBIN_REG_ARRAY_ / SBIN_WORD / SBIN_WORD_ / SBIN_WORD_ARRAY | SBIN_WORD_ARRAY_ / SCA / SCAS / SCOPE / SCOPE_XY / SCROLL / SDEC / SDEC_ / SDEC_BYTE / SDEC_BYTE_ / SDEC_BYTE_ARRAY / SDEC_BYTE_ARRAY_ / SDEC_LONG / SDEC_LONG_ / SDEC_LONG_ARRAY / SDEC_LONG_ARRAY_ / SDEC_REG_ARRAY / SDEC_REG_ARRAY_ | SDEC_WORD / SDEC_WORD_ / SDEC_WORD_ARRAY / SDEC_WORD_ARRAY_ / SEND / SET / SETBYTE / SETCFRQ / SETCI / SETCMOD / SETCQ / SETCY / SETD / SETDACS / SETINT1 / SETINT2 / SETINT3 / SETLUTS | SETNIB / SETPAT / SETPIV / SETPIX / SETQ / SETQ2 / SETR / SETREGS / SETS / SETSCP / SETSE1 / SETSE2 / SETSE3 / SETSE4 / SETWORD / SETXFRQ / SEUSSF / SEUSSR | SHEX / SHEX_ / SHEX_BYTE / SHEX_BYTE_ / SHEX_BYTE_ARRAY / SHEX_BYTE_ARRAY_ / SHEX_LONG / SHEX_LONG_ / SHEX_LONG_ARRAY / SHEX_LONG_ARRAY_ / SHEX_REG_ARRAY / SHEX_REG_ARRAY_ / SHEX_WORD / SHEX_WORD_ / SHEX_WORD_ARRAY / SHEX_WORD_ARRAY_ / SHL / SHR | SIGNED / SIGNX / SIZE / SKIP / SKIPF / SPACING / SPECTRO / SPLITB / SPLITW / SPRITE / SPRITEDEF / SQRT / STALLI / STEP / STRCOMP / STRING / STRSIZE / SUB | SUBR / SUBS / SUBSX / SUBX / SUMC / SUMNC / SUMNZ / SUMZ / TERM / TEST / TESTB / TESTBN / TESTN / TESTP / TESTPN / TEXT / TEXTANGLE / TEXTSIZE | TEXTSTYLE / TITLE / TJF / TJNF / TJNS / TJNZ / TJS / TJV / TJZ / TO / TRACE / TRGINT1 / TRGINT2 / TRGINT3 / TRIGGER / TRUE / TRUNC |
|---|---|---|---|---|---|---|---|

## Table 50 — 1 rows × 7 cols

| UBIN / UBIN_ / UBIN_BYTE / UBIN_BYTE_ / UBIN_BYTE_ARRAY / UBIN_BYTE_ARRAY_ / UBIN_LONG / UBIN_LONG_ / UBIN_LONG_ARRAY / UBIN_LONG_ARRAY_ / UBIN_REG_ARRAY / UBIN_REG_ARRAY_ / UBIN_WORD / UBIN_WORD_ / UBIN_WORD_ARRAY | UBIN_WORD_ARRAY_ / UDEC / UDEC_ / UDEC_BYTE / UDEC_BYTE_ / UDEC_BYTE_ARRAY / UDEC_BYTE_ARRAY_ / UDEC_LONG / UDEC_LONG_ / UDEC_LONG_ARRAY / UDEC_LONG_ARRAY_ / UDEC_REG_ARRAY / UDEC_REG_ARRAY_ / UDEC_WORD / UDEC_WORD_ | UDEC_WORD_ARRAY / UDEC_WORD_ARRAY_ / UHEX / UHEX_ / UHEX_BYTE / UHEX_BYTE_ / UHEX_BYTE_ARRAY / UHEX_BYTE_ARRAY_ / UHEX_LONG / UHEX_LONG_ / UHEX_LONG_ARRAY / UHEX_LONG_ARRAY_ / UHEX_REG_ARRAY / UHEX_REG_ARRAY_ / UHEX_WORD | UHEX_WORD_ / UHEX_WORD_ARRAY / UHEX_WORD_ARRAY_ / UNTIL / UPDATE / VAR / VARBASE / WAITATN / WAITCT / WAITCT1 / WAITCT2 / WAITCT3 / WAITFBW / WAITINT / WAITMS | WAITPAT / WAITSE1 / WAITSE2 / WAITSE3 / WAITSE4 / WAITUS / WAITX / WAITXFI / WAITXMT / WAITXRL / WAITXRO / WC / WCZ / WFBYTE / WFLONG | WFWORD / WHILE / WHITE / WINDOW / WMLONG / WORD / WORDFILL / WORDMOVE / WORDS_1BIT / WORDS_2BIT / WORDS_4BIT / WORDS_8BIT / WRBYTE / WRC / WRFAST | WRLONG / WRLUT / WRNC / WRNZ / WRPIN / WRWORD / WRZ / WXPIN / WYPIN / WZ |
|---|---|---|---|---|---|---|

## Table 51 — 1 rows × 6 cols

| X_16P_2DAC8_WFWORD / X_16P_4DAC4_WFWORD / X_1ADC8_0P_1DAC8_WFBYTE / X_1ADC8_8P_2DAC8_WFWORD / X_1P_1DAC1_WFBYTE / X_2ADC8_0P_2DAC8_WFWORD / X_2ADC8_16P_4DAC8_WFLONG / X_2P_1DAC2_WFBYTE / X_2P_2DAC1_WFBYTE / X_32P_4DAC8_WFLONG / X_4ADC8_0P_4DAC8_WFLONG / X_4P_1DAC4_WFBYTE / X_4P_2DAC2_WFBYTE / X_4P_4DAC1_WFBYTE / X_8P_1DAC8_WFBYTE / X_8P_2DAC4_WFBYTE | X_8P_4DAC2_WFBYTE / X_ALT_OFF / X_ALT_ON / X_DACS_0_0_0_0 / X_DACS_0_0_X_X / X_DACS_0_X_X_X / X_DACS_0N0_0N0 / X_DACS_0N0_X_X / X_DACS_1_0_1_0 / X_DACS_1_0_X_X / X_DACS_1N1_0N0 / X_DACS_3_2_1_0 / X_DACS_OFF / X_DACS_X_0_X_X / X_DACS_X_X_0_0 / X_DACS_X_X_0_X | X_DACS_X_X_0N0 / X_DACS_X_X_1_0 / X_DACS_X_X_X_0 / X_DDS_GOERTZEL_SINC1 / X_DDS_GOERTZEL_SINC2 / X_IMM_16X2_1DAC2 / X_IMM_16X2_2DAC1 / X_IMM_16X2_LUT / X_IMM_1X32_4DAC8 / X_IMM_2X16_2DAC8 / X_IMM_2X16_4DAC4 / X_IMM_32X1_1DAC1 / X_IMM_32X1_LUT / X_IMM_4X8_1DAC8 / X_IMM_4X8_2DAC4 / X_IMM_4X8_4DAC2 | X_IMM_4X8_LUT / X_IMM_8X4_1DAC4 / X_IMM_8X4_2DAC2 / X_IMM_8X4_4DAC1 / X_IMM_8X4_LUT / X_PINS_OFF / X_PINS_ON / X_RFBYTE_1P_1DAC1 / X_RFBYTE_2P_1DAC2 / X_RFBYTE_2P_2DAC1 / X_RFBYTE_4P_1DAC4 / X_RFBYTE_4P_2DAC2 / X_RFBYTE_4P_4DAC1 / X_RFBYTE_8P_1DAC8 / X_RFBYTE_8P_2DAC4 / X_RFBYTE_8P_4DAC2 | X_RFBYTE_LUMA8 / X_RFBYTE_RGB8 / X_RFBYTE_RGBI8 / X_RFLONG_16X2_LUT / X_RFLONG_32P_4DAC8 / X_RFLONG_32X1_LUT / X_RFLONG_4X8_LUT / X_RFLONG_8X4_LUT / X_RFLONG_RGB24 / X_RFWORD_16P_2DAC8 / X_RFWORD_16P_4DAC4 / X_RFWORD_RGB16 / X_WRITE_OFF / X_WRITE_ON / XCONT / XINIT | XOR / XORC / XORO32 / XORZ / XSTOP / XYPOL / XZERO / YELLOW / ZEROX / ZSTR / ZSTR_ |
|---|---|---|---|---|---|

## Table 52 — 4 rows × 2 cols

| Date | Notes |
|---|---|
| 09/09/2021 | First public draft release. |
| 10/15/2021 | Enhanced Instruction Pipeline diagrams and explanations, and added Wait and Branch examples. |
| 11/01/2022 | Added underscore, ALL CAPS and <all_lowercase> to Conventions.  Clarified CORDIC Solver result availability.  Clarified System Counter upper and lower usage.  Added floating point, sprite, and debug keyboard and mouse symbols to Propeller 2 Reserved Words. |

## Table 53 — 2 rows × 4 cols

| Parallax Inc. / 599 Menlo Drive, Suite 100 / Rocklin, CA 95765 / USA | Office: +1 916-624-8333 / Toll Free US: 888-512-1024 | sales@parallax.com / support@parallax.com | www.parallax.com/p2 / forums.parallax.com |
|---|---|---|---|
| Purchase of the P2X8C4M64P does not include any license to emulate any other device nor to communicate via any specific proprietary protocol;  P2X8C4M64P connectivity objects and code examples provided or referenced by Parallax, Inc. are NOT licensed and are provided for research and development purposes only; end users must seek permission to use licensed protocols for their applications and products from the protocol license holders. / Parallax,  Inc. makes  no  warranty,  representation  or  guarantee  regarding  the  suitability  of  its  products  for  any  particular  purpose,  nor  does  Parallax,  Inc.  assume  any  liability  arising  out  of  the  application  or  use  of  any  product, and specifically disclaims any and all liability, including without limitation consequential or incidental damages even if Parallax, Inc.  has  been  advised  of  the  possibility  of  such  damages.   / Copyright © 2022 Parallax, Inc. All rights are reserved. Parallax, the Parallax logo, the P2 logo, and Propeller are trademarks of Parallax, Inc. |  |  |  |
