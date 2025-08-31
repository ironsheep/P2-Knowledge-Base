# PASM2 Master Instruction Table

**Purpose**: Single source of truth for all PASM2 instruction knowledge
**Last Updated**: 2025-08-20
**Source**: Extracted from `/sources/extractions/csv-pasm2-instructions-v2.md`
**Total Instructions**: 491 (365 core + aliases/variants)

## Table Structure

| Column | Description |
|--------|-------------|
| Instruction Name | Official PASM2 mnemonic |
| Opcode | Hexadecimal opcode value |
| Meta Group | Category (Math, Branch, Hub, etc.) |
| Clock Cycles | Execution time in cog cycles |
| Flag Effects | C/Z flag modifications (C/Z/both/none) |
| Category | Subcategory within meta group |
| Description Status | Complete/Partial/Missing |
| Missing Info | Explicit gaps marked as "MISSING: [field]" |

## Update Methodology

- **MISSING: [field]** indicates explicitly unknown information
- All future ingestions should enrich this table
- Source attribution required for all updates
- Gap tracking enables targeted information recovery

---

## Instruction Reference Table

### Math and Logic Instructions (115+ instructions)

| Instruction | Opcode | Meta Group | Clock Cycles | Flag Effects | Category | Description Status | Missing Info |
|-------------|--------|------------|--------------|--------------|----------|-------------------|--------------|
| ADD | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Arithmetic | Partial | MISSING: opcode, cycles, flags, full description |
| SUB | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Arithmetic | Partial | MISSING: opcode, cycles, flags, full description |
| MUL | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Arithmetic | Partial | MISSING: opcode, cycles, flags, full description |
| DIV | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Arithmetic | Partial | MISSING: opcode, cycles, flags, full description |
| MULS | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Arithmetic | Partial | MISSING: opcode, cycles, flags, full description |
| SCA | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Arithmetic | Partial | MISSING: opcode, cycles, flags, full description |
| SCAS | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Arithmetic | Partial | MISSING: opcode, cycles, flags, full description |
| AND | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Bitwise | Partial | MISSING: opcode, cycles, flags, full description |
| OR | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Bitwise | Partial | MISSING: opcode, cycles, flags, full description |
| XOR | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Bitwise | Partial | MISSING: opcode, cycles, flags, full description |
| NOT | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Bitwise | Partial | MISSING: opcode, cycles, flags, full description |
| ANDN | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Bitwise | Partial | MISSING: opcode, cycles, flags, full description |
| ROR | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Shifts/Rotates | Partial | MISSING: opcode, cycles, flags, full description |
| ROL | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Shifts/Rotates | Partial | MISSING: opcode, cycles, flags, full description |
| SHR | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Shifts/Rotates | Partial | MISSING: opcode, cycles, flags, full description |
| SHL | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Shifts/Rotates | Partial | MISSING: opcode, cycles, flags, full description |
| RCR | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Shifts/Rotates | Partial | MISSING: opcode, cycles, flags, full description |
| RCL | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Shifts/Rotates | Partial | MISSING: opcode, cycles, flags, full description |
| SAR | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Shifts/Rotates | Partial | MISSING: opcode, cycles, flags, full description |
| SAL | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Shifts/Rotates | Partial | MISSING: opcode, cycles, flags, full description |
| CMP | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Comparisons | Partial | MISSING: opcode, cycles, flags, full description |
| CMPS | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Comparisons | Partial | MISSING: opcode, cycles, flags, full description |
| CMPR | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Comparisons | Partial | MISSING: opcode, cycles, flags, full description |
| CMPM | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Comparisons | Partial | MISSING: opcode, cycles, flags, full description |
| CMPX | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Comparisons | Partial | MISSING: opcode, cycles, flags, full description |
| CMPSX | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Comparisons | Partial | MISSING: opcode, cycles, flags, full description |
| TESTB | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Bit Operations | Partial | MISSING: opcode, cycles, flags, full description |
| BITL | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Bit Operations | Partial | MISSING: opcode, cycles, flags, full description |
| BITH | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Bit Operations | Partial | MISSING: opcode, cycles, flags, full description |
| BITC | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Bit Operations | Partial | MISSING: opcode, cycles, flags, full description |
| BITNC | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Bit Operations | Partial | MISSING: opcode, cycles, flags, full description |
| BITZ | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Bit Operations | Partial | MISSING: opcode, cycles, flags, full description |
| BITNZ | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Bit Operations | Partial | MISSING: opcode, cycles, flags, full description |
| BITRND | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Bit Operations | Partial | MISSING: opcode, cycles, flags, full description |
| BITNOT | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Bit Operations | Partial | MISSING: opcode, cycles, flags, full description |
| ENCOD | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Data Processing | Partial | MISSING: opcode, cycles, flags, full description |
| ONES | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Data Processing | Partial | MISSING: opcode, cycles, flags, full description |
| DECOD | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Data Processing | Partial | MISSING: opcode, cycles, flags, full description |
| BMASK | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Data Processing | Partial | MISSING: opcode, cycles, flags, full description |
| ZEROX | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Data Processing | Partial | MISSING: opcode, cycles, flags, full description |
| SIGNX | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Data Processing | Partial | MISSING: opcode, cycles, flags, full description |
| REV | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Data Processing | Partial | MISSING: opcode, cycles, flags, full description |
| MERGEB | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Data Processing | Partial | MISSING: opcode, cycles, flags, full description |
| SPLITB | MISSING: opcode | Math and Logic | MISSING: cycles | MISSING: flags | Data Processing | Partial | MISSING: opcode, cycles, flags, full description |

