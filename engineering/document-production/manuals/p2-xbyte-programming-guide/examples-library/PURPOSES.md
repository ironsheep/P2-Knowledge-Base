# Example purposes

The one header field `sync-manual-examples.py` will not derive. Everything else
in an example's header (the manual, the version, where it appears, the dates)
is read from the repository at sync time. This is the sentence a person writes.

Keep it to one line, and say what the example *shows*, not what it *is*.

- `xbyte-minimal-vm.spin2`: The smallest complete XBYTE program - load the table, prime the FIFO, arm the engine, four handlers, halt
- `xbyte-growing-vm.spin2`: The minimal VM grown to eleven bytecodes - a shared ALU body, variables, a branch, and a cog that arms twice
- `xbyte-display-list.spin2`: The engine driving a graphics display list - the same dispatch with no interpreter in sight
