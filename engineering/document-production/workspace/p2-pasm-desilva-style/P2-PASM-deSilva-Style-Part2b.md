# Chapter 9: Streaming Data

Data is like water—sometimes you need a bucket, sometimes a fire hose. The P2's streaming system gives you both. With the FIFO and streamer, you can move megabytes per second without your cog breaking a sweat. Let's open the floodgates!

## The Hook: DMA Without the Drama

Remember copying arrays byte by byte? Or bit-banging video signals? The P2's streamer laughs at such primitive methods. It's like having a dedicated highway for data, complete with automatic traffic control. Your cog sets the destination and source, then gets back to important work while data flows in the background.

## The FIFO: Your Data Pipeline

The FIFO (First In, First Out) is a 64-long buffer between cog and hub:

```pasm2
' Set up FIFO for reading hub data
        rdfast  #0, ##source_data       ' Start fast read
        
' Read sequential data at maximum speed
.loop   rflong  value                   ' Read next long from FIFO
        ' Process value...
        ' FIFO automatically refills from hub!
        djnz    count, #.loop
```

### FIFO Modes and Operations

| Operation | Purpose | Speed |
|-----------|---------|-------|
| RDFAST | Start hub→cog streaming | Setup only |
| WRFAST | Start cog→hub streaming | Setup only |
| RFLONG | Read next long from FIFO | 2 clocks |
| RFWORD | Read next word from FIFO | 2 clocks |
| RFBYTE | Read next byte from FIFO | 2 clocks |
| WFLONG | Write long to FIFO | 2 clocks |

\begin{sidetrack}
\textbf{Why 64 Longs?}

The FIFO size is a sweet spot. It's large enough to hide hub latency (the FIFO refills while you process), but small enough to fit in the cog without using precious cog RAM. At 64 longs, you can stream continuously at nearly cog RAM speeds!
\end{sidetrack}

## The Streamer: Hardware Data Mover

The streamer is like the FIFO's big brother—it can move data to/from pins automatically:

```pasm2
' Stream data to pins for video generation
        wrpin   ##P_SYNC_TX, #0         ' Configure pins 0-7
        wxpin   #%1_00111, #0           ' 8-bit mode
        dirh    #7<<6 | #0              ' Enable pins 0-7
        
' Configure streamer for 8-bit parallel output
        mov     pa, ##DM_8BIT_PINS      ' 8-bit to pins mode
        or      pa, #0                  ' Starting at pin 0
        setdacs pa                      ' Configure streamer
        
' Start streaming from hub
        rdfast  #0, ##video_buffer      ' Point FIFO at data
        xinit   ##X_8BIT_LUT, #0        ' Start streaming!
        
' Streamer now runs independently!
' Your cog is free to do other work
```

### Streamer Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| 1-bit serial | Stream bits to one pin | Serial protocols |
| 2/4/8-bit parallel | Multiple pins simultaneously | Parallel interfaces |
| 16/32-bit parallel | Wide parallel output | Memory interfaces |
| LUT lookup | Use LUT as palette | Video generation |
| ADC sampling | Stream from pins to hub | Data acquisition |
| NCO (Numerically Controlled Oscillator) | Frequency generation | Audio, RF |

## Video Generation with the Streamer

Here's where the streamer truly shines:

```pasm2
' VGA signal generation (640x480)
vga_driver
        rdfast  #0, ##screen_buffer     ' Point to video data
        
' Horizontal sync pulse
hsync   xcont   ##M_SYNC, #0            ' Sync pulse
        xcont   ##M_BACK_PORCH, #0      ' Back porch
        
' Stream visible pixels
        xcont   ##M_VISIBLE, #0         ' 640 pixels
        
        xcont   ##M_FRONT_PORCH, #0     ' Front porch
        
' Check for end of frame
        djnz    line_count, #hsync
        jmp     #new_frame
```

\begin{interlude}
\textbf{The Streaming Revolution}

Traditional microcontrollers need the CPU to move every byte for video. The P2's streamer does it in hardware, leaving your cog free to generate the next frame, handle sprites, or run game logic. It's the difference between being a one-person band and having a backing orchestra.
\end{interlude}

## LUT as Color Palette

The LUT (Look-Up Table) works with the streamer for indexed color:

```pasm2
' Load 256-color palette into LUT
        mov     ptrb, ##palette_data
        mov     pa, #0
        
.load   rdlong  color, ptrb++
        wrlut   color, pa
        add     pa, #1
        cmp     pa, #256 wz
if_nz   jmp     #.load

' Configure streamer to use LUT
        setcy   ##CYCLES_PER_PIXEL
        setcq   ##$FF                   ' 8-bit LUT mode
        
' Stream pixels through LUT
        xinit   ##X_8BIT_LUT, #0        ' Each byte indexes LUT
```

## High-Speed Data Acquisition

Stream data from pins to hub:

```pasm2
' Sample 8 pins at high speed
        wrfast  #0, ##sample_buffer     ' Destination in hub
        
' Configure streamer for input
        setdacs ##DM_8BIT_PINS_IN | #16 ' Read pins 16-23
        
' Start acquisition
        xinit   ##X_SAMPLES, #0         ' Sample count
        
' Wait for completion
        waitxfi                         ' Wait for streamer done
```

## Streaming Patterns

### Pattern 1: Double Buffering
```pasm2
' Two buffers for seamless streaming
buffer_a    long    $4000
buffer_b    long    $5000
current     long    0

' Stream from one while filling other
stream  xor     current, #1             ' Toggle buffer
        mov     pa, buffer_a
        test    current, #1 wz
if_nz   mov     pa, buffer_b
        
        rdfast  #0, pa                  ' Stream from current
        ' Fill other buffer while streaming...
```

### Pattern 2: Circular Buffer Streaming
```pasm2
' Continuous streaming with wrap
        rdfast  ##$8000_0000, ##buffer  ' Bit 31 = wrap mode
        
' Stream continuously
.loop   rflong  data
        ' Process data...
        ' FIFO wraps automatically at buffer end!
        jmp     #.loop
```

### Pattern 3: Format Conversion
```pasm2
' Convert 8-bit samples to 16-bit while streaming
.convert
        rfbyte  sample                  ' Get 8-bit sample
        shl     sample, #8              ' Convert to 16-bit
        or      sample, sample          ' Duplicate for stereo
        wrlong  sample, ptra++          ' Store 16-bit
        djnz    count, #.convert
```

\begin{missing}
🚧 \textbf{CONTENT MISSING - COMING SOON}

Need to add:
- Complete streamer command encoding
- DDS/NCO mode for frequency synthesis
- Goertzel mode for frequency detection
- HDMI output patterns
- USB streaming configurations
\end{missing}

## Your Turn: Stream Master

\begin{yourturn}
\textbf{Challenge 1: Audio Player}
Stream WAV file data from hub to DAC pins.

\textbf{Challenge 2: Logic Analyzer}
Capture 8 digital signals to hub memory at high speed.

\textbf{Challenge 3: VGA Text Mode}
Generate 80x25 text display using LUT for font.

\textbf{Challenge 4: Data Logger}
Stream ADC samples continuously to a circular buffer.

\textbf{Challenge 5: Pattern Generator}
Output test patterns to 8 pins from hub data.
\end{yourturn}

## Streaming Gotchas

### Gotcha 1: FIFO Conflicts
```pasm2
' WRONG - FIFO used by both!
        rdfast  #0, ##data1
        xinit   ##X_STREAM, #0  ' Streamer uses FIFO too!
        rflong  value           ' Conflicts with streamer!
        
' RIGHT - One at a time
        rdfast  #0, ##data1
        rflong  value           ' Use FIFO
        ' ... finish FIFO operations ...
        xinit   ##X_STREAM, #0  ' Now streamer can use it
```

### Gotcha 2: Timing Criticality
```pasm2
' WRONG - missed data!
.loop   rflong  value
        ' Long processing...     ' FIFO might underrun!
        djnz    count, #.loop
        
' RIGHT - keep up with stream
.loop   rflong  value
        wrlong  value, ptra++   ' Quick operation
        djnz    count, #.loop
```

### Gotcha 3: Hub Alignment
```pasm2
' WRONG - misaligned streaming
        rdfast  #0, ##buffer+1  ' Not long-aligned!
        
' RIGHT - align to long boundary
        rdfast  #0, ##buffer    ' Long-aligned address
```

\begin{review}
🔍 \textbf{NEEDS TECHNICAL REVIEW}

Need to verify:
- Exact streamer command bit patterns
- FIFO refill timing and thresholds
- Maximum streaming rates for each mode
- LUT color format specifications
\end{review}

## The Philosophy of Streaming

The P2's streaming embodies key principles:

1. **Hardware does heavy lifting**: Move data without CPU
2. **Parallelism everywhere**: Stream while processing
3. **Flexibility in modes**: Serial, parallel, LUT, NCO
4. **Deterministic timing**: Predictable data flow

