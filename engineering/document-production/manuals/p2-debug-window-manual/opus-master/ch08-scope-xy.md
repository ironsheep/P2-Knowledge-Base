# Chapter 8: The SCOPE_XY Window — XY, Lissajous, and Phase Plots

The SCOPE_XY window plots one value against another. Where the SCOPE window
(Chapter 7) shows a signal *over time* — amplitude on the vertical axis, time
marching across the horizontal — SCOPE_XY puts the *first* value on the X axis and
the *second* on the Y axis, and draws a dot where they meet. Feed it a stream of
`(x, y)` pairs and it draws the path those pairs trace out: a Lissajous figure from
two oscillators, the phase relationship between two signals, the orbit of a moving
point, a polar curve.

Reach for SCOPE_XY when the relationship between two values matters more than how
either one changes over time. Two sine sources at the same frequency draw an
ellipse whose shape encodes their phase difference; the same two at a 3:2 frequency
ratio draw a stable knot. A position `(x, y)` plotted continuously becomes a
trajectory. SCOPE is the right tool for a waveform you want to read left to right;
SCOPE_XY is the right tool when the *shape* in the plane is the thing you want to
see.

> Keyboard and mouse input (`PC_KEY`, `PC_MOUSE`) work in SCOPE_XY as in every
> window; they share one mechanism documented in Chapter 12. This chapter is about
> output — configuring the plot and feeding it coordinate pairs.

![The SCOPE_XY window tracing a 2:3 Lissajous figure.](inbox/assets/fig-08-scope-xy.png){width=65%}

## Creating a SCOPE_XY window

You create and configure the window in one `DEBUG` statement. The first token after
the backtick is the window type (`SCOPE_XY`); the second is a name you choose.
Channel names — the strings that label each trace — go on the same line, and each
may be followed by a color:

```spin2
PUB main()
  debug(`SCOPE_XY Lissajous SIZE 256 RANGE 1000 SAMPLES 0 'XY')  ' create + name
  debug(`Lissajous `(500, 250))                                  ' feed by name
