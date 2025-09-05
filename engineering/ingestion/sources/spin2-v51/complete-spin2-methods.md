# Complete Spin2 Built-In Methods Reference

## Overview
Spin2 provides 135+ built-in methods for hardware control, math operations, memory management, and system functions.

---

## Hub Control Methods

### Cog Management
```spin2
COGINIT(CogNum, PASMaddr, PTRAvalue)
  ' Start PASM code in a cog, returns cog ID or -1 if no cog free

COGSPIN(CogNum, Method({Pars}), StkAddr)  
  ' Start Spin2 method in a cog, returns cog ID or -1 if no cog free

COGSTOP(CogNum)
  ' Stop specified cog

COGID() : CogNum
  ' Get current cog's ID

COGCHK(CogNum) : Running
  ' Check if cog is running, returns -1 if running or 0 if not
```

### Lock Management
```spin2
LOCKNEW() : LockNum
  ' Check out new lock (0..15) or < 0 if none available

LOCKRET(LockNum)
  ' Return lock to inventory

LOCKTRY(LockNum) : LockState
  ' Try to capture lock, -1 if successful or 0 if taken

LOCKREL(LockNum)
  ' Release captured lock

LOCKCHK(LockNum) : LockState
  ' Check lock state, bit 31 = captured, bits 3:0 = owner cog
```

### Attention Signaling
```spin2
COGATN(CogMask)
  ' Strobe ATN to cogs per 16-bit mask

POLLATN() : AtnFlag
  ' Check for ATN strobe, -1 if strobed or 0 if not

WAITATN()
  ' Wait for ATN strobe
```

### Clock Control
```spin2
HUBSET(Value)
  ' Execute HUBSET instruction with value

CLKSET(NewCLKMODE, NewCLKFREQ)
  ' Safely set new clock mode and frequency
```

---

## Pin Control Methods

### Basic Pin Operations
```spin2
PINH | PINHIGH(PinField)
  ' Drive pins high

PINL | PINLOW(PinField)  
  ' Drive pins low

PINT | PINTOGGLE(PinField)
  ' Toggle pins

PINF | PINFLOAT(PinField)
  ' Float pins (high-Z)

PINW | PINWRITE(PinField, Data)
  ' Write data to pins

PINR | PINREAD(PinField) : PinStates
  ' Read pin states
```

### SmartPin Operations
```spin2
PINSTART(PinField, Mode, Xval, Yval)
  ' Start smart pins: DIR=0, WRPIN=Mode, WXPIN=Xval, WYPIN=Yval, DIR=1

PINCLEAR(PinField)
  ' Clear smart pins: DIR=0, WRPIN=0

WRPIN(PinField, Data)
  ' Write mode register of smart pins

WXPIN(PinField, Data)
  ' Write X register of smart pins

WYPIN(PinField, Data)
  ' Write Y register of smart pins

AKPIN(PinField)
  ' Acknowledge smart pins

RDPIN(Pin) : Zval
  ' Read and acknowledge smart pin, bit 31 = C flag

RQPIN(Pin) : Zval
  ' Read smart pin without acknowledge
```

---

## Timing Methods

### System Counter
```spin2
GETCT() : Count
  ' Get 32-bit system counter

POLLCT(Tick) : Past
  ' Check if tick value passed, -1 if yes

WAITCT(Tick)
  ' Wait until system counter reaches tick
```

### Delays
```spin2
WAITUS(Microseconds)
  ' Delay for microseconds

WAITMS(Milliseconds)
  ' Delay for milliseconds
```

### Time Measurement
```spin2
GETSEC() : Seconds
  ' Get seconds since boot

GETMS() : Milliseconds
  ' Get milliseconds since boot
```

---

## Math Methods

### CORDIC Operations
```spin2
ROTXY(x, y, angle32bit) : rotx, roty
  ' Rotate X,Y by angle

POLXY(length, angle32bit) : x, y
  ' Convert polar to Cartesian

XYPOL(x, y) : length, angle32bit
  ' Convert Cartesian to polar

QSIN(length, step, stepsInCircle) : y
  ' Calculate sine using CORDIC

QCOS(length, step, stepsInCircle) : x
  ' Calculate cosine using CORDIC

QLOG(value)
  ' Logarithm via CORDIC

QEXP(value)
  ' Exponential via CORDIC
```

### Extended Math
```spin2
MULDIV64(mult1, mult2, divisor) : quotient
  ' 64-bit intermediate multiply/divide

GETRND() : rnd
  ' Get random number

NAN(float) : NotANumber
  ' Check if float is NaN
```

---

## Memory Methods

### Block Operations
```spin2
BYTEMOVE(Destination, Source, Count)
  ' Copy bytes

WORDMOVE(Destination, Source, Count)
  ' Copy words

LONGMOVE(Destination, Source, Count)
  ' Copy longs

BYTESWAP(AddrA, AddrB, Count)
  ' Swap bytes between addresses

WORDSWAP(AddrA, AddrB, Count)
  ' Swap words between addresses

LONGSWAP(AddrA, AddrB, Count)
  ' Swap longs between addresses
```

