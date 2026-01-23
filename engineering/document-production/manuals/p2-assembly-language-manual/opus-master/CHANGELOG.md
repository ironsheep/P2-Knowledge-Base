# P2 Assembly Language Reference Manual - Changelog

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
