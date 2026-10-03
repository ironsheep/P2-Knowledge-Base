::: caution
**Who meets it:** PASM2 that runs DDS/Goertzel bursts one at a time, with the streamer idle between them, and relies on `GETXACC` to clear the accumulators.

**What you see:** with the streamer idle, `GETXACC` returns the sums but clears nothing, so each burst adds to what earlier bursts left and each reading is a running total.

**What to do:** take each burst's sums as the difference of two readings taken with the streamer idle, one before the burst and one after it. The `burst_sums` routine does this, and steps around Erratum E5 as well.
:::
