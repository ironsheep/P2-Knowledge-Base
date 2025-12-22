# WC, WZ, and WCZ Effects Guide for PASM2

This document provides a comprehensive explanation of the WC, WZ, and WCZ instruction effects in PASM2, including what they mean, why all three exist, how they are encoded, and practical usage patterns.

---

## Table of Contents

1. [Overview: What Are C and Z?](#1-overview-what-are-c-and-z)
2. [The Effect Modifiers](#2-the-effect-modifiers)
3. [Encoding Details](#3-encoding-details)
4. [Why Three Separate Effects?](#4-why-three-separate-effects)
5. [What Sets C and Z](#5-what-sets-c-and-z)
6. [Using C and Z in Conditional Execution](#6-using-c-and-z-in-conditional-execution)
7. [Instruction Support for Effects](#7-instruction-support-for-effects)
8. [Extended Effects (ANDC, ANDZ, etc.)](#8-extended-effects-andc-andz-etc)
9. [Practical Examples](#9-practical-examples)
10. [Common Patterns](#10-common-patterns)
11. [Best Practices](#11-best-practices)

---

## Quick Reference: Effect Support by Instruction Category

| Category | Allowed Effects | Instructions |
|----------|----------------|--------------|
| **Most ALU ops** | WC, WZ, WCZ | ADD, SUB, CMP, AND, OR, XOR, MOV, SHL, SHR, etc. |
| **WCZ-only (40)** | WCZ only | BIT*, DIR*, DRV*, FLT*, OUT* |
| **WC-only (9)** | WC only | COGID, COGINIT, GETCT, LOCKNEW, LOCKREL, LOCKTRY, MODC, RDPIN, RQPIN |
| **WZ-only (5)** | WZ only | MODZ, MUL, MULS, SCA, SCAS |
| **Extended (4)** | WC, WZ, ANDC, ANDZ, ORC, ORZ, XORC, XORZ (no WCZ) | TESTP, TESTPN, TESTB, TESTBN |

**Important**: You cannot write `WC WZ` as separate tokens. Use `WCZ` to update both flags.

---

## 1. Overview: What Are C and Z?

The Propeller 2 has two status flags that can be modified by instructions and used for conditional execution:

### The C Flag (Carry)

The **C flag** (Carry) is a single-bit status flag that typically indicates:
- **Arithmetic overflow/underflow**: Set when an addition overflows or subtraction underflows
- **Bit shifted out**: Set to the bit that was shifted out during shift/rotate operations
- **Comparison result**: Set based on unsigned comparison (below/above)
- **Pin state**: Set to reflect a pin's input state
- **MSB/LSB**: Set to the most or least significant bit of a result

### The Z Flag (Zero)

The **Z flag** (Zero) is a single-bit status flag that typically indicates:
- **Zero result**: Set when an operation produces a zero result
- **Equality**: Set when two values are equal
- **All bits clear**: Set when all tested bits are zero
- **Pin state**: Can reflect a pin's state (with certain instructions)

### Flag Persistence

**Critical concept**: The C and Z flags **retain their values** between instructions. They only change when an instruction explicitly modifies them using WC, WZ, or WCZ. This persistence is what makes conditional execution possible.

```spin2
        ADD     x, y    WC          ' C is updated, Z unchanged
        SUB     a, b                ' Neither C nor Z changed
        MOV     temp, x WZ          ' Z is updated, C still from ADD above
        if_c    JMP     #somewhere  ' Uses C flag from ADD (not SUB or MOV)
```

---

## 2. The Effect Modifiers

### WC - Write Carry

**WC** tells the instruction to update the C flag based on the instruction's result.

```spin2
        ADD     x, #100     WC      ' Update C flag (set if overflow)
        SHL     value, #1   WC      ' Update C flag (set to bit shifted out)
        CMP     a, b        WC      ' Update C flag (set if a < b unsigned)
```

### WZ - Write Zero

**WZ** tells the instruction to update the Z flag based on the instruction's result.

```spin2
        ADD     x, #100     WZ      ' Update Z flag (set if result is 0)
        MOV     value, x    WZ      ' Update Z flag (set if value is 0)
        AND     a, b        WZ      ' Update Z flag (set if result is 0)
```

### WCZ - Write Carry and Zero

**WCZ** tells the instruction to update **both** C and Z flags based on the instruction's result.

```spin2
        ADD     x, #100     WCZ     ' Update both C and Z flags
        SUB     a, b        WCZ     ' Update both C and Z flags
```

### WCZ = WC + WZ (But You Cannot Write Both Separately)

**WCZ is exactly equivalent to specifying both WC and WZ together.** It's a convenience shorthand:

| Effect | C Updated? | Z Updated? | Binary Encoding |
|--------|------------|------------|-----------------|
| (none) | No | No | `00` |
| WZ | No | **Yes** | `01` |
| WC | **Yes** | No | `10` |
| WCZ | **Yes** | **Yes** | `11` |

**Important**: You cannot write `WC WZ` as separate tokens on the same instruction. The parser treats effects as single tokens. If you need both flags updated, you **must** use `WCZ`:

```spin2
        ADD     x, y    WC WZ   ' ERROR - invalid syntax!
        ADD     x, y    WCZ     ' Correct - updates both flags
```

---

## 3. Encoding Details

### Instruction Format

Effects are encoded in bits [20:19] of the 32-bit instruction word:

```
Bit 20 = WC (Write Carry)
Bit 19 = WZ (Write Zero)

[20:19] = 00  →  No effect (flags unchanged)
[20:19] = 01  →  WZ only
[20:19] = 10  →  WC only
[20:19] = 11  →  WCZ (both)
```

### Compiler Implementation

From the PNut-TS compiler (`parseUtils.ts`):

```typescript
// Effect encoding values
WC  = 0b0010  // Bit 1 set → WC
WZ  = 0b0001  // Bit 0 set → WZ
WCZ = 0b0011  // Bits 0 and 1 set → WC + WZ
```

When the compiler processes an effect, it ORs the effect value shifted left by 19 bits into the instruction:

```typescript
// From spinResolver.ts
this.instructionImage |= attemptedEffects << 19;
```

---

## 4. Why Three Separate Effects?

### Independent Flag Control

Having separate WC and WZ effects provides **fine-grained control** over which flags are modified. This is essential for several reasons:

#### 1. Flag Preservation Across Operations

You may need to preserve one flag while updating another:

```spin2
        CMP     a, b        WC      ' Set C based on comparison
        ' ... other code that must not change C ...
        MOV     temp, x     WZ      ' Set Z based on value, preserve C
        if_c_and_z  JMP #special    ' Use BOTH flags together
```

#### 2. Separate Condition Testing

Different flags often represent different conditions:

```spin2
        SUB     count, #1   WCZ     ' Update both flags
        if_z    JMP #done           ' If count reached zero
        if_c    JMP #underflow      ' If count went negative (unsigned)
```

#### 3. Efficiency - Only Update What You Need

Updating flags has no performance cost, but choosing which flags to update makes your code's intent clearer:

```spin2
        ' We only care about zero/non-zero
        MOV     value, x    WZ
        if_z    JMP #is_zero

        ' We only care about carry (overflow)
        ADD     sum, delta  WC
        if_c    JMP #overflow
```

#### 4. Complex Conditional Logic

The P2 supports 16 different conditions based on C and Z combinations. Having independent control lets you build complex conditions:

```spin2
        CMP     x, #10      WC      ' C=1 if x < 10 (unsigned)
        CMP     y, #20      WZ      ' Z=1 if y == 20
        if_c_and_z  ...             ' Execute if x<10 AND y==20
```

---

## 5. What Sets C and Z

Different instructions set C and Z to different values. Here's a comprehensive reference:

### Arithmetic Instructions

| Instruction | C Flag | Z Flag |
|-------------|--------|--------|
| `ADD D,S` | Unsigned overflow (carry out) | Result is zero |
| `ADDX D,S` | Unsigned overflow with carry | Result is zero |
| `ADDS D,S` | Signed overflow | Result is zero |
| `ADDSX D,S` | Signed overflow with carry | Result is zero |
| `SUB D,S` | Unsigned underflow (borrow) | Result is zero |
| `SUBX D,S` | Unsigned underflow with borrow | Result is zero |
| `SUBS D,S` | Signed overflow | Result is zero |
| `SUBSX D,S` | Signed overflow with borrow | Result is zero |

### Comparison Instructions

| Instruction | C Flag | Z Flag |
|-------------|--------|--------|
| `CMP D,S` | D < S (unsigned) | D == S |
| `CMPS D,S` | D < S (signed) | D == S |
| `CMPX D,S` | D < S (unsigned, extended) | D == S (extended) |
| `CMPSX D,S` | D < S (signed, extended) | D == S (extended) |
| `CMPR D,S` | D < S (reversed) | D == S |
| `TEST D,S` | Parity of (D AND S) | (D AND S) == 0 |

### Logical Instructions

| Instruction | C Flag | Z Flag |
|-------------|--------|--------|
| `AND D,S` | Parity of result | Result is zero |
| `OR D,S` | Parity of result | Result is zero |
| `XOR D,S` | Parity of result | Result is zero |
| `NOT D` | Parity of result | Result is zero |

### Shift/Rotate Instructions

| Instruction | C Flag | Z Flag |
|-------------|--------|--------|
| `SHL D,S` | Last bit shifted out (MSB→) | Result is zero |
| `SHR D,S` | Last bit shifted out (→LSB) | Result is zero |
| `SAR D,S` | Last bit shifted out | Result is zero |
| `ROL D,S` | Last bit rotated out | Result is zero |
| `ROR D,S` | Last bit rotated out | Result is zero |
| `RCL D,S` | MSB before rotation | Result is zero |
| `RCR D,S` | LSB before rotation | Result is zero |

### Move Instructions

| Instruction | C Flag | Z Flag |
|-------------|--------|--------|
| `MOV D,S` | S[31] (MSB of source) | S == 0 |
| `ABS D,S` | S was negative | Result is zero |
| `NEG D,S` | S was non-zero | Result is zero |

### Pin Instructions

| Instruction | C Flag | Z Flag |
|-------------|--------|--------|
| `TESTP #pin` | Pin input state | (varies by mode) |
| `TESTPN #pin` | Inverted pin input | (varies by mode) |

### Special Instructions

| Instruction | C Flag | Z Flag |
|-------------|--------|--------|
| `GETCT D` | CT[32] (bit 32 of counter) | - |
| `GETRND D` | Random bit | Random result is zero |
| `LOCKTRY #n` | Lock was acquired | - |
| `LOCKREL #n` | Lock was already free | - |

---

## 6. Using C and Z in Conditional Execution

### Condition Codes

Every PASM2 instruction can be conditionally executed based on C and Z flags:

| Condition | C | Z | Meaning | Aliases |
|-----------|---|---|---------|---------|
| `IF_ALWAYS` | X | X | Always execute | (default) |
| `IF_C` | 1 | X | Carry set | IF_B, IF_LT |
| `IF_NC` | 0 | X | Carry clear | IF_AE, IF_GE |
| `IF_Z` | X | 1 | Zero set | IF_E |
| `IF_NZ` | X | 0 | Zero clear | IF_NE |
| `IF_C_AND_Z` | 1 | 1 | Both set | IF_SAME |
| `IF_C_AND_NZ` | 1 | 0 | C set, Z clear | |
| `IF_NC_AND_Z` | 0 | 1 | C clear, Z set | |
| `IF_NC_AND_NZ` | 0 | 0 | Both clear | IF_GT, IF_A |
| `IF_C_OR_Z` | 1+ | 1+ | Either set | |
| `IF_C_OR_NZ` | 1 | 0+ | C or not Z | |
| `IF_NC_OR_Z` | 0+ | 1 | Not C or Z | IF_LE, IF_BE |
| `IF_NC_OR_NZ` | 0+ | 0+ | Either clear | |
| `IF_C_EQ_Z` | = | = | C equals Z | |
| `IF_C_NE_Z` | ≠ | ≠ | C differs from Z | IF_DIFF |

### Example: Conditional Execution

```spin2
        CMP     value, #100     WCZ     ' Compare value to 100
        if_z    MOV     result, #0      ' If equal: result = 0
        if_c    MOV     result, #-1     ' If below: result = -1
        if_nc_and_nz  MOV result, #1    ' If above: result = 1
```

---

## 7. Instruction Support for Effects

### Why WC, WZ, and WCZ Are Defined Separately in Instructions

You might wonder: **Why do instruction definitions specify allowed effects as WC, WZ, and WCZ separately? Why not just define WC and WZ permissions, with WCZ being automatically allowed when both are?**

The answer lies in the **hardware encoding** and what the flags actually mean for each instruction:

#### The Effect Permission Field

Each instruction definition includes a 2-bit **allowedEffects** field:

```
Bit 1 = WC permission (can write to C flag)
Bit 0 = WZ permission (can write to Z flag)

0b00 = Neither WC nor WZ allowed
0b01 = Only WZ allowed (C has no meaningful result)
0b10 = Only WC allowed (Z has no meaningful result)
0b11 = WC, WZ, and WCZ all allowed
```

#### Why Some Instructions Only Support WC or WZ

Some instructions only produce meaningful results for **one flag**:

| Scenario | Example | Why |
|----------|---------|-----|
| Only C meaningful | `LOCKTRY`, `COGID` | C=1 means lock acquired or cog is on; Z has no defined meaning |
| Only Z meaningful | `MUL`, `MULS` | Z=1 if either operand was zero; no carry concept |
| Neither meaningful | `NOP` | No result that relates to C or Z |
| Both meaningful | `ADD`, `CMP` | C=overflow/compare, Z=zero result |

#### WCZ Is NOT Just "WC + WZ"

While the **encoding** of WCZ (0b11) equals WC (0b10) + WZ (0b01), the **permission** to use WCZ requires that **both** individual effects are meaningful for the instruction.

The compiler validates this with:

```typescript
// From spinResolver.ts
if ((attemptedEffects & allowedEffects) == 0 ||
    (attemptedEffects == 0b11 && allowedEffects != 0b11)) {
  throw new Error('This effect is not allowed for this instruction');
}
```

This means:
- If you try `WCZ` but the instruction only allows `WZ`, you get an error
- Even though `WCZ` includes the `WZ` bit, you can't use it unless `WC` is also allowed

#### Practical Example

Consider a hypothetical instruction that only produces a meaningful carry:

```spin2
        SOMEOP  D, S    WC      ' OK - C has meaning
        SOMEOP  D, S    WZ      ' ERROR - Z has no meaning for this instruction
        SOMEOP  D, S    WCZ     ' ERROR - WCZ requires both to be meaningful
```

This design ensures you don't accidentally request a flag update that would give you undefined/garbage values.

### Not All Instructions Support All Effects

Instructions have different effect permissions encoded in their definition:

| Permission | Binary | Meaning |
|------------|--------|---------|
| None | `00` | No effects allowed |
| WZ only | `01` | Only WZ allowed |
| WC only | `10` | Only WC allowed |
| WC/WZ/WCZ | `11` | All effects allowed |

### Instructions with Full Effect Support (WC/WZ/WCZ)

Most ALU instructions support all effects:
- `ADD`, `SUB`, `AND`, `OR`, `XOR`, `MOV`, `NOT`
- `CMP`, `CMPS`, `TEST`
- `SHL`, `SHR`, `SAR`, `ROL`, `ROR`
- `ABS`, `NEG`, `SIGNX`, `ZEROX`
- And many more...

### Instructions with Restricted Effects

Some instructions only support specific effects. The PNut-TS compiler implementation reveals several distinct categories:

#### WCZ-Only Instructions (40 instructions)

These instructions **only accept WCZ** - not WC or WZ individually. This is because for these pin/bit operations, both C and Z are set to the **same value** (the original state of the bit/pin before modification), so it doesn't make sense to update just one flag.

| Category | Instructions (8 each) |
|----------|----------------------|
| BIT* | BITL, BITH, BITC, BITNC, BITZ, BITNZ, BITRND, BITNOT |
| DIR* | DIRL, DIRH, DIRC, DIRNC, DIRZ, DIRNZ, DIRRND, DIRNOT |
| DRV* | DRVL, DRVH, DRVC, DRVNC, DRVZ, DRVNZ, DRVRND, DRVNOT |
| FLT* | FLTL, FLTH, FLTC, FLTNC, FLTZ, FLTNZ, FLTRND, FLTNOT |
| OUT* | OUTL, OUTH, OUTC, OUTNC, OUTZ, OUTNZ, OUTRND, OUTNOT |

```spin2
        DRVH    #pin        WCZ     ' Valid - C and Z both set to original OUT state
        DRVH    #pin        WC      ' ERROR: This effect is not allowed for this instruction
        DRVH    #pin        WZ      ' ERROR: This effect is not allowed for this instruction
        DRVH    #pin                ' Valid - no effect, flags unchanged
```

The compiler uses a special `tryWCZ()` function that specifically checks for WCZ (value 0b11). If you use WC or WZ alone, the standard effect validation rejects it.

#### WC Only Instructions (9 instructions)

These have `allowedEffects = 0b10` and only support WC:

| Instruction | C Flag Meaning |
|-------------|----------------|
| COGID | 1 if cog is on |
| COGINIT | 1 if no free cog |
| GETCT | CT[32] (bit 32 of counter) |
| LOCKNEW | 1 if no LOCK available |
| LOCKREL | 1 if lock was already free |
| LOCKTRY | 1 if got LOCK |
| MODC | cccc[{C,Z}] |
| RDPIN | modal result |
| RQPIN | modal result |

```spin2
        COGID   result      WC      ' Valid - C = 1 if cog is on
        COGID   result      WZ      ' ERROR: This effect is not allowed
        COGID   result      WCZ     ' ERROR: This effect is not allowed
```

#### WZ Only Instructions (5 instructions)

These have `allowedEffects = 0b01` and only support WZ:

| Instruction | Z Flag Meaning |
|-------------|----------------|
| MODZ | zzzz[{C,Z}] |
| MUL | (S == 0) \| (D == 0) |
| MULS | (S == 0) \| (D == 0) |
| SCA | result == 0 |
| SCAS | result == 0 |

```spin2
        MUL     a, b        WZ      ' Valid - Z = 1 if either operand was 0
        MUL     a, b        WC      ' ERROR: This effect is not allowed
        MUL     a, b        WCZ     ' ERROR: This effect is not allowed
```

#### Extended Effects Only - TEST* Instructions (4 instructions)

These use `getCorZ()` which supports WC, WZ, and extended effects, but **explicitly rejects WCZ**:

- TESTP, TESTPN, TESTB, TESTBN

Supported effects: WC, WZ, ANDC, ANDZ, ORC, ORZ, XORC, XORZ

```spin2
        TESTP   #pin        WC      ' Valid
        TESTP   #pin        WZ      ' Valid
        TESTP   #pin        ANDC    ' Valid - C = C AND pin_state
        TESTP   #pin        WCZ     ' ERROR: Expected WC, WZ, ANDC, ANDZ, ORC, ORZ, XORC, or XORZ
```

#### Branch Instructions (5 instructions - register mode only)

CALL, CALLA, CALLB, CALLD, JMP support all effects only when using register mode:

```spin2
        CALL    #address            ' Immediate mode - no effects supported
        CALL    reg         WCZ     ' Register mode - WC, WZ, WCZ all valid
        JMP     #label              ' Immediate mode - no effects
        JMP     reg         WC      ' Register mode - effects supported
```

### Effect Validation

The compiler checks effect permissions and produces an error if invalid:

```
"This effect is not allowed for this instruction"
```

---

## 8. Extended Effects (ANDC, ANDZ, etc.)

Beyond the basic WC/WZ/WCZ, certain instructions support **extended effects** that combine logic operations with flag updates:

### Extended Effect Table

| Effect | Encoding | Operation |
|--------|----------|-----------|
| ANDC | `0110` | C = C AND instruction_result_C |
| ANDZ | `0101` | Z = Z AND instruction_result_Z |
| ORC | `1010` | C = C OR instruction_result_C |
| ORZ | `1001` | Z = Z OR instruction_result_Z |
| XORC | `1110` | C = C XOR instruction_result_C |
| XORZ | `1101` | Z = Z XOR instruction_result_Z |

### Encoding Structure

Extended effects use a 4-bit encoding:
```
Bits [1:0] = Which flag (01=Z, 10=C)
Bits [3:2] = Logic operation (00=direct, 01=AND, 10=OR, 11=XOR)
```

### Usage with TESTP/TESTPN

The most common use is with pin test instructions:

```spin2
        ' Test multiple pins and AND the results
        TESTP   #pin0       WC      ' C = pin0 state
        TESTP   #pin1       ANDC    ' C = C AND pin1 state
        TESTP   #pin2       ANDC    ' C = C AND pin2 state
        if_c    JMP #all_high       ' Jump if ALL pins were high

        ' Test multiple pins and OR the results
        TESTP   #pin0       WC      ' C = pin0 state
        TESTP   #pin1       ORC     ' C = C OR pin1 state
        TESTP   #pin2       ORC     ' C = C OR pin2 state
        if_c    JMP #any_high       ' Jump if ANY pin was high
```

### Usage with TESTB/TESTBN

Test bits and combine results:

```spin2
        ' Check if multiple bits are set
        TESTB   flags, #0   WC      ' C = bit 0
        TESTB   flags, #4   ANDC    ' C = C AND bit 4
        TESTB   flags, #7   ANDC    ' C = C AND bit 7
        if_c    JMP #all_set        ' Jump if bits 0, 4, and 7 all set
```

---

## 9. Practical Examples

### Example 1: 64-bit Addition

```spin2
' Add two 64-bit values: [hi1:lo1] + [hi2:lo2] → [hi_r:lo_r]
        ADD     lo_r, lo2       WC      ' Add low words, save carry
        ADDX    hi_r, hi2               ' Add high words with carry
```

### Example 2: Multi-Precision Comparison

```spin2
' Compare 64-bit values: [hi1:lo1] vs [hi2:lo2]
        CMP     lo1, lo2        WCZ     ' Compare low, set both flags
        CMPX    hi1, hi2        WCZ     ' Compare high with extended
        if_c    JMP #less_than          ' [hi1:lo1] < [hi2:lo2]
        if_z    JMP #equal              ' [hi1:lo1] == [hi2:lo2]
        JMP     #greater_than           ' [hi1:lo1] > [hi2:lo2]
```

### Example 3: Loop with Counter

```spin2
' Execute loop 10 times
        MOV     count, #10
.loop
        ' ... loop body ...
        DJNZ    count, #.loop           ' Decrement and jump if not zero
        ' (DJNZ implicitly tests for zero)
```

### Example 4: Wait for Pin High

```spin2
' Wait for pin to go high
.wait   TESTP   #input_pin  WC
        if_nc   JMP #.wait              ' Loop while pin is low
```

### Example 5: Serial Bit Output

```spin2
' Shift out 8 bits, MSB first
        MOV     bits, #8
.bitloop
        SHL     data, #1        WC      ' Shift MSB into C
        DRVC    #tx_pin                 ' Drive pin to C state
        WAITX   bit_time                ' Wait one bit time
        DJNZ    bits, #.bitloop
```

### Example 6: Finding First Set Bit

```spin2
' Find position of highest set bit in value
        ENCOD   result, value   WZ      ' Encode (find MSB), set Z if value=0
        if_z    MOV result, #-1         ' Return -1 if no bits set
```

### Example 7: Conditional Value Selection

```spin2
' result = (a < b) ? x : y
        CMP     a, b            WC      ' C=1 if a < b (unsigned)
        if_c    MOV result, x
        if_nc   MOV result, y
```

### Example 8: Accumulating Pin States

```spin2
' Read 8 input pins into a byte
        MOV     result, #0
        TESTP   #pin7           WC      ' Get MSB
        RCL     result, #1              ' Shift into result
        TESTP   #pin6           WC
        RCL     result, #1
        ' ... repeat for pins 5-0 ...
```

---

## 10. Common Patterns

### Pattern 1: Test-and-Branch

```spin2
        TEST    flags, #MASK    WZ      ' Test bits
        if_nz   JMP #bits_set           ' Branch if any bit set
```

### Pattern 2: Count-and-Loop

```spin2
        MOV     count, #N
.loop   ' ... body ...
        SUB     count, #1       WZ      ' Decrement counter
        if_nz   JMP #.loop              ' Continue if not zero
```

### Pattern 3: Compare-and-Select

```spin2
        CMP     value, limit    WC
        if_c    MOV value, limit        ' Clamp to minimum
```

### Pattern 4: Overflow Detection

```spin2
        ADD     sum, delta      WC
        if_c    MOV sum, #$FFFFFFFF     ' Saturate on overflow
```

### Pattern 5: Multi-Condition Testing

```spin2
        ' Note: CMP is unsigned, CMPS is signed
        CMPS    x, #0           WC      ' C=1 if x < 0 (signed comparison)
        CMPS    x, #100         WZ      ' Z=1 if x == 100
        if_c_or_z  JMP #special         ' If x<0 OR x==100
```

### Pattern 6: Lock Acquisition

```spin2
.retry  LOCKTRY #lock_num       WC      ' Try to acquire lock
        if_nc   JMP #.retry             ' Retry if not acquired
        ' ... critical section ...
        LOCKREL #lock_num               ' Release lock
```

---

## 11. Best Practices

### 1. Be Explicit About Flag Usage

Always use effects when you need the flags, even if the instruction "naturally" produces them:

```spin2
' BAD: Relies on implicit flag behavior
        SUB     count, #1
        if_z    JMP #done       ' Might work, but unclear

' GOOD: Explicitly requests flag update
        SUB     count, #1   WZ
        if_z    JMP #done       ' Clear intent
```

### 2. Use WCZ When You Need Both Flags

Don't try to update flags separately when you need both:

```spin2
' This is NOT valid syntax:
        ADD     x, y    WC WZ   ' ERROR!

' Use WCZ instead:
        ADD     x, y    WCZ     ' Correct
```

### 3. Preserve Flags When Needed

Be aware that most instructions between a flag-setting operation and its use will NOT change the flags (unless they have WC/WZ/WCZ):

```spin2
        CMP     a, b        WC      ' Set C flag
        MOV     temp, x             ' Does NOT change C (no effect)
        ADD     y, #1               ' Does NOT change C (no effect)
        if_c    JMP #a_less_b       ' Still uses C from CMP
```

### 4. Use the Right Comparison Instruction

- `CMP` - Unsigned comparison (C = D < S unsigned)
- `CMPS` - Signed comparison (C = D < S signed)
- `TEST` - Bit testing (Z = (D AND S) == 0, C = parity)

### 5. Document Complex Flag Logic

```spin2
        ' Build condition: (pin0 AND pin1) OR pin2
        TESTP   #pin0       WC      ' C = pin0
        TESTP   #pin1       ANDC    ' C = pin0 AND pin1
        TESTP   #pin2       ORC     ' C = (pin0 AND pin1) OR pin2
        if_c    JMP #condition_met
```

### 6. Remember: Effects Have Zero Performance Cost

Using WC, WZ, or WCZ adds no execution time. Use them freely when you need flag information.

---

## Summary

| Effect | Bits [20:19] | C Updated | Z Updated | Usage |
|--------|--------------|-----------|-----------|-------|
| (none) | `00` | No | No | Don't need flags |
| WZ | `01` | No | Yes | Only need zero test |
| WC | `10` | Yes | No | Only need carry/comparison |
| WCZ | `11` | Yes | Yes | Need both flags |

**Key Takeaways:**
1. **WCZ = WC + WZ** - It's a shorthand for updating both flags
2. **You cannot write `WC WZ`** - Effects are single tokens; use `WCZ` for both
3. **Flags persist** - They only change when explicitly modified
4. **Not all instructions support all effects** - The compiler validates:
   - 40 instructions (BIT\*, DIR\*, DRV\*, FLT\*, OUT\*) accept **only WCZ**
   - 9 instructions accept **only WC** (COGID, COGINIT, GETCT, LOCKNEW, LOCKREL, LOCKTRY, MODC, RDPIN, RQPIN)
   - 5 instructions accept **only WZ** (MODZ, MUL, MULS, SCA, SCAS)
   - 4 instructions (TESTP, TESTPN, TESTB, TESTBN) accept WC/WZ/extended but **not WCZ**
5. **Extended effects** (ANDC, ORC, etc.) combine logic with flag updates
6. **Zero cost** - Effects don't slow down execution

---

*This document describes WC, WZ, and WCZ effects in PASM2 as implemented in the PNut-TS compiler.*
