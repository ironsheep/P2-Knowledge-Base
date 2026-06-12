# Chapter 8: Frequency Generation (NCO) {#ch8}

This chapter covers the two Numerically Controlled Oscillator (NCO) modes: **P_NCO_FREQ** (%00110) for precise frequency generation with 50% duty cycle, and **P_NCO_DUTY** (%00111) for frequency generation with variable duty cycle.


## 8.1 NCO Concept

### What is an NCO?

A Numerically Controlled Oscillator generates precise frequencies by accumulating a phase value. On each clock (or base period), a frequency control word is added to a phase accumulator. When the accumulator overflows (or crosses a threshold), the output toggles.

### P2 NCO Architecture

```{=latex}
\DiagNcoArch
```

### Key Properties

- **Frequency resolution**: 32-bit phase accumulator provides ~0.05 Hz resolution at 200 MHz
- **Phase coherence**: Multiple NCOs can be phase-locked via initial phase setting
- **Deterministic timing**: Hardware-based, independent of software execution


## 8.2 P_NCO_FREQ Mode (%00110)

### Function

P_NCO_FREQ generates a square wave at a precise frequency. The output reflects the MSB of the phase accumulator (Z[31]), creating a 50% duty cycle output.

### Configuration

| Register | Field | Purpose |
|----------|-------|---------|
| X[15:0] | Base period | Clock cycles between phase updates |
| X[31:16] | Initial phase | Written to Z[31:16] on WXPIN |
| Y[31:0] | Frequency control | Added to Z each base period |
| Z[31:0] | Phase accumulator | Z[31] drives output |

### Output Behavior

On each base period (every X[15:0] clocks):

1. Y is added to Z
2. Output = Z[31]
3. If Z overflows, IN is raised

The output toggles when Z[31] changes, creating a square wave.

### Frequency Formula

```formula
frequency = (Y × sysclk) / (X[15:0] × 2³²)
```

For X[15:0] = 1 (maximum update rate):
```formula
frequency = (Y × sysclk) / 2³²
```

Solving for Y:
```formula
Y = (frequency × 2³²) / sysclk
```

### Worked Examples

**Example 1: 1 kHz at 200 MHz sysclk**
```formula
Y = (1000 × 4,294,967,296) / 200,000,000
Y = 4,294,967,296,000 / 200,000,000
Y = 21,475
```

**Example 2: 44.1 kHz (audio sample rate) at 200 MHz**
```formula
Y = (44100 × 4,294,967,296) / 200,000,000
Y = 189,408,057,753,600 / 200,000,000
Y = 947,040
```

**Example 3: 1 MHz at 200 MHz**
```formula
Y = (1,000,000 × 4,294,967,296) / 200,000,000
Y = 21,474,836
```

### Configuration Sequence

**Spin2:**
```spin2
CON
  _clkfreq = 200_000_000
  NCO_PIN = 10

PUB nco_frequency(freq_hz) | y_value
  ' Calculate Y for desired frequency
  y_value := freq_hz FRAC _clkfreq
  
  PINFLOAT(NCO_PIN)
  WRPIN(NCO_PIN, P_NCO_FREQ | P_OE)
  WXPIN(NCO_PIN, 1)                       ' Base period = 1 clock
  WYPIN(NCO_PIN, y_value)
  PINLOW(NCO_PIN)
```

**PASM2:**
```pasm2
              dirl      #NCO_PIN
              wrpin     ##(P_NCO_FREQ | P_OE), #NCO_PIN
              wxpin     #1, #NCO_PIN              ' Base period = 1
              wypin     freq_y, #NCO_PIN          ' Frequency value
              drvl      #NCO_PIN
```

### Resolution vs Update Rate Tradeoff

Using X[15:0] > 1 reduces update rate but can smooth jitter:

| X[15:0] | Updates/sec at 200 MHz | Effect |
|---------|------------------------|--------|
| 1 | 200,000,000 | Maximum resolution |
| 10 | 20,000,000 | Reduced jitter |
| 100 | 2,000,000 | Lower CPU access rate |

For most applications, X[15:0] = 1 provides best frequency resolution.


## 8.3 P_NCO_DUTY Mode (%00111)

### Function

P_NCO_DUTY generates a frequency with variable duty cycle. The output reflects the phase accumulator overflow state, allowing duty cycle control.

### Key Difference from P_NCO_FREQ

| Mode | Output Based On | Duty Cycle |
|------|-----------------|------------|
| P_NCO_FREQ | Z[31] | Always 50% |
| P_NCO_DUTY | Z overflow | Variable |

