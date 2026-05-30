# Chapter 2: Enhanced Direct I/O - Low-Level Pin Modes {#ch2}

Enhanced Direct I/O extends basic pin control with configurable drive strength, input conditioning, and basic analog capabilities—all without entering Smart Pin modes. These features are configured via WRPIN using P_ constants with mode bits [4:0] = %00000 (`P_NORMAL`).

## 2.1 Overview

### What Enhanced Direct I/O Provides

While Chapter 1 covered the fundamental DIR/OUT/IN operations, Enhanced Direct I/O adds:

- **Drive Strength Selection**: 8 options for high-side drive, 8 options for low-side drive
- **Input Conditioning**: Logic level, Schmitt trigger, and comparator modes
- **Input Routing**: Select from local pin or adjacent pins (-3 to +3)
- **Basic Analog**: DAC output and ADC input without Smart Pin modes
- **Polarity Control**: Invert input or output signals

### Configuration Method

All Enhanced Direct I/O features are configured via WRPIN:

**Spin2:**
```spin2
WRPIN(pin, P_constant1 | P_constant2 | ...)
```

**PASM2:**
```pasm2
              wrpin     pin, ##(P_constant1 | P_constant2)
```

### The P_ Constant Architecture

P_ constants are 32-bit values where specific bit fields control different aspects of pin behavior:

| Bits | Field | Function |
|------|-------|----------|
| 31:28 | AAAA | A input selection and polarity |
| 27:24 | BBBB | B input selection and polarity |
| 23:21 | FFF | A,B input logic / filter selection |
| 20:12 | MMMMMMMMM | Low-level pin mode and sub-mode |
| 11:10 | TT | DIR/OUT control (P_OE, P_BITDAC) |
| 9:5 | SSSSS | Smart Pin mode (00000 = P_NORMAL) |

When mode bits [9:5] = %00000, the pin operates in P_NORMAL mode with enhanced characteristics from other bit fields.

## 2.2 Drive Strength

The P2 provides configurable drive strength for both high-side (driving to VIO) and low-side (driving to ground) independently. This enables open-drain configurations, current limiting, and power optimization.

### Drive-High Options

Select one drive-high constant. These control the high-side output driver.

| Constant | Bits[17:15] | Drive | Current/Impedance | Use Case |
|----------|-------------|-------|-------------------|----------|
| `P_HIGH_FAST` (default) | %000 | Fast CMOS | ~30mA / ~100Ω | Standard digital, LEDs |
| `P_HIGH_1K5` | %001 | Resistive | ~2mA / 1.5kΩ | Current limiting, protection |
| `P_HIGH_15K` | %010 | Resistive | ~200µA / 15kΩ | Pull-up resistor |
| `P_HIGH_150K` | %011 | Resistive | ~20µA / 150kΩ | Weak pull-up |
| `P_HIGH_1MA` | %100 | Current source | 1mA | Constant current |
| `P_HIGH_100UA` | %101 | Current source | 100µA | Low-power pull-up |
| `P_HIGH_10UA` | %110 | Current source | 10µA | Very low power |
| `P_HIGH_FLOAT` | %111 | Float | High-Z | Open-drain output |

### Drive-Low Options

Select one drive-low constant. These control the low-side output driver.

| Constant | Bits[14:12] | Drive | Current/Impedance | Use Case |
|----------|-------------|-------|-------------------|----------|
| `P_LOW_FAST` (default) | %000 | Fast CMOS | ~30mA / ~100Ω | Standard digital, LEDs |
| `P_LOW_1K5` | %001 | Resistive | ~2mA / 1.5kΩ | Current limiting |
| `P_LOW_15K` | %010 | Resistive | ~200µA / 15kΩ | Pull-down resistor |
| `P_LOW_150K` | %011 | Resistive | ~20µA / 150kΩ | Weak pull-down |
| `P_LOW_1MA` | %100 | Current sink | 1mA | Constant current |
| `P_LOW_100UA` | %101 | Current sink | 100µA | Low-power pull-down |
| `P_LOW_10UA` | %110 | Current sink | 10µA | Very low power |
| `P_LOW_FLOAT` | %111 | Float | High-Z | Totem-pole disable |

