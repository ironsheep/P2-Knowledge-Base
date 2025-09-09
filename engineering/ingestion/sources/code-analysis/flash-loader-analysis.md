# Flash Loader Analysis
*Source: flash_loader.spin2 (v51)*  
*Size: 9.5KB / ~290 lines*  
*Purpose: SPI Flash programmer and boot loader for P2*

## Executive Summary
This is a sophisticated piece of production code that demonstrates advanced P2 programming techniques. It's a dual-purpose program that:
1. Programs application code into SPI flash memory  
2. Serves as a boot loader that executes from COG RAM to load applications from flash

## Key Architectural Patterns Discovered

### 1. Smart Pin SPI Communication Pattern
**Discovery**: Professional SPI implementation using Smart Pins for hardware-accelerated communication

```spin2
' Pin assignments (standard P2 flash pins)
spi_cs = 61
spi_ck = 60  
spi_di = 59
spi_do = 58

' Smart Pin configuration for SPI clock
fltl    #spi_ck                 ' Reset smart pin
wrpin   #%01_00101_0, #spi_ck    ' Transition output mode
wxpin   #1, #spi_ck              ' 1 clock per transition
drvl    #spi_ck                  ' Enable smart pin
```

**Pattern**: Uses Smart Pin transition mode for generating precise SPI clock signals without CPU intervention.

### 2. Streamer + Smart Pin Coordination
**Discovery**: Combines streamer and smart pins for maximum throughput

```spin2
xinit   rmode, pa        ' Start streamer outputting bits
wypin   tranp, #spi_ck   ' Start clock transitions
waitxfi                  ' Wait for streamer completion
```

**Pattern**: Streamer handles data transfer while smart pin generates clock - true parallel operation.

### 3. Multi-Stage Boot Process
**Discovery**: Sophisticated multi-stage loading architecture

```
Stage 1: ROM bootloader loads first 1KB from flash → COG RAM
Stage 2: Flash loader (this code) executes from COG  
Stage 3: Loader copies initial app data from COG → HUB
Stage 4: Loader streams remaining app from flash → HUB
Stage 5: Application launches from HUB RAM
```

### 4. Checksum Verification Pattern
**Discovery**: Triple-layer data integrity checking

```spin2
' Three checksum levels:
1. Download checksum - verifies data before programming
2. Loader checksum - "Prop" signature verification  
3. Application checksum - verified before each boot
```

**Implementation**:
```spin2
rdfast  #0, #0           ' Start fast read
rep     #2, s            ' Repeat for all longs
rflong  v                ' Read long
add     @label/4, v  wz  ' Add to checksum (Z=1 if valid)
```

### 5. Self-Modifying Code Techniques
**Discovery**: Dynamic instruction modification for optimization

```spin2
.block  cmp    s, #$40        wcz
if_be   setd   .cmd, #$20         ' Modify instruction operand
if_be   sets   .tst, #$0F         ' Modify instruction source
```

**Pattern**: Changes erase command from 64KB to 4KB blocks dynamically based on remaining data size.

### 6. Hub-to-Hub Block Copy Pattern
**Discovery**: Efficient 512-long block transfers

```spin2
.move   setq2   #$200-1        ' Setup 512-long transfer
        rdlong  0, ptra++      ' Read block from source
        setq2   #$200-1        ' Setup write
        wrlong  0, ptrb++      ' Write block to destination
        djnf    t, #.move      ' Repeat for all blocks
```

### 7. COG Relaunch Pattern
**Discovery**: Clean application startup

```spin2
coginit #0, #$00000     ' Restart COG 0 from hub address 0
```

**Pattern**: Used both for launching application and handling failures.

### 8. Precise Timing Control
**Discovery**: Cycle-accurate SPI timing

```spin2
wypin   x, #spi_ck      ' 2 cycles
waitx   #3              ' 2+3 cycles  
xinit   wmode, #0       ' 2 cycles - perfectly aligned
```

**Pattern**: Comments show cycle counts for precise alignment of clock and data.

### 9. Error Handling Pattern
**Discovery**: Fail-safe shutdown on checksum failure

```spin2
stop    if_nz  fltl  #spi_di addpins 2  ' Float all SPI pins
        if_nz  hubset #%0010            ' Stop system clock
```

**Pattern**: System enters safe state on error - no errant code execution possible.

## Advanced Instruction Usage Observed

