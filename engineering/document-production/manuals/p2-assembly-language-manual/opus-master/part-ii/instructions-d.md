# Instructions: D

This section contains all PASM2 instructions beginning with the letter D.

**Conditional Jump Timing Convention:** Conditional jumps in this section (DJZ, DJNZ, DJF, DJNF) show their `Clks` field as `not-taken / taken`. The *taken* value depends on execution context:

| Context | Clocks when taken |
|:--------|:----------------:|
| Cog / LUT execution | 4 |
| Hub execution | 13...20 |

So `2 or 4 / 2 or 13-20` reads as: 2 cycles when the jump is not taken, 4 cycles when taken in cog/LUT, 13–20 cycles when taken in hub execution.



::: instrheader
## DECMOD {#decmod}
Decrement Modulus

[Arithmetic Operations](#arithmetic-operations) - Decrements with modulus wrap-around from zero to a maximum.
:::

**DECMOD**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

**Operation:** if D == 0 then `D = S`, `C = 1`, else `D = D - 1`, `C = 0`

**Result:** If Dest was not equal to 0, it is decremented by 1; otherwise Dest is reset to Src.

- Dest is a register containing the value to decrement down to 0 with modulus, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is the modulus limit to apply to Dest's decrement operation.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0111001 | CZI | DDDDDDDDD | SSSSSSSSS | D was 0 | result == 0 | D | 2 |


**Related:** [INCMOD](#incmod)

**Explanation:**

DECMOD compares Dest with 0—if not equal, it decrements Dest; otherwise it sets Dest equal to Src. If Dest begins in the range 0 to Src, iterations of DECMOD will decrement Dest repetitively from Src to 0.

If the WC or WCZ effect is specified, the C flag is set (1) if Dest was equal to 0 and subsequently reset to Src, or is cleared (0) if not reset. This indicates that the modulus wrapping occurred.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result is zero, or is cleared (0) if it is non-zero.

DECMOD does not limit Dest within the specified range—if Dest begins as greater than Src, iterations will continue to decrement it down through Src before cycling from Src to 0. This instruction is useful for implementing circular buffers and modular counters that wrap from 0 back to a maximum value.



::: instrheader
## DECOD {#decod}
Decode Bit Position

[Arithmetic Operations](#arithmetic-operations) - Generates a bitmask with a single bit set at the specified position.
:::

**DECOD**  *Dest, {#}Src*\
**DECOD**  *Dest*

**Operation:** `D = 1 << S[4:0]`

**Result:** A 32-bit value, with the bit position corresponding to Src or Dest value (0-31) set high, is stored in Dest.

- Dest is the register in which to store the decoded value and optionally begins by containing the 5-bit bit position value it is requesting (syntax 2).
- Src is an optional register or 5-bit literal whose value is the bit position to set high in the decoded value.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001110 | 00I | DDDDDDDDD | SSSSSSSSS | --- | --- | D | 2 |
| EEEE | 1001110 | 000 | DDDDDDDDD | DDDDDDDDD | --- | --- | D | 2 |


**Related:** [ENCOD](#encod), [BMASK](#bmask)

**Explanation:**

DECOD generates a 32-bit value with just one bit high, corresponding to the Src or Dest value (0-31) and stores that result in Dest. In effect, Dest becomes %1 << value via the DECOD instruction, where value is Src[4:0] or Dest[4:0].

Examples of decoded values:

- A value of 0 generates %00000000_00000000_00000000_00000001
- A value of 5 generates %00000000_00000000_00000000_00100000
- A value of 15 generates %00000000_00000000_10000000_00000000

The first syntax form uses Src to specify the bit position, while the second syntax form uses Dest[4:0] as both the input bit position and the destination for the result.

DECOD is the complement of ENCOD. It is commonly used to generate bit masks for testing or setting individual bits within registers or memory locations.



::: instrheader
## DIRC / DIRNC {#dirc}
Set Pin Direction by C flag

[Pin I/O and smart pins](#pin-io-and-smart-pins) - Sets pin direction based on C flag state.
:::

\hypertarget{dirnc}{}

**DIRC**  *{#}Dest*  **{WCZ}**\
**DIRNC**  *{#}Dest*  **{WCZ}**

**Operation:** `DIR[pin range] = src` (DIRC src=C, DIRNC src=!C); `C,Z = DIR bit`

**Result:** The I/O pin direction bit(s), described by Dest, are set to output/input according to C or !C; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to output or input.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000010 | DIR bit† | DIR bit† | DIR bit | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000011 | DIR bit† | DIR bit† | DIR bit | 2 |

† Original direction state of the base pin (D[5:0]) before instruction executes.

**Related:** [DIRZ](#dirz), [DIRNZ](#dirnz), [DIRL](#dirl), [DIRH](#dirh), [DIRNOT](#dirnot), [DIRRND](#dirrnd)

**Explanation:**

DIRC or DIRNC alters the direction register's bit(s) designated by Dest to equal the state, or inverse state, of the C flag. All other bits are left unchanged.

DIRC sets the pin(s) to the direction indicated by the C flag: high (1) sets the pin(s) to output, low (0) to input. DIRNC inverts this relationship, setting the pin(s) according to the inverse of the C flag (!C).

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

When Dest is a register, the register's value bits [10:0] are used as-is to form the 11-bit ID range, unless a SETQ instruction immediately precedes the DIRC or DIRNC instruction; substituting SETQ's Dest[4:0] in place of value bits[10:6], for DIRC or DIRNC's use.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group (DIRA or DIRB); it will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are updated to the original state of DIRA / DIRB's base bit, identified by Dest.



::: instrheader
## DIRH {#dirh}
Set Pin Direction High

[Pin I/O and smart pins](#pin-io-and-smart-pins) - Sets pins to output direction.
:::

**DIRH**  *{#}Dest*  **{WCZ}**

**Operation:** `DIR[pin range] = 1`; `C,Z = DIR bit`

**Result:** The I/O pins described by Dest are set to output direction; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to output.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000001 | DIR bit† | DIR bit† | DIR bit | 2 |

† Original direction state of the base pin (D[5:0]) before instruction executes.

**Related:** [DIRL](#dirl), [DIRC](#dirc), [DIRNC](#dirnc), [DIRZ](#dirz), [DIRNZ](#dirnz)

**Explanation:**

DIRH sets the direction register's bit(s) designated by Dest to high (1), making the pin(s) outputs. All other direction bits are left unchanged.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

If the WCZ effect is specified, the C flag is set to the original state of the base direction bit, and Z is set to the same value.



::: instrheader
## DIRL {#dirl}
Set Pin Direction Low

[Pin I/O and smart pins](#pin-io-and-smart-pins) - Sets pins to input direction.
:::

**DIRL**  *{#}Dest*  **{WCZ}**

**Operation:** `DIR[pin range] = 0`; `C,Z = DIR bit`

**Result:** The I/O pins described by Dest are set to input direction; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to input.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000000 | DIR bit† | DIR bit† | DIR bit | 2 |

† Original direction state of the base pin (D[5:0]) before instruction executes.

**Related:** [DIRH](#dirh), [DIRC](#dirc), [DIRNC](#dirnc), [DIRZ](#dirz), [DIRNZ](#dirnz)

**Explanation:**

DIRL alters the direction register's bit(s) designated by Dest to be low (0), setting the I/O pin(s) to input mode. The rest of the direction bits are left as-is.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

If the WCZ effect is specified, the C flag is set to the original state of the base direction bit, and Z is set to the same value.



::: instrheader
## DIRNOT {#dirnot}
Direction Not

[Pin I/O and smart pins](#pin-io-and-smart-pins) - Toggles pin direction to opposite state.
:::

**DIRNOT**  *{#}Dest*  **{WCZ}**

**Operation:** toggle `DIR[pin range]`; `C,Z = DIR bit`

**Result:** The I/O pin direction bit(s), described by Dest, are toggled to their opposite state(s); the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to toggle to the opposite direction.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000111 | DIR bit† | DIR bit† | DIR bit | 2 |

† Original direction state of the base pin (D[5:0]) before instruction executes.

**Related:** [DIRRND](#dirrnd), [DIRL](#dirl), [DIRH](#dirh), [DIRC](#dirc), [DIRNC](#dirnc), [DIRZ](#dirz), [DIRNZ](#dirnz)

**Explanation:**

DIRNOT alters the direction register's bit(s) designated by Dest to their inverse state. All other bits are left unchanged. Pins that were outputs become inputs, and pins that were inputs become outputs.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

When Dest is a register, the register's value bits [10:0] are used as-is to form the 11-bit ID range, unless a SETQ instruction immediately precedes the DIRNOT instruction; substituting SETQ's Dest[4:0] in place of value bits[10:6], for DIRNOT's use.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group (DIRA or DIRB); it will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are updated to the original state of DIRA / DIRB's base bit, identified by Dest.



::: instrheader
## DIRZ / DIRNZ {#dirz}
Set Pin Direction by Z flag

[Pin I/O and smart pins](#pin-io-and-smart-pins) - Sets pin direction based on Z flag state.
:::

\hypertarget{dirnz}{}

**DIRZ**  *{#}Dest*  **{WCZ}**\
**DIRNZ**  *{#}Dest*  **{WCZ}**

**Operation:** `DIR[pin range] = src` (DIRZ src=Z, DIRNZ src=!Z); `C,Z = DIR bit`

**Result:** The I/O pin direction bit(s), described by Dest, are set to output/input according to Z or !Z; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to output or input.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000100 | DIR bit† | DIR bit† | DIR bit | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000101 | DIR bit† | DIR bit† | DIR bit | 2 |

† Original direction state of the base pin (D[5:0]) before instruction executes.

**Related:** [DIRC](#dirc), [DIRNC](#dirnc), [DIRNOT](#dirnot), [DIRRND](#dirrnd), [DIRL](#dirl), [DIRH](#dirh)

**Explanation:**

DIRZ or DIRNZ alters the direction register's bit(s) designated by Dest to equal the state, or inverse state, of the Z flag. All other bits are left unchanged.

DIRZ sets the pin(s) to the direction indicated by the Z flag: high (1) sets the pin(s) to output, low (0) to input. DIRNZ inverts this relationship, setting the pin(s) according to the inverse of the Z flag (!Z).

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

When Dest is a register, the register's value bits [10:0] are used as-is to form the 11-bit ID range, unless a SETQ instruction immediately precedes the DIRZ or DIRNZ instruction; substituting SETQ's Dest[4:0] in place of value bits[10:6], for DIRZ or DIRNZ's use.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group (DIRA or DIRB); it will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are updated to the original state of DIRA / DIRB's base bit, identified by Dest.



::: instrheader
## DIRRND {#dirrnd}
Direction Random

[Pin I/O and smart pins](#pin-io-and-smart-pins) - Sets pin direction to random state.
:::

**DIRRND**  *{#}Dest*  **{WCZ}**

**Operation:** `DIR[pin range] = RND`; `C,Z = DIR bit`

**Result:** The I/O pin direction bit(s), described by Dest, are each set randomly low or high (input or output); the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set randomly to input or output.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000110 | DIR bit† | DIR bit† | DIR bit | 2 |

† Original direction state of the base pin (D[5:0]) before instruction executes.

**Related:** [DIRC](#dirc), [DIRNC](#dirnc), [DIRZ](#dirz), [DIRNZ](#dirnz), [DIRNOT](#dirnot), [DIRL](#dirl), [DIRH](#dirh)

**Explanation:**

DIRRND alters the direction register's bit(s) designated by Dest to be random low and high (input and output), based on bit(s) from the Xoroshiro128** PRNG. All other bits are left unchanged.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

When Dest is a register, the register's value bits [10:0] are used as-is to form the 11-bit ID range, unless a SETQ instruction immediately precedes the DIRRND instruction; substituting SETQ's Dest[4:0] in place of value bits[10:6], for DIRRND's use.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group (DIRA or DIRB); it will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are updated to the original state of DIRA / DIRB's base bit, identified by Dest, before the random modification occurs.



::: instrheader
## DJF {#djf}
Decrement and Jump If Full

[Branching and Flow Control](#branching-and-flow-control) - Decrements and jumps if result wraps to $FFFFFFFF.
:::

**DJF**  *Dest, {#}Src*

**Operation:** `D = D - 1`; jump to S if D == $FFFF_FFFF

**Result:** Dest is decremented. If the result equals $FFFF_FFFF (full), PC is set to a new relative (#Src) or absolute (Src) address; otherwise execution continues with the next instruction.

- Dest is a register whose value is decremented and tested for full or not full.
- Src is a register, 9-bit literal, or 20-bit augmented literal whose value is the absolute or relative address to set PC to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011011 | 10I | DDDDDDDDD | SSSSSSSSS | --- | --- | D | 2 or 4 / 2 or 13-20 |


**Related:** [DJNF](#djnf), [DJZ](#djz), [DJNZ](#djnz)

**Explanation:**

DJF decrements the value in Dest, writes the result, and jumps to the address described by Src if the result is full ($FFFF_FFFF, or -1 signed).

This instruction is useful for implementing loops that count down until a register wraps from 0 to -1. Use # prefix on Src for relative addressing; omit # for absolute addressing.

The instruction executes in 2 clock cycles when the branch is not taken. When taken, it executes in 4 clock cycles during cog/LUT execution, or 13-20 clock cycles during hub execution.



::: instrheader
## DJNF {#djnf}
Decrement and Jump If Not Full

[Branching and Flow Control](#branching-and-flow-control) - Decrements and jumps if result does not wrap.
:::

**DJNF**  *Dest, {#}Src*

**Operation:** `D = D - 1`; jump to S if D != $FFFF_FFFF

**Result:** Dest is decremented. If the result does NOT equal $FFFF_FFFF (not full), PC is set to a new relative (#Src) or absolute (Src) address; otherwise execution continues with the next instruction.

- Dest is a register whose value is decremented and tested for full or not full.
- Src is a register, 9-bit literal, or 20-bit augmented literal whose value is the absolute or relative address to set PC to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011011 | 11I | DDDDDDDDD | SSSSSSSSS | --- | --- | D | 2 or 4 / 2 or 13-20 |


**Related:** [DJF](#djf), [DJZ](#djz), [DJNZ](#djnz)

**Explanation:**

DJNF decrements the value in Dest, writes the result, and jumps to the address described by Src if the result is NOT full (not equal to $FFFF_FFFF).

This instruction is useful for implementing loops that continue until a register wraps from 0 to -1 (full). Use # prefix on Src for relative addressing; omit # for absolute addressing.

Dest is always written with the decremented value. PC is written only when the result in Dest is not full.

The instruction executes in 2 clock cycles when the branch is not taken. When taken, it takes 4 clock cycles in cog/LUT execution, or 13–20 clock cycles in hub execution.



::: instrheader
## DJZ / DJNZ {#djz}
Decrement and Jump If Zero

[Branching and Flow Control](#branching-and-flow-control) - Decrements and conditionally jumps based on zero result.
:::

\hypertarget{djnz}{}

**DJZ**  *Dest, {#}Src*\
**DJNZ**  *Dest, {#}Src*

**Result:** Dest is decremented by 1, and conditionally jumps based on the result.

- Dest is a register whose value is decremented and tested.
- Src is the jump address: use # for relative, omit for absolute.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011011 | 00I | DDDDDDDDD | SSSSSSSSS | --- | --- | D + PC* | 2 or 4 / 2 or 13-20 |
| EEEE | 1011011 | 01I | DDDDDDDDD | SSSSSSSSS | --- | --- | D + PC* | 2 or 4 / 2 or 13-20 |

```{=latex}
*PC is written only when the jump condition is met.
```


**Related:** [DJF](#djf), [DJNF](#djnf), [IJZ](#ijz), [IJNZ](#ijnz), [TJZ](#tjz), [TJNZ](#tjnz)

**Explanation:**

DJZ and DJNZ decrement Dest and conditionally jump based on whether the result is zero or non-zero:

| Instruction | Jumps when |
|-------------|------------|
| DJZ | result == 0 |
| DJNZ | Result != 0 |

DJNZ is one of the most commonly used loop instructions—it continues looping while the counter is non-zero.

Example loop:
```pasm2
        mov     count, #10              ' Set loop counter to 10
.loop   ' loop body here
        djnz    count, #.loop           ' Decrement and loop if not zero
```

Takes 2 clocks when not jumping; when jumping, 4 clocks in cog/LUT execution or 13–20 clocks during hub execution (pipeline flush).



::: instrheader
## DRVC / DRVNC {#drvc}
Drive Pins by C flag

[Pin I/O and smart pins](#pin-io-and-smart-pins) - Drives pins high or low based on C flag state.
:::

\hypertarget{drvnc}{}

**DRVC**  *{#}Dest*  **{WCZ}**\
**DRVNC**  *{#}Dest*  **{WCZ}**

**Operation:** `OUT[pin range] = src`, `DIR[pin range] = 1` (DRVC src=C, DRVNC src=!C); `C,Z = OUT bit`

**Result:** The I/O pins described by Dest are set to the output direction and to an output level of low/high according to C or !C; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to output direction and output levels of low or high.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001011010 | OUT bit† | OUT bit† | OUT bit | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001011011 | OUT bit† | OUT bit† | OUT bit | 2 |

† Original output state of the base pin (D[5:0]) before instruction executes.

**Related:** [DRVZ](#drvz), [DRVNZ](#drvnz), [DRVH](#drvh), [DRVL](#drvl), [DRVNOT](#drvnot), [DRVRND](#drvrnd)

**Explanation:**

DRVC or DRVNC sets the I/O pin(s) designated by Dest to the output direction and to a low/high output level according to the C flag or its inverse (!C). All other pins are left unchanged.

DRVC sets the pin(s) to the output direction and to the level indicated by the C flag: high (1) for high output, low (0) for low output. DRVNC inverts this relationship, setting the output level according to the inverse of the C flag (!C).

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group; it will not cross the port boundary.

If the WCZ effect is specified, the C flag is set to the original state of the base OUT bit, and Z is set to the same value.



::: instrheader
## DRVH {#drvh}
Drive Pins High

[Pin I/O and smart pins](#pin-io-and-smart-pins) - Sets pins to output direction and drives high.
:::

**DRVH**  *{#}Dest*  **{WCZ}**

**Operation:** `OUT[pin range] = 1`, `DIR[pin range] = 1`; `C,Z = OUT bit`

**Result:** The I/O pins described by Dest are set to the output direction and to an output level of high; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to output direction and high output level.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001011001 | OUT bit† | OUT bit† | OUT bit | 2 |

† Original output state of the base pin (D[5:0]) before instruction executes.

**Related:** [DRVL](#drvl), [DRVC](#drvc), [DRVNC](#drvnc), [DRVZ](#drvz), [DRVNZ](#drvnz)

**Explanation:**

DRVH sets the I/O pin(s) designated by Dest to the output direction and to a high output level. All other pins are left unchanged.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group; it will not cross the port boundary.

If the WCZ effect is specified, the C flag is set to the original state of the base OUT bit, and Z is set to the same value.



::: instrheader
## DRVL {#drvl}
Drive Pins Low

[Pin I/O and smart pins](#pin-io-and-smart-pins) - Sets pins to output direction and drives low.
:::

**DRVL**  *{#}Dest*  **{WCZ}**

**Operation:** `OUT[pin range] = 0`, `DIR[pin range] = 1`; `C,Z = OUT bit`

**Result:** The I/O pins described by Dest are set to the output direction and to an output level of low; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to output direction and low output level.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001011000 | OUT bit† | OUT bit† | OUT bit | 2 |

† Original output state of the base pin (D[5:0]) before instruction executes.

**Related:** [DRVH](#drvh), [DRVC](#drvc), [DRVNC](#drvnc), [DRVZ](#drvz), [DRVNZ](#drvnz)

**Explanation:**

DRVL sets the I/O pin(s) designated by Dest to the output direction and to a low output level. All other pins are left unchanged.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group; it will not cross the port boundary.

If the WCZ effect is specified, the C flag is set to the original state of the base OUT bit, and Z is set to the same value.

Note that the new DIRx state is not data-forwarded; the next pipelined instruction sees the old state.



::: instrheader
## DRVNOT {#drvnot}
Drive Not

[Pin I/O and smart pins](#pin-io-and-smart-pins) - Sets pins to output direction and toggles output level.
:::

**DRVNOT**  *{#}Dest*  **{WCZ}**

**Operation:** toggle `OUT[pin range]`, `DIR[pin range] = 1`; `C,Z = OUT bit`

**Result:** The I/O pins described by Dest are set to the output direction and to their opposite output level(s); the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to the output direction and toggle to opposite output levels.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001011111 | OUT bit† | OUT bit† | OUT bit | 2 |

† Original output state of the base pin (D[5:0]) before instruction executes.

**Related:** [DRVRND](#drvrnd), [DRVH](#drvh), [DRVL](#drvl), [DRVC](#drvc), [DRVNC](#drvnc), [DRVZ](#drvz), [DRVNZ](#drvnz)

**Explanation:**

DRVNOT sets the I/O pin(s) designated by Dest to the output direction and toggles their output level(s) to the opposite state. All other pins are left unchanged. This instruction achieves the same effect as two instructions—OUTNOT followed by DIRH.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

When Dest is a register, the register's value bits [10:0] are used as-is to form the 11-bit ID range, unless a SETQ instruction immediately precedes the DRVNOT instruction; substituting SETQ's Dest[4:0] in place of value bits[10:6], for DRVNOT's use.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group (DIRA or DIRB and OUTA or OUTB); it will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are updated to the original state of OUTA / OUTB's base bit, identified by Dest.

Note that the new DIRx state is not data-forwarded; the next pipelined instruction sees the old state.



::: instrheader
## DRVZ / DRVNZ {#drvz}
Drive Pins by Z flag

[Pin I/O and smart pins](#pin-io-and-smart-pins) - Drives pins high or low based on Z flag state.
:::

\hypertarget{drvnz}{}

**DRVZ**  *{#}Dest*  **{WCZ}**\
**DRVNZ**  *{#}Dest*  **{WCZ}**

**Operation:** `OUT[pin range] = src`, `DIR[pin range] = 1` (DRVZ src=Z, DRVNZ src=!Z); `C,Z = OUT bit`

**Result:** The I/O pins described by Dest are set to the output direction and to an output level of low/high according to Z or !Z; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to output direction and output levels of low or high.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001011100 | OUT bit† | OUT bit† | OUT bit | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001011101 | OUT bit† | OUT bit† | OUT bit | 2 |

† Original output state of the base pin (D[5:0]) before instruction executes.

**Related:** [DRVC](#drvc), [DRVNC](#drvnc), [DRVH](#drvh), [DRVL](#drvl), [DRVNOT](#drvnot), [DRVRND](#drvrnd)

**Explanation:**

DRVZ or DRVNZ sets the I/O pin(s) designated by Dest to the output direction and to a low/high output level according to the Z flag or its inverse (!Z). All other pins are left unchanged.

DRVZ sets the pin(s) to the output direction and to the level indicated by the Z flag: high (1) for high output, low (0) for low output. DRVNZ inverts this relationship, setting the output level according to the inverse of the Z flag (!Z).

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group; it will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are set to the original state of the base OUT bit.



::: instrheader
## DRVRND {#drvrnd}
Drive Random

[Pin I/O and smart pins](#pin-io-and-smart-pins) - Sets pins to output direction with random output levels.
:::

**DRVRND**  *{#}Dest*  **{WCZ}**

**Operation:** `OUT[pin range] = RND`, `DIR[pin range] = 1`; `C,Z = OUT bit`

**Result:** The I/O pins described by Dest are set to the output direction and each output level is set randomly low or high; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to the output direction and with output level(s) set randomly to low or high.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001011110 | OUT bit† | OUT bit† | DIRx, OUTx | 2 |

† Original output state of the base pin (D[5:0]) before instruction executes.

**Related:** [DRVH](#drvh), [DRVL](#drvl), [DRVC](#drvc), [DRVNC](#drvnc), [DRVZ](#drvz), [DRVNZ](#drvnz), [DRVNOT](#drvnot)

**Explanation:**

DRVRND sets the I/O pin(s) designated by Dest to the output direction and with output level(s) set randomly low and high, based on bit(s) from the Xoroshiro128** PRNG. All other pins are left unchanged. This instruction can affect one or more of the bits within the DIRA or DIRB and OUTA or OUTB registers.

DRVRND achieves the same effect as two instructions—OUTRND followed by DIRH.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

When Dest is a register, the register's value bits [10:0] are used as-is to form the 11-bit ID range, unless a SETQ instruction immediately precedes the DRVRND instruction; substituting SETQ's Dest[4:0] in place of value bits[10:6], for DRVRND's use.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group (DIRA or DIRB and OUTA or OUTB); it will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are updated to the original state of OUTA / OUTB's base bit, identified by Dest, before the random modification occurs.

Note that the new DIRx state is not data-forwarded; the next pipelined instruction sees the old state.



