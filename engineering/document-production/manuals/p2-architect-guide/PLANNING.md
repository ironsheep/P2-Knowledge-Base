# P2 Architect's Guide — Planning Charter (rich-planning phase)

**Status:** DRAFT planning charter · 2026-06-22 · **provisional slug** `p2-architect-guide`
**Phase:** rich planning — specify identity, scope, chapter architecture, voice, source-map, and the
open design decisions. This precedes the formal `creation-guide.md` + `voice-guide.md` (which this spawns).
**Title (D1, approved):** *The P2 Architect's Guide — Thinking in Cogs, Pins, and Forces* (name tension noted §11)

> **Origin.** Came out of reading the P1 Propeller Manual's structure during its ingestion (backbone done
> 2026-06-22). The P1 manual got architecture orientation "for free" as Ch1 of one book; P2's richness forced
> a split into many topic manuals (PASM2, Spin2 v55, Smart Pins, Streamer, Debug) — which removed the place
> where the subsystems are introduced *in relation to each other*. This manual is that missing layer.

---

## 1. The thesis (one sentence)
**The P2 is a coarse-grained *spatial* computing fabric, and this guide teaches a developer — and an AI agent —
how to *think* in it: hold the architecture as a mental model, turn it into a running program, and derive a
sound object/cog decomposition from physical forces rather than taste.**

## 2. What this is — and emphatically is NOT
- **IS:** the **orientation + design-reasoning layer** that sits *above* the reference manuals and ties the
  subsystems together. A *slim* manual (no length cap — content-driven, kept brief by link-out; D5), not a comprehensive reference.
- **IS NOT:**
  - a Spin2 reference — that's the **Spin2 Language Reference v55** (excellent; we do not replace or duplicate it).
  - a PASM2 reference — that's the **P2 Assembly Language Manual**.
  - a per-subsystem deep dive — those are the **Smart Pins / Streamer / Debug** guides.
  - a re-spec of the silicon — that's **Chip Gracey's Silicon Doc** (a spec, not a teaching doc).
  - a learn-PASM tutorial — that's **DeSilva**.
