# Chapter 9: Digital Signal Analysis - LOGIC Window Applications

*Your multimeter shows continuity. Your scope shows edges. But where's the protocol? Where's the timing relationship? Where's the state machine visualization? The LOGIC window transforms the P2 into a protocol analyzer, showing not just signals but their meaning. This is where bits become bytes, edges become events, and debugging becomes forensic analysis.*

## Beyond Simple Logic Levels

Traditional debugging shows you high or low, one or zero. But digital systems communicate through patterns—protocols with start bits, addresses, acknowledgments, and checksums. The LOGIC window doesn't just capture these signals; it decodes them, analyzes them, and reveals the conversation happening on your board.

Consider debugging an I2C bus. An oscilloscope shows you rise times and voltage levels. A logic probe confirms activity. But the LOGIC window shows you which device is being addressed, whether it acknowledged, what data was transferred, and if the transaction completed successfully. It's the difference between seeing letters and reading words.

## LOGIC Window Fundamentals

The LOGIC window operates as a multi-channel analyzer with protocol awareness:

```spin2
CON
  ' LOGIC window capabilities
  MAX_CHANNELS = 32         ' Simultaneous signals
  SAMPLE_DEPTH = 16384      ' Samples per channel
  TRIGGER_MODES = 8         ' Trigger configurations
  DECODE_PROTOCOLS = 12     ' Built-in decoders
  
VAR
  long trigger_mask
  long trigger_pattern
  long sample_buffer[512]
  
PUB logic_analyzer_basics()
  ' Create LOGIC window with configuration
  DEBUG(`LOGIC Analyzer SIZE 800 400 POS 100 100)
  DEBUG(`Analyzer CHANNELS 8)                    ' Monitor 8 signals
  DEBUG(`Analyzer LABELS "CLK" "DATA" "CS" "MOSI" "MISO" "INT" "RST" "ERR")
  DEBUG(`Analyzer SAMPLE_RATE 10000000)          ' 10MHz sampling
  DEBUG(`Analyzer TRIGGER PATTERN %00010000)     ' Trigger on bit 4 high
  DEBUG(`Analyzer COLORS GREEN YELLOW RED BLUE CYAN MAGENTA WHITE GRAY)
  
  ' Capture and display
  capture_logic_state()
  decode_protocols()
  measure_timing()
```

## Protocol Decoding and Analysis

### I2C Bus Analysis

Decode I2C transactions in real-time:

```spin2
CON
  I2C_SDA = 8
  I2C_SCL = 9
  
VAR
  byte i2c_buffer[256]
  byte device_address
  byte register_address
  byte data_bytes[32]

PUB i2c_protocol_analyzer() | state, byte_count, current_byte
  ' Configure for I2C analysis
  DEBUG(`LOGIC I2C SIZE 800 300)
  DEBUG(`I2C CHANNELS 2 LABELS "SDA" "SCL")
  DEBUG(`I2C DECODE I2C)  ' Enable I2C decoder
  
  state := IDLE
  byte_count := 0
  
  repeat
    case state
      IDLE:
        if detect_start_condition()
          state := ADDRESS
          DEBUG(`TERM "START detected")
          
      ADDRESS:
        device_address := capture_i2c_byte()
        if device_address & 1
          DEBUG(`TERM "Read from $" hex_(device_address >> 1))
        else
          DEBUG(`TERM "Write to $" hex_(device_address >> 1))
        
        if check_ack()
          state := DATA
        else
          DEBUG(`TERM "NACK - Device not responding")
          state := IDLE
          
      DATA:
        current_byte := capture_i2c_byte()
        data_bytes[byte_count++] := current_byte
        DEBUG(`I2C BYTE hex_(current_byte))
        
        if detect_stop_condition()
          DEBUG(`TERM "STOP - Transaction complete")
          analyze_transaction(@data_bytes, byte_count)
          state := IDLE
          byte_count := 0

PRI detect_start_condition() : detected
  ' SDA falls while SCL high
  if ina[I2C_SCL] and not ina[I2C_SDA]
    detected := true
    
