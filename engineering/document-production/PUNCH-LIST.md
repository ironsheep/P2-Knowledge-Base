# Document Production — Punch List

Cross-cutting document-production cleanup items that are **not** specific to a single
manual. Per-manual items live in each `workspace/<slug>/PUNCH-LIST.md`.

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