- **Discipline:** every place a subsystem is introduced, the guide **orients then links out** ("smart pins do
  X — the 32 modes are in the Blue Book"). Link-out, never duplicate. This boundary is the manual's contract.

## 3. Why this is a unique community contribution ("why us")
The community has the Silicon Doc (dense spec), deep topic manuals, and scattered forum lore. **No one is
producing a curated, trust-chain-verified "how to think in P2."** We can — because we have the cross-source-
verified KB behind it, *and* we have just built the P1→P2 delta catalogue, so this guide can also serve the
large P1-veteran community migrating to P2. The capstone (functional decomposition as a *spatial-computing
discipline*) is a genuinely original framing no existing P2 document offers.

## 4. Target audiences (four, dual-served)
1. **Newcomer with MCU background** — needs the mental model before any manual makes sense (the on-ramp).
2. **P1 veteran migrating to P2** — knows cogs/hub; needs "what's the same, what's new" (smart pins, CORDIC,
   streamer, events) — leverages our P1→P2 delta work (§9).
3. **Working P2 dev** — can write a cog; wants the *decomposition discipline* to stop building accidental
   sequential machines on parallel silicon (the capstone, Ch3).
4. **AI code-generating agent** — served the same orientation via the KB YAML (dual-rendering, §8).

## 5. The altitude arc — chapter architecture (4 chapters; a GUIDED ASCENT)
**Pedagogical spine (Stephen, 2026-06-22):** comfort first, abstraction last. Less-experienced engineers must
feel at home with the P2 before we ask them to think like architects. So Chs 1–3 are concrete and welcoming —
picture the chip, learn to *read* its code, then *use* the features; Ch4 (the meta / experienced-engineer
lens) comes last and is deliberately earned. **The "spatial-computing fabric" thesis is itself meta — it
anchors Ch4, NOT Ch1.**

**Ch2 added (Stephen, 2026-06-23):** the original 3-chapter plan assumed the reader could already read a
structured language. But the primary audience includes people coming with **no P1, no Spin2, and no PASM2** —
they have never seen a `CON`/`PUB`/`DAT` block, indentation-as-structure, or a PASM2 instruction. Showing the
**language structure** is therefore essential, and it earned its own chapter rather than being crammed into
the hands-on chapter. (The P1 ecosystem met this need with a separate "Propeller Programming Tutorial" that
shipped in the Propeller Tool's on-line help — *not* in the bound manual; we fold that role into the guide.)

| Ch | Title (working) | Altitude | Purpose | Defers to |
|----|-----------------|----------|---------|-----------|
| 1 | **Meet the Propeller 2** | the territory, concretely | warm, feature-first mental model: the parts you can picture — 8 cogs, pins, hub, smart pins, CORDIC, streamer/FIFO, events, memory/boot, clock — and what each *does*. Build intuition through features, NOT abstraction. (Quietly seed one idea: "each cog just keeps running, independently" — Ch4 cashes it in.) *Orient, don't spec.* | Silicon Doc, datasheet, the topic manuals |
| 2 | **Reading P2 Code** | the language, structurally | give a from-zero reader (no P1, no Spin2/PASM2) the structural literacy to read **every example in the guide**. Teach enough STRUCTURE to read fluently — NOT a language reference. | Spin2 v55 doc, PASM2 manual, DeSilva tutorial |
| 3 | **Putting It to Work** | the basics of doing | *use* the features — launch a cog, drive a pin, the Spin2-vs-PASM2 choice, the object/run-time model, hub sharing, boot/run. Comfort through doing; this is the "rich feature intro+use" chapter. | Spin2 v55, PASM2 manual, Smart Pins/Streamer guides |
| 4 | **Thinking in P2 — Functional Decomposition** | the capstone (advanced) | *now* the spatial-computing thesis (space vs time) + the forces (resource ownership/timing, data-flow contracts, rate adaptation, emergent altitude) + the **first-contact procedure** + ONE worked derivation. **Teaches the METHOD of deriving an architecture — never prescribes one.** | the decomposition YAML layer (its golden home) |

### Ch2 "Reading P2 Code" — definition of done (the anti-shortchange contract)
A reader with **no P1, no Spin2, no PASM2** must, after this chapter, be able to read every code example in
the guide unaided. Each objective below must be covered (sourced from the Spin2 v55 doc + the PASM2 manual,
never from memory):

1. The six Spin2 block types — `CON` `OBJ` `VAR` `PUB` `PRI` `DAT` — and what each holds (`CON` is the
   default/initial block; a block runs until the next block keyword).
2. A file *is* an object; **at least one `PUB` is required** and execution begins at the **first `PUB`**.
3. Method anatomy: `PUB name(params) : return | locals`; how one method calls another; built-ins like
   `pinhigh`/`waitms` are **method calls, not keywords**.
4. Objects compose: `OBJ` instantiates another file; you call `obj.method()`.
5. **Indentation is structure** (no braces / `begin`–`end`); the `repeat` / `if` / `case` shapes.
6. Values: `:=` (assign) vs `=` (constant); `_` digit groups, `$` hex, `%` binary; named constants.
6a. **Line continuation `...`** — a line ending in `...` continues onto the next (rest of the line ignored);
    this is *also* how the guide keeps long statements within the page width, so it appears in examples.
7. Comments (`'` to end of line).
8. PASM2 instruction anatomy: `{condition} mnemonic dest, source {effects} ' comment` — `#` immediate,
   `##` full 32-bit immediate, `wc`/`wz` flag effects, conditional execution (`if_z`, …) exist (defer depth).
9. Where PASM2 lives: a `DAT` cog program or inline `org`/`end`; even "pure assembly" sits in a Spin2 file.

**Coverage gate:** after authoring, extract every Spin2/PASM2 construct used in ANY example across the whole
guide and confirm each is introduced here (or is safe from context). Constructs to watch: `...`, `org`/`end`,
`:=` vs `=`, `obj.method()`, and method-call-not-keyword.

Front matter: the thesis + how to read (audiences/paths) + the accessible MCU↔FPGA hook (§5.1). Back matter:
glossary (from `decomposition-glossary.yaml`) · a "where to go next" map into the reference manuals ·
**Appendix A — Computing in Space and Time: Why We Borrow FPGA Language** · **Appendix B — Further Reading on
Functional Decomposition**. (P1→P2 migration is woven as sidebars, not an appendix — §9.)

### 5.1 The space/time (MCU↔FPGA) framing — placement
The P2 straddles the microprocessor and FPGA design spaces; the deep "why" is that **an MCU computes in time,
an FPGA computes in space, and the P2 is a coarse-grained spatial fabric** (already formalized in
`architecture/decomposition/spatial-computing.yaml`). This framing lives in **three** places, by altitude:
- **Front-matter hook (accessible):** "you know microcontrollers; you've heard of FPGAs; the P2 lives in the
  gap between them." Familiar landmarks, concrete — fits comfort-first, no abstraction.
- **Ch3 (teaching):** the formal space-vs-time thesis as the rationale for the decomposition forces.
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

> **Reading paths** (one slim book, four audiences): newcomer = 1→2, then 3 when ready; P1 vet = follow the
> "P1 note:" sidebars through 1, then 3; working dev = straight to 3, 1–2 as reference.

> **⚠️ Ch3 anti-prescription principle (load-bearing, Stephen 2026-06-22).** The final decomposition is
> **unique to every project** — we **cannot and must not prescribe outcomes**. Ch3 teaches *techniques for
> thinking* (the forces + the first-contact procedure); the reader/agent then *derives* their own. This is the
> decomposition layer's own thesis: understand the forces → derive a sound architecture for a machine you've
> never seen; have only the catalogue → you can only pattern-match. **The robot-dog derivation is a
> DEMONSTRATION of the method running on one machine, explicitly NOT a template** — framed "your machine will
> derive a different, equally sound answer." The chapter's takeaway is the *method*, never the example's object set.

## 6. Source map (trust-chain grounding — nothing invented)
| Chapter | Primary sources (already in-repo) |
|---------|-----------------------------------|
| Ch1 | `deliverables/ai/P2/architecture/` — `p2-architecture-mental-model.yaml` (the AI-facing half, **already written**), `cog.yaml`, `hub.yaml`, `cordic.yaml`, `streamer/`, `event_system.yaml`, `interrupts.yaml`, `clock_system.yaml`, `boot-rom/`, `locks.yaml`, `lookup_ram.yaml`, `fifo.yaml`, `xbyte_engine.yaml`; Silicon Doc v35; P2 datasheet |
| Ch2 | `guides/spin2-getting-started.yaml`, `guides/pasm2-getting-started.yaml`; `serial_loader.yaml` / `boot-rom/`; `language/` YAML |
| Ch3 | `architecture/decomposition/` — **all 12 entries** (`decomposition-method`, `first-contact-procedure`, `resource-ownership`, `data-flow-contracts`, `rate-adaptation`, `altitude-layering`, `cross-cutting-forces`, `resource-budget`, `spatial-computing`, `evaluation-vocabulary`, `decomposition-glossary`, `worked-derivation-robot-dog`) |
| Migration appendix | `engineering/ingestion/P1-DOCUMENT-LINEAGE.md` (P1↔P2 edges) + `central-analysis/p1-p2-comparison/P1-P2-FEATURE-COMPARISON.md` |

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
- **D1 — Name:** ✅ *The P2 Architect's Guide — Thinking in Cogs, Pins, and Forces.* ⚠️ *Open tension:*
  "Architect's" leans advanced and slightly cuts against the welcoming goal; held as **aspirational** ("this
  guide makes you a P2 architect"), with the warm Ch1 + subtitle doing the welcoming. Revisit only if it
  reads as a gate.
- **D2 — Four chapters** (revised 2026-06-23, was "three"): Ch1 picture the chip · **Ch2 read the code
  (NEW)** · Ch3 put it to work · Ch4 think in P2. **decomposition is LAST and earned**; Chs 1–3 are the
  concrete, comfort-building ascent (§5). The added Ch2 "Reading P2 Code" exists because the audience
  includes readers with no P1/Spin2/PASM2 background who must be shown the language *structure* before any
  example will read (its DoD is in §5).
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
  roster invariant; promote to Live on release.
- **Platform:** ride the shared `p2kb-platform-*` stack + thin local overlay (consistent with the unification
  effort); shared common cover.

## 14. Next steps
1. ✅ D1–D6 resolved (§11), pedagogy spine + anti-prescription + voice gradient locked.
2. **NEXT:** draft the formal `creation-guide.md` + `voice-guide.md` from this charter (house format) —
   creation-guide carries the chapter specs + source map + verification protocol; voice-guide carries §10
   (positioning, altitude gradient, the warm-but-not-glib / not-prescriptive rules).
3. Then opus-master authoring Ch1→Ch3, each verified against its source-map and (Ch3) the decomposition YAML,
   with the anti-prescription gate (§12) applied to every Ch3 section.

## 15. Future / candidate additions (PARKED — not up next, don't forget)

A small pipeline of things we may want, surfaced 2026-06-23 while reconciling against the **Propeller
Manual v1.0** (ISBN 1‑928982‑38‑7). That edition carried *two* from-zero chapters that v1.2 removed
(moved to the Propeller Tool on‑line help): **Ch2 "Using the Propeller Tool"** and **Ch3 "Propeller
Programming Tutorial."** Our guide now has the language (Ch2 "Reading P2 Code"), but not the toolchain
how‑to. Candidates:

- **CANDIDATE CHAPTER — "Using {toolchain}"** (the modern analog of v1.0's "Using the Propeller Tool").
  A from‑zero reader is told to "use your development tool" but never *how* to build, load, and see output.
  Cover the actual P2 toolchains and the build→load→run→observe loop: **SPIN Tools IDE**; **VS Code + the
  spin2 extension + `pnut-ts` (compiler) + `pnut-term-ts` (terminal / DEBUG window)**; loading to a board
  (the Edge module we now picture in Ch1), and seeing `DEBUG`/serial output. `{toolchain}` is deliberately
  a slot — the guide should not marry one IDE. Likely a short chapter or an appendix; revisit chapter
  count if added (we're at four). **Not up next.**
- **INGEST the v1.0/v1.01 Propeller Programming Tutorial** into the P1 corpus — logged as gap **G‑P1‑007**
  (recoverable: v1.01 PDF archived at nagasm.org / archive.org). Value: a P1‑corpus source AND a pedagogy
  model. NB it teaches **Spin1/PASM1**, so it's a *model* for our P2 Ch2, never a content source.

## 16. Shape refinement — the three-act book (Stephen, 2026-06-24, RECORD-ONLY SEED)

> **Status:** dictated shape notes captured before building. This is the **seed** of the
> reworked plan; we flesh it out into detail and generate initial content in a later working
> session. It supersedes the loose "front-end pillar + AI-assist pillar" framing in the
> NEXT-SESSION note and gives §15's parked "Using {toolchain}" candidate a concrete home.
> Reconcile §5 (chapter architecture) into this three-act shape when we next flesh the plan.

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