PRI capture_i2c_byte() : value | bit
  ' Capture 8 bits MSB first
  repeat bit from 7 to 0
    waitpeq(1 << I2C_SCL, 1 << I2C_SCL, 0)  ' Wait for SCL high
    value |= ina[I2C_SDA] << bit
    waitpeq(0, 1 << I2C_SCL, 0)             ' Wait for SCL low
  return value
```

### SPI Bus Monitoring

Multi-slave SPI analysis with timing:

```spin2
PUB spi_bus_monitor() | cs_pins, active_slave
  ' Monitor 4-slave SPI bus
  DEBUG(`LOGIC SPI SIZE 800 400)
  DEBUG(`SPI CHANNELS 7)  ' CLK, MOSI, MISO, CS0-3
  DEBUG(`SPI LABELS "CLK" "MOSI" "MISO" "CS0" "CS1" "CS2" "CS3")
  
  cs_pins := %1111000  ' CS pins on bits 3-6
  
  repeat
    ' Detect which slave is selected
    active_slave := !ina[3..6]  ' Active low CS
    
    if active_slave
      DEBUG(`TERM "Slave " dec_(active_slave) " selected")
      
      ' Capture transaction
      capture_spi_transaction(active_slave)
      
      ' Display decoded data
      display_spi_results()
      
PRI capture_spi_transaction(slave) | bit_count, mosi_data, miso_data
  bit_count := 0
  mosi_data := 0
  miso_data := 0
  
  ' Capture while CS is low
  repeat while not ina[3 + slave]
    waitpeq(1 << SPI_CLK, 1 << SPI_CLK, 0)  ' Rising edge
    
    mosi_data := (mosi_data << 1) | ina[SPI_MOSI]
    miso_data := (miso_data << 1) | ina[SPI_MISO]
    bit_count++
    
    waitpeq(0, 1 << SPI_CLK, 0)  ' Falling edge
    
  DEBUG(`LOGIC SPI DATA `(mosi_data, miso_data, bit_count))
```

### UART Stream Decoding

Automatic baud rate detection and decoding:

```spin2
PUB uart_auto_decoder() | baud_rate, bit_time, char
  ' Auto-detect baud rate
  baud_rate := detect_baud_rate()
  bit_time := clkfreq / baud_rate
  
  DEBUG(`LOGIC UART SIZE 800 200)
  DEBUG(`UART CHANNEL 1 LABEL "RX")
  DEBUG(`UART DECODE UART `(baud_rate) 8 N 1)
  
  repeat
    char := receive_uart_byte(bit_time)
    
    ' Display character and hex
    DEBUG(`TERM "'" chr_(char) "' ($" hex_(char) ") ")
    
    ' Decode special sequences
    case char
      $0D: DEBUG(`TERM "[CR]")
      $0A: DEBUG(`TERM "[LF]")
      $1B: decode_escape_sequence()
      other: check_protocol_patterns(char)

PRI detect_baud_rate() : baud | shortest_pulse
  ' Measure shortest pulse width
  shortest_pulse := POSX
  
  repeat 100
    waitpne(ina[RX_PIN], RX_PIN, 0)
    start_time := cnt
    waitpeq(ina[RX_PIN], RX_PIN, 0)
    pulse_width := cnt - start_time
    
    if pulse_width < shortest_pulse
      shortest_pulse := pulse_width
  
  ' Calculate baud from shortest pulse
  baud := clkfreq / shortest_pulse
  
  ' Round to standard baud rate
  case baud
    110..150: return 115200
    200..250: return 230400
    450..550: return 460800
    900..1100: return 921600
    other: return 115200  ' Default
```

## State Machine Visualization

### Finite State Machine Tracking

Visualize state transitions in real-time:

```spin2
VAR
  byte current_state
  byte state_history[256]
  word state_index
  long state_times[16]  ' Time in each state

PUB state_machine_monitor() | pins, new_state
  ' Monitor 4-bit state output
  DEBUG(`LOGIC States SIZE 800 300)
  DEBUG(`States CHANNELS 4 LABELS "S0" "S1" "S2" "S3")
  DEBUG(`States DECODE BINARY)
  
  ' Create state diagram
  DEBUG(`PLOT StateDiagram SIZE 400 300 POS 810 0)
  DEBUG(`StateDiagram MODE XY RANGE 0 15 0 15)
  
  repeat
    pins := ina[STATE_PINS]
    new_state := pins & $F
    
    if new_state <> current_state
      ' Log transition
      log_state_transition(current_state, new_state)
      
      ' Update visualization
      DEBUG(`States MARKER `(state_index) COLOR GREEN)
      DEBUG(`StateDiagram LINE `(current_state, new_state))
      
      ' Track time in state
      state_times[current_state] += cnt - state_enter_time
      state_enter_time := cnt
      
      current_state := new_state
      state_history[state_index++ & $FF] := new_state

