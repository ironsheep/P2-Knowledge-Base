# P2KB contract gaps — sprint plan

**Head:** `yaml:p2kb` · **Written:** 2026-11-07 · **Status:** READY. Planning Gate met on 2026-11-07 after
three independent audit rounds. Tasks are generated (`plan-to-tasks`) and the sprint started
(`sprint-start`) only on Stephen's word.

**Evidence:** `engineering/analysis/2026-11-07-chip-simulator-gaps-vs-kb-purpose.md`, reading
`engineering/ingestion/external-inputs/from-Chip/P2-KB-gaps-for-simulation.md`. Three read-only surveys
re-measured every FIX, ADD and PROVE row on 2026-11-07. The results below replace the analysis's rows.

**What the sprint is for.** Stephen, 2026-11-07: *"I want to put this into a detailed sprint plan so we
can upgrade the P2KB with information this has identified, if we have sources."* The KB is the
programmer's contract, so the sprint corrects what it states wrongly, carries across what our sources
already say, makes it findable, and proves the few programmer-visible unknowns.

**Done means:** every row below is fixed, added, or stated as not documented; a KB release serves it
with its audit passed; and each bench arm has an accepted EF entry or a recorded reason it gave none.
Every YAML file the sprint touches is certified whole (§16), and every Silicon Doc section has a
recorded YAML home or a reason it is not carried (§15).

**Shape (Stephen, 2026-11-07, "yes, the shape you recommend").** Two plans. This one: the Silicon Doc
walk (§15) runs as research before this plan's gate and its findings join this plan; the update then
certifies every file it touches (§16). A separate process plan, written later, makes source carriage
part of ingestion's definition of done, adds the programmer question list and its KB-only probe, walks
the datasheet, the instruction CSV and the Spin2 sources, and certifies the remaining founding files
in waves, one KB release per wave. Evidence for the split:
`engineering/analysis/2026-11-07-why-the-contract-gaps-were-missed.md`.

