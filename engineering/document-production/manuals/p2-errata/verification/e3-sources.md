# E3 verification sidecar: Erratum E3, GETCT Returns a Stale Upper Long

Chapter: `opus-master/e3-getct-stale-upper-long.md` (v0.2.0 shape, task «#359»). Every number,
quotation and code excerpt in the chapter, mapped to the file and line it came from. Paths are
relative to the repository root unless marked `M/` (= `engineering/document-production/manuals/p2-errata/`).

Abbreviations used below:

| Tag | File |
|---|---|
| LEDGER | `engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md` |
| SD | `engineering/ingestion/sources/silicon-doc/p2-documentation.txt` |
| RIG-A | `M/audit/verification-tests/test-o18-getct-upper-stale-runA.spin2` (byte-identical to `hardware-verification/campaigns/2026-09-p2-errata-predictions/tests/` copy, checked with `cmp` at v0.1.0) |
| RIG-B | `M/audit/verification-tests/test-o18-getct-upper-stale-runB.spin2` (byte-identical to the campaign copy, checked with `cmp` at v0.1.0) |
| RIG-FIX | `M/audit/verification-tests/e3-fix-keeper-cog-test.spin2` (the workaround's test program, under the name it ran with; since #360 the reader's copy is `examples-library/e3-workaround-keeper-cog-test.spin2`). Run on silicon once, 2026-09-26 (LOG-FIX). |
| LOG-A2 | `M/audit/verification-tests/logs/debug_260924-231939.log` (Run A, second build; .bin 13037 bytes = the rig on disk) |
| LOG-A1 | `M/audit/verification-tests/logs-orig/debug_260924-204946.log` (Run A, first build) |
| LOG-B2 | `M/audit/verification-tests/logs/debug_260924-231846.log` (Run B, second build; .bin 12550 bytes = the rig on disk) |
| LOG-B1 | `M/audit/verification-tests/logs-orig/debug_260924-204835.log` (Run B, first build) |
| LOG-FIX | `M/audit/verification-tests/logs/debug_260926-015546.log` (the workaround run, run once; LOG-FIX:14 downloads `e3-fix-keeper-cog-test.bin` of 13008 bytes, the size of the `.bin` beside RIG-FIX on disk per `ls -l`) |
| APP-A | `M/opus-master/appendix-a-test-programs.md` |
| KB-MD | `deliverables/ai/P2/language/spin2/constructs/method_definition.yaml` |
| KB-COGINIT | `deliverables/ai/P2/language/spin2/methods/coginit.yaml` |

Numbers quoted in the chapter's reader text are taken from the second-build logs (LOG-A2,
LOG-B2), the build that matches the rig files on disk. The first-build logs were checked for
the same D values and verdicts.

