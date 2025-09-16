# Mouse Hover Coordinate Reference

## Status: Undocumented But Powerful Feature

**Discovery Source**: Pascal source code examination (not in Spin2 documentation)
**Availability**: All debug windows
**Configuration**: None required - always active

## Complete Hover Coordinate Format Reference

| Window | Format | Units | Description | Use Cases |
|--------|--------|-------|-------------|-----------|
| **TERM** | `<col>,<row>` | Characters | Column and row position (0-based) | Text layout, cursor positioning, alignment verification |
| **BITMAP** | `<x>,<y>` | Pixels | Pixel coordinates from origin | Sprite positioning, collision detection, pixel art |
| **PLOT** | `<grid_x>,<grid_y>` | Grid units | Direction-aware grid position | Data value reading, trace comparison, trend analysis |
| **LOGIC** | `<time>,<sample>` | Time units, samples | Time position and sample index | Pulse width, frequency, protocol timing |
| **SCOPE** | `<x>,<y>` | Scaled units | Voltage and time coordinates | Amplitude measurement, timing, waveform analysis |
| **SCOPE_XY** | `<x>,<y>` or `<r>,<θ>°` | Units or polar | Cartesian or polar coordinates | Phase measurement, Lissajous patterns, vectors |
| **FFT** | `<freq_bin>,<amplitude>` | Bin, magnitude | Frequency bin and level | Harmonic identification, noise floor, peaks |
| **SPECTRO** | `<time>,<freq>` | Time, frequency | Waterfall position | Time-frequency correlation, modulation tracking |
| **MIDI** | `<x>,<y>` | Display units | Display coordinates | Note timing, velocity, MIDI events |

## Detailed Window Behaviors

### Terminal Window (TERM)
- **Zero-Based**: Coordinates start at (0,0) in top-left
- **Range**: Limited by configured terminal size
- **Precision**: Character-level granularity
- **Updates**: Real-time as mouse moves

### Bitmap Window (BITMAP)  
- **Origin**: Top-left is (0,0)
- **Range**: 0 to width-1, 0 to height-1
- **Precision**: Single pixel accuracy
- **Scaling**: Accounts for window zoom level

### Plot Window (PLOT)
- **Direction Aware**: Handles left/right, top/bottom plotting
- **Grid Based**: Snaps to grid intersections
- **Multi-Trace**: Y-value for trace under cursor
- **Scaling**: Follows configured ranges

### Logic Analyzer (LOGIC)
- **Dual Information**: Both time and sample position
- **Time Units**: Depends on timebase setting
- **Sample Index**: Absolute position in buffer
- **Zoom Aware**: Time units scale with zoom

### Oscilloscope (SCOPE)
- **Scaled Values**: Real voltage and time units
- **Pixel Mapping**: Direct screen coordinates
- **Graticule Aware**: Aligns with grid divisions
- **Trigger Point**: Relative to trigger position

### XY Oscilloscope (SCOPE_XY)
- **Mode Switching**: Automatic cartesian/polar
- **Polar Format**: Radius and angle in degrees
- **Cartesian**: Scaled X and Y values
- **Center Origin**: (0,0) at screen center

### FFT Window
- **Frequency Bins**: Maps to actual frequencies
- **Calculation**: `freq = bin * sample_rate / fft_size`
- **Amplitude**: Logarithmic or linear scale
- **Peak Detection**: Hover identifies exact peaks

### Spectrogram (SPECTRO)
- **Time Axis**: Waterfall progression time
- **Frequency Axis**: Same as FFT bins
- **Color Mapping**: Intensity at hover point
- **History**: Shows time evolution

## Hover-Based Workflows

### 1. Timing Measurement Workflow
```
LOGIC Window Process:
1. Hover over signal rising edge → Note time T1
2. Hover over signal falling edge → Note time T2  
3. Pulse width = T2 - T1
4. No cursors needed, no display changes
```

### 2. Frequency Identification Workflow
```
FFT Window Process:
1. Hover over spectral peak → Read frequency bin
2. Calculate: freq = bin * fs / N
3. Hover over harmonics → Verify integer multiples
4. Identify spurious frequencies instantly
```

### 3. Phase Measurement Workflow
```
SCOPE_XY Polar Mode Process:
1. Display Lissajous pattern
2. Hover over pattern extremes → Read angle directly
3. Phase shift = angle difference
4. Track phase changes in real-time
```

