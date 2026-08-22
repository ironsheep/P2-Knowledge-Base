# Chapter 12: Digital Input {#ch12}

This chapter covers reading digital signals, from basic direct I/O through enhanced input conditioning. Topics include INA/INB registers, TESTP instruction, Schmitt trigger inputs, level comparison, and pull-up/pull-down resistors.


## 12.1 Input Architecture

### P2 Input Path

Every P2 I/O pin includes a complete input path with multiple conditioning options:

```{=latex}
\DiagInputPath
```

### Input Timing

| Path | Latency | Data Freshness |
|------|---------|----------------|
| INA/INB register | 3 clocks | Older |
| TESTP/TESTPN | 2 clocks | Fresher |

### Default Input Mode

With no configuration (WRPIN = 0 or P_NORMAL), pins operate as standard CMOS inputs with approximately 1.65V threshold.


## 12.2 Reading Input State

### Spin2 Methods

**PINREAD(pin)** - Read single pin state:
```spin2
value := PINREAD(pin)                      ' Returns 0 or 1
```

**PINR(pin)** - Alias for PINREAD:
```spin2
value := PINR(pin)
```

**Reading via INA/INB:**
```spin2
value := INA                               ' All 32 bits of P0-P31
value := INB                               ' All 32 bits of P32-P63
bit := (INA >> pin) & 1                    ' Single bit extraction
```

### PASM2 Instructions

**TESTP** - Read pin to C or Z flag:
```pasm2
              testp     #pin wc             ' Pin state → C flag
              testp     #pin wz             ' Pin state → Z flag
        if_c  jmp       #pin_high           ' Branch if high (C = IN[pin])
        if_nz jmp       #pin_low            ' Branch if Z=0 → pin low
```

**TESTPN** - Read inverted pin state:
```pasm2
              testpn    #pin wc             ' Inverted state → C
        if_c  jmp       #pin_low            ' C=1 means pin was low
```

**TESTP Flag Operations:**
```pasm2
              testp     #pin andc           ' C = C AND pin_state
              testp     #pin orc            ' C = C OR pin_state
              testp     #pin xorc           ' C = C XOR pin_state
              testp     #pin andz           ' Z = Z AND pin_state
              testp     #pin orz            ' Z = Z OR pin_state
              testp     #pin xorz           ' Z = Z XOR pin_state
```

**Reading INA/INB directly:**
```pasm2
              mov       value, ina          ' Read P0-P31
              mov       value, inb          ' Read P32-P63
              test      ina, mask wz        ' Test specific bits
```

### TESTP vs INA Timing

TESTP reaches the pin a clock sooner than the INA/INB register path (the latencies are tabulated in §12.1; see also Ch1, Input Timing). For time-critical input sampling, prefer TESTP.

```{=latex}
\DiagTestpVsIna
```


## 12.3 Input Conditioning Options

### P_LOGIC_A, P_LOGIC_A_FB, and P_LOGIC_B_FB

All three present the pin as a standard CMOS logic input (~1.65V threshold). They are not interchangeable spellings of one mode — they differ along **two independent routing axes**:

- **Which input reaches IN.** Every smart pin has two independently-selectable input taps, **A** and **B**; each tap can read this pin, a ±1/±2/±3 neighbor, or the pin's own OUT bit (Appendix B, *A/B Input Selection*). `P_LOGIC_A` sends the **A** tap to IN; `P_LOGIC_B_FB` sends the **B** tap instead.
- **What drives the pin's output.** Either the cog's **OUT** bit (the normal path) or the pin's own logic level **fed back** to the output. The `_FB` suffix selects that feedback path.

| Constant | Input → IN | Output driven by |
|----------|:----------:|:----------------:|
| `P_LOGIC_A` (default) | A | OUT |
| `P_LOGIC_A_FB` | A | feedback |
| `P_LOGIC_B_FB` | B | feedback |

```spin2
WRPIN(pin, P_LOGIC_A)         ' A → IN; pin output = cog OUT bit (default)
WRPIN(pin, P_LOGIC_A_FB)      ' A → IN; output = own logic level (feedback)
WRPIN(pin, P_LOGIC_B_FB)      ' B → IN; feedback out (tap AND path differ)
```

`P_LOGIC_B_FB` therefore differs from the `P_LOGIC_A` default on *both* axes — it is not "the same input, routed differently."

### P_SCHMITT_A

Schmitt trigger input — its hysteresis (separate rising and falling thresholds) adds noise immunity and produces clean edges on slow or noisy signals. For how a Schmitt trigger works, see Ch2 §2.3.

