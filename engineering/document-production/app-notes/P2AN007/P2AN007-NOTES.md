# P2AN007 — Working Notes

**Status:** stood up + drafted 2026-07-06 (Family C app-notes sprint); v0.1.0 draft ready for PDF review
**Created:** 2026-07-06
**Topic:** Data Structures with the New Language Facilities (roster item **C2**, Concurrency & New Language Features family)
**Owning manual (enrichment fork):** Spin2 Reference Manual — **PARKED**, so this note is the guided home (no foundational fork)
**Related notes:** P2AN005 (Cooperative Multitasking), P2AN006 (Stack Sizing) — same sprint; the Architect's Guide (contract decisions)
**Sprint plan:** `engineering/planning/FAMILY-C-APP-NOTES-SPRINT-PLAN.md`

## Purpose

The Spin2 STRUCT facility ({Spin2_v45}) plus the worked *implementation* of hub-shared cross-cog
structures (ring/queue/mailbox with indexing + locking) has reference-only KB coverage and no guided
home. This note is that home, and the P2 successor (lineage only) to Parallax P1 AN003 (Abstract
Data Structures).

## SCOPE BOUNDARY (load-bearing) — implementation-only

C2 teaches the **worked code** for the structures. The **contract decision** — which structure to
use, why, copy vs. reference, the three-planes framing, and especially **refcount-vs-copy fan-out**
(flagged irreversible in `data-flow-contracts.yaml`) — stays with the **P2 Architect's Guide** +
the decomposition YAML layer. The note CITES the Guide for the "why," never re-derives it. This is
what keeps C2 from bloating into the Guide's territory. (Roster §3 C2 + disposition ledger.)

## Archetype & structure

Techniques-catalog: shared base (STRUCT syntax + the atomic-single-long publish discipline +
in-cog-vs-cross-cog + the choose-the-structure→Architect's-Guide boundary), a decision table, then
four runnable recipes R1–R4, each with a 🔍 Verify. No ToC. No rendered figures.

## Recipes (all compile `pnut_ts -d` v1.55.0)

| # | Recipe | STRUCT/lock features | Lock? | File |
|---|---|---|---|---|
| R1 | In-cog record + array | STRUCT decl, typed members, array, whole-struct copy, SIZEOF | no | `in-cog-record.spin2` |
| R2 | Lock-free SPSC ring buffer | STRUCT array in hub, single-owner head/tail, `& MASK`, publish-index-last | no | `spsc-ring-buffer.spin2` |
| R3 | Latest-wins mailbox | STRUCT cmd block, seq bumped LAST, seq/ack handshake | no | `latest-wins-mailbox.spin2` |
| R4 | Locked multi-writer queue | LOCKNEW/LOCKTRY/LOCKREL, release-on-path, ascending-order note | yes | `locked-multiwriter-queue.spin2` |

Deque: shown in Adapt-It as the ring/queue mechanism with both ends live (no new primitive).

## The one discipline taught

A single hub long is atomic; a multi-field record is not. Every cross-cog recipe writes the record's
fields FIRST, then flips one long (index or sequence counter) that publishes them. Single writer of
that long → no lock (R2/R3); several writers → one hardware lock (R4).

## Sources (all P2-native — no P1 content read or cited)

- `deliverables/ai/P2/language/spin2/keywords/STRUCT.yaml` (syntax, members, arrays, SIZEOF, pointers, cross-object export/import, the >15-long struct-pointer bracket gotcha)
- `deliverables/ai/P2/language/spin2/methods/{locknew,locktry,lockrel,lockret,lockchk}.yaml` + `architecture/locks.yaml` (16 locks, LOCKTRY test-and-set, deadlock ordering, release-on-all-paths)
- `deliverables/ai/P2/architecture/decomposition/data-flow-contracts.yaml` + `patterns/implementation/{spin2_latest_wins_mailbox,spin2_buffer_management}.yaml` (the comm-style mechanisms; CITED, choice deferred to the Guide)
- Ground truth: `pnut_ts` v1.55.0 compiles.

"Successor to AN003" is **roster lineage metadata only**. No P1 document read or cited (AN003 is
P1-Spin, has no STRUCT). AN003 PDF un-ingested (`external-inputs/P1/AppNotes/AN003-...pdf`) — not
needed.

## P2KB findings (logged; YAML fixes DEFERRED to after PDF review)

- **F-199 (CONFIRMED)** — `patterns/implementation/spin2_shared_memory.yaml` uses P1 `lockset()`/
  `lockclr()` (do NOT exist in P2; would not compile). This note deliberately uses the real P2
  `LOCKTRY`/`LOCKREL` and never cites the P1 form. Deferred fix: rewrite the pattern to P2 locks.
- **F-200 (CONFIRMED)** — `spin2_event_dispatcher.yaml` is SPSC-only but unscoped; R4 shows the
  lock-guarded multi-writer form explicitly.

## Open questions (for authoring / audit)

- Cross-cog atomicity / race-freedom is a runtime multi-cog property — compile proves legality only;
  described from the atomic-single-long model; a two-cog hardware confirmation is a later step
  (→ EF ledger if accepted). No invented DEBUG captures.
- YAML companion: `deliverables/ai/P2/application-notes/p2an007-data-structures-new-facilities.yaml`
  — established schema; agreement-gated against this body.

## Canonical source

Body: `opus-master/P2AN007.md` (+ `opus-master/front-matter.md` cover). Edit here; the workspace
render is generated and overwrites edits.
