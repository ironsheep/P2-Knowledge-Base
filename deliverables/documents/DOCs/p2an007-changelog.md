# P2AN007 — Data Structures with the New Language Facilities — Changelog

## v1.0.1 (2026-08-08)

A licensing change. No technical content changed.

- **Licensed CC BY-SA 4.0** — share and adapt this note, including commercially, with attribution and under the same terms.


## v1.0.0 (2026-07-13)

Initial release for community review. A techniques-catalog application note for the Spin2 `STRUCT`
facility — packed, named, typed records — and the worked code for sharing them safely across cogs.
One shared idea (a single hub long is atomic but a multi-field record is not, so a record is
published by writing its fields first and flipping one long last) applied through six runnable
recipes: an in-cog record and array, a lock-free single-producer/single-consumer ring buffer, a
latest-wins command mailbox published with a sequence counter, a lock-guarded multi-writer queue on
the real P2 hardware locks (`LOCKNEW`/`LOCKTRY`/`LOCKREL`), a whole command record packed into a
single atomically-published long with `{Spin2_v54}` member bitfields, and compiler-computed member
offsets with `{Spin2_v53}` `OFFSETOF` for the places raw addressing is unavoidable. Recipes R1–R4
need only `{Spin2_v45}`, so a compiler predating the newer facilities still builds them.

The note carries the counter-intuitive fact at the heart of packed records: fitting a record into
one long does not make it atomic, because each bitfield write is a read-modify-write of the backing
long — atomicity comes from staging the record privately and publishing it in a single store. Every
cross-cog claim here is confirmed on real P2 silicon with two cogs actually contending: each
discipline was measured against a deliberately-broken version of itself, and the broken version was
required to fail before the result was accepted.

Implementation-only by design: the note teaches the worked code and defers the *contract decision*
(which structure to use and why, copy vs. reference) to the P2 Architect's Guide. Every recipe
compiles clean under `pnut_ts -d`. Ships with a downloadable example library of all six programs.
