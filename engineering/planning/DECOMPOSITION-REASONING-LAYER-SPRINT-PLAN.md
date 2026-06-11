# Sprint Plan — P2 Functional-Decomposition Reasoning Layer

**Head:** yaml (KB-for-agents) · **active_element:** `yaml:p2kb`
**Status:** STARTED 2026-06-11 — ships as KB `v1.7.0` (see Sprint-start record)
**Design rationale (companion):** `engineering/planning/DECOMPOSITION-LAYER-SYNTHESIS-PLAN.md`
(decisions D-A…D-E resolved there; this doc is the executable, deliverable-structured plan)

> **What this builds.** A new generative guidance layer under
> `deliverables/ai/P2/architecture/decomposition/` that teaches a consuming agent
> **how to derive an object/cog decomposition for an unfamiliar P2 hardware mix** —
> what P2 assets/features drive the cuts and how to make each decision — synthesizing
> the robot-dog force-set (architecture-discussion-000) under the authority-tier
> discipline (architecture-discussion-001). Corpus/object evaluation is a separate
> later pass and is **out of scope** here.

---

## Sprint-start record (2026-06-11)

- **Ships as: P2 Knowledge Base `v1.7.0`** — middle-version bump from the last KB
  release `v1.6.3` (commit `b0f48a8`), zeroing the patch digit. KB releases tag
  `vN.N.N` (distinct from manual tags). A KB-standards version dashboard is planned
  but not yet built; until then the version is read from the latest `v*` release
  tag/commit. Released via `release-yamls` (§17).
- **Entry baseline: GREEN** — `validate-yaml-syntax.py` clean; `validate-crossref-keys.py`
  resolves all 2,600+ refs, zero dangling. Closeout checks the exit baseline against this.
- **Working tree:** `deliverables/` blast radius clean/committed. Foundation committed
  at start = the two `engineering/planning/` docs + the `.claude/skill-conventions.md`
  PLAN_DIR unification. **NOT committed:** ingestion-head work-in-progress (the
  `*-PROTOTYPE.md`, `SPTutTItus/`, the `.gitignore` p2kb-update-requests rule, and the
  two operations/standards docs) — ingestion cleanup is in flight, left untouched.
- **Tracking:** the 5 tasks on the board belong to the parked `manual-layout-standards`
  sprint (other head) — left parked; none completed. This sprint's tasks are tagged
  for the **YAML** filter so `todo_next` processes only YAML work.

---

## A. Definitions that govern every authoring section (state once)

**A.1 — YAML schema to match** (from existing concept entries
`language/spin2/concepts/object_archetypes.yaml`,
`architecture/p2-architecture-mental-model.yaml`):
`concept` / `title` / `category` / `summary` / named-body-sections /
`related` (bare KB-root-relative **file paths**) / `see_also` (annotated camelCase
ids, `"desc: p2kbKey"`) / `oneliner`. **No tier field exists today** — we add one
(A.2).

**A.2 — Authority-tier field (D-A).** Each body section carries
`authority_tier: PHYSICS|PRINCIPLE|HEURISTIC|PATTERN|EXAMPLE`; where a section
genuinely mixes tiers, inline-tag the individual claims. The tier **selects the
grounding** (A.3).

**A.3 — Grounding policy + self-sufficiency (§4 / §4.1 of the design doc).**
- PHYSICS claim → cite an **internal P2KB path/key** (map in Appendix G).
- PRINCIPLE/HEURISTIC → cite the **durable reference canon** (author/title/year).
- EXAMPLE → **inlined, self-contained**, tagged illustrative-not-normative.
- **Never** reference a guiding/working doc (000/-001/handoff/this plan) or any
  relative path from shipped YAML; absorb the substance instead.

**A.4 — Per-entry Definition of Done (the verification model for every authoring
section below).**
- *Normal:* `validate-yaml-syntax.py` clean; `validate-crossref-keys.py` clean (all
  `related:` paths resolve); concept-style fields present; force entries carry the
  five required fields (`what_it_is`, `why_on_p2`, `how_it_cuts`, `example`,
  `failure_if_ignored`); every section `authority_tier`-tagged; entry appears in the
  regenerated index.
- *Edge:* every PHYSICS claim resolves to an Appendix-G citation; every HEURISTIC
  states an explicit escape condition; every EXAMPLE tagged illustrative; the
  generative test holds (vocabulary + forces + axes + invitations present).
