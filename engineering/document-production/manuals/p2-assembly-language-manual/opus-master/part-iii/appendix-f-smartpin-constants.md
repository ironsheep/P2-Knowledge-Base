# Appendix F: Smart Pin Mode Constants

PASM2 provides an extensive set of predefined constants for configuring the P2's 64 Smart Pins. These constants replace complex 32-bit configuration patterns with readable symbolic names, making SmartPin programming practical and maintainable.

## SmartPin Configuration Word Structure

Each SmartPin is configured through a 32-bit mode word with the following structure:

```
Bits [31..0] = %AAAA_BBBB_FFF_PPPPPPPPPPPPP_TT_MMMMM_0
```

| Field | Bits | Purpose |
|-------|------|---------|
| AAAA | 31-28 | A input selector (polarity and source) |
| BBBB | 27-24 | B input selector (polarity and source) |
| FFF | 23-21 | A/B input logic and filter settings |
| P | 20-8 | Low-level pin mode and parameters |
| TT | 7-6 | DIR/OUT control mode |
| MMMMM | 5-1 | Smart pin operating mode (0-31) |
| 0 | 0 | Reserved (must be 0) |

Constants are combined using OR operations to build the complete configuration:

```pasm
        mov     mode, ##P_PWM_TRIANGLE | P_OE | P_LOCAL_A
        wrpin   mode, #56
```



## A Input Configuration

### A Input Polarity (pick one)

| Constant | Value | Description |
|----------|-------|-------------|
| P_TRUE_A | %0000_0000_000_0000000000000_00_00000_0 | True A input (default) |
| P_INVERT_A | %1000_0000_000_0000000000000_00_00000_0 | Invert A input |

### A Input Selection (pick one)

| Constant | Value | Description |
|----------|-------|-------------|
| P_LOCAL_A | %0000_0000_000_0000000000000_00_00000_0 | Select local pin for A input (default) |
| P_PLUS1_A | %0001_0000_000_0000000000000_00_00000_0 | Select pin+1 for A input |
| P_PLUS2_A | %0010_0000_000_0000000000000_00_00000_0 | Select pin+2 for A input |
| P_PLUS3_A | %0011_0000_000_0000000000000_00_00000_0 | Select pin+3 for A input |
| P_OUTBIT_A | %0100_0000_000_0000000000000_00_00000_0 | Select OUT bit for A input |
| P_MINUS3_A | %0101_0000_000_0000000000000_00_00000_0 | Select pin-3 for A input |
| P_MINUS2_A | %0110_0000_000_0000000000000_00_00000_0 | Select pin-2 for A input |
| P_MINUS1_A | %0111_0000_000_0000000000000_00_00000_0 | Select pin-1 for A input |



## B Input Configuration

### B Input Polarity (pick one)

| Constant | Value | Description |
|----------|-------|-------------|
| P_TRUE_B | %0000_0000_000_0000000000000_00_00000_0 | True B input (default) |
| P_INVERT_B | %0000_1000_000_0000000000000_00_00000_0 | Invert B input |

### B Input Selection (pick one)

| Constant | Value | Description |
|----------|-------|-------------|
| P_LOCAL_B | %0000_0000_000_0000000000000_00_00000_0 | Select local pin for B input (default) |
| P_PLUS1_B | %0000_0001_000_0000000000000_00_00000_0 | Select pin+1 for B input |
| P_PLUS2_B | %0000_0010_000_0000000000000_00_00000_0 | Select pin+2 for B input |
| P_PLUS3_B | %0000_0011_000_0000000000000_00_00000_0 | Select pin+3 for B input |
| P_OUTBIT_B | %0000_0100_000_0000000000000_00_00000_0 | Select OUT bit for B input |
| P_MINUS3_B | %0000_0101_000_0000000000000_00_00000_0 | Select pin-3 for B input |
| P_MINUS2_B | %0000_0110_000_0000000000000_00_00000_0 | Select pin-2 for B input |
| P_MINUS1_B | %0000_0111_000_0000000000000_00_00000_0 | Select pin-1 for B input |



