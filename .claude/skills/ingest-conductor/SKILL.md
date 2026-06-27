<!-- Requires MCP: todo-mcp (head pointer + wave manifest); filesystem. Spawns subagents that each run the ingest-source skill. -->
---
name: ingest-conductor
description: >-
  Run a PARALLEL ingestion WAVE — fan several independent sources out to
  per-source subagents that each extract in STAGE-ONLY mode, then hand the
  staged batch to ingest-wrap-reduce for the single-writer merge. Use when
  the user says "ingest these N sources", "do an ingestion wave", "fan out
  the ingestion backlog", "parallelize the next ingestions", or there are
  two or more independent queued sources on the dashboard. This is the MAP
  half of map→reduce ingestion; ingest-wrap-reduce is the REDUCE half. For a
  SINGLE source, or sources that depend on each other, do NOT use this —
  run ingest-source serially.
---

# Conduct a parallel ingestion wave (the MAP half)

This is the **INGESTION head**'s fan-out driver. It does not re-extract
anything itself — it **delegates the per-source procedure to `ingest-source`**
(passes 1–5 only) running in parallel subagents, then triggers the serial
`ingest-wrap-reduce` to merge. The per-pass methodology lives in
`engineering/ingestion/` and in `ingest-source`; this skill orchestrates, it
does not restate.

> **Why stage instead of write?** The 7-pass ingestion has a natural seam:
> **passes 1–5 (content / code / images / post-proc / per-source validation)
> are independent per source**, but **passes 6–7 (cross-source Q&A + conflict
> audit, and registration of the shared dashboards) are cross-source and
> single-writer.** The registers also hand out *sequential* IDs (`F-NNN`
> findings, `G-NNN` gaps, `Q-NNN` expert-questions) that parallel agents
> cannot safely allocate. So the map runs 1–5 into a staging area and touches
> **no** canonical file or register; the reduce owns every shared write. This
> makes write-contention impossible by construction.

## 0. Head integration

1. **Set the pointer to the wave:** `mcp__todo-mcp__context_set
   key:"active_element" value:"ingestion:wave:<wave-slug>"` (pick a short slug,
   e.g. `boards-2026-06`). A wave is a *batch* element; individual sources are
   registered in step 2.
2. **Record the wave manifest:** `mcp__todo-mcp__context_set
   key:"ingest_wave_<wave-slug>"` with the source list (each: folder slug +
   input path + DOCX/PDF + whether it is a new source or a delta edition + any
   **companion inputs**, see §2). This is what `ingest-wrap-reduce` reads to find
   the batch.

## 1. The fan-out gate — decide whether to parallelize at all

Fan out **only** when the wave is genuinely a parallel map:

- **Two or more sources**, AND
- **mutually independent** — no source's extraction depends on another's, and
  none is a *delta edition* of another source in the same wave (a v55-over-v51
  delta must see the prior edition settled — sequence those across waves, never
  within one).

If the set is a single source, or any pair is coupled, **stop and run
`ingest-source` serially** for them — do not stand up the wave machinery. Record
the decision (and which sources were held back as coupled) in the hand-back.

## 2. Classify each source, then register the wave up front (single-writer, before any fan-out)

Do this **in this conductor**, serially, so no two agents ever race the dashboard.

**First classify each source into one of four modes** — this is the load-bearing
adaptation: a wave routinely mixes *new* sources with *re-ingestions* of existing
ones, and the mode drives both the row handling here and the promotion in the
reduce. Decide by searching the dashboard + `git log` + `sources/`:

| Mode | When | Canonical target (the reduce lands it) | Row handling (here) |
|------|------|----------------------------------------|---------------------|
| **new** | greenfield — no existing folder/row | create `sources/<src>/` | **add** row at 0%, gates open |
| **completion** | existing source, **same edition**, partial — fill missing passes (images/code/audit) | **augment** existing `sources/<src>/` | keep existing row + its %; add an in-flight marker |
| **re-extraction** | existing source, **same edition**, prior capture lossy/fabricated — replace | promote into existing `sources/<src>/` + **obsolete the prior** (`ingest-source` §0.6) | keep existing row; add an in-flight marker |
| **new-edition delta** | a newer edition supersedes the prior (e.g. v55 over v51) | **new** `sources/<src-edition>/`, keep prior for lineage (`ingest-source` §0.5) | **add** the new-edition row at 0%; leave the prior row intact |