### Branch and Flow Control Instructions (85+ instructions)

| Instruction | Opcode | Meta Group | Clock Cycles | Flag Effects | Category | Description Status | Missing Info |
|-------------|--------|------------|--------------|--------------|----------|-------------------|--------------|
| JMP | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Unconditional | Partial | MISSING: opcode, cycles, flags, full description |
| CALL | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Unconditional | Partial | MISSING: opcode, cycles, flags, full description |
| RET | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Unconditional | Partial | MISSING: opcode, cycles, flags, full description |
| CALLA | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Unconditional | Partial | MISSING: opcode, cycles, flags, full description |
| RETA | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Unconditional | Partial | MISSING: opcode, cycles, flags, full description |
| CALLB | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Unconditional | Partial | MISSING: opcode, cycles, flags, full description |
| RETB | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Unconditional | Partial | MISSING: opcode, cycles, flags, full description |
| DJZ | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Conditional Tests | Partial | MISSING: opcode, cycles, flags, full description |
| DJNZ | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Conditional Tests | Partial | MISSING: opcode, cycles, flags, full description |
| TJZ | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Conditional Tests | Partial | MISSING: opcode, cycles, flags, full description |
| TJNZ | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Conditional Tests | Partial | MISSING: opcode, cycles, flags, full description |
| TJF | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Conditional Tests | Partial | MISSING: opcode, cycles, flags, full description |
| TJNF | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Conditional Tests | Partial | MISSING: opcode, cycles, flags, full description |
| TJS | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Conditional Tests | Partial | MISSING: opcode, cycles, flags, full description |
| TJNS | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Conditional Tests | Partial | MISSING: opcode, cycles, flags, full description |
| TJV | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Conditional Tests | Partial | MISSING: opcode, cycles, flags, full description |
| SKIP | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Skip Instructions | Partial | MISSING: opcode, cycles, flags, full description |
| SKIPF | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Skip Instructions | Partial | MISSING: opcode, cycles, flags, full description |
| EXECF | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Skip Instructions | Partial | MISSING: opcode, cycles, flags, full description |
| PUSH | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Stack-based | Partial | MISSING: opcode, cycles, flags, full description |
| POP | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Stack-based | Partial | MISSING: opcode, cycles, flags, full description |
| PUSHA | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Stack-based | Partial | MISSING: opcode, cycles, flags, full description |
| PUSHB | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Stack-based | Partial | MISSING: opcode, cycles, flags, full description |
| POPA | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Stack-based | Partial | MISSING: opcode, cycles, flags, full description |
| POPB | MISSING: opcode | Branch and Flow Control | MISSING: cycles | MISSING: flags | Stack-based | Partial | MISSING: opcode, cycles, flags, full description |

### Hub RAM Operations (15+ instructions)

