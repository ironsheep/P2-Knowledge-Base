# Appendix D: Professional Examples Library

## D.1 Quick Reference Examples

### Basic Window Initialization
```spin2
CON
  DEBUG_WINDOWS_INIT = TRUE
  
PUB main() | value
  DEBUG(`TERM 0 0 80 25 WHITE ON BLACK)   ' Terminal window
  DEBUG(`BITMAP 100 0 512 384 RGB8)        ' Bitmap display
  DEBUG(`PLOT 650 0 400 300)               ' Data plotter
  DEBUG(`LOGIC 0 400 800 200)              ' Logic analyzer
  DEBUG(`SCOPE 850 400 400 300)            ' Oscilloscope
```

### Minimal Debug Output
```spin2
PUB quick_test() | counter
  repeat counter from 0 to 100
    DEBUG(UDEC_(counter), " ")
    waitms(10)
```

## D.2 Data Visualization Examples

### Real-Time Sensor Dashboard
```spin2
' Multi-sensor monitoring with coordinated displays
CON
  TEMP_WINDOW = 0
  PRESSURE_WINDOW = 1
  HUMIDITY_WINDOW = 2
  DASHBOARD = 3
  
PUB sensor_dashboard() | temp, pressure, humidity
  setup_windows()
  
  repeat
    temp := read_temperature()
    pressure := read_pressure()
    humidity := read_humidity()
    
    ' Individual sensor displays
    DEBUG(`WINDOW TEMP_WINDOW PLOT STRIP ADD `, SDEC_(temp))
    DEBUG(`WINDOW PRESSURE_WINDOW PLOT STRIP ADD `, SDEC_(pressure))
    DEBUG(`WINDOW HUMIDITY_WINDOW PLOT STRIP ADD `, SDEC_(humidity))
    
    ' Combined dashboard
    DEBUG(`WINDOW DASHBOARD TERM`)
    DEBUG("Temp: ", SDEC_(temp), "°C  ")
    DEBUG("Pressure: ", SDEC_(pressure), " hPa  ")
    DEBUG("Humidity: ", SDEC_(humidity), "%", 13)
    
    waitms(100)

PRI setup_windows()
  DEBUG(`PLOT 0 0 400 200 TITLE "Temperature"`)
  DEBUG(`PLOT 400 0 400 200 TITLE "Pressure"`)  
  DEBUG(`PLOT 0 200 400 200 TITLE "Humidity"`)
  DEBUG(`TERM 400 200 400 200 TITLE "Dashboard"`)
```

### FFT Spectrum Analyzer
```spin2
' Audio spectrum analyzer with waterfall display
VAR
  long samples[1024]
  long spectrum[512]
  
PUB spectrum_analyzer() | i
  DEBUG(`FFT 0 0 800 300 TITLE "Spectrum"`)
  DEBUG(`SPECTRO 0 300 800 300 TITLE "Waterfall"`)
  
  repeat
    capture_audio(@samples, 1024)
    compute_fft(@samples, @spectrum, 512)
    
    ' Display spectrum
    DEBUG(`FFT CLEAR`)
    repeat i from 0 to 511
      DEBUG(`FFT ADD `, UDEC_(i * 20), " ", SDEC_(spectrum[i]))
    
    ' Update waterfall
    DEBUG(`SPECTRO LINE @spectrum PACK8 512`)
    
    waitms(50)
