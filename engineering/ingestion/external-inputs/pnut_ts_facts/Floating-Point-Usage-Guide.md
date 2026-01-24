# Floating-Point Usage Guide

## Overview

Spin2 supports IEEE-754 single-precision (32-bit) floating-point numbers. Float operations are performed by the Spin2 interpreter software, as the P2 has no hardware FPU.

**Key Points:**
- Floats stored in 32 bits (same size as LONG)
- Software implementation - slower than integer math
- IEEE-754 single precision (~7 decimal digits precision)
- Float operators use `.` suffix to distinguish from integer operators

## Basic Usage

### Float Constants

```spin2
CON
  PI          = 3.14159
  E           = 2.71828
  GRAVITY     = 9.81
  TEMP_SCALE  = 0.0625

VAR
  long temperature                     ' Floats stored in LONGs

PUB demo()
  temperature := 25.5
  temperature := temperature +. 0.1
```

### Float Literal Syntax

```spin2
CON
  ' Standard decimal notation
  value1 = 3.14159
  value2 = 0.001
  value3 = 100.0

  ' Scientific notation (e or E)
  value4 = 1.0e6                       ' 1,000,000
  value5 = 2.5E-3                      ' 0.0025
  value6 = 6.022e23                    ' Avogadro's number

  ' Negative values
  value7 = -273.15
  value8 = -1.0e-10
```

### Conversion Functions

```spin2
PUB conversion_demo() | int_val, float_val

  ' Integer to float
  int_val := 100
  float_val := float(int_val)          ' 100.0

  ' Float to integer (truncate toward zero)
  float_val := 3.7
  int_val := trunc(float_val)          ' 3

  float_val := -3.7
  int_val := trunc(float_val)          ' -3

  ' Float to integer (round to nearest)
  float_val := 3.7
  int_val := round(float_val)          ' 4

  float_val := 3.4
  int_val := round(float_val)          ' 3

  float_val := -3.7
  int_val := round(float_val)          ' -4
```

## Float Operators

All float operators use a `.` suffix to distinguish them from integer operators.

### Arithmetic Operators

| Operator | Operation | Example |
|----------|-----------|---------|
| `+.` | Addition | `a +. b` |
| `-.` | Subtraction | `a -. b` |
| `*.` | Multiplication | `a *. b` |
| `/.` | Division | `a /. b` |
| `-.` (unary) | Negation | `-. a` |

```spin2
PUB arithmetic_demo() | a, b, result
  a := 10.5
  b := 3.2

  result := a +. b                     ' 13.7
  result := a -. b                     ' 7.3
  result := a *. b                     ' 33.6
  result := a /. b                     ' 3.28125

  result := -. a                       ' -10.5
```

### Comparison Operators

| Operator | Operation | Returns |
|----------|-----------|---------|
| `<.` | Less than | TRUE (-1) or FALSE (0) |
| `>.` | Greater than | TRUE or FALSE |
| `<=.` | Less or equal | TRUE or FALSE |
| `>=.` | Greater or equal | TRUE or FALSE |
| `==.` | Equal | TRUE or FALSE |
| `<>.` | Not equal | TRUE or FALSE |

```spin2
PUB comparison_demo() | a, b
  a := 3.14
  b := 2.71

  if a >. b
    debug("a is greater")

  if a ==. 3.14
    debug("a equals pi (approximately)")
```

### Math Functions

| Function | Operation | Example |
|----------|-----------|---------|
| `FABS` | Absolute value | `fabs(a)` |
| `FSQRT` | Square root | `fsqrt(a)` |
| `NAN` | Check for NaN | `nan(a)` |

```spin2
PUB math_demo() | value, result
  value := -5.5
  result := fabs(value)                ' 5.5

  value := 16.0
  result := fsqrt(value)               ' 4.0

  ' Check for invalid result
  if nan(result)
    debug("Result is not a number")
```

## IEEE-754 Format

Single-precision floats use 32 bits:

```
Bit:  31   30-23      22-0
      S    EEEEEEEE   MMMMMMMMMMMMMMMMMMMMMMM
      |    |          |
      |    |          +-- Mantissa (23 bits, implied leading 1)
      |    +------------- Exponent (8 bits, biased by 127)
      +------------------ Sign (0=positive, 1=negative)
```

### Special Values

| Value | Sign | Exponent | Mantissa |
|-------|------|----------|----------|
| +0.0 | 0 | 0 | 0 |
| -0.0 | 1 | 0 | 0 |
| +Infinity | 0 | 255 | 0 |
| -Infinity | 1 | 255 | 0 |
| NaN | X | 255 | Non-zero |

### Precision Limits

- **Range:** ~1.2e-38 to ~3.4e38
- **Precision:** ~7 significant decimal digits
- **Smallest increment near 1.0:** ~1.2e-7

