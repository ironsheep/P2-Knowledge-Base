# P2AN007 — Data Structures with the New Language Facilities — Changelog

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
