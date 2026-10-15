# p2-debug-techniques — source folder

**What it is.** A partner project's hard-won debug and instrumentation techniques for the P2
(Spin2/PASM2, pnut-ts), handed to us as three files. The raw files stay private and uncommitted in
`engineering/ingestion/external-inputs/appNote-fodder-NO-COMMIT/p2-debug techniques/`:

| File | Nature |
|---|---|
| `P2-DEBUG-AND-INSTRUMENTATION-TECHNIQUES.md` | the generalized, project-independent write-up (16 sections) |
| `P2-DEVELOPMENT-TECHNIQUES.md` | the same ground as the source project practised it, with its file:line evidence |
| `DEBUG-MASK-CHANNELS-GUIDE.md` | one driver's `DEBUG_MASK` channel scheme (project-specific) |

**Authority: 🟡 cross-check, a LEAD.** Every claim is verified before it reaches the KB or a
document. On the first read, three claims already failed against the compiler, the KB or our bench.
The project's silicon measurements enter as **XF** entries (the external-project hardware register),
graded on its four admission rules, and gaps are asked of the project before any new test is written.

**What this folder holds (committed, with no project names or paths):**
- `CLAIM-LEDGER.md`: every claim, with its kind, KB status, verification route and destinations.
- `TOOLBOX-PLAN.md`: the debug toolbox plan («#433», 2026-10-15): a KB home for every trap,
  technique and fact an agent needs (point of use, symptom hubs, patterns), its Standard A proof,
  and the execution batches. `toolbox-probes/` holds the compile probes it cites.

**How it is used.** These are Stephen's decisions of 2026-10-12, recorded in todo-mcp key
`debug_techniques_decisions`:
- the ingestion fans out to the KB YAML first;
- it then feeds one diagnostics handbook, whose shape is confirmed by a prototype first;
- it feeds a P2AN006 revision (done: v1.0.2);
- and it feeds additions to the I/O & Smart Pins, Streamer and PNut-Term-TS guides and the planned
  Anti-Patterns and Spin2 Reference manuals.

The tasks are «#427»–«#432».
