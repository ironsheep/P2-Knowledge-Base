# PASM2 Instruction Encoding Reference (for disassembly)

**Generated from** `deliverables/ai/P2/language/pasm2/*.yaml` — the per-instruction
knowledge-base YAMLs. Regenerate with `engineering/tools/gen-pasm2-encoding-reference.py`.
One row per instruction;
the **Encoding** column is the authoritative 32-bit bit pattern.

## How to read the encoding

Each instruction word is 32 bits, written MSB→LSB as space-separated fields:

| Field | Bits | Meaning |
|-------|------|---------|
| `EEEE` | 31..28 | Condition code (execute-if); `1111` = always. |
| opcode | 27..21 (typically 7 bits) | Fixed instruction-selector bits — the primary decode key. |
| `C` `Z` `I` (`CZI`) | per instruction | C-effect (WC), Z-effect (WZ), and I = immediate-S select. Some instructions use `L` for immediate-D, or repurpose these bits. |
| `DDDDDDDDD` | 9 bits | Destination register (or 9-bit immediate when `L`=1, or a sub-opcode/field). |
| `SSSSSSSSS` | 9 bits | Source register (or 9-bit immediate when `I`=1, or a sub-opcode/field). |

> Literal `0`/`1` digits in a pattern are fixed opcode bits — match these to decode.
> Letter runs (`D`, `S`, `A`, `R`, `N`, `W`, etc.) are operand/field bits. Branch and
> augment instructions replace `D`/`S` with wide immediate fields (e.g. `AAAAAAAAA`
> address bits, 23-bit `AUGS`/`AUGD` literals); the pattern shown is exact per instruction.

## Condition codes (`EEEE`, bits 31..28)

The 4-bit `EEEE` prefix selects conditional execution (sourced from
`language/pasm2/concepts/conditional_execution.yaml`):

| EEEE | Mnemonic | Condition | Aliases |
|------|----------|-----------|---------|
| `0000` | _RET_ | Always + Return | IF_RET |
| `0001` | IF_NC_AND_NZ | C=0 AND Z=0 | IF_NZ_AND_NC, IF_A, IF_GT, IF_00 |
| `0010` | IF_NC_AND_Z | C=0 AND Z=1 | IF_Z_AND_NC, IF_01 |
| `0011` | IF_NC | C=0 | IF_AE, IF_GE, IF_0X |
| `0100` | IF_C_AND_NZ | C=1 AND Z=0 | IF_NZ_AND_C, IF_10 |
| `0101` | IF_NZ | Z=0 | IF_NE, IF_X0 |
| `0110` | IF_C_NE_Z | C≠Z | IF_DIFF, IF_Z_NE_C |
| `0111` | IF_NC_OR_NZ | C=0 OR Z=0 | IF_NZ_OR_NC, IF_NOT_11 |
| `1000` | IF_C_AND_Z | C=1 AND Z=1 | IF_Z_AND_C, IF_11 |
| `1001` | IF_C_EQ_Z | C=Z | IF_SAME, IF_Z_EQ_C |
| `1010` | IF_Z | Z=1 | IF_E, IF_X1 |
| `1011` | IF_NC_OR_Z | C=0 OR Z=1 | IF_Z_OR_NC, IF_NOT_10 |
| `1100` | IF_C | C=1 | IF_B, IF_LT, IF_1X |
| `1101` | IF_C_OR_NZ | C=1 OR Z=0 | IF_NZ_OR_C, IF_NOT_01 |
| `1110` | IF_C_OR_Z | C=1 OR Z=1 | IF_Z_OR_C, IF_BE, IF_LE, IF_NOT_00 |
| `1111` | IF_ALWAYS | Always | (no prefix) |

> `%0000` is exclusively the `_RET_` prefix (always-execute + return); it is NOT
> the encoding for `IF_NEVER`. `IF_NEVER` assembles to EEEE=`%1111` (always),
> identical to the bare no-prefix form, regardless of whether `WC`/`WZ` are written
> (pnut-ts boundary-probed). `%1111` is the default (always), printed with no `IF_` prefix.

---

**Coverage:** 359 instructions, 357 with an encoding pattern, 2 WITHOUT (listed at end).

---

## Branch  (36)

| Mnemonic | Encoding | Operands | Flags | Cyc | Summary |
|----------|----------|----------|-------|-----|---------|
| **CALL** | `EEEE 1101101 RAA AAAAAAAAA AAAAAAAAA`<br>`EEEE 1101011 CZ0 DDDDDDDDD 000101101` | #S \| D | C,Z | 4 | Call a subroutine; store return context on the stack |
| **CALLA** | `EEEE 1101011 CZ0 DDDDDDDDD 000101110`<br>`EEEE 1101110 RAA AAAAAAAAA AAAAAAAAA` | #S \| D | C,Z | 5-12 (cog/LUT) / 14-32 (hub-exec) | Call a subroutine; store return context in the Hub long at PTRA++ |
| **CALLB** | `EEEE 1101011 CZ0 DDDDDDDDD 000101111`<br>`EEEE 1101111 RAA AAAAAAAAA AAAAAAAAA` | #S \| D | C,Z | 5-12 (cog/LUT) / 14-32 (hub-exec) | Call a subroutine; store return context in the Hub long at PTRB++ |
| **CALLD** | `EEEE 11100WW RAA AAAAAAAAA AAAAAAAAA`<br>`EEEE 1011001 CZI DDDDDDDDD SSSSSSSSS` | D,#S/{@}S \| D,S/# | C,Z | 4 | Call a subroutine; store return context in PA/PB/PTRA/PTRB/D |
| **CALLPA** | `EEEE 1011010 0LI DDDDDDDDD SSSSSSSSS` | D/#,S/@ | -- | 4 | Call a subroutine; store return context on the stack and copy D into PA |
| **CALLPB** | `EEEE 1011010 1LI DDDDDDDDD SSSSSSSSS` | D/#,S/@ | -- | 4 | Call a subroutine; store return context on the stack and copy D into PB |
| **DJF** | `EEEE 1011011 10I DDDDDDDDD SSSSSSSSS` | D,S/@ | -- | 2 | Decrement value and jump if full (-1; $FFFF_FFFF) or not full (<> -1; <> $FFFF_FFFF) |
| **DJNF** | `EEEE 1011011 11I DDDDDDDDD SSSSSSSSS` | D,S/@ | -- | 2 | Decrement value and jump if full (-1; $FFFF_FFFF) or not full (<> -1; <> $FFFF_FFFF) |
| **DJNZ** | `EEEE 1011011 01I DDDDDDDDD SSSSSSSSS` | D,S/@ | -- | 2 | Decrement, jump if zero or not zero |
| **DJZ** | `EEEE 1011011 00I DDDDDDDDD SSSSSSSSS` | D,S/@ | -- | 2 | Decrement, jump if zero or not zero |
| **EXECF** | `EEEE 1101011 00L DDDDDDDDD 000110011` | D/#0..511 | -- | 4/4 | Call+Skip |
| **IJNZ** | `EEEE 1011100 01I DDDDDDDDD SSSSSSSSS` | D,S/@ | -- | 2 | Increment value and jump if zero or not zero |
| **IJZ** | `EEEE 1011100 00I DDDDDDDDD SSSSSSSSS` | D,S/@ | -- | 2 | Increment value and jump if zero or not zero |
| **JMP** | `EEEE 1101011 CZ0 DDDDDDDDD 000101100`<br>`EEEE 1101100 RAA AAAAAAAAA AAAAAAAAA` | #S \| D | C,Z | 4 | Jump |
| **JMPREL** | `EEEE 1101011 00L DDDDDDDDD 000110000` | D/#0..511 | -- | 4 | Jump ahead/back by D instructions |
| **REP** | `EEEE 1100110 1LI DDDDDDDDD SSSSSSSSS` | @,S/# \| D/#,S/# | -- | 2/2 | Execute next D[8:0] instructions S times |
| **RESI0** | `EEEE 1011001 110 111111110 111111111` | operand_xlat | -- | 4 | Resume from interrupt 0 |
| **RESI1** | `EEEE 1011001 110 111110100 111110101` | operand_xlat | -- | 4 | Resume from interrupt 1 |
| **RESI2** | `EEEE 1011001 110 111110010 111110011` | operand_xlat | -- | 4 | Resume from interrupt 2 |
| **RESI3** | `EEEE 1011001 110 111110000 111110001` | operand_xlat | -- | 4 | Resume from interrupt 3 |
| **RET** | `EEEE 1101011 CZ1 000000000 000101101` | operand_xlat | C,Z | 4 | Return by popping stack (K) |
| **RETA** | `EEEE 1101011 CZ1 000000000 000101110` | operand_xlat | C,Z | 11...18 (cog) / 20...40 (hub-exec) | Return by reading hub long (L) at --PTRA |
| **RETB** | `EEEE 1101011 CZ1 000000000 000101111` | operand_xlat | C,Z | 11...18 (cog) / 20...40 (hub-exec) | Return by reading hub long (L) at --PTRB |
| **RETI0** | `EEEE 1011001 110 111111111 111111111` | operand_xlat | -- | 4 | Return from interrupt 0 |
| **RETI1** | `EEEE 1011001 110 111111111 111110101` | operand_xlat | -- | 4 | Return from interrupt 1 |
| **RETI2** | `EEEE 1011001 110 111111111 111110011` | operand_xlat | -- | 4 | Return from interrupt 2 |
| **RETI3** | `EEEE 1011001 110 111111111 111110001` | operand_xlat | -- | 4 | Return from interrupt 3 |
| **SKIP** | `EEEE 1101011 00L DDDDDDDDD 000110001` | D/#0..511 | -- | 2 | Skip next instructions based on D bitmask |
| **SKIPF** | `EEEE 1101011 00L DDDDDDDDD 000110010` | D/#0..511 | -- | 2 | Fast skip - jump over instructions based on D bitmask |
| **TJF** | `EEEE 1011101 00I DDDDDDDDD SSSSSSSSS` | D,S/@ | -- | 2 | Test value and jump if full ($FFFFFFFF) |
| **TJNF** | `EEEE 1011101 01I DDDDDDDDD SSSSSSSSS` | D,S/@ | -- | 2 | Test value and jump if not full (<> $FFFF_FFFF) |
| **TJNS** | `EEEE 1011101 11I DDDDDDDDD SSSSSSSSS` | D,S/@ | -- | 2 | Test value and jump if not signed (positive) |
| **TJNZ** | `EEEE 1011100 11I DDDDDDDDD SSSSSSSSS` | D,S/@ | -- | 2 | Test value and jump if zero or not zero |
| **TJS** | `EEEE 1011101 10I DDDDDDDDD SSSSSSSSS` | D,S/@ | -- | 2 | Test value and jump if signed (D[31] = 1) |
| **TJV** | `EEEE 1011110 00I DDDDDDDDD SSSSSSSSS` | D,S/@ | -- | 2 not-taken / 4 taken (cog); 2 not-taken / 13-20 taken (hub-exec) | Test value and jump if overflowed |
| **TJZ** | `EEEE 1011100 10I DDDDDDDDD SSSSSSSSS` | D,S/@ | -- | 2 | Test value and jump if zero |

