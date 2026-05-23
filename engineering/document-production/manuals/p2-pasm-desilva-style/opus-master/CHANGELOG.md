# DeSilva PASM2 Tutorial Manual - Changelog

## v2.3.0 (2026-05-23)

**Voice Refresh Release** — Closes the F.2.a audit finding from v2.2.0 (Ch 7-16 voice drift) and a pair of cross-chapter structural inconsistencies surfaced while doing the voice work.

### Voice Refresh, Chapters 7-16 (HIGH)

The v2.2.0 audit's F.2.a finding noted that Ch 7-16 read more like a technical reference than the conversational DeSilva voice established in Ch 1-6. Re-measuring voice-marker density on the canonical master (rather than the cross-file comparison the original audit used) confirmed the gap was localized to *conversational micro-markers between section headers* — structural sections (Your Turn, What We've Learned, etc.) were comparable or higher in Ch 7-16, but prose connective tissue ("let's", "we'll", "Uff!", "Don't worry") was 73–100% lower.

Per-chapter surgical voice touches added (no content rewriting):

- **Ch 7 (CORDIC Magic)** — Removed a redundant restated-hook paragraph leftover from the v2.2.0 hook-strengthening pass, added three light voice touches.
- **Ch 8 (Basic I/O)** — Five voice touches: TRIS-bits aside in the pin-direction explanation, "we'll meet a few specialized cousins" follow-up to the fundamental four, "yes, you'll usually reach for Smart Pins" framing for the bit-bang section, a determinism celebration, and a "Before you pull your hair out" lead-in for Common I/O Gotchas.
- **Ch 9 (Streaming Data)** — Four voice touches: an off-by-one aside on the SETQ count semantics, a connective opener for the previously code-only "Writing Through the FIFO" section, a "Before you pull your hair out" lead-in for Common Streaming Gotchas, and an "Uff!" celebration on the performance-numbers conclusion.
- **Ch 10 (Hub Execution)** — Four voice touches: "Let's peek behind the curtain" opener for How Hub Execution Works, a callback-to-Ch-9 framing for the Hub Execution FIFO section with a "moving sidewalk" metaphor, a clearer follow-up on what the FIFO read-ahead actually buys, and a voice lead-in for Common Hub Execution Gotchas.
- **Ch 11 (Why No Interrupts?)** — Reviewed; no edits needed. The story-based opener, "Try that with interrupts. I'll wait. Actually, I won't," "Uff! Even writing interrupt code feels wrong on a Propeller!", and the 15-years-never-needed-interrupts personal note already establish this chapter as the voice-density high-water mark.
- **Ch 12 (Optimization Mastery)** — Two light touches: "Before we hunt for clocks to save" lead-in for Understanding the Pipeline, "Before you rewrite everything in REP and SKIP" lead-in for Common Optimization Gotchas.
- **Ch 13 (LUT Memory)** — Light touch (taste chapter): "Enough theory — let's see what people actually use the LUT for" opener for Practical Examples.
- **Ch 14 (Smart Pins Orientation)** — Light touch (taste chapter): "Don't worry, you don't have to memorize all 32 mode bit-patterns" reassurance for Configuration Values Demystified.
- **Ch 15 (Event-Driven Programming)** — Light touch (taste chapter): "Let's meet the cast" opener for The Four Selectable Events, "Time to put events to work" opener for Practical Examples.
- **Ch 16 (Multi-COG Orchestration)** — Four voice touches: framing for the three Communication Patterns ("Eight processors running in parallel sounds wonderful — until you realize they need to talk to each other"), a communication-vs-synchronization connector for Synchronization Techniques with "16 hardware locks. They're tiny and they're fast" framing for Using Locks, a "Before you pull your hair out wondering why the eight-COG dream turned into a debugging nightmare" lead-in for Common Multi-COG Gotchas, and a "The hardware gives you eight processors. Whether your design survives the journey is up to you" lead-in for Design Principles.

Post-refresh voice-marker density (Ch 7-16, per 1000 lines):

