# P2AN007 — Working Notes

**Status:** drafted 2026-07-06 (Family C app-notes sprint); **extended + bumped to v1.0.0 pre-release 2026-07-13** —
adds R5 (member bitfields, v54) + R6 (OFFSETOF, v53). Hardware-verification rigs built and compile-clean;
awaiting Stephen's silicon run before the PDF renders.
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
| R5 | Whole record in one long | member bitfields **{Spin2_v54}** (nameless form), staged-local + ONE whole-struct store | no | `single-long-packed-record.spin2` |
| R6 | Raw addressing, safely | **OFFSETOF {Spin2_v53}** + SIZEOF over a packed wire header; `^struct` pointer view | n/a | `packed-header-offsets.spin2` |

Deque: shown in Adapt-It as the ring/queue mechanism with both ends live (no new primitive).

## The one discipline taught

A single hub long is atomic; a multi-field record is not. Every cross-cog recipe writes the record's
fields FIRST, then flips one long (index or sequence counter) that publishes them. Single writer of
that long → no lock (R2/R3); several writers → one hardware lock (R4).

**R5 carries that thesis to its conclusion — and to its trap.** Member bitfields let a whole record
occupy one long, so the payload and its sequence number publish in a single atomic store. But fitting
in one long does NOT make it atomic: each bitfield write is a read-modify-write of the backing long,
so filling the SHARED record field-by-field is several separate stores a reader can land between.
Atomicity comes from staging privately + ONE whole-struct store (and ONE whole-struct load to read).
This is the counter-intuitive point of the whole note and it is what VT4 measures.

## Version-gate policy (v1.0.0)

R1–R4 stay `{Spin2_v45}` so an older compiler still builds them; the newer floors bind only the files
that use them (R6 → v53, R5 → v54). Note the v54 bitfield syntax parses UNCONDITIONALLY (no
level54_symbols table), so `{Spin2_v54}` is a declaration of intent, not an enforced gate — a clean
compile does not prove the toolchain is new enough. Said explicitly in the note.

## Why R5/R6 belong here at all (2026-07-13 decision)

Checked fleet-wide: **no reader-facing P2 document covers `OFFSETOF` or struct member bitfields.** The
KB has both fully (`methods/offsetof.yaml`, `concepts/struct-bitfields.yaml`), the ASM manual's audit
explicitly excludes them from its reserved-words appendix, and the Spin2 Reference Manual is PARKED —
so this note is STRUCT's only guided home. Adding them before the first render costs one authoring
pass; adding them after v1.0.0 releases would cost a bump + re-audit + re-render.

## F-213 — a defect this work surfaced in our own draft

v0.1.0's R3 told the reader *"drop that wait and the newest command always wins."* The worker reads
`opcode`/`arg0`/`arg1` as THREE separate shared reads; the seq/ack handshake is the only thing stopping
the writer overwriting the command mid-read. R3 **as printed** is correct — the *guidance to modify it*
was unsafe. v1.0.0 replaces it with a pitfall + the two honest non-blocking options (pack into one long
per R5; or re-check the sequence after copying and discard a straddling copy). Filed F-213. VT2 arm C
measures it. Surfaced by the act of designing the rig — writing down what R3 guarantees exposed the
sentence that contradicted it.

## Hardware verification (NEXT — Stephen-gated)

`audit/verification-tests/` — 5 self-auditing rigs, all `pnut_ts -d`-clean, git-ignored workspace
(`.gitignore` extended 2026-07-13 to cover `app-notes/*/audit/` — it previously only covered
`manuals/*/audit/`; P2AN007 is the first app note with an audit workspace). Each race rig runs the
correct discipline AND a deliberately-broken control with an IDENTICAL injected delay in both arms, so
the arms differ in exactly one thing: where the publish happens. **Zero tears in both arms = the
detector was never exercised = INCONCLUSIVE, not a pass** — the rigs enforce that themselves.

| Rig | Proves | Log |
|---|---|---|
| VT1 | R2 — publish-index-last prevents torn reads | `logs/vt1.log` |
| VT2 | R3 — publish order + the ack is load-bearing (F-213 arm C) | `logs/vt2.log` |
| VT3 | R4 — the hardware lock actually serializes two writers | `logs/vt3.log` |
| VT4 | R5 — a one-long record still needs a one-store publish | `logs/vt4.log` |
| VT5 | R6/R1 — OFFSETOF/SIZEOF match the numbers the note prints | `logs/vt5.log` |

