# The P2 Architect's Guide — Creation Guide

**Canonical Name:** `p2-architect-guide`
**Document Title:** The P2 Architect's Guide — Thinking in Cogs, Pins, and Forces
**Created:** 2026-06-22
**Planning charter:** `PLANNING.md` (the rich-planning phase this guide is derived from — read it for the *why*)

---

## 1. Document Identity

### 1.1 Purpose and Scope
This is the **orientation and design-reasoning layer** that sits *above* the P2 reference manuals and ties the
subsystems together. It does three jobs, climbing in altitude: it **introduces** the P2 as a set of features a
newcomer can picture, it shows how to **turn those features into a running program**, and it teaches how to
**think about decomposing a problem** onto the chip. It is deliberately **slim** — no length cap, but kept brief
by a strict link-out discipline (it orients, then points to the deep manuals; it never duplicates them).

**This document IS:**
- A warm, feature-first mental model of the P2 (cogs, hub, smart pins, CORDIC, streamer, events, memory/boot).
- A bridge from "what the chip is" to "how I structure and run a program on it."
- A teaching of the **functional-decomposition method** — the techniques for *deriving* a sound cog/object
  architecture from physical forces.
- The human face of reasoning we also serve as AI-facing YAML (dual-target, §5.5).

**This document is NOT:**
- A Spin2 reference — that is the **Spin2 Language Reference v55** (excellent; we do not replace or duplicate it).
- A PASM2 reference — that is the **P2 Assembly Language Manual**.
- A per-subsystem deep dive — those are the **I/O & Smart Pins ("Blue Book")**, **Streamer**, and **Debug** guides.
- A re-spec of the silicon — that is the **Silicon Doc** (a spec, not a teaching doc).
- A learn-by-building tutorial — that is **DeSilva** (a guided build with a strong narrator).
- **A prescriptive design manual.** Decomposition is unique to every project; this guide teaches *how to think*,
  never *what to build* (§3.4 — load-bearing).

### 1.2 Target Audience (four readers, one slim book)
1. **Newcomer with MCU background** — needs the mental model before any reference manual makes sense.
2. **P1 veteran migrating to P2** — knows cogs/hub; needs "what's the same, what's new" (served by woven
   "P1 note:" sidebars).
3. **Working P2 dev** — can write a cog; wants the decomposition discipline so parallel silicon doesn't get
   used as a slow sequential machine.
4. **AI code-generating agent** — served the same understanding via the lightweight on-demand KB YAML (§5.7).

**Assumed knowledge:** general embedded/microcontroller literacy and a programming background. **Not** assumed:
any prior P2 (or P1) experience. Chapters 1–2 build the background; Chapter 3 assumes the reader has it.

### 1.3 Relationship to Other Manuals
| Manual | Relationship |
|--------|-------------|
| **Spin2 Language Reference v55** | The Spin2 reference. This guide orients you to Spin2's *role* and the Spin2-vs-PASM2 choice, then links here. |
| **P2 Assembly Language Manual** | The PASM2 reference. Same: orient, link out. |
| **I/O & Smart Pins User Guide ("Blue Book")** | The smart-pin deep dive (the 32 modes). This guide introduces *what smart pins are for*, then links. |
| **P2 Streamer Programming Guide** | The streamer deep dive. Orient + link. |
| **P2 Debug Window / Single-Step Debugger** | Tooling for observing/stepping. Referenced where relevant. |
| **DeSilva PASM2 Tutorial** | A guided PASM build with a narrator. This guide is the conceptual/architectural orientation, not a build — complementary, not overlapping. |
| **P1 Propeller Manual (v1.2) + P1→P2 deltas** | The structural inspiration and the source for the "P1 note:" sidebars. |

---

## 2. Document Architecture

