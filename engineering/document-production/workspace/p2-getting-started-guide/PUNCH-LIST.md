# Getting Started with the Propeller 2 — Punch List

> Split 2026-06-24 from the *P2 Architect's Guide* first draft; the archived
> sprint-closeout section below is that draft's history (it built five figures; this
> orientation book carries the three that live in Chapters 1–3).

Active-work register. Completed items are swept into the dated archive at the bottom at
each closeout; the list above carries only **outstanding** work.

---

## Outstanding

- [ ] **Emoji / marker glyph drop (cosmetic, guide-wide).** The 💡 (U+1F4A1), ⚠ (U+26A0),
      and the U+FE0F variation selector are **dropped as missing glyphs** by the platform
      fonts (emoji only — no other glyph missing). They degrade **gracefully**: the bold
      `**Tip:**` / `**Watch out:**` label still renders, no tofu box. Guide-wide (every
      chapter + front matter use the same markers), so it's a style decision, not a local
      patch. **Resolve in the visual/style pass:** (a) adopt an emoji-capable fallback font
      on the platform, or (b) drop the emoji guide-wide and keep the bold text label
      (matches the "rare inline markers" intent), or (c) follow the Streamer precedent
      (emoji → fenced callout). Decide once, apply everywhere.

- [ ] **Platform: tall non-encoding tables silently drop overflow rows** (flagged for
      `project_manual_layout_standards`). `p2kb-platform-tables.lua` routes a tall, non-encoding
      multi-col table to a **non-breaking `tblr`** (tabularray), which clips rows past the
      page bottom with **no compile error**. Caught here on the Appendix A 12-row table
      (worked around by splitting it into two 6-row tables); the 5-row budget table was fine.
      The filter's breakable-vs-non-breaking heuristic should route tall tables to `longtblr` —
      it can bite any manual with a long explanatory table.

- [ ] **Fig 5 density — minor polish (not blocking).** The per-unit-calibration box sits a
      little tight against COG B; tighten on the next visual pass.

---

## Archive

### Swept 2026-06-23 — v0.1 first-draft sprint closeout

**Figures 1–5 — authored & verified** (Forge daemon test-v5; compile log clean, numbered
1–5 via `\renewcommand{\thefigure}{\arabic{figure}}`; macros in `templates/p2kb-architect-diagrams.sty`):

- [x] **Figure 1** — P2 Edge module on a Breakout Board (reused Parallax `64029` photo,
      attributed; `\screenshotfig`, keyline framed).
- [x] **Figure 2** — 8 COGs around the hub (reused `\EightCogSimpleDiagram`, verbatim from the Assembly manual).
- [x] **Figure 3** — memory hierarchy (reused `\CogHubRelationshipDiagram`, verbatim from the Assembly manual).
- [x] **Figure 4** — temporal↔spatial spectrum (NEW `\SpaceTimeSpectrumDiagram`).
- [x] **Figure 5** — robot object-and-COG map + "one machine's answer" banner (NEW `\RobotDecompositionDiagram`).
- [x] Decision recorded: a List of Figures was **deliberately omitted** (narrative guide, figures are inline illustrations).

**First-build render review** (forge-test daemon round-trips test-v1..v8 + the clean production PDF):

- [x] **FIXED (test-v1 fatal):** inline code `` `org … end` `` (Ch2/now Ch3) used a Unicode
      ellipsis U+2026 → `\lstinline` undefined-control-sequence under `--listings`. Changed to
      `org ... end`. (Generalized rule now lives in `.claude/skills/forge-test/project-overlay.md`.)
- [x] **FIXED (test-v2 silent drop):** the Appendix A 12-row terminology table overflowed a
      non-breaking `tblr` and clipped its last two rows (GALS, Place-and-route). Split into two
      6-row tables; all 12 terms verified present. *(The underlying platform-filter cause stays
      open above.)*
- [x] **FIXED:** figure numbering rendered "0.N" (unnumbered named chapters) → continuous
      "Figure 1–5" via `\thefigure` override.
- [x] `::: p1note` sidebars render as `P1NoteBlock` boxes (warm-bronze, "P1 NOTE" title).
- [x] Cover image + title page + Guide Organization panel + TOC correct (incl. the 4-chapter update).
- [x] Code-block colors verified (Spin2 blue / PASM2 green) on test-v5..v8; no long listings to overflow.
