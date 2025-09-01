# P2 Edge Standard Breakout Board - Complete Extraction Audit

**Source Document**: `64029-P2-Edge-Breakout-Board-Guide-20230301.pdf`  
**Document Type**: Hardware Guide - P2 Edge Standard Breakout Board  
**Version**: v1.0 (03/01/2023)  
**Pages**: 11  
**Extraction Date**: 2025-08-24  
**Trust Level**: GREEN (Official Parallax documentation, current version)  
**Extraction Completeness**: 100% (Complete systematic extraction)  

## Document Overview

**Product**: P2 Edge Breakout Board (#64029)  
**Purpose**: Standard interface to P2 Edge Module for experimenting and developing with Propeller 2  
**Compatibility**: Designed for P2 Edge Module (#P2-EC)  
**Key Differentiator**: **ALL 64 P2 pins available at convenient headers**

## Key Technical Specifications

### Power Requirements
- **Input Voltage**: 5 VDC (absolute maximum 5.5 VDC)
- **Input Current**: Recommended minimum 100 mA, maximum per application
- **Power Jack**: 2.1 mm center-positive DC barrel jack
- **VIO Power Supplies**: 3.3 V up to 300 mA per 8 I/O pins (requires P2 Edge Module)
- **Current Rating**: Up to 3A for heavy load and multi-cog use

### Physical Specifications
- **PCB Dimensions**: 4 x 1.4 in (101.6 x 35.6 mm) - **LARGER than Mini**
- **Operating Temperature**: -40 to +185 °F (-40 to +85 °C)
- **Socket**: 0.05 in (1.27 mm) pitch, 80-way vertical socket for P2 Edge Module
- **Mounting**: Four 3.2 mm diameter plated holes connected to GND

### Programming Options
- **USB Programming**: Serial up to 2 MBaud (requires Prop Plug #32201)
- **Wireless Programming**: Up to 2 MBaud (requires P2 WX WiFi Adapter #64007 + WX WiFi SIP module #32420S)

## **CRITICAL FINDING: Complete Pin Access**

### **ALL 64 PINS Available at Headers**
**This is the KEY differentiator from the Mini Breakout Board!**

### Pin Header Configuration
**Eight 2×6 Headers**: All pins P0–P63 accessible (8 groups × 8 pins = 64 pins)

1. **P0–P7**: Header with 5V, 3.3V LDO V00 (300mA shared)
2. **P8–P15**: Header with 5V, 3.3V LDO V08 (300mA shared)  
3. **P16–P23**: Header with 5V, 3.3V LDO V16 (300mA shared)
4. **P24–P31**: Header **without 5V**, 3.3V LDO V24 (300mA shared)
5. **P32–P39**: Header with 5V, 3.3V LDO V32 (300mA shared)
6. **P40–P47**: Header with 5V, 3.3V LDO V40 (300mA shared)
7. **P48–P55**: Header with 5V, 3.3V LDO V48 (300mA shared)
8. **P56–P63**: Header **without 5V**, 3.3V LDO V56 (300mA shared), **includes RES pin**

### 5V Power Distribution
- **6 headers WITH 5V**: P0-P23, P32-P55 (48 pins)
- **2 headers WITHOUT 5V**: P24-P31, P56-P63 (16 pins)
- **Controllable**: Via "HDR 5V ON" jumper on power header

## Hardware Features

### Unique Power Management System
**2×3 Power Header** with pre-installed jumpers:
- **"PWR ON" jumper**: Controls entire board power
- **"HDR 5V ON" jumper**: Controls 5V to accessory headers only
- **Pro Tip**: Remove HDR 5V ON jumper if not using 5V to reduce damage risk

### Module Orientation System
- **White orientation circle** on PCB bottom-left
- **Alignment**: Module's orientation hole closest to white circle
- **Component side**: Must face RESET button

### Comprehensive I/O Access
- **No prototyping sections needed**: All pins at headers
- **Immediate access**: P0-P63 ready for jumper wires
- **Professional layout**: Eight organized header groups

## Compatible Accessories & Ecosystem

### Enhanced Add-on Selection
**More add-ons listed than Mini Breakout:**
- **P2-ES Eval Board Accessory Set** (#64006-ES)
- **HyperRAM & HyperFLASH Add-On** (#64004-ES)
- **Protoboard Add-on** (#64005-ES)
- **P2 microSD Add-on Board** (#64009) ⭐ NEW
- **Universal Motor Driver P2 Add-on Board** (#64010) ⭐ NEW
- **P2 RTC Add-on Board** (#64013) ⭐ NEW
- **P2 HD Audio Add-on Set** (#64014) ⭐ NEW
- **P2 Eval HUB75 Adapter Board** (#64032) ⭐ NEW

### Programming Compatibility
- **Prop Plug**: Same 4-pin header (∇ △ RES VSS)
- **Wireless**: P56-P63 header for WX adapter
- **Reset**: Button + RES pin at P56-P63 header

## Cross-Reference Analysis vs Mini Breakout

### **MAJOR ADVANTAGE: No Pin Access Compromises**

| Feature | Mini Breakout (#64019) | Standard Breakout (#64029) |
|---------|----------------------|---------------------------|
| **All pins at headers** | ❌ Only P0-P31, P56-P63 (40 pins) | ✅ ALL P0-P63 (64 pins) |
| **P32-P55 access** | ⚠️ Bottom jumpers only | ✅ Convenient headers |
| **5V headers** | 4 headers (32 pins) | 6 headers (48 pins) |
| **Size** | 3.15 × 1.4 in (compact) | 4.0 × 1.4 in (larger) |
| **Prototyping areas** | ✅ Two 4×5 matrices | ❌ None needed |
| **Add-on compatibility** | Good selection | Enhanced selection |

### Module Compatibility Analysis

| Module Type | Standard Breakout Benefit | Trade-off |
|-------------|--------------------------|-----------|
| **P2 Edge Standard** | ✅ **Perfect match** - full 64-pin access | Larger form factor |
| **P2 Edge 32MB** | ⚠️ **Unused headers** - P32-P55 inaccessible | Wasted board space |

## Special Function Pins (P56-P63)
**Same as all other breakouts:**
- **P56**: Buffered LED
- **P57**: Buffered LED  
- **P58**: Flash SPI DO (MISO)
- **P59**: Flash SPI DI (MOSI)
- **P60**: Flash SPI CLK
- **P61**: Flash SPI CS
- **P62**: Prop-Plug RXD (P2 TXD)
- **P63**: Prop-Plug TXD (P2 RXD)

## Power System Architecture

### VIO Supply Mapping
**All 8 LDO regulators utilized:**
```
V00: Powers P0-P7   + header supply + optional 5V
V08: Powers P8-P15  + header supply + optional 5V
V16: Powers P16-P23 + header supply + optional 5V
V24: Powers P24-P31 + header supply (3.3V only)
V32: Powers P32-P39 + header supply + optional 5V
V40: Powers P40-P47 + header supply + optional 5V
V48: Powers P48-P55 + header supply + optional 5V
V56: Powers P56-P63 + header supply (3.3V only)
```

### Power Safety Features
⚠️ **CRITICAL WARNINGS**:
- Never exceed 5.5 VDC input voltage
- Do NOT apply voltage to Vxx pins (they are outputs)
- Do NOT join Vxx pins together
- **5V pins are NOT 5V tolerant** - 3.3V I/O only!
- Remove HDR 5V ON jumper if not using 5V supply

## Questions for Enhanced Coverage

### **Design Decision Questions**
1. **Size Trade-off**: What projects justify the larger 4" form factor vs 3.15" Mini?
2. **Pin Header Selection**: Why do P24-P31 and P56-P63 lack 5V while others have it?
3. **Power Management**: What's the advantage of controllable 5V via jumpers?

### **Performance Questions**  
4. **Multi-Board Power**: Can multiple Standard Breakouts share a 5V supply safely?
5. **Current Distribution**: What's the total current draw with all 8 LDOs at full load?
6. **Thermal Considerations**: Are there thermal limits with high current on multiple headers?

### **Application Questions**
7. **Add-on Stacking**: How many P2 add-on boards can be stacked simultaneously?
8. **Pin Assignment Strategy**: What's the recommended approach for 64-pin projects?
9. **Breadboard Integration**: What's the best way to interface with standard breadboards?

### **Selection Criteria Questions**
10. **vs Mini Breakout**: When is the Standard board worth the extra size/cost?
11. **vs Larger Breakouts**: Are there even larger P2 breakout options available?
12. **Module Pairing**: Which P2 Edge module variants work best with this breakout?

## Source Quality Assessment

**Trust Level**: GREEN  
- Official Parallax documentation
- Current version (v1.0, 2023)
- Professional technical writing
- Comprehensive specifications
- Enhanced accessory coverage vs Mini

**Extraction Completeness**: 100%
- All technical specifications captured
- Complete pin assignments documented  
- Full accessory compatibility noted
- Power management system fully detailed
- All warnings and constraints captured

**Question Coverage**: ~35%
- Hardware specifications well covered
- Pin assignments completely documented
- Power system architecture clear
- Design rationale questions unanswered  
- Application guidance limited
- Selection criteria incomplete

**Strategic Priority**: MEDIUM-HIGH
- Essential for Standard module users
- Critical for 64-pin project decisions
- Lower priority than performance research
- Supports complete breakout selection matrix

---

## **STRATEGIC COMPATIBILITY INSIGHT**

### **Perfect for P2 Edge Standard Module**
- **Zero compromises**: Full 64-pin header access
- **Professional development**: All pins immediately accessible
- **Expansion ready**: Enhanced add-on board selection
- **Future-proof**: Supports full P2 pin utilization

### **Inefficient for P2 Edge 32MB Module**
- **Wasted space**: P32-P55 headers unusable
- **Size penalty**: 27% larger than Mini with no benefit
- **Cost inefficiency**: Paying for unused capability

### **Decision Framework**
```
If using Standard P2 Edge Module → Standard Breakout Board
If using 32MB P2 Edge Module → Mini Breakout Board
If unsure about pin count needs → Standard Breakout Board
```

---

**Extraction Status**: ✅ COMPLETE  
**Next Action**: Create comprehensive 3-board compatibility matrix  
**Cross-Reference**: Links to Edge module analyses for complete system understanding