# The P2 Architect's Guide — Creation Guide

**Canonical Name:** `p2-architect-guide`
**Document Title:** The P2 Architect's Guide — Thinking in Cogs, Pins, and Forces
**Created:** 2026-06-22 · **Re-scoped:** 2026-07-08 (v1.0.0 three-act realization)
**Planning charter:** `PLANNING.md` (the rich-planning phase this guide is derived from — read it for the *why*)

---

## 1. Document Identity

### 1.1 Purpose and Scope
This is a short, **narrative design-and-realization book** — the layer that sits *above* the P2 reference
manuals and teaches how to take a real embedded project from an idea to a shipped build, how to *derive* its
software architecture onto the chip, and how all of that changes with an AI agent at your side. It opens at
the design desk, not at "here is the chip." It is deliberately **slim** — no length cap, but kept brief by a
strict link-out discipline (it orients toward the deep manuals; it never duplicates them) — and it carries
**zero embedded code examples**, by design (the mechanics belong to *Getting Started* and the reference set).

**Getting Started with the Propeller 2 (released v1.0.0) is a stated prerequisite.** The orientation content
that this book used to carry — the old "Meet the P2 / Reading Code / Putting It to Work" chapters — was **split
out** into *Getting Started*. This guide **assumes** that orientation and opens where it ends. It no longer
teaches what a cog, hub, or smart pin *is*; it teaches how to *think in* them.

**This document IS:**
- A design book: how a real, shippable project gets off the ground — deciding what to build, learning the
  hardware, building the capability, finishing and shipping (Part I).
- A teaching of the **functional-decomposition method** — the techniques for *deriving* a sound cog/object
  architecture from physical forces (Part II, the capstone).
- A walk of that **same work with an AI agent** in the loop — what changes in cost and reach at each step
  (Part III).
- The human face of the same decomposition reasoning we also serve as AI-facing KB YAML (dual-target, §5.7).

**This document is NOT:**
- An **orientation manual** — that is now *Getting Started with the Propeller 2* (its prerequisite).
- A Spin2 reference — that is the **Spin2 Reference Manual v55** (we do not replace or duplicate it).
- A PASM2 reference — that is the **P2 Assembly Language Reference**.
- A per-subsystem deep dive — those are the **I/O & Smart Pins User Guide**, **Streamer**, and **Debug** guides.
- A re-spec of the silicon — that is the **Parallax Propeller 2 Documentation v35** (a spec, not a teaching doc).
- A learn-by-building tutorial — that is **DeSilva** (a guided PASM2 build with a strong narrator).
- **A prescriptive design manual.** Decomposition is unique to every project; Part II teaches *how to think*,
  never *what to build* (§3.4 — load-bearing).

### 1.2 Target Audience
The reader has already done *Getting Started* — the P2 orientation is assumed, not built here. Two readers are
served:
1. **The working developer designing a real system.** Can already write a P2 program (launch a cog, drive a
   pin, share through hub, choose Spin2 or PASM2). Wants the front-of-project craft (Part I) and the
   decomposition discipline (Part II) so parallel silicon doesn't get used as a slow sequential machine.
2. **The "how does an agent change this?" reader.** The same developer, or one curious about agentic
   development, asking what an AI agent does to each step of the work (Part III).
3. **The migrating P1 veteran** navigates by the woven **"P1 note"** sidebars wherever a design decision
   differs from the P1.

**Assumed knowledge:** the P2 orientation from *Getting Started* (the subsystems and how to read P2 code) plus
general embedded/microcontroller literacy. The pure newcomer is *Getting Started*'s audience, not this book's —
we do **not** build the "newcomer needs the mental model" ground here; that job left with the split.

### 1.3 Relationship to Other Manuals
| Manual | Relationship |
|--------|-------------|
| **Getting Started with the Propeller 2** | This guide's **companion and prerequisite** — the orientation (the chip, and how to read its code) this guide assumes and opens on top of. |
| **Spin2 Reference Manual v55** | The Spin2 reference. This guide points to Spin2's *role* in a design and links out for syntax. |
| **P2 Assembly Language Reference** | The PASM2 reference and the source for the inter-cog coordination primitives (locks, atomic access, cog attention) Part II's seams are built from. Orient + link. |
| **I/O & Smart Pins User Guide** | The smart-pin deep dive (every mode). Part II's smart-pin triage points here. |
| **P2 Streamer Programming Guide** | The streamer/video deep dive. Orient + link. |
| **P2 Debug Window / Single-Step Debugger** | The bring-up/observation tooling behind Part II's per-layer tests. Referenced where relevant. |
| **DeSilva PASM2 Tutorial** | A guided PASM2 build with a narrator — complementary to this conceptual/architectural book, not overlapping. |
| **Parallax Propeller 2 Documentation v35 (Rev B/C)** | The architectural ground truth behind the hardware of Part I and the decomposition of Part II. |
| **P1 Propeller Manual (v1.2) + P1→P2 deltas** | Source for the "P1 note" sidebars. |

