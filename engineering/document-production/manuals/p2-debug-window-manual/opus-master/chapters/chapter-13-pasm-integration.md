# Chapter 13: PASM Assembly Integration

*Your Spin2 code calls DEBUG. Clear, simple, effective. But what about that critical assembly driver running in another cog? That interrupt handler executing in nanoseconds? That hand-optimized signal processing routine? PASM assembly integration brings debug visibility to the metal, where cycles matter and every instruction counts. This is debugging at the speed of silicon.*

## Assembly-Level Debug Reality

Assembly code runs where high-level languages fear to tread—interrupt service routines measured in nanoseconds, bit-banged protocols at 100MHz, signal processing that consumes every cycle. Traditional debugging here means toggling pins and counting cycles on an oscilloscope. But P2's DEBUG integration in PASM changes everything. Now your assembly code can stream data to debug windows without destroying the timing it worked so hard to achieve.

Consider a high-speed SPI driver running at 50MHz. Adding traditional debug output would destroy the timing. But PASM DEBUG commands execute in deterministic time, streaming data to windows without breaking the protocol. You see the data being shifted, the clock transitions, the chip select timing—all while the driver maintains perfect SPI timing. This isn't debugging that interferes; it's debugging that observes.

## PASM DEBUG Architecture

```spin2
DAT
              org       0
              
' PASM debug configuration
DEBUG_PIN     long      63              ' Debug serial pin
DEBUG_BAUD    long      2_000_000       ' 2Mbaud debug rate
DEBUG_MODE    long      %0001           ' Async serial mode

' Debug from assembly
asm_debug     mov       debug_val, counter
              call      #debug_dec      ' Send decimal value
              
              mov       debug_val, state
              call      #debug_hex      ' Send hex value
              
              ' Direct debug instruction
              debug     ("Counter: ", udec(counter), " State: ", uhex(state))
              
              ' Continue normal execution
              jmp       #main_loop

' Debug output routines
debug_dec     ' Convert to decimal and send
              mov       digit_count, #10
.dec_loop     ' ... decimal conversion ...
              call      #debug_char
              djnz      digit_count, #.dec_loop
              ret

debug_hex     ' Convert to hex and send
              mov       nibble_count, #8
.hex_loop     ' ... hex conversion ...
              call      #debug_char
              djnz      nibble_count, #.hex_loop
              ret

debug_char    ' Send single character
              wypin     debug_val, #DEBUG_PIN
              waitx     bit_time
              ret
```

## Deterministic Debug Timing

### Cycle-Accurate Debug Points

Debug without disrupting timing:

```spin2
DAT
high_speed_driver
              org       0
              
' Critical timing loop - 50MHz operation
critical_loop
              ' Read input - 2 cycles
              testp     #INPUT_PIN wc
              
              ' Process - 4 cycles
              rcl       shift_reg, #1
              
              ' Debug without breaking timing - 2 cycles
              wxpin     shift_reg, #DEBUG_STREAM
              
              ' Output - 2 cycles
              drvl      #OUTPUT_PIN
              
              ' Loop - 2 cycles
              djnz      bit_count, #critical_loop
              
              ' Total: 12 cycles = 150MHz/12 = 12.5MHz
              ' Debug integrated with zero timing impact

PUB monitor_driver()
  ' Configure streaming debug pin
  DEBUG(`LOGIC Driver SIZE 800 400)
  DEBUG(`Driver STREAM_PIN 48)  ' Hardware streaming
  
  ' Driver runs at full speed while streaming
  coginit(DRIVER_COG, @high_speed_driver, @parameters)
  
  ' Display streamed data
  repeat
    DEBUG(`Driver PACK32 256 STREAM)  ' Hardware captured
```

### Debug FIFO Management

Buffer debug data for burst transmission:

```spin2
DAT
fifo_debug
              org       0
              
' Debug FIFO configuration
DEBUG_FIFO    long      $0000_0000      ' FIFO buffer (16 longs)
fifo_head     long      0
fifo_tail     long      0
fifo_count    long      0