**Not in this sprint:** the machine model (CORDIC iterations, generator constants, clock-level pin
behaviour, the debugger's wire format), a simulator, and the conformance suite. One new check is built: §12's pre-tag certification gate,
which Stephen asked for with F-640's hold (2026-11-06). Every other check is a compile, a search, or an
existing gate.

**Paths.** `SD` = `engineering/ingestion/sources/silicon-doc/silicon-doc-text.txt`. `P2D` = the
`p2-documentation.txt` beside it. `DS` = `engineering/ingestion/sources/p2-datasheet/p2-datasheet-text.txt`.
`CSV` = `engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv`.
`INT` = `engineering/ingestion/external-inputs/source-code/spin-interpreter/v55/Spin2_interpreter.spin2`.
KB paths are under `deliverables/ai/P2/`; `pasm2/` means `language/pasm2/`.

---

## Open Questions

Each is posed to Stephen one at a time, with its reasoning in full. The recommendations:

1. ~~A question packet to Chip~~ **Resolved 2026-11-07: no questions to Chip.** Stephen: *"no questions to
   chip, we resolve things ourselves"*. §10 now states those items ourselves.
2. ~~What the bench carries~~ **Resolved 2026-11-07: all 15 arms as planned** (Stephen: *"all 15 as
   planned"*). §9 stands; the left-out list stays out.
3. ~~The cog-state page~~ **Not a question: where approved content lives is ours to decide** (Stephen,
   2026-11-07). §11's page is decided: one canonical home for cog state.
4. ~~The v1.25.6 held work~~ **Not a question: already decided.** Stephen held F-640 "documents first"
   on 2026-11-06, with the whole-page record as a gate and the sweep by operand to come with it. The
   documents shipped on 2026-11-07, so all three join this release (§12, §16).
5. ~~Manual masters~~ **Resolved 2026-11-07: YAML first, manuals after.** Stephen: *"complete the YAML
   edits for all of what we're trying to do, then, in a focused effort, apply the YAML changes to all
   the manuals."* §13 is now a running record of manual reach, kept during the YAML work.
6. ~~Committing the evidence~~ **Not a question: commits are ours** (Stephen, 2026-11-07). Chip's
   document, the analyses, the walk ledger and this plan are committed together, as records.
7. ~~Final scope adjustment~~ **Resolved 2026-11-07.** All 19 open register entries were shown to Stephen
   as one group, each group with its proposed disposition. He answered *"yes as recommended as long as
   it is sourced and proven fact"*. Planning Gate aspect 3 lists each entry's disposition as it was shown
   to him.

---

## File table

| File | Scope | § |
|---|---|---|
| `architecture/hub.yaml` | Alignment, empty hub, debug area, egg-beater wording | 1 |
| `architecture/cog.yaml` | COGINIT D layout | 1 |
| `architecture/smart-pins/smart-pin-11110-async-serial-transmit.yaml` | IN timing, buffer | 1, 7 |
| `architecture/smart-pins/smart-pin-11111-async-serial-receive.yaml` | Stop-bit claims | 1 |
| `architecture/xbyte_engine.yaml` | Flag source, `$1FF`, compressed index, no pop | 1, 5 |
| `architecture/cordic.yaml` | Stall claim, overwrite rule | 1, 7 |
| `architecture/system-registers/complete-system-registers-index.yaml`, `dira-dirb-registers.yaml` | Unsourced COGINIT claims | 1, 11 |
| `pasm2/concepts/cog_hub_execution.yaml` | RD/WR timing | 1 |
| `pasm2/concepts/execution_modes.yaml` | `$80000+` line | 1 |
| `pasm2/concepts/rep_instruction.yaml` | REP wording, `_RET_` source, link | 1, 3 |
| `pasm2/concepts/multi_cog_synchronization.yaml` | `$7F000` mailbox | 1 |
| `pasm2/brk.yaml`, `pasm2/rcr.yaml` | One defect each | 1 |
| `pasm2/trgint1..3.yaml` | STALLI wording, unchanged until arm H answers | 1, 9 |
| `engineering/tools/validation/audit-yaml-certification-record.py` (new), wired into `validate-dod-release.py` | §12's pre-tag gate: a release-diff YAML file with no certification row fails | 12 |
| `pasm2/alignl.yaml`, `language/spin2/methods/coginit.yaml` | Alignment siblings | 1 |
| `language/spin2/methods/getrnd.yaml` | "True random" and cryptographic claims | 1 |
| `pasm2/concepts/branch_addressing.yaml`, `pasm2/loc.yaml`, 43 S-branch pages | Units table and one line each | 3 |
| `pasm2/concepts/addressing_modes.yaml`, `setq_block_ops.yaml` | PTR expressions, block update | 3 |
| `pasm2/concepts/special_registers.yaml`, `alti.yaml`, `testb.yaml`, 8 `bit*` pages | Q life, ALTI codes, shared opcode | 4 |
| `pasm2/hubset.yaml`, `getbrk.yaml`, `architecture/event_system.yaml` | Mode table, PRNG, GETBRK, clearing | 6 |
| `architecture/smart_pins.yaml`, 11 `dir*`/`out*` pages | Reset states, wrap sentence | 7 |
| `pasm2/concepts/pixel_mixer.yaml` (new), six pixel pages | Formula and table | 7 |
| `pasm2/rgbsqz.yaml`, `rgbexp.yaml`, `crcbit.yaml`, `crcnib.yaml`, `rdlut.yaml`, `wrlut.yaml`, `architecture/lookup_ram.yaml` | Bit rules, PTRx scale | 7, 9 |
| `architecture/interrupts.yaml`, `architecture/io_pin_timing.yaml`, 62 instruction pages | Aliases, links | 8 |
| `architecture/cog_state.yaml` (new, decided) | What a cog holds | 11 |
| `external-sources/compiler-verification/COMPILE-PROOFS.md` | CP-031 to CP-033 | 2 |
| `external-sources/hardware-verification/` | New campaign, EF entries | 9 |
| `engineering/ingestion/sources/silicon-doc/SILICON-DOC-CARRIAGE-LEDGER.md`, `carriage-walk-2026-11-07/` | Walk ledger and range files (written 2026-11-07) | 15, 17 |
| `engineering/operations/YAML-CERTIFICATION-RECORD.md` (new) | One row per certified file | 16 |
| `engineering/ingestion/SOURCE-ERRATA.md` | Four new source errata | 17.9 |
| The files in §17's packages | Walk findings | 17 |

## Design decisions to flag

- **New pages:** `pixel_mixer.yaml`, because six instructions share one table and none owns it. The
  alternative is to put it in `mixpix.yaml` with five pages pointing there. Decided by the rule that a
  fact has one canonical home. `architecture/cog_state.yaml` is decided the same way (§11). The
  colorspace converter and DVI output (§17.3) get their home by the same rule during the work.
- **`CALLD` in the units table:** the cell stays "not yet proven" until the bench answers, and
  `branch_addressing.yaml:16`, which lists `CALLD` as a byte form today, is changed with it.
- **Directive marker and `bits` fields:** no change. No code-writing agent needs a marker, and 0 of 407
  `bits` fields are malformed. His "about 140" is not pursued: our measurement stands.

---

## 1. Fix what we serve wrongly

**Why.** These are served now and each can produce wrong code. **Rule:** everything seen wrong is fixed
in the pass and searched for as a class (`yaml-knowledge-base-maintenance`), and only a true blocker
goes to the register.

| Defect | Served text | Truth, with source | Also fix |
|---|---|---|---|
| COGINIT D layout | `architecture/cog.yaml:201-204`: D[31] mode, D[30], D[20], D[19:0] address | `%E_N_xVVV`; the address is S (SD:376-392; `pasm2/coginit.yaml:5`) | None found |
| Async TX IN | `smart-pin-11110-…:20,34`: raised "when transmission complete" | IN rises when a word moves to the shifter; busy in C means complete (SD:4696,:4701,:4707) | None found |
| Async RX stop bit | `smart-pin-11111-…:10,13,19,213`: "validated" | The state sequence has no stop-bit step (SD:4727-4736) | The I/O guide already agrees (`chapter-17-serial-receive.md:34`) |
| Hub alignment | `hub.yaml:107,114,241-242`: "must be" aligned | "No special alignment rules" (SD:2868) | `hub.yaml:18,95,201`; `language/spin2/methods/coginit.yaml:45`; `pasm2/alignl.yaml:24` |
| Empty hub | `hub.yaml:233` "Reserved"; `execution_modes.yaml:140` "Usually ROM" | `$80000..$FBFFF` reads `$00` (SD table 31; INT:2036); top 16 KB at `$FC000` (SD:2870) | None found |
| Debug area | `hub.yaml:236`: `$7F000_$7FFFF` | Top 16 KB, buffers from `$FFC00` (SD:2399,:2437,:2455) | `multi_cog_synchronization.yaml:81,226` mailbox sits in the protected region |
| Egg-beater order | `hub.yaml:70-71`: "COG 0→1→2…" | Each cog reaches the next slice every clock (SD:2999,:3001) | None found |
| BRK order | `pasm2/brk.yaml:12`: `…_BCDEFGHIJKLM` | `%aaaaaaaaaaaaaaaaeeee_LKJIHGFEDCBA` (SD:2498-2512) | Assembly `instructions-b.md:311` (§13) |
| RD/WR timing | `cog_hub_execution.yaml:83,182,225,227,231,233,349`: 9-24, 3-12 | 9..16 and 3..10 in cog, 9..26 and 3..20 in hub (DS:1827-1841; CSV line 178) | None found |
| RCR shift 0 | `pasm2/rcr.yaml:28`: `D[31]` | `D[0]` (CSV:30; the page's own `:18,:32`) | Seven sibling pages are right |
| XBYTE flags | `xbyte_engine.yaml:42`: "from bytecode" | Bits 1,0 of the table index (SD:946; `:194`) | XBYTE guide `xbyte-body.md:822,1113` (§13) |
| XBYTE trigger | `xbyte_engine.yaml:248`: "RET to `$1F8..$1FF`" | `$1FF` (SD:897,:965) | None found |
| REP wording | `rep_instruction.yaml:68,97`: "No branches" | A taken branch cancels REP (SD:775; `:95`) | None found |
| REP and `_RET_` | `rep_instruction.yaml:160` unsourced | SD:775; INT:219,:266 rely on it. Source it, no bench | None found |
| CORDIC stall | `cordic.yaml:142`: "when pipeline full" | No source. The hazard is overwriting (DS:93,:925; SD:3413) | None found |
| HUBSET framing | `hubset.yaml:20,25-26`: "in clock mode, D[31]" | The top bits pick the circuit (SD:2600-2606) | Done with §6's table |
| GETRND | `spin2/methods/getrnd.yaml:5,12,101,113,119,138,141`: true random, cryptographic | PRNG (P2D:6442-6447); `spin2/concepts/random_generation.yaml:16` says so | New: not in the analysis |
| COGINIT resets | `complete-system-registers-index.yaml:145,157,265-266`; `dira-dirb-registers.yaml:112` | No source. Marked not documented now; settled by bench arm I (§9, §11) | None found |
| TRGINT and STALLI | `trgint1..3.yaml:12,:29`: "regardless of STALLI mode" | Conflict: CSV:328 against SD:2272,:2353. Settled by bench arm H. **Stays as is until then**, since it quotes a source | Assembly `instructions-t.md:434,448`, `appendix-c-categorical-index.md:443-445` (§13) |

**Verify.** Normal: each new wording matches its source at the line. Edge: class searches by meaning
find no sibling, including paraphrases the surveys' phrase greps could miss. Error: the release audit's
row-by-row comparison of any restated table (SD:2498-2512, SD:2600-2606, DS:1827-1841). Gates:
`verify-yaml-format.py`, `audit-yaml-claim-sourcing.py`, `audit-constant-fidelity.py`.

## 2. Compile proofs

**Why.** Encoding facts are not stated in words in any source. **Measured here** with `pnut-ts` 1.55.10
(scratch, listings decoded). Each record names a small program and its decoded words.

| Record | Proves | Measured |
|---|---|---|
| CP-031 | Branch units | 20-bit JMP/CALL/CALLA/CALLB bytes; 9-bit instructions; LOC longs in cog, bytes in hub; `##` S-branches 18-bit (cog and hub) |
| CP-032 | PTR expressions | `ptra++` `161`, `++ptra` `141`, `ptra--` `17F`, `--ptra` `15F`, `ptra[3]` `103`, `ptra[-20]` `12C`, `ptrb[31]` `19F`, `ptra++[16]` `160`, `ptra--[16]` `170`; `ptra[##1000]` `$8003E8`, `ptra++[##1000]` `$B003E8` |
| CP-033 | TESTB and BITx | Same opcode. `bitl` none or WCZ; `testb` WC or WZ. **`bitl x,#1 wc` and `testb x,#1 wcz` are both refused**, so the assembler enforces the split |

`COMPILE-PROOFS.md:21` gives CP-031 as next. Starting point: no CP covers these, and the YAML states the
units only on `tjs.yaml:14-16` and three siblings.

**Verify.** Normal: each program is versioned beside its record and recompiles to the same words. Edge:
both signs and both execution spaces (cog and hub) for each branch form, and `ptra++[16]` (`160`), the encoding
whose index is `00000`. Error: the CP-033 program keeps both refused lines as separate files, and each
must fail to compile. Compiler output proves encoding, never what silicon does.

## 3. Addressing

**Why.** Agents hand-write branches and pointer expressions, and the units differ by form. This extends
the addressing work behind v1.25.3 to v1.25.5.

- **`branch_addressing.yaml`, new `offset_units`,** keyed by form: `#` 20-bit (bytes), `#\` (address), LOC
  (longs in cog, bytes in hub), 9-bit S (instructions, times four in hub; SD:690,:5566), `##` S
  (SD:5571-5575), `CALLD` (bench arm A). A footer states the Spin2 object-offset rule and links
  `hub_address_resolution`.
- **43 S-branch pages** gain one line in `tjs.yaml:14-16`'s wording and a link. The set is 47: the `djz`
  to `tjv` family with `callpa` and `callpb` (15) and the event jumps (32). `tjs`, `tjnf`, `tjns` and `tjv`
  already carry the line (the set is defined in Planning Gate 4, with its command). `tjs`, `tjnf` and
  `tjns` say "20-bit signed", which is reconciled with arm B. Until arm B answers, the 43 pages say only
  what CP-031 proves (9-bit S in instructions, times four in hub) and say nothing about `##` S-branches.
  If arm B shows the 18-bit field lands correctly, the `##` line is added; if it shows it does not, the
  pages carry the trap and how to write around it.
- **`loc.yaml:13`** gets its unit.
- **`addressing_modes.yaml`, new `ptr_expression_encoding`:** layout `%1SUPNNNNN`, index widths, `00000` =
  16, the forms table, and the augmented form (SD:3164-3205, :3245-3252).
- **`setq_block_ops.yaml`, new `ptrx_with_block_transfers`:** the index is overridden and the pointer moves
  by the block (SD:3283-3298; EF-067), linked from the errata entries.
- **`rep_instruction.yaml`:** one link for REP in hub. The analysis's ADD row is already satisfied
  (`cog_hub_execution.yaml:32-34`, `instruction_skipping.yaml:107-108`).

**Verify.** Normal: every table row has a CP or source. Edge: `ptra--[16]`, `##` negative, cog and hub.
Error: `audit-kb-code-compiles.py` on all changed blocks; the units table is compared row by row with
the listings.

## 4. Registers and prefixes

**Why.** A prefix (SETQ, ALTx, AUGS) changes the instruction after it, and an agent that misjudges how
long that lasts writes code that works only by accident. Starting point: `special_registers.yaml:42-47`
gives no lifetime for Q and reads it with the wrong instructions (§17.2). `alti.yaml:5` names the mask
and control fields but not the codes. `testb.yaml` (50 lines) never names the shared opcode.
`instruction_skipping.yaml:113` covers absolute branches but not a plain JMP.

- **Q's life, `special_registers.yaml`:** what ends it (SD:1181-1187), what the next instruction gets
  (SD:1196), and the span uses (SD:60-62). Linked from `setq`, `setq2`, `rdlut`, `getxacc`, `xoro32`,
  `crcnib`, `qdiv`, `qfrac`, `qrotate`, `coginit`, `muxq`.
- **ALTI, `alti.yaml`:** new `src_operand` with the mask sizes (SD:618-626) and control codes (SD:628-650).
- **TESTB and BITx, `testb.yaml`** with links from the eight `bit*` pages: CP-033.
- **Skip and JMP:** a plain JMP shifts the pattern like any instruction (SD:789), and SKIPF runs through
  relative branches (SD:891). Stated in `instruction_skipping.yaml`; no bench.

**Verify.** Normal: the ALTI table matches SD row by row. Edge: the Q entry says nothing unsupported
about XBYTE until arm G. Error: the interpreter's own uses of Q (`INT:406`) do not contradict the entry.

## 5. XBYTE

**Why.** Agents writing a bytecode engine need the index the hardware actually computes, and whether a
return pops. Starting point: `xbyte_engine.yaml:118-134` describes the index-form bit in words, with no
formula, and `:42` and `:248` are §1's defects.

In `xbyte_engine.yaml`, in the same pass as §1's two fixes: the compressed-index formula (SD:998-1001,
confirmed by INT:7,:406), and that a return to `$1FF` does not pop (SD:897), noting that `INT:2950`'s
"pops" means the next return.

**Verify.** Normal: worked example from `_ret_ setq #$1A1`. Edge: both sides of the `%BBBB` split. Error:
the XBYTE guide agrees, or §13 lists the difference.

## 6. HUBSET, PRNG, events, GETBRK

- **`hubset.yaml`:** one `operand_modes` table (SD:2600-2606); the `%0010` row points to `hub.yaml:39-53`,
  which stays the home for L, W and D; `prng_seeding` (P2D:6442-6447). The Hardware Manual (`:525`) says
  "all bits of D" where the Silicon Doc says `{1, D[30:0]}`; with D's MSB required high, the two give the
  same value, so there is no conflict to state.
- **`event_system.yaml`, new `event_clearing`:** one table from the PASM2 Manual's event text
  (`pasm2-manual-text.txt:3288-3450`). Its QMT sentence at `:3367` names the wrong event, so that row
  comes from `SD:2209` and the manual slip is recorded in `SOURCE-ERRATA`. Links go from the 63 event
  instruction pages: the 16 `poll*` pages, the 15 `wait*` event pages (all except `waitx`) and the 32
  event jumps. None links `architecture/event_system.yaml` today
  (run from `deliverables/ai/P2/language/pasm2`: `(ls poll*.yaml wait*.yaml; <the event-jump ls of
  Planning Gate 4>) | grep -vx waitx.yaml` gives 63, and piping that to `xargs grep -l
  architecture/event_system.yaml | wc -l` gives 0). This replaces the earlier "21 pages holding the sentence",
  which had no command behind it.
- **`getbrk.yaml`:** state codes and the 16 event-trap bits (SD:2527-2593). `P2D:6018` has a typo, so
  `SD:2591` is the citation.

**Verify.** Normal: both tables row by row. Edge: `D[31]` seeding beside the clock-mode rows. Error: no
cell says more than its source about which events cog start clears (only ATN, INT, QMT, XRL).

## 7. Smart pins, CORDIC, bit rules

- **`smart_pins.yaml`, `z_register.reset_preload`:** a table of "During reset (DIR=0)" values (SD:3918,
  :3929 to :4254). ADC, USB, sync RX and async RX are stated as not documented; no bench.
- **Async TX `buffering`:** one-word buffer ahead of the shifter (SD:4696-4705).
- **Wrap sentence on 11 pages:** `dirh`, `dirl`, `dirc`, and the eight `out*` pages, from
  `pasm2/concepts/basic-io.yaml:165-170`.
- **Reading a driven pin:** IN returns the pin's read state, three clocks old (SD:3706; DS:1032,:1067,
  :1076). Goes to `io_pin_timing.yaml`.
- **CORDIC overwrite rule, `cordic.yaml`:** DS:924-926, SD:3413, EF-053.
- **Pixel mixer, new page:** formula and Table 13 (SD:1214-1255), seven clocks (SD:1200).
- **`rgbsqz`, `rgbexp`, `crcbit`, `crcnib`:** bit rules (CSV:155-156,:411-412). CRCNIB's bit order waits
  for arm O.

**Verify.** Normal: Table 13 row by row. Edge: `RGBSQZ`'s source concatenation is 31 bits, stated as
D[31:16] = 0 only after checking it. Error: nothing in the reset table goes beyond its mode's line.

## 8. Findability

**Why.** Chip listed as guesses things the KB states. **Measured:** 0 of 22 interrupt-control pages link
`architecture/interrupts.yaml`, 0 of 40 pin pages link `architecture/io_pin_timing.yaml`, neither page
has an `aliases:` block, and `p2kb_find latency` returns 0. Aliases are harvested, plural `keywords:` is
not (`generate-p2kb-index.py:130-242`).

**Target.** Aliases on both pages (`latency`, `pin timing`, `OUT to pin`, `interrupt priority`, and so
on), `related:` links from the 62 pages (BRK, COGBRK, GETBRK to `debug_interrupt.yaml`), and the same
treatment for pages this sprint adds. The 62 are named in Planning Gate 4 with the command that counts
them. Starting point: `interrupts.yaml` and `io_pin_timing.yaml` have no `aliases:` key
(`grep -c '^aliases:'` gives 0 for each). `wrpin.yaml:122-138` is the pattern for the `aliases:` block,
and `:139-144` for the `related:` block.

**Verify.** Normal: after a local index regeneration, each alias resolves. Edge: the natural question
"how long from OUT to the pin changing" ranks the timing page first, or its gap is recorded for the
`p2kb-mcp` ranking, which is outside this tree. Error: `validate-crossref-keys.py` reads 100%. Re-run the
live `p2kb_find` after publishing, since the server reads the published index.

## 9. The bench visit

**Why bench at all.** Each arm's sources are silent after the survey's search, correct code can depend on
the answer, and each closes a named KB cell. Stephen, 2026-11-06: *"Let's make sure they're essential,
though, and we're not just doing it for fun."* Both programs are bare board, no jumpers, reporting through
DEBUG, in one visit. Both go in `campaigns/2026-11-kb-contract-gaps/` with their `RUN-SHEET.md`, in the
form of `campaigns/2026-11-kb-findings/RUN-SHEET.md`.

**Rig rules.** Free pins only (P0-P7, P32-P47). Every arm has two sides that must come out differently, so
a stuck or non-running test cannot read as a result (*"use your dual-arm testing techniques"*, Stephen,
2026-11-06); a control that misses prints `RIG FAIL`. Each arm that can run away runs in a worker cog under
a supervisor timeout, so one bad landing cannot lose the others. Results print before verdicts.

**Program 1: instruction flow. No pins.**

| Arm | Question | Readings | Control | Closes |
|---|---|---|---|---|
| A | Does `calld pa,#far` in hub land on its label? | Marker at the label, or a marker from a sled at the byte reading of the field | Far `call` lands; a hand-encoded CALLD with a byte offset, showing which reading the silicon uses | §3 units cell; punch list item 14 |
| B | Does a backward `djnz x,##far` land correctly in cog and in hub? | Label marker, or a hub sled (cog case) | A forward `##` branch; a near 9-bit branch | §3; `tjs` wording; punch list item 15 |
| C | Does a pending SETQ survive an instruction cancelled by a false condition, or by SKIP? | Registers changed by a later plain `RDLONG`: 4 survived, 1 consumed | Adjacent `SETQ`/`RDLONG` reads 4; plain `RDLONG` reads 1 | §11 cell |
| D | Same for AUGS and AUGD | `y` = augmented or not | No cancelled instruction; no AUGS | §11 cell; extends EF-033, EF-091 |
| E | Do CALLA, CALLB, CALLD, RETA, RETB suspend a skip pattern? | Marker sum: full means suspended | CALL reads suspended (SD:791); no call reads skipped | `instruction_skipping.yaml` |
| F | Does ALTD/ALTS/ALTR apply past a skipped instruction? | `base+idx` or `x` changed | No skip; `NOP` between | §11 cell |
| G | Does `_RET_ SETQ2 #D` leave Q for the next bytecode's routine? | `MUXQ` readback `$A5` or not | Adjacent `SETQ`/`MUXQ` reads `$A5`; `QDIV` first reads 0 | §4, §11; his `_RET_` claim |
| H | Does `TRGINT1` branch while STALLI is active? | ISR count before and after `ALLOWI` | ALLOWI throughout: ISR runs | §1 TRGINT row; Assembly master |

**Program 2: cog lifecycle and data. P0-P2 only.**

| Arm | Question | Readings | Control | Closes |
|---|---|---|---|---|
| I | What survives `COGINIT` of a running cog, of a stopped cog, and of itself? DIR, OUT, C, Z, stack, PA, PB, Q, LUT, CT target, skip, REP | Each state against a never-used cog's baseline and against the dirty image | The reader sees the dirty state on a plain jump, proving it can read each class | §1 COGINIT row; §11 |
| J | Is a cog's OUT gated by its own DIR? | Cog 0 DIR=1, OUT=0; worker DIR=0, OUT=1: reads 1 independent, 0 gated. Swapped | Worker drives; no worker (`test-f361-f564-subpin-cogstop.spin2`'s arms) | §7 pin page |
| K | Which read retires a CORDIC result? | Y-only, X then Y, and X twice, identified by `QMUL k,#$FFFFFFFF` | EF-053's X-only stream; Y-then-X from `cordic_interleave.spin2` | §7 cordic |
| L | What does QDIV return when the quotient exceeds 32 bits? | `$8000_0000` wrap, saturate, or other, and the remainder | In-range quotient; EF-089 divide by zero | §7 cordic |
| M | What does GETQX return with nothing pending? | Value, and the 2-clock time (SD:3413) | A pending read beforehand | §7 cordic |
| N | What is the unit of `RDLUT`/`WRLUT` PTRx indexes and updates? | Pointer delta and value read for `ptra++`, `ptra[n]` | Known LUT contents; a hub `RDLONG` beside it | `rdlut`, `wrlut` |
| O | CRCNIB's bit order | Result against four `CRCBIT`s fed Q[31] down | The reverse order must differ | `crcnib.yaml` |

