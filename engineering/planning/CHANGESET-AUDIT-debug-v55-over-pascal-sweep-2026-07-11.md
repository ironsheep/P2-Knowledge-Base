# Changeset Audit — DEBUG Manual: v55-text-over-Pascal reversal class

**Date:** 2026-07-11
**Commit swept:** `f3e702ed` ("Fabrication-audit §6: class-wide correctness sweep A")
— the **pre-empirical** doc sweep whose editors verified against Spin2 **v55 text**
(the derivative that carries errors), not against the Pascal-derived REF.
**Class audited:** DEBUG-window **defaults / keyword-availability / value→behavior
mappings** where the manual (at HEAD) follows v55 text but contradicts the
higher-authority chain **Pascal `DebugDisplayUnit.pas` → REF → v55 text**, with
empirical (real-P2) findings outranking all.
**Authorities used:** `REF/theory-of-operations/*.md` (Pascal-quoting, v55-verified
2026-06-01), `REF/DEBUG-WINDOW-DIRECTIVE-MATRIX.md`,
`ingestion/.../hardware-verification/P2-EMPIRICAL-FINDINGS.md` (EF-025..032).
**Windows covered:** TERM, BITMAP, PLOT, LOGIC, SCOPE, SCOPE_XY, FFT, SPECTRO, MIDI.

## Bottom line

**The class is NOT yet clear beyond the known 3.** Five additional confirmed
instances survive at HEAD, plus one secondary (conflicted) cluster.

- The empirical conflict-test batch (EF-025..032, 2026-07-10/11) already drove
  reversions **beyond** the 3 the changeset-audit named: LOGIC `SAMPLES`/`SPACING`/
  `LINESIZE` (EF-027), FFT negative-`LINESIZE` filled-bars (EF-026), and MIDI
  `$RRGGBB` color (EF-029) are all **correct at HEAD**. Good.
- But that batch tested only TERM / FFT-linesize / LOGIC-ranges / PLOT-textstyle /
  MIDI-color / SCOPE-size. **BITMAP was never conflict-tested**, so its two sweep
  reversals slipped through unchallenged — and the `POS`/`TITLE` default reversals
  and the FFT channel-`grid` field were not in scope of any EF test either.

**New confirmed instances (still wrong at HEAD): 5** — FFT-legend, BITMAP-SPARSE,
BITMAP-LUT, POS-default, TITLE-default. **Plus 1 secondary cluster** (LINESIZE/
DOTSIZE "half-pixels") where REF-fixed-point and empirical conflict.

---

## Per-window checklist

| Window | Verdict |
|---|---|
| **TERM** | **FLAG** — POS default `0, 0` (F-4); TITLE default `none` (F-5). Color pair `Lime` = D-F2, already fixed ✓ |
| **BITMAP** | **FLAG** — SPARSE described as round-dot / background-color / needs DOTSIZE≥4 (F-2); LUT "entries 0–7 hold default colors" (F-3). Both contradict REF; both were correct pre-sweep. |
| **PLOT** | **minor** — dropped the "default text color is white" fact (N-1). TITLE default `none` (F-5). PRECISE default = D-F1, already fixed ✓ |
| **LOGIC** | **FLAG** — POS default `0, 0` (F-4); TITLE default `(none)` (F-5). SAMPLES/SPACING/LINESIZE (EF-027) already fixed ✓; DOTSIZE row (D-F3) restored ✓ |
| **SCOPE** | **FLAG (secondary)** — LINESIZE relabeled "half-pixels, 3 = 1.5 px" (S-6), contradicts EF-027 + LOGIC's own "pixels." |
| **SCOPE_XY** | **FLAG** — POS default `0, 0` (F-4); DOTSIZE "half-pixels, 6 = 3-pixel dot" (S-6, secondary). |
| **FFT** | **FLAG** — channel `grid` field rewritten as 4-bit "legend" with text-legend bits 2–3 (F-1); LINESIZE "half-pixels" (S-6, secondary). Negative-linesize filled-bars (EF-026) already fixed ✓ |
| **SPECTRO** | **CLEAN** — the `SIGNED`/zero-extend-by-default rewrite is a *correct* fix (matrix §7.1, §8.6). No POS/TITLE default claim was changed here. |
| **MIDI** | **FLAG (POS only)** — POS default `0 0` (F-4). TITLE `none (window name)` is correct ✓; COLOR `$RRGGBB` (EF-029) already fixed ✓ |

