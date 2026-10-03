# Erratum E7: After a No-Wait RDFAST, the Next Hub Instruction Can Complete Early {#ch-e7}

<!-- include: shared-e7.md -->

## What happens {#sec-e7-actual}

The P2 Documentation, section FAST SEQUENTIAL FIFO INTERFACE, gives `RDFAST` two modes, chosen by bit 31 of D. For the waiting mode:

> If D[31] = 0, RDFAST/WRFAST will wait for any previous WRFAST to finish and then reconfigure the hub FIFO interface for reading or writing. In the case of RDFAST, it will additionally wait until the FIFO has begun receiving hub data, so that it can start being used in the next instruction.

For the no-wait mode:

> If D[31] = 1, RDFAST/WRFAST will not wait for FIFO reconfiguration, taking only two clocks. In this case, your code must allow a sufficient number of clocks before any attempt is made to read or write FIFO data.

That requirement concerns FIFO data, which the cog reads with `RFLONG` and its kin. Neither paragraph restricts a hub read or write at its own address after a no-wait `RDFAST`, or makes an exception for a waiting `RDFAST` that follows one. A FIFO read too soon after a no-wait `RDFAST` is the case the no-wait paragraph does cover, and it is not this erratum.

On P2 hardware, in cog execution, a hub instruction started fewer than 16 clocks after the start of a no-wait `RDFAST` can complete before its own hub access. Counted from the start of the `RDFAST`, its own 2 clocks included:

- a `RDBYTE`, `RDWORD` or `RDLONG` returns the previous hub read's data instead of the data at its own address, and its `WC`/`WZ` flags agree with that wrong value;
- a `WRBYTE`, `WRWORD` or `WRLONG` is lost if a hub read follows it at once;
- a `SETQ` block `RDLONG` writes one wrong long and changes cog registers outside its destination, or the cog stops responding;
- a waiting `RDFAST` takes 2 clocks without waiting, and the `RFLONG` after it returns `$0000_0000`.

Nothing flags any of these. Whether an instruction is affected depends on the hub alignment of the two addresses, so the same code can work on one pass and fail on the next. The release coincides with the arrival of the FIFO's first long, 8 to 15 clocks after the `RDFAST` starts: at 2 clocks a `RDLONG` was released in 43 of the 64 alignments, at 8 clocks in all 64, at 14 in 16, and from 16 clocks on in none. A no-wait `WRFAST` released nothing.

The condition is narrow. It needs a hub instruction within seven two-clock instructions of a no-wait `RDFAST`, and code normally does other work there. Code that uses only the waiting form never meets it, and `RDFAST` cannot be used in hub execution.

## A proven workaround {#sec-e7-workaround}

**What any workaround must do:** after a no-wait `RDFAST`, start no hub instruction until at least 16 clocks have passed from the start of the `RDFAST`; or use the waiting form of `RDFAST`.

**One way, proven on P2 hardware:** a `WAITX #HUB_SPACING_WAITX` (12) directly after the no-wait `RDFAST`, with the constant in a `CON` block:

```pasm2
  HUB_SPACING_WAITX = 12                ' RDFAST 2 + WAITX 2+12 = 16 clocks
```

```pasm2
        rdfast  nowait, hub_stream      ' no-wait RDFAST (D[31] = 1)
        waitx   #HUB_SPACING_WAITX      ' E7: >= 16 clocks to next hub op
        rdlong  value, hub_addr  wcz    ' hub_addr's long, and its flags
```

The `WAITX` makes the spacing to the next hub instruction 16 clocks: a *rule at each use*, applied wherever a hub instruction follows a no-wait `RDFAST`. In your code, `nowait` is a register holding `$8000_0000`, `hub_stream` holds the FIFO's start address, `hub_addr` the address read, and `value` receives the long. On silicon this block returned the long at `hub_addr` with its own flags in all 64 hub alignments, 16 trials each; the same spacing before a `WRLONG`, `WRWORD` or `WRBYTE` landed every write.

**Another way, proven on P2 hardware: the waiting form.** A `RDFAST` with `D[31]` = 0 needs no spacing:

```pasm2
        rdfast  #0, hub_stream          ' waiting RDFAST (D[31] = 0)
        wrlong  value, hub_addr         ' lands at hub_addr
        rdlong  check, hub_addr  wcz    ' reads value back, and its flags
```

In every test that ran it, for every instruction above, the waiting form released nothing. Its cost is the wait for the FIFO, 10 to 17 clocks where a no-wait `RDFAST` takes 2.

**Other instructions in the window** meet the condition just as well, since the release depends only on the spacing: seven two-clock instructions after the no-wait `RDFAST` released nothing (`NOP`s were tested), and before a `SETQ` block `RDLONG` the `SETQ` counts as one of the seven.

**The limits:** tested in cog execution, one cog, 200 MHz, for the instructions listed above. `WMLONG`, `SETQ2` block reads, `SETQ` block writes, the instructions that read the hub stack, an interrupt taken inside the window, and the streamer were not tested.

**Found by** a bench test built to measure something else, on 2026-09-25. The clean-room design study then predicted that the condition reaches every hub read and write, and P2 hardware confirmed it on 2026-10-01. Parallax does not list it.
