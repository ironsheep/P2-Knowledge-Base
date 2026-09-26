# Appendix A: The Test Programs {#app-a}

Every erratum in this manual was confirmed on silicon by a test program, and every workaround it prints ran on silicon inside a test program. Each program is in the examples archive. They are the programs that ran, prepared for readers: each carries a new file header, and internal labels in its comments and in its printed output are replaced with the erratum they refer to. Every measuring routine assembles to the same bytes as the program that ran. The Spin2 code in cog 0 that starts each run, checks its controls and prints the results was brought to the Spin2 authoring guide, so some printed labels and hub addresses differ from the original run. The archive copies themselves were run on P2 hardware on 2026-09-26, and every value the programs analyse, every class and every verdict matched the original runs. Beyond labels, hub addresses and counter timestamps, two things differed, as they differ between any two runs: the E6 test's count of the running ADC's toggles, and the SINC2 test's two deliberately jittered arms. One start-up sample, which the SINC2 test excludes from its analysis (the first sample of its first `XZERO` arm), read differently from both original runs; the cause is not yet known.

## What each program decides {#sec-a-list}

The erratum tests decide whether the defect is present. The workaround tests run the block that *A proven workaround* prints, byte for byte, and each also reproduces the erratum in the same run, so that a clean result cannot come from a test that is unable to see the defect. The workarounds for E1, E2 and E6 are arms of the erratum test itself.

| Erratum | File | What it decides |
|---|---|---|
| E1 | `e1-setq-block-pointer-step-test.spin2` | the `PTRx` step of a `SETQ`/`SETQ2` block transfer with and without an `ALTD` between them, for six transfer forms, with three single-long references; its control arms are the workaround |
| E2 | `e2-altx-takes-pending-augs-test.spin2` | whether an immediate-`#S` `ALTD` or `ALTR` between `AUGS` and its target takes the augment; the register-`S` workaround; `AUGD` across an immediate-`S` `ALTS` |
| E3 | `e3-getct-stale-upper-long-runA.spin2` | the upper long `GETCT WC` returns in cogs 4-7 after that group has missed one wrap, and after it has missed two |
| E3 | `e3-getct-stale-upper-long-runB.spin2` | the same readings with a cog of cogs 4-7 running from the start |
| E3 | `e3-workaround-keeper-cog-test.spin2` | the workaround: with the keeper cog started first, whether cogs of 4-7 started after one and after two wraps read the current upper long; then, with the keeper stopped, that the erratum returns |
| E4 | `e4-getxacc-clear-gating-test.spin2` | whether `GETXACC` clears the accumulators with the streamer idle, in a non-Goertzel mode, and inside a Goertzel burst |
| E5 | `e5-goertzel-one-clock-lag-test.spin2` | how many terms a reading after a Goertzel burst holds, and where the last term goes |
| E5 (scope) | `e5-goertzel-sinc2-iteration-count-test.spin2` | not an erratum test: the documented SINC2 constraint that E5's workaround does not cover; which samples a varying iteration count corrupts, whether one clock of read jitter does the same, and whether `XZERO` or a constant count keeps every sample clean |
| E4, E5 | `e4-e5-workaround-read-sums-test.spin2` | the workaround: whether the `burst_sums` helper routine returns exactly *N* terms for bursts of 1 to 1001 clocks, back to back, at both input levels; alongside, the uncorrected reads that show both errata |
| E6 | `e6-dac-mode-adc-enable-test.spin2` | whether raising `OUT` runs the ADC in a DAC smart-pin mode with `TT` = `%00` and with `TT` = `%01`; the `TT` = `%01` word is the workaround |
| E7 | `e7-rdfast-blocking-after-no-wait-test.spin2` | how many clocks a `RDFAST` needs before its first read, in every hub alignment, for blocking and no-wait `RDFAST` and `WRFAST`, and what a blocking `RDFAST` does when issued while a no-wait one is still arming |
| E7 | `e7-workaround-rdfast-spacing-test.spin2` | the workaround: whether the printed `WAITX` line between the two `RDFAST`s gives a correct first read in every hub alignment; alongside, the unspaced sweep that shows the erratum |

## How they are built and run {#sec-a-run}

Every program shares one construction:

- **One file each.** Spin2 in cog 0; the measurement itself is PASM2 in a cog of its own, started by `COGINIT`.
- **The debugger stays out of the measurement.** `DEBUG_COGS = %0000_0001` confines the debug interrupt to cog 0, which only collects the results from hub RAM and prints them.
- **Controls before verdicts.** Each program checks its controls first. If any control fails, it prints a `RIG FAIL` line and no verdict.
- **Outcomes written in advance.** The result each program would print if the erratum were present, and if it were absent, is written into the program before it runs.
- **Raw values printed.** Every measured value is printed, not only the verdict, so the verdict can be re-derived from the output.

To run one:

1. Compile with DEBUG enabled: `pnut-ts -d <file>.spin2` (or PNut with DEBUG).
2. Download to RAM on a bare P2 board, with a reset. The E3 programs check that the counter starts from zero, so the download must reset the part.
3. Watch the DEBUG terminal. The program ends with its verdict line.

Pin use: the E4 and E5 programs, including the SINC2 test and the E4/E5 workaround test, drive P3 from the measuring cog, so P3 must be free. The E6 test drives P4 and reads it through P5, so both must be free and unconnected. The others use no pins.

Running time: the E3 erratum programs wait for the counter's lower long to wrap, which takes 2^32^ clocks (21.47 s at 200 MHz); Run A ends about 105 s after reset and Run B about 44 s after reset. The E7 erratum test printed its output over about 23 s, the SINC2 test over about 5 s. The E1, E2, E4, E5 and E6 erratum programs each printed their whole output in about one second. Of the workaround tests, the E3 test ends about 67 s after reset, since it waits through three wraps; the E7 test printed its output over about 8 s, and the E4/E5 test in about one second.

The E1 to E5 erratum programs ran on 2026-09-24 on a P2 board at 200 MHz, each twice, from two builds with identical measuring code, and every measured value matched between the runs. The E5 SINC2, E6 and E7 erratum programs ran on 2026-09-25, each twice. The three workaround tests ran on 2026-09-26, once each, on the same board at 200 MHz; each reproduced its erratum and passed every control in the same run.
