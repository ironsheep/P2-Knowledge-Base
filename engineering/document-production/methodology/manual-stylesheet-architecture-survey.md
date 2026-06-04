# Manual Stylesheet Architecture — Deterministic Survey

**Status:** Survey/map (decision input for the layout-standards effort)
**Companions:** `manual-layout-standards-INPUTS.md`, `manual-layout-standards-USER-PREFERENCES.md`
**Reproduce:** `python3 manual-stylesheet-compare.py` → `manual-stylesheet-comparison-RAW.md`

> **Membership correction (2026-06-04):** the live working set is **assembly, debug-window,
> io-smart-pins, pasm-desilva, single-step-debugger (ssdbg), streamer** — plus **ai-privacy-guide**
> (live, but presentation-class; uses the pristine shared `p2kb-foundation.sty` directly, no
> content/diagram/filter stack — not part of the manual layout problem set). **Smart-pins-tutorial
> and spin2-reference-manual are DORMANT.** An earlier draft of this survey wrongly included
> smart-pins (the heavy part-based fork) and omitted ssdbg; the numbers below are the corrected set.
> Roster of record: `manual-production-working-set.md`.

## Method (deterministic, reproducible)

For every template/filter file **actually used** by each of the 6 live manuals (as declared
in each `request.json` + the `\usepackage` lines of each main `.latex`), we measured the
fraction of its **non-blank lines** that appear **identically** in another document's file.
Two passes:
- **RAW** — literal line match.
- **NORM** — after replacing each document's slug (`pasm2`/`sp`/`desilva`/`iosp`/`streamer`/
  `debugwin`) with a placeholder, so a renamed-but-otherwise-identical line counts as shared.

This neutralizes rename noise and exposes *real* structural divergence. Numbers below are
machine-generated, not estimated.

---

## Headline finding — it is NOT "six independent stylesheets"

The six manuals are **one platform that was physically copied and lightly forked**, not six
independent designs. There are three tiers:

| Tier | Documents | Foundation shared (NORM) | Character |
|------|-----------|--------------------------|-----------|
| **1 — Twin platform** | assembly (pasm2), debug-window (debugwin), io-smart-pins (iosp), streamer | **98.9%** | Effectively the *same* foundation + same reference Lua filters |
| **2 — Light fork** | pasm-desilva | **78.6%** | Pedagogical styling diverged; foundation still mostly shared |
| **2 — Moderate fork** | single-step-debugger (ssdbg) | **60.4%** | Larger foundation (336 ln, 39.6% unique); minimal content + one filter |
| **(separate)** | ai-privacy-guide | uses pristine `p2kb-foundation.sty` | Live, presentation-class; outside the manual layout set |

The four Tier-1 foundations are **literally the same file** apart from **3–4 comment/metadata
lines each** (the `% Based on:` provenance line, the `\ProvidesPackage` name, and an
`\RequirePackage{amssymb}` that two of them added). Of ~279 lines, **257 are identical across
all four.** The provenance comments even document the lineage explicitly:
`pasm2 → iosp → {streamer, debugwin}`, each "rebased on the live-publication standard for
visual consistency." A manual "rebase onto the live standard" practice is already happening —
just by hand.

**Implication for the layout effort:** a foundation-level fix (widow/orphan penalties,
part-intro→chapter flow, keep-together rules) is **one edit that drops into 4 documents
verbatim**, a near-clean port into desilva, and a careful merge into smart-pins. This is the
opposite of "fix it six times."

---

## Per-document used-file inventory + commonality

Full table in `manual-stylesheet-comparison-RAW.md`. Salient rows:

### Foundations (where the page-layout logic lives)

| doc | foundation lines | same-role NORM% | % in all-6 core | % unique |
|-----|-----:|-----:|-----:|-----:|
| assembly (pasm2) | 278 | 98.9 | 52.2 | 1.1 |
| debug-window | 279 | 98.9 | 52.0 | 1.1 |
| io-smart-pins (iosp) | 279 | 98.9 | 52.0 | 1.1 |
| streamer | 279 | 98.9 | 52.0 | 1.1 |
| pasm-desilva | 281 | 78.6 | 49.5 | 21.4 |
| single-step-debugger (ssdbg) | 336 | 60.4 | 42.6 | 39.6 |

