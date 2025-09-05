# Spin2 & PASM Integration - Critical Deep Dive

## Inline PASM Code - The Power of Mixed Execution

### The ORG...END Block

Inline PASM allows you to drop from high-level Spin2 directly into assembly within the same method. This is **NOT** like inline assembly in C - it's a complete context switch to machine code.

```spin2
PUB method() | localVar1, localVar2
  ' Spin2 code here
  x := 100
  
  ORG                    ' Start PASM, default at $000
    MOV localVar1, #200  ' Direct access to Spin2 variables!
    ADD localVar1, localVar2
    _RET_                ' Return to Spin2
  END
  
  ' Back in Spin2
  return localVar1       ' Returns modified value
```

### Critical Memory Map for Inline PASM

```
Cog Register Space:
$000-$11F: Your PASM code loads here (288 longs)
$120-$1D7: Spin2 interpreter (DO NOT TOUCH)
$1D8-$1DF: PR0-PR7 general purpose (8 longs)
$1E0-$1EF: First 16 method variables (16 longs) ← CRITICAL!
$1F0-$1FF: Special registers (IJMP, IRET, PA, PB, INA, etc.)

LUT Space:
$000-$00F: Available for your use (16 longs)
$010-$1FF: Spin2 interpreter uses (DO NOT TOUCH)
```

### The Magic of $1E0-$1EF: Variable Mapping

**This is crucial**: The first 16 LONG variables of your method (parameters, returns, locals) are **automatically copied** to cog registers $1E0-$1EF before PASM executes, and copied back after.

```spin2
PUB calculate(a, b, c) : result | temp1, temp2, temp3
  ' a     → $1E0
  ' b     → $1E1  
  ' c     → $1E2
  ' result → $1E3
  ' temp1 → $1E4
  ' temp2 → $1E5
  ' temp3 → $1E6
  
  ORG
    MOV result, a      ' Using symbolic names!
    ADD result, b
    SHL result, c
    _RET_
  END
  ' result is automatically copied back to hub
```

### ORG Placement Options

```spin2
ORG                    ' Default: start at $000, limit at $120
ORG $080              ' Start at $080, default limit $120
ORG $040, $100        ' Start at $040, limit at $100
ORG $100, $120        ' Use upper available space
```

### Inline PASM Execution Sequence

1. **Save** streamer bytecode address
2. **Copy** first 16 method longs from hub → $1E0-$1EF
3. **Load** PASM code from hub → specified cog registers
4. **CALL** the PASM code
5. **Copy** $1E0-$1EF back to hub (update variables)
6. **Restore** streamer and continue Spin2

## Calling PASM from Spin2

### Three Ways to Execute PASM

#### 1. Inline PASM (ORG...END)
```spin2
PUB method()
  ORG
    ' PASM code here
  END
```

#### 2. CALL to Cog Registers
```spin2
PUB method()
  ' First load code into cog
  ORG $080
    myCode: MOV OUTA, #$FF
           _RET_
  END
  
  ' Later call it
  CALL(#$080)          ' # means cog address
```

#### 3. CALL to Hub RAM
```spin2
DAT
  hubCode     MOV OUTA, #$FF
              RET
              
PUB method()
  CALL(@hubCode)       ' @ means hub address
```

### Critical Difference: # vs @

- `CALL(#address)` - Call PASM in **cog registers**
- `CALL(@address)` - Call PASM in **hub RAM**

## REGLOAD and REGEXEC - Dynamic Code Loading

### The Chunk Format

**Every chunk MUST start with two WORDs**:
```spin2
DAT
  chunk  WORD  startReg, numRegs-1  ' Header (2 words)
         ' ...actual code/data follows...
```

### REGLOAD - Load Code/Data into Registers

```spin2
PUB loadCustomCode()
  REGLOAD(@myChunk)    ' Load chunk into specified registers
  ' Code is now in cog, can be called
  CALL(#$100)          ' Call if loaded at $100

DAT
  myChunk  WORD  $100, codeEnd-codeStart-1  ' Load at $100
  
  ORG $100
codeStart
  MOV OUTA, INA
  XOR OUTA, #$FF
  _RET_
codeEnd
```

### REGEXEC - Load and Execute

```spin2
PUB setupInterrupt()
  REGEXEC(@interruptChunk)  ' Load AND call immediately
  ' Returns here after setup completes
  
DAT
  interruptChunk  WORD  $118, intEnd-intStart-1
  
  ORG $118             ' High registers, out of the way
intStart
  ' Set up timer interrupt
  MOV IJMP1, #intHandler
  GETCT PA
  ADDCT1 PA, ##10_000_000
  SETINT1 #1           ' Enable CT-passed-CT1 interrupt
  _RET_                ' Return to Spin2
  
intHandler
  DRVNOT #56 ADDPINS 3
  ADDCT1 PA, ##10_000_000
  RETI1
intEnd
```

### REGLOAD vs REGEXEC

| Feature | REGLOAD | REGEXEC |
|---------|---------|----------|
| Loads code | Yes | Yes |
| Calls code | No | Yes (automatically) |
| Use case | Load multiple routines | Load and run setup code |
| Returns | After loading | After code executes |

## Data Structures and Field Pointers

### Bitfield Syntax - The Hidden Power

**Every variable in Spin2 can be treated as a bitfield!**

```spin2
VAR
  LONG status
  
PUB example()
  ' Access individual bits
  status.[0] := 1              ' Set bit 0
  status.[31] := 0             ' Clear bit 31
  
  ' Access bit ranges
  status.[7..0] := $FF        ' Set lower byte
  status.[15..8] := $AA       ' Set second byte
  
  ' Using ADDBITS for field definition
  status.[4 ADDBITS 3] := %101 ' Bits [7..4] = %101
```