---

## New instances (contradict the higher-authority REF at HEAD)

### F-1 · FFT channel-def "legend" field fabricates a 4-bit legend-text mapping
- **Manual (HEAD, `ch09-fft.md:132`, also 135/142/265/370):**
  "`legend` | Legend flags (`%abcd`): bit 0 = min (baseline) line, bit 1 = max
  (top) line, **bit 2 = min-value legend text, bit 3 = max-value legend text**"
- **REF (`FFT_Theory_of_Operations.md`):** field is **`grid`**, an int bitfield
  "**bit 0 = baseline line, bit 1 = top line, default 0**" (L110, L203). The
  Pascal draw path tests **only** `vGrid[i] and 1` (baseline) and `vGrid[i] and 2`
  (top) — L738-749 — and there is **no legend-text rendering** anywhere keyed off
  bits 2–3. Matrix §7.3 FFT and §5.4 likewise name the field `grid`.
- **Verdict:** the manual's bits 2–3 "legend text" behavior is a **fabrication**;
  renaming `grid`→`legend` also drops the accurate name. Only 2 line-flag bits exist.
- **Reader-harm:** a reader who sets bit 2/3 expecting on-canvas min/max value
  labels gets nothing; the `%abcd` framing invents two nonexistent controls.
- **Proposed fix:** restore the field name **`grid`** and the 2-bit mapping
  (bit 0 = baseline line, bit 1 = top line); delete the bit 2/3 legend-text rows and
  the "legend flag"/"legend line" prose (revert L12/135/142/265/370 wording to grid).

### F-2 · BITMAP SPARSE described as round-dot / background-color / DOTSIZE≥4
- **Manual (HEAD, `ch04-bitmap.md:49`, also 48/310-311/323/398-401):**
  "`SPARSE color` | **Round-dot mode (needs `DOTSIZE`≥4); sets the background
  color**"; "SPARSE draws each magnified pixel as a large **round dot against its
  background color** (and requires a `DOTSIZE` of at least 4)."
- **REF (`BITMAP_Theory_of_Operations.md`, Path 2 sparse render, L524-556):**
  each logical pixel is drawn as a **bordered square block** — `SmoothShape(...,
  vDotSize, vDotSizeY, 0,0,0, vSparse, 255)` (rectangle, corner-radius 0) for the
  **border in `vSparse` color**, then an inner data-color fill at 75% size.
  Summary text: "Outer border in `vSparse` color (**grid effect**)… Creates
  magnified pixel display with **visible grid**." `vSparse` is the **border/grid
  color** (L91), **not** a background; there is **no DOTSIZE≥4 gate**.
- **Verdict:** wrong on three counts (round-dot, background-color, ≥4 gate). The
  **pre-sweep manual was correct** ("SPARSE sets the grid-border color"; square
  block with grid border) — the sweep reversed it toward v55-text phrasing.
- **Reader-harm:** reader expects round dots on a colored background; actual output
  is grid-bordered square blocks where the "background" color they picked is the
  grid line color. The heatmap example (L306-324) mis-describes its own render.
- **Proposed fix:** restore square-block-with-grid-border wording; `SPARSE color`
  sets the **grid/border color**; drop "round dot" and the "DOTSIZE≥4" requirement.

### F-3 · BITMAP LUT modes claim a built-in default palette (entries 0–7)
- **Manual (HEAD, `ch04-bitmap.md:84-87`):** "If you select a LUT mode without
  defining a palette, **entries 0–7 hold default colors** — so `LUT1` and `LUT2`
  render entirely in those defaults, while `LUT4`/`LUT8` leave entries above 7
  undefined."