**Left out, with the reason:**

| Item | Reason |
|---|---|
| Two AUGS in a row, ALTI's I bit in other modes | No assembler output or plausible program reaches them; stated as not documented (§10) |
| XORO32 algorithm, SEUSS permutations, egg-beater phase, COGINIT start time, SETQ start-up formula | Mechanism or low programmer value; stated as not documented where an agent would ask (§10) |
| Async RX low stop bit | The state sequence answers it (SD:4727-4736) |
| RDPIN before the first result (ADC, RX) | Correct code waits for IN; stated as not documented |
| Pointer forms `--`, `++PTRx` on blocks | Stated by SD:3283-3298 |
| `XF-017`, `DT-367`/`XF-008`, `XF-006`, `XF-010`, `XF-013`, SINC2 start-up | Not this sprint's questions, and `DT-367` can kill the output. Open Question 2 |
| `VO-P-001`, `VO-X-001`, `VO-X-002` | Need external hardware |

**Prototype (all 15 arms, 2026-11-07).** Arm A: `calld pa,#landing` in hub, compiled in a full `-d`
program, gives `FE1FFC12` (R=1, A=-1006), item 14 in a runnable shape (`callddemo.spin2`). Arm B (`proto_armB.spin2`): a backward
`djnz x,##cogtop` in cog and `djnz x,##hubtop` in hub, each 300 longs back, with a forward `##` and a
near 9-bit branch as controls. Both backward words are `FF0001FF` + `FB6E6CD1` (`$3FED1`, -303), and the
forward control is `$1`. Identical fields in both spaces were not expected (punch list item 15, extended
as unexplained), and that is exactly what the arm runs to settle. Arms C to O (`proto_arms.spin2`):
every critical sequence was compiled in one `-d` program, with a supervisor that launches a worker cog
and stops it on a timeout. The words were decoded from the listing (`pnut-ts -d -l`, 1.55.10). Each
assembles as intended:

