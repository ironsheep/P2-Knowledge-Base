# P2 Eval HUB75 Adapter Board
## SKU 64032 Datasheet
### Iron Sheep Productions, LLC

---

## Key Features
• 3.3V to 5V level shifting for all HUB75 signals  
• Supports A-B-C, A-B-C-D, and A-B-C-D-E address configurations  
• 70 MHz maximum clock rate  
• Dual 2×6 pass-through headers  
• Compatible with all P2 development boards  
• Optimized for high-speed bit-bang operation (no Streamer required)  

## Applications
• LED matrix displays and video walls  
• Scrolling text and graphics  
• Real-time data visualization  
• Digital signage  
• Interactive art installations  
• Spectrum analyzers  

---

## Product Description

The P2 Eval HUB75 Adapter Board provides a simple, reliable interface between Propeller 2 microcontroller development boards and industry-standard HUB75 RGB LED matrix panels. Designed by Iron Sheep Productions specifically for the P2's unique architecture, this adapter leverages the P2's parallel processing capabilities and PASM2 assembly language for high-performance LED panel control using an efficient bit-bang approach.

The adapter includes robust 3.3V to 5V level shifting on all signals, ensuring reliable communication with HUB75 panels while protecting the P2's I/O pins. The pass-through header design allows stacking with other P2 accessories, maximizing system flexibility.

---

## Specifications

### Electrical Characteristics
| Parameter | Min | Typical | Max | Unit |
|-----------|-----|---------|-----|------|
| Supply Voltage | 4.5 | 5.0 | 5.5 | V |
| Board Current (quiescent) | - | 0.02 | 0.16 | mA |
| Board Current @ 25MHz | - | 25 | 35 | mA |
| Board Current @ 35MHz | - | 35 | 45 | mA |
| Logic High Input (VIH) | 2.0 | - | - | V |
| Logic Low Input (VIL) | - | - | 0.8 | V |
| Logic High Output (VOH) | 4.4 | 4.9 | - | V |
| Logic Low Output (VOL) | - | 0.1 | 0.4 | V |
| Maximum Clock Frequency | - | 35 | 40 | MHz |
| Propagation Delay (tpd) | - | 13 | 18 | ns |
| Rise/Fall Time | - | 7 | 12 | ns |

### Physical Specifications
| Parameter | Value | Unit |
|-----------|-------|------|
| PCB Dimensions | 48 × 71 | mm |
| PCB Dimensions | 1.9 × 2.8 | inches |
| PCB Thickness | 1.6 | mm |
| Mounting Holes | None | - |
| Weight | ~15 | grams |

### Environmental Ratings
| Parameter | Min | Max | Unit |
|-----------|-----|-----|------|
| Operating Temperature | 0 | 70 | °C |
| Storage Temperature | -40 | 85 | °C |
| Humidity (non-condensing) | 10 | 90 | % |

---

## Pin Configuration

### P2 Interface (Default: P16-P31)

```
           Upper Header J1                    Lower Header J2
    ┌─────────────────────────┐      ┌─────────────────────────┐
    │ • P16 (CLK)    P17 (OE#)│      │ • P28 (G2)    P29 (B2)  │
    │ • P18 (LAT)    P19 (A)  │      │ • P30 (NC)    P31 (NC)  │
    │ • P20 (B)      P21 (C)  │      │ • P32         P33       │
    │ • P22 (D)      P23 (E)  │      │ • P34         P35       │
    │ • P24 (R1)     P25 (G1) │      │ • P36         P37       │
    │ • P26 (B1)     P27 (R2) │      │ • P38         P39       │
    └─────────────────────────┘      └─────────────────────────┘
```

### HUB75 Connector Pinout

