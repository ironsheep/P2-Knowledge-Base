# Chapter 13: Timing Measurement {#ch13}

This chapter covers smart pin modes for measuring time intervals: **P_STATE_TICKS** (%10000) for timing both high and low states, **P_HIGH_TICKS** (%10001) for timing high states only, and **P_EVENTS_TICKS** (%10010) for event timing and timeout detection.


## 13.1 Timing Measurement Overview

### P2 Timing Capabilities

The P2 smart pin timing modes provide hardware-based time measurement with clock-cycle resolution. All measurements are in system clock cycles.

| Mode | Function | Trigger |
|------|----------|---------|
| P_STATE_TICKS | Both high and low durations | Every transition |
| P_HIGH_TICKS | High state duration only | High-to-low transition |
| P_EVENTS_TICKS | Time N events or timeout | Event count or timeout |

### Resolution and Range

At 200 MHz sysclk:

- Resolution: 5 ns (1 clock cycle)
- Maximum measurement: $80000000 clocks = 10.74 seconds
- Overflow behavior: Z saturates at $80000000

### Common Applications

- PWM duty cycle analysis
- Pulse width measurement
- Frequency measurement
- Protocol timing verification
- Timeout/watchdog monitoring


## 13.2 P_STATE_TICKS Mode (%10000)

### Function

P_STATE_TICKS continuously measures the duration of each logic state (both high and low). On every transition, the previous state's duration is captured in Z and the state type is stored in the C flag.

### Operation

```{=latex}
\DiagPulseWidthMeas
```

### Configuration

| Register | Purpose |
|----------|---------|
| X | Not used |
| Y | Not used |
| Z | Duration of previous state (clocks) |
| C flag | Previous state (1=was high, 0=was low) |
| IN flag | Raised on every transition |

On reset (DIR=0), IN is low and **Z is preloaded to $0000_0001, not 0**. Software that reads Z before the first transition therefore gets 1, never a zero — which keeps a naive `period / Z` calculation from dividing by zero on the first window.

### Reading Measurements

**Spin2:**
```spin2
CON
  _clkfreq = 200_000_000
  INPUT_PIN = 20

PUB measure_states() | duration, was_high
  PINFLOAT(INPUT_PIN)
  WRPIN(INPUT_PIN, P_STATE_TICKS)
  PINLOW(INPUT_PIN)                        ' Enable

  repeat
    repeat until PINREAD(INPUT_PIN)        ' Wait for transition
    duration := RDPIN(INPUT_PIN)

    ' Check C flag (bit 31 of RDPIN result indicates C)
    was_high := (duration >> 31) & 1
    duration &= $7FFFFFFF                  ' Mask off C flag

    if was_high
      DEBUG("High time: ", UDEC_(duration), " clocks")
    else
      DEBUG("Low time: ", UDEC_(duration), " clocks")
```

**PASM2:**
```pasm2
              dirl      #INPUT_PIN
              wrpin     ##P_STATE_TICKS, #INPUT_PIN
              dirh      #INPUT_PIN

.loop         testp     #INPUT_PIN wc       ' Wait for IN flag
        if_nc jmp       #.loop

              rdpin     duration, #INPUT_PIN wc  ' Read duration, C=state
        if_c  mov       high_time, duration
        if_nc mov       low_time, duration

              jmp       #.loop
```

### PWM Analysis Example

```spin2
CON
  _clkfreq = 200_000_000
  PWM_PIN = 20

VAR
  long high_time, low_time

PUB analyze_pwm() : frequency, duty_percent
  PINFLOAT(PWM_PIN)
  WRPIN(PWM_PIN, P_STATE_TICKS | P_SCHMITT_A)
  PINLOW(PWM_PIN)

  ' Get one complete cycle
  repeat 2
    repeat until PINREAD(PWM_PIN)
    if RDPIN(PWM_PIN) & $8000_0000         ' C flag = was high
      high_time := RDPIN(PWM_PIN) & $7FFF_FFFF
    else
      low_time := RDPIN(PWM_PIN) & $7FFF_FFFF

  ' Calculate results
  frequency := _clkfreq / (high_time + low_time)
  duty_percent := (high_time * 100) / (high_time + low_time)
```


## 13.3 P_HIGH_TICKS Mode (%10001)

### Function

P_HIGH_TICKS measures only the duration of high states. On each high-to-low transition, the high time is captured in Z and IN is raised. Low periods are ignored.

### Operation

```{=latex}
\DiagHighTicksMeas
```

### Configuration

| Register | Purpose |
|----------|---------|
| X | Not used |
| Y | Not used |
| Z | Duration of previous high state (clocks) |
| IN flag | Raised on high-to-low transition |

