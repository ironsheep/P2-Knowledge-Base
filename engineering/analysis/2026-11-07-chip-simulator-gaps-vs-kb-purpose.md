# Chip's simulator gap list, measured against what P2KB is for

**Input:** `engineering/ingestion/external-inputs/from-Chip/P2-KB-gaps-for-simulation.md`, from Chip
Gracey with an agent, November 2026, written against KB commit `1b0b173` (v1.24.7, 2026-10-12).
**Measured:** 2026-11-07, against the working tree at KB v1.25.5 and `pnut-ts` 1.55.10.
**Status:** report only. No YAML, register or manual has changed. Nothing here is decided.
**Work from:** `engineering/planning/P2KB-CONTRACT-GAPS-SPRINT-PLAN.md`, which re-measured every FIX, ADD
and PROVE row at its cited lines and moved some rows. Where the two differ, the plan is right.

## The short answer

P2KB should take far more from this document than its title suggests, but not for the simulator's
reason. Read as a programmer's document, Chip's list exposes real KB defects and real gaps. Read as a
simulator's document, a smaller part of it asks for something the KB is not.

- **Do these for the KB's own sake:** fix what it states wrongly, carry across what sources we already
  hold say, and put the programmer-visible unknowns to Chip or the bench.
- **Leave out the machine model:** exact CORDIC iterations, generator constants, clock-level pin
  behaviour and the debugger's wire format. They describe how the chip produces a result, which a
  correct program does not depend on.
- **If a machine model is ever wanted, build it as a separate system.** Its natural form is executable
  code plus a shared conformance suite, not YAML prose. The suite is the piece worth starting whether
  or not anyone builds the model, because it would also test the KB.

| Disposition | Items | Meaning |
|---|---|---|
| **FIX** | 18 | The KB states something wrong, self-contradicting or unsourced |
| **ADD** | 29 | A programmer needs it and a source we hold, or the compiler, already answers it |
| **PROVE** | 18 | A programmer can see it, but the sources are silent: ask Chip, or run the bench |
| **EDGE** | 6 | Could go either way; decide per item |
| **MODEL** | 8 | Simulator-only; does not belong in the served KB |
| **OK** | 36 | Already stated correctly; nothing to do except possibly findability |

The table in the Appendix has all 115 items, including 7 defects the check found that his list did not
name. Counts are of those rows. Items were split by hand, so treat them as proportions.

## The test used

Our doctrine already states the test for what reaches an agent: *whether it helps the agent build code
or understand the P2 and its drivers*, and an entry says *what a thing is, how to reach it and what it
is useful for*. Applied to this document, that gives three questions per item:

1. **Would correct code depend on it?** If a program's correctness changes with the answer, it belongs.
2. **Could an agent act on it?** A fact no code can use costs context and earns nothing.
3. **Can we prove it at tier?** A source, a compile proof, a bench run or a designer's statement. An item
   passing 1 and 2 but failing 3 is a question to resolve, not a thing to leave out.

The distinction underneath is **contract versus mechanism.** The KB is the programmer's contract: what
the chip promises. A simulator also needs the mechanism: how the chip keeps that promise. CORDIC shows
the line well. An agent needs the formats, the rule that results must be collected on time, and how
accurate the low bits are. It does not need the iteration count, unless it is reproducing the result
bit for bit, which is exactly what a simulator does and a program does not.

## What the document is, and how far to trust it

- **It is a strong field report, not a source.** Chip designed the part, but the document is
  co-written with an agent and most of it is questions. Its (G) items are explicitly guesses. Facts
  from it enter the KB through the normal routes, and a direct answer from Chip goes through the
  existing `chip-gracey-clarifications` channel.
- **Its decoder result is good news for us.** Generating a decoder from our encodings gave him 357
  instructions in 407 encodings. Our tree has exactly that: 382 PASM2 files, 25 of them directives,
  407 encoding entries, all decoding.
- **Its checks do not touch silicon.** The 93 passing results compare the simulator with values
  computed separately, so they say nothing about the chip itself.
- **Its "(V) items can go in as written" is nearly right.** I compiled the encoding claims:

