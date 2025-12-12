# Instructions: S

This section contains all PASM2 instructions beginning with the letter S.



::: instrheader
## SAL {#sal}
Shift Arithmetic Left

[Arithmetic Operations](#arithmetic-operations) - Shifts bits left, extending the original LSB into new rightmost bits.
:::

**SAL**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are shifted left by Src bits, extending Dest[0] into new rightmost bits.

- Dest is a register containing the value to arithmetically left shift.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to shift.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0000111 | CZI | DDDDDDDDD | SSSSSSSSS | D | Last bit out\textsuperscript{1} | Result = 0 | 2 |


**Related:** [SAR](#sar), [SHL](#shl), [SHR](#shr)

**Explanation:**

SAL shifts the destination's binary value left by the source number of places (0-31 bits) and sets the new LSBs to that of the original Dest[0]. SAL is the complement of SAR for bit streams but not for math operations. For swift 32-bit integer multiplication by a power-of-two, use SHL instead.

::: pasm2
        SAL     data, #4       ' Shift left 4 bits, extending LSB
:::



::: instrheader
## SAR {#sar}
Shift Arithmetic Right

[Arithmetic Operations](#arithmetic-operations) - Shifts bits right, preserving the sign bit for signed division.
:::

**SAR**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are shifted right by Src bits, extending Dest[31] (the sign bit) into new leftmost bits.

- Dest is a register containing the value to arithmetically right shift.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to shift.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0000110 | CZI | DDDDDDDDD | SSSSSSSSS | D | Last bit out\textsuperscript{1} | Result = 0 | 2 |


**Related:** [SAL](#sal), [SHL](#shl), [SHR](#shr)

**Explanation:**

SAR shifts the destination's binary value right by the source number of places (0-31 bits) and sets the new MSBs to that of the original Dest[31], preserving the sign of a signed integer. This is useful for bit stream manipulation and for swift division. It is similar to SHR for swift division by a power-of-two, but is safe for both signed and unsigned integers.

::: pasm2
        SAR     value, #3      ' Divide signed value by 8
:::



::: instrheader
## SCA {#sca}
Scale

[Arithmetic Operations](#arithmetic-operations) - Scales unsigned 16-bit values by multiplying and right-shifting.
:::

**SCA**  *Dest, {#}Src*  **{WZ}**

---

**Result:** The upper 16 bits of the unsigned product from the 16-bit Dest and Src multiplication is substituted as the next instruction's S value.

- Dest is a register containing the 16-bit value to multiply with Src.
- Src is a register, 9-bit literal, or 16-bit augmented literal to multiply with Dest.
- WZ is an optional effect to update the Z flag.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010001 | 0ZI | DDDDDDDDD | SSSSSSSSS | --- | --- | Product = 0 | 2 |


**Related:** [SCAS](#scas)

**Explanation:**

SCA multiplies the lower 16 bits of each of Dest and Src together, right shifts the 32-bit product by 16 (to scale down the result), and substitutes this value as the next instruction's S value. This is useful for creating scaled unsigned 16-bit values for subsequent operations.

::: pasm2
        SCA     factor, #$8000  ' Scale by 0.5 (32768/65536)
        ADD     result, #0      ' Add scaled value
:::



::: instrheader
## SCAS {#scas}
Scale Signed

[Arithmetic Operations](#arithmetic-operations) - Scales signed 16-bit values by multiplying and right-shifting.
:::

**SCAS**  *Dest, {#}Src*  **{WZ}**

---

**Result:** The upper 18 bits of the signed product from the 16-bit Dest and Src multiplication is substituted as the next instruction's S value.

- Dest is a register containing the signed 16-bit value to multiply with Src.
- Src is a register, 9-bit literal, or signed 16-bit augmented literal to multiply with Dest.
- WZ is an optional effect to update the Z flag.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010001 | 1ZI | DDDDDDDDD | SSSSSSSSS | --- | --- | Result = 0 | 2 |


**Related:** [SCA](#sca)

**Explanation:**

SCAS multiplies the lower signed 16 bits of each of Dest and Src together, right shifts the 32-bit product by 14 (to scale down the result), and substitutes this value as the next instruction's S value. This is useful for creating scaled signed values for subsequent operations.



::: instrheader
## SETBYTE {#setbyte}
Set Byte

[Arithmetic Operations](#arithmetic-operations) - Writes an 8-bit value to a specific byte position within a register.
:::

**SETBYTE**  *Dest, {#}Src, #N*\
**SETBYTE**  *{#}Src*

---

**Result:** Src[7:0] is written to byte N (0-3) of Dest, or to another register byte described by prior ALTSB instruction.

- Dest is a register in which to modify a byte.
- Src is a register or 8-bit literal whose bits [7:0] will be stored in the designated location.
- N is a 2-bit literal (0-3) identifying the byte of Dest to modify.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1000110 | NNI | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |
| EEEE | 1000110 | 00I | 000000000 | SSSSSSSSS | D* | --- | --- | 2 |


*Dest and byte ID specified by prior ALTSB instruction.

**Related:** [ALTSB](#altsb), [SETNIB](#setnib), [SETWORD](#setword), [GETBYTE](#getbyte)

**Explanation:**

SETBYTE stores Src[7:0] into the byte identified by N within Dest, or the byte and register described by a prior ALTSB instruction. No other bits are modified. N (0-3) identifies a value's individual bytes by position in least-significant byte order. The second syntax is intended for use after an ALTSB instruction in a loop to iteratively affect a series of byte values within contiguous long registers.

::: pasm2
        SETBYTE data, #$FF, #2  ' Set byte 2 of data to $FF
:::



::: instrheader
## SETCFRQ {#setcfrq}
Set Colorspace Converter Frequency

[Color Space and Pixel Operations](#color-space-and-pixel-operations) - Configures the frequency parameter for colorspace conversion hardware.
:::

**SETCFRQ**  *{#}Dest*

---

**Result:** The colorspace converter CFRQ parameter is set to Dest[31:0].

- Dest is a register or literal value (0-511) to set as CFRQ parameter.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000111011 | --- | --- | --- | 2 |


**Related:** [SETCI](#setci), [SETCMOD](#setcmod), [SETCQ](#setcq), [SETCY](#setcy)

**Explanation:**

Sets the colorspace converter CFRQ parameter to the value in Dest. This instruction configures the frequency parameter for the colorspace conversion hardware.



::: instrheader
## SETCI {#setci}
Set Colorspace Converter CI

[Color Space and Pixel Operations](#color-space-and-pixel-operations) - Configures the CI parameter for colorspace conversion hardware.
:::

**SETCI**  *{#}Dest*

---

**Result:** The colorspace converter CI parameter is set to Dest[31:0].

- Dest is a register or literal value (0-511) to set as CI parameter.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000111001 | --- | --- | --- | 2 |


**Related:** [SETCFRQ](#setcfrq), [SETCMOD](#setcmod), [SETCQ](#setcq), [SETCY](#setcy)

**Explanation:**

Sets the colorspace converter CI parameter to the value in Dest. This instruction configures the CI parameter for the colorspace conversion hardware.



::: instrheader
## SETCMOD {#setcmod}
Set Colorspace Converter Mode

[Color Space and Pixel Operations](#color-space-and-pixel-operations) - Configures the mode parameter for colorspace conversion hardware.
:::

**SETCMOD**  *{#}Dest*

---

**Result:** The colorspace converter CMOD parameter is set to Dest[8:0].

- Dest is a register or literal value (0-511) to set as CMOD parameter.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000111100 | --- | --- | --- | 2 |


**Related:** [SETCFRQ](#setcfrq), [SETCI](#setci), [SETCQ](#setcq), [SETCY](#setcy)

**Explanation:**

Sets the colorspace converter CMOD parameter to Dest[8:0]. This instruction configures the mode parameter for the colorspace conversion hardware.



::: instrheader
## SETCQ {#setcq}
Set Colorspace Converter CQ

[Color Space and Pixel Operations](#color-space-and-pixel-operations) - Configures the CQ parameter for colorspace conversion hardware.
:::

**SETCQ**  *{#}Dest*

---

**Result:** The colorspace converter CQ parameter is set to Dest[31:0].

- Dest is a register or literal value (0-511) to set as CQ parameter.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000111010 | --- | --- | --- | 2 |


**Related:** [SETCFRQ](#setcfrq), [SETCI](#setci), [SETCMOD](#setcmod), [SETCY](#setcy)

**Explanation:**

Sets the colorspace converter CQ parameter to the value in Dest. This instruction configures the CQ parameter for the colorspace conversion hardware.



::: instrheader
## SETCY {#setcy}
Set Colorspace Converter CY

[Color Space and Pixel Operations](#color-space-and-pixel-operations) - Configures the CY parameter for colorspace conversion hardware.
:::

**SETCY**  *{#}Dest*

---

**Result:** The colorspace converter CY parameter is set to Dest[31:0].

- Dest is a register or literal value (0-511) to set as CY parameter.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000111000 | --- | --- | --- | 2 |


**Related:** [SETCFRQ](#setcfrq), [SETCI](#setci), [SETCMOD](#setcmod), [SETCQ](#setcq)

**Explanation:**

Sets the colorspace converter CY parameter to the value in Dest. This instruction configures the CY parameter for the colorspace conversion hardware.



::: instrheader
## SETD {#setd}
Set Destination Field

[Register Indirection](#register-indirection) - Sets the D field of a template for use with ALTI instruction.
:::

**SETD**  *Dest, {#}Src*

---

**Result:** The D field [17:9] of template Dest is set to Src[8:0].

- Dest is a register whose 32-bit value is a template for use with an ALTI instruction.
- Src is a register or 9-bit literal whose value (Src[8:0]) is copied to the D field of Dest.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001101 | 10I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |


**Related:** [SETS](#sets), [SETR](#setr), [ALTI](#alti)

**Explanation:**

SETD copies Src[8:0] to the D field of the template Dest to be used with an ALTI instruction. Bits outside the D field remain unaffected. The D field holds the address of a register (or sometimes a literal value) for the instruction to use as its destination value, and usually as its result destination, during its execution.

SETD can also be used in self-modifying register RAM code. Unlike with ALTx instructions, when used this way, field value modification occurs in the program code itself (not the instruction pipeline); code is altered, values persist. Due to the instruction pipeline nature, after modifying a code register, it is necessary to elapse at least two instructions before executing the modified register.



::: instrheader
## SETDACS {#setdacs}
Set DACs

[Pin I/O and Smart Pins](#pin-io-and-smart-pins) - Sets all four DAC channels simultaneously from a single register.
:::

**SETDACS**  *{#}Dest*

---

**Result:** DAC3 = Dest[31:24], DAC2 = Dest[23:16], DAC1 = Dest[15:8], DAC0 = Dest[7:0].

- Dest is a register or literal value (0-511) containing four 8-bit DAC values.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000011100 | --- | --- | --- | 2 |


**Explanation:**

Sets all four DAC channels simultaneously from the four bytes in Dest. DAC3 receives bits [31:24], DAC2 receives bits [23:16], DAC1 receives bits [15:8], and DAC0 receives bits [7:0].



::: instrheader
## SETINT1 / SETINT2 / SETINT3 {#setint1}
Set Interrupt Source (1, 2, Or 3)

[Interrupts](#interrupts) - Configures which event triggers the specified interrupt level.
:::

\hypertarget{setint2}{}\hypertarget{setint3}{}

**SETINT1**  *{#}Dest*\
**SETINT2**  *{#}Dest*\
**SETINT3**  *{#}Dest*

---

**Result:** The specified interrupt source (INT1, INT2, or INT3) is set to Dest[3:0].

- Dest is a register or literal value (0-511) containing interrupt source in bits [3:0].


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000100101 | --- | --- | --- | 2 |
| EEEE | 1101011 | 00L | DDDDDDDDD | 000100110 | --- | --- | --- | 2 |
| EEEE | 1101011 | 00L | DDDDDDDDD | 000100111 | --- | --- | --- | 2 |


**Related:** [NIXINT1/2/3](#nixint1), [TRGINT1/2/3](#trgint1), [RETI0/1/2/3](#reti0), [RESI0/1/2/3](#resi0)

**Explanation:**

SETINT1, SETINT2, and SETINT3 configure which event will trigger their respective interrupt levels. The interrupt source is specified in Dest[3:0].

The P2 provides three configurable interrupt levels (INT1-INT3), each of which can be independently configured to respond to different event sources.



::: instrheader
## SETLUTS {#setluts}
Set LUT Sharing

[Lookup Table](#lookup-table) - Enables or disables LUT sharing between adjacent cog pairs.
:::

**SETLUTS**  *{#}Dest*

---

**Result:** If Dest[0] = 1, LUT sharing is enabled where LUT writes within the adjacent odd/even companion cog are copied to this cog's LUT.

- Dest is a register or literal value (0-511) with enable bit in Dest[0].


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000110111 | --- | --- | --- | 2 |


**Related:** [RDLUT](#rdlut), [WRLUT](#wrlut)

**Explanation:**

Enables or disables LUT sharing based on Dest[0]. When enabled (Dest[0] = 1), LUT writes within the adjacent odd/even companion cog are automatically copied to this cog's LUT, allowing cogs to share lookup table data.



::: instrheader
## SETNIB {#setnib}
Set Nibble

[Arithmetic Operations](#arithmetic-operations) - Writes a 4-bit value to a specific nibble position within a register.
:::

**SETNIB**  *Dest, {#}Src, #N*\
**SETNIB**  *{#}Src*

---

**Result:** Src[3:0] is written to nibble N (0-7) of Dest, or to another register nibble described by prior ALTSN instruction.

- Dest is a register in which to modify a nibble.
- Src is a register or 4-bit literal whose bits [3:0] will be stored in the designated location.
- N is a 3-bit literal (0-7) identifying the nibble of Dest to modify.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 100000N | NNI | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |
| EEEE | 1000000 | 00I | 000000000 | SSSSSSSSS | D* | --- | --- | 2 |


*Dest and nibble ID specified by prior ALTSN instruction.

**Related:** [ALTSN](#altsn), [SETBYTE](#setbyte), [SETWORD](#setword), [GETNIB](#getnib)

**Explanation:**

SETNIB stores Src[3:0] into the nibble identified by N within Dest, or the nibble and register described by a prior ALTSN instruction. No other bits are modified. N (0-7) identifies a value's individual nibbles by position in least-significant nibble order. The second syntax is intended for use after an ALTSN instruction in a loop to iteratively affect a series of nibble values within contiguous long registers.

::: pasm2
        SETNIB  data, #$A, #5   ' Set nibble 5 of data to $A
:::



::: instrheader
## SETPAT {#setpat}
Set Pin Pattern

[Pin I/O and Smart Pins](#pin-io-and-smart-pins) - Configures pin pattern matching for PAT event detection.
:::

**SETPAT**  *{#}Dest, {#}Src*

---

**Result:** Pin pattern for PAT event is configured. C selects INA/INB, Z selects =/!=, Dest provides mask value, Src provides match value.

- Dest is a register or immediate containing mask value.
- Src is a register or immediate containing match value.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011111 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 |


**Related:** [POLLPAT](#pollpat), [WAITPAT](#waitpat)

**Explanation:**

Sets pin pattern for PAT event detection. The C flag selects INA or INB for monitoring, the Z flag selects equality (=) or inequality (!=) matching, Dest provides the mask value to select which pins to monitor, and Src provides the match value to compare against.



::: instrheader
## SETPIV {#setpiv}
Set Pixel Blend Factor

[Color Space and Pixel Operations](#color-space-and-pixel-operations) - Sets the blend factor for BLNPIX and MIXPIX pixel operations.
:::

**SETPIV**  *{#}Dest*

---

**Result:** BLNPIX/MIXPIX blend factor is set to Dest[7:0].

- Dest is a register or literal value (0-511) containing 8-bit blend factor in bits [7:0].


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000111101 | --- | --- | --- | 2 |


**Related:** [SETPIX](#setpix), [BLNPIX](#blnpix), [MIXPIX](#mixpix)

**Explanation:**

Sets the blend factor for BLNPIX and MIXPIX operations to Dest[7:0]. This controls the blending ratio for pixel mixing operations.



::: instrheader
## SETPIX {#setpix}
Set Pixel Mixer Mode

[Color Space and Pixel Operations](#color-space-and-pixel-operations) - Configures the MIXPIX operating mode for pixel combining.
:::

**SETPIX**  *{#}Dest*

---

**Result:** MIXPIX mode is set to Dest[5:0].

- Dest is a register or literal value (0-511) containing 6-bit mode in bits [5:0].


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000111110 | --- | --- | --- | 2 |


**Related:** [SETPIV](#setpiv), [MIXPIX](#mixpix)

**Explanation:**

Sets the MIXPIX operating mode to Dest[5:0]. This configures how the pixel mixer combines pixel values.



::: instrheader
## SETQ {#setq}
Set Q Register

[Hub Memory Access](#hub-memory-access) - Loads the Q register for block transfers and multi-parameter instructions.
:::

**SETQ**  *{#}Dest*

---

**Result:** Q register is set to Dest.

- Dest is a register or literal value (0-511) to load into Q.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000101000 | --- | --- | --- | 2 |


**Related:** [SETQ2](#setq2), [RDLONG](#rdlong), [WRLONG](#wrlong)

**Explanation:**

Sets Q register to Dest. Use before RDLONG/WRLONG/WMLONG to set block transfer count. Also used before MUXQ/COGINIT/QDIV/QFRAC/QROTATE/WAITxxx instructions to provide additional parameters.

::: pasm2
        SETQ    #16-1          ' Set up for 16-long block transfer
        RDLONG  buffer, ptra   ' Read 16 longs from hub
:::

**Pitfall (Silicon Bug):** Intervening ALTx, AUGS, or AUGD instructions between SETQ and RDLONG/WRLONG/WMLONG cancel the block-size PTRx delta calculation. The correct number of longs transfers, but PTRx advances by only a single-long delta instead of the full block size. Avoid placing any ALTx or AUGx instruction between SETQ and the block transfer instruction, or manually adjust PTRx afterward.


::: instrheader
## SETQ2 {#setq2}
Set Q For LUT Transfers

[Hub Memory Access](#hub-memory-access) - Loads the Q register for LUT-to-hub block transfers.
:::

**SETQ2**  *{#}Dest*

---

**Result:** Q register is set to Dest for LUT block transfers.

- Dest is a register or literal value (0-511) to load into Q.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000101001 | --- | --- | --- | 2 |


**Related:** [SETQ](#setq), [RDLONG](#rdlong), [WRLONG](#wrlong), [RDLUT](#rdlut), [WRLUT](#wrlut)

**Explanation:**

Sets Q register to Dest. Use before RDLONG/WRLONG/WMLONG to set LUT block transfer. SETQ2 enables block transfers to/from LUT RAM instead of COG RAM: SETQ2 + RDLONG performs block read from HUB to LUT, while SETQ2 + WRLONG performs block write from LUT to HUB. This is essential for fast bulk data movement for lookup tables, waveform tables, and large datasets.

::: pasm2
        SETQ2   #256-1         ' Set up for 256-long LUT transfer
        RDLONG  0, ptra        ' Read 256 longs from hub into LUT
:::

**Pitfall (Silicon Bug):** Same as SETQ—intervening ALTx, AUGS, or AUGD instructions between SETQ2 and RDLONG/WRLONG/WMLONG cancel the block-size PTRx delta calculation. The data transfers correctly, but PTRx advances by only a single-long delta instead of the full block size. Avoid placing any ALTx or AUGx instruction between SETQ2 and the block transfer instruction.


::: instrheader
## SETR {#setr}
Set Result Field

[Register Indirection](#register-indirection) - Sets the Result field of a template for use with ALTI instruction.
:::

**SETR**  *Dest, {#}Src*

---

**Result:** The Result field [27:19] of template Dest is set to Src[8:0].

- Dest is a register whose 32-bit value is a template for use with an ALTI instruction.
- Src is a register or 9-bit literal whose value (Src[8:0]) is copied to the Result field of Dest.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001101 | 01I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |


**Related:** [SETD](#setd), [SETS](#sets), [ALTI](#alti)

**Explanation:**

SETR copies Src[8:0] to the Result field of the template Dest to be used with an ALTI instruction. Bits outside the Result field remain unaffected. The Result field does not exist in instruction opcodes, but takes its value from the D field, holding the address of a register for the instruction to use as its result destination upon execution.

SETR can also be used in self-modifying register RAM code, though it affects the Instr field and upper two bits of the FX field rather than a non-existent Register field. Unlike with ALTx instructions, when used this way, field value modification occurs in the program code itself (not the instruction pipeline); code is altered, values persist. Due to the instruction pipeline nature, after modifying a code register, it is necessary to elapse at least two instructions before executing the modified register.



::: instrheader
## SETS {#sets}
Set Source Field

[Register Indirection](#register-indirection) - Sets the S field of a template for use with ALTI instruction.
:::

**SETS**  *Dest, {#}Src*

---

**Result:** The S field [8:0] of template Dest is set to Src[8:0].

- Dest is a register whose 32-bit value is a template for use with an ALTI instruction.
- Src is a register or 9-bit literal whose value (Src[8:0]) is copied to the S field of Dest.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001101 | 11I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |


**Related:** [SETD](#setd), [SETR](#setr), [ALTI](#alti)

**Explanation:**

SETS copies Src[8:0] to the S field of the template Dest to be used with an ALTI instruction. Bits outside the S field remain unaffected. The S field holds the address of a register or literal value for an instruction to use as its source value during its execution.

SETS can also be used in self-modifying register RAM code. Unlike with ALTx instructions, when used this way, field value modification occurs in the program code itself (not the instruction pipeline); code is altered, values persist. Due to the instruction pipeline nature, after modifying a code register, it is necessary to elapse at least two instructions before executing the modified register.



::: instrheader
## SETSCP {#setscp}
Set Oscilloscope

[Miscellaneous](#miscellaneous) - Configures the four-channel hardware oscilloscope for debugging.
:::

**SETSCP**  *{#}Dest*

---

**Result:** Four-channel oscilloscope enable is set to Dest[6] and input pin base is set to Dest[5:2].

- Dest is a register or literal value (0-511) containing enable bit [6] and pin base [5:2].


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 001110000 | --- | --- | --- | 2 |


**Explanation:**

Sets the four-channel oscilloscope enable to Dest[6] and sets the input pin base to Dest[5:2]. This configures the hardware oscilloscope feature for debugging and signal monitoring.



::: instrheader
## SETSE1 / SETSE2 / SETSE3 / SETSE4 {#setse1}
Set Selectable Event (1, 2, 3, Or 4)

[Events and Timing](#events-and-timing) - Configures the detection criteria for selectable events.
:::

\hypertarget{setse2}{}\hypertarget{setse3}{}\hypertarget{setse4}{}

**SETSE1**  *{#}Dest*\
**SETSE2**  *{#}Dest*\
**SETSE3**  *{#}Dest*\
**SETSE4**  *{#}Dest*

---

**Result:** The specified selectable event configuration (SE1-SE4) is set to Dest[8:0].

- Dest is a register or literal value (0-511) containing event configuration in bits [8:0].


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000100000 | --- | --- | --- | 2 |
| EEEE | 1101011 | 00L | DDDDDDDDD | 000100001 | --- | --- | --- | 2 |
| EEEE | 1101011 | 00L | DDDDDDDDD | 000100010 | --- | --- | --- | 2 |
| EEEE | 1101011 | 00L | DDDDDDDDD | 000100011 | --- | --- | --- | 2 |


**Related:** [POLLSE1/2/3/4](#pollse1), [WAITSE1/2/3/4](#waitse1), [JSE1/2/3/4](#jse1), [JNSE1/2/3/4](#jnse1)

**Explanation:**

SETSE1, SETSE2, SETSE3, and SETSE4 configure their respective selectable event's detection criteria. The Dest[8:0] operand specifies which condition will trigger the event.

The P2 provides four independent selectable events, each of which can be configured to detect various conditions including pin states, hub operations, CORDIC completion, and other system events. Once configured, these events can be polled with POLLSEn, waited upon with WAITSEn, or used for conditional jumps with JSEn and JNSEn.



::: instrheader
## SETWORD {#setword}
Set Word

[Arithmetic Operations](#arithmetic-operations) - Writes a 16-bit value to a specific word position within a register.
:::

**SETWORD**  *Dest, {#}Src, #N*\
**SETWORD**  *{#}Src*

---

**Result:** Src[15:0] is written to word N (0-1) of Dest, or to another register word described by prior ALTSW instruction.

- Dest is a register in which to modify a word.
- Src is a register, 9-bit literal, or 16-bit augmented literal whose bits [15:0] will be stored in the designated location.
- N is a 1-bit literal (0-1) identifying the word of Dest to modify.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001001 | 0NI | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |
| EEEE | 1001001 | 00I | 000000000 | SSSSSSSSS | D* | --- | --- | 2 |


*Dest and word ID specified by prior ALTSW instruction.

**Related:** [ALTSW](#altsw), [SETNIB](#setnib), [SETBYTE](#setbyte), [GETWORD](#getword)

**Explanation:**

SETWORD stores Src[15:0] into the word identified by N within Dest, or the word and register described by a prior ALTSW instruction. No other bits are modified. N (0-1) identifies a value's individual words by position in least-significant word order. The second syntax is intended for use after an ALTSW instruction in a loop to iteratively affect a series of word values within contiguous long registers.

::: pasm2
        SETWORD data, #$ABCD, #1  ' Set high word of data to $ABCD
:::



::: instrheader
## SETXFRQ {#setxfrq}
Set Streamer Frequency

[Streamer](#streamer) - Sets the NCO frequency that controls streamer data output rate.
:::

**SETXFRQ**  *{#}Dest*

---

**Result:** Streamer NCO frequency is set to Dest.

- Dest is a register or literal value (0-511) containing frequency value.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000011101 | --- | --- | --- | 2 |


**Related:** [XINIT](#xinit), [XCONT](#xcont)

**Explanation:**

Sets the streamer NCO (Numerically Controlled Oscillator) frequency to Dest. This controls the frequency at which the streamer outputs data.



::: instrheader
## SEUSSF {#seussf}
Seuss Forward

[Arithmetic Operations](#arithmetic-operations) - Transforms bits by relocating and inverting for pseudo-random scrambling.
:::

**SEUSSF**  *Dest*

---

**Result:** Dest is transformed by relocating and periodically inverting bits. Returns to original value on 32nd iteration.

- Dest is a register to transform.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001100100 | D | --- | --- | 2 |


**Related:** [SEUSSR](#seussr)

**Explanation:**

Relocates and periodically inverts bits within Dest using a forward pattern. The transformation returns to the original value after 32 iterations. This is useful for pseudo-random bit scrambling and data obfuscation.



::: instrheader
## SEUSSR {#seussr}
Seuss Reverse

[Arithmetic Operations](#arithmetic-operations) - Reverse transforms bits for pseudo-random scrambling, inverse of SEUSSF.
:::

**SEUSSR**  *Dest*

---

**Result:** Dest is transformed by relocating and periodically inverting bits. Returns to original value on 32nd iteration.

- Dest is a register to transform.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001100101 | D | --- | --- | 2 |


**Related:** [SEUSSF](#seussf)

**Explanation:**

Relocates and periodically inverts bits within Dest using a reverse pattern. The transformation returns to the original value after 32 iterations. This is useful for pseudo-random bit scrambling and data obfuscation, providing the inverse operation of SEUSSF.



::: instrheader
## SHL {#shl}
Shift Left

[Arithmetic Operations](#arithmetic-operations) - Shifts bits left, inserting zeros for fast multiplication by powers of two.
:::

**SHL**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are shifted left by Src bits, inserting zeros (0) as new rightmost bits.

- Dest is a register containing the value to left shift.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to shift.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0000011 | CZI | DDDDDDDDD | SSSSSSSSS | D | Last bit out\textsuperscript{1} | Result = 0 | 2 |


**Related:** [SHR](#shr), [SAL](#sal), [SAR](#sar), [ROL](#rol)

**Explanation:**

SHL shifts the destination's binary value left by the source number of places (0-31 bits) and sets the new LSBs to 0. This is useful for bit-stream manipulation as well as for swift multiplication; signed or unsigned 32-bit integer multiplication by a power-of-two. Care must be taken for power-of-two multiplications since upper bits shift through the MSB (sign bit), mangling large signed values.

::: pasm2
        SHL     value, #2      ' Multiply by 4
:::



::: instrheader
## SHR {#shr}
Shift Right

[Arithmetic Operations](#arithmetic-operations) - Shifts bits right, inserting zeros for fast unsigned division.
:::

**SHR**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are shifted right by Src bits, inserting zeros (0) as new leftmost bits.

- Dest is a register containing the value to right shift.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to shift.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0000010 | CZI | DDDDDDDDD | SSSSSSSSS | D | Last bit out\textsuperscript{1} | Result = 0 | 2 |


**Related:** [SHL](#shl), [SAR](#sar), [ROR](#ror)

**Explanation:**

SHR shifts the destination's binary value right by the source number of places (0-31 bits) and sets the new MSBs to 0. This is useful for bit-stream manipulation as well as for swift division; unsigned 32-bit integer division by a power-of-two. For similar division of a signed value, use SAR instead.

::: pasm2
        SHR     value, #3      ' Divide unsigned by 8
:::



::: instrheader
## SIGNX {#signx}
Sign Extend

[Arithmetic Operations](#arithmetic-operations) - Sign-extends a value above the specified bit position.
:::

**SIGNX**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The Dest value is sign-extended above the bit indicated by Src and is stored in Dest. Optionally the C and Z flags are updated to the resulting MSB and zero status.

- Dest is a register containing the value to sign-extend above bit Src[4:0] and where the result is written.
- Src is a register or 9-bit literal whose value (lower 5 bits) identifies the bit of Dest to sign-extend beyond.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0111011 | CZI | DDDDDDDDD | SSSSSSSSS | D | MSB of result | Result = 0 | 2 |


**Related:** [ZEROX](#zerox)

**Explanation:**

SIGNX fills the bits of Dest above the bit indicated by Src[4:0] with the value of that identified bit, i.e. sign-extending the value. This is handy when converting encoded or received signed values from a small bit width to a large bit width, i.e. 32 bits.

::: pasm2
        SIGNX   value, #7      ' Sign-extend 8-bit value to 32 bits
:::



::: instrheader
## SKIP {#skip}
Skip Instructions

[Branching and Flow Control](#branching-and-flow-control) - Cancels subsequent instructions based on a bitmask pattern.
:::

**SKIP**  *{#}Dest*

---

**Result:** Subsequent instructions 0-31 are cancelled for each '1' bit in Dest[0]-Dest[31].

- Dest is a register or literal value (0-511) containing skip pattern bitmask.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000110001 | --- | --- | --- | 2 |


**Related:** [SKIPF](#skipf)

**Explanation:**

Skips instructions based on Dest bitmask. Subsequent instructions 0-31 get cancelled for each '1' bit in Dest[0]-Dest[31]. Each set bit causes the corresponding sequential instruction to be cancelled (replaced with NOP).

::: pasm2
        SKIP    #%10101        ' Skip instructions 0, 2, 4
        NOP                    ' Skipped (bit 0)
        ADD     x, #1          ' Executed (bit 1 = 0)
        NOP                    ' Skipped (bit 2)
:::



::: instrheader
## SKIPF {#skipf}
Skip Instructions Fast

[Branching and Flow Control](#branching-and-flow-control) - Leaps over instructions based on a bitmask for faster skipping.
:::

**SKIPF**  *{#}Dest*

---

**Result:** Program counter leaps over cog/LUT instructions based on Dest bitmask.

- Dest is a register or literal value (0-511) containing skip pattern bitmask.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000110010 | --- | --- | --- | 2 |


**Related:** [SKIP](#skip)

**Explanation:**

Like SKIP, but instead of cancelling instructions, the PC leaps over them. This provides faster execution when skipping multiple instructions, as the skipped instructions are never fetched or executed.

**CRITICAL: COG/LUT Memory Only**

SKIPF can ONLY leap over instructions when executing from **COG or LUT memory**. When SKIPF is executed from Hub memory, it automatically **reverts to SKIP behavior** (cancelling instructions in the pipeline instead of stepping over them). This is a hardware limitation—the Hub memory FIFO can only provide sequential instructions; random PC stepping requires the random-access capability of COG/LUT memory.

**Best Practice:** Use SKIP for code in Hub memory (ORGH sections), SKIPF for code in COG/LUT memory (ORG sections).

**REP Compatibility:**
- SKIP is fully compatible with REP—cancellation maintains instruction counts
- SKIPF works with REP ONLY if all skip patterns result in identical instruction counts
- Recommendation: Use SKIP within REP blocks for predictable behavior



::: instrheader
## SPLITB {#splitb}
Split Bits To Bytes

[Arithmetic Operations](#arithmetic-operations) - Redistributes every 4th bit into separate bytes.
:::

**SPLITB**  *Dest*

---

**Result:** Dest = {Dest[31], Dest[27], Dest[23], Dest[19], ...Dest[12], Dest[8], Dest[4], Dest[0]}.

- Dest is a register to transform.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001100000 | D | --- | --- | 2 |


**Related:** [SPLITW](#splitw), [MERGEB](#mergeb)

**Explanation:**

Splits every 4th bit of Dest into bytes. The bits at positions 0, 4, 8, 12, 16, 20, 24, 28 become the new low byte, the bits at positions 1, 5, 9, 13, 17, 21, 25, 29 become the second byte, and so on. This is useful for bit reordering and data unpacking operations.



::: instrheader
## SPLITW {#splitw}
Split Bits To Words

[Arithmetic Operations](#arithmetic-operations) - Separates odd and even bits into separate words.
:::

**SPLITW**  *Dest*

---

**Result:** Dest = {Dest[31], Dest[29], Dest[27], Dest[25], ...Dest[6], Dest[4], Dest[2], Dest[0]}.

- Dest is a register to transform.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001100010 | D | --- | --- | 2 |


**Related:** [SPLITB](#splitb), [MERGEW](#mergew)

**Explanation:**

Splits odd and even bits of Dest into separate words. The even bits (0, 2, 4, ...30) become the low word, and the odd bits (1, 3, 5, ...31) become the high word. This is useful for bit reordering and data unpacking operations.



::: instrheader
## STALLI {#stalli}
Disallow Interrupts

[Interrupts](#interrupts) - Disables interrupt branching to protect critical code sections.
:::

**STALLI**

---

**Result:** All future interrupts are disallowed.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | 000100001 | 000100100 | --- | --- | --- | 2 |


**Related:** [ALLOWI](#allowi)

**Explanation:**

STALLI disables interrupt branching. STALLI is the complement of the ALLOWI instruction; both are used to protect short, vital sections of main code from timing jitter or state loss caused by asynchronous interrupt handling.

::: pasm2
        STALLI                 ' Disable interrupts
        ' Critical section...
        ALLOWI                 ' Re-enable interrupts
:::



::: instrheader
## SUB {#sub}
Subtract

[Arithmetic Operations](#arithmetic-operations) - Subtracts unsigned Src from unsigned Dest.
:::

**SUB**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Difference of unsigned Dest and unsigned Src is stored in Dest and optionally the C and Z flags are updated to the borrow and zero status.

- Dest is a register containing the value to subtract Src from, and where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is subtracted from Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0001100 | CZI | DDDDDDDDD | SSSSSSSSS | D | Borrow of (D - S) | Result = 0 | 2 |


**Related:** [SUBX](#subx), [SUBS](#subs), [SUBSX](#subsx), [SUBR](#subr), [ADD](#add)

**Explanation:**

SUB subtracts the unsigned Src from the unsigned Dest and stores the result into the Dest register. To subtract unsigned multi-long values, use SUB followed by SUBX as described in Subtracting Two Multi-Long Values. SUB and SUBX are also used in subtracting signed multi-long values with SUBSX ending the sequence.

::: pasm2
        SUB     count, #1 WZ   ' Decrement count, set Z if zero
:::



::: instrheader
## SUBR {#subr}
Subtract Reverse

[Arithmetic Operations](#arithmetic-operations) - Subtracts unsigned Dest from unsigned Src (reverse order).
:::

**SUBR**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Difference of unsigned Src and unsigned Dest is stored in Dest and optionally the C and Z flags are updated to the borrow and zero status.

- Dest is a register containing the value to subtract from Src, and where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is subtracted by Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0010110 | CZI | DDDDDDDDD | SSSSSSSSS | D | Borrow of (S - D) | Result = 0 | 2 |


**Related:** [SUB](#sub)

**Explanation:**

SUBR subtracts the unsigned Dest from the unsigned Src and stores the result into the Dest register. This is the reverse of the subtraction order of SUB, computing Src - Dest instead of Dest - Src.



::: instrheader
## SUBS {#subs}
Subtract Signed

[Arithmetic Operations](#arithmetic-operations) - Subtracts signed Src from signed Dest.
:::

**SUBS**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Difference of signed Dest and signed Src is stored in Dest and optionally the C and Z flags are updated to the sign and zero status.

- Dest is a register containing the value to subtract Src from, and where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is subtracted from Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0001110 | CZI | DDDDDDDDD | SSSSSSSSS | D | Sign of (D - S) | Result = 0 | 2 |


**Related:** [SUB](#sub), [SUBX](#subx), [SUBSX](#subsx)

**Explanation:**

SUBS subtracts the signed Src from the signed Dest and stores the result into the Dest register. If Src is a 9-bit literal, its value is interpreted as positive (0-511; it is not sign-extended). Use ##Value (or insert a prior AUGS instruction) for a 32-bit signed value; negative or positive. To subtract signed multi-long values, use SUB (not SUBS) followed possibly by SUBX, and finally SUBSX.



::: instrheader
## SUBSX {#subsx}
Subtract Signed Extended

[Arithmetic Operations](#arithmetic-operations) - Subtracts signed Src plus C from signed Dest for multi-long operations.
:::

**SUBSX**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Difference of signed Dest and signed Src (plus C) is stored in Dest and optionally the C and Z flags are updated to the extended sign and zero status.

- Dest is a register containing the value to subtract Src plus C from, and where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value plus C is subtracted from Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0001111 | CZI | DDDDDDDDD | SSSSSSSSS | D | Sign of D-(S+C) | Z AND (Result = 0) | 2 |


**Related:** [SUB](#sub), [SUBX](#subx), [SUBS](#subs)

**Explanation:**

SUBSX subtracts the signed value of Src plus C from the signed Dest and stores the result into the Dest register. The SUBSX instruction is used to perform signed multi-long (extended) subtraction, such as 64-bit subtraction. Use WC or WCZ on preceding SUB and SUBX instructions for proper final C flag. Use WZ or WCZ on preceding SUB and SUBX instructions for proper final Z flag. To subtract signed multi-long values, use SUB (not SUBS) followed possibly by SUBX, and finally SUBSX.



::: instrheader
## SUBX {#subx}
Subtract Extended

[Arithmetic Operations](#arithmetic-operations) - Subtracts unsigned Src plus C from unsigned Dest for multi-long operations.
:::

**SUBX**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Difference of unsigned Dest and unsigned Src (plus C) is stored in Dest and optionally the C and Z flags are updated to the extended borrow and zero status.

- Dest is a register containing the value to subtract Src plus C from, and where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value plus C is subtracted from Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0001101 | CZI | DDDDDDDDD | SSSSSSSSS | D | Borrow of (D - (S + C)) | Z AND (result = 0) | 2 |


**Related:** [SUB](#sub), [SUBSX](#subsx)

**Explanation:**

SUBX subtracts the unsigned value of Src plus C from the unsigned Dest and stores the result into the Dest register. The SUBX instruction is used to perform unsigned multi-long (extended) subtraction, such as 64-bit subtraction. Use WC or WCZ on preceding SUB and SUBX instructions for proper final C flag. If C is set after the last SUBX in a multi-long subtraction, it indicates unsigned underflow. Use WZ or WCZ on preceding SUB and SUBX instructions for proper final Z flag. To subtract unsigned multi-long values, use SUB followed by one or more SUBX instructions.



::: instrheader
## SUMC / SUMNC / SUMZ / SUMNZ {#sumc}
Conditional Sum

[Arithmetic Operations](#arithmetic-operations) - Conditionally adds or subtracts based on flag state.
:::

**SUMC**  *Dest, {#}Src*  **{WC|WZ|WCZ}**\
**SUMNC**  *Dest, {#}Src*  **{WC|WZ|WCZ}**\
**SUMZ**  *Dest, {#}Src*  **{WC|WZ|WCZ}**\
**SUMNZ**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Conditionally adds or subtracts Src from Dest based on flag state.

- Dest is a register containing the value to adjust.
- Src is a register, 9-bit literal, or 32-bit augmented literal.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0011100 | CZI | DDDDDDDDD | SSSSSSSSS | D | Sign | Result = 0 | 2 |
| EEEE | 0011101 | CZI | DDDDDDDDD | SSSSSSSSS | D | Sign | Result = 0 | 2 |
| EEEE | 0011110 | CZI | DDDDDDDDD | SSSSSSSSS | D | Sign | Result = 0 | 2 |
| EEEE | 0011111 | CZI | DDDDDDDDD | SSSSSSSSS | D | Sign | Result = 0 | 2 |


**Explanation:**

These instructions conditionally add or subtract Src from Dest based on the specified flag state:

| Instruction | Subtracts when | Adds when |
|-------------|----------------|-----------|
| SUMC | C = 1 | C = 0 |
| SUMNC | C = 0 | C = 1 |
| SUMZ | Z = 1 | Z = 0 |
| SUMNZ | Z = 0 | Z = 1 |

The C flag (with WC) is updated to reflect the correct sign of the result.

SUMC and SUMZ subtract when their flag is set (1). SUMNC and SUMNZ subtract when their flag is clear (0), providing complementary behavior.


