# P2 Architect's Guide — First-Draft Build · Retrospective

**Sprint:** `arch-guide-v0.1` (first-draft build) · **closed out** 2026-06-23.
**Closeout artifacts:** CHANGELOG v0.1.0 (manual head) + the sprint-plan "SPRINT COMPLETE" stamp + the
PUBLICATION-ROSTER row + the Platform Freshness Ledger PUBLISH line — there is no separate closeout doc;
in this manual head, closeout *is* the standing-doc sweep.
**Shipped:** a 4-chapter v0.1 first-draft manual (Meet the Propeller 2 · Reading P2 Code · Putting It to
Work · Thinking in P2) + back matter + 5 figures; clean production PDF (48 pp) on the Forge.
Commits `b1176567..e9ae30ef` on `main` (not pushed). All 7 sprint tasks (#93–#99) archived.

---

## Discovered perspectives
- **The plan under-specified the reader's prior knowledge.** "Newcomer to the P2" silently assumed a reader
  who can already read a structured language; the real audience includes people with **no P1, no Spin2, no
  PASM2** — they've never seen a `CON`/`PUB`/`DAT` block. That gap only surfaced when Stephen flagged it
  mid-sprint, and it cost a whole new chapter (Ch2 "Reading P2 Code").
- **Ingested editions can silently lose content.** Propeller Manual v1.0 carried a "Propeller Programming
  Tutorial" chapter (and a "Using the Propeller Tool" chapter) that v1.2 *removed* (moved to the Tool's
  on-line help). I trusted our ingested-v1.2 structure-map and wrongly asserted the tutorial "was never a
  chapter." A structure-map of **one** edition is not the document's history.
- **Sibling manuals already held the diagrams.** The 8-COG-around-the-hub and memory-hierarchy figures
  existed verbatim in the Assembly manual's diagram stack; reusing them (vs authoring new) saved real time
  and kept the family look identical.

## Process insights
- **The forge-test daemon round-trip earned its keep** — it caught three defects before production: a
  `\lstinline` crash on a Unicode ellipsis in inline code; a **silent table-row drop** (a 12-row table
  rendered as a non-breaking tabularray `tblr` and clipped its last two rows past the page bottom — including
  the anti-FPGA capstone row); and figure numbers rendering "0.N" because the guide uses unnumbered named
  chapters.
- **But one of those was statically catchable, and I ran the static gate too late.** `audit-inline-code-ascii.py`
  exists precisely to stop the ellipsis-class crash *without* a Forge cycle — yet I ran it (inside
  prepare-manual) only **after** the daemon round-trip. Running the cheap source gates *before* submitting to
  the daemon would have caught it for free. → operationalized (Methodology §1).
- **Writing a DoD + coverage-gate BEFORE authoring prevented shortchanging.** When Stephen asked "how do we
  prevent shortchanging this [new chapter]?", the move that worked: write the learning-objectives as a
  definition-of-done, then run a coverage gate (every Spin2/PASM2 construct used in *any* example across the
  guide is introduced). The gate caught a real gap — `@` (address-of) used before it was introduced.
- **Golden-source fidelity + the anti-prescription gate held** with no drift — Ch4 derived from the
  decomposition YAML, Ch2 from the Spin2 v55 doc; the robot-dog stayed labeled "one machine's answer."

## Quality & efficiency observations
- **Faster than planned:** chapter authoring (golden sources made it near-transcription, not invention);
  diagram reuse; the 7 original tasks each ran far under estimate.
- **Slower / wasted cycles:** ~3 daemon round-trips went to render-only defects (table drop, figure
  numbering) — genuinely only-visible-on-render, so unavoidable — but ~1 (the ellipsis) was avoidable with a
  pre-check. The figure pass + the unplanned Ch2 + the v1.0 cross-check roughly **doubled** the sprint's
  scope beyond the original DoD; the standing docs were stale at "closeout" until the dedicated sweep.

## Downstream impact
- **Enables:** the orientation layer above the reference manuals now exists (4 chapters); Ch2 fills the
  no-language-background gap; reusable architect diagram macros are in place; the "Using {toolchain}"
  chapter is scoped (PLANNING §15).
- **Destabilizes / flags (real):** the **platform tables filter routes a tall non-encoding table to a
  non-breaking `tblr` that silently drops overflow rows** — a *platform* defect that can bite any manual
  with a long explanatory (non-encoding) table. Worked around here by splitting the table; flagged for the
  layout-standards effort. The emoji-marker glyph drop is likewise guide-wide / platform-wide.
- **New source gap:** G-P1-007 — the v1.0/v1.01 "Propeller Programming Tutorial" is a recoverable P1-corpus
  source we don't have (Spin1/PASM1 → a pedagogy model for us, not P2 content).

## Methodology lessons
1. **[forge-test] Run the cheap static source-gates BEFORE the daemon round-trip.** — **ADOPTED** this
   retrospective in `.claude/skills/forge-test/project-overlay.md`. Before submitting a doc to the
   interactive daemon, run `audit-inline-code-ascii.py` + `audit-code-line-length.py` on the *opus-master*
   source; a `\lstinline`-fatal character or an over-budget code line fails the build only after a full
   round-trip, so the static check is free insurance. *certified: PENDING* (would have caught the test-v1
   ellipsis; certifies the first time it catches something on a real pre-daemon run).
2. **[sprint-plan] PROPOSAL — an audience-prior-knowledge planning step.** A plan question: *"what can the
   target reader NOT yet read or do?"* would have surfaced the missing language chapter at plan time instead
   of mid-sprint. Build-sized refinement to the planning skill; parked, not built.
3. **[ingest-source] Editions differ — verify a content/structure claim against the actual artifact, and
   treat any extraction/structure-map as one-edition-only.** Captured as a lesson; not a new gate (covered by
   the existing verify-against-primary-source discipline, now reinforced here). Closed-no-change as a buffer
   candidate.
4. **Diagram-reuse-before-author** and **DoD+coverage-gate-for-net-new-units** are genuine reusable patterns,
   noted here; not yet operationalized (no clean central-skill home — future doc-authoring-overlay material).

---

*Verdict: this sprint produced real process learning worth acting on — one rule adopted locally
(static-gates-before-daemon), one planning-gap PROPOSAL, and one confirmed platform defect to chase. Not a
clean no-delta execution.*