\begin{chapterend}
✨ \textbf{You're now a streaming data maestro!}

You've learned: FIFO for fast hub access, streamer for automatic data movement, video generation techniques, and high-speed acquisition patterns.

Next: Chapter 10 breaks free from the 2KB limit with hub execution!
\end{chapterend}

---

# Chapter 10: Hub Execution

Two kilobytes. That's all the code space a cog has. But what if your program is bigger? What if you need complex algorithms, large lookup tables, or just more code? Hub execution breaks the chains, giving you access to all 512KB while still running on a cog. Freedom never felt so good!

## The Hook: From Studio Apartment to Mansion

Cog RAM is like a studio apartment—cozy, everything within reach, but cramped. Hub execution is like moving to a mansion—room to spread out, but it takes longer to get anywhere. The P2 lets you use both: live in the studio for speed-critical code, visit the mansion for everything else.

## Hub Execution Basics

Jumping to hub code is simple:

```pasm2
' In cog RAM
        org     0
start   mov     pa, #42
        jmp     ##hub_code      ' Jump to hub (## = absolute)
        
' In hub RAM
        orgh    $4000           ' Hub origin
hub_code
        add     pa, #100        ' This runs from hub!
        mul     pa, #2
        ' ... hundreds more instructions ...
        jmp     #start          ' Jump back to cog
```

### Performance Differences

| Execution Location | Speed | Code Size | Best For |
|-------------------|-------|-----------|----------|
| Cog RAM | 2 clocks/instruction | 2KB max | Tight loops, drivers |
| Hub RAM | 3-11 clocks/instruction | 512KB max | Complex algorithms |
| Hub with FIFO | ~3 clocks/instruction | 512KB max | Sequential code |

\begin{sidetrack}
\textbf{The Hub Execution Secret}

Hub execution uses the FIFO to prefetch instructions. If your code is sequential (no jumps), it runs almost as fast as cog code. But every jump flushes the FIFO, causing a delay. This is why hub execution loves straight-line code and hates jumpy spaghetti.
\end{sidetrack}

## Mixed Execution Strategies

### Strategy 1: Fast Core, Big Library
```pasm2
' Core loop in cog (fast)
        org     0
main_loop
        call    ##process_data  ' Call hub routine
        call    ##update_display
        call    ##check_inputs
        jmp     #main_loop
        
' Libraries in hub (big)
        orgh    $4000
process_data
        ' Complex processing...
        ret
        
update_display
        ' Display handling...
        ret
```

### Strategy 2: Speed-Critical Islands
```pasm2
' Most code in hub
        orgh    $1000
main    ' Setup code...
        call    #fast_routine   ' Call cog routine
        ' More hub code...
        
' Speed-critical in cog
        org     0
fast_routine
        ' Time-critical code
        setq    #16-1           ' Fast block copy
        rdlong  0, ptra
        ' Process in cog RAM (fast!)
        setq    #16-1
        wrlong  0, ptrb
        jmp     ##main          ' Back to hub
```

### Strategy 3: Overlay System
```pasm2
' Load different code sections as needed
        org     0
loader  mov     target, ##overlay_1
        call    #load_overlay
        call    #overlay_area   ' Run it
        
        mov     target, ##overlay_2
        call    #load_overlay
        call    #overlay_area   ' Run different code
        
load_overlay
        setq    ##512-1         ' Load 512 longs
        rdlong  overlay_area, target
        ret
        
overlay_area
        res     512             ' Reserve space
```

## Hub Execution Optimization

### Tip 1: Minimize Jumps
```pasm2
' BAD - Many jumps, FIFO thrashing
loop    rdlong  pa, ptra++
        cmp     pa, #0 wz
if_z    jmp     #skip           ' Jump flushes FIFO
        add     total, pa
skip    djnz    count, #loop    ' Another jump
        
' GOOD - Conditional execution, no jumps
loop    rdlong  pa, ptra++
        cmp     pa, #0 wz
if_nz   add     total, pa       ' No jump needed!
        djnz    count, #loop    ' Only one jump
```

### Tip 2: Align Critical Code
```pasm2
' Align hot functions to long boundaries
        alignl                  ' Align to next long
critical_function
        ' Time-sensitive code here
        ' Better FIFO efficiency
```

### Tip 3: Batch Operations
```pasm2
' Process multiple items per iteration
        orgh
process_batch
        rdlong  val1, ptra[0]
        rdlong  val2, ptra[1]
        rdlong  val3, ptra[2]
        rdlong  val4, ptra[3]
        add     ptra, #16
        
        ' Process all 4 values
        ' Fewer jumps = better performance
```

\begin{interlude}
\textbf{The FIFO Dance}

Think of the FIFO as a patient assistant. When you execute sequentially, it runs ahead, fetching instructions before you need them. But when you jump, it has to stop, dump everything, and start over at the new location. This is why hub execution rewards predictable code flow.
\end{interlude}

## Large Data Structures in Hub

Hub execution shines with big data:

```pasm2
        orgh    $8000
        
' Large lookup table
sine_table
        long    $0000, $00C9, $0192, $025B
        long    $0324, $03ED, $04B6, $057F
        ' ... 1024 entries ...
        
' Access from hub execution
lookup_sine
        and     angle, ##$3FF   ' 10-bit angle
        shl     angle, #2       ' Convert to byte offset
        add     angle, ##sine_table
        rdlong  result, angle
        ret
```

## Advanced Hub Execution Techniques

### Technique 1: Computed Jumps
```pasm2
        orgh
dispatch
        shl     command, #2     ' Commands are longs
        add     command, ##jump_table
        rdlong  target, command
        jmp     target          ' Indirect jump
        
jump_table
        long    cmd_read
        long    cmd_write
        long    cmd_erase
        long    cmd_verify
```

### Technique 2: Hub Subroutine Library
```pasm2
' Standard library in hub
        orgh    $10000
        
' String functions
strlen  mov     count, #0
.loop   rdbyte  pa, ptrb++ wz
if_nz   add     count, #1
if_nz   jmp     #.loop
        ret
        
strcmp  ' String compare...
        ret
        
strcpy  ' String copy...
        ret
```

### Technique 3: Self-Modifying Hub Code
```pasm2
' Hub code CAN be self-modifying!
        orgh
modify_me
        mov     pa, #0          ' This 0 will change
        
' Modify the immediate value
        mov     pb, ##modify_me
        rdlong  instruction, pb
        andn    instruction, ##$1FF
        or      instruction, #42 ' New immediate
        wrlong  instruction, pb
        
' Now it executes with new value
        call    ##modify_me     ' pa = 42
```

\begin{missing}
🚧 \textbf{CONTENT MISSING - COMING SOON}

Need to add:
- SKIPF patterns in hub execution
- Hub execution with interrupts
- Debugging hub code
- Performance profiling techniques
- Code caching strategies
\end{missing}

## Your Turn: Hub Execution Mastery

\begin{yourturn}
\textbf{Challenge 1: Menu System}
Implement a large menu system in hub with fast response code in cog.

\textbf{Challenge 2: Compression Algorithm}
Port a compression algorithm that needs more than 2KB of code.

\textbf{Challenge 3: Interpreter}
Create a simple bytecode interpreter that runs from hub.

\textbf{Challenge 4: Graphics Library}
Build a graphics library with line, circle, and polygon functions in hub.

\textbf{Challenge 5: Performance Test}
Compare hub vs cog execution speed for various algorithms.
\end{yourturn}

## Hub Execution Gotchas

### Gotcha 1: Address Confusion
```pasm2
' WRONG - mixing address spaces
        org     0
        jmp     #hub_code       ' # is cog-relative!
        
        orgh    $4000
hub_code
        
' RIGHT - use ## for absolute
        jmp     ##hub_code      ' ## is absolute address
```

### Gotcha 2: FIFO Conflicts
```pasm2
' WRONG - FIFO used for execution AND data
        orgh
        rdfast  #0, ##buffer    ' FIFO for data
        rflong  pa              ' Breaks hub execution!
        
' RIGHT - save/restore FIFO
        push    ptra            ' Save FIFO state
        rdfast  #0, ##buffer
        rflong  pa
        pop     ptra            ' Restore for execution
```

### Gotcha 3: Timing Assumptions
```pasm2
' WRONG - assumes cog timing
        orgh
        waitx   #2              ' NOT 2 clocks in hub!
        
' RIGHT - account for hub timing
        waitx   #8              ' Adjust for hub speed
```

\begin{review}
🔍 \textbf{NEEDS TECHNICAL REVIEW}

Please verify:
- Exact hub execution timing per instruction type
- FIFO depth and refill behavior
- Impact of hub window alignment
- Maximum sustainable hub execution rate
\end{review}

## The Philosophy of Hub Execution

Hub execution embodies a key principle: **Use the right tool for the job**

1. **Cog RAM**: Fast, small, deterministic
2. **Hub RAM**: Large, flexible, good enough
3. **Mixed Mode**: Best of both worlds
4. **Know Your Needs**: Profile, measure, optimize

\begin{chapterend}
✨ \textbf{You've broken free from the 2KB limit!}

You've mastered: Hub execution basics, mixed execution strategies, optimization techniques, and large-scale program organization.

Next: Chapter 11 dives deep into the CORDIC engine—your mathematical supercomputer!
\end{chapterend}

---

# Chapter 11: The CORDIC Engine

Hidden inside every P2 cog is a mathematical genius—the CORDIC engine. It can calculate sine, cosine, logarithms, square roots, and even rotate vectors, all in hardware. No lookup tables. No approximations. Just pure mathematical precision delivered at silicon speed. Welcome to math paradise!

## The Hook: From Algebra to Alchemy

Remember implementing sine functions with Taylor series? Or lookup tables eating precious memory? The CORDIC laughs at such primitive ways. It transforms complex mathematics into simple hardware operations. One instruction starts it, another retrieves the result. It's like having Wolfram Alpha in silicon.

## CORDIC Fundamentals

CORDIC (COordinate Rotation DIgital Computer) uses only shifts and adds to compute complex functions:

```pasm2
' Calculate sine and cosine simultaneously
        mov     angle, ##$4000_0000     ' 90 degrees
        qrotate #$7FFF, angle           ' Max amplitude, rotate
        
' Wait minimum 8 clocks for simple operations
        nop                             ' Could do other work
        
' Get results
        getqx   cosine                  ' cos(90°) = 0
        getqy   sine                    ' sin(90°) = 32767
```

### CORDIC Operations

| Operation | Command | Clocks | Result |
|-----------|---------|--------|--------|
| Rotate | QROTATE | 8-58 | X,Y rotated |
| Vector | QVECTOR | 8-58 | Magnitude, angle |
| Multiply | QMUL | 2 | 32×32→64 bit |
| Divide | QDIV | 2-30 | Quotient, remainder |
| Square Root | QSQRT | 2-30 | Square root |
| Logarithm | QLOG | 2-30 | Natural log |
| Exponential | QEXP | 2-30 | e^x |

\begin{sidetrack}
\textbf{The CORDIC Magic}

CORDIC works by rotating vectors through progressively smaller angles. Each iteration doubles precision. It's like zooming in on the answer, getting closer with each step. The P2 does this in hardware, completing in microseconds what would take software milliseconds.
\end{sidetrack}

## Trigonometric Functions

### Full Circle Rotation
```pasm2
' Generate points around a circle
        mov     radius, #100
        mov     angle, #0
        mov     count, #360
        
.circle add     angle, ##$0100_0000     ' ~3.5 degrees
        qrotate radius, angle
        getqx   x                       ' X coordinate
        getqy   y                       ' Y coordinate
        
        ' Plot point at (x,y)
        call    #plot_point
        
        djnz    count, #.circle
```

### Angle Measurement
```pasm2
' Find angle from (0,0) to (x,y)
        mov     x, #100
        mov     y, #100
        
        setq    y                       ' Y in Q register
        qvector x, #0                   ' Start vectoring
        
        getqx   magnitude               ' Distance to point
        getqy   angle                   ' Angle (45° here)
```

### Precision Sine Wave
```pasm2
' High-precision sine wave generation
        mov     phase, #0
        mov     delta, ##$0010_0000     ' Frequency
        
.wave   qrotate ##$7FFF_FFFF, phase    ' Maximum precision
        getqy   sample                  ' 32-bit sine value
        
        ' Output to DAC
        shr     sample, #16             ' Scale to 16-bit
        add     sample, ##$8000         ' Offset to unsigned
        wypin   sample, #DAC_PIN
        
        add     phase, delta
        jmp     #.wave
```

## Advanced Mathematics

### Natural Logarithm
```pasm2
' Calculate ln(x)
        mov     value, ##1000
        qlog    value
        getqx   result                  ' ln(1000) = 6.907...
        
' Result is in 5.27 fixed-point format
        shr     result, #27             ' Integer part = 6
```

### Exponential Function
```pasm2
' Calculate e^x
        mov     power, ##$0200_0000     ' 2.0 in fixed-point
        qexp    power
        getqx   result                  ' e^2 = 7.389...
```

### Square Root with Remainder
```pasm2
' Integer square root
        mov     value, ##1000000
        qsqrt   value, #0
        getqx   root                    ' 1000
        getqy   remainder               ' 0
        
' Fractional square root
        mov     value, ##2
        shl     value, #30              ' Scale up
        qsqrt   value, #0
        getqx   root                    ' Scaled √2
```

\begin{interlude}
\textbf{Fixed-Point Formats}

The CORDIC uses various fixed-point formats:
- Angles: 32-bit, full circle = $1_0000_0000
- Logarithms: 5.27 format (5 integer, 27 fractional bits)
- General: Often 16.16 or custom formats

Understanding these formats is key to CORDIC mastery.
\end{interlude}

## 3D Graphics with CORDIC

```pasm2
' 3D point rotation
' Rotate point (x,y,z) around Z axis
rotate_z
        setq    y
        qrotate x, angle_z
        getqx   new_x
        getqy   new_y
        ' Z unchanged for Z-axis rotation
        
' Rotate around X axis
rotate_x
        setq    z
        qrotate y, angle_x
        getqx   new_y
        getqy   new_z
        ' X unchanged for X-axis rotation
        
' Perspective projection
project mov     pa, ##FOCAL_LENGTH
        qmul    pa, x
        qdiv    pa, z
        getqx   screen_x
        
        qmul    pa, y
        qdiv    pa, z
        getqx   screen_y
```

## Signal Processing

### FFT Butterfly
```pasm2
' Complex multiplication for FFT
' (a+bi) * (c+di) = (ac-bd) + (ad+bc)i
complex_mul
        qmul    a, c            ' ac
        getqx   real_part
        qmul    b, d            ' bd
        getqx   pa
        sub     real_part, pa   ' ac-bd
        
        qmul    a, d            ' ad
        getqx   imag_part
        qmul    b, c            ' bc
        getqx   pa
        add     imag_part, pa   ' ad+bc
```

### Digital Filter
```pasm2
' IIR filter using CORDIC multiply
' y[n] = a0*x[n] + a1*x[n-1] - b1*y[n-1]
iir_filter
        qmul    x_n, a0
        getqx   acc
        
        qmul    x_n1, a1
        getqx   pa
        add     acc, pa
        
        qmul    y_n1, b1
        getqx   pa
        sub     acc, pa
        
        mov     y_n, acc        ' Output
        mov     x_n1, x_n       ' Update history
        mov     y_n1, y_n
```

\begin{missing}
🚧 \textbf{CONTENT MISSING - COMING SOON}

Need to add:
- Hyperbolic functions (sinh, cosh, tanh)
- Arc functions (asin, acos, atan)
- Complex number operations
- Matrix operations with CORDIC
- Detailed timing for each operation
\end{missing}

## CORDIC Patterns

### Pattern 1: Coordinate Transformation
```pasm2
' Convert polar to Cartesian
polar_to_cart
        qrotate radius, angle
        getqx   x
        getqy   y
        ret
        
' Convert Cartesian to polar
cart_to_polar
        setq    y
        qvector x, #0
        getqx   radius
        getqy   angle
        ret
```

### Pattern 2: Animation Curves
```pasm2
' Smooth ease-in-out curve
        qlog    progress        ' Log curve
        getqx   pa
        qexp    pa              ' Smooth S-curve
        getqx   smoothed
```

### Pattern 3: Random Direction
```pasm2
' Random unit vector
        getrnd  angle           ' Random angle
        qrotate #$7FFF, angle   ' Unit vector
        getqx   rand_x
        getqy   rand_y
```

## Your Turn: CORDIC Wizardry

\begin{yourturn}
\textbf{Challenge 1: Plasma Effect}
Generate a plasma effect using sine/cosine combinations.

\textbf{Challenge 2: 3D Wireframe Cube}
Rotate and project a 3D cube using CORDIC.

\textbf{Challenge 3: Audio Synthesizer}
Create multiple waveforms using CORDIC functions.

\textbf{Challenge 4: Mandelbrot Set}
Calculate Mandelbrot fractal using complex multiplication.

\textbf{Challenge 5: PID Controller}
Implement a PID control loop using CORDIC math.
\end{yourturn}

## CORDIC Gotchas

### Gotcha 1: Timing Requirements
```pasm2
' WRONG - result not ready!
        qrotate x, angle
        getqx   result          ' Too soon!
        
' RIGHT - wait for completion
        qrotate x, angle
        waitx   #8-2            ' Minimum 8 clocks
        getqx   result
```

### Gotcha 2: Format Confusion
```pasm2
' WRONG - mixing formats
        mov     angle, #90      ' Degrees don't work!
        
' RIGHT - use CORDIC angle format
        mov     angle, ##$2000_0000  ' 45 degrees
```

### Gotcha 3: Pipeline Conflicts
```pasm2
' WRONG - overwriting operation
        qmul    a, b
        qdiv    c, d            ' Cancels multiply!
        
' RIGHT - wait for completion
        qmul    a, b
        getqx   result
        qdiv    c, d
        getqx   quotient
```

\begin{review}
🔍 \textbf{NEEDS TECHNICAL REVIEW}

Verify:
- Exact cycle counts for all operations
- Fixed-point format specifications
- Maximum precision achievable
- Pipeline behavior with multiple operations
\end{review}

## The Philosophy of CORDIC

The CORDIC engine represents a profound idea:

1. **Complex from simple**: Shifts and adds create transcendental functions
2. **Hardware acceleration**: What's hard in software is easy in silicon
3. **Parallel processing**: Each cog has its own CORDIC
4. **Mathematical elegance**: One algorithm, many functions

\begin{chapterend}
✨ \textbf{You're now a CORDIC calculation wizard!}

You've mastered: Trigonometric functions, logarithms and exponentials, 3D transformations, signal processing, and the mathematical power of hardware acceleration.

Next: Chapter 12 explores advanced synchronization with events and locks!
\end{chapterend}

---

# Chapter 12: Events and Locks

Eight cogs working independently is powerful. Eight cogs working together is unstoppable. But coordination requires communication, and communication requires synchronization. Events and locks are your tools for orchestrating the perfect multi-cog symphony. Let's learn to conduct!

## The Hook: The Orchestra Conductor's Baton

Imagine conducting an orchestra where musicians can't see you or each other. How do they stay in sync? That's the challenge of multi-cog programming. Events are your baton movements—signals that cogs can watch for. Locks are your section leaders—ensuring only one plays the solo at a time. Together, they transform chaos into harmony.

## Advanced Event Architecture

Beyond simple pin events, the P2 offers a rich event ecosystem:

```pasm2
' Configure multiple event sources
        setse1  ##SE_PIN_RISE | 16      ' Pin 16 rising edge
        setse2  ##SE_TIMER_MATCH        ' CT1 match
        setse3  ##SE_LOCK_AVAIL | 0     ' Lock 0 available
        
' Wait for any event
        waitse1                         ' Sleep until event
        
' Or poll multiple events
.check  pollse1 wc
if_c    jmp     #handle_pin
        pollse2 wc
if_c    jmp     #handle_timer
        pollse3 wc
if_c    jmp     #handle_lock
        jmp     #.check
```

### Event Selection Patterns

| Pattern | Encoding | Description |
|---------|----------|-------------|
| Single Pin | %01_pppppp | Specific pin edge |
| Pin Pattern | %10_pppppp_mmmmmm | Multiple pins match |
| Timer Match | %11_00_tttt | CT timer equals value |
| Timer Pass | %11_01_tttt | CT timer passes value |
| Lock State | %11_10_llll | Lock becomes available |
| ATN Signal | %11_11_cccc | Cog attention signal |

\begin{sidetrack}
\textbf{Why Events Over Interrupts?}

Events are gentler than interrupts. They don't hijack your code—they politely wait until you're ready. This makes debugging easier, timing more predictable, and coordination cleaner. Use interrupts for urgency, events for efficiency.
\end{sidetrack}

## Lock Strategies

### Advanced Lock Patterns

#### Pattern 1: Read-Write Lock
```pasm2
' Multiple readers, exclusive writer
READ_LOCK = 0
WRITE_LOCK = 1
reader_count long 0

' Reader entry
reader_acquire
        locktry #READ_LOCK wc
if_c    jmp     #reader_acquire
        
        rdlong  pa, ##reader_count
        add     pa, #1
        wrlong  pa, ##reader_count
        
        lockrel #READ_LOCK
        ret

' Writer entry
writer_acquire
        locktry #WRITE_LOCK wc
if_c    jmp     #writer_acquire
        
.wait   rdlong  pa, ##reader_count wz
if_nz   jmp     #.wait                  ' Wait for readers
        
        locktry #READ_LOCK wc           ' Block new readers
if_c    jmp     #$-1
        ret
```

#### Pattern 2: Priority Locks
```pasm2
' Higher priority cogs get preference
priority_acquire
        rdlong  my_pri, ##cog_priority
        
.try    locktry #0 wc
if_nc   ret                             ' Got it!
        
' Check if we should yield
        rdlong  pa, ##waiting_priority
        cmp     my_pri, pa wc
if_c    waitx   ##1000                  ' Yield to higher priority
        
        wrlong  my_pri, ##waiting_priority
        jmp     #.try
```

#### Pattern 3: Deadlock Prevention
```pasm2
' Always acquire locks in same order
multi_lock_acquire
        mov     lock_order, ##lock_sequence
        
.next   rdbyte  lock_num, lock_order++ wz
if_z    ret                             ' All acquired
        
.try    locktry lock_num wc
if_c    jmp     #.try
        jmp     #.next
        
lock_sequence
        byte    2, 5, 7, 0              ' Always this order
```

## Cog Attention System

The attention system provides instant cog-to-cog signaling:

```pasm2
' Signal specific cogs
        cogatn  #%0000_0010             ' Signal cog 1
        cogatn  #%1111_1110             ' Signal cogs 1-7
        
' Wait for attention
        waitatn                         ' Sleep until signaled
        
' Poll attention status
        pollatn wc                      ' Check if signaled
if_c    jmp     #handle_attention
```

### Attention Patterns

#### Pattern 1: Work Distribution
```pasm2
' Master distributes work
master  rdlong  work_item, ##queue
        wrlong  work_item, ##work_buffer
        
' Find idle worker
        mov     mask, #%0000_0010       ' Start with cog 1
.find   cogatn  mask                    ' Try to signal
        pollatn wc                      ' Did they respond?
if_c    jmp     #.next_worker
        jmp     #.work_assigned
        
.next_worker
        shl     mask, #1
        jmp     #.find

' Worker waits for work
worker  waitatn                         ' Sleep until work
        rdlong  task, ##work_buffer
        ' Process task...
        cogatn  #%0000_0001             ' Signal completion
```

#### Pattern 2: Barrier Synchronization
```pasm2
' All cogs must reach barrier
barrier mov     pa, cogid
        mov     pb, #1
        shl     pb, pa                  ' Our cog bit
        
' Signal we're at barrier
        lock    #BARRIER_LOCK
        rdlong  pa, ##barrier_mask
        or      pa, pb
        wrlong  pa, ##barrier_mask
        unlock  #BARRIER_LOCK
        
' Wait for all cogs
.wait   rdlong  pa, ##barrier_mask
        cmp     pa, ##$FF wz            ' All 8 cogs?
if_nz   jmp     #.wait
```

\begin{interlude}
\textbf{The Attention Philosophy}

Attention signals are like tapping someone on the shoulder—immediate but not rude. Unlike interrupts that barge in, attention signals wait politely until the cog checks. This makes them perfect for cooperation without disruption.
\end{interlude}

## Complex Event Scenarios

### Scenario 1: Data Pipeline
```pasm2
' Three-stage pipeline with events
' Stage 1: Read sensor
stage1  rdpin   data, #SENSOR
        wrlong  data, ##pipe1_2
        cogatn  #%0000_0100             ' Signal stage 2
        waitse1                         ' Wait for feedback
        jmp     #stage1

' Stage 2: Process data  
stage2  waitatn                         ' Wait for data
        rdlong  data, ##pipe1_2
        ' Process...
        wrlong  result, ##pipe2_3
        cogatn  #%0000_1000             ' Signal stage 3
        cogatn  #%0000_0010             ' Acknowledge stage 1
        jmp     #stage2

' Stage 3: Output result
stage3  waitatn
        rdlong  result, ##pipe2_3
        ' Output...
        cogatn  #%0000_0100             ' Acknowledge stage 2
        jmp     #stage3
```

### Scenario 2: Event-Driven State Machine
```pasm2
' State machine with multiple event triggers
state_machine
        mov     state, #IDLE
        
.loop   cmp     state, #IDLE wz
if_z    call    #state_idle
        cmp     state, #ACTIVE wz
if_z    call    #state_active
        cmp     state, #ERROR wz
if_z    call    #state_error
        jmp     #.loop

state_idle
        setse1  ##SE_PIN_RISE | START_BTN
        waitse1
        mov     state, #ACTIVE
        ret

state_active
        setse1  ##SE_PIN_RISE | STOP_BTN
        setse2  ##SE_TIMER_PASS
        setse3  ##SE_PIN_RISE | ERROR_PIN
        
        pollse1 wc
if_c    mov     state, #IDLE
        pollse2 wc
if_c    call    #timeout_handler
        pollse3 wc
if_c    mov     state, #ERROR
        ret
```

## Performance Monitoring with Events

```pasm2
' Profile code sections using events
profile_start
        getct   start_time
        setse1  ##SE_TIMER_PASS
        addct1  start_time, ##MAX_CYCLES
        
' Code to profile
        call    #function_to_test
        
' Check if we exceeded time
        pollse1 wc
if_c    jmp     #too_slow
        
        getct   end_time
        sub     end_time, start_time
        ' Store timing result
```

\begin{missing}
🚧 \textbf{CONTENT MISSING - COMING SOON}

Need to add:
- SETQ + COGINIT for parameter passing
- Hub lock instructions
- Event filtering and debouncing
- Power management with events
- Multi-cog debugging strategies
\end{missing}

## Your Turn: Synchronization Mastery

\begin{yourturn}
\textbf{Challenge 1: Producer-Consumer Queue}
Implement a thread-safe queue with multiple producers and consumers.

\textbf{Challenge 2: Parallel Sort}
Sort an array using multiple cogs with proper synchronization.

\textbf{Challenge 3: Event Logger}
Create a system that logs events from multiple sources with timestamps.

\textbf{Challenge 4: Resource Pool}
Manage a pool of resources with fair allocation among cogs.

\textbf{Challenge 5: Watchdog System}
Implement a watchdog that monitors all cogs and restarts failed ones.
\end{yourturn}

## Synchronization Gotchas

### Gotcha 1: Lock Leaks
```pasm2
' WRONG - lock never released on error
        locktry #0 wc
if_c    jmp     #$-1
        
        call    #risky_operation ' Might fail!
        
        lockrel #0              ' Never reached on error
        
' RIGHT - always release
        locktry #0 wc
if_c    jmp     #$-1
        
        call    #risky_operation
        
cleanup lockrel #0              ' Always executed
        ret
```

### Gotcha 2: Event Race
```pasm2
' WRONG - event can be missed
        setse1  ##SE_PIN_RISE | 16
        ' Event happens here - missed!
        waitse1
        
' RIGHT - check first
        setse1  ##SE_PIN_RISE | 16
        pollse1 wc              ' Check if already occurred
if_nc   waitse1                 ' Wait only if needed
```

### Gotcha 3: Attention Overflow
```pasm2
' WRONG - multiple attentions lost
        cogatn  #%0000_0010
        cogatn  #%0000_0010     ' Second overwrites first!
        
' RIGHT - wait for acknowledgment
        cogatn  #%0000_0010
.wait   pollatn wc              ' Wait for response
if_nc   jmp     #.wait
```

\begin{review}
🔍 \textbf{NEEDS TECHNICAL REVIEW}

Verify:
- Maximum event response latency
- Lock fairness implementation
- Attention signal queuing behavior
- Event priority handling
\end{review}

## The Philosophy of Synchronization

Perfect synchronization requires understanding these principles:

1. **Minimize critical sections**: Hold locks briefly
2. **Prevent deadlocks**: Consistent lock ordering
3. **Use appropriate tools**: Events for waiting, locks for exclusion
4. **Design for cooperation**: Cogs should help, not fight
5. **Test thoroughly**: Race conditions hide well

\begin{chapterend}
✨ \textbf{You've mastered the art of multi-cog harmony!}

You've learned: Advanced event configuration, sophisticated lock patterns, attention signaling, and complex synchronization scenarios.

Ready for Part IV? We'll apply everything to real applications: video, serial protocols, signal processing, and multi-cog orchestration!
\end{chapterend}# Part IV: Applications

