# P2 Assembly Language Manual - Creation Guide

**Canonical Name:** `p2-assembly-language-manual`
**Document Title:** P2 Assembly Language (PASM2) Manual

---

## 1. Document Identity

### 1.1 Purpose and Scope

This manual serves as the **definitive source of truth** for the Propeller 2 assembly language (PASM2). It consolidates and supersedes the partial Parallax draft manual, providing complete, authoritative documentation for every PASM2 instruction.

**This document IS:**
- A complete technical reference for the PASM2 language:
  - **359 instructions** (actual executable opcodes)
  - **15 directives** (ORG, ORGF, ORGH, BYTE, WORD, LONG, FILE, BYTEFIT, WORDFIT, ALIGNL, ALIGNW, DITTO, FIT, RES, END)
  - **6 constants** (TRUE, FALSE, PI, etc.)
  - **Special registers** (DIRA, DIRB, INA, INB, OUTA, OUTB, etc.)
- The authoritative source when conflicts exist between older documents
- A reference that grounds readers in P2's unique architectural concepts
- Suitable for both quick lookup and deep understanding

**This document is NOT:**
- A tutorial for learning assembly (that's the DeSilva manual: `p2-pasm-desilva-style`)
- A comprehensive Smart Pins guide (that's `p2-smart-pins-tutorial`)
- A beginner's first introduction to P2

### 1.2 Target Audience

This manual serves three audiences, in order of primary focus:

1. **Experienced P2 Developers** (primary)
   - Have 1+ years of P2 experience
   - Need quick, accurate lookup of instruction details
   - Want edge cases, encoding details, flag behavior
   - "I've used this instruction before, remind me of the details"

2. **Experienced Embedded Developers New to P2** (secondary)
   - Know assembly language from other platforms (ARM, AVR, x86)
   - Need to understand P2's unique architectural model
   - May be misled by assumptions from other architectures
   - "I know assembly, but P2 does things differently"

3. **Neophytes Graduating from DeSilva Tutorial** (tertiary)
   - Completed the pedagogical DeSilva manual
   - Ready for the "official" technical reference
   - Need deeper details than the tutorial provided
   - "I learned the basics, now I need the complete picture"

### 1.3 Relationship to Other Manuals

| Manual | Purpose | Relationship |
|--------|---------|--------------|
| **This manual** | Instruction reference, source of truth | The definitive technical reference |
| `p2-pasm-desilva-style` | Tutorial - "Discovering P2 Assembly" | Pedagogical complement; readers graduate to this manual |
| `p2-smart-pins-tutorial` | Smart Pin modes and applications | This manual covers Smart Pin *instructions*; that manual covers *modes* |
| `p2-debug-window-manual` | DEBUG system reference | This manual covers DEBUG instruction; that manual covers DEBUG windows |

### 1.4 Source Material

This manual replaces and enhances the partial Parallax draft:

**Original Source:**
- **Document:** `P2-Assembly-Language-PASM2-Manual-Draft-221117.pdf`
- **Location:** `/engineering/ingestion/sources/pasm2-manual/`
- **Status:** PRELIMINARY/DRAFT, ~315 instructions documented
- **Gap:** ~60 instructions had minimal or no documentation

**Knowledge Base Source (Authoritative):**
- **Location:** `/engineering/knowledge-base/P2/language/pasm2/`
- **Count:** 376 YAML files total:
  - 359 instructions
  - 15 directives (ORG, ORGF, ORGH, BYTE, WORD, LONG, FILE, BYTEFIT, WORDFIT, ALIGNL, ALIGNW, DITTO, FIT, RES, END)
  - 6 constants (TRUE, FALSE, PI, NEGX, POSX, COGEXEC)
  - 1 special registers reference file
- **Status:** Complete language element inventory with structured data

**Additional Sources:**
- Silicon documentation
- P2 spreadsheet (encoding data)
- Community-validated examples

---

## 2. Document Architecture: The Technical Bible Model

### 2.1 Rationale

The P2 is a genuinely unique architecture. Concepts from ARM, x86, or RISC-V can mislead developers:
- 8 symmetric COGs with true parallel execution
- Deterministic timing on every instruction
- 64 Smart Pins with embedded processors
- CORDIC coprocessor for hardware math
- Architecture that makes interrupts largely unnecessary

Even experienced embedded developers are, in some sense, neophytes to *this* architecture. The manual must establish the mental model before diving into instruction details.

### 2.2 Overall Structure

```
FRONT MATTER
├── Title, Copyright, Credits
├── How to Use This Manual
├── Document Conventions
└── Change Log

PART I: ARCHITECTURAL FOUNDATION (~30-40 pages)
├── Chapter 1: The P2 Execution Model
├── Chapter 2: The Instruction Format
├── Chapter 3: Flags and Conditional Execution
├── Chapter 4: Timing and Determinism
└── Chapter 5: Special Hardware Overview

PART II: LANGUAGE REFERENCE (bulk of manual)
├── Instructions A-Z (359 entries)
├── Directives (10 entries)
├── Constants (6 entries)
└── Special Registers

PART III: APPENDICES
├── A. Instruction Encoding Master Table
├── B. Categorical Instruction Index
├── C. Special Registers
├── D. Predefined Constants
├── E. Reserved Words
└── F. Opcode Bit Patterns

COMPREHENSIVE INDEX
```

### 2.3 Part I: Architectural Foundation

Part I establishes the mental model. It is **reference material, not tutorial** - concise, authoritative, precise.

**Chapter 1: The P2 Execution Model**
- COG architecture (512 longs, parallel execution)
- Hub memory (shared 512KB, access timing)
- LUT memory (per-COG, fast access)
- The execution pipeline

**Chapter 2: The Instruction Format**
- 32-bit instruction encoding
- Condition codes (EEEE field)
- Destination and Source fields
- Immediate vs Register operands
- AUGS/AUGD for 32-bit immediates

**Chapter 3: Flags and Conditional Execution**
- C and Z flags
- Flag modification effects (WC, WZ, WCZ)
- All IF_x conditions with truth tables
- Conditional execution patterns

**Chapter 4: Timing and Determinism**
- Clock cycles per instruction
- Hub access windows (egg beater)
- Deterministic timing guarantees
- Timing-critical code patterns

**Chapter 5: Special Hardware Overview**
- CORDIC coprocessor (brief - points to instructions)
- Smart Pins (brief - points to separate manual)
- Streamer (brief - points to instructions)
- Event system and interrupts

Each chapter ends with a **Key Concepts** box summarizing 5-7 essential points.

### 2.4 Part II: Language Reference

The heart of the manual - complete documentation for all PASM2 language elements:

**Instructions (359 entries):**
- Alphabetical A-Z organization
- Complete documentation per instruction
- Consistent entry format enabling pattern recognition

**Directives (10 entries):**
- ORG, ORGH - Assembly origin control
- BYTE, WORD, LONG - Data declarations
- RES - Reserve space
- FIT - Verify code fits in COG
- ALIGNL, ALIGNW - Alignment directives
- HUBEXEC - Hub execution mode

**Constants (6 entries):**
- TRUE, FALSE - Boolean constants
- PI - Mathematical constant
- NEGX, POSX - Signed range boundaries
- COGEXEC - COG execution mode constant

**Special Registers:**
- DIRA, DIRB - Pin direction registers
- INA, INB - Pin input registers
- OUTA, OUTB - Pin output registers
- PTRA, PTRB, PA, PB - Pointer registers

This is where 90% of usage happens. Optimized for:
- Fast lookup by name
- Complete information per entry
- Consistent format enabling pattern recognition
- Cross-references to related elements and Part I concepts

### 2.5 Part III: Appendices

Appendices enable discovery and provide reference tables:

- **Appendix A:** Complete encoding table for all instructions
- **Appendix B:** Categorical index (instructions grouped by function)
- **Appendix C:** Special registers (PTRA, PTRB, PA, PB, etc.)
- **Appendix D:** Predefined constants
- **Appendix E:** Reserved words (PASM2 + Spin2)
- **Appendix F:** Opcode bit patterns

**Appendix B (Categorical Index)** is particularly important - it serves the "I need to do X, which instruction?" use case without polluting the alphabetical reference.

### 2.6 Why This Structure Works

1. **Part I establishes the mental model** - Grounds readers in P2's unique architecture
2. **Part I is skippable but valuable** - Experienced P2 devs can skip to Part II; others benefit from foundation
3. **Part II is the heart** - Alphabetical, complete, every instruction
4. **Part III enables discovery** - Categorical index, encoding tables, reference data
5. **Cross-references tie it together** - Instructions reference Part I concepts; related instructions link to each other

---

## 3. Pedagogical Framework

### 3.1 The Paradox of Reference Documentation

A reference manual isn't a tutorial, yet people *learn* from it:
- **Repeated exposure** - Same format reinforces mental model
- **Contextual learning** - Look up what you need when you need it
- **Pattern recognition** - Consistent structure lets brain focus on content
- **Discovery through proximity** - Related instructions spark new understanding

We design this manual to teach well through its structure.

### 3.2 Core Pedagogical Principles

#### Cognitive Load Management
- **Ruthless consistency** - Same sections, same order, same terminology
- **Visual hierarchy** - Eye knows instantly where to look
- **Progressive disclosure** - Important info first, details later
- **Chunking** - Related information grouped visually

#### Schema Building
- **Part I builds the schema** - COGs, Hub, Flags become mental "folders"
- **Part II references the schema** - "See Chapter 3" tells brain where to file
- **Consistent categories** - Every instruction labeled with category
- **Cross-references** - "Related: ADDX, ADDS" builds instruction families

#### Spaced Repetition Through Structure
- **Consistent format = repeated exposure** - After 20 lookups, format is internalized
- **Flag behavior in every entry** - C and Z effects seen hundreds of times
- **Encoding table in every entry** - Pattern becomes second nature
- **Category labels** - Taxonomy reinforced with each lookup

#### Concrete Before Abstract
- **Syntax first, encoding second** - What you type before the bits
- **Plain language descriptions** - "Add two unsigned values" before technical details
- **Examples that illuminate** - Show *why* you'd use this instruction
- **Procedural operation descriptions** - "First X, then Y, finally Z"

### 3.3 The Power of Cross-References

When someone looks up ADD, showing ADDX, ADDS, ADDSX teaches the *structure* of the instruction set:

- **Family groupings** - ADD family, SUB family, CMP family
- **Contrast pairs** - "See also: SUB (opposite operation)"
- **Prerequisite chains** - "Requires SETQ for burst mode"
- **Alternative approaches** - "For signed values, see ADDS"

### 3.4 Consistent Terminology

Every inconsistency creates confusion. Every consistent use reinforces meaning.

- Define terms once in Part I glossary
- Use those exact terms everywhere
- Never "register" sometimes and "location" other times
- Pick one: "C flag" or "carry flag" - use it consistently

### 3.5 Error Prevention

Knowing what NOT to do is as important as knowing what to do:

- **Notes section for pitfalls** - Common mistakes called out
- **Explicit constraints** - "Dest cannot be immediate"
- **Edge cases** - "When Src is 0, behavior is..."
- **Hardware limitations** - "Maximum 511 without AUGS"

---

## 4. Source Materials & Authority

### 4.1 Primary Sources

| Source | Location | Content | Authority |
|--------|----------|---------|-----------|
| **YAML Instruction Files** | `/engineering/knowledge-base/P2/language/pasm2/` | 375 instruction definitions | PRIMARY - structured, validated |
| **Parallax PASM2 Manual** | `/engineering/ingestion/sources/pasm2-manual/` | Original descriptions, examples | SECONDARY - prose reference |
| **P2 Spreadsheet** | (ingested) | Encoding data, complete inventory | PRIMARY - encoding authority |
| **Silicon Documentation** | (ingested) | Hardware behavior details | PRIMARY - hardware truth |

### 4.2 Authority Hierarchy

When sources conflict:
1. **Silicon documentation** - Hardware behavior is ground truth
2. **YAML files** - Structured, validated data
3. **Spreadsheet** - Encoding accuracy
4. **Parallax manual** - Prose descriptions, examples
5. **Forum posts** - Supplementary only, requires validation

### 4.3 Traceability Requirements

Each instruction entry should be traceable to sources:
- Which YAML file contains the structured data
- Which page of Parallax manual has prose (if any)
- Whether encoding was verified against spreadsheet
- Any silicon doc references for hardware behavior

---

## 4A. Content Verification Protocol (Hallucination Prevention)

**Added:** 2026-01-23
**Derived from:** PASM2 Manual Content Verification Sprint - See `audit/content-verification-sprint-2026-01/`

### Why This Section Exists

The PASM2 manual audit discovered that **hallucinations occur at the moment of writing**, not after. Two critical fabrications (HUBSET "sync" capabilities that don't exist) passed multiple review cycles because no verification protocol existed at write-time.

**Critical insight**: Sections 4.1-4.3 tell you WHERE sources are and WHICH are authoritative. This section tells you HOW TO VERIFY claims before writing them.

### 4A.1 Claim Types and Required Sources

For PASM2 instruction documentation, every claim falls into these categories:

| Claim Type | Required Source | Example Claim |
|------------|-----------------|---------------|
| **Instruction behavior** | YAML `description:` + Silicon Doc | "ADD stores sum in Dest" |
| **Flag effects** | YAML `flags:` field | "C flag set on carry" |
| **Cycle timing** | YAML `clocks:` field | "Takes 2 clock cycles" |
| **Encoding bits** | YAML `encoding:` + Spreadsheet | "Opcode is 0001000" |
| **Syntax forms** | YAML `syntax:` field | "ADD Dest, {#}Src {WC}" |
| **Hardware capability** | Silicon Doc ONLY | "CORDIC computes sin/cos" |
| **Synchronization claims** | Silicon Doc ONLY | "Hub access every 8 clocks" |

### 4A.2 Red-Flag Phrases for PASM2

**STOP and verify when you're about to write:**

| Phrase | Risk Level | Why Suspicious | Action |
|--------|------------|----------------|--------|
| "provides synchronization" | **CRITICAL** | F01/F02 fabrications used this | Find in Silicon Doc or DON'T WRITE |
| "eliminates variation" | **CRITICAL** | Optimization claims need proof | Citation required |
| "side effect of" | HIGH | Invented secondary behaviors | Must be in YAML or Silicon Doc |
| "also enables" | HIGH | Capability creep | Verify the capability exists |
| "automatically" | MEDIUM | Automatic behavior must be documented | Check source for automatic behavior |
| "can be used to" | MEDIUM | Use case attribution | Verify the use case is valid |
| "mechanism for" | MEDIUM | Implementation claim | Must trace to hardware doc |

### 4A.3 The Verification Protocol

**Before writing ANY instruction claim:**

```
┌─────────────────────────────────────────────────────────────────┐
│           PASM2 CLAIM VERIFICATION CHECKLIST                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. What am I claiming? (behavior/timing/capability/syntax)     │
│                                                                 │
│  2. Which source should contain this?                           │
│     □ YAML file: /engineering/knowledge-base/P2/language/pasm2/ │
│     □ Silicon Doc: specific section                             │
│     □ Spreadsheet: encoding data                                │
│                                                                 │
│  3. Can I cite the EXACT location?                              │
│     □ YAML field name and value                                 │
│     □ Silicon Doc page/section                                  │
│     □ Spreadsheet row/column                                    │
│                                                                 │
│  4. Does the source say this EXACTLY?                           │
│     □ YES → Write the claim                                     │
│     □ NO, I'm extrapolating → DON'T WRITE IT                    │
│     □ Source doesn't exist → Mark as gap, don't invent          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4A.4 PASM2-Specific Verification Examples

**Example 1: Correct Verification (ADD instruction)**

Claim to write: "ADD sets the C flag if carry occurs"

1. Claim type: Flag effect
2. Required source: YAML `flags:` field
3. Check: `add.yaml` → `flags: { c: "carry", z: "result == 0" }`
4. Source says exactly this? YES → Write the claim

**Example 2: Blocked Fabrication (HUBSET "sync")**

Attempted claim: "HUBSET provides a synchronization mechanism that eliminates hub access variation"

1. Claim type: Hardware capability
2. Required source: Silicon Doc HUBSET section
3. Check: Silicon Doc lists 5 HUBSET functions: clock config, crystal control, PLL, hub sync mode, cog reset
4. Does "eliminates variation" appear? NO
5. Does "synchronization mechanism" appear? NO (only "sync mode" for specific crystal function)
6. Result: **CLAIM BLOCKED** - This is extrapolation/fabrication

**Example 3: Gap Handling (undocumented timing)**

Claim to write: "WRPIN timing varies based on Smart Pin mode"

1. Claim type: Timing behavior
2. Required source: YAML `clocks:` field
3. Check: YAML shows fixed clock count, no mode variation documented
4. Silicon Doc check: No Smart Pin timing variation table found
5. Result: **Don't write as fact** → Instead write: "Timing is [X clocks] as specified; mode-specific variations, if any, are not documented in available sources."

### 4A.5 Source Location Quick Reference

| Content | Primary Location |
|---------|------------------|
| Instruction YAML files | `/engineering/knowledge-base/P2/language/pasm2/` |
| Silicon documentation | `/engineering/ingestion/sources/silicon/` |
| Parallax draft manual | `/engineering/ingestion/sources/pasm2-manual/` |
| Encoding spreadsheet | (ingested data, cross-reference via YAML) |
| Audit findings | `./audit/` (this manual's audit folder) |

### 4A.6 What To Do When Source Doesn't Exist

1. **Don't invent** - If it's not documented, we can't claim it
2. **Mark the gap** - Use comment markers: `<!-- NEEDS_VERIFICATION: [claim] -->`
3. **Document the unknown** - "Behavior in this case is not specified in available sources"
4. **Check audit findings** - Previous verification sprint may have addressed this

### 4A.7 Full Audit Methodology Reference

For comprehensive post-write audit procedures, see:
- `engineering/operations/process/TECHNICAL-DOCUMENT-AUDIT-METHODOLOGY.md` (generic methodology)
- `./audit/` (this manual's specific audit documentation)

---

## 5. Instruction Entry Specification

### 5.1 Entry Layout (Parallax Format)

Each instruction entry follows this structure, matching the Parallax draft manual format:

```
INSTRUCTION_NAME
Short description
Category Link - One-line summary of instruction purpose.

SYNTAX  (one line per form)
INSTR1  {#}Src  {effects}
INSTR2  {#}Src  {effects}

**Result:** Brief statement of what happens.

  • Parameter1 description
  • Parameter2 description
  • Effects description

┌──────┬─────────┬─────┬───────────┬───────────┬───────┬─────────┬─────────┬────────┐
│ COND │  INSTR  │ FX  │   DEST    │    SRC    │ Write │ C Flag  │ Z Flag  │ Clocks │
├──────┼─────────┼─────┼───────────┼───────────┼───────┼─────────┼─────────┼────────┤
│ EEEE │ 0001000 │ CZI │ DDDDDDDDD │ SSSSSSSSS │   D   │ carry   │ D = 0   │   2    │
└──────┴─────────┴─────┴───────────┴───────────┴───────┴─────────┴─────────┴────────┘
(footnotes if needed)

**Related:** INSTR1, INSTR2, INSTR3

**Explanation:**
Prose description of instruction behavior. Multiple paragraphs as needed.

Flag behavior paragraphs.

Additional details, edge cases, usage notes.
```

### 5.2 Entry Structure Details

#### Header Block
- **Instruction Name** - Large heading, the mnemonic(s)
- **Short description** - Human-readable name (e.g., "Add unsigned", "Compare signed")
- **Category** - Hyperlinked category (e.g., "Math Instruction", "I/O Pin Instruction")
- **One-liner** - Brief summary after the category

#### Syntax Block
- One line per syntax form
- Monospace formatting
- Shows all valid parameter combinations

#### Result Line
- Single sentence stating what the instruction produces
- Appears after a horizontal rule

#### Parameters
- Bullet list describing each parameter
- Includes Dest, Src, and any effects (WC, WZ, WCZ)

#### Encoding Table
- **Horizontal table format** with styled gray header row
- Columns: COND, INSTR, FX, DEST, SRC, Write, C Flag, Z Flag, Clocks
- **One row per encoding variant** (see Section 5.3)
- Monospace font for encoding values
- "—" indicates no effect on a flag
- Footnotes (superscript markers) for conditional behaviors

#### Related Line
- Inline list of related instruction hyperlinks
- No categories - just comma-separated names

#### Explanation Section
- Prose paragraphs describing behavior in detail
- Flag behavior described in dedicated paragraphs
- Examples embedded in prose when helpful

### 5.3 When Multiple Encoding Rows Appear

The encoding table has **one row per distinct encoding**. Multiple rows appear when:

**1. Multiple related instructions share an entry:**
```
DIRZ / DIRNZ
...
│ EEEE │ 1101011 │ CZI │ DDDDDDDDD │ 001000100 │ DIRx │ ... │
│ EEEE │ 1101011 │ CZI │ DDDDDDDDD │ 001000101 │ DIRx │ ... │
```
Each instruction variant (DIRZ, DIRNZ) gets its own row.

**2. Multiple syntax forms for one instruction:**
```
GETBYTE Dest, {#}Src, #Num
GETBYTE Dest
...
│ EEEE │ 1000111 │ NNI │ DDDDDDDDD │ SSSSSSSSS │  D  │ ... │
│ EEEE │ 1000111 │ 000 │ DDDDDDDDD │ 000000000 │  D  │ ... │
```
The first form uses Src and Num; the second form (for ALTGB) has fixed encoding.

**3. Instruction families documented together:**
```
JCT1/2/3 / JNCT1/2/3
...
│ EEEE │ 1011110 │ 01I │ 000000001 │ SSSSSSSSS │ PC¹ │ ... │
│ EEEE │ 1011110 │ 01I │ 000000010 │ SSSSSSSSS │ PC¹ │ ... │
│ EEEE │ 1011110 │ 01I │ 000000011 │ SSSSSSSSS │ PC¹ │ ... │
│ EEEE │ 1011110 │ 01I │ 000010001 │ SSSSSSSSS │ PC¹ │ ... │
│ EEEE │ 1011110 │ 01I │ 000010010 │ SSSSSSSSS │ PC¹ │ ... │
│ EEEE │ 1011110 │ 01I │ 000010001 │ SSSSSSSSS │ PC¹ │ ... │
```
Six instructions (JCT1, JCT2, JCT3, JNCT1, JNCT2, JNCT3) = six rows.

**Key principle:** Each unique opcode encoding = one table row.

### 5.4 Encoding Table Column Reference

| Column | Content | Notes |
|--------|---------|-------|
| COND | `EEEE` | Condition field (always EEEE for conditional execution) |
| INSTR | 7-bit opcode | The instruction's opcode bits |
| FX | `CZI` or variant | Flag/immediate bits; may show `NNI`, `000`, etc. |
| DEST | `DDDDDDDDD` | 9-bit destination field |
| SRC | `SSSSSSSSS` | 9-bit source field; may be fixed value |
| Write | What's written | `D`, `D and PC`, `DIRx`, `—`, etc. |
| C Flag | C behavior | Effect description or `—` for no change |
| Z Flag | Z behavior | Effect description or `—` for no change |
| Clocks | Cycle count | May be complex: `2 or 4 / 2 or 13-20` |

### 5.5 Table Footnotes

Use superscript markers for conditional behaviors:

```
│ ... │ PC¹ │ — │ — │ 2 or 4 / 2 or 13-20 │
...
¹ PC is written only when the counter event flag is set (or is clear in syntax 4-6).
```

### 5.6 Section Requirements

| Section | Required? | Notes |
|---------|-----------|-------|
| Instruction Name | YES | Mnemonic(s) as heading |
| Short description | YES | Human-readable name |
| Category + one-liner | YES | Linked category, brief summary |
| Syntax | YES | All valid forms, one per line |
| Result | YES | One-sentence outcome statement |
| Parameters | YES | Bullet list of all parameters |
| Encoding Table | YES | One row per encoding variant |
| Related | YES | Inline hyperlinked list |
| Explanation | YES | Prose description of behavior |

### 5.7 Writing Guidelines

**Syntax:** One line per form. Monospace. Show all valid combinations.

**Result:** Single sentence. States what the instruction produces or affects.

**Parameters:** Bullet list. Be precise about what each can be (register, immediate, augmented).

**Encoding Table:** Generate from YAML. One row per encoding. Use "—" for no flag effect.

**Related:** Inline comma-separated list. Hyperlink each instruction name.

**Explanation:**
- Prose paragraphs, not numbered steps
- Describe the operation clearly
- Dedicate paragraphs to C flag and Z flag behavior when they're updated
- Include usage context and edge cases
- Embed examples in prose when they illuminate

### 5.8 Directive Entry Format

Directives are assembler-time constructs, not runtime instructions. They have a different format:

```
DIRECTIVE_NAME
Short description
Directive - One-line summary of directive purpose.

DAT
  code_and_data_statements
  DIRECTIVE
  data_statements

**Result:** Brief statement of what the directive does.

  • Parameter descriptions

**Explanation:**
Prose description of directive behavior.

**Example**
Code example showing typical usage, often with before/after memory diagrams.
```

**Key differences from instructions:**
- **No encoding table** - Directives don't generate machine code
- **Syntax shown in DAT context** - Shows usage within DAT blocks
- **Memory diagrams** - TikZ diagrams showing byte/word/long alignment (where helpful)
- **Before/after examples** - Visual demonstration of effect

**Memory alignment diagrams (TikZ):**
For directives like ALIGNW, ALIGNL, BYTE, WORD, LONG, include memory layout diagrams showing:
- Byte positions within longs
- Address boundaries (L0, L1, L2... for longs; W0, W1... for words; B0, B1... for bytes)
- Before and after states when relevant

---

## 6. Terminology Standards

### 6.1 Canonical Terms

Use these terms consistently throughout:

| Canonical Term | NOT These | Notes |
|----------------|-----------|-------|
| C flag | carry flag, C, carry | Always "C flag" in prose |
| Z flag | zero flag, Z, zero | Always "Z flag" in prose |
| COG | cog, Cog | All caps |
| Hub | hub, HUB | Title case |
| LUT | lut, Lut | All caps (Lookup Table) |
| register | location, address, variable | For COG memory locations |
| immediate | literal, constant, value | For # values |
| effect | modifier, flag effect | For WC, WZ, WCZ |
| condition | conditional, IF | For IF_x prefixes |

### 6.2 Notation Standards

| Notation | Meaning |
|----------|---------|
| `Dest` | Destination register |
| `Src` | Source operand |
| `{#}` | Optional immediate prefix |
| `{effect}` | Optional WC/WZ/WCZ |
| `D` | Destination in encoding |
| `S` | Source in encoding |
| `EEEE` | Condition field in encoding |
| `$` | Hexadecimal prefix or current address |
| `%` | Binary prefix |
| `##` | 32-bit augmented immediate |

---

## 7. Quality Requirements

### 7.1 Validation Checklist

Each instruction entry must pass:

- [ ] **Completeness** - All required sections present
- [ ] **Syntax accuracy** - All forms verified against YAML
- [ ] **Encoding accuracy** - Bit pattern matches spreadsheet
- [ ] **Flag accuracy** - C and Z behavior verified
- [ ] **Timing accuracy** - Cycle count verified
- [ ] **Cross-references valid** - All "Related" instructions exist
- [ ] **Example compiles** - If present, tested with pnut_ts
- [ ] **Terminology consistent** - Uses canonical terms

### 7.2 Code Example Testing

All code examples must:
1. Compile with `pnut_ts` without errors
2. Be syntactically correct PASM2
3. Demonstrate the instruction's purpose
4. Include explanatory comments

### 7.3 Coverage Tracking

Maintain tracking of:
- Instructions with complete entries
- Instructions needing enhancement
- Instructions with unverified encoding
- Instructions lacking examples (where examples would help)

---

## 8. Production Workflow

### 8.1 Template Generation

1. **Extract from YAML** - Pull structured data from knowledge base
2. **Apply entry template** - Generate skeleton with available data
3. **Mark gaps** - Flag sections needing manual input
4. **Queue for enhancement** - Track what needs work

### 8.2 Enhancement Process

1. **Select instruction** - Prioritize by usage frequency or gap severity
2. **Research sources** - Check Parallax manual, silicon doc, forums
3. **Write/enhance sections** - Fill gaps, improve descriptions
4. **Validate** - Run checklist, test examples
5. **Cross-reference** - Ensure related instructions link correctly
6. **Mark complete** - Update tracking

### 8.3 Assembly and Output

1. **Combine Part I chapters** - Architectural foundation
2. **Sort Part II entries** - Alphabetical order
3. **Generate appendices** - Encoding tables, categorical index
4. **Build index** - Comprehensive cross-reference
5. **Output markdown** - Complete manual source
6. **Generate PDF** - Via PDF Forge

### 8.4 PDF Generation

- **Template:** To be created (similar to other P2KB manuals)
- **Output directory:** `/engineering/pdf-forge/production/p2-assembly-language-manual/`
- **Lua filters:** As needed for formatting
- **Request file:** `request.json` with appropriate pandoc_args

### 8.5 Encoding Tables and TikZ Diagrams

This manual uses two visual approaches:
1. **LaTeX Tables** for instruction encodings (dense, tabular format matching Parallax draft)
2. **TikZ Diagrams** for architectural concepts, memory layouts, and bit manipulation visualizations

#### 8.5.1 Instruction Encoding: Tables (Not Diagrams)

Instruction encodings use a **horizontal table format** with styled gray header:

```
┌──────┬─────────┬─────┬───────────┬───────────┬───────┬─────────┬─────────┬────────┐
│ COND │  INSTR  │ FX  │   DEST    │    SRC    │ Write │ C Flag  │ Z Flag  │ Clocks │
├──────┼─────────┼─────┼───────────┼───────────┼───────┼─────────┼─────────┼────────┤
│ EEEE │ 0001000 │ CZI │ DDDDDDDDD │ SSSSSSSSS │   D   │  carry  │  D = 0  │   2    │
└──────┴─────────┴─────┴───────────┴───────────┴───────┴─────────┴─────────┴────────┘
```

**Why tables instead of TikZ diagrams:**
- Matches the Parallax draft manual format exactly
- Scales naturally for multi-row encodings (multiple syntax forms)
- Easier to generate programmatically from YAML
- More compact and information-dense
- Includes result columns (Write, C Flag, Z Flag, Clocks) in same view

**Table styling (LaTeX):**
- `booktabs` for clean horizontal rules
- `colortbl` for gray header background
- `\ttfamily` for monospace encoding values
- Consistent column widths across all entries

#### 8.5.2 TikZ Diagrams: Where They Add Value

TikZ is reserved for visual concepts that benefit from graphical representation:

**Part I Architectural Diagrams:**
- COG memory map (addresses 0-511, showing register regions)
- Hub memory organization (512KB layout)
- LUT memory layout (512 longs per COG)
- Egg beater hub access timing diagram
- Instruction pipeline visualization
- 8-COG parallel execution overview

**Directive Memory Layout Diagrams:**
- Byte/Word/Long alignment (ALIGNW, ALIGNL examples)
- Hub address boundaries
- Before/after memory state comparisons
- Byte ordering within longs (little-endian)

**Bit/Nibble Reordering Diagrams:**
Instructions that rearrange bits or nibbles benefit from before/after visualizations:
- SPLITB, SPLITW - Bit/word splitting operations
- MERGB, MERGW - Bit/word merging operations
- MOVBYTS - Byte shuffling within a long
- ROLNIB, ROLBYTE, ROLWORD - Nibble/byte/word rotation
- SETNIB, SETBYTE, SETWORD - Nibble/byte/word insertion
- GETNIB, GETBYTE, GETWORD - Nibble/byte/word extraction
- REV - Bit reversal

These diagrams show the 32-bit value with labeled positions, arrows indicating movement, and before/after states.

**Special Register Maps:**
- DIRA/DIRB bit-to-pin assignments (32 bits → 32 pins)
- Special purpose register address map ($1F0-$1FF)
- PTRA/PTRB pointer structure

**CORDIC Operation Diagrams:**
- Input/output register flow
- Operation queue visualization

#### 8.5.3 TikZ Template Strategy

**Templates to Create:**

1. **`\MemoryMap{start}{end}{regions}`**
   - Generic memory region visualization
   - Used for COG, Hub, and LUT maps
   - Configurable labels and highlighting

2. **`\ByteAlignment{size}{values}`**
   - Shows byte ordering in memory
   - Little-endian visualization
   - Address annotations (L0, L1, W0, W1, B0-B3)

3. **`\BitReorder{before}{after}{arrows}`**
   - 32-bit value with numbered bit positions
   - Shows before and after states
   - Arrows or color coding to show movement
   - Used for SPLITB, MERGB, MOVBYTS, etc.

4. **`\RegisterMap{name}{fields}`**
   - Generic register bit field layout
   - Shows bit positions and field names
   - Used for special registers, configuration values

#### 8.5.4 Implementation

**Reference Implementation:**
See `/engineering/document-production/workspace/p2-pasm-desilva-style/templates/p2kb-desilva-diagrams.sty` for existing TikZ diagram definitions.

**TikZ Libraries Required:**
```latex
\RequirePackage{tikz}
\usetikzlibrary{shapes.geometric, arrows.meta, positioning, calc, decorations.pathreplacing}
```

**Color Palette:**
```latex
\definecolor{diagram-box}{HTML}{E8E8E8}      % Light gray fill
\definecolor{diagram-border}{HTML}{666666}   % Medium gray border
\definecolor{diagram-highlight}{HTML}{D4E8D4} % Light green highlight
\definecolor{diagram-text}{HTML}{333333}     % Dark gray text
```

#### 8.5.5 Diagram Inventory

| Diagram Type | Count | Notes |
|--------------|-------|-------|
| Part I Architectural | ~8 | COG, Hub, LUT maps, pipeline, timing |
| Directive Memory | ~5 | ALIGNW, ALIGNL, BYTE/WORD/LONG layouts |
| Bit Reordering | ~12 | SPLITB/W, MERGB/W, MOVBYTS, ROLxxx, etc. |
| Special Registers | ~4 | $1F0-$1FF map, PTRA/PTRB structure |
| CORDIC | ~2 | Queue operation, register flow |

**Total TikZ diagrams:** ~31 (vs. 359 encoding tables)

---

## 9. Maintenance & Evolution

### 9.1 Update Procedures

When Parallax releases new information:
1. Identify affected instructions
2. Update YAML files first (source of truth)
3. Regenerate affected manual entries
4. Update change log
5. Increment version number

### 9.2 Version Control

- Manual version tracks with P2KB releases
- Change log in front matter documents updates
- Git history provides full audit trail

### 9.3 Change Documentation

Every update should document:
- What changed
- Why it changed (source reference)
- When it changed
- Who validated the change

---

## 10. Voice Guidelines (Summary)

*Detailed voice guidelines in separate `voice-guide.md`*

### Core Voice Characteristics

- **Technical** - Precise, accurate, unambiguous
- **Authoritative** - This is the source of truth
- **Concise** - Every word serves a purpose
- **Consistent** - Same terminology, same structure
- **Complete** - No gaps, no "probably"

### What We Say

- Definitive statements: "The C flag is set if..."
- Precise descriptions: "Dest receives the sum of Dest and Src"
- Clear constraints: "Src must be a register or 9-bit immediate"

### What We Don't Say

- Hedging: "probably", "typically", "usually"
- Tutorial voice: "Let's explore...", "You might wonder..."
- Informal: "basically", "just", "simply"
- Vague: "works like", "similar to" (without specifics)

---

## Appendix: Exemplar Instruction Entry (Parallax Format)

```
ADD
Add unsigned
Math Instruction - Add two unsigned values.

ADD  Dest, {#}Src  {WC|WZ|WCZ}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Result:** The sum of Dest and Src is stored in Dest.

  • Dest is the register containing the first operand and receiving the sum.
  • Src is a register, 9-bit literal, or 32-bit augmented literal to add to Dest.
  • WC, WZ, or WCZ are optional effects to update flags.

┌──────┬─────────┬─────┬───────────┬───────────┬───────┬─────────┬─────────┬────────┐
│ COND │  INSTR  │ FX  │   DEST    │    SRC    │ Write │ C Flag  │ Z Flag  │ Clocks │
├──────┼─────────┼─────┼───────────┼───────────┼───────┼─────────┼─────────┼────────┤
│ EEEE │ 0001000 │ CZI │ DDDDDDDDD │ SSSSSSSSS │   D   │  carry  │  D = 0  │   2    │
└──────┴─────────┴─────┴───────────┴───────────┴───────┴─────────┴─────────┴────────┘

**Related:** ADDX, ADDS, ADDSX, SUB

**Explanation:**

ADD adds the unsigned values of Dest and Src and stores the 32-bit result in Dest.

If the WC or WCZ effect is specified, the C flag is set (1) if the addition
produces a carry out of bit 31, or is cleared (0) otherwise.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result
equals zero, or is cleared (0) otherwise.

For 64-bit addition, use ADD with WC on the low longs, then ADDX on the high
longs to incorporate the carry:

    add     X_lo, Y_lo      wc      ' Add low longs, capture carry
    addx    X_hi, Y_hi              ' Add high longs with carry-in

For signed addition with signed overflow detection, use ADDS instead.
```

---

## Code Line Budget

**Max code columns (K): 76**

Provenance: Inherited from the shared platform code-box stack. As of the 2026-06-10
platform migration this manual renders code through the platform `IOSPBlock` / `Spin2Block`
(via `p2kb-platform-code-coloring.lua`) on the platform page geometry
(`top/bottom=0.75in, left/right=1in`) and code-box insets (`left=30pt, right=10pt`) —
geometry identical to the certified torture-test instrument that calibrated K=76. Code
boxes do not wrap, so an over-budget line is an authorship defect: fix it with the legal
Spin2 `...` continuation, or by moving / splitting a trailing comment — never a typeset
wrap.

---

*Last Updated: 2026-06-10*
*Version: 1.2 - Platform migration; added Code Line Budget (K=76, inherited from platform)*
