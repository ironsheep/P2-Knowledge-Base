# Sprint 1 — Guide Normalization — Retrospective

**Sprint:** `guide-normalization` · 11 tasks `«#205»`–`«#215»` · closed 2026-08-15
**Closeout:** `engineering/history/sprints/2026-08-15-guide-normalization-sprint-1-CLOSEOUT.md`
**Build shipped:** none — Sprint 1 ships no versioned artifact by Stephen's decision at sprint start.

**Verdict up front:** this sprint produced **real process learning worth acting on**. Two planning
gaps were diagnosed and both are already operationalized into project overlays. It was not a clean
execution with no methodology delta.

---

## Discovered perspectives

- **The house layer already existed, and the sizing debate was a false binary.** Planning framed it
  as "define once and point" vs "copy into eleven". The catalog had answered it a month earlier
  (`3d8a653c`, 2026-07-20) and six of ten guides already cited it as canonical. The real model —
  canonical statement in the catalog, local adaptation per guide — was discoverable by reading the
  file nobody had opened.
- **Every voice contradiction in the corpus has one root cause:** the rule was written by naming
  banned **words** instead of naming the **defect**. One authoring error, eleven guides.
- **The corpus validated the structural rule before we imposed it.** The only two guides already
  practising "reference, never restate" (XBYTE, app-note) had **zero** voice contradictions; every
  restating guide had at least one. That is evidence, not preference — worth more than the argument
  we would otherwise have had.
- **The most dangerous site is a checklist, not a rule.** A rule gets read and weighed; a checklist
  gets run mechanically by an auditor. Assembly's creation-guide banned "usually" — R1's own
  canonical example of a *required* qualifier.
- **A guide teaches register by example, not by its rules section.** The Debug Window creation guide
  declared the Discovery-Guide voice out of standard *and was written in it*, using "20× improvement"
  as its exemplar of a well-sourced claim while the sibling voice guide cited that exact phrase as
  forbidden marketing.
- **«#214» inverted its own hypothesis.** We looked for damage by *removal* — diff-visible — and
  found none. The measurement pointed at damage by *suppression*: qualifiers never written, which no
  diff can show. **The thing we could measure was not the thing most likely to be wrong.**
- **The auditors were better than the checklists.** `periodic-audit-2026-05-22` §F.1 grepped for
  hedges, found three, kept all three with reasons, and closed Verified-OK. The dangerous rule was
  absorbed by judgment for nine months. That is reassuring and *not* a reason to keep the rule.

## Process insights

- **Ordering the instrument first was right and paid immediately** — it caught that the hand count
  was the wrong *order of magnitude* (176 vs ~100), which no amount of re-reading would have.
- **But ordering it first was not enough** — the repair tasks had already been sized from the hand
  count. See Methodology lesson 1.
- **The atomic green-unit convention worked exactly as designed.** «#206» went red at its own
  completion by design, and the charter said so in both the task text and the resume key. No agent
  tried to "fix" the red by weakening detections across seven subsequent tasks.
- **Printing exemptions and exclusions by name is what makes "clean" mean something.** 24 exemptions
  and 4 roster-Abandoned exclusions are named on every run — so PASS never quietly means "we didn't
  look there".
- **The crash cost almost nothing**, because «#214» had produced no partial state and the resume key
  was current. The breadcrumb discipline is doing its job.
- **Friction: the `BUILD_COMMAND` slot is wrong for this project** and the charter had to override it
  inline. `validate-yaml-syntax.py` scans `manifests/` + `knowledge-base/` and returns a green that
  verifies almost nothing; `verify-yaml-format.py` is the real gate. This is already logged as a
  `baseline-health` candidate and has now bitten a second time.

## Quality and efficiency observations

- **Actuals ran far under estimate** — 11h estimated, ~65 minutes of recorded task time. The estimates
  were sized for authoring; most tasks turned out to be *mechanical repair against a gate that tells
  you exactly where to look*. Building the instrument first is what converted authoring into repair.
- **The exception proves it: «#214» ran 35m against a 60m estimate but was the only genuinely
  investigative task** — and it was the one whose scope was mis-specified.
- **Reading was slower than grepping and won five times.** See below.
- **The descriptors cost more than they should have** because nothing pointed at them — «#215» found
  D2/D3/D4 defects there by hand, in files no gate scans.

## Downstream impact

**Enables:**
- Sprint 2 can measure manual text against a guide layer that is internally consistent for the first
  time. Editing a manual against a self-contradicting guide was the collision that forced the split.
- `DOC_AUDIT_COMMAND` is set, so `plan-to-tasks` §2a stops firing its "instrument owed" clause.
- DeSilva is reachable by the conventional `<element>/voice-guide.md` lookup, so the next sweep will
  not skip it the way this one nearly did.
