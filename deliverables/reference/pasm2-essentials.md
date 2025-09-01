# PASM2 Essential Instructions

*Quick Reference v0.1.0*

## Most Common Instructions

### Data Movement
```pasm2
MOV     dest, source      ' Copy source to dest
MOVBYTS dest, source, #n  ' Move bytes with pattern
SETS    dest, #value      ' Set source field (bits 8:0)
SETD    dest, #value      ' Set dest field (bits 17:9)
```

### Arithmetic
```pasm2
ADD     dest, source      ' dest = dest + source
SUB     dest, source      ' dest = dest - source  
MUL     dest, source      ' Unsigned 32x32→32
MULS    dest, source      ' Signed 32x32→32
```

### Logic
```pasm2
AND     dest, source      ' dest = dest AND source
OR      dest, source      ' dest = dest OR source
XOR     dest, source      ' dest = dest XOR source
NOT     dest              ' dest = NOT dest
```

### Bit Operations
```pasm2
SHL     dest, count       ' Shift left
SHR     dest, count       ' Shift right
ROL     dest, count       ' Rotate left
ROR     dest, count       ' Rotate right
REV     dest              ' Reverse bits
```

### Hub Memory Access
```pasm2
RDLONG  dest, ptr         ' Read long from hub
WRLONG  value, ptr        ' Write long to hub
RDBYTE  dest, ptr         ' Read byte from hub
WRBYTE  value, ptr        ' Write byte to hub
```

### Pin Control
```pasm2
DRVL    #pin              ' Drive pin low
DRVH    #pin              ' Drive pin high
DRVNOT  #pin              ' Toggle pin
TESTP   #pin         WC   ' Test pin → C
WAITPE  #pin              ' Wait pin edge
```

### Flow Control
```pasm2
JMP     #address          ' Jump to address
CALL    #address          ' Call subroutine
RET                       ' Return from subroutine
DJNZ    reg, #address     ' Decrement and jump if not zero
IJNZ    reg, #address     ' Increment and jump if not zero
```

### COG Control
```pasm2
COGINIT #n, #address      ' Start COG n
COGSTOP #n                ' Stop COG n
COGID   dest              ' Get current COG ID
```

### Timing
```pasm2
WAITX   ##cycles          ' Wait specified cycles
WAITCT1                   ' Wait for CT1 match
ADDCT1  dest, #delta      ' Add to CT1
GETCT   dest              ' Get system counter
```

## Condition Codes

### Flags
- **C**: Carry flag
- **Z**: Zero flag

### Conditional Execution
```pasm2
IF_C    ADD x, y          ' Execute if C = 1
IF_NC   ADD x, y          ' Execute if C = 0
IF_Z    ADD x, y          ' Execute if Z = 1
IF_NZ   ADD x, y          ' Execute if Z = 0
```

### Write Flags
```pasm2
ADD     x, y         WC   ' Write carry flag
ADD     x, y         WZ   ' Write zero flag
ADD     x, y         WCZ  ' Write both flags
```

## Immediate Values

### Small Immediates (9-bit)
```pasm2
MOV     x, #511           ' Max 9-bit value
ADD     x, #-256         ' Min 9-bit value
```

### Large Immediates (32-bit)
```pasm2
MOV     x, ##1000000      ' Use ## for > 9 bits
AUGD    #high_bits        ' Alternative: augment
MOV     x, #low_bits      ' destination field
```

## Special Registers

### COG Special Registers ($1F0-$1FF)
```
$1F0  IJMP3   Interrupt 3 jump
$1F1  IRET3   Interrupt 3 return
$1F2  IJMP2   Interrupt 2 jump
$1F3  IRET2   Interrupt 2 return
$1F4  IJMP1   Interrupt 1 jump
$1F5  IRET1   Interrupt 1 return
$1F6  PA      CALLD return address
$1F7  PB      CALLD parameter
$1F8  PTRA    Pointer A
$1F9  PTRB    Pointer B
$1FA  DIRA    Direction register A
$1FB  DIRB    Direction register B
$1FC  OUTA    Output register A
$1FD  OUTB    Output register B
$1FE  INA     Input register A
$1FF  INB     Input register B
```

## CORDIC Operations

### Start CORDIC
```pasm2
QROTATE x, y, angle       ' Rotate (x,y) by angle
QVECTOR x, y              ' Convert to polar
QMUL    x, y              ' Multiply
QDIV    x, y              ' Divide
QSQRT   x                 ' Square root
```

### Get CORDIC Result
```pasm2
GETQX   dest              ' Get X result
GETQY   dest              ' Get Y result
```

## Smart Pin Control

### Basic Setup
```pasm2
WRPIN   mode, #pin        ' Set pin mode
WXPIN   x, #pin           ' Set X parameter
WYPIN   y, #pin           ' Set Y parameter
RDPIN   dest, #pin        ' Read pin result
```

## Memory Alignment

### Hub Addresses
- **Byte**: Any address
- **Word**: Even addresses (bit 0 = 0)
- **Long**: Addresses divisible by 4 (bits 1:0 = 00)

## Timing Reference

### Instruction Cycles (typical)
- COG to COG: 2 clocks
- Hub random read: 9-16 clocks
- Hub sequential: 2 clocks
- CORDIC: 55-58 clocks
- WAITx: Variable

## Common Patterns

### Infinite Loop
```pasm2
loop    ' Do something
        ...
        JMP     #loop
```

### Subroutine
```pasm2
main    CALL    #mysub
        ...
        
mysub   ' Subroutine code
        ...
        RET
```

### Table Lookup
```pasm2
        MOV     index, #5
        ALTS    index, #table
        MOV     value, 0-0
        
table   LONG    $100, $200, $300
```

---

*P2 Quick Reference v0.1.0*
*Source: P2 Documentation v35, Parallax Inc.*