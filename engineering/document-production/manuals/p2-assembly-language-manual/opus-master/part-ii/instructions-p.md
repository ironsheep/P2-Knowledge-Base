<!-- PASM2 Instruction Reference - P Instructions -->
<!-- Generated from YAML knowledge base -->
<!-- Source: /workspaces/P2-Knowledge-Base/engineering/knowledge-base/P2/language/pasm2/ -->

# P Instructions

This section covers all PASM2 instructions beginning with the letter P, organized by instruction family.

## POLL Instructions — Event Polling

The POLL family of instructions checks event status without waiting. Each POLL instruction copies the state of its corresponding event flag into the C and/or Z flags (when WC, WZ, or WCZ effects are specified) and then clears the event flag. These instructions enable non-blocking event-driven programming by allowing the cog to check for events and continue execution without suspending.

### POLLATN — Event

Checks the attention event flag without waiting.

#### Syntax
```pasm
        POLLATN {WC|WZ|WCZ}
```

#### Result
Attention event flag is optionally copied into C and/or Z, then it is cleared.

#### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional flag effects to capture event state |

#### Encoding
\simpleencoding{EEEE | 1101011 | CZ0 | 000001110 | 000100100 | — | ATN Event | ATN Event | 2}

#### Related Instructions
- [COGATN](#cogatn) — Send attention request to another cog
- [WAITATN](#waitatn) — Wait for attention event
- [JATN](#jatn) — Jump if attention event occurred
- [JNATN](#jnatn) — Jump if attention event did not occur

#### Explanation
POLLATN copies the state of the attention event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the attention event flag prior to clearing it.

The attention event flag is set whenever another cog issues an attention request for this cog. The attention event flag is cleared upon cog start, or execution of POLLATN, WAITATN, JATN, or JNATN instructions.

This instruction enables inter-cog communication by allowing a cog to check whether another cog has requested its attention without blocking execution.

---

### POLLCT1 / POLLCT2 / POLLCT3 — Event {#pollct1}

Checks the counter event flag (1, 2, or 3) without waiting.

#### Syntax
```pasm
        POLLCT1 {WC|WZ|WCZ}
        POLLCT2 {WC|WZ|WCZ}
        POLLCT3 {WC|WZ|WCZ}
```

#### Result
CTn event flag state is optionally copied into C and/or Z, then the flag is cleared.

#### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional flag effects to capture event state |

#### Encoding
| Instruction | Encoding |
|-------------|----------|
| POLLCT1 | `EEEE 1101011 CZ0 000000001 000100100` |
| POLLCT2 | `EEEE 1101011 CZ0 000000010 000100100` |
| POLLCT3 | `EEEE 1101011 CZ0 000000011 000100100` |

**Clocks:** 2

#### Related Instructions
- [ADDCT1/2/3](#addct1) — Add to CTn event trigger
- [WAITCT1/2/3](#waitct1) — Wait for CTn event
- [JCT1/2/3](#jct1) — Jump if CTn event occurred
- [JNCT1/2/3](#jnct1) — Jump if CTn event did not occur

#### Explanation
POLLCT1, POLLCT2, and POLLCT3 copy the state of their respective counter event flags into C and/or Z and then clear the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the counter event flag prior to clearing it.

Each counter event flag is set whenever the System Counter (CT) passes the value in that counter's event trigger register; that is, the MSB of (CT - CTn) is 0. The counter event flag is cleared upon execution of ADDCTn, POLLCTn, WAITCTn, JCTn, or JNCTn.

These instructions enable time-based event polling without blocking execution. The P2 provides three independent counter event triggers (CT1, CT2, CT3) allowing a cog to simultaneously track multiple timing requirements such as watchdog timers, periodic tasks, and timeout detection.

---

### POLLFBW — Event

Checks the FIFO-interface-block-wrap event flag without waiting.

#### Syntax
```pasm
        POLLFBW {WC|WZ|WCZ}
```

#### Result
FIFO-interface-block-wrap event flag is optionally copied into C and/or Z, then it is cleared.

#### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional flag effects to capture event state |

#### Encoding
\simpleencoding{EEEE | 1101011 | CZ0 | 000001001 | 000100100 | — | FBW Event | FBW Event | 2}

#### Related Instructions
- [RDFAST](#rdfast) — Start FIFO read operation
- [WRFAST](#wrfast) — Start FIFO write operation
- [FBLOCK](#fblock) — Set FIFO block parameters
- [WAITFBW](#waitfbw) — Wait for FIFO block wrap
- [JFBW](#jfbw) — Jump if FIFO block wrap occurred
- [JNFBW](#jnfbw) — Jump if FIFO block wrap did not occur

#### Explanation
POLLFBW copies the state of the FIFO-interface-block-wrap event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the FIFO-interface-block-wrap event flag prior to clearing it.

The FIFO-interface-block-wrap event flag is set whenever the Hub RAM FIFO interface exhausts its block count and reloads its block count and start address. The flag is cleared upon execution of RDFAST, WRFAST, FBLOCK, POLLFBW, WAITFBW, JFBW, or JNFBW instructions.

This instruction enables circular buffer management for high-speed Hub RAM transfers. When the FIFO interface completes a block, the event signals that the buffer has wrapped and is ready for the next iteration.

---

### POLLINT — Event

Checks the interrupt-occurred event flag without waiting.

#### Syntax
```pasm
        POLLINT {WC|WZ|WCZ}
```

#### Result
Interrupt-occurred event flag is optionally copied into C and/or Z, then it is cleared.

#### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional flag effects to capture event state |

#### Encoding
\simpleencoding{EEEE | 1101011 | CZ0 | 000000000 | 000100100 | — | INT Event | INT Event | 2}

#### Related Instructions
- [WAITINT](#waitint) — Wait for interrupt event
- [JINT](#jint) — Jump if interrupt occurred
- [JNINT](#jnint) — Jump if interrupt did not occur

#### Explanation
POLLINT copies the state of the interrupt-occurred event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the interrupt-occurred event flag prior to clearing it.

The interrupt-occurred event flag is set whenever interrupt 1, 2, or 3 occurs. Debug interrupts are ignored. The flag is cleared upon cog start, or execution of POLLINT, WAITINT, JINT, or JNINT instructions.

This instruction enables non-blocking interrupt handling. The cog can check for interrupts and respond appropriately without suspending execution in a wait loop.

---

### POLLPAT — Event

Checks the pin-pattern-detected event flag without waiting.

#### Syntax
```pasm
        POLLPAT {WC|WZ|WCZ}
```

#### Result
Pin-pattern-detected event flag is optionally copied into C and/or Z, then it is cleared.

#### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional flag effects to capture event state |

#### Encoding
\simpleencoding{EEEE | 1101011 | CZ0 | 000001000 | 000100100 | — | PAT Event | PAT Event | 2}

#### Related Instructions
- [SETPAT](#setpat) — Configure pin pattern detection
- [WAITPAT](#waitpat) — Wait for pin pattern match
- [JPAT](#jpat) — Jump if pattern matched
- [JNPAT](#jnpat) — Jump if pattern did not match

#### Explanation
POLLPAT copies the state of the pin-pattern-detected event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the pin-pattern-detected event flag prior to clearing it.

The pin-pattern-detected event flag is set whenever the masked input pins match or don't match the pattern described by a previous SETPAT instruction. The flag is cleared upon execution of SETPAT, POLLPAT, WAITPAT, JPAT, or JNPAT instructions.

This instruction enables non-blocking pattern detection on input pins. The cog can monitor for specific pin states or changes without blocking, allowing it to perform other work while waiting for external signals.

---

### POLLQMT — Event

Checks the CORDIC-read-but-empty event flag without waiting.

#### Syntax
```pasm
        POLLQMT {WC|WZ|WCZ}
```

#### Result
CORDIC-read-but-empty event flag is optionally copied into C and/or Z, then it is cleared.

#### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional flag effects to capture event state |

#### Encoding
\simpleencoding{EEEE | 1101011 | CZ0 | 000001111 | 000100100 | — | QMT Event | QMT Event | 2}

#### Related Instructions
- [GETQX](#getqx) — Get CORDIC X result
- [GETQY](#getqy) — Get CORDIC Y result
- [JQMT](#jqmt) — Jump if CORDIC empty
- [JNQMT](#jnqmt) — Jump if CORDIC not empty

#### Explanation
POLLQMT copies the state of the CORDIC-read-but-empty event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the CORDIC-read-but-empty event flag prior to clearing it.

The CORDIC-read-but-empty event flag is set whenever GETQX or GETQY executes without any CORDIC results available or in progress. The flag is cleared upon cog start or execution of POLLQMT, WAITQMT, JQMT, or JNQMT instructions.

This instruction enables error detection for CORDIC operations. Reading CORDIC results before they are ready produces undefined values and sets this event flag, allowing the program to detect and handle the error condition.

---

### POLLSE1 / POLLSE2 / POLLSE3 / POLLSE4 — Event {#pollse1}

Checks the selectable event flag (1, 2, 3, or 4) without waiting.

#### Syntax
```pasm
        POLLSE1 {WC|WZ|WCZ}
        POLLSE2 {WC|WZ|WCZ}
        POLLSE3 {WC|WZ|WCZ}
        POLLSE4 {WC|WZ|WCZ}
```

#### Result
SEn event flag state is optionally copied into C and/or Z, then the flag is cleared.

#### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional flag effects to capture event state |

#### Encoding
| Instruction | Encoding |
|-------------|----------|
| POLLSE1 | `EEEE 1101011 CZ0 000000100 000100100` |
| POLLSE2 | `EEEE 1101011 CZ0 000000101 000100100` |
| POLLSE3 | `EEEE 1101011 CZ0 000000110 000100100` |
| POLLSE4 | `EEEE 1101011 CZ0 000000111 000100100` |

**Clocks:** 2

#### Related Instructions
- [SETSE1/2/3/4](#setse1) — Configure selectable event source
- [WAITSE1/2/3/4](#waitse1) — Wait for selectable event
- [JSE1/2/3/4](#jse1) — Jump if SEn event occurred
- [JNSE1/2/3/4](#jnse1) — Jump if SEn event did not occur

#### Explanation
POLLSE1, POLLSE2, POLLSE3, and POLLSE4 copy the state of their respective selectable event flags into C and/or Z and then clear the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the selectable event flag prior to clearing it.

Each selectable event flag is set whenever the corresponding configured event occurs. The flag is cleared upon execution of SETSEn, POLLSEn, WAITSEn, JSEn, or JNSEn instructions.

The P2 provides four independent selectable event generators that can be configured to monitor various hardware conditions including pin edges, Smart Pin events, Hub RAM FIFO status, and more. These instructions enable non-blocking monitoring of multiple hardware sources concurrently.

---

### POLLXFI — Event

Checks the streamer-finished event flag without waiting.

#### Syntax
```pasm
        POLLXFI {WC|WZ|WCZ}
```

#### Result
Streamer-finished event flag is optionally copied into C and/or Z, then it is cleared.

#### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional flag effects to capture event state |

#### Encoding
\simpleencoding{EEEE | 1101011 | CZ0 | 000001011 | 000100100 | — | XFI Event | XFI Event | 2}

#### Related Instructions
- [XINIT](#xinit) — Initialize streamer
- [XZERO](#xzero) — Initialize streamer with zeros
- [XCONT](#xcont) — Continue streamer
- [WAITXFI](#waitxfi) — Wait for streamer finished
- [JXFI](#jxfi) — Jump if streamer finished
- [JNXFI](#jnxfi) — Jump if streamer not finished

#### Explanation
POLLXFI copies the state of the streamer-finished event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the streamer-finished event flag prior to clearing it.

The streamer-finished event flag is set whenever the streamer runs out of commands to process. The streamer-finished event flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXFI, WAITXFI, JXFI, or JNXFI instructions.

This instruction enables non-blocking management of the streamer subsystem. The cog can queue streamer commands and check for completion without blocking, allowing it to prepare the next data while the streamer processes the current transfer.

---

### POLLXMT — Event

Checks the streamer-empty event flag without waiting.

#### Syntax
```pasm
        POLLXMT {WC|WZ|WCZ}
```

#### Result
Streamer-empty event flag is optionally copied into C and/or Z, then it is cleared.

#### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional flag effects to capture event state |

#### Encoding
\simpleencoding{EEEE | 1101011 | CZ0 | 000001010 | 000100100 | — | XMT Event | XMT Event | 2}

#### Related Instructions
- [XINIT](#xinit) — Initialize streamer
- [XZERO](#xzero) — Initialize streamer with zeros
- [XCONT](#xcont) — Continue streamer
- [WAITXMT](#waitxmt) — Wait for streamer ready
- [JXMT](#jxmt) — Jump if streamer ready
- [JNXMT](#jnxmt) — Jump if streamer not ready

#### Explanation
POLLXMT copies the state of the streamer-empty event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the streamer-empty event flag prior to clearing it.

The streamer-empty event flag is set whenever the streamer is ready for a new command. The streamer-empty event flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXMT, WAITXMT, JXMT, or JNXMT instructions.

This instruction enables pipelined streamer operations. By checking when the streamer is ready for the next command, the cog can queue operations without gaps, achieving maximum throughput for video generation, DAC output, or other streaming applications.

---

### POLLXRL — Event

Checks the streamer-LUT-RAM-rollover event flag without waiting.

#### Syntax
```pasm
        POLLXRL {WC|WZ|WCZ}
```

#### Result
Streamer-LUT-RAM-rollover event flag is optionally copied into C and/or Z, then it is cleared.

#### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional flag effects to capture event state |

#### Encoding
\simpleencoding{EEEE | 1101011 | CZ0 | 000001101 | 000100100 | — | XRL Event | XRL Event | 2}

#### Related Instructions
- [XINIT](#xinit) — Initialize streamer
- [XZERO](#xzero) — Initialize streamer with zeros
- [XCONT](#xcont) — Continue streamer
- [WAITXRL](#waitxrl) — Wait for LUT rollover
- [JXRL](#jxrl) — Jump if LUT rollover occurred
- [JNXRL](#jnxrl) — Jump if LUT rollover did not occur

#### Explanation
POLLXRL copies the state of the streamer-LUT-RAM-rollover event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the streamer-LUT-RAM-rollover event flag prior to clearing it.

The streamer-LUT-RAM-rollover event flag is set whenever location $1FF of the Lookup RAM is read by the streamer. The streamer-LUT-RAM-rollover event flag is cleared upon cog start or upon execution of POLLXRL, WAITXRL, JXRL, or JNXRL instructions.

This instruction enables circular buffer management when using LUT RAM as a streamer data source. The event signals when the streamer has wrapped around to the beginning of the LUT buffer, allowing the application to refill the consumed portion.

---

### POLLXRO — Event

Checks the streamer-NCO-rollover event flag without waiting.

#### Syntax
```pasm
        POLLXRO {WC|WZ|WCZ}
```

#### Result
Streamer-NCO-rollover event flag is optionally copied into C and/or Z, then it is cleared.

#### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional flag effects to capture event state |

#### Encoding
\simpleencoding{EEEE | 1101011 | CZ0 | 000001100 | 000100100 | — | XRO Event | XRO Event | 2}

#### Related Instructions
- [XINIT](#xinit) — Initialize streamer
- [XZERO](#xzero) — Initialize streamer with zeros
- [XCONT](#xcont) — Continue streamer
- [WAITXRO](#waitxro) — Wait for NCO rollover
- [JXRO](#jxro) — Jump if NCO rollover occurred
- [JNXRO](#jnxro) — Jump if NCO rollover did not occur

#### Explanation
POLLXRO copies the state of the streamer NCO rollover event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the streamer-NCO-rollover event flag prior to clearing it.

The streamer-NCO-rollover event flag is set whenever the streamer's numerically-controlled oscillator (NCO) rolls over. The streamer-NCO-rollover event flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXRO, WAITXRO, JXRO, or JNXRO instructions.

This instruction enables precise timing control for streamer operations that use the NCO for rate control. The NCO rollover event signals completion of a timing period, useful for synchronized video output, audio generation, or other time-critical streaming applications.

---

## POP Instructions — Stack Operations

The POP family of instructions retrieves values from stacks. POP works with the internal K register stack, while POPA and POPB read from Hub RAM stacks using PTRA and PTRB as stack pointers. These instructions enable subroutine call/return mechanisms and temporary value storage.

### POP — Miscellaneous

Pops a value from the internal K register stack.

#### Syntax
```pasm
        POP     D        {WC|WZ|WCZ}
```

#### Result
D receives the value from the K register.

#### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Destination register to receive popped value |
| WC/WZ/WCZ | Optional flag effects |

#### Encoding
\simpleencoding{EEEE | 1101011 | CZ0 | DDDDDDDDD | 000101011 | D | K[31] | Result = 0 | 2}

#### Related Instructions
- [PUSH](#push) — Push value onto internal stack
- [POPA](#popa) — Pop from Hub stack using PTRA
- [POPB](#popb) — Pop from Hub stack using PTRB

#### Explanation
POP pops the internal stack register K into destination register D. The C flag is set to bit 31 of the popped value when the WC effect is specified. The Z flag is set if the popped value equals zero when the WZ effect is specified.

The P2 provides a single-level internal stack register K that is automatically used by CALL instructions to store the return address. POP retrieves this value, typically as part of a return sequence, though it can also be used to retrieve any value previously stored with PUSH.

---

### POPA — Hub RAM

Pops a long value from Hub RAM using PTRA as the stack pointer.

#### Syntax
```pasm
        POPA    D        {WC|WZ|WCZ}
```

#### Result
D receives the long value from Hub address --PTRA.

#### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Destination register to receive popped value |
| WC/WZ/WCZ | Optional flag effects |

#### Encoding
\simpleencoding{EEEE | 1011000 | CZ1 | DDDDDDDDD | 101011111 | D | MSB of long | Result = 0 | 9...16}

#### Related Instructions
- [PUSHA](#pusha) — Push value to Hub stack using PTRA
- [POPB](#popb) — Pop from Hub stack using PTRB
- [PTRA](#ptra) — Stack pointer register A

#### Explanation
POPA reads a long from Hub address --PTRA into destination register D. PTRA is automatically decremented by 4 before the read occurs (pre-decrement), implementing a descending stack model where the stack grows downward in memory.

The C flag is set to the MSB (bit 31) of the popped value when the WC effect is specified. The Z flag is set if the popped value equals zero when the WZ effect is specified.

This instruction enables Hub RAM-based stacks for deep subroutine nesting and large temporary storage. The descending stack model (decrement before read) pairs with PUSHA's ascending model (write then increment) to create a standard stack convention.

---

### POPB — Hub RAM

Pops a long value from Hub RAM using PTRB as the stack pointer.

#### Syntax
```pasm
        POPB    D        {WC|WZ|WCZ}
```

#### Result
D receives the long value from Hub address --PTRB.

#### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Destination register to receive popped value |
| WC/WZ/WCZ | Optional flag effects |

#### Encoding
\simpleencoding{EEEE | 1011000 | CZ1 | DDDDDDDDD | 111011111 | D | MSB of long | Result = 0 | 9...16}

#### Related Instructions
- [PUSHB](#pushb) — Push value to Hub stack using PTRB
- [POPA](#popa) — Pop from Hub stack using PTRA
- [PTRB](#ptrb) — Stack pointer register B

#### Explanation
POPB reads a long from Hub address --PTRB into destination register D. PTRB is automatically decremented by 4 before the read occurs (pre-decrement), implementing a descending stack model where the stack grows downward in memory.

The C flag is set to the MSB (bit 31) of the popped value when the WC effect is specified. The Z flag is set if the popped value equals zero when the WZ effect is specified.

Having two independent Hub stack pointers (PTRA and PTRB) allows a cog to manage separate stacks for different purposes, such as one for subroutine calls and another for parameter passing or local variables.

---

## PUSH Instructions — Stack Operations

The PUSH family of instructions stores values onto stacks. PUSH works with the internal K register stack, while PUSHA and PUSHB write to Hub RAM stacks using PTRA and PTRB as stack pointers. These instructions enable subroutine call/return mechanisms and temporary value storage.

### PUSH — Miscellaneous

Pushes a value onto the internal K register stack.

#### Syntax
```pasm
        PUSH    {#}D
```

#### Result
The value from D (or immediate value) is stored in the K register.

#### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Source register or 9-bit immediate value (0-511) |

#### Encoding
\simpleencoding{EEEE | 1101011 | 00L | DDDDDDDDD | 000101010 | — | — | — | 2}

#### Related Instructions
- [POP](#pop) — Pop value from internal stack
- [PUSHA](#pusha) — Push to Hub stack using PTRA
- [PUSHB](#pushb) — Push to Hub stack using PTRB

#### Explanation
PUSH pushes the value in D (or an immediate value 0-511) onto the internal stack register K. This instruction does not affect any flags.

The P2 provides a single-level internal stack register K that is automatically used by CALL instructions to store the return address. PUSH can be used to save other values in K, though this overwrites any return address that may be stored there. The typical use is to temporarily save a value that will be restored with POP before the subroutine returns.

---

### PUSHA — Hub RAM

Pushes a long value to Hub RAM using PTRA as the stack pointer.

#### Syntax
```pasm
        PUSHA   {#}D
```

#### Result
The long value from D is written to Hub address PTRA++.

#### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Source register or 9-bit immediate value to push |

#### Encoding
\simpleencoding{EEEE | 1100011 | 0L1 | DDDDDDDDD | 101100001 | — | — | — | 3...10}

#### Related Instructions
- [POPA](#popa) — Pop from Hub stack using PTRA
- [PUSHB](#pushb) — Push to Hub stack using PTRB
- [PTRA](#ptra) — Stack pointer register A

#### Explanation
PUSHA writes the long value in D (or a 9-bit immediate value) to Hub address PTRA++. PTRA is automatically incremented by 4 after the write occurs (post-increment).

This instruction does not affect any flags. The post-increment model means PTRA always points to the next available stack location after the push operation.

PUSHA paired with POPA implements a descending stack in Hub RAM. PUSHA increments after writing (grows upward), while POPA decrements before reading (shrinks downward). Initialize PTRA to the top of the stack area before first use.

---

### PUSHB — Hub RAM

Pushes a long value to Hub RAM using PTRB as the stack pointer.

#### Syntax
```pasm
        PUSHB   {#}D
```

#### Result
The long value from D is written to Hub address PTRB++.

#### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Source register or 9-bit immediate value to push |

#### Encoding
\simpleencoding{EEEE | 1100011 | 0L1 | DDDDDDDDD | 111100001 | — | — | — | 3...10}

#### Related Instructions
- [POPB](#popb) — Pop from Hub stack using PTRB
- [PUSHA](#pusha) — Push to Hub stack using PTRA
- [PTRB](#ptrb) — Stack pointer register B

#### Explanation
PUSHB writes the long value in D (or a 9-bit immediate value) to Hub address PTRB++. PTRB is automatically incremented by 4 after the write occurs (post-increment).

This instruction does not affect any flags. The post-increment model means PTRB always points to the next available stack location after the push operation.

Having two independent Hub stack pointers (PTRA and PTRB) allows a cog to manage separate stacks for different purposes. For example, PTRA might track subroutine return addresses while PTRB manages a parameter stack or circular buffer.
