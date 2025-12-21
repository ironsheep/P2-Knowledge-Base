# P2 Assembly Language Reference Manual - Changelog

## v1.3.0 (2025-12-15)

**Directives, Flags & Compiler Integration Release** - Expanded directive documentation, new Condition Code Reference appendix, systematic corrections from internal consistency audit, enhanced flag documentation from PNut-TS compiler analysis, Parallax draft audit, user feedback audit (hub execution mechanism correction), and Chapter 5 scope alignment.

### Part I: Architectural Foundation

**Chapter 1 - The P2 Execution Model:**
- Section 1.2.1: Condensed PR0-PR7 documentation to cross-reference (detailed documentation in Part II)
- Section 1.2.2: Removed duplicate diagram and table; added cross-references to Part II and Appendix C
- Section 1.2: Reduced redundancy (~35 lines) while preserving conceptual clarity
- Section 1.3.1: Added hub memory flexibility note (organization is application-defined)
- Section 1.4.1: Added LUT code execution note (executes code at same speed as COG RAM)
- Section 1.5: Added FIFO explanation for hub execution (distinct from egg-beater for data)
- Section 1.6.2: Corrected hub execution mechanism—changed "egg-beater access pattern" to "FIFO hardware prefetch" (critical error fix from user feedback audit)
- Section 1.6.2: Added FIFO limitation pitfall warning (RDFAST, WRFAST, streamer unavailable during Hub execution)
- Key Concepts: Added LUT execution mode; added FIFO limitation bullet

**Chapter 4 - Timing and Determinism:**
- Section 4.8.2: Corrected hub execution mechanism—changed "egg beater hub access mechanism" to "FIFO prefetch mechanism" (consistency fix)

**Chapter 5 - Special Hardware Overview:**
- Section 5.6 XBYTE: Replaced with properly-scoped version (~151 lines → ~50 lines); removed marketing language; retained technical essentials with instruction cross-references
- Section 5.7.3: Corrected boot pin post-boot statement—hardware (SPI Flash, SD card, serial interface) remains attached after boot; pins are under user code control but practical usage depends on connected hardware
- Section 5.8 DEBUG: Replaced with properly-scoped version (~301 lines → ~50 lines); content relocated to P2 Debug Window Manual; retained essential awareness for PASM2 programmers
- Key Concepts: Condensed XBYTE and DEBUG bullets to match revised section scope

**Chapter 2 - The Instruction Format:**
- Section 2.2.1: Simplified condition code table; full alias documentation moved to Appendix B
- Section 2.2.2: Condensed _RET_ documentation with cross-reference to Appendix B for advanced patterns
- Section 2.2.3: Renamed from "Signed vs. Unsigned Comparison Condition Codes" to "Comparison Condition Aliases"; clarified that alias choice (IF_A vs IF_GT) is stylistic, not functional

**Chapter 3 - Flags and Conditional Execution:**
- Section 3.3.3: Replaced 16-row condition table with brief summary and cross-reference to Appendix B
- Section 3.3.4: Unified comparison alias documentation; both terminology styles (Magnitude/Arithmetic) now presented as equivalent
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

**Signed Arithmetic C Flag (5 instructions):**
- ADDS, ADDSX, SUBS, SUBSX, CMPS: C flag description now uses "correct sign of" wording to clarify borrow/carry behavior for signed operations

**Z Flag Notation Standardization (71 occurrences):**
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

**C Flag WCZ Effect Documentation (12 instructions):**

DIR family:
- DIRH, DIRL: Added missing C flag behavior to WCZ explanation

DRV family:
- DRVC/DRVNC, DRVH, DRVL, DRVZ/DRVNZ: Added missing C flag behavior to WCZ explanation

OUT family:
- OUTH, OUTL, OUTNOT: Corrected WCZ explanation (removed incorrect "C flag is not affected"); now documents C and Z both set to original output state

#### Terminology Standardization

**C Flag Terminology (10 instructions):**
- NEG, NEGC, NEGNC, NEGZ, NEGNZ: Changed "Sign of result" / "Sign" to "MSB of result"
- MUXC, MUXNC, MUXNZ, MUXZ, XOR: Changed "Parity" to "parity of result"

**Shift/Rotate Instructions (8 instructions):**
- RCL, RCR, ROL, ROR, SAL, SAR, SHL, SHR: Added footnote clarifying edge case when S[4:0] = 0

**Limit Instructions (4 instructions):**
- FGE, FGES, FLE, FLES: Added footnote explaining "limit enforced" means C = 1 if D changed, else C = 0

**Pin I/O Flag Descriptions (standardized with footnotes):**
- OUT family (8 instructions): Changed verbose "Original OUTx base bit" / "orig out" to "OUT bit" with footnote
- FLT family (8 instructions): Changed "Original OUTx base bit" to "OUT bit" with footnote
- DIR family (8 instructions): Changed "DIRx" / "Original DIRx base bit" to "DIR bit" with footnote
- DRV family (8 instructions): Changed "DIRx* + OUTx" to "OUT bit" with footnote

