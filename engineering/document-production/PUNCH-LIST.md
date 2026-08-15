# Document Production — Punch List

Cross-cutting document-production cleanup items that are **not** specific to a single
manual. Per-manual items live in each `workspace/<slug>/PUNCH-LIST.md`.

---

## Front-matter `\markboth{}{}` missing in four manuals — OPEN

**Status:** ⏳ Open — relocated here 2026-08-15 from a stale auto-memory during the Sprint-2
entry check. Verified still owed at relocation time, not carried forward on trust.

XBYTE's front matter carries the copyright-page `\markboth{}{}` one-liner; **four manuals do
not.** Measured 2026-08-15 (`grep -c markboth opus-master/front-matter.md`): XBYTE **1**;
Streamer, Architect's Guide, Getting Started, Debug Window all **0**.

**Two of the four — Streamer and Debug Window — are in Sprint 2's release wave.** They are
being re-rendered and patch-bumped anyway, so the one-liner should ride those renders rather
than earn its own cycle later. Architect's Guide and Getting Started are not in the wave and
wait for their next render.

**Sibling item, verified DONE and NOT carried:** the platform `\needspace 7→3` change is
already applied in `platform/templates/p2kb-platform-foundation.sty` (§194 documents the
3-baselineskip reserve; §198 records that 7 proved over-aggressive), and the 2026-08-08
render wave verified 14/15 full documents against it. Recorded here only so the next reader
does not re-open it.

---

## Guide-conformance instrument — standards-tree coverage — OPEN

**Status:** ⏳ Open — deferred 2026-08-15 by Stephen's decision on the Sprint-2 planning
questions. Sprint 2 widens the glob to **descriptors only**; this is the remaining half.

`engineering/tools/validation/audit-guide-conformance.py` globs the voices catalog,
`app-notes/APP-NOTE-*.md`, and `manuals/*/*guide*.md`. Two layers sit outside it. Sprint 2
takes the first (`MANUAL-DESCRIPTOR.md`, 17 files). This entry holds the second:
**`engineering/standards/documentation-standards/` — 19 files, of which only the voices
catalog is currently scanned.**

**Measured, not estimated** (2026-08-15, scratch copy of the instrument with both globs
widened — 28 files/0 findings → 63 files/60 findings):

| Layer | files w/ findings | findings |
|---|---|---|
| descriptors — **taken in Sprint 2** | 11 | 38 |
| standards tree — **this entry** | 8 | 22 |

The 22 concentrate in four files: `style-guide-extraction-tasks.md` (6),
`instruction-documentation-template.md` (6), `capitalization-and-terminology-standard.md` (4),
`documentation-generation-planning.md` (1) — plus 5 spread across the extraction-era style
guides covered by the next entry. Detections are D4 codename and D2 `pnut_ts`, same classes
the descriptor pass will already be clearing.

**One item here is not mere coverage and should be read before this is scheduled:**
`capitalization-and-terminology-standard.md` (4 findings, last touched 2026-06-23 — the only
recently-live file in the group) appears to carry casing/terminology rules that Sprint 1
declared belong **only** in `documentation-voices-catalog.md`. If that holds, it is a
**competing canon home** — a D1-class defect in a live file, which is the exact failure mode
Sprint 1 existed to end, sitting just outside the glob. That one may deserve promotion out of
this punch list into a sprint. Verify by reading it against the catalog; do not conclude from
the finding count.

**Why deferred:** the release goal is repaired *documentation*. The standards tree is
authoring infrastructure — a defect there misdirects future writing but does not appear in
any shipped PDF. Descriptors were taken because `document-audit` resolves per-manual overlays
from them, so a descriptor defect misdirects the audits that gate the releases themselves.

---

## Extraction-era standards-tree cleanup — OPEN

**Status:** ⏳ Open — deferred 2026-08-15 by Stephen's decision. The whole archive effort is
parked as inappropriate to the release-repaired-documentation goal. **One carve-out is flagged
below and still needs a call.**

Six files in `engineering/standards/documentation-standards/`, all last touched **2025-09-01**,
all left over from the extraction era. Verified 2026-08-15 by reading the referrers, not by
counting them:

**Confirmed orphaned — referenced only by records-*of*, never consumers-*of*** (the ingestion
extraction index, the Sprint-2 plan that flagged them, a 2025 work-session summary, and
Sprint 1's closeout):

- `pasm2-manual-style-guide.md`
- `smartpins-style-guide.md`
- `pasm2-spreadsheet-style-guide.md`
- `style-guide-extraction-tasks.md` — zero referrers
- `documentation-generation-planning.md` — zero referrers
- `instruction-documentation-template.md` — zero referrers

Disposition when scheduled: relocate to the gitignored local archive per
[[feedback_archive_retired_docs_locally]]. Archiving them changes **nothing measured** while
the glob covers descriptors only — the standards tree is not scanned, so there is no baseline
benefit. This is pure tree hygiene and was correctly deferred.

**⚠ CARVE-OUT — `desilva-style-guide.md` is not an orphan, it is a stale fork.** This one is
a different class from the other six and is the reason this entry is worth re-reading rather
than batch-archiving later:

- `standards/documentation-standards/desilva-style-guide.md` — **207 lines**, referenced by
  exactly one 2025 history file.
- `manuals/p2-pasm-desilva-style/desilva-style-guide.md` — **282 lines**, the live one. Cited
  by that manual's `MANUAL-DESCRIPTOR.md` (`style_guide:`) and load-bearing in the
  `voice-guide.md` Sprint 1 authored (it carries the R4 REJECT rationale). Already inside the
  instrument's glob.

Different content, same filename, and the manual is **released**. The live pointers are
relative and resolve correctly, so nothing is broken today; the exposure is a filename lookup
finding the stale 207-line copy first. That is not hypothetical for these specific materials —
this project has already been bitten by superseded DeSilva copies
([[reference_desilva_masters_current_source]]: `archived-2025/` and `.backup` poison). Cost to
close is a single `git mv` to the archive. **Stephen's call whether it rides with the rest of
this entry or gets pulled forward.**

---

## Platform-migration doc drift (cross-manual) — OPEN

**Status:** ⏳ Open — surfaced 2026-06-25 during the assembly-manual v3.1.0 dead-filter cleanup.

The 2026-06-10 platform migration retired the bespoke `p2kb-<slug>-{foundation,content}.sty`
forks and the per-manual fork Lua filters in favor of the shared `p2kb-platform-*` stack, but
several docs still reference the retired fork pipeline as if it were current:

- **`methodology/manual-production-working-set.md`** (~L111–122) — the "parts" coverage table
  lists fork filters/sty for **assembly, iosp, and streamer** (`p2kb-pasm2-pagination.lua` /
  `p2kb-pasm2-content.sty`, plus the iosp/streamer equivalents). Reconcile each migrated
  manual's row to its current platform pipeline (or its surviving local overlay).
- **`manuals/p2-single-step-debugger-manual/creation-guide.md`** (~L100) — uses a now-removed
  `workspace/p2-assembly-language-manual/filters/p2kb-pasm2-code-coloring.lua` path as an
  example; repoint to a current filter.
- **General sweep:** grep the doc tree for retired `p2kb-<slug>-{foundation,content}.sty` and
  per-manual fork-filter names across **all** migrated manuals (not just assembly) and
  reconcile any *current-state* claims to the platform stack. Leave dated snapshots and
  "adapted from …" provenance comments frozen — they correctly describe a past state.

**Routing note:** manual-specific instances of this drift are tracked in the relevant manual's
own punch list (e.g. the assembly manual's `TEMPLATE-THEORY-OF-OPERATIONS.md` rewrite and
`style-guide.md` §7.4.2 filter-name fix live in
`workspace/p2-assembly-language-manual/PUNCH-LIST.md`).

---

## IOSP Ch. 16 — scope-mode / Goertzel completion (deferred enrichment) — OPEN

**Status:** ⏳ Open — surfaced 2026-06-27 during the ADC-foundation enrichment audit
(P2AN001 instrumentation-ADC work). Deliberately **carved out** of that enrichment because it
belongs to the GETSCP scope-window mechanism, NOT the SINC-ADC spine being enriched now.

IOSP Chapter 16 §16.5 (smart-pin mode %11010, ADC scope-with-trigger) is documented at a
"simplified" level (Titus cross-audit). Complete later:
- Scope-mode **filter-type selector** bits (Tukey 68-tap / 45-tap, Hann 28-tap).
- Full **scope capture sequencing** (SETSCP / SETXFRQ / XINIT / XSTOP).
- The **GETSCP window-overlap ENOB** technique (TonyB_ sub-thread) — see
  `app-notes/P2AN001/research/improved-adc-pin-techniques/STUDY-improved-adc-pin-techniques.md` §B9.

Not blocking the ADC-foundation enrichment or the P2AN001 app note.

---

## Legacy backup artifacts — disposition pending — OPEN

**Status:** ⏳ Open — surfaced 2026-08-08 during the backup-convention overhaul
(`engineering/standards/BACKUP-CONVENTION.md`, commit `c3c7366f`).

That sweep relocated **532 files / 57 MB** of mechanical backups into `.backups/`.
Four artifacts were **deliberately left in place** because they are not mechanical
clutter and deleting or moving them is a judgement call, not a cleanup.

**1 — Incident salvage (untracked, left in the tree).** Deliberate archive, not prune:

- `engineering/document-production/pipelines/backups/pdf-generation-guide-RECOVERED.md.backup.20250820_212847`
- `engineering/pipelines/backups/pdf-generation-workflow-v2.md.backup.20250821_191710`
- `engineering/pipelines/backups/pdf-workflow.md.backup.20250821_191500`

Dated the night of the **2025-08-21 loss of 3300+ lines of PDF-generation
documentation** — the incident that created Sacred Rule #1 — and one is named
*RECOVERED*. These look like the salvaged artifacts of that loss. They are
untracked, so deletion would be unrecoverable. Decide where they belong (a
deliberate archive under `engineering/history/`?) rather than letting a future
prune take them.

**2 — Tracked backup files (repo content, not clutter).** Moving these is a repo
change, so they were left alone:

- `engineering/document-production/manuals/p2-pasm-desilva-style/opus-master/COMPLETE-OPUS-MASTER-backup-2025-12-06-pre-backport.md`
  — sitting **in the DeSilva master folder**, which is exactly the adjacency the
  new convention exists to prevent. It has already caused a wrong-source
  incident, and during this very sprint a first-match glob in the new license
  gate selected *it* instead of the real master. Git preserves its content, so
  removing it from the working tree is safe whenever the call is made.
- `engineering/history/sessions/SESSION-END-BACKUP-20250825.md` — reads as a
  session history document that merely has "BACKUP" in its name. Probably keep
  as-is; confirm and leave.

Not blocking anything. The convention and its gate are in place; this is only
the disposition of what predates them.

---
