# P2AN006 — Example Library

The complete, runnable source for the worked recipes in **Application Note
P2AN006, "Sizing Cog & Task Stacks,"** plus the utility they are built around.
Each recipe is extracted verbatim from the opus-master so the download and the
document never drift.

| File | Recipe | Demonstrates |
|---|---|---|
| `isp_stack_check.spin2` | — (the instrument) | the sentinel-fill stack-overflow utility (© Stephen M. Moraco, MIT) |
| `instrument-cog-stack.spin2` | R1 | guard a `cogspin` worker: `prepStackForCheck` + `checkStack` |
| `high-water-mark.spin2` | R2 | measure real usage with `reportStackUse`, then right-size |
| `pinpoint-overflow.spin2` | R3 | granular `checkStack` to localize the overrunning routine |
| `size-task-stack.spin2` | R4 | the same technique on a `TASKSPIN` task stack (needs `{Spin2_v47}`) |

**Layout rule.** Every recipe declares its sentinel long (`endStackMark`)
**immediately after** the stack buffer in the same `DAT` block, so the sentinel
physically abuts the buffer — the technique depends on it.

**Version gate.** R1–R3 are ordinary Spin2 and need no directive. R4 uses
`TASKSPIN`, so it opens with `{Spin2_v47}`.

**Verification.** Every file compiles clean under `pnut-ts -d` (v1.55, `_clkfreq =
200_000_000`); the recipes each `OBJ`-include `isp_stack_check.spin2` from this
folder. Build with DEBUG enabled (`-d`) — the utility reports through `debug()`.
Watching the overflow halt actually fire (shrink a stack below what its code
needs) is a bench step on a P2 board.

**Packaging.** At release these files are published as `P2AN006-src-<YYMMDD>.zip`
beside the PDF in `deliverables/documents/DOCs/`, with a download link in the
publication roster (per the app-note production convention — see
`../../APP-NOTE-CREATION-GUIDE.md` §6).
