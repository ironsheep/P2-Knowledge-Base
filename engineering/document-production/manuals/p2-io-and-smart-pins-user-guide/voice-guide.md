# P2 I/O & Smart Pins User Guide - Voice Guide

**Document:** P2 I/O & Smart Pins User Guide
**Purpose:** Define the writing voice and tone for consistent, authoritative I/O system reference

---

## 1. Voice Philosophy

### 1.1 The Guiding Principle

> **This guide tells you exactly how to control P2 pins - from simple digital I/O through autonomous Smart Pin modes - with all the configuration options laid out clearly.**

This is a **practical reference** that supports multiple entry points:
- "I'm new to P2 I/O" → Start with Direct I/O chapters
- "I know what I want to accomplish" → Use the Intent Index
- "I need details on a specific mode" → Go directly to that chapter

The voice must be:
- **Authoritative** - This is the source of truth for P2 I/O
- **Precise** - No ambiguity about configurations or behavior
- **Comprehensive** - All options presented, not just common ones
- **Practical** - Focused on how to accomplish real tasks

### 1.2 Scope: Three Layers of I/O

This guide covers the complete P2 pin I/O system:

```
Layer 2: Smart Pin Modes (%00001-%11111)
         └── Autonomous functions (NCO, PWM, ADC, Serial, etc.)
         
Layer 1: Enhanced Direct I/O (P_NORMAL + P_ constants)
         └── Drive strength, Schmitt trigger, comparators, basic DAC/ADC
         
Layer 0: Pure Direct I/O (DIR/OUT/IN)
         └── Fundamental bit-level pin control
```

The voice is consistent across all layers - same precision, same format, same thoroughness.

---

## 2. Voice Characteristics

### 2.1 Technical Precision

**Direct I/O example:**
```
DRVH sets DIR to 1 and OUT to 1, driving the pin high. The instruction
executes in 2 clock cycles. The pin begins driving on the clock cycle
following instruction completion.
```

**Smart Pin example:**
```
Configure WRPIN with mode bits [4:0] = %11110 for asynchronous serial
transmit. X[31:16] sets the bit period in sysclk cycles. X[4:0] sets
the bit count minus one (0-31 for 1-32 bits).
```

- Exact terminology throughout
- Specific values and ranges
- No hedging: "sets" not "typically sets"

### 2.2 Structured Predictability

Every Direct I/O instruction and every Smart Pin mode follows consistent format:
- What it does (one sentence)
- Configuration details (all parameters)
- All applicable P_ constants
- Spin2 + PASM2 examples
- Use cases and considerations

### 2.3 Comprehensive Coverage

For every topic, present ALL options:

**Drive Strength (don't just mention one):**
```
Drive-High Options:
- P_HIGH_FAST (default) - 30mA fast drive
- P_HIGH_1K5 - 1.5kΩ resistive drive
- P_HIGH_15K - 15kΩ resistive drive (pull-up)
- P_HIGH_150K - 150kΩ resistive drive (weak pull-up)
- P_HIGH_1MA - 1mA current source
- P_HIGH_100UA - 100μA current source
- P_HIGH_10UA - 10μA current source
- P_HIGH_FLOAT - Float (no drive)
```

### 2.4 Task-Oriented Guidance

Include "when to use" and "considerations" throughout:

```
**When to use P_HIGH_15K:**
- Creating a pull-up for open-drain bus (I²C)
- Default-high input with external pull-down switch
- Reducing EMI on slow-changing signals

**When NOT to use:**
- High-speed signals (use P_HIGH_FAST)
- Driving capacitive loads (rise time too slow)
```

---

## 3. Voice Rules

### 3.1 Always Do

| Rule | Example |
|------|---------|
| Use definitive statements | "DRVH drives the pin high" ✅ |
| Be specific about values | "X[4:0] = bits minus 1 (0-31)" ✅ |
| List ALL options | Show all 8 drive strengths, not just 2 ✅ |
| Include timing where relevant | "Executes in 2 clock cycles" ✅ |
| Show both Spin2 and PASM2 | Every example in both languages ✅ |
| Cross-reference related content | "See also: DRVL, DRVNOT" ✅ |
| Use third person | "The instruction performs..." ✅ |

### 3.2 Never Do

| Rule | Bad Example | Why |
|------|-------------|-----|
| Never hedge | "The pin might be driven" ❌ | Creates ambiguity |
| Never use first person | "We configure the pin..." ❌ | Tutorial voice |
| Never use second person | "You should set..." ❌ | Tutorial voice |
| Never be conversational | "Let's explore..." ❌ | Tutorial voice |
| Never minimize | "Simply set the mode" ❌ | Dismissive |
| Never omit options | "Use P_HIGH_FAST" (only) ❌ | Incomplete |
| Never assume context | "As you know..." ❌ | Must stand alone |

### 3.3 Voice Comparison

| Aspect | Green Book Tutorial | This User Guide |
|--------|---------------------|-----------------|
| Person | Second ("you") | Third (instruction/mode names) |
| Tone | Warm, encouraging | Authoritative, comprehensive |
| Coverage | Selected examples | ALL options |
| Hedging | Occasional | Never |
| Celebration | Yes ("Well done!") | Never |
| Questions | Yes ("Why?") | No |
| Decision guidance | Occasional | Systematic |

---

## 4. Section-Specific Voice

### 4.1 Direct I/O Instructions

```
**DRVH - Drive High**

Drives pin high by setting DIR=1 and OUT=1.

**Syntax:**
  DRVH  {#}D

**Operation:**
  1. Set DIR bit for pin D to 1 (output mode)
  2. Set OUT bit for pin D to 1 (high state)
  3. Pin begins driving high on next clock

**Timing:** 2 clock cycles

**Spin2 Equivalent:** PINHIGH(pin)

**Related:** DRVL, DRVNOT, DRVC, DRVNC, OUTH, DIRH
```

### 4.2 P_ Constant Groups

```
**Drive-High Strength Constants**

These constants set the high-side drive characteristics. Combine with
a drive-low constant to set both directions.

| Constant | Value | Drive | Use Case |
|----------|-------|-------|----------|
| P_HIGH_FAST | %...000... | 30mA | High-speed digital signals |
| P_HIGH_1K5 | %...001... | 1.5kΩ | Moderate current limiting |
| P_HIGH_15K | %...010... | 15kΩ | Pull-up resistor |
| P_HIGH_150K | %...011... | 150kΩ | Weak pull-up |
| P_HIGH_1MA | %...100... | 1mA | Current source |
| P_HIGH_100UA | %...101... | 100μA | Low-power pull-up |
| P_HIGH_10UA | %...110... | 10μA | Very low power |
| P_HIGH_FLOAT | %...111... | Float | Open-drain output |

**Combining constants:**
  mode := P_HIGH_15K | P_LOW_FLOAT  ' Open-drain with pull-up
```

### 4.3 Smart Pin Mode Entries

```
**NCO Frequency Mode (P_NCO_FREQ, %00110)**

Generates a precise square wave using numerically-controlled oscillation.

**Configuration:**

| Parameter | Value/Range | Description |
|-----------|-------------|-------------|
| Mode bits | %00110 | NCO Frequency mode |
| X[15:0] | 1-65535 | Base period in sysclk cycles |
| X[31:16] | 0-65535 | Initial phase (0-65535 = 0°-360°) |
| Y[31:0] | 1 to 2³²-1 | Frequency control value |
| Z[31:0] | (accumulator) | Phase accumulator, Z[31] drives output |
| IN bit | Set on overflow | Indicates frequency cycle complete |

**Frequency Formula:**
  frequency = (Y × sysclk) / 2³²
  
  Solving for Y:
  Y = (frequency × 2³²) / sysclk

**Applicable P_ Constants:**
- P_OE - Output enable (required for output)
- P_INVERT_OUT - Invert output polarity
- P_HIGH_* / P_LOW_* - Drive strength selection
- Input routing (P_PLUS1_A, etc.) - Not typically used

**Considerations:**
- Best frequency resolution with X[15:0] = 1
- Trade resolution for update rate with larger X
- X[31:16] enables phase synchronization between multiple pins
- Combine with P_DAC_* constants for analog output

**Spin2 Example:**
[complete example]

**PASM2 Example:**
[complete example]

**Use Cases:**
- Clock generation
- Audio tone synthesis
- Local oscillators
- Phase-locked multi-pin signals

**Related Modes:** P_NCO_DUTY (%00111), P_TRANSITION (%00101)
```

### 4.4 Considerations Sections

Every mode chapter includes a "Considerations" section:

```
**Configuration Considerations**

When implementing async serial TX, consider:

**Baud Rate Accuracy:**
- X[31:16] = sysclk / baud provides integer division
- X[15:10] adds fractional bits for higher accuracy
- At 200 MHz sysclk, 115200 baud: X[31:16] = 1736, error < 0.1%
- Verify tolerance matches receiver requirements

**Drive Strength:**
- P_HIGH_FAST / P_LOW_FAST - Standard CMOS levels, short traces
- P_HIGH_1K5 / P_LOW_1K5 - Current limiting for protection
- Consider cable length and termination requirements

**Polarity:**
- TTL/CMOS: P_TRUE_OUT (idle high, start bit low)
- RS-232: P_INVERT_OUT (idle low after level shifter)

**Multi-Drop (RS-485):**
- Use separate pin for drive enable
- Coordinate with P_TRANSITION for timed disable after transmission
```

---

## 5. Terminology Standards

### 5.1 Canonical Terms

| Canonical Term | NOT These | Notes |
|----------------|-----------|-------|
| Direct I/O | basic I/O, simple I/O | The fundamental layer |
| Smart Pin | smartpin, SmartPin | Title case, two words |
| DIR bit | direction bit | Direction control |
| OUT bit | output bit | Output state |
| IN bit | input bit | Input/status |
| X register | X value, X field | Smart Pin register |
| Y register | Y value, Y field | Smart Pin register |
| Z register | Z value, accumulator | Smart Pin register |
| mode bits | mode field | Bits [4:0] in WRPIN |
| sysclk | system clock | Clock frequency reference |
| P_ constant | pin constant | Configuration constant |

### 5.2 Instruction/Method References

- **PASM2 instructions:** Bold uppercase: "The **DRVH** instruction..."
- **Spin2 methods:** Bold mixed case: "The **PINHIGH** method..."
- **P_ constants:** Monospace: `P_NCO_FREQ`, `P_HIGH_15K`
- **In code blocks:** Plain text, all caps for PASM2

### 5.3 Register Field Notation

- Bit ranges: "X[15:0]" for bits 15 through 0
- Full register: "the X register"
- Specific bits: "bit 31 of Z"
- Mode value: "%00110" with percent prefix

---

## 6. Quality Checklist

Before finalizing any section, verify:

### Voice Consistency
- [ ] Third person throughout
- [ ] No hedging language
- [ ] No tutorial voice
- [ ] Definitive statements only

### Completeness
- [ ] ALL options listed (not just common ones)
- [ ] ALL applicable P_ constants mentioned
- [ ] Both Spin2 and PASM2 examples
- [ ] Considerations section included
- [ ] Cross-references to related content

### Accuracy
- [ ] Values verified against sources
- [ ] Formulas correct and tested
- [ ] Examples compile and run
- [ ] Timing information verified

---

## 7. Summary

```
Voice = Authoritative + Comprehensive + Practical
```

**Core principles:**
- Every option presented, not just common ones
- Definitive statements, no hedging
- Third person, no tutorial voice
- Both languages (Spin2 + PASM2) always
- "When to use" guidance throughout
- All P_ constants documented for each mode

**The result:**
A complete reference that answers "how do I control P2 pins?" at every level - from basic digital I/O through sophisticated Smart Pin modes - with all configuration options clearly presented.

---

*Last Updated: 2026-01-24*
*Version: 2.0 - Expanded scope: Direct I/O + Smart Pins*
