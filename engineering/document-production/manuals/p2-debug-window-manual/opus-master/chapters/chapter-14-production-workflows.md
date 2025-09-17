# Chapter 14: Production Integration Workflows

*Debug windows aren't just for debugging—they're for documenting, demonstrating, validating, and deploying. When screenshots become specifications, test results become reports, and debug sessions become training materials, the debug system transforms from development tool to production asset. This is where temporary becomes permanent, where debugging becomes part of the product.*

## From Debug to Deployment

Traditional thinking separates debug from production—debug code gets stripped before release, debug outputs disappear in deployment. But P2's debug windows challenge this assumption. Why remove the oscilloscope view that helps field technicians? Why strip the diagnostic dashboard that customer support needs? Why delete the performance monitors that prove your system meets specifications?

Consider a motor controller going to production. Instead of removing debug capabilities, you refine them into diagnostic modes. The SCOPE window becomes the built-in oscilloscope for field troubleshooting. The FFT window becomes the vibration analyzer for predictive maintenance. The LOGIC window becomes the protocol analyzer for system integration. Debug windows evolve from development tools to product features.

## Documentation Through Debug

### Living Documentation

Debug windows as interactive specifications:

```spin2
PUB generate_timing_diagram() | state
  ' Create timing specification diagram
  DEBUG(`LOGIC TimingSpec SIZE 800 400 POS 100 100)
  DEBUG(`TimingSpec TITLE "SPI Interface Timing Specification")
  DEBUG(`TimingSpec CHANNELS 4 LABELS "CLK" "MOSI" "MISO" "CS")
  DEBUG(`TimingSpec GRID ON)
  DEBUG(`TimingSpec CURSORS ON)
  
  ' Generate reference timing
  repeat state from 0 to 7
    ' Clock
    clk := state & 1
    DEBUG(`TimingSpec CH1 `(clk))
    
    ' MOSI changes on falling edge
    if clk == 0
      mosi := (test_data >> (7-state/2)) & 1
      DEBUG(`TimingSpec CH2 `(mosi))
    
    ' MISO changes on rising edge  
    if clk == 1
      miso := (response_data >> (7-state/2)) & 1
      DEBUG(`TimingSpec CH3 `(miso))
    
    ' CS remains low
    DEBUG(`TimingSpec CH4 0)
    
    ' Add timing annotations
    if state == 2
      DEBUG(`TimingSpec ANNOTATION "Setup Time" CURSOR)
    if state == 3
      DEBUG(`TimingSpec ANNOTATION "Hold Time" CURSOR)
    
    waitms(100)  ' Slow for visibility
  
  ' Capture screenshot for documentation
  DEBUG(`TimingSpec SCREENSHOT "spi_timing_spec.png")
  
  ' Add specifications
  DEBUG(`TERM "SPI Timing Specifications:")
  DEBUG(`TERM "  Clock Frequency: 10MHz max")
  DEBUG(`TERM "  Setup Time: 10ns min")
  DEBUG(`TERM "  Hold Time: 5ns min")
  DEBUG(`TERM "  CS to Clock: 20ns min")

PUB create_waveform_documentation()
  ' Generate all specified waveforms
  repeat test from 0 to NUM_TESTS-1
    ' Configure scope for this test
    DEBUG(`SCOPE Doc#test SIZE 800 400)
    DEBUG(`Doc#test TITLE test_names[test])
    DEBUG(`Doc#test TIMEBASE test_timebases[test])
    DEBUG(`Doc#test VOLTS test_scales[test])
    
    ' Generate test waveform
    generate_test_signal(test)
    capture_waveform(@waveform_buffer)
    
    ' Display with measurements
    DEBUG(`Doc#test PACK16 512 @waveform_buffer)
    DEBUG(`Doc#test MEASUREMENTS ON)
    
    ' Capture for documentation
    waitms(500)  ' Let display stabilize
    DEBUG(`Doc#test SCREENSHOT test_files[test])
    
    ' Generate markdown documentation
    generate_markdown_section(test)
```

### Interactive Specifications

Debug windows as executable specs:

```spin2
PUB interactive_protocol_spec()
  ' Create interactive protocol documentation
  DEBUG(`TERM ProtocolSpec SIZE 800 600)
  DEBUG(`ProtocolSpec CLEAR)
  DEBUG(`ProtocolSpec "INTERACTIVE PROTOCOL SPECIFICATION\n")
  DEBUG(`ProtocolSpec "===================================\n\n")
  
  ' Menu system
  DEBUG(`ProtocolSpec "Select protocol to demonstrate:\n")
  DEBUG(`ProtocolSpec "1. I2C Write Transaction\n")
  DEBUG(`ProtocolSpec "2. I2C Read Transaction\n")
  DEBUG(`ProtocolSpec "3. SPI Full Duplex\n")
  DEBUG(`ProtocolSpec "4. UART Frame Format\n")
  DEBUG(`ProtocolSpec "5. Custom Protocol\n")
  
  repeat
    key := DEBUG(PC_KEY)
    
    case key
      "1": demonstrate_i2c_write()
      "2": demonstrate_i2c_read()
      "3": demonstrate_spi_fullduplex()
      "4": demonstrate_uart_frame()
      "5": demonstrate_custom_protocol()
      "r": run_all_demonstrations()
      "s": save_all_screenshots()

PRI demonstrate_i2c_write()
  ' Step-by-step I2C write with annotations
  DEBUG(`LOGIC I2CDemo SIZE 800 300 POS 0 300)
  DEBUG(`I2CDemo CHANNELS 2 LABELS "SDA" "SCL")
  
  DEBUG(`TERM "\nI2C Write Transaction:\n")
  
  ' Start condition
  DEBUG(`TERM "1. START condition: SDA falls while SCL high\n")
  sda := 1
  scl := 1
  DEBUG(`I2CDemo DATA `(sda, scl))
  waitms(200)
  
  sda := 0  ' SDA falls
  DEBUG(`I2CDemo DATA `(sda, scl))
  DEBUG(`I2CDemo MARKER "START")
  waitms(200)
  
  ' Address byte
  DEBUG(`TERM "2. Send 7-bit address + W bit\n")
  repeat bit from 7 to 0
    scl := 0
    sda := (DEVICE_ADDR >> bit) & 1
    DEBUG(`I2CDemo DATA `(sda, scl))
    waitms(100)
    
    scl := 1
    DEBUG(`I2CDemo DATA `(sda, scl))
    waitms(100)
    
    if bit == 0
      DEBUG(`I2CDemo MARKER "W")
  
  ' Continue with ACK, data, stop...
```

## Test Automation Integration

### Automated Test Reporting

Debug windows generate test reports:

```spin2
VAR
  long test_results[100]
  byte test_status[100]
  
PUB automated_test_suite() | test_id, passed, failed
  ' Initialize test report
  DEBUG(`TERM TestReport SIZE 800 600)
  DEBUG(`TestReport CLEAR)
  DEBUG(`TestReport "AUTOMATED TEST REPORT\n")
  DEBUG(`TestReport "Generated: " timestamp() "\n")
  DEBUG(`TestReport "======================\n\n")
  
  ' Test progress bar
  DEBUG(`PLOT Progress SIZE 800 50 POS 0 0)
  DEBUG(`Progress MODE BAR RANGE 0 100)
  
  ' Run test suite
  passed := 0
  failed := 0
  
  repeat test_id from 0 to NUM_TESTS-1
    ' Update progress
    progress := (test_id * 100) / NUM_TESTS
    DEBUG(`Progress `(progress))
    
    ' Run test
    result := execute_test(test_id)
    test_results[test_id] := result
    
    ' Update report
    if result == PASS
      test_status[test_id] := "✓"
      passed++
      DEBUG(`TestReport "✓ ")
    else
      test_status[test_id] := "✗"
      failed++
      DEBUG(`TestReport "✗ ")
    
    DEBUG(`TestReport "Test " dec_(test_id) ": " test_names[test_id])
    DEBUG(`TestReport " - " test_descriptions[test_id] "\n")
    
    ' Capture evidence
    if result == FAIL
      capture_failure_evidence(test_id)
  
  ' Generate summary
  generate_test_summary(passed, failed)
  
  ' Export results
  export_test_results()

PRI capture_failure_evidence(test_id)
  ' Capture debug windows for failed tests
  DEBUG(`ALL_WINDOWS SCREENSHOT "test_" dec_(test_id) "_failure.png")
  
  ' Capture specific data
  case test_categories[test_id]
    TIMING_TEST:
      DEBUG(`LOGIC TestEvidence SAVE "test_" dec_(test_id) "_timing.csv")
    
    ANALOG_TEST:
      DEBUG(`SCOPE TestEvidence SAVE "test_" dec_(test_id) "_waveform.csv")
    
    FREQUENCY_TEST:
      DEBUG(`FFT TestEvidence SAVE "test_" dec_(test_id) "_spectrum.csv")
  
  ' Log detailed failure info
  DEBUG(`TestReport "  FAILURE DETAILS:\n")
  DEBUG(`TestReport "    Expected: " expected_values[test_id] "\n")
  DEBUG(`TestReport "    Actual: " actual_values[test_id] "\n")
  DEBUG(`TestReport "    Evidence: test_" dec_(test_id) "_*.png/csv\n")

PRI generate_test_summary(passed, failed) | pass_rate
  ' Summary statistics
  pass_rate := (passed * 100) / (passed + failed)
  
  DEBUG(`TestReport "\n======================\n")
  DEBUG(`TestReport "TEST SUMMARY\n")
  DEBUG(`TestReport "======================\n")
  DEBUG(`TestReport "Total Tests: " dec_(passed + failed) "\n")
  DEBUG(`TestReport "Passed: " dec_(passed) "\n")
  DEBUG(`TestReport "Failed: " dec_(failed) "\n")
  DEBUG(`TestReport "Pass Rate: " dec_(pass_rate) "%\n")
  
  ' Visual summary
  DEBUG(`PLOT Summary SIZE 400 300 POS 400 300)
  DEBUG(`Summary MODE PIE)
  DEBUG(`Summary DATA `(passed, failed))
  DEBUG(`Summary LABELS "Pass" "Fail")
  DEBUG(`Summary COLORS GREEN RED)
```

### Continuous Integration

Debug windows in CI/CD pipelines:

```spin2
PUB ci_test_runner() | commit_hash, build_number
  ' Get CI environment info
  commit_hash := get_env("GIT_COMMIT")
  build_number := get_env("BUILD_NUMBER")
  
  ' Initialize CI reporting
  DEBUG(`TERM CIReport SIZE 800 600)
  DEBUG(`CIReport "CI BUILD #" dec_(build_number) "\n")
  DEBUG(`CIReport "Commit: " hex_(commit_hash) "\n")
  DEBUG(`CIReport "Branch: " get_env("GIT_BRANCH") "\n")
  DEBUG(`CIReport "======================\n\n")
  
  ' Performance baseline comparison
  DEBUG(`PLOT Performance SIZE 800 300 POS 0 0)
  DEBUG(`Performance TRACES 2 LABELS "Current" "Baseline")
  
  ' Run performance tests
  repeat test from 0 to PERF_TESTS-1
    current_perf := measure_performance(test)
    baseline_perf := load_baseline(test)
    
    DEBUG(`Performance DATA `(current_perf, baseline_perf))
    
    ' Check regression
    if current_perf < (baseline_perf * 0.95)  ' 5% regression threshold
      DEBUG(`CIReport "PERFORMANCE REGRESSION: Test " dec_(test))
      DEBUG(`CIReport " Degradation: " dec_((baseline_perf - current_perf) * 100 / baseline_perf) "%\n")
      ci_test_failed := TRUE
  
  ' Memory usage analysis
  check_memory_usage()
  
  ' Code coverage visualization
  display_code_coverage()
  
  ' Set CI exit code
  if ci_test_failed
    set_exit_code(1)  ' Fail the build
  else
    set_exit_code(0)  ' Pass the build
    
    ' Update baselines on success
    if get_env("UPDATE_BASELINE") == "true"
      update_performance_baselines()
```

## Customer Support Tools

### Built-in Diagnostics

Debug windows as service tools:

```spin2
PUB diagnostic_mode() | mode
  ' Product diagnostic interface
  DEBUG(`TERM DiagMenu SIZE 800 600)
  DEBUG(`DiagMenu CLEAR)
  DEBUG(`DiagMenu "SYSTEM DIAGNOSTICS\n")
  DEBUG(`DiagMenu "==================\n\n")
  DEBUG(`DiagMenu "1. System Health Check\n")
  DEBUG(`DiagMenu "2. Performance Monitor\n")
  DEBUG(`DiagMenu "3. Signal Analysis\n")
  DEBUG(`DiagMenu "4. Error Log Review\n")
  DEBUG(`DiagMenu "5. Calibration Mode\n")
  DEBUG(`DiagMenu "6. Generate Support Bundle\n")
  
  repeat
    mode := DEBUG(PC_KEY) - "0"
    
    case mode
      1: system_health_check()
      2: performance_monitor_mode()
      3: signal_analysis_mode()
      4: error_log_review()
      5: calibration_mode()
      6: generate_support_bundle()

PRI system_health_check()
  ' Comprehensive system test
  DEBUG(`TERM "\nSYSTEM HEALTH CHECK\n")
  DEBUG(`TERM "-------------------\n")
  
  ' Voltage rails
  DEBUG(`SCOPE Voltages SIZE 400 200 POS 0 200)
  DEBUG(`Voltages CHANNELS 4 LABELS "3.3V" "5V" "12V" "VREF")
  
  measure_voltages(@voltages)
  DEBUG(`Voltages PACK16 4 @voltages)
  
  ' Check tolerances
  if check_voltage_tolerances(@voltages)
    DEBUG(`TERM "✓ Power supplies: OK\n")
  else
    DEBUG(`TERM "✗ Power supplies: OUT OF SPEC\n")
    identify_voltage_problems(@voltages)
  
  ' Temperature monitoring
  check_temperatures()
  
  ' Communication interfaces
  check_communications()
  
  ' Memory integrity
  check_memory_integrity()
  
  ' Generate health score
  health_score := calculate_health_score()
  DEBUG(`TERM "\nOVERALL HEALTH SCORE: " dec_(health_score) "%\n")
  
  if health_score < 80
    DEBUG(`TERM "\nRECOMMENDATION: Contact support\n")
    suggest_corrective_actions()

PRI generate_support_bundle()
  ' Collect all diagnostic data
  DEBUG(`TERM "\nGENERATING SUPPORT BUNDLE...\n")
  
  ' System information
  bundle_id := generate_bundle_id()
  DEBUG(`TERM "Bundle ID: " hex_(bundle_id) "\n")
  
  ' Capture all debug windows
  DEBUG(`ALL_WINDOWS SCREENSHOT "bundle_" hex_(bundle_id) "_screen.png")
  
  ' Export data logs
  DEBUG(`SCOPE EXPORT "bundle_" hex_(bundle_id) "_waveforms.csv")
  DEBUG(`LOGIC EXPORT "bundle_" hex_(bundle_id) "_digital.csv")
  DEBUG(`FFT EXPORT "bundle_" hex_(bundle_id) "_spectrum.csv")
  DEBUG(`PLOT EXPORT "bundle_" hex_(bundle_id) "_trends.csv")
  
  ' System configuration
  export_configuration("bundle_" hex_(bundle_id) "_config.json")
  
  ' Error history
  export_error_log("bundle_" hex_(bundle_id) "_errors.log")
  
  ' Performance metrics
  export_performance_data("bundle_" hex_(bundle_id) "_perf.csv")
  
  ' Compress bundle
  compress_bundle(bundle_id)
  
  DEBUG(`TERM "\n✓ Support bundle created: bundle_" hex_(bundle_id) ".zip\n")
  DEBUG(`TERM "  Size: " dec_(bundle_size) " KB\n")
  DEBUG(`TERM "  Send to: support@company.com\n")
```

### Remote Debugging

Debug windows over network:

```spin2
PUB remote_debug_server() | client_ip, command
  ' Start remote debug server
  DEBUG(`TERM "Remote Debug Server Started\n")
  DEBUG(`TERM "Listening on port 8080\n\n")
  
  repeat
    ' Wait for client connection
    client_ip := wait_for_connection()
    
    DEBUG(`TERM "Client connected from " ip_string(client_ip) "\n")
    
    ' Remote debug session
    repeat while connected
      command := receive_command()
      
      case command
        CMD_GET_STATUS:
          send_system_status()
          
        CMD_START_SCOPE:
          ' Enable scope remotely
          DEBUG(`SCOPE Remote SIZE 800 400)
          start_streaming_scope()
          
        CMD_GET_SCREENSHOT:
          ' Capture and send screenshot
          DEBUG(`ALL_WINDOWS SCREENSHOT "remote_capture.png")
          send_file("remote_capture.png")
          
        CMD_RUN_DIAGNOSTIC:
          ' Run diagnostic remotely
          result := run_diagnostic(get_parameter())
          send_result(result)
          
        CMD_LIVE_STREAM:
          ' Stream debug windows
          start_debug_stream(client_ip)
          
        CMD_DISCONNECT:
          DEBUG(`TERM "Client disconnected\n")
          connected := FALSE

PRI start_debug_stream(client_ip)
  ' Stream debug windows to remote client
  repeat while streaming_active
    ' Capture frame
    frame_data := capture_debug_frame()
    
    ' Compress if needed
    if compression_enabled
      frame_data := compress_frame(frame_data)
    
    ' Send to client
    send_frame(client_ip, frame_data)
    
    ' Throttle to requested FPS
    waitms(1000 / stream_fps)
```

## Performance Validation

### Benchmark Visualization

Debug windows for performance proof:

```spin2
PUB benchmark_suite() | test, baseline, current
  ' Performance benchmark dashboard
  DEBUG(`PLOT Benchmarks SIZE 800 400 POS 0 0)
  DEBUG(`Benchmarks MODE BARS)
  DEBUG(`Benchmarks LABELS benchmark_names)
  
  ' Comparison chart
  DEBUG(`PLOT Comparison SIZE 800 200 POS 0 400)
  DEBUG(`Comparison TRACES 2 LABELS "Baseline" "Current")
  
  repeat test from 0 to NUM_BENCHMARKS-1
    ' Run benchmark
    DEBUG(`TERM "Running: " benchmark_names[test] "...")
    
    current := run_benchmark(test)
    baseline := benchmark_baselines[test]
    
    ' Update displays
    DEBUG(`Benchmarks DATA `(current))
    DEBUG(`Comparison DATA `(baseline, current))
    
    ' Calculate improvement
    if current > baseline
      improvement := ((current - baseline) * 100) / baseline
      DEBUG(`TERM " +" dec_(improvement) "% improvement\n")
    else
      degradation := ((baseline - current) * 100) / baseline
      DEBUG(`TERM " -" dec_(degradation) "% degradation\n")
    
    ' Detailed analysis for outliers
    if abs(current - baseline) > (baseline / 10)  ' >10% change
      analyze_performance_change(test, baseline, current)

PRI analyze_performance_change(test, baseline, current)
  ' Deep dive into performance changes
  DEBUG(`TERM "\nPerformance Analysis for " benchmark_names[test] ":\n")
  
  ' Profile the code
  DEBUG(`PLOT Profile SIZE 800 300 POS 0 0)
  profile_data := profile_benchmark(test)
  DEBUG(`Profile PACK16 256 @profile_data)
  
  ' Identify hot spots
  hot_spots := identify_hot_spots(@profile_data)
  
  DEBUG(`TERM "Hot spots:\n")
  repeat i from 0 to hot_spots-1
    DEBUG(`TERM "  " function_names[hot_spot_ids[i]])
    DEBUG(`TERM ": " dec_(hot_spot_times[i]) " cycles\n")
  
  ' Cache analysis
  cache_misses := analyze_cache_performance()
  DEBUG(`TERM "Cache misses: " dec_(cache_misses) "\n")
  
  ' Recommendation
  suggest_optimizations(test, @profile_data)
```

### Compliance Testing

Debug windows for regulatory compliance:

```spin2
PUB emc_compliance_test()
  ' EMC compliance testing with debug windows
  DEBUG(`FFT EMC SIZE 800 400 POS 0 0)
  DEBUG(`EMC TITLE "EMC Compliance Test - FCC Part 15")
  DEBUG(`EMC RANGE 30000000 1000000000)  ' 30MHz-1GHz
  DEBUG(`EMC SCALE LOG)
  DEBUG(`EMC REFERENCE FCC_LIMIT_CLASS_B)
  
  ' Test each frequency band
  repeat band from 0 to NUM_BANDS-1
    ' Configure for band
    set_frequency_range(band_starts[band], band_stops[band])
    
    ' Measure emissions
    measure_emissions(@emissions)
    
    ' Display with limit line
    DEBUG(`EMC PACK16 1024 @emissions)
    DEBUG(`EMC LIMIT_LINE @fcc_limits[band])
    
    ' Check compliance
    if check_compliance(@emissions, @fcc_limits[band])
      DEBUG(`TERM "✓ Band " dec_(band) ": PASS\n")
    else
      DEBUG(`TERM "✗ Band " dec_(band) ": FAIL\n")
      identify_emission_sources(@emissions)
    
    ' Capture evidence
    DEBUG(`EMC SCREENSHOT "emc_band_" dec_(band) ".png")
    DEBUG(`EMC EXPORT "emc_band_" dec_(band) ".csv")
  
  ' Generate compliance report
  generate_compliance_report()

PRI generate_compliance_report()
  ' Official compliance documentation
  DEBUG(`TERM "\n============================\n")
  DEBUG(`TERM "EMC COMPLIANCE TEST REPORT\n")
  DEBUG(`TERM "============================\n\n")
  DEBUG(`TERM "Product: " PRODUCT_NAME "\n")
  DEBUG(`TERM "Model: " MODEL_NUMBER "\n")
  DEBUG(`TERM "Serial: " SERIAL_NUMBER "\n")
  DEBUG(`TERM "Test Date: " timestamp() "\n")
  DEBUG(`TERM "Standard: FCC Part 15 Class B\n\n")
  
  ' Results summary
  DEBUG(`TERM "Test Results:\n")
  repeat band from 0 to NUM_BANDS-1
    DEBUG(`TERM "  " dec_(band_starts[band]/1000000) "-")
    DEBUG(`TERM dec_(band_stops[band]/1000000) " MHz: ")
    DEBUG(`TERM compliance_status[band] "\n")
  
  ' Engineer signature
  DEBUG(`TERM "\n_______________________\n")
  DEBUG(`TERM "Test Engineer\n")
  DEBUG(`TERM "Date: " date_string() "\n")
```

## Training and Education

### Interactive Tutorials

Debug windows as teaching tools:

```spin2
PUB tutorial_system() | lesson
  ' Interactive tutorial using debug windows
  DEBUG(`TERM Tutorial SIZE 400 600 POS 0 0)
  DEBUG(`Tutorial CLEAR)
  DEBUG(`Tutorial "P2 DEBUG WINDOW TUTORIAL\n")
  DEBUG(`Tutorial "========================\n\n")
  DEBUG(`Tutorial "Select a lesson:\n")
  
  ' List lessons
  repeat lesson from 0 to NUM_LESSONS-1
    DEBUG(`Tutorial dec_(lesson+1) ". " lesson_titles[lesson] "\n")
  
  repeat
    selection := DEBUG(PC_KEY) - "0"
    
    if selection > 0 and selection <= NUM_LESSONS
      run_lesson(selection - 1)

PRI run_lesson(lesson_id)
  ' Clear and setup for lesson
  DEBUG(`TERM CLEAR)
  DEBUG(`TERM lesson_titles[lesson_id] "\n")
  DEBUG(`TERM "=" * strsize(lesson_titles[lesson_id]) "\n\n")
  
  ' Create windows for lesson
  case lesson_id
    LESSON_SCOPE_BASICS:
      ' Interactive scope lesson
      DEBUG(`SCOPE Training SIZE 400 300 POS 400 0)
      DEBUG(`TERM "This lesson covers SCOPE window basics.\n\n")
      DEBUG(`TERM "The SCOPE window displays analog signals.\n")
      DEBUG(`TERM "Watch the waveform as we change parameters:\n\n")
      
      ' Demonstrate features
      repeat step from 0 to lesson_steps[lesson_id]-1
        DEBUG(`TERM "Step " dec_(step+1) ": " step_descriptions[lesson_id][step] "\n")
        
        execute_lesson_step(lesson_id, step)
        
        ' Wait for user
        DEBUG(`TERM "\nPress SPACE to continue...\n")
        repeat until DEBUG(PC_KEY) == " "
    
    LESSON_LOGIC_ANALYSIS:
      ' Logic analyzer training
      setup_logic_lesson()
      
    LESSON_FFT_SPECTRUM:
      ' Frequency analysis training  
      setup_fft_lesson()

PRI execute_lesson_step(lesson, step)
  ' Execute interactive lesson steps
  case lesson
    LESSON_SCOPE_BASICS:
      case step
        0:  ' Basic waveform
          DEBUG(`Training CLEAR)
          generate_sine_wave(1000, 1000)  ' 1kHz, 1V
          DEBUG(`Training PACK16 512 @waveform)
          
        1:  ' Change frequency
          DEBUG(`TERM "Increasing frequency to 5kHz...\n")
          generate_sine_wave(5000, 1000)
          DEBUG(`Training PACK16 512 @waveform)
          
        2:  ' Add second channel
          DEBUG(`Training CHANNELS 2)
          generate_dual_waveform()
          DEBUG(`Training PACK16 1024 @dual_waveform)
```

### Demo Mode

Automated demonstrations:

```spin2
PUB demo_mode() | demo_step
  ' Automated demo for trade shows
  DEBUG(`TERM Demo SIZE 800 100 POS 0 0)
  DEBUG(`Demo "AUTOMATED DEMONSTRATION MODE")
  
  demo_step := 0
  
  repeat
    case demo_step
      0:  ' Introduction
        show_introduction()
        
      1:  ' Basic debugging
        demonstrate_basic_debug()
        
      2:  ' Advanced features  
        demonstrate_advanced_features()
        
      3:  ' Performance
        demonstrate_performance()
        
      4:  ' Applications
        demonstrate_applications()
    
    demo_step := (demo_step + 1) // 5
    
    ' Check for manual override
    if DEBUG(PC_KEY) == ESC
      return  ' Exit demo mode

PRI demonstrate_advanced_features()
  DEBUG(`Demo CLEAR)
  DEBUG(`Demo "ADVANCED DEBUG FEATURES\n")
  
  ' Multi-window coordination
  DEBUG(`SCOPE Sig1 SIZE 400 200 POS 0 100)
  DEBUG(`FFT Spec1 SIZE 400 200 POS 400 100)
  DEBUG(`LOGIC Dig1 SIZE 400 200 POS 0 300)
  DEBUG(`PLOT Data1 SIZE 400 200 POS 400 300)
  
  ' Synchronized update
  repeat 100
    ' Generate test signal
    generate_complex_signal()
    
    ' Update all windows simultaneously
    DEBUG(`Sig1 PACK16 256 @time_data)
    DEBUG(`Spec1 PACK16 128 @freq_data)
    DEBUG(`Dig1 PACK8 32 @logic_data)
    DEBUG(`Data1 `(measurement))
    
    waitms(50)
  
  DEBUG(`Demo "\n✓ Multi-window coordination demonstrated\n")
```

## Troubleshooting Production Issues

Common production integration issues:

**Problem**: Debug windows in production build
**Solution**: Conditional compilation
```spin2
#ifdef PRODUCTION
  #define DEBUG_OUTPUT(x)  ' No-op in production
#else
  #define DEBUG_OUTPUT(x) DEBUG(x)
#endif
```

**Problem**: Customer sees debug information
**Solution**: Access control
```spin2
' Require password for debug mode
if get_password() == DEBUG_PASSWORD
  enable_debug_windows()
else
  disable_debug_windows()
```

**Problem**: Debug data fills storage
**Solution**: Circular logging
```spin2
' Limit debug log size
if debug_log_size > MAX_LOG_SIZE
  rotate_debug_logs()
```

## Chapter Summary

Production integration transforms debug windows from development tools into production assets. By incorporating debug capabilities into documentation, testing, support, and training workflows, the investment in debugging infrastructure continues to provide value throughout the product lifecycle.

From automated testing to field diagnostics, from compliance validation to customer training, debug windows become an integral part of the production system. The ability to visualize, analyze, and document system behavior doesn't end when development completes—it evolves to support the product in deployment, maintenance, and evolution.

This completes our journey through P2 debug windows, from basic terminal output to production-integrated visualization systems. The debug capabilities we've explored aren't just features—they're a philosophy of observable, understandable, and maintainable embedded systems.

Next, we'll consolidate this knowledge in comprehensive appendices that serve as quick references for all debug window capabilities.