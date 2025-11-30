# Instructions: N

This section contains all PASM2 instructions beginning with the letter N.

---

## NEG {#neg}

Negate
[Math Instruction](#math-instructions) - Negate a value.

```
NEG  Dest, {#}Src  {WC|WZ|WCZ}
NEG  Dest          {WC|WZ|WCZ}
```

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

---

## NEGC {#negc}

Negate C
[Math Instruction](#math-instructions) - Negate value according to C.

```
NEGC  Dest, {#}Src  {WC|WZ|WCZ}
NEGC  Dest          {WC|WZ|WCZ}
```

**Result:** The Src or Dest value, possibly negated according to C, is stored into Dest.

- Dest is a register to receive the Src or -Src value (syntax 1), or contains the value to negate (syntax 2) according to C.
- Src is an optional register, 9-bit literal, or 32-bit augmented literal whose value (if C=0) or negated value (if C=1) is stored into Dest.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{0110100}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Sign of result}{Result = 0}{2}
\encodingrow{EEEE}{0110100}{CZ0}{DDDDDDDDD}{DDDDDDDDD}{D}{Sign of result}{Result = 0}{2}
\end{encodingtable}
```

**Related:** [NEGNC](#negnc), [NEGZ](#negz), [NEGNZ](#negnz), [NEG](#neg)

**Explanation:**

NEGC conditionally negates the value in Src (syntax 1) or Dest (syntax 2) based on the C flag state. If C = 1, the value is negated before being stored in Dest. If C = 0, the value is stored as-is (not negated). When negation is performed, it flips the value's sign; for example, 5 becomes -5, or -200 becomes 200.

This instruction is useful for conditional arithmetic operations where the sign of a value needs to be adjusted based on previous computation results captured in the C flag.

If the WC or WCZ effect is specified, the C flag is set (1) if the result is negative, or is cleared (0) if positive.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result is zero, or is cleared (0) if it is non-zero.

---

## NEGNC {#negnc}

Negate not C
[Math Instruction](#math-instructions) - Negate value according to !C.

```
NEGNC  Dest, {#}Src  {WC|WZ|WCZ}
NEGNC  Dest          {WC|WZ|WCZ}
```

**Result:** The Src or Dest value, possibly negated according to !C, is stored into Dest.

- Dest is a register to receive the Src or -Src value (syntax 1), or contains the value to negate (syntax 2) according to !C.
- Src is an optional register, 9-bit literal, or 32-bit augmented literal whose value (if !C=0) or negated value (if !C=1) is stored into Dest.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{0110101}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Sign of result}{Result = 0}{2}
\encodingrow{EEEE}{0110101}{CZ0}{DDDDDDDDD}{DDDDDDDDD}{D}{Sign of result}{Result = 0}{2}
\end{encodingtable}
```

**Related:** [NEGC](#negc), [NEGZ](#negz), [NEGNZ](#negnz), [NEG](#neg)

**Explanation:**

NEGNC conditionally negates the value in Src (syntax 1) or Dest (syntax 2) based on the inverse of the C flag state. If C = 0 (!C = 1), the value is negated before being stored in Dest. If C = 1 (!C = 0), the value is stored as-is (not negated). When negation is performed, it flips the value's sign; for example, 21 becomes -21, or -1,374 becomes 1,374.

This instruction complements NEGC, providing the opposite conditional behavior. It is useful when the logic requires negation when the C flag is clear rather than set.

If the WC or WCZ effect is specified, the C flag is set (1) if the result is negative, or is cleared (0) if positive.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result is zero, or is cleared (0) if it is non-zero.

---

## NEGNZ {#negnz}

Negate not Z
[Math Instruction](#math-instructions) - Negate value according to !Z.

```
NEGNZ  Dest, {#}Src  {WC|WZ|WCZ}
NEGNZ  Dest          {WC|WZ|WCZ}
```

**Result:** The Src or Dest value, possibly negated according to !Z, is stored into Dest.

- Dest is a register to receive the Src or -Src value (syntax 1), or contains the value to negate (syntax 2) according to !Z.
- Src is an optional register, 9-bit literal, or 32-bit augmented literal whose value (if !Z=0) or negated value (if !Z=1) is stored into Dest.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{0110111}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Sign of result}{Result = 0}{2}
\encodingrow{EEEE}{0110111}{CZ0}{DDDDDDDDD}{DDDDDDDDD}{D}{Sign of result}{Result = 0}{2}
\end{encodingtable}
```

**Related:** [NEGZ](#negz), [NEGC](#negc), [NEGNC](#negnc), [NEG](#neg)

**Explanation:**

NEGNZ conditionally negates the value in Src (syntax 1) or Dest (syntax 2) based on the inverse of the Z flag state. If Z = 0 (!Z = 1), the value is negated before being stored in Dest. If Z = 1 (!Z = 0), the value is stored as-is (not negated). When negation is performed, it flips the value's sign; for example, 193 becomes -193, or -3,062 becomes 3,062.

This instruction complements NEGZ, providing the opposite conditional behavior. It is useful when the logic requires negation when the Z flag is clear (result non-zero) rather than set.

If the WC or WCZ effect is specified, the C flag is set (1) if the result is negative, or is cleared (0) if positive.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result is zero, or is cleared (0) if it is non-zero.

---

## NEGZ {#negz}

Negate Z
[Math Instruction](#math-instructions) - Negate value according to Z.

```
NEGZ  Dest, {#}Src  {WC|WZ|WCZ}
NEGZ  Dest          {WC|WZ|WCZ}
```

**Result:** The Src or Dest value, possibly negated according to Z, is stored into Dest.

- Dest is a register to receive the Src or -Src value (syntax 1), or contains the value to negate (syntax 2) according to Z.
- Src is an optional register, 9-bit literal, or 32-bit augmented literal whose value (if Z=0) or negated value (if Z=1) is stored into Dest.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{0110110}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Sign of result}{Result = 0}{2}
\encodingrow{EEEE}{0110110}{CZ0}{DDDDDDDDD}{DDDDDDDDD}{D}{Sign of result}{Result = 0}{2}
\end{encodingtable}
```

**Related:** [NEGNZ](#negnz), [NEGC](#negc), [NEGNC](#negnc), [NEG](#neg)

**Explanation:**

NEGZ conditionally negates the value in Src (syntax 1) or Dest (syntax 2) based on the Z flag state. If Z = 1, the value is negated before being stored in Dest. If Z = 0, the value is stored as-is (not negated). When negation is performed, it flips the value's sign; for example, 526 becomes -526, or -41 becomes 41.

This instruction is useful for conditional arithmetic operations where the sign of a value needs to be adjusted based on zero-test results from previous operations.

If the WC or WCZ effect is specified, the C flag is set (1) if the result is negative, or is cleared (0) if positive.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result is zero, or is cleared (0) if it is non-zero.

---

## NIXINT1 / NIXINT2 / NIXINT3 {#nixint1}

Cancel interrupt (1, 2, or 3)
[Event Instruction](#event-instructions) - Cancel INTn interrupt.

```
NIXINT1
NIXINT2
NIXINT3
```

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

---

## NOP {#nop}

No operation
[Misc Instruction](#misc-instructions) - No operation, just elapse two cycles.

```
NOP
```

**Result:** Two clock cycles are consumed.

```{=latex}
\simpleencoding{0000}{0000000}{000}{000000000}{000000000}{---}{---}{---}{2}
```

**Related:** [WAITX](#waitx), [WAITCNT](#waitcnt)

**Explanation:**

NOP simply consumes two clock cycles without performing any operation. No registers are modified, no flags are affected, and no memory is accessed.

NOP is primarily used for timing adjustments, creating precise delays, or as a placeholder during development. It can also be used to align code for performance optimization or to fill instruction slots in pipelined operations.

---

## NOT {#not}

Not
[Logic Instruction](#logic-instructions) - Bitwise NOT a value.

```
NOT  Dest, {#}Src  {WC|WZ|WCZ}
NOT  Dest          {WC|WZ|WCZ}
```

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

---
