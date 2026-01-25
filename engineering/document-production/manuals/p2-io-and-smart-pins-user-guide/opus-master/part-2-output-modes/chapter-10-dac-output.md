# Chapter 10: DAC Output

This chapter covers digital-to-analog conversion using the P2's built-in DAC capabilities. Topics include the resistor DAC output options, 8-bit direct DAC control, and 16-bit dithered DAC modes: **P_DAC_DITHER_RND** (%00010) and **P_DAC_DITHER_PWM** (%00011).

---

## 10.1 DAC Architecture Overview

### P2 DAC Structure

Each P2 I/O pin includes analog output capability through a resistive DAC network. The DAC operates at 8-bit resolution natively, with dithering modes available to achieve effective 16-bit resolution.

```
                    ┌─────────────────────────────────────┐
M[7:0] ────────────►│        8-bit DAC                   │
(from Smart Pin     │     (per-pin resistor network)     │
 or WRPIN)          └─────────────────────────────────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────────────┐
M[12:10] ──────────►│    Output Mode Selection           │
(%101 = DAC)        │  990Ω / 600Ω / 124Ω / 75Ω         │
                    └─────────────────────────────────────┘
                                    │
                                    ▼
                                 PIN OUT
```

### DAC Mode Enable

The DAC output requires M[12:10] = %101 in the pin configuration. This is automatically set by the P_DAC_* constants:

| Constant | Resistance | Voltage Range | Current Capability |
|----------|------------|---------------|-------------------|
| P_DAC_990R_3V | 990Ω | 0 to 3.3V | ~3.3 mA max |
| P_DAC_600R_2V | 600Ω | 0 to 2.0V | ~3.3 mA max |
| P_DAC_124R_3V | 124Ω | 0 to 3.3V | ~27 mA max |
| P_DAC_75R_2V | 75Ω | 0 to 2.0V | ~27 mA max |

### Resolution Options

| Mode | Resolution | Update Rate | Best For |
|------|------------|-------------|----------|
| Direct (M[7:0]) | 8-bit | Every clock | Fast signals |
| Dithered PRNG | 16-bit | Sample period | Control signals |
| Dithered PWM | 16-bit | Sample period | Audio |

---

## 10.2 Resistor DAC Options

### Understanding the DAC Network

The P2 uses a resistor-weighted DAC that switches between voltage rails. The resistance values determine both the output impedance and the voltage swing.

### P_DAC_990R_3V

High impedance, full voltage range.

**Specifications:**
- Output impedance: 990Ω
- Voltage range: 0V to 3.3V
- Bit weight: 3.3V / 256 = 12.9 mV/LSB
- Drive current: Limited (~3.3 mA at full scale)

**Best for:**
- High-impedance loads
- Voltage references
- Signals to op-amp inputs
- Low-power applications

**Spin2:**
```spin2
WRPIN(pin, P_DAC_990R_3V | P_OE)
DIRH(pin)
```

### P_DAC_600R_2V

Lower impedance, reduced voltage range.

**Specifications:**
- Output impedance: 600Ω
- Voltage range: 0V to 2.0V
- Bit weight: 2.0V / 256 = 7.8 mV/LSB
- Drive current: Moderate (~3.3 mA at full scale)

**Best for:**
- Interface to 2V systems
- Better load driving than 990Ω
- Moderate current requirements

### P_DAC_124R_3V

Low impedance, full voltage range.

**Specifications:**
- Output impedance: 124Ω
- Voltage range: 0V to 3.3V
- Bit weight: 3.3V / 256 = 12.9 mV/LSB
- Drive current: High (~27 mA at full scale)

**Best for:**
- Driving cables
- Direct speaker drive
- LED brightness control
- Low-impedance loads

### P_DAC_75R_2V

Lowest impedance, reduced voltage range.

**Specifications:**
- Output impedance: 75Ω
- Voltage range: 0V to 2.0V
- Bit weight: 2.0V / 256 = 7.8 mV/LSB
- Drive current: Highest (~27 mA at full scale)

**Best for:**
- 75Ω cable termination
- Video signals (though limited to 2V)
- Maximum current drive

