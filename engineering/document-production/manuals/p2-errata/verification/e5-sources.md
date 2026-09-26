# E5 sources: Erratum E5, The Goertzel Accumulators Trail by One Clock

Chapter: `opus-master/e5-goertzel-one-clock-lag.md` (v0.2.0 shape, task «#359»). Every
number, quotation and code excerpt in the chapter, mapped to its source. Paths are
repo-relative; `M` = `engineering/document-production/manuals/p2-errata`. Internal document:
ids and paths are allowed here, never in the chapter.

**Classification ruling (arbiter, 2026-09-26).** The Goertzel SINC2 iteration-count corruption
is documented behaviour (the P2 Documentation's *NOTE ABOUT GOERTZEL SINC2 MODE*, Chip Gracey,
2024.12.16, SDT:1704–1705), so under `CLASSIFICATION-GUIDANCE.md` it is not an erratum and not
part of E5. Basis: the SINC2 rig's own header (S2R:152–155) says the one-clock lag's share
"cannot be isolated in a continuous stream ... the fit absorbs" it. The chapter therefore
carries SINC2 only as one scope paragraph in *A proven workaround* (the routine is SINC1-only;
the documented SINC2 constraint is separate; its two remedies held on a part) and one sentence
in *The test program*. It claims no causal link between the lag and the SINC2 corruption.

**Workaround wording (2026-09-26, task #360; Stephen's decision, voice-guide §2).** The reader's
change is a *workaround*, never a *fix* (a fix is a silicon revision). Section *The fix*
(`{#sec-e5-fix}`) is now *A proven workaround* (`{#sec-e5-workaround}`), rule-first: *What any
workaround must do* (the condition, as in the front matter's summary table), *One way, proven
on a real P2* and the block, then *Other ways that meet the condition*; the subsection *The
fix's test* is now *The workaround's test* (`{#sec-e5-workaround-proof}`). The CAUTION box's
third line is *Workaround* (the condition); the status row is *Workaround proven on silicon*.
FIX's reader copy is renamed `e4-e5-workaround-read-sums-test.spin2` (ARCHIVE-WKR below; its
renames are listed in `e4-sources.md`); no line added or removed, and the object image is
byte-identical to the pre-#360 archive. FIX and FL are the as-run record and keep their wording.

| Key | Path |
|---|---|
| LEDGER | `engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md` (EF-070 at 978–990; second session header 994–1005; EF-072 at 1027–1054) |
| LOG2 | `M/audit/verification-tests/logs/debug_260924-231829.log` (lag test, second run, style-conformed build) |
| LOG1 | `M/audit/verification-tests/logs-orig/debug_260924-204804.log` (lag test, first run, as-authored build) |
| RIG | `M/audit/verification-tests/test-so84-goertzel-last-term-lag.spin2` (reader name `e5-goertzel-one-clock-lag-test.spin2`) |
| FIX | `M/audit/verification-tests/e4-e5-fix-read-sums-test.spin2` (the as-run name; the reader's copy is `e4-e5-workaround-read-sums-test.spin2` since #360; ran once on silicon 2026-09-26, log FL) |
| FL | `M/audit/verification-tests/logs/debug_260926-015810.log` (the workaround run; full re-derivation and verbatim lines in `e4-sources.md` §"The workaround run (FL)") |
| S2R | `M/audit/verification-tests/test-goertzel-sinc2-iteration-count.spin2` (reader name `e5-goertzel-sinc2-iteration-count-test.spin2`; campaign copy `.../campaigns/2026-09-p2-errata-predictions/tests/`) |
| S2L1 | `M/audit/verification-tests/logs/debug_260925-214001.log` (SINC2 test, run 1, 21:40, `.bin` 25081 bytes, S2L1:14) |
| S2L2 | `M/audit/verification-tests/logs/debug_260925-214858.log` (SINC2 test, run 2, 21:48, same size, S2L2:14) |
| SDOC | `engineering/ingestion/sources/silicon-doc/p2-documentation.txt` (the 2025 capture) |
| SDT | `engineering/ingestion/sources/silicon-doc/silicon-doc-text.txt` (the current DOCX capture of the same P2 Documentation v35; the only capture holding the 2024.12.16 note) |
| CHIP | `engineering/ingestion/external-inputs/forum-threads/ProblemGoertzelSINC2mode/INGEST.md` (Chip Gracey's forum report, 2024-12-16; used only for authorship of the note, not quoted) |
| HARN | `M/verification/e5-harness-zero-burst.spin2` (v0.1.0 workaround harness; superseded, see below) |

LOG1 and LOG2 carry identical data on lines 20-145 (timestamps aside); every lag-test log line
quoted below is from LOG2 and appears with the same content at the same line number in LOG1.
S2L1 and S2L2 agree line for line except in the jitter arms and the verdict lines quoting them
(LEDGER:1002–1005); the S2L1 lines quoted in §4 have S2L2 counterparts at S2L2:87 (same text),
S2L2:591 (Q1 verdict) and S2L2:598–601 (Q4 lines), each with the same numbers.

## 0. The drop-in block (*A proven workaround*)

**Printed code now mirrors the conformed archive copy (2026-09-26, «#360»); the measuring PASM
is byte-identical to the as-run rig.** ARCHIVE-WKR = `examples-library/e4-e5-workaround-read-sums-test.spin2`
(renamed from `e4-e5-fix-read-sums-test.spin2` later in #360, lines unchanged; conformed 2026-09-26, task #360: the block's `'` line comments became a `{ }` block comment,
and a new `CON` part names `ZERO_COUNT` (4) and `INPUT_NIB` (3) in place of the literals
`#4`/`#3`; same instructions, same PASM measuring image, byte-identical to FIX's). See
`e4-sources.md` §"The drop-in block" for the full width/ASCII/byte-identity detail, identical
for this chapter since it prints the same block.

| Item | Source |
|---|---|
| The 35-line `pasm2` block under *One way, proven on a real P2* in *A proven workaround* (30 lines pre-#360) | ARCHIVE-WKR:683–717 (post-#360, between the markers ARCHIVE-WKR:682/718). Pre-#360: FIX:808–837, byte-identical (between the markers FIX:807 and FIX:838). The same block, byte for byte, is printed in Erratum E4's *A proven workaround*. Post-#360, the chapter's fence (chapter 56–90) equals ARCHIVE-WKR:683–717 (verified by `engineering/tools/verify-example-corpus-identity.py`, GREEN); pre-#360 the same awk, run over this file, printed `compared 30 chapter lines with 30 rig lines` and no `DIFF` line |
| Printed in full here as well as in E4 | a reader who lands on E5 first pastes without turning to E4; creation-guide §4.6 puts the proven block in every *A proven workaround* |
| **The run that proved it** | FL, 2026-09-26, run once, 200 MHz (FL:1, FL:13): 60 of 60 calls S = N × C, cosine and sine; re-derived from FL:24–113 in `e4-sources.md` §"The workaround run (FL)"; E5-specific rows in §5a below |

| Chapter text in *A proven workaround* | Source |
|---|---|
| *What any workaround must do*: deliver the burst's held last term before reading, in SINC1 mode | LEDGER:979–983 (EF-070: the last term is held and arrives with the next Goertzel burst); front matter summary table |
| *One way*: `burst_sums`, which ends every burst with a zero-term burst before reading and also steps around E4 | the block (above); FIX:24 ("combines both workarounds in one routine"), FIX:38–40 |
| guarantee: all N terms, no term left held; helper routine, SINC1 | FIX:24–28, FIX:127–128 (pre-registered outcome), met in FL (§5a) |
| "On silicon, this block returned exactly N terms ... in all 60 calls ...; in the 6 calls made while an earlier burst's term was still held, it added that term before its first reading, and it left no term for any later call" | FL:34–113 (S = N×C every line; call-0 lead = C in each record; later B = previous Q) — §5a |
| same routine as Erratum E4; one call steps around both | FIX:24 ("combines both workarounds in one routine") |
| usage; printed values are the test program's | FIX:809–810, FIX:830–831 |
| zero bursts: count 4, S[15:12] clear; first delivers the held term; second delivers the last term and leaves a zero held | FIX:812–815, FIX:35–41; mechanism LEDGER:979–983; LOG2:39 (`d2=-19` after a zero burst) |
| readings idle, no clear (Erratum E4) | FIX:39–41 |
| *Other ways*: by the mechanism under *Why it happens*, a Goertzel burst whose terms are all zero, run after the burst and before the reading, delivers the held term | the chapter's own *Why it happens* ("A zero-term burst works for the same reason"; study reading, §2); LEDGER:981–983 |
| *Other ways*: the kind measured is the routine's own (count 4, S[15:12] clear); in the erratum test, started by `XINIT` and read after 500 clocks, not `WAITXFI`, the reading was exactly N terms above the reading before the measured burst in all 16 sequences; other zero bursts not tested | RIG:183 (`ZCOUNT = 4`), RIG:181–182 (`$0000_00C3`, S[15:12] clear), RIG:187 (`WAIT_IDLE = 500`); LOG2:39 etc. (`d1 + d2 = N*C`, §3 last row), LOG2:143 (16 sequences); no other zero-burst form in RIG or FIX |
| cost: two zero bursts of 4 NCO rollovers; `WAITXFI`; 17 instructions, 8 longs | as in `e4-sources.md` (FIX:813, 817/821/823, 812–828, 830–837; SDOC:3500–3501; SDT:2097, 2182) |
| limits: one burst at a time; `XINIT` issues at once | SDOC:2742 / SDT:1282; SDT:1284 |
| conditions: cog RAM, `$8000_0000`, one pin, no DAC, N 1 to 1001, first call with a held term | FIX:47–54, 63, 88–92, 189–198, 647; "ran ... once", 200 MHz: FL:1, FL:13 |
| DAC output on each clock of a DDS/Goertzel command | SDOC:3985 / SDT:1555 |

### The SINC1-only scope paragraph (after the guarantee)

| Chapter text | Source |
|---|---|
| "The routine is for SINC1 mode." | FIX:5 ("(SINC1 only)"), FIX:28–29 ("nothing here runs SINC2"); FIX:64 and FIX:830 (mode word D[7] = 0, SINC1) |
| "its zero burst has not been tested as a flush" (in SINC2) | LEDGER:1051–1052 ("Scope note (study reading, untested): in SINC2 the E5 zero-burst workaround does not flush the first stage"); no SINC2 zero-burst-as-flush arm exists in any rig (S2R uses a SINC1 zero burst only, S2R:67–68, S2R:1503–1505) |
| "not recommended there" | follows from the untested scope note; arbiter ruling item 2 |
| "the P2 Documentation's note on Goertzel SINC2 mode, by Chip Gracey (2024.12.16)" | SDT:1704 (heading `NOTE ABOUT GOERTZEL SINC2 MODE (2024.12.16)`); authorship CHIP:7, CHIP:38–41 ("I made this note in the silicon doc"). Not in SDOC (`grep -n "NOTE ABOUT GOERTZEL"` over SDOC returns nothing) |
| "a varying number of iterations in a Goertzel cycle corrupts the current and next samples" | SDT:1705, paraphrased from "generates periodic problematic GETXACC readings when the number of iterations in a Goertzel cycle varies" and "Being off by a single clock cycle will corrupt the current and next samples." |
| "which is documented and is not this erratum" | arbiter ruling; CLASSIFICATION-GUIDANCE.md (documented behaviour is not class 1) |
| its two remedies: same-length NCO cycles, or `XZERO` | SDT:1705 (the note's own remedy: a clock frequency giving the same number of clocks per Goertzel cycle); CHIP:30, CHIP:49 (power-of-two count; XZERO); LEDGER:1050 |
| test program `e5-goertzel-sinc2-iteration-count-test.spin2`; 2026-09-25, 200 MHz, run twice | S2R:3 (rig), reader name per `appendix-a-test-programs.md:18`; S2R:35 and S2R:286 (`_clkfreq = 200_000_000`); LEDGER:1000–1005 (date, run twice, 21:40 and 21:49) |
| `SETXFRQ` `$0080_0000`, 256 clocks per cycle, 2,048-clock commands chained with `XCONT`; 0 of 1,020 SINC2 samples off | S2R:75–76 ("2^31 / F = 256 exactly. M = 8 -> every command 2048 clocks"); S2R:1571 (P2-S2 is `KIND_XCONT`); S2L1:75 (windows 2,048 ×1,021), S2L1:87 (`SINC2: 1_020 samples; outliers 0`), S2L1:593 (`power of two: 0 of 1_020 off`) |
| `XZERO` at `$0080_0040` (8 cycles) and `$00A3_D70C` (100 and 25,000): one length each; 0 of 1,020, 0 of 2,044, 0 of 12 changed | S2R:113–115 (XZS-S2, XZC-S2, XZL-S2); S2L1:509, 527, 545 (one window length each); S2L1:600–602 (`d changed in 0 of 1_020`, `0 of 2_044`, `0 of 12`); S2L1:603 (VERDICT Q4) |
| `XCONT` at the same settings gave 30, 12 and 4 corrupted samples | S2L1:600–602 (`XCONT twin ... outliers 30` / `outliers 12` / `outliers 4`) |

The paragraph makes no claim that the lag causes the SINC2 corruption (S2R:152–155; arbiter ruling).

### Superseded v0.1.0 workaround snippet

The v0.1.0 chapter printed a 10-line zero-burst snippet compiled in HARN (HARN:45–54; pnut-ts
1.55.8, `.bin` 6420 bytes, encodings recorded in the v0.1.0 sidecar). At v0.2.0 it is not
printed: the printed workaround is the FIX drop-in block (task «#359» decision 4). HARN is left in
place, unchanged. The measurement behind the old snippet (step 3's zero burst, 16 of 16) stays
in the chapter's proof as evidence.

## 1. Quotations and statements of Parallax documentation

| Chapter text | Source |
|---|---|
| "This mode is unique, in that it outputs and inputs on every clock in which the command is active." | SDOC:3985 (first sentence of the line); SDT:1555 |
| "The 8-bit sine (byte 3) and cosine (byte 2) values ... into their respective 32-bit accumulators." | SDOC:4094-4095 (one sentence across the line break); SDT:1602 |
| `SIN_ACC += SIN_MUL`, `COS_ACC += COS_MUL`, SINC1 case, D[23] = `%0`; each `_MUL` = bitstream sum × lookup value | SDOC:4100-4116 (D[23] table; `%0` SINC1 at 4107-4109; `SIN_MUL = bitstream_sum * lookup_sin` 4111, `COS_MUL = bitstream_sum * lookup_cos` 4112, `SIN_ACC += SIN_MUL` 4115, `COS_ACC += COS_MUL` 4116; "36" at 4113 is a page number); SDT:1610–1613 |
| CAUTION "(P2 Documentation, *DDS/Goertzel*)" | SDOC:3984 / SDT:1553 (heading) |
| KNOWN BUGS does not list this behaviour | SDOC:197-227 (lists only the SETQ/ALTx and AUGS/ALTx bugs); `grep -n -i "goertzel\|getxacc"` over SDOC returns no line in 197-227 |
| S[15:12] selects which pins are summed; S[19] inversion | SDOC:4002-4006; SDOC:4035-4044 (`%0xxx_1xxx` "Base pin +3 is summed", `(0 ⇢ -1, 1 ⇢ +1)`) |
| `SETXFRQ` `$8000_0000` = one rollover per clock | SDOC:2753-2754 |
| D[15:0] counts NCO rollovers | SDOC:3500-3501 |
| GETXACC: cosine into D, sine into the next instruction's S | SDOC:4097-4098 |

The v0.1.0 paragraph citing design-material intent (CLASS:39) was removed at v0.2.0: *What the
P2 is documented to do* names only the P2 Documentation.

## 2. Claims about what the part does

| Chapter claim | Source |
|---|---|
| Reading after N clocks holds N-1 terms; the last waits in an internal register no instruction reads; added on the first active clock of the next Goertzel burst; waiting does not deliver it | LEDGER:978-981 |
| Zero burst (same mode, S[15:12] clear) delivers the held term; nothing spills | LEDGER:981-983 |
| 16 of 16; sign flips with P3; sine channel same pattern with 37 | LEDGER:987-989 |
| Rig conditions (lag test): bare P2 board, 200 MHz, pnut-ts 1.55.8 -d, 2026-09-24, run twice from two builds with identical measuring engines, every value matched | LEDGER:892-894 |
| Not published by Parallax | LEDGER:978 heading "(new)"; LEDGER:887-889; KNOWN BUGS above |
| Mechanism in *Why it happens* | study brief Part 2, paraphrased at programmer's-model level; no signal/module names, no HDL, no line refs (unchanged from v0.1.0) |

## 3. Numbers (lag test, unchanged from v0.1.0)

| Number in chapter | Meaning | Source |
|---|---|---|
| 64, 65 | burst lengths N | RIG:184-185 (`N_A = 64`, `N_B = 65`); LOG2:36,41 |
| 16 sequences; 4 repetitions; both levels | run size | RIG:84-85, 186, 192; LOG2:143 |
| 1000 clocks | R1 to R1b wait | RIG:188 (`WAIT_R1B = 1000`), RIG:698-699 |
| 0 (R1b-R1) in all 16 | idle stability | LOG2:39,44,...,114 (every `dx:` row reads `R1b-R1=0`); LOG2:120 |
| 500 clocks | wait after each XINIT | RIG:187 (`WAIT_IDLE = 500`), RIG:695 etc. |
| 4 | zero-burst count | RIG:183 (`ZCOUNT = 4`), RIG:737 |
| 512 LUT longs | LUT fill | RIG:636-638 (`#$1FF` down to 0 with `djnf`), RIG:49 |
| `$2513_0000`, `$13` (19), `$25` (37) | LUT long, cosine and sine bytes | RIG:176-179; LOG2:33 |
| `$0C3`, `0`, `$1FF` | LUT readback addresses | RIG:641-643, 733-735; LOG2:33 |
| `$8000_0000` | SETXFRQ | RIG:632, 731 |
| `$F007_0000` | mode word | RIG:180, 736; RIG:154-156 (field breakdown) |
| `$0000_80C3`, `$0000_00C3` | term / zero S operands | RIG:181-182, 158-159 |
| `DEBUG_COGS = %0000_0001` | debugger confinement | RIG:173 |
| cog 1 | measuring cog | LOG2:32 |
| 200 MHz | clock | RIG:172; LEDGER:892 |
| 2026-09-24 | run date | LOG2:1, LOG1:1; LEDGER:893 |
| -19 / +19, C per level | measured C | LOG2:118 |
| -37 / +37 | sine C | LOG2:123 |
| results table, P3 low N=64 | `-1_197`, 0, `-19`, `-1_197`, `-1_216`, `-19` | LOG2:39 |
| results table, P3 low N=65 | `-1_216`, 0, `-19`, `-1_216`, `-1_235`, `-19` | LOG2:44 |
| results table, P3 high N=64 | `1_197`, 0, `19`, `1_197`, `1_216`, `19` | LOG2:79 |
| results table, P3 high N=65 | `1_216`, 0, `19`, `1_216`, `1_235`, `19` | LOG2:84 |
| "other three repetitions read the same values" | | LOG2:49,59,69 (= 39); 54,64,74 (= 44); 89,99,109 (= 79); 94,104,114 (= 84) |
| sine, P3 low N=64: `d1=-2_331`, `d2=-37`, `d3=-2_331`, `d4=-2_368`, `d5=-37` | | LOG2:40 |
| sine lag and carry pattern 16 of 16 | | LOG2:124 |
| 16 of 16 lag; carry arm | | LOG2:143, 145 |
| outcomes table (lag / no lag / lost) | | RIG:102-107; LOG2:23-27 |
| C measured as (R2-B)[65] - (R2-B)[64] | | RIG:61-68, 470 |
| 2 Mbaud; `pnut-ts -d`; success looks like | | RIG:163-168 |
| run twice, identical values | | LOG1:20-145 vs LOG2:20-146 (same data); LEDGER:893-894 |
| zero burst: after it, N terms over the reading before the burst; next burst `(N-1)*C` | | LOG2:39 etc. (`d1 + d2 = N*C`: -1,197 + -19 = -1,216 = 64 × -19; `d3 = (N-1)*C`); LEDGER:981–983 |

## 4. Raw log lines the numbers were taken from

Lag test, LOG2, verbatim (the one accumulator label in them is the renamed `xsum`/`ysum`, see
`verification/README.md`):

```
32: [2026-09-24T23:18:30.654] Cog0  measuring cog = 1 (debugger restricted to cog 0)
33: [2026-09-24T23:18:30.654] Cog0  LUT readback [$0C3]=$2513_0000 [0]=$2513_0000 [$1FF]=$2513_0000  expected $2513_0000
39: [2026-09-24T23:18:30.656] Cog0     dx: B-B0=0 d1=-1_197 R1b-R1=0 d2=-19 d3=-1_197 d4=-1_216 d5=-19
40: [2026-09-24T23:18:30.657] Cog0     dy: B-B0=0 d1=-2_331 R1b-R1=0 d2=-37 d3=-2_331 d4=-2_368 d5=-37
44: [2026-09-24T23:18:30.659] Cog0     dx: B-B0=0 d1=-1_216 R1b-R1=0 d2=-19 d3=-1_216 d4=-1_235 d5=-19
79: [2026-09-24T23:18:30.675] Cog0     dx: B-B0=0 d1=1_197 R1b-R1=0 d2=19 d3=1_197 d4=1_216 d5=19
84: [2026-09-24T23:18:30.677] Cog0     dx: B-B0=0 d1=1_216 R1b-R1=0 d2=19 d3=1_216 d4=1_235 d5=19
118: [2026-09-24T23:18:30.693] Cog0  C measured, xsum: P3 LOW reps -19 -19 -19 -19 | P3 HIGH reps 19 19 19 19  (predicted -19 / +19)
120: [2026-09-24T23:18:30.694] Cog0  controls: LUT ok, pin ok, idle ok (R1b-R1 = 0), zero-after-zero ok, all deltas whole multiples of 19, C ok
123: [2026-09-24T23:18:30.698] Cog0  ysum: idle moves 0, zero-after-zero moves 0, non-multiples of 37: 0, C_meas P3 LOW -37 -37 -37 -37 HIGH 37 37 37 37
124: [2026-09-24T23:18:30.698] Cog0  YSUM: TRUE (lag) pair in 16 of 16, carry arm TRUE in 16 of 16 (see dy rows for the rest)
143: [2026-09-24T23:18:30.710] Cog0  counts over 16 sequences: TRUE 16  no-lag 0  lost 0  other 0
145: [2026-09-24T23:18:30.726] Cog0  VERDICT: CONFIRMED - all 16 sequences (N=64,65; P3 low,high; 4 reps) read d1=(N-1)C, d2=C, R1b-R1=0, and the carry arm read (N-1)C, N*C, C
```

SINC2 test (for the scope paragraph's two remedies only), S2L1, verbatim (no accumulator label
in these lines):

```
87: [2026-09-25T21:40:03.858] Cog0    SINC2: 1_020 samples; outliers 0 (huge >= 1000 terms: 0, max |e| 0); window-changed samples 0, of them clean 0; outliers with no window change 0
593: [2026-09-25T21:40:05.691] Cog0  VERDICT Q1: CONFIRMED - power of two: 0 of 1_020 off; non-power-of-two: every odd window corrupts that sample and the next, then clean (pairs NPS 15, NPL 15, CHP 6); rates 30/1_020, 30/1_020, 12/2_044
600: [2026-09-25T21:40:05.697] Cog0  Q4 XZS-S2 (SINC2, 2^23+64, XZERO): windows 2_048..2_048 clocks, d changed in 0 of 1_020 (d(k=4) = 4_194_304, C*n^2 = 4_194_304) | XCONT twin NPS-S2 (SINC2, 2^23+64, XCONT): odd windows 15, outliers 30
601: [2026-09-25T21:40:05.698] Cog0  Q4 XZC-S2 (SINC2, 1 MHz, 100 cycles, XZERO): windows 20_000..20_000 clocks, d changed in 0 of 2_044 (d(k=4) = 400_000_000, C*n^2 = 400_000_000) | XCONT twin CHP-S2 (SINC2, 1 MHz, 100 cycles, XCONT): odd windows 6, outliers 12
602: [2026-09-25T21:40:05.699] Cog0  Q4 XZL-S2 (SINC2, 1 MHz, 25000 cycles, XZERO): windows 5_000_000..5_000_000 clocks, d changed in 0 of 12 (d(k=4) = -1_004_630_016, C*n^2 = -1_004_630_016) | XCONT twin XCL-S2 (SINC2, 1 MHz, 25000 cycles, XCONT): odd windows 2, outliers 4
603: [2026-09-25T21:40:05.701] Cog0  VERDICT Q4: CONFIRMED - XZERO kept one window length and an unchanging SINC2 sample at 10.24 us, 100 us and 25 ms measurements (streams 10.5 / 204.8 / 400 ms), where the XCONT twins varied and corrupted
```

## 5. The workaround's test (*How it was proven*, subsection) — design facts (results: §5a)

| Chapter text | Source |
|---|---|
| calls the printed routine byte for byte | FIX:31–33, FIX:779 |
| 64-clock burst 63 × C; 65-clock burst right after 65 × C; zero burst alone C; 7-clock 6 × C, term left held | FIX:115–121, FIX:184–186 (`N_NAIVE_A = 64`, `N_NAIVE_B = 65`, `N_DIRTY = 7`), FIX:731–772 |
| first call starts with the term held; before reading gains exactly C, later calls nothing | FIX:88–89, FIX:99–101 |
| every call returns N × C, N = 1 to 1001 | FIX:98, FIX:189–198 |
| (N-1) × C = zero burst did not deliver | FIX:131 |

## 5a. The workaround run (FL) — the E5 results paragraph

Re-derived from FL's raw lines (FL:24–113), not from its verdict line; the full derivation
(controls, CAL, all 12 positive-control rows, all 60 calls, both channels) is in
`e4-sources.md` §"The workaround run (FL)". Verdict re-derived: CONFIRMED.

| Chapter number / statement | Source |
|---|---|
| every control passed | FL:24–25 (W), FL:29 (Z, LUT), FL:30/44/58/72/86/100 (PIN); cross-check FL:138 |
| C = 61 / 23 at P3 low, -61 / -23 at P3 high, every record | FL:31, 45, 59 (X: 64,904 - 61,000 = 3,904 = D64; 68,869 - 64,904 = 3,965 = D65; C = 61; Y 1,472 / 1,495 → 23), FL:73, 87, 101 (negated); cross-check FL:116–121 |
| lag in all 12 rows | FL:32–33, 46–47, 60–61, 74–75, 88–89, 102–103; cross-check FL:137 |
| cosine at P3 low: 3,843 (63 × 61), 3,965 (65 × 61), 61, 366 (6 × 61) | FL:32: 72,712 - 68,869; 76,677 - 72,712; 76,738 - 76,677; 77,104 - 76,738 (same differences FL:46, FL:60) |
| sine: 1,449, 1,495, 23, 138 | FL:33: 27,416 - 25,967; 28,911 - 27,416; 28,934 - 28,911; 29,072 - 28,934 |
| P3 high: the same values negated | FL:74–75, 88–89, 102–103 (e.g. FL:74: 401,197 - 405,040 = -3,843; 396,805 - 397,171 = -366) |
| first call found exactly C: 77,165 against 77,104 (P3 low, first record); 396,744 against 396,805 (P3 high, fourth record) | FL:34 `B=77_165`, FL:32 `RD=77_104`; FL:76 `B=396_744`, FL:74 `RD=396_805` |
| every later before reading = previous own reading | FL:35–43, 49–57, 63–71, 77–85, 91–99, 105–113: each `B=` equals the previous line's `Q=`, X and Y |
| 60 calls N × C; 61 (N=1) to 61,061 (N=1001) cosine at P3 low; -23 to -23,023 sine at P3 high | FL:34 (`S=61`), FL:43 (`S=61_061`); FL:76 (`S=-23`), FL:85 (`S=-23_023`); all 60 lines FL:34–113 |
| none returned (N-1) × C | re-derivation; cross-check FL:203 (`(N-1)*C 0`) |
| run once, 2026-09-26, 200 MHz | FL:1, FL:13 |
| Status "Yes — 2026-09-26, on a P2 board at 200 MHz, run once; helper routine (SINC1)" | the above; kind per creation-guide §4.6; SINC1: FIX:5, FIX:64 |

Raw lines used here beyond those quoted in `e4-sources.md`, verbatim:

```
46: [2026-09-26T01:58:10.846] Cog0     NAIVE X: P=186_172 R1=190_015 P2=190_015 R2=193_980 R3=194_041 RD=194_407
75: [2026-09-26T01:58:10.860] Cog0     NAIVE Y: P=152_720 R1=151_271 P2=151_271 R2=149_776 R3=149_753 RD=149_615
113: [2026-09-26T01:58:10.879] Cog0     call 9 N=1_001  X: B=122_061 S=-61_061 Q=61_000  Y: B=46_023 S=-23_023 Q=23_000
137: [2026-09-26T01:58:10.892] Cog0    E4 and E5 reproduced in all 12 rows: the idle GETXACC cleared nothing, the burst read one term short, the held term arrived later
```

## 6. Code and the test-program section

| Chapter code / text | Source |
|---|---|
| The drop-in block (35 lines post-#360, 30 pre-#360) | ARCHIVE-WKR:683–717 (post-#360); FIX:808–837 (pre-#360, §0) |
| Excerpt: burst, R1, R1b, zero burst, R2 (12 lines) | RIG:694-705, verbatim |
| Excerpt: carry arm (14 lines) | RIG:707-720, verbatim |
| Excerpt: the workaround program's second "clear" and 65-clock burst (12 lines) | FIX:746–757, verbatim (widths 23–71); in the reader's copy ARCHIVE-WKR:621–632 (unchanged by the #360 renames). FIX:736 and FIX:740 (86 and 82 columns) keep the first half of that arm out of the excerpt |
| v0.1.0 excerpt `dmode_` .. `imk_` (RIG:736-739) | dropped at v0.2.0 (excerpt budget 2–4); `dz_`, `imz_`, `imk_` are described in prose before the first excerpt (RIG:737–739) |
| one sentence: the SINC2 test program checks the documented SINC2 constraint, not this erratum | arbiter ruling item 4; S2R:13–27 (what the rig tests) |
| Widths / verbatim check | every fence line ≤ 76 and present in a rig; each fence located as one contiguous rig range by the v0.2.0 awk check (FIX:808–837, RIG:694–705, RIG:707–720, FIX:746–757) |

No `PENDING-BENCH` placeholder remains in the chapter; each was filled from FL (§5a).
