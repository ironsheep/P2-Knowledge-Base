# P2 Assembly Language Reference Manual - Changelog

## v3.1.5 (2026-08-08)

A licensing change. No technical content changed.

- **Licensed CC BY-SA 4.0**: share and adapt this manual, including commercially, with attribution and under the same terms.


## v3.1.4 (2026-07-14)

**Hyphenated names print exactly as written**: compound terms and cross-references keep their authored spelling.

### Fixed
- Hyphenated compound terms read as written: `not-taken` branch timing, `1..4-byte` FIFO values.
- The cross-reference to the **P2 I/O & Smart Pins User Guide** carries that guide's exact name, so it resolves.

## v3.1.3 (2026-07-11)

**A silicon- and hardware-grounded accuracy pass**: instruction semantics, flag effects, and timing across the reference verified against the P2 documentation and real-hardware measurement.

### Changed
- Instruction behavior and flag effects read as the silicon defines them, including the AUGS/AUGD augment surviving intervening instructions before its `#` immediate, and the TEST, interrupt-priority, COGINIT, and QEXP semantics.
- Timing reflects measured behavior: bracketing code with two GETCT reads carries a fixed 2-clock overhead, hardware-confirmed on real P2 silicon.

## v3.1.2 (2026-07-04)

**Event-wait timeout documentation**: the event-waiting instructions document how a preceding SETQ arms a hardware timeout, hardware-verified on P2 silicon.

### Changed
- The event-wait instructions (WAITSE1–WAITSE4, WAITCT1–WAITCT3, WAITPAT, WAITATN, and the WAITxxx event family) document the SETQ-armed timeout: a System-Counter target loaded into SETQ immediately before the wait bounds it, so a single instruction stalls on its event or the deadline, whichever comes first, with C/Z reporting which. With no preceding SETQ the wait carries no timeout, and its WC/WZ/WCZ form clears both flags as a one-instruction flag-clear.
- The affected `Operation:` lines carry the timeout condition (`C/Z = timeout`, with the prior SETQ supplying the System-Counter deadline).

## v3.1.1 (2026-06-29)

**Execution-model and instruction-reference refinements**: a clearer cog/LUT/hub model and the streamer's role in Chapter 1, better guidance on reading an instruction entry, and an uppercase style for mnemonics in prose.

### Added
- §1.4.4 "Moving Hub Data: the Cog and the Streamer", cog-driven hub access (RDLONG/WRLONG, with SETQ for fast bursts) alongside each cog's own streamer, a close cousin of a DMA channel that moves data on its own at a set rate. A REP block of transfers is interrupt-atomic.
- REP reference (Part II): a REP block is interrupt-atomic, uninterruptible for its duration, including debug interrupts, the blocking counterpart to the streamer's autonomous transfer.
- §2.8.3 (reading an entry): explains the conditional `Operation:` line, exact pseudocode carried when an instruction's behavior is not obvious from its description, illustrated with ADDX.
- CMP carries an `Operation:` line (`C = borrow of (D - S); Z = (D == S)`), matching its CMPS / CMPX / CMPSX / CMPR / CMPM compare-family siblings.

### Changed
- §1.6 Execution Modes presents cog and LUT execution as one contiguous 1024-long fast space, identical two-clock timing, the program counter rolling from cog RAM into LUT RAM ($1FF to $200) at no cost, in a single "Cog and LUT Execution" section, with hub execution as the performance boundary where instructions stream through the FIFO and a branch to hub costs at least 13 clocks. REP repeats a cog/LUT block with no per-iteration branch.
- Instruction mnemonics in prose are set in uppercase, marking them as code tokens.

## v3.1.0 (2026-06-25)

**Instruction-reference accuracy and presentation pass**: a content re-audit against the Knowledge Base alongside a voicing, layout, and typography refresh.

### Changed
- Refreshed typography for a cleaner, more consistent look across the manual.
- Each instruction entry reads as a single unit, its syntax flowing directly into Operation and Result.
- 206 instruction entries carry a concise `Operation:` line summarizing the instruction's effect.
- Faster-instruction and related-instruction cross-references (e.g. SCA/SCAS, FLE/FGE) make lower-cycle alternatives discoverable from each entry.
- Smart-pin setup (WRPIN): the sequence enables the pin (DIRH) before writing the Y parameter (WYPIN), the ordering correct for every mode and required by the trigger and serial modes.
- Appendix F: configuration-word field labels follow the Silicon Doc, `M` for bits 20–8, `S` for the 5-bit operating-mode selector.

