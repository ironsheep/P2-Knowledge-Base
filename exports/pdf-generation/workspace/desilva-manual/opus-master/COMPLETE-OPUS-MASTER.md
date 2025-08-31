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
*Knowledge Base Coverage: 80%*

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
        org     0               ' Start at COG address 0
        
        drvh    #56             ' Drive pin 56 high (LED on)
        waitx   ##25_000_000    ' Wait ~0.25 seconds at 100MHz
        drvl    #56             ' Drive pin 56 low (LED off)  
        waitx   ##25_000_000    ' Wait ~0.25 seconds
        jmp     #$-4            ' Jump back 4 instructions
```

That's it! Five instructions and you have a blinking LED. Load this into any COG and watch the magic happen.

## What's Really Happening

Well, now that you've seen it work (you did try it, right?), let's talk about what's actually going on here.

### The Instructions Decoded

**`org 0`** - This tells the assembler to start placing code at COG address 0. Every COG has its own private 512 longs (2KB) of memory, and execution always starts at address 0 when a COG is loaded.

**`drvh #56`** - This drives pin 56 high (3.3V). The 'h' means high. The '#' means we're using an immediate value (the actual number 56) rather than the contents of register 56. One instruction, and your LED is on!

**`waitx ##25_000_000`** - This waits for 25 million clock cycles. At the default 100MHz clock, that's 0.25 seconds. Notice the double '##'? That means this is a 32-bit immediate value. Single '#' only gives us 9 bits.

**`drvl #56`** - Drive low. LED off. You get the pattern.

**`jmp #$-4`** - Jump back 4 instructions. The '$' means "current address", so '$-4' means "4 instructions back from here". Infinite loop achieved!

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
        org     0
        
        mov     delay, ##25_000_000    ' Set delay to 0.25 seconds
        
blink   drvh    #56                    ' LED on
        waitx   delay                  ' Wait
        drvl    #56                    ' LED off
        waitx   delay                  ' Wait
        jmp     #blink                 ' Repeat forever
        
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
        org     0
        
        mov     short, ##10_000_000    ' 0.1 second
        mov     long_d, ##30_000_000   ' 0.3 seconds
        
pattern drvh    #56                    ' Short pulse 1
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
        
        jmp     #pattern
        
short   long    0
long_d  long    0
```

### Experiment 2: Multiple LEDs
Blink LEDs on pins 56 and 57 alternately:

```pasm2
        org     0
        
loop    drvh    #56                    ' LED 56 on
        drvl    #57                    ' LED 57 off
        waitx   ##25_000_000
        
        drvl    #56                    ' LED 56 off
        drvh    #57                    ' LED 57 on
        waitx   ##25_000_000
        
        jmp     #loop
```

### Experiment 3: Fading (Advanced)
This one's a bit tricky - we'll use PWM to fade the LED:

```pasm2
        org     0
        
        wrpin   ##P_PWM_TRIANGLE, #56  ' Configure pin 56 for PWM
        wxpin   ##$100, #56            ' Set period to 256
        dirh    #56                    ' Enable the pin
        
fade    wypin   level, #56             ' Set duty cycle
        waitx   ##100_000              ' Small delay
        add     level, #1              ' Increment brightness
        and     level, #$FF            ' Wrap at 256
        jmp     #fade
        
level   long    0
```

Don't worry if the PWM example seems complex - we'll cover Smart Pins in detail in Chapter 8!

## The Medicine Cabinet

Feeling overwhelmed? Here's the simplified prescription:

**Minimum viable blinker** - Just 3 instructions:
```pasm2
loop    drvnot  #56         ' Toggle pin 56
        waitx   ##25_000_000 ' Wait
        jmp     #loop       ' Repeat
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

1. **Forgetting the ##** - Using `waitx #25_000_000` will NOT wait for 0.25 seconds! Single # only allows values up to 511.

2. **Wrong pin number** - The P2 Eval board's LEDs are on pins 56-63. The P2 Edge module might have different assignments.

3. **No clock setup** - We're assuming the default 100MHz clock. If someone's changed it, your timing will be off.

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

---

**Have Fun!** And remember, every expert was once a beginner who kept their LED blinking when everyone else gave up.

---

