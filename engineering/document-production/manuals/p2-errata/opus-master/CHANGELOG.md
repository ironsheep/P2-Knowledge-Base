# P2 Errata - Changelog

## v0.2.0 (2026-09-26) — Community Review Draft

**Seven silicon errata, and each opens with what to do about it** — a three-line caution box at the top of every erratum, what any workaround must do, and one drop-in workaround that ran on P2 hardware.

### Added

- **E6, In a DAC Smart-Pin Mode, OUT Needs TT Bit 0 to Run the ADC**: with `TT` = `%00`, raising `OUT` does not run the pin's ADC, contrary to the published `%TT` table
- **E7, After a No-Wait RDFAST, the Next Hub Instruction Can Complete Early**: started fewer than 16 clocks after a no-wait `RDFAST`, a hub read returns the previous hub read's data with that value's flags, a hub write is lost when a hub read follows at once, a `SETQ` block `RDLONG` writes a wrong long and overwrites cog registers or the cog stops, and a waiting `RDFAST` skips its wait so the next read returns zero. Its workaround is one rule: the waiting form of `RDFAST`, or at least 16 clocks before the next hub instruction, with drop-in blocks for a read, a write and the waiting form, each proven on P2 hardware. Four more E7 test programs in Appendix A and the examples archive
- **Find an Erratum by Symptom**: a lookup in the front matter from each symptom a program can show to the erratum that produces it
- **E5, a SINC2 scope note**: the E5 workaround is for SINC1. SINC2 has its own documented constraint (the P2 Documentation's note on Goertzel SINC2 mode), which is not this erratum; its two remedies, a constant iteration count or `XZERO`, held on silicon
- **A proven workaround for every erratum**, led by the condition any workaround must meet, printed exactly as it ran on silicon, and named by kind: one-time startup workaround, rule at each use, or helper routine. It is one way, not the only way: the part keeps its defect, and a workaround steps around it. E4 and E5 share one helper routine, `burst_sums`, that returns a burst's exact sums
- **Six workaround test programs** in Appendix A, each of which also reproduces its erratum in the same run
- **The examples archive**: every test program that ran, as the reader's copy, conforming to the Spin2 authoring guide; its measuring code assembles to the same bytes as the program that ran, and each copy was run again on P2 hardware with the same analysed values and verdicts

### Changed

- **Every erratum opens with a caution box**: what the P2 Documentation says to expect, what the part does instead, and what any workaround must do
- **Section headings name whose statement is contradicted and what a program sees**: *What the P2 is documented to do*, *What the P2 does*, *What your program sees*, *A proven workaround*, *How it was proven on P2 hardware*
- **Chapters are headed by erratum number** (*Erratum E3*), in the contents and running heads as well
- **The summary table** lists all seven errata and, for each, what any workaround must do and the proven way
- **E3 is described as a stale window with a known end**: it opens when a group of four cogs that missed a counter wrap starts a cog, and closes at the group's next wrap, in one step, whatever the lag (confirmed on silicon from 1, 2 and 8 missed wraps). It holds for cogs 0-3 as well as 4-7, and Spin2's `GETMS()` and `GETSEC()` read short inside it, as `GETCT WC` does
- **E3's workaround condition** is now "no 64-bit time inside the stale window", with two proven ways to meet it: keep a cog of the group running at every wrap (the keeper, or a cog of your own; a cog held in `WAITATN`, `WAITX` or `WAITCT1` counts), or wait out one wrap
- **Three more E3 test programs** in Appendix A and the examples archive: a waiting keeper, cogs 0-3 with every cog stopped, and eight missed wraps with `GETMS()`/`GETSEC()`
- **E3 names everything the stale window reaches, and everything it does not**: `DEBUG_TIMESTAMP` stamps join `GETCT WC`, `GETMS()` and `GETSEC()`, since a message sent from the window carries a stamp one wrap early per missed wrap and prints out of time order; the counter events, the `SETQ` timeout, `WAITX`, and Spin2's `GETCT()`, `WAITCT()`, `POLLCT()`, `WAITMS()` and `WAITUS()` are unaffected, inside the window and across its closing wrap. A cog held in `WAITCT1` keeps its group current, as one held in `WAITATN` or `WAITX` does. Three more test programs in Appendix A and the examples archive, one with a script that reads the stamps from the saved log
- **Sources** add the Parallax Spin2 Language Documentation, for what `GETMS()` and `GETSEC()` return and what `DEBUG_TIMESTAMP` stamps

## v0.1.0 (2026-09-25) — Community Review Draft

**Five silicon errata, each proven on P2 hardware** — two that Parallax published, and three new ones predicted from the design and confirmed on the bench.

### Added

- **E1, SETQ Block Transfers Lose Their Pointer Step**: an `ALTx`, `AUGS` or `AUGD` between `SETQ` and a block `RDLONG`/`WRLONG`/`WMLONG` leaves `PTRx` moved by one long's step, while the data transfers correctly
- **E2, An Immediate ALTx Takes a Pending AUGS**: an `ALTx` with an immediate `#S` between `AUGS` and its target takes the augment, and the target takes it too
- **E3, GETCT Returns a Stale Upper Long**: a cog group that had no cog running when the counter wrapped reads an upper long that is behind
- **E4, GETXACC Clears Only During a Goertzel Burst**: idle, or in any other streamer mode, `GETXACC` returns the live accumulator and clears nothing
- **E5, The Goertzel Accumulators Trail by One Clock**: a burst's last term lands in the next burst
- **What counts as an erratum**: the three classes of finding, defined once, and why this manual lists only the first
- **A summary table** of every erratum found so far, with its workaround
