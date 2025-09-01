# P2 Streamer - p2docs.github.io (Partial)

**Source**: https://p2docs.github.io/streamer.html  
**Import Date**: 2025-08-15  
**Status**: 🔴 INCOMPLETE DOCUMENTATION - Page under construction  
**Verification Status**: 🟡 PARTIAL - Limited instruction details only  
**Purpose**: High-speed data streaming (full documentation needed)

## ⚠️ Documentation Limitations

**Source Status**: Page shows "construction" GIF and "Make dots go brr" - clearly incomplete
**Content Available**: Basic instruction encodings only
**Missing**: DMA capabilities, data transfer modes, video coordination details

## Available Streamer Instructions

### Core Control Instructions
```pasm2
SETXFRQ freq    ' Set Streamer NCO frequency
XINIT   config  ' Initialize Streamer  
XCONT   config  ' Continue Streamer
XZERO   config  ' Continue Streamer and reset NCO phase
XSTOP           ' Stop Streamer
```

### Data Retrieval
```pasm2
GETXACC result  ' Get Goertzel accumulator
```

## ADA Project Implications

**Critical Gap**: Streamer is likely essential for:
- **High-speed video data output** - "Make dots go brr" suggests video pixel streaming
- **DMA-like operations** - Fast memory-to-pin transfers
- **Video timing coordination** - NCO frequency control suggests precise timing

**Next Steps Required**:
1. Find official P2 Streamer documentation
2. Cross-reference with our existing P2 knowledge base
3. Test Streamer capabilities with actual hardware

## Documentation Priority

**HIGH PRIORITY** for ADA projects - Streamer likely critical for:
- Video output performance
- Real-time graphics
- Audio streaming
- High-bandwidth I/O

## Verification Requirements

🔴 **URGENT**: Need complete Streamer documentation from official sources
🟡 **PARTIAL**: Instruction names require verification against our PASM2 database