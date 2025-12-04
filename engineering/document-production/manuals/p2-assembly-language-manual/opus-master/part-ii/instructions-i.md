# Instructions: I

This section contains all PASM2 instructions beginning with the letter I.



::: instrheader
## IJZ / IJNZ {#ijz}
Increment and Jump If Zero {#ijnz}
Category: [Branch](instruction-categories.md#branch)
:::

**IJZ**  *Dest, {#}Src*
**IJNZ**  *Dest, {#}Src*

---

**Result:** Dest is incremented by 1, and conditionally jumps based on the result.

- Dest is a register whose value is incremented and tested.
- Src is the jump address: use # for relative, omit for absolute.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011100 | 00I | DDDDDDDDD | SSSSSSSSS | D + PC* | --- | --- | 2 or 4 |
| EEEE | 1011100 | 01I | DDDDDDDDD | SSSSSSSSS | D + PC* | --- | --- | 2 or 4 |

```{=latex}
*PC is written only when the jump condition is met.
```


**Related:** [DJZ](instructions-d.md#djz), [DJNZ](instructions-d.md#djnz), [TJZ](instructions-t.md#tjz), [TJNZ](instructions-t.md#tjnz)

**Explanation:**

IJZ and IJNZ increment Dest and conditionally jump based on whether the result is zero or non-zero:

| Instruction | Jumps when |
|-------------|------------|
| IJZ | Result = 0 |
| IJNZ | Result ≠ 0 |

IJZ is useful for counting until overflow to zero (from $FFFF_FFFF to 0). IJNZ is useful for counting up from a negative value until reaching zero.

Takes 2 clocks when not jumping, 4 clocks when jumping (pipeline flush).



::: instrheader
## INCMOD {#incmod}
Increment Modulus
Category: [Math and Logic](instruction-categories.md#math-and-logic)
:::

**INCMOD**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** If Dest was not equal to Src, it is incremented by 1; otherwise Dest is reset to 0.

- Dest is a register containing the value to increment up to Src with modulus, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is the modulus limit to apply to Dest's increment operation.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0111000 | CZI | DDDDDDDDD | SSSSSSSSS | D | D = S, set D = 0 and C = 1, else D = D + 1 and C = 0 | Result = 0 | 2 |


**Related:** [DECMOD](instructions-d.md#decmod), [ADDCT1/2/3](instructions-a.md#addct1)

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