Then, for each source:
- **Only `new` and `new-edition delta` rows start at 0%.** Never reset an existing
  source's row to 0% — `completion`/`re-extraction` keep their current % and gain a
  `‹wave-refresh in-flight›` marker, so a mid-wave interruption still resumes
  correctly via `whats-next`.
- Stand up the **staging** mirror — `engineering/ingestion/_staging/<wave-slug>/<src>/`
  — NOT the canonical target — for **every** mode (the reduce decides how to land
  it). Ensure `engineering/ingestion/_staging/` is gitignored; it is transient and
  torn down by the reduce.
- **Record each source's mode** (and, for the non-`new` modes, the path of its prior
  `sources/<src>/` baseline) in the wave manifest `ingest_wave_<wave-slug>` — the
  per-agent contract (§3) and the reduce both read it.

**Companion inputs — a first-class manifest shape.** A single logical source may
ship more than one input file: a **primary** document plus one or more
**companions** that ride with it, each carrying its own *role* and *tier* (per the
edition/role model). Two kinds seen so far:
- **cross-check companion** — a 3rd-party datasheet that corroborates the primary
  (e.g. the AKM **AK5704** datasheet beside the #64014 HD-Audio guide); tier 🟡
  cross-check, **never** promoted as a P2-fact authority.
- **example-code companion** — the product-page driver/example archive a board
  guide defers its code to (the code itself lives off-document; see §3 capture rule).

Record companions in the manifest as `companions: [{path, role: cross-check|example-code, tier}]`
on the owning source. They do **not** get their own dashboard row (they are inputs
to one logical source, not separate sources); the reduce reflects them in
`AUTHORITATIVE-SOURCES` (cross-check companion) and `DOCUMENT-LINEAGE` (captured
example code). If a referenced companion is **named but not staged on disk**, do
not block the wave — record it as a candidate gap (the agent flags it; the reduce
issues the `G-`).

Use the filesystem MCP for these writes, not bash (Sacred Rule #2), and respect
non-destructive editing on the shared dashboard (Sacred Rule #1: size-check +
backup the dashboard before adding/modifying rows).

## 3. The per-agent contract (what each map subagent must and must NOT do)

Each subagent runs **`ingest-source` passes 1–5 in STAGE-ONLY mode** for exactly
one source. Spell this out in the subagent's prompt:

- **Write only inside** `engineering/ingestion/_staging/<wave-slug>/<src>/`,
  mirroring the canonical `sources/<src>/` layout (text, `complete-*.md`,
  `assets/code-*`, `assets/images-*`, the pass-5 `<src>-extraction-audit.md`).
- **Do passes 1–5 only.** Defer pass 6 (cross-source Q&A + conflict audit) and
  pass 7 (registration) to the reduce — they need the whole batch.
- **Touch nothing canonical:** not `sources/`, not the dashboard, not
  AUTHORITATIVE-SOURCES / DOCUMENT-LINEAGE / KNOWLEDGE-GAPS, not the corrections
  register. **Allocate no `F-`/`G-`/`Q-` IDs** — the reduce owns ID issuance.
- **Keep canonical `sources/` byte-for-byte untouched — including tool intermediates.**
  `pdf2md`/docling/`camelot`/`pdftotext` default to writing output *next to the
  input file*, and the input lives in canonical `sources/<src>/` — so a naive run
  drops a stray `.md`/`.csv` into canonical. Direct every tool's `--output` (or
  `cwd`) at your staging dir (or a scratch dir under it), and if a tool still drops
  an intermediate in `sources/`, move it into staging before you finish. The reduce
  promotes from staging; anything you leak into `sources/` bypasses that gate.
- **Carry the manifest's auth tier forward — do not re-litigate tier philosophy.**
  The dashboard legend is fixed: 🏆 = *authoritative*, which **includes official
  Parallax documentary guides** (it is NOT empirical-only). Propose the tier the
  manifest already carries; only propose a *change* on hard evidence (a demonstrated
  factual error), and even then the **reduce adjudicates**. Do not flag a Parallax
  board guide's 🏆 as "mis-assigned because it's documentary" — that is wrong.
- **Single-source post-processing only** in pass 4; any *cross-source* matrix is
  reduce work.
- **Honor the source's mode** (from the manifest), reading the prior
  `sources/<src>/` baseline **read-only** when one exists:
  - `new` / `re-extraction` → extract fully (passes 1–5). A `re-extraction` does
    *not* trust the prior lossy capture; it re-does the work.
  - `completion` → extract **only the missing passes/gaps** the baseline lacks
    (e.g. images, `pnut_ts` code validation, the pass-5 audit) — don't redo what is
    already good; the HANDBACK lists which gaps were filled.
  - `new-edition delta` → extract fully **and diff against the prior edition** to
    scope the change set (`ingest-source` §0.5).
  In every mode the agent **still writes only into staging** and touches nothing
  canonical (the prior baseline is read-only input).
- **Handle companion inputs per their role** (from the manifest):
  - **cross-check companion** (datasheet) → extract only the *corroboration subset*
    needed to confirm the primary's fact-bearing fields (register map index, pinout,
    electrical/format specs); keep it clearly labelled as cross-check tier, in its own
    staged file (`<companion>-crosscheck-*.md`), never blended into the primary; report
    the corroboration verdict (match / conflict, with evidence) in the HANDBACK.
  - **example-code companion** (product-page driver/example archive) → **capture it
    into staging and catalog its availability — that is as far as the map goes.**
    Stage the archive/sources under `assets/code-<date>/` (unpacked if small),
    record in the HANDBACK *that* driver/example code exists and where it came from,
    and note it is **captured-not-processed** (no `pnut_ts` deep-validate, no
    extraction matrix — a later dedicated code pass owns that). The point now is that
    the code is *in the source tree and findable*, not that it is analysed.
  - **companion named but not on disk** → do not fetch from the web mid-wave; flag it
    as a candidate gap (the reduce issues the `G-` and notes the product-page source).
