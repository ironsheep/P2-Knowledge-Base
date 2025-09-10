# Part II: Essential Tools

# Chapter 5: Mathematics Unleashed

Remember when you had to write software multiply routines? Or lookup tables for sine and cosine? The P2 laughs at such primitive ways. With hardware multiply, divide, and the CORDIC engine, math isn't just fast—it's fun!

## The Hook: From Calculator to Supercomputer

The P2 can multiply two 16-bit numbers in 2 clocks. Divide? 2 clocks. Need the sine of an angle? 8-58 clocks depending on precision. Calculate square roots, logarithms, rotate vectors? All in hardware. It's like upgrading from an abacus to a graphing calculator.

## Hardware Multiply: Your New Best Friend

The P2 has a built-in 16×16 signed multiplier with 32-bit result:

```pasm2
' Simple multiplication
        mov     pa, #100
        mov     pb, #200
        mul     pa, pb          ' pa = 100 * 200 = 20,000
        
' Signed multiplication
        mov     pa, ##-1000
        mov     pb, #50
        muls    pa, pb          ' pa = -1000 * 50 = -50,000
```

### Extended Precision: 32×32 Multiplication

Need bigger numbers? The P2 has you covered:

```pasm2
' 32x32 bit multiplication with 64-bit result
        mov     pa, ##1_000_000
        mov     pb, ##2_000_000
        
        qmul    pa, pb          ' Start CORDIC multiply
        getqx   result_lo       ' Get lower 32 bits
        getqy   result_hi       ' Get upper 32 bits
' Result: 2,000,000,000,000 in result_hi:result_lo
```

\begin{sidetrack}
\textbf{The CORDIC Secret}

CORDIC stands for "COordinate Rotation DIgital Computer." It's a clever algorithm that uses only shifts and adds to calculate complex math functions. The P2 has this in hardware, making it incredibly powerful for signal processing, graphics, and control systems.
\end{sidetrack}

## Division: No More Tears

Software division is slow and painful. Hardware division is instant gratification:

```pasm2
' Simple division
        mov     pa, #1000
        mov     pb, #25
        qdiv    pa, pb          ' Start division
        getqx   quotient        ' quotient = 40
        getqy   remainder       ' remainder = 0
        
' Signed division
        mov     pa, ##-1000
        mov     pb, #30
        qdiv    pa, pb
        getqx   quotient        ' quotient = -33
        getqy   remainder       ' remainder = -10
```

### Scaling and Fixed-Point Math

```pasm2
' Fixed-point multiply (16.16 format)
        mov     pa, ##$0001_8000   ' 1.5 in 16.16
        mov     pb, ##$0002_0000   ' 2.0 in 16.16
        
        qmul    pa, pb
        getqx   result_lo
        getqy   result_hi
        
' Extract integer part (shift right 16)
        shr     result_lo, #16
        shl     result_hi, #16
        or      result_lo, result_hi
' Result: 3 (1.5 * 2.0)
```

## The CORDIC Engine: Mathematical Magic

The CORDIC can do trigonometry, logarithms, and more:

### Sine and Cosine
```pasm2
' Calculate sine and cosine of 45 degrees
        mov     angle, ##$2000_0000  ' 45° in P2 angle units
        
        qrotate #1, angle           ' Unit vector, rotate by angle
        getqx   cos_val             ' Cosine result
        getqy   sin_val             ' Sine result
' Results: cos(45°) and sin(45°) in fixed-point
```

### Vector Rotation
```pasm2
' Rotate a 2D point around origin
        mov     x, #100             ' X coordinate
        mov     y, #50              ' Y coordinate
        mov     angle, ##$4000_0000 ' 90 degrees
        
        setq    y                   ' Set Y
        qrotate x, angle            ' Rotate (x,y) by angle
        getqx   new_x               ' new_x = -50
        getqy   new_y               ' new_y = 100
```

### Square Root
```pasm2
' Calculate square root
        mov     value, ##1000000
        
        qsqrt   value, #0           ' Start square root
        getqx   result              ' result = 1000
```

\begin{interlude}
\textbf{Angle Units in P2}

The P2 uses a clever angle system: a full circle is $2^{32}$ units. This means:
- 90° = $1,073,741,824$ ($2^{30}$)
- 180° = $2,147,483,648$ ($2^{31}$)
- 360° = $4,294,967,296$ ($2^{32}$ = 0, wraps around)

Why? Binary angles wrap naturally, just like real angles!
\end{interlude}

## Mathematical Patterns

### Pattern 1: Fast Sine Wave Generation
```pasm2
' Generate sine wave samples
        mov     phase, #0
        mov     delta, ##$0100_0000  ' Frequency
        
genwave add     phase, delta        ' Advance phase
        qrotate #$7FFF, phase       ' Max amplitude, current phase
        getqy   sample              ' Get sine value
        wrlong  sample, ptra++      ' Store sample
        jmp     #genwave
```

