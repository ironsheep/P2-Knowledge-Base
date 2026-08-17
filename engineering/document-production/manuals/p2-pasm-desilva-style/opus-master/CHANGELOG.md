# DeSilva PASM2 Tutorial Manual - Changelog

## v3.0.6 (2026-08-16)

**An honest platform comparison, and the multi-cog hazard that costs a debugging session.**

### Added

- **"Two cogs touching the same pin"** (Chapter 16): DIR and OUT are OR'd across cogs, so two drivers produce a result resembling neither, unreported
- **`RQPIN`** named as the safe multi-cog pin read
- **The RP2350 (Pico 2)** joins Appendix A's platform table, with PIO compared: a state machine is a restricted resource, a cog a full processor
- **The software axis** (Appendix A): two languages to learn, a library situation not comparable to an ESP32's, a smaller ecosystem, a higher cost of entry
- **The P2 Architect's Guide** in Further Reading: this manual teaches how to write PASM2, that one what belongs in which cog

### Changed

- **Appendix A argues from growth**: the eighth job on one processor changes the timing of the seven already there; per-cog, it does not
- **The library discussion** states the cost plainly — you write more code yourself, and what changes is the *kind* of hours
- **Smart pins** end the scramble for a pin that supports your function; the pinmux conflict goes, the resource conflict stays, and Chapter 16 teaches it
- **The interrupt comparison** (Chapter 11): a dedicated timer and a careful scheme reach the same precision; the argument is what that scheme costs
- **Timing claims are the ones silicon supports**: a cog's timing does not shift because another cog got busy, and today's measurement holds next week
- **The parallel-processing pitch** (Preface) names what goes away — deciding which task gets the processor — and points at Appendix A for the cost
- **Acknowledgments** credit deSilva, Chip Gracey and the P2 community; the production note describes AI-assisted authorship in deSilva's style, every example compiled

## v3.0.5 (2026-08-11)

**Worked examples that run as written** — the smart-pin and serial examples assemble and behave as their text describes, and Chapter 1 tells you which pin your board's LED is on.

### Fixed
- Chapter 1 "Experiment 3: Fading": the LED fades, ramping over about 1.3 seconds
- Smart-pin examples drive their pins (`P_OE`), including PWM and the configuration-order example
- Async serial transmit and receive examples assemble as printed
- Quadrature example reads its B phase from the next pin up (`P_PLUS1_B`)

