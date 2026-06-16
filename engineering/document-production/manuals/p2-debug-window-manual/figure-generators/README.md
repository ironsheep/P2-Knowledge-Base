# Figure Generators — P2 Debug Window Manual

Runnable Spin2 programs that **produce the manual's figures on real P2 hardware**.
Each program draws the exact scene for one figure, then captures it with the
DEBUG-window `SAVE WINDOW` directive and halts. Run it, and the host writes a
`.bmp`; convert that to the `.png` the manual embeds.

These are **separate from the manual's teaching examples** — the capture plumbing
(`SAVE WINDOW`) lives here, never in the chapter code a reader sees.

## How to capture

1. Compile + run the generator on a P2 with a debug terminal attached.
2. When it halts, the terminal host has written `<figure-name>.bmp` to the host.
3. Convert to PNG and drop it into the manual's assets, e.g.:
   ```
   python3 -c "from PIL import Image; Image.open('fig-07-scope.bmp').save('fig-07-scope.png')"
   ```
   then copy into `../../workspace/p2-debug-window-manual/assets/`.

**Capture convention (per correction F-024):** `SAVE WINDOW 'name'` — give the
name **without** an extension; the directive appends `.bmp` automatically
(`'fig-07-scope'` → `fig-07-scope.bmp`). Including `.bmp` yields `.bmp.bmp`.

> **Capture host: `pnut-term-ts`.** It drives the window display and performs the
> `SAVE WINDOW` capture, writing a `.bmp`. Hand the `.bmp` files back; they are
> converted to the `.png` the manual embeds (PIL one-liner above), then copied
> into the manual's `assets/`.

## Figure → generator map

| Figure (asset) | Window | Generator |
|---|---|---|
| `fig-03-term-first.png`     | TERM     | `fig-03-term-first.spin2` |
| `fig-03-term-dashboard.png` | TERM     | `fig-03-term-dashboard.spin2` |
| `fig-04-bitmap.png`         | BITMAP   | `fig-04-bitmap.spin2` |
| `fig-05-plot-gauge.png`     | PLOT     | `fig-05-plot-gauge.spin2` |
| `fig-05-plot-pid.png`       | PLOT     | `fig-05-plot-pid.spin2` |
| `fig-05-plot-sprite.png`    | PLOT     | `fig-05-plot-sprite.spin2` |
| `fig-06-logic.png`          | LOGIC    | `fig-06-logic.spin2` |
| `fig-07-scope.png`          | SCOPE    | `fig-07-scope.spin2` |
| `fig-07-scope-glitch.png`   | SCOPE    | `fig-07-scope-glitch.spin2` |
| `fig-08-scope-xy.png`       | SCOPE_XY | `fig-08-scope-xy.spin2` |
| `fig-09-fft.png`            | FFT      | `fig-09-fft.spin2` |
| `fig-10-spectro.png`        | SPECTRO  | `fig-10-spectro.spin2` |
| `fig-11-midi.png`           | MIDI     | `fig-11-midi.spin2` |

## Provenance

Command sequences are taken from the **audited** opus-master chapters (ch03–ch11),
not the pre-audit `examples-library/` demos (which use commands the content audit
flagged, e.g. `AXIS`/`GRID`/`POINT`, `CHANNELS`/`LABELS`). Every generator is
compile-certified with `pnut-ts`. Scenes are a first cut — refine against the
first real capture.
