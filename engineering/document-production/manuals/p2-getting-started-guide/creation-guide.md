# Getting Started with the Propeller 2 — Creation Guide

> **Split note (2026-06-24):** This book was split from the original *P2 Architect's Guide* first
> draft (4 chapters). This is now the **Getting Started** orientation book — a warm on-ramp that
> teaches what the P2 IS, how to READ its code, and how to USE its features (three chapters). The
> functional-decomposition chapter, the spatial-computing thesis, the FPGA-language appendices
> (A/B), and the decomposition glossary moved to the advanced design book; their creation guidance
> now lives in `manuals/p2-architect-guide/creation-guide.md` (*The P2 Architect's Guide —
> Designing Real Systems on the Propeller 2*). This guide links readers to that design book as the
> next step.

**Canonical Name:** `p2-getting-started-guide`
**Document Title:** Getting Started with the Propeller 2
**Created:** 2026-06-22 (as the Architect's Guide first draft) · **Split:** 2026-06-24
**Planning charter:** `PLANNING.md` (the rich-planning phase this guide is derived from — read it for the *why*)

---

## 1. Document Identity

### 1.1 Purpose and Scope
This is the **orientation on-ramp** that sits *above* the P2 reference manuals and welcomes a newcomer to the
chip. It does three jobs: it **introduces** the P2 as a set of features a newcomer can picture, it teaches how to
**read** P2 code so no example is opaque, and it shows how to **use** those features in a running program. It is
deliberately **slim** — no length cap, but kept brief by a strict link-out discipline (it orients, then points to
the deep manuals; it never duplicates them). The advanced design-reasoning layer (functional decomposition,
the spatial-computing thesis) is the sibling book, *The P2 Architect's Guide*, to which this book hands off.

**This document IS:**
- A warm, feature-first mental model of the P2 (cogs, hub, smart pins, CORDIC, streamer, events, memory/boot).
- A reading-literacy on-ramp: a from-zero reader can read every P2 code example in the book.
- A bridge from "what the chip is" to "how I run a program on it."

**This document is NOT:**
- A Spin2 reference — that is the **Spin2 Language Reference v55** (excellent; we do not replace or duplicate it).
- A PASM2 reference — that is the **P2 Assembly Language Manual**.
- A per-subsystem deep dive — those are the **I/O & Smart Pins**, **Streamer**, and **Debug** guides.
- A re-spec of the silicon — that is the **P2 Documentation v35** (a spec, not a teaching doc).
- A learn-by-building tutorial — that is **DeSilva** (a guided build with a strong narrator).
- **A design / decomposition book.** Functional decomposition and the spatial-computing thesis are the advanced
  follow-on, *The P2 Architect's Guide* (`manuals/p2-architect-guide/`). This book hands the ready reader off to it.

### 1.2 Target Audience (the readers this orientation serves)
1. **Newcomer with MCU background** — needs the mental model before any reference manual makes sense.
2. **P1 veteran migrating to P2** — knows cogs/hub; needs "what's the same, what's new" (served by woven
   "P1 note:" sidebars).
3. **Anyone who needs to read existing P2 code** — Spin2 or PASM2 examples in the wild — and wants the literacy
   to follow them.

**Assumed knowledge:** general embedded/microcontroller literacy and a programming background. **Not** assumed:
any prior P2 (or P1) experience. The chapters build the background in order; each assumes the one before it.

### 1.3 Relationship to Other Manuals
| Manual | Relationship |
|--------|-------------|
| **Spin2 Language Reference v55** | The Spin2 reference. This guide orients you to Spin2's *role* and the Spin2-vs-PASM2 choice, then links here. |
| **P2 Assembly Language Manual** | The PASM2 reference. Same: orient, link out. |
| **I/O & Smart Pins User Guide** | The smart-pin deep dive (the 32 modes). This guide introduces *what smart pins are for*, then links. |
| **P2 Streamer Programming Guide** | The streamer deep dive. Orient + link. |
| **P2 Debug Window / Single-Step Debugger** | Tooling for observing/stepping. Referenced where relevant. |
| **DeSilva PASM2 Tutorial** | A guided PASM build with a narrator. This guide is the conceptual orientation, not a build — complementary, not overlapping. |
| **The P2 Architect's Guide** | The advanced design book (functional decomposition, spatial-computing thesis). This orientation book is its prerequisite on-ramp and hands the ready reader off to it. |
| **P1 Propeller Manual (v1.2) + P1→P2 deltas** | The structural inspiration and the source for the "P1 note:" sidebars. |

---

## 2. Document Architecture

### 2.1 Overall structure — the guided on-ramp
```
FRONT MATTER
├── Title page
├── How to read this guide (the readers + reading paths)
└── What the Propeller 2 is, in one accessible paragraph

CHAPTER 1 — Meet the Propeller 2            (the territory, concretely)
   the parts you can picture, and what each does — NO abstraction

CHAPTER 2 — Reading P2 Code                 (literacy)
   how to read Spin2 and PASM2: the object/method shape, blocks,
   the constructs that recur — so no later example is opaque

CHAPTER 3 — Putting It to Work              (the basics of doing)
   use the features: launch a cog, drive a pin, Spin2-vs-PASM2,
   the object/run-time model, hub sharing, boot/run

BACK MATTER
└── Where to go next — the map into the reference manuals AND
    the handoff to *The P2 Architect's Guide* (the design book)

(woven throughout: "P1 note:" sidebars for migrating P1 veterans)
```
Length is content-driven (no cap); link-out keeps each chapter slim.

### 2.2 Chapter rationale (the pedagogical spine — comfort first)
- **Ch1 is concrete on purpose.** A less-experienced engineer must feel at home with the P2 first. Ch1 builds
  the mental model through *features you can picture*, not through abstraction. It quietly seeds one idea —
  "each cog just keeps running, independently" — that the later chapters and the design book cash in.
- **Ch2 makes every example readable.** Before asking the reader to *use* the chip, give them the literacy to
  *read* its code. By the end of Ch2 a from-zero reader can follow any Spin2 or PASM2 example in the book.
- **Ch3 earns comfort through doing.** Using the features (launch a cog, drive a pin, choose Spin2 or PASM2)
  is what makes the chip feel approachable — and leaves the reader ready for the design book's harder lens.

---

## 3. Pedagogical Framework

### 3.1 The guided on-ramp
The guide is a single warm climb: picture the parts (Ch1) → learn to read the code (Ch2) → put the features to
work (Ch3). Each chapter earns the trust that lets the reader follow into the next. Standard explanatory moves
apply throughout: advance organizer first (big picture before parts), motivation before mechanism, concrete
imagery to build a model, differentiation by contrast so similar features become distinct.

### 3.2 Comfort first (the non-negotiable)
Every chapter assumes intelligence, not P2 experience. Every unfamiliar term is defined on first use with a
concrete use. Nothing may drift into abstraction "because it's elegant" — elegance that doesn't yet help the
newcomer belongs in the design book, not here.

### 3.3 Reading literacy (Ch2 — load-bearing)
By the end of Ch2, a **from-zero reader must be able to read every code example in the book** — Spin2 and the
PASM2 snippets the later chapters and reference manuals show. This is the definition-of-done for Ch2: any
construct that appears in a Ch1/Ch3 example, or that a reader will meet immediately in the reference manuals,
must have been made readable here (the block structure, the object/method shape, the operators and idioms that
recur). If an example elsewhere in the book uses something Ch2 never taught the reader to read, that is a defect.

### 3.4 The reader paths
Newcomer = 1→2→3 in order. P1 vet = follow the "P1 note:" sidebars through 1, then read on. Reader who only needs
to *read* existing code = 1→2, with 3 as needed. The "Where to go next" back matter points the ready reader to
the reference manuals and to the design book, *The P2 Architect's Guide*. Front-matter "How to read" states these
paths explicitly.

---

## 4. Source Materials

### 4.1 Primary sources (all in-repo; nothing invented)
| Chapter | Primary sources |
|---------|-----------------|
| Ch1 — Meet the Propeller 2 | `deliverables/ai/P2/architecture/` — `p2-architecture-mental-model.yaml`, `cog.yaml`, `hub.yaml`, `cordic.yaml`, `streamer/`, `event_system.yaml`, `interrupts.yaml`, `clock_system.yaml`, `boot-rom/`, `locks.yaml`, `lookup_ram.yaml`, `fifo.yaml`, `xbyte_engine.yaml`; P2 Documentation v35; P2 datasheet |
| Ch2 — Reading P2 Code | `language/` YAML (Spin2 syntax/methods/operators, PASM2 instruction shape); `guides/spin2-getting-started.yaml`, `guides/pasm2-getting-started.yaml`; Spin2 v55 + PASM2 manual (for link-outs) |
| Ch3 — Putting It to Work | `guides/spin2-getting-started.yaml`, `guides/pasm2-getting-started.yaml`; `serial_loader.yaml` / `boot-rom/`; `language/` YAML; Spin2 v55 + PASM2 manual (for link-outs) |
| "P1 note:" sidebars | `engineering/ingestion/P1-DOCUMENT-LINEAGE.md` (P1↔P2 edges) + `central-analysis/p1-p2-comparison/P1-P2-FEATURE-COMPARISON.md` |

> Decomposition source material (`architecture/decomposition/`) → that lives in the design book,
> *The P2 Architect's Guide* (`manuals/p2-architect-guide/creation-guide.md`).

### 4.2 Authority hierarchy
The KB YAML is the canonical home for every fact. Where YAML is silent, the P2 Documentation v35 and P2 datasheet are
authoritative for silicon facts. The manual **derives** from these and asserts nothing independently.

### 4.3 Content verification protocol (hallucination prevention)
- **Every factual claim traces to the KB / P2 Documentation v35 / datasheet.** No unsourced performance numbers, no
  invented behavior, no undocumented roadmap claims. Nothing is asserted from memory.
- **Code examples** compile-cert with `pnut-ts` (`-d` for any DEBUG code) before inclusion.
- **Reading-literacy gate (Ch2):** review every later code example against the question *"did Ch2 teach the
  reader to read every construct this example uses?"* If an example uses something Ch2 never made readable, fix
  Ch2 (or simplify the example). See §3.3 — this is Ch2's definition-of-done.
- **Link-out gate:** review every section against *"am I duplicating Spin2 v55 / the P2 I/O & Smart Pins User Guide / PASM2 manual?"*
  If yes, cut to an orientation + a link.

---

## 5. Content Specifications

### 5.1 Chapter 1 — Meet the Propeller 2
Feature-first orientation. For each subsystem: what it is (one or two plain sentences), what it's *for* (the
motivating use), and a pointer to its deep manual. Order to build intuition (cogs → hub/memory → pins/smart
pins → CORDIC/streamer → events → clock/boot). Imagery and "you" are welcome. **No** spatial-computing
abstraction; **no** exhaustive enumeration (e.g., name that smart pins have 32 modes, link to the P2 I/O & Smart Pins User Guide —
do not list them).

