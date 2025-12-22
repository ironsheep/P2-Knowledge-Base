# Chapter 3: Flags and Conditional Execution

<!-- Chapter covering C and Z flags, WC/WZ/WCZ effects, and IF_x conditions -->

The P2 has two status flags that enable conditional execution and multi-precision arithmetic. Understanding flag behavior is essential for writing efficient, branching-free code.

The P2's flag system differs from many processors in two important ways. First, flags persist until explicitly modified—an instruction without WC or WZ effects leaves flags unchanged, allowing flag values to be used by multiple subsequent instructions. Second, any instruction can be made conditional using IF_x prefixes, enabling deterministic branchless programming where instruction timing remains constant regardless of data values.

These two features combine to create a powerful programming model where complex decision logic can be expressed without branches, maintaining cycle-accurate timing while reducing code size and improving readability.


## 3.1 The C and Z Flags

Each COG maintains two independent status flags that track computation results and enable conditional execution. These flags are named C (Carry) and Z (Zero), but their meanings extend beyond these basic interpretations depending on the instruction that sets them.

### 3.1.1 The C Flag (Carry/Borrow)

The C flag serves multiple purposes depending on instruction context:

**For arithmetic operations**, C indicates **unsigned overflow** after addition (carry out of bit 31) or **unsigned borrow** after subtraction (when the subtrahend exceeds the minuend). This enables multi-precision arithmetic where carries or borrows propagate between 32-bit operations.

**For shift and rotate operations**, C captures the **bit value shifted out** of the result. A left shift stores bit 31 in C; a right shift stores bit 0 in C. This enables implementing shifts wider than 32 bits by chaining operations.

**For comparison operations**, C indicates the **relationship between operands**. After an unsigned comparison (CMP), C=1 means the first operand is below (less than) the second. After a signed comparison (CMPS), C=1 means the first operand is less than the second using signed interpretation.

**For logical operations**, C indicates **parity**—whether the result contains an odd number of 1 bits. This specialized behavior supports error detection and certain bit manipulation patterns.

### 3.1.2 The Z Flag (Zero)

The Z flag indicates **zero result** or **equality** across most instructions:

**For arithmetic and logical operations**, Z=1 when the result equals zero. This enables testing for zero values, detecting exhausted counters, or identifying cleared registers.

**For comparison operations**, Z=1 when the operands are equal. This works for both signed (CMPS) and unsigned (CMP) comparisons—equality has the same meaning regardless of interpretation.

**For bit test operations**, Z=1 when the tested bits are all clear. The TEST instruction ANDs its operands and sets Z based on whether the result is zero, effectively testing whether any specified bits are set.

### 3.1.3 Flag Persistence and Independence

Flags retain their values until explicitly modified by a WC, WZ, or WCZ effect. This persistence is a deliberate design feature that enables powerful programming patterns:

::: pasm2
                cmp     a, b            wcz     ' Set flags once
        if_c    mov     min, a                  ' Use C here
        if_nc   mov     min, b                  ' And here
        if_z    mov     equal, #1               ' And use Z here
:::

In this example, one comparison sets both flags, and three subsequent instructions each test the preserved flag values. No instruction between them modifies the flags, so the flag state from the comparison remains available.

Each COG maintains its own C and Z flags completely independently. Flag values in COG 0 have no relationship to flag values in COG 1. This independence ensures parallel execution across COGs operates without interference.


## 3.2 Flag Modification Effects

Every instruction can optionally specify which flags to update using effect modifiers. These modifiers—WC, WZ, and WCZ—control whether the instruction modifies the C flag, the Z flag, both flags, or neither flag. The operation always executes; effects only determine whether flags are updated.

### 3.2.1 The WC Effect

::: pasm2
        add     result, value   wc      ' Update C flag based on carry
:::

When WC (Write C) is specified, the instruction updates the C flag according to its specific C condition while leaving Z unchanged. For ADD, this means C is set if the addition produces a carry out of bit 31. For CMP, this means C is set if the first operand is less than the second. Each instruction defines its own C condition as documented in the instruction reference.

The key insight: WC means "update C according to this instruction's C rule." The rule varies by instruction, but the WC effect itself is consistent—it enables C modification.

### 3.2.2 The WZ Effect

::: pasm2
        add     result, value   wz      ' Update Z flag based on result
:::

When WZ (Write Z) is specified, the instruction updates the Z flag based on whether the result equals zero, while leaving C unchanged. Z=1 indicates a zero result; Z=0 indicates a non-zero result. This behavior is consistent across nearly all instructions—the Z flag always reflects "is the result zero?"

