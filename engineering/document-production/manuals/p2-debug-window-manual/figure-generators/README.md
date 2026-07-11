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

### No-fig chapter generators (ch01/02/12/13/14/15) + KEEP re-runs — added 2026-07-11 (§6 prep)

These wrap the previously never-run `examples-library/` demos for ch01, ch02, ch12–ch15 (RC-2:
authored outside the tested fig pipeline). Window-create + feed commands are **byte-preserved
from the matching `examples-library/*.spin2`**; the harness only bounds the reader's infinite
`repeat` and adds `SAVE` + `DEBUG_END_SESSION`. All compile clean with `pnut-ts -d`. See
`HARDWARE-RUN-LIST-2026-07-11.md` for the bracketed batched-session run-list.

| Generator | Window | Certifies example | Evidence |
|---|---|---|---|
| `fig-01-getting-started-term.spin2` | TERM | ch01-getting-started-term | BMP |
| `fig-02-term-pin-config.spin2` | TERM | ch02-term-pin-config | BMP |
| `fig-02-term-print-value.spin2` | TERM | ch02-term-print-value | BMP |
| `fig-02-term-signals.spin2` | TERM | ch02-term-signals | BMP |
| `fig-06-logic-spi-bus.spin2` | LOGIC | ch06-logic-spi-bus (KEEP: TRIGGER + colours) | BMP (may refresh ch06 fig) |
| `fig-10-spectro-runup.spin2` | SPECTRO | ch10-spectro-runup (KEEP: LUMA8X+TRACE8) | BMP |
| `fig-12-keyboard-adjust.spin2` | TERM | ch12-keyboard-adjust | event-log (DBG_INPUT) |
| `fig-12-mouse-pointer.spin2` | TERM | ch12-mouse-pointer | event-log + visual cross-check |
| `fig-13-packed-bitmap-frame.spin2` | BITMAP | ch13-packed-bitmap-frame (LUT/LUTCOLORS) | BMP |
| `fig-13-packed-logic-stream.spin2` | LOGIC | ch13-packed-logic-stream | BMP |
| `fig-13-packed-scope.spin2` | SCOPE | ch13-packed-scope | BMP |
| `fig-14-multiwindow.spin2` | SCOPE+TERM | ch14-multiwindow | BMP |
| `fig-14-pasm-inline.spin2` | TERM | ch14-pasm-inline | BMP |
| `fig-14-pasm-scope.spin2` | SCOPE | ch14-pasm-scope | BMP |
| `fig-14-pasm-terminal.spin2` | TERM | ch14-pasm-terminal | BMP |
| `fig-14-scope-trace.spin2` | SCOPE+TERM | ch14-scope-trace | BMP |
| `fig-15-control-panel.spin2` | PLOT | ch15-control-panel | event-log + visual (Y-consistency) |
| `fig-15-dashboard.spin2` | TERM | ch15-dashboard | BMP |
| `fig-15-panel-plot.spin2` | PLOT+2 BMP LAYERs | ch15-panel-plot (LAYER/external-BMP) | BMP (needs panel_bg.bmp + digits.bmp) |

## Provenance

Command sequences are taken from the **audited** opus-master chapters (ch03–ch11),
not the pre-audit `examples-library/` demos (which use commands the content audit
flagged, e.g. `AXIS`/`GRID`/`POINT`, `CHANNELS`/`LABELS`). Every generator is
compile-certified with `pnut-ts`. Scenes are a first cut — refine against the
first real capture.
