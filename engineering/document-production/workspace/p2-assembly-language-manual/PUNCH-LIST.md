# Narrative Improvements TODO

This document catalogues narrative improvements to add more detail in future revisions.

---

## ~~Instruction Entry Header Format Audit~~ ✅ COMPLETED

**Status:** ✅ Completed 2025-12-04

All 314 PASM2 manual entries audited and updated with correct header format including color bar headers.

---

## ~~Related Links Audit~~ ✅ COMPLETED

**Status:** ✅ Completed 2025-12-04

Related links audited and fixed to use correct anchor targets for multi-instruction blocks.

---

## ~~Colored Vertical Bars for Entry Types~~ ✅ COMPLETED

**Status:** ✅ Completed 2025-12-04

Color bar headers implemented:
- **Instructions** - Red (`\colorbar{red}`)
- **Directives** - Amber (`\colorbar{amber}`)
- **Constants** - Violet (`\colorbar{violet}`)

All 314 entries updated with appropriate color bars.

---

## ~~Missing Diagrams (Part I)~~ ✅ COMPLETED

**Status:** ✅ Completed 2025-12-04

### Implemented Diagrams:
- ✅ 8-COG overview
- ✅ COG memory map ($000-$1FF)
- ✅ Special register map ($1F0-$1FF)
- ✅ Hub memory map (512KB)
- ✅ LUT memory layout

### Not Needed:
- ⊘ Egg beater timing - Text explanation in section 4.3.1 is sufficiently clear; diagram would be redundant

---

## ~~CORDIC Pipelining~~ ✅ COMPLETED

**Status:** ✅ Completed 2025-12-04

**Location:** Part I Chapter 5, Sections 5.1.3-5.1.6

**What was added:**
- ✅ 5.1.3 CORDIC Pipelining - Hub rotation access (8 clocks per COG), 6-7 ops in flight
- ✅ 5.1.4 The Pipeline Phases - Fill/steady-state/drain pattern with code examples
- ✅ 5.1.5 Result Retrieval Timing - GETQX/GETQY stalling, POLLQMT for non-blocking check, Event 15
- ✅ 5.1.6 Practical Pipelining Example - Complete rotate_points example with all three phases
- ✅ Performance comparison (3× speedup for pipelined vs sequential)
- ✅ Corrected previous misinformation about "queue depth of one"

---

## PASM Code Examples - Right Edge Comments

**Location:** All Part II instruction entries with `::: pasm2` code examples

**Current state:** Some code examples may have comments that run too long and could wrap or be truncated in the PDF.

**Needed:** Audit all PASM2 code examples for:
- Comments exceeding reasonable line length (~60 chars for comment portion)
- Reformat long comments to wrap to next line or abbreviate
- Ensure consistent comment alignment within each example

---

---

## DEBUG Instruction Chapter

**Location:** New chapter needed (Part I Chapter 6 or dedicated section)

**Current state:** DEBUG instruction removed from Part II instruction reference. It requires special treatment beyond a standard instruction entry because DEBUG is not a single instruction but a family of debugging directives with complex syntax.

**Needed:** Create a dedicated narrative chapter covering:

### Core DEBUG Functionality
- DEBUG instruction syntax overview
- DEBUG vs DEBUG() - statement vs expression forms
- Compile-time behavior (code generation for serial output)
- Runtime behavior (serial communication with host)

### Output Formatting
- Basic value display: `DEBUG(udec(x), uhex(y))`
- Signed vs unsigned: `sdec`, `udec`, `shex`, `uhex`
- Binary output: `ubin`, `sbin`
- String output and labels
- Formatting options: field width, padding, separators

### Visual Debugging Tools
- `DEBUG(`\`SCOPE)` - Oscilloscope display
- `DEBUG(`\`PLOT)` - XY plotting
- `DEBUG(`\`TERM)` - Terminal window
- `DEBUG(`\`BITMAP)` - Bitmap display
- Configuration parameters for each visual mode

### Practical Debugging Patterns
- Watching register values in loops
- Timing measurement with DEBUG
- Conditional debugging (debug only when condition met)
- Multi-COG debugging considerations
- Performance impact of DEBUG statements

### Development Environment Integration
- PropTool DEBUG window configuration
- FlexProp/FlexGUI integration
- Serial port requirements and baud rates
- Disabling DEBUG for production builds

---

## FIFO Knowledge Base Content ⊘ NOT FOR THIS MANUAL

**Status:** ⊘ YAML knowledge base upgrade - not part of this manual

**Location:** `engineering/knowledge-base/P2-support/components/fifo.yaml` and `deliverables/ai/P2/`

**Current state:** A minimal 44-line FIFO YAML exists in `P2-support/components/` but:
- May not be in the correct location (support folder vs main deliverables)
- Content is sparse compared to Silicon Doc source material
- Missing key technical details (FBLOCK, RFVAR/RFVARS, D[31] modes, depth formula)

