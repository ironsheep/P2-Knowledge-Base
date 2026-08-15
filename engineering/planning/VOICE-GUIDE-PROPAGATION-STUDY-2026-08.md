# Voice-Guide Propagation Study — 2026-08

**Planning artifact (P1)** for `MANUAL-CORRECTIONS-AND-RETIRED-DOC-CLEANUP-SPRINT-PLAN.md`.
**Status:** in progress — IOSP, Debug Window and DeSilva decided; the partial set and the two "full" guides pending verification.

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

### DeSilva PASM2 Tutorial — *highly stylized, deliberate voice* · **DECIDED**

**Read:** `desilva-style-guide.md` (Writing Voice §), `why-desilva-voice-works.md` (a pedagogical
defence of the voice with research citations; its own summary: *"His 'flaws' are features that
reduce cognitive load, build trust, and improve retention"*).

**My working hypothesis was partly wrong.** I predicted E2 would largely reject. The evidence says
two of its four anti-patterns *reinforce* rules DeSilva already has, and the two that reject are
different ones. Deciding this from reputation would have got it backwards.

**E2 must be decided per anti-pattern, not as a block:**

| anti-pattern | decision | evidence |
|--------------|----------|----------|
| **Tutorial filler** ("you might wonder", "let's explore") | **REJECT** | XBYTE's own §2.3 table lists DeSilva as *"Tutorial filler: Occasional"* — the origin document permits it here. It is the register. |
| **Reader-as-foil** ("the obvious way to think about X is wrong", "it is tempting to…") | **ADOPT** | DeSilva's style guide already states **"No condescension: Respect reader intelligence."** Reader-as-foil *is* condescension — the besserwisser tells the reader what they think, then corrects them. This element **reinforces an existing DeSilva principle.** ⚠ Adapt the wording so *gentle prerequisite checks with escape routes* — an explicitly preserved element — are not caught by it. Those offer the reader an exit; they do not correct a belief imputed to them. |
| **Self-admiration** (text praising its subject or its own explanation) | **ADOPT — adapted** | DeSilva celebrates the **reader's** achievement ("Uff!" = shared relief, "emotional punctuation", verdict *"✅ HELPS"*), which is a different act from the text admiring itself. Adopt, and state the carve-out explicitly so celebration of reader progress survives untouched. |
| **Staged reveal** ("and here is the trap", "Hold that result") | **REJECT as written — judgement call, flag for Stephen** | The tutorial's pedagogy is *"Show before explaining"* and *"Conversational responsiveness"*, which is sequencing in service of learning, not withholding to manufacture a beat. The two are hard to separate by rule. Recommend rejecting the row rather than risk flattening the pedagogy, while noting the underlying concern (withholding *purely* for effect) remains covered by E1 — an unstaged fact cannot be overstated. |

| element | decision | reason |
|---------|----------|--------|
| **E1** | **ADOPT** | Accuracy is register-independent, and a tutorial's worked examples are exactly where an overstated claim reaches a beginner. DeSilva may be our most §2.2a-native voice already: *"Acknowledge complexity: 'This is tricky, and that's okay'"* is calibration, and the persona is explicitly *"sometimes-wrong-but-honest"*. ⚠ Scope it to **technical claims about the P2** — not to the voice's playful self-assessment, which is a different act. |
| **E3** | **REJECT** | Two reasons, both from the sources. (1) **E3's own carve-out applies:** *"A declared refrain is not a beat. A deliberate, announced structural device … is structure, not cadence drift — keep it."* DeSilva's Chapter End boxes and celebration moments are exactly that — declared, structural, and documented in the style guide's box-type list. (2) The rationale document defends emotional punctuation as pedagogy (Emotional Design; achievement milestones), so a budget that thins it trades a documented learning benefit for a cadence metric. |

**Standing caution for this manual.** `why-desilva-voice-works.md` carries an explicit
*"DON'T Add These Modern 'Improvements'"* list — learning-objective boxes, formal assessment
questions, rigid structural requirements, academic citations in the main text. Any future
propagation into this guide should be checked against that list first; it exists because the
manual has been "improved" before.

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
3. **DeSilva** — **no cadence measurement**; E3 is rejected. Measure E1 (technical claims above their evidence) and the two adopted E2 rows only.
4. All targets — the E1 reconciliation is a guide edit, not a text edit; it changes what P2 counts
   as a defect (a qualifier is no longer one).