### 2.1 Overall structure — the guided ascent
```
FRONT MATTER
├── Title page
├── How to read this guide (the four readers + reading paths)
├── The thesis, stated once, plainly
└── The MCU↔FPGA hook (accessible: "the P2 lives in the gap between them")

CHAPTER 1 — Meet the Propeller 2            (the territory, concretely)
   the parts you can picture, and what each does — NO abstraction yet

CHAPTER 2 — Putting It to Work              (the basics of doing)
   use the features: launch a cog, drive a pin, Spin2-vs-PASM2,
   the object/run-time model, hub sharing, boot/run

CHAPTER 3 — Thinking in P2: Functional Decomposition   (the capstone, earned)
   space vs time · the forces · the first-contact procedure ·
   ONE worked derivation (robot dog) · teaches METHOD, never outcomes

BACK MATTER
├── Glossary (from decomposition-glossary.yaml)
├── Where to go next — the map into the reference manuals
├── Appendix A — Computing in Space and Time: Why We Borrow FPGA Language
└── Appendix B — Further Reading on Functional Decomposition

(woven throughout: "P1 note:" sidebars for migrating P1 veterans)
```
Length is content-driven (no cap); link-out keeps each chapter slim.

### 2.2 Chapter rationale (the pedagogical spine — comfort first, abstraction last)
- **Ch1 is concrete on purpose.** A less-experienced engineer must feel at home with the P2 before being asked
  to think like an architect. Ch1 builds the mental model through *features you can picture*, not through the
  spatial-computing abstraction (that is meta — it waits for Ch3). It quietly seeds one idea — "each cog just
  keeps running, independently" — that Ch3 later cashes in.
- **Ch2 earns comfort through doing.** Using the features (launch a cog, drive a pin, choose Spin2 or PASM2)
  is what makes the chip feel approachable and sets up the cog/resource intuition Ch3 needs.
- **Ch3 is the capstone, deliberately last.** Functional decomposition is the experienced-engineer lens; it is
  earned by Chs 1–2, never rushed. It is also where the spatial-computing thesis finally belongs.

---

## 3. Pedagogical Framework

### 3.1 The guided ascent
The guide is a single climb in altitude: warm base camp (Chs 1–2) → a roped, careful ascent to a real summit
(Ch3). Each chapter earns the trust that lets the reader follow into the next, harder one. Standard explanatory
moves apply throughout: advance organizer first (big picture before parts), motivation before mechanism,
concrete imagery to build a model, differentiation by contrast so similar features become distinct.

### 3.2 Comfort first (the non-negotiable)
Chapters 1–2 assume intelligence, not P2 experience. Every unfamiliar term is defined on first use with a
concrete use. Nothing in Chs 1–2 may drift into abstraction "because it's elegant" — elegance that doesn't yet
help the newcomer waits for Ch3.

### 3.3 Rigor without glibness (Ch3)
Functional decomposition is a serious intellectual framework. The warmth stays, but the glibness drops to zero:
we are *careful and precise*, and we carry the rigor through a worked example the reader can follow rather than
through abstraction that lectures. The tone shift the reader should feel is "you're ready for this now," never
"buckle up, it gets hard."

### 3.4 Teach the METHOD, never the OUTCOME (load-bearing)
**The final decomposition is unique to every project — we cannot and must not prescribe it.** Chapter 3 hands
the reader the *forces* and the *first-contact procedure*; the reader then *derives* their own architecture.
This is the decomposition layer's own thesis: understand the forces → derive a sound architecture for a machine
you have never seen; have only a catalogue → you can only pattern-match. Consequences for authoring:
- The **robot-dog derivation is a DEMONSTRATION of the method on one machine**, explicitly framed "your machine
  will derive a *different, equally sound* answer." It is never a template to copy.
- Every Ch3 section must teach a *technique for deriving*, not a recommended object set. **If a passage reads as
  "do it this way," that is a defect** (quality gate, §4.4 + PLANNING §12).

### 3.5 The four-reader paths
Newcomer = 1→2, then 3 when ready. P1 vet = follow the "P1 note:" sidebars through 1, then 3. Working dev =
straight to 3, with 1–2 as reference. Front-matter "How to read" states these explicitly.

---

## 4. Source Materials

