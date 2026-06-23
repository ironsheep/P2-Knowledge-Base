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

```{=latex}
\screenshotfig[width=0.9\linewidth]{inbox/assets/p2-edge-breakout.png}
```

::: {.figurecaption #fig:p2-edge-board}
A P2 Edge module — the small board carrying the Propeller 2 chip — seated on a P2 Edge Breakout Board. This is the hardware the guide's examples assume. *(Image courtesy of Parallax Inc.)*
:::

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

```{=latex}
\EightCogSimpleDiagram
```

::: {.figurecaption #fig:whole-chip}
Eight independent COGs arranged around the shared hub, taking turns on a fixed rotation — the "egg beater." (The 64 smart pins live on the outside of the chip; we meet them a few pages on.)
:::

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

```{=latex}
\CogHubRelationshipDiagram
```

::: {.figurecaption #fig:memory-tiers}
The memory tiers. Each COG's private RAM and LUT sit right next to the processor (fast, 2-cycle access); the 512 KB hub is shared by all eight (a few cycles' wait via the egg beater).
:::

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
deep reference. The *I/O & Smart Pins User Guide* walks through
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
just need the picture. With it in hand, the next chapter makes sure you can *read* a P2
program — the handful of structural rules that turn Spin2 and PASM2 from a wall of
symbols into something legible — and the chapter after that puts these parts to work:
we'll launch a COG, drive a pin, and see how a real P2 program is actually shaped.

# Reading P2 Code

Chapter 1 gave you the chip. Before we put it to work, let's make sure you can *read* a
P2 program — because the chapters ahead are full of small examples, and they'll only
teach you anything if the code on the page isn't a mystery. If you've never seen Spin2
or PASM2, this chapter is your Rosetta stone: by the end you'll be able to read every
example in this guide. We are deliberately *not* teaching the whole language here — the
reference manuals do that, in depth — we're teaching its **shape**: the small set of
structural rules that, once you know them, make P2 code legible. That's a much smaller
thing to learn, and it's enough to follow along everywhere else.

One orienting fact first: P2 code is written in *two* languages, and you'll see both.
**Spin2** is the high-level language — readable, object-based, where most of a program
lives. **PASM2** is the assembly language — the P2's native instructions, used for the
small, time-critical pieces. Most of what you'll read is Spin2, so we start there; we
meet PASM2 near the end of the chapter. You do not need to *write* either one to read
this guide — you need to recognize their parts.

## A program is an object — six kinds of block

Here's the first and most useful thing to know: **a Spin2 file is an object**, and an
object is built from just six kinds of *block*. Each block begins with a keyword in the
far-left column, and runs until the next such keyword appears. Here is one of each, in a
single skeleton — don't read it for what it *does* yet, just for its *shape*:

```spin2
CON                           ' constants: clock, pins, fixed values
  _clkfreq = 200_000_000
  LED      = 56

OBJ                           ' other objects (files) this one builds on
  serial : "jm_fullduplexserial"

VAR                           ' this object's own variables
  long  count

PUB main()                    ' PUBlic method; first PUB runs
  count := 0

PRI helper(x) : result        ' a PRIvate method — an internal helper
  result := x + 1

DAT                           ' data, tables, and PASM2 code live here
  greeting  byte  "hi", 0
```

That's the whole grammar of a P2 file at the top level. The six blocks:

- **`CON` — constants.** Fixed values with names: the clock speed, pin numbers, sizes.
  A file starts in `CON` mode even before you write the word, so constants can sit at
  the very top.
- **`OBJ` — objects.** The other files this one builds on — drivers, libraries, your own
  code. More on these below.
- **`VAR` — variables.** This object's own data. Every separate instance of the object
  gets its own copy of its `VAR`s.
- **`PUB` — public methods.** The object's *interface* — the methods other code may
  call. **Every program needs at least one**, and the **first `PUB` is where execution
  begins** (the boot ROM from Chapter 1 starts it on COG 0).
- **`PRI` — private methods.** Internal helpers, callable only from inside this object.
- **`DAT` — data.** Tables and fixed data — and, as we'll see, PASM2 code.

You won't always use all six; a small program might be just `CON` and one `PUB`. But
every P2 file you read is some arrangement of these blocks, so spotting the keywords in
the left margin tells you instantly how the file is organized.

One distinction to fix in your mind now, because it trips up nearly everyone at first:
an **object and a COG are not the same thing**. An object is a unit of *code* — a file
you write and compile. A COG (Chapter 1) is a *processor* that runs code. There's no
fixed relationship between the two: the methods of one object might run on a single COG,
be spread across several, or share a COG with other work. *What* runs *where* is a
decision you make — and it's exactly what Chapter 4 is about.

::: p1note
**P1 note — same as P1.** If you wrote Spin on the Propeller 1, this is home: the same
`CON`/`OBJ`/`VAR`/`PUB`/`PRI`/`DAT` block structure, the same "a file is an object,"
the same first-`PUB`-runs rule. Spin2 adds capabilities inside the blocks, but the
skeleton is identical — you can skim this chapter and just note what's new.
:::

## Methods — how the work is organized

A **method** is a named piece of code you can call — the P2's word for a function or
subroutine. You've already seen the shape in the skeleton; here it is named:

```spin2
PUB blink(pin, count) : ok | i
```

Reading left to right: `PUB` (public) or `PRI` (private); the method's **name**; its
**parameters** in parentheses (`pin`, `count` — the values the caller passes in); after
the colon, an optional **return value** (`ok`); and after the bar, optional **local
variables** (`i`) that exist only while the method runs. Most of those parts are
optional — `PUB main()` is a complete, valid header.

You call a method by naming it: `blink(56, 10)`. And here's a point that saves a
beginner real confusion: many things that *look* like built-in keywords are actually
just **method calls** — `pinhigh(LED)`, `waitms(250)`, `cogspin(...)` are all methods
the language provides, called exactly the way you'd call your own. There's no separate
category to memorize; if it has a name and parentheses, it's a method call.

## Indentation is the structure

This is the rule most likely to trip up a newcomer, so we'll say it plainly: **in
Spin2, indentation defines structure.** There are no braces, no `begin`/`end`. A control
statement owns exactly the lines indented beneath it. Look:

```spin2
PUB countdown(n)
  repeat n                    ' indented lines = the loop body
    pinhigh(LED)
    waitms(100)
    pinlow(LED)
  pinhigh(LED)                ' un-indented: runs after the loop
```

The two `pin` calls and the `waitms` are inside the loop because they're indented under
`repeat`; the final `pinhigh` is *not* indented under it, so it runs once after the loop
finishes. The three shapes you'll meet most are `repeat` (loop — forever, a fixed count,
or while a condition holds), `if`/`else` (choose), and `case` (choose among many). In
every one, what's controlled is simply what's indented under it.

## Values, names, and a line you'll see broken

A few small things, and you'll have seen every kind of token the examples use:

- **`:=` assigns; `=` defines a constant.** Inside a method, `count := 0` *puts* the
  value 0 into the variable `count`. Inside `CON`, `LED = 56` *names* the constant 56.
  Different jobs — assign with `:=`, name with `=`.
- **Named constants over bare numbers.** We write `LED` once in `CON` and use the name
  everywhere, rather than scattering `56` through the code. You'll see this habit
  throughout the guide.
- **Number forms.** Underscores group digits for readability (`200_000_000`); `$` marks
  hexadecimal (`$1FF`); `%` marks binary (`%1101`). The underscores are purely cosmetic.
- **`@name` means "the address of" `name`.** Most of the time you pass a variable's
  *value*; sometimes a method needs to reach the variable (or buffer) itself, and you
  hand it the address with `@` — you'll see `@stack`, `@count`, `@"some text"` in the
  examples ahead.
- **A comment** starts with a single quote `'` and runs to the end of the line.
- **`...` continues a line.** A line that ends in three dots `...` continues onto the
  next, as if the break weren't there — and the rest of the line after the `...` is
  ignored, so a comment can sit there. We lean on this in the guide to keep a long
  statement within the page margin, so you'll see it in examples:

```spin2
  x := first_term + second_term + third_term ...   ' continued below
       + fourth_term
```

When you see a trailing `...`, just read on to the next line as one statement.

## Objects — building from other files

Back to `OBJ`, because composing objects is how real P2 programs are built. An `OBJ`
block pulls in *another* Spin2 file and gives it a name; you then call that file's public
methods through the name:

```spin2
OBJ
  serial : "jm_fullduplexserial"    ' the driver file, as "serial"

PUB main()
  serial.start(63, 62, 115_200)     ' call a method through the name
  serial.str(@"hello")
```

`serial` is an *instance* of the driver object; `serial.start(...)` calls the `start`
method inside it. This is exactly how you use the community's drivers and your own code:
each object minds its own data and exposes methods, and a top-level object wires several
together. (The full object model — instances, arrays of objects, parameters — is in the
*Spin2 Language Reference*.)

## The other language: PASM2

Everything so far has been Spin2. The P2's *other* language is **PASM2** — its native
assembly, the actual instructions the COG runs. You reach for it only where timing has
to be exact, but you'll *read* it often, because most drivers have a PASM2 core. So it's
worth being able to recognize its shape too.

A line of PASM2 is much flatter than Spin2 — one instruction per line:

```pasm2
loop    drvnot  #LED              ' toggle the LED pin
        waitx   ##20_000_000      ' wait ~0.1 s at 200 MHz
        jmp     #loop             ' do it again, forever
```

Read a line left to right: an optional **label** in the left column (`loop` — a name for
this spot, so other instructions can jump to it); the **instruction** (`drvnot`,
`waitx`, `jmp`); then its **operands**. A `#` before an operand means "this is an
immediate value" — a literal number or address, not a register; `##` means a *full
32-bit* immediate (needed for big values like `20_000_000`). Two more parts you'll see
but don't need yet: some instructions end in a **flag effect** like `wc` or `wz` (the
instruction updates a status flag), and any instruction can carry a **condition** prefix
like `if_z` (run only when a flag is set). The deep meaning of all of these is the
*P2 Assembly Language Manual*'s job; here, you just need to parse the line.

