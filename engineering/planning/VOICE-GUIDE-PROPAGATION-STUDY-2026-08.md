# Voice-Guide Propagation Study — 2026-08

**Planning artifact (P1)** for `MANUAL-CORRECTIONS-AND-RETIRED-DOC-CLEANUP-SPRINT-PLAN.md`.
**Status:** **DECIDED 2026-08-15 — Stephen approved the tree, the four-rule house layer, the DeSilva
per-row decisions, and the creation-guide rule.** Survey complete for all ten guides plus the
catalog and the app-note guide (read, not grepped). **No guide has been edited; this is research
plus decisions.**

> **§00 — THE SETTLED MODEL (read this before the sections below, which record how we got here).**
>
> **The house layer already existed and already answered the sizing question.** Commit `3d8a653c`
> (2026-07-20) added a normative **"The Shared Discipline — applies to every voice"** section to
> `documentation-voices-catalog.md`, which states the rules and then says *"the write-time
> counterparts live in each manual's voice-guide."* Six of ten guides already cite it as canonical.
> The model is **canonical statement in the catalog, local adaptation in each guide** — not
> "define once and point" and not "copy into eleven".
>
> **Three layers:** house canon (`documentation-voices-catalog.md`) → class
> (`APP-NOTE-VOICE-GUIDE.md`) → document (`<element>/voice-guide.md`). Adjacent files
> (`creation-guide.md`, `style-guide.md`) **may reference voice rules, never restate them.**
>
> **Three structural rules:** (1) never restate a shared rule, adapt it; (2) record rejections with
> reasons; (3) **quality checklists point at rules, never re-encode them** — rule 3 alone would have
> prevented every contradiction in §0 and §0b.
>
> **The house layer goes to FOUR named rules** — the catalog's three and Chip's three are *not the
> same three*. **E2 is missing from the house layer** (it lives only as prose inside the Claude Voice
> failure-mode paragraph) although seven of ten guides carry the rows. Promote it:
>
> | | rule | maps to |
> |---|------|---------|
> | **R1** | Calibrated confidence — never state a claim above its evidence | E1 |
> | **R2** | The payoff-sentence test | E1 (second half) |
> | **R3** | The anti-pattern family — tutorial filler · reader-as-foil · self-admiration · staged reveal | **E2, promoted** |
> | **R4** | Cadence budget — the metronome | E3 |
>
> Every guide declares **ADOPT / ADAPT / REJECT against R1–R4, with a reason**.
>
> **The root cause of every contradiction below, stated once:** *the rule was written by naming
> banned **words** instead of naming the **defect**.* The fix pattern, applied identically
> everywhere: **(1)** name the defect ("vague hedging that avoids commitment"), never a word list;
> **(2)** every restatement site gets a pointer to that guide's calibrated-confidence section;
> **(3)** checklists point, never re-encode. Architect and Getting Started already do all three and
> are the template.

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

## §0b. The propagation is incomplete EVERYWHERE — including in the origin

Reading the four guides that already carry §2.2a shows the element was added as a **section** while
the rest of each guide was never swept. **Every one of them still contains an unreconciled
"no hedging" statement, and three of them have it in their QUALITY CHECKLIST:**

| guide | §2.2a present | residual unreconciled statements |
|-------|---------------|----------------------------------|
| **XBYTE** *(origin)* | ✅ | L47 "no hedging"; **L219 checklist** — "Reference layer: third person, no hedging, no tutorial voice" |
| **Streamer** | ✅ | L61 "no hedging"; **L317 checklist** — "No hedging language ('may,' 'might,' 'probably')" |
| **Assembly** | ✅ (§4.2a) | L16, L57; **L431 checklist** — "No hedging language ('may,' 'might,' 'probably,' 'typically')" |
| IOSP | ✗ | §3.2 rule + §3.3 cell |
| Debug Window | ✗ | §3.2 rule + §3.3 cell |

**The checklist instances are the dangerous ones.** A quality checklist is what an auditor runs
mechanically. One that says *"No hedging language ('may', 'might', 'probably', 'typically')"*
instructs an auditor to strip exactly the calibrated qualifiers §2.2a requires — so the guide
contains its own counter-order, and the mechanical half wins.

**The correct pattern already exists**, in the Assembly guide's §4.2 table:

> | Never write **vague** hedging | "The C flag may be set" ❌ | Creates ambiguity about what the
> silicon does. **NOT the same as a calibrated qualifier — see §4.2a** |

