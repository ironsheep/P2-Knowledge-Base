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
| **FIX** | `engineering/document-production/manuals/p2-errata/audit/verification-tests/e4-e5-fix-read-sums-test.spin2` (reader name `e4-e5-fix-read-sums-test.spin2`; 871 lines, header "Updated.... 26 Sep 2026"; **not yet run on silicon** at this writing; not yet replicated to the campaign `tests/` folder) |
| **S2R** | `.../audit/verification-tests/test-goertzel-sinc2-iteration-count.spin2` (reader name `e5-goertzel-sinc2-iteration-count-test.spin2`) |
| **S2L1** | `.../audit/verification-tests/logs/debug_260925-214001.log` (SINC2 test, run 1) |
| **HAR** | `engineering/document-production/manuals/p2-errata/verification/e4-harness-difference.spin2` (v0.1.0 workaround harness; superseded, see below) |
| **BRF** | `engineering/document-production/manuals/p2-errata/code-validation/test-briefs/BRIEF-SO80.md` (mechanism only; not quoted) |

L1 and L2 carry the measurement lines at the **same line numbers** (23–102). Every `Cog0` line
of the two logs is identical except the `INIT ... jump` address (different builds) and the
final `DEBUG_END_SESSION` line, present only in L2. Command used to check this (v0.1.0):
`diff <(grep -o "Cog0 .*" L2) <(grep -o "Cog0 .*" L1)` with the full paths above; output was
exactly those two differences.

## The drop-in block (*The fix*)

