# Chapter 14: Counting Modes {#ch14}

This chapter covers Smart Pin counting modes: **P_REG_UP** (%01100) for gated edge counting, **P_REG_UP_DOWN** (%01101) for accumulator up/down, **P_COUNT_RISES** (%01110) for edge counting with direction, **P_COUNT_HIGHS** (%01111) for high-time counting, and **P_QUADRATURE** (%01011) for quadrature encoder decoding.


## 14.1 Counting Mode Overview

### Available Counting Modes

| Mode | Constant | Function |
|------|----------|----------|
| %01011 | P_QUADRATURE | Quadrature encoder decoding |
| %01100 | P_REG_UP | Count A edges when B high (gated) |
| %01101 | P_REG_UP_DOWN | Accumulate A edges, B controls direction |
| %01110 | P_COUNT_RISES | Count edges with optional up/down |
| %01111 | P_COUNT_HIGHS | Count clocks while input high |

### Common Features

All counting modes share these characteristics:

- 32-bit counter range
- Continuous or periodic measurement
- X register controls measurement period
- Z register holds count value
- IN flag indicates period completion

### Continuous vs Periodic Mode

**Continuous (X=0):**

- Counter runs indefinitely
- Read current value anytime with RDPIN/RQPIN
- No IN flag generation
- Suitable for position tracking

**Periodic (X>0):**

- Counts for X clock cycles
- Result placed in Z at period end
- IN flag raised at each period
- Counter continues with residual value
- Suitable for rate/velocity measurement


## 14.2 P_QUADRATURE Mode (%01011)

### Function

P_QUADRATURE decodes standard quadrature encoder signals (A/B phase with 90° offset). The counter increments or decrements based on rotation direction, providing position tracking with 4× resolution.

### Quadrature Signal Pattern

```{=latex}
\DiagQuadrature
```

### Configuration

| Register | Purpose |
|----------|---------|
| X | Period (0=continuous, >0=periodic) |
| Y | Not used |
| Z | Quadrature step count (signed 32-bit) |

### Position Tracking (Continuous Mode)

**Spin2:**
```spin2
CON
  _clkfreq = 200_000_000
  ENC_A = 20                               ' Encoder A signal
  ENC_B = 21                             ' Encoder B signal (must be A+1)

PUB encoder_init()
  ' Configure quadrature decoder (uses A and B inputs)
  PINFLOAT(ENC_A)
  WRPIN(ENC_A, P_QUADRATURE | P_PLUS1_B)   ' B from adjacent pin
  WXPIN(ENC_A, 0)                          ' Continuous mode
  PINLOW(ENC_A)

PUB read_position() : position
  position := RDPIN(ENC_A)                 ' Signed 32-bit position

PUB zero_position()
  PINFLOAT(ENC_A)                          ' Pulse DIR low
  PINLOW(ENC_A)                            ' Re-enable
```

**PASM2:**
```pasm2
              dirl      #ENC_A
              wrpin     ##P_QUADRATURE | P_PLUS1_B, #ENC_A
              wxpin     #0, #ENC_A          ' Continuous
              dirh      #ENC_A

.read         rdpin     position, #ENC_A    ' Get position
```

### Velocity Measurement (Periodic Mode)

```spin2
CON
  _clkfreq = 200_000_000
  ENC_A = 20
  PERIOD_MS = 100                          ' 100ms measurement

PUB encoder_velocity_init() | period_clocks
  period_clocks := (_clkfreq / 1000) * PERIOD_MS

  PINFLOAT(ENC_A)
  WRPIN(ENC_A, P_QUADRATURE | P_PLUS1_B)
  WXPIN(ENC_A, period_clocks)              ' Periodic mode
  PINLOW(ENC_A)

PUB read_velocity() : steps_per_period
  repeat until PINREAD(ENC_A)              ' Wait for period
  steps_per_period := RDPIN(ENC_A)         ' Signed value
```

