# Chapter 1: The DEBUG Display Windows

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
| **TERM** | A scrolling text terminal — status lines, variable dumps, logs | Ch 3 |
| **BITMAP** | A pixel raster you draw into directly, framebuffer-style | Ch 4 |
| **PLOT** | An XY plotting surface with layered drawing and sprites | Ch 5 |
| **LOGIC** | A logic-analyzer trace of 1–32 digital channels | Ch 6 |
| **SCOPE** | A time-domain oscilloscope of 1–8 sampled values | Ch 7 |
| **SCOPE_XY** | An XY (Lissajous / phase) scope | Ch 8 |
| **FFT** | A frequency-domain spectrum | Ch 9 |
| **SPECTRO** | A spectrogram — frequency content over time | Ch 10 |
| **MIDI** | A piano-keyboard display driven by MIDI note messages | Ch 11 |

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
DEBUG(`Status "Ready.")
```

The name is the whole interface. The first statement said "make a TERM window and
call it `Status`"; the second says "send this to `Status`." You can feed the same
window from many places in your program, and you can feed two windows the same data
by naming both. A complete minimal program:

```spin2
CON _clkfreq = 200_000_000

PUB main()
  debug(`TERM Status SIZE 40 20)   ' create a window named "Status"
  debug(`Status "Ready.")          ' feed it by name
  repeat                           ' keep the program (and window) alive
```

Compile this with `pnut_ts -d` (Chapter 2 covers the setup) and a 40×20 terminal
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
- **Strings** — text in single quotes, such as `'Sawtooth'`, or in the Spin2 source
  written with double quotes, such as `"Ready."`. A string is shown literally.
- **Numbers** — written in decimal, hex (`$FF`), or binary (`%1010`). What a number
  *means* depends on context, and that is the rule you must internalize.

### Values versus command codes

A number in the feed stream is interpreted one of two ways, and you control which:

- A number sent through a **formatter** is *displayed as text*. The formatters
  are the same `DEBUG()` output commands you use for serial output, in their
  value-only form: `` `udec_(x) ``, `` `uhex_(x) ``, `` `sdec_(x) ``, and so on.
  There are also shorthands: `` `(x) `` is short for `SDEC_` (signed decimal),
  `` `$(x) `` for `UHEX_` (hex), `` `%(x) `` for `UBIN_` (binary), `` `.(x) `` for
  `FDEC_` (floating point), and `` `#(x) `` to send the character whose code is `x`.
  If `x` holds 25, then `` `udec_(x) `` puts the two characters `2` and `5` into the
  stream.
- A **bare number** — one not wrapped in a formatter — is a *command code*. The
  window reads it as an instruction, not as text to display.

This is why a terminal treats a bare `13` as a newline rather than printing the
digits "13": `13` is a command code. To show the number thirteen, you would send
`` `udec_(13) `` or the literal string `"13"`. Carry this rule into every chapter:

> **To display a number, format it. To issue a command, send it bare.**
> `` `udec_(temp) `` shows the value of `temp`; a bare `13` is a command code, not
> the text "13".

Each window assigns its own meaning to its command codes and to its raw data
values — what a number does in a TERM window (cursor and color control) is not what
it does in a SCOPE window (a sample value). Those meanings are documented in the
per-window chapters. The element model — keywords, strings, formatted values,
and bare command numbers — is the same everywhere.

## Commands common across windows

Most windows share a small set of named-keyword commands. You send them by name,
after the window name, the same way you send data:

- **`CLEAR`** — clear the window's contents and reset it to wait for new data.
- **`SAVE`** — save the window's current image to a file on the host. Most windows
  accept `SAVE 'filename'`, and optionally `SAVE WINDOW 'filename'` to capture the
  whole window rather than just the display area.
- **`UPDATE`** — control buffered repainting. A window placed in update mode (by
  adding `UPDATE` to its creation line) does not redraw as data arrives; it
  repaints only when you feed it the `UPDATE` command. This eliminates flicker when
  you redraw a whole display at once. Not every window supports buffered mode — its
  chapter says whether it does.
- **`PC_KEY`** and **`PC_MOUSE`** — read the host keyboard and mouse back into your
  program, so a window can be interactive. These work across window types and share
  one mechanism, so they are covered together in Chapter 12.

Each window also has commands of its own — `TRIGGER` and `HOLDOFF` on SCOPE and
LOGIC, the drawing commands on PLOT, and so on. Those belong to the window and are
documented in its chapter.

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

These windows are hosted by **`pnut_term_ts`**, the host application that opens and
draws them. You produce a program that drives them by compiling with **`pnut_ts`**
using the `-d` (debug) option. Chapter 2 walks through installing and running both.

## A note on high data rates

The `DEBUG()` link carries every element you send over a serial connection, so the
rate at which a window can be fed is bounded by that link. When you need to push
data fast — capturing a high-speed signal, for instance — the streaming windows
accept **packed-data modes** that unpack many samples from each long you send,
moving far more data per `DEBUG()` statement. Packed-data modes are covered in
Chapter 13; you do not need them to get started.

## Where to go next

Read **Chapter 2** for setup — installing the tools and getting your first window
on screen. Then go to the chapter for the window you need: **TERM** (Ch 3) is the
right first stop, since most debugging starts as text and the chapter exercises
every part of the model you just learned. From there, choose by the shape of your
data — a waveform wants **SCOPE** (Ch 7), digital channels want **LOGIC** (Ch 6), a
custom instrument wants **PLOT** (Ch 5), and so on down the table above.