### 5.2 Chapter 2 — Reading P2 Code
Make every example readable. Teach the *shape* of P2 code so a from-zero reader can follow it: the Spin2
object/method structure and its blocks (`CON`/`VAR`/`OBJ`/`PUB`/`PRI`/`DAT`), the operators and idioms that
recur, indentation-as-structure, and how a PASM2 instruction reads (label · instruction · operands · effects)
so the assembly snippets later in the book and in the reference manuals are not opaque. This is *literacy*, not
a full language tour — teach what the reader will actually meet, and link out for the complete reference. Code
examples are short, `pnut-ts`-verified, and chosen to illustrate a reading construct. **Definition-of-done:**
every construct used by any example in this book (Ch1, Ch3, and Ch2 itself) has been made readable here (§3.3,
§4.3 reading-literacy gate).

### 5.3 Chapter 3 — Putting It to Work
Show the features *in use*. The cog/object/run-time model; launching cogs; the Spin2-vs-PASM2 decision (as a
*decision*, with the trade-offs, not a syntax tour); hub sharing; the boot/run model. Code examples are short,
purposeful, and `pnut-ts`-verified, showing *why* not just *what*. Link out for full language detail. Every
construct an example uses must already be readable from Ch2 (§4.3 gate).

### 5.4 "P1 note:" sidebars
Short, optional, in-context margin/callout boxes for migrating P1 veterans: "same as P1," "changed from P1," or
"new in P2." A newcomer can ignore them; a P1 vet can navigate by them. Sourced from the P1→P2 delta catalogue.