- **Emit a handback manifest** at `_staging/<wave-slug>/<src>/HANDBACK.md`:
  the source's **mode** (and, for `completion`, which prior gaps it filled);
  per-pass counts (paragraphs/tables; code extracted / `pnut_ts`-validated /
  failed; images extracted / quality-passed / OCR'd); the proposed Auth tier;
  the proposed dashboard cells (C·K·I·A·X) and completeness %; and — as
  *proposals, not applied* — candidate answered-gaps, candidate new gaps,
  candidate expert-questions, and candidate conflicts (each with its evidence
  and the authority it would be judged against). The reduce adjudicates and
  numbers these.

## 4. Fan out

Spawn one subagent per source (in a single batch so they run concurrently), each
carrying the §3 contract and its source's input path. The subagents inherit the
ingestion tooling `ingest-source` uses (DOCX/PDF extraction, `pnut_ts`,
`image-tools-mcp`).

## 5. Barrier — collect, then trigger the reduce

Wait for every subagent, then:

- **Collect** each `_staging/<wave-slug>/<src>/HANDBACK.md`.
- **Handle partial failure deterministically:** a source whose agent died or
  produced no clean staging stays at **0% on the dashboard** (its row was added
  in step 2 but never advances) — report it as failed-this-wave; the wave
  proceeds with the rest. Never half-promote a failed source.
- **Trigger the reduce:** invoke `ingest-wrap-reduce` with `<wave-slug>`. That
  skill drains staging, merges cross-source, rolls up the quad, and routes
  conflicts. The conductor does **not** do any of that.

## 6. Hand back

Report: the wave slug and its sources; the fan-out decision (and any coupled
sources held for serial ingestion); per-source map status (staged-OK / failed);
and that `ingest-wrap-reduce <wave-slug>` is the next step. Do not report
completeness %, conflicts, or gap movement — those are the reduce's outputs.

## What NOT to do

- **Don't fan out a single source or a coupled set** — that is serial
  `ingest-source` work; the wave machinery is overhead there.
- **Don't let a map agent write canonical files or allocate register IDs** — the
  whole design rests on map=stage-only, reduce=single-writer.
- **Don't run pass 6/7 in the map** — cross-source triangulation and the shared
  dashboards need the complete batch.
- **Don't conflate *editions* with *re-ingestions*** — a *new edition* (delta) is a
  new `sources/<src>/` folder (and never shares a wave with its predecessor, §1);
  but a *same-edition* `completion` or `re-extraction` correctly lands in the
  **existing** folder (§2 modes). Don't force a new folder for those, and don't
  reset their dashboard row to 0%.
- **Don't skip the up-front dashboard registration** — rows at 0%/gates-open are
  load-bearing for `whats-next` resume if the wave is interrupted mid-flight.
