# Instructions: E

This section contains all PASM2 instructions beginning with the letter E.



::: instrheader
## ENCOD {#encod}
Encode Bit Position

[Arithmetic Operations](#arithmetic-operations) - Returns the position of the highest set bit.
:::

**ENCOD**  *Dest, {#}Src*  **{WC|WZ|WCZ}**\
**ENCOD**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** The bit position value of the top-most high bit (1) in Src, or Dest, is stored in Dest.

- Dest is a register in which to store the encoded bit position value and optionally contains the 32-bit value to encode (syntax 2).
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is to be encoded into a bit position.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0111100 | CZI | DDDDDDDDD | SSSSSSSSS | S != 0 | result == 0 | D | 2 |
| EEEE | 0111100 | CZ0 | DDDDDDDDD | DDDDDDDDD | Original D != 0 | result == 0 | D | 2 |


**Related:** [DECOD](#decod)

**Explanation:**

ENCOD stores the bit position value (0-31) of the top-most high bit (1) of Src, or Dest, into Dest. The instruction scans from the most significant bit (bit 31) down to the least significant bit (bit 0) and returns the position of the first 1 bit encountered.

If the WC or WCZ effect is specified, the C flag is set (1) if Src (or original Dest in syntax 2) was not zero, or is cleared (0) if it was zero. This allows distinguishing between an input value of 1 (which encodes to 0) versus an input value of 0 (which also produces a result of 0).

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if not zero.

For example:

- `%00000000_00000000_00000000_00000001` encodes to 0 (bit position of the only 1)
- `%00000000_00000000_00000000_00100000` encodes to 5 (bit position 5 is the top-most 1)
- `%00000000_00000000_10000001_01000000` encodes to 15 (bit position 15 is the top-most 1)
- `%00000000_00000000_00000000_00000000` encodes to 0 with C flag cleared to 0

If the value to encode may be 0, use the WC or WCZ effect and check the resulting C flag to distinguish between the cases of input = 1 versus input = 0. Without this flag check, both cases would produce a Dest value of 0.

ENCOD is the complement of DECOD. Where DECOD converts a bit position (0-31) into a 32-bit value with a single bit set, ENCOD performs the reverse operation, converting a 32-bit value into the position of its highest set bit.



::: instrheader
## EXECF {#execf}
Execute with Skip Pattern

[Branching and Flow Control](#branching-and-flow-control) - Jumps to address with skip pattern for conditional execution.
:::

**EXECF**  *{#}Dest*

---

**Result:** PC is set to Dest[9:0] and the SKIPF pattern is set to Dest[31:10].

- Dest is a register or 10-bit literal specifying the target address in bits [9:0] and the skip pattern in bits [31:10].


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00I | DDDDDDDDD | 000110011 | --- | --- | --- | 4 |


**Related:** [CALL](#call), [SKIPF](#skipf), [SKIP](#skip)

**Explanation:**

EXECF performs a combined jump and skip pattern operation. The instruction sets the program counter (PC) to the 10-bit address specified in Dest[9:0] and simultaneously loads the SKIPF pattern register with the value from Dest[31:10].

The PC is set to the address formed by zero-extending Dest[9:0] to create a COG/LUT address: PC = {10'b0, Dest[9:0]}. This allows jumping to any location within the 1024-address COG/LUT memory space (addresses 0-511 for COG, 512-1023 for LUT).

The SKIPF pattern in Dest[31:10] provides a 22-bit pattern that controls which subsequent instructions will be skipped after the jump. Like SKIPF, this allows the PC to leap over instructions rather than cancelling them, providing fast conditional execution without the overhead of traditional branch instructions.

EXECF combines the functionality of CALL (jumping to a new address) and SKIPF (setting a skip pattern), enabling efficient implementation of computed branches with conditional execution. This is particularly useful for jump tables and state machines where both the target address and subsequent execution pattern need to be determined dynamically.

The instruction takes 4 clock cycles to execute, regardless of whether it executes from COG/LUT or Hub memory.