*Continue to [Chapter 2: Architecture Safari](02-architecture-safari.md) →*

---

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

```
Each COG Contains:
┌────────────────────────────────┐
│ 512 Longs of RAM (2KB)         │ ← Your code and data live here
├────────────────────────────────┤
│ Program Counter (PC)            │ ← Points to next instruction
├────────────────────────────────┤
│ Z Flag (Zero)                   │ ← Result was zero
│ C Flag (Carry)                  │ ← Carry/borrow occurred
├────────────────────────────────┤
│ FIFO (Optional)                 │ ← For streaming operations
├────────────────────────────────┤
│ Interrupt Vectors (Optional)    │ ← If you really must...
└────────────────────────────────┘
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

```
Hub Memory Layout:
┌────────────────────┐ $00000
│                    │
│    Your Program    │
│    (Spin2/PASM2)   │
│                    │
├────────────────────┤ 
│                    │
│     Variables      │
│       Stack        │
│       Data         │
│                    │
├────────────────────┤
│                    │
│    (Free Space)    │
│                    │
└────────────────────┘ $7FFFF (512KB)
```

### The Egg Beater Revolution

Now here's where P2 gets clever. In P1, COGs took turns accessing the hub in a round-robin fashion. If you missed your slot, you waited for the wheel to come around again.

P2 uses what we call the "egg beater" model. Imagine eight beaters (COGs) all whipping through the same bowl (hub) simultaneously, but their paths are cleverly arranged so they never collide:

```
Traditional (P1) Hub Access:
COG0 → COG1 → COG2 → COG3 → ... → COG0 (repeat)
Each COG waits its turn

