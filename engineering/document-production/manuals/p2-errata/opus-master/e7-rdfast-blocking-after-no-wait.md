# Erratum E7: After a No-Wait RDFAST, the Next Hub Instruction Can Complete Early {#ch-e7}

::: caution
**Expected:** a hub read or write issued after a no-wait `RDFAST` (`D[31]` = 1) reads or writes its own hub address, and a waiting `RDFAST` (`D[31]` = 0) waits until the FIFO has begun receiving hub data.

**Actual:** started fewer than 16 clocks after the no-wait `RDFAST`, the next hub instruction can complete before its own hub access: `RDBYTE`, `RDWORD` and `RDLONG` return the previous hub read's data with that value's flags, `WRBYTE`, `WRWORD` and `WRLONG` are lost if a hub read follows at once, a `SETQ` block `RDLONG` writes one wrong long and overwrites cog registers outside its destination or the cog does not finish, and a waiting `RDFAST` skips its wait, so the next `RFLONG` returns `$0000_0000`.

**Workaround:** use the waiting form of `RDFAST`, or start the next hub instruction at least 16 clocks after the start of the no-wait `RDFAST`; see *A proven workaround*.
:::

This erratum affects a cog that starts the hub FIFO with a no-wait `RDFAST` and then issues a hub instruction (a hub read or write, a block read, or another `RDFAST`) before 16 clocks have passed. Whether that instruction is affected depends on the hub alignment of the two addresses and on the spacing, so the same code can run correctly on one pass and fail on the next. A cog that uses only the waiting form of `RDFAST` does not meet it, and neither does a no-wait `WRFAST`; it was measured in cog execution, since `RDFAST` cannot be used in hub execution.

## What the P2 is documented to do {#sec-e7-documented}

The P2 Documentation (Parallax), section RANDOM ACCESS INTERFACE, states what a hub read does:

> For these instructions, the D operand is the register which will receive the data read from the hub. The S/#/PTRx operand supplies the hub address to read from. If WC is expressed, the MSB of the byte, word, or long read from the hub will be written to C. If WZ is expressed, Z will be set if the data read from the hub equaled zero, otherwise Z will be cleared.

and what a hub write does:

> For these instructions, the D/# operand supplies the data to be written to the hub. The S/#/PTRx operand supplies the hub address to write to.

Its section FAST BLOCK MOVES adds the block read: "By preceding RDLONG with either SETQ or SETQ2, multiple hub RAM longs can be read into either cog register RAM or cog lookup RAM."

The section FAST SEQUENTIAL FIFO INTERFACE gives `RDFAST` and `WRFAST` two modes, chosen by bit 31 of the D operand. For the waiting mode:

> If D[31] = 0, RDFAST/WRFAST will wait for any previous WRFAST to finish and then reconfigure the hub FIFO interface for reading or writing. In the case of RDFAST, it will additionally wait until the FIFO has begun receiving hub data, so that it can start being used in the next instruction.

For the no-wait mode:

> If D[31] = 1, RDFAST/WRFAST will not wait for FIFO reconfiguration, taking only two clocks. In this case, your code must allow a sufficient number of clocks before any attempt is made to read or write FIFO data.

The no-wait paragraph's requirement concerns FIFO data, which the cog reads with `RFLONG` and its kin. It places no restriction on a hub read or write at its own address, nor on a later `RDFAST`, and the waiting paragraph makes no exception for a `RDFAST` that follows a no-wait one. By these statements, a hub read issued at any time after a no-wait `RDFAST` returns the data at its own address with flags from that data, a hub write lands at its own address, and a waiting `RDFAST` waits until the FIFO has begun receiving its own address's data.

A FIFO read issued too soon after a no-wait `RDFAST` alone is the case the no-wait paragraph does cover, and it is not this erratum: in the test that found this erratum, such a read returned `$0000_0000`, and the first spacing at which it was correct was 8 to 15 clocks, depending on hub alignment. The documentation states the requirement for that case, and the case belongs to the companion manual *P2 Anti-Patterns*.

