<!-- Requires MCP: todo-mcp (region pointer + fan-out manifest); filesystem; p2kb-mcp (p2kb-obex-find/get/download). pnut_ts to compile any captured code. -->
---
name: mine-and-delineate
description: >-
  Process external community code (OBEX / Quick Bytes / forum / external)
  to determine a DOCUMENTATION boundary — what is foundational (enriches the
  owning manual) versus what is advanced technique (becomes an app note).
  Use when the user says "mine the <topic> examples", "decide the IOSP-vs-app-note
  split for <region>", "run the boundary determination for <region>", "fan out
  the boundary passes for these regions", or an app-note/manual-enrichment effort
  needs its split settled before authoring. This is the shared front-end of the
  two-pipeline app-note model (document-enrichment + app-note). It is NEITHER
  KB-fact ingestion (distinct from ingest-source) NOR authoring — it decides the
  split first; the owning-manual edit and the app-note authoring are downstream.
---

# Mine and delineate — determine a documentation boundary

This skill turns community code into a **boundary decision**: for a topic region
(e.g. DAC, frequency measurement, USB), study real examples and **delineate**
what is *foundational* — belongs in the owning reference/manual — from what is
*advanced technique* — belongs in an app note. The examples are what make the
boundary **objective rather than guessed** (proven on P2AN001 ADC, P2AN002 CORDIC).

It has **two modes**:

- **Single-source mode** (§§1–4) — one region, run inline. The unit procedure.
- **Fan-out / coordinator mode** (§§5–7) — N independent regions in parallel,
  each emitting the **same mergeable artifact**, then a single-writer **reduce**
  that lands every foundational fork into its owning manual. Document generation
  (authoring the app notes) is **downstream of the reduce**, never part of it.

It does **not** edit the owning manual's opus-master itself (that is
`document-finalize` / the manual's revision skills) and does **not** author the
app note (that is the app-note authoring pass). It produces the **artifact** that
drives both, and — in fan-out mode — performs the single-writer merge of the
foundational forks.

---

## The two-discriminator delineation test (the heart of the skill)

Every boundary call reduces to two questions (from
`engineering/analysis/p2-app-note-roster.md` §1):