---

## 2. Document Architecture

### 2.1 Overall structure — three Parts (= three acts), Chapters 1–14
The book is a design-and-realization narrative in **three Parts**, each a self-contained *act*, followed by a
send-off and back matter. Modeled on the debug-window-manual structure (Parts contain shorter chapters).

```
FRONT MATTER
├── Title page + "Guide Organization" (the three acts + the reference back matter)
├── Copyright / Trademarks / Acknowledgments / Sources
├── How to Use This Guide (Getting Started is the prerequisite; the reader-entry doors)
└── Conventions ("cog" not CPU; named constants; language coloring; P1-note sidebars; sparing markers)

PART I — GETTING A PROJECT OFF THE GROUND      (the pre-decomposition front of a project)
├── Chapter 1  — Deciding What to Build
├── Chapter 2  — Learning the Hardware        (\FourPhaseSpineDiagram)
├── Chapter 3  — Building the Capability
└── Chapter 4  — Finishing and Shipping       (+ "Where this leaves you" hand-off into Part II)

PART II — THINKING IN P2: FUNCTIONAL DECOMPOSITION     (the capstone method)
├── Chapter 5  — Computing in Space, Not Just in Time  (\SpaceTimeSpectrumDiagram)
├── Chapter 6  — Where Object Shape Comes From         (the two co-designed axes)
├── Chapter 7  — The Forces That Do the Cutting        (the four forces)
├── Chapter 8  — Completing and Judging a Decomposition (cross-cutting objects · budget · the four judging tools)
└── Chapter 9  — The Method in Action    (first-contact procedure + two worked derivations:
                 \RobotDecompositionDiagram · \StreamingPipelineDiagram)

PART III — THE SAME WORK, WITH AN AGENT       (the same work, walked a third time)
├── Chapter 10 — The Mindset: Sufficient Guidance, Not the Perfect Prompt
├── Chapter 11 — Deciding and Learning, with an Agent
├── Chapter 12 — Building and Shipping, with an Agent
├── Chapter 13 — Through the Decomposition, with an Agent
└── Chapter 14 — New Reach: Beyond What You Could Build Alone

IN CLOSING                                     (the send-off; distance covered; catalogue-vs-craft)

BACK MATTER
├── Appendix A — Computing in Space and Time (Why We Borrow FPGA Language)
├── Appendix B — Further Reading on Functional Decomposition
├── Glossary   (weighted toward Part II's decomposition vocabulary)
└── Where to Next — the map into the reference manuals

(woven throughout Parts I–II: bronze "P1 note" sidebars for migrating P1 veterans)
```
Length is content-driven (no cap); link-out keeps each chapter slim.

**Heading convention (platform-governed):** Parts are `# Part N — Title` (→ `\manualpart`); chapters are
`# Chapter N: Title` (colon after the number; an em-dash only *before* an optional subtitle, which the
pagination filter splits into `\chaptersubtitle`). See `p2kb-platform-pagination.lua`.

**Figures — four vector TikZ diagrams** (deferred at draft as `\...Diagram` macros, logged in `PUNCH-LIST.md`):
the **four-phase project spine** (Ch 2), the **space/time spectrum** placing the P2 between MCU and FPGA
(Ch 5), the **walking-robot object-and-cog map** (Ch 9), and the **streaming-pipeline data flow** (Ch 9).

### 2.2 The three-act arc (the pedagogical spine)
- **Act I (Part I) — the front of a project, from twelve real projects.** A four-phase spine — *decide → learn
  → build → finish/ship* — that every project moved through *before* any decomposition. It hands Part II a
  wired-up, understood embedded application: a pin map, parts that talk, a feel for their rates and deadlines.
  Not one cog is assigned in Part I; that is the point.
- **Act II (Part II) — the capstone method.** Derive a cog/object architecture from physical forces. Teaches
  the **method, never the outcome** (§3.4). The four-phase spine of Act I hands off here.
