# Chapter 8: Data Visualization Mastery - PLOT Window

*Strip charts. Scatter plots. Real-time graphs. The PLOT window transforms raw numbers into visual insight, revealing patterns invisible in text. Where terminal output shows trees, PLOT shows the forest—trends, anomalies, correlations, and behaviors that emerge only through visualization. This is where debugging becomes data science.*

## The Visualization Advantage

Numbers lie through precision. When you see "2047, 2048, 2049, 2048, 2047", your brain registers stability. But plot those same values over time and you might discover a 100Hz oscillation, a slow drift, or periodic spikes that text obscures. The PLOT window doesn't just display data—it reveals truth through patterns.

Consider debugging a temperature control system. Terminal output shows temperatures within range. But plot those readings and you see oscillation around the setpoint, increasing amplitude suggesting instability, or a deadband that's too wide. The same data, transformed by visualization, tells a completely different story.

## PLOT Window Architecture

The PLOT window operates as a real-time graphing system with professional features:

```spin2
CON
  ' PLOT window capabilities
  MAX_POINTS = 16384        ' Maximum points per trace
  MAX_TRACES = 8            ' Simultaneous traces
  UPDATE_MODES = 4          ' Strip, Scope, XY, Polar
  
VAR
  long plot_buffer[1024]
  long x_position
  byte auto_scale
  
PUB plot_fundamentals()
  ' Create a PLOT window with all options
  DEBUG(`PLOT MyData SIZE 800 400 POS 100 100)
  DEBUG(`MyData GRID 10 10)                      ' Grid divisions
  DEBUG(`MyData RANGE -1000 1000)                ' Y-axis range
  DEBUG(`MyData TRACES 3)                        ' Multiple traces
  DEBUG(`MyData COLORS RED GREEN BLUE)           ' Trace colors
  DEBUG(`MyData STYLE LINES)                     ' Line plot
  DEBUG(`MyData TITLE "System Performance")      ' Window title
  
  ' Send data multiple ways
  single_point_plotting()
  array_plotting()
  continuous_streaming()
  xy_plotting()
```

## Plotting Modes and Techniques

### Strip Chart Mode - Time Series Data

The most common mode, perfect for continuous monitoring:

```spin2
PUB strip_chart_example() | value, time_stamp
  ' Configure as strip chart
  DEBUG(`PLOT Strip SIZE 800 300)
  DEBUG(`Strip MODE STRIP)
  DEBUG(`Strip POINTS 500)  ' Visible history
  
  repeat
    ' Single value advances X automatically
    value := read_sensor()
    DEBUG(`Strip `(value))
    
    ' Auto-scrolling when edge reached
    waitms(100)  ' 10Hz update rate

PUB multi_channel_strip() | ch1, ch2, ch3
  ' Multiple traces on same timeline
  DEBUG(`PLOT Multi TRACES 3)
  
  repeat
    ch1 := read_adc(0)
    ch2 := read_adc(1) 
    ch3 := read_adc(2)
    
    ' All three update together
    DEBUG(`Multi `(ch1, ch2, ch3))
    waitms(50)
```

### Oscilloscope Mode - Triggered Capture

For repetitive signals, triggered display:

```spin2
PUB oscilloscope_mode() | trigger_level, samples[512]
  ' Configure scope mode
  DEBUG(`PLOT Scope MODE SCOPE)
  DEBUG(`Scope POINTS 512)
  DEBUG(`Scope TRIGGER 2048 RISING)
  
  trigger_level := 2048
  
  repeat
    ' Wait for trigger condition
    waitpeq(trigger_level, ADC_PIN, 0)
    
    ' Rapid capture
    repeat i from 0 to 511
      samples[i] := read_adc_fast()
    
    ' Display complete waveform
    DEBUG(`Scope PACK16 512 @samples)
    
    ' No scroll - overwrites each time

