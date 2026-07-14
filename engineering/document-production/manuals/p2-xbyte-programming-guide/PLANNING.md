# P2 XBYTE Programming Guide — Seed / Planning Document

> **This is the seed document for a NEW manual.** It captures our present
> shared understanding from the design conversation that originated this
> manual, so nothing is lost before the full folder triad is stood up. It
> becomes the manual's standing `PLANNING.md`. Status markers throughout:
> **LOCKED** (decided), **OPEN** (still to decide), **TO-VERIFY** (claim to
> source before it goes in print).

- **Slug:** `p2-xbyte-programming-guide` (matches the Streamer guide pattern)
- **Provisional title:** *P2 XBYTE Programming Guide* — subtitle TBD, around
  *Building Interpreters and Emulators on the Propeller 2*
- **Status:** In progress (roster: `## In progress`, type=manual)
- **Originated:** 2026-06-26
- **Modeled on:** the **P2 Streamer Programming Guide** — its *layout,
  richness, and voice* are the target. Same `concepts → practical use →
  example` spine. Born on the shared `p2kb-platform-*` stack.

---

## 0. SCOPE REVISION — v0.1.0 first-draft build (2026-06-26, decided with Stephen)

The full stand-up began on 2026-06-26. Stephen narrowed the v0.1.0 scope from the
original three-act design captured below. **This section governs; the later sections
are the fuller design vision, retained for a future edition but partly DEFERRED.**

- **Capstone micro = 6502 (RESOLVED).** Closes §5/§9 open decision #1. 6809 stays as a
  one-chapter **SETQ2 vignette** (alternate-table prefix-page dispatch), per §5.
- **External P2 projects → Appendix C, links only (CHANGED).** The Arc8de 8-console
  arcade and the Yume emulator suite (§8) are NOT the cold-open and do NOT appear in the
  narrative in this edition. They become **Appendix C "Further Implementations"**: each a
  link + author + what-it-emulates + license. (All the §8 verification work still stands;
  it just routes to the appendix.)
- **Cold-open reframed → concept, not project (CHANGED).** Chapter 1 opens on the *idea*
  (every interpreter runs the same fetch→dispatch→run loop; XBYTE does it in hardware for
  ~6 clocks), with a forward-pointer to Appendix C for "see it in the wild."
- **"Systems similar to the P2" → DEFERRED out of v0.1.0 (CHANGED).** The IBM Series/1
  **EDL anchor (§6)** and the **kindred-architecture vignettes (§7)** — Transputer/Occam,
  XMOS xCORE, GreenArrays, Cell SPE — and the S/360 channels-as-P2-I/O parallel (§4/§5)
  are **cut from this edition**. They remain documented below as the design vision for a
  later edition; do NOT reintroduce them without Stephen.
- **§4 architectural-families contrast → KEPT but trimmed.** "How guest-CPU instruction
  shapes map onto XBYTE" is core pedagogy (Ch. 10); it stays. The P2-kinship framing and
  the mainframe-channel parallel are removed from it (those are the "similar to P2"
  material above).
- **NEW Ch. 13 "XBYTE Beyond Interpreters" → ADDED (2026-07-04, Stephen approved).**
  Widens the manual off interpreters/CPUs: a graded application map (the "whistle-wetting"
  breadth table) + three tiny illustrative sketches (terminal/ANSI escape · MIDI status
  dispatch · graphics display list) + a §13.6 promotion of one-shot `SETQ2` from
  emulator-trick to general mode-switch (grounded in the Spin2 interpreter's own
  variable-operator use). Does NOT reintroduce the deferred "similar systems" material —
  this is XBYTE *applications*, not architecture contrast. Instruction Reference + Config
  chapters renumbered 13/14 → 14/15. Code sketches compile-clean (pnut-ts) and within K=76.

Resulting v0.1.0 shape: **15** chapters in 4 parts + Appendices A–D + Index — see
`creation-guide.md` §2 for the authored structure of record.

---

## 0-bis. SCOPE REVISION — **v0.2.0, the evidence-grounded edition** (2026-07-14) — *PROPOSED, awaiting Stephen*

> **This section governs v0.2.0 and supersedes §4 below** (the architectural-families
> contrast), which was written from reasoning and has now **failed verification three times**.
> **Evidence:** `TECHNIQUE-MINING.md` — nine implementations, five-plus authors, all read.

### Why this revision exists

Stephen asked for a per-processor **"what will hurt when you emulate this"** table, and proposed
grounding it in **live working emulators** rather than ISA reasoning. That study found the guide's
Part III framing is **confidently wrong**, and produced far more than a table.

