# Presentation Platform Unification — Study & Spec

**Status:** Draft 1 (2026-06-06). Founding spec for migrating the manual /
presentation rendering stacks from the current **fork-per-manual** model to a
shared **platform + thin per-manual override** model.

**Predecessor:** `manual-layout-standards-{SPRINT-PLAN,USER-PREFERENCES,INPUTS}.md`
(the layout standards). This study *productizes* those standards: instead of
hand-porting each certified standard into every manual's fork, the standards
live once in a shared platform that every manual consumes.

---

## 1. Why (the root problem)

Every manual today ships its own full fork of the stack:
`p2kb-<slug>-{foundation,content,diagrams}.sty` + `p2kb-<slug>-*.lua`. The
torture instrument is the certified reference, but each manual carries *its own
copies*. Consequences, all observed:

1. **Drift is the default.** Streamer was forked early and is missing 6+
   certified standards. No one erred — forks drift unless re-synced by hand.
2. **Maintenance is O(standards × manuals).** Every fix must be hand-ported into
   N manuals. We lived the worst case porting the token-fit Lua.
3. **"Certified" is a lie at the file level.** We certify
   `p2kb-torture-tables.lua`; Streamer ships `p2kb-streamer-tables.lua` — a
   *different file* the instrument never tested. The entire drift class comes
   from this gap.

Standards are not freezing — we *added two* this session (LayoutBlock markers,
Formula/Syntax keep-together). So the O(N) port cost recurs forever. That math
is the case for unifying.

---

## 2. Method

- One Explore agent per live manual classified its stack against the certified
  torture standards (checklist A–L below) + its manual-specific surface.
- **Findings were re-verified directly** where agents disagreed. One material
  correction: the streamer agent reported fix #5 PRESENT; direct grep showed
  both iosp and streamer `tables.lua` are **Version 6.7, `get_max_token_length`
  absent, `\tiny` tier absent** → fix #5 is in **no** manual. Trust the matrix
  below, which reflects the verified state.

### Standards checklist (the certified platform standards)