### Selection Guide

| Application | Recommended | Reason |
|-------------|-------------|--------|
| Op-amp input | P_DAC_990R_3V | High impedance acceptable |
| Audio to amp | P_DAC_600R_2V | Balance of drive and range |
| Direct speaker | P_DAC_124R_3V | Current drive needed |
| LED control | P_DAC_124R_3V | Current source capability |
| Coax cable | P_DAC_75R_2V | Impedance matching |

---

## 10.3 Direct 8-bit DAC Control

### Using WRPIN for Static DAC

For simple DAC output without smart pin modes, write the value directly:

**Spin2:**
```spin2
CON
  DAC_PIN = 20

PUB set_voltage_8bit(value) | mode
  ' Configure for 8-bit DAC output
  ' Value in M[7:0] of WRPIN D operand
  mode := (value << 8) | P_DAC_124R_3V
  WRPIN(DAC_PIN, mode)
  DIRH(DAC_PIN)

PUB voltage_to_dac(millivolts) : dac_value
  ' Convert millivolts to 8-bit DAC value (3.3V range)
  dac_value := millivolts * 256 / 3300
  dac_value := 0 #> dac_value <# 255
```

**PASM2:**
```pasm2
              ' Set DAC to mid-scale (128)
              mov       dac_mode, ##($80 << 8) | P_DAC_990R_3V
              wrpin     dac_mode, #DAC_PIN
              dirh      #DAC_PIN
```

### Updating DAC Value

To change the DAC output, issue a new WRPIN with the updated M[7:0] field:

**Spin2:**
```spin2
PUB update_dac(pin, value) | current_mode
  ' Read current mode, update value bits
  current_mode := (value << 8) | P_DAC_124R_3V
  WRPIN(pin, current_mode)
```

### BIT_DAC Mode

When OUT controls the pin (not a smart pin mode), M[7:4] and M[3:0] define two DAC levels:
- OUT=1: M[7:4] duplicated as {M[7:4], M[7:4]}
- OUT=0: M[3:0] duplicated as {M[3:0], M[3:0]}

This creates a simple 2-level DAC controlled by the OUT bit.

---

## 10.4 16-bit Dithered DAC Modes

### Dithering Concept

The P2 achieves 16-bit DAC resolution using 8-bit hardware plus temporal dithering. By rapidly switching between adjacent 8-bit values in a precise pattern, the time-averaged output achieves 16-bit resolution.

```
Target: $8040 (16-bit)
Upper byte: $80 (128)
Lower byte: $40 (64 of 256)

Output pattern: 75% at $80, 25% at $81
Average = 0.75 × 128 + 0.25 × 129 = 128.25 ≈ $80.40
```

### P_DAC_DITHER_RND (%00010)

Uses pseudo-random dithering for smooth 16-bit output.

**Characteristics:**
- Random switching between adjacent levels
- Uniform spectral distribution of dither noise
- No periodic artifacts
- Suitable for control signals

**Configuration:**

| Register | Purpose |
|----------|---------|
| X[15:0] | Sample period in clocks (1 = immediate update) |
| Y[15:0] | 16-bit DAC value |
| Z | ADC accumulation (if OUT=1) |

**Spin2:**
```spin2
CON
  _clkfreq = 200_000_000
  DAC_PIN = 48

PUB dithered_dac_prng(value16) | mode
  ' Setup 16-bit PRNG dithered DAC
  mode := P_DAC_DITHER_RND | P_DAC_124R_3V | P_OE

  PINFLOAT(DAC_PIN)
  WRPIN(DAC_PIN, mode)
  WXPIN(DAC_PIN, 1)                       ' Immediate updates
  WYPIN(DAC_PIN, value16)
  PINLOW(DAC_PIN)

PUB update_value(value16)
  WYPIN(DAC_PIN, value16)                 ' Takes effect immediately
```

**PASM2:**
```pasm2
              dirl      #DAC_PIN
              wrpin     ##(P_DAC_DITHER_RND | P_DAC_124R_3V | P_OE), #DAC_PIN
              wxpin     #1, #DAC_PIN       ' Immediate mode
              dirh      #DAC_PIN
              wypin     value16, #DAC_PIN
```