### Added
- **"Which Pin Is *Your* LED?"** (Chapter 1): LED pins differ by board — P56/P57 on the P2 Edge Module, **P38/P39** on the 32MB PSRAM Module
- **"Why Your LEDs Glow When You Touch Them"** (Chapter 1): the onboard LEDs are buffered, so a floating buffer input switches them on
- `P_OE` introduced in Chapter 1 where the first smart pin appears
- Smart Pin Quick Reference (Chapter 14): `P_OE` in the recipe, the Golden Rule, and marked on every output mode
- Chapter 1 states what the fading experiment looks like: a ramp to full, then a snap back to dark
- LED pin table covers the P2 Eval Board (#64000) too, and names the LED switch position (ON)


## v3.0.4 (2026-08-08)

A licensing change. No technical content changed.

- **Licensed CC BY-SA 4.0**: share and adapt this manual, including commercially, with attribution and under the same terms.


## v3.0.3 (2026-07-11)

**A technical-accuracy pass**: instruction semantics, timing, and the worked examples verified against the P2 silicon documentation and the current compiler.

### Changed
- PASM2 behavior and timing read as the silicon defines them, the CORDIC is one solver the cogs share through hub slots, `MUL` is a 16×16→32 multiply, and the RCFAST oscillator runs at a nominal ~24 MHz.

### Fixed
- The `TESTP` WZ result reflects the pin state as the silicon reports it, and the async-serial transmit recipe drives its output pin (`P_OE`): so these worked examples behave as the text describes.

## v3.0.2 (2026-07-07)

**A naming refinement and three event-encoding corrections**: an example titled for what it teaches, and event-table entries that match the silicon.

### Changed
- The dedicated-cog servo example is titled "Real-World Example: Dedicated-Cog Servo Control," and its lead-in describes the timing as rock-steady. Accurate framing for a focused teaching example; no code changed.

### Fixed
- Event-table encodings match the silicon: `SETSE` selector `%000` is the LUT read/write & hub-lock event, `EVENT_INT %0000` reads "an interrupt occurred," and `EVENT_QMT %1111` reads "read with no CORDIC result available."

## v3.0.1 (2026-06-25)

**Accuracy re-audit, typography refresh, and a companion example library**: every code example compile-checked against the current compiler, with a presentation pass on the shared manual platform.

### Changed
- Refreshed typography for a cleaner, more consistent look across the manual.
- A companion example library collects ready-to-run versions of the manual's early programs (first blink, multi-cog blink, hub counters).
- The smart-pin recipe (Ch 14) enables the pin (DIRH) before writing the Y parameter (WYPIN): the one ordering correct for every mode, and the ordering the trigger and serial modes require.
- Every PASM2 and Spin2 example compiles against the current compiler, using P2 instructions and current Spin2 syntax: in-range immediates, absolute (`#\`) long jumps, DAT-label string addresses (`##@label`), the `{Spin2_v43}` directive for the `BYTE()`/`LONG()`/`LSTRING()` composers, long-aligned DAT data, and labels clear of instruction and keyword names.

### Fixed
- Quantitative values match silicon: smart pins offer 32 modes, CORDIC results (including QDIV) arrive 55 clocks later, the cog uses a 5-stage pipeline, and random hub access takes 9–16 clocks.
- CORDIC sine/cosine results are full-scale-signed, with $7FFF_FFFF representing 1.0.
- The cog reads one shared 64-bit system counter via GETCT, with its own CT1/CT2/CT3 compare targets for timed events.
- The servo clamp uses FGE for the lower limit and FLE for the upper limit.
- Reading a pin works regardless of its direction.
- The cover's code-color legend reads: green = PASM2, blue = Spin2, teal = multi-cog, purple = CORDIC, red = antipattern.
- Cross-references resolve to the right chapters: the smart-pin pointer to Chapter 14, and the Chapter 12 preview to the LUT memory, smart pins, and event-driven topics of Chapters 13–15.

## v3.0.0 (2026-06-10)

**Content re-audit on the shared presentation platform**: every technical claim re-verified against the current P2 Knowledge Base, delivered on the common P2 manual presentation platform.

### Instruction Semantics

- MUL/MULS: 16×16→32 multiply; QMUL is unsigned
- MERGEB: bit-merge, the inverse of SPLITB
- QLOG/QEXP: base-2 logarithm and 2^x
- OUTH/OUTL: set the OUT bit only, leaving pin direction unchanged

### Timings and Values

- QDIV result latency is 55 clocks; CORDIC angle resolution and spiral rotation angles match the silicon
- Random hub-access timing is 9–16 clocks; the FIFO is 19 stages deep
- COG load size is 504 longs ($000–$1F7), with a 496-instruction code ceiling

### Code Examples

- LOCKTRY spin-locks retry on failure with the correct carry polarity
- QVECTOR examples pass Y as the S operand; a COGINIT-passed value is read from PTRA with MOV
- The SKIP example uses LSB-first bit order, and the servo-frame loop terminates
- SETSE edge/level modes, the EVENT_XRL description, the ADC sample period, and the PWM/streamer setup examples verified against the silicon

### Presentation

- Figures and tables are numbered with captions and collected in Lists of Figures and Tables; long tables and code blocks carry continuation markers across page breaks

---

## v2.2.0 (2026-05-23)

**Periodic release**: Hub-exec timing accuracy, expanded pedagogical structure across Chapters 4-6 and 13-15, and consistent Your Turn block rendering throughout.

### New Content

- Chapter 4 (Hub Connection): Your Turn experiments, Common Gotchas, What We've Learned, Coming Up Next, Have Fun! closer
- Chapter 5 (Mathematics): Medicine Cabinet quick-reference plus the four closing sections
- Chapter 6 (Flags and Decisions): Medicine Cabinet plus the four closing sections
- Chapters 13-15 (LUT Memory, Smart Pins Orientation, Event-Driven Programming): closing trio added (What We've Learned, Coming Up Next, Have Fun!)
- Chapter 3: ALTx hub-exec compatibility sidetrack confirming all 11 ALTx instructions work identically in cog-exec and hub-exec
- Chapter 12: GETCT overflow Pitfall callout covering the ~21.5-second 32-bit CT wrap at 200 MHz, with 64-bit-capture and work-with-deltas strategies

### Enhanced Accuracy

- Chapter 10 (Hub Execution): sequential hub-exec code runs at 2 clocks/instruction; only branches pay the 13+ clock refill cost
- Chapter 12 (Optimization): RDLONG, WRLONG, DJNZ timing tables show both cog-exec and hub-exec ranges
- Chapter 12: REP-in-hub-exec note explains the 13+ clock per-iteration cost from the hidden return-jump
- Chapter 7 (CORDIC) sprite rotation example uses PTRA post-increment idiom
- Chapter 13 (LUT Memory) SETQ2 example uses correct destination operand syntax
- Chapter 12 (Optimization) REP and loop unrolling examples use canonical hub-access patterns
- Chapter 12: WRLUT 32-bit constant uses `##` augmented immediate
- Code-block comments use native PASM2/Spin2 syntax throughout

### Throughout

- Your Turn exercise boxes render with consistent styling across all chapters
- Tutorial voice tightened in Chapters 7-16 to match the conversational register established in Chapters 1-6

---

## v2.1.0 (2026-01-30)

**Code Example Accuracy** - Relative jump offsets corrected for augmented instructions.

### Chapter 1 - Your First Spin

- LED blinker example: JMP offset corrected to account for hidden AUGS instructions generated by `##` immediates

---

## v2.0.0 (2026-01-23)

**Code-Verified Release** - All code examples verified against YAML Knowledge Base instruction definitions. Address space documentation hardened through systematic claim verification.

### Part II: Core Skills (Chapters 5-8)

#### Chapter 5 - Mathematics
- CORDIC timing: All code comments verified at 55 clocks (hardware-exact)

### Part III: Advanced Topics (Chapters 9-12)

#### Chapter 9 - Streaming
- FIFO examples: Audio processing and filter pipeline examples demonstrate correct single-direction pattern (FIFO for read, PTRA for write)

#### Chapter 10 - Hub Execution
- Address thresholds: Hub execution boundary documented as ≥$400
- Memory map: Complete address space summary ($000-$1FF COG, $200-$3FF LUT, ≥$400 Hub)

#### Chapter 12 - Optimization
- CORDIC overlap examples: Timing comments verified at 55 clocks throughout

### Part IV: System Integration (Chapters 13-16)

#### Chapter 11 - The Propeller Way
- COGINIT: Reaction timer example uses correct SETQ + 2-operand pattern

#### Chapter 16 - Multi-COG
- COGINIT: Medicine Cabinet example uses correct SETQ + 2-operand pattern

### Verification Notes

**Verification Sources:**
- YAML Knowledge Base: `deliverables/ai/P2/language/pasm2/*.yaml`
- QROTATE, QMUL, MUL, SETQ, COGINIT, REP instruction definitions
- Silicon Documentation v35

**Methodology:**
- Systematic claim extraction from document text
- Cross-reference against YAML instruction definitions
- Red-flag phrase scanning ("automatically", "eliminates") for hallucination detection

---

## v1.1.0 (2025-12-12)

**Audit-Verified Release** - Comprehensive audit with user feedback review (14 items) and mnemonic validation against PNut_TS compiler database and YAML Knowledge Base.

### Part I: Foundations (Chapters 1-4)

#### Chapter 1 - First Blink
- Clock configuration: Clarified P2 boots at ~20MHz RC, examples assume 200MHz

#### Chapter 2 - Understanding COGs
- Register classification: Documented dual-purpose (496-503) vs special-purpose (504-511) registers
- COG launch: Clarified COGEXEC_NEW behavior with 8-COG system

#### Chapter 3 - Instructions
- Relative jumps: Clarified `$-4` addresses longs (not instruction count)
- REP instruction: Corrected byte count in block copy example (256 longs = 1024 bytes)
- **NEW**: `_RET_` prefix documentation - conditional return prefix for any instruction
- **NEW**: `FILE` directive - importing external binary data files into DAT blocks
- **NEW**: String and data generation methods - `@"text"`, `STRING()`, `LSTRING()`

#### Chapter 4 - Memory
- Hub access timing: Documented 2-9 clock range for random access
- Screen buffer example: Updated to 320x240 resolution (fits 512KB hub)

### Part II: Core Skills (Chapters 5-8)

#### Chapter 5 - Mathematics
- MUL instruction: Documented as 16x16→32 unsigned multiply
- 64-bit multiplication: Documented QMUL+GETQX/GETQY CORDIC pattern
- Fixed-point math: Updated example to use CORDIC for full precision

#### Chapter 7 - CORDIC
- QROTATE syntax: Verified D=X coordinate, S=angle parameter order throughout
- Angle constants: Corrected $0100_0000 = ~1.4° (1/256 rotation)

### Part III: Advanced Topics (Chapters 9-12)

#### Chapter 9 - Streaming
- FIFO throughput: Documented up to 1 long per clock sustained rate
- FIFO pipeline: Clarified single-direction operation (read OR write, not both)

#### Chapter 10 - Hub Execution
- Timing characteristics: Clarified branch vs linear code performance

#### Chapter 11 - The Propeller Way
- Pin waiting: Updated to P2 TESTP+loop and SETSE/WAITSE patterns
- Low-power waiting: Documented WAITSE/WAITCT for COG sleep

#### Chapter 12 - Optimization
- Hub access timing: Corrected RDLONG (9-16 clocks) and WRLONG (3-10 clocks)
- DJNZ timing: Documented branch penalty (2 or 4 clocks)
- PTR expressions: Corrected addressing mode examples

### Part IV: System Integration (Chapters 13-16)

#### Chapter 13 - LUT Memory
- LUT sharing mechanism: Documented SETLUTS write-copying from neighbor COG
- Memory comparison table: Corrected hub RAM timing to 2-9 clocks

#### Chapter 15 - Events
- Interrupt setup: Documented SETSE+EVENT_SE pattern for pin-triggered interrupts
- SETINT syntax: Verified single-operand form with EVENT_* constants
- **NEW**: Complete EVENT_* constants reference table (16 event sources with values and descriptions)

#### Chapter 16 - Multi-COG
- COGINIT syntax: Documented 2-parameter form with SETQ for PTRA

### Presentation

- Code block colors aligned with IDE conventions (Propeller Tool, Spin Tools IDE):
  - PASM2 blocks: Green color family
  - Spin2 blocks: Blue color family
  - Multi-COG blocks: Teal color family (distinct from Spin2)

- Pedagogical environment colors with semantic associations:
  - Medicine Cabinet: Tan/beige theme (band-aid association for "remedy/help")
  - Your Turn: Amber theme (attention, action)
  - Sidetrack: Rose-red theme (distinct warm color)
  - Interlude: Orange theme (warmth, storytelling)

- Antipattern code blocks: Clear red theme (`#FFEBEE` / `#E53935`) for unmistakable "warning/wrong" semantic

- Antipattern div structure fixed (Chapters 13, 15): WRONG code renders in red, RIGHT code renders in green PASM2 blocks

- Base font size changed from 12pt to 11pt (matches P2 Assembly Language Manual)

- PDF navigation: Table of Contents entries fully clickable (both title and page number navigate to chapter)

- Page break improvements:
  - Medicine Cabinet and Interlude boxes request 40% page height before starting
  - Section/subsection headings stay with following content (no orphaned headings)

- Markdown formatting fixes:
  - 52 lists now have required blank line after lead-in text
  - 2 LaTeX diagram commands (WRPIN, SETSE bit fields) properly wrapped for Pandoc
  - Code block line length standardized to 75 characters max

### Verification Notes

**Sections Verified Correct:**
- All P_* Smart Pin mode constants
- SETSE mode bit patterns
- OUTA/DIRA register usage
- Bulk LUT load SETQ2 pattern

**Sources Used for Verification:**
- PNut_TS Instruction Database
- P2KB YAML Knowledge Base
- P2 Instructions v35 - Rev B_C Silicon CSV
- Silicon Documentation v35
- Spin2 Language Manual v51a

---

## v1.0.0 (2025-12-11)

Initial community review release.

- 16 chapters covering P2 PASM2 fundamentals
- DeSilva pedagogical style environments (Medicine Cabinet, Your Turn, Sidetrack, etc.)
- 5-color code block system for different code types
- Comprehensive index and cross-references