This consistency makes WZ predictable. After any arithmetic, logical, or shift operation with WZ, checking IF_Z tests whether the result was zero. After a comparison with WZ, checking IF_Z tests whether the operands were equal.

**Exception: Extended Instructions (Z AND behavior)**

The extended arithmetic instructions—ADDX, SUBX, ADDSX, SUBSX, CMPX, CMPSX—use a modified Z flag update rule:

```text
Z = Z AND (result == 0)
```

Instead of simply replacing Z with the zero test, these instructions AND the new zero status with the existing Z flag. This behavior is essential for multi-precision arithmetic:

::: pasm2
' 64-bit addition: [hi:lo] += [bhi:blo]
        add     lo, blo         wcz     ' Add low 32 bits, Z = (lo_result == 0)
        addx    hi, bhi         wcz     ' High + carry, Z = Z AND (hi==0)
        ' Z is now 1 only if BOTH lo and hi were zero
        '  (entire 64-bit result is zero)
:::

Without this AND behavior, the final Z flag would only reflect the last 32-bit operation, losing information about whether the full multi-precision result was zero. The AND logic accumulates zero detection across all operations in the chain.

**Source Verification:** CSV v35 documents this as "Z = Z AND (Result = 0)" for all extended instructions.

### 3.2.3 The WCZ Effect

::: pasm2
        add     result, value   wcz     ' Update both flags
:::

When WCZ (Write C and Z) is specified, both flags are updated according to their respective conditions. You can specify WC to update only C, WZ to update only Z, or WCZ to update both—these are the three valid effect options.

WCZ is common after comparisons where both the ordering (C) and equality (Z) matter, or after arithmetic operations where both carry detection and zero detection are needed.

### 3.2.4 Special Flag Effects (ANDC/ANDZ/ORC/ORZ/XORC/XORZ)

The TESTB, TESTBN, TESTP, and TESTPN instructions support additional flag effects that perform bitwise operations on the existing flag value rather than replacing it. These enable testing multiple bits and accumulating the results into a single flag.

| Effect | Operation | Description |
|:-------|:----------|:------------|
| ANDC | C = C AND bit | AND tested bit into C |
| ANDZ | Z = Z AND bit | AND tested bit into Z |
| ORC | C = C OR bit | OR tested bit into C |
| ORZ | Z = Z OR bit | OR tested bit into Z |
| XORC | C = C XOR bit | XOR tested bit into C |
| XORZ | Z = Z XOR bit | XOR tested bit into Z |

Unlike WC and WZ which replace the flag value, these effects combine the tested bit with the existing flag value using the specified boolean operation.

**Use Case: Testing Multiple Bits**

The most common use is testing whether ALL bits in a set are high (AND), or whether ANY bit in a set is high (OR):

::: pasm2
' Test if ALL of pins 0, 4, and 7 are high (AND pattern)
        testp   #0              wc      ' C = pin 0 state
        testp   #4              andc    ' C = C AND pin 4 state
        testp   #7              andc    ' C = C AND pin 7 state
        ' C = 1 only if ALL three pins are high

' Test if ANY of pins 0, 4, or 7 is high (OR pattern)
        testpn  #0              wc      ' C = NOT pin 0 (so C=0 if pin high)
        testpn  #4              andc    ' C = C AND NOT pin 4
        testpn  #7              andc    ' C = C AND NOT pin 7
        ' C = 0 if ANY pin is high, C = 1 if ALL pins are low
:::

**TESTB vs TESTP:**

- TESTB tests a bit within a register: `TESTB reg, #bit_number`
- TESTP tests a pin's input state: `TESTP #pin_number`
- TESTBN and TESTPN test the inverted bit or pin state

**Source Verification:** CSV v35 documents these as `C/Z = C/Z AND/OR/XOR D[S[4:0]]` for TESTB variants and `C/Z = C/Z AND/OR/XOR IN[D[5:0]]` for TESTP variants.

### 3.2.5 No Effect (Default)

::: pasm2
        add     result, value           ' Execute operation, preserve flags
:::

When no effect is specified, the instruction executes normally but leaves both C and Z unchanged. This is not a "do nothing" mode—the operation completes, the destination is written, and timing is identical to the flagged version. Only the flags are preserved.

This behavior enables using flag values across multiple instructions without interference:

::: pasm2
                cmp     a, b            wc      ' Set C based on comparison
                mov     temp, c                 ' Does not modify C
                add     temp, d                 ' Does not modify C
        if_c    mov     result, temp            ' Tests original C
:::

The comparison sets C, and two subsequent operations execute without modifying it. The conditional instruction tests the comparison result even though two operations occurred in between.

### 3.2.6 Effect Availability

Not all instructions support all effect modifiers. Each instruction defines which effects are valid based on whether its C and Z outputs have meaningful interpretations.

**Effect Permission Categories:**

| Permission | Allowed Effects | Reason |
|------------|-----------------|--------|
| None | (no effects) | Instruction produces no meaningful flag result |
| WC only | WC | Only the C flag has a defined meaning |
| WZ only | WZ | Only the Z flag has a defined meaning |
| Full | WC, WZ, WCZ | Both flags have defined meanings |

**Why WCZ Requires Both Flags:**

Although WCZ encodes as the combination of WC and WZ bits, the assembler validates that both individual effects are meaningful before allowing WCZ. Using WCZ on an instruction that only supports WC would set Z to an undefined value—the assembler prevents this by requiring full effect support for WCZ.

::: pasm2
' Example: LOCKTRY only produces meaningful C (lock acquired)
        locktry #0              wc      ' Valid: C = lock acquired
        locktry #0              wz      ' ERROR: Z has no meaning
        locktry #0              wcz     ' ERROR: WCZ requires both to be valid
:::

**Common Restrictions:**

- **NOP**: No effects allowed (and no condition prefix)
- **LOCKTRY/LOCKREL**: WC only (C indicates lock status)
- **TESTP/TESTPN/TESTB/TESTBN**: Support both basic effects (WC, WZ) and extended effects (ANDC, ORC, etc.) as documented in Section 3.2.4
- **Some Hub memory operations**: May have restricted effect support

The Part II instruction reference documents the allowed effects for each instruction in its encoding table. When an invalid effect is specified, the assembler produces the error: "This effect is not allowed for this instruction."


## 3.3 Conditional Execution

The P2 allows any instruction to execute conditionally based on the current flag values. This conditional execution mechanism enables branchless programming—expressing decision logic without jump instructions—which maintains deterministic timing and often reduces code size.

### 3.3.1 The IF_x Prefix

Any instruction can be made conditional by prefixing with an IF_x condition. When the condition is false, the instruction does not execute, but still consumes its normal execution time (2 clock cycles). When the condition is true, the instruction executes normally:

::: pasm2
                cmp     a, b            wcz     ' Compare, set flags
        if_z    mov     result, #1              ' Only if Z=1 (equal)
        if_nz   mov     result, #0              ' Only if Z=0 (not equal)
:::

This three-instruction sequence sets `result` to 1 if `a` equals `b`, or 0 if they differ. It takes exactly three clock cycles regardless of the comparison result. The unconditional CMP always executes, then exactly one of the two conditional MOVs executes.

The timing predictability is crucial. Traditional branch-based code has variable timing depending on which path is taken. Conditional execution eliminates this variation—the instruction stream is fixed, and timing is constant.

### 3.3.2 Conditional Execution Timing

When a conditional instruction's condition is false, the instruction does not execute but still consumes 2 clock cycles. This behavior might seem wasteful, but it provides deterministic timing—critical for real-time operations, protocol timing, and cycle-accurate code.

Consider this example:

::: pasm2
                test    flags, #BIT_READY  wz   ' Check ready bit
        if_nz   rdlong  data, ptr               ' Read if ready
        if_nz   add     ptr, #4                 ' Advance if read occurred
:::

This sequence takes exactly three clock cycles whether the ready bit is set or clear. If implementing the same logic with branches:

::: pasm2
                test    flags, #BIT_READY  wz
        if_z    jmp     #skip
                rdlong  data, ptr
                add     ptr, #4
skip
:::

The branch version takes 2 cycles when not ready (test + jump) or 4 cycles when ready (test + not-jump + rdlong + add). The timing varies by 100%. The conditional version maintains constant 3-cycle timing.

For real-time code, deterministic timing often matters more than average speed.

### 3.3.3 Available Conditions

The P2 provides sixteen conditions covering all possible combinations of C and Z flag states. Each condition can be expressed using its primary mnemonic or one of several aliases designed to make code more readable in specific contexts.

The most commonly used conditions are:

- **IF_C** / **IF_NC** — Test the C flag (set / clear)
- **IF_Z** / **IF_NZ** — Test the Z flag (set / clear)
- **(no condition)** — When omitted, instructions execute unconditionally (encodes as EEEE=1111)
- **_RET_** — Execute instruction, then return

