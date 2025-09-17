# Chapter 12: Multi-Window Coordination

*One window shows the I2C transaction. Another displays the resulting waveform. A third plots the control loop response. A fourth logs the state machine transitions. Separately, they tell fragments of the story. Together, they reveal the complete system behavior. Multi-window coordination transforms debugging from sequential investigation to parallel comprehension, where cause and effect become visible simultaneously.*

## The Power of Parallel Visibility

Single-window debugging is like watching a movie through a keyhole—you see action but miss context. Multi-window debugging provides the wide shot, the close-up, and the reaction shot simultaneously. When your motor controller receives a command, you want to see the command bits, the PWM output, the current waveform, and the position feedback all at once. Time correlation across windows reveals relationships that sequential viewing would miss.

Consider debugging a closed-loop control system. The LOGIC window shows your setpoint changes. The SCOPE window displays the system response. The PLOT window tracks the error signal. The FFT window reveals oscillation frequencies. When all four update synchronously, you instantly see that oscillation appears only when the setpoint changes rapidly—a slew rate limitation invisible to single-window analysis.

## Window Orchestration Architecture

```spin2
CON
  ' Multi-window system limits
  MAX_WINDOWS = 16          ' Simultaneous windows
  MAX_BANDWIDTH = 2_000_000 ' Total debug bandwidth
  UPDATE_RATES = 8          ' Different sync rates
  
VAR
  long window_handles[16]
  long update_timestamps[16]
  byte window_active[16]
  long master_timebase
  
PUB multi_window_system()
  ' Initialize window coordination
  master_timebase := cnt
  
  ' Create synchronized window set
  create_logic_window(0, 100, 100)     ' Top-left
  create_scope_window(1, 500, 100)     ' Top-right
  create_plot_window(2, 100, 400)      ' Bottom-left
  create_fft_window(3, 500, 400)       ' Bottom-right
  
  ' Set synchronized update rates
  set_window_sync_group(0, 3, 100)     ' 100Hz group
  
  ' Start coordinated capture
  coordinate_all_windows()
```

## Synchronized Data Capture

### Time-Aligned Sampling

Ensure all windows show the same moment:

```spin2
VAR
  long sync_timestamp
  long capture_buffers[4][1024]
  byte capture_ready[4]

PUB synchronized_capture() | window
  ' Single trigger point for all windows
  sync_timestamp := cnt
  
  ' Launch parallel capture cogs
  repeat window from 0 to 3
    cognew(@capture_cog, @capture_buffers[window])
  
  ' Wait for all captures
  repeat until capture_ready[0] & capture_ready[1] & capture_ready[2] & capture_ready[3]
  
  ' Update all windows with synchronized data
  DEBUG(`LOGIC SyncData TIMESTAMP `(sync_timestamp))
  DEBUG(`SyncData PACK8 1024 @capture_buffers[0])
  
  DEBUG(`SCOPE SyncData TIMESTAMP `(sync_timestamp))
  DEBUG(`SyncData PACK16 1024 @capture_buffers[1])
  
  DEBUG(`PLOT SyncData TIMESTAMP `(sync_timestamp))
  DEBUG(`SyncData PACK16 1024 @capture_buffers[2])
  
  DEBUG(`FFT SyncData TIMESTAMP `(sync_timestamp))
  DEBUG(`SyncData PACK16 512 @capture_buffers[3])

DAT
capture_cog
              org       0
              
              ' Wait for sync point
              rdlong    target, sync_ptr
:wait         rdlong    current, cnt_addr
              cmp       current, target wc
        if_c  jmp       #:wait
              
              ' Rapid capture
              mov       count, ##1024
              mov       ptr, par
              
:loop         rdpin     sample, #ADC_PIN
              wrlong    sample, ptr
              add       ptr, #4
              djnz      count, #:loop
              
              ' Signal complete
              mov       done, #1
              wrbyte    done, ready_ptr
              
              cogstop   cogid
```

### Trigger Propagation

One event triggers all windows:

```spin2
PUB master_slave_triggering() | trigger_source
  ' Configure master trigger
  DEBUG(`LOGIC Master TRIGGER PATTERN %10101010)
  
  ' Slave other windows to logic trigger
  DEBUG(`SCOPE Slave TRIGGER EXTERNAL LOGIC)
  DEBUG(`PLOT Slave TRIGGER EXTERNAL LOGIC)
  DEBUG(`FFT Slave TRIGGER EXTERNAL LOGIC)
  
  repeat
    ' Wait for master trigger
    trigger_source := wait_for_trigger()
    
    if trigger_source == LOGIC_TRIGGERED
      ' All windows capture simultaneously
      DEBUG(`ALL WINDOWS TRIGGERED)
      
      ' Coordinated capture
      capture_all_windows()
      
      ' Synchronized display update
      update_all_displays()

