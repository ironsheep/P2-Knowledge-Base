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
{\large August 2026\par}
\vspace{0.2cm}
{\large\color{blue}Version 3.0.6\par}

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
\item \textcolor{green!50!black}{\textbf{Green}} -- PASM2
\item \textcolor{blue!60!black}{\textbf{Blue}} -- Spin2
\item \textcolor{purple!60!black}{\textbf{Purple}} -- CORDIC
\item \textcolor{teal!70!black}{\textbf{Teal}} -- Multi-Cog
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

```{=latex}
\markboth{}{}
```

Copyright © 2025-2026 Iron Sheep Productions, LLC and Parallax Inc.

This work is licensed under the Creative Commons Attribution–ShareAlike 4.0 International License (CC BY-SA 4.0).

You are free to:

- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:

- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

To view the full license, visit: https://creativecommons.org/licenses/by-sa/4.0/

### Trademarks

Propeller, Propeller 2, P2, Spin, and the Parallax logo are trademarks of Parallax Inc. This license grants permissions under copyright only; it does not grant rights to use these trademarks, and adapted or redistributed copies must not imply endorsement by, or official status with, Iron Sheep Productions, LLC or Parallax Inc.

### Disclaimer

The information in this manual is subject to change without notice. While every effort has been made to ensure accuracy, the authors and publishers assume no responsibility for errors or omissions, or for damages resulting from the use of the information contained herein.


# Dedication

**To deSilva** — *Whose legendary P1 assembly tutorial taught a generation of programmers that assembly language could be approachable, enjoyable, and even fun. Your unique voice—combining technical precision with human warmth—showed us that great documentation teaches not just the mind, but speaks to the spirit of discovery.*

**To the Propeller Community** — *Who have spent countless hours exploring, documenting, and sharing their knowledge. From the early P1 pioneers to today's P2 innovators, your collective wisdom makes this manual possible.*

**To Future Makers** — *May you find in these pages the same joy of discovery that we experienced. The Propeller 2 is more than a microcontroller—it's an invitation to think differently about computing. Welcome to the journey.*

*"The best way to predict the future is to invent it."* — Alan Kay


# Acknowledgments

**deSilva** - For creating the gold standard of microcontroller documentation with the P1 Assembly Tutorial. Your pedagogical approach, combining technical depth with human empathy, remains unmatched. This manual attempts to honor your legacy while adapting to the P2's capabilities.

**Chip Gracey** - Creator of the Propeller architecture. Thank you for giving us a microcontroller that thinks differently and challenges us to do the same.

### Community Contributors

**The Parallax Forums Community** - Your questions, answers, code examples, and endless experimentation have created a living knowledge base that no single author could match.

**Early P2 Adopters** - Who dealt with evolving documentation, changing specifications, and still produced amazing projects that showed us what was possible.

### Production Notes

This manual was created using:

- Knowledge extracted from official Parallax technical documentation and OBEX (Object Exchange) community contributions
- AI-assisted authorship in the style of deSilva's P1 Assembly Tutorial, with every example compiled
- Community validation and real-world testing
- A commitment to making parallel processing accessible to everyone

Any errors, omissions, or dad jokes that fell flat are entirely the responsibility of the authors, not our distinguished contributors.


# Preface: Welcome to the Journey

Well, here we are! You're about to embark on a journey into the heart of the Propeller 2, and I promise you, it's going to be quite different from what you might expect.

### A Different Kind of Processor

The Propeller 2 isn't just another microcontroller. Oh no, it's something far more interesting. Imagine, if you will, eight independent processors (we call them cogs) all working together in perfect harmony, sharing a common memory space, yet each running their own programs at full speed. No interrupts fighting for attention, no complex priority schemes, just eight brains working in parallel.

And if you think this sounds terribly complicated, you're probably right... but here's the secret: the thing that usually makes embedded work hard — deciding which task gets the processor, and when — largely goes away. You give a task its own cog, and it simply runs. Learning the P2 is real work, and Appendix A is honest about where that work is; this is what you get for it.

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

**The Reference Approach** — Already know what you're looking for? The table of contents and index are your friends. The appendices contain every instruction, every smart pin mode, every CORDIC operation.

### What Makes the P2 Special?

Let me count the ways:

- **8 symmetric cogs** - No master/slave relationships, all cogs are equal
- **64 smart pins** - Each pin has its own processor for I/O operations
- **CORDIC engine** - Hardware trigonometry and coordinate transformations
- **Hardware multiply/divide** - Finally! Real math at hardware speed
- **512KB of RAM** - Shared by all cogs with deterministic access timing
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

**Instead of one processor fighting with interrupts**, you get eight complete, identical processors (cogs) that run truly in parallel. Your serial handler never delays your motor control. Your sensor sampling never misses a deadline. Each task owns its own processor.

**Instead of fixed peripherals**, every one of the 64 pins contains its own programmable state machine. Any pin can become a UART, PWM output, quadrature encoder, ADC - whatever you need, wherever you need it.

**Instead of timing that depends on cache luck**, the hub memory has deterministic access. Your timing loops work the same way every time.

**Instead of calling math libraries**, there's a hardware CORDIC that gives you sine, cosine, and arctangent (via vector rotate and convert) with results ready about 55 clocks after the solver takes your command.

Does this mean P2 is perfect for everything? Of course not. But if your projects involve multiple real-time tasks, precise timing, video or audio generation, or just running out of peripheral pins - you're in the right place.

For a full comparison to ARM, ESP32, Arduino, and PIC platforms, see [Appendix A](#appendix-a-platform-comparison). But you probably want to blink that LED first, don't you?

## The Hook: Making Light

I know you're absolutely crazy to have your first instruction executed, so let's not waste any time. Here's a complete PASM2 program that blinks an LED on pin 56 (that's the built-in LED on the P2 Eval board):

```pasm2
CON
  _clkfreq = 200_000_000        ' 200 MHz system clock

DAT
' LED Blinker - Your first PASM2 program!
        org     0               ' Start at cog address 0

        drvh    #56             ' Drive pin 56 high (LED on)
        waitx   ##50_000_000    ' Wait 0.25 seconds at 200MHz
        drvl    #56             ' Drive pin 56 low (LED off)
        waitx   ##50_000_000    ' Wait 0.25 seconds
        jmp     #$-6            ' Jump back 6 longs (## adds hidden AUGD)
```

That's it! Five lines of code and you have a blinking LED. Load this into any cog and watch the magic happen.

::: sidetrack
### Which Pin Is *Your* LED?

Before you go further: **pin 56 is not universal.** Every example in this book says 56, because that is the built-in LED on the P2 Eval board I'm writing against. Your board may disagree, and a perfectly correct program blinking a pin with no LED on it is a demoralizing way to start.

The P2 Edge modules put their two buffered LEDs on different pins depending on which module you have:

| Board | LED pins |
|-------|----------|
| P2 Edge Module (P2-EC) | P56, P57 |
| P2 Edge 32MB PSRAM Module (P2-EC32MB) | **P38, P39** |
| P2 Eval Board (#64000) | P56-P63 (P56, P57 free) |

That difference is not cosmetic. On the 32MB module, P56 and P57 are the PSRAM **clock** and **chip-enable** lines - so `drvh #56` there doesn't light anything, and it *does* stamp on the memory bus. Change the pin number, don't fight it.

Two more things that will save you an evening:

- Both Edge modules have a bank of mini DIP switches, one of which is labelled **LED**. It gates power to those LEDs, and it is labelled ON/OFF - it must be **ON**. If it's off, your code is fine and your LEDs are dark.
- Those LED pins sit in a **high-impedance** state until you drive them, and they're sensitive to nearby objects. Which brings us to a trick of the light worth knowing about...
:::

::: sidetrack
### Why Your LEDs Glow When You Touch Them

You may notice - before running any code at all - that brushing a pin with a finger, or clipping on a scope probe, or just draping a long wire nearby, lights an onboard LED. Nothing is broken. You have not damaged anything.

The key is that these LEDs are **buffered**. Your P2 pin doesn't feed the LED directly; it feeds the *input* of a buffer, and the buffer drives the LED from board power when that input goes high. That buffer is what keeps the LEDs from loading down your signals - but its input is a high-impedance node, and out of reset your P2 pin isn't driving it either. A pin in that state is an antenna, and you - or your probe lead - are a fairly good one at mains frequency. It takes very little to push that floating input past the buffer's threshold, and when it crosses, the buffer switches: the LED doesn't glimmer, it comes **on**.

This isn't a quirk anyone is embarrassed about - the P2 Edge module guides say so outright, noting that because the P2's pins are high-impedance by default, "the LEDs will be sensitive to objects moving close to" those pins. It's the price of a deliberate trade: the buffer keeps the LEDs from loading those pins, so they stay completely free for you to use.

On the P2 Eval board there's a second, entirely unmysterious reason for lit LEDs. The LEDs on **P58 through P63** are shared with the USB data lines and the memory signals, so they're genuinely busy during boot and after every reset. That's the board working, not a fault. P56 and P57 are the two left free for you.

The cure is the same as the lesson: **a floating pin has no opinion.** The moment your code executes `drvh` or `drvl`, the cog's output driver wins and the flicker stops. If you want a pin held at a known level *without* driving it, the P2 gives you pull-ups and pull-downs for exactly that. Uff - your first piece of real hardware intuition, and you got it by accident.
:::

## What's Really Happening

Well, now that you've seen it work (you did try it, right?), let's talk about what's actually going on here.

### The Instructions Decoded

**`org 0`** - This tells the assembler to start placing code at cog address 0. Every cog has its own private 512 longs (2KB) of memory, and execution always starts at address 0 when a cog is loaded.

**`drvh #56`** - This drives pin 56 high (3.3V). The 'h' means high. The '#' means we're using an immediate value (the actual number 56) rather than the contents of register 56. One instruction, and your LED is on!

**`waitx ##50_000_000`** - This waits for 50 million clock cycles. At 200 MHz, that's 0.25 seconds. Notice the double '##'? That means this is a 32-bit immediate value. Single '#' only gives us 9 bits.

**`drvl #56`** - Drive low. LED off. You get the pattern.

**`jmp #$-6`** - Jump back 6 longs. The '$' means "current address", so '$-6' means "6 addresses back from here". Why 6? Each `##` immediate generates a hidden AUGD instruction (it augments the `waitx` destination operand), so we have 6 longs total: drvh, AUGD, waitx, drvl, AUGD, waitx. Infinite loop achieved!

### But Wait, There's More!

"Hold on," you might say, "how does this even get into the cog?"

Ah, excellent question! In the real world, you'd typically launch this from Spin2 (the high-level language) like this:

```{.spin2 caption="ch01-first-blink.spin2"}
CON
  _clkfreq = 200_000_000  ' 200 MHz system clock

PUB main()
    coginit(COGEXEC_NEW, @blink_code, 0)  ' Start PASM2 in new cog
    repeat  ' Keep the main cog alive

DAT
        org     0
blink_code
        drvh    #56
        waitx   ##50_000_000
        drvl    #56
        waitx   ##50_000_000
        jmp     #$-6
```

The **COGINIT** instruction loads your PASM2 code from hub memory into a fresh cog and starts it running. Meanwhile, your Spin2 code keeps running in its own cog. You now have parallel processing!

::: sidetrack
### The Clock Preamble

Notice the `CON` section at the top of that example? Every P2 program needs to configure its system clock:

```pasm2
CON
  _clkfreq = 200_000_000  ' 200 MHz system clock
```

This tells the P2 to run at 200 MHz using your board's crystal oscillator. Without it, the chip runs on its internal RCFAST oscillator—nominally ~24 MHz (spec'd at 20 MHz minimum)—and timing-dependent code (including DEBUG output) won't behave as expected.

At 200 MHz with most instructions taking 2 clocks, each cog executes approximately 100 million instructions per second (100 MIPS). With 8 cogs running in parallel, that's 800 MIPS of total processing power—and that's before smart pins start handling I/O autonomously.

**From here on, we'll omit this preamble from examples to keep them focused on the concept being taught.** When you create your own files, always include it at the top before your `PUB` or `DAT` sections.
:::

## Let's Make It Better

The blinker works, but it's a bit rigid, isn't it? What if we want to change the blink rate? Let's use a register:

```pasm2
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

Uff! Look at that - we're using a register now! The **MOV** instruction copies our delay value into a register (which we cleverly named 'delay'). Now we can change the blink rate by modifying just one value.

*A note on terminology: P2 documentation often uses "register" to refer to any long in cog RAM. Unlike ARM or x86 where registers are a small, special set (R0-R15, EAX, etc.), every cog RAM location can be used as a general-purpose register. However, the last 16 locations (496-511) have special functions: addresses 496-503 are dual-purpose (usable as RAM if interrupts aren't used), and 504-511 are special-purpose registers (PTRA, PTRB, DIRA, DIRB, OUTA, OUTB, INA, INB). When you see "register" in P2 context, think "cog RAM location."*

## Understanding Cogs

Here's something important: each cog is a complete processor with its own memory. When we loaded our blink program, it was copied from hub memory into cog memory. The cog then executes it independently, without any further connection to hub memory (unless we explicitly read or write to it).

Think of it like this:

- **Hub memory** is the meeting place (512KB shared by all)
- **Cog memory** is private workspace (2KB per cog)
- Loading a cog is like making a photocopy - the cog gets its own copy to run

This is why our blinker keeps running even after the Spin2 code that launched it goes into an infinite repeat loop. The cog is independent!

## Your Turn: Experiments

Now for the fun part. Try these modifications:

### Experiment 1: Different Patterns
Make the LED blink in a pattern: short-short-long (like SOS):

```pasm2
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

### Experiment 2: Multiple LEDs
Blink LEDs on pins 56 and 57 alternately:

```pasm2
        org     0
        
.loop   drvh    #56                    ' LED 56 on
        drvl    #57                    ' LED 57 off
        waitx   ##50_000_000           ' 0.25 sec at 200 MHz

        drvl    #56                    ' LED 56 off
        drvh    #57                    ' LED 57 on
        waitx   ##50_000_000           ' 0.25 sec at 200 MHz

        jmp     #.loop
```

### Experiment 3: Fading (Advanced)
This one's a bit tricky - we'll use PWM to fade the LED:

```pasm2
        org     0
        
        dirl    #56                    ' Reset the pin before configuring
        wrpin   ##P_PWM_TRIANGLE | P_OE, #56 ' PWM mode, output enabled
        wxpin   ##$0100_0001, #56      ' Frame = 256 base periods
        dirh    #56                    ' Enable the pin
        
.fade   wypin   level, #56             ' Set duty cycle
        waitx   ##1_000_000            ' ~1.3 s per ramp at 200 MHz
        add     level, #1              ' Increment brightness
        and     level, #$FF            ' Wrap at 256
        jmp     #.fade
        
level   long    0
```

What you should see: the LED climbs from dark to full over about a second and a third, then **snaps** back to dark and climbs again. That snap is `and level, #$FF` rolling 255 back to 0 in a single step - the brightness ramp is a sawtooth. Don't let the mode name mislead you: `P_PWM_TRIANGLE` describes the counter *inside* the smart pin, running at hundreds of kilohertz, not the shape of the brightness you see. If you'd rather it breathed in and out, ramp `level` back down instead of letting it wrap.

Don't worry if the PWM example seems complex - we'll cover smart pins in detail in Chapter 14!

One piece of it is worth pointing at now, though, because it bites everybody once: the `| P_OE`. **DIRH** starts the smart pin, but it does *not* connect the smart pin to the pin's output driver - `P_OE` does. Leave it out and the smart pin dutifully generates your waveform and drives it precisely nowhere. The LED just sits there, dark, and the code looks perfect.

::: medicine-cabinet
Feeling overwhelmed? Here's the simplified prescription:

**Minimum viable blinker** - Just 3 instructions:

```pasm2
.loop   drvnot  #56          ' Toggle pin 56
        waitx   ##50_000_000 ' 0.25s at 200MHz
        jmp     #.loop       ' Repeat
```

The **DRVNOT** instruction toggles a pin - if it's high, make it low; if it's low, make it high. Sometimes simpler is better!
:::

::: sidetrack
### Why Start at Address 0?

You might wonder why cog code always starts at address 0. It's actually quite elegant:

When a cog is started with `coginit`, the hardware:

1. Stops the cog (if it was running)
2. Copies 504 longs from hub to cog memory (addresses 0-503); the top 8 (504-511) are special hardware registers, not loaded
3. Starts execution at cog address 0

This means every cog program starts fresh, with a clean slate. No residual state, no confusion. It's like each cog gets a fresh brain transplant every time it starts!

The last 16 longs (addresses 496-511) have special functions: 496-503 are dual-purpose (usable as RAM if interrupts not used), and 504-511 are special-purpose registers (PTRA, PTRB, DIRA, DIRB, OUTA, OUTB, INA, INB). We'll explore these later.
:::

## Common Gotchas

Before we move on, let me save you some debugging time:

1. **Forgetting the ##** - Using `waitx #25_000_000` will NOT wait for 0.25 seconds! Single # only allows values up to 511.

2. **Wrong pin number** - The P2 Eval board's eight LEDs are on pins 56-63. The P2 Edge Standard Module has two LEDs on pins 56-57; the 32MB Edge Module uses 56-57 for its PSRAM and places its two LEDs on pins 38-39 instead.

