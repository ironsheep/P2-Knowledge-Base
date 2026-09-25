# Chapter 4: GETXACC Clears Only During a Goertzel Burst {#ch-e4}

`GETXACC` is documented to read the streamer's Goertzel cosine and sine accumulators and to
clear them. On the part, the clear takes effect only while a DDS/Goertzel streamer command is
running. With the streamer idle, or running the other streamer mode tested, `GETXACC` returns
the accumulators and leaves them unchanged, so each Goertzel burst adds to whatever earlier
bursts left behind. A reading taken after a burst measures that burst only when the reading
taken before it is subtracted.

## What the design says {#sec-e4-design}

The P2 Documentation states the clear in its streamer instruction table and again in its
description of the DDS/Goertzel mode. The instruction table's entry for `GETXACC` reads:

> Get Goertzel X into D and Y into next S, clear X and Y

The DDS/Goertzel mode description reads:

> After some number of complete NCO cycles, both accumulators can be simultaneously captured
> into holding registers and cleared using the GETXACC instruction. GETXACC writes the captured
> cosine accumulation into D and places the captured sine accumulation into the next
> instruction's S value. Subsequent GETXACC instructions will return the same values until a
> new streamer command executes.

The SINC1/SINC2 table that follows that description carries the column heading:

> Accumulations (SIN_ACC/COS_ACC are read and cleared by GETXACC)

None of the three places makes the clear depend on the streamer's mode or on whether a
streamer command is running.

## What the part does {#sec-e4-part}

In this chapter a *Goertzel burst* is one DDS/Goertzel streamer command for the clocks it
runs, and a *term* is the product the streamer adds to each accumulator on each of those
clocks.

- **Streamer idle.** `GETXACC` returns the current value of the accumulators and leaves them
  as they were. Repeated reads return the same value, bit for bit.
- **Streamer running another mode.** One other mode was tested: the immediate-to-pins mode,
  one pin wide, with its output disabled, started by `XINIT`. A `GETXACC` issued as the next
  instruction after that `XINIT`, and another issued 100 clocks later with the command still
  running, both returned the value from before the `XINIT` and cleared nothing.
- **A new Goertzel burst.** The burst adds its terms to the value the accumulators already
  hold. Starting a streamer command does not reset them.
- **During a Goertzel burst.** The clear acts. `GETXACC` returns everything accumulated so
  far, including what earlier bursts left, and the accumulation continues from the clear. The
  read plus the next read hold exactly what the same burst gives when it is not read: no term
  is lost and none is counted twice.

The sine accumulator behaved as the cosine accumulator did in every case measured.

## The symptom {#sec-e4-symptom}

A program that relies on the documented clear, issues one `GETXACC` after each burst, and
treats the reading as that burst's result gets a running total instead: each reading holds the
burst plus everything accumulated since the last clear. In one repetition of the test program,
the reading before a 256-clock burst was 14,823 and the reading after it was 30,378; the burst
itself contributed 15,555.

A `GETXACC` issued before an `XINIT` in order to zero the accumulators returns the running
total and zeroes nothing.

A `GETXACC` inside a Goertzel burst returns the leftover from earlier bursts together with the
part of the burst run so far. In the test program, a read 29 terms into a burst that started
from 17,080 returned 18,849.

What does not go wrong: the accumulation itself is exact. Every difference the test program
measured was a whole multiple of the per-clock term, the same burst gave the same difference
from every starting value, and a read inside a burst split it into two parts that sum
exactly to the unread burst. Consecutive idle reads return the same value, as the documentation
says they do.

## The workaround {#sec-e4-workaround}

**Measured on silicon.** Read the accumulators with the streamer idle immediately before the
burst and again after it has ended, and subtract. The test program did this for every burst it
scored. For a 256-clock burst the before-and-after difference was 15,555 in all eight
repetitions, from starting values of 976, 14,823, 12,871, 10,919 and 8,967.

