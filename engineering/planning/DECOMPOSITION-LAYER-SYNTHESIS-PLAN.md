---
title: Authoring Plan — P2 Functional-Decomposition Reasoning Layer
kind: authoring plan (synthesis of two architecture-discussion inputs into P2KB YAML)
status: APPROVED (2026-06-11) — D-A / D-B / D-C / D-D signed off; proceeding to sprint-plan → tasks → execution
created: 2026-06-11
active_element: yaml:p2kb
inputs:
  - architecture-discussion-000/  (robot-dog perspective — forces, §5 first-contact procedure, §8 synthesizer brief)
  - architecture-discussion-001/  (authority-tier charter + three-plane/canon lenses; corpus-eval schema = OUT OF SCOPE this pass)
scope_cut: >
  THIS pass authors the decomposition-GUIDANCE YAML only. No object/corpus study,
  no OBEX, no seed grading. The 001 corpus-evaluation schema is a SEPARATE later
  ratification pass.
---

# Authoring Plan — P2 Functional-Decomposition Reasoning Layer

## 1. Goal (one sentence)

Author a new P2KB YAML area that teaches a consuming agent **how to derive a sound
object/cog decomposition for an unfamiliar P2 hardware mix** — what P2 assets and
architectural features drive the cuts, and how to make each decision — rather than
pattern-matching a catalog of shapes.

## 2. Scope of this pass

- **In:** the generative decomposition guidance (the mechanism), authored as YAML
  under a new area, grounded per §4 below.
- **Out:** object/corpus evaluation (the 001 schema), OBEX study, seed grading —
  that is a separate ratification pass that stress-tests this layer once it exists.
- **EXAMPLEs** in this pass are transcribed from the worked examples **already
  written into 000** (robot-dog `file:line` illustrations), carried in as cited,
  *illustrative-not-normative* material. We generate no new examples and evaluate
  no objects here.

## 3. Synthesis approach (how 000 and 001 combine)

Agreed framing: **001 governs the discipline and shape; 000 provides the
project-ratified substance.** Operationally:

- **001 sets the quality bar and the carving guide** — the authority-tier tagging
  (§5 below), the generative-not-catalog rule, the "every topic supplies
  vocabulary / forces / axes / invitations" test, and the pattern skeleton
  (Context / Forces / Resolution / Varies-by / Smells / Neighbours). 001 also
  contributes analytical **lenses 000 lacks**: the three planes (data / control /
  event), the FPGA-domain / spatial-computing thesis, the connascence evaluation
  vocabulary, and the reference canon.
- **000 is the spine of the content** — forces 1–4, cross-cutting C1–C5, the §5
  first-contact procedure, the worked examples, and §8's synthesizer rules
  (dedupe-on-concept, keep-the-why-and-failure-mode, one unified procedure,
  preserve provenance, respect existing entries).
- **Where they overlap, dedupe on concept** (000 §8 rule 1), using 000's canonical
  names as the reconciliation key. Where 001 adds a lens, fold it in. Where 000
  has substance 001 only gestures at, that substance leads.

## 4. Grounding policy (two-tier) + reference self-sufficiency

Every claim is grounded according to **what kind of claim it is** — and every
reference the *shipped* YAML carries must be **self-sufficient** (resolvable
without any file outside the published KB; see §4.1).

- **Architectural fact** (a P2 asset/feature: cogs, OR'd pins, CORDIC latency, the
  streamer, LUT-pair sharing, smart-pin modes, hub egg-beater) → **cite a P2KB
  key.** Resolves within the published KB; must be true about the silicon.
- **Decision guidance** (how to reason about a cut: the forces, the procedure,
  connascence, the planes) → cite the **durable reference canon** by full
  bibliographic identity (author, title, year) — Parnas, Page-Jones, CSP/occam,
  Kahn, synchronous dataflow, GALS, Alexander, DDD. These are location-independent
  published works. "How to decide" is not a P2 fact and cannot be grounded as one.
- **Example** → **inlined, self-contained**, tagged `EXAMPLE` /
  illustrative-not-normative. The content stands on its own; it is **not** cited to
  an external working doc.

### 4.1 Reference self-sufficiency (REQUIRED)

The shipped YAML must read completely on its own. It is MCP-served and consumed
standalone; we cannot guarantee where any guiding document sits relative to it.

- **Do NOT reference the guiding/working documents** (architecture-discussion-000,
  -001, the robot-dog handoff bundle, this plan) or any relative file path to them,
  anywhere in the shipped YAML. Their substance is **fully absorbed/inlined** so a
  reader never needs the source.
