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
*KB:* `language/pasm2/concepts/streamer_smartpin_control.yaml` (the shape only, never the −6 fit)

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
*KB:* `architecture/streamer/pin-capture.yaml`

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
*KB:* `architecture/streamer/pin-capture.yaml`

Their driver disables the MISO smart pin before every streamer read because the live smart pin
*"interferes with streamer's direct pin reading"* (verified on hardware 2026-01-23). Roughly twenty
bench sessions of an SCK instrument counted *"transitions complete"* flags instead of clock edges.

*Why it is admissible:* both observations are exactly what `pin-capture.yaml`'s
`why_direct_capture_fails` predicts, arrived at independently and expensively.

*What it grounds:* the *direction* of the `in_signal_semantics` claim. It does **not** substitute
for `VO-J-005`, which measures the smart-pin and neighbour lanes **in the same buffer** so the
contrast is one result rather than two runs compared.

### XF-004 · A plain-pin observer counts 4,736 SCK rises per SD sector read — `CONFIRMED`
*KB:* not a KB fact — SD-protocol arithmetic and a one-off instrumentation count, not a P2 behaviour

100 Ω jumper from SCK (P61) to a plain pin (P57); an edge counter reading its own pin counted
**4,736** rises on every one of six reads.

*Why the number is trustworthy:* it decomposes exactly — 512 × 8 = 4,096 data, plus 16 CRC, plus
624 of command, response, token poll and trailing clocks.

*Controls:* two pre-registered self-tests ran first — a DC check following both levels, and 137
driven edges counting 137.

*What it grounds:* nothing in the KB today. Recorded because it is a clean worked example of
instrumenting a bus with a spare pin, and because it is the calibration behind `XF-002`.

### From the project's debug and instrumentation write-up — graded 2026-10-13 («#429»)

The project's write-up of its debug techniques (dated 2026-09-08, ingested as `p2-debug-techniques`)
tags many claims *"measured on P2 silicon with a recorded run"*, but carries **no run record**: no
board, attachments or control arm, and a clock only where a claim is about the clock. Every silicon
claim below is therefore `UNGRADED`, with the missing rules named. The project has been asked for the
records (one request, all items); no test of ours is written for any of these until that answer is
in. Claims that were tool behaviour, host-tool behaviour or method, and claims a Parallax document,
an `EF` or `XF-001`–`XF-004` already settles, were not entered (the «#429» grading pass recorded
which). Each entry gives the claim at the project's own scope.

### XF-005 · A formatted number can print as an endless digit run while the value is right — `UNGRADED`
*KB:* not a KB fact — UNGRADED: no run record; nothing in the KB rests on it
A formatted field printed as endless `0_000_…` groups, sometimes with a letter inside the digits;
two consecutive prints of one variable read `0` then `7`; a run passed every assertion and never
reached its end marker because a display was still emitting. *Scope, in their words:* "Each of
these was observed on silicon." *Gap:* rules 1, 2, 3 — no occurrence count, board, clock or log;
rule 4 unknown. Not a VO candidate: a symptom with no named cause.

