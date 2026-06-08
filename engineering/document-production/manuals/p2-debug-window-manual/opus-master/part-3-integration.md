```{=latex}
\part{Integration}
```

The window chapters each drove one window in one direction: your program produces
output, the window shows it. Real debugging asks for more, and Part III covers the
three things you reach for once the individual windows are familiar.

[Chapter 12](#ch-12) reverses the flow — `PC_KEY` and `PC_MOUSE` read the host's keyboard
and mouse back through the same debug link, turning any window into a control
surface. [Chapter 13](#ch-13) makes that link carry more: packed-data modes fold many small
samples into a single `DEBUG()` call so a high-rate capture keeps up. [Chapter 14](#ch-14)
runs several windows at once and reaches into PASM2, driving the same windows from
assembly in their own cog.

None of these is a new window. Each is a technique that combines the windows you
already know.
