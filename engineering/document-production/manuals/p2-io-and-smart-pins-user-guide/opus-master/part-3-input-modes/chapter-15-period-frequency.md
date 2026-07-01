# Chapter 15: Period and Frequency Measurement {#ch15}

This chapter covers smart pin modes for measuring signal periods and calculating frequency. Two approaches are available: measuring over a fixed number of periods, or measuring over a fixed time window. Used together, these modes enable precise frequency and duty cycle determination.


## 15.1 Measurement Philosophy

### Which Chapter and Mode?

Several smart-pin modes across Chapters 13–15 measure time-domain signal properties. Use this map to pick the right starting point:

| You want to measure… | Recommended mode(s) | Where |
|----------------------|---------------------|-------|
| Pulse width / high or low duration | P_HIGH_TICKS, P_STATE_TICKS | Ch13 |
| Time between events / timeout | P_EVENTS_TICKS | Ch13 |
| Edge or event count | P_COUNT_RISES (and other counting modes) | Ch14 |
| Period (precise, frequency range known) | P_PERIODS_TICKS | Ch15 §15.2 |
| Frequency (unknown or variable) | P_COUNTER_PERIODS | Ch15 §15.3 |
| Duty cycle | P_PERIODS_HIGHS + P_PERIODS_TICKS (or the time-window pair) | Ch15 §15.2/§15.4 |

### Two Approaches to Period Measurement

| Approach | Modes | Method | Best For |
|----------|-------|--------|----------|
| Period-based | %10011, %10100 | Count time or states over X periods | Known frequency range, precise period measurement |
| Time-based | %10101-%10111 | Count time, states, or periods in X clock window | Unknown frequency, consistent update rate |

### Why Multiple Concurrent Measurements?

The silicon documentation states: "At least two of these measurements must be made concurrently to get useful results."

For frequency calculation:
```formula
frequency = periods / time
```

For duty cycle calculation:
```formula
duty_cycle = high_time / total_time
```

A single measurement provides either a count or a time, but calculating frequency or duty requires both.

> **Compute these ratios with `MULDIV64`, not `*` and `/`.** Frequency and duty combine large values: `periods * sysclk` overflows a 32-bit long for any real signal — 100 periods times 200 MHz is already 20 billion, past the 4.29-billion limit — so a plain `(periods * sysclk) / time` silently returns a wrong number. Spin2's `MULDIV64(a, b, divisor)` forms the `a * b` product in a 64-bit intermediate, then divides, so the result stays exact. Every frequency and duty calculation in this chapter uses it; so should yours.

### Trigger Sensitivity

All period measurement modes use Y[1:0] to select A/B input trigger combinations:

| Y[1:0] | Trigger | Description |
|--------|---------|-------------|
| %00 | A-rise to B-rise | Standard period: rising edge to rising edge |
| %01 | A-rise to B-edge | A rising to any B transition |
| %10 | A-edge to B-rise | Any A transition to B rising |
| %11 | A-edge to B-edge | Any transition to any transition (maximum sensitivity) |

**Note:** The B-input reads the same pin as the A-input *by default* (when no `P_PLUSn_B` / `P_MINUSn_B` routing modifier is applied) — exactly what single-pin cycle measurement needs. No special constant is required.


## 15.2 Period-Based Modes (Measure X Periods)

### Mode %10011: P_PERIODS_TICKS

**Purpose:** Measure total time for X complete signal periods.

**Operation:**

1. Configure X register with number of periods to measure
2. Smart pin counts clock cycles from first trigger to completion of X periods
3. IN flag raised when measurement complete
4. RDPIN returns total clock cycles

**Registers:**

| Register | Function |
|----------|----------|
| X | Number of periods to measure |
| Y[1:0] | Trigger sensitivity |
| Z | Total clock cycles for X periods |

**Configuration:**
```spin2
' Measure time for 100 periods
PINSTART(pin, P_PERIODS_TICKS, 100, %00)
```

**Period Calculation:**
```formula
period_clocks = RDPIN(pin)                    ' Total for X periods
single_period = period_clocks / X             ' Average period
frequency = sysclk / single_period            ' In Hz
```

### Mode %10100: P_PERIODS_HIGHS

**Purpose:** Measure total high-state time across X periods.

**Operation:**

1. Configure X register with number of periods to measure
2. Smart pin accumulates clock cycles when A-input is HIGH
3. IN flag raised when X periods complete
4. RDPIN returns total high-time clock cycles

**Registers:**

| Register | Function |
|----------|----------|
| X | Number of periods to measure |
| Y[1:0] | Trigger sensitivity |
| Z | Total clock cycles A was HIGH across X periods (max $80000000) |