PUB cross_window_triggering()
  ' Complex trigger conditions across windows
  
  repeat
    ' Trigger when multiple conditions met
    if (logic_state == ERROR_STATE) and (scope_amplitude > THRESHOLD)
      DEBUG(`TRIGGER_ALL "Cross-window trigger fired")
      
      ' Capture state from all sources
      snapshot_system_state()
      
    ' Or trigger on calculated conditions
    if (fft_peak_frequency > 1000) and (plot_trend == RISING)
      DEBUG(`TRIGGER_ALL "Frequency/trend trigger")
      analyze_correlation()
```

## Window Layout Patterns

### Dashboard Layouts

Create comprehensive monitoring dashboards:

```spin2
PUB system_dashboard()
  ' Define dashboard regions
  TOP_ROW := 0
  MIDDLE_ROW := 200
  BOTTOM_ROW := 400
  LEFT_COL := 0
  CENTER_COL := 266
  RIGHT_COL := 533
  
  ' Status indicators (top row)
  DEBUG(`TERM Status SIZE 266 200 POS `(LEFT_COL) `(TOP_ROW))
  DEBUG(`PLOT Vitals SIZE 266 200 POS `(CENTER_COL) `(TOP_ROW))
  DEBUG(`LOGIC State SIZE 266 200 POS `(RIGHT_COL) `(TOP_ROW))
  
  ' Main displays (middle row)
  DEBUG(`SCOPE Signals SIZE 266 200 POS `(LEFT_COL) `(MIDDLE_ROW))
  DEBUG(`FFT Spectrum SIZE 266 200 POS `(CENTER_COL) `(MIDDLE_ROW))
  DEBUG(`PLOT Trends SIZE 266 200 POS `(RIGHT_COL) `(MIDDLE_ROW))
  
  ' Control panel (bottom row)
  DEBUG(`TERM Control SIZE 800 200 POS `(LEFT_COL) `(BOTTOM_ROW))
  
  ' Update all dashboard elements
  repeat
    update_status_panel()
    update_vitals_plot()
    update_state_logic()
    update_signal_scope()
    update_spectrum_fft()
    update_trends_plot()
    process_control_inputs()
    
    waitms(100)  ' 10Hz dashboard update

PUB tabbed_interface() | active_tab
  ' Tabbed window organization
  active_tab := 0
  
  repeat
    ' Show only active tab's windows
    case active_tab
      0:  ' Overview tab
        show_overview_windows()
      1:  ' Detailed analysis tab
        show_analysis_windows()
      2:  ' Performance tab
        show_performance_windows()
      3:  ' Diagnostics tab
        show_diagnostic_windows()
    
    ' Tab switching on keypress
    if key := DEBUG(PC_KEY)
      case key
        "1".."4": active_tab := key - "1"
        TAB: active_tab := (active_tab + 1) // 4
```

### Picture-in-Picture

Overlay critical info on main displays:

```spin2
PUB pip_display()
  ' Main window
  DEBUG(`SCOPE Main SIZE 800 600 POS 0 0)
  
  ' PiP overlay windows
  DEBUG(`LOGIC PiP1 SIZE 200 150 POS 580 20 OVERLAY)
  DEBUG(`PLOT PiP2 SIZE 200 150 POS 580 190 OVERLAY)
  DEBUG(`TERM PiP3 SIZE 200 150 POS 580 360 OVERLAY)
  
  repeat
    ' Update main display
    DEBUG(`Main PACK16 1024 @main_waveform)
    
    ' Update PiP windows with critical info
    DEBUG(`PiP1 PACK1 32 @digital_states)
    DEBUG(`PiP2 `(error_signal))
    DEBUG(`PiP3 "State: " hex_(current_state))