```pasm2
' Per-burst sums: read idle before and after, take the difference
        getxacc x0                ' idle: the running total so far
        mov     y0, 0-0           ' sine arrives as this S value
        xinit   gmode, gsel       ' one Goertzel burst
        waitx   ##4000            ' wait until well past its end
        getxacc x1                ' idle again
        mov     y1, 0-0
        sub     x1, x0            ' cosine sum of this burst
        sub     y1, y0            ' sine sum of this burst

gmode   long    $F007_0100        ' Goertzel, SINC1, P0-P3, count 256
gsel    long    $0008_80A5        ' P3 inverted, summed; LUT offset $0A5
```

The values in `gmode` and `gsel` are the ones the test program used. The 4,000-clock wait is
also the test program's; the longest Goertzel burst it ran was 256 clocks, at an NCO frequency
of `$8000_0000`. The condition the measurement supports is that both reads fall outside the
burst; a longer burst needs a longer wait.

**Measured on silicon.** When a `GETXACC` does fall inside the burst, the burst's total is
still recoverable: the read inside the burst, minus the reading taken before the burst, plus
the reading taken after it, equalled the unread burst in every repetition.

The difference holds one term fewer than the burst has clocks. That is a separate erratum,
with its own workaround, in [Chapter 5](#ch-e5).

**Not tested:** SINC2 accumulation, more than one input pin, bursts started by `XZERO` or
`XCONT`, continuous `XCONT` loops, and accumulator values near the 32-bit limit. The largest
value any read returned in the runs was 36,600.

## Why it happens {#sec-e4-why}

The clean-room design study traces the behaviour to how the accumulators are updated. Each
accumulator is rewritten only on the clocks of a running DDS/Goertzel command; on every other
clock it holds its value, whatever instruction the cog executes. The clear in `GETXACC` is not
a separate action on the accumulator. It is folded into that same per-clock update: on the
clock the clear arrives, the update starts the accumulator over instead of adding to its old
value. When no update happens, because the streamer is idle or running a different mode, the
clear has nothing to act through, and the accumulator keeps its value.

The read does not depend on the update. `GETXACC` returns the accumulator's current value,
which is why idle reads repeat exactly and why a read inside a burst returns the running sum.
When the clear does act, the accumulator starts over from the one term that has been formed but
not yet added ([Chapter 5](#ch-e5)), and that term appears in the next reading. That is why a
read inside a burst and the read after it partition the burst exactly.

By the study's reading, every mode other than DDS/Goertzel behaves as the idle streamer does.
One such mode was tested.

## How it was proven {#sec-e4-proof}

The test program runs on a P2 board at 200 MHz with nothing connected to pins P0 to P7. One
cog, started from a `DAT` block, does all streamer work and issues every `GETXACC`; the
debugger is confined to cog 0, which only waits for the results and prints them. The measuring
cog drives P3 low as a plain output with its smart pin off, so the streamer's input bit for P3
holds a fixed level.

**Construction.** All 512 LUT longs hold `$173D_0000`, and the NCO frequency is `$8000_0000`.
Each Goertzel burst is an `XINIT` whose `D` is `$F007_0000` plus a count (SINC1, no DAC output,
input pins P0 to P3) and whose `S` is `$0008_80A5` (P3 inverted and summed, the other three
pins ignored). With P3 low, each active clock adds 61 to the cosine accumulator and 23 to the
sine accumulator. Every phase starts from the same preamble: an 8-clock Goertzel burst, a
4-clock burst whose terms are all zero (`S` of `$0008_00A5`), and an idle `GETXACC` whose value,
B, must be nonzero, so that a clear which wrongly acted would show.

**Controls**, all passed in both runs: the 512 LUT longs read back unchanged; P3 read at its
driven level at every check; `POLLXFI` reported the streamer finished after every wait and still
running at every read meant to fall inside a command; and a calibration pair of 64-clock bursts
moved the cosine accumulator by +3,843 with P3 low and by −3,843 with P3 high (63 × 61 each
way), which shows the term follows the pin and is a whole multiple of 61.

**Idle and non-Goertzel reads.** In each of eight repetitions, after the preamble: a read with
the streamer idle; an `XINIT` of `$4000_0400` (immediate-to-pins, one pin, output disabled,
count `$0400`) followed at once by a read; a read 100 clocks later, with that command
confirmed still running; and a read after it ended. Each of those reads, and the idle read
taken before each calibration burst and before each burst of the two runs below, was compared
with its preamble's B. All 50 reads equalled B bit for bit, and none returned zero. In the
first repetition, B and the four reads were all 488.

**Reads inside a burst.** Each repetition ran two 256-clock bursts, each after its own
preamble. Run A: an idle read P, the burst with no read inside it, a 4,000-clock wait, and a
read RA. Run B: the same, with one `GETXACC` issued a fixed `WAITX` delay after the `XINIT`
(read R1), and after the wait a read R2. The delays were 30 in the first four repetitions, then
62, 94, 126 and 190. The outcomes were fixed before the run: run B's R1 + R2 − P equal to run
A's RA − P confirms the partition; a result 61 short would mean the clear lost a term; 61 over,
that a term was counted twice; a difference equal to R1, that the clear did not act during the
burst.

Results for the first repetition:

| Quantity | Value | Terms of 61 |
|---|---|---|
| Run A: RA − P (16,531 − 976) | 15,555 | 255 |
| Run B: R1 − P (18,849 − 17,080) | 1,769 | 29 |
| Run B: R2 | 13,786 | 226 |
| Run B: R1 + R2 − P | 15,555 | 29 + 226 = 255 |

In all eight repetitions RA − P was 15,555 and R1 + R2 − P equalled it exactly, while the read
point moved from term 29 to term 189, one term behind the `WAITX` operand each time. R2 was
13,786 in each of the first four repetitions, although run B started from 17,080 in the first
and from 30,927 in the next three: the read inside the burst discarded everything before it.
The sine accumulator, recorded for information, moved on no idle read and split the same way
(5,865 in both runs of every repetition). That a 256-clock burst gives 255 terms is the lag of
[Chapter 5](#ch-e5).

The program was run twice on 2026-09-24, from two builds with identical measuring code; every
value printed was the same in both runs.

## The test program {#sec-e4-program}

The test program is `e4-getxacc-clear-gating-test.spin2`. Its measuring code is a `DAT`
block started by `COGINIT`; the Spin2 method `main` waits for it, prints every raw value, checks
the controls, and prints one verdict for the idle and non-Goertzel reads and one for the reads
inside a burst.

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

`dch_` and `dzero_` are the preamble's 8-clock and zero-term bursts, `dcal_` the 64-clock
calibration burst, `drun_` the 256-clock burst of runs A and B, and `dimm_` the non-Goertzel
command. `dlytab` holds run B's eight `WAITX` delays.

The before-and-after pattern, as the calibration block runs it. The `call #xfi_end` checks with
`POLLXFI` that the streamer has finished before the second read:

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

Run A is the same pattern with `drun_`. Run B's read inside the burst follows; the delay is
loaded from `dlytab` before the preamble, so only the `WAITX` separates the `XINIT` from the
`GETXACC`:

```pasm2
                call    #preamble
                getxacc p_
                mov     py_, 0-0
                xinit   drun_, son_
                waitx   dly_
                getxacc r1_                     ' R1: mid-burst
                mov     r1y_, 0-0
```

The non-Goertzel reads follow the same shape in the block marked `phase (i)`: an `XINIT` of
`dimm_` with the next instruction a `GETXACC`, a `WAITX` of 100 clocks and a second
`GETXACC`, then a `POLLXFI` check that the command is still running.

## Status {#sec-e4-status}

| Field | Content |
|---|---|
| Erratum | E4 |
| Published by Parallax | No |
| Found by | Predicted by the clean-room design study; confirmed here |
| Confirmed on silicon | Yes — 2026-09-24, on a P2 board at 200 MHz, run twice |
| Workaround proven on silicon | Yes: the before-and-after difference, measured in every repetition; the one-clock lag of Chapter 5 still applies to it |
| Affects | `GETXACC` with the streamer idle or in a non-Goertzel mode: it returns the Goertzel accumulators without clearing them. Measured with SINC1 bursts started by `XINIT`, one input pin |
| Test program | `e4-getxacc-clear-gating-test.spin2` |