### Fixed
- Signed add/subtract flag semantics: ADDS, ADDSX, SUBS, SUBSX, and the SUM family document C as carrying the correct sign of the result.
- GETBRK: WC/WZ/WCZ return cog status, skip-and-execution state, and the queued 32-bit skip pattern respectively; a flag effect is required.
- Program Counter: reading the return address uses the supported CALLD idiom.
- Random number generator documented as a hardware pseudo-random generator (Xoroshiro128\*\*), true-random seeded at startup.
- PTRx updating-index range is -16 to +16; RDFAST maximum block size, CRCBIT bit order, the SCAS and RDLONG flag-effect cells, and the ANDZ bit-test example are all documented accurately.
- Operation-line notation uses ASCII throughout for reliable rendering.

## v3.0.0 (2026-06-10)

**Full content re-audit on the shared presentation platform**: every checkable claim re-verified against the current P2 Knowledge Base, with figures, tables, and code rendered on the common manual platform.

### Part I: Architectural Foundation

- Timing, flag effects, and addressing across Chapters 2–6 verified against the Knowledge Base
- §4.2.3: the Clocks-column notation covers the cog / hub-exec split and the taken-branch refill cost
- §4.6.1: the hub-aligned loop example documents its steady-state period of 24 cycles (3× the 8-cycle hub window)

### Part II: Instruction Reference

- Encodings, semantics, flag effects, and timing ranges verified against the Knowledge Base across every instruction chapter
- Hub-access and branch instructions carry both cog and hub-exec timing ranges

### Part III: Appendices

- Appendix G: X_DACS streamer constants document per-channel DAC routing
- Appendix H: reserved-word listings and category counts are internally consistent
- Encoding and reference tables size columns to content and repeat their headers across page breaks; long code blocks carry continuation markers
- Figures and tables are numbered with captions, with Lists of Figures and Tables

### Throughout

- Code examples fit within the code box
- Licensed under CC BY-NC-ND 4.0

---

## v2.3.0 (2026-05-22)

**Periodic release**: Hub-exec timing accuracy across timing tables and prose, ALTx cross-mode compatibility documented, inline-PASM-with-multitasking gap closed, and seven code-example fixes.

### Critical Fix

- END (Inline PASM) section: multitasking taskptr table ($100..$11F) overlap with the inline-PASM code area documented
- END section: variable limits (16 longs at $1E0..$1EF) and code limits (288 longs from ORG) distinguished

### Enhanced Accuracy

- WRLONG, WRBYTE, WRWORD: timing rows show both cog/LUT and hub-exec ranges
- RET, JMP, JMPREL: timing rows show both cog and hub-exec ranges
- All conditional branches (J*, DJ*, TJ*, IJ*): timing rows show `2 or 4 / 2 or 13-20`
- Conditional Jump Timing Convention subsection opens each instruction chapter that contains branches
- REP: hub-exec section explains the 13+ clock per-iteration cost from the hidden return-jump
- §6.6 ALTx Modified Addressing: Hub-Exec Compatibility note confirms all 11 ALTx variants operate identically in cog-exec and hub-exec

### Code Examples

- MUXQ comparison uses the canonical `mov temp, source` then `and temp, mask` two-instruction pattern
- Special-registers PTRB example uses `wval` as the register name (avoids WORD directive collision)
- Appendix E constants: POSX, NEGX, PI references use `##` augmented-immediate prefix
- Appendix E constants: P2 native mnemonics `fles` and `fges` replace the P1-only `mins` and `maxs`

### Cross-Reference Integrity

- Per-variant anchors for seven four-variant grouped instructions (BITC, FLTC, MUXC, NEGC, OUTC, SUMC, WRC) resolve in PDF output

### Documentation

- Front-matter P1-vs-P2 table shows ~380 documented instructions
- README and creation-guide reflect actual structure (6 chapters Part I, 15 directives, 10 appendices A–J)

