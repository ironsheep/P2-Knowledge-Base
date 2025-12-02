# Narrative Improvements TODO

This document catalogues narrative improvements to add more detail in future revisions.

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

## XBYTE Bytecode Engine

**Location:** Part I Chapter 5, Section 5.7 (Hardware)

**Current state:** Brief overview of XBYTE functionality exists, but lacks depth on practical usage and configuration.

**Needed:** Locate XBYTE source ingestion materials and embellish the XBYTE description to be more meaningful:
- XBYTE instruction table format and layout
- Bytecode dispatch mechanism details
- Practical examples of bytecode interpreter implementation
- Performance characteristics and timing
- Comparison with traditional instruction dispatch approaches

---

*Created: 2025-12-02*
*Last updated: 2025-12-02*