**Root cause, stated plainly:** Chapter 10 was **derived, not observed**. Three of its claims failed
against real code (the x86 prefix claim → **F-219**; the 68000 `RFWORD` claim; and the 65816 —
graded "the sweet spot" — which is emulated on P2 **without XBYTE at all**).

### The four ideas that reshape the manual

1. **Three separable concerns, not two assets.** §10.1 teaches *auto-fetch* + *table dispatch*. The
   honest model is **fetch** · **dispatch** · **memory model**. Proven by the `i8086_xt` hub-vs-PSRAM
   pair: swapping the entire memory backend changed **115 of 8,314 lines and ZERO dispatch lines**.
2. **Auto-fetch is a coupling decision, not a feature.** The FIFO streams **hub only**. Taking
   auto-fetch **welds the guest's code to hub RAM**; hand-rolling the fetch costs clocks and buys a
   **swappable memory backend**. If the guest may outgrow hub, you pay for auto-fetch once — in a
   rewrite.
3. **There is no loop body.** XBYTE's loop is *hardware*. Every cross-cutting per-instruction
   concern — cycle pacing, interrupt polling, debug hooks, guest refresh registers, prefix-state
   reset, bus arbitration — **has nowhere to live.** MegaYume's Z80 loop does all six. A software
   loop costs ~3 clocks and gives you **a place to stand**. *This is the real reason the big
   emulators decline XBYTE, and the manual never says it.*
4. **A ladder, not a binary.** Plain jump table → `EXECF` + skip patterns → XBYTE. All three exist
   **on one guest CPU** (the 8086), so the reader can see every rung with the guest held constant.
   **You do not have to climb all the way.**

### Chapter-by-chapter

