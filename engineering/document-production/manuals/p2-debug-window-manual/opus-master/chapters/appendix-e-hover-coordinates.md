# Appendix E: Mouse Hover Coordinate Display

## Discovery and Documentation Status

This powerful feature was discovered through examination of the Pascal source code implementation, not from the Spin2 documentation. The mouse hover coordinate display is an undocumented but fully functional capability present in all debug windows, transforming them into precision measurement tools without requiring any clicking or mode changes.

## Overview

Every P2 debug window implements sophisticated mouse tracking that displays context-specific coordinate information as you hover over the display. This feature operates continuously and automatically, requiring no configuration or activation. Simply moving your mouse over any debug window reveals precise position, time, frequency, or value information relevant to that window type.

## Window-Specific Hover Formats

### Complete Hover Display Reference Table

| Window Type | Hover Format | Description | Primary Use Cases |
|------------|--------------|-------------|-------------------|
| **TERM** | `<col>,<row>` | Character position | Cursor positioning, layout planning, text alignment |
| **BITMAP** | `<x>,<y>` | Pixel coordinates | Graphics debugging, sprite positioning, pixel-perfect alignment |
| **PLOT** | `<grid_x>,<grid_y>` | Grid coordinates | Data value reading, multi-channel comparison, trend analysis |
| **LOGIC** | `<time>,<sample>` | Time units and sample position | Timing measurements, protocol debugging, edge detection |
| **SCOPE** | `<x>,<y>` | Scaled coordinates | Voltage measurements, time measurements, waveform analysis |
| **SCOPE_XY** | `<x>,<y>` or `<r>,<θ>°` | Cartesian or polar | Phase measurements, Lissajous analysis, vector displays |
| **FFT** | `<freq_bin>,<amplitude>` | Frequency and level | Harmonic identification, noise analysis, spectrum peaks |
| **SPECTRO** | `<time>,<freq>` | Time and frequency | Waterfall analysis, frequency tracking, event correlation |
| **MIDI** | `<x>,<y>` | Display coordinates | Note timing, velocity analysis, event positioning |

## Detailed Window Descriptions

### Terminal Window (TERM)
- **Format**: `<column>,<row>`
- **Range**: Based on configured terminal size
- **Resolution**: Character-level precision
- **Applications**:
  - Planning screen layouts before coding
  - Debugging text positioning issues
  - Verifying cursor movement calculations
  - Checking alignment of formatted output

### Bitmap Window (BITMAP)
- **Format**: `<x>,<y>`
- **Range**: 0 to configured width/height minus 1
- **Resolution**: Single pixel precision
- **Applications**:
  - Sprite collision box verification
  - Graphics primitive endpoint checking
  - Pixel-perfect art alignment
  - Coordinate system debugging

### Plot Window (PLOT)
- **Format**: `<grid_x>,<grid_y>`
- **Special Feature**: Direction-aware (accounts for left/right, top/bottom plotting)
- **Resolution**: Grid unit precision
- **Applications**:
  - Reading exact data values from traces
  - Comparing values across multiple channels
  - Identifying peaks and valleys
  - Measuring change rates between points

### Logic Analyzer Window (LOGIC)
- **Format**: `<time_units>,<sample_position>`
- **Time Units**: Depends on sample rate and zoom level
- **Sample Position**: Absolute sample number in buffer
- **Applications**:
  - Measuring pulse widths (hover start and end)
  - Calculating frequencies from period measurements
  - Verifying setup and hold times
  - Protocol timing validation
  - Correlating events across channels

### Oscilloscope Window (SCOPE)
- **Format**: `<x_pixel>,<y_pixel>`
- **Scaling**: Accounts for voltage and time base settings
- **Resolution**: Pixel-level precision
- **Applications**:
  - Voltage measurements without cursors
  - Time interval measurements
  - Rise/fall time calculations
  - Peak-to-peak measurements
  - DC offset verification

### XY Oscilloscope Window (SCOPE_XY)
- **Dual Format Support**:
  - Cartesian: `<scaled_x>,<scaled_y>`
  - Polar: `<radius>,<angle>°`
