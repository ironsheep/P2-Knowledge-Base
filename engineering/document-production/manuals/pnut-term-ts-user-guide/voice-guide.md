# Voice Guide — PNut-Term-TS User Guide

**Status:** DRAFT for review (Phase 1)
**Created:** 2026-07-21
**Adapted from:** the P2 Single-Step Debugger Manual voice guide (its closest
sibling — same host application, same "operate this desktop tool" register).

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
  exit codes. No hedging, no marketing ("powerful", "revolutionary",
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
   debug baud is **`pnut_ts`**. There is no "PNut IDE" and no `pnut.exe`. The
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
