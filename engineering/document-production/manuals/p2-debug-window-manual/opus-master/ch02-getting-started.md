# Chapter 2: Getting Started {#ch-2}

This chapter takes you from a `.spin2` source file to a live DEBUG display
window on your screen. The path is short: compile with debugging enabled, run the
program from the host application, and the window opens. Everything in this manual
builds on this loop, so it is worth doing once, end to end, before you move on to
the individual windows.

## What you need

Two things, and nothing else:

- **A P2 board** connected to your computer over USB. Any P2 board works; no
  shields, sensors, probes, or external wiring are required.
- **A PC running `pnut-term-ts`**, the host application that programs the P2 and
  opens the DEBUG display windows.

The compiler is `pnut-ts`, and the host application that opens the display windows
is `pnut-term-ts`; this manual uses that pair throughout. The same DEBUG display
windows are also hosted by **PNut** and by the **Spin Tools IDE**, so the examples
work in those environments too — just confirm your environment runs the DEBUG link
at 2 Mbaud (see [Chapter 13](#ch-13)). Every example in this manual runs on a bare
board with the USB cable as its only connection.

## Compiling with debugging

DEBUG output is not part of your program unless you ask for it. By default the
compiler strips every `DEBUG()` statement, so a release build carries no debugging
overhead. To keep the DEBUG statements — and the display windows they drive — you
compile with the `-d` flag:

```command
pnut-ts -d myprogram.spin2
```

`-d` (equivalently `--debug`) tells `pnut-ts` to compile the DEBUG statements into
the binary instead of discarding them. Without it, the `DEBUG()` calls in your
source produce no output and no windows open. This is the single most common
reason a window fails to appear: the program was compiled without `-d`.

## Running it

Run the compiled program from `pnut-term-ts`. It programs the P2 over USB and then
listens for DEBUG output. When your program executes a `DEBUG()` statement that
names a display window, `pnut-term-ts` opens that window and begins drawing into
it. The window stays open and updates live as more data arrives.

DEBUG data travels from the P2 to the host over a serial link on the P2's pins 62
(transmit) and 63 (receive) — the standard programming pins — at 2 Mbaud. You do
not configure any of this; it is the default, and `pnut-term-ts` is already
listening on it. You only need to know the link exists, because its speed is the
ceiling on how fast a window can update.

## Your first window

Here is a complete program that opens a text window and prints a value:

```{.spin2 caption="ch02-term-print-value.spin2"}
CON _clkfreq = 200_000_000

PUB main() | reading
  debug(`TERM Status SIZE 30 5)  ' create a 30x5 text window named "Status"
  reading := 42
  debug(`Status 'Reading: `(reading)' 13)   ' feed it by name
  repeat                                          ' keep the window open
```

Two `DEBUG()` statements, two distinct jobs:

- The first **creates** a window. The first token after the backtick is the window
  type (`TERM`); the second is a name you choose (`Status`). `SIZE 30 5` makes it
  30 columns by 5 rows.
- The second **feeds** that window, addressing it by the name you gave it. The
  single-quoted text prints as-is; the `` `(reading) `` substitution inside it
  prints the decimal text of `reading` — the characters `42`; the bare `13` is a
  newline. (In a TERM, display a value with `` `(value) `` substitution, not
  `` `udec_ `` — the trailing-underscore formatters render as a glyph here.)

This create-by-name, feed-by-name model is how every window in this manual works.
You declare a window once with a type and a name, then drive it by that name for
the rest of the program. The window type determines what the window draws and what
commands it accepts — covered chapter by chapter — but the two-step pattern never
changes.

**One restriction on the name you choose: it must not be a DEBUG display
directive.** Two different vocabularies are in play here, and only one of them can
collide with your window name:

- **Spin2's reserved words do not matter.** The compiler passes the display name
  through as raw text; it never interprets it. A window named `Field` works
  perfectly well even though `FIELD` is a Spin2 keyword.
- **The display vocabulary's own words do matter.** The parser classifies each token
  before deciding what to do with it, and a token it already knows can never become
  a window name. Naming a window `Trace`, `Box`, `Red`, `RGB24` or `Size` declares
  **no window at all**.

The failure is silent at both layers: the program compiles without complaint, the
host reports nothing, and no window appears — every feed addressed to that name
goes nowhere. If a window you created never shows up, suspect its name first.

The complete rule has five parts. A name is legal when **all** of them hold:

1. **It starts with a letter or `_`**, followed by letters, digits or `_`. A leading
   digit makes the token parse as a *number*, which aborts the statement — a
   different failure from the one above, and just as quiet.
2. **It is not one of the 103 reserved display words** — the nine window types, the
   eleven color names, the nineteen color modes, the twelve packed-data modes, and
   the fifty-two directives. [Appendix A](#appendix-a) lists the directives;
   remember that the colors, color modes and packed modes are reserved too, and
   that *another* window's directive is as fatal as your own window's.
3. **It is not the name of a window that is currently open.** Names are per-session
   symbols, so a second `SCOPE Waves` addresses the existing `Waves`.
4. **Case does not distinguish names.** `Trace`, `TRACE` and `trace` are one symbol,
   so changing capitalization never escapes rule 2. Your original casing is what
   the window's title bar displays.
5. **Only the first 30 characters count.** Anything longer is truncated silently,
   so two names that share their first 30 characters are the same window.

In practice: pick a short, ordinary word that is not a display term — `Scan`,
`Panel`, `Waves`, `Status`, `Probe` — and none of this comes up. Names are also
reusable: `CLOSE` a window and its name is free again.

> Display values as text, issue commands with bare numbers.
> In a TERM, a `` `(x) `` substitution inside single-quoted text shows the digits of
> `x`; a bare `13` is the newline command,
> not the text "13". Value-only output formatters such as `UDEC_`, `SDEC_`,
> `UHEX_`, `SHEX_`, and `UBIN_` — every DEBUG output command has a trailing-underscore
> value-only form — feed a numeric data element (consumed by the
> graphing windows), so to display a value's text in a TERM use `` `(value) ``
> substitution instead.

Compile it with `pnut-ts -d`, run it from `pnut-term-ts`, and a small text window
titled `Status` opens showing `Reading: 42`.

## The no-hardware philosophy

You do not need anything wired to the P2 to see any window in this manual work.
That is deliberate. The P2 can generate its own data in software, and a generated
signal drives a display window exactly the way a real sensor would. Throughout
this manual, examples produce their own data using:

- **counters** — a variable you increment in a loop,
- **the CORDIC solver** — `QSIN` / `ROTXY` for smooth waveforms and rotations,
- **the random-number generator** — `GETRND` (or the `??` operator) for noise,
- **`GETCT`** — the system counter, for timing and elapsed-time measurements.

A counter feeding a text window, a CORDIC sine wave feeding a SCOPE, RNG noise
feeding a LOGIC trace — each exercises the full path from `DEBUG()` to a live
window with no wiring at all. This program drives a text window from two software
sources, a CORDIC sine and the RNG:

```{.spin2 caption="ch02-term-signals.spin2"}
CON _clkfreq = 200_000_000

PUB main() | angle, wave, noise
  debug(`TERM Signals SIZE 40 5)
  angle := 0
  repeat
    wave  := qsin(1000, angle, $1000)              ' CORDIC: a sine value
    noise := getrnd() & $FF                        ' RNG: a noise value
    debug(`Signals 1 'wave=`(wave)  noise=`(noise)')
    angle += $0040
    waitms(50)
```

The `1` after the window name homes the cursor each pass, so the line updates in
place. Where a real-hardware version of an example is worth showing, this manual
adds it as a short optional note *after* the software-only version — but you can
work through the entire manual on a bare board.

## Optional DEBUG configuration symbols

The defaults above need no setup. If you want to change them, declare any of these
symbols in a `CON` block and the compiler picks them up:

| Symbol | Default | What it sets |
|--------|---------|--------------|
| `DEBUG_PIN_TX` | `62` | The P2 pin that transmits DEBUG data. Must be 62 for display windows to open. |
| `DEBUG_PIN_RX` | `63` | The P2 pin that receives host input (keyboard, mouse). |
| `DEBUG_BAUD` | `2_000_000` | The DEBUG serial baud rate. |
| `DEBUG_COGS` | `%11111111` | Which cogs have debugging enabled; bits 7..0 enable cogs 7..0. |
| `DEBUG_DELAY` | `0` | Milliseconds to wait before the program starts transmitting DEBUG output. |
| `DEBUG_WINDOWS_OFF` | `0` | Set non-zero to suppress all DEBUG windows after programming. |

For display windows to open at all, `DEBUG_PIN_TX` must be 62 — that is the pin
`pnut-term-ts` listens on. The defaults already satisfy this; the symbols exist for
the cases where you must move the link or limit which cogs participate.

```{.spin2 caption="ch02-term-pin-config.spin2"}
CON _clkfreq = 200_000_000

CON
  DEBUG_PIN_TX = 62
  DEBUG_PIN_RX = 63
  DEBUG_BAUD   = 2_000_000

PUB main()
  debug(`TERM Status SIZE 30 5)
  debug(`Status 'Ready.' 13)
  repeat                         ' keep the window open
```

## Where to go next

You now have the loop that every chapter relies on: compile with `-d`, run from
`pnut-term-ts`, address a window by the name you gave it. From here:

- **[Chapter 3](#ch-3) — TERM** covers the text window in full: cursor positioning, command
  codes, color pairs, and buffered updates. Start there if you are new to the
  display windows.
- The graphical windows each have their own chapter — **BITMAP** ([Ch 4](#ch-4)),
  **PLOT** ([Ch 5](#ch-5)), **LOGIC** ([Ch 6](#ch-6)), **SCOPE** ([Ch 7](#ch-7)),
  **SCOPE_XY** ([Ch 8](#ch-8)), **FFT** ([Ch 9](#ch-9)), **SPECTRO** ([Ch 10](#ch-10)),
  and **MIDI** ([Ch 11](#ch-11)). Each follows the same create-then-feed pattern shown here.
