# Parallax Draft PASM2 Manual Comparison Audit

**Audit Date:** 2025-12-04
**Draft Source:** `engineering/ingestion/sources/pasm2-manual/` (November 2022, 162 pages)
**Our Manual:** `engineering/document-production/manuals/p2-assembly-language-manual/`

---

## Executive Summary

Comprehensive comparison of the Parallax Draft PASM2 Manual against our new P2 Assembly Language Reference Manual to identify content gaps and ensure no valuable information is lost.

---

## Audit Findings and Decisions

### 1. Multi-Long Operations Tutorial
**Draft Location:** Pages 11-14
**Status:** APPROVED FOR MIGRATION

**Finding:** The draft contains a comprehensive 4-page tutorial with:
- Step-by-step examples for 64-bit and 96-bit unsigned/signed arithmetic
- Visual hex/decimal calculation diagrams showing carry propagation
- Explicit guidance on instruction sequencing (ADD → ADDX → ADDX for unsigned, ADD → ADDX → ADDSX for signed)

**Our Source:** Found Chip Gracey's authoritative 128-bit examples at:
`engineering/ingestion/external-inputs/from-Chip/math-pasm.txt`

**Decision:** Create comprehensive Multi-Long Operations chapter using Chip's 128-bit source as the pattern. Include ALL intermediate forms:
- 32-bit (single-long) - baseline
- 64-bit (double-long) - ADD + ADDX/ADDSX
- 96-bit (triple-long) - ADD + ADDX + ADDX/ADDSX
- 128-bit (quad-long) - ADD + ADDX + ADDX + ADDX/ADDSX

Cover ADD, SUB, and CMP for both signed and unsigned. This will be comprehensive but highly useful.

**Location:** Part I, new chapter or section in Chapter 3

---

### 2. Expression Operators
**Draft Location:** Page 28
**Status:** APPROVED FOR MIGRATION

**Finding:** Complete operator table for PASM2 constant expressions:

| Category | Operators |
|----------|-----------|
| Unary | `!` (NOT), `+` (positive), `-` (negate) |
| Binary Bitwise | `>>`, `<<`, `&`, `\|`, `^` |
| Binary Arithmetic | `+`, `-`, `*`, `/`, `+/`, `//`, `+//` |
| Limits | `#>` (min), `<#` (max) |
| Comparison | `<`, `+<`, `>`, `+>`, `<=`, `+<=`, `>=`, `+>=`, `==`, `<>` |
| Boolean | `!!`, `&&`, `\|\|`, `^^`, `<=>` |
| Ternary | `? :` |

**Decision:** Add to Part I Chapter 2 (Instruction Format) as new section "Constant Expressions and Operators". Rationale: Operators are fundamental syntax needed immediately, not reference material for occasional lookup.

**Location:** Part I Chapter 2, Section 2.x

---

### 3. Term Definitions / Glossary
**Draft Location:** Page 29
**Status:** APPROVED - CREATE APPENDIX G

**Finding:** Precise definitions for encoding terms:
- A/Addr - 20-bit relative/absolute address
- C/Carry Flag - Detailed explanation with multiple meanings
- D/Dest/Destination - 9-bit register address or 32-bit augmented value
- H/Hub Long - Hub RAM long for subroutine context
- I - Immediate flag meaning
- K/Stack - 8-level hardware stack
- L - Literal flag
- N - Index number (0-1, 0-3, 0-7)
- PC - Program counter behavior
- R - Relative flag
- Result - Value written at instruction end
- S/Src/Source - 9-bit literal or register address
- W - Register to write (PA, PB, PTRA, PTRB)
- Z/Zero Flag - Detailed explanation

**Decision:** Create Appendix G with these term definitions. Front matter already promises "Appendix G: Glossary" but file doesn't exist.

**Location:** Part III Appendix G

---

### 4. PR0-PR7 Shared Registers
**Draft Location:** Page 27
**Status:** ✅ COMPLETE (2025-12-04)

**Finding:** Draft documents:
```
PR0..PR7    PASM2 to Spin2 shared registers
```
These are at COG addresses $1D8-$1DF (decimal 472-479).