- *Error (must be caught, not shipped):* a dangling `related:` path →
  `validate-crossref-keys`; a HEURISTIC with no escape condition → self-review/audit;
  an ungrounded PHYSICS claim → checked against Appendix G; any working-doc/relative
  reference → self-sufficiency check (A.3).

---

## 1. Scaffold the area + lock the authority-tier convention

**Why.** Every later section depends on a fixed schema and tier vocabulary.
**Starting point.** Schema exemplars at `language/spin2/concepts/object_archetypes.yaml`
and `architecture/p2-architecture-mental-model.yaml`; no `architecture/decomposition/`
dir exists yet.
**Target.** Create `deliverables/ai/P2/architecture/decomposition/`. Write the area's
`category` value and the `authority_tier` field spec (A.2) once, as a short convention
note the entries follow. Confirm the index generator (`generate-p2kb-index.py`) and
both validators accept the new area + the new field (stub-test with one minimal entry).
**Integration.** New `category` string; nothing references the area yet.
**Verification.** Validators clean on a stub entry; stub appears in regenerated index;
the new field does not break syntax/crossref validation.

## 2. Entry — `decomposition-glossary` (author first: shared vocabulary)

**Why.** Fixes canonical names so every other entry reconciles to one vocabulary
(000 §8 rule 1); carries the authority-tier legend and the reference-canon index.
**Source.** 000 §8 (glossary ask) + 001 §4.7 (canon, each name paired with the P2
mechanism it governs).
**Target.** Canonical-name map (Forces 1–4, C1–C5, the three planes); tier legend
(A.2); canon index (Parnas, Constantine/Yourdon, Page-Jones, Hoare CSP/occam, Kahn,
Lee & Messerschmitt SDF, GALS, Alexander, DDD, rate-monotonic) — each as a durable
bibliographic citation, each paired with the P2 mechanism it informs.
**Integration.** Every entry §2–§13 `see_also`-links here.
**Verification.** A.4; plus: every canon entry is a self-sufficient citation (no
working-doc reference), every canonical name used downstream resolves here.

## 3. Entry — `decomposition-method`

**Why.** The generative theory: forces = grammar, archetypes = vocabulary; shape is
*derived*, not chosen; decomposition is **two-axis** (logical + physical lattice).
**Source.** 000 §2–§3; 001 §4.1.
**Tiers.** PRINCIPLE-dominant.
**Grounding.** Physical-axis assets cite Appendix G (cogs, smart pins, CORDIC, locks,
hub, LUT, streamer); reasoning cites canon (Parnas, Constantine/Yourdon).
**Integration.** `related:` → `language/spin2/concepts/object_archetypes.yaml`,
`architecture/p2-architecture-mental-model.yaml`; `see_also:` → all force entries.
**Verification.** A.4; generative test explicitly satisfied.

## 4. Entry — `first-contact-procedure`

**Why.** The spine: the ordered observation→force routine an agent runs on unseen
hardware (enumerate wires → assign cog owners → map cadences/adapters → resolve
same-bus multi-rate via in-cog tasks → choose data-flow contracts → layer by
unit-conversion → place cross-cutting → reconcile to the hardest deadline).
**Source.** 000 §5–§6; 001 §4.5.
**Tiers.** PRINCIPLE/HEURISTIC (each ordering step that can be skipped states its
escape condition).
**Integration.** Each step `see_also`-routes to its force entry (§5–§12).
**Verification.** A.4; each step names the force it routes to and the observation
that triggers it.

## 5. Entry — `resource-ownership` (Force 1)

**Why.** Singular ownership as a **correctness rule**; singleton-vs-instance from
sharing topology.
**Source.** 000 Force 1.
**Tiers.** PHYSICS (OR'd pins / no bus mutex; atomic longs) → PRINCIPLE (one owning
cog per bus) → HEURISTIC (singleton when shared, instance when sole).
**Grounding.** OR'd-pins → `architecture/p2-architecture-mental-model.yaml` (pin_io)
+ `architecture/smart_pins.yaml` (pin_output_hierarchy); atomic long →
mental-model (hub_ram). Five required force-fields.
**Verification.** A.4; the PHYSICS line carries the Appendix-G pin-OR citation.

## 6. Entry — `data-flow-contracts` (Force 2 × three planes)

