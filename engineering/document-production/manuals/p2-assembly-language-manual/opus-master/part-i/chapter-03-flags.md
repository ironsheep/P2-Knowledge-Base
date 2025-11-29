# Chapter 3: Flags and Conditional Execution

<!-- Chapter covering C and Z flags, WC/WZ/WCZ effects, and IF_x conditions -->

The P2 has two status flags that enable conditional execution and multi-precision arithmetic. Understanding flag behavior is essential for writing efficient, branching-free code.

The P2's flag system differs from many processors in two important ways. First, flags persist until explicitly modified—an instruction without WC or WZ effects leaves flags unchanged, allowing flag values to be used by multiple subsequent instructions. Second, any instruction can be made conditional using IF_x prefixes, enabling deterministic branchless programming where instruction timing remains constant regardless of data values.

These two features combine to create a powerful programming model where complex decision logic can be expressed without branches, maintaining cycle-accurate timing while reducing code size and improving readability.

---

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

```pasm
        cmp     a, b            wc wz   ' Set flags once
        if_c    mov   min, a            ' Use C here
        if_nc   mov   min, b            ' And here
        if_z    mov   equal, #1         ' And use Z here
```

In this example, one comparison sets both flags, and three subsequent instructions each test the preserved flag values. No instruction between them modifies the flags, so the flag state from the comparison remains available.

Each COG maintains its own C and Z flags completely independently. Flag values in COG 0 have no relationship to flag values in COG 1. This independence ensures parallel execution across COGs operates without interference.

---

## 3.2 Flag Modification Effects

Every instruction can optionally specify which flags to update using effect modifiers. These modifiers—WC, WZ, and WCZ—control whether the instruction modifies the C flag, the Z flag, both flags, or neither flag. The operation always executes; effects only determine whether flags are updated.

### 3.2.1 The WC Effect

```pasm
        add     result, value   wc      ' Update C flag based on carry
```

When WC (Write C) is specified, the instruction updates the C flag according to its specific C condition while leaving Z unchanged. For ADD, this means C is set if the addition produces a carry out of bit 31. For CMP, this means C is set if the first operand is less than the second. Each instruction defines its own C condition as documented in the instruction reference.

The key insight: WC means "update C according to this instruction's C rule." The rule varies by instruction, but the WC effect itself is consistent—it enables C modification.

### 3.2.2 The WZ Effect

```pasm
        add     result, value   wz      ' Update Z flag based on result
```

When WZ (Write Z) is specified, the instruction updates the Z flag based on whether the result equals zero, while leaving C unchanged. Z=1 indicates a zero result; Z=0 indicates a non-zero result. This behavior is consistent across nearly all instructions—the Z flag always reflects "is the result zero?"

This consistency makes WZ predictable. After any arithmetic, logical, or shift operation with WZ, checking IF_Z tests whether the result was zero. After a comparison with WZ, checking IF_Z tests whether the operands were equal.

### 3.2.3 The WCZ Effect

```pasm
        add     result, value   wcz     ' Update both flags
```

When WCZ (Write C and Z) is specified, both flags are updated according to their respective conditions. This is exactly equivalent to specifying both WC and WZ, but requires less typing and produces more readable code.

WCZ is common after comparisons where both the ordering (C) and equality (Z) matter, or after arithmetic operations where both carry detection and zero detection are needed.

### 3.2.4 No Effect (Default)

```pasm
        add     result, value           ' Execute operation, preserve flags
```

When no effect is specified, the instruction executes normally but leaves both C and Z unchanged. This is not a "do nothing" mode—the operation completes, the destination is written, and timing is identical to the flagged version. Only the flags are preserved.

This behavior enables using flag values across multiple instructions without interference:

```pasm
        cmp     a, b            wc      ' Set C based on comparison
        mov     temp, c                 ' Does not modify C
        add     temp, d                 ' Does not modify C
        if_c    mov   result, temp      ' Still tests original C value
```

The comparison sets C, and two subsequent operations execute without modifying it. The conditional instruction tests the comparison result even though two operations occurred in between.

---

## 3.3 Conditional Execution

The P2 allows any instruction to execute conditionally based on the current flag values. This conditional execution mechanism enables branchless programming—expressing decision logic without jump instructions—which maintains deterministic timing and often reduces code size.

### 3.3.1 The IF_x Prefix

Any instruction can be made conditional by prefixing with an IF_x condition. When the condition is false, the instruction does not execute, but still consumes its normal execution time (typically one clock cycle). When the condition is true, the instruction executes normally:

```pasm
        cmp     a, b            wc wz   ' Compare, set flags
        if_z    mov   result, #1        ' Execute only if Z=1 (equal)
        if_nz   mov   result, #0        ' Execute only if Z=0 (not equal)
```

