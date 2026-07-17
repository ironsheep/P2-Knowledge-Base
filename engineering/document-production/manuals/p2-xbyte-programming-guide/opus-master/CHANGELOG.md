# P2 XBYTE Programming Guide - Changelog

## v0.4.0 (2026-07-17) — the community-thread pass (in development)

A Parallax forum thread — **"basic XBYTE questions"** (`discussion/176253`) — and
its attached minimal VM were tested against the guide, question by question. The
guide already answered the things its reader was stuck on: where the dispatch
table lives, how to load it, how to arm the engine, and why handlers cannot run
from hub. Three additions close what it did *not* cover. None is a correction;
all are additive, and each traces to the Silicon Doc or the `SETLUTS` definition —
not to the community code, which serves only as a corroborating example.

- **§6.1 — the 256-entry ceiling and the *own*-cog LUT (enhancement).** A new
  HARDWARE note answers a misconception the thread surfaced (trying to "double" the
  table across two cogs' LUTs to fit a large opcode set): a bytecode is one byte,
  so it indexes at most **256** entries, read from the running cog's own LUT.
  `SETLUTS` mirrors a companion cog's LUT *writes* and does **not** merge address
  spaces. For more than 256 distinct opcodes the tool is a prefix + one-shot
  `SETQ2` **alternate table** (§8.3, Chapter 17), not more LUT; compression (§9.3)
  is the complement for *shared* handlers.
- **§8.1 + §10.4 + Appendix D — the arming `$1FF` is never popped
  (completeness).** §8.1 now states the mechanism the Silicon Doc gives verbatim —
  the triggering return *"does not pop the stack,"* which is why a single
  `PUSH #$1FF` serves every dispatch. §10.4 adds the consequence the guide's
  run-once examples never hit: a **reusable** interpreter cog that re-arms must
  `POP` that stale `$1FF` on exit, or the eight-level hardware stack drifts one
  entry per job and eventually wraps with no fault. New Appendix D row for the
  symptom.
- **§12.4 + Appendix C.8 — the dedicated interpreter cog (enhancement).** A new
  §12.4 names the structural step every real interpreter takes right after the
  minimal VM works — give the engine its own cog, launched by `COGINIT` with the
  table already in its LUT and fed by a hub mailbox — and a new Appendix C entry
  cites the thread's community example (refaQtor's *essential XBYTE*) as a compact,
  real instance of that shape, and of the §10.4 `POP`.
- **Clarity — obscure idioms replaced with plain wording.** This guide serves human
  readers *and* AI code-generation agents, so culturally-specific idioms whose literal
  words mislead were swapped for plain terms (the deliberate, clear metaphor voice —
  ladder/rung, road, tax/ledger — is untouched): *used in anger* → *put to full use*
  (§C.1); *The long tail* → *Edge cases* (§14.9 heading); *the sting* → *the catch*
  (§14.8); *in the flesh* → *made concrete* (§C.8).

## v0.3.0 (2026-07-15) — the reader's-frame edition

Added a front orientation layer so the guide opens on *why* and *what*, not mechanism. A reader
was gathering detail from the front with no frame; now two XBYTE-free chapters precede everything
and you meet the engine already knowing what you are pointing it at. Structural, not a patch:
a new **Part I** was inserted, so former Chapters 1–18 are now **3–20** and former Parts I–V are
now **II–VI** (all cross-references and anchors renumbered to match).

- **§8.2 · §9.2 · §9.5 · Appendix A — mode-operand bit 1 corrected (correctness).** The guide
  formerly called bit 1 an "undocumented `x` bit" and floated a "stack-pop control" reading from the
  demo's *no stack pop* comment. That was wrong. Reading the *full* Silicon Doc mode table (all ten
  forms, not just the two 256-entry patterns) shows **bit 1 is the index-form selector**: `0` indexes
  the dispatch table from the bytecode's low bits, `1` from its high bits — and in the 256-entry mode,
  where the byte fills all eight index bits, bit 1 is simply **ignored**. Confirmed by Chip Gracey.
  §9.2's table is now expanded from five rows to the **full ten forms** (primary + alternate per size),
  the false "stack-pop" speculation is removed, and the leave-it-0 default is re-explained (it selects
  the low-bits form). Resolves **F-223**; retires Chip question Q7.
