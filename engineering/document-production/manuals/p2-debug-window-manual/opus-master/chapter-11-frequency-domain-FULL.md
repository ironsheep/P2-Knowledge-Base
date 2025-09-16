# Chapter 11: Frequency Domain Analysis - FFT and SPECTRO Windows

*Your ear hears the motor whine. Your scope shows a complex waveform. But what frequencies compose that sound? Which harmonics reveal bearing wear? Where's the 60Hz hum hiding in your sensor data? The FFT and SPECTRO windows transform time-domain confusion into frequency-domain clarity, revealing the spectral fingerprint of every signal. This is where noise becomes information and vibrations tell stories.*

## The Hidden Spectrum

Every signal is a symphony of frequencies, but time-domain views show only the combined result. A square wave isn't just a square wave—it's a fundamental frequency plus odd harmonics at specific amplitudes. That clean sine wave from your function generator? Look closer with FFT and find harmonic distortion, phase noise, and spurious emissions your scope missed.

The frequency domain reveals what time domain obscures. Consider debugging an accelerometer signal. In time domain, it's a noisy mess. Transform it with FFT and suddenly you see: 50Hz from motor vibration, 120Hz from an unbalanced load, 1kHz from gear mesh, and 8kHz from bearing wear. Each frequency tells you exactly what's happening mechanically. The noise was information all along—you just needed the right lens to see it.

## FFT Window Fundamentals

The FFT window provides real-time spectrum analysis:

```spin2
CON
  ' FFT window capabilities
  FFT_SIZES = 7            ' 128 to 8192 points
  WINDOW_FUNCTIONS = 6     ' Rectangular, Hanning, Hamming, etc.
  AVERAGING_MODES = 4      ' None, exponential, peak hold, linear
  SCALE_TYPES = 3          ' Linear, Log, dB
  
VAR
  long time_samples[1024]
  long frequency_bins[512]
  long window_coefficients[1024]
  
PUB spectrum_analyzer_basics()
  ' Create FFT window with configuration
  DEBUG(`FFT Spectrum SIZE 800 400 POS 100 100)
  DEBUG(`Spectrum SAMPLES 1024)                  ' FFT size
  DEBUG(`Spectrum WINDOW HANNING)                ' Window function
  DEBUG(`Spectrum SCALE LOG)                     ' Logarithmic frequency
  DEBUG(`Spectrum MAGNITUDE DB)                  ' dB magnitude scale
  DEBUG(`Spectrum RANGE 0 10000)                 ' 0-10kHz display
  DEBUG(`Spectrum AVERAGING 4)                   ' Average 4 spectrums
  
  ' Capture and analyze
  capture_time_domain()
  apply_window_function()
  compute_fft()
  display_spectrum()
```

## Window Functions and Their Uses

### Selecting the Right Window

Different windows for different measurements:

```spin2
PUB window_function_comparison() | rect[512], hann[512], hamm[512], black[512]
  ' Generate test signal - two tones
  repeat i from 0 to 1023
    signal[i] := 1000 * sin(i * 360 * 1000 / SAMPLE_RATE)  ' 1kHz
    signal[i] += 500 * sin(i * 360 * 1500 / SAMPLE_RATE)   ' 1.5kHz
  
  ' Apply different windows
  apply_rectangular(@signal, @rect, 1024)
  apply_hanning(@signal, @hann, 1024)
  apply_hamming(@signal, @hamm, 1024)
  apply_blackman(@signal, @black, 1024)
  
  ' Display results
  DEBUG(`FFT Rectangular WINDOW NONE)
  DEBUG(`Rectangular PACK16 512 @rect)
  
  DEBUG(`FFT Hanning WINDOW HANNING)
  DEBUG(`Hanning PACK16 512 @hann)
  
  DEBUG(`FFT Hamming WINDOW HAMMING)
  DEBUG(`Hamming PACK16 512 @hamm)
  
  DEBUG(`FFT Blackman WINDOW BLACKMAN)
  DEBUG(`Blackman PACK16 512 @black)
  
  ' Compare characteristics
  DEBUG(`TERM "Rectangular: Best frequency resolution, most leakage")
  DEBUG(`TERM "Hanning: Good general purpose, moderate leakage")
  DEBUG(`TERM "Hamming: Minimizes nearest sidelobe")
  DEBUG(`TERM "Blackman: Best sidelobe suppression, widest mainlobe")

