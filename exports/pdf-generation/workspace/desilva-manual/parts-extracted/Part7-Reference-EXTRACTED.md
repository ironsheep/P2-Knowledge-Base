# Appendix A: Instruction Set Reference

## Quick Reference Format

Each instruction entry includes:
- Syntax
- Operation
- Flags affected
- Timing
- Example

## Memory Access Instructions

### RDBYTE - Read Byte from Hub
```
Syntax:  RDBYTE D, S/# {WZ/WC}
Operation: D = byte at hub[S]
Flags:    Z = (D == 0), C = D[7]
Timing:   2-9 clocks
Example:  RDBYTE value, hubaddr wz
```

### RDWORD - Read Word from Hub
```
Syntax:  RDWORD D, S/# {WZ/WC}
Operation: D = word at hub[S]
Flags:    Z = (D == 0), C = D[15]
Timing:   2-9 clocks
```

### RDLONG - Read Long from Hub
```
Syntax:  RDLONG D, S/# {WZ/WC}
Operation: D = long at hub[S]
Flags:    Z = (D == 0), C = D[31]
Timing:   2-9 clocks
```

[Continue with all instruction categories...]

---

*For complete instruction details, see the P2 Silicon Documentation*

---

# Index

## A
- ADC operations: Ch15
- ADD instruction: Ch3, Ch5
- Address modes: Ch3
- ALTD/ALTS: Ch3
- Architecture: Ch2
- Assembly basics: Ch3

## B
- Bit manipulation: Ch3
- Block transfers: Ch4, Ch9
- Booleans: Ch3

## C
- C flag: Ch6
- CALL/RET: Ch3
- Clock timing: Ch2
- CMP instruction: Ch6
- COG anatomy: Ch2
- COG communication: Ch2, Ch16
- Conditional execution: Ch3, Ch6
- CORDIC: Ch7
- Counters: Ch2

## D
- DAC operations: Ch15
- Debugging: Ch12
- Division: Ch5
- DRVH/DRVL: Ch1

## E
- Egg beater: Ch2, Ch4

## F
- FIFO: Ch4, Ch9
- Flags: Ch6
- Flow control: Ch3

## G
- GETMULH: Ch5
- GETQX/GETQY: Ch7

## H
- Hardware multiply: Ch5
- HDMI: Ch13
- Hub execution: Ch10
- Hub memory: Ch2, Ch4

## I
- I2C: Ch14
- Immediate values: Ch3
- Instruction format: Ch3
- Interrupts: Ch11

## J
- JMP instruction: Ch3

## L
- LED control: Ch1
- Locks: Ch2, Ch16
- Logic operations: Ch3

## M
- Mailboxes: Ch2, Ch16
- Mathematics: Ch5
- Memory access: Ch4
- MOV instruction: Ch3
- MUL/MULS: Ch5
- Multi-COG: Ch16

## O
- Optimization: Ch12

## P
- Parallel processing: Ch2
- Pipeline: Ch7, Ch12
- Pins, Smart: Ch8
- PTRA/PTRB: Ch3, Ch4
- PWM: Ch8

## Q
- Q flag: Ch7
- QDIV: Ch5
- QROTATE: Ch7

## R
- RDBYTE/RDWORD/RDLONG: Ch4
- REP instruction: Ch3
- Rotation: Ch3, Ch7

## S
- Serial protocols: Ch14
- Shift operations: Ch3
- Signal processing: Ch15
- SKIP instruction: Ch3, Ch6
- Smart Pins: Ch8
- SPI: Ch14
- Streamer: Ch9

## T
- Timer: Ch2
- Timing: Ch2, Ch12
- Trigonometry: Ch7

## U
- UART: Ch8, Ch14

## V
- VGA: Ch13
- Video generation: Ch13

## W
- WAITX: Ch1
- WRBYTE/WRWORD/WRLONG: Ch4

## Z
