# Erratum E7: A Blocking RDFAST Can Skip Its Wait After a No-Wait RDFAST {#ch-e7}

::: caution
**Expected:** a blocking `RDFAST` (`D[31]` = 0) waits until the FIFO has begun receiving hub data, so the next instruction can read the first long at its address.

**Actual:** issued 8 to 15 clocks after a no-wait `RDFAST` (`D[31]` = 1), at one spacing that depends on the hub alignment, the blocking `RDFAST` takes 2 clocks without waiting, and the next `RFLONG` returns `$0000_0000`.

**Workaround:** at least 16 clocks must pass from the start of the no-wait `RDFAST` to the start of the blocking one; see *A proven workaround*.
:::

This erratum affects a cog that starts the hub FIFO with a no-wait `RDFAST` and then, a few clocks later, restarts it at another address with a blocking `RDFAST` and reads in the next instruction. The failure needs both instructions, in that order, 8 to 15 clocks apart; a cog that uses only blocking `RDFAST`s, or only no-wait ones, does not meet it. It was measured in cog execution, with `RFLONG` as the read.

## What the P2 is documented to do {#sec-e7-documented}

The P2 Documentation (Parallax), section FAST SEQUENTIAL FIFO INTERFACE, gives `RDFAST` and `WRFAST` two modes, chosen by bit 31 of the D operand. For the blocking mode:

> If D[31] = 0, RDFAST/WRFAST will wait for any previous WRFAST to finish and then reconfigure the hub FIFO interface for reading or writing. In the case of RDFAST, it will additionally wait until the FIFO has begun receiving hub data, so that it can start being used in the next instruction.

For the no-wait mode:

> If D[31] = 1, RDFAST/WRFAST will not wait for FIFO reconfiguration, taking only two clocks. In this case, your code must allow a sufficient number of clocks before any attempt is made to read or write FIFO data.

The blocking paragraph names one thing the instruction waits for first, a previous `WRFAST`, and makes no exception for a `RDFAST` that follows a no-wait `RDFAST`. By it, a blocking `RDFAST` issued at any time after a no-wait one still waits until the FIFO has begun receiving the new address's data, and the next instruction can read that data.

The no-wait paragraph's requirement describes a different case, and that case is not this erratum. In the same test, a read issued too soon after a no-wait `RDFAST` alone returned `$0000_0000`, and the first spacing at which such a read was correct was 8 to 15 clocks, depending on hub alignment. The documentation states the requirement for that case, and the case belongs to the companion manual *P2 Anti-Patterns*. This erratum is the blocking `RDFAST` failing its own promise: the read follows a blocking `RDFAST`, which is documented to wait.

The KNOWN BUGS section of the P2 Documentation does not list this behaviour. In the reviewers' comments attached to that section of the document, replying to a note that an `RDFAST` corruption bug should be listed there, Chip Gracey wrote: "Yes, but I can't explain it well." The comments do not describe the conditions or the symptom. The defect in this chapter is plausibly that bug; nothing in the comments establishes it.

## What the P2 actually does {#sec-e7-actual}

The arrangement tested, in cog execution: a no-wait `RDFAST` (D = `$8000_0000`), then either nothing or a `WAITX`, then a blocking `RDFAST #0` to a different hub address, then `RFLONG` as the very next instruction. The spacing is counted from the start of the no-wait `RDFAST` to the start of the blocking one, the no-wait `RDFAST`'s own 2 clocks included. It was swept over 2 and 4 to 44 clocks (3 cannot be reached, since every instruction takes at least 2 clocks) in each of 64 hub alignments: the 8 hub RAM slices the blocking `RDFAST`'s address can lie in, each at 8 starting points in the hub's rotation.

