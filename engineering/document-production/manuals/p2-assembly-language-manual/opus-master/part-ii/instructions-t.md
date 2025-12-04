# Instructions: T

This section contains all PASM2 instructions beginning with the letter T.



## TEST {#test}

Test

[Math and Logic](#math-and-logic) - Test the parity and zero state of a register value.

**TEST**  *Dest*  **{WC|WZ|WCZ}**
**TEST**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The parity and zero-state of Dest, or of Dest bitwise ANDed with Src, is stored in the C and Z flags.

- Dest is a register whose value will be tested.
- Src is an optional register, 9-bit literal, or 32-bit augmented literal to AND with Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0111110 | CZ0 | DDDDDDDDD | DDDDDDDDD | --- | Parity of D | D = 0 | 2 |
| EEEE | 0111110 | CZI | DDDDDDDDD | SSSSSSSSS | --- | Parity of (D \& S) | (D \& S) = 0 | 2 |


**Related:** [TESTN](#testn), [TESTB](#testb), [TESTBN](#testbn), [TESTP](#testp), [TESTPN](#testpn)

**Explanation:**

TEST determines the parity (number of high bits) and the zero or non-zero state of Dest, or of Dest bitwise ANDed with Src, and stores the results in the C and/or Z flag.

If the WC or WCZ effect is specified, the C flag is set to 1 if the number of high bits in Dest (or Dest ANDed with Src) is odd, or is cleared to 0 if it is even.

If the WZ or WCZ effect is specified, the Z flag is set to 1 if Dest (or Dest ANDed with Src) is zero, or is cleared to 0 if it is not zero.

TEST is non-destructive—it does not modify Dest.

::: pasm2
        TEST    flags WCZ      ' Test all bits for parity and zero
        TEST    value, #$FF WZ ' Test low byte for zero
:::



## TESTB {#testb}

Test bit

[Math and Logic](#math-and-logic) - Test a single bit in a register and write the result to C or Z.

**TESTB**  *Dest, {#}Src*  **WC/WZ**
**TESTB**  *Dest, {#}Src*  **ANDC/ANDZ**
**TESTB**  *Dest, {#}Src*  **ORC/ORZ**
**TESTB**  *Dest, {#}Src*  **XORC/XORZ**

---

**Result:** The state of bit Src[4:0] of Dest is read and either stored as-is, or bitwise ANDed, ORed, or XORed into C or Z.

- Dest is a register whose bit will be tested.
- Src is a register or 5-bit literal (0-31) specifying bit position.
- WC/WZ writes bit state directly to C or Z flag.
- ANDC/ANDZ ANDs bit state with C or Z flag.
- ORC/ORZ ORs bit state with C or Z flag.
- XORC/XORZ XORs bit state with C or Z flag.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0100000 | CZI | DDDDDDDDD | SSSSSSSSS | --- | D[S[4:0]] | D[S[4:0]] | 2 |
| EEEE | 0100010 | CZI | DDDDDDDDD | SSSSSSSSS | --- | C/Z AND D[S[4:0]] | C/Z AND D[S[4:0]] | 2 |
| EEEE | 0100100 | CZI | DDDDDDDDD | SSSSSSSSS | --- | C/Z OR D[S[4:0]] | C/Z OR D[S[4:0]] | 2 |
| EEEE | 0100110 | CZI | DDDDDDDDD | SSSSSSSSS | --- | C/Z XOR D[S[4:0]] | C/Z XOR D[S[4:0]] | 2 |


**Related:** [TESTBN](#testbn), [TESTP](#testp), [TESTPN](#testpn)

**Explanation:**

TESTB reads the state (0 or 1) of a bit in Dest designated by Src, and either stores it as-is, or bitwise ANDs, ORs, or XORs it into C or Z. The bit position is specified by Src[4:0] (0-31). The WC, WZ, ANDC, ANDZ, ORC, ORZ, XORC, or XORZ effect determines how the bit state is applied to the selected flag.

TESTB is useful for examining individual bits without modifying the register value.

::: pasm2
        TESTB   flags, #7 WC   ' Test bit 7, store in C
        TESTB   mask, #3 ANDC  ' AND bit 3 with current C
:::



## TESTBN {#testbn}

Test bit negated

[Math and Logic](#math-and-logic) - Test a single bit in a register, invert the result, and write to C or Z.

**TESTBN**  *Dest, {#}Src*  **WC/WZ**
**TESTBN**  *Dest, {#}Src*  **ANDC/ANDZ**
**TESTBN**  *Dest, {#}Src*  **ORC/ORZ**
**TESTBN**  *Dest, {#}Src*  **XORC/XORZ**

---

**Result:** The inverted state of bit Src[4:0] of Dest is read and either stored as-is, or bitwise ANDed, ORed, or XORed into C or Z.

- Dest is a register whose bit will be tested.
- Src is a register or 5-bit literal (0-31) specifying bit position.
- WC/WZ writes inverted bit state to C or Z flag.
- ANDC/ANDZ ANDs inverted bit state with C or Z flag.
- ORC/ORZ ORs inverted bit state with C or Z flag.
- XORC/XORZ XORs inverted bit state with C or Z flag.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0100001 | CZI | DDDDDDDDD | SSSSSSSSS | --- | !D[S[4:0]] | !D[S[4:0]] | 2 |
| EEEE | 0100011 | CZI | DDDDDDDDD | SSSSSSSSS | --- | C/Z AND !D[S[4:0]] | C/Z AND !D[S[4:0]] | 2 |
| EEEE | 0100101 | CZI | DDDDDDDDD | SSSSSSSSS | --- | C/Z OR !D[S[4:0]] | C/Z OR !D[S[4:0]] | 2 |
| EEEE | 0100111 | CZI | DDDDDDDDD | SSSSSSSSS | --- | C/Z XOR !D[S[4:0]] | C/Z XOR !D[S[4:0]] | 2 |


**Related:** [TESTB](#testb), [TESTP](#testp), [TESTPN](#testpn)

**Explanation:**

TESTBN reads the state (0 or 1) of a bit in Dest designated by Src, inverts that result, and either stores it as-is, or bitwise ANDs, ORs, or XORs it into C or Z. The bit position is specified by Src[4:0] (0-31). The WC, WZ, ANDC, ANDZ, ORC, ORZ, XORC, or XORZ effect determines how the inverted bit state is applied to the selected flag.

TESTBN is useful for testing whether a bit is clear (0) rather than set (1).



## TESTN {#testn}

Test not

[Math and Logic](#math-and-logic) - Test the parity and zero state of a register ANDed with an inverted value.

**TESTN**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The parity and zero-state of Dest bitwise ANDed with !Src is stored in the C and Z flags.

- Dest is a register whose value will be tested.
- Src is a register, 9-bit literal, or 32-bit augmented literal to invert and AND with Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0111111 | CZI | DDDDDDDDD | SSSSSSSSS | --- | Parity of (D \& !S) | (D \& !S) = 0 | 2 |


**Related:** [TEST](#test), [TESTB](#testb), [TESTBN](#testbn)

**Explanation:**

TESTN determines the parity (number of high bits) and the zero or non-zero state of Dest bitwise ANDed with !Src and stores the results in the C and/or Z flag.

If the WC or WCZ effect is specified, the C flag is set to 1 if the number of high bits in Dest ANDed with !Src is odd, or is cleared to 0 if it is even.

If the WZ or WCZ effect is specified, the Z flag is set to 1 if Dest ANDed with !Src is zero, or is cleared to 0 if it is not zero.

TESTN is non-destructive—it does not modify Dest. It is useful for testing which bits in Dest are set while masking out specific bits defined by Src.



## TESTP / TESTPN {#testp}

Test pin / Test pin negated {#testpn}

[Pin](#pin) - Test the state of an I/O pin and write the result (or inverted result) to C or Z.

**TESTP**  *{#}Dest*  **WC/WZ**
**TESTP**  *{#}Dest*  **ANDC/ANDZ**
**TESTP**  *{#}Dest*  **ORC/ORZ**
**TESTP**  *{#}Dest*  **XORC/XORZ**

**TESTPN**  *{#}Dest*  **WC/WZ**
**TESTPN**  *{#}Dest*  **ANDC/ANDZ**
**TESTPN**  *{#}Dest*  **ORC/ORZ**
**TESTPN**  *{#}Dest*  **XORC/XORZ**

---

**Result:** The state (TESTP) or inverted state (TESTPN) of the I/O pin described by Dest is read and either stored as-is, or bitwise ANDed, ORed, or XORed into C or Z.

- Dest is a register or 6-bit literal (0-63) identifying the I/O pin.
- WC/WZ writes pin state to C or Z flag.
- ANDC/ANDZ ANDs pin state with C or Z flag.
- ORC/ORZ ORs pin state with C or Z flag.
- XORC/XORZ XORs pin state with C or Z flag.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000000 | --- | IN | IN | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000001 | --- | !IN | !IN | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000010 | --- | C/Z AND IN | C/Z AND IN | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000011 | --- | C/Z AND !IN | C/Z AND !IN | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000100 | --- | C/Z OR IN | C/Z OR IN | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000101 | --- | C/Z OR !IN | C/Z OR !IN | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000110 | --- | C/Z XOR IN | C/Z XOR IN | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000111 | --- | C/Z XOR !IN | C/Z XOR !IN | 2 |


IN = pin state at Dest[5:0]; !IN = inverted pin state.

**Related:** [TESTB](#testb), [TESTBN](#testbn), [DRVL](instructions-d.md#drvl), [DRVH](instructions-d.md#drvh)

**Explanation:**

TESTP reads the state (0 or 1) of the I/O pin designated by Dest, and either stores it as-is, or bitwise ANDs, ORs, or XORs it into C or Z. TESTPN does the same but inverts the pin state first. The pin number is specified by Dest[5:0] (0-63). The WC, WZ, ANDC, ANDZ, ORC, ORZ, XORC, or XORZ effect determines how the pin state is applied to the selected flag.

Both instructions read the actual pin state from the IN register, not the output register. This makes them useful for reading sensor inputs, detecting edges, and building multi-bit values from pin states. TESTPN is particularly useful for active-low signals where a low pin state (0) indicates an active condition.

::: pasm2
        TESTP   #10 WC         ' Read pin 10 state into C
        TESTP   sensor_pin WZ  ' Test sensor pin, store in Z
        TESTPN  #button WC     ' C=1 if active-low button pressed
:::



## TJF / TJNF {#tjf}

Test and jump if full / not full {#tjnf}

[Branch](#branch) - Test a register value and jump based on full ($FFFF_FFFF) state.

**TJF**  *Dest, {#}Src*
**TJNF**  *Dest, {#}Src*

---

**Result:** Dest is tested and conditionally jumps based on full state.

- Dest is a register whose value is tested for full state.
- Src is a register, 9-bit literal, or 20-bit augmented literal specifying jump address.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011101 | 00I | DDDDDDDDD | SSSSSSSSS | PC (conditional) | --- | --- | 2 or 4 |
| EEEE | 1011101 | 01I | DDDDDDDDD | SSSSSSSSS | PC (conditional) | --- | --- | 2 or 4 |


**Related:** [TJZ](#tjz), [TJNZ](#tjnz), [TJS](#tjs), [TJNS](#tjns), [TJV](#tjv)

**Explanation:**

TJF and TJNF test Dest for "full" state ($FFFF_FFFF = -1 = all bits set) and conditionally jump:

| Instruction | Jumps when |
|-------------|------------|
| TJF | Dest = $FFFF_FFFF (full) |
| TJNF | Dest ≠ $FFFF_FFFF (not full) |

The address (Src) can be absolute or relative. To specify an absolute address, Src must be a register containing a 20-bit address value. To specify a relative address, use #Label for a 9-bit signed offset or use ##Label for a 20-bit signed offset. Offsets are relative to the instruction following the TJF/TJNF.

Takes 2 clocks when not jumping, 4 clocks when jumping (pipeline flush).



## TJS / TJNS {#tjs}

Test and jump if signed / not signed {#tjns}

[Branch](#branch) - Test a register value and jump based on sign bit state.

**TJS**  *Dest, {#}Src*
**TJNS**  *Dest, {#}Src*

---

**Result:** Dest is tested and conditionally jumps based on sign bit state.

- Dest is a register whose value is tested for sign bit.
- Src is a register, 9-bit literal, or 20-bit augmented literal specifying jump address.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011101 | 10I | DDDDDDDDD | SSSSSSSSS | PC (conditional) | --- | --- | 2 or 4 |
| EEEE | 1011101 | 11I | DDDDDDDDD | SSSSSSSSS | PC (conditional) | --- | --- | 2 or 4 |


**Related:** [TJZ](#tjz), [TJNZ](#tjnz), [TJF](#tjf), [TJNF](#tjnf), [TJV](#tjv)

**Explanation:**

TJS and TJNS test the sign bit (bit 31) of Dest and conditionally jump:

| Instruction | Jumps when |
|-------------|------------|
| TJS | Dest[31] = 1 (negative/signed) |
| TJNS | Dest[31] = 0 (positive/unsigned) |

The address (Src) can be absolute or relative. To specify an absolute address, Src must be a register containing a 20-bit address value. To specify a relative address, use #Label for a 9-bit signed offset or use ##Label for a 20-bit signed offset. Offsets are relative to the instruction following the TJS/TJNS.

Takes 2 clocks when not jumping, 4 clocks when jumping (pipeline flush).



## TJZ / TJNZ {#tjz}

Test and jump if zero / not zero {#tjnz}

[Branch](#branch) - Test a register value and jump based on zero/non-zero result.

**TJZ**  *Dest, {#}Src*
**TJNZ**  *Dest, {#}Src*

---

**Result:** Dest is tested (not modified), and conditionally jumps based on zero/non-zero result.

- Dest is a register whose value is tested (unchanged).
- Src is the jump address: use # for relative, omit for absolute.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011100 | 10I | DDDDDDDDD | SSSSSSSSS | PC* | --- | --- | 2 or 4 |
| EEEE | 1011100 | 11I | DDDDDDDDD | SSSSSSSSS | PC* | --- | --- | 2 or 4 |

```{=latex}
*PC is written only when the jump condition is met.
```


**Related:** [TJF](#tjf), [TJNF](#tjnf), [TJS](#tjs), [TJNS](#tjns), [TJV](#tjv), [DJZ](instructions-d.md#djz), [DJNZ](instructions-d.md#djnz)

**Explanation:**

TJZ and TJNZ test Dest (without modifying it) and conditionally jump based on whether the value is zero or non-zero:

| Instruction | Jumps when |
|-------------|------------|
| TJZ | Dest = 0 |
| TJNZ | Dest ≠ 0 |

Unlike DJZ/DJNZ which decrement before testing, these instructions only test.

::: pasm2
        TJNZ    count, #loop   ' Loop while count <> 0
        TJZ     count, #done   ' Exit when count = 0
:::

Takes 2 clocks when not jumping, 4 clocks when jumping (pipeline flush).



## TJV {#tjv}

Test and jump if overflow

[Branch](#branch) - Test a register value against the C flag and jump if overflow occurred.

**TJV**  *Dest, {#}Src*

---

**Result:** Dest is tested against C and if it has overflowed (Dest[31] != C), PC is set to a new relative (#Src) or absolute (Src) address.

- Dest is a register whose value is tested for overflow.
- Src is a register, 9-bit literal, or 20-bit augmented literal specifying jump address.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 00I | DDDDDDDDD | SSSSSSSSS | PC (conditional) | --- | --- | 2 or 4 |


**Related:** [ADDS](instructions-a.md#adds), [ADDSX](instructions-a.md#addsx), [SUBS](instructions-s.md#subs), [SUBSX](instructions-s.md#subsx)

**Explanation:**

TJV tests the value in Dest against C and jumps to the address described by Src if Dest has overflowed (Dest[31] != C). This instruction requires that C be updated (to the correct sign) by the previous ADDS, ADDSX, SUBS, SUBSX, CMPS, CMPSX, or SUMx instruction. The address (Src) can be absolute or relative.

The instruction takes 2 cycles if the jump is not taken, or 4 cycles if taken.

::: pasm2
        ADDS    result, delta WC  ' Signed add, update C
        TJV     result, #overflow_handler
:::






## TRGINT1 / TRGINT2 / TRGINT3 {#trgint1}

Trigger interrupt (1, 2, or 3) {#trgint2} {#trgint3}

[Interrupt](#interrupt) - Software-trigger interrupt handler.

**TRGINT1**
**TRGINT2**
**TRGINT3**

---

**Result:** The specified interrupt handler (INT1, INT2, or INT3) is triggered regardless of STALLI mode.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | 000100010 | 000100100 | --- | --- | --- | 2 |
| EEEE | 1101011 | 000 | 000100011 | 000100100 | --- | --- | --- | 2 |
| EEEE | 1101011 | 000 | 000100100 | 000100100 | --- | --- | --- | 2 |


**Related:** [SETINT1/2/3](instructions-s.md#setint1), [NIXINT1/2/3](instructions-n.md#nixint1), [RETI0/1/2/3](instructions-r.md#reti0), [RESI0/1/2/3](instructions-r.md#resi0)

**Explanation:**

TRGINT1, TRGINT2, and TRGINT3 software-trigger their respective interrupt handlers, regardless of STALLI mode. This allows code to explicitly invoke interrupt service routines without waiting for external events.

The P2 provides three independent interrupt levels, and each TRGINT instruction triggers only its corresponding level. Use these instructions when you need to invoke an interrupt handler programmatically.

