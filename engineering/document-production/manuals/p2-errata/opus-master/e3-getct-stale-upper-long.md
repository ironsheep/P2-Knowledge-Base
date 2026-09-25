# Chapter 3: GETCT Returns a Stale Upper Long {#ch-e3}

`GETCT WC` reads the upper long of the 64-bit system counter from a copy kept
by the reading cog's group of four cogs, and that copy advances at a wrap of the
lower long only if a cog of the group is running at the wrap. A cog started in a
group that had no running cog at one or more wraps reads an upper long that is
behind by one for each wrap missed, while plain `GETCT` returns a current lower
long. From reset only cog 0 runs, so the first cog a program starts among cogs
4-7 reads a stale upper long if it starts after the first wrap, 2^32^ clocks
after reset (21.47 s at 200 MHz).

## What the design says {#sec-e3-design}

The P2 Documentation, in its list of what the hub provides the cogs, describes
one counter:

> 64-bit free-running counter which increments every clock, cleared on reset

Its list of the improvements made to the chip states how a cog reads the upper
half of that counter:

> System counter extended to 64 bits. GETCT WC retrieves upper 32-bits.

and its description of the counter events names the lower half:

> Event 1 = CT passed CT1 (CT is the lower 32-bits of the free-running 64-bit global counter)

The documentation describes a single counter. It does not qualify the value
`GETCT WC` returns by cog number, or by which other cogs are running.

## What the part does {#sec-e3-part}

The eight cogs form two groups of four: cogs 0-3 and cogs 4-7. `GETCT` does not
read the counter itself; each group reads its own copy of the counter's two
longs, and the two halves of that copy behave differently.

- **The lower long is current.** In every pair the test took, including every
  pair in which the upper long was stale, the lower long a sampling cog read
  with plain `GETCT` lay between cog 0's own lower-long reads taken just before
  and just after it.
- **The upper long advances at a wrap of the lower long only while at least one
  cog of the group is running.** A group with no running cog at a wrap keeps its
  previous upper long.

Measured on cog 4, in the cogs 4-7 group, against cog 0 and cog 1 in the cogs
0-3 group:

- A cog started in a group that missed wraps reads an upper long behind cog 0's
  by the number of wraps missed. Cog 4, first started after its group had
  missed one wrap, read 1 behind; started again after its group had missed two
  more, it read 2 behind.
- Starting a cog does not bring its group's upper long up to date. The reading
  taken just after the start was already behind, and a reading late in the same
  2^32^-clock span was behind by the same amount.
- The first wrap the group runs through restores the correct value in one step.
  Cog 4, 1 behind, ran through the next wrap and then read the same upper long
  as cog 0.
- A group whose only running cog stops is exposed again. Cog 4 was stopped after
  it had caught up; its group then missed two wraps with no cog running, and cog
  4, started again, read 2 behind.

At reset only cog 0 runs, so the cogs 4-7 group has no running cog until the
program starts one, and its upper long stays at zero through every wrap until
then. The first wrap comes 2^32^ clocks after reset: 21.47 s at 200 MHz.

The defect was confirmed at 200 MHz, for one and for two missed wraps. The test
sampled cog 1 and cog 4; the other cogs of each group were not sampled
separately, and the cogs 0-3 group was not tested with every one of its cogs
stopped.

## The symptom {#sec-e3-symptom}

In a cog of a group that missed wraps, `GETCT WC` followed by `GETCT` yields a
64-bit time that is short by 2^32^ clocks for each wrap missed. In one pair of
the test, cog 0 read its own counter immediately before and immediately after
cog 4 read:

| Read by | Upper long (`GETCT WC`) | Lower long (`GETCT`) |
|---|---|---|
| cog 0, before | `$0000_0001` | `$1020_DB39` |
| cog 4 | `$0000_0000` | `$1020_DB59` |
| cog 0, after | `$0000_0001` | `$1020_DBA1` |

The three lower longs are in order; the upper long is one behind, a gap of 2^32^
clocks, which is 21.47 s at 200 MHz.

In a program this shows up in two ways:

- A 64-bit time stamp taken in the stale cog and one taken in a cog of an
  up-to-date group disagree by 2^32^ clocks for each wrap missed.
- The stale cog's upper long advances by more than one at the next wrap it runs
  through, as its group's copy catches up. Cog 4 read `$0000_0000_$E013_C141`
  late in one span and `$0000_0002_$1001_4D69` early in the next: its upper long
  went from 0 to 2 across one wrap. A 64-bit interval that cog times across that
  wrap includes 2^32^ clocks that did not pass, one for the wrap its group had
  missed.

