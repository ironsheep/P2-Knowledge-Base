# Erratum E1: SETQ Block Transfers Lose Their Pointer Step {#ch-e1}

::: caution
**Expected:** A `SETQ` or `SETQ2` block `RDLONG` or `WRLONG` through `ptra++` moves `PTRA` past the whole block, 4 bytes per long (P2 Documentation, *FAST BLOCK MOVES*).

**Actual:** With an `ALTD` between the `SETQ` and the transfer, every long still moves, but `PTRA` moves only 4 bytes, the step `ptra++` gives a single long.

**Fix:** Keep the `SETQ` or `SETQ2` directly before the transfer, with nothing between them; see *The fix*.
:::

The erratum affects PASM code that places an `ALTD` between a `SETQ` or `SETQ2` and the block transfer it prepares, to redirect the block's first register, and then uses `PTRx` after the transfer: a loop that walks a hub buffer one block at a time, or an address computed from the pointer. Code that reloads the pointer before its next use is not affected. Parallax publishes the defect in the P2 Documentation.

## What the P2 is documented to do {#sec-e1-documented}

A `SETQ` or `SETQ2` placed before `RDLONG`, `WRLONG` or `WMLONG` turns that instruction into a fast block move. The P2 Documentation, in its section *FAST BLOCK MOVES*, states what a `PTRx` expression does in a block move:

> For fast block moves, PTRx expressions cannot have arbitrary index values, since the index will be overridden with the number of longs, with bit 4 of the encoded index value serving as the `++`/`--` indicator.

Its example for `SETQ #x` followed by `RDLONG first_reg,PTRA++` reads x+1 longs from `PTRA` and gives the update as `PTRA += (x+1)*4`: the pointer moves past the whole block. Outside a block move, the same document defines a `PTRx` update as `PTRx += INDEX*SCALE`, where `SCALE` is 4 for `RDLONG`, `WRLONG` and `WMLONG`. A plain `ptra++` therefore moves `PTRA` by 4, and `ptra++[3]` moves it by 12.

The P2 Documentation records the departure from the block rule in its KNOWN BUGS section:

> Intervening ALTx/​AUGS/​AUGD instructions between SETQ/​SETQ2 and RDLONG/​WRLONG/​WMLONG-PTRx instructions will cancel the special-case block-size PTRx deltas. The expected number of longs will transfer, but PTRx will only be modified according to normal PTRx expression behavior:

The example that follows loads 16 longs with `SETQ #16-1`, alters the start register with `ALTD start_reg`, and issues `RDLONG 0,ptra++`. Its comment gives the result: `ptra` is incremented by 4 (1 long), not by 16*4.

## What the P2 actually does {#sec-e1-actual}

With an `ALTD` between `SETQ` or `SETQ2` and a block `RDLONG` or `WRLONG` that carries a post-increment `PTRx` expression, one instruction does two things:

- **The transfer completes as written, and the redirect holds.** The number of longs set by `SETQ` or `SETQ2` moves, to or from the registers the `ALTD` selects. The block is read from, or written to, the hub address `PTRx` held before the instruction.
- **`PTRx` takes the plain expression's step.** The pointer changes by the amount the same expression gives without a `SETQ`: +4 for `ptra++` and `ptrb++`, +12 for `ptra++[3]`. The step does not depend on the block length. An 8-long block moved `PTRA` by +4, the same as a 4-long block.

This held for every form tested: `SETQ` with `RDLONG` into cog registers at 4 and at 8 longs, `SETQ2` with `RDLONG` into lookup RAM, and `SETQ` with `WRLONG` from cog registers, through `PTRA` and through `PTRB`, with `ptra++` and with `ptra++[3]`. The measured values are in *How it was proven on a real P2*.

The confirmation is narrower than Parallax's statement. **Only `ALTD` was tested as the intervening instruction; Parallax names `ALTx`, `AUGS` and `AUGD`.** `WMLONG`, `SETQ2` with `WRLONG`, and the decrement and pre-modify forms (`ptra--`, `++ptra`, `--ptra`) were not tested. In the pre-modify forms the expression also sets the hub address the block starts from, so what the part does with that address under this erratum is not established here.

An `ALTD` on its own does not disturb the pointer. A single `RDLONG` with `ptra++`, redirected by `ALTD` and with no `SETQ` before it, moved `PTRA` by +4, as it does without the `ALTD`.

## What your program sees {#sec-e1-sees}

Your data is right and your pointer is not. Every long of the block lands where the `ALTD` sends it, the longs on either side of the block are untouched, and the hub side of the transfer starts at the address `PTRx` held. Only the value left in `PTRx` differs: after a 4-long block through `ptra++`, `PTRA` points 4 bytes past the start of the block instead of 16.