```spin2
CON
  ' These are equal due to limited precision
  value1 = 1.0000001
  value2 = 1.0000002                   ' May equal value1!

  ' Precision degrades at larger magnitudes
  large1 = 1000000.1
  large2 = 1000000.2                   ' Difference may be lost
```

## Patterns

### Temperature Conversion

```spin2
PUB celsius_to_fahrenheit(celsius) : fahrenheit
  '' Convert Celsius to Fahrenheit

  fahrenheit := celsius *. 1.8 +. 32.0

PUB fahrenheit_to_celsius(fahrenheit) : celsius
  '' Convert Fahrenheit to Celsius

  celsius := (fahrenheit -. 32.0) /. 1.8
```

### Sensor Scaling

```spin2
CON
  ADC_MAX       = 4095                 ' 12-bit ADC
  VOLTAGE_REF   = 3.3                  ' Reference voltage
  SCALE_FACTOR  = 0.0625               ' Sensor scaling

PUB read_voltage() : voltage | raw
  '' Read ADC and convert to voltage

  raw := read_adc()
  voltage := float(raw) *. VOLTAGE_REF /. float(ADC_MAX)

PUB read_temperature() : temp_c | voltage
  '' Read temperature sensor

  voltage := read_voltage()
  temp_c := (voltage -. 0.5) /. SCALE_FACTOR
```

### Distance Calculation

```spin2
PUB distance(x1, y1, x2, y2) : dist | dx, dy
  '' Calculate distance between two points

  dx := x2 -. x1
  dy := y2 -. y1
  dist := fsqrt(dx *. dx +. dy *. dy)
```

### Angle Calculations

```spin2
CON
  PI        = 3.14159265
  DEG_TO_RAD = 0.01745329              ' PI / 180
  RAD_TO_DEG = 57.2957795              ' 180 / PI

PUB degrees_to_radians(degrees) : radians
  radians := degrees *. DEG_TO_RAD

PUB radians_to_degrees(radians) : degrees
  degrees := radians *. RAD_TO_DEG

PUB circumference(radius) : circ
  circ := 2.0 *. PI *. radius

PUB area_circle(radius) : area
  area := PI *. radius *. radius
```

### Moving Average Filter

```spin2
CON
  ALPHA = 0.1                          ' Filter coefficient (0-1)

VAR
  long filtered_value
  long first_sample

PUB init_filter()
  first_sample := TRUE

PUB filter(new_sample) : result
  '' Exponential moving average filter

  if first_sample
    filtered_value := float(new_sample)
    first_sample := FALSE
  else
    ' filtered = alpha * new + (1-alpha) * filtered
    filtered_value := ALPHA *. float(new_sample) +. (1.0 -. ALPHA) *. filtered_value

  result := round(filtered_value)
```

### PID Controller

```spin2
CON
  KP = 1.0                             ' Proportional gain
  KI = 0.1                             ' Integral gain
  KD = 0.05                            ' Derivative gain
  DT = 0.01                            ' Time step (seconds)

VAR
  long integral
  long prev_error

PUB init_pid()
  integral := 0.0
  prev_error := 0.0

PUB pid_update(setpoint, measured) : output | error, derivative
  '' Calculate PID controller output

  error := setpoint -. measured

  ' Integral term
  integral := integral +. error *. DT

  ' Derivative term
  derivative := (error -. prev_error) /. DT
  prev_error := error

  ' PID output
  output := KP *. error +. KI *. integral +. KD *. derivative
```

### Linear Interpolation

```spin2
PUB lerp(a, b, t) : result
  '' Linear interpolation: a + (b-a)*t
  '' t=0.0 returns a, t=1.0 returns b

  result := a +. (b -. a) *. t

PUB map_range(value, in_min, in_max, out_min, out_max) : result
  '' Map value from one range to another

  result := (value -. in_min) /. (in_max -. in_min)
  result := result *. (out_max -. out_min) +. out_min
```

## Float vs Fixed-Point

### When to Use Float

- Sensor data with decimal values
- Scientific calculations
- When precision matters more than speed
- Complex formulas (easier to read/write)

### When to Use Fixed-Point

- Time-critical code
- PASM routines
- Simple scaling operations
- When you control the value range

### Fixed-Point Example

```spin2
CON
  ' Fixed-point with 16.16 format
  FIXED_ONE = $0001_0000               ' 1.0 in fixed-point
  FIXED_HALF = $0000_8000              ' 0.5 in fixed-point

PUB fixed_multiply(a, b) : result
  '' Multiply two 16.16 fixed-point numbers

  result := (a * b) >> 16

PUB fixed_divide(a, b) : result
  '' Divide two 16.16 fixed-point numbers

  result := (a << 16) / b

PUB int_to_fixed(value) : fixed
  '' Convert integer to 16.16 fixed-point

  fixed := value << 16

PUB fixed_to_int(fixed) : value
  '' Convert 16.16 fixed-point to integer (truncate)

  value := fixed >> 16
```

### Performance Comparison

