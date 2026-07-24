# sprint-retrospective — P2-Knowledge-Base overlay

Applies **additively** to the central `sprint-retrospective` skill.

Central §5 carries the promotion-source lifecycle natively (adopt → certify →
promote, with its own verdict set), selected by `PROMOTION_SOURCE: yes` — set in
this project's `skill-conventions.md`. Central explicitly delegates three
project-specific things back to this overlay: **the certification vocabulary,
the cert-marker names, and the project entry shape.** This overlay supplies
exactly those and nothing more — it no longer restates the lifecycle, the
promotion precondition, or the verdict set (all central now).

## Certification vocabulary — what counts as evidence here

A locally-adopted rule accrues promotion weight only from a demonstrated catch;
until then it is `certified: PENDING`. What certifies it, by rule type:

- **Corrective rules** certify when they actually find / fix / correct
  something in real work — append a one-line `certified:` note with *what it
  caught* and *when*.
- **Preventive rules / gates** certify by **firing on a real catch** (you
  cannot observe absence-of-failure) — e.g. the pre-flight gate certified by
  catching a `.json`/`.gz` gzip drift on its first run.

The cert-marker is the literal `certified:` line: `certified: PENDING` while
adopted-but-unproven, replaced by `certified: <catch> — <YYYY-MM-DD>` once it
fires. Accumulated `certified:` lines are the evidence carried into a promotion
proposal.

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
