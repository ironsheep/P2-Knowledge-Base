# Manual Production — Live Working Set (layout-effort scope view)

**Established:** 2026-06-04 (from generated-PDF listing + user confirmation)
**Roster of record:** `../PUBLICATION-ROSTER.md` — that file is authoritative for live/dormant
status. This doc is the **layout-effort scope view**: it layers the foundation-tier analysis on
top of the canonical roster. If the two ever disagree on membership, PUBLICATION-ROSTER.md wins.

**Purpose:** Show which live documents are in scope for the layout-standards effort and how they
relate architecturally (foundation tiers). Layout work targets the live set.

## Live working set

Six P2 manuals (confirmed by their generated PDFs) plus the AI privacy guide:

| # | Document (PDF) | Workspace | slug | Foundation tier | Notes |
|---|----------------|-----------|------|-----------------|-------|
| 1 | P2-Assembly-Language-Manual.pdf | p2-assembly-language-manual | pasm2 | Tier-1 twin (98.9%) | richest table machinery |
| 2 | P2-Debug-Window-Manual.pdf | p2-debug-window-manual | debugwin | Tier-1 twin (98.9%) | minimal filters (code-coloring only) |
| 3 | P2-IO-and-Smart-Pins-User-Guide.pdf | p2-io-and-smart-pins-user-guide | iosp | Tier-1 twin (98.9%) | the live-publication standard others rebase on |
| 4 | P2-PASM-deSilva-Style.pdf | p2-pasm-desilva-style | desilva | Tier-2 light fork (78.6%) | pedagogical styling diverged |
| 5 | P2-Single-Step-Debugger-Manual.pdf | p2-single-step-debugger-manual | ssdbg | Tier-2 moderate fork (60.4%) | larger 336-ln foundation, 40% unique |
| 6 | P2-Streamer-Programming-Guide.pdf | p2-streamer-programming-guide | streamer | Tier-1 twin (98.9%) | reference Lua byte-identical to iosp |
| 7 | (ai-privacy-guide) | ai-privacy-guide | — | uses pristine `p2kb-foundation.sty` | **live**, presentation-class; outside the manual table/figure layout problem set |

### Generated-PDF sizes/dates at capture (2026-06-04)
```
1927896  May 23 17:52  P2-Assembly-Language-Manual.pdf
 782874  Jun  3 23:15  P2-Debug-Window-Manual.pdf
1201545  May 31 02:48  P2-IO-and-Smart-Pins-User-Guide.pdf
 724276  May 23 17:36  P2-PASM-deSilva-Style.pdf
 547041  May 31 17:05  P2-Single-Step-Debugger-Manual.pdf
 471232  Jun  4 00:03  P2-Streamer-Programming-Guide.pdf
```
(ai-privacy-guide PDF not in this listing; confirmed live separately by the user.)

## Dormant (NOT live — out of scope for the layout effort)

| Workspace | Why dormant |
|-----------|-------------|
| ~~p2-smart-pins-tutorial~~ | **Retired and archived 2026-08-16** — superseded by the I/O & Smart Pins User Guide; moved out of the live tree to the gitignored local `archive/` together with its bespoke `p2kb-sp-` fork. No longer dormant-but-revivable: out of scope permanently unless deliberately revived from git history. |
| spin2-reference-manual | Placeholder/planning stage; foundation copy only, no source manual. |

## Scope implications for the layout-standards effort

- **Layout work targets the 6 live manuals.** ai-privacy-guide is live but presentation-class
  and not part of the table/figure layout problems; it rides the pristine shared foundation, so
  it benefits automatically from any shared-foundation improvement.
- **Tier-1 twins (pasm2, debugwin, iosp, streamer)** differ only by 3–4 comment lines — a
  foundation fix lands in all four verbatim.
- **The two forks needing genuine porting are desilva (light) and ssdbg (moderate).**
- **Part-flow feature (B4) caveat:** the only part-based doc (smart-pins) is dormant, and every
  live doc builds with `--top-level-division=chapter`. Before building B4 we must determine how
  the live docs introduce `\part` (the user reports they do have parts). See the survey's open
  question.

## Generation-cost ordering (binding constraint for the layout effort)

PDF generation is a human-in-loop Forge round-trip, so **per-PDF generation time is the binding
constraint** on how fast we can iterate layout fixes — more than table-richness or page count.

- **Assembly Language Reference ≈ 25 minutes per PDF generation** (largest manual ~22.5k md
  lines + the heaviest `diagrams.sty`, 64.8 KB of TikZ). Confirmed by the user 2026-06-04.
- Generation time is driven mostly by **TikZ diagram compilation** + total length. Relative
  `diagrams.sty` weight: assembly 64.8 KB ≫ iosp 27.6 KB > streamer 12.0 KB ≈ desilva 13.5 KB;
  ssdbg/debug-window have little/no diagrams. PDF output sizes (proxy for length): streamer
  471 KB < ssdbg 547 KB < desilva 724 KB < debug-window 783 KB < iosp 1.20 MB < assembly 1.93 MB.

**Rule for this effort: work fastest-generating first, slowest last.** Prove rules on a small,
fast Tier-1 doc; propagate to the twins (verbatim, near-free); regenerate the slow Assembly
manual **last and ideally once**, after the rules are already proven elsewhere.

