# P2 Errata - Changelog

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
