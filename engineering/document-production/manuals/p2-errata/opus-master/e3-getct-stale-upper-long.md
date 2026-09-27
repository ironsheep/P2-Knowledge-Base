# Erratum E3: GETCT Returns a Stale Upper Long {#ch-e3}

::: caution
**Expected:** `GETCT WC` returns the upper 32 bits of the P2's one 64-bit free-running counter, and Spin2's `GETMS()` and `GETSEC()` return the time since boot from that counter, whichever cog calls them.

**Actual:** in a cog of a group of four cogs (0-3 or 4-7) that has had no running cog at one or more wraps of the counter's lower long, all three return a time behind by 2^32^ clocks (21.47 s at 200 MHz) for each wrap missed, until that group runs through its next wrap.

**Workaround:** keep a cog of the group running at every wrap, or take no 64-bit time in that group until it has run through one wrap; see *A proven workaround*.
:::

This erratum affects a program that takes a 64-bit time, with `GETCT WC`, `GETMS()` or `GETSEC()`, in a cog of cogs 4-7 and starts its first cog there more than 2^32^ clocks after reset, 21.47 s at 200 MHz. It affects in the same way a program that stops every cog of either group and starts one there again after a wrap has passed. The error is a window, not a lasting state: it closes at the first wrap the group runs through, at most 2^32^ clocks after it opens. This chapter calls it the *stale window*. Plain `GETCT`, which reads the lower long, is not affected.

## What the P2 is documented to do {#sec-e3-documented}

The P2 Documentation (Parallax) describes one counter. Its overview of the chip lists, among what the hub provides the cogs:

> 64-bit free-running counter which increments every clock, cleared on reset

Its list of the improvements made to the chip states how a cog reads the upper half of that counter:

> System counter extended to 64 bits. GETCT WC retrieves upper 32-bits.

and its section EVENTS names the lower half:

> Event 1 = CT passed CT1 (CT is the lower 32-bits of the free-running 64-bit global counter)

The Spin2 Language Documentation (Parallax, v55) states what `GETSEC()` returns:

> Get seconds since booting, uses 64-bit system counter and CLKFREQ, rolls over every 136 years.

and what `GETMS()` returns:

> Get milliseconds since booting, uses 64-bit system counter and CLKFREQ, rolls over every 49.7 days.

Neither document qualifies these values by cog number, or by which other cogs are running. The KNOWN BUGS section of the P2 Documentation does not list this behaviour.

## What the P2 does {#sec-e3-actual}

The eight cogs form two groups of four: cogs 0-3 and cogs 4-7. `GETCT` does not read the counter itself; each group reads its own copy of the counter's two longs, and the two halves of that copy behave differently.

- **The lower long is current.** In every pair the tests took, including every pair in which the upper long was stale, the lower long a sampling cog read with plain `GETCT` lay between the reference cog's own lower-long reads taken just before and just after it.
- **The upper long advances at a wrap of the lower long only while at least one cog of the group is running.** A group with no running cog at a wrap keeps its previous upper long. A cog held in `WAITATN` or in `WAITX` at the wrap counts as running: each, alone in cogs 4-7, kept the group current.

From these two rules the stale window follows, and each of its parts was measured:

- **It opens** when a program starts a cog in a group that missed wraps. Cog 4, first started after its group had missed one wrap, read 1 behind; started again after its group had missed two more, it read 2 behind. Cogs 4 and 7, started after their group had missed eight wraps, read 8 behind.
- **Starting a cog does not bring its group's upper long up to date.** The reading taken just after the start was already behind, and a reading late in the same 2^32^-clock span was behind by the same amount.
- **It closes at the first wrap the group runs through, in one step, whatever the lag.** Cog 4, 1 behind, ran through the next wrap and then read the same upper long as cog 0; cogs 4 and 7, 8 behind, did the same, and so did cogs 1 and 3, 2 behind. Both tests that read again one wrap later found the group still current.
- **It opens again only if every cog of the group stops.** Cog 4 was stopped after it had caught up; its group then missed two wraps with no cog running, and cog 4, started again, read 2 behind.

