# Chapter 3: Smart Pin Architecture - Autonomous I/O {#ch3}

Smart pins transform P2 I/O pins from simple input/output points into autonomous peripheral engines. Once configured, a smart pin operates independently of the cog—generating waveforms, measuring signals, counting events, or performing analog conversions without consuming cog cycles. This chapter establishes the mental model for understanding all smart pin modes documented in Parts II through IV.


## 3.1 The Autonomous Operation Concept

### What Makes Smart Pins "Smart"

A traditional microcontroller pin requires continuous software attention. To generate a PWM signal, for example, software must toggle the pin at precise intervals. To measure an input pulse width, software must sample the pin and track timing. These operations consume CPU cycles and require precise interrupt handling.

Smart pins invert this model. Once configured:

- **The hardware generates signals autonomously** - PWM, serial data, NCO waveforms run without cog intervention
- **The hardware measures signals autonomously** - Pulse widths, frequencies, quadrature positions accumulate in registers
- **The cog interacts only when needed** - To read results, update parameters, or reconfigure

This autonomous operation enables:

- **Precise timing** - Hardware-level timing accuracy, independent of software execution
- **Multi-channel operation** - Every pin can run its own smart pin mode simultaneously
- **Reduced cog load** - cogs spend time on computation rather than I/O bit-banging
- **Deterministic behavior** - Hardware timing is unaffected by software complexity

### The Relationship Between Cog and Smart Pin

Each smart pin operates as an independent state machine. The cog's role is:

1. **Configure** the smart pin (mode, parameters)
2. **Enable** the smart pin (set DIR=1)
3. **Monitor** the IN flag for events
4. **Read** results when ready
5. **Update** parameters as needed
6. **Disable** when finished

Between these interactions, the smart pin runs autonomously.


## 3.2 The X / Y / Z Registers (plus the mode word)

Every smart pin has four 32-bit registers: a mode-configuration register written by WRPIN (the mode-control word, see §3.5), plus the three parameter/result registers—X, Y, and Z—described here. The mode register establishes *what* the pin does; X, Y, and Z carry the data it works with:

### X Register - Configuration and Parameters

The X register holds configuration parameters that define **how** the smart pin operates. Its meaning varies by mode:

| Mode Category | Typical X Usage |
|---------------|-----------------|
| Timing modes | Base period in clock cycles |
| Counter modes | Measurement window duration |
| Serial modes | Bit timing / baud rate parameters |
| ADC modes | Sample period and filter settings |

X is written via the **WXPIN** instruction. Some modes use only X[15:0]; others use the full 32 bits. Many modes also use X[31:16] for secondary parameters (frame period, initial phase, etc.).

### Y Register - Input Data or Secondary Configuration

The Y register holds:

- **Output data** for transmit modes (serial data to send)
- **Target values** for output modes (PWM duty cycle, DAC level)
- **Mode modifiers** for some input modes (sensitivity selection)

Y is written via the **WYPIN** instruction. For many modes, Y is updated repeatedly during operation to provide new output data or adjust behavior.

### Z Register - Accumulator and Results

The Z register is the smart pin's working register:

- **Accumulators** - Counting events, timing measurements
- **Phase accumulators** - NCO modes track phase in Z
- **Output buffers** - Results for cog to read

Z is read via **RDPIN** or **RQPIN**. Software cannot write Z directly—it is managed by the smart pin hardware.

### Register Initialization

When a smart pin is reset (DIR transitions from 1 to 0), the registers are initialized according to the mode. Specific initialization behavior is documented in each mode's chapter.


## 3.3 The IN Bit - Event Signaling

### Purpose of the IN Bit

Each smart pin has an **IN bit** that signals events to cogs. This is the same IN bit readable via TESTP/TESTPN, but its meaning changes when a smart pin mode is active.

In P_NORMAL mode (no smart pin):

- IN reflects the physical pin state

In smart pin modes:

- IN signals mode-specific events (data ready, measurement complete, overflow, etc.)

### When IN is Raised

Each mode defines when it raises IN:

| Mode Category | IN is raised when... |
|---------------|----------------------|
| Output modes | Cycle completes, buffer ready for new data |
| Measurement modes | Measurement period completes |
| Serial TX | Ready for next data word |
| Serial RX | Data word received |
| Counter modes | Measurement window expires |

### Acknowledging IN

When a cog interacts with a smart pin, the IN bit is **acknowledged** (lowered). This prepares the smart pin to signal the next event.

**Instructions that acknowledge:**

