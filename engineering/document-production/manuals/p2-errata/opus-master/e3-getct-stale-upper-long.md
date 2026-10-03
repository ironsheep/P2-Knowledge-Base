# Erratum E3: GETCT Returns a Stale Upper Long {#ch-e3}

<!-- include: shared-e3.md -->

## What happens {#sec-e3-actual}

The P2 Documentation describes one counter, a "64-bit free-running counter which increments every clock, cleared on reset", and states that "GETCT WC retrieves upper 32-bits". The Spin2 Language Documentation (v55) says that `GETMS()` and `GETSEC()` use the 64-bit system counter, and that with `DEBUG_TIMESTAMP` declared "each DEBUG message will be time-stamped with the 64-bit CT value". Neither document qualifies these values by cog number, or by which other cogs are running.

What the part does follows from one model, measured on P2 hardware. The eight cogs form two groups of four, cogs 0-3 and cogs 4-7, and each group reads its own copy of the counter. The lower long of that copy is always current. The upper long advances at a wrap of the lower long, once every 2^32^ clocks (21.47 s at 200 MHz), and only if at least one cog of the group is running at that moment. A group with no running cog at a wrap keeps its previous upper long. A cog held in a wait counts as running: a cog held in `WAITATN`, in `WAITX` or in `WAITCT1`, alone in its group, kept the group current.

At reset only cog 0 runs, so cogs 0-3 stay current for as long as one of them runs. Cogs 4-7 have no running cog until the program starts one, and their upper long stays at zero through every wrap until then. A cog started there after the first wrap reads behind by 2^32^ clocks for each wrap missed; starting it does not bring the group up to date. That error is a **stale window** with a known end: it closes at the first wrap the group runs through, in one step, whatever the lag (measured from one, two and eight missed wraps). After that the group stays current for as long as one of its cogs runs. Either group opens a new window if all four of its cogs stop and a wrap passes before one starts again; cogs 0-3 did the same as cogs 4-7.

In a program, `GETMS()` called in Spin2 cog 5 after its group had missed eight wraps (171,798 ms at 200 MHz), at the same moment as in cog 0:

| Called in | `GETMS()` | `GETSEC()` |
|---|---|---|
| cog 0 | 190,617 | 190 |
| cog 5, in the stale window | 18,819 | 18 |
| cog 0, after the window closed | 194,637 | 194 |
| cog 5, after the window closed | 194,637 | 194 |

A `DEBUG_TIMESTAMP` stamp shows the same error, so in a log that mixes messages from both groups, messages sent from the window carry times out of order. An interval timed in 64 bits across the closing wrap includes 2^32^ clocks that did not pass for each wrap the group missed.

Nothing that works on the lower long alone is affected, inside the window or across the wrap that closes it. In PASM2, these time as in an up-to-date group: plain `GETCT`, `ADDCT1`-`ADDCT3` with `WAITCT1`-`WAITCT3`, `POLLCT1`-`POLLCT3`, `JCT1`-`JCT3`, `JNCT1`-`JNCT3`, interrupts on the CT1-CT3 events, the `SETQ` timeout of a wait, and `WAITX`. In Spin2, so do `GETCT()`, `WAITCT()`, `POLLCT()`, `WAITMS()` and `WAITUS()`.

This is the erratum ordinary code meets. A program meets it as soon as it starts a cog of 4-7 after running for more than 21.47 s and takes a 64-bit time there.

## A proven workaround {#sec-e3-workaround}

**What any workaround must do:** take no 64-bit time, a `DEBUG_TIMESTAMP` stamp included, inside a stale window. Either keep a cog of the group running at every wrap from the first wrap on, so that the window never opens, or wait it out: take no 64-bit time in the group until it has run through one wrap since its first cog started.

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

The keeper keeps a cog of 4-7 running through every wrap, so the stale window never opens in cogs 4-7, and a cog your program starts there at any later time reads the same upper long as cog 0: a *one-time startup workaround*. Put the block at the top of your top-level object, ahead of every other `PUB` method, since Spin2 runs the first `PUB` method of the top-level object at start; your own `main()` body follows the `coginit` line. `KEEPER_COG` must be a cog of 4-7 that nothing else in your program starts or stops.

On silicon, with the keeper running, cogs 4, 5 and 6, started after one or two wraps, read the same upper long as cog 0 in every reading. With the keeper stopped, cog 6 read one behind.

**Other ways that meet the condition:**

- **A cog of your own.** A cog your program already starts in 4-7 before the first wrap and never stops does what the keeper does, even if it spends its time waiting. The P2 Documentation does not say which cog a free-cog start chooses, so start that cog in 4-7 by number, or check the cog number the start returns.
- **Waiting it out.** Once the group's first cog has run through one wrap, at most 2^32^ clocks after it starts, the group reads current.

**The cost** is one cog for the life of the program. A program that needs all eight cogs meets the condition if one of its own cogs of 4-7 starts before the first wrap and never stops. The block covers cogs 4-7. Cogs 0-3 stay current through cog 0, which runs `main()`; a program that stops every cog of 0-3 needs the same care there.

**Found by** the clean-room design study, as a prediction, and confirmed on P2 hardware on 2026-09-24. Parallax does not list it.