(The "% in all-6 core" is lower than "same-role NORM%" because the all-6 core is dragged down
by the two forks; the 4 twins share 98.9% *with each other*.)

### Table-handling Lua (your C8/C9 defects live here)

| doc | table filter | lines | same-role NORM% |
|-----|------|-----:|-----:|
| io-smart-pins | `p2kb-iosp-tables.lua` | 893 | 99.9 |
| streamer | `p2kb-streamer-tables.lua` | 893 | 99.9 |
| assembly | `p2kb-pasm2-tables.lua` | 783 | 98.9 |
| smart-pins | `p2kb-sp-table-autowidth.lua` | 19 | 21.1 |
| *(debug-window, desilva: no table filter used)* | — | — | — |

- iosp and streamer table filters differ by only **32 lines out of 893** (~96% identical).
- All three reference table filters share **439 identical lines**; pasm2 is the more-diverged
  one but still 98.9% common.
- **There is effectively ONE table-handling implementation** across the three reference docs —
  so the table-split standard (C9) and width-overflow fix (C8) are also largely a single edit.
- Smart-pins uses a tiny 19-line auto-width shim instead; debug-window and desilva use none.

### Other shared Lua

- **mnemonic-bold**: ~613–621 lines, **~100% identical** across pasm2/iosp/streamer/sp.
- **code-coloring**: ~99% shared across pasm2/iosp/streamer/desilva (sp lighter at 60%).
- **figures**: 100% identical across iosp/streamer (151 lines); pasm2 98.5%.
- **pagination** (Lua): iosp/streamer 100% identical; pasm2 90.5%; desilva a lighter 51.6%.
- **Genuinely unique** (no sharing): sp's `frontmatter`, `structure`, `index-toc`,
  `fix-title-as-part`, `fix-hypertarget`; pasm2's `entry-format`, `entry-headers`;
  sp `numbering.sty`. These are document-genre-specific and *should* be unique.

### Content & diagrams (expected to diverge — and they do)

`content.sty` ranges 39–90% shared; `diagrams.sty` 9–67%. This divergence is **intentional and
fine** — different visual identity and different TikZ figures per document. The layout effort
should **not** try to converge these.

---

## What this means for the layout-standards plan

1. **The "consolidate vs. port 6×" decision is now easy on the merits.** The layout-critical
   layer (foundation + reference table/pagination/figure Lua) is *already* a de-facto shared
   platform — it's just copied, not linked. Converging *only that layer* into a real shared
   include would capture 4 documents at ~99% with near-zero loss, leave desilva a thin override,
   and leave smart-pins as the one genuine special case. Content/diagram styling stays per-doc.

2. **A pilot fix propagates cheaply.** Whatever we prove on one Tier-1 document ports verbatim
   to the other three Tier-1 docs, with desilva and smart-pins as the two that need attention.

3. **The two forks are the real work.** desilva (light, 21% unique) and ssdbg (moderate, 40%
   unique, 336-line foundation) are where any layout rule needs genuine porting/merging rather
   than copy-paste. The heavy part-based fork (smart-pins) is now **out of scope (dormant)**.

   **RESOLVED (2026-06-04) — how live docs make parts:** parts and chapters are both level-1 `#`
   headings, distinguished by title text. A **pagination Lua filter** rewrites headers matching
   `^Part ` into `\manualpart{}` (RawBlock); `\manualpart` (in each doc's `*-content.sty`) renders
   the part page and sets a flag that makes the patched `\chapter` skip its page break so the first
   chapter stays on the part page (A2/A3). **Only 3 live docs use parts: assembly, io-smart-pins,
   streamer** (all Tier-1 twins, near-identical pagination filters). desilva/debug-window/ssdbg
   have no part mechanism. **Why B4 broke:** `\manualpart` hardcodes fixed `0.9in` vspace bands
   that assume only the title sits before the chapter — no slot for intro text — so added intro
   paragraphs collided with the following chapter heading. Fix = redesign `\manualpart` as a
   natural vertical flow in the 3 part-using `*-content.sty` files. Full detail in
   `manual-production-working-set.md`.

4. **Open decision (unchanged, but now well-grounded):** do we (a) formally consolidate the
   shared layer into one included file all six pull from, or (b) keep self-contained copies and
   adopt a disciplined "rebase onto the live standard" sync step? The data favors (a) for the
   layout layer specifically; (b) is the status quo and already happening by hand.
