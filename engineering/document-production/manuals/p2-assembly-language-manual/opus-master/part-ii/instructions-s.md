# Instructions: S

This section contains all PASM2 instructions beginning with the letter S.



## SAL {#sal}

Shift arithmetic left
[Shift/Rotate Instruction](#shift-rotate-instructions) - Shift bits left, extending original LSB into new rightmost positions.

**SAL**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are shifted left by Src bits, extending Dest[0] into new rightmost bits.

- Dest is a register containing the value to arithmetically left shift.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to shift.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0000111}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Last bit out\textsuperscript{1}}{Result = 0}{2}

\textsuperscript{1} C = last bit shifted out if S[4:0] > 0, else D[31]
```

**Related:** [SAR](#sar), [SHL](#shl), [SHR](#shr)

**Explanation:**

SAL shifts the destination's binary value left by the source number of places (0-31 bits) and sets the new LSBs to that of the original Dest[0]. SAL is the complement of SAR for bit streams but not for math operations. For swift 32-bit integer multiplication by a power-of-two, use SHL instead.

::: pasm2
        SAL     data, #4       ' Shift left 4 bits, extending LSB
:::



## SAR {#sar}

Shift arithmetic right
[Shift/Rotate Instruction](#shift-rotate-instructions) - Shift bits right, extending sign bit into new leftmost positions.

**SAR**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are shifted right by Src bits, extending Dest[31] (the sign bit) into new leftmost bits.

- Dest is a register containing the value to arithmetically right shift.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to shift.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0000110}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Last bit out\textsuperscript{1}}{Result = 0}{2}

\textsuperscript{1} C = last bit shifted out if S[4:0] > 0, else D[0]
```