| ID | Standard | Home |
|----|----------|------|
| A | Widow/orphan penalties = 10000 | foundation.sty |
| B | Chapter titlespacing (titlesec, `-38pt`) | foundation.sty |
| C | Part titlespacing | content.sty |
| D | `contmarkers` tcbset style **defined** | content.sty |
| E | `contmarkers` **applied** to code boxes | content.sty |
| F | LayoutBlock carries `contmarkers` | content.sty |
| G | Formula/Syntax **keep-together** (not breakable) | content.sty |
| H | Long-table → `longtblr` + `rowhead=1` | tables.lua |
| I | Wide-table token-fit allocator + `\tiny` tier + token-aware `is_instr_desc` col1 (fix #5) | tables.lua |
| J | Table continuation markers | tables.lua |
| K | Figure move-whole (`\needspace`) | figures.lua |
| L | Code-line budget `**Max code columns (K): N**` | creation-guide.md |

---

## 3. The variation matrix (6 live manuals + instrument)

`✓`=present/aligned · `✗`=missing · `~`=divergent · `n/a`=construct not used

| Std | torture (ref) | iosp | ALM (pasm2) | deSilva | debug-win | ssdbg | streamer |
|-----|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| A penalties | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| B chapter titlespacing | ✓ | ✓ | ✓ | ~ −50pt | ✓ | ✗ `\@makechapterhead` | ✓ |
| C part titlespacing | ✓ | ✓ | ✓ | ~ | ~ `\@part` | ✓ | ✓ |
| D contmarkers defined | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| E contmarkers applied | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| F LayoutBlock markers | ✓ | ✗ (has block) | n/a | n/a | n/a | n/a | ✗ (has block) |
| G Formula/Syntax keep-together | ✓ | ✗ breakable | n/a | n/a | n/a | n/a | ✗ breakable |
| H longtblr+rowhead | ✓ | ✓ | ~ longtable, no rowhead | n/a | n/a | n/a (pandoc) | ✓ |
| I fix #5 token-fit | ✓ | ✗ | ✗ | n/a | n/a | n/a | ✗ |
| J table cont. markers | ✓ | ✓ | ✓ | n/a | n/a | n/a | ✓ |
| K figure move-whole | ✓ | ✓ | ~ truncated, no needspace | n/a (no filter) | n/a (no filter) | n/a (no figs) | ✓ |
| L code budget K | ✓ =76 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

**Universal gaps (every manual missing): A, D, E, L** — and fix #5 (I) is in no
manual. These are unambiguous platform material.

### Stack shape

| Manual | templates | filters | Notes |
|--------|-----------|---------|-------|
| torture (ref) | 3 sty + latex | 5 (code-coloring, tables, figures, mnemonic-bold, pagination) | the certified set |
| **iosp** | 3 sty + latex | 5 (same) | the ancestor/twin — closest to platform |
| **streamer** | 3 sty + latex | 5 (same) | twin of iosp |
| ALM (pasm2) | 3 sty (content 780, **diagrams 2012**) + latex | **7** (+entry-headers, +entry-format) | reference apparatus: entry types, encoding tables |
| deSilva | 3 sty + latex | **6** (NO tables, NO figures; +div-blocks, +semantic-blocks, +semantic) | pedagogical; code routed via `:::spin2` divs, not the code-coloring filter |
| debug-window | **2 sty** (NO diagrams) | 5 but different (code-coloring **29 ln**, +div-blocks, +semantic, +non-floating-images ×2 dup) | discovery boxes; no tables/figures/mnemonic/pagination |
| ssdbg | 4 (generic `p2kb-foundation` 378 + `ssdbg-foundation` 380 + content **40**) | **1** (code-coloring 30) | minimal; pagination baked in foundation; `\@makechapterhead` not titlesec |

---

## 4. Style families (the real structure)

The six manuals are not one population — they cluster into families, and the
platform must serve the families, not assume uniformity:

1. **Full technical "twins" — iosp, streamer.** Closest to the certified
   platform; just missing the recent standards. **Lowest-risk migration →
   Streamer is the pilot.**
2. **Reference (specialized) — ALM.** Full code family *plus* a large bespoke
   apparatus: entry-type headers, 9-column encoding tables, 2 extra filters, a
   2012-line diagrams.sty. Heavy local override surface.
3. **Tutorial — deSilva.** Pedagogical boxes (Your Turn, Sidetrack, Medicine
   Cabinet, Interlude, Chapter End, …) with their own colors + `:::`-div
   routing + sidetrack-TOC extraction. The **stress-test of the override layer.**
4. **Discovery — debug-window.** Debug-window semantic boxes (Discovery,
   Experiment, Performance, per-window-type blocks). Simplified code path.
5. **Minimal technical — ssdbg.** Two code boxes, one filter, baked pagination,
   non-titlesec headings.
6. **Presentation / prose (OUTSIDE the hierarchy) — AI guide.** See §5.

**Key existing-asset finding:** a **generic `p2kb-foundation.sty` (378 lines)**
already exists and is shared by **ssdbg and the AI guide**. An embryonic shared
base is already in the tree — the platform foundation should build on / replace
it rather than inventing a new one.

---

## 5. The AI-guide pattern (separate, non-hierarchy family — for future docs)

The AI guide (`workspace/ai-privacy-guide/`) deliberately does **not** use the
P2-technical style hierarchy. We document its pattern so future prose/guide-style
publications have a template to follow:

- **request:** `format_type: document_generation` (not the manuals' template path).
  Two documents (AI Privacy Guide, AI Implementation Strategy) in one request.
- **template:** `p2kb-presentation.latex` (194 lines) + the generic
  `p2kb-foundation.sty` (378 lines).
- **filters:** **none.** `pandoc_args` = `--pdf-engine=xelatex --toc
  --toc-depth=2`. No code-box family, no tables/figures filters, no mnemonic
  bolding.
- **docs:** carries its own `TEMPLATE-THEORY-OF-OPERATIONS.md` and
  `templates/README.md`.

**Pattern name (proposed):** *Presentation/prose family* — `p2kb-presentation`
template + generic foundation + TOC + prose, no technical apparatus. Suitable
for strategy/overview/policy/guide documents that are not P2 code references.
It should share the **same generic foundation** as the technical platform (so
geometry/penalties/hyperref are consistent) but bring its own presentation
template and no filters. Track it as a first-class family in the platform, not a
one-off.

---

## 6. Proposed architecture

**Shared platform + thin per-manual override; parameterize Lua, don't fork it.**

The platform has **two pillars**: the *mechanism* (penalties, contmarkers,
tables, figures — below) **and** the *vocabulary* — a shared **semantic block
catalog** so manuals select block/callout types instead of reinventing them. The
catalog is its own registry: `presentation-block-catalog.md`. Many things first
filed as "per-manual local" turn out to be re-skins of shared catalog types,
which *shrinks* the true local tail (see that doc's §4–§5). The catalog also
carries two LOCKED standards (its §7–§8): the **block taxonomy** (6 decisions)
and the **Figures & Tables standard** — all visuals are numbered figures, tables
numbered + captioned, bold "**Figure N**/**Table N**" labels, auto LoF/LoT,
`\ref`-able, plus the screenshot keyline (default-on thin gray border). Adopted
as the standard going forward, subject to evolution.

```
platform/                              (deployed once; every manual consumes)
  p2kb-platform-foundation.sty         geometry, penalties(A), titlespacing(B/C), hyperref
  p2kb-platform-content.sty            code-box family + contmarkers(D/E/F) + keep-together(G)
                                       + iosp-* color palette
  p2kb-platform-tables.lua             longtblr+rowhead(H) + fix #5(I) + cont-markers(J)
  p2kb-platform-figures.lua            figure move-whole(K)
  p2kb-platform-code-coloring.lua      shared code coloring  (bug-free: see gate G1)
  p2kb-platform-mnemonic-bold.lua      mnemonic uppercasing  (bug-free: see gate G1)
  p2kb-platform-pagination.lua

per manual:
  p2kb-<slug>-local.sty                \input AFTER platform; manual colors/macros/boxes
  p2kb-<slug>-<semantic>.lua           manual-unique :::div → manual-unique box routers
  <slug>-reference.latex (cover) + request.json   (already per-manual)
  p2kb-<slug>-diagrams.sty             manual TikZ content macros (content, not layout)

presentation family (AI-guide style):
  p2kb-presentation.latex + p2kb-platform-foundation.sty, no filters

instrument:
  torture ALSO consumes the platform  → certification finally tests the shipped bytes
```

The elegant payoff: if **both the instrument and the manuals include the same
platform files**, certifying on the instrument certifies the exact files every
manual ships. The drift class disappears *by construction*, not by discipline.

### Common / specific boundary

| Goes to PLATFORM (shared) | Stays LOCAL (per-manual override) |
|---------------------------|-----------------------------------|
| Page geometry, penalties, titlesec titlespacing, hyperref | Cover/`reference.latex`, `request.json` |
| Standard code-box family (Spin2/IOSP/CORDIC/MultiCOG/Antipattern) + contmarkers | Manual-rebranded colors (if any) via `-local.sty` override |
| LayoutBlock, FormulaBlock/SyntaxBlock (keep-together) | Manual-unique environments: deSilva pedagogical boxes, debug-window discovery boxes, ALM entry/encoding apparatus |
| `iosp-*` color palette (shared today) | Manual-unique `:::`-div → box routing filters |
| tables / figures / mnemonic-bold / pagination / code-coloring filters | `diagrams.sty` TikZ **content** macros (figures are content, not layout) |
| Code-line budget K=76 mechanism | The per-manual K value line in its creation-guide |

**Forge filename-keying implication:** shared platform filenames mean one
platform deploy updates the file for *all* manuals — a feature (fix once,
everywhere) *iff* the files are truly identical. Discipline required: nothing may
silently depend on a divergent copy. The Forge "two stores" rule (manual store
vs interactive store) is unchanged.

---

## 7. Migration plan (phased; verify each)

**Platform-readiness gates (clear BEFORE any manual adopts a shared filter):**

- **G1 — blank-line bug.** ssdbg deliberately avoids `mnemonic-bold` because
  sibling filters "drop blank lines." The platform code-coloring/mnemonic
  filters must be proven bug-free (blank lines preserved) before manuals adopt
  them. Verify on the instrument.
- **G2 — deSilva code-div regression (RESOLVED path, validated 2026-06-06).**
  deSilva authors code as `:::` divs, but this is an **accidental regression**,
  not a legit pattern: the 2025-12-06 backport (commit `e34d7ee`) flipped it from
  fenced to divs. Evidence: pre-backport backup = **0 div / 86 fenced**; live
  master = **211 div / 20 fenced**. Every other manual is fenced with **zero
  code-divs** — deSilva is the sole exception. **FIX (do in deSilva's migration
  step):** revert the ~211 code-divs to fenced (202 `:::pasm2`, 5 `:::spin2`, 8
  `:::antipattern`, 1 `:::multicog`); normalize the 20 fenced stragglers; back up
  the 6537-line master first; render-verify. This lets deSilva adopt the shared
  code-coloring filter cleanly and makes `desilva-div-blocks.lua` (the code
  router) vestigial — keep only `semantic-blocks.lua` for the legitimate
  pedagogical divs (your-turn/sidetrack). Also fix the 2 non-hyphenated semantic
  divs that don't map under the active filter. **Net: G2 is no longer a blocker,
  it's a cleanup.**

**Order:**

1. **Promote** the certified torture stack → `p2kb-platform-*` (the common core
   from §6), parameterizing the Lua. Make the instrument consume it; re-certify
   (re-run the torture round-trip green).
2. **Pilot: Streamer** (a twin — lowest risk). Replace its fork with
   `\input{p2kb-platform-content}` + a thin `p2kb-streamer-local.sty`; point
   `request.json` at platform filters; keep `streamer-diagrams.sty`. Plus the
   content-side work that is the same either way: **fix the 18 overlong code
   lines + seed K=76.**
3. **Verify the pilot = "concrete evidence":** Streamer render is **page-for-page
   identical-or-better** than its current production PDF, and it consumes the
   *same* platform files the instrument certified.
4. **Roll the rest, one at a time, family by family**, verifying each:
   iosp (twin, easy) → ALM (heavy local apparatus) → debug-window → ssdbg
   (foundation mechanism differs) → deSilva (the stress-test, last). The AI guide
   is documented as its own family (§5) but is **not migrated in this pass**.

### Success criteria (definition of "done correctly")

- The instrument and each migrated manual include the **same** platform files.
- A future standard change edits **one** platform file and every manual inherits
  it on next build.
- Each manual's render is regression-checked page-for-page against its last
  production PDF: identical, or improved by the newly-inherited standards.

---

## 8. Open decisions / risks

- **Lua override ergonomics.** LaTeX `\input` overrides cleanly; Lua does not.
  Resolution: shared filters do universal work; manual-unique semantic routing
  stays as small per-manual filters that emit platform box names. Confirm this
  holds for ALM's entry/encoding filters.
- **Color palette.** `iosp-*` colors are shared today; confirm no manual silently
  depends on a tweaked value before centralizing.
- **ssdbg foundation mechanism.** Uses `\@makechapterhead`/`\@part`, not
  titlesec. Migrating means switching it to the platform titlesec path — verify
  its pagination (baked in foundation) survives.
- **Migration touches 6 live publications.** Mitigate by phasing + per-manual
  render verification + the instrument as standing regression harness. Never
  big-bang.
- **Don't over-abstract.** If only one manual needs a thing, it stays in its
  `-local`, never the platform.
```