**Why.** The real inter-cog treatment (latest-wins+ack, lock-free single-writer
telemetry, freshness counters) crossed with the data/control/event plane model;
**when to choose which.** Replaces the blocking mailbox toy (superseded in §15).
**Source.** 000 Force 2; 001 §4.3.
**Tiers.** PRINCIPLE/HEURISTIC + one inlined EXAMPLE (the seq-bumped-last publish).
**Grounding.** No-OS/atomic-long → mental-model (inter_cog_communication, hub_ram);
locks → `architecture/locks.yaml`; cogatn → `architecture/cog_attention.yaml`.
Reasoning → CSP, Kahn.
**Integration.** `related:` → `language/spin2/patterns/implementation/spin2_mailbox_communication.yaml`
(the entry it supersedes, redirect wired in §15).
**Verification.** A.4; the three planes each graded; EXAMPLE tagged illustrative.

## 7. Entry — `rate-adaptation` (Force 3 + in-cog tasks)

**Why.** Clock-domain-crossing (rate-domain decoupling) + slew/easing as
object-worthy responsibilities — the missing half of "smart-pins-first"; plus
**cooperative tasks-within-a-cog** for one-bus-many-cadences (§4 tension).
**Source.** 000 Force 3 + §4 tension; 001 §4.3; canon SDF/GALS/Kahn.
**Tiers.** PRINCIPLE/HEURISTIC.
**Grounding.** Smart pins → `architecture/smart_pins.yaml`; streamer/FIFO →
`architecture/fifo.yaml` + `architecture/streamer/overview.yaml`; deterministic cogs
→ `architecture/cog.yaml`.
**Verification.** A.4; the in-cog-tasks resolution carries its escape condition.

## 8. Entry — `altitude-layering` (Force 4)

**Why.** Split by **unit conversion / axis of change**, not line/component count.
**Source.** 000 Force 4; canon Parnas (information hiding).
**Tiers.** PRINCIPLE/HEURISTIC (layer depth yields to tiny cog memory — escape
condition stated, grounded via Appendix G cog-RAM size).
**Verification.** A.4.

## 9. Entry — `cross-cutting-forces` (C1–C5)

**Why.** Objects that span/guard the tree: safety override, external-vocabulary
translation, per-unit config, testability seam, lifecycle/init order.
**Source.** 000 cross-cutting C1–C5.
**Tiers.** PRINCIPLE; C1 ties to cog independence (a hung cog keeps driving pins) —
PHYSICS grounded via Appendix G (cog.yaml).
**Verification.** A.4; all five placed with why/how-it-cuts/failure.

## 10. Entry — `spatial-computing` (FPGA-domain + smell catalog)

**Why.** The thesis: coarse-grained spatial fabric; assign function to space, think
in pipelines, push to the edge, latency-insensitive interconnect — **plus the smell
catalog** (funnel, hub saturation, timing-coupled cogs, poll/signal inversion,
over-locking).
**Source.** 001 §4.4; 000 failure modes.
**Tiers.** PRINCIPLE + HEURISTIC + an explicit SMELL set.
**Grounding.** Hub bandwidth/egg-beater → `architecture/hub.yaml`; deterministic
cogs → `architecture/cog.yaml`.
**Verification.** A.4; each smell names its detectable signature.

## 11. Entry — `evaluation-vocabulary` (judge a cut)

**Why.** The "judge a decomposition" toolkit absent from P2KB today:
coupling-as-integer, **connascence** (static/dynamic + P2 manifestations),
back-pressure-as-min-cut.
**Source.** 001 §4.2; canon Page-Jones (connascence), Constantine/Yourdon (coupling).
**Tiers.** PRINCIPLE.
**Grounding.** Dynamic-connascence-across-a-cog-boundary → jitter/races grounded via
Appendix G (cog determinism, hub timing).
**Verification.** A.4; each connascence type given a concrete P2 manifestation.

## 12. Entry — `resource-budget`

**Why.** The allocation table as a **required design artifact**; "out of cogs" =
"too coupled — re-cut."
**Source.** 001 §4.6; 000 §6.
**Tiers.** HEURISTIC/PRINCIPLE.
**Grounding.** The lattice counts (8 cogs, 64 smart pins, 16 locks, shared CORDIC,
LUT pairs, hub bandwidth) all cite Appendix G.
**Verification.** A.4; the budget template enumerates every finite resource with its
Appendix-G citation.

## 13. Entry — `worked-derivation-robot-dog` (EXAMPLE end-to-end)

**Why.** One narrated derivation, every step tagged with its force/plane decision —
the thing P2KB lacks (it has nouns and verbs, no whole-system derivation).
**Source.** 000 §7 + the cited robot-dog artifacts, **inlined self-contained**.
**Tiers.** EXAMPLE throughout; illustrative-not-normative banner.
**Verification.** A.4; **self-sufficiency is the sharp gate here** — the entire
derivation reads standalone with zero reference to 000 or any file path; each step
links to the force entry it exercises.