PRI log_state_transition(from, to)
  DEBUG(`TERM "State: " hex_(from) " -> " hex_(to))
  
  ' Decode state meaning
  case to
    $0: DEBUG(`TERM " (IDLE)")
    $1: DEBUG(`TERM " (INIT)")
    $2: DEBUG(`TERM " (READY)")
    $4: DEBUG(`TERM " (ACTIVE)")
    $8: DEBUG(`TERM " (ERROR)")
    other: DEBUG(`TERM " (UNKNOWN)")
```

### Protocol State Machines

Track protocol states with timing requirements:

```spin2
PUB usb_state_monitor() | state, j_state, k_state, se0_count
  ' Monitor USB D+/D- for state changes
  DEBUG(`LOGIC USB SIZE 800 400)
  DEBUG(`USB CHANNELS 2 LABELS "D+" "D-")
  
  state := USB_IDLE
  se0_count := 0
  
  repeat
    j_state := ina[D_PLUS]
    k_state := ina[D_MINUS]
    
    case (j_state << 1) | k_state
      %00:  ' SE0 (Single-Ended Zero)
        se0_count++
        if se0_count > 2500  ' 2.5us at 1MHz sampling
          state := USB_RESET
          DEBUG(`USB STATE "RESET")
          
      %01:  ' K state (Idle for LS/FS)
        if state <> USB_IDLE
          state := USB_IDLE
          DEBUG(`USB STATE "IDLE")
        se0_count := 0
        
      %10:  ' J state  
        if state == USB_IDLE
          state := USB_SYNC
          DEBUG(`USB STATE "SYNC")
        se0_count := 0
        
      %11:  ' SE1 (Error)
        state := USB_ERROR
        DEBUG(`USB STATE "ERROR!")
        se0_count := 0
```

## Timing Analysis and Measurements

### Pulse Width and Period Measurement

Measure timing characteristics automatically:

```spin2
VAR
  long pulse_widths[100]
  long pulse_periods[100]
  byte pulse_index

PUB timing_analyzer() | last_edge, this_edge, width
  DEBUG(`LOGIC Timing SIZE 800 300)
  DEBUG(`Timing CHANNELS 4)
  DEBUG(`Timing MEASUREMENTS ON)  ' Enable automatic measurements
  
  ' Manual measurement loop
  repeat
    ' Wait for rising edge
    waitpeq(0, SIGNAL_PIN, 0)
    waitpeq(SIGNAL_PIN, SIGNAL_PIN, 0)
    last_edge := cnt
    
    ' Wait for falling edge
    waitpeq(0, SIGNAL_PIN, 0)
    this_edge := cnt
    
    ' Calculate and store pulse width
    width := this_edge - last_edge
    pulse_widths[pulse_index] := width
    
    ' Wait for next rising edge for period
    waitpeq(SIGNAL_PIN, SIGNAL_PIN, 0)
    this_edge := cnt
    
    ' Calculate period
    pulse_periods[pulse_index] := this_edge - last_edge
    pulse_index := (pulse_index + 1) // 100
    
    ' Display statistics
    display_timing_stats()