## CORDIC Solver  (10)

| Mnemonic | Encoding | Operands | Flags | Cyc | Summary |
|----------|----------|----------|-------|-----|---------|
| **GETQX** | `EEEE 1101011 CZ0 DDDDDDDDD 000011000` | D | C,Z | 2 | {WC/WZ/WCZ} Retrieve CORDIC result X into D |
| **GETQY** | `EEEE 1101011 CZ0 DDDDDDDDD 000011001` | D | C,Z | 2 | {WC/WZ/WCZ} Retrieve CORDIC result Y into D |
| **QDIV** | `EEEE 1101000 1LI DDDDDDDDD SSSSSSSSS` | D/#,S/# | -- | 2 | Perform 64÷32 unsigned division with 32-bit quotient and remainder |
| **QEXP** | `EEEE 1101011 00L DDDDDDDDD 000001111` | D/#0..511 | -- | 2 | Convert 5:27-bit logarithm to 32-bit unsigned integer |
| **QFRAC** | `EEEE 1101001 0LI DDDDDDDDD SSSSSSSSS` | D/#,S/# | -- | 2 | Perform 64÷32 unsigned fractional division with D as upper 32 bits |
| **QLOG** | `EEEE 1101011 00L DDDDDDDDD 000001110` | D/#0..511 | -- | 2 | Convert 32-bit unsigned integer to 5:27-bit logarithm format |
| **QMUL** | `EEEE 1101000 0LI DDDDDDDDD SSSSSSSSS` | D/#,S/# | -- | 2 | Perform 32×32 unsigned multiplication producing 64-bit result |
| **QROTATE** | `EEEE 1101010 0LI DDDDDDDDD SSSSSSSSS` | D/#,S/# | -- | 2 | Rotate a 32-bit signed (X, Y) point around origin (0, 0) by a specified angle |
| **QSQRT** | `EEEE 1101001 1LI DDDDDDDDD SSSSSSSSS` | D/#,S/# | -- | 2 | Calculate square root of 64-bit unsigned number formed from {S, D} |
| **QVECTOR** | `EEEE 1101010 1LI DDDDDDDDD SSSSSSSSS` | D/#,S/# | -- | 2 | Convert cartesian coordinates (X, Y) to polar coordinates (length, angle) |

## Color Space Converter  (5)

| Mnemonic | Encoding | Operands | Flags | Cyc | Summary |
|----------|----------|----------|-------|-----|---------|
| **SETCFRQ** | `EEEE 1101011 00L DDDDDDDDD 000111011` | D/#0..511 | -- | 2 | Set the colorspace converter \"CFRQ\" parameter to D[31:0] |
| **SETCI** | `EEEE 1101011 00L DDDDDDDDD 000111001` | D/#0..511 | -- | 2 | Set the colorspace converter \"CI\" parameter to D[31:0] |
| **SETCMOD** | `EEEE 1101011 00L DDDDDDDDD 000111100` | D/#0..511 | -- | 2 | Set the colorspace converter \"CMOD\" parameter to D[8:0] |
| **SETCQ** | `EEEE 1101011 00L DDDDDDDDD 000111010` | D/#0..511 | -- | 2 | Set the colorspace converter \"CQ\" parameter to D[31:0] |
| **SETCY** | `EEEE 1101011 00L DDDDDDDDD 000111000` | D/#0..511 | -- | 2 | Set the colorspace converter \"CY\" parameter to D[31:0] |

## Debug Directives  (1)

| Mnemonic | Encoding | Operands | Flags | Cyc | Summary |
|----------|----------|----------|-------|-----|---------|
| **DEBUG** | **(missing)** | operand_debug | -- | TBD | Debug instruction |

## Event  (72)