- The Sprint-2 edit-vs-regenerate gate is cleared — the DeSilva creation guide no longer says a
  6,176-line shipped manual must be *regenerated* to fix two sections.

**Destabilizes / owes:**
- **The guide layer is now gated; the manual layer is not.** D4 and D6 almost certainly extend into
  manual text the same way D2 did, and 299 files repo-wide still carry `pnut_ts`.
- **Two known coverage holes** — descriptors and the standards tree — with proven defects inside
  them. Closing them re-opens the green unit, so it is a deliberate decision, not a chore.
- **The suppression question is open and unmeasured**, and it is the harder one.

## Methodology lessons

Both entries below were logged in-flight to `feedback_skill_evolution_candidates.md` and are
**adopted** (operationalized into overlays this retrospective) and **certified** (each already caught
something real in this sprint).

**1. `plan-to-tasks` — an instrument's first run is a planning input, not just a gate.**
When a sprint builds a measuring instrument, ordering it first is necessary but insufficient: no
downstream task's **scope or estimate** may be fixed until it has run once. *Certified:* the first
run returned 176 findings against a planned ~100, concentrated in 62 codename sites vs the 5 named by
hand — after «#207»/«#208» had already been sized against the subset.
→ Adopted: `.claude/skills/plan-to-tasks/project-overlay.md`.

**2. `sprint-plan` — scope boundaries come from the artifact, never from prose.**
Any date or commit bounding an investigation must be pickaxed out of the artifact under
investigation. **A cited SHA is evidence that something changed then; it is never evidence that
nothing changed before.** *Certified:* moved «#214»'s window from 3–4 weeks to 7–9 months; as written
the task would have scanned ~1 commit instead of ~120 and returned a meaningless NIL.
→ Adopted: `.claude/skills/sprint-plan/project-overlay.md`.

**3. Observed here, not yet a candidate — the name-collision failure mode.**
Plan §6 and task «#215» were both called "Documentation Blast Radius" and covered *different artifact
sets* in different sprints. The cross-reference row `Plan §6 → «#215»` would have read as discharged
and buried nine live Sprint-2 commitments. `sprint-closeout` §1's both-directions reconciliation
caught it — **the existing rule worked**. Recorded as evidence the reconciliation step earns its
place, not as a new rule.

**4. Re-surfaced, not new — the `BUILD_COMMAND` slot mismatch** (existing `baseline-health` candidate,
line 60 of the buffer). It has now caused friction twice: the sprint charter had to carry an inline
override warning, and closeout had to deviate from §4. **Deferred once already — promote its
severity.**

### The method note that outranks all of the above

**READ, DO NOT GREP.** Hand counts and keyword surveys were wrong **five separate times** across this
effort: the original 21-site count (actual 176); the cadence table (R4 in five guides, not three);
the anti-pattern counts for Architect and Getting Started; plan §6's claim that
`HEAD-DISPATCH-DRAFT.md` references the retired slug (it never has); and **«#214»'s sole candidate
finding, which would have been FALSE if judged from the diff rather than the file.**

The instrument fixes four of those five. It does **not** fix the fifth, and that asymmetry is the
lesson: **a machine replaces counting, not reading.** It can tell you where to look; it cannot tell
you whether a hedge covered partial evidence or a wrong claim. Sprint 2 should not read the new gate
as permission to stop opening files.

---

## Candidates-file triage

Project is `PROMOTION_SOURCE: yes` — promotion-source verdicts apply (adopt → certify → promote).

| Entry | Verdict | Note |
|---|---|---|
| `plan-to-tasks` — instrument's first run is a planning input | **Adopted + Certified** | new this sprint; overlay written |
| `sprint-plan` — scope boundaries from the artifact, not prose | **Adopted + Certified** | new this sprint; overlay written |
| `baseline-health` — name which validator covers which tree | **Deferred → severity raised** | second occurrence; blocked closeout §4 |
| `document-finalize` ×3, `release-yamls` ×2, `yaml-kb-maintenance`, `forge-test`, `document-audit` v2.0.0, `sprint-retrospective` lifecycle | **Keep, untouched** | Sprint 1 exercised none of them |
| 6 build-sized Proposals | **Keep, parked** | unchanged |

**No entry was closed-no-change and none was deleted.** Nothing in the buffer was disproven; the two
new entries earned certification the same day they were logged, which is unusual and worth noting —
both were certified by the very failures that produced them.

**Awaiting Stephen:** whether either new rule is general enough to run through the promotion gate now
(owner-judgment override, `SKILLS-AUTHORING.md` Test 3), or should wait for convergence from a second
project. Neither is urgent.
