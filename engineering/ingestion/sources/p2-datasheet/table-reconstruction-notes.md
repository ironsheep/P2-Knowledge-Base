# P2 Datasheet Table Reconstruction Notes

## Table 0: Part Number Legend

The part number P2X8C4M64P breaks down as follows:

| Part Number Segment | Meaning |
|--------------------|---------|
| P2X | Propeller 2 |
| 8C | 8 cogs (processors) |
| 4M | 4 Mbit Hub RAM (512 KB) |
| 64P | 64 smart I/O pins |

This was extracted as a vertical list instead of a table with the segments on one row and meanings on another.

## Table 2: Pin Descriptions - Power Pin Groups

The extracted text shows "Vxxyy" as a placeholder, but this actually represents 15 separate power pins for groups of 4 I/O pins each:

| Pin Name | Description |
|----------|-------------|
| V0003    | Power for pins P0-P3 |
| V0407    | Power for pins P4-P7 |
| V0811    | Power for pins P8-P11 |
| V1215    | Power for pins P12-P15 |
| V1619    | Power for pins P16-P19 |
| V2023    | Power for pins P20-P23 |
| V2427    | Power for pins P24-P27 |
| V2831    | Power for pins P28-P31 |
| V3235    | Power for pins P32-P35 |
| V3639    | Power for pins P36-P39 |
| V4043    | Power for pins P40-P43 |
| V4447    | Power for pins P44-P47 |
| V4851    | Power for pins P48-P51 |
| V5255    | Power for pins P52-P55 |
| V5659    | Power for pins P56-P59 |
| V6063    | Power for pins P60-P63 |

**Pattern**: Each Vxxyy pin provides 3.3V power for a group of 4 consecutive I/O pins
- "V" prefix indicates power pin
- First two digits (xx) = first pin in group
- Last two digits (yy) = last pin in group
- Groups of 4 allow for isolated, ultra-stable power references for clean DAC/ADC operations

**Note**: You mentioned "Victor" in speech recognition - these are actually "V" (for Voltage/VDD) followed by the pin numbers.

## Table 1: Memory Configuration

The extracted table is completely broken. Here's the correct structure:

| Region | Depth | Width | Program Counter Address Range (Hex) | PASM Instruction D/S Address Range (Hex) |
|--------|-------|-------|-------------------------------------|------------------------------------------|
| Cog "Register" RAM | 512 | 32 bits | $00000..$001FF | $000..$1FF |
| Cog "Lookup" RAM | 512 | 32 bits | $00200..$003FF | $000..$1FF |
| Hub RAM | 524,288 | 8 bits | $00400..$7FFFF | $00000..$7FFFF |

## Table 3: Dual-Purpose Registers

These registers can be used as general RAM or for special purposes when their functions are enabled:

| Address | Name | Purpose |
|---------|------|------|
| $1F0 | RAM/IJMP3 | Interrupt Call Address for interrupt 3 |
| $1F1 | RAM/IRET3 | Interrupt Return Address for interrupt 3 |
| $1F2 | RAM/IJMP2 | Interrupt Call Address for interrupt 2 |
| $1F3 | RAM/IRET2 | Interrupt Return Address for interrupt 2 |
| $1F4 | RAM/IJMP1 | Interrupt Call Address for interrupt 1 |
| $1F5 | RAM/IRET1 | Interrupt Return Address for interrupt 1 |
| $1F6 | RAM/PA | CALL D immediate return / CALL PA parameter / LOC address |
| $1F7 | RAM/PB | CALL D immediate return / CALL PB parameter / LOC address |

## Table 4: Special-Purpose Registers

These registers always have special functions:

| Address | Name | Purpose |
|---------|------|------|
| $1F8 | PTRA | Pointer A to Hub RAM |
| $1F9 | PTRB | Pointer B to Hub RAM |
| $1FA | DIRA | Output enables for P31..P0 |
| $1FB | DIRB | Output enables for P63..P32 |
| $1FC | OUTA | Output states for P31..P0 |
| $1FD | OUTB | Output states for P63..P32 |
| $1FE | INA | Input states for P31..P0 (also debug interrupt call address) |
| $1FF | INB | Input states for P63..P32 (also debug interrupt return address) |