```spin2
WRPIN(pin, P_SCHMITT_A)
```

**Use when:**

- Input signal has slow edges
- Signal travels through noisy environment
- Preventing oscillation on threshold crossing

### TTL Threshold (via P_LEVEL_A)

There is no dedicated TTL-threshold constant. To detect a ~1.4V TTL crossing, use the programmable level comparator with a level value of 108 (1.4V ÷ 3.3V × 256 ≈ 108):

```spin2
WRPIN(pin, P_LEVEL_A | (108 << 8))         ' ~1.4V threshold (TTL)
PINFLOAT(pin)
```

**Use when:**

- Interfacing with TTL logic
- Legacy 5V logic with reduced swing
- Signals that don't reach full CMOS levels

### P_LEVEL_A

Programmable level comparator input:

```spin2
' Compare against 8-bit level value
' Level in M[7:0] (shifted into WRPIN value)
level := 128                               ' Mid-scale (approx 1.65V)
WRPIN(pin, P_LEVEL_A | (level << 8))
```

**Level calculation:**
```formula
threshold_voltage = (level / 256) × 3.3V
```

| Level | Voltage |
|-------|---------|
| 0 | 0.0V |
| 64 | 0.83V |
| 128 | 1.65V |
| 192 | 2.48V |
| 255 | 3.28V |

**Use when:**

- Custom threshold required
- Detecting specific voltage levels
- Analog signal digitization


## 12.4 Pull-Up and Pull-Down Resistors

Pull resistors and when to use them are covered in Ch2 §2.2; this section gives the smart-pin constants and how to apply them to inputs.

### Available Options

| Constant | Resistance | Current at 3.3V |
|----------|------------|-----------------|
| P_HIGH_15K | 15kΩ | 220 µA |
| P_HIGH_150K | 150kΩ | 22 µA |
| P_LOW_15K | 15kΩ | 220 µA |
| P_LOW_150K | 150kΩ | 22 µA |

### Configuration

**Pull-up (for active-low buttons):**
```spin2
' 15kΩ weak drive-high acts as a pull-up
WRPIN(pin, P_HIGH_15K)
PINHIGH(pin)                               ' DIR=1, OUT=1 → 15kΩ drive high
```

**Pull-down (for active-high buttons):**
```spin2
' 15kΩ weak drive-low acts as a pull-down
WRPIN(pin, P_LOW_15K)
PINLOW(pin)                                ' DIR=1, OUT=0 → 15kΩ drive low
```

**Combined with input conditioning:**
```spin2
' Schmitt trigger input with 15kΩ drive-high pull-up
WRPIN(pin, P_SCHMITT_A | P_HIGH_15K)
PINHIGH(pin)                               ' DIR=1, OUT=1 → 15kΩ drive high
```

### Choosing Resistance

| Resistance | Advantages | Disadvantages |
|------------|------------|---------------|
| 15kΩ | Stronger pull, faster rise | Higher current draw |
| 150kΩ | Lower power | Slower rise, more noise susceptible |

**15kΩ recommended for:**

- Mechanical switches and buttons
- Long wire runs
- Noisy environments

**150kΩ suitable for:**

- Battery-powered systems
- Short PCB traces
- Low-speed signals


## 12.5 Floating Input Behavior

### Why Inputs Float

When an input pin has no connection and no pull resistor:

- Input buffer amplifies internal noise
- State oscillates unpredictably
- High-speed transitions increase power consumption
- Can cause false triggering

### Detecting Floating Inputs

Floating inputs exhibit rapid state changes:

```spin2
PUB detect_float(pin) : is_floating | count, i
  ' Count transitions in short period
  count := 0
  repeat i from 0 to 1000
    if PINREAD(pin) <> PINREAD(pin)
      count++

  is_floating := (count > 100)
```

### Preventing Float

**Always configure unused pins:**
```spin2
' Option 1: Drive low
PINLOW(unused_pin)

' Option 2: Weak drive-low (holds pin low)
WRPIN(unused_pin, P_LOW_150K)
PINLOW(unused_pin)                         ' DIR=1, OUT=0 → 150kΩ drive low

' Option 3: Weak drive-high (holds pin high)
WRPIN(unused_pin, P_HIGH_150K)
PINHIGH(unused_pin)                        ' DIR=1, OUT=1 → 150kΩ drive high
```


## 12.6 Multi-Pin Input Patterns

### Reading Pin Groups

**Spin2:**
```spin2
' Read 8 pins starting at base_pin
pins_value := PINREAD(base_pin ADDPINS 7)

' Read specific pin range
value := INA.[base_pin + 7..base_pin]
```