### P_DAC_DITHER_PWM (%00011)

Uses PWM dithering for better dynamic range.

**Characteristics:**
- Maximum 2 transitions per 256 clocks
- Lower switching noise than PRNG
- Fclock/256 component at -48 dB
- Suitable for audio applications

**Configuration:**

| Register | Purpose |
|----------|---------|
| X[15:0] | Sample period (must be multiple of 256) |
| Y[15:0] | 16-bit DAC value |
| Z | ADC accumulation (if OUT=1) |

**Spin2:**
```spin2
CON
  _clkfreq = 200_000_000
  DAC_PIN = 48
  SAMPLE_PERIOD = 256                     ' Minimum (256 clocks)

PUB dithered_dac_pwm(value16) | mode
  ' Setup 16-bit PWM dithered DAC
  mode := P_DAC_DITHER_PWM | P_DAC_600R_2V | P_OE

  PINFLOAT(DAC_PIN)
  WRPIN(DAC_PIN, mode)
  WXPIN(DAC_PIN, SAMPLE_PERIOD)           ' Must be multiple of 256
  WYPIN(DAC_PIN, value16)
  PINLOW(DAC_PIN)

PUB update_value_sync(value16)
  ' Wait for sample complete before update
  repeat until PINREAD(DAC_PIN) & $8000_0000
  WYPIN(DAC_PIN, value16)
```

**PASM2:**
```pasm2
              dirl      #DAC_PIN
              wrpin     ##(P_DAC_DITHER_PWM | P_DAC_600R_2V | P_OE), #DAC_PIN
              wxpin     ##256, #DAC_PIN    ' Sample period
              dirh      #DAC_PIN
              wypin     value16, #DAC_PIN

.wait         testp     #DAC_PIN wc        ' Wait for IN flag
        if_nc jmp       #.wait
              wypin     new_value, #DAC_PIN
```

### Comparing Dithering Methods

| Aspect | PRNG Dither | PWM Dither |
|--------|-------------|------------|
| Transitions | Random (many) | Max 2 per 256 clocks |
| Spectrum | White noise floor | Fclock/256 tone at -48 dB |
| Dynamic range | Good | Better |
| Best for | Control signals | Audio |
| Sample period | Any value ≥1 | Multiple of 256 |

---

## 10.5 DAC with Other Modes

### NCO + DAC for Waveform Generation

Combine NCO frequency generation with DAC output:

**Spin2:**
```spin2
CON
  _clkfreq = 200_000_000
  WAVE_PIN = 20

PUB nco_dac_wave(freq_hz) | mode, y_val
  ' NCO square wave through DAC for filtered sine output
  mode := P_NCO_FREQ | P_DAC_990R_3V | P_OE
  y_val := (freq_hz * $1_0000_0000) / _clkfreq

  PINFLOAT(WAVE_PIN)
  WRPIN(WAVE_PIN, mode)
  WXPIN(WAVE_PIN, 1)
  WYPIN(WAVE_PIN, y_val)
  PINLOW(WAVE_PIN)
```

The NCO generates a square wave, and with external RC filtering, approximates a sine wave.

### PWM + DAC Integration

PWM modes can combine with DAC for analog PWM output:

```spin2
' PWM triangle through DAC for smooth analog output
mode := P_PWM_TRIANGLE | P_DAC_600R_2V | P_OE
```

---

## 10.6 ADC Feedback

### Monitoring DAC Loading

Dithered DAC modes support ADC feedback to measure pin loading:

**Spin2:**
```spin2
PUB read_dac_loading(pin) : loading | mode
  ' Enable ADC feedback (OUT=1)
  PINWRITE(pin, 1)

  ' Wait for accumulation
  WAITUS(100)

  ' Read ADC value
  loading := RDPIN(pin)
```

The ADC accumulates samples during the sample period. The result indicates how the DAC output is being loaded by external circuitry.

### Load Detection Applications

- Verify expected load impedance
- Detect open/short conditions
- Implement current limiting
- Calibrate DAC output

---

