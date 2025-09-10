# Chapter 13: Video Generation

The P2 doesn't just blink LEDs—it paints pictures at 60 frames per second. With its streamer, smart pins, and raw speed, it can generate VGA, HDMI, composite, and more. No external chips needed. Welcome to the world where a microcontroller becomes a graphics card!

## The Hook: From Pixels to Pictures

Traditional microcontrollers struggle to toggle a pin fast enough for video. The P2? It can drive multiple displays simultaneously while running game logic, handling input, and playing sound. How? By making video generation a hardware problem, not a software one. Let's paint some pixels!

## Video Fundamentals

Video is just precisely-timed signals:

```pasm2
' VGA timing for 640x480 @ 60Hz
' Pixel clock: 25.175 MHz
' 
' Horizontal (31.5 kHz):
'   Visible: 640 pixels (25.42 µs)
'   Front porch: 16 pixels (0.64 µs)
'   Sync pulse: 96 pixels (3.81 µs)
'   Back porch: 48 pixels (1.91 µs)
'   Total: 800 pixels (31.78 µs)
'
' Vertical (60 Hz):
'   Visible: 480 lines
'   Front porch: 10 lines
'   Sync pulse: 2 lines
'   Back porch: 33 lines
'   Total: 525 lines
```

\begin{sidetrack}
\textbf{The Video Timing Dance}

Video is like a typewriter that never stops. It sweeps left to right (horizontal scan), then drops down a line. After filling the screen, it jumps back to the top (vertical retrace). The sync pulses tell the monitor when to start new lines and frames. Miss the timing, lose the picture!
\end{sidetrack}

## Basic VGA Driver

```pasm2
' Minimal VGA driver - 640x480 monochrome
vga_driver
        mov     ijmp1, #hsync_interrupt
        setint1 ##INT_CT1              ' Interrupt on timer
        
        getct   pa
        addct1  pa, ##H_TOTAL           ' Next line timing
        
' Configure streamer for pixels
        wrpin   ##P_SYNC_TX, #0         ' Pins 0-7 for RGB
        wxpin   #7, #0                  ' 8-bit mode
        dirh    #$FF                    ' Enable pins 0-7
        
' Main loop - prepare line data
main_loop
        rdfast  #0, line_ptr            ' Point to line data
        add     line_ptr, ##LINE_BYTES
        cmp     line_num, #V_VISIBLE wc
if_nc   mov     line_ptr, ##blank_line  ' Vertical blanking
        jmp     #main_loop

' Horizontal sync interrupt
hsync_interrupt
        ' Sync pulse
        drvl    #HSYNC_PIN
        waitx   ##H_SYNC_CYCLES
        drvh    #HSYNC_PIN
        
        ' Back porch
        waitx   ##H_BACK_CYCLES
        
        ' Stream visible pixels
        xinit   ##X_PIXELS, #0          ' Stream 640 pixels
        
        ' Update vertical
        incmod  line_num, ##V_TOTAL-1
        tjnz    line_num, #.no_vsync
        
        ' Vertical sync
        drvl    #VSYNC_PIN
        waitct1
        waitct1                         ' 2 lines
        drvh    #VSYNC_PIN
        
.no_vsync
        addct1  pa, ##H_TOTAL
        reti1
```

## Color Graphics with LUT

```pasm2
' 256-color palette mode
init_palette
        mov     ptrb, ##palette_data
        mov     pa, #0
.load   rdlong  color, ptrb++
        wrlut   color, pa++
        tjnz    pa, #.load              ' Load 256 colors
        
' Configure streamer for LUT mode
        setcq   ##$FF                   ' 8-bit LUT
        setcy   ##CYCLES_PER_PIXEL
        xcont   ##M_LUT, #0             ' LUT streaming mode
```

### Drawing Primitives

```pasm2
' Fast horizontal line
draw_hline
        mov     pa, y
        mul     pa, ##SCREEN_WIDTH
        add     pa, x1
        add     pa, ##screen_buffer
        
        mov     count, x2
        sub     count, x1
        
.loop   wrbyte  color, pa++
        djnz    count, #.loop
        ret

' Filled rectangle
fill_rect
        mov     dy, y2
        sub     dy, y1
.yloop  mov     backup_x1, x1
        mov     backup_x2, x2
        call    #draw_hline
        add     y1, #1
        mov     x1, backup_x1
        mov     x2, backup_x2
        djnz    dy, #.yloop
        ret
```

\begin{interlude}
\textbf{The Frame Buffer Dilemma}

640×480×1 byte = 307KB. The P2 has 512KB total. This means you can have a full-resolution frame buffer with 205KB left for code and data. Or use lower resolutions, fewer colors, or clever tricks like tiles and sprites. Choose wisely!
\end{interlude}

## Tile-Based Graphics

Save memory with 8×8 tiles:

```pasm2
' Tile map system (80×60 tiles of 8×8 pixels)
render_tiles
        mov     tile_y, #0
.yloop  mov     tile_x, #0
        
.xloop  ' Get tile number from map
        mov     pa, tile_y
        mul     pa, #80                 ' Tiles per row
        add     pa, tile_x
        add     pa, ##tile_map
        rdbyte  tile_num, pa
        
        ' Calculate tile graphics address
        shl     tile_num, #6            ' 64 bytes per tile
        add     tile_num, ##tile_gfx
        
        ' Copy tile to line buffer
        mov     ptrb, ##line_buffer
        mov     pa, tile_x
        shl     pa, #3                  ' 8 pixels per tile
        add     ptrb, pa
        
        setq    #2-1                    ' 8 bytes = 2 longs
        rdlong  ptrb, tile_num
        
        add     tile_x, #1
        cmp     tile_x, #80 wz
if_nz   jmp     #.xloop
        
        ' Stream the line
        rdfast  #0, ##line_buffer
        xinit   ##X_LINE, #0
        
        add     tile_y, #1
        cmp     tile_y, #60 wz
if_nz   jmp     #.yloop
        ret
```

## Sprite System

```pasm2
' Sprite renderer with transparency
draw_sprite
        ' Calculate screen position
        mov     pa, sprite_y
        mul     pa, ##SCREEN_WIDTH
        add     pa, sprite_x
        add     pa, ##screen_buffer
        
        ' Sprite source
        mov     ptrb, ##sprite_data
        
        mov     sy, #SPRITE_HEIGHT
.yloop  mov     sx, #SPRITE_WIDTH
        
.xloop  rdbyte  pixel, ptrb++
        cmp     pixel, #TRANSPARENT wz
if_nz   wrbyte  pixel, pa               ' Skip transparent
        add     pa, #1
        djnz    sx, #.xloop
        
        add     pa, ##SCREEN_WIDTH-SPRITE_WIDTH
        djnz    sy, #.yloop
        ret
```

## HDMI Output

```pasm2
' HDMI using P2's built-in encoding
hdmi_init
        wrpin   ##P_HDMI_SYNCS, #HDMI_BASE
        wxpin   ##$10_0000, #HDMI_BASE  ' Divider
        dirh    #HDMI_BASE+3<<6|#HDMI_BASE
        
' Encode and stream HDMI
hdmi_stream
        rdfast  #0, ##hdmi_buffer
        setcq   ##HDMI_CQ_CONFIG
        
.loop   xcont   ##HDMI_VISIBLE, #0     ' Visible pixels
        xcont   ##HDMI_HBLANK, #%1111  ' Blanking with syncs
        djnz    lines, #.loop
```

\begin{missing}
🚧 \textbf{CONTENT MISSING - COMING SOON}

Need to add:
- Complete HDMI protocol details
- Composite video generation
- Component video (YPbPr)
- Text mode implementation
- Double buffering techniques
\end{missing}

## Advanced Techniques

### Copper Effects (Per-Line Changes)
```pasm2
' Change colors per scanline (like Amiga Copper)
copper_list
        word    100, $FF_00_00          ' Line 100: Red
        word    150, $00_FF_00          ' Line 150: Green
        word    200, $00_00_FF          ' Line 200: Blue
        word    0, 0                    ' End marker

process_copper
        rdword  target_line, copper_ptr
        cmp     line_num, target_line wz
if_nz   ret
        
        add     copper_ptr, #2
        rdword  new_color, copper_ptr
        add     copper_ptr, #2
        
        ' Apply color change
        wrlut   new_color, #BACKGROUND_INDEX
        ret
```

### Plasma Effect
```pasm2
' Real-time plasma generation
plasma_frame
        add     phase1, #3
        add     phase2, #5
        
        mov     y, #0
.yloop  mov     x, #0
        
.xloop  ' Calculate plasma value
        mov     pa, x
        add     pa, phase1
        qrotate #127, pa               ' sin(x + phase1)
        getqy   val1
        
        mov     pa, y
        add     pa, phase2
        qrotate #127, pa               ' sin(y + phase2)
        getqy   val2
        
        add     val1, val2
        add     val1, #128              ' Offset to 0-255
        
        ' Write pixel
        wrbyte  val1, screen_ptr++
        
        add     x, #1
        cmp     x, #320 wz
if_nz   jmp     #.xloop
        
        add     y, #1
        cmp     y, #240 wz
if_nz   jmp     #.yloop
        ret
```