| Ch | Change | Source |
|----|--------|--------|
| **1** | **ADD** "If you're building…" router (mirrors Streamer §1.7; forward-points to Ch. 13 — §13.2 already *is* this content, buried). **ADD** "What XBYTE costs you": 256 LUT longs, handler space, the `$1FF` stack slot, `PA`/`PB`, **and the FIFO**. **REVISE** §1.5 with the honest cost (idea 3). | T-budget; L4 |
| **2** | **ADD** skipping is **suspended inside a `CALL`** (Silicon Doc — our own Ch. 11 depends on it and never says why it's safe). **ADD** a trailing pattern runs **past** the handler → the NOP landing pad. **ADD** (aside) bit 10 is the pattern's LSB → free per-opcode flag. | D3/T4 · A3/T5 · T18 |
| **4** | **REFRAME** §4.4 "Dispatch, by hand" — not pedagogy: it is the **debug mode** *and* what production emulators actually ship (4 independent sightings). **ADD** `orgf` table placement. | A4/T6 · T11 |
| **5** | ✅ **CONFIRMED** by Parallax's official clock table. **FIX §5.3 (F-217)** — interruptibility is sold as a pure benefit; handlers doing atomic work must shield with **`REP`** (Chip does it 8×). *Correctness hazard.* | J1 · B4 |
| **6** | **ADD** the `SETQ2` collision caution (block-move vs one-shot mode). **RESOLVE J3** — *"no stack pop"* in Parallax's arming line; **verify against the Silicon Doc before writing.** | B6/T12 · J3 |
| **7** | ✅ **CONFIRMED** by Chip's `$1A1`. **ADD** it as a worked reference (compression + F together, in a real bytecode set). | B2/T14 |
| **8** | **ADD** re-point the FIFO from `PB` to resume after a hub call. | A5/T8 |
| **NEW** | **Guest interrupts** — `JATN` poll + guest IE as a cog register + **inject via a synthesized `EXECF` operand**. *Converged: two authors, two guests.* And the placement lesson: with a loop you poll once; under XBYTE you must poll **inside handlers**. | T1/T19 |
| **NEW** | **Debugging XBYTE** — `GETBRK` exposes the 9-bit mode + the live skip pattern; the debugger *displays* both (struck-through instructions); the debug ISR preserves the hardware stack, which is **why** XBYTE survives being debugged; and the **de-arm-and-substitute** technique. Motivated by idea 3. | D1/D2/D4 · A4 |
| **10** | ⚠️ **REWRITE.** Becomes: three concerns (1) → the dispatch ladder (4) → the coupling decision (2) → no loop body (3) → **the concerns table** → prose per concern → why the 6502. | all |
| **11** | Keep **tiny & illustrative** (charter holds). **ADD** a forward pointer to **two-stage dispatch** (opcode → addressing mode → operation) as the real way the addressing-mode matrix is solved — *converged across two authors*. Do not build it. | T15 |
| **12** | **WIDEN.** The **prefix taxonomy** (F-219): **map/escape** prefixes change *which handler runs* → `SETQ2` ✅; **modifier** prefixes change *how it behaves* → state register ❌. Z80 has **both** (`CB`/`ED` map; `DD`/`FD` modifier) — the perfect illustration. **ADD** Chip's `SETQ2`-as-**grammar** and two live tables at different LUT bases. | K3/F-219 · B3/T9/T10 |
| **13** | **§13.7 "When XBYTE is the wrong tool" gets the real content** (idea 3 + hub-only fetch + LUT/FIFO contention). **ADD** JIT as an option we never name. | E2 · T16 |
| **App C** | Credit every mined project (existence proofs a reader can study). | all |
| **App D** | **ADD** the new traps: landing pad · `REP` shield · `SETQ2` collision. | A3 · B4 · B6 |

### The concerns table (Stephen's original ask — now evidence-driven)

Rows: **6502/65C02 · Z80 · 8080 · 6809 · 8051 · 65816 · 68000 · x86 · ARM/MIPS · CHIP-8**
Cells are **short words, not symbols** (Stephen: *"don't make it harder to read"* — and Ch. 13
already uses ★/◑/○ for *fit*, where filled = **good**; reusing them for *concerns*, where filled =
**bad**, is exactly the trap).

Columns, **as the evidence now dictates** — note the first two were **not** in the original design
and they **dominate every real target**:

**Where the code lives** · **Is LUT free** · **Dispatch fit** · **Prefixes** (map / modifier) ·
**Flags** · **Decimal** · **Guest interrupts** · **Cycle accuracy** · **Quirks**

Then one prose subsection **per concern** (not per CPU). Cycle-accuracy and undocumented opcodes stay
prose, not columns — forcing them into the grid is what would wreck it.

### Deliberately NOT claimed

- **The 8086-on-XBYTE claim is an unverified forum lead with no artifact** (thread 173345: 19 posts,
  zero downloadables). It does **not** enter the manual as fact — **and we do not overclaim the
  converse either.** Two x86 implementations decline XBYTE; that is evidence about *those two*, not
  proof that x86 *cannot*.
- **No evolution narrative** from the archive dates (`Simple-i8086` uses `EXECF`; `i8086_xt` does
  not). Authorship/lineage is **not established** — record strategies, not stories.
- **T18** converges across two cores **by the same author.** Present it with its mechanism, not as
  "everyone does this."

### Flagged decisions for Stephen

1. **Scope.** This is a Ch. 10 rewrite + two new chapters + fixes across seven — v0.1.0 → **v0.2.0**,
   not a patch. Confirm.
2. **The concerns table** — inside Ch. 10, or its own chapter? (It is now big enough to stand alone.)
3. **The worked example** (display list, compiled + committed) — still wanted? It also closes a real
   gap: **the manual currently ships ZERO `.spin2` files**, though `creation-guide.md` §5.3 requires
   examples to compile.
4. **J3 blocks Ch. 6** — *"no stack pop"* must be resolved against the Silicon Doc first. Do not guess.

---

## 1. Why this manual exists (LOCKED)

The community wants to understand **XBYTE** — the P2's hardware bytecode-
execution engine — its use, and **how to build interpreters and emulators**
with it. XBYTE is one of the P2's most distinctive and least-documented
capabilities. This manual is the definitive community reference for it.

**Thesis (the spine of the whole document):** XBYTE automates the inner loop
of every bytecode VM (*fetch next bytecode → look up handler → dispatch →
run → repeat*) in hardware, at ~6 clocks of overhead per bytecode. The
manual teaches the whole system, then proves it by re-hosting a real,
interpreted, event-driven language and a real small CPU on the P2.

---

## 2. The technical core (SOURCED — Silicon Doc v35 + P2KB YAML)

Primary sources: **Silicon Doc v35** (`engineering/ingestion/sources/silicon-doc/`,
"XBYTE - Bytecode Execution Engine" section) and P2KB YAML key
**`p2kbArchXbyteEngine`** + the instruction entries. These are authoritative;
cite them when grounding manual content.

**XBYTE mechanism:**
- Hardware bytecode dispatch: ~**6 clocks overhead** per bytecode (vs ~9 for
  software dispatch); minimum XBYTE loop = 8 clocks (Silicon Doc verbatim).
  *(Discipline: the 6-clock figure is a Silicon-Doc hardware fact and is
  citable. Do NOT publish Spin2-method bytecode-interpreter clock timings —
  that's a separate banned class.)*
- **8-clock dispatch cycle** walked clock-by-clock (RFBYTE → MOV PA → RDLUT →
  **EXECF D** → MOV PB,GETPTR/MODCZ → flush → reload → first handler instr).
- Reads the bytecode stream through the **hub FIFO** (`RDFAST` +
  `RFBYTE`/`RFWORD`/`RFLONG`, and especially `RFVAR`/`RFVARS` for variable-
  length operands; `GETPTR`).
- Dispatches through a **256-entry table in LUT RAM**; each LUT entry **is an
  EXECF operand** — `[9:0]` = handler address, `[31:10]` = a 22-bit SKIPF
  pattern.
- **Special registers:** `PA` ($1F6) = current bytecode/operand; `PB` ($1F7)
  = FIFO pointer.
- **Arming:** `_RET_ SETQ {#}D` (persistent mode) or `_RET_ SETQ2 {#}D`
  (one-shot alternate-table mode) with `$1FF` on the hardware stack.
- **Table-size / compression modes:** 256 / 128 / 64 / 32 / 16 bytecodes,
  plus the `%ABBBB` compression scheme; the `F` flag-write bit (write
  bytecode index LSBs to C/Z).

**The key insight — the skip family IS the engine (LOCKED as pedagogy):**
`SKIP` / `SKIPF` / `EXECF` are not adjacent topics, they are what XBYTE is
*built out of*. Teach them FIRST as foundation, then reveal XBYTE as "the
hardware that runs an EXECF dispatch for you, once per bytecode, for free."
- **EXECF** = jump + load skip pattern (XBYTE's LUT entry is an EXECF operand;
  clock 4 of the cycle *is* an EXECF).
- **SKIPF** = fast skip, PC leaps over instructions (COG/LUT) — the idiom for
  one shared handler body serving several related bytecodes via a per-
  bytecode skip pattern.
- **SKIP** = cancel-style sibling (works in hubexec too) — compare/contrast.

**Full instruction/feature cast the manual must cover:** SKIP, SKIPF, EXECF;
SETQ/SETQ2, _RET_, the `$1FF` stack convention; RDFAST + RFBYTE/RFWORD/RFLONG
+ RFVAR/RFVARS, GETPTR; PA/PB; LUT as routine store; the 6 table/compression
modes + F bit; REP as a supporting idiom.

---

## 3. Document shape — three acts, Streamer-style (LOCKED in outline)

1. **Hook + Concepts.** Open on the real **8-console RJ11 system** (§7) as
   proof of XBYTE's payoff. Teach the skip family, the FIFO bytecode stream,
   LUT dispatch, SETQ/SETQ2 modes, the 6-clock cycle.
2. **The architectural map (§4).** How processor *families* fall onto XBYTE's
   features — the contrast/reference chapter. Includes the **EDL anchor (§5)**
   as its conceptual centerpiece and the **kindred-architecture vignettes
   (§6)**.
3. **Practical → capstone (§5 candidate analysis).** Build a small custom VM
   (auto-XBYTE loop), then a **tiny, illustrative** emulation of a small CPU.
   Close with the **verified real-world implementations (§7)**.

**Design principle — TINY & ILLUSTRATIVE (LOCKED).** The capstone emulator is
a *teaching artifact*: enough to show the technique end-to-end and to
compile-check with `pnut-ts`, explicitly **NOT a complete/faithful reference
implementation**. Neither we nor a future contributor should over-build it.

---

## 4. Architectural-families contrast (LOCKED as a chapter; content TO-VERIFY when written)

Organizing insight: XBYTE has two separable assets — **auto-fetch** (pull the
next byte from the FIFO and dispatch, zero software) and the **table/EXECF
dispatch machinery**. Different CPU families use different amounts of each.

| Family | Instruction shape | Auto-fetch fit | Table/EXECF fit | Teaches |
|--------|-------------------|----------------|------------------|---------|
| **8-bit micros** (6502, 8008, 8051, 6809, Z80) | byte stream, opcode-first | ✅ full strength | ✅ ideal | the sweet spot |
| **68000** | 16-bit word opcodes + extension words | ⚠️ partial (dispatch on high byte, then secondary) | ✅ LUT 1st-level | word-opcode CISC |
| **80x86** | variable-length, prefixes + `0F` escape + ModR/M + SIB | ✅ fetch fits | ✅ but decode explodes | SETQ2 prefix-dispatch to its limit |
| **MIPS** | fixed 32-bit words, bit-field decode | ❌ no byte stream (`RFLONG` the word) | ✅ 6-bit opcode → 64-entry table + SETQ2 secondary for R-type funct | fixed RISC: table without auto-fetch |
| **mainframe** (IBM S/360) | variable-length (2/4/6B), **opcode-first, length encoded in opcode high bits** | ✅ clean | ✅ | autonomous I/O channels → P2 I/O (one-paragraph mention, §5) |

Reframes the manual from "a feature + one emulator" into a **map of how every
processor family maps onto XBYTE** — where it shines, where you adapt, where
you reach the limits. This is the reference-grade value.

---

## 5. Capstone CPU candidate analysis

**Reference-implementation principle applies: whichever is chosen, the build
stays tiny & illustrative (a representative subset), not a full emulator.**

| CPU | Opcode | XBYTE auto-stream | Table fill | Size / full-emu | Audience | Special showcase |
|-----|--------|-------------------|-----------|------------------|----------|------------------|
| **8008** | 1B, first | ✅ purest | sparse | **smallest** (~48 ops) | historical (first 8-bit µP) | shared-handler skip patterns (`MOV r,r`) |
| **6502** | 1B, first | ✅ ideal | ~151/256 | medium | high (NES/C64/Apple) | clean baseline, `RFVAR` operands |
| **8051** | 1B, first | ✅ excellent | **~255/256 (full)** | large (memory model) | **highest (embedded)** | full-256 mode + bit/bank skip patterns |
| **6809** | 1B + `$10`/`$11` pages | ✅ excellent | ~200+ | large (postbyte) | high (CoCo/Vectrex/arcade) | **SETQ2** alternate tables (prefix pages) |
| MIX (Knuth) | 1B `C` field, **mid-word** | ⚠️ word-fetch fights it | — | small (64 opcodes) | Knuth pedigree | hand-rolled RDLUT/EXECF dispatch |
| MMIX (Knuth) | 1B, first | ✅ perfect dispatch | 256 | too big (64-bit + FP) | — | perfect table fit, impractical body |
| IBM S/360 | 1B, first, length-in-opcode | ✅ clean | — | large (subset only) | mainframe | channel-as-I/O (see below) |

**CAPSTONE = OPEN.** Down to **8008 / 6502 / 8051**:
- **8008** → smallest, purest XBYTE, definitely finishable; weaker "wow."
- **6502** → balanced: impressive, recognizable, tractable (default if unsure).
- **8051** → best full-256 showcase + most relevant to the P2's embedded
  audience; cost is the multi-address-space memory model (heaviest of the
  three).
- **6809** → kept as a *vignette only* (`$10`/`$11` page dispatch) to
  demonstrate **SETQ2**, regardless of capstone choice.

**Recommended structure:** small custom VM teaches the auto-XBYTE loop → one
8-bit micro as the tiny capstone → 6809 SETQ2 vignette → EDL anchor (§5 below)
as the architecture-chapter centerpiece.

**IBM S/360 — DEMOTED to a one-paragraph mention (LOCKED).** Clean opcode-
first fit with instruction length encoded in the opcode high bits; its
**channel architecture** (CCW channel programs executed autonomously by I/O
channels) prefigured the P2's autonomous I/O (smart pins / streamer / cogs).
Lovely parallel, but it overlaps the Streamer guide's I/O territory and is not
the manual's thesis — so: a mention in §4, not a full vignette. Source:
*IBM System/360 Principles of Operation* (GA22-6821) when written.

---

## 6. The IBM EDL anchor (LOCKED) — architecture-chapter centerpiece

**Decision: ONE IBM anchor, and it is EDL** (not S/360). EDL strictly
dominates S/360 on the "why this manual exists" axis.

**What it is:** the IBM **Series/1** (1976, 16-bit real-time/process-control
mini) ran **EDX** (Event Driven Executive, the OS) and **EDL** (Event Driven
Language, the HLL). EDL's *primitives were the real-time model itself* —
tasks, events (WAIT/POST), attention/interrupt handling, sensor-based and
process I/O, timing — mapping almost 1:1 onto P2 concepts (**cogs as tasks,
hardware events, pin/interrupt handling, smart pins as sensor I/O, system
counter as timebase**).

**The killer fact (VERIFIED this session):** on the Series/1, **EDL object
code was executed by an emulator** — EDX "included an embedded interpreter for
EDL." So EDL is, factually, an **interpreted/bytecode instruction set**. Re-
hosting it on the P2 via XBYTE is the manual's thesis made literal: a real,
historical, event-driven *bytecode* language running on an event-driven, multi-
cog chip via the hardware bytecode engine. It closes the loop no 8-bit micro
can.

**Sourcing (VERIFIED available):** Bitsavers holds the EDX library at
`http://bitsavers.org/pdf/ibm/series1/edx/` — confirmed present: EDX **Study
Guides** SR30-0220 and SR30-0436 (carry EDL language detail + examples). The
formal **Language Reference SC34-0314** and **Language Programming Guide
SC34-0943** are reported on Bitsavers/Manx (exact path TO-VERIFY when we
source). Other library books: SC34-0312 (System Guide), SC34-0313 (Utilities/
Operator Commands/Program Prep), SC34-0316 (Communications), LY34-0168
(Internal Design, licensed), SX34-0101 (Reference Summary).
- TO-VERIFY when written: pin down SC34-0314 / SC34-0943 PDFs; confirm the EDL
  object-code / emulator-execution mechanics from the Language Reference or
  Internal Design before any concrete EDL encoding goes in print.

**Why this anchor (Stephen's rationale, recorded):** the contrast that an
event-driven architecture like the P2's existed *long before* the P2, as an
**independent implementation** of the same ideas, and is "a very different
animal." Personal interest: he found EDL/EDX genuinely fun to use, for the
same reasons he likes the P1 and P2 — and that interest is what surfaced it.

**Role:** EDL is the **featured vignette / conceptual centerpiece** of the
architecture chapter — NOT the buildable code capstone (the capstone stays a
tiny 8-bit micro per §5). 
- OPEN possibility to weigh after reading the Language Reference: emulating
  the **EDL VM itself** as the capstone (it's already a bytecode machine, so it
  may be cleaner than emulating Series/1 bare metal) — flagged, not promised.

---

## 7. Kindred-architecture vignettes (LOCKED as a set; content TO-VERIFY/cite when written)

Tiny (one-paragraph) mentions of architectures that **independently arrived at
the P2's philosophy** (many deterministic processors, event-driven, autonomous/
software-defined I/O, message-passing over interrupt-soup). Framing: "the P2's
ideas have ancestors and cousins." EDL is the *featured* anchor; these are the
surrounding constellation.

- **Transputer + Occam (INMOS, 1980s)** — array of processors w/ on-chip
  memory + hardware links; Occam = CSP processes + channels. The historical
  heavyweight; maps onto cogs + inter-cog communication.
- **XMOS xCORE + XC (contemporary)** — the P2's closest living cousin:
  deterministic logical cores, hardware-scheduled threads, event-driven ports,
  software-defined peripherals. By the transputer's architect (David May). The
  "P2 isn't alone *today*" point.
- **GreenArrays GA144 + Forth (Chuck Moore)** — 144 tiny async computers, local
  memory, port communication. Many-simple-cores minimalism; cross-links to
  XBYTE because Forth threaded interpreters are a classic bytecode-VM use.
- **Cell Broadband Engine — SPEs (PS3)** — synergistic cores each w/ local
  store + explicit DMA, no transparent cache = the cog local-memory + explicit-
  hub-movement model at another scale.
- *(optional one-liners)* **PSoC** configurable peripheral fabric as a smart-pin
  kin; **Parallax P1** as the P2's own direct lineage (heritage, not contrast).

---

## 8. Real-world implementations / references (gather + VERIFY — never from memory)

The P2 community has open-source implementations where **console ROM images
run on real P2 silicon**. These become a "Further Implementations" reference
section + grounding.

**Flagship hook — the P2 Arc8de project.** A real, existing community project: a
single P2 emulating the **Intel 8080** and running **up to 8 simultaneous
mini-arcade cabinets**. Creators: **Chip Egues** (lead architect), **Baggers**
(co-dev on the 8080 emulator; wrote the multiplayer tank + light-cycles games
in 8080 asm), **VonSzarvas** (PCB), **Coley**
(cabinet); cabinet graphics by **Andy C Spencer** (Retro Computer Museum, UK).
License **CC BY-SA 3.0**; Fusion 360 cabinet model on OBEX; DXF/PDF cabinet
files on the forum. Status (2021 page-1 snapshot — see the fuller p1–p8 timeline
below): emulator done, PCBs done, cabinets being built.

Core concept, quoted from the thread: *"P2 microcontroller emulating the intel
8080 processor in a single cog whilst simultaneously generating a display
(composite video) and single channel of audio."* So **one cog = one console**
(8080 emulation + composite video + 1-channel audio), and the P2's eight cogs
give eight independent cabinets. Per-console hardware: joystick + 5–6 buttons,
composite-video display, single-channel speaker audio, 3mm birch-ply laser-cut
cabinet.

**Software — stated precisely (corrected 2026-06-26 after a fact-check):** the
project began as an **8080 emulator** (Chip + Baggers) to run the classic
arcade game **Space Invaders**; the system now runs **8 separate arcade games**
plus a **multiplayer tank game** and a **multiplayer light-cycles game** — and
the thread states **only those last two** are *"written by Baggers in 8080
assembler."* **Game provenance — CONFIRMED (original ROM code).** The Parallax Arc8de product
page states each cog *"runs an 8080 emulator to execute the original ROM code"*
— so the arcade games ARE the **original ROM binaries** (Stephen's correction
was right). The multiplayer tank + light-cycles are the new-original additions
by Baggers. Guardrail retained: do **NOT** claim "all games written by Baggers"
(an earlier draft did; it was wrong).

Why it's the cold-open: it is the *proof of the low-overhead-dispatch payoff* —
eight simultaneous CPU emulations (each also driving its own video + audio) fit
on one P2 only because per-instruction emulation cost is small enough to leave
headroom. And it emulates the **Intel 8080** — a close cousin of our **8008**
capstone candidate and squarely in the §4 "8-bit micro" sweet spot (a point in
favor of 8008-as-capstone for cold-open coherence).

Source: Parallax forum thread "P2 Arc8de Project" — **all 8 pages read**
(`https://forums.parallax.com/discussion/173341/p2-arc8de-project`, p1–p8).

**Resolved from the full thread:**
- **Connector = ethernet-class cable, NOT RJ11.** Each cabinet links to the
  central P2 module over a single **Cat5/Cat6 cable carrying power + video +
  audio + I/O together** (Coley, p2: *"high quality Cat6 cable for each cab"*;
  p5: *"Power, Video, Audio and I/O - All in one"*). Stephen's RJ11-phone-cable
  recollection was off — it's **RJ45-class cabling** (thread itself is slightly
  inconsistent Cat5 vs Cat6).
- **Links found:** Parallax product page
  (`parallax.com/p2arc8de-one-p2-ec-module-provides-audio-video-and-buttons-for-eight-8-concurrent-games/`);
  OBEX Autodesk Fusion cabinet model
  (`obex.parallax.com/obex/autodesk-fusion-model-of-p2-arca8de-8in1/`); build
  videos (YouTube `VuvPvKg4_sM`, `mJIMBu8-LoE`). **No Arc8de *emulator/game*
  source repo was posted** in the thread — only the cabinet model + product page.
- **Cross-link:** **wuerfel_21** (author of the Yume suite below) contributed
  **artifact-color graphics code** for the 8-head display — Arc8de and the Yume
  emulators share a contributor.
- **Timeline/status:** 8 cabinets built 2021, shown at **PlayExpo Blackpool**
  (Oct 2021); a **Guinness World Record attempt** was in flight; stalled
  2022–23; **revived Feb 2025** — Ken Gracey planning **~30 units for a May 2025
  event** and pledging to *"commit [videos, resources, design files, hardware]
  to a home on our web site, permanently."*

- **Game provenance — RESOLVED (original ROM code).** The **Parallax Arc8de
  product page** states: *"Each of the P2's 8 cogs runs an 8080 emulator to
  execute the original ROM code"* — confirming the arcade games are **original
  ROM binaries** (Stephen was right). Per-game I/O is strikingly lean — **video
  on one pin, audio on one pin, button input on one pin** per console; module =
  **P2-EC**. (Source: `parallax.com/p2arc8de-…` product page.)

**STILL TO-VERIFY (not stated anywhere read — 8 thread pages + product page):**
- **Whether Arc8de uses XBYTE** for the 8080 core vs. a hand-rolled dispatch —
  neither the thread nor the product page states the dispatch mechanism, and the
  emulator source isn't posted. The "one cog per console" payoff holds either way.
  **PENDING:** Stephen asked **Chip Egues** directly 2026-06-26; answer expected
  ~2026-06-27 — when received, record as a personal-communication citation and
  clear this flag. (Also ask whether the emulator source will be published.)

**Captured emulator repos — the "Yume" suite** (user-supplied 2026-06-26; by
**wuerfel_21**, GitHub org **IRQsome**). Umbrella project **p2-dreamy-emulators**
(`https://sr.ht/~wuerfel_21/p2-dreamy-emulators/`). These run console ROM images
on **P2 + PSRAM** — prime §8 references, and concrete instances of the §4
families map (their guest CPUs are exactly the 68000 / 6502-family rows):

| Emulator | Console | Guest CPU(s) | Repos | Status |
|----------|---------|--------------|-------|--------|
| **MegaYume** | SEGA Mega Drive / Genesis | Motorola 68000 + Z80 | `github.com/IRQsome/MegaYume` · `git.sr.ht/~wuerfel_21/MegaYume` | released |
| **NeoYume** | SNK Neo Geo AES | Motorola 68000 + Z80 | `github.com/IRQsome/NeoYume` · `git.sr.ht/~wuerfel_21/NeoYume` | released |
| **MisoYume** | Super Nintendo (SNES) | 65(C)816 (6502 family) | `github.com/IRQsome/MisoYume` · `git.sr.ht/~wuerfel_21/MisoYume` | beta |

(SourceHut mirrors under evaluation by the author.) **TO-VERIFY when §8 is
written:** license per repo; **whether/how each actually uses XBYTE** vs. other
dispatch (a 68000 is the "word-opcode CISC, partial auto-fetch" §4 case —
confirm from source, never assume); confirm guest-CPU details from the repos.
The flagship Arc8de project (above) is a *separate* effort from the Yume suite.

**DISCIPLINE (trust chain):** do NOT name repos, authors, "which consoles," or
the 8-console project from memory. Gather via OBEX (p2kb tools) + Parallax
forums + GitHub, then cite each with **URL + author + what it emulates +
license**. Stephen will supply the names he knows (incl. the 8-console
project); Claude verifies + formats. Breadth target: **representative, not
exhaustive** — the community already finds the long tail; we just want the
spread covered.

---

## 9. Open decisions — RESOLVED for v0.1.0 (see §0)

1. **Capstone micro** — ✅ **6502** (was 8008/6502/8051).
2. **EDL depth** — ✅ **DEFERRED** out of v0.1.0 entirely (was: featured vignette vs.
   EDL-VM-as-capstone). Held for a later edition.
3. **Real-world reference list** — ✅ routes to **Appendix C** (links only); §8 names
   verified. Pending: Chip Egues' answer on whether Arc8de uses XBYTE (record as a
   personal-communication citation if/when it lands; otherwise the appendix states the
   dispatch mechanism is unstated).
