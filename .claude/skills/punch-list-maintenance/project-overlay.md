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
