# P2AN004 — Release-Gate Deep Audit (2026-07-03)

**Doc:** P2AN004 "Frequency / Period / Pulse Measurement" (Read Sensors by Timing, Counting, and Decoding on a P2 Pin)
**For:** v1.0.0 first release
**Verdict:** **GO** — 0 code defects. 1 LOW prose imprecision + 1 hardening + 2 trivial wording/drift items, all FIXED. 1 KB-side finding logged (F-193, non-blocking; the doc is already correct).

## Method

Exhaustive fan-out (4 independent verification agents, each on a distinct claim cluster)
against the authoritative P2KB (p2kb-mcp), the Silicon Doc v35 ingestion extracts
(`part4-smart-pins.txt`), the smart-pin YAMLs, the Spin2 v55 text, the IOSP opus-master
(companion manual, Chs. 13–15), P2AN001/002/003 (consistency anchors), the OBEX MCP, the
ams/TAOS TSL235R datasheet extract, and live `pnut-ts` v1.55 compilation. Every agent finding
was **hand-verified** before action (fan-out findings can invert). All 3 programs compile
clean (`-d`); the doc's 3 recipe blocks are drift-checked against the `examples-library/` files.

Clusters: (A) smart-pin measurement modes, (B) Spin2/PASM2 code semantics, (C) transducer /
datasheet facts, (D) attributions / OBEX / versions.

## Drain gate

**GREEN for this note's domain.** The measurement/count/frequency/quadrature findings that
surfaced during app-note authoring (F-176 `P_B_A_INPUT`-fictitious, F-177 `P_QUADRATURE_A`,
F-178 `P_HIGH_TICKS` pulse-width) are all **DONE (2026-07-01)**, and they *validated exactly the
constants P2AN004 uses* — including the F. Bauer `fb_measfreq2P` single-pin routing
(`P_COUNTER_TICKS` local + `P_COUNTER_PERIODS | P_MINUS1_A | P_MINUS1_B`) that R2 adopts verbatim.
The two register findings still open (USB analog front-end, Chip-gated; async-serial-TX
first-byte glitch, NEEDS-HW-CONFIRM) are outside this note's domain.

## Findings

### LOW — R1 Verify prose mis-described the open-sensor symptom — FIXED
The Verify block claimed an open sensor / too-short charge shows as "a count pinned near the
maximum (`$8000_0000`)." But `%10001` (`P_HIGH_TICKS`) raises IN **only on a high→low
transition**; if the node never falls (sensor disconnected, series path open, or charge too
short so it never went high), IN never rises and the polled `repeat until pinread(RC_PIN)`
loop **hangs** — the `$8000_0000` value is never returned. **Fix (opus-master prose only):**
reworded the two failure branches — a *hang* is the never-crossed symptom; a *near-zero* count
is the missing-`P_LOW_FLOAT` symptom (low output drives the node to ground instead of floating).

### HARDENING — R2 irradiance scale folded into the constant — APPLIED
`ee_x100 := muldiv64(freq * 100, CAL_UW, CAL_HZ)` pre-multiplies `freq * 100` in 32 bits, which
overflows above ~21.47 MHz. Safe for the TSL235R (250 kHz reference, ~21× margin — this is **not**
a P2AN003-R4-class in-range bug), but the note explicitly promises R2 generalizes to *any*
frequency-output sensor (e.g. a voltage-to-frequency converter). **Fix (opus-master +
examples-library, recompiled clean):** `muldiv64(freq, CAL_UW * 100, CAL_HZ)` — `CAL_UW * 100`
folds at compile time and the multiply now lands inside `muldiv64`'s 64-bit intermediate,
removing the ceiling. Identical results in-range.

### TRIVIAL — comment drift + datasheet term — FIXED
- `examples-library/light-to-freq-reader.spin2` header comment read `freq = periods * clkfreq /
  ticks` while the doc read `freq = MULDIV64(periods, clkfreq, ticks)`. Aligned the file to the
  doc (drift → 0).
- References §3 called the 250 kHz / 430 µW/cm² point the "responsivity figure"; the datasheet
  labels it an **output-frequency** operating characteristic (the number and all four conditions
  are exact). Reworded to "output-frequency figure."

### CONFIRMED (no defect)

