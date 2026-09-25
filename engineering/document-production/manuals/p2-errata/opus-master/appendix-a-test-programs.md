# Appendix A: The Test Programs {#app-a}

Every erratum in this manual was confirmed on silicon by a test program, and each program is in the examples archive. They are the programs that ran, with their internal header notes removed; their code is unchanged.

## What each program decides {#sec-a-list}

| Erratum | File | What it decides |
|---|---|---|
| E1 | `e1-setq-block-pointer-step-test.spin2` | the `PTRx` step of a `SETQ`/`SETQ2` block transfer with and without an `ALTD` between them, for six transfer forms, with three single-long references |
| E2 | `e2-altx-takes-pending-augs-test.spin2` | whether an immediate-`#S` `ALTD` or `ALTR` between `AUGS` and its target takes the augment; the register-`S` workaround; `AUGD` across an immediate-`S` `ALTS` |
| E3 | `e3-getct-stale-upper-long-runA.spin2` | the upper long `GETCT WC` returns in cogs 4-7 after that group has missed one wrap, and after it has missed two |
| E3 | `e3-getct-stale-upper-long-runB.spin2` | the same readings with a cog of cogs 4-7 running from the start: the workaround |
| E4 | `e4-getxacc-clear-gating-test.spin2` | whether `GETXACC` clears the accumulators with the streamer idle, in a non-Goertzel mode, and inside a Goertzel burst |
| E5 | `e5-goertzel-one-clock-lag-test.spin2` | how many terms a reading after a Goertzel burst holds, where the last term goes, and the zero-burst workaround |

## How they are built and run {#sec-a-run}

All six programs share one construction:

- **One file each.** Spin2 in cog 0; the measurement itself is PASM2 in a cog of its own, started by `COGINIT` from the program's `DAT` block.
- **The debugger stays out of the measurement.** `DEBUG_COGS = %0000_0001` confines the debug interrupt to cog 0, which only collects the results from hub RAM and prints them.
- **Controls before verdicts.** Each program checks its controls first. If any control fails, it prints a `RIG FAIL` line and no verdict.
- **Outcomes written in advance.** The result each program would print if the erratum were present, and if it were absent, is written into the program before it runs.
- **Raw values printed.** Every measured value is printed, not only the verdict, so the verdict can be re-derived from the output.

To run one:

1. Compile with DEBUG enabled: `pnut-ts -d <file>.spin2` (or PNut with DEBUG).
2. Download to RAM on a bare P2 board, with a reset. The E3 programs check that the counter starts from zero, so the download must reset the part.
3. Watch the DEBUG terminal. The program ends with its verdict line.

Pin use: the E4 and E5 programs drive P3 from the measuring cog, so P3 must be free. The others use no pins.

Running time: the E3 programs wait for the counter's lower long to wrap, which takes 2^32^ clocks (21.47 s at 200 MHz); Run A ends about 105 s after reset and Run B about 44 s after reset. The E1, E2, E4 and E5 programs each printed their whole output in about one second.

All six ran on 2026-09-24 on a P2 board at 200 MHz, each twice, from two builds with identical measuring code, and every measured value matched between the runs.
