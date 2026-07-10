# Chapter 6: Digital Output {#ch6}

This chapter covers digital output configurations using P_NORMAL mode (%00000) with enhanced pin settings. While not technically a "smart pin mode," these configurations use WRPIN to set drive characteristics, polarity, and output topology—extending basic Direct I/O with hardware-configurable behavior.

## 6.1 Overview

### P_NORMAL Mode

When WRPIN bits [5:1] = %00000, the pin operates in P_NORMAL mode—basic Direct I/O with enhanced characteristics. The pin is controlled by DIR and OUT bits (via DRVH, DRVL, etc.) but with configurable:

- Drive strength (high and low independently)
- Output polarity (inverted or normal)
- Input conditioning (Schmitt trigger, comparator)

### When to Use P_NORMAL Output

**Use P_NORMAL output for:**

- Simple on/off control (LEDs, relays, enables)
- Software-timed signals (bit-banging)
- Irregular patterns not suited to smart pin automation
- Open-drain/open-collector interfaces
- When cog control is preferred over autonomy

**Consider smart pin modes (Chapters 7-11) for:**

- Precise timing requirements
- Free-running oscillators
- PWM at high frequencies
- Serial communication
- Autonomous operation

## 6.2 Output Configurations

### Push-Pull Output (Standard)

The default configuration: both high and low are actively driven.

**Configuration:**
```spin2
WRPIN(pin, P_HIGH_FAST | P_LOW_FAST)      ' Default drive strength
```

Or use Direct I/O without WRPIN (defaults apply):
```spin2
PINHIGH(pin)                              ' Drives high
PINLOW(pin)                               ' Drives low
```

**Drive Strength Options:**

| High Drive | Low Drive | Use Case |
|------------|-----------|----------|
| P_HIGH_FAST | P_LOW_FAST | Standard digital (30mA) |
| P_HIGH_1K5 | P_LOW_1K5 | Current-limited (~2mA) |
| P_HIGH_1MA | P_LOW_1MA | Current-source LED drive |

**Example - LED with current limiting:**

```spin2
CON
  LED_PIN = 56

PUB setup()
  ' 1.5kΩ series resistance limits current
  WRPIN(LED_PIN, P_HIGH_1K5 | P_LOW_FAST)

PUB led_on()
  PINHIGH(LED_PIN)

PUB led_off()
  PINLOW(LED_PIN)
```

```pasm2
              wrpin     ##(P_HIGH_1K5 | P_LOW_FAST), #LED_PIN
              drvh      #LED_PIN          ' LED on
              drvl      #LED_PIN          ' LED off
```

### Open-Drain Output

Drives low actively; floats when logically high. Requires external pull-up resistor. Used for I²C, 1-Wire, and multi-master buses.

**Configuration:**
```spin2
WRPIN(pin, P_HIGH_FLOAT | P_LOW_FAST)
```

**Behavior:**

- PINHIGH/DRVH → Pin floats (external pull-up pulls high)
- PINLOW/DRVL → Pin drives low

**Example - I²C-style bus:**

```spin2
CON
  SDA_PIN = 0
  SCL_PIN = 1

PUB setup_i2c()
  ' Open-drain with fast low drive
  WRPIN(SDA_PIN, P_HIGH_FLOAT | P_LOW_FAST | P_SCHMITT_A)
  WRPIN(SCL_PIN, P_HIGH_FLOAT | P_LOW_FAST | P_SCHMITT_A)
  
  ' Release lines (high via external pull-ups)
  PINHIGH(SDA_PIN)
  PINHIGH(SCL_PIN)

PUB sda_low()
  PINLOW(SDA_PIN)                         ' Drive low

PUB sda_release()
  PINHIGH(SDA_PIN)                        ' Float (pull-up makes high)

PUB sda_read() : state
  state := PINREAD(SDA_PIN)               ' Read current state
```

```pasm2
' Open-drain configuration
              wrpin ##(P_HIGH_FLOAT | P_LOW_FAST | P_SCHMITT_A), #SDA_PIN
              
' Drive low
              drvl      #SDA_PIN
              
' Release (float high)
              drvh      #SDA_PIN

' Read
              testp     #SDA_PIN wc       ' C = SDA state
```

`TESTP` is used for the read-back (rather than reading the INA register) deliberately: it sees the pin two clocks old versus three for INA — one clock fresher, which matters on a fast bus where a line is driven and immediately sampled (see §1.2).

**With Internal Pull-Up:**

If external pull-up isn't available, use internal resistive drive:
```spin2
WRPIN(pin, P_HIGH_15K | P_LOW_FAST)       ' 15kΩ pull-up when high
```

Note: Internal pull-ups are weaker than typical external pull-ups and may not meet bus specifications for higher speeds.

### Open-Source Output

Drives high actively; floats when logically low. Less common than open-drain.