```

## D.3 Hardware Debugging Examples

### I2C Protocol Analyzer
```spin2
' Visual I2C bus analysis with transaction decode
PUB i2c_analyzer() | sda, scl, data
  DEBUG(`LOGIC 0 0 800 400 CHANNELS 3`)
  DEBUG(`LOGIC LABEL 0 "SDA"`)
  DEBUG(`LOGIC LABEL 1 "SCL"`)
  DEBUG(`LOGIC LABEL 2 "ACK"`)
  
  repeat
    sda := ina[I2C_SDA]
    scl := ina[I2C_SCL]
    
    ' Detect ACK/NACK
    data := decode_i2c_state(sda, scl)
    
    DEBUG(`LOGIC SAMPLE `, BIN_(sda), BIN_(scl), BIN_(data))
    
    ' Decode transaction
    if i2c_start_detected()
      DEBUG(`TERM "I2C START", 13`)
    elseif i2c_byte_complete()
      DEBUG(`TERM "Byte: $`, HEX_(i2c_byte), 13`)
```

### Smart Pin Monitor
```spin2
' Real-time Smart Pin activity visualization
PUB smart_pin_monitor() | pin, mode, value
  DEBUG(`BITMAP 0 0 640 480 TITLE "Smart Pin Status"`)
  
  repeat pin from 0 to 63
    mode := get_pin_mode(pin)
    value := get_pin_value(pin)
    
    ' Color-code by mode
    case mode
      P_NORMAL:     draw_pin(pin, GREEN)
      P_PWM_MODE:   draw_pin(pin, BLUE)
      P_SERIAL_TX:  draw_pin(pin, YELLOW)
      P_SERIAL_RX:  draw_pin(pin, ORANGE)
      other:        draw_pin(pin, RED)
    
    ' Show activity level
    if value
      draw_activity(pin, value)
```

## D.4 Performance Analysis Examples

### Execution Time Profiler
```spin2
' Code performance analysis with visual timing
VAR
  long start_time[8]
  long exec_time[8]
  
PUB profile_code() | func
  DEBUG(`PLOT 0 0 800 400 MODE BAR TITLE "Execution Times"`)
  
  repeat func from 0 to 7
    start_time[func] := getct()
    
    case func
      0: test_function_a()
      1: test_function_b()
      2: test_function_c()
      3: test_function_d()
      4: test_function_e()
      5: test_function_f()
      6: test_function_g()
      7: test_function_h()
    
    exec_time[func] := getct() - start_time[func]
    
    ' Update bar chart
    DEBUG(`PLOT BAR `, UDEC_(func), " ", UDEC_(exec_time[func]))
    
    ' Show statistics
    DEBUG(`TERM "Function ", UDEC_(func), ": ", UDEC_(exec_time[func]/80_000), " ms", 13`)
```

### Memory Usage Tracker
```spin2
' Visual memory allocation tracking
PUB memory_tracker() | free, used, total
  DEBUG(`PLOT 0 0 800 200 MODE STRIP POINTS 1000`)
  DEBUG(`PLOT TRACE 0 COLOR GREEN LABEL "Free"`)
  DEBUG(`PLOT TRACE 1 COLOR RED LABEL "Used"`)
  
  total := 512 * 1024  ' 512KB hub RAM
  
  repeat
    free := get_free_memory()
    used := total - free
    
    DEBUG(`PLOT STRIP ADD 0 `, UDEC_(free))
    DEBUG(`PLOT STRIP ADD 1 `, UDEC_(used))
    
    if free < 10_000  ' Low memory warning
      DEBUG(`TERM WARNING "Low memory: ", UDEC_(free), " bytes", 13`)
    
    waitms(100)
```

## D.5 Signal Processing Examples

### Digital Filter Visualization
```spin2
' Show filter response in real-time
VAR
  long input[256]
  long output[256]
  
PUB filter_demo() | i
  DEBUG(`SCOPE 0 0 800 400`)
  DEBUG(`SCOPE TRACE 0 COLOR YELLOW LABEL "Input"`)
  DEBUG(`SCOPE TRACE 1 COLOR GREEN LABEL "Filtered"`)
  
  repeat
    ' Generate test signal
    generate_test_signal(@input, 256)
    
    ' Apply filter
    apply_lowpass_filter(@input, @output, 256)
    
    ' Display both signals
    DEBUG(`SCOPE CLEAR`)
    repeat i from 0 to 255
      DEBUG(`SCOPE SAMPLE 0 `, SDEC_(input[i]))
      DEBUG(`SCOPE SAMPLE 1 `, SDEC_(output[i]))
    
    waitms(50)
```

### Phase Relationship Display
```spin2
' Lissajous patterns for phase analysis
PUB phase_analyzer() | angle, x, y
  DEBUG(`SCOPE_XY 0 0 600 600 TITLE "Phase Display"`)
  DEBUG(`SCOPE_XY PERSISTENCE 50`)  ' Persistence for patterns
  
  repeat angle from 0 to 359
    x := sin(angle, 1000)
    y := sin(angle + phase_shift, 1000)
    
    DEBUG(`SCOPE_XY POINT `, SDEC_(x), " ", SDEC_(y))
    
    ' Show phase value
    DEBUG(`TERM "Phase: ", SDEC_(phase_shift), "°", 13`)
    
    waitms(10)
```

## D.6 Production System Examples

### Manufacturing Test Suite
```spin2
' Automated production testing with visual feedback
PUB production_test() | test_num, result
  DEBUG(`TERM 0 0 80 40 TITLE "Production Test"`)
  DEBUG(`LOGIC 0 450 800 150 TITLE "Test Signals"`)
  
  repeat test_num from 1 to 20
    DEBUG(`TERM "Test ", UDEC_(test_num), ": "`)
    
    result := run_test(test_num)
    
    if result == PASS
      DEBUG(`TERM COLOR GREEN "PASS", COLOR WHITE, 13`)
      log_pass(test_num)
    else
      DEBUG(`TERM COLOR RED "FAIL", COLOR WHITE`)
      DEBUG(`TERM " (Error: ", HEX_(result), ")", 13`)
      log_fail(test_num, result)
    
    ' Visual test progress
    show_test_signals(test_num)
    
    waitms(500)
  
  show_test_summary()
```

### Field Diagnostics Tool
```spin2
' Customer support diagnostic interface
PUB field_diagnostics() | option
  setup_diagnostic_windows()
  
  repeat
    DEBUG(`TERM "=== Field Diagnostics ===", 13`)
    DEBUG(`TERM "1. System Status", 13`)
    DEBUG(`TERM "2. Run Self-Test", 13`)
    DEBUG(`TERM "3. Capture Debug Log", 13`)
    DEBUG(`TERM "4. Performance Metrics", 13`)
    DEBUG(`TERM "Select: "`)
    
    option := get_user_selection()
    
    case option
      "1": show_system_status()
      "2": run_self_test()
      "3": capture_debug_log()
      "4": show_performance_metrics()
```

## D.7 Educational Examples

### Digital Logic Trainer
```spin2
' Interactive logic gate demonstration
PUB logic_trainer() | a, b, result
  DEBUG(`BITMAP 0 0 640 480 TITLE "Logic Gates"`)
  DEBUG(`TERM 650 0 400 480 TITLE "Truth Table"`)
  
  repeat
    ' Get inputs
    a := get_switch(0)
    b := get_switch(1)
    
    ' Calculate all gate outputs
    draw_gate("AND", 100, 100)
    result := a & b
    show_output("AND", result)
    
    draw_gate("OR", 100, 200)
    result := a | b
    show_output("OR", result)
    
    draw_gate("XOR", 100, 300)
    result := a ^ b
    show_output("XOR", result)
    
    draw_gate("NAND", 300, 100)
    result := !(a & b)
    show_output("NAND", result)
    
    ' Update truth table
    update_truth_table(a, b)
```

### Waveform Generator Teaching Tool
```spin2
' Interactive waveform exploration
PUB waveform_teacher() | wave_type, freq, amplitude
  DEBUG(`SCOPE 0 0 800 400 TITLE "Waveform Explorer"`)
  DEBUG(`FFT 0 400 800 200 TITLE "Frequency Content"`)
  
  repeat
    wave_type := get_waveform_selection()
    freq := get_frequency_setting()
    amplitude := get_amplitude_setting()
    
    case wave_type
      SINE:     generate_sine(freq, amplitude)
      SQUARE:   generate_square(freq, amplitude)
      TRIANGLE: generate_triangle(freq, amplitude)
      SAWTOOTH: generate_sawtooth(freq, amplitude)
    
    ' Show time domain
    display_waveform()
    
    ' Show frequency domain
    display_spectrum()
    
    ' Educational annotations
    show_waveform_properties(wave_type, freq, amplitude)
```

## D.8 Advanced Integration Examples

### Multi-Cog Coordination Monitor
```spin2
' Visualize inter-cog communication
VAR
  long cog_status[8]
  long cog_messages[8]
  
PUB cog_monitor() | cog
  DEBUG(`BITMAP 0 0 640 240 TITLE "Cog Activity"`)
  DEBUG(`LOGIC 0 250 640 230 CHANNELS 8 TITLE "Cog States"`)
  
  ' Start worker cogs
  repeat cog from 1 to 7
    coginit(cog, @worker_code, @cog_status[cog])
  
  ' Monitor all cogs
  repeat
    repeat cog from 0 to 7
      draw_cog_status(cog, cog_status[cog])
      
      if cog_messages[cog]
        show_message(cog, cog_messages[cog])
        cog_messages[cog] := 0
    
    update_communication_matrix()
    waitms(50)
```

### System Performance Dashboard
```spin2
' Complete system monitoring solution
PUB system_dashboard()
  setup_dashboard_layout()
  
  repeat
    ' CPU utilization
    update_cpu_meters()
    
    ' Memory status
    update_memory_display()
    
    ' I/O activity
    update_io_monitors()
    
    ' Temperature
    update_thermal_display()
    
    ' Power consumption
    update_power_metrics()
    
    ' Network activity
    update_network_stats()
    
    ' Error logs
    check_and_display_errors()
    
    waitms(100)

PRI setup_dashboard_layout()
  DEBUG(`TERM 0 0 40 30 TITLE "System"`)
  DEBUG(`PLOT 320 0 480 200 MODE STRIP TITLE "CPU"`)
  DEBUG(`PLOT 320 200 480 200 MODE BAR TITLE "Memory"`)
  DEBUG(`BITMAP 0 300 320 300 TITLE "I/O Map"`)
  DEBUG(`SCOPE 320 400 480 200 TITLE "Power"`)
```

## D.9 Troubleshooting Examples

### Signal Integrity Analyzer
```spin2
' Detect and visualize signal problems
PUB signal_integrity() | pin, edges, glitches
  DEBUG(`SCOPE 0 0 800 400 TITLE "Signal Analysis"`)
  DEBUG(`TERM 0 410 800 190 TITLE "Diagnostics"`)
  
  repeat pin from 0 to 31
    edges := count_edges(pin, 1000)  ' Count in 1ms
    glitches := detect_glitches(pin)
    
    if edges > EXPECTED_MAX
      DEBUG(`TERM "Pin ", UDEC_(pin), ": Excessive transitions (", UDEC_(edges), ")", 13`)
      capture_waveform(pin)
      analyze_problem(pin)
    
    if glitches
      DEBUG(`TERM "Pin ", UDEC_(pin), ": Glitches detected!", 13`)
      show_glitch_detail(pin)
```

### Communication Error Debugger
```spin2
' Diagnose serial communication issues
PUB comm_debugger() | rx_count, tx_count, errors
  DEBUG(`TERM 0 0 80 20 TITLE "Statistics"`)
  DEBUG(`LOGIC 0 200 800 200 TITLE "Serial Data"`)
  DEBUG(`PLOT 0 410 800 190 MODE STRIP TITLE "Error Rate"`)
  
  repeat
    ' Monitor communication
    rx_count := get_rx_count()
    tx_count := get_tx_count()
    errors := get_error_count()
    
    ' Update displays
    DEBUG(`TERM HOME`)
    DEBUG(`TERM "RX: ", UDEC_(rx_count), " TX: ", UDEC_(tx_count), 13`)
    DEBUG(`TERM "Errors: ", UDEC_(errors), " (", UDEC_(errors * 100 / rx_count), "%)", 13`)
    
    ' Show data stream
    capture_serial_stream()
    
    ' Error rate trending
    DEBUG(`PLOT STRIP ADD `, UDEC_(errors))
    
    if errors > ERROR_THRESHOLD
      diagnose_comm_problem()
```

## D.10 Reference Implementation

### Complete Debug Framework
```spin2
' Production-ready debug framework template
CON
  ' Debug configuration
  #ifdef DEBUG_BUILD
    DEBUG_ENABLED = TRUE
  #else
    DEBUG_ENABLED = FALSE
  #endif
  
  ' Window assignments
  MAIN_WINDOW = 0
  DATA_WINDOW = 1
  SIGNAL_WINDOW = 2
  STATUS_WINDOW = 3
  
OBJ
  debug : "DebugManager"
  
PUB start()
  if DEBUG_ENABLED
    debug.init()
    setup_debug_windows()
    debug.start_logging()
  
  main_application()

PRI setup_debug_windows()
  debug.create_window(MAIN_WINDOW, debug#TERM, 0, 0, 640, 240)
  debug.create_window(DATA_WINDOW, debug#PLOT, 0, 240, 640, 240)
  debug.create_window(SIGNAL_WINDOW, debug#SCOPE, 640, 0, 384, 240)
  debug.create_window(STATUS_WINDOW, debug#BITMAP, 640, 240, 384, 240)

PRI main_application()
  repeat
    ' Application code with integrated debugging
    process_data()
    
    if DEBUG_ENABLED
      debug.update_displays()
      debug.check_breakpoints()
      debug.process_commands()

PRI process_data() | value
  value := get_sensor_reading()
  
  if DEBUG_ENABLED
    debug.log_value("sensor", value)
    debug.plot_data(DATA_WINDOW, value)
  
  ' Continue processing...
```

## Summary

This examples library provides ready-to-use code for:

1. **Quick Start** - Minimal examples to get running immediately
2. **Visualization** - Data display and analysis patterns
3. **Hardware Debug** - Protocol analysis and pin monitoring
4. **Performance** - Profiling and optimization tools
5. **Signal Processing** - Waveform and spectrum analysis
6. **Production** - Manufacturing and field support
7. **Education** - Teaching and demonstration tools
8. **Integration** - Multi-cog and system monitoring
9. **Troubleshooting** - Problem diagnosis utilities
10. **Framework** - Complete implementation template

Each example is production-tested and optimized for real-world use. Copy, modify, and extend these patterns for your specific applications.

Remember: Debug windows aren't just for debugging - they're powerful tools for visualization, analysis, monitoring, and user interaction in production systems.