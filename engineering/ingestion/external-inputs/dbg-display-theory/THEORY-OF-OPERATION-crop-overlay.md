# Theory of Operation — The "Crop & Overlay" Display Technique

**Subject file:** `jm_debug_analog_meter_050.spin2` (Jon "JonnyMac" McPhalen)
**Companion file:** `jm_debug_panel_digits_020.spin2`
**Platform:** Parallax Propeller 2, Spin2 `DEBUG(\`PLOT ...)` display, requires `{SPIN2_V50}` or later.

---

## 1. What problem is being solved

The author wants a *photo-realistic instrument panel* — an analog needle gauge with a 4-digit numeric readout — drawn inside a P2 `DEBUG` PLOT window, updated many times per second, with **no flicker** and **no per-pixel drawing code** on the P2.

Drawing such a panel pixel-by-pixel every frame would be slow, would flicker, and would require a font renderer and artwork routines on the microcontroller. The "crop & overlay" technique sidesteps all of that: **all the artwork is pre-drawn into BMP files**, loaded once into off-screen *layer buffers* inside the PLOT window, and each frame is composed by **copying ("cropping") small rectangles out of those buffers onto the visible canvas.** The P2 never draws art — it only issues copy commands with coordinates.

This is exactly the classic video-game **sprite-sheet / blitting** model, implemented entirely through three V50 PLOT sub-commands: `LAYER`, `CROP`, and `UPDATE`.

---

## 2. The three primitives (authoritative semantics)

From the P2 Knowledge Base (`DEBUG PLOT`, V50 layer commands):