## A/B Input Logic (pick one)

| Constant | Value | Description |
|----------|-------|-------------|
| P_PASS_AB | %0000_0000_000_0000000000000_00_00000_0 | Pass A and B through (default) |
| P_AND_AB | %0000_0000_001_0000000000000_00_00000_0 | A AND B → A, pass B |
| P_OR_AB | %0000_0000_010_0000000000000_00_00000_0 | A OR B → A, pass B |
| P_XOR_AB | %0000_0000_011_0000000000000_00_00000_0 | A XOR B → A, pass B |
| P_FILT0_AB | %0000_0000_100_0000000000000_00_00000_0 | Filter A and B (2-clock sample) |
| P_FILT1_AB | %0000_0000_101_0000000000000_00_00000_0 | Filter A and B (3-clock sample) |
| P_FILT2_AB | %0000_0000_110_0000000000000_00_00000_0 | Filter A and B (5-clock sample) |
| P_FILT3_AB | %0000_0000_111_0000000000000_00_00000_0 | Filter A and B (8-clock sample) |



## Low-Level Pin Modes

### Logic/Schmitt/Comparator Input Modes (pick one)

| Constant | Value | Description |
|----------|-------|-------------|
| P_LOGIC_A | %0000_0000_000_0000000000000_00_00000_0 | Logic level A → IN, output OUT (default) |
| P_LOGIC_A_FB | %0000_0000_000_0001000000000_00_00000_0 | Logic level A → IN, output feedback |
| P_LOGIC_B_FB | %0000_0000_000_0010000000000_00_00000_0 | Logic level B → IN, output feedback |
| P_SCHMITT_A | %0000_0000_000_0011000000000_00_00000_0 | Schmitt trigger A → IN, output OUT |
| P_SCHMITT_A_FB | %0000_0000_000_0100000000000_00_00000_0 | Schmitt trigger A → IN, output feedback |
| P_SCHMITT_B_FB | %0000_0000_000_0101000000000_00_00000_0 | Schmitt trigger B → IN, output feedback |
| P_COMPARE_AB | %0000_0000_000_0110000000000_00_00000_0 | A > B → IN, output OUT |
| P_COMPARE_AB_FB | %0000_0000_000_0111000000000_00_00000_0 | A > B → IN, output feedback |

### ADC Input Modes (pick one)

| Constant | Value | Description |
|----------|-------|-------------|
| P_ADC_GIO | %0000_0000_000_1000000000000_00_00000_0 | ADC GIO → IN, output OUT |
| P_ADC_VIO | %0000_0000_000_1000010000000_00_00000_0 | ADC VIO → IN, output OUT |
| P_ADC_FLOAT | %0000_0000_000_1000100000000_00_00000_0 | ADC FLOAT → IN, output OUT |
| P_ADC_1X | %0000_0000_000_1000110000000_00_00000_0 | ADC 1x gain → IN, output OUT |
| P_ADC_3X | %0000_0000_000_1001000000000_00_00000_0 | ADC 3.16x gain → IN, output OUT |
| P_ADC_10X | %0000_0000_000_1001010000000_00_00000_0 | ADC 10x gain → IN, output OUT |
| P_ADC_30X | %0000_0000_000_1001100000000_00_00000_0 | ADC 31.6x gain → IN, output OUT |
| P_ADC_100X | %0000_0000_000_1001110000000_00_00000_0 | ADC 100x gain → IN, output OUT |

### DAC Output Modes (pick one)

| Constant | Value | Description |
|----------|-------|-------------|
| P_DAC_990R_3V | %0000_0000_000_1010000000000_00_00000_0 | DAC 990Ω, 3.3V peak, ADC 1x → IN |
| P_DAC_600R_2V | %0000_0000_000_1010100000000_00_00000_0 | DAC 600Ω, 2.0V peak, ADC 1x → IN |
| P_DAC_124R_3V | %0000_0000_000_1011000000000_00_00000_0 | DAC 123.75Ω, 3.3V peak, ADC 1x → IN |
| P_DAC_75R_2V | %0000_0000_000_1011100000000_00_00000_0 | DAC 75Ω, 2.0V peak, ADC 1x → IN |