## Your Turn: Video Mastery

\begin{yourturn}
\textbf{Challenge 1: Bouncing Ball}
Create a bouncing ball animation with smooth motion.

\textbf{Challenge 2: Text Console}
Implement an 80×25 text display with a character ROM.

\textbf{Challenge 3: Spectrum Analyzer}
Display audio spectrum using bars or waterfall.

\textbf{Challenge 4: Game Screen}
Create a simple game display with score, lives, and playfield.

\textbf{Challenge 5: Video Modes}
Switch between different resolutions and color depths.
\end{yourturn}

## Video Gotchas

### Gotcha 1: Timing Precision
```pasm2
' WRONG - timing drift
.loop   waitx   ##LINE_TIME     ' Accumulates error!
        call    #draw_line
        jmp     #.loop
        
' RIGHT - use CT timers
        getct   pa
.loop   addct1  pa, ##LINE_TIME ' Absolute timing
        waitct1
        call    #draw_line
        jmp     #.loop
```

### Gotcha 2: Memory Bandwidth
```pasm2
' WRONG - can't keep up
.pixel  rdlong  color, ptra++   ' Too slow for video!
        xcont   #1, color
        djnz    count, #.pixel
        
' RIGHT - use streamer
        rdfast  #0, ptra
        xinit   ##X_PIXELS, #0  ' Hardware streaming
```

### Gotcha 3: Color Space
```pasm2
' WRONG - RGB values not formatted
        mov     color, red
        or      color, green
        or      color, blue     ' Wrong bit positions!
        
' RIGHT - proper RGB formatting
        shl     red, #16        ' R in bits 23-16
        shl     green, #8       ' G in bits 15-8
        or      color, red
        or      color, green
        or      color, blue     ' B in bits 7-0
```

\begin{review}
🔍 \textbf{NEEDS TECHNICAL REVIEW}

Verify:
- Exact VGA timing parameters
- HDMI encoding specifications
- Maximum pixel clock rates
- Color format specifications
\end{review}

## The Philosophy of Video Generation

P2 video generation embodies these principles:

1. **Hardware for heavy lifting**: Streamer handles pixel flow
2. **Software for creativity**: Your code controls what to display
3. **Memory tradeoffs**: Resolution vs. color depth vs. features
4. **Timing is everything**: Video waits for no one
5. **Parallel possibilities**: Multiple cogs for complex effects