- **Mode Selection**: Automatic based on display mode
- **Applications**:
  - Phase shift measurements (polar mode)
  - Lissajous pattern analysis
  - Vector magnitude and angle
  - Quadrature signal debugging
  - Complex impedance visualization

### FFT Window (FFT)
- **Format**: `<frequency_bin>,<amplitude_level>`
- **Frequency Bin**: Corresponds to actual frequency based on sample rate
- **Amplitude**: Scaled magnitude value
- **Applications**:
  - Identifying exact frequencies of peaks
  - Measuring harmonic relationships
  - Quantifying noise floor levels
  - Comparing spectral components
  - Finding spurious emissions

### Spectrogram Window (SPECTRO)
- **Format**: `<time>,<frequency>`
- **Time Axis**: Waterfall progression
- **Frequency Axis**: Same as FFT bins
- **Applications**:
  - Tracking frequency changes over time
  - Identifying intermittent signals
  - Correlating time-domain events with frequency content
  - Monitoring modulation patterns
  - Detecting frequency hopping

## Practical Measurement Techniques

### Timing Measurements Without Clicking

The hover coordinate system enables precise measurements without modifying the display:

1. **Pulse Width Measurement** (LOGIC window):
   - Hover over rising edge, note time value
   - Hover over falling edge, note time value
   - Subtract for pulse width
   - No need for cursors or markers

2. **Frequency Identification** (FFT window):
   - Hover over spectral peak
   - Read exact frequency bin
   - Calculate actual frequency from bin number and sample rate
   - Identify harmonics by their exact relationships

3. **Phase Measurement** (SCOPE_XY in polar mode):
   - Hover over Lissajous pattern points
   - Read angle directly in degrees
   - Compare multiple points for phase relationships
   - No trigonometry required

### Multi-Point Comparison

Since hovering doesn't change the display, you can quickly sample multiple points:

```spin2
' Example: Using hover to compare multiple channels in PLOT
' User hovers over same X position on different traces
' Reads Y values to compare channel amplitudes
' No clicking required, display remains stable
```

### Data Exploration Workflow

1. **Initial Survey**: Move mouse across display to get value ranges
2. **Identify Features**: Hover over peaks, edges, anomalies
3. **Precise Measurement**: Note exact coordinates at points of interest
4. **Correlation**: Compare coordinates across different windows
5. **Documentation**: Record measurements without display artifacts

## Advantages Over Traditional Cursors

### Non-Invasive Measurement
- Display never changes during measurement
- No cursor lines obscuring data
- No accidental clicks changing settings
- Multiple quick measurements without mode changes

### Speed and Efficiency
- Instant readout at any position
- No cursor positioning time
- No menu navigation for measurement modes
- Rapid comparison across many points

### Precision Without Complexity
- Exact values without interpolation
- No cursor snap or quantization issues
- Full resolution of underlying data
- No measurement mode configuration

## Integration with P2 Development

### Debugging Workflows

The hover coordinate feature integrates seamlessly with P2 debugging:

1. **Signal Integrity Analysis**:
   - Hover over SCOPE traces to verify voltage levels
   - Check rise times and overshoot
   - Measure settling times
   - Verify DC bias points

2. **Digital Protocol Debugging**:
   - Use LOGIC hover to measure bit periods
   - Verify inter-byte timing
   - Check setup/hold relationships
   - Measure clock duty cycles

3. **Algorithm Verification**:
   - PLOT hover for exact algorithm outputs
   - FFT hover for frequency response validation
   - SCOPE_XY polar mode for phase-locked loop debugging
   - SPECTRO hover for time-frequency correlation

### Performance Optimization

The hover system helps optimize P2 code:

- Measure actual timing versus theoretical
- Identify unexpected delays or glitches
- Verify CORDIC calculation results
- Check Smart Pin timing configurations

## Compensating for Missing Features

The hover coordinate system partially compensates for the lack of:

### Automatic Measurements
While there are no automatic measurement commands, hover provides:
- Manual but precise measurements
- No configuration complexity
- Immediate results
- Full control over measurement points