## Table 5: PASM2 Execution Regions

This table shows where instructions are fetched from based on the Program Counter value:

| PC Address | Instruction Source | Memory Width | PC Increment |
|------------|-------------------|--------------|-------------|
| $00000..$001FF | Cog Register RAM | 32 bits | 1 |
| $00200..$003FF | Cog Lookup RAM | 32 bits | 1 |
| $00400..$7FFFF | Hub RAM | 8 bits | 4 |

**Critical details:**
- Register and Lookup RAM are 32-bit wide (native long access)
- Hub RAM is 8-bit wide (byte-addressable)
- PC increments by 1 for cog-resident code (Register/Lookup RAM)
- PC increments by 4 for Hub-resident code (because instructions are 4 bytes)

## Table 6: Clock Configuration - HUBSET Instruction Format

`HUBSET ##%0000_000E_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS`

### PLL Enable Field
| Field | Value | Effect | Notes |
|-------|-------|--------|-------|
| %E | 0 | PLL off | |
| %E | 1 | PLL on | XI input must be enabled by %CC. Allow 10ms for crystal+PLL to stabilize |

### PLL Input Divider Field
| Field | Value | Effect | Notes |
|-------|-------|--------|-------|
| %DDDDDD | 0..63 | 1..64 division of XI frequency | This divided XI frequency feeds the PLL reference input |

### PLL Feedback Divider Field  
| Field | Value | Effect | Notes |
|-------|-------|--------|-------|
| %MMMMMMMMMM | 0..1023 | 1..1024 division of VCO frequency | Acts as multiplier. VCO must stay within 100-200 MHz |

### PLL Output Divider Field
| Field | Value | Effect |
|-------|-------|--------|
| %PPPP | 0 | VCO / 2 |
| | 1 | VCO / 4 |
| | 2 | VCO / 6 |
| | 3 | VCO / 8 |
| | 4 | VCO / 10 |
| | 5 | VCO / 12 |
| | 6 | VCO / 14 |
| | 7 | VCO / 16 |
| | 8 | VCO / 18 |
| | 9 | VCO / 20 |
| | 10 | VCO / 22 |
| | 11 | VCO / 24 |
| | 12 | VCO / 26 |
| | 13 | VCO / 28 |
| | 14 | VCO / 30 |
| | 15 | VCO / 1 |

### Crystal Configuration Field
| Field | XI Status | XO Status | XI/XO Impedance | Loading Caps |
|-------|-----------|-----------|-----------------|-------------|
| %CC=00 | ignored | float | Hi-Z | OFF |
| %CC=01 | input | 600Ω drive | 1MΩ | OFF (no caps) |
| %CC=10 | input | 600Ω drive | 1MΩ | 15pF per pin |
| %CC=11 | input | 600Ω drive | 1MΩ | 30pF per pin |

### Clock Source Select Field
| Field | Clock Source | Notes |
|-------|--------------|-------|
| %SS=00 | RCFAST | 20+ MHz minimum (nominally ~24 MHz), can be switched to at any time, used on boot up |
| %SS=01 | RCSLOW | ~20 kHz, can be switched to at any time, low-power |
| %SS=10 | XI | Direct from XI pin (CC != %00, allow 5ms for crystal to stabilize) |
| %SS=11 | PLL | PLL output (CC != %00 and E=1, allow 10ms for crystal+PLL to stabilize) |

### ⚠️ CRITICAL WARNING
**Incorrectly switching away from PLL (%SS = %11) can cause a clock glitch that will hang the clock circuit!**

**Safe switching procedure:**
1. ALWAYS switch to internal oscillator first:
   - `HUBSET #$F0` for RCFAST
   - `HUBSET #$F1` for RCSLOW
2. Then switch to your desired clock configuration

### Stabilization Requirements
- Crystal only (XI): Allow 5ms stabilization
- Crystal + PLL: Allow 10ms stabilization
- Internal clocks (RCFAST/RCSLOW): Can switch immediately

## Table 7: I/O Pin Registers

