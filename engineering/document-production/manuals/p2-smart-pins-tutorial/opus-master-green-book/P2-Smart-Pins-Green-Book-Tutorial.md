```{=latex}
% Banner image at top (full width) with drop shadow for visual balance
\begin{tcolorbox}[
  enhanced,
  boxrule=1.5pt,
  colframe=gray!60,
  colback=white,
  drop shadow southeast,
  shadow={3pt}{-3pt}{1mm}{black!15},
  left=0pt, right=0pt, top=0pt, bottom=0pt,
  width=\textwidth,
  arc=0pt,
  outer arc=0pt
]
\includegraphics[width=\linewidth]{inbox/assets/book-artwork.png}
\end{tcolorbox}

\begin{center}
\vspace{0.6cm}
{\fontsize{36}{42}\selectfont\bfseries P2 Smart Pins \& I/O\par}
\vspace{0.3cm}
{\Large\itshape Master Every Aspect of P2 Input/Output Through Progressive Learning\par}
\vspace{0.6cm}
{\large December 2025\par}
\vspace{0.2cm}
{\large\color{blue}Version 1.0 - Technical Review\par}

\vfill
\begin{tcolorbox}[
  colback=gray!5,
  colframe=gray!40,
  boxrule=1pt,
  width=0.85\textwidth,
  center,
  title={\bfseries\color{black} Tutorial Guide},
  colbacktitle=gray!15,
  coltitle=black
]
\textbf{Learn by doing with color-coded examples!}

\vspace{0.3cm}
\begin{minipage}[t]{0.45\textwidth}
\textbf{Code Block Colors:}
\begin{itemize}
\item \textcolor{green!50!black}{\textbf{Green}} -- Spin2 examples
\item \textcolor{orange!70!black}{\textbf{Yellow}} -- PASM2 assembly
\item \textcolor{red!60!black}{\textbf{Red}} -- Antipatterns (avoid!)
\end{itemize}
\end{minipage}%
\hfill%
\begin{minipage}[t]{0.50\textwidth}
\textbf{Special Sections:}
\begin{itemize}
\item \textcolor{blue!60!black}{\textbf{Tips}} -- helpful hints
\item \textcolor{gray!70!black}{\textbf{Diagrams}} -- timing \& signal flow
\end{itemize}
\end{minipage}
\end{tcolorbox}
\vspace{1cm}
\end{center}

\clearpage
\pagestyle{fancy}

\tableofcontents

\clearpage
```

# Copyright and License

Copyright © 2025 Iron Sheep Productions, LLC and Parallax Inc.

This work is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0).

You are free to:

- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:

- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made
- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license

To view the full license, visit: https://creativecommons.org/licenses/by-sa/4.0/

### Trademarks

Parallax, Propeller, Spin, and the Parallax logo are trademarks of Parallax Inc.

## Acknowledgments

This tutorial would not exist without the contributions of many individuals:

**Jon Titus** for the original Smart Pins documentation and tutorial approach that forms the pedagogical foundation of this work.

**Evan Hillis** for the original ASCII art Smart Pin block diagram that helped the community understand Smart Pin architecture.

**Raymond Allen** for the color Smart Pin block diagram based on Evan's work.

**The P2 Community** for extensive testing, feedback, and real-world usage that has refined our understanding of Smart Pins.


## Preface: Your Complete Journey into P2 I/O

Welcome, my friend! You're about to discover the complete input/output capabilities of the Propeller 2. We'll start with the basics - simple pin control - and build up to one of the P2's most powerful features: Smart Pins.

### What Makes This Tutorial Special?

This isn't just a Smart Pins reference. This is your complete guided journey from "How do I control a pin?" through "What's a Smart Pin?" all the way to "I can't believe what I just built!" We'll start simple, build confidence, and before you know it, you'll be orchestrating all 64 I/O pins like a maestro conducting a symphony.

### Who Is This For?

Are you new to the P2? Perfect! We'll start with the absolute basics.
Are you a P1 veteran? Excellent! You'll appreciate the familiar instructions before diving into Smart Pins.
Are you somewhere in between? You're exactly where you need to be.

The only requirement is curiosity and a willingness to experiment. P2 I/O is best learned by doing, and we'll be doing plenty!

### How to Use This Tutorial

**The Learning Path** (recommended for first-timers):
Start with Chapter 0 to understand basic I/O, then read Part I to understand Smart Pins conceptually, then work through Part II mode by mode. Each section builds on concepts from previous ones. By Part III, you'll be combining techniques in ways that would make other microcontrollers jealous.

**The Project Path** (when you have something specific in mind):
If you just need basic I/O, Chapter 0 has you covered. For Smart Pins, jump to the mode you need in Part II, but don't skip the introduction - it contains crucial concepts. Each mode chapter stands alone but references related modes.

