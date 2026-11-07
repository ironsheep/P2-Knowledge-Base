# Silicon Doc carriage ledger

**Source:** P2 Documentation v35, Rev B/C silicon (`silicon-doc-text.txt`, 5,625 lines).
**Walked:** 2026-11-07, from the source side, for `engineering/planning/P2KB-CONTRACT-GAPS-SPRINT-PLAN.md` §15.
**Question per fact:** does a YAML file under `deliverables/ai/P2/` carry it, carry it wrongly, or not
carry it?

This is the source's own ledger. The source itself is unchanged.

## How it was walked

Eight fresh agents each read one range in full, split at the document's own headings, under
`carriage-walk-2026-11-07/BRIEF.md`. Their row-level ledgers are `carriage-walk-2026-11-07/range-1.md` to
`range-8.md`. **Every row there is an agent's claim.** A row becomes a finding only when it has been
hand-checked at both ends: the SD line and the YAML line. The hand-checked rows are listed below. The
rest are confirmed the same way, by content, before each is fixed, because the agents' YAML line numbers
were sometimes wrong (range 6) even when the finding was right.

## Totals

| Range | SD lines | Area | MATCH | PARTIAL | MISMATCH | NOT CARRIED | Already in plan |
|---|---|---|---|---|---|---|---|
| 1 | 1-504 | Overview, pins, memories, modes, cog start, cog RAM, LUT | 66 | 17 | 7 | 5 | 6 |
| 2 | 505-1197 | Indirection, branches, REP, skip, XBYTE, SETQ | 49 | 6 | 5 | 2 | 8 |
| 3 | 1198-2034 | Pixel ops, streamer, colorspace, DVI, pin timing, attention | 47 | 14 | 4 | 16 | 1 |
| 4 | 2035-2865 | Events, interrupts, debug, GETBRK, clock | 55 | 9 | 3 | 4 | 5 |
| 5 | 2866-3701 | Hub RAM, FIFO, random access, block moves, CORDIC, locks | 40 | 7 | 7 | 7 | 9 |
| 6 | 3702-4253 | Smart pins: overview, configuration, first modes | 40 | 10 | 9 | 2 | 2 |
| 7 | 4254-4818 | Smart pins: remaining modes | 39 | 20 | 12 | 10 | 3 |
| 8 | 4819-5625 | Serial loader, DAT ORG, instruction summary | 51 | 11 | 4 | 7 | 3 |
| **All** | | | **387** | **94** | **51** | **53** | **37** |

Range 4 has one row that is both MATCH and in the plan. Range 5's NOT CARRIED count includes 2 mechanism
or example rows. Range 7 also has 1 UNEXPLAINED row. Range 8 compared 359 encoding lines: 353 identical
to the YAML, 4 differing only in notation, and 2 empty opcode slots.

## Hand-checked findings

All 26 findings checked so far were confirmed, as was the R-bit source erratum below. None was refuted.

