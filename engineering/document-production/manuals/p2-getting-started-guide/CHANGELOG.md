# Changelog — The P2 Architect's Guide

All notable changes to *The P2 Architect's Guide — Thinking in Cogs, Pins, and
Forces* are recorded here. The manual owns its own version (manual head); this is
the source of truth for the version string carried in `request.json` metadata and
on the title page.

Format follows the house manual-changelog convention (audience-facing, traceable
to commits). Newest entry first.

---

## v0.1.0 — First Draft (in progress)

**Status:** first-draft build sprint (`arch-guide-v0.1`), started 2026-06-22.
Plan: `engineering/planning/P2-ARCHITECT-GUIDE-FIRSTDRAFT-SPRINT-PLAN.md`.

The inaugural draft of a new slim manual — the orientation layer that teaches the
P2 mental model and functional decomposition, then links out to the reference
manuals rather than duplicating them. First manual born directly on the unified
presentation platform (`p2kb-platform-*`).

- Born on the unified presentation platform (`p2kb-platform-*`) — the first manual
  stood up directly on the shared stack.
- **Four chapters** authored from the trust-chain sources: **Ch 1 "Meet the Propeller 2"**
  (the chip — architecture YAML + Silicon Doc v35 + datasheet) · **Ch 2 "Reading P2 Code"**
  (the language *structure* for readers new to Spin2/PASM2 — the six blocks, methods,
  indentation, the `...` continuation, objects, PASM2 anatomy — from the Spin2 v55 doc +
  the Assembly manual) · **Ch 3 "Putting It to Work"** (hands-on, pnut_ts-verified
  examples) · **Ch 4 "Thinking in P2"** (functional decomposition, derived from the
  decomposition reasoning layer — anti-prescription gate applied throughout).
- Back matter: Appendix A (space-vs-time + the FPGA-terminology table), Appendix B
  (further reading — every citation verified), Glossary, Where-to-Next. House-standard
  front matter with the four reading paths and the conventions block.
- **Five figures**: a Parallax P2-Edge-on-Breakout photo; two diagrams reused verbatim
  from the Assembly manual (8 COGs around the hub; the memory hierarchy); and two new
  TikZ diagrams (the space-vs-time spectrum; the worked-derivation object/COG map).
- Verified on the PDF Forge — production PDF generated clean (48 pp); open cosmetic
  items logged to `PUNCH-LIST.md`.

_(In development — not yet a public release. Code examples pnut_ts-verified; code lines
audited to K=76. The original 3-chapter plan grew to four when Ch2 "Reading P2 Code" was
added for from-zero readers — see PLANNING D2.)_
