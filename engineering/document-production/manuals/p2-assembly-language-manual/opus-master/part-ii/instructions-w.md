# W Instructions

This section documents all PASM2 instructions beginning with W, including wait operations, memory writes, FIFO operations, and Smart Pin configuration.

---

## WAITATN — Event

Wait for attention event from another cog.

### Syntax
```pasm
        WAITATN {WC|WZ|WCZ}
```

### Result
Waits for an attention event to occur (unless the event flag is already set), then clears the event flag and resumes execution at the next instruction. Optionally times out if the attention event doesn't occur soon enough, setting C and/or Z flags before resuming.

### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional effects to update flags on timeout |

### Encoding
```
EEEE 1101011 CZ0 000011110 000100100
```
**Write:** —
**C Flag:** Set if timeout occurred before event
**Z Flag:** Set if timeout occurred before event
**Clocks:** 2+

### Related Instructions
- [COGATN](#cogatn) — Send attention to another cog
- [POLLATN](#pollatn) — Poll attention flag without waiting
- [JATN](#jatn) — Jump if attention flag set
- [JNATN](#jnatn) — Jump if attention flag clear

### Explanation
WAITATN waits for an attention event to occur, stalling the pipeline until the event flag is set. The attention event flag is set whenever another cog issues an attention request for this cog using COGATN. The flag is cleared upon cog start or execution of POLLATN, WAITATN, JATN, or JNATN instructions.

To set an optional timeout, insert a SETQ instruction (with a future System Counter target value) immediately before WAITATN. The WC, WZ, or WCZ effect is recommended only when timeout is specified. The C flag and/or Z flag is set (1) if timeout occurred before the event, or cleared (0) if the event occurred before timeout.

During a wait, the pipeline is stalled—no instructions execute and no interrupts are processed in the cog until the wait condition ends.

---

## WAITCT1 — Event

Wait for counter 1 event flag.

### Syntax
```pasm
        WAITCT1 {WC|WZ|WCZ}
```

### Result
Waits for the CT1 event flag to be set, then clears the flag and resumes execution. If timeout occurs (with prior SETQ), C and/or Z are set.

### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional effects to update flags on timeout |

### Encoding
```
EEEE 1101011 CZ0 000010001 000100100
```
**Write:** —
**C Flag:** Set if timeout occurred before event
**Z Flag:** Set if timeout occurred before event
**Clocks:** 2+

### Related Instructions
- [WAITCT2](#waitct2) — Wait for counter 2 event
- [WAITCT3](#waitct3) — Wait for counter 3 event
- [ADDCT1](#addct1) — Add value to CT1 event trigger
- [POLLCT1](#pollct1) — Poll CT1 flag without waiting

### Explanation
WAITCT1 waits for a counter 1 event to occur, stalling the pipeline until the event flag is set. The CT1 event flag is set whenever the System Counter (CT) passes the value in the CT1 event trigger register; i.e., MSB of (CT - CT1) is 0.

To set an optional timeout, insert a SETQ instruction (with a future System Counter target value) immediately before WAITCT1. The WC/WZ/WCZ effect is recommended only with timeout specified. Flags are set (1) if timeout occurred before the event, or cleared (0) if the event occurred first.

The CT1 event flag is cleared by execution of ADDCT1, POLLCT1, WAITCT1, JCT1, or JNCT1 instructions.

During a wait, the pipeline is stalled—no instructions execute and no interrupts are processed until the wait ends. This provides deterministic timing for time-critical operations.

---

## WAITCT2 — Event

Wait for counter 2 event flag.

### Syntax
```pasm
        WAITCT2 {WC|WZ|WCZ}
```

### Result
Waits for the CT2 event flag to be set, then clears the flag and resumes execution. If timeout occurs (with prior SETQ), C and/or Z are set.

### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional effects to update flags on timeout |

### Encoding
```
EEEE 1101011 CZ0 000010010 000100100
```
**Write:** —
**C Flag:** Set if timeout occurred before event
**Z Flag:** Set if timeout occurred before event
**Clocks:** 2+

### Related Instructions
- [WAITCT1](#waitct1) — Wait for counter 1 event
- [WAITCT3](#waitct3) — Wait for counter 3 event
- [ADDCT2](#addct2) — Add value to CT2 event trigger
- [POLLCT2](#pollct2) — Poll CT2 flag without waiting

### Explanation
WAITCT2 waits for a counter 2 event to occur, stalling the pipeline until the event flag is set. The CT2 event flag is set whenever the System Counter (CT) passes the value in the CT2 event trigger register; i.e., MSB of (CT - CT2) is 0.

To set an optional timeout, insert a SETQ instruction (with a future System Counter target value) immediately before WAITCT2. The WC/WZ/WCZ effect is recommended only with timeout specified. Flags are set (1) if timeout occurred before the event, or cleared (0) if the event occurred first.

The CT2 event flag is cleared by execution of ADDCT2, POLLCT2, WAITCT2, JCT2, or JNCT2 instructions.

During a wait, the pipeline is stalled—no instructions execute and no interrupts are processed until the wait ends.

---

## WAITCT3 — Event

Wait for counter 3 event flag.

### Syntax
```pasm
        WAITCT3 {WC|WZ|WCZ}
```

### Result
Waits for the CT3 event flag to be set, then clears the flag and resumes execution. If timeout occurs (with prior SETQ), C and/or Z are set.

### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional effects to update flags on timeout |

### Encoding
```
EEEE 1101011 CZ0 000010011 000100100
```
**Write:** —
**C Flag:** Set if timeout occurred before event
**Z Flag:** Set if timeout occurred before event
**Clocks:** 2+

### Related Instructions
- [WAITCT1](#waitct1) — Wait for counter 1 event
- [WAITCT2](#waitct2) — Wait for counter 2 event
- [ADDCT3](#addct3) — Add value to CT3 event trigger
- [POLLCT3](#pollct3) — Poll CT3 flag without waiting

### Explanation
WAITCT3 waits for a counter 3 event to occur, stalling the pipeline until the event flag is set. The counter 3 event flag is set whenever the System Counter (CT) passes the value in the CT3 event trigger register; i.e., MSB of (CT - CT3) is 0.

To set an optional timeout, insert a SETQ instruction (with a future System Counter target value) immediately before WAITCT3. The WC, WZ, or WCZ effect is recommended only when timeout is specified. The C flag and/or Z flag is set (1) if timeout occurred before the event, or cleared (0) if the event occurred before timeout.

The counter event flag is cleared upon execution of ADDCT3, POLLCT3, WAITCT3, JCT3, or JNCT3 instructions.

During a wait, the pipeline is stalled—no instructions execute and no interrupts are processed in the cog until the wait condition ends.

---

## WAITFBW — Event

Wait for FIFO-interface-block-wrap event.

### Syntax
```pasm
        WAITFBW {WC|WZ|WCZ}
```

### Result
Waits for a FIFO-interface-block-wrap event to occur, then clears the flag and resumes execution. Optionally times out with C/Z set if event doesn't occur soon enough.

### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional effects to update flags on timeout |

### Encoding
```
EEEE 1101011 CZ0 000011001 000100100
```
**Write:** —
**C Flag:** Set if timeout occurred before event
**Z Flag:** Set if timeout occurred before event
**Clocks:** 2+

### Related Instructions
- [RDFAST](#rdfast) — Set up fast FIFO read
- [WRFAST](#wrfast) — Set up fast FIFO write
- [FBLOCK](#fblock) — Set FIFO block parameters
- [POLLFBW](#pollfbw) — Poll FIFO block wrap flag

### Explanation
WAITFBW waits for a FIFO-interface-block-wrap event to occur, stalling the pipeline until the event flag is set. The FIFO-interface-block-wrap event flag is set whenever the Hub RAM FIFO interface exhausts its block count and reloads its block count and start address.

To set an optional timeout, insert a SETQ instruction (with a future System Counter target value) immediately before WAITFBW. The WC, WZ, or WCZ effect is recommended only when timeout is specified. The C flag and/or Z flag is set (1) if timeout occurred before the event, or cleared (0) if the event occurred before timeout.

The FIFO-interface-block-wrap event flag is cleared upon execution of RDFAST, WRFAST, FBLOCK, POLLFBW, WAITFBW, JFBW, or JNFBW instructions.

During a wait, the pipeline is stalled—no instructions execute and no interrupts are processed in the cog until the wait condition ends.

---

## WAITINT — Event

Wait for interrupt-occurred event.

### Syntax
```pasm
        WAITINT {WC|WZ|WCZ}
```

### Result
Waits for an interrupt-occurred event, then clears the flag and resumes execution. Optionally times out with C/Z set if event doesn't occur soon enough.

### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional effects to update flags on timeout |

### Encoding
```
EEEE 1101011 CZ0 000010000 000100100
```
**Write:** —
**C Flag:** Set if timeout occurred before event
**Z Flag:** Set if timeout occurred before event
**Clocks:** 2+

### Related Instructions
- [POLLINT](#pollint) — Poll interrupt flag without waiting
- [JINT](#jint) — Jump if interrupt occurred
- [JNINT](#jnint) — Jump if interrupt not occurred

### Explanation
WAITINT waits for an interrupt-occurred event to occur, stalling the pipeline until the event flag is set. The interrupt-occurred event flag is set whenever interrupt 1, 2, or 3 occurs—debug interrupts are ignored.

To set an optional timeout, insert a SETQ instruction (with a future System Counter target value) immediately before WAITINT. The WC, WZ, or WCZ effect is recommended only when timeout is specified. The C flag and/or Z flag is set (1) if timeout occurred before the event, or cleared (0) if the event occurred before timeout.

The interrupt-occurred event flag is cleared upon cog start or execution of POLLINT, WAITINT, JINT, or JNINT instructions.

During a wait, the pipeline is stalled—no instructions execute and no interrupts are processed in the cog until the wait condition ends.

---

## WAITPAT — Event

Wait for pin-pattern-detected event.

### Syntax
```pasm
        WAITPAT {WC|WZ|WCZ}
```

### Result
Waits for a pin-pattern-detected event, then clears the flag and resumes execution. Optionally times out with C/Z set if event doesn't occur soon enough.

### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional effects to update flags on timeout |

### Encoding
```
EEEE 1101011 CZ0 000011000 000100100
```
**Write:** —
**C Flag:** Set if timeout occurred before event
**Z Flag:** Set if timeout occurred before event
**Clocks:** 2+

### Related Instructions
- [SETPAT](#setpat) — Configure pin pattern detector
- [POLLPAT](#pollpat) — Poll pattern flag without waiting
- [JPAT](#jpat) — Jump if pattern detected
- [JNPAT](#jnpat) — Jump if pattern not detected

### Explanation
WAITPAT waits for a pin-pattern-detected event to occur, stalling the pipeline until the event flag is set. The pin-pattern-detected event flag is set whenever the masked input pins match or don't match the pattern described by a previous SETPAT instruction.

To set an optional timeout, insert a SETQ instruction (with a future System Counter target value) immediately before WAITPAT. The WC, WZ, or WCZ effect is recommended only when timeout is specified. The C flag and/or Z flag is set (1) if timeout occurred before the event, or cleared (0) if the event occurred before timeout.

The pin-pattern-detected event flag is cleared upon execution of SETPAT, POLLPAT, WAITPAT, JPAT, or JNPAT instructions.

During a wait, the pipeline is stalled—no instructions execute and no interrupts are processed in the cog until the wait condition ends.

---

## WAITSE1 — Event

Wait for selectable event 1 flag.

### Syntax
```pasm
        WAITSE1 {WC|WZ|WCZ}
```

### Result
Waits for the SE1 event flag to be set, then clears the flag and resumes execution. If timeout occurs (with prior SETQ), C and/or Z are set.

### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional effects to update flags on timeout |

### Encoding
```
EEEE 1101011 CZ0 000010100 000100100
```
**Write:** —
**C Flag:** Set if timeout occurred before event
**Z Flag:** Set if timeout occurred before event
**Clocks:** 2+

### Related Instructions
- [WAITSE2](#waitse2) — Wait for selectable event 2
- [WAITSE3](#waitse3) — Wait for selectable event 3
- [WAITSE4](#waitse4) — Wait for selectable event 4
- [SETSE1](#setse1) — Configure selectable event 1
- [POLLSE1](#pollse1) — Poll SE1 flag without waiting

### Explanation
WAITSE1 waits for selectable event 1 to occur, stalling the pipeline until the event flag is set. The SE1 event flag is set whenever the configured selectable event 1 occurs.

To set an optional timeout, insert a SETQ instruction (with a future System Counter target value) immediately before WAITSE1. The WC/WZ/WCZ effect is recommended only with timeout specified. Flags are set (1) if timeout occurred before the event, or cleared (0) if the event occurred first.

The SE1 event flag is cleared by execution of SETSE1, POLLSE1, WAITSE1, JSE1, or JNSE1 instructions.

During a wait, the pipeline is stalled—no instructions execute and no interrupts are processed until the wait ends.

---

## WAITSE2 — Event

Wait for selectable event 2 flag.

### Syntax
```pasm
        WAITSE2 {WC|WZ|WCZ}
```

### Result
Waits for the SE2 event flag to be set, then clears the flag and resumes execution. If timeout occurs (with prior SETQ), C and/or Z are set.

### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional effects to update flags on timeout |

### Encoding
```
EEEE 1101011 CZ0 000010101 000100100
```
**Write:** —
**C Flag:** Set if timeout occurred before event
**Z Flag:** Set if timeout occurred before event
**Clocks:** 2+

### Related Instructions
- [WAITSE1](#waitse1) — Wait for selectable event 1
- [WAITSE3](#waitse3) — Wait for selectable event 3
- [WAITSE4](#waitse4) — Wait for selectable event 4
- [SETSE2](#setse2) — Configure selectable event 2
- [POLLSE2](#pollse2) — Poll SE2 flag without waiting

### Explanation
WAITSE2 waits for selectable event 2 to occur, stalling the pipeline until the event flag is set. The SE2 event flag is set whenever the configured selectable event 2 occurs.

To set an optional timeout, insert a SETQ instruction (with a future System Counter target value) immediately before WAITSE2. The WC/WZ/WCZ effect is recommended only with timeout specified. Flags are set (1) if timeout occurred before the event, or cleared (0) if the event occurred first.

The SE2 event flag is cleared by execution of SETSE2, POLLSE2, WAITSE2, JSE2, or JNSE2 instructions.

During a wait, the pipeline is stalled—no instructions execute and no interrupts are processed until the wait ends.

---

## WAITSE3 — Event

Wait for selectable event 3 flag.

### Syntax
```pasm
        WAITSE3 {WC|WZ|WCZ}
```

### Result
Waits for the SE3 event flag to be set, then clears the flag and resumes execution. If timeout occurs (with prior SETQ), C and/or Z are set.

### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional effects to update flags on timeout |

### Encoding
```
EEEE 1101011 CZ0 000010110 000100100
```
**Write:** —
**C Flag:** Set if timeout occurred before event
**Z Flag:** Set if timeout occurred before event
**Clocks:** 2+

### Related Instructions
- [WAITSE1](#waitse1) — Wait for selectable event 1
- [WAITSE2](#waitse2) — Wait for selectable event 2
- [WAITSE4](#waitse4) — Wait for selectable event 4
- [SETSE3](#setse3) — Configure selectable event 3
- [POLLSE3](#pollse3) — Poll SE3 flag without waiting

### Explanation
WAITSE3 waits for selectable event 3 to occur, stalling the pipeline until the event flag is set. The SE3 event flag is set whenever the configured selectable event 3 occurs.

To set an optional timeout, insert a SETQ instruction (with a future System Counter target value) immediately before WAITSE3. The WC/WZ/WCZ effect is recommended only with timeout specified. Flags are set (1) if timeout occurred before the event, or cleared (0) if the event occurred first.

The SE3 event flag is cleared by execution of SETSE3, POLLSE3, WAITSE3, JSE3, or JNSE3 instructions.

During a wait, the pipeline is stalled—no instructions execute and no interrupts are processed until the wait ends.

---

## WAITSE4 — Event

Wait for selectable event 4 flag.

### Syntax
```pasm
        WAITSE4 {WC|WZ|WCZ}
```

### Result
Waits for the SE4 event flag to be set, then clears the flag and resumes execution. If timeout occurs (with prior SETQ), C and/or Z are set.

### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional effects to update flags on timeout |

### Encoding
```
EEEE 1101011 CZ0 000010111 000100100
```
**Write:** —
**C Flag:** Set if timeout occurred before event
**Z Flag:** Set if timeout occurred before event
**Clocks:** 2+

### Related Instructions
- [WAITSE1](#waitse1) — Wait for selectable event 1
- [WAITSE2](#waitse2) — Wait for selectable event 2
- [WAITSE3](#waitse3) — Wait for selectable event 3
- [SETSE4](#setse4) — Configure selectable event 4
- [POLLSE4](#pollse4) — Poll SE4 flag without waiting

### Explanation
WAITSE4 waits for selectable event 4 to occur, stalling the pipeline until the event flag is set. The SE4 event flag is set whenever the configured selectable event 4 occurs.

To set an optional timeout, insert a SETQ instruction (with a future System Counter target value) immediately before WAITSE4. The WC/WZ/WCZ effect is recommended only with timeout specified. Flags are set (1) if timeout occurred before the event, or cleared (0) if the event occurred first.

The SE4 event flag is cleared by execution of SETSE4, POLLSE4, WAITSE4, JSE4, or JNSE4 instructions.

During a wait, the pipeline is stalled—no instructions execute and no interrupts are processed until the wait ends.

---

## WAITX — Miscellaneous

Wait for D+1 clock cycles.

### Syntax
```pasm
        WAITX   {#}D {WC/WZ/WCZ}
```

### Result
Stalls the cog for D+1 clock cycles, providing precise timing delays. Sets C and Z to 0 after completion.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Number of cycles minus 1 to wait (0-511 for immediate) |
| WC/WZ/WCZ | Optional effects; always set to 0 after completion |

### Encoding
```
EEEE 1101011 CZL DDDDDDDDD 000011111
```
**Write:** —
**C Flag:** Set to 0 after completion
**Z Flag:** Set to 0 after completion
**Clocks:** 2 + D

### Related Instructions
- [WAITCT1](#waitct1) — Wait for specific CT value
- [WAITCT2](#waitct2) — Wait for specific CT value
- [WAITCT3](#waitct3) — Wait for specific CT value
- [WAITPAT](#waitpat) — Wait for pin pattern
- [WAITSE1-4](#waitse1) — Wait for selectable event

### Explanation
WAITX stalls the cog for precise timing delays. The actual wait time is D+1 cycles minimum. This instruction is critical for bit-banging protocols, PWM generation, and timing-sensitive operations where precise delays are required.

WAITX blocks cog execution completely—no instructions execute and no interrupts are processed during the wait period. For long delays, consider using WAITCT instructions instead. For continuous PWM generation, use Smart Pins rather than software loops with WAITX.

WAITX is essential for protocols requiring precise bit timing, such as HUB75 RGB LED panel driving, SPI bit-banging, and other time-critical I/O operations. The instruction guarantees deterministic timing regardless of other system activity.

---

## WAITXFI — Event

Wait for streamer-finished event.

### Syntax
```pasm
        WAITXFI {WC|WZ|WCZ}
```

### Result
Waits for a streamer-finished event to occur, then clears the flag and resumes execution. Optionally times out with C/Z set if event doesn't occur soon enough.

### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional effects to update flags on timeout |

### Encoding
```
EEEE 1101011 CZ0 000011011 000100100
```
**Write:** —
**C Flag:** Set if timeout occurred before event
**Z Flag:** Set if timeout occurred before event
**Clocks:** 2+

### Related Instructions
- [WAITXMT](#waitxmt) — Wait for streamer empty
- [WAITXRL](#waitxrl) — Wait for streamer LUT rollover
- [WAITXRO](#waitxro) — Wait for streamer NCO rollover
- [XINIT](#xinit) — Initialize streamer
- [XCONT](#xcont) — Continue streamer

### Explanation
WAITXFI waits for a streamer-finished event to occur, stalling the pipeline until the event flag is set. The streamer-finished event flag is set whenever the streamer runs out of commands to process.

To set an optional timeout, insert a SETQ instruction (with a future System Counter target value) immediately before WAITXFI. The WC, WZ, or WCZ effect is recommended only when timeout is specified. The C flag and/or Z flag is set (1) if timeout occurred before the event, or cleared (0) if the event occurred before timeout.

The streamer-finished event flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXFI, WAITXFI, JXFI, or JNXFI instructions.

During a wait, the pipeline is stalled—no instructions execute and no interrupts are processed in the cog until the wait condition ends.

---

## WAITXMT — Event

Wait for streamer-empty event.

### Syntax
```pasm
        WAITXMT {WC|WZ|WCZ}
```

### Result
Waits for a streamer-empty event to occur, then clears the flag and resumes execution. Optionally times out with C/Z set if event doesn't occur soon enough.

### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional effects to update flags on timeout |

### Encoding
```
EEEE 1101011 CZ0 000011010 000100100
```
**Write:** —
**C Flag:** Set if timeout occurred before event
**Z Flag:** Set if timeout occurred before event
**Clocks:** 2+

### Related Instructions
- [WAITXFI](#waitxfi) — Wait for streamer finished
- [WAITXRL](#waitxrl) — Wait for streamer LUT rollover
- [WAITXRO](#waitxro) — Wait for streamer NCO rollover
- [XINIT](#xinit) — Initialize streamer
- [XCONT](#xcont) — Continue streamer

### Explanation
WAITXMT waits for a streamer-empty event to occur, stalling the pipeline until the event flag is set. The streamer-empty event flag is set whenever the streamer is ready for a new command.

To set an optional timeout, insert a SETQ instruction (with a future System Counter target value) immediately before WAITXMT. The WC, WZ, or WCZ effect is recommended only when timeout is specified. The C flag and/or Z flag is set (1) if timeout occurred before the event, or cleared (0) if the event occurred before timeout.

The streamer-empty event flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXMT, WAITXMT, JXMT, or JNXMT instructions.

During a wait, the pipeline is stalled—no instructions execute and no interrupts are processed in the cog until the wait condition ends.

---

## WAITXRL — Event

Wait for streamer-LUT-RAM-rollover event.

### Syntax
```pasm
        WAITXRL {WC|WZ|WCZ}
```

### Result
Waits for a streamer-LUT-RAM-rollover event to occur, then clears the flag and resumes execution. Optionally times out with C/Z set if event doesn't occur soon enough.

### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional effects to update flags on timeout |

### Encoding
```
EEEE 1101011 CZ0 000011101 000100100
```
**Write:** —
**C Flag:** Set if timeout occurred before event
**Z Flag:** Set if timeout occurred before event
**Clocks:** 2+

### Related Instructions
- [WAITXFI](#waitxfi) — Wait for streamer finished
- [WAITXMT](#waitxmt) — Wait for streamer empty
- [WAITXRO](#waitxro) — Wait for streamer NCO rollover
- [POLLXRL](#pollxrl) — Poll LUT rollover flag

### Explanation
WAITXRL waits for a streamer-LUT-RAM-rollover event to occur, stalling the pipeline until the event flag is set. The streamer-LUT-RAM-rollover event flag is set whenever location $1FF of the Lookup RAM is read by the streamer.

To set an optional timeout, insert a SETQ instruction (with a future System Counter target value) immediately before WAITXRL. The WC, WZ, or WCZ effect is recommended only when timeout is specified. The C flag and/or Z flag is set (1) if timeout occurred before the event, or cleared (0) if the event occurred before timeout.

The streamer-LUT-RAM-rollover event flag is cleared upon cog start or execution of POLLXRL, WAITXRL, JXRL, or JNXRL instructions.

During a wait, the pipeline is stalled—no instructions execute and no interrupts are processed in the cog until the wait condition ends.

---

## WAITXRO — Event

Wait for streamer-NCO-rollover event.

### Syntax
```pasm
        WAITXRO {WC|WZ|WCZ}
```

### Result
Waits for a streamer-NCO-rollover event to occur, then clears the flag and resumes execution. Optionally times out with C/Z set if event doesn't occur soon enough.

### Parameters
| Parameter | Description |
|-----------|-------------|
| WC/WZ/WCZ | Optional effects to update flags on timeout |

### Encoding
```
EEEE 1101011 CZ0 000011100 000100100
```
**Write:** —
**C Flag:** Set if timeout occurred before event
**Z Flag:** Set if timeout occurred before event
**Clocks:** 2+

### Related Instructions
- [WAITXFI](#waitxfi) — Wait for streamer finished
- [WAITXMT](#waitxmt) — Wait for streamer empty
- [WAITXRL](#waitxrl) — Wait for streamer LUT rollover
- [POLLXRO](#pollxro) — Poll NCO rollover flag

### Explanation
WAITXRO waits for a streamer-NCO-rollover event to occur, stalling the pipeline until the event flag is set. The streamer-NCO-rollover event flag is set whenever the streamer's numerically-controlled oscillator (NCO) rolls over.

To set an optional timeout, insert a SETQ instruction (with a future System Counter target value) immediately before WAITXRO. The WC, WZ, or WCZ effect is recommended only when timeout is specified. The C flag and/or Z flag is set (1) if timeout occurred before the event, or cleared (0) if the event occurred before timeout.

The streamer-NCO-rollover event flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXRO, WAITXRO, JXRO, or JNXRO instructions.

During a wait, the pipeline is stalled—no instructions execute and no interrupts are processed in the cog until the wait condition ends.

---

## WFBYTE — Hub FIFO

Write byte to FIFO.

### Syntax
```pasm
        WFBYTE  {#}D
```

### Result
Writes the byte in D[7:0] into the FIFO. Must be used after WRFAST has configured the FIFO.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Byte value to write (bits 7:0 used) |

### Encoding
```
EEEE 1101011 00L DDDDDDDDD 000010101
```
**Write:** —
**C Flag:** No effect
**Z Flag:** No effect
**Clocks:** 2

### Related Instructions
- [WFWORD](#wfword) — Write word to FIFO
- [WFLONG](#wflong) — Write long to FIFO
- [WRFAST](#wrfast) — Set up fast FIFO write

### Explanation
WFBYTE writes a byte from D[7:0] into the Hub FIFO interface. This instruction must be used after WRFAST has configured the FIFO for fast Hub memory writes. The FIFO provides high-performance streaming writes to Hub RAM.

Only the lower 8 bits of D are written; the upper 24 bits are ignored. WFBYTE executes in 2 clock cycles when the FIFO is ready. If the FIFO is full, execution stalls until space becomes available.

---

## WFLONG — Hub FIFO

Write long to FIFO.

### Syntax
```pasm
        WFLONG  {#}D
```

### Result
Writes the long in D[31:0] into the FIFO. Must be used after WRFAST has configured the FIFO.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Long value to write (all 32 bits used) |

### Encoding
```
EEEE 1101011 00L DDDDDDDDD 000010111
```
**Write:** —
**C Flag:** No effect
**Z Flag:** No effect
**Clocks:** 2

### Related Instructions
- [WFBYTE](#wfbyte) — Write byte to FIFO
- [WFWORD](#wfword) — Write word to FIFO
- [WRFAST](#wrfast) — Set up fast FIFO write

### Explanation
WFLONG writes a long (32-bit value) from D[31:0] into the Hub FIFO interface. This instruction must be used after WRFAST has configured the FIFO for fast Hub memory writes. The FIFO provides high-performance streaming writes to Hub RAM.

All 32 bits of D are written. WFLONG executes in 2 clock cycles when the FIFO is ready. If the FIFO is full, execution stalls until space becomes available.

---

## WFWORD — Hub FIFO

Write word to FIFO.

### Syntax
```pasm
        WFWORD  {#}D
```

### Result
Writes the word in D[15:0] into the FIFO. Must be used after WRFAST has configured the FIFO.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Word value to write (bits 15:0 used) |

### Encoding
```
EEEE 1101011 00L DDDDDDDDD 000010110
```
**Write:** —
**C Flag:** No effect
**Z Flag:** No effect
**Clocks:** 2

### Related Instructions
- [WFBYTE](#wfbyte) — Write byte to FIFO
- [WFLONG](#wflong) — Write long to FIFO
- [WRFAST](#wrfast) — Set up fast FIFO write

### Explanation
WFWORD writes a word (16-bit value) from D[15:0] into the Hub FIFO interface. This instruction must be used after WRFAST has configured the FIFO for fast Hub memory writes. The FIFO provides high-performance streaming writes to Hub RAM.

Only the lower 16 bits of D are written; the upper 16 bits are ignored. WFWORD executes in 2 clock cycles when the FIFO is ready. If the FIFO is full, execution stalls until space becomes available.

---

## WMLONG — Hub RAM

Write masked long to hub RAM (non-zero bytes only).

### Syntax
```pasm
        WMLONG  D,{#}S/P
```

### Result
Writes only non-$00 bytes in D[31:0] to hub address S/PTRx. Prior SETQ/SETQ2 invokes cog/LUT block transfer.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Long value with bytes to write (non-zero bytes only) |
| S/P | Hub address or pointer (PTRA/PTRB) |

### Encoding
```
EEEE 1010011 11I DDDDDDDDD SSSSSSSSS
```
**Write:** —
**C Flag:** No effect
**Z Flag:** No effect
**Clocks:** 3...10

### Related Instructions
- [WRLONG](#wrlong) — Write long to hub RAM
- [WRBYTE](#wrbyte) — Write byte to hub RAM
- [WRWORD](#wrword) — Write word to hub RAM

### Explanation
WMLONG writes only non-zero bytes from D to Hub RAM at address S. Each byte in D is examined: if the byte is $00, that byte position in Hub RAM is not modified; if the byte is non-zero, it is written to Hub RAM.

This masked write capability is useful for sprite graphics, text overlay, and other applications where selective pixel/byte updates are needed without affecting other data in the same long.

Prior execution of SETQ or SETQ2 invokes cog or LUT block transfer mode, writing multiple longs with masking.

---

## WRBYTE — Hub RAM

Write byte to hub RAM.

### Syntax
```pasm
        WRBYTE  {#}D,{#}S/P
```

### Result
Writes the byte in D[7:0] to hub address S/PTRx.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Byte value to write (bits 7:0 used) |
| S/P | Hub address or pointer (PTRA/PTRB) |

### Encoding
```
EEEE 1100010 0LI DDDDDDDDD SSSSSSSSS
```
**Write:** —
**C Flag:** No effect
**Z Flag:** No effect
**Clocks:** 3...10

### Related Instructions
- [WRWORD](#wrword) — Write word to hub RAM
- [WRLONG](#wrlong) — Write long to hub RAM
- [RDBYTE](#rdbyte) — Read byte from hub RAM

### Explanation
WRBYTE writes the byte in D[7:0] to Hub RAM at address S/PTRx. Only the lower 8 bits of D are written; the upper 24 bits are ignored.

The instruction takes 3 to 10 clock cycles depending on Hub RAM timing. Hub RAM uses a rotating time-slot system where each cog gets access during its assigned slot. If the instruction executes during this cog's slot, it completes in 3 cycles. Otherwise, it must wait for the next available slot.

When S specifies PTRA or PTRB, the pointer value is used as the Hub address. Pointer auto-increment modes (++ and --) can be applied for sequential access.

---

## WRC — Math and Logic

Write C flag value to register.

### Syntax
```pasm
        WRC     D
```

### Result
Writes 0 or 1 to D according to the C flag state. D = {31'b0, C}.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Destination register |

### Encoding
```
EEEE 1101011 000 DDDDDDDDD 001101100
```
**Write:** D
**C Flag:** No effect
**Z Flag:** No effect
**Clocks:** 2

### Related Instructions
- [WRNC](#wrnc) — Write inverted C flag to register
- [WRZ](#wrz) — Write Z flag to register
- [WRNZ](#wrnz) — Write inverted Z flag to register

### Explanation
WRC copies the C flag state to register D. If C is set (1), D becomes 1. If C is clear (0), D becomes 0. The upper 31 bits of D are cleared to zero.

This instruction provides a convenient way to convert flag states into numeric values for computation or storage. Combined with conditional execution, WRC enables flag-based value selection without branching.

---

## WRFAST — Hub FIFO

Begin new fast hub write via FIFO.

### Syntax
```pasm
        WRFAST  {#}D,{#}S
```

### Result
Initializes the Hub FIFO for fast writes. D[31] = no wait, D[13:0] = block size in 64-byte units (0 = max), S[19:0] = block start address.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Configuration: bit 31 = nowait, bits 13:0 = block size |
| S | Hub RAM start address (bits 19:0) |

### Encoding
```
EEEE 1100100 0LI DDDDDDDDD SSSSSSSSS
```
**Write:** —
**C Flag:** No effect
**Z Flag:** No effect
**Clocks:** 2 or WRFAST finish + 3

### Related Instructions
- [WFBYTE](#wfbyte) — Write byte to FIFO
- [WFWORD](#wfword) — Write word to FIFO
- [WFLONG](#wflong) — Write long to FIFO
- [RDFAST](#rdfast) — Begin fast hub read via FIFO

### Explanation
WRFAST configures the Hub FIFO interface for fast streaming writes to Hub RAM. After WRFAST executes, use WFBYTE, WFWORD, or WFLONG to write data through the FIFO.

D[13:0] specifies the block size in 64-byte units. A value of 0 selects the maximum block size. D[31] controls wait behavior: if set, FIFO writes proceed without stalling even when Hub RAM is busy.

S[19:0] specifies the starting Hub RAM address. The FIFO automatically increments the address as data is written. When the block is exhausted, the FIFO can be configured to wrap or stop.

If a previous WRFAST operation is still active, this instruction may stall until the previous operation finishes, adding 3 cycles to the base 2-cycle execution time.

---

## WRLONG — Hub RAM

Write long to hub RAM.

### Syntax
```pasm
        WRLONG  {#}D,{#}S/P
```

### Result
Writes the long in D[31:0] to hub address S/PTRx. Prior SETQ/SETQ2 invokes cog/LUT block transfer.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Long value to write (all 32 bits used) |
| S/P | Hub address or pointer (PTRA/PTRB) |

### Encoding
```
EEEE 1100011 0LI DDDDDDDDD SSSSSSSSS
```
**Write:** —
**C Flag:** No effect
**Z Flag:** No effect
**Clocks:** 3...10

### Related Instructions
- [WRBYTE](#wrbyte) — Write byte to hub RAM
- [WRWORD](#wrword) — Write word to hub RAM
- [WMLONG](#wmlong) — Write masked long to hub RAM
- [RDLONG](#rdlong) — Read long from hub RAM

### Explanation
WRLONG writes the 32-bit value in D to Hub RAM at address S/PTRx. All 32 bits of D are written.

The instruction takes 3 to 10 clock cycles depending on Hub RAM timing. Hub RAM uses a rotating time-slot system where each cog gets access during its assigned slot. If the instruction executes during this cog's slot, it completes in 3 cycles. Otherwise, it must wait for the next available slot.

When S specifies PTRA or PTRB, the pointer value is used as the Hub address. Pointer auto-increment modes (++ and --) can be applied for sequential access.

Prior execution of SETQ or SETQ2 invokes block transfer mode, writing multiple longs from cog or LUT RAM to Hub RAM in a burst transfer.

---

## WRLUT — Lookup Table

Write D to LUT address.

### Syntax
```pasm
        WRLUT   {#}D,{#}S/P
```

### Result
Writes D to LUT address S/PTRx.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Value to write |
| S/P | LUT address or pointer (PTRA/PTRB) |

### Encoding
```
EEEE 1100001 1LI DDDDDDDDD SSSSSSSSS
```
**Write:** —
**C Flag:** No effect
**Z Flag:** No effect
**Clocks:** 2

### Related Instructions
- [RDLUT](#rdlut) — Read from LUT address
- [WRLONG](#wrlong) — Write to hub RAM
- [SETQ](#setq) — Set up block transfer

### Explanation
WRLUT writes the value in D to the Lookup Table (LUT) at address S/PTRx. The LUT is a 512-long (2KB) fast memory space shared between cog RAM and LUT RAM in the upper 256 addresses.

When S specifies PTRA or PTRB, the pointer value is used as the LUT address. Only the lower 9 bits of the address are used (0-511), selecting from the 512-long LUT space.

WRLUT executes in 2 clock cycles, providing fast access to LUT RAM for lookup tables, buffers, and temporary storage. The LUT is particularly useful for data that needs faster access than Hub RAM but doesn't fit in cog registers.

---

## WRNC — Math and Logic

Write inverted C flag value to register.

### Syntax
```pasm
        WRNC    D
```

### Result
Writes 0 or 1 to D according to the inverted C flag state. D = {31'b0, !C}.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Destination register |

### Encoding
```
EEEE 1101011 000 DDDDDDDDD 001101101
```
**Write:** D
**C Flag:** No effect
**Z Flag:** No effect
**Clocks:** 2

### Related Instructions
- [WRC](#wrc) — Write C flag to register
- [WRZ](#wrz) — Write Z flag to register
- [WRNZ](#wrnz) — Write inverted Z flag to register

### Explanation
WRNC copies the inverted C flag state to register D. If C is clear (0), D becomes 1. If C is set (1), D becomes 0. The upper 31 bits of D are cleared to zero.

This instruction provides a convenient way to convert inverted flag states into numeric values for computation or storage. Combined with conditional execution, WRNC enables flag-based value selection without branching.

---

## WRNZ — Math and Logic

Write inverted Z flag value to register.

### Syntax
```pasm
        WRNZ    D
```

### Result
Writes 0 or 1 to D according to the inverted Z flag state. D = {31'b0, !Z}.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Destination register |

### Encoding
```
EEEE 1101011 000 DDDDDDDDD 001101111
```
**Write:** D
**C Flag:** No effect
**Z Flag:** No effect
**Clocks:** 2

### Related Instructions
- [WRC](#wrc) — Write C flag to register
- [WRNC](#wrnc) — Write inverted C flag to register
- [WRZ](#wrz) — Write Z flag to register

### Explanation
WRNZ copies the inverted Z flag state to register D. If Z is clear (0), D becomes 1. If Z is set (1), D becomes 0. The upper 31 bits of D are cleared to zero.

This instruction provides a convenient way to convert inverted flag states into numeric values for computation or storage. Combined with conditional execution, WRNZ enables flag-based value selection without branching.

---

## WRPIN — Smart Pin

Configure smart pin mode.

### Syntax
```pasm
        WRPIN   {#}D,{#}S
```

### Result
Sets the mode of smart pins S[10:6]+S[5:0]..S[5:0] to D, acknowledges smart pins. Wraps within A/B pins. Prior SETQ overrides S[10:6].

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Smart pin mode configuration |
| S | Pin number or pin range |

### Encoding
```
EEEE 1100000 0LI DDDDDDDDD SSSSSSSSS
```
**Write:** —
**C Flag:** No effect
**Z Flag:** No effect
**Clocks:** 2

### Related Instructions
- [WXPIN](#wxpin) — Set smart pin X parameter
- [WYPIN](#wypin) — Set smart pin Y parameter
- [RDPIN](#rdpin) — Read smart pin result
- [AKPIN](#akpin) — Acknowledge smart pin

### Explanation
WRPIN configures the operating mode of one or more Smart Pins. Each of the P2's 64 pins has a dedicated Smart Pin module capable of autonomous operation for PWM, serial I/O, pulse measurement, ADC, and many other functions.

**CRITICAL REQUIREMENT**: Smart pins MUST be reset (DIR=0) before configuring with WRPIN. This ensures the smart pin is in a known state and prevents configuration conflicts.

The standard configuration sequence is:
1. DIRL pin — Reset smart pin (required)
2. WRPIN mode, pin — Configure smart pin mode
3. WXPIN x, pin — Set X parameter
4. WYPIN y, pin — Set Y parameter
5. DIRH pin — Enable smart pin

WRPIN #0, pin clears all smart pin configuration. The smart pin begins operation when DIR is set high after configuration.

When S[10:6] is non-zero, multiple pins are configured. Prior SETQ can override the pin count. Pin numbering wraps within A pins (0-31) and B pins (32-63).

---

## WRWORD — Hub RAM

Write word to hub RAM.

### Syntax
```pasm
        WRWORD  {#}D,{#}S/P
```

### Result
Writes the word in D[15:0] to hub address S/PTRx.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Word value to write (bits 15:0 used) |
| S/P | Hub address or pointer (PTRA/PTRB) |

### Encoding
```
EEEE 1100010 1LI DDDDDDDDD SSSSSSSSS
```
**Write:** —
**C Flag:** No effect
**Z Flag:** No effect
**Clocks:** 3...10

### Related Instructions
- [WRBYTE](#wrbyte) — Write byte to hub RAM
- [WRLONG](#wrlong) — Write long to hub RAM
- [RDWORD](#rdword) — Read word from hub RAM

### Explanation
WRWORD writes the word (16-bit value) in D[15:0] to Hub RAM at address S/PTRx. Only the lower 16 bits of D are written; the upper 16 bits are ignored.

The instruction takes 3 to 10 clock cycles depending on Hub RAM timing. Hub RAM uses a rotating time-slot system where each cog gets access during its assigned slot. If the instruction executes during this cog's slot, it completes in 3 cycles. Otherwise, it must wait for the next available slot.

When S specifies PTRA or PTRB, the pointer value is used as the Hub address. Pointer auto-increment modes (++ and --) can be applied for sequential access.

---

## WRZ — Math and Logic

Write Z flag value to register.

### Syntax
```pasm
        WRZ     D
```

### Result
Writes 0 or 1 to D according to the Z flag state. D = {31'b0, Z}.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Destination register |

### Encoding
```
EEEE 1101011 000 DDDDDDDDD 001101110
```
**Write:** D
**C Flag:** No effect
**Z Flag:** No effect
**Clocks:** 2

### Related Instructions
- [WRC](#wrc) — Write C flag to register
- [WRNC](#wrnc) — Write inverted C flag to register
- [WRNZ](#wrnz) — Write inverted Z flag to register

### Explanation
WRZ copies the Z flag state to register D. If Z is set (1), D becomes 1. If Z is clear (0), D becomes 0. The upper 31 bits of D are cleared to zero.

This instruction provides a convenient way to convert flag states into numeric values for computation or storage. Combined with conditional execution, WRZ enables flag-based value selection without branching.

---

## WXPIN — Smart Pin

Set smart pin X parameter.

### Syntax
```pasm
        WXPIN   {#}D,{#}S
```

### Result
Sets the X register of smart pins S[10:6]+S[5:0]..S[5:0] to D, acknowledges smart pins. Wraps within A/B pins. Prior SETQ overrides S[10:6].

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | X parameter value |
| S | Pin number or pin range |

### Encoding
```
EEEE 1100000 1LI DDDDDDDDD SSSSSSSSS
```
**Write:** —
**C Flag:** No effect
**Z Flag:** No effect
**Clocks:** 2

### Related Instructions
- [WRPIN](#wrpin) — Configure smart pin mode
- [WYPIN](#wypin) — Set smart pin Y parameter
- [RDPIN](#rdpin) — Read smart pin result

### Explanation
WXPIN sets the X parameter of one or more Smart Pins. The X register meaning depends on the smart pin mode:

- For PWM modes: Sets frame period or duty cycle parameter
- For serial modes: Controls bit timing and configuration
- For pulse measurement: Sets measurement parameters
- For transition modes: Controls timebase

Writing the X register also acknowledges the smart pin, clearing any completion flags. When S[10:6] is non-zero, multiple pins are configured. Prior SETQ can override the pin count.

---

## WYPIN — Smart Pin

Set smart pin Y parameter.

### Syntax
```pasm
        WYPIN   {#}D,{#}S
```

### Result
Sets the Y register of smart pins S[10:6]+S[5:0]..S[5:0] to D, acknowledges smart pins. Wraps within A/B pins. Prior SETQ overrides S[10:6].

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Y parameter value |
| S | Pin number or pin range |

### Encoding
```
EEEE 1100001 0LI DDDDDDDDD SSSSSSSSS
```
**Write:** —
**C Flag:** No effect
**Z Flag:** No effect
**Clocks:** 2

### Related Instructions
- [WRPIN](#wrpin) — Configure smart pin mode
- [WXPIN](#wxpin) — Set smart pin X parameter
- [RDPIN](#rdpin) — Read smart pin result

### Explanation
WYPIN sets the Y parameter of one or more Smart Pins. The Y register serves multiple purposes depending on smart pin mode:

- For PWM modes: Sets the base period
- For SPI/serial modes: Controls data to transmit
- For counter modes: Sets count value
- For ADC modes: Initiates conversions

Writing the Y register also acknowledges pin completion, clearing any completion flags. This dual purpose makes WYPIN essential for continuous smart pin operation—it both provides new data and signals that previous results have been processed.

When S[10:6] is non-zero, multiple pins are configured. Prior SETQ can override the pin count. Pin numbering wraps within A pins (0-31) and B pins (32-63).
