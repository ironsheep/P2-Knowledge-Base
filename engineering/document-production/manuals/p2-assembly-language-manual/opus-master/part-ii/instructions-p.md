# Instructions: P

This section contains all PASM2 instructions beginning with the letter P.



::: instrheader
## POLLATN {#pollatn}
Poll Attention event

[Events and Timing](#events-and-timing) - Polls and clears the inter-cog attention event flag.
:::

**POLLATN**  **{WC|WZ|WCZ}**

**Operation:** `C,Z = ATN event flag`; then clear flag

**Result:** Attention event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001110 | 000100100 | ATN Event | ATN Event | --- | 2 |


**Related:** [COGATN](#cogatn), [WAITATN](#waitatn), [JATN](#jatn), [JNATN](#jnatn)

**Explanation:**

POLLATN copies the state of the attention event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the attention event flag prior to clearing it.

The attention event flag is set whenever another cog issues an attention request for this cog using COGATN. The flag is cleared upon cog start, or execution of POLLATN, WAITATN, JATN, or JNATN instructions.

POLLATN does not block execution.



::: instrheader
## POLLCT1 / POLLCT2 / POLLCT3 {#pollct1}
Poll Counter event

[Events and Timing](#events-and-timing) - Polls and clears the system counter event flag.
:::

\hypertarget{pollct2}{}\hypertarget{pollct3}{}

**POLLCT1**  **{WC|WZ|WCZ}**\
**POLLCT2**  **{WC|WZ|WCZ}**\
**POLLCT3**  **{WC|WZ|WCZ}**

**Operation:** `C,Z = CTn event flag`; then clear flag

**Result:** CTn event flag state is optionally copied into C and/or Z, then the flag is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000000001 | 000100100 | CT1 Event | CT1 Event | --- | 2 |
| EEEE | 1101011 | CZ0 | 000000010 | 000100100 | CT2 Event | CT2 Event | --- | 2 |
| EEEE | 1101011 | CZ0 | 000000011 | 000100100 | CT3 Event | CT3 Event | --- | 2 |


**Related:** [ADDCT1/2/3](#addct1), [WAITCT1/2/3](#waitct1), [JCT1/2/3](#jct1), [JNCT1/2/3](#jnct1)

**Explanation:**

POLLCT1, POLLCT2, and POLLCT3 copy the state of their respective counter event flags into C and/or Z and then clear the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the counter event flag prior to clearing it.

Each counter event flag is set whenever the System Counter (CT) passes the value in that counter's event trigger register; that is, the MSB of (CT - CTn) is 0. The counter event flag is cleared upon execution of ADDCTn, POLLCTn, WAITCTn, JCTn, or JNCTn.

These instructions do not block execution. The P2 provides three independent counter event triggers (CT1, CT2, CT3).



::: instrheader
## POLLFBW {#pollfbw}
Poll FIFO Block Wrap event

[Events and Timing](#events-and-timing) - Polls and clears the FIFO block wrap event flag.
:::

**POLLFBW**  **{WC|WZ|WCZ}**

**Operation:** `C,Z = FBW event flag`; then clear flag

**Result:** FIFO-interface-block-wrap event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001001 | 000100100 | FBW Event | FBW Event | --- | 2 |


**Related:** [RDFAST](#rdfast), [WRFAST](#wrfast), [FBLOCK](#fblock), [WAITFBW](#waitfbw), [JFBW](#jfbw), [JNFBW](#jnfbw)

**Explanation:**

POLLFBW copies the state of the FIFO-interface-block-wrap event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The FIFO-interface-block-wrap event flag is set whenever the hub RAM FIFO interface exhausts its block count and reloads its block count and start address. The flag is cleared upon execution of RDFAST, WRFAST, FBLOCK, POLLFBW, WAITFBW, JFBW, or JNFBW instructions.

POLLFBW does not block execution.



::: instrheader
## POLLINT {#pollint}
Poll Interrupt event

[Events and Timing](#events-and-timing) - Polls and clears the interrupt-occurred event flag.
:::

**POLLINT**  **{WC|WZ|WCZ}**

**Operation:** `C,Z = INT event flag`; then clear flag

**Result:** Interrupt-occurred event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000000000 | 000100100 | INT Event | INT Event | --- | 2 |


**Related:** [WAITINT](#waitint), [JINT](#jint), [JNINT](#jnint)

**Explanation:**

POLLINT copies the state of the interrupt-occurred event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The interrupt-occurred event flag is set whenever interrupt 1, 2, or 3 occurs. Debug interrupts are ignored. The flag is cleared upon cog start, or execution of POLLINT, WAITINT, JINT, or JNINT instructions.

POLLINT does not block execution.



::: instrheader
## POLLPAT {#pollpat}
Poll Pin Pattern event

[Events and Timing](#events-and-timing) - Polls and clears the pin pattern match event flag.
:::

**POLLPAT**  **{WC|WZ|WCZ}**

**Operation:** `C,Z = PAT event flag`; then clear flag

**Result:** Pin-pattern-detected event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001000 | 000100100 | PAT Event | PAT Event | --- | 2 |


**Related:** [SETPAT](#setpat), [WAITPAT](#waitpat), [JPAT](#jpat), [JNPAT](#jnpat)

**Explanation:**

POLLPAT copies the state of the pin-pattern-detected event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The pin-pattern-detected event flag is set whenever the masked input pins match or don't match the pattern described by a previous SETPAT instruction. The flag is cleared upon execution of SETPAT, POLLPAT, WAITPAT, JPAT, or JNPAT instructions.

POLLPAT does not block execution.



::: instrheader
## POLLQMT {#pollqmt}
Poll CORDIC Empty event

[Events and Timing](#events-and-timing) - Polls and clears the CORDIC empty event flag.
:::

**POLLQMT**  **{WC|WZ|WCZ}**

**Operation:** `C,Z = QMT event flag`; then clear flag

**Result:** CORDIC-read-but-empty event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001111 | 000100100 | QMT Event | QMT Event | --- | 2 |


**Related:** [GETQX](#getqx), [GETQY](#getqy), [JQMT](#jqmt), [JNQMT](#jnqmt)

**Explanation:**

POLLQMT copies the state of the CORDIC-read-but-empty event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The CORDIC-read-but-empty event flag is set whenever GETQX or GETQY executes without any CORDIC results available or in progress. The flag is cleared upon cog start or execution of POLLQMT, JQMT, or JNQMT instructions. There is no WAITQMT instruction, because the event could not happen while waiting.

POLLQMT does not block execution.



::: instrheader
## POLLSE1 / POLLSE2 / POLLSE3 / POLLSE4 {#pollse1}
Poll Selectable event

[Events and Timing](#events-and-timing) - Polls and clears a configurable selectable event flag.
:::

\hypertarget{pollse2}{}\hypertarget{pollse3}{}\hypertarget{pollse4}{}

**POLLSE1**  **{WC|WZ|WCZ}**\
**POLLSE2**  **{WC|WZ|WCZ}**\
**POLLSE3**  **{WC|WZ|WCZ}**\
**POLLSE4**  **{WC|WZ|WCZ}**

**Operation:** `C,Z = SEn event flag`; then clear flag

**Result:** SEn event flag state is optionally copied into C and/or Z, then the flag is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000000100 | 000100100 | SE1 Event | SE1 Event | --- | 2 |
| EEEE | 1101011 | CZ0 | 000000101 | 000100100 | SE2 Event | SE2 Event | --- | 2 |
| EEEE | 1101011 | CZ0 | 000000110 | 000100100 | SE3 Event | SE3 Event | --- | 2 |
| EEEE | 1101011 | CZ0 | 000000111 | 000100100 | SE4 Event | SE4 Event | --- | 2 |


**Related:** [SETSE1/2/3/4](#setse1), [WAITSE1/2/3/4](#waitse1), [JSE1/2/3/4](#jse1), [JNSE1/2/3/4](#jnse1)

**Explanation:**

POLLSE1, POLLSE2, POLLSE3, and POLLSE4 copy the state of their respective selectable event flags into C and/or Z and then clear the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the selectable event flag prior to clearing it.

Each selectable event flag is set whenever the corresponding configured event occurs. The flag is cleared upon execution of SETSEn, POLLSEn, WAITSEn, JSEn, or JNSEn instructions.

The P2 provides four independent selectable event generators that can be configured to monitor various hardware conditions.



::: instrheader
## POLLXFI {#pollxfi}
Poll Streamer Finished event

[Events and Timing](#events-and-timing) - Polls and clears the streamer finished event flag.
:::

**POLLXFI**  **{WC|WZ|WCZ}**

**Operation:** `C,Z = XFI event flag`; then clear flag

**Result:** Streamer-finished event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001011 | 000100100 | XFI Event | XFI Event | --- | 2 |


**Related:** [XINIT](#xinit), [XZERO](#xzero), [XCONT](#xcont), [WAITXFI](#waitxfi), [JXFI](#jxfi), [JNXFI](#jnxfi)

**Explanation:**

POLLXFI copies the state of the streamer-finished event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The streamer-finished event flag is set whenever the streamer runs out of commands to process. The flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXFI, WAITXFI, JXFI, or JNXFI instructions.

POLLXFI does not block execution.



::: instrheader
## POLLXMT {#pollxmt}
Poll Streamer Empty event

[Events and Timing](#events-and-timing) - Polls and clears the streamer empty event flag.
:::

**POLLXMT**  **{WC|WZ|WCZ}**

**Operation:** `C,Z = XMT event flag`; then clear flag

**Result:** Streamer-empty event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001010 | 000100100 | XMT Event | XMT Event | --- | 2 |


**Related:** [XINIT](#xinit), [XZERO](#xzero), [XCONT](#xcont), [WAITXMT](#waitxmt), [JXMT](#jxmt), [JNXMT](#jnxmt)

**Explanation:**

POLLXMT copies the state of the streamer-empty event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The streamer-empty event flag is set whenever the streamer is ready for a new command. The flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXMT, WAITXMT, JXMT, or JNXMT instructions.

POLLXMT does not block execution.



::: instrheader
## POLLXRL {#pollxrl}
Poll Streamer LUT Rollover event

[Events and Timing](#events-and-timing) - Polls and clears the streamer LUT rollover event flag.
:::

**POLLXRL**  **{WC|WZ|WCZ}**

**Operation:** `C,Z = XRL event flag`; then clear flag

**Result:** Streamer-LUT-RAM-rollover event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001101 | 000100100 | XRL Event | XRL Event | --- | 2 |


**Related:** [XINIT](#xinit), [XZERO](#xzero), [XCONT](#xcont), [WAITXRL](#waitxrl), [JXRL](#jxrl), [JNXRL](#jnxrl)

**Explanation:**

POLLXRL copies the state of the streamer-LUT-RAM-rollover event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The streamer-LUT-RAM-rollover event flag is set whenever location $1FF of the Lookup RAM is read by the streamer. The flag is cleared upon cog start or upon execution of POLLXRL, WAITXRL, JXRL, or JNXRL instructions.

POLLXRL does not block execution.



::: instrheader
## POLLXRO {#pollxro}
Poll Streamer NCO Rollover event

[Events and Timing](#events-and-timing) - Polls and clears the streamer NCO rollover event flag.
:::

**POLLXRO**  **{WC|WZ|WCZ}**

**Operation:** `C,Z = XRO event flag`; then clear flag

**Result:** Streamer-NCO-rollover event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001100 | 000100100 | XRO Event | XRO Event | --- | 2 |


**Related:** [XINIT](#xinit), [XZERO](#xzero), [XCONT](#xcont), [WAITXRO](#waitxro), [JXRO](#jxro), [JNXRO](#jnxro)

**Explanation:**

POLLXRO copies the state of the streamer NCO rollover event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The streamer-NCO-rollover event flag is set whenever the streamer's numerically-controlled oscillator (NCO) rolls over. The flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXRO, WAITXRO, JXRO, or JNXRO instructions.

POLLXRO does not block execution.



::: instrheader
## POP {#pop}
Pop From Internal Stack

[Miscellaneous](#miscellaneous) - Pops the top entry of the internal hardware stack.
:::

**POP**  *Dest*  **{WC|WZ|WCZ}**

**Operation:** `D = K (stack)`; `C = K[31]`

**Result:** Dest receives the top entry (K) of the internal stack.

- Dest is the register to receive the popped value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000101011 | K[31] | result == 0 | D | 2 |


**Related:** [PUSH](#push), [POPA](#popa), [POPB](#popb)

**Explanation:**

POP pops the top entry of the internal stack, K, into the destination register Dest. The P2 has an 8-level hardware stack that CALL instructions use to store return addresses: CALL pushes and RET pops.

If the WC or WCZ effect is specified, the C flag is set to bit 31 of the popped value.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the popped value equals zero, or is cleared (0) if non-zero.

POP can retrieve any value previously stored with PUSH. Because RET and POP both take the top entry, every PUSH must be balanced by a POP before the RET that expects the return address.



::: instrheader
## POPA {#popa}
Pop From hub stack A

[Hub Memory Access](#hub-memory-access) - Pops a long from hub memory using PTRA as stack pointer.
:::

**POPA**  *Dest*  **{WC|WZ|WCZ}**

**Operation:** `D = hub[--PTRA]`; `C = long[31]`

**Result:** Dest receives the long value from hub address --PTRA.

- Dest is the register to receive the popped value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011000 | CZ1 | DDDDDDDDD | 101011111 | MSB of long | result == 0 | D | 9...16 |


**Related:** [PUSHA](#pusha), [POPB](#popb), [POP](#pop)

**Explanation:**

POPA reads a long from hub address --PTRA into the destination register Dest. PTRA is automatically decremented by 4 before the read occurs (pre-decrement). Paired with PUSHA's post-increment write to PTRA++, this implements an ascending stack that grows upward in memory (toward higher addresses).

If the WC or WCZ effect is specified, the C flag is set to the MSB (bit 31) of the popped value.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the popped value equals zero, or is cleared (0) if non-zero.

Timing is 9...16 clocks for cog execution and 9...26 clocks for hub execution. The access takes 1 more clock when it crosses a hub long.



::: instrheader
## POPB {#popb}
Pop From hub stack B

[Hub Memory Access](#hub-memory-access) - Pops a long from hub memory using PTRB as stack pointer.
:::

**POPB**  *Dest*  **{WC|WZ|WCZ}**

**Operation:** `D = hub[--PTRB]`; `C = long[31]`

**Result:** Dest receives the long value from hub address --PTRB.

- Dest is the register to receive the popped value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011000 | CZ1 | DDDDDDDDD | 111011111 | MSB of long | result == 0 | D | 9...16 |


**Related:** [PUSHB](#pushb), [POPA](#popa), [POP](#pop)

**Explanation:**

POPB reads a long from hub address --PTRB into the destination register Dest. PTRB is automatically decremented by 4 before the read occurs (pre-decrement). Paired with PUSHB's post-increment write to PTRB++, this implements an ascending stack that grows upward (toward higher addresses) in memory.

If the WC or WCZ effect is specified, the C flag is set to the MSB (bit 31) of the popped value.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the popped value equals zero, or is cleared (0) if non-zero.

Timing is 9...16 clocks for cog execution and 9...26 clocks for hub execution. The access takes 1 more clock when it crosses a hub long.

Having two independent hub stack pointers (PTRA and PTRB) allows a cog to manage separate stacks for different purposes.



::: instrheader
## PUSH {#push}
Push To Internal Stack

[Miscellaneous](#miscellaneous) - Pushes a value onto the internal hardware stack.
:::

**PUSH**  *{#}Dest*

**Result:** The value from Dest (or immediate value) becomes the new top entry (K) of the internal stack.

- Dest is a register or 9-bit immediate value (0-511) to push.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000101010 | --- | --- | --- | 2 |


**Related:** [POP](#pop), [PUSHA](#pusha), [PUSHB](#pushb)

**Explanation:**

PUSH pushes the value in Dest (or an immediate value 0-511) onto the internal stack. This instruction does not affect any flags.

The P2 has an 8-level hardware stack that CALL instructions use to store return addresses: CALL pushes and RET pops. PUSH adds a new top entry; it does not overwrite the return address below it. The next RET or POP takes the pushed value first, so each PUSH must be balanced by a POP before the RET that expects the return address.



::: instrheader
## PUSHA {#pusha}
Push To hub stack A

[Hub Memory Access](#hub-memory-access) - Pushes a long to hub memory using PTRA as stack pointer.
:::

**PUSHA**  *{#}Dest*

**Operation:** `hub[PTRA++] = D`

**Result:** The long value from Dest is written to hub address PTRA++.

- Dest is a register or 9-bit immediate value to push.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100011 | 0L1 | DDDDDDDDD | 101100001 | --- | --- | --- | 3...10 |


**Related:** [POPA](#popa), [PUSHB](#pushb), [PUSH](#push)

**Explanation:**

PUSHA writes the long value in Dest (or a 9-bit immediate value) to hub address PTRA++. PTRA is automatically incremented by 4 after the write occurs (post-increment).

This instruction does not affect any flags. The post-increment model means PTRA always points to the next available stack location after the push operation.

PUSHA paired with POPA implements an ascending stack in hub RAM (the pointer advances to higher addresses on each push).

Timing is 3...10 clocks for cog execution and 3...20 clocks for hub execution. The access takes 1 more clock when it crosses a hub long.



::: instrheader
## PUSHB {#pushb}
Push To hub stack B

[Hub Memory Access](#hub-memory-access) - Pushes a long to hub memory using PTRB as stack pointer.
:::

**PUSHB**  *{#}Dest*

**Operation:** `hub[PTRB++] = D`

**Result:** The long value from Dest is written to hub address PTRB++.

- Dest is a register or 9-bit immediate value to push.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100011 | 0L1 | DDDDDDDDD | 111100001 | --- | --- | --- | 3...10 |


**Related:** [POPB](#popb), [PUSHA](#pusha), [PUSH](#push)

**Explanation:**

PUSHB writes the long value in Dest (or a 9-bit immediate value) to hub address PTRB++. PTRB is automatically incremented by 4 after the write occurs (post-increment).

This instruction does not affect any flags. The post-increment model means PTRB always points to the next available stack location after the push operation.

Timing is 3...10 clocks for cog execution and 3...20 clocks for hub execution. The access takes 1 more clock when it crosses a hub long.

Having two independent hub stack pointers (PTRA and PTRB) allows a cog to manage separate stacks for different purposes.


