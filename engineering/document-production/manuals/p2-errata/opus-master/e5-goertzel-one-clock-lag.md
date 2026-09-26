# Erratum E5: The Goertzel Accumulators Trail by One Clock {#ch-e5}

::: caution
**Expected:** A `GETXACC` reading after a DDS/Goertzel burst of N clocks holds all N of the burst's terms (P2 Documentation, *DDS/Goertzel*).

**Actual:** It holds the first N-1; the last term is held back and added on the first clock of the next Goertzel burst.

**Fix:** Run each SINC1 burst through the `burst_sums` helper routine, which ends every burst with a zero-term burst before reading; see *The fix*.
:::

The erratum affects PASM code that runs DDS/Goertzel bursts and reads the accumulators with `GETXACC` after each one: every reading is short by the burst's last term, and the next burst's reading carries it. The erratum was predicted by the clean-room design study and confirmed on silicon.

## What the P2 is documented to do {#sec-e5-documented}

The P2 Documentation describes the DDS/Goertzel mode as working on every clock of the command:

> This mode is unique, in that it outputs and inputs on every clock in which the command is active.

It then states what becomes of each clock's lookup values:

> The 8-bit sine (byte 3) and cosine (byte 2) values from the lookup RAM will each be multiplied by the bitstream sum (an integer from -3 to +3) and then added into their respective 32-bit accumulators.

Its table of accumulation modes gives the SINC1 case (D[23] = `%0`) as `SIN_ACC += SIN_MUL` and `COS_ACC += COS_MUL`, where each `_MUL` is the bitstream sum times the lookup value. By that description, a command that is active for N clocks adds N terms to each accumulator, and a `GETXACC` issued after it returns all N.

The KNOWN BUGS section of the P2 Documentation does not list this behaviour.

## What the P2 actually does {#sec-e5-actual}

On each active clock of a Goertzel burst, each accumulator adds the term formed on the **previous** active clock, not the term formed on that clock. After a burst of N active clocks:

- the accumulator holds the burst's first N-1 terms, plus the last term of the previous Goertzel burst if one was still held when this burst began;
- the burst's last term is held in an internal register. `GETXACC` does not return it, and it does not change while the streamer is idle;
- the first active clock of the next Goertzel burst adds the held term to the accumulator, ahead of that burst's own terms.

Both accumulations behave this way: the cosine accumulation that `GETXACC` writes into D, and the sine accumulation it places into the next instruction's S. No term is lost; the last term of each burst arrives one burst late.

This was confirmed on silicon in SINC1 mode, with one input pin summed, for bursts of 64 and 65 clocks, each started by `XINIT` from an idle streamer and read with the streamer idle. The test ran no other streamer mode between bursts, so whether a command in another mode disturbs the held term is not established.

## What your program sees {#sec-e5-sees}

If your program runs a Goertzel burst of N clocks, waits for it to end and reads with `GETXACC`, you get a sum short by exactly the burst's last term. Reading again later does not recover it: in the test, a second reading 1000 clocks after the first had moved by 0 in all 16 sequences. The missing term appears in the next Goertzel burst's reading, which is one term long.

When every term is the same (a steady input and one lookup value), the carried term stands in for the missing one from the second burst on: in the test, a burst that directly followed another burst read `N*C`, where a burst that followed a zero burst read `(N-1)*C`. When the input or the lookup value changes from clock to clock, each reading is the previous burst's last term plus the first N-1 terms of its own burst.

The shortfall was one term at both burst lengths tested. The idle reading is stable, and every term reaches the accumulator eventually.

The difference of two idle readings is still needed as well, because `GETXACC` does not clear the accumulators while the streamer is idle; that is Erratum E4, and the fix below removes both.

## The fix {#sec-e5-fix}