What does not go wrong:

- Plain `GETCT` returned a current lower long in every pair of every reading, in
  both groups.
- A cog of a group that had a running cog at every wrap read the same upper long
  as cog 0: cog 1 in every reading of both runs, and cog 4 throughout the run in
  which it ran from the start of the program.
- The stale value is steady. All ten pairs of each reading agreed, early and
  late in the span.
- Before the first wrap the correct upper long is zero, and a group's copy
  starts from zero at reset, so a program that has run for fewer than 2^32^
  clocks since reset is not exposed.
- Only `GETCT` was exercised. The counter events, which the documentation
  defines on the lower long, were not tested.

## The workaround {#sec-e3-workaround}

Keep at least one cog of each group the program uses running from before the
first wrap, 2^32^ clocks after reset (21.47 s at 200 MHz), and do not let every
cog of that group stop afterward. Cogs 0-3 are covered for as long as cog 0,
which runs from reset, keeps running. For cogs 4-7, start the cog there at the
beginning of the program and do not stop it:

```spin2
PUB main()
  ' start the cog that reads the counter in cogs 4-7 at once,
  ' before 2^32 clocks have run, and never stop it
  coginit(4, @worker, 0)

DAT
                org
worker          getct   hi      wc      ' upper long: current
                getct   lo              ' lower long
                ' ... the cog's work ...
                jmp     #worker
hi              res     1
lo              res     1
```

The workaround is proven on silicon. In the second test program (Run B, under
*How it was proven*), cog 4 was started at the beginning of the program, while the lower long read `$00DB_96FF`, and kept
running; its upper long matched cog 0's before the first wrap, early and late
after it, and after the second wrap.

What the proof covers: the cog kept running was the cog that read the counter,
held in a polling loop. Two variants follow from the same group rule but were
not tested on silicon: a separate cog held running only to keep its group
current while other cogs of the group are started and stopped, and reading the
upper long in a cog of cogs 0-3 and passing it to cogs 4-7 through hub RAM.

## Why it happens {#sec-e3-why}

The P2 has one 64-bit counter, but a cog does not read it directly. Each group
of four cogs holds its own copy of the counter's two longs, and `GETCT` reads
the group's copy: the lower long without `WC`, the upper long with it. The group
refreshes the two halves of its copy on different schedules.

The lower half is refreshed on every clock on which any cog of the group is
running. If the group has been idle, the first clock on which one of its cogs
runs brings the lower half up to date, so a newly started cog reads a current
lower long.

The upper half is refreshed only once in 2^32^ clocks, at the wrap of the lower
long, and only if a cog of the group is running at that moment. Nothing else
refreshes it: not a cog start, and not the clocks that pass between wraps. A
group with no running cog at a wrap keeps its previous upper long. At the next
wrap it runs through, it takes the counter's upper long as it is then, which is
why the error closes in a single step rather than shrinking by one.

The counter and both groups' copies start from zero at reset, and at reset only
cog 0 runs. The cogs 0-3 group therefore refreshes at every wrap from the start,
for as long as cog 0 runs; the cogs 4-7 group refreshes at none until a program
starts a cog there.

Running here means the state a cog is in between its start and its stop, the
state `COGCHK` reports. In the design, what a running cog is executing does not
enter into it; the test kept its cogs in a polling loop and did not try a cog
held in a wait instruction such as `WAITX`.

## How it was proven {#sec-e3-proof}

Two programs, Run A and Run B, were each downloaded to RAM with a chip reset and
run on a bare P2 board at 200 MHz, with the debugger confined to cog 0. Each was run twice, from two builds: as first written, and with its
comments and layout conformed to house style and its measuring code unchanged.
Every D value and every verdict matched between the two builds.

**Arrangement.** Cog 0 is the reference. Cog 1, in the cogs 0-3 group, and cog 4,
in the cogs 4-7 group, run the same sampler: on each new request from cog 0 it
executes `GETCT WC` then `GETCT`, writes both longs to hub RAM, then writes an
acknowledgment. One **pair** is taken as follows: cog 0 reads its own counter
(`GETCT WC`, `GETCT`), writes a request, waits for the acknowledgment, reads the
sampler's two longs, and reads its own counter again. The sampler's reads
therefore fall between cog 0's two reads.