### Level-Comparison Modes (pick one)

| Constant | Value | Description |
|----------|-------|-------------|
| P_LEVEL_A | %0000_0000_000_1100000000000_00_00000_0 | A > Level → IN, output OUT |
| P_LEVEL_A_FBN | %0000_0000_000_1101000000000_00_00000_0 | A > Level → IN, output negative feedback |
| P_LEVEL_B_FBP | %0000_0000_000_1110000000000_00_00000_0 | B > Level → IN, output positive feedback |
| P_LEVEL_B_FBN | %0000_0000_000_1111000000000_00_00000_0 | B > Level → IN, output negative feedback |



## Low-Level Pin Sub-Modes

### Sync Mode (pick one)

| Constant | Value | Description |
|----------|-------|-------------|
| P_ASYNC_IO | %0000_0000_000_0000000000000_00_00000_0 | Asynchronous I/O (default) |
| P_SYNC_IO | %0000_0000_000_0000100000000_00_00000_0 | Synchronous I/O |

### IN Polarity (pick one)

| Constant | Value | Description |
|----------|-------|-------------|
| P_TRUE_IN | %0000_0000_000_0000000000000_00_00000_0 | True IN bit (default) |
| P_INVERT_IN | %0000_0000_000_0000010000000_00_00000_0 | Invert IN bit |

### Output Polarity (pick one)

| Constant | Value | Description |
|----------|-------|-------------|
| P_TRUE_OUTPUT | %0000_0000_000_0000000000000_00_00000_0 | True output (default) |
| P_TRUE_OUT | %0000_0000_000_0000000000000_00_00000_0 | Alias for P_TRUE_OUTPUT |
| P_INVERT_OUTPUT | %0000_0000_000_0000001000000_00_00000_0 | Invert output |
| P_INVERT_OUT | %0000_0000_000_0000001000000_00_00000_0 | Alias for P_INVERT_OUTPUT |



## Drive Strength

### Drive-High Strength (pick one)

| Constant | Value | Description |
|----------|-------|-------------|
| P_HIGH_FAST | %0000_0000_000_0000000000000_00_00000_0 | Drive high fast (30mA) - default |
| P_HIGH_1K5 | %0000_0000_000_0000000001000_00_00000_0 | Drive high 1.5kΩ |
| P_HIGH_15K | %0000_0000_000_0000000010000_00_00000_0 | Drive high 15kΩ |
| P_HIGH_150K | %0000_0000_000_0000000011000_00_00000_0 | Drive high 150kΩ |
| P_HIGH_1MA | %0000_0000_000_0000000100000_00_00000_0 | Drive high 1mA current source |
| P_HIGH_100UA | %0000_0000_000_0000000101000_00_00000_0 | Drive high 100μA current source |
| P_HIGH_10UA | %0000_0000_000_0000000110000_00_00000_0 | Drive high 10μA current source |
| P_HIGH_FLOAT | %0000_0000_000_0000000111000_00_00000_0 | Float high (high-impedance) |

### Drive-Low Strength (pick one)

| Constant | Value | Description |
|----------|-------|-------------|
| P_LOW_FAST | %0000_0000_000_0000000000000_00_00000_0 | Drive low fast (30mA) - default |
| P_LOW_1K5 | %0000_0000_000_0000000000001_00_00000_0 | Drive low 1.5kΩ |
| P_LOW_15K | %0000_0000_000_0000000000010_00_00000_0 | Drive low 15kΩ |
| P_LOW_150K | %0000_0000_000_0000000000011_00_00000_0 | Drive low 150kΩ |
| P_LOW_1MA | %0000_0000_000_0000000000100_00_00000_0 | Drive low 1mA current sink |
| P_LOW_100UA | %0000_0000_000_0000000000101_00_00000_0 | Drive low 100μA current sink |
| P_LOW_10UA | %0000_0000_000_0000000000110_00_00000_0 | Drive low 10μA current sink |
| P_LOW_FLOAT | %0000_0000_000_0000000000111_00_00000_0 | Float low (high-impedance) |



