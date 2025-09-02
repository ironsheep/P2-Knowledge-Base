# V4 to V5 Enhancement Audit - BEFORE State

**Date**: 2025-09-01
**Document**: P2-Smart-Pins-Green-Book-Tutorial-v4.md
**Purpose**: Document current state before adding PASM2 examples for V5

## Current Coverage Analysis

| Mode | Name | Spin2 | PASM2 | Status | Action Needed |
|------|------|-------|-------|--------|---------------|
| %00000 | Smart Pin OFF (Default State) | 1 | 0 | ⚠️ Missing PASM2 | Add PASM2 |
| %00001 | Repository Mode (Shared Storage) | 3 | 2 | ✅ Balanced | Maybe add 1 PASM2 |
| %00010 & %00011 | DAC Output Modes | 30 | 2 | ⚠️ Heavily imbalanced | Add many PASM2 |
| %00100 | Pulse/Cycle Output | 1 | 1 | ✅ Balanced | Good |
| %00101 | NCO Frequency | 2 | 1 | ✅ Balanced | Maybe add 1 PASM2 |
| %00110 | NCO Duty | 1 | 0 | ⚠️ Missing PASM2 | Add PASM2 |
| %00111 | Transition Output | 1 | 1 | ✅ Balanced | Good |
| %01000 | PWM Sawtooth | 1 | 1 | ✅ Balanced | Good |
| %01001 | PWM Triangle | 1 | 1 | ✅ Balanced | Good |
| %01010 | Switch-Mode Power Supply | 1 | 1 | ✅ Balanced | Good |
| %01011 | Quadrature Encoder | 2 | 1 | ✅ Balanced | Maybe add 1 PASM2 |
| %01100 | Count Rises | 2 | 0 | ⚠️ Missing PASM2 | Add 2 PASM2 |
| %01101 | A-B Encoder (Inc/Dec) | 1 | 0 | ⚠️ Missing PASM2 | Add PASM2 |
| %01110 | Incremental Encoder | 1 | 0 | ⚠️ Missing PASM2 | Add PASM2 |
| %01111 | Local/Global Comparator | 4 | 0 | ⚠️ Missing PASM2 | Add 4 PASM2 |
| %11000 & %11001 | USB Host/Device Modes | 1 | 0 | ⚠️ Missing PASM2 | Add PASM2 |
| %11010 | Oscilloscope Mode | 0 | 0 | ❌ No examples | Add both |
| %11011 | Synchronous Serial Transmit | 3 | 1 | ⚠️ Imbalanced | Add 2 PASM2 |
| %11111 | ADC Input Modes | 29 | 0 | ⚠️ Missing PASM2 | Add many PASM2 |

## Summary Statistics

### Current State (V4):
- **Total Smart Pin modes documented**: 19 (some grouped)
- **Modes with both languages**: 9
- **Modes with Spin2 only**: 9
- **Modes with PASM2 only**: 0
- **Modes with no examples**: 1

### Code Distribution:
- **Total Spin2 examples**: 87
- **Total PASM2 examples**: 12
- **Current ratio**: 7.25:1 (Spin2:PASM2)

## Critical Gaps

### Modes Completely Missing PASM2:
1. %00000 - Smart Pin OFF
2. %00110 - NCO Duty
3. %01100 - Count Rises (2 Spin2 examples)
4. %01101 - A-B Encoder
5. %01110 - Incremental Encoder
6. %01111 - Local/Global Comparator (4 Spin2 examples!)
7. %11000/%11001 - USB Modes
8. %11111 - ADC Input (29 Spin2 examples!)

### Most Imbalanced:
1. **ADC Input**: 29 Spin2, 0 PASM2
2. **DAC Output**: 30 Spin2, 2 PASM2
3. **Comparator**: 4 Spin2, 0 PASM2

## Target for V5

### Goals:
- Achieve closer to 1:1 ratio for Spin2:PASM2
- Every mode should have at least 1 PASM2 example
- Critical modes (ADC, DAC) need multiple PASM2 examples
- Add examples for Oscilloscope mode

### Expected After Enhancement:
- Target ~75-80 PASM2 examples (from current 12)
- Target ratio: ~1.1:1 (from current 7.25:1)
- All modes with at least basic PASM2 coverage

## Available Resources

### Titus Code Files:
- 47 PASM2 files available in `/engineering/ingestion/sources/smart-pins/assets/code-20250824/`
- 17 Spin2 files for reference
- 34 configuration snippets

### Next Steps:
1. Map Titus reqXX files to specific modes
2. Identify which files provide the missing PASM2 examples
3. Insert PASM2 examples after corresponding Spin2 examples
4. Ensure proper blank lines for formatting
5. Create V5 and re-audit