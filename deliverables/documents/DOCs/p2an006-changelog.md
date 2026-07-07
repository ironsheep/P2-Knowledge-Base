# P2AN006 — Sizing Cog & Task Stacks — Changelog

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