```

## Data Flow Coordination

### Producer-Consumer Patterns

Windows as data pipeline stages:

```spin2
VAR
  long pipeline_buffer[1024]
  long processed_buffer[1024]
  byte stage_complete[4]

PUB data_pipeline()
  ' Stage 1: Capture raw data (LOGIC window)
  DEBUG(`LOGIC RawCapture SIZE 400 200 POS 0 0)
  
  ' Stage 2: Filter/process (invisible)
  ' ...
  
  ' Stage 3: Display processed (SCOPE window)
  DEBUG(`SCOPE Filtered SIZE 400 200 POS 400 0)
  
  ' Stage 4: Analyze spectrum (FFT window)
  DEBUG(`FFT Analysis SIZE 400 200 POS 0 200)
  
  ' Stage 5: Track trends (PLOT window)
  DEBUG(`PLOT Trends SIZE 400 200 POS 400 200)
  
  repeat
    ' Pipeline processing
    if stage_complete[0]  ' Raw data ready
      apply_filter(@pipeline_buffer, @processed_buffer)
      DEBUG(`SCOPE Filtered PACK16 1024 @processed_buffer)
      stage_complete[1] := TRUE
      
    if stage_complete[1]  ' Filtered data ready
      compute_spectrum(@processed_buffer, @spectrum_buffer)
      DEBUG(`FFT Analysis PACK16 512 @spectrum_buffer)
      stage_complete[2] := TRUE
      
    if stage_complete[2]  ' Spectrum ready
      extract_trend(@spectrum_buffer, @trend_value)
      DEBUG(`PLOT Trends `(trend_value))
      stage_complete[3] := TRUE
```

### Circular Buffer Sharing

Multiple windows view same data:

```spin2
VAR
  long shared_circular[8192]
  long write_index
  long read_indices[4]  ' Per window

PUB shared_buffer_windows()
  ' All windows read from same circular buffer
  ' but at different rates and positions
  
  ' Fast update window - shows latest
  DEBUG(`SCOPE Latest SIZE 400 300 POS 0 0)
  
  ' Slow update window - shows history
  DEBUG(`PLOT History SIZE 400 300 POS 400 0)
  
  ' Triggered window - shows events
  DEBUG(`LOGIC Events SIZE 800 300 POS 0 300)
  
  ' Start data producer
  cognew(@data_producer, @shared_circular)
  
  repeat
    ' Each window reads at its own rate
    update_latest_scope()     ' Every 10ms
    
    if cnt - last_history > clkfreq/10
      update_history_plot()   ' Every 100ms
      last_history := cnt
      
    if trigger_detected()
      update_event_logic()    ' On trigger only

PRI update_latest_scope()
  ' Show most recent 256 samples
  start_idx := (write_index - 256) & $1FFF
  DEBUG(`SCOPE Latest PACK16 256 @shared_circular[start_idx])

