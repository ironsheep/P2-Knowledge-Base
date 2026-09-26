# Example purposes

The one header field `sync-manual-examples.py` will not derive. Everything else
in a program's header (the manual, the version, the chapters that name it, the
dates) is read from the repository at sync time. This is the sentence a person
writes.

Each line is Appendix A's "What it decides" entry for the file, prefixed with
the erratum it belongs to. Keep it to one line, ASCII only.

- `e1-setq-block-pointer-step-test.spin2`: Erratum E1 test: the PTRx step of a SETQ/SETQ2 block transfer with and without an ALTD between them, for six transfer forms, with three single-long references; its control arms are the fix
- `e2-altx-takes-pending-augs-test.spin2`: Erratum E2 test: whether an immediate-#S ALTD or ALTR between AUGS and its target takes the augment; the register-S fix; AUGD across an immediate-S ALTS
- `e3-getct-stale-upper-long-runA.spin2`: Erratum E3 test, Run A: the upper long GETCT WC returns in cogs 4-7 after that group has missed one wrap, and after it has missed two
- `e3-getct-stale-upper-long-runB.spin2`: Erratum E3 test, Run B: the Run A readings with a cog of cogs 4-7 running from the start
- `e3-fix-keeper-cog-test.spin2`: Erratum E3 fix test: with the keeper cog started first, whether cogs of 4-7 started after one and after two wraps read the current upper long; then, with the keeper stopped, that the erratum returns
- `e4-getxacc-clear-gating-test.spin2`: Erratum E4 test: whether GETXACC clears the accumulators with the streamer idle, in a non-Goertzel mode, and inside a Goertzel burst
- `e5-goertzel-one-clock-lag-test.spin2`: Erratum E5 test: how many terms a reading after a Goertzel burst holds, and where the last term goes
- `e5-goertzel-sinc2-iteration-count-test.spin2`: Erratum E5 scope test, not an erratum test: the documented SINC2 constraint that E5's fix does not cover; which samples a varying iteration count corrupts, whether one clock of read jitter does the same, and whether XZERO or a constant count keeps every sample clean
- `e4-e5-fix-read-sums-test.spin2`: Errata E4 and E5 fix test: whether the burst_sums helper routine returns exactly N terms for bursts of 1 to 1001 clocks, back to back, at both input levels; alongside, the uncorrected reads that show both errata
- `e6-dac-mode-adc-enable-test.spin2`: Erratum E6 test: whether raising OUT runs the ADC in a DAC smart-pin mode with TT = %00 and with TT = %01; the TT = %01 word is the fix
- `e7-rdfast-blocking-after-no-wait-test.spin2`: Erratum E7 test: how many clocks a RDFAST needs before its first read, in every hub alignment, for blocking and no-wait RDFAST and WRFAST, and what a blocking RDFAST does when issued while a no-wait one is still arming
- `e7-fix-rdfast-spacing-test.spin2`: Erratum E7 fix test: whether the printed WAITX line between the two RDFASTs gives a correct first read in every hub alignment; alongside, the unspaced sweep that shows the erratum