- In every alignment, exactly one spacing failed, in all 16 trials. At that spacing the blocking `RDFAST` took 2 clocks, the time of a no-wait `RDFAST`, and the `RFLONG` returned `$0000_0000`: not the first long at the blocking `RDFAST`'s address, not data from the no-wait `RDFAST`'s address, and not the FIFO's earlier contents.
- The failing spacing was between 8 and 15 clocks, set by the hub alignment. Each spacing from 8 to 15 clocks was the failing one in exactly 8 of the 64 alignments.
- At every other spacing tested, the blocking `RDFAST` waited 10 to 17 clocks, and the `RFLONG` returned the correct first long.

In total, 1,024 of 43,008 reads were wrong, every one `$0000_0000`, and the other 41,984 were correct.

The failure needs the no-wait `RDFAST` before the blocking one. In the same test, a blocking `RDFAST` with no `RDFAST` before it gave the correct next-instruction read in all 3,072 trials (with `RFLONG`, `RFWORD` and `RFBYTE`), taking 10 to 17 clocks. A second no-wait `RDFAST` in the blocking one's place, with a `WAITX #200` before the read, moved the FIFO to its own address in all 43,008 trials.

## What your program sees {#sec-e7-sees}

If your program issues a blocking `RDFAST` 8 to 15 clocks after a no-wait `RDFAST`, the `RFLONG` that follows can return `$0000_0000` in place of the first long at the new address. Nothing else marks the failure: the read does not stall, and with `WCZ` the flags were those of a zero long (C clear, Z set) in every failing trial the test printed.

Whether it happens depends on the spacing and on the hub alignment at the moment your code runs. Each spacing from 8 to 15 clocks failed in 8 of the 64 alignments tested and read correctly in the other 56, so the same code can read correctly on one pass and return zero on another if its hub alignment differs between them. Spacings of 2 and 4 to 7 clocks, and of 16 to 44 clocks, read correctly in every alignment tested.

The long after the zero is not the second long either. The test printed the second `RFLONG` for one trial in each failing alignment: where the new address lay in hub slice 0, 1 or 2, it returned the first long at that address; in slices 3 to 7 it returned `$0000_0000` again. Reads past the second were not made. The test's data regions in hub RAM were unchanged: it re-checked them after every alignment.

## A proven workaround {#sec-e7-workaround}

**What any workaround must do:** let at least 16 clocks pass from the start of the no-wait `RDFAST` to the start of the blocking one.

**One way, proven on a real P2:** a `WAITX #RDFAST_SPACING_WAITX` (12) directly after the no-wait `RDFAST`.

```pasm2
CON
  RDFAST_SPACING_WAITX = 12            ' RDFAST 2 + WAITX 2+12 = 16 clocks
DAT
        rdfast  nowait, hub_first      ' no-wait RDFAST (D[31] = 1)
        waitx   #RDFAST_SPACING_WAITX  ' E7: >= 16 clocks, RDFAST to RDFAST
        rdfast  #0, hub_next           ' blocking RDFAST: now it waits
        rflong  first_long             ' reads hub_next's first long
```

The `WAITX #RDFAST_SPACING_WAITX` (12) makes the spacing from the start of the no-wait `RDFAST` to the start of the blocking one 16 clocks, one more than the largest failing spacing measured, so that the blocking `RDFAST` waits and the `RFLONG` after it reads the first long at `hub_next`; it is a rule at each use, applied wherever your code issues a blocking `RDFAST` after a no-wait one.

In your code, `nowait` is a register holding `$8000_0000` (`D[31]` = 1, and a block count of 0, so no wrap); `hub_first` and `hub_next` hold the two hub addresses, and `first_long` receives the first long at `hub_next`.

