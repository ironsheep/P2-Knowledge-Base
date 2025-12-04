# Instructions: N

This section contains all PASM2 instructions beginning with the letter N.



## NEG {#neg}

Negate
[Math and Logic](#math-and-logic) - Negate a value.

**NEG**  *Dest, {#}Src*  **{WC|WZ|WCZ}**
**NEG**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** The Src or Dest value is negated and stored into Dest.

- Dest is a register to receive the -Src value (syntax 1), or contains the value to negate (syntax 2).
- Src is an optional register, 9-bit literal, or 32-bit augmented literal whose negated value is stored into Dest.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{0110011}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Sign of result}{Result = 0}{2}
\encodingrow{EEEE}{0110011}{CZ0}{DDDDDDDDD}{DDDDDDDDD}{D}{Sign of result}{Result = 0}{2}
\end{encodingtable}
```

**Related:** [ABS](#abs), [NEGC](#negc), [NEGNC](#negnc), [NEGZ](#negz), [NEGNZ](#negnz)

**Explanation:**

NEG negates the value in Src (syntax 1) or Dest (syntax 2) and stores the result in the Dest register. The negation flips the value's sign; for example, 78 becomes -78, or -306 becomes 306.

When using syntax 1, NEG negates the Src operand and stores the result into Dest. When using syntax 2 (where Src is omitted), NEG negates the value already in Dest and stores the result back into Dest.

If the WC or WCZ effect is specified, the C flag is set (1) if the result is negative, or is cleared (0) if positive.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if it is non-zero.



## NEGC / NEGNC / NEGZ / NEGNZ {#negc}

Conditional negate {#negnc} {#negz} {#negnz}
[Math and Logic](#math-and-logic) - Negate value according to C, NC, Z, or NZ flag.

**NEGC**  *Dest, {#}Src*  **{WC|WZ|WCZ}**
**NEGC**  *Dest*  **{WC|WZ|WCZ}**

**NEGNC**  *Dest, {#}Src*  **{WC|WZ|WCZ}**
**NEGNC**  *Dest*  **{WC|WZ|WCZ}**

**NEGZ**  *Dest, {#}Src*  **{WC|WZ|WCZ}**
**NEGZ**  *Dest*  **{WC|WZ|WCZ}**

**NEGNZ**  *Dest, {#}Src*  **{WC|WZ|WCZ}**
**NEGNZ**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** The Src or Dest value, conditionally negated based on flag state, is stored into Dest.

| Instruction | Negates when |
|-------------|--------------|
| NEGC | C = 1 |
| NEGNC | C = 0 |
| NEGZ | Z = 1 |
| NEGNZ | Z = 0 |

- Dest is a register to receive the result.
- Src is an optional register, 9-bit literal, or 32-bit augmented literal.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{0110100}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Sign}{Result = 0}{2}
\encodingrowcont{EEEE}{0110100}{CZ0}{DDDDDDDDD}{DDDDDDDDD}{D}{Sign}{Result = 0}{2}
\encodingrowcont{EEEE}{0110101}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Sign}{Result = 0}{2}
\encodingrowcont{EEEE}{0110101}{CZ0}{DDDDDDDDD}{DDDDDDDDD}{D}{Sign}{Result = 0}{2}
\encodingrowcont{EEEE}{0110110}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Sign}{Result = 0}{2}
\encodingrowcont{EEEE}{0110110}{CZ0}{DDDDDDDDD}{DDDDDDDDD}{D}{Sign}{Result = 0}{2}
\encodingrowcont{EEEE}{0110111}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Sign}{Result = 0}{2}
\encodingrow{EEEE}{0110111}{CZ0}{DDDDDDDDD}{DDDDDDDDD}{D}{Sign}{Result = 0}{2}
\end{encodingtable}
```

**Related:** [NEG](#neg)

**Explanation:**

These instructions conditionally negate the value in Src (two-operand form) or Dest (single-operand form) based on the specified flag condition. If the condition is true, the value is negated (sign flipped) before being stored in Dest. If the condition is false, the value is stored unchanged.

NEGC and NEGZ negate when their flag is set (1). NEGNC and NEGNZ negate when their flag is clear (0), providing complementary behavior.

If the WC or WCZ effect is specified, the C flag is set (1) if the result is negative, or cleared (0) if positive.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result is zero, or cleared (0) if non-zero.



## NIXINT1 / NIXINT2 / NIXINT3 {#nixint1}

Cancel interrupt (1, 2, or 3)
[Event](#event) - Cancel INTn interrupt.

**NIXINT1**
**NIXINT2**
**NIXINT3**

---

**Result:** The specified interrupt event (INT1, INT2, or INT3) is cancelled.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1101011}{000}{000100101}{000100100}{---}{---}{---}{2}
\encodingrowcont{EEEE}{1101011}{000}{000100110}{000100100}{---}{---}{---}{2}
\encodingrow{EEEE}{1101011}{000}{000100111}{000100100}{---}{---}{---}{2}
\end{encodingtable}
```

**Related:** [SETINT1/2/3](instructions-s.md#setint1), [TRGINT1/2/3](instructions-t.md#trgint1), [RETI0/1/2/3](instructions-r.md#reti0), [RESI0/1/2/3](instructions-r.md#resi0)

**Explanation:**

NIXINT1, NIXINT2, and NIXINT3 cancel any pending interrupt events for their respective interrupt levels. These instructions prevent the interrupt from occurring even if its event condition has been met.

The P2 provides three independent interrupt levels, and each NIXINT instruction cancels only its corresponding level. Use these instructions when an interrupt that was previously configured is no longer needed or when the program needs to explicitly clear a pending interrupt condition before it can trigger cog execution flow changes.



## NOP {#nop}

No operation
[Miscellaneous](#miscellaneous) - No operation, just elapse two cycles.

**NOP**

---

**Result:** Two clock cycles are consumed.

```{=latex}
\simpleencoding{0000}{0000000}{000}{000000000}{000000000}{---}{---}{---}{2}
```

**Related:** [WAITX](#waitx), [WAITCNT](#waitcnt)

**Explanation:**

NOP simply consumes two clock cycles without performing any operation. No registers are modified, no flags are affected, and no memory is accessed.

NOP is primarily used for timing adjustments, creating precise delays, or as a placeholder during development. It can also be used to align code for performance optimization or to fill instruction slots in pipelined operations.



## NOT {#not}

Not
[Math and Logic](#math-and-logic) - Bitwise NOT a value.

**NOT**  *Dest, {#}Src*  **{WC|WZ|WCZ}**
**NOT**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** The bitwise NOT of Src or Dest is stored in Dest.

- Dest is the register containing the value to bitwise NOT (syntax 2) or to be replaced by the bitwise NOT of Src (syntax 1).
- Src is an optional register, 9-bit literal, or 32-bit augmented literal whose value will be bitwise NOTed and stored into Dest.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{0110001}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{!S[31]}{Result = 0}{2}
\encodingrow{EEEE}{0110001}{CZ0}{DDDDDDDDD}{DDDDDDDDD}{D}{!D[31]}{Result = 0}{2}
\end{encodingtable}
```

**Related:** [AND](#and), [OR](#or), [XOR](#xor), [ANDN](#andn)

**Explanation:**

NOT performs a bitwise NOT operation, inverting all bits of the value in Src (syntax 1) or Dest (syntax 2), and stores the result into Dest. Each 0 bit becomes 1, and each 1 bit becomes 0.

When using syntax 1, NOT inverts the Src operand and stores the result into Dest. When using syntax 2 (where Src is omitted), NOT inverts the value already in Dest and stores the result back into Dest.

If the WC or WCZ effect is specified, the C flag is set to the inverse of bit 31 of the source operand. For syntax 1, this is the inverse of S[31]; for syntax 2, this is the inverse of D[31].

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if it is non-zero.


