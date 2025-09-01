# P2X8C4M64P Datasheet - Technical Content Extraction

**Source**: Propeller2-P2X8C4M64P-Datasheet-20221101.pdf
**Date**: 2022/11/01
**Publisher**: Parallax Inc.
**Type**: Official Technical Datasheet

---

## 📊 Unique Knowledge Contributions

This datasheet provides critical hardware-level information not found in other sources:

### 1. Physical Implementation Details
- **Package**: 14x14mm exposed-pad 100-pin TQFP
- **Temperature Range**: AEC-Q100 Level 2 (-40 to +105°C)
- **Moisture Sensitivity**: MSL 3 (168 hours)
- **Exposed Pad**: Serves as GND and heatsink

### 2. Electrical Specifications
- **Core Voltage**: 1.8 VDC via VDD pins
- **I/O Voltage**: 3.3 VDC via VIO pins (groups of 4)
- **Power Consumption**: ~130 µA in low-power mode
- **Clock Stopped Power**: ~100 µA (leakage only)

### 3. Memory Architecture (Precise)
```
Region          Depth      Width     PC Address       PASM D/S Address
Cog Register    512        32 bits   $00000-$001FF   $000-$1FF
Cog Lookup      512        32 bits   $00200-$003FF   $000-$1FF  
Hub RAM         524,288    8 bits    $00400-$7FFFF   $00000-$7FFFF
```

### 4. Performance Specifications
- **Clock**: 180 MHz typical, 320 MHz extended
- **Hub Access**: 720 MB/s per cog @ 180 MHz
- **Execution**: 720 MIPs total (90 MIPs/cog) @ 180 MHz
- **Math/Logic**: 2-clock execution including 16x16 multiply
- **Bytecode**: 6-clock custom executor

### 5. Clock System Details
Six clock modes with glitch-free switching:
- Internal RC: ~24 MHz (initial boot clock)
- Crystal oscillator: 7.5pF/15pF loading caps
- External clock input
- Fractional PLL: 1-64 divider → 1-1024 multiplier → optional (1-15)*2 post-divider
- Low-power RC: ~20 kHz
- Clock stop mode

### 6. Smart Pin Capabilities (Hardware Level)
- **DACs**: 8-bit 120Ω (3ns) and 1kΩ with 16-bit oversampling
- **ADCs**: Delta-sigma with 5 ranges, 2 sources, VIO/GIO calibration
- **Filtering**: 2/3/5/8-bit unanimous with selectable sample rate
- **Drive Modes**: logic/1.5k/15k/150k/1mA/100µA/10µA/float
- **Relative Pin Access**: -3 to +3 pin offset capability

### 7. CORDIC Solver Specifications
32-bit pipelined with scale-factor correction:
- 32x32 unsigned multiply → 64-bit result
- 64/32 unsigned divide → 32-bit quotient + remainder
- 64→32 square root
- Polar/Cartesian conversions
- Logarithm conversions
- **Timing**: Start every 8 clocks, results in 55 clocks

### 8. Boot System Architecture
16KB Boot ROM contains:
- SPI loader for 8-pin flash or SD card
- Serial loader with Hex and Base64 protocols
- P2 Monitor (interactive terminal)
- TAQOZ Forth (interactive programming)
- Loads into last 16KB of Hub RAM on boot

### 9. Compliance Information
- **RoHS3**: EU 2011/65/EU compliant
- **REACH**: EU EC 1907/2006 compliant
- **ECCN**: 3A991A2 (EU EAR99)
- **HTSUS**: 8542.31.0001

### 10. Pin Configuration Details
- **Power Distribution**: Multiple VDD for clean core power
- **I/O Power**: VIO pins power groups of 4 I/Os
- **TEST Pin**: Must be tied to ground
- **Thermal**: Exposed pad critical for heat dissipation

---

## 🔍 Critical Design Information

### Minimal Connection Requirements
1. All VDD pins connected to 1.8V
2. All VIO pins connected to 3.3V
3. TEST pin grounded
4. Exposed pad connected to ground plane
5. Decoupling capacitors on all power pins

### Crystal Oscillator Configuration
- Internal loading capacitors provided
- Supports 7.5pF or 15pF crystals
- XI and XO pins for crystal connection
- Can feed PLL for frequency multiplication

### Boot Memory Options
1. **SPI Flash**: 8-pin connection, auto-boot
2. **MicroSD Card**: SPI mode boot support
3. **Dual Boot**: Flash primary, SD secondary
4. **Serial**: Host-based loading

---

## 📋 Hardware Function Highlights

### Counter/Timer Capabilities
- 28 counter modes per cog
- 64-bit hub global counter
- 16 event trackers per cog
- Six 32-bit clock modes

### Video Output Support
- **Analog**: VGA/HDTV/NTSC/PAL
- **Digital**: HDMI 480p@60fps, 720p@24fps
- Live colorspace conversion (3x3 matrix)
- Pixel blending for 8:8:8:8 data

### Communication Protocols
Hardware support for:
- USB 12 Mbps (full/low speed via odd/even pairs)
- Synchronous serial (1-32 bits, up to clock/2)
- Asynchronous serial (1-32 bits, up to clock/3)
- Quadrature decoder with 32-bit counter

### ADC Modes
- Delta-Sigma
- SINC1/2/3 filtering
- Scope mode
- Goertzel analysis (4 ADC bit streams per cog)

---

## 🚨 Design Considerations

### Thermal Management
- Exposed pad MUST be connected to ground plane
- Acts as primary heat dissipation path
- Critical for high-frequency operation

### Power Supply Requirements
- Clean 1.8V for core (all VDD pins)
- Clean 3.3V for I/O (all VIO pins)
- Separate analog/digital supplies recommended
- Adequate decoupling essential

### Clock Configuration
- Starts on internal RC (~24 MHz)
- Software-controlled clock switching
- PLL configuration for high frequencies
- Low-power modes via clock reduction

---

## 📊 Comparison with Other Sources

### Information Unique to Datasheet:
1. Physical package specifications
2. Thermal characteristics
3. Electrical absolute maximums
4. Compliance/regulatory data
5. Detailed power consumption
6. Pin-level specifications
7. Boot ROM contents
8. Hardware connection requirements

### Information Complementing Silicon Doc:
- More concise overview
- Focus on implementation vs theory
- Practical connection examples
- Boot process details
- Compliance information

---

*Extraction Complete - This datasheet provides essential hardware implementation details not found in other P2 documentation*