# P2AN006 — Sizing Cog & Task Stacks — Changelog

## v1.0.1 (2026-08-08)

A licensing change. No technical content changed — not a page of it.

- **License restored to CC BY-SA 4.0.** This note is again licensed Creative Commons Attribution–ShareAlike 4.0 International, the license the community-review editions carried from 2025-12-09 through 2026-05-22. You may share and adapt it, including commercially, with attribution and under the same terms.
- **Why it changed back.** The CC BY-NC-ND terms it carried from 2026-06 went well beyond their intent. NonCommercial does not restrict resale — it restricts *all* commercial use, including a paid course referencing a chapter or a distributor bundling the PDF with a board. NoDerivatives blocked translations, excerpting, and community forks. The concern behind that change was only that someone might resell this as their own product.
- **Trademark, not copyright, addresses that concern.** The Trademarks note now states that the license grants permissions under copyright only: a reuser may copy, adapt, translate, and sell the text, but may not present the result as the official edition or imply endorsement.
- **Nothing was retroactively taken.** Creative Commons licenses are irrevocable, so every copy distributed under BY-SA stays BY-SA permanently.

## v1.0.0 (2026-07-07)

Initial release for community review. A techniques-catalog application note for sizing the stack
buffers that `cogspin` (new-cog) and `TASKSPIN` (intra-cog task) require on the P2 — where an
undersized stack silently overwrites hub memory with no hardware trap. One shared idea (fill the
stack with a known pattern and watch a sentinel just past its end) applied through four runnable
recipes: instrument a new-cog stack against overflow, find the high-water mark and right-size,
pinpoint which routine overran the stack, and size a cooperative task's stack (the companion to
P2AN005). Built around the MIT-licensed `isp_stack_check` utility (Stephen M. Moraco), which ships
in the example library. Every recipe compiles clean under `pnut_ts -d`; the overflow-detection and
halt behavior is described from the utility's design, with observing it fire noted as a bench step.
Ships with a downloadable example library of the utility plus all four programs.