## 10.7 Voltage Calculation

### 8-bit DAC Voltage

```
Voltage = (DAC_value / 256) × Full_Scale_Voltage

For P_DAC_990R_3V or P_DAC_124R_3V:
  Voltage = (DAC_value / 256) × 3.3V

For P_DAC_600R_2V or P_DAC_75R_2V:
  Voltage = (DAC_value / 256) × 2.0V
```

### 16-bit DAC Voltage

```
Voltage = (DAC_value / 65536) × Full_Scale_Voltage

For 3.3V range:
  Voltage = (DAC_value / 65536) × 3.3V
  Resolution = 3.3V / 65536 = 50.4 µV/LSB

For 2.0V range:
  Voltage = (DAC_value / 65536) × 2.0V
  Resolution = 2.0V / 65536 = 30.5 µV/LSB
```

### Voltage to DAC Value

**Spin2:**
```spin2
PUB millivolts_to_dac16(mv, full_scale_mv) : dac16
  ' Convert millivolts to 16-bit DAC value
  dac16 := (mv * 65536) / full_scale_mv
  dac16 := 0 #> dac16 <# 65535

PUB set_voltage_mv(pin, mv)
  ' Set DAC to specific voltage (3.3V full scale)
  wypin(pin, millivolts_to_dac16(mv, 3300))
```

---

## 10.8 Complete Examples

### Example 1: Simple Voltage Reference

```spin2
CON
  _clkfreq = 200_000_000
  REF_PIN = 20

PUB voltage_reference(millivolts) | mode, dac_val
  ' Create stable voltage reference
  ' Using 16-bit PWM dithered DAC for precision

  mode := P_DAC_DITHER_PWM | P_DAC_990R_3V | P_OE
  dac_val := (millivolts * 65536) / 3300

  PINFLOAT(REF_PIN)
  WRPIN(REF_PIN, mode)
  WXPIN(REF_PIN, 256)                     ' Minimum sample period
  WYPIN(REF_PIN, dac_val)
  PINLOW(REF_PIN)

PUB set_2v5_reference()
  voltage_reference(2500)                 ' 2.5V output
```

### Example 2: Audio Waveform Generator

```spin2
CON
  _clkfreq = 200_000_000
  AUDIO_PIN = 48
  SAMPLE_RATE = 44100

VAR
  long phase
  long phase_inc

PUB audio_init()
  ' Initialize audio DAC at 44.1 kHz
  PINFLOAT(AUDIO_PIN)
  WRPIN(AUDIO_PIN, P_DAC_DITHER_PWM | P_DAC_600R_2V | P_OE)
  WXPIN(AUDIO_PIN, _clkfreq / SAMPLE_RATE / 256 * 256)  ' Round to 256
  WYPIN(AUDIO_PIN, $8000)                 ' Start at mid-scale
  PINLOW(AUDIO_PIN)

  phase := 0

PUB set_frequency(hz)
  ' Set sine wave frequency
  phase_inc := (hz * $1_0000_0000) / SAMPLE_RATE

PUB audio_sample() : sample | sine_val
  ' Generate next audio sample
  phase += phase_inc

  ' Get sine value (-32768 to +32767)
  sine_val := sin(phase >> 16)

  ' Convert to 16-bit unsigned (0 to 65535)
  sample := sine_val + $8000

PUB audio_output()
  ' Output audio sample
  repeat until PINREAD(AUDIO_PIN) & $8000_0000
  WYPIN(AUDIO_PIN, audio_sample())
```

### Example 3: DC Motor Speed Control

```spin2
CON
  _clkfreq = 200_000_000
  MOTOR_PIN = 16

VAR
  long current_speed
  long target_speed

PUB motor_init()
  ' Initialize motor control DAC
  PINFLOAT(MOTOR_PIN)
  WRPIN(MOTOR_PIN, P_DAC_DITHER_RND | P_DAC_124R_3V | P_OE)
  WXPIN(MOTOR_PIN, 1)                     ' Fast updates
  WYPIN(MOTOR_PIN, 0)                     ' Start stopped
  PINLOW(MOTOR_PIN)

  current_speed := 0
  target_speed := 0

PUB set_motor_speed(percent)
  ' Set target speed (0-100%)
  target_speed := (percent * 65535) / 100

PUB motor_ramp_update()
  ' Smooth acceleration/deceleration
  if current_speed < target_speed
    current_speed += (target_speed - current_speed) / 10 + 1
  elseif current_speed > target_speed
    current_speed -= (current_speed - target_speed) / 10 + 1

  WYPIN(MOTOR_PIN, current_speed)
```

