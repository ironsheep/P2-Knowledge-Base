# Study — "Improved ADC Pin Techniques" forum thread

**Source thread:** https://forums.parallax.com/discussion/175609/improved-adc-pin-techniques (4 pages, 2023-11-27 → 2024-04-07)
**Local capture:** `thread-p1.md … thread-p4.md` (verbatim posts) + `code/` (7 attachments, verbatim) + `P2_ADC_Schematic.pdf`
**Studied:** 2026-06-27 for P2AN001 (P2 instrumentation-ADC app note)
**Authority note:** **cgracey = Chip Gracey, the P2 silicon designer.** His statements about *why the ADC behaves as it does* and *its design limits* are near-authoritative (he designed the analog front end). Empirical performance numbers he quotes are bench results from his own rig — strong, but rig-specific, not datasheet guarantees. Everything here must still be re-derived/verified against P2 silicon + `pnut_ts` before it enters the note (trust chain).

---

## 1. Speaker credibility map (who to weight)

| Participant | Role / signal | How to weight |
|---|---|---|
| **cgracey** | **P2 silicon designer.** Drove this entire investigation; posted all the core code. | **Authoritative on design intent & limits.** His "why" explanations are ground truth; his perf numbers are credible bench results. |
| **evanh** | Long-time P2 ADC experimenter; deep on the SINC/decimation behavior; released characterization data. | **High.** Corroborates and adds precise mechanism detail (decimation/settling, real resistor values >500 kΩ). |
| **Tubular** | Did early "glob top" ADC characterization (temperature, per-pin VIO/GIO spread). | **High** on empirical pin-to-pin/temperature behavior. |
| **TonyB_** | Sharp on the scope-mode windowing (Hann/Tukey overlap to raise ENOB). | **High** but a *different* sub-topic (GETSCP scope path, not the smart-pin SINC ADC). |
| **Christof Eb.** | Pushes for a rigorous, dependable spec (ENOB definition, single-pin, temp range). | **Useful framing** — represents the end-user's "what do I actually get" question. |
| **SaucySoliton** | Built a trapezoid-window SINC3 variant; motor-driver use case. | **Medium-high** — credible working alternative; verify independently. |
| **jmg** | Tempco-matching caution on external resistors. | **Medium** — correct, narrow point. |
| Rayman, iseries, Maciek, rogloh, ManAtWork, ErNa, HydraHacker, others | Application questions, motor theory, anecdotes. | **Context only** — use for "what people want to build," not technique. |

---

## 2. AXIS A — Driving the chip (how the P2 ADC actually behaves + its limits)

These are facts about the silicon. The strongest material for the note's "How It Works" section.

