# Instructions: J

This section contains all PASM2 instructions beginning with the letter J.



::: instrheader
## JATN {#jatn}
Jump If Attention Set

[Events and Timing](#events-and-timing) - Jumps if the ATN event flag is set.
:::

**JATN**  *{#}S*

---

**Result:** If the ATN event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000001110 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JNATN](#jnatn), [COGATN](#cogatn), [POLLATN](#pollatn)

**Explanation:**

JATN checks the ATN (attention) event flag and conditionally jumps to the address specified by S if the flag is set. The ATN event flag indicates that one or more other cogs are requesting this cog's attention via the COGATN instruction.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the ATN event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JATN is useful for implementing inter-cog communication mechanisms where one cog needs to signal and get the attention of another cog for coordination or data exchange purposes.



::: instrheader
## JCT1 / JCT2 / JCT3 {#jct1}
Jump If Counter Event Set {#jct2} {#jct3}

[Events and Timing](#events-and-timing) - Jumps if the counter event flag is set.
:::

**JCT1**  *{#}S*
**JCT2**  *{#}S*
**JCT3**  *{#}S*

---

**Result:** If the CTn event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000000001 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |
| EEEE | 1011110 | 01I | 000000010 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |
| EEEE | 1011110 | 01I | 000000011 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |

```{=latex}
\textsuperscript{1} PC is written only when the CTn event flag is set.
```


**Related:** [JNCT1/2/3](#jnct1), [ADDCT1/2/3](#addct1), [POLLCT1/2/3](#pollct1), [WAITCT1/2/3](#waitct1)

**Explanation:**

JCT1, JCT2, and JCT3 check their respective counter event flags and conditionally jump to the address specified by S if the flag is set. Each CTn event flag is automatically set when the system counter reaches the CTn target value that was previously configured using the corresponding ADDCTn instruction.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the CTn event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

The P2 provides three independent hardware counters for timing operations, allowing a cog to manage multiple simultaneous time-based events without software overhead. These instructions are commonly used for timing loops, delays, and periodic task scheduling.



::: instrheader
## JFBW {#jfbw}
Jump If FIFO Block Wrap Set

[Events and Timing](#events-and-timing) - Jumps if the FIFO block wrap event flag is set.
:::

**JFBW**  *{#}S*

---

**Result:** If the FIFO interface block wrap event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000001001 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JNFBW](#jnfbw), [RFBYTE](#rfbyte), [WFBYTE](#wfbyte), [SETQ2](#setq2)

**Explanation:**

JFBW checks the FIFO interface block wrap event flag and conditionally jumps to the address specified by S if the flag is set. This event flag is set when a FIFO read or write operation wraps around the configured block boundary.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the FIFO interface block wrap event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JFBW is useful for implementing circular buffer operations and managing block-based data transfers through the FIFO interface, allowing code to respond immediately when a block boundary has been crossed.



::: instrheader
## JINT {#jint}
Jump If Interrupt Set

[Events and Timing](#events-and-timing) - Jumps if the INT event flag is set.
:::

**JINT**  *{#}S*

---

**Result:** If the INT event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000000000 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JNINT](#jnint), [POLLINT](#pollint), [SETINT1/2/3](#setint1)

**Explanation:**

JINT checks the INT (interrupt) event flag and conditionally jumps to the address specified by S if the flag is set. The INT event flag indicates that a hardware interrupt condition is pending, as configured by one of the SETINT instructions.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the INT event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JINT provides a polling-based mechanism for handling hardware interrupts, allowing code to check for interrupt conditions at convenient points in the program flow rather than using asynchronous interrupt handling.



::: instrheader
## JMP {#jmp}
Jump

[Branching and Flow Control](#branching-and-flow-control) - Unconditionally jumps to a new address.
:::

**JMP**  *D*  **{WC/WZ/WCZ}**
**JMP**  *#A*
**JMP**  *#\A*

---

**Result:** PC is set to the address specified by D or A.

- D is a register containing the absolute jump address, and optionally flag values in bits [31:30].
- A is a 20-bit absolute or PC-relative address. Use \ prefix to force absolute addressing when using #.
- WC, WZ, or WCZ are optional effects to set C flag to D[31] and/or Z flag to D[30].


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000101100 | PC | D[31] | D[30] | 4 |
| EEEE | 1101100 | RAA | AAAAAAAAA | AAAAAAAAA | PC | --- | --- | 4 |


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
| EEEE | 1101011 | 00L | DDDDDDDDD | 000110000 | PC | --- | --- | 4 |


**Related:** [JMP](#jmp), [CALL](#call), [DJNZ](#djnz), [IJMP1/2/3](#ijmp1)

**Explanation:**

JMPREL performs a relative jump by adding or subtracting the value in D to the current PC value. This allows position-independent code that can jump forward or backward by a specified number of instructions without knowing the absolute address.

For COG execution mode, the lower 20 bits of D are added to PC. Positive values jump forward, negative values (in two's complement) jump backward. The offset is in units of instructions (longs).

For Hub execution mode, the lower 18 bits of D are shifted left by 2 bits (multiplied by 4) before being added to PC. This accounts for the fact that Hub addresses are byte addresses and each instruction occupies 4 bytes. The offset is still conceptually in units of instructions.

The instruction executes in 4 clock cycles in COG execution mode. In Hub execution mode, jumps take 13-20 clock cycles depending on Hub access timing.

JMPREL is useful for implementing position-independent code, jump tables, and dynamic control flow where the jump offset is computed at runtime.



::: instrheader
## JNATN {#jnatn}
Jump If Attention Clear

[Events and Timing](#events-and-timing) - Jumps if the ATN event flag is clear.
:::

**JNATN**  *{#}S*

---

**Result:** If the ATN event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000011110 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JATN](#jatn), [COGATN](#cogatn), [POLLATN](#pollatn)

**Explanation:**

JNATN checks the ATN (attention) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JATN, allowing code to jump when no other cog is requesting attention.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the ATN event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNATN is useful for implementing polling loops that wait until the ATN flag is clear before proceeding with other operations.



::: instrheader
## JNCT1 / JNCT2 / JNCT3 {#jnct1}
Jump If Counter Event Clear {#jnct2} {#jnct3}

[Events and Timing](#events-and-timing) - Jumps if the counter event flag is clear.
:::

**JNCT1**  *{#}S*
**JNCT2**  *{#}S*
**JNCT3**  *{#}S*

---

**Result:** If the CTn event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000010001 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |
| EEEE | 1011110 | 01I | 000010010 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |
| EEEE | 1011110 | 01I | 000010011 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |

```{=latex}
\textsuperscript{1} PC is written only when the CTn event flag is clear.
```


**Related:** [JCT1/2/3](#jct1), [ADDCT1/2/3](#addct1), [POLLCT1/2/3](#pollct1), [WAITCT1/2/3](#waitct1)

**Explanation:**

JNCT1, JNCT2, and JNCT3 check their respective counter event flags and conditionally jump to the address specified by S if the flag is clear. These are the logical complements of JCT1/2/3, allowing code to jump when the corresponding counter event has not yet occurred.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the CTn event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

These instructions are useful for implementing polling loops that continue until a counter event occurs, or for skipping code that should only execute before a specific time. The P2's three independent counter event polling mechanisms enable sophisticated timing control with minimal code overhead.



::: instrheader
## JNFBW {#jnfbw}
Jump If FIFO Block Wrap Clear

[Events and Timing](#events-and-timing) - Jumps if the FIFO block wrap event flag is clear.
:::

**JNFBW**  *{#}S*

---

**Result:** If the FIFO interface block wrap event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000011001 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JFBW](#jfbw), [RFBYTE](#rfbyte), [WFBYTE](#wfbyte), [SETQ2](#setq2)

**Explanation:**

JNFBW checks the FIFO interface block wrap event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JFBW, allowing code to jump when no block wrap has occurred.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the FIFO interface block wrap event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNFBW is useful for polling loops that wait until a block wrap occurs, or for conditional code that should only execute when within a block boundary.



::: instrheader
## JNINT {#jnint}
Jump If Interrupt Clear

[Events and Timing](#events-and-timing) - Jumps if the INT event flag is clear.
:::

**JNINT**  *{#}S*

---

**Result:** If the INT event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000010000 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JINT](#jint), [POLLINT](#pollint), [SETINT1/2/3](#setint1)

**Explanation:**

JNINT checks the INT (interrupt) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JINT, allowing code to jump when no interrupt is pending.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the INT event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNINT is useful for polling loops that wait until an interrupt occurs, or for implementing interrupt-safe critical sections that should only execute when interrupts are not pending.



::: instrheader
## JNPAT {#jnpat}
Jump If Pattern Match Event Clear

[Events and Timing](#events-and-timing) - Jumps if the PAT event flag is clear.
:::

**JNPAT**  *{#}S*

---

**Result:** If the PAT event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000011000 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JPAT](#jpat), [SETPAT](#setpat), [POLLPAT](#pollpat)

**Explanation:**

JNPAT checks the PAT (pattern match) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JPAT, allowing code to jump when no pattern match has occurred.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the PAT event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNPAT is useful for polling loops that wait until a specific pattern appears on the I/O pins, or for conditional logic that should execute only when the pattern has not yet matched.



::: instrheader
## JNQMT {#jnqmt}
Jump If CORDIC Empty Event Clear

[Events and Timing](#events-and-timing) - Jumps if the CORDIC-read-but-empty event flag is clear.
:::

**JNQMT**  *{#}S*

---

**Result:** If the CORDIC-read-but-empty event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000011111 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JQMT](#jqmt), [QMUL](#qmul), [QROTATE](#qrotate), [GETQX](#getqx), [GETQY](#getqy)

**Explanation:**

JNQMT checks the CORDIC-read-but-empty event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JQMT, allowing code to jump when the CORDIC result is ready or has not been prematurely read.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the CORDIC-read-but-empty event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNQMT is useful for ensuring CORDIC results are read at the correct time, helping to detect and handle timing errors in mathematical operations.



::: instrheader
## JNSE1 / JNSE2 / JNSE3 / JNSE4 {#jnse1}
Jump If Selectable Event Clear {#jnse2} {#jnse3} {#jnse4}

[Events and Timing](#events-and-timing) - Jumps if the selectable event flag is clear.
:::

**JNSE1**  *{#}S*
**JNSE2**  *{#}S*
**JNSE3**  *{#}S*
**JNSE4**  *{#}S*

---

**Result:** If the SEn event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000010100 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |
| EEEE | 1011110 | 01I | 000010101 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |
| EEEE | 1011110 | 01I | 000010110 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |
| EEEE | 1011110 | 01I | 000010111 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |

```{=latex}
\textsuperscript{1} PC is written only when the SEn event flag is clear.
```


**Related:** [JSE1/2/3/4](#jse1), [SETSE1/2/3/4](#setse1), [POLLSE1/2/3/4](#pollse1), [WAITSE1/2/3/4](#waitse1)

**Explanation:**

JNSE1, JNSE2, JNSE3, and JNSE4 check their respective selectable event flags and conditionally jump to the address specified by S if the flag is clear. These are the logical complements of JSE1/2/3/4, allowing code to jump when the corresponding selectable event has not occurred.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the SEn event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

The P2 provides four selectable event sources, each configurable via SETSE instructions to detect various hardware conditions. These polling mechanisms provide maximum flexibility for event-driven control flows.



::: instrheader
## JNXFI {#jnxfi}
Jump If Streamer Finished Event Clear

[Events and Timing](#events-and-timing) - Jumps if the XFI event flag is clear.
:::

**JNXFI**  *{#}S*

---

**Result:** If the XFI event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000011011 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JXFI](#jxfi), [XINIT](#xinit), [XCONT](#xcont), [POLLXFI](#pollxfi)

**Explanation:**

JNXFI checks the XFI (streamer finished) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JXFI, allowing code to jump when the streamer has not yet finished.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XFI event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNXFI is useful for polling loops that wait until the streamer completes its operation, synchronizing code execution with streamer activity.



::: instrheader
## JNXMT {#jnxmt}
Jump If Streamer Empty Event Clear

[Events and Timing](#events-and-timing) - Jumps if the XMT event flag is clear.
:::

**JNXMT**  *{#}S*

---

**Result:** If the XMT event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000011010 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JXMT](#jxmt), [XINIT](#xinit), [XCONT](#xcont), [POLLXMT](#pollxmt)

**Explanation:**

JNXMT checks the XMT (streamer empty) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JXMT, allowing code to jump when the streamer still has data to transmit.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XMT event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNXMT is useful for maintaining continuous streamer operation by reloading data only when the streamer buffer still contains data, avoiding underrun conditions.



::: instrheader
## JNXRL {#jnxrl}
Jump If Streamer LUT Rollover Event Clear

[Events and Timing](#events-and-timing) - Jumps if the XRL event flag is clear.
:::

**JNXRL**  *{#}S*

---

**Result:** If the XRL event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000011101 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JXRL](#jxrl), [XINIT](#xinit), [XCONT](#xcont), [POLLXRL](#pollxrl)

**Explanation:**

JNXRL checks the XRL (streamer LUT RAM rollover) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JXRL, allowing code to jump when the streamer LUT RAM address has not rolled over.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XRL event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNXRL is useful for implementing circular buffer management for streamer operations using LUT RAM, allowing code to detect when a buffer boundary has not yet been crossed.



::: instrheader
## JNXRO {#jnxro}
Jump If Streamer NCO Rollover Event Clear

[Events and Timing](#events-and-timing) - Jumps if the XRO event flag is clear.
:::

**JNXRO**  *{#}S*

---

**Result:** If the XRO event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000011100 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JXRO](#jxro), [XINIT](#xinit), [XCONT](#xcont), [POLLXRO](#pollxro)

**Explanation:**

JNXRO checks the XRO (streamer NCO rollover) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JXRO, allowing code to jump when the streamer's NCO (numerically controlled oscillator) has not rolled over.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XRO event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNXRO is useful for timing-sensitive streamer applications where code needs to synchronize with or detect the absence of NCO rollovers in the streaming operation.



::: instrheader
## JPAT {#jpat}
Jump If Pattern Match Event Set

[Events and Timing](#events-and-timing) - Jumps if the PAT event flag is set.
:::

**JPAT**  *{#}S*

---

**Result:** If the PAT event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000001000 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JNPAT](#jnpat), [SETPAT](#setpat), [POLLPAT](#pollpat)

**Explanation:**

JPAT checks the PAT (pattern match) event flag and conditionally jumps to the address specified by S if the flag is set. The PAT event flag is set when the I/O pins match a pattern previously configured with the SETPAT instruction.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the PAT event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JPAT is useful for implementing hardware-triggered control flow where code execution branches based on specific pin state patterns, enabling efficient event-driven programming without continuous polling.



::: instrheader
## JQMT {#jqmt}
Jump If CORDIC Empty Event Set

[Events and Timing](#events-and-timing) - Jumps if the CORDIC-read-but-empty event flag is set.
:::

**JQMT**  *{#}S*

---

**Result:** If the CORDIC-read-but-empty event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000001111 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JNQMT](#jnqmt), [QMUL](#qmul), [QROTATE](#qrotate), [GETQX](#getqx), [GETQY](#getqy)

**Explanation:**

JQMT checks the CORDIC-read-but-empty event flag and conditionally jumps to the address specified by S if the flag is set. This event flag is set when code attempts to read CORDIC results before the calculation has completed, indicating a timing error.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the CORDIC-read-but-empty event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JQMT is useful for error handling in CORDIC operations, allowing code to detect and respond to premature reads of calculation results, which can help debug timing issues in mathematical code.



::: instrheader
## JSE1 / JSE2 / JSE3 / JSE4 {#jse1}
Jump If Selectable Event Set {#jse2} {#jse3} {#jse4}

[Events and Timing](#events-and-timing) - Jumps if the selectable event flag is set.
:::

**JSE1**  *{#}S*
**JSE2**  *{#}S*
**JSE3**  *{#}S*
**JSE4**  *{#}S*

---

**Result:** If the SEn event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000000100 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |
| EEEE | 1011110 | 01I | 000000101 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |
| EEEE | 1011110 | 01I | 000000110 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |
| EEEE | 1011110 | 01I | 000000111 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |

```{=latex}
\textsuperscript{1} PC is written only when the SEn event flag is set.
```


**Related:** [JNSE1/2/3/4](#jnse1), [SETSE1/2/3/4](#setse1), [POLLSE1/2/3/4](#pollse1), [WAITSE1/2/3/4](#waitse1)

**Explanation:**

JSE1, JSE2, JSE3, and JSE4 check their respective selectable event flags and conditionally jump to the address specified by S if the flag is set. Each selectable event can be configured to detect various hardware conditions using the corresponding SETSE instruction.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the SEn event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

The P2 provides four independent selectable event sources, enabling multiple concurrent hardware event detection mechanisms for sophisticated event-driven applications.



::: instrheader
## JXFI {#jxfi}
Jump If Streamer Finished Event Set

[Events and Timing](#events-and-timing) - Jumps if the XFI event flag is set.
:::

**JXFI**  *{#}S*

---

**Result:** If the XFI event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000001011 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JNXFI](#jnxfi), [XINIT](#xinit), [XCONT](#xcont), [POLLXFI](#pollxfi)

**Explanation:**

JXFI checks the XFI (streamer finished) event flag and conditionally jumps to the address specified by S if the flag is set. The XFI event flag is set when the streamer completes its current operation.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XFI event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JXFI is useful for chaining streamer operations or triggering code execution immediately when a streaming operation completes, enabling efficient streamer-driven workflows.



::: instrheader
## JXMT {#jxmt}
Jump If Streamer Empty Event Set

[Events and Timing](#events-and-timing) - Jumps if the XMT event flag is set.
:::

**JXMT**  *{#}S*

---

**Result:** If the XMT event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000001010 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JNXMT](#jnxmt), [XINIT](#xinit), [XCONT](#xcont), [POLLXMT](#pollxmt)

**Explanation:**

JXMT checks the XMT (streamer empty) event flag and conditionally jumps to the address specified by S if the flag is set. The XMT event flag is set when the streamer's internal buffer becomes empty and needs to be refilled.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XMT event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JXMT is useful for implementing continuous streaming operations where the code needs to reload data into the streamer when the buffer empties, preventing gaps or underruns in the output stream.



::: instrheader
## JXRL {#jxrl}
Jump If Streamer LUT Rollover Event Set

[Events and Timing](#events-and-timing) - Jumps if the XRL event flag is set.
:::

**JXRL**  *{#}S*

---

**Result:** If the XRL event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000001101 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JNXRL](#jnxrl), [XINIT](#xinit), [XCONT](#xcont), [POLLXRL](#pollxrl)

**Explanation:**

JXRL checks the XRL (streamer LUT RAM rollover) event flag and conditionally jumps to the address specified by S if the flag is set. The XRL event flag is set when the streamer's LUT RAM address pointer rolls over from the end back to the beginning of the configured range.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XRL event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JXRL is useful for implementing circular buffer operations with the streamer using LUT RAM, allowing code to detect when a complete cycle through the buffer has occurred.



::: instrheader
## JXRO {#jxro}
Jump If Streamer NCO Rollover Event Set

[Events and Timing](#events-and-timing) - Jumps if the XRO event flag is set.
:::

**JXRO**  *{#}S*

---

**Result:** If the XRO event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000001100 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JNXRO](#jnxro), [XINIT](#xinit), [XCONT](#xcont), [POLLXRO](#pollxro)

**Explanation:**

JXRO checks the XRO (streamer NCO rollover) event flag and conditionally jumps to the address specified by S if the flag is set. The XRO event flag is set when the streamer's numerically controlled oscillator (NCO) rolls over, which occurs at regular intervals determined by the NCO frequency setting.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XRO event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JXRO is useful for timing-critical streamer applications where code needs to synchronize with the NCO rollovers, such as sample-rate based operations or periodic streamer updates.


