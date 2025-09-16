# Chapter 10: Waveform Analysis - SCOPE and SCOPE_XY Windows

*Your DMM reads 3.3V. Stable, right? Launch the SCOPE window and discover 500mV of ripple, 10kHz oscillation, and periodic dropouts. The average may be 3.3V, but the story is in the shape—the rise time that reveals capacitance, the overshoot that warns of instability, the phase shift that explains why your control loop oscillates. This is where static measurements become dynamic understanding.*

## The Analog Truth

Digital systems pretend the world is binary, but every signal is analog at heart. That clean digital edge? It's a exponential curve fighting parasitic capacitance. That stable power rail? It's a battlefield of switching transients and ground bounce. The SCOPE window reveals this hidden analog reality, turning your P2 into a multi-channel oscilloscope that sees what digital debugging misses.

Consider debugging a switching power supply. Your voltmeter shows 5.00V output. Perfect? The SCOPE window shows the real story: 200mV ripple at the switching frequency, ringing on each transition, and load-dependent phase shifts approaching instability. One measurement lies; the waveform tells the truth.

## SCOPE Window Architecture

The SCOPE window provides dual-mode oscilloscope functionality:

```spin2
CON
  ' SCOPE window capabilities
  MAX_CHANNELS = 4          ' Simultaneous waveforms
  MAX_SAMPLES = 16384       ' Per channel buffer
  TIMEBASE_RANGE = 12       ' 1us to 10s/div
  VOLTAGE_RANGE = 8         ' 10mV to 20V/div
  TRIGGER_TYPES = 6         ' Edge, level, pulse, etc.
  
VAR
  long waveform_buffer[4][1024]
  long trigger_level
  byte trigger_channel
  byte trigger_mode
  
PUB oscilloscope_fundamentals()
  ' Create SCOPE window with full configuration
  DEBUG(`SCOPE Waveform SIZE 800 400 POS 100 100)
  DEBUG(`Waveform CHANNELS 4)
  DEBUG(`Waveform TIMEBASE 100us)                ' 100us per division
  DEBUG(`Waveform VOLTS 1V)                      ' 1V per division
  DEBUG(`Waveform TRIGGER CH1 RISING 2048)       ' Trigger setup
  DEBUG(`Waveform GRID 10 8)                     ' Grid divisions
  DEBUG(`Waveform COLORS YELLOW CYAN MAGENTA GREEN)
  
  ' Multiple display modes
  single_channel_detail()
  multi_channel_comparison()
  xy_mode_analysis()
  persistence_display()
```

## Waveform Capture and Display

### Real-Time Continuous Mode

Stream waveforms continuously:

```spin2
PUB continuous_waveform() | samples[256], sample_count
  ' Configure for continuous streaming
  DEBUG(`SCOPE Stream MODE CONTINUOUS)
  DEBUG(`Stream CHANNELS 2)
  DEBUG(`Stream RATE 1000000)  ' 1MHz sample rate
  
  sample_count := 0
  
  repeat
    ' Capture burst of samples
    repeat i from 0 to 255
      samples[i] := read_adc(0)  ' Channel 1
      waitus(1)  ' 1MHz rate
    
    ' Send to scope
    DEBUG(`Stream PACK16 256 @samples)
    
    ' No trigger - continuous roll
    sample_count += 256
    
    ' Update measurements
    if sample_count // 1024 == 0
      update_measurements(@samples)

