# Spin2 Debugger Analysis
*Source: Spin2_debugger.spin2 (v51)*  
*Size: 33KB / ~1000 lines*  
*Purpose: Complete debug infrastructure for P2 development*

## Executive Summary
This is the official P2 debugger that provides comprehensive debugging capabilities for Spin2/PASM2 applications. It demonstrates advanced P2 features including:
- ISR (Interrupt Service Routine) handling
- Dynamic code overlays
- Multi-COG debugging coordination
- Serial communication protocol
- Register state management
- Floating-point output formatting

## Key Architectural Patterns Discovered

### 1. Protected Memory Architecture
**Discovery**: Uses fixed hub RAM regions for debug infrastructure

```spin2
' Protected hub RAM usage ($FC000..$FFFFF)
dat_addr = $FC000    ' DEBUG data
sav_addr = $FEA00    ' COG register save buffer
dbg_addr = $FF1A0    ' Debugger code + overlays
' $FFC00..$FFFFF    ' Per-COG ISR buffers (silicon-fixed)
```

**Pattern**: Reserves upper 256KB of hub RAM for debug system, protected by hardware.

### 2. Debug ISR Architecture
**Discovery**: Sophisticated interrupt handling with state preservation

```spin2
' Debug interrupt flow:
' 1. JMP #$1F8 to ROM (hardware)
' 2. ROM saves $000..$00F to hub
' 3. ROM loads debug ISR from hub
' 4. Debug ISR saves $010..$1F7
' 5. Debugger executes
' 6. Restore all registers
' 7. RETI0 returns to application
```

**Pattern**: Complete register preservation allows transparent debugging.

### 3. Lock-Based Multi-COG Coordination
**Discovery**: Uses lock[15] for exclusive resource access

```spin2
.wait   locktry #15      wc  ' Wait for lock[15]
if_nc   jmp     #.wait      ' Spin until acquired

' ... critical section ...

lockrel #15                 ' Release lock[15]
```

**Pattern**: Ensures only one COG at a time can access debug resources (serial pins, save buffer).

### 4. Dynamic Code Overlay System
**Discovery**: Loads different code segments on demand

```spin2
' Load overlay and execute
loc     pb, #\dbg_addr+(@bp_handler-@debugger)
setq    #overlay_end-overlay_begin
rdlong  overlay_begin, pb
jmp     #bp_handler
```

**Pattern**: Overlays allow complex functionality in limited COG RAM.

### 5. Smart Pin Repository Mode
**Discovery**: Uses RX pin as data storage

```spin2
' Configure RX pin as long repository
wrpin   #%00_00001_0, @_rxpin_/4   ' Repository mode
dirh    @_rxpin_/4                  ' Enable output
wxpin   _clkfreq_, @_rxpin_/4      ' Store clock frequency
```

**Pattern**: Smart pins can store data when not used for communication.

### 6. Bytecode Interpreter Pattern
**Discovery**: Efficient bytecode processing for DEBUG commands

```spin2
debug_byte:
    callpa  #z, #getdeb        ' Get bytecode
    test    z, #$E0       wz   ' Check command type
if_nz jmp   #arg_cmd          ' Argument command
    altgb   z, #.table        ' Index into jump table
    getbyte w
    jmp     w                 ' Execute command
```

**Pattern**: Jump table dispatch for efficient command processing.

### 7. Floating-Point Output Implementation
**Discovery**: Complete IEEE 754 float-to-string conversion

```spin2
fpout:
    ' Unpack mantissa and exponent
    ' Multiply by powers of 10
    ' Convert to decimal digits
    ' Format with scientific notation
```

**Pattern**: Sophisticated FP handling without hardware FP unit.

### 8. CRC-Based Register Verification
**Discovery**: Uses CRC for efficient register state checking

```spin2
setq    x
rep     #1, #8
crcnib  pa, crcpoly    ' Calculate CRC nibble
```

**Pattern**: Hardware CRC acceleration for data integrity.

### 9. Serial Protocol Optimization
**Discovery**: Word-packed transmission for efficiency

```spin2
' Pack word as %HHHHHHHH01LLLLLLLL for single transmit
shr     pa, #8-2
rolbyte pa, t1, #0
bith    pa, #8
bitl    pa, #9
setbyte txrx, #17, #0   ' 18-bit mode
```

**Pattern**: Reduces serial overhead by packing data.

### 10. Stack Preservation Pattern
**Discovery**: Complete 8-level stack save/restore

```spin2
pop     stk0    ' Save stack
pop     stk1
...
pop     stk7

' Later...
push    stk7    ' Restore stack
push    stk6
...
push    stk0
```

## Advanced Instruction Usage Observed

### Unique Instructions
1. **GETBRK** - Get break status
2. **BRK** - Set breakpoint
3. **COGBRK** - Break another COG
4. **LOCKTRY/LOCKREL** - Lock management
5. **ALTGB** - Indirect byte access
6. **CRCNIB** - CRC calculation
7. **SEUSSF** - Checksum calculation
8. **RQPIN** - Read pin state
9. **DECOD/ENCOD** - Decode/encode values
10. **AUGS** - Augment source

