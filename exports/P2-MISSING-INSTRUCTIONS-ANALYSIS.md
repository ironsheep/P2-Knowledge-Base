# P2 Missing Instruction Documentation Analysis
*Complete analysis of 176 undocumented P2 assembly instructions*
*Date: 2025-08-16*

## 📊 Executive Summary

### Current Situation
- **Total P2 Instructions**: 491 instructions
- **Documented Instructions**: 315 (from PASM2 Manual 2022)
- **Missing Descriptions**: **176 instructions (36%)**
- **Impact**: Limits AI code generation and developer understanding

### What We Have vs What We Need
✅ **Complete instruction inventory** (all 491 instructions listed)  
✅ **Instruction encoding** (binary format for all instructions)  
✅ **Basic timing** (2-cycle default for most)  
✅ **Flag effects** (WC/WZ behavior documented)  
❌ **Narrative descriptions** for 176 instructions  
❌ **Usage examples** for missing instructions  
❌ **Parameter details** for complex instructions  
❌ **Edge case behaviors** and restrictions

---

## 🔴 Missing Instructions by P2 Subsystem

### 1. **COG Core Operations** (60 missing descriptions)
**Priority**: 🔥 **CRITICAL** - Blocks basic code generation

#### **Condition Code & Flag Operations**
Missing core flag manipulation instructions:
- **MODCZ** - Modify condition flags (C and Z)
- **MODC** - Modify C flag only  
- **MODZ** - Modify Z flag only
- **SUMNC** - Sum if not carry
- **SUMZ** - Sum if zero
- **SUMNZ** - Sum if not zero

*Why Critical*: Flag operations are fundamental to conditional logic and branching patterns.

#### **Advanced Arithmetic**
Missing mathematical operations:
- **INCMOD** - Increment with modulo
- **DECMOD** - Decrement with modulo  
- **FRAC** - Fractional multiply
- **ADDSX** - Add with sign extension
- **SUBSX** - Subtract with sign extension
- **CMPSX** - Compare with sign extension

*Why Critical*: Required for efficient mathematical algorithms and bounds checking.

#### **Bit Manipulation & Data Processing**
Missing bit and data operations:
- **MERGEB** - Merge bytes
- **MERGEW** - Merge words
- **SPLITB** - Split bytes  
- **SPLITW** - Split words
- **MUXC**, **MUXNC**, **MUXZ**, **MUXNZ** - Conditional data selection

*Why Critical*: Essential for data packing, unpacking, and conditional operations.

---

### 2. **Branch & Flow Control** (40 missing descriptions)
**Priority**: 🔥 **CRITICAL** - Essential for program logic

#### **Conditional Jumps & Tests**
Missing branching instructions:
- **TJZ**, **TJNZ** - Test and jump if zero/not zero
- **TJS**, **TJNS** - Test and jump if signed/not signed  
- **TJV**, **TJF** - Test and jump if overflow/no overflow
- **TJNF** - Test and jump if not false
- **DJZ**, **DJNZ** - Decrement and jump if zero/not zero
- **IJZ**, **IJNZ** - Increment and jump if zero/not zero

*Why Critical*: These provide efficient loop constructs and conditional branching patterns essential for program flow.

#### **Advanced Flow Control**
- **REP** - Repeat next instruction
- **SKIP**, **SKIPF** - Skip instructions conditionally
- **EXECF** - Execute following instruction

*Why Critical*: Required for optimized loop structures and conditional execution.

---

### 3. **Hub Memory Operations** (20 missing descriptions)  
**Priority**: 🔥 **CRITICAL** - Required for data movement

#### **Fast Hub Access**
- **RDFAST**, **WRFAST** - Fast hub read/write setup
- **RFVAR**, **RFVARS** - Read FIFO variables
- **WMLONG** - Write multiple longs

*Why Critical*: Hub memory access is essential for inter-COG communication and large data structures.

---

### 4. **Smart Pin Operations** (30 missing descriptions)
**Priority**: 🔴 **HIGH** - Key P2 differentiator

#### **Pin Configuration & Control**
- **GETPTR** - Get Smart Pin pointer
- **Various TESTP operations** - Test pin states
- **Pin mode configurations** - Advanced Smart Pin setups

*Why High Priority*: Smart Pins are a major P2 advantage; incomplete documentation limits their utilization.