PRI update_measurements(buffer) | min, max, avg, rms
  ' Calculate waveform parameters
  min := POSX
  max := NEGX
  avg := 0
  rms := 0
  
  repeat i from 0 to 255
    value := long[buffer][i]
    if value < min
      min := value
    if value > max
      max := value
    avg += value
    rms += value * value
  
  avg /= 256
  rms := sqrt(rms / 256)
  
  ' Display measurements
  DEBUG(`TERM "Vpp: " dec_(max - min) " ")
  DEBUG(`TERM "Vavg: " dec_(avg) " ")
  DEBUG(`TERM "Vrms: " dec_(rms))
```

### Triggered Single-Shot Capture

Capture specific events:

```spin2
PUB triggered_capture() | pretrigger[512], posttrigger[512]
  ' Configure triggered mode
  DEBUG(`SCOPE OneShot MODE SINGLE)
  DEBUG(`OneShot TRIGGER CH1 RISING 2048)
  DEBUG(`OneShot PRETRIGGER 50)  ' 50% pre-trigger
  
  repeat
    ' Continuous pre-trigger buffer
    repeat i from 0 to 511
      pretrigger[i] := read_adc(0)
      if pretrigger[i] > 2048 and pretrigger[i-1] <= 2048
        ' Trigger detected!
        trigger_capture(@posttrigger)
        display_complete_waveform(@pretrigger, @posttrigger)
        quit  ' Single shot
      
      waitus(10)  ' 100kHz sampling

PRI trigger_capture(buffer) | i
  ' Rapid post-trigger capture
  repeat i from 0 to 511
    long[buffer][i] := read_adc(0)
    waitus(10)
    
PRI display_complete_waveform(pre, post)
  ' Combine pre and post trigger
  DEBUG(`SCOPE Complete SAMPLES 1024)
  
  ' Send pre-trigger portion
  DEBUG(`Complete PACK16 512 `(pre))
  
  ' Mark trigger point
  DEBUG(`Complete TRIGGER_MARK)
  
  ' Send post-trigger portion
  DEBUG(`Complete PACK16 512 `(post))
```

### Envelope Mode for Modulated Signals

Capture signal envelopes:

```spin2
PUB envelope_detector() | carrier[1024], envelope_max[128], envelope_min[128]
  ' For AM modulated signals
  DEBUG(`SCOPE Envelope MODE ENVELOPE)
  
  repeat
    ' Capture fast carrier
    repeat i from 0 to 1023
      carrier[i] := read_adc(0)
      
    ' Extract envelope
    repeat i from 0 to 127
      ' Find min/max in each segment
      envelope_max[i] := NEGX
      envelope_min[i] := POSX
      
      repeat j from 0 to 7
        sample := carrier[i*8 + j]
        if sample > envelope_max[i]
          envelope_max[i] := sample
        if sample < envelope_min[i]
          envelope_min[i] := sample
    
    ' Display both envelopes
    DEBUG(`Envelope TRACES 2)
    DEBUG(`Envelope PACK16 128 @envelope_max)
    DEBUG(`Envelope PACK16 128 @envelope_min)
