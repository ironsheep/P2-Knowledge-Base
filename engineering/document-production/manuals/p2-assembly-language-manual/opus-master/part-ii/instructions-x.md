# Instructions: X

This section contains all PASM2 instructions beginning with the letter X. The X instructions include the XOR logic operation, the xoroshiro32+ PRNG instruction, and the streamer control family.



::: instrheader
## XCONT {#xcont}
Execute Continue

[streamer](#streamer) - Buffers a streamer command continuing from current phase.
:::

**XCONT**  *{#}Dest, {#}Src*

**Result:** Buffers a new streamer command to execute when the current command completes its final NCO rollover, continuing from current phase.

- Dest is the streamer mode configuration.
- Src is the data value or hub address for the streamer operation.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100110 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2+ |


**Related:** [XINIT](#xinit), [XZERO](#xzero), [XSTOP](#xstop), [WAITXFI](#waitxfi)

**Explanation:**

XCONT buffers a new streamer command that executes automatically when the current command completes. Unlike XINIT and XZERO, XCONT preserves the phase accumulator, allowing continuation of streamer operations without a phase discontinuity.

This instruction enables chaining multiple streamer operations together while maintaining phase coherence. The buffered command waits for the current command's NCO (numerically controlled oscillator) to complete its final rollover before activation.

The mode word in Dest specifies the streamer configuration including pin assignments, data direction, and transfer format. The Src parameter provides either immediate data or a hub memory address depending on the mode configuration.



::: instrheader
## XINIT {#xinit}
Execute Initialize

[streamer](#streamer) - Issues a streamer command immediately with phase reset to zero.
:::

**XINIT**  *{#}Dest, {#}Src*

**Result:** Issues a streamer command immediately with the phase accumulator reset to zero.

- Dest is the streamer mode configuration.
- Src is the data value or hub address for the streamer operation.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100101 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 |


**Related:** [XCONT](#xcont), [XZERO](#xzero), [XSTOP](#xstop), [WAITXFI](#waitxfi), [SETXFRQ](#setxfrq)

**Explanation:**

XINIT starts a streamer operation immediately, resetting the phase accumulator to zero. This provides a clean starting point for high-speed data transfers between the cog and hub memory or I/O pins.

The streamer operates as a hardware DMA engine, transferring data without cog intervention. The mode word in Dest configures critical parameters:

- Transfer direction (input from pins to hub, output from hub to pins, or cog-only operations)
- Number of pins involved in the transfer
- Data formatting (bit order, byte packing, word sizes)

The Src parameter provides either the data source (for immediate transfers) or a hub memory address (for hub-based transfers).

XINIT commonly coordinates with smart pins to achieve maximum I/O throughput:

```pasm2
        XINIT   mode, data         ' Start data transfer
        WYPIN   count, #clk_pin    ' Start clock generation
        WAITXFI                    ' Wait for completion
```

This parallel operation eliminates cog intervention, enabling sustained high-speed data rates limited only by the configured clock frequency.



::: instrheader
## XOR {#xor}
Exclusive Or

[Arithmetic Operations](#arithmetic-operations) - Performs bitwise exclusive OR of Dest and Src.
:::

**XOR**  *Dest, {#}Src*  **{WC/WZ/WCZ}**

**Operation:** `D = D ^ S`; `C = parity of result`

**Result:** Dest XOR Src is stored in Dest. Optionally sets C to parity of result and Z if result equals zero.

- Dest is the register containing the value to XOR with Src.
- Src is a register, 9-bit literal, or 32-bit augmented literal (##) whose value is XORed with Dest.
- WC sets C to the parity (odd number of 1 bits) of the result.
- WZ sets Z if the result equals zero.
- WCZ sets both C and Z.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0101011 | CZI | DDDDDDDDD | SSSSSSSSS | parity of result | result == 0 | D | 2 |


**Related:** [AND](#and), [OR](#or), [ANDN](#andn), [TEST](#test)

**Explanation:**

XOR performs a bitwise exclusive OR operation between Dest and Src, storing the result in Dest. Each bit position in the result is set to 1 if the corresponding bits in Dest and Src differ, or 0 if they match.

| Dest | Src | Result |
|:----:|:---:|:------:|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

The exclusive OR operation has several important properties:

- XORing a value with itself produces zero (useful for clearing registers)
- XORing a value with all 1s produces the bitwise complement
- XORing twice with the same value returns the original (useful for simple encryption)
- XOR is commutative: A XOR B equals B XOR A

When the WC effect is specified, the C flag receives the parity of the result—set to 1 if the result contains an odd number of 1 bits, or cleared to 0 for an even number. This provides a fast parity calculation.

When the WZ effect is specified, the Z flag is set if the result equals zero (meaning Dest and Src were identical), or cleared if the result is non-zero (Dest and Src differ in at least one bit).



::: instrheader
## XORO32 {#xoro32}
Xoroshiro 32

[Arithmetic Operations](#arithmetic-operations) - Generates next pseudo-random number using xoroshiro32+ algorithm.
:::

**XORO32**  *Dest*

**Result:** Dest is updated with the next PRNG state. The generated random value is placed into the S field of the next instruction.

- Dest is the register containing the 32-bit PRNG state.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001101000 | --- | --- | D | 2 |


**Related:** [GETRND](#getrnd), [SETQ](#setq)

**Explanation:**

XORO32 implements one iteration of the xoroshiro32+ algorithm, a fast, high-quality pseudo-random number generator. The instruction updates the generator state in Dest and simultaneously makes the generated random value available to the next instruction by injecting it into that instruction's S field.

The xoroshiro32+ algorithm provides excellent statistical properties for a 32-bit generator:

- Long period (2^32^ - 1 values before repeating)
- Good distribution across all output bits
- Fast execution (2 clocks per random number)
- Small state requirement (single 32-bit value)

```pasm2
        MOV     seed, initial_value  ' Initialize with non-zero seed

.loop   XORO32  seed                 ' Advance PRNG state
        MOV     random_val, 0        ' Next instruction receives random in S
        ' Process random_val...
```

The random value appears in the S field of the instruction immediately following XORO32. This means the next instruction must be one that reads from S, and the value specified for S in that instruction's encoding is ignored—it gets replaced by the random value.

The seed value in Dest must be non-zero. A seed of zero will produce only zero values. For best results, initialize the seed with a value from GETRND or another entropy source.



::: instrheader
## XSTOP {#xstop}
Execute Stop

[streamer](#streamer) - Immediately halts the active streamer operation.
:::

**XSTOP**

**Result:** The currently active streamer operation terminates immediately.

- Takes no operands.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100101 | 011 | 000000000 | 000000000 | --- | --- | --- | 2 |


**Related:** [XINIT](#xinit), [XCONT](#xcont), [XZERO](#xzero), [WAITXFI](#waitxfi)

**Explanation:**

XSTOP immediately halts any active streamer operation. This provides programmatic control to abort streamer transfers before completion.

When XSTOP executes, the streamer hardware stops all data movement and pin activity. Any buffered streamer command (from XCONT or XZERO) is also discarded.

XSTOP is useful when:

- Error conditions require aborting a transfer
- Dynamic control flow needs to terminate streaming based on data content
- Cleanup is required before reconfiguring the streamer

After XSTOP, the streamer remains idle until a new XINIT command is issued. XSTOP is itself an alias for XINIT #0,#0, so it leaves the phase accumulator zeroed. To restart, issue XINIT (which begins a new command with phase reset to zero); XCONT cannot be used to restart from idle because it only buffers behind an active command.



::: instrheader
## XZERO {#xzero}
Execute Zero

[streamer](#streamer) - Buffers a streamer command with phase reset to zero.
:::

**XZERO**  *{#}Dest, {#}Src*

**Result:** Buffers a new streamer command to execute when the current command completes, resetting phase to zero.

- Dest is the streamer mode configuration.
- Src is the data value or hub address for the streamer operation.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100101 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2+ |


**Related:** [XINIT](#xinit), [XCONT](#xcont), [XSTOP](#xstop), [WAITXFI](#waitxfi)

**Explanation:**

XZERO buffers a new streamer command that executes automatically when the current command completes, with the phase accumulator reset to zero. This combines the buffering behavior of XCONT with the phase-zeroing behavior of XINIT.

The buffered command waits for the current streamer operation's NCO (numerically controlled oscillator) to complete its final rollover before activation. When activation occurs, the phase accumulator resets to zero, providing a clean starting point for the new operation.

This instruction enables chaining multiple streamer operations where each operation should start from a known phase state. This applies when switching between different streamer modes or when phase coherence between operations is not required.

The mode word in Dest specifies the streamer configuration including pin assignments, data direction, and transfer format. The Src parameter provides either immediate data or a hub memory address depending on the mode configuration.