### Pattern 2: Polar to Cartesian
```pasm2
' Convert (radius, angle) to (x, y)
        mov     radius, #100
        mov     angle, ##$2000_0000  ' 45 degrees
        
        qrotate radius, angle
        getqx   x                   ' X coordinate
        getqy   y                   ' Y coordinate
```

### Pattern 3: Fast Averaging
```pasm2
' Average of 8 values using multiply
        mov     sum, value1
        add     sum, value2
        add     sum, value3
        add     sum, value4
        add     sum, value5
        add     sum, value6
        add     sum, value7
        add     sum, value8
        
' Divide by 8 (multiply by 1/8)
        qmul    sum, ##$2000_0000   ' × 0.125 in fixed point
        getqy   average             ' Upper 32 bits = result
```

\begin{missing}
🚧 \textbf{CONTENT MISSING - COMING SOON}

Need to add:
- CORDIC pipeline timing details
- Logarithm and exponential functions
- Hyperbolic functions
- Vector magnitude calculation
\end{missing}

## Your Turn: Math Playground

\begin{yourturn}
\textbf{Challenge 1: Circle Drawing}
Use sine/cosine to calculate points around a circle.

\textbf{Challenge 2: Temperature Conversion}
Implement °C to °F using multiply and divide: F = C × 9/5 + 32

\textbf{Challenge 3: Moving Average}
Create a 16-sample moving average filter using hardware math.

\textbf{Challenge 4: Vector Graphics}
Rotate a triangle shape around its center using CORDIC.

\textbf{Challenge 5: Fixed-Point Calculator}
Implement add, subtract, multiply, divide in 16.16 fixed-point.
\end{yourturn}

## Math Gotchas and Tips

### Gotcha 1: CORDIC is Pipelined
```pasm2
' WRONG - result not ready!
        qmul    pa, pb
        getqx   result          ' Too soon!
        
' RIGHT - CORDIC needs time
        qmul    pa, pb
        nop                     ' Wait 2 clocks minimum
        getqx   result          ' Now it's ready
```

### Gotcha 2: Overflow in Multiply
```pasm2
' Multiplying two 16-bit values can overflow 32 bits
        mov     pa, ##50000
        mov     pb, ##50000
        mul     pa, pb          ' Overflow! Result is wrong
        
' Use QMUL for larger results
        qmul    pa, pb
        getqx   result_lo
        getqy   result_hi       ' Full 64-bit result
```

### Gotcha 3: Division by Zero
```pasm2
' Check for divide by zero
        tjz     divisor, #div_error
        qdiv    dividend, divisor
        getqx   result
```

\begin{review}
🔍 \textbf{NEEDS TECHNICAL REVIEW}

Please verify:
- Exact CORDIC operation timings
- Fixed-point format conventions
- Overflow behavior in MUL vs MULS
\end{review}

## The Power of Hardware Math

With hardware math, the P2 can:
- Generate real-time audio effects
- Render 3D graphics
- Control motors with precise PID loops
- Process sensor data with digital filters
- Calculate FFTs for spectrum analysis

All without breaking a sweat!

