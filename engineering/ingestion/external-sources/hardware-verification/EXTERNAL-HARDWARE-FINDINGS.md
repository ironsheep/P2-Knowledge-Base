# External-project hardware findings — running ledger

**What this is.** P2 behaviours **proved by test on real silicon, on a partner project's bench**.
Same kind of evidence as [`P2-EMPIRICAL-FINDINGS.md`](P2-EMPIRICAL-FINDINGS.md); different rig,
different hands. Entries are `XF-NNN` and each one **names the project it came from**.

## Why this is a separate register, and what that does NOT mean

It does **not** mean weaker. Stephen, 2026-09-19: *"This comes from the project that is developing
the software on the hardware and running against hardware. The external source in this case is one
of our own projects, and we have hardware runs to prove behavior."* A partner project's controlled
run against silicon is hardware evidence, and it outranks every documentary source the same way
ours does.

It is separate because **`EF-NNN` carries a specific promise** — *we* built the test, *we* ran it,
*we* accepted it, so its scope and its failure modes are ours to answer for. When a reader asks
"what rig, what board, what else was on the bus?", an EF entry answers from this project's own
records. An XF entry cannot, so it says whose bench it was and carries that project's own scope
statement verbatim. Keeping the promise intact is worth more than a single ledger.

**Authority order** (matching `DOMAIN_AUTHORITY` in `.claude/skill-conventions.md`):

1. `EF-NNN` — our bench.
2. `XF-NNN` — a partner project's bench. **Equal in kind to EF**; cite it exactly as freely, and
   name the project when you do.
3. The `pnut-ts` compiler, for legality only.
4. Parallax documentary sources.
5. The published P2KB YAML.

Where an XF entry and a documentary source disagree, the silicon wins — same as EF.

## Admission rules

An entry earns `XF-NNN` when all of these hold. They are the same bar we hold ourselves to:

1. **It ran on silicon**, and the entry says on what board, at what clock, with what else attached.
2. **It carries a control.** A positive arm alone is not a measurement — there must be something
   that could have failed and did not, or a negative arm that failed as predicted.
3. **Its scope is stated by the project that ran it**, in their words, and we do not widen it.
   A five-point fit is recorded as a five-point fit.
4. **The claim is separable from their driver.** A result that only holds inside one codebase is a
   note about that codebase, not a P2 behaviour.

A submission that misses one of these is still **recorded** — as `XF-NNN · UNGRADED`, with the gap
named — rather than discarded. Discarding it loses the observation; grading it honestly does not.

**Status legend:** `CONFIRMED` · `CONFIRMED-FALSE` · `SCOPED` (real, and bounded by a scope the
submitting project states) · `UNGRADED` (recorded, admission bar not met — says which rule) ·
`SUPERSEDED`.

---

## P2X8C4M64P / uSD-FAT32 project

### XF-001 · The write-side SPI alignment pad is a phase of period `hp`, with exactly one losing value — `SCOPED`

Streamer driving a `P_SYNC_TX` MOSI against a `P_TRANSITION` SCK. SCK starts on the next
base-period boundary after `WYPIN` while the streamer start moves continuously, so only `hp`
distinct phases exist (`hp` = the SCK half-period in sysclks) and **exactly one of them loses**.
At the losing phase the failure is **silent whole-sector write corruption** — no error, no status
bit. A pad safe at one `hp` can be exactly wrong at another: their default of 4 was maximally safe
at `hp=7` and landed on the cliff at `hp=5`, which any sysclk from 201–250 MHz reaches at an
ordinary 25 MHz SPI ceiling.

*Measured:* five independently measured rungs, losing residue `pad ≡ −6 (mod hp)`:

| `hp` | 4 | 5 | 6 | 7 | 14 |
|---|---|---|---|---|---|
| measured losing residue | 2 | 4 | 0 | 1 | 8 |
| `(−6) mod hp` | 2 | 4 | 0 | 1 | 8 |