- **Smart-pin modes (cluster A, all VERIFIED against Spin2 v55 + YAML + Silicon Doc):**
  %10001 `P_HIGH_TICKS`, %10101 `P_COUNTER_TICKS`, %10111 `P_COUNTER_PERIODS`, %01011
  `P_QUADRATURE` — encodings, constant names, and mechanisms all correct. Modifiers
  `P_SCHMITT_A`/`P_OE`/`P_LOW_FLOAT`/`P_LOW_150K`/`P_FILT1_AB`/`P_PLUS1_B`/`P_MINUS1_A`/
  `P_MINUS1_B` all real symbols with correct meanings. Reciprocal formula `freq = periods ×
  clkfreq ÷ ticks` and the worked 50 kHz/100 ms/200 MHz example (5000 periods, 20 M ticks →
  50 000 Hz) exact. R2 single-pin routing (both A **and** B routed back) is required by the
  Silicon "period = A-rise to B-rise, B default = own pin" rule and matches the fb_measfreq2P
  donor. R3 X=0 continuous totalizer, DIR-pulse zero, `sar 2` per-detent normalization all correct.

- **Code semantics (cluster B, no BUG):** R1 `pinf`/`pinl` DIR-pulse reset with `P_OE` keeping
  the driver enabled regardless of DIR (float only when OUT→0) is sound. R2 overflow-safe
  (`periods * clkfreq` inside `muldiv64`'s 64-bit path; divide-by-zero guarded; `freq` return
  var zero-inits). R3 `rdpin sar mod4x` signed normalization, clamp+re-anchor bookkeeping,
  active-low hold-for-window button debounce all correct. **R3 self-test hand-traced: reads 5
  then 3** (gray code +4/detent → `20 sar 2 = 5`; `(20−8) sar 2 = 3`) — no half-quadrature error.

- **Transducer/datasheet (cluster C, all VERIFIED vs TAOS038E):** fO 250 kHz typ @ 430 µW/cm²
  @ 635 nm @ 5 V; 2.7–5.5 V (works at 3.3 V); dark 0.4–10 Hz; linear irradiance map; 0.1 µF
  decouple (high end of the datasheet's 0.01–0.1 µF range); 3-pin square-wave. RC-decay physics
  (τ = R·C) and CdS direction (brighter → lower R → faster discharge → smaller count) correct.

- **Attributions/OBEX (cluster D, all VERIFIED):** OBEX #2831 P2_rctime / phonoclese (incl.
  REGEXEC / `org $1B0` / `RETI1` specifics, confirmed against captured source); OBEX #2829
  Quadrature Encoder / Jon "JonnyMac" McPhalen; TSL235R Quick Bytes four-name credit (Bauer,
  McPhalen, C. Gracey, K. Gracey); `fb_measfreq2P` donor located in-repo; `pnut_ts` v1.55;
  copyright/CC-BY-NC-ND/trademark block byte-identical to released siblings.

## KB-side finding routed to corrections register

**F-192 (logged, NEEDS-VERIFICATION, non-blocking):** the audit surfaced a tension with the
existing **F-187** (Chip Gracey 🏆), which added A-only routing (`P_MINUS1_A` / `P_MINUS2_A`) to
the `smart-pin-10110`/`10111` YAML + IOSP §15.4 concurrent-measurement examples. The Silicon Doc
period definition (period = A-rise → B-rise; and its explicit note "the B-input can be set to the
same pin as the A-input for single-pin cycle measurement") plus the working `fb_measfreq2P` donor
both indicate a *neighbour* cell needs **B routed too** (`| P_MINUS1_B`), else its idle B never
rises and the window hangs. Because F-187 is 🏆-attributed, F-192 is logged as NEEDS-VERIFICATION
(hardware spot-check to confirm A-only actually hangs) rather than a blind YAML edit. **P2AN004 is
unaffected** — R2 already routes both A and B (correct under either reading), so this is
non-blocking for this release.

## Gate

- Drain gate: **GREEN** (domain findings all DONE; open findings out of domain).
- Code: 3/3 compile clean with `-d`; longest code line 75 ≤ K=76; 0 U+FE0F in body.
- Drift: doc ↔ examples-library aligned (comment drift fixed).
- Verdict: **GO** to visual/diagram phase, then finalize → release.
