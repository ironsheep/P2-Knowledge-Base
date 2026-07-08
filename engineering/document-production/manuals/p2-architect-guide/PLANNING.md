# P2 Architect's Guide — Planning Charter (rich-planning phase)

**Status:** RE-CUT planning charter · 2026-06-22 (v1) → **2026-07-04 (v2, post-split three-act re-cut)** · slug `p2-architect-guide`
**Phase:** rich planning — specify identity, scope, chapter architecture, voice, source-map, and the
open design decisions. This precedes the formal `creation-guide.md` + `voice-guide.md` (which this spawns).
**Title (D1, LOCKED 2026-07-04):** *The P2 Architect's Guide — Thinking in Cogs, Pins, and Forces*
(name tension of §11 closed — see D1). The subtitle triad now traces the book's spine:
**Cogs** = the parallel compute model · **Pins** = Act I (peripherals → buses → pin budget) ·
**Forces** = Act II (the decomposition forces).

> **⚠️ RE-CUT BANNER (2026-07-04) — read this first.** The v0.1.0 first draft was a **single
> 4-chapter orientation-plus-method book** (Ch1 Meet the P2 · Ch2 Reading P2 Code · Ch3 Putting It
> to Work · Ch4 Thinking in P2). A 2026-06-24 walkthrough review
> (`audit/walkthrough-feedback-2026-06-24.md`) drove a **split**:
> - **Orientation Chs 1–3 forked out** → *Getting Started with the Propeller 2*, **released v1.0.0
>   (2026-06-24)**. That book now owns "picture the chip / read the code / put it to work."
> - **THIS book becomes the design + realization book** — it keeps Ch4 (functional decomposition)
>   and grows a **three-act shape** (§5, superseding the old 4-chapter table): **Act I** design the
>   system (peripherals → buses → pin budget, agent-agnostic) · **Act II** decompose it onto the P2
>   (the ex-Ch4 capstone) · **Act III** realize it with agent support (build→load→run→observe +
>   toolchains). *Getting Started is now a stated prerequisite; this book no longer teaches
>   orientation.* The three-act architecture is the concrete realization of the §16 seed.

> **Origin.** Came out of reading the P1 Propeller Manual's structure during its ingestion (backbone done
> 2026-06-22). The P1 manual got architecture orientation "for free" as Ch1 of one book; P2's richness forced
> a split into many topic manuals (PASM2, Spin2 v55, Smart Pins, Streamer, Debug) — which removed the place
> where the subsystems are introduced *in relation to each other*. That missing-layer role now splits cleanly:
> **Getting Started** re-introduces the subsystems in relation to each other (orientation); **this guide** takes
> the oriented reader forward into *designing, decomposing, and realizing a real system* on the P2.

---

## 1. The thesis (one sentence)
**The P2 is a coarse-grained *spatial* computing fabric, and this guide takes an oriented developer — and an
AI agent — from a system idea to a realized build: design the hardware around it (peripherals → buses → pin
budget), derive a sound object/cog decomposition from physical forces rather than taste, then realize it —
optionally with an agent's help.** (The mental-model *orientation* that precedes all of this now lives in its
own book, *Getting Started with the Propeller 2*; this guide assumes it.)

## 2. What this is — and emphatically is NOT
- **IS:** the **design + realization layer** that sits *above* both *Getting Started* (orientation) and the
  reference manuals. It teaches the reader to take an oriented understanding of the P2 forward into a **real
  system**: choose the peripherals and buses and spend the pin budget (Act I), decompose the behavior onto the
  cog/smart-pin/CORDIC/hub fabric (Act II), and realize the build with the round-trip and toolchains — with or
  without agent assistance (Act III). A *slim* manual (no length cap — content-driven, kept brief by link-out; D5),
  not a comprehensive reference.
- **IS NOT:**
  - **an orientation / "meet the chip" book** — that's now ***Getting Started with the Propeller 2*** (released
    v1.0.0), which this guide treats as a **prerequisite**. This book does **not** re-teach cogs, pins, the six
    Spin2 blocks, or how to read an example.
  - a Spin2 reference — that's the **Spin2 Language Reference (v55)** (excellent; we do not replace or duplicate it).
  - a PASM2 reference — that's the **P2 Assembly Language Manual**.
  - a per-subsystem deep dive — those are the **Smart Pins / Streamer / Debug** guides.
  - a re-spec of the silicon — that's the **P2 (Propeller 2) documentation set** (a spec, not a teaching doc).
  - a learn-PASM tutorial — that's the **DeSilva-style PASM2 tutorial**.
