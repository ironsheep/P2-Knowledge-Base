# TikZ Diagram Integration Plan for Smart Pins Tutorial

## Overview

**Working Document Location:** `/engineering/document-production/workspace/p2-smart-pins-tutorial/P2-Smart-Pins-Green-Book-Tutorial.md`

The workspace markdown document is the authoritative source (3607 lines, Sep 10). It references images from `v6-assets/` but the actual images are in `assets/` - this path mismatch needs fixing.

The opus-master-green-book versions are historical snapshots.

Many images can be replaced with TikZ diagrams from the new `p2kb-smartpins-diagrams.sty` package located in:
`/engineering/document-production/workspace/p2-smart-pins-tutorial/templates/`

## Current Image References in v7.md

| Line | Current Reference | Caption | Status |
|------|------------------|---------|--------|
| 148 | `v6-assets/P2 SmartPins-220809_page03_img01.png` | Basic I/O Output Timing | **REPLACE** with `\DRVHTimingDiagram` |
| 154 | `v6-assets/P2 SmartPins-220809_page04_img01.png` | Basic I/O Input Sampling | **REPLACE** with `\TESTBINATimingDiagram` |
| 351 | `v6-assets/smart-pins-master-trimmed.png` | Smart Pin Block Diagram | **KEEP** (complex colored diagram) |
| 388 | `v6-assets/P2 SmartPins-220809_page04_img01.png` | Smart Pin Configuration Flow | **REPLACE** with `\TESTBINATimingDiagram` (same image reused) |
| 533 | `v6-assets/P2 SmartPins-220809_page04_img02.png` | Pin Configuration Register Layout | **REPLACE** with `\TESTPTimingDiagram` |
| 921 | `v6-assets/P2 SmartPins-220809_mode00011_page13_img01.png` | DAC Output Characteristics | **REPLACE** with `\DACPWMPeriodDiagram` |
| 994 | `v6-assets/P2 SmartPins-220809_mode01000_page19_img01.png` | Pulse Output Timing | **KEEP** (oscilloscope screenshot) |
| 1063 | `v6-assets/P2 SmartPins-220809_mode00100_page15_img01.png` | NCO Frequency Generation | **REPLACE** with `\PulseWidthMeasurementDiagram` |
| 1136 | `v6-assets/P2 SmartPins-220809_mode01001_page21_img01.png` | NCO Duty Mode Operation | **REPLACE** with `\SawtoothPWMDiagram` |
| 1187 | `v6-assets/P2 SmartPins-220809_mode01000_page20_img01.png` | Transition Output Timing | **REPLACE** with `\TrianglePWMDiagram` |
| 1233 | `v6-assets/P2 SmartPins-220809_mode01001_page21_img01.png` | PWM Sawtooth Waveform | **REPLACE** with `\SawtoothPWMDiagram` (same image) |
| 1299 | `v6-assets/P2 SmartPins-220809_mode01000_page20_img01.png` | PWM Triangle Waveform | **REPLACE** with `\TrianglePWMDiagram` (same image) |
| 1348 | `assets/smps-timing-diagram.png` | SMPS Timing Diagram | **MISSING** - needs creation |
| 1407 | `v6-assets/P2 SmartPins-220809_mode01011_page23_img01.png` | Quadrature Encoder Signals | **REPLACE** with `\QuadEncoderDiagram` |
| 1476 | `v6-assets/P2 SmartPins-220809_mode10010_page31_img01.png` | Pulse Counting Timing | **REPLACE** with `\PeriodMeasurementDiagram` |
| 1530 | `assets/ab-encoder-timing.png` | A-B Encoder Timing | **MISSING** - could use `\QuadEncoderDiagram` |
| 1591 | `assets/comparator-operation.png` | Comparator Operation | **MISSING** - needs creation |
| 1655 | `v6-assets/P2 SmartPins-220809_mode10000_page29_img01.png` | Time Measurement Timing | **REPLACE** with `\HighLowCountingDiagram` |
| 1719 | `v6-assets/P2 SmartPins-220809_mode11100_page46_img01.png` | Sync Serial Transmit Timing | **REPLACE** with `\SyncSerialFallingDiagram` |
| 1743 | `assets/uart-frame-structure.png` | UART Frame Structure | **MISSING** - needs creation |
| 1822 | `assets/adc-operation-diagram.png` | ADC Operation Diagram | **MISSING** - needs creation |

## Summary

| Category | Count |
|----------|-------|
| **Can be replaced with TikZ** | 14 |
| **Keep as PNG** (oscilloscope/complex) | 2 |
| **Missing assets** (need creation) | 5 |

## Integration Approach

### Option A: Direct LaTeX Integration (Recommended for PDF Forge)

Replace markdown image syntax with raw LaTeX blocks:

**Before:**
```markdown
![Basic I/O Output Timing](v6-assets/P2 SmartPins-220809_page03_img01.png)
```

**After:**
```markdown
```{=latex}
\DRVHTimingDiagram
```
```

This requires:
1. Include `\usepackage{p2kb-smartpins-diagrams}` in the LaTeX template
2. Use pandoc's raw LaTeX passthrough (`{=latex}` blocks)

### Option B: Keep Images, Generate from TikZ

Generate PNG files from TikZ for inclusion:
1. Create standalone LaTeX files for each diagram
2. Compile to PDF, then convert to PNG
3. Replace images in v6-assets with TikZ-generated versions

This maintains markdown compatibility but adds build complexity.

### Option C: Hybrid Approach

1. For PDF generation via PDF Forge: Use Option A (raw LaTeX)
2. For web/preview: Keep PNG fallbacks

## Files to Modify

1. **LaTeX Template**: Add `\usepackage{p2kb-smartpins-diagrams}` to the document template
2. **Markdown Source**: Replace image references with raw LaTeX blocks
3. **Pandoc Args**: Ensure raw LaTeX passthrough is enabled

## Available TikZ Diagrams Not Currently Used

These diagrams from `p2kb-smartpins-diagrams.sty` are available but not yet referenced:

- `\TransitionCountingDiagram` (page16)
- `\NCOPWMTimingDiagram` (page17 img01)
- `\NCOPWMBlockDiagram` (page17 img02)
- `\ContinuousPeriodDiagram` (page32)
- `\TimeoutWatchdogDiagram` (page33)
- `\DualInputTimeDiagram` (page34)
- `\SyncSerialRisingDiagram` (page46 img02)

These may be useful for additional content or alternative explanations.

## Missing Diagrams to Create

The following diagrams are referenced but don't exist in either PNG or TikZ form:

1. `smps-timing-diagram.png` - SMPS switching timing
2. `comparator-operation.png` - Analog comparator operation
3. `uart-frame-structure.png` - UART frame with start/stop/data bits
4. `adc-operation-diagram.png` - ADC conversion process

These could be added to `p2kb-smartpins-diagrams.sty` as new TikZ commands.

## Next Steps

1. **Decision**: Choose integration approach (A, B, or C)
2. **Template Update**: Add package to LaTeX template
3. **Markdown Update**: Convert image references to chosen format
4. **Test**: Generate PDF to verify diagrams render correctly
5. **Missing Diagrams**: Create TikZ for missing assets if needed
