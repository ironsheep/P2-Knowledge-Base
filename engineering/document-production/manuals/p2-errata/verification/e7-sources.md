# E7 sources: Erratum E7, After a No-Wait RDFAST, the Next Hub Instruction Can Complete Early

Verification sidecar for `opus-master/e7-rdfast-blocking-after-no-wait.md` (CH below). Every
number, quotation and code excerpt in the chapter maps to a file and line below. Internal
document: ids and paths are allowed here, never in the chapter.

**History.** Written 2026-09-26 (task «#359», v0.2.0 shape) for E7 as first found (a waiting
`RDFAST` after a no-wait one, EF-073/074) and updated the same day for the workaround run (LF,
EF-077) and the *workaround* wording (#360). **Rewritten 2026-10-01 (task «#368»)** when O29 was
merged into E7 (Stephen, 2026-10-01: "yes merge and record our reasoning";
`CLASSIFICATION-GUIDANCE.md`, *What one erratum is*): the chapter now covers every hub
instruction a no-wait `RDFAST` releases (EF-084, EF-086, EF-087 — written before the merge, they
call it "E8"; read as E7). The chapter file name is kept (`e7-rdfast-blocking-after-no-wait.md`:
not reader-visible; Sacred Rule 5); its title changed. **Every `CH:` number below is the
2026-10-01 chapter's.** The first-found material was carried over from the 2026-09-26 chapter
with *blocking* → *waiting* in prose (the P2 Documentation's own word is "wait"; the printed
block and the programs keep *blocking*, CH:99, CH:105) and its evidence rows remapped.

**Corrected in the ledger while writing (2026-10-01).** EF-084's title said "the waiting form,
or 16 clocks (7 non-hub instructions), prevents both" (the read and the write). The write runs
T3/T4/C4 ran at k = 0 only (LO:255–283; no k on any `RUN T3`/`T4`/`C4` line), so the 16-clock
rule is proven for reads, not writes. EF-084's title and limits now say so, and the chapter
states it (CH:83, CH:111, CH:114, CH:121).

## Abbreviations

| Tag | File |
|---|---|
| **DOC** | `engineering/ingestion/sources/silicon-doc/p2-documentation.txt` (v35) |
| **DOCT** | `engineering/ingestion/sources/silicon-doc/silicon-doc-text.txt` (current online edition; same sentences, checked) |
| **LED** | `engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md` (EF-073 at 1065, EF-074 at 1089, EF-077 at 1157, EF-084 at 1331, EF-086 at 1393, EF-087 at 1434) |
| **RIG** | `.../p2-errata/audit/verification-tests/test-rdfast-wrfast-readiness-boundary.spin2` (first-found test as run; reader copy ARCHIVE) |
| **FIX** | `.../audit/verification-tests/e7-fix-rdfast-spacing-test.spin2` (spacing workaround test as run; reader copy ARCHIVE-WKR) |
| **RO / RB / RC** | `.../audit/verification-tests/test-o29-rdfast-nowait-releases-hub-op.spin2` / `test-o29b-rdfast-nowait-hub-op-scope.spin2` / `test-o29c-setq-block-workaround.spin2` (as run; byte-identical to the campaign copies under `hardware-verification/campaigns/2026-09-p2-errata-predictions/tests/`, `cmp` silent, 2026-10-01) |
| **ARCHIVE** | `examples-library/e7-rdfast-blocking-after-no-wait-test.spin2` |
| **ARCHIVE-WKR** | `examples-library/e7-workaround-rdfast-spacing-test.spin2` |
| **AO / AB / AC** | `examples-library/e7-next-hub-instruction-test.spin2` / `e7-every-hub-width-test.spin2` / `e7-workaround-setq-block-test.spin2` (reader copies of RO / RB / RC, made 2026-10-01; see *The reader copies*) |
| **L1 / L2** | `.../audit/verification-tests/logs/debug_260925-214019.log` / `debug_260925-214922.log` (first-found test, runs 1 and 2) |
| **LF** | `.../logs/debug_260926-015823.log` (spacing workaround run) |
| **LO** | `.../logs/debug_261001-000927.log` (release test; `.bin` 30034 bytes, LO:14, equal to RO's build) |
| **LB** | `.../logs/debug_261001-014330.log` (scope test) |
| **LC** | `.../logs/debug_261001-114625.log` (block-read workaround test) |
| **WX** | `deliverables/ai/P2/language/pasm2/waitx.yaml` |

L1 and L2 share line numbering for every line cited (E_REBLK block L1/L2:1351–1479; the 128
row lines compared the same; LED:1092 "identical in both runs").

## Quotations

| Chapter text | Source |
|---|---|
| "For these instructions, the D operand is the register which will receive the data read from the hub. The S/#/PTRx operand supplies the hub address to read from. If WC is expressed, ... otherwise Z will be cleared." (CH:17) | DOC:6868–6871, four lines joined with single spaces; DOCT:3131–3137 identical (DOCT:3059 is the FIFO section's "equals", not this one) |
| section name RANDOM ACCESS INTERFACE (CH:15) | DOC:6850; DOCT:3123 |
| "For these instructions, the D/# operand supplies the data to be written to the hub. The S/#/PTRx operand supplies the hub address to write to." (CH:21) | DOC:6909–6910; DOCT:3147–3149 |
| "By preceding RDLONG with either SETQ or SETQ2, multiple hub RAM longs can be read into either cog register RAM or cog lookup RAM." (CH:23) | DOC:7170–7171 joined; DOCT:3257 first sentence |
| "If D[31] = 0, RDFAST/WRFAST will wait ... so that it can start being used in the next instruction." (CH:27) | DOC:6705–6707 joined; DOCT:3041 |
| "If D[31] = 1, RDFAST/WRFAST will not wait ... before any attempt is made to read or write FIFO data." (CH:31) | DOC:6708–6709 joined; DOCT:3043 |
| section name FAST SEQUENTIAL FIFO INTERFACE; mode by bit 31 of D (CH:25) | DOC:6669, DOC:6704–6705 |
| "While in hub execution mode, the FIFO cannot be used for anything else. So, during hub execution these instructions cannot be used: RDFAST / WRFAST / FBLOCK" (CH:37) | DOC:746–748 joined (the list's first line only); DOCT:353–355. DOCT:349 carries an inline reviewer remark ("Elsewhere I read that the spin interpreter...") between paragraphs, which is why DOC is the quoted edition |
| section name HUB EXECUTION (CH:37) | DOCT:347 (heading); DOC's extraction runs the heading into the preceding text |
| KNOWN BUGS does not list this behaviour (CH:39) | DOC:197–227: two items only (SETQ/ALTx PTRx deltas; ALTx immediate-#S and AUGS) |
| the no-wait paragraph restricts FIFO data only (CH:33) | DOC:6708–6709 ("read or write FIFO data"); RFLONG et al. are the FIFO read instructions, DOC:6712 onward ("manually read sequential data from the hub") |

## Numbers: hub reads and writes (release, scope and block tests)

| Chapter number | Where | Source |
|---|---|---|
| spacing = start of no-wait `RDFAST` to start of the next hub instruction; k `NOP`s → 2 + 2k clocks | CH:43, CH:45 | `RDFAST` no-wait 2 clocks DOC:6708; `NOP` 2 clocks; RO trial copies (AO:2132–2200: only the `RDFAST` and k `NOP`s between primer and test); LO:503 verdict text "test RDLONG issued 16 clocks after the RDFAST" at k=7 |
| one cog, cog execution, 200 MHz, debugger in cog 0 | CH:43, CH:143 | LO:20 banner `clk 200 MHz`; RO header (`DEBUG_COGS = %0000_0001`); LED:1333 |
| primer `$A5A5_0001`, sentinel `$5A5A_0002`, seed `$C3C3_0003`, old `$0F0F_0004`, new `$F0F0_0005` | CH:47, CH:57, CH:145 | LO:21 `values: primer $A5A5_0001 sentinel $5A5A_0002 seed $C3C3_0003 old $0F0F_0004 new $F0F0_0005` |
| 64 alignments × 16 repetitions = 1,024 records per run | CH:45, CH:145 | LO:24 `Every run: 16 repetitions x 64 cells`; every `all reps` line `of 1024` |
| released alignments by spacing 2..18: 43, 54, 61, 64, 48, 32, 16, 0, 0 | CH:49–51, CH:83, CH:134 | LO:159, 169, 179, 189, 199, 209, 219, 229, 239 (`rep0 primer 43 … 54 … 61 … 64 … 48 … 32 … 16 … 0 … 0`), all with `cells with disagreeing reps 0`; window table LO:493–501 |
| 688 of 1,024 at k = 0; none at k = 7, 8 | CH:149 | LO:159 `primer 688 sentinel 336`; LO:229, 239 `primer 0 sentinel 1024` |
| waiting form: `$5A5A_0002` in all 1,024 at every k | CH:53, CH:111 | LO:69–149 (C2 k0..k8, every one `sentinel 1024`) |
| `RDBYTE`/`RDWORD` at 2 clocks: same 43 alignments; `$D4 $C3 $B2 $A1`, `$C3D4 $A1B2` from `$A1B2_C3D4`; none at 16 | CH:54 | LB:490 (RDBYTE verdict, `off0 $D4 … off3 $A1`, `k=7 none`), LB:495 (RDWORD, `off0 $C3D4 off2 $A1B2`); k=7 rows LB:253, 300, 347, 394, 441, 488 (`sentinel 1024`); LED:1408–1411 |
| flags: released `$A5A5_0001` C=1 Z=0; primer `$0000_0000` → `$0000_0000` C=0 Z=1; correct `$5A5A_0002` C=0 Z=0; 688/336 | CH:55 | LB:201 (FLAGS C), LB:203 (FLAGS Z); LED:1402–1405 |
| released byte/word flags from the value returned | CH:55 | LB:490, 495 (`prediction A with its flags`, `C1Z0`) |
| `PTRA++` +4 in 688 released and 336 correct | CH:56 | LB:205 `released cells: … +4 x688 … correct cells: … +4 x336` |
| `WRLONG` at 2 clocks: 43 (old,old), 21 (primer,new); `NOP` follower: (seed,new) in 64; waiting form (new,new) 1,024 | CH:57, CH:149 | LO:271–272 (T3: `old 1376 new 336 primer 336`; `OO 43 PN 21`); LO:282–283 (T4: `DN 64`); LO:260 (C4: `(new,new) cells 1024 of 1024`) |
| `WRBYTE`/`WRWORD`, every offset, 2 clocks: 43 lost, 21 read-back released; 64 landed with nothing following; waiting form landed | CH:58 | LB:788, 793 (verdicts); LB:521, 569, 617, 665, 713, 761 (WB0–3/WW0/WW2 `C k0`: `(new,new) cells 1024 of 1024`) |
| writes tested at 2 clocks only | CH:58, CH:83, CH:114, CH:121 | LO `RUN C3/C4/T3/T4` lines carry no k (LO:240, 251, 262, 273; RO trial copies `w_w1`/`w_w2` have no `NOP` before the `WRLONG`, AO:2251–2259); LB arm 3 runs all `k0` |
| block read at 4 clocks (`RDFAST` 2 + `SETQ` 2), fresh cog, four alignments released for a single `RDLONG` at 4 clocks, 4 trials each | CH:59 | LC:29–31 (arm 1 header: per cell 4 trials, fresh cog, the four cells); LED:1439–1446 ("all released in EF-084's single-read map at k = 1 (also 4 clocks)") |
| af0/ar0, af0/ar4: long 0 primer, longs 1–7 seed; `$000` `$FC78_00B0`→`$0000_0060`/`$0000_0061`, `$001` `$F605_8C64`→`$4000_0053`; completed | CH:59 | LC:108–112 (af0/ar0 #1), LC:115–133 (#2–#4), LC:136–161 (af0/ar4 #1–#4: `$0000_0061`); sacrificial range at the ping `$A5A5_0001 $C3C3_0003 …` |
| af2/ar0, af1/ar3: nothing written, did not finish within 1 s | CH:59 | LC:165, 169, 173, 177, 181, 185, 189, 193 (`completed: NO - did not finish within 1 s (stopped)`) |
| scope test's block read at 4 clocks: first trial, long 0 primer, 1–7 unwritten, cog lost | CH:59, CH:152 | LB:940–942, 951–952 (`MUUUUUUU`, `never written … 1023 records`) |
| block read waiting form and 16/18/20 clocks: right block 1,024, 0 registers changed, finished | CH:59, CH:112, CH:154 | LC:273, 276, 279, 282 (verdicts); LC:241, 255, 269 (k6/k7/k8 `right block 1024`); LB:935–937 (waiting form in the scope test) |
| `SETQ` counts as one of the seven (6 `NOP`s + `SETQ` = 16 clocks) | CH:112 | RC:2542 comment; LC:32 (`rdfast 2 + 6 nop 12 + setq 2`); LED:1448–1449 |
| no-wait `WRFAST`: no release, `RDLONG … WCZ` and `WRLONG` at 2 and 16 | CH:60, CH:121 | LB:906, 908 |
| `NOP` control and positive control (PS) | CH:147 | LO:49 (C1 `sentinel 1024`), LO:249 (C3 `(new,new) 1024`), LO:59 (PS `1024 of 1024`) |
| no other value; repetitions agree | CH:148 | LO:480 `RIG OK: O29 - … no other value … every cell's 16 repetitions identical` |
| E7N positive control in the release test (spacings 2, 4..20; failing spacing by phase as first test) | CH:150 | LO:284–413; LO:481–489 (phase table `AAAAAAAA … BBBBBBBB`, `8 each`); LO:490 `REPRODUCED` |
| E7B: 18,432 trials, `RDFAST`s 20–34 clocks | CH:70, CH:150 | LO:506–507 |
| scope and block tests reproduced the release first | CH:152, CH:154 | LB:90 `RIG OK (arm 0, positive control): EF-084 reproduced`; LC:84 (same) |
| fresh cog per run/trial; cog RAM checked against the loaded image | CH:154 | LC:88–90 (integrity lines), LED:1435–1437 |
| controls in every run; no repetition disagreed | CH:152, CH:176 | LB `cells with disagreeing reps 0` on every `all reps` line; no `RIG FAIL` in LO, LB, LC (`grep -c "RIG FAIL"` = 0 each) |
| ran 2026-10-01, once each | CH:176, Status CH:245–246 | LO:1, LB:1, LC:1 session dates; one log each in `logs/` |
| about 2 s / 5 s / 9 s (Appendix A) | appendix | first to last `Cog0` line: LO 00:09:28.928→00:09:30.905; LB 01:43:31.170→01:43:35.830; LC 11:46:26.621→11:46:35.546 |

## Numbers: the waiting `RDFAST` (first found) — carried over, remapped

| Chapter number | Where | Source |
|---|---|---|
| waiting `RDFAST` "takes 2 clocks without waiting" at the failing spacing | CH:64, CH:79, CH:167 | every E_REBLK detail line, L1/L2:1352–1478 (even lines) `el X..X base X-2`; exc = the waiting `RDFAST`'s clocks (RIG:600, RIG:1013); LED:1093 |
| next `RFLONG` returns `$0000_0000` | box CH:6, CH:64, CH:79, CH:167 | L1/L2:1486 `zero 1_024`; L1/L2:1487 `got $0000_0000 expected $A5A5_0080` |
| failing spacing 8 to 15 clocks; each in exactly 8 of 64 | CH:65, CH:79 | L1/L2:1487 `wrong up to gap 15 clk`; detail lines `dist 8`..`dist 15`; LED:1095 |
| exactly one spacing failed per alignment, all 16 trials | CH:64 | every E_REBLK `cls` string has exactly one `Z` |
| every other spacing: waited 10 to 17 clocks | CH:66 | every `exc` string only `A`..`H` (= 10..17, RIG:809–812) apart from the single `2` |
| 1,024 of 43,008 wrong, 41,984 correct | CH:68 | L1/L2:1486–1487 |
| 64 alignments, 42 spacings, 16 trials; 3 unreachable | CH:62, CH:156 | RIG:210–214, RIG:82–87; L2:23 |
| waiting alone: 3,072 of 3,072, `RFLONG`/`RFWORD`/`RFBYTE`, 10..17 | CH:70 | L1/L2:1511–1512; LED:1074–1076 |
| zero flags C clear Z set in every failing trial printed | CH:79 | E_REBLK detail lines `cz 2` (RIG:245, RIG:1464–1465) |
| second `RFLONG`: slices 0–2 first long, 3–7 zero | CH:79 | detail lines `v2` (L2:1352–1398 vs 1400–1478); also LO:286–413 E7N `v2` (s0–s2 new[s], s3–s7 `$0000_0000`) |
| 16..44 correct in every alignment | CH:83 | every `cls` all `.` from j13; LED:1104–1105 |
| no-wait read alone first correct at 8..15 (the anti-pattern case) | CH:35 | L1/L2:1498–1499, 1509; LED:1076–1080 |
| failing spacing by starting point 10, 9, 8, 15, 14, 13, 12, 11; same for every slice; equals first correct no-wait read | CH:133, CH:164–165 | L2:1352–1366 (detail lines by p), slices 1–7 repeat; B_NW slice-0 rows L1/L2:490, 497, 503, 516, 528, 539, 549, 558 |
| slice 0 start 0: 7→13, 8→12, 9→11, 10→2, 11→17, 12→16 | CH:133, CH:169–172 | L1/L2:1353 `exc AGFEDCB2HGFE...` (codes RIG:801–814) |
| regions, patterns, loading, sync read, sweep, GETCT arithmetic | CH:156 | RIG:61–70, 234–236, 1272–1276, 1456–1467, 599–600; L1/L2:1483 PHASE CHECK |
| controls; every control correct both runs | CH:158 | L1/L2:1481 `RIG OK: …`; no `RIG FAIL` |
| 2026-09-25, twice, same result | CH:176 | L1:1, L2:1; LED:1092 |
| spacing workaround test: controls, positive control, 1,024 of 1,024, 29,696 | CH:107, CH:174 | see *The workaround run (LF)* below |

## The printed block (A proven workaround)

| | |
|---|---|
| Chapter | CH:94–100 (`CON`/`DAT` + 4 instruction lines, max width 75) |
| Source | ARCHIVE-WKR:1099–1105, between the markers `E7 WORKAROUND BLOCK: begin`/`end` (ARCHIVE-WKR:1098, 1106). The header regenerated on 2026-10-01 (new chapter title in *Appears in*) added one line, so every ARCHIVE-WKR and ARCHIVE line number is one more than in the 2026-09-26 sidecar. Byte-identity checked 2026-10-01 by matching each chapter fence against the archive files (a python line-list match): the block matches ARCHIVE-WKR:1099–1105 exactly; `verify-example-corpus-identity.py` GREEN |
| The run that proved it | LF (2026-09-26), FIX:1152–1155 = the block's instructions; 1,024 of 1,024 (LF:484–547) |
| Kind | rule at each use (CH:103) |
| Wording around it (2026-10-01) | CH:103 now says "the next hub instruction, here a waiting `RDFAST`"; CH:105 explains the comment's *blocking*. The block itself is unchanged (it must stay byte-identical) |

## Code excerpts (verbatim, contiguous)

| Chapter excerpt | As-run lines | Archive lines (printed) | Max width |
|---|---|---|---|
| `v_rebn rdlong c_junk, c_oldb` / `waitx c_phase` / `getct c_t0` (CH:187–189) | RIG:1456–1458 | ARCHIVE:1384–1386 | 38 |
| `rflong c_r1 wcz` … `jmp #post_read` (CH:195–200) | RIG:1462–1467 | ARCHIVE:1390–1395 (the same six lines recur at other arms; this is the `v_rebn` copy, three lines after CH:187–189's) | 59 |
| `if distIdx == 0` … (CH:206–209) | RIG:562–565 | ARCHIVE:464–467 | 45 |
| inline: `rdfast c_nowait, c_midb`, `waitx c_dly`, `rdfast #0, c_new` (CH:192) | RIG:1459–1461 | ARCHIVE:1387–1389 | 88/29/88, named inline |
| `r_k7` … `jmp #r_settle` (CH:221–231) | RO:2177–2187 | AO:2181–2191 | 37 |
| `c_prim` primer address, `c_mode` D, `c_pf` stream, `c_pr` test address (CH:234) | RO:2320, 2335, 2343–2344, 2104, 2107 | AO:2324 (`c_prim long HUB_PRIM`), 2339 (`c_mode … RDFAST D under test`), 2108 (`add c_pf, c_strm … slot bits = af`), 2111 (`add c_pr, c_tbl … slot bits = ar`) |  |

No harness: every fence is verbatim from a program that ran, so nothing was compiled for this
chapter beyond the reader copies themselves.

## The reader copies AO, AB, AC (2026-10-01)

Made by three dispatched agents from RO, RB, RC (`cp`, then comment/label text and cog-0 Spin2
style only); verified by the arbiter:

| | AO | AB | AC |
|---|---|---|---|
| measuring image (object offsets, as-run / reader) | $258–$6B0 / $258–$6B0 | $3DC–$AE4 / $3F4–$AFC | $1AC–$52C / $1B8–$538 |
| bytes, identical | 1,112, yes | 1,800, yes | 896, yes |
| DAT labels PASM..PASM_END, names and cog addresses | 82, same | 93, same | 55, same |

Method: each as-run source rebuilt with `pnut-ts -d -l` 1.55.8 in the scratchpad (each equals the
stored audit `.bin`, `cmp` silent), each reader copy built the same way; the image range read
from the listings' `PASM` and `PASM_END` symbols; bytes compared at file offset object base
`$241A` + offset (the base the agents found independently for AB and AC). First image long
`$FF00_0005` (AO, AB) and `$FC78_00B0` (AC, the baseline value the program prints for register
`$000`, LC:108). DEBUG data unchanged (2 records, 24 bytes, all three; every printed line goes
through one `zstr_` of a hub line buffer). Style gate (`spin2-style`, armed rules) GREEN; prepare
gates 12/12 GREEN. Printed labels changed (`O29`/`O29B`/`O29C` → `E7`, `EF-084` → "Erratum E7" or
"single reads"/"the recorded map", `(harness)` → `(test program)`); the agents' full old→new lists
are in the task record. AB and AC also restructured cog-0 methods for the armed style rules (no
early `return`; `_body` helper methods): **behaviour of those methods is confirmed only by the
bench re-run of the reader copies, which is owed** (Appendix A says the copies have not been run).

## *Why it happens*: basis

No reader-citable source describes the mechanism; the section states an account fitted to the
measurements and says so (CH:127). The study's mechanism for O29 (the brief) is **not** used: no
signal names, no "completion" internals; the account is stated at the programmer's model only.

- "The release follows the arrival of the FIFO's first long": the waiting-`RDFAST` failing
  spacing equals the first-correct no-wait read spacing at every starting point (rows above).
- "8 to 15 clocks after the `RDFAST` starts": the first-correct no-wait read range (L1/L2:1509).
- "The window matches an instruction still waiting": the k-sweep counts (LO:493–501) and that a
  `RDLONG` waits for its hub slot (DOC hub RAM timing; the egg-beater rotation, RIG:62–64). The
  sentence is phrased as "the pattern expected if", not as a proven cause.
- "never the FIFO's data or the data at its own address": no `F` (stream long) and no `X` record
  in any run (LO:480; LB per-run `F 0 X 0`).
- One clock earlier and later: the `exc` characters either side of the `2` are in `A`..`H` in every
  row; the slice-0/p0 values (11, 2, 17) are an example only (L2:1369 shows `A` = 10 after the `2`
  in slice 1).

## Where the chapter departs from the ledger's wording

- EF-084's "16 clocks prevents both": corrected in the ledger; the chapter claims the spacing for
  reads only (above).
- EF-084/086/087 say "E8"; the chapter says E7 throughout (the merge).
- LED "arming" (EF-074 title) is not a P2 Documentation term; the chapter states spacings.
- EF-086 "the cog then stopped responding" / EF-087 "the cog does not finish": the chapter says
  "did not finish within 1 s" and "can stop responding", and leaves the cause unknown (CH:122,
  CH:137).
- The Spin2 interpreter's use of the waiting form only (RO header, arbiter-verified) is not in
  the chapter: it is not a Parallax documentation statement and was not measured on silicon.

## The workaround run (LF), re-derived from the per-cell lines

Carried over unchanged from the 2026-09-26 sidecar (task «#359»/«#360»); chapter positions now
CH:107 and CH:174.

| Chapter claim | Raw LF lines |
|---|---|
| ran 2026-09-26, once; 200 MHz | LF:1, LF:20 |
| the `.bin` that ran is the rig on disk | LF:14 (`e7-fix-rdfast-spacing-test.bin`, 19215 bytes, mtime = on-disk) |
| controls: GETCT/WAITX arithmetic; `WAITX #12` = 16 clocks; RDLONG pattern; primed FIFO; late no-wait read | LF:29–92; LF:93–157 (`ok 16/16 OK el 16..16 expected 16`); LF:159–222; LF:224–287; LF:289–352; LF:549 |
| positive control: one failing spacing per alignment, same spacings, 1,024 of 43,008 | LF:355–482 (one `Z` per `cls`, one detail line per cell); LF:552–553 |
| 16..44: first and second read correct, 29,696 | LF:555 |
| the printed block: 1,024 of 1,024, first long then the next | LF:484–547 (`F_FIX … ok 16/16 OK v2bad 0`), LF:556 |
| waiting `RDFAST` in the block 10..17 clocks, 8 different times per slice | LF:484–547 `exc` values; LF:551 PHASE CHECK |

Not in LF and so not claimed: a second run of the workaround test; the block's C/Z; the board's
identity.
