# Instructions: M

This section contains all PASM2 instructions beginning with the letter M.



::: instrheader
## MERGEB {#mergeb}
Merge Bits Of Bytes

[Arithmetic Operations](#arithmetic-operations) - Rearranges bits by extracting one bit from each byte and merging them.
:::

**MERGEB**  *D*

**Operation:** `D = {D[31], D[23], D[15], D[7], ... D[24], D[16], D[8], D[0]}`

**Result:** Bits from each byte in D are rearranged into a specific merged pattern.

- D is a register containing the value whose byte bits will be merged.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001100001 | --- | --- | D | 2 |


**Related:** [MERGEW](#mergew), [SPLITB](#splitb), [SPLITW](#splitw)

**Explanation:**

MERGEB rearranges the bits within D by extracting one bit from each byte and merging them into a specific pattern. The result is: D = {D[31], D[23], D[15], D[7], D[30], D[22], D[14], D[6], ..., D[24], D[16], D[8], D[0]}.

This operation takes the most significant bit from each of the four bytes in D and places them in the upper nibble of the result, then the next most significant bit from each byte into the next nibble, and so on. Each group of four bits in the result contains one bit from each of the four original bytes.

MERGEB is useful for bit-plane conversions, graphics operations, and data transformations where bits need to be regrouped across byte boundaries. It performs the inverse operation of SPLITB, which distributes bits back into their original byte positions.



::: instrheader
## MERGEW {#mergew}
Merge Bits Of Words

[Arithmetic Operations](#arithmetic-operations) - Rearranges bits by interleaving from the two 16-bit words.
:::

**MERGEW**  *D*

**Operation:** `D = {D[31], D[15], D[30], D[14], ... D[17], D[1], D[16], D[0]}`

**Result:** Bits from each word in D are rearranged into a specific merged pattern.

- D is a register containing the value whose word bits will be merged.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001100011 | --- | --- | D | 2 |


**Related:** [MERGEB](#mergeb), [SPLITB](#splitb), [SPLITW](#splitw)

**Explanation:**

MERGEW rearranges the bits within D by extracting corresponding bits from each of the two 16-bit words and interleaving them. The result is: D = {D[31], D[15], D[30], D[14], D[29], D[13], ..., D[17], D[1], D[16], D[0]}.

This operation interleaves the bits from the upper and lower words of D, alternating between taking a bit from the upper word and a bit from the lower word. The most significant bit of the result comes from the most significant bit of the upper word, the next bit from the most significant bit of the lower word, and so on.

MERGEW is useful for word-level bit-plane conversions, graphics operations requiring word-aligned data transformations, and encoding operations. It performs the inverse operation of SPLITW, which de-interleaves the bits back into their original word positions.



::: instrheader
## MIXPIX {#mixpix}
Mix Pixels

[Color Space and Pixel Operations](#color-space-and-pixel-operations) - Blends pixel bytes according to SETPIX and SETPIV configuration.
:::

**MIXPIX**  *D,{#}S*

**Result:** Bytes of S are blended into bytes of D according to the SETPIX and SETPIV configuration.

- D is a register containing the destination pixel bytes to be modified.
- S is a register, 9-bit literal, or 32-bit augmented literal containing the source pixel bytes.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010010 | 11I | DDDDDDDDD | SSSSSSSSS | --- | --- | D | 7 |


**Related:** [SETPIX](#setpix), [SETPIV](#setpiv), [ADDPIX](#addpix), [MULPIX](#mulpix), [BLNPIX](#blnpix)

**Explanation:**

MIXPIX performs pixel blending operations on the four bytes of D using the four bytes of S, according to the mixing parameters previously configured by SETPIX and SETPIV instructions. Each byte is treated as a separate pixel component (typically used for red, green, blue, and alpha channels in RGBA color format).

The SETPIX instruction configures the pixel mixer mode, which determines how the source and destination bytes are combined (such as multiply, add, or blend operations). The SETPIV instruction provides additional configuration values that affect the mixing calculation.

This instruction executes in 7 clock cycles to perform the pixel arithmetic on all four bytes in parallel. The exact blending formula depends on the mode set by SETPIX, but typically implements standard pixel compositing operations used in graphics rendering, such as alpha blending, color multiplication, or additive blending.

MIXPIX blends two pixels per the configured mode in one operation.



::: instrheader
## MODC {#modc}
Modify C Flag

[Arithmetic Operations](#arithmetic-operations) - Sets or clears C flag based on a modifier and current flag states.
:::

**MODC**  *c*  **{WC}**

**Operation:** `C = cccc[{C,Z}]`

**Result:** The C flag is set or cleared according to the modifier and current C and Z flag states.

- c is a 4-bit modifier constant (such as `_set`, `_clr`, `_c`, `_z`) that selects which combination of current C and Z flag states produces a 1 result for the C flag.
- WC must be specified for the C flag modification to take effect; without it, the result is computed but not written to the flag.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | C01 | 0cccc0000 | 001101111 | cccc[{C,Z}] | --- | --- | 2 |


**Related:** [MODZ](#modz), [MODCZ](#modcz), [TESTB](#testb), [TESTBN](#testbn)

**Explanation:**

MODC provides conditional modification of the C flag based on a 4-bit modifier value and the current state of both the C and Z flags. The modifier value acts as a lookup table, where each of the four bits corresponds to one of the four possible combinations of the current C and Z flag states: 00, 01, 10, and 11.

The modifier is applied as: C = cccc[{C,Z}], where {C,Z} forms a 2-bit index into the 4-bit modifier value. For example, if the current C flag is 1 and Z flag is 0, the index is binary 10 (2 decimal), and the C flag is set to bit 2 of the modifier value.

Common modifier values enable useful operations: $F (binary 1111) always sets C to 1, $0 (binary 0000) always clears C to 0, $C (binary 1100) copies C to itself (C unchanged, independent of Z), and $3 (binary 0011) sets C to the inverse of the current C (NC), independent of Z.

MODC is typically used after comparison or test instructions to create complex conditional logic without branching. It provides a mechanism to compute a boolean result based on multiple flag conditions in a single instruction.

The WC effect must be specified for the modification to take effect. Without WC, the instruction computes the result but does not write it to the C flag, rendering the instruction ineffective for most purposes.



::: instrheader
## MODCZ {#modcz}
Modify C And Z Flags

[Arithmetic Operations](#arithmetic-operations) - Sets or clears both C and Z flags based on modifiers.
:::

**MODCZ**  *c,z*  **{WC/WZ/WCZ}**

**Operation:** `C = cccc[{C,Z}]`; `Z = zzzz[{C,Z}]`

**Result:** Both C and Z flags are set or cleared according to their modifiers and the current C and Z flag states.

- c is a 4-bit modifier constant (such as `_set`, `_clr`, `_c`, `_z`) that selects which combination of current C and Z flag states produces a 1 result for the C flag.
- z is a 4-bit modifier constant that selects which combination of current C and Z flag states produces a 1 result for the Z flag.
- WC, WZ, or WCZ must be specified for the flag modifications to take effect; without them, results are computed but not written.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ1 | 0cccczzzz | 001101111 | cccc[{C,Z}] | zzzz[{C,Z}] | --- | 2 |


**Related:** [MODC](#modc), [MODZ](#modz), [TESTB](#testb), [TESTBN](#testbn)

**Explanation:**

MODCZ provides simultaneous conditional modification of both the C and Z flags based on 4-bit modifier values and the current state of both flags. Each modifier value acts as a lookup table, where each of the four bits corresponds to one of the four possible combinations of the current C and Z flag states: 00, 01, 10, and 11.

The modifiers are applied as: C = cccc[{C,Z}] and Z = zzzz[{C,Z}], where {C,Z} forms a 2-bit index into each 4-bit modifier value. Both flags are updated simultaneously based on the same initial C and Z states, allowing complex boolean operations to be computed in parallel.

This instruction implements conditional logic operations without branching. For example, modifier values can implement logical operations like AND, OR, XOR between the flags, or conditional moves where one flag's new value depends on the other flag's current state.

Common uses include implementing state machines where both flags represent state bits, performing multi-condition tests after comparison operations, and creating compact conditional code sequences that would otherwise require multiple instructions or branches.

The WC, WZ, or WCZ effect must be specified for the modifications to take effect. Without these effects, the instruction computes results but does not write them to the flags, rendering the instruction ineffective for most purposes.

MODCZ updates both flags from the same initial flag state, which separate MODC/MODZ cannot do: with separate instructions, one flag update affects the other's calculation.

**Modifier Constants:**

| Value | Binary | Mnemonic | Description |
|:-----:|:------:|:---------|:------------|
| 0 | 0000 | _CLR | Always clear (result = 0) |
| 1 | 0001 | _NC_AND_NZ | C=0 AND Z=0 |
| 2 | 0010 | _NC_AND_Z | C=0 AND Z=1 |
| 3 | 0011 | _NC | Copy inverse of C (not C) |
| 4 | 0100 | _C_AND_NZ | C=1 AND Z=0 |
| 5 | 0101 | _NZ | Copy inverse of Z (not Z) |
| 6 | 0110 | _C_NE_Z | C XOR Z (C not equal to Z) |
| 7 | 0111 | _NC_OR_NZ | C=0 OR Z=0 (NAND) |
| 8 | 1000 | _C_AND_Z | C=1 AND Z=1 (AND) |
| 9 | 1001 | _C_EQ_Z | NOT(C XOR Z) (C equals Z) |
| 10 | 1010 | _Z | Copy Z |
| 11 | 1011 | _NC_OR_Z | C=0 OR Z=1 |
| 12 | 1100 | _C | Copy C |
| 13 | 1101 | _C_OR_NZ | C=1 OR Z=0 |
| 14 | 1110 | _C_OR_Z | C=1 OR Z=1 (OR) |
| 15 | 1111 | _SET | Always set (result = 1) |

```pasm2
        MODCZ   _CLR, _SET      ' Clear C, set Z
        MODCZ   _SET, _CLR      ' Set C, clear Z
        MODCZ   _C, _Z          ' C and Z unchanged (copy to themselves)
        MODCZ   _Z, _C          ' Swap C and Z values
        MODCZ   _NC, _NZ        ' Invert both flags
```



::: instrheader
## MODZ {#modz}
Modify Z Flag

[Arithmetic Operations](#arithmetic-operations) - Sets or clears Z flag based on a modifier and current flag states.
:::

**MODZ**  *z*  **{WZ}**

**Operation:** `Z = zzzz[{C,Z}]`

**Result:** The Z flag is set or cleared according to the modifier and current C and Z flag states.

- z is a 4-bit modifier constant (such as `_set`, `_clr`, `_c`, `_z`) that selects which combination of current C and Z flag states produces a 1 result for the Z flag.
- WZ must be specified for the Z flag modification to take effect; without it, the result is computed but not written to the flag.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 0Z1 | 00000zzzz | 001101111 | --- | zzzz[{C,Z}] | --- | 2 |


**Related:** [MODC](#modc), [MODCZ](#modcz), [TESTB](#testb), [TESTBN](#testbn)

**Explanation:**

MODZ provides conditional modification of the Z flag based on a 4-bit modifier value and the current state of both the C and Z flags. The modifier value acts as a lookup table, where each of the four bits corresponds to one of the four possible combinations of the current C and Z flag states: 00, 01, 10, and 11.

The modifier is applied as: Z = zzzz[{C,Z}], where {C,Z} forms a 2-bit index into the 4-bit modifier value. For example, if the current C flag is 0 and Z flag is 1, the index is binary 01 (1 decimal), and the Z flag is set to bit 1 of the modifier value.

Common modifier values enable useful operations: $F (binary 1111) always sets Z to 1, $0 (binary 0000) always clears Z to 0, $A (binary 1010) copies Z to itself (preserving current state), and $C (binary 1100) sets Z if C=1.

MODZ is typically used after comparison or test instructions to create complex conditional logic without branching. It provides a mechanism to compute a boolean result based on multiple flag conditions in a single instruction.

The WZ effect must be specified for the modification to take effect. Without WZ, the instruction computes the result but does not write it to the Z flag, rendering the instruction ineffective for most purposes.



::: instrheader
## MOV {#mov}
Move

[Arithmetic Operations](#arithmetic-operations) - Copies a value from source to destination register.
:::

**MOV**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

**Result:** The Src value is stored in Dest.

- Dest is a register where the Src value will be written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is copied to Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0110000 | CZI | DDDDDDDDD | SSSSSSSSS | S[31] | result == 0 | D | 2 |


**Related:** [MOVBYTS](#movbyts), [MUXNIBS](#muxnibs), [MUXNITS](#muxnits), [SETQ](#setq)

**Explanation:**

MOV copies the value from Src into the Dest register, providing the fundamental data movement operation in PASM2. This is one of the most frequently used instructions, enabling register initialization, value copying, and data transfer between registers.

If the WC or WCZ effect is specified, the C flag is set to the most significant bit of the source value (Src[31]), which represents the sign bit when Src is interpreted as a signed 32-bit value. This allows MOV to simultaneously copy a value and test its sign.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result written to Dest equals zero, or is cleared (0) if the result is non-zero. This enables immediate testing of whether the moved value is zero without requiring a separate comparison instruction.

MOV with immediate values is commonly used for register initialization:

```pasm2
        mov     counter, #100           ' Initialize counter to 100
        mov     mask, ##$FFFF_0000      ' Load 32-bit constant using AUGS
```

MOV between registers is used for preserving values and working with temporary copies:

```pasm2
        mov     temp, value             ' Save value in temp
        add     value, increment        ' Modify value
        mov     result, value           ' Copy final result
```

When combined with flag effects, MOV enables efficient value testing:

```pasm2
                mov     data, source  wz        ' Copy and test if zero
        if_nz   call    #process                ' Process only if non-zero
                mov     signed, value  wc       ' Copy and test sign bit
        if_c    neg     signed, signed          ' Make positive if negative
```



::: instrheader
## MOVBYTS {#movbyts}
Move Bytes

[Arithmetic Operations](#arithmetic-operations) - Rearranges bytes within a register according to a selection pattern.
:::

**MOVBYTS**  *D,{#}S*

**Operation:** `D = {D.BYTE[S[7:6]], D.BYTE[S[5:4]], D.BYTE[S[3:2]], D.BYTE[S[1:0]]}`

**Result:** Bytes within D are rearranged according to the byte selection pattern in S.

- D is a register containing the bytes to be rearranged.
- S is a register, 9-bit literal, or 32-bit augmented literal containing the byte selection pattern.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001111 | 11I | DDDDDDDDD | SSSSSSSSS | --- | --- | D | 2 |


**Related:** [MERGEB](#mergeb), [SPLITB](#splitb), [ROLBYTE](#rolbyte)

**Explanation:**

MOVBYTS rearranges the four bytes within D according to a selection pattern specified in the lower 8 bits of S. The result is: D = {D.BYTE[S[7:6]], D.BYTE[S[5:4]], D.BYTE[S[3:2]], D.BYTE[S[1:0]]}.

Each 2-bit field in S selects which of the four original bytes in D will appear in each position of the result. S[1:0] selects the byte for the least significant position, S[3:2] for the second byte, S[5:4] for the third byte, and S[7:6] for the most significant byte. The 2-bit values 0, 1, 2, and 3 select bytes 0 (bits 7:0), 1 (bits 15:8), 2 (bits 23:16), and 3 (bits 31:24) respectively.

For example, to swap the high and low words of D, use S = $4E (binary 01_00_11_10), which places byte 2 in position 0, byte 3 in position 1, byte 0 in position 2, and byte 1 in position 3. To reverse all four bytes, use S = $1B (binary 00_01_10_11).

MOVBYTS is useful for byte-order conversions (endianness swapping), color channel reordering in pixel data, and general byte permutation operations. It executes in 2 clock cycles, making it an efficient alternative to multiple shift and mask operations.

Common patterns include:

- S = $E4 (binary 11_10_01_00): No change (identity)
- S = $1B (binary 00_01_10_11): Reverse bytes (big/little endian swap)
- S = $B1 (binary 10_11_00_01): Swap bytes within each word
- S = $4E (binary 01_00_11_10): Swap words



::: instrheader
## MUL {#mul}
Multiply

[Arithmetic Operations](#arithmetic-operations) - Multiplies two 16-bit unsigned values, producing 32-bit result.
:::

**MUL**  *Dest, {#}Src*  **{WZ}**

**Operation:** `D = unsigned(D[15:0] * S[15:0])`; `Z = (S==0 OR D==0)`

**Result:** The 32-bit unsigned product of the lower 16 bits of Dest and Src is stored in Dest.

- Dest is a register containing the 16-bit value to multiply with Src, and is where the 32-bit result is written.
- Src is a register, 9-bit literal, or 16-bit augmented literal whose lower 16 bits are multiplied with Dest.
- WZ is an optional effect to update the Z flag.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010000 | 0ZI | DDDDDDDDD | SSSSSSSSS | --- | (S == 0) OR (D == 0) | D | 2 |


**Related:** [MULS](#muls), [QMUL](#qmul), [SCA](#sca), [SCAS](#scas)

**Explanation:**

MUL performs an unsigned 16-bit by 16-bit multiplication, taking only the lower 16 bits from each of Dest and Src, multiplying them together, and storing the full 32-bit unsigned product into Dest. This is a fast 2-clock multiplication operation suitable for small integer arithmetic and fixed-point calculations.

The operation is: D = unsigned(D[15:0] * S[15:0]). The upper 16 bits of both Dest and Src are ignored during the multiplication, but the full 32-bit result can utilize all bits in the destination register. For example, multiplying $0001_8000 by $0002_4000 produces $2000_0000 (using only the $8000 and $4000 values).

If the WZ effect is specified, the Z flag is set (1) if either Dest or Src equals zero before the multiplication, or is cleared (0) if both are non-zero. Note that this tests the pre-multiplication values, not the result, providing a quick way to detect zero operands.

MUL is commonly used for scaling operations in fixed-point arithmetic:

```pasm2
        mov     value, ##1000           ' Value = 1000
        mul     value, #25              ' Multiply by 25: value = 25000
```

For fixed-point math with 16-bit fractional parts:

```pasm2
        ' Multiply two 16.16 fixed-point numbers
        ' Result in upper 16 bits needs shifting
        mov     temp, frac1
        mul     temp, frac2             ' temp = product (low 16 of each)
        shr     temp, #16               ' Adjust for fixed-point scale
```

For this multiply-then-shift-by-16 scaling pattern, SCA performs the same work in a single instruction: SCA computes `unsigned(D[15:0] * S[15:0]) >> 16` and substitutes the result directly as the next instruction's S operand.

For multiplications larger than 16x16 bits, use the CORDIC solver QMUL instruction, which can multiply full 32-bit values and produces a 64-bit result accessible through the upper and lower result registers. MUL's 2-clock speed makes it ideal when the operands are known to fit in 16 bits.



::: instrheader
## MULPIX {#mulpix}
Multiply Pixels

[Color Space and Pixel Operations](#color-space-and-pixel-operations) - Multiplies corresponding pixel bytes in parallel.
:::

**MULPIX**  *D,{#}S*

**Operation:** for each byte n: `D.BYTE[n] = D.BYTE[n] * S.BYTE[n]` as fractions ($FF = 1.0, $00 = 0.0)

**Result:** Each byte of S is multiplied with the corresponding byte of D, with results stored in D.

- D is a register containing four pixel bytes to be multiplied.
- S is a register, 9-bit literal, or 32-bit augmented literal containing four pixel bytes as multipliers.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010010 | 01I | DDDDDDDDD | SSSSSSSSS | --- | --- | D | 7 |


**Related:** [ADDPIX](#addpix), [BLNPIX](#blnpix), [MIXPIX](#mixpix), [SETPIX](#setpix)

**Explanation:**

MULPIX performs parallel multiplication on four byte pairs, treating each byte as a fractional value where $FF represents 1.0 and $00 represents 0.0. Each of the four bytes in S is multiplied with the corresponding byte in D, and the results replace the bytes in D.

The multiplication treats bytes as 8-bit fractional values in the range 0.0 to 1.0, where $FF represents 1.0 and $00 represents 0.0. For each byte position, the operation multiplies the two fractional bytes and stores the fractional product, so $FF * $FF = $FF (1.0 * 1.0 = 1.0).

MULPIX multiplies each color component of D by the corresponding component of S. For example, multiplying an RGB color by a brightness value: if D contains $80_60_40_20 (RGBA values) and S contains $80_80_80_FF (50% brightness on RGB, full alpha), each color component is reduced to 50% of its original value.

MULPIX executes in 7 clock cycles to perform all four parallel multiplications. This is significantly faster than performing four separate multiply and scale operations, making it practical for real-time graphics processing.

Common uses include:

- Color modulation (tinting): Multiply each color channel by a tint value
- Brightness adjustment: Multiply RGB by a brightness factor
- Alpha premultiplication: Multiply RGB by alpha for compositing
- Texture filtering: Combine texel colors with interpolation weights

The instruction treats all bytes independently, so it can be used for any four-byte parallel multiply operation, not just color processing.



::: instrheader
## MULS {#muls}
Multiply Signed

[Arithmetic Operations](#arithmetic-operations) - Multiplies two signed 16-bit values, producing signed 32-bit result.
:::

**MULS**  *Dest, {#}Src*  **{WZ}**

**Operation:** `D = signed(D[15:0] * S[15:0])`; `Z = (S==0 OR D==0)`

**Result:** The 32-bit signed product of the signed lower 16 bits of Dest and Src is stored in Dest.

- Dest is a register containing the signed 16-bit value to multiply with Src, and is where the signed 32-bit result is written.
- Src is a register, 9-bit literal, or signed 16-bit augmented literal whose lower 16 bits are multiplied with Dest.
- WZ is an optional effect to update the Z flag.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010000 | 1ZI | DDDDDDDDD | SSSSSSSSS | --- | (S == 0) OR (D == 0) | D | 2 |


**Related:** [MUL](#mul), [QMUL](#qmul), [SCA](#sca), [SCAS](#scas)

**Explanation:**

MULS performs a signed 16-bit by 16-bit multiplication, taking only the lower 16 bits from each of Dest and Src as signed values, multiplying them together, and storing the full signed 32-bit product into Dest. This is a fast 2-clock multiplication operation suitable for signed integer arithmetic and signed fixed-point calculations.

The operation is: D = signed(D[15:0] * S[15:0]). The upper 16 bits of both Dest and Src are ignored during the multiplication. The lower 16 bits are treated as signed values (using two's complement representation), so values from $8000 (-32768) to $7FFF (+32767) are valid inputs. The 32-bit result is the sign-extended product of the two signed 16-bit operands.

For example, multiplying $FFFF_8000 (-32768 in lower 16 bits) by $0000_0002 (+2) produces $FFFF_0000 (-65536 as a signed 32-bit value). The upper 16 bits of the operands are ignored.

If the WZ effect is specified, the Z flag is set (1) if either Dest or Src equals zero before the multiplication, or is cleared (0) if both are non-zero. Note that this tests the pre-multiplication values, not the result, providing a quick way to detect zero operands.

Signed scaling example:

```pasm2
        mov     velocity, signed_speed
        muls    velocity, time          ' velocity = speed * time (signed)
```

For signed fixed-point math with 16-bit fractional parts:

```pasm2
        ' Multiply two signed 16.16 fixed-point numbers
        mov     temp, signed_frac1
        muls    temp, signed_frac2      ' Signed multiplication
        sar     temp, #16               ' Arithmetic shift to preserve sign
```

For this signed multiply-then-shift pattern, SCAS does signed scaled multiply in one instruction: `signed(D[15:0] * S[15:0]) >> 14`, where `$4000` represents 1.0, substituting the result into the next instruction's S operand.

MULS differs from MUL only in that it treats the 16-bit operands as signed values rather than unsigned. The choice between them depends on whether the values being multiplied represent signed or unsigned quantities.

For multiplications larger than 16x16 bits, use the CORDIC solver QMUL instruction, which can multiply full signed 32-bit values and produces a signed 64-bit result accessible through the upper and lower result registers.



::: instrheader
## MUXC / MUXNC / MUXZ / MUXNZ {#muxc}
Multiplex Flag To Bits

[Arithmetic Operations](#arithmetic-operations) - Sets selected bits to a flag value based on mask.
:::

\hypertarget{muxnc}{}\hypertarget{muxz}{}\hypertarget{muxnz}{}

**MUXC**  *D,{#}S*  **{WC|WZ|WCZ}**\
**MUXNC**  *D,{#}S*  **{WC|WZ|WCZ}**\
**MUXZ**  *D,{#}S*  **{WC|WZ|WCZ}**\
**MUXNZ**  *D,{#}S*  **{WC|WZ|WCZ}**

**Operation:** `D = (!S & D) | (S & {32{src}})` where src = C/!C/Z/!Z; `C = parity of result`

**Result:** Each bit position in D where S has a 1 is set to the specified flag value. Optionally sets C to parity and Z if result is zero.

- D is a register whose bits will be set to the flag value where S has 1 bits.
- S is a register, 9-bit literal, or 32-bit augmented literal that selects which bits to modify.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0101100 | CZI | DDDDDDDDD | SSSSSSSSS | parity of result | result == 0 | D | 2 |
| EEEE | 0101101 | CZI | DDDDDDDDD | SSSSSSSSS | parity of result | result == 0 | D | 2 |
| EEEE | 0101110 | CZI | DDDDDDDDD | SSSSSSSSS | parity of result | result == 0 | D | 2 |
| EEEE | 0101111 | CZI | DDDDDDDDD | SSSSSSSSS | parity of result | result == 0 | D | 2 |


**Related:** [MUXQ](#muxq), [TESTB](#testb), [TESTBN](#testbn)

**Explanation:**

These instructions modify selected bits in D based on a flag value:

| Instruction | Sets bits to |
|-------------|--------------|
| MUXC | C flag value |
| MUXNC | !C (inverted C) |
| MUXZ | Z flag value |
| MUXNZ | !Z (inverted Z) |

For each bit position where S contains a 1, the corresponding bit in D is replaced with the flag value (or its inverse). All other bits in D remain unchanged. The operation is: D = (!S & D) | (S & {32{flag}}).

MUXC and MUXZ copy the direct flag value; MUXNC and MUXNZ copy the inverted flag value.

Example: Conditionally set bits based on a comparison:

```pasm2
        cmp     value, limit  wc        ' Set C if value < limit
        muxc    status, #$01            ' Set bit 0 if less than
        muxnc   status, #$02            ' Set bit 1 if greater or equal
```

If the WC or WCZ effect is specified, the C flag is set to the parity of the result. If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero.

These instructions provide an efficient alternative to conditional branches when setting bits based on flag states.



::: instrheader
## MUXNIBS {#muxnibs}
Multiplex Nibbles

[Arithmetic Operations](#arithmetic-operations) - Replaces nibbles in Dest where Src nibbles are non-zero.
:::

**MUXNIBS**  *Dest, {#}Src*

**Operation:** for each nibble n (0..7): if `S.NIBBLE[n] != 0` then `D.NIBBLE[n] = S.NIBBLE[n]`

**Result:** Each non-zero nibble in Src replaces the corresponding nibble in Dest.

- Dest is a register whose nibbles will be updated from Src.
- Src is a register, 9-bit literal, or 32-bit augmented literal containing nibble values to copy.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001111 | 01I | DDDDDDDDD | SSSSSSSSS | --- | --- | D | 2 |


**Related:** [MUXNITS](#muxnits), [MUXQ](#muxq), [MOVBYTS](#movbyts), [SPLITB](#splitb)

**Explanation:**

MUXNIBS selectively copies nibbles (4-bit fields) from Src to Dest based on whether each nibble in Src is non-zero. For each of the eight nibble positions, if the nibble in Src is non-zero, that nibble value is copied to the corresponding position in Dest. If the nibble in Src is zero, the corresponding nibble in Dest remains unchanged.

For example, if Dest = $1234_5678 and Src = $0A00_0C0D, the result is Dest = $1A34_5C7D. The nibbles at positions 6 ($A), 2 ($C), and 0 ($D) from Src are copied because they are non-zero, while positions 7, 5, 4, 3, and 1 remain unchanged in Dest because the corresponding Src nibbles are zero.

This instruction is useful for sparse updates where only certain nibbles need modification:

```pasm2
        ' Update only the changed nibbles in a configuration register
        mov     config, current_config
        muxnibs config, changes         ' Apply non-zero changes only
```

MUXNIBS is commonly used in graphics operations for palette updates, bit-field modifications where fields are naturally nibble-aligned, and efficient sparse data updates. It provides a single-instruction way to perform selective nibble replacement that would otherwise require multiple mask and merge operations.

The instruction treats nibbles independently, enabling parallel conditional updates across all eight nibble positions in a single 2-clock operation.



::: instrheader
## MUXNITS {#muxnits}
Multiplex Nits

[Arithmetic Operations](#arithmetic-operations) - Replaces bit pairs in Dest where Src bit pairs are non-zero.
:::

**MUXNITS**  *Dest, {#}Src*

**Operation:** for each 2-bit field n (0..15): if `S[2n+1:2n] != 0` then `D[2n+1:2n] = S[2n+1:2n]`

**Result:** Each non-zero bit pair in Src replaces the corresponding bit pair in Dest.

- Dest is a register whose bit pairs will be updated from Src.
- Src is a register, 9-bit literal, or 32-bit augmented literal containing bit pair values to copy.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001111 | 00I | DDDDDDDDD | SSSSSSSSS | --- | --- | D | 2 |


**Related:** [MUXNIBS](#muxnibs), [MUXQ](#muxq), [MOVBYTS](#movbyts), [SPLITB](#splitb)

**Explanation:**

MUXNITS selectively copies bit pairs (2-bit fields, called "nits") from Src to Dest based on whether each bit pair in Src is non-zero. For each of the sixteen bit pair positions, if the bit pair in Src is non-zero (01, 10, or 11), that bit pair value is copied to the corresponding position in Dest. If the bit pair in Src is zero (00), the corresponding bit pair in Dest remains unchanged.

For example, if Dest = $5555_5555 (binary 01_01_01_01... in bit pairs) and Src = $00A0_0002 (containing non-zero bit pairs at positions 11, 10, and 0), only those three bit pairs are updated in Dest while the others remain as 01.

This instruction is particularly useful for pixel graphics operations where 2-bit values represent pixel data (such as in 4-color graphics modes), sparse bit-field updates, and state machine implementations where state variables are represented as 2-bit fields.

MUXNITS provides parallel conditional updates across all sixteen bit pair positions in a single 2-clock operation:

```pasm2
        ' Update specific 2-bit fields in a packed structure
        mov     state, current_state
        muxnits state, updates          ' Apply non-zero updates only
```

The name "nits" comes from "nibble bits" or 2-bit fields, representing the next smaller grouping after nibbles (4-bit fields). This instruction complements MUXNIBS by operating at a finer granularity.



::: instrheader
## MUXQ {#muxq}
Multiplex Q

[Arithmetic Operations](#arithmetic-operations) - Copies bits from Src to Dest at positions where Q has 1 bits.
:::

**MUXQ**  *Dest, {#}Src*

**Operation:** `D = (D & !Q) | (S & Q)` (Q from prior SETQ)

**Result:** Bits from Src are copied to Dest at positions where Q has 1 bits.

- Dest is a register whose bits will be updated from Src.
- Src is a register, 9-bit literal, or 32-bit augmented literal containing bit values to copy.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001111 | 10I | DDDDDDDDD | SSSSSSSSS | --- | --- | D | 2 |


**Related:** [SETQ](#setq), [MUXC](#muxc), [MUXZ](#muxz), [MUXNIBS](#muxnibs), [MUXNITS](#muxnits)

**Explanation:**

MUXQ performs selective bit copying from Src to Dest based on a mask previously loaded into the Q register using SETQ. The mask is loaded into the Q register with SETQ executed immediately before MUXQ. For each bit position where Q contains a 1, the corresponding bit from Src is copied into Dest. For bit positions where Q contains a 0, the corresponding bit in Dest remains unchanged. The operation is: D = (!Q & D) | (Q & S).

MUXQ must be preceded by SETQ to load the mask into Q:

```pasm2
        setq    mask                    ' Load mask into Q
        muxq    dest, source            ' Copy masked bits from source
```

This provides atomic masked bit updates that are more efficient than separate AND and OR operations:

```pasm2
        ' Traditional approach (4 instructions):
        mov     temp, source            ' Copy source
        and     temp, mask              ' Extract source bits
        andn    dest, mask              ' Clear masked bits in dest
        or      dest, temp              ' Merge into dest

        ' MUXQ approach (2 instructions):
        setq    mask                    ' Set mask
        muxq    dest, source            ' Atomic masked copy
```

MUXQ is critical for parallel I/O operations, especially driving multiple pins simultaneously:

```pasm2
        ' Update multiple RGB LED pins atomically
        setq    rgb_mask                ' Mask for RGB pins
        muxq    outa, rgb_data          ' Update all RGB pins together
```

The Q register mask enables masked bit manipulation:

```pasm2
        ' Update specific configuration bits
        setq    ##$00FF_FF00            ' Mask for middle bytes
        muxq    config, new_values      ' Update only those bytes
```

MUXQ updates multiple bits of Dest in one 2-clock operation using the Q register as a mask.

Unlike MUXC and MUXZ which replicate a single flag bit to all selected positions, MUXQ copies the actual corresponding bits from the source, enabling true parallel bit transfer operations.