PRI apply_hanning(input, output, size) | coefficient
  ' Hanning window: 0.5 - 0.5*cos(2*pi*n/(N-1))
  repeat n from 0 to size-1
    coefficient := 500 - 500 * cos(n * 360 / (size-1))
    long[output][n] := (long[input][n] * coefficient) / 1000
```

### Dynamic Window Selection

Choose window based on signal characteristics:

```spin2
PUB adaptive_windowing() | signal_type
  ' Analyze signal to select optimal window
  signal_type := analyze_signal_type()
  
  case signal_type
    TRANSIENT:
      ' Rectangular for transients
      DEBUG(`FFT Window WINDOW RECTANGULAR)
      DEBUG(`TERM "Transient detected - using rectangular window")
      
    CONTINUOUS_SINE:
      ' Hanning for continuous tones
      DEBUG(`FFT Window WINDOW HANNING)
      DEBUG(`TERM "Continuous tone - using Hanning window")
      
    NOISE_LIKE:
      ' Flat-top for accurate amplitude
      DEBUG(`FFT Window WINDOW FLATTOP)
      DEBUG(`TERM "Noise signal - using flat-top window")
      
    MULTIPLE_TONES:
      ' Blackman for separation
      DEBUG(`FFT Window WINDOW BLACKMAN)
      DEBUG(`TERM "Multiple tones - using Blackman window")

PRI analyze_signal_type() : type | zero_crossings, peak_count
  ' Simple signal classification
  zero_crossings := count_zero_crossings(@signal_buffer, 1024)
  peak_count := count_peaks(@signal_buffer, 1024)
  variance := calculate_variance(@signal_buffer, 1024)
  
  if zero_crossings < 10
    return TRANSIENT
  elseif peak_count =< 3
    return CONTINUOUS_SINE
  elseif variance > NOISE_THRESHOLD
    return NOISE_LIKE
  else
    return MULTIPLE_TONES
```

## Frequency Resolution and Accuracy

### Bin Resolution Calculations

Understanding frequency bins:

```spin2
PUB frequency_resolution() | bin_width, actual_freq, measured_freq
  ' Resolution depends on sample rate and FFT size
  SAMPLE_RATE := 100_000  ' 100kHz sampling
  FFT_SIZE := 1024        ' 1024-point FFT
  
  bin_width := SAMPLE_RATE / FFT_SIZE  ' 97.65Hz per bin
  
  DEBUG(`TERM "FFT Configuration:")
  DEBUG(`TERM "  Sample rate: " dec_(SAMPLE_RATE) "Hz")
  DEBUG(`TERM "  FFT size: " dec_(FFT_SIZE))
  DEBUG(`TERM "  Bin width: " dec_(bin_width) "Hz")
  DEBUG(`TERM "  Frequency range: 0-" dec_(SAMPLE_RATE/2) "Hz")
  
  ' Test measurement accuracy
  actual_freq := 1234  ' 1234Hz test signal
  
  ' Generate and measure
  generate_test_tone(actual_freq)
  capture_samples(@time_buffer, FFT_SIZE)
  compute_fft(@time_buffer, @freq_buffer)
  
  ' Find peak bin
  peak_bin := find_peak_bin(@freq_buffer, FFT_SIZE/2)
  measured_freq := peak_bin * bin_width
  
  DEBUG(`TERM "Actual: " dec_(actual_freq) "Hz")
  DEBUG(`TERM "Measured: " dec_(measured_freq) "Hz")
  DEBUG(`TERM "Error: " dec_(abs(actual_freq - measured_freq)) "Hz")

