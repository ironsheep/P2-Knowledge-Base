# Erratum E1: SETQ Block Transfers Lose Their Pointer Step {#ch-e1}

<!-- include: shared-e1.md -->

## What happens {#sec-e1-actual}

A `SETQ` or `SETQ2` placed before `RDLONG`, `WRLONG` or `WMLONG` makes it a block transfer. The P2 Documentation, in its section *FAST BLOCK MOVES*, gives the pointer update for one: `SETQ #x` followed by `RDLONG first_reg,PTRA++` reads x+1 longs and updates `PTRA += (x+1)*4`, past the whole block. Parallax publishes the exception in the KNOWN BUGS section of the same document:

> Intervening ALTx/​AUGS/​AUGD instructions between SETQ/​SETQ2 and RDLONG/​WRLONG/​WMLONG-PTRx instructions will cancel the special-case block-size PTRx deltas. The expected number of longs will transfer, but PTRx will only be modified according to normal PTRx expression behavior:

On P2 hardware, with an `ALTD` between the `SETQ` and the transfer, every long of the block moved, to the registers the `ALTD` selected and from the hub address `PTRx` held. `PTRx` then changed by the step the same expression gives without a `SETQ`: +4 for `ptra++` and `ptrb++`, +12 for `ptra++[3]`, whatever the length of the block. An 8-long block moved `PTRA` by 4, as a 4-long block did. This held for `SETQ` with `RDLONG` at 4 and 8 longs, `SETQ2` into lookup RAM, and `SETQ` with `WRLONG`, through `PTRA` and through `PTRB`.

Your data is right and your pointer is not. A loop that walks a hub buffer one block at a time starts each block 4 bytes after the start of the one before, so its reads overlap; built on `WRLONG`, each block overwrites all but the first long of the one before it. Code that reloads the pointer before its next use is not affected.

The arrangement is unusual: the reason to write an `ALTD` there is to redirect the block's first register. The `##` path in the box is the one that is easy to miss, because no `AUGS` appears in the source: with `pnut-ts`, `setq #3` followed by `rdlong buf, ptra++[##100]` assembles to `SETQ`, `AUGS`, `RDLONG`.

Only `ALTD` was tested as the intervening instruction; Parallax names `AUGS` and `AUGD` as well. `WMLONG`, `SETQ2` with `WRLONG`, and the decrement and pre-modify forms (`ptra--`, `++ptra`, `--ptra`) were not tested.

## A proven workaround {#sec-e1-workaround}

**What any workaround must do:** nothing may sit between the `SETQ` or `SETQ2` and the block transfer it prepares.

**One way, proven on P2 hardware:** write the `SETQ` or `SETQ2` directly before the transfer.

```pasm2
CON ' ---- E1 Workaround: Block Length ----
  BLOCK_LONGS   = 4                     ' longs in your block

DAT ' ---- E1 Workaround: Block Transfer ----
                setq    #BLOCK_LONGS - 1        ' directly before RDLONG
                rdlong  block_first, ptra++     ' block's first register
```

With the `SETQ` or `SETQ2` as the instruction directly before the transfer, the whole block moves and `PTRx` steps past all of it: a *rule at each use*. In your code, `BLOCK_LONGS - 1` is your block length minus one and `block_first` is the first register of your block. A hub address or offset too large for nine bits goes into `PTRx` before the `SETQ`, so that the transfer carries no `##` operand.

On silicon these two lines advanced `PTRA` by 16 with all four longs in place, and the same adjacent form gave the full block step for an 8-long read, through `PTRB`, for a `WRLONG`, for `SETQ2` into lookup RAM, and with `ptra++[3]`.

The cost is the redirect: without the `ALTD`, the block's first register is fixed when the code is assembled. No form that keeps the redirect has been run on silicon.

**Found by** Parallax, and published in the P2 Documentation's KNOWN BUGS section. Confirmed on P2 hardware on 2026-09-24.