- C: `if_c mov` between `setq` and `rdlong` is `C6046A01`, with `modc _clr wc` making it false.
- D: `mov y,#$1FF` follows a pending `augs #$12345` (`FF000091`).
- E: `skip` then `calla`.
- F: `altd idx,#base` (`F98C783D`) then `mov 0-0,#7`.
- G: `_ret_ setq2 #5` is `0D640A29`.
- H: `stalli`/`trgint1`/`allowi` are `FD604224`/`FD604424`/`FD604024` (D = $21/$22/$20).
- I: `cogid`/`setq`/`coginit`.
- J: `testp #1 wc` is `FD740240`, the DIRL opcode with C set.
- K: `qmul` then `getqy` then `getqx`.
- L: `setq ##$1_0000` then `qdiv`.
- M: `getqx x wc` is `FD706A18`.
- N: `wrlut x,ptra++` (S=`161`) and `rdlut y,ptra[2]` (S=`102`).
- O: `setq`/`crcnib`/`crcbit`.

The prototype found three construction traps the run sheet must avoid:
1. P2 has no `if_never`: condition `%0000` is `_RET_`, so the compiler read `if_never` as a label. A cancelled
   instruction uses a condition made false at run time.
2. `calla #\hubsub` in a Spin2 object encodes $4FC, the assembler's own `ORGH` address and not the
   run-time hub address.
