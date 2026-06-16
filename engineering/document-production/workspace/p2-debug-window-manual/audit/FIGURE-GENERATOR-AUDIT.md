# Figure-Generator Audit & Rework (2026-06-13)

The `screenshot-capture/examples/fig-*.spin2` programs render the hero figures. They
were producing **empty content / dark backgrounds** (bad for a printed manual). All were
re-grounded against the **v55 golden source** directive tables, reworked for
**light, print-friendly backgrounds + high-contrast content**, and **all 10 compile clean
under `pnut-ts -d`**.

Capture scaffolding is unchanged (CON `DEBUG_DELAY`; `waitms 700` open → draw →
`waitms 500` → `SAVE` → `waitms 2000` → end-marker → `CLOSE`).

| Figure | Root problem | Fix |
|--------|--------------|-----|
| fig-03 TERM | dark (orange-on-black); troubleshooting stub | white canvas (`BACKCOLOR $FFFFFF`) + 4 print pairs (black/white labels, white/blue header, white/green ok, white/red alert); proper static dashboard frame |
| fig-04 BITMAP | OK (plasma fills canvas) | unchanged (verified compiles) |
| fig-05 PLOT gauge | **black bg + dark-grey `$404040` ticks on black = invisible** | white bg; mid-grey ticks, dark ring, blue hub, red needle; POLAR moved to runtime (v55 = PLOT Feeding) |
| fig-05 PLOT sprite | dark bg (cyan on black) | light grey-blue bg (`$ECEFF1`) + saturated blue sprite (`$FF1976D2`) |
| fig-06 LOGIC | dark default bg, possibly-invisible default traces | `COLOR $FFFFFF $C0C0C0` (white bg, grey grid) + dark-blue traces on all 8 channels |
| fig-07 SCOPE | dark default bg | white bg + grey grid + dark-blue trace + full legend `%1111` |
| fig-08 SCOPE_XY | dark default bg | white bg + grey grid + dark-blue trace + `DOTSIZE 4` |
| fig-09 FFT | dark bg; thin line | white bg + grey grid + **filled bars (`LINESIZE -3`)** + blue trace. ⚠ **max-amplitude (channel field 3, currently 400000) may need tuning** so the two peaks reach ~75% height |
| fig-10 SPECTRO | dark (LUMA8X = black→colour) + only 60 lines | **LUMA8W** (white→blue, light bg) + fill full `DEPTH` (256 frames). ⚠ **RANGE/MAG may need tuning** for contrast |
| fig-11 MIDI | 88-key default range, 3 lit keys, far too wide | `RANGE 55 72` (~1.5 octaves) + `SIZE 12` (legible keys); blue/red lit-key colours |

## Tuning flags for the external render pass
- **fig-09 FFT** — adjust the channel `max` field (and `mag`) so the two tone peaks fill the plot.
- **fig-10 SPECTRO** — adjust `RANGE` (saturation power) / `MAG` so the chirp diagonal is well-saturated against the white background.

These two are scale-dependent and cannot be tuned without seeing the render; the rest
should render correctly as written.

## Manual ↔ external consistency
- **fig-03 ↔ Ch3 dashboard:** synced (both now the white/light scheme). 
- **Remaining manual worked-examples** (Ch5 gauge, Ch7 SCOPE, Ch8 SCOPE_XY, Ch9 FFT, etc.):
  their creation/colour directives should be synced to the final generators **after** the
  external render confirms the visuals (so FFT/SPECTRO scale tuning is mirrored once, not twice).

---

## RESUME CHECKPOINT (2026-06-13, context cleared here)

**Single source of truth:** `manuals/p2-debug-window-manual/figure-generators/` (11 .spin2).
The internal `workspace/.../screenshot-capture/` duplicate was REMOVED — do not recreate it.

**Generators state:** all 11 rewritten on the **v55 golden idioms** and compile-clean (`pnut-ts -d`):
- SINGLE-quoted strings in every backtick stream (double quotes render blank).
- NAMED colors + brightness only (raw-hex `COLOR`/`BACKCOLOR` are ignored); `BACKCOLOR` on creation.
- Theme: white background, blue primary (`$1976D2` = Spin2 code color), named semantic accents;
  SPECTRO=`LUMA8W`; BITMAP plasma kept vivid; MIDI light piano w/ blue/red lit keys.

**Next render pass (user generates externally, clearing old BMPs first) — confirm:**
1. Do **instrument** windows (SCOPE/LOGIC/SCOPE_XY/FFT) honor `COLOR WHITE GRAY` for a WHITE
   background? If they come up dark, switch those to **bright traces on native dark** (proven).
2. **FFT/SPECTRO** magnitude scaling may need a tweak (flagged in-file).

**THEN — figures ↔ manual-text sync (NOT yet done, required to 100%):**
Every `fig-XX` cited in a chapter must match (a) its generator and (b) that chapter's worked-example
code. Audit each chapter's figure citation against the generator + worked example; reconcile drift.

**THEN — PDF:** prepare-manual → Forge (manual also flagged to-regenerate behind platform
`figures.lua`/`content.sty`).
