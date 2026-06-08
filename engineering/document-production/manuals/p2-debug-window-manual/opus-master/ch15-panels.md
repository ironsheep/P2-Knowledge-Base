# Chapter 15: Building Control and Status Panels — From Text Dashboards to Sprite-Blitted Instruments {#ch-15}

The window chapters each documented one window in isolation. This chapter puts three
of them together for a single, practical job: building **status panels** — instrument
displays you watch — and **control panels** — on-screen surfaces you operate with the
mouse and keyboard.

You have already met every piece. The TERM window positions text at fixed rows and
columns ([Chapter 3](#ch-3)); the PLOT window draws primitives and composites bitmap
layers ([Chapter 5](#ch-5)); `PC_KEY` and `PC_MOUSE` read the host keyboard and mouse
back into your program ([Chapter 12](#ch-12)). A panel is what you get when you
combine them.

The reason this takes so little code is that the display does the drawing. Your
artwork — a text layout, or a set of bitmap images — is **data**, authored once. Each
frame, the P2 issues a short sequence of *position* and *copy* commands; it never
rasterizes a glyph or shades a pixel itself. Buffered (double-buffered) mode presents
each finished frame at once, so the display does not flicker. And because the same
window reads input, a picture becomes a control surface with no added hardware. A
working panel is typically a few dozen lines of Spin2.

This chapter covers two jobs. For **status displays** there is a spectrum of three
techniques — positioned text, vector drawing, and sprite-sheet blitting — and the
guidance is to use the lightest one that does the job. For **control panels** there is
one technique: read input, decide what was hit, act, and redraw. The closing section
is a decision guide.

## A status panel is positioned output, refreshed in place

A scrolling log answers "what just happened." A status panel answers "what is the
state right now" — a fixed face whose labels never move and whose values update in
place. Every status technique in this chapter is the same idea at a different cost:
draw the static frame once, then overwrite only the parts that change, and never let
anything scroll.

### Technique 1 — Text dashboards (TERM), the lightest panel

The TERM window already does everything a textual status panel needs, with no
artwork at all. You draw the fixed labels once, then position the cursor with the
`3` (set row) and `2` (set column) command codes and overprint each value field where
it sits. [Chapter 3](#ch-3) develops this fully under "A positioned dashboard"; the
technique in brief:

```spin2
CON _clkfreq = 200_000_000

PUB main() | angle, rpm, temp, volts
  debug(`TERM Status SIZE 32 6 TITLE 'System Status')

  ' Draw the static labels once.
  debug(`Status 0 4 "SYSTEM STATUS")       ' clear, pair 0, title at (0,0)
  debug(`Status 3 2 2 0 "RPM  :")          ' row 2, col 0
  debug(`Status 3 3 2 0 "Temp :")
  debug(`Status 3 4 2 0 "Volts:")

  angle := 0
  repeat
    rpm   := 1500 + qsin(500, angle, 360)  ' software-generated readings
    temp  := 40 + qsin(8, angle, 360)
    volts := 120 + qsin(3, angle, 360)

    ' Overprint only the value fields, each at a fixed (row, col). Trailing
    ' spaces pad to a fixed width so a shorter value erases a longer one.
    debug(`Status 3 2 2 8 `udec_(rpm) "   ")
    debug(`Status 3 3 2 8 `udec_(temp) "   ")
    debug(`Status 3 4 2 8 `udec_(volts) "   ")

    angle += 3
    waitms(100)
```

The labels are written once; the loop touches only the three value cells, so the
panel reads like a fixed instrument face. Pad every in-place field to a constant
width with trailing spaces — overprinting replaces only the characters you send, so
without padding, printing `99` over `100` leaves `990`.

Reach for a TERM dashboard whenever the status is textual or tabular: register dumps,
state names, counters, a handful of named readings. It needs no images, no layers,
and no graphics window. When a value is better shown as a *shape* — a needle, a bar,
a trace — move up to PLOT.

### Technique 2 — Vector instruments (PLOT), drawn each frame

When a reading is continuous, draw it. The PLOT window's primitives (`LINE`,
`CIRCLE`, `BOX`, and the rest) compose an instrument from geometry, and in buffered
mode you redraw the whole face each frame without flicker. [Chapter 5](#ch-5) builds a
complete analog gauge this way under "A worked instrument": center the origin, switch
to polar so the needle is a single `LINE` from the center to the reading's angle, and
draw the dial with `LINE` and `CIRCLE`.

Vector drawing suits anything geometric and continuously variable — a needle, a
moving bar, a level, a live trace — because the shape is computed from the value
rather than enumerated. It costs a handful of primitive commands per frame and needs
no external artwork. When the face you want is richer than geometry — a
photo-realistic bezel, styled digits, a lamp that lights — move up to sprite-sheet
blitting.

### Technique 3 — Sprite-sheet panels (PLOT layers), composed from bitmap art

The richest panels are assembled from pre-drawn bitmap **artwork** rather than drawn
on the P2. You author the look as Windows BMP files, load them once into the PLOT
window's eight off-screen **layers**, and build each frame by **copying rectangles**
out of those layers onto the canvas with `CROP`. The P2 issues only copy commands and
a little arithmetic; all the pixels were drawn in an image editor. This is the
sprite-sheet (blitting) model, and it is the technique behind Jon McPhalen's
("JonnyMac") DEBUG instrument panels.

> **Requires `{Spin2_v50}`.** The `LAYER`, `CROP`, and sprite commands are V50
> additions. The source file's first line must be `{Spin2_v50}` (or later), compiled
> with a Spin2 v50+ `pnut_ts`. Without it, these commands are not recognized.

**The BMP format is specific.** `LAYER` accepts a **24-bit, uncompressed (BI_RGB),
no-alpha** Windows BMP — one BMP pixel maps to one canvas pixel, with no scaling.
Author each image at the exact device size you will display it. (A short Python +
Pillow generator can produce these images and is the practical way to author the
artwork; that tooling is documented separately from this manual.)

**`CROP` is an opaque copy, and that drives the whole discipline.** Because the
bitmaps carry no transparency, every `CROP` overwrites its destination rectangle
completely. Three consequences follow, and they are the rules of the technique:

- **There is no transparent overlay.** Each sprite cell must already contain the
  correct background around its shape, because blitting it replaces everything in that
  rectangle.
- **You erase by restoring, not by clearing.** To remove something, copy the pristine
  background back over it. So the background layer must contain the empty look of every
  region you will later overwrite.
- **Seams must match.** The pixels just outside a blitted cell come from the
  background; the pixels inside come from the sprite. For an invisible seam, author the
  cell's border to match the background exactly — same colors, same box.

`CROP` has three forms ([Chapter 5](#ch-5) documents them in full), and each is one
idiom of this technique:

```debug-update
CROP layer                           ' whole layer: paint/reset the scene
CROP layer left top width height     ' same spot: erase by restore
CROP layer left top width height x y ' to (x,y): blit a sprite
```

There are two ways to pack visual state into the artwork. Most panels use both:

- **Whole-state layers** — one full-canvas BMP per state. Load `leds_off.bmp` and
  `leds_on.bmp` into two layers; to set an indicator, copy its patch from whichever
  layer holds the wanted state. Strength: trivial code and pixel-perfect alignment
  (source and destination coincide). Cost: one full image per state, so reserve it for
  a few states (on/off, up/down).
- **Font / atlas strips** — one BMP holds many equal cells in a row, and you select
  the cell by arithmetic: `srcX = index * cellWidth`. This is how every numeric
  readout works, and it yields unlimited values from one small image.

A layer may be larger than the window; the area below the visible canvas is free
off-screen storage. JonnyMac's analog meter stacks five color copies of its digit
font below the gauge in the *same* layer and selects color by source Y — the window
shows only the top, and the rest is a palette the code samples from.

The example loads a background and a digit-font strip, then shows a live 3-digit
reading by blitting one glyph per column (the font-strip pattern), erasing the box
first by restoring background:

```spin2
{Spin2_v50}
CON _clkfreq = 200_000_000

PUB main() | angle, reading
  ' Two BMP layers, loaded once and reused every frame.
  debug(`PLOT Panel SIZE 200 96 POS 200 200 HIDEXY UPDATE)
  debug(`Panel LAYER 1 'panel_bg.bmp')      ' background: frame + empty box
  debug(`Panel LAYER 2 'digits.bmp')        ' font strip: 0-9, each 30x48
  debug(`Panel CROP 1)                      ' paint the background once
  debug(`Panel UPDATE)

  angle := 0
  repeat
    reading := 50 + qsin(50, angle, 360)    ' software reading 0..100
    show3(reading)
    debug(`Panel UPDATE)                    ' one flip per frame
    angle += 4
    waitms(50)

' Blit a fixed-width 3-digit reading using the font strip (form c), after
' erasing the readout box by restoring its background (form b).
PRI show3(value) | d, col, x, div
  debug(`Panel CROP 1 45 24 110 48)         ' erase box: restore bg patch
  div := 100
  repeat col from 0 to 2
    d := (value / div) // 10                 ' this column's digit, 0..9
    x := 50 + col * 36                        ' on-screen slot
    debug(`Panel CROP 2 `(d * 30, 0, 30, 48, x, 28))
    div /= 10
```

Each digit costs the P2 one rectangle copy and a divide — there is no glyph
renderer. The same pattern scales to any readout: more columns, a sign cell at the end
of the strip, or a second strip for hex (`0`–`9 A`–`F`). Combine the techniques freely
— the analog meter draws its needle with a vector `LINE` over a blitted bezel, then
restores a clean hub patch over the needle's base to hide the pivot.

## Control panels — reading the surface back

A status panel becomes a control panel when the window reads input. The same
`PC_KEY` / `PC_MOUSE` commands from [Chapter 12](#ch-12) turn any window into a
surface you operate: the user clicks a drawn button or presses a key, and your program
acts. Three rules carry over from that chapter — each input command must be the **last**
command in its `DEBUG()` statement, the window must have **focus**, and `PC_MOUSE`
fills **seven consecutive longs** (`xpos, ypos, wheel, left, middle, right, pixel`,
buttons `0`/`-1`, coordinates negative when the pointer is outside).

Two patterns make a panel interactive:

- **Hit-testing** maps an input position to a control. For a rectangular zone, a
  bounding-box test (`x` within `x1..x2` and `y` within `y1..y2`) answers "was this
  control clicked." A row of controls is a `case` on the coordinate.
- **The dirty flag** keeps the panel cheap. Poll input every pass, but recompose and
  `UPDATE` only when something actually changed. A panel that redraws only on a real
  event uses almost no link bandwidth while idle.

This panel draws two buttons and a value bar, and adjusts the value from either the
arrow keys or a mouse click on a button. It recomposes only on a change:

```spin2
{Spin2_v50}
CON _clkfreq = 200_000_000

PUB main() | m[7], key, value, dirty, lastL
  debug(`PLOT Ctrl SIZE 300 140 POS 200 200 BACKCOLOR $202020 HIDEXY UPDATE)
  value := 50
  dirty := true                              ' force the first draw
  lastL := 0

  repeat
    ' Poll both inputs; each is the LAST command in its statement.
    key := 0
    debug(`Ctrl PC_KEY(@key))
    debug(`Ctrl PC_MOUSE(@m))

    case key                                 ' keyboard: arrows nudge
      1: value -= 5                           ' Left  arrow
         dirty := true
      2: value += 5                           ' Right arrow
         dirty := true

    if m[3] and not lastL                     ' left-button press edge
      if in_box(m[0], m[1], 25, 45, 75, 95)
        value -= 5
        dirty := true
      if in_box(m[0], m[1], 225, 45, 275, 95)
        value += 5
        dirty := true
    lastL := m[3]

    value := 0 #> value <# 100                ' clamp to range

    if dirty
      draw(value)
      debug(`Ctrl UPDATE)
      dirty := false
    waitms(20)

' Bounding-box hit test: true when (x,y) is inside the rectangle.
PRI in_box(x, y, x1, y1, x2, y2) : hit
  hit := (x >= x1) and (x <= x2) and (y >= y1) and (y <= y2)

PRI draw(v) | len
  debug(`Ctrl CLEAR)
  debug(`Ctrl COLOR $C04040 SET 50 70 BOX 50 50 0 255)   ' minus button
  debug(`Ctrl COLOR $40C040 SET 250 70 BOX 50 50 0 255)  ' plus button
  len := 1 + v * 150 / 100                    ' value 0..100 -> bar length
  debug(`Ctrl COLOR $4080FF)
  debug(`Ctrl SET `(75 + len / 2, 70) BOX `(len, 24, 0, 255))
```

Click the window to give it focus, then click a button or use the arrow keys. The
`lastL` variable holds the previous left-button state so a click fires once on the
press edge rather than every poll while the button is held. The `dirty` flag means the
panel sits idle — polling but not redrawing — until an input changes the value.

## Considerations — choosing a technique

- **Use the lightest technique that does the job.** Textual or tabular status → a TERM
  dashboard, no artwork. A continuous, geometric value → PLOT vector drawing. A rich or
  photo-realistic face → PLOT sprite-sheet blitting. Do not author BMP layers for a job
  a positioned text field handles.
- **Always run panels in buffered mode.** Create the window with `UPDATE`, compose the
  whole frame, then issue one `` `UPDATE ``. Batching every change behind a single flip
  is what makes the panel flicker-free.
- **Erase by restoring, never by guessing.** In the blitting technique there is no
  clear-to-blank; copy clean background over a region (`CROP` form b) or repaint the
  whole scene (form a). The background layer must hold the empty look of everything you
  overwrite.
- **Gate redraws behind a dirty flag** for interactive panels. Poll input continuously,
  but recompose only on a real change so an idle panel costs almost nothing.
- **High-rate panels need packed feeds.** When a panel is driven by a fast sample
  stream, the debug link is the bottleneck; pack many samples per `DEBUG()` call
  ([Chapter 13](#ch-13)).
- **Run several panels at once.** Each `DEBUG(\`PLOT ...)` or `DEBUG(\`TERM ...)` with a
  distinct name is an independent window; a cog can drive a wall of panels, and PASM2
  can drive them too ([Chapter 14](#ch-14)).

## Try it

Start from the TERM dashboard and add one interactive field: poll `PC_KEY` in the loop
and let the `+` and `-` keys adjust one of the readings, redrawing only on a keypress.
Then rebuild the same panel in PLOT with a sprite-digit readout (Technique 3) and a
mouse-clickable button (the control pattern) — you will have moved one panel across the
whole spectrum, from positioned text to a blitted, clickable instrument, using nothing
but the debug link and a bare P2 board.
