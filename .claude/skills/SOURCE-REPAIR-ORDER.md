# Repairing unsourced content — the order, and why it is an order

**Stated once here. Skills point at this file; none of them restate it** — a restated rule
drifts from its original, which is the defect this file exists to prevent. Same convention as
`REGISTER-CONSULTATION.md`.

Origin: 2026-08-24, the P2KB constant-fidelity sprint. An agent consuming the shipped KB could
not work out how to configure a pull-up and reported contradictions. Seven defects
(F-321…F-327) had passed every release. Stephen set the repair shape below over a softer form
that had been tasked; every rule here is one of the specific things that would otherwise have
gone wrong.

---

## 1. The order

> **Re-ingest the source → remove ALL of it → repopulate by re-deriving from the source.**

Three steps, in that sequence. Not "keep the block and find a citation for it."

## 2. Why cite-in-place is the wrong move, even though it is cheaper

**Cite-in-place is claim-first.** It opens an existing block, then goes looking for an authority
that supports what the block already says. That is how a loosely-related citation gets stapled
onto a wrong claim — and the result is worse than the uncited original, because it now *looks*
grounded and no instrument can tell the difference.

**Repopulation is source-first.** Read the source, write what it states, in the source's
wording. If the result matches what was removed, good. If it does not, the source wins.

The distinction is not academic. Every defect in the sprint's origin story was written by
someone reasoning plausibly who could have produced a citation: `P_HIGH_15K` *behaves a bit
like* a pull-up; a drive ladder *ought to* have current steps; `M[6:0]` *looks like* the drive
field. None of it was careless and all of it was confident.

**Corollary — volume inverts the temptation, so watch for the other failure too.** Under
cite-in-place the pressure is to invent a value. Under remove-all it is to talk yourself out of
a deletion. Uncited means removed; whether you believe an authority exists is the repopulation
step's judgement, made from the source, not this step's.

## 3. Why the re-ingestion moves FIRST — the part that is easy to get backwards

Removing before repairing the source looks safe because git holds everything. It is not, for
two reasons:

1. **You should know what can be restored before you delete it.** Where an extraction fails,
   the disposition is a recorded gap — and that wants recording *now*, not discovering later.
2. **Check that a restore path actually exists for every class being purged.** In the sprint
   that produced this file, the datasheet class had one (§8b) and the board-guide class did
   not. Same removal, two different consequences: reversible for one, permanent for the other.
   That asymmetry is what made the ordering a defect rather than a preference.

**A finding that says "re-ingest this source, then re-verify every claim derived from it" is an
ordering instruction, not just a work item.** (F-250 said exactly that, and the first tasking
scheduled the re-ingestion *after* the sweep that consumed those facts.)

## 4. The gate — an incomplete ingestion stops the destructive step

Under cite-in-place a weak source meant a weak citation. **Under remove-all it means the
content is permanently gone.** So ingestion completeness becomes a precondition of the purge,
not a best effort.

Stephen, 2026-08-24: *"stop if we have ingestion problems, see if we can complete ingestions
before continuing."*

Written in the stop roster's vocabulary — **this file mints no stop**:

| Situation | Kind | Reaches Stephen? |
|---|---|---|
| An extraction path failed; others remain untried | **step halt** — try the next path | No |
| Every path exhausted, content still unrecoverable | **sprint stop 1** — a decision he owns (accept permanent loss, or source the document differently) | Yes |
| The container simply cannot do a thing | **named non-stop** — a capability limit yields a provisional verdict | No |

Exhaust the tooling before escalating. For a PDF that means the whole ladder — `camelot
lattice` → `camelot stream` → `pdf-layout` → `pdf-ocr --force-ocr` + re-extract → a different
page range → **a DOCX edition if one exists**, which carries table structure a PDF text layer
cannot. `/opt/pdf-tools/README.md` documents the chain.

**Dispatch does not transfer this stop.** A dispatched agent that exhausts its paths escalates
to the **arbiter**; the arbiter judges whether they are genuinely exhausted and only then raises
it. (`task-execution` dispatch contract §2 — dispatch does not transfer authority it never had.)

## 5. Two traps this file exists to keep catching

- **A citation into a hole.** A source can be present, ingested, and dashboard-green while
  being unable to carry the fact you are citing. F-250: a board guide extracted with a tool
  whose font encoding dropped every numeral — digits on 91 of 1315 lines — while its dashboard
  row read `100% (stated)`. Citing into that is not grounding. Check what the ingestion
  actually recovered before citing into it.
- **A status line is not evidence, and it lies in both directions.** It can claim completeness
  a source does not have, and it can mark work outstanding that is done. Measure the artifact.
  A cheap proxy that works for this trap: **digit density** — a hardware document whose
  extraction is nearly digit-free has failed, not been read. It catches *total* numeral loss,
  not partial, so it is a smoke alarm and never a clean bill of health.
  Executable since 2026-08-24: `engineering/tools/validation/audit-extraction-digit-density.py`,
  mandatory on every pass-1 extraction (`ingest-source` §2a). Run it; don't reason about it.

## 6. What the closeout must report

Three numbers, never one "closed" total: **grounded fixes · gaps · removals.** A single number
cannot distinguish the outcome this file wants from the one it exists to prevent — closing
fifty findings by guessing at some of them has not fixed fifty findings, it has replaced
defects we could see with defects we cannot.

Related: `REGISTER-CONSULTATION.md` · `HEAD-DISPATCH-DRAFT.md`
