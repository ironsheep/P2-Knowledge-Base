# P2 Streamer Programming Guide - Creation Guide

**Canonical Name:** `p2-streamer-programming-guide`  
**Document Title:** P2 Streamer Programming Guide  
**Created:** 2026-01-22

---

## 1. Document Identity

### 1.1 Purpose and Scope

This guide does two complementary jobs. It **teaches** what the streamer is, why the P2 has one, and how to think about it — the conceptual understanding a reader needs before the details mean anything — and it serves as the **comprehensive reference** for every streamer mode, constant, and configuration. It consolidates silicon documentation, Spin2 documentation, and real-world code into a single authoritative source, written in two registers (see `voice-guide.md`, Section 1.4): a warm teaching register for the conceptual chapter and chapter openers, and a precise reference register for the tables and specifications.

**This document IS:**
- A conceptual introduction to the streamer — what it is, why it exists, and when to use it
- A complete reference for streamer modes, constants, and configurations
- The authoritative source for NCO frequency calculations
- A practical guide with working code examples and integration notes (DAC, colorspace converter, FIFO)

**This document is NOT:**
- A *tutorial* — it teaches the hardware and how to think about it, but it does not walk you through building a project step by step with progressive exercises (that is the DeSilva style; this guide teaches understanding, not a guided build)
- A complete video system design guide (it covers the streamer, not full video architecture)
- A substitute for the P2 basics — it builds the streamer-specific background a newcomer needs, but assumes general familiarity with PASM2 and the P2's COG/Hub model

### 1.2 Target Audience

This guide serves developers who:
1. **Are implementing video output** (VGA, HDMI, composite)
2. **Need high-speed I/O** (SPI, parallel data, DAC waveforms)
3. **Are building signal processing systems** (Goertzel analysis, DDS synthesis)
4. **Are debugging streamer-based code** (mode configuration, timing issues)

**Assumed Knowledge:**
- P2 COG and Hub memory architecture
- Basic PASM2 instruction set
- RDFAST/WRFAST FIFO operations
- Pin and DAC fundamentals

### 1.3 Relationship to Other Manuals

| Manual | Relationship |
|--------|-------------|
| **P2 Assembly Language Manual** | Covers XINIT/XCONT/XZERO instructions; this guide covers streamer *usage* |
| **P2 Smart Pins Tutorial** | Smart pins often coordinate with streamer (SPI clocks, etc.) |
| **P2 Debug Window Manual** | DEBUG can observe streamer output |
| **DeSilva PASM Style** | A true step-by-step tutorial; this guide teaches concepts and explains the hardware, but is not a guided build |

---

## 2. Document Architecture

### 2.1 Overall Structure

```
FRONT MATTER
├── Title Page
├── Version History
└── How to Use This Guide

PART I: STREAMER FUNDAMENTALS (~15 pages)
├── Chapter 1: Introduction and Overview
├── Chapter 2: Architecture
├── Chapter 3: NCO and Timing
└── Chapter 4: Command Structure

PART II: MODE REFERENCE (~40 pages)
├── Chapter 5: Immediate Modes (IMM)
├── Chapter 6: RDFAST Modes (RF)
├── Chapter 7: WRFAST Modes (WF)
├── Chapter 8: RGB Video Modes
├── Chapter 9: ADC Sampling Modes
└── Chapter 10: DDS/Goertzel Mode

PART III: CONFIGURATION REFERENCE (~20 pages)
├── Chapter 11: DAC Channel Configuration
├── Chapter 12: Pin Selection and Control
├── Chapter 13: Programming Constants (Symbols)
└── Chapter 14: Events and Synchronization

PART IV: APPLICATIONS (~25 pages)
├── Chapter 15: Video Output (VGA, HDMI)
├── Chapter 16: High-Speed Serial (SPI)
├── Chapter 17: Signal Processing (DDS, Goertzel)
└── Chapter 18: Integration Patterns

APPENDICES
├── A: Complete Mode Encoding Table
├── B: Symbol Quick Reference
├── C: Frequency Calculation Tables
└── D: Troubleshooting Guide

INDEX
```

### 2.2 Part Rationale

**Part I (Fundamentals):** Establishes the mental model - how the streamer works, NCO timing, command structure. Essential for understanding all modes.

**Part II (Mode Reference):** The heart of the document. Each mode category fully documented with encoding, parameters, and examples.