| His (V) claim | Measured | Verdict |
|---|---|---|
| 20-bit JMP/CALL/CALLA/CALLB relative are bytes | −4040, −4008, −4012, −4016 in hub, each equal to the byte distance; bytes in cog too | Confirmed |
| **CALLD relative is bytes** (he groups it with these) | `calld pa/pb/ptra/ptrb,#far` in hub encodes **−1005 to −1008, the instruction distance**; near targets take the 9-bit form | **Not confirmed. See below** |
| 9-bit branches are in instructions | `djnz` and `tjz` encode −5 for a target five instructions before the next PC, same in hub | Confirmed |
| `LOC` relative is longs in cog | −7 in cog; **−28 in hub, which is bytes** | Confirmed, and hub is bytes |
| PTR layout, index widths, `00000` = 16 | All forms tested match, including `ptra[-20]` and `ptra--[16]` | Confirmed |
| Augmented PTR: `%1SUP` at bits 23..20, 20-bit signed | `ptra[##-1000]` gives index `$FFC18`; `ptra++[##1000]` gives `$B003E8` | Confirmed |
| Empty hub reads zero; top 16 KB at `$FC000` | Silicon Doc table 31 and interpreter line 2036 | Confirmed |
| `_RET_ SETQ2` applies to the table only, not the next routine | The Silicon Doc says "next bytecode, only"; nothing states the Q half | **Inferred from the interpreter working on his simulator; needs proof** |
| Tables at "LUT $100 and $215" | These mix two conventions: RDLUT index and cog address | Harmless, but do not copy as written |

His (G) on `djnz x,##far` also has an encoding answer now: **instructions**, an 18-bit field (−1003 for
a target 1,003 instructions back). And `TESTB`/`TESTP` versus `BITx`/`DIRx` is confirmed as he says:
`WC` or `WZ` alone (`01`, `10`) is the test, none or `WCZ` (`00`, `11`) is the bit operation. No document
we hold states it.

Compiler results prove the encoding, not what silicon does with it.

### The one unexplained result

Measured in one block on `pnut-ts` 1.55.10: `CALL`, `CALLA`, `CALLB`, `JMP` and `LOC` encode a far hub
target in bytes, and all four `CALLD PA/PB/PTRA/PTRB,#rel` forms encode it in instructions. I cannot
tell whether this is a compiler defect or how the silicon reads that encoding. If the silicon treats
this field as bytes, as the Silicon Doc's other 20-bit forms suggest, then `calld pa,#far` in hub code
branches to the wrong address. A short jumper-free bench run decides it. It is recorded as item 14 on
the PNut-TS punch list, marked unexplained. PNut itself was not tested.

## What to do for the KB

### 1. Fix what we serve wrongly (18 items)

None of these is in the register today. The ones most likely to produce broken code:

| KB location | It says | Truth | Harm to an agent |
|---|---|---|---|
| `architecture/cog.yaml:199-205` | COGINIT D is `D[31]` mode, `D[30]`, `D[20]` | `%E_N_xVVV`, as `language/pasm2/coginit.yaml:5` says | Builds a wrong COGINIT |
| `smart-pin-11110-async-serial-transmit.yaml:20,34` | IN rises "when transmission complete" | IN rises as the word enters the shifter (Silicon Doc :4696); `:207` and `smart_pins.yaml:636` agree | Shuts the pin off with a byte still going out |
| `smart-pin-11111-async-serial-receive.yaml:10,19` | Stop bit "validated automatically" | No source states any stop-bit check | Writes no framing check, trusting one that may not exist |
| `architecture/hub.yaml:107,113,241-243` | Words and longs "must be" aligned | "No special alignment rules" (Silicon Doc :2868, datasheet :701) | Pads structures and rejects valid code |
| `architecture/hub.yaml:233`, `execution_modes.yaml:140` | `$80000+` "Reserved" or "Usually ROM" | The gap reads `$00`; the interpreter relies on it | Misses a real technique |
| `language/pasm2/brk.yaml:12` | BRK bit order `BCDEFGHIJKLM` | `LKJIHGFEDCBA` (Silicon Doc, `debug_interrupt.yaml:91`, debugger source) | Enables the wrong breakpoint conditions |
| `concepts/cog_hub_execution.yaml:83,182,225-233,349` | RDLONG 9-24, WRLONG 3-12 "in both modes" | 9-16 and 3-10 in cog; 9-26 and 3-20 in hub | Wrong timing budgets |
| `system-registers/complete-system-registers-index.yaml:265-266` | COGINIT clears DIR, preserves OUT | No source found. Mark unknown until proven | Relies on an unproven reset state |

