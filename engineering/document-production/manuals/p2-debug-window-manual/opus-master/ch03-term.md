# Chapter 3: The TERM Window — Text Output {#ch-3}

The TERM window is the text terminal of the P2 debug system. You send it
characters and strings; it shows them in a scrolling grid, the way a classic
console does. It is the window you reach for first, because most debugging starts
as text: a status line, a variable dump, a running log of what your program is
doing.

You create one TERM window per `` DEBUG(`TERM ...) `` declaration, give it a name,
and from then on you address it by that name. This chapter covers everything the
window does — creating it, sending text, positioning the cursor, using color, and
controlling when the display updates.

> Keyboard and mouse input (`PC_KEY`, `PC_MOUSE`) work in the TERM window too, but
> they share one mechanism across every window type, so they are covered together
> in [Chapter 12](#ch-12). This chapter is about output.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=0.75\linewidth]{inbox/assets/fig-03-term-dashboard.png}
\caption{The TERM window as a positioned status dashboard.}
\end{figure}
```

## Creating a TERM window

You create and configure a window in a single `DEBUG` statement. The first token
after the backtick is the window type (`TERM`); the second is a name you choose.
You feed the window afterward by that name:

```spin2
PUB main()
  debug(`TERM Status SIZE 40 20)     ' create a 40x20 window named "Status"
  debug(`Status 'Ready.')            ' feed it by name
```

The configuration keywords you can add to the creation line:

| Keyword | Arguments | Default | What it sets |
|---------|-----------|---------|--------------|
| `TITLE` | `'text'` | `TERM` | The window's title-bar text |
| `POS` | `left top` | auto | Screen position of the window, in pixels |
| `SIZE` | `cols rows` | `40 20` | Grid size; each is **1–256** |
| `TEXTSIZE` | `points` | editor text size | Font size (6–200); the window sizes itself to fit |
| `COLOR` | 8 values | see below | Four foreground/background color pairs |
| `BACKCOLOR` | `rgb` | black | The canvas background — the fill used for clear and scroll (not the per-character background) |
| `UPDATE` | — | off | Enables buffered mode (see "Controlling updates") |
| `HIDEXY` | — | off | Hides the coordinate readout |

Sent at runtime in a feed (rather than on the creation line), `BACKCOLOR` instead
sets the background drawn behind subsequent characters — the per-character text
background.

`SIZE` is the one you will set most often. The grid is measured in characters, not
pixels — the window computes its pixel size from the font. A `SIZE 80 25` window
gives you a classic 80-column console.

## Sending text

Once the window exists, everything you send by its name is rendered at the cursor,
left to right, top to bottom. You can send a text string and you can substitute the
value of a variable into the line:

```spin2
debug(`Status 'Temperature: `(temp) C')
```

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=0.60\linewidth]{inbox/assets/fig-03-term-first.png}
\caption{The TERM window after its first formatted value --- with \texttt{temp} holding 25, the window shows \texttt{Temperature: 25 C}.}
\end{figure}
```

Two things are happening here, and the difference matters:

- **Text is single-quoted.** Inside a backtick feed, a string literal must use
  single quotes (`'...'`). This is the one rule that trips everyone up: a
  *double*-quoted string compiles without error but is **silently dropped at
  runtime** — the text simply never appears. Single quotes only.
- `` `(temp) `` substitutes the *decimal text* of `temp` into the line — if `temp`
  holds 25, the window shows the characters `25`. `` `(value) `` is how you display
  a number's text in a TERM (it is shorthand for signed decimal).

