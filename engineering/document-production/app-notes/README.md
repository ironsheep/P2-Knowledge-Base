# P2 Application Notes (`P2ANxxx`)

This folder is the repository for **all P2 application-note sources** — a third document
class alongside the manuals (`../manuals/`) and datasheets (`../datasheets/`).

An application note is **application-driven, single-technique, built around one complete
runnable example, and empirically grounded.** It is not a reference manual (it uses the
silicon rather than enumerating it) and not a tutorial (it assumes prerequisites and points
to the manuals for background). See the guides below for the full contract.

## The guides (read these first — they govern every note)

| Guide | Governs |
|---|---|
| **`APP-NOTE-CREATION-GUIDE.md`** | What an app note is, its canonical structure, the pedagogy behind it, sourcing & verification, naming/folder conventions |
| **`APP-NOTE-VOICE-GUIDE.md`** | How a note reads — the "guided application" register blend, markers, terminology |

## The series

| AN | Topic | Status | Notes |
|---|---|---|---|
| **P2AN001** | Single-Pin ADC Instrumentation | drafted v0.1.0 — *renumber from legacy `P2AN000` PENDING* | the foundational first note + exemplar; rests on the enriched I/O & Smart Pins User Guide Ch.16 |
| **P2AN002** | CORDIC for Real Work | committed — **next up** | lead of the Math family; numbered at production start |

> *Series starts at `001`, Parallax-style (no `AN000`); `P2AN000` was the experimental placeholder, now retired.*

> **The authoritative candidate register + production plan is the roster:**
> `engineering/analysis/p2-app-note-roster.md` (families, per-region IOSP/app-note
> boundary, disposition ledger, two-pipeline tracking model). Numbers are assigned
> at commit-to-production (per `APP-NOTE-CREATION-GUIDE.md` §6.1), so candidates
> stay named in the roster until they enter production.

## Where notes come from

The Parallax **P1 application notes** were ingested 2026-06-27 as pattern donors. Their
**P2 recreation candidacy** is recorded in
`engineering/ingestion/P1-DOCUMENT-LINEAGE.md` (§"App-note → P2 recreation candidacy").
P1 recreations re-derive every number against P2 silicon; a recreation is a *new* P2AN
number, not an inherited P1 one, and new notes need not be recreations — any P2-specific
application qualifies. **The current, authoritative candidate verdicts (which P1 topics
become P2 app notes vs. route to the Architect's Guide / manuals / community) live in the
roster** (`engineering/analysis/p2-app-note-roster.md`), which supersedes the initial
lineage-stage guesses — e.g. inter-cog *communication* routes to the Architect's Guide,
while ADC, CORDIC, multitasking, STRUCT/data-structures, and stack-sizing are app notes.

## Conventions in brief

- Series prefix **`P2AN`** + three digits. Canonical source lives in each note's
  **`opus-master/`** (edit there, never the production workspace render).
- Produced via the shared **P2KB platform stack** (`prepare-manual` → PDF Forge), inheriting
  the platform code-box family and **K = 76** unless a note diverges its code font.
- Full conventions: `APP-NOTE-CREATION-GUIDE.md` §6.

*Established 2026-06-27.*
