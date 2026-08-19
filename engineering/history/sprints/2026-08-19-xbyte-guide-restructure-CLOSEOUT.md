# XBYTE Guide Restructure — CLOSEOUT

**Closed:** 2026-08-19 · **Plan:** `XBYTE-GUIDE-RESTRUCTURE-SPRINT-PLAN.md` (archived alongside)
**Tag:** `xbyte-restructure` · **Tasks:** «#251»–«#265» (14 at cut, grew to 15 on 2026-08-18)

---

## 1. Plan audit — the section↔task table, reconciled

The plan's cross-reference table reconciles cleanly in both directions: every seq row maps to a real
plan section, and every numbered section §1–§12 has a row. No stale rows.

| seq | § | Deliverable | Task | Status | Evidence |
|---|---|---|---|---|---|
| 1 | §7a | Governing docs — PLANNING.md LOCKED + creation-guide §2 | «#251» | **SHIPPED** | guide layer PASS |
| 2 | §12 | Workspace hygiene — remove four hand-named render backups | «#252» | **REGRESSED** | see §4 |
| 3 | §1 | **The cut** — chapter permutation + Part boundaries | «#253» | **SHIPPED** | 7 Parts in master |
| 4 | §2 | Part intros, chapter openers, transitions | «#254» | **SHIPPED** | v1.1.0 |
| 5 | §3 | Cross-ref sweep, flipped-direction adjudication, Index rebuild | «#255» | **SHIPPED** | Index p114 |
| 6 | §11 | **The middle rung** — new Ch.15 + renumber 15–20 → 16–21 | «#263» | **SHIPPED** | `# Chapter 15: Growing the VM {#ch-15}` |
| 7 | §11b | Re-sweep — cross-references green after the insert | «#265» | **SHIPPED** | 21 chapters, refs resolve |
| 8 | §4 | Navigation layer — intent index, brief opener, reading paths | «#256» | **SHIPPED** | intent index in `front-matter.md` |
| 9 | §5 | Apparatus rebalance — boxes into text, code into decision chapters | «#257» | **SHIPPED** | v1.1.0 |
| 10 | §6 | Diagrams — dispatch ladder, three decisions, two kinds of prefix | «#258» | **SHIPPED** | 3 new figures, 7 total |
| 11 | §7b | Trailing guide-layer currency — voice-guide, MANUAL-DESCRIPTOR | «#259» | **SHIPPED** | conformance PASS |
| 12 | §8 | Front matter, cover title, `request.json` | «#260» | **SHIPPED** | cover reads *"P2 Interpreters & Emulators Guide"* |
| 13 | §9 | Documentation blast radius — the four artifacts no task owns | «#261» | **SHIPPED** | — |
| 14 | §10a | Draft render + page-level review | «#262» | **SHIPPED** | daemon renders |
| 15 | §10b | Audit, render, **release v1.1.0** | «#264» | **SHIPPED** | tag `p2-xbyte-programming-guide-v1.1.0` |

**14 of 15 SHIPPED. One REGRESSED — «#252», and its root cause is now fixed (§4).**

**The two atomic green-units behaved as designed.** «#253»→«#255» and «#263»→«#265» each renumber
chapters, leaving the cross-reference checker red at the first task's completion *by construction*;
the second restored it both times. Neither red was treated as a regression.

## 2. What shipped

**XBYTE Programming Guide v1.1.0** — released 2026-08-19, **114pp** (from 101pp at v1.0.1), retitled
on the cover to **"P2 Interpreters & Emulators Guide"**.

7 Parts · 21 Chapters · 4 Appendices · 154 outline entries · 7 figures (3 new) · intent index +
reading paths · a 3-file example ZIP, byte-identical to `examples-library/` and compile-clean out of
the archive.

Four findings authored and released in this sprint — **F-295** (external memory reframed as a
subsystem; the decay-prone "32 MB" ceiling and vendor names removed), **F-296** (§7.4 relocates
per-instruction work rather than forbidding it), **F-297** (the column-map notation for shared
handler bodies), **F-298** (placement is a before/after-the-work timing decision, not a prologue).