PUB interpolated_peak() | peak_bin, y1, y2, y3, interpolated_freq
  ' Parabolic interpolation for better accuracy
  peak_bin := find_peak_bin(@freq_buffer, FFT_SIZE/2)
  
  ' Get adjacent bin magnitudes
  y1 := freq_buffer[peak_bin - 1]
  y2 := freq_buffer[peak_bin]      ' Peak
  y3 := freq_buffer[peak_bin + 1]
  
  ' Parabolic interpolation
  delta := ((y3 - y1) * 1000) / (2 * (2*y2 - y1 - y3))
  interpolated_bin := peak_bin + delta / 1000
  
  interpolated_freq := interpolated_bin * bin_width
  
  DEBUG(`TERM "Interpolated frequency: " dec_(interpolated_freq) "Hz")
```

### Zero-Padding and Resolution Enhancement

Improve frequency display resolution:

```spin2
PUB zero_padding_demo() | original[512], padded[2048]
  ' Capture original signal
  capture_samples(@original, 512)
  
  ' Zero-pad to 4x size
  longmove(@padded, @original, 512)
  longfill(@padded[512], 0, 1536)  ' Add zeros
  
  ' Compute FFTs
  compute_fft(@original, @spectrum_512, 512)
  compute_fft(@padded, @spectrum_2048, 2048)
  
  ' Display both
  DEBUG(`FFT Original POINTS 256)
  DEBUG(`Original PACK16 256 @spectrum_512)
  
  DEBUG(`FFT Padded POINTS 1024)
  DEBUG(`Padded PACK16 1024 @spectrum_2048)
  
  DEBUG(`TERM "Original bins: 256, Padded bins: 1024")
  DEBUG(`TERM "Note: Padding improves display, not actual resolution")
```

## SPECTRO Window - Time-Frequency Analysis

### Spectrogram Display

Visualize frequency content over time:

```spin2
VAR
  long spectrogram_buffer[100][256]  ' 100 time slices, 256 frequency bins
  byte time_index

PUB spectrogram_display() | spectrum[256]
  ' Configure spectrogram
  DEBUG(`SPECTRO Waterfall SIZE 800 400)
  DEBUG(`Waterfall MODE SCROLL)         ' Scrolling display
  DEBUG(`Waterfall FFT_SIZE 512)        ' 512-point FFTs
  DEBUG(`Waterfall OVERLAP 256)         ' 50% overlap
  DEBUG(`Waterfall COLORMAP JET)        ' Jet colormap
  DEBUG(`Waterfall RANGE 0 10000 -60 0) ' Freq and magnitude ranges
  
  repeat
    ' Capture and compute spectrum
    capture_samples(@time_samples, 512)
    apply_window(@time_samples, WINDOW_HANNING)
    compute_fft(@time_samples, @spectrum)
    
    ' Convert to dB
    convert_to_db(@spectrum, 256)
    
    ' Add to spectrogram buffer
    longmove(@spectrogram_buffer[time_index], @spectrum, 256)
    time_index := (time_index + 1) // 100
    
    ' Update display
    DEBUG(`Waterfall LINE @spectrum)
    
    ' 50% overlap for next frame
    longmove(@time_samples, @time_samples[256], 256)

PRI convert_to_db(buffer, size) | magnitude, db
  repeat i from 0 to size-1
    magnitude := long[buffer][i]
    if magnitude > 0
      ' 20*log10(magnitude)
      db := 20 * log10(magnitude) - REFERENCE_LEVEL
      long[buffer][i] := limit(db, -60, 0)  ' Limit to display range
    else
      long[buffer][i] := -60  ' Floor value