- **Part I — The Landscape (NEW, XBYTE-free).** Two chapters that build the concepts, then name them:
  - **Chapter 1 — Why Emulate on the P2.** The draw, in three parts — the P2's *facility* for
    writing interpreters (hardware built for the interpreter's inner loop, the largest draw); a
    whole machine on one chip (the guest CPU plus its video/sound/IO on-chip, with speed a *bonus*
    for low-end guests that erodes as instruction complexity rises — not the primary sell); and
    several emulators running at once on independent cogs. Then the full range of emulation with
    this guide's slice marked (instruction-at-a-time, behavior not timing), each other approach
    given a one-line reason it is out of scope; and two reading on-ramps, for the experienced and
    the new. Host/guest are introduced on first use in §1.1, not deferred to the naming block.
  - **Chapter 2 — What This Kind of Emulation Asks of You.** The cross-cutting concerns seeded in
    plain language — where the guest lives and comes from, state-not-timing, multi-step
    instructions, guest interrupts, the no-loop-body trade, and the shared-memory budget — each
    carried forward as a question about *your* guest. Closes with the vocabulary the rest of the
    book speaks (host/guest, emulator/interpreter, behavior- vs cycle-accurate, object code) as a
    page to turn back to.
- **Part title aligned** — the building Part is now **Building Interpreters and Emulators** in the
  body, matching the cover organization (the body heading said "Building a VM"). Spelled "and"
  rather than "&": the Part-heading filter emits the title into a raw LaTeX command unescaped, so
  an ampersand there becomes a live alignment tab (chapter titles escape fine via pandoc's path).
- **Front-matter** — the Guide Organization panel and the How-to-Use map rebuilt for the
  six-Part / twenty-chapter structure.
- **§16.3 + §14.7 — guest interrupt *acceptance timing* (correctness).** The guest architecture
  decides *when* an interrupt is accepted, not just whether: Z80/8080 `EI` enable-delay, prefix /
  atomic sequences that block acceptance, and interruptible-and-resumable instructions (`LDIR`,
  `REP MOVS`). §16.3's "consistent state" rule alone accepts one instruction too early after `EI`;
  now framed as a faithfulness dial, like decimal mode and cycle accuracy.
- **§14.9 — self-modifying code, the FIFO-flush escape hatch.** You can keep auto-fetch and honour
  a rewrite by re-priming the FIFO with `RDFAST` (it re-initialises, discarding stale prefetch), at
  a per-fetch refill cost that collapses toward rung 2 — a real technique, almost never the trade.
- **§4.6 — "Designing skip patterns" (NEW).** A consolidated process — find the family → superset
  body → factor shared work into `CALL`s → assign patterns common-path-first → the F bit when a
  pattern can't express it — plus the two traps (a `##` is two longs; a pattern must fit the 22-bit
  window). Pulls together guidance that was scattered across §4.4/§4.5, §6.2, and §9.4.
- **Layout.** Platform section keep-together reserve `\needspace 7→3 baselineskip` — whole long
  sections no longer migrate off a Part-opener page and ~6 pages of trailing whitespace are
  recovered (fleet-wide platform change; titlesec `\@afterheading` still prevents orphaned heads).
  Front-matter running header no longer bleeds "Copyright and License" onto the how-to-use /
  conventions pages (blanked with `\markboth`, restored when the body's first chapter sets its mark).

- **§13.3 — the memory system, up close.** The deep payoffs the front layer forward-references,
  now hardware-verified against the KB and landed: where the guest and its assets load from (the
  Edge module's 16 MB flash and on-module microSD share pins P58–P61 — *load-then-run*, never
  fetched at instruction speed); why a large guest is held **whole in PSRAM** (P2-EC32MB, 32 MB
  linear) rather than paged from storage; and the **PSRAM bandwidth budget** — one 16-bit bus
  (~300 MB/s, 8 µs refresh) shared between the emulator's memory traffic and the display's
  framebuffer, arbitrated by the per-cog priority in the MegaYume PSRAM driver. Capacity is ample;
  bandwidth is the constraint.

## v0.2.0 (2026-07-14) — the evidence-grounded edition (in development)

Reworked from the ground up after studying **nine live, working P2 emulators** (Chip Gracey's
own Spin2 interpreter; the 8080 arcade emulators; the Yume console suite for 68000/Z80/65816;
two Intel 8086 implementations incl. a hub-vs-PSRAM pair; Zog/ZPU; a RISC-V JIT; and Parallax's
official `xbyte.spin2`). The study found the old Part III's central framing was **derived, not
observed, and wrong** — it graded guests on instruction shape, when the deciding factors are
where the guest's code lives, whether LUT is free, and how much per-instruction work the guest
needs. Every technique added below is carried anonymously into the body and credited to its
project in Appendix C; the full mining ledger is `TECHNIQUE-MINING.md`.

**Grew from 15 chapters / ~12k words to 18 chapters / ~24k words. Every code block now compiles
(`pnut-ts`).**

- **Chapter 11 — The Three Decisions (rewrite of "Mapping CPU Families").** The honest model:
  *fetch · dispatch · memory* are separable, dispatch is a **ladder** (jump table → `EXECF` →
  XBYTE) you may stop anywhere on, auto-fetch is a **coupling decision** (it welds the guest's
  code to hub), and XBYTE's loop is hardware so **there is no loop body** for cross-cutting work.
- **Chapter 12 — What Will Hurt (NEW).** The per-processor survey: two tables (can you take the
  engine · what will hurt anyway) across ten guests, with a diamond marking rows grounded in a
  real implementation, then a subsection per concern (prefixes, flags, decimal, interrupts,
  cycle accuracy, the long tail).
- **Chapter 9 — Debugging XBYTE (NEW).** `GETBRK` state, the debugger's strikethrough view, and
  the de-arm-and-substitute software-loop trace for guest-level debugging.
- **Chapter 14 — Servicing Guest Interrupts (NEW).** Guest IE as a cog register, `JATN` polling,
  the *where-to-poll* design decision, and interrupt injection via a synthesized `EXECF` operand.
- **Chapter 15 — Prefixes and Alternate Tables (widened from the 6809 vignette).** The
  **map-vs-modifier** prefix taxonomy (only map prefixes want `SETQ2`), and `SETQ2` as a general
  two-stage grammar, not just a prefix trick.
- **Correctness & mechanism fixes** — §5.4 the `REP` interrupt fence (a real hazard the old §5.3
  sold as a pure benefit); §2.5 skip-suspension-inside-CALL, the trailing-pattern trap, and the
  free bit-10 flag; §6 the `PUSH #$1FF` rule, the undocumented `x` bit stated honestly, and the
  `SETQ2` double-meaning; §8.3 resuming the stream from `PB`; §13.4 two-stage addressing-mode
  dispatch; §16.7 the three disqualifiers and the JIT option.
- **Two complete, compiled examples** — the minimal VM (Ch. 10) and a display-list engine
  (Ch. 16), byte-identical to their manual code blocks, under `examples/`. The manual's first
  compiled code, ever — the compile pass found that even Chapter 2's foundational SKIP examples
  never assembled.

Routed to the corrections register from this work: **F-217** (§5.3 hazard, fixed), **F-219**
(x86 prefix taxonomy), **F-220–223** (`xbyte_engine.yaml` broken examples, fixed), **F-224**
(Assembly Manual CORDIC/REP cross-reference). The `x`-bit meaning is an open question queued for
Chip Gracey.

## v0.1.0 (2026-06-26)

First draft — initial review build. Stands up the manual on the shared `p2kb-platform-*`
stack, modeled on the P2 Streamer Programming Guide (layout, two-register voice, richness).
Authored ground-up and grounded in the Silicon Doc v35 XBYTE section + the KB YAML
(`xbyte_engine.yaml` and the skip/FIFO/SETQ instruction set). NOT yet released.

- **Part I — XBYTE Fundamentals** — Understanding XBYTE (the bytecode VM inner loop in
  hardware); the skip family (SKIP / SKIPF / EXECF) taught first as the foundation XBYTE is
  built from; the FIFO bytecode stream (RDFAST + RFBYTE/RFWORD/RFLONG/RFVAR/RFVARS, GETPTR);
  LUT dispatch (the 256-entry table, each entry an EXECF operand).
- **Part II — The XBYTE Engine** — the 8-clock dispatch cycle walked clock-by-clock and the
  6-clock overhead; arming with SETQ / SETQ2 (persistent vs one-shot) and the `$1FF` stack
  convention; the table-size & compression modes (256/128/64/32/16, `%ABBBB`) and the F bit;
  bytecode-routine constraints and shared-handler skip patterns.
- **Part III — Building a VM** — a minimal custom VM (the auto-XBYTE loop from scratch); how
  guest CPU instruction shapes map onto XBYTE; a tiny illustrative 6502 emulator (capstone);
  the 6809 SETQ2 alternate-table vignette.
- **Part IV — Reference** — the instruction reference and the configuration-constants /
  mode-operand reference.
- **Appendices** — A: XBYTE Quick Reference · B: Encoding Summary · C: Further Implementations
  (community projects, external links only) · D: Troubleshooting · clickable Index.
- **Figures** — four TikZ diagrams on the shared platform diagram stack: the dispatch loop
  (Fig 1.1), the LUT dispatch-table entry bit-field (Fig 4.1), the 8-clock dispatch cycle
  (Fig 5.1), and the mode-operand layout (Fig 7.1), with a List of Figures.

Known first-draft limits (for the review): the example-library ZIP is not yet built; the
capstone 6502 and the 6809 vignette are deliberately tiny & illustrative, not faithful
emulators.