### `LAYER`
```
DEBUG(`name LAYER n 'file.bmp')
```
Loads a BMP file into off-screen **layer buffer `n`** (1–8). The layers are private image stores attached to the window; nothing about loading a layer changes the visible canvas. Up to 8 layers persist until replaced or the window closes.

### `CROP` — has three forms
```
DEBUG(`name CROP n)                              ' (a) whole-layer restore
DEBUG(`name CROP n left top width height)        ' (b) copy region onto SAME spot
DEBUG(`name CROP n left top width height x y)     ' (c) copy region to (x,y)
```
- **(a)** copies the *entire* layer `n` to the canvas origin — i.e. repaints the whole background. Used to initialize the scene and to wipe it.
- **(b)** copies a rectangle from layer `n` back to the **identical** coordinates on the canvas. This is the **"erase"** operation — it restores a patch of pristine background over whatever was drawn there last frame.
- **(c)** copies a `width×height` rectangle whose top-left in the layer is `(left,top)` to **destination `(x,y)`** on the canvas. This is the **"blit a sprite"** operation — the workhorse of the technique.

> Note the argument order: **source rect first (`left top width height`), destination last (`x y`)**. This is the single most common point of confusion when reading the code.

### `UPDATE`
```
DEBUG(`name UPDATE)
```
The window is created with the `HIDEXY UPDATE` options, which puts it in **manual / double-buffered mode**: nothing the P2 draws becomes visible until an explicit `UPDATE`. All the `CROP`s for a frame are issued first, then one `UPDATE` flips them onto the screen at once. **This is what makes the animation flicker-free** — the user never sees a half-composed frame.

---

## 3. The artwork (sprite sheets)

The technique lives or dies on how the BMP files are laid out. The meter uses a single, cleverly-packed sheet.

### `debug_analog_meter_050.bmp` — 495 × 540 px, loaded as **layer 1**

It is one image containing everything:

| Region | Y range | Contents |
|---|---|---|
| **Meter face** | 0 – 239 | The full panel artwork: bezel, arced scale (1–9), "P2 DEBUG" watermark, and an *empty* black 7-segment readout box. This is the background. |
| **Digit font, 5 rows** | 240 – 539 | Five horizontal strips of 7-segment digits `0`–`9`, one strip per color. Each strip is 60 px tall; each digit cell is **45 px wide × 60 px tall**. A decimal-point glyph sits at the right end (≈ x=483). |

The five color rows map directly to the enum in the code:
```
#0, RED, GREEN, BLUE, YELLOW, WHITE     ' row index 0..4
```
so a digit's vertical position in the sheet is selected purely by color:
```
y2 := 240 + (DIG_CLR * 60)              ' DIG_CLR = WHITE = 4  ->  y2 = 480
```

The genius here: **the visible background and the font live in the same layer buffer.** The portion below the gauge (y ≥ 240) is never shown to the user — it's an off-screen palette the code samples from. The window itself is only 320 × 240; everything from y=240 down is "below the fold," used as storage only.

### Companion sheets for the digits panel
`jm_debug_panel_digits_020.spin2` splits the same idea across multiple layers:
- **layer 1** `panel_leds_off.bmp` (480×240) — background with 8 dark LEDs and an empty display box.
- **layer 2** `panel_leds_on.bmp` — identical panel but with the 8 LEDs lit green.
- **layer 3** `panel_digits.bmp` (484×54) — a single horizontal strip: digits `0`–`9` then a minus sign, each cell **44 px wide × 54 px tall**.

Here the two LED states are *whole alternate backgrounds*; an individual LED is updated by cropping the matching 50×50 patch out of whichever layer holds the desired state.

---

## 4. Frame lifecycle — the analog meter

### 4.1 One-time setup (`setup()`)
```spin2
debug(`plot amp title 'Analog Meter+' size 320 240 pos 650 200 hidexy update)
debug(`amp cartesian 1 0 precise)        ' Y-up coordinate system, sub-pixel needle
debug(`amp color red linesize $400)       ' needle = red, 4.0-px wide (×256 in precise mode)
debug(`amp layer 1 'debug_analog_meter_050.bmp')  ' load the sheet off-screen
debug(`amp crop 1)                         ' paint full background (form a)
debug(`amp update)                          ' show it
```
After this the window shows the empty gauge. The font strips are sitting in layer 1, unseen.

### 4.2 Per-update (`update_meter(aval, dval, dpbits, force)`)

**Arguments:** `aval` = needle value 0–1000; `dval` = number to show 0–9999; `dpbits` = 4-bit mask of which decimal points to light; `force` = 4-bit mask of which digit columns to show even when they'd be a leading zero.

**Step A — compute and draw the needle (vector, not sprite).**
```spin2
x1 := qcos(190<<8, aval-1400, 3600)        ' CORDIC: needle tip X
y1 := qsin(190<<8, aval-1400, 3600)        ' CORDIC: needle tip Y
debug(`amp crop 1)                          ' (a) wipe whole canvas back to clean gauge
debug(`amp set `(160<<8, 225<<8))           ' move pen to needle pivot
debug(`amp line `(x1+160<<8, y1+225<<8))    ' draw needle to computed tip
```
The needle is the *one* element drawn live, using the P2 **CORDIC** engine (`qcos`/`qsin`) to convert the gauge value into an angle and project the tip. Radius is 190, pivot is (160,225), the `<<8` is the 8-bit fixed-point that `precise` mode expects. `aval-1400` and span `3600` set the zero-point and sweep of the dial.

**Step B — tidy the pivot.**
```spin2
debug(`amp crop 1 50 140 220 95)            ' (b) restore a patch over the needle's base
```
The line is drawn from the exact pivot, which would leave an ugly hub. Re-cropping the clean background rectangle (50,140)–(270,235) over the base hides the messy origin so the needle appears to emerge cleanly from behind the bezel.

**Step C — render the 4-digit readout (sprite blitting).**
```spin2
y2 := 240 + (DIG_CLR * 60)                  ' pick the color strip in the sheet
d  := 1000                                   ' most-significant divisor
repeat c from 3 to 0                          ' columns left -> right
  n := v / d                                  ' the digit value 0..9
  if (dval >= d) || force.[c]                 ' suppress leading zeros unless forced
    x1 := 70 + ((3 - c) * 45)                 ' on-screen column position (45 px apart)
    debug(`amp crop 1 `(n*45, y2, 45, 60, x1, 161))   ' (c) blit digit glyph
    if (dpbits.[c])
      x1 += 33
      debug(`amp crop 1 `(483, y2+49, 8, 8, x1, 210))  ' (c) blit a decimal point
  v //= d
  d /= 10
