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

### A Cog starting up

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
Cog's bit turns debugging off for that cog, so it never produces DEBUG output
and the debugger never breaks in it — leaving you with only the cogs you actually
care about. (`DEBUG_COGINIT` is the
compile-time equivalent of the INIT breakpoint you will arm by hand in
Chapter 6.)

## What "with debugging enabled" costs

Debugging adds a small amount of code and RAM per cog so the chip can talk to
the host. For a finished release you simply compile without `-d` and the
overhead is gone.


# Chapter 3: Orientation — The Debugger Window

When the debugger opens, you are looking at the full live state of one cog at
once. It can feel busy at first. This chapter names each area and tells you what
it is *for*; you do not need to memorize it — just know where to look.

The window is a fixed character grid divided into panes. Figure 3-1 shows the
whole window; the rest of this chapter walks through each pane in turn.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=\linewidth]{inbox/assets/ssdb-fullScreen.png}
\caption{The single-step debugger window (debugging Cog 0).}
\end{figure}
```

## The panes

**Cog / LUT register maps (left edge).** Two tall columns down the left of the
window: all cog registers ($000 – $1FF) under **REG**, and all LUT registers
($200 – $3FF) under **LUT**, with the heat-map overlay showing read/write
activity. This is where you spot "something is hammering this location" — in the
figure below, the brighter band marks recently-touched LUT locations while the
darker stretches have been quiet. Because these columns run the full height of
the window, they are shown on their own here.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[height=3.2in]{inbox/assets/reg-lut-heatmaps-tall.25.23.png}
\caption{COG (REG) and LUT register heat-map columns.}
\end{figure}
```

**Control registers (top strip).** Across the top of the window, the handful of
values that define *where you are*:

- **C** and **Z** — the carry and zero flags.
- **PC** — the Program Counter: the address of the next instruction.
- **SKIPF** — the skip pattern, if a skip sequence is active.
- **XBYTE** — the XBYTE interpreter state.
- **CT** — the 64-bit system counter.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=\linewidth]{inbox/assets/flags-pc-skipf-xbyte.png}
\caption{The control-register strip: C, Z, PC, SKIPF, XBYTE, and CT.}
\end{figure}
```

**Disassembly (middle).** Your code, disassembled, with the current PC line
highlighted so you always see what executes next. Breakpoint markers and call
depth show here too.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=0.85\linewidth]{inbox/assets/dissassembly.png}
\caption{The disassembly pane; the highlighted line is the next instruction (the current PC).}
\end{figure}
```

**Watch windows (middle-right).** A **Register Watch** that automatically lists
the registers changing as you step, the **SFR** group for the special function
registers, and an **Events** view for event flags.

**Stack display (bottom-middle).** The eight-level hardware call stack and the
PTRA / PTRB pointer values.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=\linewidth]{inbox/assets/stack.png}
\caption{The hardware call stack: eight long values.}
\end{figure}
```

**Hub memory viewer (right).** Shared RAM shown as hexadecimal with an ASCII
column alongside, plus a mini-map for jumping around quickly.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=\linewidth]{inbox/assets/hub-viewer.png}
\caption{The hub-memory viewer: hex bytes, an ASCII column, and a navigation mini-map.}
\end{figure}
```

**Control buttons (bottom-right).** Mode selectors and the GO / STOP control,
clickable with the mouse.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=1.6in]{inbox/assets/controls.png}
\caption{The control buttons: breakpoint mode toggles and the GO/STOP control.}
\end{figure}
```

## The one habit worth forming

Before you step, glance at three things: the **PC** (where am I), the **flags**
(C/Z), and the **watch** list (the registers that just changed). After
you step, glance again and see what changed. That rhythm — look, step, look — is
the whole craft.


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
line — that is your PC. Glance at the **C** and **Z** flags in the control
registers. Nothing has gone wrong; the chip is simply holding still.

**3. Take one step.** Press **Space**. Exactly one instruction executes, and the
debugger stops again. Watch the highlighted line in the disassembly move, and
watch the PC change in the control registers. You just executed a single
instruction by hand.

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


# Chapter 5: Commands and Controls

These are the controls that drive a session. They are the same whether you
reached the debugger from a Spin2 `DEBUG`, a PASM `debug`, or a cog start.

## Keyboard commands

| Key | Action | What it does |
|-----|--------|--------------|
| **Space** | Single-step | Execute one instruction (same as left-clicking **Go**) |
| **Enter** | Run / stop | Toggle continuous execution (same as right-clicking **Go**) |
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
| **INIT** | a Cog starts (COGINIT) |
| **EVENT** | a selected event triggers |
| **ADDR** | execution reaches a chosen address |
| **COGBRK** | another Cog requests an asynchronous break |

You arm and disarm these with the condition buttons. **Left-click** a button to
set that condition exclusively; **right-click** to toggle it without disturbing
the others. Three of them also have keyboard toggles from Chapter 5 — **D**
(DEBUG), **I** (INIT), and **M** (MAIN).

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

## Asynchronous break between Cogs (COGBRK)

One cog can break another. Enable **BREAK** mode (press **B**) in the cog you
want to be interruptible; the break can then be fired across to it while you are
stopped in another cog's debugger. This is how you stop a misbehaving worker cog
— essential for multi-cog debugging (Chapter 8). One limitation to remember: an
asynchronous break only lands while some cog is already sitting in its own
debugger.


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

## Multi-Cog debugging

Each cog is debugged independently, and **each cog that breaks gets its own
window** — titled *Debugger - Cog N*. To look at a different cog, switch to its
window (the windows cascade on screen as they open). Because the cogs run in
parallel, you typically arm breakpoints in each cog of interest and use COGBRK
(Chapter 6) to coordinate stopping them.

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
   **INT3** button.
2. When it fires, check the interrupt vectors in the SFR group (IJMPx / IRETx).
3. Watch the event flags to confirm which event drove the interrupt.

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
| A Cog will not respond | It may be stalled; check whether it is waiting (e.g. on an event or `waitct`). |
| Lost in hub memory | Click the hub heat-map to jump, or dial the address in with the scroll wheel. |
| A breakpoint never hits | Re-check the address and that the matching condition (ADDR/DEBUG/INT…) is armed. |


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
| Advanced multi-Cog debugging | v36 |
| Auto-triggering scope displays | v41 |
| Complete feature set | v51 and later |

> Note: this manual documents the debugger as delivered in the current
> environment — compiled with `pnut_ts` and hosted in `pnut_term_ts` — where the
> interaction model is carried forward unchanged from the original P2 single-step
> debugger.