PRI update_history_plot()
  ' Show last 2048 samples decimated
  repeat i from 0 to 255
    decimated[i] := shared_circular[(write_index - i*8) & $1FFF]
  DEBUG(`PLOT History PACK16 256 @decimated)
```

## Performance Management

### Bandwidth Allocation

Manage debug bandwidth across windows:

```spin2
VAR
  long bandwidth_budget[16]
  long bandwidth_used[16]
  long priority_levels[16]

PUB bandwidth_manager() | total_used, window
  ' Set window priorities
  priority_levels[SCOPE_WINDOW] := PRIORITY_HIGH
  priority_levels[LOGIC_WINDOW] := PRIORITY_HIGH
  priority_levels[PLOT_WINDOW] := PRIORITY_MEDIUM
  priority_levels[FFT_WINDOW] := PRIORITY_LOW
  
  ' Allocate bandwidth budget
  bandwidth_budget[SCOPE_WINDOW] := 500_000   ' 500kbps
  bandwidth_budget[LOGIC_WINDOW] := 400_000   ' 400kbps
  bandwidth_budget[PLOT_WINDOW] := 200_000    ' 200kbps
  bandwidth_budget[FFT_WINDOW] := 100_000     ' 100kbps
  
  repeat
    ' Monitor actual usage
    total_used := 0
    repeat window from 0 to 3
      bandwidth_used[window] := measure_bandwidth(window)
      total_used += bandwidth_used[window]
    
    ' Adjust if over budget
    if total_used > MAX_BANDWIDTH
      reduce_update_rates(total_used - MAX_BANDWIDTH)
    
    ' Report status
    if cnt - last_report > clkfreq
      report_bandwidth_usage()
      last_report := cnt

PRI reduce_update_rates(excess) | window
  ' Reduce low priority windows first
  repeat priority from PRIORITY_LOW to PRIORITY_HIGH
    repeat window from 0 to 3
      if priority_levels[window] == priority
        if bandwidth_used[window] > bandwidth_budget[window]
          ' Reduce this window's update rate
          new_rate := current_rate[window] * bandwidth_budget[window] / bandwidth_used[window]
          set_window_update_rate(window, new_rate)
          
          excess -= (bandwidth_used[window] - bandwidth_budget[window])
          if excess <= 0
            return
```

### Update Rate Optimization

Balance responsiveness with performance:

```spin2
PUB adaptive_update_rates() | activity_level, optimal_rate
  ' Adjust update rates based on activity
  
  repeat
    ' Measure system activity
    activity_level := measure_signal_activity()
    
    case activity_level
      IDLE:
        ' Slow updates when nothing happening
        set_all_window_rates(1)  ' 1Hz
        
      STEADY_STATE:
        ' Moderate updates for monitoring
        set_all_window_rates(10)  ' 10Hz
        
      TRANSIENT:
        ' Fast updates during changes
        set_all_window_rates(100)  ' 100Hz
        
      CRITICAL:
        ' Maximum updates for critical events
        set_all_window_rates(1000)  ' 1kHz
    
    ' Window-specific optimization
    optimize_individual_windows()

PRI optimize_individual_windows()
  ' FFT doesn't need fast updates
  if fft_window_active
    set_window_update_rate(FFT_WINDOW, 2)  ' 2Hz is plenty
  
  ' Logic needs fast updates during protocol activity
  if protocol_active
    set_window_update_rate(LOGIC_WINDOW, 1000)
  else
    set_window_update_rate(LOGIC_WINDOW, 10)
  
  ' Scope follows signal frequency
  signal_freq := measure_signal_frequency()
  scope_rate := signal_freq * 10  ' 10x oversampling
  set_window_update_rate(SCOPE_WINDOW, scope_rate)
```

## Advanced Coordination Patterns

### State Machine Visualization

Coordinate windows to show state machine operation:

```spin2
PUB state_machine_dashboard()
  ' State diagram
  DEBUG(`PLOT StateDiagram SIZE 400 400 POS 0 0)
  DEBUG(`StateDiagram MODE XY RANGE 0 100 0 100)
  
  ' State timing
  DEBUG(`LOGIC StateTiming SIZE 400 200 POS 400 0)
  DEBUG(`StateTiming CHANNELS 4 LABELS "S0" "S1" "S2" "S3")
  
  ' State variables
  DEBUG(`PLOT StateVars SIZE 400 200 POS 400 200)
  DEBUG(`StateVars TRACES 4 LABELS "Var1" "Var2" "Var3" "Var4")
  
  ' State history
  DEBUG(`TERM StateLog SIZE 400 400 POS 0 400)
  
  repeat
    ' Update state diagram
    draw_state_transition(old_state, new_state)
    
    ' Update timing diagram
    DEBUG(`StateTiming DATA `(state_bits))
    
    ' Update variables
    DEBUG(`StateVars DATA `(var1, var2, var3, var4))
    
    ' Log transitions
    DEBUG(`StateLog "T=" dec_(cnt/80000) ": ")
    DEBUG(`StateLog hex_(old_state) "->" hex_(new_state))
    DEBUG(`StateLog " (" state_name(new_state) ")\n")

PRI draw_state_transition(from, to)
  ' Animate state transitions
  repeat step from 0 to 10
    x := interpolate(state_x[from], state_x[to], step, 10)
    y := interpolate(state_y[from], state_y[to], step, 10)
    
    DEBUG(`StateDiagram POINT `(x, y) COLOR RED SIZE 5)
    waitms(20)
  
  ' Highlight active state
  DEBUG(`StateDiagram CIRCLE `(state_x[to], state_y[to]) 10 COLOR GREEN)
```

### Control Loop Analysis

Multiple windows for PID tuning:

```spin2
PUB pid_tuning_dashboard() | setpoint, process, error, output
  ' Setpoint and process variable
  DEBUG(`PLOT Response SIZE 800 300 POS 0 0)
  DEBUG(`Response TRACES 2 LABELS "Setpoint" "Process")
  DEBUG(`Response COLORS GREEN RED)
  
  ' Error signal
  DEBUG(`PLOT Error SIZE 400 300 POS 0 300)
  DEBUG(`Error LABELS "Error")
  DEBUG(`Error RANGE -100 100)
  
  ' Control output
  DEBUG(`PLOT Control SIZE 400 300 POS 400 300)
  DEBUG(`Control LABELS "Output")
  DEBUG(`Control RANGE 0 255)
  
  ' PID components
  DEBUG(`PLOT PIDterms SIZE 800 200 POS 0 600)
  DEBUG(`PIDterms TRACES 3 LABELS "P" "I" "D")
  
  repeat
    ' PID calculation
    error := setpoint - process
    p_term := Kp * error
    i_term += Ki * error
    d_term := Kd * (error - last_error)
    output := p_term + i_term + d_term
    
    ' Update all displays
    DEBUG(`Response DATA `(setpoint, process))
    DEBUG(`Error DATA `(error))
    DEBUG(`Control DATA `(output))
    DEBUG(`PIDterms DATA `(p_term, i_term, d_term))
    
    ' Interactive tuning
    if key := DEBUG(PC_KEY)
      case key
        "P", "p": adjust_Kp(key == "P")
        "I", "i": adjust_Ki(key == "I")
        "D", "d": adjust_Kd(key == "D")
