# Erratum E3: GETCT Returns a Stale Upper Long {#ch-e3}

::: caution
**Expected:** `GETCT WC` returns the upper 32 bits of the P2's one 64-bit free-running counter, whichever cog executes it.

**Actual:** in a cog of cogs 4-7 started after that group of four cogs has had no running cog at a wrap of the lower long (the first wrap comes 2^32^ clocks after reset), `GETCT WC` returns an upper long that is behind by one for each wrap missed.

**Fix:** start a keeper cog in cog 7 as the first line of your `main()` and never stop it; see *The fix*.
:::

This erratum affects a program that takes a 64-bit time with `GETCT WC` in a cog of cogs 4-7 and starts its first cog there more than 2^32^ clocks after reset, 21.47 s at 200 MHz. It affects in the same way a program that stops every cog of 4-7 and starts one there again after a wrap has passed. Plain `GETCT`, which reads the lower long, is not affected.

## What the P2 is documented to do {#sec-e3-documented}

The P2 Documentation (Parallax) describes one counter. Its overview of the chip lists, among what the hub provides the cogs:

> 64-bit free-running counter which increments every clock, cleared on reset

Its list of the improvements made to the chip states how a cog reads the upper half of that counter:

> System counter extended to 64 bits. GETCT WC retrieves upper 32-bits.

and its section EVENTS names the lower half:

> Event 1 = CT passed CT1 (CT is the lower 32-bits of the free-running 64-bit global counter)

The documentation does not qualify the value `GETCT WC` returns by cog number, or by which other cogs are running. The KNOWN BUGS section of the P2 Documentation does not list this behaviour.

## What the P2 actually does {#sec-e3-actual}

The eight cogs form two groups of four: cogs 0-3 and cogs 4-7. `GETCT` does not read the counter itself; each group reads its own copy of the counter's two longs, and the two halves of that copy behave differently.

- **The lower long is current.** In every pair the test took, including every pair in which the upper long was stale, the lower long a sampling cog read with plain `GETCT` lay between cog 0's own lower-long reads taken just before and just after it.
- **The upper long advances at a wrap of the lower long only while at least one cog of the group is running.** A group with no running cog at a wrap keeps its previous upper long.

Measured on cog 4, in the cogs 4-7 group, against cog 0 and cog 1 in the cogs 0-3 group:

- A cog started in a group that missed wraps reads an upper long behind cog 0's by the number of wraps missed. Cog 4, first started after its group had missed one wrap, read 1 behind; started again after its group had missed two more, it read 2 behind.
- Starting a cog does not bring its group's upper long up to date. The reading taken just after the start was already behind, and a reading late in the same 2^32^-clock span was behind by the same amount.
- The first wrap the group runs through restores the correct value in one step. Cog 4, 1 behind, ran through the next wrap and then read the same upper long as cog 0.
- A group whose only running cog stops is exposed again. Cog 4 was stopped after it had caught up; its group then missed two wraps with no cog running, and cog 4, started again, read 2 behind.

At reset only cog 0 runs, so the cogs 4-7 group has no running cog until the program starts one, and its upper long stays at zero through every wrap until then. The first wrap comes 2^32^ clocks after reset: 21.47 s at 200 MHz.

The defect was confirmed at 200 MHz, for one and for two missed wraps. The test sampled cog 1 and cog 4; the other cogs of each group were not sampled separately, and the cogs 0-3 group was not tested with every one of its cogs stopped.

## What your program sees {#sec-e3-sees}

In a cog of a group that missed wraps, `GETCT WC` followed by `GETCT` gives your program a 64-bit time that is short by 2^32^ clocks for each wrap missed. In one pair of the test, cog 0 read its own counter immediately before and immediately after cog 4 read:

| Read by | Upper long (`GETCT WC`) | Lower long (`GETCT`) |
|---|---|---|
| cog 0, before | `$0000_0001` | `$1020_DB39` |
| cog 4 | `$0000_0000` | `$1020_DB59` |
| cog 0, after | `$0000_0001` | `$1020_DBA1` |

The three lower longs are in order; the upper long is one behind, a gap of 2^32^ clocks, which is 21.47 s at 200 MHz.

In your program this shows up in two ways:

