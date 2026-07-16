# Chapter 9: PWM Output {#ch9}

This chapter covers the three Pulse Width Modulation (PWM) modes: **P_PWM_TRIANGLE** (%01000) for symmetric triangle-wave PWM, **P_PWM_SAWTOOTH** (%01001) for asymmetric sawtooth-wave PWM, and **P_PWM_SMPS** (%01010) for switch-mode power supply control with feedback.


## 9.1 PWM Fundamentals

### What is PWM?

Pulse Width Modulation controls the average power delivered to a load by varying the duty cycle of a digital signal. The duty cycle is the percentage of time the signal is high during each period.

### P2 PWM Architecture

All three PWM modes share a common architecture:

```{=latex}
\DiagPwmArch
```

### Key Terminology

| Term | Definition |
|------|------------|
| **Base period** | X[15:0] clock cycles between counter updates |
| **Frame period** | X[31:16] base periods forming one counter cycle |
| **PWM period** | Time for complete PWM cycle (depends on mode) |
| **Duty value** | Y[15:0] comparison threshold |

### Mode Comparison

| Mode | Counter Pattern | PWM Period | Best For |
|------|-----------------|------------|----------|
| P_PWM_TRIANGLE | Up-down | 2 × frame period | Smooth transitions |
| P_PWM_SAWTOOTH | Up only | 1 × frame period | Fast switching |
| P_PWM_SMPS | Up with feedback | Variable | Power supply |

### Complementary Outputs and Dead-Band

Each Smart Pin drives **one** physical pin, so a single PWM Smart Pin produces **one** output. There is no single-pin "complementary output" mode and no built-in dead-band. A complementary pair — for example the high-side and low-side gates of a half-bridge — is **always two Smart Pins**, one per side, enabled together and coordinated carefully.

The two pins share one frame period; the low-side pin inverts its output (`P_INVERT_OUTPUT`) so the pair switches complementarily. The **dead-band** — the brief interval where *both* outputs are off, which prevents shoot-through in a half-bridge — is produced in **software**, by offsetting the two duty values so their active intervals never overlap:

```spin2
' Two Smart Pins per half-bridge: high side true, low side inverted
WRPIN(pin_pwm_h, P_PWM_SAWTOOTH | P_OE)                   ' high side
WRPIN(pin_pwm_l, P_PWM_SAWTOOTH | P_OE | P_INVERT_OUTPUT) ' low side
' Same frame period on both; enable both together, then:
high_duty := base_duty - dead_gap   ' high side switches on later
low_duty  := base_duty + dead_gap   ' low side switches off earlier
```

There is no dead-band-width register: the width is whatever timing offset you feed the two pins, and the right value depends on the switches and the load.

## 9.2 P_PWM_TRIANGLE Mode (%01000)

### Function

P_PWM_TRIANGLE generates a symmetric PWM waveform using an up-down counter. The counter counts from the frame period value down to 1, then from 1 back up to the frame period value, creating a triangle wave pattern.

### Counter Behavior

```layout
Frame = 4

Counter:  4 → 3 → 2 → 1     (count down)
          1 → 2 → 3 → 4     (count up)
          → repeat

PWM Period = 2 × Frame Period × Base Period
```

### Output Logic

At each base period:

- If Y[15:0] >= counter → output HIGH
- If Y[15:0] < counter → output LOW

### Configuration

| Register | Field | Purpose |
|----------|-------|---------|
| X[15:0] | Base period | Clock cycles per counter update (1-65536; 0 selects 65536) |
| X[31:16] | Frame period | Counter range (1-65536; a field value of 0 selects 65536) |
| Y[15:0] | Duty value | 0 (always low) to frame period (always high) |

### Timing Formulas

```formula
PWM frequency = sysclk / (2 × X[31:16] × X[15:0])

PWM period = 2 × X[31:16] × X[15:0] / sysclk

Duty cycle = Y[15:0] / X[31:16] × 100%
```

### Worked Example

**1 kHz triangle PWM at 50% duty with 200 MHz sysclk:**

```formula
Target: 1 kHz PWM, 50% duty
PWM period = 1/1000 = 1 ms = 200,000 clocks

Frame must fit the 16-bit X[31:16] field (max 65,535). The
period needs frame × base = 100,000, so split it across the two:

Choose: Base period = 2, Frame period = 50,000
  → PWM period = 2 × 50,000 × 2 = 200,000 clocks ✓

Duty = 50% = 25,000 / 50,000
  → Y = 25,000
```

