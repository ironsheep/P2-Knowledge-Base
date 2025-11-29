# Instructions: M

This section contains all PASM2 instructions beginning with the letter M.

---

## MERGEB {#mergeb}

Merge bits of bytes
[Math and Logic Instruction](#math-and-logic-instructions) - Rearrange bits from each byte into a merged pattern.

```
MERGEB  D
```

**Result:** Bits from each byte in D are rearranged into a specific merged pattern.

- D is a register containing the value whose byte bits will be merged.

```{=latex}
\simpleencoding{EEEE}{1101011}{000}{DDDDDDDDD}{001100001}{D}{---}{---}{2}
```

**Related:** [MERGEW](#mergew), [SPLITB](#splitb), [SPLITW](#splitw)

**Explanation:**

MERGEB rearranges the bits within D by extracting one bit from each byte and merging them into a specific pattern. The result is: D = {D[31], D[23], D[15], D[7], D[30], D[22], D[14], D[6], ..., D[24], D[16], D[8], D[0]}.

This operation takes the most significant bit from each of the four bytes in D and places them in the upper nibble of the result, then the next most significant bit from each byte into the next nibble, and so on. Each group of four bits in the result contains one bit from each of the four original bytes.

MERGEB is useful for bit-plane conversions, graphics operations, and data transformations where bits need to be regrouped across byte boundaries. It performs the inverse operation of SPLITB, which distributes bits back into their original byte positions.

---

## MERGEW {#mergew}

Merge bits of words
[Math and Logic Instruction](#math-and-logic-instructions) - Rearrange bits from each word into a merged pattern.

```
MERGEW  D
```

**Result:** Bits from each word in D are rearranged into a specific merged pattern.

- D is a register containing the value whose word bits will be merged.

```{=latex}
\simpleencoding{EEEE}{1101011}{000}{DDDDDDDDD}{001100011}{D}{---}{---}{2}
```

**Related:** [MERGEB](#mergeb), [SPLITB](#splitb), [SPLITW](#splitw)

**Explanation:**

MERGEW rearranges the bits within D by extracting corresponding bits from each of the two 16-bit words and interleaving them. The result is: D = {D[31], D[15], D[30], D[14], D[29], D[13], ..., D[17], D[1], D[16], D[0]}.

This operation interleaves the bits from the upper and lower words of D, alternating between taking a bit from the upper word and a bit from the lower word. The most significant bit of the result comes from the most significant bit of the upper word, the next bit from the most significant bit of the lower word, and so on.

MERGEW is useful for word-level bit-plane conversions, graphics operations requiring word-aligned data transformations, and encoding operations. It performs the inverse operation of SPLITW, which de-interleaves the bits back into their original word positions.

---

## MIXPIX {#mixpix}

Mix pixels
[Pixel Mixer Instruction](#pixel-mixer-instructions) - Blend bytes of source into destination using pixel mixer configuration.

```
MIXPIX  D,{#}S
```

**Result:** Bytes of S are blended into bytes of D according to the SETPIX and SETPIV configuration.

- D is a register containing the destination pixel bytes to be modified.
- S is a register, 9-bit literal, or 32-bit augmented literal containing the source pixel bytes.

```{=latex}
\simpleencoding{EEEE}{1010010}{11I}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{7}
```

**Related:** [SETPIX](#setpix), [SETPIV](#setpiv), [ADDPIX](#addpix), [MULPIX](#mulpix), [BLNPIX](#blnpix)

**Explanation:**

MIXPIX performs pixel blending operations on the four bytes of D using the four bytes of S, according to the mixing parameters previously configured by SETPIX and SETPIV instructions. Each byte is treated as a separate pixel component (typically used for red, green, blue, and alpha channels in RGBA color format).

The SETPIX instruction configures the pixel mixer mode, which determines how the source and destination bytes are combined (such as multiply, add, or blend operations). The SETPIV instruction provides additional configuration values that affect the mixing calculation.

This instruction executes in 7 clock cycles to perform the pixel arithmetic on all four bytes in parallel. The exact blending formula depends on the mode set by SETPIX, but typically implements standard pixel compositing operations used in graphics rendering, such as alpha blending, color multiplication, or additive blending.

MIXPIX is essential for high-performance graphics operations, enabling real-time color mixing, transparency effects, and color space transformations without requiring multiple individual byte operations.

---

## MODC {#modc}

Modify C flag
[Flag Instruction](#flag-instructions) - Set or clear the C flag based on a modifier and current flag state.

```
MODC  c  {WC}
```

**Result:** The C flag is set or cleared according to the modifier and current C and Z flag states.

- c is a 4-bit modifier value that selects which combination of current C and Z flag states produces a 1 result for the C flag.
- WC is an optional effect to make the modification visible to subsequent flag reads.

```{=latex}
\simpleencoding{EEEE}{1101011}{C01}{0cccc0000}{001101111}{---}{cccc[\{C,Z\}]}{---}{2}
```

**Related:** [MODZ](#modz), [MODCZ](#modcz), [TESTB](#testb), [TESTBN](#testbn)

**Explanation:**

MODC provides conditional modification of the C flag based on a 4-bit modifier value and the current state of both the C and Z flags. The modifier value acts as a lookup table, where each of the four bits corresponds to one of the four possible combinations of the current C and Z flag states: 00, 01, 10, and 11.

The modifier is applied as: C = cccc[{C,Z}], where {C,Z} forms a 2-bit index into the 4-bit modifier value. For example, if the current C flag is 1 and Z flag is 0, the index is binary 10 (2 decimal), and the C flag is set to bit 2 of the modifier value.

Common modifier values enable useful operations: $F (binary 1111) always sets C to 1, $0 (binary 0000) always clears C to 0, $C (binary 1100) copies C to itself (if Z=0) or clears it (if Z=1), and $3 (binary 0011) sets C if Z=1.

MODC is typically used after comparison or test instructions to create complex conditional logic without branching. It provides a mechanism to compute a boolean result based on multiple flag conditions in a single instruction.

If the WC effect is specified, the flag modification becomes visible to subsequent instructions; otherwise, the modification may be used internally without affecting the architectural flag state.

---

## MODCZ {#modcz}

Modify C and Z flags
[Flag Instruction](#flag-instructions) - Set or clear both C and Z flags based on modifiers and current flag states.

```
MODCZ  c,z  {WC/WZ/WCZ}
```

**Result:** Both C and Z flags are set or cleared according to their modifiers and the current C and Z flag states.

- c is a 4-bit modifier value that selects which combination of current C and Z flag states produces a 1 result for the C flag.
- z is a 4-bit modifier value that selects which combination of current C and Z flag states produces a 1 result for the Z flag.
- WC, WZ, or WCZ are optional effects to make the modifications visible to subsequent flag reads.

```{=latex}
\simpleencoding{EEEE}{1101011}{CZ1}{0cccczzzz}{001101111}{---}{cccc[\{C,Z\}]}{zzzz[\{C,Z\}]}{2}
```

**Related:** [MODC](#modc), [MODZ](#modz), [TESTB](#testb), [TESTBN](#testbn)

**Explanation:**

MODCZ provides simultaneous conditional modification of both the C and Z flags based on 4-bit modifier values and the current state of both flags. Each modifier value acts as a lookup table, where each of the four bits corresponds to one of the four possible combinations of the current C and Z flag states: 00, 01, 10, and 11.

The modifiers are applied as: C = cccc[{C,Z}] and Z = zzzz[{C,Z}], where {C,Z} forms a 2-bit index into each 4-bit modifier value. Both flags are updated simultaneously based on the same initial C and Z states, allowing complex boolean operations to be computed in parallel.

This instruction enables sophisticated conditional logic operations without branching. For example, modifier values can implement logical operations like AND, OR, XOR between the flags, or conditional moves where one flag's new value depends on the other flag's current state.

Common uses include implementing state machines where both flags represent state bits, performing multi-condition tests after comparison operations, and creating compact conditional code sequences that would otherwise require multiple instructions or branches.

If the WC, WZ, or WCZ effects are specified, the flag modifications become visible to subsequent instructions. Without these effects, the modifications may be used internally without affecting the architectural flag state visible to later code.

The simultaneous update of both flags makes MODCZ more powerful than using separate MODC and MODZ instructions, as it allows each flag's new value to be based on the same initial flag state rather than having one flag update affect the other's calculation.

---

## MODZ {#modz}

Modify Z flag
[Flag Instruction](#flag-instructions) - Set or clear the Z flag based on a modifier and current flag state.

```
MODZ  z  {WZ}
```

**Result:** The Z flag is set or cleared according to the modifier and current C and Z flag states.

- z is a 4-bit modifier value that selects which combination of current C and Z flag states produces a 1 result for the Z flag.
- WZ is an optional effect to make the modification visible to subsequent flag reads.

```{=latex}
\simpleencoding{EEEE}{1101011}{0Z1}{00000zzzz}{001101111}{---}{---}{zzzz[\{C,Z\}]}{2}
```

**Related:** [MODC](#modc), [MODCZ](#modcz), [TESTB](#testb), [TESTBN](#testbn)

**Explanation:**

MODZ provides conditional modification of the Z flag based on a 4-bit modifier value and the current state of both the C and Z flags. The modifier value acts as a lookup table, where each of the four bits corresponds to one of the four possible combinations of the current C and Z flag states: 00, 01, 10, and 11.

The modifier is applied as: Z = zzzz[{C,Z}], where {C,Z} forms a 2-bit index into the 4-bit modifier value. For example, if the current C flag is 0 and Z flag is 1, the index is binary 01 (1 decimal), and the Z flag is set to bit 1 of the modifier value.

Common modifier values enable useful operations: $F (binary 1111) always sets Z to 1, $0 (binary 0000) always clears Z to 0, $A (binary 1010) copies Z to itself (preserving current state), and $C (binary 1100) sets Z if C=1.

MODZ is typically used after comparison or test instructions to create complex conditional logic without branching. It provides a mechanism to compute a boolean result based on multiple flag conditions in a single instruction.

If the WZ effect is specified, the flag modification becomes visible to subsequent instructions; otherwise, the modification may be used internally without affecting the architectural flag state.

---

## MOV {#mov}

Move
[Math and Logic Instruction](#math-and-logic-instructions) - Copy a value from source to destination.

```
MOV  Dest, {#}Src  {WC|WZ|WCZ}
```

**Result:** The Src value is stored in Dest.

- Dest is a register where the Src value will be written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is copied to Dest.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0110000}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{S[31]}{Result = 0}{2}
```

**Related:** [MOVBYTS](#movbyts), [MUXNIBS](#muxnibs), [MUXNITS](#muxnits), [SETQ](#setq)

**Explanation:**

MOV copies the value from Src into the Dest register, providing the fundamental data movement operation in PASM2. This is one of the most frequently used instructions, enabling register initialization, value copying, and data transfer between registers.

If the WC or WCZ effect is specified, the C flag is set to the most significant bit of the source value (Src[31]), which represents the sign bit when Src is interpreted as a signed 32-bit value. This allows MOV to simultaneously copy a value and test its sign.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result written to Dest equals zero, or is cleared (0) if the result is non-zero. This enables immediate testing of whether the moved value is zero without requiring a separate comparison instruction.

MOV with immediate values is commonly used for register initialization:

```pasm
        mov     counter, #100           ' Initialize counter to 100
        mov     mask, ##$FFFF_0000      ' Load 32-bit constant using AUGS
```

MOV between registers is used for preserving values and working with temporary copies:

```pasm
        mov     temp, value             ' Save value in temp
        add     value, increment        ' Modify value
        mov     result, value           ' Copy final result
```

When combined with flag effects, MOV enables efficient value testing:

```pasm
        mov     data, source  wz        ' Copy and test if zero
if_nz   call    #process                ' Process only if non-zero
        mov     signed, value  wc       ' Copy and test sign bit
if_c    neg     signed, signed          ' Make positive if negative
```

---

## MOVBYTS {#movbyts}

Move bytes
[Math and Logic Instruction](#math-and-logic-instructions) - Rearrange bytes within a register according to a control pattern.

```
MOVBYTS  D,{#}S
```

**Result:** Bytes within D are rearranged according to the byte selection pattern in S.

- D is a register containing the bytes to be rearranged.
- S is a register, 9-bit literal, or 32-bit augmented literal containing the byte selection pattern.

```{=latex}
\simpleencoding{EEEE}{1001111}{11I}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{2}
```

**Related:** [MOVBYTS](#movbyts), [MERGEB](#mergeb), [SPLITB](#splitb), [ROLBYTE](#rolbyte)

**Explanation:**

MOVBYTS rearranges the four bytes within D according to a selection pattern specified in the lower 8 bits of S. The result is: D = {D.BYTE[S[7:6]], D.BYTE[S[5:4]], D.BYTE[S[3:2]], D.BYTE[S[1:0]]}.

Each 2-bit field in S selects which of the four original bytes in D will appear in each position of the result. S[1:0] selects the byte for the least significant position, S[3:2] for the second byte, S[5:4] for the third byte, and S[7:6] for the most significant byte. The 2-bit values 0, 1, 2, and 3 select bytes 0 (bits 7:0), 1 (bits 15:8), 2 (bits 23:16), and 3 (bits 31:24) respectively.

For example, to swap the high and low words of D, use S = $4E (binary 01_00_11_10), which places byte 2 in position 0, byte 3 in position 1, byte 0 in position 2, and byte 1 in position 3. To reverse all four bytes, use S = $1B (binary 00_01_10_11).

MOVBYTS is useful for byte-order conversions (endianness swapping), color channel reordering in pixel data, and general byte permutation operations. It executes in 2 clock cycles, making it an efficient alternative to multiple shift and mask operations.

Common patterns include:
- S = $E4 (binary 11_10_01_00): No change (identity)
- S = $1B (binary 00_01_10_11): Reverse bytes (big/little endian swap)
- S = $B1 (binary 10_11_00_01): Swap words
- S = $4E (binary 01_00_11_10): Swap bytes within each word

---

## MUL {#mul}

Multiply
[Math and Logic Instruction](#math-and-logic-instructions) - Multiply two unsigned 16-bit values to produce a 32-bit result.

```
MUL  Dest, {#}Src  {WZ}
```

**Result:** The 32-bit unsigned product of the lower 16 bits of Dest and Src is stored in Dest.

- Dest is a register containing the 16-bit value to multiply with Src, and is where the 32-bit result is written.
- Src is a register, 9-bit literal, or 16-bit augmented literal whose lower 16 bits are multiplied with Dest.
- WZ is an optional effect to update the Z flag.

```{=latex}
\simpleencoding{EEEE}{1010000}{0ZI}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{(D = 0) | (S = 0)}{2}
```

**Related:** [MULS](#muls), [QMUL](#qmul), [SCA](#sca), [SCAS](#scas)

**Explanation:**

MUL performs an unsigned 16-bit by 16-bit multiplication, taking only the lower 16 bits from each of Dest and Src, multiplying them together, and storing the full 32-bit unsigned product into Dest. This is a fast 2-clock multiplication operation suitable for small integer arithmetic and fixed-point calculations.

The operation is: D = unsigned(D[15:0] * S[15:0]). The upper 16 bits of both Dest and Src are ignored during the multiplication, but the full 32-bit result can utilize all bits in the destination register. For example, multiplying $0001_8000 by $0002_4000 produces $2000_0000 (using only the $8000 and $4000 values).

If the WZ effect is specified, the Z flag is set (1) if either Dest or Src equals zero before the multiplication, or is cleared (0) if both are non-zero. Note that this tests the pre-multiplication values, not the result, providing a quick way to detect zero operands.

MUL is commonly used for scaling operations in fixed-point arithmetic:

```pasm
        mov     value, ##1000           ' Value = 1000
        mul     value, #25              ' Multiply by 25: value = 25000
```

For fixed-point math with 16-bit fractional parts:

```pasm
        ' Multiply two 16.16 fixed-point numbers
        ' Result in upper 16 bits needs shifting
        mov     temp, frac1
        mul     temp, frac2             ' temp = product (low 16 of each)
        shr     temp, #16               ' Adjust for fixed-point scale
```

For multiplications larger than 16x16 bits, use the CORDIC solver QMUL instruction, which can multiply full 32-bit values and produces a 64-bit result accessible through the upper and lower result registers. MUL's 2-clock speed makes it ideal when the operands are known to fit in 16 bits.

---

## MULPIX {#mulpix}

Multiply pixels
[Pixel Mixer Instruction](#pixel-mixer-instructions) - Multiply corresponding bytes treating them as fractional values.

```
MULPIX  D,{#}S
```

**Result:** Each byte of S is multiplied with the corresponding byte of D, with results stored in D.

- D is a register containing four pixel bytes to be multiplied.
- S is a register, 9-bit literal, or 32-bit augmented literal containing four pixel bytes as multipliers.

```{=latex}
\simpleencoding{EEEE}{1010010}{01I}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{7}
```

**Related:** [ADDPIX](#addpix), [BLNPIX](#blnpix), [MIXPIX](#mixpix), [SETPIX](#setpix)

**Explanation:**

MULPIX performs parallel multiplication on four byte pairs, treating each byte as a fractional value where $FF represents 1.0 and $00 represents 0.0. Each of the four bytes in S is multiplied with the corresponding byte in D, and the results replace the bytes in D.

The multiplication treats bytes as 8-bit fractional values in the range 0.0 to 1.0. For each byte position, the operation computes: D.BYTE[n] = (D.BYTE[n] * S.BYTE[n]) / 255. The division by 255 is implicit in the fractional representation, where $FF * $FF = $FF (1.0 * 1.0 = 1.0).

This instruction is essential for pixel color multiplication operations used in graphics rendering. For example, multiplying an RGB color by a brightness value: if D contains $80_60_40_20 (RGBA values) and S contains $80_80_80_FF (50% brightness on RGB, full alpha), each color component is reduced to 50% of its original value.

MULPIX executes in 7 clock cycles to perform all four parallel multiplications. This is significantly faster than performing four separate multiply and scale operations, making it practical for real-time graphics processing.

Common uses include:
- Color modulation (tinting): Multiply each color channel by a tint value
- Brightness adjustment: Multiply RGB by a brightness factor
- Alpha premultiplication: Multiply RGB by alpha for compositing
- Texture filtering: Combine texel colors with interpolation weights

The instruction treats all bytes independently, so it can be used for any four-byte parallel multiply operation, not just color processing.

---

## MULS {#muls}

Multiply signed
[Math and Logic Instruction](#math-and-logic-instructions) - Multiply two signed 16-bit values to produce a signed 32-bit result.

```
MULS  Dest, {#}Src  {WZ}
```

**Result:** The 32-bit signed product of the signed lower 16 bits of Dest and Src is stored in Dest.

- Dest is a register containing the signed 16-bit value to multiply with Src, and is where the signed 32-bit result is written.
- Src is a register, 9-bit literal, or signed 16-bit augmented literal whose lower 16 bits are multiplied with Dest.
- WZ is an optional effect to update the Z flag.

```{=latex}
\simpleencoding{EEEE}{1010000}{1ZI}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{(D = 0) | (S = 0)}{2}
```

**Related:** [MUL](#mul), [QMUL](#qmul), [SCA](#sca), [SCAS](#scas)

**Explanation:**

MULS performs a signed 16-bit by 16-bit multiplication, taking only the lower 16 bits from each of Dest and Src as signed values, multiplying them together, and storing the full signed 32-bit product into Dest. This is a fast 2-clock multiplication operation suitable for signed integer arithmetic and signed fixed-point calculations.

The operation is: D = signed(D[15:0] * S[15:0]). The upper 16 bits of both Dest and Src are ignored during the multiplication. The lower 16 bits are treated as signed values (using two's complement representation), so values from $8000 (-32768) to $7FFF (+32767) are valid inputs. The 32-bit result is properly sign-extended to represent the full range of products.

For example, multiplying $FFFF_8000 (-32768 in lower 16 bits) by $0000_0002 (+2) produces $FFFF_0000 (-65536 as a signed 32-bit value). The upper 16 bits of the operands are ignored, and the result is correctly signed.

If the WZ effect is specified, the Z flag is set (1) if either Dest or Src equals zero before the multiplication, or is cleared (0) if both are non-zero. Note that this tests the pre-multiplication values, not the result, providing a quick way to detect zero operands.

MULS is commonly used for signed arithmetic and physics calculations:

```pasm
        mov     velocity, signed_speed
        muls    velocity, time          ' velocity = speed * time (signed)
```

For signed fixed-point math with 16-bit fractional parts:

```pasm
        ' Multiply two signed 16.16 fixed-point numbers
        mov     temp, signed_frac1
        muls    temp, signed_frac2      ' Signed multiplication
        sar     temp, #16               ' Arithmetic shift to preserve sign
```

MULS differs from MUL only in that it treats the 16-bit operands as signed values rather than unsigned. The choice between them depends on whether the values being multiplied represent signed or unsigned quantities.

For multiplications larger than 16x16 bits, use the CORDIC solver QMUL instruction, which can multiply full signed 32-bit values and produces a signed 64-bit result accessible through the upper and lower result registers.

---

## MUXC {#muxc}

Multiplex C
[Math and Logic Instruction](#math-and-logic-instructions) - Set selected bits of destination to the C flag value.

```
MUXC  D,{#}S  {WC|WZ|WCZ}
```

**Result:** Each bit position in D where S has a 1 is set to the current C flag value.

- D is a register whose bits will be set to the C flag value where S has 1 bits.
- S is a register, 9-bit literal, or 32-bit augmented literal that selects which bits to modify.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0101100}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{parity of result}{Result = 0}{2}
```

**Related:** [MUXNC](#muxnc), [MUXZ](#muxz), [MUXNZ](#muxnz), [MUXQ](#muxq), [TESTB](#testb)

**Explanation:**

MUXC modifies selected bits in D based on the current C flag value. For each bit position where S contains a 1, the corresponding bit in D is replaced with the C flag value. All other bits in D remain unchanged. The operation is: D = (!S & D) | (S & {32{C}}), where {32{C}} represents the C flag value replicated across all 32 bits.

For example, if C = 1, D = $F0F0_F0F0, and S = $00FF_00FF, the result is D = $F0FF_F0FF, because the 1 bits in S (the lower byte of each word) are set to 1 (the C flag value), while the 0 bits in S leave the corresponding D bits unchanged.

MUXC is commonly used to conditionally set or clear specific bits based on a flag test:

```pasm
        cmp     value, limit  wc        ' Set C if value < limit
        muxc    status, #$01            ' Set bit 0 of status to C
```

Multiple bits can be set simultaneously:

```pasm
        test    data, #$80  wc          ' Test bit 7, set C if high
        muxc    flags, #$07             ' Set bits 0-2 to match C
```

If the WC or WCZ effect is specified, the C flag is set to the parity of the result (1 if an odd number of bits are set, 0 if even). If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if non-zero.

MUXC provides an efficient alternative to conditional branches when setting bits based on test results. Instead of branching, a comparison can set the C flag, and MUXC can immediately apply that result to specific bits.

---

## MUXNC {#muxnc}

Multiplex not C
[Math and Logic Instruction](#math-and-logic-instructions) - Set selected bits of destination to the inverted C flag value.

```
MUXNC  D,{#}S  {WC|WZ|WCZ}
```

**Result:** Each bit position in D where S has a 1 is set to the inverted C flag value.

- D is a register whose bits will be set to the inverted C flag value where S has 1 bits.
- S is a register, 9-bit literal, or 32-bit augmented literal that selects which bits to modify.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0101101}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{parity of result}{Result = 0}{2}
```

**Related:** [MUXC](#muxc), [MUXZ](#muxz), [MUXNZ](#muxnz), [MUXQ](#muxq), [TESTBN](#testbn)

**Explanation:**

MUXNC modifies selected bits in D based on the inverted C flag value. For each bit position where S contains a 1, the corresponding bit in D is replaced with !C (the logical complement of the C flag). All other bits in D remain unchanged. The operation is: D = (!S & D) | (S & {32{!C}}), where {32{!C}} represents the inverted C flag value replicated across all 32 bits.

For example, if C = 0, D = $F0F0_F0F0, and S = $00FF_00FF, the result is D = $F0FF_F0FF, because !C = 1, and the 1 bits in S (the lower byte of each word) are set to 1, while the 0 bits in S leave the corresponding D bits unchanged.

MUXNC is commonly used to conditionally set or clear specific bits based on the inverted result of a flag test:

```pasm
        cmp     value, limit  wc        ' Set C if value < limit
        muxnc   status, #$01            ' Set bit 0 to 1 if value >= limit
```

This is particularly useful when the desired action corresponds to the opposite of the comparison result:

```pasm
        test    enable, #$01  wc        ' Test enable bit
        muxnc   control, #$80           ' Set bit 7 high if disabled
```

If the WC or WCZ effect is specified, the C flag is set to the parity of the result (1 if an odd number of bits are set, 0 if even). If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if non-zero.

MUXNC provides the logical complement of MUXC, allowing both polarities of flag-based bit setting without requiring a separate instruction to invert the flag. Together, MUXC and MUXNC provide complete control over conditional bit manipulation based on comparison and test results.

---

## MUXNIBS {#muxnibs}

Multiplex nibbles
[Math and Logic Instruction](#math-and-logic-instructions) - Copy non-zero nibbles from source to destination.

```
MUXNIBS  Dest, {#}Src
```

**Result:** Each non-zero nibble in Src replaces the corresponding nibble in Dest.

- Dest is a register whose nibbles will be updated from Src.
- Src is a register, 9-bit literal, or 32-bit augmented literal containing nibble values to copy.

```{=latex}
\simpleencoding{EEEE}{1001111}{01I}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{2}
```

**Related:** [MUXNITS](#muxnits), [MUXQ](#muxq), [MOVBYTS](#movbyts), [SPLITB](#splitb)

**Explanation:**

MUXNIBS selectively copies nibbles (4-bit fields) from Src to Dest based on whether each nibble in Src is non-zero. For each of the eight nibble positions, if the nibble in Src is non-zero, that nibble value is copied to the corresponding position in Dest. If the nibble in Src is zero, the corresponding nibble in Dest remains unchanged.

For example, if Dest = $1234_5678 and Src = $0A00_0C0D, the result is Dest = $1A34_5C7D. The nibbles at positions 6 ($A), 2 ($C), and 0 ($D) from Src are copied because they are non-zero, while positions 7, 5, 4, 3, and 1 remain unchanged in Dest because the corresponding Src nibbles are zero.

This instruction is useful for sparse updates where only certain nibbles need modification:

```pasm
        ' Update only the changed nibbles in a configuration register
        mov     config, current_config
        muxnibs config, changes         ' Apply non-zero changes only
```

MUXNIBS is commonly used in graphics operations for palette updates, bit-field modifications where fields are naturally nibble-aligned, and efficient sparse data updates. It provides a single-instruction way to perform selective nibble replacement that would otherwise require multiple mask and merge operations.

The instruction treats nibbles independently, enabling parallel conditional updates across all eight nibble positions in a single 2-clock operation.

---

## MUXNITS {#muxnits}

Multiplex nits
[Math and Logic Instruction](#math-and-logic-instructions) - Copy non-zero bit pairs from source to destination.

```
MUXNITS  Dest, {#}Src
```

**Result:** Each non-zero bit pair in Src replaces the corresponding bit pair in Dest.

- Dest is a register whose bit pairs will be updated from Src.
- Src is a register, 9-bit literal, or 32-bit augmented literal containing bit pair values to copy.

```{=latex}
\simpleencoding{EEEE}{1001111}{00I}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{2}
```

**Related:** [MUXNIBS](#muxnibs), [MUXQ](#muxq), [MOVBYTS](#movbyts), [SPLITB](#splitb)

**Explanation:**

MUXNITS selectively copies bit pairs (2-bit fields, called "nits") from Src to Dest based on whether each bit pair in Src is non-zero. For each of the sixteen bit pair positions, if the bit pair in Src is non-zero (01, 10, or 11), that bit pair value is copied to the corresponding position in Dest. If the bit pair in Src is zero (00), the corresponding bit pair in Dest remains unchanged.

For example, if Dest = $5555_5555 (binary 01_01_01_01... in bit pairs) and Src = $00A0_0002 (containing non-zero bit pairs at positions 11, 9, and 0), only those three bit pairs are updated in Dest while the others remain as 01.

This instruction is particularly useful for pixel graphics operations where 2-bit values represent pixel data (such as in 4-color graphics modes), sparse bit-field updates, and state machine implementations where state variables are represented as 2-bit fields.

MUXNITS provides parallel conditional updates across all sixteen bit pair positions in a single 2-clock operation:

```pasm
        ' Update specific 2-bit fields in a packed structure
        mov     state, current_state
        muxnits state, updates          ' Apply non-zero updates only
```

The name "nits" comes from "nibble bits" or 2-bit fields, representing the next smaller grouping after nibbles (4-bit fields). This instruction complements MUXNIBS by operating at a finer granularity.

---

## MUXNZ {#muxnz}

Multiplex not Z
[Math and Logic Instruction](#math-and-logic-instructions) - Set selected bits of destination to the inverted Z flag value.

```
MUXNZ  D,{#}S  {WC|WZ|WCZ}
```

**Result:** Each bit position in D where S has a 1 is set to the inverted Z flag value.

- D is a register whose bits will be set to the inverted Z flag value where S has 1 bits.
- S is a register, 9-bit literal, or 32-bit augmented literal that selects which bits to modify.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0101111}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{parity of result}{Result = 0}{2}
```

**Related:** [MUXZ](#muxz), [MUXC](#muxc), [MUXNC](#muxnc), [MUXQ](#muxq), [CMP](#cmp)

**Explanation:**

MUXNZ modifies selected bits in D based on the inverted Z flag value. For each bit position where S contains a 1, the corresponding bit in D is replaced with !Z (the logical complement of the Z flag). All other bits in D remain unchanged. The operation is: D = (!S & D) | (S & {32{!Z}}), where {32{!Z}} represents the inverted Z flag value replicated across all 32 bits.

The Z flag is typically set by comparison or arithmetic instructions when a result equals zero. MUXNZ therefore sets the selected bits high when the previous result was non-zero, and low when it was zero.

For example, after a comparison that sets Z to indicate equality:

```pasm
        cmp     value, target  wz       ' Set Z if equal
        muxnz   status, #$01            ' Set bit 0 if not equal
```

This is particularly useful when the desired action corresponds to the non-zero condition:

```pasm
        sub     counter, #1  wz         ' Decrement and test
        muxnz   flags, #$80             ' Set flag if counter not exhausted
```

If the WC or WCZ effect is specified, the C flag is set to the parity of the result (1 if an odd number of bits are set, 0 if even). If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if non-zero. Note that the WZ effect updates the Z flag based on the result value, not the original Z flag state that determined which value to mux.

MUXNZ provides the logical complement of MUXZ, allowing both polarities of zero-test-based bit setting without requiring a separate instruction to invert the flag. Together, MUXZ and MUXNZ provide complete control over conditional bit manipulation based on zero-detection results.

---

## MUXQ {#muxq}

Multiplex Q
[Math and Logic Instruction](#math-and-logic-instructions) - Copy selected bits from source to destination based on Q register mask.

```
MUXQ  Dest, {#}Src
```

**Result:** Bits from Src are copied to Dest at positions where Q has 1 bits.

- Dest is a register whose bits will be updated from Src.
- Src is a register, 9-bit literal, or 32-bit augmented literal containing bit values to copy.

```{=latex}
\simpleencoding{EEEE}{1001111}{10I}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{2}
```

**Related:** [SETQ](#setq), [MUXC](#muxc), [MUXZ](#muxz), [MUXNIBS](#muxnibs), [MUXNITS](#muxnits)

**Explanation:**

MUXQ performs selective bit copying from Src to Dest based on a mask previously loaded into the Q register using SETQ. For each bit position where Q contains a 1, the corresponding bit from Src is copied into Dest. For bit positions where Q contains a 0, the corresponding bit in Dest remains unchanged. The operation is: D = (!Q & D) | (Q & S).

MUXQ must be preceded by SETQ to load the mask into Q:

```pasm
        setq    mask                    ' Load mask into Q
        muxq    dest, source            ' Copy masked bits from source
```

This provides atomic masked bit updates that are more efficient than separate AND and OR operations:

```pasm
        ' Traditional approach (3 instructions):
        andn    dest, mask              ' Clear masked bits
        and     temp, source, mask      ' Extract source bits
        or      dest, temp              ' Merge into dest

        ' MUXQ approach (2 instructions):
        setq    mask                    ' Set mask
        muxq    dest, source            ' Atomic masked copy
```

MUXQ is critical for parallel I/O operations, especially driving multiple pins simultaneously:

```pasm
        ' Update multiple RGB LED pins atomically
        setq    rgb_mask                ' Mask for RGB pins
        muxq    outa, rgb_data          ' Update all RGB pins together
```

The Q register mask enables sophisticated bit manipulation:

```pasm
        ' Update specific configuration bits
        setq    ##$00FF_FF00            ' Mask for middle bytes
        muxq    config, new_values      ' Update only those bytes
```

MUXQ is particularly valuable for HUB75 RGB panel driving and other applications requiring atomic multi-pin updates. It executes in 2 clock cycles, providing high-performance parallel bit operations essential for real-time graphics and control applications.

Unlike MUXC and MUXZ which replicate a single flag bit to all selected positions, MUXQ copies the actual corresponding bits from the source, enabling true parallel bit transfer operations.

---

## MUXZ {#muxz}

Multiplex Z
[Math and Logic Instruction](#math-and-logic-instructions) - Set selected bits of destination to the Z flag value.

```
MUXZ  D,{#}S  {WC|WZ|WCZ}
```

**Result:** Each bit position in D where S has a 1 is set to the current Z flag value.

- D is a register whose bits will be set to the Z flag value where S has 1 bits.
- S is a register, 9-bit literal, or 32-bit augmented literal that selects which bits to modify.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0101110}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{parity of result}{Result = 0}{2}
```

**Related:** [MUXNZ](#muxnz), [MUXC](#muxc), [MUXNC](#muxnc), [MUXQ](#muxq), [CMP](#cmp)

**Explanation:**

MUXZ modifies selected bits in D based on the current Z flag value. For each bit position where S contains a 1, the corresponding bit in D is replaced with the Z flag value. All other bits in D remain unchanged. The operation is: D = (!S & D) | (S & {32{Z}}), where {32{Z}} represents the Z flag value replicated across all 32 bits.

The Z flag is typically set by comparison or arithmetic instructions when a result equals zero. MUXZ therefore sets the selected bits high when the previous result was zero, and low when it was non-zero.

For example, after a comparison that sets Z to indicate equality:

```pasm
        cmp     value, target  wz       ' Set Z if equal
        muxz    status, #$01            ' Set bit 0 if equal
```

Multiple status bits can be updated simultaneously:

```pasm
        sub     counter, #1  wz         ' Decrement and test for zero
        muxz    flags, #$07             ' Set bits 0-2 if counter exhausted
```

MUXZ is commonly used to record test results in status registers without branching:

```pasm
        ' Build status word from multiple tests
        test    data, #$80  wz          ' Test bit 7
        muxz    status, #$01            ' Record result in bit 0
        test    data, #$40  wz          ' Test bit 6
        muxz    status, #$02            ' Record result in bit 1
```

If the WC or WCZ effect is specified, the C flag is set to the parity of the result (1 if an odd number of bits are set, 0 if even). If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if non-zero. Note that the WZ effect updates the Z flag based on the result value, not the original Z flag state that determined which value to mux.

MUXZ provides an efficient alternative to conditional branches when recording zero-test results as bits. It enables building status values from multiple tests without requiring any jumps or conditional execution.

---
