# E3 verification sidecar: Chapter 3, GETCT Returns a Stale Upper Long

Chapter: `opus-master/e3-getct-stale-upper-long.md`. Every number, quotation and code
excerpt in the chapter, mapped to the file and line it came from. Paths are relative to the
repository root unless marked `M/` (= `engineering/document-production/manuals/p2-errata/`).

Abbreviations used below:

| Tag | File |
|---|---|
| LEDGER | `engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md` |
| SD | `engineering/ingestion/sources/silicon-doc/p2-documentation.txt` |
| RIG-A | `M/audit/verification-tests/test-o18-getct-upper-stale-runA.spin2` (byte-identical to `hardware-verification/campaigns/2026-09-p2-errata-predictions/tests/` copy, checked with `cmp`) |
| RIG-B | `M/audit/verification-tests/test-o18-getct-upper-stale-runB.spin2` (byte-identical to the campaign copy, checked with `cmp`) |
| LOG-A2 | `M/audit/verification-tests/logs/debug_260924-231939.log` (Run A, second build; .bin 13037 bytes = the rig on disk) |
| LOG-A1 | `M/audit/verification-tests/logs-orig/debug_260924-204946.log` (Run A, first build) |
| LOG-B2 | `M/audit/verification-tests/logs/debug_260924-231846.log` (Run B, second build; .bin 12550 bytes = the rig on disk) |
| LOG-B1 | `M/audit/verification-tests/logs-orig/debug_260924-204835.log` (Run B, first build) |
| HARNESS | `M/audit/verification/e3-harness-keep-group-running.spin2` |

Numbers quoted in the chapter's reader text are taken from the second-build logs (LOG-A2,
LOG-B2), the build that matches the rig files on disk. The first-build logs were checked for
the same D values and verdicts.

---

## 1. Quotations of Parallax documentation (section *What the design says*)

| Chapter text | Source |
|---|---|
| "in its list of what the hub provides the cogs" | SD:414 `The hub provides the cogs with:` |
| > 64-bit free-running counter which increments every clock, cleared on reset | SD:436, verbatim |
| "Its list of the improvements made to the chip" | SD:62 `The following improvements were made to the chip:` |
| > System counter extended to 64 bits. GETCT WC retrieves upper 32-bits. | SD:81, verbatim |
| > Event 1 = CT passed CT1 (CT is the lower 32-bits of the free-running 64-bit global counter) | SD:5131, verbatim |
| "It does not qualify the value `GETCT WC` returns by cog number, or by which other cogs are running." | Absence claim. Every `GETCT` occurrence in SD (`grep -n -i getct`): 81, 5408, 5411, 5674, 5715, 11350. None qualifies the read by cog or by cog activity. SD:5674 lists `GETCT+WC` among instructions that hold off an interrupt branch; unrelated. |

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
| 2^32^ clocks per wrap; 21.47 s at 200 MHz | opening para; *What the part does*; *The symptom*; *The workaround* | RIG-A:109 `CLOCK / RUN TIME: _clkfreq = 200_000_000 -> 2^32 clocks = 21.47 s per` / RIG-A:110 `wrap.`; RIG-B:112-113 same. LEDGER:945 gives the rounded "21.5 s at 200 MHz"; the chapter uses the rig's 21.47 s. |
| 200 MHz | throughout; Status | RIG-A:123 `_clkfreq    = 200_000_000`; LEDGER:892 "bare P2 board, 200 MHz" |
| 2026-09-24, run twice | Status | LEDGER:893 "RAM download with reset, 2026-09-24 (Stephen). **Run twice**, from two builds"; log headers LOG-A2:1, LOG-B2:1, LOG-A1, LOG-B1 (all 2026-09-24) |
| debugger confined to cog 0 | *How it was proven* | RIG-A:124 / RIG-B:127 `DEBUG_COGS  = %0000_0001`; LEDGER:890 |
| "as first written, and with its comments and layout conformed ... measuring code unchanged" | *How it was proven* | LEDGER:893-894 "(as authored, then style-conformed with identical measuring engines): every measured value matched" |
| "Every D value and every verdict matched between the two builds" | *How it was proven* | LOG-A1:234-245 vs LOG-A2:234-245 (slot 0..10 D and st identical; both VERDICT CONFIRMED); LOG-B1:152-160 vs LOG-B2:144-152 (slots 0..7 identical; both VERDICT CONFIRMED) |
| `$1000_0000`, `$F000_0000` (pair window) | *How it was proven* | RIG-A:126-127 `LOWIN   = $1000_0000` / `HIWIN   = $F000_0000`; RIG-A:39-40; LEDGER:948 |
| `$E000_0000` (late reading) | *How it was proven* | RIG-A:128 `LATE    = $E000_0000` |
| ten pairs per reading | *The symptom*; *How it was proven* | RIG-A:129 `NPAIRS  = 10`; every `=> D=` line in all four logs ends `valid pairs=10 tries=10` |
| 100 ms | *How it was proven* (controls) | RIG-A:79 `C5  every request answered within 100 ms (sampler alive).`; RIG-A:304 `take_pair(mb, seq, clkfreq / 10)` |
| about 105 s (Run A), about 44 s (Run B) | *The test program* | RIG-A:110-111 `Run A ends at CT hi=4, lo=$E000_0000: about 4.9 x 21.47 s` / `= ~105 s after reset (plus download).`; RIG-B:113-114 `Run B ends at CT hi=2, lo=$1000_0000:` / `about 2.06 x 21.47 s = ~44 s after reset (plus download).` |
| `pnut-ts` 1.55.8, `-d` | *The test program* | RIG-A:119 `COMPILER: pnut-ts v1.55.8,  pnut-ts -d -l test-o18-getct-upper-stale-runA.spin2`; LEDGER:893 |
| "at reset only cog 0 runs" | opening; *What the part does*; *Why* | LOG-A2:22 and LOG-B2:14 `running cogs=%00000001` at boot; LEDGER:944 |

