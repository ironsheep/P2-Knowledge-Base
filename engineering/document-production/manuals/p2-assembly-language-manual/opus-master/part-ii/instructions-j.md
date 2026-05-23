# Instructions: J

This section contains all PASM2 instructions beginning with the letter J.

**Conditional Jump Timing Convention:** Conditional jumps (including event-jumps and counter-jumps) show their `Clks` field as `not-taken / taken`. The *taken* value depends on execution context:

| Context | Clocks when taken |
|:--------|:----------------:|
| COG / LUT execution | 4 |
| Hub execution | 13...20 |

So `2 or 4 / 2 or 13-20` reads as: 2 cycles when the jump is not taken (either context), 4 cycles when taken in cog/LUT, 13–20 cycles when taken in hub execution.



::: instrheader
## JATN / JNATN {#jatn}
Jump If Attention Set / Clear {#jnatn}

[Events and Timing](#events-and-timing) - Jumps based on ATN event flag state.
:::

**JATN**  *{#}S*\
**JNATN**  *{#}S*

---

**Result:** JATN jumps if the ATN event flag is set; JNATN jumps if the ATN event flag is clear.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000001110 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |
| EEEE | 1011110 | 01I | 000011110 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |

PC is written only when the condition is met (flag set for JATN, flag clear for JNATN).


**Related:** [COGATN](#cogatn), [POLLATN](#pollatn)

**Explanation:**

JATN checks the ATN (attention) event flag and conditionally jumps if the flag is set. JNATN performs the opposite test, jumping if the flag is clear. The ATN event flag indicates that one or more other cogs are requesting this cog's attention via the COGATN instruction.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the condition is not met, execution continues with the next instruction.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

These instructions are useful for implementing inter-cog communication mechanisms where one cog needs to signal and get the attention of another cog for coordination or data exchange purposes.



::: instrheader
## JCT1 / JCT2 / JCT3 / JNCT1 / JNCT2 / JNCT3 {#jct1}
Jump If Counter Event Set / Clear

[Events and Timing](#events-and-timing) - Jumps based on counter event flag state.
:::

\hypertarget{jct2}{}\hypertarget{jct3}{}\hypertarget{jnct1}{}\hypertarget{jnct2}{}\hypertarget{jnct3}{}

**JCT1**  *{#}S*\
**JCT2**  *{#}S*\
**JCT3**  *{#}S*

**JNCT1**  *{#}S*\
**JNCT2**  *{#}S*\
**JNCT3**  *{#}S*

---

**Result:** JCTn jumps if the CTn event flag is set; JNCTn jumps if the CTn event flag is clear.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000000001 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |
| EEEE | 1011110 | 01I | 000000010 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |
| EEEE | 1011110 | 01I | 000000011 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |
| EEEE | 1011110 | 01I | 000010001 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |
| EEEE | 1011110 | 01I | 000010010 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |
| EEEE | 1011110 | 01I | 000010011 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |

PC is written only when the condition is met (flag set for JCTn, flag clear for JNCTn).


**Related:** [ADDCT1/2/3](#addct1), [POLLCT1/2/3](#pollct1), [WAITCT1/2/3](#waitct1)

**Explanation:**

JCT1, JCT2, and JCT3 check their respective counter event flags and conditionally jump to the address specified by S if the flag is set. JNCT1, JNCT2, and JNCT3 perform the opposite test, jumping if the flag is clear. Each CTn event flag is automatically set when the system counter reaches the CTn target value that was previously configured using the corresponding ADDCTn instruction.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the condition is not met, execution continues with the next instruction.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

The P2 provides three independent hardware counters for timing operations, allowing a cog to manage multiple simultaneous time-based events without software overhead. JCTn instructions are commonly used for timing loops that wait until a counter fires, while JNCTn instructions enable polling loops that continue until a counter event occurs.



::: instrheader
## JFBW / JNFBW {#jfbw}
Jump If FIFO Block Wrap Set / Clear {#jnfbw}

[Events and Timing](#events-and-timing) - Jumps based on FIFO block wrap event flag state.
:::

**JFBW**  *{#}S*\
**JNFBW**  *{#}S*

---

**Result:** JFBW jumps if the FIFO block wrap event flag is set; JNFBW jumps if the flag is clear.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000001001 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |
| EEEE | 1011110 | 01I | 000011001 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |

PC is written only when the condition is met.


**Related:** [RFBYTE](#rfbyte), [WFBYTE](#wfbyte), [SETQ2](#setq2)

**Explanation:**

JFBW checks the FIFO interface block wrap event flag and jumps if set. JNFBW performs the opposite test, jumping if clear. This event flag is set when a FIFO read or write operation wraps around the configured block boundary.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the condition is not met, execution continues with the next instruction.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

These instructions are useful for implementing circular buffer operations and managing block-based data transfers through the FIFO interface.



::: instrheader
## JINT / JNINT {#jint}
Jump If Interrupt Set / Clear {#jnint}

[Events and Timing](#events-and-timing) - Jumps based on INT event flag state.
:::

**JINT**  *{#}S*\
**JNINT**  *{#}S*

---

**Result:** JINT jumps if the INT event flag is set; JNINT jumps if the flag is clear.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000000000 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |
| EEEE | 1011110 | 01I | 000010000 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |

PC is written only when the condition is met.


**Related:** [POLLINT](#pollint), [SETINT1/2/3](#setint1)

**Explanation:**

JINT checks the INT (interrupt) event flag and jumps if set. JNINT performs the opposite test, jumping if clear. The INT event flag indicates that a hardware interrupt condition is pending, as configured by one of the SETINT instructions.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the condition is not met, execution continues with the next instruction.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

These instructions provide a polling-based mechanism for handling hardware interrupts, allowing code to check for interrupt conditions at convenient points in the program flow.



::: instrheader
## JMP {#jmp}
Jump

[Branching and Flow Control](#branching-and-flow-control) - Unconditionally jumps to a new address.
:::

**JMP**  *D*  **{WC/WZ/WCZ}**\
**JMP**  *#A*\
**JMP**  *#\A*

---

**Result:** PC is set to the address specified by D or A.

- D is a register containing the absolute jump address, and optionally flag values in bits [31:30].
- A is a 20-bit absolute or PC-relative address. Use \ prefix to force absolute addressing when using #.
- WC, WZ, or WCZ are optional effects to set C flag to D[31] and/or Z flag to D[30].


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000101100 | D[31] | D[30] | PC | 4 / 13-20 † |
| EEEE | 1101100 | RAA | AAAAAAAAA | AAAAAAAAA | --- | --- | PC | 4 / 13-20 † |

† **Timing varies by execution context:**

| Context | Clocks |
|:--------|:------:|
| COG / LUT execution | 4 |
| Hub execution | 13...20 |


**Related:** [CALL](#call), [RET](#ret), [JMPREL](#jmprel), [CALLD](#calld)

**Explanation:**

JMP performs an unconditional jump to a new address, setting the PC to either the value in register D or the immediate address A.

The first syntax form (JMP D) reads the jump address from register D and sets PC to that value. When the WC or WCZ effect is specified, the C flag is set to bit 31 of D. When the WZ or WCZ effect is specified, the Z flag is set to bit 30 of D. This allows flags to be restored as part of a jump, which is useful for return-from-subroutine operations where both PC and flags need to be restored.

The second syntax form (JMP #A) jumps to an immediate address. The R bit in the encoding determines whether the address is PC-relative (R=1) or absolute (R=0). By default, the assembler uses PC-relative addressing for # jumps. The backslash prefix (\) forces absolute addressing: JMP #\address.

For PC-relative jumps in COG execution mode, the 20-bit address field is added to PC. For Hub execution mode, the lower 18 bits are shifted left by 2 (multiplied by 4) before being added to PC, since Hub addresses are long-aligned.

The instruction executes in 4 clock cycles in COG execution mode. In Hub execution mode, jumps take 13-20 clock cycles depending on Hub access timing.



::: instrheader
## JMPREL {#jmprel}
Jump Relative

[Branching and Flow Control](#branching-and-flow-control) - Jumps by adding a signed offset to the PC.
:::

**JMPREL**  *{#}D*

---

**Result:** PC is incremented or decremented by the value in D.

- D is a register or 9-bit literal specifying the signed offset in instructions. For COG execution, PC += D[19:0]. For Hub execution, PC += D[17:0] << 2.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000110000 | --- | --- | PC | 4 / 13-20 † |

† **Timing varies by execution context:**

| Context | Clocks |
|:--------|:------:|
| COG / LUT execution | 4 |
| Hub execution | 13...20 |


**Related:** [JMP](#jmp), [CALL](#call), [DJNZ](#djnz), [IJMP1/2/3](#ijmp1)

**Explanation:**

JMPREL performs a relative jump by adding or subtracting the value in D to the current PC value. This allows position-independent code that can jump forward or backward by a specified number of instructions without knowing the absolute address.

For COG execution mode, the lower 20 bits of D are added to PC. Positive values jump forward, negative values (in two's complement) jump backward. The offset is in units of instructions (longs).

For Hub execution mode, the lower 18 bits of D are shifted left by 2 bits (multiplied by 4) before being added to PC. This accounts for the fact that Hub addresses are byte addresses and each instruction occupies 4 bytes. The offset is still conceptually in units of instructions.

The instruction executes in 4 clock cycles in COG execution mode. In Hub execution mode, jumps take 13-20 clock cycles depending on Hub access timing.

JMPREL is useful for implementing position-independent code, jump tables, and dynamic control flow where the jump offset is computed at runtime.






::: instrheader
## JSE1 / JSE2 / JSE3 / JSE4 / JNSE1 / JNSE2 / JNSE3 / JNSE4 {#jse1}
Jump If Selectable Event Set / Clear

[Events and Timing](#events-and-timing) - Jumps based on selectable event flag state.
:::

\hypertarget{jse2}{}\hypertarget{jse3}{}\hypertarget{jse4}{}\hypertarget{jnse1}{}\hypertarget{jnse2}{}\hypertarget{jnse3}{}\hypertarget{jnse4}{}

**JSE1**  *{#}S*\
**JSE2**  *{#}S*\
**JSE3**  *{#}S*\
**JSE4**  *{#}S*

**JNSE1**  *{#}S*\
**JNSE2**  *{#}S*\
**JNSE3**  *{#}S*\
**JNSE4**  *{#}S*

---

**Result:** JSEn jumps if the SEn event flag is set; JNSEn jumps if the SEn event flag is clear.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000000100 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |
| EEEE | 1011110 | 01I | 000000101 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |
| EEEE | 1011110 | 01I | 000000110 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |
| EEEE | 1011110 | 01I | 000000111 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |
| EEEE | 1011110 | 01I | 000010100 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |
| EEEE | 1011110 | 01I | 000010101 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |
| EEEE | 1011110 | 01I | 000010110 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |
| EEEE | 1011110 | 01I | 000010111 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |

PC is written only when the condition is met (flag set for JSEn, flag clear for JNSEn).


**Related:** [SETSE1/2/3/4](#setse1), [POLLSE1/2/3/4](#pollse1), [WAITSE1/2/3/4](#waitse1)

**Explanation:**

JSE1, JSE2, JSE3, and JSE4 check their respective selectable event flags and conditionally jump to the address specified by S if the flag is set. JNSE1, JNSE2, JNSE3, and JNSE4 perform the opposite test, jumping if the flag is clear. Each selectable event can be configured to detect various hardware conditions using the corresponding SETSE instruction.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the condition is not met, execution continues with the next instruction.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

The P2 provides four independent selectable event sources, enabling multiple concurrent hardware event detection mechanisms for sophisticated event-driven applications. JSEn instructions are commonly used for event-triggered actions, while JNSEn instructions enable polling loops that continue until an event occurs.



::: instrheader
## JPAT / JNPAT {#jpat}
Jump If Pattern Match Event Set / Clear {#jnpat}

[Events and Timing](#events-and-timing) - Jumps based on PAT event flag state.
:::

**JPAT**  *{#}S*\
**JNPAT**  *{#}S*

---

**Result:** PC is set to the address specified by S if the PAT event flag is set (JPAT) or clear (JNPAT).

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:------:|:----:|
| EEEE | 1011110 | 01I | 000001000 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |
| EEEE | 1011110 | 01I | 000011000 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |


**Related:** [SETPAT](#setpat), [POLLPAT](#pollpat)

**Explanation:**

JPAT and JNPAT check the PAT (pattern match) event flag and conditionally jump to the address specified by S. JPAT jumps if the flag is set; JNPAT jumps if it is clear. The PAT event flag is set when the I/O pins match a pattern previously configured with the SETPAT instruction.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the flag is in the opposite state, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JPAT is useful for implementing hardware-triggered control flow where code execution branches based on specific pin state patterns. JNPAT is useful for polling loops that wait until a specific pattern appears on the I/O pins.



::: instrheader
## JQMT / JNQMT {#jqmt}
Jump If CORDIC Empty Event Set / Clear {#jnqmt}

[Events and Timing](#events-and-timing) - Jumps based on CORDIC-read-but-empty event flag state.
:::

**JQMT**  *{#}S*\
**JNQMT**  *{#}S*

---

**Result:** PC is set to the address specified by S if the CORDIC-read-but-empty event flag is set (JQMT) or clear (JNQMT).

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:------:|:----:|
| EEEE | 1011110 | 01I | 000001111 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |
| EEEE | 1011110 | 01I | 000011111 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |


**Related:** [QMUL](#qmul), [QROTATE](#qrotate), [GETQX](#getqx), [GETQY](#getqy)

**Explanation:**

JQMT and JNQMT check the CORDIC-read-but-empty event flag and conditionally jump to the address specified by S. JQMT jumps if the flag is set; JNQMT jumps if it is clear. This event flag is set when code attempts to read CORDIC results before the calculation has completed, indicating a timing error.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the flag is in the opposite state, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JQMT is useful for error handling in CORDIC operations, allowing code to detect and respond to premature reads of calculation results. JNQMT is useful for ensuring CORDIC results are read at the correct time, helping to detect and handle timing errors in mathematical operations.




::: instrheader
## JXFI / JNXFI {#jxfi}
Jump If Streamer Finished Event Set / Clear {#jnxfi}

[Events and Timing](#events-and-timing) - Jumps based on XFI event flag state.
:::

**JXFI**  *{#}S*\
**JNXFI**  *{#}S*

---

**Result:** PC is set to the address specified by S if the XFI event flag is set (JXFI) or clear (JNXFI).

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:------:|:----:|
| EEEE | 1011110 | 01I | 000001011 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |
| EEEE | 1011110 | 01I | 000011011 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |


**Related:** [XINIT](#xinit), [XCONT](#xcont), [POLLXFI](#pollxfi)

**Explanation:**

JXFI and JNXFI check the XFI (streamer finished) event flag and conditionally jump to the address specified by S. JXFI jumps if the flag is set; JNXFI jumps if it is clear. The XFI event flag is set when the streamer completes its current operation.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the flag is in the opposite state, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JXFI is useful for chaining streamer operations or triggering code execution immediately when a streaming operation completes. JNXFI is useful for polling loops that wait until the streamer completes its operation.



::: instrheader
## JXMT / JNXMT {#jxmt}
Jump If Streamer Empty Event Set / Clear {#jnxmt}

[Events and Timing](#events-and-timing) - Jumps based on XMT event flag state.
:::

**JXMT**  *{#}S*\
**JNXMT**  *{#}S*

---

**Result:** PC is set to the address specified by S if the XMT event flag is set (JXMT) or clear (JNXMT).

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:------:|:----:|
| EEEE | 1011110 | 01I | 000001010 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |
| EEEE | 1011110 | 01I | 000011010 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |


**Related:** [XINIT](#xinit), [XCONT](#xcont), [POLLXMT](#pollxmt)

**Explanation:**

JXMT and JNXMT check the XMT (streamer empty) event flag and conditionally jump to the address specified by S. JXMT jumps if the flag is set; JNXMT jumps if it is clear. The XMT event flag is set when the streamer's internal buffer becomes empty and needs to be refilled.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the flag is in the opposite state, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JXMT is useful for implementing continuous streaming operations where the code needs to reload data into the streamer when the buffer empties. JNXMT is useful for maintaining continuous streamer operation by reloading data only when the streamer buffer still contains data.



::: instrheader
## JXRL / JNXRL {#jxrl}
Jump If Streamer LUT Rollover Event Set / Clear {#jnxrl}

[Events and Timing](#events-and-timing) - Jumps based on XRL event flag state.
:::

**JXRL**  *{#}S*\
**JNXRL**  *{#}S*

---

**Result:** PC is set to the address specified by S if the XRL event flag is set (JXRL) or clear (JNXRL).

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:------:|:----:|
| EEEE | 1011110 | 01I | 000001101 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |
| EEEE | 1011110 | 01I | 000011101 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |


**Related:** [XINIT](#xinit), [XCONT](#xcont), [POLLXRL](#pollxrl)

**Explanation:**

JXRL and JNXRL check the XRL (streamer LUT RAM rollover) event flag and conditionally jump to the address specified by S. JXRL jumps if the flag is set; JNXRL jumps if it is clear. The XRL event flag is set when the streamer's LUT RAM address pointer rolls over from the end back to the beginning of the configured range.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the flag is in the opposite state, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JXRL is useful for implementing circular buffer operations with the streamer using LUT RAM, detecting when a complete cycle through the buffer has occurred. JNXRL is useful for detecting when a buffer boundary has not yet been crossed.



::: instrheader
## JXRO / JNXRO {#jxro}
Jump If Streamer NCO Rollover Event Set / Clear {#jnxro}

[Events and Timing](#events-and-timing) - Jumps based on XRO event flag state.
:::

**JXRO**  *{#}S*\
**JNXRO**  *{#}S*

---

**Result:** PC is set to the address specified by S if the XRO event flag is set (JXRO) or clear (JNXRO).

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:------:|:----:|
| EEEE | 1011110 | 01I | 000001100 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |
| EEEE | 1011110 | 01I | 000011100 | SSSSSSSSS | --- | --- | PC | 2 or 4 / 2 or 13-20 |


**Related:** [XINIT](#xinit), [XCONT](#xcont), [POLLXRO](#pollxro)

**Explanation:**

JXRO and JNXRO check the XRO (streamer NCO rollover) event flag and conditionally jump to the address specified by S. JXRO jumps if the flag is set; JNXRO jumps if it is clear. The XRO event flag is set when the streamer's numerically controlled oscillator (NCO) rolls over, which occurs at regular intervals determined by the NCO frequency setting.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the flag is in the opposite state, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JXRO is useful for timing-critical streamer applications where code needs to synchronize with the NCO rollovers. JNXRO is useful for detecting the absence of NCO rollovers in the streaming operation.



