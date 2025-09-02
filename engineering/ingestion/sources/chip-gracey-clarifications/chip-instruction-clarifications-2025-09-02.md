# Chip Gracey Instruction Clarifications - Advanced Arithmetic

## Source Information
- **Provider**: Chip Gracey (P2 Designer)
- **Date**: 2025-09-02
- **Context**: Advanced arithmetic instructions and extended precision patterns
- **Source File**: `/engineering/ingestion/external-inputs/from-Chip/math-pasm.txt`
- **Method**: Direct expert clarification
- **Total Instructions Clarified**: 6 new + comprehensive ADD/SUB/CMP overview

## Status Impact
- **Previous Instruction Gap**: 165 instructions (after first clarification)
- **Post-Clarification Gap**: 159 instructions
- **Gap Reduction**: 6 instructions directly
- **BONUS**: Programming patterns for extended precision arithmetic

---

## Instruction Documentation

### 1. INCMOD - Increment with Modulo

**Syntax**: `INCMOD D,{#}S {WC/WZ/WCZ}`

**Function**: Increment D with wrapping to 0 if D = S
- If D = S then D = 0 and C flag = 1
- Else D = D + 1 and C flag = 0
- Z flag is set if D result is 0

**Use Cases**:
- Circular buffer indexing
- Counter with automatic reset
- State machine cycling

---

### 2. DECMOD - Decrement with Modulo

**Syntax**: `DECMOD D,{#}S {WC/WZ/WCZ}`

**Function**: Decrement D with wrapping to S if D = 0
- If D = 0 then D = S and C flag = 1
- Else D = D - 1 and C flag = 0
- Z flag is set if D result is 0

**Use Cases**:
- Reverse circular buffer traversal
- Countdown with automatic reload
- Cyclic state machine reverse

---

### 3. FRAC - Fractional Multiply (Spin2 operator)

**Syntax**: `x FRAC y` (Spin2)

**Function**: Computes unsigned (x << 32) / y
- Performs fractional multiplication
- Returns the fractional part of division
- Useful for scaling operations

**Use Cases**:
- Fixed-point arithmetic
- Scaling calculations
- Proportional computations

---

### 4. ADDSX - Add with Sign Extension

**Syntax**: `ADDSX D,{#}S {WC/WZ/WCZ}`

**Function**: Adds (S + C flag) into D with true sign result
- D = D + S + C flag
- C = true sign of D result (bit above MSB)
- Z = Z AND (D result == 0)

**Critical Use**: Capping multi-long signed additions
- Used as the FINAL instruction in multi-word signed add
- Provides true sign of entire multi-word result
- Maintains cumulative zero detection

---

### 5. SUBSX - Subtract with Sign Extension

**Syntax**: `SUBSX D,{#}S {WC/WZ/WCZ}`

**Function**: Subtracts (S + C flag) from D with true sign result
- D = D - S - C flag
- C = true sign of D result (bit above MSB)
- Z = Z AND (D result == 0)

**Critical Use**: Capping multi-long signed subtractions
- Used as the FINAL instruction in multi-word signed subtract
- Provides true sign of entire multi-word result
- Maintains cumulative zero detection

---

### 6. CMPSX - Compare with Sign Extension

**Syntax**: `CMPSX D,{#}S {WC/WZ/WCZ}`

**Function**: Compares D to (S + C flag) with true sign result
- X = D - S - C flag (result not stored)
- C = true sign of comparison
- Z = Z AND (X == 0)

**Critical Use**: Capping multi-long signed comparisons
- Used as the FINAL instruction in multi-word signed compare
- Provides true sign of entire multi-word comparison
- Maintains cumulative equality detection

---

## Comprehensive ADD/SUB/CMP Overview

### ADD Family
| Instruction | Operation | C Flag | Z Flag |
|------------|-----------|--------|--------|
| ADD | D = D + S | carry | (result == 0) |
| ADDX | D = D + S + C | carry | Z AND (result == 0) |
| ADDS | D = D + S | true sign | (result == 0) |
| ADDSX | D = D + S + C | true sign | Z AND (result == 0) |

### SUB Family
| Instruction | Operation | C Flag | Z Flag |
|------------|-----------|--------|--------|
| SUB | D = D - S | borrow | (result == 0) |
| SUBX | D = D - S - C | borrow | Z AND (result == 0) |
| SUBS | D = D - S | true sign | (result == 0) |
| SUBSX | D = D - S - C | true sign | Z AND (result == 0) |

### CMP Family
| Instruction | Operation | C Flag | Z Flag |
|------------|-----------|--------|--------|
| CMP | X = D - S | borrow | (X == 0) |
| CMPX | X = D - S - C | borrow | Z AND (X == 0) |
| CMPS | X = D - S | true sign | (X == 0) |
| CMPSX | X = D - S - C | true sign | Z AND (X == 0) |

---

## Critical Insights

### The X Suffix Pattern
- **X suffix**: Includes carry/borrow in operation
- **Z behavior**: ANDs with existing Z (cumulative zero detection)
- **Purpose**: Multi-word arithmetic chaining

### The S Suffix Pattern
- **S suffix**: Returns true sign instead of carry/borrow
- **Sign meaning**: The bit above the MSB of the result
- **Purpose**: Signed arithmetic operations

### The SX Combination
- **SX suffix**: Both carry inclusion AND true sign result
- **Critical role**: FINAL instruction in signed multi-word operations
- **Why final**: Converts carry chain to true sign

---

## Related Programming Patterns

**NOTE**: This clarification includes critical programming patterns for extended precision arithmetic. See companion document:
`chip-gracey-programming-patterns-2025-09-02.md`

---

**Document Status**: Complete - Instruction clarifications extracted
**Companion Document**: Programming patterns documented separately
**Integration Status**: Ready for matrix update