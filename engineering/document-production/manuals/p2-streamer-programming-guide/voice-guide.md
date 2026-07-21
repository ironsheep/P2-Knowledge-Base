# P2 Streamer Programming Guide - Voice Guide

**Document:** P2 Streamer Programming Guide  
**Purpose:** Define writing voice and tone — a guide that teaches the streamer conceptually, then serves as a precise reference  
**Created:** 2026-01-22

---

## 1. Voice Philosophy

### 1.1 The Guiding Principle

> **This guide first helps you understand what the streamer is and why you would use it, then tells you exactly how every mode works and how to configure it.**

The document does two jobs, so it speaks in **two registers** (defined in Section 1.4):

- A **teaching register** — the conceptual chapter and each chapter's opening orientation — warm, plain-spoken, and motivated, for a reader meeting the streamer for the first time.
- A **reference register** — the mode tables, bit fields, symbol tables, and per-instruction detail — for a reader who already knows what they need and wants it fast. The reference register must be:
  - **Authoritative** - the source of truth for streamer operation
  - **Precise** - no ambiguity about modes, bit fields, or timing
  - **Efficient** - dense information for developers who know what they need
  - **Practical** - real examples showing actual usage patterns

Sections 2–6 of this guide codify the **reference** register; Section 1.4 defines the **teaching** register and when each applies.

### 1.2 Pedagogical Grounding

These voice choices are grounded in learning theory adapted for reference documentation. See `creation-guide.md`, Section 3 (Pedagogical Framework) for the research basis:

- **Consistent structure** reduces cognitive load (Sweller, 1988)
- **Multiple representations** (tables, prose, code) support dual coding (Paivio, 1971)
- **Dense information** rewards expertise through repeated use
- **Pattern recognition** through identical entry formats accelerates lookup

Unlike tutorial manuals, reference documents serve learning through **repeated retrieval** - the hundredth lookup should take seconds, not minutes.

### 1.3 Target Audience

The Streamer Programming Guide serves a **spectrum** of readers, and the two registers exist to serve both ends of it:

- **Newcomers** — developers (including hobbyist and DIY engineers) coming to the P2 who have heard of the streamer but do not yet know what it is, why it exists, or when to reach for it. The **teaching register** is for them: the conceptual chapter and chapter openers assume no prior streamer knowledge and define unfamiliar terms as they appear.
- **Experienced developers** — readers who understand P2 COG/Hub architecture and want to implement video, high-speed I/O, or signal processing, or who are porting or debugging streamer code. The **reference register** is for them: quick lookup of modes, constants, configurations, and exact bit fields.

The teaching layer builds the background a newcomer needs (hub memory and the FIFO, pins, DACs) rather than assuming it; the reference layer assumes it. A single reader typically starts in the teaching register and graduates into the reference register as they build.

### 1.4 The Two Registers — Teaching and Reference

The guide deliberately switches voice depending on what the reader needs at that moment.

**Use the teaching register for:** the conceptual chapter (Chapter 1, "Understanding the Streamer"), the opening orientation of each Part and each mode chapter, and the first explanation of any unfamiliar concept (DDS, Goertzel, colorspace conversion).

Teaching-register rules:

- **Plain language first.** Define every unfamiliar term on first use, in one or two sentences, with a concrete use — e.g., Goertzel as "asking how much of one specific frequency is present in a signal; used to decode phone touch-tones." Never let a named feature appear unexplained.
- **Motivate before detail.** Say *why* something matters before *how* it works.
- **"You" and light analogy are allowed and encouraged.** The metronome, the paced pipe, the player-piano roll — imagery is how a newcomer forms a mental model. Use it.
- **Differentiate by contrast.** When several options sound alike, show what makes them *different* rather than describing each in isolation.
- **Comparative grounding is a soft bridge, never a crutch.** When a real-world parallel (DMA is the obvious one) would help an experienced reader, offer it as a clearly skippable aside — a `> If you've used X before:` note. The explanation must always stand on its own for a reader who has never met that parallel. Do not make understanding depend on outside knowledge.
- **Applications are pointers, not pitches.** Frame applications as "if you're building X, these are the modes to understand," directing the reader rather than selling the hardware.

