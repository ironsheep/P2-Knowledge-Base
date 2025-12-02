# Smart Pins TikZ Diagrams Reference

This document maps the original PNG assets to their TikZ diagram replacements.

## Package Usage

Include in your LaTeX template:
```latex
\usepackage{p2kb-smartpins-diagrams}
```

Then use diagram commands in your document:
```latex
\DRVHTimingDiagram
```

## Diagram Mapping

### Timing Diagrams (Instruction/Pin Behavior)

| Original Image | TikZ Command | Description |
|---------------|--------------|-------------|
| `page03_img01.png` | `\DRVHTimingDiagram` | DRVH #0 instruction timing showing System Clock, DIRA, OUTA, and instruction execution |
| `page04_img01.png` | `\TESTBINATimingDiagram` | TESTB INA, #0 instruction timing with register transfers and ALU operation |
| `page04_img02.png` | `\TESTPTimingDiagram` | TESTP #0 instruction timing (simplified pin test) |

### PWM/DAC Diagrams

| Original Image | TikZ Command | Description |
|---------------|--------------|-------------|
| `page13_img01.png` | `\DACPWMPeriodDiagram` | Mode %00011 - DAC input levels (240/239) and PWM period timing (256 system-clock periods) |
| `page15_img01.png` | `\PulseWidthMeasurementDiagram` | Mode %00100 - Pulse width measurement showing X[15:0] and X[31:16] bit fields, IN Flag |
| `page16_img01.png` | `\NCOFrequencyDiagram` | Mode %00101 - NCO Frequency transition counting (Y[31:0] = 12 transitions), X[15:0] period |

### NCO Duty Mode Diagrams (Mode %00110)

| Original Image | TikZ Command | Description |
|---------------|--------------|-------------|
| `page17_img01.png` | `\NCODutyTimingDiagram` | Mode %00110 - Multi-signal timing: IN Flag, Output, Base Period, System Clock with Z[31:16] values |
| `page17_img02.png` | `\NCODutyBlockDiagram` | Mode %00110 - NCO Duty datapath block diagram: System Clock → Divider → Adder → Z register |

### Triangle/Sawtooth PWM Diagrams

| Original Image | TikZ Command | Description |
|---------------|--------------|-------------|
| `page20_img01.png` | `\TrianglePWMDiagram` | Triangle wave PWM with counter steps, frame/PWM periods, IN signal |
| `page21_img01.png` | `\SawtoothPWMDiagram` | Sawtooth wave PWM variant |

### Quadrature Encoder

| Original Image | TikZ Command | Description |
|---------------|--------------|-------------|
| `page23_img01.png` | `\QuadEncoderDiagram` | Quadrature encoder circuit schematic + CW/CCW timing waveforms |

### Counting/Measurement Diagrams

| Original Image | TikZ Command | Description |
|---------------|--------------|-------------|
| `page29_img01.png` | `\HighLowCountingDiagram` | High/low state counting with Q/R/S regions, C/Z flag outputs |
| `page31_img01.png` | `\PeriodMeasurementDiagram` | Period measurement (9 cycles) with system-clock count output |
| `page32_img01.png` | `\ContinuousPeriodDiagram` | Continuous period measurement (two 6-cycle measurements) |
| `page33_img01.png` | `\TimeoutWatchdogDiagram` | Timeout/watchdog with clock reset on each input pulse |
| `page34_img01.png` | `\DualInputTimeDiagram` | Dual input (A/B) time measurement, Q+R calculation |

### Serial Data Diagrams

| Original Image | TikZ Command | Description |
|---------------|--------------|-------------|
| `page46_img01.png` | `\SyncSerialFallingDiagram` | Synchronous serial receive, sampling on falling clock edge, LSB→MSB |
| `page46_img02.png` | `\SyncSerialRisingDiagram` | Synchronous serial receive, sampling on rising clock edge, LSB→MSB |

## Images NOT Converted (Keep as PNG)

These are oscilloscope screenshots or complex diagrams that should remain as images:

| Image | Reason |
|-------|--------|
| `page19_img01.png` | Oscilloscope screenshot (GW Instek) with UI elements |
| `page52_img01.png` | Oscilloscope waveform capture (yellow trace) |
| `page52_img02.png` | Oscilloscope waveform capture (yellow trace) |
| `smart-pins-master-trimmed.png` | Complex colored block diagram (Custom I/O Pad Ring + Synthesized Core Logic) - could be recreated but very complex (~200+ lines TikZ) |

## Color Definitions

The package defines these colors for consistent styling:

```latex
\definecolor{sp-border}{HTML}{000000}      % Black borders
\definecolor{sp-text}{HTML}{000000}        % Black text
\definecolor{sp-annotation}{HTML}{0000AA}  % Blue annotations
\definecolor{sp-block-fill}{HTML}{FFFFFF}  % White block fill
\definecolor{sp-block-border}{HTML}{000000} % Black block borders
```

## Common Styles

The package provides these TikZ styles:

- `sp-signal` - Thick black lines for signal waveforms
- `sp-clock` - Clock signal styling
- `sp-annotation` - Small text annotations
- `sp-label` - Labels on left side of diagrams
- `sp-block` - Block diagram boxes
- `sp-arrow` - Directional arrows
- `sp-dim` - Dimension/measurement lines

## Notes

1. All diagrams are designed to match the visual style of the original PNG images
2. Diagrams use monochrome styling (black lines on white) like the originals
3. The annotation color (blue) is used sparingly for emphasis, matching originals
4. Each diagram is wrapped in `\begin{center}...\end{center}` for automatic centering
5. Diagrams scale appropriately for typical LaTeX document widths
