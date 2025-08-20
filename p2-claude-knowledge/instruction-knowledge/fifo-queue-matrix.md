# FIFO/Queue Operations Matrix

**Purpose**: Documents P2 FIFO and queue operations for data streaming and buffering.

## FIFO Access Instructions

### Hub FIFO Operations
```pasm2
RDFAST  setup_value, start_addr     ' Setup fast hub read FIFO
RFBYTE  dest                        ' Read byte from FIFO
RFWORD  dest                        ' Read word from FIFO
RFLONG  dest                        ' Read long from FIFO
RFVAR   dest                        ' Read variable from FIFO
```

### Streamer FIFO Operations
```pasm2
XINIT   streamer_mode, start_addr   ' Initialize streamer
XZERO   count, value                ' Zero-fill streamer
XCONT   mode, count                 ' Continue streamer operation
```

### LUT FIFO Operations
```pasm2
WRLUT   source, addr                ' Write to LUT (FIFO behavior)
RDLUT   dest, addr                  ' Read from LUT (FIFO behavior)
```

## Data Flow Patterns

### Sequential Read Pattern
```pasm2
RDFAST  #0, start_addr      ' Setup FIFO for sequential read
.loop   RFLONG value        ' Read next value
        ' Process value
        DJNZ   count, #.loop ' Continue until done
```

### Streaming Pattern  
```pasm2
XINIT   mode, buffer_addr   ' Initialize streamer
XCONT   mode, byte_count    ' Stream specified bytes
' Data streams automatically to configured output
```

### Circular Buffer Pattern
```pasm2
' Setup circular buffer using LUT
SETLUT  buffer_start
.loop   RDLUT   value, read_ptr
        ADD     read_ptr, #1
        AND     read_ptr, #buffer_mask  ' Wrap around
```

## FIFO Coordination Requirements

### Setup Dependencies
- **RDFAST before RF*** instructions**: Must initialize FIFO before reading
- **XINIT before XCONT**: Streamer must be initialized before continuation
- **Address alignment**: Some FIFO operations require aligned addresses

### Performance Considerations
- **FIFO depth limitations**: Understanding buffer sizes and overflow conditions
- **Clock cycle timing**: FIFO access timing vs regular memory access
- **Hub timing coordination**: FIFO operations vs other hub access

## Research Gaps - DEMO CRITICAL

### High Priority (Demo Impact)
1. **FIFO setup parameter calculation** (3 hours)
   - RDFAST setup value encoding and meaning
   - Address alignment requirements for FIFO operations
   - FIFO depth and performance relationships

2. **Streamer mode configuration** (4 hours)
   - XINIT mode parameter encoding and options
   - Streamer output pin configuration
   - Data format and timing control

3. **RF* instruction behavior differences** (2 hours)
   - RFBYTE vs RFWORD vs RFLONG performance
   - Data alignment and endianness handling
   - FIFO advancement and position tracking

### Medium Priority (Development Important)
4. **Circular buffer implementation** (5 hours)
   - LUT-based circular buffer techniques
   - Wrap-around logic and masking
   - Read/write pointer coordination

5. **FIFO overflow and underflow handling** (3 hours)
   - Detection of FIFO boundary conditions
   - Recovery strategies for buffer problems
   - Flow control techniques

### Low Priority (Documentation Complete)
6. **Advanced streaming patterns** (8 hours)
   - Complex streamer configurations
   - Multi-channel data streaming
   - Performance optimization techniques

**Total Research Required**: 25 hours
**Demo Critical Subset**: 9 hours (36% of total)

## Integration Notes

**Cross-References**:
- State Setup Matrix: RDFAST/XINIT as setup instructions
- Instruction Sequence Matrix: FIFO operation ordering requirements
- Smart Pin Matrix: Streamer output to Smart Pins

**Documentation Sources Needed**:
- Hub FIFO architecture documentation
- Streamer subsystem technical reference
- LUT usage patterns and circular buffer examples
- Performance timing documentation for FIFO operations