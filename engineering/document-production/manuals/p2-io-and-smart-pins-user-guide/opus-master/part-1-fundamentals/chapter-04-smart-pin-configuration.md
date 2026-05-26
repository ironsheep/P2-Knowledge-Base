# Chapter 4: Smart Pin Configuration

This chapter documents the instructions and methods for configuring and interacting with Smart Pins. The configuration instructions—WRPIN, WXPIN, WYPIN—establish Smart Pin behavior. The read instructions—RDPIN, RQPIN—retrieve results. The acknowledge instruction—AKPIN—signals the Smart Pin without reading.

---

## 4.1 Configuration Instructions Overview

| Instruction | Purpose | Effect on IN |
|-------------|---------|--------------|
| **WRPIN** | Set mode and pin configuration | Acknowledges (lowers IN) |
| **WXPIN** | Set X register parameters | Acknowledges (lowers IN) |
| **WYPIN** | Set Y register parameters | Acknowledges (lowers IN) |
| **RDPIN** | Read Z register | Acknowledges (lowers IN) |
| **RQPIN** | Read Z register quietly | Does NOT acknowledge |
| **AKPIN** | Acknowledge only | Acknowledges (lowers IN) |

All configuration and acknowledge instructions execute in 2 clock cycles.

---

## 4.2 WRPIN - Write Pin Configuration

### Function

WRPIN establishes the complete pin configuration including:
- Smart Pin mode selection
- Low-level pin configuration (drive strength, input mode)
- Input routing and polarity
- DIR/OUT control options

### PASM2 Syntax

```
WRPIN   {#}D, {#}S
```

- **D**: 32-bit configuration value
- **S**: Pin number (0-63) or pin field with span

### Spin2 Syntax

```spin2
WRPIN(PinField, Mode)
```

