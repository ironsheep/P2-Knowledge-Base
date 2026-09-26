# Erratum E2: An Immediate ALTx Takes a Pending AUGS {#ch-e2}

::: caution
**Expected:** An `ALTx` with a nine-bit immediate `#S` leaves its `D` register unchanged
(P2 Documentation, *REGISTER INDIRECTION*).

**Actual:** Between an `AUGS` and the instruction the `AUGS` was written for, the `ALTx`
takes the augment too, and its `D` register moves by bits 17:9 of the augmented value.

**Fix:** Give that `ALTx` a register `S` instead of an immediate `#S`; see *The fix*.
:::

The erratum affects PASM code that writes an `AUGS` explicitly and places an `ALTx` with
an immediate `#S` between it and the instruction it was written for, as in Parallax's own
example. The `##` literal syntax does not produce this arrangement by itself: the
assembler places the `AUGS` it generates immediately before the instruction that carries
the `##`. Parallax publishes the defect in the P2 Documentation.

## What the P2 is documented to do {#sec-e2-documented}

An `AUGS` holds 23 bits for the next instruction that carries a literal `#S`. That
instruction takes them as bits 31:9 of its `S`, keeps its own 9-bit field as bits 8:0,
and the augment is cancelled. The `ALTx` instructions accept an augmented `S`: their `S`
may be a register, a 9-bit literal or an augmented literal.

The P2 Documentation, in its section *REGISTER INDIRECTION*, describes how `ALTS`, `ALTD`
and `ALTR` use that `S`: the sum of `D[8:0]` and `S[8:0]` is the address substituted into
the next instruction, so `S` serves as a register base and `D` as an index. It continues:

> Additionally, S[17:9] is always sign-extended and added to the D register for index
> updating. Normally, a nine-bit #address will be used for S, causing S[17:9] to be zero,
> so that D is unaffected:

The same document publishes the defect, under KNOWN BUGS:

