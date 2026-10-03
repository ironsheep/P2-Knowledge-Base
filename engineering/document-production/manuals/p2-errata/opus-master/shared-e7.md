::: caution
**Who meets it:** PASM2 that starts the hub FIFO with a no-wait `RDFAST` (`D[31]` = 1) and starts another hub instruction fewer than 16 clocks later: a hub read or write, a `SETQ` block read, or a waiting `RDFAST`. Code that does other work in between, or uses the waiting form, does not meet it.

**What you see:** that instruction can complete early. A read returns the previous hub read's data, with that value's flags; a write is lost if a hub read follows it at once; a block read writes wrong data, or the cog stops responding; a waiting `RDFAST` does not wait. Whether it happens depends on hub alignment, so the same code can work on one pass and fail on the next.

**What to do:** allow at least 16 clocks from the start of the no-wait `RDFAST` to the next hub instruction (`WAITX #12` directly after it, or seven two-clock instructions), or use the waiting form.
:::