| Mnemonic | Encoding | Operands | Flags | Cyc | Summary |
|----------|----------|----------|-------|-----|---------|
| **ADDCT1** | `EEEE 1010011 00I DDDDDDDDD SSSSSSSSS` | D,S/# | -- | 2 | Set CT1 counter event trigger time |
| **ADDCT2** | `EEEE 1010011 01I DDDDDDDDD SSSSSSSSS` | D,S/# | -- | 2 | Set CT2 counter event trigger time |
| **ADDCT3** | `EEEE 1010011 10I DDDDDDDDD SSSSSSSSS` | D,S/# | -- | 2 | Set CT3 counter event trigger time |
| **COGATN** | `EEEE 1101011 00L DDDDDDDDD 000111111` | D/#0..511 | -- | 2 | Get the attention of one or more other cogs |
| **JATN** | `EEEE 1011110 01I 000001110 SSSSSSSSS` | S/# | -- | 2 | Jump if ATN event flag is set |
| **JCT1** | `EEEE 1011110 01I 000000001 SSSSSSSSS` | S/# | -- | 2 | Jump if counter 1 event flag is set |
| **JCT2** | `EEEE 1011110 01I 000000010 SSSSSSSSS` | S/# | -- | 2 | Jump if counter 2 event flag is set |
| **JCT3** | `EEEE 1011110 01I 000000011 SSSSSSSSS` | S/# | -- | 2 | Jump if counter 3 event flag is set |
| **JFBW** | `EEEE 1011110 01I 000001001 SSSSSSSSS` | S/# | -- | 2 | Jump if FIFO interface block wrap event flag is set or clear |
| **JINT** | `EEEE 1011110 01I 000000000 SSSSSSSSS` | S/# | -- | 2 | Jump if INT event flag is set |
| **JNATN** | `EEEE 1011110 01I 000011110 SSSSSSSSS` | S/# | -- | 2 | Jump if ATN event flag is clear |
| **JNCT1** | `EEEE 1011110 01I 000010001 SSSSSSSSS` | S/# | -- | 2 | Branch |
| **JNCT2** | `EEEE 1011110 01I 000010010 SSSSSSSSS` | S/# | -- | 2 | Branch |
| **JNCT3** | `EEEE 1011110 01I 000010011 SSSSSSSSS` | S/# | -- | 2 | Branch |
| **JNFBW** | `EEEE 1011110 01I 000011001 SSSSSSSSS` | S/# | -- | 2 | Jump if FIFO interface block wrap event flag is set or clear |
| **JNINT** | `EEEE 1011110 01I 000010000 SSSSSSSSS` | S/# | -- | 2 | Branch |
| **JNPAT** | `EEEE 1011110 01I 000011000 SSSSSSSSS` | S/# | -- | 2 | Branch |
| **JNQMT** | `EEEE 1011110 01I 000011111 SSSSSSSSS` | S/# | -- | 2 | Jump if CORDIC-read-but-empty event flag set or clear |
| **JNSE1** | `EEEE 1011110 01I 000010100 SSSSSSSSS` | S/# | -- | 2 | Branch |
| **JNSE2** | `EEEE 1011110 01I 000010101 SSSSSSSSS` | S/# | -- | 2 | Branch |
| **JNSE3** | `EEEE 1011110 01I 000010110 SSSSSSSSS` | S/# | -- | 2 | Branch |
| **JNSE4** | `EEEE 1011110 01I 000010111 SSSSSSSSS` | S/# | -- | 2 | Branch |
| **JNXFI** | `EEEE 1011110 01I 000011011 SSSSSSSSS` | S/# | -- | 2 | Branch |
| **JNXMT** | `EEEE 1011110 01I 000011010 SSSSSSSSS` | S/# | -- | 2 | Jump if streamer empty event flag set or clear |
| **JNXRL** | `EEEE 1011110 01I 000011101 SSSSSSSSS` | S/# | -- | 2 | Jump if streamer LUT RAM rollover event flag set or clear |
| **JNXRO** | `EEEE 1011110 01I 000011100 SSSSSSSSS` | S/# | -- | 2 | Branch |
| **JPAT** | `EEEE 1011110 01I 000001000 SSSSSSSSS` | S/# | -- | 2 | Branch |
| **JQMT** | `EEEE 1011110 01I 000001111 SSSSSSSSS` | S/# | -- | 2 | Jump if CORDIC-read-but-empty event flag set or clear |
| **JSE1** | `EEEE 1011110 01I 000000100 SSSSSSSSS` | S/# | -- | 2 | Branch |
| **JSE2** | `EEEE 1011110 01I 000000101 SSSSSSSSS` | S/# | -- | 2 | Branch |
| **JSE3** | `EEEE 1011110 01I 000000110 SSSSSSSSS` | S/# | -- | 2 | Branch |
| **JSE4** | `EEEE 1011110 01I 000000111 SSSSSSSSS` | S/# | -- | 2 | Branch |
| **JXFI** | `EEEE 1011110 01I 000001011 SSSSSSSSS` | S/# | -- | 2 | Branch |
| **JXMT** | `EEEE 1011110 01I 000001010 SSSSSSSSS` | S/# | -- | 2 | Jump if streamer empty event flag set or clear |
| **JXRL** | `EEEE 1011110 01I 000001101 SSSSSSSSS` | S/# | -- | 2 | Jump if streamer LUT RAM rollover event flag set or clear |
| **JXRO** | `EEEE 1011110 01I 000001100 SSSSSSSSS` | S/# | -- | 2 | Jump if streamer NCO rollover (XRO) event flag set |
| **POLLATN** | `EEEE 1101011 CZ0 000001110 000100100` | operand_pollwait | C,Z | 2 | Retrieve and clear attention flag |
| **POLLCT1** | `EEEE 1101011 CZ0 000000001 000100100` | operand_pollwait | C,Z | 2 | Retrieve and clear CT1 event flag |
| **POLLCT2** | `EEEE 1101011 CZ0 000000010 000100100` | operand_pollwait | C,Z | 2 | Retrieve and clear CT2 event flag |
| **POLLCT3** | `EEEE 1101011 CZ0 000000011 000100100` | operand_pollwait | C,Z | 2 | Retrieve and clear CT3 event flag |
| **POLLFBW** | `EEEE 1101011 CZ0 000001001 000100100` | operand_pollwait | C,Z | 2 | Retrieve and clear FIFO-interface-block-wrap event flag |
| **POLLINT** | `EEEE 1101011 CZ0 000000000 000100100` | operand_pollwait | C,Z | 2 | Retrieve and clear interrupt-occurred event flag |
| **POLLPAT** | `EEEE 1101011 CZ0 000001000 000100100` | operand_pollwait | C,Z | 2 | Retrieve and clear pin-pattern-detected event flag |
| **POLLQMT** | `EEEE 1101011 CZ0 000001111 000100100` | operand_pollwait | C,Z | 2 | Retrieve and clear CORDIC-read-but-empty event flag |
| **POLLSE1** | `EEEE 1101011 CZ0 000000100 000100100` | operand_pollwait | C,Z | 2 | Retrieve and clear SE1 event flag |
| **POLLSE2** | `EEEE 1101011 CZ0 000000101 000100100` | operand_pollwait | C,Z | 2 | Retrieve and clear SE2 event flag |
| **POLLSE3** | `EEEE 1101011 CZ0 000000110 000100100` | operand_pollwait | C,Z | 2 | Retrieve and clear SE3 event flag |
| **POLLSE4** | `EEEE 1101011 CZ0 000000111 000100100` | operand_pollwait | C,Z | 2 | Retrieve and clear SE4 event flag |
| **POLLXFI** | `EEEE 1101011 CZ0 000001011 000100100` | operand_pollwait | C,Z | 2 | Retrieve and clear streamer-finished event flag |
| **POLLXMT** | `EEEE 1101011 CZ0 000001010 000100100` | operand_pollwait | C,Z | 2 | Retrieve and clear streamer-empty event flag |
| **POLLXRL** | `EEEE 1101011 CZ0 000001101 000100100` | operand_pollwait | C,Z | 2 | Retrieve and clear streamer-LUT-RAM-rollover event flag |
| **POLLXRO** | `EEEE 1101011 CZ0 000001100 000100100` | operand_pollwait | C,Z | 2 | Retrieve and clear streamer-NCO-rollover event flag |
| **SETPAT** | `EEEE 1011111 1LI DDDDDDDDD SSSSSSSSS` | D/#,S/# | -- | 2 | Set pin pattern for PAT event detection |
| **SETSE1** | `EEEE 1101011 00L DDDDDDDDD 000100000` | D/#0..511 | -- | 2 | Configure selectable event 1 for pin/LUT/lock triggers |
| **SETSE2** | `EEEE 1101011 00L DDDDDDDDD 000100001` | D/#0..511 | -- | 2 | Configure selectable event 2 for pin/LUT/lock triggers |
| **SETSE3** | `EEEE 1101011 00L DDDDDDDDD 000100010` | D/#0..511 | -- | 2 | Configure selectable event 3 for pin/LUT/lock triggers |
| **SETSE4** | `EEEE 1101011 00L DDDDDDDDD 000100011` | D/#0..511 | -- | 2 | Configure selectable event 4 for pin/LUT/lock triggers |
| **WAITATN** | `EEEE 1101011 CZ0 000011110 000100100` | operand_pollwait | C,Z | 2 | Wait for and clear attention flag |
| **WAITCT1** | `EEEE 1101011 CZ0 000010001 000100100` | operand_pollwait | C,Z | 2 | Wait for and clear CT1 event flag |
| **WAITCT2** | `EEEE 1101011 CZ0 000010010 000100100` | operand_pollwait | C,Z | 2 | Wait for and clear CT2 event flag |
| **WAITCT3** | `EEEE 1101011 CZ0 000010011 000100100` | operand_pollwait | C,Z | 2 | Wait for and clear counter 3 event flag |
| **WAITFBW** | `EEEE 1101011 CZ0 000011001 000100100` | operand_pollwait | C,Z | 2 | Wait for and clear FIFO-interface-block-wrap event flag |
| **WAITINT** | `EEEE 1101011 CZ0 000010000 000100100` | operand_pollwait | C,Z | 2 | Wait for and clear interrupt-occurred event flag |
| **WAITPAT** | `EEEE 1101011 CZ0 000011000 000100100` | operand_pollwait | C,Z | 2 | Wait for and clear pin-pattern-detected event flag |
| **WAITSE1** | `EEEE 1101011 CZ0 000010100 000100100` | operand_pollwait | C,Z | 2 | Wait for and clear SE1 event flag |
| **WAITSE2** | `EEEE 1101011 CZ0 000010101 000100100` | operand_pollwait | C,Z | 2 | Wait for and clear SE2 event flag |
| **WAITSE3** | `EEEE 1101011 CZ0 000010110 000100100` | operand_pollwait | C,Z | 2 | Wait for and clear SE3 event flag |
| **WAITSE4** | `EEEE 1101011 CZ0 000010111 000100100` | operand_pollwait | C,Z | 2 | Wait for and clear SE4 event flag |
| **WAITXFI** | `EEEE 1101011 CZ0 000011011 000100100` | operand_pollwait | C,Z | 2 | Wait for and clear streamer-finished event flag |
| **WAITXMT** | `EEEE 1101011 CZ0 000011010 000100100` | operand_pollwait | C,Z | 2 | Wait for and clear streamer-empty event flag |
| **WAITXRL** | `EEEE 1101011 CZ0 000011101 000100100` | operand_pollwait | C,Z | 2 | Wait for and clear streamer-LUT-RAM-rollover event flag |
| **WAITXRO** | `EEEE 1101011 CZ0 000011100 000100100` | operand_pollwait | C,Z | 2 | Wait for and clear streamer-NCO-rollover event flag |

