# P2 Architecture Overview

*Developer Reference v0.1.0*

## Core Architecture

### Multiprocessor Design
- **8 COGs**: Symmetric 32-bit processors
- **Independent Operation**: Each COG runs autonomously
- **Shared Hub Memory**: 512KB accessible by all COGs
- **No Operating System**: Direct hardware control

### COG Specifications
- **COG RAM**: 512 longs (2KB) per COG
- **LUT RAM**: 512 longs (2KB) additional lookup table memory
- **Registers**: $000-$1FF in COG RAM
- **Special Registers**: $1F0-$1FF for hardware functions
- **Execution Speed**: Most instructions complete in 2 clock cycles

## Memory Architecture

### Memory Hierarchy
```
COG RAM     : 512 longs per COG (fastest)
LUT RAM     : 512 longs per COG (fast, shareable)
Hub RAM     : 512KB shared (slower, shared)
External    : Via pins (slowest)
```

### Hub Memory Access - "Egg Beater"
The P2 uses a unique rotating slice mechanism:
- Hub memory divided into 8 slices
- Each COG gets access to one slice per clock
- Slices rotate every clock cycle
- Random access: 9-16 clocks
- Sequential access: 2 clocks (following the rotation)

## Smart Pins Subsystem

### Overview
- **64 Smart Pins**: Each pin has autonomous processing capability
- **32 Modes**: Different operating modes per pin
- **Independent Operation**: Pins operate without COG intervention
- **Buffered I/O**: Built-in FIFOs and state machines

### Smart Pin Categories (Partial - v0.1)
1. **Digital I/O**: Basic input/output
2. **Pulse/Cycle**: PWM, frequency measurement
3. **Serial**: Asynchronous serial, synchronous serial
4. **ADC/DAC**: Analog conversion modes
5. **Special**: USB, quadrature encoder, etc.

*Note: Full Smart Pin documentation by Jon Titus pending integration*

## CORDIC Solver

### Capabilities
- **54-stage pipeline**: Parallel operation
- **32-bit precision**: Full-width calculations
- **Operations**:
  - ROTATE: Coordinate rotation
  - VECTOR: Polar to rectangular
  - MULTIPLY: 32x32 → 64-bit
  - DIVIDE: 64/32 → 32-bit quotient
  - SQRT: Square root
  - LOG/EXP: Logarithm and exponential

### Performance
- **55-58 clock cycles**: Typical completion time
- **Pipelined**: Can accept new operation each clock
- **Parallel**: Doesn't block COG execution

## Instruction Pipeline

### 5-Stage Pipeline
1. **Fetch**: Get instruction from memory
2. **Decode**: Determine operation
3. **Execute**: Perform operation
4. **Memory**: Access hub if needed
5. **Write**: Store results

### Pipeline Stalls
- Hub memory access (waiting for slice)
- CORDIC operations (waiting for result)
- WAITx instructions (deliberate stall)

## Clock System

### Clock Sources
- **Internal RC**: ~24MHz (varies with temperature)
- **Crystal/Oscillator**: External clock input
- **PLL**: 3.125MHz to 500MHz output

### Clock Distribution
- **System Clock**: Main clock for all COGs
- **Clock Modes**: Multiple PLL configurations
- **Maximum Frequency**: 180MHz typical, 200MHz possible

## Interrupt System

### Three Interrupt Levels
- **INT1**: Highest priority
- **INT2**: Medium priority  
- **INT3**: Lowest priority

### Interrupt Sources
- Pin state changes
- Timer events
- Pattern matches
- Smart Pin events

### Interrupt Philosophy
*Note: P2 philosophy favors using multiple COGs over interrupts*

## Boot Process

⚠️ **Documentation Gap**: Boot process details pending from Chip Gracey

### Known Boot Options
- Serial boot from pins P63/P62
- SPI flash boot
- SD card boot

## Power Architecture

### Power Domains
- **VDD**: 1.8V core voltage
- **VIO**: 3.3V I/O voltage
- **Separate supplies**: For analog sections

### Power Management
- Clock gating per COG
- COG shutdown capability
- Pin drive strength control

## Debug Features

### Hardware Debug
- **DEBUG interrupt**: Hidden 4th interrupt level
- **SETBRK instruction**: Hardware breakpoints
- **Pin monitoring**: Real-time pin state observation

### Software Debug
- **DEBUG statements**: Built into SPIN2
- **Serial output**: Via Smart Pins
- **Logic analyzer**: Using Smart Pins

## Performance Characteristics

### Typical Performance
- **MIPS per COG**: ~90 MIPS at 180MHz
- **Total MIPS**: ~720 MIPS (8 COGs)
- **Hub bandwidth**: 900MB/s at 180MHz
- **Pin toggle rate**: Up to 250MHz

### Optimization Strategies
1. Use COG/LUT RAM for speed-critical code
2. Align hub accesses with egg beater rotation
3. Use CORDIC for complex math
4. Offload I/O to Smart Pins
5. Parallelize across COGs

## Comparison with P1

| Feature | P1 | P2 |
|---------|----|----|
| COGs | 8 | 8 |
| COG RAM | 512 longs | 512 longs |
| LUT RAM | None | 512 longs |
| Hub RAM | 32KB | 512KB |
| Smart Pins | None | 64 |
| CORDIC | None | Yes |
| Clock Speed | 80MHz | 180MHz+ |
| Instructions | ~350 | ~450 |

---

*This is v0.1.0 documentation - significant sections pending*

*Source: P2 Documentation v35 by Chip Gracey, Parallax Inc.*