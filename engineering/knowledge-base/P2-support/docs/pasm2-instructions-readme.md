# PASM2 Instructions

## Overview
Complete collection of P2 Assembly (PASM2) instruction definitions.

## Categories
Instructions are logically grouped but stored as individual files:
- **Math Operations**: ADD, SUB, MUL, DIV, etc.
- **Logic Operations**: AND, OR, XOR, NOT, etc.
- **Branch/Jump**: JMP, CALL, RET, TJZ, etc.
- **Memory Access**: RD*, WR*, MOV, etc.
- **Smart Pin Control**: WRPIN, RDPIN, etc.
- **CORDIC Operations**: QROTATE, QVECTOR, etc.
- **Special Functions**: HUBSET, COGINIT, etc.

## File Format
Each `.yaml` file contains complete instruction documentation following the repository schema.

## Extraction Sources
1. P2-Instruction-Set.csv - Base definitions
2. P2-Datasheet-v35 - Timing and encoding
3. Silicon-Doc-v35 - Detailed narratives
4. Forum posts - Clarifications and edge cases

## Coverage Status
- Total PASM2 instructions: ~500
- Currently extracted: [Building]
- Average completeness: [Tracking]