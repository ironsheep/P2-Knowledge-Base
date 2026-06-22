<!-- Requires MCP: todo-mcp (wave manifest + head pointer); filesystem. Uses pnut_ts + the validate-*.py suite as the reduce gate. -->
---
name: ingest-wrap-reduce
description: >-
  Merge a staged ingestion WAVE in a single serial single-writer pass — drain
  each source's staging into canonical sources/, dedup, run the cross-source
  Q&A + conflict audit (pass 6) across the whole batch at once, roll up the
  ingestion quad (dashboard + AUTHORITATIVE-SOURCES + DOCUMENT-LINEAGE +
  KNOWLEDGE-GAPS), and exception-route every conflict touching published YAML
  to the corrections register. Use after ingest-conductor reports a wave's
  map agents are done, when the user says "wrap the ingestion wave" / "reduce
  the staged sources" / "merge the ingestion backlog". This is the REDUCE half
  of map→reduce ingestion; ingest-conductor is the MAP half.
---

# Wrap a staged ingestion wave (the REDUCE half)

This is the **INGESTION head**'s single-writer merge. The map (`ingest-conductor`
+ per-source `ingest-source` passes 1–5) has left each source extracted into
`engineering/ingestion/_staging/<wave-slug>/<src>/` with a `HANDBACK.md` of
proposals — and has touched **no** canonical file. This skill is the **only**
writer of the shared dashboards and registers for the wave, which is what makes
the parallel fan-out safe: only here are the sequential `F-`/`G-`/`Q-` IDs
issued, so they can never collide.

> **Gather-then-resolve.** Build the *complete* inventory of staged outputs and
> proposed deltas across the whole wave **before** writing anything canonical.
> The batch reveals cross-source patterns (the same fact corroborated or
> contradicted by two wave siblings) that no single source shows, and it lets
> the expensive steps — the corroboration pass, the validator gate, the quad
> roll-up — run **once** for the wave, not once per source.

## 0. Entry

1. Read the pointer / wave: `mcp__todo-mcp__context_get key:"active_element"`
   (expects `ingestion:wave:<wave-slug>`) and `ingest_wave_<wave-slug>` for the
   source list. If invoked standalone, take the wave slug from the user.
2. **Inventory (gather):** read every `_staging/<wave-slug>/<src>/HANDBACK.md`
   plus the staged artifacts. Assemble one batch inventory — per source: the
   staged files, the pass-5 audit result, and the proposed register deltas
   (Auth tier, dashboard cells, answered/new gaps, expert-Qs, conflicts). Do not
   write anything yet.

## 1. Promote staged extractions → canonical, **per the source's mode**