PRI display_timing_stats() | min_width, max_width, avg_width
  ' Calculate statistics
  min_width := POSX
  max_width := 0
  avg_width := 0
  
  repeat i from 0 to 99
    if pulse_widths[i] < min_width
      min_width := pulse_widths[i]
    if pulse_widths[i] > max_width
      max_width := pulse_widths[i]
    avg_width += pulse_widths[i]
    
  avg_width /= 100
  
  ' Convert to microseconds
  min_us := min_width * 1_000_000 / clkfreq
  max_us := max_width * 1_000_000 / clkfreq
  avg_us := avg_width * 1_000_000 / clkfreq
  
  DEBUG(`TERM "Pulse Width - Min: " dec_(min_us) "us")
  DEBUG(`TERM " Max: " dec_(max_us) "us")
  DEBUG(`TERM " Avg: " dec_(avg_us) "us")
  
  ' Calculate frequency from period
  if pulse_periods[0] > 0
    frequency := clkfreq / pulse_periods[0]
    DEBUG(`TERM " Freq: " dec_(frequency) "Hz")
```

### Setup and Hold Time Verification

Verify timing requirements are met:

```spin2
PUB setup_hold_checker() | data_time, clock_time, setup, hold
  ' Monitor data vs clock timing
  DEBUG(`LOGIC SetupHold SIZE 800 400)
  DEBUG(`SetupHold CHANNELS 2 LABELS "DATA" "CLK")
  DEBUG(`SetupHold CURSORS ON)  ' Enable measurement cursors
  
  ' Required timing (in nanoseconds)
  REQUIRED_SETUP := 10
  REQUIRED_HOLD := 5
  
  repeat
    ' Wait for data change
    waitpne(ina[DATA_PIN], DATA_PIN, 0)
    data_time := cnt
    
    ' Wait for clock edge
    waitpeq(CLK_PIN, CLK_PIN, 0)
    clock_time := cnt
    
    ' Calculate setup time
    setup := (clock_time - data_time) * 1_000_000_000 / clkfreq
    
    ' Wait for clock to go low
    waitpeq(0, CLK_PIN, 0)
    
    ' Check if data changed (hold violation)
    if ina[DATA_PIN] <> previous_data
      hold := (cnt - clock_time) * 1_000_000_000 / clkfreq
    else
      hold := REQUIRED_HOLD + 1  ' OK
    
    ' Flag violations
    if setup < REQUIRED_SETUP
      DEBUG(`SetupHold VIOLATION "SETUP" `(setup) "ns")
    if hold < REQUIRED_HOLD
      DEBUG(`SetupHold VIOLATION "HOLD" `(hold) "ns")
    
    previous_data := ina[DATA_PIN]
```

## Multi-Signal Correlation

### Bus Transaction Analysis

Correlate multiple signals for complete picture:

```spin2
PUB parallel_bus_analyzer() | address, data, control
  ' 16-bit address, 8-bit data, 4-bit control
  DEBUG(`LOGIC Bus SIZE 800 500)
  DEBUG(`Bus CHANNELS 28)  ' A0-15, D0-7, RD, WR, CS, ALE
  
  repeat
    ' Wait for ALE (Address Latch Enable)
    waitpeq(ALE_PIN, ALE_PIN, 0)
    address := ina[0..15]
    
    ' Wait for RD or WR
    waitpne(RD_PIN | WR_PIN, RD_PIN | WR_PIN, 0)
    
    if not ina[RD_PIN]  ' Read cycle
      data := ina[16..23]
      DEBUG(`Bus READ hex_(address) " -> " hex_(data))
      
    elseif not ina[WR_PIN]  ' Write cycle
      data := ina[16..23]
      DEBUG(`Bus WRITE hex_(address) " <- " hex_(data))
      
    ' Decode address regions
    case address
      $0000..$3FFF:
        DEBUG(`TERM " (ROM)")
      $4000..$7FFF:
        DEBUG(`TERM " (RAM)")
      $8000..$8FFF:
        DEBUG(`TERM " (I/O)")
      other:
        DEBUG(`TERM " (Unmapped)")
```

### Glitch Detection

Find signal integrity issues:

```spin2
VAR
  long glitch_count
  long glitch_timestamps[100]
  
PUB glitch_detector() | stable_time, last_state, min_pulse
  ' Define minimum valid pulse width
  min_pulse := clkfreq / 1_000_000  ' 1 microsecond
  
  DEBUG(`LOGIC Glitch SIZE 800 400)
  DEBUG(`Glitch CHANNELS 8)
  DEBUG(`Glitch TRIGGER GLITCH `(min_pulse))
  
  last_state := ina[0..7]
  stable_time := cnt
  
  repeat
    if ina[0..7] <> last_state
      pulse_width := cnt - stable_time
      
      if pulse_width < min_pulse
        ' Glitch detected!
        glitch_count++
        glitch_timestamps[glitch_count // 100] := cnt
        
        DEBUG(`Glitch MARKER `(cnt) COLOR RED)
        DEBUG(`TERM "GLITCH on pins " bin_(ina[0..7] ^ last_state))
        DEBUG(`TERM " Width: " dec_(pulse_width * 1000 / clkfreq) "ns")
        
        ' Log for analysis
        log_glitch_event(ina[0..7] ^ last_state, pulse_width)
      
      last_state := ina[0..7]
      stable_time := cnt
```

## Advanced Triggering Strategies

### Complex Trigger Conditions

Set up sophisticated trigger scenarios:

```spin2
PUB advanced_triggering() | trigger_state
  ' Sequential trigger - Pattern A then Pattern B
  DEBUG(`LOGIC Advanced SIZE 800 400)
  
  trigger_state := WAIT_FOR_A
  
  repeat
    case trigger_state
      WAIT_FOR_A:
        ' First condition: Address = $1234
        if ina[0..15] == $1234
          trigger_state := WAIT_FOR_B
          arm_time := cnt
          DEBUG(`TERM "Trigger A matched")
          
      WAIT_FOR_B:
        ' Second condition: Write within 100us
        if not ina[WR_PIN]
          if (cnt - arm_time) < (clkfreq / 10_000)
            ' Trigger!
            capture_buffer()
            DEBUG(`LOGIC TRIGGERED)
            trigger_state := TRIGGERED
          else
            ' Timeout - rearm
            trigger_state := WAIT_FOR_A
            
      TRIGGERED:
        ' Analyze captured data
        analyze_trigger_buffer()
        
        ' Rearm after analysis
        if ina[REARM_PIN]
          trigger_state := WAIT_FOR_A