At reset only cog 0 runs, so the cogs 4-7 group has no running cog until the program starts one, and its upper long stays at zero through every wrap until then. The first wrap comes 2^32^ clocks after reset: 21.47 s at 200 MHz. The cogs 0-3 group is kept current by cog 0 for as long as cog 0, or another cog of 0-3, runs. With every cog of 0-3 stopped, cog 0 included, cogs 0-3 showed the same stale window: cogs 1 and 3, started after their group had missed two wraps, read 2 behind, and read current after the next wrap.

The defect was confirmed at 200 MHz, for lags of one, two and eight missed wraps, in cogs 4-7 (cogs 4 and 7 sampled) and in cogs 0-3 (cogs 1 and 3 sampled).

## What your program sees {#sec-e3-sees}

In a cog of a group that missed wraps, `GETCT WC` followed by `GETCT` gives your program a 64-bit time that is short by 2^32^ clocks for each wrap missed. In one pair of the test, cog 0 read its own counter immediately before and immediately after cog 4 read:

| Read by | Upper long (`GETCT WC`) | Lower long (`GETCT`) |
|---|---|---|
| cog 0, before | `$0000_0001` | `$1020_DB39` |
| cog 4 | `$0000_0000` | `$1020_DB59` |
| cog 0, after | `$0000_0001` | `$1020_DBA1` |

The three lower longs are in order; the upper long is one behind, a gap of 2^32^ clocks, which is 21.47 s at 200 MHz.

`GETMS()` and `GETSEC()` show the same error, in milliseconds and seconds. After eight missed wraps, 171,798 ms at 200 MHz, a Spin2 cog in the group and cog 0 called both in the same instant:

| Called in | `GETMS()` | `GETSEC()` |
|---|---|---|
| cog 0 | 190,617 | 190 |
| cog 5, in the stale window | 18,819 | 18 |
| cog 0, after the window closed | 194,637 | 194 |
| cog 5, after the window closed | 194,637 | 194 |

In your program the stale window has four parts:

- **It opens** when your program starts the first cog of a group that has had no running cog at one or more wraps. From reset that is any first cog of 4-7 started more than 2^32^ clocks after reset.
- **Inside it,** a 64-bit time stamp, a `GETMS()` or a `GETSEC()` you take in that group is behind one taken in an up-to-date group by 2^32^ clocks for each wrap missed. The error is steady: all ten pairs of each reading agreed, early and late in the span.
- **It closes** at the group's next wrap, at most 2^32^ clocks after it opens, and the upper long catches up in one step. A 64-bit interval you time across that wrap includes 2^32^ clocks that did not pass for each wrap the group missed: cog 4, 8 behind, read `$0000_0000_$E013_BB32` late in one span and `$0000_0009_$1001_546A` early in the next, an upper long that went from 0 to 9 across one wrap.
- **After it,** the group reads current for as long as one of its cogs keeps running. It opens again only if every cog of the group stops and a wrap passes before one starts.

What does not go wrong:

- Plain `GETCT` returned a current lower long in every pair of every reading, in both groups.
- A cog of a group that had a running cog at every wrap read the same upper long as the reference cog, in every reading of every test.
- Before the first wrap the correct upper long is zero, and a group's copy starts from zero at reset, so a program that has run for fewer than 2^32^ clocks since reset is not exposed.
- Only `GETCT`, `GETMS()` and `GETSEC()` were exercised. The counter events, which the P2 Documentation defines on the lower long, were not tested.

## A proven workaround {#sec-e3-workaround}

**What any workaround must do:** never use a 64-bit time taken inside a stale window. Either keep the window from opening, with a cog of the group running at every wrap of the lower long from the first wrap on, or wait it out, taking no 64-bit time in a group until it has run through one wrap since its first cog started.

**One way, proven on P2 hardware:** a keeper cog, started by the first line of `main()` and never stopped.