' Main processing loop
process_loop
              ' Time-critical processing
              call      #process_data
              
              ' Queue debug data (2 cycles only)
              wrlong    result, fifo_ptr
              incmod    fifo_head, #15
              
              ' Continue immediately
              jmp       #process_loop

' Background debug transmitter (runs between processing)
debug_sender
              ' Check for queued data
              cmp       fifo_head, fifo_tail wz
        if_z  jmp       #debug_sender
              
              ' Send queued debug data
              rdlong    debug_val, fifo_ptr
              call      #send_debug
              incmod    fifo_tail, #15
              
              jmp       #debug_sender

' Parallel execution
PUB launch_debug_system()
  ' Start processor in one cog
  coginit(PROCESSOR_COG, @process_loop, @data)
  
  ' Start debug sender in another
  coginit(DEBUG_COG, @debug_sender, @DEBUG_FIFO)
  
  ' Monitor debug output
  repeat
    DEBUG(`PLOT Processing FIFO_DEPTH `(fifo_count))
```

## Register and State Visualization

### Live Register Display

Watch registers change in real-time:

```spin2
DAT
register_monitor
              org       0
              
' Debug register bank
monitor_loop
              ' Send all key registers
              debug     ("REGS A:", uhex(reg_a), 
                        " B:", uhex(reg_b),
                        " C:", uhex(reg_c),
                        " X:", uhex(reg_x),
                        " Y:", uhex(reg_y),
                        " Z:", uhex(reg_z))
              
              ' Send flags
              debug     ("FLAGS C:", ubin(c_flag),
                        " Z:", ubin(z_flag),
                        " INT:", ubin(int_state))
              
              ' Continue execution
              jmp       #main_code

PUB register_dashboard()
  ' Create register display
  DEBUG(`TERM Registers SIZE 400 300 POS 0 0)
  DEBUG(`Registers CLEAR)
  DEBUG(`Registers GOTOXY 0 0)
  
  ' Flag visualization
  DEBUG(`LOGIC Flags SIZE 400 100 POS 0 300)
  DEBUG(`Flags CHANNELS 8 LABELS "C" "Z" "N" "V" "I1" "I2" "I3" "CT")
  
  ' Real-time update
  repeat
    ' Registers update automatically from PASM
    ' Flags shown graphically
    flag_byte := get_flag_byte()
    DEBUG(`Flags PACK8 1 @flag_byte)
```

### Stack Tracking

Monitor stack operations:

```spin2
DAT
stack_monitor
              org       0
              
' Stack instrumentation
push_debug    
              ' Before push
              debug     ("PUSH ", uhex(x), " SP:", udec(stack_ptr))
              
              ' Actual push
              alts      stack_ptr, #stack_base
              mov       0-0, x
              add       stack_ptr, #1
              
              ' After push
              debug     ("SP->", udec(stack_ptr))
              ret

pop_debug
              ' Before pop
              debug     ("POP SP:", udec(stack_ptr))
              
              ' Actual pop
              sub       stack_ptr, #1
              altd      stack_ptr, #stack_base
              mov       x, 0-0
              
              ' After pop
              debug     (" ->", uhex(x), " SP:", udec(stack_ptr))
              ret

PUB stack_visualization()
  ' Stack display window
  DEBUG(`PLOT Stack SIZE 200 600 POS 600 0)
  DEBUG(`Stack MODE BARS)
  DEBUG(`Stack RANGE 0 32)
  
  ' Stack operations log
  DEBUG(`TERM StackOps SIZE 400 200 POS 0 400)
  
  ' Monitor stack depth
  repeat
    depth := read_stack_depth()
    DEBUG(`Stack `(depth))
    
    ' Warn on overflow/underflow
    if depth > 30
      DEBUG(`StackOps "WARNING: Stack near full!")
    elseif depth < 2
      DEBUG(`StackOps "WARNING: Stack near empty!")
