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