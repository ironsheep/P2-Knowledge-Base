# Chapter 7: Packed Data Revolution - 16× Compression

*Your oscilloscope display crawls at 2 frames per second. Your logic analyzer drops samples. Your data logger chokes on the stream. Sound familiar? You're transmitting data the wrong way—sending human-readable text when you should be sending packed binary. This chapter transforms your debug performance from slideshow to real-time.*

## The Bandwidth Crisis

Every time you send `DEBUG(udec(value), " ")`, you're wasting 80% of your bandwidth. A single 16-bit number becomes 5-7 ASCII characters plus delimiters—that's 7 bytes to transmit 2 bytes of actual data. When you're debugging a 1024-sample waveform, that inefficiency multiplies into seconds of delay and megabytes of waste.

The P2's packed data formats solve this crisis with surgical precision. Instead of converting binary to text, transmitting text, then converting back to binary for display, packed formats maintain binary efficiency throughout the pipeline. The result? Up to 32× compression for digital signals, 16× for analog samples, and the difference between unusable and professional debugging.

## Understanding Packed Formats

The P2 provides seven packed data formats, each optimized for specific data types and ranges:

```spin2
CON
  ' Packed format compression ratios
  PACK1_RATIO = 32   ' 1 bit per sample - digital signals
  PACK2_RATIO = 16   ' 2 bits per sample - 4-state logic
  PACK4_RATIO = 8    ' 4 bits per sample - hex digits
  PACK8_RATIO = 4    ' 8 bits per sample - bytes
  PACK16_RATIO = 2   ' 16 bits per sample - words
  PACK32_RATIO = 1   ' 32 bits per sample - longs (no compression)
  
VAR
  long waveform[1024]
  byte digital_samples[128]  ' 1024 bits packed

PUB compression_demonstration() | start_time, text_time, packed_time
  ' Generate test waveform
  repeat i from 0 to 1023
    waveform[i] := 2048 + 1000 * sin(i * 360 / 64)
  
  ' Method 1: Traditional text transmission (SLOW)
  start_time := cnt
  repeat i from 0 to 1023
    DEBUG(udec(waveform[i]), " ")
  text_time := cnt - start_time
  
  ' Method 2: Packed binary transmission (FAST)
  start_time := cnt
  DEBUG(`PLOT Waveform PACK16 1024 @waveform)
  packed_time := cnt - start_time
  
  ' Display performance improvement
  DEBUG(`TERM Results)
  DEBUG("Text transmission: ", udec(text_time / 80_000), "ms")
  DEBUG("Packed transmission: ", udec(packed_time / 80_000), "ms")
  DEBUG("Speedup: ", udec(text_time / packed_time), "x faster")
```

## Format Selection Strategy

Choosing the optimal packed format requires understanding your data's characteristics:

### PACK1 - Digital Signal Streams
Perfect for digital logic, GPIO states, and binary sensors. Each byte carries 8 samples:

```spin2
PUB monitor_gpio_bank() | gpio_states[4]
  ' Pack 32 GPIO pins into 4 bytes
  repeat
    repeat i from 0 to 3
      gpio_states[i] := 0
      repeat bit from 0 to 7
        gpio_states[i] |= (ina[i*8 + bit] & 1) << bit
    
    ' Transmit 32 pins in just 4 bytes!
    DEBUG(`LOGIC GPIOs PACK1 32 @gpio_states)
    waitms(10)  ' 100Hz update rate with minimal bandwidth
```

### PACK2 - Multi-State Logic
Ideal for I2C (SDA/SCL), quadrature encoders, or any 4-state system:

```spin2
PUB track_i2c_bus() | i2c_samples[256]
  ' Each sample: Bit1=SDA, Bit0=SCL
  ' Values: 0=%00 (both low), 1=%01 (clock high), 2=%10 (data high), 3=%11 (both high)
  
  repeat i from 0 to 1023
    sample := (ina[SDA_PIN] << 1) | ina[SCL_PIN]
    i2c_samples[i>>2] |= sample << ((i & 3) * 2)
  
  ' 1024 samples in 256 bytes
  DEBUG(`LOGIC I2C PACK2 1024 @i2c_samples)
```

### PACK4 - Nibble Data
Excellent for hex displays, BCD values, or 16-level measurements:

```spin2
PUB visualize_16_level_adc() | samples[128]
  ' 4-bit ADC or reduced precision for speed
  
  repeat i from 0 to 511
    level := read_adc() >> 8  ' Reduce 12-bit to 4-bit
    samples[i>>1] |= level << ((i & 1) * 4)
  
  ' 512 samples in 128 longs
  DEBUG(`PLOT Levels PACK4 512 @samples)