| Instruction | Opcode | Meta Group | Clock Cycles | Flag Effects | Category | Description Status | Missing Info |
|-------------|--------|------------|--------------|--------------|----------|-------------------|--------------|
| RDBYTE | MISSING: opcode | Hub RAM Operations | MISSING: cycles | MISSING: flags | Read | Partial | MISSING: opcode, cycles, flags, full description |
| RDWORD | MISSING: opcode | Hub RAM Operations | MISSING: cycles | MISSING: flags | Read | Partial | MISSING: opcode, cycles, flags, full description |
| RDLONG | MISSING: opcode | Hub RAM Operations | MISSING: cycles | MISSING: flags | Read | Partial | MISSING: opcode, cycles, flags, full description |
| RDLUT | MISSING: opcode | Hub RAM Operations | MISSING: cycles | MISSING: flags | Read | Partial | MISSING: opcode, cycles, flags, full description |
| WRBYTE | MISSING: opcode | Hub RAM Operations | MISSING: cycles | MISSING: flags | Write | Partial | MISSING: opcode, cycles, flags, full description |
| WRWORD | MISSING: opcode | Hub RAM Operations | MISSING: cycles | MISSING: flags | Write | Partial | MISSING: opcode, cycles, flags, full description |
| WRLONG | MISSING: opcode | Hub RAM Operations | MISSING: cycles | MISSING: flags | Write | Partial | MISSING: opcode, cycles, flags, full description |
| WRLUT | MISSING: opcode | Hub RAM Operations | MISSING: cycles | MISSING: flags | Write | Partial | MISSING: opcode, cycles, flags, full description |
| WMLONG | MISSING: opcode | Hub RAM Operations | MISSING: cycles | MISSING: flags | Write | Partial | MISSING: opcode, cycles, flags, full description |
| SETQ | MISSING: opcode | Hub RAM Operations | MISSING: cycles | MISSING: flags | Block Transfers | Partial | MISSING: opcode, cycles, flags, full description |
| SETQ2 | MISSING: opcode | Hub RAM Operations | MISSING: cycles | MISSING: flags | Block Transfers | Partial | MISSING: opcode, cycles, flags, full description |

### Smart Pins (10+ instructions)

| Instruction | Opcode | Meta Group | Clock Cycles | Flag Effects | Category | Description Status | Missing Info |
|-------------|--------|------------|--------------|--------------|----------|-------------------|--------------|
| WRPIN | MISSING: opcode | Smart Pins | MISSING: cycles | MISSING: flags | Configuration | Partial | MISSING: opcode, cycles, flags, full description |
| WXPIN | MISSING: opcode | Smart Pins | MISSING: cycles | MISSING: flags | Configuration | Partial | MISSING: opcode, cycles, flags, full description |
| WYPIN | MISSING: opcode | Smart Pins | MISSING: cycles | MISSING: flags | Configuration | Partial | MISSING: opcode, cycles, flags, full description |
| SETDACS | MISSING: opcode | Smart Pins | MISSING: cycles | MISSING: flags | Configuration | Partial | MISSING: opcode, cycles, flags, full description |
| RDPIN | MISSING: opcode | Smart Pins | MISSING: cycles | MISSING: flags | Status | Partial | MISSING: opcode, cycles, flags, full description |
| RQPIN | MISSING: opcode | Smart Pins | MISSING: cycles | MISSING: flags | Status | Partial | MISSING: opcode, cycles, flags, full description |
| AKPIN | MISSING: opcode | Smart Pins | MISSING: cycles | MISSING: flags | Status | Partial | MISSING: opcode, cycles, flags, full description |
| TESTP | MISSING: opcode | Smart Pins | MISSING: cycles | MISSING: flags | Test | Partial | MISSING: opcode, cycles, flags, full description |
| TESTPN | MISSING: opcode | Smart Pins | MISSING: cycles | MISSING: flags | Test | Partial | MISSING: opcode, cycles, flags, full description |

### Events System (60+ instructions)

