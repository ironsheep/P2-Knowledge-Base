# PTRA/PTRB Complete Findings

## Overview
PTRA and PTRB are special pointer registers in the P2 used for efficient hub memory access with auto-increment/decrement capabilities.

## Register Addresses
- **PTRA**: COG RAM address $1F8 (special-purpose register)
- **PTRB**: COG RAM address $1F9 (special-purpose register)
- **Size**: 32 bits each
- **Purpose**: Pointer A/B to hub RAM

## WW Field Encoding (for CALLD/LOC instructions)
- **WW = 00**: PA register
- **WW = 01**: PB register
- **WW = 10**: PTRA register  
- **WW = 11**: PTRB register

## Addressing Capabilities

### Basic Ranges
- **With update**: -16 to +16 
- **Without update**: -32 to +31
- These are INDEX values that get multiplied by SCALE

### SCALE Values (automatic based on instruction)
**Critical**: S bit in PTR expression encoding determines PTRA vs PTRB
- S = 0 for PTRA
- S = 1 for PTRB

Scale multipliers:
- **RDBYTE/WRBYTE**: SCALE = 1
- **RDWORD/WRWORD**: SCALE = 2  
- **RDLONG/WRLONG/WMLONG**: SCALE = 4

## PTR Expression Encoding

### Encoding Format: 1SUPNNNNN
- **Bit 8 (1)**: Always 1 to indicate PTR expression
- **Bit 7 (S)**: 0=PTRA, 1=PTRB
- **Bit 6 (U)**: 0=keep PTRx same, 1=update PTRx
- **Bit 5 (P)**: 0=use PTRx+offset, 1=use PTRx (post-modify)
- **Bits 4-0 (NNNNN)**: Index value

### Basic Forms
```
100000000  PTRA                'use PTRA
110000000  PTRB                'use PTRB
100IIIIII  PTRA[INDEX6]        'use PTRA + INDEX6*SCALE
110IIIIII  PTRB[INDEX6]        'use PTRB + INDEX6*SCALE
```

### Auto-increment/decrement Forms
```
101100001  PTRA++              'use PTRA, PTRA += 1*SCALE
111100001  PTRB++              'use PTRB, PTRB += 1*SCALE
101011111  PTRA--              'use PTRA, PTRA -= 1*SCALE
111011111  PTRB--              'use PTRB, PTRB -= 1*SCALE
101111111  ++PTRA              'use PTRA + 1*SCALE, PTRA += 1*SCALE
111111111  ++PTRB              'use PTRB + 1*SCALE, PTRB += 1*SCALE
101011111  --PTRA              'use PTRA - 1*SCALE, PTRA -= 1*SCALE
111011111  --PTRB              'use PTRB - 1*SCALE, PTRB -= 1*SCALE
```

### Indexed Auto-increment/decrement Forms
```
1011NNNNN  PTRA++[INDEX]       'use PTRA, PTRA += INDEX*SCALE
1111NNNNN  PTRB++[INDEX]       'use PTRB, PTRB += INDEX*SCALE
1010NNNNN  PTRA--[INDEX]       'use PTRA, PTRA -= INDEX*SCALE
1110NNNNN  PTRB--[INDEX]       'use PTRB, PTRB -= INDEX*SCALE
```

Where INDEX = 1..16 for the 5-bit NNNNN field.

## Usage in Instructions

### Random Access Interface
Per Silicon Doc RANDOM ACCESS INTERFACE section:
- PTR expressions can use 5-bit scaled index (no AUGS)
- PTR expressions can use 20-bit unscaled index (with AUGS)
- When AUGS augments #S to 32 bits: #%1SUPNNNNN format applies

### Read/Write Instructions
All RDxxxx/WRxxxx instructions can use PTR expressions:
- **RDBYTE D,PTRA** - Read byte at PTRA into D
- **RDWORD D,PTRA--** - Read word at PTRA into D, PTRA -= 1*2
- **RDLONG D,++PTRB[10]** - Read long at PTRB + 10*4 into D, PTRB += 10*4
- **WRBYTE D,--PTRA** - Write lower byte in D at PTRA - 1*1, PTRA -= 1*1
- **WRWORD D,PTRB[-7]** - Write lower word in D to PTRB - 7*2
- **WRLONG #10,PTRB++** - Write long value 10 at PTRB, PTRB += 1*4

### Block Moves with SETQ
Fast block moves using SETQ override the index with the number of longs:
```
SETQ #x
RDLONG first_reg,PTRA        'read x+1 longs from PTRA

SETQ #x  
RDLONG first_reg,PTRA++      'read x+1 longs from PTRA, PTRA += (x+1)*4

SETQ #x
RDLONG first_reg,PTRA--      'read x+1 longs from PTRA, PTRA -= (x+1)*4

SETQ #x
RDLONG first_reg,++PTRA      'read x+1 longs from PTRA+(x+1)*4, PTRA += (x+1)*4

SETQ #x
RDLONG first_reg,--PTRA      'read x+1 longs from PTRA-(x+1)*4, PTRA -= (x+1)*4
```

