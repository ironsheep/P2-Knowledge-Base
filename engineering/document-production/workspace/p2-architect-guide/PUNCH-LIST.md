# The P2 Architect's Guide — Punch List

Active-work register. Completed items are swept into the dated archive at the bottom at
each closeout; the list above carries only **outstanding** work.

---

## Outstanding

- [ ] **Emoji / marker glyph drop (cosmetic, guide-wide).** The 💡 (U+1F4A1), ⚠ (U+26A0),
      and the U+FE0F variation selector are **dropped as missing glyphs** by the platform
      fonts (emoji only — no other glyph missing). They degrade **gracefully**: the bold
      `**Tip:**` / `**Watch out:**` label still renders, no tofu box. Guide-wide (every
      chapter + front matter use the same markers), so it's a style decision, not a local
      patch. **ADDRESSED (AG-14, 2026-07-08):** the guide now maps the warning + bulb markers to
      **fontawesome** icons (`\WatchoutIcon` / `\TipIcon` in `p2kb-architect-local.sty`) via an
      `\IfFileExists{fontawesome5.sty}` guard that falls back to bold `[!]` / `[*]` text if the
      package is absent — either way, **no tofu**. The emoji stay in the markdown; a Str handler in
      `p2kb-architect-local.lua` converts them (survives the latex-escape pass). **Confirm the icons
      render in the v1.0.0 PDF, then close.** (Guide-local for now; promoting the fallback-font
      approach platform-wide for the other manuals stays a style-pass call.)

- [ ] **Platform: tall non-encoding tables silently drop overflow rows** (flagged for
      `project_manual_layout_standards`). `p2kb-platform-tables.lua` routes a tall, non-encoding
      multi-col table to a **non-breaking `tblr`** (tabularray), which clips rows past the
      page bottom with **no compile error**. Caught here on the Appendix A 12-row table
      (worked around by splitting it into two 6-row tables); the 5-row budget table was fine.
      The filter's breakable-vs-non-breaking heuristic should route tall tables to `longtblr` —
      it can bite any manual with a long explanatory table.
      **Fix:** in `p2kb-platform-tables.lua`, route a tall / non-encoding multi-column table to
      **`longtblr`** (breakable) instead of `tblr`. **How to prove it's fixed — use the layout
      torture test** (`engineering/document-production/workspace/p2-layout-torture-test/`): add a
      fixture case with a **non-encoding multi-column table long enough to overflow one page**
      (~20+ rows), generate it on the PDF Forge, and confirm **every row appears** — the overflow
      rows flow onto the next page rather than being silently clipped, with no compile error.
      Proven fixed when that fixture's full row count is present in the rendered PDF. *(Also logged
      to the platform layout-standards effort — `methodology/manual-layout-standards-INPUTS.md`.)*

- [x] **Calibration-box density — RESOLVED 2026-07-08.** The robot-decomposition diagram (now
      Figure 9.1) was redrawn to the real **three-cog** structure; per-unit **servo** calibration
      now sits on the **COG A** side, clear of the I/O cog. No longer tight. (Sweep at closeout.)

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
