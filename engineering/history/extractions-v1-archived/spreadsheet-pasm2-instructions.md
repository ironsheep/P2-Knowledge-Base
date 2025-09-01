# P2 PASM2 Instruction Spreadsheet Extraction

## Source Document
- **Official Name**: P2 Instructions v35 - Rev B/C Silicon
- **Author**: Chip Gracey (P2 Designer)
- **Source**: Available from [Parallax.com](https://www.parallax.com)
- **Local Path**: `/import/p2/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv`
- **Type**: CSV spreadsheet with complete instruction reference
- **Processed**: 2025-08-14
- **Total Rows**: 514 (including headers)

## Extraction Summary
This is the complete extraction from the P2 instruction spreadsheet, preserved as an independent analysis.

---

## Part 1: PASM2 Instruction Extraction

### Overall Statistics
- **Total Instructions**: 491 entries (365 core instructions + aliases/variants)
- **Instruction Width**: 32-bit fixed
- **Register Count**: 512 cog registers (addresses $000-$1FF)

### Instructions by Category

#### 1. Math and Logic (115+ instructions)
- **Arithmetic**: ADD, SUB, MUL, DIV, MULS, SCA, SCAS
- **Bitwise**: AND, OR, XOR, NOT, ANDN
- **Shifts/Rotates**: ROR, ROL, SHR, SHL, RCR, RCL, SAR, SAL
- **Comparisons**: CMP, CMPS, CMPR, CMPM, CMPX, CMPSX
- **Bit Operations**: TESTB, BITL, BITH, BITC, BITNC, BITZ, BITNZ, BITRND, BITNOT
- **Data Processing**: ENCOD, ONES, DECOD, BMASK, ZEROX, SIGNX, REV, MERGEB, SPLITB

#### 2. Branch and Flow Control (85+ instructions)
- **Unconditional**: JMP, CALL, RET, CALLA, RETA, CALLB, RETB
- **Conditional Tests**: DJZ, DJNZ, TJZ, TJNZ, TJF, TJNF, TJS, TJNS, TJV
- **Skip Instructions**: SKIP, SKIPF, EXECF
- **Stack-based**: PUSH, POP, PUSHA, PUSHB, POPA, POPB

#### 3. Hub RAM Operations (15+ instructions)
- **Read**: RDBYTE, RDWORD, RDLONG, RDLUT
- **Write**: WRBYTE, WRWORD, WRLONG, WRLUT, WMLONG
- **Block Transfers**: SETQ, SETQ2 (enable burst mode)

#### 4. Smart Pins (10+ instructions)
- **Configuration**: WRPIN, WXPIN, WYPIN, SETDACS
- **Status**: RDPIN, RQPIN, AKPIN
- **Test**: TESTP, TESTPN with AND/OR/XOR modifiers

#### 5. Events System (60+ instructions)
- **Setup**: SETSE1-4, SETPAT, ADDCT1-3
- **Polling**: POLLINT, POLLCT1-3, POLLSE1-4, POLLPAT, POLLQMT
- **Waiting**: WAITINT, WAITCT1-3, WAITSE1-4, WAITPAT
- **Branching**: JINT, JCT1-3, JSE1-4, JPAT

#### 6. CORDIC Solver (10+ instructions)
- **Math**: QMUL, QDIV, QFRAC, QSQRT
- **Trigonometric**: QROTATE, QVECTOR
- **Logarithmic**: QLOG, QEXP
- **Results**: GETQX, GETQY

#### 7. Pin I/O Control (35+ instructions)
- **Direction**: DIRL, DIRH, DIRC, DIRNC, DIRZ, DIRNZ, DIRRND, DIRNOT
- **Output**: OUTL, OUTH, OUTC, OUTNC, OUTZ, OUTNZ, OUTRND, OUTNOT
- **Float**: FLTL, FLTH, FLTC, FLTNC, FLTZ, FLTNZ, FLTRND, FLTNOT
- **Drive**: DRVL, DRVH, DRVC, DRVNC, DRVZ, DRVNZ, DRVRND, DRVNOT

#### 8. Hub FIFO Operations (10+ instructions)
- **Setup**: RDFAST, WRFAST, FBLOCK, GETPTR
- **Read**: RFBYTE, RFWORD, RFLONG, RFVAR, RFVARS
- **Write**: WFBYTE, WFWORD, WFLONG

#### 9. Register Indirection (15+ instructions)
- **Field Alteration**: ALTR, ALTD, ALTS, ALTB, ALTI
- **Nibble/Byte/Word**: ALTSN, ALTGN, ALTSB, ALTGB, ALTSW, ALTGW

#### 10. Specialized Hardware
- **Pixel Mixer**: ADDPIX, MULPIX, BLNPIX, MIXPIX, SETPIV, SETPIX
- **Color Space**: SETCY, SETCI, SETCQ, SETCFRQ, SETCMOD
- **Streamer**: XINIT, XSTOP, XZERO, XCONT, SETXFRQ, GETXACC

### Instruction Encoding Pattern
```
EEEE OOOOOOO CZI DDDDDDDDD SSSSSSSSS
│    │       │││ │         │
│    │       │││ │         └─ 9-bit Source (register or immediate)
│    │       │││ └─────────── 9-bit Destination register
│    │       ││└───────────── I: Immediate flag (1 = #S)
│    │       │└────────────── Z: Zero flag modifier
│    │       └─────────────── C: Carry flag modifier
│    └──────────────────────── 7-bit Opcode
└───────────────────────────── 4-bit Condition code (EEEE)
```

### Addressing Modes
- **Register Direct**: D and S specify register addresses
- **Immediate**: #S provides 9-bit immediate (I=1)
- **Extended Immediate**: AUGS/AUGD extend to 32-bit
- **Indirect via PTRx**: PTRA/PTRB with auto-increment/decrement
- **Bit-field**: Instructions can specify bit ranges [31:0]

### Condition Codes (EEEE field)
- Controls conditional execution of instructions
- 16 possible conditions (details in silicon doc)
- Special: 0000 = never, 1111 = always

---

## Part 2: Questions & Unknowns
*These questions emerge from spreadsheet analysis and will be answered by the Silicon Document*

### Architecture Questions
- [ ] What exactly is a COG and how does it relate to traditional CPU cores?
- [ ] What is the hub memory architecture and how is it shared among 8 COGs?
- [ ] What does "hub slot timing" mean (9-16 cycles variable)?
- [ ] What is LUT RAM and how does it differ from COG RAM?
- [ ] How do COGs achieve non-interference at runtime?
- [ ] What are hub exec, cog exec, and LUT exec modes?
- [ ] What determines the 8-cog vs 16-cog timing modes?

### Memory System Questions
- [ ] What is the memory map (COG RAM, LUT RAM, Hub RAM addresses)?
- [ ] How do PTRA and PTRB pointers work with auto-increment/decrement?
- [ ] What are "hub longs" and why does crossing them add cycles?
- [ ] How does the FIFO system work for streaming transfers?
- [ ] What is the difference between SETQ and SETQ2 for block transfers?
- [ ] How do stack operations work (PUSHA/B, POPA/B)?

### Instruction Execution Questions
- [ ] What are the 16 condition codes (EEEE field values)?
- [ ] How does instruction prefixing work (AUGS/AUGD)?
- [ ] What does "Next Inst Shielded from Interrupt" mean?
- [ ] How do ALT instructions modify the following instruction?
- [ ] What is the REP instruction and how does it work?
- [ ] How do SKIP/SKIPF/EXECF instructions operate?

### Flag Operations Questions
- [ ] What exactly do C (carry) and Z (zero) flags represent?
- [ ] What does "C = parity of result" mean for logic operations?
- [ ] How do extended operations (ADDX, SUBX) use flags?
- [ ] What is the difference between WC/WZ and ANDC/ANDZ modifiers?
- [ ] How do conditional operations use flag states?

### Smart Pin Questions
- [ ] What are Smart Pins and what makes them "smart"?
- [ ] What are the Smart Pin modes referenced in the spreadsheet?
- [ ] How do WRPIN, WXPIN, WYPIN configure pins differently?
- [ ] What is SETDACS and how does it relate to DACs?
- [ ] How do pins interact with the event system?
- [ ] What is the difference between DIR, OUT, FLT, and DRV pin operations?

### Event System Questions
- [ ] What types of events can be detected?
- [ ] How do SE1-4 (Selectable Events) work?
- [ ] What are CT1-3 (Counter/Timers)?
- [ ] How does pattern matching (PAT) work?
- [ ] What is the relationship between polling and waiting?
- [ ] How do event-triggered branches work?

### CORDIC Solver Questions
- [ ] What is a CORDIC solver and why is it in hardware?
- [ ] How many cycles do different CORDIC operations take?
- [ ] What precision/range do CORDIC operations support?
- [ ] How do you pipeline CORDIC operations?
- [ ] What coordinate systems does QROTATE/QVECTOR use?

### Specialized Hardware Questions
- [ ] What is the Pixel Mixer and its use cases?
- [ ] How does the Color Space Converter work?
- [ ] What is the Streamer and how does it move data?
- [ ] How do these specialized units interact with COGs?
- [ ] What is XINIT/XSTOP/XCONT for?

### Interrupt System Questions
- [ ] How do interrupts work in a multi-COG system?
- [ ] What are INT1-3 interrupt sources?
- [ ] How do RESI/RETI differ from normal returns?
- [ ] What is the interrupt latency?
- [ ] How does interrupt shielding work?

### Timing Questions
- [ ] Why are most instructions 2 cycles?
- [ ] What determines hub access timing (9-16 cycles)?
- [ ] How does crossing hub longs affect timing?
- [ ] What is the relationship between cog and system clock?
- [ ] How deterministic is instruction timing?

### System Questions
- [ ] How does COGINIT start a new COG?
- [ ] What are hub locks (LOCKNEW, LOCKREL)?
- [ ] What is HUBSET configuring?
- [ ] How does debugging work (BRK, GETBRK)?
- [ ] What is the boot process for the P2?

---

## Part 3: Silicon Document Knowledge
*To be populated from PDF processing*

### Table of Contents Structure
*Will extract TOC first to organize information*

### Architecture Deep Dive
*Comprehensive understanding from silicon doc*

### Instruction Set Complete Reference
*Full instruction documentation with examples*

---

## Part 4: Synthesized Understanding

### P2 Architecture Model
*Complete mental model after both documents*

### Programming Patterns
*Best practices and common patterns*

### Resource Management
*How to effectively use COGs, hub, pins*

---

## Part 5: AI-Optimized Documentation Plan

### Structure for AI Consumption
- Hierarchical JSON schemas
- Relationship graphs
- Quick reference tables
- Example patterns

### User Documentation Style Notes
*To be extracted from existing docs*

---

## Processing Log

### 2025-08-14 - Spreadsheet Processing
- Started: 15:45 PST
- Completed: 16:10 PST
- Instructions found: 491 total (365 core + aliases)
- Categories identified: 14 major groups
- Questions generated: 60+ specific questions across 11 topics

### [Pending] - PDF Processing
- Will extract table of contents first
- Process by complete sections
- Answer questions systematically
- Build comprehensive P2 model

---

*This is a living document that will grow as we process the source materials*