The same documentation, section HUB EXECUTION, excludes `RDFAST` from hub execution: "While in hub execution mode, the FIFO cannot be used for anything else. So, during hub execution these instructions cannot be used: RDFAST / WRFAST / FBLOCK".

The KNOWN BUGS section of the P2 Documentation does not list this behaviour.

## What the P2 does {#sec-e7-actual}

In every test below the spacing is counted from the start of the no-wait `RDFAST` to the start of the hub instruction that follows it, the `RDFAST`'s own 2 clocks included. A hub instruction that completes before its own hub access is called *released* below. Every test ran in cog execution, in one cog, at 200 MHz.

**Hub reads and writes.** The arrangement: a `RDLONG` of a known long (the *previous hub read*), a no-wait `RDFAST` (D = `$8000_0000`) of a long in one of the 8 hub RAM slices, 0 to 8 `NOP`s, then the instruction under test at an address in one of the 8 slices. The two slices give 64 hub alignments; each was run 16 times. With k `NOP`s the instruction under test starts 2 + 2k clocks after the no-wait `RDFAST`.

- **`RDLONG`** with the previous hub read `$A5A5_0001` and `$5A5A_0002` at its own address. In the released alignments it wrote `$A5A5_0001` to its destination, in all 16 repetitions; elsewhere, `$5A5A_0002`. The released alignments, at spacings of 2 to 18 clocks:

  | Spacing (clocks) | 2 | 4 | 6 | 8 | 10 | 12 | 14 | 16 | 18 |
  |---|---|---|---|---|---|---|---|---|---|
  | Released alignments, of 64 | 43 | 54 | 61 | 64 | 48 | 32 | 16 | 0 | 0 |

  With the waiting form in place of the no-wait `RDFAST`, the `RDLONG` returned `$5A5A_0002` in all 1,024 records at every spacing.
- **`RDBYTE` and `RDWORD`**, at a spacing of 2 clocks, with the previous hub read `$A1B2_C3D4`: released in the same 43 alignments as `RDLONG`, each returned the byte or word at its own offset within the previous read's long: `$D4`, `$C3`, `$B2` and `$A1` for byte offsets 0 to 3, `$C3D4` and `$A1B2` for word offsets 0 and 2. At 16 clocks none was released.
- **Flags.** A released `RDLONG ... WCZ` set C and Z from the long it returned: `$A5A5_0001` gave C set and Z clear, and with the previous hub read `$0000_0000` it returned `$0000_0000` with C clear and Z set. The correct reads (`$5A5A_0002`) gave C clear and Z clear. Each run had 688 released and 336 correct records. Released `RDBYTE` and `RDWORD` set their flags from the byte or word they returned.
- **`PTRA++`.** A `RDLONG` through `PTRA++` stepped `PTRA` by 4 in all 688 released records and all 336 correct ones.
- **`WRLONG`**, writing `$F0F0_0005` over `$0F0F_0004` at a spacing of 2 clocks, then a `RDLONG` of the same address at once. In the 43 alignments, the write was lost: that `RDLONG` and a later one both read `$0F0F_0004`. In the other 21, the write landed, and the `RDLONG` that followed it at once was released instead and returned the previous hub read's long. With a `NOP` in place of the immediate `RDLONG`, the write landed in all 64 alignments. With the waiting form, it landed and read back correctly in all 1,024 records.
- **`WRBYTE` and `WRWORD`**, at every offset and a spacing of 2 clocks, did the same: the write lost in the 43 alignments when a read of the target followed at once, and landed in all 64 when nothing followed. With the waiting form, every write landed.
- **`SETQ` block `RDLONG`** of 8 longs, started 4 clocks after the no-wait `RDFAST` (the `RDFAST` and the `SETQ`), each trial in a freshly started cog, in four alignments in which a single `RDLONG` at 4 clocks is released, 4 trials each. In two alignments, the block's first long was the previous hub read's long, its other seven were not written, and cog registers `$000` and `$001`, outside the block's destination, changed from `$FC78_00B0` and `$F605_8C64` to `$0000_0060` (or `$0000_0061`) and `$4000_0053`, which are neither block data nor the previous read; the cog then finished its work. In the other two, nothing was written and the cog did not finish within 1 s. The four trials in each alignment were the same. In the scope test's earlier run, the first block read at 4 clocks gave the same first long and seven unwritten longs, and the cog did not finish. With the waiting form, and at spacings of 16, 18 and 20 clocks, the block read the right 8 longs in all 1,024 records, no cog register outside the destination changed, and the cog finished.
- **A no-wait `WRFAST`** in place of the no-wait `RDFAST` released nothing: a `RDLONG ... WCZ` and a `WRLONG` at spacings of 2 and 16 clocks were correct in every record.

