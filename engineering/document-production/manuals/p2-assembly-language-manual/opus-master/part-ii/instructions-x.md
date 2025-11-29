# X Instructions

This section documents all PASM2 instructions beginning with X, organized alphabetically.

## XCONT — Streamer

Buffer new streamer command to be issued on final NCO rollover of current command, continuing phase.

### Syntax
```pasm
        XCONT   {#}D,{#}S
```

### Result
A new streamer command is buffered and will be issued when the current streamer command completes its final NCO rollover. The phase accumulator continues from its current value rather than being reset to zero.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Streamer mode configuration (register or 9-bit immediate). Configures transfer direction, pin count, and data format. |
| S | Data value or hub address (register or 9-bit immediate) for the streamer operation. |

### Encoding
\simpleencoding{EEEE | 1100110 | 0LI | DDDDDDDDD | SSSSSSSSS | — | — | — | 2+}

### Related Instructions
- [XINIT](#xinit--streamer) — Issue streamer command immediately, zeroing phase
- [XZERO](#xzero--streamer) — Buffer new streamer command, zeroing phase
- [XSTOP](#xstop--streamer) — Stop streamer immediately
- [WAITXFI](#waitxfi) — Wait for streamer to finish

### Explanation
XCONT buffers a new streamer command that executes automatically when the current command completes. Unlike XINIT and XZERO, XCONT preserves the phase accumulator, allowing seamless continuation of streamer operations without phase discontinuities.

This instruction enables chaining multiple streamer operations together while maintaining phase coherence. The buffered command waits for the current command's NCO (numerically controlled oscillator) to complete its final rollover before activation.

The mode word in D specifies the streamer configuration including pin assignments, data direction, and transfer format. The S parameter provides either immediate data or a hub memory address depending on the mode configuration.

XCONT executes in a minimum of 2 clock cycles, with additional cycles required for the actual streamer operation to complete.

---

## XINIT — Streamer

Issue streamer command immediately, zeroing phase.

### Syntax
```pasm
        XINIT   {#}D,{#}S
```

### Result
A streamer command executes immediately with the phase accumulator reset to zero. The streamer begins data transfer according to the mode configuration.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Streamer mode configuration (register or 9-bit immediate). Configures transfer direction, pin count, and data format. |
| S | Data value or hub address (register or 9-bit immediate) for the streamer operation. |

### Encoding
\simpleencoding{EEEE | 1100101 | 0LI | DDDDDDDDD | SSSSSSSSS | — | — | — | 2}

### Related Instructions
- [XCONT](#xcont--streamer) — Continue streamer from current phase
- [XZERO](#xzero--streamer) — Buffer new streamer command, zeroing phase
- [XSTOP](#xstop--streamer) — Stop streamer immediately
- [WAITXFI](#waitxfi) — Wait for streamer to finish
- [WYPIN](#wypin) — Set smart pin Y parameter
- [SETXFRQ](#setxfrq) — Set streamer frequency

### Explanation
XINIT starts a streamer operation immediately, resetting the phase accumulator to zero. This provides a clean starting point for high-speed data transfers between the cog and hub memory or I/O pins.

The streamer operates as a hardware DMA engine, transferring data without CPU intervention. The mode word in D configures critical parameters:
- Transfer direction (input from pins to hub, output from hub to pins, or cog-only operations)
- Number of pins involved in the transfer
- Data formatting (bit order, byte packing, word sizes)

The S parameter provides either the data source (for immediate transfers) or a hub memory address (for hub-based transfers).

XINIT commonly coordinates with smart pins to achieve maximum I/O throughput. A typical pattern starts the streamer with XINIT and simultaneously starts a smart pin clock generator with WYPIN, allowing both to operate in parallel:

```pasm
        XINIT   mode,data          ' Start data transfer
        WYPIN   count,#clk_pin     ' Start clock generation
        WAITXFI                    ' Wait for completion
```

This parallel operation eliminates CPU intervention, enabling sustained high-speed data rates limited only by the configured clock frequency.

XINIT executes in exactly 2 clock cycles, though the complete streamer operation requires additional time based on the data volume and configured speed.

---

## XOR — Math and Logic

Bitwise XOR a value with another.

### Syntax
```pasm
        XOR     D,{#}S      {WC|WZ|WCZ}
```

### Result
D XOR S is stored in D and flags are optionally updated with parity and zero status.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the value to bitwise XOR with S and destination for the result. |
| S | Register, 9-bit immediate, or 32-bit augmented immediate whose value will be bitwise XORed into D. |
| WC | Optional effect to update C flag with parity of result. |
| WZ | Optional effect to update Z flag if result equals zero. |
| WCZ | Optional effect to update both C and Z flags. |

### Encoding
\simpleencoding{EEEE | 0101011 | CZI | DDDDDDDDD | SSSSSSSSS | D | Parity | Zero | 2}

### Related Instructions
- [AND](#and) — Bitwise AND operation
- [OR](#or) — Bitwise OR operation
- [ANDN](#andn) — Bitwise AND NOT operation
- [TEST](#test) — Test bits (non-destructive AND)

### Explanation
XOR performs a bitwise exclusive OR operation between D and S, storing the result in D. Each bit position in the result is set to 1 if the corresponding bits in D and S differ, or 0 if they match.

The exclusive OR operation has several important properties:
- XORing a value with itself produces zero (useful for clearing registers)
- XORing a value with all 1s produces the bitwise complement
- XORing twice with the same value returns the original (useful for simple encryption)
- XOR is commutative: A XOR B equals B XOR A

When the WC effect is specified, the C flag receives the parity of the result—set to 1 if the result contains an odd number of 1 bits, or cleared to 0 for an even number. This provides a fast parity calculation.

When the WZ effect is specified, the Z flag is set if the result equals zero (meaning D and S were identical), or cleared if the result is non-zero (D and S differ in at least one bit).

XOR executes in exactly 2 clock cycles.

---

## XORO32 — Math and Logic

Iterate D with xoroshiro32+ PRNG algorithm.

### Syntax
```pasm
        XORO32  D
```

### Result
D is updated with the next state of the xoroshiro32+ pseudo-random number generator algorithm. The generated random value is placed into the S field of the immediately following instruction.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the 32-bit PRNG state, which is updated to the next state. |

### Encoding
\simpleencoding{EEEE | 1101011 | 000 | DDDDDDDDD | 001101000 | D | — | — | 2}

### Related Instructions
- [GETRND](#getrnd) — Get true random value from hub
- [SETQ](#setq) — Set Q register (alternative for holding random values)

### Explanation
XORO32 implements one iteration of the xoroshiro32+ algorithm, a fast, high-quality pseudo-random number generator. The instruction updates the generator state in D and simultaneously makes the generated random value available to the next instruction by injecting it into that instruction's S field.

The xoroshiro32+ algorithm provides excellent statistical properties for a 32-bit generator:
- Long period (2^32 - 1 values before repeating)
- Good distribution across all output bits
- Fast execution (2 clocks per random number)
- Small state requirement (single 32-bit value)

A typical usage pattern generates random numbers in sequence:

```pasm
        MOV     seed,initial_value      ' Initialize with non-zero seed

.loop   XORO32  seed                    ' Advance PRNG state
        MOV     random_val,0            ' Next instruction receives random in S
        ' Process random_val...
```

The random value appears in the S field of the instruction immediately following XORO32. This means the next instruction must be one that reads from S, and the value specified for S in that instruction's encoding is ignored—it gets replaced by the random value.

The seed value in D must be non-zero. A seed of zero will produce only zero values. For best results, initialize the seed with a value from GETRND or another entropy source.

XORO32 executes in exactly 2 clock cycles.

---

## XSTOP — Streamer

Stop streamer immediately.

### Syntax
```pasm
        XSTOP
```

### Result
The currently active streamer operation terminates immediately.

### Parameters
None.

### Encoding
\simpleencoding{EEEE | 1100101 | 011 | 000000000 | 000000000 | — | — | — | 2}

### Related Instructions
- [XINIT](#xinit--streamer) — Issue streamer command immediately, zeroing phase
- [XCONT](#xcont--streamer) — Continue streamer from current phase
- [XZERO](#xzero--streamer) — Buffer new streamer command, zeroing phase
- [WAITXFI](#waitxfi) — Wait for streamer to finish

### Explanation
XSTOP immediately halts any active streamer operation. This provides programmatic control to abort streamer transfers before completion.

When XSTOP executes, the streamer hardware stops all data movement and pin activity. Any buffered streamer command (from XCONT or XZERO) is also discarded.

XSTOP is useful when:
- Error conditions require aborting a transfer
- Dynamic control flow needs to terminate streaming based on data content
- Cleanup is required before reconfiguring the streamer

After XSTOP, the streamer remains idle until a new XINIT command is issued. The phase accumulator state is undefined after XSTOP—use XINIT (which zeros the phase) rather than XCONT to restart operations.

XSTOP executes in exactly 2 clock cycles.

---

## XZERO — Streamer

Buffer new streamer command, zeroing phase.

### Syntax
```pasm
        XZERO   {#}D,{#}S
```

### Result
A new streamer command is buffered and will be issued when the current streamer command completes its final NCO rollover. The phase accumulator is reset to zero when the buffered command activates.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Streamer mode configuration (register or 9-bit immediate). Configures transfer direction, pin count, and data format. |
| S | Data value or hub address (register or 9-bit immediate) for the streamer operation. |

### Encoding
\simpleencoding{EEEE | 1100101 | 1LI | DDDDDDDDD | SSSSSSSSS | — | — | — | 2+}

### Related Instructions
- [XINIT](#xinit--streamer) — Issue streamer command immediately, zeroing phase
- [XCONT](#xcont--streamer) — Continue streamer from current phase
- [XSTOP](#xstop--streamer) — Stop streamer immediately
- [WAITXFI](#waitxfi) — Wait for streamer to finish

### Explanation
XZERO buffers a new streamer command that executes automatically when the current command completes, with the phase accumulator reset to zero. This combines the buffering behavior of XCONT with the phase-zeroing behavior of XINIT.

The buffered command waits for the current streamer operation's NCO (numerically controlled oscillator) to complete its final rollover before activation. When activation occurs, the phase accumulator resets to zero, providing a clean starting point for the new operation.

This instruction enables chaining multiple streamer operations where each operation should start from a known phase state. This is particularly useful when switching between different streamer modes or when phase coherence between operations is not required.

The mode word in D specifies the streamer configuration including pin assignments, data direction, and transfer format. The S parameter provides either immediate data or a hub memory address depending on the mode configuration.

XZERO executes in a minimum of 2 clock cycles, with additional cycles required for the actual streamer operation to complete.
