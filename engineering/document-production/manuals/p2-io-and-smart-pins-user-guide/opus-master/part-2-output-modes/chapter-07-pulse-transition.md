# Chapter 7: Pulse & Transition — Signal Generation {#ch7}

This chapter covers hardware-generated pulses and transitions using two smart pin modes: **P_PULSE** (%00100) for generating counted pulse cycles, and **P_TRANSITION** (%00101) for generating counted signal transitions.


## 7.1 Overview

### Pulse vs Transition

**P_PULSE (Pulse/Cycle Output):**

- Generates a programmable number of pulse cycles
- Each cycle has configurable high-time and low-time
- Output returns to low when complete
- Y register controls the number of cycles

**P_TRANSITION (Transition Output):**

- Generates a programmable number of signal transitions (edges)
- Each transition occurs at a fixed base period
- Output remains at final state when complete
- Y register controls the number of transitions

### When to Use These Modes

**Use P_PULSE for:**

- Stepper motor step pulses
- Trigger pulses with specific counts
- Timed burst generation
- PWM with controlled duration

**Use P_TRANSITION for:**

- Precise edge generation
- RS-485 direction control timing
- Delayed signal assertion
- Clock bursts with known edge count


## 7.2 P_PULSE Mode (%00100)

### Function

P_PULSE generates a specified number of pulse cycles. Each cycle consists of a programmable high-time followed by a programmable low-time. When the cycle count reaches zero, the output remains low and IN is raised.

### Configuration

| Register | Field | Purpose |
|----------|-------|---------|
| X[15:0] | Base period | Total cycle length in clock cycles |
| X[31:16] | Compare value | Output HIGH while counter > this; numerically the LOW-time clocks |
| Y[31:0] | Cycle count | Number of cycles to generate |

### Output Behavior

On each clock, the base period counter counts from X[15:0] down to 1, then restarts. The output is:

- **HIGH** when counter > X[31:16] AND Y > 0
- **LOW** otherwise

After each complete base period (counter reaches 1), Y is decremented. When Y reaches 0, the output stays low and IN is raised.

### Timing Diagram

For X[15:0] = 4, X[31:16] = 2, Y = 3:

```{=latex}
\DiagPulseOutput
```

### Duty Cycle Calculation

The duty cycle is determined by the compare value relative to the base period:

```formula
High time = X[15:0] - X[31:16] clocks
Low time  = X[31:16] clocks
Duty cycle = (X[15:0] - X[31:16]) / X[15:0]
```

**Special cases:**

- X[31:16] = 0: Output stays high for entire period (100% duty)
- X[31:16] = X[15:0]: Output stays low (0% duty)

### Configuration Sequence

**Spin2:**
```spin2
CON
  PULSE_PIN = 10
  BASE_PERIOD = 1000                      ' 1000 clocks per cycle
  LOW_TIME = 500                          ' X[31:16]: 500 lo, 500 hi (50%)
  CYCLE_COUNT = 10                        ' Generate 10 pulses

PUB generate_pulses() | ack
  PINFLOAT(PULSE_PIN)                     ' Reset
  WRPIN(PULSE_PIN, P_PULSE | P_OE)        ' Configure mode
  WXPIN(PULSE_PIN, BASE_PERIOD | (LOW_TIME << 16))  ' Set timing
  PINLOW(PULSE_PIN)                       ' Enable
  
  WYPIN(PULSE_PIN, CYCLE_COUNT)           ' Trigger: generate 10 pulses
  
  ' Wait for completion
  repeat until PINREAD(PULSE_PIN) == 1
  ack := RDPIN(PULSE_PIN)        ' Acknowledge completion (discard value)
```

**PASM2:**
```pasm2
              dirl      #PULSE_PIN
              wrpin     ##(P_PULSE | P_OE), #PULSE_PIN
              wxpin     ##(BASE_PERIOD | (LOW_TIME << 16)), #PULSE_PIN
              drvl      #PULSE_PIN
              
              wypin     #CYCLE_COUNT, #PULSE_PIN     ' Trigger
              
.wait         testp     #PULSE_PIN wc
        if_nc jmp       #.wait
              rdpin     result, #PULSE_PIN           ' Acknowledge
```

### Retriggering

Writing a non-zero Y value — whether the pin is idle (Y already 0) or a sequence is still running (Y > 0) — begins pulse output at the next base period boundary. There is no immediate-start fast path; every non-zero Y write is honored at the next base period.

This allows continuous pulse generation or mid-stream adjustment.


## 7.3 P_TRANSITION Mode (%00101)

### Function

P_TRANSITION generates a specified number of signal transitions (edges). Each transition occurs at the base period boundary. The output toggles on each boundary until the transition count reaches zero.

### Configuration