PASM2 shows up in two places. A whole COG program lives in a **`DAT` block**; and a short
burst can be dropped right inside a Spin2 method between `org` and `end`:

```spin2
PUB toggle(pin)
  org                           ' a little PASM2, inline
    drvnot  pin
  end
```

Either way — and this is the thread back to Chapter 1's boot story — even a program
that's "all assembly" still lives inside a Spin2 file. Spin2 is always the host.

::: p1note
**P1 note — changed in P2.** PASM2 will look familiar to a P1 assembly programmer — the
label · instruction · destination, source · effects shape carries straight over. What's
new is *scale*: far more instructions, the `##` full-width immediate, and richer
conditionals. If you knew PASM1, you read PASM2 on sight; you'll just meet new mnemonics.
:::

## Where this leaves you

You can now read a P2 program. You know a file is an object built from six kinds of
block; that methods are the named pieces of work, and the first `PUB` is where things
start; that indentation — not punctuation — is the structure; how values, names, and the
`...` continuation look on the page; how objects compose through a name; and what a line
of PASM2 is made of. That's the literacy every example in this guide assumes. With it in
hand, the next chapter stops reading and starts *doing* — your first real program, a
second COG, and the choices a P2 program actually makes.

# Putting It to Work

Now that you can picture the chip *and* read its code, let's use it. This chapter is about *doing* — by
the end you'll have driven a pin, launched a second COG, shared data between COGs, and
made the one decision every P2 program makes (Spin2 or PASM2?). The point isn't to
teach you the whole language — the reference manuals do that, and we'll point you to
them — it's to make the chip feel like something you can actually program. We'll keep
the examples short, and every one of them compiles.

You met both of the P2's languages in Chapter 2 — Spin2 and PASM2 — so the examples
below should read cleanly; this chapter is about putting them to work, not parsing
them. Where a program makes a real choice, we'll stop and look at it.

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
  cog := cogspin(NEWCOG, blink(LED_A, 250), @stack)  ' run on another COG
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

The `org ... end` block is real PASM2 running inside a Spin2 method. You don't need to
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

You can already write a P2 program. You can launch a COG, drive a pin, share data
through hub, and choose Spin2 or PASM2 for a given job. That's the hard part of getting
started, and it's behind you. What's left is the part that turns a working program into a
*good* design: looking at a whole problem and deciding what goes on which COG in the first
place — how to carve the machine into the right set of cooperating pieces. You're ready
for that now, and this chapter is about how it's done.

We're going to do something different from the first two chapters. Up to here we've
*described* the chip. Now we're going to *reason* about it. Functional decomposition — the
craft of cutting a system into parts — is a real engineering discipline with decades of
literature behind it, and we're going to treat it that way: carefully, and without
pretending it's easy. The good news is that the P2 makes the reasoning unusually concrete.
On a lot of processors, "how should I structure this?" is a matter of taste. On the P2, as
you'll see, the structure is mostly *derived* — the hardware and the timing hand you most
of the answer, if you know how to ask.

One thing before we start, and it matters enough that it shapes the whole chapter: **there
is no single right answer that this chapter can hand you.** Every machine is different, so
every good decomposition is different. What you can learn — what generalizes — is the
*method* for deriving one. So that's what we'll teach: the forces that do the cutting, the
order to apply them in, and the way to judge the result. Late in the chapter we'll watch
the whole method run on one example machine, start to finish. Read that example to see the
moves, never to copy the answer — your machine will give a different, equally sound shape.

## Computing in space, not just in time

Start with the idea that makes the rest of this chapter worth the effort. It's the one we
quietly planted back in Chapter 1, when we said each COG just keeps running its own job,
independently. Here's where we cash it in.

There are two very different ways a chip can compute. A conventional microcontroller
computes **in time**: one core runs a sequence of instructions, one after another, and the
way it does more is by going faster or by slicing that one core into time-shared pieces.
An FPGA sits at the opposite pole — it computes **in space**: you lay out function as
actual parallel hardware, many things happening physically at once, with no single
instruction stream at all. These aren't just two speeds; they're two fundamentally
different shapes of computation.

The Propeller 2 lives between them, and closer to the spatial side than you might expect.
Its eight independent, deterministic COGs and its sixty-four programmable smart pins form
what's best described as a **coarse-grained spatial fabric**: not the fine-grained sea of
logic gates an FPGA gives you, but a modest number of real, parallel computing elements you
can assign function to, each running its one job continuously. Decomposed well, a P2 design
behaves like spatial hardware — parallel pipelines whose throughput is set by the *rate*
data flows, not by how many instructions any one stage runs. Decomposed badly, the very
same silicon collapses back into a slow sequential machine: one COG doing everything in
turn while the other seven idle.

That sentence is the reason this chapter exists. The whole discipline of P2 decomposition
is, at bottom, the practice of keeping your design on the *spatial* side of that line — of
spreading function across the fabric instead of funnelling it back through a single core
out of habit. Everything that follows is in service of that.

```{=latex}
\SpaceTimeSpectrumDiagram
```