```

### PACK8 - Byte Streams
Standard for 8-bit data, audio samples, or serial streams:

```spin2
PUB stream_audio_8bit() | audio_buffer[256]
  ' 8-bit audio at 8kHz
  
  repeat
    ' Fill buffer with ADC samples
    repeat i from 0 to 255
      audio_buffer[i] := read_adc() >> 4  ' 12-bit to 8-bit
    
    ' Stream 256 samples efficiently
    DEBUG(`SCOPE Audio PACK8 256 @audio_buffer)
    ' Automatic timing achieves steady 8kHz
```

### PACK16 - High-Resolution Data
For precision measurements, 16-bit ADCs, or signed values:

```spin2
PUB precision_oscilloscope() | samples[512]
  ' 16-bit resolution oscilloscope
  
  ' Configure for triggered capture
  arm_trigger(LEVEL_TRIGGER, 2048)
  
  ' Capture burst
  repeat i from 0 to 511
    samples[i] := read_adc_16bit()
  
  ' Display with full resolution
  DEBUG(`SCOPE Precision PACK16 512 @samples)
  
  ' Calculate and display statistics
  analyze_waveform(@samples, 512)
```

## Advanced Packing Techniques

### Dynamic Format Selection

Adapt compression based on data characteristics:

```spin2
PUB adaptive_compression() | data[1024], format, range
  ' Analyze data range
  min_val := POSX
  max_val := NEGX
  
  repeat i from 0 to 1023
    if data[i] < min_val
      min_val := data[i]
    if data[i] > max_val
      max_val := data[i]
  
  range := max_val - min_val
  
  ' Select optimal format
  case
    range < 2:
      send_pack1(@data, 1024)      ' Binary
    range < 4:
      send_pack2(@data, 1024)      ' 2-bit
    range < 16:
      send_pack4(@data, 1024)      ' 4-bit
    range < 256:
      send_pack8(@data, 1024)      ' 8-bit
    other:
      send_pack16(@data, 1024)     ' 16-bit
```

### Delta Compression

For slowly changing signals, transmit differences:

```spin2
PUB delta_encoding() | samples[1024], deltas[1024], previous
  ' Compute deltas
  previous := samples[0]
  deltas[0] := samples[0]  ' First sample absolute
  
  repeat i from 1 to 1023
    deltas[i] := samples[i] - previous
    previous := samples[i]
  
  ' Most deltas fit in 8 bits even if samples are 16-bit
  if max_delta < 128
    DEBUG(`PLOT Deltas PACK8 1024 @deltas)
  else
    DEBUG(`PLOT Deltas PACK16 1024 @deltas)
```

### Multi-Channel Packing

Interleave multiple signals efficiently:

```spin2
PUB four_channel_packed() | ch1[256], ch2[256], ch3[256], ch4[256], packed[1024]
  ' Interleave 4 channels into single stream
  repeat i from 0 to 255
    packed[i*4] := ch1[i]
    packed[i*4+1] := ch2[i]
    packed[i*4+2] := ch3[i]
    packed[i*4+3] := ch4[i]
  
  ' Send as single burst
  DEBUG(`SCOPE_XY Quad PACK16 1024 @packed CHANNELS 4)
```

## Performance Optimization Patterns

### Double Buffering for Continuous Streaming

Eliminate gaps in data transmission:

```spin2
VAR
  long buffer_a[512], buffer_b[512]
  long active_buffer
  byte buffer_select

PUB continuous_streaming()
  cognew(@sampler_cog, @active_buffer)
  
  repeat
    if buffer_select
      active_buffer := @buffer_a
      waitms(1)  ' Let sampler switch
      DEBUG(`SCOPE Stream PACK16 512 @buffer_b)
    else
      active_buffer := @buffer_b
      waitms(1)
      DEBUG(`SCOPE Stream PACK16 512 @buffer_a)
    
    buffer_select ^= 1

DAT
sampler_cog
  ' Assembly sampling routine fills active buffer
  ' Achieves gap-free streaming at maximum rates
```

### Bandwidth Budget Planning

Calculate your bandwidth requirements:

```spin2
PUB calculate_bandwidth(samples_per_sec, bits_per_sample) : bytes_per_sec
  ' Account for protocol overhead
  bytes_per_sec := samples_per_sec * bits_per_sample / 8
  
  ' Add DEBUG protocol overhead (~10%)
  bytes_per_sec := bytes_per_sec * 110 / 100
  
  ' Compare to available bandwidth
  if bytes_per_sec > 230_400  ' 2Mbaud practical limit
    DEBUG("WARNING: Bandwidth exceeded, reduce sample rate or precision")
    
  return bytes_per_sec

PUB optimize_parameters() | rate, format
  ' Find optimal combination
  repeat rate from 1000 to 100_000 step 1000
    repeat format from 1 to 16
      bandwidth := calculate_bandwidth(rate, format)
      if bandwidth <= 230_400
        DEBUG("Rate: ", udec(rate), "Hz, Format: PACK", udec(format))
```

## Real-World Applications

### High-Speed Data Logger

```spin2
VAR
  long log_buffer[8192]  ' 32KB buffer
  long write_index
  long read_index
  byte logging_active

PUB data_logger_init()
  ' Configure high-speed logging
  logging_active := TRUE
  cognew(@logger_engine, @log_buffer)
  
  ' Start display update loop
  repeat while logging_active
    if write_index <> read_index
      samples := (write_index - read_index) & $1FFF
      if samples >= 512
        DEBUG(`PLOT Logger PACK16 512 @log_buffer[read_index])
        read_index := (read_index + 512) & $1FFF
    
    if ina[STOP_PIN]
      logging_active := FALSE