**A waiting `RDFAST`.** This is the erratum as first found. The arrangement: a no-wait `RDFAST` (D = `$8000_0000`), then either nothing or a `WAITX`, then a waiting `RDFAST #0` to a different hub address, then `RFLONG` as the next instruction. It was swept over spacings of 2 and 4 to 44 clocks (3 cannot be reached, since every instruction takes at least 2 clocks) in each of 64 hub alignments: the 8 hub RAM slices the waiting `RDFAST`'s address can lie in, each at 8 starting points in the hub's rotation.

- In every alignment, exactly one spacing failed, in all 16 trials. At that spacing the waiting `RDFAST` took 2 clocks, the time of a no-wait `RDFAST`, and the `RFLONG` returned `$0000_0000`: not the first long at the waiting `RDFAST`'s address, not data from the no-wait `RDFAST`'s address, and not the FIFO's earlier contents.
- The failing spacing was between 8 and 15 clocks, set by the hub alignment. Each spacing from 8 to 15 clocks was the failing one in exactly 8 of the 64 alignments.
- At every other spacing tested, the waiting `RDFAST` waited 10 to 17 clocks, and the `RFLONG` returned the correct first long.

In total, 1,024 of 43,008 reads were wrong, every one `$0000_0000`, and the other 41,984 were correct.

The failure needs the no-wait `RDFAST` before the waiting one. In the same test, a waiting `RDFAST` with no `RDFAST` before it gave the correct next-instruction read in all 3,072 trials (with `RFLONG`, `RFWORD` and `RFBYTE`), taking 10 to 17 clocks. With the first `RDFAST` in the waiting form as well, every read was correct in all 18,432 trials at spacings of 2 and 4 to 20 clocks, the two `RDFAST`s together taking 20 to 34 clocks.

## What your program sees {#sec-e7-sees}

If your program issues a hub instruction fewer than 16 clocks after the start of a no-wait `RDFAST`, what it sees depends on the instruction:

- **A `RDBYTE`, `RDWORD` or `RDLONG`** can write its destination with the previous hub read's data in place of the data at its own address: for a `RDBYTE` or `RDWORD`, the byte or word at its own offset within the long that read returned. With `WC`, `WZ` or `WCZ`, the flags are those of the wrong value, so a test on them agrees with the wrong data. A `RDLONG` through `PTRA++` still steps `PTRA`.
- **A `WRBYTE`, `WRWORD` or `WRLONG`** can be lost if a hub read follows it at once (a `RDLONG` of the same address was tested): the hub keeps its old contents, and nothing marks the loss. Where the write lands, that read can be released instead and return the previous hub read's data.
- **A `SETQ` block `RDLONG`** can write one wrong long, the previous hub read's, leave the rest of its destination unwritten, and change cog registers outside its destination; or the cog can stop responding.
- **A waiting `RDFAST`**, issued 8 to 15 clocks after the no-wait one, can take 2 clocks without waiting, and the `RFLONG` that follows returns `$0000_0000` in place of the first long at the new address, with the flags of a zero long (C clear, Z set) in every failing trial the test printed. The long after the zero is not the second long either: where the new address lay in hub slice 0, 1 or 2, the second `RFLONG` returned the first long at that address; in slices 3 to 7 it returned `$0000_0000` again.