You see the effect at the next access through that pointer. A loop that walks a hub buffer block by block with `SETQ`, `ALTD` and `RDLONG ..., ptra++` starts each block 4 bytes after the start of the previous one, not after its end, so its reads return overlapping data. The same loop built on `WRLONG` writes each block over all but the first long of the block before it. Any address your code computes from `PTRx` after the transfer carries the same error.

## The fix {#sec-e1-fix}

```pasm2
                setq    #4 - 1
                rdlong  dst + 2, ptra++
```

With the `SETQ` or `SETQ2` as the instruction directly before the transfer, the whole block moves and `PTRx` steps past all of it: a *rule at each use*. In your code, `#4 - 1` is your block length minus one and `dst + 2` is the first register of your block.

These two lines are the test program's control for the 4-long read, and on silicon they advanced `PTRA` by +16 in every round, with all four longs in place. The same adjacent form gave the full block step for an 8-long read (+32), through `PTRB`, for a `WRLONG` from cog registers, for `SETQ2` into lookup RAM, and with `ptra++[3]` (+16 each, for 4 longs); in the last, the block count overrides the index, as the P2 Documentation states.

The cost is the redirect. Without the `ALTD`, the block's first register is the one named in the instruction's `D` field, fixed when the code is assembled. No form that keeps the redirect has been run on silicon, so none is printed here. The adjacent form was run for the six transfers above; the forms named as untested in *What the P2 actually does* were not run in it either.

## Why it happens {#sec-e1-why}

A block transfer depends on the cog knowing that a `SETQ` or `SETQ2` came before it, and the cog keeps that knowledge in two forms.

The first form is held across an intervening `ALTx`, `AUGS` or `AUGD`, so that those instructions can sit between a `SETQ` and the transfer it prepares. The transfer takes its long count from this held form, which is why the full block still moves.

The pointer update does not use the held form. It asks only whether the instruction immediately before the `RDLONG`, `WRLONG` or `WMLONG` was a `SETQ` or `SETQ2`. With an `ALTD` in that position the answer is no, so the pointer is updated as for a single-long access: by the index encoded in the `PTRx` expression, times 4. For `ptra++` the index is 1, giving 4; for `ptra++[3]` it is 3, giving 12.

By the same reasoning an `AUGS` or `AUGD` in that position also breaks the adjacency the pointer update looks for. The test program did not exercise them.

## How it was proven on a real P2 {#sec-e1-proof}

The test runs on a bare P2 board at 200 MHz. The measurement runs in a PASM cog of its own, started with `COGINIT`, because the Spin2 interpreter in cog 0 uses `PTRA` as its stack pointer. The debugger's interrupt is confined to cog 0 (`DEBUG_COGS = %0000_0001`), so it never enters the measuring cog. Cog 0 reads the results from hub RAM and does all checking and printing.

The measuring cog runs 15 arms, one after another, as one round, and runs 4 rounds, interleaved. Each arm loads the pointer, copies it to a register, executes one transfer, and copies the pointer again; the change in the pointer is the second copy minus the first. Before every arm, the destination region and a separate trap region are refilled with the sentinel `$5E5E_5E5E` and the pointer is reloaded, so no arm inherits another's data. Hub source long *k* holds `$A5A0_0000` + *k*, and each read starts at source long 4, so a complete block read from there holds `$A5A0_0004` onward.

Each hazard arm (`SETQ`, `ALTD`, transfer) is paired with a control arm that is the same transfer with no `ALTD`. The hazard arm's own `D` field names the trap region, and its `ALTD` redirects the block to the place the control writes. A lost `ALTD` would put the block in the trap; a lost `SETQ` would move one long. Both possible pointer changes were written into the program before the run: the plain expression's step if the erratum holds, the block step if it does not. Three single-long references establish the plain steps on this part, and every control had to read its required change and a complete, correctly placed block in every round before any verdict was given.

The results, from the second run, in bytes:

| Transfer | Longs | Without `ALTD` | With `ALTD` | Longs at the `ALTD` destination |
|---|:--:|:--:|:--:|:--:|
| `setq #3` + `rdlong ..., ptra++` | 4 | +16 | **+4** | 4/4 |
| `setq #7` + `rdlong ..., ptra++` | 8 | +32 | **+4** | 8/8 |
| `setq #3` + `rdlong ..., ptra++[3]` | 4 | +16 | **+12** | 4/4 |
| `setq #3` + `rdlong ..., ptrb++` | 4 | +16 | **+4** | 4/4 |
| `setq #3` + `wrlong ..., ptra++` | 4 | +16 | **+4** | 4/4 |
| `setq2 #3` + `rdlong` (lookup RAM) `..., ptra++` | 4 | +16 | **+4** | 4/4 |