3. **Clock setup required** - P2 boots on its internal RCFAST oscillator (nominally ~24MHz, spec'd 20MHz minimum). Most programs configure 200MHz with a crystal. Our examples assume 200MHz - adjust **WAITX** values if your clock differs.

4. **Cog already running** - If you `coginit` to a specific cog that's already running something else, it will be stopped and replaced. Use `COGEXEC_NEW` to automatically find a free cog.

## What We've Learned

Let's celebrate what you've accomplished:

- ✅ Written your first PASM2 program
- ✅ Controlled hardware (LED) directly
- ✅ Used immediate values (# and ##)
- ✅ Created loops with JMP
- ✅ Understood cog independence
- ✅ Modified code for different patterns

That's quite a lot for Chapter 1!

## Coming Up Next

In Chapter 2, we'll take our "Architecture Safari" and explore:

- How 8 cogs really work together
- The hub memory system and the "egg beater"
- Why the P2 doesn't need interrupts
- How to make cogs talk to each other

But for now, enjoy your blinking LED. You've just taken your first step into parallel processing!


**Have Fun!** And remember, every expert was once a beginner who kept their LED blinking when everyone else gave up.




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
- No priorities (all cogs are equal)
- Deterministic timing (you know EXACTLY when things happen)
- True parallel processing (not time-slicing)

It's like the difference between one stressed-out juggler trying to keep eight balls in the air versus eight relaxed people each tossing one ball. Which seems simpler?

## Cog Anatomy 101

Let's dissect a cog and see what makes it tick:

```{=latex}
\CogAnatomyDiagram
```

But here's the beautiful part: Cogs are identical. There's no "master" cog or "special" cog. Any cog can do anything any other cog can do. Democracy in silicon!

### The 512-Long Limit

Each cog has exactly 512 longs (2048 bytes) of memory. The first 496 longs ($000–$1EF) are yours to use for code and data. The last 16 ($1F0–$1FF) have special roles: $1F0–$1F7 can serve as ordinary registers or hold the interrupt vectors and the PA/PB parameters, and $1F8–$1FF are the special-purpose registers (PTRA/PTRB, the I/O registers, and friends) — but not like P1; we'll get to that.

"Only 496 instructions?" you might cry. "That's tiny!"

Well, yes and no. Remember:

1. PASM2 instructions are powerful - one instruction often does what takes several in other processors
2. You have EIGHT of these cogs
3. There's hub execution mode for larger programs (Chapter 10)
4. Most real-time tasks fit easily in 496 instructions

Think of it like haiku - the constraint forces elegance.

## Meet the Hub: The Meeting Place

The hub is where cogs come together. It's 512KB of RAM shared by all cogs, and it's where the magic of cooperation happens.

```{=latex}
\HubMemoryDiagram
```

### The Egg Beater Revolution

Now here's where P2 gets clever. In P1, cogs took turns accessing the hub in a round-robin fashion. If you missed your slot, you waited for the wheel to come around again.

P2 uses what we call the "egg beater" model. Imagine eight beaters (cogs) all whipping through the same bowl (hub) simultaneously, but their paths are cleverly arranged so they never collide:

```{=latex}
\EggBeaterDiagram
```

The practical result? Hub access is MUCH faster and more predictable. Instead of waiting up to 16 clocks (P1), you wait at most 7 clocks (#cogs-1) to reach your hub slice on the P2, and often less if you align your accesses properly.

## Let's See Cogs in Action

Here's a simple demonstration of multiple cogs working together:

```{.spin2 caption="ch02-multicog-blink.spin2"}
' Multi-cog LED Pattern Demo
PUB main() | i
    repeat i from 0 to 3
        coginit(COGEXEC_NEW, @cog_code, 56 + i)  ' Start 4 cogs
    repeat  ' Main cog just watches

DAT
        org     0
cog_code
        mov     pin_num, ptra          ' Pin number was passed in via PTRA

.loop   drvnot  pin_num                ' Toggle our LED
        shl     pin_num, #24           ' Pin number to bits 24-31
        or      pin_num, ##10_000_000  ' Combine with delay
        waitx   pin_num                ' Wait (varies per cog!)
        shr     pin_num, #24           ' Restore pin number
        jmp     #.loop

pin_num long    0
```

What's happening here:

1. The main Spin2 code starts 4 cogs
2. Each cog gets a different pin number (56, 57, 58, 59)
3. Each cog blinks its LED at a slightly different rate
4. All four LEDs blink independently and simultaneously!

## Cog Communication: How They Talk

Cogs are independent, but they're not isolated. They can communicate through hub memory:

### Method 1: Simple Variables

```pasm2
' cog 1: Writer
        mov     value, #42
        wrlong  value, ##$1000  ' Write to hub address $1000

' cog 2: Reader  
        rdlong  result, ##$1000 ' Read from hub address $1000
```

### Method 2: Locks (When It Matters)

When multiple cogs might write to the same location, we need locks:

```pasm2
' Get a lock
.try_lock
        locktry lock_id wc     ' Try to get lock (C=1 if we got it)
  if_nc jmp     #.try_lock     ' Keep trying until we get it

        ' Critical section - we have the lock!
        rdlong  value, ##shared_addr
        add     value, #1
        wrlong  value, ##shared_addr

        lockrel lock_id        ' Release the lock

lock_id long    0              ' Lock 0-15
```

### Method 3: Mailboxes (Elegant)

A mailbox is just a hub location where cogs leave messages:

```pasm2
' cog A: Leave a message
        wrlong  message, ##mailbox
        
' cog B: Check for messages
.check  rdlong  data, ##mailbox wz
   if_z jmp     #.check        ' Keep checking if empty
        wrlong  #0, ##mailbox  ' Clear mailbox
        ' Process the message in 'data'
```

## The Timer: Everyone Gets One

Every cog reads the same free-running 64-bit system counter (with **GETCT**), and each cog has its own CT1/CT2/CT3 compare targets to schedule timed events against it. This is incredibly useful:

```pasm2
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

The beauty? Each cog has its own CT1/CT2/CT3 compare targets, so your timed waits never collide with another cog's. No shared-resource conflicts!

## Why No Interrupts? (Usually)

Here's a controversial P2 feature: it HAS interrupts, but you probably shouldn't use them. Why?

Because with 8 cogs, you don't need interrupts! Instead of interrupting important work, just dedicate a cog to monitoring whatever would have triggered the interrupt:

```pasm2
' Traditional (with interrupts):
' Main code runs, gets interrupted, handles event, returns

' Propeller way:
' cog 1: Main code runs uninterrupted
' cog 2: Watches for event continuously
pin_watcher
        testp   #BUTTON_PIN wc
   if_c jmp     #button_pressed
        jmp     #pin_watcher
        
button_pressed
        wrlong  ##1, ##button_flag  ' Signal other cogs
        jmp     #pin_watcher
```

No interrupt latency, no context switching, no priority inversion. Just dedicated, deterministic monitoring.

## Real-World Example: Parallel Sensors

Let's read four different sensors simultaneously:

```pasm2
' Each cog runs this with different parameters
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

Four cogs running this code = four sensors being read truly simultaneously. Try doing that with a single processor and interrupts!

::: medicine-cabinet
Feeling overwhelmed by all this parallel processing? Here's your prescription:

**Start simple**: Use just one or two cogs at first

```spin2
' Just two cogs - main program and one helper
PUB main()
    coginit(COGEXEC_NEW, @helper, 0)
    ' Your main code here
```

**Debug one cog at a time**: Get each cog working alone before combining

```pasm2
' Test cog in isolation first
debug_cog
        drvh    #MY_DEBUG_LED  ' Visual confirmation it's running
        ' Your actual code here
```

**Use Spin2 for coordination**: Let the high-level language handle the complex stuff

```spin2
' Spin2 manages cogs, PASM2 does the real-time work
PUB orchestrator()
    startSensorCog(0)
    startMotorCog(1)
    startCommsCog(2)
    ' Spin2 coordinates, PASM2 executes
```
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

1. **Cog RAM is copied, not shared** - Changes in cog RAM don't affect hub RAM unless you explicitly write them back

2. **Cog-exec cogs start at cog address 0** - Always! Your code better be there. (A hub-exec cog instead starts at the hub address you pass to COGINIT.)

3. **Hub addresses are byte addresses** - cog addresses are long addresses. Don't mix them up!

```pasm2
   rdlong  value, ##$1000  ' Reads from hub byte address $1000
   mov     value, $100     ' Moves from cog long address $100 (256)
   ' Note: cog RAM is only 512 longs ($000-$1FF)!
```

4. **PTRA/PTRB are your friends** - These special registers make hub access much easier

5. **Cogs are truly independent** - Stopping one cog doesn't affect others (unless they're waiting for it)

## What We've Learned

Look at what you now understand:

- ✅ Why eight processors is simpler than one with interrupts
- ✅ How cogs are structured and limited
- ✅ The hub memory system and egg beater access
- ✅ Multiple ways for cogs to communicate
- ✅ Why interrupts are usually unnecessary
- ✅ How to think in parallel

## Your Turn: Experiments

### Experiment 1: Cog Counter
Start cogs to increment different hub locations. With COGEXEC_NEW, the loop will start up to 7 new cogs (since cog 0 runs Spin2):

```{.spin2 caption="ch02-hub-counters.spin2"}
PUB main() | i
    repeat i from 0 to 7
        coginit(COGEXEC_NEW, @counter, $1000 + (i * 4))
    repeat
        ' Monitor the counters in hub RAM
        
DAT
        org     0
counter mov     hub_ptr, ptra          ' Our hub address arrived in PTRA
.loop   rdlong  value, hub_ptr
        add     value, #1
        wrlong  value, hub_ptr
        waitx   ##1_000_000
        jmp     #.loop
        
hub_ptr long    0
value   long    0
```

### Experiment 2: Parallel Pattern
Make 8 LEDs display a moving pattern, with each cog controlling one LED:

```pasm2
' Each cog gets a 2-long parameter block (pin, delay) in ptra
' (COGINIT passes just ONE value—the PTRA pointer—so pack both into hub)
        org     0
        rdlong  pin, ptra[0]
        rdlong  delay, ptra[1]   ' Different delay per cog
        
.flash  drvh    pin
        waitx   delay
        drvl    pin
        waitx   delay
        shl     delay, #1        ' Double the delay
        cmp     delay, ##100_000_000 wcz
   if_a mov     delay, ##1_000_000  ' Reset if too long
        jmp     #.flash
```

## Coming Up Next

In Chapter 3, "Speaking PASM2", we'll dive deep into the instruction set:

- The anatomy of an instruction
- Conditional execution that will blow your mind
- Math operations that actually make sense
- Why PASM2 is unlike any assembly you've used

But for now, appreciate what you've learned: you understand the Propeller's parallel philosophy. That's not just technical knowledge - it's a new way of thinking about computing.


**Have Fun!** Remember, parallel processing isn't harder - it's different. And different can be wonderful.




# Chapter 3: Speaking PASM2

*Learning the native tongue*

## The Hook: One Instruction, Many Powers

Look at this single PASM2 instruction:

```pasm2
        add     value, #1 wc
```

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

The **MOV** family - your bread and butter:

```pasm2
' Basic move
        mov     dest, source    ' dest = source
        mov     x, #42         ' x = 42 (immediate)
        mov     x, ##70000     ' x = 70000 (32-bit immediate)

' But wait, there's more!
        not     dest, source    ' dest = NOT source (inverted)
        abs     dest, source    ' dest = |source|
        neg     dest, source    ' dest = -source

' And the mind-blowing ones
        altd    dest, source    ' Modify NEXT inst's dest field!
        alts    dest, source    ' Modify NEXT inst's source field!
```

Well, that escalated quickly! Don't worry about **ALTD**/**ALTS** yet - just know they exist and they're amazing.

### Math Without Tears

P2 has hardware multiply and divide. Let that sink in. Hardware. Multiply. And. Divide.

```pasm2
' Addition and subtraction
        add     x, y           ' x = x + y
        sub     x, y           ' x = x - y
        adds    x, y           ' Signed add
        subs    x, y           ' Signed subtract

' The revolution: hardware multiply!
        mul     x, y           ' x = x[15:0] * y[15:0] (unsigned 16x16->32)
        muls    x, y           ' Signed 16x16->32 multiply
        
' And hardware divide!
        qdiv    x, y           ' Start division x/y
        getqx   result         ' Get quotient
        getqy   remainder      ' Get remainder
```

Here's a complete multiply example:

```pasm2
' Simple 16x16->32 multiply (2 clocks)
        mov     x, #123
        mov     y, #456
        mul     x, y           ' Result: 123 * 456 = 56088 in x
        ' Uses lower 16 bits of each operand!

' For full 32x32->64 multiply, use CORDIC:
        qmul    x, y           ' Start multiply (uses full 32 bits)
        ' ... 55 clocks of other work ...
        getqx   low            ' Lower 32 bits of result
        getqy   high           ' Upper 32 bits of result
```

Uff! In the old days, we'd write loops for this. Now hardware does it!

### Logic Operations

Your Boolean friends:

```pasm2
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

### Shifting and Rotating

Moving bits around:

```pasm2
        shl     x, #3          ' Shift left 3 bits
        shr     x, #3          ' Shift right 3 bits
        sar     x, #3          ' Arithmetic shift right (signed)
        rol     x, #3          ' Rotate left 3 bits
        ror     x, #3          ' Rotate right 3 bits
        
' Variable shifts (amount in register)
        shl     x, y           ' Shift x left by y bits
        
' Fancy ones
        rev     x              ' Reverse bit order (!!)
        mergeb  x              ' Merge bits, not bytes (inverse of SPLITB)
```

## Flow Control: Jump!

### Unconditional Jumps

```pasm2
        jmp     #target        ' Jump to target
        jmp     target         ' Jump to address in target register
        
' Relative jumps
        jmp     #$-4          ' Jump back 4 longs (= 4 instructions)
        jmp     #$+8          ' Jump forward 8 longs (= 8 instructions)
```

### Conditional Execution (The Magic)

Here's where PASM2 gets beautiful. ANY instruction can be conditional:

```pasm2
if_z    add     x, #1          ' Only add if Z flag set
if_nz   add     x, #1          ' Only add if Z flag clear
if_c    add     x, #1          ' Only add if C flag set
if_nc   add     x, #1          ' Only add if C flag clear
```

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

And the comparison conditions (use after **CMP**):

| Condition | Meaning |
|-----------|---------|
| `if_a` | If above (unsigned greater) |
| `if_b` | If below (unsigned less) |
| `if_ae` | If above or equal |
| `if_be` | If below or equal |

### The Call/Return Dance

```pasm2
        call    #subroutine    ' Call subroutine
        ret                    ' Return from subroutine
        
' But here's the P2 twist - CALL uses internal stack
subroutine
        ' Do something useful
        ret                    ' Returns to instruction after CALL
        
' You get 8 levels of hardware stack!
```

### The _RET_ Prefix: Return With Benefits

Here's a clever trick the P2 offers. What if you could execute an instruction *and* return from a subroutine in one go? That's exactly what the `_RET_` prefix does.

```pasm2
' Normal way: Two instructions
add_and_return
        add     x, y            ' Do the add
        ret                     ' Then return (RET is a ~4-cycle branch)

' _RET_ way: One instruction!
add_and_return
        _ret_   add     x, y    ' Add AND return (saves 2 cycles)
```

The `_RET_` prefix says: "Execute this instruction, then return." It's like getting a free return ticket with your instruction. The add happens, flags get set normally, and then—pop!—you're back at the caller.

**When does _RET_ NOT return?**

Here's the catch: if the instruction itself branches, no return happens. The branch wins:

```pasm2
        _ret_   jmp     #somewhere      ' JMP wins - no return
        _ret_   call    #helper         ' CALL wins - no return
        _ret_   djnz    count, #loop    ' Branch? No return. Zero? Return!
```

That last one is interesting! If `count` isn't zero, **DJNZ** branches and no return. But when `count` hits zero, no branch occurs, so you get your return. Clever, right?

**One-Instruction Subroutines**

This is where `_RET_` really shines:

```pasm2
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

```pasm2
DAT             org

send_byte       rdbyte  x, ptr          ' Global label
                wypin   x, tx_pin
                ret

receive_byte    testp   rx_pin    wc    ' Another global label
                rdpin   x, rx_pin
                ret
```

Global labels are visible everywhere in your DAT block. You can jump to them, call them, reference them from Spin2 - they're your main signposts.

### Local Labels: The Little Helpers

But here's a problem. What if every routine needs a loop? You can't have two labels called `loop` - the assembler would be terribly confused.

Enter local labels. Prefix a name with a dot (`.`) and it becomes local:

```pasm2
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

Each global label starts a new "scope". The `.loop` under `send_byte` is completely separate from the `.loop` under `receive_byte`. You can reuse `.loop`, `.done`, `.retry`, `.exit` to your heart's content.

### The Colon Alternative

You might also see local labels with a colon prefix:

```pasm2
:loop           djnz    count, #:loop   ' Same as .loop
```

Both `:` and `.` work identically. I prefer the dot - it's what modern convention has settled on - but you'll see both in the wild.

### Reference Operators: Finding Your Labels

When you reference a label, you need to tell the assembler what you want:

```pasm2
' In cog code (after ORG):
        jmp     #my_routine     ' # = immediate cog address
        call    #.helper        ' # works for local labels too
        mov     x, #data_table  ' Get cog address of data

' For hub addresses (used with Spin2):
        mov     ptr, ##@hub_data ' ##@ = full hub address of label
```

The `#` means "immediate value" - use this for jumps and calls within cog code. The `@` means "hub address" - use this when passing addresses to Spin2 or for hub memory operations.

### Scope Boundaries: When Local Labels Reset

Here's the rule: **every global label or data definition starts a new local scope**.

```pasm2
func_a          mov     x, #1           ' Scope #1 begins
.loop           djnz    x, #.loop       ' .loop in scope #1

data_block      long    0, 0, 0, 0      ' Scope #2 begins (data!)

func_b          mov     y, #2           ' Scope #3 begins
.loop           djnz    y, #.loop       ' .loop in scope #3, OK!
.done           ret
```

This is wonderfully useful - your utility routines can all use `.loop` and `.done` without stepping on each other's toes.

### The Medicine: Quick Reference

| What | Syntax | Example |
|------|--------|---------|
| Global label | `name` | `my_routine` |
| Local label | `.name` or `:name` | `.loop`, `:done` |
| Jump to label | `#label` | `jmp #.loop` |
| Hub address | `##@label` | `mov ptr, ##@data` |

### Common Gotchas

1. **Forgetting the dot**: `loop` is global, `.loop` is local. If you accidentally create a global `loop`, you'll get conflicts.

2. **Scope surprise**: Data definitions (`LONG`, `WORD`, `BYTE`) also start new scopes. If you put data between two parts of a routine, your local labels won't work!

3. **The 30-character limit**: Keep label names to 30 characters or fewer—the compiler rejects any name longer than 30. `this_is_a_really_long_label_name` (32 characters) will be rejected.

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
entry           mov     ptra, buffer_addr   ' Read hub pointer Spin2 stored
                mov     count, BUFFER_SIZE
.fill           wrbyte  fill_value, ptra++
                djnz    count, #.fill
                jmp     #$

' Constants (read-only, effectively)
fill_value      byte    $55
                alignl
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

**String Addresses in PASM**

Need a string's address? In PASM you point at a DAT label with `##@`:

```pasm2
        mov     ptra, ##@hello      ' ptra points to "Hello!" in hub
        call    #print_string

        mov     ptra, ##@err_msg    ' Another string
        call    #print_string

        alignl
hello   byte    "Hello!", 0
        alignl
err_msg byte    "Error: ", 0
```

The string lives in your DAT block, and `@label` gives its hub address. Spin2 has an even shorter shortcut - `@"Hello!"` composes the string and hands back its address with no separate label - but that one is Spin2-only, not PASM.

**STRING("text") and LSTRING("text")**

These work similarly but in different contexts:

```spin2
{Spin2_v43}                       ' enable LSTRING (a v43+ keyword)
' In Spin2 code (not PASM):
debug(STRING("Temperature: "))    ' Zero-terminated string address
debug(LSTRING("Status"))          ' Length byte first, then string
```

`STRING()` returns the hub address of a zero-terminated string - same as what C programmers expect. `LSTRING()` puts a length byte at the front, which is handy when you need to know the string length without scanning for null. `LSTRING()` is a newer keyword, so it needs a `{Spin2_v43}` (or later) directive at the top of your file before the compiler will recognize it.

**BYTE[], WORD[], LONG[] - Data Arrays**

In Spin2, you can compose inline data and get its address:

```spin2
{Spin2_v43}                            ' BYTE/WORD/LONG composers (v43+)
tbl := BYTE(10, 20, 30, 40, 50)        ' Returns address of byte array
config := LONG($DEAD_BEEF, $CAFE_BABE)
```

These are primarily Spin2 features, but they generate hub data that your PASM code can access if you know the addresses.

**The Pattern:**

| Method | Result | Use Case |
|--------|--------|----------|
| `file "name"` | Raw binary data | Images, audio, lookup tables |
| `##@label` | String address | Inline strings in PASM (DAT label) |
| `@"text"` | String address | Quick inline strings (Spin2 shortcut) |
| `STRING("text")` | Zero-terminated string address | Spin2 string constants |
| `LSTRING("text")` | Length-prefixed string | Spin2, needs `{Spin2_v43}` |

## The Flags: C and Z (plus the Q register)

Flags are your friends. They remember things:

```pasm2
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

Q isn't a flag at all—it's a 32-bit register you load with **SETQ**/**SETQ2**. It supplies an extra operand to block hub transfers (**SETQ** + **RDLONG**/**WRLONG**), CORDIC operations (Chapter 7), and the streamer. The only true condition flags are C and Z.

## Special Instructions That Will Blow Your Mind

### SKIP - The Instruction Skipper

```pasm2
        skip    ##%00001010    ' LSB first: 1=skip, 0=execute
        add     x, #1         ' Executed (bit 0 = 0)
        add     y, #1         ' Skipped! (bit 1 = 1)
        add     z, #1         ' Executed (bit 2 = 0)
        sub     a, #1         ' Skipped! (bit 3 = 1)
        sub     b, #1         ' Executed (bit 4 = 0)
        ' ... bit N controls the Nth instruction after SKIP
```

This is like having conditional execution on steroids!

### REP - Hardware Loops

```pasm2
        rep     #4, #5         ' Repeat next 4 instructions 5 times
        add     x, #1
        sub     y, #1
        rol     z, #1
        ror     w, #1
        ' These 4 instructions execute 5 times total
        ' No loop overhead!
```

### ALTD/ALTS - Instruction Modification

```pasm2
' Modify the next instruction's destination
        mov     index, #10
        altd    index, #array  ' Next instruction's dest = array+10
        mov     0-0, value     ' Actually moves to array[10]!
```

This replaces self-modifying code from P1. Much cleaner!

::: sidetrack
**Hub-Exec Note:** All ALTx instructions — **ALTI**, **ALTS**, **ALTD**, **ALTR**, **ALTB**, **ALTSN**, **ALTSB**, **ALTSW**, **ALTGN**, **ALTGB**, **ALTGW** — work identically in cog-exec and hub-exec modes. They act on the next pipelined instruction regardless of whether it came from cog/LUT memory or the hub-prefetch FIFO. So when you graduate to hub execution in Chapter 10, every ALTx trick you learn here still works.
:::

## Real-World Example: Fast Memory Copy

Let's combine what we've learned:

```pasm2
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

::: medicine-cabinet
Feeling overwhelmed? Here's your simplified prescription:

**Minimum Instructions to Know**

```pasm2
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

```pasm2
   rdlong  x, ptra++      ' Read and auto-increment
   rdlong  x, ++ptra      ' Pre-increment then read
   rdlong  x, ptra--      ' Read and auto-decrement
   rdlong  x, ptra[5]     ' Read from ptra + 5*4
```

4. **Address confusion**:
   - Cog addresses are in longs (0-511)
   - Hub addresses are in bytes (0-524287)

## Your Turn: Experiments

### Experiment 1: Conditional Counter
Count up if button pressed, down if not:

```pasm2
        org     0
        
.loop   testp   #BUTTON_PIN wc ' Test button
if_c    add     counter, #1    ' Increment if pressed
if_nc   sub     counter, #1    ' Decrement if not

        wrlong  counter, ##HUB_ADDR ' Display count
        waitx   ##1_000_000
        jmp     #.loop
        
counter long    0
```

### Experiment 2: Pattern Matcher
Find a pattern in data:

```pasm2
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

### Experiment 3: Speed Test
Compare multiply methods:

```pasm2
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

::: sidetrack
### Why PASM2 Is Different

Most assembly languages are thin wrappers over hardware. PASM2 is different - it's designed for humans:

1. **Regularity**: Nearly every instruction shares the same D, S/# operand pattern (hub, branch, and no-operand instructions have their own restricted forms)
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
- ✅ Special instructions (**SKIP**, **REP**, the **ALT** family)
- ✅ flag operations and testing
- ✅ Why PASM2 is human-friendly

## Coming Up Next

Chapter 4, "The Hub Connection", explores:

- Reading and writing hub memory
- The FIFO and fast block transfers
- Hub execution mode
- Sharing data between cogs

You now speak basic PASM2. Time to learn how cogs communicate!


**Have Fun!** Remember, PASM2 isn't like other assembly languages - it's actually enjoyable!




# Chapter 4: The Hub Connection

*How cogs share and care*

## The Hook: Instant Communication

```pasm2
' cog 1: Leave a message
        wrlong  ##$DEADBEEF, ##$1000
        
' cog 2: Get the message
        rdlong  message, ##$1000
        ' message now contains $DEADBEEF!
```

That's it - cogs talking through hub memory. But there's so much more...

## Reading from Hub

The basics are simple:

```pasm2
        rdbyte  value, hubaddr    ' Read 1 byte
        rdword  value, hubaddr    ' Read 2 bytes (word)
        rdlong  value, hubaddr    ' Read 4 bytes (long)
        
' With PTRA/PTRB magic
        rdlong  value, ptra++     ' Read and increment pointer
        rdlong  value, ++ptra     ' Increment then read
        rdlong  value, ptra[5]    ' Read from ptra + 5*4
```

## Writing to Hub

Just as easy:

```pasm2
        wrbyte  value, hubaddr    ' Write 1 byte
        wrword  value, hubaddr    ' Write 2 bytes
        wrlong  value, hubaddr    ' Write 4 bytes
        
' The mighty block transfer
        setq    #16-1             ' Transfer 16 longs
        rdlong  buffer, hubaddr   ' Reads 16 longs in one go!
```

## The FIFO Pipeline

Here's where P2 gets serious about speed:

```pasm2
' Start the FIFO
        rdfast  #0, ##data_start  ' Start fast read
        
' Now read at maximum speed
.loop   rflong  value            ' Read from FIFO
        ' Process value
        djnz    count, #.loop    ' Decrement and jump if not zero
        
' No hub timing worries - FIFO handles it all!
```

## Real-World Example: Video Buffer

```pasm2
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

::: medicine-cabinet
**Simple hub access pattern**:

```pasm2
' Just use PTRA for everything
        mov     ptra, ##hub_address
        rdlong  value, ptra++
        ' That's all you really need!
```
:::

## Your Turn: Experiments

Now you know the moves. Try these to make them stick:

1. **Round-trip:** Write a long to hub at address `$1000`, then read it back into a different register. Verify the values match using a comparison and a flag.

2. **Block fill:** Use **SETQ** + **WRLONG** to fill 64 consecutive longs in hub memory with the value `$DEAD_BEEF`. Then read them back one by one and confirm.

3. **FIFO race:** Use **RDFAST** to stream a sequence of longs from hub. Compare the throughput to a loop of individual **RDLONG** instructions. The difference should astonish you.

4. **Pointer arithmetic:** Set **PTRA** to a hub address, then use **RDLONG** `val, ptra[3]` to read the third long ahead — without moving the pointer. Experiment with `++`, `--`, and indexed forms.

## Common Gotchas

Before you pull your hair out debugging hub access:

1. **Forgetting the `##`** — hub addresses are 20-bit. On **RDxxx**/**WRxxx** a bare `#address` only encodes 8 bits (0–255)—the 9th S-field bit selects PTR-expression mode, not address 256+—so you'll hit the wrong memory. Always use `##` for any hub address above 255.

2. **Unaligned long access costs a clock** — **RDLONG** and **WRLONG** can read or write a long starting at *any* byte address (no low-bit masking, unlike P1). When the long straddles two hub-RAM slices you simply pay one extra clock. Only the FIFO/wrapping mode actually requires long alignment.

3. **SETQ block size** — **SETQ** `#N-1` transfers `N` longs (not `N-1`). The `-1` is because the encoded field is "count minus one." Off-by-one bugs love this one.

4. **PTRA vs. PTRB** — Both are pointer registers, but they're independent. Don't assume **PTRA** holds anything if you've been working with **PTRB**.

5. **Hub-exec vs. cog-exec timing** — In cog-exec, **RDLONG** is 9–16 cycles. In hub-exec, it's 9–26 cycles. Inner loops that hammer hub should run from cog memory when possible.

## What We've Learned

Look at all the ground we've covered:

- ✅ How to read and write hub memory from cog code
- ✅ Why pointer registers (PTRA, PTRB) exist and when to use them
- ✅ How the FIFO pipeline accelerates sequential hub reads
- ✅ Block transfers with **SETQ** for moving big chunks at once
- ✅ The pattern for clearing or filling buffer-sized regions

You now have the entire cog↔hub vocabulary at your disposal.

## Coming Up Next

In Chapter 5, we'll unleash the P2's mathematical muscle:

- Hardware multiply and divide that don't require library calls
- 64-bit arithmetic without sweating
- A preview of the CORDIC coprocessor (it gets a full chapter later)
- Fixed-point math for fast trigonometry

But first, take a break. Hub access is one of those topics where letting it sit a day helps it lock in. Try one of the experiments above tomorrow.

**Have Fun!** And remember — the FIFO is doing real work even when your code looks idle. Trust it.



# Chapter 5: Mathematics Unleashed

*Hardware multiply and divide - finally!*

## The Hook: Hardware Multiply

```pasm2
        mul     x, y              ' 16x16->32 bit unsigned multiply
        ' Result in x (lower 16 bits of each operand used)

        ' For full 32x32->64 bit multiply, use CORDIC:
        qmul    x, y              ' Start 32x32->64 multiply
        ' ... other work (55 clocks) ...
        getqx   low               ' Get lower 32 bits
        getqy   high              ' Get upper 32 bits
```

Remember doing this with shifts and adds? Those days are over!

## The Multiplication Revolution

```pasm2
' Unsigned multiply
        mul     result, value     ' result = low 32 bits
        
' Signed multiply  
        muls    result, value     ' Signed version
        
' Scale by a power of two
        shr     result, #1        ' Scale by 0.5 (divide by 2)
```

## Division Without Tears

```pasm2
' Start division
        qdiv    dividend, divisor ' Start the operation
        
' Get results (takes 55 clocks)
        getqx   quotient         ' Get quotient
        getqy   remainder        ' Get remainder
        
' Fractional division
        qfrac   numerator, denominator
        getqx   fraction         ' 32-bit fraction
```

## 64-Bit Operations

```pasm2
' 64-bit add
        add     low1, low2 wc
        addx    high1, high2

' 64-bit multiply (uses CORDIC)
        qmul    x, y           ' Start 32x32->64 multiply
        ' ... 55 clocks ...
        getqx   low            ' Lower 32 bits
        getqy   high           ' Upper 32 bits
```

## Real-World Example: Fixed-Point Math

```pasm2
' 16.16 fixed point multiply (uses CORDIC for full precision)
fixed_mul
        qmul    a, b             ' Start 32x32->64 unsigned multiply
        ' ... 55 clocks (do other work) ...
        getqx   low              ' Lower 32 bits
        getqy   high             ' Upper 32 bits
        ' Extract middle 32 bits for 16.16 result:
        shl     high, #16        ' Upper 16 bits of result
        shr     low, #16         ' Lower 16 bits of result
        mov     a, low           ' Combine for 16.16 format
        or      a, high
```

::: medicine-cabinet
**Quick math reference**:

- **MUL** D, S — unsigned 16×16→32
- **MULS** D, S — signed 16×16→32
- **QMUL** D, S — full 32×32→64 (read via **GETQX**/**GETQY** after 55 clocks)
- **QDIV** D, S — full 32-bit divide (read via **GETQX** quotient / **GETQY** remainder after 55 clocks)
- **QFRAC** D, S — fractional divide (returns 32-bit fraction in **GETQX**)
- 64-bit add: **ADD** + **ADDX** chained with **WC**

For everyday integer work, **MUL**/**MULS** are 2 clocks and you're done. For precision (full 64-bit results, fixed-point math, signed division), **QMUL**/**QDIV** route through the CORDIC and pay 55 clocks — but they don't block the cog, so you can interleave other work.
:::

## Your Turn: Experiments

Stretch your math muscles:

1. **Compute the average:** Read 8 longs from hub, sum them with **ADD**, then divide by 8 using a **SHR** (or **QDIV** if you want exact). Compare both approaches.

2. **Fractional reciprocal:** Use **QFRAC** to compute `2^32 / x` for various x values. You've just built a hardware reciprocal table.

3. **Pipeline overlap:** Start a **QMUL**, do 30+ clocks of other work (compute something else, update a counter), then **GETQX**/**GETQY**. Measure total cycles vs. doing the multiply blocking-style.

4. **64-bit counter:** Build a 64-bit increment loop using **ADD** + **ADDX**. Add to it in a tight loop and watch the high word advance when the low one wraps.

## Common Gotchas

The math instructions hide a few traps:

1. **MUL is unsigned, MULS is signed** — Using the wrong one on negative values gives spectacular nonsense. When in doubt, **MULS**.

2. **MUL is a 16×16 multiply** — It multiplies the low 16 bits of each operand into a complete 32-bit product (nothing is discarded). To multiply full 32-bit operands into a 64-bit result, use **QMUL** + **GETQX**/**GETQY**.

3. **GETQX/GETQY block until ready** — They wait for the CORDIC. If you call them too early, your cog stalls. If you call them later than necessary, you've wasted cycles. The sweet spot is starting the CORDIC, doing exactly 55 clocks of other work, then reading.

4. **Don't outrun the CORDIC pipeline** — The CORDIC is a 54-stage pipeline, so you *may* issue several operations before reading; **GETQX**/**GETQY** return their results in issue order. Results are only lost if you let too many accumulate before reading, or if an enabled interrupt steals clocks during the overlap—so keep interrupts disabled while juggling.

## What We've Learned

A whole arithmetic library, in your back pocket:

- ✅ Hardware multiply (**MUL**, **MULS**) in just 2 clocks
- ✅ Division and modulo via **QDIV** + **GETQX**/**GETQY**
- ✅ Fractional division via **QFRAC** for fast reciprocals
- ✅ 64-bit chains using **ADD**/**ADDX**, **SUB**/**SUBX** with **WC**
- ✅ Fixed-point patterns for 16.16 math

You no longer have to write multiply-by-shift-and-add. Those days really are over.

## Coming Up Next

In Chapter 6 we'll meet the P2's most quietly powerful feature: **conditional execution**. Every instruction can be conditional — no branches needed, deterministic timing preserved. We'll cover:

- The C and Z flags and how to update them
- Building complex conditions with **WC**, **WZ**, **WCZ** combined with **IF_x** prefixes
- **SKIP** and **SKIPF** for skipping patterns of instructions

If conditional execution doesn't change how you think about flow control, nothing will.

**Have Fun!** And remember — the CORDIC is a coprocessor with infinite patience. Use it.



# Chapter 6: Flags and Decisions

*Making choices at machine speed*

## The Hook: Any Instruction Can Be Conditional

```pasm2
        cmp     x, y wcz         ' Compare x and y
if_a    mov     result, x        ' If x > y, result = x
if_be   mov     result, y        ' If x <= y, result = y
        ' Max function in 3 instructions!
```

## The C and Z Flags

```pasm2
' Z Flag - Zero detection
        sub     x, y wz          ' Z=1 if x equals y
if_z    jmp     #equal          ' Jump if equal

' C Flag - Carry/Borrow
        add     x, y wc          ' C=1 if overflow
if_c    jmp     #overflow       ' Handle overflow
```

## Complex Conditions

```pasm2
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

## Skip Patterns - Conditional Blocks

```pasm2
        skipf   pattern          ' Set skip pattern
        add     x, #1           ' Maybe executed
        sub     y, #1           ' Maybe executed
        mov     z, #0           ' Maybe executed
        ' Pattern determines what runs!
```

::: medicine-cabinet
**Conditional execution quick reference**:

- **WC** — write the C flag with the instruction's carry-out
- **WZ** — write the Z flag based on result == 0
- **WCZ** — write both flags
- **IF_C**, **IF_NC** — execute next instruction only if C set / clear
- **IF_Z**, **IF_NZ** — same for Z
- **IF_A**, **IF_B**, **IF_AE**, **IF_BE** — unsigned comparisons after **CMP**
- **IF_GT**, **IF_LT**, **IF_GE**, **IF_LE** — signed comparisons after **CMPS**
- **IF_E**, **IF_NE** — equal / not equal (same as **IF_Z**/**IF_NZ** after compare)

