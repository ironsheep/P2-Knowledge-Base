# Chapter 4: The BITMAP Window — Pixel Raster {#ch-4}

The BITMAP window is the framebuffer of the P2 debug system. You send it pixel
values; it writes them straight into a bitmap canvas, one pixel per value, and
shows the result. It is the window you reach for when your data *is* an image — a
camera frame, a computed pattern, a sensor field, a scrolling persistence display —
or whenever you want to put colored pixels on screen under direct control.

BITMAP displays pixel data and nothing else. It has no drawing primitives: there
is no line, box, circle, or text command in this window. You give it numbers, and
each number becomes a pixel at the current position. How those numbers are
interpreted as color is set by the window's *color mode*; where each pixel lands is
governed by the *trace* pattern. This chapter covers both, along with the control
commands that position, scroll, clear, and save the canvas.

> Keyboard and mouse input (`PC_KEY`, `PC_MOUSE`) work in the BITMAP window, but they
> share one mechanism across every window type, so they are covered together in
> [Chapter 12](#ch-12). This chapter is about output.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=0.50\linewidth]{inbox/assets/fig-04-bitmap.png}
\caption{The BITMAP window showing a synthetic 32×24 thermal-array heatmap.}
\end{figure}
```

## Creating a BITMAP window

You create and configure the window in a single `DEBUG` statement. The first token
after the backtick is the window type (`BITMAP`); the second is a name you choose.
You feed the window afterward by that name:

```spin2
PUB main()
  ' create a 256x256 true-color canvas
  debug(`BITMAP Img SIZE 256 256 RGB24)
  debug(`Img `($FF0000))                  ' write one red pixel
```

The configuration keywords you can add to the creation line:

| Keyword | Arguments | Default | What it sets |
|---------|-----------|---------|--------------|
| `TITLE` | `'text'` | `BITMAP` | The window's title-bar text |
| `POS` | `left top` | auto | Screen position of the window, in pixels |
| `SIZE` | `width height` | `256 256` | Canvas size in pixels; each is **1–2048** |
| `DOTSIZE` | `x [y]` | `1 1` | Pixel magnification for sparse mode; each is **1–256** |
| `SPARSE` | `color` | off | Enable sparse mode; sets the grid-border color |
| *color mode* | (varies) | `RGB24` | One of the 19 color-mode keywords (see below) |
| `LUTCOLORS` | up to 256 `rgb` | (none) | Define the palette for the LUT modes |
| `TRACE` | `mode` | `0` | Scan/scroll pattern, **0–15** (see "Trace patterns") |
| `RATE` | `count` | one scan line | Pixels written between display refreshes |
| `LONGS_1BIT` … `BYTES_4BIT` | — | off | Packed pixel format (see "Packed pixel data") |
| `UPDATE` | — | off | Enables manual update mode (see "Control commands") |
| `HIDEXY` | — | off | Hides the coordinate readout |

`SIZE` sets the canvas in pixels — both dimensions run from 1 to 2048, so the
canvas can be as large as 2048×2048. Memory for two full bitmaps is allocated at
that size, so very large canvases are limited by host memory rather than by the
window itself. Unlike SCOPE or FFT, BITMAP has no margins: the entire canvas is the
drawable area, and pixel (0, 0) is the top-left corner.

## Color modes

A pixel value is just a number until a color mode tells the window how many bits it
carries and how to turn them into a color. You set the mode with one of 19
keywords on the creation line, and you can change it mid-stream (see "Control
commands"). Every mode is converted internally to 24-bit RGB before it reaches the
canvas.

The modes fall into four families:

**Palette (LUT) modes** — index into a 256-entry lookup table you supply with
`LUTCOLORS`:

| Mode | Bits/pixel | Colors | Index |
|------|-----------|--------|-------|
| `LUT1` | 1 | 2 | bit 0 → palette entry 0–1 |
| `LUT2` | 2 | 4 | bits 0–1 → entry 0–3 |
| `LUT4` | 4 | 16 | bits 0–3 → entry 0–15 |
| `LUT8` | 8 | 256 | byte → entry 0–255 |

`RGB24` is the window's default color mode — not a LUT mode. If you select a LUT
mode without defining a palette, the palette is uninitialized and LUT-mode pixels
render as garbage — you must supply one with `LUTCOLORS`.

**Luminance and RGB-intensity modes** — 8-bit value mapped against a single tint
color you pick with a color-tune keyword:

| Mode | Meaning |
|------|---------|
| `LUMA8` / `LUMA8W` / `LUMA8X` | Brightness in one color: black-base, white-base, expanded-range |
| `RGBI8` / `RGBI8W` / `RGBI8X` | Upper 3 bits select a color, lower 5 bits are intensity |

For the LUMA modes you name the tint color after the keyword (for example,
`LUMA8 GREEN`); the 8-bit value then runs that color from dark to bright. The `W`
variants run from white toward the color; the `X` variants expand the value range.

**HSV (hue/value) modes** — pack a hue and a brightness into each pixel:

| Mode | Bits/pixel | Layout |
|------|-----------|--------|
| `HSV8` / `HSV8W` / `HSV8X` | 8 | 4-bit hue, 4-bit value |
| `HSV16` / `HSV16W` / `HSV16X` | 16 | 8-bit hue, 8-bit value |

Hue maps around a color wheel (red → yellow → green → cyan → blue → magenta → red);
value sets brightness. As with the luminance modes, `W` runs from white and `X`
expands the range.

**Direct RGB modes** — the value *is* the color:

| Mode | Bits/pixel | Layout |
|------|-----------|--------|
| `RGB8` | 8 | 3:3:2 (RRRGGGBB) |
| `RGB16` | 16 | 5:6:5 (RRRRRGGGGGGBBBBB) |
| `RGB24` | 24 | 8:8:8 (full color, `$RRGGBB`) |

`RGB24` carries a full color in every pixel and needs no palette — it is the
simplest mode to reason about when each pixel's color is computed independently.
`RGB16` (5:6:5) and `RGB8` (3:3:2) trade color depth for bandwidth.

Only one color mode is active at a time. Pixels you sent earlier are already
rendered and do not change when you switch modes; the new mode applies to every
pixel that follows.

### Defining a palette

For the LUT modes, `LUTCOLORS` loads the palette. It reads up to 256 RGB24 values
and stores them as palette entries 0, 1, 2, and so on. Send the keyword and all of
its colors in one `DEBUG` statement, because the window stops reading palette
entries at the first non-numeric element:

```spin2
PUB main() | x, y
  ' LUT4: a 16-color palette defined inline
  debug(`BITMAP Tiles SIZE 16 16 LUT4 LUTCOLORS ...
         $000000 $202020 $400000 $004000 ...
         $000040 $404000 $004040 $400040 ...
         $808080 $C0C0C0 $FF0000 $00FF00 ...
         $0000FF $FFFF00 $00FFFF $FFFFFF)
  repeat y from 0 to 15
    repeat x from 0 to 15
      debug(`Tiles `((x ^ y) & $0F))  ' each pixel is a 4-bit palette index
```

Because the pixels store palette *indices*, you can resend `LUTCOLORS` later to
recolor the whole image without redrawing a single pixel — the canvas reinterprets
its stored indices through the new palette.

## Sending pixel data

Once the window exists, every number you send by its name becomes a pixel. You send
a value with `` `() `` — the parentheses send the *value* of the expression, not its
visible digits:

```spin2
debug(`Img `(color))      ' write one pixel = the value of `color`
debug(`Img `($FF7F00))    ' write one orange pixel (RGB24)
```

Each pixel is plotted at the current position, and then the position advances to the
next pixel according to the trace pattern. You do not address pixels individually in
the common case; you stream them, and the trace pattern lays them out for you.

### Trace patterns

The trace pattern decides where the first pixel goes and which way the position
steps after each pixel. It is a 4-bit value set with `TRACE`: the low three bits
choose one of eight scan patterns, and bit 3 turns on scrolling.

The eight scan patterns (bit 3 clear, values 0–7):

| `TRACE` | Start corner | Step direction | At end of line |
|---------|-------------|----------------|----------------|
| `0` | top-left | left → right | next line down, wrap |
| `1` | top-right | right → left | next line down, wrap |
| `2` | bottom-left | left → right | next line up, wrap |
| `3` | bottom-right | right → left | next line up, wrap |
| `4` | top-left | top → bottom | next column right, wrap |
| `5` | bottom-left | bottom → top | next column right, wrap |
| `6` | top-right | top → bottom | next column left, wrap |
| `7` | bottom-right | bottom → top | next column left, wrap |

Patterns 0–3 scan horizontally (the X axis advances every pixel); patterns 4–7 scan
vertically (the Y axis advances every pixel). Pattern 0 is the default and gives the
familiar TV-raster layout: pixels fill left-to-right, top-to-bottom, and the
position wraps back to the top after the last pixel.

Adding 8 to any pattern sets bit 3 and turns the end-of-line wrap into a **scroll**.
Instead of wrapping to the opposite edge, the whole canvas shifts by one line and
the vacated line is filled with the background color, so new data always lands at the
leading edge:

| `TRACE` | Behavior |
|---------|----------|
| `8` | top line, left → right, scroll **down** |
| `10` | bottom line, left → right, scroll **up** |
| `12` | left column, top → bottom, scroll **right** |
| `14` | right column, top → bottom, scroll **left** |

(Values 9, 11, 13, 15 are the reverse-direction variants of these four.) A scrolling
trace turns BITMAP into a chart recorder: each batch of pixels becomes a new line at
the top while older lines march down the canvas.

Setting `TRACE` resets the position to the new pattern's start corner. The default
`RATE` also follows from the pattern — horizontal patterns refresh every `width`
pixels (one row), vertical patterns every `height` pixels (one column).

### Packed pixel data

The DEBUG serial link is the bottleneck for any sizable image, so BITMAP can unpack
several pixels from each number you send. You enable a packing format on the
creation line or mid-stream; from then on, each number is split into multiple
pixels before plotting.

The formats name the container size and the bits per pixel, running from
`LONGS_1BIT` (32 one-bit pixels per long) through `BYTES_4BIT` (2 four-bit pixels
per byte). `LONGS_1BIT` gives the largest bandwidth saving — 32× — and pairs
naturally with `LUT1`:

```spin2
PUB main() | x, y, packed, bit
  ' LONGS_1BIT: 32 one-bit pixels packed into each long
  debug(`BITMAP Mono SIZE 32 32 LUT1 LONGS_1BIT)
  repeat y from 0 to 31
    packed := 0
    repeat x from 0 to 31
      bit := ((x ^ y) >> 2) & 1
      packed |= bit << x
    debug(`Mono `(packed))    ' one long -> 32 pixels of one row
```

Choose a canvas width divisible by the pack count so each packed value lines up with
a whole number of pixels; otherwise a value's pixels can straddle a line boundary.

### Random-access writes with SET

When you do not want to stream, `SET` positions the pixel cursor directly. It takes
an X and a Y (each must lie within the canvas bounds — an out-of-range coordinate
is ignored, not clamped) and cancels any scrolling on the active pattern. The next pixel value you send lands at that position:

```spin2
PUB main() | x, y, v
  debug(`BITMAP Dots SIZE 128 128 RGB24 UPDATE)
  repeat 200
    x := getrnd() +// 128            ' GETRND gives the coordinates
    y := getrnd() +// 128
    v := getrnd() & $FFFFFF          ' and the color
    debug(`Dots SET `(x, y) `(v))    ' place one pixel at (x, y)
  debug(`Dots UPDATE)                ' show the result once
```

Use `SET` for scattered or non-sequential writes; use a trace pattern when the data
arrives in scan order.

## Control commands

These commands are sent at runtime, prefixed with a backtick, by the window's name.
Several change configuration mid-stream; the rest manage the display.

| Command | Arguments | Effect |
|---------|-----------|--------|
| *color mode* | (varies) | Switch the active color mode for following pixels |
| `LUTCOLORS` | up to 256 `rgb` | Reload the palette (LUT modes) |
| `TRACE` | `mode` | Switch scan/scroll pattern; resets position to its start corner |
| `RATE` | `count` | Set pixels written between display refreshes |
| `SET` | `x y` | Position the pixel cursor; cancels scrolling |
| `SCROLL` | `x y` | Shift the canvas by `x`, `y` pixels; fill the vacated strips |
| `CLEAR` | — | Fill the canvas with the background color; reset position |
| `UPDATE` | — | Refresh the display now (required in manual-update mode) |
| `SAVE` | — | Save the current canvas image to a file on the host |
| `CLOSE` | — | Close this window and free its resources |

`SCROLL` shifts the whole canvas by a signed amount: positive `x` scrolls right,
negative left; positive `y` scrolls down, negative up. Each argument ranges over
±canvas-dimension, and the strip exposed by the shift is filled with the background
color. This is the manual counterpart to a scrolling trace — use it to pan an image
or reposition a waveform.

`CLEAR` fills the canvas with the background color and returns the pixel position to
the active pattern's start corner. Unless the window is in manual-update mode, it
refreshes the display immediately.

`UPDATE` and manual-update mode work together. By default the canvas repaints
automatically as pixels arrive (every `RATE` pixels). Add `UPDATE` to the creation
line and the window stops repainting on its own; your pixels accumulate off-screen
and appear only when you send the `` `UPDATE `` command. This gives you whole-frame,
flicker-free updates — write an entire frame, then show it at once.

`RATE` tunes the automatic-update cadence: the display refreshes once every `count`
pixels. A small count repaints often (smoother, slower); a large count repaints
rarely (faster, choppier). The default is one scan line — `width` pixels for
horizontal patterns, `height` for vertical; `RATE -1` selects a full canvas
(`width × height`).

`SAVE` writes the current canvas to an image file on the host running
`pnut_term_ts`.

## A complete example

This program animates a **thermal-array heatmap**. A 32×24 grid stands in for a
thermopile sensor like the MLX90640 — the kind of low-resolution infrared array
you would point at a board to find a hot component, or at a doorway to count
people. Each cell holds a temperature; the program renders a slowly drifting warm
spot over a cool background. No hardware is involved — the temperatures are
computed in software — but the data has exactly the shape a real array would
produce.

The canvas is only 32×24 logical cells, so each is magnified to a 12-pixel block
with `DOTSIZE` and `SPARSE` (the magnified, low-resolution display the window is
built for). `LUMA8 RED` maps each cell's 8-bit temperature from dark (cool) to
bright (hot):

```spin2
CON
  _clkfreq = 200_000_000
  COLS = 32                                ' a 32x24 thermopile array
  ROWS = 24                                '   (MLX90640-class)

PUB main() | x, y, ang, cx, cy

  ' 32x24 grid: each cell a 12px block with grid border; temperature -> tint
  debug(`BITMAP Heat SIZE 32 24 DOTSIZE 12 SPARSE GRAY LUMA8 RED UPDATE)

  ang := 0
  repeat
    ' the warm spot drifts slowly across the array
    cx := 16 + qsin(10, ang, 256)
    cy := 12 + qsin(7, ang*2, 256)
    debug(`Heat CLEAR)
    repeat y from 0 to ROWS-1
      repeat x from 0 to COLS-1
        debug(`Heat `(cell(x, y, cx, cy)))
    debug(`Heat UPDATE)
    ang += 3
    waitms(250)                            ' ~4 fps, like a real thermopile

PRI cell(x, y, cx, cy) : temp | dx, dy, d2
  ' synthetic temperature: a warm peak at (cx,cy) over a cool ambient
  dx := x - cx
  dy := y - cy
  d2 := dx*dx + dy*dy
  temp := (220 - d2*3) #> 0                 ' peak falls off with distance
  temp := (temp + 30) <# 255                ' add ambient, clamp to a byte
```

Each frame: `CLEAR` resets the canvas, the nested loops stream all 768 cell values
in raster order under the default trace, and `UPDATE` paints the finished frame at
once. Moving the spot's center (`cx`, `cy`) each pass makes the hot region drift.

The size of this image is the lesson. A 32×24 array is 768 values; even sent as a
full byte each and refreshed a few times a second, that is only a couple of
kilobytes per second — comfortably inside the debug link's budget
([Chapter 1](#ch-1)). A small, slow sensor grid is exactly the kind of "image" the
link carries well. A live *camera* frame is the opposite case: 320×240 in `RGB24`
is about 230 KB, more than a second of link, so video would crawl in at well under
one frame per second. When your image is a sensor field of tens or hundreds of
cells at a few Hz, BITMAP is the right window; when it is full-motion video, it is
not.

### Where you'd use this

In computer science and computer engineering, the BITMAP window is for **computer
vision and framebuffer visualization** — seeing the pixels a program produced or
consumed — and for **2D scalar-field visualization**, where a grid of values is
clearest as a colored field rather than a table of numbers.

**On an embedded project**, you reach for it to show a thermal-array heatmap (as
here), to preview an LED-matrix framebuffer before it goes to the panel, to
visualize a capacitive-touch grid, or to map signal strength or occupancy across a
grid of sensors.

**Bandwidth fit:** small or slow grids — sensor arrays, LED matrices, touch grids,
a few hundred to a few thousand cells at a few Hz — stream comfortably; live camera
video does not fit and is out.

**Extension (real hardware):** replace the synthetic `cell` temperatures with a
real I²C read from an MLX90640 (or any sensor grid) into the same per-cell values,
and the heatmap shows live infrared.

## Considerations

- **Match the color mode to the data.** `RGB24` is simplest when each pixel's color
  is computed on its own. The LUT modes are smaller per pixel and let you recolor an
  image by reloading the palette. The HSV and LUMA modes map a single magnitude to a
  color, which suits sensor fields and heat maps.
- **Packing buys bandwidth.** A full `RGB24` frame is three bytes per pixel; the DEBUG
  link cannot stream large true-color frames quickly. For higher frame rates, drop to
  a LUT mode and a packed format (`LONGS_1BIT` with `LUT1` packs 32 pixels per long).
- **Pick the trace pattern to the layout.** Pattern 0 for raster images; a scrolling
  pattern (8, 10, 12, 14) for chart-recorder and persistence displays where new data
  enters at one edge.
- **Use manual update for whole frames.** When you redraw the entire canvas each
  pass, `UPDATE` mode prevents the partial-frame flicker you would see with automatic
  refresh. For a steadily growing image, automatic refresh with a suitable `RATE` is
  simpler.
- **Sparse mode is for magnified, low-resolution displays.** `DOTSIZE` with `SPARSE`
  draws each logical pixel as a `DOTSIZE`-square block with a grid border — useful for
  LED-matrix and pixel-art views — but it renders far more slowly than the 1:1 path,
  so keep the logical canvas small.
- **There are no drawing primitives here.** BITMAP plots pixels only. For lines,
  shapes, text, and sprites, use the PLOT window ([Chapter 5](#ch-5)), which shares BITMAP's
  color modes but adds a coordinate system and drawing commands.

## Try it

Start with the heatmap example. First widen the temperature range or move the spot
faster and watch the tint track it. Then switch the color mode: change `LUMA8 RED`
to `HSV16` and feed each cell a hue computed from its temperature — cool cells blue,
hot cells red — for the classic rainbow thermal palette. Next, make a different
kind of display: drop `SPARSE`/`DOTSIZE`, set `SIZE 128 128` and `TRACE 8`, and send
one row of values per pass to turn the window into a scrolling chart recorder. You
will have exercised creation config, two color modes, sparse and full canvases, a
scrolling trace, and manual updates in a single program.
