# Chapter 5: The Goertzel Accumulators Trail by One Clock {#ch-e5}

In the streamer's DDS/Goertzel mode, the sine and cosine accumulators trail the products they sum by one active clock. A `GETXACC` reading taken after a burst of N clocks holds the burst's first `N-1` products; the last one waits in an internal register that no instruction reads, and is added on the first active clock of the next Goertzel burst. Ending each burst with a short burst of zero terms, in the same mode, before reading delivers the held product and leaves nothing to spill into the next burst.

## What the design says {#sec-e5-design}

The P2 Documentation describes the DDS/Goertzel mode as working on every clock of the command:

> This mode is unique, in that it outputs and inputs on every clock in which the command is active.

It then states what becomes of each clock's lookup values:

> The 8-bit sine (byte 3) and cosine (byte 2) values from the lookup RAM will each be multiplied by the bitstream sum (an integer from -3 to +3) and then added into their respective 32-bit accumulators.

Its table of accumulation modes gives the SINC1 case (D[23] = `%0`) as `SIN_ACC += SIN_MUL` and `COS_ACC += COS_MUL`, where each `_MUL` is the bitstream sum times the lookup value. By that description, a command that is active for N clocks adds N products to each accumulator, and a `GETXACC` issued after it returns all N.

The KNOWN BUGS section of the P2 Documentation does not list this behaviour. The clean-room design study found the same intent stated inside the design material as well: notes in the design describe the per-clock product as feeding the accumulator, with both valid on the same clock. That material is not quoted here.

## What the part does {#sec-e5-part}

On each active clock of a Goertzel burst, each accumulator adds the product formed on the **previous** active clock, not the product formed on that clock. After a burst of N active clocks:

- the accumulator holds the burst's first `N-1` products, plus the last product of the previous Goertzel burst if one was still held when this burst began;
- the burst's last product is held in an internal register. `GETXACC` does not return it, and it does not change while the streamer is idle;
- the first active clock of the next Goertzel burst adds the held product to the accumulator, ahead of that burst's own products.

Both accumulations behave this way: the cosine accumulation that `GETXACC` writes into D, and the sine accumulation it places into the next instruction's S. No product is lost; the last product of each burst arrives one burst late.

This was confirmed on silicon in SINC1 mode (D[23] = `%0`), with one input pin summed, for bursts of 64 and 65 clocks, each started by `XINIT` from an idle streamer and read with the streamer idle. The test ran no other streamer mode between bursts, so whether a command in another mode disturbs the held product is not established.

## The symptom {#sec-e5-symptom}

A program that runs a Goertzel burst of N clocks, waits for it to end and reads with `GETXACC` gets a sum short by exactly the burst's last product. Reading again later does not recover it: in the test, a second reading 1000 clocks after the first had moved by 0 in all 16 sequences. The missing product appears in the next Goertzel burst's reading, which is one product long.

When every product is the same (a steady input and one lookup value), the carried product stands in for the missing one from the second burst on: in the test, a burst that directly followed another burst read `N*C`, where a burst that followed a zero burst read `(N-1)*C`. When the input or the lookup value changes from clock to clock, each reading is the previous burst's last product plus the first `N-1` products of its own burst.

The shortfall was one product at both burst lengths tested. The idle reading is stable, and every product reaches the accumulator eventually.

## The workaround {#sec-e5-workaround}

Follow every burst with a short zero-term burst before reading. The zero burst uses the same mode bits in `XINIT`'s D operand, with the four pin-summation bits of its S operand, S[15:12], all clear, so that every product it forms is zero. Its first active clock adds the held product to the accumulator, and it leaves a zero product held. The reading after it holds all N products of the measured burst, and nothing spills into the next burst. The test used a zero burst of 4 clocks.

```pasm2
        getxacc base_x          ' reading before the burst
        mov     base_y, 0-0     ' sine accumulation follows
        xinit   dburst, imm_on  ' N-clock burst, pin inputs on
        waitx   ##500           ' wait until the burst has ended
        xinit   dzero, imm_off  ' zero-term burst: S[15:12] = 0
        waitx   ##500           ' adds the held term; leaves 0 held
        getxacc x               ' now all N terms are in
        mov     y, 0-0
        sub     x, base_x       ' cosine sum of the N clocks
        sub     y, base_y       ' sine sum of the N clocks
```