### Dual Encoder Setup

Use two smart pins for position and velocity simultaneously:

```spin2
CON
  _clkfreq = 200_000_000
  POS_PIN = 20                             ' Position tracking
  VEL_PIN = 22                             ' Velocity measurement

PUB dual_encoder_init()
  ' Position on pin 20 (continuous)
  WRPIN(POS_PIN, P_QUADRATURE | P_PLUS1_B)
  WXPIN(POS_PIN, 0)
  PINLOW(POS_PIN)

  ' Velocity on pin 22 (periodic, same encoder signals)
  WRPIN(VEL_PIN, P_QUADRATURE | P_MINUS1_B)
  WXPIN(VEL_PIN, _clkfreq / 10)            ' 100ms period
  PINLOW(VEL_PIN)
```


## 14.3 P_REG_UP Mode (%01100)

### Function

P_REG_UP counts positive edges on A-input, but only when B-input is high. This provides gated counting for frequency measurement and event counting with enable control.

### Operation

```{=latex}
\DiagGatedCount
```

### Configuration

| Register | Purpose |
|----------|---------|
| X | Period (0=continuous, >0=periodic) |
| Y | Not used |
| Z | Edge count |

### Gated Frequency Counter

```spin2
CON
  _clkfreq = 200_000_000
  SIGNAL_PIN = 20
  GATE_PIN = 21
  GATE_TIME_MS = 1000                      ' 1 second gate

PUB frequency_counter() : freq_hz | period_clocks
  period_clocks := (_clkfreq / 1000) * GATE_TIME_MS

  ' Configure gated counter
  PINFLOAT(SIGNAL_PIN)
  WRPIN(SIGNAL_PIN, P_REG_UP | P_PLUS1_B)
  WXPIN(SIGNAL_PIN, period_clocks)
  PINLOW(SIGNAL_PIN)

  ' Gate is controlled by B-input (pin 21)
  ' For hardware gate: connect gate signal to pin 21
  ' For software gate: drive pin 21 high to enable counting

  PINHIGH(GATE_PIN)                        ' Enable counting

  repeat until PINREAD(SIGNAL_PIN)         ' Wait for period
  freq_hz := RDPIN(SIGNAL_PIN)             ' Edges in gate period
```

### Software-Controlled Gate

```spin2
PUB gated_count_between(enable_pin, signal_pin) : count
  ' Count events while enable_pin is high
  PINFLOAT(signal_pin)
  WRPIN(signal_pin, P_REG_UP | P_PLUS1_B)
  WXPIN(signal_pin, 0)                     ' Continuous
  PINLOW(signal_pin)

  PINHIGH(enable_pin)                      ' Start counting
  WAITMS(1000)                             ' Count for 1 second
  PINLOW(enable_pin)                       ' Stop counting

  count := RDPIN(signal_pin)
```


## 14.4 P_REG_UP_DOWN Mode (%01101)

### Function

P_REG_UP_DOWN accumulates A-input positive edges with direction controlled by B-input. When B is high, edges increment the counter. When B is low, edges decrement the counter.

### Operation

```{=latex}
\DiagUpDownCount
```

### Configuration

| Register | Purpose |
|----------|---------|
| X | Period (0=continuous, >0=periodic) |
| Y | Not used |
| Z | Signed count (increments/decrements) |

### Up/Down Counter

```spin2
CON
  COUNT_PIN = 20
  DIR_PIN = 21                             ' High=up, Low=down

PUB updown_counter_init()
  PINFLOAT(COUNT_PIN)
  WRPIN(COUNT_PIN, P_REG_UP_DOWN | P_PLUS1_B)
  WXPIN(COUNT_PIN, 0)                      ' Continuous
  PINLOW(COUNT_PIN)

PUB read_count() : value
  value := RDPIN(COUNT_PIN)                ' Signed result

PUB count_up()
  PINHIGH(DIR_PIN)                         ' Next edges increment

PUB count_down()
  PINLOW(DIR_PIN)                          ' Next edges decrement
```