```

### Waterfall Persistence

Show signal history with persistence:

```spin2
PUB persistence_spectrogram() | persistence_map[256][256]
  ' 2D persistence map
  wordfill(@persistence_map, 0, 256*256)
  
  DEBUG(`SPECTRO Persistence SIZE 800 600)
  DEBUG(`Persistence MODE PERSIST)
  DEBUG(`Persistence DECAY 10)  ' 10% decay per frame
  
  repeat
    ' Get new spectrum
    capture_and_compute_spectrum(@spectrum)
    
    ' Update persistence map
    repeat freq from 0 to 255
      intensity := spectrum[freq] / 16  ' Scale to 0-255
      
      ' Add to persistence with decay
      repeat old_intensity from 0 to 255
        if persistence_map[freq][old_intensity] > 0
          persistence_map[freq][old_intensity] := 
            persistence_map[freq][old_intensity] * 9 / 10  ' Decay
      
      ' Add new point
      persistence_map[freq][intensity] := 255  ' Full intensity
    
    ' Display persistence map
    DEBUG(`Persistence MAP @persistence_map)
```

## Real-Time Analysis Applications

### Audio Spectrum Analyzer

Professional audio analysis:

```spin2
PUB audio_spectrum_analyzer() | left[1024], right[1024]
  ' Stereo spectrum analyzer
  DEBUG(`FFT AudioLeft SIZE 400 400 POS 0 0)
  DEBUG(`FFT AudioRight SIZE 400 400 POS 400 0)
  
  ' Configure for audio
  DEBUG(`AudioLeft RANGE 20 20000)     ' 20Hz-20kHz
  DEBUG(`AudioLeft SCALE LOG)          ' Log frequency scale
  DEBUG(`AudioLeft WEIGHTING A)        ' A-weighting
  
  repeat
    ' Capture stereo audio at 44.1kHz
    repeat i from 0 to 1023
      left[i] := read_adc(LEFT_IN)
      right[i] := read_adc(RIGHT_IN)
      waitus(22)  ' ~44.1kHz
    
    ' Process both channels
    process_audio_channel(@left, @left_spectrum)
    process_audio_channel(@right, @right_spectrum)
    
    ' Display spectrums
    DEBUG(`AudioLeft PACK16 512 @left_spectrum)
    DEBUG(`AudioRight PACK16 512 @right_spectrum)
    
    ' THD+N measurement
    thd_left := calculate_thd_plus_n(@left_spectrum)
    thd_right := calculate_thd_plus_n(@right_spectrum)
    
    DEBUG(`TERM "THD+N  L: " dec_(thd_left) "%  R: " dec_(thd_right) "%")

PRI process_audio_channel(input, output)
  ' Apply window
  apply_hanning(input, @windowed, 1024)
  
  ' Compute FFT
  compute_fft(@windowed, output)
  
  ' Apply A-weighting
  apply_a_weighting(output, 512)
  
  ' Convert to dB
  convert_to_db(output, 512)
```

### Vibration Analysis

Machine condition monitoring:

```spin2
PUB vibration_monitor() | accel_x[2048], accel_y[2048], accel_z[2048]
  ' 3-axis vibration analysis
  DEBUG(`SPECTRO Vibration SIZE 800 600)
  DEBUG(`Vibration FFT_SIZE 2048)
  DEBUG(`Vibration RANGE 0 1000)  ' 0-1kHz for machinery
  
  ' Baseline measurement
  capture_baseline()
  
  repeat
    ' Capture acceleration data
    repeat i from 0 to 2047
      accel_x[i] := read_accel(X_AXIS)
      accel_y[i] := read_accel(Y_AXIS)
      accel_z[i] := read_accel(Z_AXIS)
      waitus(500)  ' 2kHz sampling
    
    ' Compute spectrums
    compute_fft(@accel_x, @spectrum_x)
    compute_fft(@accel_y, @spectrum_y)
    compute_fft(@accel_z, @spectrum_z)
    
    ' Combine for total vibration
    repeat i from 0 to 1023
      total_vibration[i] := sqrt(spectrum_x[i]**2 + 
                                  spectrum_y[i]**2 + 
                                  spectrum_z[i]**2)
    
    ' Display waterfall
    DEBUG(`Vibration LINE @total_vibration)
    
    ' Detect fault frequencies
    detect_bearing_faults(@total_vibration)
    detect_imbalance(@total_vibration)
    detect_misalignment(@spectrum_x, @spectrum_y)