- A pair counts only if cog 0's two upper longs agree and all three lower longs
  lie between `$1000_0000` and `$F000_0000`, clear of any wrap.
- **D** is cog 0's upper long minus the sampler's upper long.
- Each pair also checks that the sampler's lower long lies strictly between cog
  0's two lower longs.
- A reading is ten counted pairs, and all ten must give the same D.

**Controls.** Any failure stops the run with no verdict.

- Cog 1, running from the start of the program, must give D = 0 in every
  reading.
- Cog 0's own upper long must equal the number of wraps of its lower long that
  cog 0 has watched since reset, checked on every poll.
- The set of running cogs, polled throughout every wait, must be exactly the
  cogs the program started; in Run A, no cog of 4-7 may run before cog 4 is
  started.
- At start the upper long must read 0 and only cog 0 may be running, which
  shows the download reset the part.
- Every request must be answered within 100 ms.

The expected D of every reading, for the defect present and for it absent, was
fixed in each program before the run.

**Run A** holds cogs 4-7 idle until cog 0's upper long reads 1, starts cog 4,
and reads it just after the start and again late in the same span. Cog 4 then
runs through the next wrap and is read again. Cog 4 is then stopped, its group
misses two wraps with no cog running, and cog 4 is started again and read just
after the restart and late in the span. **Run B** starts cog 4 at the beginning
of the program, beside cog 1, and reads it before the first wrap, early and late
after it, and after the second wrap.

Wrap *n* below is the wrap after which cog 0's upper long reads *n*. An early
reading is taken with the lower long past `$1000_0000`, a late one past
`$E000_0000`.

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

In every reading of both runs all ten pairs agreed on D, and the lower-long
check held in every pair. Each program's verdict line read `CONFIRMED`, in both
builds.

## The test program {#sec-e3-program}

The two files are `e3-getct-stale-upper-long-runA.spin2` (Run A) and
`e3-getct-stale-upper-long-runB.spin2` (Run B). They share the sampler, the
pair protocol and the controls, and differ only in when cog 4 starts and which
readings are taken.

The sampler is started explicitly in cog 1 and in cog 4 (`COGINIT #1` and
`COGINIT #4`), with its hub mailbox address in `PTRA`. On each new request
number it reads the counter and writes both longs:

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

It then writes the request number back as its acknowledgment and returns to
`s_loop`. Cog 0's side of a pair, in the method `take_pair`, is inline PASM2 that
executes `GETCT WC` and `GETCT` before writing the request, and again after
seeing the acknowledgment and reading the sampler's two longs. From those six
longs each reading computes D and the lower-long check (`+<` is the unsigned
less-than):

```spin2
    dd := rhb - shi
    br := (rlb +< slo) and (slo +< rla)
    if not br
      rbf[slotIdx]++
```

Run A's defect step: cogs 4-7 stay idle while cog 0 waits for its upper long to
read 1, with the running-cog set polled throughout the wait; then cog 4 is
started and read, with cog 1 read beside it:

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

Later in the same file, `cogstop(4)` at upper long 2 and a second `start_cog4`
at upper long 4 take the two-missed-wrap readings.

Run B changes the arrangement in one place: both samplers start at the beginning
of the program.

```spin2
  ' ---- both samplers from program start: cog 1 (group 0), cog 4 (group 1)
  start_cog1(@mb1)
  start_cog4(@mb4)
  waitms(10)
  expect_mask(M_C1C4)
```

Each file prints every pair raw, a summary line per reading, and a one-line
verdict. Both are compiled with `pnut-ts` 1.55.8 with DEBUG enabled (`-d`) and
downloaded to RAM; the download must reset the part, since the program checks
that the counter starts from zero. Run A ends about 105 s after reset and Run B
about 44 s after reset.

## Status {#sec-e3-status}

| Field | Content |
|---|---|
| Erratum | E3 |
| Published by Parallax | No |
| Found by | Predicted by the clean-room design study; confirmed here |
| Confirmed on silicon | Yes — 2026-09-24, on a P2 board at 200 MHz, run twice |
| Workaround proven on silicon | Yes |
| Affects | `GETCT WC` in a cog of a four-cog group that had no running cog at one or more wraps of the lower long (measured on cogs 4-7); plain `GETCT` is not affected |
| Test program | `e3-getct-stale-upper-long-runA.spin2`, `e3-getct-stale-upper-long-runB.spin2` |