A condition prefix adds no clocks and causes no pipeline flush—a simple ALU instruction still takes 2 clocks whether it runs or is skipped. (Multi-cycle instructions like **RDLONG** at 9–16 clocks or **GETQX** at up to 58 keep their own larger counts, conditional or not.) No branches, no surprise.
:::

## Your Turn: Experiments

Practice the conditional mindset:

1. **Branchless absolute value:** Compute `result = abs(x)` using **ABS** — then prove to yourself the same thing works branchless using **CMPS** + a conditional **NEG**.

2. **Saturating add:** Add two unsigned values; if the result overflows (**WC** sets C), clamp to `$FFFF_FFFF`. No jumps.

3. **Min/max:** Build a min function using **CMP** + conditional **MOV**. Then build max. Three instructions each.

4. **Skip-pattern selector:** Use **SKIPF** with a runtime bit pattern to selectively execute 4 different instructions based on a state byte. This is the building block for hand-coded jump tables.

## Common Gotchas

The conditional mindset has its own traps:

1. **Forgetting the effect** — `cmp x, y` *with no flag effect* doesn't update C or Z. You need **WC**, **WZ**, or **WCZ**. The default for **CMP** is no update.

2. **Signed vs. unsigned comparison** — **CMP** sets flags for unsigned semantics (**IF_A**/**IF_B**). **CMPS** sets them for signed (**IF_GT**/**IF_LT**). Mixing them produces baffling bugs near zero and at the high bit.

3. **One instruction follows the prefix** — `IF_C mov x, y` conditionally runs *only* the **MOV**. The instruction after that runs unconditionally. To skip a block, use **SKIPF**.

4. **C flag inversion on subtract** — **SUB** sets C on *borrow*, not carry. So after `sub a, b wc`, C=1 means `a < b` (unsigned). Many P1 programmers expect the opposite — re-check.

5. **Skip patterns are LSB-first** — In **SKIPF**, bit 0 controls the next instruction, bit 1 the one after, etc. The numbering can feel backward; sketch it out.

## What We've Learned

You can now think like a P2 programmer:

- ✅ Every instruction can carry a condition prefix
- ✅ Flags are updated only when you ask (**WC**, **WZ**, **WCZ**)
- ✅ Unsigned and signed comparisons use different instructions (**CMP** vs. **CMPS**)
- ✅ Complex multi-way logic without a single jump using **IF_x** prefixes
- ✅ **SKIP** and **SKIPF** for skipping arbitrary patterns of instructions

You've learned to write branchless code that preserves deterministic timing. That's the deepest part of P2 thinking.

## Coming Up Next

Chapter 7 reveals the CORDIC coprocessor in full — the math beast you glimpsed in Chapter 5. Trigonometry at the speed of logic gates:

- Rotate points in three instructions
- Polar↔Cartesian conversion
- Hardware square root and natural log
- Pipelined operations for graphics and signal processing

If you thought hardware multiply was nice, wait until you see what the CORDIC does.

**Have Fun!** And remember — every `jmp` you avoid is a pipeline flush you didn't pay for.




# Chapter 7: CORDIC Magic


*Trigonometry at the speed of logic gates*

## The Hook: Rotate a Point in 4 Lines

Let me show you something that, on most processors, would take a coffee break of instructions, a math library, and probably a tear or two:

```pasm2
' Rotate point (x,y) by angle - that's it!
        setq    y_coord         ' Set Y coordinate
        qrotate x_coord, angle  ' Start rotation by angle
        getqx   new_x          ' Get rotated X (55 clocks later)
        getqy   new_y          ' Get rotated Y
```

Read that again. *Four lines*, and a 2D rotation is done. No floating-point library. No lookup tables. No iterative approximation. The P2 has a hardware trigonometric coprocessor—a single CORDIC solver in the hub that every cog can call on—just waiting for you to wake it up. You're about to learn how.

Let me show you something even more impressive:

```pasm2
' Calculate sine and cosine simultaneously
        qrotate ##$7FFF_FFFF, angle  ' D=radius (max), S=angle
        getqx   cosine               ' cos(angle); $7FFF_FFFF = 1.0
        getqy   sine                 ' sin(angle); $7FFF_FFFF = 1.0
        ' Both trig functions in 55 clocks total!
```

## What Just Happened?

CORDIC stands for COordinate Rotation DIgital Computer. It's a method invented in 1959 for calculating trigonometric functions using only shifts and adds - no multiplies needed! The P2 has a single CORDIC solver built into the hub, shared by all cogs—each cog gets a hub slot in which to hand off a command.

Think of CORDIC as your mathematical co-processor that can:

- Rotate points around the origin
- Convert between rectangular and polar coordinates  
- Calculate sine and cosine (tangent by dividing sine by cosine)
- Compute square roots and magnitudes
- Find arctangent (angle between points)
- Even do logarithms and exponentials!