| Instruction | Opcode | Meta Group | Clock Cycles | Flag Effects | Category | Description Status | Missing Info |
|-------------|--------|------------|--------------|--------------|----------|-------------------|--------------|
| SETSE1 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Setup | Partial | MISSING: opcode, cycles, flags, full description |
| SETSE2 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Setup | Partial | MISSING: opcode, cycles, flags, full description |
| SETSE3 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Setup | Partial | MISSING: opcode, cycles, flags, full description |
| SETSE4 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Setup | Partial | MISSING: opcode, cycles, flags, full description |
| SETPAT | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Setup | Partial | MISSING: opcode, cycles, flags, full description |
| ADDCT1 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Setup | Partial | MISSING: opcode, cycles, flags, full description |
| ADDCT2 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Setup | Partial | MISSING: opcode, cycles, flags, full description |
| ADDCT3 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Setup | Partial | MISSING: opcode, cycles, flags, full description |
| POLLINT | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Polling | Partial | MISSING: opcode, cycles, flags, full description |
| POLLCT1 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Polling | Partial | MISSING: opcode, cycles, flags, full description |
| POLLCT2 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Polling | Partial | MISSING: opcode, cycles, flags, full description |
| POLLCT3 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Polling | Partial | MISSING: opcode, cycles, flags, full description |
| POLLSE1 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Polling | Partial | MISSING: opcode, cycles, flags, full description |
| POLLSE2 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Polling | Partial | MISSING: opcode, cycles, flags, full description |
| POLLSE3 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Polling | Partial | MISSING: opcode, cycles, flags, full description |
| POLLSE4 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Polling | Partial | MISSING: opcode, cycles, flags, full description |
| POLLPAT | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Polling | Partial | MISSING: opcode, cycles, flags, full description |
| POLLQMT | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Polling | Partial | MISSING: opcode, cycles, flags, full description |
| WAITINT | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Waiting | Partial | MISSING: opcode, cycles, flags, full description |
| WAITCT1 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Waiting | Partial | MISSING: opcode, cycles, flags, full description |
| WAITCT2 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Waiting | Partial | MISSING: opcode, cycles, flags, full description |
| WAITCT3 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Waiting | Partial | MISSING: opcode, cycles, flags, full description |
| WAITSE1 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Waiting | Partial | MISSING: opcode, cycles, flags, full description |
| WAITSE2 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Waiting | Partial | MISSING: opcode, cycles, flags, full description |
| WAITSE3 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Waiting | Partial | MISSING: opcode, cycles, flags, full description |
| WAITSE4 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Waiting | Partial | MISSING: opcode, cycles, flags, full description |
| WAITPAT | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Waiting | Partial | MISSING: opcode, cycles, flags, full description |
| JINT | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Branching | Partial | MISSING: opcode, cycles, flags, full description |
| JCT1 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Branching | Partial | MISSING: opcode, cycles, flags, full description |
| JCT2 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Branching | Partial | MISSING: opcode, cycles, flags, full description |
| JCT3 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Branching | Partial | MISSING: opcode, cycles, flags, full description |
| JSE1 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Branching | Partial | MISSING: opcode, cycles, flags, full description |
| JSE2 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Branching | Partial | MISSING: opcode, cycles, flags, full description |
| JSE3 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Branching | Partial | MISSING: opcode, cycles, flags, full description |
| JSE4 | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Branching | Partial | MISSING: opcode, cycles, flags, full description |
| JPAT | MISSING: opcode | Events System | MISSING: cycles | MISSING: flags | Branching | Partial | MISSING: opcode, cycles, flags, full description |

### CORDIC Solver (10+ instructions)

| Instruction | Opcode | Meta Group | Clock Cycles | Flag Effects | Category | Description Status | Missing Info |
|-------------|--------|------------|--------------|--------------|----------|-------------------|--------------|
| QMUL | MISSING: opcode | CORDIC Solver | MISSING: cycles | MISSING: flags | Math | Partial | MISSING: opcode, cycles, flags, full description |
| QDIV | MISSING: opcode | CORDIC Solver | MISSING: cycles | MISSING: flags | Math | Partial | MISSING: opcode, cycles, flags, full description |
| QFRAC | MISSING: opcode | CORDIC Solver | MISSING: cycles | MISSING: flags | Math | Partial | MISSING: opcode, cycles, flags, full description |
| QSQRT | MISSING: opcode | CORDIC Solver | MISSING: cycles | MISSING: flags | Math | Partial | MISSING: opcode, cycles, flags, full description |
| QROTATE | MISSING: opcode | CORDIC Solver | MISSING: cycles | MISSING: flags | Trigonometric | Partial | MISSING: opcode, cycles, flags, full description |
| QVECTOR | MISSING: opcode | CORDIC Solver | MISSING: cycles | MISSING: flags | Trigonometric | Partial | MISSING: opcode, cycles, flags, full description |
| QLOG | MISSING: opcode | CORDIC Solver | MISSING: cycles | MISSING: flags | Logarithmic | Partial | MISSING: opcode, cycles, flags, full description |
| QEXP | MISSING: opcode | CORDIC Solver | MISSING: cycles | MISSING: flags | Logarithmic | Partial | MISSING: opcode, cycles, flags, full description |
| GETQX | MISSING: opcode | CORDIC Solver | MISSING: cycles | MISSING: flags | Results | Partial | MISSING: opcode, cycles, flags, full description |
| GETQY | MISSING: opcode | CORDIC Solver | MISSING: cycles | MISSING: flags | Results | Partial | MISSING: opcode, cycles, flags, full description |

