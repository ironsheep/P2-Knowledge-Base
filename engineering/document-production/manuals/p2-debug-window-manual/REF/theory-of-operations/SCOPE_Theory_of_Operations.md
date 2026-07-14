# SCOPE Display Window - Theory of Operations

**Current as of**: PNut v55 for Propeller 2
**Directive coverage verified**: 2026-06-01 against `DebugDisplayUnit.pas` (v55)
**Re-ratified against raw v55 source**: 2026-07-14 — usage/example layer corrected (create-vs-update
phase model, positional channel-def order, packing default, packed-sample distribution, trigger-offset
edge mapping, `SAVE` grammar, `CLOSE`, 24-bit bitmaps, stale citations)
**Companion**: [Debug Window Directive Matrix](../DEBUG-WINDOW-DIRECTIVE-MATRIX.md) — cross-window config/display/keyboard/mouse reference

## Table of Contents

1. [Introduction](#1-introduction)
2. [Architecture Overview](#2-architecture-overview)
3. [Display Type and Constants](#3-display-type-and-constants)
4. [Data Structures](#4-data-structures)
5. [Configuration and Initialization](#5-configuration-and-initialization)
6. [Channel Configuration](#6-channel-configuration)
7. [Auto-Ranging System](#7-auto-ranging-system)
8. [Sample Processing](#8-sample-processing)
9. [Trigger System](#9-trigger-system)
10. [Rendering Pipeline](#10-rendering-pipeline)
11. [Scaling and Positioning](#11-scaling-and-positioning)
12. [User Commands](#12-user-commands)
13. [Performance Characteristics](#13-performance-characteristics)
14. [Comparison with Other Display Types](#14-comparison-with-other-display-types)
15. [Usage Examples](#15-usage-examples)
16. [Implementation Details](#16-implementation-details)
17. [Element Array Protocol Specification](#17-element-array-protocol-specification)
18. [Buffer Management and Timing](#18-buffer-management-and-timing)
19. [Bitmap System and Double-Buffering](#19-bitmap-system-and-double-buffering)
20. [Shared Infrastructure](#20-shared-infrastructure)
21. [Initialization Lifecycle](#21-initialization-lifecycle)
22. [Summary](#22-summary)

---

## 1. Introduction

The **SCOPE** display window is a multi-channel oscilloscope for the Propeller 2 (P2) microcontroller debug environment. It provides real-time visualization of analog signals with features similar to traditional oscilloscope hardware:

- **Up to 8 analog channels** with independent configuration
- **Automatic range detection** (auto-ranging) for each channel
- **Manual scaling control** (low, high, tall, base, grid)
- **Level-based triggering** with rising/falling edge detection
- **Holdoff control** to stabilize display
- **Circular sample buffer** (single interleaved buffer: 2048 sets × 8 channels)
- **Rate limiting** for display update control
- **Anti-aliased trace rendering**
- **Flexible data packing** (12 packing modes)

The SCOPE window is ideal for monitoring sensor values, ADC readings, analog signals, and any continuous time-domain data.

**File Location**: `DebugDisplayUnit.pas`

**Key Methods**:
- `SCOPE_Configure` (lines 1151-1207): Initialization and channel setup
- `SCOPE_Update` (lines 1209-1337): Sample ingestion and trigger processing
- `SCOPE_Draw` (lines 1339-1364): Waveform rendering
- `SCOPE_Range` (lines 1366-1379): Auto-ranging calculation

---

## 2. Architecture Overview

### 2.1 System Context

The SCOPE window operates as part of the P2 debug display system:

```
┌─────────────────────────────────────────────────────────────┐
│                    Propeller 2 Hardware                     │
│              (Analog Signal Sampling)                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Serial Transmission
                         │ (Packed Sample Sets)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      SerialUnit.pas                          │
│            (Background Thread, 16MB RX Buffer)               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Element Array Parsing
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                       DebugUnit.pas                          │
│                  (Display Management Layer)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ UpdateDisplay Trigger
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   DebugDisplayUnit.pas                       │
│                     SCOPE_Update Method                      │
│                                                              │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   │
│  │ Data Packing │   │ Auto-Ranging │   │   Trigger    │   │
│  │   UnPack()   │──>│ SCOPE_Range()│──>│  Detection   │   │
│  └──────────────┘   └──────────────┘   └──────────────┘   │
│                                              │               │
│                                              │ RateCycle     │
│                                              ▼               │
│                     ┌──────────────────────────────┐        │
│                     │     SCOPE_Draw Method        │        │
│                     │   (Multi-Trace Rendering)    │        │
│                     └──────────────────────────────┘        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Double-Buffered Display
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Windows VCL Canvas                         │
│              (Oscilloscope Visualization)                    │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Data Flow

**Configuration Flow** (Window Creation — **keys only**):
```
Create message → FormCreate → SetDefaults → SCOPE_Configure (keys) → Set Metrics → Show Window
```

**Channel Definition Flow** (a *separate*, later message):
```
Update message → SCOPE_Update → 'label' … → vLabel/vAuto/vLow/vHigh/vTall/vBase/vGrid/vColor
```

**Sample Flow** (Data Acquisition):
```
P2 Samples → Pack Data → Serial TX → UnPack → Sample Set Assembly → Circular Buffer → Trigger Check → SCOPE_Draw
```

**Auto-Ranging Flow** (Dynamic Scaling):
```
Sample Buffer → SCOPE_Range Scan → Find Min/Max → Update vLow/vHigh → Apply Scale Factor
```

---

## 3. Display Type and Constants

### 3.1 Display Type Identifier

```pascal
dis_scope = 1;
```

The SCOPE display is the second display type (index 1) in the debug display system.

**Source Location**: Line 23 in DebugDisplayUnit.pas

### 3.2 Buffer Constants

```pascal
Channels         = 8;                    // Maximum channels
Y_SetSize        = Channels;             // 8 samples per set (one per channel)
Y_Sets           = DataSets;             // 2048 sample sets
Y_PtrMask        = Y_Sets - 1;           // 2047 (for circular buffer)
```

**Purpose**:
- `Channels`: Maximum number of simultaneous analog channels (8)
- `Y_SetSize`: Samples per complete set (one sample from each channel)
- `Y_Sets`: Number of sample sets in circular buffer (2048)
- `Y_PtrMask`: Bit mask for circular buffer wraparound (2047 = 0x7FF)

**Memory Calculation**:
```
Y_SampleBuff: 2048 sets × 8 samples × 4 bytes = 65,536 bytes = 64 KB
```

**Source Locations**: `DataSetsExp` = 154, `DataSets` = 155, **`Channels` = 157**, `Y_SetSize`/`Y_Sets`/`Y_PtrMask` = 167-169 in DebugDisplayUnit.pas.

### 3.3 Size Constraints

```pascal
scope_wmin    = 32;                      // Minimum width in pixels
scope_wmax    = SmoothFillMax;           // Maximum width (2048)
scope_hmin    = 32;                      // Minimum height in pixels
scope_hmax    = SmoothFillMax;           // Maximum height (2048)
```

**Source Locations**: Lines 210-213 in DebugDisplayUnit.pas

### 3.4 Default Values

```pascal
// From SCOPE_Configure (lines 1156-1159)
vRate        := 1;               // Default rate divisor (1 = every sample)
vDotSize     := 0;               // Default dot size (0 = no dots)
vLineSize    := 3;               // Default line thickness (pixels)
vTextSize    := FontSize;        // Default label font size (FontSize global, default 10)
```

---

## 4. Data Structures

### 4.1 Sample Buffer

```pascal
Y_SampleBuff: array[0..Y_Sets * Y_SetSize - 1] of integer;
```

**Characteristics**:
- **Size**: 2048 sets × 8 channels = 16,384 samples total
- **Element Type**: 32-bit signed integer
- **Access Pattern**: Circular buffer with wraparound
- **Organization**: Interleaved by sample set
  - `Y_SampleBuff[set * 8 + channel]` = sample for given set and channel

**Buffer Layout**:
```
Set 0:  [Ch0][Ch1][Ch2][Ch3][Ch4][Ch5][Ch6][Ch7]
Set 1:  [Ch0][Ch1][Ch2][Ch3][Ch4][Ch5][Ch6][Ch7]
...
Set 2047: [Ch0][Ch1][Ch2][Ch3][Ch4][Ch5][Ch6][Ch7]
```

**Circular Buffer Management**:
```pascal
// Write sample set
Move(samp, Y_SampleBuff[SamplePtr * Y_SetSize], Y_SetSize shl 2);
SamplePtr := (SamplePtr + 1) and Y_PtrMask;

// Read sample (k sets back, channel j)
v := Y_SampleBuff[((SamplePtr - k - 1) and Y_PtrMask) * Y_SetSize + j];
```

**Source Location**: Line 361

### 4.2 Channel Configuration Arrays

```pascal
vAuto        : array[0..Channels - 1] of boolean;     // Auto-ranging enable per channel
vLow         : array[0..Channels - 1] of integer;     // Low value (bottom of range)
vHigh        : array[0..Channels - 1] of integer;     // High value (top of range)
vTall        : array[0..Channels - 1] of integer;     // Vertical height in pixels
vBase        : array[0..Channels - 1] of integer;     // Vertical offset in pixels
vGrid        : array[0..Channels - 1] of integer;     // Grid flag bitmask (rendered in ClearBitmap)
vLabel       : array[0..Channels - 1] of string;      // Channel labels
vColor       : array[0..Channels - 1] of integer;     // Trace colors (RGB24)
```

**Purpose**:

**vAuto**: Auto-ranging mode per channel
- `True`: Automatically calculate vLow/vHigh from sample buffer
- `False`: Use manually specified vLow/vHigh values

**vLow/vHigh**: Value range for vertical scaling
- `vLow`: Corresponds to bottom of trace area
- `vHigh`: Corresponds to top of trace area
- Range: -$80000000 to $7FFFFFFF (full 32-bit signed)

**vTall**: Vertical height in pixels
- Determines vertical span of trace
- Default: vHeight (full display height)
- Allows partial-height traces for multi-channel overlay

**vBase**: Vertical offset in pixels
- Positive: Shift trace up
- Negative: Shift trace down
- Default: 0 (no offset)
- Useful for overlaying multiple channels

**vGrid**: Grid flag bitmask (rendered, default 0 = off)
- Drawn in `ClearBitmap` for `dis_scope` (lines 3290-3333), not in `SCOPE_Draw`
- 4-bit mask: bit0=baseline line, bit1=top line, bit2=min-value label, bit3=max-value label
- Lines/labels use a channel-tinted color (`AlphaBlend(vColor[i], vBackColor, $40)`)

**Default Initialization** (lines 1189-1197):
```pascal
for i := 0 to Channels - 1 do
begin
  vAuto[i] := False;
  vLow[i]  := -$80000000;
  vHigh[i] := $7FFFFFFF;
  vTall[i] := vHeight;
  vBase[i] := 0;
  vGrid[i] := 0;
end;
```

**Source Locations**: Lines **303-311** — `vLabel` 303, `vAuto` 304, `vHigh` 305, `vLow` 306, `vMag` 307 *(FFT-only)*, `vTall` 308, `vBase` 309, `vGrid` 310, `vColor` 311.

### 4.3 Trigger State Variables

```pascal
vTriggerChannel : integer;       // Channel to trigger on (-1 = disabled, 0-7 = channel)
vTriggerAuto    : boolean;       // Auto-trigger mode
vTriggerArm     : integer;       // Arm level (must cross before trigger)
vTriggerFire    : integer;       // Fire level (trigger occurs here)
vTriggerOffset  : integer;       // Sample offset for trigger position (0..vSamples-1)
vHoldOff        : integer;       // Holdoff count to prevent re-triggering
vHoldOffCount   : integer;       // Current holdoff counter
vArmed          : boolean;       // Trigger armed state
vTriggered      : boolean;       // Trigger event occurred
```

**Trigger Logic**:

**vTriggerChannel**: Selects which channel to monitor
- `-1`: Trigger disabled (free-running mode)
- `0-7`: Channel index to trigger on

**vTriggerAuto**: Auto-calculate trigger levels
- `True`: Calculate arm/fire levels from sample buffer range
  - Arm level = low + (high - low) / 3 (lower third)
  - Fire level = low + (high - low) / 2 (middle)
- `False`: Use manually specified arm/fire levels

**vTriggerArm/vTriggerFire**: Threshold levels
- **Rising edge**: `TriggerFire >= TriggerArm`
  - Arm when signal drops below TriggerArm
  - Fire when signal rises above TriggerFire
- **Falling edge**: `TriggerFire < TriggerArm`
  - Arm when signal rises above TriggerArm
  - Fire when signal falls below TriggerFire

**vTriggerOffset**: Pre/post-trigger position. It is a **SAMPLE INDEX — a count of sample sets back
from the newest — not a pixel offset.** It is clamped to `0..vSamples-1` (`KeyValWithin(vTriggerOffset,
0, vSamples - 1)`, `SCOPE_Update` 1248) and it selects the tested sample by *age*:

```pascal
t := Y_SampleBuff[((SamplePtr - vTriggerOffset - 1) and Y_PtrMask) * Y_SetSize + vTriggerChannel];  // 1295
```

`SCOPE_Draw` plots the `k`-sets-back sample at `x = (vMarginLeft + vWidth - 1) shl 8 - k/vSamples ×
vWidth × $100` (1358) — **k = 0 (newest) is the RIGHT edge**, `k = vSamples-1` (oldest) the left. The
trigger indicator confirms it: `x := vBitmapWidth - vMarginRight - Round((vTriggerOffset + 1) /
vSamples * vWidth)` (`ClearBitmap` 3353) — measured **leftward from the right edge**. So:

- `0`: Trigger at the **RIGHT** edge — the whole screen is **pre-trigger** history (what led up to the trigger)
- `vSamples/2`: Trigger at center (default) — half pre-trigger, half post-trigger
- `vSamples-1`: Trigger at the **LEFT** edge — the whole screen is **post-trigger** (what happened after the trigger)

*(Rendered pixel position of the indicator line is a `Round()` of the above; exact sub-pixel placement is
**NEEDS-HARDWARE**, but the edge mapping is unambiguous from the code.)*

**Default Initialization** (lines 1198-1203):
```pascal
vTriggerChannel := -1;
vTriggerAuto := False;
vTriggerArm := -1;
vTriggerFire := 0;
vTriggerOffset := vSamples div 2;
vHoldOff := vSamples;
```

### 4.4 Display State Variables

```pascal
vSamples        : integer;       // Horizontal resolution (sets displayed)
vWidth          : integer;       // Display width in pixels
vHeight         : integer;       // Display height in pixels
vRate           : integer;       // Rate divisor (1 = every sample triggers draw)
vRateCount      : integer;       // Current rate counter
vDotSize        : integer;       // Dot size (0 = no dots) — passed to SmoothDot as `vDotSize shl 7`
vLineSize       : integer;       // Line thickness (0 = no lines) — passed to SmoothLine as `vLineSize shl 6`
vTextSize       : integer;       // Label font size
vIndex          : integer;       // Number of active channels
```

---

## Directive Reference (v55-verified)

> Quick lookup tables drawn from §5.2 of the [Debug Window Directive Matrix](../DEBUG-WINDOW-DIRECTIVE-MATRIX.md) and §4 shared input model. Pascal line numbers refer to `DebugDisplayUnit.pas` (v55).

### Configuration directives

Accepted by `SCOPE_Configure` (lines 1151–1207). All directives are optional; the window may be opened with only a name.

> 🔴 **The create message accepts KEYS ONLY** (`while NextKey do`, 1161). A channel-def string,
> `TRIGGER` or `HOLDOFF` here ends the parse and discards the rest of the message — and per **EF-003**
> a channel def on the create line **prevents the window from being created at all**. Those belong in a
> separate update message (§6.1).

| Directive | Parameters | Range / default | Pascal lines |
|---|---|---|---|
| `TITLE` | `'string'` | `"<name> - SCOPE"` (FormCreate:626) | 1163–1164 |
| `POS` | `left top` | offset from host origin ≈(0,210); no cascade (FormCreate:628-629, KeyPos:2712-2716) | 1165–1166 |
| `SIZE` | `width height` (pixels) | each int 32–2048 / 256×256 | 1167–1168 |
| `SAMPLES` | `n` | int 16–2048 / 256 | 1169–1170 |
| `RATE` | `n` | int 1–2048 / 1 | 1171–1172 |
| `DOTSIZE` | `n` | int 0–32 / 0¹ | 1173–1174 |
| `LINESIZE` | `n` | int 0–32 / 3¹ | 1175–1176 |
| `TEXTSIZE` | `n` | int 6–200 / 10 (`FontSize`) | 1177–1178 |
| `COLOR` | `back grid` | each: named color or RGB24 / black `$000000`, gray `$404040` | 1179–1181 |
| `HIDEXY` | *(flag)* | — / shown | 1182–1183 |
| `LONGS_1BIT`…`BYTES_4BIT` `{ALT}` `{SIGNED}` | *(packing mode)* | 12 modes / **none — the default is UNPACKED**² | 1184–1185 |

¹ Post-configure default: if both `DOTSIZE` and `LINESIZE` are 0, `DOTSIZE` is forced to 1 (line 1188).
`DOTSIZE` takes a **single** value for SCOPE (`KeyValWithin(vDotSize, 0, 32)`, 1173-1174) — the optional
second (`y`) value exists only for SPECTRO/PLOT/BITMAP.

² **There is no default packing mode.** `SetDefaults` (2915) runs before `SCOPE_Configure` and calls
`SetPack(0, False, False)`; `SetPack` (4152-4155) special-cases `val = 0`, **bypassing the `PackDef`
table**: `vPackCount = 1`, `vPackShift = 32`, `vPackMask = $FFFFFFFF` ⇒ **one full 32-bit sample per
transmitted long**. `LONGS_1BIT` is one of twelve opt-in keys, **not** the default. `ALT` and `SIGNED`
are optional trailing modifiers (up to two, either order — `KeyPack` 2817-2832); sign-extension is a
**runtime flag**, never a property of the mode.

**Note on `SAMPLES`/`RATE`/`HOLDOFF` clamps**: `KeyValWithin` is **assign-and-clamp** — an
out-of-range value is saturated into range, never ignored (`Within`, GlobalUnit.pas:222-227).

### Display / data directives

Accepted by `SCOPE_Update` (lines 1209–1337) on every subsequent message.

| Directive | Parameters | Range / value-set / default | Pascal lines |
|---|---|---|---|
| *string* (channel def) | `'label' (AUTO \| lo hi) {tall} {base} {grid} {color}` — **strictly positional** | `label`: free string. `AUTO`: keyword flag → vAuto:=True. `lo`/`hi`: int32 (defaults −$80000000 / $7FFFFFFF). `tall`: int / vHeight. `base`: int / 0. `grid`: int / 0 — **4-bit `%abcd` mask, rendered** (bit0=baseline line, bit1=top line, bit2=min-value TEXT, bit3=max-value TEXT) in `ClearBitmap` 3298-3333; see §19.3. `color`: named keyword or numeric (via `vColorMode`) / `DefaultScopeColors[i]` — **requires every preceding positional**. Up to 8 channels (`Channels`=8); a **9th def overwrites channel 8 in place** (`vIndex` saturates at 1219, but the write still lands at `vIndex-1` = 7) | 1217–1231 |
| `TRIGGER` | `channel (AUTO \| arm fire) {offset}` | `channel`: int **−1..7** (−1=disabled/free-run). `AUTO`: keyword flag → vTriggerAuto:=True (else `arm`,`fire`: int32). `offset`: **a SAMPLE INDEX**, int **0…vSamples−1** / vSamples div 2 (not pixels — see §4.3) | 1236–1249 |
| `HOLDOFF` | `n` | int **2..2048** / vSamples (set in Configure); resets vHoldOffCount:=0 | 1250–1251 |
| `CLEAR` | *(none)* | `vTriggered:=False` (suppresses the trigger indicator), clears + presents the bitmap, resets SamplePop and vRateCount | 1252–1259 |
| `SAVE` | `'name'` \| `WINDOW {'name'}` \| `l t w h {'name'}` \| *(bare)* | `SAVE 'name'` → writes `Bitmap[1]` (the **front** buffer) to `name.bmp`. `SAVE WINDOW 'name'` → desktop **BitBlt scrape** of the window's *outer* rect (title bar + borders; occludable). `SAVE l t w h 'name'` → desktop scrape of an arbitrary screen region. Omitting the filename in the two scrape forms captures to memory and **writes no file**. **Bare `SAVE` writes nothing** (`Exit`). ⚠️ A non-`WINDOW` key after `SAVE` is **consumed and discarded** — `` `MyScope SAVE CLEAR `` does nothing *and eats the `CLEAR`* (`KeySave` 2843-2848). | 1260–1261 |
| `CLOSE` | *(none)* | **Closes the window** and frees its display slot. Handled one layer up — at the **parser**, not in `SCOPE_Update` (`p2com.asm` 19565-19624 clears the display's `debug_display_ena` bit; `TDebugForm.ChrIn`, DebugUnit.pas:236-237, runs the full update and *then* closes). Command-only (ignored in a create message), multi-target, and **update-first/close-second** — `` `MyScope SAVE 'shot' CLOSE `` saves, then closes. | *(parser layer)* |
| `PC_KEY` | *(none)* | Transmits latched key byte → P2 | 1262–1263 |
| `PC_MOUSE` | *(none)* | Transmits mouse position + color → P2 | 1264–1265 |

> ⚠️ `SAVE 'name'` writes **`Bitmap[1]`, the front buffer**. SCOPE presents via `BitmapToCanvas(0)`
> on every draw, so the front buffer is normally current — but any `SAVE` issued in a message that
> has not yet triggered a draw writes the **previously presented** frame.

### Keyboard & mouse

Input handling is **shared across all nine display windows** via form-level event handlers on `TDebugDisplayForm`. Per-window variation is **only** in coordinate mapping.

**Shared handlers** (identical for all windows):

| Handler | Lines | Behavior |
|---|---|---|
| `WMGetDlgCode` | 585–589 | Captures Tab key (`DLGC_WANTTAB`); Tab does not change focus |
| `FormMouseMove` | 647–809 | Renders live measurement-cursor overlay showing window coordinates. Suppressed when `HIDEXY` set (line 737) |
| `FormMouseWheel` | 811–817 | Latches wheel direction into `vMouseWheel` (+1/−1) for **100 ms**, then auto-clears (819–823) |
| `FormKeyPress` | 825–831 | Latches pressed key byte into `vKeyPress` for **100 ms**, then auto-clears (853–857) |
| `FormKeyDown` | 833–851 | Maps non-printable keys: Left=1, Right=2, Up=3, Down=4, Home=5, End=6, Delete=7, Insert=10, PageUp=11, PageDown=12; forwards to `FormKeyPress` |

The 100 ms latch means a key/wheel event not polled within that window is silently dropped.

**`PC_KEY` → `SendKeyPress`** (3579–3583): transmits one LONG = latched `vKeyPress` byte (0 if none), then clears it. Behavior is **identical for all nine windows**.

**`PC_MOUSE` → `SendMousePos`** (3537–3577): transmits two LONGs:
- LONG 1: `x` bits 0–12, `y` bits 13–25, `wheel` bits 26–27, L/M/R buttons bits 28/29/30. If cursor is outside the client area, LONG 1 = `$03FFFFFF`.
- LONG 2: RGB color of pixel under cursor (`$RRGGBB`). If off-window, `$FFFFFFFF`.

**SCOPE coordinate mapping** — ⚠️ the **on-screen readout** and the **`PC_MOUSE` wire
value use different coordinates**:

- **On-screen readout** (`FormMouseMove` lines 668–675): SCOPE and FFT share this branch.
  The cursor is shown as a pixel offset from the plot origin with **Y inverted**:
  ```
  x = cursor_x − vMarginLeft               (0 = left edge of plot)
  y = vMarginTop + vHeight − 1 − cursor_y  (0 = bottom of plot, increasing upward)
  ```
  Outside the plot rectangle the readout string is empty (no overlay drawn).
- **`PC_MOUSE` wire value** (`SendMousePos`, 3537–3577): `SendMousePos` has **no `dis_scope`
  branch** — it only transforms SPECTRO/PLOT/BITMAP (÷dotsize) and TERM (char cells). For
  SCOPE it transmits the **raw client-pixel** `x,y` (no margin offset, no Y inversion). The
  P2 therefore receives raw pixels, *not* the inverted plot-origin coordinate shown on screen.

`HIDEXY` suppresses the on-screen readout but does **not** disable `PC_MOUSE` reporting.

**TRIGGER form** (SCOPE-specific, `SCOPE_Update` lines 1236–1249):
```
TRIGGER channel (AUTO | arm fire) {offset}
  channel : -1 (disable/free-run) | 0..7
  AUTO    : arm/fire auto-computed from buffer range each sample set
  arm     : arm threshold (integer)
  fire    : fire threshold (integer)
  offset  : trigger position as a SAMPLE INDEX (sets back from newest), 0..vSamples-1
            (default = vSamples div 2). 0 = trigger at the RIGHT edge; vSamples-1 = LEFT edge. See §4.3.
```

`TRIGGER` and `HOLDOFF` are **update-phase only** — `SCOPE_Configure`'s `case` (1162-1186) has no
`key_trigger`/`key_holdoff` arm. Placing them in the create message truncates the configure parse (§6.1).

---

## 5. Configuration and Initialization

### 5.1 SCOPE_Configure Method

```pascal
procedure TDebugDisplayForm.SCOPE_Configure;
var
  i: integer;
begin
  // Set unique defaults
  vRate := 1;
  vDotSize := 0;
  vLineSize := 3;
  vTextSize := FontSize;

  // Process any parameters
  while NextKey do
  case val of
    key_title:       KeyTitle;
    key_pos:         KeyPos;
    key_size:        KeySize(vWidth, vHeight, scope_wmin, scope_wmax, scope_hmin, scope_hmax);
    key_samples:     KeyValWithin(vSamples, 16, Y_Sets);
    key_rate:        KeyValWithin(vRate, 1, Y_Sets);
    key_dotsize:     KeyValWithin(vDotSize, 0, 32);
    key_linesize:    KeyValWithin(vLineSize, 0, 32);
    key_textsize:    KeyTextSize;
    key_color:       if KeyColor(vBackColor) then KeyColor(vGridColor);
    key_hidexy:      vHideXY := True;
    key_longs_1bit..key_bytes_4bit:  KeyPack;
  end;

  // Set defaults
  if (vDotSize = 0) and (vLineSize = 0) then vDotSize := 1;
  for i := 0 to Channels - 1 do
  begin
    vAuto[i] := False;
    vLow[i]  := -$80000000;
    vHigh[i] := $7FFFFFFF;
    vTall[i] := vHeight;
    vBase[i] := 0;
    vGrid[i] := 0;
  end;
  vTriggerChannel := -1;
  vTriggerAuto := False;
  vTriggerArm := -1;
  vTriggerFire := 0;
  vTriggerOffset := vSamples div 2;
  vHoldOff := vSamples;

  // Set form metrics
  SetTextMetrics;
  SetSize(ChrWidth, ChrHeight * 2, ChrWidth, ChrWidth);
end;
```

**Source Location**: Lines 1151-1207

### 5.2 Configuration Parameters

| Parameter | Command | Default | Range | Purpose |
|-----------|---------|---------|-------|---------|
| Title | `TITLE 'string'` | `"<name> - SCOPE"` | - | Window title (caption set in FormCreate) |
| Position | `POS x y` | host origin ≈(0,210), no cascade | offset from host origin | Window position |
| Size | `SIZE width height` | 256 × 256 | 32-2048 | Display dimensions |
| Samples | `SAMPLES count` | 256 | 16-2048 | Horizontal resolution |
| Rate | `RATE divisor` | 1 | 1-2048 | Display update rate divisor |
| Dot Size | `DOTSIZE n` | 0 | 0-32 | Dot size (0 = no dots; rendered width **NEEDS-HARDWARE** — see §20.3) |
| Line Size | `LINESIZE n` | 3 | 0-32 | Line thickness (0 = no lines; `LINESIZE 3` renders 3 px, measured) |
| Text Size | `TEXTSIZE size` | 10 (FontSize) | 6-200 | Label font size |
| Colors | `COLOR back grid` | Black/Gray | RGB24 | Background and grid colors |
| Hide XY | `HIDEXY` | Show | - | Hide mouse coordinates |
| Packing | `LONGS_1BIT` etc. `{ALT} {SIGNED}` | **unpacked** (1 sample/long, 32-bit, unsigned) | 12 opt-in modes | Data packing format |

**Packing default** — `SetDefaults` (line 2915) calls `SetPack(0, False, False)` *before*
`SCOPE_Configure` runs; `SetPack` (4152-4155) treats `val = 0` as a special case that **bypasses
`PackDef`**: `vPackCount := 1`, `vPackShift := 32`, `vPackMask := $FFFFFFFF`. So with **no** packing
keyword, each transmitted long is **one full 32-bit sample**. `LONGS_1BIT` is *not* the default.

### 5.3 Rendering Mode Validation

```pascal
// Set defaults (line 1188)
if (vDotSize = 0) and (vLineSize = 0) then vDotSize := 1;
```

**Purpose**: Ensure at least one rendering mode is active.
- If both dot and line sizes are 0, default to dot size of 1
- Prevents invisible traces

---

## 6. Channel Configuration

### 6.1 Channel Configuration Syntax

> ### 🔴 Channel definitions are **UPDATE-phase only** — never on the create line
>
> `SCOPE_Configure` is a **key-only** parser: `while NextKey do` (line 1161). `NextKey` fails on the
> first non-key element, so a **channel-def string — or `TRIGGER`, or `HOLDOFF` — placed in the create
> message terminates the configure parse, and every element after it is silently discarded.**
> `key_trigger`/`key_holdoff` have no arm in `SCOPE_Configure`'s `case` (1162-1186) at all; they are
> parsed **only** by `SCOPE_Update` (1236-1251), and channel defs only by `SCOPE_Update`'s
> `if NextStr then` branch (1217-1231).
>
> **Hardware-confirmed consequence (EF-003): a SCOPE channel-def on the create line prevents the
> window from being created at all.** It does not "open empty" — no window appears.
>
> **Always use the two-message pattern** (as every shipped Spin2 demo does):
>
> ```spin2
> debug(`SCOPE MyScope SIZE 254 84 SAMPLES 128)   ' 1. CREATE — keys only
> debug(`MyScope 'Sawtooth' 0 63 64 10 %1111)     ' 2. UPDATE — channel def
> debug(`MyScope TRIGGER 0 HOLDOFF 2)             ' 3. UPDATE — trigger/holdoff
> ```
>
> (`DEBUG-TESTING/DEBUG_SCOPE.spin2:5-6`, `DEBUG_SCOPE_2CHAN.spin2:5-8`.)

**String Element Format** (an element of an **update** message — `SCOPE_Update` 1217-1231):
```
'label' {AUTO | low high} {tall} {base} {grid} {color}
```

**⚠️ The parameters are strictly POSITIONAL.** After the label, `SCOPE_Update` reads them in fixed
order — `AUTO` *or* `low`+`high`, then `tall`, `base`, `grid`, then `color` — and any `KeyVal` that
finds no number does `Continue`, abandoning the rest of that def. There is **no way to skip a
positional and supply a later one**: a bare number after the label is the **`low` bound**, never a
color, and a numeric color requires *every* preceding positional to be present.

**Parameters**:
- `label`: Channel name
- `AUTO`: Enable auto-ranging (exclusive with low/high)
- `low high`: Manual range (min/max values)
- `tall`: Vertical height in pixels (default: vHeight)
- `base`: Vertical offset in pixels (default: 0)
- `grid`: Grid flag bitmask (default: 0; bits select baseline/top lines and min/max labels — see §4.2/§19.3)
- `color`: Trace color — named keyword or numeric (interpreted through the current `vColorMode`, default RGB24); default `DefaultScopeColors[i]`

### 6.2 Auto-Ranging Mode

**Syntax** (in an **update** message, after the window exists):
```
debug(`MyScope 'SENSOR' AUTO)
```

**Channel-def parsing code** — `SCOPE_Update` (lines 1217-1232):
```pascal
if NextStr then
begin
  if vIndex <> Channels then Inc(vIndex);
  vLabel[vIndex - 1] := PChar(val);
  if KeyIs(key_auto) then
    vAuto[vIndex - 1] := True
  else
  begin
    if not KeyVal( vLow[vIndex - 1]) then Continue;
    if not KeyVal(vHigh[vIndex - 1]) then Continue;
  end;
  if not KeyVal(vTall[vIndex - 1]) then Continue;
  if not KeyVal(vBase[vIndex - 1]) then Continue;
  if not KeyVal(vGrid[vIndex - 1]) then Continue;
  KeyColor(vColor[vIndex - 1]);
end
```

**Behavior**:
- `vAuto[channel] = True`
- vLow/vHigh automatically calculated by SCOPE_Range on each draw
- Trace scale adapts to signal range

### 6.3 Manual Ranging Mode

**Syntax** (in an **update** message):
```
debug(`MyScope 'ADC' -128 127 256 0 0 $FF0000)
```

**Parameters** (positional — `label low high tall base grid color`):
- Label: "ADC"
- Low: -128 (bottom of display)
- High: 127 (top of display)
- Tall: 256 pixels (vertical span)
- Base: 0 (no vertical offset)
- Grid: 0 (no grid lines/labels; nonzero would enable them per the bitmask)
- Color: Red ($FF0000)

**Behavior**:
- `vAuto[channel] = False`
- vLow/vHigh remain fixed
- Trace scale is constant

### 6.4 Overlay Configuration

**Multiple Channels with Offsets** (each channel def is its own **update**-message element; `grid` must
be supplied before `color`):
```spin2
debug(`SCOPE MyScope)                            ' create — keys only
debug(`MyScope 'CH1' AUTO 128 0   0 $00FF00)     ' label AUTO tall base grid color
debug(`MyScope 'CH2' AUTO 128 128 0 $FF0000)
```

**Result**:
- CH1: Green, 128px tall, bottom half of display
- CH2: Red, 128px tall, top half of display
- Overlaid on same time base

> ⚠️ **Do not omit `grid`.** Written as `'CH1' AUTO 128 0 $00FF00` (five elements), `SCOPE_Update`
> 1228-1231 consumes `128`→`vTall`, `0`→`vBase`, **`$00FF00`→`vGrid`**, and then `KeyColor(vColor[…])`
> finds nothing — so the channel keeps its **default** `DefaultScopeColors[i]` and gets a nonsense
> grid mask. (The trace still *looks* green because `DefaultScopeColors[0]` happens to be `clLime`
> — the right answer for the wrong reason. CH2 would be **red-by-default**, not red-by-request.)

### 6.5 Configuration Examples

Every SCOPE session is **at least two messages**: a create message carrying **keys only**, then one or
more update messages carrying the channel defs (see the caution in §6.1).

**Example 1: Single Auto-Ranging Channel**:
```spin2
debug(`SCOPE MyScope)                    ' create
debug(`MyScope 'TEMPERATURE' AUTO)       ' update: channel def
```

Result:
- 1 channel
- Automatic range detection
- Green (`DefaultScopeColors[0]` = `clLime` `$00FF00`)

**Example 2: Fixed Range ADC**:
```spin2
debug(`SCOPE MyScope)                    ' create
debug(`MyScope 'ADC' 0 1023 256)         ' update: label low high tall
```

Result:
- 1 channel
- Fixed 0-1023 range
- 256 pixels tall
- Green (default color; `base`/`grid`/`color` were not supplied, so parsing stops after `tall`)

**Example 3: Multi-Channel with Colors**:
```spin2
debug(`SCOPE MyScope SIZE 512 384)               ' create — keys only
debug(`MyScope 'X' AUTO 128 0   0 $FF0000)       ' update: 3 channel defs
debug(`MyScope 'Y' AUTO 128 128 0 $00FF00)
debug(`MyScope 'Z' AUTO 128 256 0 $0000FF)
```

Result:
- 3 channels (X, Y, Z)
- Auto-ranging
- 128 pixels each
- Stacked vertically (base offsets: 0, 128, 256)
- Red, green, blue

(The three defs may also be packed into **one** update message — `SCOPE_Update`'s `while not NextEnd`
loop, 1215, takes any number of strings — but they may **never** ride on the create message.)

---

## 7. Auto-Ranging System

### 7.1 SCOPE_Range Method

```pascal
procedure TDebugDisplayForm.SCOPE_Range(channel: integer; var low, high: integer);
var
  k: integer;
  v: int64;
begin
  low := $7FFFFFFF;
  high := -$80000000;
  for k := SamplePop - 1 downto 0 do
  begin
    v := Y_SampleBuff[((SamplePtr - k - 1) and Y_PtrMask) * Y_SetSize + channel];
    if v < low then low := v;
    if v > high then high := v;
  end;
end;
```

**Source Location**: Lines 1366-1379

**Processing**:
1. Initialize low/high to extreme values
2. Scan all samples in buffer for given channel
3. Track minimum (low) and maximum (high)
4. Return range via var parameters

**Complexity**: O(n) where n = SamplePop (number of samples)

### 7.2 Auto-Ranging Application

**Code** (SCOPE_Draw, line 1346):
```pascal
for j := vIndex - 1 downto 0 do if vAuto[j] then SCOPE_Range(j, vLow[j], vHigh[j]);
```

**Processing**:
- Called once per SCOPE_Draw invocation
- Only processes channels with `vAuto[j] = True`
- Updates vLow/vHigh for those channels
- Scaling recalculated based on new range

### 7.3 Auto-Trigger Range Calculation

**Code** (SCOPE_Update, lines 1289-1294):
```pascal
if vTriggerAuto then
begin
  SCOPE_Range(vTriggerChannel, low, high);
  vTriggerArm := (high - low) div 3 + low;
  vTriggerFire := (high - low) div 2 + low;
end;
```

**Formula**:
```
range = high - low
vTriggerArm  = low + range / 3    (lower third)
vTriggerFire = low + range / 2    (midpoint)
```

**Example**:
```
Signal range: 100 to 700
  range = 600
  arm  = 100 + 200 = 300
  fire = 100 + 300 = 400

Trigger on rising edge crossing 400 (after falling below 300)
```

### 7.4 Range Stability

**Potential Issue**: Range can change rapidly if signal varies.

**Mitigation Strategies**:
1. Use manual ranging for stable display
2. Use trigger holdoff to prevent excessive updates
3. Use rate limiting to slow down updates

**Trade-offs**:
- Auto-ranging: Adapts to signal, but may be unstable
- Manual ranging: Stable display, but requires known signal range

---

## 8. Sample Processing

### 8.1 SCOPE_Update Method Overview

```pascal
procedure TDebugDisplayForm.SCOPE_Update;
var
  ch, i, t, v, low, high: integer;
  samp: array[0..Y_SetSize - 1] of integer;
begin
  ch := 0;
  while not NextEnd do
  begin
    // String element: channel configuration (see Section 6)
    if NextStr then ...
    // Key element: trigger/control commands
    else if NextKey then ...
    // Numeric elements: sample data
    else while NextNum do ...
  end;
end;
```

**Source Location**: Lines 1209-1337

### 8.2 Sample Set Assembly

**Processing Loop** (lines 1268-1335):
```pascal
while NextNum do
begin
  // Get channel sample(s)
  v := NewPack;
  for i := 1 to vPackCount do
  begin
    // Enter sample into local buffer
    samp[ch] := UnPack(v);
    Inc(ch);
    if ch = vIndex then
    begin
      // Complete sample set received
      ch := 0;
      Move(samp, Y_SampleBuff[SamplePtr * Y_SetSize], Y_SetSize shl 2);
      SamplePtr := (SamplePtr + 1) and Y_PtrMask;
      if SamplePop < vSamples then Inc(SamplePop);
      // Trigger processing...
    end;
  end;
end;
```

**Sample Set Assembly**:
1. Read packed value: `v = NewPack()`
2. Unpack samples: `samp[ch] = UnPack(v)`
3. Increment channel counter
4. When all channels received (`ch = vIndex`):
   - Copy complete set to circular buffer
   - Advance write pointer
   - Increment fill level (until full)
   - Process trigger
   - Reset channel counter for next set

**⚠️ Sub-samples go ROUND-ROBIN across the channels.** `ch` is declared once, at the top of
`SCOPE_Update` (1213: `ch := 0;`), and is **never reset per transmitted long** — it advances through the
sub-samples of a long and wraps only when a set completes (`if ch = vIndex then ch := 0`, 1277-1279).
A single packed long therefore feeds **successive channels**, not one channel.

**Example** (4 channels, `LONGS_1BIT` → `vPackCount = 32`):
```
One transmitted long unpacks to 32 sub-samples, distributed round-robin
across the active channels:
  sub-sample 0→ch0, 1→ch1, 2→ch2, 3→ch3, 4→ch0, 5→ch1, …

⇒ 32 / 4 = 8 complete sample sets stored per transmitted long
  (32 sub-samples × 1 long = 32 samples total, i.e. 8 sets × 4 channels).
```

`UnPack` (4166-4171) takes the **LOW** sub-field first (`Result := v and vPackMask; v := v shr
vPackShift;`), so within one long the sub-samples are consumed **least-significant field first**.

**Default (no packing keyword)**: `vPackCount = 1`, so **one transmitted long = one sample for one
channel**, and `vIndex` consecutive longs form one complete set — the case the shipped demos use
(`DEBUG_SCOPE_2CHAN.spin2:11` sends `` `(a,b) `` = two longs per set).

### 8.3 Buffer Management

**Write Operation** (line 1281):
```pascal
Move(samp, Y_SampleBuff[SamplePtr * Y_SetSize], Y_SetSize shl 2);
```

**Breakdown**:
- `samp`: Local array with one sample per channel
- `Y_SampleBuff[SamplePtr * Y_SetSize]`: Destination in circular buffer
- `Y_SetSize shl 2`: Byte count (8 channels × 4 bytes = 32 bytes)

**Pointer Advancement** (line 1282):
```pascal
SamplePtr := (SamplePtr + 1) and Y_PtrMask;
```

**Fill Level** (line 1283):
```pascal
if SamplePop < vSamples then Inc(SamplePop);
```

- Increments until buffer is full
- Once full, stays at vSamples (circular buffer overwrites oldest)

---

## 9. Trigger System

The SCOPE window implements a **level-based** trigger system (as opposed to LOGIC's edge-based trigger).

### 9.1 Trigger Configuration

**TRIGGER Command Syntax**:
```
TRIGGER channel {AUTO | arm fire} {offset}
```

**Parameters**:
- `channel`: Channel to trigger on (-1 = disabled, 0-7 = channel index)
- `AUTO`: Auto-calculate arm/fire levels
- `arm fire`: Manual arm/fire threshold levels
- `offset`: Trigger position as a **sample index** (sets back from the newest), 0..vSamples-1 — **not pixels** (§4.3)

**Phase**: `TRIGGER` is parsed **only** by `SCOPE_Update` (1236-1249). It cannot appear in the create
message (§6.1).

**Configuration Code** (lines 1236-1249):
```pascal
key_trigger:
begin
  vArmed := False;
  if not KeyValWithin(vTriggerChannel, -1, 7) then Continue;
  if KeyIs(key_auto) then
    vTriggerAuto := True
  else
  begin
    vTriggerAuto := False;
    if not KeyVal(vTriggerArm) then Continue;
    if not KeyVal(vTriggerFire) then Continue;
  end;
  KeyValWithin(vTriggerOffset, 0, vSamples - 1);
end;
```

**Examples**:
```
TRIGGER 0 AUTO             // Auto-trigger on channel 0
TRIGGER 1 500 600 256      // Trigger on channel 1, arm=500, fire=600, offset=256
TRIGGER -1                 // Disable trigger (free-running)
```

### 9.2 Trigger Detection Algorithm

**Rising Edge Trigger** (`TriggerFire >= TriggerArm`):

```pascal
if vArmed then
begin
  if t >= vTriggerFire then
  begin
    vTriggered := True;
    vArmed := False;
  end;
end
else
begin
  if t <= vTriggerArm then vArmed := True;
end;
```

**Sequence**:
1. Signal below arm level → ARM
2. Signal rises above fire level → TRIGGER
3. Disarm

**Falling Edge Trigger** (`TriggerFire < TriggerArm`):

```pascal
if vArmed then
begin
  if t <= vTriggerFire then
  begin
    vTriggered := True;
    vArmed := False;
  end;
end
else
begin
  if t >= vTriggerArm then vArmed := True;
end;
```

**Sequence**:
1. Signal above arm level → ARM
2. Signal falls below fire level → TRIGGER
3. Disarm

**Source Location**: Lines 1295-1325

### 9.3 Trigger State Machine

```
Rising Edge (Fire > Arm):

    Signal
      │
Arm   ├─────┐      Armed
      │     │
      │     ▼
Fire  │   ──┼──    Triggered
      │
      │
     ─┴─────


Falling Edge (Fire < Arm):

    Signal
      │
Fire  │   ──┼──    Triggered
      │     │
      │     ▼
Arm   ├─────┘      Armed
      │
      │
     ─┴─────
```

### 9.4 Trigger Comparison Code

**Full Implementation** (lines 1286-1325):
```pascal
if vTriggerChannel >= 0 then
begin
  if SamplePop <> vSamples then Continue;      // Wait for full buffer

  // Auto-calculate trigger levels if enabled
  if vTriggerAuto then
  begin
    SCOPE_Range(vTriggerChannel, low, high);
    vTriggerArm := (high - low) div 3 + low;
    vTriggerFire := (high - low) div 2 + low;
  end;

  // Read sample at trigger position
  t := Y_SampleBuff[((SamplePtr - vTriggerOffset - 1) and Y_PtrMask) * Y_SetSize + vTriggerChannel];

  // Check arming and firing
  if vArmed then
  begin
    if vTriggerFire >= vTriggerArm then
    begin
      if t >= vTriggerFire then
      begin
        vTriggered := True;
        vArmed := False;
      end;
    end
    else
    begin
      if t <= vTriggerFire then
      begin
        vTriggered := True;
        vArmed := False;
      end;
    end;
  end
  else
  begin
    if vTriggerFire >= vTriggerArm then
    begin
      if t <= vTriggerArm then vArmed := True;
    end
    else
    begin
      if t >= vTriggerArm then vArmed := True;
    end;
  end;

  // Holdoff processing
  if vHoldOffCount > 0 then Dec(vHoldOffCount);
  if not vTriggered or (vHoldOffCount > 0) then Continue;
  vHoldOffCount := vHoldOff;

  // Update display
  if RateCycle then SCOPE_Draw;
end
```

### 9.5 Holdoff System

**Same as LOGIC window**:
```pascal
key_holdoff:
  if KeyValWithin(vHoldOff, 2, Y_Sets) then vHoldOffCount := 0;
```

**Behavior**: Prevent re-triggering for `vHoldOff` samples after trigger event.

### 9.6 Trigger Disabled Mode

**Condition**: `vTriggerChannel = -1`

**Code** (lines 1331-1332):
```pascal
else if RateCycle then SCOPE_Draw;
```

**Behavior**: Free-running mode - display updates on every rate cycle.

---

## 10. Rendering Pipeline

### 10.1 SCOPE_Draw Method

```pascal
procedure TDebugDisplayForm.SCOPE_Draw;
var
  j, k, x, y, color, offset: integer;
  v: int64;
  fScale: Extended;
begin
  // Autoscale enabled channels
  for j := vIndex - 1 downto 0 do if vAuto[j] then SCOPE_Range(j, vLow[j], vHigh[j]);

  // Draw scope
  ClearBitmap;
  for j := vIndex - 1 downto 0 do
  begin
    if vHigh[j] = vLow[j] then fscale := 0
    else fScale := (vTall[j] - 1) / (Abs(Int64(vHigh[j]) - Int64(vLow[j]))) * $100;
    if vHigh[j] > vLow[j] then offset := vLow[j] else offset := vHigh[j];
    color := vColor[j];
    for k := SamplePop - 1 downto 0 do
    begin
      v := Y_SampleBuff[((SamplePtr - k - 1) and Y_PtrMask) * Y_SetSize + j];
      x := (vMarginLeft + vWidth - 1) shl 8 - Round(k / vSamples * vWidth * $100);
      y := (vMarginTop + vHeight - 1 - vBase[j]) shl 8 - Round((v - offset) * fScale);
      DrawLineDot(x, y, color, k = SamplePop - 1)
    end;
  end;
  BitmapToCanvas(0);
end;
```

**Source Location**: Lines 1339-1364

### 10.2 Rendering Steps

**Step 1: Auto-Range Update** (line 1346):
```pascal
for j := vIndex - 1 downto 0 do if vAuto[j] then SCOPE_Range(j, vLow[j], vHigh[j]);
```

Update vLow/vHigh for auto-ranging channels.

**Step 2: Clear Canvas** (line 1348):
```pascal
ClearBitmap;
```

Fill with background color.

**Step 3: Per-Channel Loop** (lines 1349-1362):

For each channel:
1. Calculate scale factor
2. Set color
3. Plot all samples
4. Connect with lines/dots

**Step 4: Display Update** (line 1363):
```pascal
BitmapToCanvas(0);
```

Copy render target to display buffer.

### 10.3 Scale Factor Calculation

**Code** (lines 1351-1353):
```pascal
if vHigh[j] = vLow[j] then fscale := 0
else fScale := (vTall[j] - 1) / (Abs(Int64(vHigh[j]) - Int64(vLow[j]))) * $100;
if vHigh[j] > vLow[j] then offset := vLow[j] else offset := vHigh[j];
```

**Scale Factor Formula**:
```
fScale = (tall - 1) / |high - low| × 256
```

**Converts**:
- Value units → pixel units (fixed-point)

**Offset**:
- If `high > low`: offset = low (normal case)
- If `high < low`: offset = high (inverted range)

**Example**:
```
vLow = 0, vHigh = 1023, vTall = 256

fScale = (256 - 1) / |1023 - 0| × 256
       = 255 / 1023 × 256
       = 63.81

Value 512: y_offset = 512 × 63.81 = 32,672 (fixed-point) ≈ 128 pixels
```

### 10.4 Coordinate Calculation

**Horizontal (Time)** (line 1358):
```pascal
x := (vMarginLeft + vWidth - 1) shl 8 - Round(k / vSamples * vWidth * $100);
```

**Formula**:
```
x = (left + width - 1) × 256 - (k / samples) × width × 256
```

**Effect**:
- Right-to-left plotting
- k = 0 (newest): right edge
- k = SamplePop-1 (oldest): left edge

**Vertical (Value)** (line 1359):
```pascal
y := (vMarginTop + vHeight - 1 - vBase[j]) shl 8 - Round((v - offset) * fScale);
```

**Formula**:
```
y = (top + height - 1 - base) × 256 - (value - offset) × scale
```

**Effect**:
- Bottom-to-top plotting
- Low values at bottom
- High values at top
- vBase offsets entire trace vertically

### 10.5 Point Rendering

**Code** (line 1360):
```pascal
DrawLineDot(x, y, color, k = SamplePop - 1)
```

**Same as LOGIC**: Connects points with lines (if vLineSize > 0) and/or draws dots (if vDotSize > 0).

---

## 11. Scaling and Positioning

### 11.1 Vertical Scaling Examples

**Example 1: Full-Scale ADC (0-1023)**:
```
vLow = 0
vHigh = 1023
vTall = 256
vBase = 0

fScale = 255 / 1023 × 256 = 63.81

Value 0:    y = (top + 255) × 256 - (0 - 0) × 63.81 = bottom
Value 512:  y = (top + 255) × 256 - 512 × 63.81 = middle
Value 1023: y = (top + 255) × 256 - 1023 × 63.81 = top
```

**Example 2: Signed Temperature (-40 to +85 °C)**:
```
vLow = -40
vHigh = 85
vTall = 256
vBase = 0

range = |85 - (-40)| = 125
fScale = 255 / 125 × 256 = 522.24

Value -40:  y = bottom
Value 0:    y = (top + 255) × 256 - (0 - (-40)) × 522.24 = middle-low
Value +85:  y = top
```

### 11.2 Overlay with Base Offsets

**Example: 3 Channels Stacked**:
```
CH1: vTall = 100, vBase = 0
CH2: vTall = 100, vBase = 100
CH3: vTall = 100, vBase = 200
```

**Result**:
- CH1: Bottom 100 pixels
- CH2: Middle 100 pixels
- CH3: Top 100 pixels

**Y Calculation**:
```
CH1: y = (top + height - 1 - 0) × 256 - ...
CH2: y = (top + height - 1 - 100) × 256 - ...
CH3: y = (top + height - 1 - 200) × 256 - ...
```

### 11.3 Inverted Range

**Configuration**:
```
vLow = 100
vHigh = -100
```

**Effect**:
- High values at bottom
- Low values at top
- Inverted display

**Code** (line 1353):
```pascal
if vHigh[j] > vLow[j] then offset := vLow[j] else offset := vHigh[j];
```

Handles inverted ranges correctly.

---

## 12. User Commands

### 12.1 Configuration Commands

| Command | Parameters | Purpose |
|---------|------------|---------|
| `TITLE` | 'string' | Set window title |
| `POS` | x y | Set window position |
| `SIZE` | width height | Set display dimensions (32-2048) |
| `SAMPLES` | count | Set horizontal resolution (16-2048) |
| `RATE` | divisor | Set display update rate (1-2048) |
| `DOTSIZE` | n | Set dot size (0-32, 0=no dots) — **single value**; the optional `{y}` form is SPECTRO/PLOT/BITMAP-only |
| `LINESIZE` | n | Set line thickness (0-32, 0=no lines) |
| `TEXTSIZE` | size | Set label font size (6-200) |
| `COLOR` | back grid | Set background and grid colors |
| `HIDEXY` | - | Hide mouse coordinates |
| Packing modes | `{ALT} {SIGNED}` | Set data packing format (12 opt-in modes; **default = unpacked**) |

### 12.2 Runtime Commands

| Command | Parameters | Purpose |
|---------|------------|---------|
| *string* | 'label' {AUTO\|low high} {tall} {base} {grid} {color} | Define / redefine a channel (positional) |
| `TRIGGER` | channel {AUTO\|arm fire} {offset} | Configure trigger (offset = sample index) |
| `HOLDOFF` | count | Set holdoff count (2-2048) |
| `CLEAR` | - | Clear display, reset SamplePop/vRateCount, suppress trigger indicator |
| `SAVE` | 'name' \| WINDOW {'name'} \| l t w h {'name'} | Save `Bitmap[1]` (front buffer), or desktop-scrape a region, to `name.bmp`. **Bare `SAVE` writes nothing.** |
| `CLOSE` | - | Close the window (parser-layer directive; the rest of the message executes first) |
| `PC_KEY` | - | Request keyboard state |
| `PC_MOUSE` | - | Request mouse position/color |

**All of the above are UPDATE-phase directives** — none of them may appear in the create message
(`SCOPE_Configure` is `while NextKey do`, 1161; only `CLOSE` is special, being handled above
`DebugDisplayUnit.pas` entirely, and it is ignored in a create message by design).

### 12.3 Channel Configuration Format

**String Element** (update phase only; strictly positional):
```
'label' {AUTO | low high} {tall} {base} {grid} {color}
```

---

## 13. Performance Characteristics

### 13.1 Memory Usage

**Sample Buffer**:
```
Y_SampleBuff: 2048 sets × 8 channels × 4 bytes = 64 KB
```

**Channel Configuration**:
```
Arrays (vAuto, vLow, vHigh, etc.): ~8 × 8 × 4 bytes = 256 bytes
Labels: 8 × ~20 bytes = 160 bytes
Total: ~400 bytes
```

**Display Bitmaps**:

Both bitmaps are **`pf24bit` — 3 bytes/pixel, BGR, no alpha** (`FormCreate` 597/599:
`Bitmap[0].PixelFormat := pf24bit;`), and `SetSize` (2956-2961) sizes them to the **client area**
(`vMarginLeft + vWidth + vMarginRight` × `vMarginTop + vHeight + vMarginBottom`), not to
`vWidth × vHeight`:

```
Typical (vWidth=512, vHeight=256; margins = ChrWidth, ChrHeight*2, ChrWidth, ChrWidth
         → at FontSize 10: ChrWidth ≈ 8, ChrHeight ≈ 16):

client ≈ (8 + 512 + 8) × (32 + 256 + 8) = 528 × 296
528 × 296 × 3 bytes × 2 bitmaps ≈ 937 KB  (~0.9 MB)
```

**Total**: ~1.0 MB (typical — 64 KB sample buffer + ~0.9 MB bitmaps + ~0.4 KB channel config)

### 13.2 Rendering Performance

**Auto-Ranging Cost**:
```
SCOPE_Range: O(n) where n = SamplePop
Called once per auto-ranging channel per draw
```

**Rendering Cost**:
```
Channels × Samples × DrawLineDot
Example: 4 channels × 512 samples = 2048 calls
```

### 13.3 Optimization Strategies

1. **Disable Auto-Ranging**: Use manual ranges for stable, faster rendering
2. **Rate Limiting**: Reduce update frequency with RATE parameter
3. **Reduce Samples**: Lower vSamples for fewer plot points
4. **Single Channel**: Monitor one signal at a time

---

## 14. Comparison with Other Display Types

### 14.1 SCOPE vs. LOGIC

**SCOPE Advantages**:
- Analog/continuous value visualization
- Auto-ranging for unknown signals
- Per-channel vertical scaling (vTall, vBase)
- Level-based triggering

**LOGIC Advantages**:
- More channels (32 vs. 8)
- Optimized for digital signals
- Edge-based triggering
- Multi-bit range mode

**Use Cases**:
- **SCOPE**: ADC values, temperatures, analog sensors
- **LOGIC**: Digital I/O, communication protocols

### 14.2 SCOPE vs. SCOPE_XY

**SCOPE Advantages**:
- Time-domain display
- Multiple independent channels
- Triggering support

**SCOPE_XY Advantages**:
- XY/polar plotting
- Phase relationship visualization
- Lissajous figures

**Use Cases**:
- **SCOPE**: Signal vs. time
- **SCOPE_XY**: Signal vs. signal (phase, trajectory)

---

## 15. Usage Examples

> **All examples follow the mandatory two-message pattern** — create with **keys only**, then feed the
> channel defs / `TRIGGER` / `HOLDOFF` in separate **update** messages addressed to the window's
> instance name. A channel def or `TRIGGER` on the create line prevents the window from being created
> (EF-003; `SCOPE_Configure`'s `while NextKey do`, line 1161). See §6.1.

### 15.1 Basic Single-Channel Scope

**Setup**:
```spin2
debug(`SCOPE MyScope)                 ' create (keys only)
debug(`MyScope 'ADC' AUTO)            ' update: channel def
```

**P2 Code**:
```spin2
repeat
  value := adc_read()
  debug(`MyScope `(value))
```

**Result**: Auto-ranging oscilloscope display of ADC values.

### 15.2 Multi-Channel with Fixed Ranges

**Setup**:
```spin2
debug(`SCOPE MyScope SIZE 512 256 SAMPLES 256)   ' create (keys only)
debug(`MyScope 'X' -100 100 128 0   0 $FF0000)   ' update: label low high tall base grid color
debug(`MyScope 'Y' -100 100 128 128 0 $00FF00)
```

**P2 Code**:
```spin2
repeat
  x := accelerometer_x()
  y := accelerometer_y()
  debug(`MyScope `(x,y))              ' one long per channel, in channel order
```

**Result**: Two channels (X/Y) with fixed ±100 range, stacked display.

### 15.3 Triggered Capture

**Setup**:
```spin2
debug(`SCOPE MyScope SAMPLES 512)        ' create (keys only)
debug(`MyScope 'SIGNAL' 0 1023)          ' update: channel def
debug(`MyScope TRIGGER 0 500 600 256)    ' update: channel 0, arm 500, fire 600, offset 256
```

**P2 Code**:
```spin2
repeat
  value := read_signal()
  debug(`MyScope `(value))
```

**Result**: Display updates when the signal on channel 0 rises from <500 (arm) to >600 (fire). With
`offset = 256` of `SAMPLES 512`, the trigger point sits **mid-screen**: the left half shows the 256
samples that led up to the trigger, the right half the 256 samples after it (see §4.3).

### 15.4 High-Speed with Rate Limiting

**Setup**:
```spin2
debug(`SCOPE MyScope SAMPLES 1024 RATE 100)   ' create (keys only)
debug(`MyScope 'DATA' AUTO)                   ' update: channel def
```

**P2 Code**:
```spin2
repeat
  value := fast_sample()
  debug(`MyScope `(value))
  waitx(10)
```

**Result**: Fast sampling, display updates every 100th sample set (reduces PC CPU load).

---

## 16. Implementation Details

### 16.1 Data Packing

**Same as LOGIC**: 12 **opt-in** packing modes, `LONGS_1BIT` … `BYTES_4BIT`, each optionally followed by
`ALT` and/or `SIGNED`. **With no packing keyword the window is UNPACKED** — `SetDefaults`:2915 →
`SetPack(0,…)` ⇒ `vPackCount = 1`, `vPackShift = 32`, `vPackMask = $FFFFFFFF` (one full 32-bit sample
per long). Packing is fixed at creation: the pack keys appear only in `SCOPE_Configure`, never in
`SCOPE_Update`.

**Example** (4 channels, `LONGS_8BIT` → `vPackCount = 4`):
```
Each long unpacks to 4 sub-samples, LOW byte first, distributed round-robin:
  byte0 → ch0, byte1 → ch1, byte2 → ch2, byte3 → ch3
⇒ exactly one complete 4-channel sample set per long.
Efficient for byte-range data (0-255; add SIGNED for -128..127)
```

### 16.2 Fixed-Point Arithmetic

**8.8 Format**: All coordinates use 8.8 fixed-point (left-shifted by 8).

**Example**:
```
x = 100 pixels → x_fixed = 100 << 8 = 25600
```

### 16.3 Sample Set Transmission Protocol

**Element Stream**:
```
ele_num: packed_value_1 (contains samples for all channels)
ele_num: packed_value_2
...
ele_end
```

**Unpacking**: Assembles complete sample sets before storing in buffer.

---

## 17. Element Array Protocol Specification

### 17.1 Protocol Overview

The SCOPE display receives configuration and sample data through an **element array protocol** that uses parallel arrays of types and values.

**Element Storage** (GlobalUnit.pas:126-127; `DebugDisplayLimit = 1100`, GlobalUnit.pas:35):
```pascal
DebugDisplayType:  array[0..DebugDisplayLimit - 1] of byte;      // type tags are BYTES
DebugDisplayValue: array[0..DebugDisplayLimit - 1] of integer;
```

**Capacity**: 1100 elements per message

Element `[0]` is the display type (`ele_dis`) and `[1]` the window name (`ele_nam`); directives begin at
`ptr := 2` (`FormCreate` 625-632).

### 17.2 SCOPE **Configuration** Message Example — keys only

`SCOPE_Configure` runs `while NextKey do` (1161), so the create message may contain **nothing but keys
and their numeric arguments**. A channel-def string here would end the parse (and, per EF-003, the
window would not be created at all):

```
Element Array (create message):
[0] type=ele_dis   value=dis_scope       → display type
[1] type=ele_nam   value=<ptr>           → 'MyScope' (window/instance name)
[2] type=ele_key   value=key_samples     → SAMPLES
[3] type=ele_num   value=512             → horizontal resolution
[4] type=ele_key   value=key_longs_16bit → LONGS_16BIT (packing)
[5] type=ele_end   value=0
```

### 17.3 SCOPE **Channel-Definition** Message Example (update phase)

Channel defs are parsed by `SCOPE_Update` 1217-1231, strictly **positionally**
(`label` → `AUTO | low high` → `tall` → `base` → `grid` → `color`):

```
Element Array (update message):
[0] type=ele_str   value=<ptr>           → 'Signal1'
[1] type=ele_num   value=0               → low
[2] type=ele_num   value=1023            → high
[3] type=ele_num   value=200             → tall
[4] type=ele_num   value=0               → base
[5] type=ele_num   value=15              → grid (%1111)
[6] type=ele_key   value=key_red         → color  (or ele_num $FF0000, via vColorMode)
[7] type=ele_end   value=0
```

A bare number immediately after the label is the **`low` bound** — it is never read as a color.

### 17.4 SCOPE Sample Data Message Example

Packed sub-samples are distributed **round-robin across the active channels** (§8.2), and `UnPack`
(4166-4171) yields the **low** sub-field first (`Result := v and vPackMask; v := v shr vPackShift`):

```
(2 channels, LONGS_16BIT SIGNED → vPackCount = 2; low half unpacked first)
Element Array:
[0] type=ele_num   value=$00640032       → set N:   ch0 = $0032 = 50,   ch1 = $0064 = 100
[1] type=ele_num   value=$FF9CFF38       → set N+1: ch0 = $FF38 = -200, ch1 = $FF9C = -100
[2] type=ele_end   value=0
```

---

## 18. Buffer Management and Timing

### 18.1 Single Interleaved Circular Buffer (not per-channel)

SCOPE uses **one** shared circular buffer holding interleaved sample sets — there is no per-channel array. The buffer and its pointers are declared once:

```pascal
Y_SampleBuff : array[0..Y_Sets * Y_SetSize - 1] of integer;   // line 361
SamplePtr    : integer;                                        // line 402
SamplePop    : integer;                                        // line 403
```

**Constants** (`Channels` = line **157**; `Y_SetSize`/`Y_Sets`/`Y_PtrMask` = lines **167-169**; `DataSets` = 155):
```
Channels  = 8            // also Y_SetSize: one slot per channel in each set
Y_Sets    = 2048         // number of sample sets (= DataSets = 1 shl 11)
Y_PtrMask = Y_Sets - 1   // 2047, circular wrap mask
Total = 2048 × 8 × 4 bytes = 65,536 bytes
```

A single write pointer `SamplePtr` and a single fill counter `SamplePop` are shared by **all** channels, because every channel's sample for one time-slot lives in the same set. There are no `SamplePtr[ch]`/`SamplePop[ch]` arrays and no `SamplePtrMask` symbol.

### 18.2 Write Operations

A full set (all active channels) is assembled in a local `samp` array, then block-copied into the buffer (`SCOPE_Update`, lines 1281-1283):

```pascal
Move(samp, Y_SampleBuff[SamplePtr * Y_SetSize], Y_SetSize shl 2);  // copy 8 longs (32 bytes)
SamplePtr := (SamplePtr + 1) and Y_PtrMask;
if SamplePop < vSamples then Inc(SamplePop);
```

`SamplePop` saturates at `vSamples` (the displayed width), not at `Y_Sets`. Any individual sample for set `k`-back, channel `j`, is read as:

```pascal
Y_SampleBuff[((SamplePtr - k - 1) and Y_PtrMask) * Y_SetSize + j]
```

### 18.3 Auto-Ranging Updates

There are **no** running `vMin/vMax/vScale/vCenter` accumulators. Range is recomputed from scratch by a full O(SamplePop) buffer scan in `SCOPE_Range` (lines 1366-1379), invoked at draw time for each auto channel (`SCOPE_Draw`, line 1346):

```pascal
for j := vIndex - 1 downto 0 do if vAuto[j] then SCOPE_Range(j, vLow[j], vHigh[j]);
```

`SCOPE_Range` writes the discovered min/max directly into `vLow[j]`/`vHigh[j]`. The pixel scale is then derived per draw (line 1352), not stored:

```pascal
fScale := (vTall[j] - 1) / Abs(Int64(vHigh[j]) - Int64(vLow[j])) * $100;
```

### 18.4 Trigger Detection

SCOPE triggering is **level-based** (arm/fire), not a single-level edge crossing, and is evaluated inline in `SCOPE_Update` (lines 1286-1332) immediately after each set is stored — never from a separate `prev_value`/`vTriggerLevel` comparison. The sample tested is read at the configured offset from the buffer:

```pascal
t := Y_SampleBuff[((SamplePtr - vTriggerOffset - 1) and Y_PtrMask) * Y_SetSize + vTriggerChannel];
```

See §9 for the full arm→fire state machine, holdoff, and free-run path.

---

## 19. Bitmap System and Double-Buffering

### 19.1 Bitmap Architecture

Two bitmaps, both **`pf24bit` — 3 bytes/pixel, BGR, no alpha** — created in `FormCreate` (lines 596-599) and freed in `FormDestroy` (lines 875-876):

```pascal
Bitmap : array[0..1] of TBitmap;   // line 257
Bitmap[0].PixelFormat := pf24bit;  // 597 — render target
Bitmap[1].PixelFormat := pf24bit;  // 599 — present buffer
```

`Bitmap[0]` is the off-screen render target; `Bitmap[1]` is the buffer drawn to the window canvas (and the one `SAVE 'name'` writes to disk). Both are sized to the full client area in `SetSize` (lines **2956-2961**, cached into `vBitmapWidth`/`vBitmapHeight` at 2963-2964); for SCOPE that is `vMarginLeft + vWidth + vMarginRight` × `vMarginTop + vHeight + vMarginBottom` — the **client area**, not `vWidth × vHeight` and certainly not an unconditional 512×512.

`BitmapToCanvas(0)` (lines 3522-3530) performs the present: copy `Bitmap[0]`→`Bitmap[1]`, then `Canvas.Draw(0,0,Bitmap[1])` (SCOPE is **not** in the StretchDraw set `[dis_spectro,dis_plot,dis_bitmap]`, so it blits 1:1, no stretch).

### 19.2 Trace Rendering

The real render loop is in `SCOPE_Draw` (lines 1355-1361). It walks the **single interleaved** buffer newest-to-oldest (`k` from `SamplePop-1` downto 0) and plots each point through `DrawLineDot` — there is no `SampleBuff[ch][idx]`, no `vCenter`/`vScale`, and no direct `SmoothLine`/`SmoothDot` calls here:

```pascal
for k := SamplePop - 1 downto 0 do
begin
  v := Y_SampleBuff[((SamplePtr - k - 1) and Y_PtrMask) * Y_SetSize + j];
  x := (vMarginLeft + vWidth - 1) shl 8 - Round(k / vSamples * vWidth * $100);
  y := (vMarginTop + vHeight - 1 - vBase[j]) shl 8 - Round((v - offset) * fScale);
  DrawLineDot(x, y, color, k = SamplePop - 1)
end;
```

`DrawLineDot` (lines 3423-3431) is the only line/dot API and decides between the two primitives by configured size — it connects to the previous point with `SmoothLine` when `vLineSize > 0` (and not the first point), and overlays `SmoothDot` when `vDotSize > 0`. The boolean argument is `k = SamplePop - 1` (the oldest point, drawn first), which suppresses the connecting line on the first plotted point:

```pascal
if (vLineSize > 0) and not first then SmoothLine(vPixelX, vPixelY, x, y, vLineSize shl 6, color, $FF);
if (vDotSize > 0)             then SmoothDot(x, y, vDotSize shl 7, color, $FF);
vPixelX := x;  vPixelY := y;
```

There is no `vLineStyle` boolean in SCOPE; line-vs-dot is purely a function of `vLineSize`/`vDotSize` (both may be active simultaneously).

### 19.3 Vertical Scaling and Grid

`vTall[j]` is a **per-channel pixel span**, not a divisor of `vHeight/vIndex`. `vBase[j]` is a **per-channel pixel offset** subtracted from the baseline, not a percentage. Both feed the fixed-point `y` formula above directly (line 1359): the bottom of channel `j`'s band sits at `vMarginTop + vHeight - 1 - vBase[j]`, and `fScale = (vTall[j]-1)/|vHigh[j]-vLow[j]| × $100` maps value units to sub-pixels.

`vGrid[j]` **is** rendered — in `ClearBitmap` for the `dis_scope` case (lines 3290-3333), it is a 4-bit flag mask drawn as dotted grid lines / value labels in a channel-tinted color (`AlphaBlend(vColor[i], vBackColor, $40)`):

| Bit | Value | Drawn |
|---|---|---|
| 0 | 1 | baseline line at `vBase[i]` (3298-3303) |
| 1 | 2 | top line at `vBase[i]+vTall[i]` (3304-3309) |
| 2 | 4 | min-value text label at baseline (3310-3321) |
| 3 | 8 | max-value text label at top (3322-3333) |

`ClearBitmap` also draws the plot frame (3287-3289), channel name labels (3366+), and, when `vTriggered`, a dotted trigger-position indicator line (3337-3357).

---

## 20. Shared Infrastructure

### 20.1 Color System

```pascal
DefaultScopeColors: array[0..7] of integer = (
  clLime,     // $00FF00 — Lime green
  clRed,      // $FF0000 — Red
  clCyan,     // $00FFFF — Cyan
  clYellow,   // $FFFF00 — Yellow
  clMagenta,  // $FF00FF — Magenta
  clBlue,     // $7F7FFF — Blue
  clOrange,   // $FF7F00 — Orange
  clOlive     // $7F7F00 — Olive
);
```

**Source Location**: Line 241 in DebugDisplayUnit.pas

> **`clLime` is a Delphi `clXxx` palette constant — it is NOT a DEBUG colour keyword.** The DEBUG
> keyword that names `$00FF00` is **`GREEN`**. The two colour systems are distinct: `DefaultScopeColors`
> is written in Delphi's vocabulary, while a channel def's `color` element takes a DEBUG keyword
> (`GREEN`, `RED`, …, each optionally followed by a 0-15 brightness nibble — except `BLACK`/`WHITE`,
> which take none) or a **numeric** value interpreted through the current `vColorMode`
> (`TranslateColor`, 3090-3173; default `key_rgb24`, `SetDefaults` 2889).

### 20.2 Data Packing System

**Default: unpacked** (`SetDefaults`:2915 → `SetPack(0, False, False)` — one full 32-bit sample per
long, unsigned). When a packing mode *is* selected, SCOPE typically uses:
- **LONGS_16BIT**: 2 sub-samples per long (append `SIGNED` for signed values)
- **LONGS_8BIT**: 4 sub-samples per long (append `SIGNED` for signed values)

```pascal
// UnPack (lines 4166-4171)
function TDebugDisplayForm.UnPack(var v: integer): integer;
begin
  Result := v and vPackMask;
  v := v shr vPackShift;                                          // advance to next sub-sample
  if vPackSignx and (Result shr (vPackShift - 1) and 1 = 1) then  // sign-extend only when SIGNED set
    Result := Result or ($FFFFFFFF xor vPackMask);
end;
```

The unpack state uses `vPackMask`, `vPackShift`, and `vPackSignx` (set by `KeyPack` 2817-2832 → `SetPack`); there is no `vPackSize`/`vPackIndex` counter. `SCOPE_Update` iterates `vPackCount` sub-samples per transmitted value (line 1272), each obtained from a fresh `v := NewPack` (line 1271). **`UnPack` yields the LOW sub-field first**, then shifts `v` right for the next one.

**Sign extension is a RUNTIME flag, not a property of the mode.** `PackDef` (140-152) encodes `0 shl 16`
for *every* entry and `SetPack` reads only bits 0-15 — so no mode is "inherently signed". Sign-extension
happens only when the trailing `SIGNED` keyword set `vPackSignx` **and** the sub-sample's own top bit is 1
(4170).

**`ALT`** (`NewPack`, 4158-4164) applies three **cumulative** guards (`vPackShift <= 1`, `<= 2`, `<= 4`).
For a 1-bit mode all three fire ⇒ each byte's 8 bits are **fully reversed** (`$01 → $80`) — it is *not* a
stage-1 adjacent-bit swap. For `*_2BIT` only the pair+nibble swaps apply; for `*_4BIT` only the nibble
swap; for 8/16/32-bit modes `ALT` is a no-op. `NewPack` **consumes no elements** — it begins
`Result := val;`, reusing the value already latched by the enclosing `while NextNum do`.

### 20.3 Fixed-Point Arithmetic

**8.8 fixed-point** for sub-pixel rendering. `SCOPE_Draw` builds `x`/`y` in `<<8` units (lines 1358-1359) and `DrawLineDot` (3423-3431) scales pen/dot sizes the same way — **`vLineSize shl 6` at line 3426**, **`vDotSize shl 7` at line 3428** (line 3427 is only the `if (vDotSize > 0) then` test):
```pascal
x := (vMarginLeft + vWidth - 1) shl 8 - Round(k / vSamples * vWidth * $100);  // 1358
y := (vMarginTop + vHeight - 1 - vBase[j]) shl 8 - Round((v - offset) * fScale); // 1359
```

> **The shift constants are code fact; the rendered widths are not derivable from them.**
> `LINESIZE 3` — despite `shl 6` — renders as **3 whole pixels** (hardware-measured, EF-027): the
> anti-aliasing envelope in `SmoothLine` widens small radii, so the tidy "half-pixel" arithmetic does
> not predict what appears on screen. Because that derivation demonstrably fails for `LINESIZE`, it
> cannot be trusted for `DOTSIZE` either: **`DOTSIZE`'s rendered width has never been measured —
> NEEDS-HARDWARE.** This document therefore does not claim `DOTSIZE` is a radius *or* a diameter.

---

## 21. Initialization Lifecycle

### 21.1 Window Creation Sequence

The real lifecycle runs entirely in `FormCreate` (lines **591-645**), which dispatches to `SCOPE_Configure` for `dis_scope` (635) and ends with `Show;` (644). There is no `vLineStyle`/`vTrigger` boolean, no per-channel buffer init loop, and `vAuto` defaults to **False**, not True.

```pascal
// FormCreate (591-645), abridged
Bitmap[0] := TBitmap.Create;  Bitmap[0].PixelFormat := pf24bit;   // 596-597
Bitmap[1] := TBitmap.Create;  Bitmap[1].PixelFormat := pf24bit;   // 598-599
vTextSize := FontSize;  SetTextMetrics;                           // 601-602
// ... cursor/desktop bitmaps, polar colors ...
DisplayType := P2.DebugDisplayValue[0];                           // 625
SetCaption(PChar(P2.DebugDisplayValue[1]) + ' - ' + TypeName[DisplayType]); // 626
Left := P2.DebugDisplayLeft;  Top := P2.DebugDisplayTop;          // 628-629
SetDefaults;                                                       // 631 (2880-2917)
ptr := 2;
case DisplayType of                                                // 633
  dis_scope: SCOPE_Configure;                                      // 635
  ...
end;                                                               // 643
Show;                                                              // 644
```

`SetDefaults` (lines 2880-2917) primes the shared state before SCOPE's own defaults: `vWidth:=256`, `vHeight:=256`, `vSamples:=256`, `vIndex:=0`, `vColor[i]:=DefaultScopeColors[i]` for all 8 channels (line 2888), `vColorMode:=key_rgb24`, `vLabel[i]:=''` (2914), and — critically — **`SetPack(0, False, False)` (2915) ⇒ the window starts UNPACKED** (1 sample/long, 32-bit, unsigned). `SCOPE_Configure` then overrides `vRate:=1`, `vDotSize:=0`, `vLineSize:=3`, `vTextSize:=FontSize` (lines 1156-1159). **No window sets a packing default of its own.**

### 21.2 Configuration Parameter Processing

`SCOPE_Configure` parses **keys only** (lines 1161-1186); channel-label strings and `TRIGGER`/`HOLDOFF` are handled later by `SCOPE_Update`, not here. There is no `key_tall`/`key_base`/`key_line`/`key_dot` and no `KeyRange`:

```pascal
while NextKey do
case val of
  key_title:    KeyTitle;
  key_pos:      KeyPos;
  key_size:     KeySize(vWidth, vHeight, scope_wmin, scope_wmax, scope_hmin, scope_hmax);
  key_samples:  KeyValWithin(vSamples, 16, Y_Sets);
  key_rate:     KeyValWithin(vRate, 1, Y_Sets);
  key_dotsize:  KeyValWithin(vDotSize, 0, 32);
  key_linesize: KeyValWithin(vLineSize, 0, 32);
  key_textsize: KeyTextSize;
  key_color:    if KeyColor(vBackColor) then KeyColor(vGridColor);
  key_hidexy:   vHideXY := True;
  key_longs_1bit..key_bytes_4bit: KeyPack;
end;
```

### 21.3 Channel-Default and Trigger Initialization

After key parsing, `SCOPE_Configure` (lines 1188-1203) forces a dot if no rendering mode is set, then initializes the per-channel arrays and trigger state. Note `vAuto[i] := False` (manual ranging is the default) and the full-32-bit initial range:

```pascal
if (vDotSize = 0) and (vLineSize = 0) then vDotSize := 1;     // 1188
for i := 0 to Channels - 1 do
begin
  vAuto[i] := False;          // NOT True
  vLow[i]  := -$80000000;
  vHigh[i] := $7FFFFFFF;
  vTall[i] := vHeight;
  vBase[i] := 0;
  vGrid[i] := 0;
end;
vTriggerChannel := -1;        // trigger disabled (free-run) by default
vTriggerAuto    := False;
vTriggerArm     := -1;
vTriggerFire    := 0;
vTriggerOffset  := vSamples div 2;
vHoldOff        := vSamples;
```

There are no `vMin/vMax/vCenter/vScale` accumulators to initialize (see §18.3). `SamplePtr`/`SamplePop` are plain integers reset to 0 by global allocation / `CLEAR`, not a per-channel loop.

### 21.4 Form Metrics and Bitmap Sizing

`SCOPE_Configure` closes by establishing text metrics and margins (lines 1204-1206):

```pascal
SetTextMetrics;
SetSize(ChrWidth, ChrHeight * 2, ChrWidth, ChrWidth);  // left, top, right, bottom margins
```

`SetSize` (lines 2926-2970) sets the client area to `margins + vWidth/vHeight`, sizes **both** bitmaps to that client area (2958-2961), caches `vBitmapWidth`/`vBitmapHeight`, rebuilds the `BitmapLine` scanline table, then clears the bitmap with `vTriggered := False; ClearBitmap`.

### 21.5 Cleanup and Destruction

Bitmaps are released in `FormDestroy` (lines 875-876); the form's timers are freed in the `Destroy` destructor (lines 580-582):

```pascal
Bitmap[0].Free;   // FormDestroy, 875
Bitmap[1].Free;   // FormDestroy, 876
```

---

## 22. Summary

The **SCOPE** display window is a comprehensive multi-channel oscilloscope for the Propeller 2 debug environment, providing real-time analog signal visualization with automatic and manual scaling, level-based triggering, and flexible display control.

**Usage in one line**: **create with keys only, then feed channel defs / `TRIGGER` / `HOLDOFF` in
separate update messages** — `SCOPE_Configure` is a key-only parser (1161), and a channel def on the
create line prevents the window from being created (EF-003).

**Key Capabilities**:
- Up to 8 analog channels with independent configuration (a 9th def overwrites channel 8)
- Auto-ranging or manual range specification per channel
- Level-based triggering with rising/falling edge detection
- Vertical scaling (vTall) and offset (vBase) for channel overlay
- Single 2048-set interleaved circular buffer (shared `SamplePtr`/`SamplePop`)
- Rate limiting and holdoff for display control
- Anti-aliased trace rendering with lines and/or dots

**Performance Profile**:
- 64 KB sample buffer
- Auto-ranging: O(n) per channel per draw
- Rendering: O(channels × samples)
- Efficient for 4-8 channels at 256-512 samples

**Common Use Cases**:
- ADC monitoring and visualization
- Sensor data logging (temperature, pressure, etc.)
- Signal waveform analysis
- Multi-channel comparison
- Triggered event capture

The SCOPE window integrates seamlessly with the P2 debug ecosystem, providing oscilloscope-grade visualization for analog signal debugging and analysis.

---

**End of SCOPE Theory of Operations**