This three-instruction sequence sets `result` to 1 if `a` equals `b`, or 0 if they differ. It takes exactly three clock cycles regardless of the comparison result. The unconditional CMP always executes, then exactly one of the two conditional MOVs executes.

The timing predictability is crucial. Traditional branch-based code has variable timing depending on which path is taken. Conditional execution eliminates this variation—the instruction stream is fixed, and timing is constant.

### 3.3.2 Conditional Execution Timing

When a conditional instruction's condition is false, the instruction does not execute but still consumes one clock cycle. This behavior might seem wasteful, but it provides deterministic timing—critical for real-time operations, protocol timing, and cycle-accurate code.

Consider this example:

```pasm
        test    flags, #BIT_READY  wz          ' Check ready bit
        if_nz   rdlong  data, ptr               ' Read if ready
        if_nz   add     ptr, #4                 ' Advance pointer if read occurred
```

This sequence takes exactly three clock cycles whether the ready bit is set or clear. If implementing the same logic with branches:

```pasm
        test    flags, #BIT_READY  wz
        if_z    jmp     #skip
        rdlong  data, ptr
        add     ptr, #4
skip:
```

The branch version takes 2 cycles when not ready (test + jump) or 4 cycles when ready (test + not-jump + rdlong + add). The timing varies by 100%. The conditional version maintains constant 3-cycle timing.

For real-time code, deterministic timing often matters more than average speed.

### 3.3.3 Complete Condition Table

The P2 provides sixteen conditions that cover all possible combinations of the C and Z flag states, plus two special cases (always and never). Many conditions have multiple names—aliases that make code more readable in different contexts:

| Condition | Aliases | C | Z | True When |
|-----------|---------|---|---|-----------|
| IF_ALWAYS | (none) | * | * | Always executes (unconditional) |
| IF_NEVER | (none) | - | - | Never executes (acts as NOP) |
| IF_C | IF_B | 1 | * | C = 1 (carry set, below) |
| IF_NC | IF_AE, IF_NB | 0 | * | C = 0 (no carry, above or equal) |
| IF_Z | IF_E | * | 1 | Z = 1 (zero, equal) |
| IF_NZ | IF_NE | * | 0 | Z = 0 (not zero, not equal) |
| IF_C_AND_Z | IF_BE | 1 | 1 | C = 1 AND Z = 1 (below or equal) |
| IF_C_AND_NZ | (none) | 1 | 0 | C = 1 AND Z = 0 |
| IF_NC_AND_Z | (none) | 0 | 1 | C = 0 AND Z = 1 |
| IF_NC_AND_NZ | IF_A, IF_NE | 0 | 0 | C = 0 AND Z = 0 (above) |
| IF_C_OR_Z | (none) | 1 or * | * or 1 | C = 1 OR Z = 1 |
| IF_C_OR_NZ | (none) | 1 or * | 0 or * | C = 1 OR Z = 0 |
| IF_NC_OR_Z | (none) | 0 or * | * or 1 | C = 0 OR Z = 1 |
| IF_NC_OR_NZ | (none) | 0 or * | 0 or * | C = 0 OR Z = 0 |
| IF_C_EQ_Z | (none) | same | same | C equals Z (both 0 or both 1) |
| IF_C_NE_Z | (none) | diff | diff | C differs from Z (one 0, one 1) |

The asterisk (*) in the C or Z column means "don't care"—the condition is true regardless of that flag's value. For OR conditions, the notation "1 or *" means C=1 makes the condition true regardless of Z, or Z matching the specified pattern makes it true regardless of C.

### 3.3.4 Comparison Condition Aliases

After a comparison instruction, certain IF_x conditions correspond to familiar relational operators. The aliases make comparison-based conditionals read naturally:

**Unsigned Comparisons (CMP)**

After `CMP a, b WC WZ`, the flags indicate the relationship between unsigned values:

| Condition | Alias | Relational Operator | Meaning |
|-----------|-------|---------------------|---------|
| IF_C | IF_B | < | a is below (less than) b |
| IF_NC | IF_AE | >= | a is above or equal to b |
| IF_Z | IF_E | == | a equals b |
| IF_NZ | IF_NE | != | a not equal to b |
| IF_NC_AND_NZ | IF_A | > | a is above (greater than) b |
| IF_C_OR_Z | IF_BE | <= | a is below or equal to b |

The aliases IF_B (below), IF_AE (above or equal), IF_BE (below or equal), and IF_A (above) correspond exactly to unsigned relational operators. After comparing two unsigned values, these aliases express the intended test clearly.

**Signed Comparisons (CMPS)**

After `CMPS a, b WC WZ`, the same condition names apply but with signed interpretation:

| Condition | Relational Operator | Meaning |
|-----------|---------------------|---------|
| IF_C | < | a is less than b (signed) |
| IF_NC | >= | a is greater or equal to b (signed) |
| IF_Z | == | a equals b |
| IF_NZ | != | a not equal to b |
| IF_NC_AND_NZ | > | a is greater than b (signed) |
| IF_C_OR_Z | <= | a is less or equal to b (signed) |

The conditions are identical, but the comparison instruction (CMP vs. CMPS) determines whether the interpretation is unsigned or signed. Equality (IF_Z) and inequality (IF_NZ) work identically for both—the bit patterns either match or they don't.

---

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

---

## 3.5 Common Flag Patterns

Understanding common flag usage patterns accelerates learning and provides templates for solving typical programming problems. These patterns demonstrate how flags enable elegant, efficient solutions.

### 3.5.1 Testing a Bit

Testing whether a specific bit is set uses TEST with WZ:

```pasm
        test    value, #%00000100  wz   ' Test bit 2
        if_nz   jmp     #bit_set        ' Jump if bit is set
```

TEST performs a bitwise AND of its operands but writes the result nowhere—it only sets flags. The mask `%00000100` isolates bit 2. If bit 2 is set, the AND produces a non-zero result (specifically, the value 4), so Z=0. If bit 2 is clear, the AND produces zero, so Z=1.

The condition IF_NZ tests "not zero," which corresponds to "bit is set." This pattern works for testing any single bit or combination of bits—just construct the appropriate mask.

### 3.5.2 Multi-Precision Addition

Adding values wider than 32 bits requires propagating the carry between word additions:

```pasm
        add     x_lo, y_lo      wc      ' Add low words, capture carry
        addx    x_hi, y_hi              ' Add high words plus carry
```

The first ADD adds the low 32 bits and sets C if the addition carries out. The ADDX instruction (Add with Carry) adds the high 32 bits plus the carry from the first addition. This extends to any number of words:

```pasm
        add     x0, y0          wc      ' Add word 0
        addx    x1, y1          wc      ' Add word 1 plus carry
        addx    x2, y2          wc      ' Add word 2 plus carry
        addx    x3, y3                  ' Add word 3 plus carry
```

Each ADDX uses the carry from the previous addition and generates a new carry for the next addition. The result is 128-bit (4 × 32-bit) addition with correct carry propagation.

### 3.5.3 Conditional Assignment

Selecting between two values based on a comparison uses conditional moves:

```pasm
        cmp     a, b            wc      ' Compare a and b
        if_c    mov   result, a         ' If a < b, result = a
        if_nc   mov   result, b         ' If a >= b, result = b
```

This implements `result = min(a, b)` without branches. The comparison sets C if `a < b` (unsigned). Exactly one of the two conditional moves executes, storing the smaller value in result. The sequence takes exactly three clock cycles regardless of which value is smaller.

For maximum of two values, invert the conditions:

```pasm
        cmp     a, b            wc      ' Compare a and b
        if_c    mov   result, b         ' If a < b, result = b
        if_nc   mov   result, a         ' If a >= b, result = a
```

### 3.5.4 Branchless Absolute Value

Computing the absolute value of a signed number uses the ABS instruction with conditional negation:

```pasm
        abs     result, value   wc      ' Get absolute value, C = was negative
        if_c    neg   result            ' Correct if value was negative
```

Wait—this looks wrong. If ABS already computes the absolute value, why negate it afterward?

The issue is a quirk of two's complement: the most negative value (-2,147,483,648 or $8000_0000) has no positive representation in 32 bits. Its absolute value cannot be represented. The ABS instruction handles this by leaving the value unchanged and setting C to indicate the exceptional case.

For all other negative values, ABS correctly computes the absolute value and clears C. For -2,147,483,648, ABS leaves it unchanged and sets C, and the conditional NEG negates it back to itself (since negating $8000_0000 produces $8000_0000).

Most code doesn't care about this edge case and can simply use `ABS result, value` without the conditional correction.

### 3.5.5 Conditional Increment/Decrement

Updating a counter only when a condition is met uses conditional arithmetic:

```pasm
        test    flags, #FLAG_READY  wz  ' Test ready flag
        if_nz   add   count, #1         ' Increment if ready
```

This increments `count` only when the ready flag is set. No branches are needed, and timing is deterministic—two clock cycles regardless of flag state.

### 3.5.6 Bounds Checking

Checking whether a value falls within a range combines comparison and logical conditions:

```pasm
        cmp     value, min      wc      ' Check if value < min
        if_c    jmp   #out_of_range     ' Too small
        cmp     value, max      wc      ' Check if value >= max
        if_nc   jmp   #out_of_range     ' Too large
        ' Value is in range [min, max)
```

