# Debug Window Manual — Example Audit Rubric & Truth Matrix

**Created:** 2026-06-13
**Purpose:** the single standard for auditing every `debug()` example (manual +
figure generators) against the **PNut v55-reconciled** P2KB YAMLs
(`deliverables/ai/P2/language/spin2/debug-displays/*.yaml` +
`statements/debug.yaml`). The manual predates the v1.8.0/v1.9.0 reconciliation,
so every example must be re-verified.

**Authority order:** the window YAML (`debug-displays/<win>.yaml`) and the
`string_quoting` block in `statements/debug.yaml` are ground truth. NOTE: the
legacy top of `statements/debug.yaml` (control_characters "12 = form feed",
trailing-backtick examples) is **stale and contradicts the window YAMLs** — do
NOT cite it; it is logged separately for a YAML-head correction.

---

## A. The string-quoting model (THE headline failure mode — silent, no error)

Three contexts in a `debug()` call, each with its own quote rule:

| Context | Quote | Why |
|---|---|---|
| **Plain (non-backtick) debug** text — `debug("temp=", udec_(x))` | **double** `"…"` | `'` here starts a Spin2 comment, not a string |
| **Streamed text/data** in a backtick window (TERM printing, etc.) — `` debug(`Term "Ready." 13) `` | **double** `"…"` | a Spin2 string literal → character stream (CORRECT, idiomatic) |
| **Display-command ARGUMENT** — `TITLE 'x'`, `SAVE 'x'`, `LAYER n 'x.bmp'` | **single** `'…'` | parsed by the display engine (`check_dd_str`, apostrophe-only) |
| Inside `` `(expr) `` substitution | **double** (normal Spin2) | it is ordinary Spin2 expression syntax |

**THE BUG to hunt:** a **command argument** (TITLE / SAVE / LAYER filename / any
keyword that takes a string) written with **double quotes**. Result: the chars
get streamed as data, the command consumes no argument, the title/filename is
**silently lost — no compile error.** e.g. `` SAVE "shot") `` → no file written.