```

## Interrupt and Event Debugging

### Interrupt Service Visualization

Debug interrupts without disrupting them:

```spin2
DAT
interrupt_handler
              org       0
              
' Interrupt entry point
isr_entry
              ' Timestamp interrupt (2 cycles)
              getct     isr_timestamp
              
              ' Save context (6 cycles)
              mov       save_a, reg_a
              mov       save_b, reg_b
              mov       save_c, reg_c
              
              ' Debug interrupt entry (2 cycles)
              wxpin     isr_timestamp, #ISR_DEBUG_PIN
              
              ' Process interrupt
              call      #handle_interrupt
              
              ' Debug interrupt exit (2 cycles)
              wxpin     ##$FFFFFFFF, #ISR_DEBUG_PIN
              
              ' Restore context (6 cycles)
              mov       reg_a, save_a
              mov       reg_b, save_b
              mov       reg_c, save_c
              
              ' Return from interrupt
              reti0
              
' Total overhead: 18 cycles + handler

PUB interrupt_monitor()
  ' ISR timing display
  DEBUG(`SCOPE ISRtiming SIZE 800 200 POS 0 0)
  DEBUG(`ISRtiming TRIGGER LEVEL 1)
  
  ' ISR frequency
  DEBUG(`FFT ISRfreq SIZE 400 200 POS 0 200)
  
  ' ISR duration histogram
  DEBUG(`PLOT ISRhist SIZE 400 200 POS 400 200)
  DEBUG(`ISRhist MODE HISTOGRAM)
  
  repeat
    ' Capture ISR timing
    if isr_active
      duration := cnt - isr_timestamp
      DEBUG(`ISRtiming `(duration))
      
      ' Update histogram
      bucket := duration / BUCKET_SIZE
      histogram[bucket]++
      DEBUG(`ISRhist PACK32 32 @histogram)
```

### Event System Tracking

Monitor P2's event system:

```spin2
DAT
event_monitor
              org       0
              
' Configure event monitoring
setup_events
              ' Set event sources
              setse1    #%001_000000 | PIN_A  ' Rising edge on PIN_A
              setse2    #%010_000000 | PIN_B  ' Falling edge on PIN_B
              setse3    #%100_000000 | TIMER  ' CT match
              
' Event polling loop
event_loop
              ' Check all events
              pollse1   wc
        if_c  call      #handle_event1
              
              pollse2   wc
        if_c  call      #handle_event2
              
              pollse3   wc
        if_c  call      #handle_event3
              
              jmp       #event_loop

handle_event1
              ' Debug event 1
              debug     ("EVENT1 @ ", udec(cnt))
              
              ' Process event
              ' ...
              ret