## DIR/OUT Control (TT Field)

| Constant | Value | Description |
|----------|-------|-------------|
| P_TT_00 | %0000_0000_000_0000000000000_00_00000_0 | TT = %00 (default) |
| P_TT_01 | %0000_0000_000_0000000000000_01_00000_0 | TT = %01 |
| P_TT_10 | %0000_0000_000_0000000000000_10_00000_0 | TT = %10 |
| P_TT_11 | %0000_0000_000_0000000000000_11_00000_0 | TT = %11 |
| P_OE | %0000_0000_000_0000000000000_01_00000_0 | Output enable in smart pin mode |
| P_CHANNEL | %0000_0000_000_0000000000000_01_00000_0 | Enable DAC channel (non-smart mode) |
| P_BITDAC | %0000_0000_000_0000000000000_10_00000_0 | Enable BITDAC (non-smart mode) |



## Smart Pin Operating Modes (32 Modes)

### Mode %00000 - %00011: Repository and DAC Dither Modes

| Constant | Value | Description |
|----------|-------|-------------|
| P_NORMAL | %0000_0000_000_0000000000000_00_00000_0 | Normal I/O (smart pin disabled) |
| P_REPOSITORY | %0000_0000_000_0000000000000_00_00001_0 | Long repository (non-DAC mode) |
| P_DAC_NOISE | %0000_0000_000_0000000000000_00_00001_0 | DAC noise (DAC mode) |
| P_DAC_DITHER_RND | %0000_0000_000_0000000000000_00_00010_0 | DAC 16-bit random dither |
| P_DAC_DITHER_PWM | %0000_0000_000_0000000000000_00_00011_0 | DAC 16-bit PWM dither |

### Mode %00100 - %00111: Pulse and NCO Modes

| Constant | Value | Description |
|----------|-------|-------------|
| P_PULSE | %0000_0000_000_0000000000000_00_00100_0 | Pulse/cycle output |
| P_TRANSITION | %0000_0000_000_0000000000000_00_00101_0 | Transition output |
| P_NCO_FREQ | %0000_0000_000_0000000000000_00_00110_0 | NCO frequency output |
| P_NCO_DUTY | %0000_0000_000_0000000000000_00_00111_0 | NCO duty cycle output |

### Mode %01000 - %01011: PWM Modes

| Constant | Value | Description |
|----------|-------|-------------|
| P_PWM_TRIANGLE | %0000_0000_000_0000000000000_00_01000_0 | PWM with triangle carrier |
| P_PWM_SAWTOOTH | %0000_0000_000_0000000000000_00_01001_0 | PWM with sawtooth carrier |
| P_PWM_SMPS | %0000_0000_000_0000000000000_00_01010_0 | PWM for switch-mode power supplies |
| P_QUADRATURE | %0000_0000_000_0000000000000_00_01011_0 | A-B quadrature encoder input |

### Mode %01100 - %01111: Counter Modes

| Constant | Value | Description |
|----------|-------|-------------|
| P_REG_UP | %0000_0000_000_0000000000000_00_01100_0 | Inc on A-rise when B-high |
| P_REG_UP_DOWN | %0000_0000_000_0000000000000_00_01101_0 | Inc on A-rise/B-high, dec on A-rise/B-low |
| P_COUNT_RISES | %0000_0000_000_0000000000000_00_01110_0 | Count A-rises, optionally dec on B-rise |
| P_COUNT_HIGHS | %0000_0000_000_0000000000000_00_01111_0 | Count A-highs, optionally dec on B-high |

### Mode %10000 - %10111: Timing Measurement Modes

