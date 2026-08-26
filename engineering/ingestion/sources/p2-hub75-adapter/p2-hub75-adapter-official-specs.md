# P2 Eval HUB75 Adapter Board (64032) - Official Specifications
*Iron Sheep Productions, LLC*

## Product Overview

**SKU**: 64032  
**Manufacturer**: Iron Sheep Productions, LLC  
**Purpose**: Simple means to connect and drive HUB75 RGB LED Matrix panels from Propeller 2  
**Status**: Retiring from Parallax store (quantity limited to stock on hand)  
**GitHub Repository**: [P2 HUB75 Driver and Documentation](https://github.com/ironsheep/P2-HUB75-LED-Matrix-Driver)  
**OBEX**: ISP HUB75 Driver available in P2 Object Exchange  

## Official Specifications

### Physical Specifications
- **PCB Dimensions**: 1.9 × 2.8 inches (48 × 71 mm)
- **Form Factor**: Dual 2×6-pin female pass-through headers with 0.1″ spacing
- **Connectors**: Standard HUB75 16-pin IDC connector

### Electrical Specifications
- **Operating Voltage**: +5 VDC (supplied by P2 Development Board)
- **Maximum Clock Rate**: 70 MHz (limited by level shifter ICs)
- **Level Shifting**: 3.3V to 5V for all HUB75 signals
- **Address Line Support**: 
  - A-B-C (8 row scan, supports 16-row panels)
  - A-B-C-D (16 row scan, supports 32-row panels)
  - A-B-C-D-E (32 row scan, supports 64-row panels)

### Compatible Development Systems
- P2 Eval Board (#64000)
- P2 Edge Module Breadboard (#64020) with P2 Edge Module (#P2-EC)
- P2 Edge Mini Breakout Board (#64019) with P2 Edge Module (#P2-EC)

## Supported Panel Types

### HUB75 Standards
- **Standard HUB75**: 3-4 address lines for smaller panels
- **HUB75E**: 5 address lines for larger panels (64+ rows)

### Pixel Pitch Options
- **P1.25**: 1.25mm × 1.25mm (ultra-fine detail)
- **P2**: 2mm × 2mm (fine detail, popular choice)
- **P3**: 3mm × 3mm (balanced size/resolution)
- **P4**: 4mm × 4mm (good visibility)
- **P5**: 5mm × 5mm (medium size)
- **P6**: 6mm × 6mm (larger displays)
- **P7**: 7mm × 7mm (large format)
- **P8**: 8mm × 8mm (maximum physical size)

### Example Compatible Panels
- HUB75 RGB LED Panel, 128 × 128 mm, 64 × 64 dots
- Common sizes: 16×32, 32×32, 32×64, 64×64 pixels
- Daisy-chainable for larger displays

## Key Features

1. **Robust Level Shifting**: Provides 3.3V to 5V level shifting for all signals at HUB75 connector
2. **Wide Compatibility**: Supports panels using A-B-C, A-B-C-D, and A-B-C-D-E address lines
3. **Driver Integration**: Perfect for use with ISP HUB75 Driver from P2 OBEX
4. **Pass-Through Design**: Compatible with P2 boards having side-by-side 2×6 accessory headers
5. **High Performance**: Supports up to 70 MHz clock rate for smooth animations

## Applications

- **Text Display**: Scroll messages and notifications
- **Large Format**: Connect multiple panels for video walls
- **Custom Lighting**: Control colors, saturation, and intensity
- **Data Visualization**: Real-time graphs and meters
- **Digital Signage**: Dynamic advertising and information displays
- **Art Installations**: Interactive LED displays

## HUB75 Interface Pinout

Standard 16-pin IDC connector:

| Pin | Signal | Description | Direction |
|-----|--------|-------------|-----------|
| 1 | R1 | Red data, upper half | Output |
| 2 | G1 | Green data, upper half | Output |
| 3 | B1 | Blue data, upper half | Output |
| 4 | GND | Ground | - |
| 5 | R2 | Red data, lower half | Output |
| 6 | G2 | Green data, lower half | Output |
| 7 | B2 | Blue data, lower half | Output |
| 8 | GND | Ground | - |
| 9 | A | Row select bit 0 | Output |
| 10 | B | Row select bit 1 | Output |
| 11 | C | Row select bit 2 | Output |
| 12 | D | Row select bit 3 | Output |
| 13 | CLK | Clock signal | Output |
| 14 | LAT | Latch signal | Output |
| 15 | OE | Output Enable (active low) | Output |
| 16 | GND | Ground | - |

**Note**: Pin 12 (D) is used for 32+ row panels, E signal (if needed) is typically on a separate connection.

## P2 Pin Mapping (Typical Configuration)

```spin2
CON
  ' HUB75 Data pins (6 bits parallel) - consecutive for streamer
  HUB75_R1 = 0   ' Red data, upper half
  HUB75_G1 = 1   ' Green data, upper half  
  HUB75_B1 = 2   ' Blue data, upper half
  HUB75_R2 = 3   ' Red data, lower half
  HUB75_G2 = 4   ' Green data, lower half
  HUB75_B2 = 5   ' Blue data, lower half
  
  ' HUB75 Control pins
  HUB75_CLK = 6  ' Clock signal
  HUB75_LAT = 7  ' Latch signal
  HUB75_OE = 8   ' Output Enable
  
  ' Row select pins
  HUB75_A = 9    ' Row select bit 0
  HUB75_B = 10   ' Row select bit 1
  HUB75_C = 11   ' Row select bit 2
  HUB75_D = 12   ' Row select bit 3 (32+ row panels)
  HUB75_E = 13   ' Row select bit 4 (64+ row panels)
```

## Power Requirements

### Adapter Board
- Powered from P2 development board's 5V supply
- Board consumption: <50mA (level shifters and support circuitry)

### LED Panels (User-Supplied Power)
**IMPORTANT**: LED panels require separate 5V power supply!

| Panel Size | Typical Current | Peak Current | PSU Recommended |
|------------|-----------------|--------------|-----------------|
| 16×32 | 1-2A | 4A | 5V 5A |
| 32×32 | 2-3A | 8A | 5V 10A |
| 32×64 | 3-4A | 12A | 5V 15A |
| 64×64 | 4-6A | 20A | 5V 25A |

**Power Guidelines**:
- Use thick power cables (18 AWG or larger)
- Distribute power injection for multiple panels
- Add capacitors near panel power inputs
- Consider power supply efficiency and cooling

## Software Support

### ISP HUB75 Driver Features
- Multiple panel support (daisy-chain and grid configurations)
- Automatic panel detection
- PWM brightness control (0-255 levels)
- Color correction and gamma adjustment
- Double-buffering for flicker-free updates
- Text rendering with multiple fonts
- Graphic primitives (lines, circles, rectangles)
- BMP image display support

### Basic Initialization Example
```spin2
OBJ
  display : "isp_hub75_matrix"
  
PUB main()
  ' Initialize single 64x32 panel
  display.start(HUB75_R1, HUB75_CLK, HUB75_LAT, HUB75_OE, 64, 32, 1)
  
  ' Set brightness (0-255)
  display.setBrightness(128)
  
  ' Clear to black
  display.clear()
  
  ' Draw test pattern
  display.drawText(0, 0, string("P2 HUB75"), $FFFF, $0000)
  display.update()
```

## Performance Specifications

### Refresh Rates (Typical)
| Panel Size | Colors | Refresh Rate | P2 Clock |
|------------|--------|--------------|----------|
| 32×32 | 24-bit | 120 Hz | 200 MHz |
| 64×32 | 24-bit | 100 Hz | 200 MHz |
| 64×64 | 24-bit | 60 Hz | 200 MHz |
| 128×64 | 24-bit | 30 Hz | 200 MHz |

### Bandwidth Calculations
```
Bandwidth = Width × Height × Colors × RefreshRate × ScanRate
Example 64×32 panel:
  = 64 × 32 × 3 bytes × 100 Hz × (1/16 scan)
  = 38.4 KB/s data rate
```

## Purchasing Information

### Adapter Board
- **Availability**: Limited to stock on hand (product retiring)
- **Source**: Parallax Inc. Store
- **SKU**: 64032

### HUB75 Panels (Not Stocked by Parallax)
- **Recommended Source**: AliExpress (search "HUB75")
- **Alternative Sources**: Adafruit, SparkFun, Amazon
- **Selection Criteria**:
  - Pixel pitch based on viewing distance
  - Indoor vs outdoor brightness requirements
  - Power budget and cooling capabilities
  - Physical size constraints

## Developer Notes

This product represents significant development effort by Stephen Moraco (Iron Sheep Productions). The comprehensive driver suite on GitHub includes:
- Multiple example programs
- Detailed API documentation
- Panel configuration guides
- Troubleshooting tips
- Community contributions welcome

## Troubleshooting Guide

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| No display | No panel power | Connect separate 5V supply to panel |
| Dim display | Insufficient power | Use larger power supply |
| Flickering | Low refresh rate | Reduce panel size or colors |
| Wrong colors | Pin mapping | Check R1/G1/B1 connections |
| Ghosting | Slow OE timing | Adjust OE pulse width |
| Missing rows | Address lines | Verify A/B/C/D connections |

## Revision History

- **v1.0**: Initial release
- **Current**: Production version (retiring)

## Support Resources

- **GitHub**: Full documentation and drivers
- **P2 Forums**: Community support
- **OBEX**: Latest driver versions
- **Author Contact**: Via GitHub repository

## Legal Notice

P2 Eval HUB75 Adapter Board is a product of Iron Sheep Productions, LLC.  
Propeller 2 is a trademark of Parallax Inc.  
HUB75 is an industry standard interface.

---

*For the latest updates and drivers, visit the [GitHub repository](https://github.com/ironsheep/P2-HUB75-LED-Matrix-Driver)*