The pipeline itself is a fixed 55 clocks from command hand-off to result. Add the 0–7 clock wait for your cog's hub slot (plus the **GETQX**/**GETQY** read), and the end-to-end time varies only slightly around that.

## The CORDIC Pipeline - Your Mathematical Assembly Line

Here's the beautiful part: CORDIC operations are pipelined. While one calculation is running, you can start another. Let's see what that buys us:

```pasm2
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
        ' Generated 256 samples, overlapping a few instructions per pass
```

This loop overlaps only the three instructions between `qrotate` and `getqy` with the 55-clock latency, so `getqy` still stalls for most of it each pass. To *truly* hide the latency you software-pipeline across iterations: issue the next sample's `qrotate` before reading the previous sample's `getqy`, keeping a command in flight while you harvest the last result. Uff! That's how you get free math!

## Core CORDIC Operations

### QROTATE - The Rotation Engine

Here's a subtle detail: CORDIC operations work on 2D coordinates (X, Y), but the **QROTATE** instruction only takes one coordinate directly. The solution? **SETQ** loads the Y coordinate into the Q register, then **QROTATE** takes X from its first operand. It's a two-instruction dance that becomes second nature:

```pasm2
' Basic rotation: rotate point (x,y) by angle
        setq    y              ' First: load Y into Q register
        qrotate x, angle       ' Then: X from operand, Y from Q
        getqx   new_x          ' Result: X' = X*cos(θ) - Y*sin(θ)
        getqy   new_y          ' Result: Y' = X*sin(θ) + Y*cos(θ)
```

The angle format is special: it's a 32-bit unsigned value where:

- $0000_0000 = 0 degrees
- $4000_0000 = 90 degrees  
- $8000_0000 = 180 degrees
- $C000_0000 = 270 degrees
- $FFFF_FFFF = just under 360 degrees

This makes angle math incredibly easy - just use regular addition and subtraction!

### QVECTOR - From Rectangular to Polar

```pasm2
' Convert (x,y) to polar (radius, angle)
        qvector x, y           ' X in D, Y in S (no SETQ for QVECTOR)
        getqx   radius         ' sqrt(x² + y²)
        getqy   angle          ' atan2(y, x)
```

Perfect for:

- Finding distances between points
- Converting joystick input to angle/magnitude
- Radar and sonar applications

### The Power of 32-Bit Precision

CORDIC uses 32-bit precision throughout:

- Angles: 32 bits (0.00000008 degree resolution!)
- Coordinates: 32 bits signed
- Results: Full 32-bit or 64-bit when needed

## Real-World Example: Spinning a Sprite

Let's rotate a sprite around its center:

```pasm2
' Rotate sprite vertices around center
' (PTRA for vertex iteration — only PTRA/PTRB support ++ post-increment.)
rotate_sprite
        mov     ptra, ##sprite_data
        mov     vertex_count, #4        ' 4 corners

next_vertex
        rdlong  x, ptra++              ' Get X coordinate, advance pointer
        rdlong  y, ptra++              ' Get Y coordinate, advance pointer

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

        ' Store rotated vertex (back up PTRA 8 to overwrite source longs)
        sub     ptra, #8
        wrlong  x, ptra++
        wrlong  y, ptra++

        djnz    vertex_count, #next_vertex
        
        ' Increment rotation for animation
        add     rotation_angle, ##$0100_0000  ' ~1.4 deg (1/256 rotation)
```

## Your Turn: CORDIC Experiments

::: your-turn
**Your Turn:** Create a circular motion pattern

Starting code:

```pasm2
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

Goal: Make a dot trace a perfect circle on screen
Hint: After qrotate, use getqx/getqy to get coordinates
Success Check: Smooth circular motion, no gaps
:::

::: your-turn  
**Your Turn:** Distance calculator

Starting code:

```pasm2
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

Goal: Calculate the distance between the two points
Hint: qvector dx, dy gives you radius (distance) in QX
Success Check: Distance should be 50 units
:::

::: medicine-cabinet
Feeling overwhelmed by all this trigonometry? Here's your simplified prescription:

**Too Complex?** Just remember these three patterns:

**Pattern 1: Get sine/cosine**

```pasm2
        qrotate ##$7FFF_FFFF, angle    ' D=radius, S=angle
        getqx   cos_value
        getqy   sin_value
```

**Pattern 2: Rotate a point**

```pasm2
        setq    y
        qrotate x, angle
        getqx   new_x
        getqy   new_y
```

**Pattern 3: Get distance**

```pasm2
        qvector dx, dy
        getqx   distance
```

Master these three and you can do 90% of what you need!
:::

## Advanced CORDIC: The Pipeline Dance

Here's where CORDIC gets really powerful - overlapping operations:

```pasm2
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

See what happened? We started each new CORDIC operation immediately after the previous one, then retrieved results later. This pipeline approach means we're effectively getting one rotation every few instructions instead of waiting 55 clocks each time!

## CORDIC for Graphics

Want to draw a spiral? CORDIC makes it trivial:

```pasm2
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
        add     angle, ##$0400_0000   ' Rotate 5.625 degrees (1/64 turn)
        add     radius, ##100         ' Expand slowly
        
        cmp     radius, ##30000 wcz
   if_b jmp     #draw_spiral
```

## CORDIC for Audio

Generate perfect sine waves for audio:

```pasm2
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

## Common CORDIC Gotchas

Before you pull your hair out debugging, know these:

1. **Mind the pipeline depth** - The P2 has one shared CORDIC solver in the hub (not one per cog). You may have several operations in flight at once—results queue and are read in issue order via **GETQX**/**GETQY**. They're only lost if you outrun the 54-stage pipeline before reading, or an enabled interrupt steals enough clocks during the overlap.

2. **55 clocks after hand-off** - Results are ready exactly 55 clocks after the solver *receives* your command—but your cog first waits 0 to 7 clocks (on an 8-cog P2) for its hub slot, so time it from hand-off, not from the instruction issue.

3. **Don't forget SETQ** - For two-operand operations (**QROTATE** with X,Y), you must load Y into Q first.

4. **Results are scaled** - When rotating a vector of length $7FFF_FFFF, the X/Y results come back scaled so that $7FFF_FFFF represents 1.0 (full-scale signed).

5. **Angles wrap naturally** - Adding $1_0000_0000 to an angle is the same as adding 0. Use this!

## What About QLOG, QEXP?

Don't worry, we won't leave logarithms and exponentials behind. CORDIC handles those too:

```pasm2
' Base-2 logarithm
        qlog    value
        getqx   result          ' log2(value) in 5.27 fixed point
        
' Base-2 exponential (2^x)
        qexp    value  
        getqx   result          ' 2^value
```

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

Chapter 8 brings us back to Earth with "Basic I/O" - the fundamental pin operations that make the real world connection. We'll save smart pins for another manual and focus on the essentials: making pins go high and low, reading buttons, and basic timing.

But first, take a moment to appreciate what you just learned. CORDIC is unique to the Propeller 2 - most microcontrollers would need extensive software libraries to do what you just did in three instructions!


**Have Fun!** And remember - with CORDIC, you're not just calculating trigonometry, you're doing it at hardware speed. That's magical!


# Chapter 8: Basic I/O

*Making the real world connection*

## The Hook: One Pin, Three Instructions, Infinite Possibilities

Watch this:

```pasm2
' Complete button-and-LED program
.loop   testp   #BUTTON_PIN wc  ' Read button into C flag
   if_c drvh    #LED_PIN        ' If pressed, LED on
  if_nc drvl    #LED_PIN        ' If not pressed, LED off
        jmp     #.loop          ' Repeat forever
```

Four lines. Complete input/output program. No configuration registers, no data direction setup, no port manipulation. Just pure, simple I/O.

But wait, let me show you the same thing with even more elegance:

```pasm2
' Even simpler - button controls LED directly
.loop   testp   #BUTTON_PIN wc  ' Read button
        drvc    #LED_PIN        ' Drive LED from C flag!
        jmp     #.loop
```

Three lines! The **DRVC** instruction drives the pin to match the C flag. Input becomes output. Simple becomes simpler.

## Understanding P2 Pins

Let's unpack what makes those three lines so short. Every P2 pin is bidirectional and incredibly capable. Unlike older microcontrollers where you set data direction registers (remember TRIS bits? DDRA? Yeah, we don't miss those either), P2 pins change direction on the fly based on the instruction you use.

Here's the mental model:

- **Output instructions** (**DRVH**/**DRVL**/**DRVNOT**) automatically drive the pin (direction becomes output)
- **Float instructions** (**FLTL**/**FLTH**) make the pin high-impedance (direction becomes input)
- **Reading a pin** (**TESTP**) works regardless of its direction
- No setup required!

## Digital Output: Making Things Happen

### The Fundamental Four

```pasm2
        drvh    #56            ' Drive pin 56 HIGH (3.3V)
        drvl    #56            ' Drive pin 56 LOW (0V)
        drvnot  #56            ' Toggle pin 56
        fltl    #56            ' Float pin 56 (high-Z)
```

That's it. Four instructions, 90% of your output needs covered. We'll meet a few specialized cousins below, but if you only remember these four, you'll get a lot done.

### Conditional Driving

Here's where P2 gets clever:

```pasm2
        drvc    #56            ' Drive pin to match C flag
        drvnc   #56            ' Drive pin to NOT C flag
        drvz    #56            ' Drive pin to match Z flag
        drvnz   #56            ' Drive pin to NOT Z flag
```

And the really clever one:

```pasm2
        drvnot  #56 wcz        ' Toggle pin AND read old state to C
        ' C now contains what the pin WAS before toggling
```

### Random and Pattern Outputs

```pasm2
        drvrnd  #56            ' Drive pin to a random level (hardware PRNG)
        outl    #56            ' Set OUT bit low (dir unchanged)
        outh    #56            ' Set OUT bit high (dir unchanged)
```

## Digital Input: Reading the World

### Basic Pin Reading

```pasm2
        testp   #BUTTON_PIN wc ' Read pin into C flag
   if_c jmp     #pressed       ' Branch if high
  if_nc jmp     #not_pressed   ' Branch if low
```

Or read into Z flag for zero/non-zero testing:

```pasm2
        testp   #SENSOR_PIN wz ' Read pin into Z flag  
   if_z jmp     #sensor_high   ' Jump if pin high (Z=1 when pin=1)
  if_nz jmp     #sensor_low    ' Jump if pin is low
```

### Reading Multiple Pins

```pasm2
' Read 8 pins at once (pins 0-7)
        mov     mask, #$FF     ' Pins 0-7
        testb   ina, #0 wc     ' Test pin 0
        rcl     result, #1     ' Rotate C into result
        testb   ina, #1 wc     ' Test pin 1
        rcl     result, #1
        ' ... continue for all 8 pins
```

## Pin Timing: When Things Happen

### Waiting for Pin Changes

```pasm2
' Wait for pin to go high
wait_high
        testp   #SIGNAL_PIN wc
  if_nc jmp     #wait_high
        
' Wait for pin to go low  
wait_low
        testp   #SIGNAL_PIN wc
   if_c jmp     #wait_low
```

But there's a better way - hardware-assisted waiting with Smart Events:


```pasm2
        waitse1               ' Wait for event 1
        waitse2               ' Wait for event 2
        ' Configure events to watch pins - super efficient!
```

## Real-World Example: Button Debouncing

Mechanical buttons bounce. Here's how to handle it:

```pasm2
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

## Bit-Banged Serial (The Basics)

Yes, you'll usually reach for smart pins for serial — but it's worth seeing how to do it the hard way once, just so you appreciate what smart pins are doing for you. Here's how:

```pasm2
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

## Your Turn: I/O Experiments

::: your-turn
**Your Turn:** Create a light chaser

Starting code:

```pasm2
        org     0
        
        mov     pattern, #1     ' Start with one LED
        
.loop   mov     pins, pattern   ' Your code here
        ' Make pattern rotate through pins 56-63
        ' Add delay between changes
        ' Wrap around at the end, then jmp #.loop
```

Goal: Create a rotating light pattern on LEDs
Hint: Use SHL and check for overflow
Success Check: Single lit LED rotating through all positions
:::

::: your-turn
**Your Turn:** Reaction timer

Starting code:

```pasm2
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

Goal: Measure reaction time between LED and button press
Hint: Use getct after button detection
Success Check: Time measured in clock cycles
:::

::: medicine-cabinet
Feeling overwhelmed by all these pin operations? Here's the simplified prescription:

**Just need something working?** Remember these patterns:

**Output pattern:**

```pasm2
        drvh    #PIN    ' Make it high
        drvl    #PIN    ' Make it low
        drvnot  #PIN    ' Toggle it
```

**Input pattern:**

```pasm2
        testp   #PIN wc ' Read it
   if_c jmp     #high  ' It's high
  if_nc jmp     #low   ' It's low
```

**Timed pattern:**

```pasm2
.loop   drvnot  #LED
        waitx   ##50_000_000
        jmp     #.loop
```

That's 80% of all I/O right there!
:::

## Advanced Pin Control

### Pin Groups

You can control multiple pins at once:

```pasm2
        drvh    #LED_BASE addpins 3  ' Drive 4 pins high (base+3)
        drvl    #LED_BASE addpins 7  ' Drive 8 pins low
```

### Direct Pin Manipulation

For when you need absolute control:

```pasm2
        mov     outa, pattern    ' Set output register directly
        mov     dira, ##$FF      ' Set direction reg (rare in P2!)
```

But honestly? You'll rarely need these. The individual pin instructions are cleaner and clearer.

## Common I/O Gotchas

Before you pull your hair out wondering why a pin "won't work," save yourself debugging time and skim these:

1. **Pin numbers are 0-63** - Not port.bit notation like other MCUs

2. **No pullup/pulldown by default** - Use external resistors or configure smart pin modes (advanced topic)

3. **Pins float on reset** - All pins start as inputs (floating)

4. **Reading output pins** - You CAN read a pin you're driving (reads the actual pin state)

5. **3.3V logic levels** - P2 is 3.3V, not 5V tolerant!

## Timing Is Everything

Now here's something we'll keep coming back to: P2 I/O is deterministic. When you execute:

```pasm2
        drvh    #56
        drvl    #57
```

Pin 56 goes high, then pin 57 goes low exactly two clocks later—each instruction is deterministic, so that spacing is fixed and repeatable every single time, with no jitter. (If you need two pins to change on the *very same* clock, set them in one instruction—a single `OUTA` write, or `DRVH` with `ADDPINS` over a contiguous group.) Uff! Try getting timing that predictable on an interrupt-driven MCU. This determinism is what makes P2 perfect for precise timing applications.

## Real-World Example: Servo Control

Even without smart pins, controlling a servo is easy:

```pasm2
' Standard servo control (1-2ms pulse every 20ms)
servo_control
        mov     position, ##300_000    ' 1.5ms = center at 200MHz

servo_loop
        drvh    #SERVO_PIN
        waitx   position              ' 1-2ms high pulse
        drvl    #SERVO_PIN
        mov     rest, ##4_000_000     ' 20ms frame at 200MHz
        sub     rest, position        ' Low time fills out the 20ms frame
        waitx   rest

        ' Adjust position as needed
        rdlong  position, ##position_addr
        fge     position, ##200_000   ' Limit to 1ms min
        fle     position, ##400_000   ' Limit to 2ms max
        
        jmp     #servo_loop
```

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

You might wonder - if basic I/O is this simple, why do we need smart pins?

Well, while you CAN bit-bang serial at 115200 baud, or generate PWM, or measure frequencies using the techniques in this chapter, smart pins do all of this in hardware, freeing your cog for more important work.

**For smart pin details**: See the dedicated "P2 Smart Pins Manual" which covers all 32 modes, from simple PWM to complex protocol generation. Smart pins deserve their own complete treatment!

## Coming Up Next

Chapter 9 takes us into "Streaming Data" - the P2's incredible FIFO system that can move megabytes of data without breaking a sweat. We'll see how to stream video, audio, and massive data blocks at maximum speed.


**Have Fun!** Remember, every embedded system ultimately comes down to pins going high and low. You've just mastered the fundamentals that everything else builds upon!


# Chapter 9: Streaming Data

*Moving mountains of data without breaking a sweat*

## The Hook: 2KB in 4 Instructions

Watch this data transfer magic:

```pasm2
' Copy 512 longs (2KB) fast — the most a cog block move can hold
        setq    ##512-1         ' Setup for 512 longs (cog RAM limit)
        rdlong  buffer, source  ' Read them all!
        setq    ##512-1         ' Setup for 512 longs
        wrlong  buffer, dest    ' Write them all!
        ' 2KB moved in microseconds!
```

Four instructions. Two kilobytes. Faster than DMA on most processors. (A cog holds only 512 registers, so that's the ceiling for a single **SETQ** block through cog RAM—move more with the FIFO/streamer.) And we're just getting started...

## Block Transfers: The Power Move

The **SETQ** instruction is your gateway to block transfers:

```pasm2
' Basic block read
        setq    #16-1           ' Transfer 16 longs (minus 1!)
        rdlong  buffer, hubaddr ' Reads 16 consecutive longs
        
' Basic block write
        setq    #16-1           ' Transfer 16 longs
        wrlong  buffer, hubaddr ' Writes 16 consecutive longs
```

Here's the trick: **SETQ** tells the next hub instruction how many longs to transfer. The "-1" is because it's a count from 0 (yes, we'll trip over that off-by-one at least once — everyone does).

## The FIFO: Your Streaming Pipeline

The FIFO (First In, First Out) is P2's streaming engine. Think of it as a conveyor belt between hub memory and your cog:

```pasm2
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

The beauty? The FIFO reads ahead automatically. While you're processing one value, it's already fetching the next. No hub timing slots to worry about!

## Writing Through the FIFO

Reading was nice — writing is symmetric. We'll use **WRFAST** instead of **RDFAST**, and **WFLONG** instead of **RFLONG**, and that's it:

```pasm2
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

## Real-World Example: Screen Buffer Clear

Let's clear a 320x240x4 byte screen buffer (~307KB - fits in hub!):

```pasm2
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

## Streaming with the Streamer

The streamer is different from the FIFO - it's a dedicated DMA engine that can move data between hub memory and pins:

```pasm2
' Configure streamer for video output
        setxfrq ##PIXEL_FREQ    ' Set the pixel (NCO) output rate
        
' Start streaming video data to pins
        xinit   ##STREAM_CMD, #0  ' Start streamer
        ' Data flows from hub to pins automatically!
```

## FIFO and Cog Execution

Here's something amazing - you can execute code from hub through the FIFO:

```pasm2
' Execute large program from hub
        orgh    $1000           ' Code in hub memory
        
hub_code
        ' This code is in hub but executes like it's in cog
        add     x, y
        sub     a, b
        ' Can be megabytes of code!
```

When you call or jump to hub code, the FIFO automatically feeds instructions to the cog. It's like having unlimited code space!

::: medicine-cabinet
Feeling overwhelmed by all this streaming? Here's your prescription:

**Just need to move data?** Use these simple patterns:

**Block read pattern:**

```pasm2
        setq    #SIZE-1
        rdlong  buffer, source
```

**Block write pattern:**

```pasm2
        setq    #SIZE-1
        wrlong  buffer, dest
```

**FIFO read pattern:**

```pasm2
        rdfast  #0, ##source
.loop   rflong  value
        ' Process value
        djnz    count, #.loop
```

That's 90% of streaming right there!
:::

## Advanced Streaming Techniques

### Circular Buffers with FIFO

```pasm2
' Circular buffer reading
        rdfast  ##BUF_BLOCKS, ##buffer  ' D[13:0]=block count; auto-wraps
        
circular_loop
        rflong  value                   ' Read from FIFO
        ' Process value
        ' FIFO automatically wraps at buffer end!
        jmp     #circular_loop
```

