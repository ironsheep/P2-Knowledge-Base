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