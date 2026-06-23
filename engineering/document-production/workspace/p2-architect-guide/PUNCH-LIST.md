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
  - **Ch3 (Thinking in P2), §"Computing in space, not just in time"** — the space-vs-time
    spectrum: a temporal single-core MCU at one end, a spatial FPGA at the other, the P2
    between them as a coarse-grained spatial fabric of 8 COGs + 64 smart pins.
  - **Ch3, §"Watching the method run: a walking robot"** — the derived object-and-COG map
    for the example robot: bus-1 control COG (its three cooperative tasks + four-tier
    motion stack), the bus-2/IO COG, the orchestrator, the smart-pin-owned discrete
    signals, and the inter-COG seams labeled by plane (data/control/event).
- [ ] **Emoji / marker glyph — FINDING (test-v3):** the 💡 (U+1F4A1), ⚠ (U+26A0),
      and the U+FE0F variation selector are **dropped as missing glyphs** by the
      platform fonts (40 `Missing character` log lines, emoji only — no other glyph
      missing). They degrade **gracefully**: the bold `**Tip:**` / `**Watch out:**`
      label still renders, no tofu box. Guide-wide (Ch1–2 use the same markers), so
      it's a style decision, not a Ch3 patch. **Resolve in the visual/style pass:**
      either (a) adopt an emoji-capable fallback font on the platform, or (b) drop the
      emoji guide-wide and keep the bold text label (matches the "rare inline markers"
      intent), or (c) follow the Streamer precedent (emoji → fenced callout). Decide
      once, apply across all three chapters + front matter.

## First-build render review (forge-test daemon round-trip, 2026-06-23)

First build (test-v1) **failed**, second (test-v2) succeeded at 41pp; defects found
and fixed in-source, re-verified on test-v3:

- [x] **FIXED (test-v1 fatal):** inline code `` `org … end` `` (Ch2) used a Unicode
      ellipsis U+2026 → `\lstinline` undefined-control-sequence under `--listings`.
      Rule: keep inline code ASCII. Changed to `org ... end`.
- [x] **FIXED (test-v2 silent drop):** the Appendix A 12-row terminology table was
      emitted as a **non-breaking `tblr`** (tabularray) by `p2kb-platform-tables.lua`
      and overflowed the page, silently clipping the last two rows (GALS,
      Place-and-route — the anti-FPGA capstone row). Split into two 6-row tables at a
      semantic seam so each fits a page. Verified all 12 terms present on test-v3.
- [x] `::: p1note` sidebars render as `P1NoteBlock` boxes (warm-bronze, "P1 NOTE" title).
- [x] Cover image + title page correct; Guide Organization panel + TOC present.
- [ ] (still to eyeball on the next build) code-block colors, a long listing near a
      page break, and the 💡/⚠️ marker glyphs.

### Platform observation (for the manual layout-standards effort)

`p2kb-platform-tables.lua` routes a **tall, non-encoding 4-col table to non-breaking
`tblr`**, which silently drops overflow rows past the page bottom (no compile error).
The 5-row robot-dog budget table is fine; the 12-row table was not. Worked around
here by splitting the table, but the filter's breakable-vs-non-breaking heuristic
should route tall tables to `longtblr` — flagged for `project_manual_layout_standards`
since it can bite any manual with a long explanatory (non-encoding) table.

---

## Archive

_(none yet)_
