# P2 Single-Step Debugger Manual

*Observe and Control Your Running P2 Code*

**Author:** Iron Sheep Productions, LLC
**Compiler:** `pnut_ts`  **Debug host:** `pnut_term_ts`


# Chapter 1: What Single-Step Debugging Is

You have written a P2 program. You compile it, you run it, and it does not do
what you expected. Maybe a value comes out wrong. Maybe one of your cogs seems
to stop. Maybe everything *looks* fine but the timing is off. Now what?

Without a debugger, your only window into the running chip is whatever you
remembered to print. You add a `DEBUG` line, run again, add another, run again —
guessing where to look. It works, but it is slow, and you can only see what you
thought to ask for in advance.

A **single-step debugger** changes the deal. Instead of watching from outside,
you step *inside* the running program. You can stop it at an exact instruction,
look at every register and memory location as it stands at that moment, run one
instruction and watch what changed, and continue until the next point of
interest. The chip pauses and waits for you.

This manual teaches you to use the P2's single-step debugger to do exactly that.

## What you can observe

When the debugger has your program paused, you can see the live state of the cog
you are looking at:

- **Cog and LUT memory** — all 512 longs of cog RAM and 512 longs of LUT RAM,
  with a *heat map* that shows which locations are being read and written.
- **The flags** — the C (carry) and Z (zero) flags.
- **The Program Counter (PC)** — exactly which instruction is next.
- **Registers** — any cog register, including the special-function registers
  (PTRA, PTRB, the I/O registers, the interrupt vectors, and more).
- **Hub memory** — the shared RAM, shown as hex and as text.
- **The call stack** — how deep into nested calls you are, and the return
  addresses.
- **Smart pins and events** — the configuration and state of the chip's
  peripherals.

> A *heat map* is a colored overlay that shows activity at a glance: locations
> being written show one color, locations being read another, quiet locations
> stay dark. You will meet it properly in Chapter 4.

## What you can control

You are not just watching — you are driving:

- **Step** — execute exactly one instruction, then stop again.
- **Run** — let the program run freely.
- **Break** — stop a freely-running program right now.
- **Breakpoints** — mark places or conditions where the program should stop on
  its own: a specific address, a `DEBUG` statement, a cog starting up, an
  interrupt, or an event.

> A *breakpoint* is a marked spot where execution should pause so you can look
> around. The *watch list* is the debugger's running tally of the registers that
> changed most recently — it surfaces them for you automatically as you step,
> rather than you choosing them in advance.

## When to reach for it

Use the single-step debugger when "add another print and run again" is not
telling you enough — when you need to *see the machine's actual state* at a
precise moment: tracking down a wrong value, understanding why a branch went the
way it did, watching memory get corrupted, or following how two cogs interact.

## A note for readers coming from the P1

If your background is the Propeller 1, two habits will trip you up, and this
manual uses the P2 forms throughout:

- Start a cog with **`COGSPIN`** / **`COGINIT`**, not the P1's `cognew`.
- Read the system counter with **`GETCT`**, not the P1's `CNT`.

The single-step debugger itself is new to you regardless of which Propeller you
came from — there was nothing quite like it on the P1.

## How this manual is organized

Chapters 2–3 get you a running debug session and oriented in the window.
Chapter 4 walks you through your first session hands-on. Chapters 5–8 are the
working reference: commands, breakpoints, observing state, and richer tasks.
Chapter 9 points you to the DEBUG *display* windows (covered in their own
manual). Chapter 10 is tips and troubleshooting, and the appendix tells you
which P2 release first carried each capability.


# Chapter 2: Turning On Debugging and Starting a Session

The debugger does not run all the time. You compile your program *with debugging
enabled*, then run it from the debug host. This chapter gets you from source code
to a paused program.

## Step 1: Compile with debugging enabled

The P2 compiler is **`pnut_ts`**. Add the `-d` flag to build your program with
debugging turned on:

```command
pnut_ts -d myprogram.spin2
```

Without `-d`, your `DEBUG` statements are stripped out and the debugger never
appears — your program just runs normally. This is exactly what you want for a
finished build, and it means you can leave `DEBUG` statements in your source.

## Step 2: Run it from the debug host

The host program is **`pnut_term_ts`**. It combines a serial terminal, the nine
DEBUG display windows, a downloader, and the single-step debugger in one
cross-platform application. Launch your compiled program through `pnut_term_ts`
to download it to the P2 and open the debug session.

## Step 3: Reach a breakpoint

The debugger window appears the first time your program reaches a place that
asks it to. There are three common ways that happens.

### A DEBUG statement in Spin2

An *argument-less* `DEBUG` statement is your Spin2 breakpoint. A bare `DEBUG`
(no parentheses) or an empty `DEBUG()` brings up the single-step debugger and
pauses execution at that line:

```spin2
PUB main() | a, b, sum
  a := 10
  b := 32
  DEBUG                            ' single-step debugger opens here
  sum := add_two(a, b)
  ' display output only — does NOT open the debugger
  DEBUG("sum = ", UDEC_(sum))

PRI add_two(x, y) : result
  result := x + y
```

