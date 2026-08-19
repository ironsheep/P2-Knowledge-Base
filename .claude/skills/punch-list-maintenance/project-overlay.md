# P2-Knowledge-Base overlay — punch-list-maintenance

> **Status (2026-06-22).** The Work Type Routing model is adopted (multi-head
> dispatch + `whats-next` front door). Still open: per-manual and per-ingestion
> punch-list homes remain `TBD` in `HEAD-DISPATCH-DRAFT.md`, and the punch-list
> relocation cleanup is recorded as separable debt in `skill-conventions.md`.
> (The YAML head's punch list is resolved: `P2KB-CORRECTION-FINDINGS.md`.)

## Augments Step 0a — resolving the per-head `PUNCH_LIST_DOC` sentinel

There is **no single project punch list.** Each head/element has its own:
- **MANUAL** — the manual's own punch list (location `TBD` per manual).
- **YAML (KB)** — `engineering/operations/P2KB-CORRECTION-FINDINGS.md`.
- **INGESTION** — per ingestion source (location `TBD`).

Identify the head/element first, then resolve the punch list from
`.claude/skills/HEAD-DISPATCH-DRAFT.md`. A `TBD` home → ask {{USER_NAME}}.

## Augments the sweep — `P2KB-CORRECTION-FINDINGS` is a punch list

The corrections register is structurally a punch list: external
observations come in, repairs are batched out. It gets the **same
lifecycle** as any punch list here — mark a finding `DONE`, then **sweep
completed items to a dated archive** (`PUNCH_LIST_ARCHIVE_PATTERN`) so the
live copy carries only outstanding work. Finding states are
`CONFIRMED` / `NEEDS-VERIFICATION` / `DONE` / `WONTFIX`; each finding keeps
its ID, exact file location, what's wrong, evidence (cite `pnut_ts` →
Spin2 v55 → Silicon Doc), and proposed correction. (See
[[project_p2kb_corrections_register]],
[[feedback_needs_verification_not_a_ship_license]].)

> **Cleanup debt (separable):** existing punch-list content needs
> relocating to its correct per-head homes, and the corrections register
> needs its dated-archive flow stood up. Recorded in `skill-conventions.md`.


---

## Augments "Archive procedure" — HOW TO ARCHIVE WITHOUT LOSING CONTENT

**Learned 2026-08-15, the expensive way. Do not re-learn it.**

The central procedure says *copy the done items into the archive, then remove them
from the active list.* Followed literally — **building** the two output files — that
sweep silently lost **223 lines and an entire section (ENH-01)**, and **passed its own
verification**, because the check was computed from the same block model that had
dropped them.

### The method: RENAME-THEN-TRIM, never build-the-output

1. `engineering/tools/backup-file.sh <register>`
2. **`git mv` the register to the dated archive path.** The archive is now complete
   **by construction** — a tracked rename of the original, not a reconstruction.
3. **Recreate the register** and delete from the archive only what stays open.
   Everything after step 2 is **subtraction from a preserved copy**.
4. **Prove it:**
   ```bash
   python3 engineering/tools/validation/audit-register-hygiene.py <register> \
           --sweep-check <pre-sweep-commit>
   ```
   Every substantive line of the pre-sweep register must still exist in the live file
   or an archive. The tool reads the original **out of git** — independently of
   whatever performed the sweep.

### `correction-sweeps/` is GITIGNORED — a second reason `git mv` is not optional

`.gitignore:276` ignores `/engineering/operations/correction-sweeps`. The three archives
in it are tracked only because each was brought in by a **rename**, and `git mv` forces
tracking regardless of the ignore rule.

**Create an archive with `cp` and it is silently UNTRACKED** — the register would point
at a file that is not in the repository, its content living only on one disk, invisible
to `git log`, to clones, and to `--sweep-check`. Everything would look fine until the
first time anyone needed the history. `git mv` is what makes the archive *exist* as far
as the repo is concerned, not merely what makes it complete.

**Verify after every sweep:**
```bash
git ls-files --error-unmatch <archive-path>   # must succeed
```

### The general trap, worth more than the procedure

**A verification computed from the same model that did the work cannot detect that
work's error.** The failed sweep's check and the failed sweep's split shared a block
model, so the check confirmed exactly the thing that was wrong. Any "did I lose
anything?" check must read the original from an **independent** source — here, `git
show <rev>:<file>`.

### Two constraints on `--sweep-check`

- **Run it at sweep time**, against the pre-sweep commit, with nothing else changed.
  Run retrospectively it flags every later **in-place rewrite** as unaccounted — and
  this register *requires* rewriting a revised finding in place, so that is churn, not
  loss. Confirm any hit against git before calling it a loss.
- It is line-presence, not structure. The companion checks — **no duplicate ID**, and
  **no allocated ID missing from live + archives** — are what prove no *finding* went
  silent. Run the tool with no flags for those; they are cheap and always valid.

### Run the gate before and after every sweep

`audit-register-hygiene.py` with no flags is the standing check (counter ahead of the
highest allocation, no duplicate IDs, no closed findings left in an open-work file, no
finding without a status, archives resolve, no ID unaccounted). A sweep is *finished*
when it exits 0.
