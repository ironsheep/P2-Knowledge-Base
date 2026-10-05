# Instructions: W

This section contains all PASM2 instructions beginning with the letter W.



::: instrheader
## WAITATN {#waitatn}
Wait For Attention

[Events and Timing](#events-and-timing) - Waits for an attention event from another cog.
:::

**WAITATN**  **{WC|WZ|WCZ}**

**Operation:** wait for ATN event then clear; (prior SETQ = CT timeout) `C/Z = timeout`

**Result:** Waits for an attention event to occur (unless the event flag is already set), then clears the event flag (unless it's being set again by the event sensor) and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.
- The timeout is armed by a `SETQ` (a future System-Counter target) placed immediately before this instruction; the wait then releases on the event **or** the deadline, whichever comes first — C/Z = 1 if the timeout won, 0 if the event won. With **no** preceding `SETQ` no timeout is armed, so the event always wins and `WC` clears C, `WZ` clears Z and `WCZ` clears both (a valid one-instruction flag-clear).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000011110 | 000100100 | Timeout | Timeout | --- | 2+ |


**Related:** [COGATN](#cogatn), [POLLATN](#pollatn), [JATN](#jatn), [JNATN](#jnatn)

**Explanation:**

WAITATN waits for an attention event to occur, stalling the pipeline until the event flag is set. The attention event flag is set whenever another cog issues an attention request for this cog using COGATN. The flag is cleared upon cog start or execution of POLLATN, WAITATN, JATN, or JNATN instructions.

To set an optional timeout, insert a SETQ instruction (with a future System Counter target value) immediately before WAITATN. With a timeout armed, WC, WZ, or WCZ reports the outcome: the flags are set (1) if the timeout occurred before the event, or cleared (0) if the event occurred before the timeout. Without a preceding SETQ, the effects clear the flags, as described above.

During a wait, the pipeline is stalled—no instructions execute and no interrupts are processed in the cog until the wait condition ends.

```pasm2
        WAITATN                ' Wait for attention from another cog
```



::: instrheader
## WAITCT1 / WAITCT2 / WAITCT3 {#waitct1}
Wait For Counter Event

[Events and Timing](#events-and-timing) - Waits for a counter event flag to be set.
:::

\hypertarget{waitct2}{}\hypertarget{waitct3}{}

**WAITCT1**  **{WC|WZ|WCZ}**\
**WAITCT2**  **{WC|WZ|WCZ}**\
**WAITCT3**  **{WC|WZ|WCZ}**

**Operation:** wait for CTn event then clear; `C/Z = timeout` (prior SETQ = CT timeout)

**Result:** Waits for the specified counter event flag (CT1, CT2, or CT3) to be set, then clears the flag (unless it's being set again by the event sensor) and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.
- The timeout is armed by a `SETQ` (a future System-Counter target) placed immediately before this instruction; the wait then releases on the event **or** the deadline, whichever comes first — C/Z = 1 if the timeout won, 0 if the event won. With **no** preceding `SETQ` no timeout is armed, so the event always wins and `WC` clears C, `WZ` clears Z and `WCZ` clears both (a valid one-instruction flag-clear).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000010001 | 000100100 | Timeout | Timeout | --- | 2+ |
| EEEE | 1101011 | CZ0 | 000010010 | 000100100 | Timeout | Timeout | --- | 2+ |
| EEEE | 1101011 | CZ0 | 000010011 | 000100100 | Timeout | Timeout | --- | 2+ |


**Related:** [ADDCT1](#addct1), [ADDCT2](#addct2), [ADDCT3](#addct3), [POLLCT1](#pollct1), [POLLCT2](#pollct2), [POLLCT3](#pollct3), [JCT1](#jct1), [JCT2](#jct2), [JCT3](#jct3)

**Explanation:**

WAITCT1, WAITCT2, and WAITCT3 wait for counter events 1, 2, or 3 respectively, stalling the pipeline until the corresponding event flag is set. Each counter event flag is set whenever the System Counter (CT) passes the value in the corresponding event trigger register (CT1, CT2, or CT3). Specifically, the flag is set when the MSB of (CT - CTx) equals 0, so the comparison is correct across counter wraparound.

The flags are cleared by execution of ADDCT*n*, POLLCT*n*, WAITCT*n*, JCT*n*, or JNCT*n* instructions (where *n* is 1, 2, or 3).

To set an optional timeout, insert a SETQ instruction immediately before the WAITCTn instruction.



::: instrheader
## WAITFBW {#waitfbw}
Wait For FIFO Block Wrap

[Events and Timing](#events-and-timing) - Waits for a FIFO block wrap event.
:::

**WAITFBW**  **{WC|WZ|WCZ}**

**Operation:** wait for FBW event then clear; `C/Z = timeout` (prior SETQ = CT timeout)

**Result:** Waits for a FIFO-interface-block-wrap event to occur, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.
- The timeout is armed by a `SETQ` (a future System-Counter target) placed immediately before this instruction; the wait then releases on the event **or** the deadline, whichever comes first — C/Z = 1 if the timeout won, 0 if the event won. With **no** preceding `SETQ` no timeout is armed, so the event always wins and `WC` clears C, `WZ` clears Z and `WCZ` clears both (a valid one-instruction flag-clear).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000011001 | 000100100 | Timeout | Timeout | --- | 2+ |


**Related:** [RDFAST](#rdfast), [WRFAST](#wrfast), [FBLOCK](#fblock), [POLLFBW](#pollfbw)

**Explanation:**

WAITFBW waits for a FIFO-interface-block-wrap event to occur, stalling the pipeline until the event flag is set. The FIFO-interface-block-wrap event flag is set whenever the hub RAM FIFO interface exhausts its block count and reloads its block count and start address.

The FIFO-interface-block-wrap event flag is cleared upon execution of RDFAST, WRFAST, FBLOCK, POLLFBW, WAITFBW, JFBW, or JNFBW instructions.



::: instrheader
## WAITINT {#waitint}
Wait For Interrupt

[Events and Timing](#events-and-timing) - Waits for an interrupt event to occur.
:::

**WAITINT**  **{WC|WZ|WCZ}**

**Operation:** wait for INT event then clear; `C/Z = timeout` (prior SETQ = CT timeout)

**Result:** Waits for an interrupt-occurred event, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.
- The timeout is armed by a `SETQ` (a future System-Counter target) placed immediately before this instruction; the wait then releases on the event **or** the deadline, whichever comes first — C/Z = 1 if the timeout won, 0 if the event won. With **no** preceding `SETQ` no timeout is armed, so the event always wins and `WC` clears C, `WZ` clears Z and `WCZ` clears both (a valid one-instruction flag-clear).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000010000 | 000100100 | Timeout | Timeout | --- | 2+ |


**Related:** [POLLINT](#pollint), [JINT](#jint), [JNINT](#jnint)

**Explanation:**

WAITINT waits for an interrupt-occurred event to occur, stalling the pipeline until the event flag is set. The interrupt-occurred event flag is set whenever interrupt 1, 2, or 3 occurs—debug interrupts are ignored.

The interrupt-occurred event flag is cleared upon cog start or execution of POLLINT, WAITINT, JINT, or JNINT instructions.



::: instrheader
## WAITPAT {#waitpat}
Wait For Pattern

[Events and Timing](#events-and-timing) - Waits for a pin pattern match event.
:::

**WAITPAT**  **{WC|WZ|WCZ}**

**Operation:** wait for PAT event then clear; `C/Z = timeout` (prior SETQ = CT timeout)

**Result:** Waits for a pin-pattern-detected event, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.
- The timeout is armed by a `SETQ` (a future System-Counter target) placed immediately before this instruction; the wait then releases on the event **or** the deadline, whichever comes first — C/Z = 1 if the timeout won, 0 if the event won. With **no** preceding `SETQ` no timeout is armed, so the event always wins and `WC` clears C, `WZ` clears Z and `WCZ` clears both (a valid one-instruction flag-clear).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000011000 | 000100100 | Timeout | Timeout | --- | 2+ |


**Related:** [SETPAT](#setpat), [POLLPAT](#pollpat), [JPAT](#jpat), [JNPAT](#jnpat)

**Explanation:**

WAITPAT waits for a pin-pattern-detected event to occur, stalling the pipeline until the event flag is set. The pin-pattern-detected event flag is set whenever the masked input pins match or don't match the pattern described by a previous SETPAT instruction.

The pin-pattern-detected event flag is cleared upon execution of SETPAT, POLLPAT, WAITPAT, JPAT, or JNPAT instructions.

SETPAT reads C and Z as inputs: C selects INA (0) or INB (1), and Z selects `==` (1) or `!=` (0) for the comparison. Set them before SETPAT.

```pasm2
        MODCZ   _clr, _set WCZ ' C = 0 (INA), Z = 1 (match when ==)
        SETPAT  mask, pattern  ' Set up pattern detector
        WAITPAT                ' Wait for pattern match
```



::: instrheader
## WAITSE1 / WAITSE2 / WAITSE3 / WAITSE4 {#waitse1}
Wait For Selectable Event (1, 2, 3, Or 4)

[Events and Timing](#events-and-timing) - Waits for a selectable event flag to be set.
:::

\hypertarget{waitse2}{}\hypertarget{waitse3}{}\hypertarget{waitse4}{}

**WAITSE1**  **{WC|WZ|WCZ}**\
**WAITSE2**  **{WC|WZ|WCZ}**\
**WAITSE3**  **{WC|WZ|WCZ}**\
**WAITSE4**  **{WC|WZ|WCZ}**

**Operation:** wait for SEn event then clear; `C/Z = timeout` (prior SETQ = CT timeout)

**Result:** Waits for the specified selectable event flag (SE1-SE4) to be set, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.
- The timeout is armed by a `SETQ` (a future System-Counter target) placed immediately before this instruction; the wait then releases on the event **or** the deadline, whichever comes first — C/Z = 1 if the timeout won, 0 if the event won. With **no** preceding `SETQ` no timeout is armed, so the event always wins and `WC` clears C, `WZ` clears Z and `WCZ` clears both (a valid one-instruction flag-clear). The `SETQ` timeout (event first gives C = 0, timeout first gives C = 1) and the `WCZ` flag-clear are hardware-verified on P2 silicon.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000010100 | 000100100 | Timeout | Timeout | --- | 2+ |
| EEEE | 1101011 | CZ0 | 000010101 | 000100100 | Timeout | Timeout | --- | 2+ |
| EEEE | 1101011 | CZ0 | 000010110 | 000100100 | Timeout | Timeout | --- | 2+ |
| EEEE | 1101011 | CZ0 | 000010111 | 000100100 | Timeout | Timeout | --- | 2+ |


**Related:** [SETSE1/2/3/4](#setse1), [POLLSE1/2/3/4](#pollse1), [JSE1/2/3/4](#jse1), [JNSE1/2/3/4](#jnse1)

**Explanation:**

WAITSE1, WAITSE2, WAITSE3, and WAITSE4 wait for their respective selectable events to occur, stalling the pipeline until the corresponding SE flag is set.

Each selectable event flag is cleared by execution of its respective SETSEn, POLLSEn, WAITSEn, JSEn, or JNSEn instruction.



::: instrheader
## WAITX {#waitx}
Wait Cycles

[Miscellaneous](#miscellaneous) - Stalls the cog for a precise number of clock cycles.
:::

**WAITX**  *{#}Dest*  **{WC|WZ|WCZ}**

**Operation:** wait `2 + D` clocks; if WC/WZ/WCZ wait `2 + (D & RND)` clocks; `C/Z = 0`

**Result:** Stalls the cog for 2 + Dest clock cycles. If WC/WZ/WCZ is specified, waits 2 + (Dest AND RND) clocks for a randomized delay and clears the flag(s) the effect names to 0 after completion (WC clears C, WZ clears Z, WCZ clears both).

- Dest is the delay value; total wait is 2 + Dest cycles (0-511 for immediate).
- WC, WZ, or WCZ enable randomized delay mode; the flag(s) the effect names are set to 0 after completion.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 000011111 | 0 | 0 | --- | 2 + D |


**Related:** [WAITCT1](#waitct1), [WAITCT2](#waitct2), [WAITCT3](#waitct3)

**Explanation:**

WAITX stalls the cog for 2 + Dest clock cycles. When WC, WZ, or WCZ is specified, the delay becomes randomized: 2 + (Dest AND RND) clocks, where RND is a random value. WAITX is critical for bit-banging protocols, PWM generation, and timing-sensitive operations where precise delays are required.

WAITX blocks cog execution completely—no instructions execute and no interrupts are processed during the wait period. For long delays, consider using WAITCT instructions instead.

```pasm2
        WAITX   #99            ' Wait 101 clock cycles (2 + 99)
```



::: instrheader
## WAITXFI {#waitxfi}
Wait For Streamer Finished

[Events and Timing](#events-and-timing) - Waits for the streamer to finish all commands.
:::

**WAITXFI**  **{WC|WZ|WCZ}**

**Operation:** wait for XFI event then clear; `C/Z = timeout` (prior SETQ = CT timeout)

**Result:** Waits for a streamer-finished event to occur, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.
- The timeout is armed by a `SETQ` (a future System-Counter target) placed immediately before this instruction; the wait then releases on the event **or** the deadline, whichever comes first — C/Z = 1 if the timeout won, 0 if the event won. With **no** preceding `SETQ` no timeout is armed, so the event always wins and `WC` clears C, `WZ` clears Z and `WCZ` clears both (a valid one-instruction flag-clear).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000011011 | 000100100 | Timeout | Timeout | --- | 2+ |


**Related:** [WAITXMT](#waitxmt), [WAITXRL](#waitxrl), [WAITXRO](#waitxro), [XINIT](#xinit), [XCONT](#xcont)

**Explanation:**

WAITXFI waits for a streamer-finished event to occur, stalling the pipeline until the event flag is set. The streamer-finished event flag is set whenever the streamer runs out of commands to process.

The streamer-finished event flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXFI, WAITXFI, JXFI, or JNXFI instructions.



::: instrheader
## WAITXMT {#waitxmt}
Wait For Streamer Empty

[Events and Timing](#events-and-timing) - Waits for the streamer to be ready for a new command.
:::

**WAITXMT**  **{WC|WZ|WCZ}**

**Operation:** wait for XMT event then clear; `C/Z = timeout` (prior SETQ = CT timeout)

**Result:** Waits for a streamer-empty event to occur, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.
- The timeout is armed by a `SETQ` (a future System-Counter target) placed immediately before this instruction; the wait then releases on the event **or** the deadline, whichever comes first — C/Z = 1 if the timeout won, 0 if the event won. With **no** preceding `SETQ` no timeout is armed, so the event always wins and `WC` clears C, `WZ` clears Z and `WCZ` clears both (a valid one-instruction flag-clear).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000011010 | 000100100 | Timeout | Timeout | --- | 2+ |


**Related:** [WAITXFI](#waitxfi), [WAITXRL](#waitxrl), [WAITXRO](#waitxro), [XINIT](#xinit), [XCONT](#xcont)

**Explanation:**

WAITXMT waits for a streamer-empty event to occur, stalling the pipeline until the event flag is set. The streamer-empty event flag is set whenever the streamer is ready for a new command.

The streamer-empty event flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXMT, WAITXMT, JXMT, or JNXMT instructions.



::: instrheader
## WAITXRL {#waitxrl}
Wait For Streamer LUT Rollover

[Events and Timing](#events-and-timing) - Waits for the streamer LUT RAM rollover event.
:::

**WAITXRL**  **{WC|WZ|WCZ}**

**Operation:** wait for XRL event then clear; `C/Z = timeout` (prior SETQ = CT timeout)

**Result:** Waits for a streamer-LUT-RAM-rollover event to occur, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.
- The timeout is armed by a `SETQ` (a future System-Counter target) placed immediately before this instruction; the wait then releases on the event **or** the deadline, whichever comes first — C/Z = 1 if the timeout won, 0 if the event won. With **no** preceding `SETQ` no timeout is armed, so the event always wins and `WC` clears C, `WZ` clears Z and `WCZ` clears both (a valid one-instruction flag-clear).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000011101 | 000100100 | Timeout | Timeout | --- | 2+ |


**Related:** [WAITXFI](#waitxfi), [WAITXMT](#waitxmt), [WAITXRO](#waitxro), [POLLXRL](#pollxrl)

**Explanation:**

WAITXRL waits for a streamer-LUT-RAM-rollover event to occur, stalling the pipeline until the event flag is set. The streamer-LUT-RAM-rollover event flag is set whenever location $1FF of the Lookup RAM is read by the streamer.

The streamer-LUT-RAM-rollover event flag is cleared upon cog start or execution of POLLXRL, WAITXRL, JXRL, or JNXRL instructions.



::: instrheader
## WAITXRO {#waitxro}
Wait For Streamer NCO Rollover

[Events and Timing](#events-and-timing) - Waits for the streamer NCO rollover event.
:::

**WAITXRO**  **{WC|WZ|WCZ}**

**Operation:** wait for XRO event then clear; `C/Z = timeout` (prior SETQ = CT timeout)

**Result:** Waits for a streamer-NCO-rollover event to occur, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.
- The timeout is armed by a `SETQ` (a future System-Counter target) placed immediately before this instruction; the wait then releases on the event **or** the deadline, whichever comes first — C/Z = 1 if the timeout won, 0 if the event won. With **no** preceding `SETQ` no timeout is armed, so the event always wins and `WC` clears C, `WZ` clears Z and `WCZ` clears both (a valid one-instruction flag-clear).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000011100 | 000100100 | Timeout | Timeout | --- | 2+ |


**Related:** [WAITXFI](#waitxfi), [WAITXMT](#waitxmt), [WAITXRL](#waitxrl), [POLLXRO](#pollxro)

**Explanation:**

WAITXRO waits for a streamer-NCO-rollover event to occur, stalling the pipeline until the event flag is set. The streamer-NCO-rollover event flag is set whenever the streamer's numerically-controlled oscillator (NCO) rolls over.

The streamer-NCO-rollover event flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXRO, WAITXRO, JXRO, or JNXRO instructions.



::: instrheader
## WFBYTE {#wfbyte}
Write FIFO Byte

[Hub Memory Access](#hub-memory-access) - Writes a byte to the hub FIFO interface.
:::

**WFBYTE**  *{#}Dest*

**Result:** Writes the byte in Dest[7:0] into the FIFO. Must be used after WRFAST has configured the FIFO.

- Dest is the byte value to write (bits 7:0 used).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000010101 | --- | --- | --- | 2 |


**Related:** [WFWORD](#wfword), [WFLONG](#wflong), [WRFAST](#wrfast)

**Explanation:**

WFBYTE writes a byte from Dest[7:0] into the hub FIFO interface. This instruction must be used after WRFAST has configured the FIFO for fast hub memory writes.

Only the lower 8 bits of Dest are written. WFBYTE executes in 2 clock cycles.



::: instrheader
## WFLONG {#wflong}
Write FIFO Long

[Hub Memory Access](#hub-memory-access) - Writes a long to the hub FIFO interface.
:::

**WFLONG**  *{#}Dest*

**Result:** Writes the long in Dest[31:0] into the FIFO. Must be used after WRFAST has configured the FIFO.

- Dest is the long value to write (all 32 bits used).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000010111 | --- | --- | --- | 2 |


**Related:** [WFBYTE](#wfbyte), [WFWORD](#wfword), [WRFAST](#wrfast)

**Explanation:**

WFLONG writes a long (32-bit value) from Dest[31:0] into the hub FIFO interface. This instruction must be used after WRFAST has configured the FIFO for fast hub memory writes.

All 32 bits of Dest are written. WFLONG executes in 2 clock cycles.



::: instrheader
## WFWORD {#wfword}
Write FIFO Word

[Hub Memory Access](#hub-memory-access) - Writes a word to the hub FIFO interface.
:::

**WFWORD**  *{#}Dest*

**Result:** Writes the word in Dest[15:0] into the FIFO. Must be used after WRFAST has configured the FIFO.

- Dest is the word value to write (bits 15:0 used).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000010110 | --- | --- | --- | 2 |


**Related:** [WFBYTE](#wfbyte), [WFLONG](#wflong), [WRFAST](#wrfast)

**Explanation:**

WFWORD writes a word (16-bit value) from Dest[15:0] into the hub FIFO interface. This instruction must be used after WRFAST has configured the FIFO for fast hub memory writes.

Only the lower 16 bits of Dest are written. WFWORD executes in 2 clock cycles.



::: instrheader
## WMLONG {#wmlong}
Write Masked Long

[Hub Memory Access](#hub-memory-access) - Writes only non-zero bytes to hub RAM.
:::

**WMLONG**  *Dest, {#}Src/P*

**Operation:** write only non-$00 bytes of D to hub[S/PTRx] (prior SETQ/SETQ2 → block transfer)

**Result:** Writes only non-$00 bytes in Dest[31:0] to hub address Src/PTRx. Prior SETQ/SETQ2 invokes cog/LUT block transfer.

- Dest is the long value with bytes to write (non-zero bytes only).
- Src/P is the hub address or pointer (PTRA/PTRB).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010011 | 11I | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 3...10 † |

† **Timing varies by execution context:**

| Context | Clocks |
|:--------|:------:|
| Cog / LUT execution | 3...10 |
| Hub execution | 3...20 |


**Related:** [WRLONG](#wrlong), [WRBYTE](#wrbyte), [WRWORD](#wrword)

**Explanation:**

WMLONG writes only non-zero bytes from Dest to hub RAM at address Src. Each byte in Dest is examined: if the byte is $00, that byte position in hub RAM is not modified; if the byte is non-zero, it is written to hub RAM.

This masked write capability is useful for sprite graphics, text overlay, and other applications where selective pixel/byte updates are needed without affecting other data in the same long.

The access takes 1 more clock when it crosses a hub long.

Prior execution of SETQ or SETQ2 invokes cog or LUT block transfer mode.

[Rev C]{.silicon-note topic="SETQ block transfer: nothing between SETQ and the transfer"} When using SETQ/SETQ2 for block transfers with PTRx expressions, do NOT place any ALTx, AUGS, or AUGD instruction between SETQ/SETQ2 and WMLONG. Per the P2 Documentation, such an intervening instruction cancels the block-size PTRx delta: PTRx takes the plain expression's own step (+4 for `ptra++`, +12 for `ptra++[3]`) instead of the full block size. Keep the SETQ and the transfer adjacent.



::: instrheader
## WRBYTE {#wrbyte}
Write Byte

[Hub Memory Access](#hub-memory-access) - Writes a byte to hub RAM.
:::

**WRBYTE**  *{#}Dest, {#}Src/P*

**Result:** Writes the byte in Dest[7:0] to hub address Src/PTRx.

- Dest is the byte value to write (bits 7:0 used).
- Src/P is the hub address or pointer (PTRA/PTRB).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100010 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 3...10 † |

† **Timing varies by execution context:**

| Context | Clocks |
|:--------|:------:|
| Cog / LUT execution | 3...10 |
| Hub execution | 3...20 |


**Related:** [WRWORD](#wrword), [WRLONG](#wrlong), [RDBYTE](#rdbyte)

**Explanation:**

WRBYTE writes the byte in Dest[7:0] to hub RAM at address Src/PTRx. Only the lower 8 bits of Dest are written.

The instruction takes 3–10 cycles in cog/LUT execution, or 3–20 cycles in hub execution, depending on hub-window alignment. When Src specifies PTRA or PTRB, the pointer value is used as the hub address. Pointer auto-increment modes can be applied for sequential access.

```pasm2
        WRBYTE  value, ptra++  ' Write byte, increment pointer
```

[Rev C]{.silicon-note topic="No-wait RDFAST and the next hub instruction"} Started fewer than 16 clocks after a no-wait `RDFAST`, WRBYTE can complete before its write lands; if a hub read follows at once, the write is lost or that read returns the previous hub read's long instead. Nothing flags it. Use the waiting `RDFAST`, or start WRBYTE at least 16 clocks after it (see [RDFAST](#rdfast)).



::: instrheader
## WRC / WRNC / WRZ / WRNZ {#wrc}
Write Flag To Register

[Arithmetic Operations](#arithmetic-operations) - Writes 0 or 1 to register based on flag state.
:::

\hypertarget{wrnc}{}\hypertarget{wrz}{}\hypertarget{wrnz}{}

**WRC**  *Dest*\
**WRNC**  *Dest*\
**WRZ**  *Dest*\
**WRNZ**  *Dest*

**Operation:** `D = {31'b0, bit}` where bit = C (WRC) / !C (WRNC) / Z (WRZ) / !Z (WRNZ)

**Result:** Writes 0 or 1 to Dest based on the specified flag condition:

| Instruction | Dest value |
|-------------|------------|
| WRC | 1 if C == 1, else 0 |
| WRNC | 1 if C == 0, else 0 |
| WRZ | 1 if Z == 1, else 0 |
| WRNZ | 1 if Z == 0, else 0 |

- Dest is the destination register. Upper 31 bits are cleared to zero.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001101100 | --- | --- | D | 2 |
| EEEE | 1101011 | 000 | DDDDDDDDD | 001101101 | --- | --- | D | 2 |
| EEEE | 1101011 | 000 | DDDDDDDDD | 001101110 | --- | --- | D | 2 |
| EEEE | 1101011 | 000 | DDDDDDDDD | 001101111 | --- | --- | D | 2 |


**Explanation:**

These instructions copy flag states to a register, providing a convenient way to convert flag conditions into numeric values for computation or storage.

WRC and WRZ write the direct flag state (C or Z), while WRNC and WRNZ write the inverted flag state. The result is always 0 or 1; the upper 31 bits of Dest are cleared.



::: instrheader
## WRFAST {#wrfast}
Write FIFO Setup

[Hub Memory Access](#hub-memory-access) - Configures the hub FIFO for fast writes.
:::

**WRFAST**  *{#}Dest, {#}Src*

**Result:** Initializes the hub FIFO for fast writes. Dest[31] = no wait, Dest[13:0] = block size in 64-byte units (0 = max), Src[19:0] = block start address.

- Dest contains configuration: bit 31 = nowait, bits 13:0 = block size.
- Src contains hub RAM start address (bits 19:0).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100100 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 or WRFAST finish + 3 |


**Related:** [WFBYTE](#wfbyte), [WFWORD](#wfword), [WFLONG](#wflong), [RDFAST](#rdfast)

**Explanation:**

WRFAST configures the hub FIFO interface for fast streaming writes to hub RAM. After WRFAST executes, use WFBYTE, WFWORD, or WFLONG to write data through the FIFO.

Dest[13:0] specifies the block size in 64-byte units. A value of 0 selects the maximum block size. Dest[31] controls wait behavior: if clear, WRFAST waits for any previous WRFAST to finish and then reconfigures the FIFO interface; if set, WRFAST does not wait for the reconfiguration and takes only 2 clocks, so the code must allow enough clocks before the first FIFO write.

Src[19:0] specifies the starting hub RAM address. The FIFO automatically increments the address as data is written.

```pasm2
        WRFAST  #0, buffer_addr  ' Set up FIFO write to buffer
        WFLONG  data               ' Write data to FIFO
```



::: instrheader
## WRLONG {#wrlong}
Write Long

[Hub Memory Access](#hub-memory-access) - Writes a long to hub RAM.
:::

**WRLONG**  *{#}Dest, {#}Src/P*

**Operation:** write D long to hub[S/PTRx] (prior SETQ/SETQ2 → block transfer)

**Result:** Writes the long in Dest[31:0] to hub address Src/PTRx. Prior SETQ/SETQ2 invokes cog/LUT block transfer.

- Dest is the long value to write (all 32 bits used).
- Src/P is the hub address or pointer (PTRA/PTRB).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100011 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 3...10 † |

† **Timing varies by execution context:**

| Context | Clocks |
|:--------|:------:|
| Cog / LUT execution | 3...10 |
| Hub execution | 3...20 |


**Related:** [WRBYTE](#wrbyte), [WRWORD](#wrword), [WMLONG](#wmlong), [RDLONG](#rdlong)

**Explanation:**

WRLONG writes the 32-bit value in Dest to hub RAM at address Src/PTRx. All 32 bits of Dest are written.

The instruction takes 3–10 cycles in cog/LUT execution, or 3–20 cycles in hub execution, depending on hub-window alignment (minimum 3 cycles when the window is hit). The access takes 1 more clock when it crosses a hub long. When Src specifies PTRA or PTRB, the pointer value is used as the hub address. Pointer auto-increment modes can be applied for sequential access.

Prior execution of SETQ or SETQ2 invokes block transfer mode, writing multiple longs from cog or LUT RAM to hub RAM in a burst transfer. SETQ sets the count for a block transfer to or from cog RAM, while SETQ2 sets it for a block transfer to or from LUT RAM.

```pasm2
        SETQ    #16-1          ' Set up for 16-long block transfer
        WRLONG  buffer, ptra   ' Write 16 longs to hub
```

[Rev C]{.silicon-note topic="SETQ block transfer: nothing between SETQ and the transfer"} When using SETQ/SETQ2 for block transfers with PTRx expressions, do NOT place any ALTx, AUGS, or AUGD instruction between SETQ/SETQ2 and WRLONG. Such intervening instructions cancel the block-size PTRx delta calculation—the data transfers correctly, but PTRx takes the plain expression's own step (+4 for `ptra++`, +12 for `ptra++[3]`) instead of the full block size. Keep the SETQ and the transfer adjacent.

[Rev C]{.silicon-note topic="No-wait RDFAST and the next hub instruction"} Started fewer than 16 clocks after a no-wait `RDFAST`, WRLONG can complete before its write lands; if a hub read follows at once, the write is lost (the hub keeps its old long) or that read returns the previous hub read's long instead. Nothing flags it. Use the waiting `RDFAST`, or start WRLONG at least 16 clocks after it (see [RDFAST](#rdfast)).



::: instrheader
## WRLUT {#wrlut}
Write LUT

[Lookup Table](#lookup-table) - Writes a value to Lookup Table RAM.
:::

**WRLUT**  *{#}Dest, {#}Src/P*

**Result:** Writes Dest to LUT address Src/PTRx.

- Dest is the value to write.
- Src/P is the LUT address or pointer (PTRA/PTRB).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100001 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 |


**Related:** [RDLUT](#rdlut), [WRLONG](#wrlong), [SETQ](#setq)

**Explanation:**

WRLUT writes the value in Dest to the Lookup Table (LUT) at address Src/PTRx. The LUT is a 512-long (2KB) fast memory space.

**Pitfall:** A literal address (`WRLUT value, #addr`) reaches only LUT $000–$0FF (0–255); `#256` and above do not assemble (`Constant must be from 0 to 255`). Use a register, or a `PTRA`/`PTRB` pointer with an optional index, to reach any of the 512 LUT longs—the address field's top bit selects the pointer form, so a literal spans only 8 bits.

When Src specifies PTRA or PTRB, the pointer value is used as the LUT address. Only the lower 9 bits of the address are used (0-511).

WRLUT executes in 2 clock cycles, providing fast access to LUT RAM for lookup tables, buffers, and temporary storage.

```pasm2
        WRLUT   value, #100    ' Write to LUT address 100
```



::: instrheader
## WRPIN {#wrpin}
Write Pin Mode

[Pin I/O and Smart Pins](#pin-io-and-smart-pins) - Configures the operating mode of a smart pin.
:::

**WRPIN**  *{#}Dest, {#}Src*

**Result:** Sets the mode of smart pins Src[10:6]+Src[5:0]..Src[5:0] to Dest, acknowledges smart pins. Wraps within A/B pins. Prior SETQ overrides Src[10:6].

- Dest is the smart pin mode configuration.
- Src is the pin number or pin range.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100000 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 |


**Related:** [WXPIN](#wxpin), [WYPIN](#wypin), [RDPIN](#rdpin), [AKPIN](#akpin)

**Explanation:**

WRPIN configures the operating mode of one or more smart pins. Each of the P2's 64 pins has a dedicated smart pin module capable of autonomous operation for PWM, serial I/O, pulse measurement, ADC, and many other functions.

See Appendix F for the A/B input-selector (%AAAA/%BBBB) encodings.

A smart pin should be configured while its DIR bit is low, holding it in reset. A WRPIN issued while DIR is high changes the use of the pin's state bits without regulation and gives unpredictable behavior in the newly selected mode.

The standard configuration sequence is:
1. DIRL pin — Reset smart pin
2. WRPIN mode, pin — Configure smart pin mode
3. WXPIN x, pin — Set X parameter (setup)
4. DIRH pin — Enable smart pin
5. WYPIN y, pin — Set Y parameter (operate, after enable)

Write the Y parameter *after* raising DIRH. The trigger modes (pulse %00100, transition %00101) and the serial modes hold Y at 0 during reset, so a WYPIN issued before DIRH never takes effect; writing Y after enable is the one order that is correct for every mode.

WRPIN #0, pin clears all smart pin configuration.

```pasm2
        DIRL    #10            ' Reset pin 10
        WRPIN   pwm_mode, #10  ' Configure for PWM
        WXPIN   period, #10    ' Set period
        DIRH    #10            ' Enable
```



::: instrheader
## WRWORD {#wrword}
Write Word

[Hub Memory Access](#hub-memory-access) - Writes a word to hub RAM.
:::

**WRWORD**  *{#}Dest, {#}Src/P*

**Result:** Writes the word in Dest[15:0] to hub address Src/PTRx.

- Dest is the word value to write (bits 15:0 used).
- Src/P is the hub address or pointer (PTRA/PTRB).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100010 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 3...10 † |

† **Timing varies by execution context:**

| Context | Clocks |
|:--------|:------:|
| Cog / LUT execution | 3...10 |
| Hub execution | 3...20 |


**Related:** [WRBYTE](#wrbyte), [WRLONG](#wrlong), [RDWORD](#rdword)

**Explanation:**

WRWORD writes the word (16-bit value) in Dest[15:0] to hub RAM at address Src/PTRx. Only the lower 16 bits of Dest are written.

The instruction takes 3–10 cycles in cog/LUT execution, or 3–20 cycles in hub execution, depending on hub-window alignment. The access takes 1 more clock when it crosses a hub long. When Src specifies PTRA or PTRB, the pointer value is used as the hub address. Pointer auto-increment modes can be applied for sequential access.

[Rev C]{.silicon-note topic="No-wait RDFAST and the next hub instruction"} Started fewer than 16 clocks after a no-wait `RDFAST`, WRWORD can complete before its write lands; if a hub read follows at once, the write is lost or that read returns the previous hub read's long instead. Nothing flags it. Use the waiting `RDFAST`, or start WRWORD at least 16 clocks after it (see [RDFAST](#rdfast)).



::: instrheader
## WXPIN {#wxpin}
Write Pin X Parameter

[Pin I/O and Smart Pins](#pin-io-and-smart-pins) - Sets the X parameter of a smart pin.
:::

**WXPIN**  *{#}Dest, {#}Src*

**Result:** Sets the X register of smart pins Src[10:6]+Src[5:0]..Src[5:0] to Dest, acknowledges smart pins. Wraps within A/B pins. Prior SETQ overrides Src[10:6].

- Dest is the X parameter value.
- Src is the pin number or pin range.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100000 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 |


**Related:** [WRPIN](#wrpin), [WYPIN](#wypin), [RDPIN](#rdpin)

**Explanation:**

WXPIN sets the X parameter of one or more smart pins. The X register meaning depends on the smart pin mode:

- For PWM modes: X[15:0] sets the base period in clocks and X[31:16] sets the PWM frame period in base periods
- For serial modes: Controls bit timing and configuration
- For the counting and quadrature measurement modes: X[31:0] sets the measurement period in clocks (0 = continuous)
- For the timing-measurement modes (%10010 to %10111): X[31:0] is a count or a time, by mode: how many A-input highs/rises/edges to accumulate, how many clocks pass before a timeout without an A-input high/rise/edge, how many A-to-B periods to measure, or the minimum number of clock cycles to track periods for
- For pulse/cycle and transition output modes: X[15:0] sets the base period in clocks

Writing the X register also acknowledges the smart pin, clearing any completion flags.



::: instrheader
## WYPIN {#wypin}
Write Pin Y Parameter

[Pin I/O and Smart Pins](#pin-io-and-smart-pins) - Sets the Y parameter of a smart pin.
:::

**WYPIN**  *{#}Dest, {#}Src*

**Result:** Sets the Y register of smart pins Src[10:6]+Src[5:0]..Src[5:0] to Dest, acknowledges smart pins. Wraps within A/B pins. Prior SETQ overrides Src[10:6].

- Dest is the Y parameter value.
- Src is the pin number or pin range.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100001 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 |


**Related:** [WRPIN](#wrpin), [WXPIN](#wxpin), [RDPIN](#rdpin)

**Explanation:**

WYPIN sets the Y parameter of one or more smart pins. The Y register serves multiple purposes depending on smart pin mode:

- For PWM modes: Sets the output value, captured at the start of every PWM frame and compared against the frame counter — the duty. The base period and frame count come from WXPIN
- For the DAC modes: Y[15:0] is the DAC output value, captured at each sample period and held for its duration
- For the synchronous and asynchronous serial modes: Y is the output word to transmit; it goes into a single-stage buffer before advancing to the shifter
- For the USB mode: Y is the byte (or command value) written to the transmit buffer of the lower (even) pin
- For pulse/cycle and transition output modes: A non-zero value starts that many pulses or transitions
- For the edge- and high-counting modes (%01110, %01111): Y[0] selects counting A only (0) or incrementing on A and decrementing on B (1)
- For ADC modes other than SINC2 sampling: Y[13:0] replaces the sample period set by WXPIN

Writing the Y register also acknowledges pin completion, clearing any completion flags. Writing Y both supplies new data and acknowledges the previous result.

```pasm2
        WYPIN   pwm_value, #10  ' Set PWM duty and acknowledge
```