PUB event_dashboard()
  ' Event timeline
  DEBUG(`LOGIC Events SIZE 800 200 POS 0 0)
  DEBUG(`Events CHANNELS 4 LABELS "SE1" "SE2" "SE3" "SE4")
  
  ' Event frequency
  DEBUG(`PLOT EventRate SIZE 400 200 POS 0 200)
  DEBUG(`EventRate TRACES 4)
  
  ' Event correlation
  DEBUG(`SCOPE_XY Correlation SIZE 400 200 POS 400 200)
  
  repeat
    ' Update event displays
    event_states := get_event_states()
    DEBUG(`Events PACK8 1 @event_states)
    
    ' Calculate rates
    repeat i from 1 to 4
      event_rates[i-1] := calculate_event_rate(i)
    DEBUG(`EventRate PACK16 4 @event_rates)
```

## Multi-Cog Coordination Debug

### Cog Communication Visualization

Debug inter-cog messaging:

```spin2
DAT
cog_messenger
              org       0
              
' Mailbox communication with debug
send_message
              ' Wait for mailbox empty
.wait         rdlong    status, mailbox_addr wz
        if_nz jmp       #.wait
              
              ' Debug outgoing message
              debug     ("COG", udec(cogid), "->", uhex(message))
              
              ' Send message
              wrlong    message, mailbox_addr
              
              ret

receive_message
              ' Check for message
              rdlong    message, mailbox_addr wz
        if_z  ret
              
              ' Debug incoming message
              debug     ("COG", udec(cogid), "<-", uhex(message))
              
              ' Clear mailbox
              wrlong    #0, mailbox_addr
              
              ' Process message
              call      #process_message
              ret

PUB multicog_dashboard()
  ' Cog activity matrix
  DEBUG(`PLOT CogMatrix SIZE 400 400 POS 0 0)
  DEBUG(`CogMatrix MODE MATRIX 8 8)
  
  ' Message flow
  DEBUG(`LOGIC MsgFlow SIZE 400 200 POS 400 0)
  DEBUG(`MsgFlow CHANNELS 8)
  
  ' Cog utilization
  DEBUG(`PLOT CogUtil SIZE 400 200 POS 400 200)
  DEBUG(`CogUtil TRACES 8 STYLE STACKED)
  
  repeat
    ' Update communication matrix
    repeat sender from 0 to 7
      repeat receiver from 0 to 7
        matrix[sender][receiver] := get_message_count(sender, receiver)
    
    DEBUG(`CogMatrix PACK8 64 @matrix)
    
    ' Show message flow
    flow_state := get_message_flow()
    DEBUG(`MsgFlow PACK8 1 @flow_state)
    
    ' Update utilization
    repeat cog from 0 to 7
      utilization[cog] := measure_cog_usage(cog)
    DEBUG(`CogUtil PACK8 8 @utilization)
```

### Lock and Semaphore Monitoring

Debug synchronization primitives:

```spin2
DAT
lock_monitor
              org       0
              
' Instrumented lock operations
acquire_lock
              ' Debug lock attempt
              debug     ("LOCK", udec(lock_id), " REQ by COG", udec(cogid))
              
              ' Try to acquire
.retry        locktry   lock_id wc
        if_nc jmp       #.got_it
              
              ' Debug retry
              debug     ("LOCK", udec(lock_id), " BUSY")
              
              ' Wait and retry
              waitx     ##1000
              jmp       #.retry
              
.got_it       ' Debug acquisition
              debug     ("LOCK", udec(lock_id), " GOT by COG", udec(cogid))
              ret

release_lock
              ' Debug release
              debug     ("LOCK", udec(lock_id), " REL by COG", udec(cogid))
              
              ' Release lock
              lockrel   lock_id
              ret

PUB lock_visualization()
  ' Lock ownership matrix
  DEBUG(`PLOT LockOwner SIZE 400 200 POS 0 0)
  DEBUG(`LockOwner MODE MATRIX 16 8)  ' 16 locks x 8 cogs
  
  ' Lock contention graph
  DEBUG(`PLOT Contention SIZE 400 200 POS 400 0)
  DEBUG(`Contention TRACES 16)
  
  ' Deadlock detection
  DEBUG(`TERM Deadlock SIZE 800 200 POS 0 200)
  
  repeat
    ' Update lock ownership
    repeat lock from 0 to 15
      owner[lock] := get_lock_owner(lock)
      waiting[lock] := count_waiting_cogs(lock)
    
    DEBUG(`LockOwner PACK8 16 @owner)
    DEBUG(`Contention PACK8 16 @waiting)
    
    ' Check for deadlocks
    if detect_deadlock()
      DEBUG(`Deadlock "DEADLOCK DETECTED!")
      analyze_deadlock()
```

## Performance Profiling

### Instruction-Level Profiling

Profile code execution:

```spin2
DAT
profiler
              org       0
              
' Profiling instrumentation
profile_start
              getct     prof_start
              
              ' Code to profile
              call      #function_to_profile
              
              getct     prof_end
              sub       prof_end, prof_start
              
              ' Send profile data
              debug     ("PROF: ", udec(prof_end), " cycles")
              
              ' Accumulate statistics
              add       total_cycles, prof_end
              add       call_count, #1
              
              ' Update min/max
              max       max_cycles, prof_end
              mins      min_cycles, prof_end
              
              ret

