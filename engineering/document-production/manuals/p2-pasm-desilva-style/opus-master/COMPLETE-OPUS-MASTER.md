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
{\fontsize{36}{42}\selectfont\bfseries P2 Assembly Programming\par}
\vspace{0.3cm}
{\Large\itshape A Human-Centered Approach to Parallel Processing\par}
\vspace{0.6cm}
{\large December 2025\par}
\vspace{0.2cm}
{\large\color{blue}Version 1.1.0 - Technical Review\par}

\vfill
\begin{tcolorbox}[
  colback=gray!5,
  colframe=gray!40,
  boxrule=1pt,
  width=0.85\textwidth,
  center,
  title={\bfseries\color{black} Tutorial Philosophy},
  colbacktitle=gray!15,
  coltitle=black
]
\textbf{Learn by doing, celebrate progress, have fun!}

\vspace{0.3cm}
\begin{minipage}[t]{0.38\textwidth}
\textbf{Code Block Colors:}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item \textcolor{green!50!black}{\textbf{Green}} -- Spin2
\item \textcolor{orange!70!black}{\textbf{Yellow}} -- PASM2
\item \textcolor{purple!60!black}{\textbf{Purple}} -- CORDIC
\item \textcolor{blue!60!black}{\textbf{Blue}} -- Multi-COG
\item \textcolor{red!60!black}{\textbf{Red}} -- Antipattern
\end{itemize}
\end{minipage}%
\hfill%
\begin{minipage}[t]{0.58\textwidth}
\textbf{Teaching Elements:}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item \textcolor{purple!60!black}{\textbf{Sidetracks}} -- deeper dives
\item \textcolor{teal!70!black}{\textbf{Medicine Cabinet}} -- simpler alternatives
\item \textcolor{green!50!black}{\textbf{Your Turn}} -- hands-on exercises
\item \textcolor{orange!70!black}{\textbf{Interludes}} -- stories \& context
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

Propeller, Propeller 2, P2, Spin, and the Parallax logo are trademarks of Parallax Inc.

### Disclaimer

The information in this manual is subject to change without notice. While every effort has been made to ensure accuracy, the authors and publishers assume no responsibility for errors or omissions, or for damages resulting from the use of the information contained herein.


# Dedication

**To deSilva** — *Whose legendary P1 assembly tutorial taught a generation of programmers that assembly language could be approachable, enjoyable, and even fun. Your unique voice—combining technical precision with human warmth—showed us that great documentation teaches not just the mind, but speaks to the spirit of discovery.*

**To the Propeller Community** — *Who have spent countless hours exploring, documenting, and sharing their knowledge. From the early P1 pioneers to today's P2 innovators, your collective wisdom makes this manual possible.*

**To Future Makers** — *May you find in these pages the same joy of discovery that we experienced. The Propeller 2 is more than a microcontroller—it's an invitation to think differently about computing. Welcome to the journey.*

*"The best way to predict the future is to invent it."* — Alan Kay


# Acknowledgments

This manual stands on the shoulders of giants. We gratefully acknowledge:

### Primary Contributors

**deSilva** - For creating the gold standard of microcontroller documentation with the P1 Assembly Tutorial. Your pedagogical approach, combining technical depth with human empathy, remains unmatched. This manual attempts to honor your legacy while adapting to the P2's capabilities.

**Iron Sheep Productions LLC (Stephen M Moraco)** - For extensive P2 documentation efforts, community tools, and the vision of creating an AI-optimized knowledge base. Your systematic approach to extracting and organizing P2 knowledge made this comprehensive manual possible.

**Chip Gracey** - Creator of the Propeller architecture. Thank you for giving us a microcontroller that thinks differently and challenges us to do the same.

### Community Contributors

**The Parallax Forums Community** - Your questions, answers, code examples, and endless experimentation have created a living knowledge base that no single author could match.

**Early P2 Adopters** - Who dealt with evolving documentation, changing specifications, and still produced amazing projects that showed us what was possible.

### Technical Reviewers

Special thanks to those who reviewed drafts, tested code examples, and provided invaluable feedback:

- The P2 Documentation Team at Parallax
- Community members who beta-tested examples
- Everyone who reported errors and suggested improvements

### Inspiration

**The MIT AI Lab** - For showing us that technical documentation can have personality

**Donald Knuth** - For proving that programming texts can be literature

**The Demoscene Community** - For pushing hardware beyond its limits and inspiring us to do the same

### Production Notes

This manual was created using:

- Knowledge extracted from official Parallax technical documentation and OBEX (Object Exchange) community contributions
- AI-assisted content generation trained on deSilva's writing style
- Community validation and real-world testing
- A commitment to making parallel processing accessible to everyone

*"If I have seen further, it is by standing on the shoulders of giants."* — Isaac Newton

Any errors, omissions, or dad jokes that fell flat are entirely the responsibility of the authors, not our distinguished contributors.


# Preface: Welcome to the Journey

Well, here we are! You're about to embark on a journey into the heart of the Propeller 2, and I promise you, it's going to be quite different from what you might expect.

### A Different Kind of Processor

The Propeller 2 isn't just another microcontroller. Oh no, it's something far more interesting. Imagine, if you will, eight independent processors (we call them COGs) all working together in perfect harmony, sharing a common memory space, yet each running their own programs at full speed. No interrupts fighting for attention, no complex priority schemes, just eight brains working in parallel.

And if you think this sounds terribly complicated, you're probably right... but here's the secret: it's actually simpler than traditional architectures once you understand the philosophy.

### About This Manual

This manual follows in the footsteps of deSilva's legendary P1 tutorial. What does that mean? It means we're going to:

1. **Start with working code** - You'll be blinking LEDs before you know what hit you
2. **Learn by doing** - Theory is important, but nothing beats hands-on experience
3. **Have some fun** - Yes, assembly language can actually be enjoyable!
4. **Be honest about complexity** - When something is hard, we'll admit it and then show you how to handle it

### Who Is This For?

Are you a complete beginner to assembly language? Welcome! We'll take good care of you.

Are you a grizzled veteran who's been writing assembly since the 6502? Welcome! The P2 will still surprise you.

Are you somewhere in between? Perfect! This is exactly where you want to be.

The only requirement is curiosity and a willingness to think a bit differently about how computers can work.

### How to Use This Manual

**The Fast Track** — If you're impatient (and who isn't?), jump straight to Chapter 1. Get that LED blinking. Feel the satisfaction. Then come back here when you're ready for more.

**The Scenic Route** — Read the chapters in order. Each builds on the previous one, and I've hidden little gems of knowledge throughout that will make later chapters easier.

**The Reference Approach** — Already know what you're looking for? The table of contents and index are your friends. The appendices contain every instruction, every Smart Pin mode, every CORDIC operation.

### What Makes the P2 Special?

Let me count the ways:

- **8 symmetric COGs** - No master/slave relationships, all COGs are equal
- **64 Smart Pins** - Each pin has its own processor for I/O operations
- **CORDIC engine** - Hardware trigonometry and coordinate transformations
- **Hardware multiply/divide** - Finally! Real math at hardware speed
- **512KB of RAM** - Shared by all COGs with deterministic access timing
- **No interrupts** - Well, actually there are interrupts, but we'll talk about why you probably don't want them

### A Note on Our Approach

The best technical documentation remembers you're human. You'll get frustrated. You'll make mistakes. Your code won't work the first time (or the second, or sometimes even the third).

That's normal. That's learning. And that's why this manual provides plenty of "medicine" along the way - simpler alternatives, working examples, and the occasional moment of levity to keep your spirits up.

### The deSilva Spirit

Throughout this manual, you'll encounter the teaching spirit of deSilva. When you see phrases like:

- "Well, ..." - We're about to correct a common assumption
- "Uff!" - We just got through something complex
- "Have Fun!" - We mean it, this stuff is actually enjoyable

These aren't just quirks; they're signals that we remember you're human and we're on this journey together.

### Ready?

Take a deep breath. Pour yourself your favorite beverage. Open your development environment.

Let's make some magic happen with the Propeller 2!


*"The Propeller architecture is based on the simple idea that the best way to avoid the complexity of interrupts is to have enough processors that you don't need them."*  
— Chip Gracey, creator of the Propeller


**Turn the page, and let's blink that LED!** →


# Chapter 1: Your First Spin

*Let's blink an LED and change your life*

## Why P2?

Before we dive into code, let me tell you why you're in for something different.

If you've fought with interrupt priority conflicts on an ARM, watched your timing jitter because of cache misses, or discovered that the UART you need is only available on pins you're already using... well, the P2 was designed by someone who got tired of those problems too.

Here's the P2 philosophy in a nutshell:

**Instead of one processor fighting with interrupts**, you get eight complete, identical processors (COGs) that run truly in parallel. Your serial handler never delays your motor control. Your sensor sampling never misses a deadline. Each task owns its own processor.

**Instead of fixed peripherals**, every one of the 64 pins contains its own programmable state machine. Any pin can become a UART, PWM output, quadrature encoder, ADC - whatever you need, wherever you need it.

**Instead of timing that depends on cache luck**, the hub memory has deterministic access. Your timing loops work the same way every time.

**Instead of calling math libraries**, there's a hardware CORDIC that computes sine, cosine, and arctangent in exactly 55 clocks. Every time.

Does this mean P2 is perfect for everything? Of course not. But if your projects involve multiple real-time tasks, precise timing, video or audio generation, or just running out of peripheral pins - you're in the right place.

For a full comparison to ARM, ESP32, Arduino, and PIC platforms, see [Appendix A](#appendix-a-platform-comparison). But you probably want to blink that LED first, don't you?

## The Hook: Making Light

I know you're absolutely crazy to have your first instruction executed, so let's not waste any time. Here's a complete PASM2 program that blinks an LED on pin 56 (that's the built-in LED on the P2 Eval board):

::: pasm2
```
CON
  _clkfreq = 200_000_000        ' 200 MHz system clock

DAT
' LED Blinker - Your first PASM2 program!
        org     0               ' Start at COG address 0

        drvh    #56             ' Drive pin 56 high (LED on)
        waitx   ##50_000_000    ' Wait 0.25 seconds at 200MHz
        drvl    #56             ' Drive pin 56 low (LED off)
        waitx   ##50_000_000    ' Wait 0.25 seconds
        jmp     #$-4            ' Jump back 4 longs (addresses)
```
:::

That's it! Five instructions and you have a blinking LED. Load this into any COG and watch the magic happen.

## What's Really Happening

Well, now that you've seen it work (you did try it, right?), let's talk about what's actually going on here.

### The Instructions Decoded

**`org 0`** - This tells the assembler to start placing code at COG address 0. Every COG has its own private 512 longs (2KB) of memory, and execution always starts at address 0 when a COG is loaded.

**`drvh #56`** - This drives pin 56 high (3.3V). The 'h' means high. The '#' means we're using an immediate value (the actual number 56) rather than the contents of register 56. One instruction, and your LED is on!

**`waitx ##50_000_000`** - This waits for 50 million clock cycles. At 200 MHz, that's 0.25 seconds. Notice the double '##'? That means this is a 32-bit immediate value. Single '#' only gives us 9 bits.

**`drvl #56`** - Drive low. LED off. You get the pattern.

**`jmp #$-4`** - Jump back 4 longs. The '$' means "current address", so '$-4' means "4 addresses back from here" (each instruction is one long). Infinite loop achieved!

### But Wait, There's More!

"Hold on," you might say, "how does this even get into the COG?"

Ah, excellent question! In the real world, you'd typically launch this from Spin2 (the high-level language) like this:

::: spin2
```
CON
  _clkfreq = 200_000_000  ' 200 MHz system clock

PUB main()
    coginit(COGEXEC_NEW, @blink_code, 0)  ' Start PASM2 in new COG
    repeat  ' Keep the main COG alive

DAT
        org     0
blink_code
        drvh    #56
        waitx   ##50_000_000
        drvl    #56
        waitx   ##50_000_000
        jmp     #$-4
```
:::

The `coginit` instruction loads your PASM2 code from hub memory into a fresh COG and starts it running. Meanwhile, your Spin2 code keeps running in its own COG. You now have parallel processing!

::: sidetrack
### The Clock Preamble

Notice the `CON` section at the top of that example? Every P2 program needs to configure its system clock:

::: pasm2
```
CON
  _clkfreq = 200_000_000  ' 200 MHz system clock
```
:::

This tells the P2 to run at 200 MHz using your board's crystal oscillator. Without it, the chip runs at a sluggish ~20 MHz on its internal RC oscillator—and timing-dependent code (including DEBUG output) won't behave as expected.

At 200 MHz with most instructions taking 2 clocks, each COG executes approximately 100 million instructions per second (100 MIPS). With 8 COGs running in parallel, that's 800 MIPS of total processing power—and that's before Smart Pins start handling I/O autonomously.

**From here on, we'll omit this preamble from examples to keep them focused on the concept being taught.** When you create your own files, always include it at the top before your `PUB` or `DAT` sections.
:::

## Let's Make It Better

The blinker works, but it's a bit rigid, isn't it? What if we want to change the blink rate? Let's use a register:

::: pasm2
```
        org     0
        
        mov     delay, ##50_000_000    ' Set delay to 0.25 sec
                                       '  (at 200 MHz)
        
.blink  drvh    #56                    ' LED on
        waitx   delay                  ' Wait
        drvl    #56                    ' LED off
        waitx   delay                  ' Wait
        jmp     #.blink                ' Repeat forever
        
delay   long    0                      ' Storage for delay value
```
:::

Uff! Look at that - we're using a register now! The `mov` instruction copies our delay value into a register (which we cleverly named 'delay'). Now we can change the blink rate by modifying just one value.

