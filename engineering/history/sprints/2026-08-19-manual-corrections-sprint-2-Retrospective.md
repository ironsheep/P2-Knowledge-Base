# Manual Corrections — Sprint 2 — Retrospective

**Sprint:** «#218»–«#239», tag `manual-corrections-2` · **Closed:** 2026-08-19
**Closeout (what shipped):** `2026-08-19-manual-corrections-sprint-2-CLOSEOUT.md`

This captures *what was learned*. Seven manuals and two KB releases shipping is in the closeout.

---

## 1. The best thing that happened was a task refusing to execute

`«#219»` said: correct the IOSP guide's "groups of four" to eight. It also said — because Sprint 2
made this standing — *ground it against the domain authority first*. Grounding returned the
**opposite** of what the task instructed, and the task was **stopped rather than executed**.

That produced F-269, the reversal of F-211, and the two-layer power-domain model the KB now
carries. Had the task simply been done as written, a correct manual would have been "corrected"
into a wrong one, and the KB's existing error would have been reinforced by a second source.

**Feed forward:** a task instruction is not authority. Any task whose body asserts a domain fact
should carry the ground-it-first clause explicitly, and "the grounding disagrees with the task" must
be a recognised, expected outcome — not an anomaly the executing agent has to invent a response to.

## 2. A class-wide sweep amplifies whatever fact it starts with

F-211 wrote the P2 Edge **board's** 8-pin LDO grouping into the **chip's** KB file, then swept it
class-wide. One wrong premise became many wrong sites, each of which then looked like corroboration.

**Two rules out of it.** Grounding must be **stronger before a sweep than before a single-site fix**
— the blast radius multiplies the error. And **a board document can never establish a silicon fact**;
the layers must be named separately or the next challenge flips them back.

The remediation is the reusable shape: fixed as an **enrichment** (`silicon_power_grouping` /
`board_power_grouping`, both named, with the reconciliation stated), not as a revert. Restoring "4"
alone would have left the KB one breakout-header challenge away from flipping to 8 again.

## 3. Name coverage is not semantic coverage

`manual_category_alignment_check.yaml` certified the conditional-execution category *"PERFECT —
Complete match"* while calling `_RET_` a suffix. It had compared the **list of condition names** —
complete — and never their **semantics**. Downstream, `_RET_ CALL` reached community review as
advice that can never work.

**Feed forward:** a check must state what it compared. A checker that compares names and reports a
category verdict is worse than no checker, because it manufactures confidence.

## 4. Publishing the KB *before* the manuals that cite it

Sprint 2 deliberately ran the YAML pass first («#218» → v1.16.3) so Streamer §17.1 and Assembly
ch.5 derived from a **published** KB rather than being authored in parallel with it.

This is the standing fix for the **F-211/F-245 recurrence** — a correction lands in the YAML and
never reaches the manuals — which had happened **twice** before this sprint. Adopt it as the default
ordering for any sprint touching both layers.

## 5. The process gap that cost the most: the closeout never ran

Sprint 2's work finished 2026-08-19. Its closeout ran **after the next sprint had already started
and shipped**. Because central `sprint-closeout` §7 is what invokes `punch-list-maintenance` — and
closeout calls itself that skill's "defined cadence" — skipping closeout silently skipped the
register sweep. **34 closed findings** accumulated in a 3,559-line register that declares it carries
open work only.

The damage is not untidiness. **Agents miss things in long lists**, so every later read of that
register was degraded, and the `document-audit` drain gate that depends on knowing what is pending
was not armed.

**Adopted:** a `sprint-closeout` project overlay stating a sprint is not closed until *every*
archivable doc is swept and `audit-register-hygiene.py` exits 0. **Still owed:** something that makes
starting sprint N+1 while sprint N is unclosed visible at the moment it happens — the overlay fixes
the procedure, not the ordering.

## 6. Status notation, and the trap of a confident wrong status

The register recorded completion in **four incompatible notations**, and was wrong in *both*
directions: findings marked nothing that were done, and one marked `RELEASED` that had not shipped.
`MANUAL HALF APPLIED` was the worst — it reads "half done" and means *the manual half of a two-half
fix is applied*, i.e. that half is complete.

The measurement has since moved from *18 unmarked of 37* to *2 of 43*, and detection is now
mechanical. But the deeper lesson held all the way into this closeout's own archive sweep: a first
pass classified on **prose** and would have archived **16 findings with work still owed**, because
their headlines read "source fixed" while their status said `CONFIRMED` and their bodies said
"render owed".

**The rule, now enforced:** the status token is authoritative; prose is never a status; `PARTIAL`
vetoes an embedded `DONE`; and a prose/status mismatch is its own finding needing a deliberate
decision, never a licence to sweep.

## 7. What worked and should be kept

- **The opus-master commit gate.** `«#234»` handed Stephen the diff and waited. Prose stayed
  uncommitted until release, and the wave audit caught two live findings before anything shipped.
- **Shortest-first wave ordering.** Seven elements, smallest first, so failures surface on a 15-page
  app note rather than a 502-page manual.
- **An app-note correction is not complete until its YAML companion carries it** (F-270 — P2AN001
  v1.0.2 fixed the document five weeks before its companion; two halves of one released deliverable
  contradicted each other). The companion ships under the same version and is half the deliverable.
