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
- State a known value as a known value: "sets" not "typically sets" — **where the
  behavior is in fact fixed.** Where it genuinely varies, the qualifier is required
  accuracy, not hedging (§3.4, R1)

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
| Never write **vague** hedging | "The pin might be driven" ❌ | Creates ambiguity about what the silicon does. **NOT the same as a calibrated qualifier — see §3.4 (R1).** |
| Never use first person | "We configure the pin..." ❌ | Tutorial voice |
| Never use second person | "You should set..." ❌ | Tutorial voice |
| Never be conversational | "Let's explore..." ❌ | Tutorial voice |
| Never minimize | "Simply set the mode" ❌ | Dismissive |
| Never omit options | "Use P_HIGH_FAST" (only) ❌ | Incomplete |
| Never assume context | "As you know..." ❌ | Must stand alone |

**These rows carry carve-outs — read §3.5 before acting on a hit.** Several were
measured against the body and narrowed; a hit that falls inside a recorded carve-out is
not a defect.

### 3.3 Voice Comparison

| Aspect | Smart Pins Tutorial (retired) | This User Guide |
|--------|---------------------|-----------------|
| Person | Second ("you") | Third (instruction/mode names) |
| Tone | Warm, encouraging | Authoritative, comprehensive |
| Coverage | Selected examples | ALL options |
| Vague hedging | Occasional | Never |
| Calibrated qualifiers (§3.4, R1) | Occasional | **Required where evidence is partial** |
| Celebration | Yes ("Well done!") | Never |
| Questions | Yes ("Why?") | No |
| Decision guidance | Occasional | Systematic |

### 3.4 The four house rules — this guide's declaration

The rules themselves are stated once, in
`engineering/standards/documentation-standards/documentation-voices-catalog.md`
("The Shared Discipline — the four house rules"). This section states what *this*
guide does about them. It does not restate them.

| rule | decision | how it applies here |
|------|----------|---------------------|
| **R1** Calibrated confidence | **ADOPT** | **Never state a claim above its evidence** — and note that this *corrects* the older blanket "never hedge" rule, which is why §3.2 and §3.3 above are scoped rather than absolute. A qualifier that reflects the true state of the evidence is **accuracy**, and it is **required** wherever the bare claim would overstate. See §3.4.1 for what this looks like in the I/O domain. |
| **R2** The payoff-sentence test | **ADOPT** | Strip the flourish off any section- or callout-closing sentence and read what remains as a bare claim; satisfy it from the *Propeller 2 Documentation v35* / the KB YAML, or cut it. Highest risk in the "Considerations" sections (§4.4), which are the only argument-driven prose in an otherwise tabular document. |
| **R3** Anti-pattern family | **ADOPT — adapted** | *Tutorial filler* and *reader-as-foil* are already covered by §3.2's bans on conversational voice, second person, and "As you know…". **Newly added here:** *self-admiration* (no praising a mode as "elegant" or a mechanism as "the single most powerful") and *staged reveal* (no withholding a mode's real constraint until after the example). All four are consistent with an authoritative third-person register. |
| **R4** Cadence budget | **ADOPT — as a forward guard** | A reference document with a mode-per-chapter structure is not the class that produces the metronome defect, so near-zero legacy findings are expected. Adopted so that new prose — chapter openers and Considerations sections — cannot drift into it. **Confirm by measurement, not by assumption, in either direction.** |

#### 3.4.1 R1 in the I/O domain — the distinction, shown

The rule is about **the defect, not the words.** There is no banned-word list, and a
checklist that names `may / might / typically` is always wrong: those words are R1
compliance as often as they are defects.

| ❌ vague hedging — avoids commitment on a fact we know | ✅ calibrated — states exactly what the evidence supports |
|---|---|
| "The pin might be driven." | "DRVH drives the pin high." *(The behavior is fixed; say so.)* |
| "WRPIN typically sets the mode bits." | "WRPIN sets mode bits D[4:0]." *(Fixed; say so.)* |
| "Settling is usually fast enough." | "Settling takes 2 clocks after the mode write; add margin above 250 MHz, where this has not been characterized." *(Partial evidence; the qualifier is where the honesty lives.)* |
| "This mode should work with most sensors." | "This mode is documented for sensors presenting a rail-to-rail output; behavior with a biased output is undocumented." |