**Configuration:**
```spin2
' Measure high time across 100 periods
PINSTART(pin, P_PERIODS_HIGHS, 100, %00)
```

**Duty Cycle with Both Modes:**
```spin2
CON
  _clkfreq = 200_000_000
  SIG_PIN = 20
  PERIODS = 100

PUB measure_duty() | total_time, high_time, duty_percent
  ' Start both measurements
  PINSTART(SIG_PIN, P_PERIODS_TICKS, PERIODS, %00)
  PINSTART(SIG_PIN+1, P_PERIODS_HIGHS, PERIODS, %00)

  ' Wait for completion
  REPEAT UNTIL PINREAD(SIG_PIN)

  total_time := RDPIN(SIG_PIN)                ' Total period time
  high_time := RDPIN(SIG_PIN+1)               ' Total high time

  duty_percent := MULDIV64(high_time, 100, total_time)
  DEBUG("Duty cycle: ", UDEC_(duty_percent), "%")
```

The loop waits on only `SIG_PIN`, yet reads both pins. That is safe because both smart pins watch the same signal for the same number of periods, so they finish on the same edge — once SIG_PIN's IN flag rises, SIG_PIN+1's result is already latched and ready to read.


## 15.3 Time-Based Modes (Measure in X Clocks)

### Mode %10101: P_COUNTER_TICKS

**Purpose:** Measure total period time within a minimum X-clock window.

**Operation:**

1. Configure X register with minimum measurement window (clock cycles)
2. Smart pin measures until X clocks elapse AND current period completes
3. Accumulates total period time (clock cycles)
4. IN flag raised when measurement complete

**Registers:**

| Register | Function |
|----------|----------|
| X | Minimum measurement window (clock cycles) |
| Y[1:0] | Trigger sensitivity |
| Z | Total clock cycles for all periods within window |

**Key Difference from %10011:**

- %10011: "Measure time for exactly X periods"
- %10101: "Measure time for all periods within X clocks"

Because the window stretches to the end of the period already in progress, **Z reports the *actual* elapsed clocks — always ≥ X, never exactly X.** Use Z, not the nominal X, as the time term in your math. That is also what makes concurrent measurement exact: run %10101, %10110, and %10111 together on the same signal with the same X, and because all three close on the same period-aligned window, frequency (`periods / Z`) and duty (`high / Z`) stay mutually consistent (see §15.4).

**Configuration:**
```spin2
' Measure periods within 100ms window
window_clocks := _clkfreq / 10                ' 100ms
PINSTART(pin, P_COUNTER_TICKS, window_clocks, %00)
```

### Mode %10110: P_COUNTER_HIGHS

**Purpose:** Measure total high-state time within a minimum X-clock window.

**Operation:**

1. Configure X register with minimum measurement window
2. Smart pin accumulates clock cycles when A-input is HIGH
3. Measurement continues until X clocks AND period completion
4. IN flag raised, RDPIN returns accumulated high time

**Registers:**

| Register | Function |
|----------|----------|
| X | Minimum measurement window (clock cycles) |
| Y[1:0] | Trigger sensitivity |
| Z | Total clock cycles A was HIGH within window |

**Configuration:**
```spin2
' Measure high time within 1-second window
PINSTART(pin, P_COUNTER_HIGHS, _clkfreq, %00)
```

### Mode %10111: P_COUNTER_PERIODS

**Purpose:** Count complete periods within a minimum X-clock window.

**Operation:**

1. Configure X register with minimum measurement window
2. Smart pin counts complete periods
3. Measurement continues until X clocks AND period completion
4. IN flag raised, RDPIN returns period count

**Registers:**

| Register | Function |
|----------|----------|
| X | Minimum measurement window (clock cycles) |
| Y[1:0] | Trigger sensitivity |
| Z | Number of complete periods (max $80000000) |

**Configuration:**
```spin2
' Count periods in 1-second window
PINSTART(pin, P_COUNTER_PERIODS, _clkfreq, %00)
```

**Frequency Calculation:**
```spin2
REPEAT UNTIL PINREAD(pin)
period_count := RDPIN(pin)
' For 1-second window, period_count = frequency in Hz
frequency := period_count
```

### Restart and Acknowledge

These modes restart automatically: a new measurement begins on the next trigger after the window completes, so you do not re-arm them by hand. How you *read* the result decides whether the IN flag is cleared:

- **RDPIN** reads Z **and acknowledges** — it clears IN, so the next completed window can raise it again. Use RDPIN as your once-per-window read.
- **RQPIN** reads Z **quietly** — it does *not* clear IN. Use it to peek mid-stream without disturbing the IN-driven cadence; the matching RDPIN still does the acknowledge.

Reading with RDPIN each time IN rises gives you exactly one fresh result per window, in lock-step with the hardware.


## 15.4 Combined Measurements

### Frequency and Duty Cycle Measurement

Using three pins simultaneously for complete signal characterization:

```spin2
CON
  _clkfreq = 200_000_000
  PIN_TIME = 20                               ' Measures total time
  PIN_HIGH = 21                               ' Measures high time
  PIN_PERIODS = 22                            ' Counts periods
  WINDOW_MS = 100                             ' 100ms measurement window

PUB measure_signal() | window, time_clks, high_clks, periods, freq, duty
  window := (_clkfreq / 1000) * WINDOW_MS

  ' Configure all three measurements
  PINSTART(PIN_TIME, P_COUNTER_TICKS, window, %00)
  PINSTART(PIN_HIGH, P_COUNTER_HIGHS, window, %00)
  PINSTART(PIN_PERIODS, P_COUNTER_PERIODS, window, %00)

  REPEAT
    ' Wait for all measurements to complete
    REPEAT UNTIL PINREAD(PIN_TIME) AND PINREAD(PIN_HIGH) ...
                 AND PINREAD(PIN_PERIODS)

    time_clks := RDPIN(PIN_TIME)              ' Actual measurement time
    high_clks := RDPIN(PIN_HIGH)              ' Total high time
    periods := RDPIN(PIN_PERIODS)             ' Period count

    ' Calculate frequency: periods / time
    freq := MULDIV64(periods, _clkfreq, time_clks)

    ' Calculate duty: high_time / total_time
    duty := MULDIV64(high_clks, 100, time_clks)

    DEBUG("Frequency: ", UDEC_(freq), " Hz")
    DEBUG("Duty cycle: ", UDEC_(duty), "%")
    DEBUG("Periods: ", UDEC_(periods))
    DEBUG("---")
```

