# Copyright and License

Copyright © 2025 Parallax Inc.  
All rights reserved.

This manual incorporates knowledge and teaching approaches inspired by:
- **deSilva's P1 Assembly Tutorial** - The foundational pedagogical approach
- **Iron Sheep Productions LLC** - Technical expertise and P2 community contributions
- **The Propeller Community** - Years of collective wisdom

---

## License

This work is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License.

You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made
- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license

---

## Trademarks

Propeller, Propeller 2, P2, Spin, and the Parallax logo are trademarks of Parallax Inc.

---

## Disclaimer

The information in this manual is subject to change without notice. While every effort has been made to ensure accuracy, the authors and publishers assume no responsibility for errors or omissions, or for damages resulting from the use of the information contained herein.

---

*First Edition: August 2025*  
*Manual Version: 1.0.0*  
*Knowledge Base Coverage: 80\textbackslash\{\}\%*

---

# Dedication

---

## To deSilva

*Whose legendary P1 assembly tutorial taught a generation of programmers that assembly language could be approachable, enjoyable, and even fun. Your unique voice—combining technical precision with human warmth—showed us that great documentation teaches not just the mind, but speaks to the spirit of discovery.*

---

## To the Propeller Community

*Who have spent countless hours exploring, documenting, and sharing their knowledge. From the early P1 pioneers to today's P2 innovators, your collective wisdom makes this manual possible.*

---

## To Future Makers

*May you find in these pages the same joy of discovery that we experienced. The Propeller 2 is more than a microcontroller—it's an invitation to think differently about computing. Welcome to the journey.*

---

*"The best way to predict the future is to invent it."*  
— Alan Kay

---

# Acknowledgments

This manual stands on the shoulders of giants. We gratefully acknowledge:

## Primary Contributors

**deSilva** - For creating the gold standard of microcontroller documentation with the P1 Assembly Tutorial. Your pedagogical approach, combining technical depth with human empathy, remains unmatched. This manual attempts to honor your legacy while adapting to the P2's capabilities.

**Iron Sheep Productions LLC (Stephen M Moraco)** - For extensive P2 documentation efforts, community tools, and the vision of creating an AI-optimized knowledge base. Your systematic approach to extracting and organizing P2 knowledge made this comprehensive manual possible.

**Chip Gracey** - Creator of the Propeller architecture. Thank you for giving us a microcontroller that thinks differently and challenges us to do the same.

## Community Contributors

**The Parallax Forums Community** - Your questions, answers, code examples, and endless experimentation have created a living knowledge base that no single author could match.

**Early P2 Adopters** - Who dealt with evolving documentation, changing specifications, and still produced amazing projects that showed us what was possible.

## Technical Reviewers

Special thanks to those who reviewed drafts, tested code examples, and provided invaluable feedback:
- The P2 Documentation Team at Parallax
- Community members who beta-tested examples
- Everyone who reported errors and suggested improvements

## Inspiration

**The MIT AI Lab** - For showing us that technical documentation can have personality

**Donald Knuth** - For proving that programming texts can be literature

**The Demoscene Community** - For pushing hardware beyond its limits and inspiring us to do the same

---

## Production Notes

This manual was created using:
- Knowledge extracted from hundreds of P2 documents, forum posts, and code examples
- AI-assisted content generation trained on deSilva's writing style
- Community validation and real-world testing
- A commitment to making parallel processing accessible to everyone

---

*"If I have seen further, it is by standing on the shoulders of giants."*  
— Isaac Newton

---

Any errors, omissions, or dad jokes that fell flat are entirely the responsibility of the authors, not our distinguished contributors.

---

# Preface: Welcome to the Journey

Well, here we are! You're about to embark on a journey into the heart of the Propeller 2, and I promise you, it's going to be quite different from what you might expect.

## A Different Kind of Processor

The Propeller 2 isn't just another microcontroller. Oh no, it's something far more interesting. Imagine, if you will, eight independent processors (we call them COGs) all working together in perfect harmony, sharing a common memory space, yet each running their own programs at full speed. No interrupts fighting for attention, no complex priority schemes, just eight brains working in parallel.

And if you think this sounds terribly complicated, you're probably right... but here's the secret: it's actually simpler than traditional architectures once you understand the philosophy.

## About This Manual

This manual follows in the footsteps of deSilva's legendary P1 tutorial. What does that mean? It means we're going to:

1. **Start with working code** - You'll be blinking LEDs before you know what hit you
2. **Learn by doing** - Theory is important, but nothing beats hands-on experience
3. **Have some fun** - Yes, assembly language can actually be enjoyable!
4. **Be honest about complexity** - When something is hard, we'll admit it and then show you how to handle it

## Who Is This For?

Are you a complete beginner to assembly language? Welcome! We'll take good care of you.

Are you a grizzled veteran who's been writing assembly since the 6502? Welcome! The P2 will still surprise you.

Are you somewhere in between? Perfect! This is exactly where you want to be.

The only requirement is curiosity and a willingness to think a bit differently about how computers can work.

## How to Use This Manual

