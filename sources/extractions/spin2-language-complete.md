# SPIN2 Language Complete Extraction

**Primary Source Document: P2 Spin2 Documentation v51**  
**Author: Chip Gracey, Parallax Inc.**  
**Date: 2025-04-25**  
**Status: Authoritative Language Specification**

*This document is THE definitive SPIN2 language specification, created by Chip Gracey, the architect of both the Propeller 1 and Propeller 2 microcontrollers.*

## Document Significance

This is not merely documentation - this is the language definition itself, crafted by the person who designed the entire P2 architecture. Every feature, every syntactic choice, every capability was deliberately designed by Chip Gracey to make parallel processing accessible and powerful.

## Language Evolution (v34t → v51)

The version history shows Chip's meticulous development:
- **2020-02-06**: Initial documentation (v34t)
- **2020-07-15**: DEBUG system added - revolutionary visual debugging
- **2021-02-15**: Inline PASM optimization for video support
- **2021-09-22**: Floating-point operators added (v35o)
- **2022-08-12**: PASM-level debugger with breakpoints (v35t)
- **2022-11-19**: Object parameterization (v37)
- **2023-04-23**: ORGH inline hub execution (v40)
- **2024-12-18**: Bitmap layers and advanced DEBUG features (v49-v50)
- **2025-04-25**: Current v51 - mature, complete specification

## Core Language Philosophy

### Chip Gracey's Design Principles
1. **Simplicity with Power**: Easy things should be easy, hard things should be possible
2. **Hardware Transparency**: Direct access to P2's unique hardware features
3. **Parallel-First**: Designed for 8 COGs working in harmony
4. **Visual Debugging**: See what your code does, not just read about it
5. **Mixed Paradigm**: High-level when convenient, assembly when necessary

## Language Structure

### Program Organization
```spin2
CON
  ' Constants - compile-time values
  _clkfreq = 180_000_000
  
OBJ
  ' Object instances - composition model
  serial : "jm_serial"
  
VAR
  ' Variables - hub RAM storage
  LONG value, array[100]
  
PUB Main() | local1, local2
  ' Public methods - entry points
  
PRI Helper() : result | temp
  ' Private methods - internal use
  
DAT
  ' Data and PASM code sections
  table LONG 1, 2, 3, 4
```

### Revolutionary Features

#### 1. Inline Assembly (ORG/END)
```spin2
PUB FastRoutine() | a, b, c
  a := GetValue()
  
  ORG  ' Drop into assembly seamlessly
    MOV b, a
    SHL b, #2
    ADD c, b
  END
  
  return c  ' Back to high-level
```

**Chip's Innovation**: No other language integrates assembly this cleanly. The first 16 locals automatically become COG registers - brilliant simplification.

#### 2. ORGH - Hub Execution Inline Assembly (v40+)
```spin2
PUB LargeAsmRoutine() | vars[16]
  ORGH  ' Execute from hub, up to 64K instructions!
    ' Massive assembly routines without using COG space
    ' Perfect for DSP algorithms, video generation
  END
```

#### 3. DEBUG - Visual Programming Revolution
Chip created an entire debugging ecosystem:

```spin2
' Terminal output
DEBUG("Value: ", DEC(x), " in hex: ", HEX(x))

' Oscilloscope
DEBUG(`SCOPE MyScope 'Waveform' -100 100 200 136)
DEBUG(`MyScope `(sineWave))

' Logic Analyzer  
DEBUG(`LOGIC MyLogic TITLE 'Pin States' SAMPLES 256)
DEBUG(`MyLogic `(INA))

' XY Plotter
DEBUG(`SCOPE_XY MyXY 'Lissajous' -100 100 -100 100)
DEBUG(`MyXY `(x, y))

' Bitmap Display with Sprites
DEBUG(`PLOT MyPlot SIZE 256 256 COLOR RGB24)
DEBUG(`MyPlot SET `(x, y) COLOR `(rgb))