*Scope, in their words:* **"a fit to five points, not a law."** Not established whether −6 is
constant across `hp`, whether it holds at `hp` = 2 and 3 (reachable, never measured), or **whether
the quantity is in sysclks at all** — a related launch delay on the same rig measured as
nanosecond-constant rather than sysclk-constant. One board, one host implementation, one card set.

*Grade rationale:* `SCOPED`, not `CONFIRMED`, entirely on rule 3 — the shape is well evidenced,
the formula is a five-point fit its own authors decline to call a law.

*What it grounds:* nothing yet. **The KB will carry the shape — one losing phase per `hp`, silent
corruption, a pad is not portable across rates — and not the formula**, until `VO-P-001` returns a
complete map. Our `streamer_smartpin_control.yaml` currently documents only the **read**-side pad
and says nothing about the write side at all.

*Submitted:* staged 2026-08-29; delivery to this tree not recorded before 2026-09-19.

### XF-002 · Neighbour routing into a counter works from a plain driven pin — `CONFIRMED`

A counter on P62 routed relative −1 from P61 counted **1,009 of 1,009** driven edges, with a
matched control on P57 ← P56 counting **601 of 601** (2026-08-28). P61 was driven as a **plain
pin** in that arm, not in `P_TRANSITION`.

*Control:* the matched second lane, and two pre-registered self-tests before it — a DC check
following both levels, and 137 driven edges counting 137.

*What it does NOT establish, and they say so:* neighbour-routed capture or counting from a pin
**while that pin runs an output smart-pin mode**. That is the contrast `VO-J-005` exists to settle,
and it remains open. See `XF-003`.

*What it grounds:* the routing half of `architecture/streamer/pin-capture.yaml`'s remedy — that
`A`-input relative routing delivers a real waveform to a non-smart neighbour. The *other* half,
that a smart-pin pin captures as handshake rather than level, is still documentary.

### XF-003 · A live smart pin interferes with the streamer's direct pin read — `CONFIRMED`

Their driver disables the MISO smart pin before every streamer read because the live smart pin
*"interferes with streamer's direct pin reading"* (verified on hardware 2026-01-23). Roughly twenty
bench sessions of an SCK instrument counted *"transitions complete"* flags instead of clock edges.

*Why it is admissible:* both observations are exactly what `pin-capture.yaml`'s
`why_direct_capture_fails` predicts, arrived at independently and expensively.

*What it grounds:* the *direction* of the `in_signal_semantics` claim. It does **not** substitute
for `VO-J-005`, which measures the smart-pin and neighbour lanes **in the same buffer** so the
contrast is one result rather than two runs compared.

### XF-004 · A plain-pin observer counts 4,736 SCK rises per SD sector read — `CONFIRMED`

100 Ω jumper from SCK (P61) to a plain pin (P57); an edge counter reading its own pin counted
**4,736** rises on every one of six reads.

*Why the number is trustworthy:* it decomposes exactly — 512 × 8 = 4,096 data, plus 16 CRC, plus
624 of command, response, token poll and trailing clocks.

*Controls:* two pre-registered self-tests ran first — a DC check following both levels, and 137
driven edges counting 137.

*What it grounds:* nothing in the KB today. Recorded because it is a clean worked example of
instrumenting a bus with a spare pin, and because it is the calibration behind `XF-002`.

---

## Lifecycle

- An `XF-NNN` graded `SCOPED` is **upgraded in place** when a later run closes its scope gap; the
  original scope line stays, marked with what closed it.
- When one of our own runs reproduces an `XF` result, the `EF-NNN` entry cites the `XF` it
  confirms, and the `XF` is marked *confirmed independently by EF-NNN*. Two independent readings
  agreeing is evidence worth recording as such.
- A submission that arrives without meeting the admission bar is recorded `UNGRADED` and the
  missing rule is named, so the submitting project knows exactly what would close it.