```

## Advanced Triggering

### Pulse Width Triggering

Trigger on specific pulse widths:

```spin2
PUB pulse_width_trigger() | start_time, width, min_width, max_width
  ' Trigger on pulses between 10-20us
  min_width := clkfreq / 100_000   ' 10us
  max_width := clkfreq / 50_000    ' 20us
  
  DEBUG(`SCOPE PulseWidth MODE TRIGGERED)
  DEBUG(`PulseWidth TRIGGER PULSE 10us 20us)
  
  repeat
    ' Wait for rising edge
    waitpeq(SIGNAL_PIN, SIGNAL_PIN, 0)
    start_time := cnt
    
    ' Wait for falling edge
    waitpeq(0, SIGNAL_PIN, 0)
    width := cnt - start_time
    
    ' Check if within range
    if width >= min_width and width <= max_width
      ' Trigger! Capture waveform
      capture_triggered_event()
      
      DEBUG(`TERM "Triggered on " dec_(width * 1_000_000 / clkfreq) "us pulse")

PUB runt_pulse_detector() | normal_level, runt_level
  ' Detect pulses that don't reach full amplitude
  normal_level := 3300  ' 3.3V in millivolts
  runt_level := 2500    ' Threshold for runt
  
  repeat
    ' Monitor for rising edge
    if read_adc(0) > 500  ' Started rising
      peak := 0
      
      ' Track until falling
      repeat while read_adc(0) > 500
        sample := read_adc(0)
        if sample > peak
          peak := sample
      
      ' Check if runt
      if peak < runt_level
        DEBUG(`SCOPE RUNT_DETECTED `(peak))
        capture_runt_event()
```

### Pattern Triggering

Trigger on multi-channel patterns:

```spin2
PUB pattern_trigger() | ch1, ch2, ch3, ch4, pattern
  ' Trigger when channels match pattern
  TRIGGER_PATTERN := %1010  ' CH4=1, CH3=0, CH2=1, CH1=0
  
  DEBUG(`SCOPE Pattern MODE PATTERN_TRIGGER)
  
  repeat
    ' Read all channels
    ch1 := read_adc(0) > 2048
    ch2 := read_adc(1) > 2048
    ch3 := read_adc(2) > 2048
    ch4 := read_adc(3) > 2048
    
    pattern := (ch4 << 3) | (ch3 << 2) | (ch2 << 1) | ch1
    
    if pattern == TRIGGER_PATTERN
      ' Pattern matched - capture all channels
      capture_multichannel()
      DEBUG(`Pattern TRIGGERED hex_(pattern))
```

## SCOPE_XY Mode - Phase and Correlation

### Lissajous Pattern Analysis

Visualize phase relationships:

```spin2
PUB lissajous_display() | x, y, phase_shift, freq_ratio
  ' XY mode for phase measurement
  DEBUG(`SCOPE_XY Phase SIZE 400 400 POS 100 100)
  DEBUG(`Phase MODE XY)
  DEBUG(`Phase RANGE -2048 2048 -2048 2048)
  DEBUG(`Phase PERSIST 100)  ' Persistence for pattern
  
  phase_shift := 0
  freq_ratio := 1
  
  repeat angle from 0 to 359
    ' Generate test signals
    x := 1500 * sin(angle * freq_ratio)
    y := 1500 * sin(angle + phase_shift)
    
    DEBUG(`Phase POINT `(x, y))
    
    ' Vary phase to show pattern changes
    if ina[BUTTON_UP]
      phase_shift := (phase_shift + 1) // 360
      DEBUG(`TERM "Phase: " dec_(phase_shift) " degrees")
    
    if ina[BUTTON_DN]
      phase_shift := (phase_shift - 1) // 360
      
    waitms(10)

