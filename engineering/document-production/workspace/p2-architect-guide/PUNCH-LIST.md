# The P2 Architect's Guide — Punch List

Active-work register. Completed items are swept into the dated archive at the bottom at
each closeout; the list above carries only **outstanding** work.

---

## Outstanding

- [ ] **Appendix B's Carloni citation overflows the right margin by 24.1pt — and has in every
      release.** `audit-pdf-margin-overflow.py` **exits 1** on it (tolerance 20pt, so 4.1pt
      beyond). Measured 2026-09-12 on both the v1.1.0 daemon render (p57) and the **released
      v1.0.3** (p49) — byte-identical overflow, so this is not new work, it is a defect that has
      been shipping.
      **The line:** `Carloni, L.P., McMillan, K.L. & Sangiovanni-Vincentelli, A.L. — "Theory of
      Latency-Insensitive` — bold IBM Plex Sans in a justified measure. TeX already broke inside
      *Sangiovanni-Vinc|entelli* and then preferred an overfull box to the badness of breaking
      after `A.L. —`. It is the longest bold author run in the appendix; the other eleven
      citations are clean.
      **Why it was NOT fixed in the v1.1.0 pass** (a dated carve-out, not a deferral): the two
      available local fixes are both worse than the defect. (a) Editing the citation — shortening
      the author list to *et al.*, or splitting the bold span — alters verified bibliographic
      text, which this project does not trade against cosmetics. (b) Inline raw LaTeX
      (`\allowbreak`, a discretionary `\-`) is **not safe in this pipeline**: the latex-escape
      pre-pass mangles inline `{=latex}` attributes, which is the documented reason
      `p2kb-architect-local.lua` converts emoji in a filter rather than in the markdown.
      **The correct fix is platform-level and belongs to its own change:** `\emergencystretch`
      (or a modest `\tolerance` lift) in `p2kb-platform-foundation.sty`, which engages only where
      a line would otherwise go overfull. That file is loaded by **every** manual, so it must be
      proven across the family on `p2-layout-torture-test`, not slipped into a content release.
      **What expires this carve-out:** the next platform-stack change that touches
      `p2kb-platform-foundation.sty` — fix it in that pass and re-run this gate on the Architect's
      Guide and at least two other manuals. Raised from the 2026-09-12 structure pass.

- [ ] **`audit-font-glyphs.py` reads the authored source, not the post-filter stream — so it
      FAILS this manual on every run, by design-accident.** The 💡 / ⚠️ / U+FE0F markers are
      deliberately left in the markdown because `filters/p2kb-architect-local.lua` `Str()`
      converts them to `\WatchoutIcon{}` / `\TipIcon{}` **before** they reach xelatex (see
      AG-14 below, and the filter's own comment explaining why the conversion lives there
      rather than in an inline `{=latex}` span). The characters never reach the font, so the
      gate's verdict is false for this document — verified 2026-09-12 twice over: by reading
      the filter, and then by finding the icons actually present in the released PDF. **Why this matters:** a gate that fails every run stops being read, and
      this one is the project's only guard against xelatex *silently* leaving a hole in the
      page. It is also the exact class the doctrine names — a gate reading the declaration
      side rather than the produced artifact.
      **Proposed fix (needs a call — it touches a shared validator every manual uses):** either
      teach the gate to apply each manual's declared glyph-converting filters before judging,
      or give it a per-manual suppression list keyed to the converting filter, so a
      *genuinely* missing glyph still fails loudly. Raised from the 2026-09-12 structure pass.

- [x] **Emoji / marker glyph drop — RESOLVED, confirmed in the artifact 2026-09-12.** The 💡 (U+1F4A1), ⚠ (U+26A0),
      and the U+FE0F variation selector are **dropped as missing glyphs** by the platform
      fonts (emoji only — no other glyph missing). They degrade **gracefully**: the bold
      `**Tip:**` / `**Watch out:**` label still renders, no tofu box. Guide-wide (every
      chapter + front matter use the same markers), so it's a style decision, not a local
      patch. **ADDRESSED (AG-14, 2026-07-08):** the guide now maps the warning + bulb markers to
      **fontawesome** icons (`\WatchoutIcon` / `\TipIcon` in `p2kb-architect-local.sty`) via an
      `\IfFileExists{fontawesome5.sty}` guard that falls back to bold `[!]` / `[*]` text if the
      package is absent — either way, **no tofu**. The emoji stay in the markdown; a Str handler in
      `p2kb-architect-local.lua` converts them (survives the latex-escape pass). **CONFIRMED in the released v1.0.3 PDF
      (2026-09-12):** all four marker sites render as fontawesome glyphs — the two Ch7
      "Watch out" callouts, the Ch8 "Tip", and the Conventions line in front matter. No tofu,
      no holes. (Text extraction shows them transliterated as `Á` / `Ď`, which is what
      fontawesome5's private-use codepoints yield — presence, not absence.) Closed. (Guide-local for now; promoting the fallback-font
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
      `org ... end`. (Generalized rule now lives in the `forge-test` skill overlay — agent-side, not shipped.)
- [x] **FIXED (test-v2 silent drop):** the Appendix A 12-row terminology table overflowed a
      non-breaking `tblr` and clipped its last two rows (GALS, Place-and-route). Split into two
      6-row tables; all 12 terms verified present. *(The underlying platform-filter cause stays
      open above.)*
- [x] **FIXED:** figure numbering rendered "0.N" (unnumbered named chapters) → continuous
      "Figure 1–5" via `\thefigure` override.
- [x] `::: p1note` sidebars render as `P1NoteBlock` boxes (warm-bronze, "P1 NOTE" title).
- [x] Cover image + title page + Guide Organization panel + TOC correct (incl. the 4-chapter update).
- [x] Code-block colors verified (Spin2 blue / PASM2 green) on test-v5..v8; no long listings to overflow.