**Part III (Configuration):** Cross-cutting concerns - DAC routing, pin selection, constants. Applies to all modes.

**Part IV (Applications):** Practical implementations showing real-world usage patterns.

---

## 3. Pedagogical Framework

### 3.1 Learning Theory for a Two-Register Guide

This guide teaches in two ways at once, and the pedagogy differs by layer.

The **teaching layer** (the conceptual chapter and each chapter's opener) works the way good explanatory writing always has: an advance organizer first (the big picture before the parts), motivation before mechanism, concrete imagery and analogy to build a mental model, and differentiation by contrast so similar-looking options become distinct. This is how a newcomer goes from "what even is a streamer?" to knowing which modes to read.

The **reference layer** (the mode tables, bit fields, and per-instruction detail) serves learning differently — not through narrative but through **pattern recognition**, **consistent structure**, and **reliable findability**. A developer who uses this layer 50 times learns more than someone who reads a tutorial once.

**Core Insight:** the two layers reinforce each other. The teaching layer gives the reference layer somewhere to attach; the reference layer gives the teaching layer the precision to cash in. The sections below identify which classic learning principles apply to each.

### 3.2 Principles That Apply (Adapted for Reference)

#### Cognitive Load Theory (Sweller, 1988)
**Application:** Reduce extraneous cognitive load through consistent formatting.

| Tutorial Approach | Reference Approach |
|-------------------|-------------------|
| Narrative reduces load through story | **Consistent structure** reduces load through predictability |
| Progressive disclosure over pages | **Consistent entry format** - every mode looks the same |
| Conversational tone eases reading | **Dense tables** - find information visually, not verbally |

**Implementation:**
- Every mode entry follows identical structure
- Tables present complex data in scannable format
- Terminology is consistent throughout (no synonyms)

#### Dual Coding Theory (Paivio, 1971)
**Application:** Multiple representations improve retention.

**Implementation:**
- Mode encoding tables (visual)
- Prose descriptions (verbal)
- Code examples (procedural)
- Block diagrams for architecture (spatial)

⚠️ **Note:** Unlike tutorials, we don't explain the diagram narratively. The diagram stands alone for those who think visually; the table stands alone for those who scan text.

#### Prior Knowledge Activation (Ausubel, 1968)
**Application:** Connect new information to existing mental models.

**Implementation:**
- Assume P2 fundamentals (don't re-teach Hub memory)
- Use familiar patterns ("like SPI but...")
- Cross-reference related hardware (DAC channels, FIFO)
- Compare modes to each other ("same as X except...")

#### Scaffolding Theory (Wood, Bruner, Ross, 1976)
**Application:** Structure supports understanding until expertise develops.

**Implementation:**
- Part I establishes mental model before mode details
- Architecture chapter explains streamer conceptually
- Then modes make sense in context
- Repeated reference builds expertise incrementally

#### Retrieval Practice Support
**Application:** Easy lookup reinforces memory through repeated retrieval.

**Implementation:**
- Mode selection tables ("which mode do I need?")
- Symbol quick reference (find without searching)
- Consistent page structure (know where to look)
- Comprehensive index (multiple entry points)

### 3.3 Principles That Don't Transfer (Tutorial-Only)

| Tutorial Principle | Why It Doesn't Apply |
|-------------------|---------------------|
| **Self-deprecating humor** | Reference seeks authority, not approachability |
| **Celebration moments** | No sequential journey to celebrate |
| **Conversational tangents** | Users seek specific info, not exploration |
| **Progressive difficulty ordering** | Users jump to what they need |
| **Learning objectives per section** | No sequential learning path |
| **Difficulty indicators (🟢🟡🔴)** | Users choose by need, not difficulty |
| **Time estimates** | Not learning sequentially |
| **"Try This" exercises** | Reference is for doing, not practicing |
| **Prerequisite checks ("You know X, don't you?")** | Assumed at document level, not per section |

**Key Distinction:** Tutorial voice says "Let's learn this together." Reference voice says "Here's what you need to know."

### 3.4 How Reference Format Serves Learning

**The Reference Learning Model:**

```
First Use: Developer has problem → Searches → Finds mode → 
          Struggles with entry format → Implements with effort

Third Use: Developer has problem → Remembers section → 
          Scans familiar structure → Implements faster

Tenth Use: Developer has problem → Goes directly to mode → 
          Extracts specific detail → Implements immediately

Expertise: Developer recalls modes from memory → 
           Reference becomes verification, not learning
```

**What Makes This Work:**

1. **Consistency builds familiarity** - Same structure every time trains the brain
2. **Dense information rewards expertise** - Tables that once seemed overwhelming become quick reference
3. **Cross-references build connections** - Repeated links create mental maps
4. **Examples provide anchors** - Concrete code grounds abstract specifications

### 3.5 Markers as Pedagogical Tools

The enhancement markers (⚠️ 💡 🔧) serve a pedagogical purpose:

| Marker | Pedagogical Function |
|--------|---------------------|
| **⚠️ Pitfall** | Prevents productive failure from becoming unproductive frustration |
| **💡 Tip** | Shares expert knowledge that saves time |
| **🔧 Hardware** | Connects software to silicon reality |

**These markers compress the wisdom that tutorials spread across narrative into dense, findable notes.** A developer who reads every pitfall warning in this manual gains experience equivalent to debugging those issues themselves.

### 3.6 Success Through Repeated Use

**Tutorial Success Metric:** Reader can implement X after reading once.

**Reference Success Metric:** Reader can implement X faster on each subsequent lookup until they no longer need to look it up.

This document optimizes for the second metric. The initial experience may be denser than a tutorial, but the hundredth lookup should take seconds, not minutes.

### 3.7 Cross-Reference to Voice Guide

The voice choices in `voice-guide.md` implement these pedagogical principles:

| Pedagogical Principle | Voice Implementation |
|-----------------------|---------------------|
| Cognitive load reduction | Consistent terminology, no synonyms |
| Pattern recognition | Identical entry format for every mode |
| Dual coding | Tables (visual) + prose (verbal) + code (procedural) |
| Prior knowledge activation | Assumes P2 basics, references related hardware |
| Retrieval practice support | Dense tables, comprehensive index |

See `voice-guide.md` Section 1.2 for the summary of pedagogical grounding.

---

## 4. Source Materials

### 4.1 Primary Sources

| Source | Location | Content | Authority |
|--------|----------|---------|-----------|
| **Silicon Doc v35** | `/engineering/ingestion/sources/silicon-doc/` | Detailed streamer operation, encoding tables, timing | PRIMARY - hardware truth |
| **Spin2 v51 Docs** | `/engineering/ingestion/sources/spin2-v51/` | Complete symbol reference (X_* constants) | PRIMARY - constant definitions |
| **Flash Loader Source** | `/engineering/ingestion/external-inputs/source-code/spin-flash-loader/` | Real-world streamer+smart pin coordination | EXAMPLE - official ROM code |
| **Quick Bytes Goertzel** | `/engineering/ingestion/sources/quick-bytes-code/` | DDS/Goertzel implementation | EXAMPLE - Parallax examples |
| **OBEX Video Drivers** | `/engineering/ingestion/external-inputs/source-code/obex-projects/` | Video output patterns | EXAMPLE - community code |

### 4.2 Authority Hierarchy

When sources conflict:
1. **Silicon Documentation** - Hardware behavior is ground truth
2. **Spin2 Documentation** - Symbol definitions
3. **Official ROM Code** - Proven implementations
4. **Community Examples** - Validated patterns

### 4.4 Content Verification Protocol (Hallucination Prevention)

**Added:** 2026-01-23
**Derived from:** PASM2 Manual Content Verification Sprint findings

#### Why This Section Exists

The PASM2 manual audit discovered that **hallucinations occur at the moment of writing**, not after. Hardware capability claims were fabricated by inferring "reasonable" behaviors. This section ensures Streamer documentation is verified before writing.

**Critical insight**: Sections 4.1-4.3 tell you WHERE sources are. This section tells you HOW TO VERIFY claims before writing them.

#### Claim Types and Required Sources for Streamer

| Claim Type | Required Source | Example Claim |
|------------|-----------------|---------------|
| **Mode encoding** | Silicon Doc mode tables | "RFBYTE uses D[31:28] = %1000" |
| **Symbol values** | Spin2 X_* constant reference | "X_RFBYTE_1P_1DAC1 = %1000 << 28" |
| **NCO behavior** | Silicon Doc NCO section | "NCO rolls over every N clocks" |
| **DAC routing** | Silicon Doc DAC section | "DAC0 drives pins %xxxx00" |
| **Pin behavior** | Silicon Doc ONLY | "Pins output in specified order" |
| **Timing claims** | Silicon Doc + validated code | "Pixel rate of 25 MHz requires..." |
| **Integration patterns** | Official ROM code (flash loader) | "WAITXFI synchronization pattern" |

#### Red-Flag Phrases for Streamer Documentation

**STOP and verify when you're about to write:**

| Phrase | Risk Level | Why Suspicious | Action |
|--------|------------|----------------|--------|
| "automatically" | **CRITICAL** | Streamer requires explicit configuration | Verify in Silicon Doc |
| "synchronizes" | **HIGH** | Sync claims need hardware evidence | Find specific mechanism |
| "optimizes" | **HIGH** | Optimization claims need proof | Cite performance data |
| "enables" (vague) | MEDIUM | Capability attribution | Find specific mode/symbol |
| "internally buffers" | MEDIUM | Buffer behavior must be documented | Check Silicon Doc |
| "protocol support" | MEDIUM | Streamer is raw data, not protocol-aware | Clarify what mode does |

#### The Verification Protocol for Streamer

**Before writing ANY Streamer claim:**

```
┌─────────────────────────────────────────────────────────────────┐
│           STREAMER CLAIM VERIFICATION CHECKLIST                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. What am I claiming? (mode/NCO/DAC/pin/timing)               │
│                                                                 │
│  2. Which source should contain this?                           │
│     □ Silicon Doc: mode tables, NCO, DAC, timing                │
│     □ Spin2 Docs: X_* symbol values                             │
│     □ ROM Code: proven implementation patterns                  │
│     □ OBEX/Community: validated usage examples                  │
│                                                                 │
│  3. Can I cite the EXACT location?                              │
│     □ Silicon Doc section (Part 2 - Pixel Operations)           │
│     □ Spin2 symbol name and hex value                           │
│     □ Code file and line                                        │
│                                                                 │
│  4. Does the source say this EXACTLY?                           │
│     □ YES → Write the claim                                     │
│     □ NO, I'm extrapolating → DON'T WRITE IT                    │
│     □ Source doesn't exist → Mark as unverified                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Streamer-Specific Verification Examples

**Example 1: Correct Verification (Mode Symbol)**

Claim to write: "X_RFBYTE_1P_1DAC1 outputs one byte per NCO rollover to 1 pin and 1 DAC"

1. Claim type: Mode behavior + symbol
2. Required source: Silicon Doc mode table + Spin2 symbol reference
3. Check: Silicon Doc → RFBYTE mode table → "1P" = 1 pin, "1DAC1" = DAC channel 1
4. Check: Spin2 → X_RFBYTE_1P_1DAC1 exists with documented value
5. Source says exactly this? YES → Write the claim

**Example 2: Blocked Fabrication**

Attempted claim: "The streamer automatically synchronizes with Hub access timing"

1. Claim type: Synchronization capability
2. Required source: Silicon Doc streamer/hub interaction section
3. Check: Silicon Doc describes NCO as independent timing source
4. Does "automatic hub synchronization" appear? NO
5. Result: **CLAIM BLOCKED** - This is an assumption about behavior

#### Full Audit Methodology Reference

For comprehensive post-write audit procedures, see:
`engineering/operations/process/TECHNICAL-DOCUMENT-AUDIT-METHODOLOGY.md`

---

### 4.5 Key Source Files

**Silicon Documentation (Part 2 - Pixel Operations):**
- `part2-pixel-ops.txt` - Streamer mode tables, DAC routing
- `part2-video-output.txt` - HDMI/DVI, colorspace converter
- `part2-more-content.txt` - DDS/Goertzel detailed operation

**Spin2 Symbol Reference:**
- `complete-streamer-symbols.md` - All X_* constants with values
- `streamer-events-symbols.txt` - EVENT_XMT, EVENT_XFI, etc.

**Code Examples:**
- `flash_loader.spin2` - XINIT/WAITXFI with smart pin coordination
- `Goertzel_ultrasonic.spin2` - Complete DDS/Goertzel example
- `p2videodrv.spin2` - VGA/video output patterns

---

## 5. Content Specifications

### 5.1 Mode Entry Format

Each mode or mode group follows this structure:

```markdown
## Mode Category Name

### Overview
[One paragraph describing what this mode category does]

### Encoding Table

| Mode | Symbol | Description | Pins | DACs |
|------|--------|-------------|------|------|
| %xxxx | X_SYMBOL | Description | N | N |

### D Field Structure
- D[31:28]: Mode selector
- D[27:24]: DAC routing
- D[23]: Enable bit
- D[22:20]: Pin group
- D[19:16]: Mode-specific
- D[15:0]: Count

### S Field Usage
[What S contains for this mode]

### Operation
[Step-by-step description of what happens on each NCO rollover]

### Example

```pasm2
' [Practical example with comments explaining WHY]
```

### Notes
⚠️ **Pitfall:** [Common mistakes]
💡 **Tip:** [Useful techniques]
🔧 **Hardware:** [Silicon details]
```

### 5.2 Code Example Standards

**Requirements:**
- Must be complete and compilable
- Must demonstrate core functionality
- Must include comments explaining purpose (not just restating instruction)
- Prefer PASM2 for low-level control examples
- Include Spin2 where high-level usage is clearer

**Example Quality:**

```pasm2
' GOOD - explains purpose
' VGA horizontal sync generation
' XZERO at sync start ensures consistent line timing
hsync:  xcont   m_bs, sync0      ' 16 pixels front porch
        xzero   m_sn, sync1      ' 96 pixels sync (phase reset)
        xcont   m_bv, sync0      ' 48 pixels back porch

' BAD - just restates instructions
hsync:  xcont   m_bs, sync0      ' xcont
        xzero   m_sn, sync1      ' xzero
        xcont   m_bv, sync0      ' xcont
```

### 5.3 Symbol Table Format

```markdown
### Mode Symbols

| Symbol | Value | Description |
|--------|-------|-------------|
| `X_RFBYTE_1P_1DAC1` | `%1000 << 28` | RFBYTE to 1 pin, 1 DAC |

### Control Symbols

| Symbol | Value | Effect |
|--------|-------|--------|
| `X_PINS_ON` | `%1 << 23` | Enable pin output |
```

### 5.4 Frequency Calculation Tables

Include pre-calculated common values:

```markdown
### Common NCO Frequencies

| Pixel Rate | At 250 MHz | At 300 MHz | At 320 MHz |
|------------|------------|------------|------------|
| 25 MHz (VGA 640x480) | $0CCC_CCCD | $0AAA_AAAB | $0A00_0000 |
| 40 MHz (VGA 800x600) | $1999_999A | $1555_5556 | $1400_0000 |
```

---

## 6. Writing Guidelines

### 6.1 Voice Summary

See `voice-guide.md` for complete voice specifications.

**Key Points:**
- Third person, authoritative
- No hedging ("may", "might", "probably")
- No tutorial voice ("let's", "you'll discover")
- Precise specifications
- Practical examples

### 6.2 Terminology

**Consistent Terms:**
- "NCO" not "oscillator" or "clock"
- "rollover" not "overflow" or "trigger"
- "command" not "instruction" (for the D operand)
- "mode" not "type" (for D[31:28])

**Formatting:**
- Instructions: **BOLD UPPERCASE** in prose
- Symbols: `monospace` (X_RFBYTE_1P_1DAC1)
- Bit fields: D[31:28], S[19:16]
- Binary: `%1011_0000`
- Hex: `$B0850000`

### 6.3 Cross-References

Use direct references:

```markdown
✅ "See DAC Channel Configuration for routing options."
✅ "Related: XINIT, XCONT, XZERO, WAITXFI"
✅ "For NCO frequency calculation, see Chapter 3."

❌ "Check out the DAC section when you get a chance."
```

---

## 7. Enhancement Markers

### 7.1 Marker Types

| Marker | Purpose | When to Use |
|--------|---------|-------------|
| ⚠️ **Pitfall:** | Common mistakes | Missing RDFAST, wrong DAC routing, timing errors |
| 💡 **Tip:** | Useful techniques | Frequency shortcuts, mode combinations, optimization |
| 🔧 **Hardware:** | Silicon details | NCO +1 trick, DAC timing, pin requirements |

### 7.2 Marker Examples

```markdown
⚠️ **Pitfall:** RFBYTE modes require RDFAST setup before the streamer 
command. Without it, the FIFO contains random data.

💡 **Tip:** For NCO frequencies that are exact fractions (1/2, 1/4, 1/8), 
no +1 adjustment is needed. Only fractional values like 1/3 need +1.

🔧 **Hardware:** DAC channels only drive pins whose two LSBs match the 
channel number. DAC0 → pins %xxxx00, DAC1 → pins %xxxx01, etc.
```

---

## 8. Quality Requirements

### 8.1 Validation Checklist

**Per Mode:**
- [ ] Encoding matches silicon documentation
- [ ] Symbol matches Spin2 documentation
- [ ] D field structure documented
- [ ] S field usage documented
- [ ] Example compiles with pnut_ts
- [ ] Pitfalls identified where applicable

**Per Chapter:**
- [ ] All modes in category covered
- [ ] Cross-references valid
- [ ] Examples demonstrate real usage
- [ ] Terminology consistent

**Document-Level:**
- [ ] All 50+ mode variants documented
- [ ] All X_* symbols included
- [ ] NCO calculations verified
- [ ] Index complete

### 8.2 Code Testing

All code examples must:
1. Compile with `pnut_ts` without errors
2. Be syntactically correct PASM2 or Spin2
3. Demonstrate the described functionality
4. Include meaningful comments

---

## 9. Production Workflow

### 9.1 Content Development

1. **Extract from sources** - Pull mode tables, symbols, examples
2. **Structure content** - Organize by mode category
3. **Write descriptions** - Clear, precise operation explanations
4. **Add examples** - Practical, tested code
5. **Add enhancements** - Pitfalls, tips, hardware notes
6. **Cross-reference** - Link related content

### 9.2 Review Process

1. **Technical accuracy** - Verify against silicon doc
2. **Code validation** - Compile all examples
3. **Consistency check** - Terminology, formatting
4. **Completeness** - All modes, symbols covered

### 9.3 PDF Generation

**Workspace:** `/engineering/document-production/workspace/p2-streamer-programming-guide/`

**Outbound:** `/engineering/document-production/outbound/p2-streamer-programming-guide/`

**Template:** Select appropriate P2KB template (similar to Assembly Language Manual)

**Pre-PDF Steps:**
1. LaTeX escape script
2. Verify all cross-references
3. Generate index entries

---

## 10. Maintenance

### 10.1 Update Triggers

- New silicon documentation release
- Symbol additions in Spin2
- Community-discovered modes or techniques
- Error corrections

### 10.2 Version Control

- Track changes in git
- Document updates in version history
- Increment version appropriately (1.x for minor, 2.x for major)

---

## 11. Success Metrics

### Quantitative
- All 50+ mode variants documented
- All ~80 X_* symbols included
- 15+ working code examples
- Complete encoding tables

### Qualitative
- Developer can find any mode in <30 seconds
- Examples are copy-paste usable
- No ambiguity in specifications
- Practical for real-world implementation

---

## Appendix: Key Content Extracted

### From Silicon Documentation

**Mode Encoding Tables:**
- Immediate → LUT → Pins/DACs (0000-0011)
- Immediate → Pins/DACs (0100-0111)
- RDFAST → LUT → Pins/DACs (0111_xxxx)
- RDFAST → Pins/DACs (1000-1011)
- RDFAST → RGB (1011_xxxx)
- Pins → WRFAST (1100-1111)
- ADC Sampling (1111_xxxx)
- DDS/Goertzel (1111_x111)

**DAC Routing (%dddd):**
- 16 configurations from no-output to 4-channel independent

**Pin Selection (%ppp):**
- 8 pin group selections with wrap-around

### From Spin2 Documentation

**Mode Symbols:** ~40 X_IMM_*, X_RF*, X_WF_* symbols
**Control Symbols:** X_PINS_ON, X_DACS_*, X_WRITE_ON, X_ALT_ON
**Event Symbols:** EVENT_XMT, EVENT_XFI, EVENT_XRO, EVENT_XRL

### From Code Examples

**Flash Loader:** XINIT+WYPIN+WAITXFI pattern for SPI
**VGA Driver:** XCONT/XZERO video line generation
**Goertzel:** DDS output with simultaneous frequency analysis

---

*Version: 1.1 - Added Pedagogical Framework (Section 3)*
*Created: 2026-01-22*
*Updated: 2026-01-22*
