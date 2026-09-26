# E1 verification sidecar: Erratum E1, SETQ Block Transfers Lose Their Pointer Step

Chapter: `opus-master/e1-setq-block-pointer-step.md`. Every number, quotation and code excerpt in
the chapter, mapped to its source. Internal document: ids are allowed here, never in the chapter.

**v0.2.0 reshape (2026-09-26, task #359).** The chapter was restructured to the v0.2.0 shape
(CAUTION box, opening, the eight fixed headings). Section names below are the v0.2.0 headings:
*What the P2 is documented to do* (was *What the design says*), *What the P2 actually does* (was
*What the part does*), *What your program sees* (was *The symptom*), *The fix* (was *The
workaround*), *How it was proven on a real P2* (was *How it was proven*). **The printed fix now
comes from the rig** (§6): it is RIG:484-485, the K_BLK4 control arm that ran on silicon. The
v0.1.0 compile harness HARN is kept unchanged as history; nothing in the v0.2.0 chapter is taken
from it.

**Workaround wording (2026-09-26, task #360; Stephen's decision, voice-guide §2).** The reader's
change is a *workaround*, never a *fix* (a fix is a silicon revision). Section *The fix*
(`{#sec-e1-fix}`) is now *A proven workaround* (`{#sec-e1-workaround}`), rule-first: *What any
workaround must do* (the condition, as in the front matter's summary table), then *One way,
proven on a real P2* and the block. The CAUTION box's third line is *Workaround* (the
condition); the status row is *Workaround proven on silicon*. In ARCHIVE the drop-in labels
read `E1 Workaround:` (ARCHIVE:577, 580) and three comments say *workaround*: text only, no
line added or removed, so every ARCHIVE line number below still holds, and the object image is
byte-identical to the pre-#360 archive (pnut-ts 1.55.8, `-d` and without). Chapter line numbers
below are post-#360. RIG and the logs are the as-run record and keep their own wording.

Path keys:

| Key | Path |
|---|---|
| LEDGER | `engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md` (EF-067 at 916-938; campaign header 884-896) |
| DOC | `engineering/ingestion/sources/silicon-doc/p2-documentation.txt` (Parallax P2 Documentation v35) |
| RIG | `engineering/document-production/manuals/p2-errata/audit/verification-tests/test-o17-setq-altd-block-ptr-delta.spin2` |
| LOG2 | `.../audit/verification-tests/logs/debug_260924-231802.log` (second run, style-conformed build) |
| LOG1 | `.../audit/verification-tests/logs-orig/debug_260924-204717.log` (first run, as-authored build) |
| HARN | `verification/e1-harness-workaround.spin2` (v0.1.0 compile harness; not used by the v0.2.0 chapter) |
| KB | `deliverables/ai/P2/language/pasm2/` |

## 1. Which build the excerpts come from

RIG on disk is the build that produced LOG2. Rebuilt a scratch copy of RIG with pnut-ts 1.55.8
`-d`: 13878 bytes, `cmp`-identical to `audit/verification-tests/test-o17-setq-altd-block-ptr-delta.bin`.
LOG2:14 records the downloaded image:

```
[2026-09-24T23:18:02.401] [SYSTEM] [DOWNLOAD TO RAM] File: test-o17-setq-altd-block-ptr-delta.bin | Size: 13878 bytes | Modified: 2026-09-25T05:16:34.962Z
```

RIG is also byte-identical (`diff -q`, no output) to the replicated copy
`hardware-verification/campaigns/2026-09-p2-errata-predictions/tests/test-o17-setq-altd-block-ptr-delta.spin2`.

Re-checked 2026-09-26 for v0.2.0, after commit `8b5dd8df` renamed study terms in RIG's header
comment (lines 69, 90, 117, 127 only; no line added or removed, so every RIG line number here
still holds): a scratch copy of RIG compiled with `/usr/local/bin/pnut-ts -d` (v1.55.8) wrote
13878 bytes and is `cmp`-identical to `audit/verification-tests/test-o17-setq-altd-block-ptr-delta.bin`;
`diff -q` against the campaign copy prints nothing. The measuring code is the code that ran.

## 2. Quotations of Parallax documentation

| Chapter | Quoted / cited text | Source |
|---|---|---|
| CAUTION *Expected*, "(P2 Documentation, *FAST BLOCK MOVES*)"; block through `ptra++` moves `PTRA` past the whole block, 4 bytes per long | "read x+1 longs from PTRA, PTRA += (x+1)*4" under heading FAST BLOCK MOVES | DOC:7169 (heading), DOC:7232-7239 |
| Opening, "Parallax publishes the defect in the P2 Documentation" | KNOWN BUGS entry | DOC:197-210 |
| Documented, section name *FAST BLOCK MOVES* | heading | DOC:7169 |
| Documented, blockquote 1 | "For fast block moves, PTRx expressions cannot have arbitrary index values, since the index will be overridden with the number of longs, with bit 4 of the encoded index value serving as the ++/-- indicator." | DOC:7220-7221 (sentence ends on 7221 at "indicator."). The chapter sets `++`/`--` in inline code so that LaTeX does not turn `--` into an en-dash; the characters are the source's. |
| Documented, para after quote 1 | `SETQ #x` + `RDLONG first_reg,PTRA++`, "read x+1 longs from PTRA, PTRA += (x+1)*4" | DOC:7232-7239 (instruction and operand columns split by extraction: 7232-7233 mnemonics, 7235-7236 operands, 7238-7239 comments) |
| Documented, `PTRx += INDEX*SCALE` | "U = 0 to keep PTRx same, 1 to update PTRx (PTRx += INDEX*SCALE)" | DOC:6946 |
| Documented, `SCALE` is 4 | "SCALE = 1 for RDBYTE/WRBYTE, 2 for RDWORD/WRWORD, 4 for RDLONG/WRLONG/WMLONG" | DOC:6944 |
| Documented, blockquote 2 | "Intervening ALTx/AUGS/AUGD instructions between SETQ/SETQ2 and RDLONG/WRLONG/WMLONG-PTRx instructions will cancel the special-case block-size PTRx deltas. The expected number of longs will transfer, but PTRx will only be modified according to normal PTRx expression behavior:" | DOC:198-200, section heading KNOWN BUGS at DOC:197. The chapter line carries an invisible U+200B (zero-width space) after five of the slashes (`ALTx/`, `AUGS/`, `SETQ/`, `RDLONG/`, `WRLONG/`; found with `grep -o -P "\w+/\x{200B}"`), carried unchanged from v0.1.0 as line-break points; the visible text is the source's. |
| Documented, example | `SETQ #16-1` ('ready to load 16 longs), `ALTD start_reg`, `RDLONG 0,ptra++`; comment "ptra will only be incremented by 4 (1 long), not 16*4 as anticipated!!!" | DOC:201-210 (extraction splits columns: mnemonics 201/203/205, operands 202/204, comments 206-210; the third comment spans 210 + 206). The chapter paraphrases the example; it does not reproduce it as a quotation. |
| A proven workaround, "the block count overrides the index, as the P2 Documentation states" | "the index will be overridden with the number of longs" | DOC:7220-7221; measured LOG2:115 |

## 3. Numbers

### CAUTION box, opening, What the P2 actually does, What your program sees

| Chapter number | Source |
|---|---|
| CAUTION *Actual*: every long still moves, `PTRA` moves only 4 bytes | LOG2:63 (delta=4, landed=4/4), LOG2:89 (delta=4, landed=8/8); LEDGER:917-919 |
| CAUTION *Workaround*: nothing between the `SETQ`/`SETQ2` and the transfer | LEDGER:933-934; LOG2:50 (the workaround's own run, see §6); DOC:198-200 (the intervening instructions are what cancels the block step) |
| Opening: code that reloads the pointer before its next use is not affected | follows from the defect being confined to the value left in `PTRx` (LOG2:63: before-address correct, data FULL); carried from v0.1.0 *The symptom* |
| `setq #3` + `altd` + `rdlong 0-0, ptra++` advances 4, not 16 | LOG2:63 (hazard +4), LOG2:50 (control +16); RIG:492-494 |
| +4 for `ptra++` | LOG2:63 |
| +4 for `ptrb++` | LOG2:154 |
| +12 for `ptra++[3]` | LOG2:128 |
| 8-long block moved `PTRA` by +4 | LOG2:89 |
| `ALTD` alone + single `RDLONG ptra++` = +4 | LOG2:37 (K_ALTD1) vs LOG2:24 (K_SINGLE) |
| "4 bytes past the start of the block instead of 16" | LOG2:63 vs LOG2:50 |
| Loop consequences (overlapping reads; a `WRLONG` loop overwrites all but the first long of the previous block) | derived from the +4 step at LOG2:63 (read) and LOG2:180 (write); not run as a loop. Carried from v0.1.0 *The symptom* |
| Plain `ptra++` = 4, `ptra++[3]` = 12 (*What the P2 is documented to do*, para after quote 1) | DOC:6944/6946 (INDEX*SCALE); measured LOG2:24 and LOG2:102 |
| Scope: only `ALTD` tested; `AUGS`/`AUGD`/other `ALTx` vendor-named | LEDGER:934-935; RIG:42-58 (arm table: every hazard arm is `altd`) |
| Untested: `WMLONG`, `SETQ2`+`WRLONG`, `ptra--`, `++ptra`, `--ptra` | RIG:42-58 (arm table lists only rdlong/wrlong post-increment forms, and setq2 only with rdlong) |

### A proven workaround

| Chapter number | Source |
|---|---|
| *What any workaround must do*: nothing between the `SETQ`/`SETQ2` and the transfer | DOC:198-200 (intervening instructions cancel the block step); LEDGER:933-934; the adjacent control column, §4 |
| Drop-in block | RIG:484-485 (see §6) |
| "advanced `PTRA` by +16 in every round, with all four longs in place" | LOG2:50, 53, 56, 59 (K_BLK4 rounds 0-3: `delta=16 data=FULL landed=4/4 abad=0 bbad=0`) |
| 8-long read +32 | LOG2:76 (K_BLK8; rounds 79, 82, 85 identical) |
| through `PTRB` +16 | LOG2:141 (K_PTRB) |
| `WRLONG` from cog registers +16 | LOG2:167 (K_WR) |
| `SETQ2` into lookup RAM +16 | LOG2:193 (K_Q2) |
| `ptra++[3]` block +16 | LOG2:115 (K_IDX3) |
| "six transfers above" | the six control arms K_BLK4, K_BLK8, K_PTRB, K_WR, K_Q2, K_IDX3 (RIG:46-57) |
| Workaround proven = SETQ adjacent (the control column) | LEDGER:933-934 |
| No form that keeps the redirect has been run on silicon | RIG:42-58 (the only arms that combine `SETQ`/`SETQ2` with an `ALTD` place the `ALTD` between them; no arm uses an explicit pointer step) |
| Forms not run in the adjacent form either | RIG:42-58 (no `WMLONG`, no `SETQ2`+`WRLONG`, no `ptra--`/`++ptra`/`--ptra` arm) |

### How it was proven on a real P2

| Chapter number | Source |
|---|---|
| bare P2 board, 200 MHz | LEDGER:892-893; LOG2:20 ("clk 200 MHz"); RIG:167 `_clkfreq = 200_000_000` |
| own PASM cog via `COGINIT`; Spin2 interpreter in cog 0 uses `PTRA` as stack pointer | RIG:30-33; RIG:222; LOG2:21 ("measuring cog 1") |
| `DEBUG_COGS = %0000_0001` | RIG:168; LEDGER:890 |
| 15 arms, 4 rounds, interleaved | RIG:37, RIG:170-171; LEDGER:920-921 |
| sentinel `$5E5E_5E5E`, refilled before every arm, pointer reloaded | RIG:38-40, RIG:175; LOG2:21 |
| source long k = `$A5A0_0000` + k; pointer starts at source long 4 | RIG:176-177; LOG2:21 |
| complete block holds `$A5A0_0004` onward | LOG2:64 |
| hazard D field names trap; ALTD target = control's destination | RIG:61-65; RIG:457-459 |
| outcomes fixed before the run | RIG:23-26, RIG:86-93; LEDGER:891 |
| controls gate the verdict, every round | RIG:81-84; LOG2:218 |
| Results table | see section 4 (raw lines) |
| "The *Without `ALTD`* column is the workaround"; first row's control = the two lines in *A proven workaround* | RIG:481-487 (K_BLK4 arm body; RIG:484-485 = the drop-in); LEDGER:933-934 |
| wrlong row: longs from the ALTD-selected registers | LOG2:181 (hub A slots 2-5 = `$C0C0_0002..5` = `wsrc[2..5]`, RIG:99-101, RIG:678-680) |
| single-long references +4, +4, +12 | LOG2:24, LOG2:37, LOG2:102 |
| every round same value | LOG2 rounds 0-3 of every arm (lines 24-217); LOG2:220-226 "in all 4 rounds" |
| trap untouched; write trap `$7E7E_0000` + k | every LOG2 round line reads `bbad=0`; LOG2:182 (B row `$7E7E_0000`..`$7E7E_000B`); RIG:180 |
| round 0 control `before=$0000_23C8 after=$0000_23D8 delta=16` | LOG2:50 |
| round 0 hazard `before=$0000_23C8 after=$0000_23CC delta=4` | LOG2:63 |
| `$A5A0_0004` to `$A5A0_0007` in slots 2-5, both | LOG2:51, LOG2:64 |
| run twice, 2026-09-24, two builds, measuring code unchanged | LEDGER:893-894; LOG1:1, LOG2:1 |
| first run start `$0000_23B8` | LOG1:63 (and every LOG1 read-arm round line) |
| second run start `$0000_23C8` | LOG2:63 |
| every change and data result matched | LEDGER:894; check below |
| values read from raw lines, not the verdict line | LEDGER:891-892 (and re-read for this chapter, section 4) |

Cross-run check (both files, same counts):

```
grep -c -E "delta=4 data=FULL landed=(1/1|4/4|8/8) abad=0 bbad=0"        LOG2: 28   LOG1: 28
grep -c -E "delta=(12|16|32) data=FULL landed=(1/1|4/4|8/8) abad=0 bbad=0" LOG2: 32   LOG1: 32
grep -c " round "                                                          LOG2: 60   LOG1: 60
```

28 = 7 arms x 4 rounds at +4 (K_SINGLE, K_ALTD1, H_BLK4, H_BLK8, H_PTRB, H_WR, H_Q2);
32 = 8 arms x 4 rounds at +12/+16/+32 (K_BLK4, K_BLK8, K_IDX1, K_IDX3, H_IDX3, K_PTRB, K_WR, K_Q2).
Per-arm values were also read line by line in both logs.

### The test program

| Chapter number | Source |
|---|---|
| filename | RIG:3 |
| 15 arms in sequence | RIG:464-588 |
| `prep_cog`, `c_rsrc` (hub address of source long 4), `c_before`/`c_after`, `dump_cog` | RIG:449-450, RIG:597-603, RIG:627-636 |
| `c_hidx` holds `dst + 2` | RIG:457 |
| other arms: `setq #8 - 1`, `ptra++[3]`, `ptrb++`, `wrlong` from `wsrc`/trap `wtrp`, `setq2` | RIG:501, 535, 552, 569, 584-586 |
| three hazard instructions at consecutive longs | RIG:153-155 (listing check recorded in the rig) |
| `FULL` = block complete and placed, both regions otherwise untouched | RIG:342-343 (`abad == 0 and bbad == 0`) |
| output order: raw block, control line, verdict per hazard arm, primary last | RIG:161-163; LOG2:218-226 |
| runs once, well under a second, RAM, DEBUG | RIG:158-160 |

### Status

| Field | Source |
|---|---|
| Published by Parallax: KNOWN BUGS | DOC:197-211 |
| Found by: Parallax | brief instruction; LEDGER:887-888 |
| 2026-09-24, P2 board, 200 MHz, run twice | LEDGER:892-894; LOG1:1; LOG2:1 |
| Workaround proven on silicon: Yes, 2026-09-24, rule at each use, adjacent `SETQ`/`SETQ2` | LEDGER:933-934, LEDGER:893; LOG2:50/53/56/59 and LOG1:50/53/56/59 (K_BLK4 in both runs); kind per creation-guide §5 |

## 4. Raw log lines used (verbatim, LOG2 unless marked)

```
LOG2:20  [2026-09-24T23:18:03.200] Cog0  === O17: SETQ + ALTD + block RDLONG PTRx delta  (pnut-ts v1.55.8, clk 200 MHz) ===
LOG2:21  [2026-09-24T23:18:03.200] Cog0  measuring cog 1 done. sentinel=$5E5E_5E5E  src long k=$A5A0_0000+k  ptr starts at src long 4
LOG2:24  [2026-09-24T23:18:03.202] Cog0    round 0 before=$0000_23C8 after=$0000_23CC delta=4 data=FULL landed=1/1 abad=0 bbad=0
LOG2:37  [2026-09-24T23:18:03.211] Cog0    round 0 before=$0000_23C8 after=$0000_23CC delta=4 data=FULL landed=1/1 abad=0 bbad=0
LOG2:50  [2026-09-24T23:18:03.220] Cog0    round 0 before=$0000_23C8 after=$0000_23D8 delta=16 data=FULL landed=4/4 abad=0 bbad=0
LOG2:51  [2026-09-24T23:18:03.221] Cog0      A: $5E5E_5E5E $5E5E_5E5E $A5A0_0004 $A5A0_0005 $A5A0_0006 $A5A0_0007 $5E5E_5E5E $5E5E_5E5E $5E5E_5E5E $5E5E_5E5E $5E5E_5E5E $5E5E_5E5E
LOG2:63  [2026-09-24T23:18:03.230] Cog0    round 0 before=$0000_23C8 after=$0000_23CC delta=4 data=FULL landed=4/4 abad=0 bbad=0
LOG2:64  [2026-09-24T23:18:03.231] Cog0      A: $5E5E_5E5E $5E5E_5E5E $A5A0_0004 $A5A0_0005 $A5A0_0006 $A5A0_0007 $5E5E_5E5E $5E5E_5E5E $5E5E_5E5E $5E5E_5E5E $5E5E_5E5E $5E5E_5E5E
LOG2:65  [2026-09-24T23:18:03.232] Cog0      B: $5E5E_5E5E $5E5E_5E5E $5E5E_5E5E $5E5E_5E5E $5E5E_5E5E $5E5E_5E5E $5E5E_5E5E $5E5E_5E5E $5E5E_5E5E $5E5E_5E5E $5E5E_5E5E $5E5E_5E5E
LOG2:76  [2026-09-24T23:18:03.240] Cog0    round 0 before=$0000_23C8 after=$0000_23E8 delta=32 data=FULL landed=8/8 abad=0 bbad=0
LOG2:89  [2026-09-24T23:18:03.250] Cog0    round 0 before=$0000_23C8 after=$0000_23CC delta=4 data=FULL landed=8/8 abad=0 bbad=0
LOG2:102 [2026-09-24T23:18:03.260] Cog0    round 0 before=$0000_23C8 after=$0000_23D4 delta=12 data=FULL landed=1/1 abad=0 bbad=0
LOG2:115 [2026-09-24T23:18:03.269] Cog0    round 0 before=$0000_23C8 after=$0000_23D8 delta=16 data=FULL landed=4/4 abad=0 bbad=0
LOG2:128 [2026-09-24T23:18:03.279] Cog0    round 0 before=$0000_23C8 after=$0000_23D4 delta=12 data=FULL landed=4/4 abad=0 bbad=0
LOG2:141 [2026-09-24T23:18:03.289] Cog0    round 0 before=$0000_23C8 after=$0000_23D8 delta=16 data=FULL landed=4/4 abad=0 bbad=0
LOG2:154 [2026-09-24T23:18:03.299] Cog0    round 0 before=$0000_23C8 after=$0000_23CC delta=4 data=FULL landed=4/4 abad=0 bbad=0
LOG2:167 [2026-09-24T23:18:03.309] Cog0    round 0 before=$0000_2480 after=$0000_2490 delta=16 data=FULL landed=4/4 abad=0 bbad=0
LOG2:180 [2026-09-24T23:18:03.319] Cog0    round 0 before=$0000_2480 after=$0000_2484 delta=4 data=FULL landed=4/4 abad=0 bbad=0
LOG2:181 [2026-09-24T23:18:03.320] Cog0      A: $5E5E_5E5E $5E5E_5E5E $C0C0_0002 $C0C0_0003 $C0C0_0004 $C0C0_0005 $5E5E_5E5E $5E5E_5E5E $5E5E_5E5E $5E5E_5E5E $5E5E_5E5E $5E5E_5E5E
LOG2:182 [2026-09-24T23:18:03.321] Cog0      B: $7E7E_0000 $7E7E_0001 $7E7E_0002 $7E7E_0003 $7E7E_0004 $7E7E_0005 $7E7E_0006 $7E7E_0007 $7E7E_0008 $7E7E_0009 $7E7E_000A $7E7E_000B
LOG2:193 [2026-09-24T23:18:03.329] Cog0    round 0 before=$0000_23C8 after=$0000_23D8 delta=16 data=FULL landed=4/4 abad=0 bbad=0
LOG2:206 [2026-09-24T23:18:03.339] Cog0    round 0 before=$0000_23C8 after=$0000_23CC delta=4 data=FULL landed=4/4 abad=0 bbad=0
LOG2:218 [2026-09-24T23:18:03.372] Cog0  RIG OK: every control read its expected delta and FULL data in all 4 rounds
LOG2:220 [2026-09-24T23:18:03.374] Cog0  ARM-VERDICT H_BLK8: CONFIRMED - pointer delta 4 (TRUE value) while all 8 longs landed at the ALTD destination, in all 4 rounds; control delta 32
LOG2:221 [2026-09-24T23:18:03.375] Cog0  ARM-VERDICT H_IDX3: CONFIRMED - pointer delta 12 (TRUE value) while all 4 longs landed at the ALTD destination, in all 4 rounds; control delta 16
LOG2:222 [2026-09-24T23:18:03.376] Cog0  ARM-VERDICT H_PTRB: CONFIRMED - pointer delta 4 (TRUE value) while all 4 longs landed at the ALTD destination, in all 4 rounds; control delta 16
LOG2:223 [2026-09-24T23:18:03.378] Cog0  ARM-VERDICT H_WR: CONFIRMED - pointer delta 4 (TRUE value) while all 4 longs landed at the ALTD destination, in all 4 rounds; control delta 16
LOG2:224 [2026-09-24T23:18:03.378] Cog0  ARM-VERDICT H_Q2: CONFIRMED - pointer delta 4 (TRUE value) while all 4 longs landed at the ALTD destination, in all 4 rounds; control delta 16
LOG2:225 [2026-09-24T23:18:03.379] Cog0  --- PRIMARY: H_BLK4  setq #3 / altd / rdlong 0-0, ptra++   TRUE delta +4, FALSE delta +16 ---
LOG2:226 [2026-09-24T23:18:03.380] Cog0  VERDICT: CONFIRMED - pointer delta 4 (TRUE value) while all 4 longs landed at the ALTD destination, in all 4 rounds; control delta 16
LOG1:63  [2026-09-24T20:47:18.270] Cog0    round 0 before=$0000_23B8 after=$0000_23BC delta=4 data=FULL landed=4/4 abad=0 bbad=0
LOG1:50  [2026-09-24T20:47:18.261] Cog0    round 0 before=$0000_23B8 after=$0000_23C8 delta=16 data=FULL landed=4/4 abad=0 bbad=0
LOG1:226 [2026-09-24T20:47:18.435] Cog0  VERDICT: CONFIRMED - pointer delta 4 (TRUE value) while all 4 longs landed at the ALTD destination, in all 4 rounds; control delta 16
```

Results-table row to raw line (control / hazard, round 0; rounds 1-3 identical, lines follow each):

| Row | Control | Hazard |
|---|---|---|
| `setq #3` + `rdlong ptra++` | LOG2:50 (16) | LOG2:63 (4, 4/4) |
| `setq #7` + `rdlong ptra++` | LOG2:76 (32) | LOG2:89 (4, 8/8) |
| `setq #3` + `rdlong ptra++[3]` | LOG2:115 (16) | LOG2:128 (12, 4/4) |
| `setq #3` + `rdlong ptrb++` | LOG2:141 (16) | LOG2:154 (4, 4/4) |
| `setq #3` + `wrlong ptra++` | LOG2:167 (16) | LOG2:180 (4, 4/4) |
| `setq2 #3` + `rdlong` LUT `ptra++` | LOG2:193 (16) | LOG2:206 (4, 4/4) |

## 5. Code excerpts (verbatim from RIG; printed lines now mirror ARCHIVE)

**Printed code now mirrors the conformed archive copy (2026-09-26, «#360»); the measuring PASM
is byte-identical to the as-run rig.** ARCHIVE = `examples-library/e1-setq-block-pointer-step-test.spin2`
(conformed 2026-09-26, task #360: renamed `dst`/`trp`+2 to `block_first`/`trap_first`, named
`BLOCK_LONGS`/`WIDE_BLOCK_LONGS`; PASM measuring image byte-identical to RIG's).

| Chapter lines (v0.2.0, post-#360) | Fence | RIG lines (as-run, history) | ARCHIVE lines (printed) | Max width |
|---|---|---|---|---|
| 53-58 (*A proven workaround*, drop-in block; post-#360 lines) | `pasm2` | RIG:484-485 | ARCHIVE:577-582 | 72 |
| 109-121 (control, K_BLK4 body) | `pasm2` | RIG:481-487 (RIG:480, the arm comment, omitted: it names a study-brief workaround label) | ARCHIVE:573-585 | 72 |
| 127-135 (hazard, H_BLK4 incl. arm comment) | `pasm2` | RIG:488-496 | ARCHIVE:586-594 | 66 |
| 143-144 (`delta` body, signature omitted: doc-commented in ARCHIVE, not contiguous with the body) | `spin2` | RIG:353-355 | ARCHIVE:375-376 | 60 |

Byte-identity (v0.2.0, pre-#360 rename): `grep -n -x -F -f <chapter> <RIG>` listed RIG:353-355,
481-487 and 488-496 in full. Post-#360, the chapter's fences equal the renamed ARCHIVE spans
above (verified by `engineering/tools/verify-example-corpus-identity.py`, GREEN); RIG is kept
as the as-run record and is no longer byte-identical to the printed fences (names differ; the
measuring PASM itself is unchanged). RIG has no tab characters (`grep -c -P "\t"` = 0, v0.1.0 check).

## 6. The drop-in block (*A proven workaround*): from the rig that ran (as-run) and the archive (printed)

The block printed first in *A proven workaround* is six lines (`CON`/`DAT` plus the two-instruction body),
byte-identical to ARCHIVE:577-582, between the `' ---- DROP-IN BEGIN/END ----` markers in
`examples-library/e1-setq-block-pointer-step-test.spin2` (markers excluded). Before the #360
conformance rename it was two lines, byte-identical to RIG:484-485, the body of arm 2, K_BLK4
(`setq #4 - 1` directly before `rdlong dst + 2, ptra++`); the archive spelling is
`setq #BLOCK_LONGS - 1` / `rdlong block_first, ptra++`, the same instructions with named
operands:

```
CON ' ---- E1 Workaround: Block Length ----
  BLOCK_LONGS   = 4                     ' longs in your block

DAT ' ---- E1 Workaround: Block Transfer ----
                setq    #BLOCK_LONGS - 1        ' directly before RDLONG
                rdlong  block_first, ptra++     ' block's first register
```

- **Contiguity and width:** ARCHIVE:577-582 are consecutive; widest line 72 columns (K = 76).
  RIG:484 and RIG:485 (the as-run rig, unrenamed) are likewise consecutive at 30 and 39 columns.
- **The run that proved it:** K_BLK4 is a control arm: the program refuses a verdict unless it
  reads its required delta and FULL data in every round (RIG:81-84, RIG:245-247).
  Run 2 (LOG2, the build on disk): LOG2:50, 53, 56, 59, `delta=16 data=FULL landed=4/4 abad=0 bbad=0`
  in all four rounds; LOG2:218 `RIG OK`. Run 1 (LOG1, first build, same measuring code):
  LOG1:50, 53, 56, 59 `delta=16 data=FULL landed=4/4 abad=0 bbad=0` (start `$0000_23B8`), and the cross-run count of full-step control
  lines is 32 in both logs (§3). Both runs 2026-09-24, P2 board, 200 MHz (LEDGER:892-894).
- **Kind:** rule at each use (the `SETQ`/`SETQ2` must be adjacent at every block transfer).
- **Arm comment RIG:480** (`workaround (a)`, a study-brief label) is not part of the block.

## 6a. v0.1.0 compile harness (history; not printed in v0.2.0)

HARN is kept unchanged. Its snippets 1 and 2 were compiled for v0.1.0; neither appears in the
v0.2.0 chapter, whose only workaround code is the rig block above. The v0.1.0 record follows.

| v0.1.0 chapter lines | HARN lines |
|---|---|
| 43-44 (snippet 1, adjacent `SETQ`) | 28-29 |
| 52-55 (snippet 2, plain `PTRA` + explicit `ADD`) | 32-35 |

Compile (v0.1.0; a scratch copy, `cmp`-identical to HARN, compiled in the session scratchpad; no output in M/):

```
/usr/local/bin/pnut-ts -l e1-harness-workaround.spin2
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: Wrote .../e1-harness-workaround.lst
pnut-ts: Wrote .../e1-harness-workaround.bin (6352 bytes)
pnut-ts: Done
```

Encodings read from the listing hub image (DAT at $00008):

| Word | Instruction | Check |
|---|---|---|
| `$F6041009` | `mov idx, #buf` | D=$008, #S=$009 |
| `$FD640628` | `setq #NLONGS - 1` | SETQ, D=3 (matches RIG's `$FD640628`) |
| `$FB041361` | `rdlong buf, ptra++` | RDLONG, D=$009, S=$161 = PTRA++ |
| `$FD640628` | `setq #NLONGS - 1` | as above |
| `$F98C1000` | `altd idx` | ALTD, I=1, D=$008, S=#0 (same form as RIG's `altd c_hidx` `$F98DF600`) |
| `$FB040100` | `rdlong 0-0, ptra` | RDLONG, D=0, S=$100 = plain PTRA (DOC:6953-6955) |
| `$F107F010` | `add ptra, #NLONGS * 4` | ADD, D=$1F8 (PTRA), #S=16 |
| `$FD9FFFFC` | `jmp #$` | |

## 7. Why it happens (paraphrase control)

Written from the mechanism in `code-validation/test-briefs/BRIEF-O17.md` Part 2, in programmer's-model
terms only: a held record of the preceding `SETQ`/`SETQ2` that survives `ALTx`/`AUGS`/`AUGD` and
feeds the transfer count; a pointer-step selection that checks only the immediately preceding
instruction. No HDL text, signal or module name, or line reference is carried into the chapter.
The `AUGS`/`AUGD` sentence is marked as untested in the chapter.