Scoped to *vague* hedging, with a cross-reference. Follow it.

**Consequence for the work.** The E1 task is **not** "add §2.2a". It is:

1. add (or reconcile) §2.2a, **and**
2. sweep **every** hedging statement in that guide — philosophy bullets, register descriptions,
   voice-comparison cells, and above all the quality checklist — scoping each to *vague* hedging
   with a cross-reference to §2.2a.

**This adds a target the sprint was not counting: the XBYTE guide itself.** It is where the element
was authored and it has the same residual conflict.

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
| **Staged reveal** ("and here is the trap", "Hold that result") | **DECIDED 2026-08-15 — ADOPT the defect, REJECT the phrase list** | Measured against the shipped master rather than reasoned from the style guide. See **§0e** below. |

| element | decision | reason |
|---------|----------|--------|
| **E1** | **ADOPT** | Accuracy is register-independent, and a tutorial's worked examples are exactly where an overstated claim reaches a beginner. DeSilva may be our most §2.2a-native voice already: *"Acknowledge complexity: 'This is tricky, and that's okay'"* is calibration, and the persona is explicitly *"sometimes-wrong-but-honest"*. ⚠ Scope it to **technical claims about the P2** — not to the voice's playful self-assessment, which is a different act. |
| **E3** | **REJECT** | Two reasons, both from the sources. (1) **E3's own carve-out applies:** *"A declared refrain is not a beat. A deliberate, announced structural device … is structure, not cadence drift — keep it."* DeSilva's Chapter End boxes and celebration moments are exactly that — declared, structural, and documented in the style guide's box-type list. (2) The rationale document defends emotional punctuation as pedagogy (Emotional Design; achievement milestones), so a budget that thins it trades a documented learning benefit for a cadence metric. |

### §0e. DeSilva staged reveal — decided on measurement

**The row is self-inconsistent at the source.** In XBYTE it names a *defect* in its "Why" column
(*"withholding a fact to manufacture a beat"*) but bans *phrases* in its "Avoid" column. That is the
identical mistake §0/§0b exist to fix, and rejecting the whole row would have let it stand here.

**What the shipped text does.** Every reveal-vocabulary hit in `COMPLETE-OPUS-MASTER.md` (6,176
lines) was located and then **read in context**. Three real candidates:

| site | text | verdict |
|------|------|---------|
| `:1151` | Heading **"When does _RET_ NOT return?"** → *"Here's the catch: if the instruction itself branches, no return happens."* | **Not a defect.** The heading announces the topic; the fact lands in the same sentence. A signpost, not withholding. |
| `:167` | *"…you're probably right… but here's the secret: it's actually simpler than traditional architectures"* | **Not staged reveal** (payoff in the same sentence). **But it IS an R1 hit** — an unsourced comparative claim. |
| `:5824` | Epilogue: *"But here's the secret: everything you've learned is just the foundation."* | **Protected** — declared crescendo in the send-off, the same carve-out Architect gets for *"So go build something."* |

**Zero instances of the actual defect.** Not one place where a fact is held back across a paragraph
or section boundary to land a beat. The vocabulary appears three times; the behaviour appears never.

**Decision — the wording for DeSilva's voice guide:**

