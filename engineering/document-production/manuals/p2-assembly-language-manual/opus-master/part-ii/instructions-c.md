# Instructions: C

This section contains all PASM2 instructions beginning with the letter C.



::: instrheader
## CALL {#call}
Call Subroutine

[Branching and Flow Control](#branching-and-flow-control) - Calls a subroutine and pushes return info to stack.
:::

**CALL**  *#Addr*\
**CALL**  *#\Addr*\
**CALL**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** Current C and Z flags and address of the next instruction are pushed onto the hardware stack, PC is set to the new address, and optionally C and Z are updated to new states.

- Addr is a symbolic reference to the target subroutine; the location to set PC to. Relative addressing is the default; use '\' to force absolute addressing.
- Dest is a register containing the 20-bit absolute address to set PC to and optional new C and Z states.
- WC, WZ, or WCZ are optional effects to update the flags from Dest's upper bit states.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101101 | RAA | AAAAAAAAA | AAAAAAAAA | --- | --- | --- | 4 / 13-20 |
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000101101 | D[31] | D[30] | --- | 4 / 13-20 |


**Related:** [RET](#ret), [CALLA](#calla), [CALLB](#callb), [CALLD](#calld), [CALLPA](#callpa), [CALLPB](#callpb)

**Explanation:**

CALL records the current state of the C and Z flags and the address of the next instruction (PC + 1 if cog/LUT execution; PC + 4 if hub execution) by pushing to the stack (K), potentially updates the C and Z flags with new given states, and jumps to the given address or offset. The routine at the new address should eventually execute a RET instruction, or an instruction with a _RET_ condition, to return to the recorded address (the instruction following the CALL) and optionally restore the C and Z flag state as it was prior.

In the first syntax form, `#Addr` and `#\Addr` encodes the instruction with relative and absolute addressing, respectively. The relative form (the default) is vital for creating relocatable code. In either case, use symbolic references for Addr and the assembler will encode it properly. Examples: `CALL #SendBit` or `CALL #\DebugStatus`.

In the second syntax form, the format of the value at Dest is `CZxxxxxx_xxxxAAAA_AAAAAAAA_AAAAAAAA`. C is the new C flag state, Z is the new Z flag state, A is the new 20-bit address to jump to, and x are don't-care bits. This syntax effectively swaps the flags and PC with the value in the Dest register (and RET swaps them back), making it convenient for switching between two threads.

If the WC or WCZ effect is specified, the C flag is updated to match D[31], after its original state is recorded.

If the WZ or WCZ effect is specified, the Z flag is updated to match D[30], after its original state is recorded.

The instruction takes 4 cycles for cog/LUT execution, or 13-20 cycles for hub execution.



::: instrheader
## CALLA {#calla}
Call Subroutine via PTRA

[Branching and Flow Control](#branching-and-flow-control) - Calls subroutine using PTRA as stack pointer.
:::

**CALLA**  *#Addr*\
**CALLA**  *#\Addr*\
**CALLA**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** Current C and Z flags and address of the next instruction are written to hub RAM at PTRA, PTRA is incremented by 4, PC is set to the new address, and optionally C and Z are updated to new states.

- Addr is a symbolic reference to the target subroutine; the location to set PC to. Relative addressing is the default; use '\' to force absolute addressing.
- Dest is a register containing the 20-bit absolute address to set PC to and optional new C and Z states.
- WC, WZ, or WCZ are optional effects to update the flags from Dest's upper bit states.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101110 | RAA | AAAAAAAAA | AAAAAAAAA | --- | --- | --- | 5-12 / 14-32 |
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000101110 | D[31] | D[30] | --- | 5-12 / 14-32 |


**Related:** [CALL](#call), [CALLB](#callb), [CALLD](#calld), [RETA](#reta)

**Explanation:**

CALLA writes the current C and Z flags and the address of the next instruction into the 4-byte hub RAM location at PTRA, then increments PTRA by 4, sets PC to the new relative or absolute address, and optionally updates C and Z to new states.

In the first syntax form, `#Addr` and `#\Addr` encodes the instruction with relative and absolute addressing, respectively. The relative form (the default) is vital for creating relocatable code. In either case, use symbolic references for Addr and the assembler will encode it properly.

In the second syntax form, the format of the value at Dest is `CZxxxxxx_xxxxAAAA_AAAAAAAA_AAAAAAAA`. C is the new C flag state, Z is the new Z flag state, A is the new 20-bit address to jump to, and x are don't-care bits.

If the WC or WCZ effect is specified, the C flag is set to D[31] after the original state is recorded.

If the WZ or WCZ effect is specified, the Z flag is set to D[30] after the original state is recorded.

CALLA is used for subroutine calls when hub RAM is being used as the call stack instead of the hardware stack. This is useful for deep nesting or when preserving the hardware stack for other purposes. The instruction takes 5-12 cycles for cog/LUT execution, or 14-32 cycles for hub execution.



::: instrheader
## CALLB {#callb}
Call Subroutine via PTRB

[Branching and Flow Control](#branching-and-flow-control) - Calls subroutine using PTRB as stack pointer.
:::

**CALLB**  *#Addr*\
**CALLB**  *#\Addr*\
**CALLB**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** Current C and Z flags and address of the next instruction are written to hub RAM at PTRB, PTRB is incremented by 4, PC is set to the new address, and optionally C and Z are updated to new states.

- Addr is a symbolic reference to the target subroutine; the location to set PC to. Relative addressing is the default; use '\' to force absolute addressing.
- Dest is a register containing the 20-bit absolute address to set PC to and optional new C and Z states.
- WC, WZ, or WCZ are optional effects to update the flags from Dest's upper bit states.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101111 | RAA | AAAAAAAAA | AAAAAAAAA | --- | --- | --- | 5-12 / 14-32 |
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000101111 | D[31] | D[30] | --- | 5-12 / 14-32 |


**Related:** [CALL](#call), [CALLA](#calla), [CALLD](#calld), [RETB](#retb)

**Explanation:**

CALLB writes the current C and Z flags and the address of the next instruction into the 4-byte hub RAM location at PTRB, then increments PTRB by 4, sets PC to the new relative or absolute address, and optionally updates C and Z to new states.

In the first syntax form, `#Addr` and `#\Addr` encodes the instruction with relative and absolute addressing, respectively. The relative form (the default) is vital for creating relocatable code. In either case, use symbolic references for Addr and the assembler will encode it properly.

In the second syntax form, the format of the value at Dest is `CZxxxxxx_xxxxAAAA_AAAAAAAA_AAAAAAAA`. C is the new C flag state, Z is the new Z flag state, A is the new 20-bit address to jump to, and x are don't-care bits.

If the WC or WCZ effect is specified, the C flag is set to D[31] after the original state is recorded.

If the WZ or WCZ effect is specified, the Z flag is set to D[30] after the original state is recorded.

CALLB operates identically to CALLA except it uses PTRB as the stack pointer instead of PTRA. This allows for maintaining separate call stacks or using both pointers for different purposes. The instruction takes 5-12 cycles for cog/LUT execution, or 14-32 cycles for hub execution.



::: instrheader
## CALLD {#calld}
Call with Destination register

[Branching and Flow Control](#branching-and-flow-control) - Calls subroutine saving return info to a register.
:::

**CALLD**  *PA|PB|PTRA|PTRB, #Addr*\
**CALLD**  *PA|PB|PTRA|PTRB, #\Addr*\
**CALLD**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Current C and Z flags and address of the next instruction are written to the specified register (PA, PB, PTRA, PTRB, or Dest), PC is set to the new address, and optionally C and Z are updated to new states.

- PA|PB|PTRA|PTRB is the special register to store the current C and Z flags and next address into.
- Addr is a symbolic reference to the target subroutine; the location to set PC to. Relative addressing is the default; use '\' to force absolute addressing.
- Dest is a register to write the current C and Z flags and the address of the next instruction into.
- Src is a register, 9-bit literal, or 32-bit augmented literal that contains the relative or absolute address to set PC to and optional new C and Z states. Use # for relative addressing; omit # for absolute addressing.
- WC, WZ, or WCZ are optional effects to update the flags from Src's upper bit states.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 11100WW | RAA | AAAAAAAAA | AAAAAAAAA | --- | --- | --- | 4 / 13-20 |
| EEEE | 1011001 | CZI | DDDDDDDDD | SSSSSSSSS | S[31] | S[30] | --- | 4 / 13-20 |


**Related:** [CALL](#call), [CALLPA](#callpa), [CALLPB](#callpb), [RET](#ret), [PA](#pa), [PB](#pb), [PTRA](#ptra), [PTRB](#ptrb)

**Explanation:**

CALLD records the current state of the C and Z flags and the address of the next instruction (PC + 1 if cog/LUT execution; PC + 4 if hub execution) by writing them to the PA, PB, PTRA, PTRB, or Dest register, potentially updates the C and Z flags with new given states, and jumps to the given address or offset. The routine at the new address should eventually execute another CALLD instruction to return to the recorded address (the instruction following the original CALLD), optionally restore the C and Z flag state as it was prior, and optionally prep for another CALLD.

This instruction is typically used for the P2 DEBUG function.

In the first syntax form, `#Addr` and `#\Addr` encodes the instruction with relative and absolute addressing, respectively. The relative form (the default) is vital for creating relocatable code. In either case, use symbolic references for Addr and the assembler will encode it properly. Examples: `CALLD PA, #SendBit` or `CALLD PB, #\DebugStatus`.

In the second syntax form, the format of the value at Src is `CZxxxxxx_xxxxAAAA_AAAAAAAA_AAAAAAAA`. C is the new C flag state, Z is the new Z flag state, A is the new 20-bit address to jump to, and x are don't-care bits. If Src is a 9-bit literal (immediate), it will be sign-extended to 20 bits and used as a relative offset, giving a range of -256 to +255 instructions relative to the instruction following the CALLD. When relative, PC is adjusted by signed(Src) if cog/LUT execution, or by signed(Src * 4) if hub execution.

If the WC or WCZ effect is specified, the C flag is updated to match S[31], after its original state is recorded.

If the WZ or WCZ effect is specified, the Z flag is updated to match S[30], after its original state is recorded.

The instruction takes 4 cycles for cog/LUT execution, or 13-20 cycles for hub execution.



::: instrheader
## CALLPA {#callpa}
Call Subroutine with PA Parameter

[Branching and Flow Control](#branching-and-flow-control) - Calls subroutine and loads parameter into PA.
:::

**CALLPA**  *{#}Dest, {#}Src*

---

**Result:** Current C and Z flags and address of the next instruction are pushed onto the hardware stack, Dest is copied to PA, and PC is set to the address specified by Src.

- Dest is a register, 9-bit literal, or 32-bit augmented literal whose value is copied to PA.
- Src is a register, 9-bit literal, or 32-bit augmented literal that contains the relative or absolute address to set PC to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011010 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | K, PA and PC | 4 / 13-20 |


**Related:** [CALL](#call), [CALLPB](#callpb), [CALLD](#calld), [RET](#ret), [PA](#pa)

**Explanation:**

CALLPA records the current state of the C and Z flags and the address of the next instruction (PC + 1 if cog/LUT execution; PC + 4 if hub execution) by pushing to the stack (K), copies the value of Dest to PA, and jumps to the address specified by Src. The routine at the new address should eventually execute a RET instruction to return to the recorded address and restore the flags.

This instruction is useful for passing a parameter to a subroutine via the PA register while simultaneously calling that subroutine. The parameter can be an immediate value, making it convenient for subroutines that need a single argument.

The Src operand determines the target address. If Src is preceded by #, it is treated as a relative address; otherwise it is an absolute address. If Src is a register, its lower 20 bits specify the absolute address to jump to.

The instruction takes 4 cycles for cog/LUT execution, or 13-20 cycles for hub execution.



::: instrheader
## CALLPB {#callpb}
Call Subroutine with PB Parameter

[Branching and Flow Control](#branching-and-flow-control) - Calls subroutine and loads parameter into PB.
:::

**CALLPB**  *{#}Dest, {#}Src*

---

**Result:** Current C and Z flags and address of the next instruction are pushed onto the hardware stack, Dest is copied to PB, and PC is set to the address specified by Src.

- Dest is a register, 9-bit literal, or 32-bit augmented literal whose value is copied to PB.
- Src is a register, 9-bit literal, or 32-bit augmented literal that contains the relative or absolute address to set PC to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011010 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | K, PB and PC | 4 / 13-20 |


**Related:** [CALL](#call), [CALLPA](#callpa), [CALLD](#calld), [RET](#ret), [PB](#pb)

**Explanation:**

CALLPB records the current state of the C and Z flags and the address of the next instruction (PC + 1 if cog/LUT execution; PC + 4 if hub execution) by pushing to the stack (K), copies the value of Dest to PB, and jumps to the address specified by Src. The routine at the new address should eventually execute a RET instruction to return to the recorded address and restore the flags.

This instruction operates identically to CALLPA except it uses the PB register instead of PA. This is useful for passing a parameter to a subroutine via the PB register, or when both PA and PB need to be set by using CALLPA followed by CALLPB, or when the subroutine convention uses PB for parameters.

The Src operand determines the target address. If Src is preceded by #, it is treated as a relative address; otherwise it is an absolute address. If Src is a register, its lower 20 bits specify the absolute address to jump to.

The instruction takes 4 cycles for cog/LUT execution, or 13-20 cycles for hub execution.



::: instrheader
## CMP {#cmp}
Compare Unsigned

[Arithmetic Operations](#arithmetic-operations) - Compares two unsigned values and sets flags.
:::

**CMP**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Greater/lesser and equality status is optionally written to the C and Z flags.

- Dest is the register containing the value to compare with that of Src.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is compared to Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0010000 | CZI | DDDDDDDDD | SSSSSSSSS | Unsigned (D < S) | (D == S) | --- | 2 |


**Related:** [CMPR](#cmpr), [CMPX](#cmpx), [CMPS](#cmps), [CMPSX](#cmpsx), [CMPM](#cmpm)

**Explanation:**

CMP compares the unsigned values of Dest and Src by subtracting Src from Dest and optionally setting the C and Z flags accordingly. The result of the subtraction is discarded; only the flags are affected. Dest is not modified.

If the WC or WCZ effect is specified, the C flag is set (1) if Dest is less than Src (unsigned comparison), or is cleared (0) if Dest is greater than or equal to Src. This indicates that the subtraction would require a borrow.

If the WZ or WCZ effect is specified, the Z flag is set (1) if Dest equals Src, or is cleared (0) if they are not equal.

To compare unsigned multi-long values (64-bit or larger), use CMP for the least significant long, then CMPX for each subsequent long. For example, to compare two 64-bit values:

```pasm2
        cmp     value_lo, other_lo  wc    ' Compare low longs
        cmpx    value_hi, other_hi  wcz   ' Compare high longs with borrow
        ' C and Z now reflect the 64-bit comparison result
```

CMP is fundamental for implementing conditional logic and control flow based on numeric comparisons.



::: instrheader
## CMPM {#cmpm}
Compare Most Significant Bit

[Arithmetic Operations](#arithmetic-operations) - Compares values with C set to MSB of difference.
:::

**CMPM**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Greater/lesser and equality status is optionally written to the C and Z flags.

- Dest is the register containing the value to compare with that of Src.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is compared to Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0010101 | CZI | DDDDDDDDD | SSSSSSSSS | MSB of (D-S) | (D == S) | --- | 2 |


**Related:** [CMP](#cmp), [CMPS](#cmps)

**Explanation:**

CMPM compares the unsigned values of Dest and Src by subtracting Src from Dest and optionally setting the C and Z flags accordingly. The result of the subtraction is discarded; only the flags are affected. Dest is not modified.

If the WC or WCZ effect is specified, the C flag is updated to the MSB (bit 31) of the result of Dest - Src. This is different from CMP, which sets C based on whether a borrow occurred. CMPM's C flag directly reflects the sign bit of the difference.

If the WZ or WCZ effect is specified, the Z flag is set (1) if Dest equals Src, or is cleared (0) if they are not equal.

CMPM is useful when the most significant bit of the difference carries semantic meaning for the algorithm being implemented, such as certain mathematical operations or specialized comparison logic.



::: instrheader
## CMPR {#cmpr}
Compare Reverse

[Arithmetic Operations](#arithmetic-operations) - Compares values with reversed operand order.
:::

**CMPR**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Greater/lesser and equality status is optionally written to the C and Z flags.

- Dest is the register containing the value to compare with that of Src.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is compared to Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0010100 | CZI | DDDDDDDDD | SSSSSSSSS | borrow of (S - D) | D == S | --- | 2 |


**Related:** [CMP](#cmp)

**Explanation:**

CMPR compares the unsigned values of Dest and Src by subtracting Dest from Src (the reverse of CMP) and optionally setting the C and Z flags accordingly. The result of the subtraction is discarded; only the flags are affected. Dest is not modified.

If the WC or WCZ effect is specified, the C flag is set (1) if Src is less than Dest (unsigned comparison), or is cleared (0) if Src is greater than or equal to Dest. This is the opposite condition from CMP.

If the WZ or WCZ effect is specified, the Z flag is set (1) if Dest equals Src, or is cleared (0) if they are not equal.

CMPR is useful when the natural order of operands in your code is reversed from what CMP expects, avoiding the need to swap operands or reverse the logic. Note that for unsigned multi-long comparisons, use CMP (not CMPR) followed by CMPX.



::: instrheader
## CMPS {#cmps}
Compare Signed

[Arithmetic Operations](#arithmetic-operations) - Compares two signed values and sets flags.
:::

**CMPS**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Greater/lesser and equality status is optionally written to the C and Z flags.

- Dest is the register containing the value to compare with that of Src.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is compared to Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0010010 | CZI | DDDDDDDDD | SSSSSSSSS | correct sign of (D - S) | (D == S) | --- | 2 |


**Related:** [CMP](#cmp), [CMPX](#cmpx), [CMPSX](#cmpsx)

**Explanation:**

CMPS compares the signed values of Dest and Src by subtracting Src from Dest and optionally setting the C and Z flags to indicate the comparison and operation results. The result of the subtraction is discarded; only the flags are affected. Dest is not modified.

If the WC or WCZ effect is specified, the C flag is set (1) if signed Dest is less than signed Src, or is cleared (0) if signed Dest is greater than or equal to signed Src. The comparison properly accounts for the sign bit.

If the WZ or WCZ effect is specified, the Z flag is set (1) if Dest equals Src, or is cleared (0) if they are not equal.

To compare signed multi-long values (64-bit or larger), use CMP (not CMPS) for the least significant long, optionally followed by CMPX for middle longs, and finally CMPSX for the most significant long. The final CMPSX accounts for sign extension properly. For example, to compare two 64-bit signed values:

```pasm2
        cmp     value_lo, other_lo  wc    ' Compare low longs unsigned
        cmpsx   value_hi, other_hi  wcz   ' Compare high signed w/borrow
        ' C and Z now reflect the signed 64-bit comparison result
```



::: instrheader
## CMPSUB {#cmpsub}
Compare and Subtract

[Arithmetic Operations](#arithmetic-operations) - Conditionally subtracts if Dest is greater or equal.
:::

**CMPSUB**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Dest is decremented by Src unless it is less than Src, and the comparison results are optionally written to the C and Z flags.

- Dest is the register containing the value to compare with Src and is the destination written to if a subtraction is performed.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is compared with and possibly subtracted from Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0010111 | CZI | DDDDDDDDD | SSSSSSSSS | D >= S | result == 0 | D † | 2 |

† Dest is only written if D >= S (subtraction was performed).

**Related:** [CMP](#cmp), [SUB](#sub)

**Explanation:**

CMPSUB compares the unsigned values of Dest and Src, and if Src is less than or equal to Dest, then Src is subtracted from Dest. Optionally, the C and Z flags are set to indicate the comparison and operation results.

The operation performs the comparison first. If Dest >= Src (unsigned), then Dest is updated to Dest - Src. If Dest < Src, then Dest is left unchanged.

If the WC or WCZ effect is specified, the C flag is set (1) if Dest was greater than or equal to Src (subtraction was performed), or is cleared (0) if Dest was less than Src (no subtraction).

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals 0, or is cleared (0) if non-zero. Note that if no subtraction was performed (Dest < Src), Z reflects whether Dest was already zero.

CMPSUB is particularly useful for implementing division algorithms, modulo operations, and other mathematical routines where conditional subtraction based on magnitude is needed.



::: instrheader
## CMPSX {#cmpsx}
Compare Signed Extended

[Arithmetic Operations](#arithmetic-operations) - Extended signed comparison for multi-long values.
:::

**CMPSX**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Greater/lesser and equality status is optionally written to the C and Z flags.

- Dest is the register containing the value to compare with that of Src.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is compared to Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0010011 | CZI | DDDDDDDDD | SSSSSSSSS | correct sign of (D - (S + C)) | Z AND (D == S + C) | --- | 2 |


**Related:** [CMP](#cmp), [CMPX](#cmpx), [CMPS](#cmps)

**Explanation:**

CMPSX compares the signed values of Dest and Src plus C by subtracting Src + C from Dest and optionally setting the C and Z flags accordingly. The CMPSX instruction is used to perform signed multi-long comparisons, such as 64-bit comparisons. The result of the subtraction is discarded; only the flags are affected. Dest is not modified.

If the WC or WCZ effect is specified, the C flag is set (1) if Dest is less than Src + C (as multi-long signed values), or is cleared (0) otherwise. Use WC or WCZ on preceding CMP and CMPX instructions for proper final C flag. The comparison properly accounts for sign extension.

If the WZ or WCZ effect is specified, the Z flag is set (1) if Z was previously set and the result of Dest - (Src + C) is zero, or it is cleared (0) if non-zero. This allows the Z flag to cascade through multi-long comparisons, remaining set only if all compared longs are equal.

For signed multi-long comparisons, use CMP for the least significant long, optionally CMPX for middle longs, and CMPSX for the most significant long:

```pasm2
        cmp     value_lo, other_lo  wc    ' Compare low longs
        cmpsx   value_hi, other_hi  wcz   ' Compare high signed w/borrow
        ' C=1 if signed value < other, Z=1 if equal
```



::: instrheader
## CMPX {#cmpx}
Compare Unsigned Extended

[Arithmetic Operations](#arithmetic-operations) - Extended unsigned comparison for multi-long values.
:::

**CMPX**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Greater/lesser and equality status is optionally written to the C and Z flags.

- Dest is a register containing the value to compare with that of Src plus C.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value plus C is compared to Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0010001 | CZI | DDDDDDDDD | SSSSSSSSS | borrow of (D - (S + C)) | Z AND (D == S + C) | --- | 2 |


**Related:** [CMP](#cmp), [CMPS](#cmps), [CMPSX](#cmpsx)

**Explanation:**

CMPX compares the unsigned values of Dest and Src plus C by subtracting Src + C from Dest and optionally setting the C and Z flags accordingly. The CMPX instruction is used to perform unsigned multi-long comparisons, such as 64-bit comparisons. The result of the subtraction is discarded; only the flags are affected. Dest is not modified.

If the WC or WCZ effect is specified, the C flag is set (1) if Dest is less than Src plus C (unsigned comparison), or is cleared (0) otherwise. Use WC or WCZ on preceding CMP and CMPX instructions for proper final C flag.

If the WZ or WCZ effect is specified, the Z flag is set (1) if Z was previously set and Dest equals Src + C, or it is cleared (0) otherwise. This allows the Z flag to cascade through multi-long comparisons, remaining set only if all compared longs are equal.

For unsigned multi-long comparisons, use CMP for the least significant long, then CMPX for each subsequent long:

```pasm2
        cmp     value_lo, other_lo  wc    ' Compare low longs
        cmpx    value_hi, other_hi  wcz   ' Compare high longs with borrow
        ' C=1 if unsigned value < other, Z=1 if equal
```



::: instrheader
## COGATN {#cogatn}
Cog Attention

[Events and Timing](#events-and-timing) - Signals attention to one or more cogs.
:::

**COGATN**  *{#}Dest*

---

**Result:** The attention signal of one or more cogs is strobed.

- Dest is the register or 9-bit literal whose value (lower 8-bit pattern) indicates which cogs to signal.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000111111 | --- | --- | --- | 2 |


**Related:** [POLLATN](#pollatn), [WAITATN](#waitatn), [JATN](#jatn), [JNATN](#jnatn)

**Explanation:**

COGATN strobes the attention signal for one or more cogs. Dest bit positions 7:0 represent cogs 7 through 0; high (1) bits indicate the cog(s) to signal. The receiving cog(s) then latch the signal, setting an internal flag, and can use any of the attention monitor instructions (JATN, JNATN, POLLATN, WAITATN) or interrupts to respond and clear the flag.

In the intended use case, the cog receiving an attention request knows which other cog is strobing it and how to respond. In cases where multiple cogs may request the attention of a single cog, some messaging structure may need to be implemented in hub RAM to differentiate requests.

For example, to signal cog 3:

```pasm2
        cogatn  #%0000_1000           ' Signal cog 3 (bit 3 = 1)
```

To signal multiple cogs simultaneously:

```pasm2
        cogatn  #%0001_0010           ' Signal cogs 1 and 4
```

COGATN is useful for implementing inter-cog communication, synchronization, and event notification without requiring polling of shared memory.



::: instrheader
## COGBRK {#cogbrk}
Cog Breakpoint

[Interrupts](#interrupts) - Triggers a breakpoint in a specified cog.
:::

**COGBRK**  *{#}Dest*

---

**Result:** If in the Debug ISR, trigger an asynchronous breakpoint in cog identified by Dest.

- Dest is the register or 9-bit literal whose value (lower 3-bits) indicates which cog to trigger.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000110101 | --- | --- | --- | 2 |


**Related:** [CALLD](#calld), [BRK](#brk)

**Explanation:**

COGBRK triggers an asynchronous breakpoint in a designated cog. The COGBRK instruction must be executed from within a Debug ISR (interrupt service routine) and the designated cog must already have its asynchronous breakpoint interrupt enabled. Dest[2:0] indicates the ID of the desired cog (0-7).

This instruction is part of the P2's debugging infrastructure and is typically used by debug monitors or development tools to halt a running cog for inspection. When executed, the target cog will interrupt its current execution and vector to its debug interrupt handler, allowing the debugging system to examine or modify the cog's state.

For example, to trigger a breakpoint in cog 2:

```pasm2
        cogbrk  #2                    ' Break cog 2 (must be in debug ISR)
```

COGBRK is a specialized instruction primarily used by development and debugging tools rather than in typical application code.



::: instrheader
## COGID {#cogid}
Cog Identification

[Cog Control and Locks](#cog-control-and-locks) - Gets current cog ID or checks if a cog is running.
:::

**COGID**  *{#}Dest*  **{WC}**

---

**Result:** Current cog's ID is written to Dest or C is set (1) or cleared (0) if the Dest cog is running or stopped.

- Dest is the register where the current cog's ID will be written, or is the register or 9-bit literal whose value (lower 3-bits) indicates which cog to get the status for.
- WC is an optional effect to update the C flag with the Dest cog's running status.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | C0L | DDDDDDDDD | 000000001 | Cog D[3:0] running | --- | D † | 2...9, +2 if result |

† Result written only if D is register and WC not specified.

**Related:** [COGINIT](#coginit), [COGSTOP](#cogstop)

**Explanation:**

COGID writes the current cog's ID into Dest (if Dest is a register and WC is omitted) or sets/clears the C flag according to the running/stopped state of the cog indicated by Dest[2:0] (if WC is given).

When used without the WC effect, COGID stores the current cog's ID (0-7) in the Dest register. This is useful when code needs to know which cog it is running on, for example when accessing cog-specific resources or implementing cog-aware algorithms.

When used with the WC effect, COGID checks the status of the cog specified by Dest[2:0]. If the WC effect is specified, the C flag is set (1) if the specified cog is running, or is cleared (0) if stopped. In this mode, Dest is not written.

For example, to get the current cog's ID:

```pasm2
        cogid   myid                  ' Store this cog's ID in myid
```

To check if cog 3 is running:

```pasm2
        cogid   #3              wc    ' C=1 if cog 3 is running
```



::: instrheader
## COGINIT {#coginit}
Cog Initialize

[Cog Control and Locks](#cog-control-and-locks) - Starts a cog to execute code from hub RAM.
:::

**COGINIT**  *{#}Dest, {#}Src*  **{WC}**

---

**Result:** Target cog is started according to Dest to execute code from Src. The code pointer (Src) is written to the target cog's PTRB, and optionally a data pointer is written to its PTRA if SETQ preceded COGINIT.

- Dest is the register or 9-bit literal describing the type of launch and possibly the ID of the desired cog to launch. If Dest is a register and WC is given, Dest is also where the ID of the launched cog will be written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value (lower 20 bits) is the target RAM address (for code) and the new cog's PTRB value.
- WC is an optional effect to update the C flag with the success (0) or fail (1) status and triggers Dest to be overwritten with new cog's ID.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100111 | CLI | DDDDDDDDD | SSSSSSSSS | No cog available | --- | D † | 2...9, +2 if result |

† Result written only if D is register and WC specified; contains launched cog ID.

**Related:** [COGID](#cogid), [COGSTOP](#cogstop)

**Explanation:**

COGINIT starts a new (unused) cog, a new pair of cogs (that may share LUT memory), or a specific cog by ID, to load code from hub RAM to be executed within cog/LUT RAM or to be executed right from hub RAM.

The format of Dest is `%E_N_xVVV` where:

- E controls loading (0=load from hub, 1=no load/hub exec)
- N controls target selection (0=specific cog ID, 1=find free cog)
- VVV is the cog ID or mode

The following predefined constants encode these bit patterns:

| Constant | Target | Execution | Description |
|----------|--------|-----------|-------------|
| COGEXEC + id | Specific Cog | Cog RAM | Load 496 longs from Hub to Cog RAM, execute from Cog |
| HUBEXEC + id | Specific Cog | Hub RAM | Execute directly from Hub RAM (no load) |
| COGEXEC_NEW | Any free Cog | Cog RAM | Auto-select available Cog, load and execute |
| HUBEXEC_NEW | Any free Cog | Hub RAM | Auto-select available Cog, execute from Hub |
| COGEXEC_NEW_PAIR | Adjacent pair | Cog RAM | Auto-select adjacent Cog pair for LUT sharing |
| HUBEXEC_NEW_PAIR | Adjacent pair | Hub RAM | Auto-select adjacent Cog pair, Hub execution |

For specific cog targeting, add the cog ID (0-7) to COGEXEC or HUBEXEC. The _NEW variants automatically select available resources.

The lower 20 bits of Src is the code address; the entire 32-bit Src is written to the target cog's PTRB. If COGINIT is preceded by SETQ, that value is written to the target cog's PTRA.

If the WC effect is specified, C is set (1) on failure or cleared (0) on success. When WC is given and Dest is a register, Dest receives the launched cog's ID (or $F on failure).

Common usage examples:

Load and start a specific cog from hub RAM:

```pasm2
        coginit #1, #$100             ' Load and start cog 1 from Hub $100
```

Start a free cog:

```pasm2
                coginit #COGEXEC_NEW, addr  wc  ' Find free cog, load, start
        if_c    jmp     #no_cog_available       ' Branch if no cog available
```

Skip load and execute from hub RAM:

```pasm2
        coginit #HUBEXEC+3, addr      ' Cog 3 hub exec mode
```

Start a cog pair for LUT sharing:

```pasm2
        coginit #HUBEXEC_NEW_PAIR, addr   ' Start free cog pair
```



::: instrheader
## COGSTOP {#cogstop}
Cog Stop

[Cog Control and Locks](#cog-control-and-locks) - Stops and terminates a running cog.
:::

**COGSTOP**  *{#}Dest*

---

**Result:** Cog indicated by Dest is terminated (stopped).

- Dest is the register or 9-bit literal indicating (in lowest 3 bits) which cog to stop.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000000011 | --- | --- | --- | 2-9 |


**Related:** [COGINIT](#coginit), [COGID](#cogid)

**Explanation:**

COGSTOP terminates the cog identified by Dest[2:0]. In this dormant state, the cog ceases to execute code and power consumption is greatly reduced.

The cog specified by the lower 3 bits of Dest (0-7) is immediately halted. All registers and state in that cog are lost. The cog can be restarted later using COGINIT, which will reload it with new code and reset its state.

For example, to stop cog 4:

```pasm2
        cogstop #4                    ' Stop cog 4
```

To stop the current cog (terminate self):

```pasm2
        cogid   myid                  ' Get my cog ID
        cogstop myid                  ' Stop myself
```

COGSTOP is useful for managing cog resources dynamically, shutting down cogs that are no longer needed, or resetting a cog before restarting it with new code. Note that stopping a cog does not free any hub memory it may have been using.



::: instrheader
## CRCBIT {#crcbit}
CRC Iterate Bit

[Arithmetic Operations](#arithmetic-operations) - Computes one bit iteration of a CRC calculation.
:::

**CRCBIT**  *Dest, {#}Src*

---

**Result:** Dest is updated with the next CRC iteration using the C flag and polynomial in Src.

- Dest is a register containing the current CRC value and is where the updated CRC is written.
- Src is a register or 9-bit literal containing the CRC polynomial.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001110 | 10I | DDDDDDDDD | SSSSSSSSS | --- | --- | D | 2 |


**Related:** [CRCNIB](#crcnib), [REV](#rev)

**Explanation:**

CRCBIT iterates the CRC value in Dest using the current C flag and the polynomial in Src. This instruction is designed for computing cyclic redundancy check (CRC) values bit by bit.

The operation performs a single bit iteration of a CRC calculation. The C flag represents the input bit, and Src contains the CRC polynomial. Dest contains the running CRC value and is updated with the result of this iteration.

The exact algorithm follows the standard CRC bit-wise computation:
1. Shift the CRC value in Dest left by one bit
2. If the original MSB XOR the input bit (C) is 1, XOR with the polynomial in Src

CRCBIT is typically used in a loop to process data one bit at a time:

```pasm2
        mov     crc, #0               ' Initialize CRC
.loop   rcl     data, #1        wc    ' Get next bit into C
        crcbit  crc, poly             ' Update CRC with bit
        djnz    count, #.loop         ' Repeat for all bits
```

For processing nibbles (4 bits) at a time instead, use CRCNIB.



::: instrheader
## CRCNIB {#crcnib}
CRC Iterate Nibble

[Arithmetic Operations](#arithmetic-operations) - Computes four bit iterations of a CRC calculation.
:::

**CRCNIB**  *Dest, {#}Src*

---

**Result:** Dest is updated with CRC iterations for a nibble, and Q is shifted left by 4 bits.

- Dest is a register containing the current CRC value and is where the updated CRC is written.
- Src is a register or 9-bit literal containing the CRC polynomial.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001110 | 11I | DDDDDDDDD | SSSSSSSSS | --- | --- | D | 2 |


**Related:** [CRCBIT](#crcbit), [REV](#rev)

**Explanation:**

CRCNIB iterates the CRC value in Dest for a nibble (4 bits) using the polynomial in Src, and shifts the Q register left by 4 bits. This instruction accelerates CRC calculations by processing 4 bits per instruction instead of 1.

CRCNIB performs four CRC bit-iterations in sequence, consuming the input bits from Q[31:28] (the high nibble), then shifts Q left by 4 bits to bring the next nibble into Q[31:28] for the following CRCNIB.

The typical usage pattern is:

```pasm2
        setq    data                  ' Load data into Q
        mov     crc, #0               ' Initialize CRC
.loop   crcnib  crc, poly             ' Process 4 bits from Q[31:28]
        ' Q is automatically shifted left by 4
        djnz    count, #.loop         ' Repeat for all nibbles
```

CRCNIB is more efficient than CRCBIT when processing byte-oriented data, providing a 4x speedup for CRC calculations. The automatic Q shift simplifies the loop logic for multi-nibble processing.