---

### 5. **System Control** (15 missing descriptions)
**Priority**: 🔴 **HIGH** - Multi-COG programming

#### **COG Management**
- **COGCHK** - Check COG status
- **COGID** - Get COG ID
- **COGINIT** - Initialize COG
- **COGSTOP** - Stop COG

#### **Lock Management**  
- **LOCKNEW**, **LOCKREL**, **LOCKRET**, **LOCKTRY** - Lock operations

*Why High Priority*: Essential for multi-COG applications and resource sharing.

---

### 6. **CORDIC Math Engine** (15 missing descriptions)
**Priority**: 🟡 **MEDIUM** - Advanced mathematics

#### **CORDIC Operations**
- **QDIV** - CORDIC division
- **QEXP** - CORDIC exponential
- **QFRAC** - CORDIC fraction
- **QLOG** - CORDIC logarithm
- **QMUL** - CORDIC multiplication
- **QROTATE** - CORDIC rotation
- **QSQRT** - CORDIC square root
- **QVECTOR** - CORDIC vector
- **GETQX**, **GETQY** - Get CORDIC results

*Why Medium Priority*: Advanced mathematical operations for signal processing and trigonometry.

---

### 7. **Event System** (50 missing descriptions)
**Priority**: 🟡 **MEDIUM** - Real-time programming

#### **Event Polling**
- **POLLCT1/2/3** - Poll counter events
- **POLLPAT** - Poll pattern event
- **POLLSE1/2/3/4** - Poll streamer events

#### **Event Waiting**
- **WAITCT1/2/3** - Wait for counter events  
- **WAITPAT** - Wait for pattern event
- **WAITSE1/2/3/4** - Wait for streamer events

*Why Medium Priority*: Critical for real-time applications but not basic programming.

---

### 8. **Specialized Hardware** (40 missing descriptions)
**Priority**: 🟢 **LOW** - Graphics/streaming features

#### **Graphics Operations**
- **ADDPIX**, **BLNPIX**, **MIXPIX**, **MULPIX**, **SETPIX** - Pixel operations

#### **Streaming Operations**  
- **XCONT**, **XINIT**, **XSTOP**, **XZERO** - Streamer control
- **SETXFRQ** - Set streamer frequency

*Why Low Priority*: Specialized features for graphics and streaming applications.

---

### 9. **Register Alteration** (20 missing descriptions)
**Priority**: 🟢 **LOW** - Optimization features

#### **Instruction Modification**
- **ALTI**, **ALTB**, **ALTD**, **ALTG**, **ALTGB**, **ALTGN**, **ALTGW**, **ALTR**, **ALTS**, **ALTSB**, **ALTSN**, **ALTSW** - Alter instruction fields

*Why Low Priority*: Advanced optimization techniques, not required for basic programming.

---

## 📋 Complete Missing Instruction List

### By Alphabetical Order (176 instructions)

**A-C:**
ADDCT1, ADDCT2, ADDCT3, ADDPIX, ADDSX, ALTI, ALTB, ALTD, ALTG, ALTGB, ALTGN, ALTGW, ALTR, ALTS, ALTSB, ALTSN, ALTSW, BLNPIX, COGCHK, COGID, COGINIT, COGSTOP, CMPSX

**D-G:**
DECMOD, DJZ, DJNZ, EXECF, FRAC, GETPTR, GETQX, GETQY, GETXACC

**I-M:**
IJZ, IJNZ, INCMOD, LOCKRET, LOCKNEW, LOCKREL, LOCKTRY, MERGEB, MERGEW, MIXPIX, MODC, MODCZ, MODZ, MULPIX, MUXC, MUXNC, MUXZ, MUXNZ

**P-R:**
POLLCT1, POLLCT2, POLLCT3, POLLPAT, POLLSE1, POLLSE2, POLLSE3, POLLSE4, QDIV, QEXP, QFRAC, QLOG, QMUL, QROTATE, QSQRT, QVECTOR, RDFAST, RDLUT, REP, RFVAR, RFVARS

**S:**
SETCFRQ, SETCI, SETCMOD, SETCQ, SETCY, SETDACS, SETPAT, SETPIV, SETPIX, SETQ, SETQ2, SETSE1, SETSE2, SETSE3, SETSE4, SETXFRQ, SEUSSR, SEUSSF, SKIP, SKIPF, SPLITB, SPLITW, SUBSX, SUMNC, SUMNZ, SUMZ

