# Appendix A: How Each Erratum Was Confirmed {#app-a}

Every erratum in this guide was confirmed on a P2 board (Rev C) at 200 MHz by a test program, and every workaround it prints ran on silicon inside a test program. Every program is in the examples archive. Each one checks its controls before it gives a verdict, had the result for the erratum present and for it absent written in before it ran, and prints every measured value, so its verdict can be re-derived from its output. Each workaround test also reproduces its erratum in the same run, so a clean result cannot come from a test that is unable to see the defect.

## The evidence {#sec-a-evidence}

| Erratum | Test programs | What was measured | Result |
|---|---|---|---|
| **E1** | `e1-setq-block-pointer-step-test.spin2` | The `PTRx` step of six block transfers, with and without an `ALTD` after the `SETQ`; its control arms are the workaround | With the `ALTD`, every block moved but `PTRx` took the single-long step (+4, or +12 for `ptra++[3]`); without it, the full block step. 2026-09-24, run twice |
| **E2** | `e2-altx-takes-pending-augs-test.spin2` | An immediate-`#S` `ALTD` or `ALTR` between `AUGS` and its target; the register-`S` workaround; `AUGD` across an `ALTS` | The `ALTx` moved `idx` by bits 17:9 of the augment (5); the target got the full value. With a register `S`, `idx` did not move. `AUGD` was unaffected. 2026-09-24, run twice |
| **E3** | `e3-getct-stale-upper-long-runA.spin2`, `e3-getct-stale-upper-long-runB.spin2`, `e3-cogs-0-3-stale-window-test.spin2`, `e3-stale-window-closes-test.spin2` | The upper long, `GETMS()` and `GETSEC()` in a group that missed one, two and eight wraps, in cogs 4-7 and in cogs 0-3, before and after the group's next wrap | Behind by one wrap per wrap missed, in every pair; current after one wrap run through. 2026-09-24 and 2026-09-27 |
| **E3** | `e3-pasm2-counter-targets-test.spin2`, `e3-spin2-counter-methods-test.spin2`, `e3-debug-timestamp-test.spin2` (with `e3-debug-timestamp-verdict.py`) | Every counter wait, event and timeout in PASM2 and Spin2, inside the stale window and across its closing wrap; `DEBUG_TIMESTAMP` stamps | Every wait timed as in an up-to-date group; stamps sent from the window were one wrap behind. 2026-09-29 |
| **E3** | `e3-workaround-keeper-cog-test.spin2`, `e3-workaround-waiting-cog-test.spin2` | The keeper, and keepers held in `WAITATN` and `WAITX` | Cogs of 4-7 started after one and two wraps read current; with no keeper, one behind. 2026-09-26 and 2026-09-27 |
| **E4** | `e4-getxacc-clear-gating-test.spin2` | `GETXACC` with the streamer idle, in a non-Goertzel mode, and inside a Goertzel burst | All 50 idle and non-Goertzel reads returned the accumulators unchanged; a read inside a burst cleared, and split the burst exactly. 2026-09-24, run twice |
| **E5** | `e5-goertzel-one-clock-lag-test.spin2` | How many terms a reading after a burst holds, and where the last term goes | N-1 terms, in all 16 sequences; the last term arrived with the next Goertzel burst. 2026-09-24, run twice |
| **E5** | `e5-goertzel-sinc2-iteration-count-test.spin2` | Not an erratum: the documented SINC2 constraint, and its two remedies | Both remedies held. 2026-09-25, run twice |
| **E4, E5** | `e4-e5-workaround-read-sums-test.spin2` | `burst_sums` for bursts of 1 to 1001 clocks, at both input levels | Exactly N terms on both sums in all 60 calls. 2026-09-26 |
| **E6** | `e6-dac-mode-adc-enable-test.spin2` | Whether `OUT` runs the ADC in DAC noise mode at `TT` = `%00` and at `%01`; the `%01` word is the workaround | At `%00` the ADC never ran; at `%01` it ran in every sample. 2026-09-25, run twice |
| **E7** | `e7-rdfast-blocking-after-no-wait-test.spin2`, `e7-next-hub-instruction-test.spin2`, `e7-every-hub-width-test.spin2` | Hub reads, writes, block reads and a waiting `RDFAST`, 2 to 44 clocks after a no-wait `RDFAST`, in every hub alignment | Released below 16 clocks, by alignment; none from 16 clocks on; the waiting form released nothing. 2026-09-25 and 2026-10-01 |
| **E7** | `e7-workaround-hub-access-test.spin2`, `e7-workaround-rdfast-spacing-test.spin2`, `e7-workaround-setq-block-test.spin2` | The printed blocks, the waiting form, and 16 to 20 clocks before a block read | Correct in every alignment and trial. 2026-09-26 and 2026-10-01 |

The archive copies are the programs that ran, prepared for readers: each carries a new file header, and internal labels are replaced by erratum numbers. Every measuring routine assembles to the same bytes as the program that ran. The archive copies were run again on P2 hardware, and every analysed value, class and verdict matched the original runs. The only other differences were the ones any two runs show: the E6 test's count of the running ADC's toggles, and the SINC2 test's deliberately jittered arms.

## How to run them {#sec-a-run}

1. Compile with DEBUG enabled: `pnut-ts -d <file>.spin2` (or PNut with DEBUG).
2. Download to RAM on a bare P2 board, with a reset. The E3 programs check that the counter starts from zero, so the download must reset the part.
3. Watch the DEBUG terminal. Each program ends with its verdict line, or prints `RIG FAIL` and no verdict if a control fails.
4. For `e3-debug-timestamp-test.spin2` only: save the DEBUG log and run `python3 e3-debug-timestamp-verdict.py` on it. The program cannot read its own stamps; the script prints their verdict.

**Pins.** The E4 and E5 programs drive P3, so P3 must be free. The E6 test drives P4 and reads it through P5, so both must be free and unconnected. The others use no pins.

**Running time.** The E3 programs wait for the counter's lower long to wrap, 2^32^ clocks (21.47 s at 200 MHz) each time, and run for 44 s to 216 s after reset. The others finish within about 25 s, most within a second or two.