PUB measure_phase_shift() | zero_cross_x, zero_cross_y, phase
  ' Measure actual phase between signals
  
  ' Find zero crossings
  repeat until read_adc(0) < 0
  repeat until read_adc(0) >= 0
  zero_cross_x := cnt
  
  repeat until read_adc(1) < 0
  repeat until read_adc(1) >= 0
  zero_cross_y := cnt
  
  ' Calculate phase
  time_diff := zero_cross_y - zero_cross_x
  period := measure_period(0)
  phase := (time_diff * 360) / period
  
  DEBUG(`TERM "Phase shift: " dec_(phase) " degrees")
```

### Component Characteristic Curves

Test component I-V curves:

```spin2
PUB iv_curve_tracer() | voltage, current
  ' Trace current vs voltage
  DEBUG(`SCOPE_XY IV_Curve SIZE 500 500)
  DEBUG(`IV_Curve MODE XY)
  DEBUG(`IV_Curve LABELS "Voltage (V)" "Current (mA)")
  
  repeat voltage from -2000 to 2000 step 10
    ' Apply voltage (via DAC)
    set_dac(voltage)
    waitms(1)  ' Settling time
    
    ' Measure current (via shunt)
    current := read_adc(CURRENT_SENSE)
    current := (current * 1000) / SHUNT_RESISTANCE
    
    ' Plot I-V point
    DEBUG(`IV_Curve POINT `(voltage, current))
    
    ' Identify regions
    if abs(current) > MAX_SAFE_CURRENT
      DEBUG(`TERM "WARNING: Current limit reached")
      quit

PUB capacitor_tester() | test_freq, impedance, phase
  ' Measure capacitor characteristics
  DEBUG(`SCOPE_XY Capacitor SIZE 500 500)
  
  repeat test_freq from 100 to 100000 step 100
    ' Apply test frequency
    generate_sine(test_freq)
    waitms(10)  ' Settle
    
    ' Measure impedance and phase
    impedance := measure_impedance()
    phase := measure_phase()
    
    ' Calculate capacitance
    capacitance := 1 / (2 * PI * test_freq * impedance)
    
    ' Plot frequency response
    DEBUG(`Capacitor POINT `(test_freq, impedance))
    
    ' Check for resonance
    if phase =< 0
      DEBUG(`TERM "Resonance at " dec_(test_freq) "Hz")
```

## Multi-Channel Analysis

### Differential Measurements

Measure between channels:

```spin2
PUB differential_mode() | ch1, ch2, diff, common
  ' Differential and common mode
  DEBUG(`SCOPE Differential CHANNELS 3)
  DEBUG(`Differential LABELS "CH1" "CH2" "DIFF")
  
  repeat
    ch1 := read_adc(0)
    ch2 := read_adc(1)
    
    ' Calculate differential and common
    diff := ch1 - ch2
    common := (ch1 + ch2) / 2
    
    ' Display all three
    DEBUG(`Differential DATA `(ch1, ch2, diff))
    
    ' Measure CMRR
    if common <> 0
      cmrr := 20 * log10(abs(diff) / abs(common))
      DEBUG(`TERM "CMRR: " dec_(cmrr) "dB")

PUB power_supply_monitoring() | v_in, v_out, ripple, efficiency
  ' Monitor power supply performance
  DEBUG(`SCOPE PowerSupply CHANNELS 4)
  DEBUG(`PowerSupply LABELS "Vin" "Vout" "Ripple" "Load")
  
  repeat
    ' Measure all parameters
    v_in := read_adc(VIN_CHANNEL)
    v_out := read_adc(VOUT_CHANNEL)
    i_in := read_adc(IIN_CHANNEL)
    i_out := read_adc(IOUT_CHANNEL)
    
    ' Calculate ripple (peak-to-peak)
    ripple := measure_ripple(VOUT_CHANNEL)
    
    ' Calculate efficiency
    p_in := (v_in * i_in) / 1000
    p_out := (v_out * i_out) / 1000
    
    if p_in > 0
      efficiency := (p_out * 100) / p_in
      
    ' Display all channels
    DEBUG(`PowerSupply DATA `(v_in, v_out, ripple, i_out))
    DEBUG(`TERM "Efficiency: " dec_(efficiency) "%")
```

### Time-Correlated Events

Analyze timing relationships:

```spin2
PUB timing_analysis() | clk_edge, data_edge, setup, hold
  ' Measure setup and hold times
  DEBUG(`SCOPE Timing CHANNELS 2)
  DEBUG(`Timing LABELS "CLK" "DATA")
  DEBUG(`Timing CURSORS ON)
  
  repeat
    ' Wait for clock edge
    waitpeq(CLK_PIN, CLK_PIN, 0)
    clk_edge := cnt
    
    ' Measure data timing
    data_before := read_adc(DATA_CHANNEL)
    waitus(1)
    data_after := read_adc(DATA_CHANNEL)
    
    ' Find data transition
    if data_before <> data_after
      data_edge := cnt
      
      if data_edge < clk_edge
        setup := (clk_edge - data_edge) * 1000 / clkfreq
        DEBUG(`TERM "Setup: " dec_(setup) "ns")
      else
        hold := (data_edge - clk_edge) * 1000 / clkfreq
        DEBUG(`TERM "Hold: " dec_(hold) "ns")
