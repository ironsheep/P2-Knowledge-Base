# Punch List — P2 Debug Window Manual

Outstanding work items. Sweep completed items into a dated archive at closeout.

## PDF Review Cycle — opened 2026-06-08 (R1–R5 DONE + render-verified v8/v10; STAGED to outbound)

**All five implemented and proven in the daemon render; staged to outbound 2026-06-08.**
- R1 ✅ kind-aware bars "Configuration Directive" / "Update Directive", `\footnotesize`
  quiet label (sourced from XXX_Configure/XXX_Update phases). 2 config + 21 update blocks.
- R2 ✅ `SET` two-line variant form (Cartesian / polar) with mode comments.
- R3 ✅ brace audit vs REF DIRECTIVE-MATRIX (required unbraced); directive blocks lost
  stray line-numbers; channel-defs → Configuration, runtime → Update.
- R4 ✅ chapter title + lighter grey "deck" subtitle (`\chaptersubtitle` macro in
  platform-foundation + auto-split on " — " in platform-pagination filter); TOC +
  running head show window title only.
- R5 ✅ Appendix A dense `·`-lists → 22 house-style tables (Directive | Notes; Code |
  Effect for TERM codes). Fixed a pipe-in-cell + the ≥ font-gap (→ `>=`, data-set-wide).
**Staged platform files (hash-changed): code-coloring.lua, pagination.lua, foundation.sty
+ the escaped md + assets/fig-03-term-first.png.** ⚠️ Last deploy the assets/ subdir did
NOT transfer (missing-asset build failure) — this deploy MUST get fig-03-term-first.png
into the Forge inbox/assets/.

---

## PDF Review Cycle — opened 2026-06-08 (GATHERING; do not fix until list complete)

Stephen is reviewing the first production PDF, feeding findings one at a time. Gather
all → discuss → resolve as a batch → re-render once (document-finalize discipline).

- **R1 — relabel the blue "DEBUG Syntax" bar.** Stephen: "Window Syntax" is too broad
  — each block is ONE **directive**, and a window has many. Use "directive" terminology.
  **PROPOSAL (pending Stephen):** make the bar *kind-aware*, matching Ch 1's taxonomy
  (creation-line config / runtime commands / shared): **"Creation Directive"** (e.g.
  LOGIC/SCOPE channel declarations on the creation line) vs **"Runtime Directive"**
  (CARTESIAN, SET, DOT, TRIGGER, …). Each block tagged with its kind (two fence classes
  → two filter branches). Bonus: the bar then tells the reader *when* the directive is
  used. Open: handle CLEAR/SAVE as "Runtime" or add a 3rd "Shared Directive"? Also a
  light terminology note — prose says "commands/keywords/configuration"; bars would say
  "directive" (synonym, fine, but worth one consistency check).
  **LOCKED (2026-06-08):** sourced from `DebugDisplayUnit.pas` phases (`XXX_Configure` /
  `XXX_Update`, per REF DIRECTIVE-MATRIX): two kind-aware bars — **"Configuration
  Directive"** (creation-line / Configuration phase) and **"Update Directive"** (Update
  phase — post-creation directives, data feeds, and shared CLEAR/SAVE/UPDATE). Two fence
  classes (`debug-config` / `debug-update`), one blue bar style. Shared commands fold
  into Update (no 3rd label). Label de-emphasized: title `\small\bfseries` → `\footnotesize\bfseries`
  family-wide (directive content stays prominent; the quieter tag also applies to the
  Spin2/PASM2 syntax tags in other manuals — intended, keeps the family uniform).
- **R2 — PLOT `SET` shown as TWO variant lines.** `SET` has two genuinely different
  forms: `SET x y` (Cartesian) and `SET rho theta` (polar) — different parameter
  *names*, not just optional presence. Show two lines, each with a trailing comment
  naming the mode (Cartesian / polar).
- **R3 — optional-vs-required rigor in every debug-syntax block.** `{}` must mean
  *genuinely optional*. Don't wrap required params in `{}`. Principle: same params,
  optionally present → ONE line with `{}` (the `ORIGIN` layout is the model); forms
  with DIFFERENT param names (variant syntaxes, e.g. `SET`) → SEPARATE lines. Audit
  all debug-syntax blocks for correct brace usage.
