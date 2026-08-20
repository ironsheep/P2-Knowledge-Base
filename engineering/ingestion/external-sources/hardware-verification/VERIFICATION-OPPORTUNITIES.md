# P2 Verification Opportunities — the "could-verify" register

**What this is.** The register of empirical verifications we have *identified but not
yet performed*. Its job is to make sure a verification we *could* do is never lost —
whether we run it soon or file it for "someday." It is the forward-looking companion to
[`P2-EMPIRICAL-FINDINGS.md`](P2-EMPIRICAL-FINDINGS.md): the ledger holds proofs we
**have**; this holds proofs we **could get**. When an opportunity is performed and
accepted, it graduates to an `EF-NNN` entry in the ledger and is marked `DONE → EF-NNN`
here.

## The classification rule (fold this into every audit / finding)

When an audit or a correction-finding surfaces a claim that wants empirical
confirmation, **classify the test by what rig it needs** — this decides whether we do
it or catalog it:

| Class | Rig it needs | Policy |
|-------|--------------|--------|
| **Jumper-only** | Nothing beyond the P2 board + jumper wires. On-chip DAC→pin loopback, pin-to-pin routing, a pin's own IN flag, internal references (GIO/VIO). | **We do these.** Cheap, always available — write the `.spin2`, run it, accept → EF ledger. Fold into the normal verification flow. |
| **External-hardware** | Anything *added* to the device: a calibrated voltage/frequency reference, a precision meter, a sensor/transducer, an external bias network, a signal generator, a scope-as-source. | **We catalog, we do not commit** (short term). Record it here with the **benefit** doing it would provide, so it's never lost. Do it only when the payoff justifies standing up the rig. |

**Why the split:** a jumper-only test costs a minute of the maintainer's time and is
always reproducible; an external-hardware test costs a bench setup and calibrated gear
we don't want to commit to on a release cadence. Both are worth *recording*; only the
first is worth *scheduling* by default. Stating the benefit for the external ones lets
us prioritize honestly if one ever becomes worth the setup.

---

## Section 1 — Jumper-only queue (runnable; we do these)

The standard verification flow applies (author in the manual's `audit/verification-tests/`,
run, accept, replicate to the ledger). Listed here only until performed, so the queue is
visible.