---

## v2.2.0 (2026-01-30)

**Code Example Accuracy Release** - Compiler-verified code examples throughout.

### Enhanced Accuracy

- AUGS/AUGD examples: Values correctly demonstrate 9-bit S-field limits
- Constant definitions: Valid CON block syntax throughout
- Operator tables: Corrected character rendering

### Code Verification

- 348 code examples audited with pnut_ts v1.51.7
- Inline PASM examples: Correctly tagged as Spin2

---

## v2.1.0 (2026-01-27)

**Community Feedback Release** - Corrections and expansions based on user review.

### New Content

- "For P1 Developers": P1 vs P2 instruction format comparison table
- "New in P2" features: Digital Video (HDMI/DVI), FIFO hardware, Debug Interrupt
- Section 1.6: Three execution modes documented (COG, LUT, Hub) with PC ranges
- ALT instructions: Pipeline modification coverage (ALTS, ALTD, ALTR, ALTB, ALTI)
- SETQ2: LUT burst transfer documentation added
- HUBSET: Spin2 CON block context note

### Enhanced Accuracy

- Clock specification: 180 MHz nominal; 320 MHz max (per P2 Datasheet)
- LUT timing: RDLUT 3 cycles, WRLUT 2 cycles
- Hub access: Rewritten for P2 slice architecture

### Cross-References

- Part II encoding tables: Added Chapter 2 reference note
- Condition codes: Clarified alias terminology with section reference

---

## v2.0.0 (2026-01-23)

**P1 Migration & Technical Depth Release**

### New Content