3. `coginit x,##@relaunch` encodes $108, the object offset. This is F-640's class, so arms E
   and I take their hub addresses from Spin2 (`@label` at run time) or use relative forms.

The prototypes are in `campaigns/2026-11-kb-contract-gaps/prototypes/`. The run sheet's full programs
are built from them and compiled before hand-over.

**Verify.** Normal: both arms of each question come out differently and the log's `DOWNLOAD TO RAM` line
names the binary. Edge: a landing outside the expected markers reports its address. Error: if an arm's
control misses, stop and confirm the measurement, fix the rig, re-run; the arm reports nothing until it
passes. Accepted results go to `P2-EMPIRICAL-FINDINGS.md` from EF-106, with each `.spin2` tracked in the
campaign folder.

## 10. What we state as not documented

**Why.** Where no source speaks, saying nothing hides the gap: an agent cannot tell "not covered" from
"nothing to say". Stephen, 2026-11-07: *"no questions to chip, we resolve things ourselves"*. Starting
point: none of the files below says "not documented" for these items today. Each item is closed by a
source, a compile proof, a bench arm, or a plain "not documented" on the page an agent would read:

| Item | Closed by |
|---|---|
| CALLD far field, `##` 18-bit S field | Bench arms A, B; the compiler side stays on the punch list (items 14, 15) |
| TRGINT under STALLI | Bench arm H |
| Async RX stop bit | SD:4727-4736 |
| Two AUGS in a row, ALTI's I bit in other modes | "Not documented" in `augs.yaml` and `alti.yaml` |
| XORO32 algorithm, SEUSS permutations, egg-beater phase, COGINIT start time, SETQ start-up formula | "Not documented" on `xoro32.yaml`, `seussf.yaml`, `seussr.yaml`, `hub.yaml`, `coginit.yaml`, `setq_block_ops.yaml`, only where a programmer would ask |

**Verify.** Normal: each "not documented" sits on the page an agent reads for that question. Edge: none
contradicts a source found later in the sprint. Error: no item is closed by inference.

## 11. The cog-state page

**Why.** The state a cog carries between instructions decides whether code works, and these facts have
no single home: the walk found COGINIT described wrongly at `spin2/methods/coginit.yaml:134-135`, and
`complete-system-registers-index.yaml:145,157` says "Cleared on reset and COGINIT" with no source.

**Decided** (one canonical home). `architecture/cog_state.yaml`: each piece of state a cog holds (flags, Q, stack, pending
ALT and AUGS, skip pattern, REP, events), what sets it, what consumes it, what ends it, and whether COGINIT
resets it. Cells come from sources (SD:398,:404,:2129,:2195,:2202,:2209,:2276,:2343,:2423,:3698, P2D:764;
EF-096, EF-105) and arms C, D, F, G, I. A cell with no answer says "not documented". The `system-registers`
COGINIT lines point here.

**Verify.** Normal: every cell has a source or EF. Edge: restart in place against a free cog. Error: no
cell infers from a neighbouring state.

## 12. The v1.25.6 held work

**Decided** (Stephen's 2026-11-06 hold, released when the documents shipped on 2026-11-07).
`engineering/tools/validation/audit-kb-pending.py --session` lists F-640 as held. Its three parts:

- **F-640:** `spin2-pasm2-integration.yaml:359,362,363` jump with `#\@sym` in a Spin2 object. The fix
  follows the object-offset rule in §3.
- **The sweep by operand:** search by operand form (`#\@`, `#@`, `##@`, `@@` and the rest) across the KB
  and every document master, rather than by spelling. It runs over §3's pages and every file in §17.
- **The whole-page record as a gate:** the pre-tag gate reads §16's certification record and fails
  when a file in the release diff has no row. It needs a negative control: a release diff with one
  uncertified file must fail.

**Verify.** Normal: `audit-kb-pending.py --session` reads no undecided KB entry, and the gate passes on
the real release diff. Edge: a file touched only for a `related:` link still needs its row. A file the
release deletes needs none. Error: the gate fails its negative control (one uncertified file in the
diff), and F-640's fix compiles in a Spin2 object under `audit-kb-code-compiles.py`.

## 13. Manual masters

**Decided** (Stephen, 2026-11-07). This sprint changes YAML only. No master is edited and no manual is
released. When a YAML fix is seen to reach a master, a row goes into
`engineering/planning/P2KB-CONTRACT-GAPS-MANUAL-REACH.md` at that moment, rather than in a separate
audit afterwards. A focused manual effort after the KB release applies the list to every affected
master. Reach measured so far:

| Master | Change | Waits on |
|---|---|---|
| Assembly `opus-master/part-ii/instructions-b.md:311` | BRK bit order | None |
| Assembly `opus-master/part-ii/instructions-t.md:434,448`, `opus-master/part-iii/appendix-c-categorical-index.md:443-445` | TRGINT wording | Arm H |
| XBYTE `opus-master/xbyte-body.md:822,1113` | Flags from the index (`:917` is already right) | None |
| Assembly `opus-master/part-ii/special-registers.md:501` | "Write-only … no instruction reads it back": SD:1191-1194 reads Q with MUXQ | None |

The walk's confirmed errors were searched in all 14 masters on 2026-11-07, by their YAML phrasing and
a few meaning searches (Q reading, RETI flags, LOCKTRY, streamer syntax, `HUBSET #$F0`, bandwidth, FIFO
wrap, loader inversion). Only the `special-registers.md` row was found, and that search was not
exhaustive. From here on, reach is noted as each YAML fix is made, with no separate re-audit.

**Verify.** Normal: every YAML fix whose claim appears in a master has a row in the reach notes before
the KB release. Edge: a master that already states the corrected fact gets no row. The Assembly master's
`opus-master/part-ii/instructions-r.md:284` already gives 9-16 and 9-26 cycles. Error: `git diff --stat`
over `engineering/document-production/manuals/` shows no change in this sprint's commits.

## 14. Release

`release-yamls` end to end: `audit-kb-pending.py --session`, content commit as one change set with
`P2KB_KB_RELEASE`, §1.5 change-set audit with every changed page read whole, Stephen's review, version, then
the published `p2kb_find` and `p2kb_get` probes. The bump is proposed then (additive, so likely minor); it
is his.

**Why.** The fixes reach agents only when published, and a release is the one point where the whole
change set is audited. Starting point: KB v1.25.5 is the latest tag, with nothing uncommitted under
`deliverables/ai/P2/` (`audit-kb-pending.py --session`).

**Verify.** Normal: `validate-dod-release.py` passes, the changelog is written from the diff in the
voice of `central:changelog-voicing`, and live probes confirm one fix and one alias. Edge: the probes
run more than five minutes after the push, outside GitHub raw's CDN window (F-571's release-day note).
Error: the change-set audit's agents report any hunk that is not wanted, warranted, correct and
complete, and the release waits until each is fixed.

