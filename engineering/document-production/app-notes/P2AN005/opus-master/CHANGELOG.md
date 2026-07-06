# P2AN005 — Cooperative Multitasking with Spin2 TASK Methods — Changelog

## v0.1.0 (2026-07-06)

Initial draft for community review. A techniques-catalog application note for running several
cooperative jobs in one cog through Spin2's `{Spin2_v47}` TASK method family — the modern
replacement for the hand-coded PASM coroutine. One shared idea (a task runs until it voluntarily
yields with TASKNEXT, so several jobs take turns inside a single cog) applied through four runnable
recipes the reader selects among by need: a two-task round-robin (two independent blinkers from one
cog), a cooperative yield inside a long computation (keeping a second job responsive), halt/resume
flow control (a consumer that pauses and wakes its producer, plus a synchronized start), and a task
dashboard (a live TASKCHK/TASKHLT census with a clean TASKSTOP shutdown). Every worked program
compiles clean under `pnut_ts -d`; the `TASKWAIT` keyword documented in some older material was
compile-probed, found not to exist in Spin2, and excluded. Scheduling and runtime behaviors are
described from the Spin2 v47+ documentation; hardware confirmation of live scheduling defers to a
bench pass. Ships with a downloadable example library of all four programs.
