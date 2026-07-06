# P2AN007 — Example Library

The complete, runnable source for the worked recipes in **Application Note
P2AN007, "Data Structures with the New Language Facilities."** Each file is
extracted verbatim from the opus-master so the download and the document never
drift.

| File | Recipe | Demonstrates |
|---|---|---|
| `in-cog-record.spin2` | R1 (in-cog record) | declare/fill/whole-struct-copy an array of `STRUCT` records + `SIZEOF` |
| `spsc-ring-buffer.spin2` | R2 (lock-free ring) | one-producer/one-consumer ring of records; single-owner indices, no lock |
| `latest-wins-mailbox.spin2` | R3 (latest-wins mailbox) | a command record published with a sequence counter; seq/ack, no lock |
| `locked-multiwriter-queue.spin2` | R4 (locked queue) | many writers → one queue, guarded by a P2 hardware lock (`LOCKNEW`/`LOCKTRY`/`LOCKREL`) |

**Version gate.** Every file opens with `{Spin2_v45}` as its first line — STRUCT is
a Spin2 v45 language feature.

**The one discipline.** Every cross-cog recipe writes a record's fields **first**,
then flips a single long (an index or a sequence counter) that publishes it — the
atomic hand-off. A single writer of that long needs no lock (R2, R3); several
writers need one hardware lock (R4).

**Verification.** Every file compiles clean under `pnut-ts -d` (v1.55, `_clkfreq =
200_000_000`). Build with DEBUG enabled (`-d`). Compilation proves the STRUCT and
lock code is legal; true cross-cog race-freedom is a runtime property you confirm
on a P2 board (two cogs actually contending) — see each recipe's Verify section.

**Scope.** These recipes are the *implementation*. Choosing *which* structure a
design should use, and why (copy vs. reference, latest-wins vs. queue), is a
contract decision covered by the **P2 Architect's Guide**, not this library.

**Packaging.** At release these files are published as `P2AN007-src-<YYMMDD>.zip`
beside the PDF in `deliverables/documents/DOCs/`, with a download link in the
publication roster (per the app-note production convention — see
`../../APP-NOTE-CREATION-GUIDE.md` §6).