None of these is flagged: the program sees the wrong data, the lost write, or a cog that has stopped, and no error.

Whether it happens depends on the spacing and on the hub alignment at the moment your code runs. At a spacing of 2 clocks, a `RDLONG` was released in 43 of 64 alignments; at 8 clocks, in all 64; at 14 clocks, in 16. The same code can therefore read correctly on one pass and return the wrong value on another. From 16 clocks on, no hub read or block read tested was released in any alignment, and a waiting `RDFAST` read correctly at every spacing from 16 to 44 clocks. Writes were tested at a spacing of 2 clocks only.

Whether a cog that stopped responding after a released block read wrote to hub RAM afterwards was not observed.

## A proven workaround {#sec-e7-workaround}

**What any workaround must do:** after a no-wait `RDFAST`, start no hub instruction until at least 16 clocks have passed from the start of the `RDFAST`; or use the waiting form of `RDFAST`.

**One way, proven on P2 hardware:** a `WAITX #RDFAST_SPACING_WAITX` (12) directly after the no-wait `RDFAST`.

```pasm2
CON
  RDFAST_SPACING_WAITX = 12            ' RDFAST 2 + WAITX 2+12 = 16 clocks
DAT
        rdfast  nowait, hub_first      ' no-wait RDFAST (D[31] = 1)
        waitx   #RDFAST_SPACING_WAITX  ' E7: >= 16 clocks, RDFAST to RDFAST
        rdfast  #0, hub_next           ' blocking RDFAST: now it waits
        rflong  first_long             ' reads hub_next's first long
```

The `WAITX #RDFAST_SPACING_WAITX` (12) makes the spacing from the start of the no-wait `RDFAST` to the start of the next hub instruction, here a waiting `RDFAST`, 16 clocks, so that the waiting `RDFAST` waits and the `RFLONG` after it reads the first long at `hub_next`; it is a rule at each use, applied wherever your code issues a hub instruction after a no-wait `RDFAST`.

In your code, `nowait` is a register holding `$8000_0000` (`D[31]` = 1, and a block count of 0, so no wrap); `hub_first` and `hub_next` hold the two hub addresses, and `first_long` receives the first long at `hub_next`. The comment's *blocking* is the test programs' name for the waiting form.

The rule is the spacing: at least 16 clocks from the start of the no-wait `RDFAST` to the start of the next hub instruction. The no-wait `RDFAST` takes 2 clocks and `WAITX #RDFAST_SPACING_WAITX` takes 2 + 12 = 14. The block above ran in the workaround test on 2026-09-26: in all 64 alignments, 16 trials each, `first_long` received the first long at `hub_next`, and the next `RFLONG` the long after it, in 1,024 of 1,024 trials, with the waiting `RDFAST` waiting 10 to 17 clocks. In the same run the unspaced arrangement failed as described above in all 64 alignments.

**Other ways that meet the condition, proven on P2 hardware.**

- **The waiting form.** A `RDFAST` with `D[31]` = 0 in place of the no-wait one released nothing: `RDLONG` correct at every spacing from 2 to 18 clocks; `RDBYTE`, `RDWORD` and the flags correct; `WRLONG`, `WRBYTE` and `WRWORD` landed; the `SETQ` block `RDLONG` correct with cog RAM intact; and a waiting `RDFAST` after it read correctly, in every alignment and trial tested. It is the one way proven for hub writes.
- **Seven two-clock instructions before a read.** Seven `NOP`s between the no-wait `RDFAST` and a `RDLONG`, `RDBYTE` or `RDWORD` (16 clocks) released nothing in any alignment, and neither did eight before a `RDLONG`. Before a `SETQ` block `RDLONG`, six `NOP`s and the `SETQ` (16 clocks), seven (18) and eight (20) read the right block with cog RAM intact; the `SETQ` counts as one of the seven.

Other instructions that fill at least 16 clocks meet the same condition, since the measurements tie the release to the spacing: they have not been run. Only `NOP` and `WAITX` were placed in the window. A hub write started 16 clocks or more after a no-wait `RDFAST` has not been run either: for writes, the spacing is the condition the reads set, not a proven way.