::: {.figurecaption #fig:space-time}
Computing in time vs. in space. A single-core microcontroller runs one instruction stream; an FPGA lays function out as parallel hardware. The Propeller 2 sits between them — a coarse-grained spatial fabric you assign function to.
:::

::: p1note
**P1 note — the idea is old, the room is new.** If you've built P1 designs, you've been
thinking spatially all along: dedicating a COG to a job and letting it run is exactly this
mindset, and the original Propeller pioneered it. What the P2 changes is how *much* fabric
you have to lay function onto. Smart pins can now absorb an entire bit-banged protocol that
used to cost you a whole COG; the CORDIC and the streamer take on work that used to live in
COG code; the hub is sixteen times larger. The instinct transfers intact — you have
far more space to spread into, and more reason to.
:::

The deep treatment of this space-versus-time framing — including an honest account of what
the P2 borrows from FPGA thinking and, just as importantly, what it *doesn't* — is in
Appendix A. Here, the thesis is enough: **the P2 computes in space when you let it, and
decomposition is how you let it.**

## Object shape is derived, not chosen

Here's the central move of the whole chapter, stated plainly: on the P2, the shape of your
object set is not a matter of taste picked from a menu. It is *derived* by reconciling a
small number of physical and architectural forces. Change the buses, the deadlines, or the
data rates, and the correct object set changes with them. A good decomposition is therefore
an *answer to constraints*, not a style choice.

That distinction has a practical payoff. If decompositions were chosen by taste, the most
you could do is collect examples and imitate the nearest one. Because they're derived, you
can learn the forces that do the deriving — and then produce a sound design for a machine
you have never seen before, because you're reasoning from its wiring rather than
pattern-matching to something you saw once. Reasoning from the forces generalizes;
copying an example doesn't.

It helps to separate two things that are easy to blur together. The **objects** you can
build with — a top-level application, a device driver, a semantic driver, a policy layer, a
buffer, a coordinator — are your *vocabulary*: the nouns. The **forces** are the *grammar*:
the rules that decide which nouns to instantiate, how many of each, and where the
boundaries between them fall. A vocabulary list tells you what words exist; only a grammar
tells you how to build a correct sentence you've never spoken before. This chapter is about
the grammar. (The vocabulary — the object archetypes — has its own reference in the
knowledge base; we'll lean on it but not re-list it here.)

### Two axes, co-designed

Classical software decomposition works on a single axis, and it's a purely logical one:
split behavior into modules, and judge the cuts by **cohesion** (do the things inside a
module truly belong together?) and **coupling** (how much has to cross between modules?).
That axis is real and we'll use it — it rests on decades of solid work, which Appendix B
points you to.

The P2 adds a *second* axis, a physical one: **allocation onto a finite, heterogeneous
resource lattice** — eight COGs, sixty-four smart pins, one shared CORDIC, sixteen locks, a
bounded amount of hub bandwidth, adjacent-COG LUT sharing, the streamer. And here is the
insight that makes the P2 special to design for: *that physical axis is not only a
constraint — it's a decomposition tool in its own right.* A COG is the strongest
encapsulation boundary the silicon offers: private memory, deterministic timing, no
interference from its neighbors. A smart pin can *delete an entire software module* by
absorbing its function into hardware. So "where does this boundary go?" and "what hardware
runs it?" are not two questions asked in sequence — they're one decision, made together.

The two axes are co-designed, and they keep each other honest. A boundary chosen on the
logical axis that ignores the lattice gives you an elegant module that can't actually run —
no COG free to host it, or the hub saturated feeding it. A boundary chosen on the physical
axis that ignores cohesion gives you a COG that owns three unrelated jobs and is impossible
to test. You reconcile both. When they genuinely conflict, the resource budget — an
artifact we'll build later in the chapter — is what decides.

### The failure this prevents

It's worth naming the mistake all of this exists to prevent, because it's the natural thing
to do and it looks fine right up until it doesn't. Call it the **flat device list**: every
chip gets a driver, every driver is a sibling reachable from `main()`, and the shape was
chosen by analogy to some example rather than derived from how the hardware is actually
wired. It compiles. It even runs during single-COG bring-up. Then it fails — as
intermittent, timing-dependent, nearly-undebuggable flakiness — the first moment the
derivation it skipped would have forbidden the cut. We'll see exactly how that happens when
we meet Force 1. The cure is to derive the shape instead of guessing it, and that's what the
forces are for.

## The forces that do the cutting

Four forces do the work. Three of them are **primary** — they cut the object set
horizontally, deciding who owns what and how the pieces relate. The fourth is **emergent**:
it falls out vertically, once the first three have drawn the structure. We'll take them one
at a time, and we'll lead each with the *question it asks*, because that question — asked of
your own machine — is the technique you're meant to carry away. The robot dog and the I²C
buses you'll see are illustrations of a force in motion, never a rule to transplant.

A word on emphasis before we start: for each force, the *why* matters more than the *what*.
An engineer who knows why a force exists on the P2 specifically will generalize it to
hardware we never imagined; one who memorizes a rule will eventually meet the case the rule
didn't cover and apply it wrongly. So we'll dwell on the reasons.

### Force 1 — Who owns this wire?

The first force asks a **correctness** question, not a style one. Of the four, it's the only
one that can make your program flatly *wrong* rather than merely inelegant, so it goes first.

The question is: for each serialized, stateful hardware resource — an I²C bus, a one-wire
LED chain, a smart pin in the middle of a transaction — *which single COG owns it?* And the
answer the force insists on is: exactly one. One owner per resource, and the object boundary
traces the **wire**, not your feature list.

The reason is physical, and it comes straight out of the silicon. P2 pin outputs are
OR'd together — there is no hardware referee arbitrating who gets the pin. If two COGs both
drive the same SDA and SCL lines, they don't take polite turns; their outputs combine, and
a bus transaction — which is a multi-step sequence (start, address, acknowledge, data, stop)
that assumes a single agent in charge — is corrupted. This isn't "a race you might lose." A
bus is a stateful protocol, and a stateful protocol with two uncoordinated drivers is
*guaranteed* to break. The chip gives you sixteen locks and atomic single-long hub access to
coordinate shared *data* — but a lock can't un-corrupt a half-issued I²C frame. The clean
coordination is therefore *structural*: make the resource un-shareable by giving it a single
owning object in a single COG. The hardware's lack of a referee is precisely *why* ownership
has to be explicit and singular in your software.

So Force 1 makes the primary cut, and it's usually a COG boundary. Group the devices by
which wire they sit on and what timing that wire has to meet; give each group one owning COG
and one transport object. And notice what decides the *shape* of that transport — it's the
sharing topology, not the protocol. Several devices sharing one bus inside one COG want a
single shared transport with one configuration that the device drivers call into. One device
alone on its own bus wants a self-contained transport with nothing to coordinate. You can end
up with the *same protocol implemented twice with two different state models* — and that's
correct, because how many things share the wire, not which protocol it is, decided the shape.

⚠️ **Watch out:** the flat device list is this force ignored. The moment two COGs touch one
bus, you get silent corruption that presents as flaky hardware — intermittent, timing-
dependent, and miserable to debug from the symptom, because the symptom is three layers away
from the cause. A design that picks its shape from *how many devices exist* rather than *who
shares a wire* has this failure built in from the start.

::: p1note
**P1 note — same as P1, and just as strict.** Single ownership of a serialized resource was
already the rule on the P1, for the same reason: its pins, too, gave you no hardware
arbiter. If you internalized "one COG owns the bus" on the P1, that instinct is exactly
right here — the P2 hasn't relaxed it. What the P2 adds (next force but one) is a way to
move some of those resources off COGs entirely.
:::

The fuller treatment of resource ownership — including the cases where a "shared bus"
default breaks down — lives in the decomposition layer of the knowledge base; the P2
coordination mechanisms themselves (locks, atomic access, COG attention) are in the
*P2 Assembly Language Manual*.

### Force 2 — What does each seam promise?

Once Force 1 has scattered work across several COGs, those COGs have to exchange data. The
second force asks: for each place where two COGs meet — each *seam* — *what does the
exchange promise?* Does the sender wait for the receiver? Does the receiver always see the
freshest value, or every value? Who depends on whom?

That promise is called the **contract** for the seam, and choosing it *is* a decomposition
decision, because the coupling you can tolerate determines where the boundary goes. A few
contracts you'll reach for: a *blocking call*, where the caller waits on the callee's
worst-case latency (tight coupling); a *latest-wins mailbox*, a single slot where the
producer never waits and the consumer always reads the newest value (decoupled completely);
a *ring buffer*, which decouples the two rates while preserving every sample; *published
telemetry*, where one writer puts values in hub and any number of readers take them with no
lock at all. Each contract names a different dependency direction, and choosing it draws the
boundary.

Why is this a *design* act on the P2 rather than a detail? Because the P2 has no operating
system underneath you — no message queue, no IPC layer, nothing imposing a coordination
mechanism. Inter-COG coordination is whatever *you* build out of hub RAM, atomic single-long
access, the sixteen locks, and COG-attention signalling. That absence is a feature: it means
you choose the exact coupling your timing budget allows, with nothing forced on you. An
engineer who thinks "there's no free message queue here — I am *choosing* the coupling"
designs the seam deliberately. One who reaches for a blocking call out of habit quietly
throws away the determinism the chip just gave them, by making a fast loop wait on a slow
one.

#### One seam, three planes

Here's the part that sharpens Force 2 from a single choice into a real tool. Every seam
between two COGs is really *three* relationships superimposed, and each wants its own
mechanism:

- The **data plane** — bulk, rate-defined movement. Its concerns are throughput, buffering,
  and back-pressure; its tools are the streamer, the hub FIFO, burst transfers. Get it wrong
  and you *waste bandwidth* — visible, and recoverable.
- The **control plane** — commands and state. Low-rate but correctness-critical: atomicity,
  ordering, who is allowed to write what. Its tools are hub mailboxes, locks, single-writer
  ownership of each shared long. Get it wrong and you *corrupt state* — an intermittent race.
- The **event plane** — signalling and urgency. Its concerns are latency and priority; its
  tools are COG-attention signalling, the event system, or deliberate polling. Get it wrong
  and you *miss a deadline* — and that one stays silent until the field.

Notice they're ranked by the cost of getting them wrong, and you spend your design care in
the inverse order: an event-plane mistake is the most expensive and the hardest to see, so
it deserves the most thought. The signature way to use the chip badly is to build all three
planes on one mechanism — polling a hub flag (a control-plane tool) to deliver an urgent
event (an event-plane need), or pushing bulk data through mailbox words (control-plane)
instead of the streaming path (data-plane). Naming the three planes is what lets you catch
that conflation in your own design before it ships.

There's one small discipline from the control plane worth carrying away by name, because it
recurs everywhere on the P2: when you publish a multi-field update through hub, write the
payload first and bump the signalling counter *last*. Because a single-long write is atomic,
a reader that watches that counter can never catch a torn, half-written value — the
publish-last ordering makes a lockless hand-off safe. It costs nothing and it removes a
whole category of glitch.

The failure modes Force 2 prevents are two: blocking calls between COGs that quietly
*serialize* a system that was meant to run in parallel, and multi-long structures written by
one COG and read mid-update by another, producing torn reads that look like glitches. Both
fixes are structural — choose the contract deliberately, and publish atomically. The deep
treatment of inter-COG contracts and the coordination primitives is in the *P2 Assembly
Language Manual*.

### Force 3 — Where do two cadences meet?

The third force is the one a beginner's instinct most often misses, because it corresponds to
nothing you can point at. There's no chip for it and no line item in a parts list.

Devices live in different **time domains**. An LED chain wants nanosecond-precise bit timing;
a set of servos wants a smooth fifty-hertz stream; a voice recognizer is polled lazily and
stretches the clock when it feels like it; a battery reading is meaningful about once a
second; an ultrasonic echo is a one-shot event that happens when it happens. The question
Force 3 asks is: *where does data cross from one cadence to another* — and what has to sit at
that crossing to reconcile the rates?

Because whenever data crosses a cadence boundary, *something must adapt the rate*, and that
adapter is a distinct responsibility — so it's a distinct object. The P2 positively
encourages you to put different time domains on different COGs and smart pins; that's what
eight deterministic cores and sixty-four autonomous pins are *for*. But the instant you do,
you've created the software equivalent of a clock-domain crossing — the same problem
hardware engineers handle deliberately at the boundary between two clocks — and, like its
hardware namesake, it produces glitches if you don't handle it on purpose. (The literature
has an exact name for a chip shaped like this — *globally asynchronous, locally synchronous* —
and Appendix B points you to it.)

Two kinds of adapter fall out, and they're worth telling apart:

- A **sampler or buffer**, where a fast producer and a slow consumer meet. The rule for
  picking which is a question about the consumer: does it need *every* sample, or only the
  *freshest*? Every sample means a buffer; only the freshest means a latest-wins slot. That choice is
  the whole design of the adapter.
- A **slew or easing engine**, where a discrete intent has to become a continuous stream. A
  command like "stand" or "walk" is a *step* — it arrives once. A servo physically cannot take
  a step; it needs a smooth, accelerated-then-decelerated trajectory at its own frame rate.
  The thing that turns the one into the other — the *ramp* — is a responsibility distinct from
  both the policy that knows *what* to do and the driver that knows *how* to talk to the chip.
  Pulling the ramp out of both is what keeps both of them clean.

And there's a third situation that belongs to this force, where it collides with Force 1 in a
way worth seeing. Suppose several devices share *one* bus but want *different* cadences —
servos at fifty hertz, an IMU at a hundred, a battery at one. Force 3 says "different cadences
want separating," but Force 1 flatly forbids splitting the bus across COGs. They can't both
win by cutting. The resolution isn't a second COG on the bus — it's **cooperative tasks
within the single owning COG**: several small routines sharing that one COG and that one bus,
each running at its own cadence and yielding at transaction boundaries so the bus stays
coherent. That's a first-class decomposition tool for "shared resource, multiple rates," and
it's the kind of answer you only find by holding two forces in tension instead of applying one
in isolation.

⚠️ **Watch out:** ignore the rate adapters and you get two classic embedded bugs. Skip the
sampler and a slow consumer back-pressures a fast producer (or a fast producer floods a slow
consumer) — dropped frames, stalls, torn state. Skip the slew and your servos *snap* to
position instead of moving, drawing current spikes and mechanical shock, because a step went
straight to the actuator with no ramp between intent and motion.

::: p1note
**P1 note — new room to cross into.** Rate adaptation was always a concern, but the P2 hands
you far more places to put a time domain — sixty-four smart pins that each hold their own
cadence autonomously, where the P1 had thirty-two plain pins and often a spare COG pressed
into bit-banging. That's a gift, but it's also *more cadence boundaries to cross*: every time
you push a job out to a smart pin, you've created a crossing back to the COG that needs an
adapter. The fabric got wider; mind the seams between its cells.
:::

The implementation patterns for samplers, easing engines, and cooperative tasking live in the
Spin2 pattern library; the smart-pin modes that let a pin hold its own time domain are in the
*I/O & Smart Pins User Guide*.

### Force 4 — How high does each piece sit?

The first three forces are horizontal: they decide which COG owns what, and how the pieces
talk across the gaps. The fourth is the *vertical* consequence that falls out once they've
drawn the structure — which is why we call it emergent rather than primary. It answers the
question every programmer eventually asks: *how much code goes in one object?*

The honest answer is not a line count and not a component count. It's this: **split where the
unit changes, or where the axis of change changes.** Stack the objects within an ownership
domain so that each tier does exactly one unit conversion and changes for exactly one reason.
The canonical stack climbs from *bits on a wire*, to *device registers*, to *physical units*
(millimeters, degrees, millivolts), to *behavior*. Each tier speaks a different unit than the one below it, and
that change of unit is the seam.

The principle underneath is an old and durable one — Parnas's *information hiding*: decompose
around the things that change independently, not around processing steps. Two pieces of code
that will *always* change together for the same reason belong in one object. Two that change
for different reasons — a new chip versus a new behavior — belong in different objects, even
when they sit in the same call chain. A line-count rule would never produce a clean
four-tier device stack; the unit-conversion rule produces it automatically, because each unit
boundary is exactly a place where the code above and below it change for different reasons.

On the P2 this force negotiates against a hard limit, and you should know it's there: COG-
local memory is *tiny* — 512 longs of register RAM, of which 496 are usable for PASM code and
data. Unlimited layering isn't free; each tier boundary costs a call and a little state. So the
default is one tier per unit conversion, with an explicit escape: when a COG is genuinely tight
on memory, fold two adjacent tiers together — but say so, and never fold two tiers that change
for *different* reasons just to save space, because that quietly rebuilds the monolith you were
avoiding.

That monolith — or worse, a "driver" that mixes register pokes with behavior logic, so that
swapping the IMU chip forces you to re-test the walk cycle — is the failure Force 4 prevents.
When tiers that change for different reasons are fused, every change ripples across unrelated
concerns, and the clean place you *would* have tested at is gone.

### Reconciling the forces

Here's the thing the four-forces list can hide: the real skill isn't applying each force, it's
*reconciling* them, because they pull against each other and against plain simplicity. You've
already seen one tension — Force 1 says "one COG per bus," Force 3 says "different cadences want
separating," and when three cadences share one bus, the resolution is cooperative tasks inside
the one owner. There are more like it. Force 2's instinct to decouple every seam reconciles
against simplicity — not every hand-off needs a ring buffer; a latest-wins slot is usually
enough. Force 4's instinct to layer everything reconciles against that tiny COG memory — deep
stacks cost RAM and per-call overhead you may not have.

None of these tensions has a formula. What you do is hold the forces together, let them argue,
and let the *hardware and the hardest deadline win* — those are the two things you can't
negotiate with. That habit of reconciliation, more than any single rule, is what separates a
design that fits the chip from one that fights it.

## The objects that guard the whole machine

The four forces build a clean structural tree: who owns what, how the branches talk, what
adapts between cadences, how deep each branch layers. But a real machine needs some objects that
don't live *in* that tree — they live *across* it. They're driven by concerns that don't respect
the ownership hierarchy, and if you only ever apply Forces 1–4, you end up with a tidy tree and
nowhere to put the supervisor, the translator, or the calibration data. Naming these cross-cutting
concerns is what keeps them from getting smeared across everything. There are five that recur:

- **A safety override.** Some authority has to be able to override the whole machine — a
  low-battery cutoff, a watchdog, an emergency stop — and a fault in one place has to be
  contained so it can't cascade. This wants an explicit, privileged supervisor sitting *above*
  the policy layer, able to suppress it.
- **An external-interface translator.** When you integrate a subsystem that has its *own*
  vocabulary — a sensor's command codes, a vendor's frame format — put a translation object at
  the boundary so that external naming never leaks inward. The outside vocabulary changes on
  someone else's schedule; quarantine it behind one seam and a vendor change touches one object
  instead of your whole codebase.
- **A configuration store.** Separate what varies *per physical unit* — trim offsets, pin maps,
  per-board personality — from what's fixed *by design*. Identical firmware should run on every
  unit you build; the per-unit constants belong in data, not sprinkled through your drivers.
- **Testability seams.** Shape the objects so each one can be exercised *standalone on real
  hardware* before the whole is assembled. On embedded work you can't single-step a servo; you
  bring hardware up one layer at a time. The seam you can test at is the seam you should cut at —
  and the need to observe a layer often reveals a boundary you'd otherwise have fused.
- **A lifecycle sequencer.** Objects have a *temporal* dependency graph: power and rails before
  buses, a chip awake before you actuate it, COGs launched in a safe order. Someone has to own
  that sequence.

There's a reason several of these have to be *explicit* on the P2 specifically rather than
emergent. COGs are independent — which is wonderful, because a hung COG won't drag the others
down, but also means a hung COG won't stop driving its pins on its own, and means init ordering
*isn't* implied by your call structure the way it is in a single-threaded program, because COGs
launch concurrently. The chip gives you deterministic, isolated cores; these cross-cutting
objects are how you reimpose whole-machine guarantees — safety, ordering, calibration — back on
top of that isolation. You can't assume they'll fall out of the design. You place them on
purpose, and you place them *after* the structural tree is drawn, because where each one goes
depends on the tree it's guarding.

💡 **Tip:** when you think you're done, go down this list of five and ask "where does each of
these live in my design?" — and if one genuinely isn't needed (no external vocabulary, so no
translator), say so out loud. An omission you *named* is a decision; an omission you didn't
notice is a bug waiting in the field.