### Processing Pipeline with FIFO

```pasm2
' Read data with FIFO, process, write via manual pointer dest_ptr
        rdfast  #0, ##source    ' Set up FIFO for reading
        mov     dest_ptr, ##dest

pipeline
        rflong  input           ' Get next input from FIFO

        ' Scale using 16x16 multiply (result in input)
        mul     input, #SCALE_FACTOR

        wrlong  input, dest_ptr ' Write result via dest_ptr
        add     dest_ptr, #4
        djnz    count, #pipeline
```

Note: FIFO can only read OR write at a time, not both. Use PTRA/PTRB for the other direction.

## Your Turn: Streaming Experiments

::: your-turn
**Your Turn:** Fast memory fill

Starting code:

```pasm2
        org     0
        
        mov     pattern, ##$DEADBEEF
        mov     dest, ##$1000
        mov     count, #256
        
        ' Your code here: Fill 256 longs with pattern
        ' Use SETQ and WRLONG
```

Goal: Fill memory with pattern using block transfer
Hint: You'll need setq #255 (not #256)
Success Check: Memory filled in one operation
:::

::: your-turn
**Your Turn:** Data filter pipeline

Starting code:

```pasm2
        org     0

        rdfast  #0, ##input_data        ' FIFO for reading
        mov     ptra, ##output_data     ' PTRA for writing
        mov     count, #100

filter_loop
        rflong  value                   ' Read from FIFO
        ' Your code: Simple filter
        ' Maybe average with previous value?
        wrlong  result, ptra++          ' Write via PTRA
        djnz    count, #filter_loop
```

Goal: Process streaming data through simple filter
Hint: Keep previous value in a register
Success Check: Output is filtered version of input
:::

## Common Streaming Gotchas

Before you pull your hair out wondering why your transfer is one long short, or why your FIFO won't cooperate, skim these:

1. **SETQ uses count-1** - For 16 longs, use `setq #15`, not `setq #16`

2. **FIFO is shared per cog** - Can't use FIFO for both code execution and data streaming simultaneously

3. **Write synchronization** - **WRFAST** writes complete in the background. To force a flush, issue the next **RDFAST**/**WRFAST** with D[31]=0 (it waits for the prior **WRFAST** to finish) rather than relying on a fixed delay

4. **Hub alignment** - Block transfers work best with long-aligned addresses

5. **FIFO depth** - The FIFO holds (cogs+11) = 19 longs. It refills automatically, so you rarely outrun it.

## Performance Numbers

Let's talk speed:

- **Block transfer**: Up to 1 long per clock (at 200MHz = 800MB/s!)
- **FIFO streaming**: Up to 1 long per clock sustained
- **Random hub access**: 9-16 clocks per access
- **Streamer to pins**: Up to sysclock/1 rate

Uff! That's seriously fast. Most microcontrollers need dedicated DMA controllers, peripheral coprocessors, and a stack of config registers to achieve what P2 does with two instructions. You're not paying for that DMA controller — it's already in the silicon.

## Real-World Example: Audio Buffer

Stream audio samples through processing:

```pasm2
' Audio processing pipeline
audio_process
        rdfast  #0, ##input_buffer      ' FIFO for reading input
        mov     ptra, ##output_buffer   ' PTRA for writing output
        mov     samples, ##BUFFER_SIZE

process_loop
        rflong  left_sample             ' Read left from FIFO
        rflong  right_sample            ' Read right from FIFO

        ' Apply simple low-pass filter
        add     left_filtered, left_sample
        shr     left_filtered, #1       ' Average with previous

        add     right_filtered, right_sample
        shr     right_filtered, #1

        ' Apply volume
        muls    left_filtered, volume
        muls    right_filtered, volume

        ' Output processed samples via PTRA
        wrlong  left_filtered, ptra++
        wrlong  right_filtered, ptra++

        djnz    samples, #process_loop
```

## What We've Learned

Your streaming skills now include:

- ✅ Block transfers with **SETQ**
- ✅ FIFO reading and writing
- ✅ Streaming pipeline concepts
- ✅ Circular buffer techniques
- ✅ Parallel processing while streaming
- ✅ Real-world applications

## Coming Up Next

Chapter 10 explores "hub execution" - how to break free from the 496-instruction limit and run massive programs directly from hub memory. It's like having your cake and eating it too!


**Have Fun!** Remember, streaming is about throughput, not just speed. It's the difference between carrying one brick at a time and using a wheelbarrow!


# Chapter 10: Hub Execution

*Breaking free from the 496-instruction limit*

## The Hook: Unlimited Code Space

Remember fretting about fitting your code into 496 cog instructions? Watch this:

```pasm2
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

Your code now lives in hub memory's 512KB instead of cog memory's 2KB. That's 256 times more space!

## Cog vs Hub Execution: The Trade-offs

Let's be honest about the differences:

**Cog Execution** (traditional):

- ✅ Fast: most simple instructions run in 2 clocks (hub accesses are 9–16, taken branches 5+)
- ✅ Deterministic: perfect for real-time
- ❌ Limited: only 496 instructions
- ✅ Self-contained: runs independently

**Hub Execution** (the new way):

- ✅ Fast sequential: 2 clocks per instruction (same as cog-exec, thanks to the 19-stage FIFO prefetch)
- ❌ Slower on branches: minimum 13 clocks per branch (the FIFO refill cost; +1 if target isn't long-aligned)
- ✅ Unlimited: 512KB of code space!
- ✅ Flexible: can call cog routines

The beauty? You can mix both in the same program! Sequential code in hub runs at full speed — only branches show the hub-execution penalty.

## How Hub Execution Works

Let's peek behind the curtain. When the processor encounters a jump or call to a hub address (≥$400), it automatically switches to hub execution mode. The FIFO starts streaming instructions from hub memory:

```pasm2
        org     0               ' Start in cog
        
cog_code
        ' This runs from cog RAM
        call    #hub_function   ' Call into hub
        ' Back in cog mode here
        
        orgh    $1000          ' Switch to hub addresses
        
hub_function
        ' This runs from hub RAM via FIFO
        ' Can be huge!
        ret                    ' Returns to cog code
```

The magic happens automatically. No mode switching instructions needed!

## Real-World Example: Menu System

Here's something that would never fit in cog RAM:

```pasm2
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

## The Hub Execution FIFO

You met the FIFO in the previous chapter as a data-streaming engine. Same hardware, different job here: it reads ahead, keeping a buffer of upcoming *instructions* ready for the cog. Think of it as a moving sidewalk for your code:

```pasm2
' The FIFO maintains performance by reading ahead
hub_loop
        add     x, y           ' FIFO has next instructions ready
        sub     a, b           ' No waiting for hub access
        mul     c, d           ' Instructions stream smoothly
        ' FIFO automatically refills as needed
```

This read-ahead behavior is the whole reason sequential hub code matches cog-exec speed — the FIFO is doing the waiting for you, in parallel with the cog running instructions it already prefetched.

## Mixing Cog and Hub Code

Here's the real power - combining both modes:

```pasm2
        org     0
        
' Critical timing code in cog
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

Time-critical code stays in cog RAM for deterministic timing. Complex code lives in hub RAM for space.

## Your Turn: Hub Execution Experiments

::: your-turn
**Your Turn:** Build a simple calculator

Starting code:

```pasm2
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

Goal: Create a multi-function calculator
Hint: Each function can be as complex as needed
Success Check: Multiple operations working
:::

::: medicine-cabinet
Overwhelmed by execution modes? Here's the simple version:

**Keep it simple:**

1. **Small, time-critical code** → Put in cog (org 0)
2. **Large, complex code** → Put in hub (orgh $400+)
3. **Don't overthink it** → The processor handles the switch

**Basic pattern:**

```pasm2
        org     0
        jmp     #main      ' Jump to hub

        orgh    $400
main    ' Your big program here
```

That's it. Let the processor worry about the details!
:::

## Advanced Hub Execution

### Long Jumps and Calls

Hub addresses need 20 bits, so jumping far requires special handling:

```pasm2
' Jump to distant hub code
        jmp     #\far_away  ' \ forces 20-bit absolute (non-relative) addr
        
        orgh    $40000        ' Far away in hub
far_away
        ' Code here
```

### Hub Data Access from Hub Code

When executing from hub, you can still access hub data:

```pasm2
        orgh    $1000
        
hub_code
        rdlong  value, ##hub_data  ' Read hub data
        add     value, #1
        wrlong  value, ##hub_data  ' Write back
        
        orgh    $8000
hub_data
        long    $12345678
```

### Performance Optimization

To maximize hub execution speed:

```pasm2
' Align branch targets to long (4-byte) boundaries
        alignl                 ' Align to long boundary
loop_start
        ' Loop code here
        djnz    count, #loop_start
        
' Keep critical loops small
' Consider moving inner loops to cog RAM
```

## Common Hub Execution Gotchas

Before you cram everything into hub and call it a day, know these:

1. **Speed variation** - Don't use hub execution for precise timing
2. **FIFO conflicts** - Can't stream data while executing from hub
3. **Address confusion** - Remember: <$200 is cog, $200-$3FF is LUT, ≥$400 is hub
4. **Stack depth** - Still limited to 8-level hardware stack
5. **Relative jumps** - Work differently in hub mode

## Real-World Example: Command Parser

```pasm2
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
' Would need multiple cogs without hub execution!
```

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

- ✅ Understanding cog vs hub trade-offs
- ✅ Automatic mode switching
- ✅ Mixing cog and hub code
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

```antipattern
' Traditional approach (not P2!) — interrupt-driven pseudocode
ISR(BUTTON_INTERRUPT)
    ' Interrupt service routine
    buttonPressed = true
    ' Return to interrupted code
END_ISR
```

And here's the P2 way:

```pasm2
' Dedicated cog watching button
button_watcher
        testp   #BUTTON_PIN wc
   if_c wrlong  ##1, ##button_flag
        jmp     #button_watcher
        
' Main cog doing important work
main_code
        ' Never interrupted!
        ' Checks button_flag when convenient
```

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

```pasm2
' cog 0: Main application
main_app
        ' Complex calculations
        ' Never interrupted
        rdlong  command, ##mailbox wz
   if_nz call   #process_command
        jmp     #main_app

' cog 1: Serial port handler
serial_handler
        ' Continuously monitors serial
        testp   #RX_PIN wc
   if_c call    #receive_byte
        jmp     #serial_handler
        
' cog 2: Motor control
motor_control
        ' Precise timing loops
        ' Never disrupted
        waitx   motor_time
        drvnot  #STEP_PIN
        jmp     #motor_control
        
' cog 3: Sensor monitor
sensor_monitor
        ' Watches multiple sensors
        ' Responds instantly
        ' ... and so on
```

Each cog does one thing perfectly. No interruptions. No conflicts. Just pure, focused execution.

## Real-World Example: Dedicated-Cog Servo Control

With interrupts, servo pulses jitter. With dedicated cogs, they're rock-steady:

```pasm2
' cog dedicated to servo control
servo_cog
        getct   pulse_time
        
servo_loop
        ' Generate 8 servo pulses simultaneously
        mov     servo_mask, ##$FF      ' 8 servos
        or      outa, servo_mask       ' All high
        
        mov     index, #0
check_servos
        mov     addr, index            ' PTR index is compile-time only,
        shl     addr, #2               '   so build the address by hand:
        add     addr, ptra             '   ptra (table base) + index*4
        rdlong  width, addr            ' Get pulse width
        addct1  pulse_time, width      ' Set compare time
        
        waitct1                        ' Wait for exact time
        bitl    outa, index            ' Turn off this servo
        
        incmod  index, #7  wc          ' C set when index wraps 7->0
  if_nc jmp     #check_servos          ' Loop until all 8 servos done
        
        ' Wait for 20ms frame
        waitx   ##4_000_000
        jmp     #servo_loop
        
' Result: 8 servos with ZERO jitter!
```

Try that with interrupts. I'll wait. You *can* get there — a dedicated timer peripheral and a very careful interrupt scheme will do it — but notice what you just spent to buy it, and what happens to that scheme the day you add a ninth job.

## "But P2 HAS Interrupts!"

Yes, it does. And you probably shouldn't use them.

Well, let me be more nuanced. P2 has interrupts for those rare cases where you absolutely need them:

```pasm2
' Setting up an interrupt (not recommended!)
        setse1  #%001<<6 + PANIC_BUTTON   ' SE1 triggers when pin goes high
        setint1 #EVENT_SE1                ' Enable INT1 on SE1 event

int1_handler
        ' Interrupt code here
        reti1
```

When might you use them?

- Porting legacy code that requires interrupts
- Ultra-low-power designs where cogs must sleep
- Theoretical minimum latency response (but dedicated cog is usually faster!)

Uff! Even writing interrupt code feels wrong on a Propeller!

::: medicine-cabinet
Still thinking you need interrupts? Here's your medicine:

**Think you need an interrupt for...**

**Fast response?**

```pasm2
' Dedicated cog responds in ~6 clocks
watcher
        testp   #INPUT_PIN wz         ' Test pin state
  if_nz jmp     #watcher              ' Loop until pin high
        drvh    #RESPONSE_PIN         ' Instant response!
```

**Multiple events?**

```pasm2
' One cog watches everything
monitor
        test    sensors, #SENSOR1 wz
   if_nz call   #handle_sensor1
        test    sensors, #SENSOR2 wz
   if_nz call   #handle_sensor2
        ' Check all sensors every loop
```

**Periodic tasks?**

```pasm2
' Perfect timing without interrupts
        getct   next_time
.loop   addct1  next_time, ##PERIOD
        waitct1                ' Exact timing
        call    #periodic_task
        jmp     #.loop
```

See? No interrupts needed!
:::

## The Event System: Better Than Interrupts

P2 has something better than interrupts - events:

```pasm2
' Configure event to watch pin
        setse1  #%001<<6 + BUTTON_PIN   ' Rising edge event
        
' Main code runs normally
main_loop
        ' Do work...
        pollse1 wc              ' Check if event occurred
   if_c call    #handle_button  ' Handle when convenient
        ' Continue work...
        jmp     #main_loop
```

Events are like interrupts that wait politely for you to check them. No rudeness!

## Interrupt Horror Stories

Let me share why we avoid interrupts:

### Story 1: The Jittery Display

| Approach | Problem | Result |
|----------|---------|--------|
| **With Interrupts** | Display updates interrupted by serial | Visible glitches, tearing, inconsistent timing |
| **With Cogs** | Display Cog runs uninterrupted | Perfect, smooth, glitch-free display |

### Story 2: The Missed Pulse

| Approach | Problem | Result |
|----------|---------|--------|
| **With Interrupts** | Motor step interrupted by sensor read | Missed step, motor stalls, position lost |
| **With Cogs** | Motor Cog never misses a beat | Perfect positioning, no lost steps |

### Story 3: The Debugging Nightmare

| Approach | Problem | Result |
|----------|---------|--------|
| **With Interrupts** | Bug only appears under specific timing | Days of debugging, hair loss, coffee overdose |
| **With Cogs** | Deterministic timing, reproducible behavior | Bug found in minutes, sanity preserved |

## Your Turn: Cog vs Interrupt Challenge

::: your-turn
**Your Turn:** Build a reaction timer without interrupts

Starting code:

```pasm2
        org     0
        
' cog 0: Main game logic
        setq    ##button_flag           ' PTRA for new cog
        coginit #1, @button_watcher
        
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
        
' cog 1: Button watcher
        orgh    $400
button_watcher
        ' Your code here
```

Goal: Implement button watcher cog
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

- Every cog runs predictably
- Your cog's timing doesn't change because another cog got busy
- What you measure today is what you'll measure next week

It's the difference between one gifted soloist who has to play every part in turn, and an orchestra where each player has their own part and keeps to it whatever the others are doing.

## When Interrupts Actually Make Sense

I'll admit it - there are rare cases where interrupts are appropriate:

1. **Power-critical applications** where cogs must sleep
2. **Legacy code ports** that fundamentally require interrupts
3. **Single-cog designs** (but why waste the P2's power?)

But in 15 years of Propeller programming, I've needed interrupts exactly... never.

## Common "But What About..." Questions

**Q: "But what about interrupt priority?"**
A: Cogs don't have priority. They're all equal. Design your system accordingly.

**Q: "How do I handle critical events?"**
A: Dedicate a cog to critical events. It will respond faster than any interrupt.

**Q: "Isn't dedicating a whole cog wasteful?"**
A: You have eight! And a focused cog is simpler than interrupt-riddled code.

**Q: "What about power consumption?"**
A: Use WAITSE/WAITCT for low-power waiting. Cog sleeps until event.

## What We've Learned

You now understand the Propeller way:

- ✅ Why interrupts cause problems
- ✅ How cogs eliminate interrupt need
- ✅ event system as polite alternative
- ✅ Real-world benefits of no interrupts
- ✅ Rare cases where interrupts might be used
- ✅ The philosophy of determinism

## Coming Up Next

Chapter 12 shows you "Optimization Mastery" - how to make your PASM2 code blazingly fast. We'll explore the pipeline, instruction pairing, and timing tricks that squeeze every drop of performance from the P2.


**Have Fun!** And remember - in a world of interruptions, be a cog: focused, deterministic, and uninterruptible!


# Chapter 12: Optimization Mastery

*Making the fast faster*

## The Hook: Cut Loop Overhead with One Change

Let me show you a loop that looks fine — until you realize you're paying for the same thing twice. Watch:

```pasm2
' Before optimization: ~18+ clocks (sum of the per-line minimums below)
.loop   rdlong  value, ptra      ' 9-16 (cog-exec) / 9-26 (hub-exec)
        add     value, #1        ' 2 clocks
        wrlong  value, ptra      ' 3-10 (cog-exec) / 3-20 (hub-exec)
        add     ptra, #4         ' 2 clocks
        djnz    count, #.loop    ' 2/4 (cog-exec) / 2/13-20 (hub-exec)

' After optimization using PTR expressions:
.loop   rdlong  value, ptra      ' Read from current address
        add     value, #1        ' Process
        wrlong  value, ptra++    ' Write and increment in one!
        djnz    count, #.loop    ' Saved the ADD instruction
```

That trims one instruction (2 clocks) per iteration—a modest ~10% off this hub-bound loop, and it's free. The secret? Understanding how P2 really works.

## Understanding the Pipeline

Before we hunt for clocks to save, let's understand where they go in the first place. P2 uses a **5-stage pipeline** - up to five instructions are in flight at once, each at a different stage. You don't need the stage-by-stage breakdown; what matters is the payoff: when the pipeline stays full, an instruction effectively completes every **2 clocks**.

This is why, while one instruction executes, the next is already being fetched:

```pasm2
        add     x, y      ' Executing while next inst fetches
        sub     a, b      ' Fetching while previous executes
        ' Perfect overlap = maximum throughput
```

## Instruction Timing Basics

Not all instructions are created equal:

```pasm2
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
        getqx   result          ' 2 clocks (but wait 55 for result)
```

## REP: The Speed Loop

**REP** creates hardware-accelerated loops with zero overhead:

```pasm2
' Traditional loop: overhead per iteration
.loop   add     sum, value      ' 2 clocks
        add     ptr, #4         ' 2 clocks
        djnz    count, #.loop   ' 2 or 4 clocks (4 if branch taken)

' REP loop: 0 clocks overhead!
        rep     #2, count       ' Repeat next 2 instructions
        add     sum, value      ' 2 clocks
        add     ptr, #4         ' 2 clocks = 4 total!
```

That's about 50% faster: the traditional loop pays 2 + 2 + 4 clocks (the taken **DJNZ** costs 4), while the **REP** body is just 4 clocks.

**Hub-exec note:** **REP** works in hub-exec too, but each iteration executes a hidden jump to loop back — and that hidden jump pays the 13+ clock hub-branch cost per iteration. So a 2-instruction **REP** loop that takes 4 clocks in cog-exec balloons to ~17+ clocks per iteration in hub-exec. For time-critical inner loops, keep **REP** in cog or LUT memory. Hub-exec **REP** works correctly; it just isn't zero-overhead there.

## SKIP: Conditional Execution on Steroids

**SKIP** and **SKIPF** let you conditionally execute patterns of instructions:

```pasm2
' Traditional: multiple jumps
        cmp     x, #5 wcz
if_a    jmp     #greater
if_b    jmp     #less
        jmp     #equal

' With SKIP: cancel optional steps per a precomputed pattern
'   bit N (LSB first) skips the Nth instruction after SKIP
        skip    config_mask     ' e.g. %010 runs steps 0 and 2, skips step 1
        call    #setup_uart     ' Step 0
        call    #setup_spi      ' Step 1
        call    #setup_timer    ' Step 2
        ' One pattern picks which steps run — no jumps, no stalls!
```

## Hub Access Optimization

Hub timing is critical for performance:

```pasm2
' Hub RAM allows any byte address (no masking, unlike P1). An unaligned
' long may cost at most one extra clock if it straddles a slice — still
' within RDLONG's normal 9-16 range, so it's nothing to optimize around
        rdlong  v1, ##$1001     ' Unaligned: essentially the same cost
        rdlong  v1, ##$1000     ' Aligned: no meaningful speedup
        
' Sequential ptra++ is convenient, but each read is still 9-16 clocks;
' for real throughput use the FIFO (RFLONG) or a SETQ burst
        rdlong  v1, ptra++      ' Hardware manages the pointer
        rdlong  v2, ptra++
        rdlong  v3, ptra++
```

## The FIFO Fast Path

For ultimate speed, use the FIFO:

```pasm2
' Traditional hub reading: ~13+ clocks per long (RDLONG alone is 9-16)
.loop   rdlong  value, ptra++
        add     sum, value
        djnz    count, #.loop

' FIFO reading: RFLONG is always 2 clocks
        rdfast  #0, ptra        ' Start FIFO
.loop   rflong  value           ' 2 clocks, always!
        add     sum, value      ' 2 clocks
        djnz    count, #.loop   ' 4 clocks when it branches back
        ' ~2x faster for sequential reads!
```

## Parallel Operations

CORDIC operations can overlap with other work:

```pasm2
' CORDIC overlaps with other instructions
        qmul    x, y            ' Start 32x32->64 multiply (CORDIC)
        ' 55 clocks to do other work!
        add     a, b            ' These execute during CORDIC
        sub     c, d
        mov     index, #0
        rdlong  data, ptra++
        ' ... more work
        getqx   low_result      ' Get CORDIC result (lower 32 bits)
        getqy   high_result     ' Get CORDIC result (upper 32 bits)

' QROTATE overlap
        qrotate x_coord, angle  ' Start rotation (D=X, S=angle)
        ' 55 clocks of other work!
        getqx   new_x           ' Get rotated X
        getqy   new_y           ' Get rotated Y
```

Note: **MUL**/**MULS** are 2-clock ALU instructions that complete immediately (16x16->32). Use **QMUL** for 32x32->64 with CORDIC overlap.

