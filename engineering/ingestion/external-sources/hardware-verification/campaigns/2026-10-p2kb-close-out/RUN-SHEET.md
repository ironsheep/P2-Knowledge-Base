# Run sheet — P2KB close-out bench, round 1

Eight programs in `tests/`. **Bare board, nothing attached, no jumpers.** One flash/load each, in
this order (no wiring changes between them). Each prints its own predictions first, then its
result, then `=== END ===` and `DEBUG_END_SESSION`.

**For every run**
1. USB serial connected (DEBUG on P62/P63). Board on its 20 MHz crystal (every program sets
   `_clkfreq = 200_000_000`).
2. Build `pnut-ts -d <file>`, load to RAM with DEBUG on.
3. **Save the whole console output** to `<file-stem>.log` — it is the only record.
4. If no `=== END` line appears within the hang limit below: power-cycle, note the last line seen,
   and send that — it is a hang, not a result.

| # | Program | Pins in use (keep clear) | Runs | Hang limit | Look for |
|---|---|---|---|---|---|
| 1 | `test-vo-s059-xoro-zero-seed.spin2` | none | ~1 s | 10 s | `VERDICT` line (with zero-seed repeatability) |
| 2 | `test-vo-s037-cogatn-self.spin2` | none | < 1 s | 10 s | a reading per detector form, then a `SUMMARY` line |
| 3 | `test-vo-g028-hw-stack-overflow.spin2` | none | < 1 s | 10 s | `READING` lines, arm W width, `VERDICT` |
| 4 | `test-vo-s304-pwm-x-zero-fields.spin2` | P4 (not driven) | < 1 s | 15 s | `VERDICT VO-S304` lines |
| 5 | `test-vo-j-028-y-written-dir-low-counter-modes.spin2` | **P4–P6** (P5, P6 driven) | ~1 s | 20 s | per-row verdicts, `=== SUMMARY`, VO-G006a lines |
| 6 | `test-vo-f372-usb-wrpin-on-running-pair.spin2` | **P0/P1** (driven) | ~0.1 s | 15 s | one `VERDICT VO-F372` line |
| 7 | `test-vo-j-006-lut-share-block-load-and-spin2.spin2` | none | < 1 s | 60 s | `VERDICT VO-J-006` lines |
| 8 | `test-vo-j-005r-streamer-capture-ceiling-and-skew.spin2` | **P32–P47** (P32 driven, P36–P47 held low) | 1–5 s | 45 s | `CERT` passes, E ladder, `S ENGAGEMENT`, S readings |

**Round 2 (added 2026-10-09)** — same rules as above:

| # | Program | Pins in use (keep clear) | Runs | Hang limit | Look for |
|---|---|---|---|---|---|
| 9 | `test-vo-j-035-usb-wxpin-on-running-pair.spin2` | **P0/P1** (driven) | < 1 s | 15 s | one `VERDICT VO-J-035` line (SURVIVES / DISTURBED / INCONCLUSIVE) and its settle line |

A `RIG FAIL` on gate P (a late write) means the run's timing missed a deadline — send the log; it is a
rerun, not a result.

**Two things that may happen and are not failures of the run**
- **#6 prints INCONCLUSIVE** (the bare USB pair could not sense its own line state). Then, only
  if you choose to, the fallback is jumpers P0→P2 and P1→P3 and a second-pair version, which I
  would write from that log.
- **#8 stops at `CERT`** if anything on P32–P47 reads high: something is attached or pulled up
  there. Clear it and rerun.

**Any line saying `RIG FAIL` or `NO VERDICT`** means the program's own controls rejected the run:
send the log as is; I read the raw lines and decide whether a rerun or a changed test is needed.

**After the run:** drop the eight `.log` files anywhere I can read and tell me where. I enter each
result as an `EF-NNN` in `../../P2-EMPIRICAL-FINDINGS.md`, mark its row in
`../../VERIFICATION-OPPORTUNITIES.md` `DONE → EF-NNN`, and fill the table in `README.md`.