## Keeping a budget

Everything so far has been about drawing boundaries. This section is about a number that tells
you when you've drawn them wrong.

The P2's resource lattice is *finite*, and you should treat that as a design invariant rather than
a thing you discover at the end. There are eight COGs, sixty-four smart pins, sixteen locks, one
shared CORDIC, a bounded hub bandwidth, LUT sharing only between adjacent COG pairs, and 512 longs
of memory per COG. None of those is negotiable. So a useful habit is to keep a **resource budget** —
an allocation table you fill in *as you derive*, not a report you write afterward — listing which
COG owns which timing domain, which pins run which mode, where each lock goes, how much hub traffic
you're generating, and how much of each finite thing remains. A blank row in that table is a
resource you forgot to account for.

The budget earns its keep through one sharp signal. **"Running out of COGs" is the P2's concrete way
of telling you the design is too *coupled*.** When the lattice can't hold your proposed allocation,
the boundaries are wrong — not the chip. So when you run short, the move is to *re-cut, not cram*:
look for a funnel COG that's quietly doing several jobs, a protocol a smart pin could absorb to free
a COG, or a seam whose coupling is so high it shouldn't have been cut where it was. There's an honest
escape — when every COG genuinely owns one irreducible real-time job and nothing can be absorbed, the
design is at capacity, and the answer is to reduce *scope* or move a concern off-chip, not to
time-slice a real-time job onto a shared COG. But reach for that escape last, after you've tried to
re-cut. Most "out of COGs" is too-coupled in disguise.

