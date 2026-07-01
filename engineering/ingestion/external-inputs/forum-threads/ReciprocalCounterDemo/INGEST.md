# Forum Thread Ingestion — Reciprocal Counter Demo

- **Source URL:** https://forums.parallax.com/discussion/170882/reciprocal-counter-demo
- **Thread ID:** 170882
- **Pages:** 5
- **Post count:** ~118 (31 p1 · 30 p2 · 30 p3 · 30 p4 · 18 p5)
- **OP author + date:** cgracey (Chip Gracey) — 2019-12-04 11:00
- **Fetched:** 2026-07-01
- **Topic class:** Smart-pin frequency/period/duty measurement — reciprocal counter modes (P2 I/O & Smart Pins; app-note P2AN004)

## Thread purpose

Chip Gracey posts a P2 demo that combines the smart-pin "reciprocal counter" modes to
build a competent frequency counter: three adjacent smart-pin cells simultaneously count
system-clock **ticks**, input **highs/states** (density), and complete **periods** over an
adjustable minimum measurement window, then use CORDIC 64-bit intermediate math to compute
frequency and duty without overflow. The thread runs 2019–2024 and covers the smart-pin
counting-mode setup, a long naming debate (ticks/highs/periods vs time/density/quantity),
extended crystal/PLL accuracy-and-jitter investigation with lab-grade 10 MHz references, a
widely-reused Spin2 port (Ariba), tooling notes (PNut vs FlexProp/loadp2 baud & -g debug),
and single-vs-dual-pin measurement without an external loopback wire.

## Participant trust classification

| User | Trust | Basis |
|------|-------|-------|
| cgracey (Chip Gracey) | 🏆 authoritative | P2 chip designer; demo author; ground truth on smart-pin modes & math |
| evanh | 🟢 knows the domain | Deep, consistently-correct smart-pin/PLL/scope/pin-routing analysis across the thread |
| jmg | 🟢 knows the domain | Rigorous reciprocal-counter/ppm/NCO/timebase analysis; correct crystal-cap tradeoff reasoning |
| ersmith (Eric Smith) | 🟢 knows the domain | Author of flexspin/fastspin/loadp2; authoritative on tooling & PASM local labels |
| Ariba (Andy) | 🟢 knows the domain | Contributed the canonical working Spin2 port; correct ticks/periods explanation |
| samuell (Samuel Lourenço) | 🟢 knows the domain | Strong instrumentation/clock-jitter/hardware measurement expertise (in measurement domain) |
| Francis Bauer | 🟢 knows the domain | Pointed to TSL235R Quick Byte with working inline-PASM2 smart-pin freq-measure drivers |
| Rayman | 🟡 general community | Naming opinions + a working code adaptation (VSync measure); mostly usage-level here |
| rogloh | 🟡 general community | Single tooling question |
| Bean | 🟡 general community | Question-asker; naming opinions |
| msrobots | 🟡 general community | General commentary |
| Bob Lawrence (VE1RLL) | 🟡 general community | Appreciation/commentary |
| dMajo | 🟡 general community | Brief opinion |
| pilot0315 (Martin) | 🟡 general community | Learner; troubleshooting the demo |
| Ramon | 🟡 general community | Learner; port/troubleshooting questions |

## Chip Gracey findings (trusted gold)

### CG-1 · Reciprocal counter = three smart-pin cells (ticks / highs / periods)
> "This demo shows the reciprocal counter modes working together to form a pretty
> competent frequency counter. It outputs serial text at 1Mbaud and works really well
> with the Parallax Serial Terminal."

