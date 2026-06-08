# P2 DEBUG-Plot Displays — Builder's Guide & Contrast

**Purpose:** a reference an agent can use to build new Propeller-2 `DEBUG(\`PLOT ...)` "instrument panel" displays in the style of Jon McPhalen's examples. It contrasts four working displays, extracts the reusable recipe, and documents how a display can also be an **input device** (PC keyboard + mouse).

**Companion doc:** `THEORY-OF-OPERATION-crop-overlay.md` (deep dive on the analog meter).

**Hard requirement:** all of these use V50 layer/crop commands. The source file must start with `{Spin2_v50}` (or later), and the toolchain must be PNut/Spin2 v50+.

---

## 0. The mental model in one paragraph

A PLOT window owns up to **8 off-screen image buffers ("layers")**, each loaded from a BMP. The visible canvas is composed by **copying rectangles out of those layers** (`CROP`) and then **flipping the result to screen** (`UPDATE`). Artwork is authored as BMP files — the P2 never draws pixels, it only issues *"copy this rectangle to there"* commands plus a little arithmetic to pick which rectangle and where. This is sprite-sheet blitting. Optionally the same window reads the host **keyboard and mouse** back into the P2, turning a picture into a control panel.

---

## 1. The four reference displays at a glance

| # | File | Window title | What it shows | Layers used | Vector draw? | Reads input? |
|---|------|--------------|----------------|-------------|--------------|--------------|
| 1 | `jm_debug_panel_010.spin2` | Binary LEDS | 8 LEDs = one byte (red/green) | 3 (whole-panel states) | no | no |
| 2 | `jm_debug_panel_digits_020.spin2` | Digital Display | 6-digit number + 8 LEDs | 3 (2 panel states + 1 font) | no | no |
| 3 | `jm_debug_analog_meter_050.spin2` | Analog Meter+ | Needle gauge + 4-digit readout | 1 (packed: bg + font) | **yes** (CORDIC needle) | no |
| 4 | `jm_debug_switches_030.spin2` | Binary Switches | 8 toggle switches + multi-radix readout | 5 (2 states + 3 fonts/labels) | no | **yes** (key + mouse) |

These four span the whole design space: output-only → interactive, single-layer → many-layer, pure-blit → blit+vector. Build new displays by mixing these patterns.

---

## 2. The common skeleton (every display follows this)

```spin2
{Spin2_v50}

con
  CLK_FREQ = 200_000_000
  _clkfreq = CLK_FREQ

pub main()
  setup()
  repeat
    ' ... compute state ...
    ' ... CROP sprites for changed elements ...
    debug(`NAME update)              ' flip frame to screen
    waitms(...)

