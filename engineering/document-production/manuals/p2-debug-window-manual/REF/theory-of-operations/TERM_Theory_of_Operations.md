# TERM Display Window - Theory of Operations

**Current as of**: PNut v55 for Propeller 2
**Directive coverage verified**: 2026-06-01 against `DebugDisplayUnit.pas` (v55)
**Re-ratified against raw v55**: 2026-07-14 — conflict-audit conformance pass (control-code
model, lazy column wrap, color-pair naming, `SAVE`/`CLOSE` grammar, worked examples, citations)
**Companion**: [Debug Window Directive Matrix](../DEBUG-WINDOW-DIRECTIVE-MATRIX.md) — cross-window config/display/keyboard/mouse reference

> **TS parity (2026-06-06):** `DebugTermWindow` was brought to parity by the 9-window parity
> sprint **§14** (build 0.9.27): runtime named colors + `BACKCOLOR`, the numeric control codes
> **2** / **3** (set column / set row) consuming their following numeric parameter (no
> double-dispatch), `CR`+`LF` collapsing to a single newline, default 10pt font, and
> `SIZE`/`TEXTSIZE` clamping. See matrix §8 and `termResidualsParity.test.ts`.
>
> ⚠️ **TERM has no `SET` directive.** `key_set` (= 77, line 112) is a PLOT/BITMAP keyword and
> is accepted by neither `TERM_Configure` (2193-2211) nor `TERM_Update` (2230-2255). Cursor
> placement in TERM is done with the numeric control codes **2** and **3** (2272-2275).

## Table of Contents