The rest are in the Appendix: RCR's flag cell, XBYTE's `$1F8..$1FF` and flag source, the REP block's
wording, the debug-state address, the egg-beater "COG 0→1→2" order, TRGINT versus STALLI, and an
unsourced CORDIC stall.

### 2. Carry across what we already hold (29 items)

This is the largest and cheapest gain: the source sits in the repo, and no bench or Chip is needed.
Highest value first:

- **The ALTI control table** (Silicon Doc :618-650). `alti.yaml` names the fields and gives no codes.
- **Branch units, in one place:** 20-bit bytes, 9-bit instructions, `LOC` longs in cog and bytes in hub,
  `##` S-branches in instructions. This extends the addressing work already held for v1.25.6.
- **PTR expressions:** the `%1SUPNNNNN` layout and index ranges, the block-transfer step
  (`PTRA += (x+1)*4`), and the augmented form.
- **The Q register's life:** which instructions use it, and the events that end it (Silicon Doc :1181-1187).
- **Pixel mixing:** the `DMIX`/`SMIX` formula and table. The KB has prose only.
- **XBYTE:** the compressed-index rule, F=1 flags coming from the index, and `$1FF` not popping.
- **`RGBSQZ`/`RGBEXP` and `CRCBIT` bit rules** (instruction CSV).
- **CORDIC's collection rule:** "each result must be retrieved on time or else it will be overwritten"
  (datasheet :924-926). The KB has the REP recipe without the reason.
- **Consolidations:** one HUBSET mode table, one event-clearing table, the wrap sentence missing from ten
  `DIRx`/`OUTx` pages.

### 3. Get the programmer-visible unknowns proven (18 items)

These are worth knowing because correct code can depend on them, but no source says. Our bench rule
applies: only after an exhaustive search finds the sources silent. Two routes, and they combine well:
**ask Chip first**, because many are a one-line answer from the designer, then confirm the ones that
matter on silicon. He also offers to run tests, which fits our XF tier (we specify, they run).

The most useful, because real code hits them:

- How eight cogs' `DIR` and `OUT` combine: is a cog's `OUT` gated by its own `DIR`?
- What `COGINIT` resets: `DIR`, `OUT`, flags, stack, events.
- `CALLD` far encoding in hub (above).
- CORDIC: does `QDIV` then `GETQX` alone safely drop `Y`? What comes back when the quotient overflows?
- Lifetime: `SETQ` or `AUGS` across a false condition; two `AUGS` in a row; `ALTx` before a skipped
  instruction.
- Reading back a driven pin; async RX with a bad stop bit.

Many of these fit one or two jumper-only rigs on our free pins.

### 4. Treat findability as a finding in its own right

Chip listed as guesses several things the KB already stated at his commit: pin latency, the `SETSE`
table, interrupt registers and shielding, the `WRPIN` word. Section 10 says interrupts "couldn't be
simulated from the KB alone", yet nearly all of it is there. Only part of that can be blamed on the
page: `SETSE`'s examples did contradict its table until the 2026-11-06 fix.

I do not know how his agent read the KB. But if a designer's agent missed it, a code-writing agent can
too, and the served KB shows why:

- `p2kb_find` for "latency" returns **nothing**; "pin timing" does find `p2kbArchIoPinTiming`.
- A natural question, "how long from OUT to the pin changing", returns hundreds of 0.25 and 0.125
  suggestions with no answer ranked above them.
- **No page in `language/pasm2/*.yaml` links to `architecture/interrupts.yaml` or
  `architecture/io_pin_timing.yaml`.** An agent reading `SETINT1` or `DRVH` is never led to either.

The fix is links and aliases, which is exactly the job our doctrine gives the KB.

### 5. Small items worth a sentence

- **Directives are not marked machine-readably.** Only `category:` separates them, and only `asmclk.yaml`
  says "pseudo-instruction". A marker is cheap, but no code-writing agent needs it. I would add it only
  if a tool wants it.
- **His "about 140 entries with non-32-bit `bits`" does not reproduce.** I count 0 at HEAD, on 407
  entries. The survey found 0 at his commit too. I don't know what was counted, so it is worth asking.

## Brainstorm: a description of how the P2 really operates

You asked this as a thinking exercise, so this section offers options and a leaning, not a plan.

