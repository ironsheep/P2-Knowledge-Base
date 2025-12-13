# P2 Assembly Language Reference Manual - Changelog

## v1.2.0 (2025-12-13)

**Community Feedback Release** - Additional corrections from user review of v1.0.0, addressing issues not caught in the v1.1.0 audit pass.

### Part I: Architectural Foundation

#### Chapter 1 - Execution Model
- **LUT Sharing**: Corrected shared LUT capacity from 1024 longs to 512 longs (each cog contributes its 512-long LUT for a combined 1024-long shared space, but each cog can only access 512 longs at a time)

#### Chapter 3 - Flags
- **Conditional Execution Timing**: Corrected IF_ prefix timing from 1 cycle to 2 cycles when WC/WZ/WCZ effects are not used
- **MODC/MODZ/MODCZ**: Added requirement that WC, WZ, or WCZ effect must be specified; clarified register-only D operand (no immediates); corrected syntax examples

### Part II: Instruction Reference

#### Encoding Table Column Corrections
- **Systematic fix across 26 files (~380 table rows)**: C, Z, and Result columns were shifted left by one position throughout. All instruction encoding tables now correctly show:
  - C column: Flag effect (e.g., "carry of (D + S)", "S[31]", "Parity")
  - Z column: Flag effect (e.g., "Result = 0", "Zero")
  - Result column: Destination register (e.g., "D", "PC", "---")

#### MODC/MODZ/MODCZ (instructions-m.md)
- Corrected syntax to show WC/WZ/WCZ as required, not optional
- Updated encoding table column values
- Enhanced explanation of flag modification behavior

#### Deep Audit Corrections (instructions-f.md, instructions-w.md)

**FLT* Instructions** (FLTC, FLTNC, FLTZ, FLTNZ, FLTH, FLTL, FLTNOT, FLTRND):
- Corrected C and Z flag columns from "DIRx + OUTx" to "Original OUTx base bit" per Silicon CSV ("C,Z = OUT bit")
- Corrected Result column from "OUT bit" to "OUTx"
- Updated explanation text: "Z flag" → "C and Z flags" for WCZ effect

**WAITX Instruction**:
- Corrected timing formula from "Dest+1" to "2 + Dest" per Silicon CSV
- Added randomized delay behavior documentation (when WC/WZ/WCZ specified)
- Fixed code example comment: "Wait 100" → "Wait 101 clock cycles (2 + 99)"

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