A `DEBUG` that carries something inside the parentheses — a message or a value,
like `DEBUG("sum = ", UDEC_(sum))` above — does **not** open the single-step
debugger. That form sends formatted output to the DEBUG *display* windows
instead (Chapter 9). To break into the single-step debugger, use the
argument-less `DEBUG` or `DEBUG()`.

### A DEBUG instruction in PASM

In assembly, the `debug` instruction is your breakpoint. Execution pauses on it,
and you single-step from there:

```pasm2
              org       0
start
              mov       a, #10
              debug                     ' execution pauses here
              add       a, #32
              debug                     ' and here
              jmp       #start

a             res       1
```

### A cog starting up

When a cog is started with debugging active, the debugger can break as the cog
begins — useful for catching a problem right at a cog's entry point. (You will
turn this behavior on with the INIT breakpoint in Chapter 6.)

### Opening the debugger automatically (CON-block settings)

The three ways above all place a breakpoint *in your code*. You can also make the
debugger open automatically — without adding a single `DEBUG` line — by defining
a constant in your program's top-level `CON` block. These are read at compile
time, so you still build with `pnut_ts -d`. Two of them open the debugger, and a
third narrows down which cogs are watched:

| Constant | What it does |
|----------|--------------|
| `DEBUG_MAIN` | Simply *defining* this symbol breaks at the very start of your program, ready to single-step from the first instruction. |
| `DEBUG_COGINIT` | Defining this symbol breaks every time a Cog is started (COGINIT), catching each Cog right at its entry point. |
| `DEBUG_COGS` | An 8-bit mask choosing *which* Cogs have debugging enabled — bit 0 is Cog 0 through bit 7 for Cog 7. A Cog whose bit is **clear** runs with debugging off entirely: its `DEBUG` statements produce nothing and the debugger will not break in it. Defaults to all eight. |

`DEBUG_MAIN` and `DEBUG_COGINIT` are switches: their mere presence in the `CON`
block turns the behavior on, so you write them with no value. `DEBUG_COGS` does
take a value, because it carries the cog mask:

```spin2
CON
  DEBUG_MAIN                  ' open the debugger at program start
  DEBUG_COGINIT              ' ...and again whenever a COG starts
  DEBUG_COGS    = %0000_0011  ' but only watch COGs 0 and 1
```

Reach for `DEBUG_MAIN` when you want to step from the very beginning;
`DEBUG_COGINIT` is the one when the bug is in *how* a cog starts up. Use
`DEBUG_COGS` to keep the noise down in a busy multi-cog program: clearing a
cog's bit turns debugging off for that cog, so it never produces DEBUG output
and the debugger never breaks in it — leaving you with only the cogs you actually
care about. (`DEBUG_COGINIT` is the
compile-time equivalent of the INIT breakpoint you will arm by hand in
Chapter 6.)

## What "with debugging enabled" costs

Debugging adds a small amount of code and RAM per cog so the chip can talk to
the host. For a finished release you simply compile without `-d` and the
overhead is gone.


# Chapter 3: The Debugger Window — A Guided Tour

When the debugger opens, you are looking at the full live state of one cog at
once, packed into a fixed character grid. It can feel busy — and the debugger
does little to help at first glance, because **most of its regions are not
labeled with what they are.** A few carry a terse tag (`REG`, `LUT`, `STACK`,
`HUB`), a couple add only a small delta marker to a tag (the Register Watch and
the Smart-Pin Watch), and several — the
disassembly, the hint bar — carry no label at all. You are expected to recognize
each region by *where it sits* and by *the text inside it*.

This chapter is the map that makes that easy. Figure 3-1 numbers every region;
the table right after it names each one, tells you how to recognize it, and — the
part that matters most — tells you **how you interact with it right there.** The
rest of the chapter is a zone-by-zone tour. You do not need to memorize any of
it; just know that this is where to look when you are lost on the screen.

## The screen at a glance

```{=latex}
\begin{figure}[H]
\centering
\begin{tikzpicture}
\node[anchor=south west, inner sep=0] (ssimg) at (0,0)
  {\screenshotfig{inbox/assets/ssdb-fullScreen.png}};
\begin{scope}[x={(ssimg.south east)},y={(ssimg.north west)}]
\tikzset{cq/.style={circle,draw=black,line width=0.4pt,fill=yellow,text=black,%
  font=\sffamily\bfseries\tiny,inner sep=0.3pt,minimum size=2.4ex}}
\node[cq] at (0.166,0.980) {1};
\node[cq] at (0.183,0.936) {2};
\node[cq] at (0.051,0.100) {3};
\node[cq] at (0.142,0.067) {4};
\node[cq] at (0.633,0.608) {5};
\node[cq] at (0.718,0.667) {6};
\node[cq] at (0.872,0.750) {7};
\node[cq] at (0.967,0.533) {8};
\node[cq] at (0.214,0.485) {9};
\node[cq] at (0.755,0.485) {10};
\node[cq] at (0.214,0.421) {11};
\node[cq] at (0.610,0.421) {12};
\node[cq] at (0.220,0.335) {13};
\node[cq] at (0.442,0.335) {14};
\node[cq] at (0.291,0.271) {15};
\node[cq] at (0.407,0.142) {16};
\node[cq] at (0.715,0.142) {17};
\node[cq] at (0.938,0.367) {18};
\node[cq] at (0.500,0.020) {19};
\end{scope}
\end{tikzpicture}
\caption{The single-step debugger window with every region numbered; the table below names each one. (Debugging cog 0.)}
\end{figure}
```

