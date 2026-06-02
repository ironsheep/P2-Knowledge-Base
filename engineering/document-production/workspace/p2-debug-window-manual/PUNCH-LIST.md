# Punch List — P2 Debug Window Manual

Outstanding work items. Sweep completed items into a dated archive at closeout.

## Screenshot capture — figures pending (opened 2026-06-02)

The screenshot-capture pipeline (`screenshot-capture/`, run on a P2 with `pnut-ts`
compile + `pnut-term-ts -r` run; each example `SAVE`s its own window; `CLOSE` makes it
hands-off) works end-to-end. **5 of 10 hero figures render correctly and are in the
manual; 5 are placeholders pending these fixes:**

**Captured & in the manual (real images):**
`fig-04-bitmap` (plasma) · `fig-05-plot-gauge` · `fig-05-plot-sprite` · `fig-06-logic`
(8-ch counter) · `fig-11-midi` (keyboard; see note).

**Placeholders pending — two root causes to solve:**

1. **Channel-config windows ignore the channel definition.**
   - `fig-07-scope` — shows "Channel 0" at 0–255 (my `'Wave' lo hi` range had no effect),
     so the ±1000 sine clips into a trapezoid.
   - `fig-09-fft` — empty frame; the channel def (`'Mag' …`) produced no magnitude trace.
   - `fig-10-spectro` — empty waterfall (also magnitude/RANGE/MAG scaling).
   - LOGIC's channel defs *worked* on the creation line, but SCOPE/FFT's do not.
   - **Action:** study `REF/theory-of-operations/{SCOPE,FFT,SPECTRO}` for the exact
     channel-definition placement (creation-line vs update-phase) and the magnitude
     scaling, instead of guessing.

2. **"Only the first message registers."**
   - `fig-03-term-dashboard` — TERM text won't render: positioned version showed one stray
     glyph; plain-text version is fully blank. (Graphics windows render their own text
     labels fine, so pnut-term-ts *can* draw text — TERM character output specifically isn't.)
   - `fig-11-midi` — only the first of three note-ons lights (single key, not the C-E-G
     triad). The keyboard image itself is good, so it ships as-is for now.
   - `fig-08-scope-xy` — never produces a `.bmp` at all; the Lissajous window may not open
     or the example errors at runtime.
   - **Action (needs live observation on hardware):** when each runs, does the window show
     content *live* before it closes (→ SAVE-timing) or is it blank/absent live (→ render
     bug)? Then fix accordingly.

**Confirmed working technique notes (for when we resume):**
- `DEBUG_DELAY` (≈1000 ms) before transmitting is required so the host window is open.
- Rapid feeds race; **pace them** (a small `waitms` per row fixed the BITMAP streaks).
- `` `Win CLOSE `` *does* work (closes the window, enables hands-off capture) — the golden
  matrix is wrong that it "has no live handler"; flag for upstream REF correction, and add
  `CLOSE` to ch01's "commands common across windows".

## Other

- (none yet)
