# Document Production — Punch List

- **`enhance_smartpins_context_from_docx.py` is dead code** — OPEN. `engineering/tools/extraction/enhance_smartpins_context_from_docx.py` (174 lines) hardcodes `/Users/stephen/Projects/...` absolute paths that do not exist in the devcontainer, so it cannot run here. It also does not parse DOCX despite its name — it reads an already-extracted text file. Noticed 2026-08-26 while checking for reuse before writing `docx_walk.py`. Decide: repath it, or retire it to `archive/`.

Cross-cutting document-production cleanup items that are **not** specific to a single
manual. Per-manual items live in each `workspace/<slug>/PUNCH-LIST.md`.

**This file is also the home for pending PLATFORM DECISIONS** — a proposed change to the
shared `p2kb-platform` stack that is waiting on Stephen's approval. Those used to be recorded
in prose inside whichever document surfaced them (a footnote in
`PLATFORM-FEATURE-ADOPTION.md`, a status line in `P2KB-CORRECTION-FINDINGS.md`), where nothing
re-read them. **A decision nobody is holding is a decision that never gets made.** Every
heading here ends in its own state (`— OPEN` / `— RESOLVED <date>`), so this file needs no
summary table to stay honest — deliberately, because a hand-maintained status index is the
very drift this list already tracks twice.

**Scope note:** the **P2 Layout Torture Test** is an internal test instrument — never released,
not consistency-bound, serving the layout-standards effort rather than the community. Items
about it are housekeeping and **never** gate a publication or hold a correction finding open.

---

## Review ALL manual content against the YAML-fidelity release — OPEN

**Status:** Open — raised by Stephen 2026-08-25, **owed AFTER that release ships**, not before.
Deliberately deferred: the release is being reviewed and shipped first, and the manual sweep is a
separate pass so it is not rushed alongside it.

**Why it is owed.** The `yaml-fidelity` sprint rewrote the shipped KB on a scale that has no
precedent here — every uncited quantitative block removed and then repopulated source-first, 55
constants defined that the set used and defined nowhere, and a class of mislabel corrected that
had been in the KB for months. **The manuals were authored against the KB as it was.** Anywhere a
manual repeats a fact that changed, it is now wrong, and nothing in the release path checks that.

**The specific class already proven, so this is not speculative.** Plan §3 excluded manual prose
from this sprint on the strength of a 2026-08-24 sweep that reported the masters clean. **That
measurement is false and is filed as F-356.** The IOSP master is split per chapter under
`part-*/` directories, and a flat glob misses it; searching recursively finds **23 mislabel lines,
5 "internal pull-up" assertions, and four sites teaching `WRPIN(pin, P_HIGH_15K | P_LOW_FLOAT)`** —
a composition no Parallax source states, which the KB has now removed but a published manual still
teaches. If the sweep was wrong about the manual it was most likely to be wrong about, it is not
evidence about the other eleven.

**What the review must cover** — the KB changes a manual could be repeating:

| Class | What changed in the KB | Where a manual is likely to repeat it |
|---|---|---|
| Drive strength vs bias resistors | `P_HIGH_*`/`P_LOW_*` are drive-strength selectors; the P2 has **no** pull-up/pull-down resistors, and a drive is inactive while `DIR` is low | any I/O, button, or open-collector discussion |
| The `P_HIGH_15K \| P_LOW_FLOAT` idiom | removed — it is **our** invention, not a Parallax statement | weak-pull-up examples |
| Absolute-max pin current | `150mA` deleted; the datasheet says **±30 mA** | LED and series-resistor worked examples — **this one damages hardware if repeated** |
| `WAITMS`/`WAITUS` bounds | the real limit is `$8000_0000` **clocks**, not a fixed millisecond ceiling | delay/timing examples |
| PLL lock time | settled at **10 ms**; the µs figure has no source | clock-setup sequences and their `WAITX` operands |
| Board facts | part numbers, dimensions, connector types and pin maps re-derived from the guides; **#64006G is the Goertzel board**, not a digital-I/O board | board-specific chapters and getting-started material |
| Source errata | `SOURCE-ERRATA.md` now records where a Parallax document is itself wrong — a manual may have faithfully repeated one | anywhere a guide was the cited source |

**Do not run this as a grep sweep alone.** The mislabel survives in prose that never names a
constant — *"activate the pull-ups"*, *"the internal resistor holds the line"* — which is how
E-010 stayed invisible to both instruments. Read the chapters that teach these subjects.

