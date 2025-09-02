# Chip Gracey Programming Patterns - Extended Precision Arithmetic

## Source Information
- **Provider**: Chip Gracey (P2 Designer)
- **Date**: 2025-09-02
- **Type**: Programming Patterns and Techniques
- **Source File**: `/engineering/ingestion/external-inputs/from-Chip/math-pasm.txt`
- **Authority**: ABSOLUTE - Direct from designer

---

## 🎯 CRITICAL NEW KNOWLEDGE

This document contains **authoritative patterns** for extended precision arithmetic on P2. These patterns show the EXACT instruction sequences needed for 64-bit and 128-bit operations - knowledge that is often missing or incorrectly documented.

---

## Extended Precision Addition Patterns

### 32-bit Unsigned Addition
```pasm
ADD     A0, B0     WCZ       'A0 = A0 + B0, C = carry, Z = (A0 result == 0)
```

### 64-bit Unsigned Addition
```pasm
ADD     A0, B0     WCZ       'A0 = A0 + B0, C = carry, Z = (A0 result == 0)
ADDX    A1, B1     WCZ       'A1 = A1 + B1 + C, C = carry, Z = Z AND (A1 result == 0)
```

### 128-bit Unsigned Addition
```pasm
ADD     A0, B0     WCZ       'A0 = A0 + B0, C = carry, Z = (A0 result == 0)
ADDX    A1, B1     WCZ       'A1 = A1 + B1 + C, C = carry, Z = Z AND (A1 result == 0)
ADDX    A2, B2     WCZ       'A2 = A2 + B2 + C, C = carry, Z = Z AND (A2 result == 0)
ADDX    A3, B3     WCZ       'A3 = A3 + B3 + C, C = carry, Z = Z AND (A3 result == 0)
```

### 32-bit Signed Addition
```pasm
ADDS    A0, B0     WCZ       'A0 = A0 + B0, C = true sign of A0 result, Z = (A0 result == 0)
```

### 64-bit Signed Addition
```pasm
ADD     A0, B0     WCZ       'A0 = A0 + B0, C = carry, Z = (A0 result == 0)
ADDSX   A1, B1     WCZ       'A1 = A1 + B1 + C, C = true sign of A1 result, Z = Z AND (A1 result == 0)
```
**Critical**: Note the use of ADDSX (not ADDX) for the final word!

### 128-bit Signed Addition
```pasm
ADD     A0, B0     WCZ       'A0 = A0 + B0, C = carry, Z = (A0 result == 0)
ADDX    A1, B1     WCZ       'A1 = A1 + B1 + C, C = carry, Z = Z AND (A1 result == 0)
ADDX    A2, B2     WCZ       'A2 = A2 + B2 + C, C = carry, Z = Z AND (A2 result == 0)
ADDSX   A3, B3     WCZ       'A3 = A3 + B3 + C, C = true sign of A3 result, Z = Z AND (A3 result == 0)
```
**Critical**: ADDSX only on the FINAL (most significant) word!

---

## Extended Precision Subtraction Patterns

### 32-bit Unsigned Subtraction
```pasm
SUB     A0, B0     WCZ       'A0 = A0 - B0, C = borrow, Z = (A0 result == 0)
```

### 64-bit Unsigned Subtraction
```pasm
SUB     A0, B0     WCZ       'A0 = A0 - B0, C = borrow, Z = (A0 result == 0)
SUBX    A1, B1     WCZ       'A1 = A1 - B1 - C, C = borrow, Z = Z AND (A1 result == 0)
```

### 128-bit Unsigned Subtraction
```pasm
SUB     A0, B0     WCZ       'A0 = A0 - B0, C = borrow, Z = (A0 result == 0)
SUBX    A1, B1     WCZ       'A1 = A1 - B1 - C, C = borrow, Z = Z AND (A1 result == 0)
SUBX    A2, B2     WCZ       'A2 = A2 - B2 - C, C = borrow, Z = Z AND (A2 result == 0)
SUBX    A3, B3     WCZ       'A3 = A3 - B3 - C, C = borrow, Z = Z AND (A3 result == 0)
```

### 32-bit Signed Subtraction
```pasm
SUBS    A0, B0     WCZ       'A0 = A0 - B0, C = true sign of A0 result, Z = (A0 result == 0)
```

### 64-bit Signed Subtraction
```pasm
SUB     A0, B0     WCZ       'A0 = A0 - B0, C = borrow, Z = (A0 result == 0)
SUBSX   A1, B1     WCZ       'A1 = A1 - B1 - C, C = true sign of A1 result, Z = Z AND (A1 result == 0)
```

### 128-bit Signed Subtraction
```pasm
SUB     A0, B0     WCZ       'A0 = A0 - B0, C = borrow, Z = (A0 result == 0)
SUBX    A1, B1     WCZ       'A1 = A1 - B1 - C, C = borrow, Z = Z AND (A1 result == 0)
SUBX    A2, B2     WCZ       'A2 = A2 - B2 - C, C = borrow, Z = Z AND (A2 result == 0)
SUBSX   A3, B3     WCZ       'A3 = A3 - B3 - C, C = true sign of A3 result, Z = Z AND (A3 result == 0)
```

