# P2 Errata - Changelog

## v0.2.0 (2026-09-26) — Community Review Draft

**Seven silicon errata, and each opens with what to do about it** — a three-line caution box at the top of every erratum, then a drop-in fix that ran on a real P2.

### Added

- **E6, In a DAC Smart-Pin Mode, OUT Needs TT Bit 0 to Run the ADC**: with `TT` = `%00`, raising `OUT` does not run the pin's ADC, contrary to the published `%TT` table
- **E7, A Blocking RDFAST Can Skip Its Wait After a No-Wait RDFAST**: issued 8 to 15 clocks after a no-wait `RDFAST`, at one spacing per hub alignment, a blocking `RDFAST` does not wait and the next read returns zero
- **E5, a SINC2 scope note**: the E5 fix is for SINC1. SINC2 has its own documented constraint (the P2 Documentation's note on Goertzel SINC2 mode), which is not this erratum; its two remedies, a constant iteration count or `XZERO`, held on silicon
- **A proven fix for every erratum**, printed exactly as it ran on silicon, and named by kind: one-time startup fix, rule at each use, or helper routine. E4 and E5 share one helper routine, `burst_sums`, that returns a burst's exact sums
- **Three fix test programs** in Appendix A, each of which also reproduces its erratum in the same run

### Changed

- **Every erratum opens with a caution box**: what the P2 Documentation says to expect, what the part does instead, and the fix
- **Section headings name whose statement is contradicted and what a program sees**: *What the P2 is documented to do*, *What the P2 actually does*, *What your program sees*, *The fix*, *How it was proven on a real P2*
- **Chapters are headed by erratum number** (*Erratum E3*), in the contents and running heads as well
- **The summary table** lists all seven errata and each one's fix

## v0.1.0 (2026-09-25) — Community Review Draft

**Five silicon errata, each proven on a real P2** — two that Parallax published, and three new ones predicted from the design and confirmed on the bench.

### Added

- **E1, SETQ Block Transfers Lose Their Pointer Step**: an `ALTx`, `AUGS` or `AUGD` between `SETQ` and a block `RDLONG`/`WRLONG`/`WMLONG` leaves `PTRx` moved by one long's step, while the data transfers correctly
- **E2, An Immediate ALTx Takes a Pending AUGS**: an `ALTx` with an immediate `#S` between `AUGS` and its target takes the augment, and the target takes it too
- **E3, GETCT Returns a Stale Upper Long**: a cog group that had no cog running when the counter wrapped reads an upper long that is behind
- **E4, GETXACC Clears Only During a Goertzel Burst**: idle, or in any other streamer mode, `GETXACC` returns the live accumulator and clears nothing
- **E5, The Goertzel Accumulators Trail by One Clock**: a burst's last term lands in the next burst
- **What counts as an erratum**: the three classes of finding, defined once, and why this manual lists only the first
- **A summary table** of every erratum found so far, with its workaround