### Configuration Sequence

**Spin2:**
```spin2
CON
  _clkfreq = 200_000_000
  PWM_PIN = 20

PUB triangle_pwm(freq_hz, duty_percent) | base, frame, y_val
  ' PWM period (clocks) = 2 * frame * base; frame must fit the 16-bit field
  frame := _clkfreq / (2 * freq_hz)    ' = frame * base (base starts at 1)
  base  := 1
  repeat while frame > $FFFF           ' grow base until frame fits 16 bits
    base += 1
    frame := _clkfreq / (2 * freq_hz * base)
  y_val := frame * duty_percent / 100

  PINFLOAT(PWM_PIN)
  WRPIN(PWM_PIN, P_PWM_TRIANGLE | P_OE)
  WXPIN(PWM_PIN, base | (frame << 16)) ' Base period, frame period
  WYPIN(PWM_PIN, y_val)
  PINLOW(PWM_PIN)
```

**PASM2:**
```pasm2
              dirl      #PWM_PIN
              wrpin     ##(P_PWM_TRIANGLE | P_OE), #PWM_PIN
              wxpin     x_val, #PWM_PIN
              dirh      #PWM_PIN
              wypin     y_val, #PWM_PIN
```

### Duty Cycle Waveform

For frame period = 8, duty value = 6:

```{=latex}
\DiagPwmTriangle
```

The symmetric counting creates equal rise and fall times.


## 9.3 P_PWM_SAWTOOTH Mode (%01001)

### Function

P_PWM_SAWTOOTH generates an asymmetric PWM waveform using an up-only counter. The counter counts from 1 up to the frame period value, then resets to 1.

### Counter Behavior

```layout
Frame = 4

Counter:  1 → 2 → 3 → 4     (count up)
          1 → 2 → 3 → 4     (count up, repeat)

PWM Period = Frame Period × Base Period
```

### Key Difference from Triangle

| Aspect | P_PWM_TRIANGLE | P_PWM_SAWTOOTH |
|--------|----------------|----------------|
| Counter pattern | Up-down | Up only |
| PWM period | 2 × frame × base | 1 × frame × base |
| Frequency at same X | Half | Full |
| Edges per cycle | 2 symmetric | 2 asymmetric |

### Configuration

| Register | Field | Purpose |
|----------|-------|---------|
| X[15:0] | Base period | Clock cycles per counter update |
| X[31:16] | Frame period | Counter range (1-65536; a field value of 0 selects 65536) |
| Y[15:0] | Duty value | 0 (always low) to frame period (always high) |

### Timing Formulas

```formula
PWM frequency = sysclk / (X[31:16] × X[15:0])

PWM period = X[31:16] × X[15:0] / sysclk

Duty cycle = Y[15:0] / X[31:16] × 100%
```

### Worked Example

**10 kHz sawtooth PWM at 25% duty with 200 MHz sysclk:**

```formula
Target: 10 kHz PWM, 25% duty
PWM period = 1/10,000 = 100 µs = 20,000 clocks

Choose: Base period = 1, Frame period = 20,000
  → PWM period = 20,000 × 1 = 20,000 clocks ✓

Duty = 25% = 5,000 / 20,000
  → Y = 5,000
```

### Configuration Sequence

**Spin2:**
```spin2
CON
  _clkfreq = 200_000_000
  PWM_PIN = 20

PUB sawtooth_pwm(freq_hz, duty_percent) | base, frame, y_val
  ' PWM period (clocks) = frame * base; frame must fit the 16-bit field
  frame := _clkfreq / freq_hz          ' = frame * base (base starts at 1)
  base  := 1
  repeat while frame > $FFFF           ' grow base until frame fits 16 bits
    base += 1
    frame := _clkfreq / (freq_hz * base)
  y_val := frame * duty_percent / 100

  PINFLOAT(PWM_PIN)
  WRPIN(PWM_PIN, P_PWM_SAWTOOTH | P_OE)
  WXPIN(PWM_PIN, base | (frame << 16))
  WYPIN(PWM_PIN, y_val)
  PINLOW(PWM_PIN)
```

**PASM2:**
```pasm2
              dirl      #PWM_PIN
              wrpin     ##(P_PWM_SAWTOOTH | P_OE), #PWM_PIN
              wxpin     x_val, #PWM_PIN
              dirh      #PWM_PIN
              wypin     y_val, #PWM_PIN
```

### Duty Cycle Waveform

For frame period = 8, duty value = 3:

