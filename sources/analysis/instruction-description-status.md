# PASM2 Instruction Description Status Analysis
*What we have vs what we need for AI code generation*
*Date: 2025-08-15*

## 📊 CURRENT STATUS

### What We HAVE:
1. **Instruction Inventory**: All 491 instructions with encoding (from spreadsheet)
2. **Instruction Categories**: Grouped by function (from spreadsheet)
3. **Timing Information**: Basic 2-cycle timing for most (from silicon doc)
4. **Flag Effects**: WC/WZ behavior documented (from silicon doc)
5. **Architecture Context**: How instructions fit in P2 system (from silicon doc)

### What We DON'T HAVE:
- **Narrative Descriptions**: What each instruction actually DOES
- **Usage Examples**: How to use each instruction
- **Edge Cases**: Special behaviors or restrictions
- **Detailed Semantics**: Exact operational behavior

## 🔴 MISSING INSTRUCTION DESCRIPTIONS BY P2 SUBSYSTEM

### 1. COG Core Operations (Missing ~60 descriptions)
**Basic ALU & Logic:**
- MODCZ, MODC, MODZ - Modify C/Z flags (no description of HOW)
- SUMNC, SUMZ, SUMNZ - Sum with flag conditions (behavior unclear)
- INCMOD, DECMOD - Increment/decrement with modulo (limits?)
- MERGEB, SPLITB, MERGEW, SPLITW - Merge/split operations (format?)
- SEUSSF, SEUSSR - Scramble operations (algorithm?)