| Area | Finding | SD | YAML |
|---|---|---|---|
| Cog start | COGINIT loads $000-$1F7 or starts at S; S goes to PTRB, SETQ to PTRA. The YAML says "all registers cleared except PTRA" | 376-404 | `spin2/methods/coginit.yaml:134-135` |
| Registers | $1F0-$1FF are ordinary registers; SETINTx sets an event source, not the vector | 436-470 | `pasm2/concepts/special_registers.yaml:7-9,31` |
| Hub | 32 bits per clock per cog, not "Clock_freq / 2 bytes/second" | 172 | `architecture/hub.yaml:186` |
| Hub exec | XINIT/XZERO/XCONT are barred only when the streamer mode uses the FIFO | 358 | Seven sites, to re-locate |
| MODCZ | The %0000/%1111 rule and `_CLR`..`_SET` symbols are not carried (they compile: `pnut-ts`, scratch) | 5503-5539 | `modc.yaml`, `modz.yaml`, `modcz.yaml` |
| Q | Q is read with MUXQ, not GETQX/GETQY | 1191-1194 | `special_registers.yaml:44` |
| EXECF | Jumps, then skips at the target | 786, 864 | `pasm2/concepts/branch_addressing.yaml:84,86` |
| REP | Hub REP costs a hidden jump per iteration | 773 | `rep_instruction.yaml:83-84` |
| Streamer | Mode codes `0000`-`0011` are imm to LUT | 1313-1330 | `streamer_smartpin_control.yaml:54-71` |
| Streamer | D = mode[31:16] and count[15:0]; S = data | 1282-1284, 1309, 1313 | same file `:26-30,:44` |
| DVI | Needs clock = 10x pixel rate, NCO = 1/10; the 720p values cannot work | 1751-1753 | `nco-timing.yaml:122-127` |
| Streamer | GETXACC returns the Goertzel accumulators, not a phase accumulator | 1185, 1285 | `setxfrq.yaml:81` |
| Interrupts | RETIx/RESIx restore C and Z (CALLD … WCZ) | 2294, 2306 | `reti1..3`, `resi0..3`, `reti0` `flags_affected` |
| Clock | Select %00 or %01 while the crystal or PLL settles | deglitch paragraph | `clock_system.yaml:229-249`; `hubset.yaml` recipe |
| Clock | Switch away from the PLL keeping PPPP and CC; `HUBSET #$F0`/`#$F1` clears CC, and no source states it | safe-switch warning | `clock_system.yaml:142,341` |
| Locks | The LOCKTRY example lacks WC | LOCKTRY | `architecture/locks.yaml:110-113` |
| FIFO | Wraps to its start address after D 64-byte blocks, with no power-of-2 mask | 3020-3036 | `architecture/hub.yaml:142,221-224` |
| FIFO | RFxxxx/WFxxxx move any size; the block count is in 64-byte units | 355-357, 3020 | `architecture/fifo.yaml:239` |
| Smart pins | The repository is written by WXPIN | 3914 | `multi_cog_synchronization.yaml:276`, `spin2/methods/wypin.yaml:93`, `streamer_smartpin_control.yaml:291` |
| Smart pins | PINSTART writes X during reset, so a repository loaded that way loses the value | 3918; Spin2 v55:537 | `smart-pin-00001-…:53` |
| Smart pins | RDPIN acknowledges the pin | 3720, 3847 | `smart-pin-00001-…:70` |
| Smart pins | C is the MSB of Z when a mode has no flag (source side only; YAML side searched in the fix) | 3727 | `rdpin.yaml`, `rqpin.yaml` |
| ADC | `%11000`: WYPIN overrides the period except in SINC2 sampling | 4387 | `smart-pin-11000-adc-internal-clock.yaml:32` |
| USB | IDLE has two 15k pull-downs for host, and a 1.5k pull-up for device | 4599 | USB page |
| USB | The upper pin's IN rises when the two-level output FIFO has room | 4589 | USB page |
| Loader | Plain 8-N-1, typed from any PC terminal. The Hardware Manual's "inverted" sentence conflicts, and every bench download uses standard serial | 4821, 4968 | `architecture/serial_loader.yaml:27` |

## Source errata found

| Source | Error | Evidence |
|---|---|---|
| Silicon Doc | The R bit legend gives 0 = relative | CSV:426-430 "If R = 1 then PC += A"; compiled `calld pa,#landing` is `FE1FFC12`, R = 1 relative |
| Silicon Doc | LOCKREL typo; ORG default limit | Range 8 rows; `pnut-ts` gives $1F8, as the YAML says |
| Silicon Doc | SD:4805 booter prose puts fast boot on a P60 pull-up | SD Table 36 and the Hardware Manual give a P59 pull-down, which the KB follows (range 7; to hand-check in 17.9) |
| Hardware Manual | `:1592` says loader data is inverted | SD:4821, 4968; standard serial downloads |

These go to `engineering/ingestion/SOURCE-ERRATA.md` in the sprint.

## Not compared

SD:3032-3037 and SD:3259-3298 (operand figures and block-move tables) are blank in the text extraction,
so those rows rest on the prose around them. The smart-pin schematics are images only. Both are read from
the PDF in the sprint.