| Constant | Value | Description |
|----------|-------|-------------|
| P_STATE_TICKS | %0000_0000_000_0000000000000_00_10000_0 | For A-low/high states, count ticks |
| P_HIGH_TICKS | %0000_0000_000_0000000000000_00_10001_0 | For A-high states, count ticks |
| P_EVENTS_TICKS | %0000_0000_000_0000000000000_00_10010_0 | For X A-events, count ticks / timeout |
| P_PERIODS_TICKS | %0000_0000_000_0000000000000_00_10011_0 | For X periods of A, count ticks |
| P_PERIODS_HIGHS | %0000_0000_000_0000000000000_00_10100_0 | For X periods of A, count highs |
| P_COUNTER_TICKS | %0000_0000_000_0000000000000_00_10101_0 | For periods in X+ ticks, count ticks |
| P_COUNTER_HIGHS | %0000_0000_000_0000000000000_00_10110_0 | For periods in X+ ticks, count highs |
| P_COUNTER_PERIODS | %0000_0000_000_0000000000000_00_10111_0 | For periods in X+ ticks, count periods |

### Mode %11000 - %11011: ADC and USB Modes

| Constant | Value | Description |
|----------|-------|-------------|
| P_ADC | %0000_0000_000_0000000000000_00_11000_0 | ADC sample/filter/capture (internal clock) |
| P_ADC_EXT | %0000_0000_000_0000000000000_00_11001_0 | ADC sample/filter/capture (external clock) |
| P_ADC_SCOPE | %0000_0000_000_0000000000000_00_11010_0 | ADC oscilloscope with trigger |
| P_USB_PAIR | %0000_0000_000_0000000000000_00_11011_0 | USB D+/D- pin pair |

### Mode %11100 - %11111: Serial Communication Modes

| Constant | Value | Description |
|----------|-------|-------------|
| P_SYNC_TX | %0000_0000_000_0000000000000_00_11100_0 | Synchronous serial transmit |
| P_SYNC_RX | %0000_0000_000_0000000000000_00_11101_0 | Synchronous serial receive |
| P_ASYNC_TX | %0000_0000_000_0000000000000_00_11110_0 | Asynchronous serial transmit |
| P_ASYNC_RX | %0000_0000_000_0000000000000_00_11111_0 | Asynchronous serial receive |



## Usage Examples

### PWM Output Configuration

```pasm
' Configure pin 56 for triangle PWM output
        mov     mode, ##P_PWM_TRIANGLE | P_OE
        wrpin   mode, #56
        wxpin   ##10000, #56        ' Period = 10000 clocks
        wypin   ##5000, #56         ' Duty = 50%
        dirh    #56                 ' Enable output
```

### ADC Input with Gain

```pasm
' Configure pin 32 for ADC with 10x gain
        mov     mode, ##P_ADC | P_ADC_10X
        wrpin   mode, #32
        wxpin   ##14, #32           ' 14-bit resolution
        dirl    #32                 ' Input mode
```

### Open-Drain Output (I2C-style)

```pasm
' Configure for open-drain with 1.5kΩ pull-up
        mov     mode, ##P_HIGH_FLOAT | P_LOW_1K5
        wrpin   mode, #44
```

### Schmitt Trigger Input with Filter

```pasm
' Debounced button input
        mov     mode, ##P_SCHMITT_A | P_FILT3_AB
        wrpin   mode, #0
```



## Combining Constants

SmartPin constants are designed to be combined using OR operations. The bit fields are carefully arranged so constants from different categories don't conflict:

```pasm
' Complex config: Async TX, inverted, fast drive
        mov     mode, ##P_ASYNC_TX | P_OE | P_INVERT_OUTPUT
        or      mode, ##P_HIGH_FAST | P_LOW_FAST
        wrpin   mode, pin
```



## Related Instructions

- [WRPIN](#wrpin) — Write SmartPin mode register
- [WXPIN](#wxpin) — Write SmartPin X register (period, bit timing, etc.)
- [WYPIN](#wypin) — Write SmartPin Y register (duty, data, etc.)
- [RDPIN](#rdpin) — Read SmartPin result and clear flag
- [RQPIN](#rqpin) — Read SmartPin result without clearing flag
- [AKPIN](#akpin) — Acknowledge SmartPin (clear flag only)


