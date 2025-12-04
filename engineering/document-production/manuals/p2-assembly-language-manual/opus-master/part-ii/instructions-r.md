# Instructions: R

This section contains all PASM2 instructions beginning with the letter R.



::: instrheader
## RCL {#rcl}
Rotate Carry Left

[Arithmetic Operations](#arithmetic-operations) - Shifts bits left, inserting carry flag as new LSBs.
:::

**RCL**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are shifted left by Src bits, inserting C as new LSBs.

- Dest is a register containing the value to rotate carry left.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to rotate.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0000101 | CZI | DDDDDDDDD | SSSSSSSSS | D | Last bit out\textsuperscript{1} | Result = 0 | 2 |


**Related:** [RCR](#rcr), [ROL](#rol), [ROR](#ror)

**Explanation:**

RCL shifts Dest's binary value left by Src places (0-31 bits) and sets the new LSBs to C. The carry flag acts as an extension of the register, allowing 33-bit rotations.

If the WC or WCZ effect is specified, the C flag is updated to the value of the last bit shifted out if Src is 1-31, or to Dest[31] if Src is 0.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if non-zero.

This instruction is useful for multi-precision arithmetic operations where the carry from one word needs to be propagated into the next word.



::: instrheader
## RCR {#rcr}
Rotate Carry Right

[Arithmetic Operations](#arithmetic-operations) - Shifts bits right, inserting carry flag as new MSBs.
:::

**RCR**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are shifted right by Src bits, inserting C as new MSBs.

- Dest is a register containing the value to rotate carry right.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to rotate.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0000100 | CZI | DDDDDDDDD | SSSSSSSSS | D | Last bit out\textsuperscript{1} | Result = 0 | 2 |


**Related:** [RCL](#rcl), [ROL](#rol), [ROR](#ror)

**Explanation:**

RCR shifts Dest's binary value right by Src places (0-31 bits) and sets the new MSBs to C. The carry flag acts as an extension of the register, allowing 33-bit rotations.

If the WC or WCZ effect is specified, the C flag is updated to the value of the last bit shifted out if Src is 1-31, or to Dest[0] if Src is 0.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if non-zero.

This instruction is useful for multi-precision arithmetic operations where the carry needs to be propagated through multiple words.



::: instrheader
## RCZL {#rczl}
Rotate Carry And Zero Left

[Arithmetic Operations](#arithmetic-operations) - Shifts bits left by two, inserting C and Z as new LSBs.
:::

**RCZL**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are shifted left by two places and C and Z are inserted as new LSBs.

- Dest is a register containing the value to rotate.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 001101011 | D | D[31] | D[30] | 2 |


**Related:** [RCZR](#rczr), [RCL](#rcl), [RCR](#rcr)

**Explanation:**

RCZL shifts Dest's binary value left by two places and sets Dest[1] to C and Dest[0] to Z.

If the WC or WCZ effect is specified, the C flag is updated to the original Dest[31] state.

If the WZ or WCZ effect is specified, the Z flag is updated to the original Dest[30] state.

This instruction provides a compact way to shift two flag states into a register while simultaneously extracting two bits from the register into the flags, enabling efficient state serialization and deserialization.



::: instrheader
## RCZR {#rczr}
Rotate Carry And Zero Right

[Arithmetic Operations](#arithmetic-operations) - Shifts bits right by two, inserting C and Z as new MSBs.
:::

**RCZR**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are shifted right by two places and C and Z are inserted as new MSBs.

- Dest is a register containing the value to rotate.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 001101010 | D | D[1] | D[0] | 2 |


**Related:** [RCZL](#rczl), [RCL](#rcl), [RCR](#rcr)

**Explanation:**

RCZR shifts Dest's binary value right by two places and sets Dest[31] to C and Dest[30] to Z.

If the WC or WCZ effect is specified, the C flag is updated to the original Dest[1] state.

If the WZ or WCZ effect is specified, the Z flag is updated to the original Dest[0] state.

This instruction provides a compact way to shift two flag states into a register while simultaneously extracting two bits from the register into the flags, enabling efficient state serialization and deserialization.



::: instrheader
## RDBYTE {#rdbyte}
Read Byte From Hub

[Hub Memory Access](#hub-memory-access) - Reads a zero-extended byte from Hub memory into a register.
:::

**RDBYTE**  *Dest, {#}Src/Ptr*  **{WC|WZ|WCZ}**

---

**Result:** A zero-extended byte from Hub address Src or pointer (PTRA/PTRB) is loaded into Dest.

- Dest is the register to receive the byte value.
- Src/Ptr is a Hub address from register, immediate value, or pointer register (PTRA/PTRB).
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010110 | CZI | DDDDDDDDD | SSSSSSSSS | D | MSB of byte | Result = 0 | 9...16 |


**Related:** [RDWORD](#rdword), [RDLONG](#rdlong), [WRBYTE](#wrbyte)

**Explanation:**

RDBYTE reads a byte from Hub memory at the address specified by Src (or pointer register) and loads it into Dest with zero extension (bits 31:8 are cleared to 0). The operation takes 9-16 clock cycles depending on Hub timing, as the cog must wait for its Hub access window.

If preceded by a SETQ instruction, burst reads of multiple bytes can be performed.

If the WC or WCZ effect is specified, C is set to the MSB of the byte.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.

Hub memory operations follow a round-robin access pattern where each cog gets a regular time slot. The actual latency depends on when the request arrives relative to the cog's assigned slot.



::: instrheader
## RDFAST {#rdfast}
Read Fast Via FIFO

[Hub Memory Access](#hub-memory-access) - Begins fast Hub read operation via FIFO for high-throughput streaming.
:::

**RDFAST**  *{#}Dest, {#}Src*

---

**Result:** A fast read operation begins, filling the FIFO with data from Hub memory starting at address Src.

- Dest is a configuration value: Dest[31] = no-wait mode, Dest[13:0] = block size in 64-byte units (0 = maximum).
- Src is the Hub memory start address (Src[19:0]) for the read operation.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100011 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 or WRFAST finish + 10...17 |


**Related:** [RFBYTE](#rfbyte), [RFWORD](#rfword), [RFLONG](#rflong), [WRFAST](#wrfast), [FBLOCK](#fblock)

**Explanation:**

RDFAST begins a new fast Hub read operation via the FIFO. The instruction configures automatic sequential reading from Hub memory with background FIFO refill, enabling high-throughput streaming data processing.

Dest[31] = 1 enables no-wait mode, which prevents stalls when the FIFO is being filled. Dest[13:0] specifies the block size in 64-byte units, with 0 indicating maximum size (16384 longs). Src[19:0] specifies the starting Hub address. The FIFO automatically wraps at the block boundary.

After RDFAST is executed, subsequent RFBYTE, RFWORD, or RFLONG instructions read data from the FIFO. The FIFO is automatically refilled in the background, making this ideal for checksums, CRC calculations, data processing, and block copy operations.



::: instrheader
## RDLONG {#rdlong}
Read Long From Hub

[Hub Memory Access](#hub-memory-access) - Reads a 32-bit long from Hub memory into a register.
:::

**RDLONG**  *Dest, {#}Src/Ptr*  **{WC|WZ|WCZ}**

---

**Result:** A long from Hub address Src or pointer (PTRA/PTRB) is loaded into Dest.

- Dest is the register to receive the long value.
- Src/Ptr is a Hub address from register, immediate value, or pointer register (PTRA/PTRB).
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011000 | CZI | DDDDDDDDD | SSSSSSSSS | D | MSB of long | --- | 9...16 |


**Related:** [RDBYTE](#rdbyte), [RDWORD](#rdword), [WRLONG](#wrlong)

**Explanation:**

RDLONG reads a long from Hub memory at the address specified by Src (or pointer register) and loads it into Dest. The operation takes 9-16 clock cycles depending on Hub timing, as the cog must wait for its Hub access window.

If preceded by a SETQ instruction, burst reads of multiple longs can be performed.

If the WC or WCZ effect is specified, C is set to the MSB of the long.

Hub memory operations follow a round-robin access pattern where each cog gets a regular time slot.



::: instrheader
## RDLUT {#rdlut}
Read From LUT

[Lookup Table](#lookup-table) - Reads data from the cog's lookup table memory.
:::

**RDLUT**  *Dest, {#}Src/Ptr*  **{WC|WZ|WCZ}**

---

**Result:** Data from LUT address Src or pointer (PTRA/PTRB) is loaded into Dest.

- Dest is the register to receive the data.
- Src/Ptr is a LUT address from register, immediate value, or pointer register (PTRA/PTRB).
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010101 | CZI | DDDDDDDDD | SSSSSSSSS | D | MSB of data | Result = 0 | 3 |


**Related:** [WRLUT](#wrlut), [RDLONG](#rdlong)

**Explanation:**

RDLUT reads data from the Lookup Table at the address specified by Src (or pointer register) and loads it into Dest. The LUT is a 512-long (2KB) memory area in each cog that can be used for lookup tables, buffers, or general-purpose memory. The operation takes 3 clock cycles.

If the WC or WCZ effect is specified, C is set to the MSB of the data.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.

The LUT provides fast local memory access for frequently accessed data structures, making it ideal for sin/cos tables, gamma correction tables, and small data buffers.



::: instrheader
## RDPIN {#rdpin}
Read Smart Pin

[Pin I/O and Smart Pins](#pin-io-and-smart-pins) - Reads Smart Pin result and acknowledges, clearing the ready flag.
:::

**RDPIN**  *Dest, {#}Src*  **{WC}**

---

**Result:** Smart Pin Src[5:0] result is loaded into Dest, and the pin is acknowledged.

- Dest is the register to receive the pin result.
- Src is a register or literal identifying the pin number (Src[5:0]) to read from.
- WC is an optional effect to write the modal result to C.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010100 | C1I | DDDDDDDDD | SSSSSSSSS | D | Modal result | --- | 2 |


**Related:** [RQPIN](#rqpin), [WRPIN](#wrpin), [WXPIN](#wxpin), [WYPIN](#wypin)

**Explanation:**

RDPIN reads the result value from the specified Smart Pin and acknowledges the pin, clearing its "ready" flag. The result value depends on the pin's configured mode and represents measurement data such as pulse width, period, edge count, ADC value, or serial data.

If the WC effect is specified, the C flag is set to the modal result, which provides mode-specific status information.

Smart Pins are powerful autonomous I/O processors that can measure timing, count edges, perform A/D conversion, generate PWM, and communicate serially without continuous CPU intervention. RDPIN retrieves the measured or received data after the pin signals completion.



::: instrheader
## RDWORD {#rdword}
Read Word From Hub

[Hub Memory Access](#hub-memory-access) - Reads a zero-extended word from Hub memory into a register.
:::

**RDWORD**  *Dest, {#}Src/Ptr*  **{WC|WZ|WCZ}**

---

**Result:** A zero-extended word from Hub address Src or pointer (PTRA/PTRB) is loaded into Dest.

- Dest is the register to receive the word value.
- Src/Ptr is a Hub address from register, immediate value, or pointer register (PTRA/PTRB).
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010111 | CZI | DDDDDDDDD | SSSSSSSSS | D | MSB of word | Result = 0 | 9...16 |


**Related:** [RDBYTE](#rdbyte), [RDLONG](#rdlong), [WRWORD](#wrword)

**Explanation:**

RDWORD reads a word from Hub memory at the address specified by Src (or pointer register) and loads it into Dest with zero extension (bits 31:16 are cleared to 0). The operation takes 9-16 clock cycles depending on Hub timing, as the cog must wait for its Hub access window.

If preceded by a SETQ instruction, burst reads of multiple words can be performed.

If the WC or WCZ effect is specified, C is set to the MSB of the word.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.



::: instrheader
## REP {#rep}
Repeat Block

[Branching and Flow Control](#branching-and-flow-control) - Creates a zero-overhead hardware loop for repeated execution.
:::

**REP**  *{#}Dest, {#}Src*

---

**Result:** The next Dest[8:0] instructions are executed Src times.

- Dest is the number of instructions to repeat (Dest[8:0], 0-511). If Dest[8:0] = 0, nothing repeats.
- Src is the number of repetitions. If Src = 0, instructions repeat infinitely.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100110 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 |


**Related:** [DJNZ](#djnz), [JNCT1/2/3](#jnct1)

**Explanation:**

REP creates a hardware-implemented loop that executes the next Dest[8:0] instructions Src times. If Src = 0, the instructions repeat infinitely (useful for main loops). If Dest[8:0] = 0, nothing repeats.

The REP instruction itself takes 2 cycles, and the repeated instructions execute with zero overhead—no jump penalty, no counter decrement. This makes REP ideal for time-critical inner loops.

REP blocks can be nested up to 3 levels deep, allowing complex loop structures. Interrupts are blocked during REP execution to maintain timing precision. The zero-overhead nature of REP makes it essential for high-performance applications like DSP algorithms, graphics rendering, and precise timing operations.



::: instrheader
## RESI0 / RESI1 / RESI2 / RESI3 {#resi0}
Resume From Interrupt {#resi1} {#resi2} {#resi3}

[Interrupts](#interrupts) - Resumes execution from an interrupted location.
:::

**RESI0**
**RESI1**
**RESI2**
**RESI3**

---

**Result:** Execution resumes from the interrupted location for the specified interrupt level.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011001 | 110 | 111111110 | 111111111 | --- | --- | --- | 4 (COG), 13...20 (Hub) |
| EEEE | 1011001 | 110 | 111110100 | 111110101 | --- | --- | --- | 4 (COG), 13...20 (Hub) |
| EEEE | 1011001 | 110 | 111110010 | 111110011 | --- | --- | --- | 4 (COG), 13...20 (Hub) |
| EEEE | 1011001 | 110 | 111110000 | 111110001 | --- | --- | --- | 4 (COG), 13...20 (Hub) |


**Related:** [RETI0/1/2/3](#reti0), [SETINT1/2/3](#setint1), [NIXINT1/2/3](#nixint1)

**Explanation:**

RESI0, RESI1, RESI2, and RESI3 resume execution from their respective interrupt levels. Each instruction is functionally equivalent to a CALLD instruction that restores the program counter, C flag, and Z flag from the corresponding interrupt return address registers.

Unlike RETIx instructions which return from the interrupt handler, RESIx instructions resume interrupted execution, used when an interrupt handler needs to yield to another interrupt priority level before completion.



::: instrheader
## RET {#ret}
Return From Subroutine

[Branching and Flow Control](#branching-and-flow-control) - Returns from subroutine by popping the hardware stack.
:::

**RET**  **{WC|WZ|WCZ}**

---

**Result:** The program counter, C flag, and Z flag are restored from the top of the hardware stack.

- WC, WZ, or WCZ are optional effects to restore flags from the stack.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ1 | 000000000 | 000101101 | --- | K[31] | K[30] | 4 |


**Related:** [CALL](#call), [CALLA](#calla), [CALLB](#callb), [RETA](#reta), [RETB](#retb)

**Explanation:**

RET returns from a subroutine by popping the hardware stack (K register). The program counter is restored from K[19:0].

If the WC or WCZ effect is specified, the C flag is restored from K[31].

If the WZ or WCZ effect is specified, the Z flag is restored from K[30].

The operation takes 4 cycles minimum, with variable timing depending on Hub access if the return location is in Hub memory (13-20 cycles).

The P2 provides an 8-level hardware stack for fast subroutine calls. RET is paired with CALL, CALLPA, CALLPB, CALLA, and CALLB instructions.



::: instrheader
## RETA {#reta}
Return Via PTRA Stack

[Branching and Flow Control](#branching-and-flow-control) - Returns from subroutine using PTRA as software stack pointer.
:::

**RETA**  **{WC|WZ|WCZ}**

---

**Result:** The program counter, C flag, and Z flag are restored from Hub memory at --PTRA.

- WC, WZ, or WCZ are optional effects to restore flags from the stack.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ1 | 000000000 | 000101110 | --- | L[31] | L[30] | 11...18 |


**Related:** [CALLA](#calla), [RET](#ret), [RETB](#retb)

**Explanation:**

RETA returns from a subroutine by reading a Hub long from --PTRA. PTRA is pre-decremented by 4 bytes, then a long is read from that address. The program counter is restored from L[19:0].

If the WC or WCZ effect is specified, the C flag is restored from L[31].

If the WZ or WCZ effect is specified, the Z flag is restored from L[30].

RETA is paired with CALLA for implementing software stacks in Hub memory, enabling deep call nesting beyond the 8-level hardware stack limit.



::: instrheader
## RETB {#retb}
Return Via PTRB Stack

[Branching and Flow Control](#branching-and-flow-control) - Returns from subroutine using PTRB as software stack pointer.
:::

**RETB**  **{WC|WZ|WCZ}**

---

**Result:** The program counter, C flag, and Z flag are restored from Hub memory at --PTRB.

- WC, WZ, or WCZ are optional effects to restore flags from the stack.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ1 | 000000000 | 000101111 | --- | L[31] | L[30] | 11...18 |


**Related:** [CALLB](#callb), [RET](#ret), [RETA](#reta)

**Explanation:**

RETB returns from a subroutine by reading a Hub long from --PTRB. PTRB is pre-decremented by 4 bytes, then a long is read from that address. The program counter is restored from L[19:0].

If the WC or WCZ effect is specified, the C flag is restored from L[31].

If the WZ or WCZ effect is specified, the Z flag is restored from L[30].

RETB is paired with CALLB for implementing software stacks in Hub memory, enabling deep call nesting beyond the 8-level hardware stack limit.



::: instrheader
## RETI0 / RETI1 / RETI2 / RETI3 {#reti0}
Return From Interrupt {#reti1} {#reti2} {#reti3}

[Interrupts](#interrupts) - Returns from interrupt handler to interrupted location.
:::

**RETI0**
**RETI1**
**RETI2**
**RETI3**

---

**Result:** Execution returns from the specified interrupt level to the interrupted location.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011001 | 110 | 111111111 | 111111111 | --- | --- | --- | 4 (COG), 13...20 (Hub) |
| EEEE | 1011001 | 110 | 111111111 | 111110101 | --- | --- | --- | 4 (COG), 13...20 (Hub) |
| EEEE | 1011001 | 110 | 111111111 | 111110011 | --- | --- | --- | 4 (COG), 13...20 (Hub) |
| EEEE | 1011001 | 110 | 111111111 | 111110001 | --- | --- | --- | 4 (COG), 13...20 (Hub) |


**Related:** [RESI0/1/2/3](#resi0), [SETINT1/2/3](#setint1), [NIXINT1/2/3](#nixint1)

**Explanation:**

RETI0, RETI1, RETI2, and RETI3 return from their respective interrupt handlers. Each instruction is functionally equivalent to a CALLD instruction that restores the program counter, C flag, and Z flag from the corresponding interrupt return address registers.

The P2 provides four interrupt levels (INT0-INT3), with INT0 being the lowest priority and INT3 being the highest. Each RETI instruction completes its interrupt handler and resumes normal execution at the point where the interrupt occurred.



::: instrheader
## REV {#rev}
Reverse Bits

[Arithmetic Operations](#arithmetic-operations) - Reverses all 32 bits in a register.
:::

**REV**  *Dest*

---

**Result:** The 32-bit pattern in Dest is reversed (bits 31:0 become bits 0:31).

- Dest is the register containing the bit pattern to reverse.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001101001 | D | --- | --- | 2 |


**Related:** [ROL](#rol), [ROR](#ror), [ZEROX](#zerox)

**Explanation:**

REV performs a complete bitwise reverse of the value in Dest, storing the result back into Dest. Bit 31 becomes bit 0, bit 30 becomes bit 1, and so on through bit 0 becoming bit 31. The operation takes 2 cycles and does not affect any flags.

This instruction is useful for processing binary data in different MSB/LSB order than it is transmitted with, such as serial protocols that send least-significant bit first but need processing in most-significant bit first order. It is also used in bit-reversal algorithms for FFT operations.



::: instrheader
## RFBYTE {#rfbyte}
Read Byte Via FIFO

[Hub Memory Access](#hub-memory-access) - Reads a zero-extended byte from the RDFAST FIFO.
:::

**RFBYTE**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** A zero-extended byte from the FIFO is loaded into Dest.

- Dest is the register to receive the byte value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000010000 | D | MSB of byte | Result = 0 | 2 |


**Related:** [RDFAST](#rdfast), [RFWORD](#rfword), [RFLONG](#rflong), [RFVAR](#rfvar)

**Explanation:**

RFBYTE is used after RDFAST to read zero-extended bytes from the FIFO. The byte is loaded into Dest with bits 31:8 cleared to 0.

If the WC or WCZ effect is specified, C is set to the MSB of the byte.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.

The operation takes 2 cycles when the FIFO has data available. The FIFO is automatically refilled in the background by the RDFAST operation.



::: instrheader
## RFLONG {#rflong}
Read Long Via FIFO

[Hub Memory Access](#hub-memory-access) - Reads a 32-bit long from the RDFAST FIFO.
:::

**RFLONG**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** A long from the FIFO is loaded into Dest.

- Dest is the register to receive the long value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000010010 | D | MSB of long | Result = 0 | 2 |


**Related:** [RDFAST](#rdfast), [RFBYTE](#rfbyte), [RFWORD](#rfword), [RFVAR](#rfvar)

**Explanation:**

RFLONG is used after RDFAST to read longs from the FIFO.

If the WC or WCZ effect is specified, C is set to the MSB of the long.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.

The operation takes 2 cycles when the FIFO has data available. The FIFO is automatically refilled in the background by the RDFAST operation.



::: instrheader
## RFVAR {#rfvar}
Read Variable Via FIFO

[Hub Memory Access](#hub-memory-access) - Reads a zero-extended 1-4 byte value from the RDFAST FIFO.
:::

**RFVAR**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** A zero-extended 1-4 byte value from the FIFO is loaded into Dest.

- Dest is the register to receive the variable-length value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000010011 | D | 0 | Result = 0 | 2 |


**Related:** [RDFAST](#rdfast), [RFBYTE](#rfbyte), [RFVARS](#rfvars)

**Explanation:**

RFVAR is used after RDFAST to read variable-length values (1-4 bytes) from the FIFO with zero extension. The value is loaded into Dest with upper bits cleared to 0.

If the WC or WCZ effect is specified, C is always cleared to 0.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.

The length of each value read is determined by the streamer configuration set up before the RDFAST operation.



::: instrheader
## RFVARS {#rfvars}
Read Signed Variable Via FIFO

[Hub Memory Access](#hub-memory-access) - Reads a sign-extended 1-4 byte value from the RDFAST FIFO.
:::

**RFVARS**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** A sign-extended 1-4 byte value from the FIFO is loaded into Dest.

- Dest is the register to receive the sign-extended value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000010100 | D | MSB of value | Result = 0 | 2 |


**Related:** [RDFAST](#rdfast), [RFVAR](#rfvar), [RFBYTE](#rfbyte)

**Explanation:**

RFVARS is used after RDFAST to read variable-length values (1-4 bytes) from the FIFO with sign extension. The value is loaded into Dest with upper bits set according to the MSB of the value (sign extension).

If the WC or WCZ effect is specified, C is set to the MSB of the value.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.



::: instrheader
## RFWORD {#rfword}
Read Word Via FIFO

[Hub Memory Access](#hub-memory-access) - Reads a zero-extended word from the RDFAST FIFO.
:::

**RFWORD**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** A zero-extended word from the FIFO is loaded into Dest.

- Dest is the register to receive the word value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000010001 | D | MSB of word | Result = 0 | 2 |


**Related:** [RDFAST](#rdfast), [RFBYTE](#rfbyte), [RFLONG](#rflong), [RFVAR](#rfvar)

**Explanation:**

RFWORD is used after RDFAST to read zero-extended words from the FIFO. The word is loaded into Dest with bits 31:16 cleared to 0.

If the WC or WCZ effect is specified, C is set to the MSB of the word.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.

The operation takes 2 cycles when the FIFO has data available.



::: instrheader
## RGBEXP {#rgbexp}
Expand RGB Color

[Color Space and Pixel Operations](#color-space-and-pixel-operations) - Expands 5:6:5 RGB color to 8:8:8 format.
:::

**RGBEXP**  *Dest*

---

**Result:** The 5:6:5 RGB value in Dest[15:0] is expanded into 8:8:8 format in Dest[31:8].

- Dest contains 5:6:5 RGB in Dest[15:0], receives 8:8:8 RGB in Dest[31:8].


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001100111 | D | --- | --- | 2 |


**Related:** [RGBSQZ](#rgbsqz)

**Explanation:**

RGBEXP expands a compact 5:6:5 RGB color value (commonly used in 16-bit color displays) into full 8:8:8 RGB format (24-bit true color). The input 5:6:5 value is in Dest[15:0] with 5 bits red, 6 bits green, and 5 bits blue. The output 8:8:8 value is placed in Dest[31:8] with 8 bits each for red, green, and blue. The expansion replicates the most significant bits into the lower bits to maintain color accuracy.

This instruction is useful when converting between 16-bit and 24-bit color formats for graphics processing.



::: instrheader
## RGBSQZ {#rgbsqz}
Squeeze RGB Color

[Color Space and Pixel Operations](#color-space-and-pixel-operations) - Compresses 8:8:8 RGB color to 5:6:5 format.
:::

**RGBSQZ**  *Dest*

---

**Result:** The 8:8:8 RGB value in Dest[31:8] is compressed into 5:6:5 format in Dest[15:0].

- Dest contains 8:8:8 RGB in Dest[31:8], receives 5:6:5 RGB in Dest[15:0].


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001100110 | D | --- | --- | 2 |


**Related:** [RGBEXP](#rgbexp)

**Explanation:**

RGBSQZ compresses a full 8:8:8 RGB color value (24-bit true color) into compact 5:6:5 format (16-bit color). The input 8:8:8 value is in Dest[31:8] with 8 bits each for red, green, and blue. The output 5:6:5 value is placed in Dest[15:0] with 5 bits red, 6 bits green, and 5 bits blue. The compression keeps the most significant bits of each color channel.

This instruction is useful when converting from 24-bit to 16-bit color formats for display output.



::: instrheader
## ROL {#rol}
Rotate Left

[Arithmetic Operations](#arithmetic-operations) - Rotates bits left, wrapping MSBs to LSBs.
:::

**ROL**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are rotated left by Src positions; departing MSBs are moved into LSBs.

- Dest is the register containing the value to rotate left.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to rotate.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0000001 | CZI | DDDDDDDDD | SSSSSSSSS | D | Last bit out\textsuperscript{1} | Result = 0 | 2 |


**Related:** [ROR](#ror), [RCL](#rcl), [RCR](#rcr), [SHL](#shl)

**Explanation:**

ROL rotates Dest's binary value left by Src places (0-31 bits). All MSBs rotated out are moved into the new LSBs.

If the WC or WCZ effect is specified, the C flag is updated to the value of the last bit rotated out if Src is 1-31, or to Dest[31] if Src is 0.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if non-zero. Since no bits are lost by this operation, the result will only be zero if Dest started at zero.

Rotation is useful for bit manipulation, circular buffers, hash functions, and cryptographic operations.



::: instrheader
## ROLBYTE {#rolbyte}
Rotate Byte Left Into Register

[Arithmetic Operations](#arithmetic-operations) - Rotates a byte from source into destination register.
:::

**ROLBYTE**  *Dest, {#}Src, #N*
**ROLBYTE**  *Dest*

---

**Result:** Byte N (0-3) of Src, or a byte from a source described by prior ALTGB instruction, is rotated left into Dest.

- Dest is the register into which the byte is rotated.
- Src is a register, 9-bit literal, or 32-bit augmented literal containing the target byte.
- N is a 2-bit literal (0-3) identifying the byte position in Src.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001000 | NNI | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |
| EEEE | 1001000 | 000 | DDDDDDDDD | 000000000 | D | --- | --- | 2 |


**Related:** [ROLNIB](#rolnib), [ROLWORD](#rolword), [GETBYTE](#getbyte), [SETBYTE](#setbyte), [ALTGB](#altgb)

**Explanation:**

ROLBYTE reads the byte identified by N (0-3) from Src, or a byte from the source described by a prior ALTGB instruction, and rotates it left into Dest. ROLBYTE achieves the same effect as two instructions: an 8-bit SHL followed by SETBYTE into byte 0.

The second syntax form is intended for use after an ALTGB instruction in a loop to iteratively read a series of byte values within contiguous long registers.



::: instrheader
## ROLNIB {#rolnib}
Rotate Nibble Left Into Register

[Arithmetic Operations](#arithmetic-operations) - Rotates a nibble from source into destination register.
:::

**ROLNIB**  *Dest, {#}Src, #N*
**ROLNIB**  *Dest*

---

**Result:** Nibble N (0-7) of Src, or a nibble from a source described by prior ALTGN instruction, is rotated left into Dest.

- Dest is the register into which the nibble is rotated.
- Src is a register, 9-bit literal, or 32-bit augmented literal containing the target nibble.
- N is a 3-bit literal (0-7) identifying the nibble position in Src.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 100010N | NNI | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |
| EEEE | 1000100 | 000 | DDDDDDDDD | 000000000 | D | --- | --- | 2 |


**Related:** [ROLBYTE](#rolbyte), [ROLWORD](#rolword), [GETNIB](#getnib), [SETNIB](#setnib), [ALTGN](#altgn)

**Explanation:**

ROLNIB reads the nibble identified by N (0-7) from Src, or a nibble from the source described by a prior ALTGN instruction, and rotates it left into Dest. ROLNIB achieves the same effect as two instructions: a 4-bit SHL followed by SETNIB into nibble 0.

The second syntax form is intended for use after an ALTGN instruction in a loop to iteratively read a series of nibble values within contiguous long registers.



::: instrheader
## ROLWORD {#rolword}
Rotate Word Left Into Register

[Arithmetic Operations](#arithmetic-operations) - Rotates a word from source into destination register.
:::

**ROLWORD**  *Dest, {#}Src, #N*
**ROLWORD**  *Dest*

---

**Result:** Word N (0-1) of Src, or a word from a source described by prior ALTGW instruction, is rotated left into Dest.

- Dest is the register into which the word is rotated.
- Src is a register, 9-bit literal, or 32-bit augmented literal containing the target word.
- N is a 1-bit literal (0-1) identifying the word position in Src.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001010 | 0NI | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |
| EEEE | 1001010 | 000 | DDDDDDDDD | 000000000 | D | --- | --- | 2 |


**Related:** [ROLBYTE](#rolbyte), [ROLNIB](#rolnib), [GETWORD](#getword), [SETWORD](#setword), [ALTGW](#altgw)

**Explanation:**

ROLWORD reads the word identified by N (0-1) from Src, or a word from the source described by a prior ALTGW instruction, and rotates it left into Dest. ROLWORD achieves the same effect as two instructions: a 16-bit SHL followed by SETWORD into word 0.

The second syntax form is intended for use after an ALTGW instruction in a loop to iteratively read a series of word values within contiguous long registers.



::: instrheader
## ROR {#ror}
Rotate Right

[Arithmetic Operations](#arithmetic-operations) - Rotates bits right, wrapping LSBs to MSBs.
:::

**ROR**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are rotated right by Src positions; departing LSBs are moved into MSBs.

- Dest is the register containing the value to rotate right.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to rotate.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0000000 | CZI | DDDDDDDDD | SSSSSSSSS | D | Last bit out\textsuperscript{1} | Result = 0 | 2 |


**Related:** [ROL](#rol), [RCL](#rcl), [RCR](#rcr), [SHR](#shr)

**Explanation:**

ROR rotates Dest's binary value right by Src places (0-31 bits). All LSBs rotated out are moved into the new MSBs.

If the WC or WCZ effect is specified, the C flag is updated to the value of the last bit rotated out if Src is 1-31, or to Dest[0] if Src is 0.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if non-zero. Since no bits are lost by this operation, the result will only be zero if Dest started at zero.

Rotation is useful for bit manipulation, circular buffers, hash functions, and cryptographic operations.



::: instrheader
## RQPIN {#rqpin}
Read Smart Pin Without Acknowledge

[Pin I/O and Smart Pins](#pin-io-and-smart-pins) - Reads Smart Pin result without clearing the ready flag.
:::

**RQPIN**  *Dest, {#}Src*  **{WC}**

---

**Result:** Smart Pin Src[5:0] result is loaded into Dest without clearing the pin's ready flag.

- Dest is the register to receive the pin result.
- Src is a register or literal identifying the pin number (Src[5:0]) to read from.
- WC is an optional effect to write the modal result to C.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010100 | C0I | DDDDDDDDD | SSSSSSSSS | D | Modal result | --- | 2 |


**Related:** [RDPIN](#rdpin), [WRPIN](#wrpin), [WXPIN](#wxpin), [WYPIN](#wypin)

**Explanation:**

RQPIN reads the result value from the specified Smart Pin without acknowledging the pin. Unlike RDPIN, this instruction does not clear the pin's "ready" flag, allowing the same result to be read multiple times or checked before being consumed.

If the WC effect is specified, the C flag is set to the modal result, which provides mode-specific status information.

This instruction is useful when you need to check a pin's result value without consuming it, such as polling for completion before actually processing the result.