1. **Architecture *concept* vs. language *feature/technique*.** How to *structure*
   a system → architecture (the Architect's Guide), not this skill's output. A
   specific feature/applied technique that needs how-to-use guidance → an app
   note. A single topic can split across the line: the *contract decision* is
   architecture; the *worked implementation* is technique.
2. **Reference-exists → app note, not a guide; foundational → the owning manual.**
   Where the reference already exists, only the *applied* layer is missing →
   app note; the foundational layer is **cited, not reproduced**.

**Both forks are independently optional** — this is the load-bearing lesson from
the proven runs, and the skill must handle every combination:

| Run | Foundational fork (→ owning manual) | Advanced fork (→ app note) |
|-----|-------------------------------------|----------------------------|
| **P2AN001 ADC** | **present** — basic ADC modes → IOSP Ch.16 §16.3/§16.6 (manual *lacked* it) | present — recipes (3-pin, filter, range, mains) + described-not-rebuilt capstone |
| **P2AN002 CORDIC** | **absent** — reference already adequate (PASM2 manual + `cordic.yaml`), cited not reproduced | present — applied recipes |
| **USB (this campaign)** | present — USB smart-pin mechanics → IOSP | **absent** — no app note this cycle (a later decision) |

So: emit the foundational fork **only** when the owning manual genuinely lacks the
coverage; emit the advanced fork **only** when there is a committed app note. A
region can be enrichment-only (USB), app-note-only (CORDIC), or both (ADC).

---

## The mergeable output contract (the linchpin)

Every run — single-source **or** one leg of a fan-out — emits the **same**
structured **boundary-determination artifact**, so N runs reduce identically.
The artifact is authored as the boundary sections of the app note's
`P2ANxxx-NOTES.md` (when there is an app note — the proven home, see
P2AN001/P2AN002 NOTES) **and/or** a standalone boundary doc under the owning
manual's `audit/` (for an enrichment-only region like USB). Its fields:

```
region:            <topic> + owning manual (the enrichment target)
sources_mined:     [ {name, OBEX #NNNN / QB / citation, role, tier, captured-at-path} ]
source_traceability: [ {claim / number / code, source (KB key / EF / pnut_ts / forum), verified} ]
boundary:
  foundational  -> owning manual : [ {addition, target location e.g. "IOSP Ch.16 §16.3", cite-not-reproduce} ]   # MAY BE EMPTY (reference adequate)
  advanced      -> app note      : [ {recipe / technique, archetype} ]                                            # MAY BE EMPTY (no app note this cycle)
  described_not_rebuilt: [ capstone / out-of-scope items linked but not built ]
verification_model:  hardware-independent known-answer  |  rig-gated (Tier-0/1/2 table)   # per P2AN002 vs P2AN001
open_questions:      [ ... ]      # incl. proposed corrections-register candidates — PROPOSED, never allocated here
```

**Discipline that makes the artifact trustworthy** (carried from the proven runs
and the trust chain):
- **Cite, don't reproduce, foundational reference** — the owning manual references
  the authority; it does not duplicate it.
- **Every claim traces to a source** — KB key, the empirical-findings (EF) ledger,
  a `pnut_ts` compile, or a named forum/OBEX author. No inference
  ([[feedback_no_inference_or_derivation_in_yaml]] / [[feedback_no_unsourced_claims]]).
- **Untested community code is an open-question, not a claim** — e.g. "these OBEX
  USB drivers may be production-ready, untested" is recorded as an open-question,
  never asserted.
- **Propose corrections, never allocate IDs** — a conflict with published P2KB
  content is a *proposed* `F-NNN` for the corrections register; the actual `F-`
  number is allocated by whoever lands it (the merge / the YAML-maintenance pass),
  exactly as the ingestion reduce owns `F-`/`G-`/`Q-` issuance.

---

## §1. Locate + download the examples

Set the region pointer: `mcp__todo-mcp__context_set key:"active_element"
value:"manual:<owning-manual>"` (or the app-note element) if not already there.

Find and pull the real code the boundary will be cut against:
- **OBEX** — `p2kb_obex_find` / `p2kb_obex_get` by keyword; `p2kb_obex_download`
  to extract source. **Always record the permanent `OBEX #NNNN`** (the stable id).
- **Quick Bytes** — `deliverables/ai/P2/community/quick-bytes/`.
- **Forum / external** — capture verbatim (posts + code attachments), as P2AN001
  did with Chip Gracey's ADC thread.

Capture everything **verbatim** under the region's `research/<source>/` (for an
app-note region: `app-notes/<P2ANxxx>/research/`). Do not paraphrase the source
into the capture — paraphrase loses the evidence.

## §2. Study the examples

Read the captured code + prose. Produce a `STUDY-*.md` per source cluster
(P2AN001/P2AN002 precedent) recording *what each example does* and *which
mechanism it relies on*. Compile any code you intend to lean on with `pnut_ts`
(`-d` if it uses `debug()`) — a claim resting on code that does not compile is not
a claim. Validate mechanisms against the P2KB FIRST
([[feedback_validate_idioms_against_kb_first]]) — the KB is the authority; the
community code is the *applied evidence*, not the truth source.

## §3. Delineate — apply the two-discriminator test

For each capability the examples exercise, decide foundational vs advanced via the
test above, and which fork(s) apply for this region:
- **foundational** → the owning manual (with the exact target location), **cited
  not reproduced**. Emit this fork only if the manual lacks the coverage.
- **advanced technique** → the app note (recipe + archetype). Emit only if an app
  note is committed this cycle.
