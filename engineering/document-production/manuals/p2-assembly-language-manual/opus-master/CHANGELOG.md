# P2 Assembly Language Reference Manual - Changelog

## v1.2.0 (2025-12-13)

**Community Feedback Release** - Additional corrections from user review of v1.0.0, addressing issues not caught in the v1.1.0 audit pass.

### Part I: Architectural Foundation

#### Chapter 1 - Execution Model
- **LUT Sharing**: Corrected shared LUT capacity from 1024 longs to 512 longs (each cog contributes its 512-long LUT for a combined 1024-long shared space, but each cog can only access 512 longs at a time)

#### Chapter 2 - Instruction Format
- **Section 2.4.1 DIRZ/DIRNZ example table**: Fixed C column (`D` → `DIRx`), Result column (`Orig bit` → `DIR bit`), CZI column (`CZ0` → `CZL`)
- **Section 2.8.3 ADD example table**: Fixed column shift - C column (`D` → `carry of (D + S)`), Z column (`carry of (D + S)` → `Result = 0`), Result column (`Result = 0` → `D`)

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

### Directive Documentation Corrections (directives.md)

**Data Packing and Alignment** (based on PNut_ts compiler analysis):
- Corrected all incorrect "auto-alignment" statements throughout directives section
- BYTE, WORD, LONG: Changed "automatically aligned" to "packs sequentially; use ALIGNW/ALIGNL if needed"
- ALIGNL, ALIGNW: Fixed explanatory text that incorrectly implied automatic alignment of subsequent data
- Related Directives sections: Removed "(auto-aligned in hub)" annotations
- Added clarifying note to ALIGNW example: subsequent data packing is coincidental, not automatic
- Key finding: Spin2/PASM2 has NO automatic alignment—data packs sequentially without gaps

**DITTO Directive** (complete rewrite—previous documentation was entirely wrong):
- Old (incorrect): Described as "Repeat Previous Instruction" with no parameters
- New (correct): Block-based code/data replication: `DITTO count` ... `DITTO END`
- Documented `$$` symbol for iteration index (0 to count-1)
- Added zero count behavior (block skipped entirely)
- Added restriction table: ORG/ORGH not allowed inside, `$$` only valid inside block
- Added multi-instruction block examples
- Introduced in PNut version 50

**FILE Directive**:
- Added filename requirements section documenting invalid characters (`/`, `:`, `*`, `?`, `"`, `<`, `>`, `|`)
- Documented file search order (current dir → library dir → include dirs)
- Added compiler-specific footnote about include directory support
- Added maximum filename length (253 characters) and case-insensitivity notes

**BYTEFIT Directive** (complete rewrite):
- Corrected syntax: `BYTEFIT value` (no parentheses) — it's a data directive like BYTE
- Fixed valid range: -$80 to $FF (was incorrectly documented as 0-255 only)
- Added proper examples without parentheses
- Added actual error message: `BYTEFIT values must range from -$80 to $FF`

**WORDFIT Directive** (complete rewrite):
- Corrected syntax: `WORDFIT value` (no parentheses) — it's a data directive like WORD
- Fixed valid range: -$8000 to $FFFF (was incorrectly documented as 0-65535 only)
- Added proper examples without parentheses
- Added actual error message: `WORDFIT values must range from -$8000 to $FFFF`

### PDF Rendering Fixes

**Timing Table Rendering (instructions-r.md)**:
- Fixed RDBYTE, RDFAST, RDLONG, RDWORD timing tables not rendering as tables
- Root cause: Missing blank line between footnote text and table header
- Tables now render with proper headers instead of inline text

**Cross-Reference Anchor Rendering**:
- Fixed hypertarget commands appearing literally in PDF (e.g., `\{}hypertarget{resi1}{}`)
- Affected instructions: RESI0-3, RETI0-3, SETINT1-3, NIXINT1-3, ADDCT1-3, POLLCT1-3, WAITCT1-3, WAITSE1-4, SETSE1-4, TRGINT1-3, JCT1-3, JSE1-4, and their negated variants
- Root cause: LaTeX escape processor was escaping `\hypertarget` commands
- Solution: Added hypertarget pattern to protected LaTeX commands (escape processor v6)

### Voice and Style Consistency (directives.md)

**Voice Guide Audit**:
- Removed minimizing language ("simply") from ORG, ORGF descriptions
- Removed second-person constructions ("when you need") from ORGF, BYTEFIT, WORDFIT
- Removed hedging language ("might change", "typically") from BYTEFIT, WORDFIT, FILE
- Changed "may be emitted" to definitive statements in ALIGNL, ALIGNW examples
- All Usage sections now use third-person reference voice per voice-guide.md

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
