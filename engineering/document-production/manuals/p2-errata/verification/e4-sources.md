# E4 sources: Erratum E4, GETXACC Clears Only During a Goertzel Burst

Verification sidecar for `opus-master/e4-getxacc-clear-gating.md` (v0.2.0 shape, task «#359»).
Every number, quotation and code excerpt in the chapter maps to a file and line below. Internal
document: ids and paths are allowed here, never in the chapter.

## Abbreviations

| Tag | File |
|---|---|
| **DOC** | `engineering/ingestion/sources/silicon-doc/p2-documentation.txt` (the 2025 capture the v0.1.0 chapter was verified against) |
| **SDT** | `engineering/ingestion/sources/silicon-doc/silicon-doc-text.txt` (the current DOCX capture of the same P2 Documentation v35; see `SUPERSEDED-BY-2026-08-26-DOCX.md`) |
| **LED** | `engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md` (campaign header 884–896, EF-069 at 958–976, EF-070 at 978–990; second session header 994–1005, EF-072 at 1027–1054) |
| **RIG** | `engineering/document-production/manuals/p2-errata/audit/verification-tests/test-so80-getxacc-clear-gating.spin2` (reader name `e4-getxacc-clear-gating-test.spin2`) |
| **L2** | `.../audit/verification-tests/logs/debug_260924-231817.log` (run 2, style-conformed build, `.bin` 15616 bytes, L2:14) |
| **L1** | `.../audit/verification-tests/logs-orig/debug_260924-204741.log` (run 1, as-authored build, `.bin` 15581 bytes, L1:14) |
| **FIX** | `engineering/document-production/manuals/p2-errata/audit/verification-tests/e4-e5-fix-read-sums-test.spin2` (the as-run name; the reader's copy is `e4-e5-workaround-read-sums-test.spin2` since #360; 871 lines, header "Updated.... 26 Sep 2026"; ran once on silicon 2026-09-26, log FL below; not yet replicated to the campaign `tests/` folder at this writing) |
| **FL** | `.../audit/verification-tests/logs/debug_260926-015810.log` (the workaround run; see "The workaround run (FL)") |
| **S2R** | `.../audit/verification-tests/test-goertzel-sinc2-iteration-count.spin2` (reader name `e5-goertzel-sinc2-iteration-count-test.spin2`) |
| **S2L1** | `.../audit/verification-tests/logs/debug_260925-214001.log` (SINC2 test, run 1) |
| **HAR** | `engineering/document-production/manuals/p2-errata/verification/e4-harness-difference.spin2` (v0.1.0 workaround harness; superseded, see below) |
| **BRF** | `engineering/document-production/manuals/p2-errata/code-validation/test-briefs/BRIEF-SO80.md` (mechanism only; not quoted) |

L1 and L2 carry the measurement lines at the **same line numbers** (23–102). Every `Cog0` line
of the two logs is identical except the `INIT ... jump` address (different builds) and the
final `DEBUG_END_SESSION` line, present only in L2. Command used to check this (v0.1.0):
`diff <(grep -o "Cog0 .*" L2) <(grep -o "Cog0 .*" L1)` with the full paths above; output was
exactly those two differences.

**Workaround wording (2026-09-26, task #360; Stephen's decision, voice-guide §2).** The reader's
change is a *workaround*, never a *fix* (a fix is a silicon revision). Section *The fix*
(`{#sec-e4-fix}`) is now *A proven workaround* (`{#sec-e4-workaround}`), rule-first: *What any
workaround must do* (the condition, as in the front matter's summary table), *One way, proven
on a real P2* and the block, then *Other ways that meet the condition*; the subsection *The
fix's test* is now *The workaround's test* (`{#sec-e4-workaround-proof}`). The CAUTION box's
third line is *Workaround* (the condition); the status row is *Workaround proven on silicon*.
The archive copy of FIX is renamed `e4-e5-workaround-read-sums-test.spin2` (ARCHIVE-WKR below);
its identifiers `FIX_N0..9`/`FIX_CALLS`/`R_FIX`/`F_*`/`fixval`/`score_fix`/`fix_arm`/`fidx_`/
`fixn_` are renamed `WKR_N0..9`/`WKR_CALLS`/`R_WKR`/`W_*`/`wkrval`/`score_wkr`/`wkr_arm`/`widx_`/
`wkrn_`, and comments and `debug()` text say *workaround*: no line added or removed, so every
ARCHIVE-WKR line number below still holds, and the object image is byte-identical to the
pre-#360 archive (pnut-ts 1.55.8, `-d` and without; the `-d` binary differs only in its DEBUG
data). FIX and FL are the as-run record and keep their own wording.

## The drop-in block (*A proven workaround*)

**Printed code now mirrors the conformed archive copy (2026-09-26, «#360»); the measuring PASM
is byte-identical to the as-run rig.** ARCHIVE-WKR = `examples-library/e4-e5-workaround-read-sums-test.spin2`
(renamed from `e4-e5-fix-read-sums-test.spin2` later in #360, lines unchanged; conformed 2026-09-26, task #360: the block's `'` line comments became a `{ }` block comment, and
a new `CON` part names `ZERO_COUNT` (4) and `INPUT_NIB` (3) in place of the literals `#4`/`#3`;
same instructions, same PASM measuring image, byte-identical to FIX's).

| Item | Source |
|---|---|
| The 35-line `pasm2` block under *One way, proven on a real P2* in *A proven workaround* (30 lines pre-#360) | ARCHIVE-WKR:683–717 (post-#360), byte-identical: the lines strictly between the markers `' ---- DROP-IN BEGIN ----` (ARCHIVE-WKR:682) and `' ---- DROP-IN END ----` (ARCHIVE-WKR:718). Pre-#360: FIX:808–837, between FIX:807/FIX:838. The same block is printed in Erratum E5's *A proven workaround* |
| Widths | ARCHIVE-WKR:683–717: widest lines 73 columns (`burst_sums`/`sub` operand lines), all ≤ 76 (`awk` width pass); pre-#360, FIX:808–837 ran 15–69 columns; no tab and no non-ASCII byte in either file (`grep -n -P "[^\x20-\x7E]"` returns nothing) |
| Byte-identity check | post-#360: the chapter's *A proven workaround* fence (chapter 61–95) equals ARCHIVE-WKR:683–717 (verified by `engineering/tools/verify-example-corpus-identity.py`, GREEN). Pre-#360 check (history): `awk 'NR==FNR { if (FNR>=808 && FNR<=837) r[++n]=$0; next } /^## The fix/ { f=1 } f && /^```pasm2/ { inb=1; next } inb && /^```/ { exit } inb { m++; if ($0 != r[m]) print "DIFF " m ": " $0 } END { print "compared " m " chapter lines with " n " rig lines" }' FIX <chapter>` → `compared 30 chapter lines with 30 rig lines`, no `DIFF` line |
| Kind: helper routine | creation-guide §4.6; FIX:4–6 ("drop-in fix burst_sums: one routine that runs a DDS/Goertzel burst and returns its exact cosine and sine sums") |
| **The run that proved it** | FL, 2026-09-26, run once, 200 MHz: 60 of 60 calls S = N × C on cosine and sine, re-derived from the raw lines (§"The workaround run (FL)"); FL ran the FIX build (pre-#360 names), and the #360 renames left the measuring PASM byte-identical, so the verdict still applies to ARCHIVE-WKR |

### What the chapter says about the block, and where it comes from

| Chapter text | Source |
|---|---|
| *What any workaround must do*: each burst's sums as the difference of two idle readings, before and after; an idle `GETXACC` clears nothing | the erratum itself (L2:78–79; idle reads equal B, §Proof); front matter summary table |
| *One way*: `burst_sums`, which also steps around E5 | the block (above); E5's zero bursts: FIX:38–40 |
| guarantee: sums of your burst alone, all N terms, whatever the accumulators held before | FIX:24–28 and FIX:127–128 (the pre-registered CONFIRMED outcome), met in FL (re-derived: §"The workaround run (FL)") |
| *Other ways*: any code that takes the two idle readings and subtracts meets E4's condition; run A did so: 15,555 for a 256-clock burst in all eight repetitions, from five different starting values | L2:81–88 (`dA=15_555` on every line); starting values L2:27, 32, 52, 57, 62 (976, 14,823, 12,871, 10,919, 8,967; five distinct) |
| *Other ways*: that difference is 255 terms, not 256, because of E5; the held term only a later Goertzel burst delivers; the zero bursts add it | L2:81 (`kA=255`); LED:979–983 (EF-070: N − 1 terms; the held term arrives with the next burst); FL:42 vs L2:81 (15,616 with the routine, 15,555 without) |
| put your `XINIT` D in `burst_mode`, S in `burst_sel`, `CALL #burst_sums` with the streamer idle | FIX:809–810 (the block's own comment); FIX:34 ("with the streamer idle at entry") |
| example values: SINC1, no DAC, pins P0–P3, count 256, P3 inverted and summed, LUT offset `$0A5` | FIX:830–831 (`$F007_0100`, `$0008_80A5`); decode FIX:64–66 ("[11:8]=0 (no DAC), [7]=0 (SINC1), [6:3]=0 (pins P0..P3)"; "S[19]=1 (invert), S[15]=1 (sum P3 only), LUT $0A5"); count `$0100` = 256; DOC:4035–4044 (summation table) |
| two idle readings; `GETXACC` clears nothing idle | FIX:39–41; the erratum itself (this chapter, L2:78–79) |
| zero bursts: your mode word, count 4, S[15:12] clear, every term zero | FIX:812–815 (`mov`/`setword #4, #0`/`mov`/`setnib #0, #3`); FIX:35, FIX:67–68; SETNIB nibble 3 = bits 15:12; S[15:12] are the four pin-summation enables (DOC:4002–4006) |
| first zero burst delivers any held term; second delivers the burst's last | FIX:38–40; the E5 mechanism (LED:978–983) |
| two zero bursts of 4 NCO rollovers each, at your `SETXFRQ` rate | FIX:813 (count 4); D[15:0] counts NCO rollovers (DOC:3500–3501) |
| cog waits in `WAITXFI` until each command has finished | FIX:817, 821, 823; `WAITXFI` = "Wait for the streamer-finished event flag" (SDT:2097), flag "Set whenever the streamer runs out of commands" (SDT:2182) |
| 17 instructions, 8 longs | counted: FIX:812–828 (17 instruction lines), FIX:830–837 (8 `long` lines) |
| SINC1 only; in SINC2 the zero burst is not tested as a flush and the routine is not recommended; E5's *A proven workaround* notes the separate, documented SINC2 constraint | FIX:5–6, FIX:28–29 ("SINC1 only: EF-072's scope note (untested) is that in SINC2 the zero burst does not flush the first stage ... nothing here runs SINC2"); LED:1051–1052 (scope note, study reading, untested). The SINC2 constraint is the P2 Documentation's note (SDT:1704–1705); arbiter ruling 2026-09-26: documented behaviour, not an erratum, not part of E5 (see `e5-sources.md` head) |
| `XINIT` issues at once; does not fit an `XCONT` stream | DOC:2742 / SDT:1282 ("Issue command immediately, zeroing phase"); SDT:1284 (XCONT waits for the final NCO rollover) |
| test conditions: cog RAM, NCO `$8000_0000`, one input pin, no DAC output, bursts 1 to 1001 | FIX:47–54 (P3 only; no DAC), FIX:63 (`SETXFRQ $8000_0000`), FIX:189–198 (N list), FIX:647 (`DAT org 0`, cog exec); "ran ... once" and 200 MHz: FL:1, FL:13 |
| DAC channels output on every clock of a DDS/Goertzel command | DOC:3985 / SDT:1555 ("outputs and inputs on every clock in which the command is active") |
| not tested: DAC enabled, more than one pin, other NCO frequencies, hub execution, values near the 32-bit limit | scope of FIX (FIX:53, 47–48, 63, 647); DOC:4095 ("32-bit accumulators") |

### Superseded v0.1.0 workaround snippet

The v0.1.0 chapter printed a 10-line before-and-after snippet compiled in HAR (see the v0.1.0
record below). At v0.2.0 it is no longer printed: the printed workaround is the FIX drop-in block,
which runs on a part (task «#359» decision 4). HAR is left in place, unchanged, as the record
of what v0.1.0 printed. The measurement behind the old snippet (run A, before-and-after
difference) remains in the chapter's proof as evidence.

v0.1.0 record, kept for audit: the snippet was byte-identical to HAR's `SNIPPET BEGIN`/`SNIPPET
END` block (widths 23–72) and compiled with `/usr/local/bin/pnut-ts -l <scratchpad>/e4-harness-difference.spin2`
→ `Version 1.55.8`, `Wrote ... (6344 bytes)`, `Done`.

## Quotations (Parallax P2 Documentation)

| Chapter text | Source |
|---|---|
| "Get Goertzel X into D and Y into next S, clear X and Y" | DOC:2745 (STREAMER section, heading DOC:2723; the table's instruction column lists `GETXACC` at DOC:2731, operand `D` at DOC:2737); SDT:1285 |
| "After some number of complete NCO cycles, ... until a new streamer command executes." | DOC:4096–4099, copied exactly, line breaks joined with single spaces; SDT:1604 (one line, trailing space). Section heading "DDS/Goertzel" at DOC:3984 / SDT:1553 |
| "Accumulations (SIN_ACC/COS_ACC are read and cleared by GETXACC)" | DOC:4105; SDT:1608 |
| "None of the three places makes the clear depend on the streamer's mode ..." | `grep -n -i "GETXACC\|goertzel" DOC` returns GETXACC at 2532, 2731, 2745, 4097, 4105, 4230, 5674, 11401 only. 2532 (Q register), 4230 (demo code), 5674 (interrupt-shielding list), 11401 (opcode map) state no condition either |
| CAUTION "(P2 Documentation, *STREAMER* and *DDS/Goertzel*)" | DOC:2723 (STREAMER), DOC:3984 (DDS/Goertzel) |
| "Parallax does not list it" (opening) / Status "Published by Parallax: No" | DOC:197–227 KNOWN BUGS lists only the SETQ/ALTx and AUGS/ALTx bugs; LED:958 "(new; contradicts `getxacc.yaml`)" |

## Terms and mode names

| Chapter text | Source |
|---|---|
| "the immediate-to-pins mode, one pin wide, with its output disabled" | `$4000_0400`: RIG:177 comment "1-pin immediate, D[23]=0, no DAC, count $400"; RIG:133 "Non-Goertzel (D[31:16] = $4000): [15:12]=0100 ... [7]=0 (%e off)"; mode %0100 is "Immediate ⇢ Pins/DACs" at DOC:2964–2965 |
| SINC1 | D[23] = 0 in `$F007_xxxx`; DOC:4100–4116 (D[23] %0 = SINC1); RIG:131–132 |
| "P3 inverted and summed, the other three pins ignored" | `S` = `$0008_80A5`: S[19:16] = %1000, S[15:12] = %1000; DOC:4035–4044 (%1xxx_1xxx = base pin +3 inverted and summed; `%xxxx_0xxx` rows ignore pins +0..+2); RIG:55, RIG:134 |
| "input pins P0 to P3" | RIG:52–53, RIG:132 ([6:3]=0000, group 0, pins 0..3) |
| "a term is the product the streamer adds to each accumulator on each of those clocks" | DOC:4094–4095 ("multiplied by the bitstream sum ... then added into their respective 32-bit accumulators") |
| "32-bit limit" | DOC:4095 ("32-bit accumulators") |

## The continuous-stream paragraph (*What the P2 actually does*), new at v0.2.0

| Chapter text | Source |
|---|---|
| SINC1 streams of `e5-goertzel-sinc2-iteration-count-test.spin2` ("a check of the P2 Documentation's SINC2 constraint, run on 2026-09-25"; date LED:1001–1002, S2L1:1), chained with `XCONT`, one `GETXACC` per command | S2R:101–112 (arm table: P2-S1, NPS-S1, NPL-S1, CHP-S1 are SINC1 `XCONT`; JIT-S1 SINC1 `XCONT` + `WAITX #1 WC`; every XZERO arm is SINC2); S2R:1517–1525 (`loop_xc`: one `xcont`, one `getxacc` per pass) |
| every reading analysed (all but the first three) equalled the per-clock term times the clocks since the previous reading | S2L1:71 `P2-S1 ... SINC1: 1_021 samples; x <> C*(L-g) in 0`; S2L1:118 (NPS-S1, 0), S2L1:240 (NPL-S1, 0), S2L1:353 (CHP-S1, `2_045 samples ... in 0`), S2L1:440 (JIT-S1, 0); g = 0 at S2L1:57; L = read-to-read window measured by `GETCT` (S2R:58–63); first three samples excluded, S2R:70 and S2R:374 (`WARM = 3`). Ledger summary LED:1039–1040 ("SINC1: every sample = C × (clocks in its window)") |
| "The clear during a running command also held" | a reading equal to the window's terms only (not a running total) requires the clear to act at each mid-stream read; S2R:123–125 (the model's EF-069 premise) |

## Numbers

| Chapter number | Where it appears | Source |
|---|---|---|
| 100 clocks (G2L read) | Actual; Proof | RIG:180 `G2L_WAIT = 100`, RIG:542 `waitx #G2L_WAIT` |
| 256-clock burst | Sees, Proof | RIG:174 `N_RUN = 256`; RIG:689 `drun_`; RIG:128 `drun_ = $F007_0100` |
| 14,823 → 30,378, contributed 15,555 | Sees | L2:32 `rep 1 runA B=14_823 P=14_823 RA=30_378`; L2:82 `rep 1: ... dA=15_555` |
| 29 terms, started from 17,080, returned 18,849 | Sees | L2:28 `rep 0 runB B=17_080 P=17_080 R1=18_849 R2=13_786 waitx=30`; L2:81 `k1=29` |
| 15,555 in all eight repetitions | Proof | L2:81–88, `dA=15_555` on every line |
| starting values 976, 14,823, 12,871, 10,919, 8,967 | Proof (run A paragraph) | run A `P=` at L2:27 (976), L2:32/37/42/47 (14_823), L2:52 (12_871), L2:57 (10_919), L2:62 (8_967) |
| `$F007_0100`, `$0008_80A5` | A proven workaround (printed values) | FIX:830–831; the same values as RIG:128–129 ("drun_ = $F007_0100", "son_ = $0008_80A5") |
| 4,000-clock wait | Proof | RIG:179 `WAIT_IDLE = 4000`; RIG:125; RIG:86 |
| NCO frequency `$8000_0000` | A proven workaround (limits), Proof | FIX:63, FIX:178, FIX:651; RIG:178 `FRQ = $8000_0000`, RIG:478 `setxfrq frq_`, RIG:130 |
| 36,600 (largest value read) | Proof (run A paragraph) | L2:63 `rep 7 runB ... R1=36_600`; the largest value on any raw line L2:23–64 (sine values are smaller) |
| 200 MHz | Proof, Status | RIG:161; L2:21 `clk 200 MHz`; LED:892 |
| nothing connected to P0 to P7 | Proof | RIG:34 "NO JUMPER, nothing connected to P0..P7"; L2:21 "NO jumper" |
| debugger confined to cog 0 | Proof | RIG:162 `DEBUG_COGS = %0000_0001`; RIG:45–47 |
| P3 driven low, smart pin off | Proof | RIG:35–37, RIG:475–476 |
| 512 LUT longs, `$173D_0000` | Proof | RIG:58, RIG:129 (`lutv_ = $173D_0000`), RIG:480–487 (fill + readback); FIX:69–70 (same in the workaround program) |
| 61 (cosine), 23 (sine) per active clock | Proof | RIG:59–63, RIG:165–166; confirmed by CAL L2:66–67 and Y CAL L2:93 (1_449 = 63 × 23) |
| 8-clock, 4-clock preamble bursts; zero-term `S` `$0008_00A5` | Proof | RIG:84–85, RIG:171–172, RIG:129 (`szero_ = $0008_00A5`), RIG:636–650 |
| +3,843 / -3,843, 63 × 61 | Proof | L2:66 `CAL: dLO=3_843 dHI=-3_843`; L2:67 `CAL: kLO=63 kHI=-63` |
| 64-clock calibration bursts | Proof | RIG:173 `N_CAL = 64`; RIG:688 |
| controls all passed | Proof | L2:68 `controls: all passed (LUT, XFI, P3 level, B<>0, CAL sign+negation, dA)`; same at L1:68 |
| `$4000_0400`, count `$0400` | Proof | RIG:177, RIG:128 (`dimm_ = $4000_0400`) |
| eight repetitions | Proof | RIG:181 `REPS = 8`; L2:21 `reps 8` |
| 50 reads, all equal to B, none zero | Proof | L2:78 `Half A: 50 reads; moved 0 (non-Goertzel-active 0); read exactly 0 0`; L2:79 verdict line. Composition from RIG:344–352: 2 calibration P reads + 8 reps × (G1, G2, G2L, G3, run A P, run B P) = 50 |
| 488 (B and four reads, first repetition) | Proof | L2:25 `rep 0 (i)  B=488 G1=488 G2=488 G2L=488 G3=488` |
| delays 30 ×4, then 62, 94, 126, 190 | Proof | RIG:696 `dlytab`; L2:81–88 `waitx=` values |
| Table: 16,531 - 976 = 15,555 = 255 terms | Proof | L2:27 `rep 0 runA B=976 P=976 RA=16_531`; L2:81 `kA=255 ... dA=15_555` |
| Table: 18,849 - 17,080 = 1,769 = 29 terms | Proof | L2:28; L2:81 `k1=29`. 1,769 = 29 × 61 also stated at LED:969 |
| Table: R2 = 13,786 = 226 terms | Proof | L2:28 `R2=13_786`. 226 = 13,786 / 61 is arithmetic (226 × 61 = 13,786), stated at LED:970 |
| Table: R1 + R2 - P = 15,555 | Proof | L2:81 `dB=15_555 dd=0` |
| read point term 29 to term 189, one behind `WAITX` | Proof | L2:81 `k1=29 k1-waitx=-1`, L2:88 `waitx=190 ... k1=189 k1-waitx=-1`; all eight lines L2:81–88 show `k1-waitx=-1`; LED:971 |
| dd = 0 in all 8 | Proof | L2:81–88 `dd=0 class=0`; L2:89 `classes: 0 conf=8 ...`; L2:91 verdict |
| R2 = 13,786 in first four repetitions; run B started at 17,080 then 30,927 | Proof | L2:28, 33, 38, 43 (`R2=13_786`; `P=17_080`, then `P=30_927` ×3) |
| sine: moved on no idle read; 5,865 both runs every repetition | Proof | L2:94–101 `Y rep n: dA=5_865 dB=5_865 dd=0`; L2:102 `Y Half-A-style checks that moved: 0` |
| run twice, 2026-09-24, two builds, identical values | Proof, Status | LED:892–894; log timestamps L1:1 (20:47), L2:1 (23:18); the diff above |
| outcomes written into the program before the run (dd = R1, -C, +C) | Proof | RIG:25–31 (written before the run), RIG:405–416 (classes) |
| `POLLXFI` finished / still running | Proof | RIG:663–674 (`xfi_end`, `xfi_mid`); L2:68 |
| 255 terms, not 256 = Erratum E5 | Sees, Proof | LED:979–980 (EF-070: "A reading taken after a burst of N clocks holds N − 1 terms") |

## The workaround's test (*How it was proven*, subsection) — design facts (results: §"The workaround run (FL)")

| Chapter text | Source |
|---|---|
| same construction: LUT, NCO, mode word, `S` | FIX:62–70 ("CONSTRUCTION (the one the E4 test program used, EF-069)") |
| P3 driven by the measuring cog, low first half, high second | FIX:48–51; FIX:670–674 |
| printed block is the routine called, byte for byte; `burst_mode` mode bits / `burst_sel` checked before start | FIX:31–33, 42–44; control W FIX:106–107, FIX:324–336 (`check_dropin_words`), FIX:279–280 (measuring cog not started on failure) |
| every wait on a burst is `WAITXFI` | FIX:93 |
| three records per level | FIX:78, FIX:201 `REPS = 3` |
| calibration: C = D65 - D64, flushed start and end | FIX:79–82; FIX:706–729 |
| documented use: "clear", 64-clock burst, read; "clear" again, 65-clock burst, read; zero burst alone, read; 7-clock burst without zero burst | FIX:83–89; FIX:731–772 |
| must show both errata: second "clear" = first reading (E4); 63 × C, 65 × C, C, 6 × C (E5); else `RIG FAIL` and no verdict | FIX:115–123; FIX:495–530 (`check_positive_control`); FIX:389–390 |
| ten consecutive calls, N = 1, 2, 3, 4, 7, 64, 65, 255, 256, 1001, set with `SETWORD`, first call with the 7-clock term held | FIX:90–92, FIX:189–198, FIX:774–793 (`setword burst_mode, nn_, #0` at FIX:778); FIX:88–89 |
| program waits 1,000 clocks and takes its own idle reading | FIX:91–92; FIX:206 `WAIT_REREAD = 1000`; FIX:780–782 |
| pin checks before and after each record | FIX:111; FIX:677–679, 683–685 |
| outcome written into the program before the run: 60 calls N × C both sums; lead C on first call, 0 else; idle = before + sum | FIX:95–103, FIX:126–128; FIX:248 (`TOTAL_CALLS = NREC * FIX_CALLS` = 6 × 10) |
| -C: zero burst did not deliver; +C: an older term counted | FIX:129–132 |

## Measured-vs-derived labels

| Statement | Class | Basis |
|---|---|---|
| Before-and-after idle difference gives the burst (minus E5's term) | Measured | Run A in every repetition (L2:81–88, dA constant across five distinct P values) and the calibration pair (L2:66) |
| Read inside a burst: (R1 - P) + R2 equals the unread burst | Measured | L2:81–88 `dd=0` |
| The helper routine returns N × C for every call | Measured (60 of 60, run once) | FL:34–113, re-derived |
| SINC2: the zero burst as a flush | **Not tested**; the chapter says only "not tested ... not recommended" | LED:1051–1052 |
| Continuous `XCONT` SINC1 streams: the clear acts per read | Measured (SINC2 test's SINC1 arms) | S2L1:71, 118, 240, 353, 440 |

The ledger (LED:975) says `getxacc.yaml`'s read-before-and-after rule "is exactly what this
behaviour requires"; the chapter states only what run A measured.

## Code excerpts (verbatim, contiguous; printed lines now mirror ARCHIVE)

**Printed code now mirrors the conformed archive copy (2026-09-26, «#360»); the measuring PASM
is byte-identical to the as-run rig.** ARCHIVE = `examples-library/e4-getxacc-clear-gating-test.spin2`,
ARCHIVE-WKR = `examples-library/e4-e5-workaround-read-sums-test.spin2` (conformed 2026-09-26, task #360:
named `SITE_CAL_LO_END` in place of the literal `#2`; PASM measuring image byte-identical to
RIG/FIX's; ARCHIVE-WKR's workaround renames: see the note at the top).

| Chapter excerpt | RIG lines (as-run, history) | ARCHIVE lines (printed) | Max width |
|---|---|---|---|
| The drop-in block (*A proven workaround*) | FIX:808–837 | ARCHIVE-WKR:683–717 (see the drop-in section above) | 73 |
| Command words `dch_` ... `dlytab` (now includes the `dlytab` header comment, 13 lines) | RIG:686–696 | ARCHIVE:656–668 | 74 |
| Calibration before-and-after block `call #preamble` ... `mov ry_, 0-0` (now `mov site_, #SITE_CAL_LO_END` in place of `#2`) | RIG:494–502 | ARCHIVE:464–472 | 47 |
| Run B read inside the burst `call #preamble` ... `mov r1y_, 0-0` (unchanged by #360) | RIG:589–595 | ARCHIVE:559–565 | 63 |
| Workaround program's call loop `wkr_arm` ... `mov qy_, 0-0` (FIX's `fix_arm`/`fidx_`/`fixn_` renamed `wkr_arm`/`widx_`/`wkrn_` in #360; same widths) | FIX:775–782 | ARCHIVE-WKR:650–657 | 76 (`waitx ##WAIT_REREAD`) |
| Prose description of phase (i) (not excerpted: RIG:539, 540, 543, 546 exceed 76 columns) | RIG:533–551 | n/a | n/a |

Re-check (post-#360): the chapter's fences equal the ARCHIVE/ARCHIVE-WKR spans above (verified
by `engineering/tools/verify-example-corpus-identity.py`, GREEN). Pre-#360 check (history): one
awk over FIX, RIG, the E5 rig and both chapters located every fence of the chapter as a
contiguous rig range (the five rows above) and found no fence line over 76 columns and none
absent from a rig. RIG and FIX are kept as the as-run record; the measuring PASM itself is
unchanged by the #360 rename.

Prose about the workaround program's `DAT` block: markers FIX:807/838 (ARCHIVE-WKR:682/718);
`fixn_` holds the ten lengths (FIX:803–804; printed as ARCHIVE-WKR's `wkrn_`, :678–679); `WAIT_REREAD` = 1,000 (FIX:206); prints raw readings, controls, uncorrected
readings in units of C, one line per call, one `VERDICT:` line (FIX:372–397, 583, 627–639);
drives P3 and releases it (FIX:693–694).

## *Why it happens*: paraphrase basis

Paraphrased from BRF Part 2 ("Half A — the enable", "Half B — why the coincidence",
"The claim in one paragraph") and Part 4, at the programmer's-model level: the accumulators
update only on clocks of an active DDS/Goertzel command; the clear is a substitution inside that
update rather than a separate write; the read returns the value from before the clearing edge;
after a clear the accumulator holds the one pending term. No HDL fragment, signal name, module
name or line reference from BRF appears in the chapter. "By the study's reading, every mode
other than DDS/Goertzel behaves as the idle streamer does" rests on BRF Part 2's statement that
the update is gated on the single DDS/Goertzel mode pattern; the bench tested one other mode.
Unchanged from v0.1.0 except "Chapter 5" → "Erratum E5".

## Where the chapter departs from the ledger's wording

- LED:959 "Idle, or in any other streamer mode": the chapter says one other mode was tested
  (RIG:170–177 has one non-Goertzel mode), and attributes "every mode" to the study's reading.
- LED:966–967 counts "50 of 50 reads" beside G1, G2, G2L, G3 only; the 50 also include the idle
  reads before the calibration and run A/B bursts (RIG:344–352). The chapter gives the full
  composition.
- LED:968 "B itself grows across reps (488 → 14,335) with no clear between them": not used.
  Run B's read inside the burst does clear between repetitions (R2 = 13,786 whatever the
  starting value), so the chapter uses run A's P → RA growth instead.

## The workaround run (FL), 2026-09-26 — every placeholder filled from it

**FL** = `engineering/document-production/manuals/p2-errata/audit/verification-tests/logs/debug_260926-015810.log`
(208 lines). FL:6 `[DOWNLOAD TO RAM] File: e4-e5-fix-read-sums-test.bin | Size: 16378 bytes`;
FL:13 `clk 200 MHz; 3 records per level; 10 fix calls per record`. Run **once**, 2026-09-26
(FL:1). The coordinator states the `.bin` is the rig on disk (FIX); the drop-in block in the
chapter was byte-identical to FIX:808–837 before #360 and now equals ARCHIVE-WKR:683–717, the
same instructions (§"The drop-in block").

**Re-derivation, from the raw lines FL:24–113 only** (the program's own analysis lines
FL:116–204 were read only afterwards, as a cross-check; they agree):

- **Controls.** W: FL:24–25 (`burst_mode = $F007_0100`, `burst_sel = $0008_80A5`). Z and LUT:
  FL:29 (`LUT mismatches 0  zero_mode $F007_0004  zero_sel $0008_00A5`). PIN: FL:30, 44, 58
  (`P3 IN before/after 0/0`), FL:72, 86, 100 (`1/1`). NZ: every `P=` and `B=` on FL:32–113 is
  nonzero.
- **CAL**, D64 = R - B at N=64, D65 at N=65, C = D65 - D64, per record (FL:31, 45, 59, 73, 87,
  101): X D64 = 3,904 / D65 = 3,965 → C = 61 in records 0–2; -3,904 / -3,965 → C = -61 in
  records 3–5. Y 1,472 / 1,495 → 23; -1,472 / -1,495 → -23. (e.g. FL:31: 64,904 - 61,000 =
  3,904; 68,869 - 64,904 = 3,965.)
- **Positive control**, 12 rows (FL:32–33, 46–47, 60–61, 74–75, 88–89, 102–103): P2 = R1 in
  every row; R1 - P = ±3,843 (X) / ±1,449 (Y) = 63 × C; R2 - P2 = ±3,965 / ±1,495 = 65 × C;
  R3 - R2 = ±61 / ±23 = C; RD - R3 = ±366 / ±138 = 6 × C. First record X (FL:32): 72,712 - 68,869
  = 3,843; 76,677 - 72,712 = 3,965; 76,738 - 76,677 = 61; 77,104 - 76,738 = 366.
- **Workaround, 60 calls** (FL:34–43, 48–57, 62–71, 76–85, 90–99, 104–113): every `S=` equals N × C:
  X 61, 122, 183, 244, 427, 3_904, 3_965, 15_555, 15_616, 61_061 and Y 23, 46, 69, 92, 161,
  1_472, 1_495, 5_865, 5_888, 23_023 for N = 1, 2, 3, 4, 7, 64, 65, 255, 256, 1_001 in records
  0–2, negated in records 3–5. **lead** (call 0 B - RD): +61/+23 in records 0–2 (e.g. FL:34
  77,165 - FL:32 77,104 = 61; FL:34 29,095 - FL:33 29,072 = 23), -61/-23 in records 3–5 (e.g.
  FL:76 396,744 - FL:74 396,805 = -61); calls 1–9: B = previous call's Q on every line, both
  channels (lead 0). **idle** Q - (B + S) = 0 on every line, both channels (e.g. FL:43 117,242 +
  61,061 = 178,303 = Q). Tallies, re-derived: S = N×C 60/60, lead 60/60, idle 60/60; no miss of
  (N-1)×C or (N+1)×C. **Verdict re-derived: CONFIRMED** (the pre-registered rule, FIX:127–128).
- Cross-check lines: FL:137 (`E4 and E5 reproduced in all 12 rows`), FL:138 (`controls: ... all
  passed`), FL:202–203 (tallies 60/60/60, misses 0), FL:204 (`VERDICT: CONFIRMED`).

| Chapter number / statement | Source |
|---|---|
| "all 60 calls", "1 to 1001 clocks", "both input levels", "6 calls ... term still held" | FL:34–113 (re-derivation above); FL:13 |
| printed words `$F007_0100`, `$0008_80A5`; zero-burst words `$F007_0004`, `$0008_00A5` | FL:24, FL:25, FL:29 |
| 512 LUT longs read back unchanged | FL:29 (`LUT mismatches 0`); FIX:655–662 (all 512 read back) |
| P3 at its driven level before and after every record | FL:30, 44, 58, 72, 86, 100 |
| C = 61 / 23 (P3 low, 3 records), -61 / -23 (P3 high, 3 records) | FL:31, 45, 59, 73, 87, 101 (derived as above); cross-check FL:116–121 |
| 12 rows; second "clear" = first; 63C, 65C, C, 6C | FL:32–33, 46–47, 60–61, 74–75, 88–89, 102–103; cross-check FL:125–137 |
| first record cosine: P 68,869; R1 72,712 (3,843); P2 72,712; R2 76,677 (3,965); R3 76,738 (61); RD 77,104 (366) | FL:32 |
| cosine sums at P3 low 61 … 61,061; sine 23 … 23,023; negated at P3 high | FL:34–43 (record 0; same in FL:48–57, 62–71); FL:76–85 (record 3, negated; same in FL:90–99, 104–113) |
| 256-clock call 15,616 (256 × 61) vs 15,555 (255 × 61) | FL:42 (`N=256 X: ... S=15_616`); L2:81–88 (`dA=15_555`) |
| first call's before reading moved by exactly C: 77,165 against 77,104 | FL:34 (`B=77_165`), FL:32 (`RD=77_104`) |
| later before readings = previous own reading; own reading = before + sum | FL:34–113, every line (B vs previous line's Q; Q = B + S) |
| no (N-1)×C or (N+1)×C | re-derivation; cross-check FL:203 |
| largest accumulator value read 412,909 | FL:71 (`Q=412_909`), FL:73 (`B=412_909`); the largest value on FL:31–113 |
| run once, 2026-09-26, 200 MHz | FL:1, FL:13; coordinator's note (one log) |
| Status "Yes — 2026-09-26, on a P2 board at 200 MHz, run once; helper routine" | the above; kind per creation-guide §4.6 |
| "ran ... once, from cog RAM at 200 MHz, `$8000_0000`, one input pin, no DAC, 1 to 1001" | FIX:47–54, 63, 189–198, 647; FL:13, FL:34–113 (N values) |

Raw lines from FL, verbatim:

```
6: [2026-09-26T01:58:10.010] [SYSTEM] [DOWNLOAD TO RAM] File: e4-e5-fix-read-sums-test.bin | Size: 16378 bytes | Modified: 2026-09-26T07:55:15.622Z
13: [2026-09-26T01:58:10.832] Cog0  rig: NO jumper; the measuring cog drives P3 (low, then high); clk 200 MHz; 3 records per level; 10 fix calls per record
24: [2026-09-26T01:58:10.836] Cog0    burst_mode = $F007_0100 (mode bits must be $F007_0000; the rig sets the count per call)
25: [2026-09-26T01:58:10.837] Cog0    burst_sel  = $0008_80A5 (must be $0008_80A5)
29: [2026-09-26T01:58:10.838] Cog0  header: LUT mismatches 0  zero_mode $F007_0004  zero_sel $0008_00A5
30: [2026-09-26T01:58:10.839] Cog0  #0 P3 LOW  rep 0  P3 IN before/after 0/0
31: [2026-09-26T01:58:10.839] Cog0     CAL X: N=64 B=61_000 R=64_904  N=65 B=64_904 R=68_869   Y: N=64 B=23_000 R=24_472  N=65 B=24_472 R=25_967
32: [2026-09-26T01:58:10.840] Cog0     NAIVE X: P=68_869 R1=72_712 P2=72_712 R2=76_677 R3=76_738 RD=77_104
33: [2026-09-26T01:58:10.840] Cog0     NAIVE Y: P=25_967 R1=27_416 P2=27_416 R2=28_911 R3=28_934 RD=29_072
34: [2026-09-26T01:58:10.841] Cog0     call 0 N=1  X: B=77_165 S=61 Q=77_226  Y: B=29_095 S=23 Q=29_118
42: [2026-09-26T01:58:10.844] Cog0     call 8 N=256  X: B=101_626 S=15_616 Q=117_242  Y: B=38_318 S=5_888 Q=44_206
43: [2026-09-26T01:58:10.845] Cog0     call 9 N=1_001  X: B=117_242 S=61_061 Q=178_303  Y: B=44_206 S=23_023 Q=67_229
71: [2026-09-26T01:58:10.858] Cog0     call 9 N=1_001  X: B=351_848 S=61_061 Q=412_909  Y: B=132_664 S=23_023 Q=155_687
72: [2026-09-26T01:58:10.858] Cog0  #3 P3 HIGH rep 0  P3 IN before/after 1/1
73: [2026-09-26T01:58:10.859] Cog0     CAL X: N=64 B=412_909 R=409_005  N=65 B=409_005 R=405_040   Y: N=64 B=155_687 R=154_215  N=65 B=154_215 R=152_720
74: [2026-09-26T01:58:10.859] Cog0     NAIVE X: P=405_040 R1=401_197 P2=401_197 R2=397_232 R3=397_171 RD=396_805
76: [2026-09-26T01:58:10.860] Cog0     call 0 N=1  X: B=396_744 S=-61 Q=396_683  Y: B=149_592 S=-23 Q=149_569
85: [2026-09-26T01:58:10.865] Cog0     call 9 N=1_001  X: B=356_667 S=-61_061 Q=295_606  Y: B=134_481 S=-23_023 Q=111_458
138: [2026-09-26T01:58:10.893] Cog0  controls: W, Z, LUT, PIN, NZ, CAL and the POSITIVE CONTROL all passed
202: [2026-09-26T01:58:10.931] Cog0  fix tallies (of 60 calls, cosine AND sine): S = N*C 60  lead as expected 60  idle = 0 60
203: [2026-09-26T01:58:10.932] Cog0    S misses: (N-1)*C 0  (N+1)*C 0  other multiple of C 0  not a multiple of C (any check) 0
204: [2026-09-26T01:58:10.948] Cog0  VERDICT: CONFIRMED - burst_sums returned exactly N*C, cosine and sine, in all 60 calls (N = 1..1001, P3 low and high, consecutive, 6 after an unflushed burst), and left nothing held and nothing moving
```

No `PENDING-BENCH` placeholder remains in the chapter.