### 4. Multi-Channel Comparison
```
PLOT Window Process:
1. Hover at specific X position
2. Read Y value for trace 1
3. Move vertically to trace 2
4. Read Y value for comparison
5. Calculate difference or ratio
```

## Measurement Techniques

### Non-Invasive Measurements
- **No Click Required**: Just hover to read
- **Display Unchanged**: No cursors added
- **Multiple Points**: Sample many quickly
- **Clean View**: No measurement overlays

### Precision Without Complexity
- **Direct Reading**: No interpolation needed
- **Full Resolution**: Pixel-accurate values
- **No Mode Changes**: Always available
- **No Configuration**: Works immediately

### Speed Advantages
- **Instant**: No cursor positioning time
- **Continuous**: Track changes while hovering
- **Multiple**: Check many points rapidly
- **Comparative**: Quick A/B measurements

## Compensating for Missing Features

### Replaces Automatic Measurements
While no automatic measurement commands exist, hover provides:
- Manual precision measurements
- No setup complexity
- User-controlled measurement points
- Instant results

### Replaces Traditional Cursors
Instead of cursor systems:
- Unlimited virtual cursors
- No cursor management
- No display clutter
- Faster workflow

### Replaces Protocol Decoders
For protocol analysis:
- Measure bit periods manually
- Check timing relationships
- Verify pulse widths
- Measure gaps and delays

## Best Practices

### Effective Usage
1. **Steady Positioning**: Hold mouse still for stable reading
2. **Mental Tracking**: Remember values for comparison
3. **Systematic Approach**: Scan methodically across features
4. **Reference Points**: Use grid/graticule as guides
5. **Appropriate Zoom**: Adjust for measurement precision

### Window Arrangement
- Position related windows together
- Align time axes for correlation
- Use consistent scaling
- Keep measurement areas visible

### Value Recording
- Note exact coordinate format
- Record scaling factors
- Document window settings
- Track measurement conditions

## Implementation Details

### Technical Architecture
- **Event System**: Mouse move events trigger updates
- **Coordinate Transform**: Screen to data mapping
- **Format Selection**: Window-specific formatting
- **Display Update**: Immediate coordinate display

### Consistency Design
- Every window type implements hover
- Uniform event handling
- Consistent update rate
- No performance impact

### No User Configuration
- Always enabled
- No DEBUG commands needed
- No settings to adjust
- Works out-of-box

## Examples

### Example 1: SPI Clock Period
```spin2
' Measuring SPI clock period with LOGIC hover
' 1. Display SPI clock in LOGIC window
' 2. Hover over rising edge: time = 1000  
' 3. Hover over next rising edge: time = 1025
' 4. Period = 25 time units
' 5. Frequency = 1 / period
```

### Example 2: Voltage Measurement
```spin2
' Measuring signal amplitude with SCOPE hover
' 1. Display waveform in SCOPE window
' 2. Hover over peak: read Y value = 3.3
' 3. Hover over trough: read Y value = 0.2
' 4. Peak-to-peak = 3.3 - 0.2 = 3.1V
```

### Example 3: Harmonic Analysis
```spin2
' Identifying harmonics with FFT hover
' 1. Display spectrum in FFT window
' 2. Hover over fundamental: bin 50
' 3. Hover over next peak: bin 100 (2nd harmonic)
' 4. Hover over third peak: bin 150 (3rd harmonic)
' 5. Confirm harmonic relationship
```

## Cross-Documentation Updates Required

This reference document ensures consistency across all documentation. The following documents should reference this master source:

1. **Window Study Files**: Each comprehensive study should link here
2. **Debug Manual**: Chapters 5, 7-14 should reference this
3. **Gap Analysis**: Should note this as undocumented discovery
4. **Creation Guide**: Should emphasize documenting such discoveries

## Conclusion

The mouse hover coordinate display is an undocumented gem in the P2 debug system. It transforms every window into a measurement tool without the complexity of traditional instruments. This feature provides:

- **Universal availability** across all windows
- **Zero configuration** requirement  
- **Non-invasive** measurement capability
- **Professional-grade** precision
- **Instant** results
- **Unlimited** measurement points

Master this feature to dramatically improve debugging efficiency and measurement precision. While undocumented in Spin2 reference, it's fully functional and reliable across all debug window types.

---

**Discovery Date**: 2025-09-14
**Source**: Pascal implementation examination
**Status**: Undocumented but fully functional
**Recommendation**: Essential skill for P2 debug mastery