## Real-World Example: Fast Memory Copy

Let's optimize a memory copy routine:

```pasm2
' Version 1: Basic (slow)
copy_basic
        rdlong  temp, source
        wrlong  temp, dest
        add     source, #4
        add     dest, #4
        djnz    count, #copy_basic
        ' ~18+ clocks per long

' Version 2: Better pointers
copy_better
        rdlong  temp, ptra++
        wrlong  temp, ptrb++
        djnz    count, #copy_better
        ' ~14+ clocks per long
        
' Version 3: Block transfer (ultimate)
copy_ultimate
        sub     count, #1       ' SETQ needs count-1 (0 = 1 long)
        setq    count           ' Setup block transfer
        rdlong  buffer, source  ' Read all at once
        setq    count           ' (count already decremented)
        wrlong  buffer, dest    ' Write all at once
        ' ~1 clock per long for large blocks (hub maximum)!
```

::: medicine-cabinet
Optimization overwhelming you? Start with these simple improvements:

**Three easy wins:**

1. **Use PTRA/PTRB** instead of manual pointer math

```pasm2
' Slow
        rdlong  x, addr
        add     addr, #4

' Fast
        rdlong  x, ptra++
```

2. **Align your data** to long boundaries

```pasm2
        alignl          ' Force long alignment
data    long    $12345678
```

3. **Use REP** for tight loops (note: `ptra++` works with the hub RD/WR instructions and with **RDLUT**/**WRLUT**—not with ordinary ALU ops—so we read first, then add)

```pasm2
        rep     @.end, count
        rdlong  val, ptra++     ' Fetch next long from hub
        add     sum, val        ' Accumulate
.end
```

Just these three changes trim the overhead instructions off a hub-bound loop—a modest but free speedup.
:::

## Your Turn: Optimization Challenges

::: your-turn
**Your Turn:** Optimize a checksum calculator

Starting code:

```pasm2
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

Goal: Make it at least 4x faster
Hint: Read longs instead of bytes, use FIFO
Success Check: Same checksum, much faster
:::

## Advanced Techniques

### Instruction Pairing

Some instruction pairs execute specially:

```pasm2
' ## syntax handles AUGS automatically
        mov     x, ##$12345678  ' Assembler generates AUGS + MOV
        ' Same result, cleaner code!
        
' ALTD + instruction = indirect addressing
        altd    index, #array
        mov     0-0, value      ' Stores to array[index]
```

### Pipeline-Aware Coding

Good news: unlike many pipelined CPUs, the P2 has **no data-dependency stalls**. A register result is ready for the very next instruction, so these back-to-back ops each take just 2 clocks:

```pasm2
        add     x, y
        cmp     x, #10 wcz      ' x is ready — no stall
```

The stalls worth planning around are the multi-cycle ones: hub accesses (9–16 clocks) and taken branches (pipeline flush). Interleave *those* with useful work, not ordinary ALU ops.

### Unrolling Loops

Sometimes removing the loop is faster. (Remember: `ptra++` works with the hub RD/WR instructions and with **RDLUT**/**WRLUT**—not with ordinary ALU ops—so each iteration reads then adds.)

```pasm2
' Looped version
        rep     @.end, #4
        rdlong  val, ptra++
        add     sum, val
.end

' Unrolled version (faster for small counts)
        rdlong  val, ptra++
        add     sum, val
        rdlong  val, ptra++
        add     sum, val
        rdlong  val, ptra++
        add     sum, val
        rdlong  val, ptra++
        add     sum, val
```

## Common Optimization Gotchas

Before you rewrite everything in **REP** and **SKIP**, a few sanity checks:

1. **Premature optimization** - Get it working first, then optimize
2. **Over-optimizing** - Sometimes clarity is worth 2 clocks
3. **Ignoring the big picture** - Optimize the bottleneck, not everything
4. **Breaking functionality** - Fast but wrong is useless
5. **Forgetting about power** - Faster isn't always better for battery life

## Profiling and Measurement

Always measure your optimizations:

```pasm2
' Time your code
        getct   start_time
        
        ' Code to measure
        call    #function_to_test
        
        getct   end_time
        sub     end_time, start_time
        ' end_time now contains exact clock cycles
```

**Pitfall — CT wraps:** **GETCT** reads a 32-bit free-running counter that wraps every ~21.5 seconds at 200 MHz (2³² ÷ 200 MHz). For short measurements like the one above, the **SUB** trick masks the wrap correctly thanks to two's-complement arithmetic. But for a *scheduler* or *timer* running over minutes, hours, or days, you need one of two strategies:

1. **Capture the full 64-bit count.** `GETCT D WC` latches the full 64-bit counter and returns its upper 32 bits (with `WC` set); the very next `GETCT D` (no `WC`) returns the matching lower 32 bits of that same instant. Keep the two instructions back-to-back and uninterrupted—no re-read-and-retry loop is needed.
2. **Work with deltas, not absolute time.** Compare `(now - start)` rather than `now > deadline`. The subtraction wraps correctly even when the counter does.

The 21.5-second wrap is *fast* — long enough that you won't see it in a basic example, short enough that real applications hit it constantly.

## What We've Learned

You're now an optimization expert:

- ✅ Understanding the P2 pipeline
- ✅ Instruction timing knowledge
- ✅ **REP** and **SKIP** for zero-overhead loops
- ✅ FIFO for maximum throughput
- ✅ Parallel operation techniques
- ✅ Real-world optimization strategies

## Coming Up Next

Chapters 13-15 dig into LUT memory, smart pins, and event-driven programming - with references to dedicated manuals for deep dives. Think of them as appetizers showing what's possible!


**Have Fun!** Remember, the best optimization is often a better algorithm. But when you need every last cycle, you now know how to get them!


# Chapter 13: LUT Memory - Your Private Lookup Table

*512 longs of fast, deterministic storage in every cog*

## The Hook: A Lookup Table in 3 Cycles

Need fast data lookup without hub timing? Every cog has its own private 512-long Lookup RAM (LUT):

```pasm2
' Sine table lookup - 3 clocks, every time
get_sine
        and     angle, #$FF      ' Mask to table index
        rdlut   value, angle     ' Read from LUT in 3 clocks!
        ret
```

No hub timing to worry about. No waiting for the egg beater. Just 3 clock cycles, guaranteed. The LUT is like having a personal data assistant that never takes a coffee break.

## Why Another Memory?

You might be thinking, "Wait, I already have cog RAM and hub RAM - why do I need a third memory?" Excellent question!

| Memory | Size per Cog | Access Time | Special Features |
|--------|--------------|-------------|------------------|
| Cog RAM | 512 longs | 2 clocks | Instructions live here |
| Hub RAM | 512 KB shared | 9-16 clocks (hub slot wait) | Shared by all cogs |
| **LUT RAM** | 512 longs | **3 clocks** | **Private, deterministic; shareable with a neighbor cog (see below)** |

The LUT fills a sweet spot: faster than hub memory, doesn't compete with your instruction space, and has a trick up its sleeve - neighboring cogs can share LUTs!

## Reading and Writing the LUT

### Basic LUT Access

```pasm2
' Write to LUT
        wrlut   ##$12345678, #100 ' Write 32-bit constant to LUT[100]
        wrlut   value, index      ' Write variable to LUT[index]

' Read from LUT
        rdlut   result, #100      ' Read LUT[100] into result
        rdlut   data, index       ' Read LUT[index] into data
```

Notice the operand order: **WRLUT** writes its first operand to the address in the second, while **RDLUT** reads from its second operand into the first. A bit backwards from what you might expect, but you'll get used to it.

### Building a Lookup Table

Here's how to load a sine table into LUT:

```pasm2
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

::: sidetrack
**Bulk LUT Loading with SETQ2**

For loading entire tables, **SETQ2** + **RDLONG** transfers hub data into LUT memory. The trick: when **SETQ2** is active, the **RDLONG** destination field (still 9-bit, 0–$1FF) is interpreted as a LUT offset that maps physically to $200–$3FF:

```pasm2
        setq2   #256-1              ' 256 longs to LUT
        rdlong  $000, hub_table_ptr ' Dest field 0 = physical LUT $200
```

The destination operand is the LUT offset, not the absolute address — so you write `$000` (LUT base), not `$200` (which would overflow the 9-bit field). Remember the `-1` in **SETQ2** (same rule as **SETQ** for hub block transfers).
:::

## LUT Sharing Between Cogs

Here's something clever: adjacent cog pairs can share LUT data! When you enable LUT sharing with **SETLUTS**, writes your neighbor makes to their LUT are automatically *copied* to your LUT too.

```pasm2
' --- cog 1 (consumer) - MUST enable sharing FIRST ---
        setluts #1              ' Enable LUT write copying FROM cog 0
        ' Now when cog 0 writes to its LUT, data is COPIED to our LUT

' --- cog 0 (producer) - writes AFTER consumer enables sharing ---
        wrlut   message, #10    ' Write MY LUT[10] (copies to cog 1)
        wrlut   #1, #0          ' Set ready flag (copies to cog 1)

' --- cog 1 (consumer) - reads its OWN LUT (which contains copies) ---
.wait   rdlut   flag, #0        ' Read MY LUT[0] (contains copy from cog 0)
        cmp     flag, #1 wz
  if_nz jmp     #.wait
        rdlut   message, #10    ' Read MY LUT[10] (copied from cog 0)
```

The key instruction is:

- **SETLUTS**: Enable write copying - when neighbor writes with **WRLUT**, data is copied to YOUR LUT
- **RDLUT**: Read your own LUT (which now contains copied data)

Important: The consumer cog must enable **SETLUTS** *before* the producer writes, otherwise the writes won't be copied!

This gives you a 512-long shared buffer between cog pairs without touching hub memory. Perfect for high-bandwidth data passing!

::: sidetrack
**Which Cogs Are Neighbors?**

The LUT sharing pairs are fixed:

- Cog 0 ↔ cog 1
- Cog 2 ↔ cog 3
- Cog 4 ↔ cog 5
- Cog 6 ↔ cog 7

When you enable sharing, your odd/even companion cog's LUT *writes* are copied into your own LUT — so you read the copies from your own LUT. Sharing works only within the fixed pair; non-adjacent cogs cannot share.
:::

## Practical Examples

Enough theory — let's see what people actually use the LUT for in real code:

### Fast Data Transformation

```pasm2
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

### Circular Buffer in LUT

```pasm2
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

### Fast Stack in LUT

```pasm2
' Stack implementation in LUT
' Grows downward from $1FF
stack_ptr       long    $1FF

stack_push
        wrlut   value, stack_ptr
        sub     stack_ptr, #1
        ret

stack_pop
        add     stack_ptr, #1
        rdlut   value, stack_ptr
        ret
```

## LUT with the Streamer

Here's where LUT gets really interesting. The streamer can read directly from LUT to generate waveforms without any cog intervention:

```pasm2
' Fill LUT with waveform data
' Then let Streamer output it to DAC

load_waveform
        mov     index, #0

.fill   mov     value, index
        shl     value, #24       ' Scale for DAC
        wrlut   value, index
        add     index, #1
        cmp     index, ##512 wz
  if_nz jmp     #.fill

' Now configure Streamer to read from LUT
' Streamer handles the rest - no cog cycles needed!
```

The streamer configuration for LUT reading is covered in detail in the Video and Audio manuals - but the key point is that your LUT becomes a 512-sample waveform buffer that plays automatically.

## Common Gotchas

**❌ WRONG: Confusing LUT addresses**

```antipattern
' WRONG - $200 isn't a cog register at all (cog RAM is $000..$1FF)
        mov     value, $200  ' Won't reach LUT; 9-bit reg can't hold $200
```

**✓ RIGHT: Use RDLUT for LUT access**

```pasm2
' RIGHT - RDLUT addresses the LUT space
        rdlut   value, #0       ' LUT address 0
```

**❌ WRONG: Reading LUT before neighbor writes**

```antipattern
' WRONG - No data to read yet!
        setluts #1              ' Enable sharing
        rdlut   data, #10       ' Empty - neighbor hasn't written!
```

**✓ RIGHT: Wait for neighbor's write signal**

```pasm2
' RIGHT - Wait for data to be copied
        setluts #1              ' Enable sharing BEFORE neighbor writes
.wait   rdlut   ready, #0       ' Check flag in MY LUT
        tjz     ready, #.wait   ' Wait until neighbor writes
        rdlut   data, #10       ' Now MY LUT has copied data
```

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
- Cog-pair data sharing
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
**Exercise 2: High-Speed Cog Communication**

Use LUT sharing to create a message passing system between cog 2 and cog 3:

- Cog 2 writes 8-long messages
- Cog 3 reads them without hub access
- Use a simple ready/ack protocol

```pasm2
' Hint: Use LUT[0] as ready flag, LUT[1-8] as message buffer
```
:::

## What We've Learned

The LUT in your toolbox:

- ✅ 512 longs of fast, private memory in every cog
- ✅ Deterministic access via **RDLUT** (3 clocks) / **WRLUT** (2 clocks)
- ✅ Bulk loading via **SETQ2** + **RDLONG**
- ✅ cog-pair LUT sharing for high-bandwidth data passing
- ✅ streamer source for waveform generation

## Coming Up Next

Chapter 14 hands you the keys to 64 autonomous I/O processors — smart pins. We'll cover the universal configuration pattern and the modes you'll reach for most often, then point you at the dedicated Smart Pins Manual for the deep dive.


**Have Fun!** And remember — a 3-clock private lookup table is a luxury most chips don't give you. Use it!


# Chapter 14: Smart Pins Orientation

*64 autonomous I/O processors waiting to do your bidding*

## The Hook: A UART in 4 Lines

Remember that tedious bit-bang serial from Chapter 8? Watch this:

```pasm2
' Configure pin as UART transmitter - done!
        dirl    #TX_PIN                 ' Reset pin first!
        wrpin   ##P_ASYNC_TX | P_OE, #TX_PIN  ' Async TX; P_OE drives output
        wxpin   ##BAUD_115200, #TX_PIN  ' Set baud rate
        dirh    #TX_PIN                 ' Enable - runs on its own
```

That's it. The pin is now a fully autonomous UART transmitter. It handles start bits, stop bits, timing - everything. You just feed it bytes with **WYPIN** and it sends them. The pin has become a state machine.

And here's the mind-bending part: *every single one of the 64 pins can do this*. Or PWM. Or ADC. Or quadrature decoding. Or 28 other modes.

## What Are Smart Pins, Really?

Each of the P2's 64 I/O pins contains its own little processor - a state machine that can operate completely independently of the cogs. This means:

- A pin configured as UART keeps sending/receiving without cog intervention
- A PWM output keeps running its duty cycle automatically
- An ADC samples continuously in the background
- A quadrature decoder tracks position even while your cog does other things

The cog only needs to configure the pin and occasionally read/write data. The pin does the rest.

## The Universal Smart Pin Pattern

Every smart pin follows the same configuration pattern. This is **the most important thing to remember**:

```pasm2
' === THE SMART PIN RECIPE ===

' Step 1: RESET the pin (CRITICAL!)
        dirl    pin             ' Always start by resetting

' Step 2: CONFIGURE the mode
        wrpin   mode, pin       ' What should this pin do?

' Step 3: SET the X parameter
        wxpin   x_value, pin    ' Mode-specific parameter X

' Step 4: ENABLE the pin
        dirh    pin             ' Start the magic!

' Step 5: WRITE Y / data -- AFTER enable!
        wypin   y_value, pin    ' Mode-specific parameter Y
```

Why is `wypin` shown last, *after* `dirh`? For the serial and trigger modes,
**WYPIN** is how you *feed data* to a running pin -- each byte you transmit is a
fresh `wypin` issued after the pin is enabled, so that's where it naturally
lives. (The silicon documentation's configuration procedure actually writes
**WRPIN**/**WXPIN**/**WYPIN** while DIR is low and *then* raises DIR; for pure value modes
that order is fine too. Once the pin is live, feeding it with **WYPIN** is just the
normal operating pattern.)

::: sidetrack
**Why DIRL First?**

The **DIRL** at the start isn't optional politeness - it's *required*. Smart pins must be reset before configuration to ensure they're in a known state. Skip this and you'll get unpredictable behavior as old settings conflict with new ones.

Think of it like power-cycling a misbehaving device. Always start fresh.
:::

## The Core Instructions

### Configuration Instructions

| Instruction | Purpose |
|-------------|---------|
| **WRPIN** mode, pin | Set the operating mode |
| **WXPIN** value, pin | Set X parameter (mode-specific) |
| **WYPIN** value, pin | Set Y parameter (mode-specific) |
| **DIRH** pin | Enable the smart pin |
| **DIRL** pin | Disable/reset the smart pin |

### Data Instructions

| Instruction | Purpose |
|-------------|---------|
| **WYPIN** data, pin | Write data to smart pin (same instruction!) |
| **RDPIN** data, pin | Read result, clear "ready" flag |
| **RQPIN** data, pin | Read result, keep "ready" flag |
| **AKPIN** pin | Acknowledge (clear "ready" flag only) |

### Status Instructions

| Instruction | Purpose |
|-------------|---------|
| **TESTP** pin WC | Check if IN flag is set (data ready) |
| **TESTPN** pin WC | Check if IN flag is clear |

## Understanding the IN Flag

Every smart pin has an IN flag that signals "something happened." What that something is depends on the mode:

- **UART TX**: IN high = ready for another byte
- **UART RX**: IN high = byte received
- **ADC**: IN high = new sample ready
- **PWM**: IN high = period complete
- **Counter**: IN high = measurement period complete (result ready to read)

You check this flag with **TESTP** and clear it by reading with **RDPIN** (or explicitly with **AKPIN**).

```pasm2
' Wait for smart pin to be ready
wait_ready
        testp   #PIN wc         ' Check IN flag
  if_nc jmp     #wait_ready     ' Loop if not ready
        rdpin   data, #PIN      ' Read and clear flag