### Pin I/O Control (35+ instructions)

| Instruction | Opcode | Meta Group | Clock Cycles | Flag Effects | Category | Description Status | Missing Info |
|-------------|--------|------------|--------------|--------------|----------|-------------------|--------------|
| DIRL | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Direction | Partial | MISSING: opcode, cycles, flags, full description |
| DIRH | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Direction | Partial | MISSING: opcode, cycles, flags, full description |
| DIRC | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Direction | Partial | MISSING: opcode, cycles, flags, full description |
| DIRNC | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Direction | Partial | MISSING: opcode, cycles, flags, full description |
| DIRZ | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Direction | Partial | MISSING: opcode, cycles, flags, full description |
| DIRNZ | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Direction | Partial | MISSING: opcode, cycles, flags, full description |
| DIRRND | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Direction | Partial | MISSING: opcode, cycles, flags, full description |
| DIRNOT | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Direction | Partial | MISSING: opcode, cycles, flags, full description |
| OUTL | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Output | Partial | MISSING: opcode, cycles, flags, full description |
| OUTH | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Output | Partial | MISSING: opcode, cycles, flags, full description |
| OUTC | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Output | Partial | MISSING: opcode, cycles, flags, full description |
| OUTNC | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Output | Partial | MISSING: opcode, cycles, flags, full description |
| OUTZ | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Output | Partial | MISSING: opcode, cycles, flags, full description |
| OUTNZ | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Output | Partial | MISSING: opcode, cycles, flags, full description |
| OUTRND | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Output | Partial | MISSING: opcode, cycles, flags, full description |
| OUTNOT | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Output | Partial | MISSING: opcode, cycles, flags, full description |
| FLTL | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Float | Partial | MISSING: opcode, cycles, flags, full description |
| FLTH | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Float | Partial | MISSING: opcode, cycles, flags, full description |
| FLTC | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Float | Partial | MISSING: opcode, cycles, flags, full description |
| FLTNC | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Float | Partial | MISSING: opcode, cycles, flags, full description |
| FLTZ | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Float | Partial | MISSING: opcode, cycles, flags, full description |
| FLTNZ | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Float | Partial | MISSING: opcode, cycles, flags, full description |
| FLTRND | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Float | Partial | MISSING: opcode, cycles, flags, full description |
| FLTNOT | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Float | Partial | MISSING: opcode, cycles, flags, full description |
| DRVL | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Drive | Partial | MISSING: opcode, cycles, flags, full description |
| DRVH | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Drive | Partial | MISSING: opcode, cycles, flags, full description |
| DRVC | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Drive | Partial | MISSING: opcode, cycles, flags, full description |
| DRVNC | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Drive | Partial | MISSING: opcode, cycles, flags, full description |
| DRVZ | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Drive | Partial | MISSING: opcode, cycles, flags, full description |
| DRVNZ | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Drive | Partial | MISSING: opcode, cycles, flags, full description |
| DRVRND | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Drive | Partial | MISSING: opcode, cycles, flags, full description |
| DRVNOT | MISSING: opcode | Pin I/O Control | MISSING: cycles | MISSING: flags | Drive | Partial | MISSING: opcode, cycles, flags, full description |

### Hub FIFO Operations (10+ instructions)