## 14. Pattern-boundary audit (D-E)

**Why.** Reconcile the new layer against the existing `language/spin2/patterns/`
library (separate from the 8 `patterns-analysis` files) — both directions.
**Starting point.** `language/spin2/patterns/pattern-index.yaml` +
`implementation/spin2_*`, `structural/*`, `applications/*`.
**Target.** A candidate list: (a) forces that imply a pattern the library lacks →
new-pattern candidate (e.g. latest-wins-with-ack contract; in-cog cooperative tasks;
slew/easing engine; rate-domain decoupler — none of which the library names cleanly);
(b) existing patterns to factor into / cross-link from the guidance. Recommendation
per candidate.
**Integration.** Cross-links land in §16; authoring whole new patterns is flagged as
a **scope decision for Stephen**, not silently absorbed.
**Verification.** *Normal:* every `implementation/structural/applications` pattern
classified (cross-link / new-candidate / leave). *Edge:* each new-pattern candidate
names the force that implies it. *Error:* a pattern left unclassified → audit
incomplete.

## 15. Supersession execution (D-C disposition + the three toys)

**Why.** Apply the agreed disposition without breaking inbound references
(Sacred Rule #7 — redirect, never silently delete).
**Starting point — exact inbound-reference lists in Appendix H** (from research).
**Target, case-by-case with Stephen:**
- `architecture/patterns-analysis/` — REPLACE×6 / REMOVE×1 (`memory_management`) /
  LEAVE×1 (`asm_integration`; log its P1 smells to the corrections register).
- The three toys in `language/spin2/patterns/`: `spin2_mailbox_communication`
  (blocking → add `superseded_by:` → §6, keep resolving), `few_objects` /
  `several_objects` (count taxonomy → retag toward depth+ownership, redirect).
- Log all P1-isms found in §7 study (cognew, CNT/waitcnt) to
  `engineering/operations/P2KB-CORRECTION-FINDINGS.md` regardless of disposition.
**Verification.** *Normal:* every inbound ref in Appendix H updated/redirected;
`validate-crossref-keys` clean. *Edge:* superseded keys still resolve (no 404 for a
consuming agent). *Error:* an orphaned `related:` after removal → caught by validator.

## 16. Cross-link wiring

**Why.** The layer must be discoverable from where agents already are, and must point
into the concrete vocabulary.
**Target.** Outbound `related:`/`see_also:` from new entries → grounded architecture
facts (Appendix G) + relevant `language/spin2/patterns/` entries (from §14). Inbound:
add `see_also:` to the new layer from `object_archetypes.yaml` and
`p2-architecture-mental-model.yaml` (the two altitudes 000 §1.1 says have a gap
between them).
**Verification.** A.4 across all touched files; round-trip — each new entry both
reachable from and reaching the existing tree.

## 17. Validation, index regen, release

**Why.** Ship the layer green.
**Target.** `validate-yaml-syntax.py` + `validate-crossref-keys.py` clean over the
set; **two-commit Path B** — content commit → `generate-p2kb-index.py` regen → index
commit (git-mtime dependency); then `release-yamls`; refresh local cache; verify by
**content probe** via p2kb-mcp (not version/counts).
**Verification.** *Normal:* validators clean, index regenerated, MCP serves a probe
of `decomposition-method` + the worked derivation. *Edge:* `validate-dod-release.py`
passes. *Error:* a stale-cache "verification failed" → restart MCP, re-probe (known
operational signature).

---

## Appendix G — PHYSICS grounding map (cite these for silicon facts)

| Fact | Cite (KB path : section) |
|------|--------------------------|
| 8 cogs / cog independence | `architecture/cog.yaml` (cog_independence); `…/p2-architecture-mental-model.yaml` |
| OR'd pins / no bus mutex | `architecture/p2-architecture-mental-model.yaml` (pin_io); `architecture/smart_pins.yaml` (pin_output_hierarchy) |
| CORDIC latency (~54–55 clk) / shared | `architecture/cordic.yaml` (pipeline_depth, result_latency); `language/spin2/concepts/cordic_solver.yaml` |
| 64 smart pins / autonomous modes | `architecture/smart_pins.yaml` (pin_count, independence) |
| Streamer + hub FIFO | `architecture/fifo.yaml`; `architecture/streamer/overview.yaml` |
| Adjacent-cog LUT sharing | `architecture/lookup_ram.yaml` (LUT_sharing; pairs 0-1,2-3,4-5,6-7) |
| 16 locks | `architecture/locks.yaml` (total_locks) |
| Hub egg-beater 8-clk rotation | `architecture/hub.yaml` (egg_beater_architecture.rotation_period) |
| No OS/IPC; hub+atomic+locks+cogatn | `architecture/p2-architecture-mental-model.yaml` (inter_cog_communication); `architecture/cog_attention.yaml` |
| Single-long hub R/W atomic | `architecture/p2-architecture-mental-model.yaml` (hub_ram) |

## Appendix H — supersession inbound-reference lists (redirect targets)

- **`spin2_mailbox_communication`** (`language/spin2/patterns/implementation/`): refs
  in `patterns/pattern-index.yaml:27`, `…/implementation/spin2_shared_memory.yaml:24`
  (combines_with), `…/concepts/method-pointers.yaml:240` (related).
- **`few_objects`** (`…/patterns/structural/`): `pattern-index.yaml:9`,
  `structural/no_objects.yaml:17`, `concepts/object_archetypes.yaml:479` (related).
- **`several_objects`** (`…/patterns/structural/`): `pattern-index.yaml:10`,
  `implementation/spin2_event_dispatcher.yaml:24`, `concepts/object_archetypes.yaml:480`,
  `architecture/patterns-analysis/memory_management_analysis.yaml:126`.
- **`patterns-analysis` files**: `cog_management` is a `category:` value on 6 method
  files (coginit/cogspin/cogid/cogstop/cogatn/cogchk — string tag, not a cross-ref;
  unaffected by file disposition) + 3 `combines_with`; `buffer_management`,
  `state_machine`, `timing_control`, `protocol_implementation` each referenced via
  `combines_with` across the `spin2_*`/applications patterns (full list captured in
  research output, in conversation history); `memory_management` 2 use_cases refs;
  `smart_pin_usage` / `asm_integration` — **no inbound refs** (safe to remove/leave).

---

## Notes for `plan-to-tasks`

- Sections **1–13** are the authoring spine (each = one task; shared DoD = A.4).
  Author in listed order (scaffold → glossary → method → procedure → forces →
  lenses → budget → worked example) so vocabulary and grounding are fixed before
  dependents.
- Section **14** (boundary audit) should run **before §16** (its output feeds the
  cross-links) and may surface a scope decision.
- Sections **15–17** are the close-out (supersession → wiring → validate/release);
  §15 is interactive (case-by-case with Stephen).
- Model: authoring (1–13) and the worked derivation are Opus-class (user-facing
  reasoning content); validation/index/release (17) is Sonnet-class mechanical.

---

## Section ↔ task cross-reference (generated by `plan-to-tasks`, 2026-06-11)

Sprint tag `decomposition-layer`; work filter `yaml_knowledge_base`. Run with
`todo_next tags:["yaml_knowledge_base"]` to walk these in `seq` order, isolated
from the parked manual-layout-standards tasks.

| Plan § | Deliverable | Task | seq |
|--------|-------------|------|-----|
| §1 | Scaffold area + authority-tier convention | «#6» | 2 |
| §2 | Entry `decomposition-glossary` | «#7» | 3 |
| §3 | Entry `decomposition-method` | «#8» | 4 |
| §4 | Entry `first-contact-procedure` | «#9» | 5 |
| §5 | Entry `resource-ownership` (Force 1) | «#10» | 6 |
| §6 | Entry `data-flow-contracts` (Force 2 × planes) | «#11» | 7 |
| §7 | Entry `rate-adaptation` (Force 3) | «#12» | 8 |
| §8 | Entry `altitude-layering` (Force 4) | «#13» | 9 |
| §9 | Entry `cross-cutting-forces` (C1–C5) | «#14» | 10 |
| §10 | Entry `spatial-computing` (FPGA-domain + smells) | «#15» | 11 |
| §11 | Entry `evaluation-vocabulary` | «#16» | 12 |
| §12 | Entry `resource-budget` | «#17» | 13 |
| §13 | Entry `worked-derivation-robot-dog` (EXAMPLE) | «#18» | 14 |
| §14 | Pattern-boundary audit (D-E) | «#19» | 15 |
| §15 | Supersession execution (D-C + 3 toys) | «#20» | 16 |
| §16 | Cross-link wiring | «#21» | 17 |
| §17 | Validation, index regen, release (v1.7.0) | «#22» | 18 |