### Common Drive Configurations

**Standard Digital (Default):**
```spin2
WRPIN(pin, P_HIGH_FAST | P_LOW_FAST)     ' Maximum drive both directions
```

**Open-Drain (I²C style):**
```spin2
WRPIN(pin, P_HIGH_FLOAT | P_LOW_FAST)  ' OUT=1 floats, OUT=0 drives low
```

**Open-Source:**
```spin2
WRPIN(pin, P_HIGH_FAST | P_LOW_FLOAT)  ' OUT=1 drives high, OUT=0 floats
```

**Pull-Up Resistor:**
```spin2
WRPIN(pin, P_HIGH_15K | P_LOW_FLOAT)     ' 15kΩ pull-up, no low drive
```

**Current-Limited Output:**
```spin2
WRPIN(pin, P_HIGH_1K5 | P_LOW_1K5)       ' ~2mA max in either direction
```

### Resistive vs Current Source

**Resistive modes** (1K5, 15K, 150K):

- Voltage-dependent current
- Current decreases as pin approaches target voltage
- Suitable for bus pull-ups/pull-downs
- Rise/fall time depends on load capacitance

**Current source modes** (1MA, 100UA, 10UA):

- Constant current regardless of voltage
- Useful for driving LEDs without external resistor
- Linear charging of capacitive loads
- More predictable timing

**Example - LED without external resistor:**
```spin2
' 1mA current source - suitable for indicator LED
WRPIN(led_pin, P_HIGH_1MA | P_LOW_FAST)
PINHIGH(led_pin)                          ' LED on at 1mA
```

## 2.3 Input Conditioning

Input conditioning selects how the pin's analog signal is converted to the digital IN bit.

### Logic-Level Modes

Standard digital input with selectable input source.

| Constant | Description |
|----------|-------------|
| `P_LOGIC_A` (default) | Logic level A → IN, output from OUT bit |
| `P_LOGIC_A_FB` | Logic level A → IN, output from feedback |
| `P_LOGIC_B_FB` | Logic level B → IN, output from feedback |

**Note:** "Feedback" routes the actual pin state (after driver) back to the output stage, useful for tri-state bus sensing.

### Schmitt Trigger Modes

Schmitt trigger input provides hysteresis, making the input more resistant to noise on slowly-changing signals.

| Constant | Description |
|----------|-------------|
| `P_SCHMITT_A` | Schmitt trigger A → IN, output from OUT |
| `P_SCHMITT_A_FB` | Schmitt trigger A → IN, output from feedback |
| `P_SCHMITT_B_FB` | Schmitt trigger B → IN, output from feedback |

**When to use Schmitt trigger:**

- Slow edge rates on input signals
- Noisy environments
- Mechanical switch debouncing (combined with software)
- Signals with long wiring

**Example - Schmitt trigger for button:**
```spin2
WRPIN(button_pin, P_SCHMITT_A)           ' Schmitt trigger input
PINFLOAT(button_pin)                      ' Make it an input
```

### Comparator Modes

Pin-to-pin comparison for analog signal detection.

| Constant | Description |
|----------|-------------|
| `P_COMPARE_AB` | A > B → IN, output from OUT |
| `P_COMPARE_AB_FB` | A > B → IN, output from feedback |

**Use case:** Compare two analog voltages without ADC.

**Example - Voltage comparator:**
```spin2
' Compare pin 10 (A input) to pin 11 (B input)
' IN=1 when pin 10 > pin 11
WRPIN(10, P_COMPARE_AB | P_PLUS1_B)       ' A=local (10), B=pin+1 (11)
```

## 2.4 Input Source Selection

The A and B inputs can be sourced from the local pin or adjacent pins.

### A Input Selection

| Constant | Source |
|----------|--------|
| `P_LOCAL_A` (default) | Local pin |
| `P_PLUS1_A` | Pin + 1 |
| `P_PLUS2_A` | Pin + 2 |
| `P_PLUS3_A` | Pin + 3 |
| `P_OUTBIT_A` | OUT bit (internal) |
| `P_MINUS3_A` | Pin - 3 |
| `P_MINUS2_A` | Pin - 2 |
| `P_MINUS1_A` | Pin - 1 |

