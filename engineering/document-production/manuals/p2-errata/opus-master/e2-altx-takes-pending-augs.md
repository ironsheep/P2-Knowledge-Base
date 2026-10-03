# Erratum E2: An Immediate ALTx Takes a Pending AUGS {#ch-e2}

<!-- include: shared-e2.md -->

## What happens {#sec-e2-actual}

An `AUGS` holds 23 bits for the next instruction that carries a literal `#S`, which takes them as bits 31:9 of its `S`. An `ALTx` uses its `S` in two fields: bits 8:0 are the base added to `D[8:0]` to form the substituted address, and bits 17:9 are sign-extended and added to the `D` register as an auto-increment. The P2 Documentation, in its section *REGISTER INDIRECTION*, notes that a nine-bit immediate leaves that second field zero, "so that D is unaffected". Parallax publishes the exception in the KNOWN BUGS section of the same document:

> Intervening ALTx instructions with an immediate #S operand, between AUGS and the AUGS'
> intended target instruction (which would have an immediate #S operand), will use the
> AUGS value, but not cancel it. So, the intended AUGS target instruction will use and
> cancel the AUGS value, as expected, but the intervening ALTx instruction will also use
> the AUGS value (if it has an immediate #S operand). To avoid problems in these
> circumstances, use a register for the S operand of the ALTx instruction, and not an
> immediate #S operand.

On P2 hardware, with `AUGS #$3C5C_0A55` (bits 17:9 = 5) followed by `ALTD idx,#0` or `ALTR idx,#3` and then the target, the `ALTx` moved `idx` by 5. Its redirect was unaffected, since bits 8:0 are still its own field, and the target received the full value `$3C5C_0A55`. No other register in a 32-register window around the target changed. The effect is confined to the `ALTx`'s `D` register, which a later pass of an indexing loop then reads with the wrong value.

The one-operand form counts as immediate: `ALTD idx` assembles to the same instruction word as `ALTD idx,#0`. A pending `AUGD` is not affected: with an immediate-`S` `ALTS` between `AUGD` and its target, the target received the full value and the `ALTS`'s register did not move.

The arrangement is uncommon. It needs an `AUGS` written explicitly, as in Parallax's own example. A `##` literal never produces it, because the assembler places the `AUGS` it generates directly before the instruction that carries the `##`.

`ALTD` and `ALTR` were tested as the intervening instruction, each directly after the `AUGS`, with one augment value.

## A proven workaround {#sec-e2-workaround}

**What any workaround must do:** no `ALTx` with an immediate `#S` may stand between an `AUGS` and the instruction the `AUGS` was written for.

**One way, proven on P2 hardware:** give that `ALTx` a register `S`, as Parallax directs.

```pasm2
                augs    #AUGV
                altd    idx, sreg4
                mov     0-0, #LO
```

With a register `S` on the `ALTD`, the `ALTD` takes nothing from the `AUGS`, `idx` does not move, and the augment reaches the target: a *rule at each use*.

In these lines `AUGV` is the 32-bit value the `AUGS` carries for the `MOV`, `LO` is its low 9 bits, and `sreg4` is a cog register holding the `ALTD`'s `S`: the base, 4, in bits 8:0 and a zero auto-increment in bits 17:9. In your code, the base and any auto-increment that were in the immediate `#S` go into that register. On silicon, the `MOV` was redirected to the register four along from the one `idx` addressed, which received `$3C5C_0A55`, and `idx` did not move. The cost is one cog register for each distinct `S` value.

**Found by** Parallax, and published in the P2 Documentation's KNOWN BUGS section. Confirmed on P2 hardware on 2026-09-24.