> **Don't reach for `` `udec_() `` here.** The trailing-underscore formatters
> (`` `udec_ ``, `` `sdec_ ``, `` `uhex_ ``) feed a *numeric data element* — the form
> the graphical windows (SCOPE, LOGIC, FFT) consume as a data point. Send one to a
> TERM and the number is rendered as a single **character glyph** (value 42 prints
> `*`, not `42`). In a TERM, display a value with `` `(value) `` substitution.

There is a second, lower-level way numbers reach the window — as **command codes** —
and that is the next section. The rule to carry with you: *to display a value, put
`` `(value) `` inside your single-quoted text; to issue a command, send a bare
number.*

## Command codes

A bare number in the feed stream is not printed — it is a command. The window
recognizes these codes:

| Code | Command | Effect |
|------|---------|--------|
| `0` | Clear + Home | Clear the screen and move the cursor to (0, 0) |
| `1` | Home | Move the cursor to (0, 0) without clearing |
| `2` | Set column | The **next** number is the column (0-based) |
| `3` | Set row | The **next** number is the row (0-based) |
| `4`–`7` | Select color pair | Switch to color pair 0, 1, 2, or 3 |
| `8` | Backspace | Move the cursor back one position (see caveat below) |
| `9` | Tab | Advance to the next 8-column tab stop |
| `10` / `13` | Newline | Move to the start of the next line |
| `32`–`255` | Character | Printable ASCII; normally you send these as strings |

So to clear the screen and print a heading at row 2, column 5:

```spin2
debug(`Status 0)                 ' clear + home
debug(`Status 3 2 2 5 'Heading') ' set row 2, set column 5, then print
```

Read `3 2 2 5` as two commands: `3 2` (set row to 2) and `2 5` (set column to 5).
To position with a variable instead of a literal, send the value with `` `() ``:

```spin2
debug(`Status 3 `(line) 2 `(indent) 'Positioned')
```

Here `` `(line) `` supplies the *value* of `line` as the argument to the `3` (set
row) command. It is the same `` `(value) `` substitution you use to display a
number — the window interprets it as a command argument because a command code
(`3`) precedes it. Position first, then print: the `'Positioned'` text lands at the
cursor you just set.

## Color

The TERM window holds **four color pairs**, each a foreground and a background.
You select the active pair at runtime with codes `4`–`7`. The defaults are:

| Pair | Code | Foreground | Background |
|------|------|-----------|------------|
| 0 | `4` | Orange | Black |
| 1 | `5` | Black | Orange |
| 2 | `6` | Lime | Black |
| 3 | `7` | Black | Lime |

```spin2
debug(`Status 4 'normal' 13)     ' pair 0: orange on black
debug(`Status 6 'ok' 13)         ' pair 2: lime on black
```

To choose your own colors, set all eight values (four pairs, foreground then
background each) on the creation line with `COLOR`. Values are `$RRGGBB`:

```spin2
debug(`TERM Log SIZE 60 20 COLOR ...
      $FF7F00 $000000 ...                ' pair0 fg/bg
      $000000 $FF7F00 ...                ' pair1 fg/bg
      $00FF00 $000000 ...                ' pair2 fg/bg
      $FF0000 $000000)                   ' pair3 fg/bg
```

That gives pair 0 = orange-on-black, pair 1 = black-on-orange, pair 2 =
lime-on-black, pair 3 = red-on-black — a common scheme for normal / highlighted /
success / error text.

## Cursor, tabs, and scrolling

- **Positioning** uses the `1` (home), `2` (set column), and `3` (set row) codes
  above. Columns and rows are 0-based, so the top-left cell is (0, 0).
- **Tab** (`9`) advances to the next multiple of 8 columns, printing spaces — at
  minimum one space, at most eight. It is how you line up columns in a table.
- **Auto-wrap**: when text reaches the right edge, the cursor moves to the start of
  the next line on its own.
- **Auto-scroll**: a newline on the bottom row scrolls the whole grid up one line
  and clears the new bottom line. A `SIZE 80 25` window used in a loop becomes a
  continuously scrolling log with no extra work.

```spin2
PUB log_loop() | n
  debug(`TERM Events SIZE 80 25)
  n := 0
  repeat
    debug(`Events '`(n): event' 13)         ' scrolls once it fills
    n += 1
    waitms(200)
```

> **Backspace moves, it does not erase.** Code `8` steps the cursor back one cell
> (wrapping to the previous line at column 0) but leaves the character on screen.
> To replace text, reposition with `2`/`3` and overprint, or clear with `0`.

There are no ANSI escape sequences and no text attributes (bold, underline,
blink). Positioning and color are done entirely with the command codes above. Line
feed (`10`) and carriage return (`13`) both mean "newline," and a CR+LF pair counts
as one newline. This holds when the newline is sent as a bare command number;
inside a quoted string only CR (`13`) breaks the line, while `Chr(9)` and `Chr(10)`
render as glyphs — so text pasted into a string literal will not treat its line
feeds as newlines.

## Controlling updates

By default the window draws each character as it arrives — convenient for live
logging. When you are redrawing a whole screen at once (a dashboard, say), that
per-character drawing can flicker. Add `UPDATE` to the creation line to enable
**buffered mode**: your output accumulates off-screen, and the window repaints only
when you send the `` `UPDATE `` command.

```spin2
PUB dashboard() | temp, press
  debug(`TERM Panel SIZE 40 10 UPDATE)   ' buffered
  repeat
    temp := read_temp()
    press := read_press()
    debug(`Panel 0)                       ' clear (off-screen)
    debug(`Panel 'Temp:  `(temp) C' 13)
    debug(`Panel 'Press: `(press) mb' 13)
    debug(`Panel UPDATE)                  ' repaint once, flicker-free
    waitms(250)

PRI read_temp()  : v
  v := 25                                 ' (your sensor read here)
PRI read_press() : v
  v := 1013
```

Three more runtime keyword commands round out the set:

- `` `CLEAR `` — clears the screen and homes the cursor (identical to code `0`).
- `` `SAVE `` — saves the current window image to a file on the host.
- `` `CLOSE `` — closes this window and frees its resources.

## A positioned dashboard

The scrolling log and the buffered Panel both rewrite the whole display each pass.
When a panel's *layout* is fixed — the labels never move, only the values change —
draw the labels once, then overprint just the value fields in place with the `3`
(set row) and `2` (set column) codes. Nothing scrolls, and there is no full clear.

```{.spin2 caption="ch03-term-dashboard.spin2"}
CON _clkfreq = 200_000_000

PUB main() | ang, signal, count
  debug(`TERM Panel SIZE 40 8)

  ' Draw the static layout once: a title and three fixed labels.
  debug(`Panel 0 4 'SIGNAL MONITOR')     ' clear, pair 0, title at (0,0)
  debug(`Panel 3 2 2 0 'Sample:')        ' row 2, col 0
  debug(`Panel 3 3 2 0 'Value :')        ' row 3, col 0
  debug(`Panel 3 4 2 0 'State :')        ' row 4, col 0

  ang := 0
  count := 0
  repeat
    signal := qsin(1000, ang, 256)       ' software-generated waveform

    ' Overprint only the value fields, each at a fixed (row, col). Trailing
    ' spaces pad to a fixed width so a shorter value erases a
    ' longer old one.
    debug(`Panel 3 2 2 8 '`(count)    ')
    debug(`Panel 3 3 2 8 '`(signal)    ')
    if abs signal > 800
      debug(`Panel 3 4 2 8 7 'HIGH ' 4)  ' pair 3 (red), then back to pair 0
    else
      ' pair 2 (lime), then back to pair 0
      debug(`Panel 3 4 2 8 6 'ok   ' 4)

    ang   += 4
    count += 1
    waitms(50)
```

The labels are written once; the loop touches only the three value cells, so the
fields never scroll or interfere — the panel reads like a fixed instrument face.

> Pad every in-place field to a constant width (the trailing spaces above).
> Overprinting replaces only the characters you send, so without padding, printing
> `9` over `123` leaves `923`.

### Where you'd use this

In computer science and computer engineering, the TERM window is the everyday tool
for **systems telemetry and observability** — surfacing the internal state of a
running program — and for **transaction and event logging**, a running record of
what happened and when.

**On an embedded project**, you reach for it to show per-cog load and stack
high-water marks, to inspect a peripheral's registers live, to keep running fault
and event counters, or to print a state machine's current state as it advances.

**Bandwidth fit:** text and status panels update at human-readable rates — a few
times a second is plenty — so TERM sits far inside the link budget; there is no
high-rate case to temper.

**Extension (real hardware):** swap the synthetic `qsin` reading for a real sensor
or register read, and the same panel reports live values.

## Considerations

- **Pick the grid to the job.** A status panel might be `40 10`; a scrolling log
  wants more rows; a wide table wants more columns. Both dimensions go up to 256.
- **Buffered mode is for whole-screen redraws.** For a steadily growing log, leave
  it off — real-time drawing is simpler and the per-character cost is negligible.
- **Tabs are fixed at every 8 columns.** For arbitrary alignment, position
  explicitly with the `2` (set column) command instead.
- **Use single quotes, and substitute values with `` `(value) ``.** The two most
  common mistakes both fail silently: double-quoted text is dropped (use `'...'`),
  and a value displayed with `` `udec_(x) `` arrives as a character glyph, not its
  digits (use `` `(x) ``). And remember a bare `13` is a newline command, not the
  text "13".

## Try it

Start with the dashboard example above. Then: switch it to color — print the label
in pair 0 and the value in pair 2, and turn the value red (pair 3) when it crosses a
threshold. You will have a live, color-coded status panel in a dozen lines, and
you will have used creation config, command codes, color pairs, and buffered
updates together.