- **R4 — long two-part chapter headings → title + subtitle/deck.** e.g. "Ch 9: The
  FFT Window — Frequency Spectrum" → chapter title "The FFT Window" + a styled
  subtitle "Frequency Spectrum" (smaller, not chapter-sized; maybe italic; NOT a
  numbered section). *(discuss — pedagogy + whether platform-wide or this-manual; a
  width/presentation decision)*
- **R5 — Appendix A optional-value lists still hard to read.** Has the corrections
  asked for, but the dense `·`-separated per-window keyword lists are still a legibility
  strain. Take a readability pass. *(softer)*

**Resolutions (2026-06-08):**
- R2/R3 → **proceed**, source-verified: correct required-vs-optional braces against the
  golden source (REF/theory-of-operations + Spin2 DEBUG docs), and split variant forms
  with different param names onto separate commented lines (`SET x y` Cartesian /
  `SET rho theta` polar). Don't trade one wrong signal for another — verify each.
- R4 → **AGREED.** Platform-level `\chaptersubtitle` + a Lua filter that auto-splits a
  chapter heading on " — " (before = title, after = subtitle). Subtitle: roman, lighter
  weight, sub-chapter size (not numbered, not a `##`). TOC shows the window name only.
  Pilot here; other manuals adopt for free.
- R5 → **AGREED approach:** convert Appendix A's dense `·`-separated optional-value
  lists into proper **tables** (house table styling is good + consistent; users already
  see tables throughout).

**Approved in review:** the back-matter Index ("looks really good"); the blue-bar
block *design* (relabel only).

---


## Platform migration + content-conversion proof batch (opened 2026-06-07, IN PROGRESS)

Debug Window migrated to the shared platform stack (twin) and put through Stephen's PDF
proof. The migration revealed that a platform migration is ALSO a content-convention
adoption, not just a stack swap (shared macros were loaded-but-uncalled). Batch of 10
fixes; **7 done in opus-master and daemon-proven (v3, run
`engineering/pdf-forge/interactive-testing/test-runs/debugwin-platform-v3_1780878163345/`);
3 remain.**

**DONE + verified (v3: 0 serious signatures, 122 pp, 12 imgs):**
1. All 10 figures `![](){width=}` → `\screenshotfig[width=N\linewidth]{}`+`\caption` (platform keyline). ch03–ch11.
2. Cover-fit: front-matter.md dropped `\vfill`, wrapped org panel in `\footnotesize`, tightened vspaces → footer now 44.7pt margin (was −4.6pt off-page).
3. Four part intros written in voice (part-1..4-*.md).
4. Part II divider moved before ch03-term in assemble-manual.sh → TERM now in "The Windows" (matches cover).
8. Screenshot slot at first TERM number example (ch03 "Sending text", `Temperature:`), placeholder `assets/fig-03-term-first.png` (generated via fitz; REAL capture still pending).
9. Appendix A: blank lines between Create/Config/Feed/Runtime (NOT tables — just de-jumble).
10. Ch1 "Configuration versus commands" — names the 3 keyword flavors (creation-config / runtime command / shared) + window lifecycle (no CLOSE).

