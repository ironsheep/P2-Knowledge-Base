# Debug-Window Manual — Batched Hardware Run-List (§6, 2026-07-11)

**Prepared for:** one batched PNut / `pnut-term-ts` session (Stephen-gated, task #194).
**Prepared by:** Claire (task #193 PREP).
**Sprint:** fleet-release · plan `engineering/planning/FLEET-RELEASE-EXECUTION-SPRINT-PLAN-2026-07-10.md`.

> **UPDATE 2026-07-11 evening (Claire) — batch essentially DONE:** two hardware passes today
> captured everything on this list. Morning run (03:55–04:42) captured **A1–A4, A8–A14, B2**;
> evening run (18:28–19:00) captured **A5, A6, A7, B1**. **C1–C3** are certified by
> structural-vs-reference (no hardware run needed, per the directive in Part C). **One generator
> was added AFTER this list was written and is the ONLY item still to run: A15
> `fig-13-packed-logic-multi`** (row in Part A; no input-asset .bmp needed). **Conflict tests
> D1/D2 (I/J) are DONE** — run 2026-07-11 00:58–00:59 on both platforms (`img-macOS/`,
> `img-Windows/`), read back, and RESOLVED in `audit/v55-vs-REF-reconciliation-2026-07-10.md`
> (F-205b TEXTSTYLE = per-axis hybrid; POLAR θ0 = East/CCW, no flip). **Net remaining = A15
> only.** All prior figures are captured-current unless their example changes again (e.g. a
> ch05-post edit would re-open its figure).

## Why this run exists

The chapters ch01, ch02, ch12, ch13, ch14, ch15 have **no figure-generators** — their
examples were authored outside the tested `fig-*` pipeline, so they have **never run on
real hardware** (RC-2 root cause). This package wraps each of those examples in the
proven RC-2 harness (bounded run → `SAVE` → `DEBUG_END_SESSION`) so every one gains a
generator and **never ships unrun**. It also carries two KEEP re-runs (ch06, ch10), the
three interactive certifications (ch12 ×2, ch15 control-panel), and the last two dangling
conflict tests (I, J).

**Every generator compiles clean with `pnut-ts -d` (v1.55.0) and its window-create +
feed commands are byte-preserved from the matching `examples-library/*.spin2`** (the
harness only bounds the reader's infinite `repeat` and adds the capture tail). So a run
validates the *actual* example a reader sees.

## Two hard structural checks (Q4) — DONE, both PASS (no bug)

Contrasted against the hardware-proven `REF/robot-dog/test_dog_panel.spin2` (bench-confirmed
2026-06-06) and the P2KB `pc_mouse.yaml` / `pc_key.yaml`:

1. **7 consecutive longs** — `ch12-mouse-pointer` declares `mouse[7]` and
   `ch15-control-panel` declares `m[7]`: each is 7 consecutive longs
   (mx,my,mwheel,mlb,mmb,mrb,mpix), and `PC_MOUSE(@…)` is **LAST in its statement**.
   Matches the reference idiom `long mx,my,mwheel,mlb,mmb,mrb,mpix`. **PASS.**
2. **Y-flip** — the reference flips (`py := (PANEL_H-1) - py`) only when mapping a
   bottom-left/Y-up mouse coord onto **top-left BMP artwork**.
   - `ch12-mouse-pointer` is a **TERM text read-out** — it prints the reported coords, it
     does not draw a pointer onto a PLOT, so there is **no mapping to flip**. Correct as-is.
   - `ch15-control-panel` hit-tests in the **same native PLOT space** it draws in (buttons
     drawn `SET 50 70`/`SET 250 70`; `in_box` rectangles `[25,45,75,95]`/`[225,45,275,95]`
     match exactly; no external artwork), so **no flip is needed** and it is internally
     consistent. **PASS.**

Neither check found a bug. The Y-direction *consistency* between mouse-report and PLOT-draw
is confirmed on hardware by the visual cross-check below (click LEFT → value **down**).

Arrow-key codes (`1/2/3/4 = Left/Right/Up/Down`) verified against `pc_key.yaml`.

---

## Part A — Screenshot captures (non-interactive)

Compile with `pnut-ts -d <gen>.spin2`, download+run on a P2 with `pnut-term-ts`. Each
generator bounds its loop, `SAVE`s the display area (`fig-NN-*.bmp`) **and** the window+chrome
(`…_WDW.bmp`), then `DEBUG_END_SESSION` halts the run. Hand back every `.bmp`.

| # | Generator | Window(s) | Certifies example | Bracket — capture MUST show | Priority surface |
|---|-----------|-----------|-------------------|------------------------------|------------------|
| A1 | `fig-01-getting-started-term` | TERM | ch01-getting-started-term | 40×20 window, text `Ready.` top-left | — |
| A2 | `fig-02-term-pin-config` | TERM | ch02-term-pin-config | 30×5 window, `Ready.` line | — |
| A3 | `fig-02-term-print-value` | TERM | ch02-term-print-value | `Reading: 42` | — |
| A4 | `fig-02-term-signals` | TERM | ch02-term-signals | line 1 `wave=… noise=…` (last frame) | — |
| A5 | `fig-13-packed-bitmap-frame` | BITMAP | ch13-packed-bitmap-frame | 32×16 @ DOTSIZE 8, **cyan diagonal stripes on black** (LUT1 + LUTCOLORS) | **LUT/LUTCOLORS** |
| A6 | `fig-13-packed-logic-stream` | LOGIC | ch13-packed-logic-stream | single 1-bit trace `D0`, random hi/lo | — |
| A7 | `fig-13-packed-scope` | SCOPE | ch13-packed-scope | ramp-ish 8-bit samples; **window exists** (RC-2 create-line fix) | — |
| A8 | `fig-14-multiwindow` | SCOPE + TERM | ch14-multiwindow | left SCOPE sine + right TERM `Sample …/Value …` | — |
| A9 | `fig-14-pasm-inline` | TERM | ch14-pasm-inline | `x = 12` (bounded to 12 inline-PASM iterations) | — |
| A10 | `fig-14-pasm-scope` | SCOPE | ch14-pasm-scope | ramp 0–255 fed from a **PASM cog** (RC-2 create-line) | — |
| A11 | `fig-14-pasm-terminal` | TERM | ch14-pasm-terminal | `count = ….` (hex) fed from a PASM cog | — |
| A12 | `fig-14-scope-trace` | SCOPE + TERM | ch14-scope-trace | left SCOPE sine + right TERM `Samples/Current/Peak` | — |
| A13 | `fig-15-dashboard` | TERM | ch15-dashboard | fixed-field `RPM/Temp/Volts` block, values updating | — |
| A14 | `fig-15-panel-plot` | PLOT + 2 BMP LAYERs | ch15-panel-plot | frame bg + **3-digit reading blitted from the font strip** | **LAYER/external-BMP** |
| A15 | `fig-13-packed-logic-multi` | LOGIC | ch13-packed-logic-multi | **two** 1-bit traces `D0` **and** `D1`, both random hi/lo (pre-fix bug drew everything on D0) | **mode↔channel, F-207 B** |

**Assets required in the run directory** for A14: `panel_bg.bmp` + `digits.bmp`
(both live in `examples-library/` — copy them alongside the generator before running).

## Part B — KEEP re-runs (divergences Stephen elected to keep)

| # | Generator | Window | Bracket — MUST show | Then |
|---|-----------|--------|----------------------|------|
| B1 | `fig-06-logic-spi-bus` | LOGIC | **TRIGGER-aligned** SPI frames, **named colours** CS=cyan / CLK=green / MOSI=yellow (not the free-run `fig-06-logic`) | if good, refresh the manual's **ch06 LOGIC figure** to this capture (file↔code-block parity kept) |
| B2 | `fig-10-spectro-runup` | SPECTRO | rising **diagonal streak**, `RANGE 500` + `TRACE 8` + **LUMA8X** palette actually renders (not blank — the $40000 bug is already reverted) | promote/deny the KEEP of LUMA8X+TRACE8 vs `fig-10`'s LUMA8W BLUE |

> B1 supersedes the free-run `fig-06-logic.spin2` **only if** the triggered capture is
> accepted; both are kept side-by-side until then.

## Part C — Interactive certifications (event-log, no screenshot)

These poll `PC_KEY` / `PC_MOUSE`, so they can't be screenshotted. Each enables the
channel-gated `DEBUG[DBG_INPUT]` log (`DEBUG_MASK = 1<<DBG_INPUT`) so the run emits a
re-readable record Claire reads back. **Evidence = structural-vs-reference (done) +
event-log + visual position cross-check.** Drive each as noted; hand back the `DBG_INPUT`
log text.

| # | Generator | Drive it | Event-log MUST show | Visual cross-check | Ends on |
|---|-----------|----------|----------------------|--------------------|---------|
| C1 | `fig-12-keyboard-adjust` | press ↑ ↓ ← → a few times | `KEY code=3 value=51`, `code=4 …`, `code=1 …`, `code=2 …` (codes 3/4/1/2 = U/D/L/R; value moves ±1 / ±10) | on-screen `Value:` matches the logged value | Esc |
| C2 | `fig-12-mouse-pointer` | move mouse, **left-click** in the window, then **right-click** to end | `CLICK x=… y=… pix=…` per left-press | drawn `X:/Y:` text equals the logged `x/y`; `pix` = colour under cursor | right-click |
| C3 | `fig-15-control-panel` | click the **LEFT** (minus) button, then the **RIGHT** (plus) button; also press ← → | `CLICK MINUS x=… y=…` **then value goes DOWN**; `CLICK PLUS …` **then value UP**; `KEY Left/Right` | the value bar shrinks on minus-click / grows on plus-click **and** the click coord lands inside the drawn button — this is the Y-consistency proof | Esc |

> **C3 is the decisive Y-consistency test.** If clicking the LEFT button *raises* value (or
> the coord doesn't land in the drawn button), that is a real bottom-left/top-left
> mouse-vs-draw inversion — **stop and fix**, don't certify. (Structural analysis says it is
> consistent; this run confirms it.)

### Structural-vs-reference certification — COMPLETE (2026-07-11, Claire, task #194)

**Stephen's directive (2026-07-11):** the interactive examples do **NOT** need a hardware
run — the bench-certified `REF/robot-dog/test_dog_panel.spin2` certifies the PC_KEY/PC_MOUSE
idioms; certification = **structural contrast** against it (recode only where they diverge).

Contrast performed against the reference's four pinned idioms — (1) pc_mouse = 7 consecutive
longs, (2) poll LAST-in-statement, (3) press-edge detect, (4) flip py **only** when mapping a
bottom-left/Y-up mouse coord onto **top-left BMP artwork**. Result **PASS on all three; no
divergence found → no recode**:

| Example | 7 longs / last-in-stmt | edge-detect | Y handling | Verdict |
|---------|------------------------|-------------|------------|---------|
| `ch12-keyboard-adjust` | `PC_KEY(@key)` last-in-stmt (key-only) | fresh-key (`key:=0` per poll) | n/a (TERM, no draw) | ✅ conforms |
| `ch12-mouse-pointer` | `mouse[7]`, `PC_MOUSE(@mouse)` last-in-stmt | n/a (state read-out) | TERM prints RAW coords — no artwork to map → correctly NO flip | ✅ conforms |
| `ch15-control-panel` | `m[7]`, both `PC_KEY`/`PC_MOUSE` last-in-stmt | `if m[3] and not lastL` + `lastL := m[3]` | draws + hit-tests in ONE native PLOT frame; **no CARTESIAN flip** → correctly NO py-flip | ✅ conforms |

**Grounding for the "no flip" verdict (the Q4 bug-risk):** `plot.yaml:84` —
`cursor_coordinate: "pixel / DOTSIZE, honoring CARTESIAN flip flags (vDirX/vDirY)"`. PC_MOUSE
reports in the **same** coordinate frame the drawing primitives use, so a PLOT example that
draws its own buttons (no external top-left BMP) hit-tests coord-consistently **without** a
flip. The reference needs `py := (PANEL_H-1) - py` only because its layout is a **top-left
BMP blitted via `crop`** — a frame the PLOT-native mouse coord does not share. ch15 has no
such external artwork, so the flip would be a *bug to introduce*, not one to fix.

**Evidence type: structural-vs-reference (COMPLETE).** The event-log + visual-cross-check
paths (C1–C3 above) remain available as optional belt-and-suspenders if Stephen later elects
a confirming bench run, but are **not required** for certification per the directive.

## Part D — Conflict tests I + J (last two dangling source conflicts)

Already authored + compiled (`audit/verification-tests/`). Bracketed/self-checking.

| # | Test | Emits | Settles | Read (image-tools) |
|---|------|-------|---------|--------------------|
| D1 | `conflict-testI-textstyle-justify.spin2` | `textI_horiz.bmp`, `textI_vert.bmp` | F-205b — TEXTSTYLE %XX/%YY value→direction (v55 text vs REF, inverted) | control row `$00` MUST straddle the guide-line; then which side value `%10` lands → REF (2=left/top) or v55 (2=right/bottom); `2` vs `3` MUST be opposite sides else INCONCLUSIVE |
| D2 | `conflict-testJ-polar-theta0.spin2` | `polarJ_wheel.bmp` | POLAR θ0 direction + rotation sense (ch05 flip risk) | cross-check against `fig-05` gauge orientation |

Claire promotes I/J results to ground truth in
`audit/v55-vs-REF-reconciliation-2026-07-10.md`, closing F-205 and the ch05 POLAR flip-risk.

---

## Read-back & promotion (Claire, task #194)

For each item: read the `.bmp`/log via `image-tools-mcp`, check it against the bracket above,
and certify with its **evidence type** (BMP-captured / event-log / structural-vs-reference /
visual cross-check). Promote Test I/J to ground truth; refresh ch06 (B1) and dispose ch10
(B2) per Stephen. A bracket miss on an interactive item (esp. C3) is a **real bug → fix now**,
never certify.

## Reference (external, NOT committed)

`REF/robot-dog/` (production 3-cog interactive panel, bench-confirmed 2026-06-06) is the
structural anchor for the interactive idioms. It is cited as external material and is **not**
part of the committed tree.