Reader filenames: APP-A:13-15 names the three E3 programs `e3-getct-stale-upper-long-runA.spin2`,
`e3-getct-stale-upper-long-runB.spin2` and `e3-workaround-keeper-cog-test.spin2` (the last renamed
in #360 from RIG-FIX's own name `e3-fix-keeper-cog-test.spin2`, RIG-FIX:3); the chapter uses
those names.

**Workaround wording (2026-09-26, task #360; Stephen's decision, voice-guide §2).** The reader's
change is a *workaround*, never a *fix* (a fix is a silicon revision). Section *The fix*
(`{#sec-e3-fix}`) is now *A proven workaround* (`{#sec-e3-workaround}`), rule-first: *What any
workaround must do* (the condition, as in the front matter's summary table), *One way, proven
on P2 hardware* and the keeper block, then *Other ways that meet the condition* (the Run B
evidence, formerly the section's closing Run B paragraph). The CAUTION box's third line is
*Workaround* (the condition); the status row is *Workaround proven on silicon*. ARCHIVE-WKR's
drop-in labels read `E3 Workaround:` (ARCHIVE-WKR:115, 118); `HI_FIX1/2` and `P_FIX` are renamed
`HI_WKR1/2` and `P_WKR`, and comments and `debug()` text say *workaround*: no line added or
removed, and the object image is byte-identical to the pre-#360 archive (pnut-ts 1.55.8, `-d`
and without; the `-d` binary differs only in its DEBUG data). The reading labels `F1`/`F1L`/
`F2`/`F2L` are `string()` literals in the object image and are kept. RIG-FIX and LOG-FIX are the
as-run record and keep their own wording.

---

## 0. CAUTION box and opening paragraph

| Chapter text | Source |
|---|---|
| Expected: "`GETCT WC` returns the upper 32 bits of the P2's one 64-bit free-running counter, whichever cog executes it" | SD:436 (one counter, "64-bit free-running counter"), SD:81 ("GETCT WC retrieves upper 32-bits"); no qualification by cog (absence claim, §1 last row) |
| Actual: stale upper long in a cog of 4-7 started after the group had no running cog at a wrap; behind by one per wrap missed; first wrap 2^32^ clocks after reset | LEDGER:941-946; LOG-A2:65 (D=1 after one missed wrap), LOG-A2:185 (D=2 after two) |
| Workaround: a cog of 4-7 must be running at every wrap of the lower long, from the first wrap on | LEDGER:941-944 (the group's upper long advances at a wrap only while a cog of the group runs); met by the keeper (RIG-FIX:200-211, §5; LOG-FIX, §9) and by Run B's cog 4 (§3.2) |
| "starts its first cog there more than 2^32^ clocks after reset, 21.47 s at 200 MHz" | LEDGER:944-946; 21.47 s from RIG-A:109-110 (§3) |
| "a program that stops every cog of 4-7 and starts one there again after a wrap has passed" | LOG-A2:140 (cog 4 stopped), :172 (wrap 4 with `running=%00000011`), :185 (D=2 after restart) |
| "Plain `GETCT` ... is not affected" | lower-long bracket held in every pair: LOG-A2:234-244, LOG-B2:144-151 `lo-bracket-fails=0` |

## 1. Quotations of Parallax documentation (section *What the P2 is documented to do*)

| Chapter text | Source |
|---|---|
| "Its overview of the chip lists, among what the hub provides the cogs" | SD:370-439, the chip overview following the table of contents (`Each cog has:` SD:390; `The hub provides the cogs with:` SD:414) |
| > 64-bit free-running counter which increments every clock, cleared on reset | SD:436, verbatim |
| "Its list of the improvements made to the chip" | SD:62 `The following improvements were made to the chip:` |
| > System counter extended to 64 bits. GETCT WC retrieves upper 32-bits. | SD:81, verbatim |
| "its section EVENTS" | SD:5111 `EVENTS` |
| > Event 1 = CT passed CT1 (CT is the lower 32-bits of the free-running 64-bit global counter) | SD:5131, verbatim |
| "It does not qualify the value `GETCT WC` returns by cog number, or by which other cogs are running." | Absence claim. Every `GETCT` occurrence in SD (`grep -n -i getct`): 81, 5408, 5411, 5674, 5715, 11350. None qualifies the read by cog or by cog activity. SD:5674 lists `GETCT+WC` among instructions that hold off an interrupt branch; unrelated. |
| "The KNOWN BUGS section of the P2 Documentation does not list this behaviour." | SD:197-227 (read in full): two items only, the `SETQ`/`ALTx` PTRx-delta item (E1) and the `ALTx`/`AUGS` item (E2); no counter item |

Cross-check (not cited in reader text): `deliverables/ai/P2/language/pasm2/getct.yaml`:13-17
("Read the system counter into D ... With WC: D receives the upper 32 bits of the 64-bit
counter") and :36 oneliner "Get CT[31:0], or CT[63:32] if WC, into D". The KB does not yet
carry the defect (creation-guide §6, F-462..466).

## 2. Cog groups (cogs 0-3, cogs 4-7)

- LEDGER:941 "Cogs 0–3 and 4–7 each read their own copy of the 64-bit counter."
- RIG-A:15 `(cogs 0-3 = group 0, cogs 4-7 = group 1)` (the program's stated arrangement).
- Sampled cogs: cog 1 (RIG-A:518 `coginit #1, pSampler`), cog 4 (RIG-A:533 `coginit #4, pSampler`);
  cog 0 is the reference. The chapter says so explicitly ("The test sampled cog 1 and cog 4;
  the other cogs of each group were not sampled separately").

## 3. Numbers in the chapter

| Number / value in chapter | Where in chapter | Source |
|---|---|---|
| 2^32^ clocks per wrap; 21.47 s at 200 MHz | CAUTION box; opening; *What the P2 does*; *What your program sees* | RIG-A:109 `CLOCK / RUN TIME: _clkfreq = 200_000_000 -> 2^32 clocks = 21.47 s per` / RIG-A:110 `wrap.`; RIG-B:112-113 same; RIG-FIX:116-117 same. LEDGER:945 gives the rounded "21.5 s at 200 MHz"; the chapter uses the rig's 21.47 s. |
| 200 MHz | throughout; Status | RIG-A:123 `_clkfreq    = 200_000_000`; RIG-FIX:131 same; LEDGER:892 "bare P2 board, 200 MHz" |
| 2026-09-24, run twice | *How it was proven on P2 hardware*; Status | LEDGER:893 "RAM download with reset, 2026-09-24 (Stephen). **Run twice**, from two builds"; log headers LOG-A2:1, LOG-B2:1, LOG-A1, LOG-B1 (all 2026-09-24) |
| debugger confined to cog 0 | *How it was proven on P2 hardware* (Run A/B and the workaround program) | RIG-A:124 / RIG-B:127 `DEBUG_COGS  = %0000_0001`; RIG-FIX:132 same; LEDGER:890 |
| "as first written, and with its comments and layout conformed ... measuring code unchanged" | *How it was proven on P2 hardware* | LEDGER:893-894 "(as authored, then style-conformed with identical measuring engines): every measured value matched" |
| "Every D value and every verdict matched between the two builds" | *How it was proven on P2 hardware* | LOG-A1:234-245 vs LOG-A2:234-245 (slot 0..10 D and st identical; both VERDICT CONFIRMED); LOG-B1:152-160 vs LOG-B2:144-152 (slots 0..7 identical; both VERDICT CONFIRMED) |
| `$1000_0000`, `$F000_0000` (pair window) | *How it was proven on P2 hardware* | RIG-A:126-127 `LOWIN   = $1000_0000` / `HIWIN   = $F000_0000`; RIG-A:39-40; LEDGER:948; RIG-FIX:134-135 same |
| `$E000_0000` (late reading) | *How it was proven on P2 hardware* | RIG-A:128 `LATE    = $E000_0000`; RIG-FIX:136 same |
| ten pairs per reading | *What your program sees*; *How it was proven on P2 hardware* | RIG-A:129 `NPAIRS  = 10`; RIG-FIX:137 same; every `=> D=` line in all four logs ends `valid pairs=10 tries=10` |
| "compared unsigned" (lower-long check) | *How it was proven on P2 hardware* | RIG-A:42 `LO-BRACKET = refB.lo < sampler.lo < refA.lo (unsigned)`; RIG-A:315 uses `+<`; RIG-FIX:56, :403 same |
| 100 ms | *How it was proven on P2 hardware* (controls) | RIG-A:79 `C5  every request answered within 100 ms (sampler alive).`; RIG-A:304 `take_pair(mb, seq, clkfreq / 10)`; RIG-FIX:140 `ACK_TIMEOUT_MS = 100` |
| `$00DB_96FF` (Run B cog 4 start) | *A proven workaround* (*Other ways that meet the condition*) | LOG-B2:15 |
| about 105 s (Run A), about 44 s (Run B) | *The test program* | RIG-A:110-111 `Run A ends at CT hi=4, lo=$E000_0000: about 4.9 x 21.47 s` / `= ~105 s after reset (plus download).`; RIG-B:113-114 `Run B ends at CT hi=2, lo=$1000_0000:` / `about 2.06 x 21.47 s = ~44 s after reset (plus download).` |
| about 67 s (workaround program) | *The test program* | MEASURED: LOG-FIX session start 01:55:46.807 to the last line 01:56:53.488 = 66.7 s (the chapter and Appendix A say "about 67 s"); the rig's design comment RIG-FIX:117-118 says `~66 s after reset (plus download)` |
| `pnut-ts` 1.55.8, `-d` | *The test program* | RIG-A:119 `COMPILER: pnut-ts v1.55.8,  pnut-ts -d -l test-o18-getct-upper-stale-runA.spin2`; LEDGER:893; RIG-FIX:127 `COMPILER: pnut-ts v1.55.8,  pnut-ts -d e3-fix-keeper-cog-test.spin2` |
| "at reset only cog 0 runs" | *What the P2 does*; *Why it happens* | LOG-A2:22 and LOG-B2:14 `running cogs=%00000001` at boot; LEDGER:944 |
| cog 7, cogs 4, 5, 6 (workaround program) | *A proven workaround*; *How it was proven on P2 hardware* | RIG-FIX:36-43 (cog map), :157-159 `SMP_COG_A = 4` / `_B = 5` / `_C = 6`, :201 `KEEPER_COG = 7` |
| "seven cogs remain" | *A proven workaround* (cost) | 8 cogs: SD:382 `8 cogs (processors)`; RIG-FIX:143 `COG_COUNT      = 8`; the keeper holds one |

### 3.1 Run A readings (table rows A; *What the P2 does*; *What your program sees*)

Raw lines, LOG-A2 (second build), verbatim:

```
22:[2026-09-24T23:19:40.038] Cog0  boot: cog0 CT=$0000_0000_$00BE_74FE running cogs=%00000001
35:[2026-09-24T23:19:41.314] Cog0  R0  cog1 hi=0 => D=0 status=0 valid pairs=10 tries=10
51:[2026-09-24T23:20:00.113] Cog0    alive CT=$0000_0000_$F000_119E wraps-seen=0 running=%00000011
52:[2026-09-24T23:20:01.456] Cog0    alive CT=$0000_0001_$0000_0616 wraps-seen=1 running=%00000011
54:[2026-09-24T23:20:02.793] Cog0  --- cog 4 started (first group-1 cog since reset) ---
55:[2026-09-24T23:20:02.794] Cog0  A1a cog4 hi=1 p1 ref=$0000_0001_$1020_DB39 smp=$0000_0000_$1020_DB59 ref2=$0000_0001_$1020_DBA1 D=1 lo-bracket=1
65:[2026-09-24T23:20:02.799] Cog0  A1a cog4 hi=1 => D=1 status=0 valid pairs=10 tries=10
76:[2026-09-24T23:20:02.806] Cog0  C1a cog1 hi=1 => D=0 status=0 valid pairs=10 tries=10
100:[2026-09-24T23:20:20.237] Cog0  A1b cog4 hi=1 late p10 ref=$0000_0001_$E013_C129 smp=$0000_0000_$E013_C141 ref2=$0000_0001_$E013_C191 D=1 lo-bracket=1
101:[2026-09-24T23:20:20.238] Cog0  A1b cog4 hi=1 late => D=1 status=0 valid pairs=10 tries=10
112:[2026-09-24T23:20:20.245] Cog0  C1b cog1 hi=1 late => D=0 status=0 valid pairs=10 tries=10
116:[2026-09-24T23:20:22.931] Cog0    alive CT=$0000_0002_$0000_0246 wraps-seen=2 running=%00010011
118:[2026-09-24T23:20:24.258] Cog0  A2  cog4 hi=2 p1 ref=$0000_0002_$1001_4D51 smp=$0000_0002_$1001_4D69 ref2=$0000_0002_$1001_4DB9 D=0 lo-bracket=1
128:[2026-09-24T23:20:24.264] Cog0  A2  cog4 hi=2 => D=0 status=0 valid pairs=10 tries=10
139:[2026-09-24T23:20:24.281] Cog0  C2  cog1 hi=2 => D=0 status=0 valid pairs=10 tries=10
140:[2026-09-24T23:20:24.281] Cog0  --- cog 4 stopped; waiting for CT hi=4 with cogs 4-7 idle (~43 s) ---
156:[2026-09-24T23:20:44.405] Cog0    alive CT=$0000_0003_$0000_010E wraps-seen=3 running=%00000011
172:[2026-09-24T23:21:05.880] Cog0    alive CT=$0000_0004_$0000_043E wraps-seen=4 running=%00000011
174:[2026-09-24T23:21:07.217] Cog0  --- cog 4 restarted after 2 missed wraps ---
175:[2026-09-24T23:21:07.218] Cog0  A4a cog4 hi=4 p1 ref=$0000_0004_$1020_B5B1 smp=$0000_0002_$1020_B5D1 ref2=$0000_0004_$1020_B619 D=2 lo-bracket=1
185:[2026-09-24T23:21:07.224] Cog0  A4a cog4 hi=4 => D=2 status=0 valid pairs=10 tries=10
196:[2026-09-24T23:21:07.231] Cog0  C4a cog1 hi=4 => D=0 status=0 valid pairs=10 tries=10
221:[2026-09-24T23:21:24.662] Cog0  A4b cog4 hi=4 late => D=2 status=0 valid pairs=10 tries=10
232:[2026-09-24T23:21:24.669] Cog0  C4b cog1 hi=4 late => D=0 status=0 valid pairs=10 tries=10
234:[2026-09-24T23:21:24.670] Cog0  slot 0: D=0 st=0 lo-bracket-fails=0
235:[2026-09-24T23:21:24.670] Cog0  slot 1: D=1 st=0 lo-bracket-fails=0
236:[2026-09-24T23:21:24.671] Cog0  slot 2: D=0 st=0 lo-bracket-fails=0
237:[2026-09-24T23:21:24.671] Cog0  slot 3: D=1 st=0 lo-bracket-fails=0
238:[2026-09-24T23:21:24.671] Cog0  slot 4: D=0 st=0 lo-bracket-fails=0
239:[2026-09-24T23:21:24.671] Cog0  slot 5: D=0 st=0 lo-bracket-fails=0
240:[2026-09-24T23:21:24.672] Cog0  slot 6: D=0 st=0 lo-bracket-fails=0
241:[2026-09-24T23:21:24.672] Cog0  slot 7: D=2 st=0 lo-bracket-fails=0
242:[2026-09-24T23:21:24.672] Cog0  slot 8: D=0 st=0 lo-bracket-fails=0
243:[2026-09-24T23:21:24.672] Cog0  slot 9: D=2 st=0 lo-bracket-fails=0
244:[2026-09-24T23:21:24.672] Cog0  slot 10: D=0 st=0 lo-bracket-fails=0
245:[2026-09-24T23:21:24.673] Cog0  VERDICT: CONFIRMED - cog 4 D=1 at hi=1, 0 at hi=2, 2 after two missed wraps; cog 1 D=0 throughout
```

Slot map (RIG-A:139-140): 0=R0 cog1 hi=0, 1=A1a, 2=C1a, 3=A1b, 4=C1b, 5=A2, 6=C2, 7=A4a,
8=C4a, 9=A4b, 10=C4b. `st=0` = all ten pairs agreed (not ST_MIXED) and no lower-long bracket
failure (RIG-A:136, :326-333).

Chapter values taken from these lines:

| Chapter | Line(s) |
|---|---|
| cog 4 `$0000_0000_$1020_DB59`; cog 0 `$0000_0001_$1020_DB39`, `$0000_0001_$1020_DBA1` | LOG-A2:55 |
| cog 4 `$0000_0000_$E013_C141` late in one span | LOG-A2:100 (last A1b pair) |
| cog 4 `$0000_0002_$1001_4D69` early in the next | LOG-A2:118 (first A2 pair) |
| "upper long went from 0 to 2 across one wrap" | LOG-A2:100 smp hi `$0000_0000` -> LOG-A2:118 smp hi `$0000_0002`; one wrap between (LOG-A2:116 wraps-seen=2) |
| Table row A hi=0: cog 4 not read, cog 1 D 0 | LOG-A2:35; cogs 4-7 idle: LOG-A2:23-53 `running=%00000011` |
| Table row A hi=1 just after start: cog 4 D 1, cog 1 D 0 | LOG-A2:65, :76 |
| Table row A hi=1 late: 1, 0 | LOG-A2:101, :112 |
| Table row A hi=2: 0, 0 | LOG-A2:128, :139 |
| Table row A hi=4 just after restart: 2, 0 | LOG-A2:185, :196; no cog 4-7 running across wraps 3 and 4: LOG-A2:141-173 `running=%00000011` |
| Table row A hi=4 late: 2, 0 | LOG-A2:221, :232 |
| lower-long check held in every pair | LOG-A2:234-244 `lo-bracket-fails=0` (every slot) |

First-build confirmation, LOG-A1, verbatim:

```
55:[2026-09-24T20:50:10.099] Cog0  A1a cog4 hi=1 p1 ref=$0000_0001_$1020_D896 smp=$0000_0000_$1020_D8B3 ref2=$0000_0001_$1020_D903 D=1 lo-bracket=1
65:[2026-09-24T20:50:10.105] Cog0  A1a cog4 hi=1 => D=1 status=0 valid pairs=10 tries=10
101:[2026-09-24T20:50:27.543] Cog0  A1b cog4 hi=1 late => D=1 status=0 valid pairs=10 tries=10
128:[2026-09-24T20:50:31.570] Cog0  A2  cog4 hi=2 => D=0 status=0 valid pairs=10 tries=10
185:[2026-09-24T20:51:14.530] Cog0  A4a cog4 hi=4 => D=2 status=0 valid pairs=10 tries=10
221:[2026-09-24T20:51:31.968] Cog0  A4b cog4 hi=4 late => D=2 status=0 valid pairs=10 tries=10
234:[2026-09-24T20:51:31.976] Cog0  slot 0: D=0 st=0 lo-bracket-fails=0
235:[2026-09-24T20:51:31.976] Cog0  slot 1: D=1 st=0 lo-bracket-fails=0
236:[2026-09-24T20:51:31.976] Cog0  slot 2: D=0 st=0 lo-bracket-fails=0
237:[2026-09-24T20:51:31.977] Cog0  slot 3: D=1 st=0 lo-bracket-fails=0
238:[2026-09-24T20:51:31.977] Cog0  slot 4: D=0 st=0 lo-bracket-fails=0
239:[2026-09-24T20:51:31.977] Cog0  slot 5: D=0 st=0 lo-bracket-fails=0
240:[2026-09-24T20:51:31.977] Cog0  slot 6: D=0 st=0 lo-bracket-fails=0
241:[2026-09-24T20:51:31.977] Cog0  slot 7: D=2 st=0 lo-bracket-fails=0
242:[2026-09-24T20:51:31.978] Cog0  slot 8: D=0 st=0 lo-bracket-fails=0
243:[2026-09-24T20:51:31.978] Cog0  slot 9: D=2 st=0 lo-bracket-fails=0
244:[2026-09-24T20:51:31.978] Cog0  slot 10: D=0 st=0 lo-bracket-fails=0
245:[2026-09-24T20:51:31.994] Cog0  VERDICT: CONFIRMED - cog 4 D=1 at hi=1, 0 at hi=2, 2 after two missed wraps; cog 1 D=0 throughout
```

(LOG-A1:55 is the sample the ledger quotes at LEDGER:950, `$0000_0000_$1020_D8B3`.)

### 3.2 Run B readings (table rows B; *Other ways that meet the condition* in *A proven workaround*)

Raw lines, LOG-B2 (second build), verbatim:

```
14:[2026-09-24T23:18:46.844] Cog0  boot: cog0 CT=$0000_0000_$00BB_E587 running cogs=%00000001
15:[2026-09-24T23:18:46.844] Cog0  --- cogs 1 and 4 started at CT=$0000_0000_$00DB_96FF (group 1 kept running from here on) ---
28:[2026-09-24T23:18:48.121] Cog0  B0  cog4 hi=0 => D=0 status=0 valid pairs=10 tries=10
39:[2026-09-24T23:18:48.128] Cog0  C0  cog1 hi=0 => D=0 status=0 valid pairs=10 tries=10
56:[2026-09-24T23:19:08.262] Cog0    alive CT=$0000_0001_$0000_0AFF wraps-seen=1 running=%00010011
68:[2026-09-24T23:19:09.596] Cog0  B1a cog4 hi=1 => D=0 status=0 valid pairs=10 tries=10
79:[2026-09-24T23:19:09.602] Cog0  C1a cog1 hi=1 => D=0 status=0 valid pairs=10 tries=10
104:[2026-09-24T23:19:27.044] Cog0  B1b cog4 hi=1 late => D=0 status=0 valid pairs=10 tries=10
115:[2026-09-24T23:19:27.051] Cog0  C1b cog1 hi=1 late => D=0 status=0 valid pairs=10 tries=10
119:[2026-09-24T23:19:29.737] Cog0    alive CT=$0000_0002_$0000_0E97 wraps-seen=2 running=%00010011
131:[2026-09-24T23:19:31.071] Cog0  B2  cog4 hi=2 => D=0 status=0 valid pairs=10 tries=10
142:[2026-09-24T23:19:31.077] Cog0  C2  cog1 hi=2 => D=0 status=0 valid pairs=10 tries=10
144:[2026-09-24T23:19:31.078] Cog0  slot 0: D=0 st=0 lo-bracket-fails=0
145:[2026-09-24T23:19:31.078] Cog0  slot 1: D=0 st=0 lo-bracket-fails=0
146:[2026-09-24T23:19:31.078] Cog0  slot 2: D=0 st=0 lo-bracket-fails=0
147:[2026-09-24T23:19:31.079] Cog0  slot 3: D=0 st=0 lo-bracket-fails=0
148:[2026-09-24T23:19:31.079] Cog0  slot 4: D=0 st=0 lo-bracket-fails=0
149:[2026-09-24T23:19:31.079] Cog0  slot 5: D=0 st=0 lo-bracket-fails=0
150:[2026-09-24T23:19:31.080] Cog0  slot 6: D=0 st=0 lo-bracket-fails=0
151:[2026-09-24T23:19:31.080] Cog0  slot 7: D=0 st=0 lo-bracket-fails=0
152:[2026-09-24T23:19:31.096] Cog0  VERDICT: CONFIRMED - kept group 1: cog 4 D=0 at hi=1 and hi=2; cog 1 D=0 throughout
```

Slot map (RIG-B:148-149): 0=B0, 1=C0, 2=B1a, 3=C1a, 4=B1b, 5=C1b, 6=B2, 7=C2.

| Chapter | Line(s) |
|---|---|
| "cog 4, started at the beginning of that program while the lower long read `$00DB_96FF` and kept running" | LOG-B2:15 |
| "read the same upper long as cog 0 before the first wrap and after each of the first two" | LOG-B2:28 (hi=0), :68 and :104 (hi=1), :131 (hi=2), all D=0 |
| Table row B hi=0: 0, 0 | LOG-B2:28, :39 |
| Table row B hi=1 early: 0, 0 | LOG-B2:68, :79 |
| Table row B hi=1 late: 0, 0 | LOG-B2:104, :115 |
| Table row B hi=2: 0, 0 | LOG-B2:131, :142 |
| cog 4 running through wraps 1 and 2 | LOG-B2:16-57, :80-120 `running=%00010011` |
| lower-long check held in every pair | LOG-B2:144-151 `lo-bracket-fails=0` |
| "In Run B the cog kept running was the cog that read the counter" | RIG-B:189-193 (cog 4 is the sampler, started at program start) |

First-build confirmation, LOG-B1, verbatim:

```
23:[2026-09-24T20:48:36.620] Cog0  --- cogs 1 and 4 started at CT=$0000_0000_$00DC_DB05 (group 1 kept running from here on) ---
36:[2026-09-24T20:48:37.896] Cog0  B0  cog4 hi=0 => D=0 status=0 valid pairs=10 tries=10
76:[2026-09-24T20:48:59.371] Cog0  B1a cog4 hi=1 => D=0 status=0 valid pairs=10 tries=10
112:[2026-09-24T20:49:16.820] Cog0  B1b cog4 hi=1 late => D=0 status=0 valid pairs=10 tries=10
139:[2026-09-24T20:49:20.846] Cog0  B2  cog4 hi=2 => D=0 status=0 valid pairs=10 tries=10
152:[2026-09-24T20:49:20.853] Cog0  slot 0: D=0 st=0 lo-bracket-fails=0
153:[2026-09-24T20:49:20.853] Cog0  slot 1: D=0 st=0 lo-bracket-fails=0
154:[2026-09-24T20:49:20.854] Cog0  slot 2: D=0 st=0 lo-bracket-fails=0
155:[2026-09-24T20:49:20.854] Cog0  slot 3: D=0 st=0 lo-bracket-fails=0
156:[2026-09-24T20:49:20.854] Cog0  slot 4: D=0 st=0 lo-bracket-fails=0
157:[2026-09-24T20:49:20.854] Cog0  slot 5: D=0 st=0 lo-bracket-fails=0
158:[2026-09-24T20:49:20.855] Cog0  slot 6: D=0 st=0 lo-bracket-fails=0
159:[2026-09-24T20:49:20.855] Cog0  slot 7: D=0 st=0 lo-bracket-fails=0
160:[2026-09-24T20:49:20.870] Cog0  VERDICT: CONFIRMED - kept group 1: cog 4 D=0 at hi=1 and hi=2; cog 1 D=0 throughout
```

### 3.3 Controls, Run A and Run B (section *How it was proven on P2 hardware*)

| Chapter control | Source |
|---|---|
| cog 1 D = 0 every reading, else no verdict | RIG-A:67-69 (C1), :233-239, :245-246 |
| cog 0 upper long = wraps cog 0 watched, every poll | RIG-A:70-73 (C2), :416-429 |
| running-cog set polled throughout every wait; Run A no cog 4-7 before cog 4 | RIG-A:74-77 (C3), :433-454; RIG-B:78-79 |
| boot: upper long 0, only cog 0 running | RIG-A:78 (C4), :162-173 |
| every request answered within 100 ms | RIG-A:79 (C5), :304 |
| expected D fixed before the run | RIG-A:142-146 (P_A1_TRUE..P_CTRL); RIG-B `P_B_TRUE`/`P_B_FALSE`/`P_CTRL` (RIG-B:151-154) |
| No RIG FAIL fired | no `RIG FAIL` / `HALTED` line in any of the four logs |

### 3.4 Pair protocol and D (section *How it was proven on P2 hardware*)

- Pair definition: RIG-A:31-44; cog 0 side in inline PASM2, RIG-A:382-400
  (`getct rhb wc` / `getct rlb` before `wrlong reqNum, mb`; `rdlong shi, phi` /
  `rdlong slo, plo` / `getct rha wc` / `getct rla` after the ack).
- Valid-pair rule: RIG-A:311 (`rhb <> rha or not inwin(rlb) or not inwin(slo) or not inwin(rla)` -> discard).
- D and bracket: RIG-A:314-315.
- Reading = NPAIRS agreeing pairs: RIG-A:298-333.
- The workaround program uses the same definitions: RIG-FIX:45-57 ("the measuring engine of
  test-o18-getct-upper-stale-runA/B, unchanged"), :399 (valid-pair rule), :402-403 (D and
  bracket), :389-422 (reading).

## 4. Code excerpts (section *The test program*; printed lines now mirror ARCHIVE)

All excerpts are contiguous, verbatim, and every fenced line in the chapter is 76 columns or
fewer. Checked on 2026-09-26 with an `awk` line-by-line comparison of each chapter fence against
its source range (CLAIMS of the «#359» E3 dispatch report), and an `awk` width pass over every
fenced line.

**Printed code now mirrors the conformed archive copy (2026-09-26, «#360»); the measuring PASM
is byte-identical to the as-run rig.** ARCHIVE-A = `examples-library/e3-getct-stale-upper-long-runA.spin2`,
ARCHIVE-B = `examples-library/e3-getct-stale-upper-long-runB.spin2`, ARCHIVE-WKR =
`examples-library/e3-workaround-keeper-cog-test.spin2` (renamed from `e3-fix-keeper-cog-test.spin2`
later in #360, lines unchanged; all conformed 2026-09-26, task #360: named
mailbox indices `MB_HI_IDX`/`MB_LO_IDX`, single-exit `if bHalted == FALSE` / `if status ==
SUCCESS` restructuring, named `smpCog`/`baseMask`/`pLabel` parameters in place of `mb1`/`mb4`/`name`;
PASM measuring image byte-identical to RIG-A/RIG-B/RIG-FIX's).

| # | Fence | RIG lines (as-run, history) | ARCHIVE lines (printed) | Content |
|---|---|---|---|---|
| 1 | `pasm2` | RIG-A:540-548 (identical at RIG-B:537-545) | ARCHIVE-A:534-542 | sampler loop through `wrlong  s_lo, ptra[MB_LO_IDX]`. RIG-A:549 / ARCHIVE-A:543 (`wrlong  s_req, ptra[MB_ACK_IDX]`, the ack) is over 76 columns and is described in prose instead. |
| 2 | `spin2` | RIG-A:183-191 | ARCHIVE-A:153-164 | Run A defect step: wait with cogs 4-7 idle, start cog 4, read cog 4 and cog 1; ARCHIVE-A wraps each step in `if bHalted == FALSE` (the #360 single-exit restructuring) |
| 3 | `spin2` | RIG-B:189-193 | ARCHIVE-B:134-139 | Run B: both samplers from program start; ARCHIVE-B guards the step with `if status == SUCCESS` |
| 4 | `spin2` | RIG-FIX:296-303 | ARCHIVE-WKR:236-244 | the workaround program's `arm` body: start a sampler in the named cog, check the running-cog set, read, stop, check again; ARCHIVE-WKR's parameter is `pLabel` (was `name`) and the read/stop/check-again steps are guarded by `if bHalted == FALSE` |

Re-check (post-#360): the chapter's fences equal the ARCHIVE-A/B/WKR spans above (verified by
`engineering/tools/verify-example-corpus-identity.py`, GREEN); RIG-A/B/FIX are kept as the
as-run record and are no longer byte-identical to the printed fences (names and guards differ;
the measuring PASM itself is unchanged).

The v0.1.0 D-and-bracket excerpt (RIG-A:314-317) was dropped to keep four excerpts; its content
is carried in prose under *How it was proven on P2 hardware* (§3.4).

Prose around the excerpts:

- "started explicitly in cog 1 and in cog 4 (`COGINIT #1` and `COGINIT #4`), with its hub
  mailbox address in `PTRA`": RIG-A:504-534 (`setq mb` / `coginit #1, pSampler`,
  `setq mb` / `coginit #4, pSampler`); RIG-A:537 `PTRA = mailbox`.
- "writes the request number back as its acknowledgment and returns to `s_loop`":
  RIG-A:549-550.
- "`cogstop(SMP_COG)` at upper long 2 and a second `start_cog4` at upper long 4": RIG-A:199-210
  (`cogstop(4)` pre-#360); ARCHIVE-A:180-196 (`cogstop(SMP_COG)`, `SMP_COG` = 4).
- "The workaround's test program carries the block of *A proven workaround* unchanged, between
  the comments `BEGIN DROP-IN` and `END DROP-IN`": RIG-FIX:199 `' ---- BEGIN DROP-IN ----`, :212
  `' ---- END DROP-IN ----`; in the reader's copy ARCHIVE-WKR:114 and :127.
- "its `main()` goes on to call the rest of the test": RIG-FIX:213 `  run_rig()`.
- "the same sampler instructions": RIG-FIX:597-603 and :607 are identical to RIG-A:540-546 and
  :550; RIG-FIX:604-606 carry the same instructions as RIG-A:547-549 with different trailing
  comments (compared by eye from the `awk` width listings). RIG-FIX:593-595 states "Same code as
  the sampler of test-o18-getct-upper-stale-runA/B."
- "The readings run in the order of the table": RIG-FIX:248-281.
- "`cogstop(KEEPER_COG)` stops the keeper, and the positive control is read in cog 6 after
  wrap 3": RIG-FIX:274, :279-280.

## 5. The drop-in block (section *A proven workaround*)

| Item | Source |
|---|---|
| Block | RIG-FIX:200-211, the 12 lines between the markers RIG-FIX:199 `' ---- BEGIN DROP-IN ----` and RIG-FIX:212 `' ---- END DROP-IN ----`; in the reader's copy ARCHIVE-WKR:115-126 (markers :114, :127) |
| Byte identity | pre-#360-wording: chapter fence lines 75-86 compared line for line with RIG-FIX:200-211 by `awk` (IDENTICAL 12 lines). Post-#360 wording: chapter fence lines 79-90 equal ARCHIVE-WKR:115-126 (`verify-example-corpus-identity.py`, GREEN); they differ from RIG-FIX:200-211 only in the two block labels, `E3 Fix:` (RIG-FIX:200, 203) now `E3 Workaround:` (comments; the code lines are identical) |
| Widths | RIG-FIX:200-211 widths 34, 69, 0, 35, 19, 75, 0, 10, 63, 2, 0, 75; the printed ARCHIVE-WKR:115-126 widths 41, 69, 0, 42, 19, 75, 0, 10, 63, 2, 0, 75 (all ≤ 76) |
| ASCII | `grep -n -P "\t\|[^\x00-\x7F]"` on RIG-FIX returned no line: no tab, no non-ASCII |
| Encoding of the keeper | RIG-FIX:111-112 `keeper   jmp #keeper     $FD9FFFFC ... A = -4 (one instruction back): jumps to itself` (read from the pnut-ts listing by the rig's author; not re-compiled here) |
| Proving run | LOG-FIX, 2026-09-26, run once; verdict re-derived from the raw pair lines (§9), CONFIRMED |

What the chapter says about the block, and where it comes from:

| Chapter text | Source |
|---|---|
| *What any workaround must do*: "a cog of 4-7 must be running at every wrap of the lower long, from the first wrap on, so that the cogs 4-7 group's copy of the upper long advances with the counter" | LEDGER:941-944 (group rule); failure when unmet: LOG-A2:65 (D=1), :185 (D=2); met: Run B (§3.2), LOG-FIX (§9); front matter summary table |
| guarantee: "Started by the first line of `main()` and never stopped, the keeper keeps a cog of 4-7 running through every wrap ..., so a cog your program starts in 4-7 at any later time reads the same upper long as cog 0: this is a one-time startup workaround." | RIG-FIX:27-30 ("Guarantee under test"), decided CONFIRMED by LOG-FIX (§9). |
| *Other ways*: "A cog your program already starts in 4-7 before the first wrap and never stops meets it as well" | the condition itself; Run B: cog 4 started at program start (LOG-B2:15, lower long `$00DB_96FF`), kept running, D=0 before wrap 1 and after wraps 1 and 2 (§3.2) |
| *Other ways*: Run B's kept-running cog was the reading cog; the workaround program's was a separate keeper; "Both arrangements met the condition, and both read current." | §3.2 (Run B); §9 (LOG-FIX: F1, F1L, F2, F2L all D=0) |
| *Other ways*: "The cogs tested were executing code at every wrap: a polling loop in Run B, a jump to itself for the keeper." | RIG-B:537-547 (sampler polling loop, same code as RIG-A:540-550); RIG-FIX:205 (keeper) |
| cost: "A program that already needs all eight cogs cannot add the keeper, but meets the condition if one of its own cogs of 4-7 is running from before the first wrap and is never stopped." | follows from the condition; evidence as the *Other ways* rows (Run B, §3.2); not separately tested |
| limit, added: "the same holds for a cog of your own that you rely on in place of the keeper" (a cog held in a wait instruction at a wrap is untested) | RIG-FIX:24-26; no rig parked a cog of 4-7 in a wait instruction across a wrap (RIG-A, RIG-B and RIG-FIX samplers poll) |
| "Spin2 runs the first `PUB` method of the top-level object at start" | KB-MD:61 `description: "First PUB method in top file is program entry"`; KB-MD:23 |
| "a cog of 4-7 that nothing else in your program starts or stops" | RIG-FIX:201 comment `a cog of 4-7 the program never uses`; KB-COGINIT:21 `0-7: Start specific cog (will stop if running)` (a later `coginit` into that cog would replace the keeper) |
| "The keeper executes a jump to itself and nothing else." | RIG-FIX:205; RIG-FIX:24-25 "The keeper is a busy loop (a JMP to itself)" |
| "Cogs 0-3 are kept current by cog 0 ... for as long as it or another cog of 0-3 keeps running; the cogs 0-3 group was not tested with every one of its cogs stopped" | group rule LEDGER:941-943; cog 1 D=0 in every reading of Run A and Run B (§3.1, §3.2); the untested case as in v0.1.0 |
| limit: keeper only as a jump to itself; `WAITX` not tested | RIG-FIX:24-26 "Whether a cog parked in a WAITx instruction also counts as running is NOT tested here and NOT claimed." |
| limit: only cog 7 as keeper; readers in cogs 4, 5, 6, each started after one or two wraps and stopped after its reading | RIG-FIX:36-43, :59-79, :286-303 |
| limit: keeper alone through two wraps, then stopped as a positive control | RIG-FIX:64-73, :273-281 |
| limit: 200 MHz, RAM download with a reset | RIG-FIX:131; RIG-FIX:121-123 |

The v0.1.0 workaround snippet and its compile harness (`M/verification/e3-harness-keep-group-running.spin2`)
are retired from the chapter: the printed workaround is now the RIG-FIX block. The harness file is
left in place, untouched.

## 6. The workaround's test program (section *How it was proven on P2 hardware*, the workaround)

| Chapter text | Source |
|---|---|
| "carries that block byte for byte, with the same sampler, pair protocol, D and pair rules as Run A and Run B, at 200 MHz, with the debugger confined to cog 0" | §5; RIG-FIX:45-57, :592-607, :131, :132 |
| "The keeper starts in cog 7 at the first line of `main()`." | RIG-FIX:211 |
| "Cog 1 samples the cogs 0-3 group from start to end." | RIG-FIX:38, :243-246 |
| cogs 4, 5, 6 each started just before one reading and stopped just after | RIG-FIX:39-40, :75-77, :286-303 |
| "Every reading of cogs 4-7 is paired with a reading of cog 1." | RIG-FIX:74, :250-281 |
| Table row upper 0 early, cog 4, D 0 (control) | RIG-FIX:63, :249-250, :186 `P_CTRL = 0`, :93-94 (C6), :326 |
| Table rows upper 1 early cog 5 / late cog 6: 0 with the keeper, 1 without | RIG-FIX:65-66, :255-260, :184 `P_FIX = 0` (ARCHIVE-WKR:98 `P_WKR = 0`) |
| Table rows upper 2 early cog 4 / late cog 5: 0 with the keeper, 1 or 2 without | RIG-FIX:68-69, :265-270 |
| Table row upper 3 early cog 6, keeper stopped, D 1 (positive control) | RIG-FIX:70-73, :274-280, :185 `P_POS = 1`, :95-97 (C7), :328-330 |
| "At start the running cogs must be cog 0 and the keeper only." | RIG-FIX:91 (C4), :163 `M_BOOT`, :238-240 |
| "The keeper must be seen running on every poll up to the positive control, and stopped after it." | RIG-FIX:87-90 (C3), :164-165 `M_KEEP` / `M_NOKEEP`, :249-279 |
| positive-control rationale ("cannot come from a test that is blind to it") | RIG-FIX:95-97 |
| "Cog 6 reads both with the keeper running and ... stopped: the same cog and the same code, with only the keeper changed." | RIG-FIX:77-79 |
| verdict rules: confirmed / refuted / inconclusive / no verdict | RIG-FIX:99-107; code RIG-FIX:336-345 |
| "The verdict rule was set before the run." | RIG-FIX:99 "VERDICT (one line, fixed before the run)"; :183-186 predictions |

## 7. Mechanism (section *Why it happens*)

Paraphrased at the programmer's-model level from the study's mechanism statement; nothing
quoted, no design names or line references. Each statement against the bench:

| Chapter statement | Bench consistency |
|---|---|
| "The account below is the clean-room design study's reading of the mechanism" | attribution framing, as in E6 (`opus-master/e6-dac-mode-adc-enable.md` *Why it happens*) |
| each group reads its own copy | LEDGER:941; cog 1 D=0 while cog 4 D=1 at the same moment (LOG-A2:65, :76) |
| lower half refreshed whenever a cog of the group runs; newly started cog reads a current lower long | bracket held in every pair incl. A1a just after start (LOG-A2:55-64 `lo-bracket=1`) |
| upper half refreshed only at a wrap while a group cog runs; not by a cog start | A1a D=1 just after start (LOG-A2:65); A4a D=2 just after restart (LOG-A2:185) |
| takes the counter's value at the next wrap, closing in one step | A2 D=0 after one wrap from D=1 (LOG-A2:128); smp hi 0 -> 2 (LOG-A2:100, :118) |
| copies start from zero at reset; only cog 0 runs at reset | LOG-A2:22 `running cogs=%00000001`; A1a smp hi `$0000_0000` after missing wrap 1 (LOG-A2:55) |
| "A keeper cog in 4-7 that runs from before the first wrap gives that group a running cog at every wrap, so its upper long advances with the counter's" | consequence of the group rule (LEDGER:941-944); consistent with Run B (§3.2) and with the workaround run, a separate keeper (LOG-FIX, §9). |
| "Running" = between start and stop, as COGCHK reports | the rig's running-cog mask is built from `cogchk()` (RIG-A:477-488; RIG-FIX:564-575) |
| "By the study's reading, what a running cog is executing does not enter into it." | study-level statement, NOT bench-tested; the next sentence says so |
| "The tests kept their cogs in a polling loop or, for the keeper, a jump to itself, and did not try ... `WAITX`" | samplers poll: RIG-A:540-550, RIG-FIX:597-607; keeper: RIG-FIX:205; RIG-FIX:24-26 |

## 8. Status table

| Field | Source |
|---|---|
| Published by Parallax: No | LEDGER:940 "(new; not in any vendor source)"; SD KNOWN BUGS 197-227 carries no counter item (§1) |
| Found by | brief ERRATA-CHAPTER-BRIEF.md "Found by" rule for E3-E6; LEDGER:886-889 |
| Confirmed on silicon: Yes — 2026-09-24, on a P2 board at 200 MHz, run twice | LEDGER:892-894 |
| Workaround proven on silicon: Yes — 2026-09-26, on a P2 board at 200 MHz, run once; a one-time startup workaround | LOG-FIX:1 and :14 (date, one download), LOG-FIX:226 and the re-derivation in §9 (CONFIRMED); 200 MHz RIG-FIX:131; kind: creation-guide §5 |
| Test program | APP-A:13-15 (all three names; the workaround program's reader name `e3-workaround-keeper-cog-test.spin2`); RIG-FIX:3 (its as-run name) |

## 9. The workaround run (LOG-FIX): raw lines, re-derived verdict, chapter mapping

Run once, 2026-09-26, RAM download with reset (LOG-FIX:14-17), 200 MHz (RIG-FIX:131). One
build: the `.bin` downloaded (LOG-FIX:14, 13008 bytes) matches the size of the `.bin` beside
RIG-FIX. The four PENDING-BENCH placeholders of the first reshape were filled from these lines
and removed.

Raw lines, LOG-FIX, verbatim (the per-pair lines 25-34, 36-45, 65-74, 76-85, 101-110, 112-121,
128-137, 139-148, 164-173, 175-184, 191-200, 202-211 are in the log; two are quoted here):

```
14:[2026-09-26T01:55:46.948] [SYSTEM] [DOWNLOAD TO RAM] File: e3-fix-keeper-cog-test.bin | Size: 13008 bytes | Modified: 2026-09-26T07:55:15.272Z
22:[2026-09-26T01:55:47.740] Cog0  boot: cog0 CT=$0000_0000_$00BF_2806 running cogs=%10000001
23:[2026-09-26T01:55:47.755] Cog0    alive CT=$0000_0000_$00DE_D98E wraps-seen=0 running=%10000011
35:[2026-09-26T01:55:49.037] Cog0  K0  cog4 hi=0 => D=0 status=0 valid pairs=10 tries=10
46:[2026-09-26T01:55:49.043] Cog0  C0  cog1 hi=0 => D=0 status=0 valid pairs=10 tries=10
63:[2026-09-26T01:56:09.157] Cog0    alive CT=$0000_0001_$0000_136E wraps-seen=1 running=%10000011
75:[2026-09-26T01:56:10.511] Cog0  F1  cog5 hi=1 => D=0 status=0 valid pairs=10 tries=10
86:[2026-09-26T01:56:10.518] Cog0  C1  cog1 hi=1 => D=0 status=0 valid pairs=10 tries=10
111:[2026-09-26T01:56:27.960] Cog0  F1L cog6 hi=1 late => D=0 status=0 valid pairs=10 tries=10
122:[2026-09-26T01:56:27.967] Cog0  C1L cog1 hi=1 late => D=0 status=0 valid pairs=10 tries=10
126:[2026-09-26T01:56:30.633] Cog0    alive CT=$0000_0002_$0000_01A6 wraps-seen=2 running=%10000011
138:[2026-09-26T01:56:31.986] Cog0  F2  cog4 hi=2 => D=0 status=0 valid pairs=10 tries=10
149:[2026-09-26T01:56:31.993] Cog0  C2  cog1 hi=2 => D=0 status=0 valid pairs=10 tries=10
174:[2026-09-26T01:56:49.435] Cog0  F2L cog5 hi=2 late => D=0 status=0 valid pairs=10 tries=10
185:[2026-09-26T01:56:49.452] Cog0  C2L cog1 hi=2 late => D=0 status=0 valid pairs=10 tries=10
186:[2026-09-26T01:56:49.452] Cog0  --- keeper STOPPED at CT=$0000_0002_$E088_2186; waiting for CT hi=3 with cogs 4-7 idle (~3 s) ---
187:[2026-09-26T01:56:49.468] Cog0    alive CT=$0000_0002_$E089_CEFE wraps-seen=2 running=%00000011
189:[2026-09-26T01:56:52.107] Cog0    alive CT=$0000_0003_$0000_0ACE wraps-seen=3 running=%00000011
191:[2026-09-26T01:56:53.445] Cog0  P3  cog6 hi=3 p1 ref=$0000_0003_$101F_D8F8 smp=$0000_0002_$101F_D913 ref2=$0000_0003_$101F_D965 D=1 lo-bracket=1
201:[2026-09-26T01:56:53.461] Cog0  P3  cog6 hi=3 => D=1 status=0 valid pairs=10 tries=10
212:[2026-09-26T01:56:53.468] Cog0  C3  cog1 hi=3 => D=0 status=0 valid pairs=10 tries=10
214:[2026-09-26T01:56:53.469] Cog0  slot 0: D=0 st=0 lo-bracket-fails=0
215:[2026-09-26T01:56:53.469] Cog0  slot 1: D=0 st=0 lo-bracket-fails=0
216:[2026-09-26T01:56:53.469] Cog0  slot 2: D=0 st=0 lo-bracket-fails=0
217:[2026-09-26T01:56:53.469] Cog0  slot 3: D=0 st=0 lo-bracket-fails=0
218:[2026-09-26T01:56:53.469] Cog0  slot 4: D=0 st=0 lo-bracket-fails=0
219:[2026-09-26T01:56:53.470] Cog0  slot 5: D=0 st=0 lo-bracket-fails=0
220:[2026-09-26T01:56:53.470] Cog0  slot 6: D=0 st=0 lo-bracket-fails=0
221:[2026-09-26T01:56:53.470] Cog0  slot 7: D=0 st=0 lo-bracket-fails=0
222:[2026-09-26T01:56:53.470] Cog0  slot 8: D=0 st=0 lo-bracket-fails=0
223:[2026-09-26T01:56:53.471] Cog0  slot 9: D=0 st=0 lo-bracket-fails=0
224:[2026-09-26T01:56:53.471] Cog0  slot 10: D=1 st=0 lo-bracket-fails=0
225:[2026-09-26T01:56:53.471] Cog0  slot 11: D=0 st=0 lo-bracket-fails=0
226:[2026-09-26T01:56:53.472] Cog0  VERDICT: CONFIRMED - keeper running: cogs 4/5/6 started after 1 and 2 wraps read D=0 in every reading; keeper stopped: D=1 (positive control); cog 1 D=0 throughout
```

Slot map (RIG-FIX:176-177): 0=K0, 1=C0, 2=F1, 3=C1, 4=F1L, 5=C1L, 6=F2, 7=C2, 8=F2L, 9=C2L,
10=P3, 11=C3.

**Verdict re-derived from the raw pair lines, not from LOG-FIX:226.** An `awk` pass parsed
every `p<n> ref=... smp=... ref2=...` line independently (hex decode of all six longs) and
recomputed D = ref.hi - smp.hi, validity (ref.hi == ref2.hi; all three lower longs in
[`$1000_0000`, `$F000_0000`]) and the bracket (ref.lo < smp.lo < ref2.lo, unsigned). Result, per
reading: 10 pairs, 0 invalid, 0 bracket failures, 0 disagreements with the printed D, and a
single D value:

| Reading | Pair lines | Cog 0 upper | Recomputed D (all 10 pairs) |
|---|---|---|---|
| K0 cog 4 | 25-34 | 0 | 0 |
| C0 cog 1 | 36-45 | 0 | 0 |
| F1 cog 5 | 65-74 | 1 | 0 |
| C1 cog 1 | 76-85 | 1 | 0 |
| F1L cog 6 late | 101-110 | 1 | 0 |
| C1L cog 1 late | 112-121 | 1 | 0 |
| F2 cog 4 | 128-137 | 2 | 0 |
| C2 cog 1 | 139-148 | 2 | 0 |
| F2L cog 5 late | 164-173 | 2 | 0 |
| C2L cog 1 late | 175-184 | 2 | 0 |
| P3 cog 6 | 191-200 | 3 | 1 |
| C3 cog 1 | 202-211 | 3 | 0 |

Controls, each from the raw lines:

- C1 (cog 1 D = 0, status ok, every control reading): C0, C1, C1L, C2, C2L, C3 above, all D=0
  with 10 valid pairs and no bracket failure.
- C2 (cog 0 upper long = wraps watched): a second `awk` pass over all 55 `alive` lines found
  the CT upper long equal to `wraps-seen` on every one.
- C3 (running-cog set): the same pass found `running=%10000011` (cogs 0, 1, 7) on every `alive`
  line from LOG-FIX:23 through :163, and `running=%00000011` (cogs 0, 1) on every line from
  LOG-FIX:187 on, after the keeper stop at LOG-FIX:186. The between-reading mask checks
  print only on failure.
- C4 (boot): LOG-FIX:22, CT upper long `$0000_0000`, `running cogs=%10000001` (cogs 0 and 7).
- C5 (every request answered): `grep -c -E "RIG FAIL|HALTED|TIMEOUT|DISCARD"` on LOG-FIX = 0;
  every reading `tries=10` for 10 valid pairs.
- C6 (K0 D = 0): recomputed 0.
- C7 (positive control P3 D = 1): recomputed 1; sampler upper `$0000_0002` beside cog 0's
  `$0000_0003` in every P3 pair (LOG-FIX:191-200), with wrap 3 passing while cogs 4-7 were
  idle (LOG-FIX:189 `running=%00000011`).
- Workaround arms F1, F1L, F2, F2L: all D = 0, status ok. By RIG-FIX:99-107 this is **CONFIRMED**.

Chapter values taken from LOG-FIX:

| Chapter text | Line(s) |
|---|---|
| *A proven workaround*: "confirmed on silicon on 2026-09-26, on a P2 board at 200 MHz, run once" | LOG-FIX:1, :14 (one download); RIG-FIX:131 (200 MHz) |
| *A proven workaround*: "cogs 5 and 6 started after one wrap and cogs 4 and 5 started after two each read the same upper long as cog 0 in all ten pairs" | F1 cog 5 LOG-FIX:65-75; F1L cog 6 :101-111; F2 cog 4 :128-138; F2L cog 5 :164-174 |
| *A proven workaround*: "with the keeper stopped, cog 6 read one behind" | LOG-FIX:191-201 |
| *A proven workaround* limits: "The test ran once" | LOG-FIX: a single download (LOG-FIX:14) and a single session end (LOG-FIX:227) |
| workaround table, Sampler D column: 0, 0, 0, 0, 0, **1** | LOG-FIX:35, :75, :111, :138, :174, :201 (recomputed above) |
| workaround table, Cog 1 D column: 0 in every row | LOG-FIX:46, :86, :122, :149, :185, :212 |
| "In every reading all ten pairs agreed on D, and the lower-long check held in every pair." | re-derivation above; LOG-FIX:214-225 `st=0 lo-bracket-fails=0` in every slot |
| Result: "ran once, on 2026-09-26, on a P2 board at 200 MHz, downloaded to RAM with a reset" | LOG-FIX:14-17; RIG-FIX:131; reset shown by LOG-FIX:22 (upper long 0 at boot, C4) |
| "At start the upper long read 0 and the running cogs were cog 0 and the keeper in cog 7" | LOG-FIX:22 |
| "Every control passed, and no `RIG FAIL` line was printed" | controls above; `grep -c` = 0 |
| "showed the keeper on every poll until it was stopped, with cog 0's counter at `$0000_0002_$E088_2186`, and did not show it on any poll after" | LOG-FIX:23-163 `%10000011`; :186; :187-190 `%00000011` |
| "the four readings taken after a wrap gave D = 0" | LOG-FIX:75, :111, :138, :174 |
| "cog 6 read an upper long of `$0000_0002` beside cog 0's `$0000_0003`: D = 1, the erratum as in Run A" | LOG-FIX:191 (first P3 pair; all ten alike, :191-200), :201; Run A comparison LOG-A2:65 (D=1 after one missed wrap) |
| "The verdict line read `CONFIRMED`." | LOG-FIX:226 (and re-derived above) |
| Status "Workaround proven on silicon: Yes — 2026-09-26, on a P2 board at 200 MHz, run once; a one-time startup workaround: a keeper cog in cog 7 started by the first line of `main()`" | §8 row; RIG-FIX:201, :211 |
| run length: the workaround's test program "about 67 s after reset" (*The test program*; measured 66.7 s, row above) | RIG-FIX:117-118 (design figure); consistent with LOG-FIX:17 download end 01:55:47.715 to :227 end 01:56:53.488 |

---

## 10. The stale window (2026-09-27, task «#361»): three more runs, and the chapter reshaped around them

Stephen, 2026-09-27: the chapter must speak to the erratum as a bounded window ("a transient
where counts can be off"), and show that once a cog starts in the group it reads correctly again
after one wrap of the lower long. Three tests decided what the chapter may claim; the chapter
was then reshaped (CAUTION box, *What the P2 does*, *What your program sees*, *A proven
workaround*, *Why it happens*, a new *The stale window* part of *How it was proven*, *The test
program*, *Status*). Every fact kept from the earlier shape keeps its mapping above; this section
maps what was added or changed.

| Tag | File |
|---|---|
| SPIN2 | `engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt` (Parallax Spin2 Language Documentation v55); checked against `Parallax Spin2 Documentation v55.docx` in the same folder |
| INTERP | `engineering/document-production/manuals/p2-xbyte-programming-guide/REF-NO-COMMIT/pnut-ts-parts/Spin2_interpreter.spin2` (Spin2 interpreter v55, 2026.05.07) — mechanism only, never quoted |
| RIG-W / LOG-W | `M/audit/verification-tests/e3-waiting-keeper-test.spin2` / `logs/debug_260927-162313.log` (downloaded 13,291 bytes, LOG-W:14) |
| RIG-G / LOG-G | `M/audit/verification-tests/e3-group0-idle-band-test.spin2` / `logs/debug_260927-162507.log` (13,497 bytes, LOG-G:14) |
| RIG-8 / LOG-8 | `M/audit/verification-tests/e3-band-closes-in-one-wrap-test.spin2` / `logs/debug_260927-162927.log` (14,906 bytes, LOG-8:6) |
| ARCHIVE-W / -G / -8 | `M/examples-library/e3-workaround-waiting-cog-test.spin2` / `e3-cogs-0-3-stale-window-test.spin2` / `e3-stale-window-closes-test.spin2` — the rigs with the development header replaced by the generated one. RIG-W and RIG-G had header-comment edits after the run; their as-run sources, rebuilt, are byte-identical to the downloaded builds. Then the `spin2-style` gate (armed rules) required two changes: ARCHIVE-8's `spin_sampler` parameter renamed `pSpinMailbox` (§2.5, its `@param` text had to differ from `reading()`'s) — ARCHIVE-8 and ARCHIVE-G still compile (`pnut-ts -d` 1.55.8) byte-identical to their rigs (`cmp`); ARCHIVE-W's `verdict()` early `return` became an `else` (§5.2) — same size (13,291 bytes); the keeper + sampler image (128 bytes from offset 11,823) identical and at the same offset; 723 bytes differ, in 29 runs — single bytes every 4 bytes in the table just before the image (offsets 11,775–11,811) and runs from 13,084 to the end — i.e. outside the measuring image. APP-A says so. **ARCHIVE-W re-run** 2026-09-27 (Stephen), log `M/audit/verification-tests/logs-archive/debug_260927-172602.log` (downloaded 13,291 bytes = a fresh compile of the committed file, `cmp`): all 8 readings re-derived from the pair lines match LOG-W exactly (K0 0, C0 0, E1 0, C1 0, X2 0, C2 0, P3 1, C3 0; 10 of 10 valid pairs, bracket held), 0 `RIG FAIL`/discard/timeout, the same count of polls per running-cog mask, both verdict lines `CONFIRMED` — APP-A's "run again … matched" |
| LEDGER | EF-078 (RIG-W), EF-079 (RIG-G), EF-080 (RIG-8) |

Every verdict was re-derived from the raw pair lines (script over all `p<n> ref=… smp=… ref2=…`
lines: D recomputed from the hex, bracket recomputed unsigned, window checked): all 40 counter
readings (LOG-W 8, LOG-G 16, LOG-8 16) have 10 valid pairs with one D and the bracket holding;
the three Spin2 readings (LOG-8 GBE, GBL, GXE) have 10 pairs each in one class, reclassified from
the printed ms/s values. `grep -c "RIG FAIL\|DISCARD\|TIMEOUT"` = 0 on all three logs.

| Chapter text | Source |
|---|---|
| CAUTION *Expected*: `GETMS()`/`GETSEC()` return the time since boot from that counter | SPIN2:552-553 |
| CAUTION *Actual*: "all three return a time behind by 2^32^ clocks (21.47 s at 200 MHz) for each wrap missed, until that group runs through its next wrap" | `GETCT WC`: LOG-A2 (§3.1), LOG-G:84-142, LOG-8:170-239; `GETMS`/`GETSEC`: LOG-8:203, :261 (SHORT by 171,798-9 ms = 8 x 21,474.8 ms); closes: LOG-A2 (§3.1 A2), LOG-G:169-227, LOG-8:277-346, :310 |
| Opening: "in a cog of cogs 4-7 … more than 2^32^ clocks after reset" / "either group" | as §0; either group: LOG-G (cogs 0-3) |
| *Documented*: the two Spin2 quotations | SPIN2:552 (`GETSEC()`), :553 (`GETMS()`), description column only; the `.docx` text matches word for word ("Get seconds since booting, uses 64-bit system counter and CLKFREQ, rolls over every 136 years."; "… rolls over every 49.7 days.") |
| *Documented*: "Neither document qualifies these values by cog number" | SD as §1; SPIN2:552-553 (no condition) |
| *What the P2 does*: lower long current "in every pair the tests took" | §3.1-3.2, LOG-FIX; LOG-W/-G/-8 bracket held in all 400 counter pairs (re-derivation above) |
| "A cog held in `WAITATN` or in `WAITX` at the wrap counts as running" | LOG-W:75 (E1 D=0, `WAITATN` keeper alone, mask `%10000011` on its polls), :115 (X2 D=0, `WAITX` keeper alone, `%01000011`); positive control :155 (P3 D=1, `%00000011`) |
| "Cogs 4 and 7 … missed eight wraps, read 8 behind" | LOG-8:170, :181, :228, :239 (D=8); mask `%00000011` on all 131 polls before, then `%10110011` |
| "cogs 4 and 7, 8 behind, did the same, and so did cogs 1 and 3, 2 behind" | LOG-8:277, :288, :335, :346 (D=0); LOG-G:169, :180, :216, :227 (D=0) |
| "Both tests that read again one wrap later found the group still current" | LOG-G:254, :265 (hi=4, D=0); LOG-8:373, :384 (hi=10, D=0) |
| cogs 0-3 paragraph: "cogs 1 and 3, started after their group had missed two wraps, read 2 behind" | LOG-G:84, :95, :131, :142 (D=2); no cog of 0-3 on any poll before: LOG-G `alive` lines `%00110000` (35) until the start, then `%00111010` (36); cog 0 stops LOG-G:22 |
| "confirmed … for lags of one, two and eight missed wraps, in cogs 4-7 (cogs 4 and 7 sampled) and in cogs 0-3 (cogs 1 and 3 sampled)" | LOG-A2 (1, 2), LOG-G (2), LOG-8 (8); samplers RIG-8 `SMP_COG_A = 4`, `SMP_COG_B = 7`; RIG-G `SMP_COG_A = 1`, `SMP_COG_B = 3` |
| `GETMS()`/`GETSEC()` table: cog 0 190,617 / 190, cog 5 18,819 / 18 | LOG-8:260 (GBL p10) |
| table: after the window closed, cog 0 and cog 5 both 194,637 / 194 | LOG-8:300 (GXE p1) |
| "After eight missed wraps, 171,798 ms at 200 MHz" | LOG-8:14 (`ms 171_798..171_799`), computed by `MULDIV64` from `clkfreq` in the rig |
| *Closes*: cog 4 `$0000_0000_$E013_BB32` → `$0000_0009_$1001_546A` | LOG-8 B4L p10 (the last pair before wrap 9) and X4E p1; step line LOG-8:413 |
| "all ten pairs of each reading agreed, early and late" | re-derivation above; LOG-A2 as §3.1 |
| "Only `GETCT`, `GETMS()` and `GETSEC()` were exercised" | the three rigs and RIG-A/-B/-FIX read nothing else |
| *Workaround* condition and "waiting it out" | LOG-8:277-384, LOG-G:169-265: every reading after the one closing wrap read D=0 / CURRENT |
| "a keeper held in `WAITATN`, and one held in `WAITX`, each kept cogs 4-7 current through a wrap" | LOG-W:75, :115 |
| "The P2 Documentation does not say which cog a free-cog start chooses" | SD: `grep -n -i "free cog\|lowest\|first available"` — :758-759 and :814-822 speak of "a free cog" with no order; SPIN2: no order stated (checked 2026-09-27) |
| "check the cog number the start returns" | KB-COGINIT and `pasm2/coginit.yaml` (authoring aid, not cited): D receives the launched cog's ID |
| Limits: "Spin2's `WAITMS()` and `WAITUS()` are not a wait instruction but a loop that reads the counter" | INTERP `pwct` (`getct w` / `cmpm w,x wc` / `if_c jmp #pwct`), reached from `waitus_`/`waitms_` |
| Limits: "cogs 7 and 6 held the waits" | RIG-W `KEEP_COG_E = 7`, `KEEP_COG_X = 6` |
| *Why it happens*: "`GETMS()` and `GETSEC()` are computed by the Spin2 interpreter from the calling cog's own `GETCT WC` and `GETCT`" | INTERP `getms_` (`getct z wc` / `getct y`, then `qdiv` by `clkfreq`); measured LOG-8:203, :261, :310 |
| *Why*: "What a running cog is executing does not enter into it" | the study's reading, now measured for two waits: LOG-W:75, :115 |
| *Proven*, stale-window part: "In all 40 of their counter readings … the three Spin2 readings" | re-derivation above |
| waiting table rows | LOG-W:35 (hi 0, D 0), :46 (cog 1); :75, :86; :115, :126; :155 (**1**), :166 |
| `WAITX` count "2 + D = 4,294,967,282 clocks, 14 short of 2^32^" | RIG-W `waitx ##$FFFF_FFF0` (word `$FD67E01F` + AUGD, decoded from the `.bin`); `WAITX` = 2 + D clocks (`pasm2/waitx.yaml`, authoring aid) |
| "started just after the lower long passed `$1000_0000`" | RIG-W: keeper B started right after the E1 and C1 readings, taken at `wait_until(HI_E1, LOWIN, …)`; LOG-W:65 E1 pairs at `$101F_Dxxx` |
| cogs 0-3 table rows | LOG-G:84/95/106, :131/142/153, :169/180/191, :216/227/238, :254/265/276 |
| eight-wrap table rows | LOG-8:170/181/192/203, :228/239/250/261, :277/288/299/310, :335/346/357, :373/384/395 |
| "Cog 4's own upper long … 0 in the last pair before wrap 9 and 9 in the first pair after it" | LOG-8:413 (`0 -> 9 step +9`), re-derived from the B4L/X4E pair lines |
| "Every short Spin2 pair was behind by 171,798 or 171,799 ms and by 172 s" | re-derivation: GBE and GBL offMs {171,798; 171,799}, offS {172} |
| *The test program*: the two keeper loops excerpt | ARCHIVE-W:514-523 (verbatim, ≤ 76 columns; checked by script) |
| "`DEBUG_COGS` names cogs 0 and 4" | ARCHIVE-G:24 |
| run lengths "about 66 s … 87 s … 216 s" | LOG-W:18 → :177 (65.8 s); LOG-G:17 → :294 (87.2 s); LOG-8:9 → :416 (216.1 s) |
| Status: "2026-09-27, run once each" | one download per log (LOG-W:14, LOG-G:14, LOG-8:6) |
| Status *Affects* "measured on cogs 4-7 and on cogs 0-3" | LOG-A2, LOG-8 (4-7); LOG-G (0-3) |