### B Input Selection

| Constant | Source |
|----------|--------|
| `P_LOCAL_B` (default) | Local pin |
| `P_PLUS1_B` | Pin + 1 |
| `P_PLUS2_B` | Pin + 2 |
| `P_PLUS3_B` | Pin + 3 |
| `P_OUTBIT_B` | OUT bit (internal) |
| `P_MINUS3_B` | Pin - 3 |
| `P_MINUS2_B` | Pin - 2 |
| `P_MINUS1_B` | Pin - 1 |

### Input Polarity

| Constant | Effect |
|----------|--------|
| `P_TRUE_A` (default) | Non-inverted A input |
| `P_INVERT_A` | Inverted A input |
| `P_TRUE_B` (default) | Non-inverted B input |
| `P_INVERT_B` | Inverted B input |

### A,B Input Logic

Combine A and B inputs logically before use.

| Constant | Result |
|----------|--------|
| `P_PASS_AB` (default) | Pass A, B unchanged |
| `P_AND_AB` | A AND B, B |
| `P_OR_AB` | A OR B, B |
| `P_XOR_AB` | A XOR B, B |
| `P_FILT0_AB` | FILT0 filter settings |
| `P_FILT1_AB` | FILT1 filter settings |
| `P_FILT2_AB` | FILT2 filter settings |
| `P_FILT3_AB` | FILT3 filter settings |

## 2.5 ADC Input Modes (Basic)

Basic ADC modes provide analog-to-digital conversion without Smart Pin modes. The result appears in the IN bit based on comparison.

| Constant | Gain | Description |
|----------|------|-------------|
| `P_ADC_GIO` | - | ADC GIO → IN |
| `P_ADC_VIO` | - | ADC VIO → IN |
| `P_ADC_FLOAT` | - | ADC float → IN |
| `P_ADC_1X` | 1× | Standard gain |
| `P_ADC_3X` | 3.16× | Moderate amplification |
| `P_ADC_10X` | 10× | High gain |
| `P_ADC_30X` | 31.6× | Higher gain |
| `P_ADC_100X` | 100× | Maximum gain |

**Note:** These modes provide single-bit output (comparator-style). For multi-bit ADC conversion, use Smart Pin ADC modes (Chapter 17).

**Example - Simple threshold detection:**
```spin2
' Detect when analog input exceeds ~1.65V (mid-scale)
WRPIN(adc_pin, P_ADC_1X)
PINFLOAT(adc_pin)
```

## 2.6 DAC Output Modes (Basic)

Basic DAC modes provide digital-to-analog conversion without Smart Pin modes. The DAC value is encoded in the WRPIN configuration word.

| Constant | Impedance | Peak Voltage | Description |
|----------|-----------|--------------|-------------|
| `P_DAC_990R_3V` | 990Ω | 3.3V | High impedance, full swing |
| `P_DAC_600R_2V` | 600Ω | 2.0V | Medium impedance, reduced swing |
| `P_DAC_124R_3V` | 124Ω | 3.3V | Low impedance, full swing |
| `P_DAC_75R_2V` | 75Ω | 2.0V | Lowest impedance, reduced swing |

**DAC Value Encoding:**

The 8-bit DAC value is encoded in bits [19:12] of the WRPIN configuration:

```spin2
' Set pin to output DAC level
' dac_value: 0-255 (0V to peak voltage)
dac_config := P_DAC_990R_3V | (dac_value << 12)
WRPIN(pin, dac_config)
PINH(pin)                                 ' Enable output
```

**Selecting DAC Mode:**

| Need | Use |
|------|-----|
| Maximum voltage swing | `P_DAC_990R_3V` or `P_DAC_124R_3V` |
| Driving low impedance loads | `P_DAC_124R_3V` or `P_DAC_75R_2V` |
| Lower power | `P_DAC_990R_3V` or `P_DAC_600R_2V` |
| Audio output | `P_DAC_75R_2V` (low impedance for headphones) |

**Example - Static analog voltage:**
```spin2
CON
  DAC_PIN = 40
  DAC_MIDPOINT = 128                      ' Half of 256

PUB main()
  ' Output ~1.65V (half of 3.3V)
  WRPIN(DAC_PIN, P_DAC_990R_3V | (DAC_MIDPOINT << 12))
  PINH(DAC_PIN)                           ' Enable DAC output
```