## 15. The Silicon Doc walk (research, before the gate)

**Why.** Reading a YAML file finds what is wrong in it, not what is missing from it. The Silicon Doc is
the source behind most of the missing facts, so it is walked section by section from the source side.
Chip's list was one walk; this one is ours, done completely.

**How.** SD (5,625 lines) is split at its own headings into eight ranges, each read by a fresh agent.
For every fact a programmer could depend on, the agent records the SD lines, the fact, whether it is
contract or mechanism, its YAML home (`file:line`) or NOT CARRIED, and whether the YAML matches. Every
NOT CARRIED and every mismatch is hand-checked at both ends before it enters this plan: the agents'
rows are claims. Mechanism rows are recorded and not carried, under the entry test (Planning Gate 1).

**Output.** `engineering/ingestion/sources/silicon-doc/SILICON-DOC-CARRIAGE-LEDGER.md`, a source's own
ledger, not an edit to the source. Confirmed mismatches join §1; confirmed gaps join the section that
owns their area, or a new section.

**Verify.** Normal: every SD heading appears in the ledger with a disposition. Edge: facts the plan
already lists are marked as such, not counted twice. Error: a sample of MATCH rows is re-read by hand,
since a wrong MATCH hides a defect.

## 16. Whole-file certification

**Why.** Each YAML file the sprint touches is read whole against its sources, not just its changed
lines. 175 files are known to be touched before §17's packages add theirs, and 91 of them are mostly
unchanged since August-September 2025 (Planning Gate 4 gives the command).

**Size and split.** Certification runs inside each work package, over that package's files, so no
single pass reads all 175 or more. The §1.5 change-set audit already splits by file group, and each group
also samples its certification rows. The sprint stays one release. Its size is the reason the change-set
audit runs per package as each finishes, rather than once at the end.

**What certified means.** Every claim in the file is checked against a source line, a compile proof or
an EF/XF result. A claim with no support is corrected or stated as not documented. Fixes happen in the
same pass (the KB carve-out). The file gets one row in a certification record: file, date, sources
read, result. The record is what lets the process plan count what is left.

**Design decision to flag.** The record is a new file, `engineering/operations/YAML-CERTIFICATION-RECORD.md`.
§12's pre-tag gate reads it (Stephen's held item). The process plan extends it to the founding files.

**Verify.** Normal: every file in the release diff has a row. Edge: a file touched only for a link is
still certified whole. Error: the §1.5 change-set audit samples certified files and re-checks claims
the release did not change.

## 17. Silicon Doc walk findings

**Why.** §15 ran on 2026-11-07. Its ledger is
`engineering/ingestion/sources/silicon-doc/SILICON-DOC-CARRIAGE-LEDGER.md`, with row-level detail in
`carriage-walk-2026-11-07/range-1.md` to `range-8.md` beside it. Of 622 rows: 387 MATCH, 94 PARTIAL, 51
MISMATCH, 53 NOT CARRIED, 37 already in this plan. 26 findings were hand-checked at both ends and all were
confirmed. The ledger lists them.

**The range files are part of this plan.** Each package's row list is the `## Ledger` table of its
range file, with the YAML starting point, the SD line and the finding in each row. The `## Findings`
section gives the target for each contract row. The counts were re-measured from the tables on
2026-11-07, counting the disposition column of `## Ledger` rows only (a plain grep for "MISMATCH" also
counts the Findings sections). Per range, MISMATCH and NOT CARRIED: 7/5, 5/2, 4/16, 3/4, 7/7, 9/2,
12/10, 4/7. They are reported per package as each closes.

**Work, by area.** One package per range. Each takes every MISMATCH and contract NOT CARRIED row in its range
file, and every PARTIAL row on a file it touches, under §16:

| Package | Range | Main files |
|---|---|---|
| 17.1 Cog start, registers, hub exec, MODCZ | 1 | `spin2/methods/coginit.yaml`, `special_registers.yaml`, `hub.yaml`, `modc`/`modz`/`modcz` |
| 17.2 Q, EXECF, REP in hub, XBYTE details | 2 | `special_registers.yaml`, `branch_addressing.yaml`, `rep_instruction.yaml`, `xbyte_engine.yaml` |
| 17.3 Streamer, colorspace converter, DVI | 3 | `streamer_smartpin_control.yaml`, `nco-timing.yaml`, `setxfrq.yaml`, `architecture/streamer.yaml`; colorspace and DVI are new blocks or a new page, decided by where an agent looks |
| 17.4 RETI/RESI flags, clock switching, interrupt rules, event flag clearing on 25 Jxxx pages | 4 | `reti*`, `resi*`, `clock_system.yaml`, `hubset.yaml`, `interrupts.yaml`, the J pages |
| 17.5 LOCKTRY, FIFO wrap and sizes, FIFO sharing | 5 | `locks.yaml`, `hub.yaml`, `fifo.yaml` |
| 17.6 Smart pin repository, RDPIN rules, mode examples | 6 | `smart-pin-00001-…`, `wypin.yaml`, `rdpin.yaml`, `rqpin.yaml`, the `10101` and `01111` pages |
| 17.7 ADC, USB, async examples | 7 | `smart-pin-11000-…`, USB pages, async TX/RX pages |
| 17.8 Serial loader, opcode sharing, MODCZ symbols, BYTE/WORD/LONG `[count]` | 8 | `serial_loader.yaml`, `testp*`, `dir*`, `getbrk`/`cogbrk`, `testb.yaml` |
| 17.9 Source errata | 1, 7, 8 | `engineering/ingestion/SOURCE-ERRATA.md`: SD R-bit legend, LOCKREL typo, ORG limit, booter prose's P60 fast-boot pull-up against SD Table 36 and the Hardware Manual (SD:4805, range 7); Hardware Manual loader inversion |

**Rule for each row.** Re-find it by content: the agents' YAML line numbers can be wrong. Confirm it at
the SD line and the YAML line. Then fix it, or state it as not documented. A row that does not hold is
recorded in the range file as refuted, with the reason.

**Not blank after all (checked 2026-11-07).** The range 5 agent reported SD:3032-3037 and SD:3259-3298 as
blank. They are not. The text extraction carries the RDFAST/WRFAST/FBLOCK operand layouts (SD:3028-3037)
and the block-move pointer forms (SD:3283-3298). Both match the PDF (`pdf-layout` of Part 3, lines
862-880 and 1095-1150) word for word. Those rows are compared like any other in 17.5. The smart-pin
schematics are images of the pin circuit, the analog mechanism behind the mode text. The modes a
program selects are all in the text, so the schematics carry no contract row.

