# Chapter 3: The TERM Window — Text Output

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
> in Chapter 12. This chapter is about output.

## Creating a TERM window

You create and configure a window in a single `DEBUG` statement. The first token
after the backtick is the window type (`TERM`); the second is a name you choose.
You feed the window afterward by that name:

```spin2
PUB main()
  debug(`TERM Status SIZE 40 20)     ' create a 40x20 window named "Status"
  debug(`Status "Ready.")            ' feed it by name
```

The configuration keywords you can add to the creation line:

| Keyword | Arguments | Default | What it sets |
|---------|-----------|---------|--------------|
| `TITLE` | `'text'` | `TERM` | The window's title-bar text |
| `POS` | `left top` | auto | Screen position of the window, in pixels |
| `SIZE` | `cols rows` | `40 20` | Grid size; each is **1–256** |
| `TEXTSIZE` | `points` | `10` | Font size; the window sizes itself to fit |
| `COLOR` | 8 values | see below | Four foreground/background color pairs |
| `BACKCOLOR` | `rgb` | black | The window background color |
| `UPDATE` | — | off | Enables buffered mode (see "Controlling updates") |
| `HIDEXY` | — | off | Hides the coordinate readout |

`SIZE` is the one you will set most often. The grid is measured in characters, not
pixels — the window computes its pixel size from the font. A `SIZE 80 25` window
gives you a classic 80-column console.

## Sending text

Once the window exists, everything you send by its name is rendered at the cursor,
left to right, top to bottom. You can send string literals and you can send the
value of a variable:

```spin2
debug(`Status "Temperature: " `udec_(temp) " C")
```

Two things are happening here, and the difference matters:

- A **quoted string** is printed as-is.
- `` `udec_(temp) `` prints the *decimal text* of `temp` — if `temp` holds 25, the
  window shows the characters `25`. Use the formatters (`` `udec_ ``, `` `uhex_ ``,
  `` `sdec_ ``, and so on) whenever you want to display a number.

There is a second, lower-level way numbers reach the window — as **command codes** —
and that is the next section. The rule to carry with you: *to display a number,
format it with a backtick formatter; to issue a command, send a bare number.*

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
debug(`Status 3 2 2 5 "Heading") ' set row 2, set column 5, then print
```

Read `3 2 2 5` as two commands: `3 2` (set row to 2) and `2 5` (set column to 5).
To position with a variable instead of a literal, send the value with `` `() ``:

```spin2
debug(`Status 3 `(line) 2 `(indent) "Positioned")
```

`` `(line) `` sends the *value* of `line` as the command argument — distinct from
`` `udec_(line) ``, which would print it as visible digits.

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
debug(`Status 4 "normal" 13)     ' pair 0: orange on black
debug(`Status 6 "ok" 13)         ' pair 2: lime on black
```

To choose your own colors, set all eight values (four pairs, foreground then
background each) on the creation line with `COLOR`. Values are `$RRGGBB`:

```spin2
debug(`TERM Log SIZE 60 20 COLOR $FF7F00 $000000 $000000 $FF7F00 $00FF00 $000000 $FF0000 $000000)
'                                    pair0 fg/bg     pair1 fg/bg     pair2 fg/bg     pair3 fg/bg
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
    debug(`Events `udec_(n) ": event" 13)   ' scrolls once it fills
    n += 1
    waitms(200)
```

> **Backspace moves, it does not erase.** Code `8` steps the cursor back one cell
> (wrapping to the previous line at column 0) but leaves the character on screen.
> To replace text, reposition with `2`/`3` and overprint, or clear with `0`.

There are no ANSI escape sequences and no text attributes (bold, underline,
blink). Positioning and color are done entirely with the command codes above. Line
feed (`10`) and carriage return (`13`) both mean "newline," and a CR+LF pair counts
as one newline — so text copied from a host that uses either convention behaves
the same.

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
    debug(`Panel "Temp:  " `udec_(temp) " C" 13)
    debug(`Panel "Press: " `udec_(press) " mb" 13)
    debug(`Panel `UPDATE)                 ' repaint once, flicker-free
    waitms(250)

PRI read_temp()  : v
  v := 25                                 ' (your sensor read here)
PRI read_press() : v
  v := 1013
```

Two more runtime keyword commands round out the set:

- `` `CLEAR `` — clears the screen and homes the cursor (identical to code `0`).
- `` `SAVE `` — saves the current window image to a file on the host.

## Considerations

- **Pick the grid to the job.** A status panel might be `40 10`; a scrolling log
  wants more rows; a wide table wants more columns. Both dimensions go up to 256.
- **Buffered mode is for whole-screen redraws.** For a steadily growing log, leave
  it off — real-time drawing is simpler and the per-character cost is negligible.
- **Tabs are fixed at every 8 columns.** For arbitrary alignment, position
  explicitly with the `2` (set column) command instead.
- **Display values with formatters, issue commands with bare numbers.** This is the
  single most common mistake: `` `udec_(x) `` shows the number; a bare `13` is a
  newline, not the text "13".

## Try it

Start with the dashboard example above. Then: switch it to color — print the label
in pair 0 and the value in pair 2, and turn the value red (pair 3) when it crosses a
threshold. You will have a live, color-coded status panel in a dozen lines, and
you will have used creation config, command codes, color pairs, and buffered
updates together.