**The test:** ask *what does the evidence actually support?* If the answer is a firm
fact, state it firmly. If the answer is "this much and no further", say that much — and
saying it is not hedging, it is the claim being true.

### 3.5 Carve-outs and adjudications — decided against the body, 2026-08-17

The first full conformance pass over the master (Sprint 2, «#246») read every
declared-row hit in context. Where a row fought the document and the **document** was
right, the row was corrected — that is what the following records. **A carve-out here is
a decision, not an oversight: do not "fix" against it.**

| # | Row | Decision |
|---|-----|----------|
| C-1 | §3.1/§3.2/§3.3 **person** | **Carve-out: front matter and the CHANGELOG are out of scope.** The CC-BY-SA license text ("You are free to…") is quoted legal boilerplate and is reproduced verbatim; the Acknowledgements are an author's-voice page; the CHANGELOG is governed by the changelog style guide, not this one. The person rules govern the **reference body** — where the master is now third-person throughout. |
| C-2 | §5.1 **"Smart Pin — Title case"** | **Adjudicated — the row was wrong.** The body carries ~155 lowercase "smart pin" against a handful of Title-case uses, and lowercase is what house style does with a common-noun device name (compare "cog"). **Title Case in titles and headings; lowercase "smart pin" in running prose.** What the row actually bans is the closed-up and camel forms — `smartpin`, `SmartPin` — of which the body has zero. |
| C-3 | §5.2 **"PASM2 instructions: Bold uppercase"** | **Adjudicated — superseded by platform policy (2026-06-29).** Mnemonics render **UPPERCASE, not bold**: uppercase carries the mnemonic's identity and matches its appearance in code, and bold stays reserved for genuine emphasis. This guide's manual is the origin document for `p2kb-platform-mnemonic-bold`, which applies it grammar-aware at render. Authors write mnemonics plainly; do **not** hand-bold them. |
| C-4 | §3.2 **"Never minimize"** | **Carve-out: "just" / "simply" meaning *merely*.** Eleven hits across the master, **zero** violations — every one describes what the hardware does ("a later WXPIN simply overwrites the long") or means *only* ("just before the B-input edge"). The row's defect is **dismissing the reader's effort**, not the adverb. Read the hit; do not sweep the word. |
| C-5 | §5.1 **`sysclk`** | **Carve-out: "system clock" is correct as the English noun.** The row governs the **frequency reference** — write `sysclk` for the value. "System clock" naming the clock itself or its cycles ("counts system clocks while A-input is high") is right, and the body already uses both precisely in the same sentence where both are meant. |
| C-6 | **R4** cadence budget | **Measured, not assumed — passes.** Across 827 sections, **7%** of closings land a rhetorical beat (budget ~50%), longest consecutive run **3** (limit ~4). The hits are **earned beats** carrying real information — silicon caveats, dependency notes, cross-references — and the per-chapter "This chapter covers…" / closing italic line is a **declared refrain**, which is structure, not a beat. Do not flatten either. §3.4's forward-guard prediction is confirmed for this document class. |
| C-7 | **R3** anti-pattern family | **Clean.** Zero self-admiration and zero tutorial filler in the body. *Staged reveal* is prevented structurally: every mode section runs Function → Operation → Configuration → Example, so a mode's real constraint (clock routing, data justification, the Z preload) lands **before** the example that would trip on it. |

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
- [ ] No tutorial voice
- [ ] **Voice rules R1–R4 satisfied — see §3.4.** (This item points; it does not
      re-encode. A checklist that restates a rule in its own words becomes a
      counter-order the moment the rule is refined.)

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
- Definitive where the evidence is definitive; calibrated where it is partial (§3.4, R1)
- Third person, no tutorial voice
- Both languages (Spin2 + PASM2) always
- "When to use" guidance throughout
- All P_ constants documented for each mode

**The result:**
A complete reference that answers "how do I control P2 pins?" at every level - from basic digital I/O through sophisticated Smart Pin modes - with all configuration options clearly presented.

---

*Last Updated: 2026-08-17*
*Version: 2.2 — §3.5 carve-outs and adjudications from the first full conformance pass over the master*

**Conformance baseline:** the opus-master was measured against every declared row in
§3.2–§3.4 on **2026-08-17**, at master state **post-v1.0.8**. Prose surface only —
these rules do not govern instruction tables, register layouts, code blocks, or
quick-reference matter. Extend this baseline forward as the master changes; do not
re-derive it.