The *Without `ALTD`* column is the fix: each control is the same transfer with the `SETQ` or `SETQ2` directly before it, and the first row's control is the two lines printed in *The fix*. In the `wrlong` row, the four longs that reached hub RAM are the ones in the registers the `ALTD` selected. The single-long references read +4 for `rdlong ..., ptra++`, +4 for the same instruction redirected by `ALTD`, and +12 for `rdlong ..., ptra++[3]`.

Every round of every arm gave the same value. In every arm the trap region was untouched: it held the sentinel after each read arm, and the write arm's trap registers kept their initial values `$7E7E_0000` + *k*. For the first row, round 0 printed `before=$0000_23C8 after=$0000_23D8 delta=16` for the control and `before=$0000_23C8 after=$0000_23CC delta=4` for the hazard arm, with `$A5A0_0004` to `$A5A0_0007` in destination slots 2 to 5 in both.

The test was run twice on 2026-09-24, from two builds of the program: as first written, and after a style revision that left the measuring code unchanged. The hub addresses differ between the builds (the read arms' pointer started at `$0000_23B8` in the first run and `$0000_23C8` in the second), and every pointer change and every data result matched. The values above are read from the per-round raw lines, not from the program's own verdict line.

## The test program {#sec-e1-program}

The test program is `e1-setq-block-pointer-step-test.spin2` in the examples archive. Its measuring cog is one PASM routine that runs the 15 arms in sequence. Each arm has the same frame: `prep_cog` refills the destination region `dst` and the trap region `trp` with the sentinel; the pointer is loaded from `c_rsrc`, the hub address of source long 4; `c_before` and `c_after` capture the pointer around the transfer; and `dump_cog` writes the pointer pair and both regions to a record in hub RAM.

The control for the primary pair, `SETQ` directly before `RDLONG`, carries the fix in this frame:

```pasm2
                call    #prep_cog
                mov     ptra, c_rsrc
                mov     c_before, ptra
                setq    #4 - 1
                rdlong  dst + 2, ptra++
                mov     c_after, ptra
                call    #dump_cog
```

The hazard arm places the `ALTD` between them. Its `RDLONG` names the trap region, `trp + 2`; the register `c_hidx` holds the address `dst + 2`, so a working `ALTD` sends the block to the same registers the control uses:

```pasm2
'--- arm 3  H_BLK4 : PRIMARY hazard -- SETQ / ALTD / RDLONG ptra++
                call    #prep_cog
                mov     ptra, c_rsrc
                mov     c_before, ptra
                setq    #4 - 1
                altd    c_hidx
                rdlong  trp + 2, ptra++
                mov     c_after, ptra
                call    #dump_cog
```

The other arms follow the same frame: `setq #8 - 1` for the 8-long pair, `ptra++[3]` and `ptrb++` for the index and pointer pairs, `wrlong` from the cog registers `wsrc` with the trap `wtrp` for the write pair, and `setq2` into lookup RAM for the last pair. In the listing the three instructions of every hazard arm are consecutive longs, so nothing else sits between the `SETQ`, the `ALTD` and the transfer.

Cog 0 computes each arm's pointer change from the record:

```spin2
PRI delta(armIdx, rp) : deltaVal | pRec
  pRec := recaddr(armIdx, rp)
  deltaVal := long[pRec][1] - long[pRec][0]
```

For every arm and round the program prints the pointer before and after, the change, a data class (`FULL` when the block is complete and correctly placed and both regions are otherwise untouched), and the raw contents of both regions. It then prints one line confirming that every control passed, one verdict line per hazard arm, and the verdict for the primary pair last. The program runs once, in well under a second, from RAM with DEBUG enabled; its output is on the DEBUG terminal.

## Status {#sec-e1-status}

| Field | Content |
|---|---|
| Erratum | E1 |
| Published by Parallax | Yes, *P2 Documentation*, KNOWN BUGS |
| Found by | Parallax |
| Confirmed on silicon | Yes — 2026-09-24, on a P2 board at 200 MHz, run twice |
| Fix proven on silicon | Yes — 2026-09-24, rule at each use: `SETQ`/`SETQ2` directly before the transfer |
| Affects | a `SETQ`/`SETQ2` block `RDLONG`/`WRLONG`/`WMLONG` with a `PTRx` update expression, when an `ALTx`, `AUGS` or `AUGD` sits between them (confirmed with `ALTD`) |
| Test program | `e1-setq-block-pointer-step-test.spin2` |
