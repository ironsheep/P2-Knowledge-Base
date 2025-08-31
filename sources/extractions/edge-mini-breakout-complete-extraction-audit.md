# P2 Edge Mini Breakout Board - Complete Extraction Audit

**Source Document**: `64019-P2-Edge-MiniBreakoutBoardGuide-v1.1.pdf`  
**Document Type**: Hardware Guide - P2 Edge Breakout Board  
**Version**: v1.1 (11/30/2020)  
**Pages**: 10  
**Extraction Date**: 2025-08-24  
**Trust Level**: GREEN (Official Parallax documentation, current version)  
**Extraction Completeness**: 100% (Complete systematic extraction)  

## Document Overview

**Product**: P2 Edge Mini Breakout Board (#64019)  
**Purpose**: Compact interface to P2 Edge Module for experimenting and developing with Propeller 2  
**Compatibility**: Designed for P2 Edge Module (#P2-EC)  

## Key Technical Specifications

### Power Requirements
- **Input Voltage**: 5 VDC (absolute maximum 5.5 VDC)
- **Input Current**: Recommended minimum 100 mA, maximum per application
- **Power Jack**: 2.1 mm center-positive DC barrel jack
- **VIO Power Supplies**: 3.3 V up to 300 mA per 8 I/O pins (requires P2 Edge Module)

### Physical Specifications
- **PCB Dimensions**: 3.15 x 1.4 in (80 x 35.5 mm)
- **Operating Temperature**: -40 to +185 °F (-40 to +85 °C)
- **Socket**: 0.05 in (1.27 mm) pitch, 80-way vertical socket for P2 Edge Module

### Programming Options
- **USB Programming**: Serial up to 2 MBaud (requires Prop Plug #32201)
- **Wireless Programming**: Up to 2 MBaud (requires P2 WX WiFi Adapter #64007 + WX WiFi SIP module #32420S)

## **CRITICAL FINDING: Pin Availability Analysis**

### Available Pin Groups
**Pins Available at Headers**: P0–P31 and P56–P63 = **40 pins total**
**Pins Requiring Bottom-Side Access**: P32–P55 (24 pins via jumper wires to prototyping sections)

### Pin Group Breakdown
1. **P0–P7**: Header available, 3.3V LDO V00 (300mA shared)
2. **P8–P15**: Header available, 3.3V LDO V08 (300mA shared)  
3. **P16–P23**: Header available, 3.3V LDO V16 (300mA shared)
4. **P24–P31**: Header available, 3.3V LDO V24 (300mA shared) - **NO 5V output**
5. **P32–P39**: NO header, requires bottom-side jumpers to prototyping
6. **P40–P47**: NO header, requires bottom-side jumpers to prototyping
7. **P48–P55**: NO header, requires bottom-side jumpers to prototyping
8. **P56–P63**: Header available, 3.3V LDO V56 (300mA shared) - **NO 5V output**, **includes RES pin**

## Hardware Features

### Main Components
1. **P2 Edge Module Socket**: Vertical 80-way socket with polarity protection
2. **Power Jack**: 2.1 mm center-positive for 5 VDC supply
3. **Prop Plug Header**: 4-pin programming/debugging header (∇ △ RES VSS)
4. **Reset Button**: Manual P2 microcontroller reset
5. **Prototyping Areas**: Two 4×5 hole matrices (0.1" pitch, 40 holes total)
6. **Mounting Holes**: Four plated holes connected to ground plane

### I/O Headers Configuration
- **Four 2×6 Headers with 5V**: P0-P7, P8-P15, P16-P23, P48-P55
- **Two 2×6 Headers without 5V**: P24-P31, P56-P63
- **Each Header Provides**: Two GND, one Vxx (3.3V), optional 5V, 8 I/O pins

### Special Function Pins (P56-P63)
- **P56**: Buffered LED
- **P57**: Buffered LED  
- **P58**: Flash SPI DO (MISO)
- **P59**: Flash SPI DI (MOSI)
- **P60**: Flash SPI CLK
- **P61**: Flash SPI CS
- **P62**: Prop-Plug RXD (P2 TXD)
- **P63**: Prop-Plug TXD (P2 RXD)

## Compatible Products & Ecosystem

### Getting Started Kit
- P2 Edge Module (#P2-EC)
- P2 Edge Mini Breakout Board (#64019)
- USB A to DC 2.1mm Jack Cable (#805-00019)
- Breadboard (#700-32023)
- Jumper Wire Sets (#800-00064, #800-00065)
- Prop Plug (#32201)
- USB A to Micro B Cable (#805-00016)

### Add-on Options
- **Wireless**: P2 to WX Adapter (#64007) + WX ESP8266 Module (#32420S)
- **Click/mikroBUS**: P2 to MicroBUS Click Adapter (#64008) - 900+ modules
- **Parallax Add-ons**: P2-ES Eval Board Accessory Set (#64006-ES), HyperRAM/HyperFLASH, Protoboard

## Critical Design Constraints

### Power Supply Warnings
⚠️ **CRITICAL**: Never exceed 5.5 VDC input voltage  
⚠️ **CRITICAL**: Do NOT apply voltage to Vxx pins (they are outputs)  
⚠️ **CRITICAL**: Do NOT join Vxx pins together (isolation required)

### Module Orientation
- **Correct Installation**: P0 and P38 edge pads align with PCB labels
- **Component Side**: Must face RESET button
- **Polarity Protection**: Available on power pads, but I/O damage possible

### VIO Power Limitations
- **Per Group**: 300mA total per 8-pin group
- **Per Pin**: 30mA source/sink maximum
- **Logic Level**: 3.3V only
- **Alternative**: Use Parallax Power Pal (#32133) for higher current

## Cross-Reference Analysis

### Relationship to P2 Edge Modules
This breakout board is **universal** - compatible with:
- ✅ **P2 Edge Standard Module** (64 pins available)
- ✅ **P2 Edge 32MB Module** (46 pins available)

**Key Difference**: The 32MB module's PSRAM usage (P40-P57) doesn't affect this breakout because those pins aren't brought to headers anyway - they require bottom-side access.

### Pin Access Comparison
| Pin Group | Mini Breakout Access | Standard Edge | 32MB Edge |
|-----------|-------------------|---------------|-----------|
| P0-P31 | ✅ Headers | ✅ Available | ✅ Available |
| P32-P39 | ⚠️ Jumpers only | ✅ Available | ❌ Used by PSRAM |
| P40-P47 | ⚠️ Jumpers only | ✅ Available | ❌ Used by PSRAM |  
| P48-P55 | ⚠️ Jumpers only | ✅ Available | ❌ Used by PSRAM |
| P56-P63 | ✅ Headers | ✅ Available | ✅ Available |

## Programming & Development

### Software Support
- **Primary**: Propeller Tool (SPIN/PASM languages)
- **Alternative**: Third-party tools (C, BASIC, Forth)
- **Resources**: www.parallax.com search "P2-EC"

### Development Workflow
1. Connect P2 Edge Module to Mini Breakout
2. Apply 5V power via DC jack
3. Connect Prop Plug for programming
4. Use headers P0-P31, P56-P63 for immediate access
5. Add jumpers to prototyping sections for P32-P55 access

## Questions for Enhanced Coverage

### Performance & Capability Questions
1. **Power Budget Analysis**: What's the total current draw with all 8 LDO regulators at full 300mA load?
2. **Thermal Management**: Are there thermal considerations when using multiple high-current I/O groups simultaneously?
3. **Signal Integrity**: What are the trace impedances and crosstalk characteristics for high-speed I/O?

### Design Decision Questions  
4. **P32-P55 Access**: Why weren't these pins brought to headers? Space constraints or design philosophy?
5. **5V Header Selection**: What's the rationale for excluding 5V from P24-P31 and P56-P63 headers?
6. **Prototyping Sections**: What's the intended use case for the 4×5 hole matrices?

### Compatibility Questions
7. **Module Variants**: Are there mechanical clearance issues with different Edge module heights/components?
8. **Accessory Compatibility**: Which P2 accessory boards have known fit/clearance issues?
9. **Future Compatibility**: Is the design forward-compatible with planned P2 Edge module variants?

### Development Workflow Questions
10. **Pin Assignment Strategy**: What's the recommended pin assignment for projects using both headers and jumpers?
11. **Debugging Capabilities**: Can the Prop Plug debug running programs or only program/reset?
12. **Multi-Board Systems**: Can multiple Mini Breakouts share a single power supply safely?

## Source Quality Assessment

**Trust Level**: GREEN  
- Official Parallax documentation
- Current version (v1.1, 2020)
- Professional technical writing
- Comprehensive specifications
- Clear warnings and cautions

**Extraction Completeness**: 100%
- All technical specifications captured
- Complete pin assignments documented  
- Full compatibility matrix extracted
- All warnings and constraints noted
- Programming options fully detailed

**Question Coverage**: ~40%
- Basic specifications well covered
- Hardware features completely documented
- Advanced performance characteristics missing
- Design rationale questions unanswered  
- Multi-board system guidance limited

**Strategic Priority**: MEDIUM-HIGH
- Critical for Edge module compatibility understanding
- Essential for developer board selection
- Lower priority than 32MB performance research
- Supports breadboard compatibility analysis

---

**Extraction Status**: ✅ COMPLETE  
**Next Action**: Ready for breadboard compatibility matrix analysis  
**Cross-Reference**: Links to P2 Edge Module extractions for complete system understanding