```

### Multi-Channel Protocol Analysis

Coordinate windows for complex protocols:

```spin2
PUB can_bus_analyzer()
  ' CAN signal levels
  DEBUG(`SCOPE CANsignals SIZE 400 300 POS 0 0)
  DEBUG(`CANsignals CHANNELS 2 LABELS "CANH" "CANL")
  
  ' Digital view
  DEBUG(`LOGIC CANlogic SIZE 400 300 POS 400 0)
  DEBUG(`CANlogic CHANNELS 2 LABELS "CAN_H" "CAN_L")
  DEBUG(`CANlogic DECODE CAN)
  
  ' Message list
  DEBUG(`TERM CANmessages SIZE 400 300 POS 0 300)
  
  ' Bus load
  DEBUG(`PLOT CANload SIZE 400 300 POS 400 300)
  DEBUG(`CANload LABELS "Bus Load %")
  
  repeat
    ' Capture differential signals
    can_h := read_adc(CAN_H_PIN)
    can_l := read_adc(CAN_L_PIN)
    
    ' Update scope with analog levels
    DEBUG(`CANsignals DATA `(can_h, can_l))
    
    ' Update logic with digital interpretation
    can_diff := can_h - can_l
    can_bit := can_diff > THRESHOLD
    DEBUG(`CANlogic DATA `(can_bit))
    
    ' Decode message if complete
    if message_complete()
      decode_can_message(@message_buffer)
      display_can_message()
      
    ' Calculate and display bus load
    bus_load := (bits_transmitted * 100) / (time_elapsed * CAN_BITRATE)
    DEBUG(`CANload DATA `(bus_load))
