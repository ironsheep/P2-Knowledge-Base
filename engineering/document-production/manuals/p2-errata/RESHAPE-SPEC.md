# P2 Errata — v0.3.0 Reshape Specification

**Status:** governing for v0.3.0 (task «#361»). Decided with Stephen, 2026-10-03, after Chip
Gracey's review of the v0.2.0 build (`REF-NO-COMMIT/designer-notes.md`, not committed). Once
v0.3.0 ships, `creation-guide.md` and `voice-guide.md` carry these rules permanently; this file
records the decisions and the reasoning behind them.

## 1. Why

The v0.2.0 build was 74 pages. In its seven erratum chapters (about 29,000 words), test
walkthroughs and proof took 45%, workarounds and the limits of each proof 20%, and the
description of the defect 22%. All seven used the same eight-section template, so the two
Goertzel errata got as much space as the counter erratum, and every erratum read like a case
being argued. Chip's verdict: accurate, but out of proportion. *"It needs to all be spelled
out, but contextualized and made brief enough to read."* Of the seven, the stale upper `CT` in
cogs 4-7 is the one programmers will actually meet.

The reader is an **experienced programmer working with a P2**. They open an errata for one of
three reasons: at the start of a project (*what must I watch for?*), while chasing a symptom
(*is this a known bug?*), or in code review (*does this code hit any of them?*). The book is
reshaped around those three questions. It is no longer a record of how each erratum was proven.

## 2. Decisions

| # | Decision |
|---|---|
| D1 | **Three parts.** (1) *Errata Quick Reference*: who meets which erratum, grouped by how likely they are to meet it, and the symptom lookup. (2) One entry per erratum: about a page, up to two for E3. (3) *Appendix A*, the evidence: one row per erratum. |
| D2 | **An errata sheet is a second PDF built from the same sources**: the quick reference plus each erratum's summary box, 2-3 pages. Same version as the guide, built in the same Forge request. No separate roster row or CHANGELOG. |
| D3 | **One source for shared text.** Each erratum's summary box, the triage table and the symptom table are each written once, in `shared-*.md`, and included in both documents by the assembler. Shared text is never typed twice. |
| D4 | **No "why" yet, and no placeholder.** Chip's design reasons enter when his amendment to the P2 Documentation publishes them. Each entry reads complete without them, nothing refers forward, and the insertion point is fixed (§4). The addition is tracked as a task, not mentioned in the text. |
| D5 | **The programmer's model stays; the design account goes.** Where a rule needs a model of behaviour to make sense (E3: each group of four keeps its own copy of the upper long, refreshed only at a wrap while one of its cogs runs), the entry states that model, which is measured. The clean-room study's account of the mechanism (the old *Why it happens*) is removed from reader text. |
| D6 | **Evidence leaves the body.** Proof walkthroughs and test-program walkthroughs are removed from the entries. Appendix A gives each erratum's test programs, what they measured, the result and the date. The full detail stays where it already lives: the examples archive (every program prints its raw values) and the hardware-verification ledger. |
| D7 | **Version 0.3.0**, still a community review draft. v0.2.0 was never released, but its PDF is the one Chip and the designer reviewed, so the number is not reused. 1.0.0 is the first build Chip has read and approved. |
| D8 | **Fixed:** erratum numbers E1-E7 (permanent); chapter order is numeric; chapter heading form `# Erratum EN: Title {#ch-eN}`; only official Parallax P2 documentation is cited for what the part is meant to do; *a proven workaround*, never *the fix*; every printed workaround is byte-identical to a block that ran on silicon. |

**Correction recorded during drafting:** the plan said Appendix A would carry the ledger number
for each erratum. That would break `creation-guide.md` §5: no internal identifiers (`EF-NNN`)
appear in reader text, and provenance stays in the repo. Appendix A names test programs and
results. The ledger numbers stay in the verification sidecars.

## 3. The likelihood grouping (the triage)

| Group | Errata | Why it is in this group |
|---|---|---|
| **Any multi-cog program that runs past 21 s** | E3 | `GETMS()`, `GETSEC()` and DEBUG timestamps in a cog of 4-7 that the program starts late. Ordinary code meets it. |
| **Code that streams from hub with a no-wait `RDFAST`** | E7 | Rare in practice: code normally does enough work after a no-wait `RDFAST`. One rule covers it. |
| **Hand-written PASM2 that does something unusual** | E1, E2 | An instruction between `SETQ` and its transfer, or an immediate-`S` `ALTx` between `AUGS` and its target. A `##` operand on a block transfer that uses a `PTRx` expression produces E1's arrangement without the programmer writing an `AUGS`: the assembler places one between the `SETQ` and the transfer (checked with `pnut-ts` 1.55.8: `setq #3` / `rdlong buf, ptra++[##100]` assembles to `SETQ`, `AUGS`, `RDLONG`). |
| **Specialist features** | E4, E5 (Goertzel), E6 (DAC-mode ADC) | Only programs using those features. Each workaround is one routine or one bit. |

## 4. The erratum entry

```
# Erratum EN: <title> {#ch-eN}

<!-- include: shared-eN.md -->         the summary box (shared with the sheet)

[WHY INSERTION POINT — empty in v0.3.0: Chip's design reason, one short paragraph]

## What happens {#sec-eN-actual}
   what the P2 Documentation says (owner + a short exact quote), what the part does instead,
   the programmer's model where a rule needs one, and what is NOT affected

## A proven workaround {#sec-eN-workaround}
   rule first; the arrangement to avoid (beside the workaround) where code shows it best;
   the proven block; its kind (one-time startup / rule at each use / helper routine);
   cost; other ways in a sentence or two; the limits of the proof in a sentence or two

**Found by** … · **Published by Parallax** … · confirmed on P2 hardware (date).
   One closing line. It credits whoever found the erratum (designer request).
```

- **The summary box** (`shared-eN.md`) is a `::: caution` box with three lines:
  **Who meets it:** · **What you see:** · **What to do:**. Programmer terms only, with no
  documentation quotes. It is the whole erratum for a reader who stops there, and it is
  exactly what the sheet prints.
- **Proportion is part of the text.** Each entry says how likely the erratum is, in plain words,
  so that a rare one does not read as something to hunt for. Consequences are stated in one
  or two lines, never catalogued.
- **Code fences are verbatim excerpts of archive programs** (the `corpus-identity` gate enforces
  this). An arrangement to avoid is printed from the test program's own hazard arm when that
  is short and readable; otherwise it is written as an inline instruction sequence in prose.
- **Removed:** *What the P2 is documented to do* (folded into *What happens*), *What your program
  sees* (folded into the box and *What happens*), *Why it happens*, *How it was proven on P2
  hardware*, *The test program*, and the Status table (replaced by the closing line plus
  Appendix A).

## 5. Front matter and quick reference

- **Front matter:** cover; `# Copyright and License`; `# Preface` (what this guide is and who
  it is for; how an entry is built, in three lines; erratum vs. anti-pattern in two sentences
  pointing to *P2 Anti-Patterns*; sources; acknowledgments; the review-draft note and
  permanent numbering). The template table, the full classification essay and the long
  acknowledgments are removed.
- **`# Errata Quick Reference`** (an existing chapter pattern in the pagination filter): the
  triage (`shared-triage.md`) and the symptom table (`shared-symptoms.md`).

## 6. Appendix A — How Each Erratum Was Confirmed

One table, a row per erratum: test program(s), what it measured, the result, the date. Then how
to build and run the programs (pins, run times, the reset requirement), cut to the essentials.
The anchor `{#app-a}` is kept.

## 7. Build

- **Assembler** (`workspace/p2-errata/assemble-manual.sh`) builds two files. `P2-Errata.md` is
  the front matter, the quick reference, E1-E7 and Appendix A. `P2-Errata-Sheet.md` is
  `sheet.md` with its includes expanded. A line that is exactly `<!-- include: <file> -->` is
  replaced by that opus-master file's content. A missing file stops the build, and so does an
  include left unexpanded in the output.
- **`request.json`** has two `documents`. The sheet has its own title block on page 1 (title,
  version, build date: a demo PDF identifies itself), no banner and no TOC, and
  `--top-level-division=section` so its erratum headings do not start new pages.
- **Gates:** `validate-manual-release.py` reads only `documents[0]` for its workspace-level
  gates. The sheet would ship ungated, so the runner is extended to run those gates on every
  document in the request (additive: every other manual has one document).

## 8. Out of scope for v0.3.0

- **The "why" lines:** wait for Chip's P2 Documentation amendment (D4). Tracked as a task.
- **Test programs:** unchanged. The reshape changes what the book prints, not what ran.
- **The KB:** unchanged by this reshape.
