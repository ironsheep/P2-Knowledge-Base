# WW Field Encoding for PA/PB/PTRA/PTRB

## Overview
The WW field is a 2-bit field in certain P2 instructions that specifies which special register (PA, PB, PTRA, or PTRB) to write to.

## Source Reference
Silicon Doc p2-documentation.txt, Line 667-669:
> WW - Index of special register (PA, PB, PTRA, or PTRB) to write.

## WW Field Encoding Values

| WW Bits | Register | Description |
|---------|----------|-------------|
| 00      | PA       | Write to PA register |
| 01      | PB       | Write to PB register | 
| 10      | PTRA     | Write to PTRA register |
| 11      | PTRB     | Write to PTRB register |

## Instructions Using WW Field

### CALLD - Call with Destination Save
**Encoding**: `EEEE 11100WW RAA AAAAAAAAA AAAAAAAAA`
- Saves return address to register specified by WW field
- WW determines which register (PA/PB/PTRA/PTRB) gets the return address

**Examples**:
```pasm
CALLD   PA, #routine    ' WW=00, return address saved to PA
CALLD   PB, #routine    ' WW=01, return address saved to PB  
CALLD   PTRA, #routine  ' WW=10, return address saved to PTRA
CALLD   PTRB, #routine  ' WW=11, return address saved to PTRB
```

### LOC - Load Object Code Address
**Encoding**: `EEEE 11101WW RAA AAAAAAAAA AAAAAAAAA`
- Loads address into register specified by WW field
- WW determines which register receives the address

**Examples**:
```pasm
LOC     PA, #\address    ' WW=00, address loaded to PA
LOC     PB, #\address    ' WW=01, address loaded to PB
LOC     PTRA, #\address  ' WW=10, address loaded to PTRA  
LOC     PTRB, #\address  ' WW=11, address loaded to PTRB
```

## Branch Addressing Context

Per Silicon Doc BRANCH ADDRESSING section:
- CALLPA/CALLPB/DJZ..JNXRL/JNATN/JNQMT use relative/indirect addressing
- JMP/CALL/CALLA/CALLB/CALLD use absolute/relative/indirect addressing  
- LOC uses absolute/relative addressing
- The WW field in CALLD/LOC determines which special register receives the address/return

## Related Instructions Without WW Field

### CALLPA/CALLPB - Call with PA/PB Save
**Encoding**: `EEEE 1011010 1LI DDDDDDDDD SSSSSSSSS`
- These instructions implicitly save to PA or PB (encoded in opcode, not WW field)
- CALLPA always saves return to PA
- CALLPB always saves return to PB
- Note: These cannot save to PTRA/PTRB

## Key Understanding Points

1. **WW is a 2-bit field** that maps directly to the four special registers
2. **Not all CALL variants use WW** - CALLPA/CALLPB have fixed destinations
3. **CALLD is more flexible** than CALLPA/CALLPB because it can target all 4 registers
4. **LOC also uses WW** for loading addresses into any of the 4 special registers

## Instruction Format Context
When reading P2 instruction encodings:
- EEEE = Conditional test (4 bits)
- WW = Special register index (2 bits) 
- R = Relative/Absolute addressing (1 bit)
- AA/AAAAAAAAA = Address bits (20 bits total)

## Why This Matters
Understanding the WW field is critical for:
1. Correctly encoding instructions that save to special registers
2. Understanding which registers can be targets for return addresses
3. Implementing assemblers/disassemblers
4. Generating correct machine code

## Cross-Reference
- PA/PB registers: General purpose special registers
- PTRA/PTRB registers: Pointer registers with auto-increment/decrement
- CALLD instruction: More flexible than CALLPA/CALLPB
- LOC instruction: Load addresses into special registers