- **REF (`BITMAP_Theory_of_Operations.md:606`):** "**Default contents are
  undefined**: `SetDefaults` (2880–2917) does **not** initialize `vLut[]`, so until
  a `LUTCOLORS` directive populates it, **LUT-mode pixels translate to garbage**."
- **Verdict:** wrong — there is **no** default LUT palette; the array is
  uninitialized. The **pre-sweep manual was correct** ("uninitialized… render as
  garbage… you must supply one with `LUTCOLORS`").
- **Reader-harm:** reader trusts `LUT1`/`LUT2` to show sensible default colors
  without `LUTCOLORS` and instead gets garbage/undefined pixels.
- **Proposed fix:** restore "uninitialized → garbage; supply `LUTCOLORS`" wording.

### F-4 · POS default stated as screen `0, 0` (should be cascaded / offset-from-base)
- **Manual (HEAD):** POS default = `0, 0` in **TERM** (`ch03:43`), **LOGIC**
  (`ch06:57`), **SCOPE_XY** (`ch08:50`), **MIDI** (`ch11:45`) — column labels the
  row "Screen position of the window, in pixels."
- **REF:** `LOGIC_Theory_of_Operations.md:362` — "`POS left top` | **cascaded** |
  screen coords"; matrix §7.3 — "`POS left, top` · int (**offset from base window
  pos**)"; a bare/absent POS leaves the window at its auto-cascade position
  (LOGIC theory L377-379, `KeyPos` 2712-2716).
- **Verdict:** "`0, 0`" misrepresents the default as the screen origin; the true
  default is a cascade/auto placement (0,0 is only the *offset from the base*, not a
  screen coordinate). Also internally inconsistent — SCOPE says "cascaded",
  PLOT/BITMAP/SPECTRO/FFT say "auto", these four say "0, 0".
- **Reader-harm:** implies every untouched window pins to the top-left corner and
  overlaps at (0,0); actually they auto-cascade.
- **Proposed fix:** set POS default to **"cascaded"** (or "auto") across all nine
  for consistency with SCOPE and the REF.

### F-5 · TITLE default stated as `none` (should be the window's instance name)
- **Manual (HEAD):** TITLE default = `none` in **TERM** (`ch03:42`) and **PLOT**
  (`ch05:40`); `(none)` in **LOGIC** (`ch06:56`).
- **REF:** `LOGIC_Theory_of_Operations.md:361` — "`TITLE 'string'` | **(window
  name)**"; matrix SCOPE_XY footnote — "with no `TITLE`, the caption is
  `<name> - SCOPE_XY`." The default caption is the window's **instance name**, not
  blank.
- **Verdict:** "`none`" implies a blank title bar; the caption actually defaults to
  the window name. MIDI already carries the correct form **"none (window name)"**;
  SCOPE/BITMAP/FFT/SPECTRO still show the window *type* name (also imprecise, but
  untouched by the sweep).