- WRPIN - Configure (also acknowledges)
- WXPIN - Write X (also acknowledges)
- WYPIN - Write Y (also acknowledges)
- RDPIN - Read Z and acknowledge
- AKPIN - Acknowledge without reading

**Instructions that do NOT acknowledge:**

- RQPIN - Read Z quietly (no acknowledge)

### Polling and the 2-Clock Delay

After an acknowledge, it takes **two clock cycles** before the IN bit can be polled again:

1. Cog executes RDPIN/AKPIN/etc. (acknowledges smart pin)
2. One clock elapses
3. Second clock elapses
4. IN can now be polled via TESTP

This timing matters in tight polling loops.

### RQPIN for Multi-Cog Access

The **RQPIN** (read quiet) instruction reads the Z register without acknowledging. This allows multiple cogs to read the same smart pin's result without interfering with each other. Only one cog should acknowledge; others can use RQPIN to observe.

::: caution
**Multi-cog bus collisions.** Every cog reaches each smart pin over a shared 34-bit bus for write data and acknowledgment, and the smart pin **OR**s the incoming buses from all cogs together — the same way DIR and OUT bits are OR'd before reaching a pin. So if two or more cogs issue **WRPIN, WXPIN, WYPIN, RDPIN, or AKPIN** to the *same* smart pin simultaneously, their bus data collides and corrupts. **RQPIN is the lone exception** — it does not use the acknowledge bus, so any number of cogs may RQPIN the same smart pin at once. Design multi-cog access so that only one cog configures and acknowledges a given smart pin; the others observe with RQPIN.
:::


## 3.4 The Smart Pin State Machine

Every smart pin follows a consistent state progression:

```{=latex}
\DiagPinStates
```

### State 1: Disabled (DIR=0)

When DIR=0, the smart pin is held in reset:

- The smart pin state machine is stopped
- IN is forced low
- Registers are initialized to mode-specific values
- Configuration instructions (WRPIN/WXPIN/WYPIN) are accepted

**Important:** Always issue WRPIN (mode/routing configuration) while DIR=0 — changing the mode word while the pin is running (DIR=1) can cause unpredictable behavior. WXPIN and WYPIN are different: they are the normal runtime update path and work freely while the smart pin is running (DIR=1).

### State 2: Configured

Configuration consists of up to three instructions:

1. **WRPIN** - Sets the mode and low-level pin configuration
2. **WXPIN** - Sets X register parameters
3. **WYPIN** - Sets Y register parameters (if mode uses Y)

Not all modes require all three. Some modes only need WRPIN; others need WRPIN + WXPIN; complex modes use all three.

### State 3: Enabled (DIR=1)

When DIR transitions from 0 to 1:

- The smart pin begins autonomous operation
- The state machine starts running
- Mode-specific behavior commences

The direction can be set via:

- DIRH - Set direction high (output mode)
- DRVH/DRVL - Set direction high with specific output state
- Note: For smart pins with P_OE set, output is enabled regardless of DIR

### State 4: Running

The smart pin operates autonomously:

- Generates outputs according to mode
- Measures inputs according to mode
- Updates Z register with results
- Raises IN when events occur

Cog interaction during running:

- Read results via RDPIN/RQPIN
- Update parameters via WXPIN/WYPIN
- Monitor events via TESTP

### Reset

To reset a smart pin without reconfiguring:

1. Clear DIR (DIRL or FLTL)
2. Set DIR (DIRH or DRVH/DRVL)

This restarts the smart pin with current configuration. No need to repeat WRPIN/WXPIN/WYPIN.

To completely disable and return to normal mode:

- Execute WRPIN with value 0 (or use PINCLEAR in Spin2)


## 3.5 Mode Bits and the 32 Modes

### Mode Selection via WRPIN

The smart pin mode is selected by bits [5:1] of the WRPIN D operand (bit 0 is always 0). With 5 bits, there are 32 possible modes (0-31, or %00000 through %11111).

| Mode Bits | Category |
|-----------|----------|
| %00000 | P_NORMAL - No Smart Pin mode |
| %00001-%00011 | Repository / DAC modes |
| %00100-%00101 | Pulse and Transition output |
| %00110-%00111 | NCO frequency and duty |
| %01000-%01010 | PWM modes |
| %01011 | Quadrature encoder |
| %01100-%01111 | Counter modes |
| %10000-%10010 | Timing measurement modes |
| %10011-%10111 | Period/frequency measurement |
| %11000-%11010 | ADC modes |
| %11011 | USB |
| %11100-%11111 | Serial TX/RX modes |

### Mode Constants

Spin2 and PASM2 provide named constants for each mode (P_NCO_FREQ, P_PWM_TRIANGLE, etc.). These constants have the mode bits properly positioned within the 32-bit WRPIN value.