After the run: certify each log → EF-NNN entries in the empirical ledger → fold any correction into
opus-master BEFORE the render → append the race-freedom sentence to the v1.0.0 Revision History (held
back behind a HOLD comment until the logs exist) → prepare-manual → Forge PDF → release.

### Run status

| Rig | Run 1 (07-13) | Run 2 (07-13) | State |
|---|---|---|---|
| VT1 | 0 / **200,000** | 0 / **200,000** | **BANKED** — reproduced exactly |
| VT4 | 0 / **109,642** | 0 / **116,452** | **BANKED** — reproduced |
| VT5 | 11/11 PASS | 11/11 PASS | **BANKED** — deterministic |
| VT2 | A0 / B20,000 / **C0** | A0 / B5,001 / **C0** | INCONCLUSIVE → rev 3, re-run |
| VT3 | 0 / **14,976** | 0 / **0** | INCONCLUSIVE → rev 2, re-run |

**VT4 is the empirical centerpiece.** In-place field writes to the shared packed long tore ~110k times
per 200k snapshots; the staged one-store publish tore zero, twice. R5's counter-intuitive claim is
measured, not argued.

### The phase-lock trap (methodology, cost us two runs)

VT3's unlocked arm gave 14,976 anomalies on run 1 and **0** on run 2 from a binary whose only change
was debug text. Two cogs running deterministic loops of equal length hold a near-fixed relative phase,
so "do the writers ever collide" was decided at `cogspin` time and never re-sampled; one added debug
line rerolled it. Same disease in VT2 arm C (zero twice). **Fix: make the race structural** — hold the
contended window open longer than the other cog's entire loop (VT3: 1µs → 10µs section; VT2: 1µs → 25µs
worker gap), applied identically in every arm so only the protocol still differs. Promoted to
`engineering/operations/lessons-learned/two-cog-race-rigs-must-be-structural.md`.

The INCONCLUSIVE guard is what caught this. Without it, run 2's VT3 would have banked "locked arm: 0
anomalies" as a clean PASS from a run where the detector never fired.

## Sources (all P2-native — no P1 content read or cited)

- `deliverables/ai/P2/language/spin2/keywords/STRUCT.yaml` (syntax, members, arrays, SIZEOF, pointers, cross-object export/import, the >15-long struct-pointer bracket gotcha)
- `deliverables/ai/P2/language/spin2/methods/{locknew,locktry,lockrel,lockret,lockchk}.yaml` + `architecture/locks.yaml` (16 locks, LOCKTRY test-and-set, deadlock ordering, release-on-all-paths)
- `deliverables/ai/P2/architecture/decomposition/data-flow-contracts.yaml` + `patterns/implementation/{spin2_latest_wins_mailbox,spin2_buffer_management}.yaml` (the comm-style mechanisms; CITED, choice deferred to the Guide)
- Ground truth: `pnut_ts` v1.55.0 compiles.

"Successor to AN003" is **roster lineage metadata only**. No P1 document read or cited (AN003 is
P1-Spin, has no STRUCT). AN003 PDF un-ingested (`external-inputs/P1/AppNotes/AN003-...pdf`) — not
needed.

## P2KB findings (logged; both RESOLVED — register shows F-199/F-200 `DONE (2026-07-06)`)

- **F-199 (CONFIRMED)** — `patterns/implementation/spin2_shared_memory.yaml` uses P1 `lockset()`/
  `lockclr()` (do NOT exist in P2; would not compile). This note deliberately uses the real P2
  `LOCKTRY`/`LOCKREL` and never cites the P1 form. Fix applied same day (register: DONE 2026-07-06).
- **F-200 (CONFIRMED)** — `spin2_event_dispatcher.yaml` is SPSC-only but unscoped; R4 shows the
  lock-guarded multi-writer form explicitly.

## Open questions (for authoring / audit)

- Cross-cog atomicity / race-freedom is a runtime multi-cog property — compile proves legality only.
  RESOLVED-IN-FLIGHT: the rigs above make this measurable rather than argued. Until the logs land,
  the note claims nothing about the hardware run and the Revision History withholds its confirmation
  sentence. No invented DEBUG captures.
- YAML companion: `deliverables/ai/P2/application-notes/p2an007-data-structures-new-facilities.yaml`
  — established schema; agreement-gated against this body.

## Canonical source

Body: `opus-master/P2AN007.md` (+ `opus-master/front-matter.md` cover). Edit here; the workspace
render is generated and overwrites edits.