DAT
logger_engine
  ' Assembly routine for maximum speed sampling
  ' Achieves 1MHz sample rate with 16-bit resolution
```

### Protocol Analyzer with Compression

```spin2
PUB uart_analyzer() | bit_samples[16], byte_count
  ' Capture UART at 16x oversampling
  
  repeat
    ' Wait for start bit
    waitpeq(0, UART_PIN, 0)
    
    ' Sample 10 bits (start + 8 data + stop) at 16x
    repeat bit from 0 to 9
      sample := 0
      repeat oversample from 0 to 15
        waitus(bit_time / 16)
        sample := (sample << 1) | ina[UART_PIN]
      bit_samples[bit] := sample
    
    ' Send compressed samples for analysis
    DEBUG(`LOGIC UART PACK16 10 @bit_samples)
    
    ' Extract and display decoded byte
    byte_val := decode_uart(@bit_samples)
    DEBUG(`TERM "Byte: " hex_(byte_val))
```

## Troubleshooting Packed Data

### Common Issues and Solutions

**Problem**: Display shows garbage or wrong values
**Solution**: Verify format matches data size
```spin2
' WRONG: 16-bit data with 8-bit format
DEBUG(`PLOT Signal PACK8 512 @word_array)  ' Will show only low bytes

' CORRECT: Match format to data
DEBUG(`PLOT Signal PACK16 512 @word_array)
```

**Problem**: Irregular update rates
**Solution**: Use consistent timing
```spin2
PUB steady_updates() | next_time
  next_time := cnt
  
  repeat
    ' Fixed interval regardless of processing time
    waitcnt(next_time += 80_000_000 / UPDATE_RATE)
    DEBUG(`SCOPE Signal PACK16 256 @samples)
```

**Problem**: Buffer overruns
**Solution**: Implement flow control
```spin2
VAR
  byte ready_flag

PUB controlled_streaming()
  repeat
    if ready_flag
      DEBUG(`PLOT Data PACK16 1024 @buffer)
      ready_flag := FALSE
    else
      ' Skip frame rather than corrupt
      DEBUG(`TERM "Frame dropped")
```

## Performance Metrics and Limits

Understanding the actual performance gains:

| Format | Bits/Sample | Compression | Max Sample Rate | Bandwidth Used |
|--------|------------|-------------|-----------------|----------------|
| Text   | 56 (avg)   | 0.14×       | 4 kHz          | 230 kbps      |
| PACK1  | 1          | 32×         | 230 kHz        | 230 kbps      |
| PACK2  | 2          | 16×         | 115 kHz        | 230 kbps      |
| PACK4  | 4          | 8×          | 57 kHz         | 230 kbps      |
| PACK8  | 8          | 4×          | 28 kHz         | 230 kbps      |
| PACK16 | 16         | 2×          | 14 kHz         | 230 kbps      |

These rates assume 2Mbaud serial connection. USB or network connections can achieve even higher rates.

## Chapter Summary

Packed data formats transform the P2's debug capabilities from a development convenience to a professional instrumentation platform. By choosing the right format for your data, implementing proper buffering strategies, and understanding bandwidth limits, you can achieve real-time visualization of signals that would overwhelm traditional text-based debugging.

The 16× compression isn't just a number—it's the difference between seeing your system's behavior and missing critical events. Whether you're debugging high-speed protocols, logging sensor data, or creating professional test equipment, packed formats provide the performance foundation for serious debugging work.

Next, we'll explore how the PLOT window leverages these packed formats to create professional data visualizations that rival dedicated instruments.