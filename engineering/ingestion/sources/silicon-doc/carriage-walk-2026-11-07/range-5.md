# Silicon Doc walk, range 5: SD:2866-3701

Hub RAM, cog-to-hub interface, fast FIFO, random access, block moves, CORDIC, locks.
KB root `deliverables/ai/P2/` (paths below are relative to it). `pasm2/` = `language/pasm2/`.

Note on the source text (corrected 2026-11-09, «#456»): SD:3032-3037 and SD:3283-3298 are not blank. SD:3028-3037
carries the RDFAST/WRFAST/FBLOCK operand layouts (D: `%xxxx_xxxx_xxxx_xxxx_xx00_0000_0000_0000` = block count for
limited read/write, `%xxxx_xxxx_xxxx_xxxx_xxBB_BBBB_BBBB_BBBB` = block count for wrapping; S: `...AAAA` start address for
limited read/write, `...AA00` start address for wrapping, long-aligned), and SD:3259-3298 carries the block-move syntax
boxes and the block-move pointer forms (PTRA, PTRA++, PTRA--, ++PTRA, --PTRA with the long count). Only the Table 31 and
Table 32/33 cell extraction is fragmented. Both were compared in «#456»: the operand layouts against `pasm2/rdfast.yaml`,
`wrfast.yaml`, `fblock.yaml` and `architecture/fifo.yaml` (now agree: D[13:0] block count, 0 = no wrapping, S[1:0] = %00 when
wrapping), and the five block pointer forms against `pasm2/concepts/setq_block_ops.yaml` `ptrx_with_block_transfers.forms`
(match row by row, «#448» text; compare only).

## Sections

| SD line | Heading | Disposition |
|---|---|---|
| 2866 | HUB RAM | Mostly IN-PLAN §1 (alignment, empty hub, top-16KB mirror). Little-endian byte order PARTIAL. FPGA table is mechanism. |
| 2997 | THE COG -to- HUB RAM INTERFACE | Slices MATCH; egg-beater wording IN-PLAN §1; FIFO depth/threshold MATCH; "one use at a time" (streamer vs software) NOT-CARRIED; hub.yaml bandwidth MISMATCH. |
| 3018 | FAST SEQUENTIAL FIFO INTERFACE | Instructions and flags MATCH; wrap alignment rule NOT-CARRIED; hub.yaml "power-of-2 / mask" wrap MISMATCH; fifo.yaml "64-byte minimum granularity" MISMATCH; RFVAR table MATCH; WAITX #20 PARTIAL. |
| 3123 | RANDOM ACCESS INTERFACE | Encodings, flags, WMLONG, immediate 0..255 MATCH; PTR encoding/AUGS forms IN-PLAN §3. |
| 3255 | FAST BLOCK MOVES | Rate, FIFO priority, filler MATCH; flags-from-last-long NOT-CARRIED; usable in hub exec NOT-CARRIED; $1F8..$1FF exclusion PARTIAL; PTRx override IN-PLAN §3. |
| 3302 | CORDIC Solver | Operation list, latency, slot wait MATCH; stall claim IN-PLAN §1. |
| 3317-3408 | MULTIPLY / DIVIDE / SQUARE ROOT / (X,Y) ROTATION / (X,Y) VECTORING / LOGARITHM / EXPONENT | All operand orders MATCH (QDIV, QFRAC, QSQRT, QROTATE, QVECTOR, QLOG, QEXP). |
| 3411 | OVERLAPPING CORDIC COMMANDS (+ Table 33 demo) | Interrupt/overwrite rule IN-PLAN §7; empty GETQX IN-PLAN §9 arm M; in-flight count "~6-7" MISMATCH against the demo's 8. |
| 3673 | LOCKS (Allocating Locks 3683, Using Locks 3687) | Semantics MATCH; LOCKTRY example missing WC MISMATCH; hub.yaml LOCKCHK MISMATCH; LOCKREL encoding conflict MISMATCH; round-robin fairness NOT-CARRIED; COGINIT release PARTIAL. |

## Ledger

| SD lines | Fact (one line) | C/M | YAML home (file:line) or NOT-CARRIED | Disposition | Note (quotes, searches) |
|---|---|---|---|---|---|
| 2868 | Hub RAM is little-endian | C | `language/spin2/assembly-directives/long.yaml:18-20` | CLOSED 2026-11-09 against «#446» (range-1 SD:173 row): `architecture/hub.yaml:18` reads "...at any hub address, in little-endian format" | long.yaml: "Longs are stored in little-endian format." Not on `architecture/hub.yaml` or any RD*/WR* page; hub.yaml:17 says only "8 bits (byte-addressable)". Searched `little.endian`, `endian`, `LSB first`, `low byte at` across the KB. |
| 2868 | No alignment rules for words/longs; any hub address | C | `architecture/hub.yaml:100,107,238` | IN-PLAN §1 | Hub alignment row. |
| 2868 | Hub exec from any hub address starting at $400 | C | `architecture/hub.yaml:171` | MATCH | "pc_range: $400-$FFFFF". |
| 2870-2872 | Top 16KB of RAM mirrored at $FC000..$FFFFF; ROM is cached into it; W hides it and makes it read-only except from debug ISRs | C | `architecture/hub.yaml:23,40-44,233` | IN-PLAN §1 (empty hub, top 16KB) | hub.yaml:41-44 protection_bit matches SD:2872 ("disappears from its normal range and is write-protected at $FC000..$FFFFF, except from within debug ISRs"). hub.yaml:23 "Boot ROM ... Mapped at $FC000-$FFFFF on boot" is the in-plan framing defect. |
| 2874 | HUBSET sets write protection | C | `architecture/hub.yaml:37-53` | MATCH | "%0010_xxxx_xxxx_xxLW_DDDD..." |
| 2876-2995 | Table 31, per-FPGA-board hub memory maps | M | NOT-CARRIED | NOT-CARRIED (mechanism); decision stands 2026-11-09 («#456»): the FPGA rows are not carried; the silicon row is served in `architecture/hub.yaml:222-233` (memory_map) | FPGA rows are development history. Silicon row (512KB, gap $80000..$FBFFF reads $00, W=1 lower RAM ends $7BFFF) is IN-PLAN §1 empty-hub row. Searched `DE0-Nano`, `BeMicro`, `DE2-115`, `FPGA`. |
| 2999 | 8 single-port slices; each slice holds every 8th long | C | `architecture/hub.yaml:75-83` | CORRECTED 2026-11-09 («#456» change-set audit): every 8th set of 4 bytes is served as stated; the `(address >> 2) & 7` formula and the numbered `slice_assignment` table were derived and are gone, replaced by the Hardware Manual's "lower 3 bits of its address" with "Not documented" for which address | The walk matched "slice = (address >> 2) & 7"; SD:2999 states no address-to-slice mapping. |
| 2999, 3001 | Each cog reaches the next slice every clock (not COG 0→1→2 window) | C | `architecture/hub.yaml:65-71` | IN-PLAN §1 | Egg-beater row. |
| 2999 | Up to 32 bits per clock per cog streaming | C | `architecture/hub.yaml:183-184` | CLOSED 2026-11-09 against «#445» («#456» re-read): the unsourced "Clock_freq / 2" and "Clock_freq / 8" lines are gone (grep `Clock_freq / [0-9]` over the KB: none); `performance.bandwidth` keeps `streaming` "32 bits per clock between the composite hub RAM and each cog, after the initial slice wait" (SD:2999) and `burst` "4 bytes per clock during block transfer". Judged by content: the lines were unsourced figures, not a random-access versus burst mislabel, so no replacement figure is given (nothing states one) | hub.yaml:186 "theoretical: Clock_freq / 2 bytes/second per COG" and :187-188 "sustained ... Clock_freq / 8 bytes/second" against :189 "burst: 4 bytes per clock" and SD:2999 "32 bits per clock". Theoretical figure is 8x below the burst rate it sits beside; sustained figures are unsourced. |
| 3001 | Initial slot wait up to cogs-1 clocks | C | `architecture/hub.yaml:87-88,189` | MATCH | "0-7 clocks"; "worst_case: 7 clocks". |
| 3003 | FIFO reads/writes bytes, words, longs in any mix, at any rate up to a long per clock | C | `architecture/fifo.yaml:9-13,30` | CLOSED 2026-11-09: the "Minimum transfer granularity is 64-byte blocks" note is gone; `fifo.yaml:9-13` states "any combination of bytes, words or longs, up to one long per clock" and "the wrap block count is in 64-byte units", `:30` the key feature | fifo.yaml:239 "Minimum transfer granularity is 64-byte blocks (streamer/software role)" against SD:3003 "in any combination of bytes, words, or longs, at any rate". The 64-byte block only sets the wrap length (SD:3020). |
| 3005 | Random accesses yield to the FIFO | C | `pasm2/concepts/setq_block_ops.yaml:199` (block moves only) | CLOSED 2026-11-09: `architecture/hub.yaml:141` (fifo_interface.features.random_access_yield) states that random accesses yield to the FIFO and have full opportunity when it is not busy | Stated for block moves ("the FIFO gets priority"). Not stated for single RDxxxx/WRxxxx. Searched `yield`, `priority`, `FIFO.*busy`. |
| 3007-3011 | FIFO serves one of hub exec / streamer / software at a time | C | `architecture/fifo.yaml:18-20,240-241` (hub exec only) | CLOSED 2026-11-09: `architecture/fifo.yaml:26-27` (description) and `:256` (limitations) state hub execution, streamer use and software use are one at a time; also `architecture/hub.yaml:140` and `architecture/streamer/overview.yaml:52` (resources_per_cog.hub_fifo) | Hub-exec exclusivity MATCH ("mutually exclusive"). That streamer use and RFxxxx/WFxxxx use exclude each other is not stated: fifo.yaml:8-10 merges them into one role. Searched `one of these at a time`, `only be used for one`, `three ways`, streamer pages for RFLONG/RFBYTE. |
| 3013 | RDFAST/WRFAST must run from cog/LUT RAM; streamer or RF/WF stay in cog RAM | C | `architecture/fifo.yaml:40-41,241`; `pasm2/hubexec.yaml:30` | MATCH | "cogexec only"; forbidden list. |
| 3015 | FIFO has cogs+11 stages; reloads below cogs+7, up to 5 more | M/C | `architecture/fifo.yaml:29-30,37-38,260-261` | MATCH | Quoted verbatim at :260-261. hub.yaml:126,140 "19-stage"/"19 longs" also consistent. |
| 3020 | D = count of 64-byte blocks before wrap to the original start address | C | `architecture/fifo.yaml:63,71`; `pasm2/rdfast.yaml:12-13,58` | MATCH | "Block count in 64-byte units"; "D[13:0] is a count of 64-byte blocks". |
| 3020 | Wrap returns to the start address with the block count (not a power-of-2 boundary or mask) | C | `architecture/hub.yaml:138,214-218` | CLOSED 2026-11-09 against «#445» («#456» re-read): `hub.yaml:138` (block_wrap) states a block count in 64-byte units, wrap to the original start address, long-aligned start; the circular_buffer example (`:214-218`) is `RDFAST block_count, hub_addr` with "block_count = number of 64-byte blocks" | hub.yaml:142 "block_wrap: Can wrap on power-of-2 boundaries"; :223 "RDFAST  mask, hub_addr    ' Mask sets wrap boundary" against SD:3020 "how many 64-byte blocks will be read or written before wrapping to the original start address". |
| 3020 | Wrapping requires a long-aligned start address | C | CLOSED 2026-11-09: `architecture/fifo.yaml:64,72` (configuration.rdfast / wrfast S_bits_19_0), `:79-80` (fblock S); `pasm2/rdfast.yaml:13,59`, `pasm2/wrfast.yaml:14,22`, `pasm2/fblock.yaml:14,18`; also `architecture/hub.yaml:138` | NOT-CARRIED | Searched `long-aligned`, `long aligned`, `ends in %00` with fifo/wrap/block context; hits are hub-exec branch costs only. Expected home `architecture/fifo.yaml` configuration, `pasm2/rdfast.yaml`, `wrfast.yaml`, `fblock.yaml`. |
| 3020 | Block count 0 = no wrap until whole 1MB map | C | `pasm2/rdfast.yaml:13,58`; `architecture/fifo.yaml:250` | MATCH | "A block count of 0 means no wrapping until the entire 1MB hub map has been sequenced through". |
| 3022 | FBLOCK sets next start and count, taken at wrap; usable after RDFAST, WRFAST, or a wrap event | C | `architecture/fifo.yaml:68-73,148-157`; `pasm2/fblock.yaml:12` | CLOSED 2026-11-09: `architecture/fifo.yaml:81` (configuration.fblock.usage: after RDFAST, WRFAST or a block wrap event; D a block count) and the circular_buffer / double_buffer examples (`:197-224`, `rdfast #16,...` with a block count and the buffers long-aligned); `pasm2/fblock.yaml:12-19` | fblock.yaml "Set next block for when block wraps"; fifo.yaml:73 "Called before block wrap occurs". The "after a wrap event" timing (FBLOCK in response to FBW) is only implied by the double_buffer pattern (:211-212). fifo.yaml examples pass `##buf_size` as D with no unit note (D is a block count). |
| 3026-3028 | RDFAST/WRFAST/FBLOCK encodings | C | `pasm2/rdfast.yaml:4`, `wrfast.yaml:4`, `fblock.yaml:4` | MATCH | Bit strings identical. Operand layouts SD:3028-3037 compared 2026-11-09: D[13:0] block count (0 = limited, no wrap), S[19:0] start address with S[1:0] = %00 for wrapping, now the same in `rdfast.yaml:13,60`, `wrfast.yaml:12-14,23`, `fblock.yaml:12-14,20` and `fifo.yaml:62-72`. |
| 3041 | D[31]=0: wait for prior WRFAST, then (RDFAST) until data arrives | C | `pasm2/rdfast.yaml:55` | MATCH | "waits for any previous WRFAST to finish, then until the FIFO has begun receiving hub data". |
| 3043 | D[31]=1: no wait, 2 clocks, code must allow time | C | `pasm2/rdfast.yaml:56`; `architecture/fifo.yaml:55,63` | MATCH (rdfast); fifo CLOSED 2026-11-09: `architecture/fifo.yaml:62,70` state D[31]=1 skips the whole FIFO reconfiguration wait (2 clocks) for both RDFAST and WRFAST, with `wrfast.yaml:23` | rdfast.yaml MATCH with EF-073 window. fifo.yaml:55 "No-wait flag (1 = don't wait for prior WRFAST)" narrows it: it also skips the reconfiguration wait and the RDFAST data wait. |
| 3045 | FBLOCK always 2 clocks | C | `pasm2/fblock.yaml:8`; `architecture/fifo.yaml:226` | MATCH | |
| 3049-3055 | RFBYTE..RFVARS encodings; 2 clocks | C | `pasm2/rfbyte.yaml:4,8`, `rfvar.yaml:4`, `rfvars.yaml:4` | MATCH | |
| 3057-3059 | WC = MSB of data; WZ = data zero | C | `pasm2/rfbyte.yaml:15-16`, `rfword.yaml:15`, `rflong.yaml:15`, `rfvar.yaml:22-23`, `rfvars.yaml:20-21` | MATCH | rfvar "C: Always cleared to 0" is the MSB of a zero-extended 29-bit value; consistent. |
| 3061, 3066-3108 | RFVAR/RFVARS: 1..4 bytes by MSB of each byte, 4th byte full 8 bits; zero vs sign extended | C | `pasm2/rfvar.yaml:24-33`; `pasm2/rfvars.yaml:22-30` | MATCH | "A 4th byte is always the last and carries all 8 bits"; sign bit "bit 6, 13, 20 or 28". Matches Table 32. |
| 3114-3118 | WFBYTE/WFWORD/WFLONG encodings, 2 clocks | C | `pasm2/wfbyte.yaml:4,8` | MATCH | |
| 3120 | WAITX #20 before a cog stops itself after WRFAST | C | `language/spin2/methods/cogstop.yaml:95` | CLOSED 2026-11-09: `pasm2/cogstop.yaml:45`, `pasm2/wrfast.yaml:25`, `architecture/fifo.yaml:74` carry WAITX #20 before a cog that has been writing via WRFAST stops itself | Spin2 COGSTOP page carries it. `pasm2/cogstop.yaml`, `pasm2/wrfast.yaml`, `architecture/fifo.yaml` do not (searched `waitx`, `lingering`). |
| 3127-3129 | RDBYTE/RDWORD/RDLONG encodings | C | `pasm2/rdbyte.yaml:4`, `rdword.yaml:4`, `rdlong.yaml:5` | MATCH | |
| 3135-3137 | WC = MSB, WZ = zero for RDxxxx | C | `pasm2/rdbyte.yaml:15-16`, `rdword.yaml:16-17`, `rdlong.yaml:25-26` | MATCH | |
| 3142-3145 | WRBYTE/WRWORD/WRLONG/WMLONG encodings | C | `pasm2/wrbyte.yaml:4`, `wrword.yaml:4`, `wrlong.yaml:5`, `wmlong.yaml:4` | MATCH | |
| 3151 | WMLONG skips $00 bytes | C | `pasm2/wmlong.yaml:14` | MATCH | "Write only non-$00 bytes in D[31:0]". |
| 3153-3157 | S forms: register, #$00..$FF, ##20-bit | C | `pasm2/rdbyte.yaml:33-42` (family) | MATCH | "A plain immediate source/address operand is limited to 0-255". |
| 3158-3205 | PTRx forms, %1SUPNNNNN layout, INDEX6, 00000=16, SCALE | C | `pasm2/concepts/addressing_modes.yaml:42-83` | IN-PLAN §3 | `ptr_expression_encoding`. Existing semantic text (index -32..+31, 1..16, scaling) agrees. |
| 3161-3166, 3243-3252 | AUGS reinterprets #S: 20-bit address or PTR with 20-bit index | C | `pasm2/concepts/addressing_modes.yaml:92` | IN-PLAN §3 | Augmented form. |
| 3208-3240 | Worked PTR encoding examples | C | — | IN-PLAN §3 | CP-032 covers the same words. |
| 3257 | SETQ/SETQ2 + RDLONG: one long per clock, FIFO has priority on a slice clash | C | `pasm2/concepts/setq_block_ops.yaml:67,84,199` | MATCH | "the FIFO gets priority and the block move waits for the slice to come around again". |
| 3257 | Block RDLONG WC/WZ set from the last long read | C | CLOSED 2026-11-09: `pasm2/rdlong.yaml:27` (flags_affected.block_transfer), `pasm2/concepts/setq_block_ops.yaml:18,72`, `architecture/hub.yaml:117` | NOT-CARRIED | Searched `last long`, `according to the last`, flags in `setq_block_ops.yaml`, `rdlong.yaml` (flags_affected says only "Set to MSB of long"). Home: `rdlong.yaml` flags_affected, `setq_block_ops.yaml`. |
| 3269 | WRLONG/WMLONG with immediate D after SETQ fills hub | C | `pasm2/concepts/setq_block_ops.yaml:186-195` | MATCH | "Only an immediate D fills". |
| 3276 | $1F8..$1FF cannot be block-written to hub | C | `pasm2/idioms/hub-memory.yaml:92-93` | CLOSED 2026-11-09: `pasm2/concepts/setq_block_ops.yaml:20,244-245` (overview and context_save), `pasm2/wrlong.yaml:27`, `pasm2/wmlong.yaml:20` | Carried in the idiom page only. Not in `setq_block_ops.yaml` (whose `context_save` at :223 is where an agent saves registers) or `wrlong.yaml`/`wmlong.yaml`. |
| 3283-3298 | Block PTRx: index overridden by long count, bit 4 = ++/--; plain PTRx index = 0 | C | `pasm2/concepts/setq_block_ops.yaml` | IN-PLAN §3 (compared only, 2026-11-09) | `ptrx_with_block_transfers`. SD:3283-3298 is present in the text: the five forms (PTRA, PTRA++, PTRA--, ++PTRA, --PTRA) match `setq_block_ops.yaml:136-140` row by row, as do the index override by the long count, bit 4 as the ++/-- indicator and zero for plain PTRx (`:134`). |
| 3300 | Block moves yield to the FIFO, so they work during hub execution | C | CLOSED 2026-11-09: `pasm2/concepts/cog_hub_execution.yaml:347` (hub_io_in_hubexec.note, already carried and sourced), `pasm2/hubexec.yaml:33,48`, `pasm2/concepts/setq_block_ops.yaml:18,73`, `architecture/hub.yaml:118` | NOT-CARRIED | Searched `block (move\|transfer).*hub exec`, `used during hub exec`, `yield to the`; `cog_hub_execution.yaml`, `hubexec.yaml` list what is forbidden but never say SETQ block moves are allowed. The debugger overlay example (`cog_hub_execution.yaml:133-134`) uses one without stating the rule. |
| 3304-3313 | CORDIC: 54-stage, operation list | C | `architecture/cordic.yaml:13,52-111` | MATCH | |
| 3315 | Command waits 0..cogs-1 for slot; results 55 clocks later; GETQx waits | C | `pasm2/qmul.yaml:9` ('2...9'); `architecture/cordic.yaml:20` | MATCH | All Q* pages '2...9'. |
| 3319-3326 | QMUL D*S; GETQX low, GETQY high | C | `architecture/cordic.yaml:58-59`; `pasm2/qmul.yaml:19` | MATCH | |
| 3331-3346 | QDIV {Q:D}/S; QFRAC {D:Q}/S; X=quotient, Y=remainder | C | `pasm2/qdiv.yaml:12-14`; `pasm2/qfrac.yaml:12-14`; `architecture/cordic.yaml:64-73` | MATCH | qfrac "Numerator formed from {D, SETQ value or 32'b0}". |
| 3351-3357 | QSQRT of {S:D} | C | `pasm2/qsqrt.yaml:12`; `architecture/cordic.yaml:78` | MATCH | "S = upper 32, D = lower 32". |
| 3362-3374 | QROTATE (D,Q) by S, angle unsigned $0..$FFFFFFFF = 0..360; no SETQ = polar to cartesian | C | `pasm2/qrotate.yaml:12-14,59,72`; `architecture/cordic.yaml:84-89` | MATCH | "90°=$40000000". |
| 3379-3386 | QVECTOR X=D, Y=S → length, angle | C | `pasm2/qvector.yaml:12-14` | MATCH | |
| 3391-3408 | QLOG to 5:27; QEXP from 5:27 | C | `pasm2/qlog.yaml:12`; `pasm2/qexp.yaml:12`; `architecture/cordic.yaml:100-111` | MATCH | |
| 3413 | No interrupts during an overlapped juggle: results can be overwritten | C | `architecture/cordic.yaml:142`; `pasm2/getqx.yaml:35-36` | IN-PLAN §1 (stall), §7 (overwrite rule) | getqx.yaml: "protect the entire CORDIC sequence ... using REP @.end, #1". |
| 3413 | GETQX/GETQY with nothing pending: 2 clocks, QMT set | C | `architecture/cordic.yaml:119,125` | MATCH; IN-PLAN §9 arm M (returned value) | |
| 3413, 3444-3634 | One cog can keep 8 commands outstanding (8-cog chip): demo issues 8 before the first read, then 1 in / 1 out | C | `architecture/cordic.yaml:9-13,21` | CLOSED 2026-11-09 («#456», after «#454»): `cordic.yaml:9-13` and `:21` (ops_in_flight_per_cog) give the SD sequence of eight SETQ+QROTATE commands, one result read per further command, eight trailing result reads (eight outstanding), and "Not documented: the maximum count"; EF-053's depth 7 stays in its tested shape (`:34-40`) | cordic.yaml:18 "up to ~6-7 (... the documentation says 'several', stating no hard count)" and :26 "Submit ~6-7 ops before expecting results". The source's own demo (SD:3444-3466) issues 8 QROTATEs before the first GETQY ("result 00 is ready at 54!!!" with 00..07 issued) and holds 8 outstanding in steady state. Related to, but not the same as, the §7 overwrite rule. |
| 3468-3634 | Demo reads GETQY before GETQX each result | C | — | IN-PLAN §9 arm K | Which read retires a result. |
| 3422-3433, 3639-3670 | Demo DAC setup, frame sync, output loop | M | — | NOT-CARRIED (example); decision stands 2026-11-09 («#456») | Example code only; no contract beyond the CORDIC rows. |
| 3674 | 16 locks; LOCKNEW / LOCKTRY / LOCKREL / LOCKRET | C | `architecture/locks.yaml:20-21,96-183` | MATCH | |
| 3674-3680 | No LOCKCHK instruction; status comes from LOCKREL WC | C | `architecture/hub.yaml:146-150` | CLOSED 2026-11-09 against «#445» («#456» re-read): `shared_resources.locks.operations` lists locknew, lockret, locktry, lockrel only; `hub.yaml:151` `atomic` | hub.yaml shared_resources.locks.operations: `lockchk: "Check lock state"` beside the four PASM instructions. SD lists four instructions (SD:3677-3680). LOCKCHK exists only as a Spin2 method (`language/spin2/methods/lockchk.yaml`). |
| 3680 | LOCKREL takes {WC}, so its encoding has a C bit | C | `architecture/locks.yaml:119,170` | CLOSED 2026-11-09: both LOCKREL encodings now read `EEEE 1101011 C0L DDDDDDDDD 000000111`, agreeing with `pasm2/lockrel.yaml:4` and CSV:271 (the SD:5239 `00L` slip is «#460»'s) | locks.yaml "EEEE 1101011 00L DDDDDDDDD 000000111" for LOCKREL and its query form; `pasm2/lockrel.yaml:4` "C0L"; CSV:271 "C0L". locks.yaml copies SD:5239's `00L`, which contradicts SD:3680 and SD:5239's own `{WC}`. |
| 3684 | LOCKNEW: number into D; WC C=0 success, 1 none | C | `architecture/locks.yaml:140-145`; `pasm2/locknew.yaml:13-17` | MATCH | |
| 3684 | A cog may allocate several locks | C | `architecture/locks.yaml:144` | MATCH | |
| 3686 | Any cog may LOCKRET | C | `architecture/locks.yaml:159-160` | MATCH | Not on `pasm2/lockret.yaml` (minor). |
| 3688 | LOCKTRY WC: C=1 taken; C=0 held elsewhere or not allocated | C | `architecture/locks.yaml:103-107` | MATCH | |
| 3688 | C is written only if WC is given (example code must use WC) | C | `architecture/locks.yaml:107,113-116` | CLOSED 2026-11-09: usage_example now `LOCKTRY lock_num WC`; the operation block states "C is written only when WC is given"; `pasm2/concepts/multi_cog_synchronization.yaml:352-367` deadlock schematic rewritten with WC and retry branches. Every PASM LOCKTRY instruction line under the KB carries WC (34 instruction hits in locks, locktry, lockrel, multi_cog_synchronization, basic-io; 0 without) | Example: "LOCKTRY lock_num         ' Try to get lock / IF_C    JMP #got_lock". No WC, so C is unchanged and the branch tests a stale flag. SD:3688 "If WC is used with the instruction, the C flag will indicate". Also schematic: `pasm2/concepts/multi_cog_synchronization.yaml:360-368` (no WC, no retry; illustrative only). |
| 3688, 3698 | Held lock released by LOCKREL, COGSTOP, COGINIT restart, or LOCKRET | C | `architecture/locks.yaml:44-55` | CLOSED 2026-11-09 (SD:3698 cell stays IN-PLAN §11): `locks.yaml:54` lists "restarted by COGINIT while it holds the lock"; also `pasm2/locktry.yaml:82`, `pasm2/lockrel.yaml:81` | Source line :45 quotes it; the operative list :54 says "The owner cog becoming INACTIVE - for any cause, including COGSTOP" which does not cover a COGINIT restart of a running cog (it never becomes inactive). Not on `pasm2/locktry.yaml`/`lockrel.yaml` (searched `coginit`, `cogstop`, `implicit`). |
| 3690 | Hub arbitrates locks round-robin: every spinning cog gets a fair turn | C | CLOSED 2026-11-09: `architecture/locks.yaml:109-110,190` (LOCKTRY operation, basic_mutex), `pasm2/locktry.yaml:20-21` | NOT-CARRIED | Searched `round.robin`, `fair` in `architecture/locks.yaml`, `pasm2/lock*.yaml`, `spin2/methods/lock*.yaml`. Home: `architecture/locks.yaml` (basic_mutex), `pasm2/locktry.yaml`. |
| 3692-3694 | Spin-until-acquired pattern | C | `architecture/locks.yaml:186-198` | MATCH | "LOCKTRY lock_num WC / IF_NC JMP #.retry_lock". |
| 3696 | Only the taker can release | C | `architecture/locks.yaml:124` | MATCH | |
| 3700 | LOCKREL WC: C = taken; register D gets current/last owner; still releases if caller holds it | C | `architecture/locks.yaml:166-183`; `pasm2/lockrel.yaml:12-14` | MATCH | "this is not a passive query". |

Counts (69 rows; two rows carry two dispositions and are counted under both): MATCH 40 · PARTIAL 7 · MISMATCH 7 · NOT-CARRIED 5 contract + 2 mechanism/example · IN-PLAN 9 primary (plus §9 arm M and §11 as secondary on two rows).

Closure 2026-11-09 («#456»): the 7 MISMATCH rows, the 5 contract NOT-CARRIED rows and the 7 PARTIAL rows on touched files are closed
(MISMATCH 1, 3 and 5 against «#445», the SD:173 PARTIAL against «#446»); the 2 mechanism/example NOT-CARRIED rows stand; the
IN-PLAN rows close against «#445», «#448», «#454» and the arm-M cell (stay as «#454» left them). Findings below are the walk's
original text, kept as written.

## Findings

Contract rows only, most consequential first.

1. **MISMATCH: LOCKTRY example branches on C without WC.** `architecture/locks.yaml:110-113`:
   "LOCKTRY lock_num ' Try to get lock / IF_C JMP #got_lock ' Jump if successful". SD:3688: "If WC is
   used with the instruction, the C flag will indicate afterwards whether the lock was successfully
   taken." Without WC, C is stale, so the copied code enters the critical section on a random flag.
   The same page's basic_mutex (:192) uses WC correctly. Searched `locktry` lines lacking `wc`; the
   other hits are the schematic deadlock example in `multi_cog_synchronization.yaml:360-368`.

2. **MISMATCH: hub.yaml says the FIFO wraps on power-of-2 boundaries set by a mask.**
   `architecture/hub.yaml:142` "block_wrap: Can wrap on power-of-2 boundaries"; `:221-224`
   "RDFAST mask, hub_addr ' Mask sets wrap boundary". SD:3020: "The block count determines how many
   64-byte blocks will be read or written before wrapping to the original start address and reloading
   the original block count." A mask passed as D is read as a block count. `fifo.yaml` and
   `rdfast.yaml` are right, so hub.yaml contradicts them.

3. **MISMATCH: the FIFO is said to have a 64-byte minimum transfer.** `architecture/fifo.yaml:239`
   "Minimum transfer granularity is 64-byte blocks (streamer/software role)". SD:3003: the FIFO
   "allows hub RAM to be either sequentially read or sequentially written in any combination of bytes,
   words, or longs, at any rate". The block only sets the wrap length.

4. **NOT-CARRIED: FIFO wrap needs a long-aligned start address.** SD:3020: "If you intend to use
   wrapping, your hub start address must be long-aligned (address ends in %00)". Searched
   `long-aligned`, `long aligned`, `ends in %00` near fifo/wrap/block; only hub-exec branch costs hit.
   Home: `architecture/fifo.yaml` configuration, `pasm2/rdfast.yaml`, `wrfast.yaml`, `fblock.yaml`.

5. **NOT-CARRIED: the streamer and RFxxxx/WFxxxx share the FIFO, one at a time.** SD:3007-3011: "it can
   only be used for one of these at a time" (hub execution, streamer, software). The KB states only
   the hub-exec exclusion (`fifo.yaml:18-20`) and merges streamer and software into one role
   (`fifo.yaml:8-10`). Searched `one of these at a time`, `only be used for one`, `three ways`, and the
   streamer pages for RFLONG/RFBYTE. Home: `architecture/fifo.yaml` limitations,
   `architecture/streamer/overview.yaml`.

6. **MISMATCH: CORDIC in-flight count understated.** `architecture/cordic.yaml:18` "up to ~6-7 ...
   the documentation says 'several', stating no hard count"; `:26` "Submit ~6-7 ops before expecting
   results". The source's demo (SD:3444-3466) issues 8 SETQ+QROTATE commands before the first GETQY,
   annotated "result 00 is ready at 54!!!", and then holds 8 outstanding (one in, one out per 8 clocks)
   through SD:3610. EF-053 tested only to depth 7, so it does not contradict 8.

7. **MISMATCH: LOCKREL encoding drops the C bit.** `architecture/locks.yaml:116,167`: "EEEE 1101011 00L
   DDDDDDDDD 000000111". SD:3680 gives `LOCKREL {#}D {WC}`; `pasm2/lockrel.yaml:4` and CSV:271 give
   `C0L`. The `00L` comes from SD:5239, which contradicts its own `{WC}`. Record as a source slip; the
   KB serves two encodings for one instruction.

8. **NOT-CARRIED: block-move flags come from the last long.** SD:3257: "If WC/WZ/WCZ are used with
   RDLONG, the flags will be set according to the last long read in the sequence." Searched `last long`,
   `according to the last`; `rdlong.yaml` flags_affected says only "Set to MSB of long". Home:
   `pasm2/rdlong.yaml`, `pasm2/concepts/setq_block_ops.yaml`.

9. **NOT-CARRIED: block moves are usable during hub execution.** SD:3300: "Because these fast block
   moves yield to the hub FIFO interface, they can be used during hub execution." Searched block
   move/transfer with hub exec, `used during hub exec`, `yield to the`. `cog_hub_execution.yaml` and
   `hubexec.yaml` list only what is forbidden, so an agent cannot tell SETQ+RDLONG from RDFAST.

10. **NOT-CARRIED: lock arbitration is round-robin and fair.** SD:3690: "Because lock arbitration is
    performed by the hub in a round-robin fashion, any cog waiting in a loop to capture a lock will get
    its fair turn". Searched `round.robin`, `fair` across the lock pages. Home: `architecture/locks.yaml`
    basic_mutex, `pasm2/locktry.yaml`.

11. **MISMATCH: a LOCKCHK hub operation.** `architecture/hub.yaml:153` lists `lockchk: "Check lock
    state"` among the hub's lock operations, next to the four instructions. SD:3677-3680 lists four
    instructions; status is read with LOCKREL WC (SD:3700). LOCKCHK is a Spin2 method only.

12. **MISMATCH: hub bandwidth figures.** `architecture/hub.yaml:186` "theoretical: Clock_freq / 2
    bytes/second per COG", `:187-188` sustained "Clock_freq / 8", beside `:189` "burst: 4 bytes per
    clock". SD:2999: "continuously-ascending bidirectional streaming of 32 bits per clock". The
    theoretical figure is 8x below the burst figure next to it, and the sustained figures have no source.
