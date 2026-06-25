# Per-head sentinel dispatch — DRAFT (pre-brainstorm)

> **STATUS: working dispatch table.** The 2026-06-05 Work Type Routing
> brainstorm has happened (its outcomes are recorded below); most cells are
> now resolved. The remaining `TBD` cells + the "Open items still to settle"
> list at the foot are the genuine unfinished seams — do not treat those as
> settled. (The filename keeps its `-DRAFT` suffix only because `whats-next`
> and the per-head overlays reference it by that name; renaming would break
> those refs.)

## Why this file exists

`skill-conventions.md` stores several slots as **per-head routing
sentinels** (`<per-head — …>`) because P2-Knowledge-Base is **five heads**
under one repo — manual, yaml, ingestion, obex, quickbytes (see `whats-next`
and the conventions file's preamble). A sentinel keeps a
central skill's Step 0a from hard-stopping (the slot is *present*), which
lets Step 0b load that skill's `project-overlay.md`. The overlay's job is
to **resolve the sentinel for the head currently being worked.** This file
is the shared resolution table the overlays point at, so the logic lives
in one place.

This is the same primitive as `CLAUDE.md`'s **Work Type Routing** table —
"which head am I in, and where do that head's artifacts live."

## Step 1 — Identify the head and the element

**Read the `active_element` pointer first.** The `whats-next` front-door
skill sets a todo-mcp context key `active_element` = `head:element` (e.g.
`manual:p2-streamer-guide`, `yaml:p2kb`, `ingestion:p1-propeller-manual`)
on pickup. Per-head overlays resolve their sentinels for *that* element:

```
mcp__todo-mcp__context_get key:"active_element"
```

**Fallback (key unset):** infer the head from the work target (the
file/dir the sprint or task acts on) using the table below, and prompt to
set `active_element` so downstream skills stay consistent.

| Head | Detection | "Element" the artifacts attach to |
|------|-----------|-----------------------------------|
| **MANUAL** | target under `engineering/document-production/manuals/<m>/` or `…/workspace/<m>/` | that manual — **publication** (in `PUBLICATION-ROSTER.md`) or **instrument** (workspace folder only, e.g. P2 Layout Torture Test; no version; state wherever it records runs — forge interactive-testing is one example, not the rule; purpose traces to the effort/sprint it serves) |
| **YAML (KB-for-agents)** | target under `deliverables/ai/P2/` (the P2KB YAML set) | the P2KB data set |
| **INGESTION** | target under `engineering/ingestion/sources/<src>/` | that ingestion source |
| **OBEX** | target under `engineering/obex-integration/` (the single catalog) | the OBEX catalog — one element (`obex:catalog`); state in `obex-integration/README.md` + last-release date |
| **QUICKBYTES** | target under `engineering/quickbytes-integration/` (the single corpus) | the Quick Bytes corpus — one element (`quickbytes:quick-bytes`); **parked / not processed** (see `quickbytes-integration/README.md`) |

**OBEX and QUICKBYTES are single-element heads** (one catalog / one corpus).
Their state lives in their integration `README.md`, and `whats-next` is the
authoritative spec for both. They do **not** resolve the Step-2 sentinel
table below — that table is for the versioned / release-bearing heads
(manual, yaml). The Step-2 columns are intentionally left at manual / yaml /
ingestion.

Cross-head work (e.g. a manual whose content is sourced from an ingestion
pass) — resolution rule **TBD** (brainstorm).

## Step 2 — Resolve the sentinel from the head

| Sentinel slot | MANUAL | YAML (KB) | INGESTION |
|---|---|---|---|
| `BUILD_VERSION_LOCATION` | the manual's `CHANGELOG.md` (+ `deliverables/documents/README.md` version line) | the YAML set's latest **git tag** (mirrored by the `deliverables/ai/P2` README badge + the YAML `CHANGELOG.md` top entry) — per `release-yamls` | **N/A — version-less** |
| `BUILD_VERSION_KEY` | latest version heading in the CHANGELOG | the latest git tag (= CHANGELOG top heading) | **N/A** |
| `BUILD_VERSION_EXAMPLE` | e.g. `2.3.0` | e.g. `v1.9.1` | **N/A** |
| `PLAN_DIR` | **RESOLVED — single unified dir `engineering/planning/` for all heads** (decided 2026-06-11; supersedes the former per-head sentinel; name the head/element in the filename) | ditto | ditto |
| `PUNCH_LIST_DOC` | the manual's punch list — **location TBD per manual** | `engineering/operations/P2KB-CORRECTION-FINDINGS.md` | the source's `README.md` (ingestion dashboard) row + `sources/<src>/<src>-complete-extraction-audit.md` |
| `RELEASE_NOTES_DOC` | the manual's `CHANGELOG.md` | the YAML set's `CHANGELOG.md` (top entry mirrors the git tag) | **N/A — uses completeness dashboard** |
| `SPEC_DOC` | the manual's `creation-guide.md` (candidate) | **TBD** | **N/A — gates + dashboard instead** |

## Head-specific notes

- **INGESTION is the odd head.** No version, no release notes, no spec.
  Governed by ingestion-quality / cross-reference / audit **gates** plus a
  completeness **dashboard** (dashboard location **TBD**). A central skill
  step that asks for version/release-notes/spec on the ingestion head
  should report "not applicable for ingestion" rather than inventing one.
- **Punch-list lifecycle is uniform across heads:** complete an item →
  sweep it to a dated archive (`PUNCH_LIST_ARCHIVE_PATTERN`); the live
  copy holds only outstanding work. `P2KB-CORRECTION-FINDINGS.md` (the
  YAML head's punch list) gets this same lifecycle.

## Brainstorm outcomes — session model (2026-06-05)

### The work pattern this serves

~70% single-head run-to-completion; ~30% interleaved — progress a head,
set it aside, pick another; occasionally run one straight to completion
then return to a parked head. The mechanism must let a head be **set aside
without losing the thread** and **resumed cleanly.** (Recent months have
been almost entirely the YAML and manual heads.)

### Active element — one lightweight pointer

A single todo-mcp **context key** (`active_element`) names the current
element. Its value identifies the head + element, from which the relevant
**register / state-doc** is known (publication roster | ingestion
dashboard | P2KB correction-findings). That is the *only* thing we
actively store. Set on pickup, updated on switch.

### Heads-in-flight — verified, not tracked

We do **not** maintain a separate heads-in-flight list. At pickup:

1. Identify the target head/element.
2. **Verify it against the registries.** Current focus (YAML + manuals)
   makes the two primary registries `engineering/operations/P2KB-CORRECTION-FINDINGS.md`
   and `engineering/document-production/PUBLICATION-ROSTER.md`. Consult
   `engineering/ingestion/README.md` when turning to
   ingestion — and update it as we move on (per `INGESTION-UPDATE-WORKFLOW.md`).
3. **Found → resume** that element. **Not found → the add-new-element
   process** — decide whether we're genuinely adding a new head/element;
   if so, register it in the right place (roster / dashboard) or stand up
   a new register.

### Per-element state — read the standing docs, don't duplicate

"Where we left it" is reconstructed from the element's standing doc, never
a tracker:

- **Manual** → the roster points to the manual; the manual's folder
  content (CHANGELOG, `audit/`, working notes) describes its state and
  what was last in progress.
- **Ingestion source** → the dashboard row (completeness %, gate status)
  says where we are; `<src>-complete-extraction-audit.md` carries detail.
- **YAML (KB)** → `P2KB-CORRECTION-FINDINGS.md`: **empty ⇒ everything
  published / nothing outstanding; non-empty ⇒ that is the to-do list.**

### Breadcrumb — none; reconstruct

No separate breadcrumb store. "What did we work on last, and when" already
lives in the **git commit history**; outstanding work lives in the
**standing docs** above; genuinely mid-stream uncommitted work shows in
the **git working tree**. `active_element` + those three reconstruct the
resume picture. (Revisit only if a real gap appears.)

### The front door — a session-start skill (to build)

A **project-baked front-level skill**, hit first when deciding what to do
on return. Responsibilities:

- Read `active_element`. If set: report "here's what you've been working
  on" — name the element, resolve its standing-doc state (outstanding
  items / completeness / recent commits), and offer to resume.
- If picking up something else: verify the target against the registries
  above. Known → set it active, resume. Unknown → add-new-element process.
- Keep `active_element` current.

This **formalizes and upgrades** `CLAUDE.md`'s current mandatory
session-start (`context_resume` + "what do you want to work on?") into a
head-aware, register-backed version — the stateful evolution of the old
"What are we working on today?" prompt.

### Parked initiative — P1 stabilization (~30% community drag)

P1 is a stable target (language, hardware, OBEX codebase all stable), so
it's worth completing as a basic device-support set:

- Complete ingestion of the **P1 manual** (`sources/p1-propeller-manual-v1.2`).
- Ingest the **deSilva P1 assembly-language tutorial** (`sources/desilva-p1-tutorial`).
- From those, develop a **basic P1 YAML set.**

The ingestion dashboard should mark these P1 sources as **of interest**;
the other ingestion sources are all P2 and in reasonable state (none
currently "of interest"). Community pull here is lightweight (~30% drag),
comparable to the just-produced streamer manual.

## Manual-head taxonomy + plan model (2026-06-05)

The **manual head is not flat** — it has a *type*, and the work on it has a *scope*.

**Type — recorded in `PUBLICATION-ROSTER.md`, now the complete + authoritative registry:**
- **Live** — manual (6) or presentation (AI Privacy) — consistency-bound.
- **In development / parked** — intended; may be a pre-production walk-away
  (Spin2 Ref). *Not* orphaned (intent, not state, is the discriminator).
- **Instrument** — test/standards harness (P2 Layout Torture Test);
  manual-shaped, generates PDFs, never released; serves an effort. **Its
  analysis (`audit/`) is versioned with it** — an instrument's analysis is
  durable product, not transient release-audit, so its `audit/` gets a
  `.gitignore` exception (the general `manuals/*/audit/` ignore stays for
  publications).
- **Orphaned** — not carrying forward (Green Book, superseded by IO&SP).

Physical signals (the `workspace|manuals|outbound` folder triad, a generated
PDF) prove *existence/progress*, never *category* — instruments have both.
Category = intent, read from the roster. A folder with **no** roster entry =
**anomaly to reconcile**, not a guess.

**Scope of the work — plan location (resolves the `PLAN_DIR` sentinel + the
cross-element open item):**
- **single-element** sprint plan → co-located with its element (the manual's folder).
- **cross-element** sprint plan → co-located with the **effort** it serves (an
  effort has its own home). The all-manuals layout-standards plan lives in
  `engineering/document-production/methodology/`.

**Plans-in-flight** are a resumable unit alongside elements: `whats-next` can
resume an **element** *or* a **plan/sprint** (which declares its target
scope — one element or many). For cross-element work the *plan* is the thing in
flight, not any single element.

## Built this pass (2026-06-05)

- ✅ **`whats-next` front-door skill** — `.claude/skills/whats-next/SKILL.md`,
  including the **add-new-element process** (§6).
- ✅ **`active_element` wiring** — Step 1 above reads the pointer; per-head
  overlays inherit it.
- ✅ **CLAUDE.md Session Start** now invokes `whats-next`.

## Open items still to settle

1. YAML-head **spec** home (`SPEC_DOC`) — still TBD. (Resolved since: the
   YAML **version** home = the git tag, per `release-yamls`; the **plan**
   home = unified `engineering/planning/`; the **punch-list** =
   `P2KB-CORRECTION-FINDINGS.md`. Only the spec slot remains open.)
2. **Plan-dir model — internal contradiction to settle.** Step 2 (the
   `PLAN_DIR` cell) records it RESOLVED to a single unified
   `engineering/planning/` for all heads (2026-06-11), but the 2026-06-05
   "Manual-head taxonomy + plan model" section below still says single-element
   plans co-locate with the element and cross-element plans co-locate with the
   effort. **Decide:** does unified `engineering/planning/` fully supersede
   co-location, or do the two coexist? Then align both sections so the doc
   states one model.
3. Cross-head detection (a manual sourced from an ingestion pass).
4. Recorded cleanup debt (in `skill-conventions.md`): relocate punch-list
   content per head; stand up the corrections-register dated-archive flow.