> **All three cells must watch the same signal.** Each `PINSTART` above measures the pin you name, so the signal has to reach `PIN_TIME`, `PIN_HIGH`, and `PIN_PERIODS`. Rather than wiring it to three pins, leave it on one and aim the other two cells at that pin with A-input routing: `P_MINUS1_A` and `P_MINUS2_A` make a cell read the pin one or two below it — so with the signal on `PIN_TIME`, start `PIN_HIGH` with `P_COUNTER_HIGHS | P_MINUS1_A` and `PIN_PERIODS` with `P_COUNTER_PERIODS | P_MINUS2_A`. A cell watching a neighbor does not consume that pin; the observed pin stays free for its own use. (Without this, a signal on only one pin leaves the other two cells' IN flags low and the `REPEAT UNTIL` never exits.)

### Why Three Measurements?

The actual measurement time extends beyond X clocks to complete the final period. Using P_COUNTER_TICKS provides the **actual** measurement duration, enabling precise calculations:

```formula
actual_frequency = MULDIV64(periods, sysclk, time_clks)
actual_duty = MULDIV64(high_clks, 100, time_clks)   ' percent
```

Without knowing the actual elapsed time, calculations would have error due to the period completion extension.


## 15.5 PASM2 Implementation

### Period Measurement

```pasm2
CON
  _clkfreq = 200_000_000
  SIG_PIN = 20
  PERIODS_TO_MEASURE = 1000

DAT           org

              ' Configure period measurement
              dirl      #SIG_PIN                ' Reset smart pin
              wrpin     ##P_PERIODS_TICKS, #SIG_PIN
              wxpin     ##PERIODS_TO_MEASURE, #SIG_PIN
              wypin     #%00, #SIG_PIN          ' Rise to rise
              dirh      #SIG_PIN                ' Start measurement

.wait_done
              testp     #SIG_PIN wc             ' Check IN flag
        if_nc jmp       #.wait_done             ' Wait for completion

              rdpin     total_time, #SIG_PIN    ' Get total clock cycles

              ' Calculate single period time
              mov       period_time, total_time
              qdiv      period_time, ##PERIODS_TO_MEASURE
              getqx     period_time            ' Average period in clocks

              ' Calculate frequency: sysclk / period
              mov       freq, ##_clkfreq
              qdiv      freq, period_time
              getqx     freq                    ' Frequency in Hz

              jmp       #.wait_done             ' Continuous measurement

total_time    res       1
period_time   res       1
freq          res       1
```

### Time-Window Frequency Counter

```pasm2
CON
  _clkfreq = 200_000_000
  SIG_PIN = 20

DAT           org

              ' Configure 1-second window period counter
              dirl      #SIG_PIN
              wrpin     ##P_COUNTER_PERIODS, #SIG_PIN
              wxpin     ##_clkfreq, #SIG_PIN    ' 1-second window
              wypin     #%00, #SIG_PIN
              dirh      #SIG_PIN

.measure_loop
              testp     #SIG_PIN wc
        if_nc jmp       #.measure_loop

              rdpin     frequency, #SIG_PIN     ' periods/sec = Hz

              ' frequency now contains Hz value
              ' Process or display...

              jmp       #.measure_loop

frequency     res       1
```


## 15.6 Application Examples

### Example 1: Simple Frequency Counter

```spin2
CON
  _clkfreq = 200_000_000
  INPUT_PIN = 20
  GATE_TIME_MS = 1000                         ' 1 second gate

PUB frequency_counter() | freq
  ' Count periods in 1-second window
  PINSTART(INPUT_PIN, P_COUNTER_PERIODS, _clkfreq, %00)

  DEBUG("Frequency Counter - 1 second gate")

  REPEAT
    REPEAT UNTIL PINREAD(INPUT_PIN)
    freq := RDPIN(INPUT_PIN)
    DEBUG("Frequency: ", UDEC_(freq), " Hz")
```

### Example 2: RPM Measurement

```spin2
CON
  _clkfreq = 200_000_000
  TACH_PIN = 20
  PULSES_PER_REV = 2                          ' 2 magnets on wheel

PUB measure_rpm() | periods, rpm, window
  ' 100ms measurement window
  window := _clkfreq / 10
  PINSTART(TACH_PIN, P_COUNTER_PERIODS, window, %00)

  REPEAT
    REPEAT UNTIL PINREAD(TACH_PIN)
    periods := RDPIN(TACH_PIN)

    ' Convert to RPM
    ' periods in 100ms = periods * 10 per second
    ' RPM = (periods * 10 * 60) / PULSES_PER_REV
    rpm := (periods * 600) / PULSES_PER_REV

    DEBUG("RPM: ", UDEC_(rpm))
```

### Example 3: PWM Analyzer

```spin2
CON
  _clkfreq = 200_000_000
  PWM_PIN = 20
  NUM_PERIODS = 50                            ' Average over 50 periods

PUB pwm_analyzer() | total_time, high_time, freq, duty, period_ns
  ' Use period-based measurement for PWM analysis
  PINSTART(PWM_PIN, P_PERIODS_TICKS, NUM_PERIODS, %00)
  PINSTART(PWM_PIN+1, P_PERIODS_HIGHS, NUM_PERIODS, %00)

  DEBUG("PWM Analyzer - averaging ", UDEC_(NUM_PERIODS), " periods")

  REPEAT
    REPEAT UNTIL PINREAD(PWM_PIN)

    total_time := RDPIN(PWM_PIN)
    high_time := RDPIN(PWM_PIN+1)

    ' Calculate frequency
    freq := MULDIV64(NUM_PERIODS, _clkfreq, total_time)

    ' Calculate duty cycle
    duty := MULDIV64(high_time, 1000, total_time) ' 0.1% resolution

    ' Calculate period in nanoseconds
    period_ns := MULDIV64(total_time, 1000, ...
                 NUM_PERIODS * (_clkfreq / 1_000_000))

    DEBUG("Frequency: ", UDEC_(freq), " Hz")
    DEBUG("Duty cycle: ", UDEC_(duty/10), ".", UDEC_(duty//10), "%")
    DEBUG("Period: ", UDEC_(period_ns), " ns")
    DEBUG("---")
```

### Example 4: Precision Oscillator Calibration

```{.spin2 caption="ch15-oscillator-calibration.spin2"}
CON
  _clkfreq = 200_000_000
  REF_PIN = 20                                ' Reference signal input
  TARGET_FREQ = 10_000_000                    ' 10 MHz target

PUB oscillator_calibration() | measured, error_ppm, periods
  ' Use many periods for high precision
  periods := 10000
  PINSTART(REF_PIN, P_PERIODS_TICKS, periods, %00)

  DEBUG("Oscillator Calibration")
  DEBUG("Target: ", UDEC_(TARGET_FREQ), " Hz")

  REPEAT
    REPEAT UNTIL PINREAD(REF_PIN)

    measured := RDPIN(REF_PIN)

    ' Expected clocks for TARGET_FREQ over periods cycles
    ' expected = periods * (sysclk / TARGET_FREQ)
    ' error_ppm = ((measured - expected) * 1_000_000) / expected

    ' Simplified: calculate measured frequency
    measured := MULDIV64(periods, _clkfreq, measured)

    ' Calculate error in ppm
    if measured >= TARGET_FREQ
      error_ppm := ((measured - TARGET_FREQ) * 1_000_000) / TARGET_FREQ
      DEBUG("Measured: ", UDEC_(measured), ...
            " Hz (+", UDEC_(error_ppm), " ppm)")
    else
      error_ppm := ((TARGET_FREQ - measured) * 1_000_000) / TARGET_FREQ
      DEBUG("Measured: ", UDEC_(measured), ...
            " Hz (-", UDEC_(error_ppm), " ppm)")
```


## 15.7 Precision Considerations

### Measurement Resolution

| Mode | Resolution | Accuracy |
|------|------------|----------|
| P_PERIODS_TICKS | 1 clock cycle | ±1 clock per period |
| P_COUNTER_PERIODS | 1 period | ±1 period per window |

**Improving Precision:**

- Increase measurement periods (X) for period-based modes
- Increase time window for time-based modes
- Use higher sysclk frequency

### Error Sources

| Source | Effect | Mitigation |
|--------|--------|------------|
| Quantization | ±1 clock cycle | Measure more periods |
| Trigger jitter | Random error | Use Schmitt trigger input |
| Clock accuracy | Systematic error | Use calibrated crystal |
| Period variation | Averaged out | Measure multiple periods |

### Gate Time vs Resolution

| Gate Time | Resolution at 1 kHz | Resolution at 1 MHz |
|-----------|---------------------|---------------------|
| 10 ms | 10 Hz (1%) | 10 kHz (1%) |
| 100 ms | 1 Hz (0.1%) | 1 kHz (0.1%) |
| 1 second | 0.1 Hz (0.01%) | 100 Hz (0.01%) |


## 15.8 Mode Selection Guide

### Choose P_PERIODS_TICKS (%10011) When:

- Signal frequency is approximately known
- Precise period measurement needed
- Consistent number of samples required
- Measuring periodic signals (clocks, PWM)

### Choose P_PERIODS_HIGHS (%10100) When:

- Duty cycle measurement needed
- Averaging duty over multiple periods
- Signal quality analysis required

### Choose P_COUNTER_PERIODS (%10111) When:

- Frequency is unknown or variable
- Need consistent update rate
- Simple frequency counting application
- RPM or event rate measurement

### Choose P_COUNTER_TICKS (%10101) When:

- Need actual measurement duration
- Combining with P_COUNTER_PERIODS for precision
- Time-windowed period analysis

### Choose P_COUNTER_HIGHS (%10110) When:

- Duty cycle in time window needed
- Combining with other time-window modes
- Variable frequency duty analysis


## 15.9 Quick Reference

### Mode Constants

| Mode | Constant | Description |
|------|----------|-------------|
| %10011 | P_PERIODS_TICKS | For X periods, count clock cycles |
| %10100 | P_PERIODS_HIGHS | For X periods, count A-high cycles |
| %10101 | P_COUNTER_TICKS | In X clocks, count period time |
| %10110 | P_COUNTER_HIGHS | In X clocks, count A-high time |
| %10111 | P_COUNTER_PERIODS | In X clocks, count periods |

### Trigger Sensitivity (Y[1:0])

| Value | Trigger |
|-------|---------|
| %00 | A-rise to B-rise |
| %01 | A-rise to B-edge |
| %10 | A-edge to B-rise |
| %11 | A-edge to B-edge |

### Common Modifiers

| Modifier | Function |
|----------|----------|
| (default) | B reads the same pin as A — single-pin measurement |
| P_PLUS1_B | Use next pin as B-input |
| P_MINUS1_B | Use previous pin as B-input |
| P_FILT1_AB | Add input filtering |

### Frequency Formulas

**From period measurement (P_PERIODS_TICKS):**
```formula
frequency = MULDIV64(num_periods, sysclk, rdpin_value)
```

**From period count (P_COUNTER_PERIODS):**
```formula
frequency = MULDIV64(rdpin_value, sysclk, window_clocks)
' Or for 1-second window:
frequency = rdpin_value  ' Direct Hz reading
```

### Duty Cycle Formulas

**From period-based modes:**
```formula
duty_percent = MULDIV64(high_time, 100, total_time)
```
Where:

- high_time = RDPIN from P_PERIODS_HIGHS
- total_time = RDPIN from P_PERIODS_TICKS


*This chapter covered period and frequency measurement modes. For ADC input, see Chapter 16. For serial reception, see Chapter 17.*
