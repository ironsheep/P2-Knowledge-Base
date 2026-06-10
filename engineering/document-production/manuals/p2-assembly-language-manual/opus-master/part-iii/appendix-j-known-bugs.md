::: instrheader
# Appendix J: Known Silicon Bugs {#appendix-j}
:::

This appendix documents known hardware bugs in the P2 silicon that affect instruction behavior. These bugs cannot be fixed in software updates—they are permanent characteristics of the P2X8C4M64P Rev B/C silicon.

## ALTx/AUGx Interference with SETQ Block Transfers {#bug-altx-setq}

**Affected Instructions:** SETQ, SETQ2, RDLONG, WRLONG, WMLONG with PTRx expressions

**Bug Description:**

When SETQ or SETQ2 precedes RDLONG, WRLONG, or WMLONG to set up a block transfer, intervening ALTx, AUGS, or AUGD instructions cancel the special-case block-size PTRx delta calculation. The expected number of longs transfers correctly, but PTRx is modified according to normal PTRx expression behavior rather than the block-adjusted delta.

**Example of Bug:**

```pasm2
        SETQ    #16-1           ' Ready to load 16 longs
        ALTD    start_reg       ' BUG: Cancels block-size PTRx delta!
        RDLONG  0, ptra++       ' ptra += 4 (not 64!)
```

**Expected Behavior:** After reading 16 longs with `ptra++`, ptra should advance by 64 bytes (16 × 4).

**Actual Behavior:** ptra advances by only 4 bytes (1 long) because the ALTD instruction between SETQ and RDLONG cancels the block-size adjustment.

**Workaround:**

Manually adjust PTRx after the block transfer, or restructure code to avoid ALTx/AUGx instructions between SETQ/SETQ2 and the subsequent RDLONG/WRLONG/WMLONG.

```pasm2
        ' Workaround: Adjust pointer manually after transfer
        SETQ    #16-1           ' Ready to load 16 longs
        ALTD    start_reg       ' Alter start register
        RDLONG  0, ptra++       ' ptra only advances by 4
        ADD     ptra, #(16-1)*4 ' Manually add remaining 60 bytes
```

---

## AUGS Leakage to Intervening ALTx Instructions {#bug-augs-altx}

**Affected Instructions:** AUGS, ALTD, ALTS, ALTR, and all ALTx variants

**Bug Description:**

When AUGS precedes an instruction with an immediate #S operand (its intended target), intervening ALTx instructions that also have an immediate #S operand will consume the AUGS value without canceling it. Both the intervening ALTx and the intended target instruction receive the augmented value.

**Example of Bug:**

```pasm2
        AUGS    #$FFFFF123      ' Intended for ADD instruction
        ALTD    index, #base    ' WARNING: #base also receives AUGS value!
        ADD     0-0, #$123      ' #$123 is augmented, cancels AUGS
```

**Expected Behavior:** AUGS should only affect the ADD instruction's #$123 operand.

**Actual Behavior:** AUGS affects both `#base` in the ALTD instruction AND `#$123` in the ADD instruction. The `#base` value becomes `#$FFFFF000 + base` (augmented), which is almost certainly not the intended behavior.

**Workaround:**

Use a register instead of an immediate for the ALTx instruction's S operand when an AUGS is active.

```pasm2
        ' Workaround: Use register instead of immediate in ALTx
        MOV     temp, #base     ' Load base into register first
        AUGS    #$FFFFF123      ' Intended for ADD instruction
        ALTD    index, temp     ' Register operand - unaffected by AUGS
        ADD     0-0, #$123      ' Only ADD gets the augmented value
```

---

## Summary Table

| Bug | Trigger Condition | Consequence | Workaround |
|-----|-------------------|-------------|------------|
| ALTx cancels block PTRx delta | ALTx/AUGx between SETQ and RD/WR/WMLONG | PTRx advances by single-long delta instead of block delta | Manually adjust PTRx after transfer |
| AUGS leaks to ALTx | ALTx with #S between AUGS and target | ALTx receives unintended augmented value | Use register for ALTx S operand |

---

*These bugs are documented in the official Parallax P2 documentation and affect all P2X8C4M64P Rev B/C silicon.*
