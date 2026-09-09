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

**The whole input surface was re-verified against the debugger's own code before
release**, and five things it had said turned out to be wrong. Each is the kind a
reader acts on and then mistrusts the tool for:

- **Right-click is not ignored.** Nine regions had been shown with a dash in the
  right-click column, which reads as *nothing happens*. Only four regions read
  which button you pressed; everywhere else a right-click does exactly what a
  left-click does.
- **Right-clicking a break condition also clears DEBUG.** The manual had said it
  toggles "without disturbing the others" — the one description the panel does not
  match — and four buttons depart from the general grammar in ways worth knowing.
  Both are now stated, with the trap called out: toggle DEBUG last, or use `D`.
- **There is no LUT watch list.** `R` clears the register-delta list only; the
  manual had promised it cleared a second list that does not exist.
- **Go is a three-state machine that reads its state before your button.** While
  the cog runs free it requests an asynchronous COGBRK rather than "stopping"
  anything, and the display dims after 250 ms to tell you the view is stale.
- **Some hints are deliberately empty.** Hovering a value clears the hint bar
  rather than describing it, and the manual had invented text for exactly the
  regions the tool had removed it from. Moving off the window shows the P2's clock
  frequency rather than going blank.

Also new: the keys that are captured and do nothing, `Alt`/`Cmd` being ignored
outright, `Ctrl+D` and `Ctrl+M` reaching hub navigation instead of their letter
commands, macOS right-click delivery and its whole-gesture latch, macOS
`Shift`+wheel arriving on the horizontal axis, hub scrolling wrapping where cog
scrolling clamps, and the wheel having no effect outside the disassembly and hub
panels.

Carries machine-readable copyright and licence in its PDF metadata.
