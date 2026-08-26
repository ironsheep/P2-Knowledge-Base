# Bring the YAML set to release position — sprint plan

**Opened:** 2026-08-26 · **Head:** yaml (P2KB) · **Dispatch:** inline (no Agent tool this session)

## The ask, in Stephen's words

> *"Get as close as possible to release shape for every facet you can work on without me."*
> *"Don't defer anything to my attention unless it really needs my attention."*

He is away. This sprint does everything that is settled by **a source we hold**, **a standing
rule he has already given**, or **a measurement I can take** — and stops only where his
reasoning is genuinely the input.

## Where we actually are (measured 2026-08-26, not asserted)

| | |
|---|---|
| YAML files changed since `v1.17.0` | **72** (the ledger says 61 — it predates 5 files) |
| Commits touching KB YAML since `v1.17.0` | **16** (the ledger says 11) |
| Ingestion findings applied to YAML | **0 of 8** — `ingest-source` forbids YAML edits by design |
| Ledger's pre-ship checklist | **1 of 12 fixed**, 11 live |
| Differential read of the changed files | **never done** — no artifact exists |
| Ledger currency | **stale**: zero mentions of F-362…F-371, E-012…E-016, G-021, G-026 |

## Scoping test applied to every item

**Does this need Stephen's *reasoning*, or merely a decision I can derive?** Most "decisions"
turned out to be derivable, and the plan below says how for each. The test failed for exactly
one class, listed at the end.

## Work

### A — Apply the ingestion findings to the shipped YAML

| # | Finding | Why it is determinable |
|---|---|---|
| A1 | **F-363** PA/PB "CALLD-imm parameter" → "return, CALLPA parameter" | triple-sourced, cell-identical across silicon-doc, Hardware Manual, Datasheet |
| A2 | **F-368** `getbrk.yaml` restore the Z branch; reconcile `flags_affected` | the source states it; the file contradicts itself |
| A3 | **F-369** carry the smart-pin DIR-reset behaviour | sourced at `silicon-doc-text.txt:3360` |
| A4 | **F-366** write the package/mechanical record | dimensions read twice off the drawing, transcribed in the re-test record |
| A5 | **F-370** TAQOZ entry — **re-scoped per Stephen 2026-08-26** | **existence · access · utility only.** NOT the ROM-vs-RELOADED quality comparison |
| A6 | **F-365** re-anchor 23 citations to `silicon-doc-text.txt` | verify each against the new artifact; do not translate line numbers |
| A7 | **E-016 sibling sweep** — ADDSX/SUBS/SUBSX/SUM* C-flag prose | same defect class; check our KB against the sources |

### B — Repair the 11 live ledger items

B1 `getct.yaml` has no `description:` · B2 `digital_io_board` named twice in the file that
corrected it · B3 E-010 *"enable a pin pull-up"* in both Edge Module files · B4 EF-063/EF-064
mis-attribution, 10 occurrences · B5 `edge-breadboard-carrier` power figure (guide says 5 VDC,
5.5 V max) · B6 `addon-serial-host` identity string · B7 duplicate `educational_value:` (keep
the structured block, drop the stray scalar) · B8 `total_symbols_extracted: 1224` vs the real
record count · B9 `hub75_adapter` citations into loose ingestion-root files · B10 **F-360**'s
remaining duplicate-key sites · B11 ledger item 6, below.

### C — Re-derive rather than defer

| # | Item | Approach |
|---|---|---|
| C1 | **F-359** six un-purged files with fabricated provenance headers | the finding's own third option is *"re-derive those six from the real sources"*. silicon-doc is now fully extracted, so re-derivation is far more likely to succeed than when it was filed. **Only what genuinely fails re-derivation becomes a purge question.** |
| C2 | **F-364** 13 dangling `yaml_file:` pointers | **not** a write-files-vs-inline preference: the content is already complete inline, so 11 thin files would put one fact in two homes — the defect class this project keeps finding. Remove the aspirational pointers; note in the finding that the index holds everything needed if per-register files are ever wanted. |
| C3 | **F-341** invented part numbers #64025/#64026/#64027 | Stephen confirmed they are invented, and his standing rule is *"no fabricated names in the KB tree — delete invalid names outright."* Disposition already given. |

### D — Measure rather than defer

**D1 — ledger item 6, the 30 shape changes across 24 files.** Recorded as *"a judgement, not a
correction… the change most likely to break something downstream."* **It is measurable.** Test
the actual consumers — `generate-p2kb-index.py`, the fetch script, `validate-crossref-keys.py`,
`validate-dod-release.py`, and the p2kb-mcp fetch contract — against the changed shapes. If
nothing breaks, there is no decision to make. If something breaks, that is a defect to fix, not
a preference to poll.

### E — The differential read Stephen chose, and never got

**E1.** Read each of the **72** changed files for *what was removed and whether we gutted it*,
with a verdict per file: **stronger · equal · thinner-but-honest · gutted**. Anything landing
on *gutted* is a restoration task, not a note.

### F — Instrument repair

**F1 — F-362.** `audit-register-hygiene.py` reports CLEAN on `KNOWLEDGE-GAPS.md` while reading
none of its entries; a planted duplicate ID passes at exit 0. Deferred at the release boundary
because widening a module-global status vocabulary is regression surface. **There is no release
imminent now**, and the fix is provable before/after with the tool's own negative-control suite.

