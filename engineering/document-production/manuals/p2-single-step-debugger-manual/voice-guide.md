# Voice Guide — P2 Single-Step Debugger Manual

**Status:** DRAFT for review (Phase 1)
**Created:** 2026-05-31
**Updated:** 2026-08-11 — adopted the shared narrative discipline (§"The shared
narrative discipline"), platform-wide since the XBYTE guide review (Chip Gracey,
2026-07-20); canonical statement in
`engineering/standards/documentation-standards/documentation-voices-catalog.md`.

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
3. **Correct tooling, always — and the names are hyphenated.** The compiler is
   **`pnut-ts`** (`-d` / `--debug` compiles with DEBUG enabled); as a product it is
   **PNut-TS**. The host program that shows the debugger and the DEBUG display
   windows is **`pnut-term-ts`** (product: **PNut-Term-TS**). The underscore forms
   `pnut_ts` / `pnut_term_ts` are **wrong and do not exist** — no such executable
   is installed, and every REF/feed source uses the hyphenated form. (`pnut_ts`
   shipped in this manual through v1.0 prep; a reader who typed it got
   "command not found." Verified 2026-08-11 against the binary's own usage banner:
   `PNut-TS: Usage: pnut-ts [optons] filename`.) There is no "PNut IDE", no
   `Run → Debug Enable` menu, no `pnut.exe`. Any such reference from the source
   docs is removed.
4. **Valid DEBUG formatters only.** `UDEC/SDEC/UHEX/SHEX/UBIN` (each with an
   optional trailing `_` to suppress the auto label). Never bare `DEC/HEX/BIN`
   (not valid Spin2 DEBUG output formatters). Every code example must be
   compilable by `pnut-ts`.
5. **Stay in our lane.** The nine DEBUG **display windows** (Scope, Plot, FFT,
   Logic, etc.) are the **Debug Window Manual's** subject. Here we mention they
   exist and cross-reference that manual — we do not teach them.
6. **Show, then formalize.** Prefer a tiny worked example, then the rule —
   especially for the "first session" material.

## The shared narrative discipline

A "mentor at your shoulder" register is warm and second-person, which is exactly
the register that drifts most easily into a *recognizably-AI* voice — over-confident,
self-admiring, and closing nearly every section on a rhetorical beat. A mentor
explaining a debugger is especially exposed: the subject is full of small reveals
("watch what the flags do now"), and each one invites a staged build-up.

Three guards. The canonical statement is the voices catalog's
§"The Shared Discipline"; this is its debugger-manual adaptation.

### Never do these (they read as AI, not as a mentor)

| Avoid | Why | Instead |
|-------|-----|---------|
| "the obvious way to read this panel is wrong" · "you probably expect the PC to advance" · "read that line again" | **Reader-as-foil** (the *besserwisser* register) — telling the reader what they think, then correcting them. A mentor at your shoulder never does this. | State what the panel shows; let the reader compare it to their own expectation |
| "this is the most elegant part of the debugger" · "the watch window is pure genius" · "nothing else on the P2 comes close" | **Self-admiration** — the text praising its subject or its own explanation | Say what the feature *does*; the reader can be impressed on their own |
| "and here's the catch" · "hold that address in mind" · "but there's a surprise waiting at the next step" | **Staged reveal** — withholding a fact to manufacture a beat | Deliver the fact where it belongs, unstaged, at the step it applies to |

These sit alongside the marketing superlatives already banned under **Tone** —
same defect family, different surface.

### Calibrated confidence is required — it is not hedging

Banning hedging on facts does **not** mean banning *uncertainty*. A qualifier
that reflects the true state of the evidence — "usually", "on most hosts", "in
practice" — is **accuracy**, and is required wherever the bare claim would
overstate. The test is one line: **never state a claim above its evidence.**

This manual has a concrete, recurring instance of it. We document **PNut's
intent**, and we certify against **PNut-Term-TS** (see Rule 3 and Chapter 1). Where
a behavior is certified on one host and merely expected on another, say so at that
confidence — do not flatten it into a bare universal. Keystroke and panel claims
trace to the certification source; where they do not, they get the qualifier that
matches what we actually verified.

The warm-voice trap: a closing crescendo *demands* a punchy payoff, and where no
true one exists an invented claim fills the slot. At write time, strip the flourish
off any section- or callout-closing sentence and read what remains as a bare claim —
satisfy it or cut it. Two source-free tests: does the manual already say the
opposite elsewhere? does the sentence lean on *never / always / every / only /
nothing / impossible / free / the single most*?

### Cadence is budgeted

A *beat* is a closing sentence that lands a rhetorical punch rather than finishing
the explanation — a verdict, a reversal, a directive, an aphorism that restates
with force. One good beat is good writing. The failure is **regularity**: when
nearly every section ends on one, the reader stops hearing the beat and starts
hearing the *metronome* — "instantly recognizable and becoming rapidly fatiguing."

- **At most ~half of section closings may be beats.** Cut the weakest back to a
  plain informational close.
- **No long runs** — never more than ~4 sections in a row closing on a beat. A
  stretch of flat closes is rest, not a defect.
- **Chapter closers are the worst offenders** — stay well below a beat on every
  chapter exit.
- **A declared refrain is structure, not a beat** — keep an announced structural
  device.
- **Protect the earned ones.** A beat that carries real information or *lowers*
  the text's confidence survives. Do not flatten the manual to hit a number.

The step-by-step chapters have their own version of this: a procedure that ends
every numbered walkthrough with "and now you can see exactly what your program
did" is the metronome wearing a lab coat. Let a walkthrough end on its last step.

Detection: `document-audit` Dimension #4c (payoff-sentence sweep, with a
longest-consecutive-run measure).

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
> debugging turned on*. With the `pnut-ts` compiler you do that with the `-d`
> flag:
>
> ```
> pnut-ts -d myprogram.spin2
> ```
>
> Then you run it from `pnut-term-ts`, the host program that opens the debugger
> window. The first time a `DEBUG` statement (or a PASM `DEBUG` instruction) is
> reached, execution pauses and the single-step debugger appears — your program
> is now waiting for you.