**PASM2:**
```pasm2
              ' Read bits from INA
              mov       value, ina
              shr       value, #base_pin
              and       value, #$FF         ' Mask to 8 bits
```

### Atomic Multi-Pin Read

INA/INB provide atomic snapshot of all 32 pins:

```spin2
' All pins read at same instant
snapshot_a := INA
snapshot_b := INB

' Extract fields
lower_byte := snapshot_a & $FF
upper_nibble := (snapshot_a >> 28) & $F
```

### Pin Field Extraction

**Spin2 pin field syntax:**
```spin2
' pins 8-11 (4 bits)
value := PINREAD(8 ADDPINS 3)

' Or using INA range
value := INA.[11..8]
```


## 12.7 Software Debouncing

### Why Debounce?

Mechanical switches and buttons bounce for 1-50ms after contact, causing multiple false transitions.

### Simple Delay Debounce

```spin2
PUB read_button_debounced(pin) : state
  ' Wait for stable state
  state := PINREAD(pin)
  WAITMS(20)                               ' Typical bounce period
  return PINREAD(pin)
```

### Integration Debounce

```spin2
VAR
  long button_acc[8]                       ' Accumulator per button

PUB update_buttons() | i, sample
  repeat i from 0 to 7
    sample := PINREAD(button_pins[i])
    if sample
      button_acc[i] := (button_acc[i] + 1) <# 10  ' Saturate at 10
    else
      button_acc[i] := (button_acc[i] - 1) #> 0   ' Floor at 0

PUB is_button_pressed(idx) : pressed
  pressed := (button_acc[idx] >= 8)        ' Threshold
```

### State Machine Debounce

```spin2
CON
  DEBOUNCE_MS = 50

VAR
  long last_state
  long last_change_ms

PUB debounced_read(pin) : stable_state
  if PINREAD(pin) <> last_state
    if (GETMS() - last_change_ms) > DEBOUNCE_MS
      last_state := PINREAD(pin)
      last_change_ms := GETMS()
  stable_state := last_state
```


## 12.8 Active-Low Signals

### Understanding Active-Low

Many buttons and sensors use active-low signaling:

- Idle/released: Logic high (VDD through pull-up)
- Active/pressed: Logic low (grounded)

### Configuration

```spin2
CON
  BUTTON_PIN = 20

PUB button_init()
  WRPIN(BUTTON_PIN, P_HIGH_15K)            ' 15kΩ drive-high pull-up
  PINHIGH(BUTTON_PIN)                      ' DIR=1, OUT=1 → pull-up active

PUB is_pressed() : pressed
  pressed := NOT PINREAD(BUTTON_PIN)       ' Invert for natural sense
```

### Using TESTPN

PASM2 TESTPN provides inverted read:

```pasm2
              testpn    #BUTTON_PIN wc      ' C=1 when pin is LOW
        if_c  jmp       #button_pressed
```


## 12.9 Worked Examples

### Example 1: Button with LED

```{.spin2 caption="ch12-button-schmitt-led.spin2"}
CON
  _clkfreq = 200_000_000
  LED_PIN = 56
  BUTTON_PIN = 57

PUB main()
  ' Configure LED as output
  PINLOW(LED_PIN)

  ' Configure button with pull-up and Schmitt trigger
  WRPIN(BUTTON_PIN, P_SCHMITT_A | P_HIGH_15K)
  ' DIR=1, OUT=1 -> 15kohm drive-high pull-up
  PINHIGH(BUTTON_PIN)

  ' Main loop
  repeat
    if NOT PINREAD(BUTTON_PIN)             ' Button pressed (active low)
      PINHIGH(LED_PIN)
    else
      PINLOW(LED_PIN)
```

### Example 2: Multiple Button Input

```spin2
CON
  _clkfreq = 200_000_000
  BUTTON_BASE = 20                         ' Buttons on pins 20-23

PUB main() | buttons, last_buttons, i
  ' Configure 4 buttons with pull-ups
  repeat i from 0 to 3
    WRPIN(BUTTON_BASE + i, P_SCHMITT_A | P_HIGH_15K)
    PINHIGH(BUTTON_BASE + i)      ' DIR=1, OUT=1 → 15kΩ drive-high pull-up

  last_buttons := 0

  repeat
    buttons := PINREAD(BUTTON_BASE ADDPINS 3)
    buttons := buttons XOR $F               ' Invert for active-low

    if buttons <> last_buttons
      process_buttons(buttons, last_buttons)
      last_buttons := buttons

    WAITMS(10)                             ' Debounce delay

PUB process_buttons(current, previous) | i, pressed, released
  repeat i from 0 to 3
    pressed := (current.[i]) AND NOT (previous.[i])
    released := NOT (current.[i]) AND (previous.[i])

    if pressed
      DEBUG("Button ", i, " pressed")
    if released
      DEBUG("Button ", i, " released")
```

