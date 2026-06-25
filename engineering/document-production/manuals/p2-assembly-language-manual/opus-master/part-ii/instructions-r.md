# Instructions: R

This section contains all PASM2 instructions beginning with the letter R.



::: instrheader
## RCL {#rcl}
Rotate Carry Left

[Arithmetic Operations](#arithmetic-operations) - Shifts bits left, inserting carry flag as new LSBs.
:::

**RCL**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

**Operation:** `D = [63:32] of ({D, {32{C}}} << S[4:0])`; `C = last bit shifted out (S[4:0]>0) else D[31]`

**Result:** The bits of Dest are shifted left by Src bits, inserting C as new LSBs.

- Dest is a register containing the value to rotate carry left.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to rotate.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0000101 | CZI | DDDDDDDDD | SSSSSSSSS | Last bit out† | result == 0 | D | 2 |

† If S[4:0] > 0, C receives the last bit shifted out. If S[4:0] = 0 (no shift), C receives D[31].

**Related:** [RCR](#rcr), [ROL](#rol), [ROR](#ror)

**Explanation:**

RCL shifts Dest's binary value left by Src places (0-31 bits) and sets the new LSBs to C. The carry flag acts as an extension of the register, allowing 33-bit rotations.

If the WC or WCZ effect is specified, the C flag is updated to the value of the last bit shifted out if Src is 1-31, or to Dest[31] if Src is 0.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if non-zero.

This instruction is useful for multi-precision arithmetic operations where the carry from one word needs to be propagated into the next word.



::: instrheader
## RCR {#rcr}
Rotate Carry Right

[Arithmetic Operations](#arithmetic-operations) - Shifts bits right, inserting carry flag as new MSBs.
:::

**RCR**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

**Operation:** `D = [31:0] of ({{32{C}}, D} >> S[4:0])`; `C = last bit shifted out (S[4:0]>0) else D[0]`

**Result:** The bits of Dest are shifted right by Src bits, inserting C as new MSBs.

- Dest is a register containing the value to rotate carry right.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to rotate.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0000100 | CZI | DDDDDDDDD | SSSSSSSSS | Last bit out† | result == 0 | D | 2 |

† If S[4:0] > 0, C receives the last bit shifted out. If S[4:0] = 0 (no shift), C receives D[0].

**Related:** [RCL](#rcl), [ROL](#rol), [ROR](#ror)

**Explanation:**

RCR shifts Dest's binary value right by Src places (0-31 bits) and sets the new MSBs to C. The carry flag acts as an extension of the register, allowing 33-bit rotations.

If the WC or WCZ effect is specified, the C flag is updated to the value of the last bit shifted out if Src is 1-31, or to Dest[0] if Src is 0.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if non-zero.

This instruction is useful for multi-precision arithmetic operations where the carry needs to be propagated through multiple words.



::: instrheader
## RCZL {#rczl}
Rotate Carry And Zero Left

[Arithmetic Operations](#arithmetic-operations) - Shifts bits left by two, inserting C and Z as new LSBs.
:::

**RCZL**  *Dest*  **{WC|WZ|WCZ}**

**Operation:** `D = {D[29:0], C, Z}`; `C = D[31]`, `Z = D[30]`

**Result:** The bits of Dest are shifted left by two places and C and Z are inserted as new LSBs.

- Dest is a register containing the value to rotate.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 001101011 | D[31] | D[30] | D | 2 |


**Related:** [RCZR](#rczr), [RCL](#rcl), [RCR](#rcr)

**Explanation:**

RCZL shifts Dest's binary value left by two places and sets Dest[1] to C and Dest[0] to Z.

If the WC or WCZ effect is specified, the C flag is updated to the original Dest[31] state.

If the WZ or WCZ effect is specified, the Z flag is updated to the original Dest[30] state.

This instruction provides a compact way to shift two flag states into a register while simultaneously extracting two bits from the register into the flags, enabling efficient state serialization and deserialization.



::: instrheader
## RCZR {#rczr}
Rotate Carry And Zero Right

[Arithmetic Operations](#arithmetic-operations) - Shifts bits right by two, inserting C and Z as new MSBs.
:::

**RCZR**  *Dest*  **{WC|WZ|WCZ}**

**Operation:** `D = {C, Z, D[31:2]}`; `C = D[1]`, `Z = D[0]`

**Result:** The bits of Dest are shifted right by two places and C and Z are inserted as new MSBs.

- Dest is a register containing the value to rotate.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 001101010 | D[1] | D[0] | D | 2 |


**Related:** [RCZL](#rczl), [RCL](#rcl), [RCR](#rcr)

**Explanation:**

RCZR shifts Dest's binary value right by two places and sets Dest[31] to C and Dest[30] to Z.

If the WC or WCZ effect is specified, the C flag is updated to the original Dest[1] state.

If the WZ or WCZ effect is specified, the Z flag is updated to the original Dest[0] state.

This instruction provides a compact way to shift two flag states into a register while simultaneously extracting two bits from the register into the flags, enabling efficient state serialization and deserialization.



::: instrheader
## RDBYTE {#rdbyte}
Read Byte From hub

[hub memory Access](#hub-memory-access) - Reads a zero-extended byte from hub memory into a register.
:::

**RDBYTE**  *Dest, {#}Src/Ptr*  **{WC|WZ|WCZ}**

**Operation:** `D = zero-extend(hub byte)`; `C = byte[7]`

**Result:** A zero-extended byte from hub address Src or pointer (PTRA/PTRB) is loaded into Dest.

- Dest is the register to receive the byte value.
- Src/Ptr is a hub address from register, immediate value, or pointer register (PTRA/PTRB).
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010110 | CZI | DDDDDDDDD | SSSSSSSSS | MSB of byte | result == 0 | D | 9...16 † |

† **Timing varies by execution context:**

| Context | Clocks |
|:--------|:------:|
| Cog execution | 9...16 |
| Hub execution | 9...26 |
| Cog with interrupts | 9...24 |
| Hub with interrupts | 9...44 |


**Related:** [RDWORD](#rdword), [RDLONG](#rdlong), [WRBYTE](#wrbyte)

**Explanation:**

RDBYTE reads a byte from hub memory at the address specified by Src (or pointer register) and loads it into Dest with zero extension (bits 31:8 are cleared to 0). Timing depends on execution context: 9-16 cycles for cog execution, 9-26 for hub execution, with additional latency when interrupts are enabled (9-24 for cog, 9-44 for hub). The cog must wait for its hub access window.

If preceded by a SETQ instruction, burst reads of multiple bytes can be performed.

If the WC or WCZ effect is specified, C is set to the MSB of the byte.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.

Hub memory operations follow a round-robin access pattern where each cog gets a regular time slot. The actual latency depends on when the request arrives relative to the cog's assigned slot.



::: instrheader
## RDFAST {#rdfast}
Read Fast Via FIFO

[hub memory Access](#hub-memory-access) - Begins fast hub read operation via FIFO for high-throughput streaming.
:::

**RDFAST**  *{#}Dest, {#}Src*

**Result:** A fast read operation begins, filling the FIFO with data from hub memory starting at address Src.

- Dest is a configuration value: Dest[31] = no-wait mode, Dest[13:0] = block size in 64-byte units (0 = maximum).
- Src is the hub memory start address (Src[19:0]) for the read operation.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100011 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 or WRFAST finish + 10...17 † |

† **Timing varies by execution context:**

| Context | Clocks |
|:--------|:------:|
| Cog execution | 2 or WRFAST finish + 10...17 |
| Hub execution | *Not available—FIFO in use* |
| Cog with interrupts | 2 or WRFAST finish + 10...25 |
| Hub with interrupts | *Not available—FIFO in use* |

**Note:** FIFO operations require cog execution mode. When code runs from hub memory, the FIFO is used for instruction fetch and cannot be redirected for data streaming.


**Related:** [RFBYTE](#rfbyte), [RFWORD](#rfword), [RFLONG](#rflong), [WRFAST](#wrfast), [FBLOCK](#fblock)

**Explanation:**

RDFAST begins a new fast hub read operation via the FIFO. The instruction configures automatic sequential reading from hub memory with background FIFO refill, enabling high-throughput streaming data processing. This instruction is only available when executing from cog/LUT memory, not hub memory.

Dest[31] = 1 enables no-wait mode, which prevents stalls when the FIFO is being filled. Dest[13:0] specifies the block size in 64-byte units, with 0 indicating maximum size. Src[19:0] specifies the starting hub address. The FIFO automatically wraps at the block boundary.

After RDFAST is executed, subsequent RFBYTE, RFWORD, or RFLONG instructions read data from the FIFO. The FIFO is automatically refilled in the background, making this ideal for checksums, CRC calculations, data processing, and block copy operations.



::: instrheader
## RDLONG {#rdlong}
Read Long From hub

[hub memory Access](#hub-memory-access) - Reads a 32-bit long from hub memory into a register.
:::

**RDLONG**  *Dest, {#}Src/Ptr*  **{WC|WZ|WCZ}**

**Operation:** `D = hub long`; `C = long[31]` (prior SETQ/SETQ2 → block transfer)

**Result:** A long from hub address Src or pointer (PTRA/PTRB) is loaded into Dest.

- Dest is the register to receive the long value.
- Src/Ptr is a hub address from register, immediate value, or pointer register (PTRA/PTRB).
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011000 | CZI | DDDDDDDDD | SSSSSSSSS | MSB of long | result == 0 | D | 9...16 † |

† **Timing varies by execution context:**

| Context | Clocks |
|:--------|:------:|
| Cog execution | 9...16 |
| Hub execution | 9...26 |
| Cog with interrupts | 9...24 |
| Hub with interrupts | 9...44 |


**Related:** [RDBYTE](#rdbyte), [RDWORD](#rdword), [WRLONG](#wrlong)

**Explanation:**

RDLONG reads a long from hub memory at the address specified by Src (or pointer register) and loads it into Dest. Timing depends on execution context: 9-16 cycles for cog execution, 9-26 for hub execution, with additional latency when interrupts are enabled (9-24 for cog, 9-44 for hub). The cog must wait for its hub access window.

If preceded by a SETQ instruction, burst reads of multiple longs can be performed. Using SETQ2 instead of SETQ bursts the block into LUT RAM rather than cog RAM.

If the WC or WCZ effect is specified, C is set to the MSB of the long.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.

Hub memory operations follow a round-robin access pattern where each cog gets a regular time slot.

**Pitfall (Silicon Bug):** When using SETQ/SETQ2 for block transfers with PTRx expressions, do NOT place any ALTx, AUGS, or AUGD instruction between SETQ/SETQ2 and RDLONG. Such intervening instructions cancel the block-size PTRx delta calculation—the data transfers correctly, but PTRx advances by only a single-long delta (4 bytes) instead of the full block size. This leads to corrupted subsequent operations when code expects PTRx to point past the block.



::: instrheader
## RDLUT {#rdlut}
Read From LUT

[Lookup Table](#lookup-table) - Reads data from the cog's lookup table memory.
:::

**RDLUT**  *Dest, {#}Src/Ptr*  **{WC|WZ|WCZ}**

**Operation:** `D = LUT[S/PTRx]`; `C = data[31]`

**Result:** Data from LUT address Src or pointer (PTRA/PTRB) is loaded into Dest.

- Dest is the register to receive the data.
- Src/Ptr is a LUT address from register, immediate value, or pointer register (PTRA/PTRB).
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010101 | CZI | DDDDDDDDD | SSSSSSSSS | MSB of data | result == 0 | D | 3 |


**Related:** [WRLUT](#wrlut), [RDLONG](#rdlong)

**Explanation:**

RDLUT reads data from the Lookup Table at the address specified by Src (or pointer register) and loads it into Dest. The LUT is a 512-long (2KB) memory area in each cog that can be used for lookup tables, buffers, or general-purpose memory. The operation takes 3 clock cycles.

⚠️ **Pitfall:** A literal address (`RDLUT Dest, #addr`) reaches only LUT $000–$0FF (0–255); `#256` and above do not assemble (`Constant must be from 0 to 255`). Use a register, or a `PTRA`/`PTRB` pointer with an optional index, to reach any of the 512 LUT longs—the address field's top bit selects the pointer form, so a literal spans only 8 bits.

If the WC or WCZ effect is specified, C is set to the MSB of the data.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.

The LUT provides fast local memory access for frequently accessed data structures such as sin/cos tables, gamma correction tables, and small data buffers.



::: instrheader
## RDPIN {#rdpin}
Read smart pin

[Pin I/O and smart pins](#pin-io-and-smart-pins) - Reads smart pin result and acknowledges, clearing the ready flag.
:::

**RDPIN**  *Dest, {#}Src*  **{WC}**

**Operation:** `D = smart-pin S[5:0] result`, acknowledge pin; `C = modal result`

**Result:** Smart Pin Src[5:0] result is loaded into Dest, and the pin is acknowledged.

- Dest is the register to receive the pin result.
- Src is a register or literal identifying the pin number (Src[5:0]) to read from.
- WC is an optional effect to write the modal result to C.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010100 | C1I | DDDDDDDDD | SSSSSSSSS | Modal result | --- | D | 2 |


**Related:** [RQPIN](#rqpin), [WRPIN](#wrpin), [WXPIN](#wxpin), [WYPIN](#wypin)

**Explanation:**

RDPIN reads the result value from the specified smart pin and acknowledges the pin, clearing its "ready" flag. The result value depends on the pin's configured mode and represents measurement data such as pulse width, period, edge count, ADC value, or serial data.

If the WC effect is specified, the C flag is set to the modal result, which provides mode-specific status information.

Smart pins are autonomous I/O processors that can measure timing, count edges, perform A/D conversion, generate PWM, and communicate serially without continuous cog intervention. RDPIN retrieves the measured or received data after the pin signals completion.

Because RDPIN acknowledges the pin, it resets the pin's IN flag, and the smart pin needs about 2 clock cycles to clear that flag before a TESTP poll of IN reads a valid result. Insert two NOP instructions (or other unrelated work) between RDPIN and the TESTP that polls the IN flag. RQPIN does not acknowledge the pin and so does not reset the IN flag, so no such delay is needed after RQPIN.



::: instrheader
## RDWORD {#rdword}
Read Word From hub

[hub memory Access](#hub-memory-access) - Reads a zero-extended word from hub memory into a register.
:::

**RDWORD**  *Dest, {#}Src/Ptr*  **{WC|WZ|WCZ}**

**Operation:** `D = zero-extend(hub word)`; `C = word[15]`

**Result:** A zero-extended word from hub address Src or pointer (PTRA/PTRB) is loaded into Dest.

- Dest is the register to receive the word value.
- Src/Ptr is a hub address from register, immediate value, or pointer register (PTRA/PTRB).
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010111 | CZI | DDDDDDDDD | SSSSSSSSS | MSB of word | result == 0 | D | 9...16 † |

† **Timing varies by execution context:**

| Context | Clocks |
|:--------|:------:|
| Cog execution | 9...16 |
| Hub execution | 9...26 |
| Cog with interrupts | 9...24 |
| Hub with interrupts | 9...44 |


**Related:** [RDBYTE](#rdbyte), [RDLONG](#rdlong), [WRWORD](#wrword)

**Explanation:**

RDWORD reads a word from hub memory at the address specified by Src (or pointer register) and loads it into Dest with zero extension (bits 31:16 are cleared to 0). Timing depends on execution context: 9-16 cycles for cog execution, 9-26 for hub execution, with additional latency when interrupts are enabled (9-24 for cog, 9-44 for hub). The cog must wait for its hub access window.

If preceded by a SETQ instruction, burst reads of multiple words can be performed.

If the WC or WCZ effect is specified, C is set to the MSB of the word.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.



::: instrheader
## REP {#rep}
Repeat Block

[Branching and Flow Control](#branching-and-flow-control) - Creates a zero-overhead hardware loop for repeated execution.
:::

**REP**  *{#}Dest, {#}Src*

**REP**  *@.label, {#}Src*

**Operation:** repeat the next `D[8:0]` instructions `S` times (S = 0 → forever; D[8:0] = 0 → none)

**Result:** The next Dest[8:0] instructions are executed Src times.

- Dest is the number of instructions to repeat (Dest[8:0], 0-511). If Dest[8:0] = 0, nothing repeats.
- Src is the number of repetitions. If Src = 0, instructions repeat infinitely.
- Alternatively, `@.label` calculates the instruction count automatically from a local label.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100110 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 |


**Related:** [DJNZ](#djnz), [JNCT1/2/3](#jnct1)

**Explanation:**

REP creates a hardware-implemented loop that executes the next Dest[8:0] instructions Src times. If Src = 0, the instructions repeat infinitely (useful for main loops). If Dest[8:0] = 0, nothing repeats.

The REP instruction itself takes 2 cycles, and the repeated instructions execute with zero overhead—no jump penalty, no counter decrement. This makes REP ideal for time-critical inner loops.

REP blocks cannot be nested. The P2 hardware uses a single internal counter for REP execution; starting a new REP while one is active overwrites the existing repeat state. For nested iteration, use REP for the inner loop and branch instructions (DJNZ) for outer loops. Interrupts are blocked during REP execution to maintain timing precision. REP adds no per-iteration overhead, so it suits tight timing-critical loops.

**Critical Restrictions:**

- **Branches cancel REP:** Any branch instruction (JMP, CALL, DJNZ, TJZ, etc.) executed within the repeated block immediately cancels REP activity. The branch executes normally, but repetition stops. This includes conditional branches that are taken.

- **Hub memory overhead:** When REP executes from hub memory (ORGH section), it remains functional but is no longer zero-overhead: each iteration's hidden return-jump pays the hub-branch refill cost. For zero-overhead inner loops, execute REP from cog or LUT memory; for non-time-critical loops, hub-exec REP works correctly with this per-iteration penalty.

**Forbidden instructions in REP blocks:**
- Branch instructions: JMP, CALL, CALLA, CALLB, CALLD
- Conditional branches: DJNZ, DJZ, TJZ, TJNZ, IJZ, IJNZ
- Any instruction that modifies PC

**Using Labels Instead of Counts:**

The `@.label` syntax enables REP to automatically calculate the instruction count from a local label placed after the repeated block. The assembler computes the distance between REP and the label at assembly time. This approach is preferred over hardcoded counts because it remains correct when instructions are added or removed.

**Example using instruction count (fragile):**
```pasm2
' Hardcoded count - breaks if code changes
                rep     #3, count               ' Repeat next 3 instructions
                rdlong  x, ptr                  ' 1st
                add     ptr, #4                 ' 2nd
                add     sum, x                  ' 3rd
                ' If you add code here, the count becomes wrong!
```

**Example using local label (preferred):**
```pasm2
' Label-based count - automatically correct
process_data    rep     @.end, count            ' Repeat until .end label
                rdlong  x, ptr                  ' Instructions between REP
                add     ptr, #4                 ' and label are counted
                add     sum, x                  ' automatically
.end                                            ' Empty label marks end

' Alternative using the # prefix with local label:
fill_buffer     rep     #(.done - $), #256      ' Expression = count
                wrbyte  value, ptr
                add     ptr, #1
.done
```

**Pitfall:** When using the label form, place the label immediately after the last repeated instruction. The label must be within the same local scope (same enclosing global label). See Chapter 2.10 for label scoping rules.

**Extended Count Capability:**

Both the instruction count (D) and repetition count (S) can exceed the 9-bit immediate limit of 0-511 using two methods:

| Form | Limit | Mechanism |
|------|-------|-----------|
| `#count` | 0-511 | 9-bit immediate field |
| `##count` | 0 to 2^32-1 | AUGD/AUGS prefix emitted automatically |
| `register` | 0 to 2^32-1 | Register value used at runtime |

```pasm2
' Extended repetition examples
                rep     @.end, ##1000         ' 1000 reps (AUGS prefix)
                rep     @.end, big_count      ' Register-based count
                rep     ##1000, ##2000        ' Both extended (rare)
```

**Memory Mode Constraints (for @label form):**

The `@label` end position is constrained by both the execution mode and the 9-bit encoding limit:

| Memory Mode | Address Range | @label Constraint |
|-------------|---------------|-------------------|
| Cog only | $000-$1FF | min(511 instructions, $1FF - current) |
| Cog + LUT | $000-$3FF | min(511 instructions, $3FF - current) |
| LUT only | $200-$3FF | min(511 instructions, $3FF - current) |
| Hub (ORGH) | $00000-$7FFFF | 511 instructions (encoding limit) |

REP blocks can span from cog RAM into LUT RAM when executing in combined cog+LUT mode.

**Interrupt Protection Pattern:**

A common PASM2 idiom uses REP with repetition count = 1 to stall interrupts during critical operations. (Note: This pattern is only needed in PASM2 code with interrupts enabled; Spin2 operators are already protected by the interpreter.)

```pasm2
' Protect CORDIC operation from interrupts
                rep     @.stall, #1           ' Run block once, atomically
                qmul    y, x                  ' CORDIC multiply
                getqx   x                     ' Get result
                getqy   y                     ' Get overflow
.stall
```

This works because REP stalls interrupt handling until all repeated instructions complete, even with just one iteration.

**Extended Interrupt Stall:**

For longer critical sequences, use a large instruction count with repetition = 1:

```pasm2
' Stall interrupts until ret/_ret_ is encountered
op_quna         rep     #99, #1               ' Large count, exits on ret
                qsqrt   x, #0                 ' CORDIC operations...
                qlog    x
                qexp    x
                ...
        _ret_   mov     result, x             ' REP ends at _ret_
```

The large instruction count (99) with repetition count of 1 creates an interrupt-free zone that terminates at the first `ret`, `_ret_`, or branch instruction.

**Conditional REP:**

REP itself can be conditionally executed:

```pasm2
                testp   pin                   wc
    if_c        rep     @.end, #5             ' Only repeat if C set
                add     sum, #1
.end
```

Instructions within the REP block can also be conditional:

```pasm2
                rep     @.end, #4
                add     sum, #1
                test    sum, #1               wz
    if_z        add     result, #1            ' Conditional within block
.end
```

**Bit-Bang I2C Pattern:**

```pasm2
' Output 8 bits, MSB first
.wr_byte        rep     #8, #8                ' 8 instructions, 8 times
                shl     data, #1              wc
                drvc    sda                   ' Drive SDA with carry
                drvh    scl                   ' Clock high
                waitx   delay
                drvl    scl                   ' Clock low
                waitx   delay
                nop
                nop
```

**Array Operations:**

```pasm2
' Fill array with incrementing values
                mov     counter, #0
                loc     ptra, #\hub_array
                rep     @.arr_end, #8
                add     counter, #1
                wrlong  counter, ptra++
.arr_end
```


::: instrheader
## RESI0 / RESI1 / RESI2 / RESI3 {#resi0}
Resume From Interrupt

[Interrupts](#interrupts) - Resumes execution from an interrupted location.
:::

\hypertarget{resi1}{}\hypertarget{resi2}{}\hypertarget{resi3}{}

**RESI0**
**RESI1**
**RESI2**
**RESI3**

**Result:** Execution resumes from the interrupted location for the specified interrupt level.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011001 | 110 | 111111110 | 111111111 | --- | --- | --- | 4 (Cog), 13...20 (Hub) |
| EEEE | 1011001 | 110 | 111110100 | 111110101 | --- | --- | --- | 4 (Cog), 13...20 (Hub) |
| EEEE | 1011001 | 110 | 111110010 | 111110011 | --- | --- | --- | 4 (Cog), 13...20 (Hub) |
| EEEE | 1011001 | 110 | 111110000 | 111110001 | --- | --- | --- | 4 (Cog), 13...20 (Hub) |


**Related:** [RETI0/1/2/3](#reti0), [SETINT1/2/3](#setint1), [NIXINT1/2/3](#nixint1)

**Explanation:**

RESI0, RESI1, RESI2, and RESI3 resume execution from their respective interrupt levels. Each instruction is functionally equivalent to a CALLD instruction that restores the program counter, C flag, and Z flag from the corresponding interrupt return address registers.

Unlike RETIx instructions which return from the interrupt handler, RESIx instructions resume interrupted execution, used when an interrupt handler needs to yield to another interrupt priority level before completion.



::: instrheader
## RET {#ret}
Return From Subroutine

[Branching and Flow Control](#branching-and-flow-control) - Returns from subroutine by popping the hardware stack.
:::

**RET**  **{WC|WZ|WCZ}**

**Operation:** pop K from stack; `C = K[31]`, `Z = K[30]`, `PC = K[19:0]`

**Result:** The program counter, C flag, and Z flag are restored from the top of the hardware stack.

- WC, WZ, or WCZ are optional effects to restore flags from the stack.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ1 | 000000000 | 000101101 | K[31] | K[30] | --- | 4 / 13-20 † |

† **Timing varies by execution context:**

| Context | Clocks |
|:--------|:------:|
| Cog / LUT execution | 4 |
| Hub execution | 13...20 |


**Related:** [CALL](#call), [CALLA](#calla), [CALLB](#callb), [RETA](#reta), [RETB](#retb)

**Explanation:**

RET returns from a subroutine by popping the hardware stack (K register). The program counter is restored from K[19:0].

If the WC or WCZ effect is specified, the C flag is restored from K[31].

If the WZ or WCZ effect is specified, the Z flag is restored from K[30].

The operation takes 4 cycles in cog/LUT execution, or 13–20 cycles in hub execution (the hub-branch refill cost when the return target resides in hub memory).

The P2 provides an 8-level hardware stack for fast subroutine calls. RET is paired with CALL, CALLPA, CALLPB, CALLA, and CALLB instructions.



::: instrheader
## RETA {#reta}
Return Via PTRA Stack

[Branching and Flow Control](#branching-and-flow-control) - Returns from subroutine using PTRA as software stack pointer.
:::

**RETA**  **{WC|WZ|WCZ}**

**Operation:** `L = hub[--PTRA]`; `C = L[31]`, `Z = L[30]`, `PC = L[19:0]`

**Result:** The program counter, C flag, and Z flag are restored from hub memory at --PTRA.

- WC, WZ, or WCZ are optional effects to restore flags from the stack.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ1 | 000000000 | 000101110 | L[31] | L[30] | --- | 11...18 † |

† **Timing varies by execution context:**

| Context | Clocks |
|:--------|:------:|
| Cog execution | 11...18 |
| Hub execution | 20...40 |
| Cog with interrupts | 11...26 |
| Hub with interrupts | 20...70 |

**Related:** [CALLA](#calla), [RET](#ret), [RETB](#retb)

**Explanation:**

RETA returns from a subroutine by reading a hub long from --PTRA. PTRA is pre-decremented by 4 bytes, then a long is read from that address. The program counter is restored from L[19:0].

If the WC or WCZ effect is specified, the C flag is restored from L[31].

If the WZ or WCZ effect is specified, the Z flag is restored from L[30].

RETA is paired with CALLA for implementing software stacks in hub memory, enabling deep call nesting beyond the 8-level hardware stack limit.



::: instrheader
## RETB {#retb}
Return Via PTRB Stack

[Branching and Flow Control](#branching-and-flow-control) - Returns from subroutine using PTRB as software stack pointer.
:::

**RETB**  **{WC|WZ|WCZ}**

**Operation:** `L = hub[--PTRB]`; `C = L[31]`, `Z = L[30]`, `PC = L[19:0]`

**Result:** The program counter, C flag, and Z flag are restored from hub memory at --PTRB.

- WC, WZ, or WCZ are optional effects to restore flags from the stack.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ1 | 000000000 | 000101111 | L[31] | L[30] | --- | 11...18 † |

† **Timing varies by execution context:**

| Context | Clocks |
|:--------|:------:|
| Cog execution | 11...18 |
| Hub execution | 20...40 |
| Cog with interrupts | 11...26 |
| Hub with interrupts | 20...70 |

**Related:** [CALLB](#callb), [RET](#ret), [RETA](#reta)

**Explanation:**

RETB returns from a subroutine by reading a hub long from --PTRB. PTRB is pre-decremented by 4 bytes, then a long is read from that address. The program counter is restored from L[19:0].

If the WC or WCZ effect is specified, the C flag is restored from L[31].

If the WZ or WCZ effect is specified, the Z flag is restored from L[30].

RETB is paired with CALLB for implementing software stacks in hub memory, enabling deep call nesting beyond the 8-level hardware stack limit.



::: instrheader
## RETI0 / RETI1 / RETI2 / RETI3 {#reti0}
Return From Interrupt

[Interrupts](#interrupts) - Returns from interrupt handler to interrupted location.
:::

\hypertarget{reti1}{}\hypertarget{reti2}{}\hypertarget{reti3}{}

**RETI0**
**RETI1**
**RETI2**
**RETI3**

**Result:** Execution returns from the specified interrupt level to the interrupted location.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011001 | 110 | 111111111 | 111111111 | --- | --- | --- | 4 (Cog), 13...20 (Hub) |
| EEEE | 1011001 | 110 | 111111111 | 111110101 | --- | --- | --- | 4 (Cog), 13...20 (Hub) |
| EEEE | 1011001 | 110 | 111111111 | 111110011 | --- | --- | --- | 4 (Cog), 13...20 (Hub) |
| EEEE | 1011001 | 110 | 111111111 | 111110001 | --- | --- | --- | 4 (Cog), 13...20 (Hub) |


**Related:** [RESI0/1/2/3](#resi0), [SETINT1/2/3](#setint1), [NIXINT1/2/3](#nixint1)

**Explanation:**

RETI0, RETI1, RETI2, and RETI3 return from their respective interrupt handlers. Each instruction is functionally equivalent to a CALLD instruction that restores the program counter, C flag, and Z flag from the corresponding interrupt return address registers.

The P2 provides four interrupt levels (INT0-INT3), with INT0 being the lowest priority and INT3 being the highest. Each RETI instruction completes its interrupt handler and resumes normal execution at the point where the interrupt occurred.



::: instrheader
## REV {#rev}
Reverse Bits

[Arithmetic Operations](#arithmetic-operations) - Reverses all 32 bits in a register.
:::

**REV**  *Dest*

**Operation:** `D = D[0:31]` (bit-reverse)

**Result:** The 32-bit pattern in Dest is reversed (bits 31:0 become bits 0:31).

- Dest is the register containing the bit pattern to reverse.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001101001 | --- | --- | D | 2 |


**Related:** [ROL](#rol), [ROR](#ror), [ZEROX](#zerox)

**Explanation:**

REV performs a complete bitwise reverse of the value in Dest, storing the result back into Dest. Bit 31 becomes bit 0, bit 30 becomes bit 1, and so on through bit 0 becoming bit 31. The operation takes 2 cycles and does not affect any flags.

This instruction is useful for processing binary data in different MSB/LSB order than it is transmitted with, such as serial protocols that send least-significant bit first but need processing in most-significant bit first order. It is also used in bit-reversal algorithms for FFT operations.



::: instrheader
## RFBYTE {#rfbyte}
Read Byte Via FIFO

[hub memory Access](#hub-memory-access) - Reads a zero-extended byte from the RDFAST FIFO.
:::

**RFBYTE**  *Dest*  **{WC|WZ|WCZ}**

**Operation:** `D = zero-extend(FIFO byte)`; `C = byte[7]`

**Result:** A zero-extended byte from the FIFO is loaded into Dest.

- Dest is the register to receive the byte value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000010000 | MSB of byte | result == 0 | D | 2 |


**Related:** [RDFAST](#rdfast), [RFWORD](#rfword), [RFLONG](#rflong), [RFVAR](#rfvar)

**Explanation:**

RFBYTE is used after RDFAST to read zero-extended bytes from the FIFO. The byte is loaded into Dest with bits 31:8 cleared to 0.

If the WC or WCZ effect is specified, C is set to the MSB of the byte.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.

The operation takes 2 cycles when the FIFO has data available. The FIFO is automatically refilled in the background by the RDFAST operation.



::: instrheader
## RFLONG {#rflong}
Read Long Via FIFO

[hub memory Access](#hub-memory-access) - Reads a 32-bit long from the RDFAST FIFO.
:::

**RFLONG**  *Dest*  **{WC|WZ|WCZ}**

**Operation:** `D = FIFO long`; `C = long[31]`

**Result:** A long from the FIFO is loaded into Dest.

- Dest is the register to receive the long value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000010010 | MSB of long | result == 0 | D | 2 |


**Related:** [RDFAST](#rdfast), [RFBYTE](#rfbyte), [RFWORD](#rfword), [RFVAR](#rfvar)

**Explanation:**

RFLONG is used after RDFAST to read longs from the FIFO.

If the WC or WCZ effect is specified, C is set to the MSB of the long.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.

The operation takes 2 cycles when the FIFO has data available. The FIFO is automatically refilled in the background by the RDFAST operation.



::: instrheader
## RFVAR {#rfvar}
Read Variable Via FIFO

[hub memory Access](#hub-memory-access) - Reads a zero-extended 1-4 byte value from the RDFAST FIFO.
:::

**RFVAR**  *Dest*  **{WC|WZ|WCZ}**

**Operation:** `D = zero-extend(FIFO 1..4-byte value)`; `C = 0`

**Result:** A zero-extended 1-4 byte value from the FIFO is loaded into Dest.

- Dest is the register to receive the variable-length value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000010011 | 0 | result == 0 | D | 2 |


**Related:** [RDFAST](#rdfast), [RFBYTE](#rfbyte), [RFVARS](#rfvars)

**Explanation:**

RFVAR is used after RDFAST to read variable-length values (1-4 bytes) from the FIFO with zero extension. The value is loaded into Dest with upper bits cleared to 0.

If the WC or WCZ effect is specified, C is always cleared to 0.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.

The length of each value read is determined by the streamer configuration set up before the RDFAST operation.



::: instrheader
## RFVARS {#rfvars}
Read Signed Variable Via FIFO

[hub memory Access](#hub-memory-access) - Reads a sign-extended 1-4 byte value from the RDFAST FIFO.
:::

**RFVARS**  *Dest*  **{WC|WZ|WCZ}**

**Operation:** `D = sign-extend(FIFO 1..4-byte value)`; `C = value MSB`

**Result:** A sign-extended 1-4 byte value from the FIFO is loaded into Dest.

- Dest is the register to receive the sign-extended value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000010100 | MSB of value | result == 0 | D | 2 |


**Related:** [RDFAST](#rdfast), [RFVAR](#rfvar), [RFBYTE](#rfbyte)

**Explanation:**

RFVARS is used after RDFAST to read variable-length values (1-4 bytes) from the FIFO with sign extension. The value is loaded into Dest with upper bits set according to the MSB of the value (sign extension).

If the WC or WCZ effect is specified, C is set to the MSB of the value.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.



::: instrheader
## RFWORD {#rfword}
Read Word Via FIFO

[hub memory Access](#hub-memory-access) - Reads a zero-extended word from the RDFAST FIFO.
:::

**RFWORD**  *Dest*  **{WC|WZ|WCZ}**

**Operation:** `D = zero-extend(FIFO word)`; `C = word[15]`

**Result:** A zero-extended word from the FIFO is loaded into Dest.

- Dest is the register to receive the word value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000010001 | MSB of word | result == 0 | D | 2 |


**Related:** [RDFAST](#rdfast), [RFBYTE](#rfbyte), [RFLONG](#rflong), [RFVAR](#rfvar)

**Explanation:**

RFWORD is used after RDFAST to read zero-extended words from the FIFO. The word is loaded into Dest with bits 31:16 cleared to 0.

If the WC or WCZ effect is specified, C is set to the MSB of the word.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.

The operation takes 2 cycles when the FIFO has data available.



::: instrheader
## RGBEXP {#rgbexp}
Expand RGB Color

[Color Space and Pixel Operations](#color-space-and-pixel-operations) - Expands 5:6:5 RGB color to 8:8:8 format.
:::

**RGBEXP**  *Dest*

**Operation:** `D = {D[15:11,15:13], D[10:5,10:9], D[4:0,4:2], 8'b0}` (5:6:5 → 8:8:8)

**Result:** The 5:6:5 RGB value in Dest[15:0] is expanded into 8:8:8 format in Dest[31:8].

- Dest contains 5:6:5 RGB in Dest[15:0], receives 8:8:8 RGB in Dest[31:8].


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001100111 | --- | --- | D | 2 |


**Related:** [RGBSQZ](#rgbsqz)

**Explanation:**

RGBEXP expands a compact 5:6:5 RGB color value (commonly used in 16-bit color displays) into full 8:8:8 RGB format (24-bit true color). The input 5:6:5 value is in Dest[15:0] with 5 bits red, 6 bits green, and 5 bits blue. The output 8:8:8 value is placed in Dest[31:8] with 8 bits each for red, green, and blue. The expansion replicates the most significant bits into the lower bits to maintain color accuracy.

This instruction is useful when converting between 16-bit and 24-bit color formats for graphics processing.



::: instrheader
## RGBSQZ {#rgbsqz}
Squeeze RGB Color

[Color Space and Pixel Operations](#color-space-and-pixel-operations) - Compresses 8:8:8 RGB color to 5:6:5 format.
:::

**RGBSQZ**  *Dest*

**Operation:** `D = {15'b0, D[31:27], D[23:18], D[15:11]}` (8:8:8 → 5:6:5)

**Result:** The 8:8:8 RGB value in Dest[31:8] is compressed into 5:6:5 format in Dest[15:0].

- Dest contains 8:8:8 RGB in Dest[31:8], receives 5:6:5 RGB in Dest[15:0].


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001100110 | --- | --- | D | 2 |


**Related:** [RGBEXP](#rgbexp)

**Explanation:**

RGBSQZ compresses a full 8:8:8 RGB color value (24-bit true color) into compact 5:6:5 format (16-bit color). The input 8:8:8 value is in Dest[31:8] with 8 bits each for red, green, and blue. The output 5:6:5 value is placed in Dest[15:0] with 5 bits red, 6 bits green, and 5 bits blue. The compression keeps the most significant bits of each color channel.

This instruction is useful when converting from 24-bit to 16-bit color formats for display output.



::: instrheader
## ROL {#rol}
Rotate Left

[Arithmetic Operations](#arithmetic-operations) - Rotates bits left, wrapping MSBs to LSBs.
:::

**ROL**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

**Operation:** `D = [63:32] of ({D, D} << S[4:0])`; `C = last bit shifted out (S[4:0]>0) else D[31]`

**Result:** The bits of Dest are rotated left by Src positions; departing MSBs are moved into LSBs.

- Dest is the register containing the value to rotate left.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to rotate.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0000001 | CZI | DDDDDDDDD | SSSSSSSSS | Last bit out† | result == 0 | D | 2 |

† If S[4:0] > 0, C receives the last bit shifted out. If S[4:0] = 0 (no shift), C receives D[31].

**Related:** [ROR](#ror), [RCL](#rcl), [RCR](#rcr), [SHL](#shl)

**Explanation:**

ROL rotates Dest's binary value left by Src places (0-31 bits). All MSBs rotated out are moved into the new LSBs.

If the WC or WCZ effect is specified, the C flag is updated to the value of the last bit rotated out if Src is 1-31, or to Dest[31] if Src is 0.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if non-zero. Since no bits are lost by this operation, the result will only be zero if Dest started at zero.

Rotation is useful for bit manipulation, circular buffers, hash functions, and cryptographic operations.



::: instrheader
## ROLBYTE {#rolbyte}
Rotate Byte Left Into register

[Arithmetic Operations](#arithmetic-operations) - Rotates a byte from source into destination register.
:::

**ROLBYTE**  *Dest, {#}Src, #N*\
**ROLBYTE**  *Dest*

**Operation:** `D = {D[23:0], S.BYTE[N]}`

**Result:** Byte N (0-3) of Src, or a byte from a source described by prior ALTGB instruction, is rotated left into Dest.

- Dest is the register into which the byte is rotated.
- Src is a register, 9-bit literal, or 32-bit augmented literal containing the target byte.
- N is a 2-bit literal (0-3) identifying the byte position in Src.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001000 | NNI | DDDDDDDDD | SSSSSSSSS | --- | --- | D | 2 |
| EEEE | 1001000 | 000 | DDDDDDDDD | 000000000 | --- | --- | D | 2 |


**Related:** [ROLNIB](#rolnib), [ROLWORD](#rolword), [GETBYTE](#getbyte), [SETBYTE](#setbyte), [ALTGB](#altgb)

**Explanation:**

ROLBYTE reads the byte identified by N (0-3) from Src, or a byte from the source described by a prior ALTGB instruction, and rotates it left into Dest. ROLBYTE achieves the same effect as two instructions: an 8-bit SHL followed by SETBYTE into byte 0.

The second syntax form is intended for use after an ALTGB instruction in a loop to iteratively read a series of byte values within contiguous long registers.



::: instrheader
## ROLNIB {#rolnib}
Rotate Nibble Left Into register

[Arithmetic Operations](#arithmetic-operations) - Rotates a nibble from source into destination register.
:::

**ROLNIB**  *Dest, {#}Src, #N*\
**ROLNIB**  *Dest*

**Operation:** `D = {D[27:0], S.NIBBLE[N]}`

**Result:** Nibble N (0-7) of Src, or a nibble from a source described by prior ALTGN instruction, is rotated left into Dest.

- Dest is the register into which the nibble is rotated.
- Src is a register, 9-bit literal, or 32-bit augmented literal containing the target nibble.
- N is a 3-bit literal (0-7) identifying the nibble position in Src.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 100010N | NNI | DDDDDDDDD | SSSSSSSSS | --- | --- | D | 2 |
| EEEE | 1000100 | 000 | DDDDDDDDD | 000000000 | --- | --- | D | 2 |


**Related:** [ROLBYTE](#rolbyte), [ROLWORD](#rolword), [GETNIB](#getnib), [SETNIB](#setnib), [ALTGN](#altgn)

**Explanation:**

ROLNIB reads the nibble identified by N (0-7) from Src, or a nibble from the source described by a prior ALTGN instruction, and rotates it left into Dest. ROLNIB achieves the same effect as two instructions: a 4-bit SHL followed by SETNIB into nibble 0.

The second syntax form is intended for use after an ALTGN instruction in a loop to iteratively read a series of nibble values within contiguous long registers.



::: instrheader
## ROLWORD {#rolword}
Rotate Word Left Into register

[Arithmetic Operations](#arithmetic-operations) - Rotates a word from source into destination register.
:::

**ROLWORD**  *Dest, {#}Src, #N*\
**ROLWORD**  *Dest*

**Operation:** `D = {D[15:0], S.WORD[N]}`

**Result:** Word N (0-1) of Src, or a word from a source described by prior ALTGW instruction, is rotated left into Dest.

- Dest is the register into which the word is rotated.
- Src is a register, 9-bit literal, or 32-bit augmented literal containing the target word.
- N is a 1-bit literal (0-1) identifying the word position in Src.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001010 | 0NI | DDDDDDDDD | SSSSSSSSS | --- | --- | D | 2 |
| EEEE | 1001010 | 000 | DDDDDDDDD | 000000000 | --- | --- | D | 2 |


**Related:** [ROLBYTE](#rolbyte), [ROLNIB](#rolnib), [GETWORD](#getword), [SETWORD](#setword), [ALTGW](#altgw)

**Explanation:**

ROLWORD reads the word identified by N (0-1) from Src, or a word from the source described by a prior ALTGW instruction, and rotates it left into Dest. ROLWORD achieves the same effect as two instructions: a 16-bit SHL followed by SETWORD into word 0.

The second syntax form is intended for use after an ALTGW instruction in a loop to iteratively read a series of word values within contiguous long registers.



::: instrheader
## ROR {#ror}
Rotate Right

[Arithmetic Operations](#arithmetic-operations) - Rotates bits right, wrapping LSBs to MSBs.
:::

**ROR**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

**Operation:** `D = [31:0] of ({D, D} >> S[4:0])`; `C = last bit shifted out (S[4:0]>0) else D[0]`

**Result:** The bits of Dest are rotated right by Src positions; departing LSBs are moved into MSBs.

- Dest is the register containing the value to rotate right.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to rotate.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0000000 | CZI | DDDDDDDDD | SSSSSSSSS | Last bit out† | result == 0 | D | 2 |

† If S[4:0] > 0, C receives the last bit shifted out. If S[4:0] = 0 (no shift), C receives D[0].

**Related:** [ROL](#rol), [RCL](#rcl), [RCR](#rcr), [SHR](#shr)

**Explanation:**

ROR rotates Dest's binary value right by Src places (0-31 bits). All LSBs rotated out are moved into the new MSBs.

If the WC or WCZ effect is specified, the C flag is updated to the value of the last bit rotated out if Src is 1-31, or to Dest[0] if Src is 0.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if non-zero. Since no bits are lost by this operation, the result will only be zero if Dest started at zero.

Rotation is useful for bit manipulation, circular buffers, hash functions, and cryptographic operations.



::: instrheader
## RQPIN {#rqpin}
Read Smart Pin Without Acknowledge

[Pin I/O and smart pins](#pin-io-and-smart-pins) - Reads smart pin result without clearing the ready flag.
:::

**RQPIN**  *Dest, {#}Src*  **{WC}**

**Operation:** `D = smart-pin S[5:0] result` (no ack — "quiet"); `C = modal result`

**Result:** Smart Pin Src[5:0] result is loaded into Dest without clearing the pin's ready flag.

- Dest is the register to receive the pin result.
- Src is a register or literal identifying the pin number (Src[5:0]) to read from.
- WC is an optional effect to write the modal result to C.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010100 | C0I | DDDDDDDDD | SSSSSSSSS | Modal result | --- | D | 2 |


**Related:** [RDPIN](#rdpin), [WRPIN](#wrpin), [WXPIN](#wxpin), [WYPIN](#wypin)

**Explanation:**

RQPIN reads the result value from the specified smart pin without acknowledging the pin. Unlike RDPIN, this instruction does not clear the pin's "ready" flag, allowing the same result to be read multiple times or checked before being consumed.

If the WC effect is specified, the C flag is set to the modal result, which provides mode-specific status information.

This instruction is useful for checking a pin's result value without consuming it, such as polling for completion before actually processing the result.