## 14.5 P_COUNT_RISES Mode (%01110)

### Function

P_COUNT_RISES has two sub-modes controlled by Y[0]:

- Y[0]=0: Count A-input positive edges only
- Y[0]=1: Increment on A-input edge, decrement on B-input edge

### Single-Input Mode (Y[0]=0)

Simple edge counter on A-input:

```spin2
CON
  PULSE_PIN = 20

PUB edge_counter_init()
  PINFLOAT(PULSE_PIN)
  WRPIN(PULSE_PIN, P_COUNT_RISES)
  WXPIN(PULSE_PIN, 0)                      ' Continuous
  WYPIN(PULSE_PIN, 0)                      ' Y[0]=0: A edges only
  PINLOW(PULSE_PIN)

PUB read_edge_count() : count
  count := RDPIN(PULSE_PIN)
```

### Dual-Input Mode (Y[0]=1)

Independent up/down on two signals:

```spin2
CON
  UP_PIN = 20                              ' A-input
  DOWN_PIN = 21                            ' B-input

PUB dual_counter_init()
  PINFLOAT(UP_PIN)
  WRPIN(UP_PIN, P_COUNT_RISES | P_PLUS1_B)
  WXPIN(UP_PIN, 0)                         ' Continuous
  WYPIN(UP_PIN, 1)                         ' Y[0]=1: A up, B down
  PINLOW(UP_PIN)

PUB read_net_count() : value
  value := RDPIN(UP_PIN)                   ' Net difference
```

### Periodic Rate Measurement

```spin2
CON
  _clkfreq = 200_000_000
  EVENT_PIN = 20
  PERIOD_MS = 100

PUB event_rate() : events_per_period | period
  period := (_clkfreq / 1000) * PERIOD_MS

  PINFLOAT(EVENT_PIN)
  WRPIN(EVENT_PIN, P_COUNT_RISES)
  WXPIN(EVENT_PIN, period)
  WYPIN(EVENT_PIN, 0)
  PINLOW(EVENT_PIN)

  repeat until PINREAD(EVENT_PIN)
  events_per_period := RDPIN(EVENT_PIN)
```


## 14.6 P_COUNT_HIGHS Mode (%01111)

### Function

P_COUNT_HIGHS counts system clock cycles while input is in a particular state. Two sub-modes controlled by Y[0]:

- Y[0]=0: Count clocks while A-input high
- Y[0]=1: Increment clocks while A high, decrement while B high

### Duty Cycle Integration

```spin2
CON
  _clkfreq = 200_000_000
  PWM_PIN = 20
  PERIOD_MS = 100

PUB measure_duty_cycle() : duty_percent | high_clocks, period_clocks
  period_clocks := (_clkfreq / 1000) * PERIOD_MS

  PINFLOAT(PWM_PIN)
  WRPIN(PWM_PIN, P_COUNT_HIGHS)
  WXPIN(PWM_PIN, period_clocks)
  WYPIN(PWM_PIN, 0)                        ' Count A-high clocks
  PINLOW(PWM_PIN)

  repeat until PINREAD(PWM_PIN)
  high_clocks := RDPIN(PWM_PIN)

  duty_percent := (high_clocks * 100) / period_clocks
```

### Differential High-Time

Using Y[0]=1 for differential measurement:

```spin2
CON
  _clkfreq = 200_000_000
  SIGNAL_A = 20
  SIGNAL_B = 21

PUB differential_high_time() : net_clocks | period
  period := _clkfreq / 10                  ' 100ms

  PINFLOAT(SIGNAL_A)
  WRPIN(SIGNAL_A, P_COUNT_HIGHS | P_PLUS1_B)
  WXPIN(SIGNAL_A, period)
  WYPIN(SIGNAL_A, 1)                       ' A increments, B decrements
  PINLOW(SIGNAL_A)

  repeat until PINREAD(SIGNAL_A)
  net_clocks := RDPIN(SIGNAL_A)            ' Signed difference
```