**Async TX examples (range 7, unexplained).** The examples on `smart-pin-11110-…:65,:94` and
`smart-pin-11111-…:162,:167` wait for IN before the first WYPIN. By SD:4700-4701, IN rises only once a
written word moves to the shifter, and no source or EF gives IN's state before the first write. **No
bench:** correct code need not depend on that state. The examples are rewritten to the SD sequence, which
writes and then waits for IN before each later write, or polls busy with `RDPIN … WC` (SD:4707). IN's
state before the first write is stated as not documented. EF-016 (first-byte glitch, not observed) stays
as it is. **Whose call:** bench contents are Stephen's. This case was put to him before he chose the bench
(the 2026-11-07 walk report: "We can fix it without the bench by rewriting those examples in the order
the Silicon Doc gives"). He then answered *"all 15 as planned"*, a list without it, under his 2026-11-06
rule that a bench run must be essential. Sources being silent is necessary for a bench run, not
sufficient.

**Verify.** Normal: every MISMATCH and contract NOT CARRIED row is closed in its range file, with the
fix's file and line. Edge: a row whose fix is already covered by §1-§11 is closed against that section,
not fixed twice. Error: changed code examples pass `audit-kb-code-compiles.py`, and the change-set audit
re-reads a sample of MATCH rows.

---

## Documentation Blast Radius

Run 2026-11-07, `python3 engineering/tools/validation/audit-guide-conformance.py --inventory`:

```
PASS  guide layer conformant across 49 file(s)
```

| Behaviour | Artifacts that describe it |
|---|---|
| Every fact in §1 to §11 | The YAML pages above, and `CHANGELOG.md` in the KB voice |
| Release state | `README.md` badge, `YAML-HEAD-DASHBOARD.md`, `engineering/README.md` YAML row |
| Counts | `yaml-knowledge-base-maintenance` §2.6 and §2.7 tree totals move with new pages and blocks: refresh or leave as dated readings |
| Compile and bench records | `COMPILE-PROOFS.md`, `P2-EMPIRICAL-FINDINGS.md`, `VERIFICATION-OPPORTUNITIES.md` |
| Compiler behaviour | `DRAFTS/PNUT-TS-PUNCH-LIST.md` items 14, 15: closed or sent on, per arms A, B |
| Manuals | Not changed in this sprint; reach recorded in `P2KB-CONTRACT-GAPS-MANUAL-REACH.md` for the manual effort that follows (§13) |
| Analysis | It carries a pointer here; its counts stand as what was measured then |
| Release procedure (§12, §16) | `.claude/skills/release-yamls/SKILL.md` (§1.5 certification sampling, §5.5 check count "30 checks" moves to 31), `.claude/skills/yaml-knowledge-base-maintenance/SKILL.md` (certify whole files and write the record row), `engineering/operations/PROCESS-DOC-CATALOG.md` (new record and gate), and `engineering/operations/YAML-CERTIFICATION-RECORD.md` itself |
| Bench prototypes | `campaigns/2026-11-kb-contract-gaps/prototypes/` (§9) |
| Silicon Doc walk | `SILICON-DOC-CARRIAGE-LEDGER.md` and `carriage-walk-2026-11-07/` (§15, §17); `engineering/ingestion/SOURCE-ERRATA.md` (§17.9) |

---

## Planning Gate

**Verdict: MET (2026-11-07).** Every Open Question is answered, and the audit record is at the end of
this section.

1. **Standing rulings.** Applied here, all 2026-11-07 unless dated: the scope above; *"no questions to
   chip, we resolve things ourselves"* (§10); *"yes, the shape you recommend"* (two plans, §15-§16);
   *"You just make the commits when you need them"* (commits ours, pushes his); *"Isn't this your
   decision based on content that we need to record in files?"* (where content lives is ours, §11);
   *"all 15 as planned"* (§9); YAML first and manuals after (§13); *"yes as recommended as long as it is
   sourced and proven fact"* (aspect 3; every change in this sprint rests on a source line, a CP or an
   EF/XF). Earlier: 2026-11-06 *"essential"* and *"dual-arm"* (§9); 2026-11-06 F-640 held "documents
   first" (§12); 2026-10-12 *"you are not allowed to make scoping decisions on your own"*, read with
   2026-11-07's clarification above; 2026-08-26 *"All we want to know is that TAQOZ exists, how you get to it, and what it is
   useful for"* (the entry test); 2026-08-21 *"We do not publish a release unless all the code publishes
   correctly"*; 2026-10-05 review before release; J-1 ruled 2026-11-04, new traps use `anti_patterns`.
   Also the HDL study is indicator-only and was not used; provenance is not served; bench only where
   sources are silent; no version stamps in served text.
2. **Intent.** Asked in his words, quoted at the top; done is stated and awaits his correction.
3. **Decisions and open items.** Open Questions 1 to 7 are resolved above, with his words. The
   register's 19 open entries were shown to him as a group on 2026-11-07 (*"yes as recommended as long as
   it is sourced and proven fact"*). F-640 joins (§12). Declined this sprint, visibly: F-642, F-641,
   F-424, F-280, F-316, F-317, F-301 and F-300 go to the manual effort after the KB release. F-344,
   F-332, F-341 and F-367 go to the process plan. F-562, F-566 and F-354 stay held for his action or a
   document. F-571 stays with the p2kb-mcp server. F-299 stays as platform polish, and F-418 keeps the
   scope decision it already owes. These are the per-group dispositions as the question put them to him.
   His answer accepted them as written, so each entry's disposition is his. The question is in this
   conversation's record of 2026-11-07.
4. **Premises.** Each was measured on 2026-11-07, with its command (paths from the repository root;
   `P` = `deliverables/ai/P2/language/pasm2`):
   - `python3 engineering/tools/verify-yaml-format.py` gives "All YAML files parsed cleanly".
   - `python3 engineering/tools/validate-crossref-keys.py` gives "ALL CROSS-REFERENCES RESOLVE — 4326
     checked". The earlier "2585/2585 and 1741/1741" was a stale figure and has been replaced.
   - `python3 engineering/tools/validation/audit-kb-pending.py --session` gives 8 entries, the latest
     tag v1.25.5, and 0 uncommitted. `COMPILE-PROOFS.md:21` gives CP-031 next. The ledger's highest
     entry is EF-105.
   - **S-branch set, 47:** `ls` of the 15 named files (`djz djnz djf djnf ijz ijnz tjz tjnz tjf tjnf tjs
     tjns tjv callpa callpb`) gives 15. `ls $P/j*.yaml | grep -E '/j(n)?(int|ct[123]|se[1234]|pat|fbw|xmt|xfi|xro|xrl|atn|qmt)\.yaml$'`
     gives 32. Over those 47, `grep -lE 'whole instructions|-256'` gives 4: `tjs`, `tjnf`, `tjns`,
     `tjv`. (`calld.yaml` also matches, but it is outside the set.) So 43 change.
   - **Findability, 62:** the 22 interrupt pages are `setint1-3 trgint1-3 nixint1-3 allowi stalli reti0-3
     resi0-3 brk cogbrk getbrk`, and 0 contain `architecture/interrupts.yaml` (grep). The 40 pin pages
     are the 32 `dir/out/flt/drv × l h c nc z nz rnd not` pages plus `testp testpn wrpin wxpin wypin rdpin
     rqpin akpin`, and 0 contain `architecture/io_pin_timing.yaml`. `grep -c '^aliases:'` gives 0 on both
     architecture pages.
   - **`bits` fields:** `grep -h '^- bits: ' $P/*.yaml` gives 407, and the same lines stripped of spaces
     give 0 that are not 32 characters.
   - **Certification size:** the files are listed in `engineering/planning/P2KB-CONTRACT-GAPS-CERTIFY-LIST.txt`,
     one path per line, relative to `deliverables/ai/P2/`. The list is the union of the file table, the
     47 S-branch pages, the 62 findability pages, the 32 `dir/out/flt/drv` pages, the `bit*` and pixel
     pages and §4's link pages, filtered to files that exist. `wc -l` gives 175. Founding count, run from
     `deliverables/ai/P2/`: `while read f; do t=$(wc -l < "$f"); o=$(git blame --date=short "$f" | grep -c
     ' 2025-0[89]-'); [ $((o*2)) -gt $t ] && echo "$f"; done < <list> | wc -l` gives 91. A file counts as
     founding when more than half its lines carry an August or September 2025 blame date. §17's packages
     add their files to the list as they start. The list is a recorded artifact, committed with this
     plan.
   - **Walk counts:** the disposition column of each range file's `## Ledger` table (awk over the
     table rows) gives MISMATCH 51 and NOT CARRIED 53.
   - **Rig:** Stephen chose *"all 15 as planned"* on 2026-11-07 from a question that described two
     bare-board programs, "using no jumpers and only free pins", with Program 2 on P0-P2. The free pins
     are his standing rule (memory `reference_bench_free_pins`: P0-P7, P32-P47).
