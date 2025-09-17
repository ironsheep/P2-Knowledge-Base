# V2 Image Placeholder Format Documentation

## Format Used
```
[DEBUG-WINDOW-IMAGE: description | dimensions | window-type | content-shown]
```

## Fields
1. **description**: Brief title describing what the image demonstrates
2. **dimensions**: Pixel dimensions (e.g., 256x256, 800x400)
3. **window-type**: Type of debug window (TERM, BITMAP, PLOT, SCOPE, LOGIC, SCOPE_XY, MULTI)
4. **content-shown**: Detailed description of what's visible in the screenshot

## Examples Added in V2

### Single Window Types
- `[DEBUG-WINDOW-IMAGE: First PLOT window example showing real-time data plotting | 256x256 | PLOT | Live sine wave being drawn point by point]`
- `[DEBUG-WINDOW-IMAGE: SCOPE_XY revealing motor glitch | 256x256 | SCOPE_XY | X-Y plot showing normal operation as tight cluster, with obvious outlier points revealing overcurrent spikes]`
- `[DEBUG-WINDOW-IMAGE: BITMAP revealing servo resonance | 400x200 | BITMAP | Graph showing green target line and red actual position with visible oscillations around 47Hz revealing mechanical resonance]`

### Multi-Window Layouts
- `[DEBUG-WINDOW-IMAGE: Professional multi-window debugging setup | 800x400 | MULTI | Three synchronized windows - terminal for serial monitoring, scope for analog signals, logic for digital signals]`
- `[DEBUG-WINDOW-IMAGE: Multi-COG parallel debugging | 900x200 | MULTI-TERM | Three color-coded terminal windows arranged horizontally, each showing independent COG output without interference]`

## Placement Strategy

### Pedagogically Valuable Locations
1. **First occurrence** of each window type (9 types total)
2. **Problem → Solution** sequences where debug window reveals the issue
3. **Multi-window coordination** examples showing synchronized debugging
4. **"Aha!" moments** where visual debugging solves complex problems
5. **Feature demonstrations** (triggers, cursors, measurements)

### Locations NOT Requiring Images
- Repeated similar examples
- Pure code explanations without visual output
- Setup/configuration code
- Theory sections

## Processing Instructions for Workspace

When converting V2 to final document:
1. Search for pattern: `[DEBUG-WINDOW-IMAGE:`
2. Convert to appropriate markdown/LaTeX format for PDF
3. Create placeholder box with dimensions specified
4. Include description text for image creation guidance
5. Mark as "NEEDS-SCREENSHOT" for production tracking

## Statistics
- Total placeholders added: 7 strategic locations
- Coverage: PLOT, SCOPE_XY, BITMAP, MULTI, MULTI-TERM, LOGIC, MULTI-PLOT
- Missing: FFT, SPECTRO, MIDI (not found in main examples)

## Novel Coordination Scenarios Identified

Beyond first window introductions, these advanced multi-window uses deserve images:

### 1. **PID Control Loop Tuning Dashboard** ✅ Added
- 4 synchronized PLOT windows showing setpoint/process, error, output, P/I/D terms
- Shows complete control loop dynamics in real-time
- Location: Line ~6745

### 2. **State Machine Visualization** (Could add)
- State diagram, timing chart, variables plot, event log
- Complete FSM visibility across multiple window types
- Location: Line ~6676

### 3. **Automotive Multi-Gauge Dashboard** (Could add)
- Multiple gauges using sprite layers
- Speed, RPM, temperature with warning zones
- Location: Line ~2807

### 4. **Waterfall Spectrum Display** (Could add)
- 3D visualization of frequency over time
- Shows signal evolution and patterns
- Location: Line ~4022

### 5. **I2C Multi-Channel Protocol Analysis** (Already added)
- 6-channel LOGIC showing three simultaneous I2C transactions
- Location: Previously added

### 6. **Interactive PID Parameter Adjustment** (Could add)
- Terminal for parameter input + multiple plots for response
- Shows before/after tuning effects
- Location: Line ~2362

## Next Steps
1. Copy V2 back to workspace
2. Apply preprocessing (div syntax, etc.)
3. Filter will convert these placeholders to visual elements
4. Production team can identify all needed screenshots