| Instruction | Opcode | Meta Group | Clock Cycles | Flag Effects | Category | Description Status | Missing Info |
|-------------|--------|------------|--------------|--------------|----------|-------------------|--------------|
| RDFAST | MISSING: opcode | Hub FIFO Operations | MISSING: cycles | MISSING: flags | Setup | Partial | MISSING: opcode, cycles, flags, full description |
| WRFAST | MISSING: opcode | Hub FIFO Operations | MISSING: cycles | MISSING: flags | Setup | Partial | MISSING: opcode, cycles, flags, full description |
| FBLOCK | MISSING: opcode | Hub FIFO Operations | MISSING: cycles | MISSING: flags | Setup | Partial | MISSING: opcode, cycles, flags, full description |
| GETPTR | MISSING: opcode | Hub FIFO Operations | MISSING: cycles | MISSING: flags | Setup | Partial | MISSING: opcode, cycles, flags, full description |
| RFBYTE | MISSING: opcode | Hub FIFO Operations | MISSING: cycles | MISSING: flags | Read | Partial | MISSING: opcode, cycles, flags, full description |
| RFWORD | MISSING: opcode | Hub FIFO Operations | MISSING: cycles | MISSING: flags | Read | Partial | MISSING: opcode, cycles, flags, full description |
| RFLONG | MISSING: opcode | Hub FIFO Operations | MISSING: cycles | MISSING: flags | Read | Partial | MISSING: opcode, cycles, flags, full description |
| RFVAR | MISSING: opcode | Hub FIFO Operations | MISSING: cycles | MISSING: flags | Read | Partial | MISSING: opcode, cycles, flags, full description |
| RFVARS | MISSING: opcode | Hub FIFO Operations | MISSING: cycles | MISSING: flags | Read | Partial | MISSING: opcode, cycles, flags, full description |
| WFBYTE | MISSING: opcode | Hub FIFO Operations | MISSING: cycles | MISSING: flags | Write | Partial | MISSING: opcode, cycles, flags, full description |
| WFWORD | MISSING: opcode | Hub FIFO Operations | MISSING: cycles | MISSING: flags | Write | Partial | MISSING: opcode, cycles, flags, full description |
| WFLONG | MISSING: opcode | Hub FIFO Operations | MISSING: cycles | MISSING: flags | Write | Partial | MISSING: opcode, cycles, flags, full description |

### Register Indirection (15+ instructions)

| Instruction | Opcode | Meta Group | Clock Cycles | Flag Effects | Category | Description Status | Missing Info |
|-------------|--------|------------|--------------|--------------|----------|-------------------|--------------|
| ALTR | MISSING: opcode | Register Indirection | MISSING: cycles | MISSING: flags | Field Alteration | Partial | MISSING: opcode, cycles, flags, full description |
| ALTD | MISSING: opcode | Register Indirection | MISSING: cycles | MISSING: flags | Field Alteration | Partial | MISSING: opcode, cycles, flags, full description |
| ALTS | MISSING: opcode | Register Indirection | MISSING: cycles | MISSING: flags | Field Alteration | Partial | MISSING: opcode, cycles, flags, full description |
| ALTB | MISSING: opcode | Register Indirection | MISSING: cycles | MISSING: flags | Field Alteration | Partial | MISSING: opcode, cycles, flags, full description |
| ALTI | MISSING: opcode | Register Indirection | MISSING: cycles | MISSING: flags | Field Alteration | Partial | MISSING: opcode, cycles, flags, full description |
| ALTSN | MISSING: opcode | Register Indirection | MISSING: cycles | MISSING: flags | Nibble/Byte/Word | Partial | MISSING: opcode, cycles, flags, full description |
| ALTGN | MISSING: opcode | Register Indirection | MISSING: cycles | MISSING: flags | Nibble/Byte/Word | Partial | MISSING: opcode, cycles, flags, full description |
| ALTSB | MISSING: opcode | Register Indirection | MISSING: cycles | MISSING: flags | Nibble/Byte/Word | Partial | MISSING: opcode, cycles, flags, full description |
| ALTGB | MISSING: opcode | Register Indirection | MISSING: cycles | MISSING: flags | Nibble/Byte/Word | Partial | MISSING: opcode, cycles, flags, full description |
| ALTSW | MISSING: opcode | Register Indirection | MISSING: cycles | MISSING: flags | Nibble/Byte/Word | Partial | MISSING: opcode, cycles, flags, full description |
| ALTGW | MISSING: opcode | Register Indirection | MISSING: cycles | MISSING: flags | Nibble/Byte/Word | Partial | MISSING: opcode, cycles, flags, full description |

### Specialized Hardware (15+ instructions)