### Bitfield Format (10 bits)

```
Bits [4..0]: Base bit position (0-31)
Bits [9..5]: Additional bits count (0-31)
```

### Field Access Patterns

```spin2
CON
  ' Define fields as constants
  FIELD_STATUS = 0 ADDBITS 7   ' Bits [7..0]
  FIELD_FLAGS  = 8 ADDBITS 7   ' Bits [15..8]
  FIELD_COUNT  = 16 ADDBITS 15 ' Bits [31..16]
  
VAR
  LONG register
  
PUB useFields()
  register.[FIELD_STATUS] := $FF
  register.[FIELD_FLAGS] := $00
  count := register.[FIELD_COUNT]
```

### Advanced: Structure-like Access

```spin2
CON
  ' Define a "structure" using field positions
  STRUCT_SIZE = 4  ' LONGs
  
  ' Field offsets within structure
  OFF_ID     = 0
  OFF_STATUS = 1  
  OFF_DATA   = 2
  OFF_NEXT   = 3
  
VAR
  LONG buffer[STRUCT_SIZE * 10]  ' Array of 10 "structures"
  
PUB accessStruct(index) | base
  base := @buffer + (index * STRUCT_SIZE * 4)
  
  LONG[base][OFF_ID] := index
  LONG[base][OFF_STATUS] := $ACTIVE
  LONG[base][OFF_DATA] := getData()
  LONG[base][OFF_NEXT] := @buffer + ((index+1) * STRUCT_SIZE * 4)
```

### Pointer + Field Combination

```spin2
VAR
  LONG data[100]
  
PUB complexAccess() | ptr
  ptr := @data
  
  ' Access with pointer, index, and bitfield
  LONG[ptr][5].[15..8] := $AA
  
  ' Multi-level indirection
  BYTE[@LONG[ptr][0]][3] := $FF
  
  ' With size override
  data.BYTE[10] := $12
  data.WORD[5].[15..8] := $34
```

## Practical Integration Patterns

### Pattern 1: Fast Bit Manipulation

```spin2
PUB reverseBits(value) : result
  ORG
    REV result, value   ' Hardware bit reversal
    _RET_
  END
```

### Pattern 2: Interrupt Handler Installation

```spin2
PUB installTimerISR()
  REGEXEC(@timerISR)
  ' ISR now running in background
  
DAT
  timerISR  WORD $110, isrEnd-isrCode-1
  
  ORG $110
isrCode
  MOV IJMP1, #handler
  GETCT PA
  ADDCT1 PA, ##1_000_000
  SETINT1 #1
  _RET_
  
handler
  DRVNOT #56
  ADDCT1 PA, ##1_000_000  
  RETI1
isrEnd
```

### Pattern 3: High-Speed Data Processing

```spin2
PUB processBuffer(src, dst, count) | a, b, c, d
  REPEAT count/4
    ORG
      SETQ #3            ' Fast block read
      RDLONG a, src
      ADD src, #16
      
      ' Process a, b, c, d in PASM
      XOR a, ##$12345678
      XOR b, ##$87654321
      XOR c, ##$AAAAAAAA
      XOR d, ##$55555555
      
      SETQ #3            ' Fast block write
      WRLONG a, dst
      ADD dst, #16
      _RET_
    END
```

### Pattern 4: CORDIC Acceleration

```spin2
PUB fastTrig(angle) : sine, cosine | qx, qy
  ORG
    QROTATE angle, ##$7FFF_FFFF  ' Start CORDIC
    GETQX sine
    GETQY cosine
    _RET_
  END
```

## Critical Rules and Gotchas

### 1. Register Safety

```spin2
' NEVER write to these:
' $120-$1D7 - Spin2 interpreter
' LUT $010-$1FF - Spin2 interpreter

' SAFE to use:
' $000-$11F - Your code space
' $1D8-$1DF - PR0-PR7 
' $1E0-$1EF - Method variables
' LUT $000-$00F - Free LUT
```

### 2. Variable Limit

```spin2
PUB tooMany() | v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15,v16,v17
  ORG
    MOV v16, #1   ' Works - in register
    MOV v17, #2   ' FAILS - v17 is in hub, not register!
  END
```

### 3. Stack Usage

```spin2
ORG
  CALL #subroutine1    ' Uses hardware stack
  _RET_
  
subroutine1
  CALL #subroutine2    ' Stack depth 2
  RET
  
subroutine2
  CALL #subroutine3    ' Stack depth 3
  RET
  
subroutine3
  ' Maximum depth is 8 for hardware stack
  RET
END
```

### 4. Interrupt Coexistence

```spin2
' Spin2 accommodates interrupts!
' You can set up interrupts in inline PASM
' They continue running after returning to Spin2

PUB setupPersistentISR()
  ORG $100              ' Put ISR high in memory
    MOV IJMP1, #isr
    ' Set up interrupt
    SETINT1 #1
    _RET_               ' Return to Spin2
    
  isr:
    ' This keeps running even in Spin2!
    DRVNOT #56
    RETI1
  END
```

## Why This Integration Matters

1. **Performance**: Critical sections run at full hardware speed
2. **Determinism**: Exact cycle timing when needed
3. **Hardware Access**: Direct access to P2's unique features
4. **Flexibility**: Mix high and low level in same method
5. **Interrupts**: Set up background processing while Spin2 continues
6. **No Context Switch**: Unlike traditional embedded systems
7. **Variable Sharing**: Automatic via $1E0-$1EF mapping

This tight integration between Spin2 and PASM is unique - no other embedded language provides this level of seamless mixing of high-level and assembly code with automatic variable synchronization.