*A note on terminology: P2 documentation often uses "register" to refer to any long in COG RAM. Unlike ARM or x86 where registers are a small, special set (R0-R15, EAX, etc.), every COG RAM location can be used as a general-purpose register. However, the last 16 locations (496-511) have special functions: addresses 496-503 are dual-purpose (usable as RAM if interrupts aren't used), and 504-511 are special-purpose registers (PTRA, PTRB, DIRA, DIRB, OUTA, OUTB, INA, INB). When you see "register" in P2 context, think "COG RAM location."*

## Understanding COGs

Here's something important: each COG is a complete processor with its own memory. When we loaded our blink program, it was copied from hub memory into COG memory. The COG then executes it independently, without any further connection to hub memory (unless we explicitly read or write to it).

Think of it like this:

- **Hub memory** is the meeting place (512KB shared by all)
- **COG memory** is private workspace (2KB per COG)
- Loading a COG is like making a photocopy - the COG gets its own copy to run

This is why our blinker keeps running even after the Spin2 code that launched it goes into an infinite repeat loop. The COG is independent!

## Your Turn: Experiments

Now for the fun part. Try these modifications:

### Experiment 1: Different Patterns
Make the LED blink in a pattern: short-short-long (like SOS):

::: pasm2
```
        org     0
        
        mov     short, ##20_000_000    ' 0.1 second (at 200 MHz)
        mov     long_d, ##60_000_000   ' 0.3 seconds (at 200 MHz)
        
.pattern drvh    #56                    ' Short pulse 1
        waitx   short
        drvl    #56
        waitx   short

        drvh    #56                    ' Short pulse 2
        waitx   short
        drvl    #56
        waitx   short

        drvh    #56                    ' Long pulse
        waitx   long_d
        drvl    #56
        waitx   long_d

        jmp     #.pattern
        
short   long    0
long_d  long    0
```
:::

### Experiment 2: Multiple LEDs
Blink LEDs on pins 56 and 57 alternately:

::: pasm2
```
        org     0
        
.loop   drvh    #56                    ' LED 56 on
        drvl    #57                    ' LED 57 off
        waitx   ##50_000_000           ' 0.25 sec at 200 MHz

        drvl    #56                    ' LED 56 off
        drvh    #57                    ' LED 57 on
        waitx   ##50_000_000           ' 0.25 sec at 200 MHz

        jmp     #.loop
```
:::

### Experiment 3: Fading (Advanced)
This one's a bit tricky - we'll use PWM to fade the LED:

::: pasm2
```
        org     0
        
        wrpin   ##P_PWM_TRIANGLE, #56  ' Configure pin 56 for PWM
        wxpin   ##$100, #56            ' Set period to 256
        dirh    #56                    ' Enable the pin
        
.fade   wypin   level, #56             ' Set duty cycle
        waitx   ##100_000              ' Small delay
        add     level, #1              ' Increment brightness
        and     level, #$FF            ' Wrap at 256
        jmp     #.fade
        
level   long    0
```
:::

Don't worry if the PWM example seems complex - we'll cover Smart Pins in detail in Chapter 8!

::: medicine-cabinet
Feeling overwhelmed? Here's the simplified prescription:

**Minimum viable blinker** - Just 3 instructions:

::: pasm2
```
.loop   drvnot  #56          ' Toggle pin 56
        waitx   ##50_000_000 ' 0.25s at 200MHz
        jmp     #.loop       ' Repeat
```
:::

The `drvnot` instruction toggles a pin - if it's high, make it low; if it's low, make it high. Sometimes simpler is better!
:::

::: sidetrack
### Why Start at Address 0?

You might wonder why COG code always starts at address 0. It's actually quite elegant:

When a COG is started with `coginit`, the hardware:

1. Stops the COG (if it was running)
2. Copies 512 longs from hub to COG memory (addresses 0-511)
3. Starts execution at COG address 0

This means every COG program starts fresh, with a clean slate. No residual state, no confusion. It's like each COG gets a fresh brain transplant every time it starts!

The last 16 longs (addresses 496-511) have special functions: 496-503 are dual-purpose (usable as RAM if interrupts not used), and 504-511 are special-purpose registers (PTRA, PTRB, DIRA, DIRB, OUTA, OUTB, INA, INB). We'll explore these later.
:::

## Common Gotchas

Before we move on, let me save you some debugging time:

1. **Forgetting the ##** - Using `waitx #25_000_000` will NOT wait for 0.25 seconds! Single # only allows values up to 511.

2. **Wrong pin number** - The P2 Eval board's LEDs are on pins 56-63. The P2 Edge module might have different assignments.

3. **Clock setup required** - P2 boots at ~20MHz (internal RC oscillator). Most programs configure 200MHz with a crystal. Our examples assume 200MHz - adjust WAITX values if your clock differs.

4. **COG already running** - If you `coginit` to a specific COG that's already running something else, it will be stopped and replaced. Use `COGEXEC_NEW` to automatically find a free COG.

## What We've Learned

Let's celebrate what you've accomplished:

- ✅ Written your first PASM2 program
- ✅ Controlled hardware (LED) directly
- ✅ Used immediate values (# and ##)
- ✅ Created loops with JMP
- ✅ Understood COG independence
- ✅ Modified code for different patterns

That's quite a lot for Chapter 1!

## Coming Up Next

In Chapter 2, we'll take our "Architecture Safari" and explore:

- How 8 COGs really work together
- The hub memory system and the "egg beater"
- Why the P2 doesn't need interrupts
- How to make COGs talk to each other

But for now, enjoy your blinking LED. You've just taken your first step into parallel processing!


**Have Fun!** And remember, every expert was once a beginner who kept their LED blinking when everyone else gave up.


*Continue to [Chapter 2: Architecture Safari](02-architecture-safari.md) →*


# Chapter 2: Architecture Safari

*Eight brains are better than one*

## The Propeller Philosophy

Before we dive into the technical details, let's talk philosophy. Why would anyone design a microcontroller with eight processors?

The answer is beautifully simple: to avoid complexity.

"Wait," you might say, "eight processors sounds MORE complex, not less!"

Well, consider the traditional approach:

- One processor trying to do everything
- Interrupts constantly breaking your flow
- Priority levels to juggle
- Context switching overhead
- Race conditions and timing nightmares

Now consider the Propeller way:

- Eight processors, each doing one thing well
- No interrupts needed (why interrupt when you have a dedicated processor?)
- No priorities (all COGs are equal)
- Deterministic timing (you know EXACTLY when things happen)
- True parallel processing (not time-slicing)

It's like the difference between one stressed-out juggler trying to keep eight balls in the air versus eight relaxed people each tossing one ball. Which seems simpler?

## COG Anatomy 101

Let's dissect a COG and see what makes it tick:

```{=latex}
\CogAnatomyDiagram
```

But here's the beautiful part: COGs are identical. There's no "master" COG or "special" COG. Any COG can do anything any other COG can do. Democracy in silicon!

### The 512-Long Limit

Each COG has exactly 512 longs (2048 bytes) of memory. The first 496 longs are yours to use for code and data. The last 16 are special registers (but not like P1 - we'll get to that).

"Only 496 instructions?" you might cry. "That's tiny!"

Well, yes and no. Remember:

1. PASM2 instructions are powerful - one instruction often does what takes several in other processors
2. You have EIGHT of these COGs
3. There's hub execution mode for larger programs (Chapter 10)
4. Most real-time tasks fit easily in 496 instructions

Think of it like haiku - the constraint forces elegance.

## Meet the Hub: The Meeting Place

The hub is where COGs come together. It's 512KB of RAM shared by all COGs, and it's where the magic of cooperation happens.

```{=latex}
\HubMemoryDiagram
```

### The Egg Beater Revolution

Now here's where P2 gets clever. In P1, COGs took turns accessing the hub in a round-robin fashion. If you missed your slot, you waited for the wheel to come around again.

P2 uses what we call the "egg beater" model. Imagine eight beaters (COGs) all whipping through the same bowl (hub) simultaneously, but their paths are cleverly arranged so they never collide:

```{=latex}
\EggBeaterDiagram
```

The practical result? Hub access is MUCH faster and more predictable. Instead of waiting up to 16 clocks (P1), you wait at most 8 clocks (P2), and often less if you align your accesses properly.

## Let's See COGs in Action

Here's a simple demonstration of multiple COGs working together:

::: spin2
```
' Multi-COG LED Pattern Demo
PUB main() | i
    repeat i from 0 to 3
        coginit(COGEXEC_NEW, @cog_code, 56 + i)  ' Start 4 COGs
    repeat  ' Main COG just watches

DAT
        org     0
cog_code
        rdlong  pin_num, ptra          ' Get pin number from hub

.loop   drvnot  pin_num                ' Toggle our LED
        shl     pin_num, #24           ' Pin number to bits 24-31
        or      pin_num, ##10_000_000  ' Combine with delay
        waitx   pin_num                ' Wait (varies per COG!)
        shr     pin_num, #24           ' Restore pin number
        jmp     #.loop

pin_num long    0
```
:::

What's happening here:

1. The main Spin2 code starts 4 COGs
2. Each COG gets a different pin number (56, 57, 58, 59)
3. Each COG blinks its LED at a slightly different rate
4. All four LEDs blink independently and simultaneously!

## COG Communication: How They Talk

COGs are independent, but they're not isolated. They can communicate through hub memory:

### Method 1: Simple Variables

::: pasm2
```
' COG 1: Writer
        mov     value, #42
        wrlong  value, ##$1000  ' Write to hub address $1000

' COG 2: Reader  
        rdlong  result, ##$1000 ' Read from hub address $1000
```
:::

### Method 2: Locks (When It Matters)

When multiple COGs might write to the same location, we need locks:

::: pasm2
```
' Get a lock
.try_lock
        locktry lock_id wc     ' Try to get lock
   if_c jmp     #.try_lock     ' Keep trying if failed

        ' Critical section - we have the lock!
        rdlong  value, ##shared_addr
        add     value, #1
        wrlong  value, ##shared_addr

        lockrel lock_id        ' Release the lock

lock_id long    0              ' Lock 0-15
```
:::

### Method 3: Mailboxes (Elegant)

A mailbox is just a hub location where COGs leave messages:

::: pasm2
```
' COG A: Leave a message
        wrlong  message, ##mailbox
        
' COG B: Check for messages
.check  rdlong  data, ##mailbox wz
   if_z jmp     #.check        ' Keep checking if empty
        wrlong  #0, ##mailbox  ' Clear mailbox
        ' Process the message in 'data'
```
:::

## The Timer: Everyone Gets One

Each COG has its own 64-bit timer, always counting system clocks. This is incredibly useful:

::: pasm2
```
' Method 1: Simple delay
        getct   start_time
        addct1  start_time, ##1_000_000
        waitct1                ' Wait exactly 1,000,000 clocks

' Method 2: Periodic events
        getct   time
.loop   addct1  time, ##10_000_000
        waitct1                ' Wait for next 10M clock interval
        drvnot  #56           ' Toggle LED
        jmp     #.loop        ' Perfectly periodic!
```
:::

The beauty? Each COG's timer is independent. No shared resource conflicts!

## Why No Interrupts? (Usually)

Here's a controversial P2 feature: it HAS interrupts, but you probably shouldn't use them. Why?

Because with 8 COGs, you don't need interrupts! Instead of interrupting important work, just dedicate a COG to monitoring whatever would have triggered the interrupt:

::: pasm2
```
' Traditional (with interrupts):
' Main code runs, gets interrupted, handles event, returns

' Propeller way:
' COG 1: Main code runs uninterrupted
' COG 2: Watches for event continuously
pin_watcher
        testp   #BUTTON_PIN wc
   if_c jmp     #button_pressed
        jmp     #pin_watcher
        
button_pressed
        wrlong  ##1, ##button_flag  ' Signal other COGs
        jmp     #pin_watcher
```
:::

No interrupt latency, no context switching, no priority inversion. Just dedicated, deterministic monitoring.

## Real-World Example: Parallel Sensors

Let's read four different sensors simultaneously:

::: pasm2
```
' Each COG runs this with different parameters
sensor_reader
        rdlong  sensor_pin, ptra[0]    ' Get pin assignment
        rdlong  hub_addr, ptra[1]       ' Where to store results
        
read_loop
        ' Read sensor (simplified - real sensors need protocols)
        testp   sensor_pin wc
        rcl     value, #1               ' Accumulate bits
        
        ' Every 32 reads, store to hub
        incmod  counter, #31 wc
   if_c wrlong  value, hub_addr
   if_c add     hub_addr, #4
        
        jmp     #read_loop

sensor_pin long 0
hub_addr   long 0  
value      long 0
counter    long 0
```
:::

Four COGs running this code = four sensors being read truly simultaneously. Try doing that with a single processor and interrupts!

::: medicine-cabinet
Feeling overwhelmed by all this parallel processing? Here's your prescription:

**Start simple**: Use just one or two COGs at first

::: spin2
```
' Just two COGs - main program and one helper
PUB main()
    coginit(COGEXEC_NEW, @helper, 0)
    ' Your main code here
```
:::

**Debug one COG at a time**: Get each COG working alone before combining

::: pasm2
```
' Test COG in isolation first
debug_cog
        drvh    #MY_DEBUG_LED  ' Visual confirmation it's running
        ' Your actual code here
```
:::

**Use Spin2 for coordination**: Let the high-level language handle the complex stuff

::: spin2
```
' Spin2 manages COGs, PASM2 does the real-time work
PUB orchestrator()
    startSensorCog(0)
    startMotorCog(1)
    startCommsCog(2)
    ' Spin2 coordinates, PASM2 executes
```
:::
:::

::: sidetrack
### The Philosophy of Parallel

The Propeller's design philosophy comes from a simple observation: in the real world, things happen in parallel, not in sequence.

Consider your car:

- The engine runs continuously
- The radio plays independently
- The climate control maintains temperature
- The dashboard updates displays
- The ABS monitors wheel speed

These aren't taking turns - they're all happening simultaneously. The Propeller models this reality directly. Instead of one processor frantically time-slicing between tasks, you have eight processors each focused on their job.

It's not just different - it's more natural.
:::

## Common Gotchas

Save yourself some debugging time:

1. **COG RAM is copied, not shared** - Changes in COG RAM don't affect hub RAM unless you explicitly write them back

2. **COGs start at 0** - Always! Your code better be there.

3. **Hub addresses are byte addresses** - COG addresses are long addresses. Don't mix them up!

::: pasm2
```
   rdlong  value, ##$1000  ' Reads from hub byte address $1000
   mov     value, $100     ' Moves from COG long address $100 (256)
   ' Note: COG RAM is only 512 longs ($000-$1FF)!
```
:::

4. **PTRA/PTRB are your friends** - These special registers make hub access much easier

5. **COGs are truly independent** - Stopping one COG doesn't affect others (unless they're waiting for it)

## What We've Learned

Look at what you now understand:

- ✅ Why eight processors is simpler than one with interrupts
- ✅ How COGs are structured and limited
- ✅ The hub memory system and egg beater access
- ✅ Multiple ways for COGs to communicate
- ✅ Why interrupts are usually unnecessary
- ✅ How to think in parallel

## Your Turn: Experiments

### Experiment 1: COG Counter
Start COGs to increment different hub locations. With COGEXEC_NEW, the loop will start up to 7 new COGs (since COG 0 runs Spin2):

::: spin2
```
PUB main() | i
    repeat i from 0 to 7
        coginit(COGEXEC_NEW, @counter, $1000 + (i * 4))
    repeat
        ' Monitor the counters in hub RAM
        
DAT
        org     0
counter rdlong  hub_ptr, ptra
.loop   rdlong  value, hub_ptr
        add     value, #1
        wrlong  value, hub_ptr
        waitx   ##1_000_000
        jmp     #.loop
        
hub_ptr long    0
value   long    0
```
:::

### Experiment 2: Parallel Pattern
Make 8 LEDs display a moving pattern, with each COG controlling one LED:

::: pasm2
```
' Each COG gets LED pin in ptra
        org     0
        rdlong  pin, ptra
        rdlong  delay, ptrb      ' Different delay per COG
        
.flash  drvh    pin
        waitx   delay
        drvl    pin
        waitx   delay
        shl     delay, #1        ' Double the delay
        cmp     delay, ##100_000_000 wcz
   if_a mov     delay, ##1_000_000  ' Reset if too long
        jmp     #.flash
```
:::

## Coming Up Next

In Chapter 3, "Speaking PASM2", we'll dive deep into the instruction set:

- The anatomy of an instruction
- Conditional execution that will blow your mind
- Math operations that actually make sense
- Why PASM2 is unlike any assembly you've used

But for now, appreciate what you've learned: you understand the Propeller's parallel philosophy. That's not just technical knowledge - it's a new way of thinking about computing.


**Have Fun!** Remember, parallel processing isn't harder - it's different. And different can be wonderful.


*Continue to [Chapter 3: Speaking PASM2](03-speaking-pasm2.md) →*


# Chapter 3: Speaking PASM2

*Learning the native tongue*

## The Hook: One Instruction, Many Powers

Look at this single PASM2 instruction:

::: pasm2
```
        add     value, #1 wc
```
:::

This one line:

- Adds 1 to 'value'
- Optionally sets the carry flag
- Executes in exactly 2 clock cycles
- Can be conditional
- Can even modify itself!

In most processors, that would take multiple instructions. In PASM2, it's just one. Let's learn to speak this powerful language.

## Instruction Anatomy 101

Every PASM2 instruction follows the same basic pattern:

```{=latex}
\InstructionAnatomyDiagram
```

Let's dissect a real instruction:

```{=latex}
\InstructionExampleDiagram
```

## The Basic Vocabulary

### Moving Data Around

The MOV family - your bread and butter:

::: pasm2
```
' Basic move
        mov     dest, source    ' dest = source
        mov     x, #42         ' x = 42 (immediate)
        mov     x, ##70000     ' x = 70000 (32-bit immediate)

' But wait, there's more!
        mvn     dest, source    ' dest = NOT source (inverted)
        abs     dest, source    ' dest = |source|
        neg     dest, source    ' dest = -source

' And the mind-blowing ones
        altd    dest, source    ' Modify NEXT inst's dest field!
        alts    dest, source    ' Modify NEXT inst's source field!
```
:::

Well, that escalated quickly! Don't worry about ALTD/ALTS yet - just know they exist and they're amazing.

### Math Without Tears

P2 has hardware multiply and divide. Let that sink in. Hardware. Multiply. And. Divide.

::: pasm2
```
' Addition and subtraction
        add     x, y           ' x = x + y
        sub     x, y           ' x = x - y
        adds    x, y           ' Signed add
        subs    x, y           ' Signed subtract

' The revolution: hardware multiply!
        mul     x, y           ' x = x * y (low 32 bits)
        muls    x, y           ' Signed multiply
        
' And hardware divide!
        qdiv    x, y           ' Start division x/y
        getqx   result         ' Get quotient
        getqy   remainder      ' Get remainder
```
:::

Here's a complete multiply example:

::: pasm2
```
' Simple 16x16->32 multiply (2 clocks)
        mov     x, #123
        mov     y, #456
        mul     x, y           ' Result: 123 * 456 = 56088 in x
        ' Uses lower 16 bits of each operand!

' For full 32x32->64 multiply, use CORDIC:
        qmul    x, y           ' Start multiply (uses full 32 bits)
        ' ... 54 clocks of other work ...
        getqx   low            ' Lower 32 bits of result
        getqy   high           ' Upper 32 bits of result
```
:::

Uff! In the old days, we'd write loops for this. Now hardware does it!

### Logic Operations

Your Boolean friends:

::: pasm2
```
        and     x, mask        ' x = x AND mask
        or      x, bits        ' x = x OR bits  
        xor     x, toggle      ' x = x XOR toggle
        not     x              ' x = NOT x (XOR with $FFFFFFFF)
        
' Bit manipulation
        bitl    x, #5          ' Clear bit 5 of x
        bith    x, #5          ' Set bit 5 of x
        bitnot  x, #5          ' Toggle bit 5 of x
        testb   x, #5 wc       ' Test bit 5, result in C flag
```
:::

### Shifting and Rotating

Moving bits around:

::: pasm2
```
        shl     x, #3          ' Shift left 3 bits
        shr     x, #3          ' Shift right 3 bits
        sar     x, #3          ' Arithmetic shift right (signed)
        rol     x, #3          ' Rotate left 3 bits
        ror     x, #3          ' Rotate right 3 bits
        
' Variable shifts (amount in register)
        shl     x, y           ' Shift x left by y bits
        
' Fancy ones
        rev     x              ' Reverse bit order (!!)
        mergeb  x              ' Merge bytes (AABBCCDD -> ABCDABCD)
```
:::

## Flow Control: Jump!

### Unconditional Jumps

::: pasm2
```
        jmp     #target        ' Jump to target
        jmp     target         ' Jump to address in target register
        
' Relative jumps
        jmp     #$-4          ' Jump back 4 longs (addresses)
        jmp     #$+8          ' Jump forward 8 instructions
```
:::

### Conditional Execution (The Magic)

Here's where PASM2 gets beautiful. ANY instruction can be conditional:

::: pasm2
```
if_z    add     x, #1          ' Only add if Z flag set
if_nz   add     x, #1          ' Only add if Z flag clear
if_c    add     x, #1          ' Only add if C flag set
if_nc   add     x, #1          ' Only add if C flag clear
```
:::

The basic conditions:

| Condition | Meaning |
|-----------|---------|
| `if_z` | If Z flag set (result was zero) |
| `if_nz` | If Z flag clear (result not zero) |
| `if_c` | If C flag set (carry/borrow occurred) |
| `if_nc` | If C flag clear |
| `if_c_and_z` | If both C and Z set |
| `if_c_or_z` | If either C or Z set |
| `if_c_eq_z` | If C equals Z |
| `if_c_ne_z` | If C not equal to Z |

And the comparison conditions (use after CMP):

| Condition | Meaning |
|-----------|---------|
| `if_a` | If above (unsigned greater) |
| `if_b` | If below (unsigned less) |
| `if_ae` | If above or equal |
| `if_be` | If below or equal |

### The Call/Return Dance

::: pasm2
```
        call    #subroutine    ' Call subroutine
        ret                    ' Return from subroutine
        
' But here's the P2 twist - CALL uses internal stack
subroutine
        ' Do something useful
        ret                    ' Returns to instruction after CALL
        
' You get 8 levels of hardware stack!
```
:::

### The _RET_ Prefix: Return With Benefits

Here's a clever trick the P2 offers. What if you could execute an instruction *and* return from a subroutine in one go? That's exactly what the `_RET_` prefix does.

::: pasm2
```
' Normal way: Two instructions
add_and_return
        add     x, y            ' Do the add
        ret                     ' Then return (4+ cycles total)

' _RET_ way: One instruction!
add_and_return
        _ret_   add     x, y    ' Add AND return (saves 2 cycles)
```
:::

The `_RET_` prefix says: "Execute this instruction, then return." It's like getting a free return ticket with your instruction. The add happens, flags get set normally, and then—pop!—you're back at the caller.

**When does _RET_ NOT return?**

Here's the catch: if the instruction itself branches, no return happens. The branch wins:

::: pasm2
```
        _ret_   jmp     #somewhere      ' JMP wins - no return
        _ret_   call    #helper         ' CALL wins - no return
        _ret_   djnz    count, #loop    ' Branch? No return. Zero? Return!
```
:::

That last one is interesting! If `count` isn't zero, DJNZ branches and no return. But when `count` hits zero, no branch occurs, so you get your return. Clever, right?

**One-Instruction Subroutines**

This is where `_RET_` really shines:

::: pasm2
```
' Toggle pin 0 - entire subroutine is ONE instruction!
toggle_led
        _ret_   drvnot  #0              ' Toggle and return

' Read all inputs - also just one instruction
read_inputs
        _ret_   mov     result, ina     ' Copy INA and return

' Usage:
        call    #toggle_led             ' Blink!
        call    #read_inputs            ' result now has INA
```
:::

A normal subroutine needs at least two instructions (the work + RET). With `_RET_`, you can have genuinely single-instruction subroutines. Your code gets smaller and faster.

**The Medicine: _RET_ Quick Reference**

| Pattern | What Happens |
|---------|--------------|
| `_ret_ add x, y` | ADD executes, then return |
| `_ret_ jmp #label` | JMP executes, NO return (branch wins) |
| `_ret_ djnz n, #loop` | If n>0: branch, no return. If n=0: no branch, return |

**Important**: Unlike `ret wcz`, the `_RET_` prefix does NOT restore C and Z flags from the stack. If you need flag restoration, use the regular `ret wcz` instruction.

## Labels: Naming Your Places

You've been using labels throughout this chapter without us properly introducing them. How rude of me! Let's fix that.

### Global Labels: The Big Signposts

A global label is just a name at the start of a line:

::: pasm2
```
DAT             org

send_byte       rdbyte  x, ptr          ' Global label
                wypin   x, tx_pin
                ret

receive_byte    testp   rx_pin    wc    ' Another global label
                rdpin   x, rx_pin
                ret
```
:::

Global labels are visible everywhere in your DAT block. You can jump to them, call them, reference them from Spin2 - they're your main signposts.

### Local Labels: The Little Helpers

But here's a problem. What if every routine needs a loop? You can't have two labels called `loop` - the assembler would be terribly confused.

Enter local labels. Prefix a name with a dot (`.`) and it becomes local:

::: pasm2
```
DAT             org

send_byte       rdbyte  x, ptr
.loop           testp   tx_pin    wc    ' Local to send_byte
        if_nc   jmp     #.loop
                wypin   x, tx_pin
                ret

receive_byte    testp   rx_pin    wc    ' New scope begins here
        if_nc   jmp     #.wait
.wait           testp   rx_pin    wc    ' Local to receive_byte
        if_nc   jmp     #.wait
                rdpin   x, rx_pin
.loop           shr     x, #24          ' Different .loop, OK!
                ret
```
:::

Each global label starts a new "scope". The `.loop` under `send_byte` is completely separate from the `.loop` under `receive_byte`. You can reuse `.loop`, `.done`, `.retry`, `.exit` to your heart's content.

### The Colon Alternative

You might also see local labels with a colon prefix:

::: pasm2
```
:loop           djnz    count, #:loop   ' Same as .loop
```
:::

Both `:` and `.` work identically. I prefer the dot - it's what modern convention has settled on - but you'll see both in the wild.

### Reference Operators: Finding Your Labels

When you reference a label, you need to tell the assembler what you want:

::: pasm2
```
' In COG code (after ORG):
        jmp     #my_routine     ' # = immediate COG address
        call    #.helper        ' # works for local labels too
        mov     x, #data_table  ' Get COG address of data

' For hub addresses (used with Spin2):
        mov     ptr, @hub_data  ' @ = hub address of label
```
:::

The `#` means "immediate value" - use this for jumps and calls within COG code. The `@` means "hub address" - use this when passing addresses to Spin2 or for hub memory operations.

### Scope Boundaries: When Local Labels Reset

Here's the rule: **every global label or data definition starts a new local scope**.

::: pasm2
```
func_a          mov     x, #1           ' Scope #1 begins
.loop           djnz    x, #.loop       ' .loop in scope #1

data_block      long    0, 0, 0, 0      ' Scope #2 begins (data!)

func_b          mov     y, #2           ' Scope #3 begins
.loop           djnz    y, #.loop       ' .loop in scope #3, OK!
.done           ret
```
:::

This is wonderfully useful - your utility routines can all use `.loop` and `.done` without stepping on each other's toes.

### The Medicine: Quick Reference

| What | Syntax | Example |
|------|--------|---------|
| Global label | `name` | `my_routine` |
| Local label | `.name` or `:name` | `.loop`, `:done` |
| Jump to label | `#label` | `jmp #.loop` |
| Hub address | `@label` | `mov ptr, @data` |

### Common Gotchas

1. **Forgetting the dot**: `loop` is global, `.loop` is local. If you accidentally create a global `loop`, you'll get conflicts.

2. **Scope surprise**: Data definitions (`LONG`, `WORD`, `BYTE`) also start new scopes. If you put data between two parts of a routine, your local labels won't work!

3. **The 30-character limit**: For compatibility with all tools, keep label names under 30 characters. `this_is_a_really_long_label_name` might cause trouble.

## Data in DAT Blocks: Your Program's Pantry

Speaking of data definitions starting new scopes... we should probably talk about how to actually declare data! You've seen snippets like `counter long 0` scattered through our examples, but there's a whole world of data declaration waiting for you.

### The Three Sizes

Just like Goldilocks, you have three choices:

```pasm2
DAT
my_byte         byte    $FF             ' 1 byte (8 bits)
my_word         word    $1234           ' 2 bytes (16 bits)
my_long         long    $DEADBEEF       ' 4 bytes (32 bits)
```

When do you use each? Well:

- **BYTE** for characters, small counters, flags, or when every byte of memory counts
- **WORD** for medium values, 16-bit peripherals, or when BYTE is too small but LONG is wasteful
- **LONG** for everything else - addresses, large numbers, and "I don't want to think about it"

If you're unsure, use LONG. Memory is cheap, debugging overflow errors is not.

### Multiple Values on One Line

Here's a convenience - you can list multiple values after a single type:

```pasm2
DAT
primes          long    2, 3, 5, 7, 11, 13, 17, 19
gpio_pins       byte    16, 17, 18, 19, 20, 21
message         byte    "Hello, P2!", 0     ' String with null term
```

The assembler just lays them out consecutively in memory. That string? It's just bytes - each character followed by a zero at the end.

### Arrays: The Repetition Trick

Need 100 bytes of zeros? Don't type them all out:

```pasm2
DAT
buffer          byte    0[100]          ' 100 zero bytes
lookup_table    word    $FFFF[64]       ' 64 words, all $FFFF
scratch_pad     long    0[32]           ' 32 longs of zeros
```

The `[count]` syntax repeats the value. This is your friend for buffers, tables, and anywhere you need initialized storage.

You can even combine values and repetition:

```pasm2
DAT
mixed_init      byte    $AA, $BB, 0[10], $CC, $DD
                '       ^    ^   ^^^^^   ^    ^
                '       Two vals, then 10 zeros, then two more
```

### BYTEFIT and WORDFIT: The Safety Net

Here's a subtle trap. What if you accidentally write:

```pasm2
DAT
oops            byte    1000            ' 1000 won't fit in a byte!
```

The assembler will silently truncate 1000 to 232 (the low 8 bits). Your program will run, but with wrong values. Debugging that is no fun at all.

Enter the safety net:

```pasm2
DAT
safe_byte       bytefit 100, 200, 255   ' OK - all fit in a byte
danger_byte     bytefit 100, 200, 300   ' ERROR! 300 > 255, error!

safe_word       wordfit 1000, 50000     ' OK - all fit in a word
danger_word     wordfit 1000, 70000     ' ERROR! 70000 > 65535
```

Use `BYTEFIT` and `WORDFIT` when you want the assembler to check that your constants actually fit. It's like having a compiler catch your mistakes before they become 3 AM debugging sessions.

### Alignment: Keeping Things Tidy

The P2 is quite forgiving about alignment - it can read a LONG from any address. But aligned access is faster and cleaner. Sometimes you need to force alignment:

```pasm2
DAT
some_bytes      byte    1, 2, 3         ' 3 bytes
                alignw                   ' Align to word boundary
next_word       word    $1234           ' Now properly aligned

more_bytes      byte    "ABC"           ' 3 bytes
                alignl                   ' Align to long boundary
next_long       long    $DEADBEEF       ' Now on a 4-byte boundary
```

When does alignment matter? Mostly when you're:

- Mixing data sizes in the same DAT block
- Creating structures that Spin2 code will access
- Optimizing for maximum hub access speed

If you're just starting out, don't worry about it. Add alignment when you hit problems.

### A Complete Example

Let's put it all together:

```pasm2
DAT             org

' Your code goes here
entry           mov     ptra, ##buffer_addr
                mov     count, #BUFFER_SIZE
.fill           wrbyte  fill_value, ptra++
                djnz    count, #.fill
                jmp     #$

' Constants (read-only, effectively)
fill_value      byte    $55
BUFFER_SIZE     long    256

' Lookup tables
                alignl
sin_table       word    0, 1608, 3212, 4808, 6393   ' Sine table
                word    7962, 9512, 11039, 12540    ' ... continues

' Working storage
                alignl
buffer_addr     long    0               ' Set by Spin2 at startup
temp            long    0
result          long    0

' Reserve uninitialized space
                alignl
scratch         res     16              ' Reserve 16 longs
```

Notice the pattern: code first, then constants, then working storage, then reserved space. This keeps things organized and makes your DAT block readable.

### The Medicine: Quick Reference

| Declaration | Meaning | Example |
|-------------|---------|---------|
| `byte val` | 8-bit value | `byte $FF` |
| `word val` | 16-bit value | `word $1234` |
| `long val` | 32-bit value | `long $DEADBEEF` |
| `val[n]` | Repeat n times | `byte 0[100]` |
| `bytefit` | Byte with range check | `bytefit 100, 200` |
| `wordfit` | Word with range check | `wordfit 1000, 50000` |
| `alignw` | Align to word | (no value) |
| `alignl` | Align to long | (no value) |
| `res n` | Reserve n longs | `res 16` |

### Common Gotchas

1. **Forgetting the label**: Every piece of data needs a label if you want to reference it. Anonymous data just wastes space.

2. **String termination**: `byte "Hello"` doesn't include a null terminator. Add `, 0` if you need one!

3. **RES is in longs**: `res 10` reserves 10 *longs* (40 bytes), not 10 bytes. This trips up everyone at least once.

4. **Alignment after RES**: `res` doesn't affect alignment. If you need alignment after reserved space, add an explicit `alignl` or `alignw`.

### Including External Files: FILE

Sometimes you have binary data sitting in a file - a font bitmap, a sound sample, a pre-computed lookup table. Rather than manually converting it to hex values (ugh!), you can pull it straight in:

```pasm2
DAT
font_data       file    "myfont.bin"        ' Import entire file
sound_sample    file    "beep.raw"          ' Raw audio data
lut_table       file    "precalc.dat"       ' Pre-computed values
```

The assembler reads the file at compile time and drops its raw bytes right into your DAT block. The label gives you a way to reference where the data starts.

**Where does it search?**

1. Same folder as your source file
2. Library paths (if configured)

**Practical example - embedded bitmap:**

```pasm2
DAT             org
entry           mov     ptr, ##@splash_screen
                ' ... display routine using ptr

' The image data lives right here in your code
splash_screen   file    "logo_128x64.bin"   ' 1024 bytes of pixel data
```

No conversion scripts, no copy-paste errors. Just reference the file and it's part of your program. The icing on the cake? If you update the file, recompile, and your program has the new data.

### String and Data Generation Methods

Beyond manually typing values, you have some helpers for creating data:

**@"text" - Inline String Address**

Need a string address without declaring a separate label?

```pasm2
        mov     ptra, @"Hello!"     ' ptra points to "Hello!" in hub
        call    #print_string

        mov     ptra, @"Error: "    ' Another string, inline
        call    #print_string
```

The `@"text"` syntax creates the string in hub memory and gives you its address. It's like an anonymous label for a string constant. Each unique string gets stored once, even if you reference it multiple times.

**STRING("text") and LSTRING("text")**

These work similarly but in different contexts:

```spin2
' In Spin2 code (not PASM):
debug(STRING("Temperature: "))    ' Zero-terminated string address
debug(LSTRING("Status"))          ' Length byte first, then string
```

`STRING()` returns the hub address of a zero-terminated string - same as what C programmers expect. `LSTRING()` puts a length byte at the front, which is handy when you need to know the string length without scanning for null.

**BYTE[], WORD[], LONG[] - Data Arrays**

In Spin2, you can create inline data arrays:

```spin2
' Spin2 examples:
lookup := BYTE[10, 20, 30, 40, 50]    ' Returns address of byte array
config := LONG[$DEAD_BEEF, $CAFE_BABE]
```

These are primarily Spin2 features, but they generate hub data that your PASM code can access if you know the addresses.

**The Pattern:**

| Method | Result | Use Case |
|--------|--------|----------|
| `file "name"` | Raw binary data | Images, audio, lookup tables |
| `@"text"` | String address | Quick inline strings in PASM |
| `STRING("text")` | Zero-terminated string address | Spin2 string constants |
| `LSTRING("text")` | Length-prefixed string | When you need length upfront |

## The Flags: C and Z (and Q!)

Flags are your friends. They remember things:

::: pasm2
```
' Z flag - was the result zero?
        sub     x, y wz        ' Set Z if x-y equals zero
if_z    jmp     #equal         ' Jump if they were equal

' C flag - did we carry/borrow?
        add     x, y wc        ' Set C if addition overflowed
if_c    jmp     #overflow      ' Handle overflow

' Both at once!
        cmp     x, y wcz       ' Compare and set both flags
if_a    jmp     #x_greater     ' Jump if x > y (unsigned)
```
:::

The Q flag is special - it's used by CORDIC operations (Chapter 7).

## Special Instructions That Will Blow Your Mind

### SKIP - The Instruction Skipper

::: pasm2
```
        skip    ##%11010000    ' Skip pattern (1=skip, 0=execute)
        add     x, #1         ' Skipped!
        add     y, #1         ' Skipped!  
        add     z, #1         ' Executed
        sub     a, #1         ' Skipped!
        sub     b, #1         ' Executed
        ' ... pattern continues
```
:::

This is like having conditional execution on steroids!

### REP - Hardware Loops

::: pasm2
```
        rep     #4, #5         ' Repeat next 4 instructions 5 times
        add     x, #1
        sub     y, #1
        rol     z, #1
        ror     w, #1
        ' These 4 instructions execute 5 times total
        ' No loop overhead!
```
:::

### ALTD/ALTS - Instruction Modification

::: pasm2
```
' Modify the next instruction's destination
        mov     index, #10
        altd    index, #array  ' Next instruction's dest = array+10
        mov     0-0, value     ' Actually moves to array[10]!
```
:::

This replaces self-modifying code from P1. Much cleaner!

## Real-World Example: Fast Memory Copy

Let's combine what we've learned:

::: pasm2
```
' Fast block copy using REP
fast_copy
        mov     ptra, ##source_addr    ' Source pointer
        mov     ptrb, ##dest_addr      ' Destination pointer
        
        rep     #2, ##256              ' Repeat 256 times
        rdlong  temp, ptra++           ' Read and increment
        wrlong  temp, ptrb++           ' Write and increment
        ' 1024 bytes (256 longs) copied with no loop overhead!
        
temp    long    0
```
:::

::: medicine-cabinet
Feeling overwhelmed? Here's your simplified prescription:

**Minimum Instructions to Know**

::: pasm2
```
' Moving data
        mov     dest, source   ' Copy data

' Math
        add     dest, source   ' Addition
        sub     dest, source   ' Subtraction

' Logic
        and     dest, source   ' AND operation
        or      dest, source   ' OR operation

' Flow
        jmp     #label         ' Jump
        call    #label         ' Call subroutine
        ret                    ' Return

' Flags
        cmp     x, y wcz       ' Compare and set flags
  if_z  jmp     #label         ' Conditional jump
```
:::

Master these 10 instructions and you can write real programs!
:::

## Common Gotchas

1. **Immediate values**: 
   - `#value` for 9-bit immediates (0-511)
   - `##value` for 32-bit immediates
   - Forgetting # uses the register at that address!

2. **Flag confusion**:
   - `wz` sets Z flag, `wc` sets C flag, `wcz` sets both
   - No flag update means flags unchanged

3. **PTRA/PTRB are special**:

::: pasm2
```
   rdlong  x, ptra++      ' Read and auto-increment
   rdlong  x, ++ptra      ' Pre-increment then read
   rdlong  x, ptra--      ' Read and auto-decrement
   rdlong  x, ptra[5]     ' Read from ptra + 5*4
```
:::

4. **Address confusion**:
   - COG addresses are in longs (0-511)
   - Hub addresses are in bytes (0-524287)

## Your Turn: Experiments

### Experiment 1: Conditional Counter
Count up if button pressed, down if not:

::: pasm2
```
        org     0
        
.loop   testp   #BUTTON_PIN wc ' Test button
if_c    add     counter, #1    ' Increment if pressed
if_nc   sub     counter, #1    ' Decrement if not

        wrlong  counter, ##HUB_ADDR ' Display count
        waitx   ##1_000_000
        jmp     #.loop
        
counter long    0
```
:::

### Experiment 2: Pattern Matcher
Find a pattern in data:

::: pasm2
```
        org     0
        
        mov     pattern, ##$DEADBEEF
        mov     ptra, ##data_start
        
.search rdlong  value, ptra++
        cmp     value, pattern wz
if_z    jmp     #.found
        cmp     ptra, ##data_end wcz
if_b    jmp     #.search
        jmp     #.not_found

.found  ' Pattern found!
        drvh    #SUCCESS_LED
        jmp     #$

.not_found
        drvh    #FAIL_LED
        jmp     #$
```
:::

### Experiment 3: Speed Test
Compare multiply methods:

::: pasm2
```
' Method 1: Hardware multiply
        getct   start_time
        mul     x, y
        getct   end_time
        sub     end_time, start_time
        ' Result: 2 clocks!
        
' Method 2: Shift and add (old school)
        getct   start_time
        ' ... shift/add loop here
        getct   end_time
        ' Result: Many more clocks!
```
:::

::: sidetrack
### Why PASM2 Is Different

Most assembly languages are thin wrappers over hardware. PASM2 is different - it's designed for humans:

1. **Symmetry**: Every instruction can use every addressing mode
2. **Orthogonality**: Features combine predictably
3. **Conditional everything**: Not just jumps, ANY instruction
4. **No special cases**: General-purpose registers, no accumulator

This isn't accident - it's philosophy. The P2 was designed to make assembly programming pleasant.
:::

## What We've Learned

- ✅ Instruction anatomy and structure
- ✅ Basic data movement and math
- ✅ Hardware multiply and divide (!)
- ✅ Conditional execution on any instruction
- ✅ Special instructions (SKIP, REP, ALT*)
- ✅ Flag operations and testing
- ✅ Why PASM2 is human-friendly

## Coming Up Next

Chapter 4, "The Hub Connection", explores:

- Reading and writing hub memory
- The FIFO and fast block transfers
- Hub execution mode
- Sharing data between COGs

You now speak basic PASM2. Time to learn how COGs communicate!


**Have Fun!** Remember, PASM2 isn't like other assembly languages - it's actually enjoyable!


*Continue to [Chapter 4: The Hub Connection](04-hub-connection.md) →*


# Chapter 4: The Hub Connection

*How COGs share and care*

## The Hook: Instant Communication

::: pasm2
```
' COG 1: Leave a message
        wrlong  ##$DEADBEEF, ##$1000
        
' COG 2: Get the message
        rdlong  message, ##$1000
        ' message now contains $DEADBEEF!
```
:::

That's it - COGs talking through hub memory. But there's so much more...

## Reading from Hub

The basics are simple:

::: pasm2
```
        rdbyte  value, hubaddr    ' Read 1 byte
        rdword  value, hubaddr    ' Read 2 bytes (word)
        rdlong  value, hubaddr    ' Read 4 bytes (long)
        
' With PTRA/PTRB magic
        rdlong  value, ptra++     ' Read and increment pointer
        rdlong  value, ++ptra     ' Increment then read
        rdlong  value, ptra[5]    ' Read from ptra + 5*4
```
:::

## Writing to Hub

Just as easy:

::: pasm2
```
        wrbyte  value, hubaddr    ' Write 1 byte
        wrword  value, hubaddr    ' Write 2 bytes
        wrlong  value, hubaddr    ' Write 4 bytes
        
' The mighty block transfer
        setq    #16-1             ' Transfer 16 longs
        rdlong  buffer, hubaddr   ' Reads 16 longs in one go!
```
:::

## The FIFO Pipeline

Here's where P2 gets serious about speed:

::: pasm2
```
' Start the FIFO
        rdfast  #0, ##data_start  ' Start fast read
        
' Now read at maximum speed
.loop   rflong  value            ' Read from FIFO
        ' Process value
        djnz    count, #.loop    ' Decrement and jump if not zero
        
' No hub timing worries - FIFO handles it all!
```
:::

## Real-World Example: Video Buffer

::: pasm2
```
' Fast screen clear using block transfer
' Note: SETQ/SETQ2 maximum is 511 (for 512 longs)
' For larger fills, we loop in 512-long chunks
clear_screen
        mov     hub_ptr, ##screen_buffer
        mov     chunks, ##640*480/512   ' Number of 512-long chunks
        mov     color, ##$00_00_00_00   ' Black

.loop   setq    #512-1                  ' Transfer 512 longs (max)
        wrlong  color, hub_ptr          ' Fill this chunk
        add     hub_ptr, ##512*4        ' Advance 512 longs (2KB)
        djnz    chunks, #.loop
        ' Full screen cleared with minimal loop overhead!
```
:::

::: medicine-cabinet
**Simple hub access pattern**:

::: pasm2
```
' Just use PTRA for everything
        mov     ptra, ##hub_address
        rdlong  value, ptra++
        ' That's all you really need!
```
:::
:::

*Continue to [Chapter 5: Mathematics Unleashed](05-mathematics-unleashed.md) →*


# Chapter 5: Mathematics Unleashed

*Hardware multiply and divide - finally!*

## The Hook: Hardware Multiply

::: pasm2
```
        mul     x, y              ' 16x16->32 bit unsigned multiply
        ' Result in x (lower 16 bits of each operand used)

        ' For full 32x32->64 bit multiply, use CORDIC:
        qmul    x, y              ' Start 32x32->64 multiply
        ' ... other work (54 clocks) ...
        getqx   low               ' Get lower 32 bits
        getqy   high              ' Get upper 32 bits
```
:::

Remember doing this with shifts and adds? Those days are over!

## The Multiplication Revolution

::: pasm2
```
' Unsigned multiply
        mul     result, value     ' result = low 32 bits
        
' Signed multiply  
        muls    result, value     ' Signed version
        
' Scale and multiply
        scl     result, ##$8000   ' Scale by 0.5 (32.32 fixed pt)
```
:::

## Division Without Tears

::: pasm2
```
' Start division
        qdiv    dividend, divisor ' Start the operation
        
' Get results (takes 30 clocks)
        getqx   quotient         ' Get quotient
        getqy   remainder        ' Get remainder
        
' Fractional division
        qfrac   numerator, denominator
        getqx   fraction         ' 32-bit fraction
```
:::

## 64-Bit Operations

::: pasm2
```
' 64-bit add
        add     low1, low2 wc
        addx    high1, high2

' 64-bit multiply (uses CORDIC)
        qmul    x, y           ' Start 32x32->64 multiply
        ' ... 54 clocks ...
        getqx   low            ' Lower 32 bits
        getqy   high           ' Upper 32 bits
```
:::

## Real-World Example: Fixed-Point Math

::: pasm2
```
' 16.16 fixed point multiply (uses CORDIC for full precision)
fixed_mul
        qmul    a, b             ' Start 32x32->64 signed multiply
        ' ... 54 clocks (do other work) ...
        getqx   low              ' Lower 32 bits
        getqy   high             ' Upper 32 bits
        ' Extract middle 32 bits for 16.16 result:
        shl     high, #16        ' Upper 16 bits of result
        shr     low, #16         ' Lower 16 bits of result
        or      a, low, high     ' Combine for 16.16 format
```
:::


*Continue to [Chapter 6: Flags and Decisions](06-flags-decisions.md) →*


# Chapter 6: Flags and Decisions

*Making choices at machine speed*

## The Hook: Any Instruction Can Be Conditional

::: pasm2
```
        cmp     x, y wcz         ' Compare x and y
if_a    mov     result, x        ' If x > y, result = x
if_be   mov     result, y        ' If x <= y, result = y
        ' Max function in 3 instructions!
```
:::

## The C and Z Flags

::: pasm2
```
' Z Flag - Zero detection
        sub     x, y wz          ' Z=1 if x equals y
if_z    jmp     #equal          ' Jump if equal

' C Flag - Carry/Borrow
        add     x, y wc          ' C=1 if overflow
if_c    jmp     #overflow       ' Handle overflow
```
:::

## Complex Conditions

::: pasm2
```
' Combining flags
        cmp     x, y wcz
if_a    jmp     #greater        ' x > y (unsigned)
if_b    jmp     #less           ' x < y (unsigned)
if_z    jmp     #equal          ' x == y

' Signed comparisons
        cmps    x, y wcz        ' Signed compare
if_gt   jmp     #greater        ' x > y (signed)
if_lt   jmp     #less           ' x < y (signed)
```
:::

## Skip Patterns - Conditional Blocks

::: pasm2
```
        skipf   pattern          ' Set skip pattern
        add     x, #1           ' Maybe executed
        sub     y, #1           ' Maybe executed
        mov     z, #0           ' Maybe executed
        ' Pattern determines what runs!
```
:::


*Continue to [Chapter 7: CORDIC Magic](07-cordic-magic.md) →*



# Chapter 7: CORDIC Magic


*Trigonometry at the speed of logic gates*

## The Hook: Rotate a Point in 3 Lines

Here's something that would take dozens of instructions on most processors:

::: pasm2
```
' Rotate point (x,y) by angle - that's it!
        setq    y_coord         ' Set Y coordinate
        qrotate x_coord, angle  ' Start rotation by angle
        getqx   new_x          ' Get rotated X (55 clocks later)
        getqy   new_y          ' Get rotated Y
```
:::

Three instructions. Point rotated. No lookup tables, no approximations, no floating point. Just pure mathematical precision delivered by dedicated hardware.

Let me show you something even more impressive:

::: pasm2
```
' Calculate sine and cosine simultaneously
        qrotate ##$7FFF_FFFF, angle  ' D=radius (max), S=angle
        getqx   cosine               ' cos(angle) in 2.30 fixed pt
        getqy   sine                 ' sin(angle) in 2.30 fixed pt
        ' Both trig functions in 55 clocks total!
```
:::

## What Just Happened?

CORDIC stands for COordinate Rotation DIgital Computer. It's a method invented in 1959 for calculating trigonometric functions using only shifts and adds - no multiplies needed! Each P2 COG has its own dedicated CORDIC unit built into the hardware.

Think of CORDIC as your mathematical co-processor that can:

- Rotate points around the origin
- Convert between rectangular and polar coordinates  
- Calculate sine, cosine, tangent
- Compute square roots and magnitudes
- Find arctangent (angle between points)
- Even do logarithms and exponentials!

All of this in exactly 55 clock cycles. Every time. No variation.

## The CORDIC Pipeline - Your Mathematical Assembly Line

Here's the beautiful part: CORDIC operations are pipelined. While one calculation is running, you can start another:

::: pasm2
```
' Generate sine wave samples rapid-fire
        mov     angle, #0
        mov     count, #256

generate
        qrotate ##$7FFF_FFFF, angle   ' D=radius, S=angle
        add     angle, ##$0100_0000   ' Increment angle (no wait!)
        
        ' Do other work while CORDIC calculates
        add     sample_ptr, #4
        sub     count, #1
        
        getqy   sample               ' Get sine result
        wrlong  sample, sample_ptr   ' Store it
        
        tjnz    count, #generate     ' Test-jump-not-zero
        ' Generated 256 samples with perfect overlap!
```
:::

The pipeline means you're not really waiting 55 clocks - you're getting useful work done while CORDIC churns away in the background!

## Core CORDIC Operations

### QROTATE - The Rotation Engine

Here's a subtle detail: CORDIC operations work on 2D coordinates (X, Y), but the **QROTATE** instruction only takes one coordinate directly. The solution? **SETQ** loads the Y coordinate into the Q register, then **QROTATE** takes X from its first operand. It's a two-instruction dance that becomes second nature:

::: pasm2
```
' Basic rotation: rotate point (x,y) by angle
        setq    y              ' First: load Y into Q register
        qrotate x, angle       ' Then: X from operand, Y from Q
        getqx   new_x          ' Result: X' = X*cos(θ) - Y*sin(θ)
        getqy   new_y          ' Result: Y' = X*sin(θ) + Y*cos(θ)
```
:::

The angle format is special: it's a 32-bit unsigned value where:

- $0000_0000 = 0 degrees
- $4000_0000 = 90 degrees  
- $8000_0000 = 180 degrees
- $C000_0000 = 270 degrees
- $FFFF_FFFF = just under 360 degrees

This makes angle math incredibly easy - just use regular addition and subtraction!

### QVECTOR - From Rectangular to Polar

::: pasm2
```
' Convert (x,y) to polar (radius, angle)
        setq    y              ' Load Y coordinate
        qvector x, #0          ' Start conversion
        getqx   radius         ' sqrt(x² + y²)
        getqy   angle          ' atan2(y, x)
```
:::

Perfect for:

- Finding distances between points
- Converting joystick input to angle/magnitude
- Radar and sonar applications

### The Power of 32-Bit Precision

CORDIC uses 32-bit precision throughout:

- Angles: 32 bits (0.0000084 degree resolution!)
- Coordinates: 32 bits signed
- Results: Full 32-bit or 64-bit when needed

## Real-World Example: Spinning a Sprite

Let's rotate a sprite around its center:

::: pasm2
```
' Rotate sprite vertices around center
rotate_sprite
        mov     vertex_ptr, ##sprite_data
        mov     vertex_count, #4        ' 4 corners
        
next_vertex
        rdlong  x, vertex_ptr++        ' Get X coordinate
        rdlong  y, vertex_ptr++        ' Get Y coordinate
        
        ' Center sprite at origin
        sub     x, center_x
        sub     y, center_y
        
        ' Rotate by current angle
        setq    y
        qrotate x, rotation_angle
        
        ' While waiting, we can prepare
        mov     temp_x, center_x
        mov     temp_y, center_y
        
        ' Get rotated coordinates
        getqx   x
        getqy   y
        
        ' Translate back to position
        add     x, temp_x
        add     y, temp_y
        
        ' Store rotated vertex
        wrlong  x, vertex_ptr++
        wrlong  y, vertex_ptr++
        
        djnz    vertex_count, #next_vertex
        
        ' Increment rotation for animation
        add     rotation_angle, ##$0100_0000  ' ~1.4 deg (1/256 rotation)
```
:::

## Your Turn: CORDIC Experiments

:::yourturn
**Your Turn:** Create a circular motion pattern

Starting code:

::: pasm2
```
        org     0
        
        mov     angle, #0
        mov     radius, ##100          ' 100 pixel radius

.loop   qrotate radius, angle         ' D=X (radius), S=angle
        ' Add code to:
        ' 1. Get X,Y coordinates
        ' 2. Add screen center offset
        ' 3. Draw pixel at that position
        ' 4. Increment angle
        ' 5. Loop back to .loop
```
:::

Goal: Make a dot trace a perfect circle on screen
Hint: After qrotate, use getqx/getqy to get coordinates
Success Check: Smooth circular motion, no gaps
:::

:::yourturn  
**Your Turn:** Distance calculator

Starting code:

::: pasm2
```
' Calculate distance between two points
        mov     x1, #10
        mov     y1, #20
        mov     x2, #40
        mov     y2, #60
        
        ' Calculate differences
        sub     x2, x1         ' dx
        sub     y2, y1         ' dy
        
        ' Your code here: use qvector to find distance
```
:::

Goal: Calculate the distance between the two points
Hint: qvector with Y in Q gives you radius (distance)
Success Check: Distance should be 50 units
:::

::: medicine-cabinet
Feeling overwhelmed by all this trigonometry? Here's your simplified prescription:

**Too Complex?** Just remember these three patterns:

**Pattern 1: Get sine/cosine**

::: pasm2
```
        qrotate ##$7FFF_FFFF, angle    ' D=radius, S=angle
        getqx   cos_value
        getqy   sin_value
```
:::

**Pattern 2: Rotate a point**

::: pasm2
```
        setq    y
        qrotate x, angle
        getqx   new_x
        getqy   new_y
```
:::

**Pattern 3: Get distance**

::: pasm2
```
        setq    dy
        qvector dx, #0
        getqx   distance
```
:::

Master these three and you can do 90% of what you need!
:::

## Advanced CORDIC: The Pipeline Dance

Here's where CORDIC gets really powerful - overlapping operations:

::: pasm2
```
' Process multiple points while calculating
process_points
        mov     count, #16
        mov     ptra, ##point_array
        
        ' Start first calculation
        rdlong  x, ptra++
        rdlong  y, ptra++
        setq    y
        qrotate x, angle
        
process_loop
        ' Start next calculation immediately
        rdlong  x, ptra++ wz    ' Z flag tells us if done
   if_nz rdlong  y, ptra++
   if_nz setq    y
   if_nz qrotate x, angle        ' New calculation starts
        
        ' Get previous result
        getqx   prev_x
        getqy   prev_y
        
        ' Store previous result
        wrlong  prev_x, ptrb++
        wrlong  prev_y, ptrb++
        
        djnz    count, #process_loop
        
        ' Don't forget last result!
        getqx   prev_x
        getqy   prev_y
        wrlong  prev_x, ptrb++
        wrlong  prev_y, ptrb++
```
:::

See what happened? We started each new CORDIC operation immediately after the previous one, then retrieved results later. This pipeline approach means we're effectively getting one rotation every few instructions instead of waiting 55 clocks each time!

## CORDIC for Graphics

Want to draw a spiral? CORDIC makes it trivial:

::: pasm2
```
' Expanding spiral generator
spiral
        mov     angle, #0
        mov     radius, #1

draw_spiral
        qrotate radius, angle         ' D=X (radius), S=angle
        getqx   x
        getqy   y
        
        ' Convert to screen coordinates
        sar     x, #16          ' Scale down
        sar     y, #16
        add     x, #320         ' Center X
        add     y, #240         ' Center Y
        
        ' Plot pixel (simplified)
        call    #plot_pixel
        
        ' Expand spiral
        add     angle, ##$0400_0000   ' Rotate ~22.5 degrees
        add     radius, ##100         ' Expand slowly
        
        cmp     radius, ##30000 wcz
   if_b jmp     #draw_spiral
```
:::

## CORDIC for Audio

Generate perfect sine waves for audio:

::: pasm2
```
' Audio tone generator using CORDIC
tone_generator
        mov     phase, #0
        mov     frequency, ##$0100_0000  ' ~1.4 deg/sample (1/256 rot)
        
sample_loop
        qrotate ##$7FFF_FFFF, phase     ' D=radius, S=angle
        add     phase, frequency        ' Increment phase
        
        ' Do other audio processing while waiting
        rdlong  volume, ##volume_addr
        
        getqy   sample                  ' Get sine value
        sar     sample, #16             ' Scale to 16-bit
        muls    sample, volume          ' Apply volume
        
        ' Output to DAC
        wypin   sample, #AUDIO_PIN
        
        ' Wait for sample period (48kHz)
        waitx   ##4166                  ' 200MHz / 48kHz
        
        jmp     #sample_loop
```
:::

## Common CORDIC Gotchas

Before you pull your hair out debugging, know these:

1. **One result at a time** - Each COG has its own CORDIC, but starting a new operation before retrieving your result overwrites it!

2. **55 clocks is exact** - Not 54, not 56. Always exactly 55 clocks from operation start to result ready.

3. **Don't forget SETQ** - For two-operand operations (QROTATE with X,Y), you must load Y into Q first.

4. **Results are scaled** - When rotating by unit circle ($7FFF_FFFF), results are in 2.30 fixed point format.

5. **Angles wrap naturally** - Adding $1_0000_0000 to an angle is the same as adding 0. Use this!

## What About QLOG, QEXP?

CORDIC can also do logarithms and exponentials:

::: pasm2
```
' Natural logarithm
        qlog    value
        getqx   result          ' ln(value) in 5.27 fixed point
        
' Exponential
        qexp    value  
        getqx   result          ' e^value
```
:::

These are less commonly used but incredibly powerful for DSP and scientific calculations.

:::interlude
**Jack Volder's Gift to Computing**

In 1959, Jack Volder was working on navigation computers for aircraft. He needed to calculate trigonometric functions, but the computers of the day couldn't handle the complex math quickly enough.

His insight? Any angle can be decomposed into a sequence of smaller, fixed angles. By choosing these angles cleverly (arctan of powers of 2), he could rotate vectors using only shifts and adds - no multiplication needed!

The B-58 bomber's navigation computer was the first to use CORDIC. Today, it's in your P2, calculating sines and cosines faster than those room-sized computers could add two numbers.

From military navigation to your LED projects - quite a journey for an algorithm!
:::

## What We've Learned

Let's celebrate your new CORDIC powers:

- ✅ Understood CORDIC's rotate and vector operations
- ✅ Generated sine and cosine values
- ✅ Calculated distances and angles
- ✅ Learned the pipeline technique for speed
- ✅ Created rotating graphics
- ✅ Built an audio tone generator

That's serious mathematical muscle!

## Coming Up Next

Chapter 8 brings us back to Earth with "Basic I/O" - the fundamental pin operations that make the real world connection. We'll save Smart Pins for another manual and focus on the essentials: making pins go high and low, reading buttons, and basic timing.

But first, take a moment to appreciate what you just learned. CORDIC is unique to the Propeller 2 - most microcontrollers would need extensive software libraries to do what you just did in three instructions!


**Have Fun!** And remember - with CORDIC, you're not just calculating trigonometry, you're doing it at hardware speed. That's magical!


# Chapter 8: Basic I/O

*Making the real world connection*

## The Hook: One Pin, Three Instructions, Infinite Possibilities

Watch this:

::: pasm2
```
' Complete button-and-LED program
.loop   testp   #BUTTON_PIN wc  ' Read button into C flag
   if_c drvh    #LED_PIN        ' If pressed, LED on
  if_nc drvl    #LED_PIN        ' If not pressed, LED off
        jmp     #.loop          ' Repeat forever
```
:::

Four lines. Complete input/output program. No configuration registers, no data direction setup, no port manipulation. Just pure, simple I/O.

But wait, let me show you the same thing with even more elegance:

::: pasm2
```
' Even simpler - button controls LED directly
.loop   testp   #BUTTON_PIN wc  ' Read button
        drvc    #LED_PIN        ' Drive LED from C flag!
        jmp     #.loop
```
:::

Three lines! The `drvc` instruction drives the pin to match the C flag. Input becomes output. Simple becomes simpler.

## Understanding P2 Pins

Every P2 pin is bidirectional and incredibly capable. Unlike older microcontrollers where you set data direction registers, P2 pins change direction on the fly based on the instruction you use.

Here's the mental model:

- **Output instructions** automatically make the pin an output
- **Input instructions** automatically make the pin an input  
- **Float instructions** make the pin high-impedance
- No setup required!

## Digital Output: Making Things Happen

### The Fundamental Four

::: pasm2
```
        drvh    #56            ' Drive pin 56 HIGH (3.3V)
        drvl    #56            ' Drive pin 56 LOW (0V)
        drvnot  #56            ' Toggle pin 56
        fltl    #56            ' Float pin 56 (high-Z)
```
:::

That's it. These four instructions cover 90% of your output needs.

### Conditional Driving

Here's where P2 gets clever:

::: pasm2
```
        drvc    #56            ' Drive pin to match C flag
        drvnc   #56            ' Drive pin to NOT C flag
        drvz    #56            ' Drive pin to match Z flag
        drvnz   #56            ' Drive pin to NOT Z flag
```
:::

And the really clever one:

::: pasm2
```
        drvnot  #56 wcz        ' Toggle pin AND read old state to C
        ' C now contains what the pin WAS before toggling
```
:::

### Random and Pattern Outputs

::: pasm2
```
        drvrnot #56            ' Randomly toggle (hardware random!)
        outl    #56            ' Drive low (alternate form)
        outh    #56            ' Drive high (alternate form)
```
:::

## Digital Input: Reading the World

### Basic Pin Reading

::: pasm2
```
        testp   #BUTTON_PIN wc ' Read pin into C flag
   if_c jmp     #pressed       ' Branch if high
  if_nc jmp     #not_pressed   ' Branch if low
```
:::

Or read into Z flag for zero/non-zero testing:

::: pasm2
```
        testp   #SENSOR_PIN wz ' Read pin into Z flag  
   if_z jmp     #sensor_low    ' Jump if pin low (Z=1 when pin=0)
  if_nz jmp     #sensor_high   ' Jump if pin is high
```
:::

### Reading Multiple Pins

::: pasm2
```
' Read 8 pins at once (pins 0-7)
        mov     mask, #$FF     ' Pins 0-7
        testb   ina, #0 wc     ' Test pin 0
        rcl     result, #1     ' Rotate C into result
        testb   ina, #1 wc     ' Test pin 1
        rcl     result, #1
        ' ... continue for all 8 pins
```
:::

## Pin Timing: When Things Happen

### Waiting for Pin Changes

::: pasm2
```
' Wait for pin to go high
wait_high
        testp   #SIGNAL_PIN wc
  if_nc jmp     #wait_high
        
' Wait for pin to go low  
wait_low
        testp   #SIGNAL_PIN wc
   if_c jmp     #wait_low
```
:::

But there's a better way - hardware-assisted waiting with Smart Events:


::: pasm2
```
        waitse1               ' Wait for event 1
        waitse2               ' Wait for event 2
        ' Configure events to watch pins - super efficient!
```
:::

## Real-World Example: Button Debouncing

Mechanical buttons bounce. Here's how to handle it:

::: pasm2
```
' Debounced button reader
read_button
        mov     debounce, #0
        
check_button
        testp   #BUTTON_PIN wc
   if_c add     debounce, #1    ' Count high readings
  if_nc mov     debounce, #0    ' Reset on any low
        
        cmp     debounce, #10 wcz ' Need 10 consecutive highs
  if_ae jmp     #button_confirmed
        
        waitx   ##200_000        ' Wait 1ms at 200MHz
        jmp     #check_button
        
button_confirmed
        ' Button definitely pressed
        drvh    #LED_PIN
```
:::

## Bit-Banged Serial (The Basics)

Sometimes you need serial communication without Smart Pins. Here's how:

::: pasm2
```
' Bit-bang serial transmit at 115200 baud
tx_byte
        or      data, ##$100    ' Add stop bit
        shl     data, #1        ' Add start bit (0)
        mov     bits, #10       ' 1 start + 8 data + 1 stop
        
        getct   time            ' Get current time
        
tx_loop
        shr     data, #1 wc     ' Get next bit into C
        drvc    #TX_PIN         ' Output bit
        
        addct1  time, bit_time  ' Next bit time
        waitct1                 ' Wait for it
        
        djnz    bits, #tx_loop
        ret
        
bit_time long   100_000_000 / 115200  ' Clock cycles per bit
```
:::

## Your Turn: I/O Experiments

:::yourturn
**Your Turn:** Create a light chaser

Starting code:

::: pasm2
```
        org     0
        
        mov     pattern, #1     ' Start with one LED
        
.loop   mov     pins, pattern   ' Your code here
        ' Make pattern rotate through pins 56-63
        ' Add delay between changes
        ' Wrap around at the end, then jmp #.loop
```
:::

Goal: Create a rotating light pattern on LEDs
Hint: Use SHL and check for overflow
Success Check: Single lit LED rotating through all positions
:::

:::yourturn
**Your Turn:** Reaction timer

Starting code:

::: pasm2
```
        org     0
        
        ' Turn on LED after random delay
        getrnd  delay
        and     delay, ##$3FFF_FFFF  ' Limit range
        waitx   delay
        drvh    #LED_PIN
        
        getct   start_time
        ' Your code: wait for button press
        ' Calculate reaction time
```
:::

Goal: Measure reaction time between LED and button press
Hint: Use getct after button detection
Success Check: Time measured in clock cycles
:::

::: medicine-cabinet
Feeling overwhelmed by all these pin operations? Here's the simplified prescription:

**Just need something working?** Remember these patterns:

**Output pattern:**

::: pasm2
```
        drvh    #PIN    ' Make it high
        drvl    #PIN    ' Make it low
        drvnot  #PIN    ' Toggle it
```
:::

**Input pattern:**

::: pasm2
```
        testp   #PIN wc ' Read it
   if_c jmp     #high  ' It's high
  if_nc jmp     #low   ' It's low
```
:::

**Timed pattern:**

::: pasm2
```
.loop   drvnot  #LED
        waitx   ##50_000_000
        jmp     #.loop
```
:::

That's 80% of all I/O right there!
:::

## Advanced Pin Control

### Pin Groups

You can control multiple pins at once:

::: pasm2
```
        drvh    #LED_BASE addpins 3  ' Drive 4 pins high (base+3)
        drvl    #LED_BASE addpins 7  ' Drive 8 pins low
```
:::

### Direct Pin Manipulation

For when you need absolute control:

::: pasm2
```
        mov     outa, pattern    ' Set output register directly
        mov     dira, ##$FF      ' Set direction reg (rare in P2!)
```
:::

But honestly? You'll rarely need these. The individual pin instructions are cleaner and clearer.

## Common I/O Gotchas

Save yourself debugging time:

1. **Pin numbers are 0-63** - Not port.bit notation like other MCUs

2. **No pullup/pulldown by default** - Use external resistors or configure Smart Pin modes (advanced topic)

3. **Pins float on reset** - All pins start as inputs (floating)

4. **Reading output pins** - You CAN read a pin you're driving (reads the actual pin state)

5. **3.3V logic levels** - P2 is 3.3V, not 5V tolerant!

## Timing Is Everything

Here's a critical concept: P2 I/O is deterministic. When you execute:

::: pasm2
```
        drvh    #56
        drvl    #57
```
:::

Pin 56 goes high and pin 57 goes low at EXACTLY the same clock cycle. No skew, no uncertainty. This determinism is what makes P2 perfect for precise timing applications.

## Real-World Example: Servo Control

Even without Smart Pins, controlling a servo is easy:

::: pasm2
```
' Standard servo control (1-2ms pulse every 20ms)
servo_control
        mov     position, ##300_000    ' 1.5ms = center at 200MHz

servo_loop
        drvh    #SERVO_PIN
        waitx   position              ' 1-2ms high pulse
        drvl    #SERVO_PIN
        waitx   ##4_000_000          ' Rest of 20ms at 200MHz

        ' Adjust position as needed
        rdlong  position, ##position_addr
        fle     position, ##200_000   ' Limit to 1ms min
        fge     position, ##400_000   ' Limit to 2ms max
        
        jmp     #servo_loop
```
:::

## The Power of Simple

Here's something beautiful about P2's I/O philosophy: it's transparent. Unlike microcontrollers with complex GPIO configurations, port multiplexing, and alternate functions, P2 pins just... work.

Want an output? Drive it.
Want an input? Read it.
Want it to float? Float it.

No setup, no configuration, no confusion.

## What We've Learned

Look at your new I/O skills:

- ✅ Understood P2's automatic pin direction
- ✅ Mastered the four fundamental output instructions
- ✅ Learned pin reading and conditional testing
- ✅ Created debounced inputs
- ✅ Built bit-banged serial
- ✅ Discovered deterministic timing

## A Note About Smart Pins

You might wonder - if basic I/O is this simple, why do we need Smart Pins?

Well, while you CAN bit-bang serial at 115200 baud, or generate PWM, or measure frequencies using the techniques in this chapter, Smart Pins do all of this in hardware, freeing your COG for more important work.

📚 **For Smart Pin details**: See the dedicated "P2 Smart Pins Manual" which covers all 64 modes, from simple PWM to complex protocol generation. Smart Pins deserve their own complete treatment!

## Coming Up Next

Chapter 9 takes us into "Streaming Data" - the P2's incredible FIFO system that can move megabytes of data without breaking a sweat. We'll see how to stream video, audio, and massive data blocks at maximum speed.


**Have Fun!** Remember, every embedded system ultimately comes down to pins going high and low. You've just mastered the fundamentals that everything else builds upon!


# Chapter 9: Streaming Data

*Moving mountains of data without breaking a sweat*

## The Hook: 4KB in 4 Instructions

Watch this data transfer magic:

::: pasm2
```
' Copy 1000 longs (4KB) at maximum speed
        setq    ##1000-1        ' Setup for 1000 longs
        rdlong  buffer, source  ' Read them all!
        setq    ##1000-1        ' Setup for 1000 longs  
        wrlong  buffer, dest    ' Write them all!
        ' 4KB moved in microseconds!
```
:::

Four instructions. Four kilobytes. Faster than DMA on most processors. And we're just getting started...

## Block Transfers: The Power Move

The SETQ instruction is your gateway to block transfers:

::: pasm2
```
' Basic block read
        setq    #16-1           ' Transfer 16 longs (minus 1!)
        rdlong  buffer, hubaddr ' Reads 16 consecutive longs
        
' Basic block write
        setq    #16-1           ' Transfer 16 longs
        wrlong  buffer, hubaddr ' Writes 16 consecutive longs
```
:::

The key insight: SETQ tells the next hub instruction how many longs to transfer. The "-1" is because it's a count from 0.

## The FIFO: Your Streaming Pipeline

The FIFO (First In, First Out) is P2's streaming engine. Think of it as a conveyor belt between hub memory and your COG:

::: pasm2
```
' Start FIFO reading
        rdfast  #0, ##data_start  ' Start fast read at data_start
        
' Now read data at maximum speed
stream_loop
        rflong  value            ' Read from FIFO (no waiting!)
        ' Process value here
        add     accumulator, value
        djnz    count, #stream_loop
        
' The FIFO keeps feeding data automatically
```
:::

The beauty? The FIFO reads ahead automatically. While you're processing one value, it's already fetching the next. No hub timing slots to worry about!

## Writing Through the FIFO

::: pasm2
```
' Start FIFO writing  
        wrfast  #0, ##dest_buffer
        
' Stream data out
write_loop
        ' Generate or process data
        mov     value, calculation
        wflong  value            ' Write to FIFO
        djnz    count, #write_loop
        
' Data streams to hub automatically
```
:::

## Real-World Example: Screen Buffer Clear

Let's clear a 320x240x4 byte screen buffer (~307KB - fits in hub!):

::: pasm2
```
' Ultra-fast screen clear
clear_screen
        mov     color, ##$00_00_00_00    ' Black (4 bytes per pixel)
        mov     pixels, ##320*240        ' 76,800 pixels

        wrfast  #0, ##screen_buffer      ' Start FIFO write

clear_loop
        wflong  color                    ' Write 4-byte pixel
        djnz    pixels, #clear_loop

        ' 307KB cleared at maximum hub speed!
        ' Note: Hub RAM is 512KB - plan buffer sizes accordingly
```
:::

## Streaming with the Streamer

The Streamer is different from the FIFO - it's a dedicated DMA engine that can move data between hub memory and pins:

::: pasm2
```
' Configure streamer for video output
        setcmod #$100           ' Set color mode
        setcy   ##640           ' Cycles per line
        setci   ##LINE_TIME     ' Line timing
        
' Start streaming video data to pins
        xinit   ##STREAM_CMD, #0  ' Start streamer
        ' Data flows from hub to pins automatically!
```
:::

## FIFO and COG Execution

Here's something amazing - you can execute code from hub through the FIFO:

::: pasm2
```
' Execute large program from hub
        orgh    $1000           ' Code in hub memory
        
hub_code
        ' This code is in hub but executes like it's in COG
        add     x, y
        sub     a, b
        ' Can be megabytes of code!
```
:::

When you call or jump to hub code, the FIFO automatically feeds instructions to the COG. It's like having unlimited code space!

::: medicine-cabinet
Feeling overwhelmed by all this streaming? Here's your prescription:

**Just need to move data?** Use these simple patterns:

**Block read pattern:**

::: pasm2
```
        setq    #SIZE-1
        rdlong  buffer, source
```
:::

**Block write pattern:**

::: pasm2
```
        setq    #SIZE-1
        wrlong  buffer, dest
```
:::

**FIFO read pattern:**

::: pasm2
```
        rdfast  #0, ##source
.loop   rflong  value
        ' Process value
        djnz    count, #.loop
```
:::

That's 90% of streaming right there!
:::

## Advanced Streaming Techniques

### Circular Buffers with FIFO

::: pasm2
```
' Circular buffer reading
        rdfast  ##$8000_0000, ##buffer  ' Bit 31 set = wrap mode
        
circular_loop
        rflong  value                   ' Read from FIFO
        ' Process value
        ' FIFO automatically wraps at buffer end!
        jmp     #circular_loop
```
:::

### Processing Pipeline with FIFO

::: pasm2
```
' Read data with FIFO, process, write via PTRA
        rdfast  #0, ##source    ' Set up FIFO for reading
        mov     dest_ptr, ##dest

pipeline
        rflong  input           ' Get next input from FIFO

        ' Scale using 16x16 multiply (result in input)
        mul     input, #SCALE_FACTOR

        wrlong  input, dest_ptr ' Write result via PTRA
        add     dest_ptr, #4
        djnz    count, #pipeline
```
:::

Note: FIFO can only read OR write at a time, not both. Use PTRA/PTRB for the other direction.

## Your Turn: Streaming Experiments

:::yourturn
**Your Turn:** Fast memory fill

Starting code:

::: pasm2
```
        org     0
        
        mov     pattern, ##$DEADBEEF
        mov     dest, ##$1000
        mov     count, #256
        
        ' Your code here: Fill 256 longs with pattern
        ' Use SETQ and WRLONG
```
:::

Goal: Fill memory with pattern using block transfer
Hint: You'll need setq #255 (not #256)
Success Check: Memory filled in one operation
:::

:::yourturn
**Your Turn:** Data filter pipeline

Starting code:

::: pasm2
```
        org     0
        
        rdfast  #0, ##input_data
        wrfast  #0, ##output_data
        mov     count, #100
        
filter_loop
        rflong  value
        ' Your code: Simple filter
        ' Maybe average with previous value?
        wflong  result
        djnz    count, #filter_loop
```
:::

Goal: Process streaming data through simple filter
Hint: Keep previous value in a register
Success Check: Output is filtered version of input
:::

## Common Streaming Gotchas

Watch out for these:

1. **SETQ uses count-1** - For 16 longs, use `setq #15`, not `setq #16`

2. **FIFO is shared per COG** - Can't use FIFO for both code execution and data streaming simultaneously

3. **Write synchronization** - WRFAST doesn't wait for writes to complete. Use `waitx #20` if you need to ensure completion

4. **Hub alignment** - Block transfers work best with long-aligned addresses

5. **FIFO depth** - The FIFO is 64 longs deep. Don't outrun it!

## Performance Numbers

Let's talk speed:

- **Block transfer**: Up to 1 long per clock (at 200MHz = 800MB/s!)
- **FIFO streaming**: Up to 1 long per clock sustained
- **Random hub access**: 2-9 clocks per access
- **Streamer to pins**: Up to sysclock/1 rate

This is seriously fast. Most microcontrollers need dedicated DMA controllers to achieve what P2 does with simple instructions.

## Real-World Example: Audio Buffer

Stream audio samples through processing:

::: pasm2
```
' Audio processing pipeline
audio_process
        rdfast  #0, ##input_buffer      ' Input samples
        wrfast  #0, ##output_buffer     ' Output samples
        mov     samples, ##BUFFER_SIZE
        
process_loop
        rflong  left_sample             ' Get left channel
        rflong  right_sample            ' Get right channel
        
        ' Apply simple low-pass filter
        add     left_filtered, left_sample
        shr     left_filtered, #1       ' Average with previous
        
        add     right_filtered, right_sample
        shr     right_filtered, #1
        
        ' Apply volume
        muls    left_filtered, volume
        muls    right_filtered, volume
        
        ' Output processed samples
        wflong  left_filtered
        wflong  right_filtered
        
        djnz    samples, #process_loop
```
:::

## What We've Learned

Your streaming skills now include:

- ✅ Block transfers with SETQ
- ✅ FIFO reading and writing
- ✅ Streaming pipeline concepts
- ✅ Circular buffer techniques
- ✅ Parallel processing while streaming
- ✅ Real-world applications

## Coming Up Next

Chapter 10 explores "Hub Execution" - how to break free from the 512-instruction limit and run massive programs directly from hub memory. It's like having your cake and eating it too!


**Have Fun!** Remember, streaming is about throughput, not just speed. It's the difference between carrying one brick at a time and using a wheelbarrow!


# Chapter 10: Hub Execution

*Breaking free from the 512-instruction limit*

## The Hook: Unlimited Code Space

Remember fretting about fitting your code into 496 COG instructions? Watch this:

::: pasm2
```
        orgh    $400            ' Place code in hub memory
        
        ' This can be thousands of instructions!
main    mov     x, #0
        mov     y, #0
        call    #huge_function  ' Can be massive
        call    #another_big_one
        call    #yet_another
        ' Keep going... no limit!
        
huge_function
        ' 1000 instructions? No problem!
        ' 10000 instructions? Still fine!
        ret
```
:::

Your code now lives in hub memory's 512KB instead of COG memory's 2KB. That's 256 times more space!

## COG vs Hub Execution: The Trade-offs

Let's be honest about the differences:

**COG Execution** (traditional):

- ✅ Fast: exactly 2 clocks per instruction
- ✅ Deterministic: perfect for real-time
- ❌ Limited: only 496 instructions
- ✅ Self-contained: runs independently

**Hub Execution** (the new way):

- ❌ Slower: 2-9 clocks per instruction (typically 3-4)
- ❌ Variable timing: depends on hub alignment
- ✅ Unlimited: 512KB of code space!
- ✅ Flexible: can call COG routines

The beauty? You can mix both in the same program!

## How Hub Execution Works

When the processor encounters a jump or call to a hub address (>$1FF), it automatically switches to hub execution mode. The FIFO starts streaming instructions from hub memory:

::: pasm2
```
        org     0               ' Start in COG
        
cog_code
        ' This runs from COG RAM
        call    #hub_function   ' Call into hub
        ' Back in COG mode here
        
        orgh    $1000          ' Switch to hub addresses
        
hub_function
        ' This runs from hub RAM via FIFO
        ' Can be huge!
        ret                    ' Returns to COG code
```
:::

The magic happens automatically. No mode switching instructions needed!

## Real-World Example: Menu System

Here's something that would never fit in COG RAM:

::: pasm2
```
        orgh    $2000
        
menu_system
        call    #draw_menu_frame
        call    #display_options
        call    #get_user_input
        call    #process_selection
        
        cmp     selection, #1 wcz
   if_e call    #option_1_handler
        cmp     selection, #2 wcz
   if_e call    #option_2_handler
        cmp     selection, #3 wcz
   if_e call    #option_3_handler
        ' ... many more options
        
        jmp     #menu_system
        
draw_menu_frame
        ' 200 instructions for fancy graphics
        ret
        
display_options
        ' 300 instructions for text rendering
        ret
        
option_1_handler
        ' 500 instructions for configuration
        ret
        
' Thousands of instructions total - no problem!
```
:::

## The Hub Execution FIFO

The FIFO that makes hub execution possible is the same one used for streaming data. It reads ahead, keeping a buffer of upcoming instructions:

::: pasm2
```
' The FIFO maintains performance by reading ahead
hub_loop
        add     x, y           ' FIFO has next instructions ready
        sub     a, b           ' No waiting for hub access
        mul     c, d           ' Instructions stream smoothly
        ' FIFO automatically refills as needed
```
:::

This read-ahead behavior means hub execution is often faster than the worst-case 9 clocks per instruction.

## Mixing COG and Hub Code

Here's the real power - combining both modes:

::: pasm2
```
        org     0
        
' Critical timing code in COG
critical_loop
        testp   #TRIGGER_PIN wz       ' Test trigger pin
  if_nz jmp     #critical_loop        ' Loop until triggered
        drvh    #CRITICAL_PIN         ' Immediate response!
        call    #hub_process   ' Do complex processing
        jmp     #critical_loop
        
        orgh    $4000
        
' Complex processing in hub
hub_process
        ' Hundreds of instructions for data analysis
        ' Not time-critical, so hub execution is fine
        ret
```
:::

Time-critical code stays in COG RAM for deterministic timing. Complex code lives in hub RAM for space.

## Your Turn: Hub Execution Experiments

:::yourturn
**Your Turn:** Build a simple calculator

Starting code:

::: pasm2
```
        org     0
        jmp     #calculator    ' Jump to hub code
        
        orgh    $1000
calculator
        ' Your code here:
        ' 1. Display menu
        ' 2. Get operation choice
        ' 3. Get two numbers
        ' 4. Call appropriate function
        ' 5. Display result
        
add_function
        ' Addition code
        ret
        
subtract_function
        ' Subtraction code
        ret
        
' Add more functions - no size limit!
```
:::

Goal: Create a multi-function calculator
Hint: Each function can be as complex as needed
Success Check: Multiple operations working
:::

::: medicine-cabinet
Overwhelmed by execution modes? Here's the simple version:

**Keep it simple:**

1. **Small, time-critical code** → Put in COG (org 0)
2. **Large, complex code** → Put in hub (orgh $400+)
3. **Don't overthink it** → The processor handles the switch

**Basic pattern:**

::: pasm2
```
        org     0
        jmp     #main      ' Jump to hub

        orgh    $400
main    ' Your big program here
```
:::

That's it. Let the processor worry about the details!
:::

## Advanced Hub Execution

### Long Jumps and Calls

Hub addresses need 20 bits, so jumping far requires special handling:

::: pasm2
```
' Jump to distant hub code
        jmp     ##far_away     ' ## forces 32-bit immediate
        
        orgh    $40000        ' Far away in hub
far_away
        ' Code here
```
:::

### Hub Data Access from Hub Code

When executing from hub, you can still access hub data:

::: pasm2
```
        orgh    $1000
        
hub_code
        rdlong  value, ##hub_data  ' Read hub data
        add     value, #1
        wrlong  value, ##hub_data  ' Write back
        
        orgh    $8000
hub_data
        long    $12345678
```
:::

### Performance Optimization

To maximize hub execution speed:

::: pasm2
```
' Align branch targets to 8-byte boundaries
        alignl                 ' Align to long boundary
loop_start
        ' Loop code here
        djnz    count, #loop_start
        
' Keep critical loops small
' Consider moving inner loops to COG RAM
```
:::

## Common Hub Execution Gotchas

1. **Speed variation** - Don't use hub execution for precise timing
2. **FIFO conflicts** - Can't stream data while executing from hub
3. **Address confusion** - Remember: <$200 is COG, >=$200 is hub
4. **Stack depth** - Still limited to 8-level hardware stack
5. **Relative jumps** - Work differently in hub mode

## Real-World Example: Command Parser

::: pasm2
```
        orgh    $2000
        
command_parser
        call    #get_command_line
        call    #tokenize
        
        ' Compare against commands
        mov     ptra, #command_string
        mov     ptrb, ##cmd_help
        call    #string_compare
   if_z jmp     #help_command
        
        mov     ptrb, ##cmd_run
        call    #string_compare
   if_z jmp     #run_command
        
        ' Many more commands...
        
help_command
        ' 500 instructions of help text display
        ret
        
run_command
        ' 1000 instructions of program execution
        ret
        
string_compare
        ' 50 instructions of string comparison
        ret
        
' Thousands of instructions total
' Would need multiple COGs without hub execution!
```
:::

## When to Use Hub Execution

**Perfect for:**

- User interfaces and menus
- Command processors
- Complex algorithms
- String manipulation
- Protocol handlers
- Error handling and recovery

**Avoid for:**

- Interrupt handlers (if you use them)
- Precise timing loops
- Bit-banged protocols
- Real-time control loops

## What We've Learned

You've mastered hub execution:

- ✅ Understanding COG vs hub trade-offs
- ✅ Automatic mode switching
- ✅ Mixing COG and hub code
- ✅ FIFO streaming of instructions
- ✅ When to use each mode
- ✅ Real-world applications

## Coming Up Next

Chapter 11 tackles the controversial topic: "Why No Interrupts?" We'll explore why the Propeller philosophy says you don't need them, and why that's actually a good thing!


**Have Fun!** Hub execution is like having a sports car that can also carry furniture - you get both speed and capacity when you need them!


# Chapter 11: Why No Interrupts?

*The most controversial P2 feature explained*

## The Hook: Interrupts Without Interrupts

Here's a traditional interrupt-driven button handler:

::: antipattern
```
// Traditional approach (not P2!)
ISR(BUTTON_INTERRUPT) {
    // Interrupt service routine
    buttonPressed = true;
    // Return to interrupted code
}
```
:::

And here's the P2 way:

::: pasm2
```
' Dedicated COG watching button
button_watcher
        testp   #BUTTON_PIN wc
   if_c wrlong  ##1, ##button_flag
        jmp     #button_watcher
        
' Main COG doing important work
main_code
        ' Never interrupted!
        ' Checks button_flag when convenient
```
:::

No interrupt latency. No context switching. No priority inversion. No critical sections. Just clean, deterministic, parallel processing.

## The Interrupt Problem

Let me tell you a story. You're concentrating on a complex problem when someone taps your shoulder. You stop, handle their request, then try to remember where you were. Now imagine this happening randomly, unpredictably, dozens of times per second.

That's interrupts.

Traditional processors need interrupts because they only have one processor. Something important happens? Stop everything and handle it! But this causes:

- **Latency**: Time to save context and jump to handler
- **Jitter**: Variable response time depending on what was interrupted
- **Priority inversion**: Low-priority task blocks high-priority
- **Race conditions**: Shared data access problems
- **Debugging nightmares**: Non-reproducible timing bugs

## The Propeller Solution

Eight processors. No sharing required.

::: pasm2
```
' COG 0: Main application
main_app
        ' Complex calculations
        ' Never interrupted
        rdlong  command, ##mailbox wz
   if_nz call   #process_command
        jmp     #main_app

' COG 1: Serial port handler
serial_handler
        ' Continuously monitors serial
        testp   #RX_PIN wc
   if_c call    #receive_byte
        jmp     #serial_handler
        
' COG 2: Motor control
motor_control
        ' Precise timing loops
        ' Never disrupted
        waitcnt motor_time
        drvnot  #STEP_PIN
        jmp     #motor_control
        
' COG 3: Sensor monitor
sensor_monitor
        ' Watches multiple sensors
        ' Responds instantly
        ' ... and so on
```
:::

Each COG does one thing perfectly. No interruptions. No conflicts. Just pure, focused execution.

## Real-World Example: Perfect Servo Control

With interrupts, servo pulses jitter. With dedicated COGs, they're perfect:

::: pasm2
```
' COG dedicated to servo control
servo_cog
        getct   pulse_time
        
servo_loop
        ' Generate 8 servo pulses simultaneously
        mov     servo_mask, ##$FF      ' 8 servos
        or      outa, servo_mask       ' All high
        
        mov     index, #0
check_servos
        rdlong  width, ptra[index]     ' Get pulse width
        addct1  pulse_time, width      ' Set compare time
        
        waitct1                        ' Wait for exact time
        bitl    outa, index            ' Turn off this servo
        
        incmod  index, #7
        tjnz    servo_mask, #check_servos
        
        ' Wait for 20ms frame
        waitx   ##4_000_000
        jmp     #servo_loop
        
' Result: 8 servos with ZERO jitter!
```
:::

Try that with interrupts. I'll wait. Actually, I won't - it's impossible to achieve this precision with interrupts.

## "But P2 HAS Interrupts!"

Yes, it does. And you probably shouldn't use them.

Well, let me be more nuanced. P2 has interrupts for those rare cases where you absolutely need them:

::: pasm2
```
' Setting up an interrupt (not recommended!)
        setse1  #%001<<6 + PANIC_BUTTON   ' SE1 triggers when pin goes high
        setint1 #EVENT_SE1                ' Enable INT1 on SE1 event

int1_handler
        ' Interrupt code here
        reti1
```
:::

When might you use them?

- Porting legacy code that requires interrupts
- Ultra-low-power designs where COGs must sleep
- Theoretical minimum latency response (but dedicated COG is usually faster!)

Uff! Even writing interrupt code feels wrong on a Propeller!

::: medicine-cabinet
Still thinking you need interrupts? Here's your medicine:

**Think you need an interrupt for...**

**Fast response?**

::: pasm2
```
' Dedicated COG responds in ~4 clocks
watcher
        testp   #INPUT_PIN wz         ' Test pin state
  if_nz jmp     #watcher              ' Loop until pin high
        drvh    #RESPONSE_PIN         ' Instant response!
```
:::

**Multiple events?**

::: pasm2
```
' One COG watches everything
monitor
        test    sensors, #SENSOR1 wz
   if_nz call   #handle_sensor1
        test    sensors, #SENSOR2 wz
   if_nz call   #handle_sensor2
        ' Check all sensors every loop
```
:::

**Periodic tasks?**

::: pasm2
```
' Perfect timing without interrupts
        getct   next_time
.loop   addct1  next_time, ##PERIOD
        waitct1                ' Exact timing
        call    #periodic_task
        jmp     #.loop
```
:::

See? No interrupts needed!
:::

## The Event System: Better Than Interrupts

P2 has something better than interrupts - events:

::: pasm2
```
' Configure event to watch pin
        setse1  #%01_000000 | BUTTON_PIN  ' Rising edge event
        
' Main code runs normally
main_loop
        ' Do work...
        pollse1 wc              ' Check if event occurred
   if_c call    #handle_button  ' Handle when convenient
        ' Continue work...
        jmp     #main_loop
```
:::

Events are like interrupts that wait politely for you to check them. No rudeness!

## Interrupt Horror Stories

Let me share why we avoid interrupts:

### Story 1: The Jittery Display

| Approach | Problem | Result |
|----------|---------|--------|
| **With Interrupts** | Display updates interrupted by serial | Visible glitches, tearing, inconsistent timing |
| **With COGs** | Display COG runs uninterrupted | Perfect, smooth, glitch-free display |

### Story 2: The Missed Pulse

| Approach | Problem | Result |
|----------|---------|--------|
| **With Interrupts** | Motor step interrupted by sensor read | Missed step, motor stalls, position lost |
| **With COGs** | Motor COG never misses a beat | Perfect positioning, no lost steps |

### Story 3: The Debugging Nightmare

| Approach | Problem | Result |
|----------|---------|--------|
| **With Interrupts** | Bug only appears under specific timing | Days of debugging, hair loss, coffee overdose |
| **With COGs** | Deterministic timing, reproducible behavior | Bug found in minutes, sanity preserved |

## Your Turn: COG vs Interrupt Challenge

:::yourturn
**Your Turn:** Build a reaction timer without interrupts

Starting code:

::: pasm2
```
        org     0
        
' COG 0: Main game logic
        coginit #1, @button_watcher, ##button_flag
        
game_loop
        ' Random delay
        getrnd  delay
        waitx   delay
        
        drvh    #LED_PIN
        wrlong  #0, ##button_flag
        getct   start_time
        
' Wait for button (no interrupt!)
wait_press
        rdlong  pressed, ##button_flag wz
   if_z jmp     #wait_press
        
        getct   end_time
        sub     end_time, start_time
        ' Display reaction time
        
' COG 1: Button watcher
        orgh    $400
button_watcher
        ' Your code here
```
:::

Goal: Implement button watcher COG
Hint: Continuously monitor and set flag
Success Check: Perfect timing without interrupts
:::

## The Philosophy Deep Dive

The Propeller philosophy is about **determinism over responsiveness**.

Traditional processors optimize for average-case performance:

- Interrupts handle rare events
- Most code runs uninterrupted
- When events happen, everything stops

Propeller optimizes for worst-case determinism:

- Every COG runs predictably
- No surprises, ever
- Timing is guaranteed

It's the difference between a talented soloist who might miss a note and an orchestra where everyone plays their part perfectly.

## When Interrupts Actually Make Sense

I'll admit it - there are rare cases where interrupts are appropriate:

1. **Power-critical applications** where COGs must sleep
2. **Legacy code ports** that fundamentally require interrupts
3. **Single-COG designs** (but why waste the P2's power?)

But in 15 years of Propeller programming, I've needed interrupts exactly... never.

## Common "But What About..." Questions

**Q: "But what about interrupt priority?"**
A: COGs don't have priority. They're all equal. Design your system accordingly.

**Q: "How do I handle critical events?"**
A: Dedicate a COG to critical events. It will respond faster than any interrupt.

**Q: "Isn't dedicating a whole COG wasteful?"**
A: You have eight! And a focused COG is simpler than interrupt-riddled code.

**Q: "What about power consumption?"**
A: Use WAITSE/WAITCT for low-power waiting. COG sleeps until event.

## What We've Learned

You now understand the Propeller way:

- ✅ Why interrupts cause problems
- ✅ How COGs eliminate interrupt need
- ✅ Event system as polite alternative
- ✅ Real-world benefits of no interrupts
- ✅ Rare cases where interrupts might be used
- ✅ The philosophy of determinism

## Coming Up Next

Chapter 12 shows you "Optimization Mastery" - how to make your PASM2 code blazingly fast. We'll explore the pipeline, instruction pairing, and timing tricks that squeeze every drop of performance from the P2.


**Have Fun!** And remember - in a world of interruptions, be a COG: focused, deterministic, and uninterruptible!


# Chapter 12: Optimization Mastery

*Making the fast faster*

## The Hook: Double Your Speed with One Change

Look at this seemingly innocent code:

::: pasm2
```
' Before optimization: 13 clocks
.loop   rdlong  value, ptra      ' 9-16 clocks hub access
        add     value, #1        ' 2 clocks
        wrlong  value, ptra      ' 3-10 clocks
        add     ptra, #4         ' 2 clocks
        djnz    count, #.loop    ' 2/4 clocks

' After optimization using PTR expressions:
.loop   rdlong  value, ptra      ' Read from current address
        add     value, #1        ' Process
        wrlong  value, ptra++    ' Write and increment in one!
        djnz    count, #.loop    ' Saved the ADD instruction
```
:::

Almost twice as fast! The secret? Understanding how P2 really works.

## Understanding the Pipeline

P2 has a 2-stage pipeline:

1. **Fetch** - Get next instruction
2. **Execute** - Do the work

This means while one instruction executes, the next is already being fetched:

::: pasm2
```
        add     x, y      ' Executing while next inst fetches
        sub     a, b      ' Fetching while previous executes
        ' Perfect overlap = maximum throughput
```
:::

## Instruction Timing Basics

Not all instructions are created equal:

::: pasm2
```
' 2-clock instructions (most ALU operations)
        add     x, y            ' 2 clocks
        mov     a, b            ' 2 clocks
        and     c, d            ' 2 clocks

' Variable timing (hub access)
        rdlong  value, hubaddr  ' 9-16 clocks (hub slot wait)
        wrlong  value, hubaddr  ' 3-10 clocks (variable)
        
' Long operations (CORDIC)
        qrotate x, angle        ' 2 clocks to start
        getqx   result          ' 2 clocks (but wait 55 for result)
        
' Special cases
        mul     x, y            ' 2 clocks
        qdiv    x, y            ' 2 clocks to start
        getqx   result          ' 2 clocks (but wait 30 for result)
```
:::

## REP: The Speed Loop

REP creates hardware-accelerated loops with zero overhead:

::: pasm2
```
' Traditional loop: overhead per iteration
.loop   add     sum, value      ' 2 clocks
        add     ptr, #4         ' 2 clocks
        djnz    count, #.loop   ' 2 or 4 clocks (4 if branch taken)

' REP loop: 0 clocks overhead!
        rep     #2, count       ' Repeat next 2 instructions
        add     sum, value      ' 2 clocks
        add     ptr, #4         ' 2 clocks = 4 total!
```
:::

That's 33% faster just by using REP!

## SKIP: Conditional Execution on Steroids

SKIP and SKIPF let you conditionally execute patterns of instructions:

::: pasm2
```
' Traditional: multiple jumps
        cmp     x, #5 wcz
if_a    jmp     #greater
if_b    jmp     #less
        jmp     #equal

' With SKIP: no jumps!
        cmp     x, #5 wcz
        skip    ##%11000        ' Skip pattern based on flags
        mov     result, #1      ' Execute if equal
        mov     result, #2      ' Execute if less
        mov     result, #3      ' Execute if greater
        ' No pipeline stalls from jumps!
```
:::

## Hub Access Optimization

Hub timing is critical for performance:

::: pasm2
```
' Unaligned hub access: variable timing
        rdlong  v1, ##$1001     ' Not long-aligned, slower
        
' Aligned hub access: predictable timing  
        rdlong  v1, ##$1000     ' Long-aligned, faster
        
' Sequential access: maximum speed
        rdlong  v1, ptra++      ' Hardware manages sequence
        rdlong  v2, ptra++      ' Optimal hub slot usage
        rdlong  v3, ptra++      ' Maximum throughput
```
:::

## The FIFO Fast Path

For ultimate speed, use the FIFO:

::: pasm2
```
' Traditional hub reading: ~6 clocks average per long
.loop   rdlong  value, ptra++
        add     sum, value
        djnz    count, #.loop

' FIFO reading: 2 clocks per long!
        rdfast  #0, ptra        ' Start FIFO
.loop   rflong  value           ' 2 clocks, always!
        add     sum, value      ' 2 clocks
        djnz    count, #.loop   ' 2 clocks
        ' 3x faster for sequential reads!
```
:::

## Parallel Operations

CORDIC operations can overlap with other work:

::: pasm2
```
' CORDIC overlaps with other instructions
        qmul    x, y            ' Start 32x32->64 multiply (CORDIC)
        ' 54 clocks to do other work!
        add     a, b            ' These execute during CORDIC
        sub     c, d
        mov     index, #0
        rdlong  data, ptra++
        ' ... more work
        getqx   low_result      ' Get CORDIC result (lower 32 bits)
        getqy   high_result     ' Get CORDIC result (upper 32 bits)

' QROTATE overlap
        qrotate x_coord, angle  ' Start rotation (D=X, S=angle)
        ' 54 clocks of other work!
        getqx   new_x           ' Get rotated X
        getqy   new_y           ' Get rotated Y
```
:::

Note: MUL/MULS are 2-clock ALU instructions that complete immediately (16x16->32). Use QMUL for 32x32->64 with CORDIC overlap.

## Real-World Example: Fast Memory Copy

Let's optimize a memory copy routine:

::: pasm2
```
' Version 1: Basic (slow)
copy_basic
        rdlong  temp, source
        wrlong  temp, dest
        add     source, #4
        add     dest, #4
        djnz    count, #copy_basic
        ' ~13 clocks per long

' Version 2: Better pointers
copy_better
        rdlong  temp, ptra++
        wrlong  temp, ptrb++
        djnz    count, #copy_better
        ' ~8 clocks per long
        
' Version 3: Block transfer (ultimate)
copy_ultimate
        sub     count, #1       ' SETQ needs count-1 (0 = 1 long)
        setq    count           ' Setup block transfer
        rdlong  buffer, source  ' Read all at once
        setq    count           ' (count already decremented)
        wrlong  buffer, dest    ' Write all at once
        ' <1 clock per long for large blocks!
```
:::

::: medicine-cabinet
Optimization overwhelming you? Start with these simple improvements:

**Three easy wins:**

1. **Use PTRA/PTRB** instead of manual pointer math

::: pasm2
```
' Slow
        rdlong  x, addr
        add     addr, #4

' Fast
        rdlong  x, ptra++
```
:::

2. **Align your data** to long boundaries

::: pasm2
```
        alignl          ' Force long alignment
data    long    $12345678
```
:::

3. **Use REP** for tight loops

::: pasm2
```
        rep     #1, count
        add     sum, ptra++
```
:::

Just these three changes often double performance!
:::

## Your Turn: Optimization Challenges

:::yourturn
**Your Turn:** Optimize a checksum calculator

Starting code:

::: pasm2
```
' Slow version
checksum_slow
        mov     sum, #0
        mov     addr, ##buffer
        mov     count, #256

.loop   rdbyte  temp, addr
        add     sum, temp
        add     addr, #1
        djnz    count, #.loop
```
:::

Goal: Make it at least 4x faster
Hint: Read longs instead of bytes, use FIFO
Success Check: Same checksum, much faster
:::

## Advanced Techniques

### Instruction Pairing

Some instruction pairs execute specially:

::: pasm2
```
' ## syntax handles AUGS automatically
        mov     x, ##$12345678  ' Assembler generates AUGS + MOV
        ' Same result, cleaner code!
        
' ALTD + instruction = indirect addressing
        altd    index, #array
        mov     0-0, value      ' Stores to array[index]
```
:::

### Pipeline-Aware Coding

Avoid pipeline stalls:

::: pasm2
```
' Bad: result needed immediately
        add     x, y
        cmp     x, #10 wcz      ' Stall waiting for x
        
' Good: interleave operations
        add     x, y
        mov     a, b            ' Do something else
        cmp     x, #10 wcz      ' Now x is ready
```
:::

### Unrolling Loops

Sometimes removing the loop is faster:

::: pasm2
```
' Looped version
        rep     #1, #4
        add     sum, ptra++
        
' Unrolled version (faster for small counts)
        add     sum, ptra++
        add     sum, ptra++
        add     sum, ptra++
        add     sum, ptra++
```
:::

## Common Optimization Gotchas

1. **Premature optimization** - Get it working first, then optimize
2. **Over-optimizing** - Sometimes clarity is worth 2 clocks
3. **Ignoring the big picture** - Optimize the bottleneck, not everything
4. **Breaking functionality** - Fast but wrong is useless
5. **Forgetting about power** - Faster isn't always better for battery life

## Profiling and Measurement

Always measure your optimizations:

::: pasm2
```
' Time your code
        getct   start_time
        
        ' Code to measure
        call    #function_to_test
        
        getct   end_time
        sub     end_time, start_time
        ' end_time now contains exact clock cycles
```
:::

## What We've Learned

You're now an optimization expert:

- ✅ Understanding the P2 pipeline
- ✅ Instruction timing knowledge
- ✅ REP and SKIP for zero-overhead loops
- ✅ FIFO for maximum throughput
- ✅ Parallel operation techniques
- ✅ Real-world optimization strategies

## Coming Up Next

Chapters 13-15 provide quick examples of Video Generation, Serial Protocols, and Signal Processing - with references to dedicated manuals for deep dives. Think of them as appetizers showing what's possible!


**Have Fun!** Remember, the best optimization is often a better algorithm. But when you need every last cycle, you now know how to get them!


# Chapter 13: LUT Memory - Your Private Lookup Table

*512 longs of fast, deterministic storage in every COG*

## The Hook: A Lookup Table in 3 Cycles

Need fast data lookup without hub timing? Every COG has its own private 512-long Lookup RAM (LUT):

::: pasm2
```
' Sine table lookup - 3 clocks, every time
get_sine
        and     angle, #$FF      ' Mask to table index
        rdlut   value, angle     ' Read from LUT in 3 clocks!
        ret
```
:::

No hub timing to worry about. No waiting for the egg beater. Just 3 clock cycles, guaranteed. The LUT is like having a personal data assistant that never takes a coffee break.

## Why Another Memory?

You might be thinking, "Wait, I already have COG RAM and Hub RAM - why do I need a third memory?" Excellent question!

| Memory | Size per COG | Access Time | Special Features |
|--------|--------------|-------------|------------------|
| COG RAM | 512 longs | 2 clocks | Instructions live here |
| Hub RAM | 512 KB shared | 2-9 clocks (hub slot wait) | Shared by all COGs |
| **LUT RAM** | 512 longs | **3 clocks** | **Private, deterministic, shareable with neighbor** |

The LUT fills a sweet spot: faster than hub memory, doesn't compete with your instruction space, and has a trick up its sleeve - neighboring COGs can share LUTs!

## Reading and Writing the LUT

### Basic LUT Access

::: pasm2
```
' Write to LUT
        wrlut   #$12345678, #100  ' Write constant to LUT[100]
        wrlut   value, index      ' Write variable to LUT[index]

' Read from LUT
        rdlut   result, #100      ' Read LUT[100] into result
        rdlut   data, index       ' Read LUT[index] into data
```
:::

Notice the operand order: **WRLUT** writes its first operand to the address in the second, while **RDLUT** reads from its second operand into the first. A bit backwards from what you might expect, but you'll get used to it.

### Building a Lookup Table

Here's how to load a sine table into LUT:

::: pasm2
```
' Copy 256-entry sine table from hub to LUT
load_sine_table
        mov     index, #0
        loc     ptra, #\sine_data_hub   ' Hub address of table

.loop   rdlong  value, ptra++    ' Read from hub
        wrlut   value, index     ' Write to LUT
        add     index, #1
        cmp     index, #256 wz
  if_nz jmp     #.loop
        ret

' Now lookups are fast!
get_sine
        rdlut   sine_value, angle  ' 3 clocks!
        ret
```
:::

::: sidetrack
**Bulk LUT Loading with SETQ2**

For loading entire tables, **SETQ2** + **RDLONG** can transfer hub data directly to LUT addresses $200+:

::: pasm2
```
        setq2   #256-1              ' 256 longs
        rdlong  $200, hub_table_ptr ' Load into LUT from $200
```
:::

This works because the assembler maps LUT addresses $200-$3FF. Just remember the -1 in **SETQ2** (same rule as **SETQ** for hub block transfers).
:::

## LUT Sharing Between COGs

Here's something clever: adjacent COG pairs can share LUT data! When you enable LUT sharing with SETLUTS, writes your neighbor makes to their LUT are automatically *copied* to your LUT too.

::: pasm2
```
' --- COG 1 (consumer) - MUST enable sharing FIRST ---
        setluts #1              ' Enable LUT write copying FROM COG 0
        ' Now when COG 0 writes to its LUT, data is COPIED to our LUT

' --- COG 0 (producer) - writes AFTER consumer enables sharing ---
        wrlut   message, #10    ' Write MY LUT[10] (copies to COG 1)
        wrlut   #1, #0          ' Set ready flag (copies to COG 1)

' --- COG 1 (consumer) - reads its OWN LUT (which contains copies) ---
.wait   rdlut   flag, #0        ' Read MY LUT[0] (contains copy from COG 0)
        cmp     flag, #1 wz
  if_nz jmp     #.wait
        rdlut   message, #10    ' Read MY LUT[10] (copied from COG 0)
```
:::

The key instruction is:

- **SETLUTS**: Enable write copying - when neighbor writes with WRLUT, data is copied to YOUR LUT
- **RDLUT**: Read your own LUT (which now contains copied data)

Important: The consumer COG must enable SETLUTS *before* the producer writes, otherwise the writes won't be copied!

This gives you a 512-long shared buffer between COG pairs without touching hub memory. Perfect for high-bandwidth data passing!

::: sidetrack
**Which COGs Are Neighbors?**

The LUT sharing pairs are fixed:

- COG 0 ↔ COG 1
- COG 2 ↔ COG 3
- COG 4 ↔ COG 5
- COG 6 ↔ COG 7

An even-numbered COG reads its odd neighbor's LUT, and vice versa. You cannot read LUTs from non-adjacent COGs.
:::

## Practical Examples

### Fast Data Transformation

::: pasm2
```
' Gamma correction table in LUT
' Input: 8-bit value in 'pixel'
' Output: Gamma-corrected value
gamma_correct
        and     pixel, #$FF     ' Mask to 8 bits
        rdlut   pixel, pixel    ' Transform via table
        ret

' Initialize gamma table (power law curve)
' Would be pre-calculated and loaded from hub
```
:::

### Circular Buffer in LUT

::: pasm2
```
' Fast circular buffer using LUT
' 256-entry buffer at LUT addresses 0-255

buf_write_ptr   long    0
buf_read_ptr    long    0

put_byte
        wrlut   data, buf_write_ptr
        add     buf_write_ptr, #1
        and     buf_write_ptr, #$FF   ' Wrap at 256
        ret

get_byte
        rdlut   data, buf_read_ptr
        add     buf_read_ptr, #1
        and     buf_read_ptr, #$FF    ' Wrap at 256
        ret
```
:::

### Fast Stack in LUT

::: pasm2
```
' Stack implementation in LUT
' Grows downward from $1FF
stack_ptr       long    $1FF

push
        wrlut   value, stack_ptr
        sub     stack_ptr, #1
        ret

pop
        add     stack_ptr, #1
        rdlut   value, stack_ptr
        ret
```
:::

## LUT with the Streamer

Here's where LUT gets really interesting. The Streamer can read directly from LUT to generate waveforms without any COG intervention:

::: pasm2
```
' Fill LUT with waveform data
' Then let Streamer output it to DAC

load_waveform
        mov     index, #0

.fill   mov     value, index
        shl     value, #24       ' Scale for DAC
        wrlut   value, index
        add     index, #1
        cmp     index, #512 wz
  if_nz jmp     #.fill

' Now configure Streamer to read from LUT
' Streamer handles the rest - no COG cycles needed!
```
:::

The Streamer configuration for LUT reading is covered in detail in the Video and Audio manuals - but the key point is that your LUT becomes a 512-sample waveform buffer that plays automatically.

## Common Gotchas

::: antipattern
**❌ WRONG: Confusing LUT addresses**

```
' WRONG - This reads COG RAM, not LUT!
        mov     value, $200     ' $200 is COG RAM address
```
:::

**✓ RIGHT: Use RDLUT for LUT access**

::: pasm2
```
' RIGHT - RDLUT addresses the LUT space
        rdlut   value, #0       ' LUT address 0
```
:::

::: antipattern
**❌ WRONG: Reading LUT before neighbor writes**

```
' WRONG - No data to read yet!
        setluts #1              ' Enable sharing
        rdlut   data, #10       ' Empty - neighbor hasn't written!
```
:::

**✓ RIGHT: Wait for neighbor's write signal**

::: pasm2
```
' RIGHT - Wait for data to be copied
        setluts #1              ' Enable sharing BEFORE neighbor writes
.wait   rdlut   ready, #0       ' Check flag in MY LUT
        tjz     ready, #.wait   ' Wait until neighbor writes
        rdlut   data, #10       ' Now MY LUT has copied data
```
:::

## Medicine Cabinet

::: medicine-cabinet
**LUT Memory Quick Reference**

| Instruction | Operation | Cycles |
|-------------|-----------|--------|
| **RDLUT** D, S | Read LUT[S] into D | 3 |
| **WRLUT** D, S | Write D to LUT[S] | 2 |
| **SETLUTS** D | Enable LUT write copying (D[0]=1) | 2 |

**Memory Map:**

- LUT addresses: 0-511 (512 longs = 2KB)
- Neighbor pairs: 0↔1, 2↔3, 4↔5, 6↔7

**Best Uses:**

- Lookup tables (sine, gamma, encoding)
- Fast circular buffers
- COG-pair data sharing
- Streamer waveform source
:::

## Your Turn

::: your-turn
**Exercise 1: Build an 8-bit Encoder**

Create a LUT-based ASCII to 7-segment display encoder. Load a 128-entry table where each entry maps an ASCII code to the 7-segment pattern for that character.

```pasm2
' Your code here:
' 1. Load segment patterns into LUT
' 2. Write encode_char routine
' Hint: rdlut segment_pattern, ascii_char
```
:::

::: your-turn
**Exercise 2: High-Speed COG Communication**

Use LUT sharing to create a message passing system between COG 2 and COG 3:

- COG 2 writes 8-long messages
- COG 3 reads them without hub access
- Use a simple ready/ack protocol

```pasm2
' Hint: Use LUT[0] as ready flag, LUT[1-8] as message buffer
```
:::

*Continue to [Chapter 14: Smart Pins Orientation](#chapter-14-smart-pins-orientation) →*


# Chapter 14: Smart Pins Orientation

*64 autonomous I/O processors waiting to do your bidding*

## The Hook: A UART in 4 Lines

Remember that tedious bit-bang serial from Chapter 8? Watch this:

::: pasm2
```
' Configure pin as UART transmitter - done!
        dirl    #TX_PIN                 ' Reset pin first!
        wrpin   ##P_ASYNC_TX, #TX_PIN   ' Configure as async TX
        wxpin   ##BAUD_115200, #TX_PIN  ' Set baud rate
        dirh    #TX_PIN                 ' Enable - runs on its own
```
:::

That's it. The pin is now a fully autonomous UART transmitter. It handles start bits, stop bits, timing - everything. You just feed it bytes with **WYPIN** and it sends them. The pin has become a state machine.

And here's the mind-bending part: *every single one of the 64 pins can do this*. Or PWM. Or ADC. Or quadrature decoding. Or 28 other modes.

## What Are Smart Pins, Really?

Each of the P2's 64 I/O pins contains its own little processor - a state machine that can operate completely independently of the COGs. This means:

- A pin configured as UART keeps sending/receiving without COG intervention
- A PWM output keeps running its duty cycle automatically
- An ADC samples continuously in the background
- A quadrature decoder tracks position even while your COG does other things

The COG only needs to configure the pin and occasionally read/write data. The pin does the rest.

## The Universal Smart Pin Pattern

Every Smart Pin follows the same configuration pattern. This is **the most important thing to remember**:

::: pasm2
```
' === THE SMART PIN RECIPE ===

' Step 1: RESET the pin (CRITICAL!)
        dirl    pin             ' Always start by resetting

' Step 2: CONFIGURE the mode
        wrpin   mode, pin       ' What should this pin do?

' Step 3: SET parameters
        wxpin   x_value, pin    ' Mode-specific parameter X
        wypin   y_value, pin    ' Mode-specific parameter Y

' Step 4: ENABLE the pin
        dirh    pin             ' Start the magic!
```
:::

::: sidetrack
**Why DIRL First?**

The **DIRL** at the start isn't optional politeness - it's *required*. Smart Pins must be reset before configuration to ensure they're in a known state. Skip this and you'll get unpredictable behavior as old settings conflict with new ones.

Think of it like power-cycling a misbehaving device. Always start fresh.
:::

## The Core Instructions

### Configuration Instructions

| Instruction | Purpose |
|-------------|---------|
| **WRPIN** mode, pin | Set the operating mode |
| **WXPIN** value, pin | Set X parameter (mode-specific) |
| **WYPIN** value, pin | Set Y parameter (mode-specific) |
| **DIRH** pin | Enable the Smart Pin |
| **DIRL** pin | Disable/reset the Smart Pin |

### Data Instructions

| Instruction | Purpose |
|-------------|---------|
| **WYPIN** data, pin | Write data to Smart Pin (same instruction!) |
| **RDPIN** data, pin | Read result, clear "ready" flag |
| **RQPIN** data, pin | Read result, keep "ready" flag |
| **AKPIN** pin | Acknowledge (clear "ready" flag only) |

### Status Instructions

| Instruction | Purpose |
|-------------|---------|
| **TESTP** pin WC | Check if IN flag is set (data ready) |
| **TESTPN** pin WC | Check if IN flag is clear |

## Understanding the IN Flag

Every Smart Pin has an IN flag that signals "something happened." What that something is depends on the mode:

- **UART TX**: IN high = ready for another byte
- **UART RX**: IN high = byte received
- **ADC**: IN high = new sample ready
- **PWM**: IN high = period complete
- **Counter**: IN high = threshold reached

You check this flag with **TESTP** and clear it by reading with **RDPIN** (or explicitly with **AKPIN**).

::: pasm2
```
' Wait for Smart Pin to be ready
wait_ready
        testp   #PIN wc         ' Check IN flag
  if_nc jmp     #wait_ready     ' Loop if not ready
        rdpin   data, #PIN      ' Read and clear flag
```
:::

::: sidetrack
**Event-Driven Alternative**

Instead of polling with **TESTP**, you can use the event system:

```pasm2
setse1  #%001<<6 + PIN   ' Event when IN rises
waitse1                   ' Sleep until ready - no polling!
rdpin   result, #PIN      ' Read the result
```

This is more efficient because your COG sleeps instead of spinning. See Chapter 15 for the full event story.
:::

## Common Smart Pin Modes

Here are the modes you'll use most often:

### Asynchronous Serial (UART)

::: pasm2
```
' Transmit mode
        dirl    #TX_PIN
        wrpin   ##P_ASYNC_TX | P_OE, #TX_PIN
        wxpin   ##(clkfreq/baud)<<16 | 7, #TX_PIN  ' Baud + 8 bits
        dirh    #TX_PIN

' Send a byte
send    testp   #TX_PIN wc      ' Wait for ready
  if_nc jmp     #send
        wypin   byte, #TX_PIN   ' Send it
```
:::

::: pasm2
```
' Receive mode
        dirl    #RX_PIN
        wrpin   ##P_ASYNC_RX, #RX_PIN
        wxpin   ##(clkfreq/baud)<<16 | 7, #RX_PIN
        dirh    #RX_PIN

' Get a byte
recv    testp   #RX_PIN wc      ' Check for received byte
  if_nc jmp     #recv
        rdpin   byte, #RX_PIN   ' Get it
        shr     byte, #24       ' Shift to low byte
```
:::

### PWM Output

::: pasm2
```
' PWM mode - period + duty cycle
        dirl    #PWM_PIN
        wrpin   ##P_PWM_SAWTOOTH | P_OE, #PWM_PIN
        wxpin   ##period, #PWM_PIN      ' Period in clocks
        wypin   ##duty, #PWM_PIN        ' High time in clocks
        dirh    #PWM_PIN

' Change duty cycle on the fly
        wypin   ##new_duty, #PWM_PIN    ' Just update Y parameter
```
:::

### ADC Input

::: pasm2
```
' ADC mode - continuous sampling
        dirl    #ADC_PIN
        wrpin   ##P_ADC | P_ADC_GIO, #ADC_PIN
        wxpin   ##14, #ADC_PIN          ' 14-bit mode
        dirh    #ADC_PIN

' Read ADC value
read_adc
        rdpin   adc_value, #ADC_PIN     ' Get sample
        shr     adc_value, #17          ' Right-justify the result
```
:::

### Quadrature Encoder

::: pasm2
```
' Quadrature decoder - A on pin, B on pin+1
        dirl    #ENC_PIN
        wrpin   ##P_QUADRATURE, #ENC_PIN
        dirh    #ENC_PIN

' Read position
        rdpin   position, #ENC_PIN      ' Get accumulated count
```
:::

## Configuration Values Demystified

The mode values like `P_ASYNC_TX` are constants defined by the assembler. Here's what's happening behind the scenes:

The **WRPIN** D value is a 32-bit configuration:

```{=latex}
\WRPINBitFieldDiagram
```

For most common modes, you'll use predefined constants like `P_ASYNC_TX`, `P_PWM_SAWTOOTH`, `P_ADC`. The P2 assembler knows all of them.

## Common Gotchas

**❌ WRONG: Forgetting to reset before configure**

::: antipattern
```
' WRONG - Pin may be in unknown state!
        wrpin   ##P_PWM_SAWTOOTH, #PIN
        wxpin   ##1000, #PIN
        dirh    #PIN
```
:::

**✓ RIGHT: Always DIRL first**

::: pasm2
```
' RIGHT - Start clean
        dirl    #PIN                    ' Reset first!
        wrpin   ##P_PWM_SAWTOOTH, #PIN
        wxpin   ##1000, #PIN
        dirh    #PIN
```
:::

**❌ WRONG: Enabling before configuring**

::: antipattern
```
' WRONG - Pin enabled with partial config!
        dirl    #PIN
        dirh    #PIN                    ' Enabled too early!
        wrpin   ##P_ASYNC_TX, #PIN
```
:::

**✓ RIGHT: DIRH comes last**

::: pasm2
```
' RIGHT - Configure completely, then enable
        dirl    #PIN
        wrpin   ##P_ASYNC_TX, #PIN
        wxpin   ##BAUD, #PIN
        dirh    #PIN                    ' Enable last!
```
:::

## Medicine Cabinet

::: medicine-cabinet
**Smart Pin Quick Reference**

**The Recipe:**

1. **DIRL** pin — Reset the pin first
2. **WRPIN** mode, pin — Set the operating mode
3. **WXPIN** x, pin — Set X parameter
4. **WYPIN** y, pin — Set Y parameter
5. **DIRH** pin — Enable the Smart Pin

**Common Modes:**

- **UART TX**: `P_ASYNC_TX` — Serial transmit
- **UART RX**: `P_ASYNC_RX` — Serial receive
- **PWM**: `P_PWM_SAWTOOTH` — Sawtooth wave output
- **PWM**: `P_PWM_TRIANGLE` — Triangle wave output
- **ADC**: `P_ADC` — Analog input
- **Quadrature**: `P_QUADRATURE` — Encoder
- **NCO**: `P_NCO_FREQ` — Frequency output

**Data Flow:**

- **WYPIN** = Write data TO Smart Pin
- **RDPIN** = Read data FROM Smart Pin (clears IN)
- **TESTP** = Check if IN flag set

**Golden Rule:** DIRL before WRPIN, DIRH after WXPIN/WYPIN
:::

## Your Turn

::: your-turn
**Exercise 1: PWM LED Dimmer**

Create a PWM output that dims an LED:

1. Configure a pin for PWM sawtooth mode
2. Set a 1 kHz period (at 160 MHz: period = 160,000)
3. Vary duty cycle from 0% to 100%

```pasm2
' Your code here:
' Hint: Change duty with WYPIN new_duty, #LED_PIN
```
:::

::: your-turn
**Exercise 2: Simple Serial Echo**

Set up UART at 115200 baud:

1. Configure RX on pin 63
2. Configure TX on pin 62
3. Echo every received byte back

```pasm2
' Your code here:
' At 160 MHz: baud_divisor = 160_000_000 / 115200 = 1389
' WXPIN format: (divisor << 16) | (bits - 1)
```
:::

📚 **Going Deeper**: This chapter covered the Smart Pin essentials - the configuration pattern and common modes. For complete coverage of all 32 modes, timing diagrams, and advanced techniques, see the dedicated "P2 Smart Pins Manual."

*Continue to [Chapter 15: Event-Driven Programming](#chapter-15-event-driven-programming) →*


# Chapter 15: Event-Driven Programming

*Stop spinning, start waiting*

## The Hook: No More Polling Loops

Remember all those busy loops waiting for things to happen?

::: pasm2
```
' OLD WAY: Spin waiting for serial data (burns CPU cycles!)
wait_rx testp   #RX_PIN wc      ' Check over and over
  if_nc jmp     #wait_rx        ' Spin spin spin...
        rdpin   data, #RX_PIN

' NEW WAY: Sleep until data arrives (zero CPU cycles!)
        setse1  #%001<<6 + RX_PIN  ' Wake on IN rise
        waitse1                     ' Sleep until event
        rdpin   data, #RX_PIN
```
:::

The event system lets your COG sleep while waiting. When the event happens, it wakes up instantly. No cycles wasted, and you respond the moment something happens.

## Why Events Matter

Polling loops have two problems:

1. **They waste cycles** - The COG spins doing nothing useful
2. **They add latency** - You check periodically, so there's delay between "thing happened" and "you noticed"

The event system solves both. Your COG *sleeps* and *wakes the instant* something happens. It's like having a personal assistant tap your shoulder instead of constantly looking up to check.

## The Four Selectable Events

Every COG has four configurable event channels: SE1, SE2, SE3, and SE4. Each can be configured to trigger on different conditions:

| Event | Configuration | Wait | Poll |
|-------|--------------|------|------|
| SE1 | **SETSE1** | **WAITSE1** | **POLLSE1** |
| SE2 | **SETSE2** | **WAITSE2** | **POLLSE2** |
| SE3 | **SETSE3** | **WAITSE3** | **POLLSE3** |
| SE4 | **SETSE4** | **WAITSE4** | **POLLSE4** |

Plus there are built-in timer events:

| Timer | Wait | Poll |
|-------|------|------|
| CT1 | **WAITCT1** | **POLLCT1** |
| CT2 | **WAITCT2** | **POLLCT2** |
| CT3 | **WAITCT3** | **POLLCT3** |

## Configuring an Event

The **SETSE1** through **SETSE4** instructions take a 9-bit configuration value:

```{=latex}
\SETSEBitFieldDiagram
```

### Event Modes

| Mode | Meaning |
|------|---------|
| %000 | Never (disabled) |
| %001 | IN rises (Smart Pin ready) |
| %010 | IN falls |
| %011 | IN changes |
| %100 | Pin high |
| %101 | Pin low |
| %110 | Pin rises |
| %111 | Pin falls |

### EVENT_* Constants: When You Need Interrupts

While dedicated COGs are usually better than interrupts (see Chapter 11), sometimes you need them. The **SETINT1/2/3** instructions select which event triggers an interrupt using these constants:

| Constant | Value | Description |
|----------|-------|-------------|
| `EVENT_INT` | %0000 | Pin matches interrupt configuration |
| `EVENT_CT1` | %0001 | CT equals CT1 (timer 1 target) |
| `EVENT_CT2` | %0010 | CT equals CT2 (timer 2 target) |
| `EVENT_CT3` | %0011 | CT equals CT3 (timer 3 target) |
| `EVENT_SE1` | %0100 | Selectable event 1 triggered |
| `EVENT_SE2` | %0101 | Selectable event 2 triggered |
| `EVENT_SE3` | %0110 | Selectable event 3 triggered |
| `EVENT_SE4` | %0111 | Selectable event 4 triggered |
| `EVENT_PAT` | %1000 | SETPAT pattern detected |
| `EVENT_FBW` | %1001 | Hub FIFO wrapped around |
| `EVENT_XMT` | %1010 | Streamer needs data |
| `EVENT_XFI` | %1011 | Streamer operation complete |
| `EVENT_XRO` | %1100 | NCO frequency counter rolled |
| `EVENT_XRL` | %1101 | Streamer matched pattern |
| `EVENT_ATN` | %1110 | Another COG signaled attention |
| `EVENT_QMT` | %1111 | CORDIC/PIX math complete |

**Using EVENT_* with SETINT:**

::: pasm2
```
' Enable INT1 when SE1 event occurs
        setse1  #%001<<6 + RX_PIN       ' SE1 = IN rise on RX_PIN
        setint1 #EVENT_SE1              ' INT1 fires when SE1 triggers

' Enable INT2 on timer match
        addct2  target, ##200_000       ' Set timer 2 target
        setint2 #EVENT_CT2              ' INT2 fires when CT = CT2

' Enable INT3 when another COG signals
        setint3 #EVENT_ATN              ' INT3 fires on COGATN
```
:::

**Pro tip**: You can also use these constants with WAITSE/POLLSE by first triggering them with the appropriate hardware condition, then waiting. But for most purposes, the SETSE mode bits (the table above this one) are what you'll configure directly.

### Smart Pin Events

The most common use is waiting for a Smart Pin to have data:

::: pasm2
```
' Wait for Smart Pin on pin 15 to be ready
        setse1  #%001<<6 + 15   ' IN rise on pin 15
        waitse1                  ' Sleep until ready
        rdpin   data, #15        ' Get the data
```
:::

### Pin Edge Events

You can also wait for raw pin edges (without Smart Pin):

::: pasm2
```
' Wait for rising edge on pin 5
        setse1  #%110<<6 + 5    ' Rise on pin 5
        waitse1                  ' Sleep until edge
        ' Edge detected!

' Wait for falling edge on pin 10
        setse2  #%111<<6 + 10   ' Fall on pin 10
        waitse2
        ' Edge detected!
```
:::

## Timer Events

For precise timing, use the counter comparison events:

::: pasm2
```
' Wait exactly 1 millisecond (at 200 MHz)
        getct   target          ' Current time
        add     target, ##200_000  ' +1ms at 200MHz
        addct1  target, #0      ' Set CT1 target
        waitct1                  ' Sleep until CT >= CT1

' Alternative using WAITX (simpler but less precise)
        waitx   ##200_000       ' Wait ~1ms at 200MHz
```
:::

The timer events are:

- **ADDCT1/ADDCT2/ADDCT3**: Set the comparison target
- **WAITCT1/WAITCT2/WAITCT3**: Wait until CT reaches target
- **POLLCT1/POLLCT2/POLLCT3**: Check (non-blocking) if target reached

## Waiting vs Polling

Two ways to use events:

### WAIT - Sleep Until Event

::: pasm2
```
        waitse1                 ' COG sleeps here
        ' Wakes instantly when event occurs
```
:::

- COG sleeps, uses no cycles
- Wakes immediately when event fires
- Can't do anything else while waiting

### POLL - Check and Continue

::: pasm2
```
        pollse1 wc              ' Check event, clear if set
  if_c  jmp     #event_handler  ' Handle if occurred
        ' Continue with other work...
```
:::

- COG keeps running
- Checks event flag, clears it
- Returns result in C flag
- Good for servicing multiple events

## Multiple Events

With four SE channels, you can monitor multiple sources:

::: pasm2
```
' Setup multiple events
        setse1  #%001<<6 + RX_PIN     ' Serial data ready
        setse2  #%110<<6 + BUTTON_PIN ' Button pressed
        setse3  #%001<<6 + ADC_PIN    ' ADC sample ready

event_loop
        pollse1 wc              ' Check serial
  if_c  call    #handle_serial

        pollse2 wc              ' Check button
  if_c  call    #handle_button

        pollse3 wc              ' Check ADC
  if_c  call    #handle_adc

        jmp     #event_loop
```
:::

## Practical Examples

### Timeout with Fallback

::: pasm2
```
' Wait for serial data, but give up after 100ms
wait_with_timeout
        setse1  #%001<<6 + RX_PIN     ' Serial ready event

        getct   timeout
        add     timeout, ##16_000_000  ' 100ms at 160MHz
        addct1  timeout, #0

.wait   pollse1 wc              ' Check serial
  if_c  jmp     #.got_data
        pollct1 wc              ' Check timeout
  if_c  jmp     #.timed_out
        jmp     #.wait

.got_data
        rdpin   data, #RX_PIN
        ret

.timed_out
        mov     data, #-1       ' Return error
        ret
```
:::

### Debounced Button Press

::: pasm2
```
' Wait for clean button press with debounce
debounced_button
        setse1  #%110<<6 + BUTTON  ' Rising edge
        waitse1                     ' Wait for press

        waitx   ##2_000_000        ' 10ms debounce at 200MHz

        testp   #BUTTON wc         ' Verify still pressed
  if_nc jmp     #debounced_button  ' Bounce - try again
        ret                         ' Clean press!
```
:::

### Precise Periodic Sampling

::: pasm2
```
' Sample ADC at exactly 10 kHz
sample_loop
        getct   next_sample

.loop   addct1  next_sample, ##16_000  ' 100us period
        waitct1                         ' Wait for next slot

        rdpin   sample, #ADC_PIN        ' Read sample
        wrlong  sample, buffer_ptr      ' Store it
        add     buffer_ptr, #4

        jmp     #.loop
```
:::

## ATN - Inter-COG Events

The ATN (attention) system lets COGs signal each other:

::: pasm2
```
' COG 0: Signal another COG
        cogatn  #%0000_0010     ' Send ATN to COG 1

' COG 1: Wait for attention
        waitatn                  ' Sleep until ATN received
        ' Another COG signaled us!
```
:::

The **COGATN** instruction takes an 8-bit mask where each bit corresponds to a COG. Setting bit N sends attention to COG N.

## Common Gotchas

::: antipattern
**❌ WRONG: Forgetting to clear event flag**

```
' WRONG - Event may fire before you're ready
        setse1  #%001<<6 + PIN
        ' ... do other stuff ...
        waitse1                 ' May return immediately!
```
:::

**✓ RIGHT: Poll first to clear any pending event**

::: pasm2
```
' RIGHT - Clear any stale event
        setse1  #%001<<6 + PIN
        pollse1                 ' Clear if already set
        ' ... do other stuff ...
        waitse1                 ' Now wait cleanly
```
:::

::: antipattern
**❌ WRONG: Using WAIT when you need to handle multiple sources**

```
' WRONG - Can only wait for one event at a time
        waitse1                 ' Stuck here until SE1
        ' SE2 might fire and be missed!
```
:::

**✓ RIGHT: Use POLL loop for multiple events**

::: pasm2
```
' RIGHT - Check all sources
.loop   pollse1 wc
  if_c  call    #handle_se1
        pollse2 wc
  if_c  call    #handle_se2
        jmp     #.loop
```
:::

## Medicine Cabinet

::: medicine-cabinet
**Event System Quick Reference**

**Configure Events:**

::: pasm2
```
        SETSE1/2/3/4  #%MMM_PPPPPP    ' Mode and pin
```
:::

**Event Modes:**

| %MMM | Trigger |
|------|---------|
| %001 | IN rises (Smart Pin ready) |
| %010 | IN falls |
| %011 | IN changes |
| %110 | Pin rises |
| %111 | Pin falls |

**Wait (blocking):**

::: pasm2
```
        WAITSE1/2/3/4    ' Sleep until event
        WAITCT1/2/3      ' Sleep until timer
        WAITATN          ' Sleep until attention
```
:::

**Poll (non-blocking):**

::: pasm2
```
        POLLSE1/2/3/4 WC ' Check event, clear flag, C=occurred
        POLLCT1/2/3 WC   ' Check timer, C=reached
        POLLATN WC       ' Check attention, C=received
```
:::

**Timer Setup:**

::: pasm2
```
        ADDCT1/2/3 target, #delta   ' Set comparison target
```
:::

**Inter-COG:**

::: pasm2
```
        COGATN #mask    ' Signal COGs (bit per COG)
```
:::
:::

## Your Turn

::: your-turn
**Exercise 1: Event-Driven Serial**

Rewrite a serial receive loop to use events instead of polling:

1. Configure SE1 for UART RX Smart Pin ready

2. Use WAITSE1 instead of TESTP loop

3. Measure the cycle count difference

```pasm2
' Your code here:
' Hint: setse1 #%001<<6 + RX_PIN
```
:::

::: your-turn
**Exercise 2: Dual Event Monitor**

Create a loop that monitors both a button (pin edge event) and a timer (periodic event):

1. SE1 = button press (rising edge)

2. CT1 = 1 second heartbeat

3. On button: toggle LED

4. On timer: print timestamp

```pasm2
' Your code here:
' Use POLL for both, handle whichever fires
```
:::

*Continue to [Chapter 16: Multi-COG Orchestration](#chapter-16-multi-cog-orchestration) →*


# Chapter 16: Multi-COG Orchestration

*Bringing it all together in parallel harmony*

## The Hook: A Complete System in 8 COGs

Watch this system architecture come alive:

::: pasm2
```
' Main orchestrator (COG 0)
main_orchestrator
        ' Launch the orchestra (SETQ sets PTRA for new COG)
        setq    @sensor_params
        coginit #1, @sensor_cog
        setq    @motor_params
        coginit #2, @motor_cog
        setq    @comms_params
        coginit #3, @comms_cog
        setq    @display_params
        coginit #4, @display_cog
        setq    @safety_params
        coginit #5, @safety_cog
        setq    @logger_params
        coginit #6, @logger_cog
        setq    @debug_params
        coginit #7, @debug_cog
        
        ' Now coordinate them all
orchestrate
        rdlong  sensor_data, ##SENSOR_MAILBOX wz
   if_nz call   #process_sensor_data
        
        rdlong  command, ##COMMAND_MAILBOX wz
   if_nz call   #execute_command
        
        call    #update_system_state
        wrlong  state, ##STATE_MAILBOX
        
        jmp     #orchestrate
```
:::

Eight independent processors, each with a specific job, all working in perfect coordination. This is the true power of P2!

## Communication Patterns

### The Mailbox Pattern

The simplest and most common:

::: pasm2
```
' Producer COG
producer
        ' Generate data
        call    #calculate_result
        wrlong  result, ##MAILBOX_ADDR
        
' Consumer COG
consumer
        rdlong  data, ##MAILBOX_ADDR wz
   if_z jmp     #consumer              ' Wait for data
        wrlong  #0, ##MAILBOX_ADDR     ' Clear mailbox
        call    #process_data
```
:::

### The Ring Buffer Pattern

For streaming data between COGs:

::: pasm2
```
' Writer COG
writer_cog
        rdlong  wr_ptr, ##WRITE_PTR
        wrlong  data, wr_ptr
        add     wr_ptr, #4
        and     wr_ptr, ##BUFFER_MASK  ' Wrap around
        wrlong  wr_ptr, ##WRITE_PTR
        
' Reader COG  
reader_cog
        rdlong  rd_ptr, ##READ_PTR
        rdlong  wr_ptr, ##WRITE_PTR
        cmp     rd_ptr, wr_ptr wz
   if_z jmp     #reader_cog            ' Buffer empty
        
        rdlong  data, rd_ptr
        add     rd_ptr, #4
        and     rd_ptr, ##BUFFER_MASK
        wrlong  rd_ptr, ##READ_PTR
```
:::

### The Command Queue Pattern

For sending commands between COGs:

::: pasm2
```
' Command structure in hub
' +0: Command ID
' +4: Parameter 1
' +8: Parameter 2
' +12: Result/Status

' Commander COG
send_command
        wrlong  cmd_id, ##CMD_BUFFER+0
        wrlong  param1, ##CMD_BUFFER+4
        wrlong  param2, ##CMD_BUFFER+8
        wrlong  ##$FFFF, ##CMD_BUFFER+12  ' Mark as pending
        
wait_complete
        rdlong  status, ##CMD_BUFFER+12
        cmp     status, ##$FFFF wz
   if_z jmp     #wait_complete
        
' Worker COG
process_commands
        rdlong  status, ##CMD_BUFFER+12
        cmp     status, ##$FFFF wz
  if_nz jmp     #process_commands      ' No command
        
        rdlong  cmd_id, ##CMD_BUFFER+0
        rdlong  param1, ##CMD_BUFFER+4
        rdlong  param2, ##CMD_BUFFER+8
        
        call    #execute_command
        wrlong  result, ##CMD_BUFFER+12   ' Signal complete
```
:::

## Synchronization Techniques

### Using Locks

When multiple COGs need atomic access:

::: pasm2
```
' Atomic increment using lock
atomic_increment
        locktry #COUNTER_LOCK wc
   if_c jmp     #atomic_increment     ' Retry if busy
        
        rdlong  value, ##COUNTER
        add     value, #1
        wrlong  value, ##COUNTER
        
        lockrel #COUNTER_LOCK
```
:::

### Event Synchronization

COGs waiting for specific events:

::: pasm2
```
' COG 1: Signal event
        wrlong  ##EVENT_FLAG, ##EVENT_ADDR
        
' COG 2: Wait for event
wait_event
        rdlong  flag, ##EVENT_ADDR wz
   if_z jmp     #wait_event
        wrlong  #0, ##EVENT_ADDR      ' Clear event
```
:::

## Real-World Example: Robot Controller

Let's build a complete robot control system:

::: pasm2
```
' COG 0: Main Controller
main_controller
        call    #init_system
        
main_loop
        ' Read sensor hub
        rdlong  distance, ##DISTANCE_SENSOR wz
   if_z jmp     #too_close
        
        ' Check for commands
        rdlong  cmd, ##SERIAL_COMMAND wz
   if_nz call   #process_command
        
        ' Update motor speeds
        call    #calculate_motion
        wrlong  left_speed, ##LEFT_MOTOR
        wrlong  right_speed, ##RIGHT_MOTOR
        
        jmp     #main_loop

' COG 1: Ultrasonic Sensor
sensor_cog
        ' Trigger ultrasonic pulse
        drvh    #TRIGGER_PIN
        waitx   ##1000
        drvl    #TRIGGER_PIN
        
        ' Measure echo time - wait for rising edge
.wait_hi
        testp   #ECHO_PIN wz
  if_nz jmp     #.wait_hi
        getct   start_time
.wait_lo                              ' Wait for falling edge
        testp   #ECHO_PIN wz
  if_z  jmp     #.wait_lo
        getct   end_time
        
        ' Calculate distance
        sub     end_time, start_time
        ' Convert to distance...
        wrlong  distance, ##DISTANCE_SENSOR
        
        waitx   ##10_000_000         ' 50ms at 200MHz
        jmp     #sensor_cog

' COG 2: Left Motor Driver
left_motor_cog
        rdlong  speed, ##LEFT_MOTOR wz
   if_z jmp     #left_motor_cog      ' No speed set
        
        ' Generate motor control signals
        ' ... PWM generation code
        jmp     #left_motor_cog

' COG 3: Right Motor Driver
' (Similar to left motor)

' COG 4: Serial Communications
serial_cog
        ' Check for incoming commands
        testp   #RX_PIN wc
  if_nc jmp     #serial_cog
        
        call    #receive_byte
        ' Build command...
        wrlong  command, ##SERIAL_COMMAND
        jmp     #serial_cog

' COG 5: LED Status Display
status_cog
        rdlong  system_state, ##STATE_MAILBOX
        
        ' Display state on LEDs
        cmp     system_state, #STATE_RUNNING wz
   if_z drvh    #GREEN_LED
  if_nz drvl    #GREEN_LED
        
        cmp     system_state, #STATE_ERROR wz
   if_z drvh    #RED_LED
  if_nz drvl    #RED_LED
        
        waitx   ##10_000_000
        jmp     #status_cog

' COG 6: Safety Monitor
safety_cog
        ' Monitor critical systems
        rdlong  battery, ##BATTERY_VOLTAGE
        cmp     battery, ##MIN_VOLTAGE wcz
   if_b wrlong  ##STATE_SHUTDOWN, ##STATE_MAILBOX
        
        ' Check temperature
        rdlong  temp, ##TEMPERATURE
        cmp     temp, ##MAX_TEMP wcz
   if_a wrlong  ##STATE_OVERHEAT, ##STATE_MAILBOX
        
        jmp     #safety_cog

' COG 7: Debug Output
debug_cog
        ' Output system state for debugging
        ' ... debug code
```
:::

Eight COGs, each doing one job perfectly, creating a responsive, reliable robot!

## Your Turn: Multi-COG Project

::: your-turn
**Exercise: Traffic Light Controller**

Requirements:

- COG 0: Main sequencer
- COG 1: North-South lights
- COG 2: East-West lights  
- COG 3: Pedestrian button watcher
- COG 4: Timer/scheduler

Starting structure:

::: pasm2
```
        org     0
' COG 0: Main sequencer
        ' Launch other COGs
        ' Coordinate light changes
        ' Handle pedestrian requests
        
' Your implementation here
```
:::

Goal: Working traffic light with pedestrian crossing
Hint: Use mailboxes for COG communication
Success Check: Lights change correctly, pedestrian button works
:::

::: medicine-cabinet
Multi-COG systems overwhelming? Start simple:

**Start with just 2 COGs:**

::: pasm2
```
' Main + Helper pattern
main    coginit #1, @helper, @params
        ' Main work

helper  ' Support work
```
:::

**Use simple mailboxes:**

::: pasm2
```
' Fixed hub addresses for communication
MAILBOX_1 = $1000
MAILBOX_2 = $1004
```
:::

**Debug one COG at a time:**
Test each COG in isolation before combining!
:::

## Design Principles for Multi-COG Systems

1. **Single Responsibility**: Each COG does ONE thing well
2. **Loose Coupling**: COGs communicate through hub, not direct dependencies
3. **Clear Ownership**: Each piece of data has one writer
4. **Predictable Timing**: Real-time tasks get dedicated COGs
5. **Graceful Degradation**: System continues if one COG fails

## Common Multi-COG Gotchas

1. **Race conditions** - Use locks for shared write access
2. **Deadlocks** - Avoid circular dependencies
3. **Starvation** - Ensure all COGs get resources
4. **Communication overhead** - Don't over-communicate
5. **Debugging complexity** - Use LED indicators for each COG

## What We've Learned

You've mastered multi-COG orchestration:

- ✅ Communication patterns (mailbox, ring buffer, queue)
- ✅ Synchronization techniques
- ✅ Real-world system architecture
- ✅ Design principles
- ✅ Common pitfalls and solutions

This is it - you now understand the full power of the Propeller 2!

## Your Journey Continues

You've completed this manual, but your P2 journey has just begun:

1. **Build something amazing** - Put your knowledge to work
2. **Share with the community** - Your projects inspire others
3. **Explore other manuals** - Smart Pins, Video, I/O await
4. **Push boundaries** - P2 can do things we haven't imagined yet

## Chapter Summary

:::chapterend
**Congratulations!** You've mastered multi-COG orchestration!

You now understand:

- How to coordinate 8 parallel processors
- Communication patterns between COGs
- Synchronization techniques
- Real-world system design

**You did it!** You're now fluent in PASM2 and ready to build incredible parallel systems!
:::


**Have Fun!** 

Remember what you've learned:

- Eight COGs working together are more powerful than any interrupt-driven system
- Parallel processing isn't harder, it's different
- The P2 way is about determinism and elegance
- Every complex system is just simple parts working together

Now go forth and create something amazing with your Propeller 2!


## Epilogue: The Journey Forward

Well, here we are at the end... or should I say, at the beginning?

You've traveled from blinking your first LED to orchestrating eight parallel processors. You've mastered CORDIC mathematics, tamed the FIFO, and learned why interrupts are usually the wrong answer. That's quite a journey!

But here's the secret: everything you've learned is just the foundation. The P2 community continues to discover new techniques, new optimizations, new ways to use this remarkable chip. Every project pushes the boundaries a little further.

### What Makes You Different Now

You're not just another embedded programmer anymore. You think in parallel. You see solutions that others miss. When someone says "that's impossible in real-time," you know better - you just dedicate a COG to it.

### The Community Awaits

The Parallax forums are filled with fellow travelers on this journey. Share your projects. Ask questions. Help newcomers. The community that inspired this manual continues to grow because people like you contribute back.

### One Last Story

I remember my first P2 project. I was trying to control 16 servos with perfect timing while reading sensors and communicating over serial. On my previous microcontroller, it was a nightmare of interrupts and jitter.

On the P2? Three COGs. Clean, simple, perfect timing. That's when I truly understood - this isn't just a different processor, it's a different philosophy of computing.

### Your Challenge

Build something that wouldn't be possible without parallel processing. Something that would be a nightmare of interrupts on other processors. Then share it with the world.

Show them what eight COGs can do.

Show them the Propeller way.


*"The best way to predict the future is to invent it."*  
— Alan Kay

And with your Propeller 2, you have everything you need to invent amazing futures.

**Have Fun!**

— The ghosts of deSilva, the P2 community, and one very enthusiastic AI

*P.S. - Don't forget to blink an LED once in a while, just for old times' sake. It's still magical, even after all you've learned.*


THE END

(But really, just the beginning...)

## Further Reading

This teaching manual focuses on concepts, patterns, and building your understanding. For complete technical specifications, refer to these companion documents:

**Propeller 2 Assembly Language (PASM2) Manual**
: Complete PASM2 instruction details including syntax, timing, and flag effects for all 300+ instructions. Quick lookup reference for day-to-day development.

**Parallax Propeller 2 Documentation** *(v35, Rev B/C silicon, 2021-05-18)*
: Official silicon documentation from Parallax covering hardware specifications, electrical characteristics, and detailed register maps.


# Appendix A: Platform Comparison

*How P2 compares to other microcontrollers*

If you're coming from another embedded platform, this appendix shows how the P2's approach differs and when those differences matter.

## The Landscape

The embedded world is dominated by a handful of architectures:

| Platform | Architecture | Typical Cores | Peripherals | Timing |
|----------|--------------|---------------|-------------|--------|
| **STM32** | ARM Cortex-M | 1-2 | Fixed location | Cache-dependent |
| **ESP32** | Xtensa/RISC-V | 2 | Fixed location | FreeRTOS scheduled |
| **Arduino/AVR** | AVR | 1 | Fixed location | Deterministic but slow |
| **PIC32** | MIPS | 1 | Fixed location | Interrupt-driven |
| **P2 Propeller** | Custom | **8** | **Any pin** | **Deterministic** |

## What Makes P2 Different

### Eight Real Processors, Not Time-Slicing

On ARM, ESP32, or PIC, you typically have 1-2 cores that share time between tasks using interrupts or an RTOS. The P2 gives you eight complete, identical processors that run truly in parallel.

**Traditional approach:**

::: antipattern
```
' Everyone fights for the same CPU
ISR(TIMER1_vect) { motor_control(); }   ' Might delay...
ISR(UART_RX_vect) { serial_handler(); } ' ...this
main() { while(1) { sensor_loop(); } }  ' Hope we get time
```
:::

**P2 approach:**

::: multicog
```
' Each task owns its own processor
COG0: coginit(1, @motor_control)   ' Coordinator launches workers
COG1: motor_control()              ' Dedicated - always on time
COG2: serial_handler()             ' Dedicated - never misses byte
COG3: sensor_loop()                ' Dedicated - consistent sample
COG4-7: ready for more
```
:::

No interrupt priority juggling. No RTOS configuration. Each task owns its processor.

### Smart Pins: Peripherals on Every Pin

Traditional MCUs have fixed peripheral assignments: UART1 is on PA9/PA10, SPI1 is on PB3/PB4/PB5, and if you need those pins for something else, you're stuck rerouting your PCB.

On P2, every pin contains a programmable state machine. Any pin can become a UART, SPI, PWM, ADC, quadrature decoder, or 27 other modes. The peripheral comes to your pin, not the other way around.

### Deterministic Timing

ARM MCUs with cache have unpredictable timing. A memory read might take 1 cycle (cache hit) or 50+ cycles (cache miss). Even instruction timing varies—ARM instructions take 1-3+ cycles depending on the operation. This makes cycle-accurate timing extremely difficult.

P2 takes a different approach: nearly all instructions execute in exactly **2 clock cycles**. Want to know how long a code sequence takes? Count the instructions and multiply by 2. Hub memory uses round-robin access that gives every COG predictable, guaranteed access slots. Your timing loops work identically every time—no cache luck required.

## Coming From ARM/STM32

You're used to configuring HAL structures, writing interrupt handlers, and managing DMA. Here's how P2 solves those problems:

| Instead of... | On P2... | The Benefit |
|---------------|----------|-------------|
| `HAL_UART_Transmit()` | Configure Smart Pin once, then **WYPIN** bytes | Pin handles all timing autonomously |
| `HAL_TIM_PWM_Start()` | Configure Smart Pin once, update with **WYPIN** | Pin runs independently—your COG is free |
| NVIC priority configuration | Nothing needed | All COGs equal, no priority inversion ever |
| `HAL_DMA_Start()` | Use built-in FIFO/Streamer | Simpler API, integrated into each COG |
| `arm_sin_f32()` library | **QROTATE** instruction | Hardware trig in exactly 55 clocks |
| FreeRTOS `xTaskCreate()` | **COGINIT** | True parallel execution, not scheduled |

**The result**: Deterministic timing, zero interrupt conflicts, and I/O configuration that just works.

## Coming From ESP32

You're used to WiFi/Bluetooth convenience and FreeRTOS abstractions. P2 takes a different approach:

| ESP32 Way | P2 Way | The Benefit |
|-----------|--------|-------------|
| Built-in WiFi/BT | Add WizNet or ESP module | You choose your connectivity—or skip it entirely |
| `xTaskCreate()` | **COGINIT** | Not scheduled—truly parallel, guaranteed timing |
| GPIO matrix routing | Smart Pins | 32 modes per pin, far more capability |
| FreeRTOS timing | Deterministic hub | Cycle-accurate timing guaranteed |
| Arduino framework | Spin2/PASM2 | Deeper control, deeper understanding |

**The result**: 8 real cores running simultaneously, timing you can count on, I/O flexibility that eliminates peripheral conflicts.

## Coming From Arduino/AVR

You'll find P2 familiar but dramatically more powerful:

| Arduino Way | P2 Way | The Upgrade |
|-------------|--------|-------------|
| `digitalWrite()` | **DRVH/DRVL** or Smart Pins | Similar syntax, vastly more capability |
| `delay()` blocks everything | **WAITX** or dedicated COG | Timing without blocking other tasks |
| One thing at a time | 8 things truly parallel | Real concurrency, not fake multitasking |
| 8-bit math limits | 32-bit + hardware CORDIC | No more overflow worries, hardware trig |
| Libraries for everything | Growing ecosystem + OBEX | More control, deeper understanding |

**The result**: Graduate from 8-bit limitations to 8 parallel 32-bit processors with hardware math and Smart Pins on every I/O.

## When P2 Is the Right Choice

P2 excels when you need:

- **Multiple real-time tasks** running simultaneously without conflicts
- **Precise timing** that cache misses and interrupts can't disrupt
- **Video or audio generation** requiring cycle-accurate output
- **Flexible I/O** where any pin can become any peripheral
- **Hardware math** for motor control, signal processing, or robotics
- **Multiple motor/servo control** with dedicated COGs per channel
- **Protocol implementation** where Smart Pins handle timing autonomously

## Platform Trade-offs

Every platform makes trade-offs. P2 optimizes for **determinism, parallelism, and flexibility** rather than:

| If you need... | P2's answer |
|----------------|-------------|
| Built-in WiFi/Bluetooth | Add WizNet or ESP module—you choose connectivity |
| Massive library ecosystem | Growing OBEX + helpful community |
| Ultra-low-power sleep | External modules or different platform |
| Lowest unit cost at 100K+ volumes | P2 targets flexibility over commodity pricing |

**The honest reality**: If your project is "connect to WiFi and display data," an ESP32 does that with less effort. But if your ESP32 project is fighting timing jitter, missing deadlines, or running out of peripheral pins—that's exactly what P2 solves.

## Community Resources

While P2's ecosystem is smaller than ARM or Arduino, it's active and welcoming:

**Parallax Forums** - The heart of the P2 community. Chip Gracey (P2's designer) participates actively, answering questions and discussing design decisions. You'll find help from experienced developers who've solved problems you haven't encountered yet.

**P2 Object Exchange (OBEX)** - A library of reusable Spin2 and PASM2 objects covering drivers, protocols, display interfaces, and more. Before writing something from scratch, check OBEX—someone may have already done the work.

**Community Support** - Unlike large platforms where your question disappears in a sea of posts, the P2 community is small enough that questions get noticed and answered. Many community members have decades of Propeller experience.

Coming from Arduino's library-for-everything culture, you'll write more code yourself—but you'll understand it deeply, and help is always available when you get stuck.

## The P2 Hardware Ecosystem

P2 isn't just a chip - it's a platform with expansion options:

**Video & Audio:**

- A/V Breakout Board: VGA, RCA, 80mW stereo, microphone input
- Digital Video Out: HDMI-type with differential signaling
- Built-in 8-bit DAC per pin (16-bit with dithering)

**Connectivity:**

- USB Host Board: Two USB-A ports
- USB Device Board: HID or CDC modes
- Serial Host/Device: RS-232 interfaces
- WizNet/ESP modules: Ethernet or WiFi

**Development:**

- P2 Eval Board: Complete development environment
- Edge Modules: 4MB or 32MB flash for embedding
- Breakout Boards: All 64 pins accessible

You add what you need - no paying for peripherals you won't use.

## Summary

P2 represents a fundamentally different approach to embedded computing—one that eliminates entire categories of problems:

- **Eight processors** means your motor control never delays your serial handler
- **64 Smart Pins** means peripheral conflicts become impossible
- **Deterministic timing** means your code works the same way every time
- **Hardware CORDIC** means real-time math without floating-point libraries

Engineers who've fought interrupt priority inversions, missed timing deadlines, and PCB rework due to peripheral conflicts find P2 refreshing. You spend your time solving your actual problem, not fighting your MCU.

**Welcome to the P2 community.** You've got 8 processors, 64 Smart Pins, and a community that's been building amazing things since the original Propeller. Time to see what you can build.


# Index

### A
- ADC operations: Ch14
- ADD instruction: Ch3, Ch5
- ADDCT1/2/3: Ch15
- Address modes: Ch3
- ALTD/ALTS: Ch3
- Architecture: Ch2
- Assembly basics: Ch3

### B
- Bit manipulation: Ch3
- Block transfers: Ch4, Ch9
- Booleans: Ch3

### C
- C flag: Ch6
- CALL/RET: Ch3
- Clock timing: Ch2
- CMP instruction: Ch6
- COG anatomy: Ch2
- COG communication: Ch2, Ch16
- Conditional execution: Ch3, Ch6
- CORDIC: Ch7
- Counters: Ch2

### D
- DAC operations: Ch14
- Debugging: Ch12
- Division: Ch5
- DRVH/DRVL: Ch1

### E
- Egg beater: Ch2, Ch4
- Event system: Ch15

### F
- FIFO: Ch4, Ch9
- Flags: Ch6
- Flow control: Ch3

### G
- GETQX/GETQY: Ch5, Ch7

### H
- Hardware multiply: Ch5
- Hub execution: Ch10
- Hub memory: Ch2, Ch4

### I
- IN flag: Ch14, Ch15
- Immediate values: Ch3
- Instruction format: Ch3
- Interrupts: Ch11

### J
- JMP instruction: Ch3

### L
- LED control: Ch1
- Locks: Ch2, Ch16
- Logic operations: Ch3
- LUT memory: Ch13
- LUT sharing: Ch13

### M
- Mailboxes: Ch2, Ch16
- Mathematics: Ch5
- Memory access: Ch4
- MOV instruction: Ch3
- MUL/MULS: Ch5
- Multi-COG: Ch16

### O
- Optimization: Ch12

### P
- Parallel processing: Ch2
- Pipeline: Ch7, Ch12
- Pins, Smart: Ch8, Ch14
- Platform comparison: Appendix A
- POLLSE1-4: Ch15
- PTRA/PTRB: Ch3, Ch4
- PWM: Ch8, Ch14

### Q
- Q flag: Ch7
- QDIV: Ch5
- QROTATE: Ch7

### R
- RDBYTE/RDWORD/RDLONG: Ch4
- RDLUT/WRLUT: Ch13
- RDPIN: Ch14, Ch15
- REP instruction: Ch3
- Rotation: Ch3, Ch7

### S
- SETSE1-4: Ch15
- Shift operations: Ch3
- SKIP instruction: Ch3, Ch6
- Smart Pins: Ch8, Ch14
- Streamer: Ch9, Ch13

### T
- Timer: Ch2
- Timing: Ch2, Ch12
- Trigonometry: Ch7

### U
- UART: Ch8, Ch14

### V

### W
- WAITSE1-4: Ch15
- WAITCT1-3: Ch15
- WAITX: Ch1
- WRBYTE/WRWORD/WRLONG: Ch4
- WRPIN/WXPIN/WYPIN: Ch14

### Z
- Z flag: Ch6