### 4.1 Primary sources (all in-repo; nothing invented)
| Chapter | Primary sources |
|---------|-----------------|
| Ch1 | `deliverables/ai/P2/architecture/` — `p2-architecture-mental-model.yaml` (the AI-facing half of this chapter, already written), `cog.yaml`, `hub.yaml`, `cordic.yaml`, `streamer/`, `event_system.yaml`, `interrupts.yaml`, `clock_system.yaml`, `boot-rom/`, `locks.yaml`, `lookup_ram.yaml`, `fifo.yaml`, `xbyte_engine.yaml`; Silicon Doc v35; P2 datasheet |
| Ch2 | `guides/spin2-getting-started.yaml`, `guides/pasm2-getting-started.yaml`; `serial_loader.yaml` / `boot-rom/`; `language/` YAML; Spin2 v55 + PASM2 manual (for link-outs) |
| Ch3 | `architecture/decomposition/` — all 12 entries (`decomposition-method`, `first-contact-procedure`, `resource-ownership`, `data-flow-contracts`, `rate-adaptation`, `altitude-layering`, `cross-cutting-forces`, `resource-budget`, `spatial-computing`, `evaluation-vocabulary`, `decomposition-glossary`, `worked-derivation-robot-dog`) |
| "P1 note:" sidebars | `engineering/ingestion/P1-DOCUMENT-LINEAGE.md` (P1↔P2 edges) + `central-analysis/p1-p2-comparison/P1-P2-FEATURE-COMPARISON.md` |

### 4.2 Authority hierarchy
The KB YAML is the canonical home for every fact and for the decomposition reasoning. Where YAML is silent,
the Silicon Doc and P2 datasheet are authoritative for silicon facts. The manual **derives** from these and
asserts nothing independently.

### 4.3 The Chapter-3 fidelity rule
The decomposition YAML layer is Ch3's **golden home**. The manual *teaches* the theory; it must not drift from
the YAML. Any improvement discovered while writing Ch3 is a **YAML update first**, then rendered in the manual.
Any Ch3 claim the YAML doesn't support is a finding (route to the corrections/gaps registers), not prose.

### 4.4 Content verification protocol (hallucination + prescription prevention)
- **Every factual claim traces to the KB / Silicon Doc / datasheet.** No unsourced performance numbers, no
  invented behavior, no undocumented roadmap claims.
- **Code examples** compile-cert with `pnut_ts` (`-d` for any DEBUG code) before inclusion.
- **Ch3 anti-prescription gate:** review every Ch3 section against the question *"am I teaching how to think, or
  am I prescribing what to build?"* The worked example must stay labeled as one machine's answer.
- **Link-out gate:** review every section against *"am I duplicating Spin2 v55 / the Blue Book / PASM2 manual?"*
  If yes, cut to an orientation + a link.
- **Citation gate (Appendix B):** every reading-list entry's author/title/year is verified against a real
  source before publish — marked NEEDS-VERIFICATION until checked. Never ship an unverified or invented citation.
- **FPGA-overclaim gate (Appendix A):** the borrowed vocabulary must never imply the P2 *is* an FPGA; the
  what-transfers/what-doesn't treatment is mandatory wherever the spatial framing appears.

---

## 5. Content Specifications

### 5.1 Chapter 1 — Meet the Propeller 2
Feature-first orientation. For each subsystem: what it is (one or two plain sentences), what it's *for* (the
motivating use), and a pointer to its deep manual. Order to build intuition (cogs → hub/memory → pins/smart
pins → CORDIC/streamer → events → clock/boot). Imagery and "you" are welcome. **No** spatial-computing
abstraction; **no** exhaustive enumeration (e.g., name that smart pins have 32 modes, link to the Blue Book —
do not list them).

### 5.2 Chapter 2 — Putting It to Work
Show the features *in use*. The cog/object/run-time model; launching cogs; the Spin2-vs-PASM2 decision (as a
*decision*, with the trade-offs, not a syntax tour); hub sharing; the boot/run model. Code examples are short,
purposeful, and `pnut_ts`-verified, showing *why* not just *what*. Link out for full language detail.