pub setup()
  debug(`plot NAME title 'Title' size W H pos X Y hidexy update)   ' create window
  debug(`NAME layer 1 'background.bmp')                            ' load art
  debug(`NAME layer 2 'sprites.bmp')
  debug(`NAME crop 1)                                              ' paint full background
  debug(`NAME update)                                              ' show it
```

- `` `NAME `` is the window handle you pick (`amp`, `panel`, `switches`, …). Every later command targets it.
- `hidexy` hides the on-screen measurement cursor; `update` puts the window in **manual / double-buffered** mode — nothing shows until you call `update`. **This is what kills flicker:** issue all the frame's crops, then one `update`.
- Load all layers once in `setup()`. They persist for the life of the window.

---

## 3. The three commands you actually use

### `LAYER n 'file.bmp'`
Load a BMP into off-screen buffer `n` (1–8). No visible effect.

### `CROP` — three forms (memorize the argument order)
```
crop n                              ' (a) repaint ENTIRE layer n at origin — full background / full wipe
crop n  left top width height      ' (b) copy that source rect back to the SAME spot — "erase by restore"
crop n  left top width height x y   ' (c) copy source rect (left,top,w,h) to DESTINATION (x,y) — "blit a sprite"
```
> Argument order is **source rectangle first, destination last**. The single biggest source of bugs.

### `UPDATE`
Flip the composed frame to screen. Call once per frame after all crops.

**The three idioms built from these:**
- **Draw/replace a cell:** form (c) — pick source by data, pick dest by slot index.
- **Erase a region:** form (b) — copy clean background over it. (There is no "clear"; you restore.)
- **Reset whole scene:** form (a) — repaint the entire background layer.

---

## 4. Coordinate systems — pick one deliberately

| Mode | Set with | Origin | Y direction | Used by |
|------|----------|--------|-------------|---------|
| Default | (nothing) | top-left | Y **down** | panel_010, panel_digits |
| Cartesian | `NAME cartesian 1` | bottom-left | Y **up** | switches |
| Cartesian + precise | `NAME cartesian 1 0 precise` | bottom-left | Y up, **×256 sub-pixel** | analog_meter |

`precise` multiplies all coordinates by 256 (you write `160<<8` for x=160), giving smooth sub-pixel vector lines — needed for the needle. In precise mode `linesize $400` means 4.0 px (4×256).

> When adapting coordinates between examples, first check which mode the source used — a y value means opposite things under default vs cartesian.

---

## 5. Sprite-sheet design patterns (the heart of it)

There are exactly two ways these examples encode visual state into BMP layers. New displays combine them.

### Pattern A — "whole-state layers": one full-canvas BMP per state
Each possible look is a complete background image; you pick the **layer number** to choose state, then crop the small piece you need from that layer at its own location.

- **panel_010** (`leds_off`/`leds_red`/`leds_grn`, all 480×120): the 8-LED bar in three states. To set one LED: `crop layer x y 50 50` where `layer` ∈ {1,2,3} selects off/red/green and `(x,y)` is that LED's fixed slot (form b — source = dest).
  ```spin2
  img := value.[bit] + 1 + (ledcolor * value.[bit])   ' 1=off, 2=red, 3=green
  debug(`panel crop `(img, x, y, 50, 50))             ' same-spot copy from chosen layer
  ```
- **panel_digits** (`panel_leds_off`/`panel_leds_on`): the whole panel with LEDs dark vs lit; an LED is `img := value.[bit] + 1` then `crop img x y 50 50`.
- **switches** (`p2_debug_swtiches0`/`swtiches1`): switch-bank with all toggles down vs up; one switch is `crop layer sx sy 21 51` at its slot.

> Strength: trivial code, pixel-perfect alignment (source and dest coincide). Cost: one full BMP per state, so it suits a small number of states (on/off, off/red/green).

### Pattern B — "font/atlas strips": one BMP holds many glyphs in a row (or grid)
The glyph is selected by arithmetic into the strip; destination is a layout slot. This is how all numeric readouts work.

| Sheet | Size | Cell | Index formula | Notes |
|-------|------|------|---------------|-------|
| `panel_digits.bmp` | 484×54 | 44×54 | `srcX = digit*44` | `0–9` then `–` (minus at x=440) |
| `hex_digits.bmp` | 561×50 | 33×50 | `srcX = digit*33` | `0–9 A b C d E F –` (sign at x=528) |
| analog meter font (rows 240–539 of the packed sheet) | 45×60 cells | `srcX = digit*45`, `srcY = 240 + color*60` | color picks the **row**: RED..WHITE |

Render loop (right-to-left, leading-zero suppression):
```spin2
repeat i from 0 to 5
  d  := value // base                       ' least-significant digit
  x1 := <slot for column i>
  if (i == 0) || (value)                    ' always show ones; suppress leading zeros
    debug(`NAME crop FONT `(d*CELLW, srcY, CELLW, CELLH, x1, destY))   ' blit glyph (form c)
  else
    if negative: blit the sign glyph
    quit
  value /= base
```

> Strength: unlimited values from one small BMP. The analog meter's trick: it stores **five color copies of the font stacked below the visible area of the same layer** and picks color by `srcY = 240 + color*60`. The window is only 240 tall, so rows below 240 are pure off-screen storage.

### Vector overlay (only the analog meter)
One element — the needle — is genuinely drawn, not blitted, using the CORDIC engine:
```spin2
x1 := qcos(190<<8, aval-1400, 3600)         ' tip X  (radius 190, angle from value)
y1 := qsin(190<<8, aval-1400, 3600)         ' tip Y
debug(`amp crop 1)                          ' wipe whole gauge (form a)
debug(`amp set `(160<<8, 225<<8))           ' pen to pivot
debug(`amp line `(x1+160<<8, y1+225<<8))    ' draw needle
debug(`amp crop 1 50 140 220 95)            ' restore hub patch over the messy pivot (form b)
```
Use this whenever an element is continuous (needle, trace, bar) rather than enumerable (digit, LED).

---

## 6. Image (BMP) file format — how to author the artwork

Every layer is a BMP file loaded by `LAYER n 'name.bmp'`. **Get the format exactly right or the layer won't load / won't look right.** All of the reference assets share one format; match it.

### Required format (verified from every asset in this project)
| Property | Value | Why |
|----------|-------|-----|
| Container | **Windows BMP** (`.bmp`) | The only format `LAYER` accepts. |
| Color depth | **24-bit RGB, 3 bytes/pixel** | All assets are 24-bit. |
| Alpha channel | **none** | 24-bit BMP has **no transparency** — see consequences below. |
| Compression | **none (BI_RGB, uncompressed)** | Plain pixel data. |
| Color space | sRGB, full color | Pixel value read back by `pc_mouse` as `$00_RR_GG_BB`. |

> The reference files happen to carry a 124-byte BITMAPV5 header (Photoshop/macOS "Save As BMP"); a plain 54-byte BITMAPINFOHEADER works too. What matters is **24-bit, uncompressed, no alpha.**

### The big consequence: NO transparency
Because there is no alpha, **every `CROP` copies an opaque rectangle** — it overwrites the destination completely. This drives the entire design discipline:

1. **Sprite cells must be self-contained.** Each glyph/state cell must already contain the correct background around the shape, because when you blit it, it replaces everything in that rectangle. (E.g. each digit cell includes its black readout-box background; each LED cell includes the surrounding gray bezel.)
2. **"Erasing" = copying clean background back** (CROP form b / a). There is no transparent paint. So your background layer must contain the pristine empty look of every region you'll later overwrite.
3. **Seams must match.** The pixels just outside a blitted cell come from the background; the pixels inside come from the sprite. For an invisible seam, **the cell's border pixels must match the background exactly** (same gray, same black box). Author sprites and background together, sampling the same colors.
4. **Pick a "blank" cell deliberately.** A font strip usually needs the empty/space cell to equal the readout background (so blanking a column = blit the blank cell, or re-crop background over it).

### Dimensions, grid, and layout
- **Author at exact device pixels.** No scaling happens; 1 BMP pixel = 1 window pixel. Decide the window `size W H` first, then draw to it.
- **Use a fixed cell pitch** so the index math is trivial: `srcX = index * cellWidth`. Keep cells edge-to-edge with no gaps (digits: 33, 44, or 45 px wide in the examples).
- **A layer may be larger than the window** and the extra area becomes free off-screen storage. The analog meter's layer is 495×540 inside a 320×240 window: the gauge occupies the top, and **five color copies of the digit font are stacked below y=240** purely as a palette. Use this to pack states/fonts into one layer.
- **Origin for CROP is top-left** of the image as you see it in an editor (the tool handles BMP's internal bottom-up row order). `srcY = 0` is the top row.

### Color & state encoding
- Encode a few discrete states as **whole-canvas BMPs, one per state** (Pattern A: off/red/green, switch up/down) and select with the layer number.
- Encode many values as a **horizontal strip of equal cells** (Pattern B: digit fonts) and select with `srcX = index*cellW`.
- Encode color variants either as **separate layers** or as **stacked rows in one layer** (`srcY = base + colorIndex*rowHeight`, the analog-meter approach).

### Authoring checklist for a new asset
1. Fix the window size; draw the background at that exact size; export 24-bit uncompressed BMP, no alpha.
2. For each variable element, decide Pattern A (state layers) or Pattern B (font strip), and lay cells on a uniform pitch.
3. Make each sprite cell include the matching background so blits leave no seam; make the background include the empty look so restores erase cleanly.
4. Note the exact cell width/height and each slot's destination (x,y) — those numbers go straight into your `CROP` calls.
5. Put the `.bmp` files **next to the `.spin2` source** (they're loaded by bare filename).

### Quick conversion / inspection
- Export from most editors as "BMP → 24-bit / R8G8B8, no compression."
- On macOS, convert anything to the right BMP with: `sips -s format bmp in.png --out out.bmp` (produces 24-bit BMP).
- Verify a file with: `file out.bmp` → expect `... x 24, ... ` (the `24` = 24-bit) and no compression.

---

## 7. Displays as INPUT devices (the switches example)

A graphical DEBUG window can read the **host PC's keyboard and mouse** back into the P2, so the picture becomes a control surface. Two commands do this; **each must be the LAST command in its `debug()` statement**, and the window must have focus.

### `PC_KEY(@key)` — keyboard
Writes one LONG. Returns the keypress from the last ~100 ms, else 0. Printable keys = ASCII (32–126); arrows/Home/End/etc. = small codes 1–13; Esc = 27.
```spin2
debug(`switches `pc_key(@key))              ' poll keyboard (LAST in statement)
if (key)
  case key
    "d","D": set_radix(10)
    "h","H": set_radix(16)
    "b","B": set_radix(2)
    " "    : reset_value()
```

### `PC_MOUSE(@xpos)` — mouse (7 consecutive longs)
Fills, in order: **`xpos, ypos, wheeldelta, lbutton, mbutton, rbutton, pixel`**.
- `xpos,ypos` — position in the window's coordinate basis; **both < 0 when the mouse is outside**.
- `wheeldelta` — momentary 0 / ±1.
- `lbutton/mbutton/rbutton` — **0 = up, -1 = pressed**.
- `pixel` — color under cursor `$00_RR_GG_BB`, or -1 outside.
```spin2
var long xpos, ypos, wheeldelta, lbutton, mbutton, rbutton, pixel   ' MUST be 7 consecutive longs
...
debug(`switches `pc_mouse(@xpos))           ' poll mouse (LAST in statement)
```

### Hit-testing: mapping a click to a control
The switches demo turns clicks into actions two ways:

1. **Named rectangular zone via a struct** (for the radix indicator):
   ```spin2
   con  struct rect(x1, y1, x2, y2)
   var  rect rtype
   ...
   rtype := 134, 81, 185, 106                ' the clickable zone (set in setup)
   ...
   if (lbutton) and in_zone(xpos, ypos, @rtype)
     next_radix()
   ```
   where `in_zone()` is a simple bounding-box test.

2. **Coordinate ranges via `case`** (for the 8 switches): one row band on Y, then an X `case` selects which switch:
   ```spin2
   if (lbutton) and (ypos => 129) and (ypos =< 179)
     case xpos
       265..285 : toggle_bit(0)
       232..252 : toggle_bit(1)
       ...
       034..064 : toggle_bit(7)
   ```
   `toggle_bit` flips the data bit and immediately blits the matching up/down switch sprite (Pattern A).

### The "dirty flag" loop (don't redraw every tick)
Interactive displays poll fast but only recompose/`update` when something changed:
```spin2
displayval, dirty := 0, true
repeat
  check_key()                                ' may set dirty
  check_mouse()                              ' may set dirty
  if (dirty)
    show_value(displayval, radix)            ' re-blit the readout
    debug(`switches update)                  ' single flip
    dirty := false
    waitms(250)
  waitms(100)
```

> Right-click and middle-click are used as shortcuts (next radix / reset). Button state is `-1` when pressed, so test `if (rbutton)`.

---

## 8. Decision guide for a NEW display

1. **List the elements** and classify each:
   - *Enumerable, few states* (LED on/off, switch up/down) → **Pattern A** whole-state layers, one BMP per state, `crop layer x y w h` (source=dest).
   - *Enumerable, many values* (digits, hex, letters) → **Pattern B** font strip, `srcX = index*cellW`, blit to a slot.
   - *Continuous* (needle, bar, trace) → **vector** (`set`/`line`/`dot`, often `precise`), then restore patches to clean up.
2. **Author the BMPs** to match your cell sizes. Keep background and (optionally) font in layers; remember you can stash extra glyph rows below the visible area (analog-meter trick).
3. **Choose a coordinate mode** (default vs `cartesian` vs `cartesian … precise`) and keep all coordinates consistent with it.
4. **Write `setup()`**: create window (`hidexy update`), load layers, `crop 1`, `update`.
5. **Write the update path**: compute → erase changed regions (form b) or repaint (form a) → blit new sprites (form c) → one `update`.
6. **If interactive:** add `pc_key`/`pc_mouse` polls (each LAST in its `debug()`), hit-test with bounding boxes or coordinate `case`s, and gate redraws behind a `dirty` flag.

---

## 9. Gotchas / rules of thumb

- `{Spin2_v50}` directive is mandatory for layer/crop.
- `CROP` argument order is **source rect, then destination**; the 4-number form copies to the same spot (erase), the 6-number form copies to `(x,y)` (blit).
- Nothing is visible until `UPDATE`; batch all crops, then one update — that is the no-flicker guarantee.
- There is no clear-screen — erase by re-cropping clean background.
- `pc_key`/`pc_mouse` must be the **last** command in their `debug()` statement and the window must have **focus**; key latch auto-clears after ~100 ms; mouse buttons read **-1** when down; mouse-outside gives negative coords.
- `pc_mouse` needs **7 consecutive longs**; declare them adjacently and pass the address of the first.
- Pick the coordinate mode first — a `y` value is meaningless without knowing default vs cartesian.
- Whole-state layers cost one full BMP per state; reserve for few-state elements. Font strips scale to unlimited values from one small BMP.

---

## 10. Per-file quick reference (copy-paste anchors)

**panel_010** — minimal output: 3 whole-panel layers, single same-spot crop per LED.
`img := value.[bit] + 1 + (ledcolor * value.[bit])` → `crop img x y 50 50`, step `x -= 50`.

**panel_digits** — output: panel off/on layers + 44×54 font strip (layer 3).
Blank box: `crop 1 108 53 372 106`. Digit: `crop 3 d*44 0 44 54 x1 53`. LED: `crop (bit+1) x y 50 50`.

**analog_meter** — output + vector: one packed sheet (bg + 5 color font rows at y=240..539, 45×60 cells).
Needle via `qcos/qsin` + `set`/`line`; digit: `crop 1 n*45 (240+color*60) 45 60 x1 161`; dp at sheet x=483.

**switches** — interactive: layers 1/2 = switch bank down/up (21×51 cells), 3 = hex font (33×50), 4 = radix labels `dhbo` (52×26), 5 = `radix_bits` underline (5-px rows).
Reads `pc_key` (d/h/b/o/space) and `pc_mouse` (zone + coordinate-range hit-tests); `dirty`-flag redraw.