PUB edge_counting_trigger() | edge_count, target_edges
  ' Trigger after N edges
  target_edges := 1000
  edge_count := 0
  
  repeat
    ' Count edges
    waitpne(ina[SIGNAL_PIN], SIGNAL_PIN, 0)
    edge_count++
    
    if edge_count >= target_edges
      ' Trigger and capture
      DEBUG(`LOGIC TRIGGER "Edge count reached")
      capture_and_analyze()
      edge_count := 0
```

## Real-World Applications

### Embedded System Debugging

Debug complex embedded communications:

```spin2
PUB embedded_debug_suite()
  ' Set up multi-protocol monitoring
  cognew(@i2c_monitor, @i2c_stack)
  cognew(@spi_monitor, @spi_stack)
  cognew(@uart_monitor, @uart_stack)
  cognew(@gpio_monitor, @gpio_stack)
  
  ' Main analysis loop
  repeat
    ' Check for protocol errors
    if i2c_errors + spi_errors + uart_errors > 0
      DEBUG(`TERM "Protocol errors detected!")
      diagnose_communication_issues()
    
    ' Monitor system state
    if ina[SYSTEM_STATE] <> last_state
      DEBUG(`TERM "System state change: " hex_(ina[SYSTEM_STATE]))
      last_state := ina[SYSTEM_STATE]
    
    ' Performance metrics
    calculate_bus_utilization()
    check_timing_margins()
```

### Production Test Fixtures

Automated testing with LOGIC window:

```spin2
PUB production_test() : passed | test_vector, expected, actual
  passed := true
  
  ' Apply test vectors
  repeat test_vector from 0 to NUM_VECTORS-1
    ' Set inputs
    outa[INPUT_PINS] := test_vectors[test_vector]
    waitms(1)  ' Settling time
    
    ' Capture outputs
    actual := ina[OUTPUT_PINS]
    expected := expected_outputs[test_vector]
    
    ' Compare and log
    if actual <> expected
      passed := false
      DEBUG(`LOGIC TEST_FAIL VECTOR `(test_vector))
      DEBUG(`TERM "Expected: " bin_(expected))
      DEBUG(`TERM "Actual: " bin_(actual))
      DEBUG(`TERM "Diff: " bin_(expected ^ actual))
    else
      DEBUG(`LOGIC TEST_PASS VECTOR `(test_vector))
  
  ' Final result
  if passed
    DEBUG(`TERM "ALL TESTS PASSED")
    outa[PASS_LED] := 1
  else
    DEBUG(`TERM "TEST FAILED")
    outa[FAIL_LED] := 1