### G — Remove the trap without deciding anything irreversible

**G1 — F-367.** `external-inputs/p2/` is an unlabelled second copy of the corpus whose
silicon-doc DOCX **disagrees with the canonical one on the GETBRK Z flag**. Add a README
labelling it staging-only, naming the canonical `sources/` copy for each file, and recording
which silicon-doc copy is authoritative and why. Labelling is not deletion; the reconcile-or-
retire choice stays open.

### H — Close out

**H1** regenerate the ledger **from scratch** against `v1.17.0..HEAD` — it is a derived document,
and re-deriving after the repairs produces exactly what was asked for (only the current
differences) where hand-patching would preserve the drift. **H2** regenerate index + `.gz`
together, run every gate, leave the tree at release position.

## Definition of done

- Every item in A–H complete, or explicitly listed as failing the scoping test with the reason.
- All gates green: `verify-yaml-format` · `validate-crossref-keys` · `audit-yaml-claim-sourcing`
  · `audit-constant-fidelity` · `audit-extraction-digit-density --all` · `audit-register-hygiene`
  ×3 · `validate-dod-release`.
- Ledger re-derived and current.
- **A concise list of what needs Stephen**, ready to iterate on when he returns.

## What is genuinely deferred

**One class, and it is his by ownership, not by difficulty:**

1. **The release act** — version number, `git tag`, `push`, `release-yamls`. Standing instruction:
   *"Do not automatically release."*
2. **Any block that fails C1's re-derivation** and would therefore need deleting — content loss
   is his call. Expected to be small; possibly empty.

Everything else in this plan is settled by a source, a standing rule, or a measurement.

## Entry baseline (measured 2026-08-26)

All gates exit 0. `digit-density --all` CLEAN at 65 artifacts. `validate-dod-release` 12 checks
green. Registers: F-372 / G-027 / Q-010 / E-017 next.

## Currency check (plan-to-tasks overlay §1, run 2026-08-26)

1. **Plan span / head** — 123 lines, authored 2026-08-26, head `yaml`. New document; nothing above
   the entry point.
2. **Sections superseded** — none. Compared against: the 2026-08-25 change ledger (**stale**, and
   that staleness is §H1's subject), the corrections register, and a live run of all eight gates.
3. **Register state, findings in scope** — F-341 `PARTIAL` (:2437) · F-359 `CONFIRMED` (:539) ·
   F-360 `CONFIRMED` (:489) · F-362 `CONFIRMED` (:359) · F-363 `CONFIRMED` (:285) ·
   F-364 `CONFIRMED` (:324) · F-365 `CONFIRMED` (:250) · F-366 `CONFIRMED` (:210) ·
   F-367 `CONFIRMED` (:139) · F-368 `CONFIRMED` (:173) · F-369 `CONFIRMED` (:194) ·
   F-370 `CONFIRMED` (:98) · F-371 `RESOLVED` (:53). Errata: E-010 (:284), E-016 (:319).
4. **Blocking standing rules** — (a) *"Do not automatically release"*: §H stops at a prepared tree.
   (b) *"No fabricated names in the KB tree — delete invalid names outright"*: this is what makes
   §C3 determinable rather than deferred. (c) *"Don't defer anything to my attention unless it
   really needs my attention"* (2026-08-26): applied as the scoping test throughout.
   **No contradiction found; no sprint stop.**

## Dispatch shape

`inline` — no Agent tool in this session, so the arbiter runs each task itself and the
fresh-context benefit is **not** obtained (`dispatch-contract` §6). Disclosed, not implied.

## Ordering note (§3a rework pass)

Two orderings are correctness constraints, not preferences:

- **§E1 (differential read) precedes §E2 (restore the gutted).** §E2's fix-list is *discovered* by
  §E1 and cannot be sized before it runs — the project overlay's instrument-first rule, and this
  project has had hand counts come in wrong four times.
- **§H runs last.** It certifies the tree every other task changed; any edit afterwards decertifies
  it. This is also why the ledger is re-derived rather than patched.

## Section ↔ task cross-reference

| Plan § | Deliverable | Task | seq |
|---|---|---|---|
| §A1–A3, A5 | Apply F-363 · F-368 · F-369 · F-370 (re-scoped) | «#319» | 1 |
| §A4, A6 | Package record (F-366) + re-anchor 23 citations (F-365) | «#320» | 2 |
| §B1–B4 | Ledger items 1–5: the red items + EF-063/064 | «#321» | 3 |
| §B5–B10 | Ledger items 7–11 + F-360 duplicate keys | «#322» | 4 |
| §C1–C3 | Re-derive: F-359 · F-364 · F-341 | «#323» | 5 |
| §D1 | Measure the shape-change question | «#324» | 6 |
| §E1 | Differential read, 72 files | «#325» | 7 |
| §E2 | Restore everything marked `gutted` | «#326» | 8 |
| §F1 | Fix F-362, the register-hygiene blind spot | «#327» | 9 |
| §G1 + §A7 | Label external-inputs + E-016 sibling sweep | «#328» | 10 |
| §H1–H3 | Re-derive the ledger; index+gz; hand-back list | «#329» | 11 |