Here `dburst` is the Goertzel mode word with a count of N, `dzero` is the same mode word with a count of 4, and `imm_on` and `imm_off` differ only in S[15:12]. Three conditions come with the code:

- The reading is taken as the difference of two readings because `GETXACC` does not clear the accumulators while the streamer is idle; [Chapter 4](#ch-e4) covers that erratum.
- The baseline reading holds no pending product only if the burst before it also ended with a zero burst. The test ran one zero burst before its first measurement for this reason.
- `XINIT` issues its command immediately, so each `XINIT` waits for the previous burst to end. The test waited a fixed 500 clocks after each `XINIT`, which is well past the end of a 64- or 65-clock burst at one NCO rollover per clock; a longer burst or a lower NCO frequency needs a longer wait. The test did not use `WAITXFI`.

**The workaround was proven on silicon.** In all 16 sequences the reading after the zero burst had gained exactly N products over the reading before the measured burst, and the next burst read `(N-1)*C`, so no product was carried past the zero burst. The test had no DAC output enabled. With DAC channels enabled, the zero burst is a DDS/Goertzel command like any other and, by the description quoted above, outputs on each of its clocks; that case was not tested.

## Why it happens {#sec-e5-why}

The account below is the clean-room design study's reading of the mechanism, stated at the level of the programmer's model. The measurements in the next section match it.

On each active clock of a Goertzel burst, two registers update together. One is an internal product register: it takes the product formed on that clock from the lookup value and the pin sum. The other is the accumulator that `GETXACC` reads: it adds the value the product register held going into that clock, which is the product formed on the previous active clock. Both update on the same clock edge, so the accumulator is always one product behind the product register.

When a burst ends, both registers stop updating. The last product formed stays in the product register. No instruction reads that register and nothing changes it while the streamer is idle, so waiting does not deliver it. On the first active clock of the next Goertzel burst the accumulator adds it, while the product register takes that burst's first product.

A zero-term burst works for the same reason. Its first clock moves the held product into the accumulator, and its own products are all zero, so it leaves zero behind.

In SINC1 mode the product register is replaced on every clock. In SINC2 mode (D[23] = `%1`), by the study's reading, the register keeps its value through a zero burst instead of being replaced by zero, so the zero-burst workaround does not apply there. SINC2 was not tested.

## How it was proven {#sec-e5-proven}

**The arrangement.** One P2 board at 200 MHz, nothing attached to P3.

- All streamer work and every `GETXACC` ran in a measuring cog started by `COGINIT`. The debugger was confined to cog 0 (`DEBUG_COGS = %0000_0001`), so no debug interrupt ran in the measuring cog (cog 1 in the run). Cog 0 only collected and printed the results.
- The measuring cog drove P3 as a plain output, low for half the run and high for the other half, in place of an ADC bitstream. The streamer took its inputs from pin group 0 (P0 to P3) with only base pin +3 summed.
- All 512 LUT longs held `$2513_0000`: cosine byte `$13` (19) and sine byte `$25` (37). Every cosine product was therefore +19 or -19 and every sine product +37 or -37, the sign set by P3. With S[19] clear, the P2 Documentation's summation table counts a 0 as -1 and a 1 as +1, so the cosine product C is -19 with P3 low and +19 with P3 high.
- `SETXFRQ` was set to `$8000_0000`, one NCO rollover per clock, so a command count of N is a burst of N clocks.
- The mode word was `$F007_0000` plus the count: DDS/Goertzel, SINC1, no DAC output, pin group 0. A product burst used S = `$0000_80C3` (S[15] set: base pin +3 summed); a zero burst used S = `$0000_00C3` (S[15:12] clear) and a count of 4.
- Every reading was taken 500 clocks after the `XINIT` that preceded it, with the streamer idle.

**One sequence**, run for N = 64 and N = 65, each from its own start:

| Step | Streamer command | Then read |
|---|---|---|
| 1 | zero burst | `B` |
| 2 | burst of N clocks | `R1`; 1000 clocks later, `R1b` |
| 3 | zero burst (the workaround) | `R2` |
| 4 | burst of N clocks | `R3` |
| 5 | burst of N clocks | `R4` |
| 6 | zero burst | `R5` |

The quantities are `d1 = R1-B`, `d2 = R2-R1`, `d3 = R3-R2`, `d4 = R4-R3` and `d5 = R5-R4`. Steps 4 to 6 test the carry: two bursts back to back, then a zero burst. The run was four repetitions of both lengths at P3 low, then the same at P3 high: 16 sequences.

**The outcomes, written into the program before the run**, in units of the per-clock product C:

| Hypothesis | `d1` | `d2` | `d3`, `d4`, `d5` |
|---|---|---|---|
| One-clock lag (the prediction) | `(N-1)*C` | `C` | `(N-1)*C`, `N*C`, `C` |
| No lag | `N*C` | 0 | `N*C`, `N*C`, 0 |
| Last product lost | `(N-1)*C` | 0 | `(N-1)*C`, `(N-1)*C`, 0 |

A nonzero `R1b-R1` under any of them would mean the accumulator moved while the streamer was idle, which none of the three allows.

**The controls**, each of which had to pass before the program would print a verdict:

- the LUT read back `$2513_0000` at addresses `$0C3`, `0` and `$1FF`;
- `TESTP` read P3 at its driven level before and after every sequence;
- a zero burst following a zero burst added nothing (the reading before step 1 equalled `B`);
- every one of `d1` to `d5` was a whole multiple of 19;
- C was measured without assuming any hypothesis, as `R2-B` at N = 65 minus `R2-B` at N = 64, which is one product under all three. It had to be 19 in magnitude, the same in every repetition, and opposite in sign between P3 low and P3 high.

**The results.** Every control passed. C measured -19 in all four repetitions at P3 low and 19 in all four at P3 high. The first repetition at each level and length read:

| P3 | N | `d1` | `R1b-R1` | `d2` | `d3` | `d4` | `d5` |
|---|---|---|---|---|---|---|---|
| low | 64 | `-1_197` | 0 | `-19` | `-1_197` | `-1_216` | `-19` |
| low | 65 | `-1_216` | 0 | `-19` | `-1_216` | `-1_235` | `-19` |
| high | 64 | `1_197` | 0 | `19` | `1_197` | `1_216` | `19` |
| high | 65 | `1_216` | 0 | `19` | `1_216` | `1_235` | `19` |

The other three repetitions of each row read the same values. All 16 sequences match the one-clock-lag row of the outcomes table: `d1 = (N-1)*C`, `d2 = C`, `R1b-R1 = 0`, and the carry steps `(N-1)*C`, `N*C`, `C`. The sine accumulation shows the same pattern with a product of 37: at P3 low and N = 64 it read `d1=-2_331`, `d2=-37`, `d3=-2_331`, `d4=-2_368`, `d5=-37`, and it read the lag pattern and the carry pattern in 16 of 16 sequences.

The test ran on 2026-09-24, twice, from two builds of the same program with identical measuring code. Every measured value matched between the two runs.

## The test program {#sec-e5-program}

The test program is `e5-goertzel-one-clock-lag-test.spin2` in the examples archive. Its Spin2 code in cog 0 starts the measuring cog, waits for it to finish, prints every raw reading and delta, checks the controls, and prints the verdict. The measuring cog is PASM2 in the program's DAT block and is the only code that touches the streamer.

The four command words sit at the end of the measuring code. `dmode_` is the Goertzel mode word without a count; each sequence ORs N into it to make the burst word. `dz_` is the zero burst's word with its count of 4, and `imz_` and `imk_` are the two S operands:

```pasm2
dmode_          long    MODE_G
dz_             long    MODE_G | ZCOUNT
imz_            long    IMM_Z
imk_            long    IMM_K
```

Each sequence runs the burst and the workaround like this. The program's comments call a product burst a K burst and the S operand `imm`, and `dk_` holds the burst word for the current N. `GETXACC` places the sine accumulation into the S field of the next instruction, so each `GETXACC` is followed by `mov ..., 0-0`, which receives it:

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

The carry steps follow directly, with no zero burst between the two product bursts:

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

## Status {#sec-e5-status}

| Field | Content |
|---|---|
| Erratum | E5 |
| Published by Parallax | No |
| Found by | Predicted by the clean-room design study; confirmed here |
| Confirmed on silicon | Yes — 2026-09-24, on a P2 board at 200 MHz, run twice |
| Workaround proven on silicon | Yes |
| Affects | `GETXACC` readings after a DDS/Goertzel burst, sine and cosine; tested in SINC1 mode with bursts of 64 and 65 clocks started by `XINIT` |
| Test program | `e5-goertzel-one-clock-lag-test.spin2` |
