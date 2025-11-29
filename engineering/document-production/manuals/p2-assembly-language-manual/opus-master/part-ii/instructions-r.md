# R Instructions

## RCL — Rotate Carry Left

Rotates the bits of Dest left by Src positions, inserting the carry flag as new LSBs.

### Syntax
```pasm
        RCL     D,{#}S {WC|WZ|WCZ}
```

### Result
The bits of Dest are shifted left by Src bits, inserting C as new LSBs.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the value to rotate carry left by S bits |
| S | Register or 5-bit literal (0-31) indicating the number of bit positions to rotate |
| WC/WZ/WCZ | Optional flags: write carry, write zero, or both |

### Encoding
\simpleencoding{EEEE 0000101 CZI DDDDDDDDD SSSSSSSSS | D | Last bit out¹ | Result = 0 | 2}

¹ C = last bit shifted out if S[4:0] > 0, else D[31]

### Related Instructions
- [RCR](#rcr) — Rotate carry right
- [ROL](#rol) — Rotate left
- [ROR](#ror) — Rotate right

### Explanation
RCL shifts Dest's binary value left by Src places (0-31 bits) and sets the new LSBs to C. The carry flag acts as an extension of the register, allowing 33-bit rotations. If the WC or WCZ effect is specified, the C flag is updated to the value of the last bit shifted out if Src is 1-31, or to Dest[31] if Src is 0. If the WZ or WCZ effect is specified, the Z flag is set if the Dest result equals zero, or is cleared if it is non-zero.

This instruction is useful for multi-precision arithmetic operations where the carry from one word needs to be propagated into the next word.

---

## RCR — Rotate Carry Right

Rotates the bits of Dest right by Src positions, inserting the carry flag as new MSBs.

### Syntax
```pasm
        RCR     D,{#}S {WC|WZ|WCZ}
```

### Result
The bits of Dest are shifted right by Src bits, inserting C as new MSBs.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the value to rotate carry right by S bits |
| S | Register or 5-bit literal (0-31) indicating the number of bit positions to rotate |
| WC/WZ/WCZ | Optional flags: write carry, write zero, or both |

### Encoding
\simpleencoding{EEEE 0000100 CZI DDDDDDDDD SSSSSSSSS | D | Last bit out¹ | Result = 0 | 2}

¹ C = last bit shifted out if S[4:0] > 0, else D[0]

### Related Instructions
- [RCL](#rcl) — Rotate carry left
- [ROL](#rol) — Rotate left
- [ROR](#ror) — Rotate right

### Explanation
RCR shifts Dest's binary value right by Src places (0-31 bits) and sets the new MSBs to C. The carry flag acts as an extension of the register, allowing 33-bit rotations. If the WC or WCZ effect is specified, the C flag is updated to the value of the last bit shifted out if Src is 1-31, or to Dest[0] if Src is 0. If the WZ or WCZ effect is specified, the Z flag is set if the Dest result equals zero, or is cleared if it is non-zero.

This instruction is useful for multi-precision arithmetic operations where the carry needs to be propagated through multiple words.

---

## RCZL — Rotate Carry and Zero Left

Rotates Dest left by two bit positions, inserting carry and zero flags as new LSBs.

### Syntax
```pasm
        RCZL    D {WC|WZ|WCZ}
```

### Result
The bits of Dest are shifted left by two places and C and Z are inserted as new LSBs.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the value to rotate the carry and zero flags left into |
| WC/WZ/WCZ | Optional flags: write carry, write zero, or both |

### Encoding
\simpleencoding{EEEE 1101011 CZ0 DDDDDDDDD 001101011 | D | D[31] | D[30] | 2}

### Related Instructions
- [RCZR](#rczr) — Rotate carry and zero right
- [RCL](#rcl) — Rotate carry left
- [RCR](#rcr) — Rotate carry right

### Explanation
RCZL shifts Dest's binary value left by two places and sets Dest[1] to C and Dest[0] to Z. If the WC or WCZ effect is specified, the C flag is updated to the original Dest[31] state. If the WZ or WCZ effect is specified, the Z flag is updated to the original Dest[30] state.

This instruction provides a compact way to shift two flag states into a register while simultaneously extracting two bits from the register into the flags, enabling efficient state serialization and deserialization.

---

## RCZR — Rotate Carry and Zero Right

Rotates Dest right by two bit positions, inserting carry and zero flags as new MSBs.

### Syntax
```pasm
        RCZR    D {WC|WZ|WCZ}
```

### Result
The bits of Dest are shifted right by two places and C and Z are inserted as new MSBs.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the value to rotate the carry and zero flags right into |
| WC/WZ/WCZ | Optional flags: write carry, write zero, or both |

### Encoding
\simpleencoding{EEEE 1101011 CZ0 DDDDDDDDD 001101010 | D | D[1] | D[0] | 2}

### Related Instructions
- [RCZL](#rczl) — Rotate carry and zero left
- [RCL](#rcl) — Rotate carry left
- [RCR](#rcr) — Rotate carry right

### Explanation
RCZR shifts Dest's binary value right by two places and sets Dest[31] to C and Dest[30] to Z. If the WC or WCZ effect is specified, the C flag is updated to the original Dest[1] state. If the WZ or WCZ effect is specified, the Z flag is updated to the original Dest[0] state.

This instruction provides a compact way to shift two flag states into a register while simultaneously extracting two bits from the register into the flags, enabling efficient state serialization and deserialization.

---

## RDBYTE — Read Byte from Hub RAM

Reads a zero-extended byte from hub memory into a cog register.

### Syntax
```pasm
        RDBYTE  D,{#}S/P {WC|WZ|WCZ}
```

### Result
A zero-extended byte from hub address S or pointer (PTRA/PTRB) is loaded into D.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Destination register to receive the byte value |
| S/P | Hub address from register, immediate value, or pointer register (PTRA/PTRB) |
| WC/WZ/WCZ | Optional flags: write carry, write zero, or both |

### Encoding
\simpleencoding{EEEE 1010110 CZI DDDDDDDDD SSSSSSSSS | D | MSB of byte | Result = 0 | 9...16}

### Related Instructions
- [RDWORD](#rdword) — Read word from hub RAM
- [RDLONG](#rdlong) — Read long from hub RAM
- [WRBYTE](#wrbyte) — Write byte to hub RAM

### Explanation
RDBYTE reads a byte from hub memory at the address specified by S (or pointer register) and loads it into D with zero extension (bits 31:8 are cleared to 0). The operation takes 9-16 clock cycles depending on hub timing, as the cog must wait for its hub access window. If preceded by a SETQ instruction, burst reads of multiple bytes can be performed. If the WC flag is specified, C is set to the MSB of the byte. If the WZ flag is specified, Z is set if the result equals zero.

Hub memory operations follow a round-robin access pattern where each cog gets a regular time slot. The actual latency depends on when the request arrives relative to the cog's assigned slot, resulting in the variable 9-16 cycle range.

---

## RDFAST — Begin Fast Hub Read via FIFO

Initiates a fast sequential read from hub memory into the FIFO buffer for streaming operations.

### Syntax
```pasm
        RDFAST  {#}D,{#}S
```

### Result
A fast read operation begins, filling the FIFO with data from hub memory starting at address S.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Configuration value: D[31] = no-wait mode, D[13:0] = block size in 64-byte units (0 = maximum) |
| S | Hub memory start address (S[19:0]) for the read operation |

### Encoding
\simpleencoding{EEEE 1100011 1LI DDDDDDDDD SSSSSSSSS | — | — | — | 2 or WRFAST finish + 10...17}

### Related Instructions
- [RFBYTE](#rfbyte) — Read byte via FIFO
- [RFWORD](#rfword) — Read word via FIFO
- [RFLONG](#rflong) — Read long via FIFO
- [WRFAST](#wrfast) — Begin fast hub write via FIFO
- [FBLOCK](#fblock) — Wait for FIFO block wrap

### Explanation
RDFAST begins a new fast hub read operation via the FIFO. The instruction configures automatic sequential reading from hub memory with background FIFO refill, enabling high-throughput streaming data processing. D[31] = 1 enables no-wait mode, which prevents stalls when the FIFO is being filled. D[13:0] specifies the block size in 64-byte units, with 0 indicating maximum size (16384 longs). S[19:0] specifies the starting hub address. The FIFO automatically wraps at the block boundary.

After RDFAST is executed, subsequent RFBYTE, RFWORD, or RFLONG instructions read data from the FIFO. The FIFO is automatically refilled in the background, making this ideal for checksums, CRC calculations, data processing, and block copy operations. The operation takes 2 cycles if no prior WRFAST is active, otherwise it must wait for the WRFAST to complete (10-17 additional cycles).

RDFAST is essential for high-performance applications that need to process large amounts of hub data efficiently, such as:
- Checksum and CRC calculations over memory blocks
- Audio/video data stream processing
- Fast memory-to-memory transfers when combined with sequential writes
- Serial data encoding/decoding operations

---

## RDLONG — Read Long from Hub RAM

Reads a long (32-bit value) from hub memory into a cog register.

### Syntax
```pasm
        RDLONG  D,{#}S/P {WC|WZ|WCZ}
```

### Result
A long from hub address S or pointer (PTRA/PTRB) is loaded into D.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Destination register to receive the long value |
| S/P | Hub address from register, immediate value, or pointer register (PTRA/PTRB) |
| WC/WZ/WCZ | Optional flags: write carry, write zero, or both |

### Encoding
\simpleencoding{EEEE 1011000 CZI DDDDDDDDD SSSSSSSSS | D | MSB of long | — | 9...16}

### Related Instructions
- [RDBYTE](#rdbyte) — Read byte from hub RAM
- [RDWORD](#rdword) — Read word from hub RAM
- [WRLONG](#wrlong) — Write long to hub RAM

### Explanation
RDLONG reads a long from hub memory at the address specified by S (or pointer register) and loads it into D. The operation takes 9-16 clock cycles depending on hub timing, as the cog must wait for its hub access window. If preceded by a SETQ instruction, burst reads of multiple longs can be performed. If the WC flag is specified, C is set to the MSB of the long.

Hub memory operations follow a round-robin access pattern where each cog gets a regular time slot. The actual latency depends on when the request arrives relative to the cog's assigned slot, resulting in the variable 9-16 cycle range.

---

## RDLUT — Read Data from Lookup Table

Reads a long from the lookup table (LUT) into a cog register.

### Syntax
```pasm
        RDLUT   D,{#}S/P {WC|WZ|WCZ}
```

### Result
Data from LUT address S or pointer (PTRA/PTRB) is loaded into D.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Destination register to receive the data |
| S/P | LUT address from register, immediate value, or pointer register (PTRA/PTRB) |
| WC/WZ/WCZ | Optional flags: write carry, write zero, or both |

### Encoding
\simpleencoding{EEEE 1010101 CZI DDDDDDDDD SSSSSSSSS | D | MSB of data | Result = 0 | 3}

### Related Instructions
- [WRLUT](#wrlut) — Write data to lookup table
- [RDLONG](#rdlong) — Read long from hub RAM

### Explanation
RDLUT reads data from the lookup table at the address specified by S (or pointer register) and loads it into D. The LUT is a 512-long (2KB) memory area in each cog that can be used for lookup tables, buffers, or general-purpose memory. The operation takes 3 clock cycles. If the WC flag is specified, C is set to the MSB of the data. If the WZ flag is specified, Z is set if the result equals zero.

The LUT provides fast local memory access for frequently accessed data structures, making it ideal for sin/cos tables, gamma correction tables, and small data buffers.

---

## RDPIN — Read Smart Pin Result

Reads a smart pin's result value and acknowledges the pin, clearing its ready flag.

### Syntax
```pasm
        RDPIN   D,{#}S {WC}
```

### Result
Smart pin S[5:0] result "Z" is loaded into D, and the pin is acknowledged.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Destination register to receive the pin result |
| S | Pin number (S[5:0]) to read from |
| WC | Optional flag: write carry with modal result |

### Encoding
\simpleencoding{EEEE 1010100 C1I DDDDDDDDD SSSSSSSSS | D | Modal result | — | 2}

### Related Instructions
- [RQPIN](#rqpin) — Read smart pin result without acknowledge
- [WRPIN](#wrpin) — Write smart pin mode
- [WXPIN](#wxpin) — Write smart pin X parameter
- [WYPIN](#wypin) — Write smart pin Y parameter

### Explanation
RDPIN reads the result value from the specified smart pin and acknowledges the pin, clearing its "ready" flag. The result value depends on the pin's configured mode and represents measurement data such as pulse width, period, edge count, ADC value, or serial data. If the WC flag is specified, the C flag is set to the modal result, which provides mode-specific status information.

Smart pins are powerful autonomous I/O processors that can measure timing, count edges, perform A/D conversion, generate PWM, and communicate serially without continuous CPU intervention. RDPIN retrieves the measured or received data after the pin signals completion.

---

## RDWORD — Read Word from Hub RAM

Reads a zero-extended word (16-bit value) from hub memory into a cog register.

### Syntax
```pasm
        RDWORD  D,{#}S/P {WC|WZ|WCZ}
```

### Result
A zero-extended word from hub address S or pointer (PTRA/PTRB) is loaded into D.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Destination register to receive the word value |
| S/P | Hub address from register, immediate value, or pointer register (PTRA/PTRB) |
| WC/WZ/WCZ | Optional flags: write carry, write zero, or both |

### Encoding
\simpleencoding{EEEE 1010111 CZI DDDDDDDDD SSSSSSSSS | D | MSB of word | Result = 0 | 9...16}

### Related Instructions
- [RDBYTE](#rdbyte) — Read byte from hub RAM
- [RDLONG](#rdlong) — Read long from hub RAM
- [WRWORD](#wrword) — Write word to hub RAM

### Explanation
RDWORD reads a word from hub memory at the address specified by S (or pointer register) and loads it into D with zero extension (bits 31:16 are cleared to 0). The operation takes 9-16 clock cycles depending on hub timing, as the cog must wait for its hub access window. If preceded by a SETQ instruction, burst reads of multiple words can be performed. If the WC flag is specified, C is set to the MSB of the word. If the WZ flag is specified, Z is set if the result equals zero.

Hub memory operations follow a round-robin access pattern where each cog gets a regular time slot. The actual latency depends on when the request arrives relative to the cog's assigned slot, resulting in the variable 9-16 cycle range.

---

## REP — Repeat Block

Executes the next D[8:0] instructions S times, creating a hardware loop.

### Syntax
```pasm
        REP     {#}D,{#}S
```

### Result
The next D[8:0] instructions are executed S times.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Number of instructions to repeat (D[8:0], 0-511). If D[8:0] = 0, nothing repeats |
| S | Number of repetitions. If S = 0, instructions repeat infinitely |

### Encoding
\simpleencoding{EEEE 1100110 1LI DDDDDDDDD SSSSSSSSS | — | — | — | 2}

### Related Instructions
- [DJNZ](#djnz) — Decrement and jump if not zero
- [JNCT1](#jnct1) — Jump if CT1 not reached
- [JNCT2](#jnct2) — Jump if CT2 not reached
- [JNCT3](#jnct3) — Jump if CT3 not reached

### Explanation
REP creates a hardware-implemented loop that executes the next D[8:0] instructions S times. If S = 0, the instructions repeat infinitely (useful for main loops). If D[8:0] = 0, nothing repeats. The REP instruction itself takes 2 cycles, and the repeated instructions execute with zero overhead—no jump penalty, no counter decrement. This makes REP ideal for time-critical inner loops.

REP blocks can be nested up to 3 levels deep, allowing complex loop structures. Interrupts are blocked during REP execution to maintain timing precision. The zero-overhead nature of REP makes it essential for high-performance applications like DSP algorithms, graphics rendering, and precise timing operations.

---

## RESI0 — Resume from Interrupt 0

Resumes execution after returning from interrupt 0, restoring flags and program counter.

### Syntax
```pasm
        RESI0
```

### Result
Execution resumes from the interrupted location for interrupt 0.

### Parameters
None.

### Encoding
\simpleencoding{EEEE 1011001 110 111111110 111111111 | D | — | — | 4}

### Related Instructions
- [RESI1](#resi1) — Resume from interrupt 1
- [RESI2](#resi2) — Resume from interrupt 2
- [RESI3](#resi3) — Resume from interrupt 3
- [RETI0](#reti0) — Return from interrupt 0

### Explanation
RESI0 resumes execution from interrupt 0. This is functionally equivalent to CALLD $1FE,$1FF WCZ, which restores the program counter, C flag, and Z flag from the interrupt return address registers. The operation takes 4 cycles minimum, with variable timing depending on hub access if the resume location is in hub memory (13-20 cycles).

Unlike RETIx instructions which return from the interrupt handler, RESIx instructions resume interrupted execution, used when an interrupt handler needs to yield to another interrupt priority level before completion.

---

## RESI1 — Resume from Interrupt 1

Resumes execution after returning from interrupt 1, restoring flags and program counter.

### Syntax
```pasm
        RESI1
```

### Result
Execution resumes from the interrupted location for interrupt 1.

### Parameters
None.

### Encoding
\simpleencoding{EEEE 1011001 110 111110100 111110101 | D | — | — | 4}

### Related Instructions
- [RESI0](#resi0) — Resume from interrupt 0
- [RESI2](#resi2) — Resume from interrupt 2
- [RESI3](#resi3) — Resume from interrupt 3
- [RETI1](#reti1) — Return from interrupt 1

### Explanation
RESI1 resumes execution from interrupt 1. This is functionally equivalent to CALLD $1F4,$1F5 WCZ, which restores the program counter, C flag, and Z flag from the interrupt return address registers. The operation takes 4 cycles minimum, with variable timing depending on hub access if the resume location is in hub memory (13-20 cycles).

Unlike RETIx instructions which return from the interrupt handler, RESIx instructions resume interrupted execution, used when an interrupt handler needs to yield to another interrupt priority level before completion.

---

## RESI2 — Resume from Interrupt 2

Resumes execution after returning from interrupt 2, restoring flags and program counter.

### Syntax
```pasm
        RESI2
```

### Result
Execution resumes from the interrupted location for interrupt 2.

### Parameters
None.

### Encoding
\simpleencoding{EEEE 1011001 110 111110010 111110011 | D | — | — | 4}

### Related Instructions
- [RESI0](#resi0) — Resume from interrupt 0
- [RESI1](#resi1) — Resume from interrupt 1
- [RESI3](#resi3) — Resume from interrupt 3
- [RETI2](#reti2) — Return from interrupt 2

### Explanation
RESI2 resumes execution from interrupt 2. This is functionally equivalent to CALLD $1F2,$1F3 WCZ, which restores the program counter, C flag, and Z flag from the interrupt return address registers. The operation takes 4 cycles minimum, with variable timing depending on hub access if the resume location is in hub memory (13-20 cycles).

Unlike RETIx instructions which return from the interrupt handler, RESIx instructions resume interrupted execution, used when an interrupt handler needs to yield to another interrupt priority level before completion.

---

## RESI3 — Resume from Interrupt 3

Resumes execution after returning from interrupt 3, restoring flags and program counter.

### Syntax
```pasm
        RESI3
```

### Result
Execution resumes from the interrupted location for interrupt 3.

### Parameters
None.

### Encoding
\simpleencoding{EEEE 1011001 110 111110000 111110001 | D | — | — | 4}

### Related Instructions
- [RESI0](#resi0) — Resume from interrupt 0
- [RESI1](#resi1) — Resume from interrupt 1
- [RESI2](#resi2) — Resume from interrupt 2
- [RETI3](#reti3) — Return from interrupt 3

### Explanation
RESI3 resumes execution from interrupt 3. This is functionally equivalent to CALLD $1F0,$1F1 WCZ, which restores the program counter, C flag, and Z flag from the interrupt return address registers. The operation takes 4 cycles minimum, with variable timing depending on hub access if the resume location is in hub memory (13-20 cycles).

Unlike RETIx instructions which return from the interrupt handler, RESIx instructions resume interrupted execution, used when an interrupt handler needs to yield to another interrupt priority level before completion.

---

## RET — Return from Subroutine

Returns from a subroutine by popping the return address from the hardware stack.

### Syntax
```pasm
        RET     {WC|WZ|WCZ}
```

### Result
The program counter, C flag, and Z flag are restored from the top of the hardware stack.

### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional flags: restore carry, restore zero, or both |

### Encoding
\simpleencoding{EEEE 1101011 CZ1 000000000 000101101 | — | K[31] | K[30] | 4}

### Related Instructions
- [CALL](#call) — Call subroutine
- [CALLA](#calla) — Call subroutine with PTRA stack
- [CALLB](#callb) — Call subroutine with PTRB stack
- [RETA](#reta) — Return via PTRA stack
- [RETB](#retb) — Return via PTRB stack

### Explanation
RET returns from a subroutine by popping the hardware stack (K). The program counter is restored from K[19:0]. If the WC or WCZ effect is specified, the C flag is restored from K[31]. If the WZ or WCZ effect is specified, the Z flag is restored from K[30]. The operation takes 4 cycles minimum, with variable timing depending on hub access if the return location is in hub memory (13-20 cycles).

The P2 provides an 8-level hardware stack for fast subroutine calls. RET is paired with CALL, CALLPA, CALLPB, CALLA, and CALLB instructions. The hardware stack eliminates the overhead of software stack management for shallow call depths.

---

## RETA — Return via PTRA Stack

Returns from a subroutine by reading the return address from hub memory via PTRA.

### Syntax
```pasm
        RETA    {WC|WZ|WCZ}
```

### Result
The program counter, C flag, and Z flag are restored from hub memory at --PTRA.

### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional flags: restore carry, restore zero, or both |

### Encoding
\simpleencoding{EEEE 1101011 CZ1 000000000 000101110 | — | L[31] | L[30] | 11...18}

### Related Instructions
- [CALLA](#calla) — Call subroutine with PTRA stack
- [RET](#ret) — Return from subroutine via hardware stack
- [RETB](#retb) — Return via PTRB stack

### Explanation
RETA returns from a subroutine by reading a hub long from --PTRA. PTRA is pre-decremented by 4 bytes, then a long is read from that address. The program counter is restored from L[19:0]. If the WC or WCZ effect is specified, the C flag is restored from L[31]. If the WZ or WCZ effect is specified, the Z flag is restored from L[30]. The operation takes 11-18 cycles minimum (20-40 cycles if the return location is in hub memory).

RETA is paired with CALLA for implementing software stacks in hub memory, enabling deep call nesting beyond the 8-level hardware stack limit. The PTRA pointer must be properly maintained by the calling convention.

---

## RETB — Return via PTRB Stack

Returns from a subroutine by reading the return address from hub memory via PTRB.

### Syntax
```pasm
        RETB    {WC|WZ|WCZ}
```

### Result
The program counter, C flag, and Z flag are restored from hub memory at --PTRB.

### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional flags: restore carry, restore zero, or both |

### Encoding
\simpleencoding{EEEE 1101011 CZ1 000000000 000101111 | — | L[31] | L[30] | 11...18}

### Related Instructions
- [CALLB](#callb) — Call subroutine with PTRB stack
- [RET](#ret) — Return from subroutine via hardware stack
- [RETA](#reta) — Return via PTRA stack

### Explanation
RETB returns from a subroutine by reading a hub long from --PTRB. PTRB is pre-decremented by 4 bytes, then a long is read from that address. The program counter is restored from L[19:0]. If the WC or WCZ effect is specified, the C flag is restored from L[31]. If the WZ or WCZ effect is specified, the Z flag is restored from L[30]. The operation takes 11-18 cycles minimum (20-40 cycles if the return location is in hub memory).

RETB is paired with CALLB for implementing software stacks in hub memory, enabling deep call nesting beyond the 8-level hardware stack limit. The PTRB pointer must be properly maintained by the calling convention.

---

## RETI0 — Return from Interrupt 0

Returns from interrupt 0 handler, restoring execution to the interrupted code.

### Syntax
```pasm
        RETI0
```

### Result
Execution returns from interrupt 0 to the interrupted location.

### Parameters
None.

### Encoding
\simpleencoding{EEEE 1011001 110 111111111 111111111 | D | — | — | 4}

### Related Instructions
- [RETI1](#reti1) — Return from interrupt 1
- [RETI2](#reti2) — Return from interrupt 2
- [RETI3](#reti3) — Return from interrupt 3
- [RESI0](#resi0) — Resume from interrupt 0

### Explanation
RETI0 returns from interrupt 0. This is functionally equivalent to CALLD $1FF,$1FF WCZ, which restores the program counter, C flag, and Z flag from the interrupt return address registers. The operation takes 4 cycles minimum, with variable timing depending on hub access if the return location is in hub memory (13-20 cycles).

The P2 provides four interrupt levels (INT0-INT3), with INT0 being the lowest priority. RETI0 completes the interrupt handler and resumes normal execution at the point where the interrupt occurred.

---

## RETI1 — Return from Interrupt 1

Returns from interrupt 1 handler, restoring execution to the interrupted code.

### Syntax
```pasm
        RETI1
```

### Result
Execution returns from interrupt 1 to the interrupted location.

### Parameters
None.

### Encoding
\simpleencoding{EEEE 1011001 110 111111111 111110101 | D | — | — | 4}

### Related Instructions
- [RETI0](#reti0) — Return from interrupt 0
- [RETI2](#reti2) — Return from interrupt 2
- [RETI3](#reti3) — Return from interrupt 3
- [RESI1](#resi1) — Resume from interrupt 1

### Explanation
RETI1 returns from interrupt 1. This is functionally equivalent to CALLD $1FF,$1F5 WCZ, which restores the program counter, C flag, and Z flag from the interrupt return address registers. The operation takes 4 cycles minimum, with variable timing depending on hub access if the return location is in hub memory (13-20 cycles).

The P2 provides four interrupt levels (INT0-INT3), with INT1 being the second priority level. RETI1 completes the interrupt handler and resumes normal execution at the point where the interrupt occurred.

---

## RETI2 — Return from Interrupt 2

Returns from interrupt 2 handler, restoring execution to the interrupted code.

### Syntax
```pasm
        RETI2
```

### Result
Execution returns from interrupt 2 to the interrupted location.

### Parameters
None.

### Encoding
\simpleencoding{EEEE 1011001 110 111111111 111110011 | D | — | — | 4}

### Related Instructions
- [RETI0](#reti0) — Return from interrupt 0
- [RETI1](#reti1) — Return from interrupt 1
- [RETI3](#reti3) — Return from interrupt 3
- [RESI2](#resi2) — Resume from interrupt 2

### Explanation
RETI2 returns from interrupt 2. This is functionally equivalent to CALLD $1FF,$1F3 WCZ, which restores the program counter, C flag, and Z flag from the interrupt return address registers. The operation takes 4 cycles minimum, with variable timing depending on hub access if the return location is in hub memory (13-20 cycles).

The P2 provides four interrupt levels (INT0-INT3), with INT2 being the third priority level. RETI2 completes the interrupt handler and resumes normal execution at the point where the interrupt occurred.

---

## RETI3 — Return from Interrupt 3

Returns from interrupt 3 handler, restoring execution to the interrupted code.

### Syntax
```pasm
        RETI3
```

### Result
Execution returns from interrupt 3 to the interrupted location.

### Parameters
None.

### Encoding
\simpleencoding{EEEE 1011001 110 111111111 111110001 | D | — | — | 4}

### Related Instructions
- [RETI0](#reti0) — Return from interrupt 0
- [RETI1](#reti1) — Return from interrupt 1
- [RETI2](#reti2) — Return from interrupt 2
- [RESI3](#resi3) — Resume from interrupt 3

### Explanation
RETI3 returns from interrupt 3. This is functionally equivalent to CALLD $1FF,$1F1 WCZ, which restores the program counter, C flag, and Z flag from the interrupt return address registers. The operation takes 4 cycles minimum, with variable timing depending on hub access if the return location is in hub memory (13-20 cycles).

The P2 provides four interrupt levels (INT0-INT3), with INT3 being the highest priority level. RETI3 completes the interrupt handler and resumes normal execution at the point where the interrupt occurred.

---

## REV — Reverse Bits

Reverses the bit pattern in a register, swapping bit 0 with bit 31, bit 1 with bit 30, etc.

### Syntax
```pasm
        REV     D
```

### Result
The 32-bit pattern in D is reversed (bits 31:0 become bits 0:31).

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the bit pattern to reverse |

### Encoding
\simpleencoding{EEEE 1101011 000 DDDDDDDDD 001101001 | D | — | — | 2}

### Related Instructions
- [ROL](#rol) — Rotate left
- [ROR](#ror) — Rotate right
- [ZEROX](#zerox) — Zero-extend

### Explanation
REV performs a complete bitwise reverse of the value in D, storing the result back into D. Bit 31 becomes bit 0, bit 30 becomes bit 1, and so on through bit 0 becoming bit 31. The operation takes 2 cycles and does not affect any flags.

This instruction is useful for processing binary data in different MSB/LSB order than it is transmitted with, such as serial protocols that send least-significant bit first but need processing in most-significant bit first order. It is also used in bit-reversal algorithms for FFT operations.

---

## RFBYTE — Read Byte via FIFO

Reads a zero-extended byte from the FIFO after a RDFAST operation.

### Syntax
```pasm
        RFBYTE  D {WC|WZ|WCZ}
```

### Result
A zero-extended byte from the FIFO is loaded into D.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Destination register to receive the byte value |
| WC/WZ/WCZ | Optional flags: write carry, write zero, or both |

### Encoding
\simpleencoding{EEEE 1101011 CZ0 DDDDDDDDD 000010000 | D | MSB of byte | Result = 0 | 2}

### Related Instructions
- [RDFAST](#rdfast) — Begin fast hub read via FIFO
- [RFWORD](#rfword) — Read word via FIFO
- [RFLONG](#rflong) — Read long via FIFO
- [RFVAR](#rfvar) — Read variable-length value via FIFO

### Explanation
RFBYTE is used after RDFAST to read zero-extended bytes from the FIFO. The byte is loaded into D with bits 31:8 cleared to 0. If the WC flag is specified, C is set to the MSB of the byte. If the WZ flag is specified, Z is set if the result equals zero. The operation takes 2 cycles when the FIFO has data available.

The FIFO is automatically refilled in the background by the RDFAST operation, enabling high-throughput sequential byte processing without hub access overhead for each byte. This is essential for checksum calculations, data parsing, and stream processing.

---

## RFLONG — Read Long via FIFO

Reads a long (32-bit value) from the FIFO after a RDFAST operation.

### Syntax
```pasm
        RFLONG  D {WC|WZ|WCZ}
```

### Result
A long from the FIFO is loaded into D.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Destination register to receive the long value |
| WC/WZ/WCZ | Optional flags: write carry, write zero, or both |

### Encoding
\simpleencoding{EEEE 1101011 CZ0 DDDDDDDDD 000010010 | D | MSB of long | Result = 0 | 2}

### Related Instructions
- [RDFAST](#rdfast) — Begin fast hub read via FIFO
- [RFBYTE](#rfbyte) — Read byte via FIFO
- [RFWORD](#rfword) — Read word via FIFO
- [RFVAR](#rfvar) — Read variable-length value via FIFO

### Explanation
RFLONG is used after RDFAST to read longs from the FIFO. If the WC flag is specified, C is set to the MSB of the long. If the WZ flag is specified, Z is set if the result equals zero. The operation takes 2 cycles when the FIFO has data available.

The FIFO is automatically refilled in the background by the RDFAST operation, enabling high-throughput sequential long processing without hub access overhead for each long. This is ideal for memory block processing, array operations, and bulk data transfers.

---

## RFVAR — Read Variable-Length Value via FIFO

Reads a zero-extended 1-4 byte variable-length value from the FIFO after a RDFAST operation.

### Syntax
```pasm
        RFVAR   D {WC|WZ|WCZ}
```

### Result
A zero-extended 1-4 byte value from the FIFO is loaded into D.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Destination register to receive the variable-length value |
| WC/WZ/WCZ | Optional flags: write carry, write zero, or both |

### Encoding
\simpleencoding{EEEE 1101011 CZ0 DDDDDDDDD 000010011 | D | 0 | Result = 0 | 2}

### Related Instructions
- [RDFAST](#rdfast) — Begin fast hub read via FIFO
- [RFBYTE](#rfbyte) — Read byte via FIFO
- [RFWORD](#rfword) — Read word via FIFO
- [RFLONG](#rflong) — Read long via FIFO
- [RFVARS](#rfvars) — Read sign-extended variable via FIFO

### Explanation
RFVAR is used after RDFAST to read variable-length values (1-4 bytes) from the FIFO with zero extension. The value is loaded into D with upper bits cleared to 0. If the WC flag is specified, C is always cleared to 0. If the WZ flag is specified, Z is set if the result equals zero. The operation takes 2 cycles when the FIFO has data available.

The length of each value read is determined by the streamer configuration set up before the RDFAST operation. RFVAR is useful for processing variable-length encoded data streams where different values occupy different numbers of bytes.

---

## RFVARS — Read Sign-Extended Variable via FIFO

Reads a sign-extended 1-4 byte variable-length value from the FIFO after a RDFAST operation.

### Syntax
```pasm
        RFVARS  D {WC|WZ|WCZ}
```

### Result
A sign-extended 1-4 byte value from the FIFO is loaded into D.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Destination register to receive the sign-extended value |
| WC/WZ/WCZ | Optional flags: write carry, write zero, or both |

### Encoding
\simpleencoding{EEEE 1101011 CZ0 DDDDDDDDD 000010100 | D | MSB of value | Result = 0 | 2}

### Related Instructions
- [RDFAST](#rdfast) — Begin fast hub read via FIFO
- [RFVAR](#rfvar) — Read zero-extended variable via FIFO
- [RFBYTE](#rfbyte) — Read byte via FIFO

### Explanation
RFVARS is used after RDFAST to read variable-length values (1-4 bytes) from the FIFO with sign extension. The value is loaded into D with upper bits set according to the MSB of the value (sign extension). If the WC flag is specified, C is set to the MSB of the value. If the WZ flag is specified, Z is set if the result equals zero. The operation takes 2 cycles when the FIFO has data available.

The length of each value read is determined by the streamer configuration set up before the RDFAST operation. RFVARS is useful for processing variable-length encoded signed data streams where different values occupy different numbers of bytes.

---

## RFWORD — Read Word via FIFO

Reads a zero-extended word (16-bit value) from the FIFO after a RDFAST operation.

### Syntax
```pasm
        RFWORD  D {WC|WZ|WCZ}
```

### Result
A zero-extended word from the FIFO is loaded into D.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Destination register to receive the word value |
| WC/WZ/WCZ | Optional flags: write carry, write zero, or both |

### Encoding
\simpleencoding{EEEE 1101011 CZ0 DDDDDDDDD 000010001 | D | MSB of word | Result = 0 | 2}

### Related Instructions
- [RDFAST](#rdfast) — Begin fast hub read via FIFO
- [RFBYTE](#rfbyte) — Read byte via FIFO
- [RFLONG](#rflong) — Read long via FIFO
- [RFVAR](#rfvar) — Read variable-length value via FIFO

### Explanation
RFWORD is used after RDFAST to read zero-extended words from the FIFO. The word is loaded into D with bits 31:16 cleared to 0. If the WC flag is specified, C is set to the MSB of the word. If the WZ flag is specified, Z is set if the result equals zero. The operation takes 2 cycles when the FIFO has data available.

The FIFO is automatically refilled in the background by the RDFAST operation, enabling high-throughput sequential word processing without hub access overhead for each word. This is useful for processing 16-bit audio samples, network packets, and other word-oriented data streams.

---

## RGBEXP — Expand RGB Color

Expands a 5:6:5 RGB color value into an 8:8:8 format for display.

### Syntax
```pasm
        RGBEXP  D
```

### Result
The 5:6:5 RGB value in D[15:0] is expanded into 8:8:8 format in D[31:8].

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing 5:6:5 RGB in D[15:0], receives 8:8:8 RGB in D[31:8] |

### Encoding
\simpleencoding{EEEE 1101011 000 DDDDDDDDD 001100111 | D | — | — | 2}

### Related Instructions
- [RGBSQZ](#rgbsqz) — Squeeze RGB color from 8:8:8 to 5:6:5

### Explanation
RGBEXP expands a compact 5:6:5 RGB color value (commonly used in 16-bit color displays) into full 8:8:8 RGB format (24-bit true color). The input 5:6:5 value is in D[15:0] with 5 bits red, 6 bits green, and 5 bits blue. The output 8:8:8 value is placed in D[31:8] with 8 bits each for red, green, and blue. The expansion replicates the most significant bits into the lower bits to maintain color accuracy.

This instruction is useful when converting between 16-bit and 24-bit color formats for graphics processing, blending operations, or display output.

---

## RGBSQZ — Squeeze RGB Color

Compresses an 8:8:8 RGB color value into 5:6:5 format for compact storage.

### Syntax
```pasm
        RGBSQZ  D
```

### Result
The 8:8:8 RGB value in D[31:8] is compressed into 5:6:5 format in D[15:0].

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing 8:8:8 RGB in D[31:8], receives 5:6:5 RGB in D[15:0] |

### Encoding
\simpleencoding{EEEE 1101011 000 DDDDDDDDD 001100110 | D | — | — | 2}

### Related Instructions
- [RGBEXP](#rgbexp) — Expand RGB color from 5:6:5 to 8:8:8

### Explanation
RGBSQZ compresses a full 8:8:8 RGB color value (24-bit true color) into compact 5:6:5 format (16-bit color). The input 8:8:8 value is in D[31:8] with 8 bits each for red, green, and blue. The output 5:6:5 value is placed in D[15:0] with 5 bits red, 6 bits green, and 5 bits blue. The compression keeps the most significant bits of each color channel.

This instruction is useful when converting from 24-bit to 16-bit color formats for display output or when memory/bandwidth constraints require compact color representation.

---

## ROL — Rotate Left

Rotates the bits of a register left by a specified number of positions.

### Syntax
```pasm
        ROL     D,{#}S {WC|WZ|WCZ}
```

### Result
The bits of D are rotated left by S positions; departing MSBs are moved into LSBs.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the value to rotate left by S bits |
| S | Register or 5-bit literal (0-31) indicating the number of bit positions to rotate |
| WC/WZ/WCZ | Optional flags: write carry, write zero, or both |

### Encoding
\simpleencoding{EEEE 0000001 CZI DDDDDDDDD SSSSSSSSS | D | Last bit out¹ | Result = 0 | 2}

¹ C = last bit rotated out if S[4:0] > 0, else D[31]

### Related Instructions
- [ROR](#ror) — Rotate right
- [RCL](#rcl) — Rotate carry left
- [RCR](#rcr) — Rotate carry right
- [SHL](#shl) — Shift left

### Explanation
ROL rotates D's binary value left by S places (0-31 bits). All MSBs rotated out are moved into the new LSBs. If the WC or WCZ effect is specified, the C flag is updated to the value of the last bit rotated out if S is 1-31, or to D[31] if S is 0. If the WZ or WCZ effect is specified, the Z flag is set if the result equals zero. Since no bits are lost by this operation, the result will only be zero if D started at zero.

Rotation is useful for bit manipulation, circular buffers, hash functions, and cryptographic operations. Unlike shifts, rotations preserve all bits, making them reversible operations.

---

## ROLBYTE — Rotate Byte Left

Reads a byte from a source and rotates it left into the destination register.

### Syntax
```pasm
        ROLBYTE D,{#}S,#N
        ROLBYTE D
```

### Result
Byte N (0-3) of S, or a byte from a source described by prior ALTGB instruction, is rotated left into D.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register in which to rotate the byte into |
| S | Register, 9-bit literal, or 32-bit augmented literal containing the target byte |
| N | 2-bit literal (0-3) identifying the byte position in S |

### Encoding
\begin{encodingtable}
EEEE 1001000 NNI DDDDDDDDD SSSSSSSSS & D & — & — & 2 \\
EEEE 1001000 000 DDDDDDDDD 000000000 & D & — & — & 2
\end{encodingtable}

### Related Instructions
- [ROLNIB](#rolnib) — Rotate nibble left
- [ROLWORD](#rolword) — Rotate word left
- [GETBYTE](#getbyte) — Get byte from value
- [SETBYTE](#setbyte) — Set byte in value
- [ALTGB](#altgb) — Alter next GETBYTE/ROLBYTE instruction

### Explanation
ROLBYTE reads the byte identified by N (0-3) from S, or a byte from the source described by a prior ALTGB instruction, and rotates it left into D. ROLBYTE achieves the same effect as two instructions: an 8-bit SHL followed by SETBYTE into byte 0. N (0-3) identifies a value's individual bytes by position in least-significant byte order.

The second syntax form is intended for use after an ALTGB instruction in a loop to iteratively read a series of byte values within contiguous long registers. This enables efficient unpacking of byte arrays into separate values.

---

## ROLNIB — Rotate Nibble Left

Reads a nibble from a source and rotates it left into the destination register.

### Syntax
```pasm
        ROLNIB  D,{#}S,#N
        ROLNIB  D
```

### Result
Nibble N (0-7) of S, or a nibble from a source described by prior ALTGN instruction, is rotated left into D.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register in which to rotate the nibble into |
| S | Register, 9-bit literal, or 32-bit augmented literal containing the target nibble |
| N | 3-bit literal (0-7) identifying the nibble position in S |

### Encoding
\begin{encodingtable}
EEEE 100010N NNI DDDDDDDDD SSSSSSSSS & D & — & — & 2 \\
EEEE 1000100 000 DDDDDDDDD 000000000 & D & — & — & 2
\end{encodingtable}

### Related Instructions
- [ROLBYTE](#rolbyte) — Rotate byte left
- [ROLWORD](#rolword) — Rotate word left
- [GETNIB](#getnib) — Get nibble from value
- [SETNIB](#setnib) — Set nibble in value
- [ALTGN](#altgn) — Alter next GETNIB/ROLNIB instruction

### Explanation
ROLNIB reads the nibble identified by N (0-7) from S, or a nibble from the source described by a prior ALTGN instruction, and rotates it left into D. ROLNIB achieves the same effect as two instructions: a 4-bit SHL followed by SETNIB into nibble 0. N (0-7) identifies a value's individual nibbles by position in least-significant nibble order.

The second syntax form is intended for use after an ALTGN instruction in a loop to iteratively read a series of nibble values within contiguous long registers. This enables efficient unpacking of nibble arrays, useful for BCD arithmetic and compact data encoding.

---

## ROLWORD — Rotate Word Left

Reads a word from a source and rotates it left into the destination register.

### Syntax
```pasm
        ROLWORD D,{#}S,#N
        ROLWORD D
```

### Result
Word N (0-1) of S, or a word from a source described by prior ALTGW instruction, is rotated left into D.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register in which to rotate the word into |
| S | Register, 9-bit literal, or 32-bit augmented literal containing the target word |
| N | 1-bit literal (0-1) identifying the word position in S |

### Encoding
\begin{encodingtable}
EEEE 1001010 0NI DDDDDDDDD SSSSSSSSS & D & — & — & 2 \\
EEEE 1001010 000 DDDDDDDDD 000000000 & D & — & — & 2
\end{encodingtable}

### Related Instructions
- [ROLBYTE](#rolbyte) — Rotate byte left
- [ROLNIB](#rolnib) — Rotate nibble left
- [GETWORD](#getword) — Get word from value
- [SETWORD](#setword) — Set word in value
- [ALTGW](#altgw) — Alter next GETWORD/ROLWORD instruction

### Explanation
ROLWORD reads the word identified by N (0-1) from S, or a word from the source described by a prior ALTGW instruction, and rotates it left into D. ROLWORD achieves the same effect as two instructions: a 16-bit SHL followed by SETWORD into word 0. N (0-1) identifies a value's individual words by position in least-significant word order.

The second syntax form is intended for use after an ALTGW instruction in a loop to iteratively read a series of word values within contiguous long registers. This enables efficient unpacking of word arrays into separate values.

---

## ROR — Rotate Right

Rotates the bits of a register right by a specified number of positions.

### Syntax
```pasm
        ROR     D,{#}S {WC|WZ|WCZ}
```

### Result
The bits of D are rotated right by S positions; departing LSBs are moved into MSBs.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the value to rotate right by S bits |
| S | Register or 5-bit literal (0-31) indicating the number of bit positions to rotate |
| WC/WZ/WCZ | Optional flags: write carry, write zero, or both |

### Encoding
\simpleencoding{EEEE 0000000 CZI DDDDDDDDD SSSSSSSSS | D | Last bit out¹ | Result = 0 | 2}

¹ C = last bit rotated out if S[4:0] > 0, else D[0]

### Related Instructions
- [ROL](#rol) — Rotate left
- [RCL](#rcl) — Rotate carry left
- [RCR](#rcr) — Rotate carry right
- [SHR](#shr) — Shift right

### Explanation
ROR rotates D's binary value right by S places (0-31 bits). All LSBs rotated out are moved into the new MSBs. If the WC or WCZ effect is specified, the C flag is updated to the value of the last bit rotated out if S is 1-31, or to D[0] if S is 0. If the WZ or WCZ effect is specified, the Z flag is set if the result equals zero. Since no bits are lost by this operation, the result will only be zero if D started at zero.

Rotation is useful for bit manipulation, circular buffers, hash functions, and cryptographic operations. Unlike shifts, rotations preserve all bits, making them reversible operations. ROR is particularly useful for serial communications where data needs to be processed in reverse bit order.

---

## RQPIN — Read Smart Pin without Acknowledge

Reads a smart pin's result value without acknowledging the pin, leaving its ready flag set.

### Syntax
```pasm
        RQPIN   D,{#}S {WC}
```

### Result
Smart pin S[5:0] result "Z" is loaded into D without clearing the pin's ready flag.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Destination register to receive the pin result |
| S | Pin number (S[5:0]) to read from |
| WC | Optional flag: write carry with modal result |

### Encoding
\simpleencoding{EEEE 1010100 C0I DDDDDDDDD SSSSSSSSS | D | Modal result | — | 2}

### Related Instructions
- [RDPIN](#rdpin) — Read smart pin result and acknowledge
- [WRPIN](#wrpin) — Write smart pin mode
- [WXPIN](#wxpin) — Write smart pin X parameter
- [WYPIN](#wypin) — Write smart pin Y parameter

### Explanation
RQPIN reads the result value from the specified smart pin without acknowledging the pin. Unlike RDPIN, this instruction does not clear the pin's "ready" flag, allowing the same result to be read multiple times or checked before being consumed. If the WC flag is specified, the C flag is set to the modal result, which provides mode-specific status information.

This instruction is useful when you need to check a pin's result value without consuming it, such as polling for completion before actually processing the result, or when multiple parts of the code need to examine the same measurement.