```pasm2
' Runs one DDS/Goertzel burst (SINC1 only) and returns its exact
' sums. Put your XINIT D and S in burst_mode and burst_sel, then
' CALL #burst_sums with the streamer idle. It leaves the burst's
' cosine sum in cos_sum and its sine sum in sin_sum.
burst_sums  mov     zero_mode, burst_mode   ' zero burst: your mode,
            setword zero_mode, #4, #0       '   count 4,
            mov     zero_sel, burst_sel     '   your S with every
            setnib  zero_sel, #0, #3        '   input off: S[15:12]=0
            xinit   zero_mode, zero_sel     ' adds any held term
            waitxfi
            getxacc cos_base                ' idle read: no clear
            mov     sin_base, 0-0
            xinit   burst_mode, burst_sel   ' your burst
            waitxfi
            xinit   zero_mode, zero_sel     ' adds its last term
            waitxfi
            getxacc cos_sum                 ' idle read again
            mov     sin_sum, 0-0
            sub     cos_sum, cos_base       ' cosine sum, all N terms
            sub     sin_sum, sin_base       ' sine sum, all N terms
            ret

burst_mode  long    $F007_0100              ' your D (count 256 here)
burst_sel   long    $0008_80A5              ' your S
zero_mode   long    0
zero_sel    long    0
cos_base    long    0
sin_base    long    0
cos_sum     long    0
sin_sum     long    0
```

Each call leaves in `cos_sum` and `sin_sum` the sums of your burst alone, all N of its terms, and leaves no term held for the next burst: a *helper routine*, for SINC1 mode.

On silicon, this block returned exactly N terms on both sums in all 60 calls of its test program, for bursts of 1 to 1001 clocks at both input levels; in the 6 calls made while an earlier burst's term was still held, it added that term before its first reading, and it left no term for any later call; see *How it was proven on a real P2*.

The routine is for SINC1 mode. In SINC2 mode its zero burst has not been tested as a flush, and the routine is not recommended there. SINC2 has its own, separate constraint, which is documented and is not this erratum: the P2 Documentation's note on Goertzel SINC2 mode, by Chip Gracey (2024.12.16), states that a varying number of iterations in a Goertzel cycle corrupts the current and next samples. Its two remedies held on a real P2 in the test program `e5-goertzel-sinc2-iteration-count-test.spin2` (2026-09-25, at 200 MHz, run twice). With every NCO cycle the same length (`SETXFRQ` of `$0080_0000`, 256 clocks per cycle, 2,048-clock commands chained with `XCONT`), 0 of 1,020 SINC2 samples were off. With each command issued by `XZERO`, at a `SETXFRQ` value of `$0080_0040` with 8 NCO cycles per command and of `$00A3_D70C` with 100 and with 25,000, every command kept one length and 0 of 1,020, 0 of 2,044 and 0 of 12 samples changed, where `XCONT` at the same settings gave 30, 12 and 4 corrupted samples.

This is the same routine Erratum E4 prints, because one call removes both errata. To use it, put your `XINIT` D operand (the Goertzel mode word with your count) in `burst_mode` and your S operand in `burst_sel`, set `SETXFRQ` as your program already does, and `CALL #burst_sums` with the streamer idle. The values printed in `burst_mode` and `burst_sel` are the test program's.

The zero bursts are your mode word with a count of 4 and S[15:12] clear, so every term they form is zero. The first one's first clock adds whatever term an earlier burst left held, so the before reading is complete; the second adds your burst's last term, and leaves a zero term held. Both readings are taken with the streamer idle, where `GETXACC` clears nothing (Erratum E4), so their difference is your burst.

**Cost.** Each call runs two zero bursts of 4 NCO rollovers each, at your `SETXFRQ` rate, besides your burst, and the cog waits in `WAITXFI` until each command has finished. The routine is 17 instructions, and 8 longs of cog RAM hold its operands and results.

**Limits.**

- **One burst at a time, from an idle streamer.** The routine starts every command with `XINIT`, which issues it at once, so it does not fit a continuous stream of commands chained with `XCONT`.
- **Conditions of the test.** The fix's test program ran the routine once, from cog RAM on a P2 board at 200 MHz, with an NCO frequency of `$8000_0000`, one input pin, no DAC output, and bursts of 1 to 1001 clocks, the first call of each record made with an earlier burst's term still held. With DAC channels enabled, the zero bursts are DDS/Goertzel commands like any other and, by the P2 Documentation, output on each of their clocks; that case, more than one input pin, other NCO frequencies and hub execution were not tested.