**Use the reference register for:** mode tables, bit-field specifications, symbol tables, per-instruction syntax and effects, frequency tables, and worked code examples. Its rules are in Sections 2–6 (third person, no hedging, dense, exact). Those rules govern the reference layer only; the teaching register relaxes the no-"you" and no-analogy constraints as described above.

**The handoff.** A chapter typically opens in the teaching register (a short orientation — what these modes are for, how they differ) and then shifts into the reference register for the tables and specifications. The two coexist on the page: guidance up front, precision underneath.

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
| "You might wonder why..." | **Tutorial filler** (NOT the same as calibrated confidence — see §2.2a) | State the fact directly |
| "Simply configure..." | Dismissive of complexity | "Configure..." |
| "Basically, it works like..." | Vague | Precise description |
| "Congratulations!" | Tutorial celebration | (omit) |
| "the obvious way to set the NCO is wrong" · "it is tempting to reach for XINIT here" · "Read that formula again" | **Reader-as-foil** — tells the reader what they think, then corrects them (the "besserwisser" register) | State the correct fact; let the reader draw the contrast |
| "this is where the streamer really shines" · "the single most elegant part of the FIFO" · "nothing else on the P2 comes close" | **Self-admiration** — the text praising its subject or its own explanation | State what the thing does; let the reader judge it |
| "and here is the trap" · "but there's a catch we'll get to" · "Hold that phase value" | **Staged reveal** — withholding a fact to manufacture a beat | Deliver the fact where it belongs, unstaged |

#### 2.2a Calibrated confidence is required — it is not hedging {#sec-2-2a}

Banning tutorial filler ("you might wonder", "let's explore") does **not** mean
banning *uncertainty*. A qualifier that reflects the true state of the evidence
— "essentially exact at any sysclk", "on most display timings", "in practice" —
is **accuracy**, not hedging, and it is required wherever the unqualified claim
would overstate. The test is one line: **never state a claim above its
evidence.** "The NCO never drifts" is wrong if it drifts by one LSB per
rollover; "most video modes need XZERO" is wrong if you have not surveyed them.
Say what is true at the confidence it is true, and cite the Silicon Doc when a
solid figure is lacking. A rhetorical flourish that *demands* a punchy payoff is
exactly where an unsupported claim slips in — strip the flourish and read what is
left as a bare claim before keeping it. (Shared discipline: the
`documentation-voices-catalog` §"Shared Discipline"; detection: `document-audit`
Dimension #4c payoff-sentence sweep.)

### 2.3 Voice Comparison

| Aspect | DeSilva Tutorial | This Reference |
|--------|------------------|----------------|
| Person | Second ("you") | Third (component names) |
| Tone | Warm, encouraging | Authoritative, precise |
| Tutorial filler | Occasional | Never |
| Calibrated qualifiers | Yes | **Yes, where true** (§2.2a) |
| Examples | Progressive, extensive | Targeted, illuminating |
| Celebration | Yes ("Uff!") | Never |
| Questions | Yes ("Why?") | No |
| Asides | Yes | Rarely, only for critical warnings |
| Closing beat every section | — | No (budget — §2.4) |

### 2.4 Cadence budget — not every section earns a beat {#sec-2-4}

A *beat* is a closing sentence that lands a rhetorical punch rather than
finishing the exposition — a verdict, a reversal, a directive to the reader, an
aphorism that restates with force. One well-placed beat is good writing. The
failure mode is **regularity**: when nearly every section ends on one, the reader
stops hearing the individual beat and starts hearing the *metronome* — "instantly
recognizable and becoming rapidly fatiguing" (Chip Gracey, XBYTE review
2026-07-20; adopted platform-wide). The recognizable-AI quality is the pattern,
not any one sentence, so the fix is distribution, not deletion:

- **At most ~half of section closings may be beats.** Cut the weakest back to a
  plain informational close.
- **No long runs** — never more than **~4 sections in a row** all closing on a
  beat. A stretch of flat, informational closes is rest, not a defect.
- **Chapter closers are the worst offenders** — aim well below a beat on every
  chapter exit.
- **A declared refrain is not a beat** — a deliberate, announced structural
  device is structure, keep it.
- **Protect the earned ones** — a beat that carries real information or lowers the
  text's own confidence survives. Do not flatten the document to hit a number.

Detection tooling: `document-audit` Dimension #4c (payoff-sentence sweep) measures
closing-beat rate and the longest consecutive run.

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
