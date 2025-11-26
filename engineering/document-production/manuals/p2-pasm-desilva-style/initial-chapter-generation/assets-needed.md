# P2 Assembly Manual - Assets Needed

**Document**: P2 Assembly Manual v1.0  
**Status**: Initial draft complete, PDF generation requested  
**Created**: August 20, 2025  
**Location**: `/documentation/manuals/pasm2-manual/`

## 🔧 PDF Forge Requirements

### LaTeX Packages Needed
**For Formatting Implementation**:
```bash
# Debian/Ubuntu packages for PDF Forge machine:
apt-get install texlive-fonts-extra    # Charter, Palatino fonts
apt-get install texlive-latex-extra    # mdframed, tcolorbox
apt-get install texlive-xetex          # XeLaTeX for better font support

# TeX packages (come with above):
# - XCharter or charter (body/heading font)
# - sourcecodepro (code font)
# - tcolorbox (sidetrack boxes)
# - mdframed (background colors)
# - soul (inline highlighting)
```

### Font Decision
- **Body & Headings**: Charter or Palatino (unified serif family)
- **Code**: Source Code Pro or Consolas (not Courier)
- **Reasoning**: Reduces cognitive load vs mixed serif/sans-serif

## 📦 Content Updates Required

### Pin Number Changes
**Status**: 19 instances need updating in Chapter 1  
**Current**: Uses board-specific pin 56  
**Required**: Change to universal pin 16  
**Details**: See [Pin Updates Needed](pin-updates-needed.md)  
**Rationale**: Examples should work universally, not require specific boards

## 🔴 Critical Assets Needed

### 1. Smart Pin Mode Constants
**Location in Manual**: Chapter 8, all Smart Pin examples  
**What's Missing**: Actual P_* constant values for Smart Pin modes  
**Current State**: Using placeholder values like `##P_ASYNC_TX`, `##P_PWM_TRIANGLE`  
**What's Needed**:
- Complete list of P_* constants with their hex values
- Format: `P_ASYNC_TX = $xxxxxx` 
- Source: P2 silicon documentation or Spin2 constant definitions
- **Files to check**: 
  - Spin2 interpreter source
  - P2 object files (.spin2)
  - Silicon documentation

### 2. Timing and Clock Constants
**Location in Manual**: Throughout, especially Chapter 1  
**What's Missing**: Precise clock timing values  
**Current State**: Using approximations (##25_000_000 for 0.25 seconds)  
**What's Needed**:
- Exact clock frequency constants
- BAUD rate calculation formulas
- Clock configuration register values
- Format: Constants with explanatory comments

### 3. CORDIC Pipeline Details
**Location in Manual**: Chapter 7  
**What's Missing**: Exact pipeline timing and operation codes  
**Current State**: States "55 clocks" but lacks precision on pipeline stages  
**What's Needed**:
- Exact clock counts for each CORDIC operation
- Pipeline stage details
- QROTATE, QVECTOR operation encoding
- Format: Timing diagram or table

### 4. Instruction Encoding Tables
**Location in Manual**: Appendix A  
**What's Missing**: Complete instruction encoding bit patterns  
**Current State**: Only shows syntax and basic operation  
**What's Needed**:
- 32-bit instruction encoding for each instruction
- Bit field layouts (COND, INSTR, CZ, I, D, S fields)
- Format: Tables showing bit positions
- Source: P2 instruction set documentation

### 5. Video Generation Timing
**Location in Manual**: Chapter 13  
**What's Missing**: Actual VGA/HDMI timing values  
**Current State**: Placeholder values (##HSYNC_TIMING, ##VSYNC_TIMING)  
**What's Needed**:
- VGA timing for standard resolutions (640x480, 800x600, 1024x768)
- HDMI timing parameters
- Streamer command encoding
- Format: Complete timing tables with actual values

### 6. Hardware Multiply/Divide Specifics
**Location in Manual**: Chapter 5  
**What's Missing**: Exact cycle counts and overflow behavior  
**Current State**: General descriptions  
**What's Needed**:
- Exact cycle counts for MUL, MULS, DIV, DIVS
- Overflow/underflow behavior
- Special cases (divide by zero, etc.)
- Format: Detailed operation tables

### 7. Skip Pattern Encoding
**Location in Manual**: Chapter 6  
**What's Missing**: Complete SKIP/SKIPF pattern encoding  
**Current State**: Shows concept but not all encoding options  
**What's Needed**:
- Full 32-bit skip pattern format
- EXECF interaction
- Maximum skip lengths
- Format: Bit pattern examples with explanations

### 8. Interrupt Vector Details
**Location in Manual**: Chapter 11  
**What's Missing**: Interrupt vector addresses and setup  
**Current State**: Conceptual only  
**What's Needed**:
- Interrupt vector locations
- SETINT1/SETINT2/SETINT3 encoding
- Interrupt source encoding
- Format: Complete setup examples

### 9. Memory Map Specifics
**Location in Manual**: Chapter 2  
**What's Missing**: Special register locations  
**Current State**: Mentions "last 16 longs" but lacks details  
**What's Needed**:
- Complete COG RAM special register map
- LUT RAM addressing
- Debug register locations
- Format: Memory map diagram with addresses

### 10. Real Hardware Examples
**Location in Manual**: Throughout all chapters  
**What's Missing**: Tested, verified code examples  
**Current State**: Examples are conceptually correct but untested  
**What's Needed**:
- Test each example on actual P2 hardware
- Verify timing values
- Confirm pin assignments for different boards
- Format: Verified code with test results

## 📊 Asset Priority Matrix

| Priority | Asset | Blocks | Chapter Impact |
|----------|-------|--------|----------------|
| 🔴 HIGH | Smart Pin Constants | Examples won't compile | Ch 8, 14, 15 |
| 🔴 HIGH | Instruction Encoding | Reference incomplete | Appendix A |
| 🟡 MEDIUM | CORDIC Details | Examples approximate | Ch 7 |
| 🟡 MEDIUM | Video Timing | Can't generate video | Ch 13 |
| 🟡 MEDIUM | Clock Constants | Timing imprecise | Throughout |
| 🟢 LOW | Interrupt Details | Rarely used | Ch 11 |
| 🟢 LOW | Skip Encoding | Advanced feature | Ch 6 |

## 📁 Suggested Sources

1. **P2 Silicon Documentation** (Rev B/C)
   - Should contain all instruction encodings
   - Has Smart Pin mode descriptions
   - Contains CORDIC details

2. **Spin2 Interpreter Source**
   - Contains all P_* constants
   - Has clock configuration code
   - Shows practical usage patterns

3. **P2 Object Exchange**
   - Working video drivers with timing
   - Serial communication objects
   - Tested code examples

4. **Parallax Forums**
   - Community-verified timing values
   - Hardware-tested examples
   - Board-specific pin assignments

## ✅ Verification Checklist

When providing assets, please include:
- [ ] Source document/file name
- [ ] Page/line number reference
- [ ] Version/revision of source
- [ ] Test verification (if applicable)
- [ ] Any caveats or limitations

## 📝 Notes

- Constants should be in both hex and decimal where useful
- Include comments explaining what values mean
- Provide both P2 Eval and P2 Edge pin mappings where different
- Mark any P2 revision-specific differences (Rev B vs Rev C)

---

**Last Updated**: August 20, 2025  
**Next Review**: After assets collected