# Pin Operations Usage Guide

## Overview

The Propeller 2 has 64 general-purpose I/O pins (P0-P63), each capable of:
- Digital input/output with configurable drive strength
- Smart pin modes for autonomous hardware functions
- ADC/DAC conversion
- PWM, serial, quadrature encoding, and more

Spin2 provides two levels of pin control:
- **Basic operations** - Simple digital I/O (PINLOW, PINHIGH, PINREAD, etc.)
- **Smart pin operations** - Hardware-accelerated functions (WRPIN, WXPIN, WYPIN, RDPIN)

## Basic Usage

### Digital Output

```spin2
CON
  LED_PIN = 56

PUB blink()
  repeat
    pinhigh(LED_PIN)         ' Drive pin high
    waitms(500)
    pinlow(LED_PIN)          ' Drive pin low
    waitms(500)
```

### Digital Input

```spin2
CON
  BUTTON_PIN = 57

PUB wait_for_button()
  pinfloat(BUTTON_PIN)       ' Set as input (high-impedance)
  repeat until pinread(BUTTON_PIN) == 0
  waitms(50)                 ' Debounce
```

### Pin Range Operations

```spin2
PUB set_port_high()
  pinhigh(0 ADDPINS 7)       ' Set pins 0-7 high simultaneously
  ' Alternative syntax:
  pinhigh(0..7)              ' Same effect
```

## Basic Pin Control

### PINLOW / PINL - Drive Pin Low

```spin2
PINLOW(pin)
PINL(pin)
```

Drives the specified pin to logic low (0V). Enables output driver.

```spin2
pinlow(LED_PIN)              ' Single pin
pinlow(0 ADDPINS 3)          ' Pins 0-3
pinlow(8..15)                ' Pins 8-15
```

### PINHIGH / PINH - Drive Pin High

```spin2
PINHIGH(pin)
PINH(pin)
```

Drives the specified pin to logic high (3.3V). Enables output driver.

```spin2
pinhigh(MOTOR_EN)            ' Enable motor
pinhigh(16 ADDPINS 7)        ' Set 8 pins high
```

### PINTOGGLE / PINT - Toggle Pin State

```spin2
PINTOGGLE(pin)
PINT(pin)
```

Inverts the current output state. If low, becomes high; if high, becomes low.

```spin2
PUB flash_led(pin, count) | i
  repeat count
    pintoggle(pin)
    waitms(100)
    pintoggle(pin)
    waitms(100)
```

### PINFLOAT / PINF - Float Pin (High-Impedance)

```spin2
PINFLOAT(pin)
PINF(pin)
```

Disables the output driver, making the pin high-impedance (input mode).

```spin2
pinfloat(INPUT_PIN)          ' Configure as input
value := pinread(INPUT_PIN)  ' Read the pin state
```

### PINREAD / PINR - Read Pin State

```spin2
state := PINREAD(pin)
state := PINR(pin)
```

Returns the current logic level of the pin (0 or 1).

```spin2
PUB is_button_pressed(pin) : pressed
  pinfloat(pin)              ' Ensure pin is input
  pressed := pinread(pin) == 0  ' Active low button
```

### PINWRITE / PINW - Write Pin State

```spin2
PINWRITE(pin, value)
PINW(pin, value)
```

Sets the pin output based on value: 0 = low, non-zero = high.

```spin2
pinwrite(LED_PIN, sensor_active)  ' LED reflects sensor state
pinwrite(0 ADDPINS 7, byte_value) ' Write 8-bit value to pins
```

## Smart Pin Operations

Smart pins provide hardware-accelerated functions that run autonomously. Each smart pin has:
- **Mode register** - Configures the pin's function
- **X register** - Primary parameter (meaning depends on mode)
- **Y register** - Secondary parameter
- **Z register** - Output/accumulator (read via RDPIN/RQPIN)

### PINSTART - Configure and Start Smart Pin

```spin2
PINSTART(pin, mode, x_value, y_value)
```

Configures all smart pin registers and starts the smart pin in one call.

