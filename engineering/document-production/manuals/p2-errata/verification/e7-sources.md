# E7 sources: Erratum E7, After a No-Wait RDFAST, the Next Hub Instruction Can Complete Early

Verification sidecar for `opus-master/e7-rdfast-blocking-after-no-wait.md` (CH below). Every
number, quotation and code excerpt in the chapter maps to a file and line below. Internal
document: ids and paths are allowed here, never in the chapter.

**History.** Written 2026-09-26 (task «#359», v0.2.0 shape) for E7 as first found (a waiting
`RDFAST` after a no-wait one, EF-073/074) and updated the same day for the workaround run (LF,
EF-077) and the *workaround* wording (#360). **Rewritten 2026-10-01 (task «#368»)** when O29 was
merged into E7 (Stephen, 2026-10-01: "yes merge and record our reasoning";
`CLASSIFICATION-GUIDANCE.md`, *What one erratum is*): the chapter covers every hub instruction a
no-wait `RDFAST` releases (EF-084, EF-086, EF-087 — written before the merge, they call it "E8";
read as E7). **Updated the same evening** for the read/write workaround run (EF-088, VO-J-025;
Stephen: "yes A and let's do all runs at the same bench effort"): the chapter now prints the
read, write and waiting-form blocks from that run, and no longer prints the 2026-09-26
`RDFAST`-to-`RDFAST` block (it is described in prose, CH:130, CH:195, CH:235). The chapter file
name is kept (`e7-rdfast-blocking-after-no-wait.md`: not reader-visible; Sacred Rule 5); its title
changed. **Every `CH:` number below is the chapter as of EF-088.** The first-found material is
carried over with *blocking* → *waiting* in prose (the P2 Documentation's own word is "wait"; the
test programs keep *blocking* in their names and output).

**The write gap, found and closed (2026-10-01).** EF-084's title said "the waiting form, or 16
clocks (7 non-hub instructions), prevents both" (the read and the write). Its write runs
T3/T4/C4 ran at k = 0 only (LO:240–283; no k on any `RUN T3`/`T4`/`C4` line), so the 16-clock
rule was proven for reads, not writes. EF-084's title and limits were corrected; the chapter
said so until EF-088 ran writes of every width at 16 clocks (LH:112, 132–182), and now states the
rule as proven for both (CH:83, CH:116, CH:140).

## Abbreviations

| Tag | File |
|---|---|
| **DOC** | `engineering/ingestion/sources/silicon-doc/p2-documentation.txt` (v35) |
| **DOCT** | `engineering/ingestion/sources/silicon-doc/silicon-doc-text.txt` (current online edition; same sentences, checked) |
| **LED** | `engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md` (EF-073 at 1065, EF-074 at 1089, EF-077 at 1157, EF-084 at 1331, EF-086 at 1393, EF-087 at 1434, EF-088 after it) |
| **RIG** | `.../p2-errata/audit/verification-tests/test-rdfast-wrfast-readiness-boundary.spin2` (first-found test as run; reader copy ARCHIVE) |
| **FIX** | `.../audit/verification-tests/e7-fix-rdfast-spacing-test.spin2` (spacing workaround test as run; reader copy ARCHIVE-WKR) |
| **RO / RB / RC** | `.../audit/verification-tests/test-o29-rdfast-nowait-releases-hub-op.spin2` / `test-o29b-rdfast-nowait-hub-op-scope.spin2` / `test-o29c-setq-block-workaround.spin2` (as run; byte-identical to the campaign copies, `cmp` silent) |
| **RH** | `.../audit/verification-tests/e7-workaround-hub-access-test.spin2` (read/write workaround test as run; campaign test 22, byte-identical) |
| **ARCHIVE** | `examples-library/e7-rdfast-blocking-after-no-wait-test.spin2` |
| **ARCHIVE-WKR** | `examples-library/e7-workaround-rdfast-spacing-test.spin2` |
| **AO / AB / AC** | `examples-library/e7-next-hub-instruction-test.spin2` / `e7-every-hub-width-test.spin2` / `e7-workaround-setq-block-test.spin2` (reader copies of RO / RB / RC) |
| **AH** | `examples-library/e7-workaround-hub-access-test.spin2` (RH with the generated header: from line 25 on, one line below RH, byte-identical — `diff` of the bodies silent) |
| **L1 / L2** | `.../audit/verification-tests/logs/debug_260925-214019.log` / `debug_260925-214922.log` (first-found test, runs 1 and 2) |
| **LF** | `.../logs/debug_260926-015823.log` (spacing workaround run) |
| **LO / LB / LC** | `.../logs/debug_261001-000927.log` / `-014330.log` / `-114625.log` (release, scope, block-read tests) |
| **LH** | `.../logs/debug_261001-140939.log` (read/write workaround test; `.bin` 24590 bytes, LH:14, = a fresh build of RH, `cmp` silent) |
| **LRO / LRB / LRC** | `.../audit/verification-tests/logs-archive/debug_261001-141047.log` / `-141100.log` / `-141120.log` (the AO / AB / AC re-runs; moved there from `examples-library/logs/`) |
| **WX** | `deliverables/ai/P2/language/pasm2/waitx.yaml` |

L1 and L2 share line numbering for every line cited (E_REBLK block L1/L2:1351–1479; the 128
row lines compared the same; LED:1092 "identical in both runs").

## Quotations

| Chapter text | Source |
|---|---|
| "For these instructions, the D operand is the register which will receive the data read from the hub. The S/#/PTRx operand supplies the hub address to read from. If WC is expressed, ... otherwise Z will be cleared." (CH:17) | DOC:6868–6871, four lines joined with single spaces; DOCT:3131–3137 identical |
| section name RANDOM ACCESS INTERFACE (CH:15) | DOC:6850; DOCT:3123 |
| "For these instructions, the D/# operand supplies the data to be written to the hub. The S/#/PTRx operand supplies the hub address to write to." (CH:21) | DOC:6909–6910; DOCT:3147–3149 |
| "By preceding RDLONG with either SETQ or SETQ2, multiple hub RAM longs can be read into either cog register RAM or cog lookup RAM." (CH:23) | DOC:7170–7171 joined; DOCT:3257 first sentence |
| "If D[31] = 0, RDFAST/WRFAST will wait ... so that it can start being used in the next instruction." (CH:27) | DOC:6705–6707 joined; DOCT:3041 |
| "If D[31] = 1, RDFAST/WRFAST will not wait ... before any attempt is made to read or write FIFO data." (CH:31) | DOC:6708–6709 joined; DOCT:3043 |
| section name FAST SEQUENTIAL FIFO INTERFACE; mode by bit 31 of D (CH:25) | DOC:6669, DOC:6704–6705 |
| "While in hub execution mode, the FIFO cannot be used for anything else. So, during hub execution these instructions cannot be used: RDFAST / WRFAST / FBLOCK" (CH:37) | DOC:746–748 joined (the list's first line only); DOCT:353–355. DOCT carries an inline reviewer remark between paragraphs, which is why DOC is the quoted edition |
| section name HUB EXECUTION (CH:37) | DOCT:347 (heading); DOC's extraction runs the heading into the preceding text |
| KNOWN BUGS does not list this behaviour (CH:39) | DOC:197–227: two items only (SETQ/ALTx PTRx deltas; ALTx immediate-#S and AUGS) |
| the no-wait paragraph restricts FIFO data only (CH:33) | DOC:6708–6709 ("read or write FIFO data"); RFLONG et al. are the FIFO read instructions, DOC:6712 onward |

## Numbers: hub reads and writes (release, scope and block tests)

| Chapter number | Where | Source |
|---|---|---|
| spacing = start of no-wait `RDFAST` to start of the next hub instruction; k `NOP`s → 2 + 2k clocks | CH:43, CH:45 | `RDFAST` no-wait 2 clocks DOC:6708; `NOP` 2 clocks; AO:2132–2200 (only the `RDFAST` and k `NOP`s between primer and test); LO:503 verdict text "test RDLONG issued 16 clocks after the RDFAST" at k=7 |
| one cog, cog execution, 200 MHz, debugger in cog 0 | CH:43, CH:162 | LO:20 banner `clk 200 MHz`; RO header (`DEBUG_COGS = %0000_0001`); LED EF-084 *How proven* |
| primer `$A5A5_0001`, sentinel `$5A5A_0002`, seed `$C3C3_0003`, old `$0F0F_0004`, new `$F0F0_0005` | CH:47, CH:57, CH:164 | LO:21 |
| 64 alignments × 16 repetitions = 1,024 records per run | CH:45, CH:164 | LO:24 `Every run: 16 repetitions x 64 cells`; every `all reps` line `of 1024` |
| released alignments by spacing 2..18: 43, 54, 61, 64, 48, 32, 16, 0, 0 | CH:49–51, CH:83, CH:153 | LO:159, 169, 179, 189, 199, 209, 219, 229, 239, all `cells with disagreeing reps 0`; window table LO:493–501 |
| 688 of 1,024 at k = 0; none at k = 7, 8 | CH:168 | LO:159 `primer 688 sentinel 336`; LO:229, 239 `primer 0 sentinel 1024` |
| waiting form: `$5A5A_0002` in all 1,024 at every k | CH:53, CH:126 | LO:69–149 (C2 k0..k8, every one `sentinel 1024`) |
| `RDBYTE`/`RDWORD` at 2 clocks: same 43 alignments; `$D4 $C3 $B2 $A1`, `$C3D4 $A1B2` from `$A1B2_C3D4`; none at 16 | CH:54 | LB:490, LB:495; k=7 rows LB:253, 300, 347, 394, 441, 488 (`sentinel 1024`) |
| flags: released `$A5A5_0001` C=1 Z=0; primer `$0000_0000` → C=0 Z=1; correct `$5A5A_0002` C=0 Z=0; 688/336 | CH:55 | LB:201, LB:203 |
| released byte/word flags from the value returned | CH:55 | LB:490, 495 (`prediction A with its flags`, `C1Z0`) |
| `PTRA++` +4 in 688 released and 336 correct | CH:56 | LB:205 |
| `WRLONG` at 2 clocks: 43 (old,old), 21 (primer,new); `NOP` follower: (seed,new) in 64; waiting form (new,new) 1,024 | CH:57, CH:168 | LO:271–272 (T3), LO:282–283 (T4), LO:260 (C4) |
| `WRBYTE`/`WRWORD`, every offset, 2 clocks: 43 lost, 21 read-back released; 64 landed with nothing following; waiting form landed | CH:58 | LB:788, 793; LB:521, 569, 617, 665, 713, 761 (`C k0`: `(new,new) cells 1024 of 1024`) |
| block read at 4 clocks (`RDFAST` 2 + `SETQ` 2), fresh cog, four alignments released for a single `RDLONG` at 4 clocks, 4 trials each | CH:59 | LC:29–31; LED EF-087 ("all released in EF-084's single-read map at k = 1 (also 4 clocks)") |
| af0/ar0, af0/ar4: long 0 primer, longs 1–7 seed; `$000` `$FC78_00B0`→`$0000_0060`/`$0000_0061`, `$001` `$F605_8C64`→`$4000_0053`; completed | CH:59 | LC:108–133 (af0/ar0 #1–#4), LC:136–161 (af0/ar4) |
| af2/ar0, af1/ar3: nothing written, did not finish within 1 s | CH:59 | LC:165–193 (`completed: NO - did not finish within 1 s (stopped)`) |
| scope test's block read at 4 clocks: first trial, long 0 primer, 1–7 unwritten, cog lost | CH:59, CH:171 | LB:940–942, 951–952 |
| block read waiting form and 16/18/20 clocks: right block 1,024, 0 registers changed, finished | CH:59, CH:131, CH:173 | LC:273, 276, 279, 282; LC:241, 255, 269; LB:935–937 |
| `SETQ` counts as one of the seven (6 `NOP`s + `SETQ` = 16 clocks) | CH:131 | RC:2542 comment; LC:32 |
| no-wait `WRFAST`: no release, `RDLONG … WCZ` and `WRLONG` at 2 and 16 | CH:60, CH:140 | LB:906, 908 |
| release test controls and positive control (PS) | CH:166 | LO:49 (C1), LO:249 (C3), LO:59 (PS) |
| no other value; repetitions agree | CH:167 | LO:480 |
| E7N positive control in the release test | CH:169 | LO:284–413; LO:481–489; LO:490 `REPRODUCED` |
| E7B: 18,432 trials, `RDFAST`s 20–34 clocks | CH:70, CH:169 | LO:506–507 |
| scope and block tests reproduced the release first | CH:171, CH:173 | LB:90; LC:84 |
| fresh cog per run/trial; cog RAM checked against the loaded image | CH:173 | LC:88–90 |
| ran 2026-10-01, once each | CH:197, Status CH:266–267 | LO:1, LB:1, LC:1, LH:1 |

## Numbers: the read/write workaround test (EF-088)

Re-derived from LH's per-cell rows (`rep0 a0-7` lines: every run's 64 cells parsed, every
`agree` field `........` = all 16 repetitions identical), not from the verdict lines.

| Chapter number | Where | Source |
|---|---|---|
| `WAITX #HUB_SPACING_WAITX` (12) = 14 clocks; next hub instruction at 16 | CH:89, CH:112, CH:116, CH:175 | WX (`2 + D`); LH:42 K_CLK `elapsed 16..16 clk (predicted 16)` in all 1,024; RH listing: W_READ `$21C rdfast $FC714EA8`, `$220 waitx #12 $FD64181F`, `$224 rdlong … wcz $FB1956A9` consecutive, no `AUGS` (VO-J-025 review) |
| read block: `$5A5A_0002` with its flags (C=0 Z=0), 1,024 of 1,024 | CH:112, CH:116, CH:175 | LH:92; rows: W_READ 64 × `S0` |
| write block: lands, read back at once and later, 1,024 of 1,024 | CH:112, CH:116, CH:175 | LH:112; rows: W_WRITE 64 × `NN-` |
| `WRBYTE` +0..+3, `WRWORD` +0, +2 after the same `WAITX`: merged long, 1,024 each | CH:116, CH:175 | LH:132, 142, 152, 162, 172, 182; rows 64 × `NN-` each; merged values LH:22 |
| no spacing: read released 43 of 64, write lost 43 of 64 (21 read-backs released) | CH:116, CH:175 | LH:82 (P_READ 688/336, δ 8 8 7 6 5 4 3 2), LH:102 (P_WRITE OO 688, PN 336); rows: P_READ 43 × `P1` + 21 × `S0`, P_WRITE 43 × `OO-` (δ 8 8 7 6 5 4 3 2) + 21 × `PN-` |
| waiting-form block: lands, read back with flags (C=1 Z=0), 1,024 of 1,024 | CH:126, CH:175 | LH:122; rows 64 × `NN1` (flags digit = C + 2·Z = 1) |
| flags preset C set Z set before each read trial | CH:175 | LH:43, 73, 83, 113 (`modcz C=1 Z=1`) |
| controls: `NOP` for the `RDFAST` read `$5A5A_0002` C=0 Z=0, write landed; PS stream long | CH:175 | LH:52 (C1 `S0`), LH:72 (C3 `NN-`), LH:62 (PS) |
| every control clean; `nowait` echoed `$8000_0000` | CH:197 | LH:184 |
| ran 2026-10-01, once, about one second | CH:197; Appendix A | LH:1; first to last `Cog0` line 14:09:40.208 → 14:09:41.384 |
| the tests ran in cog execution, one cog, 200 MHz, no pins | CH:162 | LH:20 banner; RH header |

## The printed blocks (A proven workaround)

| Chapter fence | Archive lines | As-run lines | Kind |
|---|---|---|---|
| CH:92 (`HUB_SPACING_WAITX = 12 …`, width 75) | AH:270, between `E7 WORKAROUND SPACING: begin/end` (AH:269, 271) | RH:269 | the constant |
| CH:98–100 (read block, 3 lines, max 73) | AH:1605–1607, markers AH:1604, 1608 | RH:1604–1606 | rule at each use (CH:112) |
| CH:106–109 (write block, 4 lines, max 73) | AH:1669–1672, markers AH:1668, 1673 | RH:1668–1671 | rule at each use |
| CH:121–123 (waiting-form block, 3 lines, max 73) | AH:1679–1681, markers AH:1678, 1682 | RH:1678–1680 | rule at each use |

Byte-identity checked by matching each chapter fence, as a list of lines, against every
`examples-library/e7-*.spin2` (python): each fence above matches exactly one archive run of lines,
and nothing else. The blocks ran as printed: LH ran the RH build (`.bin` = fresh build of RH), and
AH is RH plus the generated header. **The 2026-09-26 printed block** (ARCHIVE-WKR:1099–1105) is no
longer printed; its marker comment in ARCHIVE-WKR was reworded after the fact ("the spaced
arrangement the E7 chapter describes", comment only, no code change), and its Purpose line in
`PURPOSES.md`, the README and the header now say "a `WAITX #12`", not "the printed `WAITX`".

## Code excerpts (verbatim, contiguous)

| Chapter excerpt | As-run lines | Archive lines (printed) | Max width |
|---|---|---|---|
| `v_rebn rdlong c_junk, c_oldb` / `waitx c_phase` / `getct c_t0` (CH:208–210) | RIG:1456–1458 | ARCHIVE:1384–1386 | 38 |
| `rflong c_r1 wcz` … `jmp #post_read` (CH:216–221) | RIG:1462–1467 | ARCHIVE:1390–1395 (the `v_rebn` copy; the same six lines recur at other arms) | 59 |
| `if distIdx == 0` … (CH:227–230) | RIG:562–565 | ARCHIVE:464–467 | 45 |
| inline: `rdfast c_nowait, c_midb`, `waitx c_dly`, `rdfast #0, c_new` (CH:213) | RIG:1459–1461 | ARCHIVE:1387–1389 | 88/29/88, named inline |
| `r_k7` … `jmp #r_settle` (CH:242–252) | RO:2177–2187 | AO:2181–2191 | 37 |
| `c_prim` primer address, `c_mode` D, `c_pf` stream, `c_pr` test address (CH:255) | RO:2320, 2335, 2343–2344, 2104, 2107 | AO:2324, 2339, 2108, 2111 | |

## The reader copies AO, AB, AC — made and re-run (2026-10-01)

Made by three dispatched agents from RO, RB, RC (`cp`, then comment/label text and cog-0 Spin2
style only); verified by the arbiter:

| | AO | AB | AC |
|---|---|---|---|
| measuring image (object offsets, as-run / reader) | $258–$6B0 / $258–$6B0 | $3DC–$AE4 / $3F4–$AFC | $1AC–$52C / $1B8–$538 |
| bytes, identical | 1,112, yes | 1,800, yes | 896, yes |
| DAT labels PASM..PASM_END, names and cog addresses | 82, same | 93, same | 55, same |
| re-run log; `.bin` size on the download line | LRO, 30,090 | LRB, 44,438 | LRC, 32,254 |
| lines (original / re-run); lines differing | 491 / 491; 21 | 957 / 957; 31 | 288 / 288; 53 |

Method: each as-run source rebuilt with `pnut-ts -d -l` 1.55.8 (each equals the stored audit
`.bin`); the image range read from the listings' `PASM`/`PASM_END` symbols; bytes compared at
object base `$241A` + offset. Re-run comparison: timestamps stripped, `Cog0`/`Cog1` lines diffed in
order, each differing line diffed word by word — every changed span is a label (`O29`, `O29B`,
`O29C`, `E8`, `EF-084`, `EF-074` → E7 wording) or a hub string address (INIT jump, stack, VAR end);
no measured value, count, class or verdict differs. DEBUG data 2 records, 24 bytes each.

**Post-run edit (AO only).** LRO:485–488 printed `VERDICT E7RDLONG:`, `E7WINDOW:`, `E7WRLONG:`,
`E7WAITING` — a space lost when `O29 ` was relabelled. The 28 strings were corrected after the run
(`VERDICT E7 RDLONG` etc.); the measuring image re-checked byte-identical (1,112 bytes at
`$241A+$258`), DEBUG data still 24 bytes; the rebuilt `.bin` is 30,118 bytes. Appendix A says so.

## *Why it happens*: basis

No reader-citable source describes the mechanism; the section states an account fitted to the
measurements and says so (CH:146). The study's mechanism for O29 (the brief) is **not** used: no
signal names, no "completion" internals; the account is stated at the programmer's model only.

- "The release follows the arrival of the FIFO's first long" (CH:152): the waiting-`RDFAST`
  failing spacing equals the first-correct no-wait read spacing at every starting point.
- "8 to 15 clocks after the `RDFAST` starts" (CH:148): the first-correct no-wait read range
  (L1/L2:1509).
- "The window matches an instruction still waiting" (CH:153): the k-sweep counts (LO:493–501) and
  that a `RDLONG` waits for its hub slot (the egg-beater rotation, RIG:62–64). Phrased as "the
  pattern expected if", not as a proven cause.
- "never the FIFO's data or the data at its own address" (CH:154): no `F` and no `X` record in any
  run (LO:480; LB per-run `F 0 X 0`; LH `other 0` in every run).
- One clock earlier and later (CH:152): the `exc` characters either side of the `2` are in `A`..`H`
  in every row; the slice-0/p0 values (11, 2, 17) are an example only (L2:1369 shows `A` = 10
  after the `2` in slice 1).

## Numbers: the waiting `RDFAST` (first found) — carried over, remapped

| Chapter number | Where | Source |
|---|---|---|
| waiting `RDFAST` "takes 2 clocks without waiting" at the failing spacing | CH:64, CH:79, CH:188 | every E_REBLK detail line, L1/L2:1352–1478 (even lines) `el X..X base X-2`; exc = the waiting `RDFAST`'s clocks (RIG:600, RIG:1013) |
| next `RFLONG` returns `$0000_0000` | box CH:6, CH:64, CH:79, CH:188 | L1/L2:1486 `zero 1_024`; L1/L2:1487 |
| failing spacing 8 to 15 clocks; each in exactly 8 of 64 | CH:65, CH:79 | L1/L2:1487 `wrong up to gap 15 clk`; detail lines `dist 8`..`dist 15` |
| exactly one spacing failed per alignment, all 16 trials | CH:64 | every E_REBLK `cls` string has exactly one `Z` |
| every other spacing: waited 10 to 17 clocks | CH:66 | every `exc` string only `A`..`H` (= 10..17, RIG:809–812) apart from the single `2` |
| 1,024 of 43,008 wrong, 41,984 correct | CH:68 | L1/L2:1486–1487 |
| 64 alignments, 42 spacings, 16 trials; 3 unreachable | CH:62, CH:177 | RIG:210–214, RIG:82–87; L2:23 |
| waiting alone: 3,072 of 3,072, `RFLONG`/`RFWORD`/`RFBYTE`, 10..17 | CH:70 | L1/L2:1511–1512 |
| zero flags C clear Z set in every failing trial printed | CH:79 | E_REBLK detail lines `cz 2` |
| second `RFLONG`: slices 0–2 first long, 3–7 zero | CH:79 | detail lines `v2` (L2:1352–1398 vs 1400–1478); LO:286–413 E7N `v2` the same |
| 16..44 correct in every alignment | CH:83 | every `cls` all `.` from j13 |
| no-wait read alone first correct at 8..15 (the anti-pattern case) | CH:35 | L1/L2:1498–1499, 1509 |
| failing spacing by starting point 10, 9, 8, 15, 14, 13, 12, 11; same for every slice; equals first correct no-wait read | CH:152, CH:185–186 | L2:1352–1366; B_NW slice-0 rows L1/L2:490, 497, 503, 516, 528, 539, 549, 558 |
| slice 0 start 0: 7→13, 8→12, 9→11, 10→2, 11→17, 12→16 | CH:152, CH:190–193 | L1/L2:1353 `exc AGFEDCB2HGFE...` (codes RIG:801–814) |
| regions, patterns, loading, sync read, sweep, GETCT arithmetic | CH:177 | RIG:61–70, 234–236, 1272–1276, 1456–1467, 599–600; L1/L2:1483 PHASE CHECK |
| controls; every control correct both runs | CH:179 | L1/L2:1481 `RIG OK: …`; no `RIG FAIL` |
| 2026-09-25, twice, same result | CH:197 | L1:1, L2:1 |
| spacing workaround test: `WAITX #12` 16 clocks, positive control, 29,696, 1,024 of 1,024, 10..17 | CH:130, CH:195 | see *The spacing workaround run (LF)* below |

## Where the chapter departs from the ledger's wording

- EF-084's "16 clocks prevents both": corrected in the ledger; writes at 16 clocks are EF-088.
- EF-084/086/087 say "E8"; the chapter says E7 throughout (the merge).
- LED "arming" (EF-074 title) is not a P2 Documentation term; the chapter states spacings.
- EF-086 "the cog then stopped responding" / EF-087 "the cog does not finish": the chapter says
  "did not finish within 1 s" and "can stop responding", and leaves the cause unknown (CH:141,
  CH:156).
- The Spin2 interpreter's use of the waiting form only (RO header, arbiter-verified) is not in the
  chapter: it is not a Parallax documentation statement and was not measured on silicon.

## The spacing workaround run (LF), re-derived from the per-cell lines

Carried over from the 2026-09-26 sidecar (task «#359»/«#360»). Chapter positions CH:130, CH:195.

| Chapter claim | Raw LF lines |
|---|---|
| ran 2026-09-26, once; 200 MHz | LF:1, LF:20 |
| the `.bin` that ran is the rig on disk | LF:14 (`e7-fix-rdfast-spacing-test.bin`, 19215 bytes, mtime = on-disk) |
| controls: GETCT/WAITX arithmetic; `WAITX #12` = 16 clocks; RDLONG pattern; primed FIFO; late no-wait read | LF:29–92; LF:93–157; LF:159–222; LF:224–287; LF:289–352; LF:549 |
| positive control: one failing spacing per alignment, same spacings, 1,024 of 43,008 | LF:355–482; LF:552–553 |
| 16..44: first and second read correct, 29,696 | LF:555 |
| the spaced arrangement: 1,024 of 1,024, first long then the next | LF:484–547 (`F_FIX … ok 16/16 OK v2bad 0`), LF:556 |
| waiting `RDFAST` 10..17 clocks, 8 different times per slice | LF:484–547 `exc` values; LF:551 PHASE CHECK |

Not in LF and so not claimed: a second run of the spacing workaround test; its C/Z; the board's
identity.