The rule is the spacing: at least 16 clocks from the start of the no-wait `RDFAST` to the start of the blocking one. The no-wait `RDFAST` takes 2 clocks and `WAITX #RDFAST_SPACING_WAITX` takes 2 + 12 = 14. The basis is measured: in the erratum test, every spacing from 16 to 44 clocks read correctly in all 64 alignments and all 16 trials of each, and the blocking `RDFAST` then waited its usual 10 to 17 clocks. There the spacing was set by a `WAITX` whose register operand held 12 to 40. The block above, with `RDFAST_SPACING_WAITX` = 12, ran in the workaround test on 2026-09-26: in all 64 alignments, 16 trials each, `first_long` received the first long at `hub_next`, and the next `RFLONG` the long after it, in 1,024 of 1,024 trials, with the blocking `RDFAST` waiting 10 to 17 clocks. In the same run the unspaced arrangement failed as described above in all 64 alignments.

**Other ways that meet the condition.** Other instructions that fill at least 16 clocks from the start of the no-wait `RDFAST` to the start of the blocking one meet the same condition, since the measurements tie the failure to the spacing, not to the `WAITX`. They have not been run: only `WAITX` was placed between the two `RDFAST`s, and instructions that wait for hub RAM there were not tested (limits below).

The cost is the 14 clocks of the `WAITX`, each time a blocking `RDFAST` follows a no-wait one.

The limits of the proof:

- Only `WAITX` was tested between the two `RDFAST`s. Other instructions there, in particular instructions that wait for hub RAM, were not.
- The `WRFAST` counterpart of this arrangement was not tested.
- Making the first `RDFAST` blocking, in place of the spacing, was not tested as a workaround.
- Only `RFLONG` was tested as the read after the blocking `RDFAST`. The streamer was not used.
- The no-wait `RDFAST`'s address was a long in hub slice 0 in every trial; the blocking `RDFAST`'s address was a long in each of the 8 slices. Both used a block count of 0.
- Spacings above 44 clocks were not tested.
- Only cog execution was tested, with one cog using its FIFO, at 200 MHz.

## Why it happens {#sec-e7-why}

No account of the mechanism is available. The clean-room design study did not predict this defect, and the P2 Documentation does not describe it. What follows is what the bench shows about its timing, and what it leaves open.

The failing spacing follows the no-wait `RDFAST`, not the blocking one. The no-wait `RDFAST`'s address was the same long of hub slice 0 in every alignment tested, and at each of the 8 starting points in the hub's rotation the failing spacing was the same for all 8 slices of the blocking `RDFAST`'s address.

It also coincides with the arrival of the no-wait `RDFAST`'s data. In the same test, a no-wait `RDFAST` of a slice-0 address followed by an `RFLONG` alone first read correctly at a spacing equal, at every one of the 8 starting points, to the failing spacing here (table in the next section). The blocking `RDFAST` fails when it is issued on the clock at which the no-wait `RDFAST`'s first long has just become readable. One clock earlier and one clock later, it waits as usual. In slice 0 at the first starting point, it waited 11 clocks at a spacing of 9, took 2 at a spacing of 10, and waited 17 at a spacing of 11.

What is not known: why the wait ends at once on that clock, where the zero comes from, and whether a blocking `WRFAST`, or the streamer, is affected in the same way.

## How it was proven on a real P2 {#sec-e7-proof}

**Where it came from.** The test was built to measure something else: when the hub FIFO can first be used after `RDFAST` and `WRFAST`, in both modes. The arrangement of this erratum was one of its secondary arrangements, expected to show the blocking promise holding. The defect was not predicted.

**The arrangement.** One P2 board at 200 MHz; no pins used.

