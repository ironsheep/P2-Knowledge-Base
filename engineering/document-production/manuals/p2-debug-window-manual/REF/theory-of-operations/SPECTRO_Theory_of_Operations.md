# SPECTRO Display Window - Theory of Operations

**Current as of**: PNut v55 for Propeller 2
**Directive coverage verified**: 2026-06-01 against `DebugDisplayUnit.pas` (v55)
**Companion**: [Debug Window Directive Matrix](../DEBUG-WINDOW-DIRECTIVE-MATRIX.md) — cross-window config/display/keyboard/mouse reference

## Table of Contents

1. [Overview](#1-overview)
2. [Display Type and Constants](#2-display-type-and-constants)
3. [Data Structures](#3-data-structures)
4. [Configuration and Initialization](#4-configuration-and-initialization)
5. [Update Processing](#5-update-processing)
6. [FFT Processing Pipeline](#6-fft-processing-pipeline)
7. [Color Mapping System](#7-color-mapping-system)
8. [Rendering Pipeline](#8-rendering-pipeline)
9. [Trace System and Scrolling](#9-trace-system-and-scrolling)
10. [Rate Control System](#10-rate-control-system)
11. [Data Packing System](#11-data-packing-system)
12. [Window Management](#12-window-management)
13. [Command Protocol](#13-command-protocol)
14. [Usage Examples](#14-usage-examples)
15. [Performance Characteristics](#15-performance-characteristics)
16. [Comparison with FFT Display](#16-comparison-with-fft-display)
17. [Implementation Details](#17-implementation-details)
18. [Element Array Protocol Specification](#18-element-array-protocol-specification)
19. [Buffer Management and Timing](#19-buffer-management-and-timing)
20. [Bitmap System and Double-Buffering](#20-bitmap-system-and-double-buffering)
21. [Shared Infrastructure](#21-shared-infrastructure)
22. [Initialization Lifecycle](#22-initialization-lifecycle)
23. [Summary](#23-summary)

---

## 1. Overview

### 1.1 Purpose

The **SPECTRO** (Spectrogram) display window is a real-time frequency spectrum analyzer that visualizes audio or signal frequency content over time. Unlike the FFT display which shows a single frequency snapshot, SPECTRO creates a **waterfall display** where **color intensity always represents signal magnitude** and the two screen axes carry time and frequency — *which way round depends on `TRACE`*:

- **Trace directions 4–7 — including the default `TRACE $F`**: **horizontal = time**, **vertical = frequency bins**.
- **Trace directions 0–3**: **horizontal = frequency bins**, **vertical = time**.

The mapping is decided by the width/height swap in `SPECTRO_Configure` (1781-1787), which runs **only** when bit 2 of `vTrace` is clear:

```pascal
1781:  vHeight := FFTlast - FFTfirst + 1;
1782:  if vTrace and $4 = 0 then    // only traces 0..3 swap
```

`DEPTH` writes `vWidth` (1751), so at the default `vTrace = $F` (1724) the depth stays on the **horizontal** axis. (§16.1 and §4.3 state the same rule.)

This creates a scrolling "heat map" visualization perfect for analyzing time-varying frequency content, identifying harmonics, tracking frequency shifts, and visualizing spectral evolution.

### 1.2 Key Features

- **Real-time FFT processing**: Continuous frequency analysis with configurable FFT sizes (4 to 2048 points)
- **Waterfall visualization**: Time-scrolling color-coded frequency display
- **Flexible color mapping**: Multiple color modes including luminance, HSV, and RGB encodings
- **Logarithmic scaling**: Optional log-scale magnitude display for wide dynamic range
- **Configurable depth**: Time-history depth, independent of FFT size (default **256**; lands on the *horizontal* axis for traces 4–7 including the default, on the *vertical* axis for traces 0–3)
- **Magnification control**: Adjustable FFT magnitude scaling (bit-shift magnification)
- **Frequency range selection**: Display subset of frequency bins (FFTfirst to FFTlast)
- **Rate throttling**: Control display update rate independent of sample rate
- **Eight trace directions**: Horizontal/vertical scrolling in multiple directions
- **Dot size scaling**: X/Y pixel scaling for enlarged displays
- **Data packing**: Efficient 12-mode packed data transmission

### 1.3 Typical Applications

- **Audio spectrum analysis**: Visualize audio frequency content over time
- **Signal monitoring**: Track frequency shifts and harmonics
- **Vibration analysis**: Analyze mechanical vibration spectra
- **Communications**: Monitor RF signal spectra
- **Musical analysis**: Visualize musical notes and harmonics
- **Echo/reverb visualization**: See acoustic reflections
- **Frequency sweep analysis**: Track sweeping tones

---

## 2. Display Type and Constants

### 2.1 Display Type Identifier

**DebugDisplayUnit.pas:26**
```pascal
const
  dis_spectro = 4;
```

The SPECTRO display is identified by `dis_spectro = 4` in the display type enumeration.

### 2.2 FFT-Related Constants

**DebugDisplayUnit.pas:154-177** (plus `fft_default` at **206**, in a separate const group)
```pascal
const
  DataSetsExp           = 11;
  DataSets              = 1 shl DataSetsExp;  // 2048

  FFTexpMax             = DataSetsExp;        // 11
  FFTmax                = DataSets;           // 2048

  SPECTRO_Samples       = DataSets;           // 2048
  SPECTRO_PtrMask       = SPECTRO_Samples - 1; // 2047

  fft_default           = 512;
```

**Key Constants**:
- **FFTmax**: Maximum FFT size = 2048 samples
- **FFTexpMax**: Maximum FFT exponent = 11 (2^11 = 2048)
- **SPECTRO_Samples**: Circular buffer size = 2048 samples
- **SPECTRO_PtrMask**: Wraparound mask for circular buffer indexing
- **fft_default**: Default FFT size = 512 samples

### 2.3 Color Mode Constants

**DebugDisplayUnit.pas:43-61**
```pascal
const
  key_lut1              = 10;   // 1-bit lookup table
  key_lut2              = 11;   // 2-bit lookup table
  key_lut4              = 12;   // 4-bit lookup table
  key_lut8              = 13;   // 8-bit lookup table
  key_luma8             = 14;   // 8-bit luminance
  key_luma8w            = 15;   // 8-bit luminance, white variant
  key_luma8x            = 16;   // 8-bit luminance, extended range
  key_hsv8              = 17;   // 8-bit HSV
  key_hsv8w             = 18;   // 8-bit HSV, white variant
  key_hsv8x             = 19;   // 8-bit HSV, extended range
  key_rgbi8             = 20;   // 8-bit RGBI
  key_rgbi8w            = 21;   // 8-bit RGBI, white variant
  key_rgbi8x            = 22;   // 8-bit RGBI, extended range
  key_rgb8              = 23;   // 8-bit RGB (3:3:2)
  key_hsv16             = 24;   // 16-bit HSV
  key_hsv16w            = 25;   // 16-bit HSV, white variant
  key_hsv16x            = 26;   // 16-bit HSV, extended range
  key_rgb16             = 27;   // 16-bit RGB (5:6:5)
  key_rgb24             = 28;   // 24-bit RGB
```

SPECTRO defaults to **key_luma8x** (8-bit luminance with extended range).

---

## 3. Data Structures

### 3.1 Sample Buffer

**DebugDisplayUnit.pas:363**
```pascal
var
  SPECTRO_SampleBuff: array [0..SPECTRO_Samples - 1] of integer;
```

**Characteristics**:
- **Size**: 2048 samples (fixed, power-of-2)
- **Type**: Signed 32-bit integers
- **Organization**: Circular buffer with wrap-around
- **Indexing**: Uses `SPECTRO_PtrMask` for modulo arithmetic

**Memory footprint**: 2048 × 4 bytes = **8,192 bytes** (8 KB)

### 3.2 FFT Working Arrays

**DebugDisplayUnit.pas:384-395**
```pascal
var
  FFTexp                : integer;          // FFT exponent (2^exp = size)
  FFTmag                : integer;          // Magnitude bit-shift
  FFTfirst              : integer;          // First bin to display
  FFTlast               : integer;          // Last bin to display
  FFTsin                : array [0..FFTmax - 1] of int64;  // Sine table
  FFTcos                : array [0..FFTmax - 1] of int64;  // Cosine table
  FFTwin                : array [0..FFTmax - 1] of int64;  // Hanning window
  FFTreal               : array [0..FFTmax - 1] of int64;  // Real component
  FFTimag               : array [0..FFTmax - 1] of int64;  // Imaginary component
  FFTsamp               : array [0..FFTmax - 1] of integer; // Input samples
  FFTpower              : array [0..FFTmax div 2 - 1] of integer; // Magnitude
  FFTangle              : array [0..FFTmax div 2 - 1] of integer; // Phase
```

**Array Details**:

| Array | Size | Type | Purpose | Memory |
|-------|------|------|---------|--------|
| FFTsin | 2048 | int64 | Pre-computed sine values | 16 KB |
| FFTcos | 2048 | int64 | Pre-computed cosine values | 16 KB |
| FFTwin | 2048 | int64 | Hanning window coefficients | 16 KB |
| FFTreal | 2048 | int64 | FFT real component (working) | 16 KB |
| FFTimag | 2048 | int64 | FFT imaginary component (working) | 16 KB |
| FFTsamp | 2048 | integer | Input sample staging | 8 KB |
| FFTpower | 1024 | integer | Output magnitude per bin | 4 KB |
| FFTangle | 1024 | integer | Output phase per bin | 4 KB |

**Total FFT memory**: **96 KB**

### 3.3 Color Translation Tables

**DebugDisplayUnit.pas:365**
```pascal
var
  PolarColors: array [0..255] of integer;
```

**Purpose**: Pre-computed HSV-to-RGB color lookup table for polar color modes.

**Memory**: 256 × 4 bytes = **1,024 bytes** (1 KB)

### 3.4 Configuration Variables

**DebugDisplayUnit.pas:272-355** (the form's `v*` state block; the fields SPECTRO uses are
scattered through it — individual declaration lines given below)
```pascal
var
  vWidth                : integer;  // 276 — display width (time depth, or bins after swap)
  vHeight               : integer;  // 277 — display height (frequency bins, or depth after swap)
  vRange                : integer;  // 282 — magnitude range
  vSamples              : integer;  // 283 — FFT size (power-of-2)
  vRate                 : integer;  // 284 — update rate divisor
  vRateCount            : integer;  // 285 — rate counter
  vColorTune            : integer;  // 313 — color tint / hue offset
  vLogScale             : boolean;  // 325 — logarithmic magnitude scaling
  vHideXY               : boolean;  // 328 — suppress measurement-cursor readout
  vColorMode            : integer;  // 331 — color encoding mode
  vTrace                : integer;  // 332 — trace direction (0-7, +8 for scroll)
  vPixelX               : integer;  // 333 — current trace X position
  vPixelY               : integer;  // 334 — current trace Y position
  vDotSize              : integer;  // 336 — horizontal pixel scaling
  vDotSizeY             : integer;  // 337 — vertical pixel scaling
  vPackAlt              : boolean;  // 351 — ALT modifier   (see §11)
  vPackSignx            : boolean;  // 352 — SIGNED modifier (see §11)
  vPackMask             : integer;  // 353
  vPackShift            : integer;  // 354
  vPackCount            : integer;  // 355
```

---

## Directive Reference (v55-verified)

> Source authority: `DebugDisplayUnit.pas` (PNut v55). See also §5.5 and §4 of the
> [Debug Window Directive Matrix](../DEBUG-WINDOW-DIRECTIVE-MATRIX.md).

### Configuration directives

Accepted in `SPECTRO_Configure` (lines 1719–1790). All are optional; defaults shown.

| Directive | Parameter(s) | Range / notes | Default | Pascal lines |
|---|---|---|---|---|
| `TITLE 'str'` | string | window title | `"<name> - SPECTRO"` (FormCreate:626) | 1737-1738 |
| `POS left top` | two integers | window position | host origin ≈(0,210), no cascade (FormCreate:628-629, KeyPos:2712-2716) | 1739-1740 |
| `SAMPLES n {first last}` | n = FFT size; optional first/last bin | n clamped to 4..2048, then **rounded DOWN** to the next lower-or-equal power of 2 (`Trunc(Log2(...))`, 1744); first ∈ [0, n/2−2], last ∈ [first+1, n/2−1] | 512 (bins 0..255) | 1741-1750 |
| `DEPTH n` | integer | 1..2048 (time-history lines); writes `vWidth` (1751) — see note below on which *axis* it lands on | **256** (`SetDefaults`:2884) | 1751-1752 |
| `MAG n` | integer | 0..11 (2^n magnitude multiplier) | 0 | 1753-1754 |
| `RANGE n` | integer | 1..$7FFFFFFF | $7FFFFFFF | 1755-1756 |
| `RATE n` | integer | 1..2048 samples per display update | samples÷8 | 1757-1758 |
| `TRACE n` | integer | 0..15 (bits 0-2 = direction, bit 3 = scroll) | 15 ($F) | 1759-1760 |
| `DOTSIZE x {y}` | 1 or 2 integers | each clamped 1..16 (vs BITMAP's 1..256) | 1, 1 | 1761-1765 |
| color-mode | `mode-keyword {tune}` | **RESTRICTED:** `LUMA8`, `LUMA8W`, `LUMA8X`, `HSV16`, `HSV16W`, `HSV16X` only (line 1767). Each takes an **optional tune parameter** — see note below | `LUMA8X`, `vColorTune = 0` | 1767-1768 |
| `LOGSCALE` | none | enable log-magnitude display | off | 1769-1770 |
| `HIDEXY` | none | suppress on-screen measurement-cursor readout | off | 1771-1772 |
| packed `LONGS_1BIT..BYTES_4BIT` | `{ALT} {SIGNED}` (both optional, either order) | select data packing mode | **unpacked** (`SetDefaults`:2915 → `SetPack(0, False, False)`) | 1773-1774 |

**`SAMPLES` rounds down, never up** (1744-1745): `SAMPLES 1000` → `Log2(1000) = 9.97` →
`FFTexp = 9` → `vSamples = 512` (**not** 1024).

**`DEPTH` axis** (1751, 1781-1787): `DEPTH` always writes `vWidth`. Whether that becomes the
**horizontal** or the **vertical** extent depends on the trace direction — for traces 4–7
(including the default `$F`) it stays horizontal; for traces 0–3 the W/H swap moves it to
vertical. See §4.3. The *default value* does not vary: it is **256**, seeded unconditionally
by `SetDefaults` (2884) before `SPECTRO_Configure` runs.

**Color-mode restriction** (line 1767): SPECTRO accepts only **six** color modes — the
luminance and 16-bit HSV families (`key_luma8..key_luma8x`, `key_hsv16..key_hsv16x`).
The broader LUT, RGBI, RGB8, HSV8, RGB16, RGB24 families present in other
windows are **not** accepted here.

**Color-mode tune parameter** (`KeyColorMode`, 2785-2804): the color-mode keyword is not bare —
it optionally consumes one following element into `vColorTune`.
- `LUMA8` / `LUMA8W` / `LUMA8X` take **either** a color keyword `ORANGE`..`GRAY`
  (→ `vColorTune = val − key_orange`, i.e. 0..7, 2797) **or** a bare number (2800).
  Both `LUMA8 CYAN` and `LUMA8 3` are legal.
- `HSV16` / `HSV16W` / `HSV16X` take a **numeric hue offset only** (2803).
- Default `vColorTune = 0` (`SetDefaults`:2890).

**Packing modifiers** (`KeyPack`, 2817-2832): `ALT` = alternate bit/nibble ordering
(`NewPack`, 4158-4164 — a **full within-byte bit reversal** for the 1-bit modes);
`SIGNED` = sign-extend each unpacked sub-sample (`UnPack`, 4170). Neither is implied by the
mode — see §11.2.

### Display / data directives

Accepted in `SPECTRO_Update` (lines 1792–1834).

| Directive | Notes | Pascal lines |
|---|---|---|
| numeric sample stream | bare `ele_num` values; unpacked through current packing mode; triggers FFT+draw when buffer full and rate cycles | 1818-1831 |
| `CLEAR` | clears bitmap, resets sample-pop counter and rate counter, resets trace position | 1801-1808 |
| `SAVE …` | six forms — see the grammar below. **A bare `SAVE` writes nothing.** | 1809-1810 → `KeySave` 2839-2865 |
| `PC_KEY` | polls latched keypress; triggers `SendKeyPress` | 1811-1812 |
| `PC_MOUSE` | polls cursor position + buttons + wheel; triggers `SendMousePos` | 1813-1814 |
| `CLOSE` | closes the window and frees its display slot. **Dispatched at the parser layer, not in `SPECTRO_Update`** — see below. | *(none in `DebugDisplayUnit.pas`)* |

Strings and all other directives not listed above are rejected (string causes
immediate loop break; unrecognised keys are silently skipped).

**`SAVE` grammar** (`KeySave`, 2839-2865). The filename always comes **last**; `.bmp` is appended:

| Form | Writes |
|---|---|
| `SAVE 'name'` | `Bitmap[1]` (the front/display buffer) → `name.bmp` (2843) |
| `SAVE WINDOW 'name'` | desktop **scrape** of the window's *outer* rect — includes title bar and borders; vulnerable to occlusion (2846-2864) |
| `SAVE left top width height 'name'` | desktop scrape of an arbitrary screen region (2856-2864) |
| `SAVE WINDOW` | captures to `DesktopBitmap` in memory — **no file** |
| `SAVE l t w h` | captures to `DesktopBitmap` in memory — **no file** |
| `SAVE` (bare) | `NextStr`/`NextKey`/`KeyVal` all fail → **`Exit`; nothing at all is written** |

> ⚠️ **Sharp edge (2848):** a non-`WINDOW` keyword after `SAVE` is **consumed and then discarded**
> by the `Exit`. `` `Spec1 SAVE CLEAR `` does nothing **and eats the `CLEAR`**.
>
> ⚠️ **`SAVE 'name'` writes the bitmap at 1× LOGICAL scale — un-`DOTSIZE`d.** SPECTRO never sets
> `vSparse`, so `SetSize` (2946-2951) always allocates `Bitmap[0/1]` at `vWidth × vHeight`;
> `DOTSIZE` magnification is applied at display time only (`ClientWidth := vWidth * vDotSize`,
> 2936-2937). To capture the magnified on-screen appearance, use `SAVE WINDOW 'name'`.

**`CLOSE`** (`key_close` = 49) is a **real, working directive** even though it appears in no
`XXX_Update` case statement — it is dispatched one layer up, in `p2com.asm`:
`parse_debug_string` (p2com.asm:19565-19572) detects `CLOSE` on an *existing-display command*,
reverts the name symbol and clears that display's bit in `debug_display_ena`
(p2com.asm:19613-19624); `TDebugForm.ChrIn` (`DebugUnit.pas:236-237`) then runs the **full**
`UpdateDisplay(...)` and only afterwards closes the form. Consequences:
- **Command-only** — ignored in a *new-display declaration*.
- **Multi-target** — `` `Spec1 Spec2 CLOSE `` closes all named targets.
- **Update-first, close-second** — `` `Spec1 SAVE 'shot' CLOSE `` **saves, then closes.**
- It reclaims one of the 32 display slots; the id and the name become reusable. It is the
  per-window counterpart of the global `DEBUG_END_SESSION` teardown.

### Keyboard & mouse

SPECTRO uses the **shared input model** — there is no per-window keyboard or
mouse handling logic beyond coordinate mapping.

| Handler | Lines | Behaviour |
|---|---|---|
| `WMGetDlgCode` | 585-589 | Captures Tab key (`DLGC_WANTTAB`); Tab does not change focus. |
| `FormMouseMove` | 647-809 | Draws live measurement cursor showing `x,y` coordinates. For SPECTRO: `x = pixel ÷ vDotSize`, `y = pixel ÷ vDotSizeY` (line 733-734). Suppressed when `HIDEXY` set (line 737). |
| `FormMouseWheel` | 811-817 | Latches wheel direction (+1/−1) into `vMouseWheel`; auto-cleared 100 ms later by `FormMouseWheelTimerTick` (819-823). |
| `FormKeyPress` | 825-831 | Latches key byte into `vKeyPress`; auto-cleared 100 ms later by `FormKeyTimerTick` (853-857). |
| `FormKeyDown` | 833-851 | Maps non-printable keys: Left=1, Right=2, Up=3, Down=4, Home=5, End=6, Delete=7, Insert=10, PageUp=11, PageDown=12. |

**`PC_KEY` → `SendKeyPress`** (3579-3583): transmits one LONG = latched `vKeyPress` byte (0 if none), then clears it. Behaviour is identical across all nine windows.

**`PC_MOUSE` → `SendMousePos`** (3537-3577): transmits two LONGs.
- LONG 1: bits 0-12 = x, bits 13-25 = y, bits 26-27 = wheel, bits 28-30 = L/M/R buttons. `$03FFFFFF`/`$FFFFFFFF` sentinel when cursor is outside the window.
- LONG 2: RGB color of pixel under cursor (byte-swapped to `$RRGGBB`).

⚠️ SPECTRO's **on-screen readout** and **`PC_MOUSE` wire value differ in Y origin**:
- **On-screen readout** (`FormMouseMove`, lines 733-734): `x = X ÷ vDotSize`, `y = Y ÷
  vDotSizeY` — top-origin, no direction flip.
- **`PC_MOUSE` wire value** (`SendMousePos`, in the shared `dis_spectro, dis_plot,
  dis_bitmap` branch): applies `if not vDirY then y := ClientHeight − y` *before* dividing.
  Since `vDirY` is always `False` for SPECTRO (only PLOT's `CARTESIAN` sets it), the wire
  value is **Y-inverted** (bottom-origin): `x = X ÷ vDotSize`, `y = (ClientHeight − Y) ÷
  vDotSizeY`. So the P2 receives a bottom-origin Y, opposite the on-screen readout.

`HIDEXY` suppresses the on-screen readout only; `PC_MOUSE` still reports to the P2.

---

## 4. Configuration and Initialization

### 4.1 SPECTRO_Configure Method

**DebugDisplayUnit.pas:1719-1790**
```pascal
procedure TDebugDisplayForm.SPECTRO_Configure;
var
  i: integer;
begin
  // Set unique defaults
  vTrace := $F;                    // Trace mode $F (default scrolling)
  vColorMode := key_luma8x;        // Default to extended luminance
  vSamples := fft_default;         // 512 samples
  FFTexp := Trunc(Log2(fft_default)); // exp = 9
  FFTfirst := 0;
  FFTlast := fft_default div 2 - 1;  // 255 bins
  FFTmag := 0;                     // No magnification
  vDotSize := 1;                   // 1:1 pixel scaling
  vDotSizeY := 1;
  vRange := $7FFFFFFF;             // Maximum range

  // Process any parameters
  while NextKey do
  case val of
    key_title:
      KeyTitle;
    key_pos:
      KeyPos;
    key_samples:
    begin
      if not NextNum then Continue;
      FFTexp := Trunc(Log2(Within(val, 4, FFTmax)));
      vSamples := 1 shl FFTexp;
      FFTfirst := 0;
      FFTlast := vSamples div 2 - 1;
      if KeyValWithin(FFTfirst, 0, vSamples div 2 - 2) then
        KeyValWithin(FFTlast, FFTfirst + 1, vSamples div 2 - 1);
    end;
    key_depth:
      KeyValWithin(vWidth, 1, FFTmax);
    key_mag:
      KeyValWithin(FFTmag, 0, FFTexpMax);
    key_range:
      KeyValWithin(vRange, 1, $7FFFFFFF);
    key_rate:
      KeyValWithin(vRate, 1, FFTmax);
    key_trace:
      KeyVal(vTrace);
    key_dotsize:
      if KeyValWithin(vDotSize, 1, 16) then
      begin
        vDotSizeY := vDotSize;
        KeyValWithin(vDotSizeY, 1, 16);
      end;
    key_luma8..key_luma8x, key_hsv16..key_hsv16x:
      KeyColorMode;
    key_logscale:
      vLogScale := True;
    key_hidexy:
      vHideXY := True;
    key_longs_1bit..key_bytes_4bit:
      KeyPack;
  end;

  // Prepare
  PrepareFFT;
  if vRate = 0 then vRate := vSamples div 8;  // Default rate = samples/8
  vRateCount := vRate - 1;

  // Set form metrics
  vHeight := FFTlast - FFTfirst + 1;  // Height = frequency bin count
  if vTrace and $4 = 0 then           // If horizontal trace
  begin
    i := vWidth;
    vWidth := vHeight;                // Swap width/height
    vHeight := i;
  end;
  SetSize(0, 0, 0, 0);
  SetTrace(vTrace, False);
end;
```

### 4.2 Configuration Parameters

| Parameter | Key | Type | Range | Default | Description |
|-----------|-----|------|-------|---------|-------------|
| **title** | key_title | string | - | `"<name> - SPECTRO"` | Window title text |
| **pos** | key_pos | left, top | - | host origin ≈(0,210), no cascade | Window position (offset only; `KeyPos` reads 2 values, no size) |
| **samples** | key_samples | integer | 4-2048, floored to a power-of-2 | 512 | FFT size (also accepts bin range) |
| **depth** | key_depth | integer | 1-2048 | **256** (`SetDefaults`:2884) | Time-history depth in pixels; written to `vWidth` (1751). Becomes the **vertical** extent only for traces 0–3 (post-swap); for traces 4–7 — including the default `$F` — it is the **horizontal** extent |
| **mag** | key_mag | integer | 0-11 | 0 | Magnitude bit-shift (2^mag multiplier) |
| **range** | key_range | integer | 1-$7FFFFFFF | $7FFFFFFF | Maximum magnitude for scaling |
| **rate** | key_rate | integer | 1-2048 | samples/8 | Display update rate (samples per update) |
| **trace** | key_trace | integer | 0-15 | 15 | Trace direction and scroll mode |
| **dotsize** | key_dotsize | integer(s) | 1-16 | 1 | Pixel scaling (X, optional Y) |
| **colormode** | key_luma8..key_luma8x, key_hsv16..key_hsv16x | enum + optional tune | restricted set of **six** (line 1767) | key_luma8x | Color encoding mode; consumes an optional tune value into `vColorTune` (`KeyColorMode`, 2785-2804) |
| **colortune** | *(operand of the color-mode key)* | keyword `ORANGE`..`GRAY` **or** integer | 0-7 by keyword; any integer numerically | 0 (`SetDefaults`:2890) | LUMA8 family: tint. HSV16 family: numeric hue offset |
| **logscale** | key_logscale | boolean | - | false | Logarithmic magnitude scaling |
| **hidexy** | key_hidexy | boolean | - | false | Suppress the on-screen measurement-cursor coordinate readout (`FormMouseMove`:737). SPECTRO draws **no axis labels or text at all** (§12.3). Does **not** affect `PC_MOUSE` reporting |
| **packing** | key_longs_1bit..key_bytes_4bit | enum + `{ALT} {SIGNED}` | 12 modes | **unpacked** (`SetPack(0,False,False)`, `SetDefaults`:2915) | Data packing mode; see §11 |

### 4.3 Dimension Calculation

**Key Logic** (lines 1781-1787):
```pascal
vHeight := FFTlast - FFTfirst + 1;  // Frequency bin count
if vTrace and $4 = 0 then           // Horizontal trace modes (0-3)
begin
  i := vWidth;
  vWidth := vHeight;                // Swap dimensions
  vHeight := i;
end;
```

**Trace Mode and Dimensions**:
- **Trace 0-3** (horizontal scrolling): Width = frequency bins, Height = time depth
- **Trace 4-7** (vertical scrolling): Width = time depth, Height = frequency bins

**Example**: 512-point FFT, depth=300, trace=0
- FFT bins: 0-255 (256 bins)
- vHeight = 256 (before swap)
- vWidth = 300 (before swap)
- **After swap**: vWidth = 256, vHeight = 300
- **Display**: 256 pixels wide (frequency) × 300 pixels tall (time)

---

## 5. Update Processing

### 5.1 SPECTRO_Update Method

**DebugDisplayUnit.pas:1792-1834**
```pascal
procedure TDebugDisplayForm.SPECTRO_Update;
var
  i, v: integer;
begin
  while not NextEnd do
  begin
    if NextStr then Break;   // string not allowed
    if NextKey then
    case val of
      key_clear:
      begin
        ClearBitmap;
        BitmapToCanvas(0);
        SamplePop := 0;
        vRateCount := vRate - 1;
        SetTrace(vTrace, False);
      end;
      key_save:
        KeySave;
      key_pc_key:
        SendKeyPress;
      key_pc_mouse:
        SendMousePos;
    end
    else
    begin
      while NextNum do
      begin
        // Get sample(s)
        v := NewPack;
        for i := 1 to vPackCount do
        begin
          // Enter sample into buffer
          SPECTRO_SampleBuff[SamplePtr] := UnPack(v);
          SamplePtr := (SamplePtr + 1) and SPECTRO_PtrMask;
          if SamplePop < vSamples then Inc(SamplePop);
          if SamplePop <> vSamples then Continue;  // Buffer not full, exit
          if RateCycle then SPECTRO_Draw;
        end;
      end;
    end;
  end;
end;
```

### 5.2 Sample Processing Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Receive packed data value                                │
│    v := NewPack                                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Unpack multiple samples (if packed)                      │
│    for i := 1 to vPackCount do                              │
│      sample := UnPack(v)                                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Store in circular buffer                                 │
│    SPECTRO_SampleBuff[SamplePtr] := sample                  │
│    SamplePtr := (SamplePtr + 1) and SPECTRO_PtrMask         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Track buffer fill count                                  │
│    if SamplePop < vSamples then Inc(SamplePop)              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Wait for buffer full                                     │
│    if SamplePop <> vSamples then Continue                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Check rate throttle                                      │
│    if RateCycle then SPECTRO_Draw                           │
└─────────────────────────────────────────────────────────────┘
```

### 5.3 Command Processing

**Supported Commands**:

| Command | Key | Action |
|---------|-----|--------|
| **CLEAR** | key_clear | Clear display, reset sample buffer, reset trace position |
| **SAVE** | key_save | Write `Bitmap[1]` to `<name>.bmp`, **or** scrape a desktop region — six forms, three of which write no file. A **bare `SAVE` writes nothing** (`KeySave` 2839-2865; see the grammar table in the Directive Reference) |
| **PC_KEY** | key_pc_key | Send keyboard input to connected system |
| **PC_MOUSE** | key_pc_mouse | Send mouse position to connected system |
| **CLOSE** | key_close | Close the window and free its display slot. Dispatched in `p2com.asm`, **not** in `SPECTRO_Update` — the rest of the message executes first (see the Directive Reference) |

**CLEAR Command Behavior** (lines 1801-1808):
```pascal
ClearBitmap;                    // Fill with background color
BitmapToCanvas(0);              // Copy to display buffer
SamplePop := 0;                 // Reset buffer fill count
vRateCount := vRate - 1;        // Reset rate counter
SetTrace(vTrace, False);        // Reset trace position
```

---

## 6. FFT Processing Pipeline

### 6.1 PrepareFFT Method

**DebugDisplayUnit.pas:4178-4191**
```pascal
procedure TDebugDisplayForm.PrepareFFT;
var
  i: integer;
  Tf, Xf, Yf: extended;
begin
  for i := 0 to 1 shl FFTexp - 1 do
  begin
    Tf := Rev32(i) / $100000000 * Pi;
    SinCos(Tf, Yf, Xf);
    FFTsin[i] := Round(Yf * $1000);
    FFTcos[i] := Round(Xf * $1000);
    FFTwin[i] := Round((1 - Cos((i / (1 shl FFTexp)) * Pi * 2)) * $1000)
  end;
end;
```

**Purpose**: Pre-compute FFT twiddle factors and Hanning window coefficients.

**Hanning Window Formula**:
```
w[n] = 0.5 × (1 - cos(2πn / N))
     = (1 - cos(2πn / N))  (scaled by 2 in implementation)
```

**Fixed-Point Scaling**: All coefficients scaled by $1000 (4096) for integer arithmetic.

### 6.2 PerformFFT Method

**DebugDisplayUnit.pas:4193-4251**
```pascal
procedure TDebugDisplayForm.PerformFFT;
var
  i1, i2, i3, i4, c1, c2, th, ptra, ptrb: integer;
  ax, ay, bx, by, rx, ry: int64;
begin
  // Load samples into (real,imag) with Hanning window applied
  for i1 := 0 to 1 shl FFTexp - 1 do
  begin
    FFTreal[i1] := FFTsamp[i1] * FFTwin[i1];
    FFTimag[i1] := 0
  end;

  // Perform FFT on (real,imag)
  i1 := 1 shl (FFTexp - 1);
  i2 := 1;
  while i1 <> 0 do
  begin
    th := 0;
    i3 := 0;
    i4 := i1;
    c1 := i2;
    while c1 <> 0 do
    begin
      ptra := i3;
      ptrb := ptra + i1;
      c2 := i4 - i3;
      while c2 <> 0 do
      begin
        ax := FFTreal[ptra];
        ay := FFTimag[ptra];
        bx := FFTreal[ptrb];
        by := FFTimag[ptrb];
        rx := (bx * FFTcos[th] - by * FFTsin[th]) div $1000;
        ry := (bx * FFTsin[th] + by * FFTcos[th]) div $1000;
        FFTreal[ptra] := ax + rx;
        FFTimag[ptra] := ay + ry;
        FFTreal[ptrb] := ax - rx;
        FFTimag[ptrb] := ay - ry;
        ptra := ptra + 1;
        ptrb := ptrb + 1;
        c2 := c2 - 1;
      end;
      th := th + 1;
      i3 := i3 + i1 shl 1;
      i4 := i4 + i1 shl 1;
      c1 := c1 - 1;
    end;
    i1 := i1 shr 1;
    i2 := i2 shl 1;
  end;

  // Convert (real,imag) to (power,angle)
  for i1 := 0 to 1 shl (FFTexp - 1) - 1 do
  begin
    i2 := Rev32(i1) shr (32 - FFTexp);
    rx := FFTreal[i2];
    ry := FFTimag[i2];
    FFTpower[i1] := Round(Hypot(rx, ry) / ($800 shl FFTexp shr FFTmag));
    FFTangle[i1] := Round(ArcTan2(rx, ry) / (Pi * 2) * $100000000) and $FFFFFFFF;
  end;
end;
```

### 6.3 FFT Algorithm

**Algorithm**: Radix-2 decimation-in-time FFT (Cooley-Tukey)

**Stages**:
1. **Windowing**: Apply Hanning window to input samples
2. **Bit-reversal**: Implicitly handled by Rev32 indexing
3. **Butterfly operations**: Nested loops with twiddle factor multiplication
4. **Magnitude calculation**: Convert complex to polar (magnitude + phase)

**Butterfly Operation**:
```
For each pair (a, b):
  r = b × exp(-j2πk/N)
  a' = a + r
  b' = a - r
```

**Magnitude Formula** (line 4248):
```pascal
magnitude = √(real² + imag²) / (scaling_factor)
scaling_factor = $800 << FFTexp >> FFTmag
              = 2048 × 2^FFTexp / 2^FFTmag
```

**Magnification**:
- **FFTmag = 0**: No magnification (default)
- **FFTmag = 1**: 2× magnification
- **FFTmag = 2**: 4× magnification
- **FFTmag = n**: 2^n× magnification

### 6.4 Bit-Reversal Function

**DebugDisplayUnit.pas:4253-4260**
```pascal
function TDebugDisplayForm.Rev32(i: integer): int64;
const
  Rev4: array [0..15] of integer = ($0,$8,$4,$C,$2,$A,$6,$E,$1,$9,$5,$D,$3,$B,$7,$F);
begin
  Result := (Rev4[i shr 0 and $F] shl 28 or
             Rev4[i shr 4 and $F] shl 24 or
             Rev4[i shr 8 and $F] shl 20) and $FFF00000;
end;
```

**Purpose**: Reverse the **low 12 bits** of the index into the **high 12 bits** of the result
(the `and $FFF00000` mask at 4259). It reads only nibbles at `shr 0`, `shr 4` and `shr 8` —
**bits 12..31 of the input are discarded** (`Rev32($1000) = 0`). Twelve bits is exactly enough,
because `FFTexpMax = 11`. It is *not* a general 32-bit bit-reversal.

Used in two places:
- the twiddle phase in `PrepareFFT` (4185: `Tf := Rev32(i) / $100000000 * Pi`), and
- the output bit-reversal permutation in `PerformFFT` (4245: `i2 := Rev32(i1) shr (32 - FFTexp)`).

**Example**: `Rev32(1) = $80000000`, `Rev32(2) = $40000000`, `Rev32($1000) = 0` (out of range).

---

## 7. Color Mapping System

### 7.1 TranslateColor Method

**DebugDisplayUnit.pas:3090-3173**

The `TranslateColor` method converts pixel values from various color encodings to 24-bit RGB format for display. It is **shared by all nine windows**; the table below lists the modes `TranslateColor` implements.

> ⚠️ **SPECTRO accepts only SIX of them** — `LUMA8`, `LUMA8W`, `LUMA8X`, `HSV16`, `HSV16W`,
> `HSV16X` (`SPECTRO_Configure`:1767, `key_luma8..key_luma8x, key_hsv16..key_hsv16x`). The LUT,
> HSV8, RGBI8, RGB8, RGB16 and RGB24 rows below are reachable in other windows only. Only
> §7.2 (LUMA branch) and §7.3 (HSV branch) are on SPECTRO's path.

**Supported Color Modes** (of `TranslateColor`):

| Mode | Bits | Description | Color Space |
|------|------|-------------|-------------|
| **key_luma8** | 8 | Luminance (black to color) | Grayscale + hue |
| **key_luma8w** | 8 | Luminance (white to color) | Inverted grayscale + hue |
| **key_luma8x** | 8 | Luminance extended range | Enhanced contrast |
| **key_hsv8** | 8 | HSV (hue 4-bit, sat/val 4-bit) | Polar color wheel |
| **key_hsv16** | 16 | HSV (hue 8-bit, sat/val 8-bit) | Full HSV |
| **key_hsv16w** | 16 | HSV white variant | Inverted saturation |
| **key_hsv16x** | 16 | HSV extended range | Enhanced contrast |
| **key_rgb8** | 8 | RGB (3:3:2) | Direct RGB |
| **key_rgb16** | 16 | RGB (5:6:5) | High-color RGB |
| **key_rgb24** | 24 | RGB (8:8:8) | True-color RGB |

### 7.2 Luminance Modes (LUMA8, LUMA8W, LUMA8X)

**DebugDisplayUnit.pas:3105-3142** — note the case label is **shared with the RGBI8 family**;
the branch is transcribed here verbatim:
```pascal
    key_luma8,
    key_luma8w,
    key_luma8x,
    key_rgbi8,
    key_rgbi8w,
    key_rgbi8x:
    begin
      if mode in [key_luma8, key_luma8w, key_luma8x] then
      begin
        v := vColorTune and 7;                            // color selection (0-7)
        p := p and $FF;                                   // 8-bit luminance value
      end
      else
      begin
        v := p shr 5 and 7;                               // (RGBI8: tint from the value itself)
        p := p and $1F shl 3 or p and $1C shr 2;
      end;
      // white flag FIRST — computed from the UN-rescaled p
      w := (mode in [key_luma8w, key_rgbi8w]) or (mode in [key_luma8x, key_rgbi8x]) and (v <> 7) and (p >= $80);
      // extended-range rescale SECOND
      if (mode in [key_luma8x, key_rgbi8x]) and (v <> 7) then if (p >= $80) then p := not p and $7F shl 1 else p := p shl 1;
      if w then
      begin   // from white to color
        if v = 0 then p := (p shl 7 and $007F00 or p) xor $FFFFFF    // orange
        else
        begin
          if v <> 7 then v := v xor 7;
          p := (v shr 2 and 1 * p shl 16 or
                v shr 1 and 1 * p shl 8  or
                v shr 0 and 1 * p shl 0) xor $FFFFFF;
        end;
      end
      else
      begin  // from black to color
        if v = 0 then p := p shl 16 or p shl 7 and $007F00    // orange
        else p := v shr 2 and 1 * p shl 16 or
                  v shr 1 and 1 * p shl 8  or
                  v shr 0 and 1 * p shl 0;
      end;
    end;
```

> ⚠️ **Statement order is load-bearing.** `w` is computed at **3122**, *before* the extended-range
> rescale at **3123** — so the `p >= $80` test in `w` sees the **original** value, not the remapped
> one. Reversing the two statements inverts the `LUMA8X` white/black polarity: e.g. `p = $C0` →
> Pascal gives `w = True` with rescaled `p = $7E`; rescale-first would give `w = False`. Any port
> must emit `w :=` first.

**Color Tuning Values** (vColorTune and 7):

| Value | Color | RGB Channels |
|-------|-------|--------------|
| 0 | Orange | R+G (special case) |
| 1 | Blue | B only |
| 2 | Green | G only |
| 3 | Cyan | G+B |
| 4 | Red | R only |
| 5 | Magenta | R+B |
| 6 | Yellow | R+G |
| 7 | White | R+G+B |

### 7.3 HSV Modes (HSV8, HSV16)

**DebugDisplayUnit.pas:3143-3160** (transcribed verbatim):
```pascal
    key_hsv8,
    key_hsv8w,
    key_hsv8x,
    key_hsv16,
    key_hsv16w,
    key_hsv16x:
    begin
      // expand 8-bit to 16-bit if needed
      if mode in [key_hsv8, key_hsv8w, key_hsv8x] then p := p and $F0 * $110 or p and $0F * $11;
      // look up base color from the polar color wheel
      v := PolarColors[(p shr 8 + vColorTune) and $FF];
      p := p and $FF;                                   // saturation/value
      // white flag FIRST — computed from the UN-rescaled p
      w := (mode in [key_hsv8w, key_hsv16w]) or (mode in [key_hsv8x, key_hsv16x]) and (p >= $80);
      // extended-range rescale SECOND
      if mode in [key_hsv8x, key_hsv16x] then if (p >= $80) then p := p and $7F shl 1 xor $FE else p := p shl 1;
      if w then v := v xor $FFFFFF;
      // blend base color with saturation/value
      p := (v shr 16 and $FF * p + $FF) shr 8 shl 16 or
           (v shr  8 and $FF * p + $FF) shr 8 shl  8 or
           (v shr  0 and $FF * p + $FF) shr 8 shl  0;
      if w then p := p xor $FFFFFF;
    end;
```

> ⚠️ **Same order trap as §7.2, and this is exactly SPECTRO's `HSV16X` path.** `w` is computed at
> **3153**, *before* the extended-range rescale at **3154**. A port that rescales first inverts the
> `HSV16X` white/black polarity.

### 7.4 PolarColors Table

**DebugDisplayUnit.pas:3207-3228**
```pascal
procedure TDebugDisplayForm.SetPolarColors;
const
  tuning = -7.2;  // starts colors exactly at red
var
  i, j: integer;
  k: extended;
  v: array [0..2] of integer;
begin
  for i := 0 to 255 do
  begin
    for j := 0 to 2 do
    begin
      k := i + tuning + j * 256 / 3;
      if k >= 256 then k := k - 256;
      if      k < 256 * 2/6 then v[j] := 0
      else if k < 256 * 3/6 then v[j] := Round((k - 256 * 2/6) / (256 * 3/6 - 256 * 2/6) * 255)
      else if k < 256 * 5/6 then v[j] := 255
      else                       v[j] := Round((256 * 6/6 - k) / (256 * 6/6 - 256 * 5/6) * 255);
    end;
    PolarColors[i] := v[2] shl 16 or v[1] shl 8 or v[0];
  end;
end;
```

**Color Wheel Pattern**: Creates 256-entry table mapping hue angle (0-255) to RGB colors following standard color wheel progression (red → yellow → green → cyan → blue → magenta → red).

---

## 8. Rendering Pipeline

### 8.1 SPECTRO_Draw Method

**DebugDisplayUnit.pas:1836-1857**
```pascal
procedure TDebugDisplayForm.SPECTRO_Draw;
var
  x, p: integer;
  v: int64;
  fScale: Extended;
begin
  // Copy samples from circular buffer to FFT input
  for x := 0 to vSamples - 1 do
    FFTsamp[x] := SPECTRO_SampleBuff[(SamplePtr - vSamples + x) and SPECTRO_PtrMask];

  // Perform FFT
  PerformFFT;

  // Calculate scaling factor
  fScale := 255 / vRange;

  // Plot each frequency bin
  for x := FFTfirst to FFTlast do
  begin
    v := FFTpower[x];

    // Apply logarithmic scaling if enabled
    if vLogScale then
      v := Round(Log2(Int64(v) + 1) / Log2(Int64(vRange) + 1) * vRange);

    // Scale to 0-255 range
    p := Round(v * fScale);
    if p > $FF then p := $FF;

    // Add phase information for HSV16 modes
    if vColorMode in [key_hsv16..key_hsv16x] then
      p := p or FFTangle[x] shr 16 and $FF00;

    // Plot pixel and advance trace
    PlotPixel(p);
    if x = FFTlast then BitmapToCanvas(0);  // Capture before scroll
    StepTrace;
  end;
end;
```

### 8.2 Rendering Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Extract sample window from circular buffer               │
│    for x := 0 to vSamples - 1 do                            │
│      FFTsamp[x] := SPECTRO_SampleBuff[...]                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Perform FFT (windowing, transform, magnitude)            │
│    PerformFFT                                                │
│    → FFTpower[0..bins-1] contains magnitudes                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Calculate scaling factor                                 │
│    fScale = 255 / vRange                                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. For each frequency bin (FFTfirst to FFTlast):           │
│    ┌─────────────────────────────────────────────────────┐ │
│    │ a. Get magnitude: v = FFTpower[x]                   │ │
│    └──────────────────┬──────────────────────────────────┘ │
│                       │                                     │
│                       ▼                                     │
│    ┌─────────────────────────────────────────────────────┐ │
│    │ b. Apply log scaling if enabled:                    │ │
│    │    v = log2(v+1) / log2(range+1) × range            │ │
│    └──────────────────┬──────────────────────────────────┘ │
│                       │                                     │
│                       ▼                                     │
│    ┌─────────────────────────────────────────────────────┐ │
│    │ c. Scale to 0-255:                                  │ │
│    │    p = round(v × fScale)                            │ │
│    │    clamp to 0-255                                   │ │
│    └──────────────────┬──────────────────────────────────┘ │
│                       │                                     │
│                       ▼                                     │
│    ┌─────────────────────────────────────────────────────┐ │
│    │ d. Add phase for HSV16 modes:                       │ │
│    │    p |= FFTangle[x] >> 16 & $FF00                   │ │
│    └──────────────────┬──────────────────────────────────┘ │
│                       │                                     │
│                       ▼                                     │
│    ┌─────────────────────────────────────────────────────┐ │
│    │ e. Plot pixel at current trace position             │ │
│    │    PlotPixel(p)                                      │ │
│    └──────────────────┬──────────────────────────────────┘ │
│                       │                                     │
│                       ▼                                     │
│    ┌─────────────────────────────────────────────────────┐ │
│    │ f. Advance trace position (scroll if needed)        │ │
│    │    StepTrace                                         │ │
│    └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Copy bitmap to display buffer (after last bin)          │
│    BitmapToCanvas(0)                                        │
└─────────────────────────────────────────────────────────────┘
```

### 8.3 Logarithmic Scaling

**Formula** (line 1849):
```pascal
v := Round(Log2(Int64(v) + 1) / Log2(Int64(vRange) + 1) * vRange)
```

**Mathematical Form**:
```
v_scaled = log₂(v + 1) / log₂(range + 1) × range
```

**Purpose**: Compress wide dynamic range into displayable range while preserving detail in low-amplitude regions.

**Key point**: `LOGSCALE` rewrites `v` **back into the full 0..vRange domain** (it multiplies by
`vRange`, not by 255); the *same* `p := Round(v * fScale)` at 1850 then maps that to 0..255. So the
log curve is applied **before** the linear scaling, not instead of it.

**Example** (`vRange = 1000` ⇒ `fScale = 255/1000 = 0.255`; `Log2(1001) ≈ 9.9672`):

| Input `v` | Linear — `p = Round(v × 0.255)` | Log — `v' = Round(Log2(v+1)/Log2(1001) × 1000)` | Log — `p = Round(v' × 0.255)` |
|---|---|---|---|
| 1 | `Round(0.255)` = **0** (invisible) | `Log2(2)/9.9672 × 1000 ≈ 100.3` → **100** | `Round(25.5)` = **26** (now visible) |
| 100 | `Round(25.5)` = **26** (dim) | `Log2(101)/9.9672 × 1000 ≈ 668.0` → **668** | `Round(170.3)` = **170** (much brighter) |
| 1000 | `Round(255)` = **255** (max) | `Log2(1001)/9.9672 × 1000` = **1000** | **255** (max) |

The endpoints are fixed (`v = 0 → 0`, `v = vRange → 255`); everything between is lifted.

### 8.4 PlotPixel Method

**DebugDisplayUnit.pas:3433-3444**
```pascal
procedure TDebugDisplayForm.PlotPixel(p: integer);
var
  v: integer;
  line: PByteArray;
begin
  p := TranslateColor(p, vColorMode);  // Convert to RGB24
  line := BitmapLine[vPixelY];         // Get scanline pointer
  v := vPixelX * 3;                    // Byte offset (3 bytes/pixel)
  line[v+0] := p shr 0;                // Blue
  line[v+1] := p shr 8;                // Green
  line[v+2] := p shr 16;               // Red
end;
```

**Direct Pixel Writing**: Writes RGB24 directly to bitmap scanline for maximum performance (no GDI overhead).

---

## 9. Trace System and Scrolling

### 9.1 Trace Modes

The **vTrace** parameter controls both trace direction and scrolling behavior:

**Bit Encoding**:
- **Bits 0-2**: Direction (0-7)
- **Bit 3**: Scroll enable (0=wrap, 1=scroll)

**Direction Modes**:

| Mode | Direction | Primary Axis | Secondary Axis | Typical Use |
|------|-----------|--------------|----------------|-------------|
| **0** | Left-to-right, top-to-bottom | X+ | Y+ | Horizontal waterfall (downward) |
| **1** | Right-to-left, top-to-bottom | X- | Y+ | Horizontal waterfall reversed |
| **2** | Left-to-right, bottom-to-top | X+ | Y- | Horizontal waterfall (upward) |
| **3** | Right-to-left, bottom-to-top | X- | Y- | Horizontal waterfall reversed up |
| **4** | Top-to-bottom, left-to-right | Y+ | X+ | Vertical waterfall (rightward) |
| **5** | Bottom-to-top, left-to-right | Y- | X+ | Vertical waterfall reversed |
| **6** | Top-to-bottom, right-to-left | Y+ | X- | Vertical waterfall (leftward) |
| **7** | Bottom-to-top, right-to-left | Y- | X- | Vertical waterfall reversed left |

**Scroll Modes**:
- **vTrace = 0-7**: Wrap-around (no scrolling)
- **vTrace = 8-15**: Bitmap scrolling enabled

**Default**: vTrace = $F (15) = mode 7 with scrolling

### 9.2 SetTrace Method

**DebugDisplayUnit.pas:2973-2980** (`SetTrace`)
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

**Initial Position Logic**:
- **Modes 0, 2, 4, 5**: Start at X=0
- **Modes 1, 3, 6, 7**: Start at X=width-1
- **Modes 0, 1, 4, 6**: Start at Y=0
- **Modes 2, 3, 5, 7**: Start at Y=height-1

### 9.3 StepTrace Method

**DebugDisplayUnit.pas:2982-3061** (`StepTrace`; excerpt for mode 0)
```pascal
procedure TDebugDisplayForm.StepTrace;
var
  Scroll: boolean;
begin
  Scroll := vTrace and 8 <> 0;
  case vTrace and 7 of
    0:  // Left-to-right, top-to-bottom
    begin
      if vPixelX <> vWidth - 1 then
        Inc(vPixelX)
      else
      begin
        vPixelX := 0;
        if Scroll then
          ScrollBitmap(0, 1)      // Scroll down 1 line
        else if vPixelY <> vHeight - 1 then
          Inc(vPixelY)
        else
          vPixelY := 0;
      end;
    end;
    // ... other modes
  end;
end;
```

**Behavior**:
1. **Advance primary axis** until edge reached
2. **At edge**: Reset primary, advance secondary
3. **If scroll enabled**: Call ScrollBitmap
4. **If wrap mode**: Advance secondary or wrap to start

### 9.4 ScrollBitmap Method

**DebugDisplayUnit.pas:3446-3481**
```pascal
procedure TDebugDisplayForm.ScrollBitmap(x, y: integer);
var
  xm, ym: integer;
  src, dst: TRect;
begin
  // Determine pixel multiplier
  if vSparse = -1 then
  begin
    xm := 1;
    ym := 1;
  end
  else
  begin
    xm := vDotSize;
    ym := vDotSizeY;
  end;

  // Copy bitmap contents shifted by (x, y)
  src := Rect(0, 0, vWidth * xm, vHeight * ym);
  dst := Rect(x * xm, y * ym, (vWidth + x) * xm, (vHeight + y) * ym);
  Bitmap[0].Canvas.CopyRect(dst, Bitmap[0].Canvas, src);

  // Fill exposed area with background
  Bitmap[0].Canvas.Brush.Color := WinRGB(GetBackground);
  if x <> 0 then
  begin
    if x < 0 then
      dst := Rect((vWidth + x) * xm, 0, vWidth * xm, vHeight * ym)
    else
      dst := Rect(0, 0, x * xm, vHeight * ym);
    Bitmap[0].Canvas.FillRect(dst);
  end;
  if y <> 0 then
  begin
    if y < 0 then
      dst := Rect(0, (vHeight + y) * ym, vWidth * xm, vHeight * ym)
    else
      dst := Rect(0, 0, vWidth * xm, y * ym);
    Bitmap[0].Canvas.FillRect(dst);
  end;
end;
```

**Scroll Operation**:
1. **Copy entire bitmap** shifted by (x, y) pixels
2. **Fill exposed area** (edge strip) with background color

**Example** (y=1, downward scroll):
- Copy entire bitmap from (0,0) to (0,1)
- Fill top line (0,0) to (width,1) with background
- Next pixel plots at top edge, pushing history down

---

## 10. Rate Control System

### 10.1 RateCycle Function

**DebugDisplayUnit.pas:3079-3088**
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

**Purpose**: Throttle display updates to reduce processing load and control scrolling speed.

**Behavior**:
- Increments counter on each sample
- Returns `True` every **vRate** samples
- Resets counter to 0

**Default Rate** (line 1778):
```pascal
if vRate = 0 then vRate := vSamples div 8;  // samples/8
```

**Example** (512-point FFT):
- Default vRate = 512 / 8 = 64
- Display updates every 64 samples
- At 8000 Hz sample rate: 8000/64 = 125 updates/sec

### 10.2 Rate Control in Update Loop

**DebugDisplayUnit.pas:1829**
```pascal
if RateCycle then SPECTRO_Draw;
```

**Flow**:
```
Sample arrives → Store in buffer → Buffer full? → Rate cycle? → Draw
                                         ↓              ↓
                                        No            No
                                         ↓              ↓
                                       Wait          Wait
```

### 10.3 Rate Configuration

**Configuration** (line 1757-1758):
```pascal
key_rate:
  KeyValWithin(vRate, 1, FFTmax);
```

**Range**: 1 to 2048 samples per update

**Performance Impact**:
- **vRate = 1**: Update every sample (maximum CPU load)
- **vRate = 8**: Update every 8 samples (fast scrolling)
- **vRate = 64**: Update every 64 samples (moderate, default-ish)
- **vRate = 512**: Update every 512 samples (slow scrolling)

---

## 11. Data Packing System

The SPECTRO display uses the same 12-mode data packing system as other displays for efficient serial transmission.

### 11.1 Packing Modes

**DebugDisplayUnit.pas:140-152**
```pascal
  PackDef               : array [key_longs_1bit..key_bytes_4bit] of integer = (
                          0 shl 16 +  1 shl 8 + 32,   // key_longs_1bit:  shift=1,  count=32
                          0 shl 16 +  2 shl 8 + 16,   // key_longs_2bit:  shift=2,  count=16
                          0 shl 16 +  4 shl 8 + 8,    // key_longs_4bit:  shift=4,  count=8
                          0 shl 16 +  8 shl 8 + 4,    // key_longs_8bit:  shift=8,  count=4
                          0 shl 16 + 16 shl 8 + 2,    // key_longs_16bit: shift=16, count=2
                          0 shl 16 +  1 shl 8 + 16,   // key_words_1bit:  shift=1,  count=16
                          0 shl 16 +  2 shl 8 + 8,    // key_words_2bit:  shift=2,  count=8
                          0 shl 16 +  4 shl 8 + 4,    // key_words_4bit:  shift=4,  count=4
                          0 shl 16 +  8 shl 8 + 2,    // key_words_8bit:  shift=8,  count=2
                          0 shl 16 +  1 shl 8 + 8,    // key_bytes_1bit:  shift=1,  count=8
                          0 shl 16 +  2 shl 8 + 4,    // key_bytes_2bit:  shift=2,  count=4
                          0 shl 16 +  4 shl 8 + 2);   // key_bytes_4bit:  shift=4,  count=2
```

> ⚠️ **There is no per-mode sign flag.** Every `PackDef` entry encodes `0 shl 16`; the
> `shl 16` field is always zero and is **never read** — `SetPack` (4146-4156) consumes only
> `i shr 8 and $FF` (shift) and `i and $FF` (count), and takes `signx` as a *parameter*.
> Sign-extension is a **runtime flag** set only by a trailing `SIGNED` keyword (§11.2).

**Default packing is UNPACKED.** `SetDefaults` (2915) calls `SetPack(0, False, False)`,
and `SetPack` special-cases `val = 0` (4152-4155) — bypassing `PackDef` entirely:
`vPackShift = 32`, `vPackCount = 1`, `vPackMask = $FFFFFFFF` ⇒ **one full 32-bit sample per
transmitted long.** A packing mode is only ever in effect if a packing keyword appears in
`SPECTRO_Configure` (1773-1774). Packing is **fixed at window creation** — the pack keys
appear only in the configure loop, never in `SPECTRO_Update`.

### 11.2 Packing Table and the `ALT` / `SIGNED` modifiers

Each packing keyword may be followed by **`ALT` and/or `SIGNED`** — both optional, either
order, up to two (`KeyPack`, 2817-2832):

```pascal
2822:  v := val;
2823:  alt := False;
2824:  signx := False;
2825:  if NextKey and (val in [key_alt, key_signed]) then
2826:  begin
2827:    if val = key_alt then alt := True else signx := True;
2828:    if NextKey and (val in [key_alt, key_signed]) then
2829:      if val = key_alt then alt := True else signx := True;
2830:  end;
2831:  SetPack(v, alt, signx);
```

| Mode | Bits/Sample | Samples/Long | Bandwidth Multiplier |
|------|-------------|--------------|----------------------|
| **LONGS_1BIT** | 1 | 32 | 32× |
| **LONGS_2BIT** | 2 | 16 | 16× |
| **LONGS_4BIT** | 4 | 8 | 8× |
| **LONGS_8BIT** | 8 | 4 | 4× |
| **LONGS_16BIT** | 16 | 2 | 2× |
| **WORDS_1BIT** | 1 | 16 | 16× |
| **WORDS_2BIT** | 2 | 8 | 8× |
| **WORDS_4BIT** | 4 | 4 | 4× |
| **WORDS_8BIT** | 8 | 2 | 2× |
| **BYTES_1BIT** | 1 | 8 | 8× |
| **BYTES_2BIT** | 2 | 4 | 4× |
| **BYTES_4BIT** | 4 | 2 | 2× |

**Sign Extend** — deliberately *not* a column above: it is **never implied by the mode**. Every
mode is **unsigned** unless the directive carries a trailing `SIGNED` keyword, which sets the
runtime flag `vPackSignx` consumed by `UnPack` (4170). `LONGS_4BIT` alone is unsigned;
`LONGS_4BIT SIGNED` is signed (range −8..+7).

**`ALT`** sets `vPackAlt`, consumed by `NewPack` (4158-4164):

```pascal
4158:  function TDebugDisplayForm.NewPack: integer;
4159:  begin
4160:    Result := val;
4161:    if vPackAlt and (vPackShift <= 1) then Result := Result shr 1 and $55555555 or Result shl 1 and $AAAAAAAA;
4162:    if vPackAlt and (vPackShift <= 2) then Result := Result shr 2 and $33333333 or Result shl 2 and $CCCCCCCC;
4163:    if vPackAlt and (vPackShift <= 4) then Result := Result shr 4 and $0F0F0F0F or Result shl 4 and $F0F0F0F0;
4164:  end;
```

The three guards are **cumulative**, not exclusive:

- **1-bit modes** (`vPackShift = 1`): **all three fire** ⇒ each byte's 8 bits are **fully
  reversed** (`$01 → $80`). It is *not* a stage-1 adjacent-bit swap.
- **2-bit modes**: only the pair-swap and nibble-swap apply.
- **4-bit modes**: only the nibble-swap applies.
- **8- and 16-bit modes**: `ALT` is a **no-op** (all three guards fail).

Note also that `NewPack` **does not read the element stream** — it begins `Result := val;`,
reusing the value already latched by the enclosing `while NextNum do` (`SPECTRO_Update`, 1818-1821).
It consumes nothing and advances nothing.

### 11.3 UnPack Method

**DebugDisplayUnit.pas:4166-4171**
```pascal
function TDebugDisplayForm.UnPack(var v: integer): integer;
begin
  Result := v and vPackMask;
  v := v shr vPackShift;
  if vPackSignx and (Result shr (vPackShift - 1) and 1 = 1) then
    Result := Result or ($FFFFFFFF xor vPackMask);
end;
```

**Operation**:
1. Extract the **lowest** sub-field first (mask)
2. Shift the packed value right
3. Sign-extend **only if** `vPackSignx` is set (i.e. `SIGNED` was given) **and** the extracted
   sub-field's own top bit (`Result shr (vPackShift − 1) and 1`) is 1

**Example** (`LONGS_4BIT SIGNED` — `vPackShift = 4`, so the sign test is `Result shr 3 and 1`;
signed range is **−8..+7**):
- Packed: `$87654321`
- Sample 1: `$1` → bit 3 = 0 → **no** sign-extend → `$00000001` (+1)
- Sample 2: `$2` → bit 3 = 0 → `$00000002` (+2)
- Sample 3: `$3` → bit 3 = 0 → `$00000003` (+3)
- Sample 4: `$4` → bit 3 = 0 → `$00000004` (+4)
- Sample 5: `$5` → bit 3 = 0 → `$00000005` (+5)
- Sample 6: `$6` → bit 3 = 0 → `$00000006` (+6)
- Sample 7: `$7` → bit 3 = 0 → `$00000007` (+7)
- Sample 8: `$8` → bit 3 = 1 → **sign-extend** → `$FFFFFFF8` (−8)

Without the `SIGNED` keyword the same long yields the unsigned samples +1 … +8.

---

## 12. Window Management

### 12.1 Bitmap System

SPECTRO uses **double-buffering** for flicker-free display:

**Buffers**:
- **Bitmap[0]**: Render target (drawing buffer)
- **Bitmap[1]**: Display buffer (shown on screen)

**Rendering Flow**:
```
Plot pixels → Bitmap[0] → BitmapToCanvas(0) → Bitmap[1] → Screen
```

### 12.2 BitmapToCanvas Method

Copies Bitmap[0] to Bitmap[1] and triggers screen refresh.

**Timing** (line 1854):
```pascal
if x = FFTlast then BitmapToCanvas(0);  // Capture just before scroll
```

**Important**: Bitmap captured **before** final StepTrace to avoid tearing artifacts during scroll.

### 12.3 Window Size Calculation

**SetSize Call** (line 1788):
```pascal
SetSize(0, 0, 0, 0);
```

**Default window size**: with all defaults (depth `vWidth = 256` from `SetDefaults`,
FFT 512 → bins `vHeight = FFTlast − FFTfirst + 1 = 256`, `vTrace = $F` so bit 2 is set
→ **no** width/height swap, `vDotSize = vDotSizeY = 1`), the client area is **256 × 256
px**. (The §4 example uses `depth=300, trace=0`, which *does* swap — that is an example,
not the default.)

**Font size**: SPECTRO renders **no text labels** — `SPECTRO_Configure` does not set
`vTextSize`, so it stays at `DefaultTextSize = 10` (`SetDefaults`, 2894), and SPECTRO
exposes **no `TEXTSIZE` directive**. The value is effectively unused.

**Actual Size Determined By**:
- **vWidth**: Frequency bins (after swap) or time depth
- **vHeight**: Time depth (after swap) or frequency bins
- **vDotSize**: Horizontal pixel scaling
- **vDotSizeY**: Vertical pixel scaling

**Pixel Dimensions**:
```
PixelWidth = vWidth × vDotSize
PixelHeight = vHeight × vDotSizeY
```

**Example**:
- 512-point FFT, bins 0-255, depth=300, trace=0, dotsize=2×3
- vWidth=256, vHeight=300 (after swap)
- Display: 512×900 pixels

---

## 13. Command Protocol

### 13.1 Configuration Command

**Format** (element array). Element `[0]` is the **display type** (`ele_dis`) and `[1]` the
**window name** (`ele_nam`); directives begin at `ptr := 2` (`FormCreate`:625-632). There is
exactly **one** terminating `ele_end`:
```
[0] ele_dis, dis_spectro,
[1] ele_nam, "MySpec",
    ele_key, key_title,   ele_str, "title text",
    ele_key, key_samples, ele_num, fft_size,
    ele_key, key_depth,   ele_num, time_depth,
    ele_key, key_mag,     ele_num, magnification,
    ele_key, key_range,   ele_num, max_magnitude,
    ele_key, key_rate,    ele_num, update_rate,
    ele_key, key_trace,   ele_num, trace_mode,
    ele_key, key_dotsize, ele_num, x_scale, ele_num, y_scale,
    ele_key, key_luma8x,  // or another of the six accepted color modes; may take a tune operand
    ele_key, key_logscale,
    ele_end
```

> ⚠️ **The configure phase is KEY-ONLY** (`while NextKey do`, 1735). A non-key element — a stray
> string or a bare number — **terminates the configure parse**, and the remainder of the create
> message is silently dropped. Do not put update-phase directives or bare data in a create message.

### 13.2 Update Command

**Format**:
```
ele_num, sample1, ele_num, sample2, ..., ele_end
```

**Or with packing** — note the packing mode is selected **in the CREATE message**, not here:
```
' create message (SPECTRO_Configure, 1773-1774):
ele_key, key_longs_4bit, ele_end        // + optional ALT / SIGNED keys

' subsequent update messages carry only the packed numbers:
ele_num, packed_value1,   // contains 8 samples
ele_num, packed_value2,
..., ele_end
```

> ⚠️ **Packing cannot be changed mid-stream.** `SPECTRO_Update`'s case statement (1800-1815) has
> arms for `key_clear` / `key_save` / `key_pc_key` / `key_pc_mouse` **only** — a `key_longs_*` /
> `key_words_*` / `key_bytes_*` element arriving in an update message matches no arm and is
> **silently skipped**. The mode set at create time stays in force for the life of the window.

### 13.3 Control Commands

**Clear Display**:
```
ele_key, key_clear, ele_end
```

**Save Image** — the filename is **required** for a file to be written (`KeySave`, 2839-2865):
```
ele_key, key_save, ele_str, "filename", ele_end      → writes Bitmap[1] to filename.bmp (2843)
```

Alternate forms (desktop scrape via `BitBlt`, 2861-2864):
```
ele_key, key_save, ele_key, key_window, ele_str, "filename", ele_end   → whole window incl. title bar/borders
ele_key, key_save, ele_num, l, ele_num, t, ele_num, w, ele_num, h,
                   ele_str, "filename", ele_end                        → arbitrary screen region
```

> ⚠️ `ele_key, key_save, ele_end` (bare `SAVE`) is **non-functional**: `NextStr` fails, `NextKey`
> fails, `KeyVal(l)` fails → `Exit`. **Nothing is written.**

**Close Window**:
```
ele_key, key_close, ele_end     → parser-layer dispatch (p2com.asm); command messages only
```

---

## 14. Usage Examples

### 14.1 Basic Audio Spectrogram

**Goal**: Display audio frequency spectrum over time.

**Configuration**:
```
SPECTRO
  SAMPLES 1024       ' 1024-point FFT (512 bins, numbered 0..511 — FFTlast := vSamples div 2 - 1, 1747)
  DEPTH 400          ' 400 pixels of time history
  RATE 128           ' Update every 128 samples
  TRACE 8            ' Left-to-right, scrolling down
  LUMA8X             ' Extended luminance coloring
  DOTSIZE 2 1        ' 2× horizontal scaling
```

**Data Stream** (at 8000 Hz):
```
Sample stream: s0, s1, s2, s3, ...
Updates every 128 samples (62.5 updates/sec)
Display scrolls down showing newest at top
```

**Interpretation**:
- Horizontal: 0-4000 Hz (Nyquist frequency)
- Vertical: Time (newest at top, scrolling down)
- Brightness: Signal magnitude

### 14.2 Wideband vs. Narrowband

**Wideband** (time resolution):
```
SAMPLES 128        ' Small FFT
RATE 16            ' Frequent updates
DEPTH 1000         ' Long history
```
- **Good for**: Transients, rhythm, time-domain events
- **Poor for**: Frequency resolution

**Narrowband** (frequency resolution):
```
SAMPLES 2048       ' Large FFT
RATE 512           ' Infrequent updates
DEPTH 200          ' Shorter history
```
- **Good for**: Pitch tracking, harmonics, frequency detail
- **Poor for**: Time resolution

### 14.3 HSV Phase Display

**Goal**: Show both magnitude and phase using color.

**Configuration**:
```
SPECTRO
  SAMPLES 512
  HSV16X             ' 16-bit HSV with phase
  RANGE $10000       ' Moderate dynamic range
```

**Data Interpretation**:
- **Brightness**: Magnitude (0=black, 255=bright)
- **Hue**: Phase angle (0-255 maps to 0-360°)
- **Use**: Identify phase relationships between harmonics

### 14.4 Vibration Analysis

**Goal**: Monitor mechanical vibration spectrum.

**Configuration**:
```
SPECTRO
  SAMPLES 512
  DEPTH 500
  MAG 4              ' 16× magnification for low-level signals
  LOGSCALE           ' Logarithmic magnitude
  LUMA8 CYAN         ' Cyan coloring
  TRACE 12           ' Vertical scrolling right
```

**Interpretation**:
- Horizontal: Time
- Vertical: 0-Nyquist frequency
- Persistent harmonics visible as vertical lines
- Transients visible as horizontal bursts

### 14.5 Packed Data Transmission

**Goal**: Efficient transmission of 8-bit audio.

**Configuration**:
```
SPECTRO
  SAMPLES 512
  LONGS_8BIT SIGNED  ' 4 samples per long; SIGNED because the audio samples are signed
```

Without the trailing `SIGNED`, `UnPack` leaves each 8-bit field **unsigned** (0..255) —
`LONGS_8BIT` alone carries **no** sign flag (§11.2).

**Propeller 2 Code** — packing keeps the *first* sample in the **low** field, because `UnPack`
yields the low sub-field first (4168):
```spin2
' Pack 4 8-bit samples into one long
packed := (sample1 << 0) | (sample2 << 8) | (sample3 << 16) | (sample4 << 24)
debug(`MySpec `UDEC_(packed))      ' feed by INSTANCE name, not by display type
```
(The window must first be declared, e.g. `` debug(`SPECTRO MySpec SAMPLES 512 LONGS_8BIT SIGNED) ``;
feeding `` `SPECTRO `` — the *type* keyword — does not address a window.)

**Bandwidth**: 4× reduction vs. sending individual samples.

---

## 15. Performance Characteristics

### 15.1 Computational Complexity

**FFT Complexity**: O(N log N)

**Operation Counts** (512-point FFT):
- **Butterfly operations**: 512 × log₂(512) = 512 × 9 = 4,608
- **Complex multiplications**: ~2,304
- **Per update**: ~10,000-15,000 operations

**Windowing**: O(N) = 512 operations

**Total per FFT**: ~15,000 operations

### 15.2 Update Rate Analysis

**Frame Rate Calculation**:
```
Sample rate: fs (Hz)
FFT size: N samples
Rate divisor: R samples/update

Update rate = fs / R (updates/sec)
Time between updates = R / fs (seconds)
```

**Example** (8 kHz, 512-point, rate=64):
- Update rate = 8000 / 64 = 125 Hz
- Time between = 64 / 8000 = 8 ms

**Typical Rates**:
- **Audio (real-time)**: 30-120 Hz (smooth scrolling)
- **Instrumentation**: 10-50 Hz (analysis)
- **Slow events**: 1-10 Hz (long-term monitoring)

### 15.3 Memory Bandwidth

**Per Update**:
- **Sample buffer writes**: N × 4 bytes
- **FFT reads**: N × 4 bytes
- **FFT computation**: ~6N × 8 bytes (int64 arrays)
- **Pixel writes**: bins × 3 bytes (RGB)

**Example** (512-point):
- Sample writes: 512 × 4 = 2 KB
- FFT reads: 512 × 4 = 2 KB
- FFT computation: ~24 KB
- Pixel writes: 256 × 3 = 768 bytes
- **Total**: ~29 KB per update

**At 125 Hz**: 29 KB × 125 = 3.6 MB/sec

### 15.4 Display Bandwidth

**Scrolling Overhead**:
- **Bitmap copy**: width × height × 3 bytes per scroll
- **Example** (256×300): 256 × 300 × 3 = 230 KB per scroll

**At 125 Hz with 1-pixel scroll per update**: 230 KB × 125 = 28.75 MB/sec

**Optimization**: Scrolling handled by GPU (CopyRect), not CPU-intensive.

---

## 16. Comparison with FFT Display

### 16.1 Key Differences

| Aspect | FFT Display | SPECTRO Display |
|--------|-------------|-----------------|
| **Visualization** | Single snapshot | Time-scrolling waterfall |
| **Horizontal axis** | Frequency | Frequency (trace 0-3) or Time (trace 4-7) |
| **Vertical axis** | Magnitude | Time (trace 0-3) or Frequency (trace 4-7) |
| **Magnitude encoding** | Y-position (line graph) | Color intensity (heat map) |
| **Time history** | None (single frame) | Configurable depth |
| **Scrolling** | No | Yes (8 directions) |
| **Update behavior** | Redraw entire display | Add one line, scroll |
| **Multi-channel** | Yes (8 overlaid traces) | No (single channel) |
| **Phase display** | Optional overlay | HSV16 color encoding |
| **Typical use** | Real-time spectrum analyzer | Time-frequency analysis |

### 16.2 Shared Components

Both displays share:
- **FFT processing** (PrepareFFT, PerformFFT)
- **Data packing system** (SetPack, UnPack)
- **Sample buffer** (SPECTRO_SampleBuff vs. Y_SampleBuff)
- **Color mapping** (TranslateColor)
- **Magnification control** (FFTmag)
- **Frequency range selection** (FFTfirst, FFTlast)
- **Logarithmic scaling** (vLogScale)

### 16.3 When to Use Which

**Use FFT Display When**:
- Real-time spectrum monitoring needed
- Multiple channels compared simultaneously
- Precise magnitude measurement required
- Cursor readout needed
- Static spectrum analysis

**Use SPECTRO Display When**:
- Time evolution important
- Pattern recognition in time-frequency space
- Harmonic tracking over time
- Transient detection
- Recording/playback analysis
- Musical note visualization

---

## 17. Implementation Details

### 17.1 Fixed-Point Arithmetic

**FFT Coefficient Scaling** (lines 4187-4189):
```pascal
FFTsin[i] := Round(Yf * $1000);    // Scale by 4096
FFTcos[i] := Round(Xf * $1000);
FFTwin[i] := Round(w * $1000);
```

**Butterfly Computation** (lines 4224-4225):
```pascal
rx := (bx * FFTcos[th] - by * FFTsin[th]) div $1000;
ry := (bx * FFTsin[th] + by * FFTcos[th]) div $1000;
```

**Precision**: 12 bits fractional (1/4096 resolution)

**Range**: ±$7FFFFFFF / $1000 ≈ ±524,288

### 17.2 Bit-Reversal Indexing

**Purpose**: FFT algorithm requires bit-reversed input order.

**Implementation**: Rev32 function reverses bits of input index.

**Example** (8-point FFT):
```
Normal:  0 1 2 3 4 5 6 7
Reversed: 0 4 2 6 1 5 3 7
```

**Application** (line 4245):
```pascal
i2 := Rev32(i1) shr (32 - FFTexp);
```

Reverses only the significant bits (FFTexp bits).

### 17.3 Hanning Window

**Formula** (line 4189):
```pascal
FFTwin[i] := Round((1 - Cos((i / (1 shl FFTexp)) * Pi * 2)) * $1000)
```

**Standard Form**:
```
w[n] = 0.5 × (1 - cos(2πn / N))
```

**Implementation Form** (scaled by 2):
```
w[n] = 1 - cos(2πn / N)
```

**Purpose**: Reduce spectral leakage by tapering window edges to zero.

**Effect**: Main lobe widened slightly, sidelobes reduced >30 dB.

### 17.4 Magnitude Calculation

**Hypot Function** (line 4248):
```pascal
FFTpower[i1] := Round(Hypot(rx, ry) / ($800 shl FFTexp shr FFTmag));
```

**Magnitude**:
```
magnitude = √(real² + imag²)
```

**Scaling Factor**:
```
scale = $800 << FFTexp >> FFTmag
      = 2048 × 2^FFTexp / 2^FFTmag
```

**Example** (512-point, mag=0):
- scale = 2048 × 512 / 1 = 1,048,576
- Full-scale input → magnitude ≈ 1,048,576
- Scaled to 0-$7FFFFFFF range

### 17.5 Phase Calculation

**ArcTan2 Function** (line 4249):
```pascal
FFTangle[i1] := Round(ArcTan2(rx, ry) / (Pi * 2) * $100000000) and $FFFFFFFF;
```

**Phase Angle**:
```
angle = atan2(real, imag) / (2π) × 2^32
```

**Output**: 32-bit unsigned (0 to $FFFFFFFF maps to 0 to 2π radians)

**HSV16 Encoding** (line 1852):
```pascal
if vColorMode in [key_hsv16..key_hsv16x] then
  p := p or FFTangle[x] shr 16 and $FF00;
```

**Result**: Lower 8 bits = magnitude, upper 8 bits = phase angle (hue).

---

## 18. Element Array Protocol Specification

### 18.1 Protocol Overview

SPECTRO uses the standard element array protocol for configuration and data transmission.

**Element Storage**:
```pascal
DebugDisplayType:  array[0..DebugDisplayLimit - 1] of integer;
DebugDisplayValue: array[0..DebugDisplayLimit - 1] of integer;
```

### 18.2 SPECTRO Configuration Example

SPECTRO has **no** `SIZE`, `LOGSIZE`, or `LUTCOLORS` directives — those keys are
not handled by `SPECTRO_Configure` (lines 1735-1775). FFT size is set with
`SAMPLES`, time depth with `DEPTH`, and color via the restricted color-mode set.
A representative configuration element array is:

```
Element Array (directives begin at ptr := 2; [0] = ele_dis, [1] = ele_nam — FormCreate:625-632):
[0] type=ele_dis   value=dis_spectro   → display type
[1] type=ele_nam   value="MySpec"      → window name
[2] type=ele_key   value=key_samples   → SAMPLES
[3] type=ele_num   value=512           → 512-point FFT (FFTexp = 9, bins 0..255)
[4] type=ele_key   value=key_depth     → DEPTH
[5] type=ele_num   value=400           → 400 time-history lines (vWidth)
[6] type=ele_key   value=key_trace     → TRACE
[7] type=ele_num   value=$F            → direction 7 + scroll (KeyVal → vTrace)
[8] type=ele_key   value=key_luma8x    → LUMA8X color mode
[9] type=ele_end   value=0
```

`SAMPLES` passes its first numeric value through `Within(val, 4, FFTmax)` and
`Trunc(Log2(...))` to derive `FFTexp` (line 1744); optional first/last bin values
follow. See `SPECTRO_Configure` lines 1741-1750.

### 18.3 SPECTRO Sample Data Example

```
Element Array:
[0] type=ele_num   value=$12345678       → packed samples
[1] type=ele_num   value=$9ABCDEF0       → packed samples
[2] type=ele_end   value=0
```

---

## 19. Buffer Management and Timing

### 19.1 Sample Buffer

**DebugDisplayUnit.pas:363**
```pascal
SPECTRO_SampleBuff: array [0..SPECTRO_Samples - 1] of integer;  // 2048 samples
```

**Circular Buffer**: Stores time-domain samples before FFT processing. Indexed
by `SamplePtr` advanced with `and SPECTRO_PtrMask` (= 2047). `SamplePop` tracks
fill level up to `vSamples`; the buffer is "full" once `SamplePop = vSamples`
(`SPECTRO_Update` lines 1825-1828).

### 19.2 FFT Processing Flow

```
1. Collect samples in circular buffer (SPECTRO_Update, 1818-1830)
2. Buffer full (SamplePop = vSamples) and RateCycle true → SPECTRO_Draw (1828-1829)
3. Copy newest vSamples into FFTsamp, perform FFT (SPECTRO_Draw 1842-1844)
4. Magnitude/phase produced in FFTpower/FFTangle (PerformFFT)
5. Scale + (optional) log + (HSV16) phase, TranslateColor (SPECTRO_Draw 1846-1852)
6. PlotPixel writes one bin per pixel at vPixelX,vPixelY (3433-3444)
7. StepTrace advances/scrolls the bitmap for the waterfall effect (2982-3061)
```

### 19.3 Scrolling Mechanics

There is **no** `vScroll` variable in v55. Scrolling is driven entirely by the
`vTrace` bit-field via `StepTrace` (lines 2982-3061): `vTrace and 7` selects one
of 8 directions and `vTrace and 8` enables bitmap scrolling. The eight directions
and their scroll vectors (the `ScrollBitmap(x, y)` call each emits) are:

| `vTrace and 7` | Primary advance | Scroll call at edge |
|---|---|---|
| 0 | X+ then Y+ | `ScrollBitmap(0, 1)` (down) |
| 1 | X− then Y+ | `ScrollBitmap(0, 1)` (down) |
| 2 | X+ then Y− | `ScrollBitmap(0, -1)` (up) |
| 3 | X− then Y− | `ScrollBitmap(0, -1)` (up) |
| 4 | Y+ then X+ | `ScrollBitmap(1, 0)` (right) |
| 5 | Y− then X+ | `ScrollBitmap(1, 0)` (right) |
| 6 | Y+ then X− | `ScrollBitmap(-1, 0)` (left) |
| 7 | Y− then X− | `ScrollBitmap(-1, 0)` (left) |

When `vTrace and 8 = 0` (no scroll), the secondary axis wraps instead of
scrolling. `ScrollBitmap` shifts the bitmap by 1 unit and fills the freed edge
strip with background; the next line of bins is then plotted into that strip.

---

## 20. Bitmap System and Double-Buffering

### 20.1 Bitmap Architecture

SPECTRO renders into the shared `Bitmap[0]` (drawing target) and presents via
`BitmapToCanvas(0)` (line 3522). `PlotPixel` writes directly to scanline
pointers cached in `BitmapLine[]` as **RGB24** (3 bytes/pixel: blue, green, red —
`PlotPixel` lines 3441-3443). There is no separate RGBA buffer, and no alpha channel: the
bitmaps are `pf24bit`.

### 20.2 Waterfall Rendering

The real draw loop is `SPECTRO_Draw` (lines 1846-1856): it does **not** call
`ScrollBitmap` directly, and it has no `FFTmag[x]`/`MapToColor` array. Each bin
is read from `FFTpower[x]`, scaled, optionally log-mapped, optionally OR-ed with
phase for HSV16 modes, then `PlotPixel(p)` writes it at the current trace
position. `StepTrace` (called after each pixel) is what advances the position and
issues `ScrollBitmap` at a row/column edge:

```pascal
for x := FFTfirst to FFTlast do
begin
  v := FFTpower[x];
  if vLogScale then v := Round(Log2(Int64(v)+1) / Log2(Int64(vRange)+1) * vRange);
  p := Round(v * fScale);                     // fScale = 255 / vRange
  if p > $FF then p := $FF;
  if vColorMode in [key_hsv16..key_hsv16x] then
    p := p or FFTangle[x] shr 16 and $FF00;   // phase into upper byte
  PlotPixel(p);                                // TranslateColor → RGB24 scanline
  if x = FFTlast then BitmapToCanvas(0);       // capture before final StepTrace
  StepTrace;                                   // advance / ScrollBitmap
end;
```

### 20.3 Color Mapping

SPECTRO does not use a runtime LUT. Color is produced by `TranslateColor(p, vColorMode)`
(called inside `PlotPixel`, line 3438), and `vColorMode` is restricted to the
luminance and 16-bit HSV families only (`key_luma8..key_luma8x`,
`key_hsv16..key_hsv16x`; restriction at `SPECTRO_Configure` line 1767). For the
HSV16 family, `SPECTRO_Draw` packs phase into bits 8-15 of `p` before plotting
(line 1852: `p := p or FFTangle[x] shr 16 and $FF00`), so the byte value carries
both magnitude (low byte) and phase/hue (high byte). The HSV→RGB conversion uses
the precomputed `PolarColors[]` table (built by `SetPolarColors`, lines 3207-3228),
not a magnitude-indexed LUT.

---

## 21. Shared Infrastructure

### 21.1 FFT Engine

SPECTRO shares the same fixed-point FFT engine as FFT display:
- Optimized butterfly operations
- Bit-reversal permutation
- Twiddle factor lookup tables
- Magnitude and phase calculation

### 21.2 Color System

SPECTRO shares the standard color path: `TranslateColor` (3090-3173) plus the
`PolarColors[0..255]` table (declared line 365, built by `SetPolarColors`
lines 3207-3228). There is no `DefaultSpectrumColors` array in v55 —
`PolarColors` is the only precomputed color table, and it serves the HSV color
modes (red→yellow→green→cyan→blue→magenta hue wheel). Luminance modes are
computed arithmetically in `TranslateColor` from `vColorTune` (see §7.2).

Like BITMAP, SPECTRO has **no fixed channel/trace palette** (`DefaultScopeColors`
does not apply). The only fixed color constants are the **background** values
returned by `GetBackground` (`DebugDisplayUnit.pas` 3180–3205), selected by color
mode:

| Color mode | Background | Hex |
|---|---|---|
| LUT1/2/4/8 | `vLut[0]` | (first palette entry) |
| LUMA8/8X, HSV16/16X (and other non-"W" modes) | `clBlack` | `$000000` |
| LUMA8W, HSV16W (white-base "W" modes) | `clWhite` | `$FFFFFF` |

`clBlack`/`clWhite` are literal RGB24 values (`DebugDisplayUnit.pas` 187–188).
(SPECTRO restricts its config color mode to the six LUMA8/HSV16 modes — see §7.1 and the
Directive Reference.)

### 21.3 Data Packing

Uses the standard 12 packing modes:
- `LONGS_1BIT` through `BYTES_4BIT` — all **opt-in**; the default is **unpacked**
  (`SetPack(0, False, False)`, `SetDefaults`:2915) ⇒ one full 32-bit sample per long
- Sign extension **only** when the trailing `SIGNED` keyword is given (`KeyPack`:2825-2830 →
  `vPackSignx`, read at `UnPack`:4170). **No mode is signed by itself** — `PackDef` carries no
  sign flag
- Optional `ALT` modifier reorders bits/nibbles within each long (`NewPack`:4158-4164)
- Efficient unpacking during sample collection (`SPECTRO_Update`:1821-1825)

See §11 for the full table and the `ALT`/`SIGNED` semantics.

---

## 22. Initialization Lifecycle

### 22.1 Configuration Lifecycle

There is no `vLogSize`, `vScroll`, `vLutSize`, `InitializeFFT`, or
`GenerateSpectrumLUT` in v55. Initialization is performed entirely by
`SPECTRO_Configure` (lines 1719-1790) in this real order:

```pascal
// 1. Set unique defaults (1723-1733)
vTrace := $F; vColorMode := key_luma8x; vSamples := fft_default;  // 512
FFTexp := Trunc(Log2(fft_default));                               // 9
FFTfirst := 0; FFTlast := fft_default div 2 - 1;                  // 0..255
FFTmag := 0; vDotSize := 1; vDotSizeY := 1; vRange := $7FFFFFFF;

// 2. Process element-array directives (1735-1775)
while NextKey do case val of ... end;   // SAMPLES/DEPTH/MAG/RANGE/RATE/TRACE/...

// 3. Build FFT tables for the chosen size (1777)
PrepareFFT;                              // sin/cos/Hanning, sized by FFTexp

// 4. Default rate, prime rate counter (1778-1779)
if vRate = 0 then vRate := vSamples div 8;
vRateCount := vRate - 1;

// 5. Compute metrics; swap W/H for horizontal traces (1781-1787)
vHeight := FFTlast - FFTfirst + 1;
if vTrace and $4 = 0 then begin i := vWidth; vWidth := vHeight; vHeight := i; end;

// 6. Allocate/size bitmap + scanline pointers, then set trace origin (1788-1789)
SetSize(0, 0, 0, 0);
SetTrace(vTrace, False);
```

`SetSize` (not a manual `Bitmap[n].SetSize`) establishes the bitmap and
`BitmapLine[]` scanline pointers; `SetTrace` (2973-2980) seeds `vPixelX`/`vPixelY`
to the correct starting corner for the trace direction.

### 22.2 FFT Configuration

FFT size derives from `vSamples`/`FFTexp` set during step 1-2 above. `FFTexp` is
`Trunc(Log2(...))` of the clamped `SAMPLES` value (line 1744); `FFTmag` is the
0..11 magnitude shift from `MAG` (line 1753). `PrepareFFT` (4178-4191) then
fills `FFTsin`/`FFTcos`/`FFTwin` for `1 shl FFTexp` points. There is no separate
`FFTsize` variable — the size is always `1 shl FFTexp` / `vSamples`.

### 22.3 Runtime State

```
[Acquiring]  → SPECTRO_Update stores samples into SPECTRO_SampleBuff (1818-1830)
     ↓ (SamplePop = vSamples AND RateCycle)
[FFT]        → SPECTRO_Draw copies window, calls PerformFFT (1842-1844)
     ↓
[Rendering]  → per bin: scale/log/HSV-phase → PlotPixel → StepTrace (1846-1856)
     ↓
[Display]    → BitmapToCanvas(0) at last bin, before final StepTrace scroll (1854)
     ↓
Loop back to Acquiring
```

---

## 23. Summary

The **SPECTRO** display window provides powerful time-frequency analysis capabilities for the Propeller 2 debug system. Its waterfall visualization makes it ideal for analyzing signals with time-varying frequency content, from audio analysis to vibration monitoring to communications signals.

**Key Strengths**:
- Real-time FFT processing up to 2048 points
- Flexible scrolling in 8 directions
- Rich color mapping for magnitude and phase
- Efficient data packing (up to 32× compression)
- Logarithmic scaling for wide dynamic range
- Configurable time/frequency resolution trade-off

**Performance**: Capable of sustained 100+ Hz update rates with efficient fixed-point FFT implementation and hardware-accelerated bitmap scrolling.

The SPECTRO display complements the FFT display by adding the critical time dimension, enabling visualization of spectral evolution and pattern recognition tasks that would be impossible with static spectrum analysis alone.
