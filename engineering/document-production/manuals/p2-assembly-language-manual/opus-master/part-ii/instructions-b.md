# Instructions: B

This section contains all PASM2 instructions beginning with the letter B.



## BITC / BITNC / BITZ / BITNZ {#bitc}

Set bit(s) to flag state {#bitnc} {#bitz} {#bitnz}
[Math and Logic Instruction](#math-and-logic-instructions) - Set bit(s) to C, NC, Z, or NZ flag state.

**BITC**  *Dest, {#}Src*  **{WCZ}**
**BITNC**  *Dest, {#}Src*  **{WCZ}**
**BITZ**  *Dest, {#}Src*  **{WCZ}**
**BITNZ**  *Dest, {#}Src*  **{WCZ}**

---

**Result:** Dest bit(s) designated by Src are set to the specified flag state:

| Instruction | Sets bits to |
|-------------|--------------|
| BITC | C flag value |
| BITNC | !C (inverted C) |
| BITZ | Z flag value |
| BITNZ | !Z (inverted Z) |

- Dest is a register whose value will have bit(s) set to the flag state.
- Src identifies the bit(s) to modify: Src[4:0] = bit number, Src[9:5] = additional contiguous bits.
- WCZ is an optional effect to update the Z flag to the original bit state.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{0100010}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{orig bit}{2}
\encodingrowcont{EEEE}{0100011}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{orig bit}{2}
\encodingrowcont{EEEE}{0100100}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{orig bit}{2}
\encodingrow{EEEE}{0100101}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{orig bit}{2}
\end{encodingtable}
```

**Related:** [BITH](#bith), [BITL](#bitl), [BITNOT](#bitnot), [BITRND](#bitrnd)

**Explanation:**

These instructions set designated bit(s) in Dest to the specified flag value. BITC and BITZ copy the direct flag state; BITNC and BITNZ copy the inverted flag state.

Src[4:0] indicates the bit number (0-31). For a range, Src[9:5] specifies additional contiguous bits (1-31). A SETQ instruction preceding these can substitute its Dest[4:0] for Src[9:5].

If WCZ is specified, the Z flag is set (1) if the original base bit was set, or cleared (0) if it was clear.



## BITH {#bith}

Bit high
[Math and Logic Instruction](#math-and-logic-instructions) - Set bit(s) to high (1).

**BITH**  *Dest, {#}Src*  **{WCZ}**

---

**Result:** Dest bit(s) designated by Src are set to high (1).

- Dest is a register whose value will have one or more bits set high.
- Src is a register, 9-bit literal, or 10-bit augmented literal whose value identifies the bit(s) to modify.
- WCZ is an optional effect to update the Z flag.

```{=latex}
\simpleencoding{EEEE}{0100001}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{original D[S[4:0]]}{2}
```

**Related:** [BITL](#bitl), [BITNOT](#bitnot), [BITC](#bitc), [BITNC](#bitnc), [BITZ](#bitz), [BITNZ](#bitnz)

**Explanation:**

BITH sets the Dest bit(s) designated by Src to high (1). All other bits are left unchanged.

Src[4:0] indicates the bit number (0-31). For a range of bits, Src[4:0] indicates the base bit number and Src[9:5] indicates how many contiguous bits beyond the base should be affected (1-31). A 9-bit literal Src is enough to express the base bit (Src[4:0]) and a range of up to 16 contiguous bits (Src[8:5]). If needed, use the augmented literal feature (##Src) to augment Src to a 10-bit literal value.

When Src is a register, the register's value bits [9:0] are used as-is, unless a SETQ instruction immediately precedes BITH, substituting SETQ's Dest[4:0] in place of value bits[9:5].

If the WCZ effect is specified, the Z flag is set (1) if the original Dest base bit (before modification) was set, or is cleared (0) if it was clear. This preserves information about the original bit state before it was set high.



## BITL {#bitl}

Bit low
[Math and Logic Instruction](#math-and-logic-instructions) - Set bit(s) to low (0).

**BITL**  *Dest, {#}Src*  **{WCZ}**

---

**Result:** Dest bit(s) designated by Src are set to low (0).

- Dest is a register whose value will have one or more bits set low.
- Src is a register, 9-bit literal, or 10-bit augmented literal whose value identifies the bit(s) to modify.
- WCZ is an optional effect to update the Z flag.

```{=latex}
\simpleencoding{EEEE}{0100000}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{original D[S[4:0]]}{2}
```

**Related:** [BITH](#bith), [BITNOT](#bitnot), [BITC](#bitc), [BITNC](#bitnc), [BITZ](#bitz), [BITNZ](#bitnz)

**Explanation:**

BITL sets the Dest bit(s) designated by Src to low (0). All other bits are left unchanged.

Src[4:0] indicates the bit number (0-31). For a range of bits, Src[4:0] indicates the base bit number and Src[9:5] indicates how many contiguous bits beyond the base should be affected (1-31). A 9-bit literal Src is enough to express the base bit (Src[4:0]) and a range of up to 16 contiguous bits (Src[8:5]). If needed, use the augmented literal feature (##Src) to augment Src to a 10-bit literal value.

When Src is a register, the register's value bits [9:0] are used as-is, unless a SETQ instruction immediately precedes BITL, substituting SETQ's Dest[4:0] in place of value bits[9:5].

If the WCZ effect is specified, the Z flag is set (1) if the original Dest base bit (before modification) was set, or is cleared (0) if it was clear. This preserves information about the original bit state before it was cleared to low.



## BITNOT {#bitnot}

Bit not
[Math and Logic Instruction](#math-and-logic-instructions) - Toggle bit(s) to the opposite state.

**BITNOT**  *Dest, {#}Src*  **{WCZ}**

---

**Result:** Dest bit(s) designated by Src are toggled to their opposite state(s).

- Dest is a register whose value will have one or more bits toggled.
- Src is a register, 9-bit literal, or 10-bit augmented literal whose value identifies the bit(s) to modify.
- WCZ is an optional effect to update the C and Z flags.

```{=latex}
\simpleencoding{EEEE}{0100111}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{original D[S[4:0]]}{2}
```

**Related:** [BITH](#bith), [BITL](#bitl), [BITC](#bitc), [BITNC](#bitnc), [BITZ](#bitz), [BITNZ](#bitnz), [BITRND](#bitrnd)

**Explanation:**

BITNOT alters the Dest bit(s) designated by Src to their inverse state. All other bits are left unchanged.

Src[4:0] indicates the bit number (0-31). For a range of bits, Src[4:0] indicates the base bit number and Src[9:5] indicates how many contiguous bits beyond the base should be affected (1-31). A 9-bit literal Src is enough to express the base bit (Src[4:0]) and a range of up to 16 contiguous bits (Src[8:5]). If needed, use the augmented literal feature (##Src) to augment Src to a 10-bit literal value.

When Src is a register, the register's value bits [9:0] are used as-is, unless a SETQ instruction immediately precedes BITNOT, substituting SETQ's Dest[4:0] in place of value bits[9:5].

If the WCZ effect is specified, the C and Z flags are set (1) if the original Dest base bit (before modification) was set, or are cleared (0) if it was clear. This preserves information about the original bit state.



## BITRND {#bitrnd}

Bit random
[Math and Logic Instruction](#math-and-logic-instructions) - Set bit(s) to random low or high values.

**BITRND**  *Dest, {#}Src*  **{WCZ}**

---

**Result:** Dest bit(s) designated by Src are each set randomly to low or high.

- Dest is a register whose value will have one or more bits set randomly low or high.
- Src is a register, 9-bit literal, or 10-bit augmented literal whose value identifies the bit(s) to modify.
- WCZ is an optional effect to update the C and Z flags.

```{=latex}
\simpleencoding{EEEE}{0100110}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{original D[S[4:0]]}{original D[S[4:0]]}{2}
```

**Related:** [BITZ](#bitz), [BITNZ](#bitnz), [BITC](#bitc), [BITNC](#bitnc), [BITH](#bith), [BITL](#bitl), [BITNOT](#bitnot)

**Explanation:**

BITRND alters the Dest bit(s) designated by Src to each be an independent random low or high value, based on bit(s) from the Xoroshiro128** PRNG. All other bits are left unchanged.

Src[4:0] indicates the bit number (0-31). For a range of bits, Src[4:0] indicates the base bit number and Src[9:5] indicates how many contiguous bits beyond the base should be affected (1-31). A 9-bit literal Src is enough to express the base bit (Src[4:0]) and a range of up to 16 contiguous bits (Src[8:5]). If needed, use the augmented literal feature (##Src) to augment Src to a 10-bit literal value.

When Src is a register, the register's value bits [9:0] are used as-is, unless a SETQ instruction immediately precedes BITRND, substituting SETQ's Dest[4:0] in place of value bits[9:5].

If the WCZ effect is specified, the C and Z flags are set (1) if the original Dest base bit (before modification) was set, or are cleared (0) if it was clear. This preserves information about the original state of the base bit before randomization.

Each bit in the range is set independently from the PRNG, producing true random values suitable for cryptographic initialization vectors, random number generation, and simulation applications.



## BLNPIX {#blnpix}

Blend pixels
[Pixel Mixer Instruction](#pixel-mixer-instructions) - Alpha-blend RGB bytes using SETPIV value.

**BLNPIX**  *Dest, {#}Src*

---

**Result:** Src color value bytes are alpha-blended into Dest color value bytes using the SETPIV blend factor.

- Dest is a register containing the RGB color value to blend Src into, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose RGB color value bytes are blended into Dest.

```{=latex}
\simpleencoding{EEEE}{1010010}{10I}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{7}
```

**Related:** [ADDPIX](#addpix), [SUBPIX](#subpix), [MULPIX](#mulpix), [SETPIV](#setpiv)

**Explanation:**

BLNPIX alpha-blends the individual RGB (red, green, blue) color values of Src into that of Dest and stores the result in the Dest register. The blend factor is set by a previous SETPIV instruction.

The alpha-blending operation combines the two color values based on the blend factor, allowing smooth color transitions and transparency effects. A blend factor of 0 leaves Dest unchanged, while a blend factor of 255 completely replaces Dest with Src. Values between 0 and 255 produce proportional blends.

The instruction processes all three color channels (and alpha if present) in parallel, completing in 7 clock cycles. This enables efficient pixel manipulation for graphics applications, user interfaces, and visual effects.



## BMASK {#bmask}

Bit mask
[Math and Logic Instruction](#math-and-logic-instructions) - Generate an LSB-justified bit mask.

**BMASK**  *Dest, {#}Src*
**BMASK**  *Dest*

---

**Result:** Bit mask of size Src+1, or Dest+1 (1 to 32 bits) is stored into Dest.

- Dest is a register in which to store the generated bit mask and optionally contains the 5-bit mask size (second syntax).
- Src is a register or 5-bit literal whose value is the size of the bit mask to generate.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1001110}{01I}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{2}
\encodingrow{EEEE}{1001110}{010}{DDDDDDDDD}{DDDDDDDDD}{D}{---}{---}{2}
\end{encodingtable}
```

**Related:** [ENCOD](#encod), [DECOD](#decod), [ONES](#ones), [ZEROX](#zerox)

**Explanation:**

BMASK generates an LSB-justified bit mask (all ones) of Src+1 or Dest+1 length and stores it in Dest. The size value, whether specified by Src or Dest, is in the range 0-31 to generate 1 to 32 bits of bit mask.

In effect, Dest becomes (%10 << size) - 1 via the BMASK instruction. A size value of 0 generates a 1-bit mask (%1), a size value of 5 generates a 6-bit mask (%111111), and a size value of 15 generates a 16-bit mask (%1111_1111_1111_1111).

A bit mask is often useful in bitwise operations (AND, OR, XOR) to filter out or affect special groups of bits. For example:

```pasm
        bmask   mask, #7               ' Create 8-bit mask ($FF)
        and     data, mask             ' Keep only lower 8 bits
```

The first syntax form uses Src to specify the size, while the second syntax form (without Src) uses the value already in Dest to determine the mask size. Both forms write the resulting mask back to Dest.



## BRK {#brk}

Break
[Interrupt Instruction](#interrupt-instructions) - Trigger breakpoint in current COG.

**BRK**  *{#}Dest*

---

**Result:** If debug interrupts are enabled, a debug interrupt is triggered in the current COG and Dest's value becomes the debug code or the next debug condition.

- Dest is a register, 9-bit literal, or 32-bit augmented literal whose value becomes the debug code or condition depending on the state of execution (outside or inside of a Debug ISR).

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000110110}{---}{---}{---}{2}
```

**Related:** [GETBRK](#getbrk), [COGBRK](#cogbrk)

**Explanation:**

BRK triggers a breakpoint in the current COG and either defines a breakpoint code or the next breakpoint condition(s). The COG must have debug interrupts enabled, and if BRK is to be executed within the normal program (outside the Debug ISR), the "BRK instruction" interrupt must first be enabled from within a prior Debug ISR.

During normal program execution, the BRK instruction is used to generate a debug interrupt with an 8-bit code (from Dest[7:0]) which can be read within the Debug ISR using a GETBRK instruction. This allows the program to communicate debug information or trigger specific breakpoint handlers.

During a Debug ISR, the BRK instruction is used instead to establish the next debug interrupt condition(s) and to select INA/INB, instead of the IJMP0/IRET0 registers exposed during the ISR, so that the pins' inputs states may be read.

The format of Dest for Debug ISR use is %AAAAAAAAAAAAAAAAAAAA_BCDEFGHIJKLM where A is the 20-bit breakpoint address or 4-bit event code, and bits B-M control various interrupt enable conditions.

BRK is essential for interactive debugging, allowing precise control over program execution and inspection of program state at specific points or conditions.