> Intervening ALTx instructions with an immediate #S operand, between AUGS and the AUGS'
> intended target instruction (which would have an immediate #S operand), will use the
> AUGS value, but not cancel it. So, the intended AUGS target instruction will use and
> cancel the AUGS value, as expected, but the intervening ALTx instruction will also use
> the AUGS value (if it has an immediate #S operand). To avoid problems in these
> circumstances, use a register for the S operand of the ALTx instruction, and not an
> immediate #S operand.

Parallax's example places `ALTD index,#base` between `AUGS #$FFFFF123` and the
`ADD 0-0,#$123` the `AUGS` was written for, and marks the `ALTD` line "Look out! AUGS
will affect #base, too. Use a register, instead." The published statement does not say
what the `ALTx` does with the value it takes, and it names `AUGS` only; it says nothing
about `AUGD` in this arrangement.

## What the P2 actually does {#sec-e2-actual}

The arrangement is `AUGS #value`, then an `ALTx` with an immediate `#S`, then the target
instruction with an immediate `#S`. On the part:

- The `ALTx` receives the augmented 32-bit `S`: bits 31:9 from the `AUGS`, bits 8:0 from
  its own 9-bit field.
- The augment is not cancelled. The target receives the same augmented value.
  Parallax's statement adds that the target then cancels it; the test did not check an
  instruction after the target.

Because `S[8:0]` is still the `ALTx`'s own field, its base is unchanged and the
instruction after it is redirected to the register the program names. What changes is
the auto-increment: `S[17:9]` now comes from the `AUGS` value, and after the `ALTx`
executes, its `D` register has moved by the sign-extended value of those bits. With an
augment of `$3C5C_0A55`, whose bits 17:9 are 5, `ALTD idx,#0` and `ALTR idx,#3` each
moved `idx` by 5, and in each case the target wrote the full augmented value
`$3C5C_0A55` into the register aimed at.

The bench tested `ALTD` and `ALTR` as the intervening instruction; Parallax's statement
covers the `ALTx` instructions generally. In every tested case the `ALTx` sat directly
after the `AUGS` and the target directly after the `ALTx`; other spacings were not
tested. One augment value was used. An `AUGS` written for the `ALTx` itself (the
augmented-literal form of its `S`) was not tested.

**`AUGD` in the same position.** A pending `AUGD` survived an intervening
immediate-`S` `ALTx`. `AUGD #$1357_9B3C`, then `ALTS idxs,#0`, then `WRLONG #$13C` wrote
`$1357_9B3C`, the full augmented value, and `idxs` did not move. One `ALTx` (`ALTS`) and
one augment value were tested for this half.

## What your program sees {#sec-e2-sees}

Your `ALTx`'s `D` register changes when your program expects it to stay put. A 9-bit
immediate `#S` has bits 17:9 clear, so an immediate-`S` `ALTx` on its own has an
auto-increment of 0; in this arrangement it takes bits 17:9 of the augment instead. Any
later instruction that uses that register, such as the next pass of a loop that indexes
with it, sees the moved value.

What does not go wrong, in the tested cases:

- The instruction after the `ALTx` is redirected to the register your program names.
- The target receives the full augmented value.
- No other register in a 32-register window around the target was written.

The size of the move is set by bits 17:9 of the augment, which the documented field
split makes the auto-increment; by that split, an augment whose bits 17:9 are zero moves
nothing. The only value measured was 5.

## The fix {#sec-e2-fix}

```pasm2
                augs    #AUGV
                altd    idx, sreg4
                mov     0-0, #LO
```

With a register `S` on the `ALTD`, the `ALTD` takes nothing from the `AUGS`, `idx` does
not move, and the augment reaches the target: a *rule at each use*.

In these lines `AUGV` is the 32-bit value the `AUGS` carries for the `MOV`, `LO` is its
low 9 bits, and `sreg4` is a cog register that holds the `ALTD`'s `S`: the base, 4, in
bits 8:0 and a zero auto-increment in bits 17:9. In your code, the base and any
auto-increment that were in the immediate `#S` go into that register. On silicon, with
`AUGV` = `$3C5C_0A55`, the `MOV` was redirected to the register four along from the one
`idx` addressed, which received `$3C5C_0A55`, and `idx` did not move. The fix costs one
cog register for each distinct `S` value.

**The one-operand form is not a register form.** `ALTD idx` assembles to the same
instruction word as `ALTD idx,#0`: immediate bit set, `S` = 0. That is the arrangement
the test showed affected. The one-operand form of every `ALTx` instruction is encoded
with the immediate bit set, so writing it does not apply the fix.

The fix was run with `ALTD` as the intervening instruction, one augment value and one
base. Parallax's statement directs a register `S` for any `ALTx` in this position; no
other `ALTx` was run with one.

## Why it happens {#sec-e2-why}

An `AUGS` changes nothing in memory. It holds its 23 bits pending, and the next
instruction that fetches an immediate `S` receives them as the upper bits of that `S`.
Using the augment normally ends the pending state.

The `ALTx` instructions are a planned exception to that last step. An `ALTx` may stand
between an `AUGS` and its target without ending the pending state, so that an augment
can reach an instruction that follows an `ALTx`; Parallax's statement that the target
"will use and cancel the AUGS value, as expected" describes that intent. The exception
covers only the ending of the pending state. The choice of which instruction receives
the augmented value has no such exception: to that choice, an `ALTx` with an immediate
`#S` is one more instruction with an immediate `S`, so it receives the augment for
itself. Because it is an `ALTx`, it then leaves the augment pending, and the target,
the next instruction with an immediate `S`, receives the same value.

An `ALTx` with a register `S` has no immediate `S` to augment. It neither receives the
value nor ends the pending state, which is why the fix holds.

The effect is confined to the auto-increment because of how an `ALTx` reads its `S`.
The augment supplies bits 31:9 and leaves bits 8:0 alone. Bits 8:0 are the base, so the
redirection is unaffected. Bits 17:9 are the auto-increment, so the `D` register moves.

`AUGD` is the corresponding mechanism for a literal `#D`. The `ALTx` instructions have
no immediate form for `D`: their encodings carry an immediate bit for `S` only, and
their `D` is always a register. An `ALTx` therefore has no immediate `D` to receive a
pending `AUGD`, and the `AUGD` passes to its target.

## How it was proven on a real P2 {#sec-e2-proof}

**Arrangement.** A P2 board with nothing connected to its pins, at 200 MHz. The
measuring code is PASM, started in a fresh cog with `COGINIT` from the program's `DAT`
section. The debug interrupt was enabled in cog 0 only (`DEBUG_COGS = %0000_0001`) and
the measuring cog enabled no interrupts, so nothing could split a sequence; cog 0 only
read the results from hub RAM and printed them. Before each arm, the measuring cog
filled a window of 32 cog registers, `win[0]` to `win[31]`, with a sentinel unique to
the arm and the slot (for arm A6, slot 8: `$5E5E_0608`), and set `idx` to the cog
address of `win[8]`. After each arm it copied the window and `idx` to hub RAM. The
augment was `$3C5C_0A55`: bits 8:0 are `$055`, the target's own 9-bit field, and bits
17:9 are 5, so an `ALTx` that received it would move `idx` by 5.

**Arms and results** (the program's own arm labels; "moved" is `idx` after the arm minus
`idx` before):

| Arm | Sequence | Written | Value | Moved |
|---|---|---|---|---|
| A0 | `MOV win[8],#$055` | `win[8]` | `$0000_0055` | 0 |
| A1 | `AUGS`, `MOV win[8],#$055` | `win[8]` | `$3C5C_0A55` | 0 |
| A2 | `ALTD idx,#0`, `MOV 0-0,#$055` | `win[8]` | `$0000_0055` | 0 |
| A3 | `ALTD idx,sinc` (`$A00`), `MOV 0-0,#$055` | `win[8]` | `$0000_0055` | 5 |
| A4 | `ALTR idx,#3`, `MOV win[0],#$055` | `win[11]` | `$0000_0055` | 0 |
| A5 | `AUGS`, `ALTD idx,sreg4` (4), `MOV 0-0,#$055` | `win[12]` | `$3C5C_0A55` | 0 |
| A6 | `AUGS`, `ALTD idx,#0`, `MOV 0-0,#$055` | `win[8]` | `$3C5C_0A55` | 5 |
| A7 | `AUGS`, `ALTR idx,#3`, `MOV win[0],#$055` | `win[11]` | `$3C5C_0A55` | 5 |

In every arm exactly one window register changed. A0 to A5 are controls, and the
program issues no verdict unless all of them read exactly as expected. A1 shows the
augment reaching an adjacent target. A2 and A4 show that an immediate-`S` `ALTx` with no
`AUGS` pending leaves `idx` unchanged. A3 shows, on this part, that an `S` whose bits
17:9 are 5 moves `idx` by 5 and leaves the redirected register at `win[8]`: the same
field an augment of `$3C5C_0A55` would fill. A5 is the fix: its three instructions are
the lines printed in *The fix*. A6 and A7 are the defect: the `ALTx` moved `idx` by 5,
and the target still wrote `$3C5C_0A55`.

**The `AUGD` half.** Before each of these two arms the measuring cog wrote
`$D5D5_D5D5` to the hub long the arm writes. The control, `AUGD #$1357_9B3C` directly
before `WRLONG #$13C`, wrote `$1357_9B3C`. The test, with `ALTS idxs,#0` between the
`AUGD` and the `WRLONG`, also wrote `$1357_9B3C`; `idxs` read `$0000_0061` before and after. `idxs` held the cog
address of the register the `WRLONG` takes its hub address from, so the `ALTS`
substitution left the `WRLONG`'s address unchanged.

**Repetition.** Nothing in this test depends on timing, so the plan was repetition: the
whole battery ran three times, each in a freshly started cog, and the three hub records
were compared long for long. They were identical. The program was run twice on
2026-09-24, from two builds of the same measuring code, and every measured value matched
between the runs.

**Assembly checked.** Before the run, every `AUGS`, `AUGD` and `ALTx` instruction word
was read back from the assembler listing and its encoding confirmed. The `AUGS`
assembled to `$FF1E2E05`.

## The test program {#sec-e2-program}

The test program is `e2-altx-takes-pending-augs-test.spin2`, a single Spin2 file that
runs the measuring cog in PASM and prints its results with `debug()`. Compile it with
DEBUG enabled (`pnut-ts -d`, or PNut) and run it with the debug terminal open; it prints
about 40 lines and ends in one `VERDICT:` line, or a `RIG FAIL:` line and no verdict if
any control is wrong.

The augment is chosen so that its two fields can be told apart:

```spin2
  AUGV       = $3C5C_0A55          ' AUGS payload: [17:9] = 5, [8:0] = $055
  LO         = AUGV & $1FF         ' $055 = the target's own 9-bit #S
  AUTOINC    = (AUGV >> 9) & $1FF  ' 5 (bit 8 clear -> +5 after sign-extend)
```

The fix arm and the `ALTD` test arm differ only in the form of the `ALTD`'s `S`.
Each arm fills the window, runs its sequence, and dumps the window and `idx` to hub RAM:

```pasm2
' ---- A5 ctrl: WORKAROUND -- register-S ALTD between AUGS and target ----
                mov     armn, #5
                call    #fill
                augs    #AUGV
                altd    idx, sreg4
                mov     0-0, #LO
                call    #dump

' ---- A6 TEST: immediate-#S ALTD between AUGS and target ----
                mov     armn, #6
                call    #fill
                augs    #AUGV
                altd    idx, #0
                mov     0-0, #LO
                call    #dump
```

The two register `S` values used by the controls hold the auto-increment and the base
in their separate fields:

```pasm2
sinc            long    AUTOINC << 9     ' register S: base 0, auto-index +5
sreg4           long    S4               ' register S: base 4, auto-index 0
```

The `AUGD` test places an immediate-`S` `ALTS` between the `AUGD` and its `#D` target,
and records `idxs` before and after:

```pasm2
' ---- D2 TEST: immediate-#S ALTS between AUGD and its #D target ----
                wrlong  sentd, hubd2
                mov     idxs, #hubd2
                wrlong  idxs, ptra[H_IDXS0]
                augd    #AUGVD
                alts    idxs, #0
                wrlong  #LOD, hubd2
                wrlong  idxs, ptra[H_IDXS]
```

## Status {#sec-e2-status}

| Field | Content |
|---|---|
| Erratum | E2 |
| Published by Parallax | Yes, *P2 Documentation*, KNOWN BUGS |
| Found by | Parallax |
| Confirmed on silicon | Yes — 2026-09-24, on a P2 board at 200 MHz, run twice |
| Fix proven on silicon | Yes — 2026-09-24, rule at each use: a register `S` on the `ALTx` (run with `ALTD`) |
| Affects | an `ALTx` with an immediate `#S` between `AUGS` and its target; tested with `ALTD` and `ALTR` |
| Test program | `e2-altx-takes-pending-augs-test.spin2` |
