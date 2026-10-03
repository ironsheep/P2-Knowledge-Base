::: caution
**Who meets it:** PASM2 that writes an `AUGS` explicitly and places an `ALTx` with an immediate `#S` (such as `ALTD idx,#base`, or the one-operand `ALTD idx`) between it and the instruction it was written for. A `##` literal never produces this arrangement: the assembler places its `AUGS` directly before the instruction that carries the `##`.

**What you see:** the `ALTx` takes the augment as well, and its `D` register moves by bits 17:9 of the augmented value. The redirect and the target's value are correct.

**What to do:** give that `ALTx` a register `S`.
:::
