# Voice-Guide Propagation Study — 2026-08

**Planning artifact (P1)** for `MANUAL-CORRECTIONS-AND-RETIRED-DOC-CLEANUP-SPRINT-PLAN.md`.
**Status:** in progress — IOSP and Debug Window decided; DeSilva and the partial set pending.

**Purpose.** The XBYTE guide's 2026-07-20 audit produced three voice-guide changes. They have been
propagating outward unevenly. This study decides, **per gaining guide**, which elements are
**adopted**, **adapted**, or **rejected** — with reasons, because an undocumented rejection reads
as an oversight and gets "fixed" by the next sweep.

**Method.** Read each target guide's identity and rules sections against the source elements. Do
not grep — the earlier keyword survey said *where to look*, not *what is there*, and it missed the
conflict in §0 below entirely.

**Scope.** All ten guides, not only those this sprint edits.

---

## §0. The finding that changes how propagation must be done

**Two guides already carry a rule that §2.2a corrects.**

`p2-io-and-smart-pins-user-guide/voice-guide.md` §3.2:

> | Never hedge | "The pin might be driven" ❌ | Creates ambiguity |

and §3.3 Voice Comparison lists **Hedging: Never**. `p2-debug-window-manual/voice-guide.md` §3.2
carries the same rule, inherited (its header states it is derived from the IOSP guide).

XBYTE §2.2a says the opposite where evidence is partial:

> Banning tutorial filler … does **not** mean banning *uncertainty*. A qualifier that reflects the
> true state of the evidence … is **accuracy**, not hedging, and it is **required** wherever the
> unqualified claim would overstate. … **never state a claim above its evidence.**

**Consequence.** Appending §2.2a to these guides would leave each self-contradictory, and an author
obeying the older rule would strip exactly the qualifiers that keep claims honest. **Propagation of
§2.2a into IOSP and Debug Window is a RECONCILIATION, not an addition** — the existing "Never
hedge" row must be rewritten in the same edit.

This is also the sprint's own lesson turned on the guides: our bench leg exists because claims
outran evidence. A rule that forbids qualification *causes* that failure.

---

## The three source elements

From `acf3b4a2`, *"XBYTE voice-guide: three tweaks from Chip's voice critique"*:

| # | element | nature |
|---|---------|--------|
| **E1** | **§2.2a Calibrated confidence is required — it is not hedging.** "Never state a claim above its evidence." | **accuracy** |
| **E2** | **Anti-pattern rows** — tutorial filler · reader-as-foil ("besserwisser") · self-admiration · staged reveal | **register** |
| **E3** | **§2.4 Cadence budget** — ≤ ~half of section closings may be beats; never > ~4 in a row; chapter closers worst; a declared refrain is not a beat; protect earned beats | **register** |

## The discriminator

- **Accuracy elements (E1) propagate everywhere, including highly stylized manuals.** Truthfulness
  is not a register choice. A warm tutorial must no more overstate than a reference does.
- **Register elements (E2, E3) are voice-dependent** and must be judged per manual.

**The source guide already models this.** XBYTE's own §2.3 Voice Comparison table lists DeSilva
with *"Tutorial filler: Occasional"* and *"Celebration: Yes ('Uff!')"* — the origin document
explicitly treats DeSilva as a different register rather than a document to be brought into line.

---

## Decisions

### I/O & Smart Pins User Guide — *reference voice, third person*

Identity: "practical reference … authoritative · precise · comprehensive · practical", third
person, multiple entry points.

| element | decision | notes |
|---------|----------|-------|
| **E1** | **ADOPT — as a reconciliation** | Add §2.2a **and rewrite** the §3.2 "Never hedge" row plus the §3.3 "Hedging: Never" cell in the same edit. Proposed replacement rule: *never hedge to avoid commitment; do qualify where the evidence is genuinely partial.* Keep the existing bad example ("The pin might be driven" — an unqualified fact stated weakly) and add a good one, so the distinction is visible rather than asserted. |
| **E2** | **ADOPT — adapted** | IOSP already bans tutorial filler, conversational voice and minimizing. **Reader-as-foil, self-admiration and staged reveal are not covered.** All three are consistent with an authoritative third-person register. Adapt the examples to the I/O domain rather than importing XBYTE's. |
| **E3** | **ADOPT as a forward guard** | Reference-voice, mode-per-chapter documents are the class `#4c` fleet data found *does not* produce this defect. Adopt so future prose — including our F-261 edits — cannot drift, while expecting near-zero legacy findings. **P2 confirms by measurement; do not assume in either direction.** |