> **📖 Complete Reference:** For the full table of all sixteen conditions with their EEEE encodings, flag state patterns, and complete alias listings (comparison aliases, flag state aliases, logical aliases, and commutative forms), see **Appendix B: Condition Code Reference**.

### 3.3.4 Comparison Condition Aliases

After a comparison instruction (CMP or CMPS), the C and Z flags can be tested with aliases that express relational operators. Two equivalent terminology styles are available:

| Condition | Magnitude Style | Arithmetic Style | Relational | Meaning |
|-----------|-----------------|------------------|------------|---------|
| IF_C | IF_B | IF_LT | < | a is less than b |
| IF_NC | IF_AE | IF_GE | >= | a is greater or equal to b |
| IF_Z | IF_E | IF_E | == | a equals b |
| IF_NZ | IF_NE | IF_NE | != | a not equal to b |
| IF_NC_AND_NZ | IF_A | IF_GT | > | a is greater than b |
| IF_C_OR_Z | IF_BE | IF_LE | <= | a is less or equal to b |

**Both styles encode to identical condition codes**—the choice is purely stylistic. Use whichever terminology reads best for your code:

- **Magnitude terminology** (A = Above, B = Below) reads naturally with addresses, counts, and sizes
- **Arithmetic terminology** (GT = Greater Than, LT = Less Than) reads naturally with temperatures, positions, and deltas

**The compare instruction determines the comparison type:**

- **CMP** performs unsigned subtraction—flags reflect unsigned ordering
- **CMPS** performs signed subtraction—flags reflect signed ordering

Either alias style works correctly with either compare instruction. The choice of CMP vs. CMPS determines whether $80000000 is treated as a large positive number or a negative number. The alias you use afterward is simply a matter of which terminology reads better in your code.


## 3.4 Flag Behavior by Instruction Category

Flag meanings vary by instruction category. Understanding these patterns helps predict flag behavior without consulting the instruction reference for each operation.

### 3.4.1 Arithmetic Instructions

Arithmetic instructions set C based on unsigned overflow (carry or borrow) and set Z when the result equals zero:

| Instruction | C Flag (with WC) | Z Flag (with WZ) |
|-------------|------------------|------------------|
| ADD | Unsigned carry out of bit 31 | Result = 0 |
| ADDS | Signed overflow occurred | Result = 0 |
| SUB | Unsigned borrow (A < B) | Result = 0 |
| SUBS | Signed overflow occurred | Result = 0 |
| CMP | Unsigned borrow (A < B) | A = B |
| CMPS | Sign mismatch (signed A < B) | A = B |

For ADD, C=1 indicates that adding the operands produced a value larger than 32 bits can represent—a carry occurred. For SUB and CMP, C=1 indicates the first operand is less than the second (a borrow would be required). The result is always written to the destination (for ADD/SUB) or the flags are set (for CMP/CMPS).

ADDS and SUBS handle signed overflow detection. Signed overflow occurs when adding two positive values produces a negative result, or adding two negative values produces a positive result. The C flag captures this condition with WC.

### 3.4.2 Logic Instructions

Logical instructions set C based on parity and set Z based on whether the result is zero:

