# Ingestion backlog sprint — plan

**Opened:** 2026-08-26 · **Head:** ingestion · **Dispatch:** inline (no Agent tool this session)

## Why now

Five sources have their primary document on disk and were never fully ingested. One of
them — **silicon-doc** — is not merely incomplete: it is the **Tier-1 authority**, it sits at
**75%**, its DOCX re-extraction was **scheduled 2026-06-22 and never run**, and the DOCX carries
**48 tables that the PDF path recovered none of** (confirmed by structural survey 2026-08-26:
5,719 paragraphs, 48 `<w:tbl>`, 34 media, `comments.xml` present).

That last fact is the reason this sprint is not just backlog-clearing. **Every "no source states
it" verdict we reached during the YAML-fidelity sprint was drawn against a corpus missing those
48 tables.** Gaps G-019/G-020/G-021 and a number of uncited-block purge decisions rest on the
silence of a document we had only partially read. Re-extracting it is the *hole*; re-testing
those verdicts against it is the *filling*, and the second half is where the value is.

## Scope

### In — five ingestions, source on disk

| # | Source | Now | Primary | Note |
|---|---|---|---|---|
| 1 | **silicon-doc** | 75% | DOCX 4.8 MB | 48 tables, 34 media, reviewer comments. **Do first.** |
| 2 | pasm2-manual | 64% | PDF (draft 221117) | Parallax preliminary |
| 3 | smart-pins-titus | 90% | DOCX rev 5 | 27 reviewer comments already harvested once |
| 4 | edge-standard-module | 80% | PDF Rev D 3.0 | |
| 5 | TAQOZ Bit Bashers | 25% | DOCX | queued since 2026-06 |

### In — the hole-filling half

- **Re-test every source-silent verdict** against the completed silicon-doc extraction.
- **Register hygiene**: route new gaps/errata/conflicts; move ANSWERED rows.
- **Dashboard + quad reconciliation**, including the stale queue rows found 2026-08-26 (two
  entries still read "queued" for work that shipped 2026-06-27).

### Out

- Sources with **no primary document staged**: `iron-sheep-compiler`, `quick-bytes-code`,
  `p2docs-github-io`, `taqoz`, `rom-booter`, `flash-loader`, `p2-qa-spreadsheet`,
  `pnut-ts-pasm-ref`, and the queued P1 datasheet/manual. Several need an external fetch;
  **not done unattended.**
- Rows at 95–99% that are residual-gap percentages on already-re-ingested sources
  (p2-datasheet, p2-hardware-manual, the add-on wave) — re-running buys nothing.
- **No YAML edits.** `ingest-source` routes conflicts to the corrections register; the YAML
  head applies them. No release.

## Established decisions (cross-cutting — apply to every task)

1. **DOCX-primary** for content/code/images where a `.docx` exists; PDF ladder otherwise.
2. **The digit-density gate is mandatory** on every pass-1 artifact, and **exit 2 is not a
   pass** — it means nothing was measured. Record the number and the tool's caveat, never
   "gate passed".
3. **A mangled extraction and a silent source look identical.** Confirm against the rendered
   page before recording any fact as absent (F-250).
4. **Nested-in-cell tables must be walked** — a naive DOCX table walk drops them, and that is
   where the hardware manual's pin drive ladder was hiding.
5. **Harvest `word/comments.xml`** where present, pairing each comment to its anchor via the
   `commentRangeStart/End` ids.
6. **Errata vs gap vs correction** — the test is *"if Parallax fixed their document tomorrow,
   would this entry disappear?"* Yes → `SOURCE-ERRATA.md`. No → gap or corrections register.
7. **`KNOWLEDGE-GAPS.md` owns the `G-` and `Q-` allocators** (established 2026-08-26); read its
   declared counter, never hand-read a maximum.
8. **No commits inside a task.** Commit at the task boundary, green.

## Task set