- **Discipline (two boundaries):**
  1. *Downstream (unchanged):* every place a subsystem is touched, the guide **orients then links out** ("smart
     pins do X — the full mode catalogue is in the Smart Pins manual"). Link-out, never duplicate.
  2. *Upstream (new after the split):* the guide **assumes Getting Started** — it opens where orientation ends,
     so it never spends pages re-establishing the mental model. If a passage starts re-teaching "what a cog is,"
     that's a scope defect (it belongs in Getting Started).

## 3. Why this is a unique community contribution ("why us")
The community has the Silicon Doc (dense spec), deep topic manuals, and scattered forum lore. **No one is
producing a curated, trust-chain-verified "how to think in P2."** We can — because we have the cross-source-
verified KB behind it, *and* we have just built the P1→P2 delta catalogue, so this guide can also serve the
large P1-veteran community migrating to P2. The capstone (functional decomposition as a *spatial-computing
discipline*) is a genuinely original framing no existing P2 document offers.

## 4. Target audiences (four, dual-served)
**Shared prerequisite (new after the split):** every audience below has the P2 *orientation* — from *Getting
Started with the Propeller 2*, from prior P2 work, or (partly) from P1 experience. This book opens where that
orientation ends. The pure newcomer is *Getting Started*'s audience, not this book's.
1. **Working P2 dev designing a real system** *(primary)* — can write a cog and read an example; now faces the
   real questions: *which peripherals, which buses, how many pins, and how do I carve this behavior into cogs
   and objects without building an accidental sequential machine on parallel silicon?* Served by Acts I–II.
2. **P1 veteran migrating to P2** — knows cogs/hub round-robin/locks; designing on P2 hardware where the choices
   differ (smart pins change peripheral selection; the egg-beater changes hub timing). Served by woven "P1
   note:" sidebars *where the design decision differs* (§9) — lighter-touch than the orientation book's.
3. **Developer adopting agent-assisted development** — has a working process and wants to know *where and how*
   an AI agent helps across the design → decompose → build → observe loop, and which toolchains it drives.
   Served by Act III (the additive lens).
4. **AI code-generating agent** — served the same *decomposition reasoning* via the KB YAML (dual-rendering,
   §8); the decomposition layer is its golden home (§7).

## 5. The three-act architecture (design → decompose → realize)

> **This section supersedes the old "4-chapter guided ascent."** Those four chapters split: the first three
> (orientation) became *Getting Started*; the fourth (decomposition) is Act II here. The §16 three-act seed is
> now the live architecture, fleshed out below. **Chapter numbering / titles in Acts I & III are PROPOSED —
> Stephen shapes them interactively (§16.3); the Act boundaries and the Act II content are settled.**

> **UPDATE 2026-07-05 — content seeded, structure emerging.** Stephen dictated **12 real P2 projects**
> (`act1-seed-transcription.md`); they were consolidated into a **four-phase Act I spine** (decide → learn the
> hardware → build → ship). From that: **Act I Chapter 1 "Getting a Project Off the Ground" is drafted**
> (first draft, in the opus-master), and **Act III Chapter 3 "The Same Work, with an Agent" is forecast** as a
> skeleton mirroring that spine item-for-item, with 7 `[Stephen to add]` slots. **Emergent structure is
> currently ONE chapter per act** — Ch1 (Act I) / Ch2 = the existing "Thinking in P2" (Act II) / Ch3 (Act III)
> — deliberately left to split later if content grows (Act I candidate splits: identify / bring-up / build-ship;
> Act III mirrors). Both KB worked derivations map to real projects on the list: #5 imaging-tile =
> streaming-pipeline (data-plane), #9 robot-dog = robot-dog (control-plane). The tables below remain the
> reference for the *fuller* multi-chapter option if a split is chosen.

**The altitude gradient survives the split, at a higher entry point.** Orientation used to carry the reader
from "picture the chip" up to "think like an architect." Now *Getting Started* owns the comfort-building base,
and this book begins already at the design desk. The gradient within the book runs **concrete → rigorous →
practical**: Act I is hands-on design work you can picture; Act II is the earned, careful decomposition method;
Act III is practical realization. Acts I–II are **agent-agnostic** (universal engineering + P2 decomposition);
Act III is an **additive lens** that re-reads the whole process with an agent in it.

### ACT I — Designing the System *(agent-agnostic; the front-end)*
The universal engineering process, told for the P2. *What we do on every project* — described as **how we go
about each step**, calling out **the concerns that matter as we work through it**. No agent in the picture yet.
Sources: the P2 architecture YAML (what the chip offers a designer), the smart-pin/peripheral-mode data, the
datasheet's pin/electrical envelope.

| Ch | Title (PROPOSED) | Purpose | Defers to |
|----|------------------|---------|-----------|
| 1 | **From Idea to Block Diagram** | turn a system idea into functional blocks + the peripherals each implies; what the P2 absorbs on-chip (smart pins, streamer) vs what stays external; the concerns at this first step (requirements, on-chip-vs-off-chip, what each block needs). | Getting Started (orientation); architecture YAML |
| 2 | **Choosing Peripherals & Communications** | select the peripheral hardware and the **buses** that reach it (I²C / SPI / UART / parallel / smart-pin-native); the trade-offs & concerns — shared vs dedicated bus, speed, addressing, level/voltage. | Smart Pins manual; datasheet; peripheral datasheets (external) |
| 3 | **Spending the Pin Budget** | **bus consolidation → pin budget → pin map**; the P2 leverage (any-function-any-pin, smart pins absorbing peripheral glue); what to do when you run out of pins. | Smart Pins manual; datasheet pin table |

> *Act I chapter count is PROPOSED as 3; Ch1+Ch2 could compress to one if the material is thin — a Stephen
> call during the interactive Act I whiteboard (§16.3).*

### ACT II — Decomposing onto the P2 *(agent-agnostic; the capstone — the ex-Ch4)*
Now the reader has a hardware design and a pin map; Act II derives the **software architecture** — how the
behavior is cut into cogs and objects. This is the functional-decomposition material already specified in
§5.1–§7: the space-vs-time thesis, the forces, the first-contact procedure, and the worked derivation(s).
**Teaches the METHOD of deriving an architecture — never prescribes one** (the anti-prescription principle,
below). Its golden home stays the decomposition YAML layer (§7); the chapter derives from it and must not drift.

| Ch | Title (working) | Purpose | Defers to |
|----|-----------------|---------|-----------|
| 4 | **Thinking in P2 — Functional Decomposition** | the spatial-computing thesis (space vs time) + the forces (resource ownership/timing, data-flow contracts, rate adaptation, altitude layering + the cross-cutting forces) + the **first-contact procedure** + the **worked derivation(s)** — now *two* available from the KB: the robot-dog **control-plane** demo and the streaming-pipeline **data-plane** demo. | the decomposition YAML layer (golden home, §7) |

> *Act II may split into two chapters ("The Forces" / "Worked Derivations") if length warrants once the KB
> augmentation lands (§6a). PROPOSED as one chapter for now.*

### ACT III — Realizing with Agent Support *(the additive lens — NEW)*
After the whole agent-agnostic process is worked through, the book re-reads it with an agent in the loop:
*how does this process change if we use an agent's support?* An **additive lens on a process the reader already
understands** — never a dependency. Absorbs §15's parked "Using {toolchain}" candidate.

| Ch | Title (PROPOSED) | Purpose | Defers to |
|----|------------------|---------|-----------|
| 5 | **Where Agents Help** | map the agent's leverage back across Acts I–II (design exploration, decomposition sanity-checks, code generation, review); honest about where it helps and where human judgment stays load-bearing. | — |
| 6 | **The Build Round-Trip** | **build → load → run → observe** (DEBUG window / serial); how agent assistance plugs into each step of the loop. | Debug window manual; Getting Started |
| 7 | **The Toolchains** | the three tool sets an agent drives, kept a **slot** (§16.2): FlexProp/flexspin · SPIN Tools IDE · VS Code + spin2 + PNut-TS; loading to a board (the Edge module); seeing `DEBUG`/serial output. | the toolchains' own docs (external) |

> *Act III chapter count is PROPOSED as 3 — a Stephen call; the three questions (§16.1: where / how / which
> tools) may map to 2 or 3 chapters. Much of Act III's Acts-I–II content will be **pulled from the repository**
> where we actually used agents (§16.3) — this is the most repo-mined, least-invented act.*

### Reading literacy — now a PREREQUISITE (moved to Getting Started)
The old Ch2 "Reading P2 Code" definition-of-done — the six Spin2 blocks, method anatomy,
indentation-as-structure, `...` continuation, `:=` vs `=`, objects and `obj.method()`, PASM2 instruction
anatomy, where PASM2 lives — **shipped with *Getting Started* v1.0.0**. This book **assumes it** and does not
re-teach the language. The coverage gate is now an **upstream** one:

**Coverage gate (design book):** no code example in this book may use a Spin2/PASM2 construct that *Getting
Started* did not introduce. After authoring, extract every construct used across this guide and confirm each is
covered by Getting Started's Ch2. If an example genuinely needs a construct beyond it, either simplify the
example or add a **single inline gloss** — never re-teach the language wholesale (that's a scope defect, §2).

### Front & back matter (this book)
Front matter: the **design → decompose → realize** thesis + how to read (audiences/paths, §below) + a
**prerequisite line pointing at *Getting Started*** + the accessible MCU↔FPGA hook (§5.1). Back matter: glossary
(from `decomposition-glossary.yaml`) · a "where to go next" map into the reference manuals · **Appendix A —
Computing in Space and Time: Why We Borrow FPGA Language** (supports Act II) · **Appendix B — Further Reading on
Functional Decomposition** (supports Act II). P1→P2 migration is woven as sidebars, not an appendix — §9.

### 5.1 The space/time (MCU↔FPGA) framing — placement
The P2 straddles the microprocessor and FPGA design spaces; the deep "why" is that **an MCU computes in time,
an FPGA computes in space, and the P2 is a coarse-grained spatial fabric** (already formalized in
`architecture/decomposition/spatial-computing.yaml`). This framing lives in **three** places, by altitude:
- **Front-matter hook (accessible):** "you know microcontrollers; you've heard of FPGAs; the P2 lives in the
  gap between them." Familiar landmarks, concrete — fits comfort-first, no abstraction.
- **Act II (teaching):** the formal space-vs-time thesis as the rationale for the decomposition forces.
- **Appendix A (formalization + reference):** the temporal→spatial spectrum, an honest *what-transfers /
  what-doesn't* (P2 is coarse-grained, still software, no place-and-route — we borrow the *mindset*, not the
  claim of being an FPGA), and the **FPGA-terminology table** (term · FPGA-domain meaning · P2 mapping · where
  the mapping is loose) for the vocabulary already load-bearing in our KB (spatial, fabric, pipeline, dataflow,
  lattice, back-pressure, latency/throughput, systolic, coarse-grained).

### 5.2 Appendix B — Further Reading on Functional Decomposition
Organized along the decomposition layer's **two axes**, because each needs a different body of theory:
- **Logical** (how to cut behavior): Parnas (information hiding); Constantine & Yourdon, *Structured Design*
  (coupling/cohesion); Page-Jones — the canon already cited in `decomposition-method.yaml`.
- **Physical / concurrent** (placing it on communicating processors): Hoare's **CSP** and the **transputer /
  Occam** lineage — *more apt for the P2 than generic structured-design texts*, because the P2 is that model
  reborn (multiple identical deterministic processors, message-passing via hub mailboxes, no shared-state
  preemption); optionally Kung on systolic arrays for the dataflow/pipeline side.
Each entry carries a one-line "why it's relevant to P2." **Every citation (author/title/year) is verified
before publish** — marked NEEDS-VERIFICATION until checked (§12). A short correct list beats an impressive wrong one.

> **Reading paths** (one slim book, four audiences — all assume the *Getting Started* orientation):
> **building a new system** = Act I → II → III front-to-back; **already have a hardware design, need the
> software architecture** = straight to Act II, Act I as reference; **adopting agent assistance on an existing
> process** = Act III first, Acts I–II as the process it lenses; **P1 vet** = follow the "P1 note:" sidebars
> wherever a design decision differs from P1.

> **⚠️ Act II anti-prescription principle (load-bearing, Stephen 2026-06-22).** The final decomposition is
> **unique to every project** — we **cannot and must not prescribe outcomes**. Act II teaches *techniques for
> thinking* (the forces + the first-contact procedure); the reader/agent then *derives* their own. This is the
> decomposition layer's own thesis: understand the forces → derive a sound architecture for a machine you've
> never seen; have only the catalogue → you can only pattern-match. **The worked derivations (robot-dog
> control-plane; streaming-pipeline data-plane) are DEMONSTRATIONS of the method running on one machine each,
> explicitly NOT templates** — framed "your machine will derive a different, equally sound answer." Act II's
> takeaway is the *method*, never any example's object set.

## 6. Source map (trust-chain grounding — nothing invented)
| Act | Primary sources (already in-repo) |
|-----|-----------------------------------|
| **Act I** (design the system) | `deliverables/ai/P2/architecture/` — the designer's view: `p2-architecture-mental-model.yaml`, `cog.yaml`, `hub.yaml`, `smartpins/` + smart-pin mode data (which peripherals the P2 absorbs on-chip), `cordic.yaml`, `streamer/`, `event_system.yaml`, `lookup_ram.yaml`, `fifo.yaml`; the **P2 datasheet** (pin table, electrical envelope); the Smart Pins manual (link-out target). *Peripheral datasheets are external, cited not duplicated.* |
| **Act II** (decompose onto the P2) | `architecture/decomposition/` — **all 15 entries** (see §6a for the current list + what's new since Ch4 was drafted). Golden home (§7). |
| **Act III** (realize with agents) | **repo-mined evidence of where we actually used agents** (§16.3) — our own sprint/build history, plan docs, retrospectives; the toolchain docs (FlexProp / SPIN Tools IDE / VS Code+spin2+PNut-TS — external, cited); the Debug window manual (the observe step). |
| Migration sidebars | `engineering/ingestion/P1-DOCUMENT-LINEAGE.md` (P1↔P2 edges) + `central-analysis/p1-p2-comparison/P1-P2-FEATURE-COMPARISON.md` |

### 6a. KB decomposition-layer delta to incorporate into Act II (capstone fidelity, §7)
Ch4 was drafted (2026-06-23) against the **12-entry** decomposition layer. The layer has since grown to **15
entries** (KB v1.13.0, 2026-06-30) plus in-place enrichments. Act II must be re-audited against current HEAD
and brought into lockstep. The delta:

- **3 NEW entries:**
  - `worked-derivation-streaming-pipeline` — a **data-plane** worked derivation, the counterpart to the
    robot-dog **control-plane** demo (closed `cross-cutting-forces`' breadth-gap). *Candidate second worked
    example in Act II — may justify splitting Act II into two chapters.*
  - `shared-bus-broker` — PATTERN, **many-cogs → one-bus** (completes the shared-resource trio with
    resource-ownership's singleton and `shared-bus-replication`'s N-identical-buses).
  - `shared-bus-replication` — PATTERN, N identical buses (object-image dedup).
- **6 ENRICHED entries (fold the additions into Act II's treatment):**
  - `evaluation-vocabulary` — **4th lens: observability-of-a-cut** (distinct from bring-up isolation).
  - `data-flow-contracts` — **6th contract: fan-out-publication** (+ irreversibility, frame-pool-sizing).
  - `rate-adaptation` — decimation-placement.
  - `resource-budget` — one-forcing-sentence-per-cog.
  - `first-contact-procedure` — post-ship **as-built-audit** step.
  - `spatial-computing` — the bit-bang smell now has a **worked-escape**.

> The shared-bus trio (broker / replication / ownership-singleton) is directly relevant to **Act I's bus
> consolidation** too — the design-side "one bus, many peripherals" decision and the software-side "who owns
> the bus cog" decision are two ends of the same thread. Cross-link Act I ⇄ Act II here.

## 7. The capstone fidelity rule (load-bearing)
Chapter 3 **teaches** the decomposition theory; the **YAML layer remains its golden/canonical home**. The
manual derives from the YAML and must not drift from it. Treat any Ch3 claim the YAML doesn't support as a
finding (route to corrections/gaps), and any improvement discovered while writing as a YAML update first,
then rendered in the manual. Same trust-chain discipline as every other manual (verify against the KB, never
assert independently). This keeps the human and machine renderings conceptually in lockstep.

**And — Ch3 teaches METHOD, not OUTCOMES (§5 anti-prescription principle).** Decomposition is unique per
project; the chapter must never read as "do it this way." It hands the reader the forces + the first-contact
procedure and a single *demonstration* (robot dog), explicitly framed as one machine's answer, not a pattern
to copy. If a draft starts to feel like a recipe, that's a defect.

## 8. Dual-target rendering — RESOLVED (D4)
**Dual-target, separately SHAPED — not a 1:1 mirror.** The human manual (warm narrative) and the AI-facing
YAML target the *same understanding* but are shaped for their consumption modes:
- **Manual:** the warm, guided-ascent narrative for humans.
- **YAML:** **lightweight, granular, on-demand files** the MCP download-on-demand system fetches on a single
  thread, so a consuming agent doesn't congest its conversational context. (The decomposition layer already
  is exactly this shape; the Ch1 mental-model + getting-started YAMLs largely exist too.)
- **Relationship:** siblings from one source understanding, each idiomatic to its medium — NOT mechanically
  synced identical prose. The YAML stays the agent-facing canonical form for the reasoning (golden home, §7);
  the manual is the human face. Authoring keeps them *conceptually* in lockstep without forcing prose parity.

## 9. P1→P2 migration thread — woven sidebars (D3)
We just produced the P1→P2 delta catalogue. Fold it in as **woven "P1 note:" sidebars** through the chapters
(not a back-matter appendix): same (8 cogs, hub round-robin, locks), changed (hub egg-beater, clock setup,
64 pins), new-in-P2 (smart pins, CORDIC, streamer, events/interrupts, LUT, XBYTE). Sidebars let a P1 vet
navigate by "what's different" in-context, while a newcomer can ignore them. Uniquely ours; directly serves
the existing P1 community. Source: `P1-DOCUMENT-LINEAGE.md` edges + `P1-P2-FEATURE-COMPARISON.md`.

## 10. Voice & tone (the "how to voice it" half)

### 10.1 Positioning — where we post on the spectrum
Two reference points bracket us, each "going too far" for our purpose:
- **DeSilva** — high warmth, **high persona**, discursive: a *campfire story* with a strong narrator. Too
  playful / too much character / too digressive for a doc that must also carry real rigor.
- **Spin2 v55 & PASM2 reference** — low warmth, max density, zero persona: a *dictionary*. Nothing welcoming,
  no mental model.

**We post here: high warmth · LOW persona · content-driven density — a mentor's guided tour.** Not a campfire
story, not a dictionary. The warmth comes from *clarity and care* (a senior dev explaining the chip at a
whiteboard), **not** from adopting a character. Density is set by the material (D5: no length cap), kept brief
by the link-out discipline (§2).

### 10.2 The voice MODULATES by altitude (the core move)
- **Chs 1–2 (comfort):** maximally warm, reassuring, encouraging. Assume intelligence, not P2 experience.
  "Here's the intuition; here's why it's nice." The job is to make a newcomer feel *at home* with the P2.
- **Ch3 (capstone):** the warmth **stays** (never cold), but **rigor rises and glibness drops to zero.**
  Functional decomposition is a serious framework — we honor it by being *careful and precise*, carrying the
  rigor through the worked derivation (rigor you can *follow*, not rigor that lectures). The shift the reader
  feels is "you're ready for this now," never "buckle up, it gets hard." **And never prescriptive** (§5/§7) —
  we teach how to think, we don't hand down answers.
- The early chapters **earn the trust** that lets the reader follow into the harder terrain. Never condescend
  early; never turn glib late.

### 10.3 Standing rules
- **Terminology:** "COG" not "CPU" (community treats the COG as the computer); canonical P2 terms; show code
  *constants* not arithmetic values; instruction/bit-field formatting per platform standards. Inherit the
  shared `repo-voice-profile.md` + platform voice; this guide layers the orientation register on top.
- **What we DON'T do:** no exhaustive enumeration (link out), no marketing, no undocumented roadmap claims,
  no unsourced performance numbers, **no prescribed decompositions**.

## 11. Design decisions — RESOLVED (Stephen, 2026-06-22)
- **D1 — Name:** ✅ **LOCKED 2026-07-04** — *The P2 Architect's Guide — Thinking in Cogs, Pins, and Forces.*
  The old "Architect's leans advanced, cuts against the welcoming goal" tension is now **RESOLVED by the split**:
  welcoming is *Getting Started*'s job; this book is unapologetically the architect's/designer's book, so
  "Architect's" is a correct fit, not a gate. The subtitle triad **traces the three acts** — Cogs (the compute
  model) · Pins (Act I front-end) · Forces (Act II decomposition). Roster's alternate subtitle "Designing Real
  Systems on the Propeller 2" retired.
- **D2 — ~~Four chapters~~ → SUPERSEDED by the three-act shape (§5, 2026-07-04).** The 4-chapter plan (Ch1
  picture the chip · Ch2 read the code · Ch3 put it to work · Ch4 think in P2) was correct *for the combined
  orientation+method book*. After the split, Chs 1–3 went to *Getting Started*; Ch4 (decomposition) is **Act
  II** here, bracketed by **Act I** (design the system) and **Act III** (realize with agents). Chapter
  architecture is now §5's three acts; D2's four-chapter list is historical.
- **D3 — P1 migration:** ✅ **woven "P1 note:" sidebars** (not an appendix) — better for migrating P1 vets.
- **D4 — Dual-target, reshaped for YAML:** ✅ lightweight, granular, on-demand YAML + warm human manual; same
  understanding, two shapes; not a 1:1 mirror (§8).
- **D5 — No length cap:** ✅ content sets length; brief but useful; link-out keeps it slim.
- **D6 — Capstone depth:** ✅ distilled core + **the robot-dog worked derivation** (as a *demonstration*, not a
  template — §5 anti-prescription) + link to the YAML for the full treatment.

## 12. Risks & quality gates
- **Scope creep into reference territory** — the link-out contract (§2) is the guard; review every section
  for "am I duplicating Spin2 v55 / the Blue Book?"
- **Drift from the decomposition YAML** (§7) — Ch3 changes start in the YAML.
- **Staying slim** — the length cap (D5) is a feature; resist completeness.
- **Hallucination prevention** — same content-verification protocol as other manuals' creation-guides; every
  claim traces to the KB / Silicon Doc / datasheet.
- **Prescription creep in Ch3** (§5/§7/§10) — the gravest content risk. Decomposition is unique per project;
  if any Ch3 passage reads as "do it this way" or the robot dog reads as a template, that's a defect. Gate:
  every Ch3 section must teach a *technique for deriving*, and the worked example must stay labeled as one
  machine's answer.
- **Too-meta-too-fast** — guard the comfort-first ascent (§5): the spatial thesis and forces stay in Ch3;
  Chs 1–2 must not drift into abstraction.
- **Hallucinated citations (Appendix B)** — a reading list is the easiest place to invent a source. Every
  entry's author/title/year is **verified before publish**; marked NEEDS-VERIFICATION until checked. Trust chain.
- **FPGA overclaim (Appendix A)** — never let the borrowed vocabulary imply the P2 *is* an FPGA; the
  what-transfers/what-doesn't column is the guard (we borrow the mindset, not the claim).

## 13. Production logistics
- **Home:** `engineering/document-production/manuals/p2-architect-guide/` (this charter) → opus-master, audit,
  creation-guide, voice-guide once locked.
- **Roster:** added to PUBLICATION-ROSTER.md **In development** (provisional name) — keeps the every-folder-in-
  roster invariant; move to `## Done` on release.
- **Platform:** ride the shared `p2kb-platform-*` stack + thin local overlay (consistent with the unification
  effort); shared common cover.

## 14. Next steps (updated 2026-07-05)
1. ✅ D1–D6 resolved (§11); title LOCKED (D1); three-act architecture fleshed out (§5); AG-10–13 reconciled (§17).
2. ✅ **Trimmed** the migrated orientation Chs 1–3; **augmented Act II** against the 15-entry layer (§6a); ✅ CHANGELOG v0.2.0 opened.
3. ✅ **Captured 12 projects** + consolidated the **Act I spine**; ✅ **drafted Act I Ch1**; ✅ **forecast Act III Ch3** (skeleton, 7 slots).
4. **← STEPHEN, next:** **enrich Act I Ch1** (confirm the `[?]` facts — motor rpm/"dokko", "Click", ~30-channel; add detail/voice) and **fill the 7 Act III `[Stephen to add]` slots** (the lived AI usage per phase, and any of the 12 projects' AI story not yet inferred).
5. **Re-scope the derivative docs** to the design/realization book (this was deferred pending chapter shape, now unblocked once §4 firms up): `creation-guide.md` (chapter specs → three acts + source map §6 + capstone-fidelity/anti-prescription gates), `voice-guide.md` (altitude gradient re-expressed concrete→rigorous→practical; drop the orientation-comfort register that left with Getting Started), **front-matter.md** (still says "four chapters / short orientation" — false; update to the three acts + Getting-Started prerequisite).
6. **Decide chapter splits** (Act I: one chapter vs identify / bring-up / build-ship; Act III mirror) — *after* the content firms, per Stephen's content-first method.
7. Apply the remaining ARCH walkthrough fixes (AG-05 connascence term / AG-06 "machine" word / AG-07 done / AG-08 Fig 5 — §17) as chapters are refreshed.

## 15. Future / candidate additions (PARKED — not up next, don't forget)

A small pipeline of things we may want, surfaced 2026-06-23 while reconciling against the **Propeller
Manual v1.0** (ISBN 1‑928982‑38‑7). That edition carried *two* from-zero chapters that v1.2 removed
(moved to the Propeller Tool on‑line help): **Ch2 "Using the Propeller Tool"** and **Ch3 "Propeller
Programming Tutorial."** Our guide now has the language (Ch2 "Reading P2 Code"), but not the toolchain
how‑to. Candidates:

- **~~CANDIDATE CHAPTER — "Using {toolchain}"~~ → ABSORBED into Act III (§5, 2026-07-04).** The toolchain
  how-to (build→load→run→observe across FlexProp / SPIN Tools IDE / VS Code+spin2+PNut-TS, `{toolchain}` kept a
  slot, loading to the Edge module, seeing `DEBUG`/serial output) is now **Act III Ch6–7**, no longer a parked
  candidate. Retained here only as the lineage note (it descends from Propeller Manual v1.0's "Using the
  Propeller Tool" chapter).
- **INGEST the v1.0/v1.01 Propeller Programming Tutorial** into the P1 corpus — logged as gap **G‑P1‑007**
  (recoverable: v1.01 PDF archived at nagasm.org / archive.org). Value: a P1‑corpus source AND a pedagogy
  model. NB it teaches **Spin1/PASM1**, so it's a *model* for our P2 Ch2, never a content source.

## 16. Shape refinement — the three-act book (Stephen, 2026-06-24 seed → 2026-07-04 REALIZED in §5)

> **Status: REALIZED.** The 2026-06-24 dictated shape notes below are now the **live architecture** —
> fleshed out into **§5's three acts** (this was the flesh-out session). §16 is retained as the origin record
> and for the detail §5 references (the three tool sets §16.2, the build process §16.3). Where §16 and §5
> differ, **§5 is authoritative**. Remaining open items from the seed — the **Act I and Act III chapter
> breakdowns** — are PROPOSED in §5 and get Stephen's interactive sign-off (§16.3).

### 16.1 The book now has three acts
The guide moves from a 4-chapter shape to a **three-act** shape:

**ACT I — the universal engineering process (agent-AGNOSTIC front matter).**
The front chapters describe *what we do on every project*, with no agent in the picture at all:
- designing the system,
- choosing the peripheral hardware,
- choosing the communications,
- wiring it all up (bus consolidation → pin budget → pin map).
These chapters are **descriptive of HOW we go about each step**, and call out **the issues /
concerns that matter to us as we work through each step**. The register is universal
engineering practice — nothing here depends on having an AI agent. (This is the concrete
shape of the earlier "front-end pillar.")

**ACT II — functional decomposition (the existing capstone).**
We work the system through functional decomposition — the Ch4 / decomposition-layer material
already specified in §5–§7 (the forces, the first-contact procedure, the robot-dog worked
derivation as a *demonstration not a template*). Still agent-agnostic.

**ACT III — *now bring in agent support* (NEW closing set of chapters).**
After the whole agent-agnostic process is worked through, the book **wraps up** by asking:
*how does this entire system — this whole process — change if we choose to use an agent's
support in development?* The closing chapters answer three questions:
- **Which areas can agents support us in?** (where in Acts I–II an agent helps)
- **How does it work?** (the build→load→run→observe round-trip with agent assistance)
- **Which tools can we use?** (the toolchains an agent drives — §16.2)

This placement keeps the front universal and approachable, and makes the AI-assist material an
*additive lens* on a process the reader already understands — not a dependency. It also
absorbs §15's parked "Using {toolchain}" candidate chapter (toolchain how-to now lives in Act III).

### 16.2 The three tool sets Act III must speak to
Stephen: speak to **all three tool sets**. Items he listed, grouped (⚠️ *grouping is my
interpretation — confirm when we flesh the plan*):

1. **FlexProp / flexspin** — the flexspin IDE + the flexspin environment and download (compile + load).
2. **SPIN Tools IDE** — the SPIN Tools IDE (compile + load).
3. **VS Code + spin2 + PNut-TS** — the spin2 VS Code extension + the PNut-TS compiler + PNut-TS download / execution.

The tool set must stay a **slot**, not marry one IDE (consistent with §15's `{toolchain}` slot).

### 16.3 How we'll build it (process, Stephen 2026-06-24)
- This is the **seed**; next we **flesh out the plan in more detail**, then **generate initial content**.
- Then iterate: **add content + pull more information from the repository** — especially where we
  *actually used agents* to bolster the **latter (Act III) chapters** — and **add to the front (Act I)**
  as we discuss the general engineering process **interactively** with Stephen.
- DO NOT gut/build this session — recording only.

---

**Done already (the v1.01 cross‑check, option B, 2026-06-23):** read the v1.01 tutorial's arc (12 exercises
building `Output.spin`/`Blinker2.spin`: Concept → languages → **Objects** → first object → Cogs → Block
Designators → **Objects vs. Cogs** → many‑objects/many‑cogs → clock/timing → library objects → numbers).
It **validated** our Ch2 ordering (objects‑first, the six block designators, methods, then cogs). The one
gap it surfaced — Parallax foregrounds *"there is no direct relationship between objects and cogs"* — is
now closed: Ch2 gained an explicit **object ≠ COG** clarification.

---

## 17. Walkthrough-feedback reconciliation (2026-07-04, post-split)

The 2026-06-24 walkthrough (`audit/walkthrough-feedback-2026-06-24.md`) drove the split. Its
platform/orientation items (AG-01/02/03/04/09) were resolved **in *Getting Started***. The reshape now
**resolves the open scope decisions** that were blocked on "does decomposition belong here" (AG-10):

| ID | Item | Resolution by the three-act re-cut |
|----|------|-----------------------------------|
| **AG-10** ⭐ | *Does functional decomposition belong in this manual?* | **YES — it is Act II, the book's spine.** The reshape keeps it and brackets it (Act I designs the system that Act II decomposes; Act III realizes it). This was the gating question; answering it "stays, as Act II" unblocks AG-11–13. |
| **AG-11** | *Describe iterating the arrived-at decomposition?* | **YES — fold in.** The KB `first-contact-procedure` now carries a post-ship **as-built-audit** step (§6a); Act II teaches measure → find a bad seam → re-cut. Realism the reshape has room for. |
| **AG-12** | *"Do we have reusable objects?" as a decomposition metric?* | **YES — via the KB.** `evaluation-vocabulary` gained a 4th lens and the shared-bus trio (§6a) makes reuse explicit; Act II adds reusability as a quality check of a cut. |
| **AG-13** | *Mapping the application to P2 architectural elements?* | **Handled by the Act I ⇄ Act II bridge.** Act I produces the concrete P2 resource picture (peripherals, buses, pins); Act II's first-contact procedure maps behavior onto cog/smart-pin/CORDIC/streamer/lock. The "method → silicon" bridge is now a structural feature, not a missing step. |

**Remaining ARCH content fixes (apply as the chapters are authored/refreshed — not scope decisions):**

| ID | Item | Disposition |
|----|------|-------------|
| **AG-05** | "connascence" unfamiliar (load-bearing, ~9× in Act II) | **RESOLVED 2026-07-08 → renamed the 2nd judging tool to "change-coupling."** Could NOT swap to plain "coupling" (that's already the 1st tool, the countable one). Fix: 2nd tool is now **"Change-coupling — the sharpest tool"** (framed as sharpening the 1st: count what crosses → ask what must *change together*); **"connascence" kept once** as the formal anchor ("the design literature calls this connascence") + in Appendix B (Page-Jones cite) + glossary title "Change-coupling (connascence)". Everyday-usage jargon reduced from ~9 to 3 formal mentions. Also added a concrete **duplication** paragraph under change-coupling (two copies of an algorithm = worst change-coupling; fix = single owner + accessor hiding composition) and a P2-specific **observability** paragraph (observer cog reads lock-free published state → observe without perturbing; N observers). |
| **AG-06** | "machine" as the name for the embedded application | **RESOLVED 2026-07-07 → "embedded application"** (Stephen: "very different in nature from a general application"). Replace "machine" as the app-noun with **"embedded application"** (shorten to "application" only where the embedded context is already clear). Sweep across all three acts + front-matter in the next draft. Keep "machine" only where it means literal hardware, not the app. |
| **AG-07** | walking-robot — servo attachment unclear | **fix** — 13 servos (3/leg × 4 + 1 head), driven by the multi-channel servo controller. Apply in the Act II worked-example section. |
| **AG-08** | Figure 5 broken | **deferred — LAST**, inspect with the rendered image in front of Stephen (per the walkthrough doc). |
| **AG-14** | WATCH OUT / TIP callouts render as a **square box (tofu)** in the PDF | **fix — template.** The inline emoji ⚠️ (U+26A0 U+FE0F) and 💡 (U+1F4A1) have no glyph in the body font (IBM Plex). Options: swap to a symbol the font carries, or load an emoji/symbol font in the template. ~3 call-sites, all Ch2 body (Watch out ×2, Tip ×1). Validate at visual review. Reported 2026-07-07. |
| **AG-15** | Long single-chapter acts + long chapter headings | **structure.** Adopt the **debug-window-manual** pattern: **Parts = the three Acts**; split each Act's long chapter into several shorter chapters titled *"Chapter N: Main — Subtitle."* Apply during the Act III synthesis draft. Split granularity TBD with Stephen. Reported 2026-07-07. |

**Audience decision (2026-07-07):** target audience is **human, not agent** (Stephen). Flow is **KB → document**
(Act II was generated *from* the decomposition YAML); an agent gets its P2 facts from the **MCP/KB**, not by
reading this narrative PDF. → **Drop the two-audience framing** from front-matter ("How to Use": remove the
"*An AI agent or tool?*" door; make the guide cleanly human-facing). The Act III **closing symmetry** (guide +
agent draw on the *same* KB) stays — it's a human-meaningful point, not a claim that agents read this PDF.

**KB-harvest proposals (from Act I / Act III → the YAML) — SEPARATE follow-up `yaml-knowledge-base-maintenance`
task, Stephen go/no-go; NOT part of the reader draft, NO KB-plumbing language in the prose:**

| Candidate | Source | Rationale |
|-----------|--------|-----------|
| **Project front-end / design-process node set** | Act I (the 4-phase spine) | Real KB gap: the decomposition-reasoning layer begins *at* "which cog owns what." Nothing captures the **pre-decomposition** front-end — feasibility-before-design, narrow-vs-broad comms selection, offload-vs-port partitioning, pin-budget→adapter-board, "characterization becomes the spec," firmware-loaded-device→loader. Reusable P2 design-process patterns an agent scoping a project would reason better with; sits *above* the decomposition layer. |
| **narrow-vs-broad comms selection** pattern | Act I A3 | Peripheral/bus selection guidance (I²C/SPI vs host-style ribbon) for embedded-friendliness. |
| **offload-vs-port / companion-device partitioning** pattern | Act I A4 (#10 gateway) | System-partitioning pattern — what the P2 does vs. a companion device; complements decomposition. |
| **performance → P2-resource mapping** | Act III P-7 | Which performance need maps to which P2 architecture (LUT RAM / PSRAM / CORDIC / streamer). Architectural-selection guidance the KB could carry. |
| ~~Act III agentic principles (P-1…P-24)~~ | Act III | **Do NOT harvest** — about *using agents*, not about the P2; low KB value; stay human-guide only. |