---

## Extended Precision Comparison Patterns

### 32-bit Unsigned Compare
```pasm
CMP     A0, B0     WCZ       'X = A0 - B0, C = borrow, Z = (X == 0)
```

### 64-bit Unsigned Compare
```pasm
CMP     A0, B0     WCZ       'X = A0 - B0, C = borrow, Z = (X == 0)
CMPX    A1, B1     WCZ       'X = A1 - B1 - C, C = borrow, Z = Z AND (X == 0)
```

### 128-bit Unsigned Compare
```pasm
CMP     A0, B0     WCZ       'X = A0 - B0, C = borrow, Z = (X == 0)
CMPX    A1, B1     WCZ       'X = A1 - B1 - C, C = borrow, Z = Z AND (X == 0)
CMPX    A2, B2     WCZ       'X = A2 - B2 - C, C = borrow, Z = Z AND (X == 0)
CMPX    A3, B3     WCZ       'X = A3 - B3 - C, C = borrow, Z = Z AND (X == 0)
```

### 32-bit Signed Compare
```pasm
CMPS    A0, B0     WCZ       'X = A0 - B0, C = true sign of X, Z = (X == 0)
```

### 64-bit Signed Compare
```pasm
CMP     A0, B0     WCZ       'X = A0 - B0, C = borrow, Z = (X == 0)
CMPSX   A1, B1     WCZ       'X = A1 - B1 - C, C = true sign of X, Z = Z AND (X == 0)
```

### 128-bit Signed Compare
```pasm
CMP     A0, B0     WCZ       'X = A0 - B0, C = borrow, Z = (X == 0)
CMPX    A1, B1     WCZ       'X = A1 - B1 - C, C = borrow, Z = Z AND (X == 0)
CMPX    A2, B2     WCZ       'X = A2 - B2 - C, C = borrow, Z = Z AND (X == 0)
CMPSX   A3, B3     WCZ       'X = A3 - B3 - C, C = true sign of X, Z = Z AND (X == 0)
```

---

## 🔑 Critical Pattern Rules

### Pattern 1: Unsigned Multi-Word Operations
```
First word:  ADD/SUB/CMP   - Generates initial carry/borrow
Middle words: ADDX/SUBX/CMPX - Propagates carry/borrow
Last word:   ADDX/SUBX/CMPX - Final carry/borrow
```

### Pattern 2: Signed Multi-Word Operations
```
First word:  ADD/SUB/CMP   - Generates initial carry/borrow
Middle words: ADDX/SUBX/CMPX - Propagates carry/borrow
Last word:   ADDSX/SUBSX/CMPSX - Converts to true sign!
```

### Pattern 3: Flag Behavior
- **C Flag Evolution**: carry/borrow → carry/borrow → true sign (signed only)
- **Z Flag Evolution**: (result == 0) → AND accumulation → final equality

### Pattern 4: Word Ordering
- A0, B0 = Least significant word (LSW)
- A1, B1 = Next word
- A2, B2 = Next word
- A3, B3 = Most significant word (MSW)

---

## 🎯 Why This Matters

### Common Mistakes This Prevents
1. **Using ADDX for final signed word** - WRONG! Must use ADDSX
2. **Using ADDS for middle words** - WRONG! Only ADD/ADDX
3. **Wrong flag interpretation** - C means different things!
4. **Z flag confusion** - It accumulates with AND!

### Applications Enabled
- Cryptographic operations (256-bit, 512-bit)
- High-precision financial calculations
- Scientific computing
- Large integer arithmetic
- Extended precision DSP

---

## 📊 Pattern Summary Table

| Bits | Type | First Inst | Middle Inst | Final Inst | C Result | Z Result |
|------|------|-----------|-------------|------------|----------|----------|
| 32 | Unsigned | ADD/SUB/CMP | - | - | carry/borrow | ==0 |
| 32 | Signed | ADDS/SUBS/CMPS | - | - | true sign | ==0 |
| 64 | Unsigned | ADD/SUB/CMP | - | ADDX/SUBX/CMPX | carry/borrow | all==0 |
| 64 | Signed | ADD/SUB/CMP | - | ADDSX/SUBSX/CMPSX | true sign | all==0 |
| 128 | Unsigned | ADD/SUB/CMP | ADDX/SUBX/CMPX | ADDX/SUBX/CMPX | carry/borrow | all==0 |
| 128 | Signed | ADD/SUB/CMP | ADDX/SUBX/CMPX | ADDSX/SUBSX/CMPSX | true sign | all==0 |

---

## Integration Notes

### This Document's Role
- **Type**: Programming Patterns (not instruction definitions)
- **Authority**: ABSOLUTE - from P2 designer
- **Usage**: Reference for code generation
- **Testing**: All patterns should be validated

### Cross-References
- Instruction definitions in `chip-instruction-clarifications-*.md`
- Related to ADD/SUB/CMP instruction families
- Critical for extended precision library development

---

**Document Status**: Complete - Patterns extracted and documented
**Authority Level**: ABSOLUTE - Direct from Chip Gracey
**Usage**: Essential reference for extended precision arithmetic