## Region reference

Read this once to get the lay of the land, then use it as a lookup. The middle
column is how you *find* a region on an unlabeled screen; the last column is what
you can *do* there — the interactions are collected in full in Chapter 5.

| # | Region | Find it on screen by… | What it shows | You act here by… |
|---|--------|-----------------------|---------------|------------------|
| 1 | Title bar | top edge: *Debugger - Cog N* | which cog this window is for | — (each cog gets its own window) |
| 2 | Status strip | top row: `C Z PC SKIPF XBYTE CT` | where you are: flags, PC, skip pattern, XBYTE state, system counter | click **PC** to re-lock the disassembly to the PC; hover **CT** for elapsed seconds |
| 3 | Cog register map | far-left tall column tagged `REG` | heat map of all cog RAM ($000–$1FF) | click a spot to lock the disassembly to that cog address |
| 4 | LUT register map | 2nd tall column tagged `LUT` | heat map of all LUT RAM ($200–$3FF) | click to lock the disassembly there |
| 5 | Disassembly | center; code lines, one highlighted | your code, decoded; the highlighted line is the next instruction | L-click = lock to PC · R-click a line = toggle an address breakpoint · wheel scrolls |
| 6 | Register Watch | tagged `REG` with a delta marker, right of disassembly | cog registers that just changed | press **R** or click the box to reset the list |
| 7 | Special registers | register-name column, `IJMP3` through `INB` | the 16 special-function registers, $1F0–$1FF | click a **PTRA**/**PTRB** value to jump the hub viewer there |
| 8 | Event flags | far-right column of event names (`INT`, `CT1`, ... `QMT`), each `0/1` | which hardware events are set | click an event name to arm a break on that event |
| 9 | Execution mode | small tag below disassembly | `MAIN`, or `INT1/2/3` while in an interrupt | — (read-only) |
| 10 | Call stack | band tagged `STACK`, 8 hex values | the 8-level hardware CALL stack | click a value to jump the disassembly to that return address |
| 11 | Interrupt status | left of the pointer band: `INT1/2/3` | each interrupt's state: `off / idle / wait / busy` | — (read-only) |
| 12 | Pointers | rows `RFxx / PTRA / PTRB` + hub bytes | the FIFO and PTRA/PTRB, with the hub bytes around each | click **PTRA**/**PTRB** to jump the hub viewer there |
| 13 | Cog status | dim stack: `INIT STALLI STR MOD LUTS` | miscellaneous cog-state flags, lit when active | — (read-only) |
| 14 | Pin states | rows `DIR / OUT / IN`, 64 bits each | pin direction, output, and live input for all 64 pins | — (read-only) |
| 15 | Smart-Pin Watch | one-row strip tagged `RQPIN` with a delta marker | smart pins whose `RQPIN` value changed | L-click = reset · R-click = reset **and** toggle the DIR-only/all-pins filter |
| 16 | Hub viewer | bottom band tagged `HUB`: address + hex + ASCII | shared hub RAM as hex and text | arrows/PgUp/PgDn/wheel to scroll; click a byte to jump |
| 17 | Hub heat map | colored block right of the hub data | recent hub read/write activity | click a bright spot to jump the hub viewer there |
| 18 | Break buttons & Go | bottom-right cluster around the big button | which break conditions are armed; run/step control | L-click a condition = set it exclusively · R-click = toggle · **Go**: SPACE / ENTER |
| 19 | Hint bar | very bottom edge (empty until you hover) | a one-line description of whatever you point at | hover any region to read what it is and how to use it |

> **The fastest way to learn the screen is region 19.** Hover the mouse over
> anything and the **hint bar** tells you what it is and what a click will do. If
> you remember only one thing from this chapter, remember that.

## The tour

The rest of the chapter walks the screen top-to-bottom, grouping regions the way
your eye does. Each stop says what the region is *for* and folds in the ways you
interact with it, so you learn "what this is" and "what I can do here" together.

### The status strip (regions 1–2)

The **title bar** names the window — *Debugger - Cog N* — so you always know
which cog you are looking at; when several cogs break, each opens its own window
and you tell them apart here.

Just below it, the **status strip** is the handful of values that define *where
you are*:

- **C** and **Z** — the carry and zero flags, as they stand after the highlighted
  instruction executes.
- **PC** — the Program Counter: the address of the next instruction. Click it to
  snap the disassembly back to the PC if you have scrolled away.
- **SKIPF** — the active skip pattern (or *Suspended during INTx* while an
  interrupt is running).