PRI detect_bearing_faults(spectrum) | bpfo, bpfi, bsf, ftf
  ' Bearing fault frequencies
  BEARING_RPM := 1800
  BALLS := 9
  PITCH_DIAMETER := 40
  BALL_DIAMETER := 12
  CONTACT_ANGLE := 0
  
  ' Calculate fault frequencies
  bpfo := calculate_bpfo(BEARING_RPM, BALLS, PITCH_DIAMETER, BALL_DIAMETER)
  bpfi := calculate_bpfi(BEARING_RPM, BALLS, PITCH_DIAMETER, BALL_DIAMETER)
  bsf := calculate_bsf(BEARING_RPM, PITCH_DIAMETER, BALL_DIAMETER)
  ftf := calculate_ftf(BEARING_RPM, BALLS)
  
  ' Check for peaks at fault frequencies
  if check_peak_at_frequency(spectrum, bpfo) > THRESHOLD
    DEBUG(`TERM "WARNING: Outer race fault detected at " dec_(bpfo) "Hz")
  
  if check_peak_at_frequency(spectrum, bpfi) > THRESHOLD
    DEBUG(`TERM "WARNING: Inner race fault detected at " dec_(bpfi) "Hz")
```

### EMI/RFI Detection

Electromagnetic interference hunting:

```spin2
PUB emi_scanner() | baseline[512], current[512], difference[512]
  ' EMI detection and identification
  DEBUG(`FFT EMI SIZE 800 400)
  DEBUG(`EMI RANGE 0 100000000)  ' 0-100MHz
  DEBUG(`EMI SCALE LOG)
  DEBUG(`EMI PEAK_HOLD ON)
  
  ' Capture baseline with equipment off
  DEBUG(`TERM "Turn off all equipment for baseline...")
  waitms(3000)
  capture_rf_spectrum(@baseline)
  
  DEBUG(`TERM "Turn equipment back on...")
  waitms(3000)
  
  repeat
    ' Capture current spectrum
    capture_rf_spectrum(@current)
    
    ' Calculate difference
    repeat i from 0 to 511
      difference[i] := current[i] - baseline[i]
      
      ' Flag significant increases
      if difference[i] > EMI_THRESHOLD
        frequency := i * BIN_WIDTH
        DEBUG(`EMI MARKER `(frequency) RED)
        identify_emi_source(frequency, difference[i])
    
    ' Update display
    DEBUG(`EMI PACK16 512 @difference)

PRI identify_emi_source(freq, amplitude) | source
  ' Common EMI sources
  case freq
    48_000..52_000:
      source := "Switching power supply (50kHz)"
    13_540..13_580:
      source := "ISM band (13.56MHz)"
    26_900..27_100:
      source := "CB radio (27MHz)"
    2_400_000..2_500_000:
      source := "WiFi/Bluetooth (2.4GHz)"
    
  DEBUG(`TERM "EMI at " dec_(freq) "Hz: " source)
  DEBUG(`TERM "  Amplitude: " dec_(amplitude) "dB above baseline")
```

## Advanced FFT Techniques

### Zoom FFT

High-resolution analysis of narrow bands:

```spin2
PUB zoom_fft(center_freq, span) | decimation, shift_freq
  ' Zoom into specific frequency range
  decimation := SAMPLE_RATE / (span * 2)
  shift_freq := center_freq - (span / 2)
  
  ' Frequency shift and decimate
  repeat i from 0 to 1023
    ' Complex multiply to shift
    shifted_i := samples[i] * cos(i * shift_freq * 360 / SAMPLE_RATE)
    shifted_q := samples[i] * sin(i * shift_freq * 360 / SAMPLE_RATE)
    
    ' Low-pass filter and decimate
    if i // decimation == 0
      decimated[i/decimation] := apply_lpf(shifted_i, shifted_q)
  
  ' FFT on decimated signal
  compute_fft(@decimated, @zoomed_spectrum)
  
  ' Display zoomed spectrum
  DEBUG(`FFT Zoom RANGE `(center_freq - span/2) ` `(center_freq + span/2))
  DEBUG(`Zoom PACK16 512 @zoomed_spectrum)