| ID | Verifies (finding) | Approach (jumper-only rig) | Benefit | Status |
|----|--------------------|----------------------------|---------|--------|
| **VO-J-001** | ADC gain-mode framing — gain modes measure **centered on mid-supply (~VIO/2)** (F-202; task #172) | DAC on P0 → **jumper** → ADC on P1; coarse + fine (2 mV) sweep, auto-detect each gain's 5/50/95% crossings. Bracketed (digital short-check + GIO/VIO refs). Tests: `…/adc-gain-window-probe.spin2` + `…/adc-gain-window-fine.spin2`. | Confirmed centered on ~1.64 V for all gains; measured windows (√10 ladder). **Refuted my derived 3.3 V/gain formula.** | **DONE → EF-024** (2026-07-07) |
| **VO-J-002** | ADC ratiometric single-pin absolute-error bound (F-203 "~15 mV floor" AT_RISK) | Same P0→P1 rig; reconstruct known DAC voltages, report measured-vs-known error. `…/adc-error-floor-probe.spin2`. | Single-pin abs error **≤9 mV** (reproducible) → does NOT support a ~15 mV single-pin floor. | **DONE → EF-024** (single-pin bound). The *pin-to-pin spread* half is **RECLASSIFIED → VO-X-002** (external-hardware) — it is NOT a simple-jumper test; see the analysis below. |
| **VO-J-003** | Which `%TT` a **streamer-fed** DAC needs (F-272; task «#278») | DAC on P0 → **jumper** → ADC on P1, sensed with `P_ADC_1X \| P_ADC` / `WXPIN` 12 / `RDPIN`. Four arms, control-first: **R** streamer→digital pin read back (proves the cog's streamer reaches the pin), **C** level-driven DAC at `TT=%00` as the Parallax documentation's own program does it (proves jumper+DAC+ADC), then **T0** streamer-routed DAC at `TT=%00` and **T1** the same with `P_CHANNEL`. Rig authored + compiled: `…/p2-streamer-programming-guide/audit/verification-tests/test-f272-streamer-dac-tt.spin2`. | Closes the one arm EF-054/EF-055 do **not** cover: both are graded `[M-pre — streamer-free]`, having tested the pin arrangement with the streamer uninvolved. F-264 proved this axis **inverts**, and both candidate forms compile clean, so a compiler cannot separate them. | **READY TO RUN** — authored 2026-08-20, awaiting a bench slot. Not gating: F-272 is already `RESOLVED` from documentary sources. |

## Section 2 — External-hardware catalog (recorded; NOT committed short-term)

We could do these; we are deliberately not scheduling them. Each carries the benefit it
would provide if the rig were ever stood up.

| ID | Would verify | External hardware needed | Benefit if done | Status |
|----|--------------|--------------------------|-----------------|--------|
| **VO-X-001** | Exact ADC gain-mode input endpoints **and their device tolerance** (absolute, not nominal) | A calibrated external voltage reference + a precision meter (traceable), across several parts/temperatures | Upgrades the §16.2 **nominal** windows to **guaranteed, tolerance-bounded absolute specs** (datasheet-grade). Not needed for correctness — the nominal + calibration-caveat treatment is already correct — this would only tighten "nominal" → "characterized." | CATALOGED |
| **VO-X-002** | ADC **pin-to-pin absolute spread** (F-203 §16.8 "different pins can read ~15 mV apart") — how far pins **across the chip's VIO/GIO supply groups** read the same true voltage, raw vs. per-pin-calibrated | A **group-independent, calibrated absolute voltage reference** (not the on-chip DAC — see analysis) fanned to one ADC pin in each of several silicon VIO/GIO domains (four pins each — see the analysis below); ideally a precision meter on each domain's VIO/GIO to attribute supply variation vs. device mismatch; several parts/temperatures for a real bound | Turns §16.8's *representative* "~15 mV" into a **measured, attributed** figure — and quantifies how much per-pin two-point calibration (the §16.8 mitigation) actually recovers. Correctness of §16.8 does not depend on it (the qualitative "calibrate per pin" guidance is already right); this would let us state a real number and split it into group-supply vs. device-mismatch causes. | CATALOGED (reclassified from VO-J-002, 2026-07-07) |

### Why VO-X-002 is NOT a simple-jumper test — the analysis (do not lose this)

The pin-to-pin spread *looks* jumper-only (tie a DAC pin and several ADC pins to one node,
compare readings). Analysis of the P2 ADC architecture shows a simple-jumper rig cannot
give a clean, attributable answer:

- **VIO/GIO are PER-DOMAIN, not global — and there are TWO grouping layers.** In the
  **silicon**, the 64 pins are **16 domains of FOUR** (P0-3, P4-7, … P60-63); each domain has
  its **own** `VIO_{x}_{y}` (3.3 V) package pin and `GIO_{x}_{y}` (ground) block, and the ADC
  calibrates **ratiometrically against its own domain's VIO/GIO** (Silicon Doc: "Delta-sigma
  ADC with 5 ranges, 2 sources, and VIO/GIO calibration"). On a **P2 Edge module** the eight
  3.3 V LDOs group the headers in **eights**, one LDO feeding **two** silicon domains — a
  shared supply *net*, but each domain still reaches the die through its own VIO pin and bond
  wire. Both layers are real; the reference domain the ADC actually follows is the silicon
  four. Grounded in **F-269** (`P2KB-CORRECTION-FINDINGS.md`) — Silicon Doc v35 Part 1 p.9
  pinout + P2 datasheet *"powered in groups of 4 via VIO pins"*. **This bullet is where the
  error F-269 corrects was originally seeded**: it asserted "8 groups of 8" with no source of
  its own, and F-211 later cited it back as authority for a silicon fact. It carries its
  grounding now for exactly that reason.
- So the spread's dominant cause is **domain-to-domain supply-reference variation** (each
  domain's real VIO/GIO sitting at a slightly different potential — board IR drop, decoupling,
  routing, bond-wire), NOT within-domain device mismatch.
- **A same-domain rig sees almost nothing.** Pins in one domain share a VIO pin and a GIO
  block; after ratiometric reconstruction the shared supply cancels, leaving only small
  (sub-mV → low-mV) per-pin device mismatch. The first probe attempt used **P1-P6**, which
  spans two silicon domains (P1-P3 in `VIO_0_3`, P4-P6 in `VIO_4_7`) but only **one** Edge LDO
  net (P0-7) — so it exposed bond-wire and package IR differences at best and cancelled the
  board-level supply term entirely. It would still have under-measured the effect and falsely
  "refuted" the claim. (That probe, `…/adc-pin-spread-probe.spin2`, is retained as an
  annotated reference, marked insufficient.)
- **The on-chip DAC is itself anchored to ITS domain's VIO** — so it cannot serve as the
  domain-independent absolute reference the measurement needs. Driving the node from the DAC
  means the *source* is referenced to the DAC pin's own domain while each ADC pin reconstructs
  against its own — a confound that a jumper rig cannot remove. A clean **absolute** pin-to-pin
  spread needs an **external** reference independent of every domain's VIO/GIO.
- **Raw vs. calibrated are two different numbers.** A user doing the naive fixed-scale
  conversion (`sample * 3300 / 16383`, no per-pin GIO/VIO) eats the full domain-to-domain spread
  — that is the ~15 mV §16.8 warns about. A user doing per-pin two-point calibration (§16.8's
  recommended fix) cancels most of it. A trustworthy test must report both and attribute the
  difference, which needs the external reference (+ ideally per-group VIO/GIO metering).

Note: a *crude relative* spread (max−min across cross-domain pins, DAC-driven) is technically
jumper-feasible, but it is neither absolute nor attributable and is not worth doing on a
release cadence — hence the external-hardware classification. §16.8 stands as-is (qualitative,
correct) until VO-X-002 is ever run.

---

## Lifecycle

```
identified (here)  ──jumper-only? do it──▶  EF-NNN (ledger)   ──▶ mark "DONE → EF-NNN" here
                   ──external-hw?  catalog with benefit, revisit only if payoff justifies rig
```

A verification never just evaporates: it is either **done** (→ ledger) or **cataloged
with its benefit** (here). That is the whole point — no could-verify is lost.