### 3.1 Run A readings (table rows A; *What the part does*; *The symptom*)

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

### 3.2 Run B readings (table rows B; *The workaround*)

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
| "cog 4 was started ... while the lower long read `$00DB_96FF`" | LOG-B2:15 |
| Table row B hi=0: 0, 0 | LOG-B2:28, :39 |
| Table row B hi=1 early: 0, 0 | LOG-B2:68, :79 |
| Table row B hi=1 late: 0, 0 | LOG-B2:104, :115 |
| Table row B hi=2: 0, 0 | LOG-B2:131, :142 |
| cog 4 running through wraps 1 and 2 | LOG-B2:16-57, :80-120 `running=%00010011` |
| lower-long check held in every pair | LOG-B2:144-151 `lo-bracket-fails=0` |

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

### 3.3 Controls (section *How it was proven*)

| Chapter control | Source |
|---|---|
| cog 1 D = 0 every reading, else no verdict | RIG-A:67-69 (C1), :233-239, :245-246 |
| cog 0 upper long = wraps cog 0 watched, every poll | RIG-A:70-73 (C2), :416-429 |
| running-cog set polled throughout every wait; Run A no cog 4-7 before cog 4 | RIG-A:74-77 (C3), :433-454; RIG-B:78-79 |
| boot: upper long 0, only cog 0 running | RIG-A:78 (C4), :162-173 |
| every request answered within 100 ms | RIG-A:79 (C5), :304 |
| expected D fixed before the run | RIG-A:142-146 (P_A1_TRUE..P_CTRL); RIG-B `P_B_TRUE`/`P_B_FALSE`/`P_CTRL` (RIG-B:151-154) |
| No RIG FAIL fired | no `RIG FAIL` / `HALTED` line in any of the four logs |

### 3.4 Pair protocol and D (section *How it was proven*)

- Pair definition: RIG-A:31-44; cog 0 side in inline PASM2, RIG-A:382-400
  (`getct rhb wc` / `getct rlb` before `wrlong reqNum, mb`; `rdlong shi, phi` /
  `rdlong slo, plo` / `getct rha wc` / `getct rla` after the ack).
- Valid-pair rule: RIG-A:311 (`rhb <> rha or not inwin(rlb) or not inwin(slo) or not inwin(rla)` -> discard).
- D and bracket: RIG-A:314-315.
- Reading = NPAIRS agreeing pairs: RIG-A:298-333.

## 4. Code excerpts (section *The test program*)

All excerpts are contiguous, verbatim, and every line is 76 columns or fewer. Checked with an
awk pass: every fenced line in the chapter other than the workaround snippet is present
verbatim in RIG-A or RIG-B.

| # | Fence | Source lines | Content |
|---|---|---|---|
| 1 | `pasm2` | RIG-A:540-548 (identical at RIG-B:537-545) | sampler loop through `wrlong  s_lo, ptra[2]`. RIG-A:549 (`wrlong  s_req, ptra[3]`, the ack) is 80 columns and is described in prose instead. |
| 2 | `spin2` | RIG-A:314-317 (identical at RIG-B:312-315) | D and lower-long bracket |
| 3 | `spin2` | RIG-A:183-191 | Run A defect step: wait with cogs 4-7 idle, start cog 4, read cog 4 and cog 1 |
| 4 | `spin2` | RIG-B:189-193 | Run B: both samplers from program start |