Configuration (verbatim code lines from OP):
```
wrpin	msr_time,#msr_pin+0      ' %..._10101_0  count SysCLK ticks  (P_COUNTER_TICKS)
wrpin	msr_states,#msr_pin+1    ' %..._10110_0  count input highs   (P_COUNTER_HIGHS)
wrpin	msr_periods,#msr_pin+2   ' %..._10111_0  count periods       (P_COUNTER_PERIODS)
```
```
rqpin	clocks,#msr_pin+0
rqpin	states,#msr_pin+1
rqpin	periods,#msr_pin+2
```
**Means:** The demo dedicates three adjacent smart-pin cells (base = P0) each in a distinct
counting mode — mode field `%10101` counts elapsed system-clock ticks, `%10110` counts how
many highs (1-samples) occurred, `%10111` counts whole input periods — all gated over the
same adjustable minimum-time window (`msr_time`/X). AKPIN starts them together; a `testp`
poll waits for the done flag; RQPIN reads all three. The mode words map to the named Spin2
constants `P_COUNTER_TICKS`/`P_COUNTER_HIGHS`/`P_COUNTER_PERIODS` (%10101/%10110/%10111).
**Affects:** I/O & Smart Pins User Guide Ch.14 (counting modes) & Ch.15 (period/frequency);
P2AN004 (Frequency/Period/Pulse Measurement) — canonical worked example. Cross-check the
`%10101/%10110/%10111` ↔ `P_COUNTER_TICKS/HIGHS/PERIODS` mapping against the smart-pin YAML.

### CG-2 · 64-bit intermediate math prevents overflow (frequency & duty)
> "Note that the duty and frequency computations first multiply to produce 64-bit products,
> then divide those 64-bit products by 32-bit values. This allows full 32-bit inputs to be
> handled without any interim overflows."

Verbatim pattern (frequency = periods × sysfreq ÷ ticks; duty = states × 1000 ÷ ticks):
```
qmul	periods,##round(sysfreq)   ' 64-bit product in QX:QY
getqx	x
getqy	y
setq	y                          ' load high long of dividend
qdiv	x,clocks                   ' 64 ÷ 32
getqx	frequency
```
**Means:** Reciprocal-counter math must multiply before dividing to keep resolution; doing it
in 32 bits would overflow. CORDIC QMUL yields a 64-bit product (QX low / QY high); SETQ+QDIV
divides the full 64-bit value by the 32-bit tick count. This is the Spin2 `muldiv64()` idiom
(`freq := muldiv64(clkfreq, periods, ticks-1)` in later ports).
**Affects:** P2AN004 computation section (teach `muldiv64`/CORDIC 64-bit pattern as the
correct way); IOSP Ch.15. evanh: "My favourite feature ... is the demonstration of using a
64-bit intermediate in the calculations."

### CG-3 · "states" = "highs" = count of 1-samples during the window (→ duty)
> "It's not even 'periods'... States could be called 'highs', since it tracks how many 1's
> were reading during the measurement."