### What such a description contains

It is not one thing. It has four layers, and they land differently:

| Layer | Content | Who needs it | Natural form |
|---|---|---|---|
| **0. Contract** | What each instruction and facility promises | Everyone | KB YAML (today) |
| **1. State and interaction model** | Every piece of state a cog holds (flags, Q, stack, pending ALT and AUGS, skip pattern, REP, events) and what sets, consumes and resets it | Programmers and simulators | A table or two |
| **2. Cycle model** | Pipeline order, egg-beater phase, FIFO refill, clock-level pin behaviour, CORDIC and PRNG internals | Simulators, and cycle-counting programmers occasionally | Executable code |
| **3. Silicon-exact** | Analog pads, metastability, unintended states | Almost nobody | Not modelled |

**Layer 1 is the surprise.** It is mechanism, yet programmers trip on it, and about half of the PROVE
list is really one missing page. A single `architecture/cog-state` entry, "what a cog holds, and
what sets, consumes and resets each thing", could pass the KB's own test. It would also be the natural
home for the COGINIT answer. I would bring this one layer into the KB, once its cells are proven.

### Where layer 2 could live

**A. Inside the served KB, mixed with everything else.**
Pros: one pipeline, one server, the gates already exist.
Cons: it costs what makes the KB good. Search results for code writers fill with mechanism, as the
findability results above already warn. Agents start depending on internals. And most cells would have
no citable source, since no Parallax document states them, which fails the KB's own sourcing gate.
**I would rule this out.**

**B. A separate region in this repo, with its own index and tool.**
This has precedent: OBEX has its own region, rules and `p2kb_obex_*` tools. A `p2kb_model_*` tool would
keep it out of code-writing searches.
Pros: reuses the MCP, the bench ledger and the review habits; one place to look.
Cons: prose still cannot prove itself. Nothing tells you when a sentence about pipeline order is wrong,
and it would need a new trust tier and new gates, so it is a large commitment for a small audience.
**A workable fallback, if prose is what is wanted.**

**C. A separate system: a reference model plus a conformance suite.**
The description would *be* a running simulator, with prose generated from it or written around it. Its
truth comes from the silicon and the design, tested by traces.
Pros: this is the only form that can be wrong out loud. A cycle model in code either matches the trace
or it does not. It needs no KB trust tier and costs the KB's readers nothing. Chip has already built
much of one.
Cons: someone has to own it, and it is not ours today. Chip's simulator took its behaviour from the KB,
so it cannot independently validate the KB. Only silicon breaks that circle.
**This is where I lean.** Layer 2 belongs here.

**D. Do nothing, and let the HDL study stay as it is.**
The study's theory of operations already touches every topic on his list at the topic level, and it is
the closest thing we hold to this description. But it is indicator-tier by your ruling, git-ignored,
and its known weakness is the exact value delivered, which is what a simulator most needs. Inside a
system like C it could guide what to test without any certification. That would need your decision, and
the clean-room arrangement would need considering. The obvious question for Chip is whether a model should
come from the design source directly. I don't know what he can share.

### The piece that connects them: a conformance suite

Chip's fifth wish, "golden hardware traces", is the one idea here that serves the KB directly, and we are
closer than he knows.

**What we have:** 101 EF entries, 19 XF entries, and 87 tracked `.spin2` programs, most printing results
through DEBUG, run on real P2 silicon.

**What is missing:** the outputs in comparable form. By design we version the source and our reading of
it, not raw logs, and only two campaign folders carry a golden file. Coverage is also uneven: nothing
measures async bit timing, OUT-to-pad latency or COGINIT start time.

**What it would take:** each accepted test keeps its expected output as a small versioned file beside
its source. A runner compares. That is a modest change to one README rule.

**What it would give us, even with no simulator:**

- A regression check on what the KB asserts, runnable on any new silicon or compiler.
- A way to take outside runs (XF) with a machine check rather than prose.
- Something real to give Chip, which is more than he asked of us.

**What a simulator would give us back:** our compile gate is legality only. It proves an example is
accepted, not that it does what its text says. A simulator that passes the suite could run every KB example
and check behaviour, which is the one thing our gates cannot do today. That is a real reason for the KB
to want a simulator to exist, without the KB having to contain one.

## Suggested order, if you take any of this

