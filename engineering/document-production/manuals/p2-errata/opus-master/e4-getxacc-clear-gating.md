# Erratum E4: GETXACC Clears Only During a Goertzel Burst {#ch-e4}

<!-- include: shared-e4.md -->

## What happens {#sec-e4-actual}

The P2 Documentation's streamer instruction table gives `GETXACC` as:

> Get Goertzel X into D and Y into next S, clear X and Y

Its description of the DDS/Goertzel mode says the same, and neither makes the clear depend on the streamer's mode or on whether a streamer command is running.

In this erratum a *Goertzel burst* is one DDS/Goertzel streamer command for the clocks it runs, and a *term* is what it adds to each accumulator on each of those clocks. On P2 hardware the clear acts only while a Goertzel burst is running:

- **With the streamer idle**, `GETXACC` returns the accumulators and leaves them as they were. Repeated reads return the same value. The same held with the streamer running another mode (immediate-to-pins was tested).
- **A new Goertzel burst** adds its terms to whatever the accumulators hold. Starting a streamer command does not reset them.
- **During a Goertzel burst**, the clear acts as documented: a read returns everything accumulated so far, earlier bursts included, and the accumulation continues from the clear. No term is lost and none is counted twice.

So a program that issues one `GETXACC` after each burst and treats it as that burst's result gets a running total: in the test, the reading before a 256-clock burst was 14,823 and the reading after it was 30,378, of which the burst contributed 15,555. A `GETXACC` issued before an `XINIT` to zero the sums zeroes nothing. The accumulation itself is exact; only the clear is missing.

The difference of two idle readings is still one term short of the burst, because the burst's last term is held back until the next Goertzel burst. That is Erratum E5, and the routine below steps around both.

Only programs that measure with the Goertzel mode meet this erratum, and among them only those that run one burst at a time from an idle streamer. A continuous stream of commands chained with `XCONT`, read during each command, clears as documented.

## A proven workaround {#sec-e4-workaround}

**What any workaround must do:** take each burst's sums as the difference of two readings taken with the streamer idle, one before the burst and one after it. An idle `GETXACC` clears nothing, so the difference holds your burst whatever the accumulators held before it.

**One way, proven on P2 hardware:** the `burst_sums` helper routine, which also steps around Erratum E5.

```pasm2
{ Runs one DDS/Goertzel burst (SINC1 only) and returns its exact
  sums. Put your XINIT D and S in burst_mode and burst_sel, then
  CALL #burst_sums with the streamer idle. It leaves the burst's
  cosine sum in cos_sum and its sine sum in sin_sum.
}
CON
  ZERO_COUNT = 4    ' each zero burst: a count of 4
  INPUT_NIB  = 3    ' S nibble 3 = S[15:12], the summed inputs
DAT
burst_sums  mov     zero_mode, burst_mode       ' zero burst: your mode,
            setword zero_mode, #ZERO_COUNT, #0  '   count 4,
            mov     zero_sel, burst_sel         '   your S with every
            setnib  zero_sel, #0, #INPUT_NIB    '   input off: S[15:12]=0
            xinit   zero_mode, zero_sel         ' adds any held term
            waitxfi
            getxacc cos_base                    ' idle read: no clear
            mov     sin_base, 0-0
            xinit   burst_mode, burst_sel       ' your burst
            waitxfi
            xinit   zero_mode, zero_sel         ' adds its last term
            waitxfi
            getxacc cos_sum                     ' idle read again
            mov     sin_sum, 0-0
            sub     cos_sum, cos_base           ' cosine sum, all N terms
            sub     sin_sum, sin_base           ' sine sum, all N terms
            ret

burst_mode  long    $F007_0100                  ' your D (count 256 here)
burst_sel   long    $0008_80A5                  ' your S
zero_mode   long    0                           ' built: the zero burst's D
zero_sel    long    0                           ' built: the zero burst's S
cos_base    long    0                           ' before reading, cosine
sin_base    long    0                           ' before reading, sine
cos_sum     long    0                           ' result: cosine sum
sin_sum     long    0                           ' result: sine sum
```

Each call leaves in `cos_sum` and `sin_sum` the sums of your burst alone, all N of its terms, whatever the accumulators held before the call: a *helper routine*. To use it, put your `XINIT` D operand (the Goertzel mode word with your count) in `burst_mode` and your S operand in `burst_sel`, set `SETXFRQ` as your program already does, and `CALL #burst_sums` with the streamer idle. The values printed in `burst_mode` and `burst_sel` are the test program's.

The two zero bursts are your mode word with a count of 4 and every input switched off (`S[15:12]` clear), so every term they form is zero. The first delivers any term an earlier burst left held, and the second delivers your burst's last term (Erratum E5).

On silicon, the routine returned exactly N terms on both sums in all 60 calls of its test program, for bursts of 1 to 1001 clocks, at both input levels.

**The cost:** two zero bursts of 4 NCO rollovers each per call, besides your burst; 17 instructions and 8 longs of cog RAM.

**The limits:** SINC1 mode only, and one burst at a time from an idle streamer, since the routine starts each command with `XINIT`. It ran from cog RAM at 200 MHz with one input pin and no DAC output; DAC output, more than one input pin, other NCO frequencies and hub execution were not tested.

**Found by** the clean-room design study, as a prediction, and confirmed on P2 hardware on 2026-09-24. Parallax does not list it.
