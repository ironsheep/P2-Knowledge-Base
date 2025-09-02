# COG RAM Register Map - Complete Documentation

## Overview
Each cog has a 512 x 32-bit dual-port RAM (addresses $000-$1FF) with three distinct regions:
1. General-purpose registers ($000-$1EF)
2. Dual-purpose registers ($1F0-$1F7)
3. Special-purpose registers ($1F8-$1FF)

## Register Map

### General-Purpose Registers ($000-$1EF)
- **496 registers** for code and data usage
- Standard RAM accessible by all instructions
- No special functions

### Dual-Purpose Registers ($1F0-$1F7)

| Address | Normal Use | Special Function | Purpose When Special |
|---------|------------|------------------|----------------------|
| $1F0 | RAM | IJMP3 | Interrupt call address for INT3 |
| $1F1 | RAM | IRET3 | Interrupt return address for INT3 |
| $1F2 | RAM | IJMP2 | Interrupt call address for INT2 |
| $1F3 | RAM | IRET2 | Interrupt return address for INT2 |
| $1F4 | RAM | IJMP1 | Interrupt call address for INT1 |
| $1F5 | RAM | IRET1 | Interrupt return address for INT1 |
| $1F6 | RAM | PA | CALLD-imm parameter, or LOC address |
| $1F7 | RAM | PB | CALLD-imm parameter, or LOC address |

**Note**: These function as general RAM unless their special functions are enabled.

### Special-Purpose Registers ($1F8-$1FF)

| Address | Register | Description | Access |
|---------|----------|-------------|--------|
| **$1F8** | **PTRA** | Pointer A to hub RAM | R/W |
| **$1F9** | **PTRB** | Pointer B to hub RAM | R/W |
| $1FA | DIRA | Output enables for P31..P0 | R/W |
| $1FB | DIRB | Output enables for P63..P32 | R/W |
| $1FC | OUTA | Output states for P31..P0 | R/W |
| $1FD | OUTB | Output states for P63..P32 | R/W |
| $1FE | INA * | Input states for P31..P0 | R only |
| $1FF | INB ** | Input states for P63..P32 | R only |

\* INA becomes IJMP0 (R/W) during debug ISR  
\*\* INB becomes IRET0 (R/W) during debug ISR

## Critical Details

### PTRA/PTRB Registers ($1F8/$1F9)
- **32-bit pointers** to hub RAM
- Support auto-increment/decrement operations
- Can be used with PTR expressions in RDxxxx/WRxxxx instructions
- Initialized by COGINIT:
  - PTRA: Gets SETQ value if present, else cleared to 0
  - PTRB: Gets S operand of COGINIT (execution start address)

### Debug ISR Special Behavior
- During debug interrupts, INA/INB transform:
  - INA ($1FE) → IJMP0 (R/W) - debug ISR jump address
  - INB ($1FF) → IRET0 (R/W) - debug ISR return address
- IJMP0 initialized to $1F8 on COGINIT (debug-ISR-entry routine)

### Execute-Only ROM at $1F8-$1FF
- Contains debug ISR entry/exit routines
- These addresses have dual purpose:
  - Normal operation: Special-purpose registers
  - Debug ISR: Execute-only ROM routines
- Debug entry routine at $1F8 performs register save/restore

## Instruction Access Examples

### Direct Register Access
```pasm
MOV     PTRA, ##$1000      ' Set PTRA to hub address $1000
MOV     PTRB, ##$2000      ' Set PTRB to hub address $2000
MOV     $1F8, ##$3000      ' Same as MOV PTRA, ##$3000
```

### Using in Instructions
```pasm
RDLONG  data, PTRA         ' Read long from hub at PTRA
WRLONG  value, PTRB++      ' Write long to hub at PTRB, increment PTRB by 4
MOV     DIRA, ##$FFFF_FFFF ' Set all P31..P0 as outputs
```

### COGINIT Initialization
```pasm
SETQ    #param_block       ' This value goes to target cog's PTRA
COGINIT #0, #entry_point   ' entry_point goes to target cog's PTRB
```

## Important Notes

1. **Special vs RAM Access**: When accessing $1F8-$1FF, you're accessing special registers, not underlying RAM
2. **Read-Only Registers**: INA/INB are read-only except during debug ISR
3. **Dual-Purpose Flexibility**: $1F0-$1F7 can be used as regular RAM if interrupts not needed
4. **Debug ROM Overlay**: $1F8-$1FF contain execute-only debug routines that overlay the special registers

## Why This Matters

### For Code Generation
- Know exact addresses for special registers
- Understand dual-purpose register availability
- Handle debug ISR transformations correctly

### For Optimization
- $1F0-$1F7 provide 8 extra registers if interrupts unused
- Direct addressing to $1F8-$1FF for special operations
- PTRA/PTRB at known addresses for pointer operations

### For Debugging
- Debug ISR entry always starts at $1F8
- INA/INB transform during debug for state management
- Special ROM routines handle register preservation

## Cross-Reference
- PTR expressions: See PTRA-PTRB-FINDINGS.md
- WW field encoding: See WW-FIELD-ENCODING.md
- Interrupt system: INT1/INT2/INT3 usage
- COGINIT: Initializes PTRA/PTRB