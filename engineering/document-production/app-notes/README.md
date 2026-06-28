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
| **P2AN000** | *(to be assigned)* | **experimental — in setup** | First note; `000` marks "not yet placed in the published sequence." See `P2AN000/P2AN000-NOTES.md`. |

## Where notes come from

The Parallax **P1 application notes** were ingested 2026-06-27 as pattern donors. Their
**P2 recreation candidacy** is recorded in
`engineering/ingestion/P1-DOCUMENT-LINEAGE.md` (§"App-note → P2 recreation candidacy").
The STRONG candidates are the natural early P2 notes — AN001 Counters → **Smart Pin modes**,
AN008 → **smart-pin ADC**, AN014 Coroutines → **PASM2 `CALLD`**. Recreations re-derive every
number against P2 silicon; a recreation is a *new* P2AN number, not an inherited P1 one. New
notes need not be recreations — any P2-specific application qualifies.

## Conventions in brief

- Series prefix **`P2AN`** + three digits. Canonical source lives in each note's
  **`opus-master/`** (edit there, never the production workspace render).
- Produced via the shared **P2KB platform stack** (`prepare-manual` → PDF Forge), inheriting
  the platform code-box family and **K = 76** unless a note diverges its code font.
- Full conventions: `APP-NOTE-CREATION-GUIDE.md` §6.

*Established 2026-06-27.*