**Note:** For dynamic DAC output with waveform generation, use Smart Pin DAC modes (Chapter 10).

## 2.7 Level Comparison Modes

Level comparison modes compare the input voltage to a programmable 8-bit threshold level.

| Constant | Description |
|----------|-------------|
| `P_LEVEL_A` | A > Level → IN, output from OUT |
| `P_LEVEL_A_FBN` | A > Level → IN, output negative feedback |
| `P_LEVEL_B_FBP` | B > Level → IN, output positive feedback |
| `P_LEVEL_B_FBN` | B > Level → IN, output negative feedback |

**Level Encoding:**

The 8-bit comparison level is encoded in bits [19:12]:

```spin2
' Compare pin A input to threshold level
' level: 0-255 (0V to VIO)
level_config := P_LEVEL_A | (level << 12)
WRPIN(pin, level_config)
```

**Note:** When DIR=1, output drive is 1.5kΩ.

**Feedback Modes:**

- **FBN (Negative Feedback):** Output opposes input (stabilizing)
- **FBP (Positive Feedback):** Output reinforces input (hysteresis/latching)

## 2.8 Synchronous I/O Mode

| Constant | Effect |
|----------|--------|
| `P_ASYNC_IO` (default) | Asynchronous I/O (inputs sampled continuously) |
| `P_SYNC_IO` | Synchronous I/O (inputs sampled on clock edge) |

Synchronous mode is used for clocked interfaces where input sampling must be synchronized to a clock signal.

## 2.9 Polarity Control

### IN Bit Polarity

| Constant | Effect |
|----------|--------|
| `P_TRUE_IN` (default) | IN bit reflects actual input |
| `P_INVERT_IN` | IN bit is inverted from input |

### Output Polarity

| Constant | Effect |
|----------|--------|
| `P_TRUE_OUTPUT` / `P_TRUE_OUT` (default) | Output matches OUT bit |
| `P_INVERT_OUTPUT` / `P_INVERT_OUT` | Output is inverted from OUT bit |

**Example - Active-low LED:**
```spin2
' LED connected to VCC, turns on when pin is low
WRPIN(led_pin, P_INVERT_OUT)
PINHIGH(led_pin)                          ' Actually drives low, LED on
```

## 2.10 DIR/OUT Control

| Constant | TT Bits | Effect |
|----------|---------|--------|
| `P_TT_00` (default) | %00 | Normal operation |
| `P_TT_01` / `P_OE` | %01 | Output enable (for Smart Pin output) |
| `P_TT_10` / `P_BITDAC` | %10 | BITDAC enable |
| `P_TT_11` | %11 | Combined |
| `P_CHANNEL` | %01 | DAC channel enable (alias for P_OE) |

**P_OE** is required when using Smart Pin modes that produce output. For P_NORMAL mode, it is not needed as DIR controls output directly.

## 2.11 Combining Constants

P_ constants are combined using the OR operator. Constants from different categories can be freely combined; constants from the same category (marked "pick one") are mutually exclusive.

### Combination Rules

1. **Pick one from each category** - Only one drive-high, one drive-low, one input mode, etc.
2. **OR them together** - Use `|` operator in Spin2 or PASM2
3. **Order doesn't matter** - Constants can be combined in any order
4. **Defaults apply if omitted** - P_HIGH_FAST, P_LOW_FAST, P_LOGIC_A, etc. are defaults

### Examples

**Open-drain with Schmitt input:**
```spin2
WRPIN(pin, P_HIGH_FLOAT | P_LOW_FAST | P_SCHMITT_A)
```

**Weak pull-up with inverted input:**
```spin2
WRPIN(pin, P_HIGH_15K | P_LOW_FLOAT | P_INVERT_IN)
```

**Current-limited output with inverted polarity:**
```spin2
WRPIN(pin, P_HIGH_1K5 | P_LOW_1K5 | P_INVERT_OUT)
```

**Comparator using adjacent pin:**
```spin2
WRPIN(pin, P_COMPARE_AB | P_PLUS1_B)
```