```{=latex}
\DiagPwmSawtooth
```

The pin output is a rectangular PWM pulse with sharp digital edges in both directions. The "sawtooth" name refers to the internal counter, which ramps slowly from 1 up to the frame period and then resets quickly to 1.


## 9.4 P_PWM_SMPS Mode (%01010)

### Function

P_PWM_SMPS generates PWM output for switch-mode power supply control with voltage and current feedback. This mode extends sawtooth PWM with two feedback inputs that control cycle initiation and output cutoff.

### Feedback Inputs

| Input | Function | Source |
|-------|----------|--------|
| A-input | Voltage feedback | Low = start new cycle |
| B-input | Current limit | High = immediate output low |

### Operation Sequence

1. Counter runs sawtooth pattern (1 to frame period)
2. At frame end, wait for A-input to go low (voltage sag)
3. When A goes low, start new cycle, capture Y, raise IN
4. During cycle, if B-input goes high, force output low for remainder

The **IN flag rising marks the cycle boundary** — the instant a fresh Y is captured for the new cycle. That makes IN the synchronization cue for software: wait on (or poll) IN before writing the next duty value with WYPIN, and the update lands cleanly on the upcoming cycle instead of mid-pulse.

### Block Diagram

```{=latex}
\DiagSmpsBlock
```

### Configuration

| Register | Field | Purpose |
|----------|-------|---------|
| X[15:0] | Base period | Clock cycles per counter update |
| X[31:16] | Frame period | Maximum PWM pulse width |
| Y[15:0] | Duty value | PWM threshold (can be set once) |

### Input Selection

Use mode field bits to select A and B input sources:

| Constant | Effect |
|----------|--------|
| P_PLUS1_A | A-input from pin+1 |
| P_MINUS1_A | A-input from pin-1 |
| P_PLUS1_B | B-input from pin+1 |
| P_MINUS1_B | B-input from pin-1 |

### Typical SMPS Circuit

```{=latex}
\DiagSmpsCircuit
```

### Configuration Sequence

**Spin2:**
```spin2
CON
  _clkfreq = 200_000_000
  SMPS_PIN = 20       ' FET gate
  V_SENSE = 21        ' Voltage feedback (A-input)
  I_SENSE = 19        ' Current sense (B-input)

PUB smps_controller(duty_percent, voltage_threshold, current_limit) ...
    | mode, frame, y_val
  ' Configure voltage comparator
  WRPIN(V_SENSE, P_COMPARE_AB)
  WXPIN(V_SENSE, voltage_threshold)
  PINH(V_SENSE)

  ' Configure current comparator
  WRPIN(I_SENSE, P_COMPARE_AB)
  WXPIN(I_SENSE, current_limit)
  PINH(I_SENSE)

  ' Configure SMPS controller
  frame := 256                              ' 256 steps
  y_val := frame * duty_percent / 100
  mode := P_PWM_SMPS | P_OE | P_PLUS1_A | P_MINUS1_B

  PINFLOAT(SMPS_PIN)
  WRPIN(SMPS_PIN, mode)
  WXPIN(SMPS_PIN, 25 | (frame << 16))       ' 25 clocks base
  WYPIN(SMPS_PIN, y_val)
  PINLOW(SMPS_PIN)
```

**PASM2:**
```pasm2
              dirl      #SMPS_PIN
              mov       smps_cfg, ##(P_PWM_SMPS | P_OE)
              or        smps_cfg, ##(P_PLUS1_A | P_MINUS1_B)
              wrpin     smps_cfg, #SMPS_PIN
              wxpin     x_val, #SMPS_PIN
              dirh      #SMPS_PIN
              wypin     y_val, #SMPS_PIN    ' Set once, runs autonomously
```

### Set-and-Forget Operation

P_PWM_SMPS is designed for autonomous operation. After initial configuration with WYPIN, the smart pin:

- Monitors voltage via A-input
- Initiates pulses when voltage sags
- Limits current via B-input
- Requires no software intervention


## 9.5 Dynamic Duty Cycle Updates

### Updating Y Register

Triangle and sawtooth PWM modes capture Y[15:0] at the start of each frame. (SMPS mode is event-driven: it captures Y[15:0] after the frame period completes *and* the A-input goes low — not at a fixed clock boundary.) To change duty cycle:

**Spin2:**
```spin2
WYPIN(PWM_PIN, new_duty_value)
```

**PASM2:**
```pasm2
              wypin     new_duty, #PWM_PIN
```