1. **Fix and add (sections 1, 2, 4)** as a KB release. No bench or decision is needed beyond your go, and
   it joins the v1.25.6 addressing work naturally. Manuals inherit changes through the usual findings; at
   least one XBYTE guide line (`xbyte-body.md:1113`, flags "from the bytecode's low bits") needs the same fix.
2. **One question packet to Chip** covering PROVE, EDGE and the `CALLD` result.
3. **A bench rig** for what remains programmer-visible after his answers.
4. **The conformance change** to the hardware-verification folder.
5. **The layer 1 page,** once the COGINIT and lifetime answers are in.
6. **Layer 2 stays out of the KB.** Revisit only if someone takes on the model.

## What I did not check

- `p2docs-github-io` and `p2-qa-spreadsheet` were searched only partly; some ADD or PROVE items may have
  more support there.
- Remaining per-mode smart-pin pages, `trgint2/3`, `nixint2/3`, `addct2/3` and the debug-related manual layers.
- That the v51 debugger source matches v55 behaviour; v51 is the only debugger source we hold.
- PNut itself. All compile results are `pnut-ts` 1.55.10.
- Whether anything here changes what any manual says, beyond the one XBYTE line named.
- The survey results that I did not personally re-read at the line. I re-read the defects in section 1,
  the ALTI and pixel sources, the PRNG and CORDIC sources, the Q rule and the memory map, and I ran every
  compile result myself. Other Appendix rows rest on the surveys' cited lines.

## Appendix: every item

Silicon Doc lines cite `silicon-doc-text.txt`, except sections 7 to 11, which cite `p2-documentation.txt`.