- **described-not-rebuilt** → a ceiling example linked but not rebuilt (P2AN001's
  8-pin interpreter, P2AN002's Park/FOC capstone).

Record *why* each call was made — the boundary decision is the durable output.

## §4. Emit the artifact

Write the mergeable artifact (contract above) into its home(s): the app note's
`P2ANxxx-NOTES.md` boundary sections (Boundary delineation / Sources to mine /
Source traceability) and/or the enrichment-only boundary doc under the owning
manual's `audit/`. Set the verification model. List open-questions + proposed
corrections.

**Single-source mode ends here** — the artifact is the deliverable. It hands two
forks downstream: the **foundational fork** to the owning-manual revision
(`document-finalize` / `prepare-manual`), the **advanced fork** to app-note
authoring. This skill does not perform those edits.

---

## §5. Fan-out / coordinator mode — the MAP

Use this only when boundary determination spans **two or more independent
regions** (e.g. USB + DAC + Freq in one campaign). Modeled on
`ingest-conductor` (MAP) + `ingest-wrap-reduce` (REDUCE).

**Fan-out gate.** Fan out only when the regions are **mutually independent** (no
region's boundary depends on another's). A single region, or coupled regions, run
**single-source serially** (§§1–4) — do not stand up the fan-out machinery. Record
the decision (and any region held back as coupled) in the hand-back.

**Manifest (single-writer, before any fan-out).** Record the region list in
`mcp__todo-mcp__context_set key:"mine_wave_<wave-slug>"` — each entry: region
topic, **owning manual** (enrichment target), whether an **app-note fork** is
expected (and its `P2ANxxx`), and the sources to mine. Stand up a **staging**
mirror `engineering/document-production/_mine-staging/<wave-slug>/<region>/`
(ensure `_mine-staging/` is gitignored; it is transient and torn down after the
reduce) for each region's `research/` capture + artifact.

**Per-agent contract (spell this out in each subagent's prompt).** Each subagent
runs **§§1–4 for exactly one region, STAGE-ONLY**:
- Write **only** inside the region's staging mirror — its `research/` capture, its
  `STUDY-*.md`, and its boundary artifact (`HANDBACK.md`-style).
- **Touch nothing canonical** — not the owning manual's opus-master, not
  `P2ANxxx-NOTES.md` in place, not the corrections register. **Allocate no
  `F-NNN`** — propose only; the reduce issues IDs.
- Point every tool's output at staging — `p2kb_obex_download`, `pdf2md`, etc.
  default to writing beside their input; redirect them so nothing leaks into a
  canonical tree.
- **Emit the artifact** in the contract shape as the region's `HANDBACK.md`.

**Spawn** one subagent per region in a single batch (concurrent). **Barrier:**
wait for all, collect each region's `HANDBACK.md`. A region whose agent died or
produced no clean artifact is reported failed-this-wave and excluded from the
reduce — never half-merged.

## §6. The REDUCE — single-writer merge into the owning manual(s)

**Gather-then-resolve.** Build the complete inventory of all regions' artifacts
**before** writing anything canonical — the batch reveals cross-region overlaps no
single region shows.

1. **Reconcile overlaps across artifacts.** Two regions proposing additions to the
   *same* manual location (e.g. USB and DAC both touching analog-pin config) merge
   to **one** addition — detect and reconcile, never double-write.
2. **Land each foundational fork** into its owning manual's **opus-master**
   (single writer, non-destructive — Sacred Rule #1: size-check + backup; edit the
   opus-master, **never** the workspace render —
   [[feedback_edit_opus_master_not_workspace_render]]). Cite, don't reproduce.
3. **Allocate corrections-register IDs** — every proposed `F-NNN` from the
   artifacts is now issued (sequential, single-writer) into
   `engineering/operations/P2KB-CORRECTION-FINDINGS.md`.
4. **Promote each region's staged artifact** to its canonical home (the app note's
   `P2ANxxx-NOTES.md` boundary sections / the enrichment boundary doc).

The reduce is the **barrier**. **Document generation — authoring the app notes
from their advanced forks — is downstream of the reduce**, a separate tail of
tasks, not part of the merge (it writes different files; the merge owns the shared
owning-manual write).

## §7. Hand back

Report: the regions and the fan-out decision (and any held-back coupled region);
per-region map status (artifact-OK / failed); the overlaps reconciled in the
reduce; the foundational forks landed (with manual + location) and any `F-NNN`
issued; and the advanced forks queued for downstream authoring. Do not author the
app notes here.

---

## Validation — does the procedure reproduce the proven splits?

Before trusting the skill, dry-run it against the two proven runs:
- **P2AN001 ADC** — does §3 land basic ADC modes as a *foundational* fork to IOSP
  Ch.16 and the recipes as the *advanced* fork, with the 8-pin interpreter
  *described-not-rebuilt*? (It must.)
- **P2AN002 CORDIC** — does §3 produce **no** foundational fork (reference already
  adequate, cited not reproduced) and an app-note-only result? (It must — the
  conditional-fork handling is what makes this correct.)

If the procedure cannot reproduce both, it is wrong — fix the skill, not the run.

## Promotion note

Modeled on the proven `ingest-conductor` + `ingest-wrap-reduce` pattern but kept
**in-repo** (this is the document-production head, a different head from KB-fact
ingestion). Once the fan-out has run cleanly at least once, a dedicated
**boundary-conductor** + central promotion of this skill is a candidate — logged
in `feedback_skill_evolution_candidates.md`.
