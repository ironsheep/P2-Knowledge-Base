# P2 Errata - the test programs

Every erratum in P2 Errata was confirmed on silicon by one of these programs,
and every workaround the manual prints ran on silicon inside one of them. They are the
programs that ran. Each carries a short generated header and an MIT licence
footer; between them is the program itself.

**These are whole programs, not printed listings.** The manual quotes excerpts
of them in each erratum's *The test program* section, and prints every
workaround block byte for byte, but no file here is a copy of one listing. What differs
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
| `e1-setq-block-pointer-step-test.spin2` | E1 | The `PTRx` step of a `SETQ`/`SETQ2` block transfer with and without an `ALTD` between them, for six transfer forms; its control arms are the workaround. |
| `e2-altx-takes-pending-augs-test.spin2` | E2 | Whether an immediate-`#S` `ALTD` or `ALTR` between `AUGS` and its target takes the augment; the register-`S` workaround; `AUGD` across an immediate-`S` `ALTS`. |
| `e3-getct-stale-upper-long-runA.spin2` | E3 | The upper long `GETCT WC` returns in cogs 4-7 after that group has missed one wrap, and after it has missed two. |
| `e3-getct-stale-upper-long-runB.spin2` | E3 | The same readings with a cog of cogs 4-7 running from the start. |
| `e3-workaround-keeper-cog-test.spin2` | E3 workaround | With the keeper cog started first, whether cogs of 4-7 started after one and after two wraps read the current upper long; then, with the keeper stopped, that the erratum returns. |
| `e3-workaround-waiting-cog-test.spin2` | E3 workaround | Whether a keeper held in `WAITATN`, and one held in `WAITX`, keeps cogs 4-7 current through a wrap; then, with no keeper, that the erratum returns. |
| `e3-cogs-0-3-stale-window-test.spin2` | E3 | With every cog of 0-3 stopped across two wraps, the upper long read in cogs 1 and 3 before and after the group's next wrap. |
| `e3-stale-window-closes-test.spin2` | E3 | After eight missed wraps, the upper long read in cogs 4 and 7, and `GETMS()` and `GETSEC()` in a Spin2 cog, before and after the group's next wrap. |
| `e3-pasm2-counter-targets-test.spin2` | E3 | Whether `WAITCT1-3`, `POLLCT1-3`, `JCT1-3`, `JNCT1-3`, the CT interrupts, the `SETQ` timeout and `WAITX` time as in an up-to-date group, inside the stale window and across its closing wrap; whether a cog held in `WAITCT1` keeps its group current. |
| `e3-spin2-counter-methods-test.spin2` | E3 | Whether `WAITCT()`, `POLLCT()`, `WAITMS()`, `WAITUS()` and `GETCT()` time as in an up-to-date group, inside the stale window and across its closing wrap; `GETMS()` and `GETSEC()` alongside. |
| `e3-debug-timestamp-test.spin2` | E3 | Whether a `DEBUG_TIMESTAMP` stamp on a message sent from the stale window carries the sender's stale upper long, from Spin2 `debug()` and PASM2 `DEBUG`. Its stamps are judged from the saved log by `e3-debug-timestamp-verdict.py`. |
| `e4-getxacc-clear-gating-test.spin2` | E4 | Whether `GETXACC` clears the accumulators with the streamer idle, in a non-Goertzel mode, and inside a Goertzel burst. |
| `e5-goertzel-one-clock-lag-test.spin2` | E5 | How many terms a reading after a Goertzel burst holds, and where the last term goes. |
| `e5-goertzel-sinc2-iteration-count-test.spin2` | E5 (scope) | Not an erratum test: the documented SINC2 constraint that E5's workaround does not cover. |
| `e4-e5-workaround-read-sums-test.spin2` | E4, E5 workaround | Whether the `burst_sums` helper routine returns exactly N terms for bursts of 1 to 1001 clocks; alongside, the uncorrected reads that show both errata. |
| `e6-dac-mode-adc-enable-test.spin2` | E6 | Whether raising `OUT` runs the ADC in a DAC smart-pin mode with `TT` = `%00` and with `TT` = `%01`; the `TT` = `%01` word is the workaround. |
| `e7-rdfast-blocking-after-no-wait-test.spin2` | E7 | How many clocks a `RDFAST` needs before its first read, in every hub alignment, and what a blocking `RDFAST` does when issued while a no-wait one is still arming. |
| `e7-workaround-rdfast-spacing-test.spin2` | E7 workaround | Whether a `WAITX #12` between the two `RDFAST`s gives a correct first read in every hub alignment; alongside, the unspaced sweep that shows the erratum. |
| `e7-next-hub-instruction-test.spin2` | E7 | Whether a `RDLONG` or `WRLONG` issued 0 to 8 instructions after a no-wait `RDFAST` completes before its own hub access, in every hub alignment; the waiting form alongside; and whether a waiting first `RDFAST` removes the waiting-`RDFAST` failure. |
| `e7-every-hub-width-test.spin2` | E7 | Whether a no-wait `RDFAST` releases `RDBYTE`, `RDWORD`, `WRBYTE` and `WRWORD` as it does `RDLONG` and `WRLONG`; the flags a released read writes, and whether it still steps `PTRA++`; whether a no-wait `WRFAST` releases anything; a `SETQ` block `RDLONG` in the window. |
| `e7-workaround-hub-access-test.spin2` | E7 workaround | Whether the printed blocks hold: a `RDLONG`, or a `WRLONG` and the `RDLONG` after it, started 16 clocks after a no-wait `RDFAST`; the waiting form with no spacing; `WRBYTE` and `WRWORD` after the same spacing; alongside, the unspaced read and write that show the erratum. |
| `e7-workaround-setq-block-test.spin2` | E7 workaround | Whether the waiting form, and 16, 18 and 20 clocks between a no-wait `RDFAST` and a `SETQ` block `RDLONG`, read the right block with cog RAM intact, each run in a freshly started cog; alongside, single released block reads that show the erratum. |