```spin2
CON ' ---- E3 Workaround: Keeper Cog ----
  KEEPER_COG = 7                ' a cog of 4-7 the program never uses

DAT ' ---- E3 Workaround: Keeper Code ----
                org
keeper          jmp     #keeper         ' loop forever; never stop this cog

PUB main()
'' Start the keeper before anything else, then run the program.
''

  coginit(KEEPER_COG, @keeper, 0)       ' first line: before the first wrap
```

Started by the first line of `main()` and never stopped, the keeper keeps a cog of 4-7 running through every wrap of the lower long, so the stale window never opens in cogs 4-7, and a cog your program starts there at any later time reads the same upper long as cog 0: this is a one-time startup workaround.

The block was confirmed on silicon on 2026-09-26, on a P2 board at 200 MHz, run once: with the keeper running, cogs 5 and 6 started after one wrap and cogs 4 and 5 started after two each read the same upper long as cog 0 in all ten pairs of their readings, and with the keeper stopped, cog 6 read one behind.

**Where it goes.** Put the block at the top of your top-level object, ahead of every other `PUB` method: Spin2 runs the first `PUB` method of the top-level object at start, so this `main()` runs first. Your own `main()` body follows the `coginit` line. If your object already has a `main()`, move its body there and remove its old `PUB main()` line. In the test program, the line that follows is the call that runs the rest of the test.

`KEEPER_COG` names the keeper's cog. It must be a cog of 4-7 that nothing else in your program starts or stops.

**Other ways that meet the condition.** The condition asks for no 64-bit time inside a stale window, not for a keeper.

- **A cog of your own.** A cog your program already starts in 4-7 before the first wrap and never stops keeps the window from opening, and then no keeper is needed. It does not have to be executing: a keeper held in `WAITATN`, and one held in `WAITX`, each kept cogs 4-7 current through a wrap on P2 hardware. So a driver cog that spends its time waiting for an event or a delay meets the condition, provided it starts before the first wrap and is never stopped. The P2 Documentation does not say which cog a free-cog start chooses, so start that cog in 4-7 by its number, or check the cog number the start returns. Run B, under *How it was proven on P2 hardware*, is the evidence for a cog of the program's own: cog 4, started at the beginning of the program and kept running, read the same upper long as cog 0 before the first wrap and after each of the first two.
- **Waiting it out.** A program that cannot keep a cog of 4-7 running can wait: once the group's first cog has run through one wrap, at most 2^32^ clocks (21.47 s at 200 MHz) after it starts, the group reads current. The test with eight missed wraps is the evidence: the readings taken after the one closing wrap, and after the wrap that followed, read current in both cogs sampled. A time taken before that wrap is behind, and an interval that spans it is too long.

**The cost.** The keeper takes one cog for the life of the program: it holds cog 7, and seven cogs remain for your program. A program that already needs all eight cogs cannot add the keeper, but meets the condition if one of its own cogs of 4-7 is running from before the first wrap and is never stopped. The keeper executes a jump to itself and nothing else. Waiting it out costs no cog, only the wait.

**What it covers.** The block covers cogs 4-7 only. Cogs 0-3 are kept current by cog 0, which runs your `main()` from reset, for as long as it or another cog of 0-3 keeps running. A program that stops cog 0 while cogs 4-7 run, and later starts a cog of 0-3, needs a cog of 0-3 kept running, or the wait, in the same way.

**The limits of the proof:**

- Two waits were tested as the only running cog of a group at a wrap: `WAITATN` that nothing ends, and `WAITX` with a count of `$FFFF_FFF0`. Other wait instructions were not tested. Spin2's `WAITMS()` and `WAITUS()` are not a wait instruction but a loop that reads the counter, so a Spin2 cog in them is executing, as the polling cogs of the tests were.
- Only cog 7 was tested as the keeper executing a jump; cogs 7 and 6 held the waits. The cogs of 4-7 that read the counter after a wrap were cogs 4, 5 and 6, each started after one or two wraps and stopped again after its reading.
- The keeper ran alone in cogs 4-7 through two wraps. The test program then stopped it, as a positive control.
- The tests ran once each, at 200 MHz, with the program downloaded to RAM with a reset.

## Why it happens {#sec-e3-why}

