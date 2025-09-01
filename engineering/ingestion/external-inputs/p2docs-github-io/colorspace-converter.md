# P2 Colorspace Converter - p2docs.github.io

**Source**: https://p2docs.github.io/colorspace.html  
**Import Date**: 2025-08-15  
**Verification Status**: 🟡 NEEDS VERIFICATION - Community source, some sections under construction  
**Purpose**: Hardware video encoding capabilities for ADA video projects

## ⚠️ Verification Requirements & Limitations

- Document notes some sections "under construction"
- Must verify against official P2 video documentation
- Critical for video output accuracy

## Colorspace Converter Overview

Hardware-based colorspace conversion with configurable coefficients and multiple output modes.

### Key Features

#### TMDS Encoding Support
- **DVI/HDMI Compatibility**: Direct digital video standards support
- **Pin Output Conversion**: Converts P2 pins to TMDS format
- **Bidirectional Operation**: Forward and reverse modes
- **Clock Requirements**: Streamer clock = 1/10th system clock
- **Independent Operation**: Works independently of colorspace conversion

#### Configuration System
- **CMOD Register**: 9 control bits for mode configuration
- **Coefficient Control**: Configurable Y, I, and Q terms
- **Chroma Carrier**: Programmable frequency for NTSC/PAL

### Programming Interface

#### Configuration Instructions
```pasm2
SETCMOD    ' Configure colorspace converter mode
SETCY      ' Set Y coefficient
SETCI      ' Set I coefficient  
SETCQ      ' Set Q coefficient
SETCFRQ    ' Set chroma carrier frequency
```

### Advanced Capabilities

#### Simultaneous Output Modes
- **Dual Signal Generation**: VGA + DVI/HDMI simultaneously
- **Frequency Control**: Instantaneous changes without glitches
- **Format Flexibility**: Multiple video standards support

#### Technical Limitations
- **Digital Pipeline**: "No color transformation can be performed in the digital video pipeline"
- **Construction Status**: Some features still under development

## ADA Video Project Applications

### Video Output Systems
- **Multi-Format Support**: Single chip driving multiple display types
- **Real-Time Conversion**: Hardware colorspace processing
- **Professional Standards**: DVI/HDMI compliance
- **Retro Compatibility**: NTSC/PAL support for classic systems

### Game System Porting
- **Original Format Preservation**: Maintain authentic video output
- **Modern Display Compatibility**: Convert to contemporary standards
- **Performance**: Hardware acceleration vs software conversion
- **Simultaneous Output**: Original + modern displays

### Custom Video Solutions
- **Coefficient Programming**: Custom color transformations
- **Carrier Frequency Control**: Precise timing for video standards
- **Glitch-Free Operation**: Professional video quality

## Integration Considerations

- Clock domain management (1/10th ratio requirement)
- Pin assignment for TMDS output
- Colorspace coefficient calculation
- Video timing coordination with other P2 subsystems

## Verification & Next Steps

1. **Validate TMDS encoding details** against official specs
2. **Confirm instruction set** for colorspace operations
3. **Test coefficient ranges** and calculation methods
4. **Document clock domain requirements** precisely