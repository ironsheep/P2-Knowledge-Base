# Instructions: F

This section contains all PASM2 instructions beginning with the letter F.



::: instrheader
## FBLOCK {#fblock}
Set Next FIFO Block

[hub memory Access](#hub-memory-access) - Configures the next block for FIFO wraparound operations.
:::

**FBLOCK**  *{#}Dest, {#}Src*

**Result:** The next block parameters are configured for FIFO wraparound operations.

- Dest is a register or 9-bit literal whose value specifies the block size in 64-byte units (0 = maximum size).
- Src is a register or 9-bit literal whose value specifies the block start address in hub memory.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100100 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 |


**Related:** [RDFAST](#rdfast), [WRFAST](#wrfast), [RFLONG](#rflong), [WFLONG](#wflong)

**Explanation:**

FBLOCK configures the parameters for the next hub FIFO block that will be used when the current block wraps around. This instruction is used to set up circular buffering in hub memory for streaming read and write operations.

Dest[13:0] specifies the block size in 64-byte units. A value of 0 represents the maximum block size. The block size determines how many bytes can be transferred before the FIFO wraps to the beginning of the block.

Src[19:0] specifies the starting address of the block in hub memory. This address marks where the FIFO will wrap to when it reaches the end of the current block.

FBLOCK is typically used in conjunction with RDFAST/WRFAST for setting up high-throughput data streaming between hub memory and cog/LUT memory. The block configuration takes effect when the current FIFO operation completes and wraps around.



::: instrheader
## FGE {#fge}
Force Greater or Equal

[Arithmetic Operations](#arithmetic-operations) - Forces unsigned Dest to be at least Src (minimum clamp).
:::

**FGE**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

**Operation:** if D < S then `D = S`, `C = 1`, else D unchanged, `C = 0`

**Result:** Unsigned Dest is set to unsigned Src if Dest was less than Src.

- Dest is a register containing the unsigned value to limit to a minimum of unsigned Src, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose unsigned value is the lower limit to force upon Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0011000 | CZI | DDDDDDDDD | SSSSSSSSS | limit enforced† | result == 0 | D | 2 |

† C = 1 if limit was enforced (D changed), else C = 0 (D unchanged).

**Related:** [FLE](#fle), [FGES](#fges), [FLES](#fles)

**Explanation:**

FGE sets unsigned Dest to unsigned Src if Dest is less than Src. This is a limit minimum function that prevents Dest from sinking below the value of Src. If Dest is already greater than or equal to Src, Dest remains unchanged.

If the WC or WCZ effect is specified, the C flag is set (1) if Dest was limited (Dest was less than Src and is now equal to Src), or is cleared (0) if not limited (Dest was already greater than or equal to Src).

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if the result is non-zero.

FGE is useful for clamping values to a minimum threshold, ensuring that a value never falls below a specified floor. This is commonly used in digital signal processing, graphics calculations, and boundary checking where values must stay within valid ranges.



::: instrheader
## FGES {#fges}
Force Greater or Equal Signed

[Arithmetic Operations](#arithmetic-operations) - Forces signed Dest to be at least Src (minimum clamp).
:::

**FGES**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

**Operation:** if D < S (signed) then `D = S`, `C = 1`, else D unchanged, `C = 0`

**Result:** Signed Dest is set to signed Src if Dest was less than Src.

- Dest is a register containing the signed value to limit to a minimum of signed Src, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose signed value is the lower limit to force upon Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0011010 | CZI | DDDDDDDDD | SSSSSSSSS | limit enforced† | result == 0 | D | 2 |

† C = 1 if limit was enforced (D changed), else C = 0 (D unchanged).

**Related:** [FLES](#fles), [FGE](#fge), [FLE](#fle)

**Explanation:**

FGES sets signed Dest to signed Src if Dest is less than Src. This is a limit minimum function that prevents Dest from sinking below the signed value of Src. If Dest is already greater than or equal to Src, Dest remains unchanged. The comparison and limiting are performed treating both operands as signed 32-bit values.

If the WC or WCZ effect is specified, the C flag is set (1) if Dest was limited (Dest was less than Src and is now equal to Src), or is cleared (0) if not limited (Dest was already greater than or equal to Src).

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if the result is non-zero.

FGES is the signed counterpart to FGE and is used when working with signed values that need to be clamped to a minimum threshold.


::: instrheader
## FLE {#fle}
Force Less or Equal

[Arithmetic Operations](#arithmetic-operations) - Forces unsigned Dest to be at most Src (maximum clamp).
:::

**FLE**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

**Operation:** if D > S then `D = S`, `C = 1`, else D unchanged, `C = 0`

**Result:** Unsigned Dest is set to unsigned Src if Dest was greater than Src.

- Dest is a register containing the unsigned value to limit to a maximum of unsigned Src, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose unsigned value is the upper limit to force upon Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0011001 | CZI | DDDDDDDDD | SSSSSSSSS | limit enforced† | result == 0 | D | 2 |

† C = 1 if limit was enforced (D changed), else C = 0 (D unchanged).

**Related:** [FGE](#fge), [FLES](#fles), [FGES](#fges)

**Explanation:**

FLE sets unsigned Dest to unsigned Src if Dest is greater than Src. This is a limit maximum function that prevents Dest from rising above the value of Src. If Dest is already less than or equal to Src, Dest remains unchanged.

If the WC or WCZ effect is specified, the C flag is set (1) if Dest was limited (Dest was greater than Src and is now equal to Src), or is cleared (0) if not limited (Dest was already less than or equal to Src).

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if the result is non-zero.

FLE is useful for clamping values to a maximum threshold, ensuring that a value never exceeds a specified ceiling. This is commonly used in digital signal processing, graphics calculations, and boundary checking where values must stay within valid ranges.



::: instrheader
## FLES {#fles}
Force Less or Equal Signed

[Arithmetic Operations](#arithmetic-operations) - Forces signed Dest to be at most Src (maximum clamp).
:::

**FLES**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

**Operation:** if D > S (signed) then `D = S`, `C = 1`, else D unchanged, `C = 0`

**Result:** Signed Dest is set to signed Src if Dest was greater than Src.

- Dest is a register containing the signed value to limit to a maximum of signed Src, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose signed value is the upper limit to force upon Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0011011 | CZI | DDDDDDDDD | SSSSSSSSS | limit enforced† | result == 0 | D | 2 |

† C = 1 if limit was enforced (D changed), else C = 0 (D unchanged).

**Related:** [FGES](#fges), [FLE](#fle), [FGE](#fge)

**Explanation:**

FLES sets signed Dest to signed Src if Dest is greater than Src. This is a limit maximum function that prevents Dest from rising above the signed value of Src. If Dest is already less than or equal to Src, Dest remains unchanged. The comparison and limiting are performed treating both operands as signed 32-bit values.

If the WC or WCZ effect is specified, the C flag is set (1) if Dest was limited (Dest was greater than Src and is now equal to Src), or is cleared (0) if not limited (Dest was already less than or equal to Src).

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if the result is non-zero.

FLES is the signed counterpart to FLE and is used when working with signed values that need to be clamped to a maximum threshold.


::: instrheader
## FLTC / FLTNC / FLTZ / FLTNZ {#fltc}
Float with Output Preset by Flag

[Pin I/O and smart pins](#pin-io-and-smart-pins) - Sets pins to input direction with output preset by flag state.
:::

\hypertarget{fltnc}{}\hypertarget{fltz}{}\hypertarget{fltnz}{}

**FLTC**  *{#}Dest*  **{WCZ}**\
**FLTNC**  *{#}Dest*  **{WCZ}**\
**FLTZ**  *{#}Dest*  **{WCZ}**\
**FLTNZ**  *{#}Dest*  **{WCZ}**

**Operation:** `OUT[pin range] = src`, `DIR[pin range] = 0` (FLTC src=C, FLTNC src=!C, FLTZ src=Z, FLTNZ src=!Z); `C,Z = OUT bit`

**Result:** The I/O pins are set to input direction with output preset according to flag state. Optionally sets Z to original output state.

- Dest identifies the I/O pin(s): Dest[5:0] = base pin (0-63), Dest[10:6] = additional contiguous pins.
- WCZ is an optional effect to set Z to the original output state.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001010010 | OUT bit† | OUT bit† | OUTx | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001010011 | OUT bit† | OUT bit† | OUTx | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001010100 | OUT bit† | OUT bit† | OUTx | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001010101 | OUT bit† | OUT bit† | OUTx | 2 |

† Original output state of the base pin (D[5:0]) before instruction executes.

**Related:** [FLTH](#flth), [FLTL](#fltl), [FLTNOT](#fltnot), [FLTRND](#fltrnd)

**Explanation:**

These instructions set pin(s) to input direction (floating) while pre-setting the output register based on flag state:

| Instruction | Presets output high when |
|-------------|--------------------------|
| FLTC | C = 1 |
| FLTNC | C = 0 |
| FLTZ | Z = 1 |
| FLTNZ | Z = 0 |

When the pin is later driven as output, it will immediately be at the desired level. FLTC and FLTZ preset output high when their flag is set; FLTNC and FLTNZ preset output high when their flag is clear.

If WCZ is specified, the C and Z flags are set to the original output state of the base pin.

**Pipeline Note:** The new DIRx state is not data-forwarded to subsequent instructions; only the OUTx state is forwarded (the P2 has only one forwarding path, and OUT was prioritized). Any instruction that reads or modifies DIRx should be placed at least two instructions after a FLT instruction to see the updated direction state.



::: instrheader
## FLTH {#flth}
Float High

[Pin I/O and smart pins](#pin-io-and-smart-pins) - Sets pins to input direction with output preset high.
:::

**FLTH**  *{#}Dest*  **{WCZ}**

**Operation:** `OUT[pin range] = 1`, `DIR[pin range] = 0`; `C,Z = OUT bit`

**Result:** The I/O pins described by Dest are set to the input direction and to an output level of high.

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to input direction and output level of high.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001010001 | OUT bit† | OUT bit† | OUTx | 2 |

† Original output state of the base pin (D[5:0]) before instruction executes.

**Related:** [FLTL](#fltl), [FLTC](#fltc), [FLTNC](#fltnc), [FLTZ](#fltz), [FLTNZ](#fltnz)

**Explanation:**

FLTH sets the I/O pin(s) designated by Dest to the input direction (floating) and to a high output level. All other pins are left unchanged. This pre-sets the output register so that when the pin is later driven as output, it will immediately be high.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value, which inserts an AUGD instruction prior.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) wraps within the same 32-pin group and will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are set to the original state of the OUTA/OUTB base bit identified by Dest.

**Pipeline Note:** The new DIRx state is not data-forwarded to subsequent instructions; only the OUTx state is forwarded (the P2 has only one forwarding path, and OUT was prioritized). Any instruction that reads or modifies DIRx should be placed at least two instructions after FLTH to see the updated direction state.



::: instrheader
## FLTL {#fltl}
Float Low

[Pin I/O and smart pins](#pin-io-and-smart-pins) - Sets pins to input direction with output preset low.
:::

**FLTL**  *{#}Dest*  **{WCZ}**

**Operation:** `OUT[pin range] = 0`, `DIR[pin range] = 0`; `C,Z = OUT bit`

**Result:** The I/O pins described by Dest are set to the input direction and to an output level of low.

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to input direction and output level of low.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001010000 | OUT bit† | OUT bit† | OUTx | 2 |

† Original output state of the base pin (D[5:0]) before instruction executes.

**Related:** [FLTH](#flth), [FLTC](#fltc), [FLTNC](#fltnc), [FLTZ](#fltz), [FLTNZ](#fltnz)

**Explanation:**

FLTL sets the I/O pin(s) designated by Dest to the input direction (floating) and to a low output level. All other pins are left unchanged. This pre-sets the output register so that when the pin is later driven as output, it will immediately be low.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value, which inserts an AUGD instruction prior.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) wraps within the same 32-pin group and will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are set to the original state of the OUTA/OUTB base bit identified by Dest.

**Pipeline Note:** The new DIRx state is not data-forwarded to subsequent instructions; only the OUTx state is forwarded (the P2 has only one forwarding path, and OUT was prioritized). Any instruction that reads or modifies DIRx should be placed at least two instructions after FLTL to see the updated direction state.



::: instrheader
## FLTNOT {#fltnot}
Float Not

[Pin I/O and smart pins](#pin-io-and-smart-pins) - Sets pins to input direction with output toggled.
:::

**FLTNOT**  *{#}Dest*  **{WCZ}**

**Operation:** toggle `OUT[pin range]`, `DIR[pin range] = 0`; `C,Z = OUT bit`

**Result:** The I/O pins described by Dest are set to the input direction and to their opposite output level(s).

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to the input direction and toggle to opposite output levels.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001010111 | OUT bit† | OUT bit† | OUTx | 2 |

† Original output state of the base pin (D[5:0]) before instruction executes.

**Related:** [FLTC](#fltc), [FLTNC](#fltnc), [FLTZ](#fltz), [FLTNZ](#fltnz), [FLTRND](#fltrnd)

**Explanation:**

FLTNOT sets the I/O pin(s) designated by Dest to the input direction (floating) and toggles their output level(s) to the opposite state. All other pins are left unchanged. FLTNOT achieves the same effect as two instructions: DIRL followed by OUTNOT.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value, which inserts an AUGD instruction prior.

When Dest is a register, the register's value bits \[10:0] are used as-is to form the 11-bit ID range, unless a SETQ instruction immediately precedes the FLTNOT instruction, in which case SETQ's Dest[4:0] substitutes in place of value bits\[10:6] for FLTNOT's use.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) wraps within the same 32-pin group (DIRA or DIRB and OUTA or OUTB) and will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are updated to the original state of OUTA/OUTB's base bit identified by Dest.

**Pipeline Note:** The new DIRx state is not data-forwarded to subsequent instructions; only the OUTx state is forwarded (the P2 has only one forwarding path, and OUT was prioritized). Any instruction that reads or modifies DIRx should be placed at least two instructions after FLTNOT to see the updated direction state.



::: instrheader
## FLTRND {#fltrnd}
Float Random

[Pin I/O and smart pins](#pin-io-and-smart-pins) - Sets pins to input direction with random output levels.
:::

**FLTRND**  *{#}Dest*  **{WCZ}**

**Operation:** `OUT[pin range] = RND`, `DIR[pin range] = 0`; `C,Z = OUT bit`

**Result:** The I/O pins described by Dest are set to the input direction and each output level is set randomly low or high.

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to the input direction and with output level(s) set randomly to low or high.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001010110 | OUT bit† | OUT bit† | OUTx | 2 |

† Original output state of the base pin (D[5:0]) before instruction executes.

**Related:** [FLTC](#fltc), [FLTNC](#fltnc), [FLTZ](#fltz), [FLTNZ](#fltnz), [FLTH](#flth), [FLTL](#fltl), [FLTNOT](#fltnot)

**Explanation:**

FLTRND sets the I/O pin(s) designated by Dest to the input direction and with output level(s) set randomly low and high, based on bit(s) from the Xoroshiro128** PRNG. All other pins are left unchanged. This instruction can affect one or more of the bits within the DIRA or DIRB and OUTA or OUTB registers.

FLTRND achieves the same effect as two instructions: DIRL followed by OUTRND.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value, which inserts an AUGD instruction prior.

When Dest is a register, the register's value bits \[10:0] are used as-is to form the 11-bit ID range, unless a SETQ instruction immediately precedes the FLTRND instruction, in which case SETQ's Dest[4:0] substitutes in place of value bits\[10:6] for FLTRND's use.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) wraps within the same 32-pin group (DIRA or DIRB and OUTA or OUTB) and will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are updated to the original state of OUTA/OUTB's base bit identified by Dest.

**Pipeline Note:** The new DIRx state is not data-forwarded to subsequent instructions; only the OUTx state is forwarded (the P2 has only one forwarding path, and OUT was prioritized). Any instruction that reads or modifies DIRx should be placed at least two instructions after FLTRND to see the updated direction state.