### 5.5 Back matter — Where to go next
A light map that hands the ready reader off: the reference manuals for depth (Spin2 v55, the P2 Assembly Language
Manual, the I/O & Smart Pins User Guide, the Streamer guide, the Debug guides) and, for the reader ready to
think about *designing* systems on the P2, the sibling design book — *The P2 Architect's Guide* (functional
decomposition and the spatial-computing thesis). Each entry gets a one-line "read this when…". This is a
sign-post, not a chapter; keep it short.

---

## 6. Writing Guidelines
Voice is specified in full in `voice-guide.md`. In brief: **a mentor's guided tour — high warmth, low persona,
content-driven density**, kept maximally warm throughout (this is the orientation on-ramp). Terminology: "cog"
not "CPU" (lowercase in prose); canonical P2 terms; show code *constants*, not arithmetic values;
instruction/bit-field formatting per platform standards; inherit `repo-voice-profile.md` + the shared platform
voice. What we don't do: exhaustive enumeration, marketing, *vague* hedging (see `voice-guide.md` §2.4 —
calibrated qualifiers are required, not banned), undocumented roadmap claims, unsourced numbers.

---

## 7. Code Line Budget

- **Max code columns (K): 76**

**Provenance:** inherited from the shared platform. Getting Started is born on the unified
`p2kb-platform-*` stack and renders code through the platform code box (`p2kb-platform-content.sty`
Spin2/PASM2 blocks via `p2kb-platform-code-coloring.lua`) with the same page geometry and `Verbatim`
inset as every other platform manual — so it inherits the platform's Latin-Modern-Mono-calibrated
K=76 (the same budget the Assembly, Smart Pins, Streamer, DeSilva, Debug, and Single-Step manuals
use). Code lines are audited against K=76 by `audit-code-line-length.py` at prepare-manual time;
over-budget lines are shortened in opus-master (legal Spin2 `...` continuation or a named CON),
never typeset-wrapped.

---
*Version 0.1 — initial creation guide, derived from PLANNING.md (2026-06-22); reframed as the
**Getting Started** orientation book at the 2026-06-24 manual split (decomposition/appendix creation
guidance moved to `manuals/p2-architect-guide/creation-guide.md`).*
