# Voice Guide — PNut-Term-TS User Guide

**Status:** DRAFT for review (Phase 1)
**Created:** 2026-07-21
**Adapted from:** the P2 Single-Step Debugger Manual voice guide (its closest
sibling — same host application, same "operate this desktop tool" register).
**Updated:** 2026-08-11 — re-derived from that sibling after it adopted the shared
narrative discipline (§"The shared narrative discipline"). This guide was seeded on
2026-07-21 from a copy of the sibling that pre-dated the XBYTE guide review (Chip
Gracey, 2026-07-20), so it inherited a pre-discipline guide. Canonical statement:
`engineering/standards/documentation-standards/documentation-voices-catalog.md`.

This guide defines the voice for the **PNut-Term-TS User Guide**. It is a
*teaching user guide for a software tool* — not a terse reference, not a
whimsical tutorial. The subject is the **application itself**: how to run it,
what its controls do, and how to drive it interactively and headless.

---

## Who the reader is

- **Has a Propeller 2 and wants to see what their program is doing.** They know
  the P2 emits `debug()` output; they want the terminal that receives and
  displays it.
- **May have never run PNut-Term-TS.** We cannot assume they know what a
  PropPlug is, what "download to RAM vs flash" means for them, or how the reset
  control line (DTR/RTS) works. Introduce each before relying on it.
- **Two closely-related readers share this guide:** the developer at the GUI,
  and the automation author (CI pipeline, container, or AI coding assistant)
  driving the tool **headless**. Both are first-class; call out which mode a
  feature belongs to.
- **Wants to accomplish something**, not admire the tool: "I flashed my program
  — how do I watch its output?" / "How do I capture a run in CI and know it
  finished?"

**Design consequence:** introduce every concept before we use it, and motivate
*why* before *how*. The reader should never meet a term (PropPlug, `.p2rec`,
end-session marker, control line) cold.

## What we are teaching (the actual goal)

How to **operate PNut-Term-TS** to run, watch, capture, and automate a P2
program's `debug()` session:

- what the tool **is** and how it fits between a compiled binary and the P2,
- the **operating modes** — interactive GUI, command-line download, headed
  batch (auto-exit), IDE integration, and headless — and when to reach for each,
- the concrete **controls** — toolbar, menus, settings hierarchy, PropPlug /
  device management, recording & playback, the performance monitor,
- the **command line** — every option, the exit codes, and the "you should not
  need to set baud" behavior,
- how **logging** works and is *consumed* differently headed vs headless (the
  program-output-stays-clean principle, the USB traffic log, version banners),
- and **troubleshooting** the common failure modes (not detected, garbled text,
  no reset, blank window).

## Tone

- **Mentor at your shoulder.** Calm, plain, second person ("you"). "Plug in your
  PropPlug, then let's download the program and watch it run" — guided, not
  lectured.
- **Confident and concrete.** Real flags, real menu paths, real defaults, real
  exit codes. No *vague* hedging — calibrated qualifiers are required where the
  evidence is partial (see the calibrated-confidence rule below). No marketing
  ("powerful", "revolutionary",
  "seamless" — cut these).
- **Respectful of the reader's time.** Short sentences. One idea per paragraph.
  Tables for option/menu/setting reference; prose for concepts and workflows.

## Rules (the discipline that keeps this guide trustworthy)

1. **Introduce-before-use.** First mention of PropPlug / control line (DTR/RTS) /
   `.p2rec` / end-session marker / headless gets a one-line plain-language
   definition. No forward references to undefined terms.
2. **The source is the authority — match the shipping tool, not our memory.**
   The behavior of record is the **PNut-Term-TS repository** (the two feed
   documents, current as of **v0.10.3**). When the tool changes, re-pull and
   re-verify — do not describe behavior from recollection. If a feed and the
   live repo disagree, the repo wins.
3. **Names, exactly.** The application is **PNut-Term-TS** (the invocation is
   `pnut-term-ts`). The compiler that produces the `.bin` and bakes in the
   debug baud is **`pnut-ts`** (product: **PNut-TS**). **Both names are
   hyphenated** — the underscore forms `pnut_ts` / `pnut_term_ts` are wrong and
   do not exist as executables; every feed uses the hyphenated form, and the
   compiler's own usage banner reads `PNut-TS: Usage: pnut-ts [optons] filename`
   (verified 2026-08-11). There is no "PNut IDE" and no `pnut.exe`. The
   debug **display windows** (TERM, SCOPE, PLOT, LOGIC, …) open automatically
   from the P2's `debug()` directives — never from a menu.
4. **As-built, not aspirational.** Document only behavior the tool actually has.
   The logging feed contains an explicitly **aspirational, unimplemented**
   filename scheme — use the *canonical as-built* filenames
   (`debug_YYMMDD-HHMMSS.log`, `headless_…`, `usb-traffic_…`), never the
   proposed `{Prefix}_{Ctx}_{YYYYMMDD}_{HHMMSS}` pattern.
5. **Stay in our lane.** The `debug()` **directive syntax** for each window type
   is the Parallax P2 DEBUG specification and is documented elsewhere; the
   single-step debugger has its **own** manual. Here we say those exist and
   cross-reference them — we do not reproduce the directive reference or teach
   the debugger.
6. **Both modes, always in view.** When a capability differs headed vs headless
   (logging direction, TX path, auto-exit, reset), state the difference plainly
   rather than describing only the GUI and leaving automation readers guessing.