**Completed Work:**
1. ✅ Added PR0-PR7 to Part II Special Registers section (`opus-master/part-ii/special-registers.md`)
2. ✅ PASM2 YAML consolidated at `deliverables/ai/P2/language/pasm2/registers/pr-registers.yaml`
3. ✅ Spin2 YAML at `deliverables/ai/P2/language/spin2/registers/pr-registers.yaml`
4. ✅ Removed fabricated parameter mapping conventions (not in official docs)

**Note:** Official Parallax documentation only states PR0-PR7 provide "communication mechanism" - no parameter/return value conventions are defined.

---

### 5. Appendix B Timing Enhancement
**Draft Location:** Pages 148-159 (PASM2 IN BRIEF)
**Status:** IN RESEARCH - Postponed pending user clarification

**Finding:** The draft's "PASM2 IN BRIEF" section includes clock cycle timing for every instruction in compact reference format. Our Appendix B (Categorical Index) lists instructions by category but doesn't include timing.

**Options identified:**
- Option A: Add "Clocks" column to Appendix B tables
- Option B: Create separate Quick Reference Card
- Option C: Leave as-is (timing in Part II instruction details)

**Decision:** POSTPONED - User needs to understand the proposal before deciding.

---

### 6. Chapter 2 FX Field Detail
**Draft Location:** Pages 29-30
**Status:** IN RESEARCH - Postponed pending user clarification

