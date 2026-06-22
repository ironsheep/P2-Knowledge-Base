# The P2 Architect's Guide — Punch List

Outstanding work items for the Architect's Guide. Sweep completed items into a dated
archive section at closeout.

---

## Deferred to the post-first-draft visual pass (DD5 — named carve-out)

The v0.1.0 first draft is **prose-complete**; diagram authoring is its own effort
and is explicitly out of the first-draft DoD (sprint plan §"Out of scope"). The
chapters mark intended figure locations as `> **[Figure — …]**` placeholders; this
section collects them for the visual pass once the draft is reviewed.

- [ ] **Figure inventory** — sweep `architect-guide-body.md` for `> **[Figure — …]**`
      placeholders after the chapters are authored; list each here with its
      chapter + within-chapter location, then build TikZ `\Diag*` macros in
      `templates/p2kb-architect-diagrams.sty` (model: the Streamer diagrams stack).
  - **Ch1 (Meet the P2), opener** — "the whole chip at a glance": 8 COGs around a
    central hub, ring of 64 smart pins on the outside.
  - **Ch1, §Memory** — the three memory tiers: private COG RAM + LUT beside each
    processor, shared hub in the middle.
  - **Ch2 (Putting It to Work)** — no figure placeholders (code-driven chapter).
  - **Ch3 (Thinking in P2), §"Computing in space, not just in time"** — the space↔time
    spectrum: a temporal single-core MCU at one end, a spatial FPGA at the other, the P2
    between them as a coarse-grained spatial fabric of 8 COGs + 64 smart pins.
  - **Ch3, §"Watching the method run: a walking robot"** — the derived object-and-COG map
    for the example robot: bus-1 control COG (its three cooperative tasks + four-tier
    motion stack), the bus-2/IO COG, the orchestrator, the smart-pin-owned discrete
    signals, and the inter-COG seams labeled by plane (data/control/event).
- [ ] **Emoji / marker glyph render-watch** — if any ⚠️/💡/🔧-style markers are used,
      confirm they render on the first Forge build (family-consistent fallback to
      symbol macros if they box).

## First-build render review (after task #99's Forge build)

- [ ] `::: p1note` sidebars render as `P1NoteBlock` boxes (warm-bronze, "P1 NOTE"
      title) and break cleanly across pages.
- [ ] Code blocks colored (Spin2 blue / PASM2 green); a long listing near a page
      break paginates without overflow.
- [ ] Cover image + title page correct; TOC present with Ch1–3 + appendices.
- [ ] Read `output/P2-Architect-Guide.compile.log` — no silently-recovered errors
      (figure-in-figure, missing glyph, undefined box). Fix root cause before
      declaring the draft done; defects are not carried.

---

## Archive

_(none yet)_