## Hub Control  (8)

| Mnemonic | Encoding | Operands | Flags | Cyc | Summary |
|----------|----------|----------|-------|-----|---------|
| **COGID** | `EEEE 1101011 C0L DDDDDDDDD 000000001` | D/#0..511 | C | 2 | Get current cog's ID or any cog's status by ID |
| **COGINIT** | `EEEE 1100111 CLI DDDDDDDDD SSSSSSSSS` | D/#,S/# | C | 2 | Start an available cog, or restart a cog by ID |
| **COGSTOP** | `EEEE 1101011 00L DDDDDDDDD 000000011` | D/#0..511 | -- | 2 | Stop a cog by ID |
| **HUBSET** | `EEEE 1101011 00L DDDDDDDDD 000000000` | D/#0..511 | -- | 2 | Set hub configuration |
| **LOCKNEW** | `EEEE 1101011 C00 DDDDDDDDD 000000100` | D | C | 4...11 | Request a new LOCK |
| **LOCKREL** | `EEEE 1101011 C0L DDDDDDDDD 000000111` | D/#0..511 | C | 2...9, +2 if result | Release LOCK |
| **LOCKRET** | `EEEE 1101011 00L DDDDDDDDD 000000101` | D/#0..511 | -- | 2...9 | Return LOCK for reallocation |
| **LOCKTRY** | `EEEE 1101011 C0L DDDDDDDDD 000000110` | D/#0..511 | C | 2...9, +2 if result | Try to acquire lock |

## Hub FIFO  (12)

| Mnemonic | Encoding | Operands | Flags | Cyc | Summary |
|----------|----------|----------|-------|-----|---------|
| **FBLOCK** | `EEEE 1100100 1LI DDDDDDDDD SSSSSSSSS` | D/#,S/# | -- | 2 | New Block |
| **GETPTR** | `EEEE 1101011 000 DDDDDDDDD 000110100` | D | -- | 2 | Get current FIFO hub pointer into D |
| **RDFAST** | `EEEE 1100011 1LI DDDDDDDDD SSSSSSSSS` | D/#,S/# | -- | 2 | Begin new fast hub read via FIFO |
| **RFBYTE** | `EEEE 1101011 CZ0 DDDDDDDDD 000010000` | D | C,Z | 2 | Read zero-extended byte from FIFO |
| **RFLONG** | `EEEE 1101011 CZ0 DDDDDDDDD 000010010` | D | C,Z | 2 | Read long from FIFO |
| **RFVAR** | `EEEE 1101011 CZ0 DDDDDDDDD 000010011` | D | C,Z | 2 | Read zero-extended 1-4 byte variable from FIFO |
| **RFVARS** | `EEEE 1101011 CZ0 DDDDDDDDD 000010100` | D | C,Z | 2 | Read sign-extended 1-4 byte variable from FIFO |
| **RFWORD** | `EEEE 1101011 CZ0 DDDDDDDDD 000010001` | D | C,Z | 2 | Read zero-extended word from FIFO |
| **WFBYTE** | `EEEE 1101011 00L DDDDDDDDD 000010101` | D/#0..511 | -- | 2 | Write byte to FIFO |
| **WFLONG** | `EEEE 1101011 00L DDDDDDDDD 000010111` | D/#0..511 | -- | 2 | Write long to FIFO |
| **WFWORD** | `EEEE 1101011 00L DDDDDDDDD 000010110` | D/#0..511 | -- | 2 | Write word to FIFO |
| **WRFAST** | `EEEE 1100100 0LI DDDDDDDDD SSSSSSSSS` | D/#,S/# | -- | 2 | Begin new fast hub write via FIFO |

## Hub RAM  (11)

| Mnemonic | Encoding | Operands | Flags | Cyc | Summary |
|----------|----------|----------|-------|-----|---------|
| **POPA** | `EEEE 1011000 CZ1 DDDDDDDDD 101011111` | D/# \| D | C,Z | 9...16 (cog) / 9...26 (hub-exec) | Pop long from hub stack using PTRA (pre-decrement) |
| **POPB** | `EEEE 1011000 CZ1 DDDDDDDDD 111011111` | D/# \| D | C,Z | 9...16 (cog) / 9...26 (hub-exec) | Pop long from hub stack using PTRB (pre-decrement) |
| **PUSHA** | `EEEE 1100011 0L1 DDDDDDDDD 101100001` | D/# \| D | -- | 3...10 (cog) / 3...20 (hub-exec) | Push long to hub stack using PTRA (post-increment) |
| **PUSHB** | `EEEE 1100011 0L1 DDDDDDDDD 111100001` | D/# \| D | -- | 3...10 (cog) / 3...20 (hub-exec) | Push long to hub stack using PTRB (post-increment) |
| **RDBYTE** | `EEEE 1010110 CZI DDDDDDDDD SSSSSSSSS` | D,S/#/PTRA/PTRB | C,Z | 9 | Read zero-extended byte from hub RAM |
| **RDLONG** | `EEEE 1011000 CZI DDDDDDDDD SSSSSSSSS` | D,S/#/PTRA/PTRB | C,Z | 9...16 (cog) / 9...26 (hub-exec) | Read long from hub RAM |
| **RDWORD** | `EEEE 1010111 CZI DDDDDDDDD SSSSSSSSS` | D,S/#/PTRA/PTRB | C,Z | 9...16 (cog) / 9...26 (hub-exec) | Read zero-extended word from hub RAM |
| **WMLONG** | `EEEE 1010011 11I DDDDDDDDD SSSSSSSSS` |  | -- | 3...10 (cog) / 3...20 (hub-exec) | Write masked long to hub RAM (non-zero bytes only) |
| **WRBYTE** | `EEEE 1100010 0LI DDDDDDDDD SSSSSSSSS` | D/#,S/#/PTRA/PTRB | -- | 3...10 (cog) / 3...20 (hub-exec) | Write byte to hub RAM |
| **WRLONG** | `EEEE 1100011 0LI DDDDDDDDD SSSSSSSSS` | D/#,S/#/PTRA/PTRB | -- | 3...10 (cog) / 3...20 (hub-exec) | Write long to hub RAM |
| **WRWORD** | `EEEE 1100010 1LI DDDDDDDDD SSSSSSSSS` | D/#,S/#/PTRA/PTRB | -- | 3...10 (cog) / 3...20 (hub-exec) | Write word to hub RAM |

## Interrupt  (14)