**Finding:** Draft explains FX field encoding variations in detail:
- CZI - Standard: C, Z write enable, I = immediate
- L bit - When DEST is literal (`#` prefix)
- R bit - When address is relative (no `\` prefix)
- A field - 20-bit address spanning DEST+SRC fields

Our Chapter 2 covers basic encoding but less clearly on these variations.

**Decision:** POSTPONED - User needs to understand the proposal before deciding.

---

### 7. Reserved Words Comparison
**Draft Location:** Pages 160-161
**Status:** APPROVED - WORD-BY-WORD COMPARISON REQUIRED

**Finding:** Draft has significantly more reserved words including:
- DEBUG output macros: UBIN, UDEC, UHEX and all variants
- Streamer modes: X_* constants (78 modes)
- Smart Pin modes: P_* constants (116 modes)
- Color constants: BLACK, WHITE, YELLOW, etc.

**Decision:** Perform word-by-word comparison to ensure:
- NO words missing from our list that are in draft
- NO extra words in our list that aren't valid
- Composite list approach (PASM2 + Spin2 combined)

**Special Requirements:**
- P_* Smart Pin constants: Verify table exists, call out separately
- X_* Streamer mode constants: Verify table exists, call out separately

---

### 8. Streamer Section Expansion
**Current Location:** Part I Chapter 5, Section 5.3
**Status:** APPROVED FOR SPRINT - MAJOR EXPANSION NEEDED

**Finding:** Current Streamer section is only ~40 lines - far too brief for the P2's DMA system. Covers:
- 5.3.1 Capabilities (overview only)
- 5.3.2 Instructions (just listed, no detail)
- 5.3.3 Modes (brief 4-row table)

Section ends with deferral: "Complete mode documentation... appears in the P2 hardware documentation"

**What's missing:**
- X_* mode constants (78 modes) - not documented at all
- Detailed FIFO interaction and buffer management
- Configuration bit fields explanation
- Practical programming examples
- Buffer chaining patterns
- Timing considerations
- NCO/RF/Goertzel mode details

**Decision:**
1. Expand Section 5.3 to comprehensive coverage matching CORDIC section depth
2. Create separate X_* Streamer mode constants appendix with descriptions

**Rationale:** Streamer is the P2's DMA system - critical hardware that deserves thorough documentation, not a placeholder.

---

### 9. X_* Streamer Mode Constants Appendix
**Draft Reference:** Pages 160-161 list 78 X_* constants
**Status:** APPROVED FOR SPRINT - NEW APPENDIX

**Finding:** The 78 X_* streamer mode constants need their own appendix with:
- Complete constant list
- Description of each mode
- Configuration bit patterns
- Typical use cases

**Decision:** Create new appendix (likely Appendix H or I) dedicated to Streamer modes.

---

### 10. FIFO YAML Knowledge Base Upgrade
**Punch List Location:** FIFO Knowledge Base Content item (marked as not for manual)
**Status:** ✅ COMPLETE (2025-12-04)

**Finding:** Minimal 44-line FIFO YAML existed but was sparse compared to Silicon Doc source.

**Completed Work:**
- ✅ Created comprehensive FIFO architecture YAML at `deliverables/ai/P2/architecture/core/fifo-architecture.yaml`
- ✅ Includes FBLOCK, RFVAR/RFVARS, D[31] modes, Hub restriction, WAITX cleanup

---

## Content Already Well Covered

| Item | Draft Location | Our Coverage | Status |
|------|----------------|--------------|--------|
| Categorical Listing | Pages 15-27 | Appendix B | Adequate |
| Conditions (IF_x) | Pages 15-16 | Chapter 3 + Appendix E | Complete |
| Effects (WC, WZ, etc.) | Page 16 | Chapter 3 | Complete |
| Individual Instructions | Pages 31-146 | Part II | Comprehensive |
| Flag Modification (MODx) | Page 17 | Part II instructions | Complete |
| Augmentation (SETQ, AUGS, AUGD) | Page 17 | Part II instructions | Complete |
| Indirection (ALTx) | Page 17 | Part II instructions | Complete |

---

## Front Matter / Appendix Alignment Issue

**Front Matter promises:**
- Appendix G: Glossary ← FILE MISSING (to be created)
- Appendix H: Index ← FILE MISSING (TBD)

**Current actual files:**
- appendix-a-encoding-table.md
- appendix-b-categorical-index.md
- appendix-c-special-registers.md
- appendix-d-constants.md
- appendix-e-reserved-words.md
- appendix-f-opcodes.md

---

## Sprint Task Summary

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1 | Reserved words word-by-word comparison | HIGH | TODO (30m) |
| 2 | Verify P_* Smart Pin constants table exists | HIGH | TODO (10m) |
| 3 | **Expand Streamer section 5.3** (FIFO, config, examples, buffer chaining) | HIGH | TODO (90m) |
| 4 | **Create X_* Streamer mode constants appendix** with descriptions | HIGH | TODO (45m) |
| 5 | Create Multi-Long Operations chapter (32/64/96/128-bit) | HIGH | TODO (60m) |
| 6 | Add Expression Operators to Chapter 2 | HIGH | TODO (30m) |
| 7 | Create Appendix G Glossary | HIGH | TODO (25m) |
| 8 | Add PR0-PR7 to Special Registers section | HIGH | ✅ DONE |
| 9 | Create PASM2 YAML files for PR0-PR7 | HIGH | ✅ DONE |
| 10 | Enhance Spin2 PR0-PR7 YAMLs | MEDIUM | ✅ DONE |
| 11 | FIFO YAML knowledge base upgrade | MEDIUM | ✅ DONE |
| 12 | RESEARCH: Appendix B timing enhancement | BACKLOG | - |
| 13 | RESEARCH: Chapter 2 FX field detail | BACKLOG | - |

**Completed pre-sprint:** Tasks 8, 9, 10, 11 (85 minutes)
**Remaining for sprint:** ~5 hours (Tasks 1-7, excluding research items)

---

## Key Source Files

| Content | Location |
|---------|----------|
| Draft Manual (text) | `engineering/ingestion/sources/pasm2-manual/pasm2-manual-narrative.txt` |
| 128-bit Math Examples | `engineering/ingestion/external-inputs/from-Chip/math-pasm.txt` |
| PR0-PR7 Spin2 YAMLs | `deliverables/ai/P2/language/spin2/registers/pr0-pr7.yaml` |
| Integration YAML | `deliverables/ai/P2/language/spin2/integration/spin2-pasm2-integration.yaml` |
| FIFO YAML (sparse) | `engineering/knowledge-base/P2-support/components/fifo.yaml` |

---

*Created: 2025-12-04*
*Status: Sprint planning complete, awaiting execution*