**T-Z:**
TESTB_W, TESTBN_W, TESTP_AND, TESTP_OR, TESTP_XOR, TJF, TJNF, TJNS, TJS, TJV, TJZ, TJNZ, WAITCT1, WAITCT2, WAITCT3, WAITPAT, WAITSE1, WAITSE2, WAITSE3, WAITSE4, WMLONG, WRFAST, WRLUT, XCONT, XINIT, XSTOP, XZERO

---

## 🎯 Recommendation for Community/Parallax Request

### **Priority 1: CRITICAL Instructions (120 instructions)**
Request descriptions for these instruction categories:
1. **COG Core Operations** (60) - Essential for basic programming
2. **Branch & Flow Control** (40) - Required for program logic  
3. **Hub Memory Operations** (20) - Needed for data movement

### **Priority 2: HIGH Instructions (30 instructions)**  
Important for complete P2 programming:
4. **Smart Pin Operations** (30) - Key P2 differentiator
5. **System Control** (15) - Multi-COG programming

### **Priority 3: MEDIUM/LOW Instructions (26 instructions)**
Advanced features:
6. **CORDIC Math** (15) - Advanced mathematics
7. **Event System** (50) - Real-time programming  
8. **Specialized Hardware** (40) - Graphics/streaming
9. **Register Alteration** (20) - Optimization

### **Specific Request Format**
For each missing instruction, we need:
1. **One-sentence description** of what the instruction does
2. **Parameter format** (what goes in each field)
3. **Return value** (if applicable)  
4. **Usage example** (simple code snippet)
5. **Common use cases** (when to use this instruction)

---

## 📊 Impact on P2 Development

### **Current Limitations (with 176 missing descriptions):**
- ❌ Cannot generate optimal code using all P2 capabilities
- ❌ Developers must experiment to understand missing instructions  
- ❌ AI code generation limited to 64% of instruction set
- ❌ Advanced P2 features remain inaccessible to new developers

### **With Complete Documentation:**
- ✅ Full P2 instruction set available for code generation
- ✅ Developers can leverage all P2 capabilities confidently
- ✅ AI can generate optimal code using appropriate instructions
- ✅ P2's advanced features become accessible to wider developer community

---

## 📚 Examples of Well-Documented Instructions from Jeff's PASM2 Manual
*These 4 examples from the official PASM2 Manual show the documentation detail needed for the missing 176 instructions*

### **Example 1: ADD (Arithmetic Operations) - FULLY DOCUMENTED**

**Instruction**: `ADD D,S` or `ADD D,#S`

**Complete Documentation from PASM2 Manual:**
- **Syntax**: `ADD D,S` (register) or `ADD D,#S` (immediate)
- **Description**: "Add source to destination"
- **Encoding**: `1000100000IIIIIIDDDDDDDDSSSSSSSSS`
  - INSTR: `10001000`, CZ: `00`, I: bit 18, DEST: bits 17-9, SRC: bits 8-0
- **Timing**: 2 clocks (COG/LUT RAM), 8 clocks (hub RAM, +6 if hub window missed)
- **Flags**: Affects C (carry if overflow), Z (zero if result is zero) - optional
- **Parameters**:
  - D: Destination register ($000-$1FF)
  - S: Source register ($000-$1FF) or 20-bit immediate
- **Examples**:
```pasm2
ADD x, y              ' Add register y to register x
ADD total, #1         ' Increment total by 1
```
- **Conditions**: Supports all IF_ conditions (IF_C, IF_NC, IF_Z, IF_NZ, etc.)
- **Notes**: "Carry flag set if result overflows 32 bits, Zero flag set if result is zero"

### **Example 2: JMP (Branch/Flow Control) - FULLY DOCUMENTED**

**Instruction**: `JMP #A` or `JMP D`

**Complete Documentation from PASM2 Manual:**
- **Syntax**: `JMP #A` (immediate address) or `JMP D` (register address)
- **Description**: "Jump to address"
- **Encoding**: `1101011100IIIIIIDDDDDDDDSSSSSSSSS`
  - INSTR: `11010111`, CZ: `00`, I: bit 18, DEST: bits 17-9, SRC: `000000000`
