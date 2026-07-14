# Chapter 1: The DEBUG Display Windows {#ch-1}

The P2 gives you nine kinds of on-screen window that draw the data your program
sends. You do not wire up a display or write a rendering loop. You add a
`DEBUG()` statement to your code; when the program runs, a window opens on the
host PC and shows what you sent — text in a terminal, a trace on an oscilloscope,
a spectrum, a piano keyboard. These are the **DEBUG display windows**, and this
chapter is the shared model that every later chapter builds on.

The job of these windows is to make data you already have visible. A variable
that holds a sensor reading is hard to interpret as a printed number scrolling by;
fed to a SCOPE window it becomes a waveform you can read at a glance. A stream of
bytes is hard to follow; fed to a LOGIC window it becomes channels you can watch.
You choose the window that matches the shape of your data, send the data, and read
the result.

This chapter teaches one model that applies to all nine windows: how you create a
window, how you feed it, and how the feed stream is interpreted. Once you have
that, each per-window chapter is just the specifics — which configuration keywords
that window takes, what its data means, and which commands it adds. Read this
chapter first; then go to the chapter for the window you need.

## The nine windows

Every DEBUG display window is one of nine types. Each has a dedicated chapter that
documents all of its configuration keywords, data formats, and commands. Pick the
window that matches the shape of your data:

| Window | What it shows | Chapter |
|--------|---------------|---------|
| **TERM** | A scrolling text terminal — status lines, variable dumps, logs | [Ch 3](#ch-3) |
| **BITMAP** | A pixel raster you draw into directly, framebuffer-style | [Ch 4](#ch-4) |
| **PLOT** | An XY plotting surface with layered drawing and sprites | [Ch 5](#ch-5) |
| **LOGIC** | A logic-analyzer trace of 1–32 digital channels | [Ch 6](#ch-6) |
| **SCOPE** | A time-domain oscilloscope of 1–8 sampled values | [Ch 7](#ch-7) |
| **SCOPE_XY** | An XY (Lissajous / phase) scope | [Ch 8](#ch-8) |
| **FFT** | A frequency-domain spectrum | [Ch 9](#ch-9) |
| **SPECTRO** | A spectrogram — frequency content over time | [Ch 10](#ch-10) |
| **MIDI** | A piano-keyboard display driven by MIDI note messages | [Ch 11](#ch-11) |

These nine are the complete set the tool implements. Up to 32 display windows can
run at the same time, so a single program can drive a terminal, a scope, and a
plot together.

### Which window for which problem

When you know the *kind* of data — or the question you are trying to answer — this
maps it to the window to reach for:

| You want to see… | Reach for | Chapter |
|------------------|-----------|---------|
| Text — status lines, logs, variable dumps | TERM | 3 |
| A raw pixel image or framebuffer | BITMAP | 4 |
| A custom instrument, gauge, or drawn UI | PLOT | 5 |
| Several digital signals and their timing | LOGIC | 6 |
| A value changing over time (a waveform) | SCOPE | 7 |
| The relationship between two values (phase, Lissajous) | SCOPE_XY | 8 |
| The frequency content of a signal | FFT | 9 |
| How frequency content evolves over time | SPECTRO | 10 |
| MIDI note activity on a keyboard | MIDI | 11 |

## Create by name, feed by name

You work with a window in two steps. **First you create it; then you feed it.**

You create a window with a `DEBUG()` statement whose feed string begins with a
backtick, a window type, and a name you choose:

```spin2
DEBUG(`TERM Status SIZE 40 20)
```

The backtick (`` ` ``) marks the start of a display feed. `TERM` is the window
type. `Status` is the name — you invent it, and it must be unique among your
windows. Everything after the name configures the window; here `SIZE 40 20` makes
it a 40-column by 20-row terminal. One `DEBUG()` statement like this creates one
window.

From then on you address that window **by its name**, not by its type:

```spin2
DEBUG(`Status 'Ready.')
```

The name is the whole interface. The first statement said "make a TERM window and
call it `Status`"; the second says "send this to `Status`." You can feed the same
window from many places in your program, and you can feed two windows the same data
by naming both. A complete minimal program:

```{.spin2 caption="ch01-getting-started-term.spin2"}
CON _clkfreq = 200_000_000

PUB main()
  debug(`TERM Status SIZE 40 20)   ' create a window named "Status"
  debug(`Status 'Ready.')          ' feed it by name
  repeat                           ' keep the program (and window) alive
```

Compile this with `pnut_ts -d` ([Chapter 2](#ch-2) covers the setup) and a 40×20 terminal
named `Status` opens and shows `Ready.`. The final `repeat` matters: when a P2
program ends, it stops sending, so keep the program running while you want to watch
the window.

## The feed stream is a sequence of elements

Everything after the window name — on the creation line and on every feed
afterward — is a **feed stream**: a sequence of *elements* that the window reads
left to right. The display parser recognizes a few element types, and the
distinction between two of them is the single most important thing in this manual.

The element types are:

- **Keywords** — bare words like `SIZE`, `TITLE`, `POS`, `CLEAR`. These configure
  the window or issue a named command. Each window's chapter lists the keywords it
  understands.
- **Strings** — display text in **single** quotes, such as `'Sawtooth'` or
  `'Ready.'`. A single-quoted string is shown literally. Use single quotes for
  display text: a **double**-quoted string in a backtick display feed compiles but
  is silently dropped at runtime — the window shows nothing. (Double quotes remain
  valid inside a `` `(expr) `` substitution, which is ordinary Spin2.)
- **Numbers** — written in decimal, hex (`$FF`), or binary (`%1010`). What a number
  *means* depends on context, and that is the rule you must internalize.

### Values versus command codes

A number in the feed stream is interpreted one of two ways, and you control which:

- A number put into the stream as **display text** shows as its digits. In a TERM
  you do this with a `` `(value) `` substitution inside single-quoted text:
  `` `(x) `` is signed decimal, `` `$(x) `` hex, `` `%(x) `` binary, `` `.(x) ``
  floating point, `` `?(x) `` boolean (printing `TRUE` or `FALSE`), and `` `#(x) ``
  sends the character whose code is `x`. If `x` holds 25, then a `` `(x) ``
  substitution inside single-quoted text shows the two characters `2` and `5`.

  These punctuation forms are shorthands for the long-named formatters:
  `` `(x) `` is `SDEC_`, `` `.(x) `` is `FDEC_`, and `` `?(x) `` is `BOOL_`. Use
  whichever reads better — they compile to the same thing.

  The value-only `DEBUG()` formatters you use for serial output — `` `udec_(x) ``,
  `` `uhex_(x) ``, `` `sdec_(x) ``, and so on — also put a value in the stream, but
  as a **numeric data element**: the form the graphing windows (SCOPE, LOGIC, FFT)
  consume as a data point. Send one to a **TERM** and it renders as a single
  **character glyph** (value 42 prints `*`, not `42`), not as digits. So in a TERM,
  display a value's text with `` `(value) `` substitution — not `` `udec_ ``.
- A **bare number** — one not wrapped in a formatter or substitution — is *raw
  input* the window interprets in its own way: in a TERM window it is a **command
  code** (cursor, color, and control); in the graphing windows it is a **data
  value** (a sample to plot). Either way it is not shown as the literal digits.

This is why a terminal treats a bare `13` as a newline rather than printing the
digits "13": `13` is the newline command code. To show the number thirteen as text,
put it inside single-quoted text — `` debug(`Status '`(13)') `` — or write the
literal string `'13'`. Carry this rule into every chapter:

> **To display a number, format it. Send it bare and the window takes it as raw
> input** — a command code in TERM, a plotted data value in the graphing windows.
> In a TERM, a `` `(temp) `` substitution inside single-quoted text shows the value
> of `temp`; a bare `13` is a command code,
> not the text "13".

Each window assigns its own meaning to its command codes and to its raw data
values — what a number does in a TERM window (cursor and color control) is not what
it does in a SCOPE window (a sample value). Those meanings are documented in the
per-window chapters. The element model — keywords, strings, formatted values,
and bare command numbers — is the same everywhere.

## Configuration versus commands

Within that element model, the keywords a window understands fall into three
groups — the distinction the per-window chapters and the command reference
([Appendix A](#appendix-a)) are organized around:

- **Creation-line configuration** sets the window up once, on the
  `` DEBUG(`TYPE Name ...) `` line that creates it — `SIZE`, `TITLE`, `POS`, and
  the rest. Most cannot be changed once the window exists.
- **Runtime commands** are sent *after* creation, in later feeds, to change the
  window's state or act on it: `COLOR` and `SET` on PLOT, `TRIGGER` on SCOPE, and
  so on. A few keywords are runtime-only and must not appear on the creation line;
  each window's chapter flags which.
- **Shared commands** are the handful every window understands, covered just below.

A window opens when its creation `DEBUG()` runs and stays open as long as your
program keeps running. You can dismiss one explicitly with the shared `` `CLOSE ``
command (below), but most programs never need to — when the program ends it stops
feeding and the window stops updating, which is why the examples end in a
`repeat`, to keep the program, and its windows, alive.

## Commands common across windows

Most windows share a small set of named-keyword commands. You send them by name,
after the window name, the same way you send data:

- **`CLEAR`** — clear the window's contents and reset it to wait for new data.
- **`SAVE`** — save the window's current image to a file on the host. Most windows
  accept `SAVE 'filename'`, and optionally `SAVE WINDOW 'filename'` to capture the
  whole window rather than just the display area. The file is a `.bmp`; the
  extension is appended automatically, so give the name *without* it (`'scope'`,
  not `'scope.bmp'`). **`SAVE` has four traps — read the box below before you use it.**
- **`CLOSE`** — close one window and free it. Most programs never need this — a
  window also stops when the program stops feeding it — but `` `CLOSE `` lets you
  dismiss a single window explicitly while the rest of the program keeps running.
  `CLOSE` is a command only (it takes no arguments), it accepts more than one window
  name in a message, and it runs **after** the rest of that message — so
  `` `Win SAVE 'shot' CLOSE `` saves *and then* closes, in that order. Closing a
  window gives back one of the **32 display slots** the debug system has to hand out.
- **`UPDATE`** — control buffered repainting. A window placed in update mode (by
  adding `UPDATE` to its creation line) does not redraw as data arrives; it
  repaints only when you feed it the `UPDATE` command. This prevents flicker when
  you redraw a whole display at once. Not every window supports buffered mode — its
  chapter says whether it does.
- **`PC_KEY`** and **`PC_MOUSE`** — read the host keyboard and mouse back into your
  program, so a window can be interactive. These work across window types and share
  one mechanism, so they are covered together in [Chapter 12](#ch-12).

Each window also has commands of its own — `TRIGGER` and `HOLDOFF` on SCOPE and
LOGIC, the drawing commands on PLOT, and so on. Those belong to the window and are
documented in its chapter.

### The four `SAVE` traps

`SAVE` writes a file and tells you nothing about how it went. All four of these
failures are silent, and all four have been confirmed on hardware:

1. **No filename, no file.** The filename is *required*. A bare `` `Win SAVE ``
   writes nothing at all — no file, no error, no warning. It simply does not happen.
2. **A keyword after `SAVE` is eaten.** The filename must be the **last** thing in the
   message. Anything you put after `SAVE` other than a filename is consumed and
   discarded — `` `Win SAVE CLEAR `` writes no file **and** does not clear the window.
   You lose both commands.
3. **In buffered mode you save the *previous* frame.** `SAVE` captures the front
   buffer — what is on screen — not the drawing you have accumulated off-screen.
   Under `UPDATE` mode, send `` `UPDATE `` *before* `SAVE`, or you will file the frame
   before the one you meant.
4. **`SAVE WINDOW` scrapes the desktop.** The plain form renders the display area from
   the window's own bitmap, but `SAVE WINDOW` copies the region of the *screen* the
   window occupies — so anything overlapping it gets captured too. Keep the window
   unobscured, or prefer the plain form.

Trap 1 and trap 3 are the ones that waste an afternoon: in both cases the program
runs, the file appears (or doesn't) without complaint, and the picture you get is a
plausible one — just not the picture you asked for.

> **Prefer the plain `SAVE 'name'` form.** It renders from the window's own buffer, so
> it captures exactly your window's contents and nothing else. The two forms that
> capture the *screen* instead — `SAVE WINDOW`, and the `SAVE left top width height`
> region form — go through the host's screen-capture path, which brings in whatever is
> on screen at the time. On PNut that path is **currently unreliable**: it can return a
> truncated or offset rectangle, a neighboring window, or bare desktop. That is a tool
> bug, reported upstream. The plain form was correct in every case we exercised.

### Ending a debug session

`` `CLOSE `` dismisses one window. `DEBUG_END_SESSION` ends the **whole session** —
it is the global counterpart, and it is not a window command but a `DEBUG()`
statement of its own:

```spin2
{Spin2_v52}                ' must be the FIRST line of the file

PUB main()
  ' ... your program ...
  debug(DEBUG_END_SESSION) ' close every window and the log file
```

Executing it closes any open DEBUG windows *and* the `DEBUG.LOG` file, and **your P2
program keeps running**. It exists chiefly so that a run can signal "the output is
complete": the log file is closed and flushed, which is what lets a script — or an AI
coding assistant — know the results are ready to read rather than still being written.

`DEBUG_END_SESSION` was added in Spin2 v52, and it is **version-gated**: without
`{Spin2_v52}` (or later) as the literal first line of your source file, the compiler
does not know the symbol and the build fails with an expression error.

## How these differ from the single-step debugger

The P2 debug system has two faces, and this manual covers only one of them.

These nine display windows **visualize data your program sends** with `DEBUG()`.
Your program keeps running at full speed; the window draws whatever you feed it.
The windows do not stop your code, do not single-step it, and do not inspect cogs
or registers on their own. They show what you choose to send.

The P2 also has a **single-step debugger** — invoked by a plain `DEBUG` with no
parentheses — which interrupts a cog, lets you step through instructions, and
examine registers and flags. That is a different tool with a different purpose, and
it is the subject of the separate *P2 Single-Step Debugger Manual*. This manual
mentions it only to draw the line: when you want to *halt and step* code, you reach
for the single-step debugger; when you want to *watch data flow* while code runs,
you reach for these display windows.

## Tooling, in one line

These windows are hosted by **`pnut_term_ts`**, the host application this manual
uses throughout to open and draw them. The same DEBUG display windows are also
hosted by **PNut**, so the examples work there as well. You produce a program that
drives them by compiling with **`pnut_ts`** using the `-d` (debug) option.
[Chapter 2](#ch-2) walks through installing and running both.

## A note on high data rates

The `DEBUG()` link carries every element you send — every sample, pixel, and
value — over a single serial connection, so **the link is the budget.** At the
2 Mbaud the tool uses, 8N1 framing costs about 10 bits per byte, so the wire
moves roughly **200 KB/s of raw bytes**. After the `DEBUG()` command and
formatting overhead the usable payload is lower — as a rough working estimate,
on the order of **100–150 KB/s**.
Everything a window shows has to fit through that.

Most debugging fits comfortably: text, status panels, sensors read at a few Hz
to a few kHz, and interactive controls all sit well under the budget. What does
*not* fit is a live high-bandwidth stream — full-motion video, or a full-rate
ADC, RF, or audio feed. A single 320×240 color frame is already about 230 KB,
more than a second's worth of link, so streaming video live is off the table.

When the data you care about is faster than the link, you do not give up — you
reach for one of three strategies for living within the budget:

- **Pack** — use the streaming windows' **packed-data modes**, which unpack many
  samples from each long you send, moving several times more data per `DEBUG()`
  statement. Packing buys headroom, not an order of magnitude. Covered in
  [Chapter 13](#ch-13).
- **Decimate** — send only 1-in-N samples for a live, always-updating view of a
  slowly-evolving signal. You trade detail for a continuous trend you can watch
  in real time. Detailed in [Chapter 7](#ch-7).
- **Capture and dump** — let a tight PASM loop fill a buffer at full speed, then
  dump that buffer once over the slow link when a trigger fires. The capture runs
  at the P2's speed, not the link's; the link only carries the readout once.
  Detailed in [Chapter 7](#ch-7).

You do not need any of these to get started — but knowing the budget exists, and
that these three strategies live within it, is what keeps the later chapters
honest about which uses a given window can really serve.

**One discipline follows from the link being serial: sending output is not free.**
Each `DEBUG()` call shifts its bytes out one at a time, and the cog waits while it
does — even at 2 Mbaud that is thousands of clocks per message. Keep `DEBUG()` out
of time-critical regions: a debug call inside a tight timing loop distorts the very
timing you are trying to observe. When you must watch a fast path, capture into a
buffer at full speed and dump it once afterward (the capture-and-dump strategy
above) rather than printing from inside the loop.

## Where to go next

Read **[Chapter 2](#ch-2)** for setup — installing the tools and getting your first window
on screen. Then go to the chapter for the window you need: **TERM** ([Ch 3](#ch-3)) is the
right first stop, since most debugging starts as text and the chapter exercises
every part of the model you just learned. From there, choose by the shape of your
data — a waveform wants **SCOPE** ([Ch 7](#ch-7)), digital channels want **LOGIC** ([Ch 6](#ch-6)), a
custom instrument wants **PLOT** ([Ch 5](#ch-5)), and so on down the table above.