- **Allowed references are self-sufficient only:** (a) internal P2KB keys /
  `related:` paths that resolve within `deliverables/ai/P2/`; (b) durable external
  bibliographic citations (author / title / year) for the reference canon.
- **Source-doc provenance** (which guiding doc a force or example came from) is kept
  for *our* authoring traceability in **this plan / commit messages / git history**,
  NOT in the shipped YAML. This satisfies 000 §8 rule 4's "preserve provenance"
  without binding the YAML to a file layout.

## 5. The authority-tier mechanism (new YAML field)

A new structured field tags each statement with its tier, **at statement
granularity** (a single entry mixes tiers — e.g. "pins are OR'd" is PHYSICS;
"therefore one owning cog per bus" is PRINCIPLE). The tier also *selects the
grounding* (§4), so the two mechanisms are one:

| Tier | Meaning | Agent freedom | Grounding (per §4) |
|------|---------|---------------|--------------------|
| `PHYSICS` | silicon truth, inviolable | none — design within it | P2KB key |
| `PRINCIPLE` | a force/trade-off + why | applies with judgment | canon / source citation |
| `HEURISTIC` | default **with explicit escape condition** | overrides for a stated reason | canon / source citation |
| `PATTERN` | one resolution of named forces (generative skeleton) | consults as illustration | source citation |
| `EXAMPLE` | concrete code, frozen at one point | reads, never copies as law | cite 000, illustrative |

Rule (from 001 §3): a `HEURISTIC` without a stated escape condition is a disguised
law and is a **defect** — name when to break it. A `PATTERN`/`EXAMPLE` must be
unmistakably marked so it can never be read as a `PRINCIPLE`.

> **Open schema decision (D-A):** exact representation of the tier in YAML — a
> per-section `authority_tier:` field vs. a per-claim inline tag. Resolve before
> authoring entry #1 (proposal: per-section field, with inline tags where a
> section genuinely mixes tiers).

## 6. Proposed carving (the entire mechanism)

New area: **`deliverables/ai/P2/architecture/decomposition/`**. Proposed entries
(granularity is itself reviewable — see D-B):

