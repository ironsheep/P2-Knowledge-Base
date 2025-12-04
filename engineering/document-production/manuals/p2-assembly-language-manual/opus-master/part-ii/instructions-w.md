# Instructions: W

This section contains all PASM2 instructions beginning with the letter W.



## WAITATN {#waitatn}

Wait for attention

[Event](#event) - Wait for attention event from another cog.

**WAITATN**  **{WC|WZ|WCZ}**

---

**Result:** Waits for an attention event to occur (unless the event flag is already set), then clears the event flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000011110 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [COGATN](instructions-c.md#cogatn), [POLLATN](instructions-p.md#pollatn), [JATN](instructions-j.md#jatn), [JNATN](instructions-j.md#jnatn)

**Explanation:**

WAITATN waits for an attention event to occur, stalling the pipeline until the event flag is set. The attention event flag is set whenever another cog issues an attention request for this cog using COGATN. The flag is cleared upon cog start or execution of POLLATN, WAITATN, JATN, or JNATN instructions.

To set an optional timeout, insert a SETQ instruction (with a future System Counter target value) immediately before WAITATN. The WC, WZ, or WCZ effect is recommended only when timeout is specified. Flags are set (1) if timeout occurred before the event, or cleared (0) if the event occurred before timeout.

During a wait, the pipeline is stalled—no instructions execute and no interrupts are processed in the cog until the wait condition ends.

::: pasm2
        WAITATN                ' Wait for attention from another cog
:::



## WAITCT1 / WAITCT2 / WAITCT3 {#waitct1}

Wait for counter event {#waitct2} {#waitct3}

[Event](#event) - Wait for counter event 1, 2, or 3 flag.

**WAITCT1**  **{WC|WZ|WCZ}**
**WAITCT2**  **{WC|WZ|WCZ}**
**WAITCT3**  **{WC|WZ|WCZ}**

---

**Result:** Waits for the specified counter event flag (CT1, CT2, or CT3) to be set, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000010001 | 000100100 | --- | Timeout | Timeout | 2+ |
| EEEE | 1101011 | CZ0 | 000010010 | 000100100 | --- | Timeout | Timeout | 2+ |
| EEEE | 1101011 | CZ0 | 000010011 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [ADDCT1](instructions-a.md#addct1), [ADDCT2](#addct2), [ADDCT3](#addct3), [POLLCT1](instructions-p.md#pollct1), [POLLCT2](#pollct2), [POLLCT3](#pollct3), [JCT1](instructions-j.md#jct1), [JCT2](#jct2), [JCT3](#jct3)

**Explanation:**

WAITCT1, WAITCT2, and WAITCT3 wait for counter events 1, 2, or 3 respectively, stalling the pipeline until the corresponding event flag is set. Each counter event flag is set whenever the System Counter (CT) passes the value in the corresponding event trigger register (CT1, CT2, or CT3).

The flags are cleared by execution of ADDCT*n*, POLLCT*n*, WAITCT*n*, JCT*n*, or JNCT*n* instructions (where *n* is 1, 2, or 3).

To set an optional timeout, insert a SETQ instruction immediately before the WAITCTn instruction.



## WAITFBW {#waitfbw}

Wait for FIFO block wrap

[Event](#event) - Wait for FIFO-interface-block-wrap event.

**WAITFBW**  **{WC|WZ|WCZ}**

---

**Result:** Waits for a FIFO-interface-block-wrap event to occur, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000011001 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [RDFAST](instructions-r.md#rdfast), [WRFAST](#wrfast), [FBLOCK](instructions-f.md#fblock), [POLLFBW](instructions-p.md#pollfbw)

**Explanation:**

WAITFBW waits for a FIFO-interface-block-wrap event to occur, stalling the pipeline until the event flag is set. The FIFO-interface-block-wrap event flag is set whenever the Hub RAM FIFO interface exhausts its block count and reloads its block count and start address.

The FIFO-interface-block-wrap event flag is cleared upon execution of RDFAST, WRFAST, FBLOCK, POLLFBW, WAITFBW, JFBW, or JNFBW instructions.



## WAITINT {#waitint}

Wait for interrupt

[Event](#event) - Wait for interrupt-occurred event.

**WAITINT**  **{WC|WZ|WCZ}**

---

**Result:** Waits for an interrupt-occurred event, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000010000 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [POLLINT](instructions-p.md#pollint), [JINT](instructions-j.md#jint), [JNINT](instructions-j.md#jnint)

**Explanation:**

WAITINT waits for an interrupt-occurred event to occur, stalling the pipeline until the event flag is set. The interrupt-occurred event flag is set whenever interrupt 1, 2, or 3 occurs—debug interrupts are ignored.

The interrupt-occurred event flag is cleared upon cog start or execution of POLLINT, WAITINT, JINT, or JNINT instructions.



## WAITPAT {#waitpat}

Wait for pattern

[Event](#event) - Wait for pin-pattern-detected event.

**WAITPAT**  **{WC|WZ|WCZ}**

---

**Result:** Waits for a pin-pattern-detected event, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000011000 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [SETPAT](instructions-s.md#setpat), [POLLPAT](instructions-p.md#pollpat), [JPAT](instructions-j.md#jpat), [JNPAT](instructions-j.md#jnpat)

**Explanation:**

WAITPAT waits for a pin-pattern-detected event to occur, stalling the pipeline until the event flag is set. The pin-pattern-detected event flag is set whenever the masked input pins match or don't match the pattern described by a previous SETPAT instruction.

The pin-pattern-detected event flag is cleared upon execution of SETPAT, POLLPAT, WAITPAT, JPAT, or JNPAT instructions.

::: pasm2
        SETPAT  mask, pattern  ' Set up pattern detector
        WAITPAT                ' Wait for pattern match
:::



## WAITSE1 / WAITSE2 / WAITSE3 / WAITSE4 {#waitse1}

Wait for selectable event (1, 2, 3, or 4) {#waitse2} {#waitse3} {#waitse4}

[Event](#event) - Wait for selectable event flag.

**WAITSE1**  **{WC|WZ|WCZ}**
**WAITSE2**  **{WC|WZ|WCZ}**
**WAITSE3**  **{WC|WZ|WCZ}**
**WAITSE4**  **{WC|WZ|WCZ}**

---

**Result:** Waits for the specified selectable event flag (SE1-SE4) to be set, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000010100 | 000100100 | --- | Timeout | Timeout | 2+ |
| EEEE | 1101011 | CZ0 | 000010101 | 000100100 | --- | Timeout | Timeout | 2+ |
| EEEE | 1101011 | CZ0 | 000010110 | 000100100 | --- | Timeout | Timeout | 2+ |
| EEEE | 1101011 | CZ0 | 000010111 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [SETSE1/2/3/4](instructions-s.md#setse1), [POLLSE1/2/3/4](instructions-p.md#pollse1), [JSE1/2/3/4](instructions-j.md#jse1), [JNSE1/2/3/4](instructions-j.md#jnse1)

**Explanation:**

WAITSE1, WAITSE2, WAITSE3, and WAITSE4 wait for their respective selectable events to occur, stalling the pipeline until the corresponding SE flag is set.

Each selectable event flag is cleared by execution of its respective SETSEn, POLLSEn, WAITSEn, JSEn, or JNSEn instruction.



## WAITX {#waitx}

Wait cycles

[Event](#event) - Wait for Dest+1 clock cycles.

**WAITX**  *{#}Dest*  **{WC|WZ|WCZ}**

---

**Result:** Stalls the cog for Dest+1 clock cycles, providing precise timing delays. Sets C and Z to 0 after completion.

- Dest is the number of cycles minus 1 to wait (0-511 for immediate).
- WC, WZ, or WCZ are optional; always set to 0 after completion.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 000011111 | --- | 0 | 0 | 2 + D |


**Related:** [WAITCT1](#waitct1), [WAITCT2](#waitct2), [WAITCT3](#waitct3)

**Explanation:**

WAITX stalls the cog for precise timing delays. The actual wait time is Dest+1 cycles minimum. This instruction is critical for bit-banging protocols, PWM generation, and timing-sensitive operations where precise delays are required.

WAITX blocks cog execution completely—no instructions execute and no interrupts are processed during the wait period. For long delays, consider using WAITCT instructions instead.

::: pasm2
        WAITX   #99            ' Wait 100 clock cycles
:::



## WAITXFI {#waitxfi}

Wait for streamer finished

[Event](#event) - Wait for streamer-finished event.

**WAITXFI**  **{WC|WZ|WCZ}**

---

**Result:** Waits for a streamer-finished event to occur, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000011011 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [WAITXMT](#waitxmt), [WAITXRL](#waitxrl), [WAITXRO](#waitxro), [XINIT](instructions-x.md#xinit), [XCONT](instructions-x.md#xcont)

**Explanation:**

WAITXFI waits for a streamer-finished event to occur, stalling the pipeline until the event flag is set. The streamer-finished event flag is set whenever the streamer runs out of commands to process.

The streamer-finished event flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXFI, WAITXFI, JXFI, or JNXFI instructions.



## WAITXMT {#waitxmt}

Wait for streamer empty

[Event](#event) - Wait for streamer-empty event.

**WAITXMT**  **{WC|WZ|WCZ}**

---

**Result:** Waits for a streamer-empty event to occur, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000011010 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [WAITXFI](#waitxfi), [WAITXRL](#waitxrl), [WAITXRO](#waitxro), [XINIT](instructions-x.md#xinit), [XCONT](instructions-x.md#xcont)

**Explanation:**

WAITXMT waits for a streamer-empty event to occur, stalling the pipeline until the event flag is set. The streamer-empty event flag is set whenever the streamer is ready for a new command.

The streamer-empty event flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXMT, WAITXMT, JXMT, or JNXMT instructions.



## WAITXRL {#waitxrl}

Wait for streamer LUT rollover

[Event](#event) - Wait for streamer-LUT-RAM-rollover event.

**WAITXRL**  **{WC|WZ|WCZ}**

---

**Result:** Waits for a streamer-LUT-RAM-rollover event to occur, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000011101 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [WAITXFI](#waitxfi), [WAITXMT](#waitxmt), [WAITXRO](#waitxro), [POLLXRL](instructions-p.md#pollxrl)

**Explanation:**

WAITXRL waits for a streamer-LUT-RAM-rollover event to occur, stalling the pipeline until the event flag is set. The streamer-LUT-RAM-rollover event flag is set whenever location $1FF of the Lookup RAM is read by the streamer.

The streamer-LUT-RAM-rollover event flag is cleared upon cog start or execution of POLLXRL, WAITXRL, JXRL, or JNXRL instructions.



## WAITXRO {#waitxro}

Wait for streamer NCO rollover

[Event](#event) - Wait for streamer-NCO-rollover event.

**WAITXRO**  **{WC|WZ|WCZ}**

---

**Result:** Waits for a streamer-NCO-rollover event to occur, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000011100 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [WAITXFI](#waitxfi), [WAITXMT](#waitxmt), [WAITXRL](#waitxrl), [POLLXRO](instructions-p.md#pollxro)

**Explanation:**

WAITXRO waits for a streamer-NCO-rollover event to occur, stalling the pipeline until the event flag is set. The streamer-NCO-rollover event flag is set whenever the streamer's numerically-controlled oscillator (NCO) rolls over.

The streamer-NCO-rollover event flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXRO, WAITXRO, JXRO, or JNXRO instructions.



## WFBYTE {#wfbyte}

Write FIFO byte

[Hub FIFO](#hub-fifo) - Write byte to FIFO.

**WFBYTE**  *{#}Dest*

---

**Result:** Writes the byte in Dest[7:0] into the FIFO. Must be used after WRFAST has configured the FIFO.

- Dest is the byte value to write (bits 7:0 used).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000010101 | --- | --- | --- | 2 |


**Related:** [WFWORD](#wfword), [WFLONG](#wflong), [WRFAST](#wrfast)

**Explanation:**

WFBYTE writes a byte from Dest[7:0] into the Hub FIFO interface. This instruction must be used after WRFAST has configured the FIFO for fast Hub memory writes.

Only the lower 8 bits of Dest are written. WFBYTE executes in 2 clock cycles when the FIFO is ready. If the FIFO is full, execution stalls until space becomes available.



## WFLONG {#wflong}

Write FIFO long

[Hub FIFO](#hub-fifo) - Write long to FIFO.

**WFLONG**  *{#}Dest*

---

**Result:** Writes the long in Dest[31:0] into the FIFO. Must be used after WRFAST has configured the FIFO.

- Dest is the long value to write (all 32 bits used).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000010111 | --- | --- | --- | 2 |


**Related:** [WFBYTE](#wfbyte), [WFWORD](#wfword), [WRFAST](#wrfast)

**Explanation:**

WFLONG writes a long (32-bit value) from Dest[31:0] into the Hub FIFO interface. This instruction must be used after WRFAST has configured the FIFO for fast Hub memory writes.

All 32 bits of Dest are written. WFLONG executes in 2 clock cycles when the FIFO is ready. If the FIFO is full, execution stalls until space becomes available.



## WFWORD {#wfword}

Write FIFO word

[Hub FIFO](#hub-fifo) - Write word to FIFO.

**WFWORD**  *{#}Dest*

---

**Result:** Writes the word in Dest[15:0] into the FIFO. Must be used after WRFAST has configured the FIFO.

- Dest is the word value to write (bits 15:0 used).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000010110 | --- | --- | --- | 2 |


**Related:** [WFBYTE](#wfbyte), [WFLONG](#wflong), [WRFAST](#wrfast)

**Explanation:**

WFWORD writes a word (16-bit value) from Dest[15:0] into the Hub FIFO interface. This instruction must be used after WRFAST has configured the FIFO for fast Hub memory writes.

Only the lower 16 bits of Dest are written. WFWORD executes in 2 clock cycles when the FIFO is ready. If the FIFO is full, execution stalls until space becomes available.



## WMLONG {#wmlong}

Write masked long

[Hub RAM](#hub-ram) - Write masked long to hub RAM (non-zero bytes only).

**WMLONG**  *Dest, {#}Src/P*

---

**Result:** Writes only non-$00 bytes in Dest[31:0] to hub address Src/PTRx. Prior SETQ/SETQ2 invokes cog/LUT block transfer.

- Dest is the long value with bytes to write (non-zero bytes only).
- Src/P is the hub address or pointer (PTRA/PTRB).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010011 | 11I | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 3...10 |


**Related:** [WRLONG](#wrlong), [WRBYTE](#wrbyte), [WRWORD](#wrword)

**Explanation:**

WMLONG writes only non-zero bytes from Dest to Hub RAM at address Src. Each byte in Dest is examined: if the byte is $00, that byte position in Hub RAM is not modified; if the byte is non-zero, it is written to Hub RAM.

This masked write capability is useful for sprite graphics, text overlay, and other applications where selective pixel/byte updates are needed without affecting other data in the same long.

Prior execution of SETQ or SETQ2 invokes cog or LUT block transfer mode.



## WRBYTE {#wrbyte}

Write byte

[Hub RAM](#hub-ram) - Write byte to hub RAM.

**WRBYTE**  *{#}Dest, {#}Src/P*

---

**Result:** Writes the byte in Dest[7:0] to hub address Src/PTRx.

- Dest is the byte value to write (bits 7:0 used).
- Src/P is the hub address or pointer (PTRA/PTRB).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100010 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 3...10 |


**Related:** [WRWORD](#wrword), [WRLONG](#wrlong), [RDBYTE](instructions-r.md#rdbyte)

**Explanation:**

WRBYTE writes the byte in Dest[7:0] to Hub RAM at address Src/PTRx. Only the lower 8 bits of Dest are written.

The instruction takes 3 to 10 clock cycles depending on Hub RAM timing. When Src specifies PTRA or PTRB, the pointer value is used as the Hub address. Pointer auto-increment modes can be applied for sequential access.

::: pasm2
        WRBYTE  value, ptra++  ' Write byte, increment pointer
:::



## WRC / WRNC / WRZ / WRNZ {#wrc}

Write flag to register {#wrnc} {#wrz} {#wrnz}

[Math and Logic](#math-and-logic) - Write C, NC, Z, or NZ flag value to register.

**WRC**  *Dest*
**WRNC**  *Dest*
**WRZ**  *Dest*
**WRNZ**  *Dest*

---

**Result:** Writes 0 or 1 to Dest based on the specified flag condition:

| Instruction | Dest value |
|-------------|------------|
| WRC | 1 if C=1, else 0 |
| WRNC | 1 if C=0, else 0 |
| WRZ | 1 if Z=1, else 0 |
| WRNZ | 1 if Z=0, else 0 |

- Dest is the destination register. Upper 31 bits are cleared to zero.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001101100 | D | --- | --- | 2 |
| EEEE | 1101011 | 000 | DDDDDDDDD | 001101101 | D | --- | --- | 2 |
| EEEE | 1101011 | 000 | DDDDDDDDD | 001101110 | D | --- | --- | 2 |
| EEEE | 1101011 | 000 | DDDDDDDDD | 001101111 | D | --- | --- | 2 |


**Explanation:**

These instructions copy flag states to a register, providing a convenient way to convert flag conditions into numeric values for computation or storage.

WRC and WRZ write the direct flag state (C or Z), while WRNC and WRNZ write the inverted flag state. The result is always 0 or 1; the upper 31 bits of Dest are cleared.



## WRFAST {#wrfast}

Write FIFO setup

[Hub FIFO](#hub-fifo) - Begin new fast hub write via FIFO.

**WRFAST**  *{#}Dest, {#}Src*

---

**Result:** Initializes the Hub FIFO for fast writes. Dest[31] = no wait, Dest[13:0] = block size in 64-byte units (0 = max), Src[19:0] = block start address.

- Dest contains configuration: bit 31 = nowait, bits 13:0 = block size.
- Src contains Hub RAM start address (bits 19:0).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100100 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 or WRFAST finish + 3 |


**Related:** [WFBYTE](#wfbyte), [WFWORD](#wfword), [WFLONG](#wflong), [RDFAST](instructions-r.md#rdfast)

**Explanation:**

WRFAST configures the Hub FIFO interface for fast streaming writes to Hub RAM. After WRFAST executes, use WFBYTE, WFWORD, or WFLONG to write data through the FIFO.

Dest[13:0] specifies the block size in 64-byte units. A value of 0 selects the maximum block size. Dest[31] controls wait behavior: if set, FIFO writes proceed without stalling.

Src[19:0] specifies the starting Hub RAM address. The FIFO automatically increments the address as data is written.

::: pasm2
        WRFAST  #0, buffer_addr  ' Set up FIFO write to buffer
        WFLONG  data               ' Write data to FIFO
:::



## WRLONG {#wrlong}

Write long

[Hub RAM](#hub-ram) - Write long to hub RAM.

**WRLONG**  *{#}Dest, {#}Src/P*

---

**Result:** Writes the long in Dest[31:0] to hub address Src/PTRx. Prior SETQ/SETQ2 invokes cog/LUT block transfer.

- Dest is the long value to write (all 32 bits used).
- Src/P is the hub address or pointer (PTRA/PTRB).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100011 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 3...10 |


**Related:** [WRBYTE](#wrbyte), [WRWORD](#wrword), [WMLONG](#wmlong), [RDLONG](instructions-r.md#rdlong)

**Explanation:**

WRLONG writes the 32-bit value in Dest to Hub RAM at address Src/PTRx. All 32 bits of Dest are written.

The instruction takes 3 to 10 clock cycles depending on Hub RAM timing. When Src specifies PTRA or PTRB, the pointer value is used as the Hub address. Pointer auto-increment modes can be applied for sequential access.

Prior execution of SETQ or SETQ2 invokes block transfer mode, writing multiple longs from cog or LUT RAM to Hub RAM in a burst transfer.

::: pasm2
        SETQ    #16-1          ' Set up for 16-long block transfer
        WRLONG  buffer, ptra   ' Write 16 longs to hub
:::



## WRLUT {#wrlut}

Write LUT

[Lookup Table](#lookup-table) - Write Dest to LUT address.

**WRLUT**  *{#}Dest, {#}Src/P*

---

**Result:** Writes Dest to LUT address Src/PTRx.

- Dest is the value to write.
- Src/P is the LUT address or pointer (PTRA/PTRB).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100001 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 |


**Related:** [RDLUT](instructions-r.md#rdlut), [WRLONG](#wrlong), [SETQ](instructions-s.md#setq)

**Explanation:**

WRLUT writes the value in Dest to the Lookup Table (LUT) at address Src/PTRx. The LUT is a 512-long (2KB) fast memory space.

When Src specifies PTRA or PTRB, the pointer value is used as the LUT address. Only the lower 9 bits of the address are used (0-511).

WRLUT executes in 2 clock cycles, providing fast access to LUT RAM for lookup tables, buffers, and temporary storage.

::: pasm2
        WRLUT   value, #100    ' Write to LUT address 100
:::



## WRPIN {#wrpin}

Write pin mode

[Smart Pin](#smart-pin) - Configure smart pin mode.

**WRPIN**  *{#}Dest, {#}Src*

---

**Result:** Sets the mode of smart pins Src[10:6]+Src[5:0]..Src[5:0] to Dest, acknowledges smart pins. Wraps within A/B pins. Prior SETQ overrides Src[10:6].

- Dest is the smart pin mode configuration.
- Src is the pin number or pin range.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100000 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 |


**Related:** [WXPIN](#wxpin), [WYPIN](#wypin), [RDPIN](instructions-r.md#rdpin), [AKPIN](instructions-a.md#akpin)

**Explanation:**

WRPIN configures the operating mode of one or more Smart Pins. Each of the P2's 64 pins has a dedicated Smart Pin module capable of autonomous operation for PWM, serial I/O, pulse measurement, ADC, and many other functions.

**CRITICAL REQUIREMENT**: Smart pins MUST be reset (DIR=0) before configuring with WRPIN.

The standard configuration sequence is:
1. DIRL pin — Reset smart pin (required)
2. WRPIN mode, pin — Configure smart pin mode
3. WXPIN x, pin — Set X parameter
4. WYPIN y, pin — Set Y parameter
5. DIRH pin — Enable smart pin

WRPIN #0, pin clears all smart pin configuration.

::: pasm2
        DIRL    #10            ' Reset pin 10
        WRPIN   pwm_mode, #10  ' Configure for PWM
        WXPIN   period, #10    ' Set period
        DIRH    #10            ' Enable
:::



## WRWORD {#wrword}

Write word

[Hub RAM](#hub-ram) - Write word to hub RAM.

**WRWORD**  *{#}Dest, {#}Src/P*

---

**Result:** Writes the word in Dest[15:0] to hub address Src/PTRx.

- Dest is the word value to write (bits 15:0 used).
- Src/P is the hub address or pointer (PTRA/PTRB).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100010 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 3...10 |


**Related:** [WRBYTE](#wrbyte), [WRLONG](#wrlong), [RDWORD](instructions-r.md#rdword)

**Explanation:**

WRWORD writes the word (16-bit value) in Dest[15:0] to Hub RAM at address Src/PTRx. Only the lower 16 bits of Dest are written.

The instruction takes 3 to 10 clock cycles depending on Hub RAM timing. When Src specifies PTRA or PTRB, the pointer value is used as the Hub address. Pointer auto-increment modes can be applied for sequential access.



## WXPIN {#wxpin}

Write pin X parameter

[Smart Pin](#smart-pin) - Set smart pin X parameter.

**WXPIN**  *{#}Dest, {#}Src*

---

**Result:** Sets the X register of smart pins Src[10:6]+Src[5:0]..Src[5:0] to Dest, acknowledges smart pins. Wraps within A/B pins. Prior SETQ overrides Src[10:6].

- Dest is the X parameter value.
- Src is the pin number or pin range.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100000 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 |


**Related:** [WRPIN](#wrpin), [WYPIN](#wypin), [RDPIN](instructions-r.md#rdpin)

**Explanation:**

WXPIN sets the X parameter of one or more Smart Pins. The X register meaning depends on the smart pin mode:

- For PWM modes: Sets frame period or duty cycle parameter
- For serial modes: Controls bit timing and configuration
- For pulse measurement: Sets measurement parameters
- For transition modes: Controls timebase

Writing the X register also acknowledges the smart pin, clearing any completion flags.



## WYPIN {#wypin}

Write pin Y parameter

[Smart Pin](#smart-pin) - Set smart pin Y parameter.

**WYPIN**  *{#}Dest, {#}Src*

---

**Result:** Sets the Y register of smart pins Src[10:6]+Src[5:0]..Src[5:0] to Dest, acknowledges smart pins. Wraps within A/B pins. Prior SETQ overrides Src[10:6].

- Dest is the Y parameter value.
- Src is the pin number or pin range.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100001 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 |


**Related:** [WRPIN](#wrpin), [WXPIN](#wxpin), [RDPIN](instructions-r.md#rdpin)

**Explanation:**

WYPIN sets the Y parameter of one or more Smart Pins. The Y register serves multiple purposes depending on smart pin mode:

- For PWM modes: Sets the base period
- For SPI/serial modes: Controls data to transmit
- For counter modes: Sets count value
- For ADC modes: Initiates conversions

Writing the Y register also acknowledges pin completion, clearing any completion flags. This dual purpose makes WYPIN essential for continuous smart pin operation—it both provides new data and signals that previous results have been processed.

::: pasm2
        WYPIN   pwm_value, #10  ' Set PWM duty and acknowledge
:::

