# P2AN002 — Example Library

The complete, runnable source for every recipe in **Application Note P2AN002,
"CORDIC for Real Work."** Each file is the same program printed in the note,
extracted verbatim from the opus-master so the download and the document never
drift.

| File | Recipe | Demonstrates |
|---|---|---|
| `cordic-distance-heading.spin2` | R1 | `XYPOL` — distance & heading (cartesian → polar) |
| `cordic-rotate-point.spin2` | R2 | `ROTXY` — rotate a point about the origin |
| `cordic-draw-circle.spin2` | R3 | `POLXY` — points around a circle (DEBUG `PLOT`) |
| `cordic-sine-cosine.spin2` | R4 | `QSIN` / `QCOS` — waveform synthesis (DEBUG `SCOPE`) |
| `cordic-fixed-point.spin2` | R5 | `MULDIV64`, `XYPOL`, **QLOG**/**QEXP** — fixed-point scale & magnitude |
| `cordic-pipeline-throughput.spin2` | R6 | pipelined **QMUL** — fill / steady-state / drain |

**Verification.** Every file compiles clean under `pnut-ts -d` (v1.55, `_clkfreq =
200_000_000`). Build with DEBUG enabled (`-d`) so the `debug()` output windows
appear. Each recipe's expected result is a closed-form value you can check by hand
(see the note's Verify steps) — the CORDIC computes deterministic math.

**Packaging.** At release, these files are published as `P2AN002-src.zip`
beside the PDF in `deliverables/documents/DOCs/`, with a download link in the
publication roster (per the app-note production convention — see
`../../APP-NOTE-CREATION-GUIDE.md` §6).