### Duty Cycle Control

In P_NCO_DUTY, Y sets the duty cycle directly — the accumulator (Z) is incremented by Y each base period, and the output is high for one base period on every overflow, so the fraction of high time is Y / 2³²:

- Larger Y values → Higher duty cycle
- Smaller Y values → Lower duty cycle

The duty cycle is approximately:
```formula
duty_cycle ≈ Y / 2³²
```

**Example:**
```formula
Y = $8000_0000 → 50% duty cycle
Y = $4000_0000 → 25% duty cycle
Y = $C000_0000 → 75% duty cycle
```

### Configuration

**Spin2:**
```spin2
CON
  _clkfreq = 200_000_000
  NCO_PIN = 10

PUB nco_duty(duty_percent) | y_value
  ' In NCO_DUTY, Y sets the duty cycle directly: duty = Y / 2^32.
  ' (Base period is 1 clock, so Z accumulates Y every clock.)
  y_value := duty_percent frac 100        ' 50 -> $8000_0000, 25 -> $4000_0000

  PINFLOAT(NCO_PIN)
  WRPIN(NCO_PIN, P_NCO_DUTY | P_OE)
  WXPIN(NCO_PIN, 1)
  WYPIN(NCO_PIN, y_value)
  PINLOW(NCO_PIN)
```


## 8.4 Phase Synchronization

### Setting Initial Phase

X[31:16] sets the initial phase when WXPIN is executed:

```spin2
' Phase offset in 16-bit units (0 = 0°, 32768 = 180°, 65535 = ~360°)
phase_offset := 32768                     ' 180° offset
WXPIN(pin, 1 | (phase_offset << 16))
```

### Multi-Pin Phase Lock

For phase-locked outputs (e.g., three-phase motor control):

```spin2
CON
  _clkfreq = 200_000_000
  PHASE_A = 10
  PHASE_B = 11
  PHASE_C = 12
  FREQ_HZ = 1000

PUB three_phase_nco() | y_val, phase_120, phase_240
  y_val := FREQ_HZ FRAC _clkfreq
  
  ' Phase offsets: 0°, 120°, 240°
  phase_120 := 65536 / 3                  ' 21845
  phase_240 := 65536 * 2 / 3              ' 43691
  
  ' Configure all three
  PINFLOAT(PHASE_A)
  PINFLOAT(PHASE_B)
  PINFLOAT(PHASE_C)
  
  WRPIN(PHASE_A, P_NCO_FREQ | P_OE)
  WRPIN(PHASE_B, P_NCO_FREQ | P_OE)
  WRPIN(PHASE_C, P_NCO_FREQ | P_OE)
  
  WXPIN(PHASE_A, 1 | (0 << 16))           ' 0° phase
  WXPIN(PHASE_B, 1 | (phase_120 << 16))   ' 120° phase
  WXPIN(PHASE_C, 1 | (phase_240 << 16))   ' 240° phase
  
  ' Same frequency for all
  WYPIN(PHASE_A, y_val)
  WYPIN(PHASE_B, y_val)
  WYPIN(PHASE_C, y_val)
  
  ' Enable all simultaneously
  PINLOW(PHASE_A..PHASE_C)
```

### Phase Coherence

When multiple NCOs use the same Y value and are enabled simultaneously:

- They maintain constant phase relationship
- Phase offset is set by X[31:16] at configuration
- No drift between channels


## 8.5 Analog Output with DAC

### NCO + DAC for Sine Wave Approximation

Combine NCO with DAC modes for analog output:

```spin2
' NCO output through DAC filter
WRPIN(pin, P_NCO_FREQ | P_OE | P_DAC_990R_3V)
```

The square wave NCO output, when filtered by the resistor DAC and external RC filter, approximates a sine wave.

### Direct DAC Control

For true analog waveform generation, use the DAC modes with software updates (see Chapter 10) rather than NCO modes.


## 8.6 Frequency Accuracy Analysis

### Maximum Frequency

Maximum output frequency is sysclk / 2 (Nyquist limit):
```formula
At 200 MHz: max frequency = 100 MHz
Achieved with Y = $8000_0000
```

### Minimum Frequency

Minimum frequency with X[15:0] = 1:
```formula
min_freq = sysclk / 2³²
At 200 MHz: min_freq ≈ 0.047 Hz
```

### Frequency Error

Frequency error depends on the fractional part of Y:

```formula
Actual frequency = round(Y) × sysclk / 2³²
Error = |target - actual| / target × 100%
```

