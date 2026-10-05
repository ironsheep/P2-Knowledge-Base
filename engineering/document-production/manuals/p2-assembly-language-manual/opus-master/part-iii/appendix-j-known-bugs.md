::: instrheader
# Appendix J: Known Silicon Bugs {#appendix-j}
:::

This appendix documents known hardware bugs in the P2 silicon that affect instruction behavior. These bugs cannot be fixed in software updates—they are permanent characteristics of the P2X8C4M64P silicon. Each entry gives the condition, the effect and a workaround that steps around it. The two entries below are the bugs the Parallax documentation lists; [Silicon Notes](#silicon-notes) at the end of this appendix points to every Rev C rule this manual states, including these two.

## ALTx/AUGx Interference with SETQ Block Transfers {#bug-altx-setq}

**Affected Instructions:** SETQ, SETQ2, RDLONG, WRLONG, WMLONG with PTRx expressions

**Bug Description:**

When SETQ or SETQ2 precedes RDLONG, WRLONG, or WMLONG to set up a block transfer, an intervening ALTx, AUGS, or AUGD instruction cancels the special-case block-size PTRx delta. The expected number of longs transfers correctly, but PTRx takes the plain expression's own step (+4 for `ptra++`, +12 for `ptra++[3]`) instead of the block step. (Parallax names ALTx, AUGS and AUGD; ALTD was confirmed on silicon.)

**Example of Bug:**

```pasm2
        SETQ    #16-1           ' Ready to load 16 longs
        ALTD    start_reg       ' BUG: Cancels block-size PTRx delta!
        RDLONG  0, ptra++       ' ptra += 4 (not 64!)
```

**Expected Behavior:** After reading 16 longs with `ptra++`, ptra should advance by 64 bytes (16 × 4).

**Actual Behavior:** ptra advances by only 4 bytes, the step `ptra++` takes on its own, because the ALTD instruction between SETQ and RDLONG cancels the block-size adjustment.

**Workaround:**

Nothing may sit between the SETQ or SETQ2 and the transfer it prepares: write them adjacent. The cost is the redirect, since the block's first register is then the one named in the transfer instruction's D field.

```pasm2
        ' Workaround: SETQ directly before the transfer
        SETQ    #16-1           ' Ready to load 16 longs
        RDLONG  start_reg, ptra++ ' ptra advances by 64 bytes
```

---

## AUGS Leakage to Intervening ALTx Instructions {#bug-augs-altx}

**Affected Instructions:** AUGS, and every ALTx (ALTD, ALTS, ALTR and the others) with an immediate #S operand, including the one-operand form

**Bug Description:**

When AUGS precedes an instruction with an immediate #S operand (its intended target), an intervening ALTx that also has an immediate #S operand takes the AUGS value without canceling it. Both the intervening ALTx and the intended target instruction receive the augmented value.

The ALTx takes its base register from S[8:0], which the augment leaves unchanged, so the following instruction is still redirected to the register the program names. The ALTx's D register takes its auto-increment from S[17:9], and those bits now come from the AUGS value, so the D register (here `index`) silently moves by the sign-extended S[17:9].

The one-operand form (`ALTD index`) is encoded with the immediate bit set, so it is affected too.

**Example of Bug:**

```pasm2
        AUGS    #$FFFFF123      ' Intended for ADD instruction
        ALTD    index, #base    ' WARNING: #base also receives AUGS value!
        ADD     0-0, #$123      ' #$123 is augmented, cancels AUGS
```

**Expected Behavior:** AUGS should only affect the ADD instruction's #$123 operand, and `index` should stay as it was.

**Actual Behavior:** AUGS affects both `#base` in the ALTD instruction AND `#$123` in the ADD instruction. The ALTD's S becomes `$FFFFF000 + base`. Its bits 17:9 are %1_1111_1000 (bits 17:12 set, bits 11:9 clear), which sign-extends to -8, so `index` moves by -8. The ADD still receives `$FFFFF123`.

**Workaround:**

Use a register instead of an immediate for the ALTx instruction's S operand when an AUGS is active. The register holds the base in bits 8:0 and a zero auto-increment in bits 17:9.

```pasm2
        ' Workaround: Use register instead of immediate in ALTx
        MOV     temp, #base     ' Load base into register first
        AUGS    #$FFFFF123      ' Intended for ADD instruction
        ALTD    index, temp     ' Register operand - unaffected by AUGS
        ADD     0-0, #$123      ' Only ADD gets the augmented value
```

An AUGD pending across an intervening immediate-S ALTx is not taken by it: the AUGD reaches its #D target. This was tested with one ALTx variant, ALTS.

---

## Summary Table

| Bug | Trigger Condition | Consequence | Workaround |
|-----|-------------------|-------------|------------|
| ALTx cancels block PTRx delta | ALTx/AUGS/AUGD between SETQ/SETQ2 and a block RD/WR/WMLONG with a PTRx expression | PTRx takes the plain expression's step (+4 for `ptra++`) instead of the block step | Nothing between SETQ/SETQ2 and the transfer (keep them adjacent) |
| AUGS leaks to ALTx | ALTx with #S between AUGS and its target | ALTx receives the augmented value; its D register moves by the sign-extended S[17:9] | Use a register for ALTx S operand |

---

*These bugs are documented in the official Parallax P2 documentation and affect all P2X8C4M64P Rev B/C silicon.*

---

## Silicon Notes {#silicon-notes}

A small **Rev C** tag in the text marks a rule about how the current silicon behaves, stated where you use the instruction it concerns. Each line below names one rule and points to it; the rule itself is stated only at its tag.

::: silicon-note-index
:::
