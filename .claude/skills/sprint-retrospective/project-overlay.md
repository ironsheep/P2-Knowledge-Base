# sprint-retrospective — P2-Knowledge-Base overlay

Applies additively to the central `sprint-retrospective` skill. Overrides the
**§5 "Promote methodology lessons"** behavior with this project's
**adopt-locally → certify → promote** model.

## Why this overlay exists

Central's §5 now *triages* `feedback_skill_evolution_candidates.md`
(Addressed / Deferred / Closed-no-change, with `APPLIED` auto-Addressed) — but it
still stops at *candidate awaiting confirmation*: nothing operationalizes a
rule-sized learning in the same retrospective, and there is no certification
step. That gap is what let earlier learnings land in the buffer and **never get
operationalized** — a write-only graveyard (surfaced in the 2026-06-11
debug-window-v55 retrospective: the `baseline-health` and crossref-field-type
entries had no skill home at all).

The fix: a learning earns its way to central by **proving itself locally first**,
not by sounding good in a note.

## §5 (overridden) — Adopt locally, certify, then propose promotion

When the retrospective identifies a methodology learning, classify it and act:

1. **Rule-sized** (a constraint, gate, or check expressible in a skill/overlay):
   **operationalize it locally NOW** — write it into the actual project skill or
   `project-overlay.md` (create the overlay if absent), in the same retrospective.
   Do **not** merely log it. If no project home exists for the central skill,
   the act of creating `.claude/skills/<skill>/project-overlay.md` IS the adoption.
2. **Build-sized** (a new skill or a non-trivial design effort): central
   already parks these for a future sprint (don't build during retrospective) —
   here, tag it `PROPOSAL` so it cannot masquerade as an adopted/certified
   candidate.
3. **Then** record it in `feedback_skill_evolution_candidates.md` using the
   project entry shape below — as a *locally-adopted, promotion-pending* rule,
   not a wish.

### Certification — what earns promotion weight

A locally-adopted rule accrues **promotion weight only from demonstrated value**:

- **Corrective rules** certify when they actually find/fix/correct something in
  real work — append a one-line `certified:` evidence note (what it caught, when).
- **Preventive rules / gates** certify by **firing on a real catch** (you cannot
  observe absence-of-failure) — e.g. the pre-flight gate certified by catching a
  `.json`/`.gz` gzip drift on its first run.
- Until a rule has at least one certification, it is `certified: PENDING` — adopted
  but unproven; it does **not** yet count toward the promotion bar.

### Promotion to central

The central bar still holds (a second project independently wanting the rule —
`SKILLS-AUTHORING.md` Part 1 Test 3). This overlay **adds a precondition**: a
rule is promotion-eligible only once it is **adopted locally AND certified**.
Accumulated certifications are the evidence you bring to the promotion proposal.

## Project entry shape for `feedback_skill_evolution_candidates.md`

```
- [<target-central-skill>] <rule one-liner>
  — local home: <path it's operationalized in | PROPOSAL: not yet built>
  — certified: <find/fix it produced + date | PENDING>
  — generalizes: <why another project would want it>
  — source: <where it came from> — added: <YYYY-MM-DD>
```

`local home` is mandatory: an entry with no local home is either a `PROPOSAL`
(build-sized, parked) or it does not belong in the buffer yet — operationalize
it first.

## Triage verdicts (overrides the central Addressed/Deferred/Closed set)

- **Adopted** — operationalized locally this retrospective; `certified: PENDING`. Keep.
- **Certified** — proved its value since last review; append the evidence; weight rises. Keep.
- **Promote** — adopted + certified + second-project signal → run the generality
  gate and propose the central edit. Keep until the central edit lands, then delete.
- **Proposal** — build-sized; parked as backlog, not certified. Keep, tagged.
- **Closed-no-change** — decided not to act; delete with a one-line rationale in
  the retrospective doc.

> **Relation to central's `APPLIED` state.** When a `Promote` entry's central
> edit lands via the promotion close-out (`SKILLS-RECONCILE.md` §3), central
> marks the buffer entry `APPLIED`; the next retrospective then auto-Addresses
> and deletes it (central §5). So this overlay's `Promote → keep until the edit
> lands, then delete` is that same lifecycle, expressed in the project's
> certification vocabulary — `APPLIED` is the central-side stamp on a `Promote`
> entry whose edit has shipped.