| Marker          | Before  | After   | Ch 1-6 baseline |
|-----------------|---------|---------|------------------|
| "Uff!"          | 0.26    | 1.01    | 0.98 ✓ matched   |
| "Let's"         | 1.83    | 3.03    | 5.90             |
| "we'll"         | 0.00    | 0.50    | 3.93             |
| "Don't worry"   | 0.00    | 0.50    | 0.98             |

### Document-Wide Structural Consistency (HIGH)

**Your Turn fence-syntax normalization** — Ch 1-12 used `:::yourturn` (no hyphen, 9 occurrences) while Ch 13-16 used `::: your-turn` (hyphenated, 7 occurrences). The active Lua filter (`p2kb-desilva-semantic.lua`, per the production `workspace/p2-pasm-desilva-style/request.json`) only maps `your-turn` → `dsyourturn` LaTeX environment — the 9 Ch 1-12 blocks were falling through as unstyled `<div class="yourturn">`. All 16 Your Turn blocks now use the canonical hyphenated form and render through the tcolorbox styling.

**Chapter close-out trio added to Ch 13, 14, 15** — These three taste/appetizer chapters were missing the standard `## What We've Learned` / `## Coming Up Next` / `**Have Fun!**` sign-off pattern present in Ch 1-12 and Ch 16. Added brief, taste-chapter-appropriate versions of all three sections to each. Counts now uniform: 16 chapters / 16 WWL / 15 CUN (Ch 16 has "Your Journey Continues" instead, intentional) / 17 Have Fun! (1 per chapter + Epilogue).

**Broken relative-file links removed** — Six `*Continue to [Chapter N: Title](NN-slug.md) →*` links in Ch 1-6 pointed to chapter files that no longer exist (legacy artifacts from the pre-consolidation era when each chapter lived in its own `.md` file). Removed — the `# Chapter N: Title` heading provides navigation, and Ch 7-12 never had these links anyway.

### Method Note

Re-measurement on the canonical master before editing confirmed the audit's qualitative finding while also showing that the original cross-file metric overstated the gap (it compared Ch 1-6 in one file vs Ch 7-16 in an archived legacy file with regressions). The actual gap was real but more localized than the original metric suggested, which is why the refresh leans on light targeted touches rather than wholesale rewrites.

---

## v2.2.0 (2026-05-23)

**Periodic Audit Release** — Style-guide conformance, hub-exec timing corrections, structural completeness for Chapters 4-6, and code-example validation infrastructure.

### Style-Guide Conformance (CRITICAL)

Fixed 8 prose-mnemonic formatting violations against the manual's own "ABSOLUTE RULE" (per `desilva-style-guide.md`) that all PASM2 mnemonics appear UPPERCASE BOLD in prose. Replaced backtick-lowercase forms (`` `mov` instruction ``) and bare-uppercase forms ("The MOV family") with proper **MOV** / **COGINIT** / **DRVNOT** / **DRVC** / **SETQ** formatting across both master files.

### Hub-Exec Timing Corrections (HIGH)

Brought the manual in line with April 2026 YAML corrections (commits `fbbd9ee`, `96cf4e8`) for the hub-exec timing model:

- **Chapter 10 — Hub Execution speed claim**: Replaced "2-9 clocks per instruction (typically 3-4)" misframing with the corrected model: sequential code is 2 clocks/instruction (same as cog-exec via the 19-stage FIFO prefetch); only branches pay the 13+ clock refill cost. Applied to both `COMPLETE-OPUS-MASTER.md` and `CHAPTERS-7-16-ENHANCED.md`.
- **Chapter 12 — RDLONG/WRLONG comments**: Updated to show both `cog-exec` and `hub-exec` ranges (`9-16 / 9-26` for RDLONG, `3-10 / 3-20` for WRLONG, `2/4 / 2/13-20` for DJNZ).
- **Chapter 12 — REP-in-hub-exec caveat**: Added a Hub-Exec Note after "REP: The Speed Loop" warning that REP loops in hub-exec pay 13+ clocks per iteration for the hidden return-jump.