For each source whose pass-5 extraction audit passed, land its staged tree
according to the **mode** the conductor recorded in the wave manifest (a
failed-audit source stays in staging, reported not promoted). Single-writer and
**non-destructive** (Sacred Rule #1: size-check + backup any file >100 lines /
>50 KB before modifying; never truncate), via the **filesystem MCP**, not bash
(Sacred Rule #2):

- **new** → create `sources/<src>/` from staging.
- **completion** (same edition, partial) → **merge** the staged files into the
  existing `sources/<src>/`, *augmenting* — add the newly-extracted passes
  (images / validated code / the pass-5 audit) without clobbering prior good
  artifacts; replace a file only where the new pass genuinely supersedes it.
- **re-extraction** (same edition, prior lossy/fabricated) → promote the staged
  tree into the existing `sources/<src>/`, and **obsolete the prior artifacts**
  per `ingest-source` §0.6 (re-extraction flavor): if anything references them,
  stub-in-place / mark-superseded with a redirect **first** (Sacred Rule #7),
  only then move to a gitignored `archive/`. Flag the prior-derived downstream
  content as suspect-until-rechecked for the §3 cross-source pass.
- **new-edition delta** → create a **new** `sources/<src-edition>/`; **keep the
  prior edition's folder intact** for lineage/diff (`ingest-source` §0.5).
  Record the supersession in §6.

**Never overwrite a *prior edition's* folder** (that is the delta case → new
folder). But a *same-edition* `completion`/`re-extraction` **does** land in the
existing folder, per the modes above — that is the point of the adaptation.

## 2. Dedup across the batch and against the corpus

With all sources landed, reconcile duplicates the map could not see: a fact
extracted by two wave siblings collapses to one canonical home; near-identical
candidate gaps / conflicts merge. This step needs the whole batch — it is why
the reduce is a barrier, not a per-source step.

## 3. Cross-source Q&A + conflict audit (pass 6, across the whole wave)

Run `ingest-source` §5 (Cross-Source Q&A) and §4 (the multi-source corroboration
matrix) **over the newly-landed set together** — every new fact is triangulated
against *every* eligible ingested source, including its wave siblings (a fact a
lone serial ingestion would only have checked against the then-existing corpus
now also gets checked against the sources landing beside it). All three legs are
required — answer prior open questions, raise new ones, and flag conflicts; do
not ship having only flagged conflicts. Harvest any embedded reviewer notes
(`word/comments.xml`) per `ingest-source` §5.3. Resolve inter-source
disagreement by the authority order in `AUTHORITATIVE-SOURCES.md`
(hardware-verified → `pnut_ts` → Silicon Doc → datasheet → CSV → community).

## 4. Issue the sequential IDs (the single-writer keystone)

Now — and **only** here — allocate IDs from each register's "next ID" header,
in one pass, so they cannot collide:

- New gaps → `G-NNN` in `KNOWLEDGE-GAPS.md` Part A.
- Expert-only questions → `Q-NNN` in `KNOWLEDGE-GAPS.md` Part B.
- Conflicts touching published YAML → `F-NNN` in the corrections register
  (§7/§8 below).

Advance each register's "next ID" header in the same edit.

## 5. The reduce gate — validate before rolling up

Run the gate that applies to what the wave produced; require clean before
writing the quad:

- If the wave's findings introduce or touch cross-references in published YAML,
  run `python engineering/tools/validate-crossref-keys.py` (exit 0 = all
  resolved); if the index is affected, regenerate with
  `generate-p2kb-index.py` and confirm with `validate-dod-release.py`. **Note:**
  ingestion itself does **not** edit `deliverables/ai/P2/` YAML — those changes
  are the YAML head's, routed via the corrections register (§7). The validators
  here confirm the *registers and any ingestion-side cross-references* resolve.
- Always confirm each promoted source carries a passing pass-5 extraction audit,
  and that the roll-up leaves the quad internally consistent — completeness % /
  gate cells match the landed reality, and **no dangling references** to staged
  or archived paths (Sacred Rule #7 — redirect, never strand).

## 6. Roll up the ingestion quad (single-writer canonical write)

Update all four standing docs from the same batch, non-destructively
(`ingest-source` "Dashboards & registers"):

- **`engineering/ingestion/README.md`** (dashboard) — set each wave source's row
  to its new completeness %, gate status, and C·K·I·A·X cells, and clear the
  `‹wave-refresh in-flight›` marker. **Per mode:** `new` / `new-edition delta`
  advance from 0% (the delta also adds its row + annotates the prior row's
  lineage); `completion` / `re-extraction` advance from the **prior %** (never
  reset to 0%). Refresh the Tier-1 counts (sources, authority breakdown,
  open-question rollup) — a `new-edition delta` adds a logical source; a
  `completion`/`re-extraction` does not.
- **`AUTHORITATIVE-SOURCES.md`** — assign/confirm each source's trust tier (a
  new edition re-confirms; add aliases/part-numbers for hardware).
- **`DOCUMENT-LINEAGE.md`** — record any supersession (delta editions in the
  wave) and source→output lineage; handle obsolete prior artifacts per
  `ingest-source` §0.6 (mark-in-place + redirect before any archive move).
- **`KNOWLEDGE-GAPS.md`** — move answered rows OPEN→ANSWERED (with the source @
  edition that filled them), add the new `G-`/`Q-` rows from §4, harvest
  reviewer notes.

## 7. Exception-route conflicts → the corrections register

Append each YAML-touching conflict to
`engineering/operations/P2KB-CORRECTION-FINDINGS.md` as an `F-NNN` entry
(status `NEEDS-VERIFICATION`, or `CONFIRMED` when already settled against an
authority), carrying: what is wrong, where in `deliverables/ai/P2/`, the
evidence, and the authority order applied. This hands the defect to the YAML
head (`yaml-knowledge-base-maintenance`). **This skill never edits
`deliverables/ai/P2/` YAML itself** — it routes. Unresolved-by-any-source facts
go to `KNOWLEDGE-GAPS.md` Part B for the user, not guessed.

## 8. Surface the exception batch for the user

The conflicts (corrections register) and expert-only questions (gaps Part B) are
the **human-review queue** — the items only the user / chip designer can settle.
Present them as a batch with their F-/Q- IDs; do not self-resolve a fact that
needs an accuracy call.

## 9. Tear down + hand back

- Once promotion and the quad roll-up are validated, remove
  `engineering/ingestion/_staging/<wave-slug>/`. If any source was **not**
  promoted (failed audit), leave its staging intact and say so — never delete
  unpromoted work (Sacred Rule #1). Clear `ingest_wave_<wave-slug>` and reset
  `active_element` (to the next target or unset).
- **Report:** per-source completeness % + gate status now on the dashboard;
  trust tiers set; lineage/supersession recorded; gaps moved / raised (with
  IDs); conflicts routed to the corrections register (with `F-` IDs); validator
  results; the human-review batch (§8); and staging torn down. Suggest the next
  step (the YAML head working the routed `F-` findings).

This skill does NOT commit/push and does NOT edit P2KB YAML. It produces the
canonical, merged wave + the routed findings, in one single-writer pass.

## What NOT to do

- **Don't write any canonical file before the batch inventory is complete** —
  gather-then-resolve; the cross-source pattern only shows in the whole batch.
- **Don't let `F-`/`G-`/`Q-` IDs be allocated anywhere but §4** — sequential,
  single-writer, in one pass; this is what made the parallel map safe.
- **Don't edit `deliverables/ai/P2/` YAML** — route conflicts to the corrections
  register; the YAML head applies them.
- **Don't ship pass 6 having only flagged conflicts** — answered + new questions
  are required legs (`ingest-source` §5).
- **Don't single-source a verification** — triangulate against every eligible
  source (`ingest-source` §4).
- **Don't delete unpromoted staging** or strand a reference when tearing down —
  redirect/mark-in-place (Sacred Rule #7).
- **Don't mark a source complete with open gates** — the dashboard cells are
  load-bearing for `whats-next` resume.
- **Don't reset an existing source's row to 0%** — only `new` / `new-edition delta`
  start at 0%; `completion` / `re-extraction` advance from the prior % (§1/§6 modes).
- **Don't force a new folder for a same-edition re-ingestion** — `completion` /
  `re-extraction` land in the existing `sources/<src>/`; only a *new edition* gets a
  new folder.