### The Fast Track
If you're impatient (and who isn't?), jump straight to Chapter 1. Get that LED blinking. Feel the satisfaction. Then come back here when you're ready for more.

### The Scenic Route  
Read the chapters in order. Each builds on the previous one, and I've hidden little gems of knowledge throughout that will make later chapters easier.

### The Reference Approach
Already know what you're looking for? The table of contents and index are your friends. The appendices contain every instruction, every Smart Pin mode, every CORDIC operation.

## What Makes the P2 Special?

Let me count the ways:
- **8 symmetric COGs** - No master/slave relationships, all COGs are equal
- **64 Smart Pins** - Each pin has its own processor for I/O operations
- **CORDIC engine** - Hardware trigonometry and coordinate transformations
- **Hardware multiply/divide** - Finally! Real math at hardware speed
- **512KB of RAM** - Shared by all COGs with deterministic access timing
- **No interrupts** - Well, actually there are interrupts, but we'll talk about why you probably don't want them

## A Personal Note

I've been writing technical documentation for longer than I care to admit, and I've learned one thing: the best manual is the one that remembers you're human. You'll get frustrated. You'll make mistakes. Your code won't work the first time (or the second, or sometimes even the third).

That's normal. That's learning. And that's why I'll provide plenty of "medicine" along the way - simpler alternatives, working examples, and the occasional bad joke to keep your spirits up.

## The deSilva Spirit

Throughout this manual, you'll encounter the teaching spirit of deSilva. When you see phrases like:
- "Well, ..." - We're about to correct a common assumption
- "Uff!" - We just got through something complex
- "Have Fun!" - We mean it, this stuff is actually enjoyable

These aren't just quirks; they're signals that we remember you're human and we're on this journey together.

## Ready?

Take a deep breath. Pour yourself your favorite beverage. Open your development environment.

Let's make some magic happen with the Propeller 2!

---

*"The Propeller architecture is based on the simple idea that the best way to avoid the complexity of interrupts is to have enough processors that you don't need them."*  
— Chip Gracey, creator of the Propeller

---

**Turn the page, and let's blink that LED!** →

---

# Chapter 1: Your First Spin

*Let's blink an LED and change your life*

## The Hook: Making Light

I know you're absolutely crazy to have your first instruction executed, so let's not waste any time. Here's a complete PASM2 program that blinks an LED on pin 56 (that's the built-in LED on the P2 Eval board):

```pasm2
' LED Blinker - Your first PASM2 program!
        **ORG**     0               ' Start at COG address 0
        
        **DRVH**    #56             ' Drive pin 56 high (LED on)
        **WAITX**   ##25_000_000    ' Wait ~0.25 seconds at 100MHz
        **DRVL**    #56             ' Drive pin 56 low (LED off)  
        **WAITX**   ##25_000_000    ' Wait ~0.25 seconds
        **JMP**     #$-4            ' Jump back 4 instructions
```

That's it! Five instructions and you have a blinking LED. Load this into any COG and watch the magic happen.

## What's Really Happening

Well, now that you've seen it work (you did try it, right?), let's talk about what's actually going on here.

### The Instructions Decoded

**`org 0`** - This tells the assembler to start placing code at COG address 0. Every COG has its own private 512 longs (2KB) of memory, and execution always starts at address 0 when a COG is loaded.

**`drvh \textbackslash\{\}\#56`** - This drives pin 56 high (3.3V). The 'h' means high. The '\textbackslash\{\}\#' means we're using an immediate value (the actual number 56) rather than the contents of register 56. One instruction, and your LED is on!

**`waitx \textbackslash\{\}\#\textbackslash\{\}\#25\textbackslash\{\}\_000\textbackslash\{\}\_000`** - This waits for 25 million clock cycles. At the default 100MHz clock, that's 0.25 seconds. Notice the double '\textbackslash\{\}\#\textbackslash\{\}\#'? That means this is a 32-bit immediate value. Single '\textbackslash\{\}\#' only gives us 9 bits.

**`drvl \textbackslash\{\}\#56`** - Drive low. LED off. You get the pattern.

**`jmp \textbackslash\{\}\#\textbackslash\{\}\$-4`** - Jump back 4 instructions. The '\textbackslash\{\}\$' means "current address", so '\textbackslash\{\}\$-4' means "4 instructions back from here". Infinite loop achieved!

### But Wait, There's More!

"Hold on," you might say, "how does this even get into the COG?"

Ah, excellent question! In the real world, you'd typically launch this from Spin2 (the high-level language) like this:

```spin2
PUB main()
    coginit(COGEXEC_NEW, @blink_code, 0)  ' Start PASM2 in a new COG
    repeat  ' Keep the main COG alive

DAT
    org     0
blink_code
    drvh    #56
    waitx   ##25_000_000
    drvl    #56
    waitx   ##25_000_000
    jmp     #$-4
```

The `coginit` instruction loads your PASM2 code from hub memory into a fresh COG and starts it running. Meanwhile, your Spin2 code keeps running in its own COG. You now have parallel processing!