**All four were verified on the shipped PDF at this closeout and flipped `CONFIRMED` → `DONE`**, then
archived. F-298 was verified by *reading* the pages rather than grepping: "prologue" still appears on
p41 and p114, which is **correct** — the reframing keeps it as one named placement among several, and
the Index now lists *"a family's shared tail · an optional prologue"* as alternatives. The defect was
prologue-as-the-only-placement, and that is gone.

## 3. Exit baseline — a manual sprint's baseline is the document's audit state

| Gate | Entry (2026-08-18, `plan:55-61`) | Exit (2026-08-19) |
|---|---|---|
| Published baseline | v1.0.1, 101pp | **v1.1.0, 114pp**, tagged |
| Guide layer (`audit-guide-conformance.py`) | PASS across 45 files | **PASS across 45 files** |
| Cross-references | 387 resolvable, 0 dangling | resolvable, 0 dangling (re-swept by «#265») |
| Code-line budget K=76 | clean | **clean** (exit 0) |
| Non-ASCII in code blocks | clean | **clean** |

Not worsened on any gate. The +13pp is new material (Ch.15, three figures, navigation layer), not
drift; the release was render-verified with **zero pages differing** from an independent daemon
render.

## 4. The one regression — and why deleting the files again would have been the wrong fix

**«#252» removed four hand-named render backups from the workspace. By closeout there were nine** —
created 2026-08-18 20:32 through 2026-08-19 01:33, i.e. **during the sprint's own render cycles**.

Root cause: **`engineering/tools/conversion/latex-escape-all.sh:14`** ran
`cp "$INPUT" "$INPUT.backup.$(date +%Y%m%d_%H%M%S)"` on **every invocation**. The script reads
`$INPUT` and writes a separate `$OUTPUT` — **it never modifies its input** — so the backup protected
against nothing, while violating both halves of `engineering/standards/BACKUP-CONVENTION.md`: never
hand-name a backup, and never back up a regenerable artifact (the workspace render is rebuilt from
`opus-master` by `assemble-manual.sh` — the generator *is* the backup). A second defect rode along:
the "Backup created:" message called `date` again, so it could name a file that did not exist.

**Scope was 90 files across 17 documents**, not four across one. Fixed at the source and the litter
removed; the escaper re-tested and confirmed to produce correct output and leave nothing behind.

**The lesson:** «#252» was written as a cleanup task when the defect was a generator. A hygiene task
that deletes artifacts without naming what creates them buys one day.

## 5. Carryover

- **«#250» — RETIRED, not carried.** The fancyvrb `breaklines` fix this plan deliberately excluded
  was **rejected on 2026-08-17**, the day before this plan was cut; the plan's exclusion note was
  right about the outcome and stale about the reason. See F-281. There is no breaklines work.
- **Cross-ref filter — still ⏳ for this manual.** XBYTE was never in
  `CROSSREF-FILTER-ADOPTION.md`'s table and released twice without adopting (F-301). Now a column in
  `PLATFORM-FEATURE-ADOPTION.md`.
- **Metadata single-source — ⏳.** XBYTE's template still declares
  `\title{P2 XBYTE Programming Guide}`, the **pre-retitle** name, against a cover reading *"P2
  Interpreters & Emulators Guide"*. Adopt at its next release.
- **F-299** — two 6-column tables overhang 6.1pt/5.3pt. **Polish, inside the project's 20pt
  tolerance.** Do not re-render for it.
- **§C.1 URL margin overhang** — pre-existing and identical in v1.0.1; punch-listed for the platform
  inline-breaking work.

## 6. Verification statement

v1.1.0 was **render-verified on the delivered PDF**: 114pp, 154 outline entries, all 7 figures present
in body and List of Figures with vector content, no blank pages, compile log zero on every serious
signature including "Missing character", `.tex` sweep clean, and **zero pages differing from an
independently-verified daemon render**. Example ZIP rebuilt and checked byte-identical.

The exit gates in §3 were re-run at closeout on 2026-08-19 and are reproduced above.