PUB performance_analysis()
  ' Execution time histogram
  DEBUG(`PLOT ExecTime SIZE 400 300 POS 0 0)
  DEBUG(`ExecTime MODE HISTOGRAM)
  DEBUG(`ExecTime BINS 50)
  
  ' Hot spot visualization
  DEBUG(`PLOT HotSpots SIZE 400 300 POS 400 0)
  DEBUG(`HotSpots MODE HEATMAP)
  
  ' Statistics display
  DEBUG(`TERM Stats SIZE 800 200 POS 0 300)
  
  repeat
    ' Collect profile samples
    repeat sample from 0 to 999
      execution_time[sample] := get_profile_sample()
    
    ' Update histogram
    DEBUG(`ExecTime PACK16 1000 @execution_time)
    
    ' Calculate statistics
    mean := calculate_mean(@execution_time, 1000)
    stdev := calculate_stdev(@execution_time, 1000, mean)
    
    DEBUG(`Stats "Mean: " dec_(mean) " cycles")
    DEBUG(`Stats " StdDev: " dec_(stdev) " cycles")
    DEBUG(`Stats " Min: " dec_(min_cycles) " Max: " dec_(max_cycles))
```

### Pipeline Analysis

Visualize instruction pipeline:

```spin2
DAT
pipeline_monitor
              org       0
              
' Pipeline stage tracking
pipeline_track
              ' Stage 1: Fetch
              debug     ("FETCH: ", uhex(pc))
              
              ' Stage 2: Decode
              debug     ("DECODE: ", uhex(instruction))
              
              ' Stage 3: Execute
              debug     ("EXEC: ", uhex(result))
              
              ' Stall detection
              getct     cycle_count
              sub       cycle_count, last_cycle
              cmp       cycle_count, #2 wc
        if_nc debug     ("STALL: ", udec(cycle_count))
              
              mov       last_cycle, cycle_count
              ret

PUB pipeline_visualization()
  ' Pipeline stages
  DEBUG(`LOGIC Pipeline SIZE 800 100 POS 0 0)
  DEBUG(`Pipeline CHANNELS 6 LABELS "FETCH" "DECODE" "RF" "EX" "MEM" "WB")
  
  ' Stall histogram
  DEBUG(`PLOT Stalls SIZE 400 200 POS 0 100)
  DEBUG(`Stalls MODE HISTOGRAM)
  
  ' Throughput graph
  DEBUG(`PLOT Throughput SIZE 400 200 POS 400 100)
  
  repeat
    ' Update pipeline state
    pipeline_state := get_pipeline_state()
    DEBUG(`Pipeline PACK8 1 @pipeline_state)
    
    ' Track stalls
    if stall_detected()
      stall_cycles := measure_stall_duration()
      stall_histogram[stall_cycles]++
      DEBUG(`Stalls PACK32 32 @stall_histogram)
    
    ' Calculate throughput
    ipc := instructions_retired / cycles_elapsed
    DEBUG(`Throughput `(ipc * 100))  ' IPC * 100
```

## Real-World PASM Debug Applications

### High-Speed Protocol Implementation

Debug bit-banged protocols:

```spin2
DAT
usb_ls_driver
              org       0
              
' USB Low-Speed driver with debug
usb_bit_stuff
              ' Check for bit stuffing needed
              cmp       ones_count, #6 wz
        if_nz jmp       #.no_stuff
              
              ' Debug bit stuff
              debug     ("STUFF @ bit ", udec(bit_count))
              
              ' Insert stuffed bit
              xor       outa, usb_pins
              call      #usb_delay
              mov       ones_count, #0
              
.no_stuff     ' Send actual bit
              testb     data, bit_index wc
        if_c  or        outa, usb_pins
        if_nc andn      outa, usb_pins
              
              ' Debug each bit
              wxpin     data, #DEBUG_STREAM
              
              call      #usb_delay
              ret

PUB monitor_usb_driver()
  ' USB signal display
  DEBUG(`SCOPE USBsignal SIZE 400 300 POS 0 0)
  DEBUG(`USBsignal CHANNELS 2 LABELS "D+" "D-")
  
  ' USB packets
  DEBUG(`LOGIC USBpackets SIZE 400 300 POS 400 0)
  DEBUG(`USBpackets DECODE USB_LS)
  
  ' Bit stuffing events
  DEBUG(`PLOT BitStuff SIZE 800 200 POS 0 300)
  
  ' Launch driver
  coginit(USB_COG, @usb_ls_driver, @usb_params)
  
  ' Monitor output
  repeat
    ' Real-time signal levels
    d_plus := ina[D_PLUS_PIN]
    d_minus := ina[D_MINUS_PIN]
    DEBUG(`USBsignal DATA `(d_plus * 3300, d_minus * 3300))