### Pedagogical Structure Restoration (HIGH)

Added the missing DeSilva-pattern closing sections to Chapters 4, 5, and 6 (each previously stub-ended at the worked-example):

- **Chapter 4 — The Hub Connection**: Added "Your Turn: Experiments", "Common Gotchas", "What We've Learned", "Coming Up Next", "Have Fun!" closer.
- **Chapter 5 — Mathematics Unleashed**: Added "Medicine Cabinet" with quick math reference, plus all four required closing sections.
- **Chapter 6 — Flags and Decisions**: Added "Medicine Cabinet" with conditional execution quick reference, plus all four required closing sections.

### Voice Strengthening (HIGH)

Strengthened the two weakest Hook sections identified by the voice-conformance audit:

- **Chapter 7 (CORDIC Magic)**: Hook now adds personal framing ("Let me show you something that, on most processors, would take a coffee break of instructions…").
- **Chapter 12 (Optimization Mastery)**: Hook now opens with "Let me show you a loop that looks fine — until you realize you're paying for the same thing twice."

### Code-Example Bug Fixes (HIGH)

Found and fixed by code-validation pass with `pnut_ts` v1.51.7:

- **Chapter 7 (CORDIC Magic) sprite rotation example**: Replaced invalid `vertex_ptr++` general-register post-increment (only **PTRA**/**PTRB** support `++`) with the idiomatic **PTRA**-based pattern plus explicit `sub ptra, #8` before the writeback.
- **Chapter 13 (LUT Memory) SETQ2 example**: Corrected `rdlong $200, hub_table_ptr` (which exceeds the 9-bit destination field) to `rdlong $000, hub_table_ptr` with an explanation that the destination operand is the LUT offset, not the absolute address $200.

### Code-Example Validation Infrastructure (MEDIUM)

- Imported the improved `extract-and-validate.py` validator from the PASM2-manual sibling (uses `:error:` token detection instead of exit-code scanning — pnut_ts always exits 0 even on errors).
- Extended the extractor to handle both ` ```pasm2 ` standard fences AND `::: pasm2`/`:::` Pandoc fenced-div wrappers (used heavily in this manual).
- Extended the backup-file skip pattern to also match `-backup-` infix (catches `COMPLETE-OPUS-MASTER-backup-2025-12-06-pre-backport.md`).

Result: 333 code blocks extracted, 266 pass (80%). The 67 remaining failures are dominated by pedagogical templates (placeholder mnemonics like `INSTR D, S`), Spin2 expressions needing PUB context, and 24 fragments in `CHAPTERS-7-16-ENHANCED.md` that contain regressions (see Dual-Master Analysis below).

### Single-Source-of-Truth Consolidation (MEDIUM)

Resolved the E.x.a dual-master drift finding after confirming via the production workspace that `COMPLETE-OPUS-MASTER.md` is the only file the PDF pipeline reads. Five orphaned legacy files moved to `opus-master/archived-2025/`:

- `CHAPTERS-7-16-ENHANCED.md` (January 2025 staging file; content was merged into the canonical master but the standalone copy never received subsequent audit fixes — carried known regressions)
- `README-CHAPTERS-7-16-ENHANCED.md` (companion README)
- `COMBINED-COMPLETE-MASTER.md` (219-line never-completed stub)
- `README-COMBINED-MASTER.md` (companion README)
- `LABELS-SECTION-FOR-INSERT.md` (December 2025 staging snippet; content already integrated)

Renamed `opus-master/README-SACRED.md` → `opus-master/README.md` for standard discoverability. Added `archived-2025/README.md` explaining each archived file's history.

Validator updated to skip `archived-*` / `archive` / `legacy` / `deprecated` directories.

### Additional Code-Example Fixes (HIGH)

Two more bugs surfaced after the post-archive validation pass:

- **Chapter 12 — REP optimization example** (~line 4434): `add sum, ptra++` is invalid PASM2 — ADD does not accept hub-address expressions (only **RDxxxx** / **WRxxxx** / a few other hub-access instructions do). Rewrote to use the canonical 2-instruction pattern: `rdlong val, ptra++` then `add sum, val`.
- **Chapter 12 — Loop unrolling example** (~line 4508): Same `add sum, ptra++` bug. Same fix applied to both the looped and unrolled halves.

Result: validation pass rate **184/222 = 83%** on canonical master, with all remaining failures classifiable as pedagogical templates, placeholder syntax, or wrapper artifacts.

### Audit Artifacts

- New: `AUDIT-PROCESS.md` at the manual folder root — reusable periodic-audit process document, copied from sibling manual.
- New: `audit/periodic-audit-2026-05-22.md` — full periodic-audit findings report.
- New: `audit/dual-master-analysis-2026-05-23.md` — drift evidence and archival recommendation.
- New: `audit/dual-master-resolution-2026-05-23.md` — production-pipeline evidence confirming `COMPLETE-OPUS-MASTER.md` is canonical, with concrete archive plan.
- New: `code-validation/extract-and-validate.py` + `code-validation/.gitignore` — pnut_ts validation infrastructure with `::: pasm2` Pandoc-div support and archived-directory skip.
- New: `opus-master/archived-2025/` — historical legacy files preserved out of the production path.

### Tier 4 — Advisory Notes (LOW)

- **Chapter 3 — ALTx hub-exec compatibility note**: Added a sidetrack box at the end of the ALTD/ALTS section confirming that all 11 ALTx instructions (ALTI, ALTS, ALTD, ALTR, ALTB, ALTSN, ALTSB, ALTSW, ALTGN, ALTGB, ALTGW) work identically in cog-exec and hub-exec modes, so ALTx techniques learned here remain valid when readers reach Chapter 10.
- **Chapter 12 — GETCT overflow Pitfall callout**: Added a ⚠️ Pitfall box after the "Profiling and Measurement" example explaining the ~21.5-second 32-bit CT wrap at 200 MHz, with the two correct strategies — 64-bit capture via `GETCT D WC` for upper word, or work-with-deltas using two's-complement subtraction.

### Prior-Audit Minor Items Closed

Verified and applied the three remaining minor items from the prior audit cycle that `FIX-TRACKING.md` marked `[x]` but had not been independently re-verified:

- **UF-011 (WRLUT 32-bit constant)**: Found a real un-fixed bug at line 4614 — `wrlut #$12345678, #100` uses single `#` for a 32-bit value, which doesn't fit the 9-bit immediate field. Corrected to `wrlut ##$12345678, #100` (augmented 32-bit immediate). The `[x]` tracker mark was inaccurate.
- **UF-012 (SETQ2 bulk LUT load syntax)**: Already resolved earlier in this audit by the Tier 3 SETQ2 example fix (changed `rdlong $200, ...` → `rdlong $000, ...` with an explanatory paragraph about the destination operand being the LUT offset, not the absolute address).
- **Comment-style standardization**: Found three `//` C-style comments in the `::: antipattern` interrupt-demonstration block at line 3848-3852. Per project policy (now codified in `AUDIT-PROCESS.md` Dimension #14), PASM2/Spin2 manuals must use only native PASM2/Spin2 comment syntax even inside pseudocode and antipattern blocks. Converted all three `//` markers to `'` line comments.

### Audit Process Document Enhancement

Added **Dimension #14: Non-native comment-style leakage** to `AUDIT-PROCESS.md` (this manual *and* the sibling p2-assembly-language-manual copy). This dimension catches `//`, `/* */`, `;`, and `#`-as-comment markers in any code block — including pseudocode and antipattern blocks. PASM2 manual swept clean (its only `//` hits are legitimate Spin2 modulo-operator documentation, not comments).

The dimension's rationale: a reader sees `// foo` and `' foo` interchangeably and learns that either is "comment-shaped"; when they later write real PASM2 code with `// my note`, they get a syntax error they can't explain. Mixed comment styles in a single-language manual are an anti-pattern.

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