- **Act III (Part III) — the same work with an agent.** Walks the SAME work a third time, mirroring the Act I
  four-phase spine **item-for-item**, asking of each step: *what changes with an agent?* The stance is
  **amplify, don't abandon** (§3.6) — the agent removes none of the judgment.

---

## 3. Pedagogical Framework

### 3.1 The three-act structure earns its capstone
Each act prepares the next. Part I gives the reader a concrete, shippable project and the raw material a
decomposition works on. Part II is the earned summit — the architect's lens, applied to exactly the material
Part I produced. Part III is the additive lens: the same process, now with an agent, showing where cost drops
and reach extends. Standard explanatory moves apply throughout: motivation before mechanism, the question
before the rule, concrete imagery, differentiation by contrast.

### 3.2 The four-phase spine (Act I ↔ Act III alignment — a structural invariant)
Part I's four phases (decide what to build · learn the hardware · build the capability · finish and ship) are
drawn from twelve real projects, consolidated into one spine. Part III walks that **same** spine, item for
item — Ch 11 covers *decide + learn*, Ch 12 covers *build + finish/ship*, Ch 13 revisits the decomposition,
Ch 14 names the new reach. Keeping the two acts aligned is a load-bearing structural rule: the reader should
feel Part III answering Part I step by step.

### 3.3 Rigor without glibness (Act II)
Functional decomposition is a serious intellectual framework with decades of literature behind it. The warmth
stays, but glibness drops to zero: Part II is *careful and precise*, carrying its rigor through two worked
derivations the reader can follow rather than through abstraction that lectures. The felt tone is "you're
ready for this now," never "buckle up, it gets hard."

### 3.4 Teach the METHOD, never the OUTCOME (load-bearing — now for Act II)
**The final decomposition is unique to every project — we cannot and must not prescribe it.** Part II hands the
reader the *forces*, the *first-contact procedure*, and the *judging tools*; the reader then *derives* their
own architecture. This is the decomposition layer's own thesis: understand the forces → derive a sound
architecture for an embedded application you have never seen; have only a catalogue → you can only
pattern-match. Consequences for authoring:
- The **two worked derivations are DEMONSTRATIONS of the method**, each explicitly framed "your application
  will derive a *different, equally sound* answer." Neither is a template to copy.
- Every Part II section must teach a *technique for deriving*, not a recommended object set. **If a passage
  reads as "do it this way," that is a defect** (anti-prescription gate, §4.4 + PLANNING §12).

### 3.5 The two worked derivations (why there are two)
The strongest evidence that this is a *method* and not a catalogue is watching it produce a **different** answer
on different hardware. So Part II runs the whole method twice: a **walking robot** (a *control-plane*
application that shuffles small command words — the derivation that yields cooperative tasks inside one owning
cog) and a **streaming pipeline** (a *data-plane* application — a fast image sensor into a FIFO/decimator chain
feeding two displays, where the binding budget line is hub bandwidth, not cogs). None of the boundaries carry
over between them; only the *procedure* does. "Carry the method, never the map."

### 3.6 The agent stance — amplify, don't abandon (Act III)
Part III is an *additive* lens on a process the reader already understands, not a new process. The governing
image is the **exoskeleton**: the agent amplifies what you already know, letting you reach farther and in less
time — it does not replace your judgment. You still decide what to build, own the pin map, hold the
logic-analyzer probe, and judge the cut against the hardest deadline. The chapter's own gate — **confirm the
agent's understanding before you let it proceed** — is itself part of the method it teaches.

---

## 4. Source Materials