- **Reader-harm:** reader believes untitled windows have empty captions.
- **Proposed fix:** state the default as **"(window name)"** (adopt MIDI's phrasing)
  for TERM/PLOT/LOGIC; ideally normalize all nine.

---

## Secondary cluster (REF-fixed-point vs empirical conflict — needs a test, not a guess)

### S-6 · "half-pixels" relabeling of LINESIZE / DOTSIZE
- **Manual (HEAD):** SCOPE `LINESIZE` "in **half-pixels** (default `3` = **1.5 px**)"
  (`ch07:58`); FFT `LINESIZE` "Line width **in half-pixels**" (`ch09:81`);
  SCOPE_XY `DOTSIZE` "Sample-dot size **in half-pixels**… `6` draws a **3-pixel dot**"
  (`ch08:55`).
- **Two authorities disagree:**
  - *Fixed-point REF (why the sweep wrote this):* `SmoothLine`'s size arg is a
    **radius** = `vLineSize shl 6` while coordinates are `shl 8` (FFT theory
    L1142/1166/1185; SCOPE theory L1646) — arithmetically a **half-pixel** line
    width. This is a defensible literal reading.
  - *Empirical (outranks):* **EF-027** measured the *shared* line renderer on real
    P2 as `LINESIZE 3 → 3 px` thick (1→1, 3→3, tapering only at large values), i.e.
    **≈1:1, not 1.5 px**. The REF directive tables also call these plain
    "pixels" / "dot diameter in pixels" (SCOPE theory L385/527; SCOPE_XY L330/459),
    and the **LOGIC** chapter (same renderer) correctly says "pixels."
- **Verdict:** the "half-pixels / 3 = 1.5 px" claim contradicts the empirical
  ground truth and is **inconsistent** with LOGIC's plain "pixels" for the identical
  primitive. Treat as a likely error, but not a clean documentary reversal —
  the fixed-point math genuinely supports it, so it warrants the same empirical
  settlement LOGIC got.
- **Proposed fix:** revert SCOPE/FFT `LINESIZE` and SCOPE_XY `DOTSIZE` to plain
  **"pixels"** to match LOGIC + EF-027; OR run a targeted conflict-test
  (`SCOPE/FFT LINESIZE {1,3,7,32}`, `SCOPE_XY DOTSIZE {2,6,20}`, window-width
  pixel-ruler) to record an EF and word the manuals to it. Do **not** leave the
  same renderer described two different ways across chapters.

---

## Notes / cleared / out-of-class (not counted as findings)

- **N-1 · PLOT text color (`ch05-plot.md`):** the sweep dropped the accurate fact
  that the **default text color is white (`$FFFFFF`)**, separate from the cyan draw
  color (PLOT theory L242/3181; matrix §7.0 `textColor = clWhite`). The replacement
  guidance — "set `COLOR` just before a `TEXT` command to change the text color" —
  **is correct** (the `COLOR`-immediately-before-`TEXT` peek-ahead, PLOT theory
  L472). Low-severity: restore the "default text color is white" sentence and
  tighten "the same `COLOR` also colors `TEXT`" so it doesn't read as *every* COLOR.
- **SPECTRO `SIGNED` / zero-extend-by-default:** a *correct* fix (matrix §7.1 lists
  `SIGNED` as a modifier; §8.6 confirms default zero-extend). Cleared.
- **LUMA8X / HSV*X "black → color → white, peaking in white":** REF only says
  "expanded range" (BITMAP theory L572); the sweep's specific ramp is neither
  confirmed nor refuted by REF. Not asserted wrong — flag for a `TranslateColor` /
  color-appendix check if BITMAP is re-audited.
- **PLOT `SPRITEDEF`/`SPRITE` "added earlier (V35n)":** a Spin2 *version-gating*
  claim, not a window default / keyword-availability claim — out of this class.
- **SCOPE `` `() `` = shorthand for `SDEC_` (signed):** a DEBUG *feed-formatting*
  fact, not a window config default/keyword — out of this class; not evaluated here.
- **TEXTSIZE "editor size" (LOGIC/SCOPE_XY/FFT):** correct per §7.0a
  (`FontSize` = editor size). SCOPE still says "10" (the default editor size) — a
  harmless wording inconsistency, not a contradiction.

---

## Is the class cleared?

**No — five confirmed instances (F-1..F-5) plus one secondary cluster (S-6) remain
before Debug re-audit.** The known 3 (D-F1 PLOT PRECISE, D-F2 TERM color, D-F3
LOGIC DOTSIZE) are fixed, and the empirical batch additionally cleared LOGIC ranges
(EF-027), FFT filled-bars (EF-026), and MIDI color (EF-029) — but the batch's window
coverage had gaps, and the sweep's reversals in **BITMAP** (F-2, F-3, never
conflict-tested) and the **POS/TITLE default** and **FFT grid→legend** rewrites
(F-1, F-4, F-5) were never checked against the Pascal REF and are still live at HEAD.
Fix F-1..F-5 (documentary — REF is unambiguous); settle S-6 by reverting to "pixels"
or by one targeted linesize/dotsize hardware test.