- "For P1 Developers" section with P1-to-P2 specification comparison
- CORDIC interrupt protection patterns (Chapter 5, Section 5.1.8)
- REP instruction: extended counts (## prefix), interrupt shielding, memory constraints
- Paletted VGA example in LUT documentation
- Low hub address pitfall warning

### Enhanced Accuracy

- Timing values verified against silicon documentation
- REP and CORDIC hardware constraints documented

### Diagrams

- All diagrams now numbered for cross-referencing
- Hub Memory diagram updated
- Special Registers diagram relocated to Part II

---

## v1.4.0 (2025-12-22)

**Code Example & Effect Reference** - Corrected code examples; added effect support reference.

### Part I: Architectural Foundation

**Chapter 4 - Timing and Determinism:**
- Section 4.7.3: Corrected SUB syntax in profiling examples

### Part II: Instruction Reference

**Code Example Corrections:**
- Effect syntax: Corrected `wc wz` to `wcz` in multiple examples
- Addressing modes: Corrected `#` to `##` for 32-bit immediate values
- QROTATE example: Corrected to use SETQ for Y coordinate

### Part III: Appendices

**Appendix C - Categorical Instruction Index:**
- Added Effect Support Reference section
- Documents WCZ-only, WC-only, WZ-only, and extended effect instructions


## v1.3.0 (2025-12-21)

**Directives, Flags & Compiler Integration Release** - Expanded directive documentation, new Condition Code Reference appendix, flag effect corrections, Chapter 5 scope refinement.

### Part I: Architectural Foundation

**Chapter 1 - The P2 Execution Model:**
- Section 1.2.1: Condensed PR0-PR7 documentation to cross-reference (detailed documentation in Part II)
- Section 1.2.2: Removed duplicate diagram and table; added cross-references to Part II and Appendix C
- Section 1.2: Reduced redundancy
- Section 1.3.1: Added hub memory flexibility note (organization is application-defined)
- Section 1.4.1: Added LUT code execution note (executes code at same speed as COG RAM)
- Section 1.5: Added FIFO explanation for hub execution (distinct from egg-beater for data)
- Section 1.6.2: Corrected hub execution mechanism to FIFO hardware prefetch
- Section 1.6.2: Added FIFO limitation pitfall warning (RDFAST, WRFAST, streamer unavailable during Hub execution)
- Key Concepts: Added LUT execution mode; added FIFO limitation bullet

**Chapter 4 - Timing and Determinism:**
- Section 4.7: Corrected cycle counter description to 64-bit (Rev B/C silicon)
- Section 4.8.2: Corrected hub execution mechanism terminology

**Chapter 5 - Special Hardware Overview:**
- Section 5.6 XBYTE: Documentation condensed
- Section 5.7.3: Corrected boot pin post-boot statement (hardware remains attached; pins under user control)
- Section 5.8 DEBUG: Documentation condensed; detailed coverage expected in P2 Debug Window Manual
- Key Concepts: Condensed XBYTE and DEBUG bullets

**Chapter 2 - The Instruction Format:**
- Section 2.2.1: Simplified condition code table; IF_ALWAYS clarified; moved to Appendix B
- Section 2.2.2: Condensed _RET_ documentation with cross-reference to Appendix B
- Section 2.2.3: Renamed to "Comparison Condition Aliases"; clarified alias choice is stylistic

**Chapter 3 - Flags and Conditional Execution:**
- Section 3.3.3: Replaced condition table with summary; IF_ALWAYS clarified; cross-reference to Appendix B
- Section 3.3.4: Unified comparison alias documentation (Magnitude/Arithmetic terminology)
- Section 3.7.6: Corrected alias terminology in multi-long pattern summary
- Added Section 3.2.6 "Effect Availability" documenting effect permission categories and WCZ validation rules
- Added Section 3.4.4 "Move and Data Instructions" with flag behavior table for MOV, NEG, ABS, NOT, ENCOD, DECOD

### Part II: Directives

**New Documentation:**

- END: Added inline assembly termination directive (syntax, examples, restrictions)

**Enhanced Documentation:**
- ORG: Added `$` symbol explanation, COG/LUT memory regions table, auto-limit behavior, restrictions table
- ORGH: Added behavior by context, address constraints (Spin2 vs PASM-only), mode switching example, restrictions table
- ORGF: Added COG-mode-only restriction, restrictions table
- RES: Added RES 0 alias technique, key characteristics, RES vs LONG comparison table, restrictions table
- FIT: Added behavior by mode (COG vs Hub), common limit values table, additional examples

**Structural:**
- Directive count updated from 14 to 15
- Added "Inline Assembly Directives" category

### Part II: Instruction Reference

#### Encoding Table Corrections

**Signed Arithmetic C Flag:**
- ADDS, ADDSX, SUBS, SUBSX, CMPS: C flag wording clarified for signed operations

**Z Flag Notation Standardization:**
- Standardized comparison operators across all encoding tables: `Result = 0` → `result == 0`
- CMP family: `D = S` → `(D == S)` for clarity
- Extended results: `Z AND (Result = 0)` → `Z AND (result == 0)`

**Column Alignment Fixes:**
- CALL: Removed erroneous "K and PC" from C column; corrected table structure
- CALLD: Removed erroneous "Pxxx and PC" and "D and PC"; C flag corrected to `S[31]`

**Z Flag Structure Fixes:**
- MUL, MULS: Fixed table corruption from pipe character; now `(S == 0) OR (D == 0)`
- TEST, TESTN: Z flag standardized to `(D == 0)`, `((D & S) == 0)`, `((D & !S) == 0)`

#### Narrative Documentation Corrections

**C Flag WCZ Effect Documentation:**

DIR family:
- DIRH, DIRL: Added C flag behavior to WCZ explanation

DRV family:
- DRVC/DRVNC, DRVH, DRVL, DRVZ/DRVNZ: Added C flag behavior to WCZ explanation

OUT family:
- OUTH, OUTL, OUTNOT: Corrected WCZ explanation; C and Z both set to original output state

#### Terminology Standardization

**C Flag Terminology:**
- NEG, NEGC, NEGNC, NEGZ, NEGNZ: Standardized to "MSB of result"
- MUXC, MUXNC, MUXNZ, MUXZ, XOR: Standardized to "parity of result"

**Shift/Rotate Instructions:**
- RCL, RCR, ROL, ROR, SAL, SAR, SHL, SHR: Added footnote for S[4:0] = 0 edge case

**Limit Instructions:**
- FGE, FGES, FLE, FLES: Added footnote for "limit enforced" semantics

**Pin I/O Flag Descriptions:**
- OUT, FLT, DIR, DRV families: Standardized flag terminology with footnotes

**Miscellaneous:**
- XOR: Z flag standardized to "result == 0"
- ZEROX: C and Z flags standardized

#### Documentation Additions

- COGINIT: Added execution mode constants reference table (COGEXEC, HUBEXEC, and _NEW variants)
- MODCZ: Added modifier constants table (complements Appendix G)
- WAITATN: Added event flag re-trigger clarification
- WAITCT1/WAITCT2/WAITCT3: Added re-trigger clarification and counter comparison formula
- SCA, SCAS: Added interrupt shielding note
- FLT family: Added pipeline data-forwarding caveat (DIRx not forwarded; only OUTx forwarded)
- PTRA/PTRB: Code example comments trimmed
- GETCT: Corrected encoding table, code example, and WC effect description

### Part III: Appendices

**Appendix Restructuring:**
- Added new Appendix B: Condition Code Reference
- Renumbered subsequent appendices (B→C through I→J)
- Updated cross-references

**Appendix B - Condition Code Reference (NEW):**
- Complete 16-condition table with EEEE encodings and aliases
- IF_ALWAYS clarified (encoding used when no condition specified)
- Comparison aliases (Magnitude/Arithmetic terminology)
- Flag state aliases, logical aliases, commutative forms
- Complete _RET_ documentation with XBYTE patterns

**Appendix D - Predefined Constants (formerly Appendix C):**
- COGEXEC_NEW, COGEXEC_NEW_PAIR, HUBEXEC_NEW, HUBEXEC_NEW_PAIR: Expanded with encoding, usage examples

**Appendix E - Debug Configuration:**
- DEBUG_MAIN, DEBUG_COGINIT: Examples corrected

**Appendix H - Reserved Words (formerly Appendix G):**
- Comparison alias headers updated to Magnitude/Arithmetic terminology
- IF_ALWAYS clarified

---

## v1.2.0 (2025-12-13)

**Community Feedback Release** - Additional corrections from user review of v1.0.0.

### Part I: Architectural Foundation

- LUT Sharing: Corrected shared capacity from 1024 to 512 longs per cog
- DIRZ/DIRNZ example table: Fixed C, Result, and CZI column values
- ADD example table: Fixed column alignment
- IF_ prefix timing: Corrected from 1 cycle to 2 cycles (without WC/WZ/WCZ)
- MODC/MODZ/MODCZ: Clarified WC/WZ/WCZ requirement; register-only D operand

### Part II: Instruction Reference

**Encoding Table Corrections:**
- Systematic fix across 26 files (~380 rows): C, Z, Result columns realigned
- ALT instructions (11 total): C/Z/Result columns corrected; CZI bits are sub-opcode selectors, not flag controls
- ALTI syntax 2: Result column corrected (D, not ---)
- AUGD/AUGS: C column cleared (no flag effects)
- MODC/MODZ/MODCZ: Syntax corrected to show WC/WZ/WCZ as required

**Flag Effect Fixes:**
- FLT* instructions: C/Z flags corrected to "Original OUTx base bit"
- DIR* instructions (DIRH, DIRL, DIRNOT): Z flag added (C,Z = DIRx)
- DRV* instructions (DRVH, DRVL, DRVNOT): Z flag added (C,Z = DIRx* + OUTx)
- OUT* instructions (OUTH, OUTL, OUTNOT): C flag added (C,Z = Original OUTx base bit)
- LOCKREL: C flag added (LOCK status)
- WAITX: Timing corrected to 2 + Dest; added randomized delay documentation

### Directives

**Corrections:**
- BYTE, WORD, LONG, ALIGNL, ALIGNW: Removed incorrect auto-alignment statements
- BYTEFIT: Syntax corrected; range fixed to -$80 to $FF
- WORDFIT: Syntax corrected; range fixed to -$8000 to $FFFF
- FILE: Added filename requirements and search order documentation

**Rewrites:**
- DITTO: Complete rewrite (block-based replication with `$$` index, PNut v50+)

### Presentation

- Timing tables (RDBYTE, RDFAST, RDLONG, RDWORD): Fixed table rendering
- Cross-reference anchors: Fixed literal hypertarget commands in PDF output

---

## v1.1.0 (2025-12-12)

**Audit-Verified Release** - Comprehensive audit by Claude Opus 4.5 with 8 parallel agents verified ~19,600 lines across 41 files against authoritative sources (P2 Instructions v35 CSV, Silicon Documentation v35).

### Part II: Instruction Reference

#### Encoding Table Corrections

**Flag Effect Fixes:**
- ABS: Z flag corrected
- ADDCT1/ADDCT2/ADDCT3: C flag documentation added
- DECMOD: C flag wording aligned with CSV
- MUL/MULS: Z flag corrected to `(D = 0) OR (S = 0)`
- TEST: C/Z flags corrected to `Parity of (D & S)` and `(D & S) = 0`
- LOCKNEW: C flag column alignment corrected
- LOCKTRY: Verified correct (C flag for lock acquisition)

**Column Alignment Fixes:**
- BITC, BITNC, BITZ, BITNZ, BITH, BITL, BITNOT, BITRND: Encoding table columns realigned
- CMPM, CMPSUB, COGID, COGINIT: Encoding table columns realigned with footnotes
- OUTRND: Encoding table columns realigned

**Timing Documentation:**
- RDBYTE, RDWORD, RDLONG, RDFAST: Added 4-context timing tables (COG, Hub, COG+interrupts, Hub+interrupts)
- RETA, RETB: Added 4-context timing tables (COG: 11...18, Hub: 20...40, COG+int: 11...26, Hub+int: 20...70)

**Other Fixes:**
- AKPIN: Encoding corrected
- COGATN: Timing cycles added

### Part I: Architectural Foundation

- `_RET_` prefix: Clarified behavior and interaction with conditional execution
- Flag aliases: Documented C/NC, Z/NZ flag test aliases
- Conditional aliases: Complete IF_x condition code reference verified

### Part III: Appendices

#### Appendix A - Encoding Master Table
- **Instruction Encodings table**: Fixed multi-page rendering (was truncated to first page only). Table now spans all pages with repeating headers.
- CALLD: Opcode added (`1011001` with CZI effects) - was marked as `---`

#### Appendix B - Categorical Index
- **Arithmetic Operations table** (112 rows): Fixed multi-page rendering
- **Events and Timing table** (34 rows): Fixed multi-page rendering
- MUL: Z flag fixed (markdown table parsing issue with `|` character)
- MULS: Z flag fixed (same issue)
- TEST: C and Z flag effects corrected
- Instruction count clarified: "357 executable + 2 compiler directives"

#### Appendix G - Reserved Words
- Added missing DEBUG configuration symbols:
  - DEBUG_COGINIT, DEBUG_MAIN, DEBUG_MASK, DEBUG_DISABLE
  - DEBUG_PIN_TX, DEBUG_PIN_RX

#### Appendix H - Glossary
- Cross-reference verified correct (Appendix A for encoding tables)

### Verification Notes

**Sections Verified Excellent (Zero Issues Found):**
- Instructions E-J (74 instruction variants)
- Instructions P-Q (23 instructions)
- Instructions S-Z (105 instruction names, 121 variants)
- Appendices D-F (Constants)
- PR0-PR7 registers confirmed correct (software convention for Spin2/PASM2 interop)

**Sources Used for Verification:**
- P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv
- Silicon Documentation v35 (p2-documentation.txt)
- Parallax PASM2 Manual Draft (2022-11-01)
- Spin2 Language Manual v51a
- P2-Knowledge-Base YAML instruction definitions

### Presentation

- Code block colors aligned with IDE conventions (Propeller Tool, Spin Tools IDE):
  - PASM2 blocks: Green color family
  - Spin2 blocks: Blue color family
- Key Concepts boxes: Changed from blue to deep purple to distinguish from Spin2 code blocks
- Large tables (30+ rows): Now span multiple pages with repeating headers
- PDF navigation pane enabled (bookmarks sidebar opens automatically)

---

## v1.0.0 (2025-12-11)

Initial community review release.

- Complete instruction reference (380+ instruction variants)
- Full encoding tables with opcode patterns
- Comprehensive appendices (A-I)
- Categorical instruction index
- Reserved words reference (1,236+ identifiers)