On reset (DIR=0), IN is low and **Z is preloaded to $0000_0001, not 0** — the same divide-by-zero-safe initial value as the other timing modes. (Z also saturates at $8000_0000; bit 31 doubles as the overflow indicator, which is why the read examples mask with `$7FFF_FFFF`.)

### Pulse Width Measurement

**Spin2:**
```spin2
CON
  _clkfreq = 200_000_000
  PULSE_PIN = 20

PUB measure_pulse_width() : width_us | clocks
  PINFLOAT(PULSE_PIN)
  WRPIN(PULSE_PIN, P_HIGH_TICKS)
  PINLOW(PULSE_PIN)

  ' Wait for pulse to complete
  repeat until PINREAD(PULSE_PIN)

  clocks := RDPIN(PULSE_PIN) & $7FFF_FFFF
  width_us := clocks / (_clkfreq / 1_000_000)
```

**PASM2:**
```pasm2
              dirl      #PULSE_PIN
              wrpin     ##P_HIGH_TICKS, #PULSE_PIN
              dirh      #PULSE_PIN

.wait         testp     #PULSE_PIN wc
        if_nc jmp       #.wait

              rdpin     pulse_width, #PULSE_PIN
              and       pulse_width, ##$7FFFFFFF
```

### Servo Pulse Measurement

Hobby servos use 1-2ms pulses at 50 Hz:

```spin2
CON
  _clkfreq = 200_000_000
  SERVO_PIN = 20

PUB read_servo_pulse() : position_us | clocks
  PINFLOAT(SERVO_PIN)
  WRPIN(SERVO_PIN, P_HIGH_TICKS | P_SCHMITT_A)
  PINLOW(SERVO_PIN)

  repeat until PINREAD(SERVO_PIN)

  clocks := RDPIN(SERVO_PIN) & $7FFF_FFFF
  position_us := clocks / (_clkfreq / 1_000_000)

  ' Expected range: 1000-2000 µs
  ' 1000 µs = 0°, 1500 µs = 90°, 2000 µs = 180°
```

### Measuring Low Periods

Use P_INVERT_A to measure low periods instead:

```spin2
' Measure low time by inverting input
WRPIN(pin, P_HIGH_TICKS | P_INVERT_A)
```


## 13.4 P_EVENTS_TICKS Mode (%10010)

### Function

P_EVENTS_TICKS operates in two modes controlled by Y[2]:

- **Event timing (Y[2]=0)**: Measures time for X events to occur
- **Timeout detection (Y[2]=1)**: Detects when no event occurs within X clocks

On reset (DIR=0), IN is low and **Z is preloaded to $0000_0001, not 0** in both sub-modes — the same divide-by-zero-safe initial value used by the other timing modes.

### Event Type Selection

Y[1:0] selects what constitutes an event:

| Y[1:0] | Event Type |
|--------|------------|
| %00 | A-input high (level) |
| %01 | A-input rising edge |
| %1x | A-input any edge |

### Event Timing Mode (Y[2]=0)

Measures time until X events occur:

**Spin2:**
```spin2
CON
  _clkfreq = 200_000_000
  FREQ_PIN = 20

PUB measure_frequency() : freq_hz | clocks, events
  events := 100                            ' Count 100 edges

  PINFLOAT(FREQ_PIN)
  WRPIN(FREQ_PIN, P_EVENTS_TICKS)
  WXPIN(FREQ_PIN, events)                  ' X = event count
  WYPIN(FREQ_PIN, %01)                     ' Y[1:0] = rising edge, Y[2]=0
  PINLOW(FREQ_PIN)

  repeat until PINREAD(FREQ_PIN)           ' Wait for N events

  clocks := RDPIN(FREQ_PIN) & $7FFF_FFFF
  freq_hz := (_clkfreq * events) / clocks
```

**PASM2:**
```pasm2
              dirl      #FREQ_PIN
              wrpin     ##P_EVENTS_TICKS, #FREQ_PIN
              wxpin     #100, #FREQ_PIN     ' 100 events
              wypin     #%01, #FREQ_PIN     ' Rising edges
              dirh      #FREQ_PIN

.wait         testp     #FREQ_PIN wc
        if_nc jmp       #.wait

              rdpin     period, #FREQ_PIN
              and       period, ##$7FFFFFFF

              ' frequency = (sysclk * 100) / period
```

### Timeout Detection Mode (Y[2]=1)

Detects missing events (communication watchdog):

