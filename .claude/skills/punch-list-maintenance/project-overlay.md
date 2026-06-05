# P2-Knowledge-Base overlay — punch-list-maintenance

> **DRAFT (pre-brainstorm, 2026-06-05).** Per-head punch-list homes are
> still `TBD` in the dispatch table; this will be dialed in after the Work
> Type Routing brainstorm and the punch-list relocation cleanup.

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
Spin2 v51 → Silicon Doc), and proposed correction. (See
[[project_p2kb_corrections_register]],
[[feedback_needs_verification_not_a_ship_license]].)

> **Cleanup debt (separable):** existing punch-list content needs
> relocating to its correct per-head homes, and the corrections register
> needs its dated-archive flow stood up. Recorded in `skill-conventions.md`.
