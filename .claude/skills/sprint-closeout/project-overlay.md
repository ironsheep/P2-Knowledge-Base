# P2-Knowledge-Base overlay — sprint-closeout

## Augments §7 — closeout is the archive cadence for EVERY archivable doc, not just the punch list

Central §7 runs `punch-list-maintenance` and calls sprint closeout "its defined
cadence." In this project that skill resolves to **several** registers, and a
closeout that sweeps one and skips the others leaves exactly the backlog the
cadence exists to prevent.

**Sweep all of these at closeout:**

| Doc | Archive destination | Gate |
|---|---|---|
| `engineering/operations/P2KB-CORRECTION-FINDINGS.md` | `engineering/operations/correction-sweeps/<date>-P2KB-CORRECTION-FINDINGS-archive.md` | `audit-register-hygiene.py` exits 0 |
| `engineering/document-production/PUNCH-LIST.md` | per `PUNCH_LIST_ARCHIVE_PATTERN` | — |
| the sprint plan itself | `engineering/history/sprints/` (§8) | plan no longer in `engineering/planning/` |

**Use rename-then-trim, and prove it.** The method and the reason it matters are in
the `punch-list-maintenance` project overlay — do not archive by building the output
files. Finish with:

```bash
python3 engineering/tools/validation/audit-register-hygiene.py \
        engineering/operations/P2KB-CORRECTION-FINDINGS.md --sweep-check <pre-sweep-commit>
```

**Classify by STATUS TOKEN, never by headline prose.** A finding whose headline says
"source fixed" while its status is still `CONFIRMED` is **open** — most of them add
"render owed", and this register's own rule is that a fix applied but not yet
validated is not done. The 2026-08-19 sweep's first pass trusted the prose and would
have archived **16 findings with work still owed**. `PARTIAL` vetoes an embedded
`DONE`. The gate's `status-hygiene` class lists prose/status mismatches so they get a
deliberate decision instead of a silent sweep.

## Why this overlay exists — the cadence was skipped, and it showed

Recorded 2026-08-19. Two sprints shipped without a closeout: the **XBYTE guide
restructure** (manual released v1.1.0) and the **manual-corrections Sprint 2** (an
eight-release wave). Neither produced a closeout doc, neither archived its plan, and
because §7 never ran, neither swept the register.

The visible consequences: **34 closed findings** had accumulated in a register that
declares it carries open work only, in a **3,559-line** file; and
`engineering/planning/` holds **44 live plans** against **30** archived. Agents miss
things in long lists — so a skipped closeout does not just defer tidying, it degrades
every later read of the register.

**A sprint is not closed until its archives are swept and the gate exits 0.**