## Why it happens {#sec-e5-why}

The account below is the clean-room design study's reading of the mechanism, stated at the level of the programmer's model. The measurements in the next section match it.

On each active clock of a Goertzel burst, two registers update together. One is an internal term register: it takes the term formed on that clock from the lookup value and the pin sum. The other is the accumulator that `GETXACC` reads: it adds the value the term register held going into that clock, which is the term formed on the previous active clock. Both update on the same clock edge, so the accumulator is always one term behind the term register.

When a burst ends, both registers stop updating. The last term formed stays in the term register. No instruction reads that register and nothing changes it while the streamer is idle, so waiting does not deliver it. On the first active clock of the next Goertzel burst the accumulator adds it, while the term register takes that burst's first term.

A zero-term burst works for the same reason. Its first clock moves the held term into the accumulator, and its own terms are all zero, so it leaves zero behind.

## How it was proven on a real P2 {#sec-e5-proof}

**The arrangement.** One P2 board at 200 MHz, nothing attached to P3.

- All streamer work and every `GETXACC` ran in a measuring cog started by `COGINIT`. The debugger was confined to cog 0 (`DEBUG_COGS = %0000_0001`), so no debug interrupt ran in the measuring cog (cog 1 in the run). Cog 0 only collected and printed the results.
- The measuring cog drove P3 as a plain output, low for half the run and high for the other half, in place of an ADC bitstream. The streamer took its inputs from pin group 0 (P0 to P3) with only base pin +3 summed.
- All 512 LUT longs held `$2513_0000`: cosine byte `$13` (19) and sine byte `$25` (37). Every cosine term was therefore +19 or -19 and every sine term +37 or -37, the sign set by P3. With S[19] clear, the P2 Documentation's summation table counts a 0 as -1 and a 1 as +1, so the cosine term C is -19 with P3 low and +19 with P3 high.
- `SETXFRQ` was set to `$8000_0000`, one NCO rollover per clock, so a command count of N is a burst of N clocks.
- The mode word was `$F007_0000` plus the count: DDS/Goertzel, SINC1, no DAC output, pin group 0. A term burst used S = `$0000_80C3` (S[15] set: base pin +3 summed); a zero burst used S = `$0000_00C3` (S[15:12] clear) and a count of 4.
- Every reading was taken 500 clocks after the `XINIT` that preceded it, with the streamer idle.

**One sequence**, run for N = 64 and N = 65, each from its own start:

| Step | Streamer command | Then read |
|---|---|---|
| 1 | zero burst | `B` |
| 2 | burst of N clocks | `R1`; 1000 clocks later, `R1b` |
| 3 | zero burst | `R2` |
| 4 | burst of N clocks | `R3` |
| 5 | burst of N clocks | `R4` |
| 6 | zero burst | `R5` |

The quantities are `d1 = R1-B`, `d2 = R2-R1`, `d3 = R3-R2`, `d4 = R4-R3` and `d5 = R5-R4`. Steps 4 to 6 test the carry: two bursts back to back, then a zero burst. The run was four repetitions of both lengths at P3 low, then the same at P3 high: 16 sequences.

**The outcomes, written into the program before the run**, in units of the per-clock term C:

| Hypothesis | `d1` | `d2` | `d3`, `d4`, `d5` |
|---|---|---|---|
| One-clock lag (the prediction) | `(N-1)*C` | `C` | `(N-1)*C`, `N*C`, `C` |
| No lag | `N*C` | 0 | `N*C`, `N*C`, 0 |
| Last term lost | `(N-1)*C` | 0 | `(N-1)*C`, `(N-1)*C`, 0 |

A nonzero `R1b-R1` under any of them would mean the accumulator moved while the streamer was idle, which none of the three allows.

**The controls**, each of which had to pass before the program would print a verdict:

- the LUT read back `$2513_0000` at addresses `$0C3`, `0` and `$1FF`;
- `TESTP` read P3 at its driven level before and after every sequence;
- a zero burst following a zero burst added nothing (the reading before step 1 equalled `B`);
- every one of `d1` to `d5` was a whole multiple of 19;
- C was measured without assuming any hypothesis, as `R2-B` at N = 65 minus `R2-B` at N = 64, which is one term under all three. It had to be 19 in magnitude, the same in every repetition, and opposite in sign between P3 low and P3 high.

**The results.** Every control passed. C measured -19 in all four repetitions at P3 low and 19 in all four at P3 high. The first repetition at each level and length read:

| P3 | N | `d1` | `R1b-R1` | `d2` | `d3` | `d4` | `d5` |
|---|---|---|---|---|---|---|---|
| low | 64 | `-1_197` | 0 | `-19` | `-1_197` | `-1_216` | `-19` |
| low | 65 | `-1_216` | 0 | `-19` | `-1_216` | `-1_235` | `-19` |
| high | 64 | `1_197` | 0 | `19` | `1_197` | `1_216` | `19` |
| high | 65 | `1_216` | 0 | `19` | `1_216` | `1_235` | `19` |

The other three repetitions of each row read the same values. All 16 sequences match the one-clock-lag row of the outcomes table: `d1 = (N-1)*C`, `d2 = C`, `R1b-R1 = 0`, and the carry steps `(N-1)*C`, `N*C`, `C`. The sine accumulation shows the same pattern with a term of 37: at P3 low and N = 64 it read `d1=-2_331`, `d2=-37`, `d3=-2_331`, `d4=-2_368`, `d5=-37`, and it read the lag pattern and the carry pattern in 16 of 16 sequences.

The zero burst of step 3 is the kind the fix uses: a count of 4 with S[15:12] clear. In all 16 sequences the reading after it had gained exactly N terms over the reading before the measured burst, and the next burst read `(N-1)*C`, so no term was carried past the zero burst. This test waited a fixed 500 clocks after each `XINIT` rather than using `WAITXFI`, and had no DAC output enabled.

The test ran on 2026-09-24, twice, from two builds of the same program with identical measuring code. Every measured value matched between the two runs.

### The fix's test {#sec-e5-fix-proof}

The fix ran in the test program described in Erratum E4, which calls the printed routine byte for byte. For this erratum its checks are these. The uncorrected part of each record must show the lag in the same run: a 64-clock burst read 63 × C, the 65-clock burst right after it read 65 × C, a zero burst alone read C, and a 7-clock burst read 6 × C, with its last term left held. The first call of `burst_sums` in each record starts with that term held, so its before reading must have gained exactly C, and every later call's nothing; every call must return N × C, for N = 1 to 1001. A result of (N-1) × C would mean the zero burst did not deliver the last term.

**The results.** Every control passed, and the per-clock term measured C = 61 on the cosine sum and 23 on the sine sum at P3 low, -61 and -23 at P3 high, in every record. The uncorrected part showed the lag in all 12 rows (6 records, cosine and sine): at P3 low, on the cosine sum, the 64-clock burst read 3,843 (63 × 61), the 65-clock burst right after it 3,965 (65 × 61), the zero burst alone 61, and the 7-clock burst 366 (6 × 61); on the sine sum 1,449, 1,495, 23 and 138; at P3 high the same values negated. The first call of each record found exactly C waiting: its before reading was 61 above the 7-clock burst's reading at P3 low (77,165 against 77,104 in the first record) and 61 below it at P3 high (396,744 against 396,805 in the fourth). Every later call's before reading equalled the program's own reading after the previous call, so no call left a term behind. Every one of the 60 calls returned N × C on both sums, from 61 for N = 1 to 61,061 for N = 1001 on the cosine sum at P3 low, and -23 to -23,023 on the sine sum at P3 high; none returned (N-1) × C.

The test program was run once, on 2026-09-26, on a P2 board at 200 MHz. The values above are read from its raw lines, not from its verdict line.

## The test program {#sec-e5-program}