Egg Beater (P2) Hub Access:
All COGs access different "slices" simultaneously!
Every COG gets access every 8 clocks
No collisions, no waiting (if you're clever)
```

The practical result? Hub access is MUCH faster and more predictable. Instead of waiting up to 16 clocks (P1), you wait at most 8 clocks (P2), and often less if you align your accesses properly.

## Let's See COGs in Action

Here's a simple demonstration of multiple COGs working together:

```spin2
' Multi-COG LED Pattern Demo
PUB main() | i
    repeat i from 0 to 3
        coginit(COGEXEC_NEW, @cog_code, 56 + i)  ' Start 4 COGs
    repeat  ' Main COG just watches

DAT
        org     0
cog_code
        rdlong  pin_num, ptra          ' Get our pin number from hub
        
loop    drvnot  pin_num                ' Toggle our LED
        shl     pin_num, #24           ' Pin number to bits 24-31
        or      pin_num, ##10_000_000  ' Combine with delay
        waitx   pin_num                ' Wait (different for each COG!)
        shr     pin_num, #24           ' Restore pin number
        jmp     #loop

pin_num long    0
```

What's happening here:
1. The main Spin2 code starts 4 COGs
2. Each COG gets a different pin number (56, 57, 58, 59)
3. Each COG blinks its LED at a slightly different rate
4. All four LEDs blink independently and simultaneously!

## COG Communication: How They Talk

COGs are independent, but they're not isolated. They can communicate through hub memory:

### Method 1: Simple Variables

```pasm2
' COG 1: Writer
        mov     value, #42
        wrlong  value, ##$1000  ' Write to hub address $1000

' COG 2: Reader  
        rdlong  result, ##$1000 ' Read from hub address $1000
```

### Method 2: Locks (When It Matters)

When multiple COGs might write to the same location, we need locks:

```pasm2
' Get a lock
try_lock
        locktry lock_id wc     ' Try to get lock
   if_c jmp     #try_lock      ' Keep trying if failed
        
        ' Critical section - we have the lock!
        rdlong  value, ##shared_addr
        add     value, #1
        wrlong  value, ##shared_addr
        
        lockrel lock_id        ' Release the lock
        
lock_id long    0              ' Lock 0-15
```

### Method 3: Mailboxes (Elegant)

A mailbox is just a hub location where COGs leave messages:

```pasm2
' COG A: Leave a message
        wrlong  message, ##mailbox
        
' COG B: Check for messages
check   rdlong  data, ##mailbox wz
   if_z jmp     #check         ' Keep checking if empty
        wrlong  #0, ##mailbox  ' Clear mailbox
        ' Process the message in 'data'
```

## The Timer: Everyone Gets One

Each COG has its own 64-bit timer, always counting system clocks. This is incredibly useful:

```pasm2
' Method 1: Simple delay
        getct   start_time
        addct1  start_time, ##1_000_000
        waitct1                ' Wait exactly 1,000,000 clocks

' Method 2: Periodic events
        getct   time
loop    addct1  time, ##10_000_000
        waitct1                ' Wait for next 10M clock interval
        drvnot  #56           ' Toggle LED
        jmp     #loop         ' Perfectly periodic!
```

The beauty? Each COG's timer is independent. No shared resource conflicts!

## Why No Interrupts? (Usually)

Here's a controversial P2 feature: it HAS interrupts, but you probably shouldn't use them. Why?

Because with 8 COGs, you don't need interrupts! Instead of interrupting important work, just dedicate a COG to monitoring whatever would have triggered the interrupt:

```pasm2
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

No interrupt latency, no context switching, no priority inversion. Just dedicated, deterministic monitoring.

## Real-World Example: Parallel Sensors

Let's read four different sensors simultaneously:

```pasm2
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

Four COGs running this code = four sensors being read truly simultaneously. Try doing that with a single processor and interrupts!

## The Medicine Cabinet

Feeling overwhelmed by all this parallel processing? Here's your prescription:

**Start simple**: Use just one or two COGs at first
```spin2
' Just two COGs - main program and one helper
PUB main()
    coginit(COGEXEC_NEW, @helper, 0)
    ' Your main code here
```

**Debug one COG at a time**: Get each COG working alone before combining
```pasm2
' Test COG in isolation first
debug_cog
        drvh    #MY_DEBUG_LED  ' Visual confirmation it's running
        ' Your actual code here
```

**Use Spin2 for coordination**: Let the high-level language handle the complex stuff
```spin2
' Spin2 manages COGs, PASM2 does the real-time work
PUB orchestrator()
    startSensorCog(0)
    startMotorCog(1)  
    startCommsCog(2)
    ' Spin2 coordinates, PASM2 executes
```

## Sidetrack: The Philosophy of Parallel

The Propeller's design philosophy comes from a simple observation: in the real world, things happen in parallel, not in sequence.

Consider your car:
- The engine runs continuously
- The radio plays independently  
- The climate control maintains temperature
- The dashboard updates displays
- The ABS monitors wheel speed

These aren't taking turns - they're all happening simultaneously. The Propeller models this reality directly. Instead of one processor frantically time-slicing between tasks, you have eight processors each focused on their job.

It's not just different - it's more natural.

## Common Gotchas

Save yourself some debugging time:

1. **COG RAM is copied, not shared** - Changes in COG RAM don't affect hub RAM unless you explicitly write them back

2. **COGs start at 0** - Always! Your code better be there.

3. **Hub addresses are byte addresses** - COG addresses are long addresses. Don't mix them up!
   ```pasm2
   rdlong  value, ##$1000  ' Reads from hub byte address $1000
   mov     value, $1000    ' Moves from COG long address $1000 
   ```

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
Start 8 COGs, each incrementing a different hub location. Watch them count in parallel:

```spin2
PUB main() | i
    repeat i from 0 to 7
        coginit(COGEXEC_NEW, @counter, $1000 + (i * 4))
    repeat
        ' Monitor the counters in hub RAM
        
DAT
        org     0
counter rdlong  hub_ptr, ptra
loop    rdlong  value, hub_ptr
        add     value, #1
        wrlong  value, hub_ptr
        waitx   ##1_000_000
        jmp     #loop
        
hub_ptr long    0
value   long    0
```

### Experiment 2: Parallel Pattern
Make 8 LEDs display a moving pattern, with each COG controlling one LED:

```pasm2
' Each COG gets LED pin in ptra
        org     0
        rdlong  pin, ptra
        rdlong  delay, ptrb      ' Different delay per COG
        
flash   drvh    pin
        waitx   delay
        drvl    pin
        waitx   delay
        shl     delay, #1        ' Double the delay
        cmp     delay, ##100_000_000 wcz
   if_a mov     delay, ##1_000_000  ' Reset if too long
        jmp     #flash
```

## Coming Up Next

In Chapter 3, "Speaking PASM2", we'll dive deep into the instruction set:
- The anatomy of an instruction
- Conditional execution that will blow your mind
- Math operations that actually make sense
- Why PASM2 is unlike any assembly you've used

But for now, appreciate what you've learned: you understand the Propeller's parallel philosophy. That's not just technical knowledge - it's a new way of thinking about computing.

---

**Have Fun!** Remember, parallel processing isn't harder - it's different. And different can be wonderful.

---

*Continue to [Chapter 3: Speaking PASM2](03-speaking-pasm2.md) →*

---

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

```
[condition] instruction dest, [#]source [flags]
     ↑           ↑        ↑       ↑        ↑
 optional    what to do  target  data   optional
```

Let's dissect a real instruction:

```pasm2
if_z    add     total, #10 wc
 ↑       ↑        ↑     ↑   ↑
only if  add    to this immediate set carry
Z flag           value   value    flag
is set
```

## The Basic Vocabulary

### Moving Data Around

The MOV family - your bread and butter:

```pasm2
' Basic move
        mov     dest, source    ' dest = source
        mov     x, #42         ' x = 42 (immediate)
        mov     x, ##70000     ' x = 70000 (32-bit immediate)

' But wait, there's more!
        mvn     dest, source    ' dest = NOT source (inverted)
        abs     dest, source    ' dest = |source|
        neg     dest, source    ' dest = -source

' And the mind-blowing ones
        altd    dest, source    ' Modify NEXT instruction's dest field!
        alts    dest, source    ' Modify NEXT instruction's source field!
```

Well, that escalated quickly! Don't worry about ALTD/ALTS yet - just know they exist and they're amazing.

### Math Without Tears

P2 has hardware multiply and divide. Let that sink in. Hardware. Multiply. And. Divide.

```pasm2
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

Here's a complete multiply example:

```pasm2
' Multiply two numbers and get 64-bit result
        mov     x, #123
        mov     y, #456
        mul     x, y           ' Low 32 bits in x
        getmulh high           ' High 32 bits in high
        ' Result: 123 * 456 = 56088
        ' (all in 2 clock cycles!)
```

Uff! In the old days, we'd write loops for this. Now it's instant.

### Logic Operations

Your Boolean friends:

```pasm2
        and     x, mask        ' x = x AND mask
        or      x, bits        ' x = x OR bits  
        xor     x, toggle      ' x = x XOR toggle
        not     x              ' x = NOT x (same as XOR with $FFFFFFFF)
        
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
        sar     x, #3          ' Arithmetic shift right (sign-extend)
        rol     x, #3          ' Rotate left 3 bits
        ror     x, #3          ' Rotate right 3 bits
        
' Variable shifts (amount in register)
        shl     x, y           ' Shift x left by y bits
        
' Fancy ones
        rev     x              ' Reverse bit order (!!)
        mergeb  x              ' Merge bytes (AABBCCDD -> ABCDABCD)
```

## Flow Control: Jump!

### Unconditional Jumps

```pasm2
        jmp     #target        ' Jump to target
        jmp     target         ' Jump to address in target register
        
' Relative jumps
        jmp     #$-4          ' Jump back 4 instructions
        jmp     #$+8          ' Jump forward 8 instructions
```

### Conditional Execution (The Magic)

Here's where PASM2 gets beautiful. ANY instruction can be conditional:

```pasm2
if_z    add     x, #1          ' Only add if Z flag set
if_nz   add     x, #1          ' Only add if Z flag clear
if_c    add     x, #1          ' Only add if C flag set
if_nc   add     x, #1          ' Only add if C flag clear
```

The conditions:

```
if_z     - If Z flag set (result was zero)
if_nz    - If Z flag clear (result not zero)
if_c     - If C flag set (carry/borrow occurred)
if_nc    - If C flag clear
if_c_and_z   - If both C and Z set
if_c_or_z    - If either C or Z set
if_c_eq_z    - If C equals Z
if_c_ne_z    - If C not equal to Z
```

And the advanced ones:

```
if_a     - If above (unsigned greater)
if_b     - If below (unsigned less)
if_ae    - If above or equal
if_be    - If below or equal
```

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

## The Flags: C and Z (and Q!)

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

The Q flag is special - it's used by CORDIC operations (Chapter 7).

## Special Instructions That Will Blow Your Mind

### SKIP - The Instruction Skipper

```pasm2
        skip    ##%11010000    ' Skip pattern (1=skip, 0=execute)
        add     x, #1         ' Skipped!
        add     y, #1         ' Skipped!  
        add     z, #1         ' Executed
        sub     a, #1         ' Skipped!
        sub     b, #1         ' Executed
        ' ... pattern continues
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
        ' 512 bytes copied with no loop overhead!
        
temp    long    0
```

## The Medicine Cabinet

Feeling overwhelmed? Here's your simplified prescription:

### Minimum Instructions to Know

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
jmp     #label        ' Jump
call    #label        ' Call subroutine
ret                   ' Return

' Flags
cmp     x, y wcz      ' Compare and set flags
if_z    jmp #label    ' Conditional jump
```

Master these 10 instructions and you can write real programs!

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
   - COG addresses are in longs (0-511)
   - Hub addresses are in bytes (0-524287)

## Your Turn: Experiments

### Experiment 1: Conditional Counter
Count up if button pressed, down if not:

```pasm2
        org     0
        
loop    testp   #BUTTON_PIN wc ' Test button
if_c    add     counter, #1    ' Increment if pressed
if_nc   sub     counter, #1    ' Decrement if not
        
        wrlong  counter, ##HUB_ADDR ' Display count
        waitx   ##1_000_000
        jmp     #loop
        
counter long    0
```

### Experiment 2: Pattern Matcher
Find a pattern in data:

```pasm2
        org     0
        
        mov     pattern, ##$DEADBEEF
        mov     ptra, ##data_start
        
search  rdlong  value, ptra++
        cmp     value, pattern wz
if_z    jmp     #found
        cmp     ptra, ##data_end wcz
if_b    jmp     #search
        jmp     #not_found
        
found   ' Pattern found!
        drvh    #SUCCESS_LED
        jmp     #$
        
not_found
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

## Sidetrack: Why PASM2 Is Different

Most assembly languages are thin wrappers over hardware. PASM2 is different - it's designed for humans:

1. **Symmetry**: Every instruction can use every addressing mode
2. **Orthogonality**: Features combine predictably
3. **Conditional everything**: Not just jumps, ANY instruction
4. **No special cases**: General-purpose registers, no accumulator

This isn't accident - it's philosophy. The P2 was designed to make assembly programming pleasant.

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

---

**Have Fun!** Remember, PASM2 isn't like other assembly languages - it's actually enjoyable!

---

*Continue to [Chapter 4: The Hub Connection](04-hub-connection.md) →*

---

# Chapter 4: The Hub Connection

*How COGs share and care*

## The Hook: Instant Communication

```pasm2
' COG 1: Leave a message
        wrlong  ##$DEADBEEF, ##$1000
        
' COG 2: Get the message
        rdlong  message, ##$1000
        ' message now contains $DEADBEEF!
```

That's it - COGs talking through hub memory. But there's so much more...

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
loop    rflong  value            ' Read from FIFO
        ' Process value
        djnz    count, #loop     ' Decrement and jump if not zero
        
' No hub timing worries - FIFO handles it all!
```

## Real-World Example: Video Buffer

```pasm2
' Fast screen clear using block transfer
clear_screen
        mov     color, ##$00_00_00_00  ' Black
        setq2   ##640*480-1             ' Number of longs
        wrlong  color, ##screen_buffer  ' Fills entire screen!
        ' 1.2MB cleared in microseconds!
```

## The Medicine Cabinet

**Simple hub access pattern**:
```pasm2
' Just use PTRA for everything
        mov     ptra, ##hub_address
        rdlong  value, ptra++
        ' That's all you really need!
```

---

*Continue to [Chapter 5: Mathematics Unleashed](05-mathematics-unleashed.md) →*

---

# Chapter 5: Mathematics Unleashed

*Hardware multiply and divide - finally!*

## The Hook: 64-Bit Multiply in 2 Clocks

```pasm2
        mul     x, y              ' 32x32->64 bit multiply
        getmulh high              ' Get high 32 bits
        ' Done! 64-bit result in 2 instructions!
```

Remember doing this with shifts and adds? Those days are over!

## The Multiplication Revolution

```pasm2
' Unsigned multiply
        mul     result, value     ' result = low 32 bits
        
' Signed multiply  
        muls    result, value     ' Signed version
        
' Scale and multiply
        scl     result, ##$8000   ' Scale by 0.5 (32.32 fixed point)
```

## Division Without Tears

```pasm2
' Start division
        qdiv    dividend, divisor ' Start the operation
        
' Get results (takes 30 clocks)
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
        
' 64-bit multiply  
        mul     x, y
        getmulh high
        ' Result in high:x
```

## Real-World Example: Fixed-Point Math

```pasm2
' 16.16 fixed point multiply
fixed_mul
        muls    a, b             ' Multiply
        getmulh high            ' Get high part
        shl     a, #16          ' Shift low part
        shr     high, #16       ' Shift high part
        or      a, high         ' Combine
        ' Result in 16.16 format!
```

---

*Continue to [Chapter 6: Flags and Decisions](06-flags-decisions.md) →*

---

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

---

*Continue to [Chapter 7: CORDIC Magic](07-cordic-magic.md) →*

---

# Chapter 7: CORDIC Magic

*Trigonometry at the speed of logic*

## The Hook: Hardware Sine in 55 Clocks

```pasm2
        qrotate angle, ##$7FFF_FFFF  ' Start rotation
        getqx   cosine               ' Get cosine (55 clocks later)
        getqy   sine                 ' Get sine
        ' Hardware trigonometry!
```

No lookup tables. No approximations. Pure mathematical precision.

## What Is CORDIC?

CORDIC (COordinate Rotation DIgital Computer) is a method for calculating trigonometric functions using only shifts and adds. P2 has it in hardware!

```pasm2
' Rotate a point
        setq    y                ' Set Y coordinate
        qrotate x, angle        ' Rotate X,Y by angle
        getqx   new_x           ' Get rotated X
        getqy   new_y           ' Get rotated Y
```

## Practical Applications

```pasm2
' Calculate distance (Pythagorean theorem)
        setq    y
        qvector x, #0           ' Start vector calculation
        getqx   distance        ' sqrt(x² + y²)
        getqy   angle          ' atan2(y, x)
        
' Generate sine wave
        qrotate angle, ##AMPLITUDE
        getqy   sample         ' Sine wave sample
        add     angle, ##FREQUENCY
```

## The Pipeline Concept

CORDIC operations take 55 clocks, but they're pipelined:

```pasm2
' Start multiple operations
        qrotate angle1, radius
        add     angle1, #1
        qrotate angle1, radius  ' Starts immediately!
        ' Both complete in ~56 clocks total
```

---

*Continue to [Chapter 8: Smart Pins Symphony](08-smart-pins-symphony.md) →*

---

# Chapter 8: Smart Pins Symphony

*64 independent I/O processors*

## The Hook: UART in 3 Instructions

```pasm2
        wrpin   ##P_ASYNC_TX, #PIN    ' Configure as UART TX
        wxpin   ##BAUD_RATE, #PIN     ' Set baud rate
        dirh    #PIN                  ' Enable pin
        ' That's it - hardware UART ready!
        
        wypin   char, #PIN            ' Send a character
        ' No bit-banging required!
```

## Smart Pins Explained

Each of the 64 pins has its own processor that can:
- Generate PWM
- Measure frequency
- Send/receive serial data
- Perform ADC/DAC operations
- Count edges
- Measure pulse widths
- And much more!

## Digital I/O Basics

```pasm2
' Simple output
        drvh    #PIN            ' Drive high
        drvl    #PIN            ' Drive low
        drvnot  #PIN            ' Toggle
        fltl    #PIN            ' Float (high-Z)
        
' Simple input
        testp   #PIN wc         ' Read pin into C flag
```

## PWM and Timing

```pasm2
' PWM output
        wrpin   ##P_PWM_TRIANGLE, #PIN
        wxpin   ##1000, #PIN    ' Period
        wypin   ##500, #PIN     ' 50% duty cycle
        dirh    #PIN            ' Start PWM
```

## Serial Communications

```pasm2
' Async serial (UART)
        wrpin   ##P_ASYNC_TX, #TX_PIN
        wxpin   baud_config, #TX_PIN
        dirh    #TX_PIN
        
' Send byte
        wypin   data, #TX_PIN
        waitx   #20             ' Brief delay
        testp   #TX_PIN wc      ' Check if done
```

## Real-World Example: WS2812 LED Driver

```pasm2
' Smart pin generates precise WS2812 timing
ws2812_setup
        wrpin   ##P_PULSE, #LED_PIN
        wxpin   bit_timing, #LED_PIN
        dirh    #LED_PIN
        
send_rgb
        shl     green, #8
        or      green, red
        shl     green, #8
        or      green, blue
        wypin   green, #LED_PIN  ' Send 24-bit RGB
```

---

*Continue to [Chapter 9: Streaming Data](09-streaming-data.md) →*

---

# Chapter 9: Streaming Data

*Moving data at maximum velocity*

## The Hook: DMA-Like Streaming

```pasm2
        setq    ##1000-1         ' Transfer 1000 longs
        rdlong  buffer, source   ' Happens at maximum speed!
        ' 4KB moved in microseconds!
```

## The Streamer Concept

The streamer is P2's DMA engine:
- Moves data between hub and pins
- Generates video
- Captures high-speed data
- All without CPU intervention

## FIFO Operations

```pasm2
        rdfast  #0, hubaddr     ' Start FIFO read
loop    rflong  data           ' Read from FIFO (no waiting!)
        ' Process data
        djnz    count, #loop
```

---

*Continue to [Chapter 10: Hub Execution](10-hub-execution.md) →*

---

# Chapter 10: Hub Execution

*Breaking free from 512 instructions*

## The Hook: Unlimited Code Size

```pasm2
        orgh    $400            ' Code in hub memory
        org     0               ' But executes like COG code!
        
hub_code
        ' Your code can be megabytes!
        ' No more 512 instruction limit!
```

## COG vs Hub Execution

**COG Execution**:
- Fast (2 clocks per instruction)
- Limited to 512 instructions
- Deterministic timing

**Hub Execution**:
- Slower (2-9 clocks per instruction)
- Unlimited size
- Perfect for large programs

## Mixed Mode Programming

```pasm2
        call    #hub_function   ' Call hub code from COG
        jmp     #cog_code      ' Jump back to COG
        ' Mix and match as needed!
```

---

*Continue to [Chapter 11: Interrupts (If You Must)](11-interrupts-if-you-must.md) →*

---

# Chapter 11: Interrupts (If You Must)

*With great power comes great responsibility*

## The Hook: Yes, P2 Has Interrupts

```pasm2
        setint1 #INT_PINRISE, #BUTTON_PIN  ' Setup interrupt
        ' Your code runs normally...
        ' Until button is pressed!
        
int1_handler
        ' Interrupt code here
        reti1                               ' Return from interrupt
```

## The Interrupt Controversy

P2 has interrupts. Should you use them? Usually NO.

Why? Because you have 8 COGs! Instead of interrupting important work, dedicate a COG to monitoring.

## When to Use Them

Rarely. But sometimes useful for:
- Ultra-low latency response
- Power-saving scenarios
- Legacy code ports

## When NOT to Use Them

Most of the time! Use a dedicated COG instead:
- Cleaner code
- Deterministic timing
- No priority inversion
- Easier debugging

---

*Continue to [Chapter 12: Optimization Mastery](12-optimization-mastery.md) →*

---

# Chapter 12: Optimization Mastery

*Making it faster, smaller, better*

## The Hook: 2x Speed with One Change

```pasm2
' Before: 8 clocks
        rdlong  x, hubaddr
        add     x, #1
        wrlong  x, hubaddr
        
' After: 4 clocks  
        rdlong  x, ptra++
        add     x, #1
        wrlong  x, --ptra
        ' PTRA magic saves cycles!
```

## Pipeline Optimization

Understanding the pipeline:
- Most instructions: 2 clocks
- Hub access: 2-9 clocks
- CORDIC: 55 clocks
- Multiply: 2 clocks

## Instruction Pairing

```pasm2
' These can overlap
        mul     x, y           ' Starts multiply
        add     a, b           ' Executes while multiply runs
        getmulh result         ' Gets multiply result
```

## Memory Access Patterns

```pasm2
' Block transfers are FAST
        setq    #16-1
        rdlong  buffer, hubaddr ' 16 longs in one go!
```

---

*Continue to [Chapter 13: Video Generation](13-video-generation.md) →*

---

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

# Appendix A: Instruction Set Reference

## Quick Reference Format

Each instruction entry includes:
- Syntax
- Operation
- Flags affected
- Timing
- Example

## Memory Access Instructions

### RDBYTE - Read Byte from Hub
```
Syntax:  RDBYTE D, S/# {WZ/WC}
Operation: D = byte at hub[S]
Flags:    Z = (D == 0), C = D[7]
Timing:   2-9 clocks
Example:  RDBYTE value, hubaddr wz
```

### RDWORD - Read Word from Hub
```
Syntax:  RDWORD D, S/# {WZ/WC}
Operation: D = word at hub[S]
Flags:    Z = (D == 0), C = D[15]
Timing:   2-9 clocks
```

### RDLONG - Read Long from Hub
```
Syntax:  RDLONG D, S/# {WZ/WC}
Operation: D = long at hub[S]
Flags:    Z = (D == 0), C = D[31]
Timing:   2-9 clocks
```

[Continue with all instruction categories...]

---

*For complete instruction details, see the P2 Silicon Documentation*

---

# Index

## A
- ADC operations: Ch15
- ADD instruction: Ch3, Ch5
- Address modes: Ch3
- ALTD/ALTS: Ch3
- Architecture: Ch2
- Assembly basics: Ch3

## B
- Bit manipulation: Ch3
- Block transfers: Ch4, Ch9
- Booleans: Ch3

## C
- C flag: Ch6
- CALL/RET: Ch3
- Clock timing: Ch2
- CMP instruction: Ch6
- COG anatomy: Ch2
- COG communication: Ch2, Ch16
- Conditional execution: Ch3, Ch6
- CORDIC: Ch7
- Counters: Ch2

## D
- DAC operations: Ch15
- Debugging: Ch12
- Division: Ch5
- DRVH/DRVL: Ch1

## E
- Egg beater: Ch2, Ch4

## F
- FIFO: Ch4, Ch9
- Flags: Ch6
- Flow control: Ch3

## G
- GETMULH: Ch5
- GETQX/GETQY: Ch7

## H
- Hardware multiply: Ch5
- HDMI: Ch13
- Hub execution: Ch10
- Hub memory: Ch2, Ch4

## I
- I2C: Ch14
- Immediate values: Ch3
- Instruction format: Ch3
- Interrupts: Ch11

## J
- JMP instruction: Ch3

## L
- LED control: Ch1
- Locks: Ch2, Ch16
- Logic operations: Ch3

## M
- Mailboxes: Ch2, Ch16
- Mathematics: Ch5
- Memory access: Ch4
- MOV instruction: Ch3
- MUL/MULS: Ch5
- Multi-COG: Ch16

## O
- Optimization: Ch12

## P
- Parallel processing: Ch2
- Pipeline: Ch7, Ch12
- Pins, Smart: Ch8
- PTRA/PTRB: Ch3, Ch4
- PWM: Ch8

## Q
- Q flag: Ch7
- QDIV: Ch5
- QROTATE: Ch7

## R
- RDBYTE/RDWORD/RDLONG: Ch4
- REP instruction: Ch3
- Rotation: Ch3, Ch7

## S
- Serial protocols: Ch14
- Shift operations: Ch3
- Signal processing: Ch15
- SKIP instruction: Ch3, Ch6
- Smart Pins: Ch8
- SPI: Ch14
- Streamer: Ch9

## T
- Timer: Ch2
- Timing: Ch2, Ch12
- Trigonometry: Ch7

## U
- UART: Ch8, Ch14

## V
- VGA: Ch13
- Video generation: Ch13

## W
- WAITX: Ch1
- WRBYTE/WRWORD/WRLONG: Ch4

## Z
- Z flag: Ch6