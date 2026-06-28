# Sprint Plan — Smart-Pin ADC Foundation + P2AN000 Instrumentation-ADC App Note

**Authored:** 2026-06-27 · **Status:** ✅ CLOSED 2026-06-28 — all tasks #121–#128 SHIPPED.
Closeout audit: `engineering/history/sprints/smartpin-adc-foundation-p2an000/2026-06-28-smartpin-adc-foundation-p2an000-CLOSEOUT.md`.
**Heads touched:** yaml (P2KB) · ingestion (donor hygiene) · manual (IOSP enrichment, app-note doc class) · operations (corrections register, validator, punch list)
**Plan dir:** `engineering/planning/` · **This is a PLAN** (commits to ship), not a study.

---

## 0. Scope, consent, sequencing

Scope is **pre-consented** (Stephen, 2026-06-27): Layers 1–4 below. This plan exists to be
executed rigorously via `plan-to-tasks` → `task-execution`; it is **not** an approval gate.

**Origin.** Studying Chip Gracey's "Improved ADC Pin Techniques" forum thread (captured +
classified under `engineering/document-production/app-notes/P2AN000/research/improved-adc-pin-techniques/`)
revealed that (a) the P2 ADC's instrumentation *ceiling* is real and under-documented, and
(b) a long-recurring ADC-encoding defect has a structural root cause. This sprint fixes the
foundation (YAML + IOSP guide) and ships the application (the app note) so the two reinforce.

**Cross-head dependency & sequencing.** The app note (Layer 3) rests on the enriched IOSP
foundation (Layer 2) and the corrected YAML (Layer 1). **Execution order: §1/§3/§4 (YAML/source
hygiene) → §5 (IOSP foundation) → §6 (app note) → §7 (guide) → §8 (rig readiness).** §2 is
DROPPED (see Entry checks). §7 is process-only and may land anytime.

**Authority order** (per the corrections register): `pnut_ts` compiler → Spin2 v55 docs
(`engineering/ingestion/sources/spin2-v55/`) → Silicon Doc v35
(`engineering/ingestion/sources/silicon-doc/`). The ADC encoding is **confirmed identical**
across Silicon Doc v35 and Spin2 v55 — no authority conflict.

**Ground truth (locked, cited).**
`silicon-doc/part4-smart-pins.txt:816` — "WXPIN sets the mode to X[5:4] and the sample period
to POWER(2, X[3:0])." `:820-821` — **X[5:4]: %00 = SINC2 Sampling · %01 = SINC2 Filtering ·
%10 = SINC3 Filtering · %11 = Bitstream capturing.** Spin2 v55: `P_ADC` (%11000), `P_ADC_EXT`
(%11001), `P_ADC_SCOPE` (%11010). **`P_ADC_CAL` exists in NO authoritative source — it is a
fabrication.**

---

## Entry checks (sprint-start, 2026-06-28)

- **Working tree:** committed in 3 commits (`75aeca21`, `571f5a40`, `e5692209`). Only the
  pre-existing datasheet refactor remains — **outside the sprint blast radius, left untouched.**
- **Entry baseline (YAML head): GREEN** — `verify-yaml-format.py` 1053/1053 parse clean;
  `validate-crossref-keys.py` ALL cross-references resolved. This is the exit comparison point.
- **Tracking:** nothing to archive. 4 leftover tasks (`#110` doc-style-change close; `#54/#46/#47`
  IOSP Titus-expert/RECOMMEND_ADD/audit) — **all DEFERRED** (not this sprint). **Adjacency:**
  `#54` Q2 (scope Tukey/Hann taps) + Q5 (DAC-ENOB) neighbor our Ch.16 work + the Goertzel
  punch-list item — our edits must not contradict those pending Chip answers.
- **Build numbers (per head): NO immediate releases.** IOSP — unreleased pilot, **no bump**
  (rides first release, per task `#110` rule). P2KB YAML — **no bump** (verify-lock is
  confirm-only; donor/F-170/guard are hygiene, not a release). Ingestion donor — versionless.
  **P2AN000 — born v0.1.0** (drafted/staged, not released this sprint).
