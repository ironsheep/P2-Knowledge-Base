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
  - **10 directives** (ORG, BYTE, WORD, LONG, RES, FIT, etc.)
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
  - 10 directives (ORG, ORGH, BYTE, WORD, LONG, RES, FIT, ALIGNL, ALIGNW, HUBEXEC)
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

## 5. Instruction Entry Specification

### 5.1 Complete Entry Template

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INSTRUCTION_NAME
Full Name | Category

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AT A GLANCE
┌─────────────────────────────────────────────────────────────────────┐
│  INSTR Dest, {#}Src {WC|WZ|WCZ}                                    │
│  Cycles: N    Hub: Yes/No    Flags: C=effect, Z=effect             │
└─────────────────────────────────────────────────────────────────────┘

SYNTAX
  INSTR Dest, {#}Src {WC|WZ|WCZ}
  INSTR Dest {WC|WZ|WCZ}
  (all valid syntactic forms)

PARAMETERS
  • Dest - Register to receive result (and/or source operand)
  • Src - Register, 9-bit immediate, or 32-bit augmented immediate
  • WC - Update C flag based on result
  • WZ - Update Z flag based on result
  • WCZ - Update both C and Z flags

ENCODING
  ┌──────────────────────────────────────────────────────────────────┐
  │ EEEE  OOOOOOO  CZI  DDDDDDDDD  SSSSSSSSS                        │
  │ cond  opcode   flg  dest       src                               │
  │                                                                   │
  │ EEEE = Condition (IF_x)                                          │
  │ OOOOOOO = Opcode bits                                            │
  │ C = WC effect bit                                                │
  │ Z = WZ effect bit                                                │
  │ I = Immediate source (1 = #Src)                                  │
  │ DDDDDDDDD = Destination register address                         │
  │ SSSSSSSSS = Source register/immediate                            │
  └──────────────────────────────────────────────────────────────────┘

OPERATION
  Precise description of instruction behavior:
  1. What values are read
  2. What computation occurs
  3. What values are written
  4. How flags are affected

  C Flag: [description of C flag behavior]
  Z Flag: [description of Z flag behavior]

TIMING
  Execution: N clock cycles
  Hub Access: Yes/No (if Yes, describe timing)
  Pipeline: [any pipeline considerations]

RELATED INSTRUCTIONS
  • Similar: [instructions with similar function]
  • Family: [instruction variants - ADDX, ADDS, ADDSX]
  • See also: [complementary instructions]
  • Contrast: [opposite or alternative instructions]

EXAMPLE
  ' Brief, illuminating code example
  ' Comments explain the WHY, not just the what
          instr   dest, src       wc      ' Explanation of this usage

NOTES
  ⚠️ Pitfall: [common mistakes to avoid]
  💡 Tip: [non-obvious useful techniques]
  🔧 Hardware: [silicon-level details if relevant]

SOURCE REFERENCES
  • YAML: /engineering/knowledge-base/P2/language/pasm2/instr.yaml
  • Parallax Manual: p.XX (if documented)
  • Encoding verified: Yes/No

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 5.2 Section Requirements

| Section | Required? | Notes |
|---------|-----------|-------|
| Instruction Name | YES | Mnemonic as heading |
| Full Name / Category | YES | Human-readable name and functional category |
| At a Glance | YES | Quick-reference box |
| Syntax | YES | All valid forms |
| Parameters | YES | All parameters explained |
| Encoding | YES | Bit-level format |
| Operation | YES | Precise behavioral description |
| Timing | YES | Cycle count, hub access |
| Related Instructions | YES | Cross-references |
| Example | OPTIONAL | Include when it illuminates; omit for trivial instructions |
| Notes | OPTIONAL | Include when pitfalls, tips, or hardware details exist |
| Source References | YES | Traceability |

### 5.3 Writing Guidelines for Each Section

**At a Glance:** Most common syntax form, cycle count, flag summary. One quick look tells experienced dev what they need.

**Syntax:** Show ALL valid forms. Use consistent notation: `{#}` for optional immediate, `{effect}` for optional effects.

**Parameters:** Bullet list. Be precise about what each parameter can be (register, immediate, augmented).

**Encoding:** Visual box format. Show the bit fields clearly. Include legend for field meanings.

**Operation:** Procedural description. Number the steps. Be explicit about flag behavior - don't assume reader remembers from elsewhere.

**Timing:** Always include cycle count. Note hub access if applicable. Pipeline effects for advanced instructions.

**Related Instructions:** This is a teaching tool. Group by relationship type (similar, family, contrast).

**Example:** Only include if it adds value. The example should show *why* you'd use this instruction, not just that you can.

**Notes:** Categorize with emoji markers. Keep concise - this isn't a tutorial.

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

### 8.5 TikZ Diagrams

This manual uses **TikZ**, a LaTeX-based vector diagram language, to recreate and improve upon all diagrams from the original Parallax draft. This ensures visual consistency, professional quality, and maintainability.

#### 8.5.1 Why TikZ for All Diagrams

**Quality Benefits:**
- Resolution-independent vector output (crisp at any zoom/print size)
- Consistent with document typography
- No pixel artifacts or compression issues
- Professional appearance throughout

**Maintainability Benefits:**
- Diagrams are code - version controlled and diff-able
- Fix a typo? Edit one line of code
- Change color scheme? Update one style definition
- Add new instruction? Copy template, change values

**Pedagogical Benefits:**
- Consistent visual structure reinforces learning
- Readers develop instant recognition of patterns
- Visual consistency = reduced cognitive load
- Same diagram style throughout builds familiarity

#### 8.5.2 Diagram Types to Recreate

**Instruction Encoding Diagrams (every instruction):**
```
┌────────┬─────────┬─────┬───────────┬───────────┐
│  EEEE  │ OOOOOOO │ CZI │ DDDDDDDDD │ SSSSSSSSS │
│  31-28 │  27-21  │20-18│   17-9    │    8-0    │
│  cond  │ opcode  │flags│   dest    │    src    │
└────────┴─────────┴─────┴───────────┴───────────┘
```
- Bit field boundaries clearly marked
- Field names and bit positions labeled
- Consistent styling across all 359 instructions

**Byte/Word/Long Alignment Diagrams:**
- Memory layout showing data alignment
- Hub address boundaries
- Byte ordering within longs (little-endian visualization)
- Useful for BYTE, WORD, LONG directives and RDxxxx/WRxxxx instructions

**Special Register Maps:**
- DIRA/DIRB bit-to-pin assignments (32 bits → 32 pins)
- INA/INB/OUTA/OUTB layouts
- Special purpose register address map (496-511)
- PTRA/PTRB pointer register structure

**Architectural Diagrams (Part I):**
- COG memory map (addresses 0-511, showing register regions)
- Hub memory organization (512KB layout)
- LUT memory layout (512 longs per COG)
- Egg beater hub access timing diagram
- Instruction pipeline visualization

**CORDIC Operation Diagrams:**
- Input/output register flow
- Operation modes visualization
- Timing/pipeline for CORDIC operations

**Smart Pin Diagrams (overview only):**
- Pin configuration register layout
- Basic mode selection bits
- (Detailed Smart Pin diagrams belong in Smart Pins manual)

#### 8.5.3 TikZ Template Strategy

**Base Templates to Create:**

1. **`\InstructionEncoding{opcode}{flags}{...}`**
   - Parameterized template for any instruction's encoding
   - Accepts opcode bits, flag effects, field values
   - Produces consistent 32-bit encoding diagram

2. **`\MemoryMap{start}{end}{regions}`**
   - Generic memory region visualization
   - Used for COG, Hub, and LUT maps
   - Configurable labels and highlighting

3. **`\BitFieldDiagram{width}{fields}`**
   - Generic bit field layout
   - Used for registers, configuration values
   - Shows bit positions and field names

4. **`\ByteAlignment{size}{values}`**
   - Shows byte ordering in memory
   - Little-endian visualization
   - Address annotations

#### 8.5.4 Implementation

**Reference Implementation:**
See `/engineering/document-production/workspace/p2-pasm-desilva-style/templates/p2kb-desilva-diagrams.sty` for existing TikZ diagram definitions used in the DeSilva manual.

**TikZ Libraries Required:**
```latex
\RequirePackage{tikz}
\usetikzlibrary{shapes.geometric, arrows.meta, positioning, calc, decorations.pathreplacing}
```

**Color Palette (consistent with P2KB manuals):**
```latex
\definecolor{diagram-box}{HTML}{E8E8E8}      % Light gray fill
\definecolor{diagram-border}{HTML}{666666}   % Medium gray border
\definecolor{diagram-highlight}{HTML}{D4E8D4} % Light green highlight
\definecolor{diagram-text}{HTML}{333333}     % Dark gray text
```

**Creating New Diagrams:**
1. Define diagram as LaTeX command in `.sty` package
2. Use consistent color palette
3. Parameterize where possible for reuse
4. Test in PDF Forge before committing
5. Document diagram purpose and parameters

#### 8.5.5 Diagram Inventory

Track diagram creation progress:

| Diagram Type | Count | Status |
|--------------|-------|--------|
| Instruction Encoding | 359 | Template needed |
| Directive Layouts | ~5 | Template needed |
| Part I Architectural | ~8 | Template needed |
| Special Registers | ~6 | Template needed |
| CORDIC Operations | ~4 | Template needed |

**Goal:** All diagrams from Parallax draft recreated in TikZ, plus new diagrams where they improve understanding.

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

## Appendix: Exemplar Instruction Entry

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ADD
Add Unsigned | Math Instruction

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AT A GLANCE
┌─────────────────────────────────────────────────────────────────────┐
│  ADD Dest, {#}Src {WC|WZ|WCZ}                                      │
│  Cycles: 2    Hub: No    Flags: C=carry, Z=zero                    │
└─────────────────────────────────────────────────────────────────────┘

SYNTAX
  ADD Dest, {#}Src {WC|WZ|WCZ}

PARAMETERS
  • Dest - Register containing first operand; receives the sum
  • Src - Register, 9-bit immediate (#0-511), or 32-bit augmented immediate (##value)
  • WC - Set C flag if unsigned overflow (carry out of bit 31)
  • WZ - Set Z flag if result is zero
  • WCZ - Set both C and Z flags

ENCODING
  ┌──────────────────────────────────────────────────────────────────┐
  │ EEEE  0001000  CZI  DDDDDDDDD  SSSSSSSSS                        │
  │                                                                   │
  │ EEEE = Condition (default: 1111 = always)                        │
  │ 0001000 = ADD opcode                                             │
  │ C = 1 if WC specified                                            │
  │ Z = 1 if WZ specified                                            │
  │ I = 1 if Src is immediate (#)                                    │
  │ DDDDDDDDD = Destination register (0-511)                         │
  │ SSSSSSSSS = Source register or 9-bit immediate                   │
  └──────────────────────────────────────────────────────────────────┘

OPERATION
  1. Read the value in Dest
  2. Read the value in Src (or use immediate value)
  3. Compute Dest + Src as unsigned 32-bit addition
  4. Write the 32-bit result to Dest

  C Flag: Set to 1 if addition produces carry (overflow beyond 32 bits);
          cleared to 0 otherwise. Only updated if WC or WCZ specified.

  Z Flag: Set to 1 if result is zero; cleared to 0 otherwise.
          Only updated if WZ or WCZ specified.

TIMING
  Execution: 2 clock cycles
  Hub Access: No
  Pipeline: Standard execution, no stalls

RELATED INSTRUCTIONS
  • Family: ADDX (extended), ADDS (signed), ADDSX (signed extended)
  • Contrast: SUB (subtraction)
  • See also: ADDCT1/2/3 (counter events), ADDPIX (pixel addition)

EXAMPLE
  ' 64-bit addition: result in X_hi:X_lo
          add     X_lo, Y_lo      wc      ' Add low longs, MUST capture carry
          addx    X_hi, Y_hi              ' Add high longs with carry-in

NOTES
  ⚠️ Pitfall: For multi-long addition, forgetting WC on the first ADD
     causes incorrect results. The carry MUST propagate to ADDX.

  💡 Tip: ADD treats both operands as unsigned. For signed addition
     where you need signed overflow detection, see ADDS.

SOURCE REFERENCES
  • YAML: /engineering/knowledge-base/P2/language/pasm2/add.yaml
  • Parallax Manual: p.32
  • Encoding verified: Yes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

*Last Updated: 2025-11-26*
*Version: 1.0 - Initial Creation Guide*