The account below is the clean-room design study's reading of the mechanism, stated at the level of the programmer's model. The measurements in the next section match it.

The P2 has one 64-bit counter, but a cog does not read it directly. Each group of four cogs holds its own copy of the counter's two longs, and `GETCT` reads the group's copy: the lower long without `WC`, the upper long with it. The group refreshes the two halves of its copy on different schedules. `GETMS()` and `GETSEC()` are computed by the Spin2 interpreter from the calling cog's own `GETCT WC` and `GETCT`, so they inherit whatever that copy holds.

The lower half is refreshed on every clock on which any cog of the group is running. If the group has been idle, the first clock on which one of its cogs runs brings the lower half up to date, so a newly started cog reads a current lower long.

The upper half is refreshed only once in 2^32^ clocks, at the wrap of the lower long, and only if a cog of the group is running at that moment. Nothing else refreshes it: not a cog start, and not the clocks that pass between wraps. A group with no running cog at a wrap keeps its previous upper long. At the next wrap it runs through, it takes the counter's upper long as it is then, which is why the error closes in a single step rather than shrinking by one, whatever the lag.

The counter and both groups' copies start from zero at reset, and at reset only cog 0 runs. The cogs 0-3 group therefore refreshes at every wrap from the start, for as long as cog 0 or another of its cogs runs; the cogs 4-7 group refreshes at none until a program starts a cog there. The two groups follow the same rule: which group holds cog 0 decides only which one is covered from reset.

Running here means the state a cog is in between its start and its stop, the state `COGCHK` reports. What a running cog is executing does not enter into it: a cog held in a wait instruction keeps its group refreshed as a cog executing a loop does.

## How it was proven on P2 hardware {#sec-e3-proof}

Two programs, Run A and Run B, confirmed the erratum. Each was downloaded to RAM with a chip reset and run on a bare P2 board at 200 MHz, with the debugger confined to cog 0. Each was run twice, from two builds: as first written, and with its comments and layout conformed to house style and its measuring code unchanged. Every D value and every verdict matched between the two builds. A third program, run once, confirmed the workaround, and three more, run once each, measured the stale window; they are described after them.

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

The expected D of every reading, for the defect present and for it absent, was written into each program before the run.

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

**The workaround.** The workaround's test program decided the block printed under *A proven workaround*. It carries that block byte for byte, with the same sampler, pair protocol, D and pair rules as Run A and Run B, at 200 MHz, with the debugger confined to cog 0. The keeper starts in cog 7 at the first line of `main()`. Cog 1 samples the cogs 0-3 group from start to end. The program's own cogs of 4-7 are cogs 4, 5 and 6: each is started as a sampler just before one reading and stopped again just after it, so every cog of 4-7 that reads the counter after a wrap was started after one or two wraps through which the keeper ran alone in that group. Every reading of cogs 4-7 is paired with a reading of cog 1.

| Cog 0 upper | Reading | Sampler | Cogs 4-7 before the reading | D written in advance | Sampler D | Cog 1 D |
|---|---|---|---|---|---|---|
| 0 | early | cog 4 | the keeper, since the first line of `main()` | 0 (control) | 0 | 0 |
| 1 | early | cog 5 | the keeper alone through wrap 1 | 0 with the keeper; 1 without | 0 | 0 |
| 1 | late | cog 6 | the keeper alone through wrap 1 | 0 with the keeper; 1 without | 0 | 0 |
| 2 | early | cog 4 | the keeper alone through wraps 1 and 2 | 0 with the keeper; 1 or 2 without | 0 | 0 |
| 2 | late | cog 5 | the keeper alone through wraps 1 and 2 | 0 with the keeper; 1 or 2 without | 0 | 0 |
| 3 | early | cog 6 | the keeper stopped after the reading above; no cog running at wrap 3 | 1 (positive control) | **1** | 0 |

In every reading all ten pairs agreed on D, and the lower-long check held in every pair.