| Register | Field | Purpose |
|----------|-------|---------|
| X[15:0] | Base period | Clocks between transitions |
| Y[31:0] | Transition count | Number of edges to generate |

### Output Behavior

When Y is written with a non-zero value:

1. At each base period, the output toggles
2. Y is decremented after each toggle
3. When Y reaches 0, toggling stops
4. IN is raised
5. Output remains at its final state

### Timing Diagram

For X[15:0] = 100, Y = 4, starting from low:

```{=latex}
\DiagTransitionOutput
```

### Configuration Sequence

**Spin2:**
```spin2
CON
  TRANS_PIN = 11
  EDGE_PERIOD = 200                       ' 200 clocks between edges
  EDGE_COUNT = 8                          ' Generate 8 edges (4 cycles)

PUB generate_transitions() | ack
  PINFLOAT(TRANS_PIN)
  WRPIN(TRANS_PIN, P_TRANSITION | P_OE)
  WXPIN(TRANS_PIN, EDGE_PERIOD)
  PINLOW(TRANS_PIN)
  
  WYPIN(TRANS_PIN, EDGE_COUNT)            ' Trigger
  
  repeat until PINREAD(TRANS_PIN) == 1
  ack := RDPIN(TRANS_PIN)                 ' Acknowledge (discard value)
```

**PASM2:**
```pasm2
              dirl      #TRANS_PIN
              wrpin     ##(P_TRANSITION | P_OE), #TRANS_PIN
              wxpin     #EDGE_PERIOD, #TRANS_PIN
              drvl      #TRANS_PIN
              
              wypin     #EDGE_COUNT, #TRANS_PIN
              
.wait         testp     #TRANS_PIN wc
        if_nc jmp       #.wait
              rdpin     result, #TRANS_PIN
```

### Transition Count and Final State

The final output state depends on:

- Initial state (low after reset)
- Number of transitions (odd = opposite state, even = same state)

| Initial | Transitions | Final |
|---------|-------------|-------|
| Low | 1 | High |
| Low | 2 | Low |
| Low | 3 | High |
| Low | 4 | Low |


## 7.4 Applicable P_ Constants

Both modes support these configuration options:

| Constant | Purpose |
|----------|---------|
| `P_OE` | **Required** - Enable output |
| `P_INVERT_OUTPUT` | Invert output polarity |
| `P_HIGH_FAST` | Fast high drive (default) |
| `P_LOW_FAST` | Fast low drive (default) |
| `P_HIGH_1K5` / `P_LOW_1K5` | Current-limited drive |

**Example - Inverted output:**
```spin2
WRPIN(pin, P_PULSE | P_OE | P_INVERT_OUTPUT)
```


## 7.5 Timing Calculations

### Pulse Width Calculation

For P_PULSE:
```formula
Pulse period = X[15:0] × (1 / sysclk)
High time = (X[15:0] - X[31:16]) × (1 / sysclk)
```

**Example at 200 MHz:**
```formula
X[15:0] = 2000, X[31:16] = 500
Period    = 2000 / 200MHz = 10 µs
High time = (2000 - 500) / 200MHz = 7.5 µs
Low time  = 500 / 200MHz = 2.5 µs
Duty cycle = 1500 / 2000 = 75%
```

### Transition Period Calculation

For P_TRANSITION:
```formula
Time between edges = X[15:0] × (1 / sysclk)
```

**Example at 200 MHz:**
```formula
X[15:0] = 1000
Edge period = 1000 / 200MHz = 5 µs
```

### Timing at Different Clock Frequencies

| sysclk | X value for 1 µs | X value for 10 µs |
|--------|------------------|-------------------|
| 100 MHz | 100 | 1000 |
| 180 MHz | 180 | 1800 |
| 250 MHz | 250 | 2500 |
| 350 MHz | 350 | 3500 |

*The P2 datasheet gives a rated 180 MHz; the Silicon Documentation notes a practical ceiling around 350 MHz. Frequencies in between (e.g. 250 MHz) are commonly used. Operation above the rated frequency depends on cooling and duty cycle — sustained high-throughput work generates heat that limits the usable maximum. (180 MHz: P2 Datasheet; 350 MHz ceiling: Parallax Propeller 2 Documentation, Silicon Doc.)*


## 7.6 Comparison: When to Use Each Mode

| Requirement | Use |
|-------------|-----|
| Fixed number of pulses | P_PULSE |
| Specific duty cycle | P_PULSE |
| Single delayed edge | P_TRANSITION with Y=1 |
| Clock burst with edge count | P_TRANSITION |
| Asymmetric high/low times | P_PULSE |
| Equal high/low times | Either (P_TRANSITION simpler) |
| Stay high after pulse train | P_TRANSITION (odd count) |
| Return to low after | P_PULSE |

### Pulse vs Transition vs Software

