<!--
================================================================================
THE P2 ARCHITECT'S GUIDE — BODY (single-file, per DD3)

This file is the canonical body source. It is assembled AFTER front-matter.md by
assemble-manual.sh into P2-Architect-Guide.md for PDF Forge.

SCAFFOLD STATE (task #93): headings + authoring contracts only. Chapters and back
matter are authored by the sprint tasks below — each section heading carries the
task that fills it and its golden sources. Do NOT author content during scaffold;
this skeleton exists so assemble-manual.sh has real structure to assemble and the
template stack can be round-tripped.

  Ch1  "Meet the Propeller 2"                  → task #94 (plan §3)
  Ch2  "Putting It to Work"                    → task #95 (plan §4)
  Ch3  "Thinking in P2 (Functional Decomp.)"  → task #96 (plan §5)
  Appendix A / B, Glossary, Where-to-Next      → task #97 (plan §6)

CONVENTIONS (fixed at scaffold; front matter §98 documents them):
  - "P1 note:" migration sidebars use a fenced div:   ::: p1note  …  :::
    (mapped by filters/p2kb-architect-local.lua → P1NoteBlock; DD1)
  - Code is fenced ```spin2 / ```pasm2 and pnut_ts-verified (never code-divisions)
  - Figures are deferred (DD5): mark intended locations as
    > **[Figure — <description>]**  and log them to PUNCH-LIST.md
================================================================================
-->

# Meet the Propeller 2

By the end of this chapter you'll be able to picture the whole chip — eight
processors, one shared pool of memory, and a ring of clever pins around the
outside — and you'll know roughly what each part is for. That picture is all you
need before we start writing code. We're not going to be exhaustive here; each part
has a deep manual of its own, and we'll point you to it as we go. The goal right
now is just to make the Propeller 2 feel familiar.

If you've worked with a microcontroller before, the most useful thing to know up
front is where the P2 sits. A conventional microcontroller does one thing at a time,
very fast: a single instruction stream racing down a single core, and when you need
it to juggle several jobs at once, you lean on interrupts and a scheduler to slice
that one core into time-shared pieces. At the other extreme, an FPGA is *all*
hardware *all at once* — you describe logic and it becomes physical circuitry, with
no instruction stream at all. The P2 lives in the gap between those two landmarks.
It is still software — you write programs, the way you always have — but instead of
one core to time-share, you get **eight** real processors that genuinely run at the
same time, plus dozens of small hardware helpers around the edges that do their jobs
on their own. You rarely have to choose between "fast single thread" and "dedicated
hardware." On the P2 you usually just hand each job its own piece of silicon.

That idea — *give each job its own piece of silicon, and let it keep running* — is
the thread that runs through this whole guide. Let's meet the pieces.

> **[Figure — the whole chip at a glance: eight COGs around a central hub, with the
> ring of 64 smart pins on the outside. Logged for the visual pass (PUNCH-LIST).]**

## Eight COGs — eight little computers

The heart of the P2 is its eight processors. Each one is called a **COG**, and the
P2 community treats a COG as *the computer* — when a P2 programmer says "put that on
its own COG," they mean "give that job its own processor." All eight are identical
32-bit processors, numbered 0 through 7, and they all run at the same time, at full
speed, without getting in each other's way.

This is the part that surprises people coming from a normal microcontroller. There
is no scheduler handing out time slices, no context-switching, no operating system
quietly deciding who runs next. Each COG just keeps running its own program,
independently, from start to finish. One COG can sit in a tight control loop forever
while another talks to a sensor and a third drives a display — and none of them slows
the others down. Because nothing interrupts a COG from the outside, its timing is
*deterministic*: the same code takes exactly the same number of clock cycles every
time it runs. That predictability is why the P2 is so good at jobs where timing has
to be exact, like generating video or driving a motor.

Each COG has a little private memory of its own to hold its program and data, a fast
hardware path for calls and returns, and even its own dedicated streaming engine for
moving data at high speed (we'll get to that one shortly). You start a COG running
with a single instruction and stop it with another; a stopped COG simply powers down
until you need it again.

💡 **Tip:** The mental shift that makes the P2 click is to stop thinking "one
program that does everything" and start thinking "several small programs, each
minding one job, running side by side." Almost every P2 design is some version of
that.

::: p1note
**P1 note — same as P1:** If you're coming from the Propeller 1, this part will feel
like home: the P2 keeps the same eight-COG, shared-hub family architecture that
defined the original Propeller. Eight symmetric processors, no interrupts required,
deterministic timing — all still true. What changed is *how much* each COG can do,
which the rest of this chapter is about.
:::

For the assembly-level execution details — the instruction pipeline, how a COG
fetches and runs code, starting and stopping COGs from PASM2 — see Part I of the
*P2 Assembly Language Manual*.

## Memory — three tiers, from tiny-and-fast to big-and-shared

A COG works with memory at three levels, and it's worth knowing them apart because
the trade-off between them shapes a lot of P2 code.

Closest and fastest is each COG's **private register RAM** — 512 longs (2 KB) that
belong to that COG alone. It's small on purpose: it sits right next to the
processor, so access is immediate. Right beside it is a second private block, the
**lookup RAM** (the "LUT") — another 512 longs you can use for data, waveforms, or
extra code. These two are private, quick, and limited.

Then there's the **hub** — 512 KB of RAM shared by all eight COGs. This is the big
common pool: where your larger programs live, where COGs leave data for each other,
where buffers and tables sit. It's far roomier than the private memories, with the
trade-off that it's shared, so reaching it involves a brief, predictable wait for
your turn (more on that next).

> **[Figure — the three memory tiers: private COG RAM and LUT beside each processor,
> the shared hub in the middle. Logged for the visual pass.]**

::: p1note
**P1 note — changed in P2:** The shape is familiar — private COG RAM plus a shared
hub — but the sizes are transformed. The P1 had 32 KB of hub; the P2 has **512 KB**.
The 512-long COG register space is the same size you know, but the P2 *adds* the
512-long LUT alongside it, which the P1 didn't have at all — and adjacent COGs can
even share their LUTs for fast hand-offs.
:::

### How COGs share the hub — the "egg beater"

Because all eight COGs share one hub, something has to decide who gets access when.
On the P2 that "something" is a round-robin hardware mechanism nicknamed the **egg
beater**, and the nice thing about it is that it's completely predictable. Each COG
is guaranteed its own access slot on a fixed rotation, so a hub read or write never
fails and never stalls unpredictably — at worst you wait a few clocks for your slot
to come around. And once you're streaming a block of data, it flows at a rate of one
long per clock. There's no bus contention to reason about and no priority fights;
the hardware simply takes turns, forever, on schedule.

This is the one place where a COG's timing depends on the others, and even here it's
bounded and knowable rather than random — which is exactly what you want when you're
counting cycles.

::: p1note
**P1 note — changed in P2:** The P1 also shared its hub by strict rotation, so the
take-turns idea is familiar. The P2's egg beater refines it: the rotation is tighter,
and block transfers move a long every clock once you're synced, so the shared memory
keeps up with high-speed work in a way the P1's hub couldn't.
:::

Memory addressing, alignment, and the details of hub timing are covered in the
*P2 Assembly Language Manual* (Part I) and the *Silicon Doc*.

## Pins and smart pins — I/O that thinks for itself

Around the outside of the chip are **64 I/O pins**, numbered P0 through P63. Any COG
can read or drive any pin, so pins aren't owned by a particular processor — they're a
shared resource, and you decide by convention which COG looks after which pin.

What makes the P2's pins special is that each one is a **smart pin**: a small, self-
contained piece of hardware built into the pin itself. You configure a smart pin for
a job — measure a pulse, count edges, output a PWM signal, run a serial protocol, do
analog-to-digital or digital-to-analog conversion — and then it just *does that job
on its own*, without your COG babysitting it. Your COG sets it up once, and
afterward only steps in to hand it new data or read back a result.

This is a genuinely different way to do I/O. On most microcontrollers, holding a
serial line or measuring a signal precisely means a core has to stay busy doing it.
On the P2 you push that work out to the edge of the chip and free the COG entirely.
The guiding habit is: **before you write code to bit-bang a protocol, check whether a
smart pin already does it in hardware** — usually one does.

There are many smart-pin modes — enough to cover the common serial, timing,
counting, and analog jobs — and rather than list them here, we'll send you to the
deep reference. The *I/O & Smart Pins User Guide* (the "Blue Book") walks through
every mode with examples; this guide just wants you to know the pins are smart and to
reach for them first.

::: p1note
**P1 note — new in P2:** This one has no P1 analog. The P1 had 32 plain
general-purpose pins; the P2 has 64, and every one of them is a smart pin. If you
spent P1 projects dedicating a COG to bit-bang a UART or a PWM, that work largely
moves into the pin hardware on the P2.
:::

## The CORDIC solver — shared math hardware

The P2 has a piece of dedicated math hardware called the **CORDIC solver**, shared by
all eight COGs. You hand it a number — or a pair of numbers, or an angle — and it
hands back results that would otherwise cost you a lot of code: full 32-bit
multiply and divide, square roots, sines and cosines, vector rotations,
logarithms and exponentials.

It's *pipelined*, which means it works like an assembly line: you can feed it a
steady stream of problems and it keeps producing answers, so several operations from
a COG can be in flight at once. For anything involving real math — signal
processing, coordinate geometry, generating waveforms — the CORDIC turns work that
would be slow in software into something the hardware just does for you.

Here in the orientation we only need you to know it exists and that it's fast and
shared. The complete list of operations and exactly how to invoke them lives in the
*Silicon Doc*.

::: p1note
**P1 note — new in P2:** The P1 had no hardware math engine — it shipped log,
antilog, and sine *tables* in ROM and you did the rest in software. The P2 replaces
that with the CORDIC solver, so the trigonometry and multiply/divide you used to hand-
code are now hardware operations.
:::

## The streamer — moving data at full speed

Each COG also has its own **streamer**: a dedicated engine for moving data between the
hub and the pins (or the analog converters) at the chip's full clock rate, without
the COG having to shuttle each piece by hand. You point it at a block of hub memory
and a destination, start it, and it streams — while your COG goes on to do something
else.

The streamer is how the P2 generates video — VGA, HDMI, and composite signals all
come out of it — and it also handles high-speed audio output, fast data capture, and
some specialized signal-analysis tricks. Anything that needs a *lot* of data to move
*continuously* and *on time* is a job for the streamer.

As with the smart pins, the point right now is just to know it's there. The
*P2 Streamer Programming Guide* is the full reference for setting it up and for the
video, audio, and capture modes.

::: p1note
**P1 note — new in P2:** The P1 generated video with a simpler per-COG video
generator (the old `WAITVID` approach). The P2's streamer is a far more capable,
general-purpose data mover — video is just one of the things it does.
:::

## Events and interrupts — noticing when something happens

Sometimes a COG needs to react to something: a pin changed, a timer reached a count,
the CORDIC finished, the streamer is done. The P2 gives each COG a small **event**
system for exactly this. A COG can watch for a hardware condition and then choose how
to respond — check on it when convenient, pause until it happens, or let it trigger an
**interrupt** that drops into a handler.

What's worth knowing as a newcomer is that on the P2 events are a *convenience, not a
necessity*. Because each COG runs its own program independently, you often don't need
interrupts at all — you can simply dedicate a COG to a job and let it watch in a tight
loop, with perfectly predictable timing. Events and interrupts are there for when
they genuinely simplify a design, not because the chip forces them on you.

::: p1note
**P1 note — new in P2:** The P1 had no interrupts at all — it used the dedicate-a-COG,
poll-in-a-loop model exclusively, and that model still works beautifully on the P2.
The P2 *adds* a real event-and-interrupt system per COG as an option for when you want
it.
:::

The full set of event sources and how interrupts dispatch are documented in the
*P2 Assembly Language Manual* (Part I) and the *Silicon Doc*.

## The clock — one setting, the whole chip

All eight COGs and the hardware around them run from a single system clock, and you
choose its speed. The P2 has two built-in internal oscillators for when you don't
need anything special — a fast one (around 20 MHz) that it starts up on, and a very
slow, low-power one — and for real work you attach a crystal and let the P2's on-chip
PLL multiply it up to the speed you want, comfortably into the hundreds of megahertz.
You set this once, near the top of your program, and the whole chip runs from it.

The practical thing to remember: clock setup is a one-time decision you make up front,
not something you fiddle with as you go. Once the chip is running at your chosen speed,
every COG's deterministic timing is measured against that one clock.

::: p1note
**P1 note — changed in P2:** Same idea as the P1 — one system clock for the whole
chip, set up front — but with far more range. Where the P1 topped out at 80 MHz, the
P2 runs many times faster, well into the hundreds of megahertz.
:::

## Booting — how a program starts running

When the P2 powers up, a small program baked into its **ROM** takes over for the first
few milliseconds. It looks at a few designated pins to decide where your program
should come from — a serial connection from a host, an SPI flash chip, or a microSD
card — loads it, and hands control to COG 0. That ROM also carries a couple of handy
extras: a built-in monitor for poking at a running chip, and even a small Forth
interpreter.

For everyday work you mostly don't think about this — your development tools handle
loading — but it's good to know the path exists and that the pins used for booting
become ordinary I/O once your program is up. The *Silicon Doc* and the boot
documentation cover the boot sources and their fallback behavior in detail.

## Where this leaves us

That's the whole cast: eight independent COGs, three tiers of memory tied together by
a take-turns hub, 64 smart pins doing I/O on their own, a shared CORDIC for math, a
per-COG streamer for high-speed data, an event system for reacting to the world, one
clock to set, and a ROM that boots you. You don't need to remember every detail — you
just need the picture. With it in hand, the next chapter puts these parts to work:
we'll launch a COG, drive a pin, and see how a real P2 program is actually shaped.

# Putting It to Work

Now that you can picture the chip, let's use it. This chapter is about *doing* — by
the end you'll have driven a pin, launched a second COG, shared data between COGs, and
made the one decision every P2 program makes (Spin2 or PASM2?). The point isn't to
teach you the whole language — the reference manuals do that, and we'll point you to
them — it's to make the chip feel like something you can actually program. We'll keep
the examples short, and every one of them compiles.

A note before we start: P2 programs are written in **Spin2**, the P2's high-level
language, and **PASM2**, its assembly language. Even a "pure assembly" program lives
inside a Spin2 file structure. You don't need to know either language in depth to
follow along — the examples are small and commented, and the goal is the *shape* of a
P2 program, not its syntax.

## Your first program: drive a pin

Here is a complete, working P2 program. It blinks an LED.

```spin2
CON
  _clkfreq = 200_000_000        ' system clock: 200 MHz
  LED      = 56                 ' the pin our LED is on

PUB main()
  repeat                        ' do this forever
    pinhigh(LED)                ' LED on
    waitms(250)                 ' wait a quarter second
    pinlow(LED)                 ' LED off
    waitms(250)
```

That's the whole thing. A few things worth noticing, because they're true of every P2
program:

- The `CON` block holds **constants**. `_clkfreq` is the one constant you'll almost
  always set — it tells the chip how fast to run (here, 200 MHz), and everything
  time-related, like `waitms`, is measured against it. Giving the pin a name (`LED`)
  instead of scattering the number `56` through your code is the habit we'll keep.
- Execution starts at the **first `PUB` method** — here, `main`. That's the entry
  point; the chip runs it on COG 0 when your program loads.
- `pinhigh`, `pinlow`, and `waitms` are built-in Spin2 methods. Driving a pin really
  is that direct — name the pin, set it high or low.

💡 **Tip:** You don't load this onto the chip by hand — your development tool
(PropellerTool, *pnut*, or the VS Code extension) compiles it and sends it over. For
now, just read it as "this is what a P2 program looks like."

::: p1note
**P1 note — changed in P2:** Setting the clock is familiar, but simpler and more
flexible on the P2: one `_clkfreq` constant near the top of your program, and the
compiler works out the PLL settings for you. And pin numbers now run 0–63, not 0–31 —
there are twice as many to reach for.
:::

## Adding a second COG

A blinking LED uses one COG and ignores the other seven. The moment that matters is
when you give a job to a COG of its own. You do that with `cogspin` — it takes a
method to run, hands it to an available COG, and that COG starts running it *alongside*
the one you're already on.

```spin2
CON
  _clkfreq = 200_000_000
  LED_A    = 56
  LED_B    = 57

VAR
  long stack[64]                ' work space for the second COG

PUB main() | cog
  cog := cogspin(NEWCOG, blink(LED_A, 250), @stack)   ' hand the job to another COG
  blink(LED_B, 1000)            ' this COG keeps the slower blink for itself

PRI blink(pin, ms)
  repeat
    pintoggle(pin)
    waitms(ms)
```

When this runs, **two COGs are blinking at once** — one COG flips `LED_A` four times a
second, the other flips `LED_B` once a second, and neither one waits on the other.
That's the P2's whole personality in five lines: when you want something to happen in
parallel, you don't reach for a timer interrupt or a scheduler — you hand the job to a
COG and let it run.

Three details that generalize:

- `NEWCOG` means "any free COG" — you usually don't care which one. `cogspin` returns
  the COG number it actually used (or −1 if all eight were busy).
- The new COG needs a little **stack** space in hub to work with; that's the
  `long stack[64]` we hand it with `@stack` (the `@` means "the address of").
- `blink` is written once and used by both COGs. A `PUB` method is the public face of
  your code; a `PRI` method is private to the object. That `PUB`/`PRI` split *is* the
  P2's run-time model in miniature, which we'll come back to.

## Sharing data between COGs

Independent COGs still need to talk. The simplest way is the hub: because hub memory is
shared, a variable that lives there is visible to every COG. One COG writes it, another
reads it — a mailbox.

```spin2
CON
  _clkfreq = 200_000_000
  LED      = 56

VAR
  long stack[64]
  long count                    ' a hub variable — every COG can see it

PUB main()
  cogspin(NEWCOG, ticker(@count), @stack)   ' worker updates count in hub
  repeat
    if count & 1                ' read what the worker left for us
      pinhigh(LED)
    else
      pinlow(LED)

PRI ticker(p)
  repeat
    long[p]++                   ' bump the shared value in hub
    waitms(100)
```

Here one COG does nothing but increment `count` ten times a second, and the other COG
watches `count` and lights the LED on odd values. Neither COG calls the other; they
just agree on a spot in hub memory. Single hub reads and writes are *atomic* — a COG
always sees a whole value, never half-written — so this simple mailbox is safe. When a
hand-off is more than one value, or several COGs might write at once, the P2 gives you
**locks** (the 16 hardware locks from Chapter 1) to guard the exchange. The
*P2 Assembly Language Manual* covers the coordination patterns in depth.

::: p1note
**P1 note — changed in P2:** Sharing through hub variables works just as it did on the
P1, and locks are still how you guard a multi-step exchange. What changed underneath is
the egg-beater hub access from Chapter 1: hand-offs and block transfers move faster and
stay just as predictable.
:::

## Spin2 or PASM2? A decision, not a syntax tour

Every P2 program makes one architectural choice, sometimes many times: should this
piece of work be written in **Spin2** or **PASM2**? It helps to see it as a spectrum of
three options, not a binary.

- **Spin2** is the high-level language: objects, methods, expressions, easy to write
  and to read. It runs as interpreted bytecode, so it's slower than assembly, but your
  program can be large because the bytecodes live in the roomy hub. Reach for Spin2 for
  application logic, coordination, setup, and anything not on a tight timing budget.
- **PASM2** is native assembly: it runs at the deterministic two-clocks-per-instruction
  speed from Chapter 1, with cycle-exact timing. Reach for a dedicated PASM2 COG when a
  job must be fast and precise — a video driver, a bit-banged protocol, a tight control
  loop.
- **Inline PASM2** sits between them: a short burst of assembly dropped right inside a
  Spin2 method, for when you need native speed for a moment without dedicating a whole
  COG to it.

That middle option looks like this — the same toggle, but done with one native
instruction:

```spin2
CON
  _clkfreq = 200_000_000
  LED      = 56

PUB main()
  repeat
    toggleFast(LED)
    waitms(250)

PRI toggleFast(pin)
  org
    drvnot  pin                 ' one native instruction, full speed
  end
```

The `org … end` block is real PASM2 running inside a Spin2 method. You don't need to
read assembly to take the point: the P2 lets you stay in comfortable Spin2 for most of
a program and drop to the metal exactly where it pays off.

The honest guidance is the one most experienced P2 developers converge on: **write the
application in Spin2, and give the time-critical jobs their own PASM2 COGs.** A typical
P2 program uses both, and that's not a compromise — it's the intended shape. For the
full languages, the *Spin2 Language Reference* and the *P2 Assembly Language Manual*
are the deep references; this guide only wants you to know *which* tool fits *which*
job.

## Objects and the run-time model

A P2 program is built from **objects**. An object is a file with its own constants,
variables, and methods; you pull one in with an `OBJ` block and call its methods
through a name:

```
OBJ
  serial : "jm_fullduplexserial"   ' a driver object, by filename

PUB main()
  serial.start(63, 62, 115_200)    ' call one of its methods
```

That's how you use the community's drivers and your own: each object minds its own data
and exposes methods, and your top-level object wires them together. It's the same
mental model as the `PUB`/`PRI` split you've already seen — public methods are the
object's interface, private ones are its internals — scaled up to whole files. The
*Spin2 Language Reference* is the place for the full object model (instances, arrays of
objects, parameter passing).

## How it boots and runs

You've now seen the run model without us naming it. When the P2 powers up, the boot ROM
from Chapter 1 loads your program and starts your **first `PUB` method on COG 0**. From
there, *your* code is in charge: COG 0 runs your top object's `main`, and it launches
whatever other COGs the design needs with `cogspin` (for Spin2) or its assembly cousin
`coginit` (for a dedicated PASM2 COG). There's no operating system underneath deciding
what runs — the COGs you start are the COGs that run, exactly as you arranged them.

That is the entire run-time story: boot loads you, COG 0 starts your `main`, and your
program spreads itself across as many of the eight COGs as it needs.

## Where this leaves us

You can now read and shape a real P2 program: set the clock, drive a pin, launch a COG,
share data through hub, choose Spin2 or PASM2 for a given job, and compose objects. That
is genuinely enough to build things. What it doesn't yet tell you is *how to decide what
goes on which COG* in the first place — how to look at a whole problem and carve it into
the right set of cooperating pieces. That decision is where the P2 rewards a little real
thought, and it's what the final chapter is about.

# Thinking in P2 (Functional Decomposition)

<!-- TASK #96 (plan §5). The EARNED capstone. Formal space-vs-time thesis as the
RATIONALE → the forces → the first-contact procedure → ONE worked derivation.
Warmth STAYS, rigor RISES, glibness → 0. LOAD-BEARING ANTI-PRESCRIPTION PRINCIPLE:
teaches the METHOD of deriving an architecture, NEVER prescribes an outcome. The
robot-dog derivation is a DEMONSTRATION explicitly framed as ONE machine's answer.
SOURCES (golden home — derives, never drifts): deliverables/ai/P2/architecture/
decomposition/ — all 12 entries. Any authoring-time theory improvement lands in the
YAML FIRST, then renders here. Weave ::: p1note sidebars where the new-in-P2 fabric
changes the decomposition. -->

> **[Chapter 3 — authored in task #96.]**

# Appendix A — Computing in Space and Time (Why We Borrow FPGA Language)

<!-- TASK #97 (plan §6). Temporal→spatial spectrum; honest WHAT-TRANSFERS /
WHAT-DOESN'T (coarse-grained, still software, no place-and-route); the
FPGA-terminology table (term · FPGA meaning · P2 mapping · where it's loose).
SOURCE: architecture/decomposition/spatial-computing.yaml.
ANTI-CASE: no sentence implies the P2 IS an FPGA. -->

> **[Appendix A — authored in task #97.]**

# Appendix B — Further Reading on Functional Decomposition

<!-- TASK #97 (plan §6). Two axes — logical (Parnas; Constantine & Yourdon;
Page-Jones) and physical/concurrent (Hoare CSP + transputer/Occam; optional Kung
systolic) — each with a one-line "why it's relevant to P2". Sources cited in
decomposition-method.yaml. EVERY author/title/year VERIFIED before publish; marked
NEEDS-VERIFICATION until checked. -->

> **[Appendix B — authored in task #97.]**

# Glossary

<!-- TASK #97 (plan §6). From decomposition-glossary.yaml; terms match the YAML. -->

> **[Glossary — authored in task #97.]**

# Where to Next

<!-- TASK #97 (plan §6). Map into the reference manuals (Spin2 v55, the PASM2
Manual, Smart Pins & Streamer guides, Debug manual). Every link resolves to a real
manual. -->

> **[Where-to-Next — authored in task #97.]**
