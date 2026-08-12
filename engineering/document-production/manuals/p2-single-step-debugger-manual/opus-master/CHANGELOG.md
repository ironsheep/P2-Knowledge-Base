# P2 Single-Step Debugger Manual Changelog

## v1.0.0

**Initial release.** A complete working guide to the Propeller 2's built-in
single-step debugger — the on-chip debugger that stops your program at an exact
instruction and shows you every register, flag, and byte of memory as it stands
at that moment. It is written for anyone building with `pnut-ts -d` and running
in `pnut-term-ts`, from a first breakpoint through multi-cog and interrupt work.

The manual teaches the debugger window twice over, deliberately. A guided tour
walks the display region by region, so the wall of numbers becomes a set of
places you know. A command reference then gathers the whole interaction set in
one place to look up: every key and Ctrl combination, every left- and right-click
by region, and every wheel step in both cog and hub modes. That interaction set
is documented from the debugger's own implementation and confirmed on real P2
silicon.