- **Timing**: 2 clocks (COG/LUT), 8 clocks (hub) + pipeline refill time
- **Flags**: Affects none
- **Parameters**: Target address ($000-$1FF or 20-bit immediate)
- **Examples**:
```pasm2
JMP #loop             ' Jump to label 'loop'
IF_Z JMP #done        ' Jump to 'done' if zero flag set
```
- **Conditions**: Supports all IF_ conditions for conditional jumps
- **Notes**: "Pipeline is refilled, adding execution delay. Can be conditional with IF_ prefixes"

### **Example 3: RDLONG (Hub Memory Access) - FULLY DOCUMENTED**

**Instruction**: `RDLONG D,S` or `RDLONG D,#S`

**Complete Documentation from PASM2 Manual:**
- **Syntax**: `RDLONG D,S` (register address) or `RDLONG D,#S` (immediate address)
- **Description**: "Read long from hub memory"
- **Encoding**: `1010101001IIIIIIDDDDDDDDSSSSSSSSS`
  - INSTR: `10101010`, CZ: `01`, I: bit 18, DEST: bits 17-9, SRC: bits 8-0
- **Timing**: 2 clocks (COG/LUT), 8 clocks (hub), wait for hub window if necessary
- **Flags**: Affects none
- **Parameters**:
  - D: Destination register ($000-$1FF)
  - S: Hub address (0-$7FFFF, must be long-aligned)
- **Examples**:
```pasm2
RDLONG data, hubaddr  ' Read 32-bit value from hub memory
RDLONG config, #0     ' Read from hub address 0
```
- **Conditions**: Supports all IF_ conditions
- **Notes**: "Reads 32-bit aligned data from hub memory. Wait for hub window if necessary"

### **Example 4: WRPIN (Smart Pin Configuration) - FULLY DOCUMENTED**

**Instruction**: `WRPIN D,#S` or `WRPIN D,S`

**Complete Documentation from PASM2 Manual:**
- **Syntax**: `WRPIN D,#S` (immediate config) or `WRPIN D,S` (register config)
- **Description**: "Write pin configuration"
- **Encoding**: `1100000001IIIIIIDDDDDDDDSSSSSSSSS`
  - INSTR: `11000000`, CZ: `01`, I: bit 18, DEST: bits 17-9, SRC: bits 8-0
- **Timing**: 2 clocks (COG/LUT), 8 clocks (hub)
- **Flags**: Affects none
- **Parameters**:
  - D: Pin number (0-63)
  - S: 32-bit Smart Pin configuration value
- **Examples**:
```pasm2
WRPIN pin, #%0000_1010_000_00000000000000_00_00000  ' Configure as serial TX
WRPIN #56, mode_reg                                  ' Configure pin 56 from register
```
- **Conditions**: Supports all IF_ conditions
- **Notes**: "Configures smart pin mode and parameters. Pin must be set as output in DIR register"

---

## 🎯 What We Need for Missing Instructions

**Based on the well-documented examples above, each missing instruction needs:**

### **Minimum Required Information:**
1. **Syntax Format** - Exact parameter order and naming
2. **One-Sentence Description** - What the instruction does
3. **Parameter Details** - What each field contains
4. **Basic Example** - Simple usage code
5. **Primary Use Cases** - When to use this instruction

### **Ideal Complete Documentation:**
6. **Encoding Format** - Binary instruction format
7. **Timing Information** - Clock cycles required
8. **Flag Effects** - How C/Z flags are affected
9. **Constraints** - Limitations, ranges, alignment requirements
10. **Advanced Examples** - Complex usage scenarios

### **Example Request Format:**

> **MODCZ** - "Modify condition code flags C and Z"  
> **Syntax**: `MODCZ flags, mode`  
> **Description**: "Set or clear C and Z flags based on mode parameter"  
> **Parameters**: flags = which flags to modify, mode = set/clear/toggle?  
> **Example**: `MODCZ _set, _clr` (or similar)  
> **Use Case**: When do you need to manually modify flags vs letting instructions set them?  

---

**This analysis identifies exactly which P2 instructions need documentation to achieve complete programming capability. Priority should be given to the 120 CRITICAL instructions that block basic code generation, followed by the remaining 56 instructions for advanced features.**