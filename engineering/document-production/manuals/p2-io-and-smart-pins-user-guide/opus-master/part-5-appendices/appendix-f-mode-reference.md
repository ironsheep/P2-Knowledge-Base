# Appendix F: Complete Mode Reference

Quick reference for all 32 smart pin modes, organized by mode number.


## Mode Number Cross-Reference

| Mode | Constant | Description |
|------|----------|-------------|
| %00000 | P_NORMAL | Normal I/O (not smart pin) |
| %00001 | P_REPOSITORY / P_DAC_NOISE | Repository or DAC noise |
| %00010 | P_DAC_DITHER_RND | 16-bit PRNG dithered DAC |
| %00011 | P_DAC_DITHER_PWM | 16-bit PWM dithered DAC |
| %00100 | P_PULSE | Pulse/cycle output |
| %00101 | P_TRANSITION | Transition output |
| %00110 | P_NCO_FREQ | NCO frequency (50% duty) |
| %00111 | P_NCO_DUTY | NCO with variable duty |
| %01000 | P_PWM_TRIANGLE | Triangle-wave PWM |
| %01001 | P_PWM_SAWTOOTH | Sawtooth-wave PWM |
| %01010 | P_PWM_SMPS | SMPS PWM with feedback |
| %01011 | P_QUADRATURE | Quadrature encoder |
| %01100 | P_REG_UP | Gated increment counter |
| %01101 | P_REG_UP_DOWN | Up/down gated counter |
| %01110 | P_COUNT_RISES | Count A-input rises |
| %01111 | P_COUNT_HIGHS | Count A-input high states |
| %10000 | P_STATE_TICKS | Time high and low states |
| %10001 | P_HIGH_TICKS | Time high states only |
| %10010 | P_EVENTS_TICKS | Time N events or timeout |
| %10011 | P_PERIODS_TICKS | Time X periods |
| %10100 | P_PERIODS_HIGHS | High time for X periods |
| %10101 | P_COUNTER_TICKS | Period time in X clocks |
| %10110 | P_COUNTER_HIGHS | High time in X clocks |
| %10111 | P_COUNTER_PERIODS | Count periods in X clocks |
| %11000 | P_ADC | ADC internal clock |
| %11001 | P_ADC_EXT | ADC external clock |
| %11010 | P_ADC_SCOPE | ADC triggered scope |
| %11011 | P_USB_PAIR | USB differential pair |
| %11100 | P_SYNC_TX | Synchronous serial TX |
| %11101 | P_SYNC_RX | Synchronous serial RX |
| %11110 | P_ASYNC_TX | Asynchronous serial TX |
| %11111 | P_ASYNC_RX | Asynchronous serial RX |


::: modecard
## Mode %00000: P_NORMAL

**Normal I/O (not a smart pin mode)**

Default mode. Pin operates as standard digital I/O without smart pin functionality.
:::

### Register Usage

| Register | Function |
|----------|----------|
| DIR | Output enable |
| OUT | Output value |
| IN | Input value |

### Key Constants
None required for normal I/O.

### Quick Example
```spin2
PINHIGH(pin)                             ' Set output high
PINLOW(pin)                              ' Set output low
state := PINREAD(pin)                    ' Read input
```