- A 64-bit time stamp you take in the stale cog and one you take in a cog of an up-to-date group disagree by 2^32^ clocks for each wrap missed.
- The stale cog's upper long advances by more than one at the next wrap it runs through, as its group's copy catches up. Cog 4 read `$0000_0000_$E013_C141` late in one span and `$0000_0002_$1001_4D69` early in the next: its upper long went from 0 to 2 across one wrap. A 64-bit interval that cog times across that wrap includes 2^32^ clocks that did not pass, one for the wrap its group had missed.

What does not go wrong:

- Plain `GETCT` returned a current lower long in every pair of every reading, in both groups.
- A cog of a group that had a running cog at every wrap read the same upper long as cog 0: cog 1 in every reading of both runs, and cog 4 throughout the run in which it ran from the start of the program.
- The stale value is steady. All ten pairs of each reading agreed, early and late in the span.
- Before the first wrap the correct upper long is zero, and a group's copy starts from zero at reset, so a program that has run for fewer than 2^32^ clocks since reset is not exposed.
- Only `GETCT` was exercised. The counter events, which the documentation defines on the lower long, were not tested.

## The fix {#sec-e3-fix}

```spin2
CON ' ---- E3 Fix: Keeper Cog ----
  KEEPER_COG = 7                ' a cog of 4-7 the program never uses

DAT ' ---- E3 Fix: Keeper Code ----
                org
keeper          jmp     #keeper         ' loop forever; never stop this cog

PUB main()
'' Start the keeper before anything else, then run the program.
''

  coginit(KEEPER_COG, @keeper, 0)       ' first line: before the first wrap
```

Started by the first line of `main()` and never stopped, the keeper keeps a cog of 4-7 running through every wrap of the lower long, so a cog your program starts in 4-7 at any later time reads the same upper long as cog 0: this is a one-time startup fix.

The block was confirmed on silicon on 2026-09-26, on a P2 board at 200 MHz, run once: with the keeper running, cogs 5 and 6 started after one wrap and cogs 4 and 5 started after two each read the same upper long as cog 0 in all ten pairs of their readings, and with the keeper stopped, cog 6 read one behind.

**Where it goes.** Put the block at the top of your top-level object, ahead of every other `PUB` method: Spin2 runs the first `PUB` method of the top-level object at start, so this `main()` runs first. Your own `main()` body follows the `coginit` line. If your object already has a `main()`, move its body there and remove its old `PUB main()` line. In the test program, the line that follows is the call that runs the rest of the test.

`KEEPER_COG` names the keeper's cog. It must be a cog of 4-7 that nothing else in your program starts or stops.

**The cost.** The fix takes one cog for the life of the program: the keeper holds cog 7, seven cogs remain for your program, and a program that already needs all eight cogs cannot use it. The keeper executes a jump to itself and nothing else.

**What it covers.** The block covers cogs 4-7 only. Cogs 0-3 are kept current by cog 0, which runs your `main()` from reset, for as long as it or another cog of 0-3 keeps running; the cogs 0-3 group was not tested with every one of its cogs stopped.

**The limits of the proof:**

- The keeper was tested only as the loop above, a jump to itself. Whether a cog held in a wait instruction such as `WAITX` keeps its group current was not tested, so do not replace the loop with a wait.
- Only cog 7 was tested as the keeper. The cogs of 4-7 that read the counter after a wrap were cogs 4, 5 and 6, each started after one or two wraps and stopped again after its reading.
- The keeper ran alone in cogs 4-7 through two wraps. The test program then stopped it, as a positive control.
- The test ran once, at 200 MHz, with the program downloaded to RAM with a reset.

Run B, under *How it was proven on a real P2*, is earlier evidence of the rule the fix relies on: cog 4, started at the beginning of that program while the lower long read `$00DB_96FF` and kept running, read the same upper long as cog 0 before the first wrap and after each of the first two. In Run B the cog kept running was the cog that read the counter. The block above keeps a separate cog running while the cogs that read the counter start and stop, which is the arrangement the fix's own test program checked.

## Why it happens {#sec-e3-why}

The account below is the clean-room design study's reading of the mechanism, stated at the level of the programmer's model. The measurements in the next section match it.

The P2 has one 64-bit counter, but a cog does not read it directly. Each group of four cogs holds its own copy of the counter's two longs, and `GETCT` reads the group's copy: the lower long without `WC`, the upper long with it. The group refreshes the two halves of its copy on different schedules.