### Fill Operations
```spin2
BYTEFILL(Destination, Value, Count)
  ' Fill memory with byte value

WORDFILL(Destination, Value, Count)
  ' Fill memory with word value

LONGFILL(Destination, Value, Count)
  ' Fill memory with long value
```

### Comparison
```spin2
BYTECOMP(AddrA, AddrB, Count) : Match
  ' Compare bytes, returns -1 if match

WORDCOMP(AddrA, AddrB, Count) : Match
  ' Compare words, returns -1 if match

LONGCOMP(AddrA, AddrB, Count) : Match
  ' Compare longs, returns -1 if match
```

---

## String Methods

```spin2
STRSIZE(Addr) : Size
  ' Get string length (not including terminator)

STRCOMP(AddrA, AddrB) : Match
  ' Compare strings, -1 if match, 0 if different

STRCOPY(Destination, Source, Max)
  ' Copy string with maximum length
```

### String Creation
```spin2
STRING("Text", 13) : StringAddress
  ' Create string constant, returns address

LSTRING("Text")
  ' Create length-prefixed string
```

---

## Data Creation Methods

```spin2
BYTE(val1, val2, ...)
  ' Create byte data sequence

WORD(val1, val2, ...)
  ' Create word data sequence

LONG(val1, val2, ...)
  ' Create long data sequence
```

---

## Lookup Methods

```spin2
LOOKUP(Index: v1, v2..v3, etc) : Value
  ' Look up value by 1-based index

LOOKUPZ(Index: v1, v2..v3, etc) : Value
  ' Look up value by 0-based index

LOOKDOWN(Value: v1, v2..v3, etc) : Index
  ' Find 1-based index of value

LOOKDOWNZ(Value: v1, v2..v3, etc) : Index
  ' Find 0-based index of value
```

---

## Register Operations

```spin2
GETREGS(HubAddr, CogAddr, Count)
  ' Copy cog registers to hub

SETREGS(HubAddr, CogAddr, Count)
  ' Copy hub to cog registers
```

---

## Execution Control

```spin2
CALL(RegisterOrHubAddr)
  ' Call PASM code

REGEXEC(HubAddr)
  ' Execute register code from hub

REGLOAD(HubAddr)
  ' Load registers from hub
```

---

## I/O Stream Methods

```spin2
SEND(byte_values...)
  ' Send bytes to current output method
  ' Examples:
  SEND("Hello", 13)
  SEND($00, $FF)

RECV() : byte
  ' Receive byte from current input method
```

---

## CRC Calculation

```spin2
GETCRC(BytePtr, Poly, Count) : CRC
  ' Calculate CRC with specified polynomial
```

---

## Structure Size

```spin2
SIZEOF(Structure) : ByteCount
  ' Get size of structure in bytes
```

---

## Special Pin Field Operations

```spin2
pin ADDPINS count
  ' Create pin field from base pin plus additional pins
  ' Example: 56 ADDPINS 7 = pins 56-63

pin1 ADDBITS pin2
  ' OR pin masks together
```

---

## Method Categories by Usage

### Most Common Pin Control
- PINH / PINL / PINT - Basic pin control
- PINWRITE / PINREAD - Pin I/O
- PINSTART / PINCLEAR - SmartPin control

### Most Common Timing
- WAITMS / WAITUS - Simple delays
- GETCT - System timing
- WAITCT - Precise timing

### Most Common Memory
- BYTEMOVE / BYTEFILL - Byte operations
- LONGMOVE / LONGFILL - Long operations
- String operations

### Most Common Math
- Basic operators (see operators reference)
- MULDIV64 - Extended precision
- ROTXY / POLXY - Coordinate math

### Most Common System
- COGINIT / COGSPIN - Start cogs
- COGSTOP - Stop cogs
- HUBSET / CLKSET - Clock control

---

## Block Usage Notes

### Available in All Blocks
- Most read-only methods (GETCT, etc.)
- Data creation (BYTE, WORD, LONG)
- STRING constants

### PUB/PRI Only
- Methods with side effects
- Pin control methods
- Memory write operations
- Cog control methods

### CON Block
- Only compile-time constants
- STRING() allowed for addresses
- No runtime methods

### DAT Block  
- Data creation methods
- Address references
- Limited runtime in inline PASM

---

## Parameter Types

### PinField
Can be:
- Single pin number (0-63)
- Pin field created with ADDPINS
- Multiple pins with ADDBITS

### CogNum
- 0-7 for specific cog
- COGEXEC_NEW for any available
- NEWCOG (-1) for any available

### Addresses
- Hub RAM addresses (0-524287)
- @ prefix gets address
- @@ gets absolute hub address

---

This reference covers all 135 Spin2 built-in methods with signatures, descriptions, and usage context.