| # | Task | Gate to pass |
|---|---|---|
| 1 | silicon-doc passes 1–3 (content/tables, code, images) | digit-density exit 0 + 48/48 tables + 34/34 media accounted |
| 2 | silicon-doc passes 4–5 (post-processing, validation audit) | section-by-section audit written |
| 3 | silicon-doc pass 6 (cross-source Q&A, comments harvest, conflicts/errata) | all three legs done, not just conflicts |
| 4 | **Re-test source-silent verdicts** against the new extraction | each prior verdict re-run and recorded confirmed/overturned |
| 5 | silicon-doc pass 7 (dashboard, authority, lineage, audit of record) | quad updated |
| 6 | pasm2-manual full ingestion | 7 passes |
| 7 | smart-pins-titus completion | 7 passes |
| 8 | edge-standard-module completion | 7 passes |
| 9 | TAQOZ Bit Bashers ingestion | 7 passes |
| 10 | Dashboard + quad reconciliation sweep; retire stale queue rows | dashboard self-consistent |

## Definition of done

- Five sources ingested; dashboard rows and gates reflect measured state, not stated.
- Prior source-silent verdicts re-tested and each recorded as confirmed or overturned.
- Gaps/errata/conflicts routed; registers exit 0 under `audit-register-hygiene.py`.
- Tree clean and committed at each task boundary. **Nothing released** — that stays Stephen's.

## Currency check (plan-to-tasks overlay §1, run 2026-08-26)

1. **Plan span / head** — 87 lines, authored 2026-08-26, head `ingestion`. New document; its newest
   (only) state block is the document itself, so there is nothing above the entry point.
2. **Sections superseded** — none. Compared against: the 33 dashboard rows, the queue section
   (4 rows, **2 stale** — folded into task 10), and an on-disk survey of every candidate source.
3. **Register state, findings in scope** — G-019 `OPEN` (KNOWLEDGE-GAPS.md:47) · G-020 `OPEN` (:48) ·
   G-021 `OPEN` (:49) · G-022 `OPEN` (:50) · F-250 `PARTIAL` (CORRECTION-FINDINGS.md:2880), and its
   disposition **names a sequence** — re-ingest, then re-verify derived claims — which this plan
   honours · F-357 `RESOLVED` (:299) · F-359 `CONFIRMED`, awaiting Stephen's scope decision (:294) ·
   F-360 `CONFIRMED` (:183) · F-362 `CONFIRMED` (:53).
4. **Blocking standing rules** — (a) Stephen's *"do not automatically release"*: this sprint ships
   no release. (b) F-359 awaits his scope decision, but it gates the **release**, not ingestion.
   (c) `SOURCE-REPAIR-ORDER.md` §7, source repair before destructive sweep: no destructive sweep
   here — **this sprint is the source-repair half**. **No contradiction found; no sprint stop.**

## Entry baseline (measured 2026-08-26, before task 1)

| Gate | Exit | Value |
|---|---|---|
| `verify-yaml-format.py` | 0 | All YAML files parsed cleanly |
| `validate-crossref-keys.py` | 0 | — |
| `audit-yaml-claim-sourcing.py` | 0 | 0 Tier 1 across 1132 files; 49 Tier 2 advisory |
| `audit-constant-fidelity.py` | 0 | — |
| `audit-extraction-digit-density.py --all` | 0 | CLEAN, **58 artifacts** (rises as this sprint adds) |
| `audit-register-hygiene.py` × 3 registers | 0 | all three clean |
| `validate-dod-release.py` | 0 | 12 checks green |

## Dispatch shape

`inline` — no Agent tool in this session, so the arbiter runs each task itself and the
fresh-context benefit is **not** obtained (`dispatch-contract` §6). Disclosed rather than implied.

## Section ↔ task cross-reference

| Plan § | Deliverable | Task | seq |
|---|---|---|---|
| Task-set 1 | silicon-doc passes 1–3 (content/tables/code/images) | «#309» | 44 |
| Task-set 2 | silicon-doc passes 4–5 (post-processing, audit) | «#310» | 45 |
| Task-set 3 | silicon-doc pass 6 (Q&A, comments, errata) | «#311» | 46 |
| Task-set 4 | **Re-test source-silent verdicts** | «#312» | 47 |
| Task-set 5 | silicon-doc pass 7 (quad update) | «#313» | 48 |
| Task-set 6 | pasm2-manual ingestion | «#314» | 49 |
| Task-set 7 | smart-pins-titus completion | «#315» | 50 |
| Task-set 8 | edge-standard-module completion | «#316» | 51 |
| Task-set 9 | TAQOZ Bit Bashers ingestion | «#317» | 52 |
| Task-set 10 | Dashboard + quad reconciliation | «#318» | 53 |
