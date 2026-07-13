# P2AN007 — Data Structures with the New Language Facilities — Changelog

## v1.0.0 (2026-07-13)

First public release. Extends the note to cover the two STRUCT facilities Spin2 has gained since v45,
neither of which had a home in any reader-facing P2 document until now.

**New — R5, a whole record in one long (member bitfields, {Spin2_v54}).** Named bit ranges inside a
LONG member let an entire command record — opcode, argument, and sequence number — occupy a single
long, so the payload and the "a new one arrived" signal become the same atomic write: no lock, no
separate sequence counter, and no ordering rule left to get wrong. The recipe teaches the trap that
comes with it, which is the opposite of the obvious assumption: fitting in one long does **not** make
a record atomic, because each bitfield write is a read-modify-write of the backing long. Three field
writes are three stores a reader can land between. Atomicity comes from staging the record privately
and publishing it in one whole-struct store — and snapshotting it in one load on the way back in.

**New — R6, safe raw addressing with OFFSETOF ({Spin2_v53}).** Compiler-computed member offsets for
the places you must leave dot-notation behind: a packed header off the wire, a buffer handed to inline
PASM. The point isn't brevity — it's that a hand-counted offset goes silently wrong the day someone
widens a member, while `OFFSETOF` keeps being right.

**Unchanged:** recipes R1–R4 remain `{Spin2_v45}`, so a compiler predating these extensions still
compiles and runs them; the newer floors apply only to the files that use them. The note's scope is
still implementation-only — the contract decision (which structure, copy vs. reference) stays with
the P2 Architect's Guide. All six recipes compile clean under `pnut_ts -d` v1.55.0 and ship in the
downloadable example library.

## v0.1.0 (2026-07-06)

Initial draft for community review. A techniques-catalog application note for the Spin2 `{Spin2_v45}`
STRUCT facility and the worked implementation of sharing records safely across cogs. One shared idea
(a STRUCT is a packed named record; sharing it across cogs means publishing a multi-field record
atomically — write the fields, then flip one long) applied through four runnable recipes: an in-cog
record and array (declare, fill, whole-struct copy, SIZEOF), a lock-free single-producer/single-
consumer ring buffer, a latest-wins command mailbox published with a sequence counter, and a
lock-guarded multi-writer queue using the P2 hardware locks (LOCKNEW/LOCKTRY/LOCKREL — the real P2
lock methods, never the P1 lockset/lockclr). Implementation-only by design: the note teaches the
worked code and defers the *contract decision* (which structure to use and why, copy vs. reference)
to the P2 Architect's Guide. Every recipe compiles clean under `pnut_ts -d`; cross-cog race-freedom
is described from the atomic-single-long model, with a two-cog hardware confirmation noted as a later
step. Ships with a downloadable example library of all four programs.