```

::: sidetrack
**Event-Driven Alternative**

Instead of polling with **TESTP**, you can use the event system:

```pasm2
setse1  #%001<<6 + PIN   ' Event when IN rises
waitse1                   ' Sleep until ready - no polling!
rdpin   result, #PIN      ' Read the result
```

This is more efficient because your cog sleeps instead of spinning. See Chapter 15 for the full event story.
:::

## Common Smart Pin Modes

Here are the modes you'll use most often:

### Asynchronous Serial (UART)

```pasm2
' Transmit mode
        dirl    #TX_PIN
        wrpin   ##P_ASYNC_TX | P_OE, #TX_PIN
        wxpin   ##(CLK_FREQ/BAUD)<<16 | 7, #TX_PIN  ' Baud + 8 bits
        dirh    #TX_PIN

' Send the first byte immediately -- the buffer is empty right after enable
        wypin   txbyte, #TX_PIN

' Before each *subsequent* byte, wait until the pin is ready for more
.send   testp   #TX_PIN wc      ' IN rises once a word moves to the shifter
  if_nc jmp     #.send
        wypin   txbyte, #TX_PIN ' Send the next byte
```

```pasm2
' Receive mode
        dirl    #RX_PIN
        wrpin   ##P_ASYNC_RX, #RX_PIN
        wxpin   ##(CLK_FREQ/BAUD)<<16 | 7, #RX_PIN
        dirh    #RX_PIN

' Get a byte
.recv   testp   #RX_PIN wc      ' Check for received byte
  if_nc jmp     #.recv
        rdpin   rxbyte, #RX_PIN ' Get it
        shr     rxbyte, #24     ' Shift to low byte
```

### PWM Output

```pasm2
' PWM mode - period + duty cycle
        dirl    #PWM_PIN
        wrpin   ##P_PWM_SAWTOOTH | P_OE, #PWM_PIN
        ' X[31:16]=frame, X[15:0]=base period
        wxpin   ##frame_period<<16 | base_period, #PWM_PIN
        dirh    #PWM_PIN
        wypin   ##duty, #PWM_PIN        ' High time; Y after enable

' Change duty cycle on the fly
        wypin   ##new_duty, #PWM_PIN    ' Just update Y parameter
```

### ADC Input

```pasm2
' ADC mode - continuous sampling
        dirl    #ADC_PIN
        wrpin   ##P_ADC | P_ADC_1X, #ADC_PIN
        wxpin   ##13, #ADC_PIN          ' 14-bit mode (period = 2^13 clocks)
        dirh    #ADC_PIN

' Read ADC value
read_adc
        rdpin   adc_value, #ADC_PIN     ' Get N-bit ADC count (LSB-aligned)
```

### Quadrature Encoder

```pasm2
' Quadrature decoder - A on pin, B on pin+1
        dirl    #ENC_PIN
        ' P_PLUS1_B routes the B phase from the next pin up
        wrpin   ##P_QUADRATURE | P_PLUS1_B, #ENC_PIN
        wxpin   #0, #ENC_PIN            ' 0 = continuous totalizer
        dirh    #ENC_PIN

' Read position
        rdpin   position, #ENC_PIN      ' Get accumulated count
```

## Configuration Values Demystified

Don't worry, you don't have to memorize all 32 mode bit-patterns. The mode values like `P_ASYNC_TX` are constants defined by the assembler. But here's what's happening behind the scenes, in case you're curious:

The **WRPIN** D value is a 32-bit configuration:

```{=latex}
\WRPINBitFieldDiagram
```

For most common modes, you'll use predefined constants like `P_ASYNC_TX`, `P_PWM_SAWTOOTH`, `P_ADC`. The P2 assembler knows all of them.

## Common Gotchas

**❌ WRONG: Forgetting to reset before configure**

```antipattern
' WRONG - Pin may be in unknown state!
        wrpin   ##P_PWM_SAWTOOTH | P_OE, #PIN
        wxpin   ##1000, #PIN
        dirh    #PIN
```

**✓ RIGHT: Always DIRL first**

```pasm2
' RIGHT - Start clean
        dirl    #PIN                    ' Reset first!
        wrpin   ##P_PWM_SAWTOOTH | P_OE, #PIN
        wxpin   ##1000, #PIN
        dirh    #PIN
```

**❌ WRONG: Enabling before configuring**

```antipattern
' WRONG - Pin enabled with partial config!
        dirl    #PIN
        dirh    #PIN                    ' Enabled too early!
        wrpin   ##P_ASYNC_TX | P_OE, #PIN
```

**✓ RIGHT: DIRH comes last**

```pasm2
' RIGHT - Configure completely, then enable
        dirl    #PIN
        wrpin   ##P_ASYNC_TX | P_OE, #PIN
        wxpin   ##BAUD, #PIN
        dirh    #PIN                    ' Enable last!
```

## Medicine Cabinet

::: medicine-cabinet
**Smart Pin Quick Reference**

**The Recipe:**

1. **DIRL** pin — Reset the pin first
2. **WRPIN** mode, pin — Set the operating mode (`| P_OE` if it *outputs*)
3. **WXPIN** x, pin — Set X parameter
4. **DIRH** pin — Enable the smart pin
5. **WYPIN** y, pin — Write Y / data (after enable)

**Common Modes:** (**[OE]** = an output mode, so OR in `P_OE`)

- **[OE]** **UART TX**: `P_ASYNC_TX` — Serial transmit
- **UART RX**: `P_ASYNC_RX` — Serial receive
- **[OE]** **PWM**: `P_PWM_SAWTOOTH` — Sawtooth wave output
- **[OE]** **PWM**: `P_PWM_TRIANGLE` — Triangle wave output
- **ADC**: `P_ADC` — Analog input
- **Quadrature**: `P_QUADRATURE` — Encoder
- **[OE]** **NCO**: `P_NCO_FREQ` — Frequency output

**Data Flow:**

- **WYPIN** = Write data TO smart pin
- **RDPIN** = Read data FROM smart pin (clears IN)
- **TESTP** = Check if IN flag set

**Golden Rule:** **DIRL** before **WRPIN** · **WXPIN** before **DIRH** · **WYPIN** (data) after **DIRH** · `P_OE` on *every* output mode

**The silent failure:** every output mode (NCO, PWM, pulse, transition, serial TX, DAC, USB) needs `P_OE`. Without it the smart pin runs perfectly and drives nothing, and it still assembles clean. If a mode is supposed to make a pin *do* something and the pin is dead, suspect `P_OE` first. Receive and measuring modes (RX, ADC, quadrature, the counters) don't take it.
:::

## Your Turn

::: your-turn
**Exercise 1: PWM LED Dimmer**

Create a PWM output that dims an LED:

1. Configure a pin for PWM sawtooth mode — it's an output, so don't forget `| P_OE`
2. Set a 1 kHz period (at 160 MHz that's 160,000 clocks—too big for the 16-bit base-period field, so split it: base period = 1000, frame = 160)
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

**Going Deeper:** This chapter covered the smart pin essentials - the configuration pattern and common modes. For complete coverage of all 32 modes, timing diagrams, and advanced techniques, see the dedicated "P2 Smart Pins Manual."

## What We've Learned

Smart pin essentials:

- ✅ Every pin contains its own state machine (32 modes available)
- ✅ The universal recipe: **DIRL** → **WRPIN** → **WXPIN** → **DIRH** → **WYPIN**
- ✅ The IN flag signals "something happened" (mode-specific)
- ✅ UART, PWM, ADC, quadrature — same configuration pattern
- ✅ smart pins free the cog for other work

## Coming Up Next

Chapter 15 explores the event system — how to stop polling and start waiting, so your cog sleeps until something interesting happens. The companion to smart pins: when one tells the other a byte is ready, you want to be notified, not spinning.


**Have Fun!** And remember — every smart pin you configure is a coprocessor you don't have to babysit. That's leverage!


# Chapter 15: Event-Driven Programming

*Stop spinning, start waiting*

## The Hook: No More Polling Loops

Remember all those busy loops waiting for things to happen?

```pasm2
' OLD WAY: Spin waiting for serial data (burns cog cycles!)
wait_rx testp   #RX_PIN wc      ' Check over and over
  if_nc jmp     #wait_rx        ' Spin spin spin...
        rdpin   data, #RX_PIN

' NEW WAY: Sleep until data arrives (zero cog cycles!)
        setse1  #%001<<6 + RX_PIN  ' Wake on IN rise
        waitse1                     ' Sleep until event
        rdpin   data, #RX_PIN
```

The event system lets your cog sleep while waiting. When the event happens, it wakes up instantly. No cycles wasted, and you respond the moment something happens.

## Why Events Matter

Polling loops have two problems:

1. **They waste cycles** - The cog spins doing nothing useful
2. **They add latency** - You check periodically, so there's delay between "thing happened" and "you noticed"

The event system solves both. Your cog *sleeps* and *wakes the instant* something happens. It's like having a personal assistant tap your shoulder instead of constantly looking up to check.

## The Four Selectable Events

Let's meet the cast. Every cog has four configurable event channels: SE1, SE2, SE3, and SE4. Each can be configured to trigger on different conditions:

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
| %000 | LUT read/write & hub-lock events (not a pin event) |
| %001 | IN rises (smart pin ready) |
| %010 | IN falls |
| %011 | IN changes |
| %100 | Pin is low (level) |
| %101 | Pin is low (level) |
| %110 | Pin is high (level) |
| %111 | Pin is high (level) |

### EVENT_* Constants: When You Need Interrupts

While dedicated cogs are usually better than interrupts (see Chapter 11), sometimes you need them. The **SETINT1/2/3** instructions select which event triggers an interrupt using these constants:

| Constant | Value | Description |
|----------|-------|-------------|
| `EVENT_INT` | %0000 | In SETINT this value turns the interrupt *off*; as a POLL/WAIT event it means an interrupt occurred |
| `EVENT_CT1` | %0001 | CT reaches/passes CT1 (timer 1 target) |
| `EVENT_CT2` | %0010 | CT reaches/passes CT2 (timer 2 target) |
| `EVENT_CT3` | %0011 | CT reaches/passes CT3 (timer 3 target) |
| `EVENT_SE1` | %0100 | Selectable event 1 triggered |
| `EVENT_SE2` | %0101 | Selectable event 2 triggered |
| `EVENT_SE3` | %0110 | Selectable event 3 triggered |
| `EVENT_SE4` | %0111 | Selectable event 4 triggered |
| `EVENT_PAT` | %1000 | SETPAT pattern detected |
| `EVENT_FBW` | %1001 | Hub FIFO wrapped around |
| `EVENT_XMT` | %1010 | Streamer needs data |
| `EVENT_XFI` | %1011 | Streamer operation complete |
| `EVENT_XRO` | %1100 | NCO frequency counter rolled |
| `EVENT_XRL` | %1101 | Streamer read last LUT location ($1FF) |
| `EVENT_ATN` | %1110 | Another cog signaled attention |
| `EVENT_QMT` | %1111 | GETQX/GETQY read with no CORDIC result available |

**Using EVENT_* with SETINT:**

```pasm2
' Enable INT1 when SE1 event occurs
        setse1  #%001<<6 + RX_PIN       ' SE1 = IN rise on RX_PIN
        setint1 #EVENT_SE1              ' INT1 fires when SE1 triggers

' Enable INT2 on timer match
        addct2  target, ##200_000       ' Set timer 2 target
        setint2 #EVENT_CT2              ' INT2 fires when CT = CT2

' Enable INT3 when another cog signals
        setint3 #EVENT_ATN              ' INT3 fires on COGATN
```

**Pro tip**: These `EVENT_*` constants are only for **SETINT1/2/3**. The **WAITSE1..4**/**POLLSE1..4** instructions are dedicated per-channel opcodes that take no event-number operand—you configure their trigger with the SETSE mode bits (the table above this one) and then just wait or poll the matching channel.

### Smart Pin Events

The most common use is waiting for a smart pin to have data:

```pasm2
' Wait for smart pin on pin 15 to be ready
        setse1  #%001<<6 + 15   ' IN rise on pin 15
        waitse1                  ' Sleep until ready
        rdpin   data, #15        ' Get the data
```

### Pin Edge Events

You can also wait for raw pin edges (without smart pin):

```pasm2
' Wait for rising edge on pin 5
        setse1  #%001<<6 + 5    ' Rising edge on pin 5
        waitse1                  ' Sleep until edge
        ' Edge detected!

' Wait for falling edge on pin 10
        setse2  #%010<<6 + 10   ' Falling edge on pin 10
        waitse2
        ' Edge detected!
```

## Timer Events

For precise timing, use the counter comparison events:

```pasm2
' Wait exactly 1 millisecond (at 200 MHz)
        getct   target          ' Current time
        add     target, ##200_000  ' +1ms at 200MHz
        addct1  target, #0      ' Set CT1 target
        waitct1                  ' Sleep until CT >= CT1

' Alternative using WAITX (simpler but less precise)
        waitx   ##200_000       ' Wait ~1ms at 200MHz
```

The timer events are:

- **ADDCT1/ADDCT2/ADDCT3**: Set the comparison target
- **WAITCT1/WAITCT2/WAITCT3**: Wait until CT reaches target
- **POLLCT1/POLLCT2/POLLCT3**: Check (non-blocking) if target reached

## Waiting vs Polling

Two ways to use events:

### WAIT - Sleep Until Event

```pasm2
        waitse1                 ' cog sleeps here
        ' Wakes instantly when event occurs
```

- Cog sleeps, uses no cycles
- Wakes immediately when event fires
- Can't do anything else while waiting

### POLL - Check and Continue

```pasm2
        pollse1 wc              ' Check event, clear if set
  if_c  jmp     #event_handler  ' Handle if occurred
        ' Continue with other work...
```

- Cog keeps running
- Checks event flag, clears it
- Returns result in C flag
- Good for servicing multiple events

## Multiple Events

With four SE channels, you can monitor multiple sources:

```pasm2
' Setup multiple events
        setse1  #%001<<6 + RX_PIN     ' Serial data ready
        setse2  #%001<<6 + BUTTON_PIN ' Button pressed (rising edge)
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

## Practical Examples

Time to put events to work. Three patterns you'll reach for again and again:

### Timeout with Fallback

```pasm2
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
        neg     data, #1        ' Return error (-1)
        ret
```

### Debounced Button Press

```pasm2
' Wait for clean button press with debounce
debounced_button
        setse1  #%001<<6 + BUTTON  ' Rising edge
        waitse1                     ' Wait for press

        waitx   ##2_000_000        ' 10ms debounce at 200MHz

        testp   #BUTTON wc         ' Verify still pressed
  if_nc jmp     #debounced_button  ' Bounce - try again
        ret                         ' Clean press!
```

### Precise Periodic Sampling

```pasm2
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

## ATN - Inter-Cog Events

The ATN (attention) system lets cogs signal each other:

```pasm2
' cog 0: Signal another cog
        cogatn  #%0000_0010     ' Send ATN to cog 1

' cog 1: Wait for attention
        waitatn                  ' Sleep until ATN received
        ' Another cog signaled us!
```

The **COGATN** instruction takes a 16-bit mask in D[15:0] where each bit corresponds to a cog (cogs 0..15). Setting bit N sends attention to Cog N.

## Common Gotchas

**❌ WRONG: Forgetting to clear event flag**

```antipattern
' WRONG - event firing during 'other stuff' makes wait return at once
        setse1  #%001<<6 + PIN
        ' ... do other stuff ...
        waitse1                 ' May return immediately!
```

**✓ RIGHT: Clear right before you wait**

```pasm2
' RIGHT - SETSE1 already clears SE1, so re-clear just BEFORE the wait
        setse1  #%001<<6 + PIN
        ' ... do other stuff (an event may arrive during this) ...
        pollse1                 ' Discard any event caught during the work
        waitse1                 ' Now wait cleanly for the next one
```

**❌ WRONG: Using WAIT when you need to handle multiple sources**

```antipattern
' WRONG - Can only wait for one event at a time
        waitse1                 ' Stuck here until SE1
        ' SE2 might fire and be missed!
```

**✓ RIGHT: Use POLL loop for multiple events**

```pasm2
' RIGHT - Check all sources
.loop   pollse1 wc
  if_c  call    #handle_se1
        pollse2 wc
  if_c  call    #handle_se2
        jmp     #.loop
```

## Medicine Cabinet

::: medicine-cabinet
**Event System Quick Reference**

**Configure Events:**

```pasm2
        SETSE1/2/3/4  #%MMM_PPPPPP    ' Mode and pin
```

**Event Modes:**

| %MMM | Trigger |
|------|---------|
| %001 | IN rises (smart pin ready) |
| %010 | IN falls |
| %011 | IN changes |
| %10x | Pin is low (level) |
| %11x | Pin is high (level) |

**Wait (blocking):**

```pasm2
        WAITSE1/2/3/4    ' Sleep until event
        WAITCT1/2/3      ' Sleep until timer
        WAITATN          ' Sleep until attention
```

**Poll (non-blocking):**

```pasm2
        POLLSE1/2/3/4 WC ' Check event, clear flag, C=occurred
        POLLCT1/2/3 WC   ' Check timer, C=reached
        POLLATN WC       ' Check attention, C=received
```

**Timer Setup:**

```pasm2
        ADDCT1/2/3 target, #delta   ' Set comparison target
```

**Inter-cog:**

```pasm2
        COGATN #mask    ' Signal cogs (bit per cog)
```
:::

## Your Turn

::: your-turn
**Exercise 1: Event-Driven Serial**

Rewrite a serial receive loop to use events instead of polling:

1. Configure SE1 for UART RX smart pin ready

2. Use **WAITSE1** instead of **TESTP** loop

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

## What We've Learned

The event toolkit you now command:

- ✅ Four selectable event channels (SE1-SE4) per cog
- ✅ Three timer events (CT1-CT3) for precise scheduling
- ✅ **WAIT** (sleep) vs **POLL** (check-and-continue) tradeoffs
- ✅ The ATN inter-cog signaling system
- ✅ Common patterns: timeout-with-fallback, debounce, periodic sampling

## Coming Up Next

Chapter 16 brings the whole journey together — orchestrating eight cogs in parallel harmony to build complete systems. It's where the P2 philosophy really shines.


**Have Fun!** And remember — every spin loop you replace with **WAITSE** is cog cycles you've handed back to your design. Be generous with events!


# Chapter 16: Multi-Cog Orchestration

*Bringing it all together in parallel harmony*

## The Hook: A Complete System in 8 Cogs

Watch this system architecture come alive:

```pasm2
' Main orchestrator (cog 0)
main_orchestrator
        ' Launch the orchestra (SETQ sets PTRA for new cog)
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