- **PinField**: Single pin, range, or ADDPINS expression
- **Mode**: 32-bit configuration value (P_ constants OR'd together)

### Configuration Value Format

The D operand is a 32-bit value with the following fields:

```
D = %AAAA_BBBB_FFF_MMMMMMMMMMMMM_TT_SSSSS_0

Bits 31:28  AAAA  - A input selection and polarity
Bits 27:24  BBBB  - B input selection and polarity
Bits 23:21  FFF   - A,B input logic/filtering
Bits 20:8   MMMMMMMMMMMMM - Low-level pin mode (13 bits)
Bits 7:6    TT    - DIR/OUT control
Bits 5:1    SSSSS - Smart Pin mode (0-31)
Bit 0       0     - Reserved (always 0)
```

### Timing

- Execution: 2 clock cycles
- After WRPIN, 2 additional clocks must elapse before IN can be polled

### Effect

1. Pin is configured according to the D value
2. IN bit is acknowledged (lowered)
3. If DIR=0, Smart Pin remains in reset state
4. If DIR=1 and mode changes, behavior is unpredictable (always configure while DIR=0)

### Critical Requirements

**Configure while DIR=0:** Smart Pins must be configured while held in reset (DIR=0). The proper sequence is:
1. DIRL to reset Smart Pin
2. WRPIN to configure
3. WXPIN/WYPIN as needed
4. DRVL/DRVH to enable

**Reset to normal mode:** To return a pin to Direct I/O mode:
```pasm2
              wrpin     #0, pin         ' Reset to P_NORMAL
```

### Examples

**Spin2 - Configure NCO frequency mode:**
```spin2
WRPIN(pin, P_NCO_FREQ | P_OE)           ' NCO mode with output enable
```

**PASM2 - Configure NCO frequency mode:**
```pasm2
              wrpin     pin, ##(P_NCO_FREQ | P_OE)
```

**Spin2 - Configure with drive strength:**
```spin2
WRPIN(pin, P_PWM_TRIANGLE | P_OE | P_HIGH_FAST | P_LOW_FAST)
```

---

## 4.3 WXPIN - Write X Register

### Function

WXPIN writes the X register, which holds configuration parameters. The meaning of X varies by mode.

### PASM2 Syntax

```
WXPIN   {#}D, {#}S
```

- **D**: Value to write to X register
- **S**: Pin number (0-63) or pin field with span

### Spin2 Syntax

```spin2
WXPIN(PinField, Xvalue)
```

### Common X Register Uses

| Mode Category | X[15:0] | X[31:16] |
|---------------|---------|----------|
| Timing output modes | Base period (clocks) | Frame period or phase |
| Counter modes | Measurement window | - |
| Serial TX | Bit period | Data format |
| Serial RX | Bit period | Data format |
| ADC modes | Sample period/mode | - |

### Timing

- Execution: 2 clock cycles
- Acknowledges IN (2-clock delay before polling)

### Special Behavior

Some modes capture X[31:16] to Z[31:16] upon WXPIN, allowing phase initialization (NCO modes, for example).

### Examples

**Spin2 - Set base period:**
```spin2
WXPIN(pin, base_period)                  ' X = base_period
```

**PASM2 - Set base period with frame count:**
```pasm2
              wxpin     pin, x_value      ' X[15:0] = base, X[31:16] = frame
```

---

## 4.4 WYPIN - Write Y Register

### Function

WYPIN writes the Y register, which holds input data or secondary parameters.

### PASM2 Syntax

```
WYPIN   {#}D, {#}S
```

- **D**: Value to write to Y register
- **S**: Pin number (0-63) or pin field with span

### Spin2 Syntax

```spin2
WYPIN(PinField, Yvalue)
```

### Common Y Register Uses

| Mode Category | Y Usage |
|---------------|---------|
| PWM modes | Duty cycle value |
| NCO modes | Frequency/phase increment |
| DAC modes | Output level |
| Serial TX | Data to transmit |
| Transition output | Number of transitions |
| Counter modes | Mode modifier (Y[0]) |

### Timing

- Execution: 2 clock cycles
- Acknowledges IN (2-clock delay before polling)

### Capture Behavior

Many modes capture Y on specific events (frame start, period end). Writing Y immediately before the capture point ensures the new value is used.

### Examples

**Spin2 - Set PWM duty:**
```spin2
WYPIN(pin, duty_value)                   ' Y = duty cycle
```

**PASM2 - Send serial data:**
```pasm2
              wypin     tx_pin, data      ' Y = data to transmit
```

---

## 4.5 RDPIN - Read Z Register with Acknowledge

### Function

RDPIN reads the Z register and acknowledges the Smart Pin (lowers IN).

### PASM2 Syntax

```
RDPIN   D, {#}S
```

- **D**: Destination register for Z value
- **S**: Pin number (0-63)

### Spin2 Syntax

```spin2
result := RDPIN(Pin)
```

### Effect

1. Z register value is read to D
2. C flag receives mode-specific flag (often Z[31] or event indicator)
3. IN bit is acknowledged (lowered)

### Timing

- Execution: 2 clock cycles
- After RDPIN, 2 additional clocks before IN can be polled again

### Z Register Content by Mode

| Mode Category | Z Contains |
|---------------|------------|
| Measurement modes | Accumulated count or time |
| Counter modes | Event count |
| ADC modes | Conversion result |
| Serial RX | Received data |
| NCO modes | Phase accumulator |

### When to Use RDPIN

Use RDPIN when:
- The COG needs the result AND
- The Smart Pin should be signaled that the result was consumed

This is the normal read operation for single-COG access.

### Examples

**Spin2 - Read measurement:**
```spin2
measurement := RDPIN(pin)                ' Read Z, acknowledge
```

**PASM2 - Read and check flag:**
```pasm2
              rdpin     result, #pin wc  ' Read Z, C = flag
        if_c  jmp       #handle_event    ' Act on flag
```

---

## 4.6 RQPIN - Read Z Register Quietly

### Function

RQPIN reads the Z register WITHOUT acknowledging the Smart Pin. IN remains in its current state.

### PASM2 Syntax

```
RQPIN   D, {#}S
```

### Spin2 Syntax

```spin2
result := RQPIN(Pin)
```

### Effect

1. Z register value is read to D
2. C flag receives mode-specific flag
3. IN bit is NOT affected (no acknowledge)

### When to Use RQPIN

**Multi-COG observation:** When multiple COGs need to read the same Smart Pin's result, only one should use RDPIN; others use RQPIN to avoid acknowledging multiple times.

**Non-destructive peek:** When checking results without signaling consumption.

**Continuous modes:** Some modes (like totalizer counters) benefit from RQPIN for intermediate reads while RDPIN resets for the next period.

### Example - Multi-COG Access

```pasm2
' COG 0 (primary) uses RDPIN
              rdpin     result, #sensor  ' Read and acknowledge

' COG 1 (observer) uses RQPIN
              rqpin     result, #sensor  ' Read without acknowledge
```

---

## 4.7 AKPIN - Acknowledge Only

### Function

AKPIN acknowledges the Smart Pin without reading the Z register.

### PASM2 Syntax

```
AKPIN   {#}S
```

- **S**: Pin number (0-63) or pin field

### Spin2 Equivalent

There is no direct Spin2 equivalent. Use RDPIN with a discard variable:
```spin2
ack := RDPIN(pin)                        ' Read (discard result) to acknowledge
```

Or configure in PASM2 if needed.

### When to Use AKPIN

- Resetting the IN flag without needing the data
- Synchronizing Smart Pin timing without data consumption
- Discarding an unwanted result

### Example

```pasm2
              akpin     #pin              ' Acknowledge without reading
```

---

## 4.8 The Standard Configuration Sequence

All Smart Pin modes follow a common configuration pattern:

### Step 1: Reset the Smart Pin

```spin2
PINFLOAT(pin)                            ' DIR=0, hold in reset
' or
PINL(pin)                                ' Same effect
```

```pasm2
              dirl      #pin              ' Reset Smart Pin
```

### Step 2: Configure Mode (WRPIN)

```spin2
WRPIN(pin, P_MODE | P_OE | ...)          ' Set mode and options
```

```pasm2
              wrpin     #pin, ##(P_MODE | P_OE)
```

### Step 3: Set Parameters (WXPIN)

```spin2
WXPIN(pin, x_value)                      ' Set X register
```

```pasm2
              wxpin     #pin, x_value
```

### Step 4: Set Data/Secondary Parameters (WYPIN) - If Needed

```spin2
WYPIN(pin, y_value)                      ' Set Y register
```

```pasm2
              wypin     #pin, y_value
```

### Step 5: Enable Smart Pin

```spin2
PINLOW(pin)                              ' DIR=1, start Smart Pin
' or
PINHIGH(pin)                             ' DIR=1, start Smart Pin
```

```pasm2
              drvl      #pin              ' Enable Smart Pin
' or
              drvh      #pin              ' Enable Smart Pin
```

**Note:** For output modes, DRVL vs DRVH doesn't affect the Smart Pin output (which is controlled by the mode). Use whichever is appropriate for the pre-enabled output state.

### Complete Example - NCO Frequency

**Spin2:**
```spin2
CON
  _clkfreq = 200_000_000
  OUT_PIN = 10
  TARGET_FREQ = 1000                      ' 1 kHz output

PUB setup_nco() | y_value
  ' Calculate Y for target frequency
  ' frequency = (Y × sysclk) / 2^32
  ' Y = (frequency × 2^32) / sysclk
  y_value := TARGET_FREQ FRAC _clkfreq
  
  ' Configuration sequence
  PINFLOAT(OUT_PIN)                       ' Step 1: Reset
  WRPIN(OUT_PIN, P_NCO_FREQ | P_OE)       ' Step 2: Mode
  WXPIN(OUT_PIN, 1)                       ' Step 3: Base period = 1 clock
  WYPIN(OUT_PIN, y_value)                 ' Step 4: Frequency value
  PINLOW(OUT_PIN)                         ' Step 5: Enable
```

**PASM2:**
```pasm2
              dirl      #OUT_PIN          ' Step 1: Reset
              wrpin     #OUT_PIN, ##(P_NCO_FREQ | P_OE)   ' Step 2: Mode
              wxpin     #OUT_PIN, #1      ' Step 3: Base period = 1
              wypin     #OUT_PIN, y_val   ' Step 4: Frequency
              drvl      #OUT_PIN          ' Step 5: Enable
```

---

## 4.9 P_OE - Output Enable

### Purpose

The `P_OE` constant (TT bits = %01) enables Smart Pin output regardless of the DIR bit state.

### When P_OE is Required

**Output modes:** All Smart Pin modes that produce output require P_OE:
- NCO frequency/duty (%00110, %00111)
- PWM modes (%01000, %01001, %01010)
- Pulse/Transition (%00100, %00101)
- Serial TX (%11100, %11110)
- DAC modes (%00001, %00010, %00011 in DAC mode)
- USB (%11011)

**Without P_OE:** The Smart Pin calculates output but doesn't drive the pin. This can be useful for:
- Preparing output before enabling
- Running the mode for internal timing without external output

### When P_OE is Not Needed

**Input-only modes:** Modes that only measure input don't need P_OE:
- All timing measurement modes (%10000-%10010)
- Counter modes (%01011-%01111) unless driving output
- Period/frequency modes (%10011-%10111)
- ADC modes (%11000-%11010)
- Serial RX (%11101, %11111)

### Including P_OE

```spin2
WRPIN(pin, P_NCO_FREQ | P_OE)             ' Output enabled
WRPIN(pin, P_NCO_FREQ)                    ' Output NOT enabled (internal only)
```

---

## 4.10 Input Routing

Smart Pins can receive input from the local pin or adjacent pins.

### A Input Selection

The A input is the primary input for most modes.

| Constant | Source |
|----------|--------|
| `P_LOCAL_A` (default) | This pin's input |
| `P_PLUS1_A` | Pin + 1 |
| `P_PLUS2_A` | Pin + 2 |
| `P_PLUS3_A` | Pin + 3 |
| `P_OUTBIT_A` | This pin's OUT bit (internal) |
| `P_MINUS3_A` | Pin - 3 |
| `P_MINUS2_A` | Pin - 2 |
| `P_MINUS1_A` | Pin - 1 |

### A Input Polarity

| Constant | Effect |
|----------|--------|
| `P_TRUE_A` (default) | Non-inverted |
| `P_INVERT_A` | Inverted |

### B Input Selection

The B input is used for secondary signals (clock, quadrature channel B, etc.).

| Constant | Source |
|----------|--------|
| `P_LOCAL_B` (default) | This pin's input |
| `P_PLUS1_B` | Pin + 1 |
| `P_PLUS2_B` | Pin + 2 |
| `P_PLUS3_B` | Pin + 3 |
| `P_OUTBIT_B` | This pin's OUT bit (internal) |
| `P_MINUS3_B` | Pin - 3 |
| `P_MINUS2_B` | Pin - 2 |
| `P_MINUS1_B` | Pin - 1 |

### B Input Polarity

| Constant | Effect |
|----------|--------|
| `P_TRUE_B` (default) | Non-inverted |
| `P_INVERT_B` | Inverted |

### Input Logic Combinations

| Constant | Result |
|----------|--------|
| `P_PASS_AB` (default) | A, B passed through |
| `P_AND_AB` | A AND B, B |
| `P_OR_AB` | A OR B, B |
| `P_XOR_AB` | A XOR B, B |
| `P_FILT0_AB` | Filter 0 applied |
| `P_FILT1_AB` | Filter 1 applied |
| `P_FILT2_AB` | Filter 2 applied |
| `P_FILT3_AB` | Filter 3 applied |

### Example - Quadrature Encoder

Quadrature encoder uses two input channels (A and B):

```spin2
' Pin 10 = A input (local)
' Pin 11 = B input (pin + 1)
WRPIN(10, P_QUADRATURE | P_PLUS1_B)       ' A = pin 10, B = pin 11
WXPIN(10, 0)                              ' Continuous measurement
PINLOW(10)                                ' Enable
```

### Example - External Clock

Synchronous serial RX with external clock on adjacent pin:

```spin2
' Pin 20 = data (A input, local)
' Pin 21 = clock (B input, pin + 1)
WRPIN(20, P_SYNC_RX | P_PLUS1_B)          ' A = data, B = clock
WXPIN(20, bit_config)                     ' Configure bit format
PINLOW(20)                                ' Enable
```

---

## 4.11 Span Operations

All Smart Pin instructions support operating on multiple pins simultaneously.

### Span Encoding

The S operand (pin number) can include a span:
- S[5:0]: Base pin (0-63)
- S[10:6]: Additional pins (0-31)

### Using SETQ for Span

```pasm2
              setq      #7                ' 8 pins total (base + 7)
              wrpin     #0, mode_value    ' Configure pins 0-7
```

### Span Wrap Behavior

Spans wrap within the same 32-pin port. Pins 0-31 and 32-63 are separate ports.

### Spin2 Pin Ranges

```spin2
WRPIN(0..7, P_NCO_FREQ | P_OE)            ' Configure pins 0-7
WXPIN(0..7, period)                       ' Set X for pins 0-7
```

---

## 4.12 Reading the C Flag

RDPIN and RQPIN set the C flag based on mode-specific information:

| Mode Category | C Flag Meaning |
|---------------|----------------|
| NCO modes | Z[31] (phase MSB) |
| Measurement modes | State indicator |
| Counter modes | Overflow indicator |
| Serial RX | Parity or error |

### Checking C After Read

```pasm2
              rdpin     result, #pin wc   ' Read Z, C = flag
        if_c  jmp       #handle_flag
```

```spin2
result := RDPIN(pin)
if result & $8000_0000                    ' Check bit 31 (mode-dependent)
  ' Handle condition
```

---

## 4.13 The 2-Clock Acknowledge Delay

After any instruction that acknowledges the Smart Pin (WRPIN, WXPIN, WYPIN, RDPIN, AKPIN), two clock cycles must elapse before IN can be polled:

```pasm2
              rdpin     result, #pin      ' Acknowledge Smart Pin
              nop                         ' Clock 1
              nop                         ' Clock 2
              testp     #pin wc           ' Now safe to poll IN
```

In practice, other instructions between the acknowledge and the poll often provide sufficient delay.

---

## 4.14 Configuration Quick Reference

### Minimum Configuration (Mode Only)

```spin2
PINFLOAT(pin)
WRPIN(pin, P_MODE | P_OE)
PINLOW(pin)
```

### Standard Configuration (Mode + X)

```spin2
PINFLOAT(pin)
WRPIN(pin, P_MODE | P_OE)
WXPIN(pin, x_value)
PINLOW(pin)
```

### Full Configuration (Mode + X + Y)

```spin2
PINFLOAT(pin)
WRPIN(pin, P_MODE | P_OE)
WXPIN(pin, x_value)
WYPIN(pin, y_value)
PINLOW(pin)
```

### Reconfiguration (Change Mode)

```spin2
PINFLOAT(pin)                             ' Reset first
WRPIN(pin, NEW_MODE | P_OE)               ' New mode
WXPIN(pin, new_x)                         ' New parameters
WYPIN(pin, new_y)
PINLOW(pin)                               ' Re-enable
```

### Reset Without Reconfiguration

```spin2
PINFLOAT(pin)                             ' Reset
PINLOW(pin)                               ' Re-enable (same config)
```

### Return to Direct I/O

```spin2
PINCLEAR(pin)                             ' Reset to P_NORMAL
' or
PINFLOAT(pin)
WRPIN(pin, 0)
```

---

*This chapter covers the mechanics of Smart Pin configuration. For specific mode behaviors, see the mode chapters in Parts II-IV. For common usage patterns and debugging, see Chapter 5.*