```

## Real-World Applications

### Production Test Station

Multi-window test automation:

```spin2
PUB automated_test_station() | test_number, pass_count, fail_count
  ' Test status overview
  DEBUG(`TERM TestStatus SIZE 800 100 POS 0 0)
  
  ' Measurement displays
  DEBUG(`SCOPE Waveforms SIZE 400 250 POS 0 100)
  DEBUG(`FFT Spectrum SIZE 400 250 POS 400 100)
  DEBUG(`LOGIC Digital SIZE 400 250 POS 0 350)
  DEBUG(`PLOT Trends SIZE 400 250 POS 400 350)
  
  repeat test_number from 1 to NUM_TESTS
    ' Update status
    DEBUG(`TestStatus CLEAR)
    DEBUG(`TestStatus "Test " dec_(test_number) " of " dec_(NUM_TESTS))
    DEBUG(`TestStatus ": " test_name(test_number))
    
    ' Run test with appropriate window
    case test_categories[test_number]
      ANALOG_TEST:
        result := run_analog_test(test_number)
        DEBUG(`SCOPE Waveforms PACK16 512 @test_waveform)
        
      DIGITAL_TEST:
        result := run_digital_test(test_number)
        DEBUG(`LOGIC Digital PACK8 256 @test_pattern)
        
      FREQUENCY_TEST:
        result := run_frequency_test(test_number)
        DEBUG(`FFT Spectrum PACK16 256 @test_spectrum)
        
      PARAMETRIC_TEST:
        result := run_parametric_test(test_number)
        DEBUG(`PLOT Trends DATA `(test_measurement))
    
    ' Update statistics
    if result == PASS
      pass_count++
      DEBUG(`TestStatus " PASS" COLOR GREEN)
    else
      fail_count++
      DEBUG(`TestStatus " FAIL" COLOR RED)
      log_failure_details(test_number)
    
  ' Final report
  generate_test_report(pass_count, fail_count)
```

### System Performance Monitor

Comprehensive performance dashboard:

```spin2
PUB performance_monitor()
  ' CPU usage per cog
  DEBUG(`PLOT CogUsage SIZE 400 200 POS 0 0)
  DEBUG(`CogUsage TRACES 8 STYLE STACKED)
  
  ' Memory usage
  DEBUG(`PLOT Memory SIZE 400 200 POS 400 0)
  DEBUG(`Memory TRACES 3 LABELS "Hub" "Cog" "Free")
  
  ' I/O activity
  DEBUG(`LOGIC IOactivity SIZE 400 200 POS 0 200)
  DEBUG(`IOactivity CHANNELS 32)
  
  ' Temperature and power
  DEBUG(`SCOPE TempPower SIZE 400 200 POS 400 200)
  DEBUG(`TempPower CHANNELS 2 LABELS "Temp" "Power")
  
  ' Event log
  DEBUG(`TERM EventLog SIZE 800 200 POS 0 400)
  
  repeat
    ' Gather all metrics
    measure_cog_usage(@cog_usage)
    measure_memory_usage(@memory_stats)
    capture_io_state(@io_state)
    read_temp_power(@temp, @power)
    
    ' Update all windows
    DEBUG(`CogUsage PACK8 8 @cog_usage)
    DEBUG(`Memory DATA `(memory_stats[0], memory_stats[1], memory_stats[2]))
    DEBUG(`IOactivity PACK32 1 @io_state)
    DEBUG(`TempPower DATA `(temp, power))
    
    ' Log significant events
    if detect_anomaly()
      DEBUG(`EventLog timestamp() " Anomaly: " describe_anomaly())
    
    waitms(250)  ' 4Hz update
```

## Troubleshooting Multi-Window Systems

Common issues and solutions:

**Problem**: Windows update out of sync
**Solution**: Use common timebase
```spin2
master_time := cnt
' All windows reference same timebase
DEBUG(`ALL_WINDOWS TIMEBASE `(master_time))
```

**Problem**: Debug bandwidth saturation
**Solution**: Implement priority system
```spin2
' Critical windows get bandwidth first
if bandwidth_available() < required
  disable_low_priority_windows()
```

**Problem**: Display cluttered with too many windows
**Solution**: Use window groups
```spin2
' Show/hide window groups together
case display_mode
  OVERVIEW: show_windows(@overview_group)
  DETAIL: show_windows(@detail_group)
  DIAGNOSTIC: show_windows(@diagnostic_group)
```

## Chapter Summary

Multi-window coordination elevates debugging from isolated observations to system-wide comprehension. By synchronizing data capture, coordinating triggers, managing bandwidth, and organizing displays, you create debugging environments that reveal complex interactions and subtle relationships. The ability to see multiple aspects of system behavior simultaneously transforms troubleshooting from guesswork to science.

Whether building production test systems, tuning control loops, or analyzing complex protocols, multi-window coordination provides the comprehensive visibility needed for professional debugging. The P2 becomes not just a microcontroller with debug capability, but a complete instrumentation platform.

Next, we'll explore PASM assembly integration, where low-level code meets high-level visualization.