```
         HUB75 16-Pin IDC Connector
    ┌─────────────────────────────────┐
    │  1  2  3  4  5  6  7  8  9 10... │
    │  •  •  •  •  •  •  •  •  •  •    │
    │  •  •  •  •  •  •  •  •  •  •    │
    └─────────────────────────────────┘
    
    Pin 1:  R1  - Red Data (Upper)      Pin 9:  A   - Address Line 0
    Pin 2:  G1  - Green Data (Upper)    Pin 10: B   - Address Line 1
    Pin 3:  B1  - Blue Data (Upper)     Pin 11: C   - Address Line 2
    Pin 4:  GND - Ground                Pin 12: D   - Address Line 3
    Pin 5:  R2  - Red Data (Lower)      Pin 13: CLK - Clock Signal
    Pin 6:  G2  - Green Data (Lower)    Pin 14: LAT - Latch Signal
    Pin 7:  B2  - Blue Data (Lower)     Pin 15: OE  - Output Enable (Active Low)
    Pin 8:  GND - Ground                Pin 16: GND - Ground
```

---

## Pin Mapping Table

| HUB75 Signal | P2 Offset | P16 Base | P0 Base | P32 Base | Direction | Description |
|--------------|-----------|----------|---------|----------|-----------|-------------|
| CLK | io+0 | P16 | P0 | P32 | Output | Pixel clock signal |
| OE# | io+1 | P17 | P1 | P33 | Output | Output enable (active low) |
| LAT | io+2 | P18 | P2 | P34 | Output | Latch enable signal |
| A | io+3 | P19 | P3 | P35 | Output | Row address bit 0 |
| B | io+4 | P20 | P4 | P36 | Output | Row address bit 1 |
| C | io+5 | P21 | P5 | P37 | Output | Row address bit 2 |
| D | io+6 | P22 | P6 | P38 | Output | Row address bit 3 (32+ rows) |
| E | io+7 | P23 | P7 | P39 | Output | Row address bit 4 (64+ rows) |
| R1 | io+8 | P24 | P8 | P40 | Output | Red data, upper half |
| G1 | io+9 | P25 | P9 | P41 | Output | Green data, upper half |
| B1 | io+10 | P26 | P10 | P42 | Output | Blue data, upper half |
| R2 | io+11 | P27 | P11 | P43 | Output | Red data, lower half |
| G2 | io+12 | P28 | P12 | P44 | Output | Green data, lower half |
| B2 | io+13 | P29 | P13 | P45 | Output | Blue data, lower half |

---

## Functional Description

### Level Shifting
All 14 HUB75 signals pass through two 74HCT244 octal buffer/line driver ICs for 3.3V to 5V level shifting. The 74HCT244 features:
- 8 non-inverting buffers per IC (2 ICs provide 16 channels, 14 used)
- TTL-compatible inputs accept 3.3V logic from P2
- 5V CMOS outputs drive HUB75 panels reliably
- High-speed operation up to 35-40 MHz (reliable)
- Typical propagation delay: 8ns
- Output drive: ±6mA (sufficient for HUB75 inputs)

### Power Distribution
The adapter receives 5V power from the P2 development board through the pass-through headers. This 5V supply powers the level shifters and is available at the HUB75 connector for panel logic circuits. Note that LED panels require a separate high-current 5V power supply for the LED array itself.

