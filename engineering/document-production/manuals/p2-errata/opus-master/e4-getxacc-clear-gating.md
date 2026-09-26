# Erratum E4: GETXACC Clears Only During a Goertzel Burst {#ch-e4}

::: caution
**Expected:** `GETXACC` reads the streamer's Goertzel cosine and sine accumulators and clears them (P2 Documentation, *STREAMER* and *DDS/Goertzel*).

**Actual:** The clear acts only while a DDS/Goertzel command is running; with the streamer idle, `GETXACC` clears nothing, and each burst adds to what earlier bursts left.

**Fix:** Run each burst through the `burst_sums` helper routine, which reads the accumulators with the streamer idle before and after your burst and subtracts; see *The fix*.
:::

The erratum affects PASM code that runs DDS/Goertzel bursts one at a time, with the streamer idle between them, and relies on `GETXACC` to clear the accumulators: a reading taken after each burst, or a `GETXACC` issued before an `XINIT` to start from zero. A `GETXACC` issued while a Goertzel command is running clears as documented. The erratum was predicted by the clean-room design study and confirmed on silicon; Parallax does not list it.

## What the P2 is documented to do {#sec-e4-documented}

The P2 Documentation states the clear in its streamer instruction table and again in its description of the DDS/Goertzel mode. The instruction table's entry for `GETXACC` reads:

> Get Goertzel X into D and Y into next S, clear X and Y

The DDS/Goertzel mode description reads:

> After some number of complete NCO cycles, both accumulators can be simultaneously captured into holding registers and cleared using the GETXACC instruction. GETXACC writes the captured cosine accumulation into D and places the captured sine accumulation into the next instruction's S value. Subsequent GETXACC instructions will return the same values until a new streamer command executes.

The SINC1/SINC2 table that follows that description carries the column heading:

> Accumulations (SIN_ACC/COS_ACC are read and cleared by GETXACC)

None of the three places makes the clear depend on the streamer's mode or on whether a streamer command is running.

## What the P2 actually does {#sec-e4-actual}

In this erratum a *Goertzel burst* is one DDS/Goertzel streamer command for the clocks it runs, and a *term* is the product the streamer adds to each accumulator on each of those clocks.

- **Streamer idle.** `GETXACC` returns the current value of the accumulators and leaves them as they were. Repeated reads return the same value, bit for bit.
- **Streamer running another mode.** One other mode was tested: the immediate-to-pins mode, one pin wide, with its output disabled, started by `XINIT`. A `GETXACC` issued as the next instruction after that `XINIT`, and another issued 100 clocks later with the command still running, both returned the value from before the `XINIT` and cleared nothing.
- **A new Goertzel burst.** The burst adds its terms to the value the accumulators already hold. Starting a streamer command does not reset them.
- **During a Goertzel burst.** The clear acts. `GETXACC` returns everything accumulated so far, including what earlier bursts left, and the accumulation continues from the clear. The read plus the next read hold exactly what the same burst gives when it is not read: no term is lost and none is counted twice.

The sine accumulator behaved as the cosine accumulator did in every case measured.

