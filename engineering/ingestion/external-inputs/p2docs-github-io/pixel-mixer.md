# P2 Pixel Mixer - p2docs.github.io

**Source**: https://p2docs.github.io/mixpix.html  
**Import Date**: 2025-08-15  
**Verification Status**: 🟡 NEEDS VERIFICATION - Community source, requires validation against official P2 documentation  
**Purpose**: Hardware graphics acceleration for ADA game systems and video processing

## ⚠️ Verification Requirements

Critical for graphics accuracy:
- Instruction timing (7 cycles claimed)
- Mathematical formulas and behavior
- Format support details

## Pixel Mixer Instructions

Hardware-accelerated graphics operations with 4 specialized instructions:

### 1. ADDPIX - Saturated Color Addition
```pasm2
ADDPIX destination, source
```
- **Operation**: Adds source and destination bytes
- **Saturation**: Caps result at 255 on overflow
- **Use Case**: Brightness enhancement, additive blending

### 2. MULPIX - Color Multiplication  
```pasm2
MULPIX destination, source
```
- **Operation**: Multiplies color bytes
- **Use Case**: Color tinting, darkening effects

### 3. BLNPIX - Color Blending
```pasm2
BLNPIX destination, source
```
- **Operation**: Interpolates between source and destination colors
- **Use Case**: Alpha blending, smooth transitions

### 4. MIXPIX - Generic Color Mixing
```pasm2
MIXPIX destination, source
```
- **Operation**: Configurable mixing using SETPIX instruction
- **Flexibility**: Complex blending modes
- **Use Case**: Custom graphics effects

## Technical Specifications

### Format Support
- **32-bit RGBA**: Full color with alpha channel
- **8-bit Grayscale**: Monochrome operations
- **Per-Byte Processing**: Component-wise operations

### Performance
- **Execution Time**: 7 cycles per instruction
- **Hardware Acceleration**: No software computation required
- **Parallel Processing**: Multi-component operations

### Configuration Interface
```pasm2
SETPIV   ' Set pixel interpolation value
SETPIX   ' Configure MIXPIX operation mode
```

## ADA Game System Applications

### Sprite Graphics
- **Additive Effects**: Explosions, lighting effects (ADDPIX)
- **Color Tinting**: Character color variations (MULPIX)  
- **Transparency**: Sprite blending with backgrounds (BLNPIX)
- **Special Effects**: Custom shader-like operations (MIXPIX)

### Video Processing
- **Frame Blending**: Motion blur, fade effects
- **Color Correction**: Real-time image enhancement
- **Overlay Graphics**: HUD elements, menus
- **Filter Effects**: Game-specific visual styles

### Emulation Support
- **Original Graphics**: Preserve authentic pixel operations
- **Enhancement**: Add modern effects to classic graphics
- **Performance**: Hardware acceleration vs software emulation
- **Accuracy**: Pixel-perfect reproduction when needed

## Integration Patterns

### With Colorspace Converter
- Process pixels before colorspace conversion
- Chain operations for complex effects
- Coordinate timing for video output

### With Smart Pins
- Stream processed pixels to video output
- Coordinate with video timing signals
- Buffer graphics data efficiently

### With Streamer
- High-speed pixel data transfer
- DMA-like graphics operations
- Efficient memory-to-video pipelines

## Verification Priorities

1. **Timing accuracy**: Confirm 7-cycle execution
2. **Mathematical operations**: Validate per-byte processing
3. **Format support**: Test RGBA and grayscale modes
4. **Configuration interface**: Verify SETPIV/SETPIX behavior

## Performance Analysis

For ADA's real-time graphics:
- **7 cycles/operation** at 320MHz = ~46M pixel operations/second
- **Hardware acceleration** eliminates software overhead
- **Multi-component processing** handles RGBA efficiently