```

### DSP Algorithm Debugging

Debug signal processing:

```spin2
DAT
fir_filter
              org       0
              
' FIR filter with debug output
fir_process
              ' Clear accumulator
              mov       accum, #0
              mov       tap, #0
              
.tap_loop     ' Get sample from circular buffer
              alts      tap, #samples
              mov       sample, 0-0
              
              ' Get coefficient
              alts      tap, #coefficients
              mov       coeff, 0-0
              
              ' MAC operation
              muls      sample, coeff
              add       accum, sample
              
              ' Debug tap calculation
              debug     ("TAP", udec(tap), ": ", udec(sample), 
                        " * ", udec(coeff), " = ", udec(sample))
              
              ' Next tap
              incmod    tap, #31
              tjnz      tap, #.tap_loop
              
              ' Output result
              sar       accum, #15  ' Scale
              
              ' Debug output
              debug     ("FIR OUT: ", udec(accum))
              
              ret

PUB dsp_analysis()
  ' Input signal
  DEBUG(`SCOPE Input SIZE 400 200 POS 0 0)
  
  ' Filter taps visualization
  DEBUG(`PLOT Taps SIZE 400 200 POS 400 0)
  DEBUG(`Taps TRACES 32 STYLE STEMS)
  
  ' Output signal
  DEBUG(`SCOPE Output SIZE 400 200 POS 0 200)
  
  ' Frequency response
  DEBUG(`FFT Response SIZE 400 200 POS 400 200)
  
  repeat
    ' Show filter operation
    DEBUG(`Input PACK16 256 @input_buffer)
    DEBUG(`Taps PACK16 32 @tap_values)
    DEBUG(`Output PACK16 256 @output_buffer)
    
    ' Calculate frequency response
    compute_frequency_response(@coefficients, @response)
    DEBUG(`Response PACK16 128 @response)
```

## Troubleshooting PASM Debug

Common issues and solutions:

**Problem**: Debug output affects timing
**Solution**: Use hardware streaming
```spin2
' Software debug - slow
debug     ("Value: ", udec(value))

' Hardware streaming - fast
wxpin     value, #STREAM_PIN
```

**Problem**: Too much debug data
**Solution**: Conditional debugging
```spin2
' Debug only on error
cmp       result, expected wz
if_nz     debug     ("ERROR: ", uhex(result))
```

**Problem**: Can't debug interrupt handlers
**Solution**: Use minimal instrumentation
```spin2
' Just timestamp and flag
getct     timestamp
wxpin     ##$80000000, #DEBUG_PIN  ' Single flag bit
```

## Chapter Summary

PASM assembly integration brings professional debugging capabilities to the lowest level of P2 programming. By combining deterministic debug timing, hardware streaming, and sophisticated visualization, you can observe and analyze assembly code execution without disrupting the precise timing that assembly programming provides.

From interrupt handlers to protocol drivers, from DSP algorithms to multi-cog systems, PASM debug integration provides the visibility needed to develop and debug high-performance assembly code. The ability to see inside assembly execution while maintaining cycle-accurate timing transforms low-level debugging from blind experimentation to informed optimization.

Next, we'll explore production integration workflows, where debug windows become part of the development and deployment process.