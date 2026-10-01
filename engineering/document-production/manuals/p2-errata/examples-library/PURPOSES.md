# Example purposes

The one header field `sync-manual-examples.py` will not derive. Everything else
in a program's header (the manual, the version, the chapters that name it, the
dates) is read from the repository at sync time. This is the sentence a person
writes.

Each line is Appendix A's "What it decides" entry for the file, prefixed with
the erratum it belongs to. Keep it to one line, ASCII only.

- `e1-setq-block-pointer-step-test.spin2`: Erratum E1 test: the PTRx step of a SETQ/SETQ2 block transfer with and without an ALTD between them, for six transfer forms, with three single-long references; its control arms are the workaround
- `e2-altx-takes-pending-augs-test.spin2`: Erratum E2 test: whether an immediate-#S ALTD or ALTR between AUGS and its target takes the augment; the register-S workaround; AUGD across an immediate-S ALTS
- `e3-getct-stale-upper-long-runA.spin2`: Erratum E3 test, Run A: the upper long GETCT WC returns in cogs 4-7 after that group has missed one wrap, and after it has missed two
- `e3-getct-stale-upper-long-runB.spin2`: Erratum E3 test, Run B: the Run A readings with a cog of cogs 4-7 running from the start
- `e3-workaround-keeper-cog-test.spin2`: Erratum E3 workaround test: with the keeper cog started first, whether cogs of 4-7 started after one and after two wraps read the current upper long; then, with the keeper stopped, that the erratum returns
- `e3-workaround-waiting-cog-test.spin2`: Erratum E3 workaround test: whether a keeper held in WAITATN, and one held in WAITX, keeps cogs 4-7 current through a wrap; then, with no keeper, that the erratum returns
- `e3-cogs-0-3-stale-window-test.spin2`: Erratum E3 test: with every cog of 0-3 stopped across two wraps, the upper long read in cogs 1 and 3 before and after the group's next wrap
- `e3-stale-window-closes-test.spin2`: Erratum E3 test: after eight missed wraps, the upper long read in cogs 4 and 7, and GETMS() and GETSEC() in a Spin2 cog, before and after the group's next wrap
- `e3-pasm2-counter-targets-test.spin2`: Erratum E3 test: whether WAITCT1-3, POLLCT1-3, JCT1-3, JNCT1-3, the CT interrupts, the SETQ timeout and WAITX time as in an up-to-date group, inside the stale window and across its closing wrap; and whether a cog held in WAITCT1 keeps its group current
- `e3-spin2-counter-methods-test.spin2`: Erratum E3 test: whether Spin2's WAITCT(), POLLCT(), WAITMS(), WAITUS() and GETCT() time as in an up-to-date group, inside the stale window and across its closing wrap; GETMS() and GETSEC() alongside, which read short inside it
- `e3-debug-timestamp-test.spin2`: Erratum E3 test: whether a DEBUG_TIMESTAMP stamp on a message sent from the stale window, by Spin2 debug() and by PASM2 DEBUG, carries the sending cog's stale upper long; the stamps are judged from the saved log by e3-debug-timestamp-verdict.py
- `e4-getxacc-clear-gating-test.spin2`: Erratum E4 test: whether GETXACC clears the accumulators with the streamer idle, in a non-Goertzel mode, and inside a Goertzel burst
- `e5-goertzel-one-clock-lag-test.spin2`: Erratum E5 test: how many terms a reading after a Goertzel burst holds, and where the last term goes
- `e5-goertzel-sinc2-iteration-count-test.spin2`: Erratum E5 scope test, not an erratum test: the documented SINC2 constraint that E5's workaround does not cover; which samples a varying iteration count corrupts, whether one clock of read jitter does the same, and whether XZERO or a constant count keeps every sample clean
- `e4-e5-workaround-read-sums-test.spin2`: Errata E4 and E5 workaround test: whether the burst_sums helper routine returns exactly N terms for bursts of 1 to 1001 clocks, back to back, at both input levels; alongside, the uncorrected reads that show both errata
- `e6-dac-mode-adc-enable-test.spin2`: Erratum E6 test: whether raising OUT runs the ADC in a DAC smart-pin mode with TT = %00 and with TT = %01; the TT = %01 word is the workaround
- `e7-rdfast-blocking-after-no-wait-test.spin2`: Erratum E7 test: how many clocks a RDFAST needs before its first read, in every hub alignment, for blocking and no-wait RDFAST and WRFAST, and what a blocking RDFAST does when issued while a no-wait one is still arming
- `e7-workaround-rdfast-spacing-test.spin2`: Erratum E7 workaround test: whether a WAITX #12 between the two RDFASTs gives a correct first read in every hub alignment; alongside, the unspaced sweep that shows the erratum
- `e7-next-hub-instruction-test.spin2`: Erratum E7 test: whether a RDLONG or WRLONG issued 0 to 8 instructions after a no-wait RDFAST completes before its own hub access, in every hub alignment; the waiting form alongside; and whether making the first of two RDFASTs the waiting form removes E7's original failure
- `e7-every-hub-width-test.spin2`: Erratum E7 test: whether a no-wait RDFAST releases RDBYTE, RDWORD, WRBYTE and WRWORD as it does RDLONG and WRLONG; the flags a released read writes, and whether it still steps PTRA++; whether a no-wait WRFAST releases anything; and a SETQ block RDLONG in the window
- `e7-workaround-hub-access-test.spin2`: Erratum E7 workaround test: whether a RDLONG, or a WRLONG and the RDLONG after it, started 16 clocks after a no-wait RDFAST complete with their own hub access in every hub alignment; the waiting form with no spacing; WRBYTE and WRWORD after the same spacing; alongside, the unspaced read and write that show the erratum
- `e7-workaround-setq-block-test.spin2`: Erratum E7 workaround test: whether the waiting form, and 16, 18 and 20 clocks between a no-wait RDFAST and a SETQ block RDLONG, read the right block with cog RAM intact, each run in a fresh cog; alongside, single released block reads that show the erratum