The controls of Run A and Run B apply, with these differences. At start the running cogs must be cog 0 and the keeper only. The keeper must be seen running on every poll up to the positive control, and stopped after it. The reading at upper long 0 must give D = 0. The positive control must give D = 1: it shows that the program, on this part and in this run, sees the erratum when the keeper is absent, so a D of 0 with the keeper running cannot come from a test that is blind to it. Cog 6 reads both with the keeper running and, in the positive control, with it stopped: the same cog and the same code, with only the keeper changed.

The verdict rule was set before the run. The workaround is confirmed if the four readings taken after a wrap with the keeper running all give D = 0, with all ten pairs of each agreeing and the lower-long check holding in every pair. A reading whose ten pairs agree on a D other than 0, or a failed lower-long check, refutes it. A reading whose pairs disagree, or that gets too few valid pairs, leaves it inconclusive. A control failure gives no verdict.

**Result.** The workaround's test program ran once, on 2026-09-26, on a P2 board at 200 MHz, downloaded to RAM with a reset. At start the upper long read 0 and the running cogs were cog 0 and the keeper in cog 7. Every control passed, and no `RIG FAIL` line was printed. The running-cog set showed the keeper on every poll until it was stopped, with cog 0's counter at `$0000_0002_$E088_2186`, and did not show it on any poll after. With the keeper running, the four readings taken after a wrap gave D = 0. In the positive control, with the keeper stopped and wrap 3 missed, cog 6 read an upper long of `$0000_0002` beside cog 0's `$0000_0003`: D = 1, the erratum as in Run A. The verdict line read `CONFIRMED`.

**The stale window.** Three more programs ran once each, on 2026-09-27, on the same board at 200 MHz, downloaded to RAM with a reset. They use the same sampler, pair protocol, D and pair rules, and the same controls; each fixes its expected D values before the run, and each printed no `RIG FAIL` line. In all 40 of their counter readings all ten pairs agreed on D, and the lower-long check held in every pair; in each of the three Spin2 readings all ten pairs fell in the same class.

*Waiting cogs.* A keeper in cog 7 held in `WAITATN`, with no cog ever signalling it, ran alone in cogs 4-7 through wrap 1; it was then stopped, and a keeper in cog 6 held in `WAITX` with a count of `$FFFF_FFF0` (2 + D = 4,294,967,282 clocks, 14 short of 2^32^, started just after the lower long passed `$1000_0000`, so that the wait spanned the wrap) ran alone through wrap 2. No keeper ran through wrap 3. The samplers in cogs 4 and 5 were started for one reading each and stopped; cog 1 sampled cogs 0-3.

| Cog 0 upper | Cogs 4-7 at the wrap before the reading | Sampler | D written in advance | Sampler D | Cog 1 D |
|---|---|---|---|---|---|
| 0 | the `WAITATN` keeper, before any wrap | cog 4 | 0 (control) | 0 | 0 |
| 1 | the `WAITATN` keeper alone | cog 5 | 0 if it counts; 1 if not | 0 | 0 |
| 2 | the `WAITX` keeper alone | cog 4 | 0 if it counts; one more than the reading above if not | 0 | 0 |
| 3 | no cog running | cog 5 | one more than the reading above (positive control) | **1** | 0 |

*Cogs 0-3.* Cog 0 checked the start state, started the rest of the program in cog 4 with `COGSPIN`, and stopped itself; cog 4 was the reference from then on, and cog 5 sampled cogs 4-7. No cog of 0-3 was running on any poll until, after wrap 2, cogs 1 and 3 were started and kept running.

| Reference upper | Reading | Cogs 0-3 before the reading | Cog 1 D | Cog 3 D | Cog 5 D |
|---|---|---|---|---|---|
| 2 | early | no cog running at wraps 1 and 2 | **2** | **2** | 0 |
| 2 | late | cogs 1 and 3 running since after wrap 2 | **2** | **2** | 0 |
| 3 | early | cogs 1 and 3 ran through wrap 3 | 0 | 0 | 0 |
| 3 | late | cogs 1 and 3 ran through wrap 3 | 0 | 0 | 0 |
| 4 | early | cogs 1 and 3 ran through wrap 4 | 0 | 0 | 0 |