PUB auto_trigger_scope() | samples[256], timeout
  ' Scope with auto-trigger fallback
  
  repeat
    timeout := cnt + 80_000_000  ' 1 second timeout
    
    ' Try to catch trigger
    repeat while (read_adc() < 2048) and (cnt < timeout)
    
    if cnt >= timeout
      DEBUG(`TERM "Auto-triggered")
    
    ' Capture regardless
    repeat i from 0 to 255
      samples[i] := read_adc()
      waitus(10)
    
    DEBUG(`Scope PACK16 256 @samples)
```

### XY Mode - Phase and Correlation

Visualize relationships between signals:

```spin2
PUB xy_mode_example() | x, y, angle
  ' Configure XY mode
  DEBUG(`PLOT XY MODE XY)
  DEBUG(`XY RANGE -1000 1000 -1000 1000)  ' X and Y ranges
  DEBUG(`XY POINTS 1000)  ' Trail length
  DEBUG(`XY PERSIST 500)  ' Persistence ms
  
  ' Lissajous pattern
  repeat angle from 0 to 359
    x := 500 * sin(angle)
    y := 500 * sin(angle + 90)  ' 90-degree phase
    
    DEBUG(`XY `(x, y))
    waitms(10)

PUB correlation_plot() | input, output
  ' Show input vs output relationship
  
  repeat
    input := read_input()
    output := read_output()
    
    ' Direct correlation visible
    DEBUG(`XY `(input, output))
    
    ' Linear = straight line
    ' Hysteresis = loop
    ' Nonlinear = curve
```

### Polar Mode - Angular Data

Perfect for rotating systems or directional data:

```spin2
PUB polar_plot() | angle, radius
  ' Configure polar mode
  DEBUG(`PLOT Polar MODE POLAR)
  DEBUG(`Polar RANGE 0 1000)  ' Radius range
  
  repeat angle from 0 to 359
    ' Radar sweep pattern
    radius := measure_distance(angle)
    
    ' Angle in degrees, radius in units
    DEBUG(`Polar `(angle, radius))
    
    waitms(10)

PUB antenna_pattern() | bearing, signal_strength
  ' Plot antenna radiation pattern
  
  repeat bearing from 0 to 359 step 5
    rotate_antenna(bearing)
    signal_strength := measure_rssi()
    
    DEBUG(`Polar `(bearing, signal_strength))
  
  ' Creates rose diagram of coverage
```

## Advanced Visualization Techniques

### Auto-Scaling and Ranging

Adapt display to data dynamically:

```spin2
VAR
  long min_seen, max_seen
  long scale_factor

PUB auto_scale_plot() | value, margin
  min_seen := POSX
  max_seen := NEGX
  margin := 10  ' 10% margin
  
  repeat
    value := read_sensor()
    
    ' Track extremes
    if value < min_seen
      min_seen := value
    if value > max_seen
      max_seen := value
    
    ' Update range with margin
    range := max_seen - min_seen
    if range > 0
      DEBUG(`PLOT Auto RANGE `(
        min_seen - (range * margin / 100),
        max_seen + (range * margin / 100)))
    
    DEBUG(`Auto `(value))
    waitms(100)

PUB logarithmic_scaling() | value, log_value
  ' Logarithmic scale for wide dynamic range
  
  repeat
    value := read_sensor()
    
    if value > 0
      ' Convert to log scale (base 10)
      log_value := log10(value) * 100
    else
      log_value := 0
    
    DEBUG(`PLOT LogScale `(log_value))
```

### Statistical Overlays

Add statistical information to visualizations:

```spin2
VAR
  long sample_buffer[1000]
  long sample_index
  long mean, std_dev