```

The configuration keywords you can add to the creation line:

| Keyword | Arguments | Default | What it sets |
|---------|-----------|---------|--------------|
| `TITLE` | `'text'` | `Scope_XY` | The window's title-bar caption |
| `POS` | `left top` | cascaded | Screen position of the window, in pixels |
| `SIZE` | `radius` | `128` | Display **radius** in pixels; the plot is `2*radius` wide and tall, and always square |
| `RANGE` | `value` | `$7FFFFFFF` | Symmetric coordinate extent: the plot spans `-value` to `+value` on both axes (in polar mode, `0` to `value` for the radius) |
| `SAMPLES` | `count` | `256` | Persistence depth: how many recent points are kept and faded. `0` means infinite persistence — points accumulate and never fade |
| `RATE` | `divisor` | `1` | Plot one display update per this many samples received |
| `DOTSIZE` | `pixels` | `6` | Dot diameter, `2`–`20` |
| `TEXTSIZE` | `points` | `10` | Legend text size, `6`–`200` |
| `COLOR` | `back {grid}` | black, gray | Background color and, optionally, grid color |
| `POLAR` | `{twopi {offset}}` | — | Interpret pairs as `(radius, angle)` instead of `(x, y)` — see below |
| `LOGSCALE` | — | linear | Logarithmic radial scale, to magnify points near the center |
| `HIDEXY` | — | shown | Hide the X,Y coordinate readout at the mouse pointer |
| `'name' {color}` | — | next default color | Declare a channel (trace), optionally with a color |

Three of these behave differently from what their names might suggest, and getting
them wrong is the most common SCOPE_XY mistake:

- **`SIZE` takes one number, a radius — not a width and a height.** `SIZE 256`
  produces a 512×512 plot. The window is always square; you cannot give it separate
  width and height.
- **`RANGE` takes one number, a symmetric extent — not four edges.** `RANGE 1000`
  maps `-1000` to the left/bottom edge and `+1000` to the right/top edge. The origin
  is the center of the plot. A point at `(0, 0)` lands dead center; a point at
  `(1000, 1000)` lands in the top-right corner.
- **`SAMPLES` sets persistence depth, not a sample count to capture.** With
  `SAMPLES 0` every point you send stays on screen forever (until you clear it) —
  use this for figures you want to build up, like a complete Lissajous curve. With
  `SAMPLES 60` only the most recent 60 points are kept, and they fade from fully
  opaque (newest) to nearly transparent (oldest), drawing a comet-like trail behind
  a moving point.

### Declaring channels

Each quoted string on the creation line declares one trace and names it for the
legend. SCOPE_XY supports up to **8** traces. Put a color after a name to set that
trace's color; omit it to take the next default:

```spin2
debug(`SCOPE_XY Phase SIZE 256 RANGE 1000 SAMPLES 200 'A' RED 'B' GREEN)
```

That declares two traces — `A` in red, `B` in green. The number of channels you
declare determines how SCOPE_XY groups the numbers you feed it, which is the next
section.

## Sending coordinate pairs

Once the window exists, you feed it by name. Each pair of numbers you send is one
`(x, y)` point. Send the values inside a `` `() `` group, comma-separated:

```spin2
debug(`Lissajous `(x, y))
```

This is the same `` `() `` value syntax used throughout the DEBUG windows: it sends
the *values* of `x` and `y` as data, not their decimal text. There is no separate
"plot a point" keyword — a pair of numbers *is* a point.

With more than one channel declared, send all channels' coordinates in one feed, in
channel order — channel 0's X and Y first, then channel 1's, and so on:

```spin2
' two channels declared as 'A' and 'B':
debug(`Phase `(x1, y1, x2, y2))   ' (x1,y1) -> A, (x2,y2) -> B
```

SCOPE_XY collects values until it has a complete set — two per declared channel —
then plots all channels at once and starts the next set. You can also split a set
across several feeds; the window assembles them in arrival order.

## Polar mode

Add `POLAR` to the creation line and SCOPE_XY interprets each pair as
`(radius, angle)` instead of `(x, y)`. The first value is the distance from center
(`0` to `RANGE`); the second is an angle.

```spin2
debug(`SCOPE_XY Rose SIZE 256 RANGE 1000 POLAR 360 'Rose')
```

`POLAR` takes up to two optional numbers:

- **`twopi`** — the angle value that equals one full circle. `POLAR 360` means
  angles are in degrees; `POLAR 1000` means a full turn is 1000 units. The default
  full-circle value is `$1_0000_0000` (a full 32-bit angle); pass `0` to select that
  default explicitly, or `-1` to run angles the other direction.
- **`offset`** — an angular offset added to every angle, rotating the whole plot.

Angle `0` points up; increasing angle sweeps around the circle. Feed
`(radius, angle)` pairs exactly as you feed `(x, y)` pairs in Cartesian mode:

```spin2
debug(`Rose `(radius, angle))
```

## LOGSCALE

`LOGSCALE` switches the radial axis from linear to logarithmic, magnifying points
near the center so a wide range of magnitudes is visible at once. It applies in both
Cartesian and polar modes — in Cartesian mode each point's distance from the origin
is scaled logarithmically while its direction is preserved. Use it when your data
spans several orders of magnitude and the small values would otherwise crowd into a
dot at the center.

## Clearing and saving

Two runtime commands you send by the window's name:

- `` `CLEAR `` — clears the plot and empties the sample buffer, then waits for new
  data. Use it to start a fresh figure, especially in persistent mode
  (`SAMPLES 0`) where points otherwise never disappear.
- `` `SAVE 'filename.bmp' `` — writes a `.bmp` image of the plot area to the host.
  Add the keyword `WINDOW` before the filename to capture the entire window instead
  of just the plot.

```spin2
debug(`Lissajous CLEAR)              ' wipe the plot
debug(`Lissajous SAVE 'figure.bmp')  ' save the plot area to a file
```

A third runtime command, `` `CLOSE ``, closes the window.

## A complete example: a Lissajous figure