Prose around the excerpts:

- "started explicitly in cog 1 and in cog 4 (`COGINIT #1` and `COGINIT #4`), with its hub
  mailbox address in `PTRA`": RIG-A:504-534 (`setq mb` / `coginit #1, pSampler`,
  `setq mb` / `coginit #4, pSampler`); RIG-A:537 `PTRA = mailbox`.
- "writes the request number back as its acknowledgment and returns to `s_loop`":
  RIG-A:549-550.
- "`cogstop(4)` at upper long 2 and a second `start_cog4` at upper long 4": RIG-A:199-210.
- "`+<` is the unsigned less-than": the Spin2 operator used at RIG-A:315, and RIG-A:42
  `LO-BRACKET = refB.lo < sampler.lo < refA.lo (unsigned)`.

## 5. Workaround snippet (section *The workaround*)

The snippet is HARNESS lines 9-21 (between the BEGIN/END markers), byte for byte (awk
membership check: every snippet line present in HARNESS). Widths all 76 columns or fewer.

Compile (pnut-ts 1.55.8, extracted from `.devcontainer/pnut-ts-linux-arm64-015508.zip` into
the session scratchpad because the brief's install path
`/home/vscode/.local/pnut/pnut-ts-linux-arm64-015508/` does not exist in this container; the
harness was copied to the scratchpad so no build output lands in M/):

```
pnut-ts -l <scratch>/e3-harness-keep-group-running.spin2
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: Wrote <scratch>/e3-harness-keep-group-running.lst
pnut-ts: Wrote <scratch>/e3-harness-keep-group-running.bin (6308 bytes)
pnut-ts: Done
```

No `debug()` in the snippet, so no `-d`. Listing check: the worker's first two longs are
`$FD70061A` (`GETCT` D=$003 with C=1, i.e. `WC`, the upper long) and `$FD60081A` (`GETCT`
D=$004, C=0, the lower long), matching the encoding in SD:11347 / getct.yaml:4
`EEEE 1101011 C00 DDDDDDDDD 000011010`. `coginit(4, ...)` starts cog 4 specifically:
`deliverables/ai/P2/language/spin2/methods/coginit.yaml`:21 "0-7: Start specific cog".

"proven on silicon": LEDGER:954-955 "**Workaround proven:** keep a cog of each group in use
running from before the first wrap." Run B evidence in 3.2.

## 6. Mechanism (section *Why it happens*)

Paraphrased at the programmer's-model level from the study's mechanism statement; nothing
quoted, no design names or line references. Each statement against the bench:

| Chapter statement | Bench consistency |
|---|---|
| each group reads its own copy | LEDGER:941; cog 1 D=0 while cog 4 D=1 at the same moment (LOG-A2:65, :76) |
| lower half refreshed whenever a cog of the group runs; newly started cog reads a current lower long | bracket held in every pair incl. A1a just after start (LOG-A2:55-64 `lo-bracket=1`) |
| upper half refreshed only at a wrap while a group cog runs; not by a cog start | A1a D=1 just after start (LOG-A2:65); A4a D=2 just after restart (LOG-A2:185) |
| takes the counter's value at the next wrap, closing in one step | A2 D=0 after one wrap from D=1 (LOG-A2:128); smp hi 0 -> 2 (LOG-A2:100, :118) |
| copies start from zero at reset; only cog 0 runs at reset | LOG-A2:22 `running cogs=%00000001`; A1a smp hi `$0000_0000` after missing wrap 1 (LOG-A2:55) |
| "Running" = between start and stop, as COGCHK reports | the rig's running-cog mask is built from `cogchk()` (RIG-A:477-488) |
| "In the design, what a running cog is executing does not enter into it" | design-level statement, NOT bench-tested; the chapter says so in the same sentence ("the test kept its cogs in a polling loop and did not try a cog held in a wait instruction such as `WAITX`") |

## 7. Status table

| Field | Source |
|---|---|
| Published by Parallax: No | LEDGER:940 "(new; not in any vendor source)"; SD KNOWN BUGS 197-227 carries no counter item |
| Found by | brief instruction for E3-E5; LEDGER:886-889 |
| Confirmed on silicon: Yes — 2026-09-24, on a P2 board at 200 MHz, run twice | LEDGER:892-894 |
| Workaround proven on silicon: Yes | LEDGER:954-955 |
| Test program | RIG-A, RIG-B filenames |
