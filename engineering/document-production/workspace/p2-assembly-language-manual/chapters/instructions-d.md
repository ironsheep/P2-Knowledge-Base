# Instructions: D

This section contains all PASM2 instructions beginning with the letter D.

<!-- DEBUG instruction removed - will be covered in a dedicated narrative chapter with examples -->



## DECMOD {#decmod}

Decrement modulus
[Math Instruction](\#math-instructions) - Decrement with modulus wrapping.

**DECMOD**  *Dest, {\#}Src*  **\{WC|WZ|WCZ\}**

---

**Result:** If Dest was not equal to 0, it is decremented by 1; otherwise Dest is reset to Src.

- Dest is a register containing the value to decrement down to 0 with modulus, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is the modulus limit to apply to Dest's decrement operation.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0111001}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Modulus triggered}{Result = 0}{2}
```

**Related:** [INCMOD](\#incmod)

**Explanation:**

DECMOD compares Dest with 0—if not equal, it decrements Dest; otherwise it sets Dest equal to Src. If Dest begins in the range 0 to Src, iterations of DECMOD will decrement Dest repetitively from Src to 0.

If the WC or WCZ effect is specified, the C flag is set (1) if Dest was equal to 0 and subsequently reset to Src, or is cleared (0) if not reset. This indicates that the modulus wrapping occurred.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result is zero, or is cleared (0) if it is non-zero.

DECMOD does not limit Dest within the specified range—if Dest begins as greater than Src, iterations will continue to decrement it down through Src before cycling from Src to 0. This instruction is useful for implementing circular buffers and modular counters that wrap from 0 back to a maximum value.



## DECOD {#decod}

Decode bit position to single-bit mask
[Math Instruction](\#math-instructions) - Decode value (0-31) into single-high-bit long.

**DECOD**  *Dest, {\#}Src*
**DECOD**  *Dest*

---

**Result:** A 32-bit value, with the bit position corresponding to Src or Dest value (0-31) set high, is stored in Dest.

- Dest is the register in which to store the decoded value and optionally begins by containing the 5-bit bit position value it is requesting (syntax 2).
- Src is an optional register or 5-bit literal whose value is the bit position to set high in the decoded value.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1001110}{00I}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{2}
\encodingrow{EEEE}{1001110}{000}{DDDDDDDDD}{DDDDDDDDD}{D}{---}{---}{2}
\end{encodingtable}
```

**Related:** [ENCOD](\#encod), [BMASK](\#bmask)

**Explanation:**

DECOD generates a 32-bit value with just one bit high, corresponding to the Src or Dest value (0-31) and stores that result in Dest. In effect, Dest becomes \%1 << value via the DECOD instruction, where value is Src[4:0] or Dest[4:0].

Examples of decoded values:
- A value of 0 generates \%00000000\_00000000\_00000000\_00000001
- A value of 5 generates \%00000000\_00000000\_00000000\_00100000
- A value of 15 generates \%00000000\_00000000\_10000000\_00000000

The first syntax form uses Src to specify the bit position, while the second syntax form uses Dest[4:0] as both the input bit position and the destination for the result.

DECOD is the complement of ENCOD. It is commonly used to generate bit masks for testing or setting individual bits within registers or memory locations.



## DIRC / DIRNC {#dirc}

Set pin direction if C / not C
[I/O Pin Instruction](\#io-pin-instructions) - Set pin(s) direction to input/output according to C or !C.

**DIRC**  *{\#}Dest*  **\{WCZ\}**
**DIRNC**  *{\#}Dest*  **\{WCZ\}**

---

**Result:** The I/O pin direction bit(s), described by Dest, are set to output/input according to C or !C; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to output or input.
- WCZ is an optional effect to update flags.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1101011}{CZL}{DDDDDDDDD}{001000010}{DIRx}{---}{DIR bit}{2}
\encodingrow{EEEE}{1101011}{CZL}{DDDDDDDDD}{001000011}{DIRx}{---}{DIR bit}{2}
\end{encodingtable}
```

**Related:** [DIRZ](\#dirz), [DIRNZ](\#dirnz), [DIRL](\#dirl), [DIRH](\#dirh), [DIRNOT](\#dirnot), [DIRRND](\#dirrnd)

**Explanation:**

DIRC or DIRNC alters the direction register's bit(s) designated by Dest to equal the state, or inverse state, of the C flag. All other bits are left unchanged.

DIRC sets the pin(s) to the direction indicated by the C flag: high (1) sets the pin(s) to output, low (0) to input. DIRNC inverts this relationship, setting the pin(s) according to the inverse of the C flag (!C).

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (\#\#Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

When Dest is a register, the register's value bits [10:0] are used as-is to form the 11-bit ID range, unless a SETQ instruction immediately precedes the DIRC or DIRNC instruction; substituting SETQ's Dest[4:0] in place of value bits[10:6], for DIRC or DIRNC's use.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group (DIRA or DIRB); it will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are updated to the original state of DIRA / DIRB's base bit, identified by Dest.



## DIRH {#dirh}

Set pin direction high
[I/O Pin Instruction](\#io-pin-instructions) - Set pin(s) direction to output (high; 1).

**DIRH**  *{\#}Dest*  **\{WCZ\}**

---

**Result:** The I/O pins described by Dest are set to output direction; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to output.
- WCZ is an optional effect to update flags.

```{=latex}
\simpleencoding{EEEE}{1101011}{CZL}{DDDDDDDDD}{001000001}{DIRx}{---}{DIR bit}{2}
```

**Related:** [DIRL](\#dirl), [DIRC](\#dirc), [DIRNC](\#dirnc), [DIRZ](\#dirz), [DIRNZ](\#dirnz)

**Explanation:**

DIRH sets the direction register's bit(s) designated by Dest to high (1), making the pin(s) outputs. All other direction bits are left unchanged.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (\#\#Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

If the WCZ effect is specified, the Z flag is set to the state of the direction bit before modification.



## DIRL {#dirl}

Set pin direction low
[I/O Pin Instruction](\#io-pin-instructions) - Set pin(s) direction to input (low; 0).

**DIRL**  *{\#}Dest*  **\{WCZ\}**

---

**Result:** The I/O pins described by Dest are set to input direction; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to input.
- WCZ is an optional effect to update flags.

```{=latex}
\simpleencoding{EEEE}{1101011}{CZL}{DDDDDDDDD}{001000000}{DIRx}{---}{DIR bit}{2}
```

**Related:** [DIRH](\#dirh), [DIRC](\#dirc), [DIRNC](\#dirnc), [DIRZ](\#dirz), [DIRNZ](\#dirnz)

**Explanation:**

DIRL alters the direction register's bit(s) designated by Dest to be low (0), setting the I/O pin(s) to input mode. The rest of the direction bits are left as-is.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (\#\#Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

If the WCZ effect is specified, the Z flag is updated to the original state of the target direction bit.



## DIRNOT {#dirnot}

Direction not
[I/O Pin Instruction](\#io-pin-instructions) - Toggle pin(s) to the opposite direction.

**DIRNOT**  *{\#}Dest*  **\{WCZ\}**

---

**Result:** The I/O pin direction bit(s), described by Dest, are toggled to their opposite state(s); the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to toggle to the opposite direction.
- WCZ is an optional effect to update flags.

```{=latex}
\simpleencoding{EEEE}{1101011}{CZL}{DDDDDDDDD}{001000111}{DIRx}{---}{DIR bit}{2}
```

**Related:** [DIRRND](\#dirrnd), [DIRL](\#dirl), [DIRH](\#dirh), [DIRC](\#dirc), [DIRNC](\#dirnc), [DIRZ](\#dirz), [DIRNZ](\#dirnz)

**Explanation:**

DIRNOT alters the direction register's bit(s) designated by Dest to their inverse state. All other bits are left unchanged. Pins that were outputs become inputs, and pins that were inputs become outputs.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (\#\#Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

When Dest is a register, the register's value bits [10:0] are used as-is to form the 11-bit ID range, unless a SETQ instruction immediately precedes the DIRNOT instruction; substituting SETQ's Dest[4:0] in place of value bits[10:6], for DIRNOT's use.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group (DIRA or DIRB); it will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are updated to the original state of DIRA / DIRB's base bit, identified by Dest.



## DIRZ / DIRNZ {#dirz}

Set pin direction if Z / not Z
[I/O Pin Instruction](\#io-pin-instructions) - Set pin(s) direction to input/output according to Z or !Z.

**DIRZ**  *{\#}Dest*  **\{WCZ\}**
**DIRNZ**  *{\#}Dest*  **\{WCZ\}**

---

**Result:** The I/O pin direction bit(s), described by Dest, are set to output/input according to Z or !Z; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to output or input.
- WCZ is an optional effect to update flags.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1101011}{CZL}{DDDDDDDDD}{001000100}{DIRx}{---}{DIR bit}{2}
\encodingrow{EEEE}{1101011}{CZL}{DDDDDDDDD}{001000101}{DIRx}{---}{DIR bit}{2}
\end{encodingtable}
```

**Related:** [DIRC](\#dirc), [DIRNC](\#dirnc), [DIRNOT](\#dirnot), [DIRRND](\#dirrnd), [DIRL](\#dirl), [DIRH](\#dirh)

**Explanation:**

DIRZ or DIRNZ alters the direction register's bit(s) designated by Dest to equal the state, or inverse state, of the Z flag. All other bits are left unchanged.

DIRZ sets the pin(s) to the direction indicated by the Z flag: high (1) sets the pin(s) to output, low (0) to input. DIRNZ inverts this relationship, setting the pin(s) according to the inverse of the Z flag (!Z).

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (\#\#Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

When Dest is a register, the register's value bits [10:0] are used as-is to form the 11-bit ID range, unless a SETQ instruction immediately precedes the DIRZ or DIRNZ instruction; substituting SETQ's Dest[4:0] in place of value bits[10:6], for DIRZ or DIRNZ's use.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group (DIRA or DIRB); it will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are updated to the original state of DIRA / DIRB's base bit, identified by Dest.



## DIRRND {#dirrnd}

Direction random
[I/O Pin Instruction](\#io-pin-instructions) - Set pin(s) direction to random input/output.

**DIRRND**  *{\#}Dest*  **\{WCZ\}**

---

**Result:** The I/O pin direction bit(s), described by Dest, are each set randomly low or high (input or output); the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set randomly to input or output.
- WCZ is an optional effect to update flags.

```{=latex}
\simpleencoding{EEEE}{1101011}{CZL}{DDDDDDDDD}{001000110}{DIRx}{Original DIRx base bit}{Original DIRx base bit}{2}
```

**Related:** [DIRC](\#dirc), [DIRNC](\#dirnc), [DIRZ](\#dirz), [DIRNZ](\#dirnz), [DIRNOT](\#dirnot), [DIRL](\#dirl), [DIRH](\#dirh)

**Explanation:**

DIRRND alters the direction register's bit(s) designated by Dest to be random low and high (input and output), based on bit(s) from the Xoroshiro128** PRNG. All other bits are left unchanged.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (\#\#Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

When Dest is a register, the register's value bits [10:0] are used as-is to form the 11-bit ID range, unless a SETQ instruction immediately precedes the DIRRND instruction; substituting SETQ's Dest[4:0] in place of value bits[10:6], for DIRRND's use.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group (DIRA or DIRB); it will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are updated to the original state of DIRA / DIRB's base bit, identified by Dest, before the random modification occurs.



## DJF {#djf}

Decrement and jump if full
[Branch/Jump Instruction](\#branch-jump-instructions) - Decrement value and jump if full (-1; \$FFFF\_FFFF).

**DJF**  *Dest, {\#}Src*

---

**Result:** Dest is decremented. If the result equals \$FFFF\_FFFF (full), PC is set to a new relative (\#Src) or absolute (Src) address; otherwise execution continues with the next instruction.

- Dest is a register whose value is decremented and tested for full or not full.
- Src is a register, 9-bit literal, or 20-bit augmented literal whose value is the absolute or relative address to set PC to. Use \# for relative addressing; omit \# for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011011}{10I}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{2 or 4}
```

**Related:** [DJNF](\#djnf), [DJZ](\#djz), [DJNZ](\#djnz)

**Explanation:**

DJF decrements the value in Dest, writes the result, and jumps to the address described by Src if the result is full (\$FFFF\_FFFF, or -1 signed).

This instruction is useful for implementing loops that count down until a register wraps from 0 to -1. Use \# prefix on Src for relative addressing; omit \# for absolute addressing.

The instruction executes in 2 clock cycles when the branch is not taken, and 4 clock cycles when the branch is taken.



## DJNF {#djnf}

Decrement and jump if not full
[Branch/Jump Instruction](\#branch-jump-instructions) - Decrement value and jump if not full (<> -1; <> \$FFFF\_FFFF).

**DJNF**  *Dest, {\#}Src*

---

**Result:** Dest is decremented. If the result does NOT equal \$FFFF\_FFFF (not full), PC is set to a new relative (\#Src) or absolute (Src) address; otherwise execution continues with the next instruction.

- Dest is a register whose value is decremented and tested for full or not full.
- Src is a register, 9-bit literal, or 20-bit augmented literal whose value is the absolute or relative address to set PC to. Use \# for relative addressing; omit \# for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011011}{11I}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{2 or 4}
```

**Related:** [DJF](\#djf), [DJZ](\#djz), [DJNZ](\#djnz)

**Explanation:**

DJNF decrements the value in Dest, writes the result, and jumps to the address described by Src if the result is NOT full (not equal to \$FFFF\_FFFF).

This instruction is useful for implementing loops that continue until a register wraps from 0 to -1 (full). Use \# prefix on Src for relative addressing; omit \# for absolute addressing.

Dest is always written with the decremented value. PC is written only when the result in Dest is not full.

The instruction executes in 2 clock cycles when the branch is not taken, and 4 clock cycles when the branch is taken.



## DJZ / DJNZ {#djz}

Decrement and jump if zero / not zero \{\#djnz\}
[Branch/Jump Instruction](\#branch-jump-instructions) - Decrement a register and jump based on zero/non-zero result.

**DJZ**  *Dest, {\#}Src*
**DJNZ**  *Dest, {\#}Src*

---

**Result:** Dest is decremented by 1, and conditionally jumps:

| Instruction | Jumps when |
|-------------|------------|
| DJZ | Result = 0 |
| DJNZ | Result ≠ 0 |

- Dest is a register whose value is decremented and tested.
- Src is the jump address: use \# for relative, omit for absolute.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1011011}{00I}{DDDDDDDDD}{SSSSSSSSS}{D + PC*}{---}{---}{2 or 4}
\encodingrow{EEEE}{1011011}{01I}{DDDDDDDDD}{SSSSSSSSS}{D + PC*}{---}{---}{2 or 4}
\end{encodingtable}

*PC is written only when the jump condition is met.
```

**Related:** [DJF](\#djf), [DJNF](\#djnf), [IJZ](\#ijz), [IJNZ](\#ijnz), [TJZ](\#tjz), [TJNZ](\#tjnz)

**Explanation:**

DJZ and DJNZ decrement Dest and conditionally jump based on whether the result is zero or non-zero.

DJNZ is one of the most commonly used loop instructions—it continues looping while the counter is non-zero.

Example loop:
```pasm
        mov     count, #10              ' Set loop counter to 10
.loop   ' loop body here
        djnz    count, #.loop           ' Decrement and loop if not zero
```

Takes 2 clocks when not jumping, 4 clocks when jumping (pipeline flush).



## DRVC / DRVNC {#drvc}

Drive pins if C / not C
[I/O Pin Instruction](\#io-pin-instructions) - Set pin(s) direction to output and output level to low/high according to C or !C.

**DRVC**  *{\#}Dest*  **\{WCZ\}**
**DRVNC**  *{\#}Dest*  **\{WCZ\}**

---

**Result:** The I/O pins described by Dest are set to the output direction and to an output level of low/high according to C or !C; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to output direction and output levels of low or high.
- WCZ is an optional effect to update flags.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1101011}{CZL}{DDDDDDDDD}{001011010}{DIRx* + OUTx}{---}{OUT bit}{2}
\encodingrow{EEEE}{1101011}{CZL}{DDDDDDDDD}{001011011}{DIRx* + OUTx}{---}{OUT bit}{2}
\end{encodingtable}
```

**Related:** [DRVZ](\#drvz), [DRVNZ](\#drvnz), [DRVH](\#drvh), [DRVL](\#drvl), [DRVNOT](\#drvnot), [DRVRND](\#drvrnd)

**Explanation:**

DRVC or DRVNC sets the I/O pin(s) designated by Dest to the output direction and to a low/high output level according to the C flag or its inverse (!C). All other pins are left unchanged.

DRVC sets the pin(s) to the output direction and to the level indicated by the C flag: high (1) for high output, low (0) for low output. DRVNC inverts this relationship, setting the output level according to the inverse of the C flag (!C).

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (\#\#Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group; it will not cross the port boundary.

If the WCZ effect is specified, the Z flag is set to the state of the OUT bit before modification.



## DRVH {#drvh}

Drive pins high
[I/O Pin Instruction](\#io-pin-instructions) - Set pin(s) direction to output and output level high (1).

**DRVH**  *{\#}Dest*  **\{WCZ\}**

---

**Result:** The I/O pins described by Dest are set to the output direction and to an output level of high; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to output direction and high output level.
- WCZ is an optional effect to update flags.

```{=latex}
\simpleencoding{EEEE}{1101011}{CZL}{DDDDDDDDD}{001011001}{DIRx* + OUTx}{---}{OUT bit}{2}
```

**Related:** [DRVL](\#drvl), [DRVC](\#drvc), [DRVNC](\#drvnc), [DRVZ](\#drvz), [DRVNZ](\#drvnz)

**Explanation:**

DRVH sets the I/O pin(s) designated by Dest to the output direction and to a high output level. All other pins are left unchanged.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (\#\#Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group; it will not cross the port boundary.

If the WCZ effect is specified, the Z flag is set to the state of the OUT bit before modification.



## DRVL {#drvl}

Drive pins low
[I/O Pin Instruction](\#io-pin-instructions) - Set pin(s) direction to output and output level low (0).

**DRVL**  *{\#}Dest*  **\{WCZ\}**

---

**Result:** The I/O pins described by Dest are set to the output direction and to an output level of low; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to output direction and low output level.
- WCZ is an optional effect to update flags.

```{=latex}
\simpleencoding{EEEE}{1101011}{CZL}{DDDDDDDDD}{001011000}{DIRx* + OUTx}{---}{OUT bit}{2}
```

**Related:** [DRVH](\#drvh), [DRVC](\#drvc), [DRVNC](\#drvnc), [DRVZ](\#drvz), [DRVNZ](\#drvnz)

**Explanation:**

DRVL sets the I/O pin(s) designated by Dest to the output direction and to a low output level. All other pins are left unchanged.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (\#\#Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group; it will not cross the port boundary.

If the WCZ effect is specified, the Z flag is set to the state of the OUT bit before modification.

Note that the new DIRx state is not data-forwarded; the next pipelined instruction sees the old state.



## DRVNOT {#drvnot}

Drive not
[I/O Pin Instruction](\#io-pin-instructions) - Set pin(s) direction to output and toggle to the opposite output level.

**DRVNOT**  *{\#}Dest*  **\{WCZ\}**

---

**Result:** The I/O pins described by Dest are set to the output direction and to their opposite output level(s); the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to the output direction and toggle to opposite output levels.
- WCZ is an optional effect to update flags.

```{=latex}
\simpleencoding{EEEE}{1101011}{CZL}{DDDDDDDDD}{001011111}{DIRx* + OUTx}{---}{OUT bit}{2}
```

**Related:** [DRVRND](\#drvrnd), [DRVH](\#drvh), [DRVL](\#drvl), [DRVC](\#drvc), [DRVNC](\#drvnc), [DRVZ](\#drvz), [DRVNZ](\#drvnz)

**Explanation:**

DRVNOT sets the I/O pin(s) designated by Dest to the output direction and toggles their output level(s) to the opposite state. All other pins are left unchanged. This instruction achieves the same effect as two instructions—OUTNOT followed by DIRH.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (\#\#Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

When Dest is a register, the register's value bits [10:0] are used as-is to form the 11-bit ID range, unless a SETQ instruction immediately precedes the DRVNOT instruction; substituting SETQ's Dest[4:0] in place of value bits[10:6], for DRVNOT's use.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group (DIRA or DIRB and OUTA or OUTB); it will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are updated to the original state of OUTA / OUTB's base bit, identified by Dest.

Note that the new DIRx state is not data-forwarded; the next pipelined instruction sees the old state.



## DRVZ / DRVNZ {#drvz}

Drive pins if Z / not Z
[I/O Pin Instruction](\#io-pin-instructions) - Set pin(s) direction to output and output level to low/high according to Z or !Z.

**DRVZ**  *{\#}Dest*  **\{WCZ\}**
**DRVNZ**  *{\#}Dest*  **\{WCZ\}**

---

**Result:** The I/O pins described by Dest are set to the output direction and to an output level of low/high according to Z or !Z; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to output direction and output levels of low or high.
- WCZ is an optional effect to update flags.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1101011}{CZL}{DDDDDDDDD}{001011100}{DIRx* + OUTx}{---}{OUT bit}{2}
\encodingrow{EEEE}{1101011}{CZL}{DDDDDDDDD}{001011101}{DIRx* + OUTx}{---}{OUT bit}{2}
\end{encodingtable}
```

**Related:** [DRVC](\#drvc), [DRVNC](\#drvnc), [DRVH](\#drvh), [DRVL](\#drvl), [DRVNOT](\#drvnot), [DRVRND](\#drvrnd)

**Explanation:**

DRVZ or DRVNZ sets the I/O pin(s) designated by Dest to the output direction and to a low/high output level according to the Z flag or its inverse (!Z). All other pins are left unchanged.

DRVZ sets the pin(s) to the output direction and to the level indicated by the Z flag: high (1) for high output, low (0) for low output. DRVNZ inverts this relationship, setting the output level according to the inverse of the Z flag (!Z).

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (\#\#Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group; it will not cross the port boundary.

If the WCZ effect is specified, the Z flag is set to the state of the OUT bit before modification.



## DRVRND {#drvrnd}

Drive random
[I/O Pin Instruction](\#io-pin-instructions) - Set pin(s) direction to output and output level to random low/high.

**DRVRND**  *{\#}Dest*  **\{WCZ\}**

---

**Result:** The I/O pins described by Dest are set to the output direction and each output level is set randomly low or high; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to the output direction and with output level(s) set randomly to low or high.
- WCZ is an optional effect to update flags.

```{=latex}
\simpleencoding{EEEE}{1101011}{CZL}{DDDDDDDDD}{001011110}{DIRx + OUTx}{Original OUTx base bit}{Original OUTx base bit}{2}
```

**Related:** [DRVH](\#drvh), [DRVL](\#drvl), [DRVC](\#drvc), [DRVNC](\#drvnc), [DRVZ](\#drvz), [DRVNZ](\#drvnz), [DRVNOT](\#drvnot)

**Explanation:**

DRVRND sets the I/O pin(s) designated by Dest to the output direction and with output level(s) set randomly low and high, based on bit(s) from the Xoroshiro128** PRNG. All other pins are left unchanged. This instruction can affect one or more of the bits within the DIRA or DIRB and OUTA or OUTB registers.

DRVRND achieves the same effect as two instructions—OUTRND followed by DIRH.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (\#\#Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

When Dest is a register, the register's value bits [10:0] are used as-is to form the 11-bit ID range, unless a SETQ instruction immediately precedes the DRVRND instruction; substituting SETQ's Dest[4:0] in place of value bits[10:6], for DRVRND's use.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group (DIRA or DIRB and OUTA or OUTB); it will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are updated to the original state of OUTA / OUTB's base bit, identified by Dest, before the random modification occurs.

Note that the new DIRx state is not data-forwarded; the next pipelined instruction sees the old state.