### XF-006 · The last line is lost if the program ends before the debug transmitter drains — `UNGRADED`
*KB:* not a KB fact — UNGRADED: no run record; nothing in the KB rests on it
A program that printed its end marker or stopped without waiting for the transmitter lost its
final line mid-transmission. *Scope:* one incident ("That cost an audit its whole `STATUS:`
line"). *Gap:* rules 1, 2 — no with/without-drain arm. *VO-P candidate* if no paired run exists: a
bare `-d` program that prints, then ends or stops, with and without the drain.

### XF-007 · A board read as hung was emitting one character about every 98 s — `UNGRADED`
*KB:* not a KB fact — UNGRADED: no run record; nothing in the KB rests on it
Every cog's debug output stopped at the same moment, and the chip kept emitting about one character
per 98 s "across many intervals". *Gap:* rules 1, 2, 3 (given as an example), 4.

### XF-008 · Stopping a worker cog killed debug output mid-word — `UNGRADED`
*KB:* not a KB fact — UNGRADED: no run record; nothing in the KB rests on it
Debug output died mid-word at the call that stopped the driver's worker cog, with no payload lines
after it. *Scope, in their words:* "No mechanism is established." *Gap:* rules 1, 2, 4 (seen as
their driver's stop). *VO-P candidate* after the records: a bare `COGSTOP` of a debug-enabled cog
in a `-d` build, with `DEBUG_COGS` restricted as the control arm.

### XF-009 · A `-d` build adds no per-instruction overhead; timing differences come from layout — `UNGRADED`
*KB:* not a KB fact — UNGRADED: no run record; nothing in the KB rests on it
*Gap:* rules 1, 2 — tagged measured, no run given. *VO-P candidate* if the records are empty
(`EF-034`/`EF-035` show the timing-rig pattern).

### XF-010 · A sync-serial data pin left in smart mode is clocked by a streamer burst on another pin — `UNGRADED`
*KB:* not a KB fact — UNGRADED: no run record; nothing in the KB rests on it
A `P_SYNC_RX` pin's `IN` rises on B-clock edges, not on data; a data pin left in smart mode counts
every clock of a burst it is not part of; a burst that is not a multiple of the word size leaves the
shifter mid-word and misframes every later word until the pin is reset; the reset is `PINFLOAT`
then `WRPIN`/`WXPIN`/`PINH`, while re-arming with `WXPIN`/`WYPIN` or `AKPIN`/`DIRH` is not one.
*Gap:* rules 1, 2, 4 (localised in their driver). *VO-P candidate* for the burst, misframe and
reset claims if no isolated run exists (`EF-017`, `EF-019`, `EF-090` are the nearest rigs).

### XF-011 · `P_HIGH_15K` on an actively driven line is not a substitute for `P_HIGH_FAST` — `UNGRADED`
*KB:* not a KB fact — UNGRADED: no run record; nothing in the KB rests on it
*Gap:* rules 1, 2 — no failing and passing run given.

### XF-012 · On the P2 Edge the boot ROM drives P58–P61 at every reset — `UNGRADED`
*KB:* not a KB fact — UNGRADED: no run record; nothing in the KB rests on it
A device on those pins sees its chip-select toggle with arbitrary data at every reset, and the
flash and microSD roles on P60/P61 are exchanged. *Gap:* rules 1, 2 — no capture given. The ROM
booter listing is the authority for what it drives.

### XF-013 · A streamer count past 16 bits spills into the pin-base field — `UNGRADED`
*KB:* not a KB fact — UNGRADED: no run record; nothing in the KB rests on it
A count of 131,072 gave a different pin base and a count of 0; nothing transferred and `WAITXFI`
never returned. Consistent with `EF-065`'s carry mechanism. *Gap:* rules 1, 2. *VO-P candidate*
if the records are empty.

### XF-014 · A neighbour counter and an independent streamer decode agreed on 4,576 clock edges — `UNGRADED`
*KB:* not a KB fact — UNGRADED: no run record; nothing in the KB rests on it
A counter at relative −3 read 4,576 SCK edges for one transfer, matching a streamer decode of the
same transfer. *Gap:* rules 1, 2 — the subject pin, its smart-pin mode and the board are not given.
If the subject pin was in `P_TRANSITION`, the run bears on `VO-J-005` (see `XF-002`).

### XF-015 · `WAITMS` past `$8000_0000` clocks returns at once — `UNGRADED`
*KB:* not a KB fact — UNGRADED: no run record; nothing in the KB rests on it
`waitms(45_000)` returned in about 250 ms at 350 MHz. The Spin2 v55 documentation states the bound
("duration must not exceed $8000_0000 clocks"), not what happens past it. *Gap:* rule 1 (board),
rule 2.

### XF-016 · Delays and effects do not scale by the clock ratio — `UNGRADED`
*KB:* not a KB fact — UNGRADED: no run record; nothing in the KB rests on it
A delay measured at one sysclk did not scale by the ratio, a step at 350 MHz was absent or inverted
at 300, 250 and 200 MHz, and code layout (42 bytes of dead code) changed which tests passed. *Gap:*
rules 1, 2, 3 (units unnamed), 4. Folds into `XF-001`'s open question (whether the quantity is in
sysclks) and `VO-P-001`.

### XF-017 · A cog stopped while holding a lock frees the lock but not its number — `UNGRADED`
*KB:* `language/spin2/methods/cogstop.yaml` (states the leak on other grounds; this entry grounds nothing until graded)
After sixteen such stops `LOCKNEW` returns −1. The lock state at stop was measured 3 of 3; the leak
itself was never run to exhaustion. *Gap:* rule 1 for the leak. *VO-P candidate* — load-bearing
and with no bench evidence anywhere: stop-leak sixteen times, then `LOCKNEW`, with a `LOCKRET` arm
as the control.

### XF-018 · One hung run can break the next run on the same power-up — `UNGRADED`
*KB:* not a KB fact — UNGRADED: no run record; nothing in the KB rests on it
A byte-identical binary passed 25 of 25 as the first program after a power cycle and was silent as
the fifth. *Gap:* rules 1, 2, 4 — the cause (card or peripheral state) is not isolated.

---

## Lifecycle

- An `XF-NNN` graded `SCOPED` is **upgraded in place** when a later run closes its scope gap; the
  original scope line stays, marked with what closed it.
- When one of our own runs reproduces an `XF` result, the `EF-NNN` entry cites the `XF` it
  confirms, and the `XF` is marked *confirmed independently by EF-NNN*. Two independent readings
  agreeing is evidence worth recording as such.
- A submission that arrives without meeting the admission bar is recorded `UNGRADED` and the
  missing rule is named, so the submitting project knows exactly what would close it.
