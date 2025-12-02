# Instructions: T

This section contains all PASM2 instructions beginning with the letter T.



## TEST {#test}

Test
[Logic Instruction](\#logic-instructions) - Test the parity and zero state of a register value.

**TEST**  *Dest*  **\{WC|WZ|WCZ\}**
**TEST**  *Dest, {\#}Src*  **\{WC|WZ|WCZ\}**

---

**Result:** The parity and zero-state of Dest, or of Dest bitwise ANDed with Src, is stored in the C and Z flags.

- Dest is a register whose value will be tested.
- Src is an optional register, 9-bit literal, or 32-bit augmented literal to AND with Dest.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{0111110}{CZ0}{DDDDDDDDD}{DDDDDDDDD}{---}{Parity of D}{D = 0}{2}
\encodingrow{EEEE}{0111110}{CZI}{DDDDDDDDD}{SSSSSSSSS}{---}{Parity of (D \& S)}{(D \& S) = 0}{2}
\end{encodingtable}
```

**Related:** [TESTN](\#testn), [TESTB](\#testb), [TESTBN](\#testbn), [TESTP](\#testp), [TESTPN](\#testpn)

**Explanation:**

TEST determines the parity (number of high bits) and the zero or non-zero state of Dest, or of Dest bitwise ANDed with Src, and stores the results in the C and/or Z flag.

If the WC or WCZ effect is specified, the C flag is set to 1 if the number of high bits in Dest (or Dest ANDed with Src) is odd, or is cleared to 0 if it is even.

If the WZ or WCZ effect is specified, the Z flag is set to 1 if Dest (or Dest ANDed with Src) is zero, or is cleared to 0 if it is not zero.

TEST is non-destructive—it does not modify Dest.

::: pasm2
        TEST    flags WCZ      ' Test all bits for parity and zero
        TEST    value, \#\$FF WZ ' Test low byte for zero
:::



## TESTB {#testb}

Test bit
[Bit Test Instruction](\#bit-test-instructions) - Test a single bit in a register and write the result to C or Z.

**TESTB**  *Dest, {\#}Src*  **WC/WZ**
**TESTB**  *Dest, {\#}Src*  **ANDC/ANDZ**
**TESTB**  *Dest, {\#}Src*  **ORC/ORZ**
**TESTB**  *Dest, {\#}Src*  **XORC/XORZ**

---

**Result:** The state of bit Src[4:0] of Dest is read and either stored as-is, or bitwise ANDed, ORed, or XORed into C or Z.

- Dest is a register whose bit will be tested.
- Src is a register or 5-bit literal (0-31) specifying bit position.
- WC/WZ writes bit state directly to C or Z flag.
- ANDC/ANDZ ANDs bit state with C or Z flag.
- ORC/ORZ ORs bit state with C or Z flag.
- XORC/XORZ XORs bit state with C or Z flag.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{0100000}{CZI}{DDDDDDDDD}{SSSSSSSSS}{---}{D[S[4:0]]}{D[S[4:0]]}{2}
\encodingrowcont{EEEE}{0100010}{CZI}{DDDDDDDDD}{SSSSSSSSS}{---}{C/Z AND D[S[4:0]]}{C/Z AND D[S[4:0]]}{2}
\encodingrowcont{EEEE}{0100100}{CZI}{DDDDDDDDD}{SSSSSSSSS}{---}{C/Z OR D[S[4:0]]}{C/Z OR D[S[4:0]]}{2}
\encodingrow{EEEE}{0100110}{CZI}{DDDDDDDDD}{SSSSSSSSS}{---}{C/Z XOR D[S[4:0]]}{C/Z XOR D[S[4:0]]}{2}
\end{encodingtable}
```

**Related:** [TESTBN](\#testbn), [TESTP](\#testp), [TESTPN](\#testpn)

**Explanation:**

TESTB reads the state (0 or 1) of a bit in Dest designated by Src, and either stores it as-is, or bitwise ANDs, ORs, or XORs it into C or Z. The bit position is specified by Src[4:0] (0-31). The WC, WZ, ANDC, ANDZ, ORC, ORZ, XORC, or XORZ effect determines how the bit state is applied to the selected flag.

TESTB is useful for examining individual bits without modifying the register value.

::: pasm2
        TESTB   flags, \#7 WC   ' Test bit 7, store in C
        TESTB   mask, \#3 ANDC  ' AND bit 3 with current C
:::



## TESTBN {#testbn}

Test bit negated
[Bit Test Instruction](\#bit-test-instructions) - Test a single bit in a register, invert the result, and write to C or Z.

**TESTBN**  *Dest, {\#}Src*  **WC/WZ**
**TESTBN**  *Dest, {\#}Src*  **ANDC/ANDZ**
**TESTBN**  *Dest, {\#}Src*  **ORC/ORZ**
**TESTBN**  *Dest, {\#}Src*  **XORC/XORZ**

---

**Result:** The inverted state of bit Src[4:0] of Dest is read and either stored as-is, or bitwise ANDed, ORed, or XORed into C or Z.

- Dest is a register whose bit will be tested.
- Src is a register or 5-bit literal (0-31) specifying bit position.
- WC/WZ writes inverted bit state to C or Z flag.
- ANDC/ANDZ ANDs inverted bit state with C or Z flag.
- ORC/ORZ ORs inverted bit state with C or Z flag.
- XORC/XORZ XORs inverted bit state with C or Z flag.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{0100001}{CZI}{DDDDDDDDD}{SSSSSSSSS}{---}{!D[S[4:0]]}{!D[S[4:0]]}{2}
\encodingrowcont{EEEE}{0100011}{CZI}{DDDDDDDDD}{SSSSSSSSS}{---}{C/Z AND !D[S[4:0]]}{C/Z AND !D[S[4:0]]}{2}
\encodingrowcont{EEEE}{0100101}{CZI}{DDDDDDDDD}{SSSSSSSSS}{---}{C/Z OR !D[S[4:0]]}{C/Z OR !D[S[4:0]]}{2}
\encodingrow{EEEE}{0100111}{CZI}{DDDDDDDDD}{SSSSSSSSS}{---}{C/Z XOR !D[S[4:0]]}{C/Z XOR !D[S[4:0]]}{2}
\end{encodingtable}
```

**Related:** [TESTB](\#testb), [TESTP](\#testp), [TESTPN](\#testpn)

**Explanation:**

TESTBN reads the state (0 or 1) of a bit in Dest designated by Src, inverts that result, and either stores it as-is, or bitwise ANDs, ORs, or XORs it into C or Z. The bit position is specified by Src[4:0] (0-31). The WC, WZ, ANDC, ANDZ, ORC, ORZ, XORC, or XORZ effect determines how the inverted bit state is applied to the selected flag.

TESTBN is useful for testing whether a bit is clear (0) rather than set (1).



## TESTN {#testn}

Test not
[Logic Instruction](\#logic-instructions) - Test the parity and zero state of a register ANDed with an inverted value.

**TESTN**  *Dest, {\#}Src*  **\{WC|WZ|WCZ\}**

---

**Result:** The parity and zero-state of Dest bitwise ANDed with !Src is stored in the C and Z flags.

- Dest is a register whose value will be tested.
- Src is a register, 9-bit literal, or 32-bit augmented literal to invert and AND with Dest.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0111111}{CZI}{DDDDDDDDD}{SSSSSSSSS}{---}{Parity of (D \& !S)}{(D \& !S) = 0}{2}
```

**Related:** [TEST](\#test), [TESTB](\#testb), [TESTBN](\#testbn)

**Explanation:**

TESTN determines the parity (number of high bits) and the zero or non-zero state of Dest bitwise ANDed with !Src and stores the results in the C and/or Z flag.

If the WC or WCZ effect is specified, the C flag is set to 1 if the number of high bits in Dest ANDed with !Src is odd, or is cleared to 0 if it is even.

If the WZ or WCZ effect is specified, the Z flag is set to 1 if Dest ANDed with !Src is zero, or is cleared to 0 if it is not zero.

TESTN is non-destructive—it does not modify Dest. It is useful for testing which bits in Dest are set while masking out specific bits defined by Src.



## TESTP / TESTPN {#testp}

Test pin / Test pin negated \{\#testpn\}
[Pin Instruction](\#pin-instructions) - Test the state of an I/O pin and write the result (or inverted result) to C or Z.

**TESTP**  *{\#}Dest*  **WC/WZ**
**TESTP**  *{\#}Dest*  **ANDC/ANDZ**
**TESTP**  *{\#}Dest*  **ORC/ORZ**
**TESTP**  *{\#}Dest*  **XORC/XORZ**

**TESTPN**  *{\#}Dest*  **WC/WZ**
**TESTPN**  *{\#}Dest*  **ANDC/ANDZ**
**TESTPN**  *{\#}Dest*  **ORC/ORZ**
**TESTPN**  *{\#}Dest*  **XORC/XORZ**

---

**Result:** The state (TESTP) or inverted state (TESTPN) of the I/O pin described by Dest is read and either stored as-is, or bitwise ANDed, ORed, or XORed into C or Z.

- Dest is a register or 6-bit literal (0-63) identifying the I/O pin.
- WC/WZ writes pin state to C or Z flag.
- ANDC/ANDZ ANDs pin state with C or Z flag.
- ORC/ORZ ORs pin state with C or Z flag.
- XORC/XORZ XORs pin state with C or Z flag.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1101011}{CZL}{DDDDDDDDD}{001000000}{---}{IN}{IN}{2}
\encodingrowcont{EEEE}{1101011}{CZL}{DDDDDDDDD}{001000001}{---}{!IN}{!IN}{2}
\encodingrowcont{EEEE}{1101011}{CZL}{DDDDDDDDD}{001000010}{---}{C/Z AND IN}{C/Z AND IN}{2}
\encodingrowcont{EEEE}{1101011}{CZL}{DDDDDDDDD}{001000011}{---}{C/Z AND !IN}{C/Z AND !IN}{2}
\encodingrowcont{EEEE}{1101011}{CZL}{DDDDDDDDD}{001000100}{---}{C/Z OR IN}{C/Z OR IN}{2}
\encodingrowcont{EEEE}{1101011}{CZL}{DDDDDDDDD}{001000101}{---}{C/Z OR !IN}{C/Z OR !IN}{2}
\encodingrowcont{EEEE}{1101011}{CZL}{DDDDDDDDD}{001000110}{---}{C/Z XOR IN}{C/Z XOR IN}{2}
\encodingrow{EEEE}{1101011}{CZL}{DDDDDDDDD}{001000111}{---}{C/Z XOR !IN}{C/Z XOR !IN}{2}
\end{encodingtable}
```

IN = pin state at Dest[5:0]; !IN = inverted pin state.

**Related:** [TESTB](\#testb), [TESTBN](\#testbn), [DRVL](\#drvl), [DRVH](\#drvh)

**Explanation:**

TESTP reads the state (0 or 1) of the I/O pin designated by Dest, and either stores it as-is, or bitwise ANDs, ORs, or XORs it into C or Z. TESTPN does the same but inverts the pin state first. The pin number is specified by Dest[5:0] (0-63). The WC, WZ, ANDC, ANDZ, ORC, ORZ, XORC, or XORZ effect determines how the pin state is applied to the selected flag.

Both instructions read the actual pin state from the IN register, not the output register. This makes them useful for reading sensor inputs, detecting edges, and building multi-bit values from pin states. TESTPN is particularly useful for active-low signals where a low pin state (0) indicates an active condition.

::: pasm2
        TESTP   \#10 WC         ' Read pin 10 state into C
        TESTP   sensor\_pin WZ  ' Test sensor pin, store in Z
        TESTPN  \#button WC     ' C=1 if active-low button pressed
:::



## TJF {#tjf}

Test and jump if full
[Flow Control Instruction](\#flow-control-instructions) - Test a register value and jump if it equals \$FFFF\_FFFF.

**TJF**  *Dest, {\#}Src*

---

**Result:** Dest is tested and if it is full (\$FFFF\_FFFF), PC is set to a new relative (\#Src) or absolute (Src) address.

- Dest is a register whose value is tested for full.
- Src is a register, 9-bit literal, or 20-bit augmented literal specifying jump address.

```{=latex}
\simpleencoding{EEEE}{1011101}{00I}{DDDDDDDDD}{SSSSSSSSS}{PC (conditional)}{---}{---}{2 or 4}
```

**Related:** [TJNF](\#tjnf), [TJZ](\#tjz), [TJNZ](\#tjnz)

**Explanation:**

TJF tests the value in Dest and jumps to the address described by Src if the result is full (= -1; = \$FFFF\_FFFF).

The address (Src) can be absolute or relative. To specify an absolute address, Src must be a register containing a 20-bit address value. To specify a relative address, use \#Label for a 9-bit signed offset (a range of -256 to +255 instructions) or use \#\#Label (or insert a prior AUGS instruction) for a 20-bit signed offset (a range of -524288 to +524287). Offsets are relative to the instruction following the TJF.

The instruction takes 2 cycles if the jump is not taken, or 4 cycles if taken (13-20 cycles for Hub execution when taken).



## TJNF {#tjnf}

Test and jump if not full
[Flow Control Instruction](\#flow-control-instructions) - Test a register value and jump if it does not equal \$FFFF\_FFFF.

**TJNF**  *Dest, {\#}Src*

---

**Result:** Dest is tested and if it is not full (<> \$FFFF\_FFFF), PC is set to a new relative (\#Src) or absolute (Src) address.

- Dest is a register whose value is tested for not full.
- Src is a register, 9-bit literal, or 20-bit augmented literal specifying jump address.

```{=latex}
\simpleencoding{EEEE}{1011101}{01I}{DDDDDDDDD}{SSSSSSSSS}{PC (conditional)}{---}{---}{2 or 4}
```

**Related:** [TJF](\#tjf), [TJZ](\#tjz), [TJNZ](\#tjnz), [TJS](\#tjs), [TJNS](\#tjns)

**Explanation:**

TJNF tests the value in Dest and jumps to the address described by Src if the result is not full (<> -1; <> \$FFFF\_FFFF).

The address (Src) can be absolute or relative. To specify an absolute address, Src must be a register containing a 20-bit address value. To specify a relative address, use \#Label for a 9-bit signed offset or use \#\#Label for a 20-bit signed offset. Offsets are relative to the instruction following the TJNF.

The instruction takes 2 cycles if the jump is not taken, or 4 cycles if taken.



## TJNS {#tjns}

Test and jump if not signed
[Flow Control Instruction](\#flow-control-instructions) - Test a register value and jump if bit 31 is clear (positive/unsigned).

**TJNS**  *Dest, {\#}Src*

---

**Result:** Dest is tested and if it is not signed (Dest[31] = 0), PC is set to a new relative (\#Src) or absolute (Src) address.

- Dest is a register whose value is tested for sign bit.
- Src is a register, 9-bit literal, or 20-bit augmented literal specifying jump address.

```{=latex}
\simpleencoding{EEEE}{1011101}{11I}{DDDDDDDDD}{SSSSSSSSS}{PC (conditional)}{---}{---}{2 or 4}
```

**Related:** [TJS](\#tjs), [TJZ](\#tjz), [TJNZ](\#tjnz)

**Explanation:**

TJNS tests the value in Dest and jumps to the address described by Src if the value is not signed (Dest[31] = 0). The address (Src) can be absolute or relative. To specify an absolute address, Src must be a register containing a 20-bit address value. To specify a relative address, use \#Label for a 9-bit signed offset or use \#\#Label for a 20-bit signed offset. Offsets are relative to the instruction following the TJNS.

The instruction takes 2 cycles if the jump is not taken, or 4 cycles if taken.



## TJZ / TJNZ {#tjz}

Test and jump if zero / not zero \{\#tjnz\}
[Flow Control Instruction](\#flow-control-instructions) - Test a register value and jump based on zero/non-zero result.

**TJZ**  *Dest, {\#}Src*
**TJNZ**  *Dest, {\#}Src*

---

**Result:** Dest is tested (not modified), and conditionally jumps:

| Instruction | Jumps when |
|-------------|------------|
| TJZ | Dest = 0 |
| TJNZ | Dest ≠ 0 |

- Dest is a register whose value is tested (unchanged).
- Src is the jump address: use \# for relative, omit for absolute.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1011100}{10I}{DDDDDDDDD}{SSSSSSSSS}{PC*}{---}{---}{2 or 4}
\encodingrow{EEEE}{1011100}{11I}{DDDDDDDDD}{SSSSSSSSS}{PC*}{---}{---}{2 or 4}
\end{encodingtable}

*PC is written only when the jump condition is met.
```

**Related:** [TJF](\#tjf), [TJNF](\#tjnf), [TJS](\#tjs), [TJNS](\#tjns), [TJV](\#tjv), [DJZ](\#djz), [DJNZ](\#djnz)

**Explanation:**

TJZ and TJNZ test Dest (without modifying it) and conditionally jump based on whether the value is zero or non-zero.

Unlike DJZ/DJNZ which decrement before testing, these instructions only test.

::: pasm2
        TJNZ    count, \#loop   ' Loop while count <> 0
        TJZ     count, \#done   ' Exit when count = 0
:::

Takes 2 clocks when not jumping, 4 clocks when jumping (pipeline flush).



## TJS {#tjs}

Test and jump if signed
[Flow Control Instruction](\#flow-control-instructions) - Test a register value and jump if bit 31 is set (negative).

**TJS**  *Dest, {\#}Src*

---

**Result:** Dest is tested and if it is signed (Dest[31] = 1), PC is set to a new relative (\#Src) or absolute (Src) address.

- Dest is a register whose value is tested for sign bit.
- Src is a register, 9-bit literal, or 20-bit augmented literal specifying jump address.

```{=latex}
\simpleencoding{EEEE}{1011101}{10I}{DDDDDDDDD}{SSSSSSSSS}{PC (conditional)}{---}{---}{2 or 4}
```

**Related:** [TJNS](\#tjns), [TJF](\#tjf), [TJNF](\#tjnf), [TJZ](\#tjz), [TJNZ](\#tjnz)

**Explanation:**

TJS tests the value in Dest and jumps to the address described by Src if the result is signed (Dest[31] = 1).

The address (Src) can be absolute or relative. To specify an absolute address, Src must be a register containing a 20-bit address value. To specify a relative address, use \#Label for a 9-bit signed offset or use \#\#Label for a 20-bit signed offset. Offsets are relative to the instruction following the TJS.

The instruction takes 2 cycles if the jump is not taken, or 4 cycles if taken.

::: pasm2
        TJS     value, \#negative\_handler  ' Jump if negative
:::



## TJV {#tjv}

Test and jump if overflow
[Flow Control Instruction](\#flow-control-instructions) - Test a register value against the C flag and jump if overflow occurred.

**TJV**  *Dest, {\#}Src*

---

**Result:** Dest is tested against C and if it has overflowed (Dest[31] != C), PC is set to a new relative (\#Src) or absolute (Src) address.

- Dest is a register whose value is tested for overflow.
- Src is a register, 9-bit literal, or 20-bit augmented literal specifying jump address.

```{=latex}
\simpleencoding{EEEE}{1011110}{00I}{DDDDDDDDD}{SSSSSSSSS}{PC (conditional)}{---}{---}{2 or 4}
```

**Related:** [ADDS](\#adds), [ADDSX](\#addsx), [SUBS](\#subs), [SUBSX](\#subsx)

**Explanation:**

TJV tests the value in Dest against C and jumps to the address described by Src if Dest has overflowed (Dest[31] != C). This instruction requires that C be updated (to the correct sign) by the previous ADDS, ADDSX, SUBS, SUBSX, CMPS, CMPSX, or SUMx instruction. The address (Src) can be absolute or relative.

The instruction takes 2 cycles if the jump is not taken, or 4 cycles if taken.

::: pasm2
        ADDS    result, delta WC  ' Signed add, update C
        TJV     result, \#overflow\_handler
:::






## TRGINT1 {#trgint1}

Trigger interrupt 1
[Interrupt Instruction](\#interrupt-instructions) - Software-trigger interrupt handler 1.

**TRGINT1**

---

**Result:** The INT1 interrupt handler is triggered regardless of STALLI mode.

```{=latex}
\simpleencoding{EEEE}{1101011}{000}{000100010}{000100100}{---}{---}{---}{2}
```

**Related:** [TRGINT2](\#trgint2), [TRGINT3](\#trgint3), [SETINT1](\#setint1), [NIXINT1](\#nixint1), [RETI0](\#reti0)

**Explanation:**

TRGINT1 software-triggers interrupt handler 1, regardless of STALLI mode. This allows code to explicitly invoke the INT1 service routine without waiting for external events.



## TRGINT2 {#trgint2}

Trigger interrupt 2
[Interrupt Instruction](\#interrupt-instructions) - Software-trigger interrupt handler 2.

**TRGINT2**

---

**Result:** The INT2 interrupt handler is triggered regardless of STALLI mode.

```{=latex}
\simpleencoding{EEEE}{1101011}{000}{000100011}{000100100}{---}{---}{---}{2}
```

**Related:** [TRGINT1](\#trgint1), [TRGINT3](\#trgint3), [SETINT2](\#setint2), [NIXINT2](\#nixint2), [RETI0](\#reti0)

**Explanation:**

TRGINT2 software-triggers interrupt handler 2, regardless of STALLI mode. This allows code to explicitly invoke the INT2 service routine without waiting for external events.



## TRGINT3 {#trgint3}

Trigger interrupt 3
[Interrupt Instruction](\#interrupt-instructions) - Software-trigger interrupt handler 3.

**TRGINT3**

---

**Result:** The INT3 interrupt handler is triggered regardless of STALLI mode.

```{=latex}
\simpleencoding{EEEE}{1101011}{000}{000100100}{000100100}{---}{---}{---}{2}
```

**Related:** [TRGINT1](\#trgint1), [TRGINT2](\#trgint2), [SETINT3](\#setint3), [NIXINT3](\#nixint3), [RETI0](\#reti0)

**Explanation:**

TRGINT3 software-triggers interrupt handler 3, regardless of STALLI mode. This allows code to explicitly invoke the INT3 service routine without waiting for external events.