- **XBYTE** — the XBYTE bytecode-interpreter state.
- **CT** — the 64-bit system counter; it ticks constantly. Hover it and the hint
  bar reports the elapsed time in seconds.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=\linewidth]{inbox/assets/flags-pc-skipf-xbyte.png}
\caption{The status strip: C, Z, PC, SKIPF, XBYTE, and CT.}
\end{figure}
```

### The register maps — REG and LUT (regions 3–4)

Two tall columns run the full height of the left edge: **REG** is all 512 longs
of cog RAM ($000–$1FF), **LUT** is all 512 longs of LUT RAM ($200–$3FF). Both
carry the *heat-map* overlay — brighter cells are being read or written, darker
cells are quiet — so this is where you catch "something is hammering this
location." Click anywhere in either column to lock the disassembly to that
address and see the code living there.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[height=3.2in]{inbox/assets/reg-lut-heatmaps-tall.25.23.png}
\caption{The cog (REG) and LUT register heat-map columns.}
\end{figure}
```

### The disassembly (region 5)

The center of the window is your code, disassembled, with the **current PC line
highlighted** (white background, green text) so you always see what runs next.
This is where most of your attention lives. Three things happen right here:

- **Left-click** anywhere in the pane to lock it to *follow the PC* — handy after
  you have scrolled off looking around.
- **Right-click a line** to set or clear an **address breakpoint** there; a red
  marker appears at the left edge and the program stops when the PC reaches it.
- **Scroll** with the mouse wheel (hold **Ctrl** to move faster, **Shift** faster
  still). Scrolling detaches the pane from the PC until you left-click to re-lock.

You may see faint **strikethrough bands** across some upcoming lines: those are
the instructions the live SKIP pattern will skip. They shift as the pattern
changes — that is normal, not a rendering glitch.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=0.85\linewidth]{inbox/assets/dissassembly.png}
\caption{The disassembly; the highlighted line is the next instruction (the current PC).}
\end{figure}
```

### The watch cluster — Register Watch, Special registers, Event flags (regions 6–8)

To the right of the disassembly sit three stacked columns that update as you step.

The **Register Watch** (tagged `REG` with a small delta marker) builds itself: as you step, it lists the
cog registers whose values just changed, brightest for the freshest. You do not
curate it — it surfaces exactly what your stepping is touching. Press **R**, or
click the box, to clear it and start fresh. (Only ordinary registers $000–$1EF
appear here; the special registers show in the next column instead.)

The **Special registers** column lists the 16 special-function registers,
$1F0–$1FF, by name — the interrupt vectors, PA/PB, PTRA/PTRB, and the DIR/OUT/IN
pin registers. Click a **PTRA** or **PTRB** value to jump the hub viewer straight
to the address it holds. **INA/INB** are read-only — they mirror the live pins.

The **Event flags** column, at the far-right edge, lists the chip's hardware
events (`INT`, `CT1`, `CT2`, … `QMT`), each with a `0` or `1`. Beyond just
watching them, you can **click an event name to arm a break** on that event — the
matching button over in the control cluster lights up to confirm.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=\linewidth]{inbox/assets/watch-sfr-events.png}
\caption{The watch cluster: the Register Watch (tagged REG), the special registers, and the event flags.}
\end{figure}
```

### The state band — Execution mode, Call stack, Interrupt status, Pointers (regions 9–12)

A band across the middle reports how you got here and where your pointers aim.

- **Execution mode** reads `MAIN` normally, and flips to `INT1`/`INT2`/`INT3`
  while you are stopped inside an interrupt handler.
- The **Call stack** (`STACK`) shows the eight hardware CALL levels as hex return
  addresses. Click any value to jump the disassembly to that return address —
  the quickest way to see "who called me."
- **Interrupt status** shows `INT1/2/3` each as `off`, `idle`, `wait` (armed), or
  `busy` (its handler is running).
- **Pointers** shows the FIFO (`RFxx`) and `PTRA`/`PTRB`, each with a strip of the
  hub bytes around where it points. Click **PTRA** or **PTRB** to send the hub
  viewer there.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=\linewidth]{inbox/assets/state-band.png}
\caption{The state band: execution mode, the call stack, interrupt status, and the pointers.}
\end{figure}
```

### The cog-status and pin band (regions 13–14)

Below the state band, a dim stack of indicators — `INIT`, `STALLI`, `STR`,
`MOD`, `LUTS` — lights up when the corresponding cog-state condition is active
and stays dark otherwise.

Beside it, the **pin states** show three rows — `DIR`, `OUT`, `IN` — of 64 binary
digits each, split into two 32-bit halves. Bit 0 is the **rightmost** digit; the
right-hand half is pins 31–0 (the *A* registers) and the left-hand half is pins
63–32 (the *B* registers). `DIR` is direction (1 = output), `OUT` is the driven
level, and `IN` is what the pins actually read right now.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=\linewidth]{inbox/assets/status-pin-band.png}
\caption{The cog-status indicators and the DIR / OUT / IN pin rows.}
\end{figure}
```

### The Smart-Pin Watch (region 15)