## 14.7 Input Signal Routing

### Adjacent Pin Selection

For modes using two inputs (A and B):

| Constant | B-Input Source |
|----------|---------------|
| P_LOCAL_B | Same pin (default) |
| P_PLUS1_B | Pin + 1 |
| P_MINUS1_B | Pin - 1 |
| P_PLUS2_B | Pin + 2 |
| P_MINUS2_B | Pin - 2 |
| P_PLUS3_B | Pin + 3 |
| P_MINUS3_B | Pin - 3 |

### Input Conditioning

Add conditioning for reliable counting:

```spin2
' Schmitt trigger for noisy signals
WRPIN(pin, P_COUNT_RISES | P_SCHMITT_A)

' Filter to reduce glitches
WRPIN(pin, P_QUADRATURE | P_FILT1_AB | P_PLUS1_B)

' Invert input polarity
WRPIN(pin, P_REG_UP | P_INVERT_A)
```


## 14.8 Counter Overflow and Range

### 32-Bit Counter Range

All counting modes use 32-bit counters:

- Unsigned modes: 0 to 4,294,967,295
- Signed modes: -2,147,483,648 to +2,147,483,647

### Overflow Behavior

Counters wrap on overflow:

```formula
Unsigned: $FFFFFFFF + 1 → $00000000
Signed:   $7FFFFFFF + 1 → $80000000
```

### Detecting Overflow

For high-count applications:

```spin2
VAR
  long total_count
  long last_reading

PUB update_extended_count() | current, delta
  current := RDPIN(COUNT_PIN)
  delta := current - last_reading          ' Handles wrap
  total_count += delta
  last_reading := current
```


## 14.9 Mode Selection Guide

### Choosing the Right Mode

| Application | Mode | Configuration |
|-------------|------|---------------|
| Rotary encoder | P_QUADRATURE | X=0 for position |
| Frequency counter | P_REG_UP | X=gate_period |
| Event counter | P_COUNT_RISES | X=0, Y=0 |
| Up/down buttons | P_COUNT_RISES | X=0, Y=1 |
| Step/direction motor | P_REG_UP_DOWN | X=0 |
| PWM duty cycle | P_COUNT_HIGHS | X=period, Y=0 |
| Differential time | P_COUNT_HIGHS | X=period, Y=1 |


## 14.10 Complete Examples

### Example 1: Frequency Counter

```spin2
CON
  _clkfreq = 200_000_000
  FREQ_PIN = 20
  GATE_MS = 1000

PUB frequency_counter() : freq | period, count
  period := (_clkfreq / 1000) * GATE_MS

  PINFLOAT(FREQ_PIN)
  WRPIN(FREQ_PIN, P_COUNT_RISES | P_SCHMITT_A)
  WXPIN(FREQ_PIN, period)
  WYPIN(FREQ_PIN, 0)
  PINLOW(FREQ_PIN)

  repeat
    repeat until PINREAD(FREQ_PIN)
    count := RDPIN(FREQ_PIN)
    freq := count * (1000 / GATE_MS)       ' Scale to Hz

    DEBUG("Frequency: ", UDEC_(freq), " Hz")
```

### Example 2: Motor Position Control

