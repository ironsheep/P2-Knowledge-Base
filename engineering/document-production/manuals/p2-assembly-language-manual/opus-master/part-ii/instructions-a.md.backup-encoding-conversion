# Instructions: A

This section contains all PASM2 instructions beginning with the letter A.



## ABS {#abs}

Absolute
[Math and Logic](#math-and-logic) - Get the absolute value of a number.

**ABS**  *Dest, {#}Src*  **{WC|WZ|WCZ}**
**ABS**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** Absolute Src (or Dest) value is stored in Dest.

- Dest is the register in which to write the absolute value of Dest or Src.
- Src is an optional register, 9-bit literal, or 32-bit augmented literal whose absolute value is written to Dest.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{0110010}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{S[31]}{Result = 0}{2}
\encodingrow{EEEE}{0110010}{CZ0}{DDDDDDDDD}{DDDDDDDDD}{D}{D[31]}{Result = 0}{2}
\end{encodingtable}
```

**Related:** [NEG](#neg)

**Explanation:**

ABS determines the absolute value of Src or Dest and writes the result into Dest. The first syntax form computes the absolute value of Src, while the second syntax form (without Src) computes the absolute value of Dest itself.

If the WC or WCZ effect is specified, the C flag is set (1) if the original Src or Dest value was negative (the sign bit was 1), or is cleared (0) if it was positive. This preserves information about the original sign of the value.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result is zero, or is cleared (0) if it is non-zero.

Literal Src values are zero-extended, so ABS is best used with register Src (or augmented Src) values for meaningful signed operations.



## ADD {#add}

Add
[Math and Logic](#math-and-logic) - Add two unsigned values.

**ADD**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Sum of unsigned Src and unsigned Dest is stored in Dest.

- Dest is a register containing the value to add Src to, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is added into Dest.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0001000}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{carry of (D + S)}{Result = 0}{2}
```

**Related:** [ADDX](#addx), [ADDS](#adds), [ADDSX](#addsx), [SUB](#sub)

**Explanation:**

ADD sums the two unsigned values of Dest and Src together and stores the result into the Dest register.

If the WC or WCZ effect is specified, the C flag is set (1) if the summation results in a 32-bit overflow (unsigned carry), or is cleared (0) if no overflow. This indicates that the result exceeded the maximum unsigned 32-bit value of $FFFF_FFFF.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result of Dest + Src equals zero, or is cleared (0) if it is non-zero.

To add unsigned multi-long values (64-bit or larger), use ADD for the least significant long, then ADDX for each subsequent long. ADDX carries the overflow from the previous addition into the current one. For example, to add two 64-bit values:

```pasm
        add     value_lo, addend_lo  wc    ' Add low longs, capture carry
        addx    value_hi, addend_hi        ' Add high longs with carry-in
```

ADD and ADDX are also used for adding signed multi-long values, with ADDSX ending the sequence to properly handle sign extension.



## ADDCT1 / ADDCT2 / ADDCT3 {#addct1}

Add and set counter event trigger (1, 2, or 3)
[Event](#event) - Set CTn counter event trigger time.

**ADDCT1**  *Dest, {#}Src*
**ADDCT2**  *Dest, {#}Src*
**ADDCT3**  *Dest, {#}Src*

---

**Result:** The Src value is added into Dest and the result is also stored in the hidden CTn event trigger register.

- Dest is a register containing the value to add Src to, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is added into Dest.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1010011}{00I}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{2}
\encodingrowcont{EEEE}{1010011}{01I}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{2}
\encodingrow{EEEE}{1010011}{10I}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{2}
\end{encodingtable}
```

**Related:** [POLLCT1/2/3](#pollct1), [WAITCT1/2/3](#waitct1), [JCT1/2/3](#jct1), [JNCT1/2/3](#jnct1)

**Explanation:**

ADDCT1, ADDCT2, and ADDCT3 set their respective hidden counter event trigger registers to the value of Dest + Src. The result is also written to Dest. These instructions are used to schedule time-based events that will trigger when the System Counter (CT) reaches the specified value.

The P2 provides three independent counter event triggers (CT1, CT2, CT3), allowing a cog to manage multiple simultaneous time-based operations. Use the corresponding POLLCTn, WAITCTn, JCTn, and JNCTn instructions to process each counter's time-based events. This enables precise timing control for periodic operations, delays, and synchronized activities.



## ADDPIX {#addpix}

Add pixels
[Pixel Mixer](#pixel-mixer) - Add RGB colors with full saturation.

**ADDPIX**  *Dest, {#}Src*

---

**Result:** Src color value bytes are added into Dest color value bytes with full saturation.

- Dest is a register containing the RGB color value to add Src to, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose RGB color value bytes are added into Dest.

```{=latex}
\simpleencoding{EEEE}{1010010}{00I}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{7}
```

**Related:** [SUBPIX](#subpix), [MULPIX](#mulpix), [BLNPIX](#blnpix)

**Explanation:**

ADDPIX sums individual RGB (red, green, blue) color values of Src into that of Dest and stores the result in the Dest register. Each byte is treated as a separate color channel and is saturated to prevent wraparound.

Saturation means that if the sum of a color channel exceeds 255, the result is clamped to 255 rather than wrapping around to a low value. This prevents color distortion when combining bright colors and produces visually correct results for color blending operations.

The instruction processes all three color channels (and alpha if present) in parallel, completing in 7 clock cycles.



## ADDS {#adds}

Add signed
[Math and Logic](#math-and-logic) - Add two signed values.

**ADDS**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Sum of signed Src and signed Dest is stored in Dest.

- Dest is a register containing the value to add Src to, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is added into Dest.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0001010}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{sign of (D + S)}{Result = 0}{2}
```

**Related:** [ADD](#add), [ADDX](#addx), [ADDSX](#addsx), [SUBS](#subs)

**Explanation:**

ADDS sums the two signed values of Dest and Src together and stores the result into the Dest register.

If Src is a 9-bit literal, its value is interpreted as positive (0-511; it is not sign-extended). Use ##Value (or insert a prior AUGS instruction) for a 32-bit signed value, negative or positive.

If the WC or WCZ effect is specified, the C flag is set (1) if the summation results in a signed overflow (signed carry), or is cleared (0) if no overflow. Signed overflow occurs when the result cannot be represented in 32 bits using two's complement notation.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result of Dest + Src is zero, or is cleared (0) if it is non-zero.

To add signed multi-long values, use ADD (not ADDS) followed possibly by ADDX, and finally ADDSX as the last operation to properly handle sign extension.



## ADDSX {#addsx}

Add signed, extended
[Math and Logic](#math-and-logic) - Add two signed extended values.

**ADDSX**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Sum of signed Src plus C and signed Dest is stored in Dest.

- Dest is a register containing the value to add Src plus C to, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value plus C is added into Dest.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0001011}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{sign of (D+S+C)}{Z AND (Result = 0)}{2}
```

**Related:** [ADD](#add), [ADDX](#addx), [ADDS](#adds), [SUBSX](#subsx)

**Explanation:**

ADDSX sums the signed values of Dest and Src plus C together and stores the result into the Dest register. The ADDSX instruction is used to perform signed multi-long (extended) addition, such as 64-bit addition.

If the WC or WCZ effect is specified, the C flag is set (1) if the result is negative (Result[31] = 1), or is cleared (0) if positive. Use WC or WCZ on preceding ADD and ADDX instructions for proper final C flag state.

If the WZ or WCZ effect is specified, the Z flag is set (1) if Z was previously set and the result of Dest + Src + C is zero, or it is cleared (0) if non-zero. Use WZ or WCZ on preceding ADD and ADDX instructions for proper final Z flag state. This allows detection of a zero result across the entire multi-long value.

To add signed multi-long values, use ADD (not ADDS) followed possibly by ADDX, and finally ADDSX as the last operation. ADDSX properly handles the sign extension for the most significant portion of the multi-long value.



## ADDX {#addx}

Add extended
[Math and Logic](#math-and-logic) - Add two unsigned extended values.

**ADDX**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Sum of unsigned Src plus C and unsigned Dest is stored in Dest.

- Dest is a register containing the value to add Src plus C to, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value plus C is added into Dest.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0001001}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{carry of (D + S + C)}{Z AND (Result = 0)}{2}
```

**Related:** [ADD](#add), [ADDS](#adds), [ADDSX](#addsx), [SUBX](#subx)

**Explanation:**

ADDX sums the unsigned values of Dest and Src plus C together and stores the result into the Dest register. The ADDX instruction is used to perform unsigned multi-long (extended) addition, such as 64-bit addition.

If the WC or WCZ effect is specified, the C flag is set (1) if the summation resulted in an unsigned carry, or is cleared (0) if no carry. Use WC or WCZ on preceding ADD and ADDX instructions for proper final C flag state. If C is set after the last ADDX in a multi-long addition, it indicates unsigned overflow.

If the WZ or WCZ effect is specified, the Z flag is set (1) if Z was previously set and the result of Dest + Src + C is zero, or it is cleared (0) if non-zero. Use WZ or WCZ on preceding ADD and ADDX instructions for proper final Z flag state. This allows detection of a zero result across the entire multi-long value.

To add unsigned multi-long values, use ADD followed by one or more ADDX instructions. Each ADDX carries the overflow from the previous addition into the current one.



## AKPIN {#akpin}

Acknowledge pin
[Smart Pin](#smart-pin) - Acknowledge smart pin(s).

**AKPIN**  *{#}Src*

---

**Result:** One or more Smart Pins is acknowledged; lowering their corresponding IN signal(s).

- Src is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the Smart Pin(s) to acknowledge.

```{=latex}
\simpleencoding{EEEE}{1100000}{01I}{000000001}{SSSSSSSSS}{Ack Bus}{---}{---}{2}
```

**Related:** [WRPIN](#wrpin), [WXPIN](#wxpin), [WYPIN](#wypin), [RDPIN](#rdpin)

**Explanation:**

AKPIN acknowledges the Smart Pin(s) designated by Src. This lowers the corresponding IN signal(s) so that future Smart Pin events may raise them again later.

Src[5:0] indicates the pin number (0-63). For a range of Smart Pins, Src[5:0] indicates the first pin number (0-63) and Src[10:6] indicates how many contiguous pins beyond the first should be affected (1-31).

A 9-bit literal Src is enough to express the starting pin (Src[5:0]) and a range of up to 8 contiguous pins (Src[8:6]). If needed, use the augmented literal feature (##Src) to augment Src to the required 11-bit literal value, which automatically inserts an AUGS instruction prior.

When Src is a register, the register's value bits [10:0] are used as-is to form the 11-bit Smart Pin range, unless a SETQ instruction immediately precedes the AKPIN instruction; in that case, SETQ's Dest[4:0] substitutes for value bits[10:6] for AKPIN's use.

The range calculation (from Src[5:0] up to Src[5:0]+Src[10:6]) wraps within the same 32-pin group (DIRA or DIRB); it will not cross the port boundary.



## ALLOWI {#allowi}

Allow interrupts
[Interrupt](#interrupt) - Allow interrupts.

```
ALLOWI
```

**Result:** Any stalled and future interrupts are allowed.

```{=latex}
\simpleencoding{EEEE}{1101011}{000}{000100000}{000100100}{---}{---}{---}{2}
```

**Related:** [STALLI](#stalli)

**Explanation:**

ALLOWI re-enables interrupt branching; the default on COG start. ALLOWI is the complement of the STALLI instruction. Both are used to protect short, vital sections of main code from timing jitter or state loss caused by asynchronous interrupt handling.

When ALLOWI is executed, any interrupts that were stalled by a previous STALLI instruction are allowed to proceed, and future interrupts are also enabled. This allows the COG to respond to interrupt events normally.



## ALTB {#altb}

Alter bit
[Register Indirection](#register-indirection) - Alter subsequent BITxxx instruction.

**ALTB**  *Dest, {#}Src*
**ALTB**  *Dest*

---

**Result:** The next instruction's pipelined Dest value is altered to be (Src + Dest[13:5]) & $1FF, or just Dest[13:5] for syntax 2.

- Dest is the register whose 14-bit value is the index, or the full bit address, for the BITxxx instruction to operate on.
- Src is an optional register, 9-bit literal, or 18-bit augmented literal whose value contains a base long address (Src[8:0]; added to index (Dest[13:5]) for BITxxx) and also an optional auto-indexer value (Src[17:9]; added to Dest at the end of execution).

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1001100}{11I}{DDDDDDDDD}{SSSSSSSSS}{D\textsuperscript{1}}{---}{---}{2}
\encodingrow{EEEE}{1001100}{111}{DDDDDDDDD}{000000000}{D\textsuperscript{1}}{---}{---}{2}
\end{encodingtable}

\textsuperscript{1} Dest is post-adjusted by the auto-indexer value; the sign-extended Src[17:9]. In syntax 2, the auto-indexer value is 0.
```

**Related:** [ALTD](#altd), [ALTS](#alts), [ALTR](#altr), [ALTI](#alti)

**Explanation:**

ALTB should be followed by a BITxxx instruction. It modifies the BITxxx instruction's Dest value, enabling code to iterate through multiple bits of data across a range of register RAM.

BITxxx's Dest value is changed to (Src + Dest[13:5]) & $1FF (for syntax 1), or to Dest[13:5] (for syntax 2). Dest[13:5] corresponds to the target long register's 9-bit address and Dest[4:0] is the bit ID within it; values of 0-31 identify individual bits, by position, in least-significant bit order.

Iteratively executing ALTB followed by a BITxxx instruction, and each time incrementing ALTB's 14-bit Dest value by one, effectively writes a stream of bit values to register RAM as if it were all made of bit-sized registers.

Warning: BITxxx instructions optionally operate on a range of bits, encoded in the Src value. They don't limit themselves to only reading Src[4:0] for the bit number. For this reason, care must be taken when using ALTB with BITxxx or the index value (often used for the Src of the altered instruction) will be misinterpreted as multiple bits to affect. One way to solve this is to use a SETQ #0 followed by the ALTB then BITxxx instructions to force BITxxx's Src[9:5] bits to 0; that is, no extra bits beyond the single bit described by Src[4:0].

In syntax 1, Src consists of two 9-bit fields: a base address (Src[8:0]) and a signed auto-indexer (Src[17:9]). The base is the register RAM address where the series of bits begins. ALTB adds the long index (Dest[13:5]) to the base (Src[8:0]) to locate the register holding the target bit. The bit ID (Dest[4:0]) identifies the bit's position within that long register. At the end of ALTB execution, the optional auto-indexer value (usually 0, 1, or -1) is added to the 14-bit index (Dest) for a future ALTB+BITxxx iteration.

In syntax 2, Dest serves as the full bit address. It is the same format as in syntax 1, but represents the target long's absolute address and its bit index instead of the long's relative index (to add to a base) and bit index.

The instruction following ALTB is shielded from interrupt. Field value modification occurs in the instruction pipeline only; code is not altered, values do not persist. SETQ/SETQ2 does not affect ALTx instructions; the Q value passes through to the next instruction.



## ALTD {#altd}

Alter destination
[Register Indirection](#register-indirection) - Alter D field of next instruction.

**ALTD**  *Dest, {#}Src*
**ALTD**  *Dest*

---

**Result:** The next instruction's pipelined Dest value is altered to be (Src + Dest) & $1FF, or just Dest[8:0] in syntax 2.

- Dest is the register whose 9-bit value is the offset, or the full value, for the next instruction to operate on.
- Src is an optional register, 9-bit literal, or 18-bit augmented literal whose value contains a base (Src[8:0]; added to offset (Dest) for the next instruction) and also an optional auto-indexer value (Src[17:9]; added to Dest at the end of execution).

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1001100}{01I}{DDDDDDDDD}{SSSSSSSSS}{D\textsuperscript{1}}{---}{---}{2}
\encodingrow{EEEE}{1001100}{011}{DDDDDDDDD}{000000000}{D\textsuperscript{1}}{---}{---}{2}
\end{encodingtable}

\textsuperscript{1} Dest is post-adjusted by the auto-indexer value; the sign-extended Src[17:9]. In syntax 2, the auto-indexer value is 0.
```

**Related:** [ALTS](#alts), [ALTR](#altr), [ALTB](#altb), [ALTI](#alti)

**Explanation:**

ALTD modifies the next instruction's Dest value to be (Src + Dest) & $1FF (for syntax 1), or to Dest[8:0] (for syntax 2).

In syntax 1, Src consists of two 9-bit fields: a base value (Src[8:0]) and a signed auto-indexer (Src[17:9]). The base represents a starting point. ALTD adds the offset (Dest[8:0]) to the base (Src[8:0]) to determine the next instruction's Dest value. At the end of ALTD execution, the optional auto-indexer value (usually 0, 1, or -1) is added to the offset (Dest) for a future ALTD+instruction iteration.

In syntax 2, Dest serves as the full value. It is used as-is for the next instruction's substitute Dest value.

The instruction following ALTD is shielded from interrupt. ALTD alters the next instruction regardless of its kind. Field value modification occurs in the instruction pipeline only; code is not altered, values do not persist. SETQ/SETQ2 does not affect ALTx instructions; the Q value passes through to the next instruction.



## ALTGB {#altgb}

Alter get byte
[Register Indirection](#register-indirection) - Alter subsequent GETBYTE / ROLBYTE instruction.

**ALTGB**  *Dest, {#}Src*
**ALTGB**  *Dest*

---

**Result:** The next instruction's pipelined Src and Num fields are altered to be (Src + Dest[10:2]) & $1FF, or just Dest[10:2] for syntax 2, and Dest[1:0], respectively.

- Dest is the register whose 11-bit value is the index, or the full byte address, for the GETBYTE / ROLBYTE instruction to read.
- Src is an optional register, 9-bit literal, or 18-bit augmented literal whose value contains a base long address (Src[8:0]; added to index (Dest[10:2]) for GETBYTE / ROLBYTE) and also an optional auto-indexer value (Src[17:9]; added to Dest at end of execution).

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1001011}{01I}{DDDDDDDDD}{SSSSSSSSS}{D\textsuperscript{1}}{---}{---}{2}
\encodingrow{EEEE}{1001011}{011}{DDDDDDDDD}{000000000}{D\textsuperscript{1}}{---}{---}{2}
\end{encodingtable}

\textsuperscript{1} Dest is post-adjusted by the auto-indexer value; the sign-extended Src[17:9]. In syntax 2, the auto-indexer value is 0.
```

**Related:** [ALTGN](#altgn), [ALTGW](#altgw), [ALTSB](#altsb), [GETBYTE](#getbyte), [ROLBYTE](#rolbyte)

**Explanation:**

ALTGB should be followed by GETBYTE or ROLBYTE. It modifies the GETBYTE / ROLBYTE instruction's Src and Num values, enabling code to iterate through multiple bytes of data across a range of register RAM.

GETBYTE / ROLBYTE's Src value is changed to (Src + Dest[10:2]) & $1FF (for syntax 1), or to Dest[10:2] (for syntax 2), and its Num value is changed to Dest[1:0]. Dest[10:2] corresponds to the target long register's 9-bit address and Dest[1:0] is the byte ID within it; values of 0-3 identify individual bytes, by position, in least-significant byte order.

Iteratively executing ALTGB followed by GETBYTE or ROLBYTE, and each time incrementing ALTGB's 11-bit Dest value by one, effectively reads a stream of byte values from register RAM as if it were all made of byte-sized registers.

In syntax 1, Src consists of two 9-bit fields: a base address (Src[8:0]) and a signed auto-indexer (Src[17:9]). The base is the register RAM address where the series of bytes begins. ALTGB adds the long index (Dest[10:2]) to the base (Src[8:0]) to locate the register holding the target byte. The byte ID (Dest[1:0]) identifies the byte's position within that long register. At the end of ALTGB execution, the optional auto-indexer value (usually 0, 1, or -1) is added to the 11-bit index (Dest) for a future ALTGB+GETBYTE or ROLBYTE iteration.

In syntax 2, Dest serves as the full byte address. It is the same format as in syntax 1, but represents the target long's absolute address and its byte index instead of the long's relative index (to add to a base) and byte index.

The instruction following ALTGB is shielded from interrupt. Field value modification occurs in the instruction pipeline only; code is not altered, values do not persist. SETQ/SETQ2 does not affect ALTx instructions; the Q value passes through to the next instruction.



## ALTGN {#altgn}

Alter get nibble
[Register Indirection](#register-indirection) - Alter subsequent GETNIB / ROLNIB instruction.

**ALTGN**  *Dest, {#}Src*
**ALTGN**  *Dest*

---

**Result:** The next instruction's pipelined Src and Num values are altered to be (Src + Dest[11:3]) & $1FF, or just Dest[11:3] for syntax 2, and Dest[2:0], respectively.

- Dest is the register whose 12-bit value is the index, or the full nibble address, for the next GETNIB / ROLNIB instruction to read.
- Src is an optional register, 9-bit literal, or 18-bit augmented literal whose value contains a base long address (Src[8:0]; added to index (Dest[11:3]) for GETNIB / ROLNIB) and also an optional auto-indexer value (Src[17:9]; added to Dest at end of execution).

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1001010}{11I}{DDDDDDDDD}{SSSSSSSSS}{D\textsuperscript{1}}{---}{---}{2}
\encodingrow{EEEE}{1001010}{111}{DDDDDDDDD}{000000000}{D\textsuperscript{1}}{---}{---}{2}
\end{encodingtable}

\textsuperscript{1} Dest is post-adjusted by the auto-indexer value; the sign-extended Src[17:9]. In syntax 2, the auto-indexer value is 0.
```

**Related:** [ALTGB](#altgb), [ALTGW](#altgw), [ALTSN](#altsn), [GETNIB](#getnib), [ROLNIB](#rolnib)

**Explanation:**

ALTGN should be followed by GETNIB or ROLNIB. It modifies the GETNIB / ROLNIB instruction's Src and Num values, enabling code to iterate through multiple nibbles of data across a range of register RAM.

GETNIB / ROLNIB's Src value is changed to (Src + Dest[11:3]) & $1FF (for syntax 1), or to Dest[11:3] (for syntax 2), and its Num value is changed to Dest[2:0]. Dest[11:3] corresponds to the target long register's 9-bit address and Dest[2:0] is the nibble ID within it; values of 0-7 identify individual nibbles, by position, in least-significant nibble order.

Iteratively executing ALTGN followed by GETNIB or ROLNIB, and each time incrementing ALTGN's 12-bit Dest value by one, effectively reads a stream of nibble values from register RAM as if it were all made of nibble-sized registers.

In syntax 1, Src consists of two 9-bit fields: a base address (Src[8:0]) and a signed auto-indexer (Src[17:9]). The base is the register RAM address where the series of nibbles begins. ALTGN adds the long index (Dest[11:3]) to the base (Src[8:0]) to locate the register holding the target nibble. The nibble ID (Dest[2:0]) identifies the nibble's position within that long register. At the end of ALTGN execution, the optional auto-indexer value (usually 0, 1, or -1) is added to the 12-bit index (Dest) for a future ALTGN+GETNIB or ROLNIB iteration.

In syntax 2, Dest serves as the full nibble address. It is the same format as in syntax 1, but represents the target long's absolute address and its nibble index instead of the long's relative index (to add to a base) and nibble index.

The instruction following ALTGN is shielded from interrupt. Field value modification occurs in the instruction pipeline only; code is not altered, values do not persist. SETQ/SETQ2 does not affect ALTx instructions; the Q value passes through to the next instruction.



## ALTGW {#altgw}

Alter get word
[Register Indirection](#register-indirection) - Alter subsequent GETWORD / ROLWORD instruction.

**ALTGW**  *Dest, {#}Src*
**ALTGW**  *Dest*

---

**Result:** The next instruction's pipelined Src and Num fields are altered to be (Src + Dest[9:1]) & $1FF, or just Dest[9:1] for syntax 2, and Dest[0], respectively.

- Dest is the register whose 10-bit value is the index, or the full word address for the GETWORD / ROLWORD instruction to read.
- Src is an optional register, 9-bit literal, or 18-bit augmented literal whose value contains a base long address (Src[8:0]; added to index (Dest[9:1]) for GETWORD / ROLWORD) and also an optional auto-indexer value (Src[17:9]; added to Dest at end of execution).

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1001011}{11I}{DDDDDDDDD}{SSSSSSSSS}{D\textsuperscript{1}}{---}{---}{2}
\encodingrow{EEEE}{1001011}{111}{DDDDDDDDD}{000000000}{D\textsuperscript{1}}{---}{---}{2}
\end{encodingtable}

\textsuperscript{1} Dest is post-adjusted by the auto-indexer value; the sign-extended Src[17:9]. In syntax 2, the auto-indexer value is 0.
```

**Related:** [ALTGB](#altgb), [ALTGN](#altgn), [ALTSW](#altsw), [GETWORD](#getword), [ROLWORD](#rolword)

**Explanation:**

ALTGW should be followed by GETWORD or ROLWORD. It modifies the GETWORD / ROLWORD instruction's Src and Num values, enabling code to iterate through multiple words of data across a range of register RAM.

GETWORD / ROLWORD's Src value is changed to (Src + Dest[9:1]) & $1FF (for syntax 1), or to Dest[9:1] (for syntax 2), and its Num value is changed to Dest[0]. Dest[9:1] corresponds to the target long register's 9-bit address and Dest[0] is the word ID within it; values of 0-1 identify individual words, by position, in least-significant word order.

Iteratively executing ALTGW followed by GETWORD or ROLWORD, and each time incrementing ALTGW's 10-bit Dest value by one, effectively reads a stream of word values from register RAM as if it were all made of word-sized registers.

In syntax 1, Src consists of two 9-bit fields: a base address (Src[8:0]) and a signed auto-indexer (Src[17:9]). The base is the register RAM address where the series of words begins. ALTGW adds the long index (Dest[9:1]) to the base (Src[8:0]) to locate the register holding the target word. The word ID (Dest[0]) identifies the word's position within that long register. At the end of ALTGW execution, the optional auto-indexer value (usually 0, 1, or -1) is added to the 10-bit index (Dest) for a future ALTGW+GETWORD or ROLWORD iteration.

In syntax 2, Dest serves as the full word address. It is the same format as in syntax 1, but represents the target long's absolute address and its word index instead of the long's relative index (to add to a base) and word index.

The instruction following ALTGW is shielded from interrupt. Field value modification occurs in the instruction pipeline only; code is not altered, values do not persist. SETQ/SETQ2 does not affect ALTx instructions; the Q value passes through to the next instruction.



## ALTI {#alti}

Alter instruction
[Register Indirection](#register-indirection) - Substitute next instruction's field values from template, per configuration.

**ALTI**  *Dest, {#}Src*
**ALTI**  *Dest*

---

**Result:** The next instruction's pipelined field values are substituted from the Dest template, and Dest is modified per Src configuration.

- Dest is the register whose value contains one or more of the next instruction's field substitutes or an entire 32-bit opcode for full substitution.
- Src is an optional register, 9-bit literal, or 18-bit augmented literal whose value describes the substitutions and Dest modifications to perform.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1001101}{00I}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{2}
\encodingrow{EEEE}{1001101}{001}{DDDDDDDDD}{101100100}{---}{---}{---}{2}
\end{encodingtable}
```

**Related:** [SETD](#setd), [SETS](#sets), [SETR](#setr), [ALTD](#altd), [ALTS](#alts), [ALTR](#altr)

**Explanation:**

ALTI substitutes fields from Dest for one or more of the next instruction's pipelined Dest, Src, Result, Instr, FX, and/or Cond values, and ALTI's Dest is then modified per Src configuration (syntax 1), or the entire Dest opcode (instruction) is executed in place of the next instruction (syntax 2).

The Dest register contains the ALTI template; a 32-bit value with format similar to an opcode with Condition (31:28), Result (27:19), Indirect I (18), Dest D (17:9), and Source S (8:0) fields.

In syntax 1, Src consists of six 3-bit fields (%rrr_ddd_sss_RRR_DDD_SSS) that describe field substitution and Dest modification. The mask size fields (%rrr, %ddd, %sss) control increment/decrement masking from unlimited 9-bit (000) to 2-bit (111). The control fields (%RRR, %DDD, %SSS) control field substitution and adjustment.

In syntax 2, Dest serves as the full opcode value. It is executed as-is in place of the next instruction and Dest remains unaltered afterward.

The instruction following ALTI is shielded from interrupt. Field value modification occurs in the instruction pipeline only; code is not altered, values do not persist. SETQ/SETQ2 does not affect ALTx instructions; the Q value passes through to the next instruction.



## ALTR {#altr}

Alter result
[Register Indirection](#register-indirection) - Alter Result register address of next instruction.

**ALTR**  *Dest, {#}Src*
**ALTR**  *Dest*

---

**Result:** The next instruction's pipelined Result address (Dest address by default) is altered to be (Src + Dest) & $1FF, or just Dest[8:0] in syntax 2.

- Dest is the register whose 9-bit value is the offset, or the full value, for the next instruction to operate on.
- Src is an optional register, 9-bit literal, or 18-bit augmented literal whose value contains a base (Src[8:0]; added to offset (Dest) for the next instruction) and also an optional auto-indexer value (Src[17:9]; added to Dest at the end of execution).

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1001100}{00I}{DDDDDDDDD}{SSSSSSSSS}{D\textsuperscript{1}}{---}{---}{2}
\encodingrow{EEEE}{1001100}{001}{DDDDDDDDD}{000000000}{D\textsuperscript{1}}{---}{---}{2}
\end{encodingtable}

\textsuperscript{1} Dest is post-adjusted by the auto-indexer value; the sign-extended Src[17:9]. In syntax 2, the auto-indexer value is 0.
```

**Related:** [ALTD](#altd), [ALTS](#alts), [ALTB](#altb), [ALTI](#alti)

**Explanation:**

ALTR modifies the next instruction's Result address to be (Src + Dest) & $1FF (for syntax 1), or to Dest[8:0] (for syntax 2).

The Result address is the Dest address by default. It identifies where the result value from the instruction's execution is written at the end of execution. During execution, the pipeline holds an instruction's Dest address and the Result address as two separate entities, normally set to the same location. ALTR causes the next instruction's Result to redirect to a different address; changing an instruction from a destructive (operand overwriting) operation to a non-destructive (operand preserving) operation.

In syntax 1, Src consists of two 9-bit fields: a base value (Src[8:0]) and a signed auto-indexer (Src[17:9]). The base represents a starting point. ALTR adds the offset (Dest[8:0]) to the base (Src[8:0]) to determine the next instruction's Result address. At the end of ALTR execution, the optional auto-indexer value (usually 0, 1, or -1) is added to the offset (Dest) for a future ALTR+instruction iteration.

In syntax 2, Dest serves as the full value. It is used as-is for the next instruction's substitute Result address.

The instruction following ALTR is shielded from interrupt. ALTR alters the next instruction regardless of its kind. Field value modification occurs in the instruction pipeline only; code is not altered, values do not persist. SETQ/SETQ2 does not affect ALTx instructions; the Q value passes through to the next instruction.



## ALTS {#alts}

Alter source
[Register Indirection](#register-indirection) - Alter S field of next instruction.

**ALTS**  *Dest, {#}Src*
**ALTS**  *Dest*

---

**Result:** The next instruction's pipelined Src value is altered to be (Src + Dest) & $1FF, or just Dest[8:0] in syntax 2.

- Dest is the register whose 9-bit value is the offset, or the full value, for the next instruction to operate on.
- Src is an optional register, 9-bit literal, or 18-bit augmented literal whose value contains a base (Src[8:0]; added to offset (Dest) for the next instruction) and also an optional auto-indexer value (Src[17:9]; added to Dest at the end of execution).

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1001100}{10I}{DDDDDDDDD}{SSSSSSSSS}{D\textsuperscript{1}}{---}{---}{2}
\encodingrow{EEEE}{1001100}{101}{DDDDDDDDD}{000000000}{D\textsuperscript{1}}{---}{---}{2}
\end{encodingtable}

\textsuperscript{1} Dest is post-adjusted by the auto-indexer value; the sign-extended Src[17:9]. In syntax 2, the auto-indexer value is 0.
```

**Related:** [ALTD](#altd), [ALTR](#altr), [ALTB](#altb), [ALTI](#alti)

**Explanation:**

ALTS modifies the next instruction's Src value to be (Src + Dest) & $1FF (for syntax 1), or to Dest[8:0] (for syntax 2).

In syntax 1, Src consists of two 9-bit fields: a base value (Src[8:0]) and a signed auto-indexer (Src[17:9]). The base represents a starting point. ALTS adds the offset (Dest[8:0]) to the base (Src[8:0]) to determine the next instruction's Src value. At the end of ALTS execution, the optional auto-indexer value (usually 0, 1, or -1) is added to the offset (Dest) for a future ALTS+instruction iteration.

In syntax 2, Dest serves as the full value. It is used as-is for the next instruction's substitute Src value.

The instruction following ALTS is shielded from interrupt. ALTS alters the next instruction regardless of its kind. Field value modification occurs in the instruction pipeline only; code is not altered, values do not persist. SETQ/SETQ2 does not affect ALTx instructions; the Q value passes through to the next instruction.



## ALTSB {#altsb}

Alter set byte
[Register Indirection](#register-indirection) - Alter subsequent SETBYTE instruction.

**ALTSB**  *Dest, {#}Src*
**ALTSB**  *Dest*

---

**Result:** The next instruction's pipelined Dest and Num values are altered to be (Src + Dest[10:2]) & $1FF (syntax 1), or just Dest[10:2] (syntax 2), and Num is set to Dest[1:0]. Dest is post-adjusted by auto-indexer.

- Dest is the register whose 11-bit value is the index (Dest[10:2] = long address, Dest[1:0] = byte ID) or the full byte address for SETBYTE to operate on.
- Src is an optional register, 9-bit literal, or 18-bit augmented literal containing base long address (Src[8:0]) and optional auto-indexer value (Src[17:9]).

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1001011}{00I}{DDDDDDDDD}{SSSSSSSSS}{D\textsuperscript{1}}{---}{---}{2}
\encodingrow{EEEE}{1001011}{001}{DDDDDDDDD}{000000000}{D\textsuperscript{1}}{---}{---}{2}
\end{encodingtable}

\textsuperscript{1} Dest is post-adjusted by the auto-indexer value; the sign-extended Src[17:9]. In syntax 2, the auto-indexer value is 0.
```

**Related:** [ALTGB](#altgb), [ALTSN](#altsn), [ALTSW](#altsw), [SETBYTE](#setbyte)

**Explanation:**

ALTSB should be followed by SETBYTE. It modifies the SETBYTE instruction's Dest and Num values, enabling code to iterate through multiple bytes across register RAM.

SETBYTE's Dest is changed to (Src + Dest[10:2]) & $1FF (syntax 1), or to Dest[10:2] (syntax 2), and its Num value is changed to Dest[1:0]. Dest[10:2] is the target long register's 9-bit address; Dest[1:0] is the byte ID (0-3) within it.

Iteratively executing ALTSB followed by SETBYTE while incrementing the 11-bit Dest value writes a stream of bytes to register RAM as if it were byte-sized registers.

In syntax 1, Src contains a base address (Src[8:0]) and signed auto-indexer (Src[17:9]). In syntax 2, Dest serves as the full byte address.

The instruction following ALTSB is shielded from interrupt. ALTSB alters the next instruction regardless of its kind (intended for SETBYTE). Field value modification occurs in the instruction pipeline only; code is not altered, values do not persist. SETQ/SETQ2 does not affect ALTx instructions; the Q value passes through to the next instruction.



## ALTSN {#altsn}

Alter set nibble
[Register Indirection](#register-indirection) - Alter subsequent SETNIB instruction.

**ALTSN**  *Dest, {#}Src*
**ALTSN**  *Dest*

---

**Result:** The next instruction's pipelined Dest and Num values are altered to be (Src + Dest[11:3]) & $1FF, or just Dest[11:3] for syntax 2, and Dest[2:0], respectively.

- Dest is the register whose 12-bit value is the index, or the full nibble address, for the SETNIB instruction to operate on.
- Src is an optional register, 9-bit literal, or 18-bit augmented literal whose value contains a base long address (Src[8:0]; added to index (Dest[11:3]) for SETNIB) and also an optional auto-indexer value (Src[17:9]; added to Dest at the end of execution).

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1001010}{10I}{DDDDDDDDD}{SSSSSSSSS}{D\textsuperscript{1}}{---}{---}{2}
\encodingrow{EEEE}{1001010}{101}{DDDDDDDDD}{000000000}{D\textsuperscript{1}}{---}{---}{2}
\end{encodingtable}

\textsuperscript{1} Dest is post-adjusted by the auto-indexer value; the sign-extended Src[17:9]. In syntax 2, the auto-indexer value is 0.
```

**Related:** [ALTGN](#altgn), [ALTSB](#altsb), [ALTSW](#altsw), [SETNIB](#setnib)

**Explanation:**

ALTSN should be followed by SETNIB. It modifies the SETNIB instruction's Dest and Num values, enabling code to iterate through multiple nibbles of data across a range of register RAM.

SETNIB's Dest value is changed to (Src + Dest[11:3]) & $1FF (for syntax 1), or to Dest[11:3] (for syntax 2), and its Num value is changed to Dest[2:0]. Dest[11:3] corresponds to the target long register's 9-bit address and Dest[2:0] is the nibble ID within it; values of 0-7 identify individual nibbles, by position, in least-significant nibble order.

Iteratively executing ALTSN followed by SETNIB, and each time incrementing ALTSN's 12-bit Dest value by one, effectively writes a stream of nibble values to register RAM as if it were all made of nibble-sized registers.

In syntax 1, Src consists of two 9-bit fields: a base address (Src[8:0]) and a signed auto-indexer (Src[17:9]). The base is the register RAM address where the series of nibbles begins. ALTSN adds the long index (Dest[11:3]) to the base (Src[8:0]) to locate the register holding the target nibble. The nibble ID (Dest[2:0]) identifies the nibble's position within that long register. At the end of ALTSN execution, the optional auto-indexer value (usually 0, 1, or -1) is added to the 12-bit index (Dest) for a future ALTSN+SETNIB iteration.

In syntax 2, Dest serves as the full nibble address. It is the same format as in syntax 1, but represents the target long's absolute address and its nibble index instead of the long's relative index (to add to a base) and nibble index.

The instruction following ALTSN is shielded from interrupt. ALTSN alters the next instruction regardless of its kind (intended for SETNIB). Field value modification occurs in the instruction pipeline only; code is not altered, values do not persist. SETQ/SETQ2 does not affect ALTx instructions; the Q value passes through to the next instruction.



## ALTSW {#altsw}

Alter set word
[Register Indirection](#register-indirection) - Alter subsequent SETWORD instruction.

**ALTSW**  *Dest, {#}Src*
**ALTSW**  *Dest*

---

**Result:** The next instruction's pipelined Dest and Num fields are altered to be (Src + Dest[9:1]) & $1FF, or just Dest[9:1] for syntax 2, and Dest[0], respectively.

- Dest is the register whose 10-bit value is the index, or the full word address, for the SETWORD instruction to operate on.
- Src is an optional register, 9-bit literal, or 18-bit augmented literal whose value contains a base long address (Src[8:0]; added to index (Dest[9:1]) for SETWORD) and also an optional auto-indexer value (Src[17:9]; added to Dest at end of execution).

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1001011}{10I}{DDDDDDDDD}{SSSSSSSSS}{D\textsuperscript{1}}{---}{---}{2}
\encodingrow{EEEE}{1001011}{101}{DDDDDDDDD}{000000000}{D\textsuperscript{1}}{---}{---}{2}
\end{encodingtable}

\textsuperscript{1} Dest is post-adjusted by the auto-indexer value; the sign-extended Src[17:9]. In syntax 2, the auto-indexer value is 0.
```

**Related:** [ALTGW](#altgw), [ALTSB](#altsb), [ALTSN](#altsn), [SETWORD](#setword)

**Explanation:**

ALTSW should be followed by SETWORD. It modifies the SETWORD instruction's Dest and Num values, enabling code to iterate through multiple words of data across a range of register RAM.

SETWORD's Dest value is changed to (Src + Dest[9:1]) & $1FF (for syntax 1), or to Dest[9:1] (for syntax 2), and its Num value is changed to Dest[0]. Dest[9:1] corresponds to the target long register's 9-bit address and Dest[0] is the word ID within it; values of 0-1 identify individual words, by position, in least-significant word order.

Iteratively executing ALTSW followed by SETWORD, and each time incrementing ALTSW's 10-bit Dest value by one, effectively writes a stream of word values to register RAM as if it were all made of word-sized registers.

In syntax 1, Src consists of two 9-bit fields: a base address (Src[8:0]) and a signed auto-indexer (Src[17:9]). The base is the register RAM address where the series of words begins. ALTSW adds the long index (Dest[9:1]) to the base (Src[8:0]) to locate the register holding the target word. The word ID (Dest[0]) identifies the word's position within that long register. At the end of ALTSW execution, the optional auto-indexer value (usually 0, 1, or -1) is added to the 10-bit index (Dest) for a future ALTSW+SETWORD iteration.

In syntax 2, Dest serves as the full word address. It is the same format as in syntax 1, but represents the target long's absolute address and its word index instead of the long's relative index (to add to a base) and word index.

The instruction following ALTSW is shielded from interrupt. ALTSW alters the next instruction regardless of its kind (intended for SETWORD). Field value modification occurs in the instruction pipeline only; code is not altered, values do not persist. SETQ/SETQ2 does not affect ALTx instructions; the Q value passes through to the next instruction.



## AND {#and}

Bitwise AND
[Math and Logic](#math-and-logic) - Bitwise AND a value with another, or with the NOT of another.

**AND**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Bitwise AND of Dest and Src is stored in Dest.

- Dest is the register containing the value to bitwise AND with Src and is the destination in which to write the result.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value will be bitwise ANDed with Dest.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0101000}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{parity of result}{Result = 0}{2}
```

**Related:** [ANDN](#andn), [OR](#or), [XOR](#xor), [TEST](#test)

**Explanation:**

AND performs a bitwise AND of the value in Src into that of Dest, storing the result in Dest. Each bit in the result is 1 only if the corresponding bits in both Dest and Src are 1.

If the WC or WCZ effect is specified, the C flag is set (1) if the result contains an odd number of high (1) bits, or is cleared (0) if it contains an even number of high bits. This parity calculation is useful for error detection.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if it is non-zero.



## ANDN {#andn}

And not
[Math and Logic](#math-and-logic) - Bitwise AND a value with the NOT of another.

**ANDN**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Bitwise AND of Dest with inverse of Src is stored in Dest.

- Dest is the register containing the value to bitwise AND with the inverse of Src and is the destination in which to write the result.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose inverse value will be bitwise ANDed with Dest.
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{0101001}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{parity of result}{Result = 0}{2}
```

**Related:** [AND](#and), [OR](#or), [XOR](#xor), [TEST](#test)

**Explanation:**

ANDN performs a bitwise AND of Dest with the inverse of Src (!Src), storing the result in Dest. This effectively clears bits in Dest wherever the corresponding bits in Src are set.

ANDN is particularly useful for clearing specific bits while leaving others unchanged. For example, to clear bits 7:4 of a register while preserving all other bits, use ANDN with a mask that has 1s in positions 7:4.

If the WC or WCZ effect is specified, the C flag is set (1) if the result contains an odd number of high (1) bits, or is cleared (0) if it contains an even number of high bits.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if it is non-zero.



## ASMCLK {#asmclk}

Assembly clock instruction
[System Control](#system-control) - Assembly clock instruction.

```
ASMCLK
```

**Result:** Controls assembly-time clock operations.

```{=latex}
\simpleencoding{EEEE}{0000000}{000}{000000000}{000000000}{---}{---}{---}{2}
```

**Related:** [GETCT](instructions-g.md#getct), [POLLCT1/2/3](instructions-p.md#pollct1)

**Explanation:**

ASMCLK controls assembly-time clock operations. This instruction is used during the assembly process to manage timing-related assembly directives.



## AUGD {#augd}

Augment destination
[Miscellaneous](#miscellaneous) - Augment next literal Dest to 32-bits.

**AUGD**  *#Dest*

---

**Result:** The 23-bit value formed from Dest is queued to prefix the next literal Dest occurrence (#Dest) to form a 32-bit literal for that instruction; interrupts are also temporarily disabled.

- Dest is a 32-bit literal whose upper 23 bits are prepended to the next literal Dest occurrence.

```{=latex}
\simpleencoding{EEEE}{11111DD}{DDD}{DDDDDDDDD}{DDDDDDDDD}{Hidden D Queue}{---}{---}{2}
```

**Related:** [AUGS](#augs)

**Explanation:**

AUGD is an assistant instruction to aid with literal values that exceed 9 bits. Most PASM2 instructions have 9 bits available for literal Dest values; enough for many uses, but not all. AUGD augments the next occurrence of a literal Dest value to be a full 32-bits.

When the instruction with the soon-to-be-augmented literal is later executed, the COG uses the lower 9 bits encoded in the instruction's Dest field and prepends AUGD's 23 bits to it.

All instructions following AUGD are shielded from interrupt until after the instruction with the newly-augmented literal Dest value is executed. Dest value augmentation occurs in the instruction pipeline only; code is not altered, value does not persist. SETQ/SETQ2 does not affect AUGD; the Q value passes through to the next instruction.

Though AUGD may be manually entered wherever needed, the Parallax P2 compiler supports a convenient way to use this feature. In the target instruction's Dest field, use "##" followed by the desired 32-bit literal (instead of "#" followed by a 9-bit literal); the compiler will automatically invoke AUGD immediately before. When counting clock cycles, make sure to account for 2 extra clock cycles for instructions containing ## augmented literals.



## AUGS {#augs}

Augment source
[Miscellaneous](#miscellaneous) - Augment next literal Src to 32-bits.

**AUGS**  *#Src*

---

**Result:** The 23-bit value formed from Src is queued to prefix the next literal Src occurrence (#Src) to form a 32-bit literal for that instruction; interrupts are also temporarily disabled.

- Src is a 32-bit literal whose upper 23 bits are prepended to the next literal Src occurrence.

```{=latex}
\simpleencoding{EEEE}{11110SS}{SSS}{SSSSSSSSS}{SSSSSSSSS}{Hidden S Queue}{---}{---}{2}
```

**Related:** [AUGD](#augd)

**Explanation:**

AUGS is an assistant instruction to aid with literal values that exceed 9 bits. Most PASM2 instructions have 9 bits available for literal Src values; enough for many uses, but not all. AUGS augments the next occurrence of a literal Src value to be a full 32-bits.

When the instruction with the soon-to-be-augmented literal is later executed, the COG uses the lower 9 bits encoded in the instruction's Src field and prepends AUGS's 23 bits to it.

All instructions following AUGS are shielded from interrupt until after the instruction with the newly-augmented literal Src value is executed. Src value augmentation occurs in the instruction pipeline only; code is not altered, value does not persist. SETQ/SETQ2 does not affect AUGS; the Q value passes through to the next instruction.

Though AUGS may be manually entered wherever needed, the Parallax P2 compiler supports a convenient way to use this feature. In the target instruction's Src field, use "##" followed by the desired 32-bit literal (instead of "#" followed by a 9-bit literal); the compiler will automatically invoke AUGS immediately before. When counting clock cycles, make sure to account for 2 extra clock cycles for instructions containing ## augmented literals.


