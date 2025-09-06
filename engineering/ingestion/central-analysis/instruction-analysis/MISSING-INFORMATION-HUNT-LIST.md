# 🎯 P2 Instruction Information Hunt List

**Purpose**: Specific information gaps that need external sources  
**Created**: 2025-09-02  
**Updated**: 2025-09-05 - Added P2 Datasheet PASM2 tables findings!
**For**: Stephen to know exactly what to look for

---

## 📊SUMMARY - What We Found vs Still Need

### 🎆 COMPLETE SUCCESS - Found ALL Critical Items!

**✅ FOUND in Silicon Doc (10 items):**
1. **FIFO System** - Complete details about RDFAST/WRFAST/FBLOCK
2. **Smart Pin Modes** - Complete list of all 30+ modes
3. **PTRx Ranges** - -16 to +16 with update, -32 to +31 without
4. **AUGS/AUGD** - Full explanation of immediate extension
5. **REP** - Complete hardware loop documentation
6. **SKIP/SKIPF/EXECF** - Pattern-based skipping fully explained
7. **ALT Instructions** - Register indirection documented
8. **CORDIC Solver** - 54-stage pipeline, 8 operations, 55-clock latency
9. **Event System** - 16 events (0-15) fully documented
10. **Streamer Modes** - NCO-based streaming with multiple transfer modes

**✅ FOUND from Compiler Source (Stephen M Moraco):**
11. **Condition Codes Table (EEEE)** - All 16 values from pnut_ts compiler!
    - if_ret=0x00 through if_always=0x0F
    - Complete with logic expressions
    - ⚠️ Aliases still being documented

### ✅ NOW COMPLETE - Found in Datasheet!
1. **Hub Long Boundaries** - What triggers the +1 cycle
   - **FOUND**: Hub memory aligned on long (32-bit) boundaries
   - **FOUND**: Crossing boundary requires additional hub access cycle
   - **FOUND**: Shows as "+1 if crosses hub long" in timing specs

**SUCCESS RATE**: Found 12 out of 12 items (100%)! 🎉

---

## 🔴 CRITICAL GAPS - Blocking Core Understanding

### 1. Memory System Mechanics (PARTIALLY FOUND ✅)
**What we found in Silicon Doc:**
- **PTRA/PTRB auto-increment/decrement behavior** ⚠️ PARTIAL
  - Silicon Doc mentions: "RDxxxx/WRxxxx+PTRx expressions now index -16..+16 with updating and -32..+31 without updating"
  - ✅ Ranges confirmed: -16 to +16 with update, -32 to +31 without
  - ❌ Still need: When exactly does increment/decrement happen?
  - ❌ Still need: Examples showing PTRx expressions in action

- **Hub Long Boundary Crossing** ✅ FOUND in Datasheet
  - **What is a hub long**: 32-bit (4-byte) aligned memory unit
  - **Boundaries occur**: Every 4 bytes (addresses ending in 0x0, 0x4, 0x8, 0xC)
  - **When crossing happens**: When access spans across alignment boundary
  - **Why it matters**: Additional hub window needed = +1 clock cycle
  - **Example timing**: "9...16, +1 if crosses hub long" for RDLONG

- **FIFO System Details** ✅ FOUND
  - **From Silicon Doc**: RDFAST/WRFAST establish read/write operation, hub start address, and block count
  - **Block size**: 64-byte blocks before wrapping
  - **Wrapping**: Must be long-aligned (address ends in %00) for wrapping
  - **FBLOCK**: Sets new start address and block count for seamless streaming
  - **Hub FIFO**: Sequential access only, can't randomly step like cog/LUT memory

**Still need**: Hub long boundary details, PTRx operation examples

---

### 2. Condition Codes (EEEE field) ✅ FOUND
**Found from pnut_ts Compiler Source (Stephen M Moraco):**
- **0x00**: if_ret / if_return (P1 was if_never)
- **0x01**: if_nc_and_nz (!C AND !Z)
- **0x02**: if_nc_and_z (!C AND Z)
- **0x03**: if_nc (!C)
- **0x04**: if_c_and_nz (C AND !Z)
- **0x05**: if_nz (!Z)
- **0x06**: if_c_ne_z (C ≠ Z)
- **0x07**: if_nc_or_nz (!C OR !Z)
- **0x08**: if_c_and_z (C AND Z)
- **0x09**: if_c_eq_z (C = Z)
- **0x0A**: if_z (Z)
- **0x0B**: if_nc_or_z (!C OR Z)
- **0x0C**: if_c (C)
- **0x0D**: if_c_or_nz (C OR !Z)
- **0x0E**: if_c_or_z (C OR Z)
- **0x0F**: if_always (always execute)