4. Breadth-search for emulation targets — ✅ not needed for v0.1.0 (Appendix C is
   representative, not exhaustive).

---

## 10. Production wiring — to do at FULL stand-up (not yet done)

Only the `manuals/<slug>/` folder + this seed doc + the roster row exist so
far. Remaining to stand up the full manual (after the capstone is locked):
- Clone the **Streamer guide** skeleton: `manuals/` (opus-master/,
  creation-guide.md, MANUAL-DESCRIPTOR.md, CHANGELOG.md, voice-guide.md,
  audit/, examples-library/), `workspace/` (assemble-manual.sh, templates/,
  filters/, assets/, request.json, README.md, PUNCH-LIST.md), `outbound/`.
- Platform local overrides on the shared `p2kb-platform-*` stack:
  `p2kb-xbyte-local.sty`, `-diagrams.sty`, `-reference.latex`; wire
  `request.json` (template + lua_filters incl. the local).
- `MANUAL-DESCRIPTOR.md` (document-audit overlay: sources, code-line budget K,
  doc-class, fragile areas) + `creation-guide.md` (verification sources:
  Silicon Doc v35 XBYTE, p2kbArchXbyteEngine, the skip/EXECF YAMLs, PrincOps
  for S/360, the Bitsavers EDX library for EDL).
- Companion **example-library ZIP** (every snippet `pnut-ts`-compiled).
- Promote to Live on the roster when released.

---

## Sourcing summary (for the creation-guide)

- **XBYTE / skip family / FIFO:** Silicon Doc v35 + P2KB YAML
  (`p2kbArchXbyteEngine`, `p2kbPasm2Execf`, `p2kbPasm2Skipf`,
  `p2kbPasm2InstructionSkipping`, `p2kbArchFifo`). Authoritative, in-repo.
- **S/360:** *IBM System/360 Principles of Operation* (GA22-6821).
- **EDL / Series-1 / EDX:** Bitsavers EDX library
  (`bitsavers.org/pdf/ibm/series1/edx/`) — Study Guides SR30-0220 / SR30-0436;
  Language Reference SC34-0314; Programming Guide SC34-0943; Internal Design
  LY34-0168. EDL = emulator-executed bytecode language (verified via the EDX
  embedded-interpreter record).
- **Kindred architectures + real-world repos:** sourced/cited when written;
  never from memory.
- **Disciplines that apply:** tiny illustrative reference impl; no fabricated
  repos/authors/timings; no Spin2-method interpreter clock timings; all manual
  encodings traced to an authoritative source.