**Needed:** Verify and correct FIFO knowledge base content:
- Determine correct location for FIFO YAML in deliverables structure
- Expand content to match Silicon Doc detail level (lines 6660-6850)
- Include FBLOCK instruction for dynamic buffer management
- Include RFVAR/RFVARS variable-length encoding tables
- Include D[31] wait/no-wait mode operation
- Include hub execution restriction (FIFO unavailable during hub exec)
- Include WAITX cleanup requirement before COGSTOP after WRFAST

**Source:** Silicon Doc v35 (p2-documentation.txt lines 6660-6850)

**Tracking:** This item belongs in knowledge base maintenance, not the P2 Assembly Language Manual punch list.

---

## ~~XBYTE Bytecode Engine~~ ✅ COMPLETED

**Location:** Part I Chapter 5, Section 5.7 (Hardware)

**Status:** ✅ Completed 2025-12-04

**What was added:**
- ✅ 8-clock execution cycle table with phase/activity/description
- ✅ LUT table format section (bits [9:0] address, bits [31:10] SKIPF pattern)
- ✅ Complete SETQ D pattern configuration table (all 9 modes)
- ✅ Compressed mode explanation (%ABBBB00xF)
- ✅ Flag control section (F bit → C/Z from bytecode index)
- ✅ SETQ2 for temporary mode switching
- ✅ Bytecode routine requirements (location, exit, stack constraints)
- ✅ Practical code examples (setup sequence, minimal routine)
- ✅ Performance comparison table (software vs XBYTE dispatch)
- ✅ Applications list (VMs, interpreters, command processors, etc.)

**Source:** Silicon Doc v35 (p2-documentation.txt lines 1964-2360)

---

---

## ~~Processor Boot Sequence Section~~ ✅ COMPLETED

**Status:** ✅ Completed 2025-12-04

**Location:** Part I Chapter 5, Section 5.8

**What was added:**
- ✅ Section 5.8 Boot Process with 7 subsections
- ✅ 5.8.1 Initial Chip State (clock, COGs, RAM, pins, counter, PRNG)
- ✅ 5.8.2 Boot Source Selection (resistor pull-up detection table)
- ✅ 5.8.3 Boot Pin Assignments (serial, SPI, SD card pinouts)
- ✅ 5.8.4 The Boot Sequence (step-by-step ROM booter flow)
- ✅ 5.8.5 Serial Loading Protocol (auto-baud, commands, validation)
- ✅ 5.8.6 Clock Configuration After Boot (code example, ASMCLK explanation)
- ✅ 5.8.7 Rebooting from Software (HUBSET reset)
- ✅ Updated Key Concepts box with boot-related items

**Source:** Silicon Doc v35 (p2-documentation.txt lines 9200-9500)

---

## Content Audit Against Parallax Documentation

**Location:** All Part I and Part II content

**Current state:** Content was generated from Silicon Doc and other sources, but has not been systematically audited against the Parallax-developed documentation to ensure completeness.

**Needed:** Final validation pass comparing our content against the Parallax ingestion source to identify:
- Any instructions, modes, or features we may have missed
- Edge cases or behaviors documented by Parallax but not in our manual
- Terminology differences that should be reconciled
- Any corrections or clarifications from official sources

**Source:** Parallax-developed content in ingestion sources

**Priority:** This should be one of the final tasks before release - a quality assurance check to ensure completeness.

---

## Reserved Words Appendix Audit

**Location:** Part III Appendix E

**Current state:** Appendix E exists with 449 words across 6 categories, but this may be incomplete compared to the full reserved word sets in the actual PASM2 and Spin2 compilers.

**Needed:** Audit Appendix E against the complete reserved words list in the Draft Parallax Manual to ensure:
- All PASM2 reserved words are included
- All Spin2 reserved words are included (or clearly noted as Spin2-only)
- No missing keywords, constants, or special identifiers
- Categories are complete and accurate

**Source:** Draft Parallax Manual (ingestion source) - contains authoritative reserved words list

**Priority:** Part of final content audit before release.

---

*Created: 2025-12-02*
*Last updated: 2025-12-04*

**Completion Summary:**
- ✅ Instruction Entry Header Format Audit (2025-12-04)
- ✅ Related Links Audit (2025-12-04)
- ✅ Colored Vertical Bars for Entry Types (2025-12-04)
- ✅ XBYTE Bytecode Engine (2025-12-04)
- ✅ Processor Boot Sequence Section (2025-12-04)
- ✅ CORDIC Pipelining (2025-12-04)
- ✅ Missing Diagrams - Part I (2025-12-04)
- ⊘ FIFO Knowledge Base Content - Not for this manual (YAML upgrade task)