**Configuration:**
```spin2
WRPIN(pin, P_HIGH_FAST | P_LOW_FLOAT)
```

**Behavior:**

- PINHIGH/DRVH → Pin drives high
- PINLOW/DRVL → Pin floats (external pull-down pulls low)

### Inverted Output

Output logic is inverted from the OUT bit.

**Configuration:**
```spin2
WRPIN(pin, P_INVERT_OUTPUT)
```

**Behavior:**

- PINHIGH/DRVH (OUT=1) → Pin drives LOW
- PINLOW/DRVL (OUT=0) → Pin drives HIGH

**Use Case:** Active-low devices where software logic is more natural as active-high.

**Example - Active-low LED:**

```spin2
CON
  LED_PIN = 56                         ' LED connected to VCC, active low

PUB setup()
  WRPIN(LED_PIN, P_INVERT_OUTPUT)

PUB led_on()
  PINHIGH(LED_PIN)                        ' Drives LOW, LED on

PUB led_off()
  PINLOW(LED_PIN)                         ' Drives HIGH, LED off
```

### Tri-State Output

Explicit control of output enable separate from output value.

**Pattern 1: Using DIR for enable**

```spin2
' Output disabled (floating)
PINFLOAT(pin)

' Output enabled, driving last OUT value
PINHIGH(pin)                              ' or PINLOW(pin)
```

**Pattern 2: Pre-setting value before enable**

To avoid glitches, pre-set the output value while floating:

```spin2
' Prepare output value while disabled
WRPIN(pin, P_HIGH_FAST | P_LOW_FAST)      ' Configure
PINFLOAT(pin)                             ' Ensure disabled

' Set intended output state
' (Internal OUT register is set but pin is floating)
' Use FLT instructions to set OUT while keeping DIR=0

' Then enable
PINHIGH(pin)                              ' Enable and drive high
```

```pasm2
' Pre-set output high, pin floating
              flth      #pin              ' DIR=0, OUT=1

' Later, enable output (immediately high, no glitch)
              dirh      #pin              ' DIR=1, drives high
```

## 6.3 Software-Timed Output Patterns

### Bit-Banging Serial

For non-standard protocols or when smart pin serial modes don't fit:

```spin2
CON
  TX_PIN = 20
  BIT_TIME = 1000                         ' Clocks per bit

PUB send_byte(data) | i
  ' Start bit (low)
  PINLOW(TX_PIN)
  WAITCT(GETCT() + BIT_TIME)
  
  ' Data bits (LSB first)
  repeat i from 0 to 7
    if data & 1
      PINHIGH(TX_PIN)
    else
      PINLOW(TX_PIN)
    data >>= 1
    WAITCT(GETCT() + BIT_TIME)  ' wait one bit time
  
  ' Stop bit (high)
  PINHIGH(TX_PIN)
  WAITCT(GETCT() + BIT_TIME)
```

### Pulse Generation

```spin2
PUB pulse(pin, width_us) | start
  PINHIGH(pin)
  WAITUS(width_us)
  PINLOW(pin)
```

```pasm2
pulse         drvh      pin
              waitx     width             ' Width in clocks
              drvl      pin
              ret
```

### Fast Toggle

A fast software toggle loop:

```pasm2
.fast_toggle
              drvh      #pin              ' 2 cycles
              drvl      #pin              ' 2 cycles
              jmp       #.fast_toggle     ' 4 cycles
              
' Total: 8 cycles per complete cycle = 25 MHz at 200 MHz sysclk
  ' (The 3-clock output latency is a one-time pipeline offset,
  ' not a per-edge cost)
```

The 3-clock output latency is a fixed pipeline delay — it sets *when* each edge reaches the pad (3 clocks after the instruction completes), not *how often* edges can be produced. It does not lower the toggle frequency; throughput is set by the instruction count in the loop.

## 6.4 Timing Analysis

### Instruction Timing

| Quantity | Cycles | At 200 MHz |
|----------|--------|------------|
| DRVH/DRVL execution — cost **per transition** (throughput) | 2 | 10 ns |
| Output pipeline delay — fixed **latency** (instruction completes → pin edge) | 3 | 15 ns |
| Latency, instruction *start* → pin edge (2 + 3) | 5 | 25 ns |

**How to read this table:** the per-transition *cost* is the **2-clock** instruction time — that is what limits how fast edges can be emitted, and because back-to-back instructions pipeline, edges follow at the instruction rate. The **3-clock pipeline delay is latency, not throughput**: it shifts *when* an edge reaches the pad (5 clocks total from instruction start) but is a one-time offset, *not* added to every transition. Do **not** sum 2 + 3 to compute a per-edge rate.

### Maximum Toggle Rate

The fastest software toggle uses `REP` to remove branch overhead. `REP` repeats an instruction block without any per-iteration branch, so each `DRVNOT` costs only its own 2 clocks:

```pasm2
              rep       #1,#0             ' Repeat next instruction indefinitely
              drvnot    #pin              ' 2 cycles per toggle
```
Period: 2 cycles per toggle = 10 ns → 100M toggles/s at 200 MHz sysclk — i.e. a 50 MHz square wave.

**Branch-based tight loop** (pays the 4-clock taken branch on every edge):
```pasm2
              drvnot    #pin              ' 2 cycles
              jmp       #$-1              ' 4 cycles (taken branch)
```
Period: 6 cycles = 30 ns → ~33 MHz toggle (edge) rate at 200 MHz sysclk — i.e. a ~16.5 MHz square wave — 3× slower than the `REP` form because of the branch overhead.

The 3-clock output latency shifts *when* edges reach the pad but does not reduce the edge rate; the actual rate is set by the loop's instruction count (the per-transition cost), not by the latency.

### When Direct I/O is Faster

Direct I/O is faster than smart pins for:

- Infrequent, irregular pulses
- One-shot signals
- Quick on/off without setup overhead

Smart pins are faster when:

- Continuous waveforms are needed
- Cog should be free for other work
- Precise timing independent of software

### Smart Pin Overhead

Smart pin configuration takes ~10 cycles (DIRL + WRPIN + WXPIN + WYPIN + DRVL). For a single pulse, Direct I/O is more efficient. For continuous operation, smart pin overhead is negligible.

## 6.5 Worked Examples

### Example 1: Status LED with Blink

```{.spin2 caption="ch06-current-drive-blink.spin2"}
CON
  _clkfreq = 200_000_000
  LED_PIN = 56
  BLINK_MS = 500

PUB main()
  ' Current-source for consistent brightness
  WRPIN(LED_PIN, P_HIGH_1MA | P_LOW_FAST)
  
  repeat
    PINHIGH(LED_PIN)
    WAITMS(BLINK_MS)
    PINLOW(LED_PIN)
    WAITMS(BLINK_MS)
```

```pasm2
CON
  _clkfreq = 200_000_000

DAT           org

              wrpin     ##(P_HIGH_1MA | P_LOW_FAST), #56

.loop         drvh      #56
              waitx     half_sec
              drvl      #56
              waitx     half_sec
              jmp       #.loop

half_sec      long      100_000_000       ' 0.5 sec at 200 MHz
```

### Example 2: I²C Bit-Bang (Open-Drain)

```spin2
CON
  SDA = 0
  SCL = 1

PUB i2c_init()
  WRPIN(SDA, P_HIGH_FLOAT | P_LOW_FAST | P_SCHMITT_A)
  WRPIN(SCL, P_HIGH_FLOAT | P_LOW_FAST | P_SCHMITT_A)
  PINHIGH(SDA)                            ' Release both
  PINHIGH(SCL)

PUB i2c_start()
  PINHIGH(SDA)
  PINHIGH(SCL)
  WAITUS(5)
  PINLOW(SDA)                             ' SDA low while SCL high
  WAITUS(5)
  PINLOW(SCL)

PUB i2c_stop()
  PINLOW(SDA)
  PINHIGH(SCL)
  WAITUS(5)
  PINHIGH(SDA)                            ' SDA high while SCL high
```

### Example 3: Stepper Motor Pulses

```spin2
CON
  STEP_PIN = 10
  DIR_PIN = 11
  STEPS_PER_REV = 200

PUB step_forward(steps) | i
  PINHIGH(DIR_PIN)                        ' Direction: forward
  repeat i from 1 to steps
    PINHIGH(STEP_PIN)
    WAITUS(10)                            ' Pulse width
    PINLOW(STEP_PIN)
    WAITUS(1000)                          ' Step delay

PUB step_reverse(steps) | i
  PINLOW(DIR_PIN)                         ' Direction: reverse
  repeat i from 1 to steps
    PINHIGH(STEP_PIN)
    WAITUS(10)
    PINLOW(STEP_PIN)
    WAITUS(1000)
```

## 6.6 Configuration Quick Reference

| Topology | WRPIN Value |
|----------|-------------|
| Push-pull (standard) | `P_HIGH_FAST` \| `P_LOW_FAST` |
| Push-pull (current limit) | `P_HIGH_1K5` \| `P_LOW_1K5` |
| Open-drain | `P_HIGH_FLOAT` \| `P_LOW_FAST` |
| Open-drain + internal pull-up | `P_HIGH_15K` \| `P_LOW_FAST` |
| Open-source | `P_HIGH_FAST` \| `P_LOW_FLOAT` |
| Inverted | `P_INVERT_OUTPUT` |
| LED current source | `P_HIGH_1MA` \| `P_LOW_FAST` |


*This chapter covered software-controlled digital output. For hardware-automated pulse and transition output, see Chapter 7. For continuous waveform generation, see Chapters 8 (NCO) and 9 (PWM).*