**Spin2:**
```spin2
CON
  _clkfreq = 200_000_000
  COMM_PIN = 20
  TIMEOUT_MS = 100                         ' 100ms timeout

PUB comm_watchdog() | timeout_clocks, elapsed
  timeout_clocks := (_clkfreq / 1000) * TIMEOUT_MS

  PINFLOAT(COMM_PIN)
  WRPIN(COMM_PIN, P_EVENTS_TICKS)
  WXPIN(COMM_PIN, timeout_clocks)          ' X = timeout clocks
  WYPIN(COMM_PIN, %101)              ' Y[2]=1 (timeout), Y[1:0]=01 (rise)
  PINLOW(COMM_PIN)

  repeat
    if PINREAD(COMM_PIN)                   ' IN flag = timeout occurred
      elapsed := RDPIN(COMM_PIN) & $7FFF_FFFF
      DEBUG("Comm timeout! ", UDEC_(elapsed), " clocks since last")
      handle_timeout()

    WAITMS(10)                             ' Check periodically

PUB handle_timeout()
  ' Application-specific timeout response —
  ' flash an LED, reset peripheral, etc.
```

**PASM2:**
```pasm2
              dirl      #COMM_PIN
              wrpin     ##P_EVENTS_TICKS, #COMM_PIN
              wxpin     ##20_000_000, #COMM_PIN   ' 100ms at 200MHz
              wypin     #%101, #COMM_PIN    ' Timeout on missing edge
              dirh      #COMM_PIN

.monitor      testp     #COMM_PIN wc        ' Check for timeout
        if_c  call      #timeout_handler
              jmp       #.monitor

timeout_handler
              rdpin     elapsed, #COMM_PIN  ' Clocks since last edge
              ret
```

### Continuous vs Retriggering

In timeout mode:

- Event resets timer and Z to 1
- Timeout raises IN and restarts timer
- Z always contains clocks since last event

In event-timing mode (Y[2]=0), reading the result with `RDPIN`/`RQPIN` acknowledges the measurement and **auto-restarts** it — the next read returns the interval to the following event. No explicit re-arm is needed for back-to-back measurements.


## 13.5 Input Signal Routing

### Using Adjacent Pin Inputs

For signals on adjacent pins, use input routing constants:

| Constant | Source |
|----------|--------|
| P_PLUS1_A | Pin + 1 |
| P_MINUS1_A | Pin - 1 |
| P_PLUS2_A | Pin + 2 |
| P_MINUS2_A | Pin - 2 |
| P_PLUS3_A | Pin + 3 |
| P_MINUS3_A | Pin - 3 |

**Example:**
```spin2
' Measure signal on pin 21 using smart pin on pin 20
WRPIN(20, P_HIGH_TICKS | P_PLUS1_A)
```

### Input Conditioning for Timing

Always use input conditioning for reliable timing:

```spin2
' Add Schmitt trigger for clean edges
WRPIN(pin, P_STATE_TICKS | P_SCHMITT_A)

' Add filtering for noisy signals
WRPIN(pin, P_HIGH_TICKS | P_FILT1_AB)
```


## 13.6 Accuracy Analysis

### Measurement Resolution

| sysclk | Resolution | Max Measurable |
|--------|------------|----------------|
| 100 MHz | 10 ns | 21.47 s |
| 180 MHz | 5.56 ns | 11.93 s |
| 250 MHz | 4 ns | 8.59 s |
| 350 MHz | 2.86 ns | 6.14 s |

### Error Sources

**Quantization error:**

- ±1 clock cycle inherent uncertainty
- Relative error decreases with longer measurements

**For frequency measurement:**
```formula
error = 1 / (events × measured_period)

Example: 100 edges, 10 kHz signal
period = 10,000 clocks per edge
total = 1,000,000 clocks
error = 1 / 1,000,000 = 0.0001% = 1 ppm
```

### Averaging for Accuracy

Measure multiple periods and average:

```spin2
PUB measure_frequency_averaged(events, samples) : freq | total, i
  total := 0
  repeat i from 0 to samples - 1
    total += measure_single(events)

  freq := (_clkfreq * events * samples) / total
```


## 13.7 Complete Examples

### Example 1: Complete PWM Analyzer

```spin2
CON
  _clkfreq = 200_000_000
  PWM_PIN = 20

VAR
  long frequency
  long duty_percent
  long high_us
  long low_us

PUB pwm_analyzer() | h_clocks, l_clocks, got_high, got_low
  PINFLOAT(PWM_PIN)
  WRPIN(PWM_PIN, P_STATE_TICKS | P_SCHMITT_A)
  PINLOW(PWM_PIN)

  got_high := false
  got_low := false

  ' Capture one complete cycle
  repeat until got_high AND got_low
    repeat until PINREAD(PWM_PIN)

    if RDPIN(PWM_PIN) & $8000_0000
      h_clocks := RDPIN(PWM_PIN) & $7FFF_FFFF
      got_high := true
    else
      l_clocks := RDPIN(PWM_PIN) & $7FFF_FFFF
      got_low := true

  ' Calculate results
  frequency := _clkfreq / (h_clocks + l_clocks)
  duty_percent := (h_clocks * 100) / (h_clocks + l_clocks)
  high_us := h_clocks / (_clkfreq / 1_000_000)
  low_us := l_clocks / (_clkfreq / 1_000_000)

  DEBUG("Frequency: ", UDEC_(frequency), " Hz")
  DEBUG("Duty: ", UDEC_(duty_percent), "%")
  DEBUG("High: ", UDEC_(high_us), " µs")
  DEBUG("Low: ", UDEC_(low_us), " µs")
```

