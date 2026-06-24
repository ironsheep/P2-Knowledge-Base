# P2 PASM2 Tutorial (deSilva style) — Examples Library

These are the complete, runnable programs that appear in the deSilva-style P2
PASM2 tutorial, one file per worked example, named by the chapter it appears in.

- **Exactly as printed.** Each file is the program shown in the tutorial, verbatim
  — the same code carried by the printed caption (e.g. `ch01-first-blink.spin2`)
  under the block.
- **Complete and runnable.** Each is a whole program — a Spin2 launcher plus its
  inline PASM2 (`DAT`) cog code — not one of the tutorial's many teaching
  fragments. The bare PASM2 snippets shown to make a point are *not* here.
- **Keeps running.** Each ends in a `repeat` (and the launched cogs loop on a
  `jmp`), so the program keeps running after it starts.
- **Compiles clean.** Every file compiles with `pnut-ts`.

Open one in your P2 toolchain, compile, and run it on a P2.

## Index

| File | Chapter | What it shows |
|------|---------|---------------|
| `ch01-first-blink.spin2` | 1 — Your First Spin | Launch PASM2 in a cog from Spin2 to blink an LED |
| `ch02-multicog-blink.spin2` | 2 — Architecture Safari | Four cogs running the same code in parallel, each blinking its own pin at its own rate |
| `ch02-hub-counters.spin2` | 2 — Architecture Safari | Eight cogs each incrementing an independent counter in hub RAM |
