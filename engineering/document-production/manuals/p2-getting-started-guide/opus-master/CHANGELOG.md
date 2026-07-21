# Changelog — Getting Started with the Propeller 2

All notable changes to *Getting Started with the Propeller 2 — Meet the Chip, Read
Its Code, Put It to Work* are recorded here. The manual owns its own version (manual
head); this is the source of truth for the version string carried in `request.json`
metadata and on the title page.

Format follows the house manual-changelog convention (audience-facing, traceable to
commits). Newest entry first.

---

## v1.0.2 (2026-07-21)

A readability refinement. No chapters added, no technical content changed.

- **Prose polish** — a recurring summarizing phrase ("that's the whole …") was varied so the narration reads more naturally from chapter to chapter.

---

## v1.0.1 (2026-07-11)

An accuracy refinement. No chapters added.

- **Instruction timing** — most register-to-register PASM2 instructions execute in two clocks, while branches and hub accesses take more.

---

## v1.0.0 (2026-06-24)

**Initial release for community review.** A warm orientation on-ramp to the Propeller 2 —
the layer below the reference manuals: it builds a mental model of the chip, teaches you to
read P2 code, and puts it to work, then points you to the reference manuals for depth and to
the companion *P2 Architect's Guide* for whole-system design. P1-migration sidebars
throughout, with runnable, compile-clean Spin2 examples.