Appendix A of the manual, *The Test Programs*, lists them the same way.

## How to run one

Every program is one file: Spin2 in cog 0, and the measurement itself in PASM2
in a cog of its own, started by `COGINIT`. `DEBUG_COGS = %0000_0001` confines
the debug interrupt to cog 0, which only collects the results from hub RAM and
prints them. Five E3 programs differ:

- the eight-wrap test also runs a Spin2 cog, since `GETMS()` and `GETSEC()`
  are Spin2 methods;
- the cogs 0-3 test stops cog 0 to empty its group, so its reference and
  reporting cog is cog 4 and `DEBUG_COGS` names cogs 0 and 4;
- the PASM2 counter-targets test runs its probe in cogs 1-7, and the Spin2
  counter-methods test runs its probe as Spin2 in cogs 1-7;
- the `DEBUG_TIMESTAMP` test puts the debugger in cogs 0, 1, 4 and 7, since
  the stamp is taken by the debugger in the cog that sends the message.

1. Compile with DEBUG enabled: `pnut-ts -d <file>.spin2` (or PNut with DEBUG).
   Without `-d` every `debug()` is dropped and the program prints nothing.
2. Download to RAM on a bare P2 board, with a reset. The E3 programs check that
   the counter starts from zero, so the download must reset the part.
3. Watch the DEBUG terminal. The program ends with its verdict line.
4. For the `DEBUG_TIMESTAMP` test only: save the DEBUG log, then run
   `python3 e3-debug-timestamp-verdict.py <saved log>`. The program cannot
   read its own stamps (the debugger adds them on the way to the terminal),
   so its verdict line says only whether the stale window was where the test
   needs it; the script prints the stamp verdicts.

Each program checks its controls first; if any control fails it prints a
`RIG FAIL` line and no verdict. Every measured value is printed, not only the
verdict, so the verdict can be re-derived from the output.

## Pins

| Programs | Pins |
|----------|------|
| E4, E5, the SINC2 test and the E4/E5 workaround test | Drive P3 from the measuring cog: P3 must be free. |
| E6 | Drives P4 and reads it through P5: both must be free and unconnected. |
| All others | Use no pins. |

## Running times

At 200 MHz, as run:

| Program | Time |
|---------|------|
| E3 Run A | ends about 105 s after reset (it waits for the counter's lower long to wrap, 2^32 clocks = 21.47 s, several times) |
| E3 Run B | ends about 44 s after reset |
| E3 workaround test | ends about 67 s after reset (three wraps) |
| E3 waiting-cog workaround test | ends about 66 s after reset (three wraps) |
| E3 cogs 0-3 test | ends about 87 s after reset (four wraps) |
| E3 eight-wrap test | ends about 216 s after reset (ten wraps) |
| E3 PASM2 counter-targets test | ends about 130 s after reset (six wraps) |
| E3 Spin2 counter-methods test | ends about 44 s after reset (two wraps) |
| E3 `DEBUG_TIMESTAMP` test | ends about 45 s after reset (two wraps) |
| E7 test | prints its output over about 23 s |
| E7 workaround test | prints its output over about 8 s |
| E7 next-hub-instruction test | prints its output over about 2 s |
| E7 every-hub-width test | prints its output over about 5 s |
| E7 block-read workaround test | prints its output over about 9 s |
| E7 read/write workaround test | prints its output in about one second |
| SINC2 test | prints its output over about 5 s |
| E1, E2, E4, E5, E6 tests and the E4/E5 workaround test | print their whole output in about one second |

## Building

`.bin` output is **not** committed: it is recreatable from the source, and the
`.spin2` is the artifact of record.