| Approach | Best For |
|----------|----------|
| P_PULSE | Precise pulse trains, stepper motors |
| P_TRANSITION | Edge counting, clock bursts |
| Software (DRVH/DRVL) | Irregular patterns, conditional logic |


## 7.7 Worked Examples

### Example 1: Stepper Motor Step Pulse

```{.spin2 caption="ch07-step-motor-pulses.spin2"}
CON
  _clkfreq = 200_000_000
  STEP_PIN = 10
  STEP_PERIOD = 400                       ' 2 µs period
  STEP_LOW = 200                          ' X[31:16] compare = 1 µs low time
                                          ' (high time = 400-200 = 200 = 1 µs, 50% duty)

PUB step_motor(steps) | ack
  PINFLOAT(STEP_PIN)
  WRPIN(STEP_PIN, P_PULSE | P_OE)
  WXPIN(STEP_PIN, STEP_PERIOD | (STEP_LOW << 16))
  PINLOW(STEP_PIN)
  
  WYPIN(STEP_PIN, steps)                  ' Generate step pulses
  
  ' Wait for completion
  repeat until PINREAD(STEP_PIN) == 1
  ack := RDPIN(STEP_PIN)                  ' Acknowledge (discard value)
```

### Example 2: RS-485 Transmit Disable Delay

After transmitting, delay before releasing the line:

```spin2
CON
  _clkfreq = 200_000_000
  DE_PIN = 20                             ' Driver Enable
  DISABLE_DELAY = 2000                    ' 10 µs delay

PUB setup_de()
  PINFLOAT(DE_PIN)
  WRPIN(DE_PIN, P_TRANSITION | P_OE | P_INVERT_OUTPUT)
  WXPIN(DE_PIN, DISABLE_DELAY)
  PINLOW(DE_PIN)                          ' DE is high (enabled) after setup due to output inversion

PUB tx_complete()
  ' After transmission, trigger delayed disable
  ' DE is currently high (enabled) due to inversion
  WYPIN(DE_PIN, 1)                        ' Single transition: high → low
  ' After DISABLE_DELAY clocks, DE goes low (driver disabled)
```

### Example 3: Trigger Pulse Burst

```spin2
CON
  TRIG_PIN = 15
  PULSE_WIDTH = 100                       ' 500 ns at 200 MHz
  PULSE_COUNT = 5

PUB trigger_burst() | ack
  PINFLOAT(TRIG_PIN)
  WRPIN(TRIG_PIN, P_PULSE | P_OE)
  WXPIN(TRIG_PIN, (PULSE_WIDTH * 2) | (PULSE_WIDTH << 16))  ' 50% duty
  PINLOW(TRIG_PIN)
  
  WYPIN(TRIG_PIN, PULSE_COUNT)
  
  repeat until PINREAD(TRIG_PIN) == 1
  ack := RDPIN(TRIG_PIN)                  ' Acknowledge (discard value)
```

### Example 4: PASM2 Continuous Step Generation

```pasm2
CON
  _clkfreq = 200_000_000
  STEP_PIN = 10
  STEP_PERIOD = 400
  STEP_LOW = 200                          ' X[31:16] compare = low-time clocks

DAT           org

' Setup
              dirl      #STEP_PIN
              wrpin     ##(P_PULSE | P_OE), #STEP_PIN
              wxpin     ##(STEP_PERIOD | (STEP_LOW << 16)), #STEP_PIN
              drvl      #STEP_PIN

' Generate steps as needed
step_loop
              wypin     steps_needed, #STEP_PIN
              
.wait         testp     #STEP_PIN wc
        if_nc jmp       #.wait
              rdpin     result, #STEP_PIN
              
              ' Check for more steps
              cmp       more_steps, #0 wz
        if_nz jmp       #step_loop
              
              jmp       #$                ' Done

steps_needed  long      100
more_steps    long      0
result        long      0
```


## 7.8 Quick Reference

### P_PULSE Configuration

| Parameter | Register | Range | Notes |
|-----------|----------|-------|-------|
| Base period | X[15:0] | 1-65535 | Clocks per cycle |
| Compare value | X[31:16] | 0-65535 | Output HIGH when counter > this (low-time clocks) |
| Cycle count | Y[31:0] | 1 to 2³²-1 | Pulses to generate (0 = idle) |

### P_TRANSITION Configuration

| Parameter | Register | Range | Notes |
|-----------|----------|-------|-------|
| Edge period | X[15:0] | 1-65535 | Clocks between edges |
| Edge count | Y[31:0] | 1 to 2³²-1 | Transitions to make (0 = idle) |

### Reset State

Both modes when DIR=0:

- IN = low
- Output = low
- Y = 0


*This chapter covered hardware-timed pulse and transition generation. For continuous waveform generation, see Chapter 8 (NCO) and Chapter 9 (PWM).*