This checks whether `value` is in the range [min, max). The first comparison tests for too small; the second tests for too large. If either condition fails, the value is out of range.

---

## 3.6 Advanced Flag Usage

Beyond basic conditional execution, the P2 provides specialized instructions for manipulating flags directly and using flags to control data flow. These advanced techniques enable sophisticated flag-based algorithms.

### 3.6.1 Direct Flag Manipulation

The MODC and MODZ instructions modify flags directly without performing computations:

```pasm
        modc    #1              ' Set C flag to 1
        modz    #0              ' Clear Z flag to 0
```

MODC sets C to the specified bit value (0 or 1), and MODZ sets Z to the specified bit value. These instructions are useful when you need to establish specific flag states for subsequent conditional operations, or when implementing custom flag-based protocols.

The MODCZ instruction can modify both flags simultaneously with more complex rules:

```pasm
        modcz   _clr, _set      ' Clear C, set Z
        modcz   _set, _set      ' Set both flags
```

MODCZ accepts operands that specify operations: `_clr` (clear to 0), `_set` (set to 1), `_nc` (copy from C inverted), `_nz` (copy from Z inverted), and others. This enables complex flag manipulation in a single instruction.

### 3.6.2 Flag-Based Bit Manipulation

The MUX family of instructions uses flag values to conditionally modify individual bits:

```pasm
        muxc    value, #mask    ' If C=1, OR value with mask; if C=0, AND value with NOT mask
        muxnc   value, #mask    ' If C=0, OR value with mask; if C=1, AND value with NOT mask
        muxz    value, #mask    ' If Z=1, OR value with mask; if Z=0, AND value with NOT mask
        muxnz   value, #mask    ' If Z=0, OR value with mask; if Z=1, AND value with NOT mask
```

These instructions conditionally set or clear bits based on flag values. For example, MUXC sets the masked bits if C=1, or clears them if C=0. This enables building up bit patterns based on multiple flag tests:

```pasm
        test    input, #BIT0    wc      ' Test bit 0 of input
        muxc    output, #%0001          ' Copy bit 0 to output bit 0
        test    input, #BIT1    wc      ' Test bit 1 of input
        muxc    output, #%0010          ' Copy bit 1 to output bit 1
```

This pattern extracts and repositions bits based on flag tests, enabling bit-field manipulation.

### 3.6.3 Flag Preservation Patterns

Sometimes you need to preserve flag values across operations that might modify them. The P2 does not provide a dedicated flag save/restore mechanism, but you can use register operations:

```pasm
        ' Save flags
        wrc     temp            ' Write C to temp[0]
        wrz     temp            ' Write Z to temp[1]

        ' ... operations that modify flags ...

        ' Restore flags
        testb   temp, #0        wc      ' Read temp[0] into C
        testb   temp, #1        wz      ' Read temp[1] into Z
```

The WRC instruction writes C to the specified bit of a register (typically bit 0), and WRZ writes Z to a specified bit (typically bit 1). TESTB tests a specific bit and sets C or Z accordingly, effectively restoring the saved flag values.

An alternative approach uses MODCZ with computed values, but the TESTB pattern is more common and more readable.

### 3.6.4 Flag-Driven State Machines

Flags can encode state transitions in compact state machines. Instead of comparing state variables and branching, use flags to select the next state:

```pasm
        ' Current state determines which flags are set
        test    state, #STATE_IDLE      wz
        if_z    jmp     #handle_idle
        test    state, #STATE_ACTIVE    wz
        if_z    jmp     #handle_active
        test    state, #STATE_DONE      wz
        if_z    jmp     #handle_done
```

This pattern tests state bits and branches to handlers. Each TEST sets Z if the state bit is set, and the conditional jump executes for that state. While this uses jumps (not purely branchless), it demonstrates using flags to encode complex state without comparison operations.

---

## Key Concepts

```{=latex}
\begin{keyconcepts}
\item The C flag indicates carry, borrow, bit shifted out, or parity depending on instruction category
\item The Z flag indicates a zero result or equality across nearly all instructions
\item Flags persist until explicitly modified—instructions without WC/WZ/WCZ preserve flag values
\item WC, WZ, and WCZ effects control which flags are updated; the operation always executes
\item Any instruction can be conditional using IF\_x prefixes for deterministic branchless programming
\item 16 conditions cover all combinations of C and Z states, with comparison-friendly aliases
\item Conditional instructions consume one clock cycle whether they execute or not, maintaining deterministic timing
\item Multi-precision arithmetic chains flag results between instructions using ADDX and SUBX
\item Flag-based bit manipulation (MUXC, MUXZ) enables building bit patterns from sequential flag tests
\item Each COG maintains independent C and Z flags with no cross-COG interaction
\end{keyconcepts}
```

---

<!-- End of Chapter 3 -->
