# Changelog — Getting Started with the Propeller 2

All notable changes to *Getting Started with the Propeller 2 — Meet the Chip, Read
Its Code, Put It to Work* are recorded here. The manual owns its own version (manual
head); this is the source of truth for the version string carried in `request.json`
metadata and on the title page.

Format follows the house manual-changelog convention (audience-facing, traceable to
commits). Newest entry first.

---

## v1.0.0 (2026-06-24)

**Status:** initial public release — Community Review Edition. Split 2026-06-24 from the
original *P2 Architect's Guide* first draft.

The warm, welcoming **orientation on-ramp** to the Propeller 2 — the layer that sits
below the reference manuals, teaching the mental model and the language and then
linking out rather than duplicating. It began as Chapters 1–3 of the *P2 Architect's
Guide* first draft; on 2026-06-24 that draft was split into two books, and the
orientation chapters became this one. (The functional-decomposition and system-design
material moved to the sibling *P2 Architect's Guide — Designing Real Systems on the
Propeller 2*.)

- **Three chapters**, authored from the trust-chain sources:
  **Ch 1 "Meet the Propeller 2"** (the chip — architecture YAML + the *Parallax
  Propeller 2 Documentation v35 - Rev B/C* + datasheet) · **Ch 2 "Reading P2 Code"**
  (the language *structure* for readers new to Spin2/PASM2 — the six block types,
  methods, indentation, the `...` continuation, objects, PASM2 anatomy — from the
  Spin2 v55 doc + the Assembly manual) · **Ch 3 "Putting It to Work"** (hands-on,
  pnut_ts-verified examples).
- **Where to Next** back matter: a map into the reference manuals plus a hand-off to
  *The P2 Architect's Guide* for real-system design. House-standard front matter with
  the reader paths and conventions block.
- **Three figures**, all in Chapter 1: a Parallax P2-Edge-on-Breakout photo, and two
  diagrams reused from the Assembly manual (eight cogs around the hub; the memory
  hierarchy).
- Rides the shared **`p2kb-platform-*`** presentation stack with a thin
  `p2kb-getting-started-*` local skin.
- Walkthrough-review fixes folded in at the split: the Tip callouts fenced
  (`::: tip`, was raw emoji); P1-note sidebar leads de-duplicated (the box already
  labels them); "six kinds of blocks"; and the shared mnemonic-bold filter taught not
  to bold the English words *call / push / ones / test*.
- Release-gate audited (drain gate GREEN) + finalized: redirected two forward-references
  to the (split-out) decomposition chapter to the companion *P2 Architect's Guide*,
  corrected the memory-tier access caption, and a voice pass.
- Production-verified: clean compile log, 25 pp.

_(Code examples pnut_ts-verified; code lines audited to K=76.)_