## Judging the cut

You can now *propose* a decomposition. The last piece of the method is how to *judge* one — to look at
two candidate cuts and say, with more than a feeling, which is better. This is the part most worth
slowing down for, because it turns "that seems cleaner" into something you can actually check.

Three tools, in increasing sharpness:

**Coupling, as a countable integer.** On the P2, the coupling between two COGs is physical and
*countable* — it stops being a vibe. Across any boundary you draw, count the longs that cross it per
unit time, the fields that share an invariant (data that must change together to stay correct), and
the locks held across the cut. Minimize that number. Two candidate cuts can be compared directly by
their counts, and the lower one wins unless cohesion argues otherwise.

**Connascence — the sharpest tool.** Two pieces of code are *connascent* if changing one forces a
change in the other to stay correct. It comes in *static* forms, visible right in the source (two
sides agreeing on a name, a type, a field order), and *dynamic* forms, true only at runtime (two
sides agreeing on execution order, on timing, on a value relationship). The governing rule is:
maximize connascence *inside* a boundary, minimize what *crosses* it, and *convert* the strong dynamic
forms into weak static ones right at the seam. On the P2 the dangerous case is specific and worth
memorizing: **dynamic connascence that crosses a COG boundary** — a timing assumption, an
execution-order assumption, a shared runtime value — because the hardware will faithfully express it as
*jitter and races*. The publish-last discipline from Force 2 is exactly this conversion in action: it
takes a dynamic execution-order dependency between two COGs and makes it safe by construction.

**Back-pressure, as a min-cut.** Put the two together and you can state precisely what a good boundary
*is*. Every boundary carries a back-pressure equal to the connascence forced to cross it times the cost
of the channel that carries it — and on the P2 the channel cost is concrete (a mailbox's hub traffic, a
lock's contention, an attention signal's latency). A good boundary is a **min-cut**: the cohesion you
gain inside each piece exceeds the back-pressure across the cut. That gives you a crisp objective to aim
at instead of an aesthetic — draw the boundary where the things that must stay together stay together,
and the least, weakest connascence crosses the cheapest channel. If a cut isn't a min-cut, that's your
signal that one of the forces placed a boundary wrong, and you redraw it.

These three — coupling, connascence, back-pressure — rest on a body of design literature older than
the P2; Appendix B names the sources so you can go deeper when a problem outgrows this chapter.

## The first-contact procedure

We now have the forces, the cross-cutting objects, the budget, and the way to judge a result. The last
thing you need is the *order* to apply them in — because the forces are orthogonal, but the work isn't:
some choices depend on earlier ones (you can't pick a seam's contract before you know where the COG
boundaries are). Here is the routine to run the first time you meet a hardware mix, before you write a
single object. Think of it as a method you *adapt*, not a script you obey — the spine steps always run,
and the others state when you can skip them.

The procedure deliberately *inverts* the classic top-down approach. You don't start from the data model.
You start from the **hardware edge and the timing budget**, and let the structure fall out of them:

1. **Enumerate the wires.** What buses, timing-critical pins, and discrete signals exist? List the
   serialized resources. *(Always runs — everything downstream depends on it.)*
2. **Triage against the smart pins.** For each peripheral, can a smart pin absorb its protocol entirely
   in hardware — PWM, serial, quadrature, an ADC or DAC, edge counting? The ones a pin can own drop out
   of the COG-cadence problem completely. This is the physical axis used as a tool: a smart pin *deletes*
   a software module. *(Skip for a protocol no pin mode covers — a multi-byte I²C transaction stays a
   software-owned resource.)*
3. **Assign owners.** Group the survivors by bus and timing budget, and give each group exactly one
   owning COG and one transport object. Let the sharing topology pick the transport's shape — shared
   singleton for a shared bus, self-contained instance for a sole device. *(Always runs — this COG map
   gates every later choice.)*
4. **List the cadences.** At what rate does each device want service, and where do two rates meet? This
   surfaces the rate-domain boundaries and the discrete-to-continuous paths. *(Skip only if everything
   runs at one shared cadence with no easing path.)*
5. **Resolve same-bus rate conflicts.** Is any single bus serving multiple cadences? If so, the answer is
   cooperative tasks *within* the owning COG, not a second COG on the bus. *(Skip when no bus serves
   multiple cadences.)*
6. **Draw the seams.** For each inter-COG edge, what coupling does the deadline allow — and design its
   data, control, and event planes separately. *(Skip for a single-COG design with no seams.)*