The lower half is refreshed on every clock on which any cog of the group is running. If the group has been idle, the first clock on which one of its cogs runs brings the lower half up to date, so a newly started cog reads a current lower long.

The upper half is refreshed only once in 2^32^ clocks, at the wrap of the lower long, and only if a cog of the group is running at that moment. Nothing else refreshes it: not a cog start, and not the clocks that pass between wraps. A group with no running cog at a wrap keeps its previous upper long. At the next wrap it runs through, it takes the counter's upper long as it is then, which is why the error closes in a single step rather than shrinking by one.

The counter and both groups' copies start from zero at reset, and at reset only cog 0 runs. The cogs 0-3 group therefore refreshes at every wrap from the start, for as long as cog 0 runs; the cogs 4-7 group refreshes at none until a program starts a cog there. A keeper cog in 4-7 that runs from before the first wrap gives that group a running cog at every wrap, so its upper long advances with the counter's, and a cog started there later reads it current.

Running here means the state a cog is in between its start and its stop, the state `COGCHK` reports. By the study's reading, what a running cog is executing does not enter into it. The tests kept their cogs in a polling loop or, for the keeper, a jump to itself, and did not try a cog held in a wait instruction such as `WAITX`.

## How it was proven on a real P2 {#sec-e3-proof}

Two programs, Run A and Run B, confirmed the erratum. Each was downloaded to RAM with a chip reset and run on a bare P2 board at 200 MHz, with the debugger confined to cog 0. Each was run twice, from two builds: as first written, and with its comments and layout conformed to house style and its measuring code unchanged. Every D value and every verdict matched between the two builds. A third program, run once, confirmed the fix; it is described after them.

**Arrangement.** Cog 0 is the reference. Cog 1, in the cogs 0-3 group, and cog 4, in the cogs 4-7 group, run the same sampler: on each new request from cog 0 it executes `GETCT WC` then `GETCT`, writes both longs to hub RAM, then writes an acknowledgment. One **pair** is taken as follows: cog 0 reads its own counter (`GETCT WC`, `GETCT`), writes a request, waits for the acknowledgment, reads the sampler's two longs, and reads its own counter again. The sampler's reads therefore fall between cog 0's two reads.

- A pair counts only if cog 0's two upper longs agree and all three lower longs lie between `$1000_0000` and `$F000_0000`, clear of any wrap.
- **D** is cog 0's upper long minus the sampler's upper long.
- Each pair also checks that the sampler's lower long lies strictly between cog 0's two lower longs, compared unsigned.
- A reading is ten counted pairs, and all ten must give the same D.

**Controls.** Any failure stops the run with no verdict.

- Cog 1, running from the start of the program, must give D = 0 in every reading.
- Cog 0's own upper long must equal the number of wraps of its lower long that cog 0 has watched since reset, checked on every poll.
- The set of running cogs, polled throughout every wait, must be exactly the cogs the program started; in Run A, no cog of 4-7 may run before cog 4 is started.
- At start the upper long must read 0 and only cog 0 may be running, which shows the download reset the part.
- Every request must be answered within 100 ms.

The expected D of every reading, for the defect present and for it absent, was fixed in each program before the run.

**Run A** holds cogs 4-7 idle until cog 0's upper long reads 1, starts cog 4, and reads it just after the start and again late in the same span. Cog 4 then runs through the next wrap and is read again. Cog 4 is then stopped, its group misses two wraps with no cog running, and cog 4 is started again and read just after the restart and late in the span. **Run B** starts cog 4 at the beginning of the program, beside cog 1, and reads it before the first wrap, early and late after it, and after the second wrap.

Wrap *n* below is the wrap after which cog 0's upper long reads *n*. An early reading is taken with the lower long past `$1000_0000`, a late one past `$E000_0000`.

| Run | Cog 0 upper | Reading | Cogs 4-7 before the reading | Cog 4 D | Cog 1 D |
|---|---|---|---|---|---|
| A | 0 | early | no cog running | not read | 0 |
| A | 1 | just after cog 4 started | no cog running at wrap 1 | **1** | 0 |
| A | 1 | late | cog 4 running since after wrap 1 | **1** | 0 |
| A | 2 | early | cog 4 ran through wrap 2 | 0 | 0 |
| A | 4 | just after cog 4 restarted | cog 4 stopped; no cog running at wraps 3 and 4 | **2** | 0 |
| A | 4 | late | cog 4 running since after wrap 4 | **2** | 0 |
| B | 0 | early | cog 4 running since program start | 0 | 0 |
| B | 1 | early | cog 4 ran through wrap 1 | 0 | 0 |
| B | 1 | late | cog 4 ran through wrap 1 | 0 | 0 |
| B | 2 | early | cog 4 ran through wrap 2 | 0 | 0 |

