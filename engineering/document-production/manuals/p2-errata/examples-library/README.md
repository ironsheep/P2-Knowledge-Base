# P2 Errata - the test programs

Every erratum in P2 Errata was confirmed on silicon by one of these programs,
and every fix the manual prints ran on silicon inside one of them. They are the
programs that ran. Each carries a short generated header and an MIT licence
footer; between them is the program itself.

**These are whole programs, not printed listings.** The manual quotes excerpts
of them in each erratum's *The test program* section, and prints every fix
block byte for byte, but no file here is a copy of one listing. What differs
from the build that ran on the bench is comment and label text only: the
internal header notes are gone, and internal reference labels in comments and
in `debug()` output text are replaced by the erratum they belong to.

The header is generated, never hand-written: which manual and version the file
belongs to, the chapters that name it, and when it was written are read from
the repository at sync time. The only hand-authored field is `Purpose`, kept in
`PURPOSES.md`. Regenerate with:

```
python3 engineering/tools/sync-manual-examples.py --doc <this manual's dir>
```

| File | Erratum | What it decides |
|------|---------|-----------------|
| `e1-setq-block-pointer-step-test.spin2` | E1 | The `PTRx` step of a `SETQ`/`SETQ2` block transfer with and without an `ALTD` between them, for six transfer forms; its control arms are the fix. |
| `e2-altx-takes-pending-augs-test.spin2` | E2 | Whether an immediate-`#S` `ALTD` or `ALTR` between `AUGS` and its target takes the augment; the register-`S` fix; `AUGD` across an immediate-`S` `ALTS`. |
| `e3-getct-stale-upper-long-runA.spin2` | E3 | The upper long `GETCT WC` returns in cogs 4-7 after that group has missed one wrap, and after it has missed two. |
| `e3-getct-stale-upper-long-runB.spin2` | E3 | The same readings with a cog of cogs 4-7 running from the start. |
| `e3-fix-keeper-cog-test.spin2` | E3 fix | With the keeper cog started first, whether cogs of 4-7 started after one and after two wraps read the current upper long; then, with the keeper stopped, that the erratum returns. |
| `e4-getxacc-clear-gating-test.spin2` | E4 | Whether `GETXACC` clears the accumulators with the streamer idle, in a non-Goertzel mode, and inside a Goertzel burst. |
| `e5-goertzel-one-clock-lag-test.spin2` | E5 | How many terms a reading after a Goertzel burst holds, and where the last term goes. |
| `e5-goertzel-sinc2-iteration-count-test.spin2` | E5 (scope) | Not an erratum test: the documented SINC2 constraint that E5's fix does not cover. |
| `e4-e5-fix-read-sums-test.spin2` | E4, E5 fix | Whether the `burst_sums` helper routine returns exactly N terms for bursts of 1 to 1001 clocks; alongside, the uncorrected reads that show both errata. |
| `e6-dac-mode-adc-enable-test.spin2` | E6 | Whether raising `OUT` runs the ADC in a DAC smart-pin mode with `TT` = `%00` and with `TT` = `%01`; the `TT` = `%01` word is the fix. |
| `e7-rdfast-blocking-after-no-wait-test.spin2` | E7 | How many clocks a `RDFAST` needs before its first read, in every hub alignment, and what a blocking `RDFAST` does when issued while a no-wait one is still arming. |
| `e7-fix-rdfast-spacing-test.spin2` | E7 fix | Whether the printed `WAITX` line between the two `RDFAST`s gives a correct first read in every hub alignment; alongside, the unspaced sweep that shows the erratum. |

Appendix A of the manual, *The Test Programs*, lists them the same way.

## How to run one

Every program is one file: Spin2 in cog 0, and the measurement itself in PASM2
in a cog of its own, started by `COGINIT`. `DEBUG_COGS = %0000_0001` confines
the debug interrupt to cog 0, which only collects the results from hub RAM and
prints them.

1. Compile with DEBUG enabled: `pnut-ts -d <file>.spin2` (or PNut with DEBUG).
   Without `-d` every `debug()` is dropped and the program prints nothing.
2. Download to RAM on a bare P2 board, with a reset. The E3 programs check that
   the counter starts from zero, so the download must reset the part.
3. Watch the DEBUG terminal. The program ends with its verdict line.

Each program checks its controls first; if any control fails it prints a
`RIG FAIL` line and no verdict. Every measured value is printed, not only the
verdict, so the verdict can be re-derived from the output.

## Pins

| Programs | Pins |
|----------|------|
| E4, E5, the SINC2 test and the E4/E5 fix test | Drive P3 from the measuring cog: P3 must be free. |
| E6 | Drives P4 and reads it through P5: both must be free and unconnected. |
| All others | Use no pins. |

## Running times

At 200 MHz, as run:

| Program | Time |
|---------|------|
| E3 Run A | ends about 105 s after reset (it waits for the counter's lower long to wrap, 2^32 clocks = 21.47 s, several times) |
| E3 Run B | ends about 44 s after reset |
| E3 fix test | ends about 67 s after reset (three wraps) |
| E7 test | prints its output over about 23 s |
| E7 fix test | prints its output over about 8 s |
| SINC2 test | prints its output over about 5 s |
| E1, E2, E4, E5, E6 tests and the E4/E5 fix test | print their whole output in about one second |

## Building

`.bin` output is **not** committed: it is recreatable from the source, and the
`.spin2` is the artifact of record.
