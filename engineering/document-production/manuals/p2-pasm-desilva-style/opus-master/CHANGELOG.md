# DeSilva PASM2 Tutorial Manual - Changelog

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
