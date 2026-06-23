# The P2 Architect's Guide — Punch List

Outstanding work items for the Architect's Guide. Sweep completed items into a dated
archive section at closeout.

---

## Figures — AUTHORED & VERIFIED (test-v5, 2026-06-23)

All five figures are in the document and render clean (compile log clean, numbered
Figure 1–5 continuously since the guide uses unnumbered named chapters —
`\renewcommand{\thefigure}{\arabic{figure}}` in architect-local.sty). Macros live in
`templates/p2kb-architect-diagrams.sty` (requires the shared `p2kb-platform-diagrams`).

- [x] **Figure 1 (Ch1 opener)** — P2 Edge module on a Breakout Board. **Reused photo**
      from the Parallax `64029-P2-Edge-Breakout-Board-Guide` (Parallax OK'd reuse;
      attributed "Image courtesy of Parallax Inc."). `\screenshotfig`, keyline framed.
- [x] **Figure 2 (Ch1 opener)** — 8 COGs around the hub. **Reused** `\EightCogSimpleDiagram`
      (verbatim from the Assembly manual). Caption notes the smart-pin ring is not shown.
- [x] **Figure 3 (Ch1 §Memory)** — memory hierarchy (per-COG RAM/LUT over shared hub).
      **Reused** `\CogHubRelationshipDiagram` (verbatim from the Assembly manual).
- [x] **Figure 4 (Ch3 space-vs-time)** — temporal↔spatial spectrum, P2 in between.
      **NEW** `\SpaceTimeSpectrumDiagram`.
- [x] **Figure 5 (Ch3 worked derivation)** — the robot's object-and-COG map, with the
      "one machine's answer, not a template" banner. **NEW** `\RobotDecompositionDiagram`.

Possible later polish (not blocking): Fig 5 is dense — the per-unit-calibration box sits
a little tight against COG B; a List of Figures was deliberately omitted (narrative guide).
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
