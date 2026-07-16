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
| `single-long-packed-record.spin2` | R5 (record in one long) | member bitfields ({Spin2_v54}); a whole command record in one long, staged privately and published in one atomic store |
| `packed-header-offsets.spin2` | R6 (raw addressing) | `OFFSETOF` ({Spin2_v53}); compiler-computed member offsets over a packed wire header, plus a struct-pointer view of the same bytes |

**Version gate.** R1–R4 open with `{Spin2_v45}` — STRUCT is a Spin2 v45 language
feature. The two newer facilities raise the floor only for the files that use them:
`packed-header-offsets.spin2` needs **v53** (`OFFSETOF`), and
`single-long-packed-record.spin2` needs **v54** (member bitfields). A compiler that
predates them still builds R1–R4.

**The one discipline.** Every cross-cog recipe writes a record's fields **first**,
then flips a single long (an index or a sequence counter) that publishes it — the
atomic hand-off. A single writer of that long needs no lock (R2, R3); several
writers need one hardware lock (R4). When the payload itself fits in 32 bits, the
record *becomes* that long (R5) — but only if you stage it privately and publish it
in one whole-struct store, because filling a packed long a field at a time is still
several separate read-modify-writes.

**Verification.** Every file compiles clean under `pnut-ts -d` (v1.55, `_clkfreq =
200_000_000`). Build with DEBUG enabled (`-d`). Compilation proves the STRUCT and
lock code is legal; true cross-cog race-freedom is a runtime property you confirm
on a P2 board (two cogs actually contending) — see each recipe's Verify section.

**Scope.** These recipes are the *implementation*. Choosing *which* structure a
design should use, and why (copy vs. reference, latest-wins vs. queue), is a
contract decision covered by the **P2 Architect's Guide**, not this library.

**Packaging.** At release these files are published as `P2AN007-src.zip`
beside the PDF in `deliverables/documents/DOCs/`, with a download link in the
publication roster (per the app-note production convention — see
`../../APP-NOTE-CREATION-GUIDE.md` §6).
