# BMP Asset Spec — ch15 Panel-Plot Example

**Requested:** 2026-07-10
**For:** `examples-library/ch15-panel-plot.spin2` (and its identical copy in the manual,
`opus-master/ch15-panels.md`, "Technique 3 — Sprite-sheet panels").
**Deliver two files to:** `engineering/document-production/manuals/p2-debug-window-manual/examples-library/`
- `panel_bg.bmp`
- `digits.bmp`

These assets are currently **missing from the ZIP and the repository** — a customer reported the
example "shows nothing … also can't find them in the repository." This spec defines them exactly so
the example runs as written (no code changes to the example).

---

## Hard format requirements (both files)

- **Windows BMP, 24-bit, uncompressed (BI_RGB), NO alpha channel.** This is what the DEBUG `LAYER`
  command loads; other formats/bit-depths are silently rejected. One BMP pixel = one canvas pixel
  (the window uses default `DOTSIZE 1`, no scaling).
- Author at the **exact pixel dimensions** below — do not pad, scale, or add margins beyond what is
  specified.
- Standard top-to-bottom, left-to-right visual layout (author it the way it should look on screen;
  the DEBUG loader handles BMP's on-disk row order).

## The one cross-file constraint that must hold (the "seam" rule)

`CROP` is an **opaque** copy with no transparency. When a digit cell is blitted onto the readout
box, the cell's background pixels replace the box pixels. Therefore:

> **The digit-cell background color in `digits.bmp` MUST be byte-identical to the readout-box
> interior color in `panel_bg.bmp`.** Call this shared color **`BOX_BG`**. If they differ by even
> one RGB step, every digit paints a visible rectangle.

Recommended `BOX_BG` = **`RGB(10, 10, 10)`** (`$0A0A0A`, an unlit-LED near-black). Any color is fine
**as long as both files use the exact same value.**

---

## File 1 — `panel_bg.bmp`

**Dimensions:** **200 × 96** pixels (exactly the window `SIZE 200 96`; painted once with
`CROP 1` = whole layer to canvas origin).

**Regions:**

| Region | Rectangle (x, y, w, h) | Requirement |
|--------|------------------------|-------------|
| **Readout box interior** | **(44, 23) → 114 × 54**, i.e. x 44–157, y 23–76 | A **flat, uniform fill of `BOX_BG`** with NO detail, texture, or lines inside it. This region is repeatedly restored (`CROP 1 45 24 110 48`) and overwritten by digit blits — any interior detail would be partially clobbered and look wrong. |
| **Bezel + panel face** | everything else | Static decorative frame. Never touched after the initial paint, so style freely. |

> **Why the box region is bigger than the code's `45 24 110 48`:** the erase rect is
> (45,24,110,48) → x45–154, y24–71, and the three digits blit at x 50/86/122 (each 30 wide) and
> **y 28, height 48 → y28–75**. The union that must be uniform `BOX_BG` is x45–154, y24–75; the
> table adds a 1-px safety margin (x44–157, y23–76). Keep the whole of that flat.

**Suggested styling (aesthetic — adjust freely, but keep the box interior = `BOX_BG`):**
- Panel face: `RGB(32, 32, 32)` `$202020`.
- Bezel: a simple raised frame — e.g. a 2-px outer highlight `RGB(160,160,160)` and a 4-px face
  inset — around the 200×96 edge.
- Readout box: inset the `BOX_BG` rectangle into the panel face with a thin darker border
  **just outside** the (44,23,114,54) flat region so the border is never overwritten.
- Optional: a small label ("READOUT", units) placed **outside** the flat box region.

## File 2 — `digits.bmp`

**Dimensions:** **300 × 48** pixels (10 cells × 30 wide, 48 tall).

**Layout:** a horizontal font strip of digits **`0` `1` `2` `3` `4` `5` `6` `7` `8` `9`**, left to
right. Digit *k* occupies cell **x = k·30 … k·30+29, y = 0 … 47** (the code selects it with
`srcX = digit * 30`, cell size `30 × 48`).

| Property | Requirement |
|----------|-------------|
| Cell background | **`BOX_BG`** — exactly the same value as the panel_bg readout-box interior (seam rule above). |
| Glyph color | A bright readout color. Suggested **amber `RGB(255, 176, 0)` `$FFB000`** (or green `$33FF33`). |
| Glyph metrics | Fixed-width, centered in each 30×48 cell. A glyph roughly **20 wide × 40 tall** centered (≈5-px left/right margin, ≈4-px top/bottom) reads well. All ten digits must share identical metrics/baseline so columns align. |
| Style | Bold and legible — a clean sans or a 7-segment LED face both work. |
| Order / origin | `0` at far left (x 0–29), `9` at far right (x 270–299); upright; cell (0,0) = top-left of `0`. |

---

## Reference generator (Python + Pillow) — optional but authoritative

This produces both files to spec. The generating agent may run this directly or reproduce its
output. Fonts: substitute any bold monospace/sans available; keep the metrics fixed.

```python
from PIL import Image, ImageDraw, ImageFont

BOX_BG   = (10, 10, 10)      # shared seam color — MUST match in both files
PANEL    = (32, 32, 32)
BEZEL    = (160, 160, 160)
GLYPH    = (255, 176, 0)     # amber

# ---- panel_bg.bmp : 200 x 96 ----
bg = Image.new("RGB", (200, 96), PANEL)
d  = ImageDraw.Draw(bg)
d.rectangle([0, 0, 199, 95], outline=BEZEL, width=2)          # bezel frame
d.rectangle([42, 21, 158, 77], outline=(0, 0, 0), width=1)    # box border (outside the flat area)
d.rectangle([44, 23, 157, 76], fill=BOX_BG)                   # flat readout interior (x44-157,y23-76)
bg.save("panel_bg.bmp")                                       # Pillow writes 24-bit BI_RGB

# ---- digits.bmp : 300 x 48, ten 30x48 cells ----
strip = Image.new("RGB", (300, 48), BOX_BG)
d = ImageDraw.Draw(strip)
try:
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 40)
except OSError:
    font = ImageFont.load_default()
for k in range(10):
    s = str(k)
    l, t, r, b = d.textbbox((0, 0), s, font=font)
    w, h = r - l, b - t
    cx = k * 30 + (30 - w) // 2 - l
    cy = (48 - h) // 2 - t
    d.text((cx, cy), s, fill=GLYPH, font=font)
strip.save("digits.bmp")
```

## Acceptance checks (when the files come back)

1. `panel_bg.bmp` is exactly **200×96**, 24-bit; `digits.bmp` is exactly **300×48**, 24-bit
   (`file *.bmp` / any BMP header check).
2. The pixel at, say, `panel_bg (100, 50)` **equals** the pixel at `digits (15, 24)` — proves the
   seam color matches.
3. Drop both into `examples-library/`, compile `ch15-panel-plot.spin2` with a v50+ `pnut_ts`, run
   on hardware: the panel shows a live 3-digit readout sweeping ~0–100, digits crisp, **no visible
   rectangles/seams** around the glyphs, box cleanly erased between frames.
4. Re-zip `examples-library.zip` so the two BMPs ship with the example.
