# How We Build P2 DEBUG Displays — Claude Code + Pillow + pnut-term-ts

![Doc Type](https://img.shields.io/badge/doc-howto%20%2F%20case%20study-blue)
![Platform](https://img.shields.io/badge/platform-Propeller%202-blue)
![Technique](https://img.shields.io/badge/technique-DEBUG%20PLOT%20crop--overlay-orange)
![Maintainer](https://img.shields.io/badge/maintainer-stephen%40ironsheep.biz-blue?labelColor=black)
![License](https://img.shields.io/badge/license-MIT-green)

A reproducible account of how Claude Code and Stephen built a **graphical servo-calibration
panel** for the P2 Robot Dog — a `DEBUG(\`PLOT ...)` instrument window with live numeric readouts,
keyboard control, and real-time servo motion — and the **collaboration pattern** that made it work
even though the agent can't see a GUI. The point: *building P2 debug displays is a skill you can
hand to Claude Code.* This shows you how, end to end, so you can do it again.

> **Companion knowledge (versioned in this repo, read first):**
> [`THEORY-OF-OPERATION-crop-overlay.md`](THEORY-OF-OPERATION-crop-overlay.md) (deep dive on the
> crop-&-overlay/sprite-blit technique) and
> [`DISPLAY-PATTERNS-builders-guide.md`](DISPLAY-PATTERNS-builders-guide.md) (the reusable recipe,
> sprite patterns, and `pc_key`/`pc_mouse` input). This doc assumes those as background and focuses
> on **our** workflow, the Python tooling, and the gotchas we hit.

---

## 1. What we built

`src/test_cal_full.spin2` — a `{Spin2_v50}` PLOT window that:
- shows the **selected leg + joint** (e.g. *FRONT-LEFT · shoulder*) and its **trim value** as large
  sprite digits,
- lets you **navigate** all 13 servos (`j` = next joint, `l` = next leg) and **trim** each
  (`a`/`d` = ∓1°, `q`/`e` = ∓5°),
- drives the **real servo** live as you trim (via `isp_i2c_pca9685.gotoMicroSec`),
- **dumps the whole calibration table** to the log (`p`) so the values can be baked into firmware.

It grew from `src/test_cal_display.spin2` (increment 1 — a single joint), which we built first to
prove the pipeline. **Build small, confirm on hardware, then scale** — see §6.

---

## 2. The toolchain & the "I can't see your screen" workflow

| Tool | Role |
|------|------|
| `pnut-ts -d` | Spin2/PASM2 compiler (Iron Sheep). `-d` compiles `DEBUG()` in. Accepts `{Spin2_v50}` PLOT syntax. |
| `pnut-term-ts` | Debug terminal. **Headless** (`--headless`) for CI/agent runs; **windowed** (default) renders PLOT windows + reads keyboard/mouse. |
| **Python 3 + Pillow** | Generates the BMP artwork (backgrounds, fonts, sprite strips). |

**The key constraint and how we beat it:** the agent runs `pnut-term-ts` *headless* (no display), so
**Claude cannot see a PLOT window or send keystrokes**. But `pnut-term-ts` **mirrors every byte of
P2 output to a log file even in windowed mode** — `src/logs/debug_*.log` (relative to where you run
it). So the loop is:

```
Claude:  writes Spin2 + generates BMPs + compiles  ──▶  hands over the run command
Stephen: runs the WINDOWED terminal, sees the panel, uses the keyboard, saves with `p`
Claude:  reads src/logs/debug_*.log  ──▶  sees exactly what Stephen saw, bakes values into code
```

Claude sees everything the user sees, through the log. That single fact makes graphical,
interactive display work tractable for an agent that has no screen.

**Run commands** (note `-b 2000000` — see gotchas):
```bash
pnut-ts -d -q src/test_cal_full.spin2                         # compile (Claude)
cd src && pnut-term-ts -r test_cal_full.bin -b 2000000        # run windowed (Stephen)
```
Run from `src/` so the bare BMP filenames in `LAYER` resolve, and so the log lands in `src/logs/`.

---

## 3. Generating the artwork with Python (Pillow)

DEBUG `LAYER` requires **24-bit, uncompressed (BI_RGB), no-alpha BMP**. Pillow produces exactly that
for an `RGB` image with `img.save("x.bmp")`. Our generator is `tools/gen_cal_assets.py`.

Two sprite patterns (from the builders' guide) drive the art:
- **Font/atlas strip** (`cal_font.bmp`): one row of equal cells `0123456789-+`, 40×60 px each; a
  digit is selected by `srcX = index*40`. Unlimited numbers from one small image.
- **Word strips** (`panel_legs.bmp`, `panel_joints.bmp`): the leg names and joint names stacked as
  fixed-height cells; the active one is blitted by `srcY = index*cellH`. Changing the on-screen leg
  is "copy a different row," no text rendering on the P2.

Plus one **background** (`panel_bg.bmp`): the static frame — title, the black value box, labels, and
the key-help footer.

**The trick that keeps blind builds correct — coordinates as a single source of truth.** The Python
script defines the layout (box position, cell sizes, slot X/Y) *once*, draws the BMPs from those
numbers, **and prints a ready-to-paste Spin2 `CON` block** of the same constants. The Spin2 and the
artwork therefore can't drift. After any layout change: re-run the generator, paste the printed
`CON` values, recompile.

```bash
python3 tools/gen_cal_assets.py     # writes the .bmp files + prints the Spin2 CON layout block
```

To eyeball a BMP without a viewer, convert to PNG and look:
`python3 -c "from PIL import Image; Image.open('src/panel_bg.bmp').save('/tmp/x.png')"` — Claude can
read the PNG to verify the art rendered correctly before you ever run it.

---

## 4. The Spin2 side (DEBUG PLOT essentials we used)

- First line must be `{Spin2_v50}`.
- **Window:** `DEBUG(\`plot cal title 'P2 Servo Cal' size 480 240 pos 380 180 hidexy update)` —
  `hidexy update` = manual/double-buffered (no flicker; nothing shows until `\`cal update`).
- **Load art once:** `DEBUG(\`cal layer 1 'panel_bg.bmp')` … (layers 1–4 here).
- **Compose a frame:** erase by restoring background (`\`cal crop 1 \`(boxX,boxY,boxW,boxH)`), blit
  sprites (`\`cal crop 2 \`(srcX,0,w,h, destX,destY)`), then one `\`cal update`.
- **Input:** `DEBUG(\`cal \`pc_key(@keyCode))` — must be the **last** thing in its `DEBUG()`
  statement; returns one key (ASCII for letters). The window must have focus.
- Dynamic args use the nested backtick form `` \`(expr, expr, …) ``; constants can be written bare.

---

## 5. Gotchas we actually hit (save yourself the round-trips)

- **`-b 2000000` is mandatory on `pnut-term-ts`.** Headless opens the port at 115200 for the
  *download* (fine) but does **not** auto-apply the debug baud to the *runtime* read — without
  `-b 2000000` the 2 Mbaud `DEBUG` stream is garbage. Set `DEBUG_BAUD = 2_000_000` in the source too.
- **Use `abs(x)`, not `||x`.** pnut-ts rejects the `||` absolute-value operator ("Expected an
  expression term").
- **Use `>=` / `<=`, not `=>` / `=<`.** The `=>`/`=<` forms (seen in some P1-era examples) fail in
  pnut-ts ("Expected end of line"). (Clamp operators `#>` / `<#` are fine.)
- **BMP path resolution is relative to the terminal's working dir** — run from `src/` so bare
  `LAYER 'name.bmp'` finds the files (and the log lands in `src/logs/`).
- **Sprite cells are opaque** (no alpha): each cell must carry the right background so blits leave no
  seam — the digit/word cells use the *same* black/panel color as the box/background behind them.
- **Headless ≠ windowed.** PLOT windows and `pc_key` only work in the windowed terminal; that's why
  the human runs it and the agent reads the log.

---

## 6. The collaboration pattern (why it worked)

1. **Prove the pipeline on one element first.** Increment 1 was a single joint — it exercised every
   risky piece at once (window, BMP load, sprite blit, `pc_key`, live servo). Once that rendered and
   moved a servo on Stephen's bench, scaling to 13 joints was mostly replication.
2. **Make the agent verifiable without a screen.** Generate art → convert to PNG → Claude reads it.
   Run on hardware → Claude reads `src/logs/debug_*.log`. Every step has a text artifact the agent
   can inspect.
3. **Single source of truth for anything shared between art and code** (the layout constants).
4. **Commit each validated increment** so there's always a working restore point.

This is a repeatable skill: *describe the instrument you want; Claude designs the layout, generates
the BMPs with Pillow, writes the `{Spin2_v50}` PLOT code, and compiles; you run the windowed terminal
and report; Claude reads the log and iterates.* It works for gauges, scopes, control panels, and —
as here — hardware calibration rigs.

---

## License

MIT License - See [LICENSE](../../LICENSE) for details.

---

*Part of the Iron Sheep Productions Propeller 2 Projects Collection*

---