### Addressing Techniques
```spin2
@label/4                    ' Divide address by 4 for long indexing
##constant                  ' 32-bit immediate
#\@label                   ' Absolute address
ptrb[$1C]                  ' Indexed pointer access
alts/altd                  ' Indirect register access
```

## Code Organization Patterns

### 1. Memory Layout Management
```spin2
org                        ' COG RAM organization
orgh                       ' Hub RAM organization
fit overlay_end+1          ' Ensure code fits
res 16                     ' Reserve unintialized space
```

### 2. Conditional Compilation Flow
```spin2
if_c_and_nz   jmp    #target     ' Complex conditionals
if_nc_and_z   call   #routine
if_c_or_nz    mov    x, y
```

### 3. Table-Driven Design
- Jump tables for command dispatch
- String tables for output messages
- Power-of-10 tables for FP conversion
- CRC polynomial constants

## Performance Optimizations

### 1. Pipeline Awareness
```spin2
' Comments show cycle counts
wypin   x, #spi_ck      ' 2 cycles
waitx   #3              ' 2+3 cycles
xinit   wmode, #0       ' 2 cycles
```

### 2. Register Clustering
```spin2
cogn    cogid   cogn    ' cogn..freq form contiguous data
' Allows efficient block operations
```

### 3. REP Loops
```spin2
rep     #3, #32+1       ' Hardware loop for division
cmpsub  y, _baud_  wc
rcl     txrx, #1
shl     y, #1
```

## Discovered Idioms for YAML Enhancement

### 1. Debug ISR Setup Idiom
```yaml
idiom: "debug_isr_install"
pattern: |
  neg     t, #$40        ' Start at $FFFC0
  rep     #3, #8         ' 8 COGs
  setq    #$00F-$000    ' 16 longs
  wrlong  @isr/4, t     ' Write ISR
  sub     t, #$80       ' Next COG
```

### 2. Lock-Protected Critical Section
```yaml
idiom: "lock_critical_section"
pattern: |
  .wait   locktry #N    wc
  if_nc   jmp     #.wait
  ' ... critical code ...
  lockrel #N
```

### 3. Overlay Loading
```yaml
idiom: "overlay_load"
pattern: |
  loc     pb, #\address
  setq    #size-1
  rdlong  start, pb
  jmp     #entry
```

### 4. Serial Configuration
```yaml
idiom: "uart_smart_pin_config"
pattern: |
  fltl    #pin           ' Reset
  wrpin   #mode, #pin    ' Configure
  wxpin   baudrate, #pin ' Set baud
  drvl    #pin          ' Enable
```

## System Integration Patterns

### 1. Clock Management
```spin2
hubset  _clkmode1_      ' Start external clock
waitx   ##20_000_000/100 ' 10ms stabilization
hubset  _clkmode2_      ' Switch to external
```

### 2. Application Launch
```spin2
' Move application to $00000
' Clear trailing RAM
coginit #0, #$00000     ' Launch from hub
```

### 3. Multi-Stage Initialization
1. Configure pins
2. Set clock mode
3. Allocate locks
4. Clear debug RAM
5. Install ISRs
6. Move debugger code
7. Protect memory
8. Launch application

## Key Takeaways for Knowledge Base

### 1. Professional Debug Infrastructure
- Complete register preservation
- Non-intrusive debugging
- Multi-COG support
- Rich output formatting

### 2. Advanced P2 Features
- Hardware debug support
- Protected memory regions
- Lock-based synchronization
- Dynamic code loading

### 3. Efficient Communication
- Smart pin UART
- Packed data transmission
- Repository mode for storage
- Bytecode interpretation

### 4. Robust Error Handling
- CRC verification
- Checksum validation
- Safe state transitions
- Graceful degradation

## Recommendations for YAML Updates

### Instructions to Enhance
1. **GETBRK/BRK** - Add debug examples
2. **LOCKTRY/LOCKREL** - Add synchronization patterns
3. **ALTGB/ALTB** - Add indirect access examples
4. **CRCNIB** - Add CRC calculation pattern
5. **SEUSSF** - Add checksum example
6. **RQPIN** - Add pin reading pattern

### New Patterns to Document
1. Debug ISR implementation
2. Multi-COG synchronization
3. Dynamic overlay management
4. Bytecode interpretation
5. Floating-point formatting
6. Serial protocol optimization

### Smart Pin Modes to Enhance
- Repository mode (%00_00001_0) - Add data storage example
- Async serial TX (%01_11110_0) - Add debug output example
- Async serial RX (%00_11111_0) - Add debug input example

## Architectural Insights

### Memory Management Strategy
- Fixed regions for predictability
- Protected upper hub RAM
- Per-COG ISR buffers
- Shared save buffer with lock protection

### Communication Architecture
- Bytecode-based protocol
- Efficient packing strategies
- CRC/checksum verification
- Bidirectional command/response

### State Management
- Complete COG state preservation
- Stack preservation
- Pointer preservation
- Flag preservation

## Conclusion
The Spin2 debugger is a masterpiece of system-level P2 programming, demonstrating:
- Deep understanding of P2 architecture
- Sophisticated interrupt handling
- Efficient resource management
- Professional debug capabilities

The patterns discovered here provide invaluable insights into building robust, production-quality P2 system software. The debug infrastructure shows how to leverage P2's unique features for powerful development tools.