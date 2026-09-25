# E1 verification sidecar: Chapter 1, SETQ Block Transfers Lose Their Pointer Step

Chapter: `opus-master/e1-setq-block-pointer-step.md`. Every number, quotation and code excerpt in
the chapter, mapped to its source. Internal document: ids are allowed here, never in the chapter.

Path keys:

| Key | Path |
|---|---|
| LEDGER | `engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md` (EF-067 at 916-938; campaign header 884-896) |
| DOC | `engineering/ingestion/sources/silicon-doc/p2-documentation.txt` (Parallax P2 Documentation v35) |
| RIG | `engineering/document-production/manuals/p2-errata/audit/verification-tests/test-o17-setq-altd-block-ptr-delta.spin2` |
| LOG2 | `.../audit/verification-tests/logs/debug_260924-231802.log` (second run, style-conformed build) |
| LOG1 | `.../audit/verification-tests/logs-orig/debug_260924-204717.log` (first run, as-authored build) |
| HARN | `.../audit/verification/e1-harness-workaround.spin2` |
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

## 2. Quotations of Parallax documentation

| Chapter | Quoted / cited text | Source |
|---|---|---|
| Design, blockquote 1 | "For fast block moves, PTRx expressions cannot have arbitrary index values, since the index will be overridden with the number of longs, with bit 4 of the encoded index value serving as the ++/-- indicator." | DOC:7220-7221 (sentence ends on 7221 at "indicator.") |
| Design, para after quote 1 | `SETQ #x` + `RDLONG first_reg,PTRA++`, "read x+1 longs from PTRA, PTRA += (x+1)*4" | DOC:7232-7239 (instruction and operand columns split by extraction: 7232-7233 mnemonics, 7235-7236 operands, 7238-7239 comments) |
| Design, `PTRx += INDEX*SCALE` | "U = 0 to keep PTRx same, 1 to update PTRx (PTRx += INDEX*SCALE)" | DOC:6946 |
| Design, `SCALE` is 4 | "SCALE = 1 for RDBYTE/WRBYTE, 2 for RDWORD/WRWORD, 4 for RDLONG/WRLONG/WMLONG" | DOC:6944 |
| Design, blockquote 2 | "Intervening ALTx/AUGS/AUGD instructions between SETQ/SETQ2 and RDLONG/WRLONG/WMLONG-PTRx instructions will cancel the special-case block-size PTRx deltas. The expected number of longs will transfer, but PTRx will only be modified according to normal PTRx expression behavior:" | DOC:198-200, section heading KNOWN BUGS at DOC:197 |
| Design, example | `SETQ #16-1` ('ready to load 16 longs), `ALTD start_reg`, `RDLONG 0,ptra++`; comment "ptra will only be incremented by 4 (1 long), not 16*4 as anticipated!!!" | DOC:201-210 (extraction splits columns: mnemonics 201/203/205, operands 202/204, comments 206-210; the third comment spans 210 + 206). The chapter paraphrases the example; it does not reproduce it as a quotation. |
| Workaround, plain `PTRA` not updated | "100000000 PTRA 'use PTRA" and "U = 0 to keep PTRx same" | DOC:6953-6955, DOC:6946 |

## 3. Numbers

### Opening, What the part does, The symptom

| Chapter number | Source |
|---|---|
| `setq #3` + `altd` + `rdlong 0-0, ptra++` advances 4, not 16 | LOG2:63 (hazard +4), LOG2:50 (control +16); RIG:492-494 |
| +4 for `ptra++` | LOG2:63 |
| +4 for `ptrb++` | LOG2:154 |
| +12 for `ptra++[3]` | LOG2:128 |
| 8-long block moved `PTRA` by +4 | LOG2:89 |
| `ALTD` alone + single `RDLONG ptra++` = +4 | LOG2:37 (K_ALTD1) vs LOG2:24 (K_SINGLE) |
| "4 bytes past the start of the block instead of 16" | LOG2:63 vs LOG2:50 |
| Plain `ptra++` = 4, `ptra++[3]` = 12 (design para) | DOC:6944/6946 (INDEX*SCALE); measured LOG2:24 and LOG2:102 |
| Scope: only `ALTD` tested; `AUGS`/`AUGD`/other `ALTx` vendor-named | LEDGER:934-935; RIG:42-58 (arm table: every hazard arm is `altd`) |
| Untested: `WMLONG`, `SETQ2`+`WRLONG`, `ptra--`, `++ptra`, `--ptra` | RIG:42-58 (arm table lists only rdlong/wrlong post-increment forms, and setq2 only with rdlong) |

### The workaround

| Chapter number | Source |
|---|---|
| `PTRA` +16 for 4 longs | LOG2:50 (K_BLK4) |
| `PTRA` +32 for 8 longs | LOG2:76 (K_BLK8) |
| `PTRB` +16 | LOG2:141 (K_PTRB) |
| `SETQ2` into lookup RAM +16 | LOG2:193 (K_Q2) |
| `WRLONG` +16 | LOG2:167 (K_WR) |
| `ptra++[3]` block +16 | LOG2:115 (K_IDX3) |
| Workaround proven = SETQ adjacent (the control column) | LEDGER:933-934 |
| 9-bit `#` literal on `ADD` | KB add.yaml:10-11 ("Src is a register, 9-bit literal, or 32-bit augmented literal") |
| 128 longs or more needs `##` | arithmetic: 127 x 4 = 508 fits 0-511; 128 x 4 = 512 does not |
| Explicit-step form not tested on silicon | RIG:42-58 (no arm uses a plain `ptra` with `altd`) |

### How it was proven

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
| Workaround proven: adjacent `SETQ` | LEDGER:933-934 |

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

## 5. Code excerpts (verbatim from RIG)

| Chapter lines | Fence | Source lines | Max width |
|---|---|---|---|
| 102-108 (control, K_BLK4 body) | `pasm2` | RIG:481-487 (RIG:480, the arm comment, omitted: it names a study-brief workaround label) | 39 |
| 114-122 (hazard, H_BLK4 incl. arm comment) | `pasm2` | RIG:488-496 | 66 |
| 130-132 (`PRI delta`) | `spin2` | RIG:353-355 | 43 |

Byte-identity checked with an awk line-by-line compare of chapter vs RIG: 19 lines compared, 0 differences.
RIG has no tab characters (`grep -c -P "\t"` = 0).

## 6. Workaround snippets (compiled in HARN)

| Chapter lines | HARN lines |
|---|---|
| 43-44 (snippet 1, adjacent `SETQ`) | 28-29 |
| 52-55 (snippet 2, plain `PTRA` + explicit `ADD`) | 32-35 |

Byte-identity: awk compare, 6 lines, 0 differences. All fenced code lines in the chapter are
at most 76 columns (awk check: 25 code lines, none over 76).

Compile (a scratch copy, `cmp`-identical to HARN, compiled in the session scratchpad; no output in M/):

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
