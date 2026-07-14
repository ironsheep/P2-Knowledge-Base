# BITMAP Window - Complete Theory of Operations

**Current as of**: PNut v55 for Propeller 2
**Document Version**: 1.2
**Date**: 2026-07-14 (v1.2 — conflict-audit conformance pass: re-grounded against raw
`DebugDisplayUnit.pas` v55. Corrected the `SetSize` sparse gate + client/bitmap sizing, the
`StretchDraw` scaling story, sparse cell geometry (solid fill + **round** dot), the LUT
"default palette" claim, the colour-mode id order, `CLEAR`/`TRACE` discarding `RATE`, the
`RATE -1` and un-dotsized-`SAVE` footguns, the horizontal scroll fill strips, and the borrowed
PLOT `CIRCLE`/`TEXTSTYLE` encodings — which are re-scoped as **PLOT's, not BITMAP's**.)
**Source Files**: DebugDisplayUnit.pas, DebugUnit.pas, SerialUnit.pas, GlobalUnit.pas
**Author**: Analysis of P2 PNut Debug Display System
**Companion**: [Debug Window Directive Matrix](../DEBUG-WINDOW-DIRECTIVE-MATRIX.md) — cross-window directive reference; directive coverage re-verified against `DebugDisplayUnit.pas` (v55) on 2026-06-01

> **TS parity (2026-06-06):** The `DebugBitmapWindow` implementation was brought to full parity
> with this spec by the 9-window parity sprint **§15** (build 0.9.27): default color mode RGB24
> with one sample per long, tune consumed only by LUMA8/HSV modes (RGBI8/LUT/RGB consume none),
> `LUTCOLORS` overwriting the palette from index 0, the mode-dependent clear background
> (`GetBackground`: white for W modes, palette[0] for LUT, else black), sparse disabled below dot
> size 4, and named colors for SPARSE/LUTCOLORS. See matrix §8 and `bitmapResidualsParity.test.ts`.

---

## Executive Summary

The BITMAP window in DebugDisplayUnit.pas is a pixel-based display system that receives pixel data over a serial connection from a Propeller 2 microcontroller and renders it to a scalable bitmap canvas. The window supports 19 different color modes, 8 trace/scan patterns with optional scrolling, packed data formats, and sparse (magnified, LED-matrix-style) pixel rendering. It is a **bitmap receiver**, not a graphics canvas.

