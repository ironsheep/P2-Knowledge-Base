# Instructions: P

This section contains all PASM2 instructions beginning with the letter P.



::: instrheader
## POLLATN {#pollatn}
Poll Attention Event
Category: [Event](instruction-categories.md#event)
:::

**POLLATN**  **{WC|WZ|WCZ}**

---

**Result:** Attention event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001110 | 000100100 | --- | ATN Event | ATN Event | 2 |


**Related:** [COGATN](instructions-c.md#cogatn), [WAITATN](instructions-w.md#waitatn), [JATN](instructions-j.md#jatn), [JNATN](instructions-j.md#jnatn)

**Explanation:**

POLLATN copies the state of the attention event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the attention event flag prior to clearing it.

The attention event flag is set whenever another cog issues an attention request for this cog using COGATN. The flag is cleared upon cog start, or execution of POLLATN, WAITATN, JATN, or JNATN instructions.

This instruction enables inter-cog communication by allowing a cog to check whether another cog has requested its attention without blocking execution.



::: instrheader
## POLLCT1 / POLLCT2 / POLLCT3 {#pollct1}
Poll Counter Event {#pollct2} {#pollct3}
Category: [Event](instruction-categories.md#event)
:::

**POLLCT1**  **{WC|WZ|WCZ}**
**POLLCT2**  **{WC|WZ|WCZ}**
**POLLCT3**  **{WC|WZ|WCZ}**

---

**Result:** CTn event flag state is optionally copied into C and/or Z, then the flag is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000000001 | 000100100 | --- | CT1 Event | CT1 Event | 2 |
| EEEE | 1101011 | CZ0 | 000000010 | 000100100 | --- | CT2 Event | CT2 Event | 2 |
| EEEE | 1101011 | CZ0 | 000000011 | 000100100 | --- | CT3 Event | CT3 Event | 2 |


**Related:** [ADDCT1/2/3](instructions-a.md#addct1), [WAITCT1/2/3](instructions-w.md#waitct1), [JCT1/2/3](instructions-j.md#jct1), [JNCT1/2/3](instructions-j.md#jnct1)

**Explanation:**

POLLCT1, POLLCT2, and POLLCT3 copy the state of their respective counter event flags into C and/or Z and then clear the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the counter event flag prior to clearing it.

Each counter event flag is set whenever the System Counter (CT) passes the value in that counter's event trigger register; that is, the MSB of (CT - CTn) is 0. The counter event flag is cleared upon execution of ADDCTn, POLLCTn, WAITCTn, JCTn, or JNCTn.

These instructions enable time-based event polling without blocking execution. The P2 provides three independent counter event triggers (CT1, CT2, CT3) allowing a cog to simultaneously track multiple timing requirements.



::: instrheader
## POLLFBW {#pollfbw}
Poll FIFO Block Wrap Event
Category: [Event](instruction-categories.md#event)
:::

**POLLFBW**  **{WC|WZ|WCZ}**

---

**Result:** FIFO-interface-block-wrap event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001001 | 000100100 | --- | FBW Event | FBW Event | 2 |


**Related:** [RDFAST](instructions-r.md#rdfast), [WRFAST](instructions-w.md#wrfast), [FBLOCK](instructions-f.md#fblock), [WAITFBW](instructions-w.md#waitfbw), [JFBW](instructions-j.md#jfbw), [JNFBW](instructions-j.md#jnfbw)

**Explanation:**

POLLFBW copies the state of the FIFO-interface-block-wrap event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The FIFO-interface-block-wrap event flag is set whenever the Hub RAM FIFO interface exhausts its block count and reloads its block count and start address. The flag is cleared upon execution of RDFAST, WRFAST, FBLOCK, POLLFBW, WAITFBW, JFBW, or JNFBW instructions.

This instruction enables circular buffer management for high-speed Hub RAM transfers.



::: instrheader
## POLLINT {#pollint}
Poll Interrupt Event
Category: [Event](instruction-categories.md#event)
:::

**POLLINT**  **{WC|WZ|WCZ}**

---

**Result:** Interrupt-occurred event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000000000 | 000100100 | --- | INT Event | INT Event | 2 |


**Related:** [WAITINT](instructions-w.md#waitint), [JINT](instructions-j.md#jint), [JNINT](instructions-j.md#jnint)

**Explanation:**

POLLINT copies the state of the interrupt-occurred event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The interrupt-occurred event flag is set whenever interrupt 1, 2, or 3 occurs. Debug interrupts are ignored. The flag is cleared upon cog start, or execution of POLLINT, WAITINT, JINT, or JNINT instructions.

This instruction enables non-blocking interrupt handling.



::: instrheader
## POLLPAT {#pollpat}
Poll Pin Pattern Event
Category: [Event](instruction-categories.md#event)
:::

**POLLPAT**  **{WC|WZ|WCZ}**

---

**Result:** Pin-pattern-detected event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001000 | 000100100 | --- | PAT Event | PAT Event | 2 |


**Related:** [SETPAT](instructions-s.md#setpat), [WAITPAT](instructions-w.md#waitpat), [JPAT](instructions-j.md#jpat), [JNPAT](instructions-j.md#jnpat)

**Explanation:**

POLLPAT copies the state of the pin-pattern-detected event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The pin-pattern-detected event flag is set whenever the masked input pins match or don't match the pattern described by a previous SETPAT instruction. The flag is cleared upon execution of SETPAT, POLLPAT, WAITPAT, JPAT, or JNPAT instructions.

This instruction enables non-blocking pattern detection on input pins.



::: instrheader
## POLLQMT {#pollqmt}
Poll CORDIC Empty Event
Category: [Event](instruction-categories.md#event)
:::

**POLLQMT**  **{WC|WZ|WCZ}**

---

**Result:** CORDIC-read-but-empty event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001111 | 000100100 | --- | QMT Event | QMT Event | 2 |


**Related:** [GETQX](instructions-g.md#getqx), [GETQY](instructions-g.md#getqy), [JQMT](instructions-j.md#jqmt), [JNQMT](instructions-j.md#jnqmt)

**Explanation:**

POLLQMT copies the state of the CORDIC-read-but-empty event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The CORDIC-read-but-empty event flag is set whenever GETQX or GETQY executes without any CORDIC results available or in progress. The flag is cleared upon cog start or execution of POLLQMT, WAITQMT, JQMT, or JNQMT instructions.

This instruction enables error detection for CORDIC operations.



::: instrheader
## POLLSE1 / POLLSE2 / POLLSE3 / POLLSE4 {#pollse1}
Poll Selectable Event {#pollse2} {#pollse3} {#pollse4}
Category: [Event](instruction-categories.md#event)
:::

**POLLSE1**  **{WC|WZ|WCZ}**
**POLLSE2**  **{WC|WZ|WCZ}**
**POLLSE3**  **{WC|WZ|WCZ}**
**POLLSE4**  **{WC|WZ|WCZ}**

---

**Result:** SEn event flag state is optionally copied into C and/or Z, then the flag is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000000100 | 000100100 | --- | SE1 Event | SE1 Event | 2 |
| EEEE | 1101011 | CZ0 | 000000101 | 000100100 | --- | SE2 Event | SE2 Event | 2 |
| EEEE | 1101011 | CZ0 | 000000110 | 000100100 | --- | SE3 Event | SE3 Event | 2 |
| EEEE | 1101011 | CZ0 | 000000111 | 000100100 | --- | SE4 Event | SE4 Event | 2 |


**Related:** [SETSE1/2/3/4](instructions-s.md#setse1), [WAITSE1/2/3/4](instructions-w.md#waitse1), [JSE1/2/3/4](instructions-j.md#jse1), [JNSE1/2/3/4](instructions-j.md#jnse1)

**Explanation:**

POLLSE1, POLLSE2, POLLSE3, and POLLSE4 copy the state of their respective selectable event flags into C and/or Z and then clear the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the selectable event flag prior to clearing it.

Each selectable event flag is set whenever the corresponding configured event occurs. The flag is cleared upon execution of SETSEn, POLLSEn, WAITSEn, JSEn, or JNSEn instructions.

The P2 provides four independent selectable event generators that can be configured to monitor various hardware conditions.



::: instrheader
## POLLXFI {#pollxfi}
Poll Streamer Finished Event
Category: [Event](instruction-categories.md#event)
:::

**POLLXFI**  **{WC|WZ|WCZ}**

---

**Result:** Streamer-finished event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001011 | 000100100 | --- | XFI Event | XFI Event | 2 |


**Related:** [XINIT](instructions-x.md#xinit), [XZERO](instructions-x.md#xzero), [XCONT](instructions-x.md#xcont), [WAITXFI](instructions-w.md#waitxfi), [JXFI](instructions-j.md#jxfi), [JNXFI](instructions-j.md#jnxfi)

**Explanation:**

POLLXFI copies the state of the streamer-finished event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The streamer-finished event flag is set whenever the streamer runs out of commands to process. The flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXFI, WAITXFI, JXFI, or JNXFI instructions.

This instruction enables non-blocking management of the streamer subsystem.



::: instrheader
## POLLXMT {#pollxmt}
Poll Streamer Empty Event
Category: [Event](instruction-categories.md#event)
:::

**POLLXMT**  **{WC|WZ|WCZ}**

---

**Result:** Streamer-empty event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001010 | 000100100 | --- | XMT Event | XMT Event | 2 |


**Related:** [XINIT](instructions-x.md#xinit), [XZERO](instructions-x.md#xzero), [XCONT](instructions-x.md#xcont), [WAITXMT](instructions-w.md#waitxmt), [JXMT](instructions-j.md#jxmt), [JNXMT](instructions-j.md#jnxmt)

**Explanation:**

POLLXMT copies the state of the streamer-empty event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The streamer-empty event flag is set whenever the streamer is ready for a new command. The flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXMT, WAITXMT, JXMT, or JNXMT instructions.

This instruction enables pipelined streamer operations.



::: instrheader
## POLLXRL {#pollxrl}
Poll Streamer LUT Rollover Event
Category: [Event](instruction-categories.md#event)
:::

**POLLXRL**  **{WC|WZ|WCZ}**

---

**Result:** Streamer-LUT-RAM-rollover event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001101 | 000100100 | --- | XRL Event | XRL Event | 2 |


**Related:** [XINIT](instructions-x.md#xinit), [XZERO](instructions-x.md#xzero), [XCONT](instructions-x.md#xcont), [WAITXRL](instructions-w.md#waitxrl), [JXRL](instructions-j.md#jxrl), [JNXRL](instructions-j.md#jnxrl)

**Explanation:**

POLLXRL copies the state of the streamer-LUT-RAM-rollover event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The streamer-LUT-RAM-rollover event flag is set whenever location $1FF of the Lookup RAM is read by the streamer. The flag is cleared upon cog start or upon execution of POLLXRL, WAITXRL, JXRL, or JNXRL instructions.

This instruction enables circular buffer management when using LUT RAM as a streamer data source.



::: instrheader
## POLLXRO {#pollxro}
Poll Streamer NCO Rollover Event
Category: [Event](instruction-categories.md#event)
:::

**POLLXRO**  **{WC|WZ|WCZ}**

---

**Result:** Streamer-NCO-rollover event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001100 | 000100100 | --- | XRO Event | XRO Event | 2 |


**Related:** [XINIT](instructions-x.md#xinit), [XZERO](instructions-x.md#xzero), [XCONT](instructions-x.md#xcont), [WAITXRO](instructions-w.md#waitxro), [JXRO](instructions-j.md#jxro), [JNXRO](instructions-j.md#jnxro)

**Explanation:**

POLLXRO copies the state of the streamer NCO rollover event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The streamer-NCO-rollover event flag is set whenever the streamer's numerically-controlled oscillator (NCO) rolls over. The flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXRO, WAITXRO, JXRO, or JNXRO instructions.

This instruction enables precise timing control for streamer operations that use the NCO for rate control.



::: instrheader
## POP {#pop}
Pop From Internal Stack
Category: [Miscellaneous](instruction-categories.md#miscellaneous)
:::

**POP**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** Dest receives the value from the K register.

- Dest is the register to receive the popped value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000101011 | D | K[31] | Result = 0 | 2 |


**Related:** [PUSH](#push), [POPA](#popa), [POPB](#popb)

**Explanation:**

POP pops the internal stack register K into the destination register Dest. The P2 provides a single-level internal stack register K that is automatically used by CALL instructions to store the return address.

If the WC or WCZ effect is specified, the C flag is set to bit 31 of the popped value.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the popped value equals zero, or is cleared (0) if non-zero.

POP retrieves this value, typically as part of a return sequence, though it can also be used to retrieve any value previously stored with PUSH.



::: instrheader
## POPA {#popa}
Pop From Hub Stack A
Category: [Hub RAM](instruction-categories.md#hub-ram)
:::

**POPA**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** Dest receives the long value from Hub address --PTRA.

- Dest is the register to receive the popped value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011000 | CZ1 | DDDDDDDDD | 101011111 | D | MSB of long | Result = 0 | 9...16 |


**Related:** [PUSHA](#pusha), [POPB](#popb), [POP](#pop)

**Explanation:**

POPA reads a long from Hub address --PTRA into the destination register Dest. PTRA is automatically decremented by 4 before the read occurs (pre-decrement), implementing a descending stack model where the stack grows downward in memory.

If the WC or WCZ effect is specified, the C flag is set to the MSB (bit 31) of the popped value.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the popped value equals zero, or is cleared (0) if non-zero.

This instruction enables Hub RAM-based stacks for deep subroutine nesting and large temporary storage.



::: instrheader
## POPB {#popb}
Pop From Hub Stack B
Category: [Hub RAM](instruction-categories.md#hub-ram)
:::

**POPB**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** Dest receives the long value from Hub address --PTRB.

- Dest is the register to receive the popped value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011000 | CZ1 | DDDDDDDDD | 111011111 | D | MSB of long | Result = 0 | 9...16 |


**Related:** [PUSHB](#pushb), [POPA](#popa), [POP](#pop)

**Explanation:**

POPB reads a long from Hub address --PTRB into the destination register Dest. PTRB is automatically decremented by 4 before the read occurs (pre-decrement), implementing a descending stack model where the stack grows downward in memory.

If the WC or WCZ effect is specified, the C flag is set to the MSB (bit 31) of the popped value.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the popped value equals zero, or is cleared (0) if non-zero.

Having two independent Hub stack pointers (PTRA and PTRB) allows a cog to manage separate stacks for different purposes.



::: instrheader
## PUSH {#push}
Push To Internal Stack
Category: [Miscellaneous](instruction-categories.md#miscellaneous)
:::

**PUSH**  *{#}Dest*

---

**Result:** The value from Dest (or immediate value) is stored in the K register.

- Dest is a register or 9-bit immediate value (0-511) to push.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000101010 | --- | --- | --- | 2 |


**Related:** [POP](#pop), [PUSHA](#pusha), [PUSHB](#pushb)

**Explanation:**

PUSH pushes the value in Dest (or an immediate value 0-511) onto the internal stack register K. This instruction does not affect any flags.

The P2 provides a single-level internal stack register K that is automatically used by CALL instructions to store the return address. PUSH can be used to save other values in K, though this overwrites any return address that may be stored there.



::: instrheader
## PUSHA {#pusha}
Push To Hub Stack A
Category: [Hub RAM](instruction-categories.md#hub-ram)
:::

**PUSHA**  *{#}Dest*

---

**Result:** The long value from Dest is written to Hub address PTRA++.

- Dest is a register or 9-bit immediate value to push.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100011 | 0L1 | DDDDDDDDD | 101100001 | --- | --- | --- | 3...10 |


**Related:** [POPA](#popa), [PUSHB](#pushb), [PUSH](#push)

**Explanation:**

PUSHA writes the long value in Dest (or a 9-bit immediate value) to Hub address PTRA++. PTRA is automatically incremented by 4 after the write occurs (post-increment).

This instruction does not affect any flags. The post-increment model means PTRA always points to the next available stack location after the push operation.

PUSHA paired with POPA implements a descending stack in Hub RAM.



::: instrheader
## PUSHB {#pushb}
Push To Hub Stack B
Category: [Hub RAM](instruction-categories.md#hub-ram)
:::

**PUSHB**  *{#}Dest*

---

**Result:** The long value from Dest is written to Hub address PTRB++.

- Dest is a register or 9-bit immediate value to push.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100011 | 0L1 | DDDDDDDDD | 111100001 | --- | --- | --- | 3...10 |


**Related:** [POPB](#popb), [PUSHA](#pusha), [PUSH](#push)

**Explanation:**

PUSHB writes the long value in Dest (or a 9-bit immediate value) to Hub address PTRB++. PTRB is automatically incremented by 4 after the write occurs (post-increment).

This instruction does not affect any flags. The post-increment model means PTRB always points to the next available stack location after the push operation.

Having two independent Hub stack pointers (PTRA and PTRB) allows a cog to manage separate stacks for different purposes.