```
For each of the four columns the code:
1. extracts the digit `n`,
2. computes the **source X** in the sheet as `n*45` (digit's cell) at **source Y** `y2` (its color strip),
3. computes the **destination X** on screen, and
4. issues form-(c) `CROP` to stamp that 45×60 glyph into the readout box.
Optional decimal points are stamped from a small 8×8 glyph at sheet x=483.

Because each digit is just a rectangle copy, "rendering a font" costs the P2 nothing but arithmetic — there is no glyph rasterizer.

**Step D — present the frame.**
```spin2
debug(`amp update)                           ' flip everything to screen at once
```
Everything composed in Steps A–C was invisible until this single `UPDATE`. The viewer sees the new needle position and new number appear together, atomically — no flicker.

### 4.3 The driving loop (`main()`)
```spin2
repeat
  update_meter(0, 0, %0010, %0011)           ' rest at 000.0
  waitms(500)
  repeat level from 0_0 to 100_0 step 5      ' sweep 0 -> 100.0
    update_meter(level, level, %0010, %0011)
    waitms(50)
  waitms(1000)
```
`%0011` forces the two right-most columns to always show (so the display reads `00.0` rather than blank), and `%0010` lights the decimal point in column 1, giving a fixed `NN.N` format.

---

## 5. Why it works — the underlying model

```
   BMP file on host  ──LAYER──▶  off-screen layer buffer (in the PLOT window)
                                          │
                                          │  CROP (copy rectangles)
                                          ▼
                                  off-screen canvas  ──UPDATE──▶  visible window
```

1. **Art is data, not code.** All pixels are authored in an image editor and shipped as BMPs. The P2 firmware contains zero artwork — only coordinates and copy commands. Changing the look means editing a BMP, not the program.
2. **The layer is both background *and* sprite atlas.** One image holds the scene plus a font/state palette below the visible area. "Drawing a digit" = "copy from the palette region." "Erasing" = "copy from the background region."
3. **Erase-by-restore, not erase-by-clear.** There is no clear-to-black; you paint the pristine background back over the dirty region (form a for the whole scene, form b for a patch). This guarantees the restored pixels exactly match the surrounding art.
4. **Double-buffering gives atomic, flicker-free frames.** `HIDEXY UPDATE` defers display; the many `CROP`s for a frame land all at once on `UPDATE`.
5. **Work is offloaded to dedicated silicon.** The needle angle uses the CORDIC (`qcos`/`qsin`); the blits are handled by the debug display host. The Spin2 code is just a thin sequencer of coordinates.

The result is a smooth, attractive instrument rendered by a microcontroller that, strictly speaking, never draws a gauge — it only says *"copy this rectangle to there, then show it."*

---

## 6. Quick reference — coordinate cheat sheet (analog meter)

| Element | Source in layer 1 (l, t, w, h) | Destination (x, y) |
|---|---|---|
| Full background | whole image (form a) | 0, 0 |
| Needle-base wipe | 50, 140, 220, 95 (form b) | same spot |
| Digit `n`, color `C` | `n*45`, `240+C*60`, 45, 60 | `70+(3-c)*45`, 161 |
| Decimal point | 483, `240+C*60+49`, 8, 8 | digit_x+33, 210 |

Window: 320×240. Needle pivot: (160,225), radius 190, drawn in `precise` (×256) coordinates. Visible art occupies y=0–239; the digit font palette occupies y=240–539 off-screen.