\begin{chapterend}
✨ \textbf{You're now a P2 math wizard!}

You've mastered: Hardware multiply/divide, the CORDIC engine for trig and more, fixed-point arithmetic, and mathematical patterns.

Next: Chapter 6 shows you how flags and conditions control program flow with elegant efficiency!
\end{chapterend}

---

# Chapter 6: Flags and Decisions

Life is about making decisions. So is programming. The P2's flag system turns decision-making from a chore into an art form. With Z (zero), C (carry), and conditional execution, you'll write code that flows like poetry.

## The Hook: Every Instruction Can Think

Here's what makes P2 special: almost every instruction can be conditional. Not just jumps—ANY instruction. Imagine code that reads like: "Add these numbers if the result was zero. Rotate left if there was a carry. Store the value if both conditions are true." That's P2 assembly!

## Meet the Flags: Z and C

The P2 has two main flags that track your program's state:

```pasm2
' Z Flag (Zero)
        cmp     pa, #10 wz      ' Compare pa with 10, update Z
if_z    jmp     #equal          ' Jump if they're equal (Z=1)
if_nz   jmp     #not_equal      ' Jump if different (Z=0)

' C Flag (Carry/Borrow)
        add     pa, pb wc       ' Add with carry flag update
if_c    jmp     #overflow       ' Jump if carry occurred
if_nc   jmp     #no_overflow    ' Jump if no carry
```

### Flag Effects Table

| Instruction | WZ Effect | WC Effect |
|-------------|-----------|-----------|
| ADD | Z=1 if result is 0 | C=1 if overflow |
| SUB | Z=1 if result is 0 | C=1 if borrow |
| AND | Z=1 if result is 0 | C = parity |
| CMP | Z=1 if D=S | C=1 if D<S (unsigned) |
| TEST | Z=1 if (D AND S)=0 | C = parity |

\begin{sidetrack}
\textbf{Why Only Two Flags?}

Many processors have N (negative), V (overflow), and more. The P2 keeps it simple with just Z and C. Why? Simplicity breeds speed. Two flags can be tested in parallel, updated without penalty, and understood at a glance. When you need more complex tests, combine them!
\end{sidetrack}

## Conditional Execution: The P2's Superpower

Any instruction can be conditional:

```pasm2
' Traditional approach (other CPUs)
        cmp     value, #100 wz
        jz      skip
        mov     result, value
skip    ' Continue...

' P2 approach (elegant!)
        cmp     value, #100 wz
if_nz   mov     result, value   ' Only executes if not equal!
```

### Condition Codes

| Condition | Test | Description |
|-----------|------|-------------|
| if_z | Z=1 | Execute if zero |
| if_nz | Z=0 | Execute if not zero |
| if_c | C=1 | Execute if carry |
| if_nc | C=0 | Execute if no carry |
| if_c_and_z | C=1 AND Z=1 | Both conditions |
| if_c_or_z | C=1 OR Z=1 | Either condition |
| if_c_and_nz | C=1 AND Z=0 | Carry but not zero |
| if_nc_or_z | C=0 OR Z=1 | No carry or zero |

### Advanced Conditions

```pasm2
' Multiple conditions in sequence
        cmp     pa, #10 wc,wz   ' Update both flags
if_z    mov     result, #1      ' Equal to 10
if_c    mov     result, #2      ' Less than 10
if_nc_and_nz mov result, #3    ' Greater than 10

' Conditional chains
        test    flags, #%0001 wz
if_nz   test    flags, #%0010 wz
if_nz   test    flags, #%0100 wz
if_nz   jmp     #all_set        ' All three bits set
```

## Comparison Instructions: The Decision Makers

### CMP: The Universal Comparison
```pasm2
' Basic comparison
        cmp     pa, pb wc,wz
' After this:
' Z=1 if pa equals pb
' C=1 if pa < pb (unsigned)

' Signed comparison trick
        cmps    pa, pb wc,wz    ' Signed compare
' C=1 if pa < pb (signed)
```

### TEST: Bitwise AND Without Storing
```pasm2
' Check if bit 7 is set
        test    value, #$80 wz
if_nz   jmp     #bit7_set

' Check multiple bits
        test    status, #%00001111 wz
if_z    jmp     #no_low_bits_set
```

### TESTN: Bitwise AND with Complement
```pasm2
' Check if bits are clear
        testn   value, #$FF wz  ' Test if low byte is zero
if_z    jmp     #low_byte_clear
```

\begin{interlude}
\textbf{The Elegance of TEST}

TEST is like CMP's cousin—it does AND instead of SUB. Why is this useful? Checking bit patterns! Want to know if certain flags are set? TEST them. Need to validate a mask? TEST it. It's non-destructive reconnaissance for your data.
\end{interlude}

## Control Flow Patterns

### Pattern 1: Range Checking
```pasm2
' Check if value is between 10 and 100
        cmp     value, #10 wc      ' C=1 if value < 10
if_c    jmp     #too_small
        cmp     value, #101 wc     ' C=1 if value < 101
if_nc   jmp     #too_large
        ' Value is in range!
```

### Pattern 2: State Machine
```pasm2
state_machine
        cmp     state, #3 wc,wz
if_z    jmp     #state0
        cmp     state, #1 wz
if_z    jmp     #state1
        cmp     state, #2 wz
if_z    jmp     #state2
        jmp     #state3

state0  ' Handle state 0
        mov     state, #1
        jmp     #state_machine
        
state1  ' Handle state 1
        test    input, #1 wz
if_nz   mov     state, #2
        jmp     #state_machine
```

### Pattern 3: Min/Max Operations
```pasm2
' Find minimum of pa and pb
        cmp     pa, pb wc       ' C=1 if pa < pb
if_nc   mov     pa, pb          ' If pa >= pb, use pb
' pa now contains minimum

' Find maximum
        cmp     pa, pb wc       ' C=1 if pa < pb  
if_c    mov     pa, pb          ' If pa < pb, use pb
' pa now contains maximum
```

## Complex Decision Trees

```pasm2
' Multi-way branch based on value (0-7)
        cmp     value, #8 wc
if_nc   jmp     #error          ' >= 8 is error
        
        altd    value, #jump_table
        jmp     0-0             ' Self-modifying jump!
        
jump_table
        jmp     #handle0
        jmp     #handle1
        jmp     #handle2
        jmp     #handle3
        jmp     #handle4
        jmp     #handle5
        jmp     #handle6
        jmp     #handle7
```

\begin{missing}
🚧 \textbf{CONTENT MISSING - COMING SOON}

Need to add:
- SKIPF instruction for complex conditionals
- Flag preservation across calls
- Conditional returns (RET conditions)
- TJZ/TJNZ/TJS/TJNS instructions
\end{missing}

## Your Turn: Decision Challenges

\begin{yourturn}
\textbf{Challenge 1: Password Checker}
Compare an entered value with a stored password, set different flags for correct/incorrect.

\textbf{Challenge 2: Bubble Sort}
Implement bubble sort using conditional swaps.

\textbf{Challenge 3: Traffic Light}
Create a state machine for a traffic light with pedestrian button.

\textbf{Challenge 4: Range Classifier}
Classify values into ranges: 0-25 (cold), 26-75 (normal), 76-100 (hot).

\textbf{Challenge 5: Conditional Counter}
Count only when input pin is high AND value is less than 100.
\end{yourturn}

## Flag Tricks and Techniques

### Trick 1: Carry as Boolean
```pasm2
' Set C based on condition
        cmp     value, #50 wc   ' C = (value < 50)
        
' Use C as boolean
if_c    or      flags, #1       ' Set bit if condition true
if_nc   andn    flags, #1       ' Clear bit if false
```

### Trick 2: Zero for Equality Chains
```pasm2
' Check if multiple values are equal
        cmp     a, b wz
if_z    cmp     b, c wz
if_z    cmp     c, d wz
if_z    jmp     #all_equal
```

### Trick 3: Conditional Accumulation
```pasm2
' Sum only positive values
loop    rdlong  value, ptra++
        cmps    value, #0 wc,wz ' Check if negative
if_nc_and_nz add total, value  ' Add if positive
        djnz    count, #loop
```

## Common Flag Pitfalls

### Pitfall 1: Forgetting WZ or WC
```pasm2
' WRONG - flags not updated!
        cmp     pa, pb
if_z    jmp     #equal          ' Always skipped!

' RIGHT - update flags
        cmp     pa, pb wz
if_z    jmp     #equal
```

### Pitfall 2: Flag Corruption
```pasm2
' WRONG - ADD changes flags!
        cmp     pa, pb wz
        add     px, py          ' Destroys Z flag!
if_z    jmp     #equal          ' Wrong flag tested

' RIGHT - preserve or retest
        cmp     pa, pb wz
if_z    jmp     #equal
        add     px, py          ' Safe after branch
```

### Pitfall 3: Signed vs Unsigned
```pasm2
' WRONG - CMP is unsigned!
        mov     pa, ##-1
        cmp     pa, #0 wc       ' C=0 (wrong!)
        
' RIGHT - use CMPS for signed
        mov     pa, ##-1
        cmps    pa, #0 wc       ' C=1 (correct!)
```

\begin{review}
🔍 \textbf{NEEDS TECHNICAL REVIEW}

Verify:
- Complete list of condition codes
- Flag behavior for all ALU operations
- SKIPF instruction syntax and usage
\end{review}

## The Philosophy of Conditional Execution

Conditional execution isn't just about saving jumps—it's about expressing intent clearly:

1. **Code reads like English**: "if zero, increment counter"
2. **No pipeline stalls**: Conditions don't break flow
3. **Compact code**: Fewer jumps means smaller programs
4. **Predictable timing**: Conditional or not, same clocks

\begin{chapterend}
✨ \textbf{You're now a master of P2 decision making!}

You've learned: Z and C flags, conditional execution on any instruction, comparison operations, and control flow patterns.

Next: Chapter 7 reveals Smart Pins—64 independent I/O processors at your command!
\end{chapterend}

---

# Chapter 7: Smart Pins Revealed

Every P2 pin is smart. Not just "configurable" smart, but "has its own processor" smart. Imagine having 64 assistants, each capable of generating signals, measuring inputs, or implementing protocols—all without your CPU lifting a finger. Welcome to Smart Pin paradise!

## The Hook: Set It and Forget It

Traditional MCUs: "Toggle that pin 1000 times per second to make PWM."
P2: "Tell the pin to do PWM. Now go do something important while it handles the boring stuff."

Each Smart Pin can be a UART, a PWM generator, a frequency counter, an ADC, a DAC, or one of 60+ other modes. And they all work independently, in parallel, forever.

## Smart Pin Architecture

\begin{diagram}
🎨 \textbf{DIAGRAM NEEDED}

Smart Pin Block Diagram:
- Input from physical pin
- Smart Pin processor
- Mode configuration register
- X and Y parameter registers  
- Z result register
- Output to physical pin
- Connection to cog
\end{diagram}

Each Smart Pin has:
- **Mode Register**: Selects one of 64+ operating modes
- **X Register**: Mode-specific parameter (period, threshold, etc.)
- **Y Register**: Second parameter or accumulator
- **Z Register**: Result or status

## Basic Smart Pin Setup

```pasm2
' Configure pin 16 as PWM
        wrpin   ##P_PWM_TRIANGLE, #16   ' Set mode
        wxpin   ##$00FF_0080, #16       ' Period=255, Duty=128
        dirh    #16                     ' Enable pin
        
' Now it generates PWM forever!
' Change duty cycle anytime:
        wypin   #200, #16               ' New duty cycle
```

### Smart Pin Mode Categories

| Category | Modes | Use Cases |
|----------|-------|-----------|
| PWM/Servo | Triangle, Sawtooth, PWM | Motor control, LEDs |
| Serial | Async TX/RX, Sync | UART, SPI, I2C |
| Measurement | Frequency, Period, Count | Sensors, encoders |
| Analog | DAC, ADC, Comparator | Audio, sensing |
| Timing | Pulse, Transition | Precise delays |
| Special | Repository, Logic | State machines |

\begin{sidetrack}
\textbf{Why 64+ Modes?}

The P2 designers asked: "What do people use pins for?" Then they implemented ALL of it in hardware. PWM? Check. UART? Check. Quadrature decoding? Check. Sigma-delta ADC? Check. They even added modes for things you haven't thought of yet!
\end{sidetrack}

## PWM: The Gateway Drug

PWM is the perfect introduction to Smart Pins:

```pasm2
' 16-bit PWM on pin 16
        mov     pa, ##P_OE | P_PWM_TRIANGLE
        wrpin   pa, #16         ' Set PWM triangle mode
        
        mov     pa, ##10000     ' Period (frequency)
        shl     pa, #16
        or      pa, #5000       ' Duty (50%)
        wxpin   pa, #16         ' Configure parameters
        
        dirh    #16             ' Start PWM
        
' Smooth LED fade
fade    mov     duty, #0
.loop   wypin   duty, #16       ' Update duty cycle
        add     duty, #10
        and     duty, ##$FFFF   ' Wrap at 16 bits
        waitx   ##100_000
        jmp     #.loop
```

## Serial Communication: UART Made Easy

```pasm2
' Configure pin 16 as UART transmit (115200 baud)
        mov     pa, ##P_ASYNC_TX | P_OE
        wrpin   pa, #16
        
' Calculate bit period for 115200 baud
' bit_period = clock_freq / baud_rate
        mov     pa, ##50_000_000 / 115200
        wxpin   pa, #16
        
        dirh    #16             ' Enable transmitter
        
' Send a byte
        mov     pa, #'H'        ' Character to send
        wypin   pa, #16         ' Send it
        waitx   #20             ' Brief delay
        
' Check if ready for next byte
.wait   testp   #16 wc          ' Test if busy
if_c    jmp     #.wait          ' Wait if still sending
```

### Receiving Serial Data

```pasm2
' Configure pin 17 as UART receive
        mov     pa, ##P_ASYNC_RX
        wrpin   pa, #17
        
        mov     pa, ##50_000_000 / 115200
        wxpin   pa, #17
        
        dirh    #17             ' Enable receiver
        
' Check for received data
.check  testp   #17 wc          ' Check if data ready
if_nc   jmp     #.check         ' Keep checking
        
        rdpin   char, #17       ' Read the byte
        ' Process received character...
```

## Analog I/O: DACs and ADCs

### DAC Output
```pasm2
' 16-bit DAC on pin 20
        wrpin   ##P_DAC_990R_3V, #20    ' 990Ω, 3.3V range
        dirh    #20                     ' Enable DAC
        
' Output analog waveform
        mov     phase, #0
.wave   add     phase, ##1000
        qrotate ##$7FFF, phase         ' Generate sine
        getqy   sample
        add     sample, ##$8000         ' Offset to unsigned
        wypin   sample, #20             ' Output to DAC
        waitx   #100
        jmp     #.wave
```

### ADC Input
```pasm2
' Configure pin 21 as ADC
        wrpin   ##P_ADC | P_ADC_1X, #21 ' ADC, 1x gain
        dirh    #21                     ' Enable ADC
        
' Read analog values
.read   rdpin   value, #21              ' Read ADC
        shr     value, #12              ' Scale to 12 bits
        ' Process value...
        waitx   ##10_000                ' Sample rate
        jmp     #.read
```

\begin{interlude}
\textbf{The ADC/DAC Revolution}

Most microcontrollers have a few ADCs and maybe a DAC or two, shared between all pins. The P2? EVERY pin can be an ADC or DAC. Want 64 analog inputs? You got it. Need 64 analog outputs? No problem. It's like having a complete analog lab on a chip.
\end{interlude}

## Measurement Modes: Counting and Timing

### Frequency Counter
```pasm2
' Measure frequency on pin 8
        wrpin   ##P_COUNT_RISES, #8     ' Count rising edges
        wxpin   ##50_000_000, #8        ' Gate time (1 second)
        dirh    #8                      ' Start counting
        
        waitx   ##50_000_000            ' Wait for gate time
        rdpin   frequency, #8           ' Read frequency in Hz
```

### Pulse Width Measurement
```pasm2
' Measure pulse width
        wrpin   ##P_HIGH_TICKS, #9      ' Count high time
        dirh    #9                      ' Enable
        
.measure
        waitpeq #0, #9                  ' Wait for low
        waitpeq #1, #9                  ' Wait for high
        rdpin   pulse_width, #9         ' Read width in clocks
```

## Quadrature Encoder Decoding

```pasm2
' Set pins 10-11 for quadrature input
        wrpin   ##P_QUADRATURE, #10     ' A input
        wrpin   ##P_QUADRATURE, #11     ' B input (paired)
        dirh    #10                     ' Enable decoder
        
' Read position
.track  rdpin   position, #10           ' Current position
        ' Use position value...
        jmp     #.track
```

\begin{missing}
🚧 \textbf{CONTENT MISSING - COMING SOON}

Need to add:
- Complete Smart Pin mode table
- USB and Ethernet modes
- Differential input modes
- Pin synchronization techniques
- Repository mode for pin arrays
\end{missing}

## Smart Pin Patterns

### Pattern 1: PWM Array for LED Matrix
```pasm2
' Configure 8 pins for PWM
        mov     pin, #16
        mov     count, #8
.setup  wrpin   ##P_PWM_TRIANGLE, pin
        wxpin   ##$FF_80, pin           ' Period=255, 50% duty
        dirh    pin
        add     pin, #1
        djnz    count, #.setup
```

### Pattern 2: Multi-Channel ADC
```pasm2
' Scan 4 analog inputs
        mov     pin, #20
.scan   wrpin   ##P_ADC, pin
        dirh    pin
        waitx   #1000                   ' Settling time
        rdpin   0-0, pin                ' Self-mod destination
        movd    $-1, #samples           ' Point to array
        add     $-2, #1                 ' Next array element
        add     pin, #1
        cmp     pin, #24 wz
if_nz   jmp     #.scan
```

### Pattern 3: Software I2C Using Smart Pins
```pasm2
' Open-drain mode for I2C
        wrpin   ##P_HIGH_1K5, #SCL      ' 1.5kΩ pullup
        wrpin   ##P_HIGH_1K5, #SDA
        
' I2C operations use DIRH/DIRL for drive
' and testp for reading
```

## Your Turn: Smart Pin Mastery

\begin{yourturn}
\textbf{Challenge 1: RGB LED Control}
Use three PWM channels to create color mixing on an RGB LED.

\textbf{Challenge 2: Serial Terminal}
Implement a complete serial terminal with TX and RX.

\textbf{Challenge 3: Analog Oscilloscope}
Use ADC to sample a signal and display on serial terminal.

\textbf{Challenge 4: Servo Controller}
Generate standard servo pulses (1-2ms) on 4 pins.

\textbf{Challenge 5: Frequency Generator}
Create precise frequency output using Smart Pin modes.
\end{yourturn}

## Smart Pin Gotchas

### Gotcha 1: Pin Conflicts
```pasm2
' WRONG - two cogs configuring same pin
' Cog 0:
        wrpin   ##P_PWM_TRIANGLE, #16
' Cog 1:
        wrpin   ##P_ASYNC_TX, #16       ' Conflict!
        
' RIGHT - coordinate pin usage
' Use hub memory to track pin assignments
```

### Gotcha 2: Mode Timing
```pasm2
' WRONG - immediate read after config
        wrpin   ##P_ADC, #20
        dirh    #20
        rdpin   value, #20      ' Not ready yet!
        
' RIGHT - allow settling time
        wrpin   ##P_ADC, #20
        dirh    #20
        waitx   #1000           ' Settling time
        rdpin   value, #20
```

### Gotcha 3: Parameter Formats
```pasm2
' WRONG - incorrect parameter packing
        wxpin   #255, #16       ' Just period, no duty!
        
' RIGHT - pack both values
        mov     pa, #255
        shl     pa, #16
        or      pa, #128        ' Period=255, Duty=128
        wxpin   pa, #16
```

\begin{review}
🔍 \textbf{NEEDS TECHNICAL REVIEW}

Need to verify:
- Complete Smart Pin mode constants
- Exact parameter formats for each mode
- ADC/DAC calibration values
- USB mode implementation details
\end{review}

## The Smart Pin Philosophy

Smart Pins embody the P2's design philosophy:

1. **Offload repetitive tasks**: Let hardware handle the boring stuff
2. **Parallel everything**: 64 independent operations
3. **Flexibility over fixed function**: Reconfigure on the fly
4. **Power in simplicity**: Four registers control everything

\begin{chapterend}
✨ \textbf{You've unlocked the power of Smart Pins!}

You've learned: Smart Pin architecture, PWM and serial modes, analog I/O capabilities, measurement functions, and configuration patterns.

Next: Chapter 8 introduces interrupts and events—how to respond instantly to the world around you!
\end{chapterend}

---

# Chapter 8: Interrupts and Events

The real world doesn't wait. Sensors trigger, timers expire, data arrives—and your code needs to respond NOW. The P2's interrupt and event system lets you handle time-critical events without constantly polling. It's like having a personal assistant who taps you on the shoulder only when something important happens.

## The Hook: Sleeping Beauty with Lightning Reflexes

Your cog can sleep, consuming minimal power, then wake instantly when something happens. Or it can be busy with a task but drop everything to handle an urgent event. This is the power of interrupts and events—responsive without being reactive.

## Events: The Gentle Approach

Events are the P2's polite notification system:

```pasm2
' Set up event on pin 16 rising edge
        setse1  #%01_000000_000000_00_11_0000000_00010000
'               |  |       |       |  |  |        |
'               |  |       |       |  |  |        +-- Pin 16
'               |  |       |       |  |  +----------- Event mode
'               |  |       |       |  +-------------- Filter
'               |  |       |       +----------------- Edge detect
'               |  |       +------------------------- Pin group
'               |  +--------------------------------- Event source
'               +------------------------------------ Event type

' Simpler way using constants
        setse1  ##SE1_PIN | 16         ' Pin 16 event

' Wait for event
        waitse1                         ' Sleep until event
        ' Event occurred! Handle it...
```

### Event Sources

| Source | Configuration | Use Case |
|--------|---------------|----------|
| Pin Edge | %01_pppppp | External interrupts |
| Pin Pattern | %10_pppppp | Complex triggers |
| CT Equal | %11_00_xxxx | Timer events |
| CT Passed | %11_01_xxxx | Timeout detection |
| Lock Available | %11_10_llll | Resource ready |
| Hub FIFO | %11_11_xxxx | Data available |

\begin{sidetrack}
\textbf{Events vs Polling}

Polling is like repeatedly asking "Are we there yet?" Events are like taking a nap and being woken when you arrive. Events save power, reduce latency, and let your cog do useful work instead of checking flags constantly.
\end{sidetrack}

## Interrupts: The Demanding Approach

When events aren't urgent enough, use interrupts:

```pasm2
' Set up interrupt handler
        mov     ijmp1, ##interrupt_handler
        
' Configure interrupt on pin 16
        setint1 #%01_000000_000000_00_11_0000000_00010000
        
' Main code continues...
main_loop
        ' Doing normal work...
        add     counter, #1
        jmp     #main_loop
        
' Interrupt handler (executes immediately on trigger)
interrupt_handler
        ' Save state if needed
        push    pa
        
        ' Handle the interrupt
        drvnot  #17             ' Toggle LED
        
        ' Restore state
        pop     pa
        
        reti1                   ' Return from interrupt
```

### Three Interrupt Levels

The P2 has three interrupt priorities:

```pasm2
' Priority 1 (lowest) - normal interrupts
        mov     ijmp1, ##int1_handler
        setint1 ##INT_PIN | 16
        
' Priority 2 (medium) - urgent interrupts  
        mov     ijmp2, ##int2_handler
        setint2 ##INT_PIN | 17
        
' Priority 3 (highest) - critical interrupts
        mov     ijmp3, ##int3_handler
        setint3 ##INT_CT1
```

Higher priority interrupts can interrupt lower priority ones!

## Timer Events: Precise Timing

```pasm2
' Set up 1ms timer interrupt
        getct   pa              ' Current time
        addct1  pa, ##50_000    ' 1ms at 50MHz
        setint1 ##INT_CT1       ' Interrupt on CT1
        
' Timer interrupt handler
timer_int
        addct1  pa, ##50_000    ' Next interrupt in 1ms
        
        ' Do periodic task
        incmod  milliseconds, ##999
        
        reti1
```

\begin{interlude}
\textbf{The Beauty of ADDCT}

ADDCT (Add to CT) is genius. Instead of reading the timer, adding, and writing back (race condition!), ADDCT does it atomically. This means perfect periodic interrupts without drift, even if an interrupt is delayed.
\end{interlude}

## Event and Interrupt Patterns

### Pattern 1: Button Debouncing
```pasm2
' Interrupt on button press with debouncing
button_int
        getct   pa
        sub     pa, last_press
        cmp     pa, ##2_500_000 wc  ' 50ms debounce
if_c    reti1                       ' Too soon, ignore
        
        mov     last_press, pa
        xor     button_state, #1    ' Toggle state
        
        reti1

last_press long 0
button_state long 0
```

### Pattern 2: Data Buffer with Interrupt
```pasm2
' UART receive interrupt
uart_rx_int
        rdpin   char, #RX_PIN       ' Get received byte
        
        wrbyte  char, ptra++        ' Store in buffer
        cmp     ptra, ##buffer_end wz
if_z    mov     ptra, ##buffer_start ' Wrap around
        
        reti1
```

### Pattern 3: Multiple Event Sources
```pasm2
' Wait for any of several events
        setse1  ##SE1_PIN | 16      ' Pin 16
        setse2  ##SE2_PIN | 17      ' Pin 17
        setse3  ##SE3_CT1           ' Timer
        
        pollse1 wc                  ' Check events
if_c    jmp     #handle_pin16
        pollse2 wc
if_c    jmp     #handle_pin17
        pollse3 wc
if_c    jmp     #handle_timer
        
        waitse1                     ' Wait for any event
```

## Critical Sections and Interrupt Safety

```pasm2
' Disable interrupts for critical section
        stalli                      ' Stop all interrupts
        
        ' Critical code here
        rdlong  pa, ##shared
        add     pa, #1
        wrlong  pa, ##shared
        
        allowi                      ' Re-enable interrupts
```

### Interrupt-Safe Communication
```pasm2
' Main code writes to buffer
main    stalli
        mov     buffer, new_value
        mov     buffer_ready, #1
        allowi
        
' Interrupt reads from buffer
interrupt
        tjz     buffer_ready, #.skip
        mov     pa, buffer
        mov     buffer_ready, #0
.skip   reti1
```

\begin{missing}
🚧 \textbf{CONTENT MISSING - COMING SOON}

Need to add:
- SKIP patterns with interrupts
- Interrupt latency specifications
- Nested interrupt handling
- POLLATN/WAITATN for cog events
- Edge vs level triggering details
\end{missing}

## Advanced Event Techniques

### Selective Wake
```pasm2
' Sleep until one of multiple conditions
        setse1  ##SE1_PIN | SENSOR1
        setse2  ##SE2_PIN | SENSOR2
        setse3  ##SE3_PIN | SENSOR3
        
        waitatn                     ' Wait for any attention
        
        pollatn wc
        bitc    flags, #0           ' Record which woke us
```

### Event Filtering
```pasm2
' Filter noisy signals
        setse1  ##SE1_PIN | 16 | SE1_FILTER
        
' Event only triggers after stable signal
```

## Your Turn: Responsive Programming

\begin{yourturn}
\textbf{Challenge 1: Reaction Timer}
Measure response time between LED on and button press using interrupts.

\textbf{Challenge 2: Multi-Sensor Monitor}
Monitor 4 sensors, wake only when any changes state.

\textbf{Challenge 3: Precision Clock}
Create a real-time clock using timer interrupts.

\textbf{Challenge 4: Priority System}
Demonstrate 3-level interrupt priority with different responses.

\textbf{Challenge 5: Power Saving}
Implement sleep mode that wakes on any of 3 different events.
\end{yourturn}

## Interrupt Gotchas

### Gotcha 1: Register Corruption
```pasm2
' WRONG - corrupts main code registers!
interrupt
        mov     pa, #100        ' Destroys pa!
        reti1
        
' RIGHT - save/restore
interrupt
        push    pa
        mov     pa, #100
        pop     pa
        reti1
```

### Gotcha 2: Interrupt During Interrupt
```pasm2
' WRONG - same level can't nest
int1_handler
        ' Long operation...
        reti1   ' Another INT1 could be missed!
        
' RIGHT - quick handler or use levels
int1_handler
        ' Quick operation only
        reti1
```

### Gotcha 3: Missing Events
```pasm2
' WRONG - event lost during processing
        waitse1
        ' Process event...
        ' Another event here is lost!
        
' RIGHT - check for pending events
.loop   waitse1
        ' Process...
        pollse1 wc
if_c    jmp     #.loop          ' Handle pending
```

\begin{review}
🔍 \textbf{NEEDS TECHNICAL REVIEW}

Please verify:
- Exact interrupt latency cycles
- Event configuration bit patterns
- SKIP instruction interaction with interrupts
- Maximum interrupt frequency
\end{review}

## The Philosophy of Responsiveness

The P2's interrupt and event system embodies key principles:

1. **Sleep when possible**: Save power, wake instantly
2. **Prioritize appropriately**: Three levels for different urgencies
3. **Handle quickly**: Keep interrupt handlers short
4. **Coordinate carefully**: Use atomic operations for shared data

\begin{chapterend}
✨ \textbf{You're now responsive without being reactive!}

You've mastered: Event configuration and waiting, three-level interrupts, timer-based events, and interrupt-safe programming.

Ready for Part III? We'll explore advanced topics like streaming, hub execution, and the mighty CORDIC engine!
\end{chapterend}# Part III: Advanced Topics