- **§2 DROPPED (Green Book retired).** `P_ADC_CAL` exists only in the retired Green Book
  tutorial + its test doc; IOSP (going-forward) + the YAML already use `P_ADC_SCOPE`. No
  going-forward conflict; retired docs are not maintained. (Stephen, 2026-06-28: "Any Smart
  Pins manual reference going forward is our IOSP.")

---

## Design decisions (resolved by recommendation — redirect any before §1 starts)

Per the sprint-plan overlay, the non-obvious calls, each with the answer this plan takes:

- **D1 — `P_ADC_CAL` fix scope (RESOLVED 2026-06-28 → §2 DROPPED).** The fabricated
  `P_ADC_CAL` exists ONLY in the retired **Green Book** Smart Pins Tutorial
  (`p2-smart-pins-tutorial`, parked / superseded / not going forward) + its green-book test
  doc. The going-forward smart-pins doc is **IOSP**, already correct (`P_ADC_SCOPE`); the YAML
  is uniformly `P_ADC_SCOPE`. We do not maintain retired docs and no going-forward conflict
  exists — so the fix is not performed.
- **D2 — Where does the durable guard live (we must not modify central skills)?**
  **Recommendation (taken):** (a) `F-170` corrections-register entry as the permanent record +
  fix-trace; (b) a new in-repo validator `engineering/tools/validation/audit-adc-encoding.py`
  asserting donor == published == silicon for the X[5:4] map; (c) the central `release-yamls`
  certification-checklist line is a **skill-evolution candidate** (appended to
  `feedback_skill_evolution_candidates.md`), NOT a central-skill edit.
- **D3 — App-note recipe clock (must be ≤300 MHz; Chip's code is 320 MHz).**
  **Recommendation (taken):** standardize all recipes at **`_clkfreq = 200_000_000`** — legal,
  matches existing KB ADC examples (`p2kbArchSmartPin11000…`), clean power-of-2 period math.
- **D4 — Ratiometric content placement in IOSP Ch.16.**
  **Recommendation (taken):** a **dedicated new subsection** ("Ratiometric / Absolute-Voltage
  Instrumentation") after the mode-mechanics material, not folded into §16.8 Accuracy — it is
  a technique, not a caveat.
- **D5 — Does IOSP duplicate the app-note code?**
  **Recommendation (taken):** IOSP shows a **minimal illustrative** ratiometric snippet (the
  3-source read + the math) in its existing example style; the **app note owns the complete,
  runnable builds**. App note references IOSP; no duplication.
- **D6 — App-note recipe scaffolding.**
  **Recommendation (taken):** factor ONE shared test harness (DEBUG SCOPE in µV + the DAC
  loopback test-signal generator) that every recipe reuses; recipes differ only in the ADC
  core. No copy-pasted harness per recipe.

No blocking open questions remain.

---

## File table

| File | Action | Layer |
|---|---|---|
| `engineering/ingestion/smart-pins-catalog/ingestionSources/mode-11000-adc-internal-clock/smart-pin-11000-adc-internal-clock-concise.yaml` | **fix donor** X[5:4] encoding (L26-29, L153-154) | 1 |
| `deliverables/ai/P2/architecture/smart-pins/smart-pin-11000-adc-internal-clock.yaml` | verify-lock (already correct v1.9.0) | 1 |
| `deliverables/ai/P2/architecture/smart-pins/smart-pin-11001-adc-external-clock.yaml` | verify-lock | 1 |
| `deliverables/ai/P2/architecture/smart-pins/smart-pin-11010-adc-scope-trigger.yaml` | verify-lock (`P_ADC_SCOPE`) | 1 |
| `engineering/operations/P2KB-CORRECTION-FINDINGS.md` | add **F-170** (canonical encoding + donor root cause) | 3 |
| `engineering/tools/validation/audit-adc-encoding.py` | **new** guard validator | 3 |
| `~/.claude/.../feedback_skill_evolution_candidates.md` (in-repo copy) | append release-checklist candidate | 3 |
| IOSP `audit/` note citing the 2026-06-12 Titus finding | un-stale | 4 |
| `manuals/p2-io-and-smart-pins-user-guide/opus-master/part-3-input-modes/chapter-16-adc.md` | enrich (4 additions) | 5 |
| `engineering/document-production/app-notes/P2AN000/opus-master/P2AN000.md` | **new** app note | 6 |
| `engineering/document-production/app-notes/APP-NOTE-CREATION-GUIDE.md` | dual-archetype update | 7 |
| `app-notes/P2AN000/P2AN000-NOTES.md` | rig spec + measurement-table stub | 8 |

---

## 1. Fix the ADC encoding at its ROOT (donor) + verify-lock the published YAMLs

**Why.** The encoding defect has been fixed downstream-only and keeps threatening to re-seed.
Forensics (git): the bug was born at `e271cab0` (2025-11-29) by importing a mis-authored
donor; survived the v1.6.3 "aligned to silicon" pass (`b0f48a88`, which only touched gain
constants); fixed in the *published* file at `35344af8` (v1.9.0, 2026-06-13) — but **the donor
was never corrected.** Any "regenerate from catalog" re-introduces it.

**Current state.**
- Donor `…/mode-11000-adc-internal-clock/…-concise.yaml:26-29, 153-154` — **WRONG**: `%00 =
  Raw bitstream capture`, `%11 = (Reserved/unused)` (inverted misconception).
- Published `smart-pin-11000-adc-internal-clock.yaml:24-29, 153-156` — **CORRECT** (v1.9.0).
- Sibling `smart-pin-11001…yaml` and `smart-pin-11010…yaml` — **CORRECT** (per forensics).

**Target.** Donor encoding matches Silicon Doc (`%00 SINC2 sampling … %11 bitstream`). All
three published ADC YAMLs confirmed mutually consistent and silicon-matching. (The donor fix
is **ingestion-catalog hygiene**, done directly — it is NOT in the `deliverables/ai/P2` set,
so it is outside `yaml-knowledge-base-maintenance`'s remit; the published-YAML verify-lock IS
that skill's remit.)

**Integration.** None beyond the YAML set. No cross-refs change.

**Verification.**
- *Normal:* donor X[5:4] text now equals silicon (`%00 SINC2 sampling`, `%11 bitstream`);
  `validate-yaml-syntax.py` + `validate-crossref-keys.py` clean.
- *Edge:* diff donor vs published vs sibling 11001 → all three agree on the four-row map.
- *Error (the recurrence test):* the new guard (§3) FAILS if donor≠published≠silicon — prove
  it would have caught the original bug.

---

## 2. ~~Reconcile `P_ADC_CAL` → `P_ADC_SCOPE`~~ — REMOVED (2026-06-28)

**Dropped per D1.** `P_ADC_CAL` lives only in the **retired** Green Book tutorial (parked /
not going forward) + its test doc. IOSP (the going-forward smart-pins doc) and the YAML are
already correct (`P_ADC_SCOPE`, Spin2 v55). No going-forward naming conflict exists, and we
do not edit retired docs. (Tombstoned, not renumbered, so later sections keep their numbers.)

---

## 3. Durable guard — make the encoding un-regressable

**Why.** The defect persisted 6.5 months because the encoding was on **no** verification
checklist. A permanent record + an automated assertion stop a fifth recurrence.

**Current state.** No corrections-register entry exists for the SINC encoding; no validator
checks it. Validators live in `engineering/tools/validation/` (pattern: `audit-*.py`).

**Target.**
- **F-170** appended to `P2KB-CORRECTION-FINDINGS.md` (status `DONE`, with the canonical
  encoding, the donor root-cause narrative, and the fix-trace to §1) — the searchable record
  so this is never re-chased.
- **`audit-adc-encoding.py`** (new): asserts the X[5:4] four-row map is identical across the
  donor, the three published ADC YAMLs, and the silicon-doc-sourced truth string; non-zero
  exit on any drift. Wired into the local validator set.
- Append a **skill-evolution candidate** (release-yamls should run this assertion pre-publish)
  to `feedback_skill_evolution_candidates.md` — do NOT edit the central skill.

**Integration.** Validator joins `BUILD/TEST` validators (per `skill-conventions.md`).

**Verification.**
- *Normal:* validator passes on the corrected tree.
- *Edge:* temporarily revert the donor → validator FAILS (proves it guards the real bug path).
- *Error:* malformed YAML → validator errors cleanly, doesn't false-pass.

---

## 4. Un-stale the IOSP audit note

**Why.** The IOSP `audit/` note cites a Titus cross-audit (2026-06-12) calling the %11000
YAML encoding "wrong" — true that day, fixed the next (v1.9.0, 2026-06-13). The stale note is
what made this whole investigation think the YAML was currently broken.

**Current state.** The note lives in the IOSP `audit/` folder (Titus cross-audit of Ch.16).

**Target.** Annotate the finding as **RESOLVED (v1.9.0, 2026-06-13)** with a pointer to F-170;
do not delete (preserve the audit trail).

**Verification.** *Normal:* the note reads as resolved with date + F-170 link. *Edge:* no other
IOSP audit note still asserts the encoding is wrong (grep the audit folder).

---

## 5. IOSP Ch. 16 foundation enrichment

**Why.** The audit shows Ch.16 is competent mid-range but **undersells the ADC ceiling**: no
ratiometric instrumentation, caps at 14-bit, conflates source-switch flush with startup
warm-up, omits the hardware limits. Enriching it makes the guide authoritative and gives the
app note a foundation to cite. IOSP is **unreleased** → lands in first release, **no bump**.

**Current state** (`…/opus-master/part-3-input-modes/chapter-16-adc.md`; sections per audit):
- 16.2 Input modes (GIO/VIO/FLOAT + gain) — L35-46.
- 16.3 Mode %11000, incl. SINC2-filtering with code — L141-167; "warm-up" note — L185-189.
- 16.8 Accuracy Considerations — L502-545.
- 16.9 Quick Reference.

**Target — four additions** (reference register; follow IOSP's voice/creation guide; edits to
opus-master only, never the workspace render):
1. **New "Ratiometric / Absolute-Voltage Instrumentation" subsection** (per D4): the GIO+VIO+pin
   three-source method, `uV = (pin−GIO)/(VIO−GIO) × 3.3V`, with a **minimal** illustrative
   snippet (per D5). Source: STUDY §A2/B2 (Chip).
2. **Separate the source-switch 3-sample flush from startup warm-up** in/near 16.3 (L185-189):
   state that switching the ADC input source contaminates ~3 samples (2 decimations + 1 settle)
   — distinct from the one-time startup warm-up. Source: STUDY §A4 (Chip + evanh).
3. **Hardware-limits content in 16.8**: ~500 kΩ input impedance (value), the ~15 mV
   matched-resistor **absolute-error** mechanism (designer-stated), VIO-supply & temperature
   sensitivity, the power-of-2 period constraint (cross-link). Source: STUDY §A6.
4. **Ceiling framing** (16.3 resolution table + a note): long integration + gain reaches
   ~16–17-bit / µV territory — **mechanism only, QUALITATIVE**; explicitly frame absolute ENOB
   as board/source/temperature-dependent (Chip's numbers are bench/rig, not spec). Source:
   STUDY §6 honesty constraint.

**Integration.** App note (§6) cites these subsections. No YAML change required (the foundation
facts trace to the now-correct ADC YAMLs + the silicon doc; any net-new fact not in YAML that
we want canonical → file as a finding, do not assert).

**Verification.**
- *Normal:* the four additions present, each sourced; chapter still renders (handback model —
  Stephen renders; verify on next IOSP build).
- *Edge:* ratiometric snippet **compiles under `pnut_ts`** at 200 MHz; negative (Sig<Gio) and
  over-range (Sig>Vio) cases described.
- *Error:* no guaranteed-ENOB claim slips in (grep for "bit" claims; each must be qualified);
  no `P_ADC_CAL`.

---

## 6. P2AN000 — the instrumentation-ADC app note (techniques-catalog archetype)

**Why.** The application layer: "Measure an absolute voltage in microvolts on a P2 pin — no
external ADC." First note in the series; proves the techniques-catalog archetype.

**Current state.** Folder + research staged: `app-notes/P2AN000/` (opus-master empty; NOTES +
`research/improved-adc-pin-techniques/` with verbatim thread, 7 code attachments incl.
`EightPinADC.spin2`, and the STUDY classification). Guides: `APP-NOTE-CREATION-GUIDE.md` +
`APP-NOTE-VOICE-GUIDE.md`.

**Target** (`opus-master/P2AN000.md`; voice per APP-NOTE-VOICE-GUIDE; structure per CREATION-GUIDE
techniques-catalog archetype as amended in §7):
- **Shared base build** — single-pin instrumentation ADC, derived from `OnePinADC.spin2`,
  stripped of demo scaffolding, at **200 MHz** (D3), `pnut_ts`-certified. The **shared harness**
  (DEBUG SCOPE in µV + DAC loopback test signal) is defined once here (D6).
- **The Idea / How It Works** — SHORT: orientation + pointer to enriched IOSP Ch.16 (the doc
  contract). Mental model + the three-source concept; mechanism detail lives in IOSP.
- **Decision table** — need (resolution / channel-count / sample-rate) → technique. This is the
  "choose what your project needs" spine. Three axes (per Stephen).
- **Tiered recipes**, each a complete, runnable, `pnut_ts`-certified entry on the shared base:
  (1) single-pin absolute µV; (2) 3-pin constant-impedance ×3 accuracy (from `ThreePinADC.spin2`);
  (3) N-stage time-halving filter (rate/resolution selector); (4) range extension (series R +
  tempco note); (5) mains-cycle averaging. **Capstone/reference:** the 8-pin bytecode
  interpreter (`EightPinADC.spin2`) as "the ceiling" — described + linked, not re-taught.
- **Verify** — expected DEBUG µV output + the "drive a pin to GND, read ~0" self-check + an
  honest failure branch.
- **Pitfalls** — power-of-2 period, LDO VIO, the 15 mV absolute-error limit, high-Z loading,
  legal clock.
- **Resources** — links to IOSP Ch.16, the captured research, related modes.

**Integration.** Depends on §5 (IOSP foundation) and §1 (correct YAML). Every idiom validated
against the P2KB **first**, then `pnut_ts`. Example library staged per app-note production.

**Verification.**
- *Normal:* every code block **compiles under `pnut_ts`** at 200 MHz; the base build's expected
  µV output documented.
- *Edge:* Sig<Gio (negative), Sig>Vio (over-range), source-switch boundary (3-sample discard),
  3-pin impedance-constant rotation — each exercised by a recipe.
- *Error:* non-power-of-2 period rejected/avoided; no 320 MHz; no unsourced ENOB number; no KB
  plumbing language in the reader doc (per voice guide).

---

## 7. APP-NOTE-CREATION-GUIDE — admit the dual archetype

**Why.** The guide currently says "single technique, deep" and "removing the worked example
would break the note" — too narrow; this very note is a techniques-catalog (like P1 AN001).
The rule that just proved incomplete should be fixed (process discipline).

**Current state.** `app-notes/APP-NOTE-CREATION-GUIDE.md` §1 ("single technique, deep") and §8
checklist.

**Target.** Name **two archetypes** — *single-build* and *techniques-catalog* — and state the
two guardrails that keep a catalog from becoming a manual chapter: (a) a shared conceptual base
first; (b) every technique a complete, verified, runnable recipe + a decision aid. Note the
decomposition rule: foundation belongs in the manual; the note applies it.

**Verification.** *Normal:* guide describes both archetypes + guardrails; the P2AN000 structure
(§6) conforms. *Edge:* the single-build archetype guidance still intact (not lost in the edit).

---

## 8. Hardware-measurement readiness (qualitative now, numbers later)

**Why.** Stephen will run recipes on a rig to upgrade qualitative claims to measured ENOB. Spec
the rig + procedure now so the data slots in cleanly later (and the ceiling claims become
empirically grounded — top of the trust chain).

**Current state.** `P2AN000-NOTES.md` source-traceability table exists; no rig spec.

**Target.** Add to NOTES: the **rig tiers** — Tier 0 (P2 Edge + jumper, DAC-loopback functional
proof); Tier 1 (precision V-ref + 6.5-digit DMM + 0.1% resistors + LDO VIO → absolute/ENOB
numbers); Tier 2 (thermistor/µV source, mux for the SaucySoliton variant) — plus a **measurement
table stub** (technique → clock/rate → measured ENOB) the app note + IOSP reference, marked
"qualitative pending hardware." A short **test procedure** per recipe (what to apply, what to
read, expected vs measured).

**Verification.** *Normal:* NOTES carries the rig spec + stub table + per-recipe procedure.
*Edge:* the app note's qualitative claims each map to a stub-table row awaiting a number.

---

## Exit gate

Research complete; all decisions resolved by recommendation (none blocking); no procedure
needed that a current skill doesn't cover **except** the central `release-yamls` checklist line,
captured as a skill-evolution candidate (§3, D2). Plan ready for `plan-to-tasks`.

---

## Section ↔ task cross-reference (generated 2026-06-28)

Sprint tag: `smartpin-adc`. Execute via `todo_next tags:["smartpin-adc"]`.

| Plan § | Deliverable | Task | seq |
|---|---|---|---|
| §1 | Fix ADC encoding donor + verify-lock published YAMLs | «#121» | 12 |
| §3 | Durable guard (F-170 + audit-adc-encoding.py) | «#122» | 13 |
| §4 | Un-stale IOSP encoding audit note | «#123» | 14 |
| §5 | IOSP Ch.16 foundation enrichment (4 additions) | «#124» | 15 |
| §7 | Dual-archetype app-note guide update | «#125» | 16 |
| §8 | Rig spec + measurement-table stub | «#126» | 17 |
| §6a | P2AN000 app note — base build + harness + concept | «#127» | 18 |
| §6b | P2AN000 app note — catalog + verify + close | «#128» | 19 |
| §2 | ~~`P_ADC_CAL` reconcile~~ — DROPPED (Green Book retired) | — | — |

> Order note: §7 (guide archetype) is sequenced **before** §6 per the rework-analysis
> standards-before-application rule — the app note must conform to the updated guide. §1 is
> foundational (guard, IOSP enrichment, and the app note all rest on the corrected encoding).
