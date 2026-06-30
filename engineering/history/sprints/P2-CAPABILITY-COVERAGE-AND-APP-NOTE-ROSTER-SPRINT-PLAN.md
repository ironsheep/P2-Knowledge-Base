# P2 Capability Coverage & App-Note Roster — Sprint Plan

> **Status:** ✅ **CLOSED 2026-06-30** — all 9 commitments SHIPPED; plan certified.
> Closeout audit: `engineering/history/sprints/2026-06-30-P2-CAPABILITY-COVERAGE-AND-APP-NOTE-ROSTER-CLOSEOUT.md`.
> Committed in `fb7f8948`. (Authored 2026-06-29 via `sprint-plan`; §Open Questions all
> confirmed; executed same day → 2026-06-30.)

This sprint indexes the P2's *community-artifact landscape* (Quick Bytes,
OBEX) onto a single capability axis, refreshes OBEX, makes our skills aware of
the resulting **four-artifact model**, and produces a **ranked, placement-routed
proposed roster of P2 app notes** — derived by contrasting that landscape with
what the P1 app notes covered.

---

## § Open Questions — ✅ ALL CONFIRMED (Stephen, 2026-06-29)

All five resolved in favor of the recommendation. Planning gate closed.
Retained below as the decision record.

1. **Plan vs. study boundary — where does this sprint stop?**
   The sprint ships concrete artifacts (spine, Quick Bytes catalog, OBEX
   refresh, skill updates). **Phase 6's coverage matrix + proposed roster is an
   *analysis deliverable*** (a proposal doc in `engineering/analysis/`), and
   **authoring the proposed app notes is a separate downstream effort.**
   *Recommendation:* keep this one connected sprint **through phase 6 (the
   proposal)**, and carve out *app-note authoring* as a named follow-on sprint.
   The roster is the deliverable here, not the app notes themselves.

2. **Quick Bytes serving mechanism — index file first, or MCP verbs now?**
   OBEX gets dedicated `p2kb_obex_*` MCP verbs. Quick Bytes could mirror that
   (`p2kb_qb_*`, work in the p2kb-mcp server project) or ship as a published
   catalog under `deliverables/ai/P2/community/quick-bytes/` that agents fetch.
   *Recommendation:* **published catalog first** (no new MCP surface); add verbs
   later once the shape is proven and agents are reaching for it. Mirrors how
   OBEX matured.

3. **Homes for the new durable artifacts.**
   - Capability **spine** (the taxonomy) → *recommend*
     `engineering/standards/p2-capability-taxonomy.md` (a durable, cross-head
     classification asset).
   - **Placement rubric** (what-belongs-where) → *recommend*
     `engineering/standards/documentation-standards/artifact-placement-rubric.md`.
   - **Quick Bytes served catalog** → *recommend*
     `deliverables/ai/P2/community/quick-bytes/` (mirror the OBEX layout).
   - **Coverage matrix + roster** → *recommend* `engineering/analysis/`
     (analysis, not a shipped deliverable).

4. **App-note YAML-companion schema — design here or in the authoring sprint?**
   *Recommendation:* **record the decision now** (an app note = human doc **+**
   structured YAML companion), but **design the schema + emit-mechanism in the
   downstream authoring sprint**, piloting it on the existing **P2AN000** draft.
   This sprint only commits to the *principle* shaping the roster's framing.

5. **OBEX SD/flash driver publish — prerequisite ordering.**
   Your microSD, flash-filesystem, and dual drivers should land in OBEX
   **before** the phase-4 re-scrape so they flow into the catalog automatically
   and *close the FAT-filesystem false-gap*. *Recommendation:* treat "publish
   the three drivers to OBEX" as a **you-owned prerequisite to phase 4** (not a
   task this sprint executes, since OBEX submission is a Parallax-side action).

---

## Sprint-start record (2026-06-29)

Started via the `sprint-start` skill. Entry state pinned at execution time:

- **Head/element:** `quickbytes:quick-bytes` (primary, originating head) —
  **cross-head**: also refreshes `obex` and produces a document-production
  app-note roster. Recorded so downstream skills resolve to this element.
- **Build number:** **version-less sprint** — its character is
  ingestion/landscape + new standards docs + skills infrastructure (gate-
  governed, not released). The only versioned sub-artifact is the **OBEX
  integration catalog**: phase 4's re-scrape ships it as **v2.1 → v2.2**
  (recorded in `OBEX-INTEGRATION-COMPLETE.md`). No other version moves.
- **Working-tree audit:** sprint blast radius
  (`planning/standards/analysis/community/skills`) **clean** — only this plan
  doc was untracked (the foundation). Out-of-scope pre-existing changes (HUB75
  datasheet `.md`→dir conversion; xbyte `REF-NO-COMMIT/`) left as-is per
  Stephen; `REF-NO-COMMIT` is intentionally uncommitted.
- **Tracking-readiness:** **READY.** Context pruned **105 → 26** keys (79 dead
  closed-sprint checkpoints cleared; full backup
  `tasks/backups/project_dump_20260629_221513.json`). Stranded `#129`
  (assembly) paused. `#110`/`#54`/`#46`/`#47` remain paused/pending, out of
  scope. MEMORY.md 96 lines (healthy).
- **Entry baseline (YAML head):** **GREEN** — `verify-yaml-format.py` 1060/1060
  parse clean; `validate-crossref-keys.py` all resolved (exit 0). No failure
  groups. *Caveat:* new phase-3 QB catalog files may read as unresolved
  crossref targets until an index regen (indexing artifact, not regression) —
  the exit baseline accounts for this.

---

## Foundational model — the four-artifact shape

Everything downstream classifies against this. The four artifact types sit on
one spectrum of **increasing pedagogical depth and increasing authorship/trust
commitment:**

| Artifact | Pedagogical role | Authored by | What an agent gets |
|---|---|---|---|
| **OBEX object** | A reusable *part* — drop it in | Community | Catalog entry + download link |
| **Quick Byte** | A *worked demonstration* of one task (multi-modal); light on *why* | Parallax | Catalog entry + modality links |
| **App note** | *Guided composition* — combining subsystems to solve a task, with the *why* | **Us** | Catalog entry + **full structured YAML companion** |
| **Manual** | *Systematic reference* for a whole subsystem | **Us** | Already YAML-backed (the KB *is* the source) |

Three principles fall out, and each shapes a phase below:

- **Placement rubric (what belongs where & why).** A driver/part → OBEX. A
  "show it working" task → Quick Byte (Parallax's to author; we route to it). A
  recurring task needing *guided composition + why* → **app note** (ours). A
  foundational subsystem under-covered → **manual** gap. The sharp test:
  *an app note solves a **problem** by composing subsystems; a manual section
  documents a **subsystem** completely.*
- **Format-donor principle (how Quick Bytes inform app-note structure).** Quick
  Bytes are Parallax's *deliberate replacement* of the P1 app-note format —
  they encode lessons (task-framing, runnable code at the center, video,
  discoverability, brevity). Our app notes **fuse Quick Byte ergonomics with
  app-note depth** — *don't clone*. Their *existence* also pushes our app notes
  *up the depth axis* (don't duplicate the "just show it" tier Parallax fills).
  So Quick Bytes become a **second pattern donor** — a *format/structure* donor
  — alongside the P1 app notes (the *voice/depth* donor we already profiled in
  `P1-DOCUMENT-LINEAGE`).
- **App-note = doc + YAML companion (first-party → we can serve content, not
  just a pointer).** Because we author app notes, we can trust-stamp and serve
  their content as structured YAML — unlike community OBEX/Quick Bytes, which we
  only catalog. The companion is a **digest + links**, never a prose clone:
  task identity, spine classification, the *composition recipe* (links to the
  primitive YAMLs it uses, not re-descriptions), a reference to the runnable
  validated code, parameters/pin-maps, prerequisites, gotchas. The prose *why*
  stays in the human doc. Drift control: **one authoring act emits both**, with
  an agreement audit (like the manual↔YAML drain gate).

---

## The capability spine (draft — phase 1 finalizes)

One axis every artifact classifies against, reconciled from OBEX categories +
Quick Bytes tags + P1 app-note topics + P2 architecture:

| Domain | Leaf topics (illustrative) |
|---|---|
| **A. Core compute model** | cogs/multicore, task scheduling, execution timing, stack, coroutines→multitasking, inline PASM, data structures |
| **B. Smart Pins & I/O** | pin modes, ADC, DAC, PWM, freq/edge measurement, Schmitt/comparator, counters-equivalents |
| **C. Math & DSP** | CORDIC, fixed/float, Goertzel, filtering, FFT |
| **D. Streaming & video gen** | streamer, pixel/HDMI/VGA generation, DMA-like patterns |
| **E. Comms & protocols** | UART, I2C, SPI, 1-Wire, wireless (XBee/ESP), IoT gateway, PC-host comm |
| **F. Sensors & environment** | temp/humidity, GPS, distance/ultrasonic, light, RTC |
| **G. Displays & graphics** | VGA/DVI/HDMI text+image, LCD/e-ink, LED matrix/NeoPixel, terminal/ANSI, GUI menus/window-manager |
| **H. Motors & motion** | servo, BLDC, encoders, robotics |
| **I. Storage & memory** | onboard flash, SD/FAT, external RAM |
| **J. Audio** | sound engine, DAC audio |
| **K. Dev tools & workflow** | toolchain setup, templates, DEBUG, programming/loading |

**Key early signal:** the P1 app notes leaned a third of their list into the
*compute-model* domain (counters, abstract data structures, execution time,
multicore template, coroutines, stack) — exactly the P2's steepest learning
curve (smart pins, 8 cogs, CORDIC, streamer, native multitasking). Domain A is
the richest predicted vein of app-note gaps.

---

## Phase 1 — Lock the capability spine + four-artifact model *(design keystone)*

**Why.** Every downstream phase classifies against the spine and routes through
the placement rubric. Index Quick Bytes in a QB-only vocabulary and we'd re-map
later; this phase prevents that.

**Starting point.** Draft spine above; inputs are OBEX's 9 categories
(`deliverables/ai/P2/community/obex/objects/*.yaml` → `functionality.category`),
Quick Bytes' 21 tag categories
(`engineering/ingestion/sources/quick-bytes-discovery-manifest.md`), the 17 P1
app-note titles (this sprint's input), and the P2 architecture areas
(`deliverables/ai/P2/architecture/`).

**Target.** Three durable docs (homes per Open Q3):
1. `p2-capability-taxonomy.md` — the spine, with leaf topics + a one-line
   definition each, and a mapping note for each source vocabulary (OBEX cat →
   domain, QB tag → domain).
2. `artifact-placement-rubric.md` — the four-artifact spectrum + the routing
   decision tree + the app-note-vs-manual sharp test.
3. A short **format-donor + app-note-companion decision record** (can live in
   the taxonomy doc or the app-note doc-class folder) capturing the two
   principles so phase 2/3/6 reference one source.

**Integration points.** Phase 2 (skills cite these docs), phase 3/4/5 (classify
against the spine), phase 6 (rubric routes gaps).

**Verification.** *Normal:* every OBEX category and every QB tag maps to exactly
one domain (no orphans). *Edge:* a multi-tag artifact lands on a primary domain
plus secondaries (the schema must allow >1). *Error:* a P2-unique capability
(CORDIC, streamer) with no P1/OBEX/QB source still has a domain — the spine is
P2-complete, not just a union of the source vocabularies.

---

## Phase 2 — Operationalize the four-artifact model in the project skills *(readiness)*

**Why.** The model is only real if the skills that manage each artifact encode
it. This phase makes the skills *ready to run* before we touch the artifacts.

**Constraint (standing rule).** I **edit in-repo `.claude/skills/` overlays**
directly; **central skills get change *proposals*** appended to
`feedback_skill_evolution_candidates.md` for the maintenance agent. Two output
channels, never edit central in place.

**Starting point — skills that touch each artifact:**
- `whats-next` (`.claude/skills/whats-next/SKILL.md`) + `HEAD-DISPATCH-DRAFT.md`
  — the heads board lists `quickbytes` and `obex`; **app notes are not yet a
  recognized artifact/element.** Needs: the four-artifact model + where app
  notes sit (document-production sibling of manuals) + the placement rubric
  pointer.
- `ingest-source` / `ingest-conductor` — Quick Bytes indexing and the OBEX
  re-scrape route through ingestion-shaped processes; they should know the
  catalog-entry (not full-ingest) model for community artifacts.
- Document-production skills (`prepare-manual`, `release-manual`,
  `document-audit`, `document-finalize`) — must recognize the **app-note doc
  class** and the **doc+YAML-companion agreement gate**.
- `yaml-knowledge-base-maintenance` — the app-note YAML companion is
  first-party and lives in `deliverables/ai/P2/`; this skill governs it.

**Target.** In-repo `project-overlay.md` additions (or edits) encoding: (a) the
four-artifact model + trust tiers, (b) the placement rubric pointer, (c) the
app-note doc+YAML-companion requirement + agreement gate, (d) app notes as a
first-class document-production artifact in the head-dispatch model. Central-skill
gaps → evolution-candidates buffer.

**Integration points.** Consumes phase 1's docs; readies phases 3–6 and the
downstream authoring sprint.

**Verification.** *Normal:* invoking `whats-next` resolves an app-note element
and routes it correctly. *Edge:* a community-artifact task (QB/OBEX) routes to
catalog-entry handling, not full trust-chain ingestion. *Error:* an attempt to
author an app note without its YAML companion is caught by the agreement gate.

---

## Phase 3 — Quick Bytes: modality-aware served catalog + format-donor harvest

**Why.** The originating ask: a master list so agents discover Quick Bytes the
way they discover OBEX — *and* the format-donor harvest for app-note structure.

**Starting point.** Discovery is essentially done — all **42** Quick Bytes with
title/URL/date/tags in
`engineering/ingestion/sources/quick-bytes-discovery-manifest.md`. Missing
per-entry: confirmed code-availability, download-ZIP URL(s), author, YouTube
link. The scraper exists:
`engineering/tools/quick-bytes-integration/scrape-quick-bytes.py` (fetches index
pages 1–2, per-page extraction; note its default output dir is the *transient*
`engineering/knowledge-base/...` tree — retarget to the served deliverables
home). Partial code already pulled for two boards under
`engineering/ingestion/sources/quick-bytes-code/`.

**Target.**
1. **Served catalog** — one YAML per Quick Byte under
   `deliverables/ai/P2/community/quick-bytes/` (mirror OBEX), each carrying:
   `teaching-intent` (spine domain + leaf), title/URL/date/author, **modalities
   present** (article always; video link; source: download URL(s) + language +
   `has-code` + **`auth-gated`** flag; reference links), cross-links (matching
   OBEX object ID(s), related add-on board(s), related KB concepts), and type
   (reusable-object vs procedural how-to). **Code is linked, not adopted** — no
   community code into the trust-stamped tree.
2. **Format-donor profile** — in the same page-fetch pass, extract Quick Bytes'
   structural DNA (page sections) into a donor profile for the app-note doc
   class; **critically filtered** to keep pedagogical structure and discard
   marketing/board-CTA structure.

**Integration points.** Feeds the QB column of the phase-6 matrix; the donor
profile feeds the downstream app-note doc-class work; Open Q2 governs serving.

**Verification.** *Normal:* all 42 entries classified to a spine domain with
modality flags; a sample of download/video URLs resolve (200). *Edge:*
auth-gated downloads (e.g. simpleSound) are flagged, not failed. *Error:* a
multi-download Quick Byte records all ZIPs; a procedural (no-code) Quick Byte is
marked, not dropped.

---

## Phase 4 — OBEX refresh + spine map

**Prerequisite (you-owned, per Open Q5).** microSD / flash-filesystem / dual
drivers published to OBEX so they ride the re-scrape.

**Why.** The matrix must reflect *current* OBEX, not the 2025-09-12 baseline —
and the OBEX head's freshness is overdue on its own merit.

**Starting point.** 113 served objects under
`deliverables/ai/P2/community/obex/objects/*.yaml`; last scan **2025-09-12**
(`engineering/obex-integration/OBEX-INTEGRATION-COMPLETE.md`). Re-scrape tooling:
`engineering/tools/obex-integration/scrape-obex-repos.py`.

**Target.**
- **4a — Re-scrape → delta vs the 2025-09-12 baseline.** Surface new/changed
  objects, refresh the served catalog, note any new adoption requests. Confirm
  the three new drivers landed.
- **4b — Map current OBEX onto the spine.** Lightweight — objects are already
  categorized; add the domain/leaf classification.

**Integration points.** Feeds the OBEX column of the phase-6 matrix; advances
the OBEX head's delta-since-baseline state.

**Verification.** *Normal:* delta count reconciles (new objects since Sept
appear; the three drivers present). *Edge:* a changed (not new) object updates
in place, no duplicate. *Error:* P1-only objects stay filtered (the catalog is
100% P2-specific).

---

## Phase 5 — Map the P1 app notes onto the spine

**Why.** The P1 column is one of four matrix inputs and seeds the
"P1-had-it/P2-lacks-it" gap direction.

**Starting point.** The 17 titles supplied this sprint (`01-Counters`,
`AN002`–`AN019` with gaps at AN016/AN017), plus any ingested P1 app-note content
already profiled as a pattern donor (`P1-DOCUMENT-LINEAGE`,
`project_p1_pattern_donors_for_p2_authoring`).

**Target.** Each P1 app note classified to a spine domain/leaf, with a one-line
"P2-equivalent capability" note (e.g. P1 counters → P2 smart pins; P1 coroutines
→ P2 native multitasking) — since many P1 topics *transform* rather than map
straight across.

**Integration points.** Feeds the P1 column of the phase-6 matrix.

**Verification.** *Normal:* all 17 classified. *Edge:* a P1 topic with no clean
P2 analogue (e.g. external-SRAM-over-SPI → HyperRAM) is recorded as a
*transform*, not a 1:1 map. *Error:* a P1 GUI-series multi-part note (AN004/005/013)
is captured as a series, not collapsed to one row.

---

## Phase 6 — Coverage matrix → ranked, placement-routed app-note roster *(analysis deliverable)*

**Why.** The payoff: contrast the four corpora, find the holes, and route each
to its correct *form*.

**Starting point.** The classified corpora from phases 3–5 + existing manual
coverage (`deliverables/ai/P2/` guides/architecture/language) + the placement
rubric from phase 1.

**Target.** In `engineering/analysis/`:
1. **Coverage matrix** — rows = spine leaves; columns = P1 app note? / OBEX /
   Quick Byte / manual coverage; cells = what exists.
2. **Proposed P2 app-note roster** — **ranked** (learning-curve impact × gap
   severity) and **routed through the placement rubric** so each gap lands as:
   *app note* (ours to author), *manual* gap (chapter, not app note), *OBEX
   adoption request*, or *Quick Byte suggestion* (Parallax's to author). The
   roster explicitly **contrasts what belongs where and why** — the editorial
   discipline you asked for.
3. **Bidirectional coverage** — gaps surfaced from *both* the P1 column
   (had-it/lack-it) *and* the P2 side (P2-unique capabilities — CORDIC,
   streamer, HDMI, USB — with no P1 precedent yet needing guidance).

**Integration points.** The roster feeds the carved-out **app-note authoring**
follow-on sprint (and the existing app-note doc class / P2AN000).

**Verification.** *Normal:* every spine leaf has a matrix row; every proposed
roster item carries a rank + a placement verdict. *Edge:* a "gap" already filled
by a not-yet-indexed artifact (the SD/flash drivers) is *not* false-flagged —
the rubric checks against the refreshed corpora. *Error:* a P2-unique capability
with no P1 row still surfaces as a candidate from the P2 side.

---

## Carved-out follow-on (not this sprint)

- **App-note authoring sprint** — author the top-ranked roster items, design +
  implement the **app-note YAML-companion schema + emit-mechanism**, pilot on
  **P2AN000**. Pulled out per Open Q1/Q4.
- **`p2kb_qb_*` MCP verbs** — add the Quick Bytes serving verbs once the catalog
  shape is proven (per Open Q2).

---

## File / artifact table (new + touched)

| Path | Action | Scope |
|---|---|---|
| `engineering/standards/p2-capability-taxonomy.md` | create | The spine (Open Q3) |
| `engineering/standards/documentation-standards/artifact-placement-rubric.md` | create | The placement rubric (Open Q3) |
| `deliverables/ai/P2/community/quick-bytes/*.yaml` | create | 42 served catalog entries |
| `engineering/analysis/` (matrix + roster docs) | create | Coverage matrix + proposed roster |
| `.claude/skills/*/project-overlay.md` | edit | Four-artifact model into in-repo overlays |
| `.claude/skills/whats-next/SKILL.md`, `HEAD-DISPATCH-DRAFT.md` | edit | App notes as a first-class artifact |
| `feedback_skill_evolution_candidates.md` | append | Central-skill change proposals |
| `deliverables/ai/P2/community/obex/objects/*.yaml` | refresh | Re-scrape delta + spine classification |

> Per the sprint-plan overlay: the only **P2KB-YAML-set** edits here are the
> *served catalogs* (Quick Bytes new, OBEX refresh) — these are
> catalog-metadata, not language/architecture YAML changes, so they don't carry
> the same "design decisions to flag" gate as a content-YAML sweep. The
> **app-note YAML companion** *would* trigger that gate — and it's deferred to
> the authoring sprint, where its schema is a flagged design decision.

---

## Section ↔ task cross-reference

Tasks generated 2026-06-29 (`plan-to-tasks`), sprint tag **`cap-coverage`**.

| Plan § | Deliverable | Task | seq |
|---|---|---|---|
| Phase 1 | Lock capability spine + four-artifact model (3 docs) | «#130» | 13 |
| Phase 2 | Operationalize the model in project skills | «#131» | 14 |
| Phase 3 (3a) | Quick Bytes modality-aware served catalog | «#132» | 15 |
| Phase 3 (3b) | Quick Bytes format-donor profile | «#133» | 16 |
| Phase 4 (4a) | OBEX re-scrape delta vs 2025-09-12 (→ catalog v2.2) | «#134» | 17 |
| Phase 4 (4b) | Map OBEX onto the spine | «#135» | 18 |
| Phase 5 | Map the 17 P1 app notes onto the spine | «#136» | 19 |
| Phase 6 (6a) | Coverage matrix | «#137» | 20 |
| Phase 6 (6b) | Ranked, placement-routed app-note roster | «#138» | 21 |

> External prerequisite to «#134»: Stephen publishes the microSD / flash /
> dual drivers to OBEX. Carved-out follow-on (not this sprint): app-note
> authoring + YAML-companion schema (pilot P2AN000); `p2kb_qb_*` MCP verbs.