The test program is `e5-goertzel-one-clock-lag-test.spin2` in the examples archive. Its Spin2 code in cog 0 starts the measuring cog, waits for it to finish, prints every raw reading and delta, checks the controls, and prints the verdict. The measuring cog is PASM2 in the program's DAT block and is the only code that touches the streamer.

Each sequence runs the burst and the zero burst like this. The program's comments call a term burst a K burst and the S operand `imm`, and `dk_` holds the burst word for the current N; `dz_` is the zero burst's word with its count of 4, and `imz_` and `imk_` are the two S operands. `GETXACC` places the sine accumulation into the S field of the next instruction, so each `GETXACC` is followed by `mov ..., 0-0`, which receives it:

```pasm2
                xinit   dk_, imk_               ' BURST: count N, imm[15]=1
                waitx   ##WAIT_IDLE
                getxacc r1x_                    ' R1
                mov     r1y_, 0-0
                waitx   ##WAIT_R1B
                getxacc r1bx_                   ' R1b, 1000 clocks later
                mov     r1by_, 0-0

                xinit   dz_, imz_               ' IDIOM: zero burst
                waitx   ##WAIT_IDLE
                getxacc r2x_                    ' R2
                mov     r2y_, 0-0
```

The carry steps follow directly, with no zero burst between the two term bursts:

```pasm2
                xinit   dk_, imk_               ' CARRY ARM: K burst
                waitx   ##WAIT_IDLE
                getxacc r3x_                    ' R3
                mov     r3y_, 0-0

                xinit   dk_, imk_               ' second K burst right after
                waitx   ##WAIT_IDLE
                getxacc r4x_                    ' R4
                mov     r4y_, 0-0

                xinit   dz_, imz_               ' zero burst flushes
                waitx   ##WAIT_IDLE
                getxacc r5x_                    ' R5
                mov     r5y_, 0-0
```

`WAIT_IDLE` is 500 clocks and `WAIT_R1B` is 1000. Before the first sequence the measuring cog fills all 512 LUT longs, reads three of them back for the LUT control, drives P3 and runs one zero burst.

To run it, compile with `pnut-ts -d` and load it with DEBUG enabled (2 Mbaud). P3 must be free: the program drives it. A run that decides the question prints no `RIG FAIL` lines, a `C measured` line showing -19 and 19, and one `VERDICT:` line. Every raw reading is printed as well, so the verdict can be re-derived from the output rather than taken from the program.

The fix's test program is `e4-e5-fix-read-sums-test.spin2`, described in Erratum E4. Its uncorrected part shows this erratum in the same run as the fix; the second half of it reads like this, a `GETXACC` "to clear" followed by the 65-clock burst, whose reading carries the 64-clock burst's held term:

```pasm2
                mov     dk_, dmode_
                setword dk_, #N_NAIVE_B, #0
                getxacc ax_                     ' P2: "clear" again
                mov     ay_, 0-0
                xinit   dk_, son_               ' burst N2, right after
                waitxfi
                getxacc bx_                     ' R2
                mov     by_, 0-0
                wrlong  ax_, ptrb++             ' R_P2X
                wrlong  ay_, ptrb++
                wrlong  bx_, ptrb++             ' R_R2X
                wrlong  by_, ptrb++
```

The test program `e5-goertzel-sinc2-iteration-count-test.spin2`, cited in *The fix*, is the check of the P2 Documentation's separate SINC2 constraint, not of this erratum.

## Status {#sec-e5-status}

| Field | Content |
|---|---|
| Erratum | E5 |
| Published by Parallax | No |
| Found by | Predicted by the clean-room design study; confirmed here |
| Confirmed on silicon | Yes — 2026-09-24, on a P2 board at 200 MHz, run twice |
| Fix proven on silicon | Yes — 2026-09-26, on a P2 board at 200 MHz, run once; helper routine (SINC1) |
| Affects | `GETXACC` readings after a DDS/Goertzel burst in SINC1 mode, sine and cosine; tested with bursts of 64 and 65 clocks started by `XINIT` |
| Test program | `e5-goertzel-one-clock-lag-test.spin2`; the fix: `e4-e5-fix-read-sums-test.spin2` |
