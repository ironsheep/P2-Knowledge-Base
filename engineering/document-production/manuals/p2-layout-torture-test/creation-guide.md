# P2 Layout Torture Test — Creation Guide & Case Index

**Purpose:** This is *not* a real manual. It is an engineering harness for the manual
layout-standards effort — a small, fast-to-generate document built on the live document
stack, engineered so every known layout defect reproduces. Fixes are developed and proven
here, then ported to the live manuals.

**Stack origin:** cloned from the **Streamer Programming Guide** (a Tier-1 "twin" foundation),
slug-renamed `streamer → torture`. Because the live twins (assembly, io-smart-pins,
debug-window, streamer) share ~99% of this foundation and byte-identical reference filters,
a layout fix proven here ports to them verbatim. See
`engineering/document-production/methodology/manual-stylesheet-architecture-survey.md`.

**Authority for what "correct" means:** `methodology/manual-layout-standards-USER-PREFERENCES.md`
(the A/B/C lists). Defect codes below refer to it.

## How to use

1. Stage to outbound (escape + copy) and generate on PDF Forge — it is small, so it is fast.
2. Open the PDF and locate each case below by its heading.
3. Record pass/fail per case against its defect code.
4. Develop the rule change (foundation / content.sty / table filter / pagination filter),
   regenerate, re-check. Iterate here — never on the live manuals.
5. When all cases pass, port the proven changes to the live stack.

## Case index (v0.2 — comprehensive coverage)

| Case (heading in the doc) | Defect | What to verify |
|---------------------------|--------|----------------|
| Part I intro → "Chapter 1" | **B4** | Part intro paragraphs flow, and the Chapter 1 heading follows them WITHOUT overlapping. Root cause: chapter `\titlespacing` top space is **−38pt**, pulling the title up into the intro. |
| §1.1 "A Heading That Wants to Orphan" | **C5** | Heading not stranded alone at a page bottom; ≥1–2 body lines share its page. (No `\clubpenalty`/`\widowpenalty` today.) |
| §1.2 heading+intro+diagram+caption | **C7** | The four-element block stays together; caption never separates from its figure. (figures filter forces `[H]`.) |
| §1.3 heading immediately before code | keep-with | Heading must not strand above a code block that jumps to the next page. |
| §1.4 / §1.4.1 / §1.4.1.1 deep nesting | nested orphan | Subsection/subsubsection headings hold to following text. |
| §1.5 long wrapping heading | wrap | Two-line heading keeps consistent spacing and binds to its paragraph. |
| §2.1 long listing spanning a page | **C10** | Spanning code box must signpost the break like a continued table: footer "continues" marker + header "continued" marker, box border/background intact. No code-spanning standard today. |
| §2.2 over-long code lines | code overflow | Long code lines wrap/clip — must not run past the box's right edge. |
| §2.3 short listing at page foot | code orphan | Code block not stranded at a page bottom. |
| §3.1 long nested list | list split | List splits sensibly; no single item stranded. |
| §3.2 block quote | quote | Block quote renders/splits cleanly. |
| §3.3 boxed formula | boxed split | `formula` box does not split awkwardly at a boundary. |
| Chapter 4 long prose | **C5** | No single widow/orphan line stranded at a page boundary. |
| Part II intro → "Chapter 5" | **B4** | Confirms the part-intro fix works for *every* part. |
| §5.1 long table (60+ rows) | **C9** | Splits across pages with header row repeated + clear continuation marker. (No standard yet.) |
| §5.2 table after heading | keep-with | Heading must not strand above its table. |
| §5.3 table with caption | caption | Table caption stays with its table. |
| §6.1 wide 10-column table | **C8** | Columns must NOT overlap. Root cause: falls to pandoc-default narrow `p{}` columns. |
| §6.2 long unbreakable tokens | **C8 cause** | Long underscore tokens (no break points) must not overrun their narrow column. |
| §6.3 tall pin table | **C6** | Oversized table places gracefully without large awkward gaps. |
| §7.1 tall diagram | figure overflow | `[H]` diagram must not overflow bottom margin / leave a huge gap. |
| §7.2 long caption | caption bind | Multi-line caption stays bound to its figure. |
| §7.3 two figures in a row | float competition | Back-to-back `[H]` figures must not collide or overflow. |
| Part III intro → "Chapter 8" | **B4 / A2** | Third part-intro flow; first chapter shares the Part's page. |
| §8.1 long callout spanning a page | **C11** | Spanning callout must signpost the break (footer/header markers, intact styling) — same standard as C10/C9. Open policy: allow long callouts vs keep short. |
| §8.2 short callout at page foot | **C11** (keep-short) | A short callout must move whole to the next page, never split. |
| Chapter 9 fresh-page assertion | **A3** | Normal chapters start on a fresh page (contrast A2's part-share exception). |
| §9.1 keep-together tail blank | **A1 vs C5/C7** | Forced unit moves whole, leaving a tail blank; the blank must stay WITHIN the whitespace tolerance (the central knob). |

## Known self-inflicted issue history
- **v0.1 → v0.2:** the top-of-file block comment contained a nested `<!-- TORTURE … -->`, which
  closed the Markdown comment early and leaked text into the document body (seen in the generated
  `.tex`). Fixed by removing nested comment markers; per-case annotations are now single comments
  with no nested `<!--`/`-->`. Lesson: never nest HTML comments in pandoc Markdown.

## Constraints respected by the design

- **Automation principle:** every fix must be a general rule (foundation/filter level), not a
  per-element manual nudge. The torture cases are written in plain house-style markdown so a
  general rule is what makes them pass.
- **A1 (minimize blank areas) vs C5/C7 (keep-together):** the doc deliberately puts these in
  tension so we can tune the whitespace-tolerance threshold centrally.

## Code Line Budget

Code boxes do **not** wrap — a typeset wrap can't break a comment and re-indent it,
nor add a language line-continuation, so over-long code lines are an authorship
defect to fix in source, not a template concern. The budget below is the widest code
line the box prints; the `prepare-manual` line-length audit
(`engineering/tools/validation/audit-code-line-length.py`) flags any source code
line wider than it.

- **Max code columns (K): 76**
- **Code-box style / font:** `IOSPBlock` (the shared `::: pasm/iosp` / ```` ```pasm2 ````
  colored box), Latin Modern Mono at the box's code size, with the `numbers=left`
  gutter present. This is the **platform reference K** — the live manuals fork this
  same code-box style, so they inherit this number unless a manual diverges its code
  font (then it re-measures its own K).
- **Calibrated:** case 2.2's column ruler, render **v22** (2026-06-06). The box frame
  falls at the col-76/78 boundary (col-76 marker prints inside the frame, col-78
  outside; pitch ≈ 5.75 pt/col). Lines near K sit close to the right border; target a
  few columns under K for breathing room.
- **Re-measure when** the code font size or box geometry changes: re-render case 2.2,
  read the largest ruler marker still inside the box, update this number.
- **Remediation (authorship rule):** keep every code line ≤ K. If a line is too long,
  break the comment onto a new comment line and re-indent it, or split the statement
  using the language's line continuation and re-indent — never let the typesetter wrap.

## Maintenance

- Canonical source: `manuals/p2-layout-torture-test/opus-master/P2-Layout-Torture-Test.md`.
- Build input: `workspace/p2-layout-torture-test/P2-Layout-Torture-Test.md` (refreshed from
  opus-master, LaTeX-escaped, then staged to `outbound/`).
- Add new torture cases here and in the markdown (mark with `<!-- TORTURE: Cn ... -->`).