- Every FIFO operation ran in a measuring cog started by `COGINIT` (cog 1 in both runs), in cog execution. The debugger was confined to cog 0 (`DEBUG_COGS = %0000_0001`), which sent the commands, classified the results from hub RAM and printed them.
- Three data regions, each starting on a 32-byte boundary, so that long k of a region lies in hub slice k mod 8: the no-wait `RDFAST`'s region, long k = `$3C3C_00C0` + k; the blocking `RDFAST`'s region, `$A5A5_0080` + k; and a third region, `$0D0D_0040` + k, that the FIFO was loaded from before every trial. A wrong read can therefore be traced to its source.
- Each trial loaded the FIFO from the third region with a blocking `RDFAST`, a `WAITX #64`, two `RFLONG`s and a second `WAITX #64`, so that a stale read would show as `$0D0D_0042`. It then read a slice-0 long with `RDLONG`, which ties the cog to the hub rotation, and waited the starting point, 0 to 7 clocks. Between two `GETCT`s came the no-wait `RDFAST` of the first region's long 0, the spacing, the blocking `RDFAST #0` of long s of the second region, and `RFLONG` with `WCZ`. A second `RFLONG` followed.
- The sweep: 8 slices s times 8 starting points gives 64 alignments; 42 spacings (2, and 4 to 44 clocks); 16 trials of each, 43,008 trials in all. The 8 starting points span a whole hub rotation: a blocking `RDFAST` alone took 8 different times over them, in every slice.
- The blocking `RDFAST`'s own clocks are the `GETCT` difference less the `GETCT` overhead, the spacing and the `RFLONG`.

**The outcome, written into the program before the run.** The program expected the first long of the blocking `RDFAST`'s address at every spacing, and reported any other read as a deviation.

**The controls**, each of which had to pass before the program would print a verdict:

- a `GETCT` pair costs 2 clocks, and `WAITX` D costs 2 + D clocks at every delay the sweep used;
- plain `RDLONG`s read every pattern long at every slice;
- with no new `RDFAST`, the loaded FIFO returned `$0D0D_0042` and then the long after it;
- a no-wait `RDFAST`, then `WAITX #200`, then `RFLONG`, returned the right longs.

The program's write controls ran as well. Every control was correct in every trial of both runs.

**The results.** The failing spacing at each starting point, and the spacing at which an `RFLONG` after a no-wait `RDFAST` alone first read correctly, in clocks:

| Starting point (clocks) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| Failing spacing, every slice | 10 | 9 | 8 | 15 | 14 | 13 | 12 | 11 |
| First correct no-wait read, slice 0 | 10 | 9 | 8 | 15 | 14 | 13 | 12 | 11 |

At each failing spacing, all 16 trials read `$0000_0000`, and the blocking `RDFAST` took 2 clocks. Over the whole sweep, 1,024 of 43,008 reads were wrong, all `$0000_0000`, and 41,984 were correct; none returned the no-wait `RDFAST`'s data or the FIFO's stale contents. Every spacing from 16 to 44 clocks read correctly in every alignment and trial. Around the failure, in slice 0 at starting point 0:

| Spacing (clocks) | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|
| Blocking `RDFAST` (clocks) | 13 | 12 | 11 | 2 | 17 | 16 |
| `RFLONG` returned | correct | correct | correct | `$0000_0000` | correct | correct |

The test ran on 2026-09-25, twice. The two runs printed the same result for every alignment and spacing.

**The workaround.** The workaround test ran on 2026-09-26, once, on a P2 board at 200 MHz, with the same regions, the same loading of the FIFO before every trial and the same 64 alignments.

- Its controls were the four above and one more: `WAITX #RDFAST_SPACING_WAITX` (12) between two `GETCT`s measured 16 clocks, 2 for the `GETCT` pair and 14 for the `WAITX`, in every trial. Every control was correct in every trial.
- As a positive control, the same run swept the unspaced arrangement over the same 42 spacings. It failed at exactly one spacing in each of the 64 alignments, at the same spacings as in the erratum test (table above), with all 16 trials reading `$0000_0000` and the blocking `RDFAST` taking 2 clocks: 1,024 of 43,008 reads wrong. At every spacing from 16 to 44 clocks, the first read and the long after it were correct in all 29,696 trials.
- The block printed in *A proven workaround*, with nothing else between its lines, read the first long at `hub_next` and then the long after it in 1,024 of 1,024 trials. Its blocking `RDFAST` waited 10 to 17 clocks, taking 8 different times over the 8 starting points in every slice.

