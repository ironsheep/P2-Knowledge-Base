# E7 sources: Erratum E7, A Blocking RDFAST Can Skip Its Wait After a No-Wait RDFAST

Verification sidecar for `opus-master/e7-rdfast-blocking-after-no-wait.md` (CH below). Every
number, quotation and code excerpt in the chapter maps to a file and line below. Internal
document: ids and paths are allowed here, never in the chapter. Written 2026-09-26 (task «#359»,
v0.2.0 shape). Updated the same day when the workaround test ran (log **LF** below); its numbers
were re-derived from LF's per-cell lines, not from its verdict lines (section *The workaround
run*). No `PENDING-BENCH` comment remains in the chapter.

**Workaround wording (2026-09-26, task #360; Stephen's decision, voice-guide §2).** The reader's
change is a *workaround*, never a *fix* (a fix is a silicon revision). Section *The fix*
(`{#sec-e7-fix}`) is now *A proven workaround* (`{#sec-e7-workaround}`), rule-first: *What any
workaround must do* (CH:51, the condition, as in the front matter's summary table), *One way,
proven on P2 hardware* (CH:53) and the block, then *Other ways that meet the condition* (CH:71).
The CAUTION box's third line is *Workaround* (the condition only; the `WAITX` detail moved to
*One way*); the status row is *Workaround proven on silicon*. **Every `CH:` number below is the
post-#360-wording chapter's** (they had lagged the chapter by three lines since the #360 block
conformance; all were remapped here). FIX's reader copy is renamed
`e7-workaround-rdfast-spacing-test.spin2` (ARCHIVE-WKR); its `FIX_WAITX`/`FIX_GAP_CLK`/
`fixExcess`/`fixBad`/`verdict_fix` are renamed `WKR_WAITX`/`WKR_GAP_CLK`/`wkrExcess`/`wkrBad`/
`verdict_wkr`, the block markers read `E7 WORKAROUND BLOCK`, and comments and `debug()` text say
*workaround* (the verdict line now opens `VERDICT E7 WORKAROUND:`). The arm names `K_FIXCLK` and
`F_FIX` (printed `string()` literals) were then renamed by the arbiter to `K_WAITCLK` and
`W_BLOCK`, with `AR_KWAITCLK`/`AR_WBLOCK`/`v_kwaitclk`/`v_wblock`/`bWaitClkOk` that name them
(Spin2 string data, allowed under ruling R15): the 688-byte measuring PASM image (object
$0B4-$363) is byte-identical before and after, checked byte by byte from the two listings; the
method table and Spin2 string area moved by 23 bytes. No line added or removed, so every
ARCHIVE-WKR line number below still holds. In the as-run log the same arms print as `K_FIXCLK`
and `F_FIX`; the bench re-run of the reader copy prints `K_WAITCLK` and `W_BLOCK`. FIX and LF
are the as-run record and keep their own wording.

## Abbreviations

