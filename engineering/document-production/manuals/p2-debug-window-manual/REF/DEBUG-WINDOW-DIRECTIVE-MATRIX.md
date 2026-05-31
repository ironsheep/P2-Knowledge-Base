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

The cursor coordinate reported by **both** the live measurement cursor
(`FormMouseMove`) and `PC_MOUSE` (`SendMousePos`) is transformed per display type:

| Window | Reported coordinate basis |
|---|---|
| LOGIC | sample index (−) × channel row; origin bottom-right (`660-667`) |
| SCOPE, FFT | pixel offset from plot origin, Y inverted (`668-675`) |
| SCOPE_XY | scaled data value; Cartesian *or* polar (rho,theta) per `POLAR`/`LOGSCALE` (`676-718`) |
| PLOT | `pixel ÷ DOTSIZE`, honoring `CARTESIAN` flip flags `vDirX`/`vDirY` (`719-724`, `3558-3561`) |
| TERM | character **column,row** (`÷ ChrWidth/ChrHeight`); off-text-area = sentinel (`725-732`, `3563-3567`) |
| SPECTRO, BITMAP | `pixel ÷ DOTSIZE`, honoring direction flags (`733-734`, `3556-3562`) |
| MIDI | *(no coordinate readout / no special mapping)* |

`HIDEXY` (config directive) suppresses the on-screen measurement-cursor readout;
it does **not** disable `PC_MOUSE` reporting back to the P2.

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

*Authored 2026-05-31 against PNut v55 `DebugDisplayUnit.pas`. This matrix is the
punch-list for refreshing the nine per-window Theory-of-Operations docs under
`DOCs/pascal-REF/theory-of-operations/` (which were last verified at v51 / 2025-11-08).*