### Example 3: PASM2 Pin Polling

```pasm2
CON
  _clkfreq = 200_000_000

DAT           org

' Configure input pin
              mov       pin, BUTTON_PIN     ' Load pin 20 (DAT long value)
              wrpin     ##P_SCHMITT_A | P_HIGH_15K, pin
              drvh      pin                 ' DIR=1, OUT=1 → 15kΩ pull-up

' Wait for button press
wait_press
              testpn    pin wc              ' C=1 if pin low (pressed)
        if_nc jmp       #wait_press

' Wait for release
wait_release
              testp     pin wc              ' C=1 if pin high (released)
        if_nc jmp       #wait_release

              jmp       #wait_press         ' Wait for next press

BUTTON_PIN    long      20
pin           res       1
```

### Example 4: Voltage Level Detection

```spin2
CON
  _clkfreq = 200_000_000
  ANALOG_PIN = 10

PUB detect_voltage_ranges() : range | level, threshold
  ' Configure level comparator
  ' Test against multiple thresholds

  ' Test for >2.5V
  threshold := (250 * 256) / 330           ' 193
  WRPIN(ANALOG_PIN, P_LEVEL_A | (threshold << 8))
  PINFLOAT(ANALOG_PIN)
  WAITUS(10)
  if PINREAD(ANALOG_PIN)
    return 3                               ' Above 2.5V

  ' Test for >1.65V
  threshold := 128                         ' Mid-scale
  WRPIN(ANALOG_PIN, P_LEVEL_A | (threshold << 8))
  WAITUS(10)
  if PINREAD(ANALOG_PIN)
    return 2                               ' 1.65V to 2.5V

  ' Test for >0.83V
  threshold := 64
  WRPIN(ANALOG_PIN, P_LEVEL_A | (threshold << 8))
  WAITUS(10)
  if PINREAD(ANALOG_PIN)
    return 1                               ' 0.83V to 1.65V

  return 0                                 ' Below 0.83V
```


## 12.10 Input Timing Analysis

### Propagation Delay

From external signal to INA/INB register:

- Input buffer: small (analog settling ahead of the synchronizer)
- Synchronizer: ~1-2 clock cycles
- Register: 1 clock cycle
- Total: 3 clock cycles typical

At 200 MHz (5ns clock):

- 3 clocks = 15ns minimum
- Add external filter/conditioning time

### Sampling Considerations

For high-speed sampling:

- Use TESTP for 2-clock path (10ns at 200 MHz) — the fastest input path; the input synchronizer latency is inherent and cannot be bypassed
- Account for metastability in async signals

### Maximum Input Frequency

Theoretical maximum depends on sampling method:

- With 2-clock TESTP path: Up to sysclk/4 (50 MHz at 200 MHz)
- Practical limit with noise margin: sysclk/8 to sysclk/10


## 12.11 Quick Reference

### Input Reading

| Method | Spin2 | PASM2 | Latency |
|--------|-------|-------|---------|
| Single pin | PINREAD(pin) | TESTP #pin wc | 2 clocks |
| Multi-pin | PINREAD(base ADDPINS n) | mov val,ina | 3 clocks |
| Register | INA, INB | ina, inb | 3 clocks |

### Input Conditioning

| Constant | Function |
|----------|----------|
| P_NORMAL | Default CMOS input |
| P_LOGIC_A | Logic input, output driven by OUT |
| P_SCHMITT_A | Schmitt trigger (adds input hysteresis) |
| P_LEVEL_A | Programmable level comparator (use level=108 for ~1.4V TTL threshold) |

### Pull Resistors

| Constant | Value | Use |
|----------|-------|-----|
| P_HIGH_15K | 15kΩ pull-up | Buttons, noisy signals |
| P_HIGH_150K | 150kΩ pull-up | Low power, short traces |
| P_LOW_15K | 15kΩ pull-down | Active-high inputs |
| P_LOW_150K | 150kΩ pull-down | Low power |

### Timing Summary

For input/output path latencies (INA/INB vs TESTP), see §12.1 and Ch1, Input Timing.


*This chapter covered basic digital input. For signal measurement modes (timing, counting), see Chapter 13. For serial reception, see Chapter 17.*
