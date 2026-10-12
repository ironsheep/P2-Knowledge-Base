# Example purposes — P2AN006

One line per shipped example. `sync-manual-examples.py` reads these into the
generated header's `Purpose....` field; it will not invent one. ASCII only —
the header is `.spin2` source, and the authoring guide's rule is absolute.

- `instrument-cog-stack.spin2` — Guard a worker cog's stack: prepare it with a fill pattern and sentinel before launch, then check the sentinel while the cog runs
- `high-water-mark.spin2` — Measure how deep a worker cog's stack really got, then right-size the buffer to about 1.5 times that depth
- `pinpoint-overflow.spin2` — Find which routine overran a stack by checking the sentinel after each step of the worker
- `size-task-stack.spin2` — Size a cooperative TASKSPIN task's stack with the same technique a cog stack uses

## Not examples

Files the corpus ships that are not examples: no generated header, no printed block
required. Both `sync-manual-examples.py` and `verify-example-corpus-identity.py` read
this section.

- `isp_stack_check.spin2` — the stack-check utility object (Stephen M. Moraco, MIT), shipped verbatim with its own header