1. [Overview](#1-overview)
2. [Display Type and Constants](#2-display-type-and-constants)
3. [Data Structures](#3-data-structures)
4. [Configuration and Initialization](#4-configuration-and-initialization)
5. [Update Processing](#5-update-processing)
6. [Character Rendering](#6-character-rendering)
7. [Cursor Management](#7-cursor-management)
8. [Scrolling System](#8-scrolling-system)
9. [Control Commands](#9-control-commands)
10. [Color System](#10-color-system)
11. [Text Metrics](#11-text-metrics)
12. [Command Protocol](#12-command-protocol)
13. [Usage Examples](#13-usage-examples)
14. [Performance Characteristics](#14-performance-characteristics)
15. [Terminal Emulation](#15-terminal-emulation)
16. [Implementation Details](#16-implementation-details)
17. [Element Array Protocol Specification](#17-element-array-protocol-specification)
18. [Buffer Management and Timing](#18-buffer-management-and-timing)
19. [Bitmap System and Double-Buffering](#19-bitmap-system-and-double-buffering)
20. [Shared Infrastructure](#20-shared-infrastructure)
21. [Initialization Lifecycle](#21-initialization-lifecycle)
22. [Summary](#22-summary)

---

## 1. Overview

### 1.1 Purpose

The **TERM** (Terminal) display window provides a text-based terminal emulator for the Propeller 2 debug system. It implements a character-mode display similar to classic computer terminals or console windows, supporting:

- **Character-based display**: Grid of text characters (columns × rows)
- **Multiple colors**: Configurable foreground and background colors with 4 predefined color pairs
- **Auto-scrolling**: Automatic vertical scrolling when bottom is reached
- **Cursor positioning**: Explicit row/column positioning
- **Control codes**: Tab, backspace, newline, clear screen, home
- **VT100-style features**: Basic terminal emulation without full ANSI escape sequences
- **Real-time updates**: Immediate or buffered display updates

### 1.2 Key Features

- **Configurable size**: 1-256 columns, 1-256 rows (default: 40×20)
- **Proportional font support**: Uses Windows TrueType fonts with dynamic sizing
- **Color pairs**: 4 predefined text/background color combinations (two colors × inverse video)
- **Control codes**: clear+home (0), home (1), set column (2 *n*), set row (3 *n*), select color
  pair 0-3 (4-7), backspace (8), tab (9), newline (10, 13) — codes **11, 12 and 14-31 are inert**
- **String output**: Efficient multi-character string rendering
- **Position commands**: Explicit cursor positioning (row, column)
- **Update modes**: Real-time character-by-character or buffered batch updates
- **Scrolling**: Automatic vertical scrolling with bitmap copying
- **Clear screen**: Instant screen clear with home cursor
- **Save display**: Save terminal contents to image file

### 1.3 Typical Applications

- **Debug output**: Program status, variable dumps, trace messages
- **Data logging**: Timestamped event logs, sensor readings
- **Menu systems**: Text-based user interfaces
- **Serial console**: Terminal emulator for serial communications
- **Status displays**: Real-time system status monitoring
- **Interactive debugging**: Command-response debugging sessions
- **Test output**: Unit test results, pass/fail reports

---

## 2. Display Type and Constants

### 2.1 Display Type Identifier

**DebugDisplayUnit.pas:28**
```pascal
const
  dis_term = 6;
```

The TERM display is identified by `dis_term = 6` in the display type enumeration.

### 2.2 Terminal Size Constants

**DebugDisplayUnit.pas:203-204, 224-227**
```pascal
const
  DefaultCols           = 40;
  DefaultRows           = 20;

  term_colmin           = 1;
  term_colmax           = 256;
  term_rowmin           = 1;
  term_rowmax           = 256;
```

**Constants**:
- **DefaultCols**: Default columns = 40
- **DefaultRows**: Default rows = 20
- **term_colmin**: Minimum columns = 1
- **term_colmax**: Maximum columns = 256
- **term_rowmin**: Minimum rows = 1
- **term_rowmax**: Maximum rows = 256

### 2.3 Default Colors

**DebugDisplayUnit.pas:242**
```pascal
const
  DefaultTermColors: array[0..7] of integer =
    (clOrange, clBlack, clBlack, clOrange, clLime, clBlack, clBlack, clLime);
```

**Color Pairs** — the four defaults are **two colors × two inverse-video variants**:
- **Pair 0**: ORANGE text on BLACK background (indices 0-1)
- **Pair 1**: BLACK text on ORANGE background (indices 2-3) — *inverse of pair 0*
- **Pair 2**: GREEN text on BLACK background (indices 4-5)
- **Pair 3**: BLACK text on GREEN background (indices 6-7) — *inverse of pair 2*

**Interpretation**:
```
vColor[0] = clOrange   // Pair 0 foreground
vColor[1] = clBlack    // Pair 0 background
vColor[2] = clBlack    // Pair 1 foreground  (inverse video)
vColor[3] = clOrange   // Pair 1 background
vColor[4] = clLime     // Pair 2 foreground  ($00FF00 — pure green)
vColor[5] = clBlack    // Pair 2 background
vColor[6] = clBlack    // Pair 3 foreground  (inverse video)
vColor[7] = clLime     // Pair 3 background
```

> ⚠️ **`clLime` is a Delphi palette constant, not a DEBUG color keyword.** The two color
> systems are **distinct**:
> - **`clXxx` constants** (`DebugDisplayUnit.pas` 179-191) are literal RGB24 values used
>   *inside* the Pascal — `clLime = $00FF00`, `clOrange = $FF7F00`, `clBlack = $000000`.
>   `DefaultTermColors` (242) is written in this vocabulary.
> - **DEBUG color keywords** are what a user writes in a `debug()` directive:
>   `BLACK WHITE ORANGE BLUE GREEN CYAN RED MAGENTA YELLOW GRAY` (`key_black = 0` …
>   `key_gray = 9`, lines 32-41). **There is no `LIME` keyword** — the green keyword is
>   **`GREEN`** (`key_green = 4`, line 36).
>
> So pair 2's default *value* is `$00FF00`, and the *keyword* that names green is `GREEN`.
> The keyword path is not a literal lookup: `KeyColor` (2770-2775) routes the eight hues
> `ORANGE..GRAY` through `TranslateColor(h shl 5 or p shl 1, key_rgbi8x)`, so `GREEN` at a
> given brightness need not equal `$00FF00` exactly.

---

## 3. Data Structures

### 3.1 Terminal State Variables

**DebugDisplayUnit.pas:343-346**
```pascal
var
  vCols                 : integer;  // Number of columns
  vRows                 : integer;  // Number of rows
  vCol                  : integer;  // Current cursor column (0-based)
  vRow                  : integer;  // Current cursor row (0-based)
```

**Characteristics**:
- **vCols, vRows**: Terminal grid dimensions
- **vCol, vRow**: Current cursor position (0-based indexing)
- **Valid ranges**: `vCol ∈ [0, vCols]`, `vRow ∈ [0, vRows-1]` — `vCol` may legitimately
  rest **at `vCols`** (a "pending wrap"; the wrap is lazy, `TERM_Chr:2340`/`2347` — see §7.3)

### 3.2 Color Array

**DebugDisplayUnit.pas:311**
```pascal
var
  vColor: array [0..Channels - 1] of integer;  // Channels = 8
```

**Purpose**: Stores 8 color values defining 4 foreground/background pairs.

**Color Selection**:
```pascal
vTextColor := vColor[(pair_index) * 2 + 0];      // Foreground
vTextBackColor := vColor[(pair_index) * 2 + 1];  // Background
```

### 3.3 Text Metrics Variables

**DebugDisplayUnit.pas:254-255**
```pascal
var
  ChrHeight             : integer;  // Character cell height (pixels)
  ChrWidth              : integer;  // Character cell width (pixels)
```

**Purpose**: Stores pixel dimensions of a single character cell, calculated from font size.

### 3.4 Update Control

**DebugDisplayUnit.pas**
```pascal
var
  vUpdate               : boolean;  // Update mode flag
  vUpdateFlag           : boolean;  // Pending update flag
```

**Update Modes**:
- **vUpdate = False** (default): Real-time character-by-character display
- **vUpdate = True**: Buffered mode, manual update required

---

## Directive Reference (v55-verified)

This section is the single authoritative lookup for every directive TERM accepts,
verified against `DebugDisplayUnit.pas` (v55) on 2026-06-01. See the
[Directive Matrix §5.7](../DEBUG-WINDOW-DIRECTIVE-MATRIX.md) for the cross-window
view.

### Configuration directives

Processed once by `TERM_Configure` (lines 2181-2221). Applied before the window
opens.

| Directive | Pascal key | Parameters | Range / notes |
|-----------|-----------|------------|---------------|
| `TITLE 'str'` | `key_title` | string | Free string · window title bar text |
| `POS left top` | `key_pos` | 2 integers | left, top · offset from base window position |
| `SIZE cols rows` | `key_size` | 2 integers | **Columns × rows** (not pixels); cols int **1..256** · default 40; rows int **1..256** · default 20. **Assign-and-clamp** by `KeySize(…, term_colmin, term_colmax, term_rowmin, term_rowmax)` (`2199-2200`; constants `term_colmin/_rowmin`=1, `term_colmax/_rowmax`=**256**, lines 224-227) — out-of-range is *saturated*, never ignored: `SIZE 300 200` ⇒ **256 × 200** |
| `TEXTSIZE n` | `key_textsize` | integer | Font point size · int **6..200** · default 10 (global `FontSize` user preference); applied via `KeyTextSize` |
| `COLOR c0 c1 … c7` | `key_color` | up to 8 color values | Fills `vColor[0..7]` — 4 text/background pairs; reads up to 8, stops early if a value is absent (`2203-2204`). Each value is a named color keyword ([Directive Matrix §7.1](../DEBUG-WINDOW-DIRECTIVE-MATRIX.md) — optional 0–15 brightness nibble, but **not** for `BLACK`/`WHITE`; see the named-color notes below) **or** numeric (interpreted through `vColorMode`, which for TERM is always the `SetDefaults` value **RGB24**, 2889). **`COLOR` is config-only for TERM** — `TERM_Update` has no `key_color` arm (see below). Default: pair0 `ORANGE/BLACK`, pair1 `BLACK/ORANGE`, pair2 `GREEN/BLACK`, pair3 `BLACK/GREEN` (`DefaultTermColors`, 242 — pairs 1 & 3 are inverse video) |
| `BACKCOLOR color` | `key_backcolor` | 1 RGB24 value | Window canvas background (used for clear/scroll fill), not character background (`2205-2206`) |
| `UPDATE` | `key_update` | *(flag)* | Enables buffered mode — screen only updates on explicit `UPDATE` directive (`2207-2208`) |
| `HIDEXY` | `key_hidexy` | *(flag)* | Hides the live measurement-cursor coordinate readout; does **not** disable `PC_MOUSE` (`2209-2210`) |

### Display / data directives

Processed on every subsequent message by `TERM_Update` (lines 2223-2315).

> **TERM does NOT accept `COLOR` in the update phase.** `TERM_Update`'s key `case`
> (2231-2255) contains only `key_black..key_gray` (2232), `key_backcolor` (2238),
> `key_clear`, `key_update`, `key_save`, `key_pc_key`, `key_pc_mouse` — **there is no
> `key_color` arm**. `COLOR` is accepted only by `TERM_Configure` (2203-2204). (PLOT
> accepts `COLOR` in *both* phases — `PLOT_Update:1934` reads
> `key_color, key_black..key_gray:` — which is why the shared Matrix row is misleading
> for TERM.)

**Named-color key directives** (`key_black`..`key_gray`, lines 2232-2237):

| Directive | Action |
|-----------|--------|
| `ORANGE` `BLUE` `GREEN` `CYAN` `RED` `MAGENTA` `YELLOW` `GRAY` `{brightness 0..15}` | Sets `vTextColor` (text foreground), then `KeyColor` is called a **second time** (2236) and sets `vTextBackColor` **if** another color element follows. The optional brightness nibble (default **8**) applies **only** to these eight hues; they are computed through RGBI8X: `c := TranslateColor(h shl 5 or p shl 1, key_rgbi8x)` (`KeyColor:2770-2775`). |
| `BLACK` `WHITE` | Same two-slot behavior, but these take **NO brightness nibble** — `KeyColor:2764-2768` returns the fixed literals `$000000` / `$FFFFFF` and never calls `NextNum`. ⚠️ **Trap:** `TERM BLACK 8` does *not* mean "black, brightness 8" — the `8` is left in the element stream, where the **second** `KeyColor` (2236) eats it as a **numeric background color**. |
| `BACKCOLOR color` | Sets `vTextBackColor` only (`key_backcolor`, lines 2238-2239) |

**Keyword directives**:

| Directive | Action |
|-----------|--------|
| `CLEAR` | `key_clear` — clear entire bitmap, home cursor to (0,0), set update flag (lines 2240-2246) |
| `UPDATE` | `key_update` — immediately copy `Bitmap[0]` to canvas (`BitmapToCanvas(0)`), line 2247-2248 |
| `SAVE …` | `key_save` — six forms, see the **SAVE grammar** below (`KeySave`, 2839-2866; dispatched at 2249-2250) |
| `CLOSE` | `key_close` (= 49, line 84) — closes this window and **reclaims its display slot**. It has **no arm in any `_Update` case statement** — it is dispatched a layer up, in the **parser** (`p2com.asm:19565-19572` flags it; 19613-19624 reverts the name symbol and clears the display's bit in `debug_display_ena`), after which `TDebugForm.ChrIn` (`DebugUnit.pas:236-237`) runs the full `UpdateDisplay(...)` and *then* closes the form. **Command-only** (ignored in a new-display declaration), **multi-target** (`` `Term1 Term2 CLOSE `` closes both), and **update-first, close-second** (`` `MyTerm SAVE 'shot' CLOSE `` saves, *then* closes). |
| `PC_KEY` | `key_pc_key` — transmit latched keypress LONG to P2 (`SendKeyPress`, line 2251-2252) |
| `PC_MOUSE` | `key_pc_mouse` — transmit mouse position + buttons LONG pair to P2 (`SendMousePos`, line 2253-2254) |

**`SAVE` grammar** (`KeySave`, 2839-2866) — **six forms; three of them silently write nothing**:

| Form | Writes |
|------|--------|
| `SAVE 'name'` | `Bitmap[1]` (the **front/display** buffer) → `name.bmp` (2843) |
| `SAVE WINDOW 'name'` | desktop **scrape** of the window's *outer* rect — **includes title bar and borders**, and is vulnerable to occlusion (2846-2864) |
| `SAVE left top width height 'name'` | desktop scrape of an arbitrary screen region (2856-2864) |
| `SAVE WINDOW` | captures to memory, **no file** (the trailing `if NextStr` at 2864 fails) |
| `SAVE l t w h` | captures to memory, **no file** |
| `SAVE` (bare) | `Exit` — **nothing at all** |

The filename always comes **last**; the `.bmp` extension is appended. ⚠️ **Sharp edge:** a
non-`WINDOW` keyword after `SAVE` is **consumed and then discarded** by the `Exit` at 2848 —
`` `MyTerm SAVE CLEAR `` does nothing **and eats the `CLEAR`**. ⚠️ Because `SAVE 'name'` writes
`Bitmap[1]`, a `SAVE` issued in buffered (`UPDATE`) mode *before* the explicit `UPDATE` writes
the **stale previous frame**.

**Numeric control codes** (lines 2258-2305, `ele_num` values). Each is a numeric
element in the **0..13** control range or **32..255** printable range. Codes **0-7
are acting codes**, not "unsupported" — they are the cursor/screen/color command set.
Numbers **11, 12 and 14–31** have no `case` arm and fall through with **no action**
(silently ignored — never printed):

| Value | Parameter range | Action |
|-------|-----------------|--------|
| `0` | — | Clear screen + home cursor (0,0) |
| `1` | — | Home cursor to (0,0), no clear |
| `2 n` | `n` int **0..vCols−1** (clamped, `2273`) | Set column to `n` via `KeyValWithin(vCol, 0, vCols-1)` |
| `3 n` | `n` int **0..vRows−1** (clamped, `2275`) | Set row to `n` via `KeyValWithin(vRow, 0, vRows-1)` |
| `4` | — | Select color pair 0 → `vColor[0]`/`vColor[1]` |
| `5` | — | Select color pair 1 → `vColor[2]`/`vColor[3]` |
| `6` | — | Select color pair 2 → `vColor[4]`/`vColor[5]` |
| `7` | — | Select color pair 3 → `vColor[6]`/`vColor[7]` |
| `8` | — | Backspace — move cursor back one, wrap to previous row; no-op at (0,0) |
| `9` | — | Tab — print spaces until next 8-column boundary (minimum 1 space) |
| `10` | — | Line feed — treated identically to CR (calls `TERM_Chr(Chr(13))`) |
| `13` | — | Carriage return — advance to next row (or scroll), reset column to 0; consumes a following `10` if present |
| `32..255` | — | Printable character — render glyph at current cursor, advance column |

**String** (`ele_str`): Prints each character of the string verbatim via `TERM_Chr`
(lines 2307-2311). Characters in the string that happen to be control-code values
(e.g. `Chr(13)`) are passed directly to `TERM_Chr` and act as newlines.

### Keyboard & mouse

TERM uses the **shared input model** inherited by all nine display windows — there
is no TERM-specific keyboard or mouse handler. See
[Directive Matrix §4](../DEBUG-WINDOW-DIRECTIVE-MATRIX.md) for the full shared
model. TERM-specific notes:

| Handler | Lines | TERM behavior |
|---------|-------|---------------|
| `WMGetDlgCode` | 585-589 | Captures Tab key (all windows) |
| `FormKeyPress` | 825-831 | Latches key byte into `vKeyPress` for 100 ms |
| `FormKeyDown` | 833-851 | Maps non-printable keys: Left=1, Right=2, Up=3, Down=4, Home=5, End=6, Delete=7, Insert=10, PageUp=11, PageDown=12 |
| `FormMouseMove` | 725-732 | Displays character **col,row** as live measurement cursor; empty string (no readout) if cursor is outside the text area |
| `FormMouseWheel` | 811-817 | Latches wheel direction (+1/−1) into `vMouseWheel` for 100 ms |
| `PC_KEY` → `SendKeyPress` | 3579-3583 | Sends one LONG = `vKeyPress` byte (0 if none), then clears it |
| `PC_MOUSE` → `SendMousePos` | **3537-3577** (TERM char-cell mapping at 3563-3567) | LONG 1: `x` = char column, `y` = char row (the TERM `div ChrWidth`/`div ChrHeight` transform, 3563-3567), wheel bits 26-27 (3569), L/M/R buttons bits 28-30 (3570-3572); if cursor is **outside the text area** (margin-bounded character grid), LONG 1 = `$03FFFFFF`, LONG 2 = `$FFFFFFFF` (off-window sentinel, 3543-3549). LONG 2: RGB color under cursor (3553-3554) |

`HIDEXY` suppresses the on-screen readout from `FormMouseMove` but does **not**
prevent `PC_MOUSE` from reporting coordinates back to the P2.

---

## 4. Configuration and Initialization

### 4.1 TERM_Configure Method

**DebugDisplayUnit.pas:2181-2221**
```pascal
procedure TDebugDisplayForm.TERM_Configure;
var
  i: integer;
begin
  // Set unique defaults
  vTextSize := FontSize;
  vCols := DefaultCols;           // 40 columns
  vRows := DefaultRows;           // 20 rows
  vCol := 0;                      // Home cursor
  vRow := 0;
  for i := 0 to 7 do vColor[i] := DefaultTermColors[i];

  // Process any parameters
  while NextKey do
  case val of
    key_title:
      KeyTitle;
    key_pos:
      KeyPos;
    key_size:
      KeySize(vCols, vRows, term_colmin, term_colmax, term_rowmin, term_rowmax);
    key_textsize:
      KeyTextSize;
    key_color:
      for i := 0 to 7 do if not KeyColor(vColor[i]) then Break;
    key_backcolor:
      KeyColor(vBackColor);
    key_update:
      vUpdate := True;
    key_hidexy:
      vHideXY := True;
  end;

  // Set initial colors
  vTextColor := vColor[0];        // First pair foreground
  vTextBackColor := vColor[1];    // First pair background

  // Set form metrics
  SetTextMetrics;
  vWidth := vCols * ChrWidth;     // Pixel width
  vHeight := vRows * ChrHeight;   // Pixel height
  i := ChrWidth div 2;
  SetSize(i, i, i, i);            // Margins = half character width
end;
```

### 4.2 Configuration Parameters

| Parameter | Key | Type | Range | Default | Description |
|-----------|-----|------|-------|---------|-------------|
| **title** | key_title | string | - | `"<name> - TERM"` | Window title text |
| **pos** | key_pos | left, top | - | host origin ≈(0,210), no cascade | Window position (offset only; `KeyPos:2712-2716` reads 2 values — no width/height) |
| **size** | key_size | columns, rows | 1-256 | 40×20 | Terminal grid size |
| **textsize** | key_textsize | integer | 6-200 | `FontSize` (default 10) | Font size in points (`KeyTextSize` clamp) |
| **color** | key_color | 8 integers | RGB24 | DefaultTermColors | 8 color values (4 pairs) |
| **backcolor** | key_backcolor | integer | RGB24 | clBlack | Window background color |
| **update** | key_update | boolean | - | false | Enable buffered update mode |
| **hidexy** | key_hidexy | boolean | - | false | Hide coordinate display |

### 4.3 Size Calculation

**DebugDisplayUnit.pas:2216-2220**
```pascal
SetTextMetrics;                  // Calculate ChrWidth, ChrHeight
vWidth := vCols * ChrWidth;      // Total pixel width
vHeight := vRows * ChrHeight;    // Total pixel height
i := ChrWidth div 2;
SetSize(i, i, i, i);             // Set margins
```

**Example** (40×20 terminal, font size 12):
- ChrWidth ≈ 7 pixels (depends on font)
- ChrHeight ≈ 16 pixels
- vWidth = 40 × 7 = 280 pixels
- vHeight = 20 × 16 = 320 pixels
- Margin = 7 / 2 = 3 pixels

**Total Window**: 286×326 pixels (including margins)

---

## 5. Update Processing

### 5.1 TERM_Update Method

**DebugDisplayUnit.pas:2223-2315**
```pascal
procedure TDebugDisplayForm.TERM_Update;
var
  i, j: integer;
begin
  vUpdateFlag := False;
  while not NextEnd do
  begin
    if NextKey then
    case val of
      key_black..key_gray:      // set text color and maybe text background color
      begin
        Dec(ptr);
        KeyColor(vTextColor);
        KeyColor(vTextBackColor);
      end;
      key_backcolor:            // set text background color
        KeyColor(vTextBackColor);
      key_clear:                // clear screen and home
      begin
        ClearBitmap;
        vUpdateFlag := True;
        vCol := 0;
        vRow := 0;
      end;
      key_update:               // update bitmap
        BitmapToCanvas(0);
      key_save:                 // save bitmap
        KeySave;
      key_pc_key:               // get key
        SendKeyPress;
      key_pc_mouse:             // get mouse
        SendMousePos;
    end
    else
    begin
      if NextNum then
      case val of
        0:                      // clear screen and home
        begin
          ClearBitmap;
          vUpdateFlag := True;
          vCol := 0;
          vRow := 0;
        end;
        1:                      // home
        begin
          vCol := 0;
          vRow := 0;
        end;
        2:                      // set column
          KeyValWithin(vCol, 0, vCols - 1);
        3:                      // set row
          KeyValWithin(vRow, 0, vRows - 1);
        4..7:                   // set colors (select pair 0-3)
        begin
          vTextColor := vColor[(val - 4) * 2 + 0];
          vTextBackColor := vColor[(val - 4) * 2 + 1];
        end;
        8:                      // backspace
          if (vCol <> 0) or (vRow <> 0) then
          begin
            Dec(vCol);
            if vCol < 0 then
            begin
              vCol := vCols - 1;
              Dec(vRow);
            end;
          end;
        9:                      // tab
        begin
          TERM_Chr(' ');
          while vCol and 7 <> 0 do TERM_Chr(' ');
        end;
        10:                     // new line (10)
          TERM_Chr(Chr(13));
        13:                     // new line (13), ignore trailing linefeed (10)
        begin
          TERM_Chr(Chr(13));
          if NextNum then if val <> 10 then Dec(ptr)
        end;
        32..255:                // printable chr
          TERM_Chr(Chr(val));
      end
      else
      if NextStr then
      begin                     // string
        j := Length(PChar(val));
        if j <> 0 then for i := 0 to j - 1 do TERM_Chr(PChar(val)[i]);
      end;
    end;
  end;
  if not vUpdate and vUpdateFlag then BitmapToCanvas(0);
end;
```

### 5.2 Command Processing

**Numeric Commands**:

| Value | Command | Action |
|-------|---------|--------|
| **0** | Clear + Home | Clear screen, move cursor to (0, 0) |
| **1** | Home | Move cursor to (0, 0) |
| **2** | Set Column | Next value = column (0-based) |
| **3** | Set Row | Next value = row (0-based) |
| **4** | Color Pair 0 | Set to pair 0 colors (ORANGE on BLACK) |
| **5** | Color Pair 1 | Set to pair 1 colors (BLACK on ORANGE — inverse video) |
| **6** | Color Pair 2 | Set to pair 2 colors (GREEN on BLACK) |
| **7** | Color Pair 3 | Set to pair 3 colors (BLACK on GREEN — inverse video) |
| **8** | Backspace | Move cursor back one position |
| **9** | Tab | Space to next 8-column boundary |
| **10** | Line Feed | New line (same as CR) |
| **13** | Carriage Return | New line, ignore following LF |
| **32-255** | Printable | Display ASCII character |

**Key Commands**:

| Key | Action |
|-----|--------|
| **key_black..key_gray** | Set text foreground color; optionally set text background color from next element (lines 2232-2237). Brightness nibble applies to `ORANGE..GRAY` only — **`BLACK`/`WHITE` take none** (`KeyColor:2764-2768`) |
| **key_backcolor** | Set text background color only (line 2238-2239) |
| **key_clear** | Clear screen and home cursor |
| **key_update** | Force display update (buffered mode) |
| **key_save** | Save to `.bmp` — six forms, incl. `SAVE WINDOW` (`KeySave`, 2839-2866); see the Directive Reference |
| **key_pc_key** | Send keyboard input to host |
| **key_pc_mouse** | Send mouse position to host |

**String Command**:
- **ele_str**: Display entire string at current cursor position

---

## 6. Character Rendering

### 6.1 TERM_Chr Method

**DebugDisplayUnit.pas:2317-2354**
```pascal
procedure TDebugDisplayForm.TERM_Chr(c: Char);
var
  x, y: integer;
  r, r2: TRect;
begin
  if c = Chr(13) then              // Carriage return (newline)
  begin
    if vRow <> vRows - 1 then
      Inc(vRow)                    // Move to next row
    else
    begin
      // Scroll up one line
      r := Rect(vMarginLeft, vMarginTop,
                vMarginLeft + vCols * ChrWidth,
                vMarginTop + (vRows - 1) * ChrHeight);
      r2 := Rect(r.Left, r.Top + ChrHeight, r.Right, r.Bottom + ChrHeight);
      Bitmap[0].Canvas.CopyRect(r, Bitmap[0].Canvas, r2);

      // Clear bottom line
      Bitmap[0].Canvas.Brush.Color := WinRGB(vBackColor);
      r := Rect(r.Left, r.Bottom, r.Right, r2.Bottom);
      Bitmap[0].Canvas.FillRect(r);
      vUpdateFlag := True;
    end;
    vCol := 0;                     // Return to column 0
  end
  else
  begin
    // Auto-wrap to next line if at right edge
    if vCol = vCols then TERM_Chr(Chr(13));

    // Calculate pixel position
    x := vMarginLeft + vCol * ChrWidth;
    y := vMarginTop + vRow * ChrHeight;
    r := Rect(x, y, x + ChrWidth, y + ChrHeight);

    // Render character
    Bitmap[0].Canvas.Font.Color := WinRGB(vTextColor);
    Bitmap[0].Canvas.Brush.Color := WinRGB(vTextBackColor);
    Bitmap[0].Canvas.TextRect(r, x, y, c);
    Inc(vCol);

    // Real-time update (if not in buffered mode)
    if not vUpdate then
    begin
      Bitmap[1].Canvas.CopyRect(r, Bitmap[0].Canvas, r);
      Canvas.CopyRect(r, Bitmap[0].Canvas, r);
    end;
  end;
end;
```

### 6.2 Character Rendering Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Check character type                                     │
│    If CR (13): goto newline handling                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Check for line wrap                                      │
│    If vCol = vCols: call TERM_Chr(Chr(13))                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Calculate pixel position                                 │
│    x = vMarginLeft + vCol × ChrWidth                        │
│    y = vMarginTop + vRow × ChrHeight                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Set text colors                                          │
│    Font.Color = vTextColor                                  │
│    Brush.Color = vTextBackColor                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Render character to Bitmap[0]                            │
│    TextRect(r, x, y, c)                                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Advance cursor                                           │
│    Inc(vCol)                                                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. Real-time update (if not buffered)                       │
│    If not vUpdate:                                          │
│      Copy character rect to Bitmap[1] and Canvas            │
└─────────────────────────────────────────────────────────────┘
```

### 6.3 Newline Handling

**Normal Case** (not at bottom row):
```pascal
Inc(vRow);     // Move to next row
vCol := 0;     // Return to column 0
```

**Bottom Row Case** (scroll required):
```pascal
// Copy all rows up one line (row 1→0, 2→1, ..., 18→17)
CopyRect(destination, source);

// Clear bottom row
FillRect(bottom_row);

vRow stays at bottom;
vCol := 0;
```

---

## 7. Cursor Management

### 7.1 Cursor Position

**Current Position**:
```pascal
vCol: integer;  // Column (0-based)
vRow: integer;  // Row (0-based)
```

**Valid Ranges**:
```
vCol ∈ [0, vCols]        // vCols == "pending wrap" — see §7.3
vRow ∈ [0, vRows - 1]
```

`vCol` legitimately **rests at `vCols`** (one past the last column) after a glyph is
written into the last column: `TERM_Chr:2347` does an unconditional `Inc(vCol)` with
no wrap test after it. The wrap is deferred to the *next* character (`TERM_Chr:2340`).
The explicit set-column directive is still clamped to `0..vCols-1`
(`KeyValWithin(vCol, 0, vCols - 1)`, 2273).

### 7.2 Position Commands

**Home Cursor** (command 1):
```pascal
vCol := 0;
vRow := 0;
```

**Set Column** (command 2 + value):
```pascal
// Example: send 2, then column number
KeyValWithin(vCol, 0, vCols - 1);
```

**Set Row** (command 3 + value):
```pascal
// Example: send 3, then row number
KeyValWithin(vRow, 0, vRows - 1);
```

### 7.3 Cursor Movement

**Forward Movement** (printing character) — the wrap is **LAZY, not eager**:
```pascal
// TERM_Chr, else-branch (2338-2352):
if vCol = vCols then TERM_Chr(Chr(13));   // 2340 — deferred wrap, tested ON ENTRY
… draw the glyph at (vCol, vRow) …        // 2341-2346
Inc(vCol);                                // 2347 — UNCONDITIONAL, no wrap test after
```

`TERM_Chr` tests the wrap **on entry of the next character** (2340), not after
advancing. So printing into the last column leaves `vCol = vCols` — a *pending-wrap*
state — and the CR that opens the new row is performed only when another **printable**
character actually arrives.

> **Behavioral consequence (this is a real difference, not a formality).** An explicit
> `CR` (13) sent immediately after a last-column glyph produces **one** newline. Under
> an eager-wrap model (`Inc(vCol); if vCol = vCols then wrap`) the row would already
> have advanced, and the explicit CR would advance it *again* — emitting an **extra
> blank row**. v55 does not do that.

**Backward Movement** (backspace, command 8):
```pascal
Dec(vCol);
if vCol < 0 then
begin
  vCol := vCols - 1;
  Dec(vRow);
end;
```

**Tab Movement** (command 9):
```pascal
TERM_Chr(' ');                    // Print space
while vCol and 7 <> 0 do          // Until 8-column boundary
  TERM_Chr(' ');
```

**Tab Positions**: 0, 8, 16, 24, 32, 40, ... (every 8 columns)

---

## 8. Scrolling System

### 8.1 Scroll Trigger

**Condition**: Newline (CR) when cursor is at bottom row (vRow = vRows - 1).

**DebugDisplayUnit.pas:2324-2335**
```pascal
if vRow <> vRows - 1 then
  Inc(vRow)              // Normal case: move to next row
else
begin
  // Scroll up one line
  r := Rect(vMarginLeft, vMarginTop,
            vMarginLeft + vCols * ChrWidth,
            vMarginTop + (vRows - 1) * ChrHeight);
  r2 := Rect(r.Left, r.Top + ChrHeight, r.Right, r.Bottom + ChrHeight);
  Bitmap[0].Canvas.CopyRect(r, Bitmap[0].Canvas, r2);

  // Clear bottom line
  Bitmap[0].Canvas.Brush.Color := WinRGB(vBackColor);
  r := Rect(r.Left, r.Bottom, r.Right, r2.Bottom);
  Bitmap[0].Canvas.FillRect(r);
  vUpdateFlag := True;
end;
```

### 8.2 Scroll Operation

**Step 1: Copy Bitmap** (shift all rows up one line)
```
Source Rectangle:
  Left:   vMarginLeft
  Top:    vMarginTop + ChrHeight     (skip first row)
  Right:  vMarginLeft + vCols × ChrWidth
  Bottom: vMarginTop + vRows × ChrHeight

Destination Rectangle:
  Left:   vMarginLeft
  Top:    vMarginTop                  (overwrite from first row)
  Right:  vMarginLeft + vCols × ChrWidth
  Bottom: vMarginTop + (vRows - 1) × ChrHeight
```

**Effect**: Row 1 → Row 0, Row 2 → Row 1, ..., Row 19 → Row 18

**Step 2: Clear Bottom Line**
```
Rectangle:
  Left:   vMarginLeft
  Top:    vMarginTop + (vRows - 1) × ChrHeight
  Right:  vMarginLeft + vCols × ChrWidth
  Bottom: vMarginTop + vRows × ChrHeight

Fill with: vBackColor
```

**Step 3: Set Update Flag**
```pascal
vUpdateFlag := True;
```

### 8.3 Scroll Performance

**Bitmap Copy**: Hardware-accelerated by Windows GDI (CopyRect).

**Example** (40×20 terminal, 7×16 character):
- Bitmap size: 280×320 pixels
- Scroll area: 280×304 pixels (19 rows)
- Bytes moved: 280 × 304 × 3 = 255,360 bytes (RGB24)

**Performance**: Typically < 1 ms on modern hardware.

---

## 9. Control Commands

### 9.1 Clear Screen

**Command**: 0 or key_clear

**DebugDisplayUnit.pas:2240-2246, 2260-2266**
```pascal
ClearBitmap;
vUpdateFlag := True;
vCol := 0;
vRow := 0;
```

**Actions**:
1. Fill entire bitmap with background color
2. Set update flag
3. Home cursor to (0, 0)

### 9.2 Home Cursor

**Command**: 1

**DebugDisplayUnit.pas:2267-2271**
```pascal
vCol := 0;
vRow := 0;
```

**Action**: Move cursor to top-left without clearing screen.

### 9.3 Color Selection

**Commands**: 4, 5, 6, 7 (select color pairs 0-3)

**DebugDisplayUnit.pas:2276-2280**
```pascal
vTextColor := vColor[(val - 4) * 2 + 0];
vTextBackColor := vColor[(val - 4) * 2 + 1];
```

**Mapping**:
- **Command 4**: Pair 0 → vColor[0], vColor[1]
- **Command 5**: Pair 1 → vColor[2], vColor[3]
- **Command 6**: Pair 2 → vColor[4], vColor[5]
- **Command 7**: Pair 3 → vColor[6], vColor[7]

### 9.4 Backspace

**Command**: 8

**DebugDisplayUnit.pas:2281-2290**
```pascal
if (vCol <> 0) or (vRow <> 0) then
begin
  Dec(vCol);
  if vCol < 0 then
  begin
    vCol := vCols - 1;
    Dec(vRow);
  end;
end;
```

**Behavior**:
- Moves cursor back one position
- Wraps to previous line if at column 0
- Does nothing if at home position (0, 0)
- **Does not erase character** (just moves cursor)

### 9.5 Tab

**Command**: 9

**DebugDisplayUnit.pas:2291-2295**
```pascal
TERM_Chr(' ');
while vCol and 7 <> 0 do TERM_Chr(' ');
```

**Behavior**:
- Prints spaces until reaching next 8-column boundary
- Tab stops at: 8, 16, 24, 32, 40, ...
- Minimum advance: 1 space
- Maximum advance: 8 spaces

**Example**:
```
Column 0: Tab → advance to 8 (8 spaces)
Column 5: Tab → advance to 8 (3 spaces)
Column 8: Tab → advance to 16 (8 spaces)
Column 14: Tab → advance to 16 (2 spaces)
```

### 9.6 Newline

**Commands**: 10 (LF), 13 (CR)

**DebugDisplayUnit.pas:2296-2302**
```pascal
10:                     // new line (10)
  TERM_Chr(Chr(13));

13:                     // new line (13), ignore trailing linefeed (10)
begin
  TERM_Chr(Chr(13));
  if NextNum then if val <> 10 then Dec(ptr)
end;
```

**Behavior**:
- **LF (10)**: Converted to CR
- **CR (13)**: Process newline, consume following LF if present
- **CRLF (13, 10)**: Processed as single newline

---

## 10. Color System

### 10.1 Color Storage

**DebugDisplayUnit.pas:311**
```pascal
var
  vColor: array [0..Channels - 1] of integer;  // Channels = 8
```

**Color Format**: RGB24 (24-bit RGB, $RRGGBB)

### 10.2 Color Pairs

**Pair Structure**:
```
Pair 0: vColor[0] (foreground), vColor[1] (background)
Pair 1: vColor[2] (foreground), vColor[3] (background)
Pair 2: vColor[4] (foreground), vColor[5] (background)
Pair 3: vColor[6] (foreground), vColor[7] (background)
```

**Default Colors** (DebugDisplayUnit.pas:242) — **four inverse-video pairs**:
```pascal
DefaultTermColors: array[0..7] of integer =
  (clOrange, clBlack,    // Pair 0: ORANGE ($FF7F00) on BLACK ($000000)
   clBlack, clOrange,    // Pair 1: BLACK on ORANGE          (inverse of pair 0)
   clLime, clBlack,      // Pair 2: GREEN ($00FF00) on BLACK
   clBlack, clLime);     // Pair 3: BLACK on GREEN           (inverse of pair 2)
```
The `clXxx` constants are literal RGB24 values (`DebugDisplayUnit.pas` 179–191):
`clOrange = $FF7F00` (note: **NOT** web `$FF8000`/`$FFA500`), `clLime = $00FF00`,
`clBlack = $000000`. `WinRGB` swaps R↔B to BGR only at GDI draw time.

**Naming**: `clLime` is a **Delphi palette constant**, not a DEBUG color keyword — the
DEBUG keyword for that hue is **`GREEN`** (`key_green = 4`, line 36); no `LIME` keyword
exists. See §2.3 for the two-color-systems note.

### 10.3 Color Selection

**At Configuration** (key_color):
```pascal
for i := 0 to 7 do if not KeyColor(vColor[i]) then Break;
```

Reads up to 8 color values sequentially.

**At Runtime** (commands 4-7):
```pascal
case val of
  4:  // Pair 0
    vTextColor := vColor[0];
    vTextBackColor := vColor[1];
  5:  // Pair 1
    vTextColor := vColor[2];
    vTextBackColor := vColor[3];
  6:  // Pair 2
    vTextColor := vColor[4];
    vTextBackColor := vColor[5];
  7:  // Pair 3
    vTextColor := vColor[6];
    vTextBackColor := vColor[7];
end;
```

### 10.4 Color Usage

**Character Rendering** (TERM_Chr):
```pascal
Bitmap[0].Canvas.Font.Color := WinRGB(vTextColor);      // Text color
Bitmap[0].Canvas.Brush.Color := WinRGB(vTextBackColor); // Background
```

**Clear Operations**:
```pascal
Bitmap[0].Canvas.Brush.Color := WinRGB(vBackColor);     // Window background
```

---

## 11. Text Metrics

### 11.1 SetTextMetrics Method

**DebugDisplayUnit.pas:2919-2925**
```pascal
procedure TDebugDisplayForm.SetTextMetrics;
begin
  Bitmap[0].Canvas.Font.Size := vTextSize;
  ChrWidth := Bitmap[0].Canvas.TextWidth('X');
  ChrHeight := Bitmap[0].Canvas.TextHeight('X');
end;
```

**Purpose**: Calculate character cell dimensions based on font size.

**Process**:
1. Set font size to vTextSize (points)
2. Measure width of 'X' character → ChrWidth
3. Measure height of 'X' character → ChrHeight

### 11.2 Character Metrics

**Variables**:
```pascal
ChrWidth: integer;   // Pixels per character (horizontal)
ChrHeight: integer;  // Pixels per character (vertical)
```

**Font**: `SetTextMetrics` (2919-2925) sets only the **size**
(`Bitmap[0].Canvas.Font.Size := vTextSize`). The **face** is assigned once, earlier, in
`FormCreate:600` — `Bitmap[0].Canvas.Font.Name := FontName` — i.e. the **global font-name
preference** (the same one applied to `CursorColor.Canvas.Font.Name` at 608). So the cell
size is the measured width/height of the glyph `'X'` **in `FontName` at `vTextSize` points**
(`2921-2924`), not in an arbitrary VCL default face. `'X'` is a representative wide glyph, so
proportional fonts are accommodated by sizing every cell to that width.

> **TS-parity note:** cell width/height must be measured with the **configured font face**,
> not the browser/host default — otherwise the whole grid geometry drifts.

**Example Measurements** (approximate):

| Font Size | ChrWidth | ChrHeight |
|-----------|----------|-----------|
| 8 pt | 5 | 11 |
| 10 pt | 6 | 13 |
| 12 pt | 7 | 16 |
| 14 pt | 8 | 18 |
| 16 pt | 9 | 21 |
| 20 pt | 11 | 26 |

**Note**: Actual values depend on Windows font settings and DPI.

### 11.3 Display Dimensions

**Pixel Calculations**:
```pascal
vWidth := vCols * ChrWidth;      // Total text area width
vHeight := vRows * ChrHeight;    // Total text area height
```

**Window Size**:
```pascal
ClientWidth := vMarginLeft + vWidth + vMarginRight;
ClientHeight := vMarginTop + vHeight + vMarginBottom;
```

**Example** (40×20, font size 12):
- ChrWidth = 7, ChrHeight = 16
- vWidth = 40 × 7 = 280 pixels
- vHeight = 20 × 16 = 320 pixels
- Margin = 7 / 2 = 3 pixels
- ClientWidth = 3 + 280 + 3 = 286 pixels
- ClientHeight = 3 + 320 + 3 = 326 pixels

---

## 12. Command Protocol

### 12.1 Configuration Command

**Format** (element array). Slot `[0]` is the **display-type** element `ele_dis` — *not*
`ele_key` — and slot `[1]` is the window-**name** element `ele_nam`; `FormCreate` reads
`DisplayType := P2.DebugDisplayValue[0]` and the name from `[1]`, then begins the directive
scan at `ptr := 2` (`FormCreate:625-632`). There is exactly **one** `ele_end`, at the very end
— `NextEnd` (4124-4127) tests `DebugDisplayType[ptr] = ele_end`, so a mid-array `ele_end`
would **terminate the whole directive scan**.

```
ele_dis, dis_term,
ele_nam, <name ptr>,
ele_key, key_title,    ele_str, 'Terminal',
ele_key, key_pos,      ele_num, left, ele_num, top,      // KeyPos reads exactly 2 numbers
ele_key, key_size,     ele_num, cols, ele_num, rows,
ele_key, key_textsize, ele_num, font_size,
ele_key, key_color,
  ele_num, fg0, ele_num, bg0,
  ele_num, fg1, ele_num, bg1,
  ele_num, fg2, ele_num, bg2,
  ele_num, fg3, ele_num, bg3,
ele_key, key_update,
ele_end
```

`KeyPos` (2712-2716) reads **exactly two** numbers — `if NextNum then Left := val +
P2.DebugDisplayLeft else Exit; if NextNum then Top := val + P2.DebugDisplayTop;` — there is
**no width/height**. (Window size comes from `SIZE cols rows` × the measured cell.)

### 12.2 Update Commands

**Numeric Values**:
```
ele_num, 0,           // Clear screen and home
ele_num, 1,           // Home cursor
ele_num, 2, ele_num, col,  // Set column
ele_num, 3, ele_num, row,  // Set row
ele_num, 4,           // Color pair 0
ele_num, 5,           // Color pair 1
ele_num, 6,           // Color pair 2
ele_num, 7,           // Color pair 3
ele_num, 8,           // Backspace
ele_num, 9,           // Tab
ele_num, 10,          // Line feed
ele_num, 13,          // Carriage return
ele_num, 32,          // Space
ele_num, 65,          // 'A'
..., ele_end
```

**String Output**:
```
ele_str, "Hello, World!", ele_end
```

**Force Update** (buffered mode):
```
ele_key, key_update, ele_end
```

---

## 13. Usage Examples

> **Two rules govern every example below — get either wrong and nothing appears.**
>
> 1. **Instantiate, then feed by INSTANCE NAME.** The *first* `debug()` names the display
>    **type** followed by the **instance name** you are creating (`` `TERM MyTerm … ``); every
>    subsequent message addresses the **instance**, never the type (`` `MyTerm … ``). Feeding
>    the display *type* — `` debug(`TERM 'Hello') `` — does not reach a window.
>    (`FormCreate:625-626` reads `[0]` = display type, `[1]` = the window's name; the name is
>    what the parser resolves on later messages.)
> 2. **Strings are SINGLE-quoted.** `'Hello'` — not `"Hello"`. Double quotes are **silently
>    ignored** by the debug-string parser.

### 13.1 Basic Text Output

**Goal**: Display simple text messages.

**Propeller 2 Code**:
```spin2
debug(`TERM MyTerm SIZE 40 20)    ' create the instance "MyTerm"

debug(`MyTerm 'Hello, World!')
debug(`MyTerm 13)                 ' newline
debug(`MyTerm 'Line 2')
```

**Output**:
```
Hello, World!
Line 2
_
```

### 13.2 Cursor Positioning

**Goal**: Position text at specific row/column.

**Propeller 2 Code**:
```spin2
debug(`TERM MyTerm SIZE 40 20)

debug(`MyTerm 1)                  ' control code 1 — home cursor
debug(`MyTerm 3 5)                ' control code 3 + parameter — set row to 5
debug(`MyTerm 2 10)               ' control code 2 + parameter — set column to 10
debug(`MyTerm 'Positioned text')
```

(Use `` `(expr) `` to supply the parameter from a variable: `` debug(`MyTerm 3 `(row)) ``.)

**Output**:
```
(row 0)
(row 1)
...
(row 5)          Positioned text
```

### 13.3 Color Text

**Goal**: Use different colors for status messages.

**Propeller 2 Code**:
```spin2
' 8 values = 4 text/background pairs. COLOR is CONFIG-ONLY for TERM (2203-2204).
debug(`TERM MyTerm SIZE 40 20 COLOR $FF7F00 $000000 $000000 $FF7F00 $00FF00 $000000 $FF0000 $000000)
' pair0 Orange/Black · pair1 Black/Orange · pair2 Green/Black · pair3 Red/Black
' (Orange here = clOrange $FF7F00)

debug(`MyTerm 4 'Normal message' 13)   ' control code 4 → pair 0 (orange)
debug(`MyTerm 6 'Success!' 13)         ' control code 6 → pair 2 (green)
debug(`MyTerm 7 'Error!' 13)           ' control code 7 → pair 3 (red)
```

**Output** (in color):
```
Normal message  (orange text)
Success!        (green text)
Error!          (red text)
```

An **arbitrary** foreground/background can also be set at runtime with the named-color
directives, which TERM *does* accept in the update phase (2232-2239) — e.g.
`` debug(`MyTerm YELLOW 12 'Warning' 13) `` (yellow at brightness 12), or
`` debug(`MyTerm BACKCOLOR $202020) ``. Only the **`COLOR`** keyword itself is config-only.

### 13.4 Formatted Data Table

**Goal**: Display aligned data columns.

**Propeller 2 Code**:
```spin2
debug(`TERM MyTerm SIZE 40 20)

debug(`MyTerm 0)                  ' control code 0 — clear screen + home
debug(`MyTerm 'Sensor' 9 'Value' 9 'Status' 13)
debug(`MyTerm 'Temp' 9 `UDEC_(temp) 9 'OK' 13)
debug(`MyTerm 'Press' 9 `UDEC_(press) 9 'OK' 13)
```

**Output**:
```
Sensor  Value   Status
Temp    25      OK
Press   1013    OK
```

### 13.5 Scrolling Log

**Goal**: Continuous logging with auto-scroll.

**Propeller 2 Code**:
```spin2
debug(`TERM MyTerm SIZE 80 25)

repeat
  debug(`MyTerm `UDEC_(getms()) ' Event occurred' 13)
  waitms(100)
```

**Output** (scrolls continuously):
```
...
1234 Event occurred
1334 Event occurred
1434 Event occurred
1534 Event occurred
_
```

### 13.6 Buffered Update Mode

**Goal**: Reduce flicker during complex updates.

**Propeller 2 Code**:
```spin2
debug(`TERM MyTerm SIZE 40 20 UPDATE)   ' UPDATE at config = buffered mode

' Clear and redraw entire screen
debug(`MyTerm 0)                        ' clear
debug(`MyTerm 'Header')
debug(`MyTerm 13)
' ... more text ...
debug(`MyTerm UPDATE)                   ' force the single flush (BitmapToCanvas(0), 2247-2248)
```

**Behavior**: All text buffered in `Bitmap[0]`, then displayed once by the `UPDATE`
directive. ⚠️ A `SAVE 'name'` issued *before* that `UPDATE` writes `Bitmap[1]` — i.e. the
**stale previous frame** (`KeySave:2843`).

---

## 14. Performance Characteristics

### 14.1 Character Rendering Speed

**Single Character**:
- Font rendering: ~0.01-0.05 ms (GDI TextRect)
- Bitmap copy (real-time mode): ~0.005 ms
- **Total**: ~0.02-0.06 ms per character

**String Rendering** (N characters):
- Sequential TERM_Chr calls: N × 0.02-0.06 ms
- **100-character string**: ~2-6 ms

**Example** (40×20 terminal, full screen):
- Total characters: 800
- Render time: ~16-48 ms
- **Frame rate**: 20-60 Hz

### 14.2 Scrolling Performance

**Bitmap Copy** (CopyRect):
- 40×20 terminal, 7×16 chars
- Bitmap size: 280×320 pixels
- Scroll area: 280×304 pixels (19 rows)
- **Copy time**: ~0.5-1.0 ms (hardware-accelerated)

**Clear Bottom Line**:
- 280×16 pixels
- **Clear time**: ~0.1 ms

**Total Scroll**: ~0.6-1.1 ms

### 14.3 Update Modes

**Real-Time Mode** (vUpdate = False, default):
- Each character immediately copied to display
- **Latency**: 0.02-0.06 ms
- **Use**: Interactive console, live logging

**Buffered Mode** (vUpdate = True):
- All changes buffered in Bitmap[0]
- Single BitmapToCanvas(0) call on UPDATE command
- **Latency**: Variable (until UPDATE)
- **Use**: Complex redraws, flicker reduction

### 14.4 Memory Usage

**Bitmap Buffers**:
- Bitmap[0]: Render target
- Bitmap[1]: Display buffer
- Size: (vWidth + margins) × (vHeight + margins) × 3 bytes

**Example** (40×20, 286×326 pixels):
- Bitmap[0]: 286 × 326 × 3 = 279,852 bytes (~273 KB)
- Bitmap[1]: 286 × 326 × 3 = 279,852 bytes (~273 KB)
- **Total**: ~546 KB

**Color Array**:
- 8 integers × 4 bytes = 32 bytes

**Total Memory**: ~546 KB

---

## 15. Terminal Emulation

### 15.1 Terminal Type

**Emulation**: Basic text terminal (similar to TTY, not full VT100/ANSI)

**Supported Features**:
- Character output
- Cursor positioning (row/column) — control codes 1, 2, 3
- Scrolling
- Color selection — 4 selectable pairs (codes 4-7) **plus** arbitrary fg/bg via the
  named-color directives `BLACK..GRAY {brightness}` / `BACKCOLOR` (2232-2239)
- Tab expansion
- Newline handling
- **Mouse position readback** — the P2 polls it with `PC_MOUSE` (`SendMousePos`, 3537-3577),
  which returns the character **column, row** (TERM's char-cell transform, 3563-3567)

**Not Supported**:
- ANSI escape sequences
- Cursor movement sequences (e.g., ESC[A for up)
- Attributes (bold, underline, blink)
- Alternate screen buffer
- **ANSI/xterm mouse-*reporting* escape sequences** — note this is *not* the same as "no
  mouse": the mouse **position is available**, just not via terminal escape codes. It is
  polled with `PC_MOUSE` (see the Keyboard & mouse table in the Directive Reference).
- Line drawing characters

### 15.2 Control Code Handling

Codes **0-7 are the core acting codes** — they are the entire cursor/screen/color
command set. They are *not* "unsupported": every one of them has an explicit arm in
the `case val of` at `TERM_Update:2259-2305`.

**Supported control codes** (all handled in `TERM_Update`):

| Code | ASCII | Name | Action | Pascal |
|------|-------|------|--------|--------|
| 0 | NUL | Clear + Home | `ClearBitmap`; `vUpdateFlag := True`; `vCol := 0`; `vRow := 0` | 2260-2266 |
| 1 | SOH | Home | `vCol := 0`; `vRow := 0` (no clear) | 2267-2271 |
| 2 *n* | STX | Set column | `KeyValWithin(vCol, 0, vCols - 1)` — consumes the **next numeric element** | 2272-2273 |
| 3 *n* | ETX | Set row | `KeyValWithin(vRow, 0, vRows - 1)` — consumes the **next numeric element** | 2274-2275 |
| 4 | EOT | Select color pair 0 | `vTextColor := vColor[0]`; `vTextBackColor := vColor[1]` | 2276-2280 |
| 5 | ENQ | Select color pair 1 | `vColor[2]` / `vColor[3]` | 2276-2280 |
| 6 | ACK | Select color pair 2 | `vColor[4]` / `vColor[5]` | 2276-2280 |
| 7 | BEL | Select color pair 3 | `vColor[6]` / `vColor[7]` | 2276-2280 |
| 8 | BS | Backspace | Move cursor back (cursor only — no erase) | 2281-2290 |
| 9 | HT | Horizontal Tab | Space to next 8-column boundary | 2291-2295 |
| 10 | LF | Line Feed | New line (`TERM_Chr(Chr(13))`) | 2296-2297 |
| 13 | CR | Carriage Return | New line; swallows a following `10` | 2298-2302 |
| 32-255 | — | Printable | Render glyph via `TERM_Chr` | 2303-2304 |

**Unhandled numeric values**: **11, 12 and 14-31**. The `case` at `TERM_Update:2259-2305`
has **no arm** for them, so they fall through with **no action** — they are silently
ignored, and they are **never "treated as printable"** (only `32..255` reaches
`TERM_Chr`). Note that 11 and 12 *are* legal *input* values — `FormKeyDown` (846-847)
sends them for PageUp/PageDown — they are simply no-ops on *output*.

### 15.3 Newline Behavior

**Standard Terminal** (CRLF):
```
CR (13): Move to column 0
LF (10): Move to next row
CRLF (13, 10): Both actions
```

**TERM Display**:
```
CR (13): Column 0 + next row (combined)
LF (10): Converted to CR
CRLF (13, 10): Processed as single newline
```

**Implication**: LF and CR are equivalent; CRLF is same as single LF or CR.

### 15.4 Comparison with Standard Terminals

| Feature | TERM Display | VT100 | Basic TTY |
|---------|--------------|-------|-----------|
| **Character output** | ✓ | ✓ | ✓ |
| **Scrolling** | ✓ | ✓ | ✓ |
| **Cursor positioning** | ✓ (commands) | ✓ (ESC sequences) | ✗ |
| **Colors** | ✓ (4 selectable pairs *plus* arbitrary fg/bg via `BLACK..GRAY {brightness}` / `BACKCOLOR`) | ✓ (8/16 colors) | ✗ |
| **ANSI escapes** | ✗ | ✓ | ✗ |
| **Attributes** | ✗ | ✓ | ✗ |
| **Tab stops** | ✓ (fixed 8) | ✓ (programmable) | ✓ |
| **Backspace** | ✓ (cursor only) | ✓ (destructive) | ✓ |

---

## 16. Implementation Details

### 16.1 Bitmap System

**Double-Buffering**:
- **Bitmap[0]**: Render target (always up-to-date)
- **Bitmap[1]**: Display buffer (shown on screen)

**Real-Time Mode**:
```pascal
// After each character:
Bitmap[1].Canvas.CopyRect(r, Bitmap[0].Canvas, r);  // Update display buffer
Canvas.CopyRect(r, Bitmap[0].Canvas, r);            // Update screen
```

**Buffered Mode**:
```pascal
// On UPDATE command:
BitmapToCanvas(0);  // Copy entire Bitmap[0] → Bitmap[1] → Canvas
```

### 16.2 Font Rendering

**Windows GDI TextRect**:
```pascal
Canvas.TextRect(r, x, y, c);
```

**Parameters**:
- **r**: Clipping rectangle (character cell bounds)
- **x, y**: Text baseline position
- **c**: Character to render

**Background**: Filled automatically using Brush.Color.

**Font Metrics**: Character cells are sized to the measured width/height of `'X'`
at the configured point size (`SetTextMetrics`, 2919-2925) — not to the widest
glyph in the font. Glyphs wider than `'X'` may be clipped by the `TextRect`
clipping rectangle.

### 16.3 Coordinate System

**Logical Coordinates** (row/column):
```
vRow ∈ [0, vRows - 1]
vCol ∈ [0, vCols]        // vCols = pending-wrap state (lazy wrap, §7.3)
```

**Pixel Coordinates**:
```pascal
x := vMarginLeft + vCol * ChrWidth;
y := vMarginTop + vRow * ChrHeight;
```

**Origin**: Top-left corner of terminal grid.

### 16.4 String Processing

**DebugDisplayUnit.pas:2307-2311**
```pascal
if NextStr then
begin
  j := Length(PChar(val));
  if j <> 0 then for i := 0 to j - 1 do TERM_Chr(PChar(val)[i]);
end;
```

**Process**:
1. Get string length
2. Iterate through each character
3. Call TERM_Chr for each character

**Efficiency**: Sequential character rendering (no optimization for string batching).

### 16.5 Margin Calculation

**DebugDisplayUnit.pas:2219-2220**
```pascal
i := ChrWidth div 2;
SetSize(i, i, i, i);  // All margins = ChrWidth / 2
```

**Purpose**: Provide visual spacing around terminal grid.

**Margin**: Half-character width on all sides.

**Example** (ChrWidth = 7):
- Margin = 3 pixels
- Total window = 3 + (40×7) + 3 = 286 pixels wide

---

## 17. Element Array Protocol Specification

### 17.1 Protocol Overview

TERM uses element arrays for configuration and character data transmission.

**Element Storage**:
```pascal
DebugDisplayType:  array[0..DebugDisplayLimit - 1] of integer;
DebugDisplayValue: array[0..DebugDisplayLimit - 1] of integer;
```

### 17.2 TERM Configuration Example

A **create** message always begins with the display-type element and the window-name
element; `FormCreate` reads `DisplayType` from `[0]` and the name from `[1]`, then sets
`ptr := 2` before dispatching `TERM_Configure` (`FormCreate:625-632`). Directives therefore
start at index **2**, and a single `ele_end` terminates the array.

```
Element Array:
[0] type=ele_dis   value=dis_term        → display type (6)
[1] type=ele_nam   value=<name ptr>      → window instance name
[2] type=ele_key   value=key_size        → SIZE
[3] type=ele_num   value=40              → columns
[4] type=ele_num   value=25              → rows
[5] type=ele_key   value=key_textsize    → TEXTSIZE
[6] type=ele_num   value=12              → font size
[7] type=ele_end   value=0
```

### 17.3 TERM Character Output Example

For an **update** message the payload is reached via `UpdateDisplay(Index)`, which does
`ptr := Index` (`899-901`) with `Index = P2.DebugDisplayTargs` — i.e. `ptr` starts *past* the
list of targeted display names. The indices below are relative to that `ptr`, not absolute
array slots:

```
Element Array (from ptr):
[+0] type=ele_str   value=<ptr>           → 'Hello World'
[+1] type=ele_end   value=0
```

Each character processed sequentially through `TERM_Chr` (2307-2311).

---

## 18. Buffer Management and Timing

TERM holds **no character-grid model** in v55. There is no `TermBuff`, no
per-cell record, and no glyph/attribute store. The only retained terminal state is
the cursor position (`vCol`, `vRow`) and the active colors (`vTextColor`,
`vTextBackColor`, `vBackColor`); the on-screen text itself lives solely as pixels
in `Bitmap[0]`. All buffer management is therefore bitmap management.

### 18.1 The Bitmap Is the Buffer

`TERM_Chr` (lines 2317-2354) paints each glyph straight into `Bitmap[0]` with
`Canvas.TextRect`. The "buffer" of displayed characters is the bitmap — once a
glyph is drawn there is no record of which character occupies a cell, only the
rendered pixels. Consequently TERM cannot read back a cell's character; operations
that "erase" (e.g. backspace, code 8) only move the cursor and never repaint the
cell (see §9.4).

### 18.2 Write Operations

Writing a printable character runs the `else` branch of `TERM_Chr` (lines
2338-2353). It computes the cell's pixel rectangle from `vCol`/`vRow` and the
metrics `ChrWidth`/`ChrHeight` (lines 2341-2343), sets the fg/bg colors and draws
the glyph with `TextRect` (lines 2344-2346), then `Inc(vCol)` (line 2347).
Auto-wrap is handled first: `if vCol = vCols then TERM_Chr(Chr(13))` (line 2340),
which performs a CR (column reset + row advance or scroll) before drawing. There is
no intermediate cell store to update — the write is the draw.

### 18.3 Scrolling Operations

Scrolling is purely a pixel operation. When a CR arrives with the cursor already on
the last row (`vRow = vRows - 1`), the `else` block (lines 2326-2335) copies the
text area up one line with a single `Bitmap[0].Canvas.CopyRect` (line 2330) and
then `FillRect`s the freed bottom line with `vBackColor` (lines 2331-2333), setting
`vUpdateFlag` (line 2334). No row array is shifted — the rows move because their
pixels are block-copied. See §8 for the exact source rectangles.

### 18.4 Update Timing

In real-time mode (`vUpdate = False`, default) each `TERM_Chr` immediately mirrors
the just-drawn cell rectangle from `Bitmap[0]` to `Bitmap[1]` and to the on-screen
`Canvas` (guard `if not vUpdate` at **2348**; the two `CopyRect`s at **2350-2351**), so output
appears character-by-character. In buffered
mode (`vUpdate = True`, set by the `UPDATE` config directive) those per-character
copies are skipped; `Bitmap[0]` accumulates silently until an explicit `UPDATE`
directive runs `BitmapToCanvas(0)` (line 2248). Independently, `vUpdateFlag` is set
whenever a clear or scroll dirties the whole bitmap; at the end of `TERM_Update`,
`if not vUpdate and vUpdateFlag then BitmapToCanvas(0)` (line 2314) flushes those
full-bitmap changes in one copy.

---

## 19. Bitmap System and Double-Buffering

### 19.1 Bitmap Architecture

The v55 TERM window uses the same shared double-buffer present in all display
windows (declared in the form, not TERM-specific):

```pascal
Bitmap: array[0..1] of TBitmap;  // Double-buffered (shared infrastructure)
```

**Roles in TERM:**
- `Bitmap[0]` — render target; all `TERM_Chr` drawing goes here
- `Bitmap[1]` — display buffer; in real-time mode each character rect is also
  copied here and to `Canvas` immediately; in buffered mode only copied on `UPDATE`

### 19.2 Character Rendering

Character rendering in v55 is performed entirely inside `TERM_Chr` (lines
2317-2354); there is no separate `RenderChar` helper and no `TCharCell` cell type.
The procedure sets `Bitmap[0].Canvas.Font.Color := WinRGB(vTextColor)` and
`Bitmap[0].Canvas.Brush.Color := WinRGB(vTextBackColor)`, then calls
`Bitmap[0].Canvas.TextRect(r, x, y, c)` where `r` is the cell rectangle derived
from `vCol`/`vRow` × `ChrWidth`/`ChrHeight` plus the margins (rect derived **2341-2343**;
colors + `TextRect` **2344-2346**; `Inc(vCol)` **2347**). The
`Brush.Color` fills the cell background as part of the `TextRect` call, so each
glyph is opaque over its background pair color. See §6.1 for the full procedure.

### 19.3 Cursor Rendering

There is **no cursor rendering** in TERM. The terminal cursor is purely the implicit
write position `vCol`/`vRow` — the next glyph is drawn there. `DebugDisplayUnit.pas`
contains no caret-draw, no blink timer, and no cursor erase/restore for the TERM
window: nothing in `TERM_Chr` or `TERM_Update` paints a cursor indicator. Cursor
movement directives (home/set-column/set-row/backspace) only update the integer
pair `vCol`/`vRow`; they leave the bitmap untouched.

---

## 20. Shared Infrastructure

### 20.1 Color System

TERM color is controlled entirely by the eight-element `vColor[0..7]` array — four
text/background pairs filled at configuration time from `key_color` (or the
`DefaultTermColors`). There is no separate color-mode/LUT machinery for TERM (the
`LUT1..RGB24` color modes used by PLOT/BITMAP do not apply here), and there is no
`~n` color-escape syntax in the byte stream — color changes arrive only as numeric
codes 4-7 (select pair) or as named-color key directives (`key_black..key_gray`).
See §10 and the Directive Reference above for the runtime mechanics.

**TERM color storage (v55)**:
```pascal
vColor: array [0..7] of integer;     // 4 text/background pairs (config-time)
vTextColor, vTextBackColor: integer; // currently active text fg / bg
vBackColor: integer;                 // window canvas background (clear/scroll fill)
```

`vTextColor`/`vTextBackColor` are the colors applied per glyph by `TERM_Chr` (§19.2);
`vBackColor` is the fill used by `ClearBitmap` and by the scroll's bottom-line
`FillRect` (§8.1).

### 20.2 Text Metrics

The v55 `SetTextMetrics` measures `'X'` at the current size (see §11.1, lines 2919-2925). It
assigns **no font name** — because it does not need to: the face was already set once in
`FormCreate:600` (`Bitmap[0].Canvas.Font.Name := FontName`), so the measurement is of `'X'`
**in the global `FontName`**:

```pascal
procedure TDebugDisplayForm.SetTextMetrics;
begin
  Bitmap[0].Canvas.Font.Size := vTextSize;
  ChrWidth := Bitmap[0].Canvas.TextWidth('X');
  ChrHeight := Bitmap[0].Canvas.TextHeight('X');
end;
```

### 20.3 Control Character Processing

Control behavior is driven by **numeric elements**, not by in-band escape bytes.
`TERM_Update` (lines 2223-2315) dispatches each `ele_num` value through a `case`:
values 0-13 perform the control actions in §9 (clear, home, set column/row, select
color pair, backspace, tab, newline) and values 32-255 print a glyph via
`TERM_Chr`. There is no `~`-style escape mechanism in TERM — directives reach the
window as discrete protocol elements (`ele_key`, `ele_num`, `ele_str`), so a
control code such as CR is the integer `13`, not an embedded escape sequence.

The one place raw character bytes are interpreted is inside an `ele_str`: each
character of the string is passed to `TERM_Chr` verbatim (lines 2307-2311), so a
`Chr(13)` embedded in a string acts as a newline, but the string path still routes
through `TERM_Chr` rather than the numeric `case`. See §9 and the Directive
Reference above for the authoritative code table.

---

## 21. Initialization Lifecycle

### 21.1 Window Creation

The TERM window is created by the shared form infrastructure and configured by
`TERM_Configure` (lines 2181-2221). The lifecycle at creation:

1. The form **constructor** — `constructor TDebugDisplayForm.Create` (**551-576**) — installs
   the shared event handlers (`OnCreate`/`OnMouseMove`/`OnMouseWheel`/`OnKeyPress`/
   `OnKeyDown`/`OnPaint`/`OnDestroy`, 563-569) and creates the two `TTimer`s
   `MouseWheelTimer` / `KeyTimer` (570-575). **`FormCreate` does none of this.**
2. Shared `FormCreate` (**591-645**) runs — creates the double-buffer `Bitmap[0]`/`Bitmap[1]`
   as `pf24bit` (596-599); assigns the **global font face** `Bitmap[0].Canvas.Font.Name :=
   FontName` (600) and the global `vTextSize := FontSize` + `SetTextMetrics` (601-602); builds
   the measurement-cursor bitmaps (604-616) and the desktop-capture bitmap/DC (618-619);
   `SetPolarColors` (621); reads `DisplayType := P2.DebugDisplayValue[0]` (625) and sets the
   default caption `'<name> - TERM'` (626); sets `Left`/`Top` (628-629); runs the **global
   `SetDefaults`** (631 — `vBackColor = clBlack`, `vColorMode = key_rgb24`, `vUpdate = False`,
   `vHideXY = False`, `vTextSize = 10`); sets `ptr := 2` (632); dispatches `TERM_Configure`
   (640) and finally `Show` (644).
3. `TERM_Configure` applies TERM's unique defaults: `vTextSize := FontSize`,
   `vCols := DefaultCols` (40), `vRows := DefaultRows` (20), `vCol := 0`, `vRow := 0`,
   and `vColor[0..7] := DefaultTermColors` (lines 2186-2191). It then walks the
   element stream with `NextKey`, applying any `TITLE/POS/SIZE/TEXTSIZE/COLOR/
   BACKCOLOR/UPDATE/HIDEXY` directives (lines 2193-2211).
4. Active colors are seeded from pair 0: `vTextColor := vColor[0]`,
   `vTextBackColor := vColor[1]` (lines 2212-2213).
5. `SetTextMetrics` (2919-2925) runs inside `TERM_Configure` — sets the font **size** and
   measures `'X'` to get `ChrWidth`/`ChrHeight` (the **face** was already fixed at
   `FormCreate:600`); then `vWidth := vCols*ChrWidth`, `vHeight := vRows*ChrHeight`
   (lines 2216-2218).
6. `SetSize(i, i, i, i)` is called with `i := ChrWidth div 2` margin on all sides
   (lines 2219-2220); `SetSize` (2926-2971) sizes both bitmaps to the margined
   client area and calls `ClearBitmap`.

There is no `vCursorVisible`, no `vColorIndex`, and no `TermBuff` — none of these
exist in the v55 source. The only TERM state initialized is the cursor pair, the
colors, and the grid dimensions.

### 21.2 Configuration Processing

The actual v55 configuration parser (from `TERM_Configure` lines 2193-2211):

```pascal
while NextKey do
case val of
  key_title:    KeyTitle;
  key_pos:      KeyPos;
  key_size:     KeySize(vCols, vRows, term_colmin, term_colmax, term_rowmin, term_rowmax);
  key_textsize: KeyTextSize;
  key_color:    for i := 0 to 7 do if not KeyColor(vColor[i]) then Break;
  key_backcolor: KeyColor(vBackColor);
  key_update:   vUpdate := True;
  key_hidexy:   vHideXY := True;
end;
```

### 21.3 Runtime State

```
[Ready] → TERM_Update called with element stream
   ↓
[Dispatch] → ele_key? → named color / CLEAR / UPDATE / SAVE / PC_KEY / PC_MOUSE
             ele_num?  → control codes 0-13 or printable 32-255 → TERM_Chr
             ele_str?  → iterate chars → TERM_Chr each
   ↓ (per printable char in TERM_Chr)
[Render] → TextRect to Bitmap[0] at (vCol,vRow) pixel position
   ↓
[Advance cursor] → Inc(vCol); if vCol=vCols → wrap/scroll via TERM_Chr(Chr(13))
   ↓ (if not vUpdate)
[Copy rect] → Bitmap[1] + Canvas immediately updated
   ↓
Loop back to Ready
```

---

## 22. Summary

The **TERM** display window provides a simple yet effective text-based terminal interface for the Propeller 2 debug system. Its straightforward character-mode display makes it ideal for:

**Key Strengths**:
- Simple text output (no escape sequence complexity)
- Automatic scrolling for continuous logging
- Color-coded messages (4 color pairs)
- Direct cursor positioning
- Efficient real-time rendering
- Familiar terminal-like interface

**Typical Use Cases**:
- Debug messages and status output
- Data logging and monitoring
- Simple text-based UIs
- Serial console emulation
- Test result reporting

**Performance**: Capable of rendering hundreds of characters per second with hardware-accelerated scrolling, making it suitable for real-time debug output while maintaining minimal CPU overhead.

The TERM display complements the graphical displays (SCOPE, PLOT, SPECTRO) by providing a text-oriented interface for diagnostic messages, variable dumps, and interactive debugging sessions.