| § | Item | Disposition | Basis |
|---|---|---|---|
| 1 | 20-bit JMP/CALL/CALLA/CALLB units | ADD | `branch_addressing.yaml:14` partial; compiled; SD:731 |
| 1 | 9-bit branch units | ADD | SD:690; on `tjs` etc., absent on `djnz` |
| 1 | `LOC` units | ADD | Compiled; `loc.yaml:13` has no unit |
| 1 | `##` on S-branches | ADD | Compiled; 18-bit instructions; `tjs.yaml:12-16` agrees |
| 1 | `JMPREL` | OK | `jmprel.yaml:13`, SD:686 |
| 1 | `CALLD` far relative in hub | PROVE | Compiled in instructions, unexplained |
| 2 | `%1SUPNNNNN` layout | ADD | SD:3164-3205; only in `source:` fields today |
| 2 | Index widths, `00000` = 16 | ADD | SD:3171-3180; compiled |
| 2 | Scaling by size | OK | `addressing_modes.yaml:50` |
| 2 | Block transfer pointer update | ADD | SD:3283-3298; EF-067 |
| 2 | Augmented form | ADD | SD:3166; compiled |
| 2 | Plain immediate 0-255 | OK | `lookup_ram.yaml:127` |
| 3 | SETQ through AUGS/AUGD | OK | `augs.yaml:26`, `augd.yaml:22`; his "only ALTx" is out of date |
| 3 | Which instructions use Q, and its life | ADD | SD:1181-1187, :60-62 |
| 3 | SETQ/AUGS across a false condition | PROVE | EF-033 and EF-091 do not cover it |
| 3 | SETQ/AUGD and a skipped instruction | PROVE | EF-091 covers AUGS only |
| 3 | Two AUGS in a row | PROVE | Silent |
| 4 | Compressed-index formula | ADD | SD:998-1001; interpreter confirms |
| 4 | F=1 flags: index, not bytecode | FIX | `xbyte_engine.yaml:42` vs `:194`; SD:946 |
| 4 | `$1FF` does not pop | ADD | SD:897 |
| 4 | "RET to `$1F8..$1FF`" | FIX | `xbyte_engine.yaml:248`; sources name `$1FF` only |
| 4 | `_RET_ SETQ2` and Q on the next routine | PROVE | SD:969 covers the table only |
| 4 | PB sampling; 6 clocks and `_RET_` | OK | `xbyte_engine.yaml:41`; 8-clock minimum stated; SD wording differs |
| 5 | Which CALLs and RETs suspend a skip pattern | PROVE | Three named, CALLA/B/D unstated |
| 5 | Interrupts during a skip | OK | `instruction_skipping.yaml:117` |
| 5 | JMP inside a skip pattern | PROVE | SD:891 for SKIPF; plain SKIP only implied |
| 5 | SKIPF in hub, skipped cost | OK | `skipf_branching.yaml:36-38` |
| 5 | ALTx before a skipped instruction | PROVE | Silent |
| 5 | REP cancelled by `_RET_` | PROVE | `rep_instruction.yaml:160` is unsourced |
| 5 | REP in hub, with SKIP/SKIPF | ADD | SD:773, :883-885 |
| 5 | REP D=0, S=0 | OK | `rep.yaml:12` |
| 6 | ALTI control codes | ADD | SD:628-650 |
| 6 | ALTI mask sizes | ADD | SD:618-626 |
| 6 | ALTI and the I bit, other modes | PROVE | %RRR 101 only |
| 7 | CORDIC algorithms, iterations, rounding | MODEL | `cordic.yaml:190-194` honestly says unknown |
| 7 | QSQRT rounding, operands | OK | `qsqrt.yaml`; EF-104 |
| 7 | Divide by zero | OK | `qdiv.yaml:121`; EF-089 |
| 7 | Quotient over 32 bits | PROVE | Silent |
| 7 | Outstanding results and overwrite rule | ADD | Datasheet :924-926; EF-053 |
| 7 | Do GETQX and GETQY each consume? | PROVE | Implied by interpreter :266-272 |
| 7 | X read, not Y, then a new command | PROVE | Same rig |
| 7 | Issue rate; "pipeline full" | FIX | `cordic.yaml:142` unsourced; rate is stated |
| 7 | GETQX with nothing pending | PROVE | Timing stated, value not |
| 8 | xoroshiro128** constants | MODEL | Named only |
| 8 | Boot seeding | ADD | SD:6446-6447 |
| 8 | HUBSET seeding, 32 of 128 bits | ADD | SD:6442-6445; hardware manual differs |
| 8 | Advances every clock | OK | `xoro32.yaml:75` |
| 8 | Bits each cog sees | MODEL | "Scrambled"; mapping not given |
| 8 | XORO32 algorithm | EDGE | A deterministic instruction result; take it if Chip gives it |
| 8 | BITRND, DIRRND family bits | MODEL | Random by design |
| 8 | WAITX WC bits | MODEL | Random by design |
| 9 | Egg-beater phase | EDGE | Cycle-exact programmers might use it; EF-073 sweeps could yield it |
| 9 | RDxxx, WRxxx ranges | OK | `rdlong.yaml:17`, datasheet |
| 9 | Unaligned accesses; "must be aligned" | FIX | `hub.yaml:107,113,241`; datasheet :701 |
| 9 | SETQ block start-up | EDGE | EF-034 gives a measured rate, no formula |
| 9 | RDFAST, WRFAST start-up | OK | `rdfast.yaml:9` |
| 9 | FIFO refill | OK | `fifo.yaml:15` |
| 9 | Hub exec per-instruction | OK | `cog_hub_execution.yaml:28` |
| 9 | Branch cost | OK | `cog_hub_execution.yaml:214` |
| 9 | Hub exec and RDFAST | OK | `fifo.yaml:241`: they do not share |
| 10 | SETINTx codes, priorities | OK | `interrupts.yaml:27` |
| 10 | IJMP, IRET | OK | `interrupts.yaml:100` |
| 10 | STALLI, ALLOWI | OK | `interrupts.yaml:132` |
| 10 | RESIx, RETIx | OK | `interrupts.yaml:213` |
| 10 | TRGINT vs STALLI | FIX | `trgint1.yaml:12` vs `interrupts.yaml:188`; needs bench to settle |
| 10 | Shielding | OK | `interrupts.yaml:431` |
| 10 | HUBSET debug enable | ADD | Only in `hub.yaml:39`; `hubset.yaml` lacks it |
| 10 | Debug ISR entry and save area | OK | `debug_interrupt.yaml:64` |
| 10 | BRK conditions and bit order | FIX | `brk.yaml:12` vs SD and debugger source |
| 10 | GETBRK fields | ADD | SD:5965-6019; state encodings thin |
| 10 | COGBRK | OK | `debug_interrupt.yaml:151` |
| 10 | Debugger wire protocol | MODEL | A tool matter by our doctrine; v51 source only |
| 11 | SETSE1..4 | OK | `event_system.yaml:101`; examples fixed 2026-11-06 |
| 11 | SETPAT | OK | `event_system.yaml:183` |
| 11 | FBW, XMT, XFI, XRO, XRL | OK | `poll*.yaml` |
| 11 | Clearing rules | ADD | Stated across 16 files; no single table |
| 11 | CT1-3 fires on passing, not equality | OK | `addct1.yaml:12`, SD:5299, EF-081 |
| 12 | IN, Z and RDPIN before first result | ADD | SD:4105-4254 for documented modes; RX and ADC silent |
| 12 | Async TX buffer depth | ADD | SD:4696 |
| 12 | Async TX IN timing | FIX | Self-contradiction, SD:4696-4705 |
| 12 | Async RX stop bit | FIX | Unsupported "validated"; bench for behaviour |
| 12 | Fractional bit-edge placement | MODEL | Formula stated (SD:4692; the fraction is `X[15:10]`, not his `X[31:16]`) |
| 12 | WRPIN mode word | OK | `smart_pins.yaml:297-436` |
| 12 | Pin range wrap | ADD | Applies to all; ten `DIRx`/`OUTx` pages lack the sentence |
| 12 | WRPIN while DIR high | MODEL | `smart_pins.yaml:143` matches the limit of the documents |
| 13 | How cogs' DIR and OUT combine | PROVE | ORed, per-cog gate unstated; EF-105 does not settle |
| 13 | Smart pin output vs OUT | OK | `smart_pins.yaml:377` |
| 13 | OUT-to-pin, pin-to-INA latency | OK | `io_pin_timing.yaml:48,67` |
| 13 | Reading a driven pin | PROVE | SD:3706; cheap jumper test |
| 14 | What COGINIT resets | FIX | Index `:265-266` unsourced; rest is PROVE, see next row |
| 14 | COGINIT stack, flags, events, skip, REP | PROVE | Silent |
| 14 | COGINIT load and start time | EDGE | Absent; bench or Chip |
| 14 | Cog re-launching itself | PROVE | Example only: `coginit.yaml:70` |
| 14 | `COGID {#}D WC` | OK | `cogid.yaml:5` |
| 14 | SETLUTS | OK | `lookup_ram.yaml:73`; EF-096 |
| 14 | HUBSET modes in one place | ADD | SD:2602-2606; split across files |
| 14 | Empty hub reads zero; `$FC000` | FIX | `hub.yaml:233`, `execution_modes.yaml:140` |
| 15 | Pixel operation formulas | ADD | SD:1214-1255 |
| 15 | SEUSSF, SEUSSR permutation | EDGE | No source; deterministic, take it if Chip gives it |
| 15 | RGBSQZ, RGBEXP | ADD | CSV:411-412 |
| 15 | CRCBIT, CRCNIB | ADD | CSV:155-156; nibble order inferred |
| 15 | Shift 0 flag | FIX | `rcr.yaml:28` says `D[31]`, against `:18`, `:32` and CSV |
| 15 | ADDS, ADDSX | OK | `adds.yaml:6,25`; agree now |
| 15 | ENCOD, ONES, TESTN | OK | Per-file flags |
| 15 | GETBYTE, GETWORD Z | OK | Both "No effect" |
| 15 | RDLUT with PTRx | ADD | PTRx forms stated; scale needs a one-line proof |
| 15 | TESTB vs BITx by flags | ADD | Compiled |
| 15 | `bits` fields and pseudo marking | EDGE | 0 malformed of 407; 25 unmarked directives |
| new | COGINIT D layout in `cog.yaml:199-205` | FIX | Against `coginit.yaml:5` |
| new | RD/WR timing in `cog_hub_execution.yaml` | FIX | 9-24, 3-12 against the datasheet |
| new | REP "no branches" at `rep_instruction.yaml:68` | FIX | Against `:95` |
| new | Debug state at `$7F000` in `hub.yaml:236` | FIX | SD: last 16 KB and `$FFC00+` |
| new | Egg-beater "COG 0→1→2" in `hub.yaml:66-71` | FIX | Unsourced; sources say each cog sees the next slice |
| new | HUBSET "in clock mode, D[31]" framing, `hubset.yaml:20,26` | FIX | SD:2602-2606: the top bits pick the mode |
| new | Per-instruction links to interrupts and pin timing | FIX | 0 of 382 pages; `latency` finds nothing |