```

## Performance Optimization

### High-Speed Sampling

Achieve maximum sampling rates:

```spin2
DAT
high_speed_sampler
              org       0
              
sample_loop   mov       sample, ina        ' Read all pins
              wrlong    sample, buffer_ptr ' Store sample
              add       buffer_ptr, #4     ' Advance pointer
              cmp       buffer_ptr, buffer_end wz
        if_z  mov       buffer_ptr, buffer_start  ' Wrap
              
              djnz      count, #sample_loop
              
              ' Signal completion
              wrlong    one, done_flag
              jmp       #sample_loop
              
sample        long      0
buffer_ptr    long      0
buffer_start  long      0
buffer_end    long      0
count         long      0
done_flag     long      0
one           long      1

PUB launch_high_speed_capture(samples)
  buffer_start := @capture_buffer
  buffer_end := buffer_start + (samples * 4)
  buffer_ptr := buffer_start
  count := samples
  done_flag := @capture_done
  
  cognew(@high_speed_sampler, 0)
  
  ' Wait for capture
  repeat until capture_done
  
  ' Display results
  DEBUG(`LOGIC HighSpeed PACK8 `(samples) @capture_buffer)
```

## Troubleshooting Guide

### Common Issues and Solutions

**Problem**: Missing pulses or edges
**Solution**: Increase sample rate
```spin2
' Too slow - misses short pulses
DEBUG(`LOGIC SAMPLE_RATE 1000)  ' 1kHz

' Better - catches microsecond pulses  
DEBUG(`LOGIC SAMPLE_RATE 1000000)  ' 1MHz
```

**Problem**: Protocol decode errors
**Solution**: Verify signal levels and timing
```spin2
' Add hysteresis for noisy signals
if (ina[SIGNAL] > HIGH_THRESHOLD) and (last_state == LOW)
  state := HIGH
elseif (ina[SIGNAL] < LOW_THRESHOLD) and (last_state == HIGH)
  state := LOW
```

**Problem**: Trigger never fires
**Solution**: Verify trigger conditions
```spin2
' Debug trigger setup
DEBUG(`TERM "Trigger armed:")
DEBUG(`TERM " Pattern: " bin_(trigger_pattern))
DEBUG(`TERM " Mask: " bin_(trigger_mask))
DEBUG(`TERM " Current: " bin_(ina & trigger_mask))
```

## Chapter Summary

The LOGIC window transforms the P2 into a professional logic analyzer, capable of protocol decoding, state machine visualization, timing analysis, and multi-signal correlation. By combining high-speed sampling with intelligent triggering and real-time analysis, you can debug complex digital systems with the same precision as dedicated test equipment.

From I2C transactions to glitch detection, from state machines to timing verification, the LOGIC window provides the visibility needed to understand not just what your signals are doing, but what they mean. This isn't just logic analysis—it's system comprehension.

Next, we'll explore the SCOPE windows, where analog signals reveal their secrets through waveform analysis and phase relationships.