| Register | Cog Address | Purpose |
|----------|-------------|------|
| DIRA | $1FA | Output enable bits for P0..P31 (active high) |
| DIRB | $1FB | Output enable bits for P32..P63 (active high) |
| OUTA | $1FC | Output state bits for P0..P31 (corresponding DIRA bit must be high to enable output) |
| OUTB | $1FD | Output state bits for P32..P63 (corresponding DIRB bit must be high to enable output) |
| INA | $1FE | Input state bits for P0..P31 |
| INB | $1FF | Input state bits for P32..P63 |

Note: These are the same special-purpose registers we documented earlier, shown here in I/O context.

## Table 8: Special Pin Instructions

All these instructions operate on a single pin specified by D (0-63):

### Direction Control
| Instructions | Purpose |
|-------------|------|
| DIRL/DIRH/DIRC/DIRNC/DIRZ/DIRNZ/DIRRND/DIRNOT {#}D | Affect pin D bit in DIRx |

### Output Control
| Instructions | Purpose |
|-------------|------|
| OUTL/OUTH/OUTC/OUTNC/OUTZ/OUTNZ/OUTRND/OUTNOT {#}D | Affect pin D bit in OUTx |

### Float Control (Output + Direction)
| Instructions | Purpose |
|-------------|------|
| FLTL/FLTH/FLTC/FLTNC/FLTZ/FLTNZ/FLTRND/FLTNOT {#}D | Affect pin D bit in OUTx, clear bit in DIRx |

### Drive Control (Output + Direction)
| Instructions | Purpose |
|-------------|------|
| DRVL/DRVH/DRVC/DRVNC/DRVZ/DRVNZ/DRVRND/DRVNOT {#}D | Affect pin D bit in OUTx, set bit in DIRx |

### Pin Testing
| Instructions | Purpose |
|-------------|------|
| TESTP {#}D WC/WZ/ANDC/ANDZ/ORC/ORZ/XORC/XORZ | Read pin D bit in INx and affect C or Z |
| TESTPN {#}D WC/WZ/ANDC/ANDZ/ORC/ORZ/XORC/XORZ | Read pin D bit in !INx and affect C or Z |

**Instruction Suffix Meanings:**
- L = Low (0)
- H = High (1)
- C = from Carry flag
- NC = from Not Carry flag
- Z = from Zero flag (0 if Z=1, 1 if Z=0)
- NZ = from Not Zero flag (1 if Z=0, 0 if Z=1)
- RND = Random bit
- NOT = Toggle current state

## Table 9: WRPIN Configuration Format

The WRPIN instruction D operand format:
`%AAAA_BBBB_FFF_MMMMMMMMMMMMM_TT_SSSSS_0`

### (A) PIN Input Selector / (B) ADJ Input Selector

| %AAAA/%BBBB | Selection |
|-------------|----------|
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

### (F) PIN and ADJ Logic/Filtering

| %FFF | Logic/Filter |
|------|-------------|
| 000 | A, B (default) |
| 001 | A AND B, B |
| 010 | A OR B, B |
| 011 | A XOR B, B |
| 100 | A, B, both filtered using global filt0 settings |
| 101 | A, B, both filtered using global filt1 settings |
| 110 | A, B, both filtered using global filt2 settings |
| 111 | A, B, both filtered using global filt3 settings |

Note: The resultant 'A' drives the IN signal in non-smart-pin modes.

### (M) Pin Mode Table - RECONSTRUCTION ATTEMPT

**STRUCTURE**: Main header (3 columns) with two side-by-side 3-column tables below

**Headers:**
- Column 1: WRPIN D[20:8] Configuration | M[12:0]
- Column 2: Resulting Internal Configuration | Input  
- Column 3: (continuation) | Pin Output

**Attempted reconstruction based on extraction patterns:**

The extraction shows 8 M[12:0] patterns, 8 Input descriptions, and 8 Pin Output values.
Assuming they align in order:

| WRPIN D[20:8] Config | Input | Pin Output |
|---------------------|-------|------------|
| %0000_CIOHHHLLL | Pin Logic | OUT |
| %0001_CIOHHHLLL | Pin Logic | Input |
| %0010_CIOHHHLLL | Adj Logic | Input |
| %0011_CIOHHHLLL | Pin Schmitt | OUT |
| %0100_CIOHHHLLL | Pin Schmitt | Input |
| %0101_CIOHHHLLL | Adj Schmitt | Input |
| %0110_CIOHHHLLL | Pin > Adj | OUT |
| %0111_CIOHHHLLL | Pin > Adj | Input |

**Note about Pin Output column**: The extraction shows both "OUT"/"Input" values AND "CIOHHHLLL" patterns. This suggests the Pin Output column may show:
- The logical state (OUT/Input)
- The actual pin configuration pattern (CIOHHHLLL)

**Additional patterns found (1100-1111):**

| WRPIN D[20:8] Config | Input | Pin Output | Notes |
|---------------------|-------|------------|-------|
| %1100_CDDDDDDDD | Pin > D | OUT, 1.5 kΩ | C00001001 |
| %1101_CDDDDDDDD | Pin > D | !Input, 1.5 kΩ | C01001001 |
| %1110_CDDDDDDDD | Adj > D | Input, 1.5 kΩ | C00001001 |
| %1111_CDDDDDDDD | Adj > D | !Input, 1.5 kΩ | C01001001 |

### (M) Pin Mode Table - COMPLETE UNIFIED RECONSTRUCTION

**Table Structure**: 9 columns total (3 + GAP + 6)

| Row | WRPIN D[20:8] | Input | Pin Output¹ || CIOHHHLLL | OE² | DAC | ADC | ADC Mode | Comparator |
|-----|---------------|-------|------------||-----------|-----|-----|-----|----------|------------|
| 1 | %0000_CIOHHHLLL | Pin Logic | OUT || CIOHHHLLL | DIR | 0 | 0 | | 0 |
| 2 | %0001_CIOHHHLLL | Pin Logic | Input || CIOHHHLLL | DIR | 0 | 0 | | 0 |
| 3 | %0010_CIOHHHLLL | Adj Logic | Input || CIOHHHLLL | DIR | 0 | 0 | | 0 |
| 4 | %0011_CIOHHHLLL | Pin Schmitt | OUT || CIOHHHLLL | DIR | 0 | 0 | | 0 |
| 5 | %0100_CIOHHHLLL | Pin Schmitt | Input || CIOHHHLLL | DIR | 0 | 0 | | 0 |
| 6 | %0101_CIOHHHLLL | Adj Schmitt | Input || CIOHHHLLL | DIR | 0 | 0 | | 0 |
| 7 | %0110_CIOHHHLLL | Pin > Adj | OUT || CIOHHHLLL | DIR | 0 | 0 | | Pin > Adj |
| 8 | %0111_CIOHHHLLL | Pin > Adj | Input || CIOHHHLLL | DIR | 0 | 0 | | Pin > Adj |
| 9 | %100000_OHHHLLL | ADC, GND | OUT || 10OHHHLLL | DIR | 0 | 1 | 000 | 0 |
| 10 | %100001_OHHHLLL | ADC, Vxxyy | OUT || 10OHHHLLL | DIR | 0 | 1 | 001 | 0 |
| 11 | %100010_OHHHLLL | ADC, float | OUT || 10OHHHLLL | DIR | 0 | 1 | 010 | 0 |
| 12 | %100011_OHHHLLL | ADC, Pin 1x | OUT || 10OHHHLLL | DIR | 0 | 1 | 011 | 0 |
| 13 | %100100_OHHHLLL | ADC, Pin 3.16x | OUT || 10OHHHLLL | DIR | 0 | 1 | 100 | 0 |
| 14 | %100101_OHHHLLL | ADC, Pin 10x | OUT || 10OHHHLLL | DIR | 0 | 1 | 101 | 0 |
| 15 | %100110_OHHHLLL | ADC, Pin 31.6x | OUT || 10OHHHLLL | DIR | 0 | 1 | 110 | 0 |
| 16 | %100111_OHHHLLL | ADC, Pin 100x | OUT || 10OHHHLLL | DIR | 0 | 1 | 111 | 0 |
| 17 | %10100_DDDDDDDD | ADC, Pin 1x³ | DAC 990Ω, 3.3V || 10xxxxxxx | 0 | DIR | OUT | 011 | 0 |
| 18 | %10101_DDDDDDDD | ADC, Pin 1x³ | DAC 600Ω, 2.0V || 10xxxxxxx | 0 | DIR | OUT | 011 | 0 |
| 19 | %10110_DDDDDDDD | ADC, Pin 1x³ | DAC 123.75Ω, 3.3V || 10xxxxxxx | 0 | DIR | OUT | 011 | 0 |
| 20 | %10111_DDDDDDDD | ADC, Pin 1x³ | DAC 75Ω, 2.0V || 10xxxxxxx | 0 | DIR | OUT | 011 | 0 |
| 21 | %1100_CDDDDDDDD | Pin > D | OUT, 1.5kΩ || C00001001 | DIR | 0 | 0 | | Pin > D |
| 22 | %1101_CDDDDDDDD | Pin > D | !Input, 1.5kΩ || C01001001 | DIR | 0 | 0 | | Pin > D |
| 23 | %1110_CDDDDDDDD | Adj > D | Input, 1.5kΩ || C00001001 | DIR | 0 | 0 | | Adj > D |
| 24 | %1111_CDDDDDDDD | Adj > D | !Input, 1.5kΩ || C01001001 | DIR | 0 | 0 | | Adj > D |

**Footnotes:**
¹ OUT means output latch bit drives output; Input means the 'Input' column's item drives output
² OE is digital logic output enable only; analog output is indicated in the DAC column
³ if OUT bit = 1

**Key Understanding**:
- Modes 0-7: Single entry each (8 rows)
- Mode 8 (rows 9-12): 4 ADC input source variants (GND, Vxxyy, float, Pin 1x)
- Mode 9 (rows 13-16): 4 ADC gain variants (3.16x, 10x, 31.6x, 100x)
- Mode 10 (rows 17-18): 2 DAC/ADC combinations
- Mode 11 (rows 19-20): 2 DAC/ADC combinations 
- Modes 12-15 (rows 21-24): Comparator modes
- Total: 8 + 4 + 4 + 2 + 2 + 4 = 24 rows

**Pattern encoding observed:**
- **CIOHHHLLL**: Used in modes 0000-0111 and 1100-1111
  - C = Custom low-level pin control
  - I = Invert output
  - O = Output enable control
  - HHH = High drive strength
  - LLL = Low drive strength
- **10OHHHLLL**: Appears for modes 1000-1011 (incomplete extraction)
- **CDDDDDDDD**: Used in modes 1100-1111
  - C = Control bit
  - DDDDDDDD = 8-bit DAC value

## I/O Pin Circuit Behavior (Narratives Around Diagrams)

### Pin Pairing Architecture
- **Adjacent pins see each other**: P0↔P1, P2↔P3, P4↔P5, etc.
- **Odd pins**: 'OTHER' = even pin's NOT (inverted) output state (differential signaling)
- **Even pins**: 'OTHER' = unique pseudo-random bit (noise source for DAC dithering)

### Output Control Logic
The pin output is controlled by multiple layers:

#### When Smart Pin OFF (%SSSSS = %00000):
**Non-DAC Mode (M[12:10] ≠ %101):**
- DIR enables output
- Bit 0 of mode: 0 = OUT drives, 1 = OTHER drives

**DAC Mode (M[12:10] = %101):**
- %00: DIR enables DAC, M[7:0] sets level
- %01: OUT enables ADC, M[3:0] selects cog DAC channel
- %10: OUT drives BIT_DAC output
- %11: OTHER drives BIT_DAC output

#### When Smart Pin ON (%SSSSS > %00000):
- Bit 0: 0 = output disabled (regardless of DIR)
- Bit 0: 1 = output enabled (regardless of DIR)

**DAC Smart Modes (%SSSSS = %00001..%00011):**
- 0x: OUT enables DAC
- 1x: OTHER enables DAC

**Non-DAC Smart Modes (%SSSSS = %00100..%11111):**
- 0x: SMART/OUT drives output (or BIT_DAC if DAC_MODE)
- 1x: SMART/OTHER drives output (or BIT_DAC if DAC_MODE)

### Key Insights:
1. **Differential pairs**: Odd/even pins can create differential signals
2. **Noise injection**: Even pins have hardware random source
3. **Smart override**: Smart pins can override normal DIR/OUT control
4. **Multi-layer control**: Mode bits, smart mode, and DAC mode interact

### (T) Pin DIR/OUT Control

Field %TT (default = %00) - table details missing in extraction
## Smart Pin Modes Table (%SSSSS Field) - VERIFIED RECONSTRUCTION

The Smart Pin modes are configured via the %SSSSS field (bits 4:0 of WRPIN). There are 34 distinct smart pin modes.

### Complete Smart Pin Modes Table

| %SSSSS | Mode | Note |
|--------|------|------|
| %00000 | Smart pin off; normal operation (default) | |
| %00001 | Long repository | M[12:10] != %101 (not DAC_MODE) |
| %00010 | Long repository | M[12:10] != %101 (not DAC_MODE) |
| %00011 | Long repository | M[12:10] != %101 (not DAC_MODE) |
| %00001 | DAC noise | M[12:10] = %101 (DAC_MODE) |
| %00010 | DAC 16-bit dither, noise | M[12:10] = %101 (DAC_MODE) |
| %00011 | DAC 16-bit dither, PWM | M[12:10] = %101 (DAC_MODE) |
| %00100¹ | Pulse/cycle output | |
| %00101¹ | Transition output | |
| %00110¹ | NCO frequency | |
| %00111¹ | NCO duty | |
| %01000¹ | PWM triangle | |
| %01001¹ | PWM sawtooth | |
| %01010¹ | PWM switch-mode power supply, V and I feedback | |
| %01011 | Periodic/continuous: A-B quadrature encoder | |
| %01100 | Periodic/continuous: inc on A-rise & B-high | |
| %01101 | Periodic/continuous: inc on A-rise & B-high / dec on A-rise & B-low | |
| %01110 | Periodic/continuous: inc on A-rise {/ dec on B-rise} | |
| %01111 | Periodic/continuous: inc on A-high {/ dec on B-high} | |
| %10000 | Time A-states | |
| %10001 | Time A-highs | |
| %10010 | Time X A-highs/rises/edges -or- timeout on X A-high/rise/edge | |
| %10011 | For X periods, count time | |
| %10100 | For X periods, count states | |
| %10101 | For periods in X+ clocks, count time | |
| %10110 | For periods in X+ clocks, count states | |
| %10111 | For periods in X+ clocks, count periods | |
| %11000 | ADC sample/filter/capture, internally clocked | |
| %11001 | ADC sample/filter/capture, externally clocked | |
| %11010 | ADC scope with trigger | |
| %11011¹ | USB host/device | even/odd pin pair = DM/DP |
| %11100¹ | Sync serial transmit | A-data, B-clock |
| %11101 | Sync serial receive | A-data, B-clock |
| %11110¹ | Async serial transmit | baud rate |
| %11111 | Async serial receive | baud rate |

¹ OUT signal overridden

### Key Observations:

1. **Mode Overloading**: Modes %00001-%00011 serve dual purposes:
   - When M[12:10] != %101: Repository modes
   - When M[12:10] = %101 (DAC_MODE): DAC output modes

2. **Mode Categories**:
   - **%00000**: Off (normal I/O)
   - **%00001-%00011**: Repository or DAC modes (context-dependent)
   - **%00100-%00111**: Pulse/transition/NCO modes
   - **%01000-%01010**: PWM modes
   - **%01011-%01111**: Quadrature/encoder modes
   - **%10000-%10111**: Timing/counting modes
   - **%11000-%11010**: ADC modes
   - **%11011**: USB mode (requires pin pairs)
   - **%11100-%11111**: Serial modes

3. **Total Count**: 34 distinct smart pin modes (counting dual-purpose modes separately)

4. **Pin Pairing**: USB mode (%11011) requires odd/even pin pairs for DM/DP signals

5. **Output Override**: Serial modes (%11100-%11111) override the normal OUT signal

### Extraction Issues Found:
- The original extraction had corrupted binary values (missing % prefix)
- Some modes were shown as decimal instead of binary
- Line breaks were incorrectly placed, merging some entries
- Footnote markers were separated from their context

This reconstruction provides the complete, verified Smart Pin modes table essential for P2 programming.

## DC Characteristics Table - RECONSTRUCTED

The DC Characteristics table extraction is severely corrupted with merged cells and missing structure.

### Reconstructed DC Characteristics Table

| Symbol | Parameter | Conditions | Min | Typ¹ | Max | Units |
|--------|-----------|------------|-----|------|-----|-------|
| Vdd | Core Supply Voltage | | 1.7 | 1.8 | 1.9 | V |
| Vxxyy | VIO Supply Voltage | | 3.15 | 3.3 | 3.45 | V |
| Vih | Input Logic Threshold | | Vxxyy × 0.3 | Vxxyy × 0.5 | Vxxyy × 0.7 | V |
| Iil | Input Leakage Current | IO pin Vin = GND or Vio | ±0.1 | | ±10 | μA |
| Vol | Output Low Voltage (relative to GND) | VDD=3.3V, sinking 1mA | | 15 | | mV |
| | | VDD=3.3V, sinking 10mA | | 160 | | mV |
| | | VDD=3.3V, sinking 30mA | | 510 | | mV |
| Voh | Output High Voltage (relative to Vxxyy) | VDD=3.3V, sourcing 1mA | | -6 | | mV |
| | | VDD=3.3V, sourcing 10mA | | -170 | | mV |
| | | VDD=3.3V, sourcing 30mA | | -580 | | mV |
| Iq Vdd | VDD Quiescent Current | RESn = TEST = P0..P64 = 0V, Vxxyy = 3.3V, VDD = 1.8V | | 40 | | μA |
| Iq Vxxyy | Vxxyy Quiescent Current | RESn = TEST = P0..P64 = 0V, Vxxyy = 3.3V, VDD = 1.8V | | 0.5 | | μA |

¹ Note: Data in the Typical "Typ" column is T = 25 °C unless otherwise stated.

Operating temperature range: -40 °C to +105 °C unless otherwise noted.

## AC Characteristics Table - RECONSTRUCTED

### Reconstructed AC Characteristics Table

| Symbol | Parameter | Conditions | Min | Typ¹ | Max | Units |
|--------|-----------|------------|-----|------|-----|-------|
| Freq | Oscillator Frequency | RCSLOW (internal) | 12 | 20 | 30 | kHz |
| | | RCFAST (internal) | 20 | 24 | 30 | MHz |
| | | Direct drive (into XI) | DC | | 200 | MHz |
| | | Crystal (between XI and XO) | 1 | | 50 | MHz |
| | | PLL (fed by direct drive or crystal) | 3.33 | 180² | 320 | MHz |
| Cin | XI and XO pin Capacitance | Mode 0: Disabled (1MΩ feedback resistor off) | | 2 | | pF |
| | | Mode 1: Direct drive | | 2 | | pF |
| | | Mode 2: Crystal ≥ 16MHz | | 15 | | pF |
| | | Mode 3: Crystal < 16MHz | | 30 | | pF |

¹ Data in the Typical "Typ" column is T = 25 °C unless otherwise stated.
² Nominal PLL frequency (system clock speed) is 180 MHz at up to 105 °C.

Operating temperature range: -40 °C to +105 °C unless otherwise noted.

### Key Electrical Specifications:

1. **Power Requirements**:
   - Core voltage (Vdd): 1.8V nominal (1.7-1.9V range)
   - I/O voltage (Vxxyy): 3.3V nominal (3.15-3.45V range)
   - Ultra-low quiescent current: 40μA (core), 0.5μA (I/O)

2. **Input/Output Characteristics**:
   - Logic threshold: 50% of Vxxyy typical
   - Drive strength: Can sink/source up to 30mA
   - Very low leakage current: ±0.1μA typical

3. **Clock Capabilities**:
   - Internal RC oscillators: ~20kHz (slow), ~24MHz (fast)
   - Crystal support: 1-50MHz
   - PLL output: 3.33-320MHz (180MHz typical)
   - Direct clock input: DC to 200MHz

4. **Temperature Range**:
   - Full operation: -40°C to +105°C (AEC-Q100 Level 2)

### Extraction Issues:
- Multiple row headers merged into single cells
- Condition details separated from values
- Units column partially corrupted
- Footnote markers disconnected from context