*Eight missed wraps.* Cogs 4-7 were held idle through eight wraps; then samplers in cogs 4 and 7 and a Spin2 cog 5 that answers each request with `GETMS()` then `GETSEC()` were started and kept running. Cog 1 sampled cogs 0-3. A Spin2 pair is cog 0's own `GETMS()` and `GETSEC()` before and after cog 5's; it is *short* when cog 5's values are behind by the time of eight wraps, 171,798 to 171,799 ms and 171 to 172 s, computed from `clkfreq` before the run, and *current* when they fall between cog 0's.

| Cog 0 upper | Reading | Cog 4 D | Cog 7 D | Cog 1 D | Cog 5 `GETMS()`/`GETSEC()` |
|---|---|---|---|---|---|
| 8 | early | **8** | **8** | 0 | **short** in 10 of 10 pairs |
| 8 | late | **8** | **8** | 0 | **short** in 10 of 10 pairs |
| 9 | early | 0 | 0 | 0 | current in 10 of 10 pairs |
| 9 | late | 0 | 0 | 0 | not read |
| 10 | early | 0 | 0 | 0 | not read |

Cog 4's own upper long, read as cog 0's minus D, was 0 in the last pair before wrap 9 and 9 in the first pair after it. Every short Spin2 pair was behind by 171,798 or 171,799 ms and by 172 s.

## The test program {#sec-e3-program}

The erratum's two files are `e3-getct-stale-upper-long-runA.spin2` (Run A) and `e3-getct-stale-upper-long-runB.spin2` (Run B). They share the sampler, the pair protocol and the controls, and differ only in when cog 4 starts and which readings are taken. The workaround's test program is `e3-workaround-keeper-cog-test.spin2`. The stale-window programs are `e3-workaround-waiting-cog-test.spin2`, `e3-cogs-0-3-stale-window-test.spin2` and `e3-stale-window-closes-test.spin2`.

The sampler is started explicitly in cog 1 and in cog 4 (`COGINIT #1` and `COGINIT #4`), with its hub mailbox address in `PTRA`. On each new request number it reads the counter and writes both longs:

```pasm2
sampler         mov     s_last, #0
s_loop          rdlong  s_req, ptra
                cmp     s_req, s_last   wz
        if_z    jmp     #s_loop
                mov     s_last, s_req
                getct   s_hi            wc      ' this group's UPPER copy
                getct   s_lo                    ' this group's LOWER copy
                wrlong  s_hi, ptra[MB_HI_IDX]
                wrlong  s_lo, ptra[MB_LO_IDX]
```

It then writes the request number back as its acknowledgment and returns to `s_loop`. Cog 0's side of a pair, in the method `take_pair`, is inline PASM2 that executes `GETCT WC` and `GETCT` before writing the request, and again after seeing the acknowledgment and reading the sampler's two longs. From those six longs each reading computes D and the lower-long check, and every pair is printed.

Run A's defect step: cogs 4-7 stay idle while cog 0 waits for its upper long to read 1, with the running-cog set polled throughout the wait; then cog 4 is started and read, with cog 1 read beside it:

```spin2
  ' ---- hazard: group 1 idle across wrap 0->1 --------------------------
  if bHalted == FALSE
    debug("--- waiting for CT hi=1 with cogs 4-7 idle (~21 s) ---")
    wait_until(HI_A1, LOWIN, M_C1)
  if bHalted == FALSE
    start_cog4(@mailboxGroup1)
    waitms(COG_SETTLE_MS)
    expect_mask(M_C1C4)
  if bHalted == FALSE
    debug("--- cog 4 started (first group-1 cog since reset) ---")
    reading(R_A1A, string("A1a cog4 hi=1"), @mailboxGroup1)
    reading(R_C1A, string("C1a cog1 hi=1"), @mailboxControl)
```

Later in the same file, `cogstop(SMP_COG)` at upper long 2 and a second `start_cog4` at upper long 4 take the two-missed-wrap readings.

Run B changes the arrangement in one place: both samplers start at the beginning of the program.

