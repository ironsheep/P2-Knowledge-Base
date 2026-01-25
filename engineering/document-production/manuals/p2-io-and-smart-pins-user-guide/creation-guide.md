# P2 I/O & Smart Pins User Guide - Creation Guide

**Canonical Name:** `p2-io-and-smart-pins-user-guide`
**Document Title:** P2 I/O & Smart Pins User Guide

---

## 1. Document Identity

### 1.1 Purpose and Scope

This guide serves as the **complete practical reference** for the Propeller 2 pin I/O system. It covers three layers:

1. **Direct I/O** - Fundamental pin control via DIR/OUT/IN
2. **Enhanced Direct I/O** - P_ constants without Smart Pin modes
3. **Smart Pin Modes** - The 32 autonomous pin functions

**This document IS:**
- A complete reference for P2 pin I/O at all levels
- A practical guide for configuring pins for any task
- A task-oriented resource ("I need to do X" → here's how)
- Comprehensive coverage of ALL P_ constants and options
- Bilingual throughout (Spin2 + PASM2)

**This document is NOT:**
- A tutorial for learning from scratch (that's the Green Book)
- A replacement for silicon documentation (hardware truth)
- A beginner's first introduction to P2
- Limited to just Smart Pins (covers all I/O)

### 1.2 Target Audience

This guide serves multiple audiences with different entry points:

1. **New to P2 I/O** → Start with Part I (Direct I/O through Smart Pins)
2. **Know what they want to accomplish** → Use Intent Index (Appendix A)
3. **Need specific mode details** → Go directly to mode chapter
4. **Choosing between options** → Use comparison charts and decision guidance

### 1.3 Relationship to Other Documents

| Document | Purpose | Relationship |
|----------|---------|--------------|
| **This guide** | Complete I/O reference | Practical usage, all options |
| `p2-smart-pins-tutorial` | Green Book - learning | Pedagogical complement |
| `p2-assembly-language-manual` | PASM2 instruction reference | Covers pin *instructions* |
| Silicon documentation | Hardware truth | Authoritative for edge cases |

### 1.4 Source Materials

| Source | Location | Content |
|--------|----------|---------|
| Smart Pins catalog | `/engineering/ingestion/smart-pins-catalog/ingestionSources/` | Mode extracts |
| Spin2 v51 manual | `/engineering/ingestion/sources/spin2-v51/` | P_ constants, methods |
| P_ constants | `/engineering/ingestion/sources/spin2-v51/smartpin-symbols.txt` | Complete constant list |
| Silicon doc | `/engineering/ingestion/sources/silicon/` | Hardware behavior |
| John Titus extracts | `*/john-titus-extract.md` | Detailed mode docs |

---

## 2. Document Architecture

### 2.1 Overall Structure

```
FRONT MATTER
├── How to Use This Guide
├── Document Conventions
└── Quick Mode Selection Matrix

PART I: P2 PIN SYSTEM FUNDAMENTALS (~35-40 pages)
├── Chapter 1: Direct I/O - The Foundation
├── Chapter 2: Enhanced Direct I/O - Low-Level Pin Modes
├── Chapter 3: Smart Pin Architecture - Autonomous I/O
├── Chapter 4: Smart Pin Configuration
└── Chapter 5: Working with Smart Pins

PART II: OUTPUT MODES (simple → complex)
├── Chapter 6: Digital Output
├── Chapter 7: Pulse and Transition Generation
├── Chapter 8: Frequency Generation (NCO)
├── Chapter 9: PWM Output
├── Chapter 10: DAC Output
└── Chapter 11: Serial Transmit

PART III: INPUT MODES (simple → complex)
├── Chapter 12: Digital Input
├── Chapter 13: Timing Measurement
├── Chapter 14: Counting
├── Chapter 15: Quadrature Encoder
├── Chapter 16: Period and Frequency Measurement
├── Chapter 17: ADC (Analog Input)
└── Chapter 18: Serial Receive

PART IV: SPECIAL MODES
├── Chapter 19: Inter-COG Data Sharing (Repository)
└── Chapter 20: USB Host/Device

PART V: APPENDICES
├── Appendix A: Intent Index ("I want to...")
├── Appendix B: P_ Constants Quick Reference
├── Appendix C: Formulas Reference
├── Appendix D: Mode Comparison Charts
├── Appendix E: Troubleshooting
└── Appendix F: Complete Mode Reference

COMPREHENSIVE INDEX
```

### 2.2 Pedagogical Flow

The document supports three reading paths:

**Path 1: Learning (new to P2 I/O)**
```
Part I (all chapters) → Part II/III (as needed) → Appendices (reference)
```

**Path 2: Task-Oriented (know what to accomplish)**
```
Appendix A (Intent Index) → Specific chapter → Related considerations
```

**Path 3: Reference (know what mode)**
```
Appendix F (Mode Reference) or Chapter directly → Configuration details
```

---

## 3. Part I: Fundamentals Specification

### 3.1 Chapter 1: Direct I/O Entry Format

Each Direct I/O instruction/concept follows this format:

```
**INSTRUCTION_NAME - Brief Description**

[What it does in one sentence]

**Syntax:**
  INSTRUCTION  {parameters}

**Operation:**
  1. Step one
  2. Step two
  3. Step three

**Timing:** N clock cycles

**Spin2 Equivalent:** METHOD(params)

**Example - Spin2:**
[Working code with comments]

**Example - PASM2:**
[Working code with comments]

**Related:** INSTR1, INSTR2, INSTR3
```

### 3.2 Chapter 2: P_ Constant Group Format

Each constant group follows this format:

```
**CONSTANT GROUP NAME**

[What this group controls]

| Constant | Value | Effect | Use Case |
|----------|-------|--------|----------|
| P_XXX_A | %... | Effect | When to use |
| P_XXX_B | %... | Effect | When to use |
| ... | ... | ... | ... |

**Combining with other constants:**
  mode := P_XXX_A | P_YYY_B | P_ZZZ_C

**Considerations:**
- When to use option A vs B
- Tradeoffs between options
- Common combinations
```

### 3.3 Chapter 3-5: Smart Pin Concepts

These chapters explain the Smart Pin system without documenting individual modes. Focus on:
- What Smart Pins add over Direct I/O
- The state machine (reset → configure → run)
- How to combine P_ constants
- The X/Y/Z registers and IN flag
- Common patterns and debugging

---

## 4. Part II/III: Mode Entry Specification

### 4.1 Mode Chapter Structure

Each mode chapter (or section for related modes) follows this structure:

```
═══════════════════════════════════════════════════════════════════
MODE_NAME (P_CONSTANT, %XXXXX)
═══════════════════════════════════════════════════════════════════

**What it does:** [One paragraph explanation]

**Configuration Table:**

| Parameter | Value/Range | Description |
|-----------|-------------|-------------|
| Mode bits | %XXXXX | Mode selection |
| X register | [range/formula] | [what X controls] |
| Y register | [range/formula] | [what Y controls] |
| Z register | [description] | [what Z contains] |
| IN bit | [meaning] | [when IN is set] |
| OUT bit | [meaning] | [what OUT controls, if applicable] |

**Applicable P_ Constants:**

| Category | Constants | Notes |
|----------|-----------|-------|
| Output enable | P_OE | Required for output |
| Drive strength | P_HIGH_*, P_LOW_* | Match load requirements |
| Polarity | P_INVERT_OUT | Invert output if needed |
| Input routing | P_PLUS1_A, etc. | If using adjacent pin input |
| [other relevant] | [constants] | [notes] |

**Timing / Formulas:**
[Any timing formulas with worked examples]

**Example - Spin2:**
```spin2
' Complete working example
' With explanatory comments
' Showing all configuration steps
```

**Example - PASM2:**
```pasm2
' Complete working example
' With explanatory comments
' Showing all configuration steps
```

**Configuration Considerations:**

[Subsections covering all the choices:]

**[Topic 1]:**
- Option A: when to use, tradeoffs
- Option B: when to use, tradeoffs
- ...

**[Topic 2]:**
- ...

**Use Cases:**
- Use case 1
- Use case 2
- ...

**Related Modes:**
- P_XXX (%YYYYY) - [how it relates]
- P_ZZZ (%WWWWW) - [how it relates]
```

### 4.2 Multi-Mode Section Structure

When chapter covers multiple related modes (e.g., PWM modes):

```
═══════════════════════════════════════════════════════════════════
CHAPTER N: CATEGORY NAME
═══════════════════════════════════════════════════════════════════

**Overview:** [What this category of modes does]

**Available Modes:**
- Mode A (P_XXX, %XXXXX) - brief description
- Mode B (P_YYY, %YYYYY) - brief description
- ...

---

## N.1 Mode A (P_XXX, %XXXXX)
[Full mode entry per 4.1]

---

## N.2 Mode B (P_YYY, %YYYYY)
[Full mode entry per 4.1]

---

## N.X Choosing Between Modes

| Feature | Mode A | Mode B | Mode C |
|---------|--------|--------|--------|
| Feature 1 | ✓ | ✗ | ✓ |
| Feature 2 | ✗ | ✓ | ✓ |
| ... | ... | ... | ... |

**Decision Guide:**
- Use Mode A when: [criteria]
- Use Mode B when: [criteria]
- ...
```

### 4.3 Required Content Checklist

Every mode entry MUST include:

- [ ] One-paragraph description
- [ ] Complete configuration table (all registers)
- [ ] ALL applicable P_ constants listed
- [ ] Working Spin2 example (compiles with FlexProp)
- [ ] Working PASM2 example (compiles with pnut_ts)
- [ ] Configuration considerations (all choices explained)
- [ ] Use cases
- [ ] Related modes

---

## 5. Appendix Specifications

### 5.1 Appendix A: Intent Index

Format:
```
**I want to... [task]**
→ Chapter N: [chapter name]
→ Specifically: [mode or technique]
→ Also consider: [alternatives]
```

Categories to cover:
- Generate signals (clock, PWM, analog, serial)
- Measure signals (timing, counting, analog, serial)
- Control outputs (digital, DAC)
- Read inputs (digital, ADC)
- Communicate (SPI, I²C, UART, USB)
- Coordinate (multi-pin, multi-COG)

### 5.2 Appendix B: P_ Constants Reference

Complete table of all constants:
```
| Constant | Value | Category | Description |
|----------|-------|----------|-------------|
| P_XXX | %... | Category | What it does |
```

Grouped by category, with cross-references to chapters that use them.

### 5.3 Appendix C: Formulas Reference

All formulas in one place:
```
**NCO Frequency:**
  frequency = (Y × sysclk) / 2³²
  Y = (frequency × 2³²) / sysclk

**Worked Example:**
  For 1 kHz at 200 MHz sysclk:
  Y = (1000 × 4,294,967,296) / 200,000,000 = 21,475
```

### 5.4 Appendix D: Mode Comparison Charts

Visual comparison matrices:
```
**Output Modes Comparison:**

| Mode | Freq Range | Resolution | Duty Control | Use Case |
|------|------------|------------|--------------|----------|
| NCO Freq | ... | ... | 50% only | Clocks |
| NCO Duty | ... | ... | Variable | ... |
| PWM Tri | ... | ... | Variable | Motors |
| ... | ... | ... | ... | ... |
```

---

## 6. Content Verification Protocol

### 6.1 Claim Types and Sources

| Claim Type | Required Source |
|------------|-----------------|
| Direct I/O behavior | Silicon doc, PASM2 manual |
| P_ constant values | Spin2 v51 smartpin-symbols.txt |
| Smart Pin mode behavior | Silicon doc + Titus extract |
| Register function | Silicon doc |
| Timing | Silicon doc |
| Examples | Must compile and test |

### 6.2 Verification Checklist

Before writing any claim:
1. What am I claiming?
2. Which source contains this?
3. Can I cite the exact location?
4. Does source say this EXACTLY?
   - YES → Write the claim
   - NO → Don't write, or mark as unverified

### 6.3 Red-Flag Phrases

Stop and verify when about to write:
- "automatically synchronizes" → Citation required
- "eliminates" → Citation required
- "also provides" → Verify capability exists
- "side effect of" → Must be documented

---

## 7. Code Example Requirements

### 7.1 All Examples Must

1. **Compile** - Spin2 with FlexProp, PASM2 with pnut_ts
2. **Be complete** - Not fragments, runnable as-is
3. **Be realistic** - Use real values with explanations
4. **Be commented** - Explain what AND why
5. **Show both languages** - Spin2 AND PASM2

### 7.2 Spin2 Example Template

```spin2
' [Mode/Feature Name] - [Brief description]
' [What this example demonstrates]
CON
  _clkfreq = 200_000_000      ' System clock frequency
  PIN = 0                      ' Pin assignment
  [other constants with explanations]

VAR
  [variables if needed]

PUB main() | [locals]
  ' Configure [what]
  WRPIN(PIN, mode_value)       ' [Explain mode value]
  WXPIN(PIN, x_value)          ' [Explain X register purpose]
  WYPIN(PIN, y_value)          ' [Explain Y register purpose]
  DRVL(PIN)                    ' Enable Smart Pin
  
  ' [Main operation]
  [code with comments explaining each step]
```

### 7.3 PASM2 Example Template

```pasm2
' [Mode/Feature Name] - [Brief description]
' [What this example demonstrates]
CON
  _clkfreq = 200_000_000

DAT           org

' Configuration
              wrpin     pin, ##mode_value   ' [Explain]
              wxpin     pin, ##x_value      ' [Explain]
              wypin     pin, ##y_value      ' [Explain]
              drvl      pin                 ' Enable Smart Pin

' Main operation
[code with comments]

' Data
pin           long      0
[other data with explanations]
```

---

## 8. Quality Requirements

### 8.1 Completeness Checklist

For each mode/topic:
- [ ] All configuration parameters documented
- [ ] ALL applicable P_ constants listed
- [ ] ALL options shown (not just common ones)
- [ ] Working Spin2 example
- [ ] Working PASM2 example
- [ ] Considerations section with all choices
- [ ] Decision guidance when multiple options
- [ ] Cross-references to related content

### 8.2 Accuracy Checklist

- [ ] Values verified against source documents
- [ ] Formulas verified with worked examples
- [ ] Examples tested with compilers
- [ ] Terminology matches canonical terms
- [ ] No fabricated capabilities

### 8.3 Voice Checklist

- [ ] Third person throughout
- [ ] No hedging ("may", "might", "typically")
- [ ] No tutorial voice ("you", "we", "let's")
- [ ] Definitive statements only
- [ ] All options presented, not just favorites

---

## 9. Production Workflow

### 9.1 Chapter Development Process

1. **Research** - Gather all source material for topic
2. **Outline** - List all subtopics and options
3. **Draft** - Write following entry templates
4. **Verify** - Check all claims against sources
5. **Examples** - Write and test Spin2 + PASM2
6. **Review** - Apply quality checklists
7. **Cross-reference** - Link to related content

### 9.2 PDF Generation

- **Workspace:** `/engineering/document-production/workspace/p2-io-and-smart-pins-user-guide/`
- **Outbound:** `/engineering/document-production/outbound/p2-io-and-smart-pins-user-guide/`
- **Template:** To be created (may inherit from Smart Pins Tutorial)

---

## 10. Summary: The Content Equation

```
Content = Complete Options + Verified Claims + Working Examples + Decision Guidance
```

**Every topic must provide:**
- ALL configuration options (not just common ones)
- ALL applicable P_ constants
- Claims verified against sources
- Working code in BOTH languages
- Guidance for choosing between options
- Cross-references to related content

**The result:**
A comprehensive reference that answers any P2 I/O question with complete, accurate, practical information.

---

*Last Updated: 2026-01-24*
*Version: 2.0 - Expanded scope: Direct I/O + Smart Pins*