In every reading of both runs all ten pairs agreed on D, and the lower-long check held in every pair. Each program's verdict line read `CONFIRMED`, in both builds.

**The fix.** The fix's test program decided the block printed under *The fix*. It carries that block byte for byte, with the same sampler, pair protocol, D and pair rules as Run A and Run B, at 200 MHz, with the debugger confined to cog 0. The keeper starts in cog 7 at the first line of `main()`. Cog 1 samples the cogs 0-3 group from start to end. The program's own cogs of 4-7 are cogs 4, 5 and 6: each is started as a sampler just before one reading and stopped again just after it, so every cog of 4-7 that reads the counter after a wrap was started after one or two wraps through which the keeper ran alone in that group. Every reading of cogs 4-7 is paired with a reading of cog 1.

| Cog 0 upper | Reading | Sampler | Cogs 4-7 before the reading | D written in advance | Sampler D | Cog 1 D |
|---|---|---|---|---|---|---|
| 0 | early | cog 4 | the keeper, since the first line of `main()` | 0 (control) | 0 | 0 |
| 1 | early | cog 5 | the keeper alone through wrap 1 | 0 with the fix; 1 without | 0 | 0 |
| 1 | late | cog 6 | the keeper alone through wrap 1 | 0 with the fix; 1 without | 0 | 0 |
| 2 | early | cog 4 | the keeper alone through wraps 1 and 2 | 0 with the fix; 1 or 2 without | 0 | 0 |
| 2 | late | cog 5 | the keeper alone through wraps 1 and 2 | 0 with the fix; 1 or 2 without | 0 | 0 |
| 3 | early | cog 6 | the keeper stopped after the reading above; no cog running at wrap 3 | 1 (positive control) | **1** | 0 |

In every reading all ten pairs agreed on D, and the lower-long check held in every pair.

The controls of Run A and Run B apply, with these differences. At start the running cogs must be cog 0 and the keeper only. The keeper must be seen running on every poll up to the positive control, and stopped after it. The reading at upper long 0 must give D = 0. The positive control must give D = 1: it shows that the program, on this part and in this run, sees the erratum when the keeper is absent, so a D of 0 with the keeper running cannot come from a test that is blind to it. Cog 6 reads both with the keeper running and, in the positive control, with it stopped: the same cog and the same code, with only the keeper changed.

The verdict was fixed before the run. The fix is confirmed if the four readings taken after a wrap with the keeper running all give D = 0, with all ten pairs of each agreeing and the lower-long check holding in every pair. A reading whose ten pairs agree on a D other than 0, or a failed lower-long check, refutes it. A reading whose pairs disagree, or that gets too few valid pairs, leaves it inconclusive. A control failure gives no verdict.

**Result.** The fix's test program ran once, on 2026-09-26, on a P2 board at 200 MHz, downloaded to RAM with a reset. At start the upper long read 0 and the running cogs were cog 0 and the keeper in cog 7. Every control passed, and no `RIG FAIL` line was printed. The running-cog set showed the keeper on every poll until it was stopped, with cog 0's counter at `$0000_0002_$E088_2186`, and did not show it on any poll after. With the keeper running, the four readings taken after a wrap gave D = 0. In the positive control, with the keeper stopped and wrap 3 missed, cog 6 read an upper long of `$0000_0002` beside cog 0's `$0000_0003`: D = 1, the erratum as in Run A. The verdict line read `CONFIRMED`.

## The test program {#sec-e3-program}

The erratum's two files are `e3-getct-stale-upper-long-runA.spin2` (Run A) and `e3-getct-stale-upper-long-runB.spin2` (Run B). They share the sampler, the pair protocol and the controls, and differ only in when cog 4 starts and which readings are taken. The fix's test program is `e3-fix-keeper-cog-test.spin2`.

