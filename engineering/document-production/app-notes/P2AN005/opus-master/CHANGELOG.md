# P2AN005 — Cooperative Multitasking with Spin2 TASK Methods — Changelog

## v1.0.2 (2026-08-08)

A licensing change. No technical content changed — not a page of it.

- **License restored to CC BY-SA 4.0.** This note is again licensed Creative Commons Attribution–ShareAlike 4.0 International, the license the community-review editions carried from 2025-12-09 through 2026-05-22. You may share and adapt it, including commercially, with attribution and under the same terms.
- **Why it changed back.** The CC BY-NC-ND terms it carried from 2026-06 went well beyond their intent. NonCommercial does not restrict resale — it restricts *all* commercial use, including a paid course referencing a chapter or a distributor bundling the PDF with a board. NoDerivatives blocked translations, excerpting, and community forks. The concern behind that change was only that someone might resell this as their own product.
- **Trademark, not copyright, addresses that concern.** The Trademarks note now states that the license grants permissions under copyright only: a reuser may copy, adapt, translate, and sell the text, but may not present the result as the official edition or imply endorsement.
- **Nothing was retroactively taken.** Creative Commons licenses are irrevocable, so every copy distributed under BY-SA stays BY-SA permanently.

## v1.0.1 (2026-07-11)

A wording refinement in Adapt It / Going Further. No recipes added.

- **One bus, many cadences** — keeping a shared bus inside its single owning cog lets cooperative tasks service devices at different rates while the bus stays coherent, sidestepping cross-cog lock coordination.

## v1.0.0 (2026-07-07)

Initial release for community review. A techniques-catalog application note for running several
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
