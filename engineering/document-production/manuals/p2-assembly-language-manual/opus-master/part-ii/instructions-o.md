# Instructions: O

This section contains all PASM2 instructions beginning with the letter O.

---

## ONES {#ones}

Ones
[Math Instruction](#math-instructions) - Count the number of high bits (1s) in a value.

```
ONES  Dest, {#}Src  {WC|WZ|WCZ}
ONES  Dest          {WC|WZ|WCZ}
```

**Result:** The number of high bits (1s) in Src, or Dest, is stored in Dest.

- Dest is a register where the count of high bits is stored, and optionally contains the value to check (second syntax form).
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is checked for ones.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{0111101}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Result is odd}{Result = 0}{2}
\encodingrow{EEEE}{0111101}{CZ0}{DDDDDDDDD}{DDDDDDDDD}{D}{Result is odd}{Result = 0}{2}
\end{encodingtable}
```

**Related:** [TEST](#test), [TESTB](#testb), [TESTBN](#testbn), [BITNOT](#bitnot)

**Explanation:**

ONES tallies the number of high bits (1s) in the specified value and stores the count in Dest. This is a population count (popcount) operation commonly used for bit manipulation and analysis.

When Src is provided in the first syntax form, ONES counts the high bits in Src and stores the result (0 to 32) in Dest. When Src is omitted in the second syntax form, ONES counts the high bits in Dest itself and replaces Dest with the count.

If the WC or WCZ effect is specified, the C flag is set (1) if the count is odd, or is cleared (0) if the count is even. This provides a parity check on the number of high bits.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero (no high bits were found), or is cleared (0) if the result is non-zero (at least one high bit exists).

ONES is useful for analyzing bit patterns, counting enabled flags, and implementing parity checks in data transmission protocols.

---

## OR {#or}

Or
[Logic Instruction](#logic-instructions) - Perform bitwise OR operation.

```
OR  Dest, {#}Src  {WC|WZ|WCZ}
```

**Result:** Dest OR Src is stored in Dest.

- Dest is a register containing the value to bitwise OR with Src, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is bitwise ORed into Dest.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0101010}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Parity of Result}{Result = 0}{2}
```

**Related:** [AND](#and), [XOR](#xor), [ANDN](#andn), [NOT](#not)

**Explanation:**

OR performs a bitwise OR operation between the values in Dest and Src, storing the result in Dest. Each bit position in the result is set (1) if the corresponding bit in either Dest or Src (or both) is set, and is cleared (0) only if both corresponding bits are cleared.

The bitwise OR operation follows this truth table for each bit position:

```
Dest  Src   Result
  0    0      0
  0    1      1
  1    0      1
  1    1      1
```

If the WC or WCZ effect is specified, the C flag is set (1) if the result contains an odd number of high bits, or is cleared (0) if it contains an even number of high bits. This provides a parity indication of the result.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if the result is non-zero. Note that the result can only be zero if both Dest and Src were zero.

OR is commonly used for setting specific bits in a value, combining bit masks, and implementing logical operations in algorithms.

---

## OUTC {#outc}

Output if C
[I/O Pin Instruction](#io-pin-instructions) - Set pin output level according to C flag state.

```
OUTC  {#}Dest  {WCZ}
```

**Result:** The I/O pin output level bit(s) described by Dest are set to low/high according to C flag state.

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) for which output levels are to be set.
- WCZ is an optional effect to update flags.

```{=latex}
\simpleencoding{EEEE}{1101011}{CZL}{DDDDDDDDD}{001001010}{OUTx}{---}{Original OUTx base bit}{2}
```

**Related:** [OUTNC](#outnc), [OUTZ](#outz), [OUTNZ](#outnz), [OUTH](#outh), [OUTL](#outl)

**Explanation:**

OUTC sets the output level of the pin(s) specified by Dest to match the state of the C flag. If C is set (1), the pin(s) are driven high. If C is clear (0), the pin(s) are driven low. All other output level bits remain unchanged.

Dest[5:0] specifies the base pin number (0-63). For controlling a single pin, only these lower 6 bits matter. For controlling a range of contiguous pins, Dest[10:6] specifies how many additional pins beyond the base should be affected (0-31, where 0 means just the base pin, 1 means base plus one additional pin, etc.).

A 9-bit literal Dest can express the base pin (bits [5:0]) and up to 7 additional pins (bits [8:6]). To specify a wider range, use the augmented literal prefix (##Dest) to provide an 11-bit value, which allows controlling up to 32 contiguous pins.

If the WCZ effect is specified, the Z flag is set to the original state of the output level bit for the base pin, before the instruction executes. The C flag is not affected by this instruction.

OUTC is useful for reflecting the result of a previous comparison or calculation directly onto an output pin, such as driving an LED to indicate a status condition.

---

## OUTH {#outh}

Output high
[I/O Pin Instruction](#io-pin-instructions) - Set pin output level to high.

```
OUTH  {#}Dest  {WCZ}
```

**Result:** The I/O pin output level bit(s) described by Dest are set high (1).

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set high.
- WCZ is an optional effect to update flags.

```{=latex}
\simpleencoding{EEEE}{1101011}{CZL}{DDDDDDDDD}{001001001}{OUTx}{---}{Original OUTx base bit}{2}
```

**Related:** [OUTL](#outl), [OUTNOT](#outnot), [OUTC](#outc), [OUTNC](#outnc), [DIRH](#dirh)

**Explanation:**

OUTH sets the output level of the pin(s) specified by Dest to high (1), driving them to the high voltage level. All other output level bits remain unchanged.

Dest[5:0] specifies the base pin number (0-63). For controlling a single pin, only these lower 6 bits matter. For controlling a range of contiguous pins, Dest[10:6] specifies how many additional pins beyond the base should be affected (0-31, where 0 means just the base pin, 1 means base plus one additional pin, etc.).

A 9-bit literal Dest can express the base pin (bits [5:0]) and up to 7 additional pins (bits [8:6]). To specify a wider range, use the augmented literal prefix (##Dest) to provide an 11-bit value, which allows controlling up to 32 contiguous pins.

If the WCZ effect is specified, the Z flag is set to the original state of the output level bit for the base pin, before the instruction executes. The C flag is not affected by this instruction.

OUTH is commonly used to turn on LEDs, assert control signals, or drive pins high for any digital output purpose. For the output level change to affect the actual pin voltage, the pin must also be configured as an output using the direction control instructions.

---

## OUTL {#outl}

Output low
[I/O Pin Instruction](#io-pin-instructions) - Set pin output level to low.

```
OUTL  {#}Dest  {WCZ}
```

**Result:** The I/O pin output level bit(s) described by Dest are set low (0).

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set low.
- WCZ is an optional effect to update flags.

```{=latex}
\simpleencoding{EEEE}{1101011}{CZL}{DDDDDDDDD}{001001000}{OUTx}{---}{Original OUTx base bit}{2}
```

**Related:** [OUTH](#outh), [OUTNOT](#outnot), [OUTC](#outc), [OUTNC](#outnc), [DIRL](#dirl)

**Explanation:**

OUTL sets the output level of the pin(s) specified by Dest to low (0), driving them to the low voltage level (typically ground). All other output level bits remain unchanged.

Dest[5:0] specifies the base pin number (0-63). For controlling a single pin, only these lower 6 bits matter. For controlling a range of contiguous pins, Dest[10:6] specifies how many additional pins beyond the base should be affected (0-31, where 0 means just the base pin, 1 means base plus one additional pin, etc.).

A 9-bit literal Dest can express the base pin (bits [5:0]) and up to 7 additional pins (bits [8:6]). To specify a wider range, use the augmented literal prefix (##Dest) to provide an 11-bit value, which allows controlling up to 32 contiguous pins.

If the WCZ effect is specified, the Z flag is set to the original state of the output level bit for the base pin, before the instruction executes. The C flag is not affected by this instruction.

OUTL is commonly used to turn off LEDs, de-assert control signals, or drive pins low for any digital output purpose. For the output level change to affect the actual pin voltage, the pin must also be configured as an output using the direction control instructions.

---

## OUTNC {#outnc}

Output if not C
[I/O Pin Instruction](#io-pin-instructions) - Set pin output level according to inverted C flag state.

```
OUTNC  {#}Dest  {WCZ}
```

**Result:** The I/O pin output level bit(s) described by Dest are set to low/high according to inverted C flag state (!C).

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) for which output levels are to be set.
- WCZ is an optional effect to update flags.

```{=latex}
\simpleencoding{EEEE}{1101011}{CZL}{DDDDDDDDD}{001001011}{OUTx}{---}{Original OUTx base bit}{2}
```

**Related:** [OUTC](#outc), [OUTZ](#outz), [OUTNZ](#outnz), [OUTH](#outh), [OUTL](#outl)

**Explanation:**

OUTNC sets the output level of the pin(s) specified by Dest to match the inverse state of the C flag. If C is clear (0), the pin(s) are driven high. If C is set (1), the pin(s) are driven low. All other output level bits remain unchanged.

Dest[5:0] specifies the base pin number (0-63). For controlling a single pin, only these lower 6 bits matter. For controlling a range of contiguous pins, Dest[10:6] specifies how many additional pins beyond the base should be affected (0-31, where 0 means just the base pin, 1 means base plus one additional pin, etc.).

A 9-bit literal Dest can express the base pin (bits [5:0]) and up to 7 additional pins (bits [8:6]). To specify a wider range, use the augmented literal prefix (##Dest) to provide an 11-bit value, which allows controlling up to 32 contiguous pins.

If the WCZ effect is specified, the Z flag is set to the original state of the output level bit for the base pin, before the instruction executes. The C flag is not affected by this instruction.

OUTNC is useful for reflecting the inverse of a comparison or calculation result onto an output pin, such as driving an active-low signal or implementing inverted logic.

---

## OUTNOT {#outnot}

Output not (toggle)
[I/O Pin Instruction](#io-pin-instructions) - Toggle pin output level to opposite state.

```
OUTNOT  {#}Dest  {WCZ}
```

**Result:** The I/O pin output level bit(s) described by Dest are toggled to their opposite state(s).

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to toggle.
- WCZ is an optional effect to update flags.

```{=latex}
\simpleencoding{EEEE}{1101011}{CZL}{DDDDDDDDD}{001001111}{OUTx}{---}{Original OUTx base bit}{2}
```

**Related:** [OUTH](#outh), [OUTL](#outl), [OUTRND](#outrnd), [NOT](#not), [DRVNOT](#drvnot)

**Explanation:**

OUTNOT toggles the output level of the pin(s) specified by Dest to their opposite state. Pins that were high (1) become low (0), and pins that were low become high. All other output level bits remain unchanged.

Dest[5:0] specifies the base pin number (0-63). For controlling a single pin, only these lower 6 bits matter. For controlling a range of contiguous pins, Dest[10:6] specifies how many additional pins beyond the base should be affected (0-31, where 0 means just the base pin, 1 means base plus one additional pin, etc.).

A 9-bit literal Dest can express the base pin (bits [5:0]) and up to 7 additional pins (bits [8:6]). To specify a wider range, use the augmented literal prefix (##Dest) to provide an 11-bit value, which allows controlling up to 32 contiguous pins.

If the WCZ effect is specified, the Z flag is set to the original state of the output level bit for the base pin, before the instruction executes. The C flag is not affected by this instruction.

OUTNOT is commonly used for blinking LEDs, generating clock signals, or toggling any output that needs to alternate states. It is particularly efficient for creating square waves or implementing state machines that alternate between two states.

---

## OUTNZ {#outnz}

Output if not Z
[I/O Pin Instruction](#io-pin-instructions) - Set pin output level according to inverted Z flag state.

```
OUTNZ  {#}Dest  {WCZ}
```

**Result:** The I/O pin output level bit(s) described by Dest are set to low/high according to inverted Z flag state (!Z).

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) for which output levels are to be set.
- WCZ is an optional effect to update flags.

```{=latex}
\simpleencoding{EEEE}{1101011}{CZL}{DDDDDDDDD}{001001101}{OUTx}{---}{Original OUTx base bit}{2}
```

**Related:** [OUTZ](#outz), [OUTC](#outc), [OUTNC](#outnc), [OUTH](#outh), [OUTL](#outl)

**Explanation:**

OUTNZ sets the output level of the pin(s) specified by Dest to match the inverse state of the Z flag. If Z is clear (0), the pin(s) are driven high. If Z is set (1), the pin(s) are driven low. All other output level bits remain unchanged.

Dest[5:0] specifies the base pin number (0-63). For controlling a single pin, only these lower 6 bits matter. For controlling a range of contiguous pins, Dest[10:6] specifies how many additional pins beyond the base should be affected (0-31, where 0 means just the base pin, 1 means base plus one additional pin, etc.).

A 9-bit literal Dest can express the base pin (bits [5:0]) and up to 7 additional pins (bits [8:6]). To specify a wider range, use the augmented literal prefix (##Dest) to provide an 11-bit value, which allows controlling up to 32 contiguous pins.

If the WCZ effect is specified, the Z flag is set to the original state of the output level bit for the base pin, before the instruction executes. The C flag is not affected by this instruction.

OUTNZ is useful for reflecting the non-zero result of a previous operation onto an output pin, such as indicating when a counter or accumulator holds a non-zero value, or implementing active-low logic for zero detection.

---

## OUTRND {#outrnd}

Output random
[I/O Pin Instruction](#io-pin-instructions) - Set pin output level(s) to random values.

```
OUTRND  {#}Dest  {WCZ}
```

**Result:** The I/O pin output level bit(s) described by Dest are each set randomly to low or high.

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to random output levels.
- WCZ is an optional effect to update flags.

```{=latex}
\simpleencoding{EEEE}{1101011}{CZL}{DDDDDDDDD}{001001110}{OUTx}{Original OUTx base bit}{Original OUTx base bit}{2}
```

**Related:** [OUTC](#outc), [OUTNC](#outnc), [OUTZ](#outz), [OUTNZ](#outnz), [OUTH](#outh), [OUTL](#outl), [OUTNOT](#outnot)

**Explanation:**

OUTRND sets the output level of the pin(s) specified by Dest to random low and high states, using bits from the hardware Xoroshiro128** pseudo-random number generator (PRNG). Each affected pin is independently set to either low (0) or high (1) based on successive bits from the PRNG. All other output level bits remain unchanged.

Dest[5:0] specifies the base pin number (0-63). For controlling a single pin, only this lower 6-bit value matters. For controlling a range of contiguous pins, Dest[10:6] specifies how many additional pins beyond the base should be affected (0-31, where 0 means just the base pin, 1 means base plus one additional pin, etc.).

A 9-bit literal Dest can express the base pin (bits [5:0]) and up to 7 additional pins (bits [8:6], allowing control of 1 to 8 contiguous pins). To specify a wider range, use the augmented literal prefix (##Dest) to provide an 11-bit value, which allows controlling up to 32 contiguous pins.

When Dest is a register, the register's bits [10:0] are used directly to form the 11-bit pin range specification. However, if a SETQ instruction immediately precedes OUTRND, then SETQ's Dest[4:0] is substituted for the register's bits [10:6], allowing dynamic control of the pin range.

If the WCZ effect is specified, both the C and Z flags are set to the original state of the output level bit for the base pin, before the instruction executes.

OUTRND is useful for generating random visual patterns on LEDs, creating noise signals for testing or audio applications, or implementing randomized control sequences. The quality of randomness depends on proper initialization of the PRNG using the SETRAND instruction.

---

## OUTZ {#outz}

Output if Z
[I/O Pin Instruction](#io-pin-instructions) - Set pin output level according to Z flag state.

```
OUTZ  {#}Dest  {WCZ}
```

**Result:** The I/O pin output level bit(s) described by Dest are set to low/high according to Z flag state.

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) for which output levels are to be set.
- WCZ is an optional effect to update flags.

```{=latex}
\simpleencoding{EEEE}{1101011}{CZL}{DDDDDDDDD}{001001100}{OUTx}{---}{Original OUTx base bit}{2}
```

**Related:** [OUTNZ](#outnz), [OUTC](#outc), [OUTNC](#outnc), [OUTH](#outh), [OUTL](#outl)

**Explanation:**

OUTZ sets the output level of the pin(s) specified by Dest to match the state of the Z flag. If Z is set (1), the pin(s) are driven high. If Z is clear (0), the pin(s) are driven low. All other output level bits remain unchanged.

Dest[5:0] specifies the base pin number (0-63). For controlling a single pin, only these lower 6 bits matter. For controlling a range of contiguous pins, Dest[10:6] specifies how many additional pins beyond the base should be affected (0-31, where 0 means just the base pin, 1 means base plus one additional pin, etc.).

A 9-bit literal Dest can express the base pin (bits [5:0]) and up to 7 additional pins (bits [8:6]). To specify a wider range, use the augmented literal prefix (##Dest) to provide an 11-bit value, which allows controlling up to 32 contiguous pins.

If the WCZ effect is specified, the Z flag is set to the original state of the output level bit for the base pin, before the instruction executes. The C flag is not affected by this instruction.

OUTZ is useful for reflecting the zero result of a previous operation onto an output pin, such as indicating when a counter reaches zero, or implementing status LEDs that activate based on equality comparisons.

---