### A1. The ADC front end (from Chip + evanh + the schematic)
- The smart-pin ADC is a **sigma-delta modulator**: input current (through an on-chip resistor from the pin) is balanced against a feedback current to hold the modulator node near **VIO/2**. The pin **self-biases near VIO/2** (not exactly). [cgracey p3.9, Rayman p3.5, evanh p3.6]
- **Input impedance ≈ 500 kΩ+** on the x1 range (evanh: "real x1 resistors are over 500 kOhms"; Chip's "≈430 kΩ" combined-3-pin figure is the same ballpark). High-Z source → expect loading error with low-impedance sensors. [evanh p3.8, cgracey p1.14]
- Modulator caps ≈ **7 pF** total (PMOS+NMOS sets), designed to run at 200 MHz. [cgracey p3.3]
- **Gain ladder** (matches KB `P_ADC_*`): 1×, 3.16×, 10×, 31.6×, 100× (√10-spaced). Amplified modes center on the self-bias voltage; full range can be as little as ~50 mV p-p around center → need a huge series R (or series cap for AC). [cgracey p3.9]

### A2. The three reference sources (the crux of "instrumentation"/absolute mode)
- The ADC input can be switched among **GIO (internal ground ref), VIO (internal supply ref), the external pin, and FLOAT**. [cgracey p1.14, p2.25]
- **Absolute voltage requires all three** (GIO, VIO, pin). The shortcut of reading only FLOAT + pin **fails**: FLOAT sits within 0.5% of mid-GIO/VIO but yields ~1000 µV noise vs ~50 µV for the full three-source method. **"There's no substitute for reading all three."** [cgracey p2.25] — verified-by-failure, a strong design fact.
- The conversion formula (Chip's):
  `uV = (3_300_000 / (VIO − GIO)) × (pin − GIO)`  [cgracey p1.14]

### A3. SINC2 manual mode is the sweet spot (key hardware behavior)
- Use **SINC2 in "manual"/filtering mode** (X[5:4]=%01): the smart pin does one differentiation in hardware; software computes the differential each period (`rdpin`/`sub diff`/`add diff`). This exposes **many LSBs** that carry summable signal. Summing *full-conversion* SINC2 samples (X[5:4]=%00) instead would **lose the precision gain**. [cgracey p1.15]
  - → This matches what the **KB already documents** (`p2kbArchSmartPin11000AdcInternalClock`, "SINC2 Filtered ADC with Event Detection" example: rdpin → sub diff → add diff). The thread's *contribution* is the rationale + the GIO/VIO rotation built on top.
- **SINC3** mode: bit growth too rapid for large precision accumulations; improvement "very slight, if any" for this use. SINC3 *does* shine in the **Goertzel** circuit (selectivity). Rule of thumb cited (evanh): **Sinc filter order = modulator order + 1**; P2's modulator is 1st-order → SINC2 is the match. [cgracey p1.15/p1.22, evanh p1.17]

### A4. The 3-sample flush rule (hardware settling — must-know gotcha)
- After switching the ADC input source (GIO↔VIO↔pin), the **first 3 samples are contaminated** by the previous source; the **4th sample is the first clean one**. [cgracey p1.13]
- Why: two decimations are needed for a step to flow through the SINC2 filter, **plus one more** for the analog front-end source-switch to settle (charge sharing on the modulator cap; settles over a fraction of a µs). [evanh p1.17, cgracey p1.22]
- Keeping pin impedance **constant** during switching reduces the disturbance (see A5). [evanh p1.17]

### A5. Constant-impedance multi-pin trick (design insight)
- Tie **3 pins together**; at any instant each of the 3 is assigned one of {GIO, VIO, pin}, so **exactly one pin is always measuring the external node** → the analog source sees **constant ~430 kΩ** impedance and its voltage isn't "yanked around" on each switch. [cgracey p1.14]
- All GIO readings sum together, all VIO together, all pin together (separate accumulators) → 3 pins give **3× the conversion accuracy** of 1 pin in the same time. [cgracey p1.14, evanh p1.18]
- The critical detail evanh flagged: it's the **8-sample accumulation between source selects** + the **strict 3-source cycle** that does the work. [evanh p1.18]

### A6. The hard limits (Chip naming the chip's weaknesses — very valuable)
- **Absolute accuracy is the real problem, not noise.** The ADC uses **three separate matched resistors** for GIO/VIO/pin that "differ more than I thought they would" → pins can be **as much as 15 mV off**. Chip: "I should have designed the ADC differently, so that the same high-z resistor was used for GIO, VIO, and pin." [cgracey p3.3] — **design-limit admission from the designer; gold for an honest app note.**
  - Workaround: you *can drive the pin low* (overcoming the input) to force it near GND and measure that, and drive high for VIO — i.e. self-calibrate against the driven rails. [cgracey p3.3]
- **Noise floor:** after exhausting dithering experiments (inject DAC noise, dither sample period — "SINC2 absolutely hates" period dithering and goes wild; highs-counting mode worse), Chip concluded the FFT spurs were just a **limited-integer-range artifact**, not a deeper defect — i.e. **likely at an "impassable noise floor"** for the ADC. [cgracey p2.16–2.19]
- **Period must be power-of-2 in SINC2 sampling mode**; you cannot freely dither it. [KB + cgracey p2.17]
- **VIO supply quality matters:** VIO on a switch-mode supply ruined an earlier precision attempt; use an LDO. [Rayman p2.1]
- **Temperature / pin-to-pin spread:** VIO/GIO drift with temperature; **VIO is more stable than GIO**; outlier pins (VIO/GIO far from average) drift most. Per-chip fingerprint. [Tubular p1.16/p2.27, evanh]

### A7. WXPIN period encoding detail
- In ADC mode, **WXPIN's low 4 bits set the frame/sample time = 2^X[3:0] clocks**. [cgracey p2.3] (matches KB X[3:0] = period).

---

## 3. AXIS B — Broader / stronger ADC sampling technique (the methods)

These are the reusable *techniques* layered on the hardware — the heart of what makes the note worth writing.

### B1. Accumulate-LSBs to grow resolution (the core idea)
Run SINC2-manual fast (e.g. 128 clocks/sample), take the per-period differential, and **sum many sub-samples**. Long sample times → "16 bits, at least"; Chip calls these **17-bit conversions** in the code headers. Trade rate for resolution by choosing how many sub-samples to sum (`cycles`). [cgracey p1.1, code]

### B2. Three-source ratiometric math (absolute µV output)
Per-final-sample: accumulate ΣGIO, ΣVIO, ΣPin, then compute `(Pin−GIO)/(VIO−GIO) × 3.3 V`. The **improved** math (p2.15) lets the **CORDIC divider auto-scale**: `QFRAC(|Sig−Gio|, (Vio−Gio)<<1)` → `QMUL × (3_300_000<<1)` → `GETQY`. Cleaner and as precise as the hand-shifted version. **This is the math the app note should teach.** [cgracey p2.15, OnePin/ThreePin code]

### B3. Equal time on all three sources
Do **not** skimp on GIO/VIO thinking they're slow-moving — final quality suffers. Spend equal time on GIO, VIO, pin. [cgracey p1.15]

### B4. Two-pin interleave variant (each ref used twice)
Measure `VIO,pin,GIO,pin,VIO,pin,GIO,pin…` so a fresh GIO,pin,VIO or VIO,pin,GIO history exists after every step → emit a sample after each ref read, reusing each GIO/VIO twice; a second pin interleaves to keep impedance constant. Costs Nyquist bandwidth. [cgracey p2.29]

### B5. N-stage time-halving / resolution-doubling filter (elegant, low-cost)
A cascade where Stage k = sum of two Stage k−1 samples, emitted every 2^k periods; pick which stage to compute each period by **bit-reversing an incrementing counter, ENCOD, 32−n**. Outputs **17 stages** (raw … average-of-64K) for almost no memory/constant time. Consumer just **picks the stage** that trades rate vs resolution; ADC runs full-speed always. [cgracey p3.4] — great "Going Further" material.

### B6. Mains-frequency averaging (cheap noise win)
Average over exactly one mains cycle (50/60 Hz) to null AC pickup. Chip ran the 3-pin ADC at exactly 60 Hz to filter ambient AC; brought noise "WAY down" in the Goertzel case. [Christof p2.9, cgracey p2.10/p2.16]

### B7. Voltage-range extension (external)
Add a large **series resistor** (≫ on-chip R; e.g. with the x100 / 5 kΩ internal setting a 50 MΩ external R handles ~±250 V) to dominate the divider; add a HF cap pin→GIO to absorb spikes; **match the external R's tempco** to the on-chip resistor. For AC, a **series cap** lets DC self-bias while passing changes. [Rayman p3.5, evanh p3.8, jmg p3.7, cgracey p3.9]

### B8. SaucySoliton's trapezoid-window SINC3 variant (alternative)
Drive SINC3 with a **1-clock sample interval** + continually-reset first integrator → **continuous double integration** of the bitstream; sum overlapping windows to synthesize a **trapezoid** that both tapers edges *and* averages out PWM. Claims: any cog can read the same ADC at any rate, window can start/stop anytime, only ~2 samples each at ramp-start/ramp-end needed. Perf ≈ Chip's 1-pin code (p-p noise). Code: `code/trapezoid-adc/trapadc3.spin2`. [SaucySoliton p3.21] — **alternative approach to note/compare; verify independently.**

### B9. (Adjacent, different path) Scope-mode ENOB via window overlap
TonyB_'s thread-within-thread: overlap **GETSCP** Hann/Tukey windows at exact intervals (every 15/30/51 clocks) to extend the bitstream and raise ENOB (2× → +0.5 ENOB, 4× → +1). This is the **GETSCP scope path, not the smart-pin SINC ADC** — related but a separate mechanism. Note it as "see also," don't conflate. [TonyB_ p2.5/p2.12/p2.23, cgracey p2.24]

---

## 4. The code artifacts (the "advanced ADC source" hunt — FOUND)

All captured verbatim under `code/`. Progression of Chip's investigation:

| File | What it is | Note relevance |
|---|---|---|
| `OnePinADC.spin2` | **Single pin**, rotates GIO/VIO/pin on one pin; 17-bit; boxcar averaging filter; full DEBUG SCOPE harness. | **Best teaching centerpiece** — simplest complete instrumentation ADC. |
| `ThreePinADC.spin2` | **Three pins tied**, constant-impedance rotation; 3× accuracy. Same math + boxcar filter. | The "Adapt It / 3× accuracy" upgrade. |
| `ThreePinADC_SampleFiltering-4.9K.spin2` | Adds the **N-stage time-halving filter** (B5). | "Going Further" exemplar. |
| `ThreePinADC_SampleFiltering-8K.spin2` | Chip's **working file with idea-comments** (requires PNut_v43); contains the cycle table + improved ratiometric `ComputeSample` + an in-comments 8-channel sketch. | Richest single source of Chip's reasoning + the cycle diagram. |
| **`EightPinADC.spin2`** | **8 ADC pins at once via a PASM2 bytecode interpreter** (`_reset/_addpin/_start/_gio_adc/_msr_adc/_com_adc/_avg_adc/_wait/_jmpr` bytecodes in hub; SKIP-based variable-pin-count core; per-channel Sar/Lim/Cnt averaging). Requires latest PNut (auto-scale SCOPE). | **The "quite advanced ADC" you were hunting for.** Too advanced for the note's main build; ideal as the capstone "what's possible" appendix/reference. |
| `trapezoid-adc/` | SaucySoliton's alternative (trapadc3.spin2 + octave `.m` model + window PNG + serial deps). | Alternative-approach comparison. |
| `P2_ADC_Schematic.pdf` | The actual P2 ADC front-end schematic (Chip-released). | Ground truth for the "How It Works" front-end diagram (redraw concept in TikZ; do not copy). |

**Caveats baked into the code (must address before reuse):**
- `_clkfreq = 320_000_000` (and 324 MHz/2) — Chip "likes to go fast"; **works at any freq ≥ 10 MHz**. The note must use a **datasheet-legal clock** (≤ 300 MHz) and say so. [Rayman p2.11, cgracey p2.13]
- Hard-coded hub addresses ($08000 filter taps, $10000 sample buffer, $0FFFF flag) and pin 15 toggle for scope timing — demo scaffolding, not API.
- Requires recent PNut/Spin2 (v43+ for the SampleFiltering file; latest for EightPin auto-scale SCOPE). **Version-gate** in the note.
- None of this is `pnut_ts`-validated by us yet → **must compile-cert every example we publish.**

---

## 5. Reconciliation against the P2KB (what we already document vs. what's new)

- **Already in KB** (`p2kbArchSmartPin11000AdcInternalClock`, `…11001…`, `…11010AdcScopeTrigger`): the ADC mode %11000, the four X[5:4] sub-modes (SINC2 sampling / SINC2 filtering / SINC3 filtering / bitstream), the `P_ADC_GIO/VIO/FLOAT/1X…100X` input modes, the event-driven SETSE1/WAITSE1 pattern, the SINC2-filtering diff computation + "shift right by log2(samples)−1." The KB's SINC2-filtered example **is** the inner loop of Chip's `Measure`.
- **NOT in KB (the thread's value-add)** — candidate new KB material *and* the spine of the app note:
  1. **GIO/VIO/pin three-source rotation** for absolute (instrumentation) voltage. (A2/B2)
  2. The **ratiometric µV math** with CORDIC auto-scaling. (B2)
  3. The **3-sample flush rule** on source switch (4th sample first valid). (A4)
  4. **Constant-impedance multi-pin** rotation for 3× accuracy. (A5)
  5. **SINC2-manual-accumulate-LSBs** rationale; why not SINC3 / not full-conversion. (A3/B1)
  6. The **absolute-error limit** (matched-resistor mismatch, ≤15 mV; self-cal by driving rails). (A6)
  7. The **N-stage time-halving filter**. (B5)
  8. Practical: **LDO VIO**, mains-cycle averaging, range extension + tempco match, power-of-2 period constraint. (A6/B6/B7)
- **Potential corrections-register items** to verify against current silicon doc / our YAML:
  - The Silicon Doc **ENOB doubling claim** Chip says is too optimistic (would need a 2nd-order modulator) — "Need to change the docs." → check our ENOB wording. [cgracey p1.22]
  - Input-impedance figure: KB/our docs vs evanh's ">500 kΩ" (x1). → verify the number we publish.
  - → Route any confirmed conflict to `engineering/operations/P2KB-CORRECTION-FINDINGS.md`.

---

## 6. Open questions / unresolved in the thread (don't overclaim in the note)
- Exact achievable **ENOB at a legal clock (≤300 MHz) over 0–60 °C across pins/chips** — Christof's target of ENOB≈11 was a *request*, not a demonstrated result. Chip's numbers (50 µV noise, 100 µV p-p resolvable, "17-bit") are **bench/rig** figures.
- **Temperature compensation** never resolved (Rayman/Tubular raised; no closed solution).
- Whether the absolute-error self-cal (drive-rails) fully fixes the 15 mV — described as a method, not characterized.
- TonyB_'s window-overlap ENOB boost — promising, never benchmarked here.

---

## 7. Implications for P2AN001 (the app note)

This thread strongly supports a **P2 instrumentation-ADC app note**: *"Read an absolute voltage in microvolts on a single P2 pin — no external ADC."* Proposed mapping onto the app-note structure (`../../APP-NOTE-CREATION-GUIDE.md`):

- **The Idea** — the smart-pin sigma-delta ADC; why "absolute" needs GIO/VIO/pin; the VIO/2 self-bias.
- **How It Works** — SINC2-manual mode + diff; the 3-source ratiometric math; the 3-sample flush rule; the front-end (TikZ redraw of the schematic). *Grounded on KB %11000 + this thread.*
- **Build It** — a clean, `pnut_ts`-validated, ≤300 MHz **single-pin** version (model on `OnePinADC.spin2`, stripped of demo scaffolding).
- **See It Work / Verify** — DEBUG SCOPE in µV; expected noise band; the "drive a pin to GND, read near-zero" self-check.
- **Adapt It** — 3-pin constant-impedance for 3× accuracy; N-stage filter for rate/resolution choice; range extension; mains-cycle averaging.
- **Pitfalls** — power-of-2 period; LDO VIO; 15 mV absolute-error limit (honest!); high-Z source loading; legal clock.
- **Resources/Reference** — point to `EightPinADC.spin2` bytecode-interpreter as the advanced capstone; SaucySoliton trapezoid as an alternative.

**Single biggest authoring asset:** Chip's own admission of the absolute-error limit and the "no substitute for all three" failure result — exactly the honest, empirically-grounded voice the app-note guide calls for.
