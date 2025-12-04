# Narrative Improvements TODO

This document catalogues narrative improvements to add more detail in future revisions.

---

## Instruction Entry Header Format Audit

**Location:** All Part II instruction, directive, and constant entries

**Current state:** Most entries appear to follow the correct format, but consistency has not been verified across all ~300 entries. Category links were defined, and entries were partially updated to use them, but the work was not completed.

**Required format for every entry:**
1. **Line 1:** `## MNEMONIC {#anchor}` - All-uppercase mnemonic as heading (title font)
2. **Line 2:** Mnemonic expansion - English words as memory hook (e.g., "Add Signed, Extended")
3. **Line 3:** `[Category](#link) - Single-line description`
4. **Line 4+:** Parameter form(s) - `**MNEMONIC** *params* **{flags}**`
5. **Separator:** `---` before Result section

**Defined categories (17 total):**
- Branch, CORDIC Solver, Color Space Converter, Event
- Hub Control, Hub FIFO, Hub RAM, Interrupt
- Lookup Table, Math and Logic, Miscellaneous, Pin
- Pixel Mixer, Register Indirection, Smart Pin, Streamer, System Control

**Needed:** Audit all entries to ensure:
- Every entry has all 4 required header components
- Mnemonic expansions are present and meaningful (not just repeating the mnemonic)
- Category links use ONLY the 17 defined categories above
- Category link anchors match exactly (e.g., `#streamer-category` not `#streamer`)
- Parameter forms match actual instruction syntax
- Capitalization is consistent (Title Case for mnemonic expansion)

**Status:** Category link targets are defined in `instruction-categories.md`. Instruction entries have been partially updated but some may still have incorrect/missing category links.

**Implementation:** Create a validation script to check all entries against the format spec and category list.

---

## Related Links Audit

**Location:** All Part II instruction entries with **Related:** sections

**Current state:** Some related instruction links point to anchors that don't exist. This occurs when:
- Multiple related instructions share a single block (e.g., BITC/BITNC/BITZ/BITNZ)
- The related link targets a secondary instruction (e.g., `#bitnc`) but only the primary instruction has an anchor (e.g., `#bitc`)
- The link text shows the instruction name but the target anchor doesn't match

**Problem example:**
```markdown
**Related:** [BITNC](#bitnc), [BITZ](#bitz), [BITNZ](#bitnz)
```
But the actual block anchor is only `## BITC {#bitc}` - the other anchors don't exist.

**Needed:** Full audit of all Related links to ensure:
- Every `[MNEMONIC](#anchor)` link resolves to an existing anchor
- Links to multi-instruction blocks point to the block's single anchor

**Decision:** Each block has ONE anchor (the primary instruction). All related links to any instruction in that block point to that single anchor. Example:
- Block: `## BITC / BITNC / BITZ / BITNZ {#bitc}`
- Related links: `[BITNC](#bitc)`, `[BITZ](#bitc)`, `[BITNZ](#bitc)` - all point to `#bitc`

This is many-to-one mapping: multiple instruction names can link to one block anchor.

**Implementation:**
1. Identify all multi-instruction blocks and their primary anchors
2. Create mapping table: instruction name → block anchor
3. Audit all Related links and fix any that target non-existent anchors
4. Create validation script to prevent future broken links

---

## Colored Vertical Bars for Entry Types

**Location:** Part II instruction entries, directives, and constants

**Current state:** All reference entries (instructions, directives, constants) use identical visual styling. There's no quick visual indicator to distinguish entry types when scanning the document.

**Needed:** Add a colored vertical bar on the left edge of each entry block to visually differentiate the three entry types:
- **Instructions** - One color (e.g., blue/teal)
- **Directives** - Different color (e.g., green)
- **Constants** - Third color (e.g., gold/amber)

**Implementation approach:**
1. Update `p2kb-pasm2-content.sty` to define three entry environments with left border colors
2. Update Lua filter or markdown to wrap entries in appropriate environment
3. Or use a simpler approach with `tcolorbox` left bar styling

**Benefit:** Readers can quickly identify entry type at a glance when flipping through Part II, improving navigation and lookup efficiency.

---

## Missing Diagrams (Part I)

**Location:** Part I chapters - currently marked with `<!-- DIAGRAM: ... -->` placeholder comments

**Current state:** Six diagrams are referenced but not implemented. These are HTML comments that get stripped during processing.

**Needed diagrams:**

### Chapter 1: The P2 Execution Model
1. **8-COG overview** (line 10) - Parallel processors with shared Hub memory
2. **COG memory map** (line 42) - $000-$1FF address regions showing general vs special registers
3. **Special register map** (line 54) - DIRA, DIRB, OUTA, OUTB, INA, INB layout at $1F0-$1FF
4. **Hub memory map** (line 86) - 512KB layout showing address space organization
5. **LUT memory layout** (line 113) - 512 longs per COG, relationship to COG RAM

### Chapter 4: Timing
6. **Egg beater timing** (line 145) - 8 COGs and hub access slot rotation pattern

**Implementation:** Create TikZ diagrams using the diagram macros in p2kb-pasm2-diagrams.sty, or create PNG/SVG assets in the assets folder.

---

## CORDIC Pipelining

**Location:** Part I Chapter 5 (Hardware) and CORDIC instruction entries (QDIV, QMUL, QFRAC, QROTATE, QVECTOR, QSQRT, QLOG, QEXP)

**Current state:** Basic CORDIC usage is documented, but pipelining techniques are not covered in depth.

**Needed:** Add a paragraph or section describing tight timing techniques for multiple CORDIC requests:
- Pipelining multiple operations (issuing new request every 8 clocks while previous results are still in flight)
- Interleaving different CORDIC operations
- Timing constraints for maximum throughput
- Example showing pipelined CORDIC operations with proper result retrieval timing

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

## FIFO Knowledge Base Content

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

## Processor Boot Sequence Section

**Location:** Part I (new chapter or section in Chapter 1)

**Current state:** No dedicated coverage of how the P2 boots itself.

**Needed:** Add a section summarizing the P2 boot sequence from power-on to user code execution:
- ROM execution phase
- Clock initialization (starts in RCFAST mode)
- Hub RAM clearing behavior
- Cog 0 startup sequence
- Handoff to user code
- Why ASMCLK exists and when it's needed

**Source:** Silicon documentation ingestion source (p2-documentation.txt boot sequence sections)

**Benefit:** Understanding boot behavior is foundational for PASM2 programmers - explains chip state when user code starts, why clock setup is needed, and ROM/RAM initialization.

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