**Bit Manipulation:**
- TESTB, TESTBN - Test bit (what's the difference?)
- BITL, BITH, BITC, BITNC, BITZ, BITNZ - Bit operations (exact behavior?)
- BITRND, BITNOT - Random/NOT bit operations (which bit?)
- MUXC, MUXZ, MUXNC, MUXNZ - Mux operations (how do they work?)

### 2. Branch & Flow Control (Missing ~40 descriptions)
**Conditional Execution:**
- TJZ, TJNZ, TJF, TJNF, TJS, TJNS, TJV - Test and jump (what conditions?)
- DJZ, DJNZ, IJZ, IJNZ - Decrement/increment and jump (exact behavior?)
- SKIP, SKIPF, EXECF - Skip/execute patterns (how patterns work?)
- REP - Repeat instruction block (syntax? limitations?)

**Stack Operations:**
- PUSHA, PUSHB, POPA, POPB - Push/pop to stack A/B (where are stacks?)
- CALLA, CALLB, RETA, RETB - Call/return using stack A/B (differences?)

### 3. Hub Memory Operations (Missing ~20 descriptions)
**Block Transfers:**
- SETQ, SETQ2 - Setup block transfer (difference? limits?)
- RDLUT, WRLUT - LUT RAM access (addressing? timing?)
- WMLONG - Write masked long (how does masking work?)

**FIFO Operations:**
- RDFAST, WRFAST - Setup fast read/write (parameters?)
- FBLOCK - FIFO block operation (purpose?)
- GETPTR, RFVAR, RFVARS - FIFO pointer/variable ops (usage?)

### 4. Smart Pin Operations (Missing ~30 descriptions)
**Pin Configuration:**
- WRPIN - Write pin mode (32 modes, what are they?)
- WXPIN, WYPIN - Write X/Y parameters (what do X/Y mean per mode?)
- SETDACS - Set DACs (format? range?)

**Pin Testing:**
- TESTP, TESTPN - Test pin (difference?)
- TESTB_W, TESTBN_W - Test bit and write (how?)
- TESTP_AND, TESTP_OR, TESTP_XOR - Test with logic (usage?)

### 5. Event System (Missing ~50 descriptions)
**Event Setup:**
- SETSE1, SETSE2, SETSE3, SETSE4 - Set selectable events (what events?)
- SETPAT - Set pattern match (pattern format?)
- ADDCT1, ADDCT2, ADDCT3 - Add to counter/timers (usage?)

**Event Polling/Waiting:**
- POLLSE1-4, POLLPAT, POLLCT1-3 - Poll events (return values?)
- WAITSE1-4, WAITPAT, WAITCT1-3 - Wait for events (blocking?)
- POLLINT, WAITINT - Poll/wait interrupts (which interrupts?)

### 6. CORDIC Operations (Missing ~15 descriptions)
**Math Operations:**
- QMUL, QDIV, QFRAC, QSQRT - Queue operations (parameters?)
- QROTATE, QVECTOR - Rotation/vector ops (coordinate systems?)
- QLOG, QEXP - Logarithm/exponential (base? range?)
- GETQX, GETQY - Get results (when ready?)

### 7. Specialized Hardware (Missing ~40 descriptions)
**Pixel Mixer:**
- ADDPIX, MULPIX, BLNPIX, MIXPIX - Pixel operations (format?)
- SETPIV, SETPIX - Set pixel parameters (what parameters?)

**Color Space Converter:**
- SETCY, SETCI, SETCQ - Set color parameters (YIQ format?)
- SETCFRQ, SETCMOD - Set color frequency/mode (usage?)

**Streamer:**
- XINIT, XSTOP, XZERO, XCONT - Streamer control (modes?)
- SETXFRQ, GETXACC - Frequency/accumulator (format?)

**Goertzel:**
- GETNIB, GETBYTE, GETWORD - Get nibble/byte/word (from where?)
- SETNIB, SETBYTE, SETWORD - Set nibble/byte/word (to where?)

### 8. Register Alteration (Missing ~20 descriptions)
**ALT Instructions:**
- ALTR, ALTD, ALTS, ALTB, ALTI - Alter next instruction (how?)
- ALTSN, ALTGN, ALTSB, ALTGB - Alter nibble/byte ops (usage?)
- ALTSW, ALTGW - Alter word operations (purpose?)

### 9. System Control (Missing ~15 descriptions)
**COG Management:**
- COGINIT, COGSTOP, COGID, COGCHK - COG control (parameters?)
- LOCKNEW, LOCKRET, LOCKTRY, LOCKREL - Hub locks (16 locks, usage?)
- HUBSET - Configure hub (what settings?)

**Debug/Interrupt:**
- BRK, GETBRK, SETBRK - Breakpoint operations (debug support?)
- STALLI, ALLOWI - Interrupt enable/disable (scope?)
- RESI, RETI - Resume/return from interrupt (differences from RET?)

## 📈 INSTRUCTION DOCUMENTATION COVERAGE BY SUBSYSTEM

| P2 Subsystem | Total Instructions | Have Descriptions | Missing | Coverage |
|--------------|-------------------|-------------------|---------|----------|
| COG Core | ~115 | ~55 | ~60 | 48% |
| Branch/Flow | ~85 | ~45 | ~40 | 53% |
| Hub Memory | ~35 | ~15 | ~20 | 43% |
| Smart Pins | ~45 | ~15 | ~30 | 33% |
| Events | ~60 | ~10 | ~50 | 17% |
| CORDIC | ~15 | ~0 | ~15 | 0% |
| Specialized HW | ~60 | ~20 | ~40 | 33% |
| Register ALT | ~20 | ~0 | ~20 | 0% |
| System Control | ~20 | ~5 | ~15 | 25% |
| **TOTAL** | **~455** | **~165** | **~290** | **36%** |

## 🎯 PRIORITY FOR AI CODE GENERATION

### CRITICAL (Blocks basic code generation):
1. **Basic ALU/Logic** - Need to know what MODCZ, SUMNC, etc. do
2. **Branch/Flow** - Need jump conditions, repeat syntax
3. **Hub Memory** - Need SETQ/SETQ2 for block transfers
4. **COG Management** - Need COGINIT parameters

### IMPORTANT (Limits capability):
5. **Smart Pins** - Need mode descriptions for I/O
6. **Events** - Need event types and usage
7. **CORDIC** - Need parameter formats

### NICE TO HAVE (Advanced features):
8. **Specialized Hardware** - Pixel, color, streamer
9. **Register ALT** - Advanced instruction modification
10. **Debug/Interrupt** - Debugging support

## 📝 WHAT THIS MEANS

**Reality Check:**
- We have **instruction syntax** for 100% of instructions ✅
- We have **semantic descriptions** for only ~36% of instructions ⚠️
- The missing 64% blocks full AI code generation capability

**For v1.0 Release:**
- Can generate syntactically correct code ✅
- Can use the ~165 documented instructions ✅
- Cannot intelligently choose from all 491 instructions ❌
- Cannot generate optimal code patterns ❌

**What Screenshots Won't Solve:**
- PASM2 Manual only has ~100 instruction descriptions
- Silicon Doc doesn't have individual instruction details
- We genuinely need ~290 instruction descriptions

## ✅ RECOMMENDATION

### For Immediate v1.0:
1. **Ship with what we have** - 36% documented instructions
2. **Market as "Core PASM2"** - Focus on documented subset
3. **Clear documentation** of which instructions are fully supported

### For Complete Coverage:
1. **Ask Chip for one-sentence descriptions** of ~290 instructions
2. **Prioritize by subsystem** - Core ops first, specialized last
3. **Community crowd-source** - Let users document as they use

### The Truth:
**We DON'T have narrative descriptions for ~290 instructions.**
**This IS a real gap that screenshots won't fill.**
**We NEED either Chip's input or community documentation.**

---

*This analysis confirms we're missing critical instruction semantics*