### Debug Window Manual — *IOSP model, second person*

Its guide states it is derived from IOSP with one deliberate divergence (second person), keeping
"all of IOSP's other disciplines … voice rigor is independent of grammatical person."

| element | decision | notes |
|---------|----------|-------|
| **E1** | **ADOPT — as a reconciliation** | Same conflict, inherited. Same fix, second person. |
| **E2** | **ADOPT — adapted** | Its §3.2 already bans marketing/superlatives, celebration and chattiness — a stricter starting point than IOSP because of its history (below). Reader-as-foil, self-admiration and staged reveal still absent; add them. |
| **E3** | **ADOPT — and measure early** | **Higher risk than IOSP.** Second person plus an onboarding job is the combination that produces closing beats. Rank this manual first in P2's `#4c` measurement. |

> **Pre-existing scope, NOT created by this sweep.** The Debug Window voice guide carries a
> migration note: the shipped v2 master was written in an enthusiastic "Discovery Guide" voice
> ("Revolutionary," "20× faster," "rivals \$10,000 equipment," "Debug Iceberg Effect"), which it
> calls **out of conformance with the entire house standard**, adding that *"bringing v2 into
> conformance … is a substantial rewrite."* **This is a known, pre-existing debt.** Our F-262 fix
> is a small table correction and must conform to the new guide; the legacy rewrite is a separate
> project and must not be silently absorbed into this sprint. P2 counts them separately.

### DeSilva PASM2 Tutorial — *highly stylized, deliberate voice* · **PENDING**

Do not decide from reputation. Required reading before deciding: `desilva-style-guide.md` and
`why-desilva-voice-works.md`.

**Working hypothesis, to be confirmed or overturned by that reading:**

- **E1 — adopt.** Accuracy is register-independent, and the tutorial's worked examples are exactly
  where an overstated claim reaches a beginner. This one likely needs adapting in *wording* (its
  guide will not have a §2.2a to slot beside) but not in *substance*.
- **E2 — likely reject, in part.** Reader-as-foil and staged reveal may be constitutive of the
  deSilva voice ("Uff!", direct address, the deliberate set-up-then-reveal). Self-admiration is a
  different matter and may still be unwanted. **Decide per anti-pattern, not as a block.**
- **E3 — likely reject.** A cadence budget imposed on a deliberately rhythmic tutorial would flatten
  the quality the manual is valued for.

Whatever is rejected must be recorded here **with its reason**, so a later sweep does not undo it.

### Remaining targets — **PENDING**

| guide | current state | note |
|-------|---------------|------|
| Streamer | E1 ✅ E2 ✅ E3 ✅ | verify by reading; it is a correction target |
| Assembly | E1 ✅ E2 ✅ E3 ✅ | verify; more anti-pattern hits than XBYTE — local additions or reworded duplicates? |
| Architect | E1 ✅ E2 ✅ **E3 ✗** | finish |
| Getting Started | E1 ✅ E2 ✅ **E3 ✗** | finish |
| Single-Step Debugger | E1 ✅ E2 ✅ **E3 ✗** | finish |
| PNut-Term-TS | E1 ✅ E2 ✅ **E3 ✗** | finish |
| Smart Pins Tutorial | not surveyed | has `style-guide.md` + `presentation-style-guide.md`; being retired (sprint §5) — decide whether it gains anything at all |

The ✅/✗ above are **keyword-survey results and must be confirmed by reading.** §0 is the proof
that grep misses what matters: neither IOSP nor Debug Window showed a conflict at keyword level,
and both contain one.

---

## Feeding P2

Each decision above sets the standard P2 measures against:

1. **IOSP** — measure `#4c` beat rate; expect near-zero. Confirm.
2. **Debug Window** — measure first; and count the *pre-existing* Discovery-Guide debt separately
   from anything this sweep introduces.
3. **DeSilva** — no cadence measurement unless E3 is adopted, which is unlikely.
4. All targets — the E1 reconciliation is a guide edit, not a text edit; it changes what P2 counts
   as a defect (a qualifier is no longer one).