**NOT a bug:** double-quoted text being *printed* to a TERM window
(`` debug(`MyTerm "Ready." 13) ``). The v55 YAML's own examples use double quotes
for streamed TERM text. Do **not** "fix" these to single quotes.

**Other quoting facts:**
- **No escape** in display strings: the first `'` closes the string — a literal
  apostrophe cannot appear in a TITLE/SAVE/etc.
- **SAVE auto-appends `.bmp`** — give the base name only (`SAVE 'shot'` → `shot.bmp`;
  `SAVE 'shot.bmp'` → `shot.bmp.bmp`).

## B. Cross-cutting rules

- **Formatters:** value-only forms end in `_` (`udec_`, `uhex_`, `sdec_`, `fdec_`).
  In a backtick stream they are written tick-prefixed: `` `udec_(x) ``. The
  with-name forms (`UDEC(x)` → `x = 42`) are for plain debug. Shorthands in the
  tick stream: `` `(x) `` = SDEC_, `` `$(x) `` = UHEX_, `` `%(x) `` = UBIN_,
  `` `.(x) `` = FDEC_, `` `#(x) `` = send char code x.
- **Bare number = command code; formatted number = displayed text.** A bare `13`
  in TERM is CR, not the text "13".
- **TERM code 12 does NOTHING** (it is in the 14..31 fall-through). Clear with
  code **0** or the `CLEAR` keyword. "12 = clear/form-feed" is a serial-terminal
  carry-over error — flag any occurrence.
- **No numeric bytecode/opcode values** for debug commands (project convention) —
  refer to commands by name.
- **`pnut_ts -d`** is required to compile-verify DEBUG examples (without `-d` the
  compiler ignores debug() contents — a false pass).
- Window opens on its creation `debug()`; programs end with a `repeat` to keep
  windows alive.

## C. Per-window truth matrix (verify each claim/param against these)

**TERM** — text grid in **CHARACTERS** (SIZE cols rows; cols/rows 1..256, default
40×20 — NOT pixels). TEXTSIZE 6..200. 4 COLOR pairs; codes 4–7 select pair.
Control codes: 0=clear+home, 1=home, `2 n`=col, `3 n`=row, 4–7=pair, 8=backspace
(non-destructive), 9=tab, 10=LF(=CR), **12=NOTHING**, 13=CR, 32..255=glyph;
14..31 do nothing. No VT100/ANSI, no scrollback, no char read-back. TITLE single-quoted.

**BITMAP** — SIZE w h **pixels** 1..2048 (default 256×256). 19 color modes (LUT1/2/4/8,
LUMA8/8W/8X, RGBI8/8W/8X, RGB8, HSV8/8W/8X, HSV16/16W/16X, RGB16, RGB24=default).
Max depth **RGB24 — no 32-bit/alpha; "RGB565" is NOT a keyword (it's RGB16).**
DOTSIZE x{y} 1..256. SPARSE color (-1=off). TRACE 0..15 (bits0-2 scan, bit3 scroll).
RATE (-1=whole frame, 0=per-line). SET x y (random access, cancels scroll). SCROLL x y.
**No sprites** (sprites are PLOT). SAVE {file}|WINDOW|`l t w h`.

**PLOT** — drawing canvas, **not a chart plotter** (no line/scatter/bar chart,
no auto-scale, no axes/legend). SIZE w h 32..2048 (default 256×256). Geometry:
ORIGIN, SET, DOT, LINE (advances pos), CIRCLE w, OVAL w h, BOX w h, OBOX w h xr yr
(ROUNDED rect), **linesize 0 = filled**. POLAR {twopi {theta}}, CARTESIAN {flipy {flipx}}.
COLOR (value | named {0-15 brightness}); named except BLACK/WHITE take brightness.
OPACITY 0..255. PRECISE (8.8 sub-pixel toggle, starts ON). LINESIZE. TEXT {size {style
{angle}}} 'str'. TEXTSIZE/TEXTSTYLE/TEXTANGLE. LAYER n 'file.bmp' (n 1..8). CROP layer
(AUTO x y | l t w h {x y}). SPRITEDEF id xsize ysize (1..32) pixels... 256 colors.
SPRITE id {orient 0..7 {scale 1..64 {opacity}}}. SAVE 'name'. LAYER/SPRITE filenames
single-quoted. Coords need `` `(...) `` to evaluate expressions.

**LOGIC** — digital waveforms; **raw capture, NO protocol decode (I2C/SPI/UART/CAN),
no baud detect, no timing measurement.** SAMPLES 4..2047 (default 32; single int —
NO {first last}). SPACING 1..32 (HORIZONTAL time-axis pixel gap, default 8 — NOT
vertical). RATE 1..2048 (draw-rate divisor, NOT sample rate). DOTSIZE single scalar
0..32 (NO x{y}). LINESIZE 1..32 (default 3). COLOR back grid. Channel-def string
`'name' {count} {RANGE} {color}`. TRIGGER mask match {offset} (**EDGE-armed**:
arms on non-match, fires on transition into match — not a static level match).
HOLDOFF 2..2048. SAVE.

**SCOPE** — analog time-domain (Y vs sample index); **no auto-measure (Vpp/RMS/freq/
period/duty/rise-fall), no cursors, no XY mode (that's SCOPE_XY), no FFT overlay.**
SIZE w h 32..2048. SAMPLES 16..2048 (default 256). RATE 1..2048. DOTSIZE 0..32.
LINESIZE 0..32 (default 3; both 0 → DOTSIZE forced 1). COLOR back grid (NOT per-channel).
Up to 8 channels, def string `'label' (AUTO | lo hi) {tall} {base} {grid} {color}`.
TRIGGER channel(-1..7, -1=free-run) (AUTO | arm fire) {offset} — **level arm/fire
only** (no edge/window/external, no Auto/Normal/Single modes). HOLDOFF 2..2048.

**SCOPE_XY** — signal-vs-signal (Lissajous/phase/polar), **distinct from SCOPE.**
SIZE **single value** n → square, width=height=n*2 px (default 256→512). RANGE
1..$7FFFFFFF (±n Cartesian / 0..n radius polar). SAMPLES = **persistence** (0=persistent
accumulate; n>0=fading trail depth) — NOT a time buffer. RATE. DOTSIZE 2..20 (default 6).
POLAR {twopi {theta}}. LOGSCALE. Up to 8 traces, def `'label' {color}`. **NO TRIGGER,
no HOLDOFF, no LINESIZE (plots dots), no auto-range, no UPDATE/buffered mode.**

**FFT** — magnitude spectrum (fixed Hanning window, **not selectable**); **magnitude
only (no phase shown), no THD/SNR/bandwidth/peak-detect/harmonic, no averaging, no
waterfall (that's SPECTRO), no markers.** SAMPLES n {first last}: n = FFT size, power
of two 4..**2048 (NO 4096)**, default 512; first/last = displayed bin range (zoom).
RATE. DOTSIZE 0..32. LINESIZE -32..32 (default 3; positive=polyline, 0=no line,
**negative=filled bars of width |n|**). COLOR back grid. LOGSCALE (log of arbitrary
power — **NOT calibrated dB**). Channel def `'label' {mag {high {tall {base {grid {color}}}}}}`,
mag 0..11.

**SPECTRO** — waterfall spectrogram. SAMPLES n {first last} (n power of two 4..2048,
default 512). DEPTH 1..2048 (time-history lines). MAG n (2^n multiplier, 0..11).
RANGE 1..$7FFFFFFF. RATE (default SAMPLES/8). TRACE 0..15 (bits0-2 scroll dir, bit3
enable; default $F). DOTSIZE x{y} 1..16. **Color modes RESTRICTED to LUMA8/8W/8X and
HSV16/16W/16X only (default LUMA8X) — LUT/RGB/HSV8 are REJECTED. No named color maps
(Heat/Rainbow), no persistence, no cursors.** LOGSCALE. Axes depend on TRACE.

**MIDI** — piano keyboard; **live display only (no event list/piano-roll/timeline,
no analysis/filter/import-export). The KEYBOARD/GRID/ROLL/MONITOR modes do NOT exist.**
SIZE = **key-size scalar 1..50** (default 4; pixel size = 8+n*4 — NOT pixels). RANGE
firstKey lastKey 0..127 (default 21..108). CHANNEL 0..15 (**exact filter — 0 = channel 0
only, NOT "all"**). COLOR onWhite onBlack (default CYAN, MAGENTA). Stream: Note-On
`$9n note vel`, Note-Off `$8n note 0`; running status honored. **MIDI is the only window
with NO HIDEXY.**

**Shared (all windows):** TITLE 'str', POS left top, CLEAR, SAVE, PC_KEY, PC_MOUSE,
HIDEXY (except MIDI), UPDATE (buffered: TERM/BITMAP/PLOT only). PC_KEY/PC_MOUSE wire
formats per `debug-commands/pc_key.yaml` / `pc_mouse.yaml` (note Y-inversion gotchas).
- **CLOSE** — `` debug(`Name CLOSE) `` closes that NAMED window. This is a REAL shared
  display directive (confirmed by Stephen 2026-06-13). **The P2KB v55 YAMLs OMIT it**
  (all 9 windows + statements/debug.yaml) — that is a KB gap logged for the YAML head,
  NOT a manual defect. Do NOT remove CLOSE from the manual or figure generators.
  Distinct from `DEBUG(DEBUG_END_SESSION)` (const 27, {Spin2_v52}) which ends the WHOLE
  session (every window + DEBUG.LOG). The manual's Ch1 claim "there is no close command"
  is therefore WRONG and must be fixed; CLOSE belongs in Ch1's shared-commands list.

**CRITICAL classification caveat (learned via the CLOSE inversion):** absence of a
keyword/feature from the v55 YAML is NOT proof the manual is wrong — the YAML has at
least one confirmed omission (CLOSE). Before classifying anything FABRICATED, check
whether the manual states it CONSISTENTLY (multiple chapters) and/or the figure
generators (Stephen-authored) use it; if so, treat it as a candidate KB-gap and
VERIFY with primary source / Stephen rather than deleting doc content.

## D. Finding classification (use these in every audit)
- **FABRICATED** — feature/keyword/mode that does not exist in the YAML (e.g. RGB565,
  MIDI display modes, SCOPE measurements, LOGIC protocol decode).
- **QUOTING** — double-quoted command argument (silent-loss bug) or other quote error.
- **WRONG-PARAM** — out-of-range / wrong-arity / wrong-unit param (e.g. SCOPE_XY two-value
  SIZE, MIDI SIZE as pixels, code 12 clear, SAMPLES 4096).
- **WRONG-SEMANTICS** — claim about behavior that contradicts the YAML (TRIGGER as level
  not edge for LOGIC; SCOPE_XY SAMPLES as time-depth; LINESIZE sign meaning).
- **FORMATTER** — wrong formatter form/shorthand.
- **STALE-PROSE** — narrative describing a non-existent capability.
- **OK** — verified correct (record so we know it was checked).

## E. Output format (every audit pass returns this)
A table: `Chapter | Line/quote | Class | What's wrong | YAML evidence | Proposed fix`.
Do NOT edit — gather only. Findings consolidate into DEBUG-EXAMPLE-AUDIT-FINDINGS.md.