The cost: the waiting form waits for the FIFO, 10 to 17 clocks for a `RDFAST` alone in the tests above, where a no-wait `RDFAST` takes 2; the spacing costs up to 14 clocks after each no-wait `RDFAST` that a hub instruction follows, less where the instructions in between do other work.

The limits of the proof:

- Tested after a no-wait `RDFAST`: `RDBYTE`, `RDWORD`, `RDLONG`, `WRBYTE`, `WRWORD`, `WRLONG`, a `SETQ` block `RDLONG` of 8 longs into cog registers, and a waiting `RDFAST` followed by `RFLONG`. Not tested: `WMLONG`, `SETQ2` block reads, `SETQ` block writes, `RETA` and the other instructions that read the hub stack, the other hub instructions, an interrupt taken inside the window, and the streamer.
- `RDLONG` was tested at spacings of 2 to 18 clocks; `RDBYTE` and `RDWORD` at 2 and 16; the flags and `PTRA++` at 2; `WRLONG`, `WRBYTE` and `WRWORD` at 2 only; the no-wait `WRFAST` at 2 and 16; the block read at 4, 16, 18 and 20 clocks, in four alignments at 4 clocks; the waiting `RDFAST` at 2 and 4 to 44 clocks.
- What changed cog registers `$000` and `$001`, and whether a cog that did not finish had stalled or was running elsewhere, are not known.
- Only cog execution was tested, with one cog using its FIFO, at 200 MHz.

## Why it happens {#sec-e7-why}

The P2 Documentation does not describe this behaviour. What follows is the account that fits every measurement above, at the level of the programmer's model; it is not a description of the design.

A no-wait `RDFAST` returns after 2 clocks, but the FIFO it started goes on fetching. When the FIFO's first long arrives, 8 to 15 clocks after the `RDFAST` starts, depending on hub alignment, a hub instruction that the cog is still waiting on at that moment is ended as if its own hub access had completed. A read ended that way has fetched nothing of its own, and its destination receives the previous hub read's data, with flags from that value. A write ended that way has not yet reached the hub, and a hub instruction issued next takes its place. A waiting `RDFAST` ended that way returns before its own data has arrived.

The measurements this account rests on:

- **The release follows the arrival of the FIFO's first long.** In the test that found the waiting-`RDFAST` case, the failing spacing at each of the 8 starting points in the hub's rotation equalled the spacing at which an `RFLONG` after a no-wait `RDFAST` alone first read correctly (table under *How it was proven on P2 hardware*). It was the same for all 8 slices of the waiting `RDFAST`'s address, and so follows the no-wait `RDFAST`, not the waiting one. One clock earlier and one clock later, the waiting `RDFAST` waited as usual: in slice 0 at the first starting point, it waited 11 clocks at a spacing of 9, took 2 at a spacing of 10, and waited 17 at a spacing of 11.
- **The window matches an instruction still waiting when the first long arrives.** A `RDLONG` waits for its hub slot after it starts. Started 2 clocks after the no-wait `RDFAST`, it was released in 43 alignments; started at 8 clocks, in all 64; started at 10, 12 and 14 clocks, in 48, 32 and 16; started at 16 clocks, after the latest arrival measured (15 clocks), in none. This is the pattern expected if only an instruction still waiting for the hub at the arrival is released.
- **A released read returns old data, not new.** Its value is the previous hub read's, never the FIFO's data or the data at its own address.

What is not known: why a waiting `RDFAST` that returns early leaves the next `RFLONG` reading `$0000_0000`, what writes cog registers `$000` and `$001` during a released block read, and why a cog can stop responding after one.

## How it was proven on P2 hardware {#sec-e7-proof}

**Where it came from.** The erratum was first found on the bench, by a test built to measure something else: when the hub FIFO can first be used after `RDFAST` and `WRFAST`, in both modes. A waiting `RDFAST` after a no-wait one was among its secondary arrangements, expected to show the waiting promise holding. The clean-room design study then predicted that a no-wait `RDFAST` releases any hub instruction waiting at that moment, not only a `RDFAST`; three further tests confirmed it, and measured the workaround on block reads.