**Example: 1 kHz target at 200 MHz**
```formula
Y_exact = 21474.83648
Y_rounded = 21475
Actual freq = 21475 × 200,000,000 / 4,294,967,296 = 1000.0076 Hz
Error = 0.00076%
```

### Frequency Resolution Table

| sysclk | Resolution (X=1) |
|--------|------------------|
| 100 MHz | 0.0233 Hz |
| 180 MHz | 0.0419 Hz |
| 250 MHz | 0.0582 Hz |
| 350 MHz | 0.0815 Hz |


## 8.7 Complete Examples

### Example 1: Audio Tone Generator

```spin2
CON
  _clkfreq = 200_000_000
  SPEAKER_PIN = 56

PUB play_tone(frequency, duration_ms) | y_val
  y_val := frequency FRAC _clkfreq
  
  PINFLOAT(SPEAKER_PIN)
  WRPIN(SPEAKER_PIN, P_NCO_FREQ | P_OE)
  WXPIN(SPEAKER_PIN, 1)
  WYPIN(SPEAKER_PIN, y_val)
  PINLOW(SPEAKER_PIN)
  
  WAITMS(duration_ms)
  
  PINFLOAT(SPEAKER_PIN)                   ' Stop tone

PUB play_scale()
  play_tone(262, 500)                     ' C4
  play_tone(294, 500)                     ' D4
  play_tone(330, 500)                     ' E4
  play_tone(349, 500)                     ' F4
  play_tone(392, 500)                     ' G4
  play_tone(440, 500)                     ' A4
  play_tone(494, 500)                     ' B4
  play_tone(523, 500)                     ' C5
```

### Example 2: Variable Frequency Clock

```spin2
CON
  _clkfreq = 200_000_000
  CLK_PIN = 20

VAR
  long current_y

PUB setup_clock(initial_freq)
  current_y := initial_freq FRAC _clkfreq
  
  PINFLOAT(CLK_PIN)
  WRPIN(CLK_PIN, P_NCO_FREQ | P_OE)
  WXPIN(CLK_PIN, 1)
  WYPIN(CLK_PIN, current_y)
  PINLOW(CLK_PIN)

PUB set_frequency(new_freq)
  current_y := new_freq FRAC _clkfreq
  WYPIN(CLK_PIN, current_y)               ' Update on the fly
```

### Example 3: PASM2 Frequency Sweep

```pasm2
CON
  _clkfreq = 200_000_000

DAT           org

' Setup NCO at 1 kHz
              dirl      #NCO_PIN
              wrpin     ##(P_NCO_FREQ | P_OE), #NCO_PIN
              wxpin     #1, #NCO_PIN
              wypin     y_start, #NCO_PIN
              drvl      #NCO_PIN

' Sweep frequency upward
sweep_loop
              add       y_current, y_step
              wypin     y_current, #NCO_PIN
              waitx     sweep_delay
              cmp       y_current, y_end wc
        if_c  jmp       #sweep_loop
              
              jmp       #$

NCO_PIN       long      10
y_start       long      21475             ' 1 kHz
y_end         long      214748            ' 10 kHz
y_step        long      215               ' ~10 Hz step
y_current     long      0
sweep_delay   long      2_000_000         ' 10 ms between steps
```


## 8.8 Quick Reference

### P_NCO_FREQ Configuration

| Parameter | Register | Formula |
|-----------|----------|---------|
| Base period | X[15:0] | 1 for maximum resolution |
| Initial phase | X[31:16] | 0-65535 (0°-360°) |
| Frequency | Y | (freq × 2³²) / sysclk |

### P_NCO_DUTY Configuration

| Parameter | Register | Formula |
|-----------|----------|---------|
| Base period | X[15:0] | 1 for maximum resolution |
| Initial phase | X[31:16] | 0-65535 (0°-360°) |
| Freq × duty | Y | Varies by desired duty |

### Common Y Values at 200 MHz

| Frequency | Y Value |
|-----------|---------|
| 100 Hz | 2,147 |
| 1 kHz | 21,475 |
| 10 kHz | 214,748 |
| 100 kHz | 2,147,484 |
| 1 MHz | 21,474,836 |
| 10 MHz | 214,748,365 |

### Reset State

Both modes when DIR=0:

- IN = low
- Output = low
- Z = 0


*This chapter covered NCO-based frequency generation. For PWM output with variable duty cycle, see Chapter 9. For DAC analog output, see Chapter 10.*