**Where the truth now lives**, so the review has one place to check against:
`deliverables/ai/P2/architecture/pin-drive-configuration.yaml` (field, ladder, DIR/OUT rule, the
two verified idioms) · `deliverables/ai/P2/language/spin2/symbols/spin2-builtin-symbols-complete.yaml`
(all 116 constants, one definition each) · `engineering/ingestion/SOURCE-ERRATA.md` (where a source
is wrong and what is true instead).

**Related:** F-356 (the falsified sweep) · F-322 (the idiom's corrected attribution) · E-004, E-006,
E-010 (source errata a manual may repeat).

---

## Shipped example `.spin2` files conflict with the Spin2 authoring gate — RESOLVED 2026-08-18

**Resolved by generating the header rather than exempting the file** (Stephen's call). The
collision was real: guide §4.2/§4.2.1 require a file header and licence footer on every
`.spin2`, and each example must also be byte-identical to the listing printed in its manual,
which ~20 lines of boilerplate cannot be. The way out was to stop hand-maintaining the half
that conflicts.

**The mechanism.** `engineering/tools/sync-manual-examples.py` generates each example's header
from what the repo already knows — manual, version, dates, and **where in the manual the block
sits, read back out of its enclosing heading**. The identity gate moves from *whole file* to
*file body*, so the reader promise is unchanged. `verify-example-corpus-identity.py` was
extended (not forked) to strip a generated wrapper before comparing; a file without one is
compared whole, exactly as before. `Purpose` is the only hand-authored field, kept in
`examples-library/PURPOSES.md`; the tool refuses to invent one.

Deriving the location is what settles the "isn't that hard to maintain?" worry: a chapter that
moves is absorbed by the next sync. This manual renumbered six chapters the same day, which is
precisely the case a typed citation gets wrong.

**Adoption is per-document, at each document's next release** — that is what keeps 12 published
corpora from being churned to fix one. Adopted so far: `p2-xbyte-programming-guide` (2026-08-18,
3 files). Streamer is next. Both gates are wired into `prepare-manual`'s overlay; un-adopted
documents print `INFO: ... has not adopted` and pass.

**Two things this surfaced,** both recorded below rather than folded in silently.

---

## App-note example corpora have never been gated at all — OPEN

**Status:** Open — found 2026-08-18 while wiring the example-corpus gates. **Pre-existing**;
nothing to do with header adoption.

`verify-example-corpus-identity.py` pairs a loose `examples-library/*.spin2` to its printed
listing by a fence caption, ```` ```{.spin2 caption="<name>.spin2"} ````. **The seven app notes
carry no captioned fences anywhere** — they key examples to recipe IDs (`R1`, `R2`, …) in an
`examples-library/README.md` table instead. So the gate reports every app-note file as an
orphan and has never actually asserted anything about them:

| Document | Files | Gate result |
|---|---|---|
| P2AN001 · P2AN004 | 3 each | RED — all orphans |
| P2AN005 | 4 | RED — all orphans |
| P2AN003 · P2AN006 | 5 each | RED — all orphans |
| P2AN002 · P2AN007 | 6 each | RED — all orphans |

That is **32 files across seven published app notes** with no file-vs-printed-code check. All
six manuals are GREEN, so this is specifically an app-note-class gap.

**The decision to make:** adopt captions in the app-note masters (aligns the class with the
manuals, and is what the tools already expect), or teach the tool the recipe-ID convention
(cheaper now, keeps two conventions alive). Either way it wants doing before the next app-note
release, and it pairs naturally with that document's header adoption.

### MEASURED 2026-08-22 — the evidence points hard at captions

The bodies already agree. Comparing each corpus file against every printed `spin2` fence in
its own master: **31 of the 32 files are ALREADY byte-identical to a printed fence.** Nothing
has drifted; the only thing missing is the `caption="<name>.spin2"` attribute that lets the
tool see the pairing.

| Document | Files | Printed fences | Already byte-identical | Captions |
|---|---:|---:|---:|---:|
| P2AN001 | 3 | 8 | 3 | 0 |
| P2AN002 | 6 | 7 | 6 | 0 |
| P2AN003 | 5 | 7 | 5 | 0 |
| P2AN004 | 3 | 3 | 3 | 0 |
| P2AN005 | 4 | 4 | 4 | 0 |
| P2AN006 | 5 | 6 | 4 + 1 utility object | 0 |
| P2AN007 | 6 | 7 | 6 | 0 |
| **Total** | **32** | **42** | **31** | **0** |

So "adopt captions" is a **pure annotation task** — 31 fence attributes, no code moves, no
reformatting — and it converts a RED gate to GREEN without touching a shipped byte. Teaching
the tool recipe IDs would keep a second convention alive to describe files that already match
the first one.

**A trap for whoever does this.** Do NOT reach for `build-example-library.py` on an app note
before its captions exist. Dry-run 2026-08-22 against P2AN003: the extractor found **zero** of
its six real examples and would have written an **empty** library over a good corpus. Until
captions land, repackaging goes through `build-example-library.py --repack` (added the same
day), which rebuilds the archive from the corpus on disk and refuses to write an empty one.

**Not blocking the ZIPs.** Published-archive currency is a separate axis and is now GREEN for
all 12 documents (2026-08-22) — this gap is about the file-vs-printed-code assertion only.

**Note:** `P2AN006/examples-library/isp_stack_check.spin2` is a shipped **utility object**, not
a manual example — it already carries its own hand-written §4.2 header. Whatever convention is
chosen must let a corpus hold a non-example file without flagging it.

---

## Certify the Forge — torture-test the F-286 escaping invariant — OPEN

**Status:** ⏳ Open — queued 2026-08-17 (Stephen's call). **Deliberately sequenced AFTER** the
current release flight (the four manuals) and after Debug Window 1.1.3 + IOSP 1.0.9 reach PDF.
Not a blocker for any of those.

**What it is.** F-286 fixed five filter sites that emitted `stringify()`'d text into raw LaTeX
without escaping. Every one was measured **inert on today's content** — no live Part title, figure
caption, or sidetrack title contains `&`, `%`, `#`, or `_`. That is exactly why a production render
cannot validate the fix: there is no content to trigger the path. A render proves *no regression*;
it cannot prove the escaping works.

**The work.** Add positive cases to the **P2 Layout Torture Test** (`workspace/p2-layout-torture-test`),
which already carries 3 Part headings and 5 figure captions and exists for precisely this purpose:

| Case | Where | Must render as |
|---|---|---|
| `&` in a Part title | `# Part N: Boxes, Whitespace & Pagination` | `\manualpart{}` prints the ampersand |
| `&` and `_` in a figure caption | a `figurecaption` div | `\caption{}` prints both literally |
| `%` in a caption | a `figurecaption` div | text after the `%` still appears |

Each case **cannot render before the fix and must render after** — that is what converts "measured
inert" into "demonstrated working." Run through `forge-test` (interactive daemon store, so it never
touches the manual store and has no release consequences).

**Coverage this does NOT reach, and why:**
- **Sidetrack title** (`\addcontentsline`) — deSilva is the only consumer; covered by its release render
  as a no-regression check only.
- **Modecard title** — IOSP is the only consumer. The change there was a rebinding to a hoisted
  helper with an identical body, so risk is minimal, but it is unexercised until IOSP renders.
- **`tables.lua` `stringify` fallbacks (×4)** — unreachable by any render by construction: they fire
  only when `pandoc.write` fails. Code review is the only available check, and it is done.

**The `breaklines` platform fix is NOT part of this — it was REJECTED 2026-08-17.** It was tested on
the daemon and the render disproved it: a typeset wrap emits a comment continuation with no `'` and a
statement continuation with no Spin2 `...`, so it prints wrong-looking code that copies as broken, and
it removes the pressure to fix the source. Code boxes do not wrap — that policy is declared in
`p2kb-platform-code-coloring.lua`'s header and in `audit-code-line-length.py`. Over-long lines are an
authorship defect, and the enforcement mechanism is the gate, which F-289 repaired (it had been
skipping every captioned block). Details in F-281.

---

## A hand-named backup lives inside deSilva's `opus-master/` and is tracked — OPEN

**Status:** ⏳ Open — found 2026-08-16 by «#222»'s F-254 class sweep, **not fixed** (deleting tracked
content is not a correction task's call).

`manuals/p2-pasm-desilva-style/opus-master/COMPLETE-OPUS-MASTER-backup-2025-12-06-pre-backport.md`
— 65 KB, mode `444`, **tracked in git**, sitting in the content directory.

**Two problems, and the second is the live one:**
1. It violates the backup convention (`engineering/standards/BACKUP-CONVENTION.md`, Sacred Rule #1):
   backups are made by `engineering/tools/backup-file.sh` and land in `.backups/`, **never**
   hand-named beside the file they copy.
2. **It is sweep poison.** It carries the pre-repair F-254 text verbatim — the "shoulders of giants"
   opener, the generic `Technical Reviewers` placeholders, and the false *"trained on deSilva's
   writing style"* line. Every class sweep over `manuals/**` hits it and has to re-adjudicate it as
   a false positive. This sweep did; the next one will too. It is the same failure shape as the
   P2AN001 fan-out audit file that seeded F-269 — an inert artifact that reads as live evidence.

Not assembled into the render (the workspace README names `COMPLETE-OPUS-MASTER.md` as the sole
content source), so nothing ships from it.

**When worked:** confirm nothing references it, then remove it from the tree — the git history *is*
the backup, which is the whole point of the convention. Check the other manuals for the same shape
(`archived-2025/` and `initial-chapter-generation/` under deSilva are known-inert and are
deliberately retained; this one is not in that category).

---

## IOSP joins two mutually exclusive smart-pin modes with `+` (two tables) — OPEN

**Status:** ⏳ Open — found 2026-08-16 by «#220»'s class sweep, **deliberately not fixed** (IOSP is
out of the Sprint-2 release wave, and «#220» is scoped to the Streamer Guide).

Two IOSP tables read `P_PERIODS_HIGHS + P_PERIODS_TICKS`:
- `part-5-appendices/appendix-d-mode-comparison-charts.md:119` — *"Duty cycle | … | Both measurements needed"*
- `part-3-input-modes/chapter-15-period-frequency.md:19` — *"Duty cycle | … (or the time-window pair)"*

**Why it is a defect and not just loose typography.** These are two **mutually exclusive smart-pin
modes** in the `%SSSSS` field — `P_PERIODS_HIGHS` is `%10100`, `P_PERIODS_TICKS` is `%10011`
(`architecture/smart-pins/smart-pin-10100-*.yaml` / `-10011-*.yaml`). They cannot be combined at
all: `+` on them produces a third, wrong mode value. The cells *mean* "you need both measurements"
— run both, on two pins — and the surrounding words support that reading, but the `+` sits between
two mode constants in a table a reader scans for composable syntax.

**It is the same class as F-259**, whose rule now ships in the Streamer Guide §13.4 ("Combine
pin-mode constants with `|`, never `+`"): a reader taught that constants compose will read this as
composition. Here the honest fix is **not** `|` — these do not compose either. Use prose or "and"
so the cell stops looking like an expression.

**When worked:** re-check the whole IOSP mode-comparison appendix for the same shape, and confirm no
other manual pairs two mode constants with an operator. Ships with IOSP's next release; no bump is
owed for it alone.

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

---

## The corrections register has no machine-readable status — OPEN

**Status:** ⏳ Open — diagnosed 2026-08-17 during «#235» wave prep, when Stephen asked how many
findings we are losing by deferring them. **The answer was not a backlog; it was worse.**

**The measurement.** 37 findings in `engineering/operations/P2KB-CORRECTION-FINDINGS.md`. Completion
state is recorded in **four incompatible notations** and sometimes not at all:

| Where | Examples |
|---|---|
| A tag in the `###` title | `CONFIRMED` · `OPEN` · `DONE (2026-08-16)` · `NEEDS-VERIFICATION` · `NOTED` |
| Inline bold prose | `**RELEASED**` · `**APPLIED**` · `**KB APPLIED**` · `**FIXED**` · `**RESOLVED**` · `**MANUAL HALF APPLIED**` |
| A `**Status:**` line | F-271 only |
| Nowhere | 18 of 37 |

**It is wrong in both directions, which is the actual danger.** Of the 18 unmarked findings, four were
spot-checked against the artifacts — F-254, F-255, F-256, F-257 — and **all four were already fixed**.
Meanwhile F-262 reads `RELEASED` but ships in v1.1.3, which has not shipped. So the register
simultaneously hides completed work and claims work that has not gone out.

**`MANUAL HALF APPLIED` is the worst offender** and cost real time in this very audit: it reads as
"half done" and actually means *the manual half of a two-half KB+manual fix was applied*. Three
Streamer findings carry it (F-259, F-260, F-266) and all three are complete.

**Consequences, in order of severity:**

1. **The drain gate cannot run.** `document-audit` claims to own a YAML-HEAD drain gate — *"no publish
   while actionable corrections are pending."* Pending is not determinable without re-reading 37 prose
   blocks, so the safety net meant to catch exactly this worry **is not armed**.
2. Answering "what is outstanding?" costs a full re-read, so nobody does it routinely.
3. Genuinely deferred work looks identical to finished work.

### ⏳ HALF DELIVERED 2026-08-19 — the validator exists; the vocabulary refactor does not

**The validator asked for here is built:** `engineering/tools/validation/audit-register-hygiene.py`.
It mechanically detects the exact four-notation problem measured above — every finding carrying **no
status token**, and every finding whose **prose claims "fixed" while its status token does not**
(the `MANUAL HALF APPLIED` / `**FIXED**` class that cost real time in the 08-17 audit). It also
enforces the rules the register states about itself: no duplicate IDs, counter ahead of every
allocation, no closed finding left in an open-work file, archives resolve, and **no allocated ID
missing from live + archives**.

**The measurement has moved a long way.** 2026-08-17: *18 of 37 findings unmarked*. 2026-08-19, run
mechanically: **2 of 43** — `F-272` and `F-203`. Those two are the whole remaining gap, plus one
**off-legend** status (`F-256` reads `RESOLVED`, which is not among the register's seven declared
statuses). The 18 shrank because the wave added statuses as it drained findings, and the four
spot-checked here — F-254, F-255, F-256, F-257 — are all now closed and archived.

**What is still owed, and it is the harder half:**
1. **One `**Status:**` line per finding, fixed vocabulary** — `OPEN` · `FIXED-UNRELEASED` ·
   `RELEASED` · `BLOCKED-ON-EVIDENCE` · `PUNCH-LISTED` · `UNVERIFIED`. The tool currently reads the
   status wherever it sits (title tag or prose) because that is what the register does today; a
   single canonical location would let it stop guessing. **Mark `UNVERIFIED` wherever the state is
   not actually checked against the artifact** — a confidently wrong status is the same trap in a
   new costume.
2. **Print the open set, and wire it to the drain gate.** The tool reports violations, not the open
   worklist, so `document-audit`'s YAML-HEAD drain gate — *"no publish while actionable corrections
   are pending"* — **is still not armed**. That was consequence #1 above and it stands.
3. **Give F-272 and F-203 a status**, and flip F-256 onto the legend.

**Original fix statement, retained:** one `**Status:**` line per finding, fixed vocabulary — `OPEN` ·
`FIXED-UNRELEASED` · `RELEASED` · `BLOCKED-ON-EVIDENCE` · `PUNCH-LISTED` · `UNVERIFIED` — plus a small
validator that prints the open set and can be called by the drain gate. **Mark `UNVERIFIED` wherever the state is not
actually checked against the artifact**; a confidently wrong status is the same trap in a new costume,
and this register already teaches that a status line is not evidence.

**Deferred deliberately, not forgotten** — the goal right now is released PDFs, and this is a register
refactor that touches 37 entries and gates nothing in the current wave (that cross-reference was run
first: see the wave audit below). It should run **before the next audit cycle**, not before this
release.

**Verified consequence for the current wave: none.** All 37 findings were cross-referenced against the
seven wave elements on 2026-08-17. Exactly two touched them and both were dealt with — F-281 (Debug
Window, blocking, evidence-blocked) and F-224 (Assembly, fixed into v3.1.6 that same day).

---

## Inline-code URLs cannot break often enough and overhang the right margin — OPEN

**Found** 2026-08-18 during the XBYTE v1.1.0 draft render, by
`audit-pdf-margin-overflow.py`. **Pre-existing, not a regression** — the identical
span with the identical overhang is present in the released v1.0.1 PDF (p93 there,
p107 in the draft), so it has shipped to readers once already.

**The measurement.** `https://github.com/parallaxinc/propeller`, set as inline code in
XBYTE §C.1, ends at x=573.1pt against a 540pt text-block edge on 612pt paper. It
intrudes 33.1pt into the 72pt right margin. It is **not** cut at the paper edge, and
the URL does wrap — but the first fragment overhangs the body text visibly. A second
URL in §C.2 overhangs 18pt, under the gate's 20pt tolerance, so the gate reports one
span while two are actually leaning out.

**Why it is not a local text fix.** Inline code has no hyphenation and breaks only at
`/`. The line-breaker took the last available `/` rather than an earlier one that
would have fit. Any fix by rewording — dropping the `https://` scheme, shortening the
lead-in prose, moving the URL later in the sentence — depends on where the line
happens to wrap, so it can pass today and fail after any edit above it. Dropping the
scheme would also break the house form: every other URL in Appendix C is a full
`https://` inline-code span, and one bare exception reads as an error.

**The real fix is platform-level**: give inline-code spans more legal break points
(a discretionary after `//`, `.` and `/`), so a long URL breaks where it fits instead
of overrunning. That is a set-wide rendering change — it changes line breaks in every
manual, so it wants the set-wide scheduling rule: land it when no manual is mid-render,
adopt per manual at its next natural render, and look at re-flowed pages rather than
the log.

**This is NOT the rejected `breaklines` change, and must not be used to reopen it.**
The code-box no-wrap policy exists because a typeset wrap cannot emit a comment's `'`
prefix or a Spin2 `...` continuation, so wrapped *code* prints wrong and copies as
broken (F-281, rejected 2026-08-17). A `https://…` URL inside a prose sentence has
neither of those properties: breaking it after `/` is ordinary typography and copies
back correctly. The scope here is **inline spans in prose only** — nothing inside a
code box.

**Scheduling.** It stands alone now. This item previously read *"Do it with «#250»,
not before"*, pairing it with the fancyvrb `breaklines` work — a task that had already
been rejected when that text was written. **Corrected 2026-08-19.** Its natural
partners in one `forge-test` sweep are F-300 (PDF Title/Author metadata) and, as
polish, F-299 (6-column table overhang).

**Verify when done:** `audit-pdf-margin-overflow.py` reports zero spans on the XBYTE
PDF, and the §C.1 and §C.2 URLs both sit inside the text block with their breaks at
sensible boundaries.

---

## Pending platform decision — teach the cross-ref filter to treat `SoftBreak` as `Space` — RESOLVED 2026-08-23

> **✅ APPROVED (Stephen) AND LANDED 2026-08-23, same day it was surfaced.** The filter accepts a
> Space **or** a SoftBreak between the keyword and its number. **Proven by a before/after
> round-trip on the interactive daemon, measured on the artifact, not asserted:**
> `crossref-softbreak-v1` (before) linked **3 of 6** — every line-wrapped reference dead;
> `crossref-softbreak-v2` (after) linked **6 of 6**, each to the correct target, while **both
> negative controls** (`Chapter 99` plain, `Chapter 98` wrapped — headings that do not exist)
> **stayed plain text**. That second half is the one that matters: the new branch still honours
> the target-must-exist rule. Compile log clean; rendered page inspected and **visually
> unchanged**.
>
> **Whole-corpus re-sweep at landing: ZERO wrapped-reference sites in any manual or app note** —
> a pure no-op today, no re-render debt for any document. It is preventive, not corrective.
> **Adoption remains per manual at each one's next release** (Stephen's direction); nothing is
> re-rendered for this.
>
> **The fixture is TRACKED so the proof outlives the run:**
> `engineering/document-production/platform/tests/crossref-softbreak-test.md`, with its README
> giving the eight cases, the expected 6-link result, and how to re-run it. The daemon runs
> themselves (`interactive-testing/test-runs/crossref-softbreak-v{1,2}_*/`) are **git-ignored
> and expire in 7 days** — which is exactly why the fixture was promoted out of there. A
> platform change is permanent; the evidence it works has to be at least as durable.

*Original entry retained below for the record.*

**Status:** ~~⏳ Open~~ — **Stephen's call, never put to him.** Recommendation raised 2026-08-23 during
the PNut-Term-TS User Guide's cross-ref adoption; recorded until now only in footnote ⁶ of
`PLATFORM-FEATURE-ADOPTION.md`, which is prose nobody re-reads. **That is why it is here** — a
pending *platform* decision needs a home in a list, not a footnote inside a per-feature matrix.

**The mechanism.** `p2kb-platform-crossref.lua` matches `Chapter` + *Space* + number. When an author's
source wraps a reference across a line —

```
...configures 8N1 exclusively (Chapter
7), and 300 baud is...
```

— pandoc emits `Str "(Chapter"` · **SoftBreak** · `Str "7),"`. A SoftBreak is not a Space, so the
reference is invisible to the filter and simply does not link.

**Why it matters more than one missed link.** **The failure is SILENT** — nothing in the build reports
a reference that failed to link. The PNut-Term-TS guide rendered 26 of 27 and the miss was found only
because the adoption audit counted them. Any adopting manual can lose links this way, invisibly, and
the trigger is *source line-wrapping* — something an author cannot see and has no reason to think about.

**Not a filter bug.** The filter matched what it was told to match; the source shape changed. Fixed in
that manual by reflowing the paragraph, which then read 27 of 27.

**Cost of doing it: measured, and it is zero.** All four adopted manuals were swept for the pattern —
**zero occurrences elsewhere**, so the change is a **no-op for every adopted document today** and
carries **no re-render debt**. It was deliberately not smuggled into a manual's release, because a
platform change belongs with a platform decision.

**The ask:** approve the filter change, then it lands on its own and any future adopter is robust to
rewrapping.

---

## Layout Torture Test instrument — stale `\DiagRgbFormats` clone — OPEN (housekeeping)

**Status:** ⏳ Open, **low priority, not a correctness finding and not a release gate.** The P2 Layout
Torture Test is an **internal test instrument** — never released, not consistency-bound, serving the
manual layout-standards effort rather than the community. It is recorded here so the item is not lost,
**not** because anything is owed to a reader.

`workspace/p2-layout-torture-test/templates/p2kb-torture-diagrams.sty:176` still draws
`R 2 | G 2 | B 2 | I 2`, the RGBI8 field split that **F-303** established is a fabrication (the format
is a 3-bit colour select + 5-bit luminance, Silicon Doc `p2-documentation.txt:3800`). The macro is
invoked at `P2-Layout-Torture-Test.md:836`, so the wrong diagram renders into every torture-test build.
A copy of the macro is also staged at `pdf-forge/interactive-testing/templates/p2kb-torture-diagrams.sty:161`.
**The published half of F-303 is closed** — both live-KB sites and the Assembly Language Reference
(v3.1.7, read on p475) are corrected; this instrument copy never gated that and F-303 no longer carries it.

**The origin is worth keeping:** the correct macro lives in
`workspace/p2-streamer-programming-guide/templates/p2kb-streamer-diagrams.sty` and was fixed there.
The torture-test file is a **copy-paste clone** of it, which is how one wrong diagram became two.
If these diagram macros are ever promoted into the shared platform stack, the duplication goes away by
construction — worth considering when the platform diagram set is next touched, but **not** work to
schedule on its own account.

---

## A status line that encodes a FUTURE release event goes stale silently — OPEN

**Status:** ⏳ Open — diagnosed 2026-08-23, and it is the **root cause of a real rediscovery cost**
paid that day. Companion to *"The corrections register has no machine-readable status"* above; that
item's owed work does **not** cover this case.

**What happened.** `#288`'s whole substance — the Streamer/Assembly co-release decision and both
releases — completed 2026-08-22. On 2026-08-23 the state had to be **reconstructed from `git log`, the
roster's PUBLISH prose, and a live `grep` of the KB**, because no register said so plainly. Specifically
**F-302** still read `PARTIAL … the manual half ships with Streamer v1.1.0` — after v1.1.0 shipped.

**Then the class was swept, and it was not one entry — it was three, drifting in BOTH directions:**

| Finding | Said | Actually | Direction of the lie |
|---|---|---|---|
| **F-302** | `PARTIAL … ships with Streamer v1.1.0` | v1.1.0 shipped 2026-08-22; fully resolved | **understates** — sends you to redo finished work |
| **F-279** | `CONFIRMED` · `NOT RELEASED … ships in v1.0.2` | fixed in the v1.1.0 restructure, shipped 2026-08-19 | **understates** — a *closed* finding read as open for four days |
| **F-276** | `NOT RELEASED … ships in v3.0.6` | v3.0.6 **published 2026-08-17**; defect still open | **overstates safety** — a flawed argument was in a released manual while the register said it was not |

**F-276 is the dangerous one.** The other two waste time; that one **understated the blast radius of a
live defect in a shipped PDF.** And F-279 shows the compounding case: its fix rode a *restructure* that
renumbered the target version (v1.0.2 was never published — v1.1.0 was) **and** invalidated the line
number the finding was pinned to, so the entry became uncheckable from both ends at once.

**This is the fourth recorded instance of the family.** F-278 already carries the same correction in its
own body — *"This annotation used to read `(NOT RELEASED, v1.0.9)` … and all three were stale … the
record understated what had been done, so a reader is sent to redo finished work"* — and it names this
same tool gap explicitly. A defect class that has now been hand-corrected four times is a defect in the
process, not in four entries.

**Why the validator did not catch it, and this is the point.**
`audit-register-hygiene.py` reports **CLEAN** on this register (44 live IDs, 0 unaccounted, no
status/prose conflict). It cannot catch this class:

- The status token said `PARTIAL` and the prose said *"ships with v1.1.0"* — **future tense**. There is
  no contradiction *at the moment of writing*; the entry becomes false later, when the event occurs.
- A status containing a **promise about a version** has an implicit expiry that nothing watches. The
  register has no link from "finding F-302" to "release v1.1.0 happened."

**The general defect:** *a status line that describes a future event is correct when written and wrong
forever after, and no hygiene rule that compares a finding against itself can see it.*

**Consequence measured, not assumed:** a completed task read as open at session resume, and closing it
required a full re-derivation from primary artifacts.

**Proposed fix** (small, and it fits the existing tool):
1. **Ban the shape.** No status may name an unshipped version as its completion condition. Use
   `FIXED-UNRELEASED` + a `ships-in:` field, which is a *fact* about the fix, not a *prediction*.
2. **Teach `audit-register-hygiene.py` a release cross-check** — for every finding carrying
   `ships-in: vX`, if the roster shows `vX` PUBLISHED, flag the finding as **status-expired**. This is
   mechanically checkable today: the roster's Freshness Ledger already carries dated `PUBLISH` lines.
3. Run it as part of `release-manual`, so **shipping a release is what re-reads the findings that named it.**

This closes consequence #1 of the companion item from a different direction: rather than printing the
open worklist, it makes the register *notice* when the world moved past one of its claims.

---

## Retire `changelog-style-guide.md` once central authors the Class 3 profile — OPEN

**Raised 2026-08-23** by the v8→v9 overlay reconcile, per central adoption action **v9(a)**.

`engineering/document-production/methodology/changelog-style-guide.md` is **retained
deliberately** and must not be deleted as a redundant copy of `central:changelog-voicing`.
The reason is recorded in `.claude/skill-conventions.md` as a second `CONFORMANCE_GUIDES`
row: central's guide fully authors changelog classes 1 and 2, and leaves **class 3
(Published document)** — this project's class, for every manual and app-note CHANGELOG —
declared in its own §5 as `Status: unauthored stub`. Deleting the local file would leave
every manual CHANGELOG governed by three sentences.

This is central's *partial coverage* case, not a fork. The guide's own class section is
the authority for whether it applies, so the call is mechanical rather than a judgement
someone has to re-make each time.

**Two pieces of work, in order:**

1. **Trim the local guide to central's complement** — delete the sections central §1–§4
   already carry (prior-state ban, never-shipped versions, aggregate-into-themes,
   current-state language, the two-question gate, initial-releases-describe-the-document),
   leaving only the class-3 profile: the Part-based section structure, the entry-format
   catalog, and the length budgets. Two constraints on that pass:
   - **Four skills hard-depend on this file** — `audit-changelog` (5 references, including
     a hard-stop if the file is absent), `release-yamls`, `release-manual`, and the
     `prepare-manual` overlay. Every citation must still resolve afterward.
   - The guide layer is a **gated** surface — `DOC_AUDIT_COMMAND` must read 0 findings
     after the edit.
   Until this runs, the profile is silent on central §1.5's mandatory **theme line**; the
   `build-wrapup` overlay carries an expiring note covering the gap.

2. **Retire the file entirely** when central authors the Class 3 profile — move any genuine
   residue into the `build-wrapup` overlay first, then delete the file, drop its
   `CONFORMANCE_GUIDES` row, and repoint the four skills above.

**Trigger for step 2:** `~/.claude/skills-docs/guides/changelog-voicing.md` §5 Class 3 no
longer reads `Status: unauthored stub`. Nothing here is owed until then — but the local
guide is also the natural **source text** for that upstream profile, so proposing it is a
standing promotion candidate.
