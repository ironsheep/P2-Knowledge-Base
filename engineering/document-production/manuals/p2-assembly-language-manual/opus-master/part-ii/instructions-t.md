# T Instructions

## TEST — Test

Tests the parity and zero state of a register value.

### Syntax
```pasm
        TEST    D {WC|WZ|WCZ}
        TEST    D, {#}S {WC|WZ|WCZ}
```

### Result
The parity and zero-state of D, or of D bitwise ANDed with S, is stored in the C and Z flags.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register whose value will be tested |
| S | Optional register, 9-bit literal, or 32-bit augmented literal to AND with D |
| WC/WZ/WCZ | Optional effects to update C and/or Z flags |

### Encoding
\simpleencoding{EEEE | 0111110 | CZ0 | DDDDDDDDD | DDDDDDDDD | — | Parity of D | D = 0 | 2}

\simpleencoding{EEEE | 0111110 | CZI | DDDDDDDDD | SSSSSSSSS | — | Parity of (D & S) | (D & S) = 0 | 2}

### Related Instructions
- [TESTN](#testn) — Test with inverted source value
- [TESTB](#testb) — Test individual bit in register
- [TESTBN](#testbn) — Test individual bit negated
- [TESTP](#testp) — Test pin state
- [TESTPN](#testpn) — Test pin state negated

### Explanation
TEST determines the parity (number of high bits) and the zero or non-zero state of D, or of D bitwise ANDed with S, and stores the results in the C and/or Z flag.

If the WC or WCZ effect is specified, the C flag is set to 1 if the number of high bits in D (or D ANDed with S) is odd, or is cleared to 0 if it is even.

If the WZ or WCZ effect is specified, the Z flag is set to 1 if D (or D ANDed with S) is zero, or is cleared to 0 if it is not zero.

TEST is non-destructive—it does not modify D.

---

## TESTB — Test Bit

Tests a single bit in a register and writes the result to C or Z.

### Syntax
```pasm
        TESTB   D, {#}S         WC/WZ
        TESTB   D, {#}S         ANDC/ANDZ
        TESTB   D, {#}S         ORC/ORZ
        TESTB   D, {#}S         XORC/XORZ
```

### Result
The state of bit S[4:0] of D is read and either stored as-is, or bitwise ANDed, ORed, or XORed into C or Z.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register whose bit will be tested |
| S | Register or 5-bit literal specifying bit position (0-31) |
| WC/WZ | Write bit state to C or Z flag |
| ANDC/ANDZ | AND bit state with C or Z flag |
| ORC/ORZ | OR bit state with C or Z flag |
| XORC/XORZ | XOR bit state with C or Z flag |

### Encoding
\simpleencoding{EEEE | 0100000 | CZI | DDDDDDDDD | SSSSSSSSS | — | D[S[4:0]] | D[S[4:0]] | 2}

\simpleencoding{EEEE | 0100010 | CZI | DDDDDDDDD | SSSSSSSSS | — | C/Z AND D[S[4:0]] | C/Z AND D[S[4:0]] | 2}

\simpleencoding{EEEE | 0100100 | CZI | DDDDDDDDD | SSSSSSSSS | — | C/Z OR D[S[4:0]] | C/Z OR D[S[4:0]] | 2}

\simpleencoding{EEEE | 0100110 | CZI | DDDDDDDDD | SSSSSSSSS | — | C/Z XOR D[S[4:0]] | C/Z XOR D[S[4:0]] | 2}

### Related Instructions
- [TESTBN](#testbn) — Test bit negated
- [TESTP](#testp) — Test pin state
- [TESTPN](#testpn) — Test pin state negated

### Explanation
TESTB reads the state (0 or 1) of a bit in D designated by S, and either stores it as-is, or bitwise ANDs, ORs, or XORs it into C or Z. The bit position is specified by S[4:0] (0-31). The WC, WZ, ANDC, ANDZ, ORC, ORZ, XORC, or XORZ effect determines how the bit state is applied to the selected flag.

TESTB is useful for examining individual bits without modifying the register value.

---

## TESTBN — Test Bit Negated

Tests a single bit in a register, inverts the result, and writes to C or Z.

### Syntax
```pasm
        TESTBN  D, {#}S         WC/WZ
        TESTBN  D, {#}S         ANDC/ANDZ
        TESTBN  D, {#}S         ORC/ORZ
        TESTBN  D, {#}S         XORC/XORZ
```

### Result
The inverted state of bit S[4:0] of D is read and either stored as-is, or bitwise ANDed, ORed, or XORed into C or Z.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register whose bit will be tested |
| S | Register or 5-bit literal specifying bit position (0-31) |
| WC/WZ | Write inverted bit state to C or Z flag |
| ANDC/ANDZ | AND inverted bit state with C or Z flag |
| ORC/ORZ | OR inverted bit state with C or Z flag |
| XORC/XORZ | XOR inverted bit state with C or Z flag |

### Encoding
\simpleencoding{EEEE | 0100001 | CZI | DDDDDDDDD | SSSSSSSSS | — | !D[S[4:0]] | !D[S[4:0]] | 2}

\simpleencoding{EEEE | 0100011 | CZI | DDDDDDDDD | SSSSSSSSS | — | C/Z AND !D[S[4:0]] | C/Z AND !D[S[4:0]] | 2}

\simpleencoding{EEEE | 0100101 | CZI | DDDDDDDDD | SSSSSSSSS | — | C/Z OR !D[S[4:0]] | C/Z OR !D[S[4:0]] | 2}

\simpleencoding{EEEE | 0100111 | CZI | DDDDDDDDD | SSSSSSSSS | — | C/Z XOR !D[S[4:0]] | C/Z XOR !D[S[4:0]] | 2}

### Related Instructions
- [TESTB](#testb) — Test bit without inversion
- [TESTP](#testp) — Test pin state
- [TESTPN](#testpn) — Test pin state negated

### Explanation
TESTBN reads the state (0 or 1) of a bit in D designated by S, inverts that result, and either stores it as-is, or bitwise ANDs, ORs, or XORs it into C or Z. The bit position is specified by S[4:0] (0-31). The WC, WZ, ANDC, ANDZ, ORC, ORZ, XORC, or XORZ effect determines how the inverted bit state is applied to the selected flag.

TESTBN is useful for testing whether a bit is clear (0) rather than set (1).

---

## TESTN — Test Not

Tests the parity and zero state of a register ANDed with an inverted value.

### Syntax
```pasm
        TESTN   D, {#}S {WC|WZ|WCZ}
```

### Result
The parity and zero-state of D bitwise ANDed with !S is stored in the C and Z flags.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register whose value will be tested |
| S | Register, 9-bit literal, or 32-bit augmented literal to invert and AND with D |
| WC/WZ/WCZ | Optional effects to update C and/or Z flags |

### Encoding
\simpleencoding{EEEE | 0111111 | CZI | DDDDDDDDD | SSSSSSSSS | — | Parity of (D & !S) | (D & !S) = 0 | 2}

### Related Instructions
- [TEST](#test) — Test without inversion
- [TESTB](#testb) — Test individual bit
- [TESTBN](#testbn) — Test individual bit negated

### Explanation
TESTN determines the parity (number of high bits) and the zero or non-zero state of D bitwise ANDed with !S and stores the results in the C and/or Z flag.

If the WC or WCZ effect is specified, the C flag is set to 1 if the number of high bits in D ANDed with !S is odd, or is cleared to 0 if it is even.

If the WZ or WCZ effect is specified, the Z flag is set to 1 if D ANDed with !S is zero, or is cleared to 0 if it is not zero.

TESTN is non-destructive—it does not modify D. It is useful for testing which bits in D are set while masking out specific bits defined by S.

---

## TESTP — Test Pin

Tests the state of an I/O pin and writes the result to C or Z.

### Syntax
```pasm
        TESTP   {#}D            WC/WZ
        TESTP   {#}D            ANDC/ANDZ
        TESTP   {#}D            ORC/ORZ
        TESTP   {#}D            XORC/XORZ
```

### Result
The state of the I/O pin described by D is read and either stored as-is, or bitwise ANDed, ORed, or XORed into C or Z.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register or 6-bit literal (0-63) identifying the I/O pin |
| WC/WZ | Write pin state to C or Z flag |
| ANDC/ANDZ | AND pin state with C or Z flag |
| ORC/ORZ | OR pin state with C or Z flag |
| XORC/XORZ | XOR pin state with C or Z flag |

### Encoding
\simpleencoding{EEEE | 1101011 | CZL | DDDDDDDDD | 001000000 | — | IN[D[5:0]] | IN[D[5:0]] | 2}

\simpleencoding{EEEE | 1101011 | CZL | DDDDDDDDD | 001000010 | — | C/Z AND IN[D[5:0]] | C/Z AND IN[D[5:0]] | 2}

\simpleencoding{EEEE | 1101011 | CZL | DDDDDDDDD | 001000100 | — | C/Z OR IN[D[5:0]] | C/Z OR IN[D[5:0]] | 2}

\simpleencoding{EEEE | 1101011 | CZL | DDDDDDDDD | 001000110 | — | C/Z XOR IN[D[5:0]] | C/Z XOR IN[D[5:0]] | 2}

### Related Instructions
- [TESTPN](#testpn) — Test pin state negated
- [TESTB](#testb) — Test bit in register
- [TESTBN](#testbn) — Test bit in register negated
- [DRVL](instructions-d.md#drvl) — Drive pin low
- [DRVH](instructions-d.md#drvh) — Drive pin high

### Explanation
TESTP reads the state (0 or 1) of the I/O pin designated by D, and either stores it as-is, or bitwise ANDs, ORs, or XORs it into C or Z. The pin number is specified by D[5:0] (0-63). The WC, WZ, ANDC, ANDZ, ORC, ORZ, XORC, or XORZ effect determines how the pin state is applied to the selected flag.

TESTP reads the actual pin state from the IN register, not the output register. This makes it useful for reading sensor inputs, detecting edges, and building multi-bit values from pin states.

Common uses include Hall sensor reading for motor control, digital input edge detection, and pin state monitoring with conditional logic. The XOR operations are particularly useful for conditional inversion based on previous flag states.

---

## TESTPN — Test Pin Negated

Tests the state of an I/O pin, inverts the result, and writes to C or Z.

### Syntax
```pasm
        TESTPN  {#}D            WC/WZ
        TESTPN  {#}D            ANDC/ANDZ
        TESTPN  {#}D            ORC/ORZ
        TESTPN  {#}D            XORC/XORZ
```

### Result
The inverted state of the I/O pin described by D is read and either stored as-is, or bitwise ANDed, ORed, or XORed into C or Z.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register or 6-bit literal (0-63) identifying the I/O pin |
| WC/WZ | Write inverted pin state to C or Z flag |
| ANDC/ANDZ | AND inverted pin state with C or Z flag |
| ORC/ORZ | OR inverted pin state with C or Z flag |
| XORC/XORZ | XOR inverted pin state with C or Z flag |

### Encoding
\simpleencoding{EEEE | 1101011 | CZL | DDDDDDDDD | 001000001 | — | !IN[D[5:0]] | !IN[D[5:0]] | 2}

\simpleencoding{EEEE | 1101011 | CZL | DDDDDDDDD | 001000011 | — | C/Z AND !IN[D[5:0]] | C/Z AND !IN[D[5:0]] | 2}

\simpleencoding{EEEE | 1101011 | CZL | DDDDDDDDD | 001000101 | — | C/Z OR !IN[D[5:0]] | C/Z OR !IN[D[5:0]] | 2}

\simpleencoding{EEEE | 1101011 | CZL | DDDDDDDDD | 001000111 | — | C/Z XOR !IN[D[5:0]] | C/Z XOR !IN[D[5:0]] | 2}

### Related Instructions
- [TESTP](#testp) — Test pin state without inversion
- [TESTB](#testb) — Test bit in register
- [TESTBN](#testbn) — Test bit in register negated

### Explanation
TESTPN reads the state (0 or 1) of the I/O pin designated by D, inverts that result, and either stores it as-is, or bitwise ANDs, ORs, or XORs it into C or Z. The pin number is specified by D[5:0] (0-63). The WC, WZ, ANDC, ANDZ, ORC, ORZ, XORC, or XORZ effect determines how the inverted pin state is applied to the selected flag.

TESTPN is useful for testing whether a pin is low (0) rather than high (1), which is common when working with active-low signals.

---

## TJF — Test and Jump if Full

Tests a register value and jumps if it equals $FFFF_FFFF.

### Syntax
```pasm
        TJF     D, {#}S
```

### Result
D is tested and if it is full ($FFFF_FFFF), PC is set to a new relative (#S) or absolute (S) address.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register whose value is tested for full |
| S | Register, 9-bit literal, or 20-bit augmented literal specifying jump address |

### Encoding
\simpleencoding{EEEE | 1011101 | 00I | DDDDDDDDD | SSSSSSSSS | PC (conditional) | — | — | 2 or 4}

### Related Instructions
- [TJNF](#tjnf) — Test and jump if not full
- [TJZ](#tjz) — Test and jump if zero
- [TJNZ](#tjnz) — Test and jump if not zero

### Explanation
TJF tests the value in D and jumps to the address described by S if the result is full (= -1; = $FFFF_FFFF).

The address (S) can be absolute or relative. To specify an absolute address, S must be a register containing a 20-bit address value. To specify a relative address, use #Label for a 9-bit signed offset (a range of -256 to +255 instructions) or use ##Label (or insert a prior AUGS instruction) for a 20-bit signed offset (a range of -524288 to +524287). Offsets are relative to the instruction following the TJF. The signed offset value is in units of whole instructions—it is added to PC as-is when in Cog/LUT execution mode and is multiplied by 4 then added to PC when in Hub execution mode.

The instruction takes 2 cycles if the jump is not taken, or 4 cycles if taken (13-20 cycles for Hub execution when taken).

---

## TJNF — Test and Jump if Not Full

Tests a register value and jumps if it does not equal $FFFF_FFFF.

### Syntax
```pasm
        TJNF    D, {#}S
```

### Result
D is tested and if it is not full (<> $FFFF_FFFF), PC is set to a new relative (#S) or absolute (S) address.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register whose value is tested for not full |
| S | Register, 9-bit literal, or 20-bit augmented literal specifying jump address |

### Encoding
\simpleencoding{EEEE | 1011101 | 01I | DDDDDDDDD | SSSSSSSSS | PC (conditional) | — | — | 2 or 4}

### Related Instructions
- [TJF](#tjf) — Test and jump if full
- [TJZ](#tjz) — Test and jump if zero
- [TJNZ](#tjnz) — Test and jump if not zero
- [TJS](#tjs) — Test and jump if signed
- [TJNS](#tjns) — Test and jump if not signed

### Explanation
TJNF tests the value in D and jumps to the address described by S if the result is not full (<> -1; <> $FFFF_FFFF).

The address (S) can be absolute or relative. To specify an absolute address, S must be a register containing a 20-bit address value. To specify a relative address, use #Label for a 9-bit signed offset (a range of -256 to +255 instructions) or use ##Label (or insert a prior AUGS instruction) for a 20-bit signed offset (a range of -524288 to +524287). Offsets are relative to the instruction following the TJNF. The signed offset value is in units of whole instructions—it is added to PC as-is when in Cog/LUT execution mode and is multiplied by 4 then added to PC when in Hub execution mode.

The instruction takes 2 cycles if the jump is not taken, or 4 cycles if taken (2 or 13-20 cycles for Hub execution).

---

## TJNS — Test and Jump if Not Signed

Tests a register value and jumps if bit 31 is clear (positive/unsigned).

### Syntax
```pasm
        TJNS    D, {#}S
```

### Result
D is tested and if it is not signed (D[31] = 0), PC is set to a new relative (#S) or absolute (S) address.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register whose value is tested for sign bit |
| S | Register, 9-bit literal, or 20-bit augmented literal specifying jump address |

### Encoding
\simpleencoding{EEEE | 1011101 | 11I | DDDDDDDDD | SSSSSSSSS | PC (conditional) | — | — | 2 or 4}

### Related Instructions
- [TJS](#tjs) — Test and jump if signed
- [TJZ](#tjz) — Test and jump if zero
- [TJNZ](#tjnz) — Test and jump if not zero

### Explanation
TJNS tests the value in D and jumps to the address described by S if the value is not signed (D[31] = 0). The address (S) can be absolute or relative. To specify an absolute address, S must be a register containing a 20-bit address value. To specify a relative address, use #Label for a 9-bit signed offset (a range of -256 to +255 instructions) or use ##Label (or insert a prior AUGS instruction) for a 20-bit signed offset. Offsets are relative to the instruction following the TJNS.

The instruction takes 2 cycles if the jump is not taken, or 4 cycles if taken.

---

## TJNZ — Test and Jump if Not Zero

Tests a register value and jumps if it is not zero.

### Syntax
```pasm
        TJNZ    D, {#}S
```

### Result
D is tested and if it is not zero, PC is set to a new relative (#S) or absolute (S) address.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register whose value is tested for not zero |
| S | Register, 9-bit literal, or 20-bit augmented literal specifying jump address |

### Encoding
\simpleencoding{EEEE | 1011100 | 11I | DDDDDDDDD | SSSSSSSSS | PC (conditional) | — | — | 2 or 4}

### Related Instructions
- [TJZ](#tjz) — Test and jump if zero
- [TJF](#tjf) — Test and jump if full
- [TJNF](#tjnf) — Test and jump if not full
- [TJS](#tjs) — Test and jump if signed
- [TJNS](#tjns) — Test and jump if not signed

### Explanation
TJNZ tests the value in D and jumps to the address described by S if the result is not zero.

The address (S) can be absolute or relative. To specify an absolute address, S must be a register containing a 20-bit address value. To specify a relative address, use #Label for a 9-bit signed offset or use ##Label for a 20-bit signed offset. Offsets are relative to the instruction following the TJNZ.

The instruction takes 2 cycles if the jump is not taken, or 4 cycles if taken.

---

## TJS — Test and Jump if Signed

Tests a register value and jumps if bit 31 is set (negative).

### Syntax
```pasm
        TJS     D, {#}S
```

### Result
D is tested and if it is signed (D[31] = 1), PC is set to a new relative (#S) or absolute (S) address.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register whose value is tested for sign bit |
| S | Register, 9-bit literal, or 20-bit augmented literal specifying jump address |

### Encoding
\simpleencoding{EEEE | 1011101 | 10I | DDDDDDDDD | SSSSSSSSS | PC (conditional) | — | — | 2 or 4}

### Related Instructions
- [TJNS](#tjns) — Test and jump if not signed
- [TJF](#tjf) — Test and jump if full
- [TJNF](#tjnf) — Test and jump if not full
- [TJZ](#tjz) — Test and jump if zero
- [TJNZ](#tjnz) — Test and jump if not zero

### Explanation
TJS tests the value in D and jumps to the address described by S if the result is signed (D[31] = 1).

The address (S) can be absolute or relative. To specify an absolute address, S must be a register containing a 20-bit address value. To specify a relative address, use #Label for a 9-bit signed offset (a range of -256 to +255 instructions) or use ##Label (or insert a prior AUGS instruction) for a 20-bit signed offset (a range of -524288 to +524287). Offsets are relative to the instruction following the TJS. The signed offset value is in units of whole instructions—it is added to PC as-is when in Cog/LUT execution mode and is multiplied by 4 then added to PC when in Hub execution mode.

The instruction takes 2 cycles if the jump is not taken, or 4 cycles if taken (2 or 13-20 cycles for Hub execution).

---

## TJV — Test and Jump if Overflow

Tests a register value against the C flag and jumps if overflow occurred.

### Syntax
```pasm
        TJV     D, {#}S
```

### Result
D is tested against C and if it has overflowed (D[31] != C), PC is set to a new relative (#S) or absolute (S) address.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register whose value is tested for overflow |
| S | Register, 9-bit literal, or 20-bit augmented literal specifying jump address |

### Encoding
\simpleencoding{EEEE | 1011110 | 00I | DDDDDDDDD | SSSSSSSSS | PC (conditional) | — | — | 2 or 4}

### Related Instructions
- [ADDS](instructions-a.md#adds) — Add signed with overflow detection
- [ADDSX](instructions-a.md#addsx) — Add signed extended with overflow detection
- [SUBS](instructions-s.md#subs) — Subtract signed with overflow detection
- [SUBSX](instructions-s.md#subsx) — Subtract signed extended with overflow detection

### Explanation
TJV tests the value in D against C and jumps to the address described by S if D has overflowed (D[31] != C). This instruction requires that C be updated (to the correct sign) by the previous ADDS, ADDSX, SUBS, SUBSX, CMPS, CMPSX, or SUMx instruction. The address (S) can be absolute or relative. To specify an absolute address, S must be a register containing a 20-bit address value. To specify a relative address, use #Label for a 9-bit signed offset (a range of -256 to +255 instructions) or use ##Label (or insert a prior AUGS instruction) for a 20-bit signed offset. Offsets are relative to the instruction following the TJV. The signed offset value is in units of whole instructions—it is added to PC as-is when in Cog/LUT execution mode and is multiplied by 4 then added to PC when in Hub execution mode (long-aligned Hub code not required).

The instruction takes 2 cycles if the jump is not taken, or 4 cycles if taken (2 or 13-20 cycles for Hub execution when taken).

---

## TJZ — Test and Jump if Zero

Tests a register value and jumps if it equals zero.

### Syntax
```pasm
        TJZ     D, {#}S
```

### Result
D is tested and if it is zero, PC is set to a new relative (#S) or absolute (S) address.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register whose value is tested for zero |
| S | Register, 9-bit literal, or 20-bit augmented literal specifying jump address |

### Encoding
\simpleencoding{EEEE | 1011100 | 10I | DDDDDDDDD | SSSSSSSSS | PC (conditional) | — | — | 2 or 4}

### Related Instructions
- [TJNZ](#tjnz) — Test and jump if not zero
- [TJF](#tjf) — Test and jump if full
- [TJNF](#tjnf) — Test and jump if not full

### Explanation
TJZ tests the value in D and jumps to the address described by S if the result is zero.

The address (S) can be absolute or relative. To specify an absolute address, S must be a register containing a 20-bit address value. To specify a relative address, use #Label for a 9-bit signed offset or use ##Label for a 20-bit signed offset. Offsets are relative to the instruction following the TJZ.

The instruction takes 2 cycles if the jump is not taken, or 4 cycles if taken (2 or 13-20 cycles for Hub execution when taken).

---

## TRGINT1 / TRGINT2 / TRGINT3 — Trigger Interrupt {#trgint1}

Software-triggers interrupt handler (INT1, INT2, or INT3).

### Syntax
```pasm
        TRGINT1
        TRGINT2
        TRGINT3
```

### Result
The specified interrupt handler (INT1, INT2, or INT3) is triggered regardless of STALLI mode.

### Parameters
None.

### Encoding
| Instruction | Encoding | C | Z | Clocks |
|-------------|----------|---|---|--------|
| TRGINT1 | `EEEE 1101011 000 000100010 000100100` | — | — | 2 |
| TRGINT2 | `EEEE 1101011 000 000100011 000100100` | — | — | 2 |
| TRGINT3 | `EEEE 1101011 000 000100100 000100100` | — | — | 2 |

### Related Instructions
- [SETINT1/2/3](instructions-s.md#setint1) — Set interrupt handler
- [NIXINT1/2/3](instructions-n.md#nixint1) — Cancel interrupt
- [RETI0/1/2/3](instructions-r.md#reti0) — Return from interrupt
- [STALLI](instructions-s.md#stalli) — Stall on interrupt

### Explanation
TRGINT1, TRGINT2, and TRGINT3 software-trigger the corresponding interrupt handler, regardless of STALLI mode. This allows code to explicitly invoke interrupt service routines without waiting for external events.

The P2 provides three independent interrupt levels. Each TRGINT instruction triggers only its corresponding level. These instructions are useful for testing interrupt handlers or for implementing software-generated interrupts.