```spin2
' Configure PWM output
pinstart(PWM_PIN, P_PWM_TRIANGLE | P_OE, pwm_period, pwm_duty)

' Configure async serial transmitter
pinstart(TX_PIN, P_ASYNC_TX | P_OE, baud_rate_x, 0)
```

### PINCLEAR / PINC - Stop Smart Pin

```spin2
PINCLEAR(pin)
PINC(pin)
```

Clears the smart pin mode, stopping any autonomous operation.

```spin2
pinclear(PWM_PIN)            ' Stop PWM
pinfloat(PWM_PIN)            ' Return to input mode
```

### WRPIN - Write Mode Register

```spin2
WRPIN(mode, pin)
```

Sets the smart pin mode register. Mode constants can be combined with OR.

```spin2
wrpin(P_PWM_TRIANGLE | P_OE, PWM_PIN)
```

### WXPIN - Write X Register

```spin2
WXPIN(x_value, pin)
```

Sets the X parameter register.

```spin2
wxpin(period_clocks, PWM_PIN)
```

### WYPIN - Write Y Register

```spin2
WYPIN(y_value, pin)
```

Sets the Y parameter register.

```spin2
wypin(duty_cycle, PWM_PIN)
```

### RDPIN - Read Smart Pin (Blocking)

```spin2
value := RDPIN(pin)
```

Reads the Z register value and acknowledges the smart pin. Blocks until data is ready.

```spin2
adc_value := rdpin(ADC_PIN)
```

### RQPIN - Request Smart Pin Value (Non-Blocking)

```spin2
value := RQPIN(pin)
```

Reads the Z register without blocking or acknowledging. Use when polling.

```spin2
if pinread(ADC_PIN)          ' Check if data ready (IN flag)
  value := rqpin(ADC_PIN)    ' Read without acknowledge
```

### AKPIN - Acknowledge Smart Pin

```spin2
AKPIN(pin)
```

Acknowledges a smart pin read without retrieving the value. Clears the IN flag.

```spin2
akpin(SERIAL_PIN)            ' Acknowledge without reading
```

## Pin Mode Constants

### Drive Strength - High State

| Constant | Description |
|----------|-------------|
| `P_HIGH_FAST` | Maximum drive (default) |
| `P_HIGH_1K5` | 1.5 kΩ equivalent |
| `P_HIGH_15K` | 15 kΩ equivalent |
| `P_HIGH_150K` | 150 kΩ equivalent |
| `P_HIGH_1MA` | 1 mA current source |
| `P_HIGH_100UA` | 100 µA current source |
| `P_HIGH_10UA` | 10 µA current source |
| `P_HIGH_FLOAT` | Float when high |

### Drive Strength - Low State

| Constant | Description |
|----------|-------------|
| `P_LOW_FAST` | Maximum drive (default) |
| `P_LOW_1K5` | 1.5 kΩ equivalent |
| `P_LOW_15K` | 15 kΩ equivalent |
| `P_LOW_150K` | 150 kΩ equivalent |
| `P_LOW_1MA` | 1 mA current sink |
| `P_LOW_100UA` | 100 µA current sink |
| `P_LOW_10UA` | 10 µA current sink |
| `P_LOW_FLOAT` | Float when low |

### Input Configuration

| Constant | Description |
|----------|-------------|
| `P_SCHMITT_A` | Schmitt trigger input A |
| `P_SCHMITT_A_FB` | Schmitt A with feedback |
| `P_SCHMITT_B_FB` | Schmitt B with feedback |
| `P_TTL` | TTL-level thresholds |
| `P_SYNC_IO` | Synchronous I/O |
| `P_ASYNC_IO` | Asynchronous I/O |

### Output Enable

| Constant | Description |
|----------|-------------|
| `P_OE` | Enable output driver |
| `P_INVERT_OUTPUT` | Invert output signal |

## Smart Pin Modes

### PWM Modes

| Constant | Description |
|----------|-------------|
| `P_PWM_TRIANGLE` | Triangle wave PWM |
| `P_PWM_SAWTOOTH` | Sawtooth wave PWM |
| `P_PWM_SMPS` | Switch-mode power supply PWM |
| `P_PULSE` | Single pulse output |