PUB statistical_plot() | value, upper_band, lower_band
  ' Initialize
  longfill(@sample_buffer, 0, 1000)
  
  repeat
    value := read_sensor()
    
    ' Update circular buffer
    sample_buffer[sample_index] := value
    sample_index := (sample_index + 1) // 1000
    
    ' Calculate statistics
    calculate_stats(@sample_buffer, 1000, @mean, @std_dev)
    
    ' Plot value with statistical bands
    upper_band := mean + (2 * std_dev)
    lower_band := mean - (2 * std_dev)
    
    ' Three traces: value, upper, lower
    DEBUG(`PLOT Stats TRACES 3)
    DEBUG(`Stats `(value, upper_band, lower_band))

PRI calculate_stats(buffer, count, mean_ptr, std_ptr) | sum, sum_sq, i
  ' Calculate mean
  sum := 0
  repeat i from 0 to count-1
    sum += long[buffer][i]
  long[mean_ptr] := sum / count
  
  ' Calculate standard deviation
  sum_sq := 0
  repeat i from 0 to count-1
    diff := long[buffer][i] - long[mean_ptr]
    sum_sq += diff * diff
  long[std_ptr] := sqrt(sum_sq / count)
```

### Waterfall Displays

Show signal evolution over time:

```spin2
VAR
  long waterfall_buffer[100][256]  ' 100 time slices, 256 points each
  byte waterfall_index

PUB waterfall_display() | spectrum[256]
  ' 3D visualization using color intensity
  
  repeat
    ' Get current spectrum
    calculate_fft(@spectrum)
    
    ' Add to waterfall buffer
    longmove(@waterfall_buffer[waterfall_index], @spectrum, 256)
    waterfall_index := (waterfall_index + 1) // 100
    
    ' Display as intensity map
    display_waterfall()
    
PRI display_waterfall() | x, y, intensity
  ' Convert to color-coded display
  DEBUG(`PLOT Waterfall MODE INTENSITY)
  
  repeat y from 0 to 99
    repeat x from 0 to 255
      intensity := waterfall_buffer[y][x]
      
      ' Map intensity to color
      color := intensity_to_color(intensity)
      DEBUG(`Waterfall PIXEL `(x, y, color))
```

### Multi-Pane Layouts

Create dashboard-style displays:

```spin2
PUB four_pane_dashboard()
  ' Create four synchronized plots
  DEBUG(`PLOT Pane1 SIZE 400 200 POS 0 0)
  DEBUG(`PLOT Pane2 SIZE 400 200 POS 400 0)
  DEBUG(`PLOT Pane3 SIZE 400 200 POS 0 200)
  DEBUG(`PLOT Pane4 SIZE 400 200 POS 400 200)
  
  repeat
    ' Update all panes
    DEBUG(`Pane1 `(read_temperature()))
    DEBUG(`Pane2 `(read_pressure()))
    DEBUG(`Pane3 `(read_flow()))
    DEBUG(`Pane4 `(read_voltage()))
    
    waitms(250)  ' 4Hz update