### Reference
[Chapter 6: Digital Output](#ch6), [Chapter 12: Digital Input](#ch12)


::: modecard
## Mode %00001: P_REPOSITORY / P_DAC_NOISE

**Inter-cog data sharing or DAC noise generator**

Dual-purpose mode. Without DAC enable: 32-bit repository for data sharing between cogs. With DAC enable: pseudo-random noise output.
:::

### Register Usage

| Register | Repository | DAC Noise |
|----------|-----------|-----------|
| X[15:0] | Not used | Sample period |
| Y via WXPIN | Value to store | Not used |
| Z via RDPIN | Stored value | Not used |
| IN | New data written | Period complete |

### Key Constants
```spin2
P_REPOSITORY                             ' Mode constant
P_DAC_990R_3V | P_OE                     ' For DAC noise output
```

### Quick Example
```spin2
' Repository mode
WRPIN(pin, P_REPOSITORY)
PINH(pin)
WXPIN(pin, value)                        ' Write value
data := RQPIN(pin)                       ' Read value

' DAC noise mode
WRPIN(pin, P_DAC_NOISE | P_DAC_124R_3V | P_OE)
PINH(pin)
```

### Reference
[Chapter 18: Repository and Inter-Cog Data Sharing](#ch18), [Chapter 10: DAC Output](#ch10)


::: modecard
## Mode %00010: P_DAC_DITHER_RND

**16-bit PRNG dithered DAC**

Provides nominal 16-bit DAC resolution (averaged over time) using pseudo-random dithering between adjacent 8-bit levels. The hardware DAC is 8-bit; real precision depends on output filtering — see §18.4.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X[15:0] | Sample period (1 = immediate) |
| Y[15:0] | 16-bit DAC value |
| Z | ADC accumulation (if OUT=1) |
| IN | Sample period complete |

### Key Constants
```spin2
P_DAC_DITHER_RND | P_DAC_124R_3V | P_OE
```

### Quick Example
```spin2
WRPIN(pin, P_DAC_DITHER_RND | P_DAC_124R_3V | P_OE)
WXPIN(pin, 1)                            ' Immediate updates
WYPIN(pin, $8000)                        ' Mid-scale output
PINH(pin)
```

### Reference
[Chapter 10: DAC Output](#ch10)


::: modecard
## Mode %00011: P_DAC_DITHER_PWM

**16-bit PWM dithered DAC**

Provides 16-bit DAC resolution using PWM dithering. Better dynamic range than PRNG dithering.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X[15:0] | Sample period (must be multiple of 256) |
| Y[15:0] | 16-bit DAC value |
| Z | ADC accumulation (if OUT=1) |
| IN | Sample period complete |

### Key Constants
```spin2
P_DAC_DITHER_PWM | P_DAC_600R_2V | P_OE
```

### Quick Example
```spin2
WRPIN(pin, P_DAC_DITHER_PWM | P_DAC_600R_2V | P_OE)
WXPIN(pin, 256)                          ' Period must be 256×N
WYPIN(pin, $8000)
PINH(pin)
```

### Reference
[Chapter 10: DAC Output](#ch10)


::: modecard
## Mode %00100: P_PULSE

**Pulse/cycle output**

Generates precise timed pulses. Output a specified number of transitions with configurable timing.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X[15:0] | Base period (clocks per unit) |
| X[31:16] | Initial OUT state duration |
| Y[15:0] | Pulse count |
| Y[31:16] | Pulse duration |
| IN | Pulses complete |

### Key Constants
```spin2
P_PULSE | P_OE
```

### Quick Example
```spin2
WRPIN(pin, P_PULSE | P_OE)
WXPIN(pin, 1 | (100 << 16))              ' Base=1, pre-delay=100
WYPIN(pin, 5 | (50 << 16))               ' 5 pulses, 50 clocks each
PINH(pin)
```

### Reference
[Chapter 7: Transition and Pulse Output](#ch7)


::: modecard
## Mode %00101: P_TRANSITION

**Transition output**

Generates a specified number of output transitions with precise timing. Creates square waves or counted pulses.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X[15:0] | Period (clocks per transition) |
| X[31:16] | Initial output state time |
| Y[15:0] | Transition count (0 = continuous) |
| IN | Transitions complete |

### Key Constants
```spin2
P_TRANSITION | P_OE
```

### Quick Example
```spin2
WRPIN(pin, P_TRANSITION | P_OE)
WXPIN(pin, 100)                          ' 100 clocks per transition
WYPIN(pin, 20)                           ' 20 transitions (10 cycles)
PINH(pin)
```

### Reference
[Chapter 7: Transition and Pulse Output](#ch7)


::: modecard
## Mode %00110: P_NCO_FREQ

**NCO frequency generator (50% duty)**

Numerically Controlled Oscillator for precise frequency synthesis. Output is Z[31], creating 50% duty cycle square wave.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X[15:0] | Base period (1 for maximum resolution) |
| X[31:16] | Initial phase |
| Y[31:0] | Frequency control word |
| Z[31:0] | Phase accumulator |
| IN | Z overflow |

### Key Constants
```spin2
P_NCO_FREQ | P_OE
```

### Quick Example
```spin2
' 1 kHz at 200 MHz sysclk
y_val := 1000 FRAC 200_000_000
WRPIN(pin, P_NCO_FREQ | P_OE)
WXPIN(pin, 1)
WYPIN(pin, y_val)
PINLOW(pin)
```

### Reference
[Chapter 8: Frequency Generation (NCO)](#ch8)


::: modecard
## Mode %00111: P_NCO_DUTY

**NCO with variable duty cycle**

NCO frequency generator with duty cycle control. Output reflects Z overflow state.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X[15:0] | Base period (1 for maximum resolution) |
| X[31:16] | Initial phase |
| Y[31:0] | Frequency × duty control |
| Z[31:0] | Phase accumulator |
| IN | Z overflow |

### Key Constants
```spin2
P_NCO_DUTY | P_OE
```

### Quick Example
```spin2
WRPIN(pin, P_NCO_DUTY | P_OE)
WXPIN(pin, 1)
WYPIN(pin, $8000_0000)                   ' 50% duty
PINLOW(pin)
```

### Reference
[Chapter 8: Frequency Generation (NCO)](#ch8)


::: modecard
## Mode %01000: P_PWM_TRIANGLE

**Triangle-wave PWM**

PWM with up-down counter for symmetric output. Creates smooth PWM transitions.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X[15:0] | Base period (clocks per count) |
| X[31:16] | Frame period (counter range) |
| Y[15:0] | Duty value (0 to frame) |
| IN | Frame complete |

### Key Constants
```spin2
P_PWM_TRIANGLE | P_OE
```

### Quick Example
```spin2
' 1 kHz PWM at 50% duty, 200 MHz sysclk
WRPIN(pin, P_PWM_TRIANGLE | P_OE)
WXPIN(pin, 1 | (100_000 << 16))          ' Frame=100000
WYPIN(pin, 50_000)                       ' 50% duty
PINLOW(pin)
```

### Reference
[Chapter 9: PWM Output](#ch9)


::: modecard
## Mode %01001: P_PWM_SAWTOOTH

**Sawtooth-wave PWM**

PWM with up-only counter. Twice the frequency of triangle mode for same X values.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X[15:0] | Base period (clocks per count) |
| X[31:16] | Frame period (counter range) |
| Y[15:0] | Duty value (0 to frame) |
| IN | Frame complete |

### Key Constants
```spin2
P_PWM_SAWTOOTH | P_OE
```

### Quick Example
```spin2
' 20 kHz motor PWM, 200 MHz sysclk
WRPIN(pin, P_PWM_SAWTOOTH | P_OE)
WXPIN(pin, 1 | (10_000 << 16))           ' Frame=10000
WYPIN(pin, 2500)                         ' 25% duty
PINLOW(pin)
```

### Reference
[Chapter 9: PWM Output](#ch9)


::: modecard
## Mode %01010: P_PWM_SMPS

**SMPS PWM with feedback**

Switch-mode power supply controller with voltage and current feedback inputs.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X[15:0] | Base period |
| X[31:16] | Frame period (max pulse) |
| Y[15:0] | Duty value |
| A-input | Voltage feedback (low = new cycle) |
| B-input | Current limit (high = cut off) |
| IN | Cycle start |

### Key Constants
```spin2
P_PWM_SMPS | P_OE | P_PLUS1_A | P_MINUS1_B
```

### Quick Example
```spin2
mode := P_PWM_SMPS | P_OE | P_PLUS1_A | P_MINUS1_B
WRPIN(pin, mode)
WXPIN(pin, 25 | (256 << 16))
WYPIN(pin, 128)                          ' Set once, runs autonomous
PINLOW(pin)
```

### Reference
[Chapter 9: PWM Output](#ch9)


::: modecard
## Mode %01011: P_QUADRATURE

**Quadrature encoder decoder**

Decodes A/B quadrature signals for position tracking with 4× resolution.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X | Period (0=continuous, >0=periodic) |
| Y | Not used |
| Z | Signed position/velocity count |
| A-input | Encoder phase A |
| B-input | Encoder phase B |
| IN | Period complete (if X>0) |

### Key Constants
```spin2
P_QUADRATURE | P_PLUS1_B | P_SCHMITT_A
```

### Quick Example
```spin2
' Encoder A on pin 20, B on pin 21
WRPIN(20, P_QUADRATURE | P_PLUS1_B | P_SCHMITT_A)
WXPIN(20, 0)                             ' Continuous mode
PINLOW(20)
position := RDPIN(20)                    ' Read position
```

### Reference
[Chapter 14: Counting Modes](#ch14)


::: modecard
## Mode %01100: P_REG_UP

**Gated increment counter**

Counts A-input rising edges, but only when B-input is high.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X | Period (0=continuous, >0=periodic) |
| Y | Not used |
| Z | Edge count |
| A-input | Count signal |
| B-input | Gate enable |
| IN | Period complete |

### Key Constants
```spin2
P_REG_UP | P_PLUS1_B
```

### Quick Example
```spin2
WRPIN(pin, P_REG_UP | P_PLUS1_B)
WXPIN(pin, 0)                            ' Continuous
PINH(pin)
count := RDPIN(pin)
```

### Reference
[Chapter 14: Counting Modes](#ch14)


::: modecard
## Mode %01101: P_REG_UP_DOWN

**Up/down gated counter**

Counts A-input edges. B-input controls direction: high=increment, low=decrement.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X | Period (0=continuous, >0=periodic) |
| Y | Not used |
| Z | Signed count |
| A-input | Count signal |
| B-input | Direction (high=up) |
| IN | Period complete |

### Key Constants
```spin2
P_REG_UP_DOWN | P_PLUS1_B
```

### Quick Example
```spin2
WRPIN(pin, P_REG_UP_DOWN | P_PLUS1_B)
WXPIN(pin, 0)
PINH(pin)
count := RDPIN(pin)                      ' Signed result
```

### Reference
[Chapter 14: Counting Modes](#ch14)


::: modecard
## Mode %01110: P_COUNT_RISES

**Count A-input rising edges**

Simple edge counter. Y[0] controls mode: 0=A edges only, 1=A up/B down.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X | Period (0=continuous, >0=periodic) |
| Y[0] | Mode: 0=A only, 1=A up/B down |
| Z | Edge count |
| IN | Period complete |

### Key Constants
```spin2
P_COUNT_RISES | P_SCHMITT_A
```

### Quick Example
```spin2
WRPIN(pin, P_COUNT_RISES | P_SCHMITT_A)
WXPIN(pin, 0)                            ' Continuous
WYPIN(pin, 0)                            ' A edges only
PINH(pin)
count := RDPIN(pin)
```

### Reference
[Chapter 14: Counting Modes](#ch14)


::: modecard
## Mode %01111: P_COUNT_HIGHS

**Count A-input high clocks**

Counts system clocks while A-input is high. Y[0] controls mode.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X | Period (0=continuous, >0=periodic) |
| Y[0] | Mode: 0=A high, 1=A high minus B high |
| Z | Clock count |
| IN | Period complete |

### Key Constants
```spin2
P_COUNT_HIGHS
```

### Quick Example
```spin2
WRPIN(pin, P_COUNT_HIGHS)
WXPIN(pin, _clkfreq)                     ' 1 second period
WYPIN(pin, 0)
PINH(pin)
REPEAT UNTIL PINREAD(pin)
high_clocks := RDPIN(pin)
```

### Reference
[Chapter 14: Counting Modes](#ch14)


::: modecard
## Mode %10000: P_STATE_TICKS

**Time high and low states**

Measures duration of each state. IN raised on every transition with previous state duration.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X | Not used |
| Y | Not used |
| Z | Duration of previous state (clocks) |
| C flag | Previous state (1=was high) |
| IN | Every transition |

On reset (DIR=0), Z starts at **$0000_0001** (not 0), and Z saturates at **$8000_0000**.

### Key Constants
```spin2
P_STATE_TICKS | P_SCHMITT_A
```

### Quick Example
```spin2
WRPIN(pin, P_STATE_TICKS | P_SCHMITT_A)
PINH(pin)
REPEAT UNTIL PINREAD(pin)
duration := RDPIN(pin) wc                ' C=1 if was high
```

### Reference
[Chapter 13: Timing Measurement](#ch13)


::: modecard
## Mode %10001: P_HIGH_TICKS

**Time high states only**

Measures duration of high pulses. IN raised on high-to-low transition.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X | Not used |
| Y | Not used |
| Z | Duration of previous high (clocks) |
| IN | High-to-low transition |

On reset (DIR=0), Z starts at **$0000_0001** (not 0). Z saturates at $8000_0000, and bit 31 doubles as the overflow flag — which is why the example masks the result with `$7FFF_FFFF`.

### Key Constants
```spin2
P_HIGH_TICKS | P_SCHMITT_A
P_HIGH_TICKS | P_INVERT_A               ' To measure low pulses
```

### Quick Example
```spin2
WRPIN(pin, P_HIGH_TICKS | P_SCHMITT_A)
PINH(pin)
REPEAT UNTIL PINREAD(pin)
pulse_width := RDPIN(pin) & $7FFF_FFFF
```

### Reference
[Chapter 13: Timing Measurement](#ch13)


::: modecard
## Mode %10010: P_EVENTS_TICKS

**Time N events or detect timeout**

Two modes: measure time for X events (Y[2]=0), or detect timeout without events (Y[2]=1).
:::

### Register Usage

| Register | Function |
|----------|----------|
| X | Event count (Y[2]=0) or timeout clocks (Y[2]=1) |
| Y[1:0] | Event type: %00=high, %01=rise, %1x=edge |
| Y[2] | Mode: 0=events, 1=timeout |
| Z | Elapsed clocks |
| IN | Events complete or timeout |

### Key Constants
```spin2
P_EVENTS_TICKS
```

### Quick Example
```spin2
' Measure time for 100 rising edges
WRPIN(pin, P_EVENTS_TICKS)
WXPIN(pin, 100)
WYPIN(pin, %01)                          ' Rising edges, event mode
PINH(pin)
REPEAT UNTIL PINREAD(pin)
clocks := RDPIN(pin)
```

### Reference
[Chapter 13: Timing Measurement](#ch13)


::: modecard
## Mode %10011: P_PERIODS_TICKS

**Time X complete periods**

Measures total clock cycles for X signal periods.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X | Number of periods to measure |
| Y[1:0] | A→B event pair: %00 = A-rise→B-rise, %01 = A-rise→B-edge, %10 = A-edge→B-rise, %11 = A-edge→B-edge |
| Z | Total clocks for all periods |
| IN | Measurement complete |

This is a **two-input** mode — each period is measured from an A-input event to a B-input event, so B-input routing is required (set B to the same pin as A for single-pin cycle measurement). On reset (DIR=0), Z starts at **$0000_0000** — note that the period-counting modes reset Z to 0, unlike the state/timing modes (%10000–%10010), which reset to $0000_0001. Z saturates at $8000_0000.

### Key Constants
```spin2
P_PERIODS_TICKS
```

### Quick Example
```spin2
WRPIN(pin, P_PERIODS_TICKS)
WXPIN(pin, 100)                          ' Measure 100 periods
WYPIN(pin, %00)                          ' Rise to rise
PINH(pin)
REPEAT UNTIL PINREAD(pin)
total_clocks := RDPIN(pin)
freq := (100 * _clkfreq) / total_clocks
```

### Reference
[Chapter 15: Period and Frequency Measurement](#ch15)


::: modecard
## Mode %10100: P_PERIODS_HIGHS

**High time for X periods**

Accumulates high-state time across X periods for duty cycle measurement.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X | Number of periods |
| Y[1:0] | Trigger type |
| Z | Total high clocks across periods |
| IN | Measurement complete |

### Key Constants
```spin2
P_PERIODS_HIGHS
```

### Quick Example
```spin2
WRPIN(pin, P_PERIODS_HIGHS)
WXPIN(pin, 100)
WYPIN(pin, %00)
PINH(pin)
REPEAT UNTIL PINREAD(pin)
high_clocks := RDPIN(pin)
```

### Reference
[Chapter 15: Period and Frequency Measurement](#ch15)


::: modecard
## Mode %10101: P_COUNTER_TICKS

**Period time in X clock window**

Measures total period time within a minimum X-clock window.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X | Minimum window (clocks) |
| Y[1:0] | Trigger type |
| Z | Actual elapsed clocks |
| IN | Window complete |

### Key Constants
```spin2
P_COUNTER_TICKS
```

### Quick Example
```spin2
WRPIN(pin, P_COUNTER_TICKS)
WXPIN(pin, _clkfreq)                     ' 1 second window
WYPIN(pin, %00)
PINH(pin)
REPEAT UNTIL PINREAD(pin)
actual_time := RDPIN(pin)
```

### Reference
[Chapter 15: Period and Frequency Measurement](#ch15)


::: modecard
## Mode %10110: P_COUNTER_HIGHS

**High time in X clock window**

Accumulates high-state time within a minimum X-clock window.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X | Minimum window (clocks) |
| Y[1:0] | Trigger type |
| Z | Total high clocks in window |
| IN | Window complete |

### Key Constants
```spin2
P_COUNTER_HIGHS
```

### Quick Example
```spin2
WRPIN(pin, P_COUNTER_HIGHS)
WXPIN(pin, _clkfreq / 10)                ' 100ms window
WYPIN(pin, %00)
PINH(pin)
REPEAT UNTIL PINREAD(pin)
high_time := RDPIN(pin)
```

### Reference
[Chapter 15: Period and Frequency Measurement](#ch15)


::: modecard
## Mode %10111: P_COUNTER_PERIODS

**Count periods in X clock window**

Counts complete periods within a minimum X-clock window. Simple frequency counter.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X | Minimum window (clocks) |
| Y[1:0] | Trigger type |
| Z | Period count |
| IN | Window complete |

### Key Constants
```spin2
P_COUNTER_PERIODS
```

### Quick Example
```spin2
' Direct Hz reading with 1-second gate
WRPIN(pin, P_COUNTER_PERIODS)
WXPIN(pin, _clkfreq)                     ' 1 second
WYPIN(pin, %00)
PINH(pin)
REPEAT UNTIL PINREAD(pin)
frequency_hz := RDPIN(pin)
```

### Reference
[Chapter 15: Period and Frequency Measurement](#ch15)


::: modecard
## Mode %11000: P_ADC

**ADC with internal clock**

Sigma-delta ADC with SINC filtering. 8-14 bit resolution depending on sample period.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X[5:4] | Filter mode |
| X[3:0] | Sample period = 2^X clocks |
| Y | Period override (optional) |
| Z | ADC sample/accumulator |
| IN | Sample complete |

### Key Constants
```spin2
P_ADC_GIO | P_ADC                        ' Ground-referenced
P_ADC_10X | P_ADC                        ' 10x gain
```

### Quick Example
```spin2
WRPIN(pin, P_ADC_GIO | P_ADC)
WXPIN(pin, %00_0111)                     ' SINC2 sampling, 128 clocks
PINH(pin)
sample := RDPIN(pin)
```

### Reference
[Chapter 16: ADC (Analog Input)](#ch16)


::: modecard
## Mode %11001: P_ADC_EXT

**ADC with external clock**

Samples A-input data on B-input clock edges. For external delta-sigma ADCs.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X[5:4] | Filter mode |
| X[3:0] | Base sample period |
| Y | Period override |
| Z | ADC sample/accumulator |
| A-input | External ADC data |
| B-input | External clock |
| IN | Sample complete |

### Key Constants
```spin2
P_ADC_EXT | P_PLUS1_B
```

### Quick Example
```spin2
WRPIN(pin, P_ADC_EXT | P_PLUS1_B)
WXPIN(pin, %00_0111)
PINH(pin)
```

### Reference
[Chapter 16: ADC (Analog Input)](#ch16)


::: modecard
## Mode %11010: P_ADC_SCOPE

**ADC triggered scope capture**

Four-channel oscilloscope-style ADC with hysteretic triggering.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X[15:8] | Trigger level |
| X[7:0] | Arm level |
| Z | 4 × 8-bit samples |
| IN | Trigger fired |

### Key Constants
```spin2
P_ADC_GIO | P_ADC_SCOPE
```

### Quick Example
```spin2
' Pin must be multiple of 4
WRPIN(52, P_ADC_GIO | P_ADC_SCOPE)
WXPIN(52, (128 << 8) | 64)               ' Trigger=128, Arm=64
PINH(52)
```

### Reference
[Chapter 16: ADC (Analog Input)](#ch16)


::: modecard
## Mode %11011: P_USB_PAIR

**USB differential pair**

USB 1.1 physical layer for even/odd pin pair. Handles differential signaling.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X | Configuration |
| Y | Protocol control |
| Z | Data/status |
| Even pin | D- (DM) |
| Odd pin | D+ (DP) |
| IN | USB event |

### Key Constants
```spin2
P_USB_PAIR | P_OE
```

### Quick Example
```spin2
' Pins must be consecutive even/odd pair
WRPIN(56, P_USB_PAIR | P_OE)             ' 56=D-, 57=D+
PINH(56)
PINH(57)
```

### Reference
[Chapter 19: USB Host/Device](#ch19)


::: modecard
## Mode %11100: P_SYNC_TX

**Synchronous serial transmit**

Clocked serial transmission for SPI master and similar protocols.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X[5] | Mode: 0=continuous, 1=start-stop |
| X[4:0] | Bits minus 1 |
| Y | Transmit data (LSB first) |
| B-input | Clock source |
| IN | Buffer empty |

### Key Constants
```spin2
P_SYNC_TX | P_OE | P_PLUS1_B             ' Clock from next pin
P_SYNC_TX | P_OE | P_MINUS1_B            ' Clock from prev pin
```

### Quick Example
```spin2
' Data on pin 41, clock on pin 40
WRPIN(41, P_SYNC_TX | P_OE | P_MINUS1_B)
WXPIN(41, %1_00111)                      ' Start-stop, 8 bits
PINH(41)
WYPIN(41, data)
```

### Reference
[Chapter 11: Serial Transmission](#ch11)


::: modecard
## Mode %11101: P_SYNC_RX

**Synchronous serial receive**

Clocked serial reception for SPI slave and similar protocols.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X[5] | Mode: 0=continuous, 1=start-stop |
| X[4:0] | Bits minus 1 |
| Y | Not used |
| Z | Received data (left-justified) |
| B-input | Clock source |
| IN | Data ready |

### Key Constants
```spin2
P_SYNC_RX | P_PLUS1_B                    ' Clock from next pin
```

### Quick Example
```spin2
WRPIN(pin, P_SYNC_RX | P_PLUS1_B)
WXPIN(pin, %1_00111)                     ' Start-stop, 8 bits
PINH(pin)
REPEAT UNTIL PINREAD(pin)
data := RDPIN(pin) >> 24                 ' Left-justified, shift down
```

### Reference
[Chapter 17: Serial Receive](#ch17)


::: modecard
## Mode %11110: P_ASYNC_TX

**Asynchronous serial transmit**

UART-style transmission with automatic start/stop bit generation.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X[31:16] | Bit period (clocks) |
| X[15:10] | Fractional (1/64 clock) |
| X[4:0] | Data bits |
| Y | Transmit data (LSB first) |
| IN | Ready for next byte |

### Key Constants
```spin2
P_ASYNC_TX | P_OE
P_ASYNC_TX | P_OE | P_INVERT_OUTPUT      ' RS-232
```

### Quick Example
```spin2
bit_period := (_clkfreq / 115200) << 16
WRPIN(pin, P_ASYNC_TX | P_OE)
WXPIN(pin, bit_period | 8)               ' 8 data bits
PINLOW(pin)
REPEAT UNTIL PINREAD(pin)
WYPIN(pin, byte_value)
```

### Reference
[Chapter 11: Serial Transmission](#ch11)


::: modecard
## Mode %11111: P_ASYNC_RX

**Asynchronous serial receive**

UART-style reception with automatic start bit detection and framing.
:::

### Register Usage

| Register | Function |
|----------|----------|
| X[31:16] | Bit period (clocks) |
| X[15:10] | Fractional (1/64 clock) |
| X[4:0] | Data bits |
| Z | Received data (right-justified) |
| IN | Byte received |

### Key Constants
```spin2
P_ASYNC_RX
P_ASYNC_RX | P_INVERT_IN                 ' RS-232
```

### Quick Example
```spin2
bit_period := (_clkfreq / 115200) << 16
WRPIN(pin, P_ASYNC_RX)
WXPIN(pin, bit_period | 8)
PINH(pin)
REPEAT UNTIL PINREAD(pin)
data := RDPIN(pin) & $FF
```

### Reference
[Chapter 17: Serial Receive](#ch17)


*For full mode details, see the referenced chapters. For P_ constant values, see Appendix B.*