## The test program {#sec-e7-program}

The erratum test is `e7-rdfast-blocking-after-no-wait-test.spin2` in the examples archive. Its Spin2 code in cog 0 starts the measuring cog, sends it one command per arrangement, slice and starting point, classifies every trial, prints every row, checks the controls, and prints the verdicts. The measuring cog is PASM2 in the program's `DAT` block and is the only code that touches the FIFO. Besides this erratum's arrangement, the program measures blocking and no-wait `RDFAST` and `WRFAST` on their own, and a second no-wait `RDFAST` in place of the blocking one.

Each trial of this erratum's arrangement starts after the FIFO has been loaded. It ties the cog to the hub rotation, waits the starting point, and starts the timing:

```pasm2
v_rebn          rdlong  c_junk, c_oldb
                waitx   c_phase
                getct   c_t0
```

The next three lines, whose comments run past this page's width, are `rdfast c_nowait, c_midb` (the no-wait `RDFAST`; `c_nowait` holds `$8000_0000`), `waitx c_dly` (the spacing), and `rdfast #0, c_new` (the blocking `RDFAST`). Then the read, in the next instruction:

```pasm2
                rflong  c_r1                            wcz
                getct   c_t1
                wrc     c_r3
                bitz    c_r3, #FLAG_Z_BIT
                rflong  c_r2
                jmp     #post_read
```

`c_r3` records C in bit 0 and Z in bit 1, and the second `RFLONG` reads the long after. A second copy of the sequence, with no `WAITX`, gives the 2-clock spacing. The Spin2 side turns the spacing index j into clocks:

```spin2
  if distIdx == 0
    distClks := INSTR_CLK
  else
    distClks := NW_WAITX_OFFSET + distIdx - 1
```

`INSTR_CLK` is 2 and `NW_WAITX_OFFSET` is 4, and the measuring cog loads `c_dly` with j - 1, so j = 1 to 41 gives 4 to 44 clocks.

To run it, compile with `pnut-ts -d` and load it to RAM with DEBUG enabled. It uses no pins. A run that decides the question prints no `RIG FAIL` lines; this erratum shows as the second `ARM-VERDICT` line, which reads `DEVIATES` with 1,024 of 43,008 reads wrong. Every row is printed, so the result can be re-derived from the output rather than taken from the program.

The workaround test is `e7-workaround-rdfast-spacing-test.spin2`. It uses the same construction and the same trial, and runs the block printed in *A proven workaround*, between two marker comments, in all 64 alignments. Alongside, it runs this erratum's arrangement at every spacing from 2 to 44 clocks: a clean result for the block counts only if that sweep shows the erratum in every alignment, and otherwise the program reports the workaround as inconclusive. Its controls include that `WAITX #RDFAST_SPACING_WAITX` (12) takes 14 clocks. It ends with a `VERDICT E7 WORKAROUND:` line.

## Status {#sec-e7-status}

| Field | Content |
|---|---|
| Erratum | E7 |
| Published by Parallax | No |
| Found by | Found on the bench here, by a test built to measure something else |
| Confirmed on silicon | Yes — 2026-09-25, on a P2 board at 200 MHz, run twice |
| Workaround proven on silicon | Yes — 2026-09-26, on a P2 board at 200 MHz, run once; a rule at each use: at least 16 clocks from the start of the no-wait `RDFAST` to the start of the blocking one |
| Affects | a blocking `RDFAST` issued 8 to 15 clocks after a no-wait `RDFAST`, at the one spacing its hub alignment selects: the next `RFLONG` returns `$0000_0000`. Tested in cog execution, with `RFLONG` as the read |
| Test program | `e7-rdfast-blocking-after-no-wait-test.spin2`; the workaround: `e7-workaround-rdfast-spacing-test.spin2` |
