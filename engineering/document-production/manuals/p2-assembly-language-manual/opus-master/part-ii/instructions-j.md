# Instructions: J

This section contains all PASM2 instructions beginning with the letter J.

---

## JATN {#jatn}

Jump if ATN event flag is set
[Event Instruction](#event-instructions) - Jump to S if ATN (attention) event flag is set.

```
JATN  {#}S
```

**Result:** If the ATN event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000001110}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the ATN event flag is set.
```

**Related:** [JNATN](#jnatn), [COGATN](#cogatn), [POLLATT](#pollatt)

**Explanation:**

JATN checks the ATN (attention) event flag and conditionally jumps to the address specified by S if the flag is set. The ATN event flag indicates that one or more other cogs are requesting this cog's attention via the COGATN instruction.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the ATN event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JATN is useful for implementing inter-cog communication mechanisms where one cog needs to signal and get the attention of another cog for coordination or data exchange purposes.

---

## JCT1 {#jct1}

Jump if counter 1 event flag is set
[Event Instruction](#event-instructions) - Jump to S if CT1 (counter 1) event flag is set.

```
JCT1  {#}S
```

**Result:** If the CT1 event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000000001}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the CT1 event flag is set.
```

**Related:** [JCT2](#jct2), [JCT3](#jct3), [JNCT1](#jnct1), [ADDCT1](#addct1), [POLLCT1](#pollct1)

**Explanation:**

JCT1 checks the CT1 (counter 1) event flag and conditionally jumps to the address specified by S if the flag is set. The CT1 event flag is automatically set when the system counter reaches the CT1 target value that was previously configured using the ADDCT1 instruction.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the CT1 event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JCT1 is commonly used for timing loops, delays, and periodic task scheduling where code needs to execute when the system counter reaches a specific value.

---

## JCT2 {#jct2}

Jump if counter 2 event flag is set
[Event Instruction](#event-instructions) - Jump to S if CT2 (counter 2) event flag is set.

```
JCT2  {#}S
```

**Result:** If the CT2 event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000000010}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the CT2 event flag is set.
```

**Related:** [JCT1](#jct1), [JCT3](#jct3), [JNCT2](#jnct2), [ADDCT2](#addct2), [POLLCT2](#pollct2)

**Explanation:**

JCT2 checks the CT2 (counter 2) event flag and conditionally jumps to the address specified by S if the flag is set. The CT2 event flag is automatically set when the system counter reaches the CT2 target value that was previously configured using the ADDCT2 instruction.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the CT2 event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JCT2 provides a second independent hardware counter for timing operations, allowing a cog to manage two simultaneous time-based events without software overhead.

---

## JCT3 {#jct3}

Jump if counter 3 event flag is set
[Event Instruction](#event-instructions) - Jump to S if CT3 (counter 3) event flag is set.

```
JCT3  {#}S
```

**Result:** If the CT3 event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000000011}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the CT3 event flag is set.
```

**Related:** [JCT1](#jct1), [JCT2](#jct2), [JNCT3](#jnct3), [ADDCT3](#addct3), [POLLCT3](#pollct3)

**Explanation:**

JCT3 checks the CT3 (counter 3) event flag and conditionally jumps to the address specified by S if the flag is set. The CT3 event flag is automatically set when the system counter reaches the CT3 target value that was previously configured using the ADDCT3 instruction.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the CT3 event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JCT3 provides a third independent hardware counter for timing operations, enabling complex multi-event timing scenarios within a single cog.

---

## JFBW {#jfbw}

Jump if FIFO block wrap event flag is set
[Event Instruction](#event-instructions) - Jump to S if FIFO interface block wrap event flag is set.

```
JFBW  {#}S
```

**Result:** If the FIFO interface block wrap event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000001001}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the FIFO interface block wrap event flag is set.
```

**Related:** [JNFBW](#jnfbw), [RFBYTE](#rfbyte), [WFBYTE](#wfbyte), [SETQ2](#setq2)

**Explanation:**

JFBW checks the FIFO interface block wrap event flag and conditionally jumps to the address specified by S if the flag is set. This event flag is set when a FIFO read or write operation wraps around the configured block boundary.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the FIFO interface block wrap event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JFBW is useful for implementing circular buffer operations and managing block-based data transfers through the FIFO interface, allowing code to respond immediately when a block boundary has been crossed.

---

## JINT {#jint}

Jump if INT event flag is set
[Event Instruction](#event-instructions) - Jump to S if INT (interrupt) event flag is set.

```
JINT  {#}S
```

**Result:** If the INT event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000000000}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the INT event flag is set.
```

**Related:** [JNINT](#jnint), [POLLINT](#pollint), [SETINT1](#setint1), [SETINT2](#setint2), [SETINT3](#setint3)

**Explanation:**

JINT checks the INT (interrupt) event flag and conditionally jumps to the address specified by S if the flag is set. The INT event flag indicates that a hardware interrupt condition is pending, as configured by one of the SETINT instructions.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the INT event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JINT provides a polling-based mechanism for handling hardware interrupts, allowing code to check for interrupt conditions at convenient points in the program flow rather than using asynchronous interrupt handling.

---

## JMP {#jmp}

Jump
[Branch/Jump Instruction](#branch-jump-instructions) - Unconditional jump to address.

```
JMP   D          {WC/WZ/WCZ}
JMP   #{\}A
```

**Result:** PC is set to the address specified by D or A.

- D is a register containing the absolute jump address, and optionally flag values in bits [31:30].
- A is a 20-bit absolute or PC-relative address. Use \ prefix to force absolute addressing when using #.
- WC, WZ, or WCZ are optional effects to set C flag to D[31] and/or Z flag to D[30].

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1101011}{CZ0}{DDDDDDDDD}{000101100}{PC}{D[31]}{D[30]}{4}
\encodingrow{EEEE}{1101100}{RAA}{AAAAAAAAA}{AAAAAAAAA}{PC}{---}{---}{4}
\end{encodingtable}
```

**Related:** [CALL](#call), [RET](#ret), [JMPREL](#jmprel), [CALLD](#calld)

**Explanation:**

JMP performs an unconditional jump to a new address, setting the PC to either the value in register D or the immediate address A.

The first syntax form (JMP D) reads the jump address from register D and sets PC to that value. When the WC or WCZ effect is specified, the C flag is set to bit 31 of D. When the WZ or WCZ effect is specified, the Z flag is set to bit 30 of D. This allows flags to be restored as part of a jump, which is useful for return-from-subroutine operations where both PC and flags need to be restored.

The second syntax form (JMP #A) jumps to an immediate address. The R bit in the encoding determines whether the address is PC-relative (R=1) or absolute (R=0). By default, the assembler uses PC-relative addressing for # jumps. The backslash prefix (\) forces absolute addressing: JMP #\address.

For PC-relative jumps in COG execution mode, the 20-bit address field is added to PC. For Hub execution mode, the lower 18 bits are shifted left by 2 (multiplied by 4) before being added to PC, since Hub addresses are long-aligned.

The instruction executes in 4 clock cycles in COG execution mode. In Hub execution mode, jumps take 13-20 clock cycles depending on Hub access timing.

---

## JMPREL {#jmprel}

Jump relative
[Branch/Jump Instruction](#branch-jump-instructions) - Jump ahead or back by D instructions.

```
JMPREL  {#}D
```

**Result:** PC is incremented or decremented by the value in D.

- D is a register or 9-bit literal specifying the signed offset in instructions. For COG execution, PC += D[19:0]. For Hub execution, PC += D[17:0] << 2.

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000110000}{PC}{---}{---}{4}
```

**Related:** [JMP](#jmp), [CALL](#call), [DJNZ](#djnz), [IJMP](#ijmp)

**Explanation:**

JMPREL performs a relative jump by adding or subtracting the value in D to the current PC value. This allows position-independent code that can jump forward or backward by a specified number of instructions without knowing the absolute address.

For COG execution mode, the lower 20 bits of D are added to PC. Positive values jump forward, negative values (in two's complement) jump backward. The offset is in units of instructions (longs).

For Hub execution mode, the lower 18 bits of D are shifted left by 2 bits (multiplied by 4) before being added to PC. This accounts for the fact that Hub addresses are byte addresses and each instruction occupies 4 bytes. The offset is still conceptually in units of instructions.

The instruction executes in 4 clock cycles in COG execution mode. In Hub execution mode, jumps take 13-20 clock cycles depending on Hub access timing.

JMPREL is useful for implementing position-independent code, jump tables, and dynamic control flow where the jump offset is computed at runtime.

---

## JNATN {#jnatn}

Jump if ATN event flag is clear
[Event Instruction](#event-instructions) - Jump to S if ATN (attention) event flag is clear.

```
JNATN  {#}S
```

**Result:** If the ATN event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000011110}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the ATN event flag is clear.
```

**Related:** [JATN](#jatn), [COGATN](#cogatn), [POLLATT](#pollatt)

**Explanation:**

JNATN checks the ATN (attention) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JATN, allowing code to jump when no other cog is requesting attention.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the ATN event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNATN is useful for implementing polling loops that wait until the ATN flag is clear before proceeding with other operations.

---

## JNCT1 {#jnct1}

Jump if counter 1 event flag is clear
[Event Instruction](#event-instructions) - Jump to S if CT1 (counter 1) event flag is clear.

```
JNCT1  {#}S
```

**Result:** If the CT1 event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000010001}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the CT1 event flag is clear.
```

**Related:** [JNCT2](#jnct2), [JNCT3](#jnct3), [JCT1](#jct1), [ADDCT1](#addct1), [POLLCT1](#pollct1)

**Explanation:**

JNCT1 checks the CT1 (counter 1) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JCT1, allowing code to jump when the counter 1 event has not yet occurred.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the CT1 event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNCT1 is useful for implementing polling loops that continue until the CT1 counter event occurs, or for skipping code that should only execute before a specific time.

---

## JNCT2 {#jnct2}

Jump if counter 2 event flag is clear
[Event Instruction](#event-instructions) - Jump to S if CT2 (counter 2) event flag is clear.

```
JNCT2  {#}S
```

**Result:** If the CT2 event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000010010}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the CT2 event flag is clear.
```

**Related:** [JNCT1](#jnct1), [JNCT3](#jnct3), [JCT2](#jct2), [ADDCT2](#addct2), [POLLCT2](#pollct2)

**Explanation:**

JNCT2 checks the CT2 (counter 2) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JCT2, allowing code to jump when the counter 2 event has not yet occurred.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the CT2 event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNCT2 provides the same polling capability as JNCT1 but for the independent counter 2 event, enabling complex multi-timer control flows.

---

## JNCT3 {#jnct3}

Jump if counter 3 event flag is clear
[Event Instruction](#event-instructions) - Jump to S if CT3 (counter 3) event flag is clear.

```
JNCT3  {#}S
```

**Result:** If the CT3 event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000010011}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the CT3 event flag is clear.
```

**Related:** [JNCT1](#jnct1), [JNCT2](#jnct2), [JCT3](#jct3), [ADDCT3](#addct3), [POLLCT3](#pollct3)

**Explanation:**

JNCT3 checks the CT3 (counter 3) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JCT3, allowing code to jump when the counter 3 event has not yet occurred.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the CT3 event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNCT3 completes the set of three independent counter event polling mechanisms, allowing sophisticated timing control with minimal code overhead.

---

## JNFBW {#jnfbw}

Jump if FIFO block wrap event flag is clear
[Event Instruction](#event-instructions) - Jump to S if FIFO interface block wrap event flag is clear.

```
JNFBW  {#}S
```

**Result:** If the FIFO interface block wrap event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000011001}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the FIFO interface block wrap event flag is clear.
```

**Related:** [JFBW](#jfbw), [RFBYTE](#rfbyte), [WFBYTE](#wfbyte), [SETQ2](#setq2)

**Explanation:**

JNFBW checks the FIFO interface block wrap event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JFBW, allowing code to jump when no block wrap has occurred.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the FIFO interface block wrap event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNFBW is useful for polling loops that wait until a block wrap occurs, or for conditional code that should only execute when within a block boundary.

---

## JNINT {#jnint}

Jump if INT event flag is clear
[Event Instruction](#event-instructions) - Jump to S if INT (interrupt) event flag is clear.

```
JNINT  {#}S
```

**Result:** If the INT event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000010000}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the INT event flag is clear.
```

**Related:** [JINT](#jint), [POLLINT](#pollint), [SETINT1](#setint1), [SETINT2](#setint2), [SETINT3](#setint3)

**Explanation:**

JNINT checks the INT (interrupt) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JINT, allowing code to jump when no interrupt is pending.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the INT event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNINT is useful for polling loops that wait until an interrupt occurs, or for implementing interrupt-safe critical sections that should only execute when interrupts are not pending.

---

## JNPAT {#jnpat}

Jump if pattern match event flag is clear
[Event Instruction](#event-instructions) - Jump to S if PAT (pattern match) event flag is clear.

```
JNPAT  {#}S
```

**Result:** If the PAT event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000011000}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the PAT event flag is clear.
```

**Related:** [JPAT](#jpat), [SETPAT](#setpat), [POLLPAT](#pollpat)

**Explanation:**

JNPAT checks the PAT (pattern match) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JPAT, allowing code to jump when no pattern match has occurred.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the PAT event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNPAT is useful for polling loops that wait until a specific pattern appears on the I/O pins, or for conditional logic that should execute only when the pattern has not yet matched.

---

## JNQMT {#jnqmt}

Jump if CORDIC empty event flag is clear
[Event Instruction](#event-instructions) - Jump to S if CORDIC-read-but-empty event flag is clear.

```
JNQMT  {#}S
```

**Result:** If the CORDIC-read-but-empty event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000011111}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the CORDIC-read-but-empty event flag is clear.
```

**Related:** [JQMT](#jqmt), [QMUL](#qmul), [QROTATE](#qrotate), [GETQX](#getqx), [GETQY](#getqy)

**Explanation:**

JNQMT checks the CORDIC-read-but-empty event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JQMT, allowing code to jump when the CORDIC result is ready or has not been prematurely read.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the CORDIC-read-but-empty event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNQMT is useful for ensuring CORDIC results are read at the correct time, helping to detect and handle timing errors in mathematical operations.

---

## JNSE1 {#jnse1}

Jump if selector 1 event flag is clear
[Event Instruction](#event-instructions) - Jump to S if SE1 (selector 1) event flag is clear.

```
JNSE1  {#}S
```

**Result:** If the SE1 event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000010100}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the SE1 event flag is clear.
```

**Related:** [JNSE2](#jnse2), [JNSE3](#jnse3), [JNSE4](#jnse4), [JSE1](#jse1), [SETSE1](#setse1)

**Explanation:**

JNSE1 checks the SE1 (selector 1) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JSE1, allowing code to jump when the selector 1 event has not occurred.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the SE1 event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNSE1 provides polling capability for the first of four selectable event sources, which can be configured to detect various hardware conditions.

---

## JNSE2 {#jnse2}

Jump if selector 2 event flag is clear
[Event Instruction](#event-instructions) - Jump to S if SE2 (selector 2) event flag is clear.

```
JNSE2  {#}S
```

**Result:** If the SE2 event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000010101}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the SE2 event flag is clear.
```

**Related:** [JNSE1](#jnse1), [JNSE3](#jnse3), [JNSE4](#jnse4), [JSE2](#jse2), [SETSE2](#setse2)

**Explanation:**

JNSE2 checks the SE2 (selector 2) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JSE2, allowing code to jump when the selector 2 event has not occurred.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the SE2 event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNSE2 provides polling capability for the second of four selectable event sources, enabling independent monitoring of multiple hardware events.

---

## JNSE3 {#jnse3}

Jump if selector 3 event flag is clear
[Event Instruction](#event-instructions) - Jump to S if SE3 (selector 3) event flag is clear.

```
JNSE3  {#}S
```

**Result:** If the SE3 event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000010110}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the SE3 event flag is clear.
```

**Related:** [JNSE1](#jnse1), [JNSE2](#jnse2), [JNSE4](#jnse4), [JSE3](#jse3), [SETSE3](#setse3)

**Explanation:**

JNSE3 checks the SE3 (selector 3) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JSE3, allowing code to jump when the selector 3 event has not occurred.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the SE3 event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNSE3 provides polling capability for the third of four selectable event sources, supporting complex event-driven control flows.

---

## JNSE4 {#jnse4}

Jump if selector 4 event flag is clear
[Event Instruction](#event-instructions) - Jump to S if SE4 (selector 4) event flag is clear.

```
JNSE4  {#}S
```

**Result:** If the SE4 event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000010111}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the SE4 event flag is clear.
```

**Related:** [JNSE1](#jnse1), [JNSE2](#jnse2), [JNSE3](#jnse3), [JSE4](#jse4), [SETSE4](#setse4)

**Explanation:**

JNSE4 checks the SE4 (selector 4) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JSE4, allowing code to jump when the selector 4 event has not occurred.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the SE4 event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNSE4 completes the set of four selectable event polling mechanisms, providing maximum flexibility for hardware event monitoring.

---

## JNXFI {#jnxfi}

Jump if streamer finished event flag is clear
[Event Instruction](#event-instructions) - Jump to S if XFI (streamer finished) event flag is clear.

```
JNXFI  {#}S
```

**Result:** If the XFI event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000011011}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the XFI event flag is clear.
```

**Related:** [JXFI](#jxfi), [XINIT](#xinit), [XCONT](#xcont), [POLLXFI](#pollxfi)

**Explanation:**

JNXFI checks the XFI (streamer finished) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JXFI, allowing code to jump when the streamer has not yet finished.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XFI event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNXFI is useful for polling loops that wait until the streamer completes its operation, synchronizing code execution with streamer activity.

---

## JNXMT {#jnxmt}

Jump if streamer empty event flag is clear
[Event Instruction](#event-instructions) - Jump to S if XMT (streamer empty) event flag is clear.

```
JNXMT  {#}S
```

**Result:** If the XMT event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000011010}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the XMT event flag is clear.
```

**Related:** [JXMT](#jxmt), [XINIT](#xinit), [XCONT](#xcont), [POLLXMT](#pollxmt)

**Explanation:**

JNXMT checks the XMT (streamer empty) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JXMT, allowing code to jump when the streamer still has data to transmit.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XMT event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNXMT is useful for maintaining continuous streamer operation by reloading data only when the streamer buffer still contains data, avoiding underrun conditions.

---

## JNXRL {#jnxrl}

Jump if streamer LUT rollover event flag is clear
[Event Instruction](#event-instructions) - Jump to S if XRL (streamer LUT RAM rollover) event flag is clear.

```
JNXRL  {#}S
```

**Result:** If the XRL event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000011101}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the XRL event flag is clear.
```

**Related:** [JXRL](#jxrl), [XINIT](#xinit), [XCONT](#xcont), [POLLXRL](#pollxrl)

**Explanation:**

JNXRL checks the XRL (streamer LUT RAM rollover) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JXRL, allowing code to jump when the streamer LUT RAM address has not rolled over.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XRL event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNXRL is useful for implementing circular buffer management for streamer operations using LUT RAM, allowing code to detect when a buffer boundary has not yet been crossed.

---

## JNXRO {#jnxro}

Jump if streamer NCO rollover event flag is clear
[Event Instruction](#event-instructions) - Jump to S if XRO (streamer NCO rollover) event flag is clear.

```
JNXRO  {#}S
```

**Result:** If the XRO event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000011100}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the XRO event flag is clear.
```

**Related:** [JXRO](#jxro), [XINIT](#xinit), [XCONT](#xcont), [POLLXRO](#pollxro)

**Explanation:**

JNXRO checks the XRO (streamer NCO rollover) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JXRO, allowing code to jump when the streamer's NCO (numerically controlled oscillator) has not rolled over.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XRO event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNXRO is useful for timing-sensitive streamer applications where code needs to synchronize with or detect the absence of NCO rollovers in the streaming operation.

---

## JPAT {#jpat}

Jump if pattern match event flag is set
[Event Instruction](#event-instructions) - Jump to S if PAT (pattern match) event flag is set.

```
JPAT  {#}S
```

**Result:** If the PAT event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000001000}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the PAT event flag is set.
```

**Related:** [JNPAT](#jnpat), [SETPAT](#setpat), [POLLPAT](#pollpat)

**Explanation:**

JPAT checks the PAT (pattern match) event flag and conditionally jumps to the address specified by S if the flag is set. The PAT event flag is set when the I/O pins match a pattern previously configured with the SETPAT instruction.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the PAT event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JPAT is useful for implementing hardware-triggered control flow where code execution branches based on specific pin state patterns, enabling efficient event-driven programming without continuous polling.

---

## JQMT {#jqmt}

Jump if CORDIC empty event flag is set
[Event Instruction](#event-instructions) - Jump to S if CORDIC-read-but-empty event flag is set.

```
JQMT  {#}S
```

**Result:** If the CORDIC-read-but-empty event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000001111}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the CORDIC-read-but-empty event flag is set.
```

**Related:** [JNQMT](#jnqmt), [QMUL](#qmul), [QROTATE](#qrotate), [GETQX](#getqx), [GETQY](#getqy)

**Explanation:**

JQMT checks the CORDIC-read-but-empty event flag and conditionally jumps to the address specified by S if the flag is set. This event flag is set when code attempts to read CORDIC results before the calculation has completed, indicating a timing error.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the CORDIC-read-but-empty event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JQMT is useful for error handling in CORDIC operations, allowing code to detect and respond to premature reads of calculation results, which can help debug timing issues in mathematical code.

---

## JSE1 {#jse1}

Jump if selector 1 event flag is set
[Event Instruction](#event-instructions) - Jump to S if SE1 (selector 1) event flag is set.

```
JSE1  {#}S
```

**Result:** If the SE1 event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000000100}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the SE1 event flag is set.
```

**Related:** [JSE2](#jse2), [JSE3](#jse3), [JSE4](#jse4), [JNSE1](#jnse1), [SETSE1](#setse1)

**Explanation:**

JSE1 checks the SE1 (selector 1) event flag and conditionally jumps to the address specified by S if the flag is set. The selector 1 event can be configured to detect various hardware conditions using the SETSE1 instruction.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the SE1 event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JSE1 is the first of four selectable event polling instructions, providing flexible hardware event detection for custom event handling.

---

## JSE2 {#jse2}

Jump if selector 2 event flag is set
[Event Instruction](#event-instructions) - Jump to S if SE2 (selector 2) event flag is set.

```
JSE2  {#}S
```

**Result:** If the SE2 event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000000101}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the SE2 event flag is set.
```

**Related:** [JSE1](#jse1), [JSE3](#jse3), [JSE4](#jse4), [JNSE2](#jnse2), [SETSE2](#setse2)

**Explanation:**

JSE2 checks the SE2 (selector 2) event flag and conditionally jumps to the address specified by S if the flag is set. The selector 2 event can be configured to detect various hardware conditions using the SETSE2 instruction.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the SE2 event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JSE2 provides a second independent selectable event source, enabling multiple concurrent hardware event detection mechanisms.

---

## JSE3 {#jse3}

Jump if selector 3 event flag is set
[Event Instruction](#event-instructions) - Jump to S if SE3 (selector 3) event flag is set.

```
JSE3  {#}S
```

**Result:** If the SE3 event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000000110}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the SE3 event flag is set.
```

**Related:** [JSE1](#jse1), [JSE2](#jse2), [JSE4](#jse4), [JNSE3](#jnse3), [SETSE3](#setse3)

**Explanation:**

JSE3 checks the SE3 (selector 3) event flag and conditionally jumps to the address specified by S if the flag is set. The selector 3 event can be configured to detect various hardware conditions using the SETSE3 instruction.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the SE3 event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JSE3 provides a third independent selectable event source for sophisticated event-driven applications.

---

## JSE4 {#jse4}

Jump if selector 4 event flag is set
[Event Instruction](#event-instructions) - Jump to S if SE4 (selector 4) event flag is set.

```
JSE4  {#}S
```

**Result:** If the SE4 event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000000111}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the SE4 event flag is set.
```

**Related:** [JSE1](#jse1), [JSE2](#jse2), [JSE3](#jse3), [JNSE4](#jnse4), [SETSE4](#setse4)

**Explanation:**

JSE4 checks the SE4 (selector 4) event flag and conditionally jumps to the address specified by S if the flag is set. The selector 4 event can be configured to detect various hardware conditions using the SETSE4 instruction.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the SE4 event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JSE4 completes the set of four selectable event sources, providing maximum flexibility for complex event-driven control flow.

---

## JXFI {#jxfi}

Jump if streamer finished event flag is set
[Event Instruction](#event-instructions) - Jump to S if XFI (streamer finished) event flag is set.

```
JXFI  {#}S
```

**Result:** If the XFI event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000001011}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the XFI event flag is set.
```

**Related:** [JNXFI](#jnxfi), [XINIT](#xinit), [XCONT](#xcont), [POLLXFI](#pollxfi)

**Explanation:**

JXFI checks the XFI (streamer finished) event flag and conditionally jumps to the address specified by S if the flag is set. The XFI event flag is set when the streamer completes its current operation.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XFI event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JXFI is useful for chaining streamer operations or triggering code execution immediately when a streaming operation completes, enabling efficient streamer-driven workflows.

---

## JXMT {#jxmt}

Jump if streamer empty event flag is set
[Event Instruction](#event-instructions) - Jump to S if XMT (streamer empty) event flag is set.

```
JXMT  {#}S
```

**Result:** If the XMT event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000001010}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the XMT event flag is set.
```

**Related:** [JNXMT](#jnxmt), [XINIT](#xinit), [XCONT](#xcont), [POLLXMT](#pollxmt)

**Explanation:**

JXMT checks the XMT (streamer empty) event flag and conditionally jumps to the address specified by S if the flag is set. The XMT event flag is set when the streamer's internal buffer becomes empty and needs to be refilled.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XMT event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JXMT is useful for implementing continuous streaming operations where the code needs to reload data into the streamer when the buffer empties, preventing gaps or underruns in the output stream.

---

## JXRL {#jxrl}

Jump if streamer LUT rollover event flag is set
[Event Instruction](#event-instructions) - Jump to S if XRL (streamer LUT RAM rollover) event flag is set.

```
JXRL  {#}S
```

**Result:** If the XRL event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000001101}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the XRL event flag is set.
```

**Related:** [JNXRL](#jnxrl), [XINIT](#xinit), [XCONT](#xcont), [POLLXRL](#pollxrl)

**Explanation:**

JXRL checks the XRL (streamer LUT RAM rollover) event flag and conditionally jumps to the address specified by S if the flag is set. The XRL event flag is set when the streamer's LUT RAM address pointer rolls over from the end back to the beginning of the configured range.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XRL event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JXRL is useful for implementing circular buffer operations with the streamer using LUT RAM, allowing code to detect when a complete cycle through the buffer has occurred.

---

## JXRO {#jxro}

Jump if streamer NCO rollover event flag is set
[Event Instruction](#event-instructions) - Jump to S if XRO (streamer NCO rollover) event flag is set.

```
JXRO  {#}S
```

**Result:** If the XRO event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.

```{=latex}
\simpleencoding{EEEE}{1011110}{01I}{000001100}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4}

\textsuperscript{1} PC is written only when the XRO event flag is set.
```

**Related:** [JNXRO](#jnxro), [XINIT](#xinit), [XCONT](#xcont), [POLLXRO](#pollxro)

**Explanation:**

JXRO checks the XRO (streamer NCO rollover) event flag and conditionally jumps to the address specified by S if the flag is set. The XRO event flag is set when the streamer's numerically controlled oscillator (NCO) rolls over, which occurs at regular intervals determined by the NCO frequency setting.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XRO event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JXRO is useful for timing-critical streamer applications where code needs to synchronize with the NCO rollovers, such as sample-rate based operations or periodic streamer updates.

---