```spin2
  ' ---- both samplers from program start: cog 1 (group 0), cog 4 (group 1)
  if status == SUCCESS
    start_cog1(@mailboxControl)
    start_cog4(@mailboxGroup1)
    waitms(COG_SETTLE_MS)
    status := expect_mask(M_C1C4)
```

The workaround's test program carries the block of *A proven workaround* unchanged, between the comments `BEGIN DROP-IN` and `END DROP-IN`; its `main()` goes on to call the rest of the test. It uses the same sampler instructions and the same pair protocol as Run A and Run B. Every reading of cogs 4-7 goes through the method `arm`, which starts the sampler in the named cog, checks the running-cog set, takes the reading, stops the cog, and checks the set again:

```spin2
  longfill(@mailboxGroup1, 0, MB_LONGS)
  coginit(smpCog, @sampler, @mailboxGroup1)
  waitms(COG_SETTLE_MS)
  expect_mask(baseMask | (1 << smpCog))
  if bHalted == FALSE
    reading(slotIdx, pLabel, @mailboxGroup1)
    cogstop(smpCog)
    waitms(COG_SETTLE_MS)
    expect_mask(baseMask)
```

The readings run in the order of the table under *How it was proven on P2 hardware*. After the late reading at upper long 2, `cogstop(KEEPER_COG)` stops the keeper, and the positive control is read in cog 6 after wrap 3.

The waiting-cog test's two keepers are these two loops, each started by `COGINIT` in its own cog; the first never leaves its `WAITATN`, since no cog signals it:

```pasm2
                org     0
keepAtn         waitatn
                jmp     #keepAtn

' The WAITX keeper: each WAITX holds it for $FFFF_FFF0 + 2 clocks, just
' under one wrap period; started with the lower long past $1000_0000, the
' first wait spans the next wrap.
                org     0
keepWaitx       waitx   ##$FFFF_FFF0
                jmp     #keepWaitx
```

The cogs 0-3 test is the one program whose reference is not cog 0: its `main()` checks the start state, starts the method `controller` in cog 4 with `COGSPIN`, and stops cog 0, so `DEBUG_COGS` names cogs 0 and 4. The eight-wrap test adds a Spin2 method, `spin_sampler`, run in cog 5, which answers each request with `GETMS()` then `GETSEC()`.

Each file prints every pair raw, a summary line per reading, and a one-line verdict (the eight-wrap test prints a second verdict line for `GETMS()`/`GETSEC()`). All are compiled with `pnut-ts` 1.55.8 with DEBUG enabled (`-d`) and downloaded to RAM; the download must reset the part, since each program checks that the counter starts from zero. Run A ends about 105 s after reset, Run B about 44 s after reset, the workaround's test program about 67 s after reset, the waiting-cog test about 66 s, the cogs 0-3 test about 87 s, and the eight-wrap test about 216 s.

## Status {#sec-e3-status}

| Field | Content |
|---|---|
| Erratum | E3 |
| Published by Parallax | No |
| Found by | Predicted by the clean-room design study; confirmed here |
| Confirmed on silicon | Yes — 2026-09-24, on a P2 board at 200 MHz, run twice; the stale window's close from eight missed wraps, the cogs 0-3 group, and `GETMS()`/`GETSEC()` — 2026-09-27, run once each |
| Workaround proven on silicon | Yes — 2026-09-26, on a P2 board at 200 MHz, run once; a one-time startup workaround: a keeper cog in cog 7 started by the first line of `main()`. A keeper held in `WAITATN` or `WAITX`, and waiting out one wrap — 2026-09-27, run once |
| Affects | `GETCT WC`, `GETMS()` and `GETSEC()` in a cog of a four-cog group that had no running cog at one or more wraps of the lower long, until that group runs through its next wrap (measured on cogs 4-7 and on cogs 0-3); plain `GETCT` is not affected |
| Test program | `e3-getct-stale-upper-long-runA.spin2`, `e3-getct-stale-upper-long-runB.spin2`, `e3-workaround-keeper-cog-test.spin2`, `e3-workaround-waiting-cog-test.spin2`, `e3-cogs-0-3-stale-window-test.spin2`, `e3-stale-window-closes-test.spin2` |