Eight independent processors, each with a specific job, all working in perfect coordination. This is the true power of P2!

## Communication Patterns

Eight processors running in parallel sounds wonderful — until you realize they need to talk to each other. Let's meet the three patterns you'll use 95% of the time.

### The Mailbox Pattern

The simplest and most common — a single hub long that one cog writes and another reads:

```pasm2
' Producer cog
producer
        ' Generate data
        call    #calculate_result
        wrlong  result, ##MAILBOX_ADDR
        
' Consumer cog
consumer
        rdlong  data, ##MAILBOX_ADDR wz
   if_z jmp     #consumer              ' Wait for data
        wrlong  #0, ##MAILBOX_ADDR     ' Clear mailbox
        call    #process_data
```

### The Ring Buffer Pattern

For streaming data between cogs:

```pasm2
' Writer cog
writer_cog
        rdlong  wr_ptr, ##WRITE_PTR
        wrlong  data, wr_ptr
        add     wr_ptr, #4
        and     wr_ptr, ##BUFFER_MASK  ' Wrap around
        wrlong  wr_ptr, ##WRITE_PTR
        
' Reader cog  
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

### The Command Queue Pattern

For sending commands between cogs:

```pasm2
' Command structure in hub
' +0: Command ID
' +4: Parameter 1
' +8: Parameter 2
' +12: Result/Status

' Commander cog
send_command
        wrlong  cmd_id, ##CMD_BUFFER+0
        wrlong  param1, ##CMD_BUFFER+4
        wrlong  param2, ##CMD_BUFFER+8
        wrlong  ##$FFFF, ##CMD_BUFFER+12  ' Mark as pending
        
wait_complete
        rdlong  status, ##CMD_BUFFER+12
        cmp     status, ##$FFFF wz
   if_z jmp     #wait_complete
        
' Worker cog
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

## Synchronization Techniques

Sometimes communication isn't enough — you need two or more cogs to *agree* on what happens when. That's where synchronization comes in.

### Using Locks

When multiple cogs need atomic access to the same piece of data, P2 gives you 16 hardware locks. They're tiny and they're fast:

```pasm2
' Atomic increment using lock
atomic_increment
        locktry #COUNTER_LOCK wc      ' C=1 if we got the lock
  if_nc jmp     #atomic_increment     ' Retry until we get it
        
        rdlong  value, ##COUNTER
        add     value, #1
        wrlong  value, ##COUNTER
        
        lockrel #COUNTER_LOCK
```

### Event Synchronization

Cogs waiting for specific events:

```pasm2
' cog 1: Signal event
        wrlong  ##EVENT_FLAG, ##EVENT_ADDR
        
' cog 2: Wait for event
wait_event
        rdlong  flag, ##EVENT_ADDR wz
   if_z jmp     #wait_event
        wrlong  #0, ##EVENT_ADDR      ' Clear event
```

## Real-World Example: Robot Controller

Let's build a complete robot control system:

```pasm2
' cog 0: Main Controller
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

' cog 1: Ultrasonic Sensor
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

' cog 2: Left Motor Driver
left_motor_cog
        rdlong  speed, ##LEFT_MOTOR wz
   if_z jmp     #left_motor_cog      ' No speed set
        
        ' Generate motor control signals
        ' ... PWM generation code
        jmp     #left_motor_cog

' cog 3: Right Motor Driver
' (Similar to left motor)

' cog 4: Serial Communications
serial_cog
        ' Check for incoming commands
        testp   #RX_PIN wc
  if_nc jmp     #serial_cog
        
        call    #receive_byte
        ' Build command...
        wrlong  command, ##SERIAL_COMMAND
        jmp     #serial_cog

' cog 5: LED Status Display
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

' cog 6: Safety Monitor
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

' cog 7: Debug Output
debug_cog
        ' Output system state for debugging
        ' ... debug code
```

Eight cogs, each doing one job perfectly, creating a responsive, reliable robot!

## Your Turn: Multi-Cog Project

::: your-turn
**Exercise: Traffic Light Controller**

Requirements:

- Cog 0: Main sequencer
- Cog 1: North-South lights
- Cog 2: East-West lights  
- Cog 3: Pedestrian button watcher
- Cog 4: Timer/scheduler

Starting structure:

```pasm2
        org     0
' cog 0: Main sequencer
        ' Launch other cogs
        ' Coordinate light changes
        ' Handle pedestrian requests
        
' Your implementation here
```

Goal: Working traffic light with pedestrian crossing
Hint: Use mailboxes for cog communication
Success Check: Lights change correctly, pedestrian button works
:::

::: medicine-cabinet
Multi-cog systems overwhelming? Start simple:

**Start with just 2 cogs:**

```pasm2
' Main + Helper pattern
main    setq    @params                 ' PTRA for new cog
        coginit #1, @helper
        ' Main work

helper  ' Support work
```

**Use simple mailboxes:**

```pasm2
' Fixed hub addresses for communication
MAILBOX_1 = $1000
MAILBOX_2 = $1004
```

**Debug one cog at a time:**
Test each cog in isolation before combining!
:::

## Design Principles for Multi-Cog Systems

The hardware gives you eight processors. Whether your *design* survives the journey is up to you. A few rules of thumb we've learned the hard way:

1. **Single Responsibility**: Each cog does ONE thing well
2. **Loose Coupling**: Cogs communicate through hub, not direct dependencies
3. **Clear Ownership**: Each piece of data has one writer
4. **Predictable Timing**: Real-time tasks get dedicated cogs
5. **Graceful Degradation**: System continues if one cog fails

## Common Multi-Cog Gotchas

Before you pull your hair out wondering why the eight-cog dream turned into a debugging nightmare, skim these:

1. **Two cogs touching the same pin** - This is the one that will get you, so it goes first. DIR and OUT bits from every cog are OR'd together before they reach the pin, and a smart pin OR's the cog buses the same way. Two cogs driving one pin don't take turns — their outputs combine. If more than one cog must configure or read the same smart pin, be sure they do it at *different times*, or you'll clobber each other's bus data. (One happy exception: any number of cogs can read a smart pin at once with **RQPIN**, which stays off that shared bus entirely.) And don't reach for a lock here — a lock protects shared *data*; it can't un-corrupt a half-finished transaction. Give each bus or device one owning cog, and let the others talk to *that cog*.
2. **Race conditions** - Use locks for shared write access
3. **Deadlocks** - Avoid circular dependencies
4. **Starvation** - Ensure all cogs get resources
5. **Communication overhead** - Don't over-communicate
6. **Debugging complexity** - Use LED indicators for each cog

## What We've Learned

You've mastered multi-cog orchestration:

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
3. **Explore other manuals** - smart pins, Video, I/O await
4. **Push boundaries** - P2 can do things we haven't imagined yet

## Chapter Summary

:::chapterend
**Congratulations!** You've mastered multi-cog orchestration!

You now understand:

- How to coordinate 8 parallel processors
- Communication patterns between cogs
- Synchronization techniques
- Real-world system design

**You did it!** You're now fluent in PASM2 and ready to build incredible parallel systems!
:::


**Have Fun!** 

Remember what you've learned:

- Eight cogs working together are more powerful than any interrupt-driven system
- Parallel processing isn't harder, it's different
- The P2 way is about determinism and elegance
- Every complex system is just simple parts working together

Now go forth and create something amazing with your Propeller 2!


## Epilogue: The Journey Forward

Well, here we are at the end... or should I say, at the beginning?

You've traveled from blinking your first LED to orchestrating eight parallel processors. You've mastered CORDIC mathematics, tamed the FIFO, and learned why interrupts are usually the wrong answer. That's quite a journey!

But here's the secret: everything you've learned is just the foundation. The P2 community continues to discover new techniques, new optimizations, new ways to use this remarkable chip. Every project pushes the boundaries a little further.

### What Makes You Different Now

You're not just another embedded programmer anymore. You think in parallel. You see solutions that others miss. When someone starts sketching an interrupt scheme to keep one job on time, you reach for a different move first - give that job a cog of its own, and let it simply run.

### The Community Awaits

The Parallax forums are filled with fellow travelers on this journey. Share your projects. Ask questions. Help newcomers. The community that inspired this manual continues to grow because people like you contribute back.

### One Last Story

I remember my first P2 project. I was trying to control 16 servos with perfect timing while reading sensors and communicating over serial. On my previous microcontroller, it was a nightmare of interrupts and jitter.

On the P2? Three cogs. Clean, simple, perfect timing. That's when I truly understood - this isn't just a different processor, it's a different philosophy of computing.

### Your Challenge

Build something that wouldn't be possible without parallel processing. Something that would be a nightmare of interrupts on other processors. Then share it with the world.

Show them what eight cogs can do.

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

**The P2 Architect's Guide**
: Where this manual taught you to write PASM2, that one teaches you how to decide what goes in which cog — how to derive a design from the physical facts of your project rather than guess at one. The natural next book if you have finished here and are staring at a blank page wondering how to carve up your own system.


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
| **RP2350** (Pico 2) | ARM Cortex-M33 or RISC-V | 2 | Fixed, plus **PIO** | Cores cached; PIO deterministic |
| **P2 Propeller** | Custom | **8** | **Any pin** | **Deterministic** |

The RP2350 deserves a closer look than the others, because its **PIO** blocks are the nearest thing to the P2's approach: small programmable state machines that drive pins on their own schedule, independent of the cores. If you have written PIO programs, you already understand why offloading pin timing to dedicated hardware changes what a small chip can do. The difference is what the helper *is*: a PIO state machine is a specialised resource with its own small, restricted instruction set, while a P2 cog is a full processor running the same language as the rest of your program.

There is a second difference, and Raspberry Pi's own datasheet is candid about it: past two UARTs, two SPIs and two I²Cs, the flexible path *is* PIO — twelve state machines in three blocks, where the four machines in a block share a single 32-slot instruction memory between them. That shared 32 slots is the wall PIO users actually run into, and it is not a wall the P2 has: the smart-pin hardware sits at all 64 pins independently, and each cog carries its own 2KB of program space.

## What Makes P2 Different

### Eight Real Processors, Not Time-Slicing

On ARM, ESP32, or PIC, you typically have 1-2 cores that share time between tasks using interrupts or an RTOS. The P2 gives you eight complete, identical processors that run truly in parallel.

**Traditional approach:**

```antipattern
' Everyone fights for the same CPU
ISR(TIMER1_vect) { motor_control(); }   ' Might delay...
ISR(UART_RX_vect) { serial_handler(); } ' ...this
main() { while(1) { sensor_loop(); } }  ' Hope we get time
```

**P2 approach:**

```multicog
' Each task owns its own processor
COG0: coginit(1, @motor_control)   ' Coordinator launches workers
COG1: motor_control()              ' Dedicated - always on time
COG2: serial_handler()             ' Dedicated - never misses byte
COG3: sensor_loop()                ' Dedicated - consistent sample
COG4-7: ready for more
```

No interrupt priority juggling. No RTOS configuration. Each task owns its processor.

### Smart Pins: Peripherals on Every Pin

Traditional MCUs have fixed peripheral assignments: UART1 is on PA9/PA10, SPI1 is on PB3/PB4/PB5, and if you need those pins for something else, you're stuck rerouting your PCB.

On P2, every pin contains a programmable state machine. Any pin can become a UART, SPI, PWM, ADC, quadrature decoder, or 27 other modes. The peripheral comes to your pin, not the other way around.

### Deterministic Timing

ARM MCUs with cache have unpredictable timing. A memory read might take 1 cycle (cache hit) or 50+ cycles (cache miss). Even instruction timing varies—ARM instructions take 1-3+ cycles depending on the operation. This makes cycle-accurate timing extremely difficult.

P2 takes a different approach: most cog-register ALU and logic instructions execute in exactly **2 clock cycles**. For straight-line register code you can estimate the time by counting instructions and multiplying by 2. The multi-cycle instructions—hub reads/writes (9+ clocks, variable), taken branches (a pipeline flush), CORDIC result reads, and WAITx—cost more, so "instructions × 2" is a lower bound for real sequences, not an exact figure. Hub memory still uses round-robin access that gives every cog predictable, guaranteed access slots, so your timing loops behave identically every time—no cache luck required.

## Coming From ARM/STM32

You're used to configuring HAL structures, writing interrupt handlers, and managing DMA. Here's how P2 solves those problems:

| Instead of... | On P2... | The Benefit |
|---------------|----------|-------------|
| `HAL_UART_Transmit()` | Configure smart pin once, then **WYPIN** bytes | Pin handles all timing autonomously |
| `HAL_TIM_PWM_Start()` | Configure smart pin once, update with **WYPIN** | Pin runs independently—your cog is free |
| NVIC priority configuration | Nothing needed | All cogs equal, no priority inversion ever |
| `HAL_DMA_Start()` | Use built-in FIFO/Streamer | Simpler API, integrated into each cog |
| `arm_sin_f32()` library | **QROTATE** instruction | Hardware trig in ~55 clocks |
| FreeRTOS `xTaskCreate()` | **COGINIT** | True parallel execution, not scheduled |

**The result**: Deterministic timing, zero interrupt conflicts, and I/O configuration that just works.

## Coming From ESP32

You're used to WiFi/Bluetooth convenience and FreeRTOS abstractions. P2 takes a different approach:

| ESP32 Way | P2 Way | The Benefit |
|-----------|--------|-------------|
| Built-in WiFi/BT | Add WizNet or ESP module | You choose your connectivity—or skip it entirely |
| `xTaskCreate()` | **COGINIT** | Not scheduled—truly parallel, guaranteed timing |
| GPIO matrix routing | smart pins | 32 modes per pin, far more capability |
| FreeRTOS timing | Deterministic hub | Cycle-accurate timing guaranteed |
| Arduino framework | Spin2/PASM2 | Deeper control, deeper understanding |

**The result**: 8 real cores running simultaneously, timing you can count on, and no more shuffling functions around to find pins that support them.

## Coming From Arduino/AVR

You'll find P2 familiar but dramatically more powerful:

| Arduino Way | P2 Way | The Upgrade |
|-------------|--------|-------------|
| `digitalWrite()` | **DRVH/DRVL** or smart pins | Similar syntax, vastly more capability |
| `delay()` blocks everything | **WAITX** or dedicated cog | Timing without blocking other tasks |
| One thing at a time | 8 things truly parallel | Real concurrency, not fake multitasking |
| 8-bit math limits | 32-bit + hardware CORDIC | No more overflow worries, hardware trig |
| Libraries for everything | Growing ecosystem + OBEX | More control, deeper understanding |

**The result**: Graduate from 8-bit limitations to 8 parallel 32-bit processors with hardware math and smart pins on every I/O.

## When P2 Is the Right Choice

P2 excels when you need:

- **Multiple real-time tasks** running simultaneously without conflicts
- **Precise timing** that cache misses and interrupts can't disrupt
- **Video or audio generation** requiring cycle-accurate output
- **Flexible I/O** where any pin can become any peripheral
- **Hardware math** for motor control, signal processing, or robotics
- **Multiple motor/servo control** with dedicated cogs per channel
- **Protocol implementation** where smart pins handle timing autonomously

## Platform Trade-offs

Every platform makes trade-offs. P2 optimizes for **determinism, parallelism, and flexibility** rather than:

| If you need... | P2's answer |
|----------------|-------------|
| Built-in WiFi/Bluetooth | Add WizNet or ESP module—you choose connectivity |
| Massive library ecosystem | Growing OBEX + helpful community |
| Ultra-low-power sleep | External modules or different platform |
| Lowest unit cost at 100K+ volumes | P2 targets flexibility over commodity pricing |

## The Software Axis

The table above compares silicon. For most people choosing a platform, the decision is not made there — it is made on language, libraries, and tools. This is where the P2 is weakest, and you should hear it plainly before you commit a project to it.

**You will learn two new languages.** Spin2 and PASM2 are specific to this chip. There is no Arduino core, no ESP-IDF, no CircuitPython image that makes your existing habits transfer. What you know from other platforms will help you think, but you will be typing unfamiliar code from day one.

**The library situation is not comparable.** For an ESP32 or a Pico, a sensor you buy today almost certainly has a driver written, packaged, and installable in one line, along with a dozen tutorials. On the P2 you check OBEX, and if it is not there you write it from the datasheet. That is a real difference in project hours, and on a deadline it can be the whole decision.

**The tooling is smaller.** One compiler family rather than a dozen, and a community of thousands rather than millions. When you hit something strange, the answer is often not already on the internet — you ask on the forum, or you work it out.

**It costs more.** A Pico 2 is pocket change; a P2 Edge module and a breakout board is a different order of purchase, and at production volumes the gap does not close — the P2 is not competing for the commodity socket. (Parallax publishes current pricing; treat any figure quoted in a book as out of date.)

None of that is a reason not to use the P2. It is the price of admission, and you should know what it is before you pay it rather than discover it in week three.

## What You Are Buying With That

The argument for the P2 is not that it is faster or cheaper, because it is often neither. It is about what happens to a design as it grows.

Put eight jobs on one processor and they are sharing it, so the eighth one changes the timing of the seven that were already there. Every handler you add reopens everybody else's timing budget, and the arrangement that worked last month has to be checked again. Give each job its own cog and that simply stops being true — adding the eighth cog does not disturb the first seven, because they were never sharing anything to disturb.

That is not a claim that the P2 is quicker; you have the timing tables above and they say what they say. It is a claim about what stays true when the design changes. On anything that runs longer than a weekend, that turns out to be the property you wanted.

If your project is "connect to WiFi and display data," an ESP32 does that with less effort, and you should use one. Where the P2 earns its place is the design with several jobs that each have to keep their own time, and a pin count that will not stop growing.

## Community Resources

While P2's ecosystem is smaller than ARM or Arduino, it's active and welcoming:

**Parallax Forums** - The heart of the P2 community. Chip Gracey (P2's designer) participates actively, answering questions and discussing design decisions. You'll find help from experienced developers who've solved problems you haven't encountered yet.

**P2 Object Exchange (OBEX)** - A library of reusable Spin2 and PASM2 objects covering drivers, protocols, display interfaces, and more. Before writing something from scratch, check OBEX—someone may have already done the work.

**Community Support** - Unlike large platforms where your question disappears in a sea of posts, the P2 community is small enough that questions get noticed and answered. Many community members have decades of Propeller experience.

Coming from Arduino's library-for-everything culture, you will write more code yourself. Budget for that — it is real hours, and nothing below makes them go away.

What it does change is the *kind* of hours. On a conventional part, a library is code you call from your own thread of control, so you inherit its blocking, its interrupt usage, its timing — and two libraries that each want the same timer, or each disable interrupts at the wrong moment, will fight. Debugging that means debugging somebody else's code inside your own timing budget, and it is some of the most miserable work in embedded. Here, the thing you reuse takes a cog and some pins and hands you a mailbox. It is not sharing your processor, so that particular fight does not start. And the driver you do write is usually smaller than the one you would have imported, because the smart pin is already handling the bit-level timing that would otherwise be most of the code.

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

P2 represents a fundamentally different approach to embedded computing—one that changes which problems you spend your time on:

- **Eight processors** means your motor control never delays your serial handler
- **64 smart pins** means no function is ever stuck waiting for the one pin that supports it
- **Deterministic timing** means your code works the same way every time
- **Hardware CORDIC** means real-time math without floating-point libraries

Engineers who've fought interrupt priority inversions, missed timing deadlines, and PCB rework due to peripheral conflicts find P2 refreshing. You spend your time solving your actual problem, not fighting your MCU.

**Welcome to the P2 community.** You've got 8 processors, 64 smart pins, and a community that's been building amazing things since the original Propeller. Time to see what you can build.


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
- Cog anatomy: Ch2
- Cog communication: Ch2, Ch16
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
- Multi-cog: Ch16

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
- Q register: Ch7
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
- Smart pins: Ch8, Ch14
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
