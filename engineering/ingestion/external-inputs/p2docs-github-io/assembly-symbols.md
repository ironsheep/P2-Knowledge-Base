# P2 Assembly Symbol List - p2docs.github.io

**Source**: https://p2docs.github.io/asm_index.html  
**Import Date**: 2025-08-15  
**Verification Status**: 🟡 NEEDS VERIFICATION - Community source, requires validation against official PASM2 documentation  
**Purpose**: Complete assembly symbol reference for ADA code generation

## ⚠️ Verification Requirements

Must verify against:
- Official PASM2 assembly manual
- Parallax instruction documentation  
- Existing P2 instruction database (491 instructions)

## Assembly Symbol Categories

### 1. Math and Logic (80+ instructions)
- Largest category covering computational operations
- ADD, SUB, MUL, and advanced mathematical functions
- Bitwise operations and logical comparisons

### 2. Register Indirection
- Memory addressing modes
- Pointer-based operations

### 3. LUT Memory
- Lookup table memory operations
- Fast local memory access

### 4. Hub Memory  
- Shared memory operations
- Inter-cog communication

### 5. Hub FIFO
- First-in-first-out operations
- Streaming data handling

### 6. Branching
- Control flow instructions
- Conditional and unconditional jumps

### 7. CORDIC
- **QROTATE**: CORDIC rotation operations
- Hardware-accelerated trigonometric functions
- Essential for video signal generation

### 8. Pins
- Smart Pin control and configuration
- Direct hardware pin manipulation

### 9. Streamer
- High-speed data streaming
- DMA-like operations

### 10. Colorspace Converter
- **Critical for video**: Hardware color conversion
- RGB/YUV transformations
- Essential for ADA video projects

### 11. Events
- Interrupt and event handling
- Hardware event processing

### 12. Interrupts  
- 3 prioritized interrupt levels
- Event-driven programming support

### 13. Pixel Mixer
- **Video-specific**: Hardware pixel blending
- Graphics acceleration
- Essential for game system porting

### 14. Hub Control
- System-level control operations
- Multi-cog coordination

### 15. Miscellaneous Operations
- Utility and support functions

## Smart Pin Modes (~30 configurations)
- Advanced I/O pin capabilities
- Programmable pin functions
- Hardware-assisted I/O operations

## ADA Project Relevance

### Video Output Systems
- **Colorspace Converter**: Hardware color transformations
- **Pixel Mixer**: Real-time graphics blending
- **CORDIC**: Signal generation and timing
- **Streamer**: High-speed video data output

### Game System Emulation
- **Math/Logic**: CPU instruction emulation
- **Branching**: Control flow emulation
- **Hub Memory**: Shared state management
- **Events/Interrupts**: Timing-critical emulation

### Controller Input
- **Smart Pins**: Hardware controller interface
- **Events**: Input event processing
- **FIFO**: Input buffering

## Verification Priorities

1. **Video-specific instructions**: Colorspace, Pixel Mixer, CORDIC
2. **Smart Pin modes**: Critical for I/O interfaces
3. **Memory operations**: Hub and LUT access patterns
4. **Math operations**: Emulation performance critical

## Next Steps
- Cross-reference with official PASM2 manual
- Validate video-specific instruction details
- Document Smart Pin mode applications