| Item | Source |
|---|---|
| The 30-line `pasm2` block that opens *The fix* | FIX:808–837, byte-identical: the lines strictly between the markers `' ---- DROP-IN BEGIN ----` (FIX:807) and `' ---- DROP-IN END ----` (FIX:838). The same block is printed in Erratum E5's *The fix* |
| Widths | 15–69 columns on non-blank lines (FIX:808–837; widest FIX:815, FIX:826 and FIX:830, 69), all ≤ 76 (`awk "NR>=775 && NR<=838 { printf \"%d|%d|%s|\\n\", NR, length(\$0), \$0 }" FIX`); no tab and no non-ASCII byte anywhere in FIX (`grep -n -P "[^\x20-\x7E]" FIX` returns nothing) |
| Byte-identity check | `awk 'NR==FNR { if (FNR>=808 && FNR<=837) r[++n]=$0; next } /^## The fix/ { f=1 } f && /^```pasm2/ { inb=1; next } inb && /^```/ { exit } inb { m++; if ($0 != r[m]) print "DIFF " m ": " $0 } END { print "compared " m " chapter lines with " n " rig lines" }' FIX <chapter>` → `compared 30 chapter lines with 30 rig lines`, no `DIFF` line |
| Kind: helper routine | creation-guide §4.6; FIX:4–6 ("drop-in fix burst_sums: one routine that runs a DDS/Goertzel burst and returns its exact cosine and sine sums") |
| **The run that proved it** | **PENDING.** FIX has not run on silicon at this writing (task «#359»: Stephen is running it now; RUN-SHEET.md:12–23, row 10, logs to `logs-fixes/`). Nothing in the chapter claims a fix result; every result slot is a `PENDING-BENCH e45-fix` comment (list at the end of this file) |

### What the chapter says about the block, and where it comes from

| Chapter text | Source |
|---|---|
| guarantee: sums of your burst alone, all N terms, whatever the accumulators held before | the claim under test, FIX:24–28 and FIX:127–128 (CONFIRMED outcome). **Stands only on the fix run's CONFIRMED verdict** (PENDING-BENCH comment beside it) |
| put your `XINIT` D in `burst_mode`, S in `burst_sel`, `CALL #burst_sums` with the streamer idle | FIX:809–810 (the block's own comment); FIX:34 ("with the streamer idle at entry") |
| example values: SINC1, no DAC, pins P0–P3, count 256, P3 inverted and summed, LUT offset `$0A5` | FIX:830–831 (`$F007_0100`, `$0008_80A5`); decode FIX:64–66 ("[11:8]=0 (no DAC), [7]=0 (SINC1), [6:3]=0 (pins P0..P3)"; "S[19]=1 (invert), S[15]=1 (sum P3 only), LUT $0A5"); count `$0100` = 256; DOC:4035–4044 (summation table) |
| two idle readings; `GETXACC` clears nothing idle | FIX:39–41; the erratum itself (this chapter, L2:78–79) |
| zero bursts: your mode word, count 4, S[15:12] clear, every term zero | FIX:812–815 (`mov`/`setword #4, #0`/`mov`/`setnib #0, #3`); FIX:35, FIX:67–68; SETNIB nibble 3 = bits 15:12; S[15:12] are the four pin-summation enables (DOC:4002–4006) |
| first zero burst delivers any held term; second delivers the burst's last | FIX:38–40; the E5 mechanism (LED:978–983) |
| two zero bursts of 4 NCO rollovers each, at your `SETXFRQ` rate | FIX:813 (count 4); D[15:0] counts NCO rollovers (DOC:3500–3501) |
| cog waits in `WAITXFI` until each command has finished | FIX:817, 821, 823; `WAITXFI` = "Wait for the streamer-finished event flag" (SDT:2097), flag "Set whenever the streamer runs out of commands" (SDT:2182) |
| 17 instructions, 8 longs | counted: FIX:812–828 (17 instruction lines), FIX:830–837 (8 `long` lines) |
| SINC1 only; in SINC2 the zero burst is not tested as a flush and the routine is not recommended; E5's *The fix* notes the separate, documented SINC2 constraint | FIX:5–6, FIX:28–29 ("SINC1 only: EF-072's scope note (untested) is that in SINC2 the zero burst does not flush the first stage ... nothing here runs SINC2"); LED:1051–1052 (scope note, study reading, untested). The SINC2 constraint is the P2 Documentation's note (SDT:1704–1705); arbiter ruling 2026-09-26: documented behaviour, not an erratum, not part of E5 (see `e5-sources.md` head) |
| `XINIT` issues at once; does not fit an `XCONT` stream | DOC:2742 / SDT:1282 ("Issue command immediately, zeroing phase"); SDT:1284 (XCONT waits for the final NCO rollover) |
| test conditions: cog RAM, NCO `$8000_0000`, one input pin, no DAC output, bursts 1 to 1001 | FIX:47–54 (P3 only; no DAC), FIX:63 (`SETXFRQ $8000_0000`), FIX:189–198 (N list), FIX:647 (`DAT org 0`, cog exec). "runs" (present tense, test design), not "ran": PENDING comment beside it |
| DAC channels output on every clock of a DDS/Goertzel command | DOC:3985 / SDT:1555 ("outputs and inputs on every clock in which the command is active") |
| not tested: DAC enabled, more than one pin, other NCO frequencies, hub execution, values near the 32-bit limit | scope of FIX (FIX:53, 47–48, 63, 647); DOC:4095 ("32-bit accumulators") |

### Superseded v0.1.0 workaround snippet

The v0.1.0 chapter printed a 10-line before-and-after snippet compiled in HAR (see the v0.1.0
record below). At v0.2.0 it is no longer printed: the printed fix is the FIX drop-in block,
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
| `$F007_0100`, `$0008_80A5` | The fix (printed values) | FIX:830–831; the same values as RIG:128–129 ("drun_ = $F007_0100", "son_ = $0008_80A5") |
| 4,000-clock wait | Proof | RIG:179 `WAIT_IDLE = 4000`; RIG:125; RIG:86 |
| NCO frequency `$8000_0000` | The fix (limits), Proof | FIX:63, FIX:178, FIX:651; RIG:178 `FRQ = $8000_0000`, RIG:478 `setxfrq frq_`, RIG:130 |
| 36,600 (largest value read) | Proof (run A paragraph) | L2:63 `rep 7 runB ... R1=36_600`; the largest value on any raw line L2:23–64 (sine values are smaller) |
| 200 MHz | Proof, Status | RIG:161; L2:21 `clk 200 MHz`; LED:892 |
| nothing connected to P0 to P7 | Proof | RIG:34 "NO JUMPER, nothing connected to P0..P7"; L2:21 "NO jumper" |
| debugger confined to cog 0 | Proof | RIG:162 `DEBUG_COGS = %0000_0001`; RIG:45–47 |
| P3 driven low, smart pin off | Proof | RIG:35–37, RIG:475–476 |
| 512 LUT longs, `$173D_0000` | Proof | RIG:58, RIG:129 (`lutv_ = $173D_0000`), RIG:480–487 (fill + readback); FIX:69–70 (same in the fix program) |
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
| outcomes fixed before the run (dd = R1, -C, +C) | Proof | RIG:25–31 (written before the run), RIG:405–416 (classes) |
| `POLLXFI` finished / still running | Proof | RIG:663–674 (`xfi_end`, `xfi_mid`); L2:68 |
| 255 terms, not 256 = Erratum E5 | Sees, Proof | LED:979–980 (EF-070: "A reading taken after a burst of N clocks holds N − 1 terms") |

## The fix's test (*How it was proven*, subsection) — design facts, no results

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
| outcome fixed before the run: 60 calls N × C both sums; lead C on first call, 0 else; idle = before + sum | FIX:95–103, FIX:126–128; FIX:248 (`TOTAL_CALLS = NREC * FIX_CALLS` = 6 × 10) |
| -C: zero burst did not deliver; +C: an older term counted | FIX:129–132 |

## Measured-vs-derived labels

| Statement | Class | Basis |
|---|---|---|
| Before-and-after idle difference gives the burst (minus E5's term) | Measured | Run A in every repetition (L2:81–88, dA constant across five distinct P values) and the calibration pair (L2:66) |
| Read inside a burst: (R1 - P) + R2 equals the unread burst | Measured | L2:81–88 `dd=0` |
| The helper routine returns N × C for every call | **PENDING** (claim under test) | FIX has not run; PENDING-BENCH comments |
| SINC2: the zero burst as a flush | **Not tested**; the chapter says only "not tested ... not recommended" | LED:1051–1052 |
| Continuous `XCONT` SINC1 streams: the clear acts per read | Measured (SINC2 test's SINC1 arms) | S2L1:71, 118, 240, 353, 440 |

The ledger (LED:975) says `getxacc.yaml`'s read-before-and-after rule "is exactly what this
behaviour requires"; the chapter states only what run A measured.

## Code excerpts (verbatim, contiguous)

| Chapter excerpt | Source lines | Max width |
|---|---|---|
| The drop-in block (*The fix*) | FIX:808–837 | 69 |
| Command words `dch_` ... `dlytab` | RIG:686–696 | 56 |
| Calibration before-and-after block `call #preamble` ... `mov ry_, 0-0` | RIG:494–502 | 35 |
| Run B read inside the burst `call #preamble` ... `mov r1y_, 0-0` | RIG:589–595 | 63 |
| Fix program's call loop `fix_arm` ... `mov qy_, 0-0` | FIX:775–782 | 76 (FIX:781) |
| Prose description of phase (i) (not excerpted: RIG:539, 540, 543, 546 exceed 76 columns) | RIG:533–551 | n/a |

Check run at v0.2.0 (one awk over FIX, RIG, the E5 rig and both chapters) located every fence
of the chapter as a contiguous rig range (the five rows above) and found no fence line over 76
columns and none absent from a rig.

Prose about the fix program's `DAT` block: markers FIX:807/838; `fixn_` holds the ten lengths
(FIX:803–804); `WAIT_REREAD` = 1,000 (FIX:206); prints raw readings, controls, uncorrected
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

## PENDING-BENCH placeholders (fix run `e45-fix`)

| Chapter location | What fills it |
|---|---|
| *The fix*, after the guarantee sentence | Keep the sentence only on `VERDICT: CONFIRMED` (60 of 60 calls S = N*C, cosine and sine; lead and idle as expected); on any other verdict, rewrite *The fix* per creation-guide §4.6 |
| *The fix*, **Limits**, "Conditions of the test" | Confirm from the run the conditions the sentence after it states (NCO `$8000_0000`, one pin, no DAC, N list, both levels, cog RAM, 200 MHz); change "runs" to "ran" |
| *How it was proven*, *The fix's test*, results comment | CAL C measured (cos/sin, both levels); positive control reproduced in N of 12 rows with one example; tallies of 60 (S, lead, idle); one or two example call rows; the VERDICT line; date, runs, agreement between runs |
| *Status*, "Fix proven on silicon" | "Yes — <date>, helper routine" on CONFIRMED |