5. **Research.**
   - **The Silicon Doc walk** (§15, §17): 622 rows over the whole source, with 26 findings hand-checked at
     both ends and all confirmed. The rest are confirmed by content before each fix, under §17's rule.
     The walk changes no bench arm.
   - **Class search by meaning:** for every Silicon Doc-sourced row, the walk is that search, since it
     searched each fact under several phrasings. For §1's rows with other sources, a meaning search was
     run on 2026-11-07:
     - "cryptograph", "true random" and "hardware random" are claimed only by `getrnd.yaml`.
       `op_rand`, `xoro32` and `random_generation` say the opposite.
     - "regardless of STALLI" appears only in `trgint1..3`.
     - The 9-24 and 3-12 timings appear in our own text only in `cog_hub_execution.yaml`. Two OBEX
       mirrors, `5285` and `2850`, also contain them; they mirror the catalog and are not ours to edit.
   - **Risky designs prototyped:** all 15 arms (§9), which found three construction traps; and the CP
     programs (§2).
   - **Order against the debug toolbox:** «#435» says it "runs after the urgent YAML release", and
     «#436» and «#437» follow it. This sprint is that YAML release, so it runs first and the toolbox
     batches start from its tag. The order is settled here; `sprint-start` only re-checks it.
   - **The preview:** a clean baseline, with untracked evidence files committed with this plan.
6. **Named unknowns.** Bench outcomes: each arm says what changes either way. A silicon
   result proving the compiler wrong for CALLD or `##`: the KB states the silicon behaviour and how to write
   around it, and punch list items 14 and 15 go to the compiler. The natural-question ranking: if a fix needs
   the server, it goes to the `p2kb-mcp` agent. Arm B: §3's S-branch pages carry only what CP-031 proves
   until it answers, then gain the `##` line or the trap. Async TX initial IN: stated as not documented,
   with examples that do not depend on it (§17). Walk rows that do not hold on confirmation are recorded
   as refuted in their range file, and the package continues.

**Audit, round 1 (2026-11-07, fresh `task-survey` agent, brief `references/gate-audit-brief.md`).**
Verdict: GATE NOT MET, with 3 BLOCKS-GATE, 6 SHOULD-FIX and 3 MINOR findings. It sampled 33 citations
and found none wrong. Each finding was hand-checked, then resolved:
1. BLOCKS, risky designs deferred: all 15 arms were prototyped and decoded (§9); the meaning search was
   run (aspect 5); the toolbox order was settled (aspect 5).
2. BLOCKS, premises: crossref was re-run and the stale figure replaced. Commands were added for every
   count, and the `calld.yaml` exclusion is stated. Rig: his words quoted (aspect 4).
3. BLOCKS, dispositions: Open Question 7 is struck through and resolved. Aspect 3 states that the group
   answer accepted the per-group dispositions as put to him. The async-TX bench decision is traced to
   his choice (§17).
4. Tooling: the header no longer says "no new tool"; the gate script is in the file table, cited to
   F-640's hold.
5. Blast radius: the release skills, the process catalog, the record, the prototypes and the walk files
   were added.
6. §17: the range files are made part of the plan, with counts re-measured. The "blank" spots were
   checked and are not blank. The schematics carry no contract row.
7. Completeness: why, starting points and edge and error cases were added to §2, §4, §5, §10, §11, §12,
   §13 and §14. §8 now refers to aspect 4's page sets.
8. Consistency: the TRGINT file-table row was split, and §3 states what the pages carry before arm B
   answers.
9. Size: §16 states 175 files and 91 founding, with certification and the change-set audit split by
   package.
10. Minor, paths: the `opus-master/` prefixes were added in §13.
11. Minor, aspect 1: the auditor could not check the quoted rulings. Nothing to change.
12. Minor, stops: none needed rewording.

The fixes go beyond line-level text (new premises, new section text in §9, §16 and §17), so round 2
audits them.

**Audit, round 2 (2026-11-07, fresh `task-survey` agent).** Verdict: GATE NOT MET, with 1 BLOCKS-GATE, 4
SHOULD-FIX and 3 MINOR findings. Every premise command reproduced, and the prototype words decoded as
quoted. Findings:
1. BLOCKS, arm B not prototyped though claimed. Resolved: `proto_armB.spin2` was compiled with a backward
   `##` branch in cog and in hub plus controls, and its words are in §9. The identical fields in both
   spaces were added to punch list item 15 as unexplained.
2. "21 pages" had no command. Resolved: §6 now names 63 event pages with the command, 0 linking today.
3. The 175 and 91 counts were prose. Resolved: the list file `P2KB-CONTRACT-GAPS-CERTIFY-LIST.txt` and the
   founding command are in aspect 4, and both re-ran to 175 and 91.
4. §2's edge named the wrong `00000` encoding. Resolved: `ptra++[16]` (`160`).
5. §8's aliases pattern lines. Resolved: `wrpin.yaml:122-138` for aliases and `:139-144` for related.
6. Minor, a repeated sentence in §8: removed. 7. Minor, 17.9's ranges: now 1, 7, 8. 8. Minor, the arm label
   in `callddemo.spin2`: now "side 1/side 2".

Round 2's fixes add new text (§9, aspect 4, §6), so round 3 audits them.

**Audit, round 3 (2026-11-07, fresh `task-survey` agent).** 0 BLOCKS-GATE, 1 SHOULD-FIX and 1 MINOR
finding. All eight round-2 findings were checked: seven RESOLVED, and the §6 command was NOT RESOLVED.
The auditor re-ran the commands: arm B's words at two sites in the `.bin`, 175 and 91, and the `wrpin`
lines.
1. SHOULD-FIX, §6's command counted 59: `grep -v waitx` also dropped the four `waitx*` event waits.
   Resolved: the command now uses `grep -vx waitx.yaml`. The arbiter re-ran it from `language/pasm2` and
   got 63 pages, with 0 linking `event_system.yaml`. The conclusion was unchanged by the slip.
2. MINOR, the certification list is an artifact, not a command. Resolved: it is stated as a recorded
   artifact committed with the plan.

Both fixes are one token and one sentence, each re-run here, so no further round is needed: the brief's
condition is a round with no BLOCKS-GATE finding and nothing wrong in the previous round's fixes beyond
these line-level corrections.

**Verdict: GATE MET (2026-11-07).** Three audit rounds ran; the last had no BLOCKS-GATE finding, and its
two line-level findings were fixed and re-measured.

No questions remain: **true**, on both sides.