### 4.1 Primary sources (all in-repo; nothing invented)
| Part | Primary sources |
|------|-----------------|
| **Part I** (Act I) | `act1-seed-transcription.md` — faithful capture across **twelve real projects**, consolidated into the four-phase spine. |
| **Part II** (Act II) | `deliverables/ai/P2/architecture/decomposition/` — the KB **decomposition-reasoning layer** (decomposition-method, first-contact-procedure, resource-ownership, data-flow-contracts, rate-adaptation, altitude-layering, cross-cutting-forces, resource-budget, spatial-computing, evaluation-vocabulary, decomposition-glossary, and the worked-derivation entries). Silicon facts: Parallax Propeller 2 Documentation v35 + P2 datasheet. |
| **Part III** (Act III) | `act3-agent-seed-transcription.md` — **26 principles (P-1…P-26)** synthesized from the **same twelve projects**, walked in the same order, capturing where an agent helped (or didn't). |
| **Appendix A** | `architecture/decomposition/spatial-computing.yaml` + the decomposition layer's borrowed vocabulary. |
| **Appendix B** | the citation canon already carried in `decomposition-method.yaml` (the logical + physical/concurrent reading axes). |
| **"P1 note" sidebars** | `engineering/ingestion/P1-DOCUMENT-LINEAGE.md` (P1↔P2 edges) + `central-analysis/p1-p2-comparison/P1-P2-FEATURE-COMPARISON.md`. |

### 4.2 Authority hierarchy
The KB YAML is the canonical home for every fact and for the decomposition reasoning. Where YAML is silent, the
Parallax Propeller 2 Documentation and P2 datasheet are authoritative for silicon facts. The manual **derives**
from these and asserts nothing independently.

### 4.3 The Part II fidelity rule
The decomposition YAML layer is Part II's **golden home**. The book *teaches* the theory; it must not drift
from the YAML. Any improvement discovered while writing Part II is a **YAML update first**, then rendered in the
book. Any Part II claim the YAML doesn't support is a finding (route to the corrections/gaps registers), not
prose.

### 4.4 Content verification protocol (hallucination + prescription prevention)
- **Every factual claim traces to the KB / Parallax Propeller 2 Documentation / datasheet.** No unsourced
  performance numbers, no invented behavior, no undocumented roadmap claims.
- **Anti-prescription gate (Act II):** review every Part II section against *"am I teaching how to think, or am
  I prescribing what to build?"* Each worked derivation must stay labeled as one application's answer.
- **Link-out gate:** review every section against *"am I duplicating Spin2 v55 / the Smart Pins guide / the
  PASM2 reference / Getting Started?"* If yes, cut to an orientation + a link.
- **Prerequisite gate:** any passage that re-teaches orientation (what a cog/hub/smart pin *is*, how to read P2
  code) is a scope defect — it belongs in *Getting Started*, not here.
- **Citation gate (Appendix B):** every reading-list entry's author/title/year is verified against a real
  source before publish — marked NEEDS-VERIFICATION until checked. Never ship an unverified or invented citation.
- **FPGA-overclaim gate (Appendix A):** the borrowed vocabulary must never imply the P2 *is* an FPGA; the
  what-transfers/what-doesn't treatment is mandatory wherever the spatial framing appears.

---

## 5. Content Specifications

### 5.1 Part I — Getting a Project Off the Ground (Ch 1–4)
The front of a shippable project, drawn from twelve real projects, along the four-phase spine. Reader frame: "a
real project you're building to ship" (product, contract, or formal project — usually a blend).
- **Ch 1 — Deciding What to Build.** Where a project comes from; feasibility before design (*what's practical
  vs. possible*); choosing peripherals and how you talk to them (narrow I²C/SPI vs. broad; self-contained
  modules); the partition decision (what the P2 should *not* do — pair it with a companion device); scoping
  features honestly.
- **Ch 2 — Learning the Hardware.** The unadvertised grind: datasheets that fight you (hard to find,
  foreign-language, or absent → reverse-engineer); voltage/level-shifting at speed; the **pin budget** (the
  "Pins" of the subtitle) and adapter-board design; mechanical fabrication; firmware-loaded devices; the logic
  analyzer as the constant instrument. Closes on the `\FourPhaseSpineDiagram`.
- **Ch 3 — Building the Capability.** Making the part *usable*: interface design as deciding how someone will
  *think* about the thing; convenience layers; translation/digestion of reference code; performance chasing;
  characterizing the hardware (measurements become the product's spec); and the honest note that a project can
  meet *your own* limits, not the chip's.
- **Ch 4 — Finishing and Shipping.** The closing ritual (document, publish, announce); reusable/configurable
  extraction; the long tail of vendor updates; "shipped while honestly incomplete." Ends with **"Where this
  leaves you"** — the explicit hand-off of a wired-up, understood application into Part II, naming the questions
  (shared bus, fast-producer/slow-consumer, tiny sensors) that are *decomposition* questions.

### 5.2 Part II — Thinking in P2: Functional Decomposition (Ch 5–9)
The capstone. Derive a cog/object architecture by reconciling physical forces. Opens by stating the
method-not-outcome thesis for the whole part.
- **Ch 5 — Computing in Space, Not Just in Time.** The spatial-vs-temporal framing; the P2 as a
  **coarse-grained spatial fabric** between MCU and FPGA; decomposed well it behaves spatially, decomposed badly
  it collapses to a slow sequential machine. `\SpaceTimeSpectrumDiagram`. Points to Appendix A for the honest
  FPGA accounting.
- **Ch 6 — Where Object Shape Comes From.** Object shape is *derived*, not chosen from a menu. The **two
  co-designed axes**: the classical *logical* axis (cohesion/coupling) and the P2's *physical* axis (allocation
  onto the finite resource lattice — a decomposition tool in its own right). The failure this prevents: the
  **flat device list**.
- **Ch 7 — The Forces That Do the Cutting.** The **four forces**, each led by the *question it asks*:
  **Force 1 — resource ownership** ("who owns this wire?", the correctness force — one owner per serialized
  resource, boundary traces the wire); **Force 2 — data-flow contracts** ("what does each seam promise?", plus
  the data/control/event three-plane model and publish-last); **Force 3 — rate adaptation** ("where do two
  cadences meet?", samplers/buffers and slew/easing engines, cooperative tasks for a shared bus with multiple
  cadences); **Force 4 — altitude layering** ("how high does each piece sit?", the emergent vertical force —
  split where the unit or axis of change changes; Parnas information hiding). Closes on **reconciling** the
  forces.
- **Ch 8 — Completing and Judging a Decomposition.** The **five cross-cutting objects (C1–C5)** — safety
  override, external-interface translator, configuration store, testability seams, lifecycle sequencer; the
  **resource budget** ("running out of cogs" = too-coupled; every cog earns a one-sentence reason); and the
  **four judging tools in increasing sharpness — coupling · change-coupling · back-pressure · observability**.
  Ends on "a decomposition is revisable — expect to dial it in" (the as-built audit foreshadowed).
- **Ch 9 — The Method in Action.** The nine-step **first-contact procedure** (starts at the hardware edge and
  timing budget, inverts top-down; spine steps always run, others state when to skip; the procedure is
  *fractal*); then the two worked derivations (§3.5) — the walking robot (`\RobotDecompositionDiagram`) and the
  streaming pipeline (`\StreamingPipelineDiagram`). Closes on "carry the method, never the map."

### 5.3 Part III — The Same Work, with an Agent (Ch 10–14)
The same work walked a third time, mirroring the Act I spine, synthesized from the 26 principles. Stance:
additive lens, amplify-don't-abandon (§3.6).
- **Ch 10 — The Mindset: Sufficient Guidance, Not the Perfect Prompt.** Reject the "magic prompt" framing; the
  three dimensions of guidance (**requirements · process · foundational language understanding**) and their
  three homes (theory-of-operations docs · skills · the **P2 Knowledge Base** — "the third arm"); the human
  supplies **intent**. The **understanding gate** (have the agent tell you back before it proceeds) and the
  **exoskeleton** image; "no single 'the agent'."
- **Ch 11 — Deciding and Learning, with an Agent.** Part I's first two phases with an agent: research collapse
  (part selection, feasibility); learning the hardware (datasheet reading/translation, the
  **theory-of-operations** move); instruments as partners (annotating code with the LA map); and the boundary —
  **you are its senses and hands**, you supply the physical constraints and the **frames of reference**.
- **Ch 12 — Building and Shipping, with an Agent.** Part I's build/finish phases: in-head translation at speed;
  reshaping for a hardware change; the division of labor on performance; standalone objects with agent-written
  regression tests; the **closed autonomous loop** (a hosted agent that compiles/runs/reads on real silicon and
  converges); the **ceiling that used to be yours** lifting (inverse kinematics); documentation and the vendor
  long tail becoming surgical.
- **Ch 13 — Through the Decomposition, with an Agent.** The middle of the book with an agent: it can help
  *postulate* a decomposition and build the layers, sanity-check a cut against the four forces, catch a
  cross-plane smuggle — but it does **not** own the reconciliation. The final call stays yours.
- **Ch 14 — New Reach: Beyond What You Could Build Alone.** The change worth ending on is **reach**, not speed:
  math ceilings, platform ceilings (standing up a Linux/RPi side), a whole new artifact (a BLE mobile control
  panel); amplification for the expert, passage for the newcomer; amplification compounds via composition.

### 5.4 In Closing
The send-off: the distance covered across the three acts; what the reader carries out is a *method*, not a set
of answers (catalogue vs. craft); the closing symmetry — the knowledge an agent draws on to help you think in
P2 is the same curated body this guide was written from, and "the community is writing the other" end of it.

### 5.5 "P1 note" sidebars
Short, optional bronze callouts (fenced `::: p1note`) for migrating P1 veterans: *same as P1*, *changed in P2*,
or *new in P2*. A newcomer can skip every one; a P1 vet navigates by them. Sourced from the P1→P2 delta
catalogue.

### 5.6 Appendix A — Computing in Space and Time (Why We Borrow FPGA Language)
Formalizes the space/time positioning and justifies the borrowed vocabulary. Three parts:
1. **The temporal→spatial spectrum** — pure-temporal MCU → P2 (coarse-grained spatial fabric: 8 cogs + 64 smart
   pins as sustained concurrent concerns) → pure-spatial FPGA. The P2 *straddles* the MCU and FPGA design spaces.
2. **What transfers / what doesn't** — the P2 is coarse-grained not fine-grained, still software not synthesized
   logic, no place-and-route. **Never imply the P2 *is* an FPGA** (§4.4 gate).
3. **Terminology, mapped** — two tables of `term · FPGA-world meaning · P2 mapping · where the mapping is loose`
   for the load-bearing vocabulary (spatial, fabric, coarse-grained, pipeline, dataflow, systolic array;
   resource lattice, back-pressure, latency/throughput, latency-insensitive, GALS, place-and-route). The
   place-and-route row is the one to remember — the sharpest "does not transfer."

### 5.7 Appendix B — Further Reading on Functional Decomposition
A short, curated list along the decomposition layer's **two axes**, each entry with a one-line "why it matters
here":
- **Logical axis** (cutting behavior): Parnas (information hiding); Constantine & Yourdon, *Structured Design*
  (coupling/cohesion); Page-Jones (connascence = this guide's **change-coupling**).
- **Physical/concurrent axis** (placing it on communicating processors): Hoare's CSP; INMOS/occam (the
  Transputer lineage the P2 revives); Kahn process networks; Kung & Leiserson (systolic arrays); Lee &
  Messerschmitt (synchronous data flow); Carloni et al. (latency-insensitive design); Chapiro (GALS).
- **Boundaries, real-time, generative stance:** Evans (bounded contexts); Liu & Layland (rate-monotonic);
  Alexander (a pattern *language* — the generative stance Part II takes).

**Every citation (author/title/year) verified before publish** — NEEDS-VERIFICATION until checked (§4.4). A
short correct list beats an impressive wrong one.

### 5.8 Dual-target relationship (manual ⇄ YAML)
The book and the AI-facing decomposition YAML target the *same understanding*, shaped per medium — **not** a
1:1 mirror. The YAML stays **lightweight, granular, on-demand** (an agent fetches it a thread at a time so its
context doesn't congest); the book is the warm human narrative. Authoring keeps them *conceptually* in lockstep
without forcing prose parity. The YAML remains the agent-facing canonical form (§4.3).

---

## 6. Writing Guidelines
Voice is specified in full in `voice-guide.md`. In brief: **a mentor's guided tour — high warmth, low persona,
content-driven density**, warm *throughout* — Act I welcoming and concrete, Act II carrying rigor without
glibness (the decomposition method), Act III the amplification/agent voice. Terminology: **"cog," not "CPU" or
"core"** (lowercase in prose); canonical P2 terms; **named constants, not arithmetic values**. What we don't
do: exhaustive enumeration, marketing, hedging, undocumented roadmap claims, unsourced numbers, **prescribed
decompositions**. Inherit `repo-voice-profile.md` + the shared platform voice.

---

## 7. Code Line Budget

- **Max code columns (K): 76**

**Provenance:** inherited from the shared platform. Even though the book now carries **zero embedded code
examples**, it is born on the unified `p2kb-platform-*` stack and would render any code through the platform
code box (`p2kb-platform-content.sty` Spin2/PASM2 blocks via `p2kb-platform-code-coloring.lua`) with the same
page geometry and `Verbatim` inset as every other platform manual — so it inherits the platform's
Latin-Modern-Mono-calibrated K=76 (the same budget the Assembly, Smart Pins, Streamer, DeSilva, Debug, and
Single-Step manuals use). The budget stays documented so that any future code snippet is governed by it;
`audit-code-line-length.py` enforces K=76 at prepare-manual time (legal Spin2 `...` continuation or a named
CON to shorten; never typeset-wrapped).

---
*Version 1.1 — re-scoped 2026-07-08 to the shipped v1.0.0 three-act design-and-realization book (Parts I–III,
Ch 1–14, In Closing, back matter). Supersedes the v0.1 orientation-manual creation guide. Derived from
PLANNING.md (v2 three-act re-cut) and the shipped opus-master.*