**REMAINING (1 of 3 — #7 content sweep):**

5. **DONE (2026-06-08).** Decision resolved: added a neutral **`debug-syntax`** class
   to `p2kb-platform-code-coloring.lua` (both platform + interactive-testing copies):
   blue bar, title **"DEBUG Syntax"** (DEBUG-window display directives are a Spin2
   sub-language, not core Spin2 — so neither "Spin2 Syntax" nor "PASM2 Syntax" fit).
   Converted all 23 bare directive blocks → `` ```debug-syntax `` (ch05×18, ch06×3,
   ch07×2). Also reclassified two mis-fenced bare blocks found during the sweep:
   ch02 `pnut_ts -d` → `` ```command ``; ch09 bin-frequency → `` ```formula ``.
   **"Add to TERM" — RECOMMEND DROPPING:** on inspection, PLOT/LOGIC/SCOPE present
   their *declaration* identically to TERM (a `spin2` example + config table); their
   debug-syntax blocks are exclusively for argument-bearing *runtime* directives,
   which TERM does not have (its runtime surface is command-codes — already a table —
   plus no-arg keyword commands). Adding a syntax block to TERM would CREATE
   inconsistency (TERM would be the only simple window with one) and duplicate its
   command-code table. TERM is already consistent with its peer simple windows
   (BITMAP/SCOPE_XY/SPECTRO/MIDI). Awaiting Stephen's nod to close this sub-item.
6. **DONE (2026-06-08).** Added stable `{#ch-N}` / `{#appendix-x}` IDs to all 17
   headings; linked every cross-ref (`Chapter N`, `Ch N`, `Chapters X and/through Y`,
   `Appendix A–C`) across chapters + appendices + part dividers, without changing the
   author's wording. Both "Where to go next" sections, the ch01 roster table, and the
   ch02 graphical-windows list are clickable. Validated: 17 IDs each defined once, all
   link targets resolve, no duplicates.
7. **DONE (2026-06-08) — index built the house way, NO forge change.** Stephen
   corrected the approach: this repo's manuals (e.g. deSilva) carry a **hand-authored,
   chapter-referenced markdown Index** (`# Index` / letter dividers / `- term: ChN`),
   NOT a LaTeX `\index{}`+makeindex index. The makeindex route was the wrong machine.
   Resolution: generated `opus-master/index.md` (87 entries, letter-grouped, command
   keywords in `\texttt`, concepts plain, window entries labeled, **clickable** `[ChN](#ch-N)`
   refs reusing #6's anchors) from the 144-tag term→chapter data; removed all `\index{}`
   tags (restored pre-sweep chapter backups — #5/#6 intact); reverted the `\printindex`
   template wiring and the escape-script `\index` tweak; added `index.md` to
   `assemble-manual.sh`. Heading uses a raw `{=latex}` `\chapter*{Index}` block
   (escaper-safe → unnumbered, TOC-linked). **Proven (v7): 127pp, Index pp.126–127, 63
   working chapter links, 0 serious sigs.** (Debug gotchas found + fixed en route: a
   `$body$` token inside a template *comment* made pandoc emit the whole body twice
   → 253pp; the escaper escapes `{.unnumbered}` braces but not `{#id}`.)
   **(superseded — kept for history:)** Template wired
   (`\printindex` + TOC-linked "Index" back-matter in `p2kb-debugwin.latex`). Curated
   `\index{}` sweep DONE: **144 tags / 87 distinct entries** across 14 chapters
   (canonical spellings from Appendix A; placed via 7 parallel subagents + verified —
   strip-test reproduces backups byte-for-byte, none in fences/tables/headings, all 144
   survive the escape script). **The daemon proof (v4/v5) PROVED the index does NOT
   render — and exactly why:**
   - v4 compile log: `Writing index file input.idx` → **`No file input.ind`**. xelatex
     collects the tags into `.idx`, but `makeindex` never runs, so `\printindex` emits
     nothing. (Confirms pandoc's single `--pdf-engine=xelatex` call does NOT run makeindex.)
   - v5 tried the in-LaTeX auto-run workaround (`imakeidx` + `--pdf-engine-opt=-shell-escape`).
     Shell-escape worked (makeindex WAS invoked) but failed structurally: (a) pandoc runs
     xelatex with `-output-directory /tmp/tex2pdf.XXX`, so the `.idx` lands there and
     imakeidx's makeindex call can't find it (`Input index file input.idx not found`);
     (b) `\printindex` sits immediately before `\end{document}`, so the `.idx` isn't
     flushed when imakeidx fires. In-LaTeX auto-run fundamentally fights pandoc's
     single-call + output-directory model. **Reverted the imakeidx experiment; platform
     stays `makeidx`.**
   - *Side finding:* "mirror the Streamer indexed index" is moot — Streamer (and every
     other manual) has no real `\index{}` tags; this pipeline has never been exercised.
   **DECISION NEEDED (forge-side, affects all manuals, needs redeploy):** make the Forge
   build run makeindex. Cleanest: switch the build's pdf-engine from bare `xelatex` to
   **`latexmk -xelatex`** (auto-runs makeindex + handles passes) in the daemon
   (`DEPLOY-TO-FORGE-watch-shared-workspace.js`) and production (`generate-pdf.js`); or
   a pandoc→.tex then xelatex/makeindex/xelatex loop. The 144 tags are already placed, so
   the index "just works" the moment the build runs makeindex.

**Production re-stage state:** the outbound bundle is the PRE-batch version. After the
batch completes, re-run prepare-manual to re-stage — and the NEW
`assets/fig-03-term-first.png` must reach `outbound/.../assets/`. The escape-script
`{width=}` protection fix lives in `engineering/tools/conversion/latex_escape_processor.py`
(uncommitted) — needed by the production escape; commit it as its own change (benefits all
manuals).

**Git:** ~28 uncommitted files (opus-master content + workspace template/request/assemble +
new debugwin-local.sty + escape-script fix + creation-guide K=76 + document-finalize overlay
directive). Suggest 2+ commits: (a) Debug Window migration+content batch, (b) shared
escape-script `{width=}` fix. Daemon left RUNNING.

## Screenshot capture — figures pending (opened 2026-06-02)

The screenshot-capture pipeline (`screenshot-capture/`, run on a P2 with `pnut-ts`
compile + `pnut-term-ts -r` run; each example `SAVE`s its own window; `CLOSE` makes it
hands-off) works end-to-end. **5 of 10 hero figures render correctly and are in the
manual; 5 are placeholders pending these fixes:**

**Captured & in the manual (real images):**
`fig-04-bitmap` (plasma) · `fig-05-plot-gauge` · `fig-05-plot-sprite` · `fig-06-logic`
(8-ch counter) · `fig-11-midi` (keyboard; see note).

**Placeholders pending — two root causes to solve:**

1. **Channel-config windows ignore the channel definition.**
   - `fig-07-scope` — shows "Channel 0" at 0–255 (my `'Wave' lo hi` range had no effect),
     so the ±1000 sine clips into a trapezoid.
   - `fig-09-fft` — empty frame; the channel def (`'Mag' …`) produced no magnitude trace.
   - `fig-10-spectro` — empty waterfall (also magnitude/RANGE/MAG scaling).
   - LOGIC's channel defs *worked* on the creation line, but SCOPE/FFT's do not.
   - **Action:** study `REF/theory-of-operations/{SCOPE,FFT,SPECTRO}` for the exact
     channel-definition placement (creation-line vs update-phase) and the magnitude
     scaling, instead of guessing.

2. **"Only the first message registers."**
   - `fig-03-term-dashboard` — TERM text won't render: positioned version showed one stray
     glyph; plain-text version is fully blank. (Graphics windows render their own text
     labels fine, so pnut-term-ts *can* draw text — TERM character output specifically isn't.)
   - `fig-11-midi` — only the first of three note-ons lights (single key, not the C-E-G
     triad). The keyboard image itself is good, so it ships as-is for now.
   - `fig-08-scope-xy` — never produces a `.bmp` at all; the Lissajous window may not open
     or the example errors at runtime.
   - **Action (needs live observation on hardware):** when each runs, does the window show
     content *live* before it closes (→ SAVE-timing) or is it blank/absent live (→ render
     bug)? Then fix accordingly.

**Confirmed working technique notes (for when we resume):**
- `DEBUG_DELAY` (≈1000 ms) before transmitting is required so the host window is open.
- Rapid feeds race; **pace them** (a small `waitms` per row fixed the BITMAP streaks).
- `` `Win CLOSE `` *does* work (closes the window, enables hands-off capture) — the golden
  matrix is wrong that it "has no live handler"; flag for upstream REF correction, and add
  `CLOSE` to ch01's "commands common across windows".

## Other

- (none yet)
