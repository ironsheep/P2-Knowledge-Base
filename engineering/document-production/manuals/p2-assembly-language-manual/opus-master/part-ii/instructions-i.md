# Instructions: I

This section contains all PASM2 instructions beginning with the letter I.

**Conditional Jump Timing Convention:** Conditional jumps in this section (IJZ, IJNZ) show their `Clks` field as `not-taken / taken`. The *taken* value depends on execution context:

| Context | Clocks when taken |
|:--------|:----------------:|
| Cog / LUT execution | 4 |
| Hub execution | 13...20 |

So `2 or 4 / 2 or 13-20` reads as: 2 cycles when the jump is not taken, 4 cycles when taken in cog/LUT, 13–20 cycles when taken in hub execution.



::: instrheader
## IJZ / IJNZ {#ijz}
Increment and Jump If Zero

[Branching and Flow Control](#branching-and-flow-control) - Increments and conditionally jumps based on the result.
:::

\hypertarget{ijnz}{}

**IJZ**  *Dest, {#}Src*\
**IJNZ**  *Dest, {#}Src*

**Result:** Dest is incremented by 1, and conditionally jumps based on the result.

- Dest is a register whose value is incremented and tested.
- Src is the jump address: use # for relative, omit for absolute.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011100 | 00I | DDDDDDDDD | SSSSSSSSS | --- | --- | D + PC* | 2 or 4 / 2 or 13-20 |
| EEEE | 1011100 | 01I | DDDDDDDDD | SSSSSSSSS | --- | --- | D + PC* | 2 or 4 / 2 or 13-20 |

```{=latex}
*PC is written only when the jump condition is met.
```


**Related:** [DJZ](#djz), [DJNZ](#djnz), [TJZ](#tjz), [TJNZ](#tjnz)

**Explanation:**

IJZ and IJNZ increment Dest and conditionally jump based on whether the result is zero or non-zero:

| Instruction | Jumps when |
|-------------|------------|
| IJZ | result == 0 |
| IJNZ | Result != 0 |

IJZ is useful for counting until overflow to zero (from $FFFF_FFFF to 0). IJNZ is useful for counting up from a negative value until reaching zero.

Takes 2 clocks when not jumping, 4 clocks when jumping (pipeline flush).



::: instrheader
## INCMOD {#incmod}
Increment Modulus

[Arithmetic Operations](#arithmetic-operations) - Increments with modulus wrap-around.
:::

**INCMOD**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

**Operation:** if D == S then `D = 0`, `C = 1`, else `D = D + 1`, `C = 0`

**Result:** If Dest was not equal to Src, it is incremented by 1; otherwise Dest is reset to 0.

- Dest is a register containing the value to increment up to Src with modulus, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is the modulus limit to apply to Dest's increment operation.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0111000 | CZI | DDDDDDDDD | SSSSSSSSS | D was S (wrapped) | result == 0 | D | 2 |


**Related:** [DECMOD](#decmod), [ADDCT1/2/3](#addct1)

**Explanation:**

INCMOD compares Dest with Src. If they are not equal, INCMOD increments Dest by 1. If they are equal, INCMOD sets Dest to 0. This provides automatic wrap-around behavior for circular counting sequences.

If Dest begins in the range 0 to Src, repeated iterations of INCMOD will increment Dest cyclically from 0 to Src, then wrap back to 0, over and over. INCMOD increments Dest, wrapping to 0 after it reaches Src, which suits round-robin scheduling, circular buffer indexing, and other modulo-arithmetic operations. DECMOD provides the decrement-with-modulus equivalent for wrap-around counting downward.

If the WC or WCZ effect is specified, the C flag is set (1) if Dest was equal to Src and subsequently reset to 0 (the modulus was triggered), or is cleared (0) if Dest was incremented. This allows detecting when the cycle completes.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if it is non-zero.

INCMOD does not limit Dest within the specified range. If Dest begins at a value greater than Src, iterations of INCMOD will continue to increment it through the 32-bit rollover point ($FFFF_FFFF wrapping to $0000_0000) before it will effectively cycle from 0 to Src.

A common usage pattern for INCMOD is managing circular buffers:

```pasm2
                ' Increment tail index with modulo for circular buffer
                incmod  tail_idx, #BUF_SIZE-1  wc
        if_c    jmp     #buffer_wrapped

                ' Safe to add data at tail
                add     buffer_ptr, tail_idx
                wrbyte  new_data, buffer_ptr
```

INCMOD also indexes round-robin scheduling across a fixed number of resources:

```pasm2
                ' Round-robin through 8 ports (0-7)
.loop
                ' Service current port
                ' ... port service code ...

                ' Move to next port
                incmod  portctr, #7            wc
        if_nc   jmp     #.loop

                ' All ports serviced, continue
```



