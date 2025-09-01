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

**Try it!** Create a multiplication table by calculating 1×1 through 12×12. Time how fast the P2 does all 144 calculations. You'll be amazed!

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

**Try it!** Generate a sine wave lookup table with 256 entries. Compare the speed of table lookup vs. real-time CORDIC calculation.

**Your Turn:** Now create a frequency analyzer using the CORDIC engine. Have it detect dominant frequencies in audio signals by calculating phase differences between samples.

## Your Turn: Mathematical Mastery

\begin{yourturn}
\textbf{Challenge 1: Digital Signal Processing}
Create a simple digital filter that uses the hardware multiply to apply coefficients to input samples. Start with a 3-tap FIR filter.
\end{yourturn}

\begin{yourturn}
\textbf{Challenge 2: Graphics Engine}
Use CORDIC rotation to create a simple 3D wireframe cube renderer. Rotate the cube in real-time around all three axes.
\end{yourturn}

\begin{yourturn}
\textbf{Challenge 3: Control System}
Implement a PID controller using fixed-point mathematics. Use it to control the position of a servo motor with feedback.
\end{yourturn}

\begin{chapterend}
✨ \textbf{You've unlocked the P2's mathematical superpowers!}

The hardware multiply, divide, and CORDIC engine transform complex calculations into simple, fast operations. You're no longer limited by software math—you're empowered by silicon speed. In the next chapter, we'll use these mathematical muscles to make intelligent decisions with flags and conditionals.
\end{chapterend}

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

**Try it!** Create a safe calculator that gracefully handles all edge cases: overflow, underflow, and division by zero. Display error messages instead of crashing.

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

**Your Turn:** Build a real-time spectrum analyzer that uses the CORDIC engine to compute a Fast Fourier Transform (FFT) on incoming audio data. Display the frequency spectrum using PWM to control LED brightness.

\begin{chapterend}
✨ \textbf{You're now a P2 math wizard!}

You've mastered: Hardware multiply/divide, the CORDIC engine for trig and more, fixed-point arithmetic, and mathematical patterns.

Next: Chapter 6 shows you how flags and conditions control program flow with elegant efficiency!
\end{chapterend}

---

\begin{chapterend}
✨ \textbf{You've mastered P2 mathematics!}

The hardware multiply, divide, and CORDIC engine give you computational superpowers. Next, we'll use these tools to make smart decisions.
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

**Try it!** Build a sorting algorithm that uses these min/max operations to find the median of 5 sensor readings in real-time. Time how much faster it is than traditional sorting.

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

**Try it!** Create a data filter that processes sensor readings, rejecting outliers and averaging only values within a normal range. Use conditional execution to do it without any jumps.

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

**Your Turn:** Design a smart thermostat that uses conditional execution to make heating/cooling decisions based on temperature, time of day, and occupancy sensors. Make it energy-efficient by avoiding unnecessary operations.

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

**Try it!** Create a mood lighting system using 3 PWM channels for RGB. Make the colors cycle smoothly through the rainbow using sine waves for each channel.

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

**Try it!** Build a simple chat system between two P2s using serial communication. Add echo, line editing, and maybe even emoticons!

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

**Try it!** Create a data logger that samples multiple ADC channels and stores the results with timestamps. Graph the data to see patterns over time.

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

**Try it!** Build a tachometer that measures engine RPM by counting ignition pulses. Display the RPM on a serial terminal with real-time updates.

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

**Your Turn:** Design a complete home automation system using Smart Pins for sensors, actuators, and communication. Use temperature sensors, motion detectors, light controllers, and serial communication—all running independently while your main code handles the logic.

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

**Try it!** Set up a burglar alarm system that uses pin events to detect door/window openings. Make it arm/disarm with a button and sound an alert with PWM on a buzzer pin.

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

**Try it!** Create a real-time system with three priorities: heartbeat LED (low), sensor sampling (medium), and emergency stop (high). Watch how higher priorities preempt lower ones.

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

**Try it!** Build a combination lock using button interrupts with debouncing. Require a specific sequence of button presses within time limits to unlock.

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

**Try it!** Create a security monitoring system that sleeps until any sensor triggers, then logs which sensor activated and the precise time.

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

**Your Turn:** Design a battery-powered weather station that sleeps most of the time, waking only to sample sensors every 10 minutes or when wind speed exceeds a threshold. Use events to minimize power consumption.

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

**Try it!** Build a high-speed data logger that reads sensor data from hub memory and processes it in real-time. Measure how much faster FIFO streaming is compared to individual hub reads.

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

**Try it!** Create a digital picture frame that streams images from hub memory to a parallel LCD display. While one image displays, have your cog prepare the next image in a double buffer.

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

**Try it!** Build a retro-style graphics system that streams 8-bit indexed color pixels through a custom palette. Create animated sprites by changing the LUT contents in real-time.

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

**Try it!** Implement a smooth audio player using double buffering. While one buffer streams to the DAC, fill the other buffer with the next audio chunk. Never miss a sample!

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

**Your Turn:** Design a complete video streaming system that reads compressed video frames from hub memory, decompresses them in real-time, and streams the pixel data to a display—all while your cog handles user input and game logic.

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

**Try it!** Build a dynamic patch system that modifies hub code based on configuration data. Create different behaviors by patching function constants at runtime.

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

**Your Turn:** Create a program that automatically switches between cog and hub execution based on real-time performance monitoring. Optimize critical loops in cog RAM while keeping large data structures in hub.

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

**Your Turn:** Build a complete retro gaming console using P2's video capabilities. Generate tile-based graphics, scrolling backgrounds, animated sprites, and sound effects—all while maintaining 60 FPS gameplay.

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

**Your Turn:** Design a universal protocol translator that converts between UART, SPI, and I2C protocols in real-time. Use Smart Pins for hardware acceleration and buffer management for seamless data flow.

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

**Your Turn:** Create a real-time audio effects processor that applies multiple effects (reverb, delay, EQ) to live audio. Use the CORDIC engine for complex calculations and streaming for zero-latency processing.

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

**Your Turn:** Your final challenge awaits! Design and build a complete embedded system that uses all eight cogs: real-time video generation, multi-channel audio processing, sensor fusion, wireless communication, motor control, user interface, data logging, and system monitoring. This is your masterpiece—a symphony of silicon showcasing everything you've learned. Make it uniquely yours!

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

*Version 1.0 - August 2025*