All five tests ran on one P2 board at 200 MHz, used no pins, and kept the debugger in cog 0 (`DEBUG_COGS = %0000_0001`), which sent the commands, classified the results from hub RAM and printed them. Every measurement ran in a measuring cog started by `COGINIT`, in cog execution. Each program's expected outcomes, and the outcomes that would refute them, were written into it before the run, and each prints every measured value, so its verdict can be re-derived from its output.

**The release test.** Each trial read a primer long, `$A5A5_0001`, with `RDLONG` (which also ties the cog to the hub rotation), issued the `RDFAST` (no-wait, or waiting) of a stream long in slice *f*, then k `NOP`s (k = 0 to 8), then the instruction under test on a long in slice *r*: 64 alignments (*f*, *r*), 16 repetitions each, 1,024 records per run, read back after the cog had settled. For reads, the instruction under test was a `RDLONG` of `$5A5A_0002` into a register preset to `$C3C3_0003`. For writes, it was a `WRLONG` of `$F0F0_0005` over `$0F0F_0004`, read back at once by `RDLONG` (or after a `NOP`), and again after settling. After every command the measuring cog reported the `RDFAST` mode it had run, and the program stopped if it was not the mode sent.

- Its controls: with a `NOP` in place of the `RDFAST`, the `RDLONG` read `$5A5A_0002` and the write landed, in all 1,024 records; and a no-wait `RDFAST`, `WAITX #200` and `RFLONG` read the stream's first long in all 1,024, which shows that the `RDFAST` under test starts a stream at its address.
- No record held anything but the values named above, and every alignment's 16 repetitions were the same.
- The released counts by spacing are the table under *What the P2 does*: 688 of 1,024 records at k = 0, and none at k = 7 or 8. The write runs gave 43 lost writes and 21 released read-backs per repetition with the read-back at once, and every write landed with a `NOP` in its place.
- The same run repeated the first-found arrangement over spacings of 2 and 4 to 20 clocks, as a positive control: one failing spacing per alignment, at the same spacings as in the first test (table below). With the first `RDFAST` in the waiting form, every read was correct, in all 18,432 trials.

**The scope test.** The release test's construction, run for `RDBYTE` (offsets 0 to 3), `RDWORD` (offsets 0 and 2), `WRBYTE`, `WRWORD`, `RDLONG ... WCZ` (flags preset to C set and Z set, with a primer of `$A5A5_0001` and of `$0000_0000`), `RDLONG` through `PTRA++`, a no-wait `WRFAST` in place of the `RDFAST`, and a `SETQ #7` block `RDLONG` into a guarded range of cog registers. Each run had its own `NOP` control and waiting form. As its positive control, it reproduced the release test's `RDLONG` result first: 688 released records at k = 0, none at k = 7. In every run the released records fell in the same 43 alignments, and no repetition disagreed. The results are under *What the P2 does*. The block read at 4 clocks ran once, in its first trial: the measuring cog did not finish within 1 s, and the program stopped it.

**The block-read workaround test.** Every run and every trial in a freshly started cog, whose cog RAM was checked against the loaded image before and after. It first reproduced the release test's `RDLONG` result as its positive control, then ran single block reads at 4 clocks in four alignments, 4 trials each, with a `NOP` control in each: the right block, cog RAM intact, the cog finished. Then the workaround: the waiting form, and 6, 7 and 8 `NOP`s with the `SETQ` (16, 18 and 20 clocks), 1,024 records each.