7. **Platform differences are real — name them.** macOS native menu vs
   Windows/Linux in-window menu bar; `Cmd` vs `Ctrl`; `/dev/tty.usbserial-*` vs
   `/dev/ttyUSB*` vs COM ports; the `dialout` group on Linux. Don't flatten
   these into one imagined platform.

## The shared narrative discipline

A "mentor at your shoulder" register is warm and second-person, which is exactly
the register that drifts most easily into a *recognizably-AI* voice — over-confident,
self-admiring, and closing nearly every section on a rhetorical beat. A guide to a
desktop tool is especially exposed: feature walkthroughs invite a little flourish at
the end of each one, and forty of those in a row is a metronome.

Three guards. The canonical statement is the voices catalog's
§"The Shared Discipline"; this is its tool-guide adaptation.

### Never do these (they read as AI, not as a mentor)

| Avoid | Why | Instead |
|-------|-----|---------|
| "the obvious way to set the baud is wrong" · "you probably expect the window to clear" · "read that flag again" | **Reader-as-foil** (the *besserwisser* register) — telling the reader what they think, then correcting them | State what the tool does; let the reader compare it to their own expectation |
| "this is the most elegant part of the tool" · "the recording system is pure genius" · "no other terminal comes close" | **Self-admiration** — the text praising its subject or its own explanation (a cousin of the marketing voice already banned under **Tone**) | Say what the feature *does*; the reader can be impressed on their own |
| "and here's the catch" · "hold that exit code in mind" · "but there's a surprise when you go headless" | **Staged reveal** — withholding a fact to manufacture a beat | Deliver the fact where it belongs — in the mode, option, or step it applies to |

### Calibrated confidence is required — it is not hedging

Banning hedging on facts does **not** mean banning *uncertainty*. A qualifier that
reflects the true state of the evidence — "usually", "on most hosts", "in practice" —
is **accuracy**, and is required wherever the bare claim would overstate. The test is
one line: **never state a claim above its evidence.**

This guide has two concrete, recurring instances:

- **Platform.** Rule 7 says platform differences are real. Where we have verified a
  behavior on one platform and expect it on another, say so at that confidence
  rather than writing one imagined platform's behavior as universal.
- **Version.** Rule 2 pins the behavior of record to a stated PNut-Term-TS version.
  A claim is true *as of that version*; where behavior is known to be in motion,
  the sentence carries that, and where it is settled it does not need a qualifier
  at all. Do not sprinkle version hedges on stable behavior — that is hedging.

The "it just works" register that suits this tool is a real risk here: it is a fine
sentence when the tool genuinely does the work (reading the debug baud out of the
image), and an overstatement the moment there is a failure mode the reader will hit.
Strip the flourish off any section- or callout-closing sentence and read what remains
as a bare claim — satisfy it or cut it. Two source-free tests: does the guide already
say the opposite elsewhere (a troubleshooting entry for the very thing just declared
automatic)? does the sentence lean on *never / always / every / only / nothing /
impossible / free / the single most*?

### Cadence is budgeted

A *beat* is a closing sentence that lands a rhetorical punch rather than finishing
the explanation — a verdict, a reversal, a directive, an aphorism that restates with
force. One good beat is good writing. The failure is **regularity**: when nearly
every section ends on one, the reader stops hearing the beat and starts hearing the
*metronome* — "instantly recognizable and becoming rapidly fatiguing."

**Decision: ADOPT R4 as written** — the budget, the run limit, the chapter-closer
emphasis, the declared-refrain carve-out, and the protection for earned beats all apply
to this document unchanged. The numbers themselves are stated once, in the house canon
(`engineering/standards/documentation-standards/documentation-voices-catalog.md`, R4);
they are not copied here, because a copied number is one that drifts from the rule it
came from while still reading as authoritative.

The tool-guide version of the trap: option tables, menu walkthroughs, and
troubleshooting entries are *lists of similar things*, and closing each one on a
verdict is the fastest way to build a metronome. Let a reference entry end when the
information ends.

Detection: `document-audit` Dimension #4c (payoff-sentence sweep, with a
longest-consecutive-run measure).

## Things to actively strip from the source material

- Any "PNut IDE" / `pnut.exe` framing; menu workflows that don't exist.
- The aspirational log-filename scheme (rule 4).
- Superlatives / marketing voice.
- Deep `debug()` directive tutorials (→ cross-ref the DEBUG documentation and
  the Debug Window Manual) and single-step debugger operation (→ cross-ref the
  Single-Step Debugger Manual).
- Internal transport diagnostics (`[CTRL]`/`[DEBUGGER]` framing) — these are
  ours, compile-gated out of releases, and meaningless to a reader; mention them
  only insofar as the *principle* (program output stays clean) helps the reader.

## Example voice (before → after)

**Source (feature-listy, tool-detail-first):**
> The application supports downloading to RAM or FLASH via the -r and -f flags,
> which are mutually exclusive. It reads the debug baud rate from the binary.

**This guide (teaching, reader-first):**
> To watch your program run, you give PNut-Term-TS the compiled `.bin` and tell
> it where to put it on the P2 — into RAM for a quick edit-run cycle, or into
> flash to make it stick across power cycles:
>
> ```bash
> pnut-term-ts -r myprogram.bin      # download to RAM and run
> pnut-term-ts -f myprogram.bin      # download to FLASH and run
> ```
>
> You don't set the baud rate. When you download a binary, PNut-Term-TS reads
> the debug baud out of the image your compiler wrote, and listens at exactly
> that rate. It just works.
