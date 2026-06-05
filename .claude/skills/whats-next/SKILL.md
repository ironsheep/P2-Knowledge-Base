<!-- Requires MCP: todo-mcp -->
---
name: whats-next
description: >-
  Front-door session-start skill for P2-Knowledge-Base. Run FIRST each
  session, when deciding what to work on, or when setting work aside to
  switch heads. Head-aware, register-backed resume: reads the
  `active_element` pointer, reports "here's what you've been working on"
  by resolving the element's standing-doc state, and offers to resume —
  or verifies a new target against the registries and either resumes or
  runs the add-new-element process. Supersedes the bare `context_resume`
  + "what do you want to work on?" session-start ritual.
---

# What's next — the session front door

> **STATUS: Initial working draft (2026-06-05).** Built fresh from the
> Work Type Routing brainstorm. Expect to tune with friction. The shared
> model lives in `.claude/skills/HEAD-DISPATCH-DRAFT.md`.

P2-Knowledge-Base is **three heads** under one repo, and work is
context-switchy (~70% single-head run-to-completion; ~30% interleaved —
progress a head, set it aside, pick another, sometimes return). This skill
is how we re-enter that work without losing the thread.

**The only state we actively store is one pointer:** the todo-mcp context
key `active_element`, value `head:element` — e.g. `manual:p2-streamer-guide`,
`yaml:p2kb`, `ingestion:p1-propeller-manual`. Everything else ("where was
I", "what's outstanding") is **reconstructed from standing docs and git**,
never duplicated into a tracker.

The three heads, their registry, and their standing state:

| Head | Registry | Per-element standing state | Progress notion |
|------|----------|----------------------------|-----------------|
| **manual** | `engineering/document-production/PUBLICATION-ROSTER.md` | the manual's folder — `CHANGELOG.md`, `audit/`, working notes | version |
| **yaml** (P2KB) | the YAML tree / index | `engineering/operations/P2KB-CORRECTION-FINDINGS.md` (**empty ⇒ nothing outstanding**; non-empty ⇒ the to-do list) | version |
| **ingestion** | `engineering/ingestion/INGESTION-DASHBOARD.md` | dashboard row (completeness %, gates) + `sources/<src>/<src>-complete-extraction-audit.md` | completeness % + gates (no version) |

## 1. Pull session state

- Run `mcp__todo-mcp__context_resume` — tasks + recent context.
- Read the pointer: `mcp__todo-mcp__context_get pattern:"active_element"`.

## 2. If `active_element` is set — report, then offer to resume

Parse `head:element` and resolve its standing-doc state from the table
above:

- **manual:`<m>`** — the `PUBLICATION-ROSTER` row + the manual's folder
  (CHANGELOG latest entry, `audit/` open findings, working notes), and the
  recent commits touching that manual (`git log --oneline -- <manual path>`).
- **yaml:p2kb** — read `P2KB-CORRECTION-FINDINGS.md`. Empty ⇒ "all
  published, nothing outstanding." Non-empty ⇒ the open findings ARE the
  to-do list; summarize the `CONFIRMED` / `NEEDS-VERIFICATION` counts.
- **ingestion:`<src>`** — the `INGESTION-DASHBOARD` row (completeness %,
  gate status) + the source's extraction-audit; recent commits under
  `sources/<src>/`.

Also surface any `in_progress` / next task from `context_resume` scoped to
the element's tag (`mcp__todo-mcp__todo_next tags:["<tag>"]`).

Then report plainly: **"Here's what you've been working on: `<element>` —
`<state summary>` — last activity `<recent commits>`. Resume this, or pick
up something else?"** Ask in chat (this repo has no AskUserQuestion).

## 3. If unset, or {{USER_NAME}} picks something else — choose a target

Determine the head + element to pick up (from what they say, or ask). This
is the head-pickup selection — the stateful evolution of the old "What are
we working on today?" prompt.

## 4. Verify the target against the registries

- **manual** → is it a row in `PUBLICATION-ROSTER.md`?
- **yaml** → there is one P2KB set; it always exists. State via
  `P2KB-CORRECTION-FINDINGS.md`.
- **ingestion** → is it a row in `INGESTION-DASHBOARD.md`? (When turning to
  ingestion, also refresh the dashboard per `INGESTION-UPDATE-WORKFLOW.md`.)

**Found → §5 (resume). Not found → §6 (add-new-element).**

## 5. Set active and resume

- `mcp__todo-mcp__context_set key:"active_element" value:"<head>:<element>"`.
- Resolve the element's standing-doc state (as §2), summarize the
  outstanding work, and route into the right work mode. Downstream skills'
  per-head overlays resolve their sentinel slots from `active_element`
  (see `HEAD-DISPATCH-DRAFT.md`), so they land on this element's artifacts.

## 6. Add-new-element process (target not in any register)

1. **Confirm it's genuinely new** — not a renamed or misremembered
   existing element. Search the registries and `git log` first.
2. **Decide the head** it belongs to (manual / yaml / ingestion / a new
   head entirely).
3. **Register it:**
   - new **manual** → add a row to `PUBLICATION-ROSTER.md` and stand up the
     manual folder per the manual conventions.
   - new **ingestion source** → add a row to `INGESTION-DASHBOARD.md`,
     create `sources/<src>/` + its extraction-audit; mark it **"of
     interest"** if it's a priority (e.g. the P1 sources).
   - **yaml** → the P2KB set is single; a "new element" is usually a new
     sub-area, handled as `P2KB-CORRECTION-FINDINGS` entries, not a new
     register.
   - a genuinely new **head/work-type with no register** → stop and
     discuss standing up a new register with {{USER_NAME}} (rare).
4. Set `active_element` and proceed into §5.

## 7. Setting work aside (switch ritual)

When {{USER_NAME}} says set-aside / switch:

- **Flush state to the standing docs** — outstanding work reflected in
  `P2KB-CORRECTION-FINDINGS` / the dashboard row / the manual's notes — and
  **commit meaningful work** so the git history carries the "what/when"
  (that IS the breadcrumb; we keep no separate one).
- Update `active_element` to the new target (or clear it if stopping).
- Re-enter at §1 for the new pickup.

## Note — this supersedes CLAUDE.md "Session Start"

This skill is the mandatory session-start ritual; it subsumes the bare
`context_resume` + "what do you want to work on?" with the head-aware,
register-backed flow above. CLAUDE.md's Session Start points here.

## Known-open (working-draft seams)

- YAML head's version/plan/spec homes are still `TBD` in
  `HEAD-DISPATCH-DRAFT.md`.
- Plan-dir consolidation and cross-head detection (a manual sourced from
  an ingestion pass) are unsettled.
- Parked initiative tracked in the dispatch draft: **P1 stabilization**
  (complete P1 manual + deSilva P1 tutorial ingestion → basic P1 YAML set).
