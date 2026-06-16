# DEBUG Window Manual — Example Pedagogy & Domain-Grounding Plan

**Created:** 2026-06-15
**Head:** manual:p2-debug-window-manual
**Goal:** Complete the first draft by making every window chapter's example
(a) **worth the reader's time** and (b) **domain-grounded** — telling the reader
*where they'd actually use this window*, including embedded-specific uses — while
staying **honest about what the 2 Mbaud debug link can really carry.**

This plan is approved in principle (Stephen, 2026-06-15). Execute after the plan
is reviewed; do **no** edits until then.

---

## 1. The two pedagogical lenses (the audit criteria)

Every window example is judged against:

1. **Practical worthiness** — does it demonstrate something a developer would
   *actually do* on a real project, not just "make the window light up"?
2. **Domain breadth** — beyond the general signal-analysis demo, *which CS /
   computer-engineering areas* use this window, and — since this is an **embedded**
   toolchain — *what embedded-specific information* would a developer display here?

**Decisions locked in:**

- **Keep synthetic data. No hardware required.** Every example must still run with
  nothing wired up.
- **Name what the synthetic data stands in for** (e.g. "this `qsin` stands in for
  an ADC stream / a vibrating motor / a thermal field").
- **Apply one consistent pattern to every window chapter** (§4).
- **Do the example rewrites** (§5) even though the data is simulated — they must
  *show something useful and describe how you'd use it*.

**Scaffolding that already exists (build on, don't reinvent):**
- **ch01 "A note on high data rates"** — the link-budget seed (names only packing
  today; §2/§3 expand it).
- **ch01 "Which window for which problem"** — book-level data-shape → window selector
  (the per-chapter "Where you'd use this" blocks sit at a deeper altitude beneath it).
- **ch02 "The no-hardware philosophy"** — already establishes synthetic-data style,
  the "stands in for" voice, and the "optional real-hardware note after the
  software-only version" convention (§4 aligns to these).

---

## 2. The grounding in reality: the link is the budget

**Budget:** 2 Mbaud, 8N1 framing ≈ 10 bits/byte → **~200 KB/s raw**, and after
DEBUG command/formatting overhead realistically **~100–150 KB/s of payload.**
Every sample, pixel, and value displayed crosses that wire. This sorts uses into
three regimes:

| Regime | Fits the link? | Where it applies |
|--------|----------------|------------------|
| **Low-rate live** (sensors at Hz–low-kHz, status, UI) | ✅ Comfortably | TERM, PLOT, MIDI, keyboard/mouse, panels; small/slow sensor grids |
| **Software-paced / event** (one sample per edge/event) | ✅ Yes | LOGIC bit-bang verification; packed bursts |
| **Buffered burst** (capture fast in PASM, dump slow) | ✅ Yes (one-shot) | SCOPE/LOGIC triggered single-shot; FFT/SPECTRO blocks |
| **Live high-bandwidth stream** (video, full-rate ADC/RF/audio) | ❌ **No** | stripped from the suggestions below |

**The bandwidth callout expands the EXISTING ch01 "A note on high data rates"
section** (which today names only packing) and is cross-referenced from ch13
(packing) and the SCOPE/LOGIC acquisition notes (§3):

> *The link is the budget. These windows are for low-rate live signals,
> software-paced events, and buffered bursts — not live video or full-rate
> streams. Packing (Ch 13) buys headroom, not an order of magnitude.*

### What the budget strips or tempers

- **BITMAP** — live *camera video* is **out** (a 320×240 RGB frame ≈ 230 KB → <1 fps).
  A **thermal-array heatmap is a *better* fit than the current plasma demo** (an 8×8
  or 32×24 grid at a few Hz is kilobytes/sec). Make that contrast an explicit point.
- **LOGIC** — live monitoring of a *fast* bus is **out**; reframed as **software-paced
  protocol bring-up** and **triggered burst capture** (§3).
- **SCOPE** — live high-rate analog is **out**; kept as **low-rate sensor streaming**
  + **triggered single-shot capture** (§3).
- **SCOPE_XY** — full-rate I/Q constellation is **out**; kept as **decimated/low-rate**
  encoder-XY, tilt, slow phase-plane.
- **FFT** — **audio (44.1 kHz) live is tempered** (buffered/decimated only);
  **vibration (sub-10 kHz) and power-line harmonics (50/60 Hz sampled at a few kHz)
  are the headline fits** — low sample rate is exactly what the link wants.
- **SPECTRO** — full **RF / music is out**; kept as **vibration trending and motor
  run-up** (low rate, long duration = ideal), plus narrowband/voice.
- **TERM / PLOT / MIDI / keyboard-mouse / panels** — all low-rate, **no tempering**.

---

## 3. T&M acquisition strategies: matching a fast signal to a slow link

Live monitoring being "out" is the *setup* for the two strategies every bench DSO
and logic analyzer actually uses. Both are **fully synthetic / no-hardware** to teach.

**Technique 1 — Decimate to watch a trend (continuous, lossy).**
Push 1-in-N samples for a live, always-updating view of a slowly-evolving signal.
T&M-correct nuance: naive "every Nth sample" **aliases and drops narrow glitches**;
the honest form is **min/max (peak) decimation** — per display bucket keep the min
*and* max sample so a one-cycle spike still paints. (Optionally a boxcar/CIC
pre-average for measurement-grade decimation.) This is bench-scope roll mode.

**Technique 2 — Capture-until-trigger to catch an event (one-shot, full fidelity).**
A tight PASM loop fills a **circular buffer at full sample rate**, continuously,
while testing a trigger condition (level crossing, bus pattern, out-of-range fault).
On fire, **freeze and dump the pre-trigger + post-trigger window once** over the
slow link. Key point to state plainly: **capture fidelity is bounded by P2 loop
speed and buffer depth, not by the link** — the link only carries the readout.
This is arm → acquire → trigger → freeze → readout (the DSO model).

**The honest tradeoff (put it in the reader's hands):** decimation is always-on but
can alias/miss (mitigate with min/max); capture-til-trigger is perfect detail but
you see one window per trigger and are blind between events. **Choose by whether
you're watching a *trend* or hunting an *event*.**

**Placement — layered home (decided 2026-06-15; teach concept in the overview,
technique at the point of need, once):**
- **ch01 "A note on high data rates"** (EXISTS — currently names only packing) —
  **expand** it to name all three link-budget strategies in a sentence each
  (**pack / decimate / capture-and-dump**) with pointers: packing → ch13,
  decimate + capture-til-trigger → ch07. Keeps foundation light; plants the concept.
- **ch07 SCOPE — the canonical deep-dive home.** It already owns triggering most
  fully (arm/fire, trigger position, holdoff, pre-trigger) and hosts the worked
  glitch-capture example (§6). The **full capture-til-trigger + decimation treatment
  lives here, once.** Decimation is taught as a **short snippet + contrast** (Q4),
  not a second full example: *"take every 8th sample and a one-cycle spike vanishes;
  keep the min* and *max of each group of 8 and it survives."* Recast the existing
  triggered example as "**capture a one-shot event**," noting the trigger/buffer live
  in the PASM loop, decoupled from the link.
- **ch06 LOGIC — its logic-specific slice only:** software-paced "one sample per
  edge" + the LA-classic **transition/timestamp capture** (store edges + timestamps,
  not every sample clock; packs via ch13), with a **pointer to ch07** for the shared
  buffer/trigger mechanics. (ch06 precedes ch07, so the forward-ref is explicit; the
  logic-local content stands on its own.)
- **FFT/SPECTRO** — one-line pointers: feed **decimated** or **buffered blocks**,
  not a live full-rate stream (see Ch 7).
- **Signal generation** (stimulus side) — short note in SCOPE/SPECTRO: the P2
  generates the stimulus (DAC / NCO / PWM smart pins); **sweep/generate slowly so
  the displayed response keeps step** (the SPECTRO motor-runup *is* a slow generated
  sweep), or generate a stimulus and arm a capture on the response.

> **NOT a dedicated new section/chapter.** Earlier draft proposed homing this in
> ch02; superseded — the concept already has a home (ch01) and the technique already
> has a home (ch07 triggering). Adding a section would duplicate triggering material.

---

## 4. The consistent pattern (applied to every window chapter)

For each window chapter, add a short, uniform **"Where you'd use this"** block:

```
### Where you'd use this

<2 CS / computer-engineering areas — one sentence each>

**On an embedded project:** <tight list of embedded-specific displays>

**Bandwidth fit:** <one line: which regime from §2 this lives in>

**Extension (real hardware):** <one line on swapping the synthetic source for a
real sensor/ADC/pin>
```

**Position (decided 2026-06-15):** place the block **end-of-chapter, after the
worked example, immediately before "## Considerations."** The learning arc is
*example (concrete) → where you'd use it (transfer) → considerations (caveats, incl.
the bandwidth-fit line) → try it (practice).* Domain breadth lands better after the
reader has seen the window work; ch01's "Which window for which problem" selector
already handles up-front "which window," so the per-chapter block stays at a deeper
altitude (CS areas + embedded specifics + fit + hardware extension) and complements
that table rather than echoing it.

**Align to existing house conventions (ch02 "no-hardware philosophy"):**
- The **"stands in for"** framing is already manual style ("a generated signal drives
  a window exactly the way a real sensor would") — match its voice, don't reinvent.
- The **"Extension (real hardware)"** line is already the documented convention
  ("a real-hardware version goes as a short optional note *after* the software-only
  version") — the block formalizes it uniformly; ch09 already models it.

Plus, in the example prose: one line naming **what the synthetic data stands in for.**
Keep the runnable synthetic example as-is unless listed for rewrite in §6.

---

## 5. Per-window audit & content (tempered)

Verdicts from the 2026-06-15 fan-out audit. "Change effort" drives execution order.

| Ch | Window | Example today | Practical verdict | Effort |
|----|--------|---------------|-------------------|--------|
| 03 | TERM | Status dashboard, synthetic sine + threshold | Good — real status-panel pattern | Light |
| 04 | BITMAP | Plasma animation (synthetic) | Weak — prettiest, least grounded | **Rewrite** |
| 05 | PLOT | Sine+scatter; analog gauge | Mixed — gauge worthy, scatter decorative | **Rewrite (add)** |
| 06 | LOGIC | Software SPI bus | Good — models a real protocol | Light + §3 note |
| 07 | SCOPE | 3 synthetic waves + triggered capture | Good framing | **Rewrite (add)** + §3 |
| 08 | SCOPE_XY | Lissajous (synthetic) | Framing present, uses implied | Medium |
| 09 | FFT | 3-tone + noise; has "When to use" + HW pointer | Best mechanics; domain naming thin | Medium |
| 10 | SPECTRO | Chirp sweep (synthetic) | Weak — abstract chirp demo | **Rewrite** |
| 11 | MIDI | Scale + chord (hardcoded) | Narrow/novelty — honest niche | Special |
| 12 | Keyboard/Mouse | Arrow-key tuner; mouse state (real data) | Strong — HIL tuning | Light |
| 13 | Packed data | Synthetic — a technique chapter | Appropriate toolkit | Light |
| 15 | Panels | Live dashboard/gauge/control panel (real) | Strongest — production craft | Light |

### Domain content to add (the "Where you'd use this" substance)

- **TERM** — *CS:* systems telemetry/observability; transaction logging.
  *Embedded:* per-cog load, stack high-water marks, live peripheral-register
  inspector, boot/POST status, fault counters, state-machine current-state.
- **BITMAP** — *CS:* computer vision / framebuffer viz; 2D scalar-field viz.
  *Embedded:* thermal-array heatmap (MLX90640-class), LED-matrix framebuffer
  preview, cap-touch grid, RSSI/occupancy map. *Fit:* small/slow grids ✅; live
  camera video ❌.
- **PLOT** — *CS:* control systems; instrumentation/data-viz.
  *Embedded:* PID strip-chart (setpoint/PV/output), battery charge curve,
  calibration plot (raw ADC vs engineering units), servo/RPM dials. *Fit:* low-rate ✅.
- **LOGIC** — *CS:* protocol engineering; concurrent-systems debugging.
  *Embedded:* bit-banged-driver bring-up (verify CPOL/CPHA), chip-select/arbitration
  timing, inter-cog lock/signal timing, datasheet setup/hold checks. *Fit:*
  software-paced ✅; buffered burst ✅; live fast bus ❌. + §3 transition/timestamp note.
- **SCOPE** — *CS:* DSP waveform/filter inspection; control & power electronics.
  *Embedded:* ADC capture, PWM edge/duty, supply ripple/inrush (triggered one-shot),
  contact-bounce capture, fault-line glitch capture. *Fit:* low-rate live ✅; triggered
  burst ✅; high-rate live ❌. + §3 acquisition note.
- **SCOPE_XY** — *CS:* I/Q constellations (QAM/PSK); phase-plane/dynamical systems.
  *Embedded:* quadrature encoder A/B as XY (smart-pin), motor d-q/FOC vectors,
  PLL lock (ellipse→line), accelerometer X-Y tilt. *Fit:* decimated/low-rate ✅;
  full-rate I/Q ❌. Add encoder-XY as a named use.
- **FFT** — *CS:* audio/DSP (THD/harmonics); condition monitoring.
  *Embedded:* motor bearing-fault vibration FFT, power-line harmonic/THD, EMI
  noise-source hunting, resonance ID; audio spectrum (buffered/decimated). *Fit:*
  vibration & harmonics ✅; live audio tempered. Say what the three tones *represent*.
- **SPECTRO** — *CS:* RF/comms spectral monitoring (narrowband); acoustics/speech.
  *Embedded:* machine-health vibration trending, motor run-up/coast-down resonance
  crossings, narrowband/voice. *Fit:* low-rate long-duration ✅; full RF/music ❌.
- **MIDI** — honestly just music tech / MIDI-protocol debugging. *Embedded:*
  synth/sequencer-engine debugging, controller note-output verification, generative
  music viz. **Do not inflate.** Add one honest line: "If you're not building MIDI
  software, reach for TERM/PLOT/LOGIC instead."
- **Keyboard/Mouse (ch12)** — human-in-the-loop tuning, interactive parameter
  adjustment, manual test rigs. *Embedded:* live PID-gain tuning, setpoint nudging,
  actuator jog, calibration capture. Light touch — already strong.
- **Packed data (ch13)** — frame motivation with a concrete "capturing a high-rate
  burst that would saturate the link" scenario; it's the headroom mechanism §2/§3
  lean on. Cross-reference both ways.
- **Panels (ch15)** — live dashboards, control/tuning panels, HIL. Already strong;
  light touch.

---

## 6. Two code sets that ride with this work

Every example exists in **two forms** with different tails. The work in §5/§6
produces/updates both:

| Set | Folder | Tail | Purpose | Regenerated |
|-----|--------|------|---------|-------------|
| **Figure-generators** | `figure-generators/` | **save + close** (capture tail: save / save-window / `` `CLOSE `` / `DEBUG_END_SESSION`) | Stephen runs in PNut to produce the `_WDW` BMPs (ground truth) | **Only the ones whose figure changes or is new** |
| **Examples-library** | `examples-library/` | **trailing `repeat`** (keep window open), **no save/close** | The reader-facing code that ships with the manual (the ZIP) | **Wholesale — the complete set, replacing every file in the folder** |

**Rules:**
- A figure-generator and its library twin share the *same body*; they differ
  **only in the tail** (save+close vs. `repeat`). Keep them in lockstep.
- The **examples-library is regenerated as a complete replace-all set** so the
  shipped code matches the final manual exactly — not a patch of the changed files.
  Re-export every chapter example (repeat-terminated, no save/close) and replace the
  folder's contents.
- A figure-generator is (re)written **only** when its figure actually changes or is
  new (see per-rewrite "Changes/Adds fig-NN"). Don't touch generators for unchanged
  figures (PDF-Forge/figure persistence — only changed sources move).
- Both sets **compile `pnut-ts -d` clean** before they land.

### The four example rewrites (synthetic)

Each touches the **library** entry (always) and a **generator** (only if its figure
changes/adds), per the table above.

1. **BITMAP (ch04): plasma → thermal-array heatmap.** Synthetic moving "hot spot"
   standing in for a **32×24 thermopile array (MLX90640-class)** at a few Hz, rendered
   with HSV/LUMA magnitude→color. *Use:* IR presence/people-sensing, PCB hot-spot
   detection, thermal monitoring. *Fit note:* small grid + low refresh comfortable;
   full camera video not. **Changes `fig-04`.**

2. **SPECTRO (ch10): chirp → motor spin-up / vibration waterfall.** Same synthetic
   swept tone reframed as a **motor's shaft speed rising during run-up** — the diagonal
   streak is increasing rotation/vibration frequency. *Use:* bearing-fault band
   trending, resonance crossings during run-up/coast-down, machine-health monitoring.
   *Fit note:* vibration is sub-10 kHz, long duration — ideal. **Changes `fig-10`.**

3. **PLOT (ch05): add a PID control-loop strip chart.** Synthetic setpoint + simulated
   first-order process variable (lag response to the controller output) + controller
   output = three live traces. Stands in for **tuning a real control loop**. *Use:*
   watch setpoint vs PV to tune P/I/D gains; settling/overshoot inspection. *Fit note:*
   observed at ~50–200 Hz on screen — trivial. Keep the analog-gauge example; reframe
   the sine+scatter as primitive-teaching. **Adds a new figure** (the strip-chart's
   payload *is* the visual — setpoint/PV convergence, overshoot, settling).

4. **SCOPE (ch07): add a "capture a rare glitch" example.** Fully synthetic: generate
   a clean signal that *occasionally* throws an out-of-range spike; run a capture loop
   until the trigger fires; freeze and display the pre/post-trigger window. Demonstrates
   §3 Technique 2 end-to-end with no hardware. *Use:* catching intermittent faults,
   one-shot transients. **Adds a new figure** (the anomaly frozen at the trigger point
   with pre/post context is the payoff). This is the **only worked acquisition example**;
   decimation stays a short snippet + contrast in prose (Q4), no separate example/figure.

**LOGIC (ch06):** no full rewrite — add the §3 note + transition/timestamp framing in
prose; existing SPI example stays.

---

## 7. Execution order

1. **(this doc)** Plan reviewed & approved.
2. **ch01** — expand the existing "A note on high data rates" to name all three
   link-budget strategies (pack / decimate / capture-and-dump) with pointers (§2/§3).
3. **ch06 LOGIC + ch07 SCOPE** — the acquisition teaching (§3 layered home): ch07 gets
   the full capture-til-trigger treatment + decimation snippet/contrast; ch06 gets its
   logic-specific slice (software-paced + transition/timestamp) + pointer to ch07.
4. **ch03–15** — add the "Where you'd use this" blocks (§4), positioned end-of-chapter
   before "Considerations," + "stands in for" framing. Light chapters first
   (03, 06, 11, 12, 13, 15), then medium (08, 09).
5. **Rewrites** (§6) in effort order: BITMAP, SPECTRO, then PLOT add, then SCOPE
   glitch-capture. Each: write synthetic code → **compile `pnut-ts -d` clean** →
   write/update the **figure-generator** twin (save+close) for any figure that
   changes or is new → reassemble the manual via `assemble-manual.sh`.
6. **Regenerate the examples-library wholesale** — once chapters are final, re-export
   the **complete** set of per-chapter examples (trailing `repeat`, no save/close),
   **replacing every file** in `examples-library/`, so the shipped code == final
   manual. Verify all compile `pnut-ts -d` clean. This is the code set that rides
   along in the manual's ZIP.
7. **Figure impact — four changed/new figures** need PNut capture: `fig-04` (BITMAP
   heatmap, changed), `fig-10` (SPECTRO motor run-up, changed), **new** PID strip-chart,
   **new** glitch-capture. Their **figure-generators** (save+close) are what Stephen
   runs. **This dovetails with the open figure work (task #56)** — fold into one capture
   pass with the four already pending there (fig-03, fig-06, fig-09, fig-11).
8. **Verify** — both code sets compile `-d` clean; chapters read consistently;
   bandwidth claims internally consistent.

### Handoff (who does what)

1. **I produce:** revised chapters + reassembled manual; the **figure-generators**
   (save+close) for every changed/new figure; the **complete examples-library**
   (repeat, no save/close), replace-all.
2. **Stephen:** regenerates **all** images by running the figure-generators in PNut
   (ground truth), brings the `_WDW` BMPs back.
3. **I:** reconvert BMP→PNG into `assets/`, reassemble the manual (task #56 closes,
   `prepare-manual` task #59), one Forge PDF pass.
4. **Stephen:** assembles the **ZIP** (the examples-library code that rides with the
   manual). *I do not build the ZIP.*

## 8. Guardrails

- All new code **compiles `pnut-ts -d` clean** before it lands (DEBUG directive
  contents are only checked with `-d`).
- Synthetic-only; no hardware; name what each stands in for.
- Code constants over arithmetic; single-quote display strings (golden idiom).
- Back up `P2-Debug-Window-Manual.md` before bulk edits; edit opus-master chapters
  and reassemble — never hand-edit the assembled file.
- **Two code sets, different tails (§6):** figure-generators carry save+close;
  examples-library carries trailing `repeat`, no save/close. A generator and its
  library twin share the same body. Generators (re)written only for changed/new
  figures; examples-library regenerated wholesale (replace-all).
- Don't over-claim MIDI; keep the honest-niche framing.

## 9. Decisions recorded (Stephen, 2026-06-15)

- Keep synthetic / no hardware. ✅
- Name what data stands in for. ✅
- Consistent pattern across all chapters. ✅
- Do all four example rewrites (incl. SCOPE glitch-capture). ✅
- Add the T&M acquisition-strategy teaching (decimation + capture-til-trigger) for
  LOGIC, SCOPE, and signal generation. ✅
- Bandwidth tempering of the domain suggestions accepted as written. ✅

**Four pedagogy questions resolved (Stephen delegated the calls; 2026-06-15):**
- **Q1 (figures for added examples):** both the PLOT PID strip-chart and the SCOPE
  glitch-capture **get figures** — the visual *is* the lesson in each. Total
  changed/new figures = **4** (fig-04, fig-10, PID, glitch). ✅
- **Q2 (home of bandwidth/acquisition teaching):** **layered, not a new section** —
  concept expands the existing **ch01** "A note on high data rates"; full technique
  lives in **ch07 SCOPE** (canonical triggering home); **ch06 LOGIC** carries its
  logic-specific slice + pointer to ch07. Supersedes the earlier "home it in ch02." ✅
- **Q3 (position of "Where you'd use this" block):** **end-of-chapter, after the
  worked example, before "Considerations"** (concrete → transfer → caveats → practice);
  aligns to existing ch02 house conventions for "stands in for" + hardware-extension. ✅
- **Q4 (decimation code vs text):** capture-til-trigger is the one worked acquisition
  example; **decimation stays a short snippet + min/max contrast in prose**, no
  separate example or figure. ✅
- **Two code sets ride with this work (§6):** figure-generators (save+close) for
  regenerating changed/new figures; examples-library (repeat, no save/close)
  regenerated **wholesale, replace-all** as the code that ships in the manual ZIP. ✅
- **Handoff (§7):** I produce both code sets + reassembled manual; Stephen regenerates
  all images in PNut; I reconvert + assemble the manual; **Stephen builds the ZIP**
  (not me). ✅

---

## 10. Section ↔ task cross-reference (tag: `dw-examples`)

Generated by `plan-to-tasks` 2026-06-15. Execution order is `seq` (walk with
`todo_next tags:["dw-examples"]`). Hands off to existing `«#59»` (prepare-manual)
after `«#68»`.

| Plan § | Deliverable | Task | seq | est |
| ------ | ----------- | ---- | --- | --- |
| §7.2 | ch01 — expand "A note on high data rates" → link-budget + 3 strategies | «#60» | 3 | 30m |
| §7.3 / §3 / §6.4 | ch06+ch07 acquisition teaching + SCOPE glitch-capture example + both "Where you'd use this" blocks | «#61» | 4 | 2h30 |
| §7.5 / §6.1 | ch04 BITMAP rewrite → thermal-array heatmap (+gen fig-04, +block) | «#62» | 5 | 1h30 |
| §7.5 / §6.2 | ch10 SPECTRO reframe → motor spin-up (+gen fig-10, +block) | «#63» | 6 | 1h |
| §7.5 / §6.3 | ch05 PLOT add PID strip-chart (+new gen, +block) | «#64» | 7 | 1h30 |
| §7.4 / §4 | "Where you'd use this" blocks — ch03,08,09,11,12,13,15 + framing | «#65» | 8 | 2h |
| §7.6 | examples-library wholesale replace-all regen (ZIP code) | «#66» | 9 | 1h |
| §7.7 | figure capture/reconvert gate (4 new/changed; consolidates with #56) | «#67» | 10 | 45m |
| §7.8 | final consistency verify gate → hands to #59 | «#68» | 11 | 45m |

**Sprint tag:** `dw-examples` (distinct from `debug-window` / `figures`).
**Entry baseline (MANUAL sprint):** the manual's current first-draft document/audit
state — no local compile gate (renders on PDF Forge). Exit no-regression compares
against that state.