A one-row strip tagged `RQPIN` with a delta marker, just under the pin rows, is the smart-pin
counterpart to the register watch: it lists the smart pins whose `RQPIN` result
changed as you step. **Left-click** it to reset the list; **right-click** resets
it *and* toggles between showing only configured pins and all pins.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=\linewidth]{inbox/assets/smart-strip.png}
\caption{The Smart-Pin Watch strip, tagged RQPIN with a delta marker.}
\end{figure}
```

### The hub viewer (regions 16–17)

The bottom band is the shared **hub** RAM: a 5-hex address, the hex bytes, and an
ASCII column, with a **heat map** to its right showing recent activity. Move
around with the arrow keys (one row, $10 bytes), PgUp/PgDn (a page, $80 — more
with Ctrl/Shift), or the scroll wheel; jump straight to a location by clicking a
byte, clicking a bright spot on the heat map, or clicking a pointer value
elsewhere on screen. You can also dial an address in by scrolling the wheel over
its individual hex digits.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=\linewidth]{inbox/assets/hub-viewer.png}
\caption{The hub-memory viewer: hex bytes, an ASCII column, and the activity heat map.}
\end{figure}
```

### The break buttons and Go (region 18)

The bottom-right cluster is your control panel. The small buttons arm the break
conditions (MAIN, the interrupts, DEBUG, INIT, an event, an address); **left-click**
one to make it the only armed condition, **right-click** to toggle it alongside
the others. The large **Go** button runs the program: press **SPACE** to go to
the next armed break, or **ENTER** to run continuously through breaks (press
ENTER again to stop). Chapters 5 and 6 cover these in full.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=1.6in]{inbox/assets/controls.png}
\caption{The break-condition buttons and the Go control.}
\end{figure}
```

## The one habit worth forming

Before you step, glance at three things: the **PC** (where am I), the **flags**
(C/Z), and the **Register Watch** (what just changed). After you step, glance
again and see what changed. That rhythm — look, step, look — is the whole craft.


# Chapter 4: Your First Session

Reading about the debugger only takes you so far. Let's drive it. This chapter
uses the small program from Chapter 2; type it in (or use your own) and follow
along.

```spin2
PUB main() | a, b, sum
  a := 10
  b := 32
  ' argument-less: single-step debugger opens here
  DEBUG
  sum := add_two(a, b)
  ' has arguments: display output only, no break
  DEBUG("sum = ", UDEC_(sum))

PRI add_two(x, y) : result
  result := x + y
