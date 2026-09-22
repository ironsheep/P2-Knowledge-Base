# P2 Single-Step Debugger Manual Changelog

## v1.0.1 (2026-09-22)

**The cog register map names the instructions that write PA and PB.**

### Changed

- **`PA` and `PB` receive an address** from `CALLD`'s return form, from `CALLPA`/`CALLPB` and from `LOC`, in the special-registers map diagram

## v1.0.0 (2026-09-10): Initial public release

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

**The interaction set is stated from the debugger's own code**, and the parts that
surprise people are stated outright rather than left to be discovered:

- **Right-click is not ignored.** Only four regions read which button you pressed —
  the break buttons, the disassembly, the event names, and the smart-pin watch box.
  Everywhere else a right-click does exactly what a left-click does.
- **Right-clicking a break condition also clears DEBUG**, and four buttons — INIT,
  DEBUG, EVENT, ADDR — depart from the general grammar in ways worth knowing. The
  trap is called out where a reader meets it: toggle DEBUG last, or use `D`.
- **`R` clears the register-delta watch list.** There is no LUT watch list.
- **Go is a three-state machine that reads its state before your button.** While the
  cog runs free it requests an asynchronous COGBRK rather than stopping anything, and
  the display dims after 250 ms to say the view is stale.
- **Some hints are deliberately empty.** Hovering a value clears the hint bar rather
  than describing it; moving off the window shows the P2's clock frequency.

The reference is complete down to the details that cost an afternoon when they are
missing: the keys that are captured and do nothing, `Alt` and `Cmd` being ignored
outright, `Ctrl+D` and `Ctrl+M` reaching hub navigation rather than their letter
commands, macOS right-click delivery and its whole-gesture latch, macOS `Shift`+wheel
arriving on the horizontal axis, hub scrolling wrapping where cog scrolling clamps,
and the wheel having no effect outside the disassembly and hub panels.

Carries machine-readable copyright and licence in its PDF metadata.