## Let's Make It Better

The blinker works, but it's a bit rigid, isn't it? What if we want to change the blink rate? Let's use a register:

```pasm2
        **ORG**     0
        
        **MOV**     delay, ##25_000_000    ' Set delay to 0.25 seconds
        
blink   **DRVH**    #56                    ' LED on
        **WAITX**   delay                  ' Wait
        **DRVL**    #56                    ' LED off
        **WAITX**   delay                  ' Wait
        **JMP**     #blink                 ' Repeat forever
        
delay   long    0                      ' Storage for our delay value
```

Uff! Look at that - we're using a register now! The `mov` instruction copies our delay value into a register (which we cleverly named 'delay'). Now we can change the blink rate by modifying just one value.

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

```pasm2
        **ORG**     0
        
        **MOV**     short, ##10_000_000    ' 0.1 second
        **MOV**     long_d, ##30_000_000   ' 0.3 seconds
        
pattern **DRVH**    #56                    ' Short pulse 1
        **WAITX**   short
        **DRVL**    #56
        **WAITX**   short
        
        **DRVH**    #56                    ' Short pulse 2
        **WAITX**   short
        **DRVL**    #56
        **WAITX**   short
        
        **DRVH**    #56                    ' Long pulse
        **WAITX**   long_d
        **DRVL**    #56
        **WAITX**   long_d
        
        **JMP**     #pattern
        
short   long    0
long_d  long    0
```

### Experiment 2: Multiple LEDs
Blink LEDs on pins 56 and 57 alternately:

```pasm2
        **ORG**     0
        
loop    **DRVH**    #56                    ' LED 56 on
        **DRVL**    #57                    ' LED 57 off
        **WAITX**   ##25_000_000
        
        **DRVL**    #56                    ' LED 56 off
        **DRVH**    #57                    ' LED 57 on
        **WAITX**   ##25_000_000
        
        **JMP**     #loop
```

### Experiment 3: Fading (Advanced)
This one's a bit tricky - we'll use PWM to fade the LED:

```pasm2
        **ORG**     0
        
        **WRPIN**   ##P_PWM_TRIANGLE, #56  ' Configure pin 56 for PWM
        **WXPIN**   ##$100, #56            ' Set period to 256
        **DIRH**    #56                    ' Enable the pin
        
fade    **WYPIN**   level, #56             ' Set duty cycle
        **WAITX**   ##100_000              ' Small delay
        **ADD**     level, #1              ' Increment brightness
        **AND**     level, #$FF            ' Wrap at 256
        **JMP**     #fade
        
level   long    0
```

Don't worry if the PWM example seems complex - we'll cover Smart Pins in detail in Chapter 8!

## The Medicine Cabinet

Feeling overwhelmed? Here's the simplified prescription:

**Minimum viable blinker** - Just 3 instructions:
```pasm2
loop    **DRVNOT**  #56         ' Toggle pin 56
        **WAITX**   ##25_000_000 ' Wait
        **JMP**     #loop       ' Repeat
```

The `drvnot` instruction toggles a pin - if it's high, make it low; if it's low, make it high. Sometimes simpler is better!

## Sidetrack: Why Start at Address 0?

You might wonder why COG code always starts at address 0. It's actually quite elegant:

When a COG is started with `coginit`, the hardware:
1. Stops the COG (if it was running)
2. Copies 512 longs from hub to COG memory (addresses 0-511)
3. Starts execution at COG address 0

This means every COG program starts fresh, with a clean slate. No residual state, no confusion. It's like each COG gets a fresh brain transplant every time it starts!

The last 16 longs (addresses 496-511) are special purpose registers (DIRA, OUTA, etc. in P1 terms, though P2 handles these differently). We'll explore these later.

## Common Gotchas

Before we move on, let me save you some debugging time:

1. **Forgetting the \textbackslash\{\}\#\textbackslash\{\}\#** - Using `waitx \textbackslash\{\}\#25\textbackslash\{\}\_000\textbackslash\{\}\_000` will NOT wait for 0.25 seconds! Single \textbackslash\{\}\# only allows values up to 511.

2. **Wrong pin number** - The P2 Eval board's LEDs are on pins 56-63. The P2 Edge module might have different assignments.

3. **No clock setup** - We're assuming the default 100MHz clock. If someone's changed it, your timing will be off.

4. **COG already running** - If you `coginit` to a specific COG that's already running something else, it will be stopped and replaced. Use `COGEXEC\textbackslash\{\}\_NEW` to automatically find a free COG.

## What We've Learned

Let's celebrate what you've accomplished:
- ✅ Written your first PASM2 program
- ✅ Controlled hardware (LED) directly
- ✅ Used immediate values (\textbackslash\{\}\# and \textbackslash\{\}\#\textbackslash\{\}\#)
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

::: chapterend
**Have Fun!** And remember, every expert was once a beginner who kept their LED blinking when everyone else gave up.
:::

*Continue to [Chapter 2: Architecture Safari](02-architecture-safari.md) →*

---

# Chapter 2: Architecture Safari
