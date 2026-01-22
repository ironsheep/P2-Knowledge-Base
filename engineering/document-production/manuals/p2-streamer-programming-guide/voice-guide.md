# P2 Streamer Programming Guide - Voice Guide

**Document:** P2 Streamer Programming Guide  
**Purpose:** Define writing voice and tone for consistent, authoritative technical reference  
**Created:** 2026-01-22

---

## 1. Voice Philosophy

### 1.1 The Guiding Principle

> **This manual tells you exactly how the streamer works, what every mode does, and precisely how to configure it - when you already understand P2 basics and need to implement high-speed I/O.**

This is a **technical reference** for an advanced hardware feature. The voice must be:
- **Authoritative** - This is the source of truth for streamer operation
- **Precise** - No ambiguity about modes, bit fields, or timing
- **Efficient** - Dense information for developers who know what they need
- **Practical** - Real examples showing actual usage patterns

### 1.2 Pedagogical Grounding

These voice choices are grounded in learning theory adapted for reference documentation. See `creation-guide.md`, Section 3 (Pedagogical Framework) for the research basis:

- **Consistent structure** reduces cognitive load (Sweller, 1988)
- **Multiple representations** (tables, prose, code) support dual coding (Paivio, 1971)
- **Dense information** rewards expertise through repeated use
- **Pattern recognition** through identical entry formats accelerates lookup

Unlike tutorial manuals, reference documents serve learning through **repeated retrieval** - the hundredth lookup should take seconds, not minutes.

### 1.3 Target Audience

The Streamer Programming Guide serves developers who:
- Already understand P2 COG/Hub architecture
- Need to implement video output, high-speed I/O, or signal processing
- Want quick lookup of modes, constants, and configurations
- May be porting code or debugging streamer-based systems

**This is NOT a tutorial.** Readers should already understand:
- Basic P2 instruction set
- Hub memory and FIFO operations (RDFAST/WRFAST)
- Pin configuration concepts
- DAC fundamentals

---

## 2. Voice Characteristics

### 2.1 What We DO Say

| Pattern | Example |
|---------|---------|
| Definitive statements | "The NCO rolls over when the MSB becomes set" |
| Precise specifications | "D[27:24] selects DAC channel routing" |
| Clear constraints | "Pin output requires D[23] = 1" |
| Practical guidance | "For 25 MHz pixel rate at 250 MHz clock, use $0CCC_CCCD" |
| Direct comparisons | "XZERO zeros the phase; XCONT preserves it" |

### 2.2 What We DON'T Say

| Avoid | Why | Instead |
|-------|-----|---------|
| "Let's explore the streamer..." | Tutorial voice | "The streamer provides..." |
| "You might wonder why..." | Hedging | State the fact directly |
| "Simply configure..." | Dismissive of complexity | "Configure..." |
| "Basically, it works like..." | Vague | Precise description |
| "Congratulations!" | Tutorial celebration | (omit) |

### 2.3 Voice Comparison

| Aspect | DeSilva Tutorial | This Reference |
|--------|------------------|----------------|
| Person | Second ("you") | Third (component names) |
| Tone | Warm, encouraging | Authoritative, precise |
| Hedging | Occasional | Never |
| Examples | Progressive, extensive | Targeted, illuminating |
| Celebration | Yes ("Uff!") | Never |
| Questions | Yes ("Why?") | No |
| Asides | Yes | Rarely, only for critical warnings |

---

## 3. Enhancement Markers

### 3.1 Warning Types

Use these markers for important developer guidance:

| Marker | When to Use | Example |
|--------|-------------|---------|
| **⚠️ Pitfall:** | Common mistakes with non-obvious consequences | "⚠️ **Pitfall:** Forgetting RDFAST before RFBYTE modes causes unpredictable data" |
| **💡 Tip:** | Non-obvious techniques or optimizations | "💡 **Tip:** Use XZERO at line start to prevent phase drift accumulation" |
| **🔧 Hardware:** | Silicon-level details affecting usage | "🔧 **Hardware:** NCO frequency +1 ensures correct initial rollover timing" |

### 3.2 When to Add Enhancements

**Add ⚠️ Pitfall when:**
- A common mistake causes silent failure
- Mode requires specific prerequisites (RDFAST/WRFAST setup)
- Bit field has non-intuitive meaning
- Timing requirements are critical

**Add 💡 Tip when:**
- A technique isn't obvious from specs alone
- Performance can be significantly improved
- Mode combinations create powerful patterns
- Frequency calculation has a shortcut

**Add 🔧 Hardware when:**
- NCO behavior has implementation details
- DAC channels have specific pin requirements
- Timing affects other cog resources
- Integration with other hardware (colorspace converter, pixel mixer)

---

## 4. Terminology Standards

### 4.1 Canonical Terms

Use these terms consistently:

| Canonical Term | NOT These | Notes |
|----------------|-----------|-------|
| NCO | oscillator, clock | Numerically-Controlled Oscillator |
| rollover | overflow, trigger | When NCO MSB becomes set |
| command | instruction, setup | The D operand to XINIT/XCONT/XZERO |
| count | duration, length | The D[15:0] field |
| mode | type, format | The D[31:28] field |
| phase | position, state | NCO accumulator value |
| streamer | DMA, transfer unit | The hardware component |