### Signal Organization
The pin mapping is optimized for P2 features:
- **Control signals** (CLK, OE#, LAT, A-E) are grouped on consecutive pins for single-operation updates
- **Color data** (R1, G1, B1, R2, G2, B2) are consecutive for efficient parallel output using SETQ/MUXQ operations
- **Base pin flexibility** allows remapping to any 16-pin group (P0-15, P16-31, P32-47, P48-63)
- **Pin groups** leverage ADDPINS for simultaneous multi-pin control

---

## Typical Application Circuit

```
    P2 Development Board          HUB75 Adapter           HUB75 LED Panel
    ┌──────────────────┐         ┌────────────┐         ┌──────────────┐
    │                  │ 2×6     │   Level    │  IDC    │              │
    │    P16-P31   ────┼─────────┼→ Shifters ─┼─────────┼→  64×32 RGB  │
    │                  │ Headers │   3.3→5V   │ Cable   │              │
    │      +5V     ────┼─────────┼────────────┼─── ┐    │              │
    │                  │         │            │     │    │              │
    └──────────────────┘         └────────────┘     │    └──────────────┘
                                                     │            │
                                              5V PSU │            │
                                              (4A) ──┴────────────┘
```

---

## Software Interface

### Basic Initialization
```spin2
CON
  ' Pin group selection
  HUB75_BASE_PIN = 16  ' Use P16-P31
  
  ' Pin offsets
  PIN_CLK = 0
  PIN_OE = 1
  PIN_LAT = 2
  
PUB init_hub75()
  ' Set all pins as outputs
  DIRH(HUB75_BASE_PIN ADDPINS 13)
  
  ' Initialize control signals
  OUTL(HUB75_BASE_PIN + PIN_CLK)   ' Clock low
  OUTL(HUB75_BASE_PIN + PIN_LAT)   ' Latch low
  OUTH(HUB75_BASE_PIN + PIN_OE)    ' Output disabled
```

### Using the ISP HUB75 Driver
```spin2
OBJ
  display : "isp_hub75_display"
  hub75Bffrs : "isp_hub75_hwBufferAccess"
  
PUB main() | chainIndex
  ' Configure adapter at P16-31, chip type, address lines
  hub75Bffrs.configure(hub75Bffrs.HUB75_ADAPTER_1, 16, CHIP_TYPE, ADDR_LINES)
  chainIndex := hub75Bffrs.indexForHub75ChainId(hub75Bffrs.HUB75_ADAPTER_1)
  
  ' Start driver (uses 1 COG per chain)
  display.start(chainIndex)
  
  ' Draw operations
  display.clearScreen()
  display.drawText(0, 0, string("Hello P2!"))
  display.commitScreenToPanelSet()  ' Update display
```

### Driver Architecture

#### Communication Pattern
The driver uses a command mailbox pattern for Spin2 to PASM2 communication:

```spin2
' Command definitions
#0, CMD_DONE, CMD_CLEAR, CMD_SHOW_BUFFER, CMD_FILL_COLOR, CMD_SHOW_PWM_BUFFER

' Mailbox setup
VAR
  long ptrCommand, ptrArgument
  long dvrCommand, dvrArgument
  
PUB sendCommand(cmd, arg)
  dvrArgument := arg
  dvrCommand := cmd
  repeat while dvrCommand <> CMD_DONE  ' Wait for completion
```

#### PWM Generation via Binary Code Modulation (BCM)
The driver implements PWM without hardware timers using BCM:
- Multiple bit-plane buffers (one per bit of color depth)
- Each plane displayed for exponentially increasing durations
- Bit 0: displayed 1x, Bit 1: 2x, Bit 2: 4x, etc.
- Provides 3-8 bit color depth (8-256 levels per channel)

#### Subpage Buffering Strategy
Large displays are handled via subpaging:
- COG buffer limited to 512 bytes
- Display divided into subpages that fit in COG RAM
- Sequential processing with SETQ block transfers
- Enables support for panels larger than COG memory

---

## Panel Compatibility

### Supported Panel Types
| Panel Size | Scan Rate | Address Lines | Typical Use | Notes |
|------------|-----------|---------------|-------------|--------|
| 16×32 | 1:8 | A,B,C | Small displays | Basic configuration |
| 32×16 | 1:8 | A,B,C | Wide format | Landscape orientation |
| 32×32 | 1:16 | A,B,C,D | Square displays | Common indoor |
| 64×32 | 1:16 | A,B,C,D | Standard size | Most popular |
| 64×64 | 1:32 | A,B,C,D,E | Large displays | Requires E line |
| 128×64 | 1:32 | A,B,C,D,E | Video walls | Multiple panels |
| Special | 1:4 | A,B | High density | Requires driver mod |

### LED Driver Chip Support

#### Chips Requiring Initialization
| Chip | Init Required | Special Features | Notes |
|------|---------------|------------------|--------|
| FM6126A | Yes | Control registers 11, 12 | Magic bit sequences, brightness control |
| FM6124 | No | Enclosed latch | Standard timing |
| MBI5124GP | Yes | Special reset | Different init sequence |
| ICN2037 | No | Slow clock | Extended timing |
| ICN2038S | No | Slow clock | Extended timing |
| DP5125D | No | Standard | Common chip |
| GS6238S | No | Standard | Common chip |

#### Initialization Example (FM6126A)
```spin2
' FM6126A requires writing to control registers during init
' Register 11: Brightness control (bit 0 low, rest high)
' Register 12: Enable control (bit 9 high)
PRI resetPanelFM6126() | columnIdx
  org
    drvh pinOE        ' Disable output
    drvl pinLATCH
    xor  columnIdx, columnIdx
    rep  @.end11, maxColumns
    mov  bitIdx, columnIdx
    and  bitIdx, #$0F wz
    if_z  drvl colorPins    ' Bit 0 = low
    if_nz drvh colorPins    ' Bits 1-15 = high
    ' Latch during last 11 columns for register 11
    cmp  columnIdx, last11Cols wcz
    if_nc_and_nz drvh pinLATCH
    drvh pinCLK
    waitx #511       ' Clock pulse width
    drvl pinCLK
.end11
    drvl pinLATCH
  end
```

### Pixel Pitch Options
| Pitch | Spacing | Viewing Distance | Application |
|-------|---------|------------------|-------------|
| P1.25 | 1.25mm | 1-3m | High resolution |
| P2 | 2mm | 2-5m | Indoor displays |
| P3 | 3mm | 3-8m | General purpose |
| P4 | 4mm | 4-10m | Medium distance |
| P5 | 5mm | 5-12m | Large indoor |
| P6-P10 | 6-10mm | >8m | Outdoor/large |

---

## Power Requirements

### Adapter Board Power
- Supply: 5V ±10% from P2 development board
- Quiescent Current: 20µA typical (2× 74HCT244 @ 10µA each)
- Static Current (no switching): 160µA maximum
- Operating Current @ 25MHz: 25mA typical
- Operating Current @ 35MHz: 35mA typical
- Maximum Current: 50mA (all outputs @ 40MHz)
- Power Dissipation: 175mW typical @ 35MHz
- No separate power connection required

### 74HCT244 Detailed Specifications
| Parameter | Min | Typical | Max | Unit | Conditions |
|-----------|-----|---------|-----|------|------------|
| Quiescent Current (ICC) | - | 10 | 80 | µA | Per IC, no load |
| Dynamic Current (∆ICC) | - | 0.65 | 1.8 | mA | VI = 2.4V |
| Operating Current | - | - | 25 | mA | Per IC @ 25MHz |
| Input Current | - | - | 1 | µA | Per pin |
| Input Threshold VIH | 2.0 | - | - | V | TTL compatible |
| Input Threshold VIL | - | - | 0.8 | V | TTL compatible |
| Output High VOH | 4.4 | 4.9 | - | V | IOH = -6mA |
| Output Low VOL | - | 0.1 | 0.4 | V | IOL = 6mA |
| Output Drive Current | -6 | - | +6 | mA | Per output |
| Propagation Delay tPLH | - | 13 | 18 | ns | CL = 50pF |
| Propagation Delay tPHL | - | 13 | 18 | ns | CL = 50pF |
| Maximum Frequency | - | 35 | 40 | MHz | 50% duty cycle |

### LED Panel Power (User-Supplied)
| Panel Size | Resolution | Typical Current | Peak Current | PSU Size |
|------------|------------|-----------------|--------------|----------|
| 16×32 | 512 pixels | 1.5A | 4A | 5V 5A |
| 32×32 | 1024 pixels | 2.5A | 8A | 5V 10A |
| 64×32 | 2048 pixels | 3.5A | 12A | 5V 15A |
| 64×64 | 4096 pixels | 5A | 20A | 5V 25A |

**Important**: Always use a separate high-current 5V power supply for LED panels. Never attempt to power panels through the P2 board.

---

## Driver Implementation Details

### PASM2 Output Technique
The driver uses optimized bit-bang techniques instead of the P2 Streamer:

```spin2
DAT ' PASM2 driver code
' Parallel output using SETQ/MUXQ
outputColorBits
    SETQ    maskRgb12           ' Load mask into Q register
    MUXQ    OUTA, reg_value     ' Output masked bits in parallel
    
' Alternative using SETBYTE for byte-aligned data
    altgb   byteOffset, pCogBffrIncr
    getbyte colorByte, 0-0, #0-0
    setbyte OUTA, colorByte, #3     ' Write to specific byte of OUTA
```

### HUB75 Protocol Timing
```spin2
DAT ' Scan line output sequence
scanLine
    drvh    pinOE               ' 1. Disable output during shift
    
    rep     @.endCols, columnCount
    setbyte OUTA, colorByte, #3 ' 2. Output color data
    drvl    pinCLK              ' 3. Clock low
    waitx   #4                  ' 4. Setup time
    drvh    pinCLK              ' 5. Clock high
.endCols
    
    drvh    pinLATCH            ' 6. Latch pulse
    waitx   #3
    drvl    pinLATCH
    
    add     row_addr, #1        ' 7. Update row address
    call    #emitAddr
    
    drvl    pinOE               ' 8. Enable output
```

### Multi-Panel Configuration
The driver supports up to 3 adapter boards (chains) simultaneously:
- Each chain runs in its own COG
- Chains can have different panel configurations
- Configuration tables define each chain's parameters
- Runtime detection of panel types and LED driver chips

---

## Performance Characteristics

### Refresh Rate vs Panel Size (P2 @ 200MHz)
| Panel Size | Colors | Max Refresh Rate | Data Rate |
|------------|--------|------------------|-----------|
| 32×32 | 24-bit | 240 Hz | 5.9 Mbps |
| 64×32 | 24-bit | 120 Hz | 5.9 Mbps |
| 64×64 | 24-bit | 60 Hz | 5.9 Mbps |
| 128×64 | 24-bit | 30 Hz | 5.9 Mbps |

### Timing Requirements
| Parameter | Min | Typical | Max | Unit |
|-----------|-----|---------|-----|------|
| Clock Period | 14 | 20 | 1000 | ns |
| Clock Pulse Width | 7 | 10 | - | ns |
| Setup Time (Data to Clock) | 5 | - | - | ns |
| Hold Time (Clock to Data) | 5 | - | - | ns |
| Latch Pulse Width | 100 | 200 | - | ns |
| OE Pulse Width | 100 | - | - | ns |

---

## Mechanical Drawing

```
                           71mm (2.8")
        ┌─────────────────────────────────────┐
        │                                     │
        │  ┌───────┐           ┌───────┐     │ 48mm
        │  │ J1    │           │ J2    │     │ (1.9")
        │  │ 2×6   │           │ 2×6   │     │
        │  └───────┘           └───────┘     │
        │                                     │
        │         ┌─────────────┐            │
        │         │   HUB75     │            │
        │         │  16-pin IDC │            │
        │         └─────────────┘            │
        └─────────────────────────────────────┘
        
        Component Side View
```

---

## Compatible Development Boards

### P2 Eval Board (#64000-ES)
- Direct connection to headers P16-P31
- Alternative: P0-P15, P32-P47, P48-P63
- Full 64 I/O access

### P2 Edge Module Breadboard (#64020)
- Standard configuration: P32-P47
- Requires P2 Edge Module (#P2-EC)
- Breadboard area for additional circuits

### P2 Edge Mini Breakout Board (#64019)
- Compact form factor
- Standard configuration: P32-P47
- Requires P2 Edge Module (#P2-EC)

---

## Ordering Information

| Part Number | Description | Status |
|-------------|-------------|--------|
| 64032 | P2 Eval HUB75 Adapter Board | Retiring* |

*Limited to stock on hand. Check Parallax store for availability.

### Additional Required Items (Not Included)
- P2 Development Board (see compatible boards above)
- HUB75 LED Panel(s) - Available from various suppliers
- 5V Power Supply - Sized for panel requirements
- 16-pin IDC Cable - Usually included with panels

### Where to Buy HUB75 Panels
- AliExpress (search "HUB75")
- Adafruit Industries
- SparkFun Electronics
- Amazon

---

## Support Resources

### Documentation
- **GitHub Repository**: https://github.com/ironsheep/P2-HUB75-LED-Matrix-Driver
- **P2 Object Exchange (OBEX)**: ISP HUB75 Driver
- **Quick Start Guide**: See GitHub repository
- **API Documentation**: Included with driver

### Community Support
- **Parallax Forums**: P2 Discussion
- **GitHub Issues**: Bug reports and feature requests
- **Author Contact**: Stephen Moraco (Iron Sheep Productions)

### Example Projects
- Scrolling text display
- Spectrum analyzer
- Clock and weather display
- Game displays
- Data visualization dashboards

---

## Compliance Information

### Regulatory
- RoHS Compliant
- CE Marked (pending)
- FCC Part 15 Class B (pending)

### Environmental
- Lead-free assembly
- Recyclable materials
- Low power consumption

---

## Design Notes

### Why 74HCT244?
The 74HCT244 was specifically chosen for this application because:
- **HCT Input Stages**: TTL-compatible thresholds (2.0V VIH) reliably accept 3.3V logic from P2
- **CMOS Outputs**: Full 5V swing provides maximum noise immunity for HUB75 panels
- **Speed**: Supports 35-40MHz reliable operation, exceeding typical HUB75 requirements (10-25MHz)
- **Drive Strength**: ±6mA output current easily drives high-impedance HUB75 inputs
- **Low Power**: Only 10µA typical quiescent current per IC (80µA max)
- **Availability**: Common part, easily sourced worldwide
- **Cost Effective**: Provides 8 channels per IC at low cost

### Alternative Level Shifters
While other level shifters could work, the 74HCT244 provides the optimal balance:
- 74HCT245: Bidirectional, but not needed (all signals are outputs)
- 74AHCT244: Faster, but unnecessary for HUB75 speeds
- TXB0108: Bidirectional auto-sensing, adds complexity without benefit
- Discrete transistors: Would require 14 circuits, more PCB space

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | 2020 | Initial release |
| 1.4 | 2021 | Current production version, dual 74HCT244 design |

---

## Disclaimer

Specifications subject to change without notice. Iron Sheep Productions, LLC and Parallax Inc. assume no responsibility for any errors which may appear in this document. No patent licenses are implied.

---

## Contact Information

**Iron Sheep Productions, LLC**  
Developer: Stephen Moraco  
GitHub: @ironsheep  
Support: Via GitHub repository  

**Parallax Inc.**  
599 Menlo Drive, Suite 100  
Rocklin, CA 95765  
Phone: 916-624-8333  
Web: www.parallax.com  

---

*Copyright © 2024 Iron Sheep Productions, LLC. All rights reserved.*  
*Propeller 2 is a trademark of Parallax Inc.*  
*HUB75 is an industry standard interface.*

---

## Quick Reference Card

### Pin Assignments (P16 Base)
```
Signal: CLK  OE#  LAT  A    B    C    D    E    R1   G1   B1   R2   G2   B2
P2 Pin: P16  P17  P18  P19  P20  P21  P22  P23  P24  P25  P26  P27  P28  P29
Offset: +0   +1   +2   +3   +4   +5   +6   +7   +8   +9   +10  +11  +12  +13
```

### Initialization Sequence
1. Set pins P16-P29 as outputs
2. Set OE# high (disabled)
3. Set CLK and LAT low
4. Configure panel parameters
5. Start refresh routine

### Typical Power Budget
- P2 Board: 200-400mA @ 5V
- Adapter: 40mA @ 5V  
- LED Panel: 2-5A @ 5V (separate supply)
- Total System: ~5A @ 5V recommended