```spin2
CON
  PWM_PIN = 16

PUB start_pwm(freq_hz, duty_percent) | period, duty
  period := clkfreq / freq_hz
  duty := period * duty_percent / 100

  pinstart(PWM_PIN, P_PWM_TRIANGLE | P_OE, period, duty)

PUB set_pwm_duty(duty_percent) | period, duty
  period := clkfreq / 1000         ' Assuming 1kHz
  duty := period * duty_percent / 100
  wypin(duty, PWM_PIN)
```

### Serial Modes

| Constant | Description |
|----------|-------------|
| `P_SYNC_TX` | Synchronous serial transmit |
| `P_SYNC_RX` | Synchronous serial receive |
| `P_ASYNC_TX` | Asynchronous serial transmit |
| `P_ASYNC_RX` | Asynchronous serial receive |

```spin2
CON
  TX_PIN = 62
  RX_PIN = 63
  BAUD = 115200

PUB start_serial() | x_val
  ' X value = (clkfreq / baud) << 16 + (bits-1)
  x_val := (clkfreq / BAUD) << 16 | 7   ' 8 data bits

  ' Configure TX
  pinstart(TX_PIN, P_ASYNC_TX | P_OE, x_val, 0)

  ' Configure RX
  pinstart(RX_PIN, P_ASYNC_RX, x_val, 0)

PUB tx_byte(char)
  wypin(char, TX_PIN)
  repeat until pinread(TX_PIN)   ' Wait for completion

PUB rx_byte() : char
  repeat until pinread(RX_PIN)   ' Wait for data
  char := rdpin(RX_PIN) >> 24    ' Data in upper byte
```

### ADC Modes

| Constant | Description |
|----------|-------------|
| `P_ADC` | Basic ADC mode |
| `P_ADC_EXT` | External reference ADC |
| `P_ADC_SCOPE` | Oscilloscope mode |
| `P_ADC_GIO` | ADC with GIO input |
| `P_ADC_VIO` | ADC with VIO input |
| `P_ADC_FLOAT` | ADC with floating input |
| `P_ADC_1X` | 1x gain |
| `P_ADC_3X` | 3x gain |
| `P_ADC_10X` | 10x gain |
| `P_ADC_30X` | 30x gain |
| `P_ADC_100X` | 100x gain |

```spin2
CON
  ADC_PIN = 40

PUB read_adc() : value
  pinstart(ADC_PIN, P_ADC | P_ADC_GIO, 0, 0)
  waitms(1)                      ' Allow settling
  value := rdpin(ADC_PIN)
  pinclear(ADC_PIN)
```

### DAC Modes

| Constant | Description |
|----------|-------------|
| `P_DAC_990R_3V` | 990Ω, 3.3V range |
| `P_DAC_600R_2V` | 600Ω, 2V range |
| `P_DAC_124R_3V` | 124Ω, 3.3V range |
| `P_DAC_75R_2V` | 75Ω, 2V range |
| `P_DAC_NOISE` | DAC with noise |
| `P_DAC_DITHER_RND` | Random dithering |
| `P_DAC_DITHER_PWM` | PWM dithering |

```spin2
CON
  DAC_PIN = 41

PUB set_dac(value)
  pinstart(DAC_PIN, P_DAC_990R_3V | P_OE, 0, 0)
  wypin(value << 16, DAC_PIN)    ' Value in upper 16 bits
```

### Counter/Encoder Modes

| Constant | Description |
|----------|-------------|
| `P_QUADRATURE` | Quadrature encoder input |
| `P_REG_UP` | Register count up |
| `P_REG_UP_DOWN` | Register count up/down |
| `P_COUNT_RISES` | Count rising edges |
| `P_COUNT_HIGHS` | Count high periods |
| `P_COUNTER_TICKS` | Count clock ticks |
| `P_COUNTER_HIGHS` | Count high ticks |
| `P_COUNTER_PERIODS` | Count periods |