### Example 2: Ultrasonic Distance Measurement

```spin2
CON
  _clkfreq = 200_000_000
  TRIG_PIN = 20
  ECHO_PIN = 21

PUB measure_distance_cm() : distance | echo_us
  ' Configure echo pin for pulse timing
  PINFLOAT(ECHO_PIN)
  WRPIN(ECHO_PIN, P_HIGH_TICKS | P_SCHMITT_A)
  PINLOW(ECHO_PIN)

  ' Send 10µs trigger pulse
  PINHIGH(TRIG_PIN)
  WAITUS(10)
  PINLOW(TRIG_PIN)

  ' Wait for echo pulse to complete
  repeat until PINREAD(ECHO_PIN)

  echo_us := (RDPIN(ECHO_PIN) & $7FFF_FFFF) / (_clkfreq / 1_000_000)

  ' Distance = (echo_time / 2) / 29.1 µs/cm
  distance := echo_us / 58
```

### Example 3: PASM2 High-Speed Frequency Counter

```pasm2
CON
  _clkfreq = 200_000_000

DAT           org

' Initialize frequency measurement
              dirl      #FREQ_PIN
              wrpin     ##P_EVENTS_TICKS, #FREQ_PIN
              wxpin     ##1000, #FREQ_PIN   ' 1000 edges
              wypin     #%11, #FREQ_PIN     ' Any edge
              dirh      #FREQ_PIN

' Measure loop
freq_loop
.wait         testp     #FREQ_PIN wc
        if_nc jmp       #.wait

              rdpin     period, #FREQ_PIN
              and       period, ##$7FFFFFFF

              ' Calculate frequency = (sysclk * 1000) / period
              ' Store for main cog to read
              wrlong    period, #period_hub

              ' Auto-restarts on read
              jmp       #freq_loop

FREQ_PIN      long      20
period        long      0
period_hub    long      0
```

### Example 4: Communication Watchdog

```spin2
CON
  _clkfreq = 200_000_000
  RX_PIN = 63
  TIMEOUT_MS = 500

VAR
  long comm_ok
  long last_timeout

PUB comm_monitor() | timeout_clocks
  timeout_clocks := (_clkfreq / 1000) * TIMEOUT_MS

  PINFLOAT(RX_PIN)
  WRPIN(RX_PIN, P_EVENTS_TICKS | P_SCHMITT_A)
  WXPIN(RX_PIN, timeout_clocks)
  WYPIN(RX_PIN, %111)                      ' Timeout on any edge
  PINLOW(RX_PIN)

  comm_ok := true

  repeat
    if PINREAD(RX_PIN)                     ' Timeout occurred
      comm_ok := false
      last_timeout := GETMS()
      DEBUG("Communication lost!")
    elseif NOT comm_ok
      comm_ok := true
      DEBUG("Communication restored")

    WAITMS(50)
```


## 13.8 Quick Reference

### Timing Mode Summary

| Mode | Constant | Measures | Trigger |
|------|----------|----------|---------|
| %10000 | P_STATE_TICKS | High and low times | Every edge |
| %10001 | P_HIGH_TICKS | High time only | High→low |
| %10010 | P_EVENTS_TICKS | N events or timeout | Configurable |

### P_EVENTS_TICKS Y Register

| Y Value | Mode | Event Type |
|---------|------|------------|
| %000 | Time events | High level |
| %001 | Time events | Rising edge |
| %01x | Time events | Any edge |
| %100 | Timeout | High level |
| %101 | Timeout | Rising edge |
| %11x | Timeout | Any edge |

### Time Calculations

```formula
frequency = sysclk / period_clocks
period_us = clocks / (sysclk / 1,000,000)
period_ms = clocks / (sysclk / 1,000)
duty_percent = high_clocks * 100 / (high_clocks + low_clocks)
```

### Common Input Modifiers

| Constant | Effect |
|----------|--------|
| P_SCHMITT_A | Schmitt trigger input |
| P_INVERT_A | Invert input polarity |
| P_FILT1_AB | Add input filtering |
| P_PLUS1_A | Input from pin+1 |

### Limits

- Maximum measurement: $80000000 clocks
- At 200 MHz: 10.74 seconds
- Overflow behavior: Saturates at max value


*This chapter covered timing measurement modes. For counting modes, see Chapter 14. For period measurement with more options, see Chapter 15.*
