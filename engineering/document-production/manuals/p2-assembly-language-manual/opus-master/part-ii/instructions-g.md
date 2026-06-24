# Instructions: G

This section contains all PASM2 instructions beginning with the letter G.



::: instrheader
## GETBRK {#getbrk}
Get Breakpoint Status

[Interrupts](#interrupts) - Retrieves breakpoint or cog status information.
:::

**GETBRK**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** Breakpoint or cog status information is retrieved into Dest based on the flag effect specified.

- Dest is a register where the status information is written.
- WC, WZ, or WCZ are optional effects that determine which status information is retrieved.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000110101 | --- | --- | D | 2 |


**Related:** [BRK](#brk), [COGBRK](#cogbrk)

**Explanation:**

GETBRK retrieves various breakpoint and cog status information into the Dest register. The specific information retrieved depends on which flag effect is specified.

When the WCZ effect is specified, GETBRK retrieves the full 32-bit ISR call address into Dest. This is the address where the debug interrupt service routine will resume execution after handling the breakpoint.

When the WC effect is specified, GETBRK retrieves the 8-bit cog ID into Dest[7:0]. This identifies which cog triggered the breakpoint, useful in multi-cog debugging scenarios where a debug ISR needs to determine the calling cog.

When the WZ effect is specified, GETBRK retrieves the 8-bit breakpoint code into Dest[7:0]. This code was set by the BRK instruction and can be used for conditional breakpoint handling or to distinguish between different types of breakpoints.

When no flag effects are specified, GETBRK retrieves the 16-bit skip pattern into Dest[15:0]. This pattern is used with the SKIPF instruction to selectively execute or skip subsequent instructions, typically within an ISR context.

GETBRK is essential for implementing debug infrastructure and coordinating multi-cog debugging systems. It works in conjunction with BRK and SETBRK to provide comprehensive breakpoint support.



::: instrheader
## GETBYTE {#getbyte}
Get Byte

[Arithmetic Operations](#arithmetic-operations) - Extracts a specified byte from a 32-bit value.
:::

**GETBYTE**  *Dest, {#}Src, #Num*\
**GETBYTE**  *Dest*

---

**Operation:** `D = {24'b0, S.BYTE[N]}`

**Result:** Byte Num (0-3) of Src, or a byte from a source described by prior ALTGB instruction, is written to Dest.

- Dest is the register in which to store the byte.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value contains the target byte to read.
- Num is a 2-bit literal identifying the byte ID (0-3) of Src to read.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1000111 | NNI | DDDDDDDDD | SSSSSSSSS | --- | --- | D | 2 |
| EEEE | 1000111 | 000 | DDDDDDDDD | 000000000 | --- | --- | D | 2 |


**Related:** [ALTGB](#altgb), [GETNIB](#getnib), [GETWORD](#getword), [SETBYTE](#setbyte), [ROLBYTE](#rolbyte)

**Explanation:**

GETBYTE reads the byte identified by Num (0-3) from Src and writes it to Dest. The Num parameter identifies which of the four bytes in the 32-bit value to extract, numbered in least-significant byte order.

Num 0 selects bits [7:0], Num 1 selects bits [15:8], Num 2 selects bits [23:16], and Num 3 selects bits [31:24]. The extracted byte is zero-extended to 32 bits when written to Dest.

The second syntax form (GETBYTE Dest) is intended for use after an ALTGB instruction. This form is useful in loops that iteratively read a series of byte values from contiguous long registers. The ALTGB instruction modifies the subsequent GETBYTE instruction's source register and byte index automatically, enabling efficient sequential byte extraction without explicitly specifying the source and index on each iteration.



::: instrheader
## GETCT {#getct}
Get System Counter

[Miscellaneous](#miscellaneous) - Retrieves the current value of the system counter.
:::

**GETCT**  *Dest*  **{WC}**

---

**Operation:** `D = CT[31:0]` (or `CT[63:32]` if WC)

**Result:** The current value of the system counter CT is written to Dest.

- Dest is a register where the system counter value is written.
- WC is an optional effect to retrieve the upper 32 bits of the 64-bit counter (Rev B/C silicon).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | C00 | DDDDDDDDD | 000011010 | --- | --- | D (CT[31:0], or CT[63:32] if WC) | 2 |


**Related:** [ADDCT1/2/3](#addct1), [WAITCT1/2/3](#waitct1)

**Explanation:**

GETCT retrieves the current value of the system counter CT into the Dest register. On Rev B/C silicon, the system counter is a 64-bit counter that is reset to zero on system reset and increments by one on every clock cycle. By default, the lower 32 bits (CT[31:0]) are returned in Dest.

The CT counter provides a continuous, monotonic time reference. The lower 32 bits wrap around from $FFFF_FFFF to $0000_0000 approximately every 21.5 seconds at 200 MHz. This counter is shared across all cogs and provides the foundation for timing operations and synchronization.

**64-bit Counter (Rev B/C):** If the WC effect is specified, the upper 32 bits of the 64-bit counter (CT[63:32]) are written to Dest instead of the lower 32 bits. To capture a full 64-bit timestamp, use two consecutive GETCT instructions:

```pasm2
        getct   low_word        ' Get lower 32 bits (CT[31:0])
        getct   high_word wc    ' Get upper 32 bits (CT[63:32])
```

GETCT is commonly used with the ADDCT and WAITCT instruction families to implement precise timing, delays, and event scheduling. The retrieved counter value serves as a time reference for calculating future wait points or measuring elapsed time intervals.



::: instrheader
## GETNIB {#getnib}
Get Nibble

[Arithmetic Operations](#arithmetic-operations) - Extracts a specified nibble from a 32-bit value.
:::

**GETNIB**  *Dest, {#}Src, #Num*\
**GETNIB**  *Dest*

---

**Operation:** `D = {28'b0, S.NIBBLE[N]}`

**Result:** Nibble Num (0-7) of Src, or a nibble from a source described by prior ALTGN instruction, is written to Dest.

- Dest is the register in which to store the nibble.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value contains the target nibble to read.
- Num is a 3-bit literal identifying the nibble ID (0-7) of Src to read.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 100001N | NNI | DDDDDDDDD | SSSSSSSSS | --- | --- | D | 2 |
| EEEE | 1000010 | 000 | DDDDDDDDD | 000000000 | --- | --- | D | 2 |


**Related:** [ALTGN](#altgn), [GETBYTE](#getbyte), [GETWORD](#getword), [SETNIB](#setnib), [ROLNIB](#rolnib)

**Explanation:**

GETNIB reads the nibble identified by Num (0-7) from Src and writes it to Dest. The Num parameter identifies which of the eight nibbles in the 32-bit value to extract, numbered in least-significant nibble order.

Num 0 selects bits [3:0], Num 1 selects bits [7:4], Num 2 selects bits [11:8], and so on up to Num 7 which selects bits [31:28]. The extracted nibble is zero-extended to 32 bits when written to Dest.

The second syntax form (GETNIB Dest) is intended for use after an ALTGN instruction. This form is useful in loops that iteratively read a series of nibble values from contiguous long registers. The ALTGN instruction modifies the subsequent GETNIB instruction's source register and nibble index automatically, enabling efficient sequential nibble extraction without explicitly specifying the source and index on each iteration.



::: instrheader
## GETPTR {#getptr}
Get FIFO Hub Pointer

[hub memory Access](#hub-memory-access) - Retrieves the current FIFO hub pointer position.
:::

**GETPTR**  *Dest*

---

**Result:** The current FIFO hub pointer is written to Dest.

- Dest is a register where the FIFO hub pointer is written.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 000110100 | --- | --- | D | 2 |


**Related:** [RDFAST](#rdfast), [WRFAST](#wrfast), [RFBYTE](#rfbyte), [RFWORD](#rfword), [RFLONG](#rflong), [WFBYTE](#wfbyte), [WFWORD](#wfword), [WFLONG](#wflong)

**Explanation:**

GETPTR retrieves the current position of the hub FIFO pointer into the Dest register. This pointer tracks the current hub memory address for FIFO read and write operations initiated by RDFAST or WRFAST.

The hub FIFO pointer advances automatically as data is read from or written to the hub FIFO using the RFBYTE, RFWORD, RFLONG, WFBYTE, WFWORD, or WFLONG instructions. Each FIFO access increments the pointer by the size of the data transferred (1 byte, 2 bytes, or 4 bytes).

GETPTR is useful for monitoring FIFO transfer progress, calculating how much data has been transferred, or determining the current position within a buffer. The retrieved pointer value represents the hub memory address that will be accessed by the next FIFO read or write operation.



::: instrheader
## GETQX {#getqx}
Get CORDIC X Result

[CORDIC Coprocessor](#cordic-coprocessor) - Retrieves the X result from the CORDIC solver.
:::

**GETQX**  *Dest*  **{WC|WZ|WCZ}**

---

**Operation:** `D = CORDIC result X` (waits if not ready); `C = X[31]`

**Result:** The CORDIC X result is written to Dest after waiting if necessary for the computation to complete.

- Dest is a register where the CORDIC X result is written.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000011000 | X[31] | result == 0 | D | 2...58 |


**Related:** [GETQY](#getqy), [QROTATE](#qrotate), [QVECTOR](#qvector), [QMUL](#qmul), [QDIV](#qdiv), [QFRAC](#qfrac), [QSQRT](#qsqrt), [QLOG](#qlog), [QEXP](#qexp)

**Explanation:**

GETQX retrieves the X result from the CORDIC solver into the Dest register. If the CORDIC computation is not yet complete when GETQX executes, the instruction waits until the result is ready before retrieving it and continuing execution.

The CORDIC solver performs various mathematical operations including rotation, vectoring, multiplication, division, square root, logarithm, and exponentiation. Each operation produces two results, X and Y, which are retrieved using GETQX and GETQY respectively.

If the WC or WCZ effect is specified, the C flag is set to X[31], which is the sign bit of the result. This allows immediate determination of whether the result is negative (C = 1) or non-negative (C = 0) when interpreting the result as a signed value.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if the result is non-zero.

GETQX takes 2 clocks if the result is already available. If the result is not yet ready, GETQX waits until the CORDIC computation completes (up to 58 clocks from when the operation was queued).



::: instrheader
## GETQY {#getqy}
Get CORDIC Y Result

[CORDIC Coprocessor](#cordic-coprocessor) - Retrieves the Y result from the CORDIC solver.
:::

**GETQY**  *Dest*  **{WC|WZ|WCZ}**

---

**Operation:** `D = CORDIC result Y` (waits if not ready); `C = Y[31]`

**Result:** The CORDIC Y result is written to Dest after waiting if necessary for the computation to complete.

- Dest is a register where the CORDIC Y result is written.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000011001 | Y[31] | result == 0 | D | 2...58 |


**Related:** [GETQX](#getqx), [QROTATE](#qrotate), [QVECTOR](#qvector), [QMUL](#qmul), [QDIV](#qdiv), [QFRAC](#qfrac), [QSQRT](#qsqrt), [QLOG](#qlog), [QEXP](#qexp)

**Explanation:**

GETQY retrieves the Y result from the CORDIC solver into the Dest register. If the CORDIC computation is not yet complete when GETQY executes, the instruction waits until the result is ready before retrieving it and continuing execution.

The CORDIC solver performs various mathematical operations including rotation, vectoring, multiplication, division, square root, logarithm, and exponentiation. Each operation produces two results, X and Y, which are retrieved using GETQX and GETQY respectively.

If the WC or WCZ effect is specified, the C flag is set to Y[31], which is the sign bit of the result. This allows immediate determination of whether the result is negative (C = 1) or non-negative (C = 0) when interpreting the result as a signed value.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if the result is non-zero.

GETQY takes 2 clocks if the result is already available. If the result is not yet ready, GETQY waits until the CORDIC computation completes (up to 58 clocks from when the operation was queued).



::: instrheader
## GETRND {#getrnd}
Get Random Value

[Miscellaneous](#miscellaneous) - Retrieves a pseudo-random value from the cog's RNG.
:::

**GETRND**  *Dest*  **{WC|WZ|WCZ}**\
**GETRND**  **{WC|WZ|WCZ}**

---

**Operation:** `D = RND[31:0]`; `C = RND[31]`; `Z = RND[30]`

**Result:** The current pseudo-random value is written to Dest, or the random bits are stored in the C and Z flags.

- Dest is a register where the full 32-bit random value is written (first syntax).
- WC, WZ, or WCZ are optional effects to retrieve random bits into flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000011011 | RND[31] | RND[30], unique per cog | D | 2 |
| EEEE | 1101011 | CZ1 | 000000000 | 000011011 | RND[31] | RND[30], unique per cog | --- | 2 |


**Related:** [SETQ](#setq), [SETQ2](#setq2)

**Explanation:**

GETRND retrieves the current value from the pseudo-random number generator (RNG) that is unique to each cog. Each cog maintains its own independent RNG state that advances continuously.

The first syntax form (GETRND Dest) writes the full 32-bit random value to the Dest register. This provides a complete random word for applications requiring random data, random seeds, or probabilistic algorithms.

The second syntax form (GETRND without Dest) is used when only random flag bits are needed. This form requires at least one flag effect to be specified, otherwise the instruction has no visible effect.

If the WC or WCZ effect is specified, the C flag is set to RND[31], which is the most significant bit of the current random value.

If the WZ or WCZ effect is specified, the Z flag is set to RND[30]. Notably, RND[30] is unique per cog, meaning each cog's RNG produces independent bit sequences at this position, useful for multi-cog systems requiring independent randomness.

The random value is produced by the P2's Xoroshiro128** pseudo-random number generator, which has 128 bits of state, advances every clock cycle, and has an extremely long period (2^128 - 1).



::: instrheader
## GETSCP {#getscp}
Get Oscilloscope Samples

[Pin I/O and smart pins](#pin-io-and-smart-pins) - Retrieves four 8-bit oscilloscope samples.
:::

**GETSCP**  *Dest*

---

**Operation:** `D = {ch3[7:0], ch2[7:0], ch1[7:0], ch0[7:0]}`

**Result:** Four 8-bit oscilloscope samples are written to Dest as D = {ch3[7:0], ch2[7:0], ch1[7:0], ch0[7:0]}.

- Dest is a register where the four oscilloscope samples are written.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001110001 | --- | --- | D | 2 |


**Related:** [SETSCP](#setscp), [RDPIN](#rdpin), [WXPIN](#wxpin)

**Explanation:**

GETSCP retrieves the current samples from the four-channel digital oscilloscope into the Dest register. The oscilloscope continuously samples four independent channels and packs the 8-bit sample values into a single 32-bit word.

The four samples are arranged in the Dest register with channel 0 in bits [7:0], channel 1 in bits [15:8], channel 2 in bits [23:16], and channel 3 in bits [31:24]. Each channel provides an 8-bit unsigned sample value ranging from 0 to 255.

The oscilloscope is configured using the SETSCP instruction to specify which pins or signals each channel monitors. Once configured, the oscilloscope continuously updates its samples based on the monitored signals, and GETSCP can retrieve the latest samples at any time.

This instruction is useful for real-time signal monitoring, debugging, and creating oscilloscope-like functionality for analyzing digital signals or pin states within the P2 system.



::: instrheader
## GETWORD {#getword}
Get Word

[Arithmetic Operations](#arithmetic-operations) - Extracts a specified word from a 32-bit value.
:::

**GETWORD**  *Dest, {#}Src, #Num*\
**GETWORD**  *Dest*

---

**Operation:** `D = {16'b0, S.WORD[N]}`

**Result:** Word Num (0-1) of Src, or a word from a source described by prior ALTGW instruction, is written to Dest.

- Dest is the register in which to store the word.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value contains the target word to read.
- Num is a 1-bit literal identifying the word ID (0-1) of Src to read.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001001 | 1NI | DDDDDDDDD | SSSSSSSSS | --- | --- | D | 2 |
| EEEE | 1001001 | 100 | DDDDDDDDD | 000000000 | --- | --- | D | 2 |


**Related:** [ALTGW](#altgw), [GETNIB](#getnib), [GETBYTE](#getbyte), [SETWORD](#setword), [ROLWORD](#rolword)

**Explanation:**

GETWORD reads the word identified by Num (0-1) from Src and writes it to Dest. The Num parameter identifies which of the two words in the 32-bit value to extract, numbered in least-significant word order.

Num 0 selects bits [15:0] (the lower word), and Num 1 selects bits [31:16] (the upper word). The extracted word is zero-extended to 32 bits when written to Dest.

The second syntax form (GETWORD Dest) is intended for use after an ALTGW instruction. This form is useful in loops that iteratively read a series of word values from contiguous long registers. The ALTGW instruction modifies the subsequent GETWORD instruction's source register and word index automatically, enabling efficient sequential word extraction without explicitly specifying the source and index on each iteration.



::: instrheader
## GETXACC {#getxacc}
Get Goertzel Accumulators

[streamer](#streamer) - Retrieves Goertzel X and Y accumulators from the streamer.
:::

**GETXACC**  *Dest*

---

**Operation:** `D = Goertzel X accumulator`; the next instruction's S = Y accumulator; both accumulators are cleared

**Result:** The streamer's Goertzel X accumulator is written to Dest, the Y accumulator is written to the next instruction's S field, and both accumulators are cleared.

- Dest is a register where the Goertzel X accumulator value is written.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 000011110 | --- | --- | D | 2 |


**Related:** [XCONT](#xcont), [XINIT](#xinit), [XZERO](#xzero)

**Explanation:**

GETXACC retrieves the two Goertzel accumulators from the streamer, which are used for frequency detection and digital signal processing applications. The Goertzel algorithm accumulates signal correlation data that can be used to detect specific frequencies in an input signal.

The X accumulator value is written directly to the Dest register. The Y accumulator value is written to the S field of the immediately following instruction, utilizing the P2's next-instruction operand modification capability. After both values are retrieved, the X and Y accumulators are automatically cleared to zero.

This dual-retrieval mechanism allows both accumulator values to be captured in a compact instruction sequence. The following instruction must have an S field that can receive the Y accumulator value. Typically, this is a MOV or similar instruction where the S operand receives the Y accumulator data.

GETXACC is used in conjunction with the streamer's Goertzel mode, configured via XINIT and controlled via XCONT. The retrieved accumulator values represent the correlation between the input signal and the reference frequency configured in the Goertzel algorithm.



