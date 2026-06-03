# Debug Display Window — Directive Matrix (cross-window reference)

> **Spec authority:** PNut **v55** — `/pascal-source/P2_PNut_Public/DebugDisplayUnit.pas`
> (133,829 bytes, dated 2025-05-08; product title `PNut v55` from `PNut.dpr:23`).
> Re-verified directly against v55 source on 2026-05-31. Line references in this
> document point into that file.
>
> **Scope:** the **9 Pascal-drawn debug *display* windows** only —
> LOGIC, SCOPE, SCOPE_XY, FFT, SPECTRO, PLOT, TERM, BITMAP, MIDI.
> The single-step debugger (`DebuggerUnit.pas`) is **excluded** by design.
>
> **Purpose:** answer three questions per window — (1) what directives configure
> it, (2) what directives display data in it, (3) what directives + handlers
> support keyboard/mouse — as a single cross-window matrix. This is the
> "matrix-first" deliverable; the per-window Theory-of-Operations docs under
> `theory-of-operations/` are refreshed against it in a later pass.

---

## 0. How directives reach a window (protocol framing)

Each DEBUG display message is a stream of **elements**. The element type tags
(`DebugDisplayUnit.pas:14-19`) are:

| `ele_*` | Value | Meaning |
|---|---|---|
| `ele_end` | 0 | end of message |
| `ele_dis` | 1 | display-type selector (first element of a window's creation) |
| `ele_nam` | 2 | window instance name |
| `ele_key` | 3 | a **keyword directive** (one of `key_*`, 41–92) |
| `ele_num` | 4 | a numeric parameter |
| `ele_str` | 5 | a string parameter |

Parsing helpers walk the stream: `NextKey`/`NextNum`/`NextStr`/`NextEnd`
(`4109-4129`). The display type is chosen in `FormCreate` (`633-643`) →
`XXX_Configure`; later messages route through `UpdateDisplay` (`899-912`) →
`XXX_Update`.

Two lifecycle phases matter for this matrix:

- **Configuration phase** (`XXX_Configure`, run once at window creation) — accepts
  the *setup* directives.
- **Update phase** (`XXX_Update`, run on every subsequent message) — accepts the
  *runtime / data-display* directives and the **input** directives (`PC_KEY`,
  `PC_MOUSE`).

The full keyword vocabulary is `key_alt`(41) … `key_window`(92)
(`DebugDisplayUnit.pas:78-105`).

---

## 1. Keyword vocabulary — quick reference

### 1.1 Named-color group `key_black..key_gray` (0–9)
`BLACK WHITE ORANGE BLUE GREEN CYAN RED MAGENTA YELLOW GRAY`. Used wherever a
color is taken; a named color (except BLACK/WHITE) may be followed by an optional
0–15 brightness nibble (`KeyColor`, `2752-2783`).

### 1.2 Color-mode group `key_lut1..key_rgb24` (10–28)
`LUT1 LUT2 LUT4 LUT8 LUMA8 LUMA8W LUMA8X HSV8 HSV8W HSV8X RGBI8 RGBI8W RGBI8X RGB8
HSV16 HSV16W HSV16X RGB16 RGB24`. Selects how packed numeric data is translated to
pixels (`KeyColorMode`, `2785-2804`). LUMA/HSV modes take a tint parameter.

### 1.3 Packed-data group `key_longs_1bit..key_bytes_4bit` (29–40)
Declares how many sub-samples are packed per transmitted long/word/byte and at
what bit width (`PackDef`, `140-152`; `KeyPack`, `2817-2832`). Optional `ALT`
and/or `SIGNED` modifiers (`key_alt`=41, `key_signed`=78).

### 1.4 Functional keywords (41–92)
`ALT AUTO BACKCOLOR BOX CARTESIAN CHANNEL CIRCLE CLEAR CLOSE COLOR CROP DEPTH DOT
DOTSIZE HIDEXY HOLDOFF LAYER LINE LINESIZE LOGSCALE LUTCOLORS MAG OBOX OPACITY
ORIGIN OVAL PC_KEY PC_MOUSE POLAR POS PRECISE RANGE RATE SAMPLES SAVE SCROLL SET
SIGNED SIZE SPACING SPARSE SPRITE SPRITEDEF TEXT TEXTANGLE TEXTSIZE TEXTSTYLE
TITLE TRACE TRIGGER UPDATE WINDOW`.

---

## 2. Configuration directives — which window accepts what

✅ = accepted in that window's `_Configure`. Parameter shapes follow the table.

| Directive | LOGIC | SCOPE | SCOPE_XY | FFT | SPECTRO | PLOT | TERM | BITMAP | MIDI |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| `TITLE 'str'`        | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `POS left top`       | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `SIZE w h`           | —  | ✅ | ✅¹ | ✅ | —  | ✅ | ✅² | ✅ | ✅³ |
| `SAMPLES n {first last}` | ✅ | ✅ | ✅ | ✅⁴ | ✅⁴ | — | — | — | — |
| `SPACING n`          | ✅ | —  | —  | —  | —  | — | — | — | — |
| `RATE n`             | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | ✅ | — |
| `DOTSIZE x {y}`      | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | — |
| `LINESIZE n`         | ✅ | ✅ | —  | ✅ | —  | — | — | — | — |
| `TEXTSIZE n`         | ✅ | ✅ | ✅ | ✅ | —  | — | ✅ | — | — |
| `COLOR ...`          | ✅⁵ | ✅⁵ | ✅⁵ | ✅⁵ | — | — | ✅⁶ | — | ✅⁷ |
| `BACKCOLOR color`    | —  | —  | —  | —  | —  | ✅ | ✅ | — | — |
| color-mode `LUT1..RGB24` | — | — | — | — | ✅⁸ | ✅ | — | ✅ | — |
| `LUTCOLORS rgb24...` | —  | —  | —  | —  | —  | ✅ | — | ✅ | — |
| packed `LONGS_1BIT..BYTES_4BIT` | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | ✅ | — |
| `RANGE n`            | —  | —  | ✅ | —  | ✅ | — | — | — | ✅⁹ |
| `POLAR {twopi theta}`| —  | —  | ✅ | —  | —  | — | — | — | — |
| `LOGSCALE`           | —  | —  | ✅ | ✅ | ✅ | — | — | — | — |
| `DEPTH n`            | —  | —  | —  | —  | ✅ | — | — | — | — |
| `MAG n`              | —  | —  | —  | —  | ✅ | — | — | — | — |
| `TRACE n`            | —  | —  | —  | —  | ✅ | — | — | ✅ | — |
| `SPARSE color`       | —  | —  | —  | —  | —  | — | — | ✅ | — |
| `CHANNEL n`          | —  | —  | —  | —  | —  | — | — | — | ✅ |
| `UPDATE`             | —  | —  | —  | —  | —  | ✅ | ✅ | ✅ | — |
| `HIDEXY`             | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| *string = channel def* | ✅¹⁰ | — | ✅¹¹ | — | — | — | — | — | — |

**Footnotes (config):**
1. SCOPE_XY: `SIZE` takes one value (square); width = `val*2` (`1402-1406`).
2. TERM: `SIZE` is **columns × rows**, not pixels (`2199-2200`).
3. MIDI: `SIZE` is a key-size scalar 1–50, not pixels (`2512-2513`).
4. FFT/SPECTRO: `SAMPLES n {first last}` also sets the displayed bin range
   (`1573-1582`, `1741-1750`).
5. LOGIC/SCOPE/SCOPE_XY/FFT: `COLOR back grid` — background then grid color.
6. TERM: `COLOR` takes up to **8** colors (4 text/background pairs, `2203-2204`).
7. MIDI: `COLOR onWhite onBlack` — two velocity colors (`2522-2524`).
8. SPECTRO color-mode is restricted to `LUMA8..LUMA8X, HSV16..HSV16X` (`1767`).
9. MIDI: `RANGE firstKey lastKey` (MIDI note range 0–127, `2514-2519`).
10. LOGIC channel def: `'name' {count} {RANGE} {color}` (`971-1005`).
11. SCOPE_XY channel def: `'label' {color}` (`1429-1434`).

---

## 3. Display / data directives — which window accepts what (Update phase)

✅ = accepted in that window's `_Update`. "numeric data" = the sample/pixel/byte
stream each window consumes.

| Directive | LOGIC | SCOPE | SCOPE_XY | FFT | SPECTRO | PLOT | TERM | BITMAP | MIDI |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| numeric data stream | samples | samples | samples | samples | samples | (via SET/DOT/…) | chars/codes | pixels | MIDI bytes |
| *string channel def* | — | ✅ | — | ✅ | — | — | text | — | — |
| `TRIGGER ...`   | ✅¹ | ✅² | — | — | — | — | — | — | — |
| `HOLDOFF n`     | ✅ | ✅ | — | — | — | — | — | — | — |
| `CLEAR`         | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `SAVE ...`      | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `UPDATE`        | — | — | — | — | — | ✅ | ✅ | ✅ | — |
| color `BLACK..GRAY` / `COLOR` | — | — | — | — | — | ✅ | ✅ | — | — |
| `BACKCOLOR`     | — | — | — | — | — | ✅ | ✅ | — | — |
| color-mode `LUT1..RGB24` | — | — | — | — | — | ✅ | — | ✅ | — |
| `LUTCOLORS`     | — | — | — | — | — | ✅ | — | ✅ | — |
| `SET x y`       | — | — | — | — | — | ✅ | — | ✅³ | — |
| `SCROLL x y`    | — | — | — | — | — | — | — | ✅ | — |
| `TRACE n`       | — | — | — | — | — | — | — | ✅ | — |
| `RATE n`        | — | — | — | — | — | — | — | ✅ | — |
| `ORIGIN {x y}`  | — | — | — | — | — | ✅ | — | — | — |
| `DOT {size {opa}}` | — | — | — | — | — | ✅ | — | — | — |
| `LINE x y {size {opa}}` | — | — | — | — | — | ✅ | — | — | — |
| `CIRCLE/OVAL/BOX/OBOX ...` | — | — | — | — | — | ✅ | — | — | — |
| `LINESIZE` / `OPACITY` / `PRECISE` | — | — | — | — | — | ✅ | — | — | — |
| `TEXT/TEXTSIZE/TEXTSTYLE/TEXTANGLE` | — | — | — | — | — | ✅ | — | — | — |
| `POLAR` / `CARTESIAN` | — | — | — | — | — | ✅ | — | — | — |
| `LAYER n 'f.bmp'` / `CROP ...` | — | — | — | — | — | ✅ | — | — | — |
| `SPRITEDEF ...` / `SPRITE ...` | — | — | — | — | — | ✅ | — | — | — |
| **`PC_KEY`** (input) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **`PC_MOUSE`** (input) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Footnotes (display):**
1. LOGIC `TRIGGER mask match {offset}` (`1043-1049`).
2. SCOPE `TRIGGER channel (AUTO | arm fire) {offset}` (`1236-1249`).
3. BITMAP `SET x y` also cancels scrolling (`2433-2438`).

**TERM numeric control codes** (`2258-2305`): `0`=clear+home, `1`=home,
`2 n`=set column, `3 n`=set row, `4..7`=select color pair, `8`=backspace,
`9`=tab, `10`/`13`=newline, `32..255`=printable char. Strings print verbatim.

**PLOT** is the only window whose update phase is a full vector/raster drawing
command set (`PLOT_Update`, `1918-2155`) — it consumes almost no bare numeric
stream; geometry comes from `SET`/`DOT`/`LINE`/shape/`SPRITE` directives.

---

## 4. Keyboard & mouse — the shared input model

**Key finding: input handling is overwhelmingly shared, not per-window.** All nine
windows are instances of `TDebugDisplayForm`, so they inherit identical form-level
event handlers, and every window's `_Update` accepts the same two input directives.
Per-window variation exists **only** in coordinate mapping.

### 4.1 Shared form-level handlers (identical for all 9 windows)

| Handler | Lines | Behavior |
|---|---|---|
| `WMGetDlgCode` | 585-589 | Sets `DLGC_WANTTAB` — the window **captures Tab** (Tab won't change focus). |
| `FormMouseMove` | 647-809 | Draws a live **measurement cursor** showing the cursor's coordinates in that window's coordinate system (see §4.4). Suppressed when `HIDEXY` set (`737`). |
| `FormMouseWheel` | 811-817 | Latches wheel direction into `vMouseWheel` (+1/−1) for **100 ms**, then auto-clears (`FormMouseWheelTimerTick`, 819-823). |
| `FormKeyPress` | 825-831 | Latches the pressed key byte into `vKeyPress` for **100 ms**, then auto-clears (`FormKeyTimerTick`, 853-857). |
| `FormKeyDown` | 833-851 | Maps non-printable keys to control codes and forwards to `FormKeyPress`: Left=1, Right=2, Up=3, Down=4, Home=5, End=6, Delete=7, Insert=10, PageUp=11, PageDown=12. |

The 100 ms latch means the P2 only reads input that occurred within ~100 ms of its
`PC_KEY`/`PC_MOUSE` poll — a key/wheel event not consumed in time is dropped.

### 4.2 `PC_KEY` → `SendKeyPress` (3579-3583) — *identical for all windows*

Transmits one LONG = the latched `vKeyPress` byte (0 if none), then clears it.
There is **no per-window keyboard difference** — keyboard semantics are uniform
across all nine windows.

### 4.3 `PC_MOUSE` → `SendMousePos` (3537-3577) — same mechanism, per-window coords

Transmits **two LONGs**:

- **LONG 1 — packed position + buttons + wheel:**
  `x` = bits 0–12, `y` = bits 13–25, `wheel` (`vMouseWheel`) = bits 26–27,
  L/M/R buttons = bits 28/29/30 (`GetAsyncKeyState` of `VK_LBUTTON`/`MBUTTON`/
  `RBUTTON`). If the cursor is outside the client area (or outside the text area
  for TERM), LONG 1 = `$03FFFFFF` and LONG 2 = `$FFFFFFFF` (sentinel "off-window").
- **LONG 2 — RGB color** of the pixel under the cursor (`Canvas.Pixels`, byte-
  swapped to `$RRGGBB`).

### 4.4 Per-window coordinate mapping (the only input difference)

⚠️ **Two different coordinate systems** — the on-screen measurement readout and the
`PC_MOUSE` wire value are computed by *different code* and do **not** agree for every
window. Do not assume the P2 receives what the readout shows.

**(a) On-screen measurement readout** (`FormMouseMove`, `656-740`) — full per-window
transform, shown only as the live cursor text (suppressed by `HIDEXY`):

| Window | On-screen coordinate basis |
|---|---|
| LOGIC | sample index (−) , channel row; origin bottom-right (`660-667`) |
| SCOPE, FFT | pixel offset from plot origin, Y inverted (`668-675`) |
| SCOPE_XY | scaled data value; Cartesian *or* polar (rho,theta) per `POLAR`/`LOGSCALE` (`676-718`) |
| PLOT | `pixel ÷ DOTSIZE`, honoring `CARTESIAN` flip flags `vDirX`/`vDirY` (`719-724`) |
| TERM | character **column,row** (`÷ ChrWidth/ChrHeight`); off-text-area = blank (`725-732`) |
| SPECTRO, BITMAP | `pixel ÷ DOTSIZE` (no direction flip in the readout) (`733-734`) |
| MIDI | *(no coordinate readout)* |

**(b) `PC_MOUSE` wire value** (`SendMousePos`, `3537-3577`) — only **two** transforms
exist; everything else is sent as **raw client pixels**:

| Window(s) | `PC_MOUSE` x,y transform |
|---|---|
| SPECTRO, PLOT, BITMAP | `÷ DOTSIZE`, with `if vDirX: x:=ClientWidth−x` and `if not vDirY: y:=ClientHeight−y` (`3556-3562`) — note this **Y-inverts SPECTRO/BITMAP**, which the on-screen readout does **not** |
| TERM | character column,row, `÷ ChrWidth/ChrHeight` from the text origin (`3563-3567`) |
| LOGIC, SCOPE, SCOPE_XY, FFT | **none — raw client pixel x,y** (the sample-index / Y-inversion / scaled-value transforms in (a) are *not* applied on the wire) |
| MIDI | raw client pixel x,y |

`HIDEXY` suppresses only the (a) on-screen readout; it does **not** disable (b)
`PC_MOUSE` reporting back to the P2.

---

## 5. Per-window summary cards

Each card lists **config**, **display/data**, and **input** in one place.
Line refs are to `DebugDisplayUnit.pas` (v55).

### 5.1 LOGIC (`dis_logic`=0) — `Configure 926`, `Update 1034`
- **Config:** TITLE, POS, SAMPLES(4..2047), SPACING, RATE, DOTSIZE, LINESIZE,
  TEXTSIZE, COLOR(back,grid), HIDEXY, packed; channel-name strings with
  `{count}{RANGE}{color}`.
- **Display:** numeric sample longs; TRIGGER(mask,match,offset), HOLDOFF, CLEAR,
  SAVE.
- **Input:** shared model; PC_KEY, PC_MOUSE. Cursor = sample,row.

### 5.2 SCOPE (`dis_scope`=1) — `Configure 1151`, `Update 1209`
- **Config:** TITLE, POS, SIZE(px), SAMPLES(16+), RATE, DOTSIZE, LINESIZE,
  TEXTSIZE, COLOR(back,grid), HIDEXY, packed.
- **Display:** numeric samples; channel-def strings (`AUTO` | lo hi, tall, base,
  grid, color); TRIGGER(channel, AUTO|arm fire, offset), HOLDOFF, CLEAR, SAVE.
- **Input:** shared model; PC_KEY, PC_MOUSE. Cursor = pixel x, inverted y.

### 5.3 SCOPE_XY (`dis_scope_xy`=2) — `Configure 1386`, `Update 1443`
- **Config:** TITLE, POS, SIZE(square), RANGE, SAMPLES(0=persistent), RATE,
  DOTSIZE(2..20), TEXTSIZE, COLOR(back,grid), POLAR{twopi,theta}, LOGSCALE,
  HIDEXY, packed; label strings `{color}`.
- **Display:** numeric XY pairs; CLEAR, SAVE.
- **Input:** shared model; PC_KEY, PC_MOUSE. Cursor = data value, Cartesian or
  polar.

### 5.4 FFT (`dis_fft`=3) — `Configure 1552`, `Update 1620`
- **Config:** TITLE, POS, SIZE(px), SAMPLES n{first last}, RATE, DOTSIZE,
  LINESIZE(±), TEXTSIZE, COLOR(back,grid), LOGSCALE, HIDEXY, packed.
- **Display:** numeric samples; channel-def strings (mag, high, tall, base, grid,
  color); CLEAR, SAVE.
- **Input:** shared model; PC_KEY, PC_MOUSE. Cursor = pixel x, inverted y.

### 5.5 SPECTRO (`dis_spectro`=4) — `Configure 1719`, `Update 1792`
- **Config:** TITLE, POS, SAMPLES n{first last}, DEPTH, MAG, RANGE, RATE, TRACE,
  DOTSIZE(x,y), color-mode(LUMA8..LUMA8X/HSV16..HSV16X), LOGSCALE, HIDEXY, packed.
- **Display:** numeric samples; CLEAR, SAVE.
- **Input:** shared model; PC_KEY, PC_MOUSE. Cursor = pixel ÷ dotsize.

### 5.6 PLOT (`dis_plot`=5) — `Configure 1864`, `Update 1918`
- **Config:** TITLE, POS, SIZE(px), DOTSIZE(x,y), color-mode(LUT1..RGB24),
  LUTCOLORS, BACKCOLOR, UPDATE, HIDEXY.
- **Display (rich vector/raster set):** color-mode, LUTCOLORS, BACKCOLOR,
  COLOR/named-color, OPACITY, PRECISE, LINESIZE, ORIGIN, SET, DOT, LINE, CIRCLE,
  OVAL, BOX, OBOX, TEXT/TEXTSIZE/TEXTSTYLE/TEXTANGLE, LAYER, CROP, SPRITEDEF,
  SPRITE, POLAR, CARTESIAN, CLEAR, UPDATE, SAVE.
- **Input:** shared model; PC_KEY, PC_MOUSE. Cursor = pixel ÷ dotsize, with
  CARTESIAN flip.

### 5.7 TERM (`dis_term`=6) — `Configure 2181`, `Update 2223`
- **Config:** TITLE, POS, SIZE(cols×rows), TEXTSIZE, COLOR(up to 8), BACKCOLOR,
  UPDATE, HIDEXY.
- **Display:** named color (text{,back}), BACKCOLOR, CLEAR, UPDATE, SAVE; numeric
  control codes 0–13 + printable 32–255; strings.
- **Input:** shared model; PC_KEY, PC_MOUSE. Cursor = char col,row; off-text =
  sentinel.

### 5.8 BITMAP (`dis_bitmap`=7) — `Configure 2372`, `Update 2416`
- **Config:** TITLE, POS, SIZE(px), DOTSIZE(x,y), SPARSE, color-mode(LUT1..RGB24),
  LUTCOLORS, TRACE, RATE, packed, UPDATE, HIDEXY.
- **Display:** numeric pixels; color-mode, LUTCOLORS, TRACE, RATE, SET, SCROLL,
  CLEAR, UPDATE, SAVE.
- **Input:** shared model; PC_KEY, PC_MOUSE. Cursor = pixel ÷ dotsize.

### 5.9 MIDI (`dis_midi`=8) — `Configure 2492`, `Update 2590`
- **Config:** TITLE, POS, SIZE(keysize 1–50), RANGE(firstKey,lastKey),
  CHANNEL(0–15), COLOR(onWhite,onBlack).
- **Display:** MIDI byte stream (note-on/off velocity); CLEAR, SAVE.
- **Input:** shared model; PC_KEY, PC_MOUSE. No coordinate readout.

---

## 6. Notable v55 facts & gotchas

- **`HIDEXY`** is accepted by **all windows except MIDI**; it hides the local
  measurement cursor only — `PC_MOUSE` still reports to the P2.
- **`PC_KEY`/`PC_MOUSE` are universal** — present in all nine `_Update` methods.
  Keyboard behavior is identical everywhere; mouse differs only in coordinate
  mapping (§4.4).
- **`SIZE` is overloaded:** pixels (SCOPE/FFT/PLOT/BITMAP), square-from-half
  (SCOPE_XY), columns×rows (TERM), key-size scalar (MIDI). Not a uniform directive.
- **`SAVE`** (`KeySave`, 2839-2866) writes the window bitmap to `<name>.bmp`, or a
  desktop region (`WINDOW` keyword, or l/t/w/h) — available in every window's
  update phase.
- **`CLOSE`** (`key_close`=49) and **`CHANNEL`** (`key_channel`=46) exist in the
  keyword table; `CLOSE` has no live handler in the display windows (only PLOT has
  a `_Close` for cleanup, 2169), and `CHANNEL` is used only by MIDI config.
- **`UPDATE`** turns a window into buffered/manual-refresh mode (PLOT/TERM/BITMAP):
  drawing accumulates in `Bitmap[0]` and is only copied to screen on an explicit
  `UPDATE` directive.

---

## 7. Parameter values & legal ranges

This section gives the **value space** of every directive parameter: numeric range,
enumerated keyword set, or free-string format. All ranges are the exact
`Within`/`KeyValWithin(v, min, max)` clamps in v55 source. Out-of-range numeric
values are **clamped** (not rejected); an unrecognized keyword ends parsing of the
current directive.

### 7.0 Global defaults (`SetDefaults`, 2880-2917)

Applied to every window *before* its `_Configure` runs; a window's "unique
defaults" then override some of these.

| State | Default | State | Default |
|---|---|---|---|
| width × height | 256 × 256 | colorMode | `RGB24` |
| samples | 256 | colorTune | 0 |
| backColor | `clBlack` `$000000` | gridColor | `clGray` `$404040` |
| lineSize | 1 | dotSize | (per-window) |
| textSize | 10 | textStyle | 1 |
| textAngle | 0 | logScale | off |
| update mode | off | hideXY | off |
| rate | 0 | holdOff | 0 |
| polar | off | twoPi / theta | `$100000000` / 0 |
| sparse | −1 (off) | plotColor | `clCyan` `$00FFFF` |
| textColor | `clWhite` `$FFFFFF` | channel colors | `DefaultScopeColors[0..7]` (see §7.1 palette) |

### 7.0a Per-window font size & default window size

**Font size.** The global `FontSize` preference (set in `EditorUnit`, default **10**,
user-adjustable 1–72) and the `DefaultTextSize = 10` constant both default to **10**, so
every display window starts at **10 pt** except MIDI. The `TEXTSIZE` directive (where
accepted) clamps to **6..200** via `KeyTextSize` (2834-2837).

| Window | Default font size | Set in | `TEXTSIZE` directive? |
|---|---|---|---|
| LOGIC    | `FontSize` = **10** | 939 | yes — config (961) |
| SCOPE    | `FontSize` = **10** | 1159 | yes — config (1178) |
| SCOPE_XY | `FontSize` = **10** | 1392 | yes — config (1416) |
| FFT      | `FontSize` = **10** | 1563 | yes — config (1590) |
| TERM     | `FontSize` = **10** | 2186 | yes — config (2202) |
| PLOT     | `DefaultTextSize` = **10** | inherits `SetDefaults` 2894 | yes — **update phase** only (2037; also inline `TEXT`) |
| SPECTRO  | `DefaultTextSize` = **10** (no text drawn) | inherits 2894 | **no** |
| BITMAP   | `DefaultTextSize` = **10** (no text drawn) | inherits 2894 | **no** |
| MIDI     | `MidiKeySize div 3` = **8** | 2528 | no — scales with `SIZE` (`MidiSize` 1..50 ⇒ font 4..69) |
| *Debugger (single-step)* | `FontSize` ≈ **10**, auto-shrunk so 123 cols ≤ 4096 px | `DebuggerUnit` 597-604 | no |

**Default window size.** All sizes are before user `SIZE`/`POS`. SCOPE/SCOPE_XY/FFT
inherit `vWidth=vHeight=256` from `SetDefaults`; PLOT/SPECTRO/BITMAP draw a `vWidth ×
vHeight` (× dotsize) client with zero margins; LOGIC/TERM/MIDI compute size from
content; the debugger is a fixed character grid.

| Window | Default size (pre-`SIZE`) | `SIZE` directive | Notes |
|---|---|---|---|
| LOGIC    | `vSamples·vSpacing × channels·ChrHeight` = `32·8 × 32·ChrHeight` = **256 px** wide × 32-channel tall | — (driven by `SAMPLES`/`SPACING`/channel count) | + label-width left margin, `ChrHeight` top/bottom |
| SCOPE    | **256 × 256** (plot area) | `w h`, 32..2048 each | + `ChrWidth`/`ChrHeight·2` margins |
| SCOPE_XY | **256 × 256** (square) | `w` → `w·2` clamped 32..2048; height = width | square; + `ChrHeight·2` margins all sides |
| FFT      | **256 × 256** (plot area) | `w h`, 32..2048 each | + `ChrWidth`/`ChrHeight·2` margins |
| SPECTRO  | **256 × 256** (depth 256 × bins 256; `vTrace=$F` → no swap) | `DEPTH` 1..2048 + `SAMPLES` (bins) | zero margins; ×`vDotSize`/`vDotSizeY` (1×1) |
| PLOT     | **256 × 256** | `w h`, 32..2048 each | zero margins; ×dotsize (1×1) |
| TERM     | **40 × 20 chars** (`DefaultCols × DefaultRows`) → `40·ChrWidth × 20·ChrHeight` px | `cols rows`, 1..256 each | + `ChrWidth div 2` margins |
| BITMAP   | **256 × 256** | `w h`, 1..2048 each | zero margins; ×dotsize (1×1) |
| MIDI     | computed: `MidiKeySize·whiteKeys + border·2 × MidiKeySize·6 + border`; default 88-key (`RANGE` 21..108), `MidiSize=4` ⇒ ≈ **1256 × 148 px** | `SIZE` = `MidiSize` 1..50 | also `RANGE` changes key span |
| *Debugger* | `ChrWidth·123 × (ChrHeight·77)÷2` (fixed `123 × 77`-half-row grid) ⇒ ≈ **985 × 655 px** @ 10 pt | none (not resizable) | `DebuggerUnit.SmoothFillMax = 4096` |

### 7.1 Enumerated keyword value sets — the "legal strings"

These are the fixed keyword vocabularies a parameter may take. A color parameter
(`KeyColor`, 2752-2783) accepts **either** a named color **or** a numeric value
interpreted through the current color mode.

**Named colors** (`key_black..key_gray`, ids 0-9) — optional trailing brightness
nibble `0..15` (default `8`) for all except BLACK/WHITE (`KeyColor`, `2756-2783`).

⚠️ **These named-directive colors are NOT the `clXxx` palette constants** (see
the palette table below). Only `BLACK` and `WHITE` are returned as fixed literals
(`$000000`/`$FFFFFF`, special-cased at `2764-2767`). The other eight are *computed*
through the **RGBI8X** color space: `c := TranslateColor(h shl 5 or p shl 1,
key_rgbi8x)` where `h = id − key_orange` (the hue 0-7) and `p` is the brightness
nibble. The resolved RGB therefore depends on brightness and only *approximates*
the similarly-named palette constant. Values below are at the **default brightness
8** (verified by executing the Pascal `TranslateColor`/`KeyColor` math):

| Keyword | id | RGB @ bri 8 | RGB @ bri 15 | Keyword | id | RGB @ bri 8 | RGB @ bri 15 |
|---|--:|---|---|---|--:|---|---|
| `BLACK`   | 0 | `$000000` (fixed) | `$000000` | `CYAN`    | 5 | `$09FFFF` | `$EFFFFF` |
| `WHITE`   | 1 | `$FFFFFF` (fixed) | `$FFFFFF` | `RED`     | 6 | `$FF0909` | `$FFEFEF` |
| `ORANGE`  | 2 | `$FF8409` | `$FFF7EF` | `MAGENTA` | 7 | `$FF09FF` | `$FFEFFF` |
| `BLUE`    | 3 | `$0909FF` | `$EFEFFF` | `YELLOW`  | 8 | `$FFFF09` | `$FFFFEF` |
| `GREEN`   | 4 | `$09FF09` | `$EFFFEF` | `GRAY`    | 9 | `$848484` | `$F7F7F7` |

Higher brightness nibbles blend the hue toward white; lower nibbles toward black.
A numeric value (no keyword) is instead interpreted through the *current* color
mode (`vColorMode`), not RGBI8X.

**Palette constants** (`clXxx`, `DebugDisplayUnit.pas` 179-191) — these are the
**fixed literal RGB24 values** used for window/channel *defaults* (e.g.
`DefaultScopeColors`, `DefaultTermColors`, grid/back/plot/text defaults). They are
locally-defined literals, **not** VCL `TColor`s and **not** the named-directive
colors above:

| Constant | Hex | Constant | Hex | Constant | Hex |
|---|---|---|---|---|---|
| `clRed`    | `$FF0000` | `clCyan`    | `$00FFFF` | `clWhite` | `$FFFFFF` |
| `clLime`   | `$00FF00` | `clOrange`  | `$FF7F00` | `clBlack` | `$000000` |
| `clBlue`   | `$7F7FFF` | `clOlive`   | `$7F7F00` | `clGray`  | `$404040` |
| `clYellow` | `$FFFF00` | `clMagenta` | `$FF00FF` | `clGray2` | `$808080` |
|            |           |             |           | `clGray3` | `$D0D0D0` |

**Color modes** (`key_lut1..key_rgb24`, ids 10-28; `KeyColorMode`, 2785-2804).
LUMA/HSV/RGBI variants take a tune parameter (`W`/`X` suffixes select tuning
behavior):
`LUT1 LUT2 LUT4 LUT8 LUMA8 LUMA8W LUMA8X HSV8 HSV8W HSV8X RGBI8 RGBI8W RGBI8X RGB8
HSV16 HSV16W HSV16X RGB16 RGB24`.
*SPECTRO restricts its config color mode to `LUMA8 LUMA8W LUMA8X HSV16 HSV16W
HSV16X` only (1767).*

**Packed-data formats** (`key_longs_1bit..key_bytes_4bit`, ids 29-40;
`PackDef`, 140-152) — each unpacks one transmitted value into N sub-samples of B
bits:

| Keyword | sub-samples × bits | Keyword | sub-samples × bits |
|---|---|---|---|
| `LONGS_1BIT`  | 32 × 1 | `WORDS_1BIT` | 16 × 1 |
| `LONGS_2BIT`  | 16 × 2 | `WORDS_2BIT` | 8 × 2 |
| `LONGS_4BIT`  | 8 × 4  | `WORDS_4BIT` | 4 × 4 |
| `LONGS_8BIT`  | 4 × 8  | `WORDS_8BIT` | 2 × 8 |
| `LONGS_16BIT` | 2 × 16 | `BYTES_1BIT` | 8 × 1 |
| `BYTES_2BIT`  | 4 × 2  | `BYTES_4BIT` | 2 × 4 |

Modifiers (follow a packed keyword, `KeyPack` 2817-2832): `ALT` (alternate
nibble/word ordering) and `SIGNED` (sign-extend sub-samples). Either or both,
any order.

**Standalone modifier keywords:** `AUTO` (SCOPE channel/trigger auto-range;
PLOT CROP), `RANGE` (LOGIC channel range grouping), `WINDOW` (SAVE whole-window
region).

**Free-text string parameters** (no enumeration):
- `TITLE 'text'` — window caption (any text).
- channel/label strings (LOGIC/SCOPE/SCOPE_XY/FFT) — any text; LOGIC label may be
  followed by count/RANGE/color.
- `LAYER n 'file.bmp'` — path; **must exist and end in `.bmp`** (2060).
- `SAVE 'name'` — writes `name.bmp`; `SAVE l t w h 'name'` or `SAVE WINDOW 'name'`
  for a desktop region (`KeySave`, 2839-2866).

### 7.2 Resolved limit constants (symbol → value, 154-239)

| Symbol | Value | Symbol | Value |
|---|--:|---|--:|
| `DataSets` (`LogicSets`,`Y_Sets`,`XY_Sets`,`FFTmax`,`SmoothFillMax`) | 2048 ¹ | `Channels` | 8 |
| `LogicChannels` | 32 | `FFTexpMax` | 11 |
| `fft_default` | 512 | `DefaultCols` × `DefaultRows` | 40 × 20 |
| `scope/scope_xy/plot _wmin/_hmin` | 32 | `…_wmax/_hmax` | 2048 |
| `bitmap_wmin/_hmin` | 1 | `bitmap_wmax/_hmax` | 2048 |
| `term_colmin/_rowmin` | 1 | `term_colmax/_rowmax` | 256 |
| `plot_layermax` | 8 | `SpriteMax` | 256 |
| `SpriteMaxX/Y` | 32 | `DefaultTextSize` | 10 |

¹ These five are all `DataSets = 1 shl 11 = 2048` in **`DebugDisplayUnit.pas`** (the nine
debug-display windows). ⚠️ The single-step debugger is a separate unit: **`DebuggerUnit.pas`
redefines `SmoothFillMax = 4096`** (`DataSets`/`LogicSets`/etc. do not exist there). Don't
carry the 2048 value across to the debugger window.

### 7.3 Per-window parameter value tables

Each row: directive → parameter(s) with **type · legal range / legal set ·
default**. "color" = named color (§7.1) or numeric-through-color-mode.

#### LOGIC (`Configure 926`, `Update 1034`)
| Directive | Parameter(s) — type · range · default |
|---|---|
| `TITLE` | `'text'` · free string |
| `POS` | left, top · int (offset from base window pos) |
| `SAMPLES` | n · int **4..2047** · 32 |
| `SPACING` | n · int **1..32** · 8 |
| `RATE` | n · int **1..2048** · 1 |
| `DOTSIZE` | n · int **0..32** · 0 |
| `LINESIZE` | n · int **1..32** · 3 |
| `TEXTSIZE` | n · int **6..200** · 10 |
| `COLOR` | back, grid · color, color |
| `HIDEXY` | *(flag)* |
| packed | `LONGS_1BIT..BYTES_4BIT` `{ALT}{SIGNED}` |
| channel str | `'name'` · {count int **1..32**} · {`RANGE`} · {color} |
| *(Update)* `TRIGGER` | mask, match · int; offset · int **0..samples-1** |
| *(Update)* `HOLDOFF` | n · int **2..2048** |

#### SCOPE (`Configure 1151`, `Update 1209`)
| Directive | Parameter(s) — type · range · default |
|---|---|
| `TITLE` / `POS` | as LOGIC |
| `SIZE` | w · int **32..2048** · 256; h · int **32..2048** · 256 |
| `SAMPLES` | n · int **16..2048** · 256 |
| `RATE` | n · int **1..2048** · 1 |
| `DOTSIZE` | n · int **0..32** · 0¹ |
| `LINESIZE` | n · int **0..32** · 3¹ |
| `TEXTSIZE` | n · int **6..200** · 10 |
| `COLOR` | back, grid · color, color |
| `HIDEXY` / packed | as LOGIC |
| channel str | `'label'` · (`AUTO` \| low, high · int32) · tall, base, grid · int · {color} |
| *(Update)* `TRIGGER` | channel · int **−1..7**; (`AUTO` \| arm, fire · int32); offset · int **0..samples-1** |
| *(Update)* `HOLDOFF` | n · int **2..2048** |

¹ if DOTSIZE and LINESIZE both 0, DOTSIZE forced to 1 (1188).

#### SCOPE_XY (`Configure 1386`, `Update 1443`)
| Directive | Parameter(s) — type · range · default |
|---|---|
| `SIZE` | n · int; effective width = `n*2` clamped **32..2048**; square |
| `RANGE` | n · int **1..$7FFFFFFF** · $7FFFFFFF |
| `SAMPLES` | n · int **0..2048** · 256 (0 = persistent display) |
| `RATE` | n · int **1..2048** · 1 |
| `DOTSIZE` | n · int **2..20** · 6 |
| `TEXTSIZE` | n · int **6..200** · 10 |
| `COLOR` | back, grid · color, color |
| `POLAR` | twoPi · int (−1/0 ⇒ `$100000000`, else value); theta · int |
| `LOGSCALE` / `HIDEXY` | *(flags)* |
| label str | `'label'` · {color} |

#### FFT (`Configure 1552`, `Update 1620`)
| Directive | Parameter(s) — type · range · default |
|---|---|
| `SIZE` | w, h · int **32..2048** · 256, 256 |
| `SAMPLES` | n · int **4..2048** (→ rounded to power of 2) · 512; first · int **0..n/2−2** · 0; last · int **first+1..n/2−1** · n/2−1 |
| `RATE` | n · int **1..2048** |
| `DOTSIZE` | n · int **0..32** · 0 |
| `LINESIZE` | n · int **−32..32** · 3 (negative ⇒ vertical filled bars) |
| `TEXTSIZE` | n · int **6..200** · 10 |
| `COLOR` | back, grid · color, color |
| `LOGSCALE` / `HIDEXY` / packed | as above |
| channel str | `'label'` · mag · int **0..11**; high · int **1..$7FFFFFFF**; tall, base, grid · int · {color} |

#### SPECTRO (`Configure 1719`, `Update 1792`)
| Directive | Parameter(s) — type · range · default |
|---|---|
| `SAMPLES` | n · int **4..2048** · 512; first/last as FFT |
| `DEPTH` | n · int **1..2048** |
| `MAG` | n · int **0..11** · 0 |
| `RANGE` | n · int **1..$7FFFFFFF** · $7FFFFFFF |
| `RATE` | n · int **1..2048** |
| `TRACE` | n · int (bit-field; 3 dir bits + scroll) · $F |
| `DOTSIZE` | x · int **1..16** · 1; y · int **1..16** · 1 |
| color-mode | `LUMA8 LUMA8W LUMA8X HSV16 HSV16W HSV16X` only · LUMA8X |
| `LOGSCALE` / `HIDEXY` / packed | as above |

#### PLOT (`Configure 1864`, `Update 1918`)
| Directive | Parameter(s) — type · range · default |
|---|---|
| `SIZE` | w, h · int **32..2048** · 256, 256 |
| `DOTSIZE` | x · int **1..256** · 1; y · int **1..256** · 1 |
| color-mode / `LUTCOLORS` / `BACKCOLOR` | mode keyword / up to 256 rgb24 / color |
| `UPDATE` / `HIDEXY` | *(flags)* |
| *(Update)* `COLOR` | color · color (or `BLACK..GRAY {bright 0..15}`) |
| *(Update)* `OPACITY` | byte · int **0..255** · 255 |
| *(Update)* `PRECISE` | *(toggle; sub-pixel on/off)* |
| *(Update)* `LINESIZE` | n · int |
| *(Update)* `ORIGIN` | {x, y · int} (else current pixel) |
| *(Update)* `SET` | x, y · int (rho/theta if polar) |
| *(Update)* `DOT` | {linesize · int {opacity · int **0..255**}} |
| *(Update)* `LINE` | x, y · int {linesize {opacity}} |
| *(Update)* `CIRCLE` | width {linesize {opacity}} |
| *(Update)* `OVAL`/`BOX` | width, height {linesize {opacity}} |
| *(Update)* `OBOX` | width, height, xradius, yradius {linesize {opacity}} |
| *(Update)* `TEXT` | {size {style {angle}}} `'string'` |
| *(Update)* `TEXTSIZE`/`TEXTSTYLE`/`TEXTANGLE` | n · int |
| *(Update)* `LAYER` | n · int **1..8**; `'file.bmp'` (must exist) |
| *(Update)* `CROP` | layer **1..8**; (`AUTO` x y \| left top width height {x y}) |
| *(Update)* `SPRITEDEF` | id **0..255**; xsize **1..32**; ysize **1..32**; pixels…; 256 colors |
| *(Update)* `SPRITE` | id **0..255** {orient **0..7** {scale **1..64** {opacity **0..255**}}} |
| *(Update)* `POLAR` | {twoPi; theta} · int | `CARTESIAN` {flipY {flipX} · bool} |

#### TERM (`Configure 2181`, `Update 2223`)
| Directive | Parameter(s) — type · range · default |
|---|---|
| `SIZE` | cols · int **1..256** · 40; rows · int **1..256** · 20 |
| `TEXTSIZE` | n · int **6..200** · 10 |
| `COLOR` | up to **8** colors (4 text/back pairs) · default `ORANGE/BLACK ×2, LIME/BLACK ×2` |
| `BACKCOLOR` | color |
| `UPDATE` / `HIDEXY` | *(flags)* |
| *(Update)* color | `BLACK..GRAY` (text {, back}) · `BACKCOLOR` color |
| *(Update)* control | int **0..13** (0=clr+home,1=home,2=col,3=row,4-7=color pair,8=bksp,9=tab,10/13=newline) and **32..255**=printable |
| *(Update)* string | any text (printed verbatim) |

`set column` arg **0..cols−1**; `set row` arg **0..rows−1** (2273-2275).

#### BITMAP (`Configure 2372`, `Update 2416`)
| Directive | Parameter(s) — type · range · default |
|---|---|
| `SIZE` | w · int **1..2048** · 256; h · int **1..2048** · 256 |
| `DOTSIZE` | x · int **1..256** · 1; y · int **1..256** · 1 |
| `SPARSE` | color (−1 = off/normal) |
| color-mode / `LUTCOLORS` | as PLOT |
| `TRACE` | n · int (8 scan patterns + scroll bit) · 0 |
| `RATE` | n · int (−1 ⇒ width×height) |
| packed / `UPDATE` / `HIDEXY` | as above |
| *(Update)* `SET` | x · int **0..w−1**; y · int **0..h−1** (cancels scroll) |
| *(Update)* `SCROLL` | x · int **−w..w**; y · int **−h..h** |
| *(Update)* `TRACE` | n · int | `RATE` n · int |
| *(Update)* pixel | int (through color mode / packing) |

#### MIDI (`Configure 2492`, `Update 2590`)
| Directive | Parameter(s) — type · range · default |
|---|---|
| `SIZE` | n · int **1..50** · 4 (key-size scalar) |
| `RANGE` | firstKey · int **0..127** · 21; lastKey · int **firstKey..127** · 108 |
| `CHANNEL` | n · int **0..15** · 0 |
| `COLOR` | onWhite, onBlack · color, color · `CYAN`, `MAGENTA` |
| *(Update)* MIDI bytes | int **0..255** (note-on/off velocity state machine) |
| *(Update)* `CLEAR`/`SAVE` | — |

*(All windows additionally accept `PC_KEY` and `PC_MOUSE` in their update phase — see §4 for the shared keyboard/mouse model and return-value layouts.)*

---

*Authored 2026-05-31, value/range reference added 2026-06-01, against PNut v55
`DebugDisplayUnit.pas`. This matrix is the punch-list for refreshing the nine
per-window Theory-of-Operations docs under
`DOCs/pascal-REF/theory-of-operations/` (which were last verified at v51 / 2025-11-08).*