### Mode Categories

**Output Modes (Chapters 6-11):**
Generate signals on the pin—pulses, waveforms, serial data.

**Input Modes (Chapters 12-17):**
Measure signals on the pin—timing, counting, frequency, analog levels.

**Special Modes (Chapters 18-19):**
Inter-cog data sharing (Repository) and USB.


## 3.6 The Layered Configuration Model

Smart pin configuration is layered. Multiple aspects combine to define complete behavior:

### Layer 1: Smart Pin Mode (bits [5:1])

Selects which of the 32 modes is active. Each mode defines fundamental behavior (PWM, ADC, serial, etc.).

### Layer 2: Low-Level Pin Configuration (bits [20:8])

Controls the analog characteristics of the pin:

- Input mode (logic, Schmitt, comparator, ADC)
- Drive strength (resistive or current source options)
- DAC configuration (when applicable)

These are the same settings documented in Chapter 2 (Enhanced Direct I/O).

### Layer 3: Input Routing (bits [31:24])

Selects input sources:

- A input source: local pin, adjacent pins (-3 to +3), or OUT bit
- B input source: local pin, adjacent pins (-3 to +3), or OUT bit
- Input polarity: true or inverted
- Input logic: pass, AND, OR, XOR, or filter

### Layer 4: DIR/OUT Control (bits [7:6])

The TT bits control output behavior:

- P_OE (%01): Output enabled regardless of DIR
- Without P_OE: DIR controls output enable

For smart pin output modes, P_OE is required.

### Combining Layers

Configuration constants from different layers are combined with OR:

```spin2
mode := P_NCO_FREQ | P_OE | P_HIGH_FAST | P_LOW_FAST
```

This combines:

- Smart pin mode (P_NCO_FREQ)
- Output enable (P_OE)
- Drive strength (P_HIGH_FAST, P_LOW_FAST)


## 3.7 When to Use Smart Pins

### Smart Pins Excel At

**Precise timing requirements:**

- Clock generation with exact frequencies
- PWM with consistent timing unaffected by software
- Pulse measurement with clock-cycle accuracy

**Continuous autonomous operation:**

- Free-running oscillators
- Ongoing signal measurement
- Serial communication without polling

**High-frequency signals:**

- MHz-range waveforms (limited only by sysclk)
- High baud-rate serial
- Fast ADC sampling

**Multi-channel parallel operation:**

- Every pin can run independently
- 64 simultaneous smart pin operations possible

### Direct I/O May Be Better For

**Simple on/off control:**

- LEDs, relays, simple outputs
- Occasional pin reads

**One-time or irregular operations:**

- Configuration signals
- Status reads

**Complex conditional logic:**

- Where software decision-making determines output
- Irregular patterns that don't fit smart pin modes

**Low pin count applications:**

- When cog cycles are abundant
- When flexibility outweighs hardware efficiency

### Hybrid Approaches

Many applications combine smart pins with Direct I/O:

- Smart pin for timing-critical signals (PWM, serial)
- Direct I/O for control signals (enable, reset, status)


## 3.8 Architectural Constraints

### One Mode Per Pin

Each pin can run exactly one smart pin mode at a time. To change modes:

1. Disable the smart pin (DIR=0)
2. Reconfigure with WRPIN
3. Re-enable (DIR=1)

### Z Register is Read-Only to Software

Software cannot directly write the Z register. Z is managed entirely by smart pin hardware. To "preset" a counter or phase, use the mode-specific mechanisms (often via X or Y registers, or by reset timing).

### Acknowledge Timing

The 2-clock delay after acknowledge means polling loops must account for this latency. Tight loops polling IN immediately after RDPIN will miss the first event.

### Mode-Specific Behaviors

Each mode has unique characteristics:

- Which registers are used
- When IN is raised
- What Z contains
- How reset behaves

These details are documented in each mode's chapter.


## 3.9 Chapter Summary

Smart pins provide autonomous I/O operations through:

1. **Three registers** (X, Y, Z) for configuration, input, and results
2. **The IN bit** for event signaling
3. **A state machine** progressing from disabled through configured to running
4. **32 modes** selected by bits [5:1] of WRPIN
5. **Layered configuration** combining mode, pin settings, input routing, and output control

The key insight: once configured and enabled, smart pins operate independently. The cog is free to perform other work, interacting with the smart pin only to read results or update parameters.


*This conceptual foundation applies to all smart pin modes. Proceed to Chapter 4 for the practical configuration process, or to Part II (Chapters 6-11) for specific output modes.*