```

## Automated Measurements

### Built-in Measurements

Automatic parameter extraction:

```spin2
PUB auto_measurements() | samples[1024]
  ' Enable automatic measurements
  DEBUG(`SCOPE AutoMeasure MEASUREMENTS ON)
  
  ' Capture waveform
  capture_waveform(@samples, 1024)
  
  ' Calculate all parameters
  vpp := calculate_vpp(@samples, 1024)
  vrms := calculate_vrms(@samples, 1024)
  vavg := calculate_vavg(@samples, 1024)
  frequency := calculate_frequency(@samples, 1024)
  period := calculate_period(@samples, 1024)
  duty := calculate_duty_cycle(@samples, 1024)
  rise_time := calculate_rise_time(@samples, 1024)
  fall_time := calculate_fall_time(@samples, 1024)
  overshoot := calculate_overshoot(@samples, 1024)
  
  ' Display measurement panel
  DEBUG(`TERM "Measurements:")
  DEBUG(`TERM "  Vpp: " dec_(vpp) "mV")
  DEBUG(`TERM "  Vrms: " dec_(vrms) "mV")
  DEBUG(`TERM "  Freq: " dec_(frequency) "Hz")
  DEBUG(`TERM "  Duty: " dec_(duty) "%")
  DEBUG(`TERM "  Rise: " dec_(rise_time) "ns")

PRI calculate_frequency(buffer, count) : freq | crossings, first_cross, last_cross
  ' Count zero crossings
  threshold := calculate_vavg(buffer, count)
  crossings := 0
  first_cross := -1
  
  repeat i from 1 to count-1
    if long[buffer][i-1] < threshold and long[buffer][i] >= threshold
      crossings++
      if first_cross < 0
        first_cross := i
      last_cross := i
  
  if crossings > 1
    ' Calculate frequency from crossing period
    samples_per_period := (last_cross - first_cross) / (crossings - 1)
    freq := SAMPLE_RATE / samples_per_period
```

### Statistical Analysis

Waveform statistics and histograms:

```spin2
PUB waveform_statistics() | histogram[256], total_samples
  ' Build amplitude histogram
  bytefill(@histogram, 0, 256*4)
  total_samples := 0
  
  repeat 10000  ' Collect many samples
    sample := read_adc(0) >> 4  ' Scale to 0-255
    histogram[sample]++
    total_samples++
  
  ' Display histogram
  DEBUG(`PLOT Histogram MODE BARS)
  DEBUG(`Histogram POINTS 256)
  DEBUG(`Histogram PACK32 256 @histogram)
  
  ' Calculate statistics
  mean := 0
  variance := 0
  
  repeat i from 0 to 255
    mean += i * histogram[i]
  mean /= total_samples
  
  repeat i from 0 to 255
    diff := i - mean
    variance += diff * diff * histogram[i]
  variance /= total_samples
  
  std_dev := sqrt(variance)
  
  DEBUG(`TERM "Mean: " dec_(mean))
  DEBUG(`TERM "Std Dev: " dec_(std_dev))
```

## Real-World Applications

### Motor Control Analysis

Debug motor drive systems:

```spin2
PUB motor_analysis() | phases[3], current, speed, position
  ' Three-phase motor monitoring
  DEBUG(`SCOPE Motor CHANNELS 4)
  DEBUG(`Motor LABELS "Phase A" "Phase B" "Phase C" "Current")
  
  repeat
    ' Read three phases
    phases[0] := read_adc(PHASE_A)
    phases[1] := read_adc(PHASE_B)
    phases[2] := read_adc(PHASE_C)
    current := read_adc(CURRENT_SENSE)
    
    ' Display waveforms
    DEBUG(`Motor DATA `(phases[0], phases[1], phases[2], current))
    
    ' Analyze phase relationships
    phase_ab := calculate_phase_shift(phases[0], phases[1])
    phase_bc := calculate_phase_shift(phases[1], phases[2])
    phase_ca := calculate_phase_shift(phases[2], phases[0])
    
    ' Check for problems
    if abs(phase_ab - 120) > 5
      DEBUG(`TERM "WARNING: Phase imbalance AB")
    
    ' Calculate motor speed from phase frequency
    speed := calculate_frequency(@phases[0], 100) * 60 / POLE_PAIRS
    DEBUG(`TERM "Speed: " dec_(speed) " RPM")