```spin2
CON
  ENCODER_A = 20
  ENCODER_B = 21

PUB start_quadrature()
  ' Configure pin A for quadrature with B as partner
  pinstart(ENCODER_A, P_QUADRATURE, ENCODER_B, 0)

PUB read_encoder() : count
  count := rdpin(ENCODER_A)
```

## ADDPINS Encoding

Multiple pins can be controlled simultaneously using the ADDPINS operator:

```spin2
' Syntax: base_pin ADDPINS count
' Where count = number of additional pins (0-31)

pinhigh(0 ADDPINS 7)         ' Pins 0-7 (8 pins total)
pinlow(16 ADDPINS 3)         ' Pins 16-19 (4 pins total)

' Equivalent range syntax
pinhigh(0..7)                ' Same as 0 ADDPINS 7
```

The encoding packs base pin (6 bits) and count (5 bits) into a single value.

## Patterns

### LED with Configurable Brightness (PWM)

```spin2
CON
  LED_PIN = 56
  PWM_FREQ = 1000            ' 1 kHz

VAR
  long brightness            ' 0-100%

PUB start()
  brightness := 50
  start_pwm()

PUB start_pwm() | period
  period := clkfreq / PWM_FREQ
  pinstart(LED_PIN, P_PWM_TRIANGLE | P_OE, period, period * brightness / 100)

PUB set_brightness(percent)
  brightness := percent #> 0 <# 100
  wypin(clkfreq / PWM_FREQ * brightness / 100, LED_PIN)
```

### Debounced Button Input

```spin2
CON
  BUTTON_PIN = 57
  DEBOUNCE_MS = 50

PUB read_button() : pressed | sample1, sample2
  pinfloat(BUTTON_PIN)

  sample1 := pinread(BUTTON_PIN)
  waitms(DEBOUNCE_MS)
  sample2 := pinread(BUTTON_PIN)

  ' Only report pressed if both samples agree
  pressed := (sample1 == 0) AND (sample2 == 0)
```

### Pin as Open-Drain Output

```spin2
CON
  I2C_SDA = 28

PUB i2c_drive_low()
  pinlow(I2C_SDA)            ' Drive low

PUB i2c_release()
  pinfloat(I2C_SDA)          ' Float high (external pull-up)

PUB i2c_read_bit() : bit
  pinfloat(I2C_SDA)          ' Release
  waitns(500)                ' Setup time
  bit := pinread(I2C_SDA)
```

### Simple Frequency Measurement

```spin2
CON
  FREQ_PIN = 30

PUB measure_frequency() : freq_hz | start_count, end_count
  ' Use counter mode to count rising edges
  pinstart(FREQ_PIN, P_COUNT_RISES, 0, 0)

  start_count := rdpin(FREQ_PIN)
  waitms(1000)               ' Measure for 1 second
  end_count := rdpin(FREQ_PIN)

  freq_hz := end_count - start_count
  pinclear(FREQ_PIN)
```

### Multi-Pin Port Operations

```spin2
CON
  DATA_BASE = 0
  DATA_WIDTH = 8

PUB write_port(value)
  pinwrite(DATA_BASE ADDPINS (DATA_WIDTH-1), value)

PUB read_port() : value | i
  value := 0
  repeat i from 0 to DATA_WIDTH-1
    pinfloat(DATA_BASE + i)
  repeat i from 0 to DATA_WIDTH-1
    if pinread(DATA_BASE + i)
      value |= (1 << i)
```

## Anti-Patterns

### Forgetting to Enable Output

```spin2
' WRONG: Output not enabled
wrpin(P_PWM_TRIANGLE, PWM_PIN)    ' Missing P_OE - no output!

' CORRECT: Include P_OE for output
wrpin(P_PWM_TRIANGLE | P_OE, PWM_PIN)
pinstart(PWM_PIN, P_PWM_TRIANGLE | P_OE, period, duty)
```

### Reading Pin Without Setting Input Mode