## COGINIT Integration

### PTRA Initialization
- If COGINIT is preceded by SETQ, the SETQ value goes into target cog's PTRA
- If no SETQ is used, target cog's PTRA is cleared to zero
- This provides a convenient way to pass 32-bit parameters to newly started cogs

### PTRB Initialization  
- The S operand of COGINIT is written into target cog's PTRB register
- This is the hub/cog address from which the target cog will begin executing

Examples:
```
COGINIT #1,#$100              'load and start cog 1 from $100, PTRB = $100

COGINIT #%1_0_0101,PTRA       'start cog 5 at PTRA

SETQ ptra_val
COGINIT #%0_1_0000,addr       'ptra_val goes into target cog's PTRA
                              'load and start a free cog at addr
```

## Special Instructions

### GETPTR - Get FIFO Hub Pointer
**Encoding**: `EEEE 1101011 000 DDDDDDDDD 000110100`
**Group**: Hub FIFO
**Purpose**: Get current FIFO hub pointer into D
**Timing**: 2 clocks normally, "FIFO IN USE" when FIFO active
**CSV Row**: 328

**Important**: GETPTR returns the FIFO hub pointer, NOT PTRA/PTRB values directly.
- Used with EXECF to write FIFO pointer to PB: `MOV PB,(GETPTR)`
- Works with the hub FIFO system, not direct PTRA/PTRB access

## PTR Expression Syntax Rules

### Encoding Structure
- Bit 8: 0 for PTRA, 1 for PTRB  
- Bits 7-6: Operation type (00=base, 01=decrement, 10=increment, 11=pre-modify)
- Bits 5-0: Index value or operation specifier

### Important Notes
1. PTR expressions cannot have arbitrary index values in fast block moves
2. Index is overridden with number of longs in SETQ block operations
3. Bit 4 of encoded index serves as ++/-- indicator in block moves
4. Plain PTRA/PTRB cases have index overridden with zero in block moves

## CRITICAL KNOWN BUG - SETQ Block Operations

### Bug Description
**Intervening ALTx/AUGS/AUGD instructions between SETQ/SETQ2 and RDLONG/WRLONG/WMLONG-PTRx will cancel the special-case block-size PTRx deltas.**

### Impact
- Expected number of longs will still transfer
- PTRx will only increment/decrement by normal amount (1 long), not block size
- This breaks expected PTRx updates in block transfers

### Example
```pasm
SETQ    #16-1           'ready to load 16 longs
ALTD    start_reg       'ALTD cancels block-size PTRx deltas!
RDLONG  0,ptra++        'ptra increments by 4, not 64!
```

### Workaround
**NEVER place ALTx, AUGS, or AUGD between SETQ and block transfer with PTRx**

## Complete Instruction Access Methods

### Direct Register Access
```pasm
MOV     PTRA, value      ' Direct write to $1F8
MOV     PTRB, value      ' Direct write to $1F9
MOV     dest, PTRA       ' Direct read from $1F8
MOV     dest, PTRB       ' Direct read from $1F9
```

### CALLD/LOC with WW Field
```pasm
CALLD   PTRA, #address   ' WW=10, save return to PTRA
CALLD   PTRB, #address   ' WW=11, save return to PTRB
LOC     PTRA, #\address  ' WW=10, load address to PTRA
LOC     PTRB, #\address  ' WW=11, load address to PTRB
```

### PTR Expressions in Memory Operations
```pasm
RDLONG  D, PTRA          ' Read using PTRA (S=100000000)
RDLONG  D, PTRB          ' Read using PTRB (S=110000000)
WRLONG  D, PTRA++        ' Write and increment PTRA
WRLONG  D, PTRB--        ' Write and decrement PTRB
```

## What's Still Missing
1. Any special restrictions on PTRA/PTRB usage in hub exec mode
3. Initial values of PTRA/PTRB on cog startup (besides COGINIT)
4. Whether PTRA/PTRB can be directly written with MOV or only via PTR expressions
5. Interaction with interrupts (are PTRA/PTRB saved/restored?)

## Source References
- Silicon Doc p2-documentation.txt: 
  - COG RAM section: Lines 935-954 (register addresses $1F8/$1F9)
  - WW field encoding: Lines 667-669
  - PTR expressions: Lines 6943-7150, 7219-7267
  - RANDOM ACCESS INTERFACE: Lines 6850-6937
  - BRANCH ADDRESSING: Lines 1292-1352
  - KNOWN BUGS: Lines 197-227
- CSV "P2 Instructions v35": 
  - GETPTR instruction: Row 328
  - Column D contains instruction encodings
- Chip Gracey clarifications: (none specific to PTRA/PTRB yet)