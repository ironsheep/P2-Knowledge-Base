# Timing Operations Usage Guide

## Overview

The Propeller 2 provides timing operations based on a 32-bit system counter that increments every clock cycle. Spin2 offers both low-level counter access and convenient time-unit functions.

Timing operations:
- **Counter access** - GETCT for raw counter, POLLCT/WAITCT for events
- **Time delays** - WAITMS, WAITUS, WAITX for waiting
- **Time measurement** - GETMS, GETSEC for elapsed time since boot

The counter rolls over approximately every 21.5 seconds at 200 MHz (2^32 cycles / clock_frequency).

## Basic Usage

### Simple Delays

```spin2
PUB blink_led(pin)
  repeat
    pinhigh(pin)
    waitms(500)              ' Wait 500 milliseconds
    pinlow(pin)
    waitms(500)
```

### Measuring Elapsed Time

```spin2
PUB time_operation() | start, elapsed
  start := getms()
  perform_operation()
  elapsed := getms() - start
  debug("Operation took ", udec(elapsed), " ms")
```

### Precise Timing with Counter

```spin2
PUB precise_pulse(pin, width_us) | target
  target := getct() + (clkfreq / 1_000_000 * width_us)
  pinhigh(pin)
  waitct(target)
  pinlow(pin)
```

## Counter Operations

### GETCT - Get System Counter

```spin2
counter_value := GETCT()
```

Returns the current 32-bit system counter value. The counter increments every clock cycle.

```spin2
PUB measure_cycles() | start, stop, cycles
  start := getct()
  do_something()
  stop := getct()
  cycles := stop - start         ' Works even with rollover
```

### Counter Rollover

The 32-bit counter rolls over after 2^32 cycles:

| Clock Frequency | Rollover Period |
|-----------------|-----------------|
| 20 MHz | ~214.7 seconds |
| 100 MHz | ~42.9 seconds |
| 200 MHz | ~21.5 seconds |
| 300 MHz | ~14.3 seconds |

**Rollover-safe subtraction**: Subtracting two counter values gives correct elapsed cycles even if rollover occurred (as long as elapsed time < rollover period).

```spin2
PUB elapsed_ok() | start, stop, elapsed
  start := getct()
  waitms(100)
  stop := getct()
  elapsed := stop - start        ' Correct even if rollover happened
```

### WAITCT - Wait for Counter Value

```spin2
WAITCT(target_count)
```

Blocks until the system counter reaches or exceeds the target value.

```spin2
PUB precise_delay(cycles) | target
  target := getct() + cycles
  waitct(target)

PUB periodic_task() | next_time
  next_time := getct()
  repeat
    next_time += clkfreq / 100   ' 10ms interval
    do_work()
    waitct(next_time)            ' Wait until next period
```

### POLLCT - Poll Counter Event

```spin2
reached := POLLCT(target_count)
```

Non-blocking check if counter has reached target. Returns non-zero if target reached.

```spin2
PUB wait_with_work(target) | done
  done := FALSE
  repeat until done
    if pollct(target)
      done := TRUE
    else
      do_background_work()
```

## Time Unit Operations

### WAITMS - Wait Milliseconds

```spin2
WAITMS(milliseconds)
```

Blocks for the specified number of milliseconds. Uses CLKFREQ internally for accurate timing.

```spin2
waitms(1000)                     ' Wait 1 second
waitms(50)                       ' Wait 50 ms
```

### WAITUS - Wait Microseconds

```spin2
WAITUS(microseconds)
```

Blocks for the specified number of microseconds. Minimum resolution depends on clock frequency.

```spin2
waitus(100)                      ' Wait 100 microseconds
waitus(1)                        ' Wait 1 microsecond (if clock allows)
```

### WAITX - Wait Clock Cycles (PASM2)

In PASM2 code:

```pasm
WAITX   D/#n
```

Waits for the specified number of clock cycles. Available in PASM2 only.

```pasm
        waitx   #100             ' Wait 100 clock cycles
        waitx   delay_reg        ' Wait cycles from register
```

## Time Measurement

### GETMS - Get Milliseconds Since Boot

```spin2
ms := GETMS()
```

Returns milliseconds elapsed since program started.

