# Chapter 13: Video Generation

*From pixels to pictures*

## The Hook: VGA in 10 Instructions

```pasm2
        setcmod #$100           ' Set colorspace
        setcy   ##640*480      ' Set resolution
        setci   ##HSYNC_TIMING ' Set timing
        setcq   ##VSYNC_TIMING
        setcfrq ##PIX_FREQ     ' Set pixel frequency
        setcy   ##LINE_BUFFER  ' Set buffer address
        xinit   ##STREAMER_CMD, #0  ' Start video!
```

## Video Fundamentals

P2 generates video through:
- The streamer (DMA engine)
- Smart pins (sync signals)
- COG timing (line control)

## VGA Generation

Complete VGA driver example with proper timing and double buffering.

## HDMI Basics

P2 can generate HDMI signals using Smart Pins in special modes.

---

*Continue to [Chapter 14: Serial Protocols](14-serial-protocols.md) →*

---

# Chapter 14: Serial Protocols

*Talking to the world*

## The Hook: Hardware UART, SPI, and I2C

```pasm2
' UART in hardware
        wrpin   ##P_ASYNC_TX, #TX_PIN
        wxpin   ##BAUD_115200, #TX_PIN
        dirh    #TX_PIN
        wypin   char, #TX_PIN    ' Send character!
```

## UART Implementation

Smart Pins handle the bit timing, you handle the bytes.

## SPI Master and Slave

```pasm2
' SPI using Smart Pins
        wrpin   ##P_SYNC_TX, #MOSI_PIN
        wrpin   ##P_SYNC_RX, #MISO_PIN
        ' Clock and data handled in hardware!
```

## I2C Communication

Bit-banged or Smart Pin assisted - your choice!

---

*Continue to [Chapter 15: Signal Processing](15-signal-processing.md) →*

---

# Chapter 15: Signal Processing

*Digital meets analog*

## The Hook: 16-Bit ADC, No External Hardware

```pasm2
        wrpin   ##P_ADC_1X, #ADC_PIN   ' Configure ADC
        dirh    #ADC_PIN               ' Enable
        waitx   ##100                  ' Settle time
        rdpin   sample, #ADC_PIN       ' Read 16-bit sample!
```

## ADC and DAC Operations

Every pin can be:
- 16-bit ADC (with noise shaping)
- 16-bit DAC (with dithering)
- Comparator
- Sigma-delta converter

## Digital Filtering

Using CORDIC for DSP:

```pasm2
' Simple low-pass filter
        qrotate sample, ##FILTER_COEFF
        getqy   filtered
```

## Audio Processing

Real-time audio with Smart Pins and CORDIC.

---

*Continue to [Chapter 16: Multi-COG Orchestration](16-multi-cog-orchestration.md) →*

---

# Chapter 16: Multi-COG Orchestration

*The symphony comes together*

## The Hook: 8-COG Pipeline

```pasm2
' COG 0: Read sensor
' COG 1: Filter data  
' COG 2: Process signals
' COG 3: Control motor
' COG 4: Update display
' COG 5: Handle communications
' COG 6: Monitor safety
' COG 7: Coordinate everything
' All running simultaneously!
```

## COG Communication Patterns

### Producer-Consumer
```pasm2
' Producer COG
        wrlong  data, ##mailbox
        
' Consumer COG
poll    rdlong  data, ##mailbox wz
   if_z jmp     #poll
        wrlong  #0, ##mailbox    ' Clear
```

### Ring Buffer
```pasm2
' Circular buffer for streaming data
        wrlong  data, ptra++
        cmp     ptra, ##BUFFER_END wcz
   if_ae mov    ptra, ##BUFFER_START
```

## Locks and Semaphores

```pasm2
' Atomic operations using locks
get_lock
        locktry #0 wc
   if_c jmp     #get_lock
        ' Critical section
        lockrel #0
```

## System Architecture

Best practices for multi-COG systems:
- Dedicate COGs to specific tasks
- Minimize shared state
- Use mailboxes for commands
- Keep timing deterministic

## Real-World Example: Robot Controller

```pasm2
' Main coordinator (COG 0)
main    coginit #SENSOR_COG, @sensor_code, @sensor_params
        coginit #MOTOR_COG, @motor_code, @motor_params
        coginit #COMM_COG, @comm_code, @comm_params
        
        ' Coordination loop
loop    rdlong  sensor_data, ##SENSOR_MAILBOX
        ' Process and decide
        wrlong  motor_cmd, ##MOTOR_MAILBOX
        jmp     #loop
```

## The Medicine Cabinet

**Simple multi-COG pattern**:
```pasm2
' Just use hub variables
' Each COG owns specific addresses
' No locks needed if single-writer
```

## What We've Learned

You've completed the journey! You now understand:
- ✅ Parallel processing philosophy
- ✅ COG architecture and communication
- ✅ PASM2 instruction set
- ✅ Smart Pins and I/O
- ✅ CORDIC mathematics
- ✅ Video and serial protocols
- ✅ Multi-COG orchestration

## Your Next Steps

1. Build something amazing
2. Share with the community
3. Push the boundaries
4. Have fun!

---

**Congratulations!** You're now fluent in PASM2 and ready to unleash the full power of the Propeller 2!

---

*Continue to [Appendix A: Instruction Set Reference](appendix-a-instruction-reference.md) →*

---