The sampler is started explicitly in cog 1 and in cog 4 (`COGINIT #1` and `COGINIT #4`), with its hub mailbox address in `PTRA`. On each new request number it reads the counter and writes both longs:

```pasm2
sampler         mov     s_last, #0
s_loop          rdlong  s_req, ptra
                cmp     s_req, s_last   wz
        if_z    jmp     #s_loop
                mov     s_last, s_req
                getct   s_hi            wc      ' this group's UPPER copy
                getct   s_lo                    ' this group's LOWER copy
                wrlong  s_hi, ptra[1]
                wrlong  s_lo, ptra[2]
```

It then writes the request number back as its acknowledgment and returns to `s_loop`. Cog 0's side of a pair, in the method `take_pair`, is inline PASM2 that executes `GETCT WC` and `GETCT` before writing the request, and again after seeing the acknowledgment and reading the sampler's two longs. From those six longs each reading computes D and the lower-long check, and every pair is printed.

Run A's defect step: cogs 4-7 stay idle while cog 0 waits for its upper long to read 1, with the running-cog set polled throughout the wait; then cog 4 is started and read, with cog 1 read beside it:

```spin2
  ' ---- hazard: group 1 idle across wrap 0->1 --------------------------
  debug("--- waiting for CT hi=1 with cogs 4-7 idle (~21 s) ---")
  wait_until(1, LOWIN, M_C1)
  start_cog4(@mb4)
  waitms(10)
  expect_mask(M_C1C4)
  debug("--- cog 4 started (first group-1 cog since reset) ---")
  reading(R_A1A, string("A1a cog4 hi=1"), @mb4)
  reading(R_C1A, string("C1a cog1 hi=1"), @mb1)
```

Later in the same file, `cogstop(4)` at upper long 2 and a second `start_cog4` at upper long 4 take the two-missed-wrap readings.

Run B changes the arrangement in one place: both samplers start at the beginning of the program.

```spin2
  ' ---- both samplers from program start: cog 1 (group 0), cog 4 (group 1)
  start_cog1(@mb1)
  start_cog4(@mb4)
  waitms(10)
  expect_mask(M_C1C4)
```

The fix's test program carries the block of *The fix* unchanged, between the comments `BEGIN DROP-IN` and `END DROP-IN`; its `main()` goes on to call the rest of the test. It uses the same sampler instructions and the same pair protocol as Run A and Run B. Every reading of cogs 4-7 goes through the method `arm`, which starts the sampler in the named cog, checks the running-cog set, takes the reading, stops the cog, and checks the set again:

```spin2
  longfill(@mailboxGroup1, 0, MB_LONGS)
  coginit(smpCog, @sampler, @mailboxGroup1)
  waitms(COG_SETTLE_MS)
  expect_mask(baseMask | (1 << smpCog))
  reading(slotIdx, name, @mailboxGroup1)
  cogstop(smpCog)
  waitms(COG_SETTLE_MS)
  expect_mask(baseMask)
```

The readings run in the order of the table under *How it was proven on a real P2*. After the late reading at upper long 2, `cogstop(KEEPER_COG)` stops the keeper, and the positive control is read in cog 6 after wrap 3.

Each file prints every pair raw, a summary line per reading, and a one-line verdict. All three are compiled with `pnut-ts` 1.55.8 with DEBUG enabled (`-d`) and downloaded to RAM; the download must reset the part, since each program checks that the counter starts from zero. Run A ends about 105 s after reset, Run B about 44 s after reset, and the fix's test program about 67 s after reset.

## Status {#sec-e3-status}

| Field | Content |
|---|---|
| Erratum | E3 |
| Published by Parallax | No |
| Found by | Predicted by the clean-room design study; confirmed here |
| Confirmed on silicon | Yes — 2026-09-24, on a P2 board at 200 MHz, run twice |
| Fix proven on silicon | Yes — 2026-09-26, on a P2 board at 200 MHz, run once; a one-time startup fix: a keeper cog in cog 7 started by the first line of `main()` |
| Affects | `GETCT WC` in a cog of a four-cog group that had no running cog at one or more wraps of the lower long (measured on cogs 4-7); plain `GETCT` is not affected |
| Test program | `e3-getct-stale-upper-long-runA.spin2`, `e3-getct-stale-upper-long-runB.spin2`, `e3-fix-keeper-cog-test.spin2` |
