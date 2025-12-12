# Instructions: O

This section contains all PASM2 instructions beginning with the letter O.



::: instrheader
## ONES {#ones}
Ones

[Arithmetic Operations](#arithmetic-operations) - Counts the number of high bits (1s) in a value.
:::

**ONES**  *Dest, {#}Src*  **{WC|WZ|WCZ}**\
**ONES**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** The number of high bits (1s) in Src, or Dest, is stored in Dest.

- Dest is a register where the count of high bits is stored, and optionally contains the value to check (second syntax form).
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is checked for ones.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0111101 | CZI | DDDDDDDDD | SSSSSSSSS | D | Result is odd | Result = 0 | 2 |
| EEEE | 0111101 | CZ0 | DDDDDDDDD | DDDDDDDDD | D | Result is odd | Result = 0 | 2 |


**Related:** [TEST](#test), [TESTB](#testb), [TESTBN](#testbn), [BITNOT](#bitnot)

**Explanation:**

ONES tallies the number of high bits (1s) in the specified value and stores the count in Dest. This is a population count (popcount) operation commonly used for bit manipulation and analysis.

When Src is provided in the first syntax form, ONES counts the high bits in Src and stores the result (0 to 32) in Dest. When Src is omitted in the second syntax form, ONES counts the high bits in Dest itself and replaces Dest with the count.

If the WC or WCZ effect is specified, the C flag is set (1) if the count is odd, or is cleared (0) if the count is even. This provides a parity check on the number of high bits.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero (no high bits were found), or is cleared (0) if the result is non-zero (at least one high bit exists).

ONES is useful for analyzing bit patterns, counting enabled flags, and implementing parity checks in data transmission protocols.



::: instrheader
## OR {#or}
Bitwise Or

[Arithmetic Operations](#arithmetic-operations) - Performs bitwise OR between two values.
:::

**OR**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Dest OR Src is stored in Dest.

- Dest is a register containing the value to bitwise OR with Src, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is bitwise ORed into Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0101010 | CZI | DDDDDDDDD | SSSSSSSSS | D | Parity of Result | Result = 0 | 2 |


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



::: instrheader
## OUTC / OUTNC / OUTZ / OUTNZ {#outc}
Output By Flag State

[Pin I/O and Smart Pins](#pin-io-and-smart-pins) - Sets pin output level based on flag state.
:::

**OUTC**  *{#}Dest*  **{WCZ}**\
**OUTNC**  *{#}Dest*  **{WCZ}**\
**OUTZ**  *{#}Dest*  **{WCZ}**\
**OUTNZ**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pin output level bit(s) described by Dest are set according to the flag state. Optionally sets Z to original output state.

- Dest identifies the I/O pin(s): Dest[5:0] = base pin (0-63), Dest[10:6] = additional contiguous pins.
- WCZ is an optional effect to set Z to the original output state.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001001010 | OUTx | --- | orig out | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001001011 | OUTx | --- | orig out | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001001100 | OUTx | --- | orig out | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001001101 | OUTx | --- | orig out | 2 |


**Related:** [OUTH](#outh), [OUTL](#outl), [OUTNOT](#outnot), [OUTRND](#outrnd)

**Explanation:**

These instructions set pin output level(s) based on flag state:

| Instruction | Drives high when |
|-------------|------------------|
| OUTC | C = 1 |
| OUTNC | C = 0 |
| OUTZ | Z = 1 |
| OUTNZ | Z = 0 |

OUTC and OUTZ drive high when their flag is set; OUTNC and OUTNZ drive high when their flag is clear.

If WCZ is specified, the Z flag is set to the original output state of the base pin before modification.



::: instrheader
## OUTH {#outh}
Output High

[Pin I/O and Smart Pins](#pin-io-and-smart-pins) - Sets pin output level to high (1).
:::

**OUTH**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pin output level bit(s) described by Dest are set high (1).

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set high.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001001001 | OUTx | --- | Original OUTx base bit | 2 |


**Related:** [OUTL](#outl), [OUTNOT](#outnot), [OUTC](#outc), [OUTNC](#outnc), [DIRH](#dirh)

**Explanation:**

OUTH sets the output level of the pin(s) specified by Dest to high (1), driving them to the high voltage level. All other output level bits remain unchanged.

Dest[5:0] specifies the base pin number (0-63). For controlling a single pin, only these lower 6 bits matter. For controlling a range of contiguous pins, Dest[10:6] specifies how many additional pins beyond the base should be affected (0-31, where 0 means just the base pin, 1 means base plus one additional pin, etc.).

A 9-bit literal Dest can express the base pin (bits [5:0]) and up to 7 additional pins (bits [8:6]). To specify a wider range, use the augmented literal prefix (##Dest) to provide an 11-bit value, which allows controlling up to 32 contiguous pins.

If the WCZ effect is specified, the Z flag is set to the original state of the output level bit for the base pin, before the instruction executes. The C flag is not affected by this instruction.

OUTH is commonly used to turn on LEDs, assert control signals, or drive pins high for any digital output purpose. For the output level change to affect the actual pin voltage, the pin must also be configured as an output using the direction control instructions.



::: instrheader
## OUTL {#outl}
Output Low

[Pin I/O and Smart Pins](#pin-io-and-smart-pins) - Sets pin output level to low (0).
:::

**OUTL**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pin output level bit(s) described by Dest are set low (0).

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set low.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001001000 | OUTx | --- | Original OUTx base bit | 2 |


**Related:** [OUTH](#outh), [OUTNOT](#outnot), [OUTC](#outc), [OUTNC](#outnc), [DIRL](#dirl)

**Explanation:**

OUTL sets the output level of the pin(s) specified by Dest to low (0), driving them to the low voltage level (typically ground). All other output level bits remain unchanged.

Dest[5:0] specifies the base pin number (0-63). For controlling a single pin, only these lower 6 bits matter. For controlling a range of contiguous pins, Dest[10:6] specifies how many additional pins beyond the base should be affected (0-31, where 0 means just the base pin, 1 means base plus one additional pin, etc.).

A 9-bit literal Dest can express the base pin (bits [5:0]) and up to 7 additional pins (bits [8:6]). To specify a wider range, use the augmented literal prefix (##Dest) to provide an 11-bit value, which allows controlling up to 32 contiguous pins.

If the WCZ effect is specified, the Z flag is set to the original state of the output level bit for the base pin, before the instruction executes. The C flag is not affected by this instruction.

OUTL is commonly used to turn off LEDs, de-assert control signals, or drive pins low for any digital output purpose. For the output level change to affect the actual pin voltage, the pin must also be configured as an output using the direction control instructions.



::: instrheader
## OUTNOT {#outnot}
Output Not (Toggle)

[Pin I/O and Smart Pins](#pin-io-and-smart-pins) - Toggles pin output level to opposite state.
:::

**OUTNOT**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pin output level bit(s) described by Dest are toggled to their opposite state(s).

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to toggle.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001001111 | OUTx | --- | Original OUTx base bit | 2 |


**Related:** [OUTH](#outh), [OUTL](#outl), [OUTRND](#outrnd), [NOT](#not), [DRVNOT](#drvnot)

**Explanation:**

OUTNOT toggles the output level of the pin(s) specified by Dest to their opposite state. Pins that were high (1) become low (0), and pins that were low become high. All other output level bits remain unchanged.

Dest[5:0] specifies the base pin number (0-63). For controlling a single pin, only these lower 6 bits matter. For controlling a range of contiguous pins, Dest[10:6] specifies how many additional pins beyond the base should be affected (0-31, where 0 means just the base pin, 1 means base plus one additional pin, etc.).

A 9-bit literal Dest can express the base pin (bits [5:0]) and up to 7 additional pins (bits [8:6]). To specify a wider range, use the augmented literal prefix (##Dest) to provide an 11-bit value, which allows controlling up to 32 contiguous pins.

If the WCZ effect is specified, the Z flag is set to the original state of the output level bit for the base pin, before the instruction executes. The C flag is not affected by this instruction.

OUTNOT is commonly used for blinking LEDs, generating clock signals, or toggling any output that needs to alternate states. It is particularly efficient for creating square waves or implementing state machines that alternate between two states.



::: instrheader
## OUTRND {#outrnd}
Output Random

[Pin I/O and Smart Pins](#pin-io-and-smart-pins) - Sets pin output level to random state from PRNG.
:::

**OUTRND**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pin output level bit(s) described by Dest are each set randomly to low or high.

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to random output levels.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001001110 | Original OUTx base bit | Original OUTx base bit | OUTx | 2 |


**Related:** [OUTC](#outc), [OUTNC](#outnc), [OUTZ](#outz), [OUTNZ](#outnz), [OUTH](#outh), [OUTL](#outl), [OUTNOT](#outnot)

**Explanation:**

OUTRND sets the output level of the pin(s) specified by Dest to random low and high states, using bits from the hardware Xoroshiro128** pseudo-random number generator (PRNG). Each affected pin is independently set to either low (0) or high (1) based on successive bits from the PRNG. All other output level bits remain unchanged.

Dest[5:0] specifies the base pin number (0-63). For controlling a single pin, only this lower 6-bit value matters. For controlling a range of contiguous pins, Dest[10:6] specifies how many additional pins beyond the base should be affected (0-31, where 0 means just the base pin, 1 means base plus one additional pin, etc.).

A 9-bit literal Dest can express the base pin (bits [5:0]) and up to 7 additional pins (bits [8:6], allowing control of 1 to 8 contiguous pins). To specify a wider range, use the augmented literal prefix (##Dest) to provide an 11-bit value, which allows controlling up to 32 contiguous pins.

When Dest is a register, the register's bits [10:0] are used directly to form the 11-bit pin range specification. However, if a SETQ instruction immediately precedes OUTRND, then SETQ's Dest[4:0] is substituted for the register's bits [10:6], allowing dynamic control of the pin range.

If the WCZ effect is specified, both the C and Z flags are set to the original state of the output level bit for the base pin, before the instruction executes.

OUTRND is useful for generating random visual patterns on LEDs, creating noise signals for testing or audio applications, or implementing randomized control sequences. The quality of randomness depends on proper initialization of the PRNG using the SETRAND instruction.