**The Reference Path** (when you know what you're doing):
Chapter 0 has quick reference tables for basic I/O. Part II has quick reference boxes at the start of each Smart Pin mode. The appendices contain every constant, every formula, every detail you might need.

### A Personal Note from Your Guide

I've been working with microcontrollers for decades, and I can honestly say that the P2's I/O system represents something special. Starting with familiar, simple pin control and building up to Smart Pins that can handle complex protocols independently - that's a beautiful progression.

You'll make mistakes. Your first pin might not toggle. Your first Smart Pin might not work. Your timing might be off. That's normal! Every example in this tutorial has been tested, retested, and tested again. When something doesn't work, we'll show you why and how to fix it.

Ready? Let's start with the basics and build up to the amazing!

# Part I: Understanding P2 I/O - From Basic to Smart

## Chapter 0: P2 I/O Fundamentals - Before Smart Pins

### Why Start Here?

Before we dive into the sophisticated world of Smart Pins, let's establish a solid foundation with basic P2 I/O. If you're coming from other microcontrollers (or even the P1), you'll find familiar concepts here. More importantly, understanding what basic I/O can and can't do will help you appreciate why Smart Pins are revolutionary.

### 0.1 The Four Essential Instructions

Forget what you might have seen about 32+ pin instructions. You really only need four to get started:

::: spin2
```
PUB the_essentials()
  pinfloat(56)          ' Make P56 an input (float it)
  pinhigh(56)           ' Make P56 an output high
  pinlow(56)            ' Set P56 output to 0
  pinhigh(56)           ' Set P56 output to 1
```
:::

That's it! With just these four instructions, you can:

- Control LEDs
- Read buttons
- Create simple signals
- Interface with basic digital devices

Let's see them in action with the classic "Hello World" of embedded systems:

::: spin2
```
CON
  _clkfreq = 200_000_000        ' 200MHz system clock
  LED = 56                      ' P2 Eval board LED

PUB blink_basic()
  pinhigh(LED)                  ' Make LED pin an output high
  repeat
    pinhigh(LED)                ' LED on
    waitms(500)                 ' Wait 500ms
    pinlow(LED)                 ' LED off
    waitms(500)                 ' Wait 500ms
```
:::

::: sidetrack
### The Clock Preamble

Notice the `CON` section at the top of that example? Every Spin2 program needs to configure its system clock:

::: spin2
```
CON
  _clkfreq = 200_000_000  ' 200 MHz system clock
```
:::

This tells the P2 to run at 200 MHz using your board's crystal oscillator. Without it, the chip runs at a sluggish ~20 MHz on its internal RC oscillator---and timing-dependent code (including serial communication and `waitms()` delays) won't behave as expected.

**From here on, we'll omit this preamble from most examples to keep them focused on the Smart Pin concepts being taught.** When you create your own programs, always include `_clkfreq` in your `CON` section. The examples that do timing calculations (like baud rate divisors) will show it explicitly since the math depends on knowing the clock frequency.
:::

Simple, right? Now let's read a button:

::: spin2
```
CON
  BUTTON = 32                   ' Button on P32

PUB read_button() : pressed
  pinfloat(BUTTON)              ' Make button pin an input
  pressed := pinread(BUTTON)   ' Read the pin state
  ' Returns 1 if pressed (assuming active-high button)
```
:::

### 0.2 Reading Inputs - The INA and INB Registers

The P2 has 64 I/O pins, split across two 32-bit registers:

- **INA[31..0]** - Read pins P0 through P31
- **INB[31..0]** - Read pins P32 through P63

::: spin2
```
PUB read_multiple_inputs() | value, button1, button2, sensor, i
  ' Make P0-P7 inputs
  repeat i from 0 to 7
    pinfloat(i)                 ' Set P0..P7 as inputs

  ' Read all 8 pins at once
  value := INA & $FF            ' Get 8-bit value from P0-P7

  ' Or read individually
  button1 := pinread(0)         ' Read P0
  button2 := pinread(1)         ' Read P1
  sensor  := pinread(2)         ' Read P2
```
:::

**Important:** Input pins read the actual pin state, regardless of the output register setting. This means you can read back what you're outputting (useful for debugging).

### 0.3 Understanding Pin Timing (Simplified)

When you control pins, there's a tiny delay between your instruction and the pin actually changing:

```{=latex}
\DRVHTimingDiagram
```

**What this means in practice**: At 200MHz, the 3-clock delay is only 15 nanoseconds - essentially instant for LEDs, buttons, and most I/O!

Similarly, when reading pins:

```{=latex}
\TESTBINATimingDiagram
```

And for quick pin testing (TESTP instruction):

```{=latex}
\TESTPTimingDiagram
```

**The bottom line**: For most projects, you can completely ignore these delays! They only matter when:

- Bit-banging high-speed protocols (>10MHz)
- Synchronizing with external hardware
- Creating precise timing patterns

> **Note:** Need exact timing? See Appendix C (Timing Formulas) for clock-by-clock calculations essential for high-speed protocols.

### 0.4 The Pattern Behind Pin Instructions

Now that you've mastered the essential four, let's understand the full pattern. The P2 actually provides four operations, each with eight variants:

**The Four Operations:**

1. **DIR** - Control pin direction (input/output)
2. **OUT** - Control output state (0/1)
3. **FLT** - Float pins (make input while preserving output register)
4. **DRV** - Drive pins (make output and set level simultaneously)

**The Eight Variants (for each operation):**

- **L** - Low (0) - *You'll use this constantly*
- **H** - High (1) - *You'll use this constantly*
- **C** - Copy from Carry flag
- **NC** - NOT Carry (inverse of Carry flag)
- **Z** - Copy from Zero flag
- **NZ** - NOT Zero (inverse of Zero flag)
- **RND** - Random value (useful for testing)
- **NOT** - Invert current state - *Occasionally useful*

This gives us $4 \times 8 = 32$ instructions, but remember: **You'll use the L and H variants 95% of the time!**

Here's a practical example using the NOT variant:

::: spin2
```
PUB toggle_led()
  pinhigh(56)                   ' Make P56 an output high
  repeat
    pintoggle(56)               ' Toggle the LED state
    waitms(500)                 ' Wait 500ms
    ' No need to track on/off state - toggle does it for us!
```
:::

### 0.5 Practical I/O Patterns

Let's look at some common patterns you'll use in real projects:

#### Button Debouncing

::: spin2
```
PUB debounced_button() : pressed | sample1, sample2
  pinfloat(32)                  ' Button on P32 as input
  sample1 := pinread(32)        ' First reading
  waitms(20)                    ' Debounce delay
  sample2 := pinread(32)        ' Second reading
  pressed := sample1 & sample2  ' Both must be pressed
```
:::

#### Parallel Output (8-bit LCD, etc.)

::: spin2
```
PUB output_byte(value) | i
  repeat i from 0 to 7
    pinhigh(i)                  ' P0..P7 as outputs
  OUTA := (OUTA & !$FF) | value ' Write all 8 bits at once
```
:::

#### Simple Bit-Banged Serial (Slow but Educational)

::: spin2
```
PUB send_byte_slow(value) | bit, TX_PIN
  TX_PIN := 62                  ' Define TX pin
  pinhigh(TX_PIN)               ' TX pin as output high
  repeat bit from 0 to 7
    if value & (1 << bit)
      pinhigh(TX_PIN)           ' Send 1
    else
      pinlow(TX_PIN)            ' Send 0
    waitus(104)                 ' ~9600 baud (104us per bit)
```
:::

### 0.6 Multiple Pin Control

The P2 can control multiple pins simultaneously using the ADDPINS operator:

::: spin2
```
PUB control_multiple() | i
  ' Control 8 LEDs on P16..P23
  repeat i from 16 to 23
    pinhigh(i)                  ' Make 8 pins outputs high (all on)
  waitms(1000)
  repeat i from 16 to 23
    pinlow(i)                   ' Turn all 8 off

  ' Create a pattern
  OUTA := (OUTA & !$FF0000) | (%10101010 << 16)  ' Alternating P16-P23
```
:::

### 0.7 When Basic I/O Isn't Enough

Basic I/O is perfect for:

- Simple LED control
- Reading buttons and switches
- Slow communication protocols
- Learning and experimentation

But watch what happens when we need precise timing:

::: spin2
```
PUB square_wave_painful()
  ' Try to generate a 1kHz square wave - THE HARD WAY
  pinhigh(56)                   ' Make pin 56 output
  repeat
    pinhigh(56)                 ' Pin high
    waitus(500)                 ' 500us high
    pinlow(56)                  ' Pin low
    waitus(500)                 ' 500us low
    ' Problem: Our cog is 100% busy just toggling one pin!
```
:::

What if you need:

- 10 different square waves at different frequencies?
- PWM for motor control while doing other tasks?
- Precise pulse measurement while running your main program?
- Serial communication without dedicating a cog?

This is where Smart Pins revolutionize everything. Instead of your code toggling pins, you configure dedicated hardware to do it perfectly, forever, without using any processor time.

### 0.8 Transitioning to Smart Pins

Let's see the same 1kHz square wave using a Smart Pin:

::: spin2
```
PUB square_wave_smart()
  ' Configure Smart Pin for square wave - THE SMART WAY
  ' P_TRANSITION toggles output each period; need 2 toggles per cycle
  pinstart(56, P_TRANSITION | P_OE, clkfreq/2000, 0)

  ' That's it! Pin 56 now outputs 1kHz forever
  ' Our cog is completely free to do other things
  repeat
    ' Do whatever you want here - the square wave continues!
```
:::

The difference is profound:

- **Basic I/O**: Your code does the work
- **Smart Pins**: Hardware does the work

Ready to make your pins smart? Let's dive into Chapter 1!

### 0.9 Quick Reference - Basic I/O Instructions

For your convenience, here's the complete basic I/O instruction set in both languages:

| Operation | Spin2 Method | PASM2 Instruction | Common Use |
|-----------|--------------|-------------------|------------|
| Set pin as input | `pinfloat(pin)` | **DIRL** #pin | Reading sensors |
| Set pin as output high | `pinhigh(pin)` | **DIRH** #pin + **OUTH** #pin | Turn on LED |
| Set pin as output low | `pinlow(pin)` | **DIRH** #pin + **OUTL** #pin | Turn off LED |
| Output low (0) | `pinlow(pin)` | **OUTL** #pin | Clear output |
| Output high (1) | `pinhigh(pin)` | **OUTH** #pin | Set output |
| Toggle output | `pintoggle(pin)` | **OUTNOT** #pin | Blink without state |
| Drive low | `pinlow(pin)` | **DRVL** #pin | Output + low combined |
| Drive high | `pinhigh(pin)` | **DRVH** #pin | Output + high combined |
| Float low | `pinfloat(pin)` | **FLTL** #pin | Tri-state with out=0 |
| Float high | `pinfloat(pin)` | **FLTH** #pin | Tri-state with out=1 |
| Read pin state | `pinread(pin)` | **INA[pin]** or **INB[pin]** | Read sensor/button |

**Reading Multiple Pins:**

- **Spin2**: `value := INA & $FF` (read P0-P7), individual: `pinread(pin)`
- **PASM2**: `MOV value, INA` then mask, or use `TESTB INA, #pin`

**Controlling Multiple Pins:**

- **Spin2**: Use loops with pin methods, or direct register access `OUTA := value`
- **PASM2**: Use `ADDPINS n` suffix to control consecutive pins

> **Tip:** This table covers 90% of your basic I/O needs. The other variants (C, NC, Z, NZ, RND) are in Appendix F for when you need them.

## Chapter 1: The Smart Pin Revolution

### What Problem Do Smart Pins Solve?

Picture this: You're writing code for a robot. You need to:

- Generate PWM for four motors
- Read two quadrature encoders
- Communicate with sensors via I2C
- Send debug data via serial
- Measure battery voltage with ADC

In a traditional microcontroller, each of these tasks would eat into your processor time. Generating clean PWM at 20kHz? That's an interrupt every 50 microseconds. Reading encoders? More interrupts. Pretty soon, your processor is spending all its time servicing I/O instead of running your robot's logic.

Enter Smart Pins.

### The Smart Pin Concept

Imagine if each I/O pin had its own tiny processor - not a full CPU, but dedicated hardware that could handle one specific task perfectly. That's exactly what Smart Pins are. Each of the P2's 64 I/O pins has a Smart Pin unit that can be configured to perform one of 32 different functions, from simple digital I/O to complex protocols.

![Smart Pin Block Diagram](assets/smart-pins-master-trimmed.png)

Once configured, a Smart Pin runs completely independently. Set up a PWM? It generates perfect pulses forever. Configure a UART? It transmits and receives without bothering your code. Need to count encoder pulses? The Smart Pin counts them in hardware while your code does other things.

### Your First Smart Pin

Let's start with something simple but satisfying - making an LED blink without using any processor time.

::: spin2
```
CON
  _clkfreq = 200_000_000        ' System clock: 200MHz
  LED = 56                      ' P2 Eval board LED

PUB main()
  ' Configure Smart Pin for square wave output
  pinstart(LED, P_TRANSITION | P_OE, clkfreq/2, 0)

  ' The LED now blinks at 1Hz forever!
  ' Our code is free to do other things
  repeat
    ' The processor is completely free here
    ' The LED keeps blinking no matter what we do
```
:::

What just happened? Let's break it down:

1. **`P_TRANSITION`** tells the Smart Pin to toggle its output
2. **`P_OE`** enables the output driver (OE = Output Enable)
3. **`clkfreq/2`** sets the transition period (1Hz = 0.5s high + 0.5s low)
4. **`pinstart()`** configures and activates the Smart Pin

The magic? Once that `pinstart()` executes, the LED blinks forever without any further code. No loops, no delays, no interrupts. The Smart Pin handles everything.

### Understanding Smart Pin Architecture

Each Smart Pin contains sophisticated hardware that operates independently once configured. The architecture includes mode control logic, three 32-bit registers (X, Y, Z), input selection circuitry, and output drivers.

Each Smart Pin contains:

**Three 32-bit Registers:**

- **X Register**: Usually holds timing/period information
- **Y Register**: Usually holds value/duty cycle information
- **Z Register**: Holds results (what you read back)

**Mode Logic:**
The 6-bit mode field (%000000 to %111111) selects what the Smart Pin does. We'll explore all 32 modes, but they fall into categories:

- Digital I/O modes (repository, logic)
- Analog modes (DAC, ADC)
- Timing modes (PWM, NCO, pulse)
- Measurement modes (count, time, frequency)
- Communication modes (serial, USB)

**Input Selector:**
This is where it gets interesting - a Smart Pin can monitor ANY other pin, not just itself! Want Pin 20 to count pulses from Pin 5? No problem. Want Pin 30 to measure the frequency on Pin 10? Easy.

### The Configuration Dance

Every Smart Pin follows the same configuration sequence:

::: spin2
```
' The Universal Smart Pin Setup Sequence
pinclear(pin)                  ' 1. Reset to known state
wrpin(pin, mode)               ' 2. Set the mode
wxpin(pin, x_value)            ' 3. Configure X parameter
wypin(pin, y_value)            ' 4. Configure Y parameter
pinstart(pin, mode, x, y)      ' Or do 1-4 in one call!
```
:::

The beauty is in the consistency. Whether you're setting up a DAC, configuring a UART, or measuring pulses, it's always the same dance: mode, X, Y, enable.

### Making Mistakes (and Learning From Them)

Let's deliberately make some mistakes so you'll recognize them later:

**Mistake 1: Forgetting Output Enable**

::: antipattern
```
' This won't work - no output!
pinstart(LED, P_TRANSITION, clkfreq/2, 0)      ' Missing P_OE
```
:::

::: spin2
```
' This works - output enabled
pinstart(LED, P_TRANSITION | P_OE, clkfreq/2, 0)  ' P_OE included
```
:::

Why does this matter? Smart Pins can generate internal signals without driving the physical pin. Sometimes that's useful, but usually you want to see the output!

**Mistake 2: Wrong Timing Calculation**

::: antipattern
```
' This blinks at 0.5Hz, not 1Hz!
pinstart(LED, P_TRANSITION | P_OE, clkfreq, 0)    ' Period too long
```
:::

::: spin2
```
' This blinks at 1Hz correctly
pinstart(LED, P_TRANSITION | P_OE, clkfreq/2, 0)  ' Correct period
```
:::

Remember: Period is the time between transitions, not the full cycle time!

**Mistake 3: Not Clearing Before Reconfiguring**

::: spin2
```
' First configuration
pinstart(pin, P_PWM_SAWTOOTH | P_OE, 1000, 500)  ' 50% duty PWM

```
:::

::: antipattern
```
' Trying to change modes - might not work!
pinstart(pin, P_TRANSITION | P_OE, clkfreq/2, 0)  ' Old config!
```
:::

::: spin2
```
' Correct way - clear first
pinclear(pin)
pinstart(pin, P_TRANSITION | P_OE, clkfreq/2, 0)  ' Clean configuration
```
:::

### Exercises to Build Confidence

Before we dive into all 32 modes, let's build confidence with some exercises:

**Exercise 1: Multiple Frequencies**
Configure three LEDs to blink at different rates:

- LED1: 1Hz
- LED2: 2Hz
- LED3: 5Hz

All three should run simultaneously without any processor involvement.

**Exercise 2: Phase Offset**
Make two LEDs blink at the same frequency but opposite phases (when one is on, the other is off).

**Exercise 3: Reading Smart Pin Status**
Use `rdpin()` to read how many transitions have occurred. Display the count.

### Key Takeaways

Before we move on, let's cement the key concepts:

1. **Smart Pins are Independent**: Once configured, they run without processor involvement
2. **32 Modes Available**: Each pin can be any of 32 different functions
3. **Three Registers**: X (timing), Y (value), Z (result)
4. **Consistent Interface**: Same configuration pattern for all modes
5. **Any Pin Can Do Anything**: No dedicated pins for specific functions

Ready to explore all 32 modes? Let's go!

## Chapter 2: The Smart Pin Configuration Protocol

### The Five Sacred Steps

Every Smart Pin configuration follows the same five steps. Master these, and you've mastered Smart Pins:

1. **Clear** - Reset to known state
2. **Configure** - Set the mode
3. **X Parameter** - Usually timing
4. **Y Parameter** - Usually value
5. **Enable** - Turn it on

Let's see this in both Spin2 and PASM2:

**Spin2 Approach:**

::: spin2
```
PUB configure_smart_pin(pin, mode, x_val, y_val)
  pinclear(pin)                 ' Step 1: Clear
  wrpin(pin, mode)             ' Step 2: Mode
  wxpin(pin, x_val)            ' Step 3: X parameter
  wypin(pin, y_val)            ' Step 4: Y parameter
  dirh(pin)                    ' Step 5: Enable
```
:::

**PASM2 Approach:**

::: pasm2
```
configure_smart_pin
        dirl    #pin            ' Step 1: Clear
        wrpin   mode, #pin      ' Step 2: Mode
        wxpin   x_val, #pin     ' Step 3: X parameter
        wypin   y_val, #pin     ' Step 4: Y parameter
        dirh    #pin            ' Step 5: Enable
```
:::

### Understanding the Mode Register (WRPIN D Parameter)

The mode register (written with WRPIN) is 32 bits of configuration magic. The register layout controls both the Smart Pin mode and the pin's electrical characteristics.

```{=latex}
\WRPINFormatDiagram
```

But here's the beautiful part - Spin2 provides constants for everything:

::: spin2
```
' Instead of remembering bit patterns...
wrpin(pin, %00_0_000000_000000_00_00_00100)  ' What does this do?!

' Use meaningful constants!
wrpin(pin, P_DAC_DITHER_RND | P_DAC_124R_3V | P_OE)  ' DAC+dither+out
```
:::

### The X Register: Master of Time

In most modes, X controls timing:

**For Output Modes:**

- NCO frequency: X = frequency value
- PWM period: X = period in clocks
- Pulse length: X = pulse width

**For Measurement Modes:**

- Count window: X = measurement period
- Timeout: X = maximum wait time
- Sample period: X = sampling interval

**For Serial Modes:**

- Baud rate: X = clock divider
- Bit period: X = clocks per bit

Let's see a pattern emerge:

::: spin2
```
' NCO frequency output
wxpin(pin, $8000_0000)         ' 1/2 maximum frequency

' PWM period
wxpin(pin, 10_000)             ' 10,000 clock period

' UART baud rate (115200 at 200MHz)
wxpin(pin, (clkfreq / 115200) << 16 | 7)  ' Baud generator
```
:::

### The Y Register: Bearer of Values

Y typically holds the value or data:

**For Output Modes:**

- DAC: Y = output value (0..$FFFF)
- PWM: Y = duty cycle
- Digital: Y = output state

**For Communication:**

- TX: Y = byte to transmit
- Pin groups: Y = pin mask

**For Measurement:**

- Often unused or holds configuration

Example uses:

::: spin2
```
' DAC output at 1.65V (assuming 3.3V range)
wypin(pin, $8000)              ' Mid-scale output

' PWM at 25% duty
wypin(pin, 2500)               ' If period is 10,000

' UART transmit 'A'
wypin(pin, "A")                ' Send character
```
:::

### The Z Register: Keeper of Results

Z is read-only and holds results:

::: spin2
```
' Read encoder count
count := rdpin(encoder_pin)

' Read ADC value
voltage := rdpin(adc_pin)

' Read received UART byte
char := rdpin(serial_pin)
```
:::

But there's a crucial distinction:

**RDPIN vs RQPIN:**

- `rdpin()` - Reads AND acknowledges (clears IN flag)
- `rqpin()` - Reads WITHOUT acknowledging (preserves IN flag)

When do you use which?

::: spin2
```
' Use RDPIN when you're consuming the data
char := rdpin(serial_pin)      ' Read and clear flag

' Use RQPIN when you're just checking
if rqpin(serial_pin) & $100    ' Check if byte available
  char := rdpin(serial_pin)    ' Now read and clear
```
:::

### A/B Input Routing - The Key to Smart Pin Flexibility

Here's where Smart Pins get really powerful - each Smart Pin has TWO independent input selectors (A and B) that can monitor any nearby pin!

**The D Parameter Bit Fields**

```{=latex}
\WRPINFormatDiagram
```

**Why A/B Routing Matters**

Many Smart Pin modes use both A and B inputs:

- **A-input**: Typically the primary data signal
- **B-input**: Typically a clock, gate, or secondary signal

For example, in synchronous serial modes:

- A-input = the data line (MOSI/MISO)
- B-input = the clock line (CLK)

**A-Input Routing Constants**

| Constant | Value | Binary | Description |
|----------|-------|--------|-------------|
| P_TRUE_A | $00000000 | 0000 | This pin's input, true polarity |
| P_INVERT_A | $80000000 | 1000 | This pin's input, inverted |
| P_LOCAL_A | $00000000 | 0000 | Same as P_TRUE_A (local input) |
| P_PLUS1_A | $10000000 | 0001 | Pin+1 input, true |
| P_PLUS2_A | $20000000 | 0010 | Pin+2 input, true |
| P_PLUS3_A | $30000000 | 0011 | Pin+3 input, true |
| P_OUTBIT_A | $40000000 | 0100 | This pin's OUT bit |
| P_MINUS3_A | $50000000 | 0101 | Pin-3 input, true |
| P_MINUS2_A | $60000000 | 0110 | Pin-2 input, true |
| P_MINUS1_A | $70000000 | 0111 | Pin-1 input, true |

**B-Input Routing Constants**

| Constant | Value | Binary | Description |
|----------|-------|--------|-------------|
| P_TRUE_B | $00000000 | 0000 | This pin's input, true polarity |
| P_INVERT_B | $08000000 | 1000 | This pin's input, inverted |
| P_LOCAL_B | $00000000 | 0000 | Same as P_TRUE_B (local input) |
| P_PLUS1_B | $01000000 | 0001 | Pin+1 input, true |
| P_PLUS2_B | $02000000 | 0010 | Pin+2 input, true |
| P_PLUS3_B | $03000000 | 0011 | Pin+3 input, true |
| P_OUTBIT_B | $04000000 | 0100 | This pin's OUT bit |
| P_MINUS3_B | $05000000 | 0101 | Pin-3 input, true |
| P_MINUS2_B | $06000000 | 0110 | Pin-2 input, true |
| P_MINUS1_B | $07000000 | 0111 | Pin-1 input, true |

**Practical Example: SPI with Clock on Adjacent Pin**

For SPI communication with pins arranged as:

- Pin 10: MOSI (data out)
- Pin 11: CLK (clock)
- Pin 12: MISO (data in)

::: spin2
```
CON
  SPI_MOSI = 10
  SPI_CLK  = 11
  SPI_MISO = 12

PUB spi_setup()
  ' MOSI (pin 10): Sync TX mode, clock from pin+1 (pin 11)
  pinstart(SPI_MOSI, P_SYNC_TX | P_OE | P_PLUS1_B, 8, 0)
  '                                      ^^^^^^^^
  '                                      B-input = pin 11 (clock)

  ' CLK (pin 11): Generate clock using transition mode
  pinstart(SPI_CLK, P_TRANSITION | P_OE, 100, 0)

  ' MISO (pin 12): Sync RX mode, clock from pin-1 (pin 11)
  pinstart(SPI_MISO, P_SYNC_RX | P_MINUS1_B, 8, 0)
  '                              ^^^^^^^^^
  '                              B-input = pin 11 (clock)
```
:::

**Example: Counting Pulses from Another Pin**

::: spin2
```
' Count pulses on Pin 5 using Smart Pin 8
' Pin 8's A-input comes from pin-3 (which is pin 5)
pinstart(8, P_COUNT_RISES | P_MINUS3_A, 0, 0)
'                           ^^^^^^^^^
'                           A-input = pin 5

' Read the count
count := rdpin(8)
```
:::

**Example: Gated Counter (Count A when B is High)**

::: spin2
```
' Count pulses on pin 10 only when pin 11 is high
' Configure pin 10: count A-rises when B is high
pinstart(10, P_REG_UP | P_PLUS1_B, 0, 0)
'                       ^^^^^^^^
'                       B-input (gate) from pin 11
```
:::

**PASM2 A/B Routing:**

::: pasm2
```
' Configure sync serial TX on pin 20 with clock from pin 21
        dirl    #20
        wrpin   ##P_SYNC_TX | P_OE | P_PLUS1_B, #20
        '                            ^^^^^^^^^
        '                            B = clock from pin 21
        wxpin   #8, #20              ' 8 bits
        dirh    #20

' Configure sync serial RX on pin 22 with clock from pin 21
        dirl    #22
        wrpin   ##P_SYNC_RX | P_MINUS1_B, #22
        '                     ^^^^^^^^^
        '                     B = clock from pin 21
        wxpin   #8, #22              ' 8 bits
        dirh    #22
```
:::

::: tip
**Common Patterns:**

- For SPI: Data pins use P_PLUS1_B or P_MINUS1_B to reference the adjacent clock pin
- For gated counting: Use B-input to select the gate signal
- For quadrature encoders: A and B inputs are automatically configured by the mode
- For inverted signals: Combine with P_INVERT_A or P_INVERT_B (e.g., `P_PLUS1_B | P_INVERT_B`)
:::

This flexibility means you can:

- Route clock signals to multiple data pins without external wiring
- Create complex signal processing chains
- Monitor any nearby pin from any Smart Pin
- Implement inverted logic without external components

### Synchronizing Multiple Smart Pins

Want to start multiple PWMs in perfect sync? Here's how:

::: spin2
```
PUB start_synchronized_pwm() | pins
  pins := %1111 << 20          ' Pins P23..P20

  ' Configure while disabled
  repeat pin from 20 to 23
    pinclear(pin)
    wrpin(pin, P_PWM_SAWTOOTH | P_OE)
    wxpin(pin, 10_000)         ' Same period
    wypin(pin, 2500 * (pin - 19)) ' Different duties

  ' Enable all simultaneously!
  DIRH(pins)                   ' All start together
```
:::

In PASM2, it's even more precise:

::: pasm2
```
sync_pwm
        mov     mask, #$0F      ' Four pins
        shl     mask, #20       ' P23..P20

        ' Configure all pins
        mov     pin, #20
.loop   wrpin   pwm_mode, pin
        wxpin   period, pin
        wypin   duty, pin
        add     pin, #1
        cmp     pin, #24 wz
  if_nz jmp     #.loop

        ' Simultaneous start
        dirh    mask            ' Perfect sync!
```
:::

### Common Configuration Patterns

Let's establish some patterns you'll use repeatedly:

**Pattern 1: Digital Output**

::: spin2
```
' Blinking LED
pinstart(pin, P_TRANSITION | P_OE, clkfreq/2/freq, 0)
```
:::

**Pattern 2: Analog Output**

::: spin2
```
' DAC voltage output with PRNG dithering
pinstart(pin, P_DAC_DITHER_RND | P_DAC_124R_3V | P_OE, 0, voltage)
```
:::

**Pattern 3: Digital Input**

::: spin2
```
' Count pulses
pinstart(pin, P_COUNT_RISES, 0, 0)
```
:::

**Pattern 4: Analog Input**

::: spin2
```
' ADC reading
pinstart(pin, P_ADC_1X | P_ADC_GND, 0, 0)
```
:::

**Pattern 5: Serial Communication**

::: spin2
```
' UART setup
pinstart(pin, P_ASYNC_TX | P_OE, (clkfreq/baud) << 16 | 7, 0)
```
:::

### Debugging Smart Pin Configuration

When a Smart Pin doesn't work as expected, here's your checklist:

**1. Is it enabled?**

::: spin2
```
if testp(pin)      ' Check if DIR is set
  debug("Pin is enabled")
else
  debug("Pin is NOT enabled!")
```
:::

**2. Is the mode correct?**

::: spin2
```
' Read back configuration
mode := 0  ' NOTE: Mode config cannot be read back from pin        ' Bottom 6 bits
debug("Mode: %", mode)
```
:::

**3. Are X and Y set correctly?**
Unfortunately, you can't read these back directly, but you can test:

::: spin2
```
' For output modes, change Y and see if output changes
wypin(pin, test_value)
if rdpin(pin) == expected
  debug("Y register working")
```
:::

**4. Is the input routed correctly?**

::: spin2
```
' Test with known signal
' Apply signal to expected input pin
' Check if Smart Pin responds
```
:::

### Exercise: Configuration Workout

Let's practice configuration with increasing complexity:

**Level 1: Single Pin**
Configure Pin 20 as a 1kHz square wave.

**Level 2: Multiple Pins**
Configure Pins 20-23 as PWM outputs with:

- Same frequency (10kHz)
- Different duty cycles (25%, 50%, 75%, 100%)

**Level 3: Input and Output**

- Pin 20: Generate 1kHz square wave
- Pin 21: Count pulses from Pin 20
- Display count every second

**Level 4: Complex Routing**

- Pin 10: Generate variable frequency
- Pin 30: Measure frequency from Pin 10
- Pin 31: Measure period from Pin 10
- Compare measurements

### Configuration Best Practices

Before we dive into specific modes, remember these golden rules:

1. **Always Clear First**: Don't assume pin state
2. **Use Constants**: P_* constants prevent errors
3. **Check Mode Requirements**: Some modes need specific X/Y values
4. **Enable Last**: Configure everything before enabling
5. **Document Intent**: Comment what the configuration achieves

Ready to explore all 32 modes? Let's start with the digital I/O modes!

# Part II: Progressive Mode Tutorials

## Chapter 3: Digital I/O Modes - Your Foundation

Let's start with the simplest modes and build our understanding progressively. These digital modes form the foundation for understanding more complex Smart Pin operations.

### Mode %00000 - Smart Pin OFF (Default State)

This is where every Smart Pin begins - turned off, acting like a normal I/O pin.

**When to Use:**

- Normal GPIO operations
- Resetting a misconfigured Smart Pin
- Power-sensitive applications where Smart Pins aren't needed

**How It Works:**
In this mode, the Smart Pin hardware is completely disabled. The pin behaves exactly like a traditional microcontroller I/O pin - you can read it, write it, float it, or pull it.

::: spin2
```
CON
  _clkfreq = 200_000_000
  LED_PIN = 56                  ' LED on P2 Eval board

PUB demonstrate_normal_io()
  ' Make sure Smart Pin is OFF
  pinclear(LED_PIN)

  ' Now use as normal I/O
  repeat 10
    pinh(LED_PIN)               ' LED on
    waitms(500)
    pinl(LED_PIN)               ' LED off
    waitms(500)

  ' This uses processor time for timing!
  ' Compare to Smart Pin modes that don't
```
:::

::: pasm2
```
' Normal I/O without Smart Pin - LED blink example
                org
                dirl    #LED_PIN                ' Smart Pin off
                wrpin   #0, #LED_PIN            ' Clear mode config

.loop           outh    #LED_PIN                ' LED on
                waitx   delay                   ' Wait (uses COG time)
                outl    #LED_PIN                ' LED off
                waitx   delay                   ' Wait (uses COG time)
                jmp     #.loop

delay           long    100_000_000             ' 500ms at 200MHz
LED_PIN         =       56
```
:::

**Key Point:** Notice how we need `waitms()` / `waitx` for timing? That's processor time being consumed. Every other mode we'll learn eliminates this waste.

### Mode %00001 - Repository Mode (Shared Storage)

Now for our first real Smart Pin mode - Repository. Think of it as a mailbox where any COG can leave a 32-bit value and any COG can read it.

**When to Use:**

- Inter-COG communication without hub RAM
- Storing configuration values
- Creating flags or semaphores
- Temporary value storage

**How It Works:**
The Smart Pin becomes a 32-bit storage location. Write a value with WYPIN, read it with RDPIN. The value persists until overwritten.

::: spin2
```
CON
  MAILBOX_PIN = 20              ' Our repository pin

PUB repository_demo() | value
  ' Configure as repository
  pinstart(MAILBOX_PIN, P_REPOSITORY, 0, 0)

  ' Store a value
  wypin(MAILBOX_PIN, 12345)

  ' Read it back (from same or different COG)
  value := rdpin(MAILBOX_PIN)
  debug("Repository contains: ", sdec(value))

  ' Multiple COGs can share this
  cogspin(NEWCOG, producer(), @stack1)
  cogspin(NEWCOG, consumer(), @stack2)

PRI producer()
  repeat
    wypin(MAILBOX_PIN, getrnd())
    waitms(100)

PRI consumer() | val
  repeat
    val := rdpin(MAILBOX_PIN)
    debug("Consumer got: ", uhex(val))
    waitms(150)
```
:::

**PASM2 Implementation:**

::: pasm2
```
repository_setup
        dirl    #MAILBOX_PIN    ' Clear pin first
        wrpin   ##P_REPOSITORY, #MAILBOX_PIN
        dirh    #MAILBOX_PIN    ' Enable repository

store_value
        wypin   value, #MAILBOX_PIN   ' Store 32-bit value

read_value
        rdpin   result, #MAILBOX_PIN  ' Read current value
```
:::

**Important Notes:**

- WXPIN updates the stored value and raises the IN flag
- Reading with RDPIN clears the IN flag; RQPIN does not
- Writing overwrites immediately
- During reset (DIR=0), WXPIN instructions are ignored and IN remains low
- Perfect for configuration constants and inter-COG communication

**Complete PASM2 Example:**

::: pasm2
```
                org     0
                dirh    #12                     ' Set P12 as output
                wrpin   repo_mode, #12          ' Set repository mode
                wxpin   test_data, #12          ' Store value
                nop                             ' Register clock delay
                rqpin   result, #12             ' Read (IN unchanged)

test_data       long    $1500_0000              ' Test data to store
result          long    0                       ' Retrieved value
' P_REPOSITORY = %0000_0000_000_0000000000000_00_00001_0
repo_mode       long    P_REPOSITORY
```
:::

### Mode %00001 with DAC_MODE - DAC Noise Output

When mode %00001 is combined with DAC_MODE (M[12:10] = %101), the Smart Pin generates pseudo-random noise on its DAC output instead of functioning as a repository.

**When to Use:**

- White noise generation for audio
- Dithering source for external circuits
- Test signal generation
- Randomized analog output

**How It Works:**
The pin's 8-bit DAC receives a unique pseudo-random value on every system clock cycle. Each pin configured in this mode produces a different noise pattern.

X[15:0] sets an optional sample period in clock cycles. The IN flag rises at each period completion, useful for timing synchronization. Set X[15:0] to zero for maximum period (65,536 clocks) to minimize switching power when timing is not needed.

::: spin2
```
CON
  _clkfreq = 200_000_000
  NOISE_PIN = 20

PUB dac_noise_demo()
  ' Configure DAC noise mode with 990 ohm/3.3V output
  pinstart(NOISE_PIN, P_DAC_NOISE | P_DAC_990R_3V | P_OE, 0, 0)

  ' Output runs continuously - nothing more to do
  repeat
    waitms(1000)
    debug("DAC noise running on pin ", udec(NOISE_PIN))
```
:::

::: pasm2
```
' DAC Noise output - generates pseudo-random analog noise
                org
                dirl    #NOISE_PIN              ' Reset pin
                wrpin   dac_noise_cfg, #NOISE_PIN ' DAC noise mode
                dirh    #NOISE_PIN              ' Start DAC noise output

.loop           nop                             ' Runs continuously
                jmp     #.loop

' P_DAC_NOISE with DAC mode: M[12:10]=%101, TT=%01, Mode=%00001
dac_noise_cfg   long    P_DAC_NOISE | P_DAC_990R_3V | P_OE
NOISE_PIN       =       20
```
:::

**Important Notes:**

- This mode overrides M[7:0] to feed the DAC
- M[12:10] must be %101 to enable DAC output
- RDPIN/RQPIN retrieves the 16-bit ADC accumulation from the last sample period
- During reset (DIR=0), IN is low

---

### Mode %00010 & %00011 - DAC Dithering Modes

The P2's Smart Pins include sophisticated DAC (Digital to Analog Converter) capabilities with optional dithering for enhanced resolution.

**When to Use:**

- Generating analog voltages
- Audio output (use PRNG dithering)
- Video generation (75$\Omega$ mode with PWM dithering)
- Control voltages for external circuits
- Sensor simulation

**How It Works:**

The DAC converts a digital value to an analog voltage, with optional dithering to improve effective resolution beyond the native 8-bit range.

```{=latex}
\DACPWMPeriodDiagram
```

**Understanding DAC Configuration**

DAC configuration involves TWO separate aspects:

1. **Mode (%00010 or %00011)** - Selects the dithering algorithm
2. **Drive Configuration (M bits)** - Selects impedance and voltage range

**Mode %00010 (P_DAC_DITHER_RND): DAC with PRNG Dithering**

- Uses pseudo-random noise dithering
- Better for audio applications
- Spreads quantization noise across frequency spectrum
- No fixed period required - can update output value at any time

**Mode %00011 (P_DAC_DITHER_PWM): DAC with PWM Dithering**

- Uses PWM-based dithering
- Better dynamic range than PRNG (maximum two transitions per 256 clocks)
- Produces a predictable tone at Fclock/256 at -48dB
- Sample period must be a multiple of 256 clocks (X[7:0]=0) for proper operation

**Register Configuration:**

| Register | Function |
|----------|----------|
| X[15:0] | Sample period in clock cycles. Set to 1 for immediate updates (IN stays high). For PWM mode, must be multiple of 256. |
| Y[15:0] | DAC output value (0-65535). Captured at each sample period completion. |

**Timing Coordination:**
On completion of each sample period, Y[15:0] is captured for the next output value and the IN flag rises. Coordinate Y register updates with IN going high for glitch-free output.

**ADC Feedback:**
When OUT is high, the internal ADC is enabled. Use RDPIN/RQPIN to retrieve the 16-bit ADC accumulation from the previous sample period. This measures actual loading on the DAC pin - useful for current sensing or calibration.

**Drive Strength/Voltage Configuration Constants (set via M bits):**
| Constant | Impedance | Voltage | Use Case |
|----------|-----------|---------|----------|
| P_DAC_990R_3V | 990$\Omega$ | 3.3V | General purpose, low current |
| P_DAC_600R_2V | 600$\Omega$ | 2.0V | Moderate drive |
| P_DAC_124R_3V | 124$\Omega$ | 3.3V | Higher current, fast response |
| P_DAC_75R_2V | 75$\Omega$ | 2.0V | Video output (75$\Omega$ termination) |

**Configuration Example:**

::: spin2
```
CON
  DAC_PIN = 16

PUB dac_demo() | level
  ' Configure DAC with PRNG dithering and 3.3V/124 ohm output
  ' Mode = P_DAC_DITHER_RND, Drive = P_DAC_124R_3V
  pinstart(DAC_PIN, P_DAC_DITHER_RND | P_DAC_124R_3V | P_OE, 0, 0)

  ' Generate a slow ramp
  repeat
    repeat level from 0 to $FFFF step $100
      wypin(DAC_PIN, level)
      waitus(100)
    repeat level from $FFFF to 0 step $100
      wypin(DAC_PIN, level)
      waitus(100)

PUB video_dac_setup()
  ' Configure DAC for video output (75 ohm, 2.0V, PWM dithering)
  pinstart(VIDEO_PIN, P_DAC_DITHER_PWM | P_DAC_75R_2V | P_OE, 0, 0)
```
:::

**Audio DAC with PRNG Dithering:**

::: spin2
```
PUB sine_wave_output() | angle
  ' Use PRNG dithering for best audio quality
  pinstart(DAC_PIN, P_DAC_DITHER_RND | P_DAC_124R_3V | P_OE, 0, 0)

  repeat
    repeat angle from 0 to 359
      wypin(DAC_PIN, $8000 + (qsin(angle, 360, $7FFF)))
      waitus(28)  ' ~1kHz sine wave
```
:::

**PASM2 Implementation:**

::: pasm2
```
dac_setup
        dirl    #DAC_PIN
        ' PRNG dithering + 124 ohm/3.3V drive + output enable
        wrpin   ##P_DAC_DITHER_RND | P_DAC_124R_3V | P_OE, #DAC_PIN
        dirh    #DAC_PIN

output_voltage
        wypin   value, #DAC_PIN ' Output 16-bit value
```
:::

**Complete PASM2 Sawtooth Generator:**

::: pasm2
```
                org     0
                dirl    #20                     ' Reset DAC at pin P20
                wrpin   dac_config, #20         ' Configure DAC mode
                wxpin   dac_period, #20         ' Set sample period
                dirh    #20                     ' Enable DAC

.loop           wypin   dac_volt, #20           ' Output voltage value
.wait_period    nop
                testp   #20 wc                  ' Test IN flag
        if_nc   jmp     #.wait_period           ' Wait for sample period
                add     dac_volt, #$100         ' Add 256 to voltage
                jmp     #.loop                  ' Repeat forever

' DAC dither with PRNG: %0000_0000_000_10100_00000000_01_00010_0
'   DAC mode M[12:10]=%101 (P_DAC_990R_3V), TT=%01 (P_OE), Mode=%00010
dac_config      long    P_DAC_DITHER_RND | P_DAC_990R_3V | P_OE
dac_period      long    $100                    ' 256 clk sample period
dac_volt        long    0                       ' Y[15:0] voltage value
```
:::

::: tip
The dithering modes provide effective 16-bit resolution from the 8-bit DAC hardware by rapidly alternating between adjacent levels. PRNG dithering uses pseudo-random patterns that spread noise across frequencies (better for audio), while PWM dithering uses deterministic patterns (better for control signals).
:::

### Mode %00100 - Pulse/Cycle Output

This mode generates precise pulses or continuous cycles with programmable high and low times.

**When to Use:**

- Servo control pulses
- Stepper motor control
- Custom protocol generation
- Precise timing sequences
- One-shot or continuous pulses

**How It Works:**

The mode uses a countdown counter and comparison value to generate pulses with programmable high and low times.

```{=latex}
\PulseWidthMeasurementDiagram
```

The counter counts down from the base period, comparing against a threshold to determine output state:

| Register | Function |
|----------|----------|
| X[15:0] | Base period in clock cycles. Counter counts down from this value to 1, then restarts if Y > 0. |
| X[31:16] | Comparison threshold. Output is HIGH when counter > X[31:16] and Y > 0, else LOW. |
| Y[31:0] | Pulse count. Decrements after each complete cycle. IN rises when Y reaches zero. |

**Timing Examples:**

- X[31:16]=0: Output stays HIGH for entire duration while Y > 0
- X[15:0]=3, X[31:16]=2: Output pattern is 0-0-1 (repeat) - one clock HIGH, two clocks LOW per cycle

**Logic Inversion:**
For logic-0 pulses (inverted), set the P5 bit in the mode configuration:
`%0000_0000_000_00000_00_1_00000_11_00100_0` (note P5=1)

This mode overrides OUT to control the pin output state. During reset (DIR=0), IN is low, output is low, and Y is cleared to zero.

::: spin2
```
CON
  _clkfreq  = 200_000_000              ' System clock frequency
  US_001    = _clkfreq / 1_000_000     ' Clocks per microsecond
  MS_001    = _clkfreq / 1_000         ' Clocks per millisecond
  SERVO_PIN = 24

PUB servo_control(angle) | pulse_width
  ' Servo: 1-2ms pulse every 20ms
  ' angle: 0-180 degrees

  pulse_width := 1000 + (angle * 1000 / 180)  ' 1000-2000us

  ' Configure for servo pulses
  pinstart(SERVO_PIN, P_PULSE | P_OE, ...
    (pulse_width * US_001) << 16 | ...
    (20_000 - pulse_width) * US_001, 0)  ' Continuous

PUB single_pulse(width_us)
  ' Generate a single pulse
  pinstart(PULSE_PIN, P_PULSE | P_OE, ...
    width_us * US_001 << 16 | 1000 * US_001, ...
    1)  ' Just one pulse

  ' Wait for completion
  repeat while testp(PULSE_PIN)
```
:::

**Complete PASM2 Pulse Example:**

This example generates 16 logic-1 pulses at 25 MHz system clock (60$\mu$s pulse, 20$\mu$s low):

::: pasm2
```
' 25-MHz system clock frequency
                org     0
                dirl    #20                     ' Reset Smart Pin at P20
                wrpin   pulse_config, #20       ' Set pulse/cycle mode
                wxpin   pulse_timing, #20       ' Set timing parameters
                dirh    #20                     ' Enable Smart Pin
                wypin   cycles, #20             ' Load pulse count
                nop                             ' Delay for IN to clear

.wait           testp   #20 wc                  ' Check IN flag
        if_nc   jmp     #.wait                  ' Wait for pulses

' Pulse mode: %0000_0000_000_00000_00000000_11_00100_0
'   TT=%11 (output override active), Mode=%00100
pulse_config    long    P_PULSE | P_OE | P_TT_10
cycles          long    $0010                   ' 16 pulses
' X[31:16]=$01F4 (500 clks), X[15:0]=$05DC (1500 clks)
' At 25MHz: 60us high, 20us low per cycle
pulse_timing    long    $01F4_05DC
```
:::

**PASM2 Pulse Generation (Generic):**

::: pasm2
```
pulse_gen
        dirl    #PULSE_PIN
        wrpin   ##P_PULSE | P_OE, #PULSE_PIN

        ' Set pulse timing: X[31:16]=comparison, X[15:0]=base period
        mov     x, compare_val
        shl     x, #16
        or      x, base_period
        wxpin   x, #PULSE_PIN

        ' Set pulse count (0 = continuous)
        wypin   pulse_count, #PULSE_PIN

        dirh    #PULSE_PIN              ' Start pulsing
```
:::

### Mode %00101 - Transition Output

Transition output mode generates edges at programmable intervals - perfect for clocks and timing references.

**When to Use:**

- Clock generation
- Baud rate generation
- Timing references
- Square wave output

**How It Works:**

This mode produces a series of pulses with equal logic-0 and logic-1 periods.

| Register | Function |
|----------|----------|
| X[15:0] | Base period in clock cycles between transitions |
| Y[31:0] | Number of transitions (edges) to generate. Decrements after each toggle. |

The pin starts at logic-0 and toggles at each base period while Y > 0. The IN flag rises when Y reaches zero, with the pin remaining in its final state.

**Odd vs Even Transition Counts:**

- Even count (e.g., 8): Output returns to logic-0 when complete
- Odd count (e.g., 7): Output remains logic-1 when complete

This mode overrides OUT to control the pin output state. During reset (DIR=0), IN is low, output is low, and Y is cleared to zero.

::: spin2
```
PUB clock_generator(pin, freq_hz) | period
  ' Calculate period for transitions
  period := clkfreq / (freq_hz * 2)  ' Two transitions per cycle

  pinstart(pin, P_TRANSITION | P_OE, period, 0)

PUB multiple_clocks()
  ' Generate multiple clock frequencies
  clock_generator(20, 1_000_000)     ' 1MHz
  clock_generator(21, 500_000)       ' 500kHz
  clock_generator(22, 100_000)       ' 100kHz
  clock_generator(23, 10_000)        ' 10kHz
```
:::

**Complete PASM2 Transition Example:**

This example generates 16 transitions (8 complete cycles) with 1500 system clocks between each edge:

::: pasm2
```
                org     0
                dirl    #20                     ' Reset Smart Pin at P20
                wrpin   trans_config, #20       ' Set transition mode
                wxpin   trans_timing, #20       ' Set transition period
                dirh    #20                     ' Enable Smart Pin
                wypin   cycles, #20             ' Load transition count

.wait           nop                             ' Delay for IN to clear
                testp   #20 wc                  ' Check IN flag
        if_nc   jmp     #.wait                  ' Wait for transitions

' Transition mode: %0000_0000_000_0000_000000000_11_00101_0
'   TT=%11 (output override active), Mode=%00101
trans_config    long    P_TRANSITION | P_OE | P_TT_10
cycles          long    $0010                   ' 16 trans (8 cycles)
trans_timing    long    $0000_05DC              ' 1500 clks/transition
```
:::

**PASM2 Continuous Clock Generation:**

::: pasm2
```
trans_out
        dirl    #TRANS_PIN
        wrpin   ##P_TRANSITION | P_OE, #TRANS_PIN

        ' Set transition period
        mov     period, ##100_000           ' 100k clocks/transition
        wxpin   period, #TRANS_PIN

        wypin   ##0, #TRANS_PIN             ' Y=0 for continuous output
        dirh    #TRANS_PIN                  ' Start toggling
```
:::

### Mode %00110 - NCO Frequency

NCO (Numerically Controlled Oscillator) mode generates precise frequencies using phase accumulation.

**When to Use:**

- Clock generation
- Frequency synthesis
- Audio tone generation
- Carrier wave generation
- Precision frequency references

**How It Works:**

The NCO uses a phase accumulator that adds a fixed increment each clock cycle; the MSB of the accumulator drives the output pin.

```{=latex}
\NCOFrequencyDiagram
```

The phase accumulator overflows at a rate determined by the increment value, producing precise output frequencies:

| Register | Function |
|----------|----------|
| X[15:0] | Base period divider. Divides system clock to create base frequency. X=1 means no division. |
| X[31:16] | Phase preload. Written to Z[31:16] on WXPIN for initial phase offset. |
| Y[31:0] | Phase increment. Added to Z[31:0] at each base period. |
| Z[31:0] | Phase accumulator (internal). Z[31] drives pin output. |

**Output Behavior:**

- Pin output reflects Z[31] bit state
- IN flag rises whenever Z overflows ($Z > 2^{32}$)
- Higher Y values = higher output frequency

**Frequency Calculation:**
$$\text{Base Frequency} = \frac{\text{System Clock}}{X[15:0]}$$

$$\text{Output Frequency} = \frac{Y \times \text{Base Frequency}}{2^{32}}$$

For direct system clock operation (X=1):

$$\text{Output Frequency} = \frac{Y \times \text{System Clock}}{2^{32}}$$

$$Y = \frac{\text{Desired Frequency} \times 2^{32}}{\text{System Clock}}$$

This mode overrides OUT to control the pin output state. During reset (DIR=0), IN is low, output is low, and Z is cleared to zero.

::: spin2
```
PUB nco_frequency(pin, freq_hz) | x
  ' Calculate X value for desired frequency
  x := freq_hz frac clkfreq

  pinstart(pin, P_NCO_FREQ | P_OE, x, 0)

PUB audio_tones()
  ' Musical note frequencies
  nco_frequency(20, 440)       ' A4
  nco_frequency(21, 494)       ' B4
  nco_frequency(22, 523)       ' C5
  nco_frequency(23, 587)       ' D5
```
:::

**Complete PASM2 NCO Example:**

This example configures an NCO at 25 MHz system clock with frequency calculation:

::: pasm2
```
' 25-MHz system clock frequency
_clk_freq       =       25_000_000

                org     0
                dirl    #20                     ' Reset Smart Pin at P20
                wrpin   nco_config, #20         ' NCO frequency mode
                wxpin   #1, #20                 ' X=1: no div (25MHz)
                dirh    #20                     ' Enable Smart Pin

                ' Calculate Y for desired frequency using CORDIC
                qfrac   ##123, ##_clk_freq      ' Calc cycles for 123 Hz
                getqx   pa                      ' Get result in PA
                wypin   pa, #20                 ' Load phase increment

.loop           nop
                jmp     #.loop                  ' Run forever

' P_NCO_FREQ | P_OE = %0000_0000_000_0000_000000000_01_00110_0
nco_config      long    P_NCO_FREQ | P_OE
```
:::

**Precision Frequency Generation:**

::: spin2
```
PUB precise_10khz() | x
  ' Generate exactly 10.000kHz
  x := 10_000 frac clkfreq     ' Fractional math for precision

  pinstart(FREQ_PIN, P_NCO_FREQ | P_OE, x, 0)

  ' Verify actual frequency
  debug("X value: ", uhex_long(x))
  debug("Actual freq: ", ...
    fdec(float(x) *. float(clkfreq) /. 4294967296.0))
```
:::

**PASM2 NCO Setup:**

::: pasm2
```
nco_freq
        dirl    #NCO_PIN
        wrpin   ##P_NCO_FREQ | P_OE, #NCO_PIN

        ' Calculate X for frequency
        qfrac   frequency, ##1    ' frequency / clkfreq
        getqx   x_value
        wxpin   x_value, #NCO_PIN

        dirh    #NCO_PIN         ' Start oscillating
```
:::

### Mode %00111 - NCO Duty

NCO Duty mode generates PWM with precise duty cycle control at a specific frequency.

**When to Use:**

- PWM with specific frequency AND duty
- LED brightness control at fixed frequency
- Motor control with precise timing
- Power supply control

**How It Works:**

This mode creates logic-1 pulses of fixed duration with programmable spacing, using a phase accumulator to control both frequency and duty cycle independently.

```{=latex}
\NCODutyTimingDiagram
```

The internal architecture shows how the Z accumulator controls duty cycle:

```{=latex}
\NCODutyBlockDiagram
```

Unlike NCO Frequency mode which generates 50% duty, NCO Duty allows independent control of pulse width and period:

| Register | Function |
|----------|----------|
| X[15:0] | Base period divider. Determines the logic-1 pulse duration. |
| X[31:16] | Phase preload. Written to Z[31:16] on WXPIN for initial phase. |
| Y[31:0] | Period control. Added to Z[31:0] at each base period. Controls time between pulse starts. |
| Z[31:0] | Phase accumulator (internal). Output goes HIGH on Z overflow. |

**Timing Control:**

- Pulse width = System Clock Period $\times$ X[15:0]
- Pulse period = $2^{32} / Y$ (in base period units)

**Worked Example: 1$\mu$s pulse every 18$\mu$s at 25 MHz:**

1. For 1$\mu$s pulse width: X[15:0] = 25 (25 MHz $\div$ 25 = 1$\mu$s base period)
2. For 18$\mu$s period: $Y = 2^{32} \div 18 = 238,609,294$ = \$0E38\_E38E

The IN flag rises whenever Z overflows. This mode overrides OUT to control the pin output state. During reset (DIR=0), IN is low, output is low, and Z is cleared to zero.

::: spin2
```
PUB nco_duty_demo(pin, freq_hz, duty_percent) | x, y
  ' Calculate frequency
  x := freq_hz frac clkfreq

  ' Calculate duty threshold
  y := duty_percent * $FFFFFFFF / 100

  pinstart(pin, P_NCO_DUTY | P_OE, x, y)

PUB breathing_led() | brightness
  ' Configure for 1kHz PWM
  x := 1000 frac clkfreq
  wrpin(LED_PIN, P_NCO_DUTY | P_OE)
  wxpin(LED_PIN, x)
  dirh(LED_PIN)

  ' Smoothly vary brightness
  repeat
    repeat brightness from 0 to 100
      wypin(LED_PIN, brightness * $FFFFFFFF / 100)
      waitms(10)
    repeat brightness from 100 to 0
      wypin(LED_PIN, brightness * $FFFFFFFF / 100)
      waitms(10)
```
:::

**Complete PASM2 NCO Duty Example:**

This example generates 1$\mu$s pulses every 18$\mu$s at 25 MHz:

::: pasm2
```
' 25-MHz system clock frequency
                org     0
                dirl    #20                     ' Reset Smart Pin at P20
                wrpin   nco_duty_cfg, #20       ' NCO duty mode
                wxpin   #25, #20                ' X=25: 1us (25MHz/25)
                dirh    #20                     ' Enable Smart Pin
                wypin   y_period, #20           ' Load period value

.loop           nop
                jmp     #.loop                  ' Run forever

' P_NCO_DUTY | P_OE = %0000_0000_000_0000_000000000_01_00111_0
nco_duty_cfg    long    P_NCO_DUTY | P_OE
y_period        long    $0E38_E38E              ' 2^32/18 = 18us period
```
:::

**PASM2 Generic NCO Duty Setup:**

::: pasm2
```
nco_duty
        dirl    #DUTY_PIN
        wrpin   ##P_NCO_DUTY | P_OE, #DUTY_PIN
        wxpin   freq_x, #DUTY_PIN    ' Set pulse width via X[15:0]
        wypin   duty_y, #DUTY_PIN    ' Set period via Y
        dirh    #DUTY_PIN            ' Enable
```
:::

### Mode %01000 - PWM Triangle

PWM Triangle mode provides phase-correct PWM using a symmetric triangle wave comparison.

**When to Use:**

- Phase-correct PWM needed
- Audio applications
- Symmetric PWM requirements
- Reduced harmonics applications

**How It Works:**

This mode uses an up-down counter to create phase-correct PWM; the output changes state when the counter crosses the threshold value.

```{=latex}
\TrianglePWMDiagram
```

The symmetric counting produces centered pulses with reduced harmonic content:

| Register | Function |
|----------|----------|
| X[15:0] | Base period divider. Divides system clock to create base period units. |
| X[31:16] | Frame period in base period units. Counter counts down from this value to 1, then up to frame period. |
| Y[15:0] | PWM threshold (0 to frame period). Captured at each frame start. |

**Counter Operation:**
The counter counts from frame period down to 1, then from 1 back up to frame period. When counter $\leq$ Y, output is HIGH; when counter $>$ Y, output is LOW.

**Timing:**

- Base period = System Clock Period $\times$ X[15:0]
- Frame period = Base period $\times$ X[31:16]
- **PWM period = $2 \times$ Frame period** (due to up-down counting)

**Worked Example at 25 MHz:**

- X[15:0] = 1 (no division, 40ns base period)
- X[31:16] = \$200 (512)
- Frame period = 40ns $\times$ 512 = 20.48$\mu$s
- PWM period = $2 \times 20.48$$\mu$s = 40.96$\mu$s (~24.4 kHz)

**Duty Limits:**

- Y = 0: Constant LOW output
- Y = frame period: Constant HIGH output

This mode overrides OUT. During reset (DIR=0), IN is low, output is low, and Y[15:0] is captured.

::: spin2
```
PUB pwm_triangle(pin, freq_hz, duty_percent) | period, duty
  ' Triangle PWM has 2X period due to up/down counting
  period := clkfreq / (freq_hz * 2)
  duty := period * duty_percent / 100

  pinstart(pin, P_PWM_TRIANGLE | P_OE, period, duty)

PUB phase_correct_pwm()
  ' Phase-correct PWM for audio
  pinstart(AUDIO_PIN, P_PWM_TRIANGLE | P_OE, 256, 128)  ' 50% duty

  ' Modulate for audio
  repeat sample from 0 to 255
    wypin(AUDIO_PIN, sample)
    waitus(125)  ' 8kHz sample rate
```
:::

**Complete PASM2 Triangle PWM Example:**

::: pasm2
```
' 25 MHz system-clock frequency
                org     0
                dirl    #20                     ' Reset Smart Pin at P20
                wrpin   pwm_tri_cfg, #20        ' PWM triangle mode
                wxpin   x_regdata, #20          ' Base and frame period
                dirh    #20                     ' Enable Smart Pin
                wypin   y_regdata, #20          ' Set PWM threshold

.loop           nop
                jmp     #.loop                  ' Run forever

' P_PWM_TRIANGLE | P_OE = %0000_0000_000_00000_00000000_01_01000_0
pwm_tri_cfg     long    P_PWM_TRIANGLE | P_OE
y_regdata       long    $0000_0080              ' Y=128 (threshold)
' X[31:16]=$200 (frame=512), X[15:0]=1 (no division)
x_regdata       long    $0200_0001
```
:::

**PASM2 Triangle PWM (Generic):**

::: pasm2
```
pwm_tri
        dirl    #PWM_PIN
        wrpin   ##P_PWM_TRIANGLE | P_OE, #PWM_PIN
        wxpin   x_config, #PWM_PIN      ' X[31:16]=frame, X[15:0]=div
        wypin   duty_value, #PWM_PIN    ' Set duty threshold
        dirh    #PWM_PIN
```
:::

### Mode %01001 - PWM Sawtooth

PWM Sawtooth mode provides high-resolution PWM using a sawtooth (ramp-reset) comparison.

**When to Use:**

- Motor speed control
- LED dimming
- Power control
- Analog voltage generation (with filtering)

**How It Works:**

This mode uses an up counter that resets when reaching the frame period; output is high while counter is below the threshold.

```{=latex}
\SawtoothPWMDiagram
```

Unlike Triangle mode, the PWM period equals the frame period (not $2\times$), providing edge-aligned PWM:

| Register | Function |
|----------|----------|
| X[15:0] | Base period divider. Divides system clock to create base period units. |
| X[31:16] | Frame period in base period units. Counter counts from 1 up to this value. |
| Y[15:0] | PWM threshold (0 to frame period). Captured at each frame start. |

**Counter Operation:**
Counter counts from 1 up to frame period, then resets to 1. When counter $\leq$ Y, output is HIGH; when counter $>$ Y, output is LOW. The IN flag rises at each frame reset.

**Key Difference from Triangle:**

- **Sawtooth:** PWM period = Frame period (up count only)
- **Triangle:** PWM period = $2 \times$ Frame period (up-down count)

**Duty Limits:**

- Y = 0: Constant LOW output
- Y = frame period: Constant HIGH output

This mode overrides OUT. During reset (DIR=0), IN is low, output is low, and Y[15:0] is captured.

::: spin2
```
PUB pwm_sawtooth(pin, freq_hz, duty_percent) | period, duty
  ' Calculate period
  period := clkfreq / freq_hz

  ' Calculate duty
  duty := period * duty_percent / 100

  pinstart(pin, P_PWM_SAWTOOTH | P_OE, period, duty)

PUB motor_control(speed_percent)
  ' 20kHz PWM for motor control
  period := clkfreq / 20_000    ' 20kHz
  duty := period * speed_percent / 100

  pinstart(MOTOR_PIN, P_PWM_SAWTOOTH | P_OE, period, duty)

PUB dynamic_pwm() | duty
  ' Dynamically adjust PWM duty
  pinstart(PWM_PIN, P_PWM_SAWTOOTH | P_OE, 10_000, 0)

  repeat
    repeat duty from 0 to 10_000 step 100
      wypin(PWM_PIN, duty)     ' Update duty cycle
      waitms(10)
```
:::

**Complete PASM2 Sawtooth PWM Example:**

::: pasm2
```
' 25 MHz system-clock frequency
                org     0
                dirl    #20                     ' Reset Smart Pin at P20
                wrpin   pwm_saw_cfg, #20        ' PWM sawtooth mode
                wxpin   x_regdata, #20          ' Base and frame period
                dirh    #20                     ' Enable Smart Pin
                wypin   y_regdata, #20          ' Set PWM threshold

.loop           nop
                jmp     #.loop                  ' Run forever

' P_PWM_SAWTOOTH | P_OE = %0000_0000_000_00000_00000000_01_01001_0
pwm_saw_cfg     long    P_PWM_SAWTOOTH | P_OE
y_regdata       long    $0000_0080              ' Y=128 (threshold)
' X[31:16]=$200 (frame=512), X[15:0]=1 (no division)
x_regdata       long    $0200_0001
```
:::

**PASM2 Sawtooth PWM (Generic):**

::: pasm2
```
pwm_saw
        dirl    #PWM_PIN
        wrpin   ##P_PWM_SAWTOOTH | P_OE, #PWM_PIN
        wxpin   x_config, #PWM_PIN      ' X[31:16]=frame, X[15:0]=div
        wypin   duty_value, #PWM_PIN    ' Set duty threshold
        dirh    #PWM_PIN                ' Start PWM

update_duty
        wypin   new_duty, #PWM_PIN      ' Change duty on the fly
```
:::

### Mode %01010 - Switch-Mode Power Supply

This specialized mode provides PWM control for switch-mode power supplies with integrated voltage and current feedback. This mode overrides OUT to control the pin output state.

**When to Use:**

- DC-DC converters (buck, boost, buck-boost)
- LED drivers with current limiting
- Motor drivers with current protection
- Any application requiring closed-loop power control

**Register Configuration:**

| Register | Function |
|----------|----------|
| X[15:0] | Base period in system clock cycles |
| X[31:16] | PWM frame period in base periods |
| Y[15:0] | PWM output value (duty threshold, 0 to frame period) |

**How It Works:**

A counter updates at each base period, counting from one up to the frame period. At each base period:

1. The captured output value (Y[15:0]) is compared to the counter
2. If output value $\geq$ counter, output is HIGH
3. If output value $<$ counter, output is LOW

After the counter reaches the frame period, the 'A' input is sampled at each base period until it reads LOW. When 'A' reads LOW:

- Y[15:0] is captured for the next frame
- IN is raised
- The cycle repeats

**The A and B Feedback Inputs:**

The 'A' input serves as the voltage detector for the SMPS output. Configure an adjacent pin in DAC comparison mode to observe a voltage divider on the final SMPS output. When 'A' is LOW, the output voltage has sagged below the setpoint and a new PWM cycle begins.

The 'B' input serves as the over-current detector. If 'B' ever goes HIGH during a PWM cycle, the output is immediately forced LOW for the rest of that cycle. Configure an adjacent pin in DAC comparison mode to monitor a shunt resistor between ground and the FET source. When the shunt voltage exceeds the threshold, the FET turns off to limit current.

**Typical SMPS Operation:**

1. PWM output drives FET gate HIGH
2. Current flows through inductor, building magnetic field
3. When 'B' (current sense) goes HIGH, or duty cycle expires, FET turns off
4. Inductor energy transfers through diode to output capacitor
5. When 'A' (voltage sense) goes LOW, next cycle begins

**Reset Behavior:**

During reset (DIR=0):

- IN is LOW
- Output is LOW
- Y[15:0] is captured

**Application Note:**

Due to the nature of switch-mode power supplies, set Y[15:0] once and let it repeat indefinitely. The feedback inputs handle regulation automatically.

::: spin2
```
CON
  _clkfreq = 200_000_000
  SMPS_PIN = 20                 ' PWM output to FET gate
  ' A input (P21) = voltage feedback from DAC comparator
  ' B input (P22) = current feedback from DAC comparator

PUB smps_controller() | duty
  ' Configure SMPS mode
  ' P_PLUS1_B selects P21 for B-input (current sense)
  ' A-input is same pin by default (voltage sense)
  duty := 50                    ' 50% initial duty cycle

  ' X[15:0]=200 (1us base @ 200MHz)
  ' X[31:16]=100 (100 base periods = 100us frame = 10kHz PWM)
  pinstart(SMPS_PIN, P_PWM_SMPS | P_OE | P_PLUS1_B, $0064_00C8, duty)

  ' SMPS runs autonomously - feedback inputs control regulation
  repeat
    waitms(1000)
    debug("SMPS running, duty = ", udec(duty))
```
:::

::: pasm2
```
' Switch-mode power supply controller
' A input (P21) = voltage feedback from DAC comparator
' B input (P22) = current feedback from DAC comparator
' 200 MHz system clock, 10 kHz PWM frequency
                org
                dirl    #SMPS_PIN               ' Reset Smart Pin
                wrpin   smps_cfg, #SMPS_PIN     ' Configure SMPS mode
                wxpin   x_regdata, #SMPS_PIN    ' Base period + frame
                dirh    #SMPS_PIN               ' Enable Smart Pin
                wypin   y_regdata, #SMPS_PIN    ' Set initial duty cycle

.loop           nop
                jmp     #.loop                  ' Feedback controls it

' SMPS mode with B-input from P21: BBBB=%0001 (P_PLUS1_B), TT=%01 (P_OE)
smps_cfg        long    P_PWM_SMPS | P_OE | P_PLUS1_B
' X[15:0]=200 (1us base @200MHz), X[31:16]=100 (100 periods=10kHz)
x_regdata       long    $0064_00C8
' Y[15:0]=50 (50% initial duty)
y_regdata       long    $0000_0032
SMPS_PIN        =       20
```
:::

### Choosing the Right Output Generation Mode

With seven different output generation modes available, how do you pick the right one? This section provides a comprehensive comparison to guide your decision.

**Output Generation Modes Overview**

| Constant | X Register | Y Register | Output Behavior |
|----------|------------|------------|-----------------|
| P_PULSE | Base period | High/low times | Single or continuous pulses |
| P_TRANSITION | Toggle period | (unused) | State change at intervals |
| P_NCO_FREQ | Frequency word | (unused) | Precise frequency synthesis |
| P_NCO_DUTY | Frequency word | Duty threshold | Frequency + duty control |
| P_PWM_TRIANGLE | Period/2 | Duty value | Symmetric PWM (phase-correct) |
| P_PWM_SAWTOOTH | Period | Duty value | Standard PWM (fast) |
| P_PWM_SMPS | Base/Frame period | Duty threshold | SMPS with V/I feedback |

**P_PULSE vs P_TRANSITION: When to Use Each**

Both modes generate square waves, but they work differently:

**P_PULSE (%00100):**

- Generates precise pulses with configurable high AND low times
- X sets base period, Y[31:16] and Y[15:0] set high/low times
- Best for: Servo control, asymmetric pulses, one-shot timing
- Can generate a single pulse or continuous stream

**P_TRANSITION (%00101):**

- Toggles output at fixed intervals
- X sets the toggle period (half the output period)
- Best for: Clock generation, baud rate clocks, simple square waves
- Simpler to configure than Pulse mode

::: spin2
```
' Same 1MHz output using both modes

' TRANSITION: Simple - just set toggle period
' Output toggles every 100 clocks = 1MHz at 200MHz sysclk
pinstart(pin, P_TRANSITION | P_OE, 100, 0)

' PULSE: More control - specify high and low times separately
' High=100 clocks, Low=100 clocks = 1MHz at 200MHz sysclk
pinstart(pin, P_PULSE | P_OE, 1, 100 << 16 | 100)
```
:::

**P_NCO_FREQ vs P_NCO_DUTY: Frequency Synthesis Modes**

Both use Numerically Controlled Oscillator (NCO) for precise frequency generation:

**P_NCO_FREQ (%00110):**

- Output frequency = $(X \times \text{ClockFreq}) / 2^{32}$
- 50% duty cycle always
- Resolution: Sub-Hz precision at any frequency
- Best for: Clocks, carriers, audio tones, DDS applications

**P_NCO_DUTY (%00111):**

- Same frequency formula as NCO_FREQ
- Y sets duty cycle threshold (0-$FFFFFFFF)
- Best for: PWM at precise frequencies, LED dimming at specific rates

::: spin2
```
' Generate exactly 440Hz (A4 musical note)

' NCO_FREQ: Fixed 50% duty
x := 440 frac clkfreq        ' Calculate frequency word
pinstart(pin, P_NCO_FREQ | P_OE, x, 0)

' NCO_DUTY: Same frequency, but 25% duty
pinstart(pin, P_NCO_DUTY | P_OE, x, $40000000)  ' 25% threshold
```
:::

**P_PWM_TRIANGLE vs P_PWM_SAWTOOTH: PWM Waveform Selection**

Both generate PWM, but with different counter behavior:

**P_PWM_TRIANGLE (%01000):**

- Counter counts UP to X, then DOWN to 0
- Output changes state when counter crosses Y
- Period = $2 \times X$ clocks
- Symmetric switching (phase-correct)
- Best for: Audio DAC, motor H-bridges, reduced EMI

**P_PWM_SAWTOOTH (%01001):**

- Counter counts UP to X, then resets to 0
- Output is HIGH when counter < Y
- Period = X clocks
- Faster update response
- Best for: Motor speed control, LED dimming, general PWM

::: spin2
```
' 20kHz PWM at 50% duty using both modes
' Assume 200MHz sysclk

' SAWTOOTH: Period = X = 10,000 clocks
pinstart(pin, P_PWM_SAWTOOTH | P_OE, 10_000, 5_000)

' TRIANGLE: Period = 2*X, so X = 5,000 clocks
pinstart(pin, P_PWM_TRIANGLE | P_OE, 5_000, 2_500)
```
:::

**P_PWM_SMPS: Special Case for Power Supplies**

**P_PWM_SMPS (%01010):**

- Designed for switch-mode power supply control
- Uses A-input as ADC feedback (current sense)
- Automatically adjusts duty cycle to maintain target
- Best for: DC-DC converters, LED drivers with current control

**Decision Flowchart: Selecting an Output Mode**

```{=latex}
\OutputModeFlowchart
```

**Same Frequency, Different Modes: A Practical Example**

Generating a 10kHz signal at 200MHz sysclk:

::: spin2
```
CON
  _clkfreq = 200_000_000
  TARGET_FREQ = 10_000

PUB compare_modes()
  ' Method 1: TRANSITION - Toggle every 10,000 clocks
  ' Period = 20,000 clocks = 10kHz
  pinstart(20, P_TRANSITION | P_OE, _clkfreq / (TARGET_FREQ * 2), 0)

  ' Method 2: NCO_FREQ - Phase accumulator
  ' Sub-Hz precision, always 50% duty
  pinstart(21, P_NCO_FREQ | P_OE, TARGET_FREQ frac _clkfreq, 0)

  ' Method 3: PWM_SAWTOOTH - Standard PWM
  ' Period = 20,000 clocks, duty = 50%
  pinstart(22, P_PWM_SAWTOOTH | P_OE, ...
    _clkfreq / TARGET_FREQ, _clkfreq / TARGET_FREQ / 2)

  ' Method 4: PWM_TRIANGLE - Phase-correct PWM
  ' Period = 2 * 10,000 = 20,000 clocks
  pinstart(23, P_PWM_TRIANGLE | P_OE, ...
    _clkfreq / TARGET_FREQ / 2, _clkfreq / TARGET_FREQ / 4)
```
:::

**Key Differences to Remember:**

- **TRANSITION**: Simplest, just counts and toggles
- **NCO_FREQ**: Best frequency resolution, fixed 50% duty
- **NCO_DUTY**: Precise frequency + variable duty
- **PWM_SAWTOOTH**: Best for fast duty cycle changes
- **PWM_TRIANGLE**: Best for symmetric/phase-correct applications
- **PULSE**: Most flexible timing control
- **SMPS**: Only mode with feedback control

## Chapter 4: Measurement Modes - Precision Timing

Now let's explore modes that measure external signals - these are your oscilloscope, frequency counter, and logic analyzer all rolled into Smart Pins.

### Mode %01011 - Quadrature Encoder

This mode decodes quadrature encoder signals for position and rotation sensing. The Z register holds a 2's complement value representing the net total encoder counts in one direction minus counts in the opposite direction.

**When to Use:**

- Rotary encoder reading (motor feedback, user knobs)
- Linear encoder tracking (CNC machines, 3D printers)
- Motor position feedback (servo systems)
- Velocity measurement (periodic mode)

**How It Works:**

The Smart Pin monitors two input signals (A and B) that are $90^\circ$ out of phase, counting transitions to track position and direction.

```{=latex}
\QuadEncoderDiagram
```

The decoder watches both edges of both signals, providing $4\times$ resolution compared to single-edge counting:

**Register Configuration:**

| Register | Function |
|----------|----------|
| X[31:0] | Measurement period in clock cycles (0 = continuous mode) |
| Y | (not used) |
| Z[31:0] | Accumulated quadrature count (32-bit signed) |

**B Input Selection:**

The BBBB field in the mode control word selects the pin for the B signal. For example, to use P32 (A) and P33 (B), set BBBB = %0001, which selects P32+1 = P33.

**Two Operational Modes:**

**Continuous Mode (X = 0):**
The Z register continuously tracks the net quadrature count. Read the current position at any time with RDPIN or RQPIN. This mode works like a totalizer with no period boundaries.

**Periodic Mode (X $\neq$ 0):**
Quadrature steps are counted for X clock cycles. At the end of each period:

- The result is placed in Z
- IN is raised
- The accumulator is set to the 0/1/-1 value that would have been added

This design ensures no counts are lost across measurement boundaries. If a transition occurs exactly at the period boundary, it is added to the next period's count.

**$4\times$ Counting:**

A quadrature encoder produces four logic transitions per mechanical "click" of the shaft—two on the A input and two on the B input. The Smart Pin counts all four transitions. To obtain counts per click, use an arithmetic shift right by 2 bits:

::: pasm2
```
' Fragment - not standalone code
                sar       count, #2             ' Divide by 4, preserve sign
```
:::

**Position + Velocity Configuration:**

Configure both A and B pins to quadrature mode: one continuous (X=0) for absolute position tracking, the other periodic (X$\neq$0) for velocity measurement. Both pins track the same encoder but report different information.

**Zeroing the Count:**

Pulse DIR low at any time to reset the quadrature count to zero. No WXPIN is required—the Smart Pin reinitializes automatically.

**Reset Behavior:**

During reset (DIR=0):

- IN is LOW
- Z is set to the adder value (0/1/-1)

::: spin2
```
CON
  ENCODER_A = 32
  ENCODER_B = 33

PUB quadrature_demo() | position, last_pos
  ' Configure quadrature decoder
  ' BBBB field selects B pin offset from A pin
  pinstart(ENCODER_A, ...
    P_QUADRATURE | (ENCODER_B - ENCODER_A) << 24, 0, 0)

  last_pos := 0
  repeat
    position := rdpin(ENCODER_A) sar 2   ' Divide by 4 for clicks
    if position <> last_pos
      debug("Position: ", sdec(position))
      last_pos := position
```
:::

**PASM2 Quadrature - Periodic Mode:**

::: pasm2
```
' Quadrature encoder with periodic measurement
' Displays count on LEDs at P7:P0
' 25 MHz system clock, 2-second sample period
                org     0
                mov     dira, ##$FF             ' P7:P0 as LED outputs
                dirl    #32                     ' Reset Smart Pin at P32
                wrpin   quad_cfg, #32           ' Quadrature mode
                wxpin   x_period, #32           ' 2-second sample period
                dirh    #32                     ' Enable Smart Pin

.myloop         nop
.wait_here      testp   #32 wc                  ' Test IN flag at P32
                nop
        if_nc   jmp     #.wait_here             ' No flag? Keep waiting
                rqpin   quad_data, #32          ' Get accumulated count
                sar     quad_data, #2           ' Divide by 4 for clicks
                mov     outa, quad_data         ' Display on LEDs
                jmp     #.myloop                ' Repeat forever

' Quadrature mode: %0000_0001_000_00000_00000000_00_01011_0
'   BBBB=%0001 (P_PLUS1_B selects P33 as B input), Mode=%01011
quad_cfg        long    P_QUADRATURE | P_PLUS1_B
' 2-second period at 25 MHz = 50,000,000 clocks
x_period        long    $02FA_F080
quad_data       long    0
```
:::

**PASM2 Quadrature - Continuous Mode:**

::: pasm2
```
' Quadrature encoder with continuous (free-run) measurement
' Displays count on LEDs at P7:P0
                org     0
                mov     dira, ##$FF             ' P7:P0 as LED outputs
                dirl    #32                     ' Reset Smart Pin at P32
                wrpin   quad_cfg, #32           ' Quadrature mode
                wxpin   #0, #32                 ' X=0 for continuous
                dirh    #32                     ' Enable Smart Pin
                nop                             ' Brief settling delay

.myloop         nop
                rqpin   quad_data, #32          ' Get current count
                sar     quad_data, #2           ' Divide by 4 for clicks
                mov     outa, quad_data         ' Display on LEDs
                jmp     #.myloop                ' Repeat forever

' Quadrature mode: %0000_0001_000_00000_00000000_00_01011_0
'   BBBB=%0001 (P_PLUS1_B selects P33 as B input), Mode=%01011
quad_cfg        long    P_QUADRATURE | P_PLUS1_B
quad_data       long    0
```
:::

### Mode %01100 - Gated Positive-Edge Counter

Count rising edges on the A input, but only while the B input is HIGH. This mode provides hardware-gated counting without software intervention.

**When to Use:**

- Event counting with enable signal
- Frequency measurement with external gate
- RPM measurement with gate control
- Flow meter reading with validity signal

**Register Configuration:**

| Register | Function |
|----------|----------|
| X[31:0] | Measurement period in clock cycles (0 = continuous mode) |
| Y | (not used) |
| Z[31:0] | Accumulated count of A-rises while B is HIGH |

**B Input Gating:**

The count increments only on A-input positive edges that occur while the B input is at logic-1. When B is LOW, A-input edges are ignored. This provides hardware-level gating without software overhead.

**Two Operational Modes:**

**Continuous Mode (X = 0):**
The Z register continuously accumulates gated edge counts. Read the current count at any time with RDPIN or RQPIN.

**Periodic Mode (X $\neq$ 0):**
Gated edges are counted for X clock cycles. At the end of each period:

- The result is placed in Z
- IN is raised
- The accumulator preserves any edge that occurred at the boundary

No counts are lost across measurement boundaries.

**Reset Behavior:**

During reset (DIR=0):

- IN is LOW
- Z is set to the adder value (0/1)

**Note:** This mode does not debounce mechanical switch signals. For switches, add external RC filtering or use software debouncing.

::: spin2
```
CON
  COUNT_PIN = 32    ' A input - signal to count
  GATE_PIN = 33     ' B input - gate signal

PUB gated_counter() | count
  ' Configure gated edge counter
  ' BBBB field selects gate pin offset
  pinstart(COUNT_PIN, P_REG_UP | (GATE_PIN - COUNT_PIN) << 24, 0, 0)

  repeat
    waitms(1000)
    count := rdpin(COUNT_PIN)
    debug("Gated pulses/sec: ", udec(count))
```
:::

**PASM2 Gated Counter - Periodic Mode:**

::: pasm2
```
' Gated positive-edge counter
' Counts A-rises only when B is HIGH
' 25 MHz system clock, 1-second measurement period
                org     0
                mov     dira, ##$FF             ' P7:P0 as LED outputs
                dirl    #32                     ' Reset Smart Pin at P32
                wrpin   gated_cfg, #32          ' Gated counter mode
                wxpin   x_period, #32           ' 1-second period
                dirh    #32                     ' Enable Smart Pin

.loop           nop
.wait           testp   #32 wc                  ' Test IN flag
                nop
        if_nc   jmp     #.wait                  ' Wait for period end
                rdpin   count_data, #32         ' Get gated count
                mov     outa, count_data        ' Display on LEDs
                jmp     #.loop                  ' Repeat

' Gated counter mode: %0000_0001_000_00000_00000000_00_01100_0
'   BBBB=%0001 (P_PLUS1_B selects P33 as gate), Mode=%01100
gated_cfg       long    P_REG_UP | P_PLUS1_B
' 1-second period at 25 MHz = 25,000,000 clocks
x_period        long    $017D_7840
count_data      long    0
```
:::

### Mode %01101 - Positive-Edge Up/Down Counter

Count A-input positive edges with the B input controlling increment or decrement direction. This mode provides step/direction counting commonly used with stepper motor drivers.

**When to Use:**

- Step/direction motor feedback
- Up/down counters with edge triggering
- Manual pulse generators (MPG)
- Incremental position sensing

**Register Configuration:**

| Register | Function |
|----------|----------|
| X[31:0] | Measurement period in clock cycles (0 = continuous mode) |
| Y | (not used) |
| Z[31:0] | Net count (32-bit signed) |

**Direction Control:**

On each A-input positive edge:

- If B = HIGH (1): increment count
- If B = LOW (0): decrement count

The B input state may change at any time. The direction is sampled at each A-input edge.

**Two Operational Modes:**

**Continuous Mode (X = 0):**
The Z register continuously tracks the net count (increments minus decrements). Read the current value at any time with RDPIN or RQPIN.

**Periodic Mode (X $\neq$ 0):**
Edges are counted for X clock cycles. At the end of each period:

- The net result is placed in Z
- IN is raised
- The accumulator is set to +1/0/-1 for any edge at the boundary

No counts are lost across measurement boundaries.

**Reset Behavior:**

During reset (DIR=0):

- IN is LOW
- Z is set to the adder value (+1/0/-1)

**Note:** This mode does not debounce mechanical switch signals.

::: spin2
```
CON
  STEP_PIN = 32     ' A input - step pulses
  DIR_PIN = 33      ' B input - direction control

PUB step_dir_counter() | count
  ' Configure step/direction counter
  ' BBBB field selects direction pin offset
  pinstart(STEP_PIN, P_REG_UP_DOWN | (DIR_PIN - STEP_PIN) << 24, 0, 0)

  repeat
    count := rdpin(STEP_PIN)
    debug("Step count: ", sdec(count))
    waitms(100)
```
:::

**PASM2 Step/Direction Counter:**

::: pasm2
```
' Step/direction counter
' A-rises increment when B=1, decrement when B=0
' Continuous mode (X=0)
                org     0
                mov     dira, ##$FF             ' P7:P0 as LED outputs
                dirl    #32                     ' Reset Smart Pin at P32
                wrpin   updown_cfg, #32         ' Up/down mode
                wxpin   #0, #32                 ' X=0 for continuous
                dirh    #32                     ' Enable Smart Pin

.loop           nop
                rqpin   count_data, #32         ' Get current net count
                mov     outa, count_data        ' Display on LEDs
                jmp     #.loop                  ' Repeat

' Up/down mode: %0000_0001_000_00000_00000000_00_01101_0
'   BBBB=%0001 (P_PLUS1_B selects P33 as direction), Mode=%01101
updown_cfg      long    P_REG_UP_DOWN | P_PLUS1_B
count_data      long    0
```
:::

### Mode %01110 - Edge Counter / Dual-Edge Up/Down

This mode has two behaviors controlled by Y[0]:

- **Y[0] = 0**: Count A-input positive edges only
- **Y[0] = 1**: Increment on A-input positive edge, decrement on B-input positive edge

**When to Use:**

- Simple edge counting (Y[0]=0)
- Two-signal up/down counting (Y[0]=1)
- Separate increment/decrement inputs
- Bidirectional event counting

**How It Works:**

The Smart Pin counts rising edges on one or two inputs, incrementing or decrementing a counter based on which input triggers.

```{=latex}
\SinglePhaseEncoderDiagram
```

The counter accumulates edge events, with optional bidirectional counting when using two inputs:

**Register Configuration:**

| Register | Function |
|----------|----------|
| X[31:0] | Measurement period in clock cycles (0 = continuous mode) |
| Y[0] | Mode select: 0=count A-rises only, 1=A-rise increments/B-rise decrements |
| Z[31:0] | Accumulated count (32-bit signed when Y[0]=1) |

**Mode Y[0] = 0: Simple Edge Counter**

Counts positive edges on the A input only. The B input is ignored. This provides a basic pulse counter without gating.

**Mode Y[0] = 1: Dual-Edge Up/Down Counter**

- A-input positive edge: increment count
- B-input positive edge: decrement count

Both inputs operate independently—an A-rise and B-rise can occur in any order.

**Two Operational Modes:**

**Continuous Mode (X = 0):**
The Z register continuously tracks the count. Read the current value at any time with RDPIN or RQPIN.

**Periodic Mode (X $\neq$ 0):**
Events are counted for X clock cycles. At the end of each period:

- The result is placed in Z
- IN is raised
- The accumulator is set to 0/1/-1 for any edge at the boundary

No counts are lost across measurement boundaries.

**Reset Behavior:**

During reset (DIR=0):

- IN is LOW
- Z is set to the adder value (0/1/-1)

::: spin2
```
CON
  UP_PIN = 32       ' A input - increment signal
  DOWN_PIN = 33     ' B input - decrement signal

PUB dual_edge_counter() | count
  ' Configure dual-edge up/down counter
  ' Y[0]=1 enables increment/decrement mode
  pinstart(UP_PIN, P_COUNT_RISES | (DOWN_PIN - UP_PIN) << 24, 0, 1)

  repeat
    count := rdpin(UP_PIN)
    debug("Net count: ", sdec(count))
    waitms(100)
```
:::

**PASM2 Dual-Edge Counter:**

::: pasm2
```
' Dual-edge up/down counter
' A-rises increment, B-rises decrement
' Continuous mode (X=0)
                org     0
                mov     dira, ##$FF             ' P7:P0 as LED outputs
                dirl    #32                     ' Reset Smart Pin at P32
                wrpin   edge_cfg, #32           ' Edge counter mode
                wxpin   #0, #32                 ' X=0 for continuous
                wypin   #1, #32                 ' Y[0]=1 for up/down
                dirh    #32                     ' Enable Smart Pin

.loop           nop
                rqpin   count_data, #32         ' Get current net count
                mov     outa, count_data        ' Display on LEDs
                jmp     #.loop                  ' Repeat

' Edge counter mode: %0000_0001_000_00000_00000000_00_01110_0
'   BBBB=%0001 (P_PLUS1_B selects P33 as B input), Mode=%01110
edge_cfg        long    P_COUNT_RISES | P_PLUS1_B
count_data      long    0
```
:::

### Mode %01111 - Level Counter / Dual-Level Up/Down

This mode has two behaviors controlled by Y[0]:

- **Y[0] = 0**: Count clock cycles while A-input is HIGH
- **Y[0] = 1**: Increment while A-input is HIGH, decrement while B-input is HIGH

This mode counts based on input **levels** (HIGH state duration) rather than edges.

**When to Use:**

- Duty cycle measurement (Y[0]=0)
- High-time accumulation
- Bidirectional level-based counting (Y[0]=1)
- PWM input analysis

**How It Works:**

The Smart Pin counts clock cycles while an input is high, accumulating time rather than events.

```{=latex}
\ComparatorDiagram
```

The counter increments each clock cycle that the input remains high, providing precise duty cycle measurement:

**Register Configuration:**

| Register | Function |
|----------|----------|
| X[31:0] | Measurement period in clock cycles (0 = continuous mode) |
| Y[0] | Mode select: 0=count A-highs only, 1=A-high increments/B-high decrements |
| Z[31:0] | Accumulated count in clock cycles |

**Mode Y[0] = 0: Count A-Input Highs**

Counts system clock cycles while the A input is at logic-1. When A is LOW, the count stops but is not reset. This effectively measures the cumulative HIGH time of the input signal.

**Mode Y[0] = 1: Dual-Level Up/Down Counter**

- While A is HIGH: increment count each clock cycle
- While B is HIGH: decrement count each clock cycle

If both A and B are HIGH simultaneously, the increments and decrements cancel out (net zero change).

**Two Operational Modes:**

**Continuous Mode (X = 0):**
The Z register continuously tracks the accumulated high time. Read the current value at any time with RDPIN or RQPIN.

**Periodic Mode (X $\neq$ 0):**
High time is accumulated for X clock cycles. At the end of each period:

- The result is placed in Z
- IN is raised
- The accumulator is set to 0/1/-1 for counts at the boundary

No counts are lost across measurement boundaries.

**Reset Behavior:**

During reset (DIR=0):

- IN is LOW
- Z is set to the adder value (0/1/-1)

::: spin2
```
CON
  INPUT_PIN = 32

PUB duty_cycle_measure() | high_time, period_clks
  ' Measure duty cycle over 1 second
  period_clks := clkfreq          ' 1 second in clock cycles

  ' Y[0]=0 to count A-input high time only
  pinstart(INPUT_PIN, P_HIGH_TICKS, period_clks, 0)

  repeat
    repeat until testp(INPUT_PIN)   ' Wait for IN flag
    high_time := rdpin(INPUT_PIN)
    debug("High time: ", udec(high_time), " clocks")
    debug("Duty cycle: ", udec(high_time * 100 / period_clks), "%")
```
:::

**PASM2 Level Counter with SPI Output:**

::: pasm2
```
' Count A-input high time and transmit via SPI
' 25 MHz system clock, 1-second measurement period
                org     0
                dirl    #41                     ' Transmitter setup
                wrpin   sync_tx_mode, #41       ' Sync TX mode for P41
                wxpin   #%1_11111, #41          ' Stop/start, 32 bits
                dirh    #41                     ' Enable transmitter
                dirl    #40                     ' Clock output setup
                wrpin   clock_mode, #40         ' P40 transition mode
                wxpin   ##$1000, #40            ' Set base period
                dirh    #40                     ' Enable clock output

                dirl    #53                     ' Count A-input highs
                wrpin   a_in_mode, #53          ' Level counter mode
                wxpin   ##$17D_7840, #53        ' 1-sec period (25 MHz)
                wypin   #0, #53                 ' Y[0]=0: count highs
                dirh    #53                     ' Enable Smart Pin

.loop           nop
.wait           testp   #53 wc                  ' Get IN flag state
                nop
        if_nc   jmp     #.wait                  ' Wait for period end
                rdpin   count_data, #53         ' Get high-time count
                wypin   count_data, #41         ' Send via SPI
                wypin   #64, #40                ' Start SPI clock
                jmp     #.loop                  ' Repeat

' Level counter: %0000_0001_000_00000_00000000_00_01111_0
'   BBBB=%0001 (P_PLUS1_B), Mode=%01111
a_in_mode       long    P_COUNT_HIGHS | P_PLUS1_B
count_data      long    0
' Sync TX with inverted B from pin-1:
'   %0000_1111_000_00000_00000000_01_11100_0
'   BBBB=%1111 (P_INVERT_B | P_MINUS1_B), TT=%01, Mode=%11100
sync_tx_mode    long    P_SYNC_TX | P_OE | P_INVERT_B | P_MINUS1_B
' P_TRANSITION | P_OE = %0000_0000_000_00000_00000000_01_00101_0
clock_mode      long    P_TRANSITION | P_OE
```
:::

### Mode %10000 - Time A-Input States

This mode continuously measures the duration of both HIGH and LOW states on the A input. Each state change triggers a measurement.

**How It Works:**

When the A-input changes state, the Smart Pin:

1. Places the prior state (0 or 1) in the C-flag buffer
2. Places the prior state's duration count in Z
3. Raises IN

Use RQPIN to read both the duration and the C-flag without clearing IN. The C-flag indicates which state was measured (C=1 for HIGH period, C=0 for LOW period).

**Register Configuration:**

| Register | Function |
|----------|----------|
| X | (not used) |
| Y | (not used) |
| Z[31:0] | Duration of previous state in clock cycles (max $80000000) |

**Important Considerations:**

If states change faster than the cog can retrieve measurements, data will be lost as new measurements overwrite old ones. A workaround: use two Smart Pins to measure the same signal—one with inverted input. This allows capturing both states as long as the combined state durations allow time for retrieval.

**Reset Behavior:**

During reset (DIR=0):

- IN is LOW
- Z is set to $00000001

::: spin2
```
CON
  INPUT_PIN = 53

PUB state_timing() | duration, was_high
  pinstart(INPUT_PIN, P_TIME_STATES, 0, 0)

  repeat
    repeat until testp(INPUT_PIN)    ' Wait for state change
    duration := rdpin(INPUT_PIN) wc ' Get duration, C=prior state
    was_high := C
    if was_high
      debug("HIGH duration: ", udec(duration), " clocks")
    else
      debug("LOW duration: ", udec(duration), " clocks")
```
:::

**PASM2 State Timing:**

::: pasm2
```
' Time both HIGH and LOW states
' Saves measurements to separate variables
                org     0
                dirl    #53                     ' Reset Smart Pin
                wrpin   state_mode, #53         ' State timing mode
                dirh    #53                     ' Enable Smart Pin

.wait_high      nop
                rqpin   pin_data, #53 wc        ' Get C-flag (prior)
        if_nc   waitx   #200                    ' Delay if C=0
        if_nc   jmp     #.wait_high             ' Wait for HIGH
                mov     high_count, pin_data    ' Save HIGH duration

.wait_low       nop
                rqpin   pin_data, #53 wc        ' Get C-flag
        if_c    waitx   #200                    ' Delay if C=1
        if_c    jmp     #.wait_low              ' Wait for LOW
                mov     low_count, pin_data     ' Save LOW duration
                jmp     #.wait_high             ' Continue measuring

' State timing: %0000_0000_000_00010_00000000_00_10000_0
'   P[10]=%1 (Schmitt trigger A), Mode=%10000
state_mode      long    P_STATE_TICKS | P_SCHMITT_A
pin_data        long    0
high_count      long    0
low_count       long    0
```
:::

### Mode %10001 - Time A-Input Highs

This mode measures the duration of each HIGH state on the A input. When the input transitions from HIGH to LOW, the measurement is captured.

**How It Works:**

Clock cycles are counted while A-input is HIGH. Upon each HIGH-to-LOW transition:

1. The HIGH duration count is placed in Z
2. IN is raised

**Register Configuration:**

| Register | Function |
|----------|----------|
| X | (not used) |
| Y | (not used) |
| Z[31:0] | Duration of previous HIGH state in clock cycles (max $80000000) |

**Reset Behavior:**

During reset (DIR=0):

- IN is LOW
- Z is set to $00000001

::: spin2
```
CON
  INPUT_PIN = 53

PUB high_pulse_timing() | high_duration
  pinstart(INPUT_PIN, P_TIME_HIGHS, 0, 0)

  repeat
    repeat until testp(INPUT_PIN)      ' Wait for falling edge
    high_duration := rdpin(INPUT_PIN)
    debug("HIGH pulse: ", udec(high_duration), " clocks")
    debug("Duration: ", ...
      udec(high_duration * 1_000_000 / clkfreq), " us")
```
:::

::: pasm2
```
' Time HIGH pulses
                org     0
                dirl    #53                     ' Reset Smart Pin
                wrpin   high_mode, #53          ' HIGH timing mode
                dirh    #53                     ' Enable Smart Pin

.loop           nop
.wait           testp   #53 wc                  ' Check IN flag
        if_nc   jmp     #.wait                  ' Wait for measurement
                rdpin   high_time, #53          ' Get HIGH duration
                ' Process high_time...
                jmp     #.loop

' P_HIGH_TICKS = %0000_0000_000_00000_00000000_00_10001_0
high_mode       long    P_HIGH_TICKS
high_time       long    0
```
:::

### Mode %10010 - Event Timing and Timeout Detection

Mode %10010 (P_EVENTS_TICKS) provides dual functionality: timing a specified number of events, or detecting when events stop occurring (timeout/watchdog).

**How It Works:**

The Smart Pin counts clock cycles between events (for timing) or monitors for activity gaps (for timeout detection).

```{=latex}
\PeriodMeasurementDiagram
```

```{=latex}
\ContinuousPeriodDiagram
```

The mode can measure precise event timing or trigger an alert when expected events stop occurring:

**Two Operating Modes (controlled by Y[2]):**

| Y[2] | Mode | Function |
|------|------|----------|
| 0 | Event Timing | Measures time for X events to occur |
| 1 | Timeout Detection | Triggers after X clocks without an event |

**Event Types (Y[1:0]):**

| Y[1:0] | Event Type |
|--------|------------|
| %00 | A-input high |
| %01 | A-input rise |
| %1x | A-input edge (rise or fall) |

::: spin2
```
CON
  _clkfreq = 200_000_000
  FREQ_PIN = 53

PUB frequency_measurement() | period, frequency
  ' Time 100 rising edges for frequency measurement
  pinstart(FREQ_PIN, P_EVENTS_TICKS, 100, %001)

  repeat
    repeat until testp(FREQ_PIN)            ' Wait for measurement
    period := rdpin(FREQ_PIN) & $7FFFFFFF  ' Clock count for 100 edges

    frequency := (_clkfreq * 100) / period
    debug("Frequency: ", udec(frequency), " Hz")

PUB watchdog_timeout() | elapsed
  ' Configure as watchdog: trigger if no edge for 100ms
  pinstart(FREQ_PIN, P_EVENTS_TICKS, _clkfreq / 10, %101)

  repeat
    if testp(FREQ_PIN)
      elapsed := rdpin(FREQ_PIN)           ' Clocks since last edge
      debug("TIMEOUT - no activity for ", udec(elapsed), " clocks")
      handle_communication_loss()
```
:::

::: pasm2
```
' Timeout watchdog for communication monitoring
        dirl    #FREQ_PIN
        wrpin   ##P_EVENTS_TICKS, #FREQ_PIN
        wxpin   ##clkfreq/10, #FREQ_PIN    ' 100ms timeout threshold
        wypin   #%101, #FREQ_PIN           ' Timeout mode, edge events
        dirh    #FREQ_PIN
.loop
        testp   #FREQ_PIN wc               ' Check for timeout
  if_c  call    #handle_timeout
        jmp     #.loop

handle_timeout
        rdpin   elapsed, #FREQ_PIN         ' Get clocks since last edge
        ' Handle communication loss...
        ret
```
:::

### Mode %10011 - Period Time Accumulator

Mode %10011 (P_PERIODS_TICKS) measures total time over X complete periods, enabling precise average period/frequency measurement.

**How It Works:**

The Smart Pin accumulates clock cycles from one event type to another over multiple periods, providing averaged measurements that reduce noise.

```{=latex}
\TimeoutWatchdogDiagram
```

Each period is defined by events on A-input and B-input. The mode accumulates clock cycles from A-event to B-event over X repetitions:

```{=latex}
\DualInputTimeDiagram
```

**Period Definition (Y[1:0]):**

| Y[1:0] | A Event | B Event |
|--------|---------|---------|
| %00 | Rise | Rise |
| %01 | Rise | Edge |
| %10 | Edge | Rise |
| %11 | Edge | Edge |

::: spin2
```
CON
  _clkfreq = 200_000_000
  SIGNAL_PIN = 53

PUB average_period_measurement() | total_time, avg_period, frequency
  ' Configure for 10 period measurement (A and B on same pin)
  pinstart(SIGNAL_PIN, P_PERIODS_TICKS | P_LOCAL_B, 10, %00)

  repeat
    repeat until testp(SIGNAL_PIN)          ' Wait for 10 periods
    total_time := rdpin(SIGNAL_PIN)

    avg_period := total_time / 10
    frequency := _clkfreq / avg_period
    debug("Average period: ", udec(avg_period), " clocks")
    debug("Frequency: ", udec(frequency), " Hz")

PUB phase_delay_measurement(pin_a, pin_b) | phase_clocks, phase_degrees
  ' Measure phase delay between two signals
  ' A-input from pin_a, B-input from adjacent pin
  pinstart(pin_a, P_PERIODS_TICKS | P_PLUS1_B, 1, %00)

  repeat until testp(pin_a)
  phase_clocks := rdpin(pin_a)

  ' Convert to degrees (assuming 360 degrees = one signal period)
  phase_degrees := (phase_clocks * 360) / signal_period
  debug("Phase delay: ", udec(phase_degrees), " degrees")
```
:::

::: pasm2
```
' Average frequency measurement over 10 periods
        dirl    #SIGNAL_PIN
        wrpin   ##P_PERIODS_TICKS | P_LOCAL_B, #SIGNAL_PIN
        wxpin   #10, #SIGNAL_PIN           ' 10 periods
        wypin   #%00, #SIGNAL_PIN          ' Rise to rise
        dirh    #SIGNAL_PIN
.loop
        testp   #SIGNAL_PIN wc
  if_nc jmp     #.loop
        rdpin   total_time, #SIGNAL_PIN    ' Total clocks for 10 periods

        ' Calculate average: divide by 10
        mov     avg_period, total_time
        qdiv    avg_period, #10
        getqx   avg_period
        jmp     #.loop
```
:::

### Modes %10011-%10111 - Period-Based Measurement

These modes measure periods defined by A-input and B-input events. They provide oversampled measurements for precise frequency and duty cycle determination.

**Period Definition (Y[1:0] for all modes):**

| Y[1:0] | Period Start | Period End |
|--------|--------------|------------|
| %00 | A-input rise | B-input rise |
| %01 | A-input rise | B-input edge |
| %10 | A-input edge | B-input rise |
| %11 | A-input edge | B-input edge |

**Note:** The B-input can be set to the same pin as the A-input for single-pin cycle measurement.

**Mode %10011: For X periods, count time**

Accumulates clock cycles from A-event to B-event over X periods. Result is total time for X complete periods.

**Mode %10100: For X periods, count states**

Counts A-input trigger states (high time) within each A-to-B period over X periods. Result is cumulative duty measurement.

**Mode %10101: For periods in X+ clocks, count time**

Measures time until X clock cycles elapse, then completes any period in progress. Result is total time for however many complete periods fit within X+ clocks.

**Mode %10110: For periods in X+ clocks, count states**

Counts A-input states until X clock cycles elapse, then completes any period in progress. Result is cumulative duty for periods within X+ clocks.

**Mode %10111: For periods in X+ clocks, count periods**

Counts complete periods until X clock cycles elapse. Result is the number of complete periods.

**Reset Behavior (all modes):**

During reset (DIR=0):

- IN is LOW
- Z is set to $00000000

**Precision Frequency/Duty Measurement:**

Combining multiple measurements provides very precise frequency and duty cycle calculations. For example:

- Use %10101 to get total time for N periods
- Use %10110 to get total high-time for N periods
- Use %10111 to get exact period count

Then: `frequency = period_count * clkfreq / total_time` and `duty = (high_time * 100) / total_time`

::: spin2
```
CON
  SIGNAL_PIN = 53

PUB precision_frequency() | total_time, period_count, frequency
  ' Run two measurements concurrently for precise frequency

  ' Mode %10101: measure time for periods in 100ms+ window
  pinstart(SIGNAL_PIN, P_PERIODS_TIME | P_LOCAL_B, clkfreq/10, %00)

  repeat until testp(SIGNAL_PIN)
  total_time := rdpin(SIGNAL_PIN)

  ' Mode %10111: count periods in 100ms+ window
  pinstart(SIGNAL_PIN, P_PERIODS_COUNT | P_LOCAL_B, clkfreq/10, %00)

  repeat until testp(SIGNAL_PIN)
  period_count := rdpin(SIGNAL_PIN)

  ' Calculate precise frequency
  frequency := (period_count * clkfreq) / total_time
  debug("Periods: ", udec(period_count))
  debug("Total time: ", udec(total_time), " clocks")
  debug("Frequency: ", udec(frequency), " Hz")
```
:::

### Modes %11000-%11010 - ADC Modes

The P2's Smart Pins include sophisticated ADC capabilities for analog measurements using delta-sigma conversion.

**How It Works:**

The ADC uses delta-sigma modulation with digital filtering to convert analog voltages to digital values with configurable resolution and sample rate.

```{=latex}
\ADCSampleHoldDiagram
```

Three ADC modes provide different clocking and triggering options:

**Mode %11000**: ADC Sample/Filter with Internal Clock
**Mode %11001**: ADC Sample/Filter with External Clock
**Mode %11010**: ADC Scope with Trigger

**X Register Configuration:**

WXPIN sets the mode (X[5:4]) and sample period (X[3:0]):

| X[5:4] | Mode | Description |
|--------|------|-------------|
| %00 | SINC2 Sampling | Complete conversion, power-of-2 periods only |
| %01 | SINC2 Filtering | Requires software differencing |
| %10 | SINC3 Filtering | Better dynamic response |
| %11 | Bitstream Capture | Raw ADC bits (LSB = oldest) |

**Sample Period and Resolution:**

| X[3:0] | Period | SINC2 Sample | SINC2 Filter | SINC3 Filter |
|--------|--------|--------------|--------------|--------------|
| %0000 | 1 clk | impractical | impractical | impractical |
| %0011 | 8 clks | 4 bits | 4 ENOB | impractical |
| %0100 | 16 clks | 5 bits | 5 ENOB | 8 ENOB |
| %0101 | 32 clks | 6 bits | 6 ENOB | 10 ENOB |
| %0110 | 64 clks | 7 bits | 7 ENOB | 12 ENOB |
| %0111 | 128 clks | 8 bits | 8 ENOB | 14 ENOB |
| %1000 | 256 clks | 9 bits | 9 ENOB | 16 ENOB |
| %1001 | 512 clks | 10 bits | 10 ENOB | 18 ENOB |
| %1011 | 2048 clks | 12 bits | 12 ENOB | overflow |
| %1101 | 8192 clks | 14 bits | 14 ENOB | overflow |

*ENOB = Effective Number of Bits*

**SINC2 vs SINC3 Filtering:**

**SINC2 Filtering:** Uses double integration—sums input bits into an accumulator which feeds a second accumulator. Provides an extra bit of resolution over simple bit-summing and filters rectangular-sampling-window effects. Best for DC measurements where precision matters. Practical 14-bit resolution at 8192 clock periods. Filter becomes accurate on the second sample period.

**SINC3 Filtering:** Adds a third level of accumulation for better dynamic response. Doubles the ENOB for fast-changing signals but only slightly better than SINC2 for DC. Limited to 512 samples/period due to 27-bit accumulator constraints. Filter becomes accurate on the third sample period.

**Custom Sample Periods:**

For modes other than SINC2 Sampling (X[5:4] > %00), use WYPIN to set an arbitrary period in Y[13:0]. Maximum periods: SINC3 = 512 clocks, SINC2 = 11,585 clocks.

**27-bit Accumulator Handling (PASM2):**

The accumulators are 27 bits wide. For correct 32-bit math, either prescale or post-trim:

::: pasm2
```
' Fragment - not standalone code
' Prescale method:
                rdpin     x, #adcpin            ' Get SINC2 accumulator
                shl       x, #5                 ' Prescale 27-bit to 32-bit
                sub       x, diff               ' Compute sample
                add       diff, x               ' Update diff value

' Post-trim method:
                rdpin     x, #adcpin            ' Get SINC2 accumulator
                sub       x, diff               ' Compute sample
                add       diff, x               ' Update diff value
                zerox     x, #26                ' Trim to 27-bit
```
:::

::: spin2
```
PUB adc_reading(pin) : value
  ' Configure for ADC input with internal clock
  ' P[12:10] = %100 enables ADC mode
  pinstart(pin, P_ADC | P_ADC_1X | P_ADC_GND, 0, 0)

  waitms(1)                    ' Let SINC filter settle
  value := rdpin(pin)          ' Read ADC value

PUB adc_8bit_fast(pin) : value
  ' Fast 8-bit ADC using SINC2 sampling at 128 clocks
  pinstart(pin, P_ADC | P_ADC_1X, %00_0111, 0)

  repeat until testp(pin)       ' Wait for sample
  value := rdpin(pin)

PUB adc_14bit_precision(pin) : value
  ' High precision 14-bit ADC using SINC2 at 8192 clocks
  pinstart(pin, P_ADC | P_ADC_1X, %00_1101, 0)

  repeat until testp(pin)       ' Wait for sample (~41us at 200MHz)
  value := rdpin(pin)

PUB continuous_adc() | voltage
  ' Continuous ADC with SINC2 filtering
  pinstart(ADC_PIN, P_ADC | P_ADC_1X | P_ADC_GND, %00_0111, 0)

  repeat
    repeat until testp(ADC_PIN)
    voltage := rdpin(ADC_PIN)
    ' Convert to millivolts (assuming 3.3V reference, 8-bit)
    voltage := voltage * 3300 / 255
    debug("Voltage: ", udec(voltage), " mV")
```
:::

**PASM2 ADC Setup:**

::: pasm2
```
' Configure ADC with SINC2 sampling, 8-bit resolution
                wrpin   ##%100011_0000000_00_11000_0, #adcpin  ' ADC
                wxpin   #%00_0111, #adcpin                     ' SINC2
                dirh    #adcpin                                ' Enable

' Read samples continuously
.loop           testp   #adcpin wc              ' Check IN flag
        if_nc   jmp     #.loop                  ' Wait for sample
                rdpin   sample, #adcpin         ' Get ADC value
                ' Process sample...
                jmp     #.loop
```
:::

### Mode %11011 - USB Host/Device Mode

USB host/device mode provides low-level USB 1.1 physical layer support. This mode overrides OUT to control the pin output states. Full USB protocol implementation requires an additional software stack.

**How It Works:**

Two adjacent pins work together to handle the differential D+ and D- signals of the USB physical layer.

```{=latex}
\USBDifferentialDiagram
```

The Smart Pin handles USB signaling states (J, K, SE0, SE1) on the pin pair:

**Pin Pair Requirement:**

USB mode requires two adjacent pins configured together as an even/odd pair. Only the LSB of their pin numbers differs:

- Pins 0 and 1
- Pins 2 and 3
- Pins 4 and 5
- etc.

Both pins must be configured with identical WRPIN data of `%1_11011_0` (output enabled) or `%0_11011_0` (output disabled for "sniffer" mode).

**Sniffer Mode:**

Configure both pins with `%0_11011_0` to disable output drive, creating a USB bus observer that can monitor traffic without participating.

::: spin2
```
CON
  _clkfreq = 200_000_000
  USB_DM = 0                    ' D- on even pin
  USB_DP = 1                    ' D+ on odd pin

PUB usb_basic_setup()
  ' Configure USB pair with output enabled
  ' Both pins get identical configuration
  pinstart(USB_DM, P_USB_PAIR, 0, 0)
  pinstart(USB_DP, P_USB_PAIR, 0, 0)

  ' USB operation requires additional software stack
  ' See Parallax USB libraries for full implementation

PUB usb_sniffer_setup()
  ' Configure as USB sniffer (no output drive)
  ' Use mode without P_OE for receive-only operation
  pinfloat(USB_DM)
  pinfloat(USB_DP)
  wrpin(USB_DM, P_USB_PAIR)     ' Mode without output enable
  wrpin(USB_DP, P_USB_PAIR)
  pinh(USB_DM)                  ' Enable Smart Pin
  pinh(USB_DP)
```
:::

::: pasm2
```
' USB Host/Device mode - basic setup
' Requires even/odd pin pair (USB_DM=even, USB_DP=odd)
                org
                ' Configure USB pair with output enabled
                dirl    #USB_DM
                dirl    #USB_DP
                wrpin   usb_cfg, #USB_DM        ' D- configuration
                wrpin   usb_cfg, #USB_DP        ' D+ config (same)
                dirh    #USB_DM
                dirh    #USB_DP

                ' USB operation requires additional software stack
.loop           nop
                jmp     #.loop

' USB mode with output: TT=%01 (P_OE), Mode=%11011
usb_cfg         long    P_USB_PAIR
USB_DM          =       0                       ' D- on even pin
USB_DP          =       1                       ' D+ on odd pin
```
:::

### Mode %11100 - Synchronous Serial Transmit

Data from 1 to 32 bits shifts out synchronized with an external clock signal. This mode overrides OUT to control the pin output state. Bits shift out LSB first.

**How It Works:**

The Smart Pin shifts data out one bit per clock edge, synchronized to an external clock signal from the A-input.

**Falling Edge Clocking (data changes on rising, sampled on falling):**

```{=latex}
\SyncSerialFallingDiagram
```

**Rising Edge Clocking (data changes on falling, sampled on rising):**

```{=latex}
\SyncSerialRisingDiagram
```

The clock polarity determines when data transitions and when the receiver samples:

**X Register Configuration:**

| Field | Function |
|-------|----------|
| X[4:0] | Number of bits minus 1 (e.g., 7 for 8 bits) |
| X[5] | Mode: 0=continuous, 1=start-stop |

**Two Transmission Modes:**

**Continuous Mode (X[5]=0):**
During reset (DIR=0), WYPIN primes the shift register with the first data. After enabling (DIR=1), another WYPIN loads the buffer. When transmission completes, buffered data moves to the shifter automatically. The IN flag indicates buffer empty—load new data immediately to maintain continuous transmission.

**Start-Stop Mode (X[5]=1):**
Transmit data on demand. WYPIN can modify data before the first clock arrives. After transmission starts, WYPIN data is buffered for the next transmission.

**Double Buffering:**

WYPIN data always goes to the buffer first. During reset, data flows immediately through to the shifter. After transmission starts, buffer contents load into the shifter when the current transmission ends. IN flag signals buffer empty.

**MSB-First Transmission:**

Data shifts out LSB first by default. For MSB-first:

::: pasm2
```
' Fragment - not standalone code
                shl       data, #32-8           ' Shift 8-bit value into D[31:24]
                rev       data                  ' Reverse all bits
                ' Now LSB-first transmission sends MSB-first
```
:::

**Reset Behavior:**

During reset (DIR=0), output is held LOW. After enabling, output equals the LSB of the data written during reset.

::: spin2
```
CON
  CLK_PIN = 20
  TX_PIN = 21

PUB sync_tx_8bit(data)
  ' Transmit 8 bits, start-stop mode
  pinstart(TX_PIN, P_SYNC_TX | P_OE, %1_00111, data)

  ' Use separate transition mode pin for clock
  pinstart(CLK_PIN, P_TRANSITION | P_OE, $1000, 0)

  ' Trigger 16 clock edges (8 data bits * 2)
  wypin(CLK_PIN, 16)
```
:::

**PASM2 Sync TX - Positive Edge Clock:**

::: pasm2
```
' Synchronous serial transmit with external clock
' Positive-edge clocking (data sampled on rising edge)
                org     0
                dirl    #21                     ' Reset TX pin
                wrpin   sync_tx_mode, #21       ' Configure sync TX mode
                wxpin   #%1_00111, #21          ' Start-stop, 8 bits
                dirh    #21                     ' Enable TX

                dirl    #20                     ' Reset clock pin
                wrpin   clock_mode, #20         ' Transition output
                wxpin   ##$1000, #20            ' Set clock base period
                dirh    #20                     ' Enable clock

.loop           waitx   ##10_000_000            ' Delay between TX
                wypin   #$85, #21               ' Load $85 (%10000101)
                wypin   #16, #20                ' 16 clk edges (8 bits)
                jmp     #.loop

' Positive-edge clocking: %0000_1111_000_00000_00000000_01_11100_0
'   BBBB=%1111 (P_INVERT_B | P_MINUS1_B), TT=%01 (P_OE), Mode=%11100
sync_tx_mode    long    P_SYNC_TX | P_OE | P_INVERT_B | P_MINUS1_B
' P_TRANSITION | P_OE = %0000_0000_000_00000_00000000_01_00101_0
clock_mode      long    P_TRANSITION | P_OE
```
:::

### Mode %11101 - Synchronous Serial Receive

Receives 1 to 32 bits synchronized with an external clock. Data shifts in LSB first. Requires configuring both A (data) and B (clock) inputs.

**X Register Configuration:**

| Field | Function |
|-------|----------|
| X[4:0] | Number of bits minus 1 (e.g., 7 for 8 bits) |
| X[5] | Sample timing: 0=before B-edge, 1=coincident with B-edge |

**Sample Timing (X[5]):**

**X[5]=0 (Before B-edge):** Samples A input just before registering the B-input edge. Requires no hold time from sender. Use for most applications.

**X[5]=1 (Coincident):** Samples coincident with B-edge registration. Useful when transmitted data remains steady briefly after the clock edge. When receiving from another P2 Smart Pin in sync TX mode (which holds data for 2 clocks after B-edge), this enables fastest data transmission.

**Left-Justified Data:**

Received data is left-justified with MSB in bit 31. For 8-bit data, right-shift by 24:

::: pasm2
```
' Fragment - not standalone code
                shr       data, #24             ' Move 8-bit LSB to D[7:0]
```
:::

**MSB-First Reception:**

If sender transmits MSB-first, reverse and trim after receiving:

::: pasm2
```
' Fragment - not standalone code
                rev       data                  ' Reverse all 32 bits
                triml     data, #8              ' Keep only low 8 bits
```
:::

**IN Flag Behavior:**

When all required bits are received, IN is raised. Use RDPIN or RQPIN to retrieve the 32-bit left-justified data.

::: spin2
```
CON
  RX_PIN = 30
  CLK_PIN = 31

PUB sync_rx_8bit() : data
  ' Configure sync receive, clock from pin+1
  pinstart(RX_PIN, P_SYNC_RX | 1 << 24, %0_00111, 0)  ' BBBB=1 for CLK

  repeat until testp(RX_PIN)       ' Wait for reception complete
  data := rdpin(RX_PIN)
  data >>= 24                     ' Right-justify 8-bit value
```
:::

**PASM2 Sync RX - Complete Example:**

::: pasm2
```
' Synchronous serial receive
' Receives 8 bits, displays on LEDs at P7:P0
                org     0
                mov     dira, ##$00FF           ' P7:P0 as LED outputs

                dirl    #30                     ' Reset receiver
                wrpin   sync_rx_mode, #30       ' Configure sync RX mode
                wxpin   #%0_00111, #30          ' Pre-edge, 8 bits
                dirh    #30                     ' Enable receiver

.loop           testp   #30 wc                  ' Check IN flag
                nop
        if_nc   jmp     #.loop                  ' Wait for data

                rqpin   rcvd_data, #30          ' Get received data
                shr     rcvd_data, #24          ' Right-justify 8 bits
                mov     outa, rcvd_data         ' Display on LEDs
                jmp     #.loop

' Sync RX mode: %0000_0001_000_00000_00000000_01_11101_0
'   BBBB=%0001 (P_PLUS1_B = P31 clock), TT=%01, Mode=%11101
sync_rx_mode    long    P_SYNC_RX | P_OE | P_PLUS1_B
rcvd_data       long    0
```
:::

### Mode %11110 - Asynchronous Serial Transmit

Transmit 1 to 32 data bits at a programmable baud rate. Each transmission automatically includes a start bit (LOW) and stop bit (HIGH). This mode overrides OUT to control the pin output state.

**Frame Format:**

```{=latex}
\UARTFrameDiagram
```

**X Register Configuration:**

| Field | Function |
|-------|----------|
| X[4:0] | Number of data bits minus 1 (e.g., 7 for 8 bits) |
| X[15:10] | Fractional bit period (when X[31:26] = 0) |
| X[31:16] | Integer bit period in system clocks |

**Baud Rate Calculation:**

$$\text{clocks\_per\_bit} = \frac{\text{system\_clock\_frequency}}{\text{baud\_rate}}$$

For 200 MHz system clock at 115,200 baud:

$$\frac{200{,}000{,}000}{115{,}200} = 1736.1 \text{ clocks/bit}$$

**X Register Value:**

Method 1 (integer only): `(clocks_per_bit << 16) | (bits - 1)`

Method 2 (with fraction): `((clocks_per_bit * $10000) & $FFFFFC00) | (bits - 1)`

**Optional Parity:**

The hardware does not generate parity bits. To add parity, calculate it in software and insert at MSB+1 position. Include the parity bit in the bit count.

::: spin2
```
CON
  _clkfreq = 200_000_000
  TX_PIN = 56
  BAUD = 115_200

PUB async_tx_demo() | baud_val, i
  ' Calculate baud: (clocks_per_bit << 16) | (bits - 1)
  baud_val := (_clkfreq / BAUD) << 16 | 7     ' 8 data bits

  ' Configure async transmit with output enable
  pinstart(TX_PIN, P_ASYNC_TX | P_OE, baud_val, 0)

  ' Transmit test pattern
  repeat i from 0 to 255
    wypin(TX_PIN, i)                           ' Send byte
    repeat until testp(TX_PIN)                  ' Wait for buffer empty
    waitms(10)                                 ' Delay between bytes
```
:::

::: pasm2
```
' Asynchronous serial transmit
' 200 MHz system clock, 115200 baud, 8N1
                org
                dirl    #TX_PIN                 ' Reset TX pin
                wrpin   async_tx_mode, #TX_PIN  ' Async TX mode
                wxpin   baud_val, #TX_PIN       ' Baud and bit count
                dirh    #TX_PIN                 ' Enable TX

.loop           wypin   #$55, #TX_PIN           ' TX $55 (alt bits)
.wait           testp   #TX_PIN wc              ' Check IN (buf empty)
        if_nc   jmp     #.wait                  ' Wait for completion
                waitx   ##10_000_000            ' Delay between TX
                jmp     #.loop

' Async TX mode: TT=%01 (P_OE), Mode=%11110
async_tx_mode   long    P_ASYNC_TX | P_OE
' Baud: 200MHz/115200 = 1736 clocks, bits = 7 (8-1)
baud_val        long    $06C8_0007
TX_PIN          =       56
```
:::

### Mode %11111 - Asynchronous Serial Receive

Receive 1 to 32 data bits at a preset baud rate matching the transmitter. The Smart Pin automatically detects the start bit and samples data at the bit centers.

**X Register Configuration:**

| Field | Function |
|-------|----------|
| X[4:0] | Number of data bits minus 1 (e.g., 7 for 8 bits) |
| X[15:10] | Fractional bit period (when X[31:26] = 0) |
| X[31:16] | Integer bit period in system clocks |

**Reception Process:**

1. Smart Pin waits for start bit (HIGH-to-LOW transition)
2. Samples data bits at calculated bit centers
3. Raises IN flag when all bits received
4. RDPIN/RQPIN retrieves data (right-justified)

::: spin2
```
CON
  BAUD = 115_200

PUB uart_setup(tx_pin, rx_pin) | baud_val
  ' Calculate baud rate value
  baud_val := (clkfreq / BAUD) << 16 | 7    ' 8 bits (7+1)

  ' Configure TX with output enable
  pinstart(tx_pin, P_ASYNC_TX | P_OE, baud_val, 0)

  ' Configure RX
  pinstart(rx_pin, P_ASYNC_RX, baud_val, 0)

PUB uart_tx(pin, char)
  wypin(pin, char)
  repeat until testp(pin)   ' Wait for buffer empty

PUB uart_rx(pin) : char
  repeat until testp(pin)   ' Wait for byte received
  char := rdpin(pin) & $FF              ' Get byte, clear IN

PUB uart_rx_check(pin) : char, valid
  ' Non-blocking receive
  valid := testp(pin)
  if valid
    char := rdpin(pin) & $FF
```
:::

**PASM2 UART Receive:**

::: pasm2
```
' Asynchronous serial receive
' 200 MHz system clock, 115200 baud, 8N1
' Displays received byte on LEDs at P7:P0
                org     0
                mov     dira, ##$FF             ' P7:P0 as LED outputs

                dirl    #57                     ' Reset RX pin
                wrpin   async_rx_mode, #57      ' Async RX mode
                wxpin   baud_rx, #57            ' Set baud and bit count
                dirh    #57                     ' Enable RX

.loop           testp   #57 wc                  ' Check IN flag
        if_nc   jmp     #.loop                  ' Wait for byte
                rdpin   rx_data, #57            ' Get received byte
                mov     outa, rx_data           ' Display on LEDs
                jmp     #.loop

' Async RX mode: %0000_0000_000_00000_00000000_00_11111_0
'   TT=%00 (no output), Mode=%11111
async_rx_mode   long    P_ASYNC_RX
' Baud: 200MHz/115200 = 1736 clocks, bits = 7 (8-1)
baud_rx         long    $06C8_0007
rx_data         long    0
```
:::

**Full Duplex UART Example:**

::: spin2
```
CON
  TX_PIN = 56
  RX_PIN = 57
  BAUD = 115_200

VAR
  byte rx_buffer[64]
  byte rx_head, rx_tail

PUB start()
  ' Initialize UART
  pinstart(TX_PIN, P_ASYNC_TX | P_OE, (clkfreq / BAUD) << 16 | 7, 0)
  pinstart(RX_PIN, P_ASYNC_RX, (clkfreq / BAUD) << 16 | 7, 0)

PUB tx(char)
  wypin(TX_PIN, char)
  repeat until testp(TX_PIN)

PUB tx_str(str)
  repeat while byte[str]
    tx(byte[str++])

PUB rx() : char
  repeat until testp(RX_PIN)
  char := rdpin(RX_PIN) & $FF

PUB rx_check() : char, available
  available := testp(RX_PIN)
  if available
    char := rdpin(RX_PIN) & $FF
```
:::

## Chapter 5: Advanced Techniques

Now that we've covered all the modes, let's explore advanced techniques that combine modes and push Smart Pins to their limits.

### Polling vs Event-Driven Waiting

Every Smart Pin operation eventually completes and signals readiness through the IN flag. How you wait for that completion fundamentally affects your program's efficiency, power consumption, and responsiveness. The P2 offers two approaches: **polling** (actively checking) and **event-driven** (hardware-assisted sleeping).

#### The Polling Approach

Polling repeatedly checks the Smart Pin's IN flag until the operation completes. This is simple to implement and understand:

::: spin2
```
CON
  _clkfreq = 200_000_000
  UART_RX = 21
  BAUD = 115_200

PUB polling_receive() | byte_received
  ' Configure UART receive
  pinstart(UART_RX, P_ASYNC_RX, (_clkfreq / BAUD) << 16 | 8, 0)

  ' Polling approach - check repeatedly until data arrives
  repeat
    if pinread(UART_RX)              ' Check IN flag (bit 31)
      byte_received := rdpin(UART_RX)
      process_byte(byte_received)

PRI process_byte(b)
  debug("Received: ", uhex_byte(b))
```
:::

In PASM2, the polling loop uses the TESTP instruction:

::: pasm2
```
                org
                ' Configure UART receive Smart Pin
                dirl    #UART_RX
                wrpin   rx_mode, #UART_RX
                wxpin   bit_period, #UART_RX
                dirh    #UART_RX

                ' Polling loop - actively checks IN flag
.poll_loop      testp   #UART_RX wc              ' Test IN flag -> C
        if_nc   jmp     #.poll_loop              ' Not ready, keep poll
                rdpin   rx_data, #UART_RX        ' Read data (clears IN)
                call    #process_data
                jmp     #.poll_loop              ' Continue polling

rx_mode         long    P_ASYNC_RX
bit_period      long    (200_000_000 / 115_200) << 16 | 8
rx_data         long    0
```
:::

**Polling Characteristics:**

- **CPU Utilization**: 100% - the COG executes instructions continuously
- **Response Latency**: Very low - typically 2-8 clock cycles from event to response
- **Power**: Maximum consumption - COG never sleeps
- **Complexity**: Simple, easy to understand and debug
- **Best For**: Time-critical applications where immediate response is essential

#### The Event-Driven Approach (PASM2 Only)

Event-driven waiting uses the P2's hardware event system. The COG configures an event to trigger when the Smart Pin's IN flag rises, then sleeps until the event occurs.

**Important:** The event system instructions (`SETSE1..4`, `WAITSE1..4`, `POLLSE1..4`) are PASM2 instructions only. Spin2 does not provide built-in methods for these. To use event-driven waiting in a Spin2 program, you must use inline PASM2.

In PASM2:

::: pasm2
```
                org
                ' Configure UART receive Smart Pin
                dirl    #UART_RX
                wrpin   rx_mode, #UART_RX
                wxpin   bit_period, #UART_RX
                dirh    #UART_RX

                ' Event-driven loop - COG sleeps between events
.event_loop     setse1  #%001<<6 + UART_RX       ' Event on IN rise
                waitse1                           ' Sleep until ready
                rdpin   rx_data, #UART_RX        ' Read data (clears IN)
                call    #process_data
                jmp     #.event_loop             ' Setup next event

rx_mode         long    P_ASYNC_RX
bit_period      long    (200_000_000 / 115_200) << 16 | 8
rx_data         long    0
```
:::

**Event-Driven Characteristics:**

- **CPU Utilization**: 0% during wait - COG is suspended
- **Response Latency**: Zero clock cycles after event (instant wake)
- **Power**: Minimal during wait - COG is sleeping
- **Complexity**: Slightly more complex - requires event system knowledge
- **Best For**: Low-power applications, longer wait periods, concurrent operations

#### Event Source Configuration (PASM2)

The `SETSE1/2/3/4` instructions configure what triggers each of the four selectable events. For Smart Pin waiting, the most useful event source is the IN flag:

| Event Mode | Binary | Description |
|------------|--------|-------------|
| IN-rises | %001 | Smart Pin IN flag transitions from 0 to 1 (data ready) |
| IN-falls | %010 | Smart Pin IN flag transitions from 1 to 0 |
| IN-changes | %011 | Smart Pin IN flag changes state |

The event configuration format is: `#%MMM << 6 + pin_number`

::: pasm2
```
' Examples of event configuration
                setse1  #%001 << 6 + 10   ' Evt 1: P10 IN rises (ready)
                setse2  #%010 << 6 + 15   ' Event 2: Pin 15 IN falls
                setse3  #%011 << 6 + 20   ' Event 3: Pin 20 IN changes
```
:::

#### Comparison: When to Use Each Approach

| Aspect | Polling | Event-Driven |
|--------|---------|--------------|
| CPU during wait | 100% busy | 0% (sleeping) |
| Response time | 2-8 clocks | 0 clocks (instant) |
| Power consumption | Maximum | Minimum during wait |
| Code complexity | Simple | Moderate |
| Best for... | Multi-tasking loops, simple code | Lowest latency, power-sensitive |

**Use Event-Driven When:**

- Response latency is absolutely critical (hardware wake is instant - 0 clocks)
- Power consumption matters
- Wait times are longer (milliseconds or more)
- You want deterministic, minimal-latency response
- You want to coordinate multiple Smart Pin operations

**Use Polling When:**

- You need to do other work between checks (polling in a larger loop)
- You're monitoring multiple conditions that can't be combined into one event
- You need timeout handling or other conditional logic during the wait
- Wait times are very short and COG has nothing else to do anyway
- Simplicity is more important than efficiency

#### Multi-Source Monitoring in Spin2

Spin2 programs can monitor multiple Smart Pins by polling each one in a loop:

::: spin2
```
CON
  _clkfreq = 200_000_000
  UART_RX = 21
  ADC_PIN = 25
  ENCODER_PIN = 30

PUB multi_source_monitor() | uart_data, adc_value, encoder_count
  ' Configure multiple Smart Pins
  pinstart(UART_RX, P_ASYNC_RX, (_clkfreq / 115_200) << 16 | 8, 0)
  pinstart(ADC_PIN, P_ADC | P_ADC_1X, 0, 0)
  pinstart(ENCODER_PIN, P_QUADRATURE, 0, 0)

  repeat
    ' Poll each Smart Pin for data ready (IN flag high)
    if testp(UART_RX)
      uart_data := rdpin(UART_RX)
      handle_uart(uart_data)

    if testp(ADC_PIN)
      adc_value := rdpin(ADC_PIN)
      handle_adc(adc_value)

    if testp(ENCODER_PIN)
      encoder_count := rdpin(ENCODER_PIN)
      handle_encoder(encoder_count)
```
:::

This polling approach checks each Smart Pin's IN flag in sequence. For lower-latency multi-source monitoring, use PASM2 with the event system (`SETSE1..4`, `POLLSE1..4`).

#### ADC Sampling in Spin2

Continuous ADC sampling in Spin2 uses polling to wait for each sample:

::: spin2
```
CON
  _clkfreq = 200_000_000
  ADC_PIN = 25
  SAMPLE_COUNT = 1000

PUB adc_sampling() | samples[SAMPLE_COUNT], i, start_time, elapsed

  ' Configure ADC
  pinstart(ADC_PIN, P_ADC | P_ADC_1X, 0, 0)

  ' Polling approach - the only option in pure Spin2
  start_time := getct()
  repeat i from 0 to SAMPLE_COUNT - 1
    repeat until testp(ADC_PIN)        ' Wait for sample ready
    samples[i] := rdpin(ADC_PIN)
  elapsed := getct() - start_time

  debug("Collected ", udec(SAMPLE_COUNT), ...
    " samples in ", udec(elapsed), " clocks")
```
:::

For lower power consumption during waits, use PASM2 with the event system. The `WAITSE1` instruction suspends the COG until the Smart Pin's IN flag rises, reducing power draw compared to active polling.

#### Best Practices for Waiting

1. **Use RQPIN for Shared Access**: When multiple COGs monitor the same Smart Pin, use `rqpin()` (reads without clearing IN) so all COGs can see the data. Use `rdpin()` only when you're the sole consumer.

2. **Match Method to Wait Duration**: For Spin2, polling is the only option. For PASM2, use events (`WAITSE`) for waits longer than ~100 clocks to reduce power consumption.

3. **Consider Multi-COG Impact**: Polling ties up a COG completely. In multi-COG systems, dedicated PASM2 COGs using event-driven waiting make better use of system resources.

4. **In PASM2, Clear Before Configure**: The event flag may be set from a previous occurrence. `POLLSE` clears the flag when checking, or use `WAITSE` which auto-clears.

5. **Document Your Choice**: Comment why you chose polling vs events (PASM2) - future maintainers will thank you.

### Multi-Pin Synchronization

Starting multiple Smart Pins in perfect synchronization is crucial for many applications.

::: needs-diagram
Multi-pin sync showing:

- Configuration phase
- Simultaneous enable
- Synchronized outputs
:::

::: spin2
```
PUB sync_four_pwm() | mask
  mask := %1111 << BASE_PIN

  ' Configure all pins while disabled
  repeat pin from BASE_PIN to BASE_PIN + 3
    wrpin(pin, P_PWM_SAWTOOTH | P_OE)
    wxpin(pin, 10_000)         ' Same period
    wypin(pin, 2500 * (pin - BASE_PIN + 1))  ' Different duties

  ' Enable all simultaneously
  DIRH(mask)                   ' Perfect sync!

PUB phase_shifted_clocks() | phase
  ' Generate 4 clocks with 90-degree phase shifts
  repeat pin from 20 to 23
    phase := (pin - 20) * $4000_0000  ' 90-degree steps
    wrpin(pin, P_NCO_FREQ | P_OE)
    wxpin(pin, 1000 frac clkfreq)     ' Same frequency
    wypin(pin, phase)                  ' Different starting phase

  DIRH(%1111 << 20)            ' Start all together
```
:::

### Pin Input Routing

Smart Pins can monitor any other pin, enabling complex signal routing without external wiring.

::: needs-diagram
Pin routing diagram showing:

- Source pins
- Routing paths
- Destination Smart Pins
:::

::: spin2
```
PUB signal_distribution()
  ' Pin 10 generates reference clock
  pinstart(10, P_NCO_FREQ | P_OE, 1_000_000 frac clkfreq, 0)

  ' Pin 20 counts pulses from Pin 10
  pinstart(20, P_COUNT_RISES | 10 << 8, 0, 0)

  ' Pin 21 measures frequency of Pin 10
  pinstart(21, P_COUNT_CYCLES | 10 << 8, clkfreq, 0)

  ' Pin 22 measures period of Pin 10
  pinstart(22, P_MEASURE_PERIOD | 10 << 8, 0, 0)

  repeat
    debug("Count: ", udec(rdpin(20)))
    debug("Freq: ", udec(rdpin(21)), " Hz")
    debug("Period: ", udec(rdpin(22)), " clocks")
    waitms(1000)
```
:::

### Feedback Loops

Create closed-loop control systems using Smart Pins.

```{=latex}
\FeedbackLoopDiagram
```

::: spin2
```
PUB pwm_with_current_feedback() | current, duty
  ' PWM output on Pin 20
  pinstart(20, P_PWM_SAWTOOTH | P_OE, 10_000, 5_000)

  ' ADC input on Pin 21 (current sense)
  pinstart(21, P_ADC_1X | P_ADC_GND, 0, 0)

  ' Control loop
  TARGET_CURRENT := 2000       ' ADC counts
  duty := 5_000

  repeat
    current := rdpin(21)       ' Read actual current

    ' Adjust PWM based on error
    if current < TARGET_CURRENT
      duty := duty + 10 <# 9_999
    elseif current > TARGET_CURRENT
      duty := duty - 10 #> 0

    wypin(20, duty)            ' Update PWM
    waitms(10)                 ' Control loop rate
```
:::

### Precision Timing Networks

Build complex timing relationships using multiple Smart Pins.

```{=latex}
\ClockDistributionDiagram
```

::: spin2
```
CON
  _clkfreq = 200_000_000              ' System clock frequency
  US_001   = _clkfreq / 1_000_000     ' Clocks per microsecond

PUB timing_network()
  ' Master clock at 10MHz
  pinstart(MASTER_CLK, P_NCO_FREQ | P_OE, 10_000_000 frac clkfreq, 0)

  ' Divide by 10 (1MHz)
  pinstart(DIV10_CLK, P_COUNT_RISES | MASTER_CLK << 8, 0, 0)
  pinstart(DIV10_OUT, P_TRANSITION | P_OE, 0, 0)

  ' Create gating signals
  pinstart(GATE_1MS, P_PULSE | P_OE, ...
    (1_000 * US_001) << 16 | (9_000 * US_001), 0)

  ' Measurement windows
  pinstart(MEASURE_WIN, P_PULSE | P_OE, ...
    (100 * US_001) << 16 | (900 * US_001), 0)
```
:::

### Protocol Bridges

Use Smart Pins to translate between different protocols.

```{=latex}
\ProtocolBridgeDiagram
```

::: spin2
```
PUB uart_to_spi_bridge() | data
  ' UART receive
  pinstart(UART_RX, P_ASYNC_RX, (clkfreq / 115200) << 16 | 7, 0)

  ' SPI transmit (using sync serial)
  pinstart(SPI_CLK, P_TRANSITION | P_OE, 100, 0)  ' Clock
  pinstart(SPI_DATA, P_SYNC_TX | P_OE, 100 << 16 | 7, 0)

  repeat
    ' Wait for UART byte
    repeat until testp(UART_RX)
    data := rdpin(UART_RX) & $FF

    ' Send via SPI
    wypin(SPI_DATA, data)
    repeat until testp(SPI_DATA)
```
:::

### State Machines with Smart Pins

Build complex state machines using Smart Pin feedback.

```{=latex}
\StateMachineDiagram
```

::: spin2
```
PUB traffic_light_controller() | state, timer
  ' Red LED
  pinstart(RED_LED, P_TRANSITION | P_OE, 0, 0)

  ' Yellow LED
  pinstart(YEL_LED, P_TRANSITION | P_OE, 0, 0)

  ' Green LED
  pinstart(GRN_LED, P_TRANSITION | P_OE, 0, 0)

  ' Timer for state changes
  pinstart(TIMER_PIN, P_PULSE, 0, 0)

  state := "R"                 ' Start with red

  repeat
    case state
      "R":                     ' Red light
        pinh(RED_LED)
        pinl(YEL_LED)
        pinl(GRN_LED)
        wxpin(TIMER_PIN, 5 * clkfreq << 16 | 1)  ' 5 second timer
        wypin(TIMER_PIN, 1)
        repeat until testp(TIMER_PIN)
        state := "G"

      "G":                     ' Green light
        pinl(RED_LED)
        pinl(YEL_LED)
        pinh(GRN_LED)
        wxpin(TIMER_PIN, 4 * clkfreq << 16 | 1)  ' 4 second timer
        wypin(TIMER_PIN, 1)
        repeat until testp(TIMER_PIN)
        state := "Y"

      "Y":                     ' Yellow light
        pinl(RED_LED)
        pinh(YEL_LED)
        pinl(GRN_LED)
        wxpin(TIMER_PIN, 1 * clkfreq << 16 | 1)  ' 1 second timer
        wypin(TIMER_PIN, 1)
        repeat until testp(TIMER_PIN)
        state := "R"
```
:::

### High-Performance Smart Pin Patterns

When maximum throughput matters, these patterns eliminate bottlenecks and achieve peak Smart Pin performance.

#### Overlapped Operations

The most impactful optimization is overlapping operations - start the next operation while the current one completes. This eliminates dead time between operations:

::: spin2
```
CON
  _clkfreq = 200_000_000
  ADC_A = 20
  ADC_B = 21

PUB overlapped_adc_sampling() | sample_a, sample_b, buffer[1000], idx
  ' Configure two ADC pins
  pinstart(ADC_A, P_ADC | P_ADC_1X, 0, 0)
  pinstart(ADC_B, P_ADC | P_ADC_1X, 0, 0)

  ' NON-OVERLAPPED: Sequential sampling (slow)
  ' repeat idx from 0 to 999
  '   repeat until pinread(ADC_A)
  '   buffer[idx] := rdpin(ADC_A)    ' Wait, then read

  ' OVERLAPPED: Start B while waiting for A (fast)
  idx := 0
  repeat while idx < 1000
    ' While A is converting, process previous B result
    if pinread(ADC_A)
      sample_a := rdpin(ADC_A)
      buffer[idx++] := sample_a

    ' While B is converting, process previous A result
    if pinread(ADC_B)
      sample_b := rdpin(ADC_B)
      buffer[idx++] := sample_b
```
:::

In PASM2, overlapped operations achieve even higher throughput:

::: pasm2
```
                org
                ' Configure dual ADC
                dirl    #ADC_A
                wrpin   adc_mode, #ADC_A
                dirh    #ADC_A

                dirl    #ADC_B
                wrpin   adc_mode, #ADC_B
                dirh    #ADC_B

                mov     ptra, ##buffer

                ' Overlapped sampling loop
.sample_loop    testp   #ADC_A wc                ' Check A ready
        if_c    rdpin   temp, #ADC_A             ' Read A (non-blocking)
        if_c    wrlong  temp, ptra++             ' Store A result

                testp   #ADC_B wc                ' Check B ready
        if_c    rdpin   temp, #ADC_B             ' Read B (non-blocking)
        if_c    wrlong  temp, ptra++             ' Store B result

                cmp     ptra, ##buffer_end wc
        if_c    jmp     #.sample_loop

adc_mode        long    P_ADC | P_ADC_1X
temp            long    0
buffer          long    0[1000]
buffer_end
```
:::

#### Double-Buffering for Continuous Data Flow

Double-buffering uses two Smart Pins alternately, eliminating gaps between operations:

::: spin2
```
CON
  _clkfreq = 200_000_000
  TX_A = 20
  TX_B = 21
  BAUD = 921_600

PUB double_buffered_transmit(data_ptr, count) | ...
    bit_period, byte_val, idx
  bit_period := (_clkfreq / BAUD) << 16 | 8

  ' Configure two TX pins (external OR or separate wires)
  pinstart(TX_A, P_ASYNC_TX | P_OE, bit_period, 0)
  pinstart(TX_B, P_ASYNC_TX | P_OE, bit_period, 0)

  ' Prime the pump - start first byte on TX_A
  byte_val := byte[data_ptr++]
  wypin(TX_A, byte_val)
  idx := 1

  ' Alternating transmission - no gaps!
  repeat while idx < count
    ' While TX_A is sending, prepare TX_B
    byte_val := byte[data_ptr++]

    ' Wait for TX_A to finish, immediately start TX_B
    repeat until pinread(TX_A)
    wypin(TX_B, byte_val)
    idx++

    if idx >= count
      quit

    ' While TX_B is sending, prepare next for TX_A
    byte_val := byte[data_ptr++]

    ' Wait for TX_B to finish, immediately start TX_A
    repeat until pinread(TX_B)
    wypin(TX_A, byte_val)
    idx++

  ' Wait for final transmission
  repeat until pinread(TX_A) and pinread(TX_B)
```
:::

**Why Double-Buffering Helps:**

- Standard single-pin TX: `[SEND][wait][SEND][wait][SEND]...`
- Double-buffered: `[A:SEND][B:SEND][A:SEND][B:SEND]...`

The second approach achieves nearly 100% utilization when transmission time exceeds the time to prepare the next byte.

#### Multi-COG Smart Pin Coordination

When multiple COGs share Smart Pin access, careful coordination prevents data loss and race conditions:

::: spin2
```
CON
  _clkfreq = 200_000_000
  SHARED_ADC = 25

VAR
  long  adc_stack[50]
  long  latest_sample
  long  sample_count

PUB main() | local_sample
  ' COG 0: Configure ADC and spawn sampler
  pinstart(SHARED_ADC, P_ADC | P_ADC_1X, 0, 0)
  cogspin(NEWCOG, adc_sampler(), @adc_stack)

  ' COG 0: Consumer - uses RQPIN to read without clearing IN
  repeat
    ' RQPIN reads data WITHOUT clearing IN flag
    ' This allows the sampler COG to also see the data
    local_sample := rqpin(SHARED_ADC)
    process_sample(local_sample)
    waitms(10)

PUB adc_sampler() | sample
  ' COG 1: Producer - uses RDPIN which clears IN flag
  repeat
    repeat until pinread(SHARED_ADC)
    sample := rdpin(SHARED_ADC)        ' RDPIN clears IN
    latest_sample := sample            ' Update shared variable
    sample_count++
```
:::

**Multi-COG Access Rules:**

1. **Single Writer**: One COG should "own" the Smart Pin and use RDPIN
2. **Multiple Readers**: Other COGs use RQPIN (reads without clearing IN)
3. **Clear Ownership**: Document which COG is responsible for acknowledging

::: pasm2
```
                ' COG 0: Primary consumer (clears IN flag)
.read_primary   testp   #SHARED_PIN wc
        if_nc   jmp     #.read_primary
                rdpin   data, #SHARED_PIN        ' Read AND clear IN

                ' COG 1: Secondary observer (preserves IN flag)
.read_secondary rqpin   data, #SHARED_PIN        ' Read WITHOUT clearing
                ' Coordinate with primary for fresh data
```
:::

#### Pipelining Smart Pin Operations

For complex multi-stage processing, pipeline the operations so each stage processes while others wait:

::: spin2
```
CON
  _clkfreq = 200_000_000
  SENSOR_PIN = 20
  FILTER_PIN = 21
  OUTPUT_PIN = 22

PUB pipelined_processing() | raw, filtered, output
  ' Stage 1: Raw sensor input (ADC)
  pinstart(SENSOR_PIN, P_ADC | P_ADC_1X, 0, 0)

  ' Stage 2: Hardware filtering (using repository mode for temp storage)
  pinstart(FILTER_PIN, P_REPOSITORY, 0, 0)

  ' Stage 3: Processed output (DAC)
  pinstart(OUTPUT_PIN, P_DAC_DITHER_RND | P_DAC_124R_3V | P_OE, 0, 0)

  ' Pipeline: Each stage processes while others wait
  repeat
    ' All three operations overlap:
    ' - ADC is sampling NEXT value
    ' - Filter processes CURRENT value
    ' - DAC outputs PREVIOUS value

    if pinread(SENSOR_PIN)
      raw := rdpin(SENSOR_PIN)
      ' Start filter calculation immediately
      filtered := apply_filter(raw)

    ' Update output with filtered result
    wypin(OUTPUT_PIN, filtered)

PRI apply_filter(sample) : result
  ' Simple IIR filter example
  result := (sample + prev_sample * 3) / 4
  prev_sample := sample
```
:::

#### Timing-Critical Patterns

When jitter must be minimized, use these techniques:

::: spin2
```
CON
  _clkfreq = 200_000_000
  SAMPLE_PIN = 21

PUB low_jitter_sampling() | next_time, sample
  ' Configure ADC
  pinstart(SAMPLE_PIN, P_ADC | P_ADC_1X, 0, 0)

  ' Spin2 method: Synchronized to system counter
  ' This provides precise, predictable timing
  next_time := getct()
  repeat
    next_time += _clkfreq / 1000          ' 1ms intervals
    waitct(next_time)                      ' Precise timing
    repeat until testp(SAMPLE_PIN)          ' Ensure sample ready
    sample := rdpin(SAMPLE_PIN)            ' Read sample
    process_sample(sample)
```
:::

For absolute minimum jitter, use PASM2 with the event system. The `WAITSE` instruction provides zero-latency wake from sleep:

::: pasm2
```
                ' Minimum jitter pattern in PASM2
                ' Pre-calc all, then tight execution

                ' Setup: calculate all values before critical section
                mov     next_time, cnt
                add     next_time, interval

                ' Critical section: minimal instructions
.critical       waitcnt next_time, interval      ' Precise wait
                rdpin   sample, #ADC_PIN         ' Immediate read
                wrlong  sample, ptra++           ' Quick store
                jmp     #.critical               ' Tight loop
```
:::

#### Performance Anti-Patterns (What NOT to Do)

**Anti-Pattern 1: Unnecessary Re-configuration**

::: spin2
```
' BAD: Re-configuring on every iteration
repeat
  pinstart(ADC_PIN, P_ADC | P_ADC_1X, 0, 0)  ' Wasteful!
  sample := rdpin(ADC_PIN)

' GOOD: Configure once, read many times
pinstart(ADC_PIN, P_ADC | P_ADC_1X, 0, 0)
repeat
  repeat until pinread(ADC_PIN)
  sample := rdpin(ADC_PIN)
```
:::

**Anti-Pattern 2: Blocking Waits in Tight Loops**

::: spin2
```
' BAD: Blocking wait prevents other work
repeat
  repeat until pinread(PIN_A)    ' Stuck here!
  process_a(rdpin(PIN_A))
  repeat until pinread(PIN_B)    ' Then stuck here!
  process_b(rdpin(PIN_B))

' GOOD: Non-blocking checks allow interleaving
repeat
  if pinread(PIN_A)
    process_a(rdpin(PIN_A))
  if pinread(PIN_B)
    process_b(rdpin(PIN_B))
```
:::

**Anti-Pattern 3: Ignoring IN Flag Before Reading**

::: spin2
```
' BAD: Reading without checking IN flag
repeat 1000
  sample := rdpin(ADC_PIN)       ' May read stale data!
  waitms(1)

' GOOD: Always verify IN flag first
repeat 1000
  repeat until pinread(ADC_PIN)  ' Wait for fresh data
  sample := rdpin(ADC_PIN)
```
:::

#### Performance Metrics

| Pattern | Throughput Improvement | Complexity | Best Use Case |
|---------|----------------------|------------|---------------|
| Overlapped | 50-100% | Low | Multiple independent pins |
| Double-buffered | 80-95% | Medium | Continuous data streams |
| Multi-COG | Scales with COGs | High | Complex systems |
| Pipelined | 30-60% | Medium | Multi-stage processing |

### Task-Based I/O: Managing Multiple Smart Pins from One COG

So far we've discussed two approaches to managing multiple Smart Pins: polling loops within a single COG, and dedicating separate COGs to different I/O functions. But there's a third approach that sits between these extremes: **Spin2 tasks** --- lightweight threads that run cooperatively within a single COG.

Tasks let you structure your code as if you had multiple independent handlers, while consuming only one COG. This is particularly valuable when you have several low-to-medium bandwidth peripherals that don't justify dedicated COGs.

#### COGs vs Tasks: Choosing the Right Approach

The P2 provides 8 COGs and up to 32 tasks per COG. Understanding when to use each is crucial for efficient system design.

| Aspect | Dedicated COG | Spin2 Task |
|--------|---------------|------------|
| Execution | True parallel (simultaneous) | Time-sliced (cooperative) |
| Response latency | 0-2 clocks (hardware wake) | 20-40+ clocks (task switch) |
| Resource cost | Full COG + stack | Stack only (~64-128 longs) |
| Maximum count | 8 total | 32 per COG |
| Isolation | Complete (separate interpreter) | Shared (same COG context) |
| Best for | High-speed, time-critical | Multiple low-bandwidth |

**Use Dedicated COGs When:**

- Response time must be under 100 clock cycles
- Data rates exceed what task switching can handle
- Operations require sustained, uninterrupted processing
- You need true parallelism (simultaneous execution)

**Use Tasks When:**

- Managing multiple similar peripherals (several UARTs, sensors)
- Data rates are low enough to tolerate task-switching latency
- COGs are precious and you want to consolidate
- Peripherals naturally idle (waiting for data, conversion times)

#### The Task Switching Reality

Tasks use *cooperative multitasking* --- a task runs until it voluntarily yields control via `TASKNEXT()`, or until it blocks on a wait operation. The task switching overhead is approximately 20-40 clock cycles.

At 200 MHz, this means:

- **Task switch time**: ~100-200 nanoseconds
- **Maximum task switches per second**: ~5-10 million
- **Minimum guaranteed response**: Sum of all other tasks' execution time

This matters for Smart Pin I/O because while Task A is executing, Tasks B, C, and D are frozen. If a Smart Pin completes while its handler task is frozen, the data sits in the Z register until that task runs again.

::: spin2
```
CON
  _clkfreq = 200_000_000

VAR
  long  task1_stack[64]
  long  task2_stack[64]

PUB main()
  ' Start two tasks in addition to main
  taskspin(NEWTASK, sensor_handler(), @task1_stack)
  taskspin(NEWTASK, uart_handler(), @task2_stack)

  ' Main task continues with its own work
  repeat
    do_main_work()
    tasknext()                    ' Yield to other tasks

PUB sensor_handler()
  repeat
    if pinread(SENSOR_PIN)
      process_sensor(rdpin(SENSOR_PIN))
    tasknext()                    ' MUST yield or other tasks starve!

PUB uart_handler()
  repeat
    if pinread(UART_RX)
      process_uart(rdpin(UART_RX))
    tasknext()                    ' Cooperative yielding
```
:::

**Critical Rule**: Every task must call `TASKNEXT()` regularly. A task that enters a tight loop without yielding will starve all other tasks in that COG.

#### Practical Example: Four-Channel UART Manager

Here's a real-world example: managing four UART channels from a single COG using tasks. Each UART operates at 9600 baud --- far too slow to justify a dedicated COG, but fast enough to need prompt service.

::: spin2
```
CON
  _clkfreq = 200_000_000
  BAUD = 9600
  BIT_PERIOD = (_clkfreq / BAUD) << 16 | 8

  ' UART pins
  UART0_RX = 0
  UART1_RX = 2
  UART2_RX = 4
  UART3_RX = 6

VAR
  ' Per-channel receive buffers
  byte  rx_buffer[4][64]
  byte  rx_head[4], rx_tail[4]

  ' Task stacks
  long  uart_stack[4][48]

PUB main() | ch
  ' Configure all four UART Smart Pins
  repeat ch from 0 to 3
    pinstart(UART0_RX + ch * 2, P_ASYNC_RX, BIT_PERIOD, 0)

  ' Start a handler task for each channel
  taskspin(NEWTASK, uart_handler(0), @uart_stack[0])
  taskspin(NEWTASK, uart_handler(1), @uart_stack[1])
  taskspin(NEWTASK, uart_handler(2), @uart_stack[2])
  taskspin(NEWTASK, uart_handler(3), @uart_stack[3])

  ' Main task: process received data
  repeat
    repeat ch from 0 to 3
      if rx_head[ch] <> rx_tail[ch]
        process_byte(ch, get_byte(ch))
    tasknext()

PUB uart_handler(channel) | pin, b
  pin := UART0_RX + channel * 2

  repeat
    if pinread(pin)                 ' Check IN flag
      b := rdpin(pin) >> 24         ' Extract received byte
      put_byte(channel, b)          ' Buffer it
    tasknext()                      ' Yield to other handlers

PRI put_byte(ch, b) | next_head
  next_head := (rx_head[ch] + 1) & 63
  if next_head <> rx_tail[ch]       ' Buffer not full?
    rx_buffer[ch][rx_head[ch]] := b
    rx_head[ch] := next_head

PRI get_byte(ch) : b
  b := rx_buffer[ch][rx_tail[ch]]
  rx_tail[ch] := (rx_tail[ch] + 1) & 63
```
:::

**Why This Works at 9600 Baud:**

- Bit time at 9600 baud: ~104 microseconds
- Frame time (10 bits): ~1.04 milliseconds
- Task round-trip (4 tasks): ~400-800 nanoseconds worst case
- **Safety margin**: Over 1000x faster than needed

The Smart Pin buffers each complete byte in its Z register. As long as the handler task runs before the *next* byte arrives (1+ ms later), no data is lost.

#### When Tasks Fall Short

Tasks are unsuitable when the inter-arrival time of data approaches the task-switching overhead. Consider these scenarios:

**High-Speed Serial (1 Mbaud)**

Don't use tasks for high-speed serial! At 1 Mbaud:

- Bit time: 1 microsecond
- Byte time: ~10 microseconds (10 bits)
- Bytes per second: 100,000

With 4 tasks averaging 50 clocks each between yields:

- Round-trip: 200 clocks = 1 microsecond
- This is 10% of the byte time --- marginal!
- Any task taking longer causes data loss

**Solution:** Dedicate a COG to high-speed serial.

**Time-Critical Events**

Don't use tasks when timing is critical! If you need sub-microsecond response to a Smart Pin event, tasks cannot guarantee this. Other tasks may be executing when your event occurs.

*Example:* Pulse measurement where you must respond within 500ns of the IN flag rising.

**Solution:** Use event-driven wake (`WAITSE`) in a dedicated COG, or polling in an uninterrupted loop.

#### Task-Based vs Event-Driven: Latency Comparison

| Approach | Wake Latency | Best For |
|----------|--------------|----------|
| Event-driven (WAITSE) | 0 clocks | Single high-priority source |
| Polling loop | 2-8 clocks | Multiple sources, tight timing |
| Task-based | 20-40+ clocks | Multiple low-bandwidth sources |
| Multi-COG | 0 clocks each | Independent high-speed channels |

#### Advanced Task Patterns

**Pattern: Priority Through Frequency**

Give higher-priority channels more frequent service by calling their handlers more often:

::: spin2
```
PUB main()
  repeat
    high_priority_handler()       ' Check every iteration
    tasknext()
    high_priority_handler()       ' Check again
    medium_priority_handler()
    tasknext()
    high_priority_handler()       ' And again
    low_priority_handler()
    tasknext()
```
:::

**Pattern: Conditional Task Suspension**

Pause tasks that have nothing to do:

::: spin2
```
VAR
  long  uart_task_id[4]

PUB uart_handler(channel) | pin
  uart_task_id[channel] := taskid()
  pin := UART0_RX + channel * 2

  repeat
    if pinread(pin)
      process_byte(channel, rdpin(pin) >> 24)
    else
      taskhalt(THISTASK)          ' Suspend until woken
      ' Task resumes here when taskresume() called

PUB main_monitor() | ch
  repeat
    repeat ch from 0 to 3
      if pinread(UART0_RX + ch * 2)
        taskresume(uart_task_id[ch])  ' Wake the handler
    tasknext()
```
:::

**Pattern: Task Pools for Burst Handling**

Pre-create tasks that activate on demand:

::: spin2
```
VAR
  long  worker_stacks[4][48]
  long  work_queue[16]
  byte  queue_head, queue_tail

PUB main()
  ' Pre-start worker tasks (they immediately suspend)
  repeat i from 0 to 3
    taskspin(NEWTASK, worker(i), @worker_stacks[i])

  repeat
    if pinread(DATA_PIN)
      enqueue_work(rdpin(DATA_PIN))
      taskresume(find_idle_worker())
    tasknext()

PUB worker(id)
  repeat
    taskhalt(THISTASK)            ' Wait for work
    process(dequeue_work())        ' Do the work
```
:::

#### Task Method Summary

| Method | Purpose | Parameters |
|--------|---------|------------|
| `TASKSPIN(id, method(), @stack)` | Start new task | Task ID or NEWTASK, method to run, stack address |
| `TASKNEXT()` | Yield to next task | None |
| `TASKID()` | Get current task ID | None, returns 0-31 |
| `TASKCHK(id)` | Check if task running | Task ID, returns TRUE/FALSE |
| `TASKHALT(id)` | Pause a task | Task ID or THISTASK |
| `TASKRESUME(id)` | Resume paused task | Task ID |
| `TASKSTOP(id)` | Terminate task | Task ID or THISTASK |

#### Design Guidelines

1. **Budget your timing**: Calculate worst-case task round-trip time and ensure it's well under your fastest peripheral's inter-event time.

2. **Yield frequently**: Every task should yield at least once per logical operation. Long computations should yield periodically.

3. **Don't block in tasks**: Avoid `WAITMS()` or tight polling loops within tasks --- they freeze all other tasks.

4. **Size stacks appropriately**: Each task needs its own stack. Start with 48-64 longs and increase if you see crashes.

5. **Consider hybrid approaches**: Use tasks for slow peripherals, dedicated COGs for fast ones. One COG with 4 tasks + one dedicated COG often beats 5 separate COGs.

### IN Flag Management - RDPIN, RQPIN, and AKPIN

The IN flag is central to Smart Pin operation - it signals when an operation completes and data is ready. Understanding how to read this flag and manage its state is essential for correct Smart Pin usage.

#### The IN Flag Explained

Every Smart Pin maintains an IN flag (bit 31 of the pin's status). This flag:

- **Sets automatically** when the Smart Pin completes an operation (mode-dependent)
- **Signals data ready** - the Z register contains valid results
- **Must be cleared** before the next operation's completion can be detected
- **Is visible to all COGs** - any COG can check any pin's IN flag

Different modes set the IN flag under different conditions:

| Mode Category | IN Flag Set When |
|---------------|------------------|
| ADC modes | New sample ready |
| Serial RX | Byte/frame received |
| Serial TX | Transmission complete, ready for next |
| Measurement | Measurement complete |
| Pulse/Transition | Cycle complete |
| Counting | Count threshold reached |

#### The Three IN Flag Instructions

The P2 provides three distinct instructions for interacting with the IN flag:

**RDPIN - Read AND Acknowledge (Clear IN)**

::: spin2
```
value := rdpin(pin)
' Reads Z register AND clears IN flag atomically
' Most common - use when you're the sole consumer
```
:::

::: pasm2
```
                rdpin   result, #pin    ' Read Z register, clear IN flag
                                        ' C flag = previous IN state
```
:::

**RQPIN - Read WITHOUT Acknowledging (Preserve IN)**

::: spin2
```
value := rqpin(pin)
' Reads Z register but PRESERVES IN flag
' Use when multiple consumers need to see the same data
' Or when you're "peeking" without consuming
```
:::

::: pasm2
```
                rqpin   result, #pin    ' Read Z, IN unchanged
                                        ' C flag = current IN state
```
:::

**AKPIN - Acknowledge Only (Clear IN, Don't Read)**

::: spin2
```
akpin(pin)
' Clears IN flag without reading data
' Use when you only care that operation completed
' Or after using RQPIN and now want to acknowledge
```
:::

::: pasm2
```
                akpin   #pin            ' Clear IN flag, don't read Z
```
:::

#### When to Use Each Instruction

| Instruction | Reads Data | Clears IN | Use When |
|-------------|------------|-----------|----------|
| RDPIN | Yes | Yes | Single consumer, typical case |
| RQPIN | Yes | No | Multiple consumers, or peeking |
| AKPIN | No | Yes | Only care about completion, not data |

#### Single Consumer Pattern (Most Common)

When one COG exclusively uses a Smart Pin, RDPIN is the right choice:

::: spin2
```
CON
  _clkfreq = 200_000_000
  ADC_PIN = 25

PUB single_consumer() | sample
  pinstart(ADC_PIN, P_ADC | P_ADC_1X, 0, 0)

  repeat
    repeat until pinread(ADC_PIN)     ' Wait for IN flag
    sample := rdpin(ADC_PIN)          ' Read AND clear IN
    process(sample)
    ' IN is now clear, ready for next sample
```
:::

#### Multiple Consumer Pattern (Shared Access)

When multiple COGs need the same data, use RQPIN for observers and RDPIN or AKPIN for the primary consumer:

::: spin2
```
CON
  _clkfreq = 200_000_000
  SHARED_SENSOR = 25

VAR
  long  observer_stack[50]

PUB main() | sample
  ' COG 0: Primary consumer
  pinstart(SHARED_SENSOR, P_ADC | P_ADC_1X, 0, 0)
  cogspin(NEWCOG, observer_cog(), @observer_stack)

  repeat
    repeat until pinread(SHARED_SENSOR)
    sample := rdpin(SHARED_SENSOR)    ' Primary: Read AND clear
    primary_process(sample)

PUB observer_cog() | observed_value
  ' COG 1: Observer (doesn't clear IN)
  repeat
    ' Use RQPIN - reads without clearing IN
    observed_value := rqpin(SHARED_SENSOR)
    ' Note: Must coordinate with primary to know when value is fresh
    observe_process(observed_value)
    waitms(10)
```
:::

#### Completion-Only Pattern (No Data Needed)

When you only care that an operation completed, not about the result:

::: spin2
```
CON
  _clkfreq = 200_000_000
  TX_PIN = 20

PUB wait_for_transmission()
  ' Start a transmission
  wypin(TX_PIN, $55)

  ' Wait for completion - we don't need the data back
  repeat until pinread(TX_PIN)
  akpin(TX_PIN)                       ' Clear IN, don't read Z

  ' Or equivalently, read and discard:
  ' _ := rdpin(TX_PIN)
```
:::

#### Peek-Then-Consume Pattern

Sometimes you need to check data before deciding to consume it:

::: spin2
```
CON
  _clkfreq = 200_000_000
  UART_RX = 21

PUB peek_and_consume() | byte_val
  repeat
    repeat until pinread(UART_RX)

    ' Peek at data without consuming
    byte_val := rqpin(UART_RX)

    if byte_val == $1B                ' Escape character
      akpin(UART_RX)                  ' Acknowledge but don't process
      handle_escape()
    else
      byte_val := rdpin(UART_RX)      ' Now consume normally
      process_byte(byte_val)
```
:::

#### Multi-COG Coordination Patterns

**Pattern 1: One Producer, Multiple Consumers**

::: spin2
```
' Producer COG (owns the Smart Pin)
PUB producer()
  repeat
    repeat until pinread(SENSOR_PIN)
    latest_value := rdpin(SENSOR_PIN) ' Clear IN after reading
    data_ready := true                 ' Signal consumers

' Consumer COGs (observe only)
PUB consumer()
  repeat
    if data_ready
      my_copy := rqpin(SENSOR_PIN)    ' Read without clearing
      process(my_copy)
```
:::

**Pattern 2: Round-Robin Consumers**

::: spin2
```
VAR
  long  current_owner  ' Which COG should acknowledge

PUB cog_0_handler() | value
  repeat
    if current_owner == 0
      repeat until pinread(DATA_PIN)
      value := rdpin(DATA_PIN)        ' This COG acknowledges
      current_owner := 1               ' Pass to next COG
      process_0(value)
    else
      ' Not our turn - peek only
      value := rqpin(DATA_PIN)
      observe_0(value)

PUB cog_1_handler() | value
  repeat
    if current_owner == 1
      repeat until pinread(DATA_PIN)
      value := rdpin(DATA_PIN)        ' This COG acknowledges
      current_owner := 0               ' Pass back
      process_1(value)
    else
      value := rqpin(DATA_PIN)
      observe_1(value)
```
:::

#### PASM2 IN Flag Patterns

::: pasm2
```
                org

                ' Pattern: Wait for IN, read with acknowledge
.wait_read      testp   #pin wc                  ' Test IN -> C
        if_nc   jmp     #.wait_read              ' Loop until IN=1
                rdpin   data, #pin               ' Read and clear IN

                ' Pattern: Peek without consuming
.peek           rqpin   data, #pin wc            ' Read, keep IN, C=IN
        if_nc   jmp     #.no_data                ' No data if IN=0

                ' Pattern: Acknowledge without reading
.ack_only       testp   #pin wc
        if_c    akpin   #pin                     ' Clear IN if set

                ' Pattern: Check IN state in C flag
.check_in       rdpin   data, #pin wc            ' C = previous IN state
        if_c    call    #process_new_data        ' Had new data
        if_nc   call    #use_old_data            ' Reused old data
```
:::

#### Common Mistakes and Solutions

**Mistake 1: Reading Without Checking IN**

::: spin2
```
' WRONG: May read stale data
sample := rdpin(ADC_PIN)

' RIGHT: Always check IN first
repeat until pinread(ADC_PIN)
sample := rdpin(ADC_PIN)
```
:::

**Mistake 2: Using RDPIN When Multiple COGs Need Data**

::: spin2
```
' WRONG: First COG to read clears IN, others miss data
' COG 0:
sample := rdpin(SHARED_PIN)
' COG 1:
sample := rdpin(SHARED_PIN)  ' IN already cleared!

' RIGHT: One primary, others observe
' COG 0 (primary):
sample := rdpin(SHARED_PIN)
' COG 1 (observer):
sample := rqpin(SHARED_PIN)
```
:::

**Mistake 3: Forgetting to Clear IN**

::: spin2
```
' WRONG: IN stays set, masks next completion
repeat until pinread(TX_PIN)
wypin(TX_PIN, next_byte)      ' Started new TX, but IN still set!
repeat until pinread(TX_PIN)  ' Returns immediately (stale IN)!

' RIGHT: Clear IN before checking again
repeat until pinread(TX_PIN)
akpin(TX_PIN)                 ' OR: _ := rdpin(TX_PIN)
wypin(TX_PIN, next_byte)
repeat until pinread(TX_PIN)  ' Now waits for actual completion
```
:::

#### IN Flag Timing Considerations

The IN flag updates in real-time as the Smart Pin operates:

::: spin2
```
' The IN flag reflects the Smart Pin's current state
' It's NOT latched - if you don't read before the next
' operation completes, you may miss a completion

' For high-speed operations, ensure your read rate
' exceeds your Smart Pin operation rate:

pinstart(ADC_PIN, P_ADC | P_ADC_1X, 0, 0)

' If ADC completes every 1000 clocks, you must read
' faster than every 1000 clocks or risk missing samples
repeat
  ' This loop must complete in < 1000 clocks total
  repeat until pinread(ADC_PIN)
  sample := rdpin(ADC_PIN)
  ' Quick processing only!
```
:::

#### Quick Reference

| Need | Instruction | Notes |
|------|-------------|-------|
| Read data, I'm the only consumer | RDPIN | Clears IN automatically |
| Read data, others need it too | RQPIN | IN stays set for others |
| Just clear IN, don't need data | AKPIN | Fastest acknowledgment |
| Check if data ready | TESTP / pinread() | Doesn't affect IN flag |
| Peek at data, decide later | RQPIN + AKPIN | Two-step consume |

## Chapter 6: Multi-Pin Coordination

The true power of Smart Pins emerges when you coordinate multiple pins to create complex systems.

### Building a Complete Motor Controller

Let's combine multiple Smart Pin modes to create a sophisticated motor controller.

```{=latex}
\MotorControllerDiagram
```

::: spin2
```
OBJ
  motor : "motor_controller"

CON
  ' Motor A pins
  MOTOR_A_PWM = 20
  MOTOR_A_DIR = 21
  MOTOR_A_ENC_A = 22
  MOTOR_A_ENC_B = 23
  MOTOR_A_CURRENT = 24

PUB motor_controller_init()
  ' PWM output for speed
  pinstart(MOTOR_A_PWM, P_PWM_SAWTOOTH | P_OE, 10_000, 0)

  ' Direction control (normal I/O)
  pinl(MOTOR_A_DIR)

  ' Quadrature encoder for position
  pinstart(MOTOR_A_ENC_A, P_QUADRATURE | MOTOR_A_ENC_B << 8, 0, 0)

  ' ADC for current sensing
  pinstart(MOTOR_A_CURRENT, P_ADC_1X | P_ADC_GND, 0, 0)

PUB run_motor(speed, direction) | position, current
  ' Set direction
  if direction
    pinh(MOTOR_A_DIR)
  else
    pinl(MOTOR_A_DIR)

  ' Set speed (0-100%)
  wypin(MOTOR_A_PWM, speed * 100)

  ' Monitor operation
  repeat
    position := rdpin(MOTOR_A_ENC_A)
    current := rdpin(MOTOR_A_CURRENT)

    debug("Pos: ", sdec(position), " Current: ", udec(current))

    ' Overcurrent protection
    if current > MAX_CURRENT
      wypin(MOTOR_A_PWM, 0)    ' Stop motor
      debug("OVERCURRENT!")
      quit

    waitms(10)

PUB position_control(target_pos) | current_pos, error, output
  current_pos := rdpin(MOTOR_A_ENC_A)

  repeat while ||(target_pos - current_pos) > DEADBAND
    current_pos := rdpin(MOTOR_A_ENC_A)
    error := target_pos - current_pos

    ' Simple proportional control
    output := error * KP / 100
    output := output #> -100 <# 100  ' Limit to +/-100%

    ' Set direction and speed
    if output < 0
      pinl(MOTOR_A_DIR)
      wypin(MOTOR_A_PWM, -output * 100)
    else
      pinh(MOTOR_A_DIR)
      wypin(MOTOR_A_PWM, output * 100)

    waitms(10)

  ' Stop at position
  wypin(MOTOR_A_PWM, 0)
```
:::

### Creating a Data Acquisition System

Combine multiple ADC channels with timing and storage.

```{=latex}
\DataAcquisitionDiagram
```

::: spin2
```
CON
  NUM_CHANNELS = 8
  SAMPLE_RATE = 10_000          ' Hz
  BUFFER_SIZE = 1024

VAR
  long buffer[NUM_CHANNELS][BUFFER_SIZE]
  long buffer_index

PUB data_acquisition_init()
  ' Configure 8 ADC channels
  repeat chan from 0 to NUM_CHANNELS - 1
    pinstart(ADC_BASE + chan, P_ADC_1X | P_ADC_GND | P_ADC_SINC2, 0, 0)

  ' Configure sample timer
  pinstart(SAMPLE_TIMER, P_PULSE | P_OE, ...
    (clkfreq / SAMPLE_RATE) << 16 | 1, 0)

PUB acquire_data() | chan
  buffer_index := 0

  repeat BUFFER_SIZE
    ' Trigger sample timer
    wypin(SAMPLE_TIMER, 1)

    ' Read all channels
    repeat chan from 0 to NUM_CHANNELS - 1
      buffer[chan][buffer_index] := rdpin(ADC_BASE + chan)

    buffer_index++

    ' Wait for next sample time
    repeat until testp(SAMPLE_TIMER)

PUB process_data() | chan, sample, min, max, avg
  repeat chan from 0 to NUM_CHANNELS - 1
    min := posx
    max := negx
    avg := 0

    repeat sample from 0 to BUFFER_SIZE - 1
      min <?= buffer[chan][sample]
      max #>= buffer[chan][sample]
      avg += buffer[chan][sample]

    avg /= BUFFER_SIZE

    debug("CH", udec(chan), ": Min=", sdec(min), ...
      " Max=", sdec(max), " Avg=", sdec(avg))
```
:::

### Building a Communication Hub

Create a multi-protocol communication system.

```{=latex}
\CommunicationHubDiagram
```

::: spin2
```
OBJ
  comm : "comm_hub"

CON
  ' UART channels
  UART1_TX = 20
  UART1_RX = 21
  UART2_TX = 22
  UART2_RX = 23

  ' SPI interface
  SPI_CLK = 24
  SPI_MOSI = 25
  SPI_MISO = 26
  SPI_CS = 27

PUB comm_hub_init()
  ' UART Channel 1 (115200 baud)
  pinstart(UART1_TX, P_ASYNC_TX | P_OE, (clkfreq / 115200) << 16 | 7, 0)
  pinstart(UART1_RX, P_ASYNC_RX, (clkfreq / 115200) << 16 | 7, 0)

  ' UART Channel 2 (9600 baud)
  pinstart(UART2_TX, P_ASYNC_TX | P_OE, (clkfreq / 9600) << 16 | 7, 0)
  pinstart(UART2_RX, P_ASYNC_RX, (clkfreq / 9600) << 16 | 7, 0)

  ' SPI Master
  pinstart(SPI_CLK, P_TRANSITION | P_OE, 100, 0)
  pinstart(SPI_MOSI, P_SYNC_TX | P_OE, 100 << 16 | 7, 0)
  pinstart(SPI_MISO, P_SYNC_RX, 100 << 16 | 7, 0)
  pinl(SPI_CS)

PUB route_messages() | source, data
  repeat
    ' Check UART1
    if testp(UART1_RX)
      data := rdpin(UART1_RX) & $FF
      process_uart1_message(data)

    ' Check UART2
    if testp(UART2_RX)
      data := rdpin(UART2_RX) & $FF
      process_uart2_message(data)

    ' Check SPI
    if testp(SPI_MISO)
      data := rdpin(SPI_MISO) & $FF
      process_spi_message(data)

PRI process_uart1_message(data)
  ' Route to UART2
  wypin(UART2_TX, data)

PRI process_uart2_message(data)
  ' Route to SPI
  pinh(SPI_CS)
  wypin(SPI_MOSI, data)
  repeat until testp(SPI_MOSI)
  pinl(SPI_CS)

PRI process_spi_message(data)
  ' Route to UART1
  wypin(UART1_TX, data)
```
:::

### Synchronized Sampling System

Create a system where multiple inputs are sampled simultaneously.

```{=latex}
\SynchronizedSamplingDiagram
```

::: spin2
```
PUB synchronized_sampling() | trigger_time
  ' Configure multiple input channels
  repeat pin from INPUT_BASE to INPUT_BASE + 7
    pinstart(pin, P_COUNT_RISES, 0, 0)

  ' Take synchronized snapshot
  trigger_time := cnt

  ' Reset all counters simultaneously
  DIRL(MASK_8_PINS)
  DIRH(MASK_8_PINS)

  ' Let them count for exact period
  waitcnt(trigger_time + SAMPLE_PERIOD)

  ' Read all simultaneously (well, sequentially but fast)
  repeat pin from INPUT_BASE to INPUT_BASE + 7
    samples[pin - INPUT_BASE] := rdpin(pin)
```
:::

## Chapter 7: Troubleshooting and Optimization

Even experts encounter issues with Smart Pins. Here's how to diagnose and fix common problems.

### Common Configuration Errors


**Problem: Smart Pin doesn't respond**

::: spin2
```
PUB diagnose_smart_pin(pin)
  ' Check if pin is enabled
  if testp(pin)
    debug("Pin ", udec(pin), " is enabled")
  else
    debug("Pin ", udec(pin), " is DISABLED!")

  ' Check mode
  mode := 0  ' NOTE: Mode config cannot be read back from pin
  debug("Mode: %", ubin(mode))

  ' Try to read result
  result := rdpin(pin)
  debug("Z register: ", uhex(result))
```
:::

**Problem: Wrong timing/frequency**

::: spin2
```
PUB verify_frequency(pin, expected_hz) | measured
  ' Set up frequency counter on different pin
  pinstart(MEASURE_PIN, P_COUNT_CYCLES | pin << 8, clkfreq, 0)

  waitms(1000)
  measured := rdpin(MEASURE_PIN)

  debug("Expected: ", udec(expected_hz), " Hz")
  debug("Measured: ", udec(measured), " Hz")
  debug("Error: ", sdec(measured - expected_hz), " Hz")
```
:::

**Problem: No output signal**

::: spin2
```
PUB check_output_enable(pin)
  config := 0  ' NOTE: Pin config cannot be read back; track in software

  if config & P_OE
    debug("Output IS enabled")
  else
    debug("Output NOT enabled - add P_OE!")

  if config & P_DRIVE_MASK
    debug("Drive strength: ", uhex(config & P_DRIVE_MASK))
  else
    debug("Default drive strength")
```
:::

### Performance Optimization

The following optimizations can significantly improve Smart Pin throughput in time-critical applications.

**Minimize Pin Access Overhead**

Individual pin writes execute in ~2 clock cycles each, while masked operations update multiple pins in approximately the same time.

::: spin2
```
' Slow approach - multiple pin accesses (~16 clocks for 8 pins)
PUB slow_update()
  repeat i from 0 to 7
    wypin(BASE_PIN + i, values[i])

' Fast approach - use pin masks (~2 clocks total)
PUB fast_update()
  mask := $FF << BASE_PIN
  WYPIN(mask, packed_values)    ' Update 8 pins at once
```
:::

**Optimize Timing Precision**

::: spin2
```
PUB precise_timing() | start_time
  ' Compensate for instruction overhead
  start_time := cnt
  instruction_overhead := cnt - start_time

  ' Now adjust Smart Pin timing
  actual_period := desired_period - instruction_overhead
  wxpin(pin, actual_period)
```
:::

**Reduce Latency**

::: spin2
```
' Standard Spin2 approach - polling
PUB standard_receive() | data
  repeat
    if testp(pin)                  ' Check IN flag
      data := rdpin(pin)
      process(data)

' Tighter polling loop for lower latency
PUB tight_polling() | data
  repeat
    repeat until testp(pin)        ' Dedicated wait
    data := rdpin(pin)
    process(data)
```
:::

For absolute minimum latency, use PASM2 with the event system:

::: pasm2
```
                ' Zero-latency wake using events
                setse1  #%001 << 6 + pin      ' Event on IN rising
.loop           waitse1                        ' Sleep until event
                rdpin   data, #pin
                call    #process
                jmp     #.loop
```
:::

### Debugging Techniques

**Use Debug Smart Pin Monitor**

::: spin2
```
PUB smart_pin_monitor(pin)
  debug(`SCOPE_XY MyScope SIZE 256 SAMPLES 0 ...
    COLOR black green TRIGGER 128)

  repeat
    sample := rdpin(pin)
    debug(`MyScope `(sample))
    waitms(1)
```
:::

**Create Test Patterns**

::: spin2
```
PUB test_pattern_generator()
  ' Generate known test pattern
  repeat value from 0 to 255
    wypin(DAC_PIN, value << 8)
    waitms(10)

  ' Verify with ADC
  repeat value from 0 to 255
    expected := value << 8
    actual := rdpin(ADC_PIN) >> 8
    if ||(expected - actual) > TOLERANCE
      debug("ERROR at ", udec(value))
```
:::

**Logic Analyzer Mode**

::: spin2
```
PUB logic_analyzer()
  ' Configure 8 pins as digital inputs
  repeat pin from 0 to 7
    pinclear(pin)

  ' Capture samples
  repeat sample from 0 to BUFFER_SIZE - 1
    buffer[sample] := INA[7..0]
    waitcnt(cnt + SAMPLE_PERIOD)

  ' Display results
  repeat sample from 0 to BUFFER_SIZE - 1
    debug("", ubin(buffer[sample]))
```
:::

### Power Optimization


**Disable Unused Smart Pins**

::: spin2
```
PUB power_optimize()
  ' Disable all Smart Pins initially
  repeat pin from 0 to 63
    pinclear(pin)

  ' Only enable what's needed
  pinstart(NEEDED_PIN, mode, x, y)
```
:::

**Use Appropriate Modes**

::: spin2
```
' Power hungry - continuous ADC sampling
PUB continuous_adc()
  pinstart(ADC_PIN, P_ADC_1X, 0, 0)
  repeat
    value := rdpin(ADC_PIN)

' Power efficient - triggered ADC
PUB triggered_adc()
  pinstart(ADC_PIN, P_ADC_1X | P_ADC_TRIGGER, 0, 0)
  wypin(ADC_PIN, 1)             ' Trigger single conversion
  repeat until testp(ADC_PIN)
  value := rdpin(ADC_PIN)
  pinclear(ADC_PIN)             ' Disable until next reading
```
:::

## Chapter 8: Real-World Applications

Let's build complete, practical applications using Smart Pins.

### Digital Oscilloscope

```{=latex}
\OscilloscopeArchDiagram
```

::: spin2
```
CON
  SAMPLES = 1024
  ADC_PIN = 16
  TRIGGER_PIN = 17

VAR
  long waveform[SAMPLES]
  long trigger_level

PUB oscilloscope() | index, triggered
  ' Configure ADC input
  pinstart(ADC_PIN, P_ADC_1X | P_ADC_GND, 0, 0)

  ' Configure trigger comparator
  trigger_level := $8000        ' Mid-scale
  pinstart(TRIGGER_PIN, P_COMPARATOR | ADC_PIN << 8, 0, trigger_level)

  repeat
    ' Wait for trigger
    triggered := FALSE
    repeat until triggered
      if pinread(TRIGGER_PIN) ' Rising edge detected
        triggered := TRUE

    ' Capture waveform
    repeat index from 0 to SAMPLES - 1
      waveform[index] := rdpin(ADC_PIN)
      waitus(10)               ' 100kHz sample rate

    ' Display waveform
    display_waveform(@waveform, SAMPLES)

PRI display_waveform(buffer, count) | i, value
  debug(`SCOPE MyScope SIZE 256 256 SAMPLES 0 COLOR black green`)

  repeat i from 0 to count - 1
    value := long[buffer][i] >> 8  ' Scale to 8-bit for display
    debug(`MyScope `(value))
```
:::

### Frequency Generator with Display


::: spin2
```
OBJ
  lcd : "lcd_driver"

CON
  FREQ_OUT = 20
  MIN_FREQ = 1
  MAX_FREQ = 10_000_000

VAR
  long current_freq

PUB frequency_generator() | encoder_pos, last_pos
  ' Configure NCO for frequency output
  current_freq := 1000          ' Start at 1kHz
  update_frequency()

  ' Configure encoder for frequency adjustment
  pinstart(ENC_A, P_QUADRATURE | ENC_B << 8, 0, 0)

  last_pos := 0
  repeat
    encoder_pos := rdpin(ENC_A)

    if encoder_pos <> last_pos
      ' Adjust frequency based on encoder
      current_freq := current_freq * lookup(encoder_pos - last_pos)
      current_freq := current_freq #> MIN_FREQ <# MAX_FREQ

      update_frequency()
      display_frequency()

      last_pos := encoder_pos

PRI update_frequency()
  x := current_freq frac clkfreq
  wypin(FREQ_OUT, x)

PRI display_frequency()
  lcd.clear()
  lcd.str(string("Frequency: "))

  if current_freq => 1_000_000
    lcd.dec(current_freq / 1_000_000)
    lcd.str(string("."))
    lcd.dec((current_freq / 1000) // 1000)
    lcd.str(string(" MHz"))
  elseif current_freq => 1_000
    lcd.dec(current_freq / 1_000)
    lcd.str(string("."))
    lcd.dec(current_freq // 1000)
    lcd.str(string(" kHz"))
  else
    lcd.dec(current_freq)
    lcd.str(string(" Hz"))

PRI lookup(delta) : multiplier
  case delta
    -10...-5: multiplier := 0.1
    -4...-2:  multiplier := 0.5
    -1:       multiplier := 0.9
    0:        multiplier := 1.0
    1:        multiplier := 1.1
    2...4:    multiplier := 2.0
    5...10:   multiplier := 10.0
```
:::

### Complete Robot Controller

```{=latex}
\RobotSystemDiagram
```

::: spin2
```
OBJ
  motors : "motor_driver"
  sensors : "sensor_array"
  comm : "serial_comm"

CON
  ' Motor pins
  LEFT_PWM = 20
  LEFT_DIR = 21
  LEFT_ENC_A = 22
  LEFT_ENC_B = 23

  RIGHT_PWM = 24
  RIGHT_DIR = 25
  RIGHT_ENC_A = 26
  RIGHT_ENC_B = 27

  ' Sensor pins
  ULTRASONIC_TRIG = 30
  ULTRASONIC_ECHO = 31
  LINE_SENSORS = 32              ' Base pin for 5 sensors

PUB robot_controller()
  init_all_systems()

  repeat
    read_sensors()
    update_navigation()
    motor_control()
    communicate_status()
    waitms(10)                  ' 100Hz control loop

PRI init_all_systems()
  ' Initialize motors with Smart Pins
  init_motor(LEFT_PWM, LEFT_DIR, LEFT_ENC_A, LEFT_ENC_B)
  init_motor(RIGHT_PWM, RIGHT_DIR, RIGHT_ENC_A, RIGHT_ENC_B)

  ' Initialize sensors
  init_ultrasonic()
  init_line_sensors()

  ' Initialize communication
  comm.start(TX_PIN, RX_PIN, 115200)

PRI init_motor(pwm_pin, dir_pin, enc_a, enc_b)
  ' PWM for speed control
  pinstart(pwm_pin, P_PWM_SAWTOOTH | P_OE, 10_000, 0)

  ' Direction control
  pinl(dir_pin)

  ' Encoder feedback
  pinstart(enc_a, P_QUADRATURE | enc_b << 8, 0, 0)

PRI init_ultrasonic()
  ' Trigger output
  pinl(ULTRASONIC_TRIG)

  ' Echo measurement
  pinstart(ULTRASONIC_ECHO, P_MEASURE_HIGH, 0, 0)

PRI init_line_sensors()
  ' Configure 5 ADC channels for line sensors
  repeat i from 0 to 4
    pinstart(LINE_SENSORS + i, P_ADC_1X | P_ADC_GND, 0, 0)

PRI read_sensors() | i
  ' Read ultrasonic distance
  distance := measure_distance()

  ' Read line sensors
  repeat i from 0 to 4
    line_values[i] := rdpin(LINE_SENSORS + i)

PRI measure_distance() : dist_cm | echo_time
  ' Send trigger pulse
  pinh(ULTRASONIC_TRIG)
  waitus(10)
  pinl(ULTRASONIC_TRIG)

  ' Measure echo time
  repeat until testp(ULTRASONIC_ECHO)
  echo_time := rdpin(ULTRASONIC_ECHO)

  ' Convert to centimeters
  dist_cm := echo_time * 340 / (clkfreq * 2 / 100)

PRI update_navigation()
  ' Line following logic
  line_position := calculate_line_position()

  ' Obstacle avoidance
  if distance < MIN_DISTANCE
    avoid_obstacle()
  else
    follow_line(line_position)

PRI motor_control()
  ' Update motor speeds based on navigation
  set_motor_speed(LEFT_PWM, LEFT_DIR, left_speed)
  set_motor_speed(RIGHT_PWM, RIGHT_DIR, right_speed)

PRI set_motor_speed(pwm_pin, dir_pin, speed)
  if speed < 0
    pinl(dir_pin)               ' Reverse
    wypin(pwm_pin, -speed * 100)
  else
    pinh(dir_pin)               ' Forward
    wypin(pwm_pin, speed * 100)
```
:::

# Part III: System Integration

## Chapter 9: Building Complex Systems

### Combining Everything We've Learned

Now let's create a complete data acquisition and control system that showcases the full power of Smart Pins working together.

```{=latex}
\CompleteSystemDiagram
```

::: spin2
```
'' Complete Industrial Control System
'' Demonstrates: ADC, DAC, PWM, Encoders, Serial, Timing

CON
  _clkfreq = 200_000_000

  ' System constants
  CONTROL_RATE = 1000           ' Hz
  ADC_CHANNELS = 8
  PWM_CHANNELS = 4

OBJ
  system : "control_system"

VAR
  long adc_values[ADC_CHANNELS]
  long pwm_values[PWM_CHANNELS]
  long encoder_positions[4]
  long system_time

PUB main()
  init_system()

  repeat
    system_time++

    ' Read all inputs
    read_all_adc()
    read_all_encoders()
    check_communications()

    ' Run control algorithm
    run_control_loop()

    ' Update all outputs
    update_all_pwm()
    update_all_dac()
    send_status()

    ' Maintain timing
    waitcnt(cnt + clkfreq / CONTROL_RATE)

PRI init_system()
  ' Initialize all Smart Pins
  init_adc_channels()
  init_pwm_channels()
  init_encoder_channels()
  init_communication()
  init_timing_system()

PRI init_adc_channels() | i
  repeat i from 0 to ADC_CHANNELS - 1
    pinstart(ADC_BASE + i, P_ADC_1X | P_ADC_GND | P_ADC_SINC2, 0, 0)

PRI init_pwm_channels() | i
  repeat i from 0 to PWM_CHANNELS - 1
    pinstart(PWM_BASE + i, P_PWM_TRIANGLE | P_OE, 10_000, 5_000)

PRI init_encoder_channels() | i
  repeat i from 0 to 3
    pinstart(ENC_BASE + i*2, ...
      P_QUADRATURE | (ENC_BASE + i*2 + 1) << 8, 0, 0)

PRI read_all_adc() | i
  repeat i from 0 to ADC_CHANNELS - 1
    adc_values[i] := rdpin(ADC_BASE + i)

PRI read_all_encoders() | i
  repeat i from 0 to 3
    encoder_positions[i] := rdpin(ENC_BASE + i*2)

PRI run_control_loop() | i, error, output
  ' PID control for each channel
  repeat i from 0 to PWM_CHANNELS - 1
    error := setpoints[i] - adc_values[i]

    ' Proportional
    output := error * KP[i]

    ' Integral
    integral[i] += error
    output += integral[i] * KI[i]

    ' Derivative
    output += (error - last_error[i]) * KD[i]
    last_error[i] := error

    ' Limit output
    pwm_values[i] := output #> 0 <# 10_000

PRI update_all_pwm() | i
  repeat i from 0 to PWM_CHANNELS - 1
    wypin(PWM_BASE + i, pwm_values[i])
```
:::

### Performance Metrics and Validation


::: spin2
```
PUB measure_system_performance() | start, overhead, pins_configured
  ' Count configured Smart Pins
  pins_configured := 0
  repeat pin from 0 to 63
    if testp(pin)
      pins_configured++

  debug("Smart Pins active: ", udec(pins_configured))

  ' Measure update overhead
  start := cnt
  repeat 1000
    update_all_smart_pins()
  overhead := cnt - start

  debug("Update time: ", udec(overhead / 1000), " clocks")
  debug("Update rate: ", udec(clkfreq / (overhead / 1000)), " Hz max")

  ' Measure latency
  measure_response_latency()

PRI measure_response_latency() | start, latency
  ' Configure test pins
  pinstart(TEST_OUT, P_TRANSITION | P_OE, 1000, 0)
  pinstart(TEST_IN, P_COUNT_RISES | TEST_OUT << 8, 0, 0)

  ' Measure propagation
  start := cnt
  wypin(TEST_OUT, 1)
  repeat until rdpin(TEST_IN) > 0
  latency := cnt - start

  debug("Smart Pin latency: ", udec(latency), " clocks")
  debug("Latency: ", udec(latency * 1_000_000 / clkfreq), " ns")
```
:::

# Part IV: Reference

## Appendix A: Complete Mode Reference

### Quick Reference Table

| Mode | Constant | Name | Primary Use |
|------|----------|------|-------------|
| %00000 | P_NORMAL | Normal (Pass-through) | Disable Smart Pin mode |
| %00001 | P_REPOSITORY | Repository/DAC Noise | Shared storage or DAC noise |
| %00010 | P_DAC_DITHER_RND | DAC 16-bit PRNG Dither | Analog output with random dither |
| %00011 | P_DAC_DITHER_PWM | DAC 16-bit PWM Dither | Analog output with PWM dither |
| %00100 | P_PULSE | Pulse/Cycle Output | Pulse generation |
| %00101 | P_TRANSITION | Transition Output | State transitions at intervals |
| %00110 | P_NCO_FREQ | NCO Frequency | Frequency synthesis |
| %00111 | P_NCO_DUTY | NCO Duty | Frequency with duty control |
| %01000 | P_PWM_TRIANGLE | PWM Triangle | Phase-correct PWM (symmetric) |
| %01001 | P_PWM_SAWTOOTH | PWM Sawtooth | Standard PWM (ramp-reset) |
| %01010 | P_PWM_SMPS | PWM SMPS | Switch-mode power supply |
| %01011 | P_QUADRATURE | Quadrature Encoder | A/B encoder input |
| %01100 | P_REG_UP | Count A-rises (B-high) | Conditional pulse counting |
| %01101 | P_REG_UP_DOWN | Count A-rise, inc/dec B | Step/direction counting |
| %01110 | P_COUNT_RISES | Count A-edges | Edge counting with B-dec option |
| %01111 | P_COUNT_HIGHS | Count A-high or A&B-high | State counting/comparison |
| %10000 | P_STATE_TICKS | Time A-states | State duration measurement |
| %10001 | P_HIGH_TICKS | Time A-high states | High-state duration |
| %10010 | P_EVENTS_TICKS | Time X A-highs/rises/edges | Event timing |
| %10011 | P_PERIODS_TICKS | For X periods, count time | Period measurement |
| %10100 | P_PERIODS_HIGHS | For X periods, count states | Period state counting |
| %10101 | P_COUNTER_TICKS | For X clocks, count periods | Frequency counting |
| %10110 | P_COUNTER_HIGHS | For X clocks, count states | State frequency |
| %10111 | P_COUNTER_PERIODS | For X clocks, count time | Continuous timing |
| %11000 | P_ADC | ADC Sample/Filter (int clk) | Analog input, internal clock |
| %11001 | P_ADC_EXT | ADC Sample/Filter (ext clk) | Analog input, external clock |
| %11010 | P_ADC_SCOPE | ADC Scope with Trigger | Triggered analog capture |
| %11011 | P_USB_PAIR | USB Host/Device (pair) | USB communication |
| %11100 | P_SYNC_TX | Synchronous Serial TX | SPI/synchronous transmit |
| %11101 | P_SYNC_RX | Synchronous Serial RX | SPI/synchronous receive |
| %11110 | P_ASYNC_TX | Asynchronous Serial TX | UART transmit |
| %11111 | P_ASYNC_RX | Asynchronous Serial RX | UART receive |

## Appendix B: Complete Smart Pin Constants Reference

This appendix provides all Smart Pin-relevant P_ constants with their hex values and bit field decomposition.

### Understanding the D Parameter Bit Fields

The WRPIN D parameter (and PINSTART mode parameter) follows this 32-bit format:

```{=latex}
\WRPINFormatDiagram
```

### Smart Pin Mode Constants (SSSSS Field)

| Constant | Mode | Description |
|----------|------|-------------|
| P_NORMAL | %00000 | Smart Pin OFF (normal GPIO) |
| P_REPOSITORY | %00001 | Long repository / DAC noise |
| P_DAC_DITHER_RND | %00010 | DAC with 16-bit PRNG dither |
| P_DAC_DITHER_PWM | %00011 | DAC with 16-bit PWM dither |
| P_PULSE | %00100 | Pulse/cycle output |
| P_TRANSITION | %00101 | Transition output |
| P_NCO_FREQ | %00110 | NCO frequency |
| P_NCO_DUTY | %00111 | NCO duty cycle |
| P_PWM_TRIANGLE | %01000 | PWM triangle wave |
| P_PWM_SAWTOOTH | %01001 | PWM sawtooth wave |
| P_PWM_SMPS | %01010 | PWM for SMPS |
| P_QUADRATURE | %01011 | A/B quadrature encoder |
| P_REG_UP | %01100 | Count A-rises when B-high |
| P_REG_UP_DOWN | %01101 | Count A-rise, inc/dec by B |
| P_COUNT_RISES | %01110 | Count A-edges, optional B-dec |
| P_COUNT_HIGHS | %01111 | Count A-high or A&B-high |
| P_STATE_TICKS | %10000 | Time A-states |
| P_HIGH_TICKS | %10001 | Time A-high states |
| P_EVENTS_TICKS | %10010 | Time X A-highs/rises/edges |
| P_PERIODS_TICKS | %10011 | For X periods, count time |
| P_PERIODS_HIGHS | %10100 | For X periods, count states |
| P_COUNTER_TICKS | %10101 | For X clocks, count periods |
| P_COUNTER_HIGHS | %10110 | For X clocks, count states |
| P_COUNTER_PERIODS | %10111 | For X clocks, count time |
| P_ADC | %11000 | ADC sample/filter, internal clk |
| P_ADC_EXT | %11001 | ADC sample/filter, external clk |
| P_ADC_SCOPE | %11010 | ADC scope with trigger |
| P_USB_PAIR | %11011 | USB host/device (pin pair) |
| P_SYNC_TX | %11100 | Synchronous serial transmit |
| P_SYNC_RX | %11101 | Synchronous serial receive |
| P_ASYNC_TX | %11110 | Asynchronous serial transmit |
| P_ASYNC_RX | %11111 | Asynchronous serial receive |

### A-Input Routing Constants (AAAA Field, bits 31:28)

| Constant | Hex | AAAA | Description |
|----------|-----|------|-------------|
| P_TRUE_A | $00000000 | 0000 | This pin's input, true polarity |
| P_INVERT_A | $80000000 | 1000 | This pin's input, inverted |
| P_LOCAL_A | $00000000 | 0000 | This pin's read state (same as TRUE_A) |
| P_PLUS1_A | $10000000 | 0001 | Pin+1 input, true |
| P_PLUS2_A | $20000000 | 0010 | Pin+2 input, true |
| P_PLUS3_A | $30000000 | 0011 | Pin+3 input, true |
| P_OUTBIT_A | $40000000 | 0100 | This pin's OUT bit |
| P_MINUS3_A | $50000000 | 0101 | Pin-3 input, true |
| P_MINUS2_A | $60000000 | 0110 | Pin-2 input, true |
| P_MINUS1_A | $70000000 | 0111 | Pin-1 input, true |
| P_INVERT_PLUS1_A | $90000000 | 1001 | Pin+1 input, inverted |
| P_INVERT_PLUS2_A | $A0000000 | 1010 | Pin+2 input, inverted |
| P_INVERT_PLUS3_A | $B0000000 | 1011 | Pin+3 input, inverted |
| P_INVERT_OUTBIT_A | $C0000000 | 1100 | This pin's OUT bit, inverted |
| P_INVERT_MINUS3_A | $D0000000 | 1101 | Pin-3 input, inverted |
| P_INVERT_MINUS2_A | $E0000000 | 1110 | Pin-2 input, inverted |
| P_INVERT_MINUS1_A | $F0000000 | 1111 | Pin-1 input, inverted |

### B-Input Routing Constants (BBBB Field, bits 27:24)

| Constant | Hex | BBBB | Description |
|----------|-----|------|-------------|
| P_TRUE_B | $00000000 | 0000 | This pin's input, true polarity |
| P_INVERT_B | $08000000 | 1000 | This pin's input, inverted |
| P_LOCAL_B | $00000000 | 0000 | This pin's read state (same as TRUE_B) |
| P_PLUS1_B | $01000000 | 0001 | Pin+1 input, true |
| P_PLUS2_B | $02000000 | 0010 | Pin+2 input, true |
| P_PLUS3_B | $03000000 | 0011 | Pin+3 input, true |
| P_OUTBIT_B | $04000000 | 0100 | This pin's OUT bit |
| P_MINUS3_B | $05000000 | 0101 | Pin-3 input, true |
| P_MINUS2_B | $06000000 | 0110 | Pin-2 input, true |
| P_MINUS1_B | $07000000 | 0111 | Pin-1 input, true |
| P_INVERT_PLUS1_B | $09000000 | 1001 | Pin+1 input, inverted |
| P_INVERT_PLUS2_B | $0A000000 | 1010 | Pin+2 input, inverted |
| P_INVERT_PLUS3_B | $0B000000 | 1011 | Pin+3 input, inverted |
| P_INVERT_OUTBIT_B | $0C000000 | 1100 | This pin's OUT bit, inverted |
| P_INVERT_MINUS3_B | $0D000000 | 1101 | Pin-3 input, inverted |
| P_INVERT_MINUS2_B | $0E000000 | 1110 | Pin-2 input, inverted |
| P_INVERT_MINUS1_B | $0F000000 | 1111 | Pin-1 input, inverted |

### Input Filter Constants (FFF Field, bits 23:21)

| Constant | Hex | FFF | Description |
|----------|-----|-----|-------------|
| P_FILT0_AB | $00800000 | 100 | Filter A and B using global FILT0 setting |
| P_FILT1_AB | $00A00000 | 101 | Filter A and B using global FILT1 setting |
| P_FILT2_AB | $00C00000 | 110 | Filter A and B using global FILT2 setting |
| P_FILT3_AB | $00E00000 | 111 | Filter A and B using global FILT3 setting |
| P_SCHMITT_A | $00000000 | - | Schmitt trigger on A (via M bits) |
| P_SCHMITT_B | $00000000 | - | Schmitt trigger on B (via M bits) |
| P_SCHMITT_AB | $00000000 | - | Schmitt trigger on A and B |

### Output Control Constants (TT Field, bits 7:6)

| Constant | TT | Description |
|----------|----|-----------------------------------------|
| P_TT_00 | 00 | DIR/OUT not overridden (default) |
| P_OE | 01 | Output enable (Smart Pin controls OUT) |
| P_TT_10 | 10 | DIR overridden high, OUT not overridden |
| P_TT_11 | 11 | DIR and OUT both overridden high |

### DAC Configuration Constants (M bits 20:16)

| Constant | Hex | Impedance | Voltage | Use Case |
|----------|-----|-----------|---------|----------|
| P_DAC_990R_3V | $00140000 | 990$\Omega$ | 3.3V | General purpose |
| P_DAC_600R_2V | $00150000 | 600$\Omega$ | 2.0V | Low voltage |
| P_DAC_124R_3V | $00160000 | 124$\Omega$ | 3.3V | High current |
| P_DAC_75R_2V | $00170000 | 75$\Omega$ | 2.0V | Video output (75$\Omega$ term) |

### ADC Configuration Constants (M bits)

| Constant | Hex | Description |
|----------|-----|-------------|
| P_ADC_GIO | $00800000 | ADC GIO mode (measure pin vs GND) |
| P_ADC_VIO | $00880000 | ADC VIO mode (measure pin vs VIO) |
| P_ADC_FLOAT | $00900000 | ADC float mode (measure pin floating) |
| P_ADC_1X | $00980000 | ADC 1X gain (default) |
| P_ADC_3X | $00A00000 | ADC 3X gain |
| P_ADC_10X | $00A80000 | ADC 10X gain |
| P_ADC_30X | $00B00000 | ADC 30X gain |
| P_ADC_100X | $00B80000 | ADC 100X gain |

### Drive Strength Constants (M bits)

**High-Side Drive:**

| Constant | Hex | Description |
|----------|-----|-------------|
| P_HIGH_FAST | $00000000 | Fast high drive |
| P_HIGH_1K5 | $00000100 | 1.5K high drive |
| P_HIGH_15K | $00000200 | 15K high drive |
| P_HIGH_150K | $00000300 | 150K high drive |
| P_HIGH_1MA | $00000400 | 1mA high drive |
| P_HIGH_100UA | $00000500 | 100$\mu$A high drive |
| P_HIGH_10UA | $00000600 | 10$\mu$A high drive |
| P_HIGH_FLOAT | $00000700 | Float high |

**Low-Side Drive:**

| Constant | Hex | Description |
|----------|-----|-------------|
| P_LOW_FAST | $00000000 | Fast low drive |
| P_LOW_1K5 | $00000800 | 1.5K low drive |
| P_LOW_15K | $00001000 | 15K low drive |
| P_LOW_150K | $00001800 | 150K low drive |
| P_LOW_1MA | $00002000 | 1mA low drive |
| P_LOW_100UA | $00002800 | 100$\mu$A low drive |
| P_LOW_10UA | $00003000 | 10$\mu$A low drive |
| P_LOW_FLOAT | $00003800 | Float low |

### Combining Constants

Constants are combined with OR (|) to build complete configurations:

::: spin2
```
' Example: UART TX on pin 20, 115200 baud, 8 data bits
' P_ASYNC_TX = $0000003C (mode %11110)
' P_OE       = $00000040 (output enable)
' Combined   = $0000007C

mode := P_ASYNC_TX | P_OE
' mode = $0000_007C
' Binary: %0000_0000_000_0000000000000_01_11110_0
'          AAAA_BBBB_FFF_MMMMMMMMMMMMM_TT_SSSSS_0

pinstart(20, mode, (_clkfreq / 115_200) << 16 | 8, 0)
```
:::

::: spin2
```
' Example: SPI MOSI with clock on adjacent pin
' P_SYNC_TX  = $00000038 (mode %11100)
' P_OE       = $00000040 (output enable)
' P_PLUS1_B  = $01000000 (clock from pin+1)
' Combined   = $01000078

mode := P_SYNC_TX | P_OE | P_PLUS1_B
' mode = $0100_0078
' Binary: %0000_0001_000_0000000000000_01_11100_0
'          AAAA_BBBB_FFF_MMMMMMMMMMMMM_TT_SSSSS_0

pinstart(SPI_MOSI, mode, 8, 0)  ' 8-bit SPI
```
:::

::: spin2
```
' Example: ADC with 10X gain and Sinc2 filtering
' P_ADC      = $00000030 (mode %11000)
' P_ADC_10X  = $00040000 (10X gain in M bits)
' P_ADC_GIO  = $00100000 (GIO mode in M bits)
' Combined   = $00140030

mode := P_ADC | P_ADC_10X | P_ADC_GIO
' mode = $0014_0030

pinstart(ADC_PIN, mode, 0, 0)
```
:::

### Quick Lookup: Common Configurations

| Use Case | Constants to OR Together | Result |
|----------|--------------------------|--------|
| PWM output | P_PWM_SAWTOOTH \| P_OE | $00000052 |
| UART TX | P_ASYNC_TX \| P_OE | $0000007C |
| UART RX | P_ASYNC_RX | $0000003E |
| SPI TX | P_SYNC_TX \| P_OE \| P_PLUS1_B | $01000078 |
| SPI RX | P_SYNC_RX \| P_MINUS1_B | $0700003A |
| ADC | P_ADC \| P_ADC_1X | $00980030 |
| NCO freq | P_NCO_FREQ \| P_OE | $0000004C |
| DAC 8-bit | P_DAC_DITHER_RND \| P_DAC_124R_3V \| P_OE | $00160044 |

## Appendix C: Timing Formulas

### Frequency Calculations

**NCO Frequency:**

$$\text{Frequency} = \frac{X \times \text{ClockFreq}}{2^{32}}$$

$$X = \frac{\text{Frequency} \times 2^{32}}{\text{ClockFreq}}$$

**PWM Frequency:**

$$\text{PWM\_Freq} = \frac{\text{ClockFreq}}{\text{Period}}$$

$$\text{Period} = \frac{\text{ClockFreq}}{\text{PWM\_Freq}}$$

**Transition Rate:**

$$\text{Toggle\_Rate} = \frac{\text{ClockFreq}}{2 \times X}$$

$$X = \frac{\text{ClockFreq}}{2 \times \text{Toggle\_Rate}}$$

### Time Measurements

**Pulse Width:**

$$\text{Width\_Seconds} = \frac{\text{Count}}{\text{ClockFreq}}$$

$$\text{Width\_Microseconds} = \frac{\text{Count}}{\text{ClockFreq} / 1{,}000{,}000}$$

**Frequency from Count:**

$$\text{Frequency} = \frac{\text{Count}}{\text{Measurement\_Time}}$$

## Appendix D: Code Examples Summary

### Complete Working Examples

Code examples for all 32 Smart Pin modes are provided in-line throughout the mode chapters in Part II. Each mode section includes:

- Configuration code with PINSTART parameters
- Basic usage patterns
- Advanced techniques where applicable
- Common applications with full working code

For the most comprehensive examples, see:

- **Chapter 3**: Digital I/O modes (%00000-%00011)
- **Chapter 4**: Measurement and counting modes (%01011-%10111)
- **Chapter 5**: ADC, USB, and Serial modes (%11000-%11111)
- **Chapter 5 Advanced Techniques**: Polling vs Events, High-Performance Patterns, IN Flag Management

## Appendix E: Troubleshooting Guide

### Problem-Solution Matrix

| Problem | Possible Causes | Solutions |
|---------|----------------|-----------|
| No output | Missing P_OE | Add P_OE to mode |
| Wrong frequency | Calculation error | Check formula |
| Pin not responding | Not enabled | Use DIRH |
| Unexpected values | Wrong mode | Verify mode bits |
| Timing drift | Clock source | Check _clkfreq |

### Diagnostic Procedures

1. **Verify Configuration**
2. **Check Electrical Connections**
3. **Test with Known Good Code**
4. **Use Debug Output**
5. **Scope the Signals**

## Conclusion: Your Smart Pin Journey

### What You've Learned

Congratulations! You've mastered:

- All 32 Smart Pin modes
- Configuration techniques
- Multi-pin coordination
- System integration
- Troubleshooting methods

### Where to Go Next

::: tip
The P2 community is always discovering new Smart Pin techniques. Join the forums at forums.parallax.com to share your discoveries!
:::

**Advanced Topics to Explore:**

- Custom protocol implementation
- High-speed data acquisition
- Precision measurement systems
- Complex motor control
- Software-defined radio

### Final Thoughts

Smart Pins represent a paradigm shift in microcontroller I/O. By offloading repetitive tasks to dedicated hardware, your code becomes cleaner, more efficient, and more powerful. The techniques you've learned here will serve you well in any P2 project.

Remember: Smart Pins are tools. Like any tool, they become more powerful as you gain experience. Don't be afraid to experiment, make mistakes, and push the boundaries of what's possible.

Happy coding, and welcome to the Smart Pin revolution!

## INDEX

### A
- ADC modes: Ch 18-19, pp. 95-105
- ADC calibration: Appendix C
- ADDPINS operator: Ch 0.6, p. 8
- Analog-to-Digital: See ADC modes
- Architecture, Smart Pin: Ch 1, pp. 12-15
- Asynchronous serial: Ch 21-24, pp. 115-135

### B
- Basic I/O instructions: Ch 0, pp. 3-10
- Bit-banging: Ch 0.5, p. 7
- Button debouncing: Ch 0.5, p. 7
- Button reading: Ch 0.1-0.2, pp. 4-5

### C
- Clock cycles: Ch 0.3, p. 6
- Configuration constants: Appendix B
- Configuration sequence: Ch 1, pp. 15-16
- Counter modes: Ch 11-15, pp. 65-85
- CORDIC operations: Referenced throughout

### D
- DAC modes: Ch 2-3, pp. 20-30
- DAC configurations: Ch 2.3, pp. 23-24
- Debouncing: Ch 0.5, p. 7
- Digital-to-Analog: See DAC modes
- DIR instructions: Ch 0.1, 0.4, pp. 3-4, 6
- DIRA/DIRB registers: Ch 0.4, p. 6
- Direction control: Ch 0.1, pp. 3-4
- DIRH instruction: Ch 0.1, p. 3
- DIRL instruction: Ch 0.1, p. 3
- DRV instructions: Ch 0.4, 0.9, pp. 6, 9

### E
- Electrical specifications: DAC modes (Ch 2-3), ADC modes (Ch 18-20)
- Encoder modes: Ch 14-15, pp. 75-85
- Error handling: Appendix E
- Essential instructions: Ch 0.1, pp. 3-4
- Event system: Referenced in modes

### F
- FIFO operations: Multiple modes
- Filter modes: Ch 9, pp. 50-55
- FLT instructions: Ch 0.4, 0.9, pp. 6, 9
- Float operations: Ch 0.4, p. 6
- Frequency measurement: Ch 17, pp. 90-94

### G
- Goertzel mode: Ch 9, pp. 52-54

### H
- Hub interface: Referenced throughout

### I
- I/O fundamentals: Ch 0, pp. 3-10
- INA register: Ch 0.2, pp. 4-5
- INB register: Ch 0.2, pp. 4-5
- Input reading: Ch 0.2, pp. 4-5
- Input timing: Ch 0.3, p. 6
- Instruction reference, basic: Ch 0.9, p. 9
- Interrupts: Not used with Smart Pins

### L
- LED control: Ch 0.1, 0.5, pp. 3-4, 7
- Logic modes: Ch 4, pp. 31-35

### M
- Measurement modes: Ch 16-20, pp. 86-110
- Mode %00000 (OFF): Ch 1, p. 18
- Mode %00001 (Repository): Ch 2, pp. 20-22
- Mode %00010-%00011 (DAC): Ch 2-3, pp. 23-30
- Mode %00100-%00111 (Pulse/NCO): Ch 5-8, pp. 36-49
- Mode %01000-%01001 (PWM): Ch 9-10, pp. 50-60
- Mode %01010 (SMPS): Ch 11, pp. 61-64
- Mode %01011-%01111 (Counter): Ch 12-15, pp. 65-85
- Mode %10000-%10111 (Measurement): Ch 16-17, pp. 86-94
- Mode %11000-%11010 (ADC/Scope): Ch 18-20, pp. 95-110
- Mode %11011 (USB): Ch 21, pp. 111-114
- Mode %11100-%11111 (Serial): Ch 22-24, pp. 115-135
- Mode configuration: All mode chapters
- Mode selection guide: Appendix A
- Multi-pin coordination: Part III, pp. 136-145
- Multiple pin control: Ch 0.6, p. 8

### N
- NCO modes: Ch 6-8, pp. 40-49
- NOT instruction: Ch 0.4, p. 6

### O
- OUT instructions: Ch 0.1, 0.4, pp. 3-4, 6
- OUTA/OUTB registers: Ch 0.4, 0.6, pp. 6, 8
- OUTH instruction: Ch 0.1, p. 3
- OUTL instruction: Ch 0.1, p. 3
- OUTNOT instruction: Ch 0.4, p. 6
- Output timing: Ch 0.3, p. 6

### P
- P_ constants: Appendix B
- Parallel output: Ch 0.5, p. 7
- Pattern generation: Multiple modes
- Pin direction: Ch 0.1, pp. 3-4
- Pin timing: Ch 0.3, p. 6
- pinstart() function: Ch 1, pp. 14-15
- Pulse modes: Ch 5-6, pp. 36-42
- PWM modes: Ch 9-10, pp. 50-60

### Q
- Quadrature encoder: Ch 14-15, pp. 75-85
- Quick reference, basic I/O: Ch 0.9, p. 9
- Quick reference, Smart Pins: Each mode chapter

### R
- Random instruction variant: Ch 0.4, p. 6
- RDPIN instruction: All mode chapters
- Reading inputs: Ch 0.2, pp. 4-5
- Register structure: Ch 1, pp. 15-16
- Repository mode: Ch 2, pp. 20-22
- RQPIN instruction: Referenced in modes

### S
- Sampling timing: Ch 0.3, p. 6
- Scope mode: Ch 20, pp. 106-110
- Serial modes: Ch 21-24, pp. 111-135
- Smart Pin architecture: Ch 1, pp. 12-15
- Smart Pin concept: Ch 1, pp. 11-12
- SMPS mode: Ch 11, pp. 61-64
- Square wave generation: Ch 0.7, 1, pp. 8, 14
- Synchronous serial: Ch 22-23, pp. 120-130

### T
- Timing diagrams: Ch 0.3, p. 6
- Timing measurement: Ch 16-17, pp. 86-94
- Toggle operation: Ch 0.4, p. 6
- Transition mode: Ch 1, p. 14
- Troubleshooting: Appendix E

### U
- UART: See Asynchronous serial
- USB mode: Ch 21, pp. 111-114

### V
- Voltage measurement: See ADC modes

### W
- waitus/waitms functions: Ch 0.1, pp. 3-4
- WRPIN instruction: All mode chapters
- WXPIN instruction: All mode chapters
- WYPIN instruction: All mode chapters

### X
- X register: Ch 1, all mode chapters
- X/Y/Z registers: Ch 1, pp. 15-16

### Y
- Y register: Ch 1, all mode chapters

### Z
- Z register: Ch 1, all mode chapters
- Zero flag operations: Ch 0.4, p. 6