```spin2
PUB timestamp_event() | now
  now := getms()
  debug("Event at ", udec(now), " ms")

PUB timeout_example() | deadline
  deadline := getms() + 5000     ' 5 second timeout
  repeat
    if check_condition()
      return TRUE
    if getms() >= deadline
      return FALSE               ' Timeout
    waitms(10)
```

### GETSEC - Get Seconds Since Boot

```spin2
sec := GETSEC()
```

Returns seconds elapsed since program started.

```spin2
PUB uptime() : seconds
  seconds := getsec()

PUB log_with_timestamp(message)
  debug("[", udec(getsec()), "s] ", zstr(message))
```

## Patterns

### Periodic Execution (Jitter-Free)

```spin2
PUB run_periodic(interval_ms) | period, next_tick
  period := clkfreq / 1000 * interval_ms
  next_tick := getct()

  repeat
    next_tick += period
    do_periodic_work()
    waitct(next_tick)            ' Maintains precise spacing
```

This pattern maintains precise intervals regardless of work duration (as long as work completes before next tick).

### Timeout with Polling

```spin2
PUB wait_for_response(timeout_ms) : success | deadline
  deadline := getms() + timeout_ms

  repeat
    if response_ready()
      return TRUE
    if getms() >= deadline
      return FALSE
    waitms(1)                    ' Small delay to avoid busy-waiting
```

### Debouncing

```spin2
CON
  DEBOUNCE_MS = 50

PUB read_button(pin) : pressed | sample1, sample2
  pinfloat(pin)
  sample1 := pinread(pin)
  waitms(DEBOUNCE_MS)
  sample2 := pinread(pin)
  pressed := (sample1 == sample2) AND (sample1 == 0)
```

### Pulse Width Measurement

```spin2
PUB measure_pulse_width(pin) : width_us | start, stop
  ' Wait for rising edge
  repeat while pinread(pin) == 1
  repeat while pinread(pin) == 0

  ' Measure high time
  start := getct()
  repeat while pinread(pin) == 1
  stop := getct()

  width_us := (stop - start) / (clkfreq / 1_000_000)
```

### Rate Limiting

```spin2
VAR
  long last_action_time

PUB rate_limited_action(min_interval_ms) : allowed
  if getms() - last_action_time >= min_interval_ms
    last_action_time := getms()
    allowed := TRUE
  else
    allowed := FALSE
```

### Precise PWM (Software)

```spin2
PUB soft_pwm(pin, duty_percent, freq_hz) | period, on_time, next_cycle
  period := clkfreq / freq_hz
  on_time := period * duty_percent / 100
  next_cycle := getct()

  repeat
    pinhigh(pin)
    waitct(next_cycle + on_time)
    pinlow(pin)
    next_cycle += period
    waitct(next_cycle)
```

### Multi-Timer Pattern

```spin2
VAR
  long timer_targets[4]
  long timer_active[4]

PUB start_timer(index, ms)
  timer_targets[index] := getms() + ms
  timer_active[index] := TRUE

PUB check_timer(index) : expired
  if timer_active[index]
    if getms() >= timer_targets[index]
      timer_active[index] := FALSE
      expired := TRUE

PUB process_timers() | i
  repeat i from 0 to 3
    if check_timer(i)
      handle_timer_expired(i)
```

## Clock Frequency Considerations

### Converting Time Units

```spin2
PUB ms_to_cycles(ms) : cycles
  cycles := clkfreq / 1000 * ms

PUB us_to_cycles(us) : cycles
  cycles := clkfreq / 1_000_000 * us

PUB cycles_to_ms(cycles) : ms
  ms := cycles / (clkfreq / 1000)

PUB cycles_to_us(cycles) : us
  us := cycles / (clkfreq / 1_000_000)
```

### Minimum Resolution

The minimum delay resolution depends on clock frequency:

| Clock Freq | 1 cycle | Min practical delay |
|------------|---------|---------------------|
| 20 MHz | 50 ns | ~1 µs |
| 100 MHz | 10 ns | ~100 ns |
| 200 MHz | 5 ns | ~50 ns |
| 300 MHz | 3.3 ns | ~30 ns |

Spin2 interpreter overhead adds several microseconds to any operation.

### Compensating for Execution Time

```spin2
PUB precise_interval() | period, next, overhead
  ' Measure overhead once
  next := getct()
  waitct(next)
  overhead := getct() - next

  period := clkfreq / 1000       ' 1ms period
  next := getct()

  repeat
    next += period - overhead
    do_work()
    waitct(next)
```

## Anti-Patterns

### Busy Waiting

```spin2
' WRONG: Wastes CPU cycles
PUB bad_wait(ms) | deadline
  deadline := getms() + ms
  repeat while getms() < deadline
    ' Doing nothing but consuming cycles

' CORRECT: Use blocking wait
PUB good_wait(ms)
  waitms(ms)
```

### Ignoring Rollover

```spin2
' WRONG: Fails when counter rolls over
PUB bad_elapsed() | start, stop
  start := getct()
  do_work()
  stop := getct()
  if stop > start                ' May be false after rollover!
    return stop - start

' CORRECT: Subtraction handles rollover
PUB good_elapsed() | start, stop
  start := getct()
  do_work()
  stop := getct()
  return stop - start            ' Always correct
```

### Drift in Periodic Tasks

```spin2
' WRONG: Drifts over time due to execution time
PUB drifty_periodic()
  repeat
    do_work()
    waitms(100)                  ' 100ms AFTER work completes

' CORRECT: Maintain absolute timing
PUB precise_periodic() | next
  next := getct()
  repeat
    next += clkfreq / 10         ' 100ms interval
    do_work()
    waitct(next)                 ' Wait until next period
```

### Integer Division Truncation

```spin2
' WRONG: Loses precision for small delays
PUB bad_us_delay(us) | cycles
  cycles := clkfreq / 1_000_000 * us  ' May truncate significantly

' BETTER: Reorder to preserve precision
PUB better_us_delay(us) | cycles
  cycles := clkfreq * us / 1_000_000  ' Less truncation for small us

' Or use library functions
PUB best_us_delay(us)
  waitus(us)                     ' Handles precision internally
```

### Blocking in Time-Critical Code

```spin2
' WRONG: Blocks other processing
PUB bad_sensor_read()
  request_reading()
  waitms(100)                    ' Blocks everything for 100ms
  return get_reading()

' BETTER: Non-blocking with state machine
VAR
  long sensor_state
  long sensor_deadline

PUB start_sensor_read()
  request_reading()
  sensor_deadline := getms() + 100
  sensor_state := WAITING

PUB check_sensor_read() : ready
  if sensor_state == WAITING
    if getms() >= sensor_deadline
      sensor_state := READY
      ready := TRUE
```

## Summary Tables

### Spin2 Timing Functions

| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `GETCT()` | - | counter | Get 32-bit system counter |
| `WAITCT(target)` | target value | - | Wait until counter reaches target |
| `POLLCT(target)` | target value | 0/non-zero | Check if target reached |
| `WAITMS(ms)` | milliseconds | - | Wait specified milliseconds |
| `WAITUS(us)` | microseconds | - | Wait specified microseconds |
| `GETMS()` | - | milliseconds | Get ms since boot |
| `GETSEC()` | - | seconds | Get seconds since boot |

### Time Conversions

| From | To | Formula |
|------|-----|---------|
| Milliseconds | Cycles | `ms * clkfreq / 1000` |
| Microseconds | Cycles | `us * clkfreq / 1_000_000` |
| Cycles | Milliseconds | `cycles / (clkfreq / 1000)` |
| Cycles | Microseconds | `cycles / (clkfreq / 1_000_000)` |

### Counter Rollover Times

| Clock Frequency | Rollover Period |
|-----------------|-----------------|
| 20 MHz | 214.7 seconds |
| 100 MHz | 42.9 seconds |
| 200 MHz | 21.5 seconds |
| 300 MHz | 14.3 seconds |
| 500 MHz | 8.6 seconds |

## Related Documentation

- [Clock-Configuration-Usage-Guide.md](Clock-Configuration-Usage-Guide.md) - Setting CLKFREQ
- [Multi-Cog-Usage-Guide.md](Multi-Cog-Usage-Guide.md) - Timing coordination between COGs
- [Control-Flow-Usage-Guide.md](Control-Flow-Usage-Guide.md) - REPEAT loops with timing