| Instruction | C Flag (with WC) | Z Flag (with WZ) |
|-------------|------------------|------------------|
| AND | Parity (odd # of 1 bits) | Result = 0 |
| OR | Parity (odd # of 1 bits) | Result = 0 |
| XOR | Parity (odd # of 1 bits) | Result = 0 |
| NOT | Parity (odd # of 1 bits) | Result = 0 |

Parity means C=1 when the result contains an odd number of 1 bits, and C=0 when the result contains an even number of 1 bits. This enables parity checking for error detection—XOR all data bits together, and C indicates odd parity.

The Z flag behavior is straightforward: Z=1 when the entire 32-bit result is zero. For AND, this occurs when the operands share no common 1 bits. For OR, this occurs when both operands are zero. For XOR, this occurs when the operands are identical.

### 3.4.3 Shift and Rotate Instructions

Shift and rotate instructions capture the bit shifted or rotated out in the C flag:

| Instruction | C Flag (with WC) | Z Flag (with WZ) |
|-------------|------------------|------------------|
| SHL | Bit 31 (MSB shifted out) | Result = 0 |
| SHR | Bit 0 (LSB shifted out) | Result = 0 |
| ROL | Bit 31 (MSB rotated out) | Result = 0 |
| ROR | Bit 0 (LSB rotated out) | Result = 0 |

For left operations (SHL, ROL), the most significant bit (bit 31) moves into C. For right operations (SHR, ROR), the least significant bit (bit 0) moves into C. This enables multi-precision shifts where the bit shifted out of one word becomes the bit shifted into the next word.

The difference between shift and rotate: shifts fill the vacated bit position with 0, while rotates fill it with the bit shifted out (creating a circular rotation). Both capture the bit that exits the register in C.

### 3.4.4 Move and Data Instructions

Move and data manipulation instructions set flags based on the source or result characteristics:

| Instruction | C Flag (with WC) | Z Flag (with WZ) |
|-------------|------------------|------------------|
| MOV | MSB of source (S[31]) | Source = 0 |
| NEG | Source was non-zero | Result = 0 |
| ABS | Source was negative | Result = 0 |
| NOT | Parity of result | Result = 0 |
| ENCOD | MSB of result | Result = 0 |
| DECOD | 0 (always cleared) | Result = 0 |

MOV is notable because its C flag reflects the sign bit of the source value, not the result (which is identical to the source). This enables sign testing without a separate comparison:

::: pasm2
        mov     temp, value     wc      ' Copy value, C = sign bit
        if_c    jmp     #negative       ' Branch if negative
:::

NEG sets C=1 if the source was non-zero, which indicates that negation actually changed the value. When the source is zero, negation produces zero and C=0.

ABS sets C=1 if the source was negative, indicating that the absolute value operation inverted the sign. This flag persists even for the special case of NEGX ($80000000), whose absolute value cannot be represented in 32 bits.


## 3.5 Common Flag Patterns

Understanding common flag usage patterns accelerates learning and provides templates for solving typical programming problems. These patterns demonstrate how flags enable elegant, efficient solutions.

### 3.5.1 Testing a Bit

Testing whether a specific bit is set uses TEST with WZ:

::: pasm2
                test    value, #%00000100  wz   ' Test bit 2
        if_nz   jmp     #bit_set                ' Jump if bit is set
:::

TEST performs a bitwise AND of its operands but writes the result nowhere—it only sets flags. The mask `%00000100` isolates bit 2. If bit 2 is set, the AND produces a non-zero result (specifically, the value 4), so Z=0. If bit 2 is clear, the AND produces zero, so Z=1.

The condition IF_NZ tests "not zero," which corresponds to "bit is set." This pattern works for testing any single bit or combination of bits—just construct the appropriate mask.

### 3.5.2 Multi-Precision Addition

Adding values wider than 32 bits requires propagating the carry between word additions:

::: pasm2
        add     x_lo, y_lo      wc      ' Add low words, capture carry
        addx    x_hi, y_hi              ' Add high words plus carry
:::

The first ADD adds the low 32 bits and sets C if the addition carries out. The ADDX instruction (Add with Carry) adds the high 32 bits plus the carry from the first addition. This extends to any number of words:

::: pasm2
        add     x0, y0          wc      ' Add word 0
        addx    x1, y1          wc      ' Add word 1 plus carry
        addx    x2, y2          wc      ' Add word 2 plus carry
        addx    x3, y3                  ' Add word 3 plus carry
:::

Each ADDX uses the carry from the previous addition and generates a new carry for the next addition. The result is 128-bit (4 × 32-bit) addition with correct carry propagation.

### 3.5.3 Conditional Assignment

Selecting between two values based on a comparison uses conditional moves:

::: pasm2
                cmp     a, b            wc      ' Compare a and b
        if_c    mov     result, a               ' If a < b, result = a
        if_nc   mov     result, b               ' If a >= b, result = b
:::

This implements `result = min(a, b)` without branches. The comparison sets C if `a < b` (unsigned). Exactly one of the two conditional moves executes, storing the smaller value in result. The sequence takes exactly three clock cycles regardless of which value is smaller.

For maximum of two values, invert the conditions:

::: pasm2
                cmp     a, b            wc      ' Compare a and b
        if_c    mov     result, b               ' If a < b, result = b
        if_nc   mov     result, a               ' If a >= b, result = a
:::

### 3.5.4 Branchless Absolute Value

Computing the absolute value of a signed number uses the ABS instruction with conditional negation:

::: pasm2
                abs     result, value   wc      ' Absolute value, C = negative
        if_c    neg     result                  ' Correct if was negative
:::

Wait—this looks wrong. If ABS already computes the absolute value, why negate it afterward?

The issue is a quirk of two's complement: the most negative value (-2,147,483,648 or $8000_0000) has no positive representation in 32 bits. Its absolute value cannot be represented. The ABS instruction handles this by leaving the value unchanged and setting C to indicate the exceptional case.

For all other negative values, ABS correctly computes the absolute value and clears C. For -2,147,483,648, ABS leaves it unchanged and sets C, and the conditional NEG negates it back to itself (since negating $8000_0000 produces $8000_0000).

Most code doesn't care about this edge case and can simply use `ABS result, value` without the conditional correction.

### 3.5.5 Conditional Increment/Decrement

Updating a counter only when a condition is met uses conditional arithmetic:

::: pasm2
                test    flags, #FLAG_READY  wz  ' Test ready flag
        if_nz   add     count, #1               ' Increment if ready
:::

This increments `count` only when the ready flag is set. No branches are needed, and timing is deterministic—two clock cycles regardless of flag state.

### 3.5.6 Bounds Checking

Checking whether a value falls within a range combines comparison and logical conditions:

::: pasm2
                cmp     value, min      wc      ' Check if value < min
        if_c    jmp     #out_of_range           ' Too small
                cmp     value, max      wc      ' Check if value >= max
        if_nc   jmp     #out_of_range           ' Too large
                ' Value is in range [min, max)
:::

This checks whether `value` is in the range [min, max). The first comparison tests for too small; the second tests for too large. If either condition fails, the value is out of range.


## 3.6 Advanced Flag Usage

Beyond basic conditional execution, the P2 provides specialized instructions for manipulating flags directly and using flags to control data flow. These advanced techniques enable sophisticated flag-based algorithms.

### 3.6.1 Direct Flag Manipulation

The MODC and MODZ instructions modify flags directly without performing computations:

::: pasm2
        modc    _set    wc      ' Set C flag to 1
        modz    _clr    wz      ' Clear Z flag to 0
:::

MODC sets C according to a 4-bit modifier constant, and MODZ sets Z similarly. The WC and WZ effects are required for the modification to take effect; without them, the result is computed but discarded. Common modifier constants include `_set` (always 1), `_clr` (always 0), `_c` (current C), and `_z` (current Z).

The MODCZ instruction can modify both flags simultaneously:

::: pasm2
        modcz   _clr, _set  wcz ' Clear C, set Z
        modcz   _set, _set  wcz ' Set both flags
:::

MODCZ accepts two operands specifying operations for C and Z respectively. The WC, WZ, or WCZ effect must be specified for the flags to be modified. Modifier constants include `_clr` (clear to 0), `_set` (set to 1), `_nc` (inverted C), `_nz` (inverted Z), and others that enable complex flag manipulation in a single instruction.

### 3.6.2 Flag-Based Bit Manipulation

The MUX family of instructions uses flag values to conditionally modify individual bits:

::: pasm2
        muxc    value, #mask    ' C=1: set bits; C=0: clear bits
        muxnc   value, #mask    ' C=0: set bits; C=1: clear bits
        muxz    value, #mask    ' Z=1: set bits; Z=0: clear bits
        muxnz   value, #mask    ' Z=0: set bits; Z=1: clear bits
:::

These instructions conditionally set or clear bits based on flag values. For example, MUXC sets the masked bits if C=1, or clears them if C=0. This enables building up bit patterns based on multiple flag tests:

::: pasm2
        test    input, #BIT0    wc      ' Test bit 0 of input
        muxc    output, #%0001          ' Copy bit 0 to output bit 0
        test    input, #BIT1    wc      ' Test bit 1 of input
        muxc    output, #%0010          ' Copy bit 1 to output bit 1
:::

This pattern extracts and repositions bits based on flag tests, enabling bit-field manipulation.

### 3.6.3 Flag Preservation Patterns

Sometimes you need to preserve flag values across operations that might modify them. The P2 does not provide a dedicated flag save/restore mechanism, but you can use register operations:

::: pasm2
        ' Save flags
        wrc     temp            ' Write C to temp[0]
        wrz     temp            ' Write Z to temp[1]

        ' ... operations that modify flags ...

        ' Restore flags
        testb   temp, #0        wc      ' Read temp[0] into C
        testb   temp, #1        wz      ' Read temp[1] into Z
:::

The WRC instruction writes C to the specified bit of a register (typically bit 0), and WRZ writes Z to a specified bit (typically bit 1). TESTB tests a specific bit and sets C or Z accordingly, effectively restoring the saved flag values.

An alternative approach uses MODCZ with computed values, but the TESTB pattern is more common and more readable.

### 3.6.4 Flag-Driven State Machines

Flags can encode state transitions in compact state machines. Instead of comparing state variables and branching, use flags to select the next state:

::: pasm2
                ' Current state determines which flags are set
                test    state, #STATE_IDLE      wz
        if_z    jmp     #handle_idle
                test    state, #STATE_ACTIVE    wz
        if_z    jmp     #handle_active
                test    state, #STATE_DONE      wz
        if_z    jmp     #handle_done
:::

This pattern tests state bits and branches to handlers. Each TEST sets Z if the state bit is set, and the conditional jump executes for that state. While this uses jumps (not purely branchless), it demonstrates using flags to encode complex state without comparison operations.


## 3.7 Multi-Long Arithmetic Operations

The P2's flag system enables arithmetic operations on values wider than 32 bits. By chaining instructions that propagate carry/borrow through the C flag and accumulate zero-detection through the Z flag, you can perform addition, subtraction, and comparison on 64-bit, 96-bit, 128-bit, or arbitrarily wide values.

### 3.7.1 Instruction Family Overview

The P2 provides four variants each for ADD, SUB, and CMP operations:

**Addition Instructions:**

| Instruction | Operation | C Flag | Z Flag |
|-------------|-----------|--------|--------|
| ADD D, S | D = D + S | Carry out | D result == 0 |
| ADDX D, S | D = D + S + C | Carry out | Z AND (D result == 0) |
| ADDS D, S | D = D + S | True sign of result | D result == 0 |
| ADDSX D, S | D = D + S + C | True sign of result | Z AND (D result == 0) |

**Subtraction Instructions:**

| Instruction | Operation | C Flag | Z Flag |
|-------------|-----------|--------|--------|
| SUB D, S | D = D - S | Borrow | D result == 0 |
| SUBX D, S | D = D - S - C | Borrow | Z AND (D result == 0) |
| SUBS D, S | D = D - S | True sign of result | D result == 0 |
| SUBSX D, S | D = D - S - C | True sign of result | Z AND (D result == 0) |

**Comparison Instructions:**

| Instruction | Operation | C Flag | Z Flag |
|-------------|-----------|--------|--------|
| CMP D, S | X = D - S | Borrow | X == 0 |
| CMPX D, S | X = D - S - C | Borrow | Z AND (X == 0) |
| CMPS D, S | X = D - S | True sign of X | X == 0 |
| CMPSX D, S | X = D - S - C | True sign of X | Z AND (X == 0) |

The key distinctions:

- **Base instructions** (ADD, SUB, CMP) start a new operation and reset Z
- **X variants** (ADDX, SUBX, CMPX) propagate carry/borrow and AND the zero result
- **S variants** (ADDS, SUBS, CMPS) report the true sign instead of carry
- **SX variants** (ADDSX, SUBSX, CMPSX) combine both: propagate C, AND-accumulate Z, report true sign

### 3.7.2 The Chaining Pattern

Multi-long operations follow a consistent pattern:

1. **First long:** Use base instruction (ADD, SUB, CMP) with WCZ
2. **Middle longs:** Use X variant (ADDX, SUBX, CMPX) with WCZ
3. **Final long:** Use X variant for unsigned, SX variant for signed

The X variants are critical because they:

- Add/subtract the incoming C flag (carry/borrow from previous long)
- AND the Z result with the previous Z (tracking if all longs are zero)
- Output carry/borrow for the next long

### 3.7.3 Unsigned Multi-Long Examples

**64-bit unsigned addition** (A = A + B):

::: pasm2
        ADD     A0, B0    WCZ     ' Add low longs, C = carry, Z = (A0 == 0)
        ADDX    A1, B1    WCZ     ' Add high longs + carry, C = carry,
                                  '  Z = Z AND (A1 == 0)
        ' After: C = overflow, Z = (entire 64-bit result == 0)
:::

**128-bit unsigned addition** (A = A + B):

::: pasm2
        ADD     A0, B0    WCZ     ' A0 = A0 + B0
        ADDX    A1, B1    WCZ     ' A1 = A1 + B1 + carry
        ADDX    A2, B2    WCZ     ' A2 = A2 + B2 + carry
        ADDX    A3, B3    WCZ     ' A3 = A3 + B3 + carry
        ' After: C = overflow beyond 128 bits, Z = (entire 128-bit result == 0)
:::

**64-bit unsigned subtraction** (A = A - B):

::: pasm2
        SUB     A0, B0    WCZ     ' Subtract low longs, C = borrow
        SUBX    A1, B1    WCZ     ' Subtract high longs - borrow
        ' After: C = underflow (B > A), Z = (result == 0)
:::

**64-bit unsigned comparison** (compare A to B):

::: pasm2
        CMP     A0, B0    WCZ     ' Compare low longs
        CMPX    A1, B1    WCZ     ' Compare high longs with borrow
        ' After: C = (A < B), Z = (A == B)
        ' Use IF_B (below) or IF_AE (above/equal) for unsigned branches
:::

### 3.7.4 Signed Multi-Long Examples

For signed operations, the final instruction must be an SX variant to correctly report the sign of the overall result.

**64-bit signed addition** (A = A + B):

::: pasm2
        ADD     A0, B0    WCZ     ' Add low longs (unsigned, generates carry)
        ADDSX   A1, B1    WCZ     ' Add high longs + carry, C = true sign
        ' After: C = true sign of result (1 = negative), Z = (result == 0)
:::

**128-bit signed addition** (A = A + B):

::: pasm2
        ADD     A0, B0    WCZ     ' Unsigned add for low long
        ADDX    A1, B1    WCZ     ' Unsigned add + carry for middle longs
        ADDX    A2, B2    WCZ     ' Unsigned add + carry
        ADDSX   A3, B3    WCZ     ' Signed add for high long, C = true sign
        ' After: C = 1 if result is negative, Z = (result == 0)
:::

**64-bit signed comparison** (compare A to B):

::: pasm2
        CMP     A0, B0    WCZ     ' Compare low longs
        CMPSX   A1, B1    WCZ     ' Compare high, C = sign of difference
        ' After: C = (A < B) signed, Z = (A == B)
        ' Use IF_LT (less than) or IF_GE (greater/equal) for signed branches
:::

### 3.7.5 Understanding "True Sign"

The S and SX variants report the "true sign" of the result rather than carry/borrow. This is the conceptual bit above the MSB—the sign the result would have if computed with infinite precision.

For signed operations:

- If the result is negative (would be negative with more bits), C = 1
- If the result is non-negative, C = 0

This differs from carry/borrow, which indicates overflow in unsigned arithmetic. For signed comparisons, the true sign tells you the sign of (A - B), directly indicating whether A < B.

### 3.7.6 Practical Pattern Summary

| Operation | First Long | Middle Longs | Final Long (Unsigned) | Final Long (Signed) |
|-----------|------------|--------------|----------------------|---------------------|
| Add | ADD WCZ | ADDX WCZ | ADDX WCZ | ADDSX WCZ |
| Subtract | SUB WCZ | SUBX WCZ | SUBX WCZ | SUBSX WCZ |
| Compare | CMP WCZ | CMPX WCZ | CMPX WCZ | CMPSX WCZ |

After a multi-long comparison:

- **Magnitude terminology:** IF_B (below), IF_AE (above/equal), IF_A (above), IF_BE (below/equal)
- **Arithmetic terminology:** IF_LT (less than), IF_GE (greater/equal), IF_GT (greater), IF_LE (less/equal)
- **Equality (either style):** IF_Z (equal), IF_NZ (not equal)

Both terminology styles encode to identical condition codes—choose whichever reads best for your code. The choice of CMP vs. CMPS (not the alias style) determines whether values are compared as unsigned or signed.


```{=latex}
\begin{keyconcepts}
\item The C flag indicates carry, borrow, bit shifted out, or parity depending on instruction category
\item The Z flag indicates a zero result or equality across nearly all instructions
\item Flags persist until explicitly modified—instructions without WC/WZ/WCZ preserve flag values
\item WC, WZ, and WCZ effects control which flags are updated; the operation always executes
\item Special effects ANDC/ANDZ/ORC/ORZ/XORC/XORZ combine tested bits with existing flags (TESTx instructions only)
\item Any instruction can be conditional using IF_x prefixes for deterministic branchless programming
\item 16 conditions cover all combinations of C and Z states, with comparison-friendly aliases
\item Conditional instructions consume 2 clock cycles whether they execute or not, maintaining deterministic timing
\item Multi-precision arithmetic chains flag results between instructions using ADDX and SUBX
\item Flag-based bit manipulation (MUXC, MUXZ) enables building bit patterns from sequential flag tests
\item Each COG maintains independent C and Z flags with no cross-COG interaction
\end{keyconcepts}
```


<!-- End of Chapter 3 -->