```spin2
CON
  _clkfreq = 200_000_000
  ENC_A = 20
  ENC_B = 21
  MOTOR_PWM = 30

VAR
  long target_position
  long current_position

PUB motor_control()
  ' Initialize encoder
  WRPIN(ENC_A, P_QUADRATURE | P_PLUS1_B | P_SCHMITT_A)
  WXPIN(ENC_A, 0)
  PINLOW(ENC_A)

  target_position := 0

  repeat
    current_position := RDPIN(ENC_A)
    adjust_motor(target_position - current_position)
    WAITMS(10)

PUB goto_position(pos)
  target_position := pos

PRI adjust_motor(error)
  ' Simple proportional control
  if error > 10
    motor_forward()
  elseif error < -10
    motor_reverse()
  else
    motor_stop()

PRI motor_forward()
  ' Application-specific: drive PWM/H-bridge high for forward direction
  PINH(MOTOR_PWM)

PRI motor_reverse()
  ' Application-specific: drive PWM/H-bridge for reverse direction
  PINL(MOTOR_PWM)

PRI motor_stop()
  ' Application-specific: stop motor (PWM=0 or coast)
  PINL(MOTOR_PWM)
```

### Example 3: PASM2 Event Counter

```pasm2
CON
  _clkfreq = 200_000_000

DAT           org

' Initialize edge counter
              dirl      #EVENT_PIN
              wrpin     ##P_COUNT_RISES, #EVENT_PIN
              wxpin     #0, #EVENT_PIN      ' Continuous
              wypin     #0, #EVENT_PIN      ' A edges only
              dirh      #EVENT_PIN

' Count loop
count_loop
              rdpin     count, #EVENT_PIN   ' Read current count
              wrlong    count, #count_hub   ' Store for main cog

              waitx     ##200_000           ' 1ms update rate
              jmp       #count_loop

EVENT_PIN     long      20
count         long      0
count_hub     long      0
```

### Example 4: RPM Measurement

```spin2
CON
  _clkfreq = 200_000_000
  TACH_PIN = 20
  PULSES_PER_REV = 1                       ' Hall sensor
  SAMPLE_MS = 100

PUB measure_rpm() : rpm | period, pulses
  period := (_clkfreq / 1000) * SAMPLE_MS

  PINFLOAT(TACH_PIN)
  WRPIN(TACH_PIN, P_COUNT_RISES | P_SCHMITT_A)
  WXPIN(TACH_PIN, period)
  WYPIN(TACH_PIN, 0)
  PINLOW(TACH_PIN)

  repeat
    repeat until PINREAD(TACH_PIN)
    pulses := RDPIN(TACH_PIN)

    ' RPM = (pulses / pulses_per_rev) * (60000 / sample_ms)
    rpm := (pulses * 60000) / (PULSES_PER_REV * SAMPLE_MS)

    DEBUG("RPM: ", UDEC_(rpm))
```


## 14.11 Quick Reference

### Mode Summary

| Mode | Binary | A-Input | B-Input | Output |
|------|--------|---------|---------|--------|
| P_QUADRATURE | %01011 | Phase A | Phase B | Position |
| P_REG_UP | %01100 | Events | Gate | Gated count |
| P_REG_UP_DOWN | %01101 | Events | Direction | Up/down count |
| P_COUNT_RISES | %01110 | Up events | Down events* | Net count |
| P_COUNT_HIGHS | %01111 | Time high | Time high* | Clock count |

*When Y[0]=1

### Common Configurations

```spin2
' Continuous position tracking
WXPIN(pin, 0)                              ' X=0 for continuous

' 100ms periodic measurement at 200 MHz
WXPIN(pin, 20_000_000)                     ' X = sysclk/10

' 1 second gate at 200 MHz
WXPIN(pin, 200_000_000)                    ' X = sysclk
```

### B-Input Routing

| Need | Configuration |
|------|---------------|
| B on pin+1 | `mode` \| `P_PLUS1_B` |
| B on pin-1 | `mode` \| `P_MINUS1_B` |
| Invert B | `mode` \| `P_INVERT_B` |

### Reset Behavior

All counting modes when DIR=0:

- IN = low
- Z = initial adder value: 0 or +1 for unidirectional counters; bidirectional modes (quadrature, up/down) can also load -1, accounting for any edge coincident with reset
- Counter ready to start on DIR=1


*This chapter covered counting modes. For period measurement modes, see Chapter 15. For quadrature encoder details, see the P_QUADRATURE section above.*