7. **Layer each branch.** Within each ownership domain, how many distinct unit conversions are there?
   One tier each. *(Collapse tiers where COG memory is tight — and say so.)*
8. **Place the cross-cutting objects.** Where do the safety override, the translator, the configuration,
   the test seams, and the sequencer go? *(Name the ones a given machine doesn't need, so the omission is
   a decision.)*
9. **Reconcile.** Where do two forces disagree, and does the result fit the budget? *(Always runs — the
   reconciliation against the hardest deadline is what makes the output sound.)*

One more property worth knowing: the procedure is **fractal**. After the top-level pass, you can run the
very same routine *inside* a COG that owns a bus — it has its own internal cadences, its own seams between
cooperative tasks, its own layers. Apply it at whatever altitude you're working.

When you're done, you hold two things: the object-and-COG set, and the resource budget that proves it
fits. Judge it with the three tools from the last section before you commit a line of code.

## Watching the method run: a walking robot

Let's watch the whole method run, once, end to end, on a single machine — a small walking robot, a
quadruped "dog." Before we start, the one thing that matters most about this section: **this is one
machine's answer, shown to make the method visible — it is not a template.** Your machine will be
different, so the object set you derive will be different. Read for the *moves* — which force fires at
each step and why — never for the result. If you ever catch yourself copying a boundary from here into a
design of your own, stop, and run the procedure against *your* wiring instead. That's the whole point of
having a method rather than a catalogue.

Here's the only input we start from — the hardware, nothing else:

- **I²C bus 1** carries a multi-channel servo/PWM controller, an IMU, and a battery ADC — all behind a
  hard ~50 Hz motion deadline.
- **I²C bus 2** carries a single voice-recognition module that clock-stretches and is polled slowly.
- **Three discrete signals**: an addressable LED chain (timing-exact serial), a buzzer, and an ultrasonic
  range sensor (a one-shot ping and echo).

Nothing about the object set is given. We *derive* it, by walking the procedure.

**Steps 1–2 — enumerate, then triage.** The serialized resources are the two I²C buses and the three
discrete pins. Now triage against the smart pins: the LED chain (precise serial framing), the buzzer
(tone), and the ultrasonic ping-and-echo (pulse timing) each map to an autonomous smart-pin mode — the
pin can own the protocol, so no COG bit-bangs any of them. The two I²C buses are multi-byte stateful
protocols; they survive triage and need software owners. *Three peripherals just left the COG-cadence
problem entirely* — that's the physical axis deleting work for us.

**Step 3 — assign owners.** Bus 1 has three devices behind one timing budget, so it gets one owning COG
and a *single shared transport* that three register-level chip drivers call into. Bus 2 has one device, so
it gets a *different* owning COG and a *self-contained transport* with nothing to coordinate. The discrete
smart pins are owned by whichever COG already owns their timing domain. Notice the same protocol — I²C —
ended up with two different transport shapes, decided entirely by sharing topology.

**Steps 4–5 — cadences, and the same-bus conflict.** Bus 1 serves three cadences at once: servos near
50 Hz, the IMU near 100 Hz, the battery near 1 Hz. Force 1 won't let us split that bus across COGs, and
Force 3 won't let us pretend the cadences are the same. So the resolution is three *cooperative tasks
inside the bus-1 COG* — a sense task, a motion task, a slower dispatch task — each running at its own
cadence and yielding at bus-transaction boundaries. We also flag one discrete-to-continuous path: a "walk"
command has to become a smooth servo trajectory, so a slew engine is going to be needed.

**Step 6 — draw the seams, per plane.** The orchestrator-to-motion seam is a *control-plane* link: a
latest-wins command mailbox with a sequence/acknowledge handshake, arguments written first and the
sequence counter bumped last, so a torn read is impossible without a lock. Motion-to-everyone is a
*data/telemetry* link: lock-free published telemetry — attitude, battery, mode, leg angles — sitting in
atomic single longs with one writer and any number of lockless readers. Inbound device events (a finished
ping, a recognized word) are an *event-plane* link: a value plus a bumped freshness counter that the slow
poll edge-detects. Nothing blocks anywhere — the 50 Hz loop never waits on the orchestrator, and the
orchestrator never waits on a device.

**Step 7 — layer the motion branch.** It splits by unit conversion into four tiers: the PWM-chip register
driver (changes if the chip changes); then servo pulse-width and channel semantics (changes if the wiring
changes); then leg inverse-kinematics, foot-XYZ to joint-degrees (changes if the leg geometry changes); then
the gait and pose policy (changes if the behavior changes). A line-count rule would never have produced that
stack; the unit-conversion rule produced it on its own.

**Step 8 — place the cross-cutting objects.** A critical-battery hard-halt latch sits above policy and
suppresses *all* motion regardless of intent (safety). A voice-vocabulary-to-internal-command map sits at
the edge, separate from both the recognizer driver and the policy (translation). A per-joint trim store the
drivers read but never hard-code (configuration). A bring-up test per layer — bus scan, then chip, then
servo-center, then leg IK, then gait (testability). And the top-level orchestrator owns the launch order and
wakes the PWM chip from sleep before any servo write (lifecycle). None of these is a node in the tree; each
guards or spans it.

**Step 9 — reconcile against budget and deadline.** Tally the lattice for this machine:

| Resource | This machine uses | Of the limit |
|----------|-------------------|--------------|
| COGs | orchestrator, bus-1 body-control, bus-2/IO — about three | 8 |
| Smart pins | the LED chain, buzzer, ultrasonic — three | 64 |
| Locks | none — telemetry is single-writer atomic publish | 16 |
| CORDIC | one shared engine, uncontended at this scale | one shared |
| Hub bandwidth | modest — mailbox words, no bulk streaming | egg-beater rotation |

It fits, with COGs to spare, and nothing forces a re-cut. Now judge it with the three tools: coupling is
*low* — telemetry crosses as atomic longs, with no shared invariant and no locks — and the one dynamic
connascence that crosses a COG boundary (execution order on the command mailbox) was already tamed to static
by the publish-last discipline. This is a min-cut.

```{=latex}
\RobotDecompositionDiagram
```

