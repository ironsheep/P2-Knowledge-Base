# Changelog: The P2 Architect's Guide

All notable changes to *The P2 Architect's Guide, Thinking in Cogs, Pins, and
Forces* are recorded here. The manual owns its own version (manual head); this is
the source of truth for the version string carried in `request.json` metadata and
on the title page.

Format follows the house manual-changelog convention (audience-facing, traceable
to commits). Newest entry first.

---

## v1.0.3 (2026-08-08)

A licensing change. No technical content changed.

- **Licensed CC BY-SA 4.0**: share and adapt this guide, including commercially, with attribution and under the same terms.


## v1.0.2 (2026-07-21)

A readability refinement. No chapters added, no technical content changed.

- **Prose**: the narrative reads with steadier pacing across its section endings. The method, the two worked derivations, and every design point are unchanged.

---

## v1.0.1 (2026-07-11)

An accuracy refinement. No chapters added.

- **External memory**: PSRAM is named as an external resource, distinct from the P2's on-chip LUT RAM, CORDIC, and streamer.

---

## v1.0.0: Maiden release (2026-07-08)

**Initial release for community review.** *The P2 Architect's Guide, Thinking in Cogs, Pins, and
Forces* is a short, narrative **design and realization** book that picks up where its prerequisite,
*Getting Started with the Propeller 2*, leaves off: where *Getting Started* teaches the chip, this
guide teaches how to **design a real system on it**, and then how to do that same work with an AI
agent at your side.

What makes it distinctive is its stance, it teaches a **method, not a catalogue**. It moves in three
acts (get a project off the ground · *derive* an architecture from physical forces rather than guess
it · walk the whole process again with an agent); its two worked derivations are labeled
demonstrations on deliberately different hardware, never templates; and it is grounded throughout in
the P2 Knowledge Base and in real, hardware-verified projects.

---

## v0.2.0: Design-book re-cut (in progress)

**Status:** re-cut sprint, started 2026-07-04. Plan: `PLANNING.md` (v2, §5 + §16 + §17).

The first draft was split after a walkthrough review: the orientation Chapters 1–3 became the
separate *Getting Started with the Propeller 2* manual (released v1.0.0), and **this book was
re-cut into the design + realization book**: the same title, *Thinking in Cogs, Pins, and
Forces*, now spanning three acts (design the system → decompose onto the P2 → realize with agent
support). This entry covers the re-cut's first pass.

- **Re-scoped to a design/realization book.** *Getting Started* is now a stated prerequisite; this
  book opens at the design desk and no longer teaches orientation. Title locked; the three-act
  architecture replaces the four-chapter plan (`PLANNING.md` §5).
- **Trimmed the migrated orientation chapters** (Meet the Propeller 2 / Reading P2 Code / Putting
  It to Work) from the master, they ship in *Getting Started*. The functional-decomposition
  chapter becomes **Act II**, bracketed by Act I (design) and Act III (agent-assisted realization),
  both still to be authored.
- **Augmented Act II against the current knowledge base.** The chapter, first drafted against an
  earlier decomposition reference, was brought back into lockstep with it: a **shared-resource
  family** under Force 1 (one owner as a shared transport, a broker cog for one-bus-many-cogs, and
  the rule-vs-encoding distinction for replicated buses); a **fan-out publication** contract under
  Force 2 with its can't-walk-it-back caution; a **decimation-placement** choice under Force 3; a
  **one-forcing-sentence-per-cog** check in the budget; a **fourth judging lens, observability**;
  a post-ship **as-built audit**; and a compact **second worked machine** (a data-plane streaming
  pipeline) that reaches a deliberately different answer from the robot dog, the clearest proof the
  method is a grammar, not a template. Also grounded the robot's servos (13: three per leg ×4 + head).

_(In development, not a public release. Front matter, creation-guide, and voice-guide re-scoping,
and the authoring of Acts I and III, are the remaining re-cut work. Two walkthrough term questions
stay open pending an author decision: the "connascence" wording and the word for the embedded
application itself.)_

---

## v0.1.0: First Draft (in progress)

**Status:** first-draft build sprint (`arch-guide-v0.1`), started 2026-06-22.
Plan: `engineering/planning/P2-ARCHITECT-GUIDE-FIRSTDRAFT-SPRINT-PLAN.md`.

The inaugural draft of a new slim manual, the orientation layer that teaches the
P2 mental model and functional decomposition, then links out to the reference
manuals rather than duplicating them. First manual born directly on the unified
presentation platform (`p2kb-platform-*`).

- Born on the unified presentation platform (`p2kb-platform-*`): the first manual
  stood up directly on the shared stack.
- **Four chapters** authored from the trust-chain sources: **Ch 1 "Meet the Propeller 2"**
  (the chip, architecture YAML + Silicon Doc v35 + datasheet) · **Ch 2 "Reading P2 Code"**
  (the language *structure* for readers new to Spin2/PASM2, the six blocks, methods,
  indentation, the `...` continuation, objects, PASM2 anatomy, from the Spin2 v55 doc +
  the Assembly manual) · **Ch 3 "Putting It to Work"** (hands-on, pnut_ts-verified
  examples) · **Ch 4 "Thinking in P2"** (functional decomposition, derived from the
  decomposition reasoning layer, anti-prescription gate applied throughout).
- Back matter: Appendix A (space-vs-time + the FPGA-terminology table), Appendix B
  (further reading, every citation verified), Glossary, Where-to-Next. House-standard
  front matter with the four reading paths and the conventions block.
- **Five figures**: a Parallax P2-Edge-on-Breakout photo; two diagrams reused verbatim
  from the Assembly manual (8 COGs around the hub; the memory hierarchy); and two new
  TikZ diagrams (the space-vs-time spectrum; the worked-derivation object/COG map).
- Verified on the PDF Forge, production PDF generated clean (48 pp); open cosmetic
  items logged to `PUNCH-LIST.md`.

_(In development, not yet a public release. Code examples pnut_ts-verified; code lines
audited to K=76. The original 3-chapter plan grew to four when Ch2 "Reading P2 Code" was
added for from-zero readers, see PLANNING D2.)_