### Unique Instructions Used
1. **SETXFRQ** - Configure streamer frequency
2. **XINIT/XSTOP** - Streamer control
3. **WYPIN/WXPIN/WRPIN** - Smart pin configuration
4. **WAITXFI** - Wait for streamer completion
5. **SETQ2** - Fast block transfer setup
6. **RDFAST/RFLONG** - FIFO operations
7. **GETPTR** - Get current hub pointer
8. **ADDPINS** - Multi-pin operations
9. **MOVBYTS** - Byte rearrangement
10. **SKIP** - Instruction skipping

### Addressing Modes
```spin2
@label/4        ' Clever use of /4 for long addressing
##constant      ' Augmented immediate for 32-bit values
#\@label       ' Force absolute address mode
```

## Code Organization Patterns

### 1. Dual-Use Memory
Variables are reused between programmer and loader phases:
```spin2
s    skip  #1         ' Skip becomes variable 's'
v    long  0          ' Checksum becomes variable 'v'
```

### 2. Inline Data Tables
```spin2
tranp   long  256 * 8 * 2    ' Descriptive constant names
bmode   long  $4081_0008 + spi_di<<17  ' Bit-field construction
```

### 3. Conditional Assembly
```spin2
if_nz   jmp    #@stop/4      ' Conditional execution patterns
if_be   setd   .cmd, #$20    ' Conditional modification
```

## Performance Optimizations

### 1. Batch Operations
- Programs 256-byte pages (optimal flash page size)
- Erases 4KB/64KB blocks based on data size
- Uses 512-long hub transfers

### 2. Parallel Operations
- Streamer outputs data while smart pin generates clock
- No CPU cycles wasted on bit-banging

### 3. Minimal Overhead
- Direct COG execution (no hub exec overhead)
- Efficient checksum calculation using REP loops

## Discovered Idioms for YAML Enhancement

### 1. Smart Pin SPI Setup Idiom
```yaml
idiom: "spi_smart_pin_setup"
pattern: |
  fltl    #pin           ' Reset
  wrpin   #mode, #pin    ' Configure  
  wxpin   #timing, #pin  ' Set timing
  drvl    #pin          ' Enable
```

### 2. Streamer + Smart Pin Idiom
```yaml
idiom: "streamer_smartpin_sync"
pattern: |
  xinit   mode, data
  wypin   count, #clock_pin
  waitxfi
```

### 3. Block Transfer Idiom
```yaml
idiom: "hub_block_copy"
pattern: |
  setq2   #count-1
  rdlong  0, src++
  setq2   #count-1  
  wrlong  0, dst++
```

### 4. Checksum Verification Idiom
```yaml
idiom: "checksum_verify"
pattern: |
  rdfast  #0, #start
  rep     #2, count
  rflong  temp
  add     sum, temp wz
```

## Key Takeaways for Knowledge Base

### 1. Professional Code Structure
- Extensive documentation in comments
- Performance metrics included
- Clear section separation
- Descriptive constant/variable names

### 2. Hardware Feature Utilization
- Smart pins eliminate bit-banging
- Streamer provides DMA-like transfers
- FIFO enables efficient sequential access
- Fast block moves via SETQ2

### 3. Robust Error Handling
- Multiple checksum verifications
- Safe failure modes
- No undefined states

### 4. Efficiency Patterns
- Reuses memory between phases
- Self-modifying code for flexibility
- Optimal block sizes for operations
- Cycle-accurate timing where needed

## Recommendations for YAML Updates

### Instructions to Enhance
1. **XINIT** - Add streamer+smartpin example
2. **WYPIN** - Add SPI clock generation example
3. **SETQ2** - Add block copy example
4. **RDFAST** - Add checksum example
5. **SKIP** - Add memory reuse pattern
6. **MOVBYTS** - Add byte reordering example

### New Patterns to Document
1. SPI communication via smart pins
2. Flash memory programming sequences
3. Multi-stage boot loading
4. Checksum verification techniques
5. Safe error handling patterns

### Smart Pin Modes to Enhance
- Transition output mode (%01_00101_0) - Add SPI clock example
- Related modes should reference this implementation

## Conclusion
This flash loader is a masterclass in P2 programming, demonstrating:
- Efficient use of P2's unique hardware features
- Professional error handling and verification
- Optimal performance through parallel operations
- Clean, maintainable code structure

The patterns and idioms discovered here should significantly enhance our YAML knowledge base with real-world, production-tested examples.