> **⚠️ BITMAP has NO drawing primitives.** `BITMAP_Update` (2416–2485) accepts **only** pixel
> numbers plus the commands `LUT1..RGB24`, `LUTCOLORS`, `TRACE`, `RATE`, `SET`, `SCROLL`,
> `CLEAR`, `UPDATE`, `SAVE`, `PC_KEY`, `PC_MOUSE` (and `CLOSE`, dispatched in the parser).
> There is **no `LINE`, no `CIRCLE`, no `OVAL`, no `BOX`, no `TEXT`, no `SPRITE`** — those are
> `PLOT_Update` directives and BITMAP does **not** inherit them (see §11, §17.5). BITMAP shares
> only the *internal* renderers (`SmoothShape`, `TranslateColor`, `StepTrace`, `ScrollBitmap`)
> with PLOT/SPECTRO; sharing a renderer is not sharing a directive.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Data Structures](#2-data-structures)
3. [Window Creation and Initialization](#3-window-creation-and-initialization)
4. [Serial Communication and Data Flow](#4-serial-communication-and-data-flow)
5. [BITMAP_Update Method - Data Processing](#5-bitmap_update-method---data-processing)
6. [Color Modes and Translation](#6-color-modes-and-translation)
7. [Trace Modes and Pixel Positioning](#7-trace-modes-and-pixel-positioning)
8. [Pixel Rendering Modes](#8-pixel-rendering-modes)
9. [Scrolling System](#9-scrolling-system)
10. [Display Update Messages and Commands](#10-display-update-messages-and-commands)
11. [Drawing Primitives (PLOT Integration)](#11-drawing-primitives-plot-integration)
12. [Sprite System](#12-sprite-system)
13. [Performance Characteristics](#13-performance-characteristics)
14. [Key Behaviors and Edge Cases](#14-key-behaviors-and-edge-cases)
15. [Integration Points](#15-integration-points)
16. [Advanced Features](#16-advanced-features)
17. [Limitations and Constraints](#17-limitations-and-constraints)
18. [Comparison to Related Display Types](#18-comparison-to-related-display-types)

---

## 1. Architecture Overview

### 1.1 Display Type Classification
- **Display Type ID**: `dis_bitmap = 7` (DebugDisplayUnit.pas:29)
- **Display Name**: "BITMAP" (DebugDisplayUnit.pas:137)
- Part of a family of 9 debug display types (LOGIC, SCOPE, SCOPE_XY, FFT, SPECTRO, PLOT, TERM, BITMAP, MIDI)

### 1.2 Key Constants
```pascal
bitmap_wmin         = 1                     // Minimum width (DebugDisplayUnit.pas:229)
bitmap_wmax         = SmoothFillMax = 2048  // Maximum width
bitmap_hmin         = 1                     // Minimum height (DebugDisplayUnit.pas:231)
bitmap_hmax         = SmoothFillMax = 2048  // Maximum height (DebugDisplayUnit.pas:232)
SmoothFillMax       = DataSets = 2048       // Maximum dimension
```

### 1.3 Primary Use Cases
1. **Bitmap Receiver**: Display streaming pixel data from P2 ADC, camera, or sensor
2. **2D Graphics Canvas**: Draw shapes, text, sprites with primitives
3. **Image Processing**: Visualize processed image data with various color modes
4. **Oscilloscope Persistence**: Scrolling persistence display with trace modes
5. **Video Display**: Show video frames with color mode conversion

---

## 2. Data Structures

### 2.1 Bitmap-Specific Variables (DebugDisplayUnit.pas:252-412)

```pascal
// Display dimensions
vWidth              : integer               // Logical bitmap width (pixels)
vHeight             : integer               // Logical bitmap height (pixels)
vBitmapWidth        : integer               // Physical bitmap width (may differ if scaled)
vBitmapHeight       : integer               // Physical bitmap height
vClientWidth        : integer               // Window client area width
vClientHeight       : integer               // Window client area height

// Margins (zero for BITMAP/SPECTRO/PLOT)
vMarginLeft         : integer               // Left margin (0 for bitmap)
vMarginRight        : integer               // Right margin (0 for bitmap)
vMarginTop          : integer               // Top margin (0 for bitmap)
vMarginBottom       : integer               // Bottom margin (0 for bitmap)

// Pixel positioning
vPixelX             : integer               // Current X position (0..vWidth-1)
vPixelY             : integer               // Current Y position (0..vHeight-1)
vTrace              : integer               // Trace mode (bits 0-2: pattern, bit 3: scroll enable)
vDotSize            : integer               // Pixel X-size for sparse mode (1-256)
vDotSizeY           : integer               // Pixel Y-size for sparse mode (1-256)
vSparse             : integer               // Sparse pixel border color (-1=normal, other=sparse)

// Color system
vColorMode          : integer               // Active color mode (key_lut1..key_rgb24)
vLut                : array[0..255] of integer  // Lookup table for palette modes
vColorTune          : integer               // Color tuning parameter (hue shift, color select)

// Update control
vRate               : integer               // Update rate (pixels per screen update)
vRateCount          : integer               // Update rate counter
vUpdate             : boolean               // Manual update mode (true=wait for UPDATE command)
```

### 2.2 Bitmap Storage Arrays

```pascal
Bitmap              : array[0..1] of TBitmap    // Double-buffered bitmaps
BitmapLine          : array[0..SmoothFillMax-1] of Pointer  // Scanline pointers for direct access
```

**Bitmap[0]**: Rendering target (all drawing operations)
**Bitmap[1]**: Display buffer (copied to screen)
**BitmapLine[]**: Direct pointers to pixel data for fast PlotPixel operations

### 2.3 Shared PLOT/BITMAP Arrays (for drawing primitives)

```pascal
// Sprite system (shared with PLOT)
SpritePixels        : array[0..SpriteMax * SpriteMaxX * SpriteMaxY - 1] of byte
SpriteColors        : array[0..SpriteMax * 256 - 1] of integer
SpriteSizeX         : array[0..SpriteMax - 1] of byte
SpriteSizeY         : array[0..SpriteMax - 1] of byte

// Constants
SpriteMax           = 256                   // Maximum sprite count
SpriteMaxX          = 32                    // Maximum sprite width
SpriteMaxY          = 32                    // Maximum sprite height
```

### 2.4 Packed Data Support

```pascal
vPackAlt            : boolean               // Alternate packing mode (2 numbers per value)
vPackSignx          : boolean               // Sign-extend packed values
vPackMask           : integer               // Bit mask for extraction
vPackShift          : integer               // Right shift for next sample
vPackCount          : integer               // Samples per packed value (1-32)
```

---

## Directive Reference (v55-verified)

Complete directive coverage for BITMAP from the [Debug Window Directive Matrix](../DEBUG-WINDOW-DIRECTIVE-MATRIX.md) §5.8, re-verified against `DebugDisplayUnit.pas` v55. Line references point into that file.

### Configuration directives

Parsed in `BITMAP_Configure` (lines 2372–2414) during window creation.

| Directive | Parameters | Range / default / notes | Pascal line |
|---|---|---|---|
| `TITLE` | `'string'` | Free text; sets window caption | `KeyTitle` |
| `POS` | `left top` | int, int; window screen position | `KeyPos` |
| `SIZE` | `w h` | int **1..2048** each; default 256 × 256 (`bitmap_wmin/wmax`, `bitmap_hmin/hmax`) | `2386` |
| `DOTSIZE` | `x {y}` | int **1..256** each; default 1 × 1; if `y` omitted it copies `x` | `2388–2392` |
| `SPARSE` | `color` | Named color (`BLACK`..`GRAY` + optional 0–15 brightness) **or a number interpreted through the *currently-active* color mode** (`KeyColor` 2780: `c := TranslateColor(val, vColorMode)`) — RGB24 only if the mode is still the default RGB24. Sets `vSparse` (default −1 = off). ⚠️ **`SPARSE` alone does NOT enable sparse rendering: it additionally requires `DOTSIZE` ≥ 4 on BOTH axes.** `SetSize` (2938) keeps `vSparse` only if `(vSparse <> -1) and (vDotSize >= 4) and (vDotSizeY >= 4)`; otherwise it silently forces `vSparse := -1` (2947). | `2393–2394`; `KeyColor 2752–2783`; gate `2938`/`2947` |
| color-mode | `LUT1` `LUT2` `LUT4` `LUT8` `LUMA8` `LUMA8W` `LUMA8X` `HSV8` `HSV8W` `HSV8X` `RGBI8` `RGBI8W` `RGBI8X` `RGB8` `HSV16` `HSV16W` `HSV16X` `RGB16` `RGB24` (ids **10–28**, in that order — see §6.1) | 19 modes; default `RGB24`. Tune-parameter parsing differs by family (`KeyColorMode` 2788-2803): **LUMA8/8W/8X** take an optional tint — a color keyword (`ORANGE`..`GRAY`) **or** a numeric value; **HSV8/16 families** take a numeric tune value only; **RGBI8/8W/8X take no tune** (RGBI derives its shade from the pixel bits, `TranslateColor` 3118-3119). | `KeyColorMode`; `2395–2396` (range `key_lut1..key_rgb24`) |
| `LUTCOLORS` | `rgb24…` | Up to 256 RGB24 palette entries; only meaningful with LUT1/2/4/8 mode. ⚠️ **There is no default palette** — `vLut[]` is written *only* here (2806–2815) and is otherwise zero-initialised, so a LUT mode without `LUTCOLORS` renders entirely black (§6.2, §17.4) | `2397–2398` |
| `TRACE` | `n` | int **0..15** (bits 0–2 = scan pattern 0–7, bit 3 = scroll enable); default 0 | `2399–2400`; see §3.2 |
| `RATE` | `n` | int; pixels per screen update; **−1 ⇒ auto-set to `vWidth × vHeight`** (whole-frame refresh) — this substitution exists **only** at the tail of `BITMAP_Configure` (2413), i.e. **only in the CREATE message**; 0 ⇒ `SetTrace(vTrace, vRate = 0)` derives it as `vWidth` (scan patterns 0–3) or `vHeight` (4–7); default 0 | `2401–2402`, `2412–2413` |
| packed | `LONGS_1BIT` … `BYTES_4BIT` | 12 keywords; optional `ALT` and/or `SIGNED` modifiers | `KeyPack`; `2403–2404` |
| `UPDATE` | — | Flag; enables manual-refresh mode; display only updates on explicit `UPDATE` command | `2405–2406` |
| `HIDEXY` | — | Flag; suppresses on-screen measurement-cursor readout; does **not** disable `PC_MOUSE` | `2407–2408` |

> After `BITMAP_Configure` completes: `SetSize(0,0,0,0)` (zero margins), `SetTrace(vTrace, vRate=0)` (initialise pixel position), then `if vRate = -1 then vRate := vWidth * vHeight` (`2411–2413`).

> **Default window size:** `vWidth × vHeight = 256 × 256` (from global `SetDefaults`,
> `2880–2884`; overridable by `SIZE`, range 1..2048 each). With `vDotSize = vDotSizeY = 1`
> the client area is `256 × 256` px; sparse mode multiplies by dot size (`vWidth·vDotSize ×
> vHeight·vDotSizeY`).
>
> **Font size:** BITMAP draws **no text** — `BITMAP_Configure` does not touch `vTextSize`,
> so it remains at `DefaultTextSize = 10` (`SetDefaults`, 2894), and BITMAP exposes **no
> `TEXTSIZE` directive**. The value is effectively unused.

### Display / data directives

Parsed in `BITMAP_Update` (lines 2416–2485) on every subsequent debug message.

| Directive | Parameters | Range / default / behavior | Pascal line |
|---|---|---|---|
| *numeric pixel stream* | integer values | Each number → one pixel (or multiple if packed); color-translated via `vColorMode` and plotted at current trace position; `BitmapToCanvas` called every `vRate` pixels (via `RateCycle`) | `2459–2483` |
| color-mode | (same 19 modes as config) | Change active color mode mid-stream; affects all subsequent pixels | `2425–2426` |
| `LUTCOLORS` | `rgb24…` | Replace LUT palette entries at runtime | `2427–2428` |
| `TRACE` | `n` | int **0..15**; change scan pattern mid-stream; resets pixel position; `SetTrace(val, True)` — `ModifyRate` is **hard-coded True**, so this also **re-derives `vRate`** (to `vWidth` for patterns 0–3, `vHeight` for 4–7), discarding a user-set `RATE` | `2429–2430` |
| `RATE` | `n` | int; change pixels-per-update rate at runtime. ⚠️ **Bare `KeyVal(vRate)` — there is NO `-1` substitution here** (unlike configure, 2413). See the `RATE -1` footgun below. | `2431–2432` |
| `SET` | `x y` | x: int **0..w−1**; y: int **0..h−1**; jump cursor and **cancel scroll** (clears bit 3 of `vTrace`) | `2433–2438` |
| `SCROLL` | `x y` | x: int **−w..w**; y: int **−h..h**; positive x = right, positive y = down; fills the **vacated** strip with `GetBackground` (§9.1) | `2439–2442` |
| `CLEAR` | — | `ClearBitmap` → refresh display unless `UPDATE` mode → **`SetTrace(vTrace, True)`**: resets the pixel position to the trace start **and re-derives `vRate`** to `vWidth` (patterns 0–3) or `vHeight` (4–7). ⚠️ **A user-set `RATE` is silently DISCARDED by any `CLEAR`.** | `2443–2448` |
| `UPDATE` | — | Force screen refresh (`BitmapToCanvas(0)`); required when manual-refresh mode active | `2449–2450` |
| `SAVE` | see grammar below | `KeySave` (2839–2866) — six forms, three of which write no file. `SAVE 'name'` writes **`Bitmap[1]`** (the front buffer) at **1× LOGICAL scale, un-dotsized** (see below). | `KeySave`; `2451–2452` |
| `CLOSE` | — | Closes the window and frees its display slot. **Dispatched in the parser, not here** — it appears in no `_Update` case statement; `p2com.asm` (19565–19624) clears the display's bit in `debug_display_ena` and `TDebugForm.ChrIn` (`DebugUnit.pas:236–237`) runs the **full update first, then closes**. So `` `MyBmp SAVE 'shot' CLOSE `` saves *and then* closes. Command-only (ignored on a create line); multi-target (`` `B1 B2 CLOSE `` closes both). | `p2com.asm 19565–19624`; `DebugUnit.pas 236–237` |

#### `SAVE` grammar (`KeySave`, 2839–2866)

| Form | What it writes |
|---|---|
| `SAVE 'name'` | `Bitmap[1]` (the **front/display** buffer) → `name.bmp` |
| `SAVE WINDOW 'name'` | desktop **scrape** of the window's *outer* rect — **includes title bar and borders**; vulnerable to occlusion by other windows |
| `SAVE left top width height 'name'` | desktop scrape of an arbitrary screen region |
| `SAVE WINDOW` (no name) | captures to memory, **writes no file** |
| `SAVE l t w h` (no name) | captures to memory, **writes no file** |
| `SAVE` (bare) | `Exit` — **does nothing at all** |

The filename always comes **last**; `.bmp` is appended automatically.
**Sharp edge (2846–2848):** a non-`WINDOW` keyword after `SAVE` is consumed and then discarded by
the `Exit` — `` `MyBmp SAVE CLEAR `` does nothing **and eats the `CLEAR`**.

> **🔴 `SAVE 'name'` is UN-DOTSIZED.** It writes `Bitmap[1]`, and `DOTSIZE` magnification is a
> **display-time `StretchDraw`** (`BitmapToCanvas` 3526–3527) that **never touches the bitmap**.
> So on a normal (non-sparse) window, `SAVE 'shot'` yields a `vWidth × vHeight` file — a
> `SIZE 64 64 DOTSIZE 8` window that fills 512×512 px on screen saves a **64×64** .bmp.
> **Sole exception:** a genuinely *sparse* window (`SPARSE` colour **and** `DOTSIZE` ≥ 4 on both
> axes), where `SetSize` allocates the bitmaps at physical size (2938–2943) — that one saves at
> `vWidth·vDotSize × vHeight·vDotSizeY`.
> **To capture the magnified on-screen appearance, use `SAVE WINDOW 'name'`.**

> **🔴 `RATE -1` footgun — it works in the CREATE message ONLY.**
> The `-1 → vWidth * vHeight` substitution lives at the tail of `BITMAP_Configure` (**2413**:
> `if vRate = -1 then vRate := vWidth * vHeight;`). `BITMAP_Update`'s handler is a bare
> `KeyVal(vRate)` (**2431–2432**) with **no** substitution. And `RateCycle` (3079–3088) tests
> **equality** — `if vRateCount = vRate` — not `>=`. So a *runtime* `RATE -1` (or `RATE 0`)
> leaves the rate non-positive, the counter can never match it, and **auto-refresh freezes
> permanently** until a subsequent `TRACE`, `CLEAR` (both re-derive `vRate`) or an explicit
> `UPDATE` intervenes. Real v55 behaviour.

### Keyboard & mouse

Implemented via the **shared input model** — identical form-level handlers for all nine debug display windows (§4 of the Directive Matrix).

| Handler | Lines | Notes |
|---|---|---|
| `WMGetDlgCode` | 585–589 | Captures Tab key (`DLGC_WANTTAB`); prevents focus change |
| `FormMouseMove` | 647–809 | Draws live measurement cursor; suppressed when `HIDEXY` set (`737`) |
| `FormMouseWheel` | 811–823 | Latches wheel direction into `vMouseWheel` ±1 for 100 ms |
| `FormKeyPress` / `FormKeyDown` | 825–857 | Latches key byte into `vKeyPress` for 100 ms; arrow/nav keys mapped to codes 1–12 |

**`PC_KEY`** → `SendKeyPress` (3579–3583): transmits one LONG = latched `vKeyPress` byte (0 if none), then clears it.

**`PC_MOUSE`** → `SendMousePos` (3537–3577): transmits two LONGs.
- LONG 1: `x` bits 0–12, `y` bits 13–25, `vMouseWheel` bits 26–27, L/M/R buttons bits 28–30. Sentinel `$03FFFFFF` / `$FFFFFFFF` when cursor is outside the client area.
- LONG 2: RGB color of pixel under cursor.

**BITMAP coordinate mapping** — ⚠️ **on-screen readout and `PC_MOUSE` wire value differ in Y origin** (same situation as SPECTRO):
- **On-screen readout** (`FormMouseMove`, 733–734): `x = X ÷ DOTSIZE`, `y = Y ÷ DOTSIZEY` — top-origin, **no** direction flip.
- **`PC_MOUSE` wire value** (`SendMousePos`, 3556–3562, shared `dis_spectro, dis_plot, dis_bitmap` branch): applies `if not vDirY then y := ClientHeight − y` before dividing. `vDirY` is always `False` for BITMAP (only PLOT's `CARTESIAN` sets it), so the wire value is **Y-inverted** (bottom-origin): `y = (ClientHeight − Y) ÷ DOTSIZEY`.

`HIDEXY` suppresses the on-screen readout but does **not** disable `PC_MOUSE` reporting.

---

## 3. Window Creation and Initialization

### 3.1 Creation Flow (DebugDisplayUnit.pas:591-645)

**Step 1: Constructor** (Create method, lines 551-576)
- Called by DebugUnit when serial command `DebugDisplayType[0] = 1` is received
- Sets up form properties, bitmaps, timers, and event handlers
- Creates two 24-bit bitmaps for double-buffering

**Step 2: FormCreate Event** (DebugDisplayUnit.pas:591-645)
1. Creates bitmaps (Bitmap[0], Bitmap[1])
2. Retrieves display type from `P2.DebugDisplayValue[0]` (should be 7 for BITMAP)
3. Sets window caption from `P2.DebugDisplayValue[1]` + " - BITMAP"
4. Positions window at `P2.DebugDisplayLeft`, `P2.DebugDisplayTop`
5. Calls `SetDefaults()` to initialize variables
6. Sets `ptr := 2` (starts parsing parameters at index 2)
7. Calls `BITMAP_Configure()` based on DisplayType

### 3.2 BITMAP_Configure Method (DebugDisplayUnit.pas:2372-2414)

**Default Values Set** (lines 2375-2377):
```pascal
vTrace      = 0             // Top line, left-to-right, no scroll
vDotSize    = 1             // 1:1 pixel mapping
vDotSizeY   = 1             // 1:1 pixel mapping
```

**Parameter Parsing Loop** (lines 2379-2409):
```pascal
while NextKey do
  case val of
    key_title:          KeyTitle;
    key_pos:            KeyPos;
    key_size:           KeySize(vWidth, vHeight, bitmap_wmin, bitmap_wmax, bitmap_hmin, bitmap_hmax);
    key_dotsize:        [Set pixel scale: vDotSize, vDotSizeY]
    key_sparse:         KeyColor(vSparse);
    key_lut1..key_rgb24: KeyColorMode;
    key_lutcolors:      KeyLutColors;
    key_trace:          KeyVal(vTrace);
    key_rate:           KeyVal(vRate);
    key_longs_1bit..key_bytes_4bit: KeyPack;
    key_update:         vUpdate := True;
    key_hidexy:         vHideXY := True;
  end;
```

**Supported Configuration Keywords**:

| Keyword | Parameters | Description |
|---------|------------|-------------|
| `title` | string | Set window title |
| `pos` | x, y | Set window position |
| `size` | width, height | Set bitmap dimensions (1-2048) |
| `dotsize` | x [y] | Set pixel scale (sparse mode) |
| `sparse` | color | Enable sparse mode with border color |
| `lut1..rgb24` | [params] | Set color mode |
| `lutcolors` | colors... | Define LUT palette |
| `trace` | mode | Set trace/scan pattern (0-15) |
| `rate` | count | Set update rate (pixels per refresh) |
| `longs_1bit` etc. | [alt] [signed] | Set packed data format |
| `update` | - | Enable manual update mode |
| `hidexy` | - | Hide mouse coordinate display |

**Trace Mode Encoding** (decoded in `SetTrace` 2973-2980 [start corner] + `StepTrace` 2982-3061 [step direction + scroll]):
```
Bits 0-2: Scan pattern (0-7)
Bit 3:    Scroll enable (0=wrap, 1=scroll)

%0000: Top line, left-to-right,    no scroll
%0001: Top line, right-to-left,    no scroll
%0010: Bottom line, left-to-right, no scroll
%0011: Bottom line, right-to-left, no scroll
%0100: Left line, top-to-bottom,   no scroll
%0101: Left line, bottom-to-top,   no scroll
%0110: Right line, top-to-bottom,  no scroll
%0111: Right line, bottom-to-top,  no scroll

%1000: Top line, left-to-right,    scroll down
%1001: Top line, right-to-left,    scroll down
%1010: Bottom line, left-to-right, scroll up
%1011: Bottom line, right-to-left, scroll up
%1100: Left line, top-to-bottom,   scroll right
%1101: Left line, bottom-to-top,   scroll right
%1110: Right line, top-to-bottom,  scroll left
%1111: Right line, bottom-to-top,  scroll left
```

**Preparation Phase** (lines 2411-2413):
```pascal
SetSize(0, 0, 0, 0);                     // Zero margins for bitmap
SetTrace(vTrace, vRate = 0);             // Initialize pixel position
if vRate = -1 then vRate := vWidth * vHeight;  // Default: full bitmap
```

**SetTrace Method** (DebugDisplayUnit.pas:2973-2980):
```pascal
procedure TDebugDisplayForm.SetTrace(Path: integer; ModifyRate: boolean);
begin
  if Path and 7 in [0, 2, 4, 5] then vPixelX := 0 else vPixelX := vWidth - 1;
  if Path and 7 in [0, 1, 4, 6] then vPixelY := 0 else vPixelY := vHeight - 1;
  if ModifyRate then
    if Path and 7 in [0, 1, 2, 3] then vRate := vWidth else vRate := vHeight;
  vTrace := Path and $F;
end;
```

**Window Sizing** (SetSize method, lines 2926-2971):

For BITMAP (and SPECTRO/PLOT) — verbatim structure of `SetSize` 2934–2970:
```pascal
if DisplayType in [dis_spectro, dis_plot, dis_bitmap] then
begin
  ClientWidth  := vWidth  * vDotSize;      // 2936 — UNCONDITIONAL (sparse or not)
  ClientHeight := vHeight * vDotSizeY;     // 2937 — UNCONDITIONAL
  if (vSparse <> -1) and (vDotSize >= 4) and (vDotSizeY >= 4) then
  begin                                    // 2938 — the real SPARSE gate
    Bitmap[1].Width := ClientWidth;   Bitmap[1].Height := ClientHeight;   // 2940-2941
    Bitmap[0].Width := ClientWidth;   Bitmap[0].Height := ClientHeight;   // 2942-2943
  end                                      //        ⇒ bitmaps are PHYSICAL size
  else
  begin
    vSparse := -1;                         // 2947 — sparse SILENTLY SELF-DISABLES
    Bitmap[1].Width := vWidth;   Bitmap[1].Height := vHeight;             // 2948-2949
    Bitmap[0].Width := vWidth;   Bitmap[0].Height := vHeight;             // 2950-2951
  end                                      //        ⇒ bitmaps are LOGICAL size
end;
vBitmapWidth  := Bitmap[0].Width;   vBitmapHeight := Bitmap[0].Height;    // 2963-2964
vClientWidth  := ClientWidth;       vClientHeight := ClientHeight;        // 2965-2966
for i := 0 to vBitmapHeight - 1 do BitmapLine[i] := Bitmap[0].ScanLine[i];// 2967
vTriggered := False;                                                      // 2969
ClearBitmap;                                                              // 2970 — SetSize always clears
```

**🔴 The sparse gate (2938) — three conditions, all required:**

> Sparse rendering needs a `SPARSE` **colour** *and* `DOTSIZE` **≥ 4 on BOTH axes**.
> If any of the three fails, `SetSize` forces `vSparse := -1` (2947) and the window renders in
> **normal** mode — **sparse silently self-disables, with no error.** `SPARSE $404040 DOTSIZE 3`
> is therefore *not* a sparse window.

Consequences that the rest of this document depends on:

| | `vSparse` after `SetSize` | `Bitmap[0]/[1]` size | Client size | `BitmapToCanvas` StretchDraw |
|---|---|---|---|---|
| **Sparse active** (colour set, both dot sizes ≥ 4) | the colour | **physical** `vWidth·vDotSize × vHeight·vDotSizeY` (2940-2943) | same | **1:1 — no scaling** |
| **Sparse off, `DOTSIZE` > 1** | −1 (2947) | **logical** `vWidth × vHeight` (2948-2951) | `vWidth·vDotSize × vHeight·vDotSizeY` (2936-2937) | **upscales** (nearest-neighbour) |
| **Sparse off, `DOTSIZE` = 1** (default) | −1 | logical = client | `vWidth × vHeight` | 1:1 |

Note that `ClientWidth`/`ClientHeight` are set **unconditionally** at 2936–2937: `DOTSIZE 4` with
**no** `SPARSE` still produces a 4×-sized window — it just fills it by stretching a logical-size
bitmap rather than by drawing physical-size cells.

**Note**: Unlike SCOPE/FFT, BITMAP has zero margins. The entire bitmap is the drawable area.

---

## 4. Serial Communication and Data Flow

### 4.1 Serial Reception (SerialUnit.pas)
[Identical to FFT - see FFT documentation]

### 4.2 Debug Command Parsing (DebugUnit.pas:200-236)
[Identical to FFT - see FFT documentation]

### 4.3 Display Update Trigger (DebugUnit.pas:224-232)
[Identical to FFT - see FFT documentation]

### 4.4 Element Parsing Helpers (DebugDisplayUnit.pas:4109-4139)

`NextKey` **4109–4112**, `NextNum` **4114–4117**, `NextStr` **4119–4122**, `NextEnd` **4124–4127**,
`NextElement` **4129–4139** (the `// Get Elements //` block runs 4105–4139).
[Identical to FFT - see FFT documentation]

---

## 5. BITMAP_Update Method - Data Processing

### 5.1 Method Signature (DebugDisplayUnit.pas:2416-2485)
```pascal
procedure TDebugDisplayForm.BITMAP_Update;
var
  i, v, x, y: integer;
```

**Purpose**:
- Process incoming pixel data or commands from serial stream
- Plot pixels to bitmap using current trace mode
- Handle runtime configuration changes

### 5.2 Update Loop Structure (lines 2420-2484)
```pascal
while not NextEnd do              // Process all elements until ele_end
begin
  if NextStr then Break;          // Strings not allowed in BITMAP

  if NextKey then                 // Keyword = command
    case val of
      key_lut1..key_rgb24:   [change color mode]
      key_lutcolors:         [update palette]
      key_trace:             [change trace pattern]
      key_rate:              [change update rate]
      key_set:               [set pixel position]
      key_scroll:            [scroll bitmap]
      key_clear:             [clear bitmap]
      key_update:            [force display update]
      key_save:              [save bitmap to file]
      key_pc_key:            [send keyboard event]
      key_pc_mouse:          [send mouse event]
    end
  else
    while NextNum do              // Numbers = pixel data
      [process numeric pixels]
end;
```

### 5.3 Command Processing (lines 2423-2456)

**key_lut1..key_rgb24** (lines 2425-2426):
```pascal
key_lut1..key_rgb24:
  KeyColorMode;    // Change active color mode
```
- Changes `vColorMode` to new palette/color format
- Affects all subsequent pixel data interpretation

**key_lutcolors** (lines 2427-2428):
```pascal
key_lutcolors:
  KeyLutColors;    // Update LUT palette entries
```
- Reads up to 256 RGB24 color values
- Stores in `vLut[]` array
- Only affects LUT1/LUT2/LUT4/LUT8 color modes

**key_trace** (lines 2429-2430):
```pascal
key_trace:
  if NextNum then SetTrace(val, True);
```
- Changes scan pattern mid-stream
- Resets pixel position to starting corner
- Optionally adjusts `vRate` for new pattern

**key_set** (lines 2433-2438):
```pascal
key_set:
begin
  vTrace := vTrace and 7;              // Cancel scrolling
  if KeyValWithin(vPixelX, 0, vWidth - 1) then
    KeyValWithin(vPixelY, 0, vHeight - 1);
end;
```
- Manually positions pixel cursor
- Disables scroll mode (keeps scan pattern)
- Useful for random-access pixel writes

**key_scroll** (lines 2439-2442):
```pascal
key_scroll:
  if KeyValWithin(x, -vWidth, vWidth) then
    if KeyValWithin(y, -vHeight, vHeight) then
      ScrollBitmap(x, y);
```
- Manually scrolls bitmap by (x, y) pixels
- Positive x = scroll right, negative = scroll left
- Positive y = scroll down, negative = scroll up
- Fills vacated area with background color

**key_clear** (lines 2443-2448):
```pascal
key_clear:
begin
  ClearBitmap;                              // 2445
  if not vUpdate then BitmapToCanvas(0);    // 2446
  SetTrace(vTrace, True);                   // 2447 — ModifyRate = TRUE, unconditionally
end;
```
- Fills bitmap with the mode-dependent background color (`GetBackground`)
- Resets pixel position to the trace's starting corner
- Updates display (unless manual update mode)
- ⚠️ **Silently discards any user-set `RATE`.** `ModifyRate` is passed as a hard-coded `True`, so
  `SetTrace` (2977–2978: `if ModifyRate then if Path and 7 in [0,1,2,3] then vRate := vWidth else
  vRate := vHeight;`) **overwrites `vRate`** with `vWidth` (scan patterns 0–3) or `vHeight`
  (patterns 4–7). A `RATE n` sent earlier does not survive a `CLEAR`. (Same for a runtime
  `TRACE n`, which also passes `True` — 2430.) This is a real parity trap: re-send `RATE` after
  every `CLEAR` if you depend on it.

**key_update** (lines 2449-2450):
```pascal
key_update:
  BitmapToCanvas(0);    // Force screen update
```
- Manually triggers display refresh
- Required when `vUpdate = True` (manual mode)

### 5.4 Pixel Processing (lines 2458-2483)

**Two Rendering Paths**:

**Path 1: Normal Pixels** (vSparse = -1):
```pascal
while NextNum do
begin
  v := NewPack;                          // Get packed value (if enabled)
  for i := 1 to vPackCount do            // Unpack all samples
  begin
    PlotPixel(UnPack(v));                // Plot pixel at current position

    if RateCycle and not vUpdate then    // Update screen if rate reached
      BitmapToCanvas(0);

    StepTrace;                           // Advance to next pixel position
  end;
end;
```

**PlotPixel Method** (DebugDisplayUnit.pas:3433-3444):
```pascal
procedure TDebugDisplayForm.PlotPixel(p: integer);
var
  v: integer;
  line: PByteArray;
begin
  p := TranslateColor(p, vColorMode);    // Convert to RGB24
  line := BitmapLine[vPixelY];           // Get scanline pointer
  v := vPixelX * 3;                      // 3 bytes per pixel (24-bit)
  line[v+0] := p shr 0;                  // Blue
  line[v+1] := p shr 8;                  // Green
  line[v+2] := p shr 16;                 // Red
end;
```

**Path 2: Sparse Pixels** (vSparse ≠ -1 — i.e. a `SPARSE` colour **and** `DOTSIZE` ≥ 4 on both axes, §3.2):
```pascal
while NextNum do
begin
  v := NewPack;
  for i := 1 to vPackCount do
  begin
    // Center of the cell, in PHYSICAL bitmap coordinates (2470-2471)
    x := vPixelX * vDotSize + vDotSize shr 1;
    y := vPixelY * vDotSizeY + vDotSizeY shr 1;

    // Call 1 (2472-2474): SOLID FILLED RECTANGLE over the WHOLE cell, in the sparse colour.
    //   xro=yro=0 ⇒ rectangle := True (SmoothShape 3617); thick=0 ⇒ solid := True (3616).
    SmoothShape(x, y,
                vDotSize, vDotSizeY,
                0, 0, 0, vSparse, 255);

    // Call 2 (2475-2478): the DATA pixel — a ROUND DOT / ELLIPSE at 3/4 cell size.
    //   size = 3/4 cell; the radii passed (vDotSize, vDotSizeY) exceed half the size, so
    //   SmoothShape's clamp (3638-3639: if xro shl 1 > xs then xro := xs shr 1) forces
    //   MAXIMUM rounding ⇒ a fully-rounded ellipse, not a square.
    SmoothShape(x, y,
                vDotSize - vDotSize shr 2, vDotSizeY - vDotSizeY shr 2,
                vDotSize, vDotSizeY,
                0, TranslateColor(UnPack(v), vColorMode), 255);

    if RateCycle and not vUpdate then BitmapToCanvas(0);
    StepTrace;
  end;
end;
```

**Sparse Mode Effect**:
- Each logical pixel becomes a `vDotSize × vDotSizeY` **cell** drawn at physical coordinates
  (in sparse mode the bitmap *is* physical-size — see §3.2, §21.2).
- **Call 1 is not a border/frame.** It is a solid fill of the entire cell in the `SPARSE` colour.
- **Call 2 lays a round dot** (data colour, ~3/4 of the cell) on top of that fill. v55 calls these
  "large **round** pixels" (v55 §BITMAP, L1329).
- The grid / LED-matrix appearance is simply the **residual sparse colour left visible around the
  dot** (most of all in the cell corners) — nothing draws a grid line.
- **Every pixel is drawn.** Both `SmoothShape` calls run unconditionally for every unpacked
  sample; there is **no** "skip the pixel if its value equals the sparse colour" rule.

---

## 6. Color Modes and Translation

### 6.1 Supported Color Modes (19 modes)

Listed **in keyword-id order** (`DebugDisplayUnit.pas:43–61`). ⚠️ **The order is load-bearing** —
the ids are consumed as *ranges*: `BITMAP_Configure` (2395) and `BITMAP_Update` (2425) both
dispatch on `key_lut1..key_rgb24`, and `KeyColorMode` tests `val in [key_luma8..key_luma8x]`
(2788) and `val in [key_hsv8..key_hsv8x, key_hsv16..key_hsv16x]` (2802). Note that the **HSV8
family precedes the RGBI8 family**, and `RGB8` follows `RGBI8X`.

| id | Mode | Keyword | Bits/Pixel | Description |
|---:|------|---------|------------|-------------|
| 10 | LUT1 | `key_lut1` | 1 | 2-color palette (bit 0 → vLut[0..1]) |
| 11 | LUT2 | `key_lut2` | 2 | 4-color palette (bits 0-1 → vLut[0..3]) |
| 12 | LUT4 | `key_lut4` | 4 | 16-color palette (bits 0-3 → vLut[0..15]) |
| 13 | LUT8 | `key_lut8` | 8 | 256-color palette (byte → vLut[0..255]) |
| 14 | LUMA8 | `key_luma8` | 8 | Grayscale to color (black → color) |
| 15 | LUMA8W | `key_luma8w` | 8 | Grayscale to color (white → color) |
| 16 | LUMA8X | `key_luma8x` | 8 | Grayscale to color (expanded range) |
| 17 | HSV8 | `key_hsv8` | 8 | 4-bit hue + 4-bit value (black → hue) |
| 18 | HSV8W | `key_hsv8w` | 8 | 4-bit hue + 4-bit value (white → hue) |
| 19 | HSV8X | `key_hsv8x` | 8 | 4-bit hue + 4-bit value (expanded range) |
| 20 | RGBI8 | `key_rgbi8` | 8 | 3-bit RGB + intensity (black → color) |
| 21 | RGBI8W | `key_rgbi8w` | 8 | 3-bit RGB + intensity (white → color) |
| 22 | RGBI8X | `key_rgbi8x` | 8 | 3-bit RGB + intensity (expanded range) |
| 23 | RGB8 | `key_rgb8` | 8 | 3:3:2 RGB (R3 G3 B2) |
| 24 | HSV16 | `key_hsv16` | 16 | 8-bit hue + 8-bit value (black → hue) |
| 25 | HSV16W | `key_hsv16w` | 16 | 8-bit hue + 8-bit value (white → hue) |
| 26 | HSV16X | `key_hsv16x` | 16 | 8-bit hue + 8-bit value (expanded range) |
| 27 | RGB16 | `key_rgb16` | 16 | 5:6:5 RGB (R5 G6 B5) |
| 28 | RGB24 | `key_rgb24` | 24 | 8:8:8 RGB (full color) — **the default** (`SetDefaults` 2889) |

### 6.2 TranslateColor Function (DebugDisplayUnit.pas:3090-3173)

**Purpose**: Convert pixel value from any color mode to RGB24

**Signature**:
```pascal
function TDebugDisplayForm.TranslateColor(p, mode: integer): integer;
```

**Implementation Details**:

#### LUT Modes (lines 3097-3104)
```pascal
key_lut1:  p := vLut[p and $01];        // 1 bit → 2 colors
key_lut2:  p := vLut[p and $03];        // 2 bits → 4 colors
key_lut4:  p := vLut[p and $0F];        // 4 bits → 16 colors
key_lut8:  p := vLut[p and $FF];        // 8 bits → 256 colors
```
- Simple lookup table indexing
- `vLut[]` contains 256 RGB24 values
- 🔴 **There is NO default palette.** `vLut[]` (declared 312) is written **only** by
  `KeyLutColors` (2806–2815: `for i := 0 to $FF do if not KeyColor(vLut[i]) then Break;`).
  Nothing in `SetDefaults` (2880–2917), `FormCreate` (591–645) or `BITMAP_Configure`
  (2372–2414) populates it. As a Delphi class field it is **zero-initialised**, so every entry
  reads `$000000`.
  ⇒ **A LUT mode used without `LUTCOLORS` renders entirely black** — and `GetBackground` for
  LUT modes returns `vLut[0]` (3184–3185), so the background is black too. (v55's prose claim
  of "default colors 0..7" is wrong; see §14.1, §17.4.)

#### LUMA8/RGBI8 Modes (lines 3105-3142)

**Color Selection**:
```pascal
if mode in [key_luma8, key_luma8w, key_luma8x] then
begin
  v := vColorTune and 7;        // User-specified color (0-7)
  p := p and $FF;               // 8-bit brightness
end
else
begin
  v := p shr 5 and 7;           // Upper 3 bits = RGB color
  p := p and $1F shl 3 or p and $1C shr 2;  // Lower 5 bits = intensity
end;
```

**Color Palette** (v = 0-7):
```
0: Orange (special case)
1: Blue    (bit 0 set)
2: Green   (bit 1 set)
3: Cyan    (bits 0,1 set)
4: Red     (bit 2 set)
5: Magenta (bits 0,2 set)
6: Yellow  (bits 1,2 set)
7: White   (bits 0,1,2 set)
```

**White/Expanded Modes**:
```pascal
w := (mode in [key_luma8w, key_rgbi8w]) or
     (mode in [key_luma8x, key_rgbi8x]) and (v <> 7) and (p >= $80);

if (mode in [key_luma8x, key_rgbi8x]) and (v <> 7) then
  if (p >= $80) then p := not p and $7F shl 1 else p := p shl 1;

if w then
  // Invert: white → color (high brightness = more color)
  p := (color_channels * p) xor $FFFFFF
else
  // Normal: black → color (high brightness = more color)
  p := color_channels * p
```

#### HSV Modes (lines 3143-3160)

**8-bit HSV** (key_hsv8, key_hsv8w, key_hsv8x):
```pascal
// Expand 4-bit hue and value to 8-bit
p := p and $F0 * $110 or p and $0F * $11;
```
- Upper 4 bits: Hue (0-15 → 0-255)
- Lower 4 bits: Value (0-15 → 0-255)

**16-bit HSV** (key_hsv16, key_hsv16w, key_hsv16x):
- Upper 8 bits: Hue (0-255)
- Lower 8 bits: Value (0-255)

**Conversion Process**:
```pascal
v := PolarColors[(p shr 8 + vColorTune) and $FF];  // Hue → RGB (from precomputed table)
p := p and $FF;                                     // Extract value

w := (mode in [key_hsv8w, key_hsv16w]) or
     (mode in [key_hsv8x, key_hsv16x]) and (p >= $80);

if mode in [key_hsv8x, key_hsv16x] then
  if (p >= $80) then p := p and $7F shl 1 xor $FE else p := p shl 1;  // Expand range

if w then v := v xor $FFFFFF;    // Invert for white modes

// Apply value to each RGB channel
p := (v shr 16 and $FF * p + $FF) shr 8 shl 16 or
     (v shr  8 and $FF * p + $FF) shr 8 shl  8 or
     (v shr  0 and $FF * p + $FF) shr 8 shl  0;

if w then p := p xor $FFFFFF;    // Invert back
```

#### RGB8 Mode (lines 3161-3164)
```pascal
key_rgb8:
  p := p and $E0 * $1236E and $FF0000 or    // R (3 bits → 8 bits)
       p and $1C *   $91C and $00FF00 or    // G (3 bits → 8 bits)
       p and $03 *    $55 and $0000FF;      // B (2 bits → 8 bits)
```
- 3:3:2 format (RRRGGGBB)
- Multipliers expand to full 8-bit range

#### RGB16 Mode (lines 3165-3168)
```pascal
key_rgb16:
  p := p and $F800 shl 8 or p and $E000 shl 3 or    // R (5 bits → 8 bits)
       p and $07E0 shl 5 or p and $0600 shr 1 or    // G (6 bits → 8 bits)
       p and $001F shl 3 or p and $001C shr 2;      // B (5 bits → 8 bits)
```
- 5:6:5 format (RRRRRGGGGGGBBBBB)
- Bit replication fills lower bits

#### RGB24 Mode (lines 3169-3170)
```pascal
key_rgb24:
  p := p and $00FFFFFF;    // Already 24-bit RGB
```
- No conversion needed
- Mask to 24 bits

### 6.3 PolarColors Table (SetPolarColors, DebugDisplayUnit.pas:3207-3228)

**Purpose**: Pre-computed HSV hue → RGB conversion

**Generation** (lines 3215-3227):
```pascal
for i := 0 to 255 do
begin
  for j := 0 to 2 do    // RGB channels
  begin
    k := i + tuning + j * 256 / 3;    // Hue offset for each channel
    if k >= 256 then k := k - 256;

    if      k < 256 * 2/6 then v[j] := 0
    else if k < 256 * 3/6 then v[j] := Round((k - 256 * 2/6) / (256 * 3/6 - 256 * 2/6) * 255)
    else if k < 256 * 5/6 then v[j] := 255
    else                       v[j] := Round((256 * 6/6 - k) / (256 * 6/6 - 256 * 5/6) * 255);
  end;
  PolarColors[i] := v[2] shl 16 or v[1] shl 8 or v[0];
end;
```

**Hue Wheel** (tuning = -7.2 for red at 0):
```
0:    Red
42:   Yellow
85:   Green
128:  Cyan
170:  Blue
213:  Magenta
255:  Red (wrap)
```

---

## 7. Trace Modes and Pixel Positioning

### 7.1 Trace Mode Encoding (DebugDisplayUnit.pas:2362-2370)

**Bit Layout**:
```
Bits 0-2: Scan pattern (0-7)
Bit 3:    Scroll enable (0=wrap, 1=scroll)
```

**8 Scan Patterns**:

The two advance columns are the **primary** (every pixel) and **secondary** (at the end of a
line/column) motions, exactly as Chip's comment block prints them (2363–2370). For the vertical
patterns 4–7 the primary motion is on **Y** and the secondary on **X** — so these columns are
*not* "the X motion" and "the Y motion". Confirmed in `StepTrace`: mode 4 (3024–3031) advances
`Inc(vPixelY)` per pixel and `Inc(vPixelX)` at the end of the column.

| Mode | Description | Start | Per-pixel advance | End-of-line/column advance | At the far edge |
|------|-------------|-------|-------------------|----------------------------|-----------------|
| 0 | Top line, L→R | (0,0) | X++ | Y++ | Wrap/Scroll down |
| 1 | Top line, R→L | (W-1,0) | X-- | Y++ | Wrap/Scroll down |
| 2 | Bottom line, L→R | (0,H-1) | X++ | Y-- | Wrap/Scroll up |
| 3 | Bottom line, R→L | (W-1,H-1) | X-- | Y-- | Wrap/Scroll up |
| 4 | Left line, T→B | (0,0) | Y++ | X++ | Wrap/Scroll right |
| 5 | Left line, B→T | (0,H-1) | Y-- | X++ | Wrap/Scroll right |
| 6 | Right line, T→B | (W-1,0) | Y++ | X-- | Wrap/Scroll left |
| 7 | Right line, B→T | (W-1,H-1) | Y-- | X-- | Wrap/Scroll left |

### 7.2 StepTrace Method (DebugDisplayUnit.pas:2982-3061)

**Purpose**: Advance pixel position after each pixel write

**Algorithm**:
```pascal
procedure TDebugDisplayForm.StepTrace;
var
  Scroll: boolean;
begin
  Scroll := vTrace and 8 <> 0;    // Bit 3 = scroll enable

  case vTrace and 7 of
    0:  // Top line, left-to-right
    begin
      if vPixelX <> vWidth - 1 then
        Inc(vPixelX)              // Continue current line
      else
      begin
        vPixelX := 0;             // Wrap to left edge
        if Scroll then
          ScrollBitmap(0, 1)      // Scroll down
        else if vPixelY <> vHeight - 1 then
          Inc(vPixelY)            // Next line down
        else
          vPixelY := 0;           // Wrap to top
      end;
    end;

    // ... similar logic for modes 1-7
  end;
end;
```

**Key Behaviors**:

1. **Horizontal Scan (modes 0-3)**:
   - Primary axis: X (advance every pixel)
   - Secondary axis: Y (advance at end of line)
   - Default rate: `vRate = vWidth`

2. **Vertical Scan (modes 4-7)**:
   - Primary axis: Y (advance every pixel)
   - Secondary axis: X (advance at end of column)
   - Default rate: `vRate = vHeight`

3. **Wrap vs. Scroll**:
   - **Wrap** (bit 3 = 0): Position wraps to opposite edge
   - **Scroll** (bit 3 = 1): Bitmap scrolls, new line filled with background

### 7.3 Common Trace Modes

**Mode 0 (top-left, L→R, no scroll)**:
- TV raster scan
- Sequential memory layout
- Use for: Video frames, image data

**Mode 8 (top-left, L→R, scroll down)**:
- Oscilloscope persistence display
- New data at top, old data scrolls down
- Use for: Waveform recording, chart recorder

**Mode 12 (left-top, T→B, scroll right)**:
- Vertical waveform display
- New data at left, old data scrolls right
- Use for: Strip chart, spectrogram

---

## 8. Pixel Rendering Modes

### 8.1 Normal Mode (vSparse = -1)

**Characteristics**:
- 1:1 pixel mapping (logical pixel = physical pixel)
- Direct scanline writes for maximum speed
- Client window size = bitmap size

**PlotPixel Implementation** (DebugDisplayUnit.pas:3433-3444):
```pascal
procedure TDebugDisplayForm.PlotPixel(p: integer);
begin
  p := TranslateColor(p, vColorMode);    // Convert to RGB24
  line := BitmapLine[vPixelY];           // Get scanline pointer (fast!)
  v := vPixelX * 3;                      // 3 bytes per pixel (BGR)
  line[v+0] := p shr 0;                  // Blue
  line[v+1] := p shr 8;                  // Green
  line[v+2] := p shr 16;                 // Red
end;
```

**Performance**: ~10 million pixels/second (direct memory write)

### 8.2 Sparse Mode (vSparse ≠ -1)

**Activation** — all three required (`SetSize` 2938; see §3.2):
1. a `SPARSE` colour, **and**
2. `DOTSIZE` x ≥ 4, **and**
3. `DOTSIZE` y ≥ 4.

Otherwise `vSparse := -1` (2947) and the window is a **normal** window. There is no warning.

**Characteristics**:
- Magnified pixel display (logical pixel = `vDotSize × vDotSizeY` **physical** pixels)
- The bitmap itself is allocated at physical size (2940–2943), so the cells are drawn at real
  device resolution and `StretchDraw` is a 1:1 blit (§21.2)
- Client window size = `vWidth·vDotSize × vHeight·vDotSizeY`

**Configuration**:
```
size 64 64 dotsize 8 8 sparse $404040
```
- Creates 64×64 logical bitmap
- Each pixel rendered as an 8×8 physical cell
- Client window (and bitmap): 512×512 pixels
- Sparse/field color: dark gray ($404040)

**Rendering** (BITMAP_Update, lines 2470-2478):
```pascal
// Center of the cell (physical coords)
x := vPixelX * vDotSize + vDotSize shr 1;
y := vPixelY * vDotSizeY + vDotSizeY shr 1;

// Call 1 — SOLID FILL of the whole cell in the sparse color (xro=yro=0 ⇒ rectangle; thick=0 ⇒ solid)
SmoothShape(x, y, vDotSize, vDotSizeY, 0, 0, 0, vSparse, 255);

// Call 2 — the data pixel: a ROUND DOT at 3/4 cell size (radii clamped to max ⇒ fully rounded)
SmoothShape(x, y,
            vDotSize - vDotSize shr 2,
            vDotSizeY - vDotSizeY shr 2,
            vDotSize, vDotSizeY,
            0, TranslateColor(UnPack(v), vColorMode), 255);
```

**Visual Effect** — round dots on a solid sparse-coloured field (v55: "large **round** pixels"):
```
░░●●●░░░░░░░░░░░●●●░░      ░ = vSparse color  (the solid cell fill, showing
░●●●●●░░░░░░░░░●●●●●░           through around and between the dots)
░░●●●░░░░░░░░░░░●●●░░      ● = data color     (round dot, ~3/4 of the cell)
░░░░░░░░●●●░░░░░░░░░░
░░░░░░░●●●●●░░░░░░░░░      NOT a drawn grid: there are no grid lines in the
░░░░░░░░●●●░░░░░░░░░░      code. The "grid" is the residual sparse fill left
░░●●●░░░░░░░░░░░●●●░░      visible where the round dot does not cover the
░●●●●●░░░░░░░░░●●●●●░      square cell — chiefly the four corners.
░░●●●░░░░░░░░░░░●●●░░
```
- **Cell fill**: `vSparse` colour, **solid, whole cell** (call 1 — *not* a hollow border)
- **Dot**: data colour, **round**, ~75 % of the cell (call 2)
- **No skip rule**: every pixel is plotted, including ones whose value equals the sparse colour

> **NEEDS-HARDWARE:** the exact rendered footprint of a `DOTSIZE` cell (and of the anti-aliased
> dot inside it) has never been measured on real output. The geometry above is *code fact*; the
> resulting pixel coverage — where the AA envelope lands — is not asserted here.

**Use Cases**:
- Retro pixel art (magnified view)
- LED matrix simulation
- Low-resolution sensor displays
- Educational visualization

### 8.3 Display Update Control

**Automatic Update** (default):
```pascal
if RateCycle and not vUpdate then BitmapToCanvas(0);
```
- Display updates every `vRate` pixels
- Trade-off: Frequent updates = slow, Infrequent = choppy

**Manual Update**:
```pascal
// Configuration
update

// In code
if not vUpdate then BitmapToCanvas(0);    // Suppressed
```
- Requires explicit `UPDATE` command to refresh display
- Allows batch pixel writes without flicker
- Example:
  ```
  BITMAP `0 update 1000,2000,3000,4000 update
  ```

**Rate Cycle Timing**:
```pascal
function TDebugDisplayForm.RateCycle: boolean;
begin
  Inc(vRateCount);
  if vRateCount = vRate then
  begin
    vRateCount := 0;
    Result := True;
  end
  else Result := False;
end;
```

---

## 9. Scrolling System

### 9.1 ScrollBitmap Method (DebugDisplayUnit.pas:3446-3481)

**Purpose**: Shift bitmap content and fill vacated area with background

**Signature**:
```pascal
procedure TDebugDisplayForm.ScrollBitmap(x, y: integer);
```

**Parameters**:
- `x`: Horizontal scroll (-vWidth..+vWidth)
  - Positive = scroll right (content moves right)
  - Negative = scroll left (content moves left)
- `y`: Vertical scroll (-vHeight..+vHeight)
  - Positive = scroll down (content moves down)
  - Negative = scroll up (content moves up)

**Implementation**:
```pascal
// Calculate pixel multiplier for sparse mode
if vSparse = -1 then
begin
  xm := 1;        // Normal mode: 1:1
  ym := 1;
end
else
begin
  xm := vDotSize;   // Sparse mode: scale factor
  ym := vDotSizeY;
end;

// Define source and destination rectangles
src := Rect(0, 0, vWidth * xm, vHeight * ym);
dst := Rect(x * xm, y * ym, (vWidth + x) * xm, (vHeight + y) * ym);

// Copy bitmap to shifted position
Bitmap[0].Canvas.CopyRect(dst, Bitmap[0].Canvas, src);

// Fill vacated area with background color
Bitmap[0].Canvas.Brush.Color := WinRGB(GetBackground);

if x <> 0 then
begin
  if x < 0 then
    dst := Rect((vWidth + x) * xm, 0, vWidth * xm, vHeight * ym)     // 3468 RIGHT strip (vacated by a LEFTWARD scroll)
  else
    dst := Rect(0, 0, x * xm, vHeight * ym);                         // 3470 LEFT strip  (vacated by a RIGHTWARD scroll)
  Bitmap[0].Canvas.FillRect(dst);
end;

if y <> 0 then
begin
  if y < 0 then
    dst := Rect(0, (vHeight + y) * ym, vWidth * xm, vHeight * ym)    // 3476 BOTTOM strip (vacated by an UPWARD scroll)
  else
    dst := Rect(0, 0, vWidth * xm, y * ym);                          // 3478 TOP strip    (vacated by a DOWNWARD scroll)
  Bitmap[0].Canvas.FillRect(dst);
end;
```

**The fill strip is always on the side the content moved *away from*.** `x < 0` moves the content
left, so the vacated band — the one filled with `GetBackground` — is at the **right** edge
(`(vWidth+x)*xm … vWidth*xm`, 3468), and `x > 0` vacates the **left** edge (`0 … x*xm`, 3470).

**Automatic Scrolling** (from StepTrace):
```pascal
if Scroll then ScrollBitmap(dx, dy)    // dx, dy = -1, 0, or 1
```
- Mode 0/1 (top line): ScrollBitmap(0, 1) — scroll down
- Mode 2/3 (bottom line): ScrollBitmap(0, -1) — scroll up
- Mode 4/5 (left line): ScrollBitmap(1, 0) — scroll right
- Mode 6/7 (right line): ScrollBitmap(-1, 0) — scroll left

**Manual Scrolling** (from BITMAP_Update):
```pascal
key_scroll:
  if KeyValWithin(x, -vWidth, vWidth) then
    if KeyValWithin(y, -vHeight, vHeight) then
      ScrollBitmap(x, y);
```

---

## 10. Display Update Messages and Commands

### 10.1 Command Structure
[Identical to FFT - see FFT documentation]

### 10.2 BITMAP Command Examples

#### Create BITMAP Window
```
Serial: 0xFF 0x00 "BITMAP `My Display size 320 240 luma8 orange" 0x0D

Parsed:
[0] type=ele_dis, value=1                (1 = create new)
[1] type=ele_num, value=7                (display type: dis_bitmap)
[2] type=ele_str, value="My Display"     (title)
[3] type=ele_key, value=key_size
[4] type=ele_num, value=320              (width)
[5] type=ele_num, value=240              (height)
[6] type=ele_key, value=key_luma8        (color mode)
[7] type=ele_key, value=key_orange       (color tune)
[8] type=ele_end
```

#### Update with Pixel Data
```
Serial: 0xFF 0x00 "BITMAP `0 100,120,140,160,180,200" 0x0D

Parsed:
[0] type=ele_dis, value=2                (2 = update existing)
[1] type=ele_num, value=0                (display index)
[2] type=ele_num, value=100              (pixel data)
[3] type=ele_num, value=120
[4] type=ele_num, value=140
[5] type=ele_num, value=160
[6] type=ele_num, value=180
[7] type=ele_num, value=200
[8] type=ele_end
```

#### Change Trace Mode Mid-Stream
```
Serial: 0xFF 0x00 "BITMAP `0 trace 8 clear" 0x0D

Effect: Switch to mode 8 (top-left, L→R, scroll down), then clear
```

#### Sparse Pixel Display
```
Serial: 0xFF 0x00 "BITMAP `LED Matrix size 8 8 dotsize 16 sparse $202020 lut4" 0x0D

Creates:
- 8×8 logical display
- 16×16 pixel per logical pixel
- Client window: 128×128 pixels
- Grid color: dark gray
- 4-bit color palette (16 colors)
```

#### Packed Data Example
```
Serial: 0xFF 0x00 "BITMAP `0 longs_8bit rgb8 100,200,300,400" 0x0D

Processing:
- longs_8bit: 4 samples per long
- Each long unpacks to 4 pixels
- Total pixels plotted: 4×4 = 16
```

### 10.3 Configuration Keywords

[See section 3.2 for complete list]

---

## 11. Drawing Primitives — **PLOT's, NOT BITMAP's** (reference only)

### 11.1 Overview

> **🔴 These are PLOT directives. BITMAP does not accept any of them.**
> Every keyword in this section (`LINE`, `DOT`, `CIRCLE`, `OVAL`, `BOX`, `OBOX`, `TEXT`,
> `TEXTSTYLE`, `LAYER`, `CROP`, `SPRITEDEF`, `SPRITE`) appears **only** in the `PLOT_Update`
> case statement (1930–2155). None of them appears in `BITMAP_Update`'s case statement
> (2424–2457), so sending one to a BITMAP window is a no-op that falls through the `case` —
> and, being a key rather than a number, it does not even plot a pixel.

BITMAP shares with PLOT the **internal renderers only**: `SmoothShape` (3590–3743) — which BITMAP
calls **solely** from its sparse-pixel path (2472–2478) — plus `TranslateColor`, `SmoothFillSetup`
and the bitmap/scanline machinery. Sharing a renderer is not sharing a directive.

This section is retained purely as a cross-reference for readers comparing the two windows. It
is **not** a BITMAP feature list.

### 11.2 PLOT's primitives (for reference — unavailable in BITMAP)

#### Geometric Shapes (DebugDisplayUnit.pas:1980-2035)

**LINE** (lines 1980-2011):
```pascal
key_line:  // LINE x y {linesize {opacity}}
  SmoothLine(x1, y1, x2, y2, linesize, color, opacity);
```

**DOT** (lines 1965-1979):
```pascal
key_dot:   // DOT {linesize {opacity}}
  SmoothDot(x, y, radius, color, opacity);
```

**CIRCLE** (lines 2012-2035) — the parameter is a **WIDTH (diameter)**, *not* a radius:
```pascal
key_circle,                                   // CIRCLE width {linesize {opacity}}   (Chip's own comment, 2012)
  ...
  key_circle: SmoothShape(t1, t2, t3, t3, t3 shr 1, t3 shr 1, t7, vPlotColor, t8);   // 2031
  //                              ^^^^^^  ^^^^^^^^^^^^^^^^^^
  //                              size = width, width      radii = width shr 1
```
`t3` is passed as the **size** on both axes and halved (`t3 shr 1`) to obtain the corner radii —
so `CIRCLE 20` draws a circle **20 px across**, not 40. (Treating the argument as a radius would
double the circle. The [Directive Matrix](../DEBUG-WINDOW-DIRECTIVE-MATRIX.md) §7.3 has this right.)

**OVAL** (lines 2012-2035):
```pascal
key_oval:  // OVAL width height {linesize {opacity}}
  SmoothShape(x, y, width, height, width/2, height/2, linesize, color, opacity);
```

**BOX** (lines 2012-2035):
```pascal
key_box:   // BOX width height {linesize {opacity}}
  SmoothShape(x, y, width, height, 0, 0, linesize, color, opacity);
```

**OBOX** (rounded box, lines 2012-2035):
```pascal
key_obox:  // OBOX width height xradius yradius {linesize {opacity}}
  SmoothShape(x, y, width, height, xradius, yradius, linesize, color, opacity);
```

#### Text Rendering (DebugDisplayUnit.pas:2043-2055)

**TEXT** (lines 2043-2055):
```pascal
key_text:  // TEXT {size {style {angle}}} 'string'
  AngleTextOut(x, y, string, style, angle);
```

**Styles** (bitwise encoding — `AngleTextOut`, 3483–3520):
```
Bits 0-1: Font WEIGHT (4 levels, not a "bold" flag)                          (3485, 3494)
  0: 100 (thin)   1: 400 (normal)   2: 700 (bold)   3: 900 (black)
  ⇒ $01 = normal (DefaultTextStyle); $02 = BOLD
Bit  2:   Italic         (lfItalic := style and $04 shr 2)                    (3495)
Bit  3:   Underline      (lfUnderline := style and $08 shr 3)                 (3496)
          — there is NO strikeout bit anywhere in the source
Bits 4-5: Horizontal justify                                                 (3502-3506)
  0/1: centred on the anchor        (tx := -w/2)
  2:   text sits to the RIGHT of the anchor (anchor = text's LEFT edge)   (tx := 0)
  3:   text sits to the LEFT of the anchor  (anchor = text's RIGHT edge)  (tx := -w)
Bits 6-7: Vertical justify                                                   (3507-3511)
  0/1: centred on the anchor        (ty := h/2)
  2:   text sits ABOVE the anchor (anchor = text's BOTTOM edge)           (ty := h)
  3:   text sits BELOW the anchor (anchor = text's TOP edge)              (ty := 0)
```
Geometry: output is `TextOut(x + rx, y - ry)` (3516) and screen Y grows **down**, so `ty := h`
(case 2) lifts the whole cell above the anchor and `ty := 0` (case 3) drops it below.
The Pascal `case` arms are **bare** — Chip attached no names to these values; any justify
*name* is a downstream convention, so both halves are always stated here (where the ink lands
**and** which edge the anchor is).

#### Bitmap Layers (DebugDisplayUnit.pas:2056-2089)

**LAYER** (lines 2056-2062):
```pascal
key_layer:  // LAYER layer 'filename.bmp'
  PlotBitmap[layer - 1].LoadFromFile(filename);
```
- Loads BMP file into layer 1-8
- Layers persist across updates

**CROP** (lines 2063-2089):
```pascal
key_crop:   // CROP layer {left top width height {x y}}
            // CROP layer AUTO x y
  Bitmap[0].Canvas.CopyRect(dst, PlotBitmap[layer-1].Canvas, src);
```
- Copies rectangular region from layer to main bitmap
- AUTO mode: copies entire layer

### 11.3 SmoothShape Method (DebugDisplayUnit.pas:3590-3743)

> Unlike the rest of §11, `SmoothShape` **is** on BITMAP's path — it is what draws the sparse
> cells (2472–2478). It is documented here because PLOT's primitives all funnel into it too.

**Purpose**: Draw anti-aliased rectangle/oval with optional frame

**Signature**:
```pascal
procedure TDebugDisplayForm.SmoothShape(xc, yc,           // Center position
                                         xs, ys,           // Size (width, height)
                                         xro, yro,         // Corner radii (0=rectangle)
                                         thick,            // Frame thickness (0=solid)
                                         color: integer;   // RGB color
                                         opacity: byte);   // Alpha (0-255)
```

**Parameters**:
- `xc, yc`: Center coordinates
- `xs, ys`: Outer dimensions
- `xro, yro`: Corner radii (0 = sharp corners)
- `thick`: Frame thickness (0 = filled)
- `color`: RGB24 color
- `opacity`: Alpha blend factor

**Rendering Algorithm**:

1. **Setup** (lines 3605-3618):
   - Ignore bad input (3606–3612): any `xs`/`ys` outside 1..`SmoothFillMax`, negative `thick`, or
     a centre far off-bitmap causes a silent `Exit`
   - Call `SmoothFillSetup(xs, color)` (3614) to prepare the color buffer
   - `solid := (thick = 0) or (thick shl 1 >= xs) or (thick shl 1 >= ys);`  (3616)
   - `rectangle := (xro = 0) or (yro = 0);`                                  (3617)
   ⇒ **`thick = 0` means SOLID FILL, not "no frame"**, and **either radius = 0 means RECTANGLE**.
   Both are what BITMAP's sparse call 1 (`xro=yro=0, thick=0`) relies on.

2. **Rectangle Fast Path** (lines 3618-3636):
   ```pascal
   if rectangle then
   begin
     if solid then
       SmoothRect(xl, yt, xs, ys, opacity)         // 3626 — single filled rectangle
     else
     begin                                         // 3628-3634 — inward frame, 4 edges
       SmoothRect(xl,         yt,         xs,    thick, opacity);    // top
       SmoothRect(xl,         yb - thick, xs,    thick, opacity);    // bottom
       SmoothRect(xl,         yt + thick, thick, yf,    opacity);    // left
       SmoothRect(xr - thick, yt + thick, thick, yf,    opacity);    // right
     end;
     Exit;                                         // 3635
   end;
   ```
   The stroke is drawn **inward** from the outer box — it does not straddle the boundary by ±t/2.

3. **Rounded / Oval Rendering** (lines 3637-3743):
   - **Clamp the corner radii first** (3638–3639):
     `if (xro shl 1 > xs) then xro := xs shr 1;  if (yro shl 1 > ys) then yro := ys shr 1;`
     — this is what turns BITMAP's sparse call 2 (radii `vDotSize`/`vDotSizeY`, larger than half
     the 3/4-size shape) into a **fully rounded dot**.
   - Compute quarter-ellipse lookup tables for the corners
   - Draw the flat sections (top/bottom/left/right strips)
   - Draw the 4 rounded corners with 4-way symmetric plotting + gamma blending
   (There is **no signed-distance field** here — it is LUTs plus symmetry.)

**Anti-Aliasing**: edge coverage comes from the **quarter-ellipse lookup tables** (`xo_lut`/`yo_lut`
/`xi_lut`/`yi_lut`, declared 3595–3598) combined with the `xo_above`/`xo_below`… boundary flags and
gamma blending — plotted 4-way symmetrically. It is **not** a signed-distance field and there is no
`Abs(distance_to_edge)` term anywhere in the procedure; do not model it as one.

---

## 12. Sprite System

> **Note**: `SPRITEDEF` and `SPRITE` directives are processed only in `PLOT_Update`, not in `BITMAP_Update`. BITMAP shares the sprite data arrays (see §17.3), but the BITMAP window does **not** accept sprite commands. This section documents the shared data structures and the PLOT-side command handling for reference.

### 12.1 Sprite Data Structures (DebugDisplayUnit.pas:397-400)

```pascal
SpritePixels  : array[0..SpriteMax * SpriteMaxX * SpriteMaxY - 1] of byte
SpriteColors  : array[0..SpriteMax * 256 - 1] of integer
SpriteSizeX   : array[0..SpriteMax - 1] of byte
SpriteSizeY   : array[0..SpriteMax - 1] of byte

SpriteMax     = 256      // Maximum sprite count
SpriteMaxX    = 32       // Maximum sprite width
SpriteMaxY    = 32       // Maximum sprite height
```

**Memory Layout**:
```
Sprite 0: SpritePixels[0..1023]      (32×32 = 1024 pixels)
          SpriteColors[0..255]       (256-entry palette)
          SpriteSizeX[0], SpriteSizeY[0]

Sprite 1: SpritePixels[1024..2047]
          SpriteColors[256..511]
          SpriteSizeX[1], SpriteSizeY[1]

... (total 256 sprites)
```

### 12.2 SPRITEDEF Command (DebugDisplayUnit.pas:2090-2101)

**Syntax**:
```
SPRITEDEF id xsize ysize pixels... colors...
```

**Parameters**:
- `id`: Sprite index (0-255)
- `xsize`: Width (1-32)
- `ysize`: Height (1-32)
- `pixels`: xsize×ysize pixel values (0-255)
- `colors`: 256 RGB24 palette entries

**Processing**:
```pascal
key_spritedef:
begin
  if not KeyValWithin(t1, 0, SpriteMax - 1) then Break;     // id
  if not KeyValWithin(t2, 1, SpriteMaxX) then Break;        // xsize
  if not KeyValWithin(t3, 1, SpriteMaxY) then Break;        // ysize

  SpriteSizeX[t1] := t2;
  SpriteSizeY[t1] := t3;

  for i := 0 to t2 * t3 - 1 do
    if not KeyVal(t4) then Break
    else SpritePixels[t1 * SpriteMaxX * SpriteMaxY + i] := t4;

  for i := 0 to 255 do
    if not KeyVal(SpriteColors[t1 * 256 + i]) then Break;
end;
```

**Example**:
```
SPRITEDEF 0 8 8
  0,1,2,3,4,5,6,7,
  8,9,10,11,12,13,14,15,
  ... (64 total pixels)
  $000000,$110000,$220000,... (256 colors)
```

### 12.3 SPRITE Command (DebugDisplayUnit.pas:2102-2134)

**Syntax**:
```
SPRITE id {orientation {scale {opacity}}}
```

**Parameters**:
- `id`: Sprite index (0-255)
- `orientation`: Rotation/flip (0-7, default 0)
- `scale`: Size multiplier (1-64, default 1)
- `opacity`: Alpha (0-255, default 255)

**Orientation Modes**:
```
0: Normal          (no flip)
1: Flip X          (mirror horizontal)
2: Flip Y          (mirror vertical)
3: Flip X+Y        (rotate 180°)
4: Transpose       (swap X/Y, rotate 90° CCW)
5: Transpose + FlipY
6: Transpose + FlipX
7: Transpose + FlipX+Y
```

**Rendering** (lines 2117-2133):
```pascal
for y := 1 to SpriteSizeY[id] do
  for x := 1 to SpriteSizeX[id] do
  begin
    c := SpriteColors[id * 256 + SpritePixels[offset]];    // Lookup color
    opa := ((c shr 24 and $FF) * opacity + $FF) shr 8;     // Alpha from color + parameter

    if opa <> 0 then
      case orientation of
        0: SmoothShape(px + (x-1)*scale, py + (y-1)*scale, scale, scale, 0, 0, 0, c, opa);
        1: SmoothShape(px + (w-x)*scale, py + (y-1)*scale, scale, scale, 0, 0, 0, c, opa);  // FlipX
        2: SmoothShape(px + (x-1)*scale, py + (h-y)*scale, scale, scale, 0, 0, 0, c, opa);  // FlipY
        3: SmoothShape(px + (w-x)*scale, py + (h-y)*scale, scale, scale, 0, 0, 0, c, opa);  // FlipX+Y
        4: SmoothShape(px + (y-1)*scale, py + (x-1)*scale, scale, scale, 0, 0, 0, c, opa);  // Transpose
        5: SmoothShape(px + (y-1)*scale, py + (w-x)*scale, scale, scale, 0, 0, 0, c, opa);
        6: SmoothShape(px + (h-y)*scale, py + (x-1)*scale, scale, scale, 0, 0, 0, c, opa);
        7: SmoothShape(px + (h-y)*scale, py + (w-x)*scale, scale, scale, 0, 0, 0, c, opa);
      end;
  end;
```

**Color Alpha** (bits 24-31 of color):
```pascal
// In SPRITEDEF colors:
color = $80RRGGBB    // Alpha = 0x80 (50% transparent)
color = $FFRRGGBB    // Alpha = 0xFF (opaque)
color = $00RRGGBB    // Alpha = 0x00 (invisible)
```

---

## 13. Performance Characteristics

### 13.1 Pixel Throughput

**Normal Mode (PlotPixel)**:
- **Direct scanline write**: ~10 million pixels/second
- Memory bandwidth limited (3 bytes/pixel write)
- No overhead (no function calls after TranslateColor)

**Sparse Mode (SmoothShape)**:
- **Anti-aliased rendering**: ~100,000 pixels/second
- Each logical pixel → 2 SmoothShape calls + blending
- CPU-intensive (floating-point, alpha blending)

**Comparison**:
```
320×240 bitmap (76,800 pixels):
  Normal mode:  ~7.7 ms per frame  (130 FPS max)
  Sparse mode:  ~768 ms per frame  (1.3 FPS max)
```

### 13.2 Memory Usage

**Bitmap Storage** — `pf24bit`, **3 bytes/pixel** (BGR, no alpha):
```pascal
Bitmap[0]: vWidth × vHeight × 3 bytes      // normal mode (SetSize 2948-2951)
Bitmap[1]: vWidth × vHeight × 3 bytes

Example (640×480):
  Bitmap[0]: 921,600 bytes (900 KB)
  Bitmap[1]: 921,600 bytes (900 KB)
  Total:     1,843,200 bytes (1.8 MB)
```
⚠️ **In sparse mode the bitmaps are allocated at PHYSICAL size** (`SetSize` 2940–2943):
`vWidth·vDotSize × vHeight·vDotSizeY × 3` bytes each — memory grows with the *square* of the dot
size. `SIZE 64 64 DOTSIZE 8 SPARSE $404040` ⇒ 512×512×3 = 786,432 bytes **per** bitmap (1.5 MB
for the pair), not the 12 KB the logical size would suggest.

**Sprite Storage**:
```pascal
SpritePixels: 256 sprites × 32×32 pixels = 262,144 bytes (256 KB)
SpriteColors: 256 sprites × 256 colors × 4 bytes = 262,144 bytes (256 KB)
SpriteSizeX:  256 bytes
SpriteSizeY:  256 bytes
Total:        ~524 KB
```

**Scanline Pointers**:
```pascal
BitmapLine: 2048 pointers × 4/8 bytes = 8-16 KB
```

**Total Memory** (640×480 + sprites): ~2.4 MB

### 13.3 Serial Bandwidth

**Uncompressed** (RGB24):
```
320×240 × 3 bytes × 30 FPS = 6.9 MB/sec
Serial port (2 Mbaud): ~200 KB/sec
Conclusion: Cannot stream full-color video
```

**Compressed** (LUT4):
```
320×240 × 0.5 bytes × 30 FPS = 1.15 MB/sec
Still exceeds serial bandwidth
```

**Practical Frame Rates**:
```
RGB24 (3 bytes/pixel):
  64×64:   3 KB/frame  → 66 FPS
  128×128: 49 KB/frame → 4 FPS
  320×240: 225 KB/frame → 0.9 FPS

LUT4 (0.5 bytes/pixel):
  64×64:   2 KB/frame  → 100 FPS (achievable)
  128×128: 8 KB/frame  → 25 FPS
  320×240: 38 KB/frame → 5 FPS
```

**Recommendation**: Use LUT/LUMA modes for higher frame rates

---

## 14. Key Behaviors and Edge Cases

### 14.1 Color Mode Switching

**Runtime Change**:
```pascal
key_lut1..key_rgb24:
  KeyColorMode;    // Immediate effect on next pixel
```

**Effect**:
- All subsequent pixels interpreted in new mode
- Existing pixels unchanged (already rendered)
- LUT colors preserved across mode changes

**Example**:
```
BITMAP `0 rgb24 $FF0000,$00FF00,$0000FF lut4 0,1,2,3
```
- First 3 pixels: RGB24 (red, green, blue)
- Next 4 pixels: LUT4 (indices 0,1,2,3 → **black `$000000`** — `vLut[]` is never default-populated; it is Delphi zero-initialized until `LUTCOLORS`, so it reads black, not the v55-text's claimed "0–7 default colors")

### 14.2 Trace Mode Switching

**Runtime Change**:
```pascal
key_trace:
  if NextNum then SetTrace(val, True);
```

**Effect**:
- Pixel position reset to new starting corner
- Scan direction changed
- `vRate` adjusted for new pattern (if ModifyRate=True)

**Example**:
```
BITMAP `0 trace 0 100,200,300 trace 12 400,500,600
```
- Pixels 100,200,300: Trace 0 (top-left, L→R)
- Position reset to (0,0)
- Pixels 400,500,600: Trace 12 (left-top, T→B, scroll right)

### 14.3 Buffer Wrapping

**Automatic Wrapping** (no scroll):
```pascal
if vPixelY <> vHeight - 1 then
  Inc(vPixelY)
else
  vPixelY := 0;    // Wrap to top
```

**Overflow Protection**:
- Pixel position never exceeds bitmap bounds
- Wrap-around prevents crashes
- Old data overwritten (circular buffer behavior)

### 14.4 Packed Data Alignment

**Issue**: Packed data may not align with display dimensions

**Example**:
```
size 100 100 longs_8bit
```
- Each long = 4 pixels
- 100×100 = 10,000 pixels
- 10,000 ÷ 4 = 2,500 longs (exact)
- No issue

**Misaligned Example**:
```
size 100 100 longs_1bit
```
- Each long = 32 pixels
- 10,000 pixels ÷ 32 = 312.5 longs
- Last long has 16 unused bits
- StepTrace continues to next line mid-long

**Recommendation**: Choose bitmap size divisible by pack count

### 14.5 Sparse Mode Scaling

**Integer Scaling Only** (`BITMAP_Configure` 2387–2392):
```pascal
key_dotsize:
  if KeyValWithin(vDotSize, 1, 256) then
  begin
    vDotSizeY := vDotSize;               // y defaults to x
    KeyValWithin(vDotSizeY, 1, 256);     // optional explicit y
  end;
```
- Only integer scales supported (1, 2, 3, ..., 256); `KeyValWithin` **assigns and clamps** —
  `DOTSIZE 999` yields **256**, it is not rejected
- Fractional scales not available

**⚠️ `DOTSIZE` alone does NOT give you sparse mode** — and `DOTSIZE 1..3` *cannot*, even with a
`SPARSE` colour, because `SetSize`'s gate (2938) requires **≥ 4 on both axes** and otherwise sets
`vSparse := -1` (2947). With `DOTSIZE` > 1 and sparse off you still get a magnified window — but
by `StretchDraw` of a logical-size bitmap (hard blocks), not by drawn cells (§21.2).

**Client Window Size** — set **unconditionally** for BITMAP/SPECTRO/PLOT (2936–2937):
```pascal
ClientWidth  := vWidth * vDotSize;
ClientHeight := vHeight * vDotSizeY;
```
- Can create very large windows (2048 × 256 = 524,288 px wide!)
- May exceed screen dimensions
- In **sparse** mode the *bitmaps* are this size too (2940–2943), so memory scales with the
  square of the dot size: `vWidth·vDotSize × vHeight·vDotSizeY × 3 bytes`, ×2 buffers

**Recommendation**: Keep `vDotSize × max(vWidth, vHeight) < 2048` — `SmoothShape` also silently
ignores any cell whose size exceeds `SmoothFillMax` = 2048 (3608–3609).

---

## 15. Integration Points

### 15.1 Serial Protocol
[Identical to FFT - see FFT documentation]

### 15.2 P2 Global Variables
[Identical to FFT - see FFT documentation]

### 15.3 Form Lifecycle
[Similar to FFT - see FFT documentation]

### 15.4 Shared Infrastructure

**With SPECTRO** (dis_spectro = 4) — shares the *mechanisms*, **not** the accepted ranges:
- Shares `TranslateColor` / `GetBackground`, the `vDotSize`/`vDotSizeY` scaling mechanism, and
  `SetTrace` / `StepTrace` / `ScrollBitmap` / `BitmapToCanvas`.
- ❌ **NOT "the same color modes."** SPECTRO's config parser accepts only **six** of the nineteen
  — `key_luma8..key_luma8x, key_hsv16..key_hsv16x: KeyColorMode;` (**1767**), i.e.
  `LUMA8 / LUMA8W / LUMA8X / HSV16 / HSV16W / HSV16X` — whereas BITMAP accepts the whole
  `key_lut1..key_rgb24` range (**2395**). No LUT, no RGB, no HSV8, no RGBI on SPECTRO.
- ❌ **NOT the same `DOTSIZE` range.** SPECTRO clamps to **1..16** (1762–1765); BITMAP to
  **1..256** (2388–2391).
- Different trace behavior (SPECTRO always scrolls)

**With PLOT** (dis_plot = 5):
- Shares the **internal renderers** (`SmoothShape`, `SmoothLine`, `SmoothDot`, `AngleTextOut`)
  and the bitmap/scanline machinery — but BITMAP calls `SmoothShape` **only** from its
  sparse-pixel path (2472–2478).
- Shares the sprite **arrays** (they are per-window instance fields), but **not** the sprite
  directives — `SPRITEDEF`/`SPRITE` exist only in `PLOT_Update`.
- ❌ **BITMAP accepts NONE of PLOT's drawing directives** (`LINE`, `CIRCLE`, `TEXT`, …). See §11.
- PLOT has a coordinate system (origin/offset/polar), BITMAP does not.

**With TERM** (dis_term = 6):
- Different rendering (text-based vs. pixel-based)
- No shared infrastructure

---

## 16. Advanced Features

### 16.1 Manual Pixel Positioning

**SET Command** (DebugDisplayUnit.pas:2433-2438):
```pascal
key_set:
begin
  vTrace := vTrace and 7;     // Disable scrolling
  if KeyValWithin(vPixelX, 0, vWidth - 1) then
    KeyValWithin(vPixelY, 0, vHeight - 1);
end;
```

**Example**:
```
BITMAP `0 set 50 75 $FF0000 set 100 150 $00FF00
```
- Pixel at (50,75) = red
- Pixel at (100,150) = green
- No trace advancement

**Use Case**: Random-access pixel writes (not streaming)

### 16.2 Bitmap Scrolling

**SCROLL Command** (DebugDisplayUnit.pas:2439-2442):
```pascal
key_scroll:
  if KeyValWithin(x, -vWidth, vWidth) then
    if KeyValWithin(y, -vHeight, vHeight) then
      ScrollBitmap(x, y);
```

**Example**:
```
BITMAP `0 scroll 10 0    // Scroll right 10 pixels
BITMAP `0 scroll 0 -5    // Scroll up 5 pixels
```

**Use Cases**:
- Pan image
- Adjust waveform position
- Implement custom scroll patterns

### 16.3 LUT Animation

**Dynamic Palette**:
```
BITMAP `0 lut8 lutcolors $000000,$110000,...,$FF0000    // Red gradient
... (draw image using LUT8)
BITMAP `0 lutcolors $000000,$001100,...,$00FF00         // Change to green gradient
```

**Effect**:
- Image pixels unchanged
- Colors reinterpreted via new palette
- Instant color shift (no redraw needed)

**Use Cases**:
- Palette cycling effects
- False-color mapping
- Night mode toggle

### 16.4 Multi-Resolution Display

**Approach 1: Sparse scaling**
```
BITMAP `Low Res size 64 64 dotsize 4 sparse $000000
```
- 64×64 logical pixels
- 256×256 physical display
- Grid borders for clarity

**Approach 2: Normal + manual positioning**
```
BITMAP `High Res size 256 256
... draw at 1:1
SET 64 64  // Jump to sub-region
... draw detailed area
```

---

## 17. Limitations and Constraints

### 17.1 Bitmap Size

**Constraint**:
```pascal
bitmap_wmin = 1
bitmap_wmax = SmoothFillMax = 2048
bitmap_hmin = 1
bitmap_hmax = SmoothFillMax = 2048
```

**Maximum**: 2048×2048 = 4,194,304 pixels = 12 MB (×2 for double buffer = 24 MB)

**Practical Limit**: Memory allocation fails above ~1024×1024 on some systems

### 17.2 Sparse Mode Limits

**Constraint**:
```pascal
key_dotsize:
  if KeyValWithin(vDotSize, 1, 256) then ...      // 2388, clamped (not rejected)
```

**Minimum for sparse to work at all**: `DOTSIZE` **≥ 4 on both axes** *and* a `SPARSE` colour
(`SetSize` 2938). Below that, `vSparse := -1` (2947) — sparse **silently self-disables** and the
window renders normally.

**Maximum Client Size**: 2048 × 256 = 524,288 pixels (exceeds screen!)

**Rendering Speed**: SmoothShape very slow for large scales

### 17.3 Sprite Limits

**Constraints**:
```pascal
SpriteMax   = 256     // 256 sprites
SpriteMaxX  = 32      // 32 pixels wide
SpriteMaxY  = 32      // 32 pixels tall
```

**Memory**: 512 KB (fixed allocation, even if unused)

**Rendering**: Sprites not available in BITMAP (only PLOT)

### 17.4 Color Mode Restrictions

**LUT Modes**: Require palette definition
```
BITMAP `0 lut4        // LUT unset → all entries black $000000 (zero-init, not "0-7 default colors")
BITMAP `0 lut4 lutcolors $000000,$111111,...,$FFFFFF    // Correct
```

**HSV Modes**: Rely on PolarColors[] pre-computed table
- Cannot customize hue wheel
- `vColorTune` only shifts hue, doesn't redefine colors

### 17.5 No Built-In Drawing Commands

**BITMAP vs. PLOT**:
- BITMAP: Pixel data only (no LINE, CIRCLE, TEXT, etc.)
- PLOT: Full drawing primitives

**Workaround**: Use PLOT for graphics, then send result to BITMAP via screen capture or manual pixel copying

### 17.6 No Zooming

**Fixed Scale**:
- Normal mode: 1:1 pixel mapping
- Sparse mode: Integer scaling only
- No fractional zooming

**Workaround**: Pre-scale image data on P2 before sending

### 17.7 Single Color Mode at a Time

**Constraint**: `vColorMode` is global

**Cannot Mix**:
```
BITMAP `0 lut4 0,1,2,3 rgb24 $FF0000,$00FF00,$0000FF
```
- First 4 pixels: LUT4 (indices 0,1,2,3)
- Next 3 pixels: RGB24 (but mode already switched!)

**Workaround**: Send all pixels of one mode, then switch, then send next mode

---

## 18. Comparison to Related Display Types

### 18.1 vs. SPECTRO (dis_spectro = 4)

**SPECTRO**:
- Scrolling waterfall display (FFT over time)
- Automatic trace with scroll
- Color-coded magnitude
- No manual pixel access

**BITMAP**:
- General-purpose pixel canvas
- 8 trace modes (wrap or scroll)
- Manual pixel positioning
- Direct pixel data

**Shared**:
- Same color-translation *code* (`TranslateColor`) — but SPECTRO's parser admits only 6 of the 19
  modes (1767) vs BITMAP's 19 (2395); see §15.4
- Same sparse pixel system
- Same scaling mechanism (vDotSize, vDotSizeY) — but SPECTRO clamps `DOTSIZE` 1..16 (1762–1765)
  vs BITMAP 1..256 (2388–2391)

**Code Overlap**: ~60% (color translation, scaling, trace)

### 18.2 vs. PLOT (dis_plot = 5)

**PLOT**:
- Vector graphics (lines, shapes, text)
- Coordinate system with origin/offset
- Drawing primitives
- Sprite rendering

**BITMAP**:
- Raster graphics (pixels)
- Sequential trace patterns
- No drawing commands
- (Sprites in PLOT only)

**Shared**:
- Same bitmap storage
- Same sprite arrays
- Same rendering (SmoothShape, SmoothLine)

**Code Overlap**: ~40% (rendering primitives)

### 18.3 vs. TERM (dis_term = 6)

**TERM**:
- Text-only display
- Character grid
- ASCII rendering
- **No ANSI escape sequences.** TERM's colour comes from control codes 4–7, which select one of
  four pre-configured colour *pairs* (`TERM_Chr`); there is no ANSI/xterm escape parser anywhere
  in the source. (An earlier revision of this section claimed "ANSI color codes" — that was a
  cross-window contradiction with the TERM ToO, and TERM is right.)

**BITMAP**:
- Pixel-based display
- Arbitrary resolution
- Raw pixel data
- 19 color modes

**Shared**:
- None (completely different)

### 18.4 vs. SCOPE (dis_scope = 1)

**SCOPE**:
- Time-domain waveform
- Analog samples
- Trigger system
- Channel overlays

**BITMAP**:
- Frequency-domain or arbitrary pixel data
- No trigger
- Trace patterns instead of channels

**Shared**:
- **Packed data support only** (`SetPack`/`NewPack`/`UnPack`, 4146–4171) — **nothing else.**
- ❌ **NOT the sample buffer.** BITMAP has **no sample buffer at all**: `BITMAP_Update`
  (2416–2485) never touches `Y_SampleBuff` / `SamplePtr` / `SamplePop`. Pixels go straight to the
  bitmap via `PlotPixel` (3433–3444) or `SmoothShape` (2472–2478). See §20.1.

---

## 19. Element Array Protocol Specification

### 19.1 Protocol Overview

The BITMAP display (and all debug displays) receives commands and data through an **element array protocol**. This ASCII-based protocol uses simple type-value pairs.

**Core Concept**: Messages are sequences of **(type, value)** pairs stored in parallel arrays:
- `DebugDisplayType[i]`: Element type (byte)
- `DebugDisplayValue[i]`: Element value (integer or pointer to string)

**GlobalUnit.pas:126-127**:
```pascal
DebugDisplayType:   array[0..DebugDisplayLimit-1] of byte;
DebugDisplayValue:  array[0..DebugDisplayLimit-1] of integer;
DebugDisplayLimit = 1100;  // 1k data elements + commands
```

### 19.2 Element Type Constants

```pascal
const
  ele_end   = 0;    // End of message
  ele_key   = 3;    // Keyword/command
  ele_num   = 4;    // Numeric value
  ele_str   = 5;    // String (PChar pointer)
```

### 19.3 Configuration Example

**Propeller 2 Command**:
```spin2
debug(`BITMAP SIZE 320 240 TRACE 8 LUT8 LONGS_1BIT DOTSIZE 2)
```

**Parsed as**:
```
[ele_key:key_size] [ele_num:320] [ele_num:240]
[ele_key:key_trace] [ele_num:8]
[ele_key:key_lut8]
[ele_key:key_longs_1bit]
[ele_key:key_dotsize] [ele_num:2]
[ele_end]
```

**Parser reads sequentially**: `while NextKey do case val of...`

### 19.4 Pixel Data Example

**Sending pixel values**:
```spin2
' Send 32 1-bit pixels packed into one long
packed := %11110000_10101010_11001100_00001111
debug(`BITMAP `UDEC_(packed))
```

**Parsed as**:
```
[ele_num:packed] [ele_end]
```

**BITMAP_Update unpacks**: 32 pixels from single integer using UnPack().

---

## 20. Buffer Management and Timing

### 20.1 No Sample Buffer

**Key Difference**: Unlike SCOPE/FFT, BITMAP has **no circular sample buffer**.

**Direct Rendering**: Pixels written directly to Bitmap[0] as received.

**Memory**: Only bitmap storage (width × height × 3 bytes for RGB24).

### 20.2 Write Operation Timing

**When Pixels Are Written** (BITMAP_Update):

```pascal
while NextNum do
begin
  v := NewPack;                    // Get packed value
  for i := 1 to vPackCount do      // Unpack samples
  begin
    p := UnPack(v);                // Extract pixel value
    PlotPixel(p);                  // WRITE IMMEDIATELY to Bitmap[0]
    StepTrace;                     // Advance to next position
  end;
end;
```

**Write Characteristics**:
- **Immediate**: No buffering, straight to bitmap
- **Frequency**: On every `ele_num` received
- **Trace position**: Updated after each pixel (vPixelX, vPixelY)
- **Scrolling**: Triggered when edge reached (if scroll bit set)

**Example** (trace mode 0, left-to-right):
```
Pixel 1: PlotPixel at (0,0), StepTrace → (1,0)
Pixel 2: PlotPixel at (1,0), StepTrace → (2,0)
...
Pixel 320: PlotPixel at (319,0), StepTrace → (0,1) + maybe scroll
```

### 20.3 SET Command (Random Access)

**Direct Positioning**:
```pascal
key_set:
begin
  vTrace := vTrace and 7;              // Cancel scrolling (clear bit 3)
  if KeyValWithin(vPixelX, 0, vWidth - 1) then
    KeyValWithin(vPixelY, 0, vHeight - 1);
end;
```

**Allows**: Jump to any (x,y) position without trace pattern; also cancels scroll mode.

**Use Case**: Drawing non-sequential graphics (sprites, text, shapes).

### 20.4 Display Update Timing

**BitmapToCanvas Call** (line 2480):
```pascal
if RateCycle and not vUpdate then BitmapToCanvas(0);
```
- **Automatic (default)**: Display updates every `vRate` pixels via `RateCycle`. Both normal and sparse pixel paths share the same `RateCycle` gate.
- **Manual mode** (`vUpdate = True`): `BitmapToCanvas` is suppressed during pixel writes; explicit `UPDATE` directive forces refresh.
- `RateCycle` increments `vRateCount` and returns `True` when it reaches `vRate`, then resets to 0 (lines 3079–3088).

---

## 21. Bitmap System and Double-Buffering

### 21.1 Bitmap Architecture

**Two-Bitmap System**:
```pascal
Bitmap[0]: TBitmap;    // Render target (back buffer)
Bitmap[1]: TBitmap;    // Display buffer (front buffer)
```

**Pixel Format**: 24-bit RGB (3 bytes/pixel), BGR in memory.

**Memory** (320×240 example):
```
320 × 240 × 3 = 230,400 bytes ≈ 225 KB per bitmap
Total: 450 KB for both bitmaps
```

### 21.2 Canvas Display Scaling

`BitmapToCanvas` always *calls* `StretchDraw` for BITMAP (and SPECTRO and PLOT), regardless of sparse mode (lines 3522–3530):

```pascal
procedure TDebugDisplayForm.BitmapToCanvas(Level: integer);
begin
  if Level = 0 then
    Bitmap[1].Canvas.Draw(0, 0, Bitmap[0]);   // 3524-3525 copy back→front
  if DisplayType in [dis_spectro, dis_plot, dis_bitmap] then
    Canvas.StretchDraw(Rect(0, 0, vClientWidth, vClientHeight), Bitmap[1])   // 3527
  else
    Canvas.Draw(0, 0, Bitmap[1]);             // 3529
end;
```

**Whether it actually scales is decided in `SetSize`, not here** (2936–2951, §3.2). `StretchDraw`
stretches `Bitmap[1]` (whatever size `SetSize` gave it) to `vClientWidth × vClientHeight`
(always `vWidth·vDotSize × vHeight·vDotSizeY`, 2936–2937). So:

| Case | `Bitmap[1]` size | Client rect | Result of `StretchDraw` |
|---|---|---|---|
| **Sparse active** (colour + `DOTSIZE` ≥ 4 both axes) | **physical** `vWidth·vDotSize × vHeight·vDotSizeY` (2940-2943) | identical | **1:1 blit — nothing is stretched** |
| **Sparse off, `DOTSIZE` > 1** (no colour, or a dot size < 4) | **logical** `vWidth × vHeight` (2948-2951) | `vWidth·vDotSize × …` | **upscale** by `vDotSize`/`vDotSizeY` (nearest-neighbour block pixels) |
| **Sparse off, `DOTSIZE` = 1** (default) | `vWidth × vHeight` | `vWidth × vHeight` | 1:1 |

**Effect in sparse mode**: the magnification is *already in the bitmap*. `SmoothShape` draws each
cell (solid sparse fill + round data dot) directly into `Bitmap[0]` at **physical** coordinates —
so the anti-aliased dots survive to the screen unmangled, and the StretchDraw is a pass-through.

**Effect when sparse is off but `DOTSIZE` > 1**: `PlotPixel` writes one logical pixel per sample
into a logical-size bitmap, and `StretchDraw` blows it up — you get hard square blocks, no dots,
no sparse-coloured field. This is the case that a `DOTSIZE 2`/`DOTSIZE 3` window silently lands
in, even with a `SPARSE` colour set.

### 21.3 BitmapToCanvas Operation

```pascal
procedure BitmapToCanvas(Level: integer);
begin
  if Level = 0 then
    Bitmap[1].Canvas.Draw(0, 0, Bitmap[0]);    // Copy back→front

  // BITMAP uses StretchDraw for scaling
  Canvas.StretchDraw(Rect(0, 0, vClientWidth, vClientHeight), Bitmap[1]);
end;
```

### 21.4 PlotPixel Implementation

```pascal
procedure PlotPixel(p: integer);
var
  v: integer;
  line: PByteArray;
begin
  p := TranslateColor(p, vColorMode);    // Convert to RGB24
  line := BitmapLine[vPixelY];           // Scanline pointer
  v := vPixelX * 3;
  line[v+0] := p shr 0;                  // Blue
  line[v+1] := p shr 8;                  // Green
  line[v+2] := p shr 16;                 // Red
end;
```

**Performance**: Direct memory write, no GDI overhead.

---

## 22. Shared Infrastructure

### 22.1 Color Translation System

**TranslateColor Function**: Converts 19 color modes to RGB24.

**BITMAP-Specific Modes**:
- **LUT1/2/4/8**: Palette lookup (2-256 colors)
- **LUMA8/8W/8X**: Luminance with color tint
- **HSV8/8W/8X, HSV16/16W/16X**: Hue-saturation-value
- **RGBI8/8W/8X**: RGB + intensity
- **RGB8/16/24**: Direct RGB

**Example** (LUT8):
```pascal
p := vLut[p and $FF];    // Index into 256-color palette
```

**Color constants**: BITMAP has **no fixed channel/trace palette** (the
`DefaultScopeColors` table does not apply) — every pixel color is produced by
`TranslateColor` from the active color mode/LUT. The only fixed color constants are
the **background** values returned by `GetBackground` (`DebugDisplayUnit.pas`
3180–3205), selected by color mode:

| Color mode | Background | Hex |
|---|---|---|
| LUT1/2/4/8 | `vLut[0]` | (first palette entry) |
| LUMA8/8X, HSV8/8X, RGBI8/8X, RGB8, HSV16/16X, RGB16, RGB24 | `clBlack` | `$000000` |
| LUMA8W, HSV8W, RGBI8W, HSV16W (white-base "W" modes) | `clWhite` | `$FFFFFF` |

`clBlack`/`clWhite` are literal RGB24 values (`DebugDisplayUnit.pas` 187–188).

### 22.2 Data Packing System

**BITMAP uses 12 packing modes**:
```
LONGS_1BIT:  32 pixels/long (1-bit per pixel)
LONGS_2BIT:  16 pixels/long (2-bit per pixel)
...
BYTES_4BIT:  2 pixels/byte (4-bit per pixel)
```

**SetPack/UnPack**: Same as FFT (shared code).

**Bandwidth Savings**: 32× reduction with LONGS_1BIT.

### 22.3 Trace System

**StepTrace Function**: Advances (vPixelX, vPixelY) based on vTrace mode.

**8 Directions**: Left/right-to-right, top/bottom-to-top, with/without scrolling.

**Shared**: Used by BITMAP, SPECTRO, PLOT (not SCOPE/FFT/LOGIC).

### 22.4 ScrollBitmap Function

**Shifts bitmap contents** when edge reached:
```pascal
Canvas.CopyRect(dst, Canvas, src);    // Shift pixels
Canvas.FillRect(exposed_area);        // Clear new area
```

**Shared**: BITMAP, SPECTRO (for waterfall effect).

---

## 23. Initialization Lifecycle

### 23.1 Window Creation

**1. Form Created**: `TDebugDisplayForm.Create(Owner)`

**2. Bitmaps Allocated**:
```pascal
Bitmap[0] := TBitmap.Create;
Bitmap[1] := TBitmap.Create;
Bitmap[0].PixelFormat := pf24bit;
Bitmap[1].PixelFormat := pf24bit;
```

**3. BITMAP_Configure Called**:
```pascal
DisplayType := DebugDisplayValue[0];    // dis_bitmap = 7
ptr := 2;
case DisplayType of
  dis_bitmap: BITMAP_Configure;
end;
```

**4. Configuration Parsing**:
```pascal
// Set defaults
vTrace := 0;
vDotSize := 1;
vColorMode := key_rgb24;   // SetDefaults (line 2889); overridden by color-mode directive in BITMAP_Configure

// Parse parameters
while NextKey do
  case val of
    key_size: ...;
    key_trace: ...;
    key_lut1..key_rgb24: KeyColorMode;
    key_longs_1bit..key_bytes_4bit: KeyPack;
  end;
```

**5. Bitmap Sizing** — the tail of `BITMAP_Configure`, verbatim (2411–2413):
```pascal
SetSize(0, 0, 0, 0);                             // 2411 — zero margins; sizes BOTH bitmaps
                                                 //        and applies the SPARSE gate (§3.2)
SetTrace(vTrace, vRate = 0);                     // 2412 — ModifyRate is the EXPRESSION `vRate = 0`
if vRate = -1 then vRate := vWidth * vHeight;    // 2413 — only here, never at runtime
```
⚠️ `ModifyRate` is **`vRate = 0`**, *not* `True`. The rate is auto-derived (to `vWidth` for scan
patterns 0–3, `vHeight` for 4–7, per 2977–2978) **only when the user supplied no `RATE`**.
Passing `True` here would clobber a user-specified `RATE` — which is exactly what the *runtime*
`CLEAR` and `TRACE` handlers do (2447, 2430), and why they discard it.

**6. Ready**: Window displayed, trace at initial position, waiting for pixels.

### 23.2 Message Processing Loop

```
┌─→ 1. Serial data arrives
│   2. BITMAP_Update called
│   3. Pixel written → Bitmap[0]
│   4. StepTrace advances position
│   5. BitmapToCanvas → display updated
└─── Loop
```

**Termination**: User closes window, bitmaps auto-freed by Delphi.

---

## Conclusion

The BITMAP window implementation in DebugDisplayUnit.pas represents a highly versatile pixel-based visualization system with the following characteristics:

### Strengths:
1. **19 Color Modes**: Comprehensive palette/color format support (LUT, LUMA, HSV, RGB)
2. **8 Trace Patterns**: Flexible scan modes with optional scrolling
3. **Sparse Pixel Mode**: Magnified display with grid (ideal for retro graphics)
4. **Packed Data**: Bandwidth optimization for low-resolution displays
5. **Runtime Configuration**: Change modes, palettes, trace patterns mid-stream
6. **Direct Memory Access**: Fast scanline writes for maximum throughput
7. **Double Buffering**: Flicker-free display updates
8. **Integration**: Shares infrastructure with SPECTRO and PLOT

### Design Philosophy:
- **Flexibility**: Supports both streaming (trace modes) and random-access (SET) pixel writes
- **Efficiency**: Direct scanline access for normal mode, anti-aliased rendering for sparse mode
- **Extensibility**: Color mode framework allows easy addition of new formats
- **Compatibility**: Designed for P2 microcontroller debug/visualization workflows

### Technical Highlights:
- **PlotPixel**: ~10M pixels/sec (direct memory write)
- **TranslateColor**: Comprehensive color space conversions
- **StepTrace**: 8 scan patterns with wrap/scroll behavior
- **SmoothShape**: Anti-aliased rounded rectangles for sparse mode
- **ScrollBitmap**: Efficient bitmap shifting

### Typical Use Cases:
1. **Image Display**: Show camera, sensor, or processed image data
2. **Waveform Persistence**: Scrolling oscilloscope-style display
3. **Pixel Art**: Magnified retro graphics with sparse mode
4. **False-Color Mapping**: Sensor data with custom color modes
5. **LED Matrix Simulation**: Sparse pixel display with grid

The implementation demonstrates careful attention to both performance (direct scanline access, packed data) and flexibility (19 color modes, 8 trace patterns, runtime configuration). It serves as a robust tool for embedded systems visualization on the Propeller 2 platform.

---

## References

### Source Files:
- **DebugDisplayUnit.pas**: Main implementation (6000+ lines)
- **DebugUnit.pas**: Display management and command routing
- **SerialUnit.pas**: Serial communication and buffering
- **GlobalUnit.pas**: Global types and variables

### Key Algorithms:
- **TranslateColor**: Multi-mode color space conversion
- **StepTrace**: 8 scan patterns with wrap/scroll
- **SmoothShape**: Anti-aliased rounded rectangle rendering
- **ScrollBitmap**: Efficient bitmap shifting

### Related Displays:
- **SPECTRO**: Scrolling waterfall (shares the color-translation and scaling *code*; accepts only
  6 of the 19 modes and clamps `DOTSIZE` 1..16 — §15.4)
- **PLOT**: Vector graphics (shares the *internal* renderers and the sprite arrays — **but none of
  PLOT's drawing directives**; §11)
- **SCOPE**: Analog waveforms (shares **only** the packed-data support — BITMAP has **no** sample
  buffer; §18.4, §20.1)
- **TERM**: Text display (no overlap)

---

**End of Document**
