# Instructions: I

This section contains all PASM2 instructions beginning with the letter I.

---

## IJZ {#ijz}

Increment and jump if zero
[Branch/Jump Instruction](#branch-jump-instructions) - Increment a register value and jump if the result equals zero.

```
IJZ     Dest, {#}Src
```

**Result:** Dest is incremented by 1, and if the result equals zero, PC is set to a new address.

- Dest is a register whose value is incremented and tested for zero or not zero.
- Src is a register, 9-bit literal, or 20-bit augmented literal whose value is the absolute or relative address to set PC to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011100}{00I}{DDDDDDDDD}{SSSSSSSSS}{D and PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the result in Dest equals zero.
```

**Related:** [IJNZ](#ijnz), [DJZ](#djz), [DJNZ](#djnz)

**Explanation:**

IJZ increments the value in Dest, writes the result back to Dest, and jumps to the address described by Src if the result equals zero.

This instruction is useful for counting until overflow to zero. The typical pattern is to start with a value and increment it repeatedly until it wraps around to zero (after reaching $FFFF\_FFFF).

When the # prefix is used on Src, the addressing is relative—the value in Src is treated as a signed offset from the current PC address. This is the most common usage for loops. When # is omitted, the addressing is absolute—Src contains the actual COG address to jump to.

If the result after incrementing Dest is zero, the jump is taken and execution continues at the new address. If the result is not zero, execution continues with the next sequential instruction.

IJZ always takes 2 clock cycles when the jump is not taken, and 4 clock cycles when the jump is taken (due to the pipeline flush).

---

## IJNZ {#ijnz}

Increment and jump if not zero
[Branch/Jump Instruction](#branch-jump-instructions) - Increment a register value and jump if the result is not zero.

```
IJNZ    Dest, {#}Src
```

**Result:** Dest is incremented by 1, and if the result is not zero, PC is set to a new address.

- Dest is a register whose value is incremented and tested for zero or not zero.
- Src is a register, 9-bit literal, or 20-bit augmented literal whose value is the absolute or relative address to set PC to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011100}{01I}{DDDDDDDDD}{SSSSSSSSS}{D and PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the result in Dest is not zero.
```

**Related:** [IJZ](#ijz), [DJNZ](#djnz), [DJZ](#djz)

**Explanation:**

IJNZ increments the value in Dest, writes the result back to Dest, and jumps to the address described by Src if the result is not zero.

This instruction is useful for counting up to a specific value. The typical pattern is to start with zero (or a negative value) and increment until reaching a target count. Since most non-zero values result in a jump, the loop continues until Dest increments to exactly zero, at which point execution falls through to the next instruction.

When the # prefix is used on Src, the addressing is relative—the value in Src is treated as a signed offset from the current PC address. This is the most common usage for loops. When # is omitted, the addressing is absolute—Src contains the actual COG address to jump to.

If the result after incrementing Dest is not zero, the jump is taken and execution continues at the new address. If the result equals zero, execution continues with the next sequential instruction.

IJNZ always takes 2 clock cycles when the jump is not taken, and 4 clock cycles when the jump is taken (due to the pipeline flush).

---

## INCMOD {#incmod}

Increment with modulus
[Math Instruction](#math-instructions) - Increment a value with automatic wrap-around at a specified modulus.

```
INCMOD  Dest, {#}Src  {WC|WZ|WCZ}
```

**Result:** If Dest was not equal to Src, it is incremented by 1; otherwise Dest is reset to 0.

- Dest is a register containing the value to increment up to Src with modulus, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is the modulus limit to apply to Dest's increment operation.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0111000}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{D = S, set D = 0 and C = 1, else D = D + 1 and C = 0}{Result = 0}{2}
```

**Related:** [DECMOD](#decmod), [ADDCT1](#addct1), [ADDCT2](#addct2), [ADDCT3](#addct3)

**Explanation:**

INCMOD compares Dest with Src. If they are not equal, INCMOD increments Dest by 1. If they are equal, INCMOD sets Dest to 0. This provides automatic wrap-around behavior for circular counting sequences.

If Dest begins in the range 0 to Src, repeated iterations of INCMOD will increment Dest cyclically from 0 to Src, then wrap back to 0, over and over. This makes INCMOD ideal for round-robin scheduling, circular buffer indexing, and other modulo-arithmetic operations.

If the WC or WCZ effect is specified, the C flag is set (1) if Dest was equal to Src and subsequently reset to 0 (the modulus was triggered), or is cleared (0) if Dest was simply incremented. This allows detecting when the cycle completes.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if it is non-zero.

INCMOD does not limit Dest within the specified range. If Dest begins at a value greater than Src, iterations of INCMOD will continue to increment it through the 32-bit rollover point ($FFFF\_FFFF wrapping to $0000\_0000) before it will effectively cycle from 0 to Src.

A common usage pattern for INCMOD is managing circular buffers:

```pasm
        ' Increment tail index with modulo for circular buffer
        incmod  tail_idx, #BUF_SIZE-1  wc
if_c    jmp     #buffer_wrapped

        ' Safe to add data at tail
        add     buffer_ptr, tail_idx
        wrbyte  new_data, buffer_ptr
```

INCMOD is also ideal for round-robin scheduling across a fixed number of resources:

```pasm
        ' Round-robin through 8 ports (0-7)
.loop
        ' Service current port
        ' ... port service code ...

        ' Move to next port
        incmod  portctr, #7            wc
if_nc   jmp     #.loop

        ' All ports serviced, continue
```

---
