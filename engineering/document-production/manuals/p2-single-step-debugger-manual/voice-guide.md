# Voice Guide — P2 Single-Step Debugger Manual

**Status:** DRAFT for review (Phase 1)
**Created:** 2026-05-31

This guide defines the voice for the P2 Single-Step Debugger Manual. It is a
*teaching user manual* — not a terse reference, not a whimsical tutorial.

---

## Who the reader is

- **Knows the P2 only lightly.** May be coming from the P1 (Propeller 1), or may
  be newer still. Comfortable that the P2 has COGs, hub RAM, registers, pins —
  but not deeply fluent.
- **Has never used this debugger.** Possibly has never used *any* single-step
  debugger. We cannot assume the reader knows what a breakpoint, a watch, or
  single-stepping even is.
- **Wants to accomplish something**, not admire the tool: "my code isn't doing
  what I expect — how do I see what's happening?"

**Design consequence:** introduce every concept before we use it, and motivate
*why* before *how*. The reader should never meet a term cold.

## What we are teaching (the actual goal)

How to **use the single-step debugger** to understand and fix P2 programs:
- what single-step debugging *is* and when to reach for it,
- what you can **observe** (COG/LUT/hub memory, registers, C/Z flags, PC, the
  call stack, smart pins, events),
- what you can **control** (step, run, break, breakpoints of several kinds),
- and the concrete keystrokes/mouse actions that do each of those.

## Tone

- **Mentor at your shoulder.** Calm, plain, second person ("you"). "Let's set a
  breakpoint and watch what happens" — guided, not lectured.
- **Confident and concrete.** Real keys, real registers, real addresses. No
  hedging, no marketing ("powerful", "revolutionary" — cut these; the old source
  docs are full of them).
- **Respectful of the reader's time.** Short sentences. One idea per paragraph.
  Tables for command/register reference; prose for concepts and workflows.

## Rules (the discipline that keeps this manual trustworthy)

1. **Introduce-before-use.** First mention of breakpoint / watch / single-step /
   heat map / SFR gets a one-line plain-language definition. No forward
   references to undefined terms.
2. **P2, never P1.** Use P2 syntax exclusively: `COGINIT` / `COGSPIN` (never
   `cognew`), `GETCT` (never `CNT`). When a P1 habit is a likely trap, name it
   once explicitly ("P1 used `cognew`; on the P2 you use `COGSPIN`/`COGINIT`").
3. **Correct tooling, always.** The compiler is **`pnut_ts`** (`-d` / `--debug`
   compiles with DEBUG enabled). The host program that shows the debugger and the
   DEBUG display windows is **`pnut_term_ts`**. There is no "PNut IDE", no
   `Run → Debug Enable` menu, no `pnut.exe`. Any such reference from the source
   docs is removed.
4. **Valid DEBUG formatters only.** `UDEC/SDEC/UHEX/SHEX/UBIN` (each with an
   optional trailing `_` to suppress the auto label). Never bare `DEC/HEX/BIN`
   (not valid Spin2 DEBUG output formatters). Every code example must be
   compilable by `pnut_ts`.
5. **Stay in our lane.** The nine DEBUG **display windows** (Scope, Plot, FFT,
   Logic, etc.) are the **Debug Window Manual's** subject. Here we mention they
   exist and cross-reference that manual — we do not teach them.
6. **Show, then formalize.** Prefer a tiny worked example, then the rule —
   especially for the "first session" material.

## Things to actively strip from the source docs

- PNut-IDE menu workflows, `pnut.exe -bd/-cd`, "enable debug mode in PNut".
- P1 idioms (`cognew`, `CNT`).
- Bare `DEC/HEX/BIN` DEBUG formatters.
- Superlatives / marketing voice.
- Deep SCOPE/display tutorials (→ cross-ref Debug Window Manual).

## Example voice (before → after)

**Source (reference-ish, tool-wrong):**
> The debugger can be enabled through multiple methods in the PNut IDE. Run →
> Debug Enable (Ctrl+D) enables debug mode.

**This manual (teaching, correct):**
> Before the debugger can help you, your program has to be compiled *with
> debugging turned on*. With the `pnut_ts` compiler you do that with the `-d`
> flag:
>
> ```
> pnut_ts -d myprogram.spin2
> ```
>
> Then you run it from `pnut_term_ts`, the host program that opens the debugger
> window. The first time a `DEBUG` statement (or a PASM `DEBUG` instruction) is
> reached, execution pauses and the single-step debugger appears — your program
> is now waiting for you.
