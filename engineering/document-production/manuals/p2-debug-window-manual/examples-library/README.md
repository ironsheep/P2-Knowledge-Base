# P2 DEBUG Window Manual — Examples Library

These are the complete, runnable Spin2 programs that appear in the *P2 DEBUG
Window Manual*, one file per worked example, named by the chapter it appears in.

- **Exactly as printed.** Each file is the program shown in the manual, verbatim.
- **No capture facilities.** Unlike the figure-generators used to produce the
  manual's screenshots, these contain no `` `SAVE ``/`` `SAVE WINDOW ``/`` `CLOSE ``
  or `DEBUG_END_SESSION` commands.
- **Windows stay open.** Every program ends in a `repeat` loop so the program
  does not exit and close its DEBUG window(s) when the demo finishes.
- **Compiles clean.** Every file compiles with `pnut-ts -d` (the `-d` flag
  compiles the `debug()` directive contents as well).

Open one in your P2 toolchain, compile, and run on a P2 with the DEBUG terminal
attached — no external wiring is required.
