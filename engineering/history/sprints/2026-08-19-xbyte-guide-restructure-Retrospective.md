# XBYTE Guide Restructure — Retrospective

**Sprint:** «#251»–«#265», tag `xbyte-restructure` · **Closed:** 2026-08-19
**Closeout (what shipped):** `2026-08-19-xbyte-guide-restructure-CLOSEOUT.md`

---

## 1. A cleanup task is the wrong shape when the defect is a generator

`«#252»` said: remove four hand-named render backups from the workspace. It did. By closeout there
were **nine**, every one created during the sprint's own render cycles — and the true scope was **90
files across 17 documents**.

The generator was `latex-escape-all.sh`, backing up its input on every run, for a script that writes
a separate output and never modifies its input. The backup protected against nothing and broke both
halves of the project's backup convention.

**Feed forward:** when a plan section is written as "remove these N artifacts," the planning question
is *what created them, and will it create more before this sprint ends?* If that has no answer, the
task is scoped to the symptom. **A hygiene task that deletes artifacts without naming what creates
them buys one day.**

## 2. Naming a red as expected, in the task text, is what stopped it being "fixed"

The sprint had two atomic green-units — «#253»→«#255» and «#263»→«#265». Each renumbers chapters, so
the cross-reference checker goes **red at the first task's completion by construction**, and the
second restores it.

This worked *because all four tasks said so in their own text*. The plan's own cut note spelled out
why: without it, "an executing agent finishes the cut, sees red, correctly concludes it broke
something, and either burns time proving the red was expected or undoes its own correct work."

**Keep this.** Any multi-task unit that leaves a gate red mid-way must say so **in every task in the
unit**, not only in the plan.

## 3. §7.4 was internally inconsistent twice, and neither time was it factually wrong

F-296 and F-298 both landed on the same section, and neither was a fact error: §7.4 cited real
evidence and then **generalised past it**. F-298 is the sharper case — the text described a
*prologue* two paragraphs after citing a worked emulator that puts the same work in the *tail*.

**Feed forward:** a worked example and the generalisation drawn from it must be checked **against
each other**, not only each against the source. Both can be individually true and jointly
contradictory, and no source-grounding pass will catch it.

Corollary that showed up in the same finding: **the book had the answer in Chapter 17 and stated its
opposite in Chapter 7.** Cross-chapter self-consistency is its own audit dimension.

## 4. Adopting community feedback in substance rather than verbatim

TonyB_'s rename proposal was adopted through the **subtitle and a new Part III**, with the title left
alone — leading a title with the least familiar term costs more than it buys. The cover still
retitled to "P2 Interpreters & Emulators Guide", so the substance landed.

Worth keeping as a pattern: reviewer proposals are evidence about a *problem*, and the fix does not
have to be the reviewer's proposed *solution*. Say which was adopted and why, so the reviewer can see
their finding was taken seriously.

## 5. The plan inherited a stale task, and stated it confidently

The plan's "Not in this sprint, deliberately" note excluded the fancyvrb `breaklines` work as a
scheduling decision. That work had been **rejected outright the day before the plan was cut**. The
exclusion was right; its stated reason was two days out of date, and the plan said it with the same
confidence as everything else around it.

**Feed forward:** when a plan cites another task as context, read that task's **finding**, not the
task. The task is a dated snapshot. (Same root shape as F-301 and the «#250» sweep.)

## 6. The sprint started while the previous sprint was still open

This sprint was cut, executed and released while manual-corrections Sprint 2 sat unclosed — and
Sprint 2's own release wave was still running concurrently (its Streamer element shipped *after*
XBYTE did). Nothing about either sprint's work suffered, but **Sprint 2's closeout was skipped**, and
with it the register sweep that closeout owns.

**Adopted:** a `sprint-closeout` project overlay stating a sprint is not closed until every
archivable doc is swept and `audit-register-hygiene.py` exits 0.

**Still owed, and it is the real gap:** nothing makes *starting* sprint N+1 while sprint N is
unclosed visible at the moment it happens. `sprint-start` is where that check belongs — an entry
condition, not a closeout condition. The overlay fixes the procedure; it does not fix the ordering.
