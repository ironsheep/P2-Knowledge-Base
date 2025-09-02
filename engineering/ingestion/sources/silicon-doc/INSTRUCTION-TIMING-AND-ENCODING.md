# P2 Instruction Timing and Encoding - Critical Documentation

## Source References
- Silicon Doc p2-documentation.txt: Assembly Language section (Lines 9547+)
- Instructions.txt file referenced in doc
- CSV file column D contains matching encodings

## Instruction Pipeline Timing Diagram

From Silicon Doc Assembly Language section:

```
                        clk
_________------------____________------------____________------------____________
         |           |           |           |           |           |
rdRAM Ib |-------+   |           |           |           |           |
         |       |   |           |           |           |           |
rdRAM Ic |       |   |-------+   |           |           |           |
         |       |   |       |   |           |           |           |
         |       |   |       |   |           |           |           |
latch Da |---+   |   |       |   |           |           |           |
         +----> rdRAM Db |------------> latch Db                     |
latch Sa |---+   |   |       |   |           |           |           |
         +----> rdRAM Sb |------------> latch Sb                     |
latch Ia |---+   |   |       |   |           |           |           |
         +----> latch Ib |------------> latch Ib                     |
         |       |   |       |   |           |           |           |
         |       |   |       |   |           +------------------ALU-----------> wrRAM Ra
         |       |   |       |   |           |           |           |
         |       |   |       |   | stall/done = 'gox'    |           |
         |       |   |       |   |           |           |           |
         |       'get'       |   |       done = 'go'     |           |
         |                   |   |           |           |           |
rdRAM Id |                   |   |-------+   |           |           |
         |                   |   |       |   |           |           |
         |                   |   |       |   |           |           |
         |                   |---+       |   |           |           |
         |                   +----> rdRAM Dc |------------> latch Dc |
         |                   |---+       |   |           |           |
         |                   +----> rdRAM Sc |------------> latch Sc |
         |                   |---+       |   |           |           |
         |                   +----> latch Ic |------------> latch Ic |
         |                   |           |   |           |           |
```

## Key Pipeline Stages

1. **Instruction Fetch** (rdRAM I)
2. **Decode/Register Read** (rdRAM D/S)  
3. **Latch** (latch D/S/I)
4. **ALU Operation**
5. **Write Back** (wrRAM R)

## Timing Characteristics

- **5-stage pipeline** when full
- **2-clock execution** for most math/logic instructions
- **6-clock bytecode executor** for interpreted languages
- **Branch instructions flush pipeline** - next instruction takes 5+ clocks
- **Conditionally canceled instructions** move through pipeline in 2 clocks without executing

## GETPTR and Related Instructions

### GETPTR - Get Pointer Value
**Encoding**: Part of special register access group  
**Purpose**: Returns current PTR value (used with EXECF)
**Usage Example**: `MOV PB,(GETPTR)` - Write FIFO pointer to PB

### GETBRK - Get Break/Debug Status  
**Encoding**: Part of debug instruction group
**Forms**:
- `GETBRK D WCZ` - Returns cog internal status
- `GETBRK D WC` - Returns SKIP/SKIPF/EXECF/XBYTE pattern info
- `GETBRK D WZ` - Returns pattern queue status

### COGBRK - Trigger Breakpoint in Another Cog
**Purpose**: Trigger asynchronous breakpoint in target cog
**D/#**: %CCCC - target cog ID

### BRK - Breakpoint
**Purpose**: Generate debug interrupt with 8-bit code
**D/#**: %BBBBBBBB - 8-bit BRK code

### SETLUTS - Enable LUT Sharing
**Encoding**: EEEE 1101011 ... 000110111
**Purpose**: Enable/disable LUT RAM writes from adjacent cog
- `SETLUTS #0` - Disallow writes from other cog (default)
- `SETLUTS #1` - Allow writes from other cog

## Instruction Encoding Format Key

Per Silicon Doc COGS section:

| Field | Bits | Description |
|-------|------|-------------|
| EEEE | 4 | Conditional test (see condition codes) |
| C | 1 | 0=Don't update C, 1=Update C (WC) |
| Z | 1 | 0=Don't update Z, 1=Update Z (WZ) |
| I | 1 | 0=S is register, 1=S is immediate (#) |
| L | 1 | 0=D is register, 1=D is immediate (#) |
| R | 1 | 0=Relative address, 1=Absolute address |
| WW | 2 | Special register index (PA/PB/PTRA/PTRB) |
| DDDDDDDDD | 9 | Destination field |
| SSSSSSSSS | 9 | Source field |

## Cross-Reference with CSV

The CSV file column D contains these same instruction encodings in format:
`EEEE OOOOOOO CZI DDDDDDDDD SSSSSSSSS`

Where OOOOOOO is the 7-bit opcode field.

## Critical Understanding

1. **Pipeline awareness** is crucial for optimization
2. **2-clock baseline** for math/logic operations  
3. **Branch penalty** of 3+ additional clocks
4. **Conditional execution** doesn't save time (still 2 clocks)
5. **GETPTR** is special - returns internal pointer state
6. **Debug instructions** have dual behavior (normal vs debug ISR)

## Why This Matters

- **For optimization**: Understanding pipeline helps avoid stalls
- **For timing**: Know exact cycle counts for critical paths
- **For debugging**: GETBRK/BRK/COGBRK provide powerful debug capabilities
- **For code generation**: Proper encoding essential for machine code