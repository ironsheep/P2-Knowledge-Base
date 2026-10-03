::: caution
**Who meets it:** PASM2 that places an instruction between a `SETQ` or `SETQ2` and the block `RDLONG`, `WRLONG` or `WMLONG` it prepares, when the transfer updates `PTRx` (for example `ptra++`). Parallax names `ALTx`, `AUGS` and `AUGD` in that position. A `##` operand on the transfer puts one there without your writing it: the assembler places its `AUGS` directly before the transfer, after the `SETQ`.

**What you see:** the whole block moves, but `PTRx` steps as for a single long (`ptra++` moves it by 4), not past the block.

**What to do:** write the `SETQ` or `SETQ2` directly before the transfer, and keep `##` operands off a block transfer that updates `PTRx`.
:::