### 5.3 Chapter 3 — Thinking in P2
Open with the spatial-computing thesis (space vs time; cogs as sustained concerns). Then the forces (resource
ownership/timing, data-flow contracts, rate adaptation, emergent altitude) — each as a *lens for deriving*, with
the failure mode if ignored. Then the **first-contact procedure** (the ordered routine for an unseen machine).
Then **one** worked derivation (the robot dog) framed as a demonstration. Close on "your machine differs — the
method is the takeaway." Distilled core in-chapter; link to the YAML for the full treatment.

### 5.4 "P1 note:" sidebars
Short, optional, in-context margin/callout boxes for migrating P1 veterans: "same as P1," "changed from P1," or
"new in P2." A newcomer can ignore them; a P1 vet can navigate by them. Sourced from the P1→P2 delta catalogue.

### 5.5 Appendix A — Computing in Space and Time: Why We Borrow FPGA Language
Formalizes the design-domain positioning and justifies the borrowed vocabulary. Three parts:
1. **The temporal→spatial spectrum** — pure-temporal MCU (one instruction stream in time) → P2 (coarse-grained
   spatial fabric: 8 cogs + 64 smart pins as sustained concurrent concerns) → pure-spatial FPGA (function as
   synthesized hardware). State plainly that the P2 *straddles* the MCU and FPGA design spaces.
2. **What transfers / what doesn't** — a two-column honesty table. Transfers: concurrent sustained functions,
   partition by dataflow, rate/throughput thinking, edge processing, allocation onto a fixed resource fabric
   (the root of Ch3's "resource lattice"). Doesn't: coarse- vs fine-grained, still deterministic software not
   synthesized logic, no place-and-route/timing-closure. **Never imply the P2 *is* an FPGA** (§4.4 gate).
3. **Terminology table** — `term · FPGA-domain meaning · how it applies to the P2 · where the mapping is loose`,
   for the vocabulary already load-bearing in the KB: spatial, fabric, pipeline, dataflow, lattice,
   back-pressure, latency/throughput, systolic, coarse-grained.
Source: `architecture/decomposition/spatial-computing.yaml` + the decomposition layer's actual vocabulary.

### 5.6 Appendix B — Further Reading on Functional Decomposition
A short, curated list organized along the decomposition layer's **two axes**, each entry with a one-line
"why it's relevant to P2":
- **Logical** (cutting behavior): Parnas (information hiding); Constantine & Yourdon, *Structured Design*
  (coupling/cohesion); Page-Jones — the canon already cited in `decomposition-method.yaml`.
- **Physical / concurrent** (placing it on communicating processors): Hoare's CSP; the transputer/Occam
  lineage (the model the P2 revives — identical deterministic processors, mailbox message-passing); optionally
  Kung on systolic arrays.
**Every citation (author/title/year) verified before publish** — NEEDS-VERIFICATION until checked (§4.4). A
short correct list beats an impressive wrong one.

### 5.7 Dual-target relationship (manual ⇄ YAML)
The manual and the AI-facing YAML target the *same understanding*, shaped per medium — **not** a 1:1 mirror.
The YAML stays **lightweight, granular, on-demand** (the MCP fetches it on a single thread so an agent's context
doesn't congest); the manual is the warm human narrative. Authoring keeps them *conceptually* in lockstep
without forcing prose parity. The YAML remains the agent-facing canonical form (§4.3).

---

## 6. Writing Guidelines
Voice is specified in full in `voice-guide.md`. In brief: **a mentor's guided tour — high warmth, low persona,
content-driven density**, with the voice *modulating by altitude* (maximally warm in Chs 1–2; warm-but-rigorous,
never glib, never prescriptive in Ch3). Terminology: "COG" not "CPU"; canonical P2 terms; show code *constants*,
not arithmetic values; instruction/bit-field formatting per platform standards; inherit `repo-voice-profile.md`
+ the shared platform voice. What we don't do: exhaustive enumeration, marketing, hedging, undocumented roadmap
claims, unsourced numbers, **prescribed decompositions**.

---
*Version 0.1 — initial creation guide, derived from PLANNING.md (2026-06-22).*