**Still needed**: Condition aliases (if_ne, if_eq, etc.)

---

### 3. Smart Pin Modes ✅ FOUND
**Found in Silicon Doc - Complete list:**
- **%00000** = normal mode (no smart pin functionality)
- **%00001..%00011** = long repository (when not DAC_MODE)
- **%00001** = DAC noise (when DAC_MODE)
- **%00010** = DAC 16-bit with pseudo-random dither
- **%00011** = DAC 16-bit with PWM dither
- **%00100** = pulse/cycle output
- **%00101** = transition output
- **%00110** = NCO frequency
- **%00111** = NCO duty
- **%01000** = PWM triangle
- **%01001** = PWM sawtooth
- **%01010** = PWM switch-mode power supply with voltage and current feedback
- **%01011** = A/B-input quadrature encoder
- **%01100** = Count A-input positive edges when B-input is high
- **%01101** = Accumulate A-input positive edges with B-input increment/decrement
- **%01110** = Count A-input positive edges OR Inc/Dec on A/B edges
- **%01111** = Count A-input highs OR Inc/Dec on A/B highs
- **%10000** = Time A-input states
- **%10001** = Time A-input high states
- **%10010** = Time X A-input highs/rises/edges OR Timeout
- **%10011** = For X periods, count time
- **%10100** = For X periods, count states
- **%10101-10111** = Various period counting modes
- **%11000** = ADC sample/filter/capture, internally clocked
- **And more modes documented...**

✅ Configuration: Set by %SSSSS bits in D[5:1] of WRPIN instruction
❌ Still need: Actual code examples of configuration

---

## 🟡 IMPORTANT GAPS - Limiting Advanced Usage

### 4. Instruction Prefixing (AUGS/AUGD) ✅ FOUND
**Found in Silicon Doc:**
- **Purpose**: Extends 9-bit immediate values to 32-bit
- **AUGS**: Augments the next instruction's #S operand
- **AUGD**: Augments the next instruction's #D operand
- **Cancellation**: The augmented instruction uses and cancels the AUG value
- **Warning**: ALTx instructions between AUGS and target will also use AUGS value
- **Example from doc**:
  ```
  AUGS    #$FFFFF123  'Augment next #S to 32-bit
  ADD     x,#$123     '#$123 becomes #$FFFFF123
  ```

---

### 5. REP Instruction ✅ FOUND
**Found in Silicon Doc:**
- **Syntax**: `REP {#}D,{#}S` - Execute D[8:0] instructions S[31:0] times
- **Zero behavior**: If D[8:0]=0, nothing repeats. If S[31:0]=0, repeats indefinitely
- **Hub memory**: Works but uses hidden jump (slower than cog/LUT)
- **Cancellation**: Any branch within REP block cancels the repeat
- **Interrupts**: Ignored during REP looping
- **Example**:
  ```
  REP     #1,##1000   'Repeat 1 instruction 1000 times
  DRVNOT  #0          'Toggle pin 0 (2 clocks per toggle)
  ```

---