This program drives one SCOPE_XY window with two software sine sources — no
external hardware. The X coordinate is a sine of the phase; the Y coordinate is a
sine of three times the phase. Two sines at a 3:1 frequency ratio draw a stable
Lissajous figure. Both come from the P2's CORDIC engine via the **QSIN** method,
whose signature is `QSIN(length, step, stepsInCircle)` — it returns
`length x sin(step / stepsInCircle x 2pi)`. Passing `360` for `stepsInCircle` lets
you treat `step` as degrees.

```spin2
CON _clkfreq = 100_000_000

PUB main() | ph, x, y
  ' SIZE 256 -> 512x512 plot; RANGE 1000 -> axes span -1000..+1000;
  ' SAMPLES 0 -> persistent (the whole figure accumulates)
  debug(`SCOPE_XY Lissajous SIZE 256 RANGE 1000 SAMPLES 0 'XY')
  ph := 0
  repeat
    x := QSIN(1000, ph, 360)        ' amplitude 1000, fills the range
    y := QSIN(1000, ph * 3, 360)    ' three times the X frequency
    debug(`Lissajous `(x, y))       ' one (x, y) point per pass
    ph += 1
    waitms(5)
```

`QSIN` scales its output by the `length` argument, so an amplitude of `1000`
matches the `RANGE 1000` you set — the figure fills the plot without clipping. The
`waitms(5)` paces the points so you can watch the curve draw itself; remove it and
the figure appears at once.

To turn this into a moving point with a trail instead of a static figure, change
`SAMPLES 0` to a positive depth — say `SAMPLES 60` — and the window keeps only the
60 newest points, fading the older ones. With a single rotating vector that produces
a comet sweeping around a circle:

```spin2
    x := QCOS(800, ph, 360)         ' QCOS gives the X leg
    y := QSIN(800, ph, 360)         ' QSIN gives the Y leg -> a circle
```

## Considerations

- **`SIZE` is a radius; `RANGE` is a symmetric extent.** A `SIZE 256 RANGE 1000`
  plot is 512×512 pixels and maps data from `-1000` to `+1000` on each axis. Match
  your data's amplitude to `RANGE` so the figure fills the plot without clipping;
  values beyond `+/-RANGE` fall outside the visible area.
- **Choose persistence to the job.** `SAMPLES 0` builds a complete, permanent
  figure — right for Lissajous curves and phase portraits you want to read whole.
  A positive `SAMPLES` value draws a fading trail — right for a moving point whose
  recent path matters more than its full history. Larger depths cost more to redraw
  each update, since every kept point is re-plotted with its faded opacity.
- **Use `RATE` to throttle fast data.** With `RATE n` the window repaints once per
  `n` samples received. This reduces host load when you are feeding points faster
  than you need to see them; the samples between repaints are still buffered.
- **Send pairs, not formatted text.** `` `(x, y) `` sends the *values* as a
  coordinate pair. A backtick formatter like `` `udec_(x) `` would send the decimal
  digits as a label string, not plot a point — the same value/format distinction as
  every other window.
- **Match amplitude to `RANGE` with QSIN's `length`.** Because `QSIN`/`QCOS` scale
  by their `length` argument, setting `length` equal to `RANGE` makes a unit-circle
  signal fill the plot. Scale `length` down to shrink the figure.
- **SCOPE vs. SCOPE_XY.** Use SCOPE (Chapter 7) for a value over time; use SCOPE_XY
  for one value against another. Two signals you would view as separate traces in
  SCOPE become a single shape in SCOPE_XY, and that shape is what reveals their phase
  and frequency relationship.

## Try it

Start from the Lissajous example. Then change the frequency ratio — make `y` use
`ph * 2` instead of `ph * 3`, and watch the figure change shape; a `2:1` ratio
draws a different knot than `3:1`. Next, add a small offset to the Y phase
(`QSIN(1000, ph * 3 + 30, 360)`) and watch the figure rotate and open — that offset
is exactly the phase difference a real pair of signals would show. Finally, switch
`SAMPLES 0` to `SAMPLES 80` to trade the static figure for a moving, fading trace,
and add a second channel (declare `'XY'` and a second `'Orbit'` with its own color,
then feed four numbers per pass) to see two figures share the plot at once. You will
have used the creation config, coordinate-pair feeding, persistence, and
multi-channel layout together.