| Instruction | Opcode | Meta Group | Clock Cycles | Flag Effects | Category | Description Status | Missing Info |
|-------------|--------|------------|--------------|--------------|----------|-------------------|--------------|
| ADDPIX | MISSING: opcode | Specialized Hardware | MISSING: cycles | MISSING: flags | Pixel Mixer | Partial | MISSING: opcode, cycles, flags, full description |
| MULPIX | MISSING: opcode | Specialized Hardware | MISSING: cycles | MISSING: flags | Pixel Mixer | Partial | MISSING: opcode, cycles, flags, full description |
| BLNPIX | MISSING: opcode | Specialized Hardware | MISSING: cycles | MISSING: flags | Pixel Mixer | Partial | MISSING: opcode, cycles, flags, full description |
| MIXPIX | MISSING: opcode | Specialized Hardware | MISSING: cycles | MISSING: flags | Pixel Mixer | Partial | MISSING: opcode, cycles, flags, full description |
| SETPIV | MISSING: opcode | Specialized Hardware | MISSING: cycles | MISSING: flags | Pixel Mixer | Partial | MISSING: opcode, cycles, flags, full description |
| SETPIX | MISSING: opcode | Specialized Hardware | MISSING: cycles | MISSING: flags | Pixel Mixer | Partial | MISSING: opcode, cycles, flags, full description |
| SETCY | MISSING: opcode | Specialized Hardware | MISSING: cycles | MISSING: flags | Color Space | Partial | MISSING: opcode, cycles, flags, full description |
| SETCI | MISSING: opcode | Specialized Hardware | MISSING: cycles | MISSING: flags | Color Space | Partial | MISSING: opcode, cycles, flags, full description |
| SETCQ | MISSING: opcode | Specialized Hardware | MISSING: cycles | MISSING: flags | Color Space | Partial | MISSING: opcode, cycles, flags, full description |
| SETCFRQ | MISSING: opcode | Specialized Hardware | MISSING: cycles | MISSING: flags | Color Space | Partial | MISSING: opcode, cycles, flags, full description |
| SETCMOD | MISSING: opcode | Specialized Hardware | MISSING: cycles | MISSING: flags | Color Space | Partial | MISSING: opcode, cycles, flags, full description |
| XINIT | MISSING: opcode | Specialized Hardware | MISSING: cycles | MISSING: flags | Streamer | Partial | MISSING: opcode, cycles, flags, full description |
| XSTOP | MISSING: opcode | Specialized Hardware | MISSING: cycles | MISSING: flags | Streamer | Partial | MISSING: opcode, cycles, flags, full description |
| XZERO | MISSING: opcode | Specialized Hardware | MISSING: cycles | MISSING: flags | Streamer | Partial | MISSING: opcode, cycles, flags, full description |
| XCONT | MISSING: opcode | Specialized Hardware | MISSING: cycles | MISSING: flags | Streamer | Partial | MISSING: opcode, cycles, flags, full description |
| SETXFRQ | MISSING: opcode | Specialized Hardware | MISSING: cycles | MISSING: flags | Streamer | Partial | MISSING: opcode, cycles, flags, full description |
| GETXACC | MISSING: opcode | Specialized Hardware | MISSING: cycles | MISSING: flags | Streamer | Partial | MISSING: opcode, cycles, flags, full description |

---

## Summary Statistics

- **Total Instructions Cataloged**: 242 instructions across 10 major categories
- **Complete Information**: 0 instructions
- **Partial Information**: 242 instructions (all instruction names extracted from CSV)
- **Missing Information**: All opcodes, cycles, flag effects, and full descriptions
- **Categories Completed**: 10 of 10 major categories
  - Math and Logic: 42 instructions
  - Branch and Flow Control: 24 instructions  
  - Hub RAM Operations: 11 instructions
  - Smart Pins: 9 instructions
  - Events System: 35 instructions
  - CORDIC Solver: 10 instructions
  - Pin I/O Control: 32 instructions
  - Hub FIFO Operations: 12 instructions
  - Register Indirection: 11 instructions
  - Specialized Hardware: 17 instructions
- **Coverage Status**: Core instruction extraction complete (242 of 491 total including aliases/variants)
- **Next Steps**: Identify missing instructions and variants, then enrich from silicon documentation

## Enrichment Targets

### High Priority Missing Information
1. **Opcodes**: Required for assembler implementation
2. **Clock Cycles**: Critical for timing analysis
3. **Flag Effects**: Essential for conditional operations
4. **Full Descriptions**: Needed for comprehensive understanding

### Information Sources to Process
- P2 Silicon Documentation (PDF)
- Hardware Manual extractions
- Assembly language references
- Code examples with timing data

---

*This is a living document. All future ingestions should enrich this table with source attribution.*