## 2.12 Complete Configuration Examples

### I²C Open-Drain Configuration

```spin2
CON
  SDA_PIN = 0
  SCL_PIN = 1

PUB setup_i2c()
  ' Open-drain (most I²C setups use external pull-ups instead)
  WRPIN(SDA_PIN, P_HIGH_FLOAT | P_LOW_FAST | P_SCHMITT_A)
  WRPIN(SCL_PIN, P_HIGH_FLOAT | P_LOW_FAST | P_SCHMITT_A)
  
  ' Start with lines released (high via external pull-ups)
  PINHIGH(SDA_PIN)                        ' Float (open-drain high)
  PINHIGH(SCL_PIN)                        ' Float (open-drain high)
```

### Button Input with Internal Pull-Up

```spin2
CON
  BUTTON_PIN = 10

PUB setup_button()
  ' Internal 15kΩ pull-up, Schmitt trigger for noise immunity
  WRPIN(BUTTON_PIN, P_HIGH_15K | P_LOW_FLOAT | P_SCHMITT_A)
  PINHIGH(BUTTON_PIN)                     ' Enable pull-up
  
  ' Now PINREAD returns 1 when released, 0 when pressed
```

### LED Current Source

```spin2
CON
  LED_PIN = 56

PUB setup_led()
  ' 1mA current source - no external resistor needed
  WRPIN(LED_PIN, P_HIGH_1MA | P_LOW_FAST)
  
  ' PINHIGH turns LED on at 1mA
  ' PINLOW turns LED off
```

### Static DAC Output

```spin2
CON
  DAC_PIN = 40
  
PUB set_voltage(level) | config
  ' Output analog voltage proportional to level (0-255)
  config := P_DAC_990R_3V | (level << 12)
  WRPIN(DAC_PIN, config)
  PINH(DAC_PIN)                           ' Enable output
```

### PASM2 Configuration Examples

```pasm2
' Open-drain configuration
              wrpin sda_pin, ##(P_HIGH_FLOAT | P_LOW_FAST | P_SCHMITT_A)
              drvh      sda_pin              ' Release line (floats high)

' Internal pull-up button
              wrpin btn_pin, ##(P_HIGH_15K | P_LOW_FLOAT | P_SCHMITT_A)
              drvh      btn_pin                ' Enable pull-up

' Current-source LED
              wrpin     led_pin, ##(P_HIGH_1MA | P_LOW_FAST)
              drvh      led_pin                ' LED on at 1mA

' DAC output (1.65V = 128 at 3.3V range)
              wrpin     dac_pin, ##(P_DAC_990R_3V | (128 << 12))
              dirh      dac_pin                ' Enable DAC
```

## 2.13 Resetting to Default

To reset a pin to default configuration:

**Spin2:**
```spin2
PINCLEAR(pin)                             ' Reset to P_NORMAL
' or
WRPIN(pin, 0)                             ' Same effect
```

**PASM2:**
```pasm2
              wrpin     pin, #0           ' Reset to P_NORMAL
```

This clears all enhanced configuration and Smart Pin modes, returning the pin to basic Direct I/O operation.

## 2.14 Quick Reference

### Drive Strength Summary

| High-Side | Low-Side | Configuration |
|-----------|----------|---------------|
| Fast | Fast | Default digital (30mA) |
| Float | Fast | Open-drain |
| Fast | Float | Open-source |
| 15K | Float | Pull-up only |
| Float | 15K | Pull-down only |
| 1K5 | 1K5 | Current-limited |
| 1MA | Fast | LED current source |

### Input Mode Summary

| Mode | Hysteresis | Use Case |
|------|------------|----------|
| P_LOGIC_A | None | Fast digital signals |
| P_SCHMITT_A | Yes | Slow/noisy signals, buttons |
| P_COMPARE_AB | None | Analog comparison |
| P_ADC_* | None | Analog threshold detection |
| P_LEVEL_* | Optional | Programmable threshold |


*This chapter covers pin configuration without Smart Pin modes. For autonomous pin operations (PWM, serial, ADC, etc.), see Chapters 6-19. For the Smart Pin configuration process, see Chapter 4.*
