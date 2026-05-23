# P2 Assembly Language Reference Manual - Changelog

## v2.3.0 (2026-05-22)

**Periodic Audit Release** — Absorbs ~4 months of PASM2 YAML corrections and closes a silent multitasking gap.

### Critical Fix

- **Inline PASM × Multitasking taskptr overlap** (directives.md, END section): Documented the previously-undocumented overlap between the multitasking taskptr table ($100..$11F) and the inline-PASM code area ($000..$11F). Programs using both inline PASM and multitasking could silently lose code space without compile-time warning.

### Hub-Exec Timing Corrections

Brought timing tables and prose in line with April 2026 YAML corrections (commits fbbd9ee, 96cf4e8 "Data-set-wide timing-claim corrections"):

- **WRLONG, WRBYTE, WRWORD**: Timing now shows `3...10 / 3...20 †` (cog/LUT vs hub execution); Explanation prose updated accordingly.
- **RET**: Timing now shows `4 / 13-20 †` with context-table footnote.
- **JMP, JMPREL**: Timing now shows `4 / 13-20 †` with context-table footnote.
- **Conditional branches** (J* event-jumps, JCT*, JATN, JFBW, JINT, JPAT, JQMT, JSE*, JX*, DJ*, TJ*, IJ*): Updated `2 or 4` rows to `2 or 4 / 2 or 13-20`. Each affected instructions-*.md file now opens with a "Conditional Jump Timing Convention" subsection explaining the notation.
- **REP** (instructions-r.md): Rewrote the hub-exec paragraph from "NOT truly zero-overhead" framing to the corrected model: REP works in hub-exec, paying 13+ clocks per iteration for the hidden return-jump.

### ALTx Family Hub-Exec Documentation

- **chapter-06**: Added a "Hub-Exec Compatibility" note at the top of §6.6 ALTx Modified Addressing, documenting that all 11 ALTx instructions (ALTI, ALTS, ALTD, ALTR, ALTB, ALTSN, ALTSB, ALTSW, ALTGN, ALTGB, ALTGW) operate identically in cog-exec and hub-exec modes (per Chip Gracey clarification 2026-05-02).

### Inline-PASM Variable vs Code Limit Clarification

- **directives.md** (END section): Added a "Variable vs Code Limits in Inline PASM" subsection clarifying that the 16-long limit applies to variables only ($1E0..$1EF), while PASM code is buffered separately into cog registers starting at the ORG address (default $000), with up to 288 longs of code space.

### Cross-Reference Integrity

- Added `\hypertarget` anchors for 7 four-variant grouped instruction headings (BITC, FLTC, MUXC, NEGC, OUTC, SUMC, WRC), making per-variant anchor references (e.g. `[BITNZ](#bitnz)`) resolve correctly in PDF output.

### Documentation Polish

- **front-matter.md** P1-vs-P2 table: Updated instruction count from "~360" to "~380" to align with actual documented entry count.
- **README.md** directory listing: Updated to reflect actual structure (6 chapters in Part I, 15 directives in directives.md, 10 appendices A–J in Part III).
- **../creation-guide.md** §1.1: Corrected directive count from "10" to "15" to match current manual scope.
- **directives.md** code example: Renamed user label `bc_vectors` to `dispatch_table` to avoid visual collision with the `bc_`-prefixed compiler-bytecode naming convention.
- **chapter-01, chapter-05**: Replaced two unsourced "eliminates" capability claims with sourced/cross-referenced wording.

### Code Example Validation (pnut_ts v1.51.7)

Compiled every `pasm2` / `spin2` code block in the manual (348 total). Found and fixed **7 real bugs** in code examples:

- `instructions-m.md` MUXQ comparison: replaced invalid 3-operand `and temp, source, mask` with the correct `mov temp, source` + `and temp, mask` sequence; updated "Traditional approach (3 instructions)" comment to "(4 instructions)".
- `special-registers.md` PTRB example: renamed register `word` to `wval` to avoid collision with the WORD directive keyword.
- `appendix-e-constants.md`: corrected six bare-immediate uses of 32-bit Spin2 constants by adding the `##` augmented-immediate prefix — `POSX`, `NEGX`, and `PI` references in `cmp`/`cmps`/`mov` instructions.
- `appendix-e-constants.md`: replaced two P1 mnemonics that don't exist in P2 PASM2 — `mins` → `fles` (Force Less or Equal, Signed), `maxs` → `fges` (Force Greater or Equal, Signed).

After fixes, 296 of 348 blocks (85%) compile clean. The remaining 52 are pedagogical fragments and syntax templates that cannot compile in isolation by design (placeholder mnemonics like `INSTR D, S`, FILE directive with placeholder filenames, "wrong example" demos in the Reserved Words appendix, etc.). Full breakdown and methodology in `code-validation/VALIDATION-REPORT.md`.

### Audit Artifacts

- New: `audit/periodic-audit-2026-05-22.md` — full periodic-audit findings report driving this release.
- New: `AUDIT-PROCESS.md` at the manual folder root — reusable periodic-audit process document.
- New: `code-validation/` folder — extractor script (`extract-and-validate.py`), per-example wrapped sources, results JSON, and the validation report.

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