```spin2
' WRONG: Pin may still be in output mode
value := pinread(INPUT_PIN)       ' May read output latch, not actual pin

' CORRECT: Ensure input mode first
pinfloat(INPUT_PIN)              ' Set to input
value := pinread(INPUT_PIN)      ' Now reads actual pin state
```

### Not Clearing Smart Pin

```spin2
' WRONG: Smart pin still running after use
pinstart(ADC_PIN, P_ADC, 0, 0)
value := rdpin(ADC_PIN)
' ADC keeps running, consuming power

' CORRECT: Clear when done
pinstart(ADC_PIN, P_ADC, 0, 0)
value := rdpin(ADC_PIN)
pinclear(ADC_PIN)
pinfloat(ADC_PIN)
```

### Blocking on RDPIN Forever

```spin2
' WRONG: May block indefinitely
value := rdpin(SERIAL_RX)        ' Blocks if no data arrives

' CORRECT: Check first or use timeout
repeat until pinread(SERIAL_RX) OR timeout_reached()
if pinread(SERIAL_RX)
  value := rdpin(SERIAL_RX)
```

### Wrong Parameter Order

```spin2
' WRONG: WRPIN parameter order is (mode, pin)
wrpin(TX_PIN, P_ASYNC_TX)        ' Pin and mode swapped!

' CORRECT: Mode first, then pin
wrpin(P_ASYNC_TX | P_OE, TX_PIN)

' Note: PINSTART is (pin, mode, x, y) - different order!
pinstart(TX_PIN, P_ASYNC_TX | P_OE, x_val, y_val)
```

### Confusing Smart Pin Mailbox with COG Mailbox

Smart pin "mailbox mode" is a specific smart pin function for pin-to-pin communication, not the same as COG-to-COG SEND/RECV mailbox.

```spin2
' Smart pin mailbox - for pin synchronization
pinstart(OUT_PIN, P_MAILBOX, 0, 0)

' COG mailbox - for inter-cog communication
SEND := @my_send_routine
value := RECV()

' These are completely different mechanisms!
```

## Summary Tables

### Basic Pin Operations

| Function | Short | Parameters | Returns | Description |
|----------|-------|------------|---------|-------------|
| `PINLOW` | `PINL` | pin | - | Drive low |
| `PINHIGH` | `PINH` | pin | - | Drive high |
| `PINTOGGLE` | `PINT` | pin | - | Toggle state |
| `PINFLOAT` | `PINF` | pin | - | Float (input) |
| `PINREAD` | `PINR` | pin | 0/1 | Read state |
| `PINWRITE` | `PINW` | pin, value | - | Write state |

### Smart Pin Operations

| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `PINSTART` | pin, mode, x, y | - | Configure & start |
| `PINCLEAR` | pin | - | Stop smart pin |
| `WRPIN` | mode, pin | - | Set mode register |
| `WXPIN` | value, pin | - | Set X register |
| `WYPIN` | value, pin | - | Set Y register |
| `RDPIN` | pin | value | Read Z (blocking) |
| `RQPIN` | pin | value | Read Z (non-blocking) |
| `AKPIN` | pin | - | Acknowledge |

### Common Smart Pin Modes

| Mode | X Register | Y Register | Description |
|------|------------|------------|-------------|
| `P_PWM_TRIANGLE` | Period | Duty | Triangle PWM |
| `P_ASYNC_TX` | (clkfreq/baud)<<16 + bits | - | Serial TX |
| `P_ASYNC_RX` | (clkfreq/baud)<<16 + bits | - | Serial RX |
| `P_ADC` | - | - | ADC input |
| `P_QUADRATURE` | Partner pin | - | Encoder |
| `P_COUNT_RISES` | - | - | Edge counter |

## Related Documentation

- [Multi-Cog-Usage-Guide.md](Multi-Cog-Usage-Guide.md) - Pin access from multiple COGs
- [Timing-Operations-Usage-Guide.md](Timing-Operations-Usage-Guide.md) - Timing for pin operations
- [Spin2-Object-Patterns-Guide.md](Spin2-Object-Patterns-Guide.md) - Driver object patterns
