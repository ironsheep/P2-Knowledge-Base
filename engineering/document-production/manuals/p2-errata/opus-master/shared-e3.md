::: caution
**Who meets it:** a program that reads a 64-bit time (`GETCT WC`, `GETMS()`, `GETSEC()`, or a `DEBUG_TIMESTAMP` stamp) in a cog of 4-7 that it starts more than 2^32^ clocks after reset (21.47 s at 200 MHz). The same applies to either group of four cogs once all of its cogs have stopped and a cog starts there again after a wrap of the counter's lower long.

**What you see:** that time reads behind by 2^32^ clocks for each wrap the group missed, until the group's next wrap, at most 2^32^ clocks later. Plain `GETCT` and every wait on the counter time correctly.

**What to do:** start a cog in 4-7 on the first line of `main()` and never stop it.
:::