**Pilot (revised):** **Streamer Programming Guide** — fastest to generate (smallest output,
light diagrams), a **Tier-1 twin** (foundation/table/pagination fixes port verbatim to iosp,
assembly, debug-window), exercises the full layout machinery (tables, figures, pagination,
**parts** → can prove B4), and already has a deferred visual-review pass pending. Assembly,
despite the richest tables, is the **last** doc to touch because of the 25-min cost.

## Folder-state map — `manuals/` subfolders (surveyed 2026-06-04)

Every top-level subfolder under `engineering/document-production/manuals/` and its state. All
seven contain a real manual master (none is an empty skeleton); the only "started but empty" case
is a *workspace* with no `manuals/` source at all.

| `manuals/` subfolder | State | Manual master (evidence) | Source structure |
|----------------------|-------|--------------------------|------------------|
| p2-assembly-language-manual | LIVE | ~22,490 md lines | `opus-master/part-i, part-ii, part-iii/` |
| p2-debug-window-manual | LIVE | per-chapter (`ch04-bitmap`…`ch06-logic`) | `opus-master/` chapter files |
| p2-io-and-smart-pins-user-guide | LIVE | ~14,757 md lines | `opus-master/part-1 … part-5/` |
| p2-pasm-desilva-style | LIVE | `COMPLETE-OPUS-MASTER.md` (6,537 ln) | single-file master |
| p2-single-step-debugger-manual | LIVE | `P2-Single-Step-Debugger-Manual.md` (700 ln) | single-file master |
| p2-streamer-programming-guide | LIVE | `streamer-body.md` (1,589 ln) | single-file master |
| ~~p2-smart-pins-tutorial~~ | **ARCHIVED 2026-08-16** | — | moved out of the live tree; recoverable from git history |

### Workspaces with NO `manuals/` source folder

| Workspace | State | Detail |
|-----------|-------|--------|
| spin2-reference-manual | **STARTED — NO MANUAL YET** | Skeleton only: workspace has a `p2kb-foundation.sty` copy + README, **no `request.json`, no source**. The one genuine empty-start. (Dormant.) |
| ai-privacy-guide | LIVE (non-manual pattern) | Build + input markdown live in the *workspace*, not under `manuals/`. Presentation-class; rides the pristine shared foundation. |

## Part-introduction mechanism (resolves the B4 gating question)

**How live docs make `\part`:** parts and chapters are *both* level-1 `#` headings in the
assembled markdown, distinguished only by title text (`# Part I: …` vs `# Chapter 1: …`). With
`--top-level-division=chapter`, pandoc would make every `#` a `\chapter`; a **pagination Lua
filter** intercepts headers whose title matches `^Part ` and re-emits them as
`\manualpart{...}` (a `RawBlock`). `\manualpart` (defined in each doc's `*-content.sty`):
`\clearpage` → fixed `\vspace*{0.9in}` → centered `\Huge` title → fixed `\vspace{0.9in}` →
`\nobreak`, and sets an `aftermanualpart` flag. The `\chapter` command is patched (etoolbox) so
its built-in `\clearpage` becomes conditional — when the flag is set, the **first chapter skips
its page break and stays on the part's page** (implements preferences A2/A3).

**Coverage — only 3 live docs use parts:**

| Doc | Uses parts? | Part-detect filter | `\manualpart` def |
|-----|-------------|--------------------|-------------------|
| assembly (pasm2) | **yes** | `p2kb-pasm2-pagination.lua` | `p2kb-pasm2-content.sty` |
| io-smart-pins (iosp) | **yes** | `p2kb-iosp-pagination.lua` | `p2kb-iosp-content.sty` |
| streamer | **yes** | `p2kb-streamer-pagination.lua` | `p2kb-streamer-content.sty` |
| pasm-desilva | no | — | — |
| debug-window | no | — | — |
| single-step-debugger | no | — | — |

The three part-using docs are Tier-1 twins, and their pagination filters are near-identical
(iosp/streamer 100%, pasm2 90.5%), so a part-flow change is essentially one edit across three.

**Why B4 (part *intro* → chapter) broke:** `\manualpart` hardcodes two fixed `0.9in` vspace bands
around the title and assumes **only** the title occupies that whitespace before the chapter
follows. There is no slot for intro paragraphs. When intro text was added after `# Part I:`, the
fixed-vspace centering didn't account for the variable-height intro block, so the following
chapter heading was positioned on top of / colliding with the intro paragraph — exactly the
overlap reported. **Fix path:** redesign `\manualpart` to lay out as a natural vertical flow
(part title → optional intro block → first chapter heading) with proper inter-element spacing and
keep-together, replacing the hardcoded vspace bands — a `*-content.sty` change in the three
part-using docs.

## Roster change recorded 2026-06-04

`PUBLICATION-ROSTER.md` previously listed **3 live** (iosp, pasm2, desilva — the
convention-reconciled reference set). On 2026-06-04 the live set expanded to **7**: the three
originals **plus** debug-window, single-step-debugger (ssdbg), streamer, and ai-privacy-guide.
Of those, **smart-pins-tutorial** has since been retired and archived (2026-08-16), leaving
**spin2-reference-manual** as the only dormant workspace. The four newly-promoted
publications are live but their cross-publication convention reconciliation is **pending** — that
reconciliation is part of this layout-standards effort. See PUBLICATION-ROSTER.md for the
authoritative table and the per-publication "reconciled?" status.