```

**1. Compile with debugging and run it.**

```command
pnut_ts -d firststep.spin2
```

Launch it from `pnut_term_ts`. The program runs until it reaches the
argument-less `DEBUG`, then the single-step debugger window appears and execution
pauses. (The second statement, `DEBUG("sum = ", UDEC_(sum))`, has arguments, so it only
prints to the display windows — it will not stop here.) Your program is now
waiting for you.

**2. Get oriented.** Find the **disassembly** pane and the highlighted current
line — that is your PC. Glance at the **C** and **Z** flags in the status strip.
Nothing has gone wrong; the chip is simply holding still.

**3. Take one step.** Press **Space**. Exactly one instruction executes, and the
debugger stops again. Watch the highlighted line in the disassembly move, and
watch the PC change in the status strip. You just executed a single instruction
by hand. (Space really means "run to the next armed break"; because the default
armed condition is MAIN, that works out to one instruction per press. You will
meet the other break conditions in Chapter 6.)

**4. Watch the values change.** As you step toward `add_two`, keep an eye on the
**Register Watch** pane: the debugger lists registers automatically as they
change, so the result register shows up there on the step that writes it. Step
through the addition and watch the value land — you are seeing the computation
happen one instruction at a time.

**5. Resume.** Press **Enter** to let the program run again. It
continues to the second `DEBUG`, prints `sum = 42`, and finishes.

That is a complete debug session: **stop, look, step, look, resume.** Everything
else in this manual builds on those five moves.

> Try this: run it again, and this time keep stepping *into* `add_two` instead of
> resuming. Watch the call stack pane gain a level as you enter the method and
> lose it as you return. That is the call stack tracking you will use to find
> your way through nested code.


# Chapter 5: Command Reference

Chapter 3 introduced these controls where they live, region by region. This
chapter gathers them into one place to look up. They are the same whether you
reached the debugger from a Spin2 `DEBUG`, a PASM `debug`, or a cog start.

## Keyboard commands

| Key | Action | What it does |
|-----|--------|--------------|
| **Space** | Go to next break | Run to the next armed break (same as left-clicking **Go**); with MAIN armed, that is one instruction per press |
| **Enter** | Run / stop | Run continuously through breaks; press again to stop (same as right-clicking **Go**) |
| **B** | BREAK mode | Click the **BREAK** button — async-break mode; clears the other conditions |
| **D** | DEBUG toggle | Toggle break-on-`DEBUG` |
| **I** | INIT toggle | Toggle break-on-COGINIT |
| **M** | MAIN toggle | Toggle break-on-MAIN (single-step main code) |
| **R** | Reset watch | Clear the register watch list |
| **↑ / ↓** | Hub scroll | Scroll the hub data viewer one row (±$10) |
| **PgUp / PgDn** | Hub page | Page the hub data viewer ($80 per press; $1000 with Ctrl, $10000 with Shift) |

> **No key switches between cogs.** Each cog that hits a breakpoint opens its
> **own window**, titled *Debugger - Cog N*; the windows cascade on screen as
> they open. To work on a different cog, switch to its window. (The Tab key is
> intentionally inert inside the debugger window.)

## Mouse controls

- **Left-click a button** — activate that function.
- **Right-click a mode button** — toggle its state.
- **Left-click a value** (register, SFR, stack entry, or pointer) — jump the
  disassembly or hub viewer to the address it holds.
- **Right-click a disassembly line** — set or clear an address breakpoint there.
- **Scroll wheel** — move through the hub viewer or the disassembly.


# Chapter 6: Breakpoints

A breakpoint is how you tell the program "stop when you get here" so you do not
have to single-step from the very beginning. The P2 debugger supports several
kinds at once.

## The kinds of breakpoint

A break-condition register controls which conditions are armed:

| Condition | Stops when… |
|-----------|-------------|
| **MAIN** | main code executes |
| **INT1 / INT2 / INT3** | the corresponding interrupt fires |
| **DEBUG** | a `DEBUG` statement or `debug` instruction is reached |
| **INIT** | a cog starts (COGINIT) |
| **EVENT** | a selected event triggers |
| **ADDR** | execution reaches a chosen address |
| **COGBRK** | another cog requests an asynchronous break |

You arm and disarm these with the condition buttons in the bottom-right cluster.
**Left-click** a button to set that condition exclusively; **right-click** to
toggle it without disturbing the others. Three of them also have keyboard toggles
from Chapter 5 — **D** (DEBUG), **I** (INIT), and **M** (MAIN). An armed condition
shows bright, a disarmed one dim — there is no numeric "break value" on screen, so
the button brightness *is* your confirmation of what is armed.

## Breaking on an event

There is no button labeled "EVENT." Instead you choose *which* event in the
event-flags column (region 8, far-right edge): **click the event's name** — `CT1`,
say — and it arms as the break event. Its button in the cluster then lights,
showing the event name with an up-arrow (for example `CT1`↑), which is your
confirmation the event break is armed. With an event armed, pressing **Space**
runs the program freely until that event fires, then breaks once — so a single
Space here can cover many instructions, unlike the one-instruction step you get
with MAIN armed.

## Setting an address breakpoint

To stop when execution reaches a specific instruction, **right-click that line in
the disassembly pane**. A marker appears on the line, and the program pauses when
the PC reaches that address; right-click the line again to clear it. If the line
you want is not on screen, scroll the disassembly to it first (mouse wheel, or
click a pointer/stack value that lands there).

## Conditional breakpoints in code

You can make a breakpoint fire only when a condition holds by guarding an
argument-less `DEBUG` with an ordinary `if`:

```spin2
if value > 100
  DEBUG                 ' single-step debugger opens only when value > 100