> **Staged reveal — adopted as a defect, not as a phrase ban.** Never withhold a fact *across* a
> paragraph or section boundary so its arrival lands a beat. Announced signposts ("Here's the
> catch:") followed immediately by the fact are **structure**, and the style guide's *"Show before
> explaining"* sequencing is **pedagogy** — neither is staged reveal. **The test is distance:** if
> the fact arrives in the same breath as the signpost, it is a signpost.

**Why this beats "reject as written".** A blanket rejection applies a standard to DeSilva we have
just rejected everywhere else (ban the words, not the defect), and it leaves the real defect
uncovered — which, by this study's own rule, invites the next sweep to re-add the row unread.

**Carried to Sprint 2:** `:167`'s comparative claim is a genuine R1 finding in released DeSilva
text. It shows R1 adoption there has real bite rather than being a formality.

**Standing caution for this manual.** `why-desilva-voice-works.md` carries an explicit
*"DON'T Add These Modern 'Improvements'"* list — learning-objective boxes, formal assessment
questions, rigid structural requirements, academic citations in the main text. Any future
propagation into this guide should be checked against that list first; it exists because the
manual has been "improved" before.

### Complete current-state survey — all ten guides *(read, not grepped)*

| guide | E1 present | E1 **reconciled** elsewhere? | E2 rows | E3 | residual severity |
|-------|-----------|------------------------------|---------|----|-------------------|
| **Streamer** | ✅ §2.2a | ✗ L61 · **L317 checklist is a WORD BLACKLIST** | ✅ 3 | ✅ §2.4 | 🔴 **CRITICAL** |
| **Assembly** | ✅ §4.2a | partial — L183 row reconciled ✅, but L16, L57 and **L431 checklist WORD BLACKLIST** | ✅ 3 | ✅ §4.4 | 🔴 **CRITICAL** |
| **IOSP** | ✗ none | ✗ explicit *"Never hedge"* rule §3.2 + §3.3 cell | ✗ 0 | ✗ | 🟠 **HIGH** |
| **Debug Window** | ✗ none | ✗ same, inherited from IOSP | ✗ 0 | ✗ | 🟠 **HIGH** |
| **XBYTE** *(origin)* | ✅ §2.2a | ✗ L47 · L219 checklist (unscoped, no word list) | ✅ 3 | ✅ §2.4 | 🟡 MEDIUM |
| **Single-Step Debugger** | ✅ section | ✗ Tone bullet | ✅ 3 | **✅ present** *(corrected)* | 🟡 MEDIUM |
| **PNut-Term-TS** | ✅ section | ✗ Tone bullet | ✅ 3 | **✅ present** *(corrected)* | 🟡 MEDIUM |
| **Architect** | ✅ bullet (§2.6) | ✅ L75 row reconciled · L237 checklist scoped "on facts" | ✅ 3 | ✗ | 🟢 LOW |
| **Getting Started** | ✅ bullet (§2.4) | ✅ L77 row reconciled · L180 checklist scoped | ✅ 3 | ✗ | 🟢 LOW |
| **DeSilva** | ✗ | n/a | 2 adopt / 2 reject | **reject** | — see decision above |
| Smart Pins Tutorial | ✗ | not surveyed in depth | ✗ | ✗ | retiring (§5) — decide whether it gains anything at all |

*Correction to my own earlier count:* Architect and Getting Started **do** carry all three E2 rows.
They write "Reader-as-foil" where XBYTE writes "besserwisser", so the keyword survey undercounted
them. Third time grep misled in this study.

#### The severity ladder for the E1 residual

1. 🔴 **Word blacklists in a quality checklist** — Streamer L317 *("may," "might," "probably")*,
   Assembly L431 *(adds "typically")*. These name **the exact words §2.2a requires**. An auditor
   running the checklist mechanically will delete calibrated qualifiers as defects.
2. 🟠 **An explicit "Never hedge" rule with no §2.2a at all** — IOSP, Debug Window. The guide gives
   only the older, absolute instruction.
3. 🟡 **Unreconciled register descriptions** — XBYTE, Single-Step, PNut-Term-TS. A reader who finds
   §2.2a is fine; one who reads only the register summary is not.
4. 🟢 **Already correct** — Architect and Getting Started.

#### The model is Architect / Getting Started, not Assembly

Assembly reconciles its *rule row* but leaves a word blacklist in its checklist. Architect and
Getting Started do both: the rule row carries *"keep **calibrated** qualifiers where true — §2.6"*,
**and** the checklist is scoped to *"No hedging **on facts**"* rather than listing banned words.
**Use their pattern as the template for the E1 sweep.**

#### E3 / R4 gap — **corrected 2026-08-15**

Present in **five**: Streamer, Assembly, XBYTE, **Single-Step, PNut-Term-TS**. Commit `04f6e4e2`
(2026-08-11, *"Voice guides: adopt the shared narrative discipline in SSDB and PNut-Term-TS"*) gave
both the full three-guard section four days before this study ran; the table above originally
recorded them as absent. **Absent in Architect, Getting Started, IOSP, Debug Window.** Rejected for
DeSilva (reasons recorded above).

*That is the fourth time a keyword pass misled in this study.* Both guides drop to a one-line fix.

---

## §0c. The full site inventory — 21 unreconciled sites across 8 guides

Counted by reading every guide end to end, not by headline. This is the Sprint 1 work list for R1.

| guide | sites | severity | where |
|-------|-------|----------|-------|
| **IOSP** | **5** | 🔴 | §2.1 bans **"typically sets"** by name · §3.2 rule row · §3.3 comparison cell · §6 checklist · §7 summary. No R1 anywhere. |
| **Debug Window** | **5** | 🔴 | header note · §2.1 bans **"typically scrolls"** by name · §3.2 rule row · §3.3 cell · §7 checklist. Inherited from IOSP. |
| **Assembly** | **3** | 🔴 | §7 checklist **word list incl. "typically"** · §1.1 · §2.1. (§4.2 row and §4.3 cell already reconciled — half-fixed.) |
| **Streamer** | **2** | 🔴 | §7 checklist word list · §1.4 register description. |
| **XBYTE** *(origin)* | **2** | 🟡 | §1.4 · §6 checklist. **Also the only guide that never cites the catalog.** |
| **App-note guide** | **2** | 🟠 | **§3.2 labels "You might wonder whether…" as *Hedging*** — the exact conflation R1 exists to prevent · §1 register description. |
| **Single-Step** | **1** | 🟡 | Tone bullet only. |
| **PNut-Term-TS** | **1** | 🟡 | Tone bullet only. |
| Architect · Getting Started | **0** | 🟢 | The template. |

**Severity revision.** IOSP and Debug Window rise to 🔴 alongside the checklists. Their §2.1 lines do
not merely ban a category — they ban **"typically"** *by name*, in the voice-characteristics section
an author reads first. That is the same defect as a checklist word list, one section earlier.

**The app-note guide is 🟠 for reach, not count.** It governs every `P2ANxxx` including **P2AN002, a
Sprint 2 correction target**, and its single mislabelled row teaches the conflation directly.

---

## §0d. Collateral defects found while reading — not R1/R4, but surfaced

Per the every-commit-raises-quality rule these are recorded rather than dropped. All are in files
Sprint 1 opens anyway, except the last.

| # | file | defect |
|---|------|--------|
| 1 | Assembly `voice-guide.md` §7 | Checklist says *"Operation describes step-by-step behavior"* — but **§6.3 explicitly supersedes** the step-by-step Operation idea and forbids it (*"❌ A procedural 1-2-3-4 step list"*). **Same failure shape as the hedging rows: the checklist was not swept when the rule changed.** |
| 2 | Assembly `voice-guide.md` §6.6 | Example prose reads *"within the **COG**'s ALU"* — all-caps COG, which **§5.1 of the same file** calls out as never correct. |
| 3 | IOSP `voice-guide.md` §3.3 | Comparison column headed *"Green Book Tutorial"* — a **codename**, against our official-titles rule. |
| 4 | `desilva-style-guide.md` | **Self-contradictory on a colour:** the body specifies Medicine Cabinet as tan/beige (`#FFF8F0`/`#D2A679`); the v1.2.0 change log says it changed to cyan (`#E0F7FA`/`#00ACC1`). One is stale. **Presentation, not voice — out of Sprint 1 scope**, recorded here so it is not lost. |

Defect 1 is the most significant: it is independent evidence that **checklist drift is the failure
mode of this repo's guides**, not a one-off in the hedging rules. It is the strongest argument for
structural rule 3 (*checklists point, never re-encode*).

---

## Damage assessment — a task for P2, arising from §0b

The word-blacklist checklists are not merely inconsistent; they may already have **caused** edits.

**The question:** has any `document-audit` or `document-finalize` pass run against the Streamer or
Assembly checklists since §2.2a was added, and did it remove calibrated qualifiers from shipped
text as "hedging"?

Both manuals are **released** — Streamer v1.0.8, Assembly v3.1.5 — and Assembly's list includes
**"typically"**, which is among the commonest legitimate qualifiers in a hardware reference.

**Why it matters.** That would be a defect *we* introduced, in the opposite direction from the one
this sprint is fixing: text made **less** accurate by an over-broad rule. It is exactly the failure
§2.2a exists to prevent, delivered by the guide that contains §2.2a.

**Method (P2, research only):** identify audit/finalize passes on those two manuals after
`acf3b4a2` (2026-07-20); check their findings for hedging-language items; where found, check the
diff for qualifier removals against claims whose evidence was genuinely partial. Report count and
severity. **No edits during planning.**

---

## Feeding P2

Each decision above sets the standard P2 measures against:

1. **IOSP** — measure `#4c` beat rate; expect near-zero. Confirm.
2. **Debug Window** — measure first; and count the *pre-existing* Discovery-Guide debt separately
   from anything this sweep introduces.
3. **DeSilva** — **no cadence measurement**; E3 is rejected. Measure E1 (technical claims above their evidence) and the two adopted E2 rows only.
4. All targets — the E1 reconciliation is a guide edit, not a text edit; it changes what P2 counts
   as a defect (a qualifier is no longer one).
5. **Re-check any manual already audited against a checklist carrying the unscoped no-hedging
   line.** If an audit or finalize pass has already run against XBYTE, Streamer or Assembly using
   those checklists, calibrated qualifiers may have been stripped from shipped text as "defects".
   P2 should look for that specifically — it would be a defect we introduced, in the opposite
   direction from the one we are fixing.


---

## What we do NOT know — the honest gap list

The survey above covers **per-manual `voice-guide.md` files only**. That is one layer of three, and
the other two are unexamined.

> **Updated 2026-08-15.** Two of the three unexamined artifacts below have now been **read**, and the
> catalog turned out to answer the sizing question outright (§00). What remains genuinely unexamined
> is the **creation-guide layer** — eleven files, the next study. Gap-list item 3 (DeSilva staged
> reveal) is **resolved** in §0e.

### Newly found this pass — changes the shape of the work

| artifact | status | why it matters |
|----------|--------|----------------|
| `engineering/standards/documentation-standards/documentation-voices-catalog.md` | **last touched 2026-07-20 — the same day as the XBYTE tweaks** | It is a **house-level** catalog of voices with failure modes, and its Chip Voice entry already carries an E1-flavoured guard: *"false precision — a derived/measured value stated as if it were spec. Guard: state numbers only at their source's confidence."* **We do not know whether the intended model is "define once in the catalog, reference from each guide" or "copy into all ten."** That decision determines whether the E1 work is one edit plus pointers, or eleven parallel edits. |
| `engineering/document-production/app-notes/APP-NOTE-VOICE-GUIDE.md` | **E1 ✗ E2 ✗ E3 ✗ — at zero** | Governs **every** `P2ANxxx`, including **P2AN002 — a correction target in this sprint**. This is an **11th target** the study did not have. |
| every manual's `creation-guide.md` | **unexamined** | All eleven carry voice/tone content (3–14 hits each). A voice rule living there can contradict the voice guide exactly as the quality checklists do. This is a whole second layer, and we found the checklist conflict only by reading. |
| `engineering/document-production/repo-voice-profile.md` | **ruled out** | Not a manual standard — it profiles Stephen's voice for the X/Patreon work. Noted so nobody re-investigates it. |

### Still unknown, unmeasured

1. **Whether the damage occurred.** The Streamer/Assembly word blacklists *may* have caused
   qualifier removals in released text. Hypothesis only; nothing measured.
2. **How far any manual's TEXT sits from its guide.** P2 has not run. Zero measurements exist —
   including Debug Window's self-declared *"substantial rewrite"*, which has no count attached.
3. **DeSilva's staged-reveal row** — recorded as a judgement call, still undecided.
4. **Whether other manuals received reviewer voice feedback that never propagated.** Chip's critique
   reached the XBYTE guide. We do not know whether any other manual has an equivalent input sitting
   unapplied.
5. **What Chip's full critique said.** We have three distilled tweaks. Whether the original raised
   more that was never captured is unknown.
6. **Whether voice conformance is enforced at any gate.** `document-audit` Dimension #9 exists;
   whether it runs per release is unverified. If it does not, guides drift unchecked — which is how
   we got here.
7. **Smart Pins Tutorial's three style documents** — not surveyed. It is being retired, but we do
   not know whether other guides reference it.

### Do we need to go deeper per document?

**Yes at the house layer, now. Not yet at manual text.**

- **Now:** the voices catalog and the app-note voice guide. Both are cheap, and the catalog may
  collapse eleven edits into one plus pointers — doing per-manual work before settling that risks
  building the wrong thing eleven times.
- **Now:** a creation-guide pass for the manuals we are correcting, looking specifically for voice
  rules that contradict the voice guide. Same failure shape as the checklists, and we already know
  that shape exists here.
- **Not yet:** per-manual text depth. That is P2, and it cannot run until the guides are settled —
  measuring text against a standard we are about to change wastes the measurement.
