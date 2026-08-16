# Chapter 5: The PLOT Window — Vector Drawing Canvas {#ch-5}

The PLOT window is a vector drawing canvas. You move a drawing cursor around a
2D surface and issue primitives — dots, lines, circles, ovals, rectangles,
rounded rectangles, and rotated text — that the window renders with
anti-aliasing. On top of the primitives it gives you a coordinate system you can
re-origin and flip, a polar mode, per-element opacity, eight bitmap layers you
can composite with `CROP`, and a 256-entry sprite system. It is the window you
reach for when you need a custom instrument face, a graph, a geometric figure,
or any picture that is not a text grid ([Chapter 3](#ch-3), TERM) or a raw pixel buffer
([Chapter 4](#ch-4), BITMAP).

You create one PLOT window per `` DEBUG(`PLOT ...) `` declaration, give it a name,
and from then on address it by that name. This chapter covers everything the
window does: creating it, the coordinate system, the drawing primitives, color
and opacity, the layer/CROP/sprite system, and the update model that controls
when your drawing becomes visible.

> Keyboard and mouse input (`PC_KEY`, `PC_MOUSE`) work in the PLOT window — the
> window can report the cursor position and the color under it — but that
> mechanism is shared across every window type, so it is covered in [Chapter 12](#ch-12).
> This chapter is about drawing.

## Creating a PLOT window

You create and configure a window in a single `DEBUG` statement. The first token
after the backtick is the window type (`PLOT`); the second is a name you choose.
You feed the window afterward by that name:

```spin2
PUB main()
  debug(`PLOT Canvas SIZE 512 512)  ' create a 512x512 canvas named "Canvas"
  debug(`Canvas COLOR $00FF00 SET 256 256 DOT)   ' a green dot at the center
```

The configuration keywords you can add to the creation line:

| Keyword | Arguments | Default | What it sets |
|---------|-----------|---------|--------------|
| `TITLE` | `'text'` | `<name> - PLOT` | The window's title-bar text |
| `POS` | `left top` | host-placed | Screen position of the window, in pixels |
| `SIZE` | `width height` | `256 256` | Canvas size in pixels; each is **32–2048** |
| `DOTSIZE` | `x {y}` | `1 1` | Pixel magnification; each axis **1–256** |
| color mode | `LUT1` … `RGB24` | `RGB24` | How color values are interpreted ([Chapter 4](#ch-4)) |
| `LUTCOLORS` | `rgb24 rgb24 ...` | (LUT is all black) | Loads the palette used by the `LUT1`–`LUT8` modes |
| `BACKCOLOR` | `rgb` | black | Background fill color (`$RRGGBB`) |
| `UPDATE` | — | off | Enables buffered mode (see "The update model") |
| `HIDEXY` | — | off | Hides the mouse-coordinate readout |

If you omit `POS`, the window is placed by whatever tool is hosting the debug
session — do not count on a particular screen position, or on windows avoiding
one another. Give `POS` explicitly when the layout matters.

PLOT draws in full `RGB24` unless you select one of the other color modes — the
same 19 modes the BITMAP window uses, described in [Chapter 4](#ch-4). If you
select a `LUT` mode, load the palette with `LUTCOLORS`: the LUT is zero-filled at
creation, so **every index resolves to black until you load it**.

`SIZE` is measured in pixels, and both dimensions are clamped to the range
**32–2048**. The default is `256 256`. The canvas is drawn into an off-screen
bitmap and stretched to fill the window, so resizing the window scales the
picture rather than revealing more canvas.

`DOTSIZE` magnifies the canvas: a `DOTSIZE 2` window renders each canvas pixel as
a 2×2 block, which is useful when you want a small drawing shown large. The two
axes can differ.

`CARTESIAN`, `POLAR`, and `TEXTSIZE` are **feeding commands, not
window-instantiation keywords** — they belong to the drawing you feed the window,
not to how the window is created, which is why they are not in the table above.
`CARTESIAN` and `POLAR` select the coordinate system; `TEXTSIZE` sets the default
font size for `TEXT` (default `10`, range 6–200). They are described in the
sections that follow.

## The coordinate system

Every drawing primitive is placed relative to a **drawing cursor** — a current
(x, y) position you move with `SET`, and that some primitives advance on their
own. The cursor's coordinates are interpreted through the active coordinate
system, which you control with `ORIGIN`, `CARTESIAN`, and `POLAR`.

### Cartesian mode

Cartesian is the default. Out of the box the origin is the bottom-left corner,
**x increases rightward, and y increases upward** — the mathematical convention.
You change that with `CARTESIAN`:

```debug-update
CARTESIAN {flipy {flipx}}
```

- `flipy` — `0` leaves y increasing upward (default, the mathematical
  convention); `1` flips y to increase **downward**, the screen convention.
- `flipx` — `0` leaves x increasing rightward (default); `1` makes x increase
  **leftward**.

Both arguments are optional; sending `CARTESIAN` with no arguments returns to
Cartesian mode (from polar) without changing the flips.

### ORIGIN — moving the reference point

`ORIGIN` sets the point that coordinate (0, 0) maps to:

```debug-update
ORIGIN {x y}
```

- `ORIGIN x y` — place the origin at the pixel (x, y). `ORIGIN 256 256` centers
  the origin of a 512×512 canvas.
- `ORIGIN` with no arguments — place the origin at the *current cursor position*.
  Move the cursor with `SET`, then `ORIGIN`, and the origin is wherever the cursor
  was.

All subsequent coordinates are measured from the origin, so re-origining lets you
draw a figure in its own local coordinates and place it anywhere.

```spin2
PUB main()
  debug(`PLOT Centered SIZE 512 512)
  debug(`Centered ORIGIN 256 256)        ' (0,0) is now the canvas center
  debug(`Centered SET 100 100 DOT 6 255) ' a dot up-and-right of center
```

### SET — moving the cursor

`SET` places the drawing cursor. Its two arguments are required, but they take
different names depending on the active coordinate system:

```debug-update
SET x y          ' Cartesian: x, y
SET rho theta    ' polar: radius, angle
```

`SET` does not draw anything; it positions the cursor for the next primitive.
(Polar mode is covered below.)

### Polar mode

`POLAR` switches the window so that the cursor's two coordinates are interpreted
as **(rho, theta)** — radius and angle — and converted to Cartesian internally:

```debug-update
POLAR {twopi {theta}}
```

- `twopi` — the numeric value that represents one full turn (360°). The default
  is `$1_0000_0000` (2³²). Choosing a power of two here makes the angle math
  convenient: with `POLAR $1_0000`, a full circle is 65 536, a quarter turn is
  `$4000`, and so on. A negative `twopi` reverses the rotation direction.
- `theta` — an angular offset added to every angle, which rotates the entire
  coordinate system.

The default `twopi` of `$1_0000_0000` is one count too large for a 32-bit
argument, so it has a **shorthand**: write `POLAR 0` for `$1_0000_0000` and
`POLAR -1` for `-$1_0000_0000`. `POLAR 0` is therefore not "a full turn of zero"
— it selects the full 32-bit angle scale, which is exactly what `QROTATE` and
`QSIN` produce.

By default the angle is measured the mathematical way: `theta` = 0 points **East**
(along +x), and increasing `theta` sweeps **counter-clockwise** (a negative `twopi`,
above, flips that sweep to clockwise). The `theta` offset then rotates this whole
system to a new zero direction.

With the origin at the canvas center, polar mode draws radial figures directly:

```spin2
PUB main() | theta
  debug(`PLOT Rose SIZE 512 512 BACKCOLOR $000000)
  debug(`Rose ORIGIN 256 256 POLAR $1_0000)
  debug(`Rose COLOR $00FFFF)
  debug(`Rose SET 0 0)
  repeat theta from 0 to $1_0000
    debug(`Rose LINE 200 `(theta) 1 255)   ' spokes of a wheel, radius 200
```

Send `CARTESIAN` to leave polar mode.

### PRECISE — sub-pixel positioning

Coordinates are stored internally in a fixed-point format, and `PRECISE` decides
whether you address that format directly. `PRECISE` mode starts **off**: `DOT`
and `LINE` take whole-pixel coordinates and line sizes, which is what you want
for most drawing. `PRECISE` toggles it:

```debug-update
PRECISE
```

With `PRECISE` **on**, the line size and the (x, y) of `DOT` and `LINE` are
expressed in **256ths of a pixel**, so an anti-aliased primitive can land on a
sub-pixel position — the right choice for smooth curves and animation, where
rounding every point to an integer pixel makes motion visibly step. In this mode
a coordinate of `256` means *one pixel*, not 256 of them: scale your values up by
256 (`x << 8`) when you turn it on.

Each `PRECISE` flips the mode. Because sub-pixel is **not** the default, the
first `PRECISE` switches **to** sub-pixel mode; a second returns to whole pixels.

> **Read coordinates through the active system.** A primitive's position is
> always the cursor, transformed by polar conversion (if active), then the
> origin offset, then the axis flips. Set the system once with `ORIGIN` /
> `CARTESIAN` / `POLAR`, and every following primitive obeys it.

## Drawing primitives

The window provides six geometric primitives plus text. Each is drawn at — or,
for `LINE`, *to* — the current cursor, in the current color, with anti-aliasing.
Where a primitive takes `linesize` and `opacity`, both are optional — but an
omitted `linesize` does **not** mean the same thing everywhere:

- For `DOT` and `LINE` it falls back to the window's `LINESIZE` (default `1`).
- For the four shapes — `CIRCLE`, `OVAL`, `BOX`, `OBOX` — it falls back to
  **`0`, which means *filled***, not to the window's `LINESIZE`.

An omitted `opacity` always falls back to the window's `OPACITY`.

### DOT — a dot at the cursor

```debug-update
DOT {linesize {opacity}}
```

- `linesize` — dot diameter in pixels.
- `opacity` — alpha, `0`–`255` (`255` = opaque).

`DOT` draws at the cursor and **does not move it**.

```spin2
' semi-transparent blue dot
debug(`Canvas COLOR $0000FF SET 100 100 DOT 10 128)
```

### LINE — a line to a new point

```debug-update
LINE x y {linesize {opacity}}
```

`LINE` draws from the current cursor to (x, y) — or (rho, theta) in polar mode —
then **moves the cursor to that endpoint**. Because the cursor advances, you draw
a connected path by issuing `LINE` repeatedly:

```spin2
PUB main()
  debug(`PLOT Canvas SIZE 512 512)
  debug(`Canvas COLOR $FFFFFF SET 0 0)
  debug(`Canvas LINE 100 0 LINE 100 100 LINE 0 100 LINE 0 0)  ' a square
```

- `linesize` — line thickness in pixels.
- `opacity` — alpha, `0`–`255`.

### CIRCLE — a circle centered on the cursor

```debug-update
CIRCLE width {linesize {opacity}}
```

- `width` — diameter in pixels.
- `linesize` — outline thickness; **`0` (the default) fills the circle**, a
  value greater than zero draws an outline of that thickness.
- `opacity` — alpha, `0`–`255`.

```spin2
debug(`Canvas COLOR $FF0000 SET 256 256)
debug(`Canvas CIRCLE 100 0 255)    ' filled red disc, diameter 100
debug(`Canvas CIRCLE 120 5 255)    ' red ring, diameter 120, 5-pixel outline
```

### OVAL — an ellipse centered on the cursor

```debug-update
OVAL width height {linesize {opacity}}
```

`width` and `height` are the horizontal and vertical diameters; `linesize` and
`opacity` behave as for `CIRCLE` (`0` linesize fills).

```spin2
' filled ellipse
debug(`Canvas COLOR $00FF00 SET 256 256 OVAL 200 100 0 255)
```

### BOX — a rectangle centered on the cursor

```debug-update
BOX width height {linesize {opacity}}
```

`width` and `height` are the rectangle dimensions; `linesize` `0` fills, greater
than zero outlines. The rectangle is centered on the cursor.

```spin2
debug(`Canvas COLOR $0000FF SET 100 100 BOX 80 60 0 255)  ' filled rectangle
debug(`Canvas BOX 90 70 3 128)  ' outline, thickness 3
```

### OBOX — a rounded rectangle centered on the cursor

```debug-update
OBOX width height xradius yradius {linesize {opacity}}
```

`OBOX` adds corner-radius arguments: `xradius` and `yradius` set the horizontal
and vertical rounding of the corners. As with the other shapes, `linesize` `0`
fills and greater than zero outlines.

```spin2
debug(`Canvas COLOR $FFFF00 SET 256 256)
debug(`Canvas OBOX 100 80 10 10 0 255)    ' filled, 10-pixel rounded corners
debug(`Canvas OBOX 120 100 15 15 4 200)   ' outline, thickness 4
```

### TEXT — a string at the cursor

```debug-update
TEXT {size {style {angle}}} 'string'
```

`TEXT` renders the string at the cursor, in the **text color**. All three numeric
arguments are optional and default to the window's current text size, style, and
angle:

- `size` — font size in points.
- `style` — a style byte (below).
- `angle` — rotation in degrees, `0`–`359`. In polar mode the angle is given in
  `twopi` units instead.

> **`COLOR` only reaches `TEXT` when `TEXT` comes next.** The window keeps the
> text color *separately* from the drawing color, and a `COLOR` command updates
> it **only when the very next key is `TEXT`**. Put `COLOR` immediately before
> each `TEXT`, in the same `DEBUG` statement. If anything intervenes — even a
> `SET` — the text keeps its previous color, which starts out **white**. On a
> light background that is invisible text, and nothing in the output tells you
> why.

```spin2
PUB main()
  debug(`PLOT Labels SIZE 600 400 BACKCOLOR $FFFFFF)
  debug(`Labels TEXTSIZE 14)
  ' COLOR sits immediately before each TEXT -- that is what makes it black
  ' size 14 -- the window default
  debug(`Labels SET 300 300 COLOR $000000 TEXT 'Default')
  debug(`Labels SET 300 200 COLOR $000000 TEXT 20 'Bigger') ' size 20
  ' size 16, bold, rotated 90 degrees
  debug(`Labels SET 300 100 COLOR $000000 TEXT 16 $02 90 'Rotated')
```

The `style` byte packs weight, italic, underline, and alignment into one value:

| Bits | Field | Values |
|------|-------|--------|
| 0–1 | Weight | `0`=thin, `1`=normal, `2`=bold, `3`=heavy |
| 2 | Italic | `0`=normal, `1`=italic |
| 3 | Underline | `0`=none, `1`=underline |
| 4–5 | Horizontal align | `0`/`1`=center, `2`=right, `3`=left |
| 6–7 | Vertical align | `0`/`1`=center, `2`=top, `3`=bottom |

So `$02` is bold, `$06` is bold + italic, `$0A` is bold + underline, and
`$20` right-aligns. The default style is `$01` (`%00000001`): **normal** weight,
centered both ways.

The weight field selects a *nominal* font weight, but the DEBUG display font does
not render it as a weight progression: `$00` looks identical to the `$01` default,
and `$02`/`$03` are *not* heavier — if anything they render with slightly less ink,
not more. Don't rely on the weight field to make text bolder.

You can set the text defaults independently with `TEXTSIZE size`, `TEXTSTYLE
style`, and `TEXTANGLE angle`; a later `TEXT` that omits an argument uses the
default you set.

## Color and opacity

The PLOT window draws in 24-bit RGB. You set the active drawing color with
`COLOR`:

```debug-update
COLOR rgb
```

The argument is a `$RRGGBB` value — for example `COLOR $FF0000` is red,
`COLOR $00FF00` is green, `COLOR $0000FF` is blue. Named colors (`RED`, `GREEN`,
`BLUE`, `WHITE`, `BLACK`, `CYAN`, `MAGENTA`, `YELLOW`, `ORANGE`, `GRAY`) are also
accepted in the command stream, each with an optional `0`–`15` brightness — but a
keyword resolves to a *computed* color, not to the palette value of the same name
([Appendix C](#appendix-c)). Until you set `COLOR`, the default drawing color is
cyan (`$00FFFF`).

`COLOR` sets the color the *primitives* draw in. The **text** color is a separate
setting, and `COLOR` updates it only when `TEXT` is the next key — so a `COLOR`
meant for a label must sit immediately before that label's `TEXT`.

`BACKCOLOR rgb` sets the background fill — the color `CLEAR` paints the canvas
with. It is most often set on the creation line.

`OPACITY` sets the default alpha applied to primitives that do not specify their
own:

```debug-update
OPACITY byte
```

The value is a byte `0`–`255`, where `255` is fully opaque and lower values blend
the primitive with whatever is already on the canvas. A per-primitive `opacity`
argument (the last argument of `DOT`, `LINE`, `CIRCLE`, and the rest) overrides
this default for that one primitive.

> **`OPACITY 256` makes everything vanish.** The value is stored in a byte and it
> is **not** clamped — it wraps. Reach past the top of the range for "as opaque as
> possible" and `256` wraps to **`0`, fully transparent**: every primitive you draw
> next is invisible, with no error and no clue. The most opaque value is **`255`**.
> (Hardware-verified.)

```spin2
PUB main()
  debug(`PLOT Blend SIZE 512 512 BACKCOLOR $000000)
  debug(`Blend COLOR $FF0000 OPACITY 128)        ' default to 50% opacity
  debug(`Blend SET 128 128 BOX 100 100 0 255)  ' this box overrides: opaque
  debug(`Blend SET 180 128 BOX 100 100)  ' this box uses the 128 default
```

`LINESIZE size` sets the default line/dot thickness, in pixels, used when `DOT`
and `LINE` omit their `linesize` argument. The default is `1`. (It does not reach
the shapes — an omitted shape `linesize` is `0`, which fills.)

## Layers, CROP, and sprites

Beyond live primitives, the PLOT window holds **eight bitmap layers** and a
**256-entry sprite table**. Both let you assemble a picture from prebuilt pieces
rather than redrawing primitives every frame: you composite a layer or stamp a
sprite with a single command, which avoids re-issuing the geometry that built it.

> **`LAYER`/`CROP` need `{Spin2_v50}`.** The hidden-bitmap `LAYER` and `CROP`
> commands are V50 additions; `SPRITEDEF` and `SPRITE` were added earlier (V35n).
> Because this section uses `LAYER` and `CROP`, build it with a Spin2 v50+
> `pnut-ts` and put `{Spin2_v50}` (or later) on the source file's first line;
> without that, those two commands are not recognized.

### LAYER — load a bitmap into a layer

```debug-update
LAYER layer 'filename.bmp'
```

`LAYER` loads a Windows BMP file from the host into one of the eight layers; one
BMP pixel maps to one canvas pixel with no scaling, so author the image at the exact
pixel size you will display it. A 24-bit, uncompressed BMP is the safe choice.

- `layer` — the layer index, **`1`–`8`** (there is no layer 0).
- `filename` — a path to a file that must exist on the host and must end in
  `.bmp`. If the file is missing or has the wrong extension, the command is
  ignored.

Because the bitmap is read from the host filesystem, `LAYER` depends on a file
being present on the machine running `pnut-term-ts`; it is not generated by the
P2. The command form is what your P2 program sends; the artwork is supplied
host-side.

### CROP — composite a layer onto the canvas

`CROP` copies pixels from a loaded layer onto the main canvas. It has three forms:

```debug-update
CROP layer
CROP layer AUTO x y
CROP layer left top width height {x y}
```

- `CROP layer` — copy the entire layer to the canvas at (0, 0).
- `CROP layer AUTO x y` — copy the entire layer to the canvas at (x, y).
- `CROP layer left top width height {x y}` — copy a rectangular region of the
  layer — starting at (`left`, `top`) and `width`×`height` in size — to the
  canvas. The destination defaults to (`left`, `top`) and can be overridden with
  the optional trailing (`x`, `y`).

The copy is a pixel-for-pixel block transfer with no scaling, and in the default
pixel format it is an **opaque** block copy, so each `CROP` overwrites its
destination rectangle completely. That is why there is no separate "clear": you *erase by restoring* —
copy clean background back over a region (the second form) or repaint the whole scene
(the first form). [Chapter 15](#ch-15) builds the sprite-sheet panel technique on
these three idioms.

### SPRITEDEF and SPRITE — defining and stamping sprites

A sprite is a small palette-indexed bitmap, up to 32×32 pixels, that you define
once and then stamp anywhere, at any of eight orientations and any scale.

`SPRITEDEF` defines one:

```debug-update
SPRITEDEF id xsize ysize pixels... colors...
```

- `id` — sprite identifier, **`0`–`255`**.
- `xsize`, `ysize` — sprite dimensions, each **`1`–`32`**.
- `pixels` — `xsize x ysize` palette indices, one per pixel, in row order.
- `colors` — the palette entries the pixel bytes reference, in `$AARRGGBB` form
  (alpha, red, green, blue), where alpha `$00` is transparent and `$FF` is opaque.
  Supply **up to 256**, but only as many as your indices actually use — the parser
  reads color longs until the `DEBUG()` message ends, so a sprite that uses indices
  0 and 1 needs just two colors.

`SPRITE` stamps a defined sprite at the cursor:

```debug-update
SPRITE id {orientation {scale {opacity}}}
```

- `id` — which sprite to draw, **`0`–`255`**.
- `orientation` — **`0`–`7`**, selecting one of the eight ways a square can be
  laid down. It is not a rotation counter — it is **three independent bits** that
  compose: bit 0 flips X, bit 1 flips Y, and bit 2 **transposes** (swaps the two
  axes). So `4` on its own is a diagonal mirror, and the 90° rotations are the
  combinations that pair the transpose with a flip:

  | Code | Bits | Result |
  |------|------|--------|
  | `0` | `%000` | normal |
  | `1` | `%001` | flip X |
  | `2` | `%010` | flip Y |
  | `3` | `%011` | flip X + flip Y (= 180° rotation) |
  | `4` | `%100` | transpose (mirror about the main diagonal) |
  | `5` | `%101` | transpose + flip X (a 90° rotation) |
  | `6` | `%110` | transpose + flip Y (the other 90° rotation) |
  | `7` | `%111` | transpose + both flips (the anti-diagonal mirror) |

- `scale` — pixel magnification, **`1`–`64`**; each sprite pixel becomes a
  `scale x scale` block.
- `opacity` — an overall alpha multiplier, `0`–`255`, applied on top of each
  pixel's own alpha.

```spin2
PUB main()
  debug(`PLOT Scene SIZE 512 512 BACKCOLOR $000000 UPDATE)
  debug(`Scene CLEAR)
  debug(`Scene LAYER 1 'background.bmp')          ' host-supplied artwork
  debug(`Scene CROP 1)  ' composite full background
  ' tiny 2x2 sprite
  debug(`Scene SPRITEDEF 0 2 2 0 1 1 0 $00000000 $FFFFFFFF)
  debug(`Scene SET 256 256 SPRITE 0 0 8 255)      ' stamp it, 8x scale
  debug(`Scene UPDATE)  ' present the buffered frame
```

> **Layers are indexed 1–8.** A common error is using layer 0; the lowest valid
> layer is 1, and `LAYER`/`CROP` ignore an index outside 1–8. Sprite *ids*, by
> contrast, start at 0 and run to 255.

### Animating with a sprite

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=0.50\linewidth]{inbox/assets/fig-05-plot-sprite.png}
\caption{A sprite stamped at several scales in the PLOT window.}
\end{figure}
```

Re-stamping a sprite is cheaper than re-drawing the geometry that produced it. Define
the shape once with `SPRITEDEF`, then each frame issue a single `SPRITE` command at the
new position — you re-send one command, not the primitives. In buffered mode the motion
is flicker-free:

```{.spin2 caption="ch05-plot-field.spin2"}
CON _clkfreq = 200_000_000

PUB main() | x
  debug(`PLOT Field SIZE 256 256 BACKCOLOR $000000 UPDATE)
  ' Define a 3x3 "blip" sprite once: index 1 = lit, index 0 = transparent.
  ' Palette: entry 0 = transparent ($00......),
  ' entry 1 = opaque cyan ($FF00FFFF).
  debug(`Field SPRITEDEF 0 3 3  0 1 0  1 1 1  0 1 0  $00000000 $FF00FFFF)

  x := 0
  repeat
    debug(`Field CLEAR)  ' clear the buffered canvas
    ' stamp the sprite at (x,128), 8x
    debug(`Field SET `(x) 128 SPRITE 0 0 8 255)
    debug(`Field UPDATE)                          ' present the frame
    x := (x + 4) +// 256                          ' move right, wrap
    waitms(20)
```

The sprite is defined once; the loop re-stamps it with one `SPRITE` per frame. For a
shape built from many primitives the saving is larger still — the geometry is rasterized
into the sprite once, and every later frame costs a single stamp.

## The update model

The PLOT window has two update modes, chosen by whether you put `UPDATE` on the
creation line.

**Automatic mode** is the default. Every drawing command repaints the window as
it arrives, so the picture builds up live. This is the simplest mode and is right
for a handful of primitives or a static figure.

**Buffered mode** is enabled by the `UPDATE` keyword on the creation line. In
this mode your primitives accumulate on the off-screen canvas and **nothing is
shown until you send a runtime `` `UPDATE `` command**. Buffered mode is the right
choice for a scene built from many primitives, and it is essential for
flicker-free animation: clear, redraw the whole frame, then `UPDATE` once.

```spin2
PUB main() | f, ballx
  debug(`PLOT Anim SIZE 512 256 BACKCOLOR $000000 UPDATE)   ' buffered
  ballx := 0
  repeat f from 0 to 200
    debug(`Anim CLEAR)  ' erase (off-screen)
    debug(`Anim COLOR $FFFF00 SET `(ballx) 128 CIRCLE 30 0 255)
    debug(`Anim UPDATE)  ' present one frame
    ballx := (ballx + 4) +// 512
    waitms(20)
```

Three more commands round out display control:

- `` `CLEAR `` — fill the canvas with the background color and reset it for a new
  frame. In buffered mode this clears the off-screen canvas; the cleared state
  becomes visible at the next `UPDATE`.
- `` `SAVE 'name' `` — save the canvas image to a BMP file on the host. The
  filename is **required** and must come last: `SAVE 'name'` writes `name.bmp`
  (the `.bmp` extension is added for you — do not include it).
- `` `CLOSE `` — close this window and free its resources.

> **In buffered mode, `SAVE` captures the frame you are *showing*, not the one you
> are *drawing*.** `SAVE` reads the front buffer. If you draw a frame and then
> `SAVE` without an intervening `` `UPDATE ``, the file holds the **previous**
> frame — the new drawing is still off-screen. Send `` `UPDATE `` first, then
> `SAVE`. (Hardware-verified — and easy to miss, because the file is written, it
> is valid, and it looks plausible.) See [Chapter 1](#ch-1) for the rest of the
> `SAVE` traps.

> `UPDATE` plays two roles. On the creation line it is the **flag** that turns
> buffered mode on. At runtime, `` `UPDATE `` is the **command** that presents the
> accumulated drawing. You enable buffering once with the creation-line `UPDATE`,
> then trigger each repaint with a runtime `` `UPDATE ``.

## A complete worked example

This first program is a **tour of the drawing primitives** — it exercises the
polyline, the scatter, text, and the coordinate system so you can see each one
work, with no wiring and all of its own data generated on the P2. It plots one
cycle of a sine wave from the CORDIC engine as a connected polyline, overlays a
random scatter of dots from the hardware RNG, and labels the result. The origin is
moved to the left-center so the wave sits around a center line — y already
increases upward in the default coordinate system. The two worked instruments that
follow put these same primitives to work on real tasks.

```{.spin2 caption="ch05-plot-wave-scatter.spin2"}
CON _clkfreq = 200_000_000

PUB main() | x, y, angle, i, sx, sy

  ' Create a 512x512 plotting canvas on a black background
  debug(`PLOT Wave SIZE 512 512 BACKCOLOR $000000)

  ' Origin at left edge, vertical center; y increases upward (the default)
  debug(`Wave ORIGIN 0 256)

  ' Center axis line in dim gray
  debug(`Wave COLOR $404040)
  debug(`Wave SET 0 0)
  debug(`Wave LINE 511 0 1 255)

  ' One cycle of a CORDIC sine wave, drawn as a connected polyline.
  ' angle sweeps the full circle ($0000_0000..$FFFF_FFFF)
  ' across 512 columns.
  debug(`Wave COLOR $00FF00)
  debug(`Wave SET 0 0)
  repeat x from 0 to 511
    angle := x * ($FFFF_FFFF +/ 511)             ' +/ is UNSIGNED divide
    y := sine(angle, 200)                        ' amplitude 200 px
    debug(`Wave LINE `(x) `(y) 1 255)

  ' Random red scatter using the hardware RNG
  debug(`Wave COLOR $FF0000)
  repeat i from 0 to 99
    sx := rnd() +// 512                           ' 0..511
    sy := (rnd() +// 400) - 200                   ' -200..+199
    debug(`Wave SET `(sx) `(sy))
    debug(`Wave DOT 4 200)

  ' White centered label -- COLOR must sit immediately before TEXT
  debug(`Wave SET 256 230)
  debug(`Wave COLOR $FFFFFF TEXT 16 'QSIN + scatter')

  repeat                                         ' keep the window open

PRI sine(angle, length) : result
  org
              setq      #0                        ' Y coordinate = 0
              qrotate   length, angle  ' rotate (length, 0) by angle
              getqy     result  ' result = length * sin(angle)
  end

PRI rnd() : r
  org
              getrnd    r  ' 32-bit hardware random value
  end
```

The `sine` helper drives the CORDIC solver directly: **QROTATE** rotates the
point (`length`, 0) by `angle`, and **GETQY** returns `length x sin(angle)` — a
software-only sine source that needs no lookup table and no hardware. `rnd`
reads the on-chip random generator with **GETRND**. Both are wrapped in inline
PASM so the example builds and runs on a bare P2 board.

> **`+/`, not `/` — Spin2's plain `/` is a *signed* divide.** The angle step is
> `$FFFF_FFFF +/ 511`. Written with a plain `/`, Spin2 reads `$FFFF_FFFF` as the
> signed value **−1**, and `-1 / 511` truncates to **`0`** — so `angle` would be 0
> for every column, `sine()` would return the same value 512 times, and the "sine
> wave" would come out as a **flat horizontal line lying exactly on top of the grey
> axis this program draws two statements earlier**. It compiles, it runs, and it
> looks plausible. Any time you treat a 32-bit value as a full unsigned range —
> which is exactly what a full-circle angle is — use the unsigned operators: `+/`
> and `+//`. (`1 << 23` computes the same step here with no divide at all.)

## A worked instrument: an analog gauge

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=0.55\linewidth]{inbox/assets/fig-05-plot-gauge.png}
\caption{An analog gauge drawn in the PLOT window using polar coordinates.}
\end{figure}
```

Polar mode turns an instrument needle into a single `LINE`. Center the origin,
switch to polar so the cursor's coordinates are (radius, angle), and the needle for
any reading is one line from the center out to that reading's angle. The dial — tick
marks and a ring — is drawn the same way, so a complete analog gauge needs only
`LINE` and `CIRCLE`. This program sweeps a software-generated reading across a 240°
scale, redrawing in buffered mode so it never flickers:

```{.spin2 caption="ch05-plot-gauge.spin2"}
CON _clkfreq = 200_000_000

PUB main() | ang, value, needle, i, tick
  ' Buffered gauge: redraw the whole dial + needle each frame, flicker-free.
  debug(`PLOT Gauge SIZE 400 400 BACKCOLOR $000000 UPDATE)
  debug(`Gauge ORIGIN 200 200)            ' (0,0) at the dial center
  debug(`Gauge POLAR 360)  ' degrees; theta 0 points right (+x), +90 up

  ang := 0
  repeat
    value  := 50 + qsin(50, ang, 360)  ' software-generated 0..100 reading
    needle := (value * 240 / 100) - 120   ' map 0..100 -> -120..+120 degrees

    debug(`Gauge CLEAR)

    ' Scale: eleven radial ticks across the 240-degree sweep.
    debug(`Gauge COLOR $404040)
    repeat i from 0 to 10
      tick := (i * 24) - 120
      debug(`Gauge SET 90 `(tick) LINE 100 `(tick) 2 255)

    ' Dial ring and center hub.
    debug(`Gauge SET 0 0 CIRCLE 210 2 255)
    debug(`Gauge COLOR $00FFFF SET 0 0 CIRCLE 12 0 255)

    ' Needle: one polar line from center out to the reading's angle.
    debug(`Gauge COLOR $FF7F00 SET 0 0 LINE 95 `(needle) 4 255)

    debug(`Gauge UPDATE)                   ' present the frame

    ang += 3
    waitms(30)
```

Each frame clears the buffered canvas, draws the scale ticks and ring as polar lines
and a centered circle, places the needle with one `LINE` at the reading's angle, and
presents the frame with `UPDATE`. The reading here comes from `QSIN`; wire it to any
value your program computes and the needle follows.

> Buffered mode (`UPDATE` on the creation line) keeps the gauge smooth: the whole
> dial is redrawn off-screen each frame, then shown at once. Without it you would see
> the needle erase-and-redraw flicker.

## A worked instrument: a control-loop strip chart

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=0.75\linewidth]{inbox/assets/fig-05-plot-pid.png}
\caption{A PID control loop on the PLOT window: setpoint, the process variable's overshoot-and-settle, and the controller output.}
\end{figure}
```

A strip chart — several values traced against time — is how you watch a control
loop behave while you tune it. This program runs a complete loop in software: a
**PI controller** driving a simulated **first-order process**, with nothing wired
up. The setpoint steps up and then back down; the process variable chases it,
overshoots, and settles; the controller output is the effort that drives it there.
Plotting all three together is exactly what you do on the bench to choose P, I, and
D gains.

The loop is an honest little simulation. Each step computes the error, accumulates
it for the integral term, forms the controller output (clamped, like a real
actuator), and advances a first-order process model toward that output. The three
histories are then drawn as three polylines across the canvas:

```{.spin2 caption="ch05-plot-pid.spin2"}
CON
  _clkfreq = 200_000_000
  STEPS = 256

VAR
  long spH[STEPS], pvH[STEPS], ctlH[STEPS]

PUB main() | t, sp, pv, ctl, err, integ
  debug(`PLOT Loop SIZE 512 320 BACKCOLOR $E8E8E8)
  debug(`Loop ORIGIN 0 10)              ' baseline at bottom; y up (default)

  repeat                               ' re-run the experiment continuously
    pv := 0
    integ := 0
    repeat t from 0 to STEPS-1
      sp := (t < 128) ? 70 : 30        ' setpoint steps up then down
      err := sp - pv
      integ += err
      ctl := (err*2 + integ/32) #> 0 <# 100   ' PI control, clamp 0..100
      pv += (ctl - pv) / 10            ' first-order process lag
      spH[t] := sp
      pvH[t] := pv
      ctlH[t] := ctl

    debug(`Loop CLEAR)
    debug(`Loop COLOR $606060)
    trace(@ctlH)                       ' controller output (dark gray)
    debug(`Loop COLOR $0050C0)
    trace(@spH)                        ' setpoint (blue)
    debug(`Loop COLOR $008000)
    trace(@pvH)                        ' process variable (green)
    waitms(500)

PRI trace(p) | t
  debug(`Loop SET 0 `(long[p][0] * 3))    ' value 0..100 -> 0..300 px
  repeat t from 1 to STEPS-1
    debug(`Loop LINE `(t*2) `(long[p][t] * 3) 2 255)
```

`trace` draws one history array as a connected polyline: it `SET`s the cursor to
the first point, then issues a `LINE` to each following point, scaling the 0–100
value range to the canvas height. Each pass re-runs the whole experiment and
redraws all three traces together. Raise the proportional gain (the `*2`) or change
the integral divisor (`/32`) and the overshoot and settling time shift exactly as a
real loop's would — the chart *is* the tuning feedback.

### Where you'd use this

In computer science and computer engineering, the PLOT window is the canvas for
**control-systems work** — watching a loop respond and tuning it — and for general
**instrumentation and data visualization**, where you build the exact gauge, chart,
or figure your data calls for.

**On an embedded project**, you reach for it to plot a PID strip chart while tuning
a motor or thermal loop (as here), to trace a battery's charge curve, to plot raw
ADC against engineering units during a calibration, or to build a servo or RPM dial
like the gauge above.

**Bandwidth fit:** these are all low-rate — readings and traces updating at tens to
a few hundred points per second — and sit comfortably inside the link budget.

**Extension (real hardware):** replace the simulated process model with a real
measured value (an ADC read, a sensor sample) and the simulated `ctl` with your
actual control output, and the same strip chart shows a live loop.

## Considerations

- **Match the coordinate system to the figure.** Set `ORIGIN` and the
  `CARTESIAN` flips (or `POLAR`) once at the top, in the coordinate convention
  your figure is natural in, and every primitive follows. A graph wants the
  origin at a corner with y up; a radial display wants the origin centered and
  polar mode.
- **`linesize 0` fills; greater than zero outlines.** For `CIRCLE`, `OVAL`,
  `BOX`, and `OBOX`, the line-size argument is what selects filled versus
  outlined. This is the most common source of an unexpectedly solid or hollow
  shape.
- **`LINE` moves the cursor; `DOT` and the shapes do not.** Chain `LINE` calls to
  draw a path; use `SET` before a `DOT`, `CIRCLE`, or `TEXT` to position it.
- **Use buffered mode for whole-scene redraws.** A static figure or a few
  primitives can run in automatic mode. For animation or a many-primitive scene,
  add `UPDATE` and present each frame with one runtime `` `UPDATE ``, which
  removes the flicker of per-primitive repainting.
- **Composite prebuilt layers and sprites instead of redrawing geometry.** When a
  background or a repeated element is fixed, load it once with `LAYER` (or define
  a sprite once with `SPRITEDEF`) and place it each frame with `CROP` or
  `SPRITE`. You re-issue one command rather than every primitive that produced
  the image. Remember that `LAYER` reads a `.bmp` from the host filesystem.
- **Layers are 1–8, sprite ids are 0–255.** Mixing these ranges up is a frequent
  error; the layer commands silently ignore an out-of-range index.

## Try it

Start from the worked example. Then: switch the window to buffered mode by adding
`UPDATE` to the creation line, wrap the whole drawing in a `repeat`, animate the
phase by adding a growing offset to `angle`, and end each frame with `CLEAR` …
draw … `` `UPDATE ``. You will have a scrolling sine wave with a fresh scatter each
frame, built entirely from CORDIC and the RNG, using the coordinate system,
primitives, color, and the buffered update model together.