\begin{chapterend}
✨ \textbf{You're now painting pixels at 60 FPS!}

You've mastered: VGA timing and signals, color modes and palettes, tiles and sprites, streaming and effects.

Next: Chapter 14 explores serial protocols—UART, SPI, I2C, and beyond!
\end{chapterend}

---

# Chapter 14: Serial Protocols

The world speaks serial. UART for terminals, SPI for memories, I2C for sensors, 1-Wire for temperature probes. The P2 speaks them all—fluently, simultaneously, and often without breaking a sweat. Let's become polyglots of the digital world!

## The Hook: One Pin, Infinite Conversations

A single wire carrying complex conversations. That's serial communication. The P2 doesn't just speak these protocols—it speaks multiple instances simultaneously. Need 16 UARTs? Done. SPI master and slave at once? Easy. I2C plus custom protocol? The Smart Pins have you covered.

## UART: The Universal Language

UART is everywhere—debug terminals, GPS modules, wireless bridges:

```pasm2
' Full-duplex UART driver
' 115200 baud, 8N1
uart_init
        ' Configure TX pin
        wrpin   ##P_ASYNC_TX | P_OE, #TX_PIN
        wxpin   ##CLK_FREQ/115200, #TX_PIN
        dirh    #TX_PIN
        
        ' Configure RX pin
        wrpin   ##P_ASYNC_RX, #RX_PIN
        wxpin   ##CLK_FREQ/115200, #RX_PIN
        dirh    #RX_PIN
        ret

' Send string
uart_print
        rdbyte  char, ptra++ wz
if_z    ret                             ' Null terminator
.wait   testp   #TX_PIN wc              ' Ready?
if_c    jmp     #.wait
        wypin   char, #TX_PIN           ' Send byte
        jmp     #uart_print

' Receive with timeout
uart_getc
        mov     timeout, ##1_000_000
.wait   testp   #RX_PIN wc              ' Data ready?
if_nc   rdpin   char, #RX_PIN           ' Read it
if_nc   ret
        djnz    timeout, #.wait
        neg     char, #1                ' -1 = timeout
        ret
```

\begin{sidetrack}
\textbf{Why 115200?}

115200 baud is the sweet spot—fast enough for most applications, slow enough for long cables and cheap USB adapters. It's also a clean division of many clock frequencies. But the P2 can go much faster—several megabaud if needed!
\end{sidetrack}

## SPI: The Speed Demon

SPI trades simplicity for speed—four wires, megabits per second:

```pasm2
' SPI master mode 0 (CPOL=0, CPHA=0)
spi_init
        dirl    #SPI_CLK                ' Clock output
        dirl    #SPI_MOSI               ' Data output
        dirh    #SPI_MISO               ' Data input
        dirl    #SPI_CS                 ' Chip select output
        drvh    #SPI_CS                 ' CS high (inactive)
        ret

' Transfer byte (mode 0)
spi_byte
        mov     bit_count, #8
        shl     data_out, #24           ' MSB first
        mov     data_in, #0
        
.loop   shl     data_out, #1 wc         ' Get next bit
        outc    #SPI_MOSI               ' Output bit
        drvh    #SPI_CLK                ' Clock high
        waitx   #2
        testp   #SPI_MISO wc            ' Read input
        rcl     data_in, #1             ' Shift in
        drvl    #SPI_CLK                ' Clock low
        waitx   #2
        djnz    bit_count, #.loop
        
        mov     pa, data_in
        ret

' Burst read
spi_read_burst
        drvl    #SPI_CS                 ' Select device
        
        mov     data_out, cmd           ' Send command
        call    #spi_byte
        
.loop   mov     data_out, #$FF          ' Clock out dummy
        call    #spi_byte
        wrbyte  pa, ptrb++              ' Store received
        djnz    count, #.loop
        
        drvh    #SPI_CS                 ' Deselect
        ret
```

### Smart Pin SPI

```pasm2
' Using Smart Pins for SPI - much faster!
spi_smart_init
        ' Clock pin - transition output
        wrpin   ##P_TRANSITION | P_OE, #SPI_CLK
        wxpin   ##$0001_0002, #SPI_CLK  ' Timebase
        dirh    #SPI_CLK
        
        ' MOSI - sync serial transmit
        wrpin   ##P_SYNC_TX | P_OE, #SPI_MOSI
        wxpin   #%1_00111, #SPI_MOSI   ' 8-bit, start/stop
        dirh    #SPI_MOSI
        
        ' MISO - sync serial receive
        wrpin   ##P_SYNC_RX, #SPI_MISO
        wxpin   #%0_00111, #SPI_MISO   ' 8-bit
        dirh    #SPI_MISO
        ret

' Smart Pin transfer
spi_smart_byte
        wypin   data_out, #SPI_MOSI     ' Start TX
        wypin   #16, #SPI_CLK           ' 16 transitions
        
.wait   testp   #SPI_MISO wc            ' Wait complete
if_nc   jmp     #.wait
        rdpin   data_in, #SPI_MISO      ' Get result
        ret
```

## I2C: The Diplomatic Protocol

I2C uses just two wires for an entire bus of devices:

```pasm2
' I2C bit-banged implementation
i2c_start
        dirh    #I2C_SDA                ' SDA high
        dirh    #I2C_SCL                ' SCL high
        waitx   #I2C_DELAY
        dirl    #I2C_SDA                ' SDA low (start)
        waitx   #I2C_DELAY
        dirl    #I2C_SCL                ' SCL low
        ret

i2c_stop
        dirl    #I2C_SDA                ' SDA low
        dirh    #I2C_SCL                ' SCL high
        waitx   #I2C_DELAY
        dirh    #I2C_SDA                ' SDA high (stop)
        waitx   #I2C_DELAY
        ret

i2c_write_byte
        mov     bit_count, #8
        
.loop   shl     data, #1 wc             ' Get MSB
if_c    dirh    #I2C_SDA                ' Output bit
if_nc   dirl    #I2C_SDA
        waitx   #I2C_DELAY/2
        dirh    #I2C_SCL                ' Clock high
        waitx   #I2C_DELAY
        dirl    #I2C_SCL                ' Clock low
        waitx   #I2C_DELAY/2
        djnz    bit_count, #.loop
        
        ' Get ACK
        dirh    #I2C_SDA                ' Release SDA
        waitx   #I2C_DELAY/2
        dirh    #I2C_SCL                ' Clock high
        testp   #I2C_SDA wc             ' Read ACK
        dirl    #I2C_SCL                ' Clock low
        ret                             ' C=0 if ACK

i2c_read_byte
        mov     bit_count, #8
        mov     data, #0
        dirh    #I2C_SDA                ' Release SDA
        
.loop   dirh    #I2C_SCL                ' Clock high
        waitx   #I2C_DELAY/2
        testp   #I2C_SDA wc             ' Read bit
        rcl     data, #1                ' Shift in
        waitx   #I2C_DELAY/2
        dirl    #I2C_SCL                ' Clock low
        waitx   #I2C_DELAY
        djnz    bit_count, #.loop
        
        ' Send ACK/NAK
        test    ack_flag, #1 wc
if_c    dirh    #I2C_SDA                ' NAK
if_nc   dirl    #I2C_SDA                ' ACK
        waitx   #I2C_DELAY/2
        dirh    #I2C_SCL                ' Clock high
        waitx   #I2C_DELAY
        dirl    #I2C_SCL                ' Clock low
        dirh    #I2C_SDA                ' Release SDA
        ret
```

\begin{interlude}
\textbf{The I2C Philosophy}

I2C is democratic—multiple masters can share the bus, devices have addresses, and everyone follows the same rules. It's slower than SPI but needs fewer pins and handles multiple devices elegantly. Perfect for sensors and small memories!
\end{interlude}

## 1-Wire: Minimalism Perfected

One wire for power and data—efficiency at its finest:

```pasm2
' 1-Wire protocol (Dallas/Maxim)
ow_reset
        dirl    #OW_PIN                 ' Pull low
        waitx   ##480*US                ' 480 µs reset pulse
        dirh    #OW_PIN                 ' Release
        waitx   ##70*US                 ' Wait for presence
        testp   #OW_PIN wc              ' Check presence
        waitx   ##410*US                ' Complete slot
        ret                             ' C=0 if device present

ow_write_bit
        test    data, #1 wc
        dirl    #OW_PIN                 ' Start slot
if_c    waitx   ##6*US                  ' Write 1: short low
if_c    dirh    #OW_PIN
if_nc   waitx   ##60*US                 ' Write 0: long low
if_nc   dirh    #OW_PIN
        waitx   ##54*US                 ' Complete slot
        ret

ow_read_bit
        dirl    #OW_PIN                 ' Start slot
        waitx   ##6*US
        dirh    #OW_PIN                 ' Release
        waitx   ##9*US
        testp   #OW_PIN wc              ' Sample
        waitx   ##45*US                 ' Complete slot
        ret                             ' C = bit value
```

## Custom Protocols

Sometimes you need something special:

```pasm2
' Manchester encoding for RF
manchester_byte
        mov     bit_count, #8
        
.loop   shl     data, #1 wc
if_c    drvl    #RF_PIN                 ' 1: low then high
if_c    waitx   ##HALF_BIT
if_c    drvh    #RF_PIN
if_nc   drvh    #RF_PIN                 ' 0: high then low
if_nc   waitx   ##HALF_BIT
if_nc   drvl    #RF_PIN
        waitx   ##HALF_BIT
        djnz    bit_count, #.loop
        ret

' WS2812 LED protocol
ws2812_bit
        test    rgb_data, bit_mask wc
if_c    drvh    #LED_PIN                ' 1: long high
if_c    waitx   ##T1H
if_c    drvl    #LED_PIN
if_c    waitx   ##T1L
if_nc   drvh    #LED_PIN                ' 0: short high
if_nc   waitx   ##T0H
if_nc   drvl    #LED_PIN
if_nc   waitx   ##T0L
        ret
```

\begin{missing}
🚧 \textbf{CONTENT MISSING - COMING SOON}

Need to add:
- CAN bus implementation
- LIN bus protocol
- RS-485 with direction control
- USB bit-banging
- Infrared protocols (NEC, RC5)
\end{missing}

## Protocol Patterns

### Pattern 1: Multi-Drop Bus
```pasm2
' Address multiple devices on one bus
query_devices
        mov     device, #0
.loop   call    #select_device
        call    #send_command
        call    #read_response
        call    #deselect_device
        add     device, #1
        cmp     device, #MAX_DEVICES wz
if_nz   jmp     #.loop
        ret
```

### Pattern 2: Protocol Bridge
```pasm2
' UART to I2C bridge
bridge_loop
        call    #uart_getc              ' Get command
        cmp     char, #"R" wz           ' Read command?
if_z    call    #bridge_i2c_read
        cmp     char, #"W" wz           ' Write command?
if_z    call    #bridge_i2c_write
        jmp     #bridge_loop
```

### Pattern 3: Error Recovery
```pasm2
' Retry with exponential backoff
reliable_send
        mov     retry, #0
        mov     delay, ##INITIAL_DELAY
        
.retry  call    #send_packet
        call    #wait_ack
if_nc   ret                             ' Success!
        
        add     retry, #1
        cmp     retry, #MAX_RETRY wz
if_z    jmp     #fail
        
        waitx   delay
        shl     delay, #1               ' Double delay
        jmp     #.retry
```

## Your Turn: Protocol Mastery

\begin{yourturn}
\textbf{Challenge 1: Terminal Emulator}
Create a VT100-compatible serial terminal.

\textbf{Challenge 2: SPI Memory}
Interface with SPI flash memory for data logging.

\textbf{Challenge 3: I2C Scanner}
Scan I2C bus and report all device addresses.

\textbf{Challenge 4: Protocol Analyzer}
Decode and display protocol traffic in real-time.

\textbf{Challenge 5: Multi-Protocol Hub}
Bridge between UART, SPI, and I2C devices.
\end{yourturn}

## Protocol Gotchas

### Gotcha 1: Pull-up Resistors
```pasm2
' WRONG - no pull-ups on I2C
        dirh    #I2C_SDA        ' Driving high
        dirh    #I2C_SCL        ' Not open-drain!
        
' RIGHT - configure as open-drain
        wrpin   ##P_HIGH_1K5, #I2C_SDA ' Internal pull-up
        wrpin   ##P_HIGH_1K5, #I2C_SCL
        ' Use dirl/dirh to pull low/release
```

### Gotcha 2: Timing Tolerance
```pasm2
' WRONG - assumes exact timing
        waitx   ##EXACT_TIME
        
' RIGHT - sample in middle of bit
        waitx   ##BIT_TIME/2-MARGIN
        testp   #RX_PIN wc      ' Sample
        waitx   ##BIT_TIME/2+MARGIN
```

### Gotcha 3: Byte Order
```pasm2
' WRONG - endianness confusion
        wrlong  data, buffer    ' Little-endian
        ' Send over SPI MSB first - backwards!
        
' RIGHT - swap if needed
        rev     data            ' Reverse byte order
        ' Now send MSB first correctly
```

\begin{review}
🔍 \textbf{NEEDS TECHNICAL REVIEW}

Verify:
- Maximum reliable baud rates
- Smart Pin mode configurations for protocols
- Timing requirements for each protocol
- Error handling best practices
\end{review}

## The Philosophy of Serial Communication

Serial protocols embody timeless principles:

1. **Simplicity wins**: Fewer wires, simpler hardware
2. **Timing is contract**: Both sides must agree
3. **Error handling essential**: Real world is noisy
4. **Standards enable ecosystems**: Follow the specs
5. **Hardware acceleration helps**: Let Smart Pins do the work

\begin{chapterend}
✨ \textbf{You're now fluent in digital dialects!}

You've mastered: UART for universal communication, SPI for speed, I2C for device buses, custom protocols for special needs.

Next: Chapter 15 dives into signal processing—filters, FFTs, and real-time audio!
\end{chapterend}

---

# Chapter 15: Signal Processing

The real world is analog—sound waves, temperature changes, light levels. The P2 bridges this gap with 64 ADCs, 64 DACs, and the computational power to process signals in real-time. From audio effects to motor control, from data compression to pattern recognition, let's turn signals into insights!

## The Hook: Seeing the Invisible

Imagine seeing sound, predicting the future from sensor patterns, or extracting meaning from noise. That's signal processing. The P2 doesn't just measure signals—it understands them. With the CORDIC engine, streaming hardware, and parallel processing, you can implement DSP algorithms that usually require dedicated chips.

## Digital Filtering Fundamentals

Filters shape signals—removing noise, extracting features:

```pasm2
' Simple moving average filter (low-pass)
' Smooths data by averaging last N samples
moving_average
        rdpin   new_sample, #ADC_PIN    ' Get new sample
        
        ' Add to circular buffer
        wrlong  new_sample, buf_ptr
        add     buf_ptr, #4
        cmp     buf_ptr, ##buffer_end wz
if_z    mov     buf_ptr, ##buffer_start
        
        ' Calculate average
        mov     sum, #0
        mov     ptr, ##buffer_start
        mov     count, #FILTER_SIZE
        
.sum    rdlong  pa, ptr
        add     ptr, #4
        add     sum, pa
        djnz    count, #.sum
        
        ' Divide by size (power of 2 for speed)
        shr     sum, #FILTER_SHIFT      ' /16, /32, etc
        
        ' Output filtered value
        wypin   sum, #DAC_PIN
        ret

buffer_start
        long    0[32]                   ' 32-sample buffer
buffer_end
```

### IIR (Infinite Impulse Response) Filter
```pasm2
' First-order low-pass IIR filter
' y[n] = α*x[n] + (1-α)*y[n-1]
iir_lowpass
        rdpin   input, #ADC_PIN
        
        ' Calculate α*x[n] using CORDIC
        qmul    input, alpha            ' α in fixed-point
        getqx   term1
        
        ' Calculate (1-α)*y[n-1]
        mov     pa, ##$1_0000           ' 1.0 in 16.16
        sub     pa, alpha               ' (1-α)
        qmul    pa, previous_y
        getqx   term2
        
        ' Sum and scale
        add     term1, term2
        shr     term1, #16              ' Convert from 16.16
        mov     previous_y, term1
        
        wypin   term1, #DAC_PIN
        ret
        
alpha       long    $3333                ' 0.2 in 16.16 format
previous_y  long    0
```

\begin{sidetrack}
\textbf{FIR vs IIR}

FIR (Finite Impulse Response) filters use only input samples—stable but need many taps. IIR filters use feedback—efficient but can become unstable. Choose FIR for linear phase response, IIR for efficiency. The P2 can handle both!
\end{sidetrack}

## FFT: Frequency Domain Magic

The Fast Fourier Transform reveals frequency components:

```pasm2
' Radix-2 FFT butterfly operation
' Complex multiply: (a+bi) * (W_re+W_im*i)
fft_butterfly
        ' Load twiddle factor
        mov     W_re, twiddle_re
        mov     W_im, twiddle_im
        
        ' Complex multiply for FFT
        qmul    b_re, W_re              ' b_re * W_re
        getqx   prod1
        qmul    b_im, W_im              ' b_im * W_im
        getqx   prod2
        sub     prod1, prod2            ' Real part
        
        qmul    b_re, W_im              ' b_re * W_im
        getqx   prod3
        qmul    b_im, W_re              ' b_im * W_re
        getqx   prod4
        add     prod3, prod4            ' Imaginary part
        
        ' Butterfly add/subtract
        mov     temp_re, a_re
        mov     temp_im, a_im
        
        add     a_re, prod1             ' Top output
        add     a_im, prod3
        
        sub     temp_re, prod1          ' Bottom output
        sub     temp_im, prod3
        
        mov     b_re, temp_re
        mov     b_im, temp_im
        ret
```

### Spectrum Analyzer
```pasm2
' Real-time spectrum display
spectrum_analyzer
        ' Collect samples
        mov     count, #FFT_SIZE
        mov     ptr, ##sample_buffer
.collect
        rdpin   pa, #ADC_PIN
        wrlong  pa, ptr
        add     ptr, #4
        waitx   ##SAMPLE_PERIOD
        djnz    count, #.collect
        
        ' Apply window function
        call    #apply_hamming_window
        
        ' Perform FFT
        call    #fft_256_point
        
        ' Calculate magnitude spectrum
        mov     ptr, ##fft_output
        mov     count, #128             ' Only positive frequencies
        
.magnitude
        rdlong  real, ptr
        add     ptr, #4
        rdlong  imag, ptr
        add     ptr, #4
        
        ' Magnitude = sqrt(real² + imag²)
        qmul    real, real
        getqx   pa
        qmul    imag, imag
        getqx   pb
        add     pa, pb
        qsqrt   pa, #0
        getqx   magnitude
        
        ' Display as bar graph
        call    #draw_spectrum_bar
        
        djnz    count, #.magnitude
        ret
```

## Audio Processing

Real-time audio effects with zero latency:

```pasm2
' Audio delay/echo effect
audio_echo
        ' Read input sample
        rdpin   input, #ADC_LEFT
        
        ' Get delayed sample from circular buffer
        mov     pa, write_ptr
        sub     pa, delay_size
        and     pa, ##BUFFER_MASK
        rdlong  delayed, pa
        
        ' Mix input with delayed (echo)
        mov     output, input
        sar     delayed, #1             ' 50% mix
        add     output, delayed
        
        ' Store in delay buffer
        wrlong  input, write_ptr
        add     write_ptr, #4
        and     write_ptr, ##BUFFER_MASK
        
        ' Output mixed signal
        wypin   output, #DAC_LEFT
        ret

delay_buffer
        long    0[8192]                 ' ~180ms at 44.1kHz
BUFFER_MASK = $7FFC                    ' 8192 * 4 - 4
```

### Parametric Equalizer
```pasm2
' 3-band parametric EQ
parametric_eq
        rdpin   input, #ADC_PIN
        
        ' Low band (bass)
        mov     pa, input
        call    #biquad_lowpass
        qmul    pa, low_gain
        getqx   low_out
        
        ' Mid band
        mov     pa, input
        call    #biquad_bandpass
        qmul    pa, mid_gain
        getqx   mid_out
        
        ' High band (treble)
        mov     pa, input
        call    #biquad_highpass
        qmul    pa, high_gain
        getqx   high_out
        
        ' Sum all bands
        mov     output, low_out
        add     output, mid_out
        add     output, high_out
        
        ' Prevent clipping
        mins    output, ##$7FFF
        maxs    output, ##$8000
        
        wypin   output, #DAC_PIN
        ret
```

\begin{interlude}
\textbf{The Nyquist Theorem}

To accurately capture a signal, sample at least twice its highest frequency. For 20kHz audio, sample at 40kHz minimum (44.1kHz standard gives margin). The P2 can easily sample at MHz rates, capturing ultrasonic signals that other processors miss!
\end{interlude}

## Motor Control and PID

Signal processing isn't just audio:

```pasm2
' PID controller for motor speed
pid_control
        ' Read current speed (encoder)
        rdpin   current_speed, #ENCODER_PIN
        
        ' Calculate error
        mov     error, target_speed
        sub     error, current_speed
        
        ' Proportional term
        qmul    error, Kp
        getqx   p_term
        
        ' Integral term
        add     integral, error
        ' Limit integral (anti-windup)
        mins    integral, ##MAX_INTEGRAL
        maxs    integral, ##-MAX_INTEGRAL
        qmul    integral, Ki
        getqx   i_term
        
        ' Derivative term
        mov     derivative, error
        sub     derivative, prev_error
        mov     prev_error, error
        qmul    derivative, Kd
        getqx   d_term
        
        ' Sum PID terms
        mov     output, p_term
        add     output, i_term
        add     output, d_term
        
        ' Limit output
        mins    output, ##MAX_PWM
        maxs    output, #0
        
        ' Update motor PWM
        wypin   output, #MOTOR_PWM_PIN
        ret
        
Kp      long    $2000                   ' Proportional gain
Ki      long    $0100                   ' Integral gain
Kd      long    $0800                   ' Derivative gain
```

## Pattern Recognition

Detect patterns in signals:

```pasm2
' Zero-crossing detector for frequency measurement
zero_cross_detect
        rdpin   new_sample, #ADC_PIN
        
        ' Check for zero crossing
        xor     new_sample, prev_sample
        testb   new_sample, #31 wc      ' Sign bit changed?
if_nc   jmp     #.no_cross
        
        ' Zero crossing detected
        getct   cross_time
        mov     period, cross_time
        sub     period, last_cross
        mov     last_cross, cross_time
        
        ' Calculate frequency
        mov     pa, ##CLOCK_FREQ
        qdiv    pa, period
        getqx   frequency
        
.no_cross
        mov     prev_sample, new_sample
        ret
```

\begin{missing}
🚧 \textbf{CONTENT MISSING - COMING SOON}

Need to add:
- Correlation and convolution
- Adaptive filters
- Compression algorithms
- Neural network inference
- Sensor fusion techniques
\end{missing}

## Your Turn: Signal Processing Projects

\begin{yourturn}
\textbf{Challenge 1: Guitar Tuner}
Detect pitch using FFT and display note/frequency.

\textbf{Challenge 2: Voice Changer}
Implement pitch shifting and formant modification.

\textbf{Challenge 3: Data Logger}
Compress sensor data using delta encoding.

\textbf{Challenge 4: Heart Rate Monitor}
Extract heart rate from noisy sensor signal.

\textbf{Challenge 5: Audio Visualizer}
Create real-time spectrum display with peak detection.
\end{yourturn}

## Signal Processing Gotchas

### Gotcha 1: Aliasing
```pasm2
' WRONG - undersampling causes aliasing
        waitx   ##SLOW_RATE     ' Misses high frequencies
        
' RIGHT - sample fast enough
        waitx   ##FAST_RATE     ' > 2× highest frequency
        ' Or add anti-aliasing filter
```

### Gotcha 2: Overflow
```pasm2
' WRONG - filter can overflow
        add     sum, sample
        add     sum, sample2    ' Might overflow!
        
' RIGHT - use saturation
        add     sum, sample
        adds    sum, sample2    ' Saturating add
```

### Gotcha 3: Fixed-Point Scaling
```pasm2
' WRONG - precision loss
        shr     value, #16      ' Lose fractional bits
        mul     value, gain
        
' RIGHT - maintain precision
        qmul    value, gain     ' Full precision
        getqx   result
        shr     result, #16     ' Scale at end
```

\begin{review}
🔍 \textbf{NEEDS TECHNICAL REVIEW}

Verify:
- FFT accuracy and performance
- Filter stability conditions
- Maximum sample rates achievable
- Fixed-point precision requirements
\end{review}

## The Philosophy of Signal Processing

DSP on the P2 embodies key principles:

1. **Real-time is king**: Process as data arrives
2. **Parallel processing helps**: Multiple cogs for pipelines
3. **Hardware acceleration**: CORDIC for math, streamers for data
4. **Fixed-point suffices**: Floating-point often unnecessary
5. **Memory is precious**: Use circular buffers and streaming

\begin{chapterend}
✨ \textbf{You're now processing signals like a DSP chip!}

You've mastered: Digital filters, FFT and frequency analysis, audio processing, control systems, and pattern recognition.

Final chapter ahead: Multi-COG Orchestration—bringing it all together!
\end{chapterend}

---

# Chapter 16: Multi-COG Orchestration

This is it—the summit. Everything you've learned leads here. Eight cogs working as one, each contributing their strengths, communicating seamlessly, achieving what no single processor could. Welcome to the art of parallel orchestration, where the P2 truly shines!

## The Hook: The Symphony Finale

Remember our orchestra metaphor? Now you're not just conducting—you're composing. Each cog is an instrument with its own part to play. Some keep time (clock/sync), others provide melody (processing), some handle rhythm (I/O), and together they create something magical. Let's compose a masterpiece!

## Architecture Patterns

### Pattern 1: Pipeline Architecture
```pasm2
' Four-stage video processing pipeline
' Each cog handles one stage

' Cog 0: Video capture
capture_cog
        rdfast  #0, ##raw_buffer
        xinit   ##VIDEO_CAPTURE, #0
        
        waitxfi                         ' Wait for frame
        cogatn  #%0000_0010             ' Signal cog 1
        jmp     #capture_cog

' Cog 1: Color conversion
color_cog
        waitatn                         ' Wait for data
        
        rdfast  #0, ##raw_buffer
        wrfast  #0, ##rgb_buffer
        
.loop   rflong  pixel                   ' YUV pixel
        call    #yuv_to_rgb
        wflong  pixel                   ' RGB pixel
        djnz    pixels, #.loop
        
        cogatn  #%0000_0100             ' Signal cog 2
        cogatn  #%0000_0001             ' Ack cog 0
        jmp     #color_cog

' Cog 2: Effects processing
effects_cog
        waitatn
        ' Apply filters, overlays, etc.
        cogatn  #%0000_1000             ' Signal cog 3
        cogatn  #%0000_0010             ' Ack cog 1
        jmp     #effects_cog

' Cog 3: Display output
display_cog
        waitatn
        rdfast  #0, ##display_buffer
        xinit   ##VIDEO_OUTPUT, #0
        cogatn  #%0000_0100             ' Ack cog 2
        jmp     #display_cog
```

### Pattern 2: Worker Pool
```pasm2
' Dynamic work distribution among workers

' Cog 0: Task dispatcher
dispatcher
        ' Check for new tasks
        rdlong  task, ##task_queue wz
if_z    jmp     #dispatcher
        
        ' Find available worker
        mov     mask, #%0000_0010
.find   cogatn  mask                    ' Try to wake worker
        waitx   #10
        pollatn wc                      ' Did they respond?
if_c    shl     mask, #1                ' Try next
if_c    jmp     #.find
        
        ' Assign task
        mov     pa, mask
        encod   pa                      ' Get cog number
        shl     pa, #2                  ' Byte offset
        add     pa, ##worker_tasks
        wrlong  task, pa                ' Assign task
        
        jmp     #dispatcher

' Cogs 1-7: Workers
worker  cogid   pa                      ' Get our ID
        shl     pa, #2
        add     pa, ##worker_tasks
        
.loop   waitatn                         ' Wait for work
        cogatn  #%0000_0001             ' Acknowledge
        
        rdlong  task, pa wz             ' Get our task
if_z    jmp     #.loop                  ' No task
        
        ' Process task based on type
        mov     pb, task
        and     pb, #$FF                ' Task type
        shr     task, #8                ' Task data
        
        cmp     pb, #TASK_COMPUTE wz
if_z    call    #do_compute
        cmp     pb, #TASK_IO wz
if_z    call    #do_io
        cmp     pb, #TASK_CRYPTO wz
if_z    call    #do_crypto
        
        wrlong  #0, pa                  ' Clear task
        jmp     #.loop
```

\begin{sidetrack}
\textbf{Load Balancing}

Static assignment (cog 1 always does X) is simple but can waste resources. Dynamic assignment (any cog can do any task) maximizes utilization but adds complexity. Choose based on your needs—predictable timing favors static, maximum throughput favors dynamic.
\end{sidetrack}

### Pattern 3: Specialized Roles
```pasm2
' Each cog has a dedicated role

' Cog 0: Main controller and UI
main_controller
        call    #read_user_input
        call    #update_menu
        call    #dispatch_commands
        jmp     #main_controller

' Cog 1: Network stack
network_cog
        call    #check_ethernet
        call    #process_packets
        call    #update_connections
        jmp     #network_cog

' Cog 2: USB host
usb_cog
        call    #poll_devices
        call    #handle_transfers
        call    #process_hid
        jmp     #usb_cog

' Cog 3: Audio engine
audio_cog
        call    #mix_channels
        call    #apply_effects
        call    #stream_output
        jmp     #audio_cog

' Cog 4: Storage manager
storage_cog
        call    #handle_filesystem
        call    #cache_management
        call    #wear_leveling
        jmp     #storage_cog

' Cog 5: Security processor
crypto_cog
        call    #handle_encryption
        call    #verify_signatures
        call    #manage_keys
        jmp     #crypto_cog

' Cog 6: Sensor fusion
sensor_cog
        call    #read_all_sensors
        call    #kalman_filter
        call    #update_model
        jmp     #sensor_cog

' Cog 7: Display engine
display_cog
        call    #render_frame
        call    #handle_vsync
        call    #update_sprites
        jmp     #display_cog
```

## Communication Strategies

### Mailbox System
```pasm2
' Advanced mailbox with priorities
        orgh    $8000
        
mailbox_struct
        long    0               ' Command/Status
        long    0               ' Priority (0=highest)
        long    0               ' Sender COG ID
        long    0               ' Timestamp
        long    0[4]            ' Parameters
        long    0[16]           ' Data buffer

' Send high-priority message
send_priority_message
        cogid   sender
        getct   timestamp
        
        ' Wait for mailbox free
.wait   rdlong  status, ##mailbox_struct wz
if_nz   jmp     #.wait
        
        ' Fill message
        wrlong  command, ##mailbox_struct+0
        wrlong  priority, ##mailbox_struct+4
        wrlong  sender, ##mailbox_struct+8
        wrlong  timestamp, ##mailbox_struct+12
        
        ' Signal recipient
        cogatn  target_cog
        ret
```

### Shared Memory Map
```pasm2
' System-wide memory map
        orgh    $10000
        
' Global state (read by all)
system_status   long    0
error_flags     long    0
frame_counter   long    0
time_stamps     long    0[8]

' Per-cog sections (512 bytes each)
cog0_data       long    0[128]
cog1_data       long    0[128]
cog2_data       long    0[128]
cog3_data       long    0[128]
cog4_data       long    0[128]
cog5_data       long    0[128]
cog6_data       long    0[128]
cog7_data       long    0[128]

' Shared buffers
audio_buffer    long    0[1024]
video_buffer    long    0[2048]
network_buffer  long    0[512]
```

\begin{interlude}
\textbf{The Cache Line Dance}

When multiple cogs access the same hub location, they can create "hot spots" that slow everyone down. Spread your data across different cache lines (32-byte boundaries) to minimize contention. It's like having multiple doors to a building instead of everyone squeezing through one.
\end{interlude}

## Synchronization Masterclass

### Barrier Synchronization
```pasm2
' All cogs must reach barrier before continuing
global_barrier
        cogid   pa
        mov     pb, #1
        shl     pb, pa                  ' Our bit
        
        ' Signal arrival at barrier
        lock    #BARRIER_LOCK
        rdlong  arrived, ##barrier_mask
        or      arrived, pb
        wrlong  arrived, ##barrier_mask
        unlock  #BARRIER_LOCK
        
        ' Wait for all cogs
.wait   rdlong  pa, ##barrier_mask
        cmp     pa, ##$FF wz            ' All 8 cogs?
if_nz   jmp     #.wait
        
        ' Reset for next barrier
        cogid   pa
        cmp     pa, #0 wz               ' Cog 0 resets
if_z    wrlong  #0, ##barrier_mask
        ret
```

### Token Ring Communication
```pasm2
' Pass token around cogs in ring
token_ring
        cogid   my_id
        mov     next_id, my_id
        add     next_id, #1
        and     next_id, #7             ' Wrap to 0-7
        
.wait   rdlong  token, ##token_holder
        cmp     token, my_id wz
if_nz   jmp     #.wait                  ' Not our turn
        
        ' We have the token - do work
        call    #critical_operation
        
        ' Pass token to next cog
        wrlong  next_id, ##token_holder
        cogatn  next_id                 ' Wake next
        jmp     #token_ring
```

## Real-World Application: Game Console

Let's orchestrate a complete game system:

```pasm2
' Complete game console using all 8 cogs

' Cog 0: Game logic and AI
game_logic
        call    #update_player
        call    #update_enemies
        call    #check_collisions
        call    #update_score
        
        ' Signal renderer
        wrlong  #1, ##frame_ready
        cogatn  #%0000_1000
        
        waitx   ##FRAME_TIME
        jmp     #game_logic

' Cog 1: Input handler
input_handler
        ' Read all controllers
        call    #read_gamepad1
        call    #read_gamepad2
        call    #read_keyboard
        
        ' Process input events
        call    #translate_inputs
        wrlong  input_state, ##player_controls
        
        jmp     #input_handler

' Cog 2: Physics engine
physics_engine
        ' Update all physics objects
        rdlong  count, ##physics_objects
.loop   call    #apply_gravity
        call    #detect_collisions
        call    #resolve_forces
        djnz    count, #.loop
        
        jmp     #physics_engine

' Cog 3: Audio mixer
audio_mixer
        ' Mix all audio channels
        call    #mix_music
        call    #mix_sfx
        call    #apply_3d_audio
        
        ' Output stereo audio
        wypin   left_channel, #DAC_LEFT
        wypin   right_channel, #DAC_RIGHT
        
        jmp     #audio_mixer

' Cog 4: Sprite engine
sprite_engine
        ' Process all sprites
        mov     count, ##MAX_SPRITES
        mov     ptr, ##sprite_list
        
.loop   rdlong  sprite_data, ptr
        call    #transform_sprite
        call    #clip_sprite
        call    #draw_sprite
        add     ptr, #SPRITE_SIZE
        djnz    count, #.loop
        
        jmp     #sprite_engine

' Cog 5: Background renderer
background_renderer
        ' Render parallax layers
        call    #render_far_layer
        call    #render_mid_layer
        call    #render_near_layer
        
        ' Apply effects
        call    #apply_fog
        call    #apply_lighting
        
        jmp     #background_renderer

' Cog 6: Network multiplayer
network_handler
        ' Handle network events
        call    #receive_packets
        call    #update_remote_players
        call    #send_state_updates
        
        ' Sync with game logic
        rdlong  pa, ##game_tick
        wrlong  pa, ##network_tick
        
        jmp     #network_handler

' Cog 7: Video output
video_output
        ' Wait for frame ready
.wait   rdlong  pa, ##frame_ready wz
if_z    jmp     #.wait
        
        ' Output frame
        rdfast  #0, ##frame_buffer
        xinit   ##VIDEO_TIMING, #0
        
        ' Clear ready flag
        wrlong  #0, ##frame_ready
        
        ' Update stats
        incmod  frame_count, ##999
        wrlong  frame_count, ##fps_counter
        
        jmp     #video_output
```

\begin{missing}
🚧 \textbf{CONTENT MISSING - COMING SOON}

Need to add:
- Debugging multi-cog systems
- Performance profiling across cogs
- Power management strategies
- Fault tolerance and recovery
- Inter-cog streaming patterns
\end{missing}

## Your Turn: Orchestration Challenges

\begin{yourturn}
\textbf{Challenge 1: Music Synthesizer}
8-channel polyphonic synthesizer with effects.

\textbf{Challenge 2: Network Router}
Multi-port packet router with QoS.

\textbf{Challenge 3: Robot Controller}
Sensor fusion, motor control, and navigation.

\textbf{Challenge 4: Data Acquisition}
Multi-channel scope with triggering and storage.

\textbf{Challenge 5: Retro Computer}
Complete 8-bit computer emulation with video/audio.
\end{yourturn}

## Orchestration Gotchas

### Gotcha 1: Startup Synchronization
```pasm2
' WRONG - cogs start at different times
        coginit #1, ##worker1
        coginit #2, ##worker2   ' May start much later!
        
' RIGHT - synchronized start
        wrlong  #0, ##start_flag
        coginit #1, ##worker1
        coginit #2, ##worker2
        wrlong  #1, ##start_flag ' All wait for this
```

### Gotcha 2: Resource Conflicts
```pasm2
' WRONG - multiple cogs configure same resource
' Cog 1: wrpin ##MODE1, #16
' Cog 2: wrpin ##MODE2, #16  ' Conflict!

' RIGHT - designate resource owner
' Only Cog 1 configures pin 16
```

### Gotcha 3: Deadlock Scenarios
```pasm2
' WRONG - circular wait
' Cog A waits for B, B waits for C, C waits for A

' RIGHT - hierarchy prevents deadlock
' Higher number cogs never wait for lower
```

\begin{review}
🔍 \textbf{NEEDS TECHNICAL REVIEW}

Verify:
- Maximum inter-cog communication bandwidth
- Synchronization overhead measurements
- Optimal cog allocation strategies
- Real-world performance metrics
\end{review}

## The Philosophy of Parallel Mastery

Multi-cog orchestration embodies the highest principles:

1. **Divide and conquer**: Break problems into parallel pieces
2. **Communicate clearly**: Well-defined interfaces between cogs
3. **Synchronize carefully**: Not too much, not too little
4. **Balance loads**: Keep all cogs productive
5. **Design for scalability**: Patterns that grow with complexity

## The Journey Complete

From a blinking LED to an orchestrated symphony of eight processors—you've mastered the P2. You understand not just the instructions, but the philosophy. Not just the syntax, but the patterns. Not just the parts, but the whole.

The P2 isn't just a microcontroller—it's a parallel processing playground. Eight cogs aren't just processors—they're your orchestra. And you? You're no longer just a programmer—you're a parallel processing composer.

\begin{chapterend}
✨ \textbf{Congratulations! You've reached the summit!}

You've mastered: Pipeline architectures, worker pools, specialized roles, advanced synchronization, and real-world applications.

The P2 is yours to command. Eight cogs await your next composition. What will you create?

\textit{The journey doesn't end here—it transforms. Every project is a new symphony. Every challenge, a new movement. Welcome to the fellowship of P2 masters!}
\end{chapterend}# Appendices

# Appendix A: Instruction Quick Reference

## Data Movement Instructions

| Instruction | Description | Cycles | Example |
|-------------|-------------|--------|---------|
| MOV | Move source to destination | 2 | MOV pa, #42 |
| MOVS | Move to source field | 2 | MOVS instruction, #value |
| MOVD | Move to destination field | 2 | MOVD instruction, #reg |
| MOVI | Move to instruction field | 2 | MOVI instruction, #bits |
| SETS | Set source field | 2 | SETS instruction, value |
| SETD | Set destination field | 2 | SETD instruction, reg |
| SETI | Set instruction field | 2 | SETI instruction, bits |
| GETS | Get source field | 2 | GETS value, instruction |
| GETD | Get destination field | 2 | GETD reg, instruction |
| GETI | Get instruction field | 2 | GETI bits, instruction |

## Arithmetic Instructions

| Instruction | Description | Cycles | Example |
|-------------|-------------|--------|---------|
| ADD | Add S to D | 2 | ADD total, value |
| ADDS | Add signed with saturation | 2 | ADDS total, value |
| SUB | Subtract S from D | 2 | SUB count, #1 |
| SUBS | Subtract signed with saturation | 2 | SUBS count, #1 |
| MUL | Multiply (16×16→32) | 2 | MUL result, factor |
| MULS | Multiply signed | 2 | MULS result, factor |
| SCA | Scale (multiply and shift) | 2 | SCA value, factor |
| SCAS | Scale signed | 2 | SCAS value, factor |

## Logic Instructions

| Instruction | Description | Cycles | Example |
|-------------|-------------|--------|---------|
| AND | Logical AND | 2 | AND mask, pattern |
| ANDN | AND NOT (clear bits) | 2 | ANDN flags, #bit |
| OR | Logical OR | 2 | OR flags, #bit |
| XOR | Logical XOR | 2 | XOR value, #$FF |
| NOT | Logical NOT | 2 | NOT value |
| TEST | Test bits (AND without storing) | 2 | TEST flags, #bit wz |
| TESTN | Test NOT bits | 2 | TESTN flags, #bit wz |

## Shift and Rotate Instructions

| Instruction | Description | Cycles | Example |
|-------------|-------------|--------|---------|
| SHL | Shift left | 2 | SHL value, #1 |
| SHR | Shift right | 2 | SHR value, #1 |
| SAR | Shift arithmetic right | 2 | SAR value, #1 |
| ROL | Rotate left | 2 | ROL value, #1 |
| ROR | Rotate right | 2 | ROR value, #1 |
| RCL | Rotate left through carry | 2 | RCL value, #1 |
| RCR | Rotate right through carry | 2 | RCR value, #1 |
| REV | Reverse bits | 2 | REV value |

## Control Flow Instructions

| Instruction | Description | Cycles | Example |
|-------------|-------------|--------|---------|
| JMP | Jump to address | 2 | JMP #loop |
| CALL | Call subroutine | 2/4 | CALL #function |
| RET | Return from subroutine | 2/4 | RET |
| DJNZ | Decrement and jump if not zero | 2 | DJNZ count, #loop |
| TJZ | Test and jump if zero | 2 | TJZ value, #label |
| TJNZ | Test and jump if not zero | 2 | TJNZ value, #label |
| TJS | Test and jump if signed | 2 | TJS value, #label |
| TJNS | Test and jump if not signed | 2 | TJNS value, #label |

## Hub Memory Instructions

| Instruction | Description | Cycles | Example |
|-------------|-------------|--------|---------|
| RDLONG | Read long from hub | 9-16 | RDLONG value, ##address |
| WRLONG | Write long to hub | 3-10 | WRLONG value, ##address |
| RDWORD | Read word from hub | 9-16 | RDWORD value, ##address |
| WRWORD | Write word to hub | 3-10 | WRWORD value, ##address |
| RDBYTE | Read byte from hub | 9-16 | RDBYTE value, ##address |
| WRBYTE | Write byte to hub | 3-10 | WRBYTE value, ##address |
| RDFAST | Start fast read from hub | 2-17 | RDFAST #0, ##buffer |
| WRFAST | Start fast write to hub | 2-17 | WRFAST #0, ##buffer |
| RFLONG | Read long from FIFO | 2 | RFLONG value |
| WFLONG | Write long to FIFO | 2 | WFLONG value |

## Pin Instructions

| Instruction | Description | Cycles | Example |
|-------------|-------------|--------|---------|
| DRVH | Drive pin high | 2 | DRVH #16 |
| DRVL | Drive pin low | 2 | DRVL #16 |
| DRVNOT | Toggle pin | 2 | DRVNOT #16 |
| DRVZ | Float pin | 2 | DRVZ #16 |
| TESTP | Test pin state | 2 | TESTP #16 wc |
| WRPIN | Configure smart pin | 2 | WRPIN mode, #16 |
| WXPIN | Write X parameter | 2 | WXPIN value, #16 |
| WYPIN | Write Y parameter | 2 | WYPIN value, #16 |
| RDPIN | Read smart pin | 2 | RDPIN value, #16 |

## CORDIC Instructions

| Instruction | Description | Cycles | Example |
|-------------|-------------|--------|---------|
| QROTATE | Rotate vector | 8-58 | QROTATE x, angle |
| QVECTOR | Get magnitude and angle | 8-58 | QVECTOR x, y |
| QMUL | Multiply 32×32→64 | 2 | QMUL a, b |
| QDIV | Divide with remainder | 2-30 | QDIV dividend, divisor |
| QSQRT | Square root | 2-30 | QSQRT value, #0 |
| QLOG | Natural logarithm | 2-30 | QLOG value |
| QEXP | Exponential (e^x) | 2-30 | QEXP value |
| GETQX | Get CORDIC X result | 2 | GETQX result |
| GETQY | Get CORDIC Y result | 2 | GETQY result |

---

# Appendix B: Smart Pin Mode Catalog

## PWM Modes

| Mode | Name | Description | Use Case |
|------|------|-------------|----------|
| P_PWM_TRIANGLE | Triangle PWM | Triangle wave comparison | Motor control |
| P_PWM_SAWTOOTH | Sawtooth PWM | Sawtooth comparison | LED dimming |
| P_PWM_SMPS | Switch-mode PWM | SMPS optimized | Power supplies |
| P_NCO_FREQ | NCO frequency | Numerically controlled oscillator | Frequency generation |
| P_NCO_DUTY | NCO duty | NCO with duty control | Precise PWM |

## Serial Modes

| Mode | Name | Description | Use Case |
|------|------|-------------|----------|
| P_ASYNC_TX | Async transmit | UART transmit | Serial output |
| P_ASYNC_RX | Async receive | UART receive | Serial input |
| P_SYNC_TX | Sync transmit | Synchronous serial TX | SPI MOSI |
| P_SYNC_RX | Sync receive | Synchronous serial RX | SPI MISO |
| P_TRANSITION | Transitions | Output transitions | SPI clock |

## Measurement Modes

| Mode | Name | Description | Use Case |
|------|------|-------------|----------|
| P_COUNT_RISES | Count rises | Count rising edges | Frequency counter |
| P_COUNT_FALLS | Count falls | Count falling edges | Event counter |
| P_STATE_TICKS | State ticks | Time in state | Pulse width |
| P_HIGH_TICKS | High ticks | Time spent high | Duty cycle |
| P_PERIODS | Periods | Measure periods | Frequency measurement |
| P_PERIODS_HIGHS | Periods & highs | Period and high time | Complete waveform |

## Analog Modes

| Mode | Name | Description | Use Case |
|------|------|-------------|----------|
| P_ADC | ADC input | Analog to digital | Sensor input |
| P_ADC_EXT | ADC external | External ADC mode | Precision measurement |
| P_ADC_SCOPE | ADC scope | Scope trigger mode | Oscilloscope |
| P_DAC_990R_3V | DAC 990Ω 3.3V | DAC with 990Ω, 3.3V range | Audio output |
| P_DAC_600R_2V | DAC 600Ω 2V | DAC with 600Ω, 2V range | Video output |
| P_DAC_124R_1V | DAC 124Ω 1V | DAC with 124Ω, 1V range | Low voltage |
| P_COMPARE | Comparator | Analog comparator | Level detection |

## Special Modes

| Mode | Name | Description | Use Case |
|------|------|-------------|----------|
| P_REPOSITORY | Repository | 32-bit repository | Pin arrays |
| P_LOGIC_A | Logic A input | Logic input A | Custom logic |
| P_LOGIC_B | Logic B input | Logic input B | Custom logic |
| P_LOGIC_OUT | Logic output | Combinatorial output | Logic functions |
| P_QUADRATURE | Quadrature | Quadrature decoder | Encoders |
| P_USB_PAIR | USB pair | USB D+/D- pair | USB communication |
| P_HDMI | HDMI output | HDMI encoding | Video output |

---

# Appendix C: CORDIC Operations

## Angle Format

The P2 uses a 32-bit angle format where:
- 0° = $00000000
- 90° = $40000000
- 180° = $80000000
- 270° = $C0000000
- 360° = $100000000 (wraps to 0)

Conversion formulas:
- Degrees to P2: angle_p2 = degrees × $100000000 / 360
- Radians to P2: angle_p2 = radians × $100000000 / (2π)
- P2 to degrees: degrees = angle_p2 × 360 / $100000000

## CORDIC Timing

| Operation | Min Cycles | Max Cycles | Typical |
|-----------|------------|------------|---------|
| QROTATE | 8 | 58 | 32 |
| QVECTOR | 8 | 58 | 32 |
| QMUL | 2 | 2 | 2 |
| QDIV | 2 | 30 | 16 |
| QSQRT | 2 | 30 | 16 |
| QLOG | 2 | 30 | 16 |
| QEXP | 2 | 30 | 16 |

## Fixed-Point Formats

### 16.16 Format
- Upper 16 bits: Integer part
- Lower 16 bits: Fractional part
- 1.0 = $00010000
- 0.5 = $00008000
- -1.0 = $FFFF0000

### 5.27 Format (Logarithms)
- Upper 5 bits: Integer part
- Lower 27 bits: Fractional part
- Used for QLOG and QEXP

## CORDIC Examples

### Calculate Sin and Cos
```pasm2
' sin(45°) and cos(45°)
        mov     angle, ##$20000000      ' 45 degrees
        qrotate ##$7FFFFFFF, angle     ' Unit vector
        getqx   cos_val                 ' cos(45°) ≈ 0.707
        getqy   sin_val                 ' sin(45°) ≈ 0.707
```

### Calculate Magnitude
```pasm2
' magnitude = sqrt(x² + y²)
        setq    y
        qvector x, #0
        getqx   magnitude
```

### 32×32 Multiply
```pasm2
' result = a × b (64-bit result)
        qmul    a, b
        getqx   result_lo               ' Lower 32 bits
        getqy   result_hi               ' Upper 32 bits
```

---

# Appendix D: Pin Selection Guidelines

## Pin Categories

### Universal Pins (16-47)
- Safe for all examples and tutorials
- No board-specific functions
- Ideal for learning and prototyping
- 32 pins total

### Lower Pins (0-15)
- Often connected to board peripherals
- May have LEDs, buttons, or sensors
- Check board documentation
- 16 pins total

### Upper Pins (48-63)
- Pins 48-55: Board-specific uses
- Pins 56-57: Boot I2C EEPROM (usually)
- Pins 58-61: Boot SPI flash (usually)
- Pins 62-63: Serial programming (TX/RX)
- 16 pins total

## Board-Specific Allocations

### P2 Eval Board
- Pins 0-7: LEDs
- Pins 8-15: DIP switches
- Pins 16-31: Breadboard area
- Pins 32-47: Headers
- Pins 56-57: I2C EEPROM
- Pins 58-61: SPI flash
- Pins 62-63: USB serial

### P2 Edge Module
- Pins vary by carrier board
- Check carrier documentation
- Pins 56-63 typically reserved

## Best Practices

1. **Start with pins 16-47** for new projects
2. **Document pin usage** in code comments
3. **Check for conflicts** before using pins
4. **Reserve pins 56-63** for boot and programming
5. **Group related signals** (e.g., SPI pins adjacent)
6. **Consider noise** - separate analog from digital
7. **Plan for expansion** - leave pins available

## Pin Pairing

Some functions work best with specific pin pairs:

| Function | Pin Requirements |
|----------|------------------|
| Differential | Adjacent odd/even pairs |
| USB | Pins n and n+1 |
| HDMI | 4 consecutive pins |
| Quadrature | 2 pins (any) |
| I2C | 2 pins (any) with pull-ups |
| SPI | 3-4 pins (any arrangement) |

---

# Appendix E: Timing and Performance

## Clock Speeds

| Frequency | Period | Instruction Time | Use Case |
|-----------|--------|------------------|----------|
| 20 MHz | 50 ns | 100 ns | Low power |
| 50 MHz | 20 ns | 40 ns | Typical USB |
| 100 MHz | 10 ns | 20 ns | Standard |
| 180 MHz | 5.6 ns | 11.1 ns | Performance |
| 200 MHz | 5 ns | 10 ns | Maximum rated |
| 300 MHz | 3.3 ns | 6.7 ns | Overclocked |

## Instruction Timing

### Cog Execution
- Most instructions: 2 clocks
- Hub access: 9-16 clocks (read), 3-10 clocks (write)
- CORDIC simple: 2 clocks
- CORDIC complex: 8-58 clocks
- Jumps: 2 clocks (4 if taken)
- Interrupts: 3 clock latency

### Hub Execution
- Sequential code: ~3 clocks per instruction
- Random jumps: 5-11 clocks per instruction
- Hub window: Every cog gets access every 8 clocks
- FIFO depth: 64 longs

## Memory Bandwidth

| Operation | Speed at 100MHz |
|-----------|-----------------|
| Cog RAM | 6.4 GB/s per cog |
| Hub read (burst) | 400 MB/s |
| Hub write (burst) | 400 MB/s |
| Streamer | 400 MB/s |
| Pin I/O | 100 MHz toggle rate |

## Power Consumption

| Mode | Current (typical) |
|------|-------------------|
| 1 cog at 20 MHz | ~10 mA |
| 1 cog at 180 MHz | ~50 mA |
| 8 cogs at 180 MHz | ~200 mA |
| Plus I/O current | Varies by load |

## Deterministic Timing

The P2 provides deterministic timing for:
- Instruction execution (no cache misses)
- Hub access (egg beater ensures fairness)
- Pin I/O (smart pins handle timing)
- Interrupts (fixed latency)

This makes the P2 ideal for:
- Real-time control
- Video generation
- Protocol implementation
- Precision measurement

---

# Index

## A
- **ADC modes**: 159, 287
- **ADD instruction**: 23, 45-47, 255
- **Address modes**: 67-69
- **Alignment, hub memory**: 89-91
- **Analog I/O**: 159-161
- **Architecture overview**: 15-30
- **Arithmetic instructions**: 255
- **Attention system**: 191-193

## B
- **Binary masks**: 16-22
- **Blink program**: 1-14
- **Block transfer**: 71-73
- **Branches**: 79-82
- **Buffer, circular**: 71, 127-129

## C
- **C flag**: 79-81
- **Cache considerations**: 207
- **CALL instruction**: 82, 255
- **Circular buffer**: 71, 127-129
- **Clock speeds**: 301
- **CMP instruction**: 80-81
- **Cog communication**: 47-62
- **Cog RAM**: 31-35
- **Cogs, architecture**: 15-18
- **Comparison instructions**: 80-81
- **Conditional execution**: 79-94
- **Control flow**: 255
- **CORDIC engine**: 159-174, 287-289
- **CORDIC operations**: 287-289
- **CORDIC timing**: 287

## D
- **DAC modes**: 159, 287
- **Data movement**: 255
- **Debugging**: 239-241
- **Digital filters**: 223-226
- **Division**: 63-65
- **DJNZ instruction**: 82, 255

## E
- **Egg beater**: 47-49
- **Event system**: 111-114, 191-194
- **Events vs interrupts**: 111-112

## F
- **FFT**: 226-228
- **FIFO operations**: 127-130
- **Filtering, digital**: 223-226
- **Fixed-point math**: 65-67, 289
- **Flags (Z and C)**: 79-81
- **Frequency measurement**: 97-99

## G
- **GETQX/GETQY**: 159-161
- **Graphics primitives**: 191-193

## H
- **HDMI output**: 194-195
- **Hub arbitration**: 47-49
- **Hub execution**: 143-158
- **Hub instructions**: 256
- **Hub memory**: 35-37
- **Hub timing**: 47-49

## I
- **I2C protocol**: 209-211
- **Immediate values**: 12-13
- **Index registers**: 35
- **Instruction reference**: 255-257
- **Instruction timing**: 301
- **Interrupts**: 111-126
- **Interrupt priorities**: 113-114

## J
- **JMP instruction**: 82, 255
- **Jump tables**: 82-83

## L
- **Locks**: 49-52, 191-193
- **Logic instructions**: 255
- **LUT operations**: 130-131

## M
- **Mailbox system**: 52-53, 239-240
- **Mathematics**: 63-78
- **Memory bandwidth**: 301
- **Memory map**: 35-36
- **MOV instruction**: 31-32, 255
- **Multi-cog patterns**: 239-254
- **Multiplication**: 63-64

## N
- **NCO modes**: 131-132

## O
- **Orchestration patterns**: 239-254

## P
- **Parallel processing**: 15-17, 239-254
- **Pattern recognition**: 230-231
- **Performance metrics**: 301-302
- **PID control**: 229-230
- **Pin instructions**: 256
- **Pin selection**: 295-297
- **Pipeline architecture**: 239-241
- **Power consumption**: 302
- **PWM generation**: 95-97

## Q
- **QDIV instruction**: 64-65
- **QMUL instruction**: 63-64
- **QROTATE instruction**: 159-160
- **Quadrature decoding**: 99-100
- **Quick reference**: 255-257

## R
- **RDLONG/WRLONG**: 35-37, 256
- **Real-time processing**: 223-238
- **Rotate instructions**: 255

## S
- **Self-modifying code**: 69-70
- **Serial protocols**: 207-222
- **Shift instructions**: 255
- **Signal processing**: 223-238
- **Sine/cosine**: 159-160
- **Smart Pin modes**: 95-110, 271-273
- **Smart Pins**: 18-19, 95-110
- **SPI protocol**: 208-209
- **Sprite system**: 193-194
- **Square root**: 161
- **Streaming data**: 127-142
- **Streamer**: 128-130
- **Synchronization**: 191-206

## T
- **TEST instruction**: 81
- **Tile graphics**: 192-193
- **Timing, deterministic**: 302
- **Timing reference**: 301-302
- **Trigonometry**: 159-161

## U
- **UART protocol**: 207-208

## V
- **Vector operations**: 160-161
- **VGA generation**: 191-192
- **Video generation**: 191-206

## W
- **WAITX instruction**: 12-13
- **Worker pool pattern**: 240-241

## X
- **XINIT instruction**: 128-130

## Z
- **Z flag**: 79-81
- **Zero-crossing detection**: 230-231

---

*End of Manual*

**P2 Assembly: In the Spirit of deSilva's P1 Tutorial**