```

The debugger appears only on the iterations where `value > 100` — far more useful
than stopping every time when you are hunting an occasional case. Use the bare
`DEBUG` here: a `DEBUG` with arguments inside (such as `DEBUG(UDEC(value))`)
would send output to the display windows instead of breaking.

## Asynchronous break between cogs (COGBRK)

One cog can break another. Enable **BREAK** mode (press **B**) in the cog you
want to be interruptible; the break can then be fired across to it while you are
stopped in another cog's debugger. This is how you stop a misbehaving worker cog
— essential for multi-cog debugging (Chapter 8).

You can see when a cog is a candidate for this. A cog running free and not
hitting any break gradually **dims**, and its **Go** button changes to read
**Break**: that is the debugger telling you "this cog is running loose — click to
force an asynchronous break." One limitation to remember: an asynchronous break
only lands while some *other* cog is already sitting in its own debugger.


# Chapter 7: Observing State

The reason to pause is to look. This chapter covers what you can inspect and how.

## Memory

**Cog memory ($000 – $1FF).** 512 longs of cog RAM — your registers and code.
The heat map shows read/write activity, and the **Register Watch** pane lists
locations automatically as they change.

**LUT memory ($200 – $3FF).** 512 longs of lookup-table RAM, shared between cog
pairs (0–1, 2–3, 4–5, 6–7) and often used for fast data.

**Hub memory.** The shared RAM, shown as hex with an ASCII column. Navigate with
the arrow keys (up/down one row, $10 bytes), PgUp/PgDn (by page), the scroll
wheel, or by clicking the hub heat-map or a pointer value to jump straight to a
location. You can also dial an address in by scrolling the wheel over its hex
digits.

## Registers and the special-function registers

The special-function registers occupy the top of cog memory. Grouped by function,
they are the interrupt vectors, the pointer/parameter registers, and the I/O
registers:

```{=latex}
\SpecialRegistersMapDiagram
```

The table below gives each register's read/write access — the detail you act on at
the debugger:

| Register | Address | R/W | Purpose |
|----------|---------|-----|---------|
| IJMP3 | $1F0 | R/W | INT3 jump vector |
| IRET3 | $1F1 | R/W | INT3 return address |
| IJMP2 | $1F2 | R/W | INT2 jump vector |
| IRET2 | $1F3 | R/W | INT2 return address |
| IJMP1 | $1F4 | R/W | INT1 jump vector |
| IRET1 | $1F5 | R/W | INT1 return address |
| PA | $1F6 | R/W | Port A scratch / call argument |
| PB | $1F7 | R/W | Port B scratch / call argument |
| PTRA | $1F8 | R/W | Pointer A |
| PTRB | $1F9 | R/W | Pointer B |
| DIRA | $1FA | R/W | Direction register — pins 0–31 |
| DIRB | $1FB | R/W | Direction register — pins 32–63 |
| OUTA | $1FC | R/W | Output register — pins 0–31 |
| OUTB | $1FD | R/W | Output register — pins 32–63 |
| INA | $1FE | R | Input register — pins 0–31 (read-only) |
| INB | $1FF | R | Input register — pins 32–63 (read-only) |

In the debugger these appear in the **SFR** group: you watch them update as you
step; **INA/INB** are read-only (they mirror the live pins), and clicking a
**PTRA**/**PTRB** value jumps the hub viewer to that address.

The P2's 64 I/O pins are split into two banks of 32, and each of these registers
covers one bank: the **A** registers (DIRA/OUTA/INA) address pins **0–31**, and
the **B** registers (DIRB/OUTB/INB) address pins **32–63**. Within a register,
bit *N* is the pin at that position in its bank — so DIRA bit 0 is pin 0, while
DIRB bit 0 is pin 32 and DIRB bit 31 is pin 63. In the direction registers a bit
of 1 makes the pin an output and 0 makes it an input. So when you are watching a
pin, pick the register for its bank and read the bit at the pin's position within
that bank (pin 40, for example, is DIRB/OUTB/INB bit 8).

## The watch list

The watch list builds itself: as you step, the debugger lists the registers
whose values just changed (up to 16 at once), brightening the freshest and
fading them as they go quiet. You do not curate it — it surfaces exactly the
activity you are stepping through. Press **R** (or click the watch pane) to clear
it and start fresh; a parallel list does the same for smart pins.

The watch tracks the ordinary cog registers, $000–$1EF. The 16 special-function
registers above that ($1F0–$1FF — PA, PB, PTRA/PTRB, the interrupt vectors, the
pin registers) never appear in the watch; you read those in the **SFR** column
instead. So if you are watching for a change to, say, PTRA and the watch stays
empty, that is expected — look to the SFR column for it.

## The call stack

The stack pane shows up to eight levels of the hardware CALL stack with their
return addresses, and the disassembly indicates call depth — together they tell
you how you got to where you are.

## Smart pins and events

You can view smart-pin configuration and state to confirm a peripheral is set up
the way you intended, and watch the chip's event flags (interrupts, counter
matches, streamer events, pattern matches, and so on) to see which events are
firing.

## Reading the heat map

The heat-map overlay turns raw access into a picture: brighter/warmer cells are
being written or read heavily, darker cells are quiet. A location lighting up
when you did not expect it is often your bug.


# Chapter 8: Working Sessions

With the moves and the panes in hand, here are the tasks you will actually use
the debugger for.

## PASM-level debugging

Drop a `debug` instruction wherever you want assembly execution to pause, then
single-step and watch registers and flags change instruction by instruction:

```pasm2
              org       0
              mov       a, b
              debug                     ' pause and inspect
              add       a, #1
              debug
a             res       1
b             res       1
```

This instruction-by-instruction view is the most direct way to understand what a
piece of PASM really does to the machine.

## Multi-cog debugging

Each cog is debugged independently, and **each cog that breaks gets its own
window** — titled *Debugger - Cog N*. To look at a different cog, switch to its
window (the windows cascade on screen as they open). Because the cogs run in
parallel, you typically arm breakpoints in each cog of interest and use COGBRK
(Chapter 6) to coordinate stopping them.

A cog's window appears only once that cog actually exists and breaks. In the
example below, the download stops `main` at its first instruction — *before* the
`COGSPIN` — so at first you see only the *Cog 0* window. Step or run `main`
through the `COGSPIN`, and the blink cog launches, hits its own `DEBUG`, and its
window opens then. Do not expect the second window before the cog that owns it
has started.

```spin2
VAR
  long stack[64]

PUB main()
  ' break in main; the debugger opens here
  DEBUG
  COGSPIN(NEWCOG, blink(56, 5_000_000), @stack[0])
  repeat
    waitms(1000)

PRI blink(pin, half) | t
  t := GETCT()
  repeat
    ' break in the blink COG (opens its own window)
    DEBUG
    PINTOGGLE(pin)
    t += half
    waitct(t)
