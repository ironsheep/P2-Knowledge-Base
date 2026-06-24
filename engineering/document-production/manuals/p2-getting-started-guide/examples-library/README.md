# Getting Started with the Propeller 2 — Examples Library

These are the complete, runnable Spin2 programs that appear in *Getting Started with
the Propeller 2*, one file per worked example, named by the chapter it appears in.

- **Exactly as printed.** Each file is the program shown in the guide, verbatim — the
  same code carried by the printed caption (e.g. `ch03-blink-led.spin2`) under the
  block.
- **Complete and runnable.** Each is a whole program, not a snippet; the guide's many
  teaching fragments (the block skeleton, a method header, the indentation demo) are
  *not* here — only the programs you'd actually load and run.
- **Keeps running.** Every program ends in a `repeat` loop, so it keeps running after
  it starts.
- **Compiles clean.** Every file compiles with `pnut-ts`.

Open one in your P2 toolchain, compile, and run it on a P2.

## Index

| File | Chapter | What it shows |
|------|---------|---------------|
| `ch03-blink-led.spin2` | 3 — Putting It to Work | Your first program — blink an LED on one pin |
| `ch03-two-cog-blink.spin2` | 3 — Putting It to Work | Launch a second cog so two LEDs blink in parallel |
| `ch03-shared-mailbox.spin2` | 3 — Putting It to Work | Share data between cogs through a hub variable (a mailbox) |
| `ch03-inline-pasm-toggle.spin2` | 3 — Putting It to Work | Drop inline PASM2 into a Spin2 method — one native instruction at full speed |