| Tag | File |
|---|---|
| **DOC** | `engineering/ingestion/sources/silicon-doc/p2-documentation.txt` |
| **DOCX** | `engineering/ingestion/sources/silicon-doc/Parallax Propeller 2 Documentation v35 - Rev B_C Silicon.docx`, member `word/comments.xml` (read with `unzip -p`) |
| **SE** | `engineering/ingestion/SOURCE-ERRATA.md` (E-015 at 492–515) |
| **LED** | `engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md` (EF-073 at 1056–1078, EF-074 at 1080–1096) |
| **RIG** | `engineering/document-production/manuals/p2-errata/audit/verification-tests/test-rdfast-wrfast-readiness-boundary.spin2` (reader name `e7-rdfast-blocking-after-no-wait-test.spin2`); byte-identical to the tracked campaign copy `engineering/ingestion/external-sources/hardware-verification/campaigns/2026-09-p2-errata-predictions/tests/test-rdfast-wrfast-readiness-boundary.spin2` (`cmp` printed nothing) |
| **FIX** | `engineering/document-production/manuals/p2-errata/audit/verification-tests/e7-fix-rdfast-spacing-test.spin2` (the as-run name; the reader's copy is `e7-workaround-rdfast-spacing-test.spin2` since #360). **Untracked** (`audit/` is git-ignored; `git ls-files --error-unmatch` fails on it). Ran once, log LF |
| **LF** | `.../audit/verification-tests/logs/debug_260926-015823.log` (the workaround run, 2026-09-26 01:58:23 local, 561 lines of content + trailing blank; LF:14 `[DOWNLOAD TO RAM] File: e7-fix-rdfast-spacing-test.bin \| Size: 19215 bytes \| Modified: 2026-09-26T07:55:16.153Z`, which equals the on-disk `.bin` (19215 bytes, mtime 2026-09-26 07:55:16.153Z by `ls -l --time-style=full-iso`), built after the `.spin2` (mtime 05:07:40Z)) |
| **L1** | `.../audit/verification-tests/logs/debug_260925-214019.log` (run 1, 2026-09-25 21:40:19; `.bin` 23511 bytes, Modified 2026-09-26T03:39:23.361Z, L1:14) |
| **L2** | `.../audit/verification-tests/logs/debug_260925-214922.log` (run 2, 2026-09-25 21:49:22; `.bin` 23511 bytes, Modified 2026-09-26T03:48:33.316Z, L2:14) |
| **WX** | `deliverables/ai/P2/language/pasm2/waitx.yaml` |

L1 and L2 have the same line numbering for every line cited here (both open with a baud-rate
session, L1:1–8 / L2:1–8; `Cog0` output starts at line 18/16–20). The E_REBLK block is L1:1351–1479
and L2:1351–1479. Read side by side with `grep -o "E_REBLK s[0-7] p[0-7] .*"` on each log (no
timestamps), the 128 E_REBLK row lines were compared and are the same; LED:1083 states "identical in
both runs". The two logs differ in length by one byte: the checksum line, "after 15ms" (L1:17) vs
"after 1ms" (L2:16).

## Quotations

| Chapter text | Source |
|---|---|
| "If D[31] = 0, RDFAST/WRFAST will wait for any previous WRFAST to finish ... so that it can start being used in the next instruction." (CH:17) | DOC:6705–6707, three lines joined with single spaces |
| "If D[31] = 1, RDFAST/WRFAST will not wait ... before any attempt is made to read or write FIFO data." (CH:21) | DOC:6708–6709, two lines joined |
| section name FAST SEQUENTIAL FIFO INTERFACE (CH:15) | DOC:6669 |
| "bit 31 of the D operand" chooses the mode (CH:15) | DOC:6704 ("RDFAST and WRFAST each have two modes of operation.") + DOC:6705/6708 |
| KNOWN BUGS does not list this behaviour (CH:27) | DOC:197–227: two items only (SETQ/ALTx PTRx deltas; ALTx immediate-#S and AUGS) |
| Chip Gracey: "Yes, but I can't explain it well." (CH:27) | DOCX comment `w:id="1"`, `w:author="Chip Gracey"`, `w:date="2024-12-11T05:03:11Z"`; full text "Yes, but I can't explain it well. Would you mind writing something here and I'll approve it when you're done?". Anchor = the KNOWN (SILICON) BUGS heading: SE:497, harvest `sources/silicon-doc/reviewer-comments-harvest-2026-08-26.md:21` |
| "replying to a note that an `RDFAST` corruption bug should be listed there" (paraphrase, not quoted) | DOCX comment `w:id="0"`, author Wuerfel21 (community; not named, not quoted): "Should add the RDFAST corruption bug here" |
| "The comments do not describe the conditions or the symptom." | DOCX ids 0–4 read in full: id 2 (Wuerfel21) "I mean, me neither. I just noticed that it happens. It's probably easier to figure out looking at the actual RTL logic"; id 3 (Chip Gracey, 2025-01-02) "Or just allow enough clock cycles before using the FIFO, like the instruction mode requires."; id 4 (Wuerfel21) "It's still a bug though". SE:507–511 ("What is NOT established: the mechanism") |
| "plausibly that bug; nothing in the comments establishes it" | LED:1091–1092 ("This is plausibly the bug Chip Gracey confirmed without explaining"); stated no stronger. Chip's id-3 mitigation is **not** carried: it speaks of allowing clocks "before using the FIFO", which reads as the no-wait read requirement (class 2), not as the RDFAST-to-RDFAST spacing, and carrying it would imply a link the thread does not make |

## Numbers

| Chapter number | Where | Source |
|---|---|---|
| `D[31]` = 0 blocking, `D[31]` = 1 no-wait | box, CH:15–23 | DOC:6705, DOC:6708 |
| blocking `RDFAST` "takes 2 clocks without waiting" at the failing spacing | box, CH:33, CH:125, CH:129 | every E_REBLK detail line, L1/L2:1352–1478 (even lines): `el X..X base X-2`, e.g. L2:1352 `el 16..16 base 14`; exc = the blocking RDFAST's clocks (RIG:600, RIG:1013); the `2` in every E_REBLK `exc` string (L1/L2:1353–1479 odd lines); LED:1084–1085 |
| next `RFLONG` returns `$0000_0000` | box, CH:6, CH:33, CH:43, CH:125 | L2:1352 etc. `zero 16 ... v1 $0000_0000`; L1/L2:1486 `zero 1_024`; L1/L2:1487 `got $0000_0000 expected $A5A5_0080`; LED:1085 |
| failing spacing 8 to 15 clocks | box, CH:11, CH:34, CH:43, CH:45, Status | L1/L2:1487 `wrong up to gap 15 clk`; detail lines `dist 8`..`dist 15` (L2:1356 `j5 dist 8`, L2:1358 `j12 dist 15`); LED:1086 |
| "exactly one spacing failed, in all 16 trials" in every alignment | CH:33 | every E_REBLK `cls` string (L1/L2:1353–1479 odd) has exactly one `Z` and 41 `.`; every detail line `zero 16`; LED:1083–1084 |
| each of 8..15 "in exactly 8 of the 64 alignments" | CH:34, CH:45 | per-phase mapping below × 8 slices; LED:1086–1087 ("falls on each of 8..15 clocks exactly eight times") |
| failing spacing by starting point p (table row 1, CH:122): p0 10, p1 9, p2 8, p3 15, p4 14, p5 13, p6 12, p7 11, same for every slice | CH:89, CH:122 | detail lines: `s0 p0 j7 dist 10` (L2:1352), `s0 p1 j6 dist 9` (1354), `s0 p2 j5 dist 8` (1356), `s0 p3 j12 dist 15` (1358), `s0 p4 j11 dist 14` (1360), `s0 p5 j10 dist 13` (1362), `s0 p6 j9 dist 12` (1364), `s0 p7 j8 dist 11` (1366); slices 1–7 repeat the same p→dist at L2:1368–1478 (and L1 same lines) |
| first correct no-wait read, slice 0, by p (table row 2, CH:123): 10, 9, 8, 15, 14, 13, 12, 11 | CH:91, CH:123 | B_NW slice-0 `cls` rows, count of leading `Z` = first all-correct j: L1/L2:490 (p0, 7 Z → j7 → 10 clk), :497 (p1, 6 → j6 → 9), :503 (p2, 5 → 8), :516 (p3, 12 → j12 → 15), :528 (p4, 11 → 14), :539 (p5, 10 → 13), :549 (p6, 9 → 12), :558 (p7, 8 → 11). j → clk by RIG:562–565 |
| the no-wait RDFAST's address is a slice-0 long in every trial | CH:81, CH:89, CH:103 | RIG:1459 `rdfast c_nowait, c_midb`; `c_midb` = midBase (RIG:1220, mbox MB_MID), aligned to 32 bytes (RIG:436); slice = address bits [4:2] (RIG:62–64; DOC:6634–6635) |
| B_NW uses a slice-0 address for s = 0 (the comparison row) | CH:91 | RIG:1372 `rdfast c_nowait, c_new`, `c_new` = new base + 4*s (RIG:1232–1235), s = 0 → slice 0 |
| at every other spacing, blocking `RDFAST` waited 10 to 17 clocks | CH:35, CH:69 | every E_REBLK `exc` string (L1/L2:1353–1479 odd) contains only `A`..`H` (= 10..17, RIG:809–812) apart from the single `2` |
| 41,984 correct, 1,024 of 43,008 wrong, all zero; mid 0, stale 0, old 0 | CH:33, CH:37, CH:125 | L1/L2:1486 `E_REBLK by class: ok 41_984 flg 0 stale 0 old 0 mid 0 nsh 0 zero 1_024 oth 0`; L1/L2:1487 `DEVIATES - 1_024 of 43_008 reads wrong (mid = first RDFAST's data 0, stale 0)` |
| 64 alignments, 42 spacings, 16 trials, 43,008 | CH:31, CH:104 | RIG:210–214 (NSLICE 8, NPHASE 8, NDIST 42, TRIALS 16); L2:20 header `16 trials per cell, 8 slices x 8 phases`; L1/L2:1487 `of 43_008` |
| spacings 2 and 4..44, 3 unreachable, "every instruction takes at least 2 clocks" | CH:31, CH:45, CH:104 | RIG:82–87 ("Distance 3 is not reachable in cog exec (every instruction is >= 2 clk)"); L2:23 `j=0 ... distance 2 clk; j>=1 WAITX c_dly=j-1, distance j+3 clk (3 clk unreachable)` |
| spacing counted from start to start, no-wait RDFAST's 2 clocks included | CH:31, CH:51, CH:65, CH:69 | RIG:556–565 `distclk` ("Issue-to-issue clocks"); FIX:46–49 |
| spacings 2 and 4..7 correct in every alignment | CH:45 | every E_REBLK `cls` string begins with at least five `.` (j0..j4 = 2, 4, 5, 6, 7 clk; first `Z` at j5 earliest, L2:1357) |
| 16..44 correct in every alignment and trial | CH:45, CH:69, CH:125 | every `cls` string is all `.` from j13 (16 clk) to j41 (44 clk); L1/L2:1487 `wrong up to gap 15 clk`; LED:1093–1094 ("every gap from 16 to 44 clocks read correctly in every cell") |
| "one more than the largest failing spacing measured" | CH:65 | 16 − 15; L1/L2:1487 |
| C clear, Z set in every failing trial printed | CH:43 | every E_REBLK detail line ends `cz 2` (flags bit 0 = C, bit 1 = Z: RIG:245, RIG:1464–1465); the detail line shows one record per row (`rowShowRec`, RIG:917–918, the first failing trial) |
| the read does not stall | CH:43 | detail lines: `el` = `base` + 2, where base includes the RFLONG's 2 clocks (RIG:600); the 2 extra clocks are the blocking RDFAST's (RIG:1013) |
| second `RFLONG`: slices 0–2 returned the first long at the address, slices 3–7 `$0000_0000` | CH:47 | detail lines `v2`: s0 `$A5A5_0080` (L2:1352–1366), s1 `$A5A5_0081` (1368–1382), s2 `$A5A5_0082` (1384–1398) = new[s] (pattern RIG:70); s3..s7 `v2 $0000_0000` (L2:1400–1478). Same in L1. One trial per cell (RIG:960 prints `rowShowRec`) |
| data regions unchanged, re-checked after every alignment | CH:47 | RIG:383–387 (`region_damage()` after every row); no `REGION DAMAGE` / `RIG NOTE` line in L1 or L2 (`grep -c` = 0 on both) |
| blocking alone: 3,072 of 3,072, RFLONG/RFWORD/RFBYTE, 10..17 clocks | CH:39 | L1/L2:1511 `A (blocking) over3_072 trials: RDFAST clocks 10..17 ... ok 3_072`; L1/L2:1512 `CONFIRMED-PROMISE-HOLDS - all 3_072 ...`; LED:1065–1067 |
| second no-wait RDFAST, `WAITX #200` before the read, 43,008 of 43,008 | CH:39 | RIG:1430–1442 (`v_ren`: `waitx #LATE_WAIT`, LATE_WAIT = 200 at RIG:226); L1/L2:1484 `E_RENW by class: ok 43_008`; L1/L2:1485 `HOLDS ... all 43_008 trials`; LED:1073–1074 |
| no-wait read alone: zero, first correct spacing 8 to 15 | CH:25 | L1/L2:1498 `zero 8_704 ... of 43_008`; L1/L2:1499 `ZERO - all 8_704 wrong no-wait reads returned zero`; L1/L2:1509 `per-slice min..max clocks s0 8..15 ... s7 8..15`; LED:1067–1071 |
| slice 0, starting point 0 example: spacing 7→13, 8→12, 9→11, 10→2 (zero), 11→17, 12→16 | CH:91, CH:127–130 | L1/L2:1353 `E_REBLK s0 p0 cls .......Z.... exc AGFEDCB2HGFE...`: j4 `D`=13, j5 `C`=12, j6 `B`=11, j7 `2`, j8 `H`=17, j9 `G`=16 (codes RIG:801–814); j → clk RIG:562–565 |
| `D` = `$8000_0000` for the no-wait RDFAST | CH:31, CH:67, CH:152 | RIG:1502 `c_nowait long $8000_0000`; RIG:178–179 (opcode check); FIX:1181 |
| blocking `RDFAST #0` | CH:31, CH:103 | RIG:1461 `rdfast #0, c_new`; RIG:177 |
| block count 0, no wrap | CH:67, CH:81 | RIG:1502 comment ("0 blocks = no wrap"); DOC:6674–6675 ("just use 0 for the block count, so that wrapping won't occur") |
| 200 MHz | CH:83, CH:99, Status | RIG:207; L2:20 `clk 200 MHz` |
| cog 1 in both runs; `DEBUG_COGS = %0000_0001` | CH:101 | L1/L2:26 `measuring cog 1 running`; RIG:208 |
| no pins used | CH:99, CH:174 | RIG:34 ("No pins, no jumpers, no instruments") |
| regions 32-byte aligned; long k in slice k mod 8 | CH:102 | RIG:61–64, RIG:434–436; DOC:6634–6635 |
| patterns `$3C3C_00C0`+k, `$A5A5_0080`+k, `$0D0D_0040`+k; stale `$0D0D_0042` | CH:102–103, CH:113 | RIG:70, RIG:234–236; L2:21 |
| prime: blocking RDFAST, `WAITX #64`, two RFLONGs, `WAITX #64` | CH:103 | RIG:1272–1276; RIG:224–225 (PRIME_WAIT 64, SETTLE_WAIT 64) |
| sync RDLONG of a slice-0 long, then WAITX 0..7 | CH:103 | RIG:1456–1457 (`rdlong c_junk, c_oldb`, `waitx c_phase`); RIG:50–51 |
| 8 starting points span a whole rotation: 8 distinct blocking-RDFAST times per slice | CH:104 | L1/L2:1483 `PHASE CHECK ... s0 8 s1 8 ... s7 8`; LED:1062 |
| the blocking RDFAST's clocks = GETCT difference less overhead, spacing, RFLONG | CH:105 | RIG:599–600 (`GETCT_OVH + distclk(distIdx) + INSTR_CLK`) |
| outcome written before the run | CH:107 | RIG:136–142 (header, pre-registered: "EXPECT ... still delivers new[s] ... DEVIATES IF mid ..., stale or other"); printed before the rows at L1/L2:1351; any wrong read counts (RIG:1075, RIG:1085–1086) |
| controls: GETCT pair 2, WAITX 2+D at every swept delay; RDLONG pattern; primed FIFO `$0D0D_0042` then next; no-wait + `WAITX #200` read | CH:111–114 | RIG:94–103; L2:27, 92, 157, 222 (arm headers) |
| write controls passed; every control correct both runs | CH:116 | L1/L2:1481 `RIG OK: K_CLOCK, K_RDLONG, K_PRIME, K_NWLATE, K_WBLK, K_WLATE all correct in every trial`; no `RIG FAIL` / `NO VERDICT` in either log (`grep -c` = 0) |
| 2026-09-25, run twice, same result | CH:132, Status | L1:1, L2:1; LED:1083 ("identical in both runs") |
| `WAITX #12` = 2 + 12 = 14 clocks; 16 = 2 + 14 | CH:53, CH:65, CH:69, CH:73 | WX:8, WX:10, WX:76 (`2 + D`); RDFAST no-wait 2 clocks DOC:6708; K_CLOCK control measured WAITX = 2 + D at D = 12 (j13) in the erratum test (L1/L2:1481); FIX:55–56 |
| erratum test's spacing set by `WAITX` register operand 12 to 40 for 16..44 | CH:69 | RIG:1460 `waitx c_dly`, `c_dly` = j − 1 (RIG:1248–1251); j = 13..41 → 12..40 |
| 1,024 trials of the workaround (8 × 8 × 16) | CH:69, CH:138 | FIX:125–126 ("in every trial of every cell (1,024 trials)"); LF:484–547 (64 `F_FIX` lines × `ok 16/16`) |
| `INSTR_CLK` 2, `NW_WAITX_OFFSET` 4 | CH:172 | RIG:230, RIG:232 |
| second `ARM-VERDICT` line reads `DEVIATES`, 1,024 of 43,008 | CH:174 | L1/L2:1485 (first, E_RENW), L1/L2:1487 (second, E_REBLK) |
| workaround test: marker comments, positive control, `WAITX #12` = 14 control, `VERDICT E7 WORKAROUND:` | CH:176 | FIX:33–43, FIX:105–108 (K_FIXCLK "elapsed 16 = 2 + (2 + 12)"), FIX:115–122, FIX:137–145 (INCONCLUSIVE if the positive control does not reproduce), FIX:1151/1156 markers (ARCHIVE-WKR:1097/1105), FIX:995–1006 verdict lines (FIX prints `VERDICT E7 FIX:`; ARCHIVE-WKR:942–953 print `VERDICT E7 WORKAROUND:` since #360, DEBUG text only) |
| *What any workaround must do*: at least 16 clocks from the start of the no-wait `RDFAST` to the start of the blocking one | CH:51 | the 16..44 rows above (L1/L2:1487 `wrong up to gap 15 clk`; every `cls` all `.` from j13); LED:1093–1094; front matter summary table |
| *Other ways*: other instructions filling at least 16 clocks meet the same condition, since the measurements tie the failure to the spacing, not to the `WAITX`; not run: only `WAITX` between the two `RDFAST`s, hub-waiting instructions untested | CH:71 | the failing spacing depends only on the spacing and the alignment (CH:89; rows above), and was the same with a register `WAITX` (RIG:1460, erratum test) and an immediate one (FIX, LF); no other instruction between the two `RDFAST`s in RIG (RIG:1456–1467) or FIX (FIX:1150–1157); limits CH:77 |

## The drop-in block (A proven workaround)

**Printed code now mirrors the conformed archive copy (2026-09-26, «#360»); the measuring PASM
is byte-identical to the as-run rig.** ARCHIVE-WKR = `examples-library/e7-workaround-rdfast-spacing-test.spin2`
(renamed from `e7-fix-rdfast-spacing-test.spin2` later in #360, lines unchanged; conformed
2026-09-26, task #360: a new `CON` part names `RDFAST_SPACING_WAITX` (12) in place of the literal
`#12`; same instructions, same PASM measuring image, byte-identical to FIX's).

| | |
|---|---|
| Chapter | CH:56–62, the `pasm2` fence under *One way, proven on P2 hardware* in *A proven workaround* (seven lines post-#360, four pre-#360) |
| Source | ARCHIVE-WKR:1098–1104 (post-#360), between the markers ARCHIVE-WKR:1097 (`' ---- E7 WORKAROUND BLOCK: begin ...`) and ARCHIVE-WKR:1105 (`' ---- E7 WORKAROUND BLOCK: end ----`; both read `E7 FIX BLOCK` before the #360 wording change). Pre-#360: FIX:1152–1155, between the markers FIX:1151/1156. Byte-identical (post-#360: verified by `engineering/tools/verify-example-corpus-identity.py`, GREEN; pre-#360: widths 64, 72, 67, 65 on both sides); no tab characters in FIX or ARCHIVE-WKR (`grep -c -P "\t"` = 0) |
| Registers | FIX:1181–1184; ARCHIVE-WKR:1130–1133 (same names, different line): `nowait long $8000_0000`, `hub_first` (mid[0]), `hub_next` (new[s]), `first_long` |
| The run that proved it | LF (2026-09-26, run once): the block's lines FIX:1152–1155 ran as the `F_FIX` arm (FIX:1147–1161, `v_fix`), LF:483–547; 1,024 of 1,024 trials correct, first and second read. Details in *The workaround run* below. Reported in CH:69, CH:134–138, CH:186. LF ran the FIX build (pre-#360 literal `#12`), and the #360 renames left the measuring PASM byte-identical, so the verdict still applies to ARCHIVE-WKR. The erratum test's own basis (every spacing 16..44 correct in all 64 cells × 16 trials, L1/L2:1353–1479; spacing set there by `waitx c_dly`, a register) is kept in CH:69 alongside |
| Kind | rule at each use (CH:65); FIX:42–43 ("Guarantee the chapter prints: at least 16 clocks from the no-wait RDFAST to the blocking RDFAST") |

## Code excerpts (verbatim, contiguous; printed lines now mirror ARCHIVE)

ARCHIVE = `examples-library/e7-rdfast-blocking-after-no-wait-test.spin2` (the erratum test;
conformed 2026-09-26, task #360; the three excerpts below are unaffected in content — only the
line numbers moved, since the file's header comment was rewritten).

| Chapter excerpt | RIG/FIX lines (as-run, history) | ARCHIVE lines (printed) | Max width |
|---|---|---|---|
| Drop-in block (post-#360: `CON`/`DAT` + 4 instruction lines, 7 lines) | FIX:1152–1155 | ARCHIVE-WKR:1098–1104 | 75 |
| `v_rebn rdlong c_junk, c_oldb` / `waitx c_phase` / `getct c_t0` (CH:147–149; unchanged by #360, archive line differs — header rewritten) | RIG:1456–1458 | ARCHIVE:1383–1385 | 38 |
| `rflong c_r1 wcz` ... `jmp #post_read` (CH:155–160; unchanged by #360, archive line differs) | RIG:1462–1467 | ARCHIVE:1389–1394 | 59 |
| `if distIdx == 0` ... `NW_WAITX_OFFSET + distIdx - 1` (CH:166–169; unchanged by #360, archive line differs) | RIG:562–565 | ARCHIVE:463–466 | 45 |
| inline, not a fence: `rdfast c_nowait, c_midb`, `waitx c_dly`, `rdfast #0, c_new` (CH:152) | RIG:1459–1461, instruction fields only; the lines are 88, 29 and 88 columns with their comments, so they cannot be fenced within K = 76 and are named inline, not excerpted | ARCHIVE:1386–1388 (same widths) | n/a |

Byte-identity checked by printing both sides:
`awk '/^```/ { inb = !inb; print NR "----"; next } inb { printf "%d|%d|%s|\n", NR, length($0), $0 }' <CH>`
and
`awk '(NR>=1444 && NR<=1467) || (NR>=556 && NR<=565) {printf "%d|%d|%s|\n", NR, length($0), $0}' <RIG>` and
`awk '(NR>=1152 && NR<=1155) {printf "F%d|%d|%s|\n", NR, length($0), $0}' <FIX>`.

No harness: the chapter carries no snippet that is not taken verbatim from RIG or FIX, so nothing
was compiled for this chapter.

## *Why it happens*: basis

No study material exists for E7 (it was not predicted; LED:1091, front matter). The section states
only what the logs show, and says what is not known:

- "The failing spacing follows the no-wait RDFAST": the no-wait address is mid[0] (slice 0) in every
  cell (row above), and the failing j depends on p only, identical across s = 0..7 (L2:1352–1478).
- "coincides with the arrival of the no-wait RDFAST's data": the B_NW slice-0 first-correct j equals
  the E_REBLK failing j at every p (table rows, sources above). This is LED:1087–1088's reading
  ("fooled when it is issued at the moment the earlier no-wait fill begins arriving"), stated in
  terms of the measured comparison.
- "One clock earlier and one clock later, it waits as usual": the `exc` characters either side of the
  `2` are in `A`..`H` in every row. **Departs from LED:1088–1089** ("One clock earlier it waits 12,
  11…; one clock later it waits the full 17"): the "full 17" holds in slice 0 only; e.g. L2:1369
  (`s1 p0 ... exc BHGFEDC2AHGF...`) has `A` = 10 after the `2` and `C` = 12 before it. The chapter
  gives the slice-0, p0 values (11, 2, 17) as an example only.

## Where the chapter departs from the ledger's wording

- LED:1080 title says "while a no-wait RDFAST is still arming". "Arming" is not a P2 Documentation
  term; the chapter states the measured spacing (8 to 15 clocks) instead.
- LED:1088–1089 "one clock later it waits the full 17": see above; slice 0 only.
- LED:1093–1094 workaround "more than 15 clocks": the chapter states the condition as at least
  16 clocks, prints the workaround block (16 clocks) and the 16..44 basis.
- LED:1091 "pending the chapter's own reproducer": the erratum test is the reproducer for the
  defect (two runs); the workaround test also reproduced it, as its positive control, in its one
  run (LF).
- The chip revision is not stated (brief); the front matter states it once.
- Scope qualifiers carried from the task and LED:1094–1095: `WRFAST` twin not tested; first RDFAST
  blocking not tested as a workaround; instructions between the two RDFASTs other than `WAITX`
  (in particular hub-stalling ones) not tested (CH:77–79; and in *Other ways*, CH:71). Further qualifiers the rig earns: only RFLONG
  as the read in this arrangement (RIG:1462); no streamer (no `xinit`/`xcont`/`xzero` in RIG); block
  count 0 (RIG:1502); spacings above 44 not tested (RIG:213); cog execution, one measuring cog,
  200 MHz (CH:80–83).

## The workaround run (LF), re-derived from the per-cell lines

The verdict was re-derived from LF's per-cell lines before any summary line was read. The
summary lines (LF:549–558) agree with the per-cell derivation; they are cited only as agreement.
The three `PENDING-BENCH e7-fix` comments (CH:62, CH:125, CH:173 of the first draft) were
replaced by the text now (post-#360 wording) at CH:69, CH:134–138 and CH:186.

**Where the workaround test prints a per-cell detail line.** FIX:730: for a swept arm, a detail line is
printed for a spacing when `rowGood < TRIALS or rowV2Bad > 0`, i.e. when any first read OR any
second read at that spacing was wrong. So a cell with one detail line has every other spacing
correct in all 16 trials, first and second read.

| Chapter claim | Where | Raw LF lines (verbatim excerpt) |
|---|---|---|
| ran 2026-09-26, once; 200 MHz | CH:69, CH:134, CH:186 | LF:1 `=== Debug Logger Session Started at 2026-09-26T01:58:23.581 ===`; LF:20 `... (pnut-ts v1.55.8, clk 200 MHz, 16 trials per cell, 8 slices x 8 phases) ===`; one log for this program in `logs/` |
| the `.bin` that ran is the rig on disk | (sidecar only) | LF:14 `File: e7-fix-rdfast-spacing-test.bin \| Size: 19215 bytes \| Modified: 2026-09-26T07:55:16.153Z` = on-disk `.bin` size and mtime |
| same regions, loading, 64 alignments | CH:134 | LF:22 `patterns: new[k]=$A5A5_0080+k  old[k]=$0D0D_0040+k  mid[k]=$3C3C_00C0+k  stale reference old[2]=$0D0D_0042; hub_first=mid[0], hub_next=new[s]`; FIX:77–84 (trial = the erratum test's); LF:20 `8 slices x 8 phases` |
| control: GETCT pair 2, WAITX 2+D at every swept delay | CH:136 ("the four above") | LF:29–92, 64 lines, every one `cls .......................................... exc ..........................................` (42 `.` each: elapsed = expected at every j, every trial) |
| control: `WAITX #12` between two GETCTs = 16 clocks, every trial | CH:136 | LF:94–157, 64 lines, every one `ok 16/16 OK el 16..16 expected 16` (e.g. LF:94 `K_FIXCLK s0 p0: ok 16/16 OK el 16..16 expected 16`); header LF:93 `MUST: elapsed 16 = GETCT 2 + WAITX 2+12` |
| control: RDLONG pattern | CH:136 | LF:159–222, 64 lines `ok 16/16 OK v2bad 0`, v1/v2 = new[s], new[s+1] (e.g. LF:159 `v1 $A5A5_0080 v2 $A5A5_0081`) |
| control: primed FIFO returns `$0D0D_0042` then the next long | CH:136 | LF:224–287, 64 lines `ok 16/16 STALE v2bad 0 el 4..4 exc 0..0 v1 $0D0D_0042 v2 $0D0D_0043 cz 0` |
| control: no-wait RDFAST + `WAITX #200` + RFLONG | CH:136 | LF:289–352, 64 lines `ok 16/16 OK v2bad 0 el 208..208 exc 0..0`, v1/v2 = new[s], new[s+1] |
| every control correct in every trial | CH:136 | the four blocks above, 320 lines; LF:549 `RIG OK: K_CLOCK, K_FIXCLK, K_RDLONG, K_PRIME, K_NWLATE all correct in every trial` (agreement); no `RIG FAIL` / `NO VERDICT` line in LF |
| positive control: exactly one failing spacing per alignment | CH:137 | LF:356–482, the 64 `P_UNSPACED ... cls` lines (even lines): each has exactly one `Z`, all other 41 characters `.`; exactly one detail line per cell (LF:355–481 odd lines), so no other spacing had a wrong first or second read (FIX:730) |
| at the same spacings as in the erratum test (table above) | CH:137 | detail lines give p0 `j7 gap 10`, p1 `j6 gap 9`, p2 `j5 gap 8`, p3 `j12 gap 15`, p4 `j11 gap 14`, p5 `j10 gap 13`, p6 `j9 gap 12`, p7 `j8 gap 11`, for every slice (e.g. LF:355 `P_UNSPACED s0 p0 j7 gap 10`, LF:361 `s0 p3 j12 gap 15`, LF:481 `s7 p7 j8 gap 11`); identical to L1/L2:1352–1478. Each of 8..15 in 8 cells (LF:553 `8 clk 8, 9 clk 8, ... 15 clk 8`, agreement) |
| all 16 trials `$0000_0000`, blocking RDFAST 2 clocks | CH:137 | every P_UNSPACED detail line `ok 0 flg 0 stale 0 old 0 mid 0 nsh 0 zero 16 oth 0 v2bad 0 el X..X base X-2 v1 $0000_0000` (e.g. LF:355 `el 16..16 base 14`); every `exc` string has a single `2` at the `Z` position, all else `A`..`H` |
| 1,024 of 43,008 reads wrong | CH:137 | 64 cells × 16 (above); LF:552 `P_UNSPACED by class: ok 41_984 flg 0 stale 0 old 0 mid 0 nsh 0 zero 1_024 oth 0 of 43_008` (agreement) |
| spacings 16..44: first read and the long after it correct in all 29,696 trials | CH:137 | every `cls` string is `.` at j13..j41 (29 spacings) and no detail line exists there (FIX:730 covers the second read): 64 × 29 × 16 = 29,696; LF:555 `first read correct in 29_696 of 29_696 trials; second read wrong after a right first read in 0` (agreement) |
| the printed block: first long, then the long after it, 1,024 of 1,024 | CH:69, CH:138 | LF:484–547, 64 `F_FIX` lines, every one `ok 16/16 OK v2bad 0`, `v1` = new[s] and `v2` = new[s+1] (e.g. LF:484 `F_FIX s0 p0: ok 16/16 OK v2bad 0 el 32..32 exc 12..12 v1 $A5A5_0080 v2 $A5A5_0081 cz 0`; LF:547 `F_FIX s7 p7: ... v1 $A5A5_0087 v2 $A5A5_0088`); LF:556 `ok 1_024 ... of 1_024 (oth includes a right first read with a wrong second: 0)` (agreement) |
| "with nothing else between its lines" | CH:138 | FIX:1147 (`'--- F_FIX: the printed drop-in block, timed; nothing else sits between its lines`), FIX:1150–1157 |
| blocking RDFAST in the block waited 10 to 17 clocks | CH:69, CH:138 | the 64 `F_FIX` lines' `exc` values span `exc 10..10` (e.g. LF:486) to `exc 17..17` (e.g. LF:487), each cell a single value; exc = the blocking RDFAST's own clocks (LF:26, FIX:99–100); LF:556 `blocking RDFAST took 10..17 clk` (agreement) |
| 8 different times over the 8 starting points in every slice | CH:138 | e.g. slice 0, LF:484–491: exc 12, 11, 10, 17, 16, 15, 14, 13; every slice shows all of 10..17 once (LF:484–547); LF:551 `PHASE CHECK ... s0 8 s1 8 ... s7 8` (agreement) |
| verdict (not used as evidence) | — | LF:554 `POSITIVE CONTROL P_UNSPACED: REPRODUCED ...`; LF:558 `VERDICT E7 FIX: CONFIRMED - the printed block (waitx #12, gap 16 clk) read new[s] then new[s+1] in all 1_024 trials ...` |

Not in LF and so not claimed: a second run of the workaround test; any `F_FIX` C/Z (the block reads
without `WCZ`; FIX:1159 records `cz 0`); the board's identity (the chapter says "a P2 board").
