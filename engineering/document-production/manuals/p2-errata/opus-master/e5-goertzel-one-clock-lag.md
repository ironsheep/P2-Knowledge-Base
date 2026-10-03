# Erratum E5: The Goertzel Accumulators Trail by One Clock {#ch-e5}

<!-- include: shared-e5.md -->

## What happens {#sec-e5-actual}

The P2 Documentation describes the DDS/Goertzel mode as one that "outputs and inputs on every clock in which the command is active", and its table of accumulation modes gives the SINC1 case as `SIN_ACC += SIN_MUL` and `COS_ACC += COS_MUL` on each of those clocks. By that description a command active for N clocks adds N terms to each accumulator, and a `GETXACC` issued after it returns all N.

On P2 hardware, each active clock adds the term formed on the **previous** active clock. After a Goertzel burst of N clocks:

- the accumulators hold the burst's first N-1 terms;
- the last term is held internally. `GETXACC` does not return it, and waiting does not deliver it: a second reading 1,000 clocks after the first had not moved;
- the first clock of the next Goertzel burst adds the held term, ahead of that burst's own terms.

No term is lost; each burst's last term arrives one burst late. With a steady input the carried term stands in for the missing one from the second burst on, so a burst that directly followed another read N terms, while a burst that followed a zero burst read N-1. When the input changes from clock to clock, each reading is the previous burst's last term plus the first N-1 terms of its own.

Like Erratum E4, this reaches only programs that measure with the Goertzel mode, and a reading taken with `GETXACC` after each burst.

The confirmation is for SINC1 mode, with one input pin summed, for bursts of 64 and 65 clocks started by `XINIT` from an idle streamer. Whether a command in another streamer mode between bursts disturbs the held term was not tested.

## A proven workaround {#sec-e5-workaround}

**What any workaround must do:** deliver the burst's held last term to the accumulators before reading them, in SINC1 mode.

**One way, proven on P2 hardware:** the helper routine printed in Erratum E4, `burst_sums`. It ends every burst with a short burst whose terms are all zero before it reads, so each call returns all N terms of your burst and leaves no term held for the next. One call steps around both errata. On silicon it returned exactly N terms in all 60 calls of its test program, including the 6 calls made while an earlier burst's term was still held.

**Another way:** any Goertzel burst whose terms are all zero, run after your burst and before the reading, delivers the held term. The kind measured is the routine's own: a count of 4 with `S[15:12]` clear.

**The limits:** SINC1 only. The routine's zero burst has not been tested as a flush in SINC2 mode. SINC2 has its own documented constraint, which is not this erratum: the P2 Documentation's note on Goertzel SINC2 mode states that a varying number of iterations in a Goertzel cycle corrupts the current and next samples. Its two remedies, a constant iteration count or commands issued with `XZERO`, held on P2 hardware.

**Found by** the clean-room design study, as a prediction, and confirmed on P2 hardware on 2026-09-24. Parallax does not list it.