```

Note the P2 idioms: **`COGSPIN`** to start the cog and **`GETCT`** / `waitct` for
timing. Both breakpoints are *argument-less* `DEBUG` statements — only that form
opens the single-step debugger. The blink cog opens in **its own window**
(*Debugger - Cog N*); switch to that window to step through it on its own while
`main` keeps running.

## Finding memory corruption

When a value is being clobbered and you do not know by whom, lean on the heat
maps. The debugger has no data watchpoint, but it *colors* every read and write:

1. Keep the cog/LUT heat-map columns (or the hub heat-map) in view and step or
   run between breakpoints, watching for write activity on the affected location.
2. Watch the surrounding locations too — corruption often spills across
   neighbors.
3. Once you suspect *which* instruction is doing the writing, set an address
   breakpoint on it (right-click it in the disassembly) to stop there and catch
   the culprit in the act.

## Debugging interrupts

1. Arm the relevant interrupt breakpoint by clicking the **INT1**, **INT2**, or
   **INT3** button (alongside MAIN, so you can step up to the interrupt). When it
   fires, the **Execution mode** indicator flips from `MAIN` to `INT1`/`INT2`/`INT3`
   — that is how you know you are now stopped *inside* the handler.
2. Check the interrupt vectors in the SFR column (IJMPx / IRETx), and the
   **Interrupt status** region to see each interrupt as `wait` (armed) or `busy`
   (its handler running).
3. Watch the event flags to confirm which event drove the interrupt.

While you are inside a handler, the **SKIPF** panel reads *Suspended during INTx*
rather than a skip pattern — a reminder that any skip sequence is paused for the
duration of the interrupt. It clears when you step out through the return.

## Timing and performance

Use the **CT** system counter to measure how long a section takes: note CT,
run the section, note CT again. Because single-stepping itself is slow, measure
timing by running between breakpoints, not by stepping.


# Chapter 9: DEBUG Display Windows (Cross-Reference)

Beyond the single-step debugger, the P2 can stream live data to a set of
graphical **DEBUG display windows** — a serial terminal, a logic analyzer, an
oscilloscope, an XY scope, a plot, an FFT spectrum view, a bitmap display, and a
MIDI view — all hosted in `pnut_term_ts` alongside the debugger.

Those windows are a large topic with their own commands and workflows, and they
are covered in depth in the **P2 Debug Window Manual**. This manual stays focused
on single-step debugging; when you want real-time plotting and visualization,
turn to that manual.

What is worth knowing here: the same `DEBUG` statement that can pause execution
can also send formatted output. When you display a value, use the P2's output
formatters — `UDEC`, `SDEC`, `UHEX`, `SHEX`, `UBIN` — each with an optional
trailing underscore (`UDEC_`, `UHEX_`, …) that suppresses the automatic label
when you have already written your own:

```spin2
DEBUG("count = ", UDEC_(count))     ' prints: count = 42
DEBUG(UDEC(count))                  ' prints: count = 42  (auto label)
```


# Chapter 10: Tips and Troubleshooting

## Working effectively

- **Start small.** A single breakpoint and the step key will solve most problems
  before you need anything fancier.
- **Let the watch list work for you.** It auto-surfaces the registers that just
  changed — read it as a running summary of what your stepping is touching, and
  press **R** to clear it when you want a fresh slate.
- **Let the heat map point you.** Unexpected activity is a fast way to localize a
  bug you cannot otherwise see.
- **Use COGBRK for parallel bugs.** Coordinated stopping is the key to making
  sense of multi-cog behavior.

## Troubleshooting

| Symptom | Likely cause / fix |
|---------|--------------------|
| Debugger never appears | Did you compile with `pnut_ts -d`? Without `-d`, DEBUG is stripped. |
| A cog will not respond | It may be stalled; check whether it is waiting (e.g. on an event or `waitct`). |
| Lost in hub memory | Click the hub heat-map to jump, or dial the address in with the scroll wheel. |
| A breakpoint never hits | Re-check the address and that the matching condition (ADDR/DEBUG/INT…) is armed. |
| One **Space** advanced *two* instructions | The first was an `AUGS`/`AUGD` prefix (emitted for a `##` 32-bit immediate). The prefix and the instruction it augments are atomic — the debugger cannot break between them — so one Space steps past both. This is correct, not a stuck key. |
| The Register Watch stays empty for a special register | PA, PB, PTRA/PTRB, and the pin/vector registers ($1F0–$1FF) never show in the watch — read them in the SFR column (Chapter 7). |


# Appendix A: Feature Availability by Version

The single-step debugger and its capabilities arrived over several P2 toolchain
releases. If a feature below is missing for you, your toolchain predates it. For
current work, use the latest release; everything in this manual is available
there.

| Capability | Available since |
|------------|-----------------|
| PASM-level single-step debugging, breakpoints | v35u |
| Broad P2 hardware compatibility | v35v |
| Robust exception handling / stability | v35g |
| Automatic clock-frequency adaptation; flash-debug support | v36 |
| Advanced multi-cog debugging | v36 |
| Auto-triggering scope displays | v41 |
| Complete feature set | v51 and later |

> Note: this manual documents the debugger as delivered in the current
> environment — compiled with `pnut_ts` and hosted in `pnut_term_ts` — where the
> interaction model is carried forward unchanged from the original P2 single-step
> debugger.