### Cursor Systems
Traditional cursors are replaced by:
- Infinite "virtual cursors" via hover
- No cursor management overhead
- No display clutter
- Faster workflow for multiple measurements

### Protocol Decoders
Without automatic protocol decoding, hover enables:
- Manual bit period measurement
- Transition timing verification
- Pulse width checking
- Inter-frame gap measurement

## Best Practices

### Effective Hover Usage

1. **Steady Hand**: Hold mouse still for accurate reading
2. **Mental Notes**: Remember key coordinates for comparison
3. **Systematic Scanning**: Move methodically across features
4. **Reference Points**: Use grid lines or edges as reference
5. **Zoom Appropriately**: Adjust zoom for measurement precision

### Window Layout for Hover

Arrange windows to facilitate hover measurement:
- Place related windows adjacently
- Align time axes for correlation
- Use consistent scaling where possible
- Keep measurement areas unobstructed

### Documentation of Measurements

When recording hover measurements:
- Note window type and settings
- Record exact coordinate format
- Include scaling factors
- Document reference points

## Examples and Use Cases

### Example 1: Measuring SPI Clock Frequency

```spin2
PUB measure_spi_clock() | period
  ' Display SPI signals in LOGIC window
  debug(`LOGIC MyLogic TITLE "SPI Clock Measurement")
  
  ' User workflow:
  ' 1. Hover over clock rising edge #1: read time as 1000
  ' 2. Hover over clock rising edge #2: read time as 1025  
  ' 3. Period = 25 time units
  ' 4. Calculate frequency from time base
  ' No cursors needed, no clicks required
```

### Example 2: FFT Harmonic Analysis

```spin2
PUB identify_harmonics() | fundamental
  ' Display spectrum in FFT window
  debug(`FFT MyFFT TITLE "Harmonic Analysis")
  
  ' User workflow:
  ' 1. Hover over fundamental peak: read bin 50
  ' 2. Hover over next peak: read bin 100 (2x harmonic)
  ' 3. Hover over third peak: read bin 150 (3x harmonic)
  ' Exact harmonic relationships confirmed instantly
```

### Example 3: Phase Shift Measurement

```spin2
PUB measure_phase_shift()
  ' Display Lissajous pattern in SCOPE_XY with polar mode
  debug(`SCOPE_XY MyScope TITLE "Phase Measurement" POLAR)
  
  ' User workflow:
  ' 1. Hover over pattern maximum: read angle as 45°
  ' 2. Phase shift directly displayed, no calculation
  ' 3. Track phase changes by hovering during operation
```

## Technical Implementation Notes

### Source Discovery
This feature was identified through examination of the Pascal source code implementation files, specifically in the mouse event handling routines. The coordinate calculation and display formatting code is present for all window types, though not documented in the Spin2 language reference.

### Consistency Across Windows
Every debug window type implements hover coordinates, suggesting this was a fundamental design decision. The implementation is consistent and reliable across all window types, with appropriate formatting for each context.

### No Configuration Required
The hover coordinate display is always active and requires no DEBUG commands to enable. This makes it immediately available to all users, even those unaware of its existence.

## Conclusion

The mouse hover coordinate display is one of the P2 debug system's most powerful yet undocumented features. It transforms every debug window into a precision measurement instrument without the complexity of traditional cursor systems or measurement modes. By simply moving the mouse, developers gain immediate access to exact values, timings, and positions across all their debug displays.

This feature is particularly valuable because it:
- Requires no setup or configuration
- Works consistently across all window types  
- Provides context-appropriate formatting
- Enables non-invasive measurements
- Maintains display stability during measurement
- Offers unlimited measurement points
- Operates at full display resolution

Master the hover coordinate system, and you'll find debugging and measurement tasks become significantly faster and more precise. While it doesn't replace all the features of professional instruments, it provides an elegant and efficient solution for the vast majority of embedded development measurement needs.

## See Also

- Individual window study documents for window-specific hover details
- Chapter 5: PC Input Integration for mouse command documentation
- Window-specific chapters (7-14) for practical hover usage examples
- Gap analysis documents acknowledging this as an undocumented feature