### Example 4: PASM2 Function Generator

```pasm2
CON
  _clkfreq = 200_000_000

DAT           org

' Initialize 16-bit dithered DAC
              dirl      #DAC_PIN
              wrpin     ##(P_DAC_DITHER_PWM | P_DAC_990R_3V | P_OE), #DAC_PIN
              wxpin     ##512, #DAC_PIN    ' 512 clock sample period
              dirh      #DAC_PIN

' Generate sawtooth wave
saw_loop
              wypin     value16, #DAC_PIN
              add       value16, step_size
              waitx     delay
              jmp       #saw_loop

' Generate triangle wave
tri_loop
              wypin     value16, #DAC_PIN
              add       value16, direction
              cmp       value16, ##$FFFF wz
        if_z  neg       direction
              cmp       value16, #0 wz
        if_z  neg       direction
              waitx     delay
              jmp       #tri_loop

DAC_PIN       long      20
value16       long      0
step_size     long      256                ' Increment per sample
direction     long      256
delay         long      2000               ' Sample interval
```

---

## 10.9 Design Considerations

### Output Impedance and Loading

The DAC output impedance determines load driving capability:

| DAC Type | Output Z | Max Load | Voltage Drop at 1mA |
|----------|----------|----------|-------------------|
| P_DAC_990R_3V | 990Ω | >10kΩ | 0.99V |
| P_DAC_600R_2V | 600Ω | >6kΩ | 0.60V |
| P_DAC_124R_3V | 124Ω | >1.2kΩ | 0.12V |
| P_DAC_75R_2V | 75Ω | >750Ω | 0.08V |

### External Buffering

For driving low-impedance loads or cables, add an external buffer:

```
          ┌────────────┐
DAC OUT ──┤    Op-Amp  ├─── Buffered Out
          │  (unity)   │
          └────────────┘
```

### Filtering Dither Noise

For clean analog output, add an RC low-pass filter:

```
DAC OUT ───[R]───┬─── Filtered Out
                 │
                [C]
                 │
                GND
```

Cutoff frequency: fc = 1 / (2π × R × C)

### Power Supply Considerations

- DAC output is relative to pin ground
- Ensure clean power supply for best performance
- Consider decoupling near the pin
- Load current affects power dissipation

---

## 10.10 Quick Reference

### Resistor DAC Constants

| Constant | Resistance | Voltage | Mode Bits |
|----------|------------|---------|-----------|
| P_DAC_990R_3V | 990Ω | 3.3V | M[12:10]=%101 |
| P_DAC_600R_2V | 600Ω | 2.0V | M[12:10]=%101 |
| P_DAC_124R_3V | 124Ω | 3.3V | M[12:10]=%101 |
| P_DAC_75R_2V | 75Ω | 2.0V | M[12:10]=%101 |

### Dithered DAC Modes

| Mode | Constant | Resolution | Sample Period |
|------|----------|------------|---------------|
| PRNG Dither | P_DAC_DITHER_RND (%00010) | 16-bit | Any ≥1 |
| PWM Dither | P_DAC_DITHER_PWM (%00011) | 16-bit | Multiple of 256 |

### Voltage Formulas

```
8-bit:  V = (DAC_value / 256) × V_full_scale
16-bit: V = (DAC_value / 65536) × V_full_scale

DAC_value = (V_target / V_full_scale) × resolution
```

### Reset State (DIR=0)

All DAC modes:
- IN = low
- Y[15:0] = captured (ready for DIR=1)
- Output = low (0V)

---

*This chapter covered DAC analog output. For serial transmission modes, see Chapter 11. For input modes, see Part III.*