### 4.2 Instruction Formatting

| Context | Format | Example |
|---------|--------|---------|
| In prose | Bold uppercase | "The **XINIT** instruction..." |
| In lists | Uppercase, no bold | XINIT, XCONT, XZERO |
| In code | Uppercase | `XINIT mode, data` |

### 4.3 Bit Field Notation

- Use brackets: "D[31:28]" "S[19:16]"
- Binary with underscores: `%1011_0000_0000_0101`
- Hex with prefix: `$B0850000`
- Symbols in monospace: `X_RFWORD_RGB16`

---

## 5. Section-Specific Voice

### 5.1 Mode Descriptions

One paragraph, precise function:

```
✅ "RFBYTE modes read single bytes from hub memory via the RDFAST 
    FIFO and output them to pins and/or DAC channels at the NCO rate."

❌ "Let's explore how RFBYTE modes work. They're pretty interesting 
    because they read bytes..." (tutorial voice)
```

### 5.2 Configuration Tables

Dense, scannable format:

```
✅ | Mode | Symbol | Pins | DACs | Description |
   |------|--------|------|------|-------------|
   | 1000 | X_RFBYTE_1P_1DAC1 | 1 | 1 | RFBYTE to 1 pin, 1 DAC |

❌ "The first mode we'll look at is mode 1000, which..." (narrative)
```

### 5.3 Code Examples

Show *why*, not just *what*:

```pasm2
✅ ' VGA horizontal sync - XZERO resets phase for line timing
           xcont    m_bs, sync0      ' 16 pixels before sync
           xzero    m_sn, sync1      ' 96 pixels of sync (phase zeroed)
           xcont    m_bv, sync0      ' 48 pixels before visible

❌          xcont    m_bs, sync0      ' Sync
           xzero    m_sn, sync1      ' Sync
           xcont    m_bv, sync0      ' Sync
   (Comments just restate instruction names)
```

### 5.4 Parameter Lists

Precise constraints:

```
✅ • D[31:28] - Mode selector (0-15), determines data source and destination
   • D[27:24] - DAC routing (see DAC Channel Configuration)
   • D[23] - Pin enable (%e) or Write enable (%w) depending on mode

❌ • D - The command register (vague)
   • S - Where data comes from (incomplete)
```

---

## 6. Document Structure Voice

### 6.1 Section Introductions

Brief, purposeful:

```
✅ "The streamer's NCO times all operations. Understanding NCO 
    frequency calculation is essential for correct pixel rates."

❌ "Now we're going to learn about the NCO! This is a really 
    important part of the streamer..." (tutorial)
```

### 6.2 Cross-References

Direct links:

```
✅ "See DAC Channel Configuration for the complete %dddd routing table."
✅ "Related: XINIT, XZERO, WAITXFI"

❌ "You might want to check out the DAC section later..." (vague)
```

### 6.3 Summary Sections

Factual recaps:

```
✅ "Key Points:
    - NCO frequency = $8000_0000 × (desired_rate / clock_rate)
    - XINIT starts immediately; XCONT/XZERO wait for prior command
    - D[15:0] = 0 stops the streamer"

❌ "Great job learning about the NCO! You now understand..." (tutorial)
```

---

## 7. Quality Checklist

### Voice Consistency
- [ ] Third person throughout (no "you," "we," "I")
- [ ] No hedging language ("may," "might," "probably")
- [ ] No tutorial voice ("let's," "congratulations")
- [ ] Definitive statements only

### Terminology Consistency
- [ ] Instruction names bold uppercase in prose
- [ ] Consistent bit field notation (D[31:28])
- [ ] Symbol names in monospace (`X_RFWORD_RGB16`)
- [ ] Canonical terms from Section 4.1

### Enhancement Completeness
- [ ] Pitfalls marked with ⚠️ where critical
- [ ] Tips marked with 💡 where valuable
- [ ] Hardware notes marked with 🔧 where relevant
- [ ] Cross-references to related sections

### Clarity
- [ ] Mode descriptions precise and complete
- [ ] Examples show purpose, not just syntax
- [ ] Tables are scannable
- [ ] Constraints explicitly stated

---

## 8. Summary: The Voice Equation

```
Our Voice = Silicon Documentation Precision + Practical Developer Guidance
```

**From Silicon Doc, we preserve:**
- Technical accuracy and completeness
- Precise bit field specifications
- Authoritative mode descriptions
- Timing and hardware details

**To Silicon Doc, we add:**
- ⚠️ Pitfall warnings for common mistakes
- 💡 Tips for effective usage
- 🔧 Hardware notes for integration
- Practical code examples with context
- Cross-references between related features
- Frequency calculation helpers

**The result:**
A source-of-truth reference that tells developers exactly how the streamer works and helps them use it correctly in real applications.

---

*Version: 1.0 - Initial Voice Guide*
*Created: 2026-01-22*