The new value takes effect at the next frame boundary, preventing glitches.

### Glitch-Free Updates

The Y capture mechanism ensures:

- Mid-cycle writes do not affect current cycle
- New duty applies at next frame start
- No partial pulses or timing artifacts

### Update Timing

For smooth transitions, update rate should be much slower than PWM frequency:

| Application | PWM Frequency | Update Rate |
|-------------|---------------|-------------|
| LED dimming | 500 Hz | 50-100 Hz |
| Motor control | 20 kHz | 1-5 kHz |
| Audio | 100 kHz | 44.1 kHz |


## 9.6 PWM Resolution and Frequency Tradeoffs

### Resolution vs Frequency

PWM resolution depends on frame period (X[31:16]):

| Frame Period | Resolution | Max Frequency, triangle (200 MHz) |
|--------------|------------|------------------------|
| 256 | 8-bit | 390.6 kHz |
| 512 | 9-bit | 195.3 kHz |
| 1024 | 10-bit | 97.7 kHz |
| 4096 | 12-bit | 24.4 kHz |
| 65535 | 16-bit | 1.5 kHz |

These are triangle-mode maxima (`sysclk / (2 * frame)`). Sawtooth uses the full frame as one period, so its maximum frequency is double each value.

### Choosing Parameters

**For motor control (20 kHz, triangle mode):**
```formula
Frame period = 200_000_000 / (2 × 20_000) = 5,000
  (triangle: period = 2 × frame × base)
Actual resolution = log2(5,000) ≈ 12.3 bits
Y range: 0 to 5,000
```

**For LED dimming (500 Hz, 12-bit resolution):**
```formula
Frame period = 200_000_000 / 500 = 400,000
Must limit to 65535 max, use base period
Base = 7, Frame = 57,143
Y range: 0 to 57,143
```


## 9.7 Worked Examples

### Example 1: LED Brightness Control

```{.spin2 caption="ch09-pwm-led-fade.spin2"}
CON
  _clkfreq = 200_000_000
  LED_PIN = 56
  PWM_FREQ = 500                            ' 500 Hz (no flicker)
  ' 500 Hz sawtooth: period = 200 MHz / 500 = 400,000 clocks. That exceeds the
  ' 16-bit frame field, so split it across base and frame: base x frame = period.
  BASE_PERIOD = 8
  FRAME_PERIOD = 50000                      ' 8 x 50,000 = 400,000 -> 500 Hz

PUB led_control() | brightness
  PINFLOAT(LED_PIN)
  WRPIN(LED_PIN, P_PWM_SAWTOOTH | P_OE)
  WXPIN(LED_PIN, BASE_PERIOD | (FRAME_PERIOD << 16))
  WYPIN(LED_PIN, 0)                         ' Start at 0%
  PINLOW(LED_PIN)

  ' Fade up
  repeat brightness from 0 to FRAME_PERIOD step FRAME_PERIOD/100
    WYPIN(LED_PIN, brightness)
    WAITMS(20)

  ' Fade down
  repeat brightness from FRAME_PERIOD to 0 step FRAME_PERIOD/100
    WYPIN(LED_PIN, brightness)
    WAITMS(20)
```

### Example 2: Servo Motor Control

Standard hobby servos expect 50 Hz PWM with 1-2 ms pulse width:

```spin2
CON
  _clkfreq = 200_000_000
  SERVO_PIN = 20

  ' 50 Hz PWM = 20 ms period = 4,000,000 clocks
  ' Use base=64 to fit in 16-bit frame
  BASE_PERIOD = 64
  FRAME_PERIOD = 62500                      ' 64 × 62500 = 4,000,000

  ' Servo pulse: 1 ms = 200,000 clocks = 3125 frame units
  '              2 ms = 400,000 clocks = 6250 frame units
  SERVO_MIN = 3125                          ' 0° position
  SERVO_MAX = 6250                          ' 180° position

PUB servo_control()
  PINFLOAT(SERVO_PIN)
  WRPIN(SERVO_PIN, P_PWM_SAWTOOTH | P_OE)
  WXPIN(SERVO_PIN, BASE_PERIOD | (FRAME_PERIOD << 16))
  WYPIN(SERVO_PIN, (SERVO_MIN + SERVO_MAX) / 2)  ' Center
  PINLOW(SERVO_PIN)

PUB set_servo_angle(degrees) | pulse
  ' Map 0-180° to SERVO_MIN-SERVO_MAX
  pulse := SERVO_MIN + (SERVO_MAX - SERVO_MIN) * degrees / 180
  WYPIN(SERVO_PIN, pulse)
```