**Related:** [SAL](#sal), [SHL](#shl), [SHR](#shr)

**Explanation:**

SAR shifts the destination's binary value right by the source number of places (0-31 bits) and sets the new MSBs to that of the original Dest[31], preserving the sign of a signed integer. This is useful for bit stream manipulation and for swift division. It is similar to SHR for swift division by a power-of-two, but is safe for both signed and unsigned integers.

::: pasm2
        SAR     value, #3      ' Divide signed value by 8
:::



## SCA {#sca}

Scale
[Multiply/Divide Instruction](#multiply-divide-instructions) - Multiply 16-bit values and scale result for next instruction.

**SCA**  *Dest, {#}Src*  **{WZ}**

---

**Result:** The upper 16 bits of the unsigned product from the 16-bit Dest and Src multiplication is substituted as the next instruction's S value.

- Dest is a register containing the 16-bit value to multiply with Src.
- Src is a register, 9-bit literal, or 16-bit augmented literal to multiply with Dest.
- WZ is an optional effect to update the Z flag.

```{=latex}
\simpleencoding{EEEE}{1010001}{0ZI}{DDDDDDDDD}{SSSSSSSSS}{---}{---}{Product = 0}{2}
```

**Related:** [SCAS](#scas)

**Explanation:**

SCA multiplies the lower 16 bits of each of Dest and Src together, right shifts the 32-bit product by 16 (to scale down the result), and substitutes this value as the next instruction's S value. This is useful for creating scaled unsigned 16-bit values for subsequent operations.

::: pasm2
        SCA     factor, #$8000  ' Scale by 0.5 (32768/65536)
        ADD     result, #0      ' Add scaled value
:::



## SCAS {#scas}

Scale signed
[Multiply/Divide Instruction](#multiply-divide-instructions) - Multiply signed 16-bit values and scale result for next instruction.

**SCAS**  *Dest, {#}Src*  **{WZ}**

---

**Result:** The upper 18 bits of the signed product from the 16-bit Dest and Src multiplication is substituted as the next instruction's S value.

- Dest is a register containing the signed 16-bit value to multiply with Src.
- Src is a register, 9-bit literal, or signed 16-bit augmented literal to multiply with Dest.
- WZ is an optional effect to update the Z flag.

```{=latex}
\simpleencoding{EEEE}{1010001}{1ZI}{DDDDDDDDD}{SSSSSSSSS}{---}{---}{Result = 0}{2}
```

**Related:** [SCA](#sca)

**Explanation:**

SCAS multiplies the lower signed 16 bits of each of Dest and Src together, right shifts the 32-bit product by 14 (to scale down the result), and substitutes this value as the next instruction's S value. This is useful for creating scaled signed values for subsequent operations.



## SETBYTE {#setbyte}

Set byte
[Bit/Nibble/Byte/Word Instruction](#bit-nibble-byte-word-instructions) - Store an 8-bit value into a specified byte position within a register.

**SETBYTE**  *Dest, {#}Src, #N*
**SETBYTE**  *{#}Src*

---

**Result:** Src[7:0] is written to byte N (0-3) of Dest, or to another register byte described by prior ALTSB instruction.

- Dest is a register in which to modify a byte.
- Src is a register or 8-bit literal whose bits [7:0] will be stored in the designated location.
- N is a 2-bit literal (0-3) identifying the byte of Dest to modify.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1000110}{NNI}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{2}
\encodingrow{EEEE}{1000110}{00I}{000000000}{SSSSSSSSS}{D*}{---}{---}{2}
\end{encodingtable}
```

*Dest and byte ID specified by prior ALTSB instruction.

**Related:** [ALTSB](#altsb), [SETNIB](#setnib), [SETWORD](#setword), [GETBYTE](#getbyte)

**Explanation:**

SETBYTE stores Src[7:0] into the byte identified by N within Dest, or the byte and register described by a prior ALTSB instruction. No other bits are modified. N (0-3) identifies a value's individual bytes by position in least-significant byte order. The second syntax is intended for use after an ALTSB instruction in a loop to iteratively affect a series of byte values within contiguous long registers.

::: pasm2
        SETBYTE data, #$FF, #2  ' Set byte 2 of data to $FF
:::



## SETCFRQ {#setcfrq}

Set colorspace converter frequency
[Colorspace Instruction](#colorspace-instructions) - Configure the colorspace converter CFRQ parameter.

**SETCFRQ**  *{#}Dest*

---

**Result:** The colorspace converter CFRQ parameter is set to Dest[31:0].

- Dest is a register or literal value (0-511) to set as CFRQ parameter.

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000111011}{---}{---}{---}{2}
```

**Related:** [SETCI](#setci), [SETCMOD](#setcmod), [SETCQ](#setcq), [SETCY](#setcy)

**Explanation:**

Sets the colorspace converter CFRQ parameter to the value in Dest. This instruction configures the frequency parameter for the colorspace conversion hardware.



## SETCI {#setci}

Set colorspace converter CI
[Colorspace Instruction](#colorspace-instructions) - Configure the colorspace converter CI parameter.

**SETCI**  *{#}Dest*

---

**Result:** The colorspace converter CI parameter is set to Dest[31:0].

- Dest is a register or literal value (0-511) to set as CI parameter.

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000111001}{---}{---}{---}{2}
```

**Related:** [SETCFRQ](#setcfrq), [SETCMOD](#setcmod), [SETCQ](#setcq), [SETCY](#setcy)

**Explanation:**

Sets the colorspace converter CI parameter to the value in Dest. This instruction configures the CI parameter for the colorspace conversion hardware.



## SETCMOD {#setcmod}

Set colorspace converter mode
[Colorspace Instruction](#colorspace-instructions) - Configure the colorspace converter mode parameter.

**SETCMOD**  *{#}Dest*

---

**Result:** The colorspace converter CMOD parameter is set to Dest[8:0].

- Dest is a register or literal value (0-511) to set as CMOD parameter.

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000111100}{---}{---}{---}{2}
```

**Related:** [SETCFRQ](#setcfrq), [SETCI](#setci), [SETCQ](#setcq), [SETCY](#setcy)

**Explanation:**

Sets the colorspace converter CMOD parameter to Dest[8:0]. This instruction configures the mode parameter for the colorspace conversion hardware.



## SETCQ {#setcq}

Set colorspace converter CQ
[Colorspace Instruction](#colorspace-instructions) - Configure the colorspace converter CQ parameter.

**SETCQ**  *{#}Dest*

---

**Result:** The colorspace converter CQ parameter is set to Dest[31:0].

- Dest is a register or literal value (0-511) to set as CQ parameter.

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000111010}{---}{---}{---}{2}
```

**Related:** [SETCFRQ](#setcfrq), [SETCI](#setci), [SETCMOD](#setcmod), [SETCY](#setcy)

**Explanation:**

Sets the colorspace converter CQ parameter to the value in Dest. This instruction configures the CQ parameter for the colorspace conversion hardware.



## SETCY {#setcy}

Set colorspace converter CY
[Colorspace Instruction](#colorspace-instructions) - Configure the colorspace converter CY parameter.

**SETCY**  *{#}Dest*

---

**Result:** The colorspace converter CY parameter is set to Dest[31:0].

- Dest is a register or literal value (0-511) to set as CY parameter.

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000111000}{---}{---}{---}{2}
```

**Related:** [SETCFRQ](#setcfrq), [SETCI](#setci), [SETCMOD](#setcmod), [SETCQ](#setcq)

**Explanation:**

Sets the colorspace converter CY parameter to the value in Dest. This instruction configures the CY parameter for the colorspace conversion hardware.



## SETD {#setd}

Set destination field
[Register Indirection Instruction](#register-indirection-instructions) - Modify the D field of an instruction template for use with ALTI.

**SETD**  *Dest, {#}Src*

---

**Result:** The D field [17:9] of template Dest is set to Src[8:0].

- Dest is a register whose 32-bit value is a template for use with an ALTI instruction.
- Src is a register or 9-bit literal whose value (Src[8:0]) is copied to the D field of Dest.

```{=latex}
\simpleencoding{EEEE}{1001101}{10I}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{2}
```

**Related:** [SETS](#sets), [SETR](#setr), [ALTI](#alti)

**Explanation:**

SETD copies Src[8:0] to the D field of the template Dest to be used with an ALTI instruction. Bits outside the D field remain unaffected. The D field holds the address of a register (or sometimes a literal value) for the instruction to use as its destination value, and usually as its result destination, during its execution.

SETD can also be used in self-modifying register RAM code. Unlike with ALTx instructions, when used this way, field value modification occurs in the program code itself (not the instruction pipeline); code is altered, values persist. Due to the instruction pipeline nature, after modifying a code register, it is necessary to elapse at least two instructions before executing the modified register.



## SETDACS {#setdacs}

Set DACs
[DAC Instruction](#dac-instructions) - Simultaneously set all four DAC channels.

**SETDACS**  *{#}Dest*

---

**Result:** DAC3 = Dest[31:24], DAC2 = Dest[23:16], DAC1 = Dest[15:8], DAC0 = Dest[7:0].

- Dest is a register or literal value (0-511) containing four 8-bit DAC values.

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000011100}{---}{---}{---}{2}
```

**Explanation:**

Sets all four DAC channels simultaneously from the four bytes in Dest. DAC3 receives bits [31:24], DAC2 receives bits [23:16], DAC1 receives bits [15:8], and DAC0 receives bits [7:0].



## SETINT1 {#setint1}

Set interrupt 1 source
[Interrupt Instruction](#interrupt-instructions) - Configure the interrupt 1 source.

**SETINT1**  *{#}Dest*

---

**Result:** The INT1 interrupt source is set to Dest[3:0].

- Dest is a register or literal value (0-511) containing interrupt source in bits [3:0].

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000100101}{---}{---}{---}{2}
```

**Related:** [SETINT2](#setint2), [SETINT3](#setint3), [NIXINT1](#nixint1), [TRGINT1](#trgint1), [RETI0](#reti0)

**Explanation:**

SETINT1 configures which event will trigger interrupt 1. The interrupt source is specified in Dest[3:0]. The P2 provides three configurable interrupt levels (INT1-INT3), each of which can be independently configured to respond to different event sources.



## SETINT2 {#setint2}

Set interrupt 2 source
[Interrupt Instruction](#interrupt-instructions) - Configure the interrupt 2 source.

**SETINT2**  *{#}Dest*

---

**Result:** The INT2 interrupt source is set to Dest[3:0].

- Dest is a register or literal value (0-511) containing interrupt source in bits [3:0].

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000100110}{---}{---}{---}{2}
```

**Related:** [SETINT1](#setint1), [SETINT3](#setint3), [NIXINT2](#nixint2), [TRGINT2](#trgint2), [RETI0](#reti0)

**Explanation:**

SETINT2 configures which event will trigger interrupt 2. The interrupt source is specified in Dest[3:0].



## SETINT3 {#setint3}

Set interrupt 3 source
[Interrupt Instruction](#interrupt-instructions) - Configure the interrupt 3 source.

**SETINT3**  *{#}Dest*

---

**Result:** The INT3 interrupt source is set to Dest[3:0].

- Dest is a register or literal value (0-511) containing interrupt source in bits [3:0].

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000100111}{---}{---}{---}{2}
```

**Related:** [SETINT1](#setint1), [SETINT2](#setint2), [NIXINT3](#nixint3), [TRGINT3](#trgint3), [RETI0](#reti0)

**Explanation:**

SETINT3 configures which event will trigger interrupt 3. The interrupt source is specified in Dest[3:0].



## SETLUTS {#setluts}

Set LUT sharing
[LUT Instruction](#lut-instructions) - Enable or disable LUT sharing between adjacent cogs.

**SETLUTS**  *{#}Dest*

---

**Result:** If Dest[0] = 1, LUT sharing is enabled where LUT writes within the adjacent odd/even companion cog are copied to this cog's LUT.

- Dest is a register or literal value (0-511) with enable bit in Dest[0].

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000110111}{---}{---}{---}{2}
```

**Related:** [RDLUT](#rdlut), [WRLUT](#wrlut)

**Explanation:**

Enables or disables LUT sharing based on Dest[0]. When enabled (Dest[0] = 1), LUT writes within the adjacent odd/even companion cog are automatically copied to this cog's LUT, allowing cogs to share lookup table data.



## SETNIB {#setnib}

Set nibble
[Bit/Nibble/Byte/Word Instruction](#bit-nibble-byte-word-instructions) - Store a 4-bit value into a specified nibble position within a register.

**SETNIB**  *Dest, {#}Src, #N*
**SETNIB**  *{#}Src*

---

**Result:** Src[3:0] is written to nibble N (0-7) of Dest, or to another register nibble described by prior ALTSN instruction.

- Dest is a register in which to modify a nibble.
- Src is a register or 4-bit literal whose bits [3:0] will be stored in the designated location.
- N is a 3-bit literal (0-7) identifying the nibble of Dest to modify.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{100000N}{NNI}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{2}
\encodingrow{EEEE}{1000000}{00I}{000000000}{SSSSSSSSS}{D*}{---}{---}{2}
\end{encodingtable}
```

*Dest and nibble ID specified by prior ALTSN instruction.

**Related:** [ALTSN](#altsn), [SETBYTE](#setbyte), [SETWORD](#setword), [GETNIB](#getnib)

**Explanation:**

SETNIB stores Src[3:0] into the nibble identified by N within Dest, or the nibble and register described by a prior ALTSN instruction. No other bits are modified. N (0-7) identifies a value's individual nibbles by position in least-significant nibble order. The second syntax is intended for use after an ALTSN instruction in a loop to iteratively affect a series of nibble values within contiguous long registers.

::: pasm2
        SETNIB  data, #$A, #5   ' Set nibble 5 of data to $A
:::



## SETPAT {#setpat}

Set pin pattern
[Pin Instruction](#pin-instructions) - Configure pin pattern matching for PAT event detection.

**SETPAT**  *{#}Dest, {#}Src*

---

**Result:** Pin pattern for PAT event is configured. C selects INA/INB, Z selects =/!=, Dest provides mask value, Src provides match value.

- Dest is a register or immediate containing mask value.
- Src is a register or immediate containing match value.

```{=latex}
\simpleencoding{EEEE}{1011111}{1LI}{DDDDDDDDD}{SSSSSSSSS}{---}{---}{---}{2}
```

**Related:** [POLLPAT](#pollpat), [WAITPAT](#waitpat)

**Explanation:**

Sets pin pattern for PAT event detection. The C flag selects INA or INB for monitoring, the Z flag selects equality (=) or inequality (!=) matching, Dest provides the mask value to select which pins to monitor, and Src provides the match value to compare against.



## SETPIV {#setpiv}

Set pixel blend factor
[Pixel Instruction](#pixel-instructions) - Set the blend factor for pixel mixing operations.

**SETPIV**  *{#}Dest*

---

**Result:** BLNPIX/MIXPIX blend factor is set to Dest[7:0].

- Dest is a register or literal value (0-511) containing 8-bit blend factor in bits [7:0].

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000111101}{---}{---}{---}{2}
```

**Related:** [SETPIX](#setpix), [BLNPIX](#blnpix), [MIXPIX](#mixpix)

**Explanation:**

Sets the blend factor for BLNPIX and MIXPIX operations to Dest[7:0]. This controls the blending ratio for pixel mixing operations.



## SETPIX {#setpix}

Set pixel mixer mode
[Pixel Instruction](#pixel-instructions) - Configure the pixel mixer operating mode.

**SETPIX**  *{#}Dest*

---

**Result:** MIXPIX mode is set to Dest[5:0].

- Dest is a register or literal value (0-511) containing 6-bit mode in bits [5:0].

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000111110}{---}{---}{---}{2}
```

**Related:** [SETPIV](#setpiv), [MIXPIX](#mixpix)

**Explanation:**

Sets the MIXPIX operating mode to Dest[5:0]. This configures how the pixel mixer combines pixel values.



## SETQ {#setq}

Set Q register
[Hub Instruction](#hub-instructions) - Set the Q register for use by subsequent instructions.

**SETQ**  *{#}Dest*

---

**Result:** Q register is set to Dest.

- Dest is a register or literal value (0-511) to load into Q.

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000101000}{---}{---}{---}{2}
```

**Related:** [SETQ2](#setq2), [RDLONG](#rdlong), [WRLONG](#wrlong)

**Explanation:**

Sets Q register to Dest. Use before RDLONG/WRLONG/WMLONG to set block transfer count. Also used before MUXQ/COGINIT/QDIV/QFRAC/QROTATE/WAITxxx instructions to provide additional parameters.

::: pasm2
        SETQ    #16-1          ' Set up for 16-long block transfer
        RDLONG  buffer, ptra   ' Read 16 longs from hub
:::



## SETQ2 {#setq2}

Set Q for LUT transfers
[Hub Instruction](#hub-instructions) - Set the Q register for LUT block transfers.

**SETQ2**  *{#}Dest*

---

**Result:** Q register is set to Dest for LUT block transfers.

- Dest is a register or literal value (0-511) to load into Q.

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000101001}{---}{---}{---}{2}
```

**Related:** [SETQ](#setq), [RDLONG](#rdlong), [WRLONG](#wrlong), [RDLUT](#rdlut), [WRLUT](#wrlut)

**Explanation:**

Sets Q register to Dest. Use before RDLONG/WRLONG/WMLONG to set LUT block transfer. SETQ2 enables block transfers to/from LUT RAM instead of COG RAM: SETQ2 + RDLONG performs block read from HUB to LUT, while SETQ2 + WRLONG performs block write from LUT to HUB. This is essential for fast bulk data movement for lookup tables, waveform tables, and large datasets.

::: pasm2
        SETQ2   #256-1         ' Set up for 256-long LUT transfer
        RDLONG  0, ptra        ' Read 256 longs from hub into LUT
:::



## SETR {#setr}

Set result field
[Register Indirection Instruction](#register-indirection-instructions) - Modify the Result field of an instruction template for use with ALTI.

**SETR**  *Dest, {#}Src*

---

**Result:** The Result field [27:19] of template Dest is set to Src[8:0].

- Dest is a register whose 32-bit value is a template for use with an ALTI instruction.
- Src is a register or 9-bit literal whose value (Src[8:0]) is copied to the Result field of Dest.

```{=latex}
\simpleencoding{EEEE}{1001101}{01I}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{2}
```

**Related:** [SETD](#setd), [SETS](#sets), [ALTI](#alti)

**Explanation:**

SETR copies Src[8:0] to the Result field of the template Dest to be used with an ALTI instruction. Bits outside the Result field remain unaffected. The Result field does not exist in instruction opcodes, but takes its value from the D field, holding the address of a register for the instruction to use as its result destination upon execution.

SETR can also be used in self-modifying register RAM code, though it affects the Instr field and upper two bits of the FX field rather than a non-existent Register field. Unlike with ALTx instructions, when used this way, field value modification occurs in the program code itself (not the instruction pipeline); code is altered, values persist. Due to the instruction pipeline nature, after modifying a code register, it is necessary to elapse at least two instructions before executing the modified register.



## SETS {#sets}

Set source field
[Register Indirection Instruction](#register-indirection-instructions) - Modify the S field of an instruction template for use with ALTI.

**SETS**  *Dest, {#}Src*

---

**Result:** The S field [8:0] of template Dest is set to Src[8:0].

- Dest is a register whose 32-bit value is a template for use with an ALTI instruction.
- Src is a register or 9-bit literal whose value (Src[8:0]) is copied to the S field of Dest.

```{=latex}
\simpleencoding{EEEE}{1001101}{11I}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{2}
```

**Related:** [SETD](#setd), [SETR](#setr), [ALTI](#alti)

**Explanation:**

SETS copies Src[8:0] to the S field of the template Dest to be used with an ALTI instruction. Bits outside the S field remain unaffected. The S field holds the address of a register or literal value for an instruction to use as its source value during its execution.

SETS can also be used in self-modifying register RAM code. Unlike with ALTx instructions, when used this way, field value modification occurs in the program code itself (not the instruction pipeline); code is altered, values persist. Due to the instruction pipeline nature, after modifying a code register, it is necessary to elapse at least two instructions before executing the modified register.



## SETSCP {#setscp}

Set oscilloscope
[Debug Instruction](#debug-instructions) - Configure the four-channel oscilloscope.

**SETSCP**  *{#}Dest*

---

**Result:** Four-channel oscilloscope enable is set to Dest[6] and input pin base is set to Dest[5:2].

- Dest is a register or literal value (0-511) containing enable bit [6] and pin base [5:2].

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{001110000}{---}{---}{---}{2}
```

**Explanation:**

Sets the four-channel oscilloscope enable to Dest[6] and sets the input pin base to Dest[5:2]. This configures the hardware oscilloscope feature for debugging and signal monitoring.



## SETSE1 {#setse1}

Set selectable event 1
[Event Instruction](#event-instructions) - Configure selectable event 1 detection.

**SETSE1**  *{#}Dest*

---

**Result:** The SE1 selectable event configuration is set to Dest[8:0].

- Dest is a register or literal value (0-511) containing event configuration in bits [8:0].

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000100000}{---}{---}{---}{2}
```

**Related:** [SETSE2](#setse2), [SETSE3](#setse3), [SETSE4](#setse4), [POLLSE1](#pollse1), [WAITSE1](#waitse1)

**Explanation:**

SETSE1 configures selectable event 1's detection criteria. The Dest[8:0] operand specifies which condition will trigger the event.

The P2 provides four independent selectable events, each of which can be configured to detect various conditions including pin states, hub operations, CORDIC completion, and other system events. Once configured, these events can be polled with POLLSE1, waited upon with WAITSE1, or used for conditional jumps with JSE1 and JNSE1.



## SETSE2 {#setse2}

Set selectable event 2
[Event Instruction](#event-instructions) - Configure selectable event 2 detection.

**SETSE2**  *{#}Dest*

---

**Result:** The SE2 selectable event configuration is set to Dest[8:0].

- Dest is a register or literal value (0-511) containing event configuration in bits [8:0].

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000100001}{---}{---}{---}{2}
```

**Related:** [SETSE1](#setse1), [SETSE3](#setse3), [SETSE4](#setse4), [POLLSE2](#pollse2), [WAITSE2](#waitse2)

**Explanation:**

SETSE2 configures selectable event 2's detection criteria. The Dest[8:0] operand specifies which condition will trigger the event.



## SETSE3 {#setse3}

Set selectable event 3
[Event Instruction](#event-instructions) - Configure selectable event 3 detection.

**SETSE3**  *{#}Dest*

---

**Result:** The SE3 selectable event configuration is set to Dest[8:0].

- Dest is a register or literal value (0-511) containing event configuration in bits [8:0].

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000100010}{---}{---}{---}{2}
```

**Related:** [SETSE1](#setse1), [SETSE2](#setse2), [SETSE4](#setse4), [POLLSE3](#pollse3), [WAITSE3](#waitse3)

**Explanation:**

SETSE3 configures selectable event 3's detection criteria. The Dest[8:0] operand specifies which condition will trigger the event.



## SETSE4 {#setse4}

Set selectable event 4
[Event Instruction](#event-instructions) - Configure selectable event 4 detection.

**SETSE4**  *{#}Dest*

---

**Result:** The SE4 selectable event configuration is set to Dest[8:0].

- Dest is a register or literal value (0-511) containing event configuration in bits [8:0].

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000100011}{---}{---}{---}{2}
```

**Related:** [SETSE1](#setse1), [SETSE2](#setse2), [SETSE3](#setse3), [POLLSE4](#pollse4), [WAITSE4](#waitse4)

**Explanation:**

SETSE4 configures selectable event 4's detection criteria. The Dest[8:0] operand specifies which condition will trigger the event.



## SETWORD {#setword}

Set word
[Bit/Nibble/Byte/Word Instruction](#bit-nibble-byte-word-instructions) - Store a 16-bit value into a specified word position within a register.

**SETWORD**  *Dest, {#}Src, #N*
**SETWORD**  *{#}Src*

---

**Result:** Src[15:0] is written to word N (0-1) of Dest, or to another register word described by prior ALTSW instruction.

- Dest is a register in which to modify a word.
- Src is a register, 9-bit literal, or 16-bit augmented literal whose bits [15:0] will be stored in the designated location.
- N is a 1-bit literal (0-1) identifying the word of Dest to modify.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1001001}{0NI}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{2}
\encodingrow{EEEE}{1001001}{00I}{000000000}{SSSSSSSSS}{D*}{---}{---}{2}
\end{encodingtable}
```

*Dest and word ID specified by prior ALTSW instruction.

**Related:** [ALTSW](#altsw), [SETNIB](#setnib), [SETBYTE](#setbyte), [GETWORD](#getword)

**Explanation:**

SETWORD stores Src[15:0] into the word identified by N within Dest, or the word and register described by a prior ALTSW instruction. No other bits are modified. N (0-1) identifies a value's individual words by position in least-significant word order. The second syntax is intended for use after an ALTSW instruction in a loop to iteratively affect a series of word values within contiguous long registers.

::: pasm2
        SETWORD data, #$ABCD, #1  ' Set high word of data to $ABCD
:::



## SETXFRQ {#setxfrq}

Set streamer frequency
[Streamer Instruction](#streamer-instructions) - Set the streamer NCO frequency.

**SETXFRQ**  *{#}Dest*

---

**Result:** Streamer NCO frequency is set to Dest.

- Dest is a register or literal value (0-511) containing frequency value.

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000011101}{---}{---}{---}{2}
```

**Related:** [XINIT](#xinit), [XCONT](#xcont)

**Explanation:**

Sets the streamer NCO (Numerically Controlled Oscillator) frequency to Dest. This controls the frequency at which the streamer outputs data.



## SEUSSF {#seussf}

Seuss forward
[Bit Manipulation Instruction](#bit-manipulation-instructions) - Relocate and periodically invert bits using forward pattern.

**SEUSSF**  *Dest*

---

**Result:** Dest is transformed by relocating and periodically inverting bits. Returns to original value on 32nd iteration.

- Dest is a register to transform.

```{=latex}
\simpleencoding{EEEE}{1101011}{000}{DDDDDDDDD}{001100100}{D}{---}{---}{2}
```

**Related:** [SEUSSR](#seussr)

**Explanation:**

Relocates and periodically inverts bits within Dest using a forward pattern. The transformation returns to the original value after 32 iterations. This is useful for pseudo-random bit scrambling and data obfuscation.



## SEUSSR {#seussr}

Seuss reverse
[Bit Manipulation Instruction](#bit-manipulation-instructions) - Relocate and periodically invert bits using reverse pattern.

**SEUSSR**  *Dest*

---

**Result:** Dest is transformed by relocating and periodically inverting bits. Returns to original value on 32nd iteration.

- Dest is a register to transform.

```{=latex}
\simpleencoding{EEEE}{1101011}{000}{DDDDDDDDD}{001100101}{D}{---}{---}{2}
```

**Related:** [SEUSSF](#seussf)

**Explanation:**

Relocates and periodically inverts bits within Dest using a reverse pattern. The transformation returns to the original value after 32 iterations. This is useful for pseudo-random bit scrambling and data obfuscation, providing the inverse operation of SEUSSF.



## SHL {#shl}

Shift left
[Shift/Rotate Instruction](#shift-rotate-instructions) - Shift bits left, inserting zeros as new rightmost bits.

**SHL**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are shifted left by Src bits, inserting zeros (0) as new rightmost bits.

- Dest is a register containing the value to left shift.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to shift.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0000011}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Last bit out\textsuperscript{1}}{Result = 0}{2}

\textsuperscript{1} C = last bit shifted out if S[4:0] > 0, else D[31]
```

**Related:** [SHR](#shr), [SAL](#sal), [SAR](#sar), [ROL](#rol)

**Explanation:**

SHL shifts the destination's binary value left by the source number of places (0-31 bits) and sets the new LSBs to 0. This is useful for bit-stream manipulation as well as for swift multiplication; signed or unsigned 32-bit integer multiplication by a power-of-two. Care must be taken for power-of-two multiplications since upper bits shift through the MSB (sign bit), mangling large signed values.

::: pasm2
        SHL     value, #2      ' Multiply by 4
:::



## SHR {#shr}

Shift right
[Shift/Rotate Instruction](#shift-rotate-instructions) - Shift bits right, inserting zeros as new leftmost bits.

**SHR**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are shifted right by Src bits, inserting zeros (0) as new leftmost bits.

- Dest is a register containing the value to right shift.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to shift.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0000010}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Last bit out\textsuperscript{1}}{Result = 0}{2}

\textsuperscript{1} C = last bit shifted out if S[4:0] > 0, else D[0]
```

**Related:** [SHL](#shl), [SAR](#sar), [ROR](#ror)

**Explanation:**

SHR shifts the destination's binary value right by the source number of places (0-31 bits) and sets the new MSBs to 0. This is useful for bit-stream manipulation as well as for swift division; unsigned 32-bit integer division by a power-of-two. For similar division of a signed value, use SAR instead.

::: pasm2
        SHR     value, #3      ' Divide unsigned by 8
:::



## SIGNX {#signx}

Sign extend
[Bit Manipulation Instruction](#bit-manipulation-instructions) - Sign-extend a value beyond a designated bit position.

**SIGNX**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The Dest value is sign-extended above the bit indicated by Src and is stored in Dest. Optionally the C and Z flags are updated to the resulting MSB and zero status.

- Dest is a register containing the value to sign-extend above bit Src[4:0] and where the result is written.
- Src is a register or 9-bit literal whose value (lower 5 bits) identifies the bit of Dest to sign-extend beyond.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0111011}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{MSB of result}{Result = 0}{2}
```

**Related:** [ZEROX](#zerox)

**Explanation:**

SIGNX fills the bits of Dest above the bit indicated by Src[4:0] with the value of that identified bit, i.e. sign-extending the value. This is handy when converting encoded or received signed values from a small bit width to a large bit width, i.e. 32 bits.

::: pasm2
        SIGNX   value, #7      ' Sign-extend 8-bit value to 32 bits
:::



## SKIP {#skip}

Skip instructions
[Flow Control Instruction](#flow-control-instructions) - Skip subsequent instructions based on a bitmask.

**SKIP**  *{#}Dest*

---

**Result:** Subsequent instructions 0-31 are cancelled for each '1' bit in Dest[0]-Dest[31].

- Dest is a register or literal value (0-511) containing skip pattern bitmask.

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000110001}{---}{---}{---}{2}
```

**Related:** [SKIPF](#skipf)

**Explanation:**

Skips instructions based on Dest bitmask. Subsequent instructions 0-31 get cancelled for each '1' bit in Dest[0]-Dest[31]. Each set bit causes the corresponding sequential instruction to be cancelled (replaced with NOP).

::: pasm2
        SKIP    #%10101        ' Skip instructions 0, 2, 4
        NOP                    ' Skipped (bit 0)
        ADD     x, #1          ' Executed (bit 1 = 0)
        NOP                    ' Skipped (bit 2)
:::



## SKIPF {#skipf}

Skip instructions fast
[Flow Control Instruction](#flow-control-instructions) - Rapidly skip over instructions by jumping the program counter.

**SKIPF**  *{#}Dest*

---

**Result:** Program counter leaps over cog/LUT instructions based on Dest bitmask.

- Dest is a register or literal value (0-511) containing skip pattern bitmask.

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000110010}{---}{---}{---}{2}
```

**Related:** [SKIP](#skip)

**Explanation:**

Like SKIP, but instead of cancelling instructions, the PC leaps over them. This provides faster execution when skipping multiple instructions, as the skipped instructions are never fetched or executed.



## SPLITB {#splitb}

Split bits to bytes
[Bit Manipulation Instruction](#bit-manipulation-instructions) - Reorganize bits by extracting every 4th bit into separate bytes.

**SPLITB**  *Dest*

---

**Result:** Dest = {Dest[31], Dest[27], Dest[23], Dest[19], ...Dest[12], Dest[8], Dest[4], Dest[0]}.

- Dest is a register to transform.

```{=latex}
\simpleencoding{EEEE}{1101011}{000}{DDDDDDDDD}{001100000}{D}{---}{---}{2}
```

**Related:** [SPLITW](#splitw), [MERGEB](#mergeb)

**Explanation:**

Splits every 4th bit of Dest into bytes. The bits at positions 0, 4, 8, 12, 16, 20, 24, 28 become the new low byte, the bits at positions 1, 5, 9, 13, 17, 21, 25, 29 become the second byte, and so on. This is useful for bit reordering and data unpacking operations.



## SPLITW {#splitw}

Split bits to words
[Bit Manipulation Instruction](#bit-manipulation-instructions) - Reorganize bits by separating odd and even bits into separate words.

**SPLITW**  *Dest*

---

**Result:** Dest = {Dest[31], Dest[29], Dest[27], Dest[25], ...Dest[6], Dest[4], Dest[2], Dest[0]}.

- Dest is a register to transform.

```{=latex}
\simpleencoding{EEEE}{1101011}{000}{DDDDDDDDD}{001100010}{D}{---}{---}{2}
```

**Related:** [SPLITB](#splitb), [MERGEW](#mergew)

**Explanation:**

Splits odd and even bits of Dest into separate words. The even bits (0, 2, 4, ...30) become the low word, and the odd bits (1, 3, 5, ...31) become the high word. This is useful for bit reordering and data unpacking operations.



## STALLI {#stalli}

Disallow interrupts
[Interrupt Instruction](#interrupt-instructions) - Disable interrupt branching to protect critical code sections.

**STALLI**

---

**Result:** All future interrupts are disallowed.

```{=latex}
\simpleencoding{EEEE}{1101011}{000}{000100001}{000100100}{---}{---}{---}{2}
```

**Related:** [ALLOWI](#allowi)

**Explanation:**

STALLI disables interrupt branching. STALLI is the complement of the ALLOWI instruction; both are used to protect short, vital sections of main code from timing jitter or state loss caused by asynchronous interrupt handling.

::: pasm2
        STALLI                 ' Disable interrupts
        ' Critical section...
        ALLOWI                 ' Re-enable interrupts
:::



## SUB {#sub}

Subtract
[Math Instruction](#math-instructions) - Subtract one unsigned value from another.

**SUB**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Difference of unsigned Dest and unsigned Src is stored in Dest and optionally the C and Z flags are updated to the borrow and zero status.

- Dest is a register containing the value to subtract Src from, and where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is subtracted from Dest.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0001100}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Borrow of (D - S)}{Result = 0}{2}
```

**Related:** [SUBX](#subx), [SUBS](#subs), [SUBSX](#subsx), [SUBR](#subr), [ADD](#add)

**Explanation:**

SUB subtracts the unsigned Src from the unsigned Dest and stores the result into the Dest register. To subtract unsigned multi-long values, use SUB followed by SUBX as described in Subtracting Two Multi-Long Values. SUB and SUBX are also used in subtracting signed multi-long values with SUBSX ending the sequence.

::: pasm2
        SUB     count, #1 WZ   ' Decrement count, set Z if zero
:::



## SUBR {#subr}

Subtract reverse
[Math Instruction](#math-instructions) - Subtract the destination from the source (reverse order).

**SUBR**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Difference of unsigned Src and unsigned Dest is stored in Dest and optionally the C and Z flags are updated to the borrow and zero status.

- Dest is a register containing the value to subtract from Src, and where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is subtracted by Dest.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0010110}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Borrow of (S - D)}{Result = 0}{2}
```

**Related:** [SUB](#sub)

**Explanation:**

SUBR subtracts the unsigned Dest from the unsigned Src and stores the result into the Dest register. This is the reverse of the subtraction order of SUB, computing Src - Dest instead of Dest - Src.



## SUBS {#subs}

Subtract signed
[Math Instruction](#math-instructions) - Subtract one signed value from another.

**SUBS**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Difference of signed Dest and signed Src is stored in Dest and optionally the C and Z flags are updated to the sign and zero status.

- Dest is a register containing the value to subtract Src from, and where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is subtracted from Dest.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0001110}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Sign of (D - S)}{Result = 0}{2}
```

**Related:** [SUB](#sub), [SUBX](#subx), [SUBSX](#subsx)

**Explanation:**

SUBS subtracts the signed Src from the signed Dest and stores the result into the Dest register. If Src is a 9-bit literal, its value is interpreted as positive (0-511; it is not sign-extended). Use ##Value (or insert a prior AUGS instruction) for a 32-bit signed value; negative or positive. To subtract signed multi-long values, use SUB (not SUBS) followed possibly by SUBX, and finally SUBSX.



## SUBSX {#subsx}

Subtract signed extended
[Math Instruction](#math-instructions) - Subtract one signed extended value from another using carry.

**SUBSX**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Difference of signed Dest and signed Src (plus C) is stored in Dest and optionally the C and Z flags are updated to the extended sign and zero status.

- Dest is a register containing the value to subtract Src plus C from, and where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value plus C is subtracted from Dest.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0001111}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Sign of D-(S+C)}{Z AND (Result = 0)}{2}
```

**Related:** [SUB](#sub), [SUBX](#subx), [SUBS](#subs)

**Explanation:**

SUBSX subtracts the signed value of Src plus C from the signed Dest and stores the result into the Dest register. The SUBSX instruction is used to perform signed multi-long (extended) subtraction, such as 64-bit subtraction. Use WC or WCZ on preceding SUB and SUBX instructions for proper final C flag. Use WZ or WCZ on preceding SUB and SUBX instructions for proper final Z flag. To subtract signed multi-long values, use SUB (not SUBS) followed possibly by SUBX, and finally SUBSX.



## SUBX {#subx}

Subtract extended
[Math Instruction](#math-instructions) - Subtract one unsigned extended value from another using carry.

**SUBX**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Difference of unsigned Dest and unsigned Src (plus C) is stored in Dest and optionally the C and Z flags are updated to the extended borrow and zero status.

- Dest is a register containing the value to subtract Src plus C from, and where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value plus C is subtracted from Dest.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0001101}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Borrow of (D - (S + C))}{Z AND (result = 0)}{2}
```

**Related:** [SUB](#sub), [SUBSX](#subsx)

**Explanation:**

SUBX subtracts the unsigned value of Src plus C from the unsigned Dest and stores the result into the Dest register. The SUBX instruction is used to perform unsigned multi-long (extended) subtraction, such as 64-bit subtraction. Use WC or WCZ on preceding SUB and SUBX instructions for proper final C flag. If C is set after the last SUBX in a multi-long subtraction, it indicates unsigned underflow. Use WZ or WCZ on preceding SUB and SUBX instructions for proper final Z flag. To subtract unsigned multi-long values, use SUB followed by one or more SUBX instructions.



## SUMC / SUMNC / SUMZ / SUMNZ {#sumc}

Conditional sum {#sumnc} {#sumz} {#sumnz}
[Math Instruction](#math-instructions) - Conditionally add or subtract based on C, NC, Z, or NZ flag.

**SUMC**  *Dest, {#}Src*  **{WC|WZ|WCZ}**
**SUMNC**  *Dest, {#}Src*  **{WC|WZ|WCZ}**
**SUMZ**  *Dest, {#}Src*  **{WC|WZ|WCZ}**
**SUMNZ**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Conditionally adds or subtracts Src from Dest based on flag state:

| Instruction | Subtracts when | Adds when |
|-------------|----------------|-----------|
| SUMC | C = 1 | C = 0 |
| SUMNC | C = 0 | C = 1 |
| SUMZ | Z = 1 | Z = 0 |
| SUMNZ | Z = 0 | Z = 1 |

- Dest is a register containing the value to adjust.
- Src is a register, 9-bit literal, or 32-bit augmented literal.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{0011100}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Sign}{Result = 0}{2}
\encodingrowcont{EEEE}{0011101}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Sign}{Result = 0}{2}
\encodingrowcont{EEEE}{0011110}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Sign}{Result = 0}{2}
\encodingrow{EEEE}{0011111}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{Sign}{Result = 0}{2}
\end{encodingtable}
```

**Explanation:**

These instructions conditionally add or subtract Src from Dest based on the specified flag state. The C flag (with WC) is updated to reflect the correct sign of the result.

SUMC and SUMZ subtract when their flag is set (1). SUMNC and SUMNZ subtract when their flag is clear (0), providing complementary behavior.