The clear during a running command also held in continuous streams. In the SINC1 streams of the test program `e5-goertzel-sinc2-iteration-count-test.spin2` (a check of the P2 Documentation's SINC2 constraint, run on 2026-09-25), commands were chained with `XCONT` and one `GETXACC` was issued per command; every reading analysed (all but the first three of each stream) equalled the per-clock term times the number of clocks since the previous reading.

## What your program sees {#sec-e4-sees}

If your program issues one `GETXACC` after each burst and treats the reading as that burst's result, it gets a running total instead: each reading holds the burst plus everything accumulated since the last clear. In one repetition of the test program, the reading before a 256-clock burst was 14,823 and the reading after it was 30,378; the burst itself contributed 15,555.

A `GETXACC` issued before an `XINIT` in order to zero the accumulators returns the running total and zeroes nothing.

A `GETXACC` inside a Goertzel burst returns the leftover from earlier bursts together with the part of the burst run so far. In the test program, a read 29 terms into a burst that started from 17,080 returned 18,849.

What does not go wrong: the accumulation itself is exact. Every difference the test program measured was a whole multiple of the per-clock term, the same burst gave the same difference from every starting value, and a read inside a burst split it into two parts that sum exactly to the unread burst. Consecutive idle reads return the same value, as the documentation says they do.

The difference of two idle readings is still one term short of your burst: the burst's last term is held back until the next Goertzel burst. That is Erratum E5, and the fix below removes both.

## The fix {#sec-e4-fix}

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

Each call leaves in `cos_sum` and `sin_sum` the sums of your burst alone, all N of its terms, whatever the accumulators held before the call: a *helper routine*.

On silicon, this block returned exactly N terms on both sums in all 60 calls of its test program, for bursts of 1 to 1001 clocks at both input levels, including 6 calls made while an earlier burst's term was still held; see *How it was proven on a real P2*.

To use it, put your `XINIT` D operand (the Goertzel mode word with your count) in `burst_mode` and your S operand in `burst_sel`, set `SETXFRQ` as your program already does, and `CALL #burst_sums` with the streamer idle. The values printed in `burst_mode` and `burst_sel` are the test program's: SINC1, no DAC output, input pins P0 to P3, a count of 256, with P3 inverted and summed and a lookup offset of `$0A5`.

The routine takes its two readings with the streamer idle, where `GETXACC` clears nothing, so their difference is your burst whatever came before it. The zero bursts deal with Erratum E5: each is your mode word with a count of 4 and S[15:12] clear, so every term it forms is zero. The first delivers any term an earlier burst left held, so the before reading is complete; the second delivers your burst's last term before the after reading.

**Cost.** Each call runs two zero bursts of 4 NCO rollovers each, at your `SETXFRQ` rate, besides your burst, and the cog waits in `WAITXFI` until each command has finished. The routine is 17 instructions, and 8 longs of cog RAM hold its operands and results.

**Limits.**

- **SINC1 only.** In SINC2 mode the zero burst has not been tested as a flush, and the routine is not recommended there; *The fix* of Erratum E5 notes the P2 Documentation's separate SINC2 constraint.
- **One burst at a time, from an idle streamer.** The routine starts every command with `XINIT`, which issues it at once, so it does not fit a continuous stream of commands chained with `XCONT`. A `GETXACC` inside a running Goertzel command clears as documented.
- **Conditions of the test.** The fix's test program ran the routine once, from cog RAM on a P2 board at 200 MHz, with an NCO frequency of `$8000_0000`, one input pin, no DAC output, and bursts of 1 to 1001 clocks. With DAC channels enabled, the zero bursts are DDS/Goertzel commands like any other and, by the P2 Documentation, output on each of their clocks; that case, more than one input pin, other NCO frequencies, hub execution, and accumulator values near the 32-bit limit were not tested.

## Why it happens {#sec-e4-why}

The clean-room design study traces the behaviour to how the accumulators are updated. Each accumulator is rewritten only on the clocks of a running DDS/Goertzel command; on every other clock it holds its value, whatever instruction the cog executes. The clear in `GETXACC` is not a separate action on the accumulator. It is folded into that same per-clock update: on the clock the clear arrives, the update starts the accumulator over instead of adding to its old value. When no update happens, because the streamer is idle or running a different mode, the clear has nothing to act through, and the accumulator keeps its value.

The read does not depend on the update. `GETXACC` returns the accumulator's current value, which is why idle reads repeat exactly and why a read inside a burst returns the running sum. When the clear does act, the accumulator starts over from the one term that has been formed but not yet added (Erratum E5), and that term appears in the next reading. That is why a read inside a burst and the read after it partition the burst exactly.

By the study's reading, every mode other than DDS/Goertzel behaves as the idle streamer does. One such mode was tested.

## How it was proven on a real P2 {#sec-e4-proof}

The test program runs on a P2 board at 200 MHz with nothing connected to pins P0 to P7. One cog, started from a `DAT` block, does all streamer work and issues every `GETXACC`; the debugger is confined to cog 0, which only waits for the results and prints them. The measuring cog drives P3 low as a plain output with its smart pin off, so the streamer's input bit for P3 holds a fixed level.

**Construction.** All 512 LUT longs hold `$173D_0000`, and the NCO frequency is `$8000_0000`. Each Goertzel burst is an `XINIT` whose `D` is `$F007_0000` plus a count (SINC1, no DAC output, input pins P0 to P3) and whose `S` is `$0008_80A5` (P3 inverted and summed, the other three pins ignored). With P3 low, each active clock adds 61 to the cosine accumulator and 23 to the sine accumulator. Every phase starts from the same preamble: an 8-clock Goertzel burst, a 4-clock burst whose terms are all zero (`S` of `$0008_00A5`), and an idle `GETXACC` whose value, B, must be nonzero, so that a clear which wrongly acted would show.

**Controls**, all passed in both runs: the 512 LUT longs read back unchanged; P3 read at its driven level at every check; `POLLXFI` reported the streamer finished after every wait and still running at every read meant to fall inside a command; and a calibration pair of 64-clock bursts moved the cosine accumulator by +3,843 with P3 low and by -3,843 with P3 high (63 × 61 each way), which shows the term follows the pin and is a whole multiple of 61.

**Idle and non-Goertzel reads.** In each of eight repetitions, after the preamble: a read with the streamer idle; an `XINIT` of `$4000_0400` (immediate-to-pins, one pin, output disabled, count `$0400`) followed at once by a read; a read 100 clocks later, with that command confirmed still running; and a read after it ended. Each of those reads, and the idle read taken before each calibration burst and before each burst of the two runs below, was compared with its preamble's B. All 50 reads equalled B bit for bit, and none returned zero. In the first repetition, B and the four reads were all 488.

**Reads inside a burst.** Each repetition ran two 256-clock bursts, each after its own preamble. Run A: an idle read P, the burst with no read inside it, a 4,000-clock wait, and a read RA. Run B: the same, with one `GETXACC` issued a fixed `WAITX` delay after the `XINIT` (read R1), and after the wait a read R2. The delays were 30 in the first four repetitions, then 62, 94, 126 and 190. The outcomes were fixed before the run: run B's R1 + R2 - P equal to run A's RA - P confirms the partition; a result 61 short would mean the clear lost a term; 61 over, that a term was counted twice; a difference equal to R1, that the clear did not act during the burst.

Results for the first repetition:

| Quantity | Value | Terms of 61 |
|---|---|---|
| Run A: RA - P (16,531 - 976) | 15,555 | 255 |
| Run B: R1 - P (18,849 - 17,080) | 1,769 | 29 |
| Run B: R2 | 13,786 | 226 |
| Run B: R1 + R2 - P | 15,555 | 29 + 226 = 255 |

In all eight repetitions RA - P was 15,555 and R1 + R2 - P equalled it exactly, while the read point moved from term 29 to term 189, one term behind the `WAITX` operand each time. R2 was 13,786 in each of the first four repetitions, although run B started from 17,080 in the first and from 30,927 in the next three: the read inside the burst discarded everything before it. The sine accumulator, recorded for information, moved on no idle read and split the same way (5,865 in both runs of every repetition). That a 256-clock burst gives 255 terms is Erratum E5.

Run A is also the before-and-after difference the fix is built on: it read 15,555 in all eight repetitions, from starting values of 976, 14,823, 12,871, 10,919 and 8,967. The largest value any read returned was 36,600.

The program was run twice on 2026-09-24, from two builds with identical measuring code; every value printed was the same in both runs.

### The fix's test {#sec-e4-fix-proof}

The fix ran in its own test program, on the same construction: the LUT, the NCO frequency, the mode word and the `S` operand above, with P3 driven by the measuring cog, low for the first half of the run and high for the second. The printed block is the routine the test program calls, byte for byte, and the program checks before it starts that `burst_mode` carries the printed mode bits and `burst_sel` the printed `S`. Every wait on a burst is `WAITXFI`, as in the routine.

At each P3 level the program runs three records, each of four parts:

- **Calibration.** The per-clock term C, measured without assuming either erratum, as the difference between a 65-clock and a 64-clock burst, each read from a flushed start to a flushed end.
- **The documented use, without the fix.** A `GETXACC` "to clear", a 64-clock burst and a reading; a second `GETXACC` "to clear", a 65-clock burst right after and a reading; a zero burst alone and a reading; then a 7-clock burst read with no zero burst, which leaves its last term held for the next part. This part must show both errata in the same run: the second "clear" reading equals the first reading (Erratum E4), and the bursts read 63 × C, 65 × C, C and 6 × C (Erratum E5). If it does not, the program prints `RIG FAIL` and no verdict.
- **The fix.** Ten consecutive calls of `burst_sums`, with N = 1, 2, 3, 4, 7, 64, 65, 255, 256 and 1001, set by the program with `SETWORD` in `burst_mode`, the first call starting with the 7-clock burst's term still held. After each call the program waits 1,000 clocks and takes its own idle reading.
- **Pin checks.** P3 at its driven level before and after the record.

The outcome was fixed before the run: every one of the 60 calls returns exactly N × C on the cosine and on the sine sum; the before reading of each record's first call has gained exactly C (the held term the first zero burst delivered), and that of every other call nothing; and the program's own reading after each call equals the before reading plus the returned sum. A miss of exactly -C would mean the zero burst did not deliver the last term; +C, that an older term was counted.

**The results.** Every control passed. The printed words read `$F007_0100` and `$0008_80A5`; the routine built its zero-burst words as `$F007_0004` and `$0008_00A5`; the 512 LUT longs read back unchanged; and P3 read at its driven level before and after every record. The calibration gave C = 61 on the cosine sum and 23 on the sine sum in all three records at P3 low, and -61 and -23 in all three at P3 high.

The documented use, without the fix, showed both errata in all 12 rows (6 records, cosine and sine): the second "clear" reading equalled the first, and the bursts read 63 × C, 65 × C, C and 6 × C. In the first record, on the cosine sum: P = 68,869, R1 = 72,712 (3,843, which is 63 × 61), the second "clear" 72,712, R2 = 76,677 (3,965, which is 65 × 61), the zero burst alone 76,738 (61), and the 7-clock burst 77,104 (366, which is 6 × 61).

All 60 calls of `burst_sums` returned exactly N × C on both sums. At P3 low, for N = 1, 2, 3, 4, 7, 64, 65, 255, 256 and 1001, the cosine sums were 61, 122, 183, 244, 427, 3,904, 3,965, 15,555, 15,616 and 61,061, and the sine sums 23, 46, 69, 92, 161, 1,472, 1,495, 5,865, 5,888 and 23,023; at P3 high, the same values negated. The 256-clock call returned 15,616 (256 × 61), where the difference alone, in the erratum test above, read 15,555 (255 × 61). Each record's first call found its before reading moved by exactly C from the reading after the 7-clock burst (77,165 against 77,104 in the first record); every later call's before reading equalled the program's own reading after the previous call; and every one of the program's own readings, 1,000 clocks after a call, equalled the call's before reading plus its returned sum. No call returned (N-1) × C or (N+1) × C. The largest accumulator value read was 412,909.

The test program was run once, on 2026-09-26, on a P2 board at 200 MHz. The values above are read from its raw lines, not from its verdict line.

## The test program {#sec-e4-program}

The test program is `e4-getxacc-clear-gating-test.spin2`. Its measuring code is a `DAT` block started by `COGINIT`; the Spin2 method `main` waits for it, prints every raw value, checks the controls, and prints one verdict for the idle and non-Goertzel reads and one for the reads inside a burst.

The streamer command words sit at the end of the measuring cog's code:

```pasm2
dch_            long    MODE_G | N_CHARGE
dzero_          long    MODE_G | N_ZERO
dcal_           long    MODE_G | N_CAL
drun_           long    MODE_G | N_RUN
dimm_           long    D_IMM
son_            long    S_ON
szero_          long    S_ZERO
simm_           long    0
lutv_           long    LUTVAL
frq_            long    FRQ
dlytab          long    30, 30, 30, 30, 62, 94, 126, 190
```

`dch_` and `dzero_` are the preamble's 8-clock and zero-term bursts, `dcal_` the 64-clock calibration burst, `drun_` the 256-clock burst of runs A and B, and `dimm_` the non-Goertzel command. `dlytab` holds run B's eight `WAITX` delays.

The before-and-after pattern, as the calibration block runs it. The `call #xfi_end` checks with `POLLXFI` that the streamer has finished before the second read:

```pasm2
                call    #preamble
                getxacc p_
                mov     py_, 0-0
                xinit   dcal_, son_
                waitx   ##WAIT_IDLE
                mov     site_, #2
                call    #xfi_end
                getxacc r_
                mov     ry_, 0-0
```

Run A is the same pattern with `drun_`. Run B's read inside the burst follows; the delay is loaded from `dlytab` before the preamble, so only the `WAITX` separates the `XINIT` from the `GETXACC`:

```pasm2
                call    #preamble
                getxacc p_
                mov     py_, 0-0
                xinit   drun_, son_
                waitx   dly_
                getxacc r1_                     ' R1: mid-burst
                mov     r1y_, 0-0
```

The non-Goertzel reads follow the same shape in the block marked `phase (i)`: an `XINIT` of `dimm_` with the next instruction a `GETXACC`, a `WAITX` of 100 clocks and a second `GETXACC`, then a `POLLXFI` check that the command is still running.

The fix's test program is `e4-e5-fix-read-sums-test.spin2`; Erratum E5 shares it. The printed routine sits in its `DAT` block between the comment lines `' ---- DROP-IN BEGIN ----` and `' ---- DROP-IN END ----`. The program calls it the way a reader would, setting only the count:

```pasm2
fix_arm         mov     fidx_, #0
.call           alts    fidx_, #fixn_
                mov     nn_, 0-0                ' N for this call
                setword burst_mode, nn_, #0     ' the reader's count
                call    #burst_sums             ' THE DROP-IN
                waitx   ##WAIT_REREAD
                getxacc qx_                     ' Q: the rig's own idle read
                mov     qy_, 0-0
```

`fixn_` holds the ten burst lengths, and `WAIT_REREAD` is 1,000 clocks. The program prints every raw reading, the controls, the uncorrected readings in units of the measured C, one line per call with its sums, and one `VERDICT:` line; it drives P3 and releases it at the end, so P3 must be free.

## Status {#sec-e4-status}

| Field | Content |
|---|---|
| Erratum | E4 |
| Published by Parallax | No |
| Found by | Predicted by the clean-room design study; confirmed here |
| Confirmed on silicon | Yes — 2026-09-24, on a P2 board at 200 MHz, run twice |
| Fix proven on silicon | Yes — 2026-09-26, on a P2 board at 200 MHz, run once; helper routine |
| Affects | `GETXACC` with the streamer idle or in a non-Goertzel mode: it returns the Goertzel accumulators without clearing them. Measured with SINC1 bursts started by `XINIT`, one input pin |
| Test program | `e4-getxacc-clear-gating-test.spin2`; the fix: `e4-e5-fix-read-sums-test.spin2` |