| # | Entry | What it carries | Dominant tier(s) | Source map |
|---|-------|-----------------|------------------|------------|
| 1 | `decomposition-method` | the generative theory: forces = grammar, archetypes = vocabulary; **two-axis** decomposition (logical + physical resource-lattice); shape is *derived*, not chosen | PRINCIPLE | 000 §2–§3; 001 §4.1 |
| 2 | `first-contact-procedure` | the ordered observation→force routine an agent runs on unseen hardware (the spine) | PRINCIPLE / HEURISTIC | 000 §5–§6; 001 §4.5 |
| 3 | `resource-ownership` | Force 1: singular ownership as a **correctness rule** (OR'd pins / no bus mutex); singleton-vs-instance from sharing topology | PHYSICS→PRINCIPLE | 000 Force 1; P2KB pin facts |
| 4 | `data-flow-contracts` | Force 2 **×** 001 three planes (data/control/event): latest-wins+ack, lock-free single-writer telemetry, freshness counters; **when to choose which**. Replaces the blocking `MailboxCommunication` toy | PRINCIPLE / HEURISTIC + EXAMPLE | 000 Force 2; 001 §4.3 |
| 5 | `rate-adaptation` | Force 3 (rate-domain crossing + slew/easing) as the "clock-domain crossing" missing half of smart-pins-first; **cooperative tasks-within-a-cog** (§4 tension) | PRINCIPLE / HEURISTIC | 000 Force 3 + §4; 001 §4.3 + canon (SDF/GALS/Kahn) |
| 6 | `altitude-layering` | Force 4: split by **unit conversion / axis of change**, not line or component count | PRINCIPLE / HEURISTIC | 000 Force 4; canon (Parnas) |
| 7 | `cross-cutting-forces` | C1–C5: safety override, external-vocabulary translation, per-unit config, testability seam, lifecycle/init order | PRINCIPLE | 000 cross-cutting |
| 8 | `spatial-computing` | FPGA-domain thesis: assign function to space; pipelines; push to the edge; latency-insensitive interconnect — **+ the smell catalog** (funnel, hub saturation, timing-coupled cogs, poll/signal inversion, over-locking) | PRINCIPLE + HEURISTIC | 001 §4.4; 000 failure modes |
| 9 | `evaluation-vocabulary` | judge a cut: coupling-as-integer, **connascence** (static/dynamic + P2 manifestations), back-pressure-as-min-cut | PRINCIPLE | 001 §4.2 |
| 10 | `resource-budget` | the allocation table as a **required design artifact**; "out of cogs" = "too coupled, re-cut" | HEURISTIC / PRINCIPLE | 001 §4.6; 000 §6 |
| 11 | `worked-derivation-robot-dog` | one end-to-end derivation, every step tagged with its force/plane decision, **EXAMPLE throughout** | EXAMPLE | 000 §7 + cited code |
| 12 | `decomposition-glossary` | canonical-name map + authority-tier legend + **reference-canon index** (each name paired with the P2 mechanism it governs) | reference | 000 §8; 001 §4.7 |

Each **force** entry (3–7) carries the 000 §8 required fields — `what_it_is`,
`why_on_p2` (the silicon mechanism), `how_it_cuts`, `example` (inlined,
self-contained), and `failure_if_ignored` — **plus** the §5 tier tags and, where it
states a pattern, the generative skeleton.

The **Source map** column above is an **authoring-time** artifact (it lives in this
plan only); per §4.1 it does **not** ship into the YAML.

YAML shape follows existing p2kb concept style (`p2kbSpin2ObjectArchetypes`,
`p2kbArchP2ArchitectureMentalModel`): `concept`/`title`/`category` head, plain
`summary`, named body sections, a `related:`/`see_also:` block, a one-line
`oneliner` — extended with the `authority_tier` field (D-A) and explicit grounding
citations.

## 7. Patterns-analysis disposition (study result)

I read all 8 `architecture/patterns-analysis/*.yaml`. **Finding:** they are
machine-generated *descriptive* shape-mining (a rigid `usage_frequency` /
`structural_signature` / generic `implementation_template` / `statistics` /
`anti_patterns` template) — exactly the "common ≠ correct" catalog 001 §0 warns
against. Several are **factually defective** or **generic-CS, not P2-grounded**:

- **P1-isms** (wrong for P2): `cog_management` uses `cognew(...)` (P1 API; P2 is
  `coginit`/`cogspin`) and the blocking `long[mailbox_ptr]` poll 000 explicitly
  criticizes. `timing_control` and `state_machine` use `CNT` / `waitcnt` (P1; P2
  Spin2 uses `getct()` / `waitct()`).
- **Generic / mis-projected**: `memory_management` teaches malloc / free / buddy
  systems / garbage collection / fragmentation — **P2 has no heap**; this is
  PC-style content projected onto the P2, and it is misleading. `buffer_management`,
  `protocol_implementation`, `timing_control` cite cache lines, DMA, interrupt-
  disable critical sections — generic embedded-CS, not P2 reality.

| File | Decomposition value | Recommended disposition |
|------|--------------------|--------------------------|
| `cog_management_analysis` | superseded by #3/#4/#7; has a P1-ism + blocking toy | **REPLACE** |
| `timing_control_analysis` | cadence/rate relevance → absorbed by #5; P1-isms | **REPLACE** (salvage P2-true cadence framing into #5) |
| `buffer_management_analysis` | producer/consumer + double-buffer relevance → #4/#5; generic otherwise | **REPLACE** (salvage the streaming double-buffer note → #4/#5; note 000's flagged breadth gap) |
| `protocol_implementation_analysis` | dedicated-cog/smart-pin-assist relevance → #5/#8; rest generic; overlaps real protocol YAMLs | **REPLACE / relocate** |
| `state_machine_analysis` | thin decomposition value; also an archetype; P1-ism (`CNT`) | **REPLACE / integrate-thin** |
| `smart_pin_usage_analysis` | smart-pin-first is core (#5/#8) but factual modes live in `architecture/smart-pins/` | **REPLACE** (decomposition relevance absorbed; facts already elsewhere) |
| `memory_management_analysis` | misleading (heap/malloc/GC not P2); near-zero decomposition value | **REMOVE** |
| `asm_integration_analysis` | tangential to decomposition (inline-PASM topic) | **LEAVE — out of scope**; route its P1/correctness smells to the corrections register |

**Net:** the set is largely superseded and partly defective; little needs
integrating that 000/001 don't do better and grounded. **But** these are
MCP-served entries, so removal/redirect is a supersession action handled
case-by-case **after** the new material exists (Decision 3 / §8 step 5), honoring
Sacred Rule #7 (redirect, never silently delete cross-refs). The P1-isms surfaced
here are logged as corrections-register candidates regardless of disposition.

> **Open decision (D-C):** ratify the disposition column above (REPLACE×6 /
> REMOVE×1 / LEAVE×1), to be *executed* in the post-authoring supersession review.

## 8. Execution sequence (after sign-off)

1. **Resolve D-A / D-B / D-C** (below), set the YAML schema for the new area.
2. **Author entries 1–12** under `architecture/decomposition/`, 001-discipline +
   000-substance, every claim tier-tagged and grounded per §4. Present-plan-then-
   edit per project rule; author in dependency order (glossary + method + procedure
   first, then forces, then spatial/eval/budget, then the worked derivation).
3. **Cross-reference + ground-check**: every PHYSICS claim cites a verified P2KB
   key (probe via p2kb-mcp / local YAML); every guidance claim cites canon/000/001;
   every example tagged illustrative. Run `validate-crossref-keys.py`.
4. **Index regen** (`generate-p2kb-index.py`, post-commit Path B) + validate.
5. **Supersession review** (Decision 3): walk each patterns-analysis file and the
   `MailboxCommunication` / `FewObjects` / `SeveralObjects` entries case-by-case
   with you; apply REPLACE/REMOVE/redirect per ratified D-C; add `superseded_by:`
   pointers so old keys still resolve.
6. **Release** via `release-yamls`; refresh local cache; verify by content probe.

## 9. Decisions — RESOLVED (2026-06-11)

All four signed off; recommendations accepted as written:
- **D-A** ✅ per-section `authority_tier:` field + inline tags where a section mixes tiers.
- **D-B** ✅ keep the 12-entry carving for completeness.
- **D-C** ✅ patterns-analysis disposition (REPLACE×6 / REMOVE×1 / LEAVE×1), executed in §8 step 5.
- **D-D** ✅ new area `architecture/decomposition/`.
- **D-E** ✅ (surfaced by code research) relationship to the **existing
  `language/spin2/patterns/` library** (separate from the 8 `patterns-analysis`
  files): **crosslink, not absorb.** The decomposition layer is the higher-altitude
  generative grammar; the pattern library is concrete vocabulary it links into via
  `related:`/`see_also:`. Supersession stays scoped to the three agreed toys
  (mailbox-blocking `spin2_mailbox_communication`, count-taxonomy `few_objects` /
  `several_objects`). **New deliverable:** a **pattern-boundary audit** — both
  directions: (a) forces that imply a pattern the library lacks → new-pattern
  candidate; (b) existing patterns to factor into / cross-link from the guidance.
  Audit yields a candidate list + recommendation; acting on large candidates is a
  separate scope call.
- **PLAN_DIR** ✅ single canonical engineering plan dir `engineering/planning/`
  (decided 2026-06-11 — unify all heads; skill-conventions.md updated). This
  initiative's executable plan: `engineering/planning/DECOMPOSITION-REASONING-LAYER-SPRINT-PLAN.md`.

Original framing retained for the record:

- **D-A — tier representation in YAML** (§5): per-section `authority_tier:` field
  vs. per-claim inline tag. *Proposal: per-section field + inline where mixed.*
- **D-B — carving granularity** (§6): the 12-entry set as proposed, or consolidate
  (e.g. merge `evaluation-vocabulary` into `decomposition-method`; fold
  `resource-budget` into `first-contact-procedure`). *Proposal: keep 12 for
  completeness; revisit if any entry is too thin to stand alone.*
- **D-C — patterns-analysis disposition** (§7): ratify REPLACE×6 / REMOVE×1 /
  LEAVE×1; executed in step 5, not now.
- **D-D — new-area landing** confirmed as `architecture/decomposition/` (vs.
  extending `patterns-analysis/`). *Proposal: new area, since the charter forbids
  replicating the descriptive catalog.* (Already agreed in principle.)

## 10. Quality gates (carried from project rules)

- No unsourced claims; PHYSICS → P2KB key, guidance → durable canon citation.
- **Reference self-sufficiency (§4.1):** shipped YAML references only internal P2KB
  keys + durable bibliographic citations — never a guiding/working doc or relative
  path. Each entry reads completely on its own.
- Examples always tagged illustrative-not-normative (never a template to clone).
- Every HEURISTIC states its escape condition (else it's a defect).
- Generative test per major topic: supplies vocabulary, forces, axes, invitations.
- Acceptance (001 §6): a consuming agent can derive a sound decomposition this
  layer never explicitly covered, and justify it in the layer's own vocabulary.
