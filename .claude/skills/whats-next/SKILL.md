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

P2-Knowledge-Base is **several work-heads** under one repo (manual, yaml,
ingestion, obex, quickbytes — see the table below; `operations` is cross-cutting
infrastructure, not a work-head), and work is context-switchy (~70% single-head
run-to-completion; ~30% interleaved — progress a head, set it aside, pick
another, sometimes return). This skill is how we re-enter that work without
losing the thread. The glanceable cross-head map is `engineering/README.md`.

**The only state we actively store is one pointer:** the todo-mcp context
key `active_element`, value `head:element` — e.g. `manual:p2-streamer-guide`,
`yaml:p2kb`, `ingestion:p1-propeller-manual`. Everything else ("where was
I", "what's outstanding") is **reconstructed from standing docs and git**,
never duplicated into a tracker.

The work-heads, their registry, and their standing state (the glanceable
cross-head map is `engineering/README.md` — the heads board; this table is the
machine-readable dispatch detail):

| Head | Registry | Per-element standing state | Progress notion |
|------|----------|----------------------------|-----------------|
| **manual** | `engineering/document-production/PUBLICATION-ROSTER.md` (publications); workspace folder existence (in-dev / **instruments**) | the manual's folder — `CHANGELOG.md`, `audit/`, working notes; **instruments**: their own run artifacts (e.g. forge interactive-testing) | version (instruments: none) |
| **yaml** (P2KB) | the YAML tree / index | `engineering/operations/P2KB-CORRECTION-FINDINGS.md` (**empty ⇒ nothing outstanding**; non-empty ⇒ the to-do list) | version |
| **ingestion** | `engineering/ingestion/README.md` | dashboard row (completeness %, gates) + `sources/<src>/<src>-complete-extraction-audit.md` | completeness % + gates (no version) |
| **obex** | `engineering/obex-integration/README.md` | the integration record (`OBEX-INTEGRATION-COMPLETE.md`) + last-release date; outstanding = **delta vs the last-scan baseline** (2026-06-29, v2.2 · shipped in KB v1.13.3) | release version + delta-since-baseline (re-scan) |
| **quickbytes** | `engineering/quickbytes-integration/README.md` | the dashboard's state line (currently **NOT processed** — plans/scraper staged, ~15% discovered); single-element, parked | not-started → in-progress → integrated (parked at bottom) |

> **Single-element heads.** `yaml`, `obex`, and `quickbytes` are single-element
> (one P2KB set / one OBEX catalog / one Quick Bytes corpus), so their
> `active_element` is just `yaml:p2kb`, `obex:catalog`, `quickbytes:quick-bytes`.
> `manual` and `ingestion` are multi-element (one per manual / per source).
> **operations** is cross-cutting infrastructure (process + lessons-learned), not
> a resumable work element — it has no `active_element` form.

> **App notes + the four-artifact model.** App notes are a **document-production
> element alongside manuals** (not a separate head): target
> `engineering/document-production/app-notes/<n>/`, own doc class + version,
> resolved like a manual (`PUBLICATION-ROSTER` / its folder) but additionally
> shipping a **YAML companion** under a companion **agreement gate**. Together
> with `obex`, `quickbytes`, and `manual` they are the four P2 artifact types
> (part / worked-demo / guided-composition / systematic-reference). When a pickup
> targets any of them, the **artifact-type model** in `HEAD-DISPATCH-DRAFT.md`
> says how that type changes skill behavior; the **spine + placement rubric**
> under `engineering/standards/` are the authoritative specs.

## 1. Pull session state

- Run `mcp__todo-mcp__context_resume` — tasks + recent context.
- Read the pointer: `mcp__todo-mcp__context_get key:"active_element"`.

## 2. If `active_element` is set — report, then offer to resume

Parse `head:element` and resolve its standing-doc state from the table
above:

- **manual:`<m>`** — the `PUBLICATION-ROSTER` row + the manual's folder
  (CHANGELOG latest entry, `audit/` open findings, working notes), and the
  recent commits touching that manual (`git log --oneline -- <manual path>`).
  For a **manual-class instrument** (no CHANGELOG/version), state lives
  wherever *that* instrument records its runs — recognize the instrument by
  its workspace folder + the effort it serves, **not** by any one tooling
  path. For forge-driven instruments like the **P2 Layout Torture Test**
  that's the newest `engineering/pdf-forge/interactive-testing/test-runs/<name>-roundtrip-v*/`
  (`full-doc/output.pdf` = "generated") + the workspace `.md`'s latest edit;
  other instruments record elsewhere. "Where was I" = latest run + whether a
  visual-defect pass has run since.
- **yaml:p2kb** — read `P2KB-CORRECTION-FINDINGS.md`. Empty ⇒ "all
  published, nothing outstanding." Non-empty ⇒ the open findings ARE the
  to-do list; summarize the `CONFIRMED` / `NEEDS-VERIFICATION` counts.
- **ingestion:`<src>`** — the `INGESTION-DASHBOARD` row (completeness %,
  gate status) + the source's extraction-audit; recent commits under
  `sources/<src>/`.
  - **Wave form `ingestion:wave:<slug>`** (set by `ingest-conductor` for a
    parallel multi-source wave) — resolve state from the wave manifest in
    todo-mcp context (the conductor's per-source progress + gates), not a
    single source's extraction-audit. "Where was I" = which sources in the
    wave are done vs still outstanding.

Also surface any `in_progress` / next task from `context_resume` scoped to
the element's tag (`mcp__todo-mcp__todo_next tags:["<tag>"]`).

Then report plainly: **"Here's what you've been working on: `<element>` —
`<state summary>` — last activity `<recent commits>`. Resume this, or pick
up something else?"** Ask in chat (this repo has no AskUserQuestion).

## 3. If unset, or {{USER_NAME}} picks something else — choose a target

Determine the head + element to pick up (from what they say, or ask). This
is the head-pickup selection — the stateful evolution of the old "What are
we working on today?" prompt.

## 4. Verify the target against the registry

`PUBLICATION-ROSTER.md` is **complete and authoritative** — every
manual-shaped folder is categorized in it. Resolve the target's category,
then act:

- **manual** → find it in `PUBLICATION-ROSTER.md`:
  - **Live** (manual or presentation) or **In development / parked** →
    resume (§5).
  - **Instrument** → resume into the **effort it serves** (§5); never treat
    it as a publication, never add it to the live set.
  - **Orphaned (not carrying forward)** → do **not** silently resume.
    Confirm with {{USER_NAME}}: "this is retired (superseded/abandoned) — are
    we reviving it?" Proceed only on a yes.
  - **A `workspace|manuals|outbound/<name>` folder exists but has no roster
    entry** → **anomaly**, not a guess: surface it, have {{USER_NAME}}
    classify it, add it to the roster (preserving the "every folder appears
    once" invariant), then resume per its new category.
  - **No entry and no folder** → genuinely new → §6.
- **yaml** → one P2KB set; always exists. State via
  `P2KB-CORRECTION-FINDINGS.md`.
- **ingestion** → row in `README.md` (the dashboard)? (refresh per
  `INGESTION-UPDATE-WORKFLOW.md` when turning to ingestion).
- **obex** → single catalog; state via `obex-integration/README.md` (last
  release + whether a delta re-scan is due vs the 2026-06-29 baseline, v2.2).
- **quickbytes** → single corpus; state via `quickbytes-integration/README.md`
  (currently **NOT processed** — confirm intent before reviving; it's
  deliberately parked at the bottom of the queue).

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
   - new **ingestion source** → add a row to `README.md` (the dashboard),
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

- YAML head's **spec** home is still `TBD` in `HEAD-DISPATCH-DRAFT.md`
  (version = the git tag per `release-yamls`; plan = unified
  `engineering/planning/` — both now resolved there).
- Plan-dir model (unified `engineering/planning/` vs co-location) and
  cross-head detection (a manual sourced from an ingestion pass) are
  unsettled — see the dispatch doc's "Open items still to settle."
- Parked initiative tracked in the dispatch draft: **P1 stabilization**
  (complete P1 manual + deSilva P1 tutorial ingestion → basic P1 YAML set).