### Example 3: Motor Speed Control with Acceleration

```spin2
CON
  _clkfreq = 200_000_000
  MOTOR_PIN = 16
  PWM_FREQ = 20_000                         ' 20 kHz (inaudible)

VAR
  long current_speed
  long target_speed
  long frame_period

PUB motor_init()
  frame_period := _clkfreq / (2 * PWM_FREQ) ' triangle period = 2 x frame

  PINFLOAT(MOTOR_PIN)
  WRPIN(MOTOR_PIN, P_PWM_TRIANGLE | P_OE)   ' Triangle for smooth drive
  WXPIN(MOTOR_PIN, 1 | (frame_period << 16))
  WYPIN(MOTOR_PIN, 0)
  PINLOW(MOTOR_PIN)

  current_speed := 0
  target_speed := 0

PUB set_motor_speed(percent)
  target_speed := frame_period * percent / 100

PUB motor_update() | delta
  ' Call periodically for acceleration control
  if current_speed < target_speed
    delta := (target_speed - current_speed) / 10 + 1
    current_speed += delta
  elseif current_speed > target_speed
    delta := (current_speed - target_speed) / 10 + 1
    current_speed -= delta

  WYPIN(MOTOR_PIN, current_speed)
```

### Example 4: PASM2 High-Frequency PWM

```pasm2
CON
  _clkfreq = 200_000_000
  PWM_PIN  = 20                    ' CON symbol → #PWM_PIN is the value 20

DAT           org

' 100 kHz PWM with ~11-bit resolution (log2(2000) ≈ 11)
              dirl      #PWM_PIN
              wrpin     ##(P_PWM_SAWTOOTH | P_OE), #PWM_PIN
              wxpin     ##$07D0_0001, #PWM_PIN      ' Frame=2000, Base=1
              dirh      #PWM_PIN
              wypin     ##1000, #PWM_PIN  ' 50% duty (1000 of 2000)

' Update duty in real-time
pwm_loop
              rdlong    new_duty, duty_ptr
              wypin     new_duty, #PWM_PIN
              waitx     delay
              jmp       #pwm_loop

duty_ptr      long      0                          ' Hub address for duty
new_duty      long      0
delay         long      20_000                      ' Update rate
```


## 9.8 Quick Reference

### P_PWM_TRIANGLE Configuration

| Parameter | Register | Formula |
|-----------|----------|---------|
| Base period | X[15:0] | Clock cycles per update |
| Frame period | X[31:16] | Counter range |
| Duty value | Y[15:0] | 0 to frame period |
| PWM frequency | - | sysclk / (2 × frame × base) |
| Duty cycle | - | Y / frame × 100% |

### P_PWM_SAWTOOTH Configuration

| Parameter | Register | Formula |
|-----------|----------|---------|
| Base period | X[15:0] | Clock cycles per update |
| Frame period | X[31:16] | Counter range |
| Duty value | Y[15:0] | 0 to frame period |
| PWM frequency | - | sysclk / (frame × base) |
| Duty cycle | - | Y / frame × 100% |

### P_PWM_SMPS Configuration

| Parameter | Register | Purpose |
|-----------|----------|---------|
| Base period | X[15:0] | Clock cycles per update |
| Frame period | X[31:16] | Maximum pulse width |
| Duty value | Y[15:0] | PWM threshold |
| A-input | Mode bits | Voltage feedback |
| B-input | Mode bits | Current limit |

### Mode Constants

| Constant | Value | Purpose |
|----------|-------|---------|
| P_PWM_TRIANGLE | %01000 | Symmetric PWM |
| P_PWM_SAWTOOTH | %01001 | Asymmetric PWM |
| P_PWM_SMPS | %01010 | SMPS with feedback |
| P_OE | - | Enable output |
| P_INVERT_OUTPUT | - | Invert PWM signal |
| P_PLUS1_A | - | A from pin+1 |
| P_MINUS1_A | - | A from pin-1 |
| P_PLUS1_B | - | B from pin+1 |
| P_MINUS1_B | - | B from pin-1 |

### Reset State (DIR=0)

All PWM modes:

- IN = low
- Output = low
- Y[15:0] = captured (ready for DIR=1)


*This chapter covered PWM output modes. For DAC-based analog output, see Chapter 10. For serial transmission modes, see Chapter 11.*