**The first-found test.** Three data regions, each starting on a 32-byte boundary, so that long k of a region lies in hub slice k mod 8: the no-wait `RDFAST`'s region, long k = `$3C3C_00C0` + k; the waiting `RDFAST`'s region, `$A5A5_0080` + k; and a third region, `$0D0D_0040` + k, that the FIFO was loaded from before every trial, so that a stale read would show as `$0D0D_0042`. Each trial then read a slice-0 long with `RDLONG`, waited the starting point, 0 to 7 clocks, and between two `GETCT`s ran the no-wait `RDFAST` of the first region's long 0, the spacing, the waiting `RDFAST #0` of long s of the second region, and `RFLONG` with `WCZ`. A second `RFLONG` followed. The sweep: 8 slices s times 8 starting points gives 64 alignments; 42 spacings (2, and 4 to 44 clocks); 16 trials of each, 43,008 trials in all. The 8 starting points span a whole hub rotation: a waiting `RDFAST` alone took 8 different times over them, in every slice. The waiting `RDFAST`'s own clocks are the `GETCT` difference less the `GETCT` overhead, the spacing and the `RFLONG`.

Its controls, each of which had to pass before the program would print a verdict: a `GETCT` pair costs 2 clocks, and `WAITX` D costs 2 + D clocks at every delay the sweep used; plain `RDLONG`s read every pattern long at every slice; with no new `RDFAST`, the loaded FIFO returned `$0D0D_0042` and then the long after it; a no-wait `RDFAST`, then `WAITX #200`, then `RFLONG`, returned the right longs. The program's write controls ran as well. Every control was correct in every trial of both runs.

The failing spacing at each starting point, and the spacing at which an `RFLONG` after a no-wait `RDFAST` alone first read correctly, in clocks:

| Starting point (clocks) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| Failing spacing, every slice | 10 | 9 | 8 | 15 | 14 | 13 | 12 | 11 |
| First correct no-wait read, slice 0 | 10 | 9 | 8 | 15 | 14 | 13 | 12 | 11 |

At each failing spacing, all 16 trials read `$0000_0000`, and the waiting `RDFAST` took 2 clocks. Every spacing from 16 to 44 clocks read correctly in every alignment and trial. Around the failure, in slice 0 at starting point 0:

| Spacing (clocks) | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|
| Waiting `RDFAST` (clocks) | 13 | 12 | 11 | 2 | 17 | 16 |
| `RFLONG` returned | correct | correct | correct | `$0000_0000` | correct | correct |

**The spacing workaround test.** The first-found test's regions, loading and alignments, with the block printed in *A proven workaround*, with nothing else between its lines, in all 64 alignments. Its controls were the four above and one more: `WAITX #RDFAST_SPACING_WAITX` (12) between two `GETCT`s measured 16 clocks, 2 for the `GETCT` pair and 14 for the `WAITX`, in every trial. As a positive control, the same run swept the unspaced arrangement over the same 42 spacings; it failed at exactly one spacing in each of the 64 alignments, at the same spacings as in the first-found test, 1,024 of 43,008 reads wrong, and at every spacing from 16 to 44 clocks the first read and the long after it were correct in all 29,696 trials. The block read the first long at `hub_next` and then the long after it in 1,024 of 1,024 trials, its waiting `RDFAST` taking 8 different times over the 8 starting points in every slice.

**When they ran.** The first-found test ran on 2026-09-25, twice; the two runs printed the same result for every alignment and spacing. The spacing workaround test ran on 2026-09-26, once. The release test, the scope test and the block-read workaround test ran on 2026-10-01, once each; every control in each was correct.

## The test program {#sec-e7-program}

Five programs in the examples archive measured this erratum.

The erratum as first found is `e7-rdfast-blocking-after-no-wait-test.spin2`. Its Spin2 code in cog 0 starts the measuring cog, sends it one command per arrangement, slice and starting point, classifies every trial, prints every row, checks the controls, and prints the verdicts. The measuring cog is PASM2 in the program's `DAT` block and is the only code that touches the FIFO. Besides the waiting-`RDFAST` arrangement, the program measures waiting and no-wait `RDFAST` and `WRFAST` on their own, and a second no-wait `RDFAST` in place of the waiting one.

Each trial of the waiting-`RDFAST` arrangement starts after the FIFO has been loaded. It ties the cog to the hub rotation, waits the starting point, and starts the timing:

```pasm2
v_rebn          rdlong  c_junk, c_oldb
                waitx   c_phase
                getct   c_t0
```

The next three lines, whose comments run past this page's width, are `rdfast c_nowait, c_midb` (the no-wait `RDFAST`; `c_nowait` holds `$8000_0000`), `waitx c_dly` (the spacing), and `rdfast #0, c_new` (the waiting `RDFAST`). Then the read, in the next instruction:

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

`INSTR_CLK` is 2 and `NW_WAITX_OFFSET` is 4, and the measuring cog loads `c_dly` with j - 1, so j = 1 to 41 gives 4 to 44 clocks. A run that decides the question prints no `RIG FAIL` lines; the waiting-`RDFAST` arrangement shows as the second `ARM-VERDICT` line, which reads `DEVIATES` with 1,024 of 43,008 reads wrong.

The spacing workaround test is `e7-workaround-rdfast-spacing-test.spin2`. It uses the same construction and the same trial, and runs the block printed in *A proven workaround*, between two marker comments, in all 64 alignments. Alongside, it runs the unspaced arrangement at every spacing from 2 to 44 clocks: a clean result for the block counts only if that sweep shows the erratum in every alignment, and otherwise the program reports the workaround as inconclusive. It ends with a `VERDICT E7 WORKAROUND:` line.

The release test is `e7-next-hub-instruction-test.spin2`, the scope test `e7-every-hub-width-test.spin2`, and the block-read workaround test `e7-workaround-setq-block-test.spin2`. They share one construction: the measuring cog holds one hand-written copy of the trial for each k, so that nothing but the `RDFAST` and the k `NOP`s sits between the primer read and the instruction under test, and no `##` operand there adds an `AUGS`. Cog 0 fills the record area with `$EEEE_EEEE` before every command, so a record the measuring cog never wrote shows as unwritten. Each program prints its predictions before the first run and ends with one verdict line per prediction.

The release test's read trial with seven `NOP`s, the spacing of 16 clocks:

```pasm2
r_k7            rdlong  c_tmp, c_prim
                rdfast  c_mode, c_pf
                nop
                nop
                nop
                nop
                nop
                nop
                nop
                rdlong  c_dst, c_pr
                jmp     #r_settle
```

`c_prim` holds the primer's address, `c_mode` the `RDFAST`'s D (`$8000_0000` for the no-wait form, 0 for the waiting form), `c_pf` the stream's address in slice *f*, and `c_pr` the address of the `RDLONG` under test in slice *r*. The copies for k = 0 to 6 and 8 differ only in the number of `NOP`s.

To run any of them, compile with `pnut-ts -d` and load it to RAM with DEBUG enabled. They use no pins.

## Status {#sec-e7-status}

| Field | Content |
|---|---|
| Erratum | E7 |
| Published by Parallax | No |
| Found by | Found on the bench here, by a test built to measure something else; its reach to every hub read and write was predicted by the clean-room design study and confirmed here |
| Confirmed on silicon | Yes — 2026-09-25 (run twice) and 2026-10-01 (three tests, run once each), on a P2 board at 200 MHz |
| Workaround proven on silicon | Yes — 2026-09-26 and 2026-10-01, on a P2 board at 200 MHz; a rule at each use: the waiting form of `RDFAST`, or at least 16 clocks from the start of the no-wait `RDFAST` to the start of the next hub instruction |
| Affects | a hub instruction started fewer than 16 clocks after a no-wait `RDFAST`: hub reads return the previous hub read's data and its flags, hub writes are lost when a hub read follows at once, a `SETQ` block `RDLONG` writes a wrong long and overwrites cog registers or the cog does not finish, and a waiting `RDFAST` does not wait, so the next `RFLONG` returns `$0000_0000`. Tested in cog execution |
| Test program | `e7-rdfast-blocking-after-no-wait-test.spin2`, `e7-next-hub-instruction-test.spin2`, `e7-every-hub-width-test.spin2`; the workaround: `e7-workaround-rdfast-spacing-test.spin2`, `e7-workaround-setq-block-test.spin2` |