```

### Cepstrum Analysis

For echo detection and pitch extraction:

```spin2
PUB cepstrum_analysis() | spectrum[512], log_spectrum[512], cepstrum[512]
  ' Compute cepstrum for echo/pitch detection
  
  ' Step 1: FFT
  compute_fft(@time_signal, @spectrum)
  
  ' Step 2: Log magnitude
  repeat i from 0 to 511
    if spectrum[i] > 0
      log_spectrum[i] := log10(spectrum[i]) * 1000
    else
      log_spectrum[i] := -60_000  ' Floor
  
  ' Step 3: Inverse FFT
  compute_ifft(@log_spectrum, @cepstrum)
  
  ' Find peaks in cepstrum
  repeat i from 10 to 256  ' Skip DC area
    if cepstrum[i] > PEAK_THRESHOLD
      ' Peak indicates periodicity
      period_samples := i
      frequency := SAMPLE_RATE / period_samples
      DEBUG(`TERM "Periodic component at " dec_(frequency) "Hz")
```

## Performance Optimization

### Real-Time FFT Processing

Achieve continuous FFT updates:

```spin2
VAR
  long buffer_a[1024], buffer_b[1024]
  byte active_buffer
  long fft_cog

PUB realtime_fft()
  ' Double-buffered FFT processing
  fft_cog := cognew(@fft_engine, @active_buffer)
  
  repeat
    if active_buffer == 0
      ' Fill buffer A while FFT processes B
      capture_samples(@buffer_a, 1024)
      active_buffer := 1
    else
      ' Fill buffer B while FFT processes A
      capture_samples(@buffer_b, 1024)
      active_buffer := 0
    
    ' Display completed FFT
    if fft_complete
      DEBUG(`FFT Realtime PACK16 512 @fft_result)
      fft_complete := FALSE

DAT
fft_engine    ' Assembly FFT for maximum speed
              ' Achieves 1024-point FFT in <1ms
```

## Troubleshooting Guide

Common FFT/SPECTRO issues:

**Problem**: Frequency peaks appear at wrong frequencies
**Solution**: Verify sample rate
```spin2
' Actual sample rate may differ from expected
actual_rate := measure_actual_sample_rate()
bin_width := actual_rate / FFT_SIZE
```

**Problem**: Spectral leakage obscures weak signals
**Solution**: Use appropriate window
```spin2
' Blackman window for maximum sidelobe suppression
apply_blackman_window(@samples)
```

**Problem**: Insufficient frequency resolution
**Solution**: Increase FFT size or use zoom FFT
```spin2
' Double FFT size for double resolution
FFT_SIZE := 2048  ' Was 1024
```

## Chapter Summary

The FFT and SPECTRO windows open the frequency domain to P2 debugging, transforming time-series data into spectral information that reveals hidden patterns, identifies specific frequencies, and tracks changes over time. From audio analysis to vibration monitoring, from EMI detection to machine diagnostics, these windows provide professional spectrum analysis capabilities.

The combination of configurable FFT processing, multiple window functions, and waterfall displays creates a complete frequency analysis toolkit. Whether you're designing audio systems, monitoring machinery, or hunting electromagnetic interference, the frequency domain windows give you the spectral vision needed to see what time domain hides.

Next, we'll explore multi-window coordination, where multiple debug windows work together to provide comprehensive system visibility.