**Miscellaneous:**
- XOR: Z flag changed from "Zero" to "result == 0"
- ZEROX: C flag changed from "MSB" to "MSB of result"; Z flag changed from "Zero" to "result == 0"

#### Documentation Additions

- COGINIT: Added execution mode constants reference table (COGEXEC, HUBEXEC, and _NEW variants)

#### Parallax Draft Audit (corroborated against Silicon Documentation)

- MODCZ: Added modifier constants table to instruction block (complements Appendix G)
- WAITATN: Added event flag re-trigger clarification
- WAITCT1/WAITCT2/WAITCT3: Added re-trigger clarification; added mathematical formula for counter comparison (MSB of CT - CTx = 0)
- SCA, SCAS: Added interrupt shielding note

#### Chip Gracey Confirmation

- FLTC, FLTNC, FLTZ, FLTNZ, FLTH, FLTL, FLTNOT, FLTRND: Added pipeline data-forwarding caveat (DIRx not forwarded; only OUTx forwarded)

### Part III: Appendices

**Appendix Restructuring:**
- Added new Appendix B: Condition Code Reference (canonical source for all IF_x conditions, aliases, and _RET_ behavior)
- Renumbered subsequent appendices: B→C (Categorical Index), C→D (Special Registers), D→E (Constants), E→F (Smart Pin), F→G (Streamer), G→H (Reserved Words), H→I (Glossary), I→J (Known Bugs)
- Updated cross-references in front-matter and chapters

**Appendix B - Condition Code Reference (NEW):**
- Complete 16-condition table with EEEE encodings and all aliases
- Comparison aliases presented as two equivalent terminology styles (Magnitude: IF_A/IF_B; Arithmetic: IF_GT/IF_LT)
- Flag state aliases (IF_00, IF_01, IF_10, IF_11, IF_0X, IF_1X, IF_X0, IF_X1)
- Logical aliases (IF_SAME, IF_DIFF, IF_NOT_xx)
- Commutative forms reference
- Complete _RET_ documentation with XBYTE patterns and timing

**Appendix H - Reserved Words (formerly Appendix G):**
- Comparison alias section headers changed from "Unsigned/Signed" to "Magnitude/Arithmetic terminology"

**Appendix D - Predefined Constants (formerly Appendix C):**
- COGEXEC_NEW: Expanded with encoding note, description, usage example, and related constants
- COGEXEC_NEW_PAIR: Expanded with LUT sharing documentation and usage example
- HUBEXEC_NEW: Expanded with hub execution details and usage example
- HUBEXEC_NEW_PAIR: Expanded with combined benefits documentation and usage example

**Source Material:**
- WC-WZ-WCZ-Effects-Guide.md (PNut-TS compiler documentation)
- PASM2-Authoring-Guide.md (PNut-TS compiler documentation)
- Parallax PASM2 Manual Draft (2022-11-01)
- Silicon Documentation v35 (lines 742-751 for hub FIFO, 5152, 5206, 5299-5317, 5674)
- Chip Gracey direct confirmation (2025-12-17)
- User feedback audit (2025-12-17): Community review identifying hub execution mechanism error
- User feedback audit (2025-12-20): Boot pin post-boot statement correction; P2 Eval Board Rev C documentation ("hardwired" SD card socket), Edge Mini Breakout documentation (Flash SPI pin assignments)
- User feedback audit (2025-12-21): PDF rendering corrections, footnote symbols, code line length

### Additional Corrections (2025-12-21)

**Part I:**
- Chapter 2, Section 2.2.1: IF_ALWAYS clarified (encoding used when no condition specified, not "the default")
- Chapter 3, Section 3.3.3: IF_ALWAYS clarified (same correction)

**Part II:**
- Special Registers: PTRA/PTRB code example comments trimmed for line length
- Shift/Rotate instructions (8): Footnote symbol changed from superscript to † (dagger)
- Pin I/O instructions (OUT, FLT, DRV families): Footnote symbol changed from superscript to †

**Part III:**
- Appendix B: IF_ALWAYS clarified (same correction as Chapter 2)
- Appendix E: DEBUG_MAIN, DEBUG_COGINIT examples corrected (symbol presence sufficient; removed "= TRUE")
- Appendix H: IF_ALWAYS clarified (same correction)

### Presentation

- Encoding tables (Appendix A): Fixed multi-page rendering regression
- Grid tables: Converted to pipe format for Lua filter compatibility (Chapters 4-5, Appendices G, J)
- Not-equal symbols: Changed ≠ to != for LaTeX compatibility
- Footnote symbols: Changed ^1^ to † (dagger) for proper PDF rendering

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