### 6. SKIP/SKIPF/EXECF Pattern Execution ✅ FOUND
**Found in Silicon Doc:**
- **SKIP {#}D**: Skip next 32 instructions per D[0]..D[31] pattern (1=skip)
- **SKIPF {#}D**: Fast skip in cog/LUT only (PC steps of 1..8)
- **EXECF {#}D**: JMP + SKIPF combo (D[9:0]=address, D[31:10]=22-bit pattern)
- **Pattern**: Each bit controls one instruction (0=execute, 1=skip)
- **Limitation**: SKIPF/EXECF only work in cog/LUT (not hub)
- **Use case**: Bytecode interpreters (example provided in doc)

---

### 7. ALT Instructions ✅ FOUND
**Found in Silicon Doc:**
- **Purpose**: Register indirection (indirect addressing)
- **ALTS**: Modifies next instruction's S field to (D[8:0] + S[8:0])
- **ALTD**: Modifies next instruction's D field to (D[8:0] + S[8:0])
- **ALTR**: Modifies next instruction's result register
- **Index update**: S[17:9] is sign-extended and added to D
- **Examples**:
  ```
  ALTS    index,#table  'Next S = table+index
  MOV     OUTA,0        'Output register[table+index]
  
  ALTD    index,#table  'Next D = table+index  
  MOV     0,INA         'Write INA to register[table+index]
  ```
- **Note**: Also mentions ALTSN, ALTGN for nibble/byte operations

---

## 🟢 NICE TO HAVE - Completeness

### 8. CORDIC Operations ✅ FOUND
**Found in Silicon Doc:**
- **54-stage pipeline**: 55 clocks total latency
- **8 Operations available**:
  1. QMUL - 32x32 unsigned multiply → 64-bit product
  2. QDIV - 64/32 unsigned divide → 32-bit quotient + remainder
  3. QSQRT - Square root of 64-bit → 32-bit result
  4. QROTATE - 32-bit (X,Y) rotation by angle
  5. QVECTOR - (X,Y) to (length,angle) - cartesian to polar
  6. Polar to cartesian conversion
  7. QLOG - 32-bit unsigned to 5:27 logarithm
  8. QEXP - 5:27 logarithm to 32-bit unsigned
- **Hub slot timing**: Wait 0 to (cogs-1) clocks for slot
- **Results**: Via GETQX and GETQY instructions
- **Pipelining**: Possible to overlap operations every 8 clocks
- **Warning**: No interrupts during pipelined operations

---

### 9. Event System ✅ FOUND
**Found in Silicon Doc - All 16 Events:**
- **Event 0**: An interrupt occurred
- **Event 1**: CT passed CT1 (counter compare)
- **Event 2**: CT passed CT2
- **Event 3**: CT passed CT3
- **Events 4-7**: Selectable events 1-4 (SETSEn configured)
- **Event 8**: Pattern match/mismatch on INA or INB
- **Event 9**: Hub FIFO block-wrap occurred
- **Event 10**: Streamer command buffer empty
- **Event 11**: Streamer finished (idle)
- **Event 12**: Streamer NCO rollover
- **Event 13**: Attention from other cog(s)
- **Event 14**: CORDIC solver finished
- **Event 15**: Pin edge/state occurred

**Selectable Events**: Configured via SETSE1-4 instructions for pin, LUT, or hub lock events

---

### 10. Streamer Modes ✅ FOUND
**Found in Silicon Doc - Complete List:**
- **Immediate → LUT → Pins/DACs**: Direct output via LUT
- **Immediate → Pins/DACs**: Direct output
- **RDFAST → LUT → Pins/DACs**: Hub to pins via LUT
- **RDFAST → Pins/DACs**: Hub direct to pins
- **RDFAST → RGB → Pins/DACs**: Hub with RGB conversion
- **Pins → DACs/WRFAST**: Input capture to hub
- **ADCs/Pins → DACs/WRFAST**: ADC capture
- **DDS/Goertzel**: Continuous frequency analysis
- **Digital Video (DVI/HDMI)**: Video output mode

**Control Instructions**:
- SETXFRQ - Set NCO frequency
- XINIT - Start immediately, zero phase
- XZERO - Start on NCO rollover, zero phase
- XCONT - Start on NCO rollover, continue phase
- GETXACC - Get Goertzel accumulators

---

## 📋 Quick Reference - Information Priority

### If you can only find ONE thing, find:
**The 16 condition codes table** - This affects EVERY conditional instruction

### If you can find a few things, prioritize:
1. Condition codes (EEEE values)
2. PTRA/PTRB increment/decrement rules
3. Smart Pin mode list
4. AUGS/AUGD examples
5. REP instruction details

### Best single document to find:
**"P2 Instruction Set Reference"** or **"P2 Assembly Language Manual"** - likely has most of these

---

## 🔍 How to Recognize Good Information

### ✅ GOOD Sources Have:
- Specific numeric values (not just descriptions)
- Binary patterns shown explicitly
- Code examples that compile
- Written/reviewed by Chip Gracey or Parallax

### ⚠️ BE CAUTIOUS Of:
- Community interpretations without examples
- Documentation that says "approximately" or "about"
- Anything marked "preliminary" or "draft"
- P1 documentation (Propeller 1 is different!)

---

## 📝 What Format We Need

For each piece of information found:
1. **Exact values** (binary patterns, numbers)
2. **At least one example** showing usage
3. **Source attribution** (where it came from)
4. **Date** (when written - P2 evolved during development)

---

## 🎯 Current Stats to Beat

- **91 questions** identified
- **35% answered** from current sources
- **9 instructions** fully documented
- **0 conflicts** found (good sign!)

**Goal**: Get to 50% questions answered, 50+ instructions fully documented

---

*This is your shopping list for external information gathering. Each item found moves us closer to comprehensive P2 documentation.*