**Means:** The middle counter (mode `%10110`, `P_COUNTER_HIGHS`) accumulates how many sample
clocks saw the input high. Divided by total ticks it yields duty cycle (evanh: "Duty is the
average!"; "Density ... as in pulse density modulation"). Naming was debated: Chip floated
"clocks/highs/periods" or "time/density/quantity" and later preferred **ticks**.
**Affects:** IOSP/P2AN004 terminology — document the three counters as **ticks / highs
(density) / periods**; note duty = highs ÷ ticks. Terminology guidance only (the constant
names are fixed as TICKS/HIGHS/PERIODS).

### CG-4 · Measured pins aren't "consumed" — only their smart-pin cells are used
> (jmg) "pins aren't consumed, only their smart pin cells are used for measurement."
> cgracey: "That's true, though you would have to use their smart pin modes to control their
> output enable states."

**Means:** The +1/+2 cells used for highs/periods measurement don't block those physical pins
from other use, but you must manage their output-enable via the smart-pin mode. Later
(evanh/Ariba/Rayman) the demo shrinks to **two** cells using `P_MINUS2_A/B`,`P_MINUS3_A/B`
input rerouting so a nearby pin is measured without any external loopback wire.
**Affects:** IOSP Ch.14/15 caveat on pin-cell vs pin usage and `P_MINUS*` input routing;
P2AN004 practical wiring note (measure a neighbor within ±3 pins with no jumper).

### CG-5 · Crystal loading-cap modes affect measured accuracy (clock config)
> "I was using crystal mode %10 (7.5pF). He could try %11 (15pF), or even %01 (no caps)."
> Follow-up: "There could be a low beat frequency between the 250 MHz sample rate and the
> input frequency that contributes to a varying duty cycle via gradual aperture shift."

**Means:** The P2 XI/XO on-chip crystal loading caps (`%CC` field) trade frequency offset; a
few-ppm sysclock offset beats against the input and slowly walks the aperture, wobbling the
measured duty. Note a **discrepancy to verify**: Chip labels `%10 = 7.5pF`, `%11 = 15pF`;
jmg's own table labels `%10 = 15pF/pin`, `%11 = 30pF/pin`. Resolve against the P2 clock-config
/ hardware YAML before citing exact pF values.
**Affects:** Reference/cross-check → clock-setup docs (crystal cap `%CC` semantics) and any
measurement-accuracy caveat in P2AN004. **Do not** cite pF values until the %10/%11 pF
discrepancy is reconciled with an authoritative source.

### CG-6 · Written under PNut; tool differences can bite
> "Are you using PNut or FlexGUI? It was written under PNut. There could be some difference
> between tools."

**Means:** Original targets PNut; ports need tweaks (FlexProp/loadp2 baud defaults, `-g` for
debug, `.spin2` extension, no cross-block JMP). Provenance/tooling note, not a silicon fact.
**Affects:** Reference only (ingestion provenance; example-portability note).

## Other credible technical contributions (community / cross-check — verify before use)

- **evanh 🟢** — Headroom rule: at 250 MHz sysclk you can measure up to ~100 MHz input
  ("2x is enough but always want a little headroom"). Reasonable design guidance → P2AN004
  "measurement range" note; verify the exact ceiling against smart-pin sampling limits.
- **evanh 🟢** — Two-cell, wireless self-measurement using `P_MINUS2_A/B` / `P_MINUS3_A/B`
  input rerouting (measure a neighbor pin with no loopback wire); pin-routing block-diagram
  explanation. Cross-check the P_MINUS routing constants against smart-pin YAML.
- **jmg 🟢** — Reciprocal counters auto-scale across a wide dynamic range; summing 10–100
  gapless time+cycle captures raises precision; a simpler non-reciprocal fixed-time gate
  trades dynamic range (100 ms gate: 1% at 1 kHz vs 2 ppm at 5 MHz). Good app-note "when to
  use reciprocal vs gated" material.
- **jmg 🟢** — The ppm-of-a-single-interval metric is interval-dependent (evanh: "the
  parts-per-million method is rubbish ... depends on the measurement interval") — jitter is
  averaged out by the ~10 ms window; this counter does **not** measure jitter. Caveat for the
  app note's accuracy discussion.
- **Ariba (Andy) 🟢** — Canonical Spin2 port: `pinstart(...P_COUNTER_TICKS...)` +
  `pinstart(...P_COUNTER_PERIODS...)`, `akpin`, `rqpin`, `freq := muldiv64(clkfreq, periods,
  ticks-1)`. The `ticks-1` correction is worth verifying/explaining. Reused by Rayman for
  VSync measurement (measuring a pin within ±3 via `P_MINUS2/3` without jumpers). Strong
  candidate example for P2AN004 / IOSP.
- **Francis Bauer 🟢** — Points to the TSL235R Quick Byte (2 inline-PASM2 driver routines,
  2–3 smart pins) as another frequency-measure reference. (Repo already tracks `TSL235R-LF.md`
  — link this thread's demo to that Quick Byte.)
- **ersmith 🟢** — PASM local labels: P1 `:label` → P2 `.label` (temporary until next global
  label); REP works with local labels. Tooling: flexspin needs `-g` to enable `debug()`;
  `.spin` vs `.spin2` matters. Reference for the PASM style/tooling notes.

## Doc-impact targets (reconciliation queue)

| # | Finding | Target doc/section | Suggested action | Trust |
|---|---------|--------------------|--------------------|-------|
| 1 | Three-cell reciprocal counter: ticks/highs/periods modes `%10101/%10110/%10111` = `P_COUNTER_TICKS/HIGHS/PERIODS` | IOSP Ch.14 (counting) & Ch.15 (period/freq); P2AN004 | Add/verify worked example + confirm mode↔constant mapping in smart-pin YAML | 🏆 |
| 2 | 64-bit intermediate math (QMUL→SETQ→QDIV / `muldiv64`) prevents overflow in freq & duty | P2AN004 computation; IOSP Ch.15 | Teach the 64-bit multiply-before-divide idiom as canonical | 🏆 |
| 3 | "states/highs/density" counter → duty = highs ÷ ticks; terminology guidance | IOSP/P2AN004 terminology | Document counters as ticks/highs(density)/periods; note constant names are fixed | 🏆 |
| 4 | Measured pins not consumed; two-cell wireless measure via `P_MINUS2/3_A/B` routing (±3 pins, no jumper) | IOSP Ch.14 pin-cell vs pin; P2AN004 wiring | Add caveat + neighbor-pin routing example; verify P_MINUS constants | 🏆/🟢 |
| 5 | Crystal `%CC` loading-cap modes shift sysclock ppm → duty aperture walk; **%10/%11 pF value discrepancy** (Chip 7.5/15pF vs jmg 15/30pF) | Clock-config/hardware docs; P2AN004 accuracy caveat | Reconcile pF-per-mode against authoritative source BEFORE citing values | 🏆 (values ⚠️unverified) |
| 6 | Measurement range/headroom: ~½ sysclk input ceiling (≤100 MHz @250 MHz) | P2AN004 range note | State range with headroom; verify exact ceiling | 🟢 |
| 7 | Reciprocal vs fixed-time-gate tradeoff; gapless summing for precision; this method does NOT measure jitter | P2AN004 "method selection" + accuracy caveats | Add guidance paragraph | 🟢 |
| 8 | Canonical Spin2 port (Ariba) with `muldiv64(clkfreq,periods,ticks-1)`; Rayman VSync reuse | P2AN004 / IOSP example | Adopt as Spin2 example; verify/explain `ticks-1` correction; compile-cert with pnut_ts | 🟢 |
| 9 | PASM local-label `.label` (was `:label` on P1); tooling: flexspin `-g` for debug, `.spin2` ext, no cross-block JMP | IOSP PASM style / examples-portability note | Reference only; ensure example notes tool requirements | 🟢 |
| 10 | Link demo to TSL235R Quick Byte (inline-PASM2 freq-measure drivers) | P2AN004 related-examples; `TSL235R-LF.md` | Cross-reference the two | 🟢 |

## Open questions / unresolved

- **%10/%11 crystal-cap pF values conflict** (CG-5): Chip says %10=7.5pF/%11=15pF; jmg's table
  says %10=15pF/pin, %11=30pF/pin. Must reconcile with the P2 clock-config authority (Silicon
  Doc / hardware YAML) before any pF value is published.
- **`ticks-1` correction** in the Spin2 `muldiv64(clkfreq, periods, ticks-1)`: origin/justification
  not fully explained in-thread — verify whether it's an off-by-one gate correction before
  documenting.
- **Exact input-frequency ceiling** vs sysclk (evanh's "2×+headroom", ≤100 MHz @250 MHz): confirm
  against smart-pin edge-sampling limits.
- **Beat-frequency/aperture-walk duty wobble** (CG-5): qualitative only; no quantified model —
  present as a caveat, not a spec.
- The thread does **not** touch the ADC or the streamer despite the ingestion hypothesis; its
  content is smart-pin counting + clock/PLL accuracy only. (Pin block-diagram / ADC-as-input
  remarks on p5 are general pin-circuit background, not counter behavior.)