PUB stacked_plots() | i
  ' Vertically stacked with shared X-axis
  
  repeat i from 1 to 4
    y_pos := (i-1) * 100
    DEBUG(`PLOT Stack#i SIZE 800 100 POS 0 `(y_pos))
    DEBUG(`Stack#i GRID 10 5)
  
  repeat
    ' Synchronized time axis
    time_stamp := cnt / 80_000
    
    DEBUG(`Stack1 `(time_stamp, sensor1()))
    DEBUG(`Stack2 `(time_stamp, sensor2()))
    DEBUG(`Stack3 `(time_stamp, sensor3()))
    DEBUG(`Stack4 `(time_stamp, sensor4()))
```

## Real-Time Performance Monitoring

### System Performance Dashboard

```spin2
VAR
  long cpu_usage[8]
  long memory_free
  long task_times[16]

PUB performance_monitor()
  ' Configure performance plots
  DEBUG(`PLOT CPU SIZE 400 200 POS 0 0)
  DEBUG(`CPU TRACES 8 STYLE STACKED)
  DEBUG(`CPU TITLE "Cog Usage %")
  
  DEBUG(`PLOT Memory SIZE 400 200 POS 400 0)
  DEBUG(`Memory TITLE "Memory Usage")
  
  DEBUG(`PLOT Tasks SIZE 800 200 POS 0 200)
  DEBUG(`Tasks TRACES 16 STYLE BARS)
  DEBUG(`Tasks TITLE "Task Execution Times")
  
  repeat
    ' Update CPU usage for all cogs
    repeat cog from 0 to 7
      cpu_usage[cog] := measure_cog_usage(cog)
    
    DEBUG(`CPU PACK8 8 @cpu_usage)
    
    ' Update memory
    memory_free := clkfreq - chipused()
    DEBUG(`Memory `(memory_free))
    
    ' Update task times
    measure_all_tasks(@task_times)
    DEBUG(`Tasks PACK16 16 @task_times)
    
    waitms(1000)  ' 1Hz dashboard update
```

### Signal Quality Metrics

```spin2
PUB signal_quality_monitor() | snr, thd, amplitude, phase_noise
  ' Multi-metric signal analysis
  
  DEBUG(`PLOT Quality SIZE 800 400)
  DEBUG(`Quality TRACES 4)
  DEBUG(`Quality LABELS "SNR" "THD" "Amplitude" "Phase")
  
  repeat
    ' Measure signal quality metrics
    snr := calculate_snr()
    thd := calculate_thd()
    amplitude := measure_amplitude()
    phase_noise := measure_phase_noise()
    
    ' Normalize to percentage
    snr_pct := snr * 100 / 60  ' 60dB = 100%
    thd_pct := 100 - thd        ' Lower is better
    amp_pct := amplitude * 100 / 4096
    phase_pct := 100 - (phase_noise * 10)
    
    DEBUG(`Quality `(snr_pct, thd_pct, amp_pct, phase_pct))
    
    ' Color code based on quality
    if snr < 20
      DEBUG(`Quality COLOR 1 RED)  ' Poor signal
    elseif snr < 40
      DEBUG(`Quality COLOR 1 YELLOW)  ' Marginal
    else
      DEBUG(`Quality COLOR 1 GREEN)  ' Good
```

## Data Export and Logging

### CSV Export for Analysis

```spin2
VAR
  long log_buffer[10000]
  long log_index
  byte export_flag

PUB data_logger_with_export()
  repeat
    ' Continuous logging
    log_buffer[log_index++] := read_sensor()
    
    ' Plot real-time
    DEBUG(`PLOT Logger `(log_buffer[log_index-1]))
    
    if log_index => 10000 or export_flag
      export_to_csv()
      log_index := 0
      export_flag := FALSE
    
    waitms(10)

PRI export_to_csv() | i
  ' Export data in CSV format
  DEBUG(`TERM "timestamp,value")
  
  repeat i from 0 to log_index-1
    DEBUG(`TERM `(i * 10) "," `(log_buffer[i]))
  
  DEBUG(`TERM "Export complete: " `(log_index) " samples")
```

## Troubleshooting Visualization Issues

### Common Problems and Solutions

**Problem**: Plot updates too slowly
**Solution**: Use packed data formats
```spin2
' Slow: Individual points
repeat i from 0 to 999
  DEBUG(`PLOT Data `(array[i]))

' Fast: Packed array
DEBUG(`PLOT Data PACK16 1000 @array)
```

**Problem**: Traces overlap confusingly
**Solution**: Use transparency or offset
```spin2
' Add transparency
DEBUG(`PLOT Multi ALPHA 128)  ' 50% transparent

' Or offset traces
DEBUG(`Multi OFFSET 0 100 200)  ' Vertical offset per trace
```

**Problem**: Missing data points
**Solution**: Check buffer sizes and timing
```spin2
' Ensure buffer doesn't overflow
if (write_ptr + 1) // BUFFER_SIZE <> read_ptr
  buffer[write_ptr] := new_data
  write_ptr := (write_ptr + 1) // BUFFER_SIZE
else
  DEBUG(`TERM "Buffer overflow!")
```

## Chapter Summary

The PLOT window transforms the P2 from a microcontroller into a data analysis platform. Through strip charts, XY plots, statistical overlays, and real-time dashboards, you gain insights impossible with text output alone. The combination of high-speed packed data formats and professional visualization features creates a debugging environment that rivals dedicated test equipment.

Master the PLOT window and you master the art of seeing what your system is actually doing, not just what you think it's doing. Pattern recognition, trend analysis, anomaly detection—these become natural parts of your debugging workflow when data visualization is this accessible.

Next, we'll explore how the LOGIC window brings protocol analysis and digital signal visualization to your debugging arsenal, turning the P2 into a multi-channel logic analyzer.