::: {.figurecaption #fig:robot-decomposition}
The object-and-COG map this derivation produced — read it for the moves, not the result. A different hardware mix yields a different, equally sound shape.
:::

Now step back and notice what just happened — and especially what *didn't*. We never started from a parts
list and reached for the nearest matching template. We started from the *wires and the timing*, ran the
forces in order, and the object set *fell out*. Three things appeared that no catalogue could have handed
us: the two I²C transports are the same protocol with different state models, decided by sharing topology;
the rate adapters — the in-COG cooperative tasks and the slew engine — correspond to no chip and no feature,
they fell out of rate *mismatches*; and the cross-cutting objects had nowhere to live until the tree was
drawn, then each took a definite place. Run that same routine on *your* machine and you'll get a different
object set, equally sound. The shape is the routine's output, not its input.

## Where this leaves you

You came into this chapter able to write a P2 program. You leave it able to *design* one — to look at a
machine you've never seen, start from its wires and its deadlines, and derive a sound set of cooperating
objects across the fabric, then judge that set against a crisp objective rather than a feeling. That's the
skill that keeps you on the spatial side of the line we drew at the start: function spread across the chip,
not funnelled back through one core.

A closing word on how to hold all this. The forces, the procedure, and the judging tools are the method;
the robot dog was only the method made visible. The richest, most complete treatment of this material —
every force in full, the reference canon behind each judgment tool, more worked detail than a single chapter
can carry — lives in the decomposition layer of the P2 knowledge base, which is the golden home for this
theory and the place to go when a real design pushes past what we covered here. Appendix A takes up the
space-versus-time thesis in depth, with an honest accounting of what the P2 borrows from FPGA thinking and
what it doesn't; Appendix B is the reading list behind the whole discipline; and the glossary and the
"where to next" map point you into the reference manuals for every part you'll actually program.

You have the picture, you can put it to work, and now you can think in P2. That's the guide. The rest is
yours to build.

# Appendix A — Computing in Space and Time (Why We Borrow FPGA Language)

Throughout this guide — and especially in Chapter 4 — we describe the P2 with words borrowed from
the world of FPGAs and hardware design: *spatial*, *fabric*, *pipeline*, *dataflow*,
*back-pressure*, *systolic*. The borrowing is deliberate and useful, but it carries a risk: taken
too literally, those words would say the P2 *is* an FPGA, and it isn't. This appendix sets the
record straight — what the FPGA vocabulary buys us, and exactly where it stops.

## The temporal-to-spatial spectrum

Computation can be placed on a spectrum by *how* a machine does many things at once. At one end is
the purely **temporal** machine: a single processor core executing one instruction stream, doing
more only by running faster or by time-slicing that one core. At the other end is the purely
**spatial** machine: an FPGA, where function is laid out as physical parallel hardware — many
circuits computing simultaneously, configured by a synthesis tool, with no instruction stream at
all.

The P2 sits between these poles, nearer the spatial end than a conventional microcontroller but
well short of an FPGA. Its eight deterministic COGs and sixty-four programmable smart pins are
real, parallel computing elements you assign function to — that is the spatial character. But each
element runs *software*, an instruction stream of its own — that is the temporal character it never
sheds. The phrase the guide uses, **coarse-grained spatial fabric**, names exactly this in-between
position: spatial in how you allocate function, temporal in how each element actually computes.

## What transfers, and what doesn't

The FPGA *mindset* transfers; the FPGA *claims* do not. Three honest qualifications keep the
borrowing safe:

- **The P2 is coarse-grained, not fine-grained.** An FPGA's fabric is a sea of logic gates and
  routing you configure at the bit level. The P2's "fabric" is a handful of full 32-bit processors
  and some smart pins. You allocate whole COGs to jobs; you do not wire gates. This is a difference
  of *kind*, not degree.
- **The P2 is still software.** You write programs and launch COGs. There is no
  hardware-description language, no logic synthesis, and crucially **no place-and-route** — the step
  that maps an FPGA design onto physical silicon has no P2 equivalent. The determinism a COG gives
  you comes from fixed instruction timing, not from synthesized circuitry.
- **We borrow the discipline, not the identity.** "Think spatially" means *assign one sustained job
  per element and let it run* — a design discipline. It does not mean the P2 reconfigures its
  silicon. Every spatial behavior on the P2 is something you *arrange in software*, which is also
  why a sloppy decomposition can throw it away (the whole argument of Chapter 4).

Hold those three in mind and the vocabulary is a gift: it imports decades of hardware-design
reasoning about pipelines, latency, and dataflow into a software setting where it genuinely
applies. Forget them, and the same words mislead.

## The terminology, mapped

Each borrowed term is pinned below to its FPGA-world meaning, its P2 mapping, and — the column that
does the guarding — where the mapping goes loose. First, the vocabulary for *laying computation out*
as parallel hardware:

| Term | In the FPGA / hardware world | On the P2 | Where the mapping is loose |
|------|------------------------------|-----------|----------------------------|
| Spatial computing | Function laid out as physical parallel circuitry | Function assigned across COGs and smart pins, each running one job continuously | The P2 runs instruction streams; "spatial" is the *allocation* pattern, not literal gates |
| Fabric | The sea of configurable logic blocks and routing | The 8 COGs + 64 smart pins + the hub interconnect you allocate onto | The P2 fabric is a few coarse elements, not a fine-grained gate array |
| Coarse-grained | Processing elements larger than a single gate | Each element is a whole 32-bit processor or a smart pin | This is the defining gap — the P2 is far coarser than even a coarse-grained array |
| Pipeline | Data through chained hardware stages, throughput set by the clock | Data through a chain of COGs, throughput set by the pipeline rate, not instruction count | Each COG stage runs software with its own latency; stages are not register-locked like hardware |
| Dataflow | Computation driven by data availability along channels | COGs exchanging data through hub channels and mailboxes; correctness by data order | There is no hardware firing rule; the dataflow discipline is something you implement |
| Systolic array | A regular array of cells rhythmically passing data to neighbors | COGs as pipeline stages handing data along, sometimes via adjacent-COG LUT sharing | Only adjacent COG pairs share a LUT; it is a small, irregular array, not a large regular mesh |

Then the vocabulary for the *resources, timing, and dataflow* of the machine — ending with the one
term that does not cross over at all:

| Term | In the FPGA / hardware world | On the P2 | Where the mapping is loose |
|------|------------------------------|-----------|----------------------------|
| Resource lattice | (Loosely) the fixed grid of resources a design maps onto | The finite, heterogeneous set you budget against: 8 COGs, 64 smart pins, 1 CORDIC, 16 locks, hub bandwidth, LUT pairs | "Lattice" here means a fixed resource budget, not FPGA routing |
| Back-pressure | A downstream consumer signalling it cannot keep up, throttling upstream | A slow consumer forcing a fast producer to wait at a seam; managed with buffers and the hub FIFO | Same concept, implemented in software at hub seams |
| Latency / throughput | Time through a stage; rate of completed items | The same, measured against the system clock and the egg-beater rotation | Transfers cleanly — this pair means the same on both sides |
| Latency-insensitive | Design so correctness depends on data order, not arrival time | Hub channels designed so hub jitter is harmless by construction | A discipline you adopt, not a property the silicon enforces for you |
| GALS (globally asynchronous, locally synchronous) | Synchronous islands joined by an asynchronous interconnect | Locally-synchronous, deterministic COGs joined by the asynchronous hub fabric | An exact characterization — this one transfers well |
| Place-and-route | The synthesis step mapping a design onto physical gates and wires | *(no equivalent)* — you write software and launch COGs; nothing is synthesized | The sharpest "does not transfer": there is no P2 place-and-route at all |

The last row is the one to remember. The P2 borrows the FPGA's *way of thinking about parallel
work* while remaining, start to finish, a software machine. Appendix B points you to the literature
behind both halves of that sentence.

# Appendix B — Further Reading on Functional Decomposition

Chapter 4's method rests on a body of published work older and deeper than the P2 itself. This is
the short list — each entry with a line on why it matters here. It runs along the two axes the
chapter used: the **logical** axis (how to cut software well, independent of any chip) and the
**physical and concurrent** axis (how parallel, communicating elements compute — the literature
closest to what the P2 actually is). A third short group covers boundaries, real-time scheduling,
and the generative stance the whole approach takes.

## The logical axis — cohesion, coupling, and what to hide

- **Parnas, D.L. — "On the Criteria To Be Used in Decomposing Systems into Modules." *Communications
  of the ACM*, vol. 15, no. 12, 1972, pp. 1053–1058.** The origin of *information hiding*:
  decompose around the decisions likely to change, not around processing steps. This is the
  principle under Force 4 (layer by axis of change).
- **Constantine, L.L. & Yourdon, E. — *Structured Design: Fundamentals of a Discipline of Computer
  Program and Systems Design.* Prentice-Hall, 1979.** Where *coupling* and *cohesion* come from —
  the measures behind a good seam: low coupling across COGs, high cohesion within one.
- **Page-Jones, M. — *Fundamentals of Object-Oriented Design in UML.* Addison-Wesley, 1999.** Its
  treatment of *connascence* is the sharpest tool in Chapter 4's "judging the cut" section — and the
  source of the static-versus-dynamic distinction that, on the P2, separates a safe seam from a
  race.

## The physical and concurrent axis — communicating processes and dataflow

- **Hoare, C.A.R. — "Communicating Sequential Processes." *Communications of the ACM*, vol. 21, no.
  8, 1978, pp. 666–677; expanded as *Communicating Sequential Processes*, Prentice-Hall, 1985.** The
  formal model in which COGs are processes and mailboxes are channels. If one work explains why the
  P2's no-shared-OS, message-passing shape is sound, it is this one.
- **INMOS Ltd. — *occam Programming Manual.* Prentice-Hall, 1984.** The Transputer's language —
  independent processors, a message-passing fabric, no shared operating system. The P2 is very
  nearly a Transputer reborn, and inherits its decades of correctness reasoning.
- **Kahn, G. — "The Semantics of a Simple Language for Parallel Programming." *Proceedings of the
  IFIP Congress 74*, Stockholm, 1974, pp. 471–475.** Kahn process networks: processes that
  communicate only by blocking reads on FIFO channels are *determinate regardless of timing* — the
  rule that makes inter-COG dataflow survive hub jitter.
- **Kung, H.T. & Leiserson, C.E. — "Systolic Arrays (for VLSI)." In Mead, C. & Conway, L.,
  *Introduction to VLSI Systems*, Addison-Wesley, 1980 (§8.3).** Rhythmic data passing through a
  regular array of processing elements — the mental model for using COGs as pipeline stages.
- **Lee, E.A. & Messerschmitt, D.G. — "Synchronous Data Flow." *Proceedings of the IEEE*, vol. 75,
  no. 9, 1987, pp. 1235–1245.** Static data rates yield computable buffer sizes — the math behind
  Force 3's rate adapters and the sizing of a buffer.
- **Carloni, L.P., McMillan, K.L. & Sangiovanni-Vincentelli, A.L. — "Theory of Latency-Insensitive
  Design." *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems*, vol. 20,
  no. 9, 2001, pp. 1059–1076.** Correctness by data *order*, not arrival *time* — the formal bridge
  to the spatial domain and the discipline that makes hub jitter harmless.
- **Chapiro, D.M. — *Globally-Asynchronous Locally-Synchronous Systems.* PhD thesis, Stanford
  University, 1984.** The exact characterization of the P2 — locally synchronous COGs, an
  asynchronous hub fabric — and the source of the clock-domain-crossing discipline Force 3 borrows.

## Boundaries, real-time, and the generative stance

- **Evans, E. — *Domain-Driven Design: Tackling Complexity in the Heart of Software.* Addison-Wesley,
  2003.** *Bounded contexts* as subsystem boundaries with their own internal language — the
  reasoning behind the external-interface translator (cross-cutting force C2).
- **Liu, C.L. & Layland, J.W. — "Scheduling Algorithms for Multiprogramming in a Hard-Real-Time
  Environment." *Journal of the ACM*, vol. 20, no. 1, 1973, pp. 46–61.** Rate-monotonic scheduling —
  assigning urgency by cadence and reasoning about deadlines, the theory under the event plane's
  latency tiers.
- **Alexander, C. — *A Pattern Language: Towns, Buildings, Construction.* Oxford University Press,
  1977.** The source of the idea that patterns should *compose into a grammar* rather than sit in a
  catalogue — exactly the stance Chapter 4 takes toward decomposition: a method that generates, not
  a set of templates to copy.

# Glossary

Terms as this guide uses them, weighted toward the decomposition vocabulary of Chapter 4. For the
silicon parts themselves — COG, hub, smart pin, CORDIC, streamer — see Chapter 1.

**Altitude layering (Force 4).** The vertical decomposition force: within one ownership domain,
stack objects so each tier does exactly one unit conversion and changes for exactly one reason —
bits, then registers, then physical units, then behavior.

**Back-pressure.** The resistance a seam imposes when a consumer cannot keep up with a producer;
measured as the connascence crossing the seam times the cost of the channel that carries it. A good
boundary minimizes it.

**Coarse-grained spatial fabric.** The P2 seen as a modest number of real parallel computing
elements (8 COGs, 64 smart pins) you assign function to — spatial in allocation, but built from
whole processors rather than logic gates.

**Cohesion.** How well the parts inside one object belong together. High cohesion within an object
is the goal; it is the complement of coupling.

**Connascence.** The relationship by which changing one element forces a change in another to stay
correct. *Static* forms are visible in source (name, type, field order); *dynamic* forms are true
only at run time (execution order, timing, value). On the P2, dynamic connascence crossing a COG
boundary shows up as jitter and races.

**Cooperative tasking (tasks-in-a-COG).** Several routines sharing one COG and one bus, each running
at its own cadence and yielding at safe points — the resolution when one bus must serve several
cadences (Force 1 against Force 3).

**Coupling.** How much crosses between two objects — on the P2, a countable integer: longs per unit
time, fields under a shared invariant, locks held across the cut. Minimize it.

**Cross-cutting forces (C1–C5).** The concerns that place objects spanning or guarding the
structural tree rather than sitting in it: safety override, external-interface translation, per-unit
configuration, testability seam, and lifecycle/init order.

**Data / control / event planes.** The three superimposed relationships in any inter-COG seam —
bulk movement (data), commands and state (control), signalling and urgency (event) — each wanting
its own mechanism.

**Data-flow contract (Force 2).** The promise a seam makes: blocking call, latest-wins mailbox, ring
buffer, request/response, or published telemetry. The contract sets the dependency direction and
helps place the boundary.

**Flat device list.** The failure mode Force 1 prevents: every chip a sibling driver under `main()`,
the shape chosen by analogy rather than derived from the wiring. It compiles, then fails as flaky
hardware the moment two COGs touch one resource.

**Funnel.** A "smell": all data routed through one COG, rebuilding a sequential bottleneck whose
loop rate caps the whole system.

**GALS (globally asynchronous, locally synchronous).** The exact shape of the P2 — deterministic,
locally-synchronous COGs joined by an asynchronous hub fabric — and the reason cadence crossings
need deliberate handling.

**Latency-insensitive.** A channel designed so correctness depends on the order data arrives, not
the time — making hub jitter harmless by construction.

**Min-cut.** The objective for a good boundary: draw it where the cohesion gained inside each piece
exceeds the back-pressure across the cut.

**Pipeline.** A chain of COGs through which data flows stage to stage; throughput is set by the
pipeline's rate, not by any one stage's instruction count.

**Publish-last.** The discipline of writing a multi-field update's payload first and bumping its
signalling counter last, so a reader can never catch a torn value — a lockless hand-off made safe by
single-long atomicity.

**Rate adaptation (Force 3).** The force that inserts objects wherever two cadences meet:
samplers/buffers at rate-domain crossings, and slew/easing engines where a discrete intent must
become a continuous stream.

**Resource budget.** The allocation table — COGs, smart pins, locks, CORDIC, hub bandwidth, LUT
pairs, COG RAM — kept as a design artifact. "Running out of COGs" on it means the design is too
coupled.

**Resource lattice.** The finite, heterogeneous set of P2 resources a design allocates onto; the
physical axis of decomposition.

**Resource ownership (Force 1).** The correctness force: each serialized, stateful resource gets
exactly one owning COG, with the object boundary tracing the wire.

**Singleton vs. instance transport.** The transport's state model, decided by sharing topology — a
shared singleton when several devices share one bus, a self-contained instance when a device is
alone on its bus.

**Slew / easing engine.** The object that turns a discrete command (a "step") into a smooth,
rate-limited trajectory at a device's native frame rate.

**Spatial computing.** Doing many things at once by laying function out across hardware elements
rather than time-slicing one core; on the P2, the discipline of assigning one sustained job per COG
or smart pin.

**Systolic array.** A regular arrangement of processing elements that rhythmically pass data to
their neighbors — the FPGA-world model behind using COGs as pipeline stages.

**Transport (object).** The single owning object for a bus or serialized resource; the lowest tier
of a device stack, the one that speaks bits on the wire.

# Where to Next

This guide is the orientation layer; the reference manuals are where you go for depth. Here is the
map.

- **To write the high-level language** — the *Spin2 Language Reference* (current revision v55): the
  full object model, every built-in method and operator, the language's syntax in complete detail.
- **To write assembly** — the *P2 Assembly Language Manual*: the PASM2 instruction set, the
  execution pipeline, COG start/stop, and the inter-COG coordination primitives (locks, atomic
  access, COG attention) that Chapter 4's seams are built from. For a gentler, tutorial-style on-ramp
  to PASM2, the *DeSilva PASM2 Tutorial* teaches the assembly language from the ground up.
- **For I/O** — the *P2 I/O & Smart Pins User Guide*: every smart-pin mode, with
  examples — your first stop whenever a protocol might be absorbable at the pin (Chapter 4's
  smart-pin triage).
- **For high-speed data** — the *P2 Streamer Programming Guide*: the streamer in full, including the
  video (VGA, HDMI, composite), audio, and capture modes.
- **For debugging and bring-up** — the *P2 Debug Window Manual* and the *P2 Single-Step Debugger
  Manual*: the on-chip DEBUG output windows and the single-step debugger, the tools behind Chapter
  3's per-layer bring-up tests (cross-cutting force C4).
- **For the silicon itself** — the *Silicon Doc*: the foundational reference — CORDIC operations,
  the event system, boot sources, and the hardware-timing details the other manuals build on.
- **For the decomposition theory in full** — the *decomposition reasoning layer* of the P2 Knowledge
  Base, the golden home for Chapter 4's forces, planes, evaluation vocabulary, and worked
  derivations, in more depth than a single chapter can carry.

That is the library. Start where your current job points you, and let the picture from Chapter 1,
the language from Chapter 2, the working shape from Chapter 3, and the method from Chapter 4
guide how you put the pieces
together.