| Operation | Integer | Fixed-Point | Float |
|-----------|---------|-------------|-------|
| Addition | ~1 cycle | ~1 cycle | ~100+ cycles |
| Multiply | ~8 cycles | ~16 cycles | ~200+ cycles |
| Division | ~16 cycles | ~32 cycles | ~300+ cycles |
| Square root | ~50 cycles | ~100 cycles | ~400+ cycles |

## Anti-Patterns

### Float Equality Comparison

```spin2
' WRONG: Direct equality comparison
if result ==. 0.0
  handle_zero()

' CORRECT: Compare with tolerance
CON
  EPSILON = 0.00001

PUB float_equals(a, b) : equal
  equal := fabs(a -. b) <. EPSILON

PUB demo()
  if float_equals(result, 0.0)
    handle_zero()
```

### Accumulating Float Errors

```spin2
' WRONG: Accumulating small values loses precision
VAR
  long sum

PUB bad_accumulate(samples, count) | i
  sum := 0.0
  repeat i from 0 to count - 1
    sum := sum +. samples[i]           ' Error grows with each addition

' BETTER: Kahan summation for better precision
VAR
  long sum, compensation

PUB kahan_sum(samples, count) | i, y, t
  sum := 0.0
  compensation := 0.0
  repeat i from 0 to count - 1
    y := samples[i] -. compensation
    t := sum +. y
    compensation := (t -. sum) -. y
    sum := t
```

### Unnecessary Float Conversion

```spin2
' WRONG: Converting when not needed
PUB bad_scale(value) : result
  result := round(float(value) *. 2.0)

' CORRECT: Use integer math when possible
PUB good_scale(value) : result
  result := value * 2
```

### Float in Tight Loops

```spin2
' WRONG: Float in time-critical loop
PUB bad_loop() | i, sum
  sum := 0.0
  repeat i from 0 to 999
    sum := sum +. float(i)             ' Slow!

' CORRECT: Use integer math, convert once
PUB good_loop() | i, sum
  sum := 0
  repeat i from 0 to 999
    sum += i
  return float(sum)                    ' Convert once at end
```

### Mixing Float and Integer Operations

```spin2
' WRONG: Missing float operator
result := a +. b * c                   ' Integer multiply, then float add!

' CORRECT: Consistent float operators
result := a +. b *. c
```

### Ignoring NaN Results

```spin2
' WRONG: Assumes all operations succeed
result := fsqrt(value)
use_result(result)

' CORRECT: Check for invalid results
result := fsqrt(value)
if nan(result)
  handle_error()
else
  use_result(result)
```

### Loss of Precision in Large Values

```spin2
' WRONG: Adding small value to large value
CON
  LARGE_VALUE = 1.0e7
  SMALL_INCREMENT = 0.001

PUB bad_increment(value) : result
  result := value +. SMALL_INCREMENT   ' Increment may be lost!

' CORRECT: Track accumulated small values separately
VAR
  long large_part
  long small_part

PUB good_increment()
  small_part := small_part +. SMALL_INCREMENT
  if small_part >=. 1.0
    large_part := large_part +. 1.0
    small_part := small_part -. 1.0
```

## Summary Tables

### Conversion Functions

| Function | Input | Output | Description |
|----------|-------|--------|-------------|
| `FLOAT(x)` | Integer | Float | Convert to float |
| `TRUNC(x)` | Float | Integer | Truncate toward zero |
| `ROUND(x)` | Float | Integer | Round to nearest |

### Float Operators

| Operator | Operation | Notes |
|----------|-----------|-------|
| `+.` | Addition | |
| `-.` | Subtraction | |
| `*.` | Multiplication | |
| `/.` | Division | |
| `-.` | Negation (unary) | |
| `<.` | Less than | Returns TRUE/FALSE |
| `>.` | Greater than | Returns TRUE/FALSE |
| `<=.` | Less or equal | Returns TRUE/FALSE |
| `>=.` | Greater or equal | Returns TRUE/FALSE |
| `==.` | Equal | Returns TRUE/FALSE |
| `<>.` | Not equal | Returns TRUE/FALSE |

### Float Functions

| Function | Description | Returns |
|----------|-------------|---------|
| `FABS(x)` | Absolute value | Float |
| `FSQRT(x)` | Square root | Float (NaN if x < 0) |
| `NAN(x)` | Check for Not-a-Number | TRUE/FALSE |

### IEEE-754 Special Values

| Condition | Result |
|-----------|--------|
| 0 / 0 | NaN |
| x / 0 (x != 0) | +/- Infinity |
| sqrt(-x) | NaN |
| Overflow | +/- Infinity |
| Underflow | 0 |

## Related Documentation

- [Operators-Usage-Guide.md](Operators-Usage-Guide.md) - Operator precedence and integer operators
- [Timing-Operations-Usage-Guide.md](Timing-Operations-Usage-Guide.md) - Timing for control loops