| Mnemonic | Encoding | Operands | Flags | Cyc | Summary |
|----------|----------|----------|-------|-----|---------|
| **ALLOWI** | `EEEE 1101011 000 000100000 000100100` | operand_pollwait | -- | 2 | Allow interrupts |
| **BRK** | `EEEE 1101011 00L DDDDDDDDD 000110110` | D/#0..511 | -- | 2 | Trigger breakpoint in current cog |
| **COGBRK** | `EEEE 1101011 00L DDDDDDDDD 000110101` | D/#0..511 | -- | 2 | Trigger breakpoint in specified cog |
| **GETBRK** | `EEEE 1101011 CZ0 DDDDDDDDD 000110101` | D/# WC/WZ/WCZ | -- | 2 | Get breakpoint/cog status into D according to WC/WZ/WCZ |
| **NIXINT1** | `EEEE 1101011 000 000100101 000100100` | operand_pollwait | -- | 2 | Cancel INT1 |
| **NIXINT2** | `EEEE 1101011 000 000100110 000100100` | operand_pollwait | -- | 2 | Cancel INT2 |
| **NIXINT3** | `EEEE 1101011 000 000100111 000100100` | operand_pollwait | -- | 2 | Cancel INT3 |
| **SETINT1** | `EEEE 1101011 00L DDDDDDDDD 000100101` | D/#0..511 | -- | 2 | Set INT1 source to D[3:0] |
| **SETINT2** | `EEEE 1101011 00L DDDDDDDDD 000100110` | D/#0..511 | -- | 2 | Set INT2 source to D[3:0] |
| **SETINT3** | `EEEE 1101011 00L DDDDDDDDD 000100111` | D/#0..511 | -- | 2 | Set INT3 source to D[3:0] |
| **STALLI** | `EEEE 1101011 000 000100001 000100100` | operand_pollwait | -- | 2 | Prevent further interrupts |
| **TRGINT1** | `EEEE 1101011 000 000100010 000100100` | operand_pollwait | -- | 2 | Trigger INT1, regardless of STALLI mode |
| **TRGINT2** | `EEEE 1101011 000 000100011 000100100` | operand_pollwait | -- | 2 | Trigger INT2, regardless of STALLI mode |
| **TRGINT3** | `EEEE 1101011 000 000100100 000100100` | operand_pollwait | -- | 2 | Trigger INT3, regardless of STALLI mode |

## Lookup Table  (3)

| Mnemonic | Encoding | Operands | Flags | Cyc | Summary |
|----------|----------|----------|-------|-----|---------|
| **RDLUT** | `EEEE 1010101 CZI DDDDDDDDD SSSSSSSSS` | D,S/#/PTRA/PTRB | C,Z | 3 | Read data from LUT (lookup table) address into register |
| **SETLUTS** | `EEEE 1101011 00L DDDDDDDDD 000110111` | D/#0..511 | -- | 2 | If D[0] = 1 then enable LUT sharing |
| **WRLUT** | `EEEE 1100001 1LI DDDDDDDDD SSSSSSSSS` | D/#,S/#/PTRA/PTRB | -- | 2 | Write D to LUT address {#}S/PTRx |

## Math and Logic  (110)

