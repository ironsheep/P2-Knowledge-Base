# S Instructions

This section documents all PASM2 instructions beginning with S, organized alphabetically.

## SAL — Shift Arithmetic Left

Shifts the destination register left by the specified number of bits, extending the original LSB into new rightmost positions.

### Syntax
```pasm
        SAL     D, {#}S {WC|WZ|WCZ}
```

### Result
The bits of D are shifted left by S bits, extending D[0] into new rightmost bits.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the value to arithmetically left shift by S bits |
| S | Register or 5-bit literal (0-31) indicating the number of bits to shift left |
| WC/WZ/WCZ | Optional flag effects |

### Encoding
\simpleencoding{EEEE 0000111 CZI DDDDDDDDD SSSSSSSSS | D | Last bit shifted out if S[4:0] > 0, else D[31] | Result = 0 | 2}

### Flags
- **C**: Set to last bit shifted out if S[4:0] > 0, else D[31]
- **Z**: Set if result equals zero

### Related Instructions
- [SAR](#sar--shift-arithmetic-right) — Shift arithmetic right (complement for bit streams)
- [SHL](#shl--shift-left) — Shift left (for power-of-two multiplication)

### Explanation
SAL shifts the destination's binary value left by the source number of places (0-31 bits) and sets the new LSBs to that of the original D[0]. SAL is the complement of SAR for bit streams but not for math operations. For swift 32-bit integer multiplication by a power-of-two, use SHL instead.

---

## SAR — Shift Arithmetic Right

Shifts the destination register right by the specified number of bits, extending the sign bit into new leftmost positions.

### Syntax
```pasm
        SAR     D, {#}S {WC|WZ|WCZ}
```

### Result
The bits of D are shifted right by S bits, extending D[31] (the sign bit) into new leftmost bits.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the value to arithmetically right shift by S bits |
| S | Register or 5-bit literal (0-31) indicating the number of bits to shift right |
| WC/WZ/WCZ | Optional flag effects |

### Encoding
\simpleencoding{EEEE 0000110 CZI DDDDDDDDD SSSSSSSSS | D | Last bit shifted out if S[4:0] > 0, else D[0] | Result = 0 | 2}

### Flags
- **C**: Set to last bit shifted out if S[4:0] > 0, else D[0]
- **Z**: Set if result equals zero

### Related Instructions
- [SAL](#sal--shift-arithmetic-left) — Shift arithmetic left (complement for bit streams)
- [SHR](#shr--shift-right) — Shift right (logical shift)

### Explanation
SAR shifts the destination's binary value right by the source number of places (0-31 bits) and sets the new MSBs to that of the original D[31], preserving the sign of a signed integer. This is useful for bit stream manipulation and for swift division. It is similar to SHR for swift division by a power-of-two, but is safe for both signed and unsigned integers.

---

## SCA — Scale

Multiplies two 16-bit values and scales the result for use in the next instruction.

### Syntax
```pasm
        SCA     D, {#}S {WZ}
```

### Result
The upper 16 bits of the unsigned product from the 16-bit D and S multiplication is substituted as the next instruction's S value.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the 16-bit value to multiply with S |
| S | Register, 9-bit literal, or 16-bit augmented literal to multiply with D |
| WZ | Optional flag effect |

### Encoding
\simpleencoding{EEEE 1010001 0ZI DDDDDDDDD SSSSSSSSS | — | — | Product = 0 | 2}

### Flags
- **C**: No effect
- **Z**: Set if product equals zero (before scaling)

### Related Instructions
- [SCAS](#scas--scale-signed) — Scale signed (similar operation for signed values)

### Explanation
SCA multiplies the lower 16 bits of each of D and S together, right shifts the 32-bit product by 16 (to scale down the result), and substitutes this value as the next instruction's S value. This is useful for creating scaled unsigned 16-bit values for subsequent operations.

---

## SCAS — Scale, Signed

Multiplies two signed 16-bit values and scales the result for use in the next instruction.

### Syntax
```pasm
        SCAS    D, {#}S {WZ}
```

### Result
The upper 18 bits of the signed product from the 16-bit D and S multiplication is substituted as the next instruction's S value.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the signed 16-bit value to multiply with S |
| S | Register, 9-bit literal, or signed 16-bit augmented literal to multiply with D |
| WZ | Optional flag effect |

### Encoding
\simpleencoding{EEEE 1010001 1ZI DDDDDDDDD SSSSSSSSS | — | — | Result = 0 | 2}

### Flags
- **C**: No effect
- **Z**: Set if result equals zero (before scaling)

### Related Instructions
- [SCA](#sca--scale) — Scale (unsigned version)

### Explanation
SCAS multiplies the lower signed 16 bits of each of D and S together, right shifts the 32-bit product by 14 (to scale down the result), and substitutes this value as the next instruction's S value. This is useful for creating scaled signed values for subsequent operations.

---

## SETBYTE — Set Byte

Stores an 8-bit value into a specified byte position within a register.

### Syntax
```pasm
        SETBYTE D, {#}S, #N
        SETBYTE {#}S
```

### Result
S[7:0] is written to byte N (0-3) of D, or to another register byte described by prior ALTSB instruction.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register in which to modify a byte |
| S | Register or 8-bit literal whose bits [7:0] will be stored in the designated location |
| N | 2-bit literal identifying the byte ID (0-3) of D to modify |

### Encoding
\begin{encodingtable}
EEEE 1000110 NNI DDDDDDDDD SSSSSSSSS & D & — & — & 2 \\
EEEE 1000110 00I 000000000 SSSSSSSSS & D† & — & — & 2 \\
\end{encodingtable}

†Dest and target byte ID specified by prior ALTSB instruction.

### Flags
- **C**: No effect
- **Z**: No effect

### Related Instructions
- [ALTSB](#altsb) — Modify next SETBYTE destination
- [SETNIB](#setnib--set-nibble) — Set nibble value
- [SETWORD](#setword--set-word) — Set word value
- [GETBYTE](#getbyte) — Get byte value

### Explanation
SETBYTE stores S[7:0] into the byte identified by N within D, or the byte and register described by a prior ALTSB instruction. No other bits are modified. N (0-3) identifies a value's individual bytes by position in least-significant byte order. The second syntax is intended for use after an ALTSB instruction in a loop to iteratively affect a series of byte values within contiguous long registers.

---

## SETCFRQ — Set Colorspace Converter Frequency

Configures the colorspace converter CFRQ parameter.

### Syntax
```pasm
        SETCFRQ {#}D
```

### Result
The colorspace converter CFRQ parameter is set to D[31:0].

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register or literal value (0-511) to set as CFRQ parameter |

### Encoding
\simpleencoding{EEEE 1101011 00L DDDDDDDDD 000111011 | — | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Explanation
Sets the colorspace converter CFRQ parameter to the value in D. This instruction configures the frequency parameter for the colorspace conversion hardware.

---

## SETCI — Set Colorspace Converter CI

Configures the colorspace converter CI parameter.

### Syntax
```pasm
        SETCI   {#}D
```

### Result
The colorspace converter CI parameter is set to D[31:0].

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register or literal value (0-511) to set as CI parameter |

### Encoding
\simpleencoding{EEEE 1101011 00L DDDDDDDDD 000111001 | — | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Explanation
Sets the colorspace converter CI parameter to the value in D. This instruction configures the CI parameter for the colorspace conversion hardware.

---

## SETCMOD — Set Colorspace Converter Mode

Configures the colorspace converter mode parameter.

### Syntax
```pasm
        SETCMOD {#}D
```

### Result
The colorspace converter CMOD parameter is set to D[8:0].

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register or literal value (0-511) to set as CMOD parameter |

### Encoding
\simpleencoding{EEEE 1101011 00L DDDDDDDDD 000111100 | — | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Explanation
Sets the colorspace converter CMOD parameter to D[8:0]. This instruction configures the mode parameter for the colorspace conversion hardware.

---

## SETCQ — Set Colorspace Converter CQ

Configures the colorspace converter CQ parameter.

### Syntax
```pasm
        SETCQ   {#}D
```

### Result
The colorspace converter CQ parameter is set to D[31:0].

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register or literal value (0-511) to set as CQ parameter |

### Encoding
\simpleencoding{EEEE 1101011 00L DDDDDDDDD 000111010 | — | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Explanation
Sets the colorspace converter CQ parameter to the value in D. This instruction configures the CQ parameter for the colorspace conversion hardware.

---

## SETCY — Set Colorspace Converter CY

Configures the colorspace converter CY parameter.

### Syntax
```pasm
        SETCY   {#}D
```

### Result
The colorspace converter CY parameter is set to D[31:0].

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register or literal value (0-511) to set as CY parameter |

### Encoding
\simpleencoding{EEEE 1101011 00L DDDDDDDDD 000111000 | — | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Explanation
Sets the colorspace converter CY parameter to the value in D. This instruction configures the CY parameter for the colorspace conversion hardware.

---

## SETD — Set Destination Field

Modifies the D field of an instruction template for use with ALTI.

### Syntax
```pasm
        SETD    D, {#}S
```

### Result
The D field [17:9] of template D is set to S[8:0].

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register whose 32-bit value is a template for use with an ALTI instruction |
| S | Register or 9-bit literal whose value (S[8:0]) is copied to the D field of D |

### Encoding
\simpleencoding{EEEE 1001101 10I DDDDDDDDD SSSSSSSSS | D | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Related Instructions
- [SETS](#sets--set-source-field) — Set source field
- [SETR](#setr--set-result-field) — Set result field
- [ALTI](#alti) — Execute instruction from template

### Explanation
SETD copies S[8:0] to the D field of the template D to be used with an ALTI instruction. Bits outside the D field remain unaffected. The D field holds the address of a register (or sometimes a literal value) for the instruction to use as its destination value, and usually as its result destination, during its execution. SETD can also be used in self-modifying register RAM code. Unlike with ALTx instructions, when used this way, field value modification occurs in the program code itself (not the instruction pipeline); code is altered, values persist. Due to the instruction pipeline nature, after modifying a code register, it is necessary to elapse at least two instructions before executing the modified register.

---

## SETDACS — Set DACs

Simultaneously sets all four DAC channels.

### Syntax
```pasm
        SETDACS {#}D
```

### Result
DAC3 = D[31:24], DAC2 = D[23:16], DAC1 = D[15:8], DAC0 = D[7:0].

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register or literal value (0-511) containing four 8-bit DAC values |

### Encoding
\simpleencoding{EEEE 1101011 00L DDDDDDDDD 000011100 | — | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Explanation
Sets all four DAC channels simultaneously from the four bytes in D. DAC3 receives bits [31:24], DAC2 receives bits [23:16], DAC1 receives bits [15:8], and DAC0 receives bits [7:0].

---

## SETINT1 / SETINT2 / SETINT3 — Set Interrupt Source {#setint1}

Configures the interrupt source (1, 2, or 3).

### Syntax
```pasm
        SETINT1 {#}D
        SETINT2 {#}D
        SETINT3 {#}D
```

### Result
The specified interrupt source (INT1, INT2, or INT3) is set to D[3:0].

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register or literal value (0-511) containing interrupt source in bits [3:0] |

### Encoding
| Instruction | Encoding |
|-------------|----------|
| SETINT1 | `EEEE 1101011 00L DDDDDDDDD 000100101` |
| SETINT2 | `EEEE 1101011 00L DDDDDDDDD 000100110` |
| SETINT3 | `EEEE 1101011 00L DDDDDDDDD 000100111` |

**Clocks:** 2

### Flags
- **C**: No effect
- **Z**: No effect

### Related Instructions
- [NIXINT1/2/3](#nixint1) — Cancel interrupt
- [TRGINT1/2/3](#trgint1) — Trigger interrupt
- [RETI0/1/2/3](instructions-r.md#reti0) — Return from interrupt

### Explanation
SETINT1, SETINT2, and SETINT3 configure which event will trigger their respective interrupts. The interrupt source is specified in D[3:0]. The P2 provides three configurable interrupt levels (INT1-INT3), each of which can be independently configured to respond to different event sources.

---

## SETLUTS — Set LUT Sharing

Enables or disables LUT sharing between adjacent cogs.

### Syntax
```pasm
        SETLUTS {#}D
```

### Result
If D[0] = 1, LUT sharing is enabled where LUT writes within the adjacent odd/even companion cog are copied to this cog's LUT.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register or literal value (0-511) with enable bit in D[0] |

### Encoding
\simpleencoding{EEEE 1101011 00L DDDDDDDDD 000110111 | — | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Explanation
Enables or disables LUT sharing based on D[0]. When enabled (D[0] = 1), LUT writes within the adjacent odd/even companion cog are automatically copied to this cog's LUT, allowing cogs to share lookup table data.

---

## SETNIB — Set Nibble

Stores a 4-bit value into a specified nibble position within a register.

### Syntax
```pasm
        SETNIB  D, {#}S, #N
        SETNIB  {#}S
```

### Result
S[3:0] is written to nibble N (0-7) of D, or to another register nibble described by prior ALTSN instruction.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register in which to modify a nibble |
| S | Register or 4-bit literal whose bits [3:0] will be stored in the designated location |
| N | 3-bit literal identifying the nibble ID (0-7) of D to modify |

### Encoding
\begin{encodingtable}
EEEE 100000N NNI DDDDDDDDD SSSSSSSSS & D & — & — & 2 \\
EEEE 1000000 00I 000000000 SSSSSSSSS & D† & — & — & 2 \\
\end{encodingtable}

†Dest and target nibble ID specified by prior ALTSN instruction.

### Flags
- **C**: No effect
- **Z**: No effect

### Related Instructions
- [ALTSN](#altsn) — Modify next SETNIB destination
- [SETBYTE](#setbyte--set-byte) — Set byte value
- [SETWORD](#setword--set-word) — Set word value
- [GETNIB](#getnib) — Get nibble value

### Explanation
SETNIB stores S[3:0] into the nibble identified by N within D, or the nibble and register described by a prior ALTSN instruction. No other bits are modified. N (0-7) identifies a value's individual nibbles by position in least-significant nibble order. The second syntax is intended for use after an ALTSN instruction in a loop to iteratively affect a series of nibble values within contiguous long registers.

---

## SETPAT — Set Pin Pattern

Configures pin pattern matching for PAT event detection.

### Syntax
```pasm
        SETPAT  {#}D, {#}S
```

### Result
Pin pattern for PAT event is configured. C selects INA/INB, Z selects =/!=, D provides mask value, S provides match value.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register or immediate containing mask value |
| S | Register or immediate containing match value |

### Encoding
\simpleencoding{EEEE 1011111 1LI DDDDDDDDD SSSSSSSSS | — | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Explanation
Sets pin pattern for PAT event detection. The C flag selects INA or INB for monitoring, the Z flag selects equality (=) or inequality (!=) matching, D provides the mask value to select which pins to monitor, and S provides the match value to compare against.

---

## SETPIV — Set Pixel Blend Factor

Sets the blend factor for pixel mixing operations.

### Syntax
```pasm
        SETPIV  {#}D
```

### Result
BLNPIX/MIXPIX blend factor is set to D[7:0].

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register or literal value (0-511) containing 8-bit blend factor in bits [7:0] |

### Encoding
\simpleencoding{EEEE 1101011 00L DDDDDDDDD 000111101 | — | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Related Instructions
- [SETPIX](#setpix--set-pixel-mixer-mode) — Set pixel mixer mode

### Explanation
Sets the blend factor for BLNPIX and MIXPIX operations to D[7:0]. This controls the blending ratio for pixel mixing operations.

---

## SETPIX — Set Pixel Mixer Mode

Configures the pixel mixer operating mode.

### Syntax
```pasm
        SETPIX  {#}D
```

### Result
MIXPIX mode is set to D[5:0].

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register or literal value (0-511) containing 6-bit mode in bits [5:0] |

### Encoding
\simpleencoding{EEEE 1101011 00L DDDDDDDDD 000111110 | — | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Related Instructions
- [SETPIV](#setpiv--set-pixel-blend-factor) — Set pixel blend factor

### Explanation
Sets the MIXPIX operating mode to D[5:0]. This configures how the pixel mixer combines pixel values.

---

## SETQ — Set Q Register

Sets the Q register for use by subsequent instructions.

### Syntax
```pasm
        SETQ    {#}D
```

### Result
Q register is set to D.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register or literal value (0-511) to load into Q |

### Encoding
\simpleencoding{EEEE 1101011 00L DDDDDDDDD 000101000 | — | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Related Instructions
- [SETQ2](#setq2--set-q-for-lut-transfers) — Set Q for LUT block transfers

### Explanation
Sets Q register to D. Use before RDLONG/WRLONG/WMLONG to set block transfer count. Also used before MUXQ/COGINIT/QDIV/QFRAC/QROTATE/WAITxxx instructions to provide additional parameters.

---

## SETQ2 — Set Q for LUT Transfers

Sets the Q register for LUT block transfers.

### Syntax
```pasm
        SETQ2   {#}D
```

### Result
Q register is set to D for LUT block transfers.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register or literal value (0-511) to load into Q |

### Encoding
\simpleencoding{EEEE 1101011 00L DDDDDDDDD 000101001 | — | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Related Instructions
- [SETQ](#setq--set-q-register) — Set Q for COG RAM block transfers
- [RDLONG](#rdlong) — Read long(s) from HUB
- [WRLONG](#wrlong) — Write long(s) to HUB
- [RDLUT](#rdlut) — Read from LUT
- [WRLUT](#wrlut) — Write to LUT

### Explanation
Sets Q register to D. Use before RDLONG/WRLONG/WMLONG to set LUT block transfer. SETQ2 enables block transfers to/from LUT RAM instead of COG RAM: SETQ2 + RDLONG performs block read from HUB to LUT, while SETQ2 + WRLONG performs block write from LUT to HUB. This is essential for fast bulk data movement for lookup tables, waveform tables, and large datasets.

---

## SETR — Set Result Field

Modifies the Result field of an instruction template for use with ALTI.

### Syntax
```pasm
        SETR    D, {#}S
```

### Result
The Result field [27:19] of template D is set to S[8:0].

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register whose 32-bit value is a template for use with an ALTI instruction |
| S | Register or 9-bit literal whose value (S[8:0]) is copied to the Result field of D |

### Encoding
\simpleencoding{EEEE 1001101 01I DDDDDDDDD SSSSSSSSS | D | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Related Instructions
- [SETD](#setd--set-destination-field) — Set destination field
- [SETS](#sets--set-source-field) — Set source field
- [ALTI](#alti) — Execute instruction from template

### Explanation
SETR copies S[8:0] to the Result field of the template D to be used with an ALTI instruction. Bits outside the Result field remain unaffected. The Result field does not exist in instruction opcodes, but takes its value from the D field, holding the address of a register for the instruction to use as its result destination upon execution. SETR can also be used in self-modifying register RAM code, though it affects the Instr field and upper two bits of the FX field rather than a non-existent Register field. Unlike with ALTx instructions, when used this way, field value modification occurs in the program code itself (not the instruction pipeline); code is altered, values persist. Due to the instruction pipeline nature, after modifying a code register, it is necessary to elapse at least two instructions before executing the modified register.

---

## SETS — Set Source Field

Modifies the S field of an instruction template for use with ALTI.

### Syntax
```pasm
        SETS    D, {#}S
```

### Result
The S field [8:0] of template D is set to S[8:0].

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register whose 32-bit value is a template for use with an ALTI instruction |
| S | Register or 9-bit literal whose value (S[8:0]) is copied to the S field of D |

### Encoding
\simpleencoding{EEEE 1001101 11I DDDDDDDDD SSSSSSSSS | D | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Related Instructions
- [SETD](#setd--set-destination-field) — Set destination field
- [SETR](#setr--set-result-field) — Set result field
- [ALTI](#alti) — Execute instruction from template

### Explanation
SETS copies S[8:0] to the S field of the template D to be used with an ALTI instruction. Bits outside the S field remain unaffected. The S field holds the address of a register or literal value for an instruction to use as its source value during its execution. SETS can also be used in self-modifying register RAM code. Unlike with ALTx instructions, when used this way, field value modification occurs in the program code itself (not the instruction pipeline); code is altered, values persist. Due to the instruction pipeline nature, after modifying a code register, it is necessary to elapse at least two instructions before executing the modified register.

---

## SETSCP — Set Oscilloscope

Configures the four-channel oscilloscope.

### Syntax
```pasm
        SETSCP  {#}D
```

### Result
Four-channel oscilloscope enable is set to D[6] and input pin base is set to D[5:2].

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register or literal value (0-511) containing enable bit [6] and pin base [5:2] |

### Encoding
\simpleencoding{EEEE 1101011 00L DDDDDDDDD 001110000 | — | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Explanation
Sets the four-channel oscilloscope enable to D[6] and sets the input pin base to D[5:2]. This configures the hardware oscilloscope feature for debugging and signal monitoring.

---

## SETSE1 / SETSE2 / SETSE3 / SETSE4 — Set Selectable Event {#setse1}

Configures selectable event detection (1, 2, 3, or 4).

### Syntax
```pasm
        SETSE1  {#}D
        SETSE2  {#}D
        SETSE3  {#}D
        SETSE4  {#}D
```

### Result
The specified selectable event (SE1, SE2, SE3, or SE4) configuration is set to D[8:0].

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register or literal value (0-511) containing event configuration in bits [8:0] |

### Encoding
| Instruction | Encoding | C | Z | Clocks |
|-------------|----------|---|---|--------|
| SETSE1 | `EEEE 1101011 00L DDDDDDDDD 000100000` | — | — | 2 |
| SETSE2 | `EEEE 1101011 00L DDDDDDDDD 000100001` | — | — | 2 |
| SETSE3 | `EEEE 1101011 00L DDDDDDDDD 000100010` | — | — | 2 |
| SETSE4 | `EEEE 1101011 00L DDDDDDDDD 000100011` | — | — | 2 |

### Flags
- **C**: No effect
- **Z**: No effect

### Related Instructions
- [POLLSE1/2/3/4](#pollse1) — Poll selectable event flag
- [WAITSE1/2/3/4](#waitse1) — Wait for selectable event
- [JSE1/2/3/4](#jse1) — Jump if selectable event set
- [JNSE1/2/3/4](#jnse1) — Jump if selectable event clear

### Explanation
SETSE1, SETSE2, SETSE3, and SETSE4 configure the corresponding selectable event's detection criteria. The D[8:0] operand specifies which condition will trigger the event.

The P2 provides four independent selectable events, each of which can be configured to detect various conditions including pin states, hub operations, CORDIC completion, and other system events. Once configured, these events can be polled with POLLSE1/2/3/4, waited upon with WAITSE1/2/3/4, or used for conditional jumps with JSE1/2/3/4 and JNSE1/2/3/4.

---

## SETWORD — Set Word

Stores a 16-bit value into a specified word position within a register.

### Syntax
```pasm
        SETWORD D, {#}S, #N
        SETWORD {#}S
```

### Result
S[15:0] is written to word N (0-1) of D, or to another register word described by prior ALTSW instruction.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register in which to modify a word |
| S | Register, 9-bit literal, or 16-bit augmented literal whose bits [15:0] will be stored in the designated location |
| N | 1-bit literal identifying the word ID (0-1) of D to modify |

### Encoding
\begin{encodingtable}
EEEE 1001001 0NI DDDDDDDDD SSSSSSSSS & D & — & — & 2 \\
EEEE 1001001 00I 000000000 SSSSSSSSS & D† & — & — & 2 \\
\end{encodingtable}

†Dest and target word ID specified by prior ALTSW instruction.

### Flags
- **C**: No effect
- **Z**: No effect

### Related Instructions
- [ALTSW](#altsw) — Modify next SETWORD destination
- [SETNIB](#setnib--set-nibble) — Set nibble value
- [SETBYTE](#setbyte--set-byte) — Set byte value
- [GETWORD](#getword) — Get word value

### Explanation
SETWORD stores S[15:0] into the word identified by N within D, or the word and register described by a prior ALTSW instruction. No other bits are modified. N (0-1) identifies a value's individual words by position in least-significant word order. The second syntax is intended for use after an ALTSW instruction in a loop to iteratively affect a series of word values within contiguous long registers.

---

## SETXFRQ — Set Streamer Frequency

Sets the streamer NCO frequency.

### Syntax
```pasm
        SETXFRQ {#}D
```

### Result
Streamer NCO frequency is set to D.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register or literal value (0-511) containing frequency value |

### Encoding
\simpleencoding{EEEE 1101011 00L DDDDDDDDD 000011101 | — | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Explanation
Sets the streamer NCO (Numerically Controlled Oscillator) frequency to D. This controls the frequency at which the streamer outputs data.

---

## SEUSSF — Seuss Forward

Relocates and periodically inverts bits within a register using forward pattern.

### Syntax
```pasm
        SEUSSF  D
```

### Result
D is transformed by relocating and periodically inverting bits. Returns to original value on 32nd iteration.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register to transform |

### Encoding
\simpleencoding{EEEE 1101011 000 DDDDDDDDD 001100100 | D | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Related Instructions
- [SEUSSR](#seussr--seuss-reverse) — Seuss reverse (reverse pattern)

### Explanation
Relocates and periodically inverts bits within D using a forward pattern. The transformation returns to the original value after 32 iterations. This is useful for pseudo-random bit scrambling and data obfuscation.

---

## SEUSSR — Seuss Reverse

Relocates and periodically inverts bits within a register using reverse pattern.

### Syntax
```pasm
        SEUSSR  D
```

### Result
D is transformed by relocating and periodically inverting bits. Returns to original value on 32nd iteration.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register to transform |

### Encoding
\simpleencoding{EEEE 1101011 000 DDDDDDDDD 001100101 | D | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Related Instructions
- [SEUSSF](#seussf--seuss-forward) — Seuss forward (forward pattern)

### Explanation
Relocates and periodically inverts bits within D using a reverse pattern. The transformation returns to the original value after 32 iterations. This is useful for pseudo-random bit scrambling and data obfuscation, providing the inverse operation of SEUSSF.

---

## SHL — Shift Left

Shifts the destination register left by the specified number of bits, inserting zeros as new rightmost bits.

### Syntax
```pasm
        SHL     D, {#}S {WC|WZ|WCZ}
```

### Result
The bits of D are shifted left by S bits, inserting zeros (0) as new rightmost bits.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the value to left shift by S bits |
| S | Register or 5-bit literal (0-31) indicating the number of bits to shift left |
| WC/WZ/WCZ | Optional flag effects |

### Encoding
\simpleencoding{EEEE 0000011 CZI DDDDDDDDD SSSSSSSSS | D | Last bit shifted out if S[4:0] > 0, else D[31] | Result = 0 | 2}

### Flags
- **C**: Set to last bit shifted out if S[4:0] > 0, else D[31]
- **Z**: Set if result equals zero

### Related Instructions
- [SAL](#sal--shift-arithmetic-left) — Shift arithmetic left
- [SHR](#shr--shift-right) — Shift right

### Explanation
SHL shifts the destination's binary value left by the source number of places (0-31 bits) and sets the new LSBs to 0. This is useful for bit-stream manipulation as well as for swift multiplication; signed or unsigned 32-bit integer multiplication by a power-of-two. Care must be taken for power-of-two multiplications since upper bits shift through the MSB (sign bit), mangling large signed values.

---

## SHR — Shift Right

Shifts the destination register right by the specified number of bits, inserting zeros as new leftmost bits.

### Syntax
```pasm
        SHR     D, {#}S {WC|WZ|WCZ}
```

### Result
The bits of D are shifted right by S bits, inserting zeros (0) as new leftmost bits.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the value to right shift by S bits |
| S | Register or 5-bit literal (0-31) indicating the number of bits to shift right |
| WC/WZ/WCZ | Optional flag effects |

### Encoding
\simpleencoding{EEEE 0000010 CZI DDDDDDDDD SSSSSSSSS | D | Last bit shifted out if S[4:0] > 0, else D[0] | Result = 0 | 2}

### Flags
- **C**: Set to last bit shifted out if S[4:0] > 0, else D[0]
- **Z**: Set if result equals zero

### Related Instructions
- [SAR](#sar--shift-arithmetic-right) — Shift arithmetic right (preserves sign)
- [SHL](#shl--shift-left) — Shift left

### Explanation
SHR shifts the destination's binary value right by the source number of places (0-31 bits) and sets the new MSBs to 0. This is useful for bit-stream manipulation as well as for swift division; unsigned 32-bit integer division by a power-of-two. For similar division of a signed value, use SAR instead.

---

## SIGNX — Sign Extend

Sign-extends a value beyond a designated bit position.

### Syntax
```pasm
        SIGNX   D, {#}S {WC|WZ|WCZ}
```

### Result
The D value is sign-extended above the bit indicated by S and is stored in D. Optionally the C and Z flags are updated to the resulting MSB and zero status.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the value to sign-extend above bit S[4:0] and where the result is written |
| S | Register or 9-bit literal whose value (lower 5 bits) identifies the bit of D to sign-extend beyond |
| WC/WZ/WCZ | Optional flag effects |

### Encoding
\simpleencoding{EEEE 0111011 CZI DDDDDDDDD SSSSSSSSS | D | MSB of result | Result = 0 | 2}

### Flags
- **C**: Set to MSB of result
- **Z**: Set if result equals zero

### Related Instructions
- [ZEROX](#zerox) — Zero extend

### Explanation
SIGNX fills the bits of D above the bit indicated by S[4:0] with the value of that identified bit, i.e. sign-extending the value. This is handy when converting encoded or received signed values from a small bit width to a large bit width, i.e. 32 bits.

---

## SKIP — Skip Instructions

Skips subsequent instructions based on a bitmask.

### Syntax
```pasm
        SKIP    {#}D
```

### Result
Subsequent instructions 0-31 are cancelled for each '1' bit in D[0]-D[31].

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register or literal value (0-511) containing skip pattern bitmask |

### Encoding
\simpleencoding{EEEE 1101011 00L DDDDDDDDD 000110001 | — | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Related Instructions
- [SKIPF](#skipf--skip-instructions-fast) — Skip instructions fast (jumps over instead of cancelling)

### Explanation
Skips instructions based on D bitmask. Subsequent instructions 0-31 get cancelled for each '1' bit in D[0]-D[31]. Each set bit causes the corresponding sequential instruction to be cancelled (replaced with NOP).

---

## SKIPF — Skip Instructions Fast

Rapidly skips over instructions by jumping the program counter.

### Syntax
```pasm
        SKIPF   {#}D
```

### Result
Program counter leaps over cog/LUT instructions based on D bitmask.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register or literal value (0-511) containing skip pattern bitmask |

### Encoding
\simpleencoding{EEEE 1101011 00L DDDDDDDDD 000110010 | — | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Related Instructions
- [SKIP](#skip--skip-instructions) — Skip instructions (cancels instead of jumping)

### Explanation
Like SKIP, but instead of cancelling instructions, the PC leaps over them. This provides faster execution when skipping multiple instructions, as the skipped instructions are never fetched or executed.

---

## SPLITB — Split Bits to Bytes

Reorganizes bits by extracting every 4th bit into separate bytes.

### Syntax
```pasm
        SPLITB  D
```

### Result
D = {D[31], D[27], D[23], D[19], ...D[12], D[8], D[4], D[0]}.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register to transform |

### Encoding
\simpleencoding{EEEE 1101011 000 DDDDDDDDD 001100000 | D | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Related Instructions
- [SPLITW](#splitw--split-bits-to-words) — Split odd/even bits to words

### Explanation
Splits every 4th bit of D into bytes. The bits at positions 0, 4, 8, 12, 16, 20, 24, 28 become the new low byte, the bits at positions 1, 5, 9, 13, 17, 21, 25, 29 become the second byte, and so on. This is useful for bit reordering and data unpacking operations.

---

## SPLITW — Split Bits to Words

Reorganizes bits by separating odd and even bits into separate words.

### Syntax
```pasm
        SPLITW  D
```

### Result
D = {D[31], D[29], D[27], D[25], ...D[6], D[4], D[2], D[0]}.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register to transform |

### Encoding
\simpleencoding{EEEE 1101011 000 DDDDDDDDD 001100010 | D | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Related Instructions
- [SPLITB](#splitb--split-bits-to-bytes) — Split every 4th bit to bytes

### Explanation
Splits odd and even bits of D into separate words. The even bits (0, 2, 4, ...30) become the low word, and the odd bits (1, 3, 5, ...31) become the high word. This is useful for bit reordering and data unpacking operations.

---

## STALLI — Disallow Interrupts

Disables interrupt branching to protect critical code sections.

### Syntax
```pasm
        STALLI
```

### Result
All future interrupts are disallowed.

### Parameters
None.

### Encoding
\simpleencoding{EEEE 1101011 000 000100001 000100100 | — | — | — | 2}

### Flags
- **C**: No effect
- **Z**: No effect

### Related Instructions
- [ALLOWI](#allowi) — Allow interrupts (complement instruction)

### Explanation
STALLI disables interrupt branching. STALLI is the complement of the ALLOWI instruction; both are used to protect short, vital sections of main code from timing jitter or state loss caused by asynchronous interrupt handling.

---

## SUB — Subtract

Subtracts one unsigned value from another.

### Syntax
```pasm
        SUB     D, {#}S {WC|WZ|WCZ}
```

### Result
Difference of unsigned D and unsigned S is stored in D and optionally the C and Z flags are updated to the borrow and zero status.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the value to subtract S from, and where the result is written |
| S | Register, 9-bit literal, or 32-bit augmented literal whose value is subtracted from D |
| WC/WZ/WCZ | Optional flag effects |

### Encoding
\simpleencoding{EEEE 0001100 CZI DDDDDDDDD SSSSSSSSS | D | Borrow of (D - S) | Result = 0 | 2}

### Flags
- **C**: Set if unsigned borrow (underflow) occurs
- **Z**: Set if result equals zero

### Related Instructions
- [SUBX](#subx--subtract-extended) — Subtract extended (for multi-long subtraction)
- [SUBS](#subs--subtract-signed) — Subtract signed
- [SUBSX](#subsx--subtract-signed-extended) — Subtract signed extended
- [SUBR](#subr--subtract-reverse) — Subtract reverse

### Explanation
SUB subtracts the unsigned S from the unsigned D and stores the result into the D register. To subtract unsigned multi-long values, use SUB followed by SUBX as described in Subtracting Two Multi-Long Values. SUB and SUBX are also used in subtracting signed multi-long values with SUBSX ending the sequence.

---

## SUBR — Subtract Reverse

Subtracts the destination from the source (reverse order).

### Syntax
```pasm
        SUBR    D, {#}S {WC|WZ|WCZ}
```

### Result
Difference of unsigned S and unsigned D is stored in D and optionally the C and Z flags are updated to the borrow and zero status.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the value to subtract from S, and where the result is written |
| S | Register, 9-bit literal, or 32-bit augmented literal whose value is subtracted by D |
| WC/WZ/WCZ | Optional flag effects |

### Encoding
\simpleencoding{EEEE 0010110 CZI DDDDDDDDD SSSSSSSSS | D | Borrow of (S - D) | Result = 0 | 2}

### Flags
- **C**: Set if unsigned borrow (underflow) occurs
- **Z**: Set if result equals zero

### Related Instructions
- [SUB](#sub--subtract) — Subtract (normal order)

### Explanation
SUBR subtracts the unsigned D from the unsigned S and stores the result into the D register. This is the reverse of the subtraction order of SUB, computing S - D instead of D - S.

---

## SUBS — Subtract Signed

Subtracts one signed value from another.

### Syntax
```pasm
        SUBS    D, {#}S {WC|WZ|WCZ}
```

### Result
Difference of signed D and signed S is stored in D and optionally the C and Z flags are updated to the sign and zero status.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the value to subtract S from, and where the result is written |
| S | Register, 9-bit literal, or 32-bit augmented literal whose value is subtracted from D |
| WC/WZ/WCZ | Optional flag effects |

### Encoding
\simpleencoding{EEEE 0001110 CZI DDDDDDDDD SSSSSSSSS | D | Sign of (D - S) | Result = 0 | 2}

### Flags
- **C**: Set to sign of result (1 if negative)
- **Z**: Set if result equals zero

### Related Instructions
- [SUB](#sub--subtract) — Subtract unsigned
- [SUBX](#subx--subtract-extended) — Subtract extended
- [SUBSX](#subsx--subtract-signed-extended) — Subtract signed extended

### Explanation
SUBS subtracts the signed S from the signed D and stores the result into the D register. If S is a 9-bit literal, its value is interpreted as positive (0-511; it is not sign-extended). Use ##Value (or insert a prior AUGS instruction) for a 32-bit signed value; negative or positive. To subtract signed multi-long values, use SUB (not SUBS) followed possibly by SUBX, and finally SUBSX.

---

## SUBSX — Subtract Signed, Extended

Subtracts one signed extended value from another using carry.

### Syntax
```pasm
        SUBSX   D, {#}S {WC|WZ|WCZ}
```

### Result
Difference of signed D and signed S (plus C) is stored in D and optionally the C and Z flags are updated to the extended sign and zero status.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the value to subtract S plus C from, and where the result is written |
| S | Register, 9-bit literal, or 32-bit augmented literal whose value plus C is subtracted from D |
| WC/WZ/WCZ | Optional flag effects |

### Encoding
\simpleencoding{EEEE 0001111 CZI DDDDDDDDD SSSSSSSSS | D | Sign of D-(S+C) | Z AND (Result = 0) | 2}

### Flags
- **C**: Set to sign of D-(S+C) (1 if negative)
- **Z**: Set if Z was previously set AND result equals zero

### Related Instructions
- [SUB](#sub--subtract) — Subtract
- [SUBX](#subx--subtract-extended) — Subtract extended
- [SUBS](#subs--subtract-signed) — Subtract signed

### Explanation
SUBSX subtracts the signed value of S plus C from the signed D and stores the result into the D register. The SUBSX instruction is used to perform signed multi-long (extended) subtraction, such as 64-bit subtraction. Use WC or WCZ on preceding SUB and SUBX instructions for proper final C flag. Use WZ or WCZ on preceding SUB and SUBX instructions for proper final Z flag. To subtract signed multi-long values, use SUB (not SUBS) followed possibly by SUBX, and finally SUBSX.

---

## SUBX — Subtract Extended

Subtracts one unsigned extended value from another using carry.

### Syntax
```pasm
        SUBX    D, {#}S {WC|WZ|WCZ}
```

### Result
Difference of unsigned D and unsigned S (plus C) is stored in D and optionally the C and Z flags are updated to the extended borrow and zero status.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the value to subtract S plus C from, and where the result is written |
| S | Register, 9-bit literal, or 32-bit augmented literal whose value plus C is subtracted from D |
| WC/WZ/WCZ | Optional flag effects |

### Encoding
\simpleencoding{EEEE 0001101 CZI DDDDDDDDD SSSSSSSSS | D | Borrow of (D - (S + C)) | Z AND (result = 0) | 2}

### Flags
- **C**: Set if unsigned borrow occurs in D-(S+C)
- **Z**: Set if Z was previously set AND result equals zero

### Related Instructions
- [SUB](#sub--subtract) — Subtract
- [SUBSX](#subsx--subtract-signed-extended) — Subtract signed extended

### Explanation
SUBX subtracts the unsigned value of S plus C from the unsigned D and stores the result into the D register. The SUBX instruction is used to perform unsigned multi-long (extended) subtraction, such as 64-bit subtraction. Use WC or WCZ on preceding SUB and SUBX instructions for proper final C flag. If C is set after the last SUBX in a multi-long subtraction, it indicates unsigned underflow. Use WZ or WCZ on preceding SUB and SUBX instructions for proper final Z flag. To subtract unsigned multi-long values, use SUB followed by one or more SUBX instructions.

---

## SUMC — Sum by Carry

Conditionally adds or subtracts based on the C flag.

### Syntax
```pasm
        SUMC    D, {#}S {WC|WZ|WCZ}
```

### Result
If C = 1 then D = D - S, else D = D + S. C is set to correct sign of result.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the value to adjust |
| S | Register or immediate value to add or subtract |
| WC/WZ/WCZ | Optional flag effects |

### Encoding
\simpleencoding{EEEE 0011100 CZI DDDDDDDDD SSSSSSSSS | D | Correct sign of (D +/- S) | Result = 0 | 2}

### Flags
- **C**: Set to correct sign of result (D +/- S)
- **Z**: Set if result equals zero

### Related Instructions
- [SUMNC](#sumnc--sum-by-negated-carry) — Sum by negated carry
- [SUMZ](#sumz--sum-by-zero) — Sum by zero flag
- [SUMNZ](#sumnz--sum-by-negated-zero) — Sum by negated zero flag

### Explanation
Adjusts D by adding or subtracting S based on the C flag. If C = 1 then D = D - S, otherwise D = D + S. The C flag is updated to the correct sign of the result (D +/- S).

---

## SUMNC — Sum by Negated Carry

Conditionally adds or subtracts based on the negated C flag.

### Syntax
```pasm
        SUMNC   D, {#}S {WC|WZ|WCZ}
```

### Result
The sum of signed D and either S or -S (according to !C) is stored in D and optionally the C and Z flags are updated to the sign and zero status.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the signed value to adjust by S or -S, and where the result is written |
| S | Register, 9-bit literal, or 32-bit augmented literal whose value or negated value is added into D |
| WC/WZ/WCZ | Optional flag effects |

### Encoding
\simpleencoding{EEEE 0011101 CZI DDDDDDDDD SSSSSSSSS | D | Correct sign of (D +/- S) | Result = 0 | 2}

### Flags
- **C**: Set to correct sign of result (D +/- S)
- **Z**: Set if result equals zero

### Related Instructions
- [SUMC](#sumc--sum-by-carry) — Sum by carry
- [SUMZ](#sumz--sum-by-zero) — Sum by zero flag
- [SUMNZ](#sumnz--sum-by-negated-zero) — Sum by negated zero flag

### Explanation
SUMNC adjusts the signed D value by S or -S (depending on !C) and stores the result into the D register. If !C is true (C=0), D = D - S. If !C is false (C=1), D = D + S.

---

## SUMNZ — Sum by Negated Zero

Conditionally adds or subtracts based on the negated Z flag.

### Syntax
```pasm
        SUMNZ   D, {#}S {WC|WZ|WCZ}
```

### Result
The sum of signed D and either S or -S (according to !Z) is stored in D and optionally the C and Z flags are updated to the sign and zero status.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the signed value to adjust by S or -S, and where the result is written |
| S | Register, 9-bit literal, or 32-bit augmented literal whose value or negated value is added into D |
| WC/WZ/WCZ | Optional flag effects |

### Encoding
\simpleencoding{EEEE 0011111 CZI DDDDDDDDD SSSSSSSSS | D | Correct sign of (D +/- S) | Result = 0 | 2}

### Flags
- **C**: Set to correct sign of result (D +/- S)
- **Z**: Set if result equals zero

### Related Instructions
- [SUMC](#sumc--sum-by-carry) — Sum by carry
- [SUMNC](#sumnc--sum-by-negated-carry) — Sum by negated carry
- [SUMZ](#sumz--sum-by-zero) — Sum by zero flag

### Explanation
SUMNZ adjusts the signed D value by S or -S (depending on !Z) and stores the result into the D register. If !Z is true (Z=0), D = D - S. If !Z is false (Z=1), D = D + S.

---

## SUMZ — Sum by Zero

Conditionally adds or subtracts based on the Z flag.

### Syntax
```pasm
        SUMZ    D, {#}S {WC|WZ|WCZ}
```

### Result
If Z = 1 then D = D - S, else D = D + S. C is set to correct sign of result.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the value to adjust |
| S | Register or immediate value to add or subtract |
| WC/WZ/WCZ | Optional flag effects |

### Encoding
\simpleencoding{EEEE 0011110 CZI DDDDDDDDD SSSSSSSSS | D | Correct sign of (D +/- S) | Result = 0 | 2}

### Flags
- **C**: Set to correct sign of result (D +/- S)
- **Z**: Set if result equals zero

### Related Instructions
- [SUMC](#sumc--sum-by-carry) — Sum by carry
- [SUMNC](#sumnc--sum-by-negated-carry) — Sum by negated carry
- [SUMNZ](#sumnz--sum-by-negated-zero) — Sum by negated zero flag

### Explanation
Adjusts D by adding or subtracting S based on the Z flag. If Z = 1 then D = D - S, otherwise D = D + S. The C flag is updated to the correct sign of the result (D +/- S).