```

### Audio System Debugging

Analyze audio quality:

```spin2
PUB audio_analyzer() | left[1024], right[1024], thd, snr
  ' Stereo audio analysis
  DEBUG(`SCOPE Audio CHANNELS 2)
  DEBUG(`Audio LABELS "Left" "Right")
  
  ' Capture stereo audio
  repeat i from 0 to 1023
    left[i] := read_adc(LEFT_CHANNEL)
    right[i] := read_adc(RIGHT_CHANNEL)
    waitus(22)  ' ~44.1kHz
  
  ' Display waveforms
  DEBUG(`Audio PACK16 1024 @left)
  DEBUG(`Audio PACK16 1024 @right)
  
  ' THD measurement
  thd := calculate_thd(@left, 1024)
  DEBUG(`TERM "THD: " dec_(thd * 100) "%")
  
  ' SNR measurement
  snr := calculate_snr(@left, 1024)
  DEBUG(`TERM "SNR: " dec_(snr) "dB")
  
  ' Check phase correlation
  correlation := calculate_correlation(@left, @right, 1024)
  if correlation < 0
    DEBUG(`TERM "Channels out of phase!")
```

## Performance Optimization

### High-Speed Sampling Techniques

Achieve maximum sample rates:

```spin2
PUB burst_sampling() | samples[4096]
  ' Configure for burst capture
  DEBUG(`SCOPE Burst MODE BURST)
  DEBUG(`Burst SAMPLES 4096)
  
  ' Use assembly for max speed
  cognew(@fast_sampler, @samples)
  
  ' Wait for completion
  repeat until sample_done
  
  ' Display captured burst
  DEBUG(`Burst PACK16 4096 @samples)

DAT
fast_sampler    org     0
                mov     ptr, par
                mov     count, ##4096
                
:loop           rdpin   sample, #ADC_PIN
                wrlong  sample, ptr
                add     ptr, #4
                djnz    count, #:loop
                
                mov     sample_done, #1
                cogstop cogid
                
ptr             res     1
count           res     1
sample          res     1
```

## Troubleshooting Guide

Common scope issues and solutions:

**Problem**: Unstable trigger
**Solution**: Adjust trigger level and hysteresis
```spin2
' Add trigger hysteresis
if rising_trigger
  trigger_level_high := trigger_level + HYSTERESIS
  trigger_level_low := trigger_level - HYSTERESIS
```

**Problem**: Aliasing at high frequencies
**Solution**: Increase sample rate or add anti-alias filter
```spin2
' Nyquist criterion - sample > 2x signal frequency
required_sample_rate := signal_frequency * 10  ' 10x oversampling
```

## Chapter Summary

The SCOPE and SCOPE_XY windows transform the P2 into a capable mixed-signal oscilloscope, revealing the analog nature of digital systems and the complex relationships between signals. From basic waveform display to sophisticated phase analysis, from automated measurements to component characterization, these windows provide the insight needed to debug analog and mixed-signal systems.

Whether you're debugging power supplies, analyzing motor control, or characterizing audio systems, the SCOPE windows give you professional measurement capabilities in a microcontroller debug environment. The combination of real-time display, intelligent triggering, and automated measurements makes complex analog debugging accessible.

Next, we'll venture into the frequency domain with FFT and SPECTRO windows, where signals reveal their spectral secrets and time-frequency relationships become visible.