| Mnemonic | Encoding | Operands | Flags | Cyc | Summary |
|----------|----------|----------|-------|-----|---------|
| **ABS** | `EEEE 0110010 CZI DDDDDDDDD SSSSSSSSS`<br>`EEEE 0110010 CZ0 DDDDDDDDD DDDDDDDDD` | D{,S/#} | C,Z | 2 | Get the absolute value of a number |
| **ADD** | `EEEE 0001000 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Add two unsigned values |
| **ADDS** | `EEEE 0001010 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Add two signed values |
| **ADDSX** | `EEEE 0001011 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Add two signed extended values |
| **ADDX** | `EEEE 0001001 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Add two unsigned extended values |
| **AND** | `EEEE 0101000 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Bitwise AND a value with another, or with the NOT of another |
| **ANDN** | `EEEE 0101001 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Bitwise AND a value with another, or with the NOT of another |
| **BITC** | `EEEE 0100010 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Set bit(s) low/high according to C or !C |
| **BITH** | `EEEE 0100001 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Set bit(s) high (1) or low (0) |
| **BITL** | `EEEE 0100000 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Set bit(s) high (1) or low (0) |
| **BITNC** | `EEEE 0100011 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Set bit(s) low/high according to C or !C |
| **BITNOT** | `EEEE 0100111 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Toggle bit(s) to the opposite state |
| **BITNZ** | `EEEE 0100101 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Set bit(s) low/high according to Z or !Z |
| **BITRND** | `EEEE 0100110 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Set bit(s) random low/high |
| **BITZ** | `EEEE 0100100 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Set bit(s) low/high according to Z or !Z |
| **BMASK** | `EEEE 1001110 01I DDDDDDDDD SSSSSSSSS`<br>`EEEE 1001110 010 DDDDDDDDD DDDDDDDDD` | D{,S/#} | -- | 2 | Get 1..32-bit mask into Dest |
| **CMP** | `EEEE 0010000 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Compare two unsigned values |
| **CMPM** | `EEEE 0010101 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Compare two unsigned values, get MSB of difference |
| **CMPR** | `EEEE 0010100 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Compare two unsigned values (in reverse order to CMP) |
| **CMPS** | `EEEE 0010010 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Compare two signed values |
| **CMPSUB** | `EEEE 0010111 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Compare two unsigned values and subtract the second if it is lesser or equal |
| **CMPSX** | `EEEE 0010011 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Compare two signed values plus carry flag |
| **CMPX** | `EEEE 0010001 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Compare two unsigned values plus carry flag |
| **CRCBIT** | `EEEE 1001110 10I DDDDDDDDD SSSSSSSSS` | D,S/# | -- | 2 | Iterate CRC value in D using C and polynomial in S |
| **CRCNIB** | `EEEE 1001110 11I DDDDDDDDD SSSSSSSSS` | D,S/# | -- | 2 | Q = Q << 4 |
| **DECMOD** | `EEEE 0111001 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Decrement with modulus |
| **DECOD** | `EEEE 1001110 00I DDDDDDDDD SSSSSSSSS`<br>`EEEE 1001110 000 DDDDDDDDD DDDDDDDDD` | D{,S/#} | -- | 2 | Decode value (0-31) into single-high-bit long |
| **ENCOD** | `EEEE 0111100 CZI DDDDDDDDD SSSSSSSSS`<br>`EEEE 0111100 CZ0 DDDDDDDDD DDDDDDDDD` | D{,S/#} | C,Z | 2 | Get bit position of top-most 1 of Src or Dest into Dest |
| **FGE** | `EEEE 0011000 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Force unsigned value to be greater than or equal to another |
| **FGES** | `EEEE 0011010 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Force signed value to be greater than or equal to another |
| **FLE** | `EEEE 0011001 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Force unsigned value to be less than or equal to another |
| **FLES** | `EEEE 0011011 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Force signed value to be less than or equal to another |
| **GETBYTE** | `EEEE 1000111 NNI DDDDDDDDD SSSSSSSSS`<br>`EEEE 1000111 000 DDDDDDDDD 000000000` | D{,S/#,#0..3} | -- | 2 | Get a byte from a value |
| **GETNIB** | `EEEE 100001N NNI DDDDDDDDD SSSSSSSSS`<br>`EEEE 1000010 000 DDDDDDDDD 000000000` | D{,S/#,#0..7} | -- | 2 | Get a nibble from a value |
| **GETWORD** | `EEEE 1001001 1NI DDDDDDDDD SSSSSSSSS`<br>`EEEE 1001001 100 DDDDDDDDD 000000000` | D{,S/#,#0..1} | -- | 2 | Get a word from a value |
| **INCMOD** | `EEEE 0111000 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Increment with modulus |
| **LOC** | `EEEE 11101WW RAA AAAAAAAAA AAAAAAAAA` | D,#S{\} | -- | 2 | Load address into PA/PB/PTRA/PTRB |
| **MERGEB** | `EEEE 1101011 000 DDDDDDDDD 001100001` | D | -- | 2 | Merge bits of bytes in D |
| **MERGEW** | `EEEE 1101011 000 DDDDDDDDD 001100011` | D | -- | 2 | Merge bits of words in D |
| **MODC** | `EEEE 1101011 C01 0cccc0000 001101111` | #C{,#Z} | C | 2 | Modify C and/or Z flag(s) according to modifier mode and current state(s) |
| **MODCZ** | `EEEE 1101011 CZ1 0cccczzzz 001101111` | #C{,#Z} | C,Z | 2 | Modify C and/or Z flag(s) according to modifier mode and current state(s) |
| **MODZ** | `EEEE 1101011 0Z1 00000zzzz 001101111` | #C{,#Z} | Z | 2 | Modify C and/or Z flag(s) according to modifier mode and current state(s) |
| **MOV** | `EEEE 0110000 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Set a value into a register |
| **MOVBYTS** | `EEEE 1001111 11I DDDDDDDDD SSSSSSSSS` | D,S/# | -- | 2 | Move bytes within D, per S |
| **MUL** | `EEEE 1010000 0ZI DDDDDDDDD SSSSSSSSS` | D,S/# | Z | 2 | Multiply unsigned 16-bit x 16-bit values |
| **MULS** | `EEEE 1010000 1ZI DDDDDDDDD SSSSSSSSS` | D,S/# | Z | 2 | Multiply signed 16-bit x 16-bit values |
| **MUXC** | `EEEE 0101100 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Mux C into each D bit that is '1' in S |
| **MUXNC** | `EEEE 0101101 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Mux !C into each D bit that is '1' in S |
| **MUXNIBS** | `EEEE 1001111 01I DDDDDDDDD SSSSSSSSS` | D,S/# | -- | 2 | Set discrete nibbles of a value to non-zero nibble states of another |
| **MUXNITS** | `EEEE 1001111 00I DDDDDDDDD SSSSSSSSS` | D,S/# | -- | 2 | Set discrete bit pairs of a value to non-zero bit pair states of another |
| **MUXNZ** | `EEEE 0101111 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Set discrete bits to Z or !Z |
| **MUXQ** | `EEEE 1001111 10I DDDDDDDDD SSSSSSSSS` | D,S/# | -- | 2 | Set discrete bits of a value to that of another |
| **MUXZ** | `EEEE 0101110 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Set discrete bits to Z or !Z |
| **NEG** | `EEEE 0110011 CZI DDDDDDDDD SSSSSSSSS`<br>`EEEE 0110011 CZ0 DDDDDDDDD DDDDDDDDD` | D{,S/#} | C,Z | 2 | Negate a value |
| **NEGC** | `EEEE 0110100 CZI DDDDDDDDD SSSSSSSSS`<br>`EEEE 0110100 CZ0 DDDDDDDDD DDDDDDDDD` | D{,S/#} | C,Z | 2 | Negate value according to C |
| **NEGNC** | `EEEE 0110101 CZI DDDDDDDDD SSSSSSSSS`<br>`EEEE 0110101 CZ0 DDDDDDDDD DDDDDDDDD` | D{,S/#} | C,Z | 2 | Negate value according to !C |
| **NEGNZ** | `EEEE 0110111 CZI DDDDDDDDD SSSSSSSSS`<br>`EEEE 0110111 CZ0 DDDDDDDDD DDDDDDDDD` | D{,S/#} | C,Z | 2 | Negate value according to !Z |
| **NEGZ** | `EEEE 0110110 CZI DDDDDDDDD SSSSSSSSS`<br>`EEEE 0110110 CZ0 DDDDDDDDD DDDDDDDDD` | D{,S/#} | C,Z | 2 | Negate value according to Z |
| **NOT** | `EEEE 0110001 CZI DDDDDDDDD SSSSSSSSS`<br>`EEEE 0110001 CZ0 DDDDDDDDD DDDDDDDDD` | D{,S/#} | C,Z | 2 | Bitwise NOT a value |
| **ONES** | `EEEE 0111101 CZI DDDDDDDDD SSSSSSSSS`<br>`EEEE 0111101 CZ0 DDDDDDDDD DDDDDDDDD` | D{,S/#} | C,Z | 2 | Get number of 1s from Dest or Src into Dest |
| **OR** | `EEEE 0101010 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Bitwise OR a value with another |
| **RCL** | `EEEE 0000101 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Rotate carry flag left into value |
| **RCR** | `EEEE 0000100 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Rotate carry flag right into value |
| **RCZL** | `EEEE 1101011 CZ0 DDDDDDDDD 001101011` | D | C,Z | 2 | Rotate carry and zero flags left into value (2-bit rotate left) |
| **RCZR** | `EEEE 1101011 CZ0 DDDDDDDDD 001101010` | D | C,Z | 2 | Rotate carry and zero flags right into value (2-bit rotate right) |
| **REV** | `EEEE 1101011 000 DDDDDDDDD 001101001` | D | -- | 2 | Reverse bits of value |
| **RGBEXP** | `EEEE 1101011 000 DDDDDDDDD 001100111` | D | -- | 2 | Expand 5:6:5 RGB value in D[15:0] into 8:8:8 value in D[31:8] |
| **RGBSQZ** | `EEEE 1101011 000 DDDDDDDDD 001100110` | D | -- | 2 | Squeeze 8:8:8 RGB value in D[31:8] into 5:6:5 value in D[15:0] |
| **ROL** | `EEEE 0000001 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Rotate bits left |
| **ROLBYTE** | `EEEE 1001000 NNI DDDDDDDDD SSSSSSSSS`<br>`EEEE 1001000 000 DDDDDDDDD 000000000` | D{,S/#,#0..3} | -- | 2 | Rotate a byte left into a value |
| **ROLNIB** | `EEEE 100010N NNI DDDDDDDDD SSSSSSSSS`<br>`EEEE 1000100 000 DDDDDDDDD 000000000` | D{,S/#,#0..7} | -- | 2 | Rotate a nibble left into a value |
| **ROLWORD** | `EEEE 1001010 0NI DDDDDDDDD SSSSSSSSS`<br>`EEEE 1001010 000 DDDDDDDDD 000000000` | D{,S/#,#0..1} | -- | 2 | Rotate a word left into a value |
| **ROR** | `EEEE 0000000 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Rotate bits right |
| **SAL** | `EEEE 0000111 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Shift bits left, extending the LSB |
| **SAR** | `EEEE 0000110 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Divide signed 32-bit integer by power-of-two; a.k.a shift bits right, extending the MSB |
| **SCA** | `EEEE 1010001 0ZI DDDDDDDDD SSSSSSSSS` | D,S/# | Z | 2 | Create unsigned 16-bit scale value for next instruction's S value |
| **SCAS** | `EEEE 1010001 1ZI DDDDDDDDD SSSSSSSSS` | D,S/# | Z | 2 | Create signed 18-bit scale value for next instruction's S value |
| **SETBYTE** | `EEEE 1000110 NNI DDDDDDDDD SSSSSSSSS`<br>`EEEE 1000110 00I 000000000 SSSSSSSSS` | S/#{,D,#0..3} | -- | 2 | Set a byte to new value |
| **SETD** | `EEEE 1001101 10I DDDDDDDDD SSSSSSSSS` | D,S/# | -- | 2 | Set template D field for ALTI |
| **SETNIB** | `EEEE 100000N NNI DDDDDDDDD SSSSSSSSS`<br>`EEEE 1000000 00I 000000000 SSSSSSSSS` | S/#{,D,#0..7} | -- | 2 | Set a nibble to new value |
| **SETR** | `EEEE 1001101 01I DDDDDDDDD SSSSSSSSS` | D,S/# | -- | 2 | Set template Result field for ALTI |
| **SETS** | `EEEE 1001101 11I DDDDDDDDD SSSSSSSSS` | D,S/# | -- | 2 | Set template S field for ALTI |
| **SETWORD** | `EEEE 1001001 0NI DDDDDDDDD SSSSSSSSS`<br>`EEEE 1001001 00I 000000000 SSSSSSSSS` | S/#{,D,#0..1} | -- | 2 | Set a word to new value |
| **SEUSSF** | `EEEE 1101011 000 DDDDDDDDD 001100100` | D | -- | 2 | Relocate and periodically invert bits within D |
| **SEUSSR** | `EEEE 1101011 000 DDDDDDDDD 001100101` | D | -- | 2 | Relocate and periodically invert bits within D |
| **SHL** | `EEEE 0000011 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Shift bits left; a.k.a. multiply 32-bit integer by power-of-two |
| **SHR** | `EEEE 0000010 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Shift bits right; a.k.a. divide unsigned 32-bit integer by power-of-two |
| **SIGNX** | `EEEE 0111011 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Sign-extend value beyond designated bit |
| **SPLITB** | `EEEE 1101011 000 DDDDDDDDD 001100000` | D | -- | 2 | Split every 4th bit of D into bytes |
| **SPLITW** | `EEEE 1101011 000 DDDDDDDDD 001100010` | D | -- | 2 | Split odd/even bits of D into words |
| **SUB** | `EEEE 0001100 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Subtract one unsigned value from another |
| **SUBR** | `EEEE 0010110 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Subtract one unsigned value from another (in reverse order to SUB) |
| **SUBS** | `EEEE 0001110 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Subtract one signed value from another |
| **SUBSX** | `EEEE 0001111 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Subtract one signed extended value from another |
| **SUBX** | `EEEE 0001101 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Subtract one unsigned extended value from another |
| **SUMC** | `EEEE 0011100 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Sum +/- source into destination based on C flag |
| **SUMNC** | `EEEE 0011101 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Adjust signed value by other C-negated or !C-negated value |
| **SUMNZ** | `EEEE 0011111 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Adjust signed value by other Z-negated or !Z-negated value |
| **SUMZ** | `EEEE 0011110 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | {WC/WZ/WCZ} Sum +/-S into D by Z |
| **TEST** | `EEEE 0111110 CZ0 DDDDDDDDD DDDDDDDDD`<br>`EEEE 0111110 CZI DDDDDDDDD SSSSSSSSS` | D{,S/#} | C,Z | 2 | Test D, or bitwise AND D with S, to affect flags |
| **TESTB** | `EEEE 0100000 CZI DDDDDDDDD SSSSSSSSS`<br>`EEEE 0100010 CZI DDDDDDDDD SSSSSSSSS`<br>`EEEE 0100100 CZI DDDDDDDDD SSSSSSSSS`<br>`EEEE 0100110 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Test bit of register and write to C/Z flag |
| **TESTBN** | `EEEE 0100001 CZI DDDDDDDDD SSSSSSSSS`<br>`EEEE 0100011 CZI DDDDDDDDD SSSSSSSSS`<br>`EEEE 0100101 CZI DDDDDDDDD SSSSSSSSS`<br>`EEEE 0100111 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Test bit of D or !D and either store, AND, OR, or XOR the result into flags |
| **TESTN** | `EEEE 0111111 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Test D by bitwise ANDing with !S to affect flags only |
| **WRC** | `EEEE 1101011 000 DDDDDDDDD 001101100` | D | -- | 2 | Write 0 or 1 to D, according to C |
| **WRNC** | `EEEE 1101011 000 DDDDDDDDD 001101101` | D | -- | 2 | Write C or not C to register |
| **WRNZ** | `EEEE 1101011 000 DDDDDDDDD 001101111` | D | -- | 2 | Write Z or not Z to register |
| **WRZ** | `EEEE 1101011 000 DDDDDDDDD 001101110` | D | -- | 2 | Write 0 or 1 to D, according to Z |
| **XOR** | `EEEE 0101011 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Bitwise XOR a value with another |
| **XORO32** | `EEEE 1101011 000 DDDDDDDDD 001101000` | D | -- | 2 | Iterate D with xoroshiro32+ PRNG algorithm (requires non-zero seed) |
| **ZEROX** | `EEEE 0111010 CZI DDDDDDDDD SSSSSSSSS` | D,S/# | C,Z | 2 | Zero-extend value beyond designated bit |

## Miscellaneous  (10)

| Mnemonic | Encoding | Operands | Flags | Cyc | Summary |
|----------|----------|----------|-------|-----|---------|
| **AUGD** | `EEEE 11111DD DDD DDDDDDDDD DDDDDDDDD` | #S | -- | 2 | Augment next literal Dest to 32-bits |
| **AUGS** | `EEEE 11110SS SSS SSSSSSSSS SSSSSSSSS` | #S | -- | 2 | Augment next literal Src to 32-bits |
| **GETCT** | `EEEE 1101011 C00 DDDDDDDDD 000011010` | D | C | 2 | T=0 on reset, CT++ on every clock |
| **GETRND** | `EEEE 1101011 CZ0 DDDDDDDDD 000011011`<br>`EEEE 1101011 CZ1 000000000 000011011` | D \| {WC/WZ/WCZ} | C,Z | 2 | Get RND into C/Z |
| **NOP** | `0000 0000000 000 000000000 000000000` | operand_nop | -- | 2 | No operation, just elapse two cycles |
| **POP** | `EEEE 1101011 CZ0 DDDDDDDDD 000101011` | D | C,Z | 2 | Pop internal stack (K) to destination register |
| **PUSH** | `EEEE 1101011 00L DDDDDDDDD 000101010` | D/#0..511 | -- | 2 | Push value onto internal stack (K) |
| **SETQ** | `EEEE 1101011 00L DDDDDDDDD 000101000` | D/#0..511 | -- | 2 | Set Q to D |
| **SETQ2** | `EEEE 1101011 00L DDDDDDDDD 000101001` | D/#0..511 | -- | 2 | Set Q to D |
| **WAITX** | `EEEE 1101011 CZL DDDDDDDDD 000011111` | D/#0..511 | C,Z | 2 + D | Wait 2+D clock cycles, or 2+(D AND RND) with WC/WZ/WCZ |

## Pin  (34)

| Mnemonic | Encoding | Operands | Flags | Cyc | Summary |
|----------|----------|----------|-------|-----|---------|
| **DIRC** | `EEEE 1101011 CZL DDDDDDDDD 001000010` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to input/output according to C or !C |
| **DIRH** | `EEEE 1101011 CZL DDDDDDDDD 001000001` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to output (high; 1) or input (low; 0) |
| **DIRL** | `EEEE 1101011 CZL DDDDDDDDD 001000000` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to output (high; 1) or input (low; 0) |
| **DIRNC** | `EEEE 1101011 CZL DDDDDDDDD 001000011` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to input/output according to C or !C |
| **DIRNOT** | `EEEE 1101011 CZL DDDDDDDDD 001000111` | D/#0..511 {WC/WZ} | C,Z | 2 | Toggle pin(s) to the opposite direction |
| **DIRNZ** | `EEEE 1101011 CZL DDDDDDDDD 001000101` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to input/output according to Z or !Z |
| **DIRRND** | `EEEE 1101011 CZL DDDDDDDDD 001000110` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to random input/output |
| **DIRZ** | `EEEE 1101011 CZL DDDDDDDDD 001000100` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to input/output according to Z or !Z |
| **DRVC** | `EEEE 1101011 CZL DDDDDDDDD 001011010` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to output and output level to low/high according to C or !C |
| **DRVH** | `EEEE 1101011 CZL DDDDDDDDD 001011001` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to output and output level high (1) or low (0) |
| **DRVL** | `EEEE 1101011 CZL DDDDDDDDD 001011000` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to output and output level high (1) or low (0) |
| **DRVNC** | `EEEE 1101011 CZL DDDDDDDDD 001011011` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to output and output level to low/high according to C or !C |
| **DRVNOT** | `EEEE 1101011 CZL DDDDDDDDD 001011111` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to output and toggle to the opposite output level |
| **DRVNZ** | `EEEE 1101011 CZL DDDDDDDDD 001011101` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to output and output level to low/high according to Z or !Z |
| **DRVRND** | `EEEE 1101011 CZL DDDDDDDDD 001011110` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to output and output level to random low/high |
| **DRVZ** | `EEEE 1101011 CZL DDDDDDDDD 001011100` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to output and output level to low/high according to Z or !Z |
| **FLTC** | `EEEE 1101011 CZL DDDDDDDDD 001010010` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to input and an output level of low/high according to C |
| **FLTH** | `EEEE 1101011 CZL DDDDDDDDD 001010001` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to input and to an output level of high (1) or low (0) |
| **FLTL** | `EEEE 1101011 CZL DDDDDDDDD 001010000` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to input and to an output level of high (1) or low (0) |
| **FLTNC** | `EEEE 1101011 CZL DDDDDDDDD 001010011` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to input and an output level of low/high according to C |
| **FLTNOT** | `EEEE 1101011 CZL DDDDDDDDD 001010111` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to input and toggle to the opposite output level |
| **FLTNZ** | `EEEE 1101011 CZL DDDDDDDDD 001010101` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to input and an output level of low/high according to Z |
| **FLTRND** | `EEEE 1101011 CZL DDDDDDDDD 001010110` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to input and to an output level of random low/high |
| **FLTZ** | `EEEE 1101011 CZL DDDDDDDDD 001010100` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) direction to input and an output level of low/high according to Z |
| **OUTC** | `EEEE 1101011 CZL DDDDDDDDD 001001010` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) output level to low/high according to C or !C |
| **OUTH** | `EEEE 1101011 CZL DDDDDDDDD 001001001` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) output level to high (1) or low (0) |
| **OUTL** | `EEEE 1101011 CZL DDDDDDDDD 001001000` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) output level to high (1) or low (0) |
| **OUTNC** | `EEEE 1101011 CZL DDDDDDDDD 001001011` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) output level to low/high according to C or !C |
| **OUTNOT** | `EEEE 1101011 CZL DDDDDDDDD 001001111` | D/#0..511 {WC/WZ} | C,Z | 2 | Toggle pin(s) to the opposite output level |
| **OUTNZ** | `EEEE 1101011 CZL DDDDDDDDD 001001101` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) output level to low/high according to Z or !Z |
| **OUTRND** | `EEEE 1101011 CZL DDDDDDDDD 001001110` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) output level to random low/high |
| **OUTZ** | `EEEE 1101011 CZL DDDDDDDDD 001001100` | D/#0..511 {WC/WZ} | C,Z | 2 | Set pin(s) output level to low/high according to Z or !Z |
| **TESTP** | `EEEE 1101011 CZL DDDDDDDDD 001000000`<br>`EEEE 1101011 CZL DDDDDDDDD 001000010`<br>`EEEE 1101011 CZL DDDDDDDDD 001000100`<br>`EEEE 1101011 CZL DDDDDDDDD 001000110` | D/#0..511 WC/ANDC/ORC/XORC \| WZ/ANDZ/ORZ/XORZ | C,Z | 2 | Test pin state with optional XOR operation |
| **TESTPN** | `EEEE 1101011 CZL DDDDDDDDD 001000001`<br>`EEEE 1101011 CZL DDDDDDDDD 001000011`<br>`EEEE 1101011 CZL DDDDDDDDD 001000101`<br>`EEEE 1101011 CZL DDDDDDDDD 001000111` | D/#0..511 WC/ANDC/ORC/XORC \| WZ/ANDZ/ORZ/XORZ | C,Z | 2 | Test pin and either store, AND, OR, or XOR the result or inverse result into C/Z |

## Pixel Mixer  (6)

| Mnemonic | Encoding | Operands | Flags | Cyc | Summary |
|----------|----------|----------|-------|-----|---------|
| **ADDPIX** | `EEEE 1010010 00I DDDDDDDDD SSSSSSSSS` | D,S/# | -- | 7 | Add 8:8:8:8 pixel bytes with full saturation |
| **BLNPIX** | `EEEE 1010010 10I DDDDDDDDD SSSSSSSSS` | D,S/# | -- | 7 | Alpha-blend bytes of S into bytes of D, using SETPIV value |
| **MIXPIX** | `EEEE 1010010 11I DDDDDDDDD SSSSSSSSS` | D,S/# | -- | 7 | Mix bytes of S into bytes of D, using SETPIX and SETPIV values |
| **MULPIX** | `EEEE 1010010 01I DDDDDDDDD SSSSSSSSS` | D,S/# | -- | 7 | Multiply bytes of S into bytes of D, where $FF = 1 |
| **SETPIV** | `EEEE 1101011 00L DDDDDDDDD 000111101` | D/#0..511 | -- | 2 | Set BLNPIX/MIXPIX blend factor to D[7:0] |
| **SETPIX** | `EEEE 1101011 00L DDDDDDDDD 000111110` | D/#0..511 | -- | 2 | Set MIXPIX mode to D[5:0] |

## Register Indirection  (11)

| Mnemonic | Encoding | Operands | Flags | Cyc | Summary |
|----------|----------|----------|-------|-----|---------|
| **ALTB** | `EEEE 1001100 11I DDDDDDDDD SSSSSSSSS`<br>`EEEE 1001100 111 DDDDDDDDD 000000000` | D{,S/#} | -- | 2 | Alter subsequent BITxxx instruction |
| **ALTD** | `EEEE 1001100 01I DDDDDDDDD SSSSSSSSS`<br>`EEEE 1001100 011 DDDDDDDDD 000000000` | D{,S/#} | -- | 2 | Alter D field of next instruction |
| **ALTGB** | `EEEE 1001011 01I DDDDDDDDD SSSSSSSSS`<br>`EEEE 1001011 011 DDDDDDDDD 000000000` | D{,S/#} | -- | 2 | Alter subsequent GETBYTE / ROLBYTE instruction |
| **ALTGN** | `EEEE 1001010 11I DDDDDDDDD SSSSSSSSS`<br>`EEEE 1001010 111 DDDDDDDDD 000000000` | D{,S/#} | -- | 2 | Alter subsequent GETNIB / ROLNIB instruction |
| **ALTGW** | `EEEE 1001011 11I DDDDDDDDD SSSSSSSSS`<br>`EEEE 1001011 111 DDDDDDDDD 000000000` | D{,S/#} | -- | 2 | Alter subsequent GETWORD / ROLWORD instruction |
| **ALTI** | `EEEE 1001101 00I DDDDDDDDD SSSSSSSSS`<br>`EEEE 1001101 001 DDDDDDDDD 101100100` | D{,S/#} | -- | 2 | Substitute next instruction's field values from template, per configuration |
| **ALTR** | `EEEE 1001100 00I DDDDDDDDD SSSSSSSSS`<br>`EEEE 1001100 001 DDDDDDDDD 000000000` | D{,S/#} | -- | 2 | Alter Result register address of next instruction |
| **ALTS** | `EEEE 1001100 10I DDDDDDDDD SSSSSSSSS`<br>`EEEE 1001100 101 DDDDDDDDD 000000000` | D{,S/#} | -- | 2 | Alter S field of next instruction |
| **ALTSB** | `EEEE 1001011 00I DDDDDDDDD SSSSSSSSS`<br>`EEEE 1001011 001 DDDDDDDDD 000000000` | D{,S/#} | -- | 2 | Alter subsequent SETBYTE instruction |
| **ALTSN** | `EEEE 1001010 10I DDDDDDDDD SSSSSSSSS`<br>`EEEE 1001010 101 DDDDDDDDD 000000000` | D{,S/#} | -- | 2 | Alter subsequent SETNIB instruction |
| **ALTSW** | `EEEE 1001011 10I DDDDDDDDD SSSSSSSSS`<br>`EEEE 1001011 101 DDDDDDDDD 000000000` | D{,S/#} | -- | 2 | Alter subsequent SETWORD instruction |

## Smart Pin  (9)

| Mnemonic | Encoding | Operands | Flags | Cyc | Summary |
|----------|----------|----------|-------|-----|---------|
| **AKPIN** | `EEEE 1100000 01I 000000001 SSSSSSSSS` | S/# | -- | 2 | Acknowledge smart pin(s) |
| **GETSCP** | `EEEE 1101011 000 DDDDDDDDD 001110001` | D | -- | 2 | Get four-channel oscilloscope samples into D |
| **RDPIN** | `EEEE 1010100 C1I DDDDDDDDD SSSSSSSSS` | D,S/# | C | 2 | Read smart pin result and acknowledge pin |
| **RQPIN** | `EEEE 1010100 C0I DDDDDDDDD SSSSSSSSS` | D,S/# | C | 2 | Read smart pin result without acknowledge |
| **SETDACS** | `EEEE 1101011 00L DDDDDDDDD 000011100` | D/#0..511 | -- | 2 | DAC3 = D[31:24], DAC2 = D[23:16], DAC1 = D[15:8], DAC0 = D[7:0] |
| **SETSCP** | `EEEE 1101011 00L DDDDDDDDD 001110000` | D/#0..511 | -- | 2 | Set four-channel oscilloscope enable to D[6] and set input pin base to D[5:2] |
| **WRPIN** | `EEEE 1100000 0LI DDDDDDDDD SSSSSSSSS` | D/#,S/# | -- | 2 | Set mode of smart pins S[10:6]+S[5:0] |
| **WXPIN** | `EEEE 1100000 1LI DDDDDDDDD SSSSSSSSS` | D/#,S/# | -- | 2 | Set \"X\" of smart pins S[10:6]+S[5:0] |
| **WYPIN** | `EEEE 1100001 0LI DDDDDDDDD SSSSSSSSS` | D/#,S/# | -- | 2 | Set "Y" register of smart pins S[10:6]+S[5:0] |

## Streamer  (6)

| Mnemonic | Encoding | Operands | Flags | Cyc | Summary |
|----------|----------|----------|-------|-----|---------|
| **GETXACC** | `EEEE 1101011 000 DDDDDDDDD 000011110` | D | -- | 2 | Get streamer's Goertzel X/Y accumulators into D and next S |
| **SETXFRQ** | `EEEE 1101011 00L DDDDDDDDD 000011101` | D/#0..511 | -- | 2 | Set streamer NCO frequency to D |
| **XCONT** | `EEEE 1100110 0LI DDDDDDDDD SSSSSSSSS` | D/#,S/# | -- | 2 | Buffer new streamer command, continuing phase |
| **XINIT** | `EEEE 1100101 0LI DDDDDDDDD SSSSSSSSS` | D/#,S/# | -- | 2 | Issue streamer command immediately, zeroing phase |
| **XSTOP** | `EEEE 1100101 011 000000000 000000000` | operand_xlat | -- | 2 | Stop streamer immediately |
| **XZERO** | `EEEE 1100101 1LI DDDDDDDDD SSSSSSSSS` | D/#,S/# | -- | 2 | Buffer new streamer command, zeroing phase |

## System Control  (1)

| Mnemonic | Encoding | Operands | Flags | Cyc | Summary |
|----------|----------|----------|-------|-----|---------|
| **ASMCLK** | **(missing)** | operand_asmclk | -- | variable | Pseudo-instruction that sets clock mode from CON symbols in PASM-only programs |

---

## Instructions missing an encoding pattern in the YAMLs

These need their `encoding.bits` cross-filled (the v35 CSV spreadsheet has them):

`ASMCLK`, `DEBUG`