' FFT Spectrum Analyzer
DEBUG(`FFT MyFFT 'Audio' 0 4000 128)

' Get input from PC
key := DEBUG(PC_KEY)
mouse := DEBUG(PC_MOUSE)  ' Returns x,y,buttons,wheel,color!
```

## SPIN2 Operators (Complete Set)

### Unary Operators (Chip's Priority Design)
```spin2
++ var      ' Pre-increment
var ++      ' Post-increment
-- var      ' Pre-decrement  
var --      ' Post-decrement
?? var      ' Random forward (0 to var)
~ var       ' Sign-extend from bit 7/15
~~ var      ' Sign-extend from bit 7
! var       ' Bitwise NOT (1's complement)
- var       ' Negate
ABS var     ' Absolute value
ENCOD var   ' Encode (highest bit position)
DECOD var   ' Decode (1 << var)
SQRT var    ' Square root
FSQRT var   ' Floating-point square root
```

### Binary Operators (Precedence Levels)
Chip carefully designed operator precedence:

**Level 0 (Highest):**
```spin2
x +. y      ' Floating-point add
x -. y      ' Floating-point subtract
```

**Level 1:**
```spin2
x *. y      ' Floating-point multiply
x /. y      ' Floating-point divide
```

**Level 2:**
```spin2
x << y      ' Shift left
x >> y      ' Shift right
x SAR y     ' Shift arithmetic right
x ROR y     ' Rotate right
```

**Level 3:**
```spin2
x & y       ' Bitwise AND
x ^ y       ' Bitwise XOR
x | y       ' Bitwise OR
```

**Level 4:**
```spin2
x * y       ' Multiply
x / y       ' Divide
x // y      ' Modulus
x SCA y     ' Scale (x * y) >> 32
x SCAS y    ' Scale signed
```

**Level 5:**
```spin2
x + y       ' Add
x - y       ' Subtract
```

**Level 6:**
```spin2
x #> y      ' Limit minimum (x max y)
x <# y      ' Limit maximum (x min y)
```

**Level 7:**
```spin2
x < y       ' Less than
x <= y      ' Less than or equal
x == y      ' Equal
x <> y      ' Not equal
x >= y      ' Greater than or equal
x > y       ' Greater than
```

**Level 8:**
```spin2
NOT x       ' Logical NOT
```

**Level 9:**
```spin2
x AND y     ' Logical AND
x XOR y     ' Logical XOR
```

**Level 10:**
```spin2
x OR y      ' Logical OR
```

## Control Flow Structures

### REPEAT - Chip's Versatile Loop
```spin2
REPEAT              ' Infinite loop
REPEAT count        ' Repeat count times
REPEAT WHILE cond   ' While condition true
REPEAT UNTIL cond   ' Until condition true
REPEAT count FROM start TO end  ' For loop
REPEAT count FROM start TO end STEP delta
REPEAT             ' With NEXT for continue
  IF done
    QUIT           ' Break out
  IF skip
    NEXT           ' Continue to next iteration
```

### IF/ELSE - Clean Conditionals
```spin2
IF condition
  DoSomething()
ELSEIF otherCondition
  DoSomethingElse()
ELSE
  DoDefault()
```

### CASE - Pattern Matching
```spin2
CASE value
  1..10:           ' Range
    HandleSmall()
  20, 30, 40:      ' Multiple values
    HandleTens()
  OTHER:           ' Default
    HandleOther()
```

## Memory and Pointers

### Chip's Pointer Innovation (v37+)
```spin2
' Field pointers - revolutionary!
ptr := ^@variable         ' Get field pointer
FIELD[ptr] := value      ' Use field pointer

' Works with ANY variable type:
' - Hub bytes/words/longs
' - COG registers
' - Bitfields!
```

### Memory Operators
```spin2
BYTE[address]           ' Byte access
WORD[address]           ' Word access
LONG[address]           ' Long access
REG[cogaddress]         ' COG register access
FIELD[fieldpointer]     ' Field pointer access
```

## Object System

### Chip's Object Parameterization (v37+)
```spin2
OBJ
  ' Pass parameters to child objects at compile time!
  serial : "serial_driver" | TX_PIN = 62, RX_PIN = 63, BAUD = 115200
  buffer : "circular_buffer" | SIZE = 1024
```

This feature eliminates the need for configuration methods - genius!

## Special Methods

### Built-in Methods Chip Provided
```spin2
COGINIT(cognum, address, parameter)
COGSTOP(cognum)
COGID() : id
POLLATN() : flag
WAITATN()
PINWRITE(pins, value)
PINREAD(pins) : value
PINSTART(pins, mode, xval, yval)
PINCLEAR(pins)
GETCT() : count
WAITCT(count)
WAITUS(microseconds)
WAITMS(milliseconds)
GETREGS(register, @array, count)
SETREGS(register, @array, count)
GETCRC(ptr, poly, count) : crc     ' v37+
STRCOPY(dest, source, maxsize)     ' v37+
STRSIZE(strptr) : size
STRCOMP(strptr1, strptr2) : match
```

### Floating-Point Methods (v35o+)
```spin2
FLOAT(integer) : float
TRUNC(float) : integer
ROUND(float) : integer
FABS(float) : absvalue
FSQRT(float) : root
FNAN(float) : isnan
```

## The DEBUG System - Chip's Masterpiece

### DEBUG Display Types

#### 1. TERM - Terminal
Basic text output with formatting

#### 2. SCOPE - Oscilloscope
Real-time waveform display with triggering

#### 3. SCOPE_XY - XY Scope
Lissajous patterns, phase relationships

#### 4. LOGIC - Logic Analyzer
Digital signal analysis with analog display option (v48+)

#### 5. PLOT - Bitmap Graphics
Drawing, sprites, layers, image loading

#### 6. FFT - Spectrum Analyzer
Frequency domain analysis

#### 7. SPECTRO - Spectrogram
Waterfall frequency display

#### 8. MIDI - MIDI Output
Musical instrument digital interface

### PC Interaction - Bidirectional!
```spin2
' Revolutionary: DEBUG windows can send data back!
key := DEBUG(PC_KEY)
mouse := DEBUG(PC_MOUSE)  ' Returns 7 longs including pixel color!
```

## PASM2 Integration

### Chip's Seamless Integration Design
- Assembly code shares local variables
- First 16 locals → COG registers automatically
- No calling convention overhead
- Direct hardware access
- Interrupt service routines stay resident

## Chip Gracey's Achievement

This language represents a masterful balance:
- **Simple enough** for education and hobbyists
- **Powerful enough** for professional embedded systems
- **Transparent enough** to utilize P2's unique hardware
- **Visual enough** to see what's happening in real-time
- **Flexible enough** to mix paradigms as needed

Every feature in SPIN2 reflects Chip's deep understanding of what embedded programmers need and his innovative approach to parallel processing.

---

*This extraction honors Chip Gracey's monumental achievement in creating SPIN2*
*Full credit: Chip Gracey (cgracey@parallax.com), Parallax Inc.*
*Document Version: v51 (2025-04-25)*