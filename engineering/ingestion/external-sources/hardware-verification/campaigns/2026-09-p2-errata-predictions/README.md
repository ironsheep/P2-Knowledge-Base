# Campaign — 2026-09 P2 errata predictions (VO-J-007..011)

**Purpose:** decide, on real silicon, five predicted P2 silicon defects that an HDL-reading study
derived from the design source. Two had been published by the vendor; three had never been
observed on a part. The outcome decides which of them the **P2 Errata** manual carries: a
`CONFIRMED` item enters the manual and the KB; a disproved one stays out.

**Result: all five `CONFIRMED` → EF-066 … EF-070**, each on its first run, 2026-09-24 (Stephen).

| # | Test (`tests/`) | Prediction | VO | Verdict | EF |
|---|---|---|---|---|---|
| 1 | `test-o1-altx-imm-s-steals-augs.spin2` | an immediate-`#S` `ALTx` between `AUGS` and its target is itself augmented; the target still gets the augment; `AUGD` is immune | VO-J-007 | `CONFIRMED` | EF-066 |
| 2 | `test-o17-setq-altd-block-ptr-delta.spin2` | `SETQ` → `ALTD` → block `RDLONG … ptra++`: whole block moves, `PTRx` takes the plain step | VO-J-008 | `CONFIRMED` | EF-067 |
| 3 | `test-o18-getct-upper-stale-runA.spin2` + `…-runB.spin2` | `GETCT WC` in a four-cog group that missed a counter wrap reads a stale upper long | VO-J-009 | `CONFIRMED` | EF-068 |
| 4 | `test-so80-getxacc-clear-gating.spin2` | `GETXACC` clears only during a Goertzel burst; mid-burst it partitions the terms exactly | VO-J-010 | `CONFIRMED` | EF-069 |
| 5 | `test-so84-goertzel-last-term-lag.spin2` | the Goertzel accumulators lag by one clock; a burst's last term lands in the next burst | VO-J-011 | `CONFIRMED` | EF-070 |

**Second session (2026-09-25), three more tests, each run twice:**

| # | Test (`tests/`) | Question | VO | Verdict | EF |
|---|---|---|---|---|---|
| 6 | `test-rdfast-wrfast-readiness-boundary.spin2` | `RDFAST`/`WRFAST` readiness, blocking and no-wait, every hub alignment | VO-J-012 | blocking `CONFIRMED`; no-wait measured; a blocking `RDFAST` after a still-arming no-wait one skips its wait | EF-073, EF-074 |
| 7 | `test-goertzel-sinc2-iteration-count.spin2` | Chip Gracey's SINC2 iteration-count corruption | VO-J-013 | `CONFIRMED` (documented behaviour; not an erratum — EF-072 as corrected 2026-09-26) | EF-072 |
| 8 | `test-so9-dac-mode-adc-enable.spin2` | in a DAC smart mode, does `OUT` switch the ADC with `TT` = `%00` | VO-J-014 | `CONFIRMED` (it does not) | EF-071 |

**Fix tests (2026-09-26), each run once:** each runs, byte for byte, the drop-in fix that P2 Errata
v0.2.0 prints, and reproduces its erratum in the same run as a positive control (`RIG FAIL`, not a
verdict, if it cannot). Verdicts re-derived from the raw log lines.

| # | Test (`tests/`) | Fix proven | Verdict | EF |
|---|---|---|---|---|
| 9 | `e3-fix-keeper-cog-test.spin2` | E3: a keeper cog started in cog 7 as the first line of `main()` | `CONFIRMED` | EF-075 |
| 10 | `e4-e5-fix-read-sums-test.spin2` | E4 + E5: the `burst_sums` helper routine (SINC1) | `CONFIRMED` | EF-076 |
| 11 | `e7-fix-rdfast-spacing-test.spin2` | E7: `WAITX #12` after the no-wait `RDFAST` (16 clocks to the blocking one) | `CONFIRMED` | EF-077 |

**Reader copies (2026-09-26):** P2 Errata ships these 11 programs (12 files) as style-conformed
reader copies in `manuals/p2-errata/examples-library/` (the workaround tests renamed
`…-workaround-…`); measuring PASM byte-identical, cog-0 Spin2 restyled. All 12 were re-run: every
analysed value, class and verdict matched the runs above (ledger, after EF-077). One start-up
sample of the SINC2 test moved; it is an open question in the ledger.

**E3 band follow-ups (2026-09-27, each run once):** three questions the E3 chapter's rewrite
around the "band" (a bounded stale window, not a lasting state) depends on. Written by the
arbiter, not by an independent agent, then reviewed adversarially before the run by a fresh agent
per test — no blocker (`VERIFICATION-OPPORTUNITIES.md`, VO-J-015..017). Verdicts re-derived from
the raw pair lines.

| # | Test (`tests/`) | Question | VO | Verdict | EF |
|---|---|---|---|---|---|
| 12 | `e3-waiting-keeper-test.spin2` | does a cog of 4-7 held in `WAITATN` / `WAITX` at the wrap keep its group current? | VO-J-015 | `CONFIRMED` (both count) | EF-078 |
| 13 | `e3-group0-idle-band-test.spin2` | with every cog of 0-3 stopped across wraps, do cogs 0-3 show the same band, closed in one wrap? | VO-J-016 | `CONFIRMED` | EF-079 |
| 14 | `e3-band-closes-in-one-wrap-test.spin2` | from a lag of 8 wraps, does the band close at the first wrap the group runs through; do Spin2 `GETMS()`/`GETSEC()` see it? | VO-J-017 | `CONFIRMED` (both) | EF-080 |

**E3 scope (2026-09-29, each run once):** which other instructions and features the stale upper
long reaches — every one taken as affected and every one taken as not, proved either way. Written
by the arbiter, then reviewed adversarially before the run by a fresh agent per test
(`VERIFICATION-OPPORTUNITIES.md`, VO-J-018..020). Verdicts re-derived from the raw lines; the
sources here rebuild the binaries that ran byte for byte.

| # | Test (`tests/`) | Question | VO | Verdict | EF |
|---|---|---|---|---|---|
| 15 | `e3-scope-pasm2-ct-events-test.spin2` | do `WAITCTn`, `POLLCTn`, `JCTn`, `JNCTn`, the CT interrupts, the `SETQ` timeout or `WAITX` see the stale upper long, in the window or across its closing wrap; does a cog held in `WAITCT1` count as running? | VO-J-018 | `CONFIRMED` (none affected; `WAITCT1` counts) | EF-081 |
| 16 | `e3-scope-spin2-counter-methods-test.spin2` | do Spin2 `WAITCT()`, `POLLCT()`, `WAITMS()`, `WAITUS()` or `GETCT()` see it (with `GETMS()`/`GETSEC()` as the affected control)? | VO-J-019 | `CONFIRMED` (none affected; `GETMS`/`GETSEC` affected) | EF-082 |
| 17 | `e3-scope-debug-timestamp-test.spin2` (+ `e3-scope-debug-timestamp-verdict.py`) | does a `DEBUG_TIMESTAMP` stamp sent from the window carry it, from Spin2 `debug()` and PASM2 `DEBUG`? | VO-J-020 | `CONFIRMED` (affected, both) | EF-083 |

**Study briefs O29 and SO109 (2026-10-01, each run once):** two new predictions from the study
(golden source 0.1.5, both labelled user-reported). Each test was built by a fresh agent from its
brief alone, encodings re-derived on `pnut-ts` 1.55.8, then reviewed adversarially before the
run by another fresh agent — no blocker (`VERIFICATION-OPPORTUNITIES.md`, VO-J-021..022). SO109
is documented behaviour (P2 Documentation, BRK in the debugging section), measured here, not an
erratum candidate.

| # | Test (`tests/`) | Question | VO | Verdict | EF |
|---|---|---|---|---|---|
| 18 | `test-o29-rdfast-nowait-releases-hub-op.spin2` | after a no-wait `RDFAST`, is a following `RDLONG` released early with the previous read's long, and a `WRLONG` released early and lost; what gap clears it; does the waiting form; does a blocking first `RDFAST` remove E7? | VO-J-021 | `CONFIRMED` (all four; E7B clean) | EF-084 |
| 19 | `test-so109-conditional-brk-breaks.spin2` | with break-on-`BRK` armed, does a condition-false `BRK` still enter the debug ISR, showing the previous code; do the `SKIP` and `JMP` forms gate it? | VO-J-022 | `CONFIRMED` (documented behaviour) | EF-085 |

## How the tests were built — independence is the point

Each test was written by an agent given **only its prediction**, with no access to the study's
reasoning, and told to design for refutation: an in-run control that gates the verdict, and both
outcomes written into the program before the run. Every verdict below was then **re-derived from the
raw log lines**, not taken from the program's own `VERDICT` line. The study's briefs are internal
material and are not in this repository; nothing here depends on them.

**Common rig:** bare P2 board (SO80/SO84 drive P3 from the measuring cog — no jumper), 200 MHz,
`pnut-ts` 1.55.8 `-d`, RAM download with reset. Every test measures in a launched PASM cog and
reports from cog 0 only (`DEBUG_COGS = %0000_0001`, EF-057).

## What ran is what is committed — two runs, two builds

**Run 1** (2026-09-24, 20:46–20:51) used the programs as first authored. Before committing, they
were changed in two ways:

1. **End of session.** Every terminal path now calls `finish()`, which prints `DEBUG_END_SESSION` —
   the phrase `pnut-term-ts` watches for to end a headless or `--exit-on-end-session` run.
2. **Style.** Conformed to `central:spin2-authoring-guide`: 133 §2.1 single-letter names renamed,
   header/footer/doc comments, block labels, and single-exit restructuring of the reporting methods
   (§5.1–§5.3). Every PASM measuring engine is byte-identical to run 1's, and every debug string is
   identical apart from the added `DEBUG_END_SESSION`.

**Run 2** (2026-09-24, 23:17–23:21) ran **the files committed here**. Every measured line matches
run 1: O1, SO80 and SO84 line for line (only the loader's start address moved, with the program
size); O17 every pointer step, data pattern and classification (only absolute hub addresses moved);
O18 A and B every `D`, status and bracket result (only the absolute counter timestamps differ, as they
must). Each session ended on its own marker within a second of its last line.

The deciding lines below are from run 1; run 2 prints the same values.

## Deciding lines (verbatim, from the run logs)

**1 — O1.**
```
A5 ctrl WORKAROUND AUGS / ALTD idx,reg 4 / MOV : nchg=1 first win[12]=$3C5C_0A55 dIdx=0
A6 TEST AUGS / ALTD idx,#0 / MOV : nchg=1 first win[8]=$3C5C_0A55 dIdx=5
A7 TEST AUGS / ALTR idx,#3 / MOV : nchg=1 first win[11]=$3C5C_0A55 dIdx=5
D1 ctrl hub=$1357_9B3C  D2 test hub=$1357_9B3C  idxs before=$0000_0061 after=$0000_0061
passes differing longs vs pass 0: 0
```

**2 — O17** (every arm, all 4 rounds identical; trap region untouched throughout).
```
ARM 2 K_BLK4 (control)  n=4  required delta=16   ... delta=16 data=FULL landed=4/4
ARM 3 H_BLK4 (hazard)   n=4  TRUE delta=4  FALSE delta=16   ... delta=4 data=FULL landed=4/4
ARM 8 H_IDX3 (hazard)   n=4  TRUE delta=12  FALSE delta=16  ... delta=12 data=FULL landed=4/4
```

**3 — O18.** Run A, cog 4 first started after wrap 1, then restarted after two missed wraps:
```
A1a cog4 hi=1 p1 ref=$0000_0001_$1020_D896 smp=$0000_0000_$1020_D8B3 ref2=$0000_0001_$1020_D903 D=1
A2  cog4 hi=2 p1 ref=$0000_0002_$1001_40CE smp=$0000_0002_$1001_40F3 ref2=$0000_0002_$1001_413B D=0
A4a cog4 hi=4 p1 ref=$0000_0004_$1020_B1F6 smp=$0000_0002_$1020_B213 ref2=$0000_0004_$1020_B263 D=2
```
Run B (cog 4 running from the start): `D=0` at hi = 0, 1, 2. Group-0 control (cog 1): `D=0` in every
reading of both runs.

**4 — SO80.**
```
rep 0 (i)  B=488 G1=488 G2=488 G2L=488 G3=488 tries=1
rep 0 runA B=976 P=976 RA=16_531
rep 0 runB B=17_080 P=17_080 R1=18_849 R2=13_786 waitx=30 tries=1
Half A: 50 reads; moved 0 (non-Goertzel-active 0); read exactly 0 0
rep 0: waitx=30 kA=255 k1=29 k1-waitx=-1 dA=15_555 dB=15_555 dd=0 class=0
```

**5 — SO84** (sequence #0, N = 64, C = −19). *The tracked rigs now name the accumulations
`xsum`/`ysum` and the held term `xterm`/`yterm` (2026-09-26, before publication); the raw logs, run
before that rename, print the study's own names in their place.*
```
xsum B0=0 B=0 R1=-1_197 R1b=-1_197 R2=-1_216 R3=-2_413 R4=-3_629 R5=-3_648
dx: B-B0=0 d1=-1_197 R1b-R1=0 d2=-19 d3=-1_197 d4=-1_216 d5=-19
counts over 16 sequences: TRUE 16  no-lag 0  lost 0  other 0
```

**12 — E3 waiting keeper** (`debug_260927-162313`): after wrap 1 with only the `WAITATN` keeper,
after wrap 2 with only the `WAITX` keeper, then the positive control with no keeper:
```
E1 cog5 hi=1 (after WAITATN keeper) p1 ref=$0000_0001_$101F_D95F smp=$0000_0001_$101F_D97F ref2=$0000_0001_$101F_D9C8 D=0 lo-bracket=1
X2 cog4 hi=2 (after WAITX keeper) p1 ref=$0000_0002_$101F_E7A7 smp=$0000_0002_$101F_E7C0 ref2=$0000_0002_$101F_E810 D=0 lo-bracket=1
P3 cog5 hi=3 (positive control) p1 ref=$0000_0003_$101F_EBC7 smp=$0000_0002_$101F_EBE7 ref2=$0000_0003_$101F_EC30 D=1 lo-bracket=1
```

**13 — E3, cogs 0-3 stopped** (`debug_260927-162507`; reference = cog 4): cog 1 in the band, then
after the one closing wrap:
```
B1L cog1 band late p10 ref=$0000_0002_$E013_B7FF smp=$0000_0000_$E013_B819 ref2=$0000_0002_$E013_B86A D=2 lo-bracket=1
X1E cog1 closed early p1 ref=$0000_0003_$1001_4BD7 smp=$0000_0003_$1001_4BF1 ref2=$0000_0003_$1001_4C42 D=0 lo-bracket=1
```

**14 — E3 band closing, lag 8** (`debug_260927-162927`): cog 4 across the closing wrap, then Spin2
`GETMS`/`GETSEC` in the band and after it:
```
B4L cog4 band late p10 ref=$0000_0008_$E013_BB0F smp=$0000_0000_$E013_BB32 ref2=$0000_0008_$E013_BB7A D=8 lo-bracket=1
X4E cog4 closed early p1 ref=$0000_0009_$1001_5447 smp=$0000_0009_$1001_546A ref2=$0000_0009_$1001_54B2 D=0 lo-bracket=1
GBL cog5 GETMS/GETSEC band late p10 cog0 ms=190_617..190_617 s=190..190 cog5 ms=18_819 s=18 offMs=171_798..171_798 offS=172..172 class=0
GXE cog5 GETMS/GETSEC closed early p1 cog0 ms=194_637..194_637 s=194..194 cog5 ms=194_637 s=194 offMs=0..0 offS=0..0 class=1
```

**18 — O29** (`debug_261001-000927`): T1 at k = 0 (P = the primer, the previous read's long; S =
the sentinel, a correct read), the window table, the write arm, and the verdicts:
```
T1 k0 af0 rep0 a0-7: PPPSSSSS  agree ........
T1 k0 af1 rep0 a0-7: SPPSSSSS  agree ........
T1 k0 af2 rep0 a0-7: PPPPPPPP  agree ........
T1 k0 af3 rep0 a0-7: PPPPPPPP  agree ........
T1 k0 af4 rep0 a0-7: PPPSPPPP  agree ........
T1 k0 af5 rep0 a0-7: PPPSSPPP  agree ........
T1 k0 af6 rep0 a0-7: PPPSSSPP  agree ........
T1 k0 af7 rep0 a0-7: PPPSSSSP  agree ........
T1 k0 all reps: primer 688 sentinel 336 seed 0 other 0 of 1024 | rep0 primer 43 by delta 8 8 7 6 5 4 3 2 | cells with disagreeing reps 0
RIG OK: O29 - C1 sentinel, PS stream long and C3 (new,new) in every record, no other value in any control run, no record left unwritten, every cell's 16 repetitions identical
  k=0: 8 8 7 6 5 4 3 2 = 43 | 43 | C2 1024
  k=3: 8 8 8 8 8 8 8 8 = 64 | 64 | C2 1024
  k=6: 2 2 2 2 2 2 2 2 = 16 | 16 | C2 1024
  k=7: 0 0 0 0 0 0 0 0 = 0 | 0 | C2 1024
T3 rep0 cells: OO 43 PN 21 NN 0 ON 0 DN 0 any other pair 0 | OO by delta 8 8 7 6 5 4 3 2
T4 rep0 cells: OO 0 PN 0 NN 0 ON 0 DN 64 any other pair 0 | OO by delta 0 0 0 0 0 0 0 0
POSITIVE CONTROL E7N: REPRODUCED - all 64 cells show exactly one failing spacing in 8..15 clk, 16/16 $0000_0000, blocking RDFAST 2 clk
VERDICT O29 RDLONG: CONFIRMED - T1 released 43 of 64 cells early in every repetition, each reading exactly the primer $A5A5_0001, split by delta 8 8 7 6 5 4 3 2 as predicted; C1 and C2 k=0 sentinel in every record
VERDICT O29 WINDOW: CONFIRMED - every k from 0 to 8 and every delta as predicted; zero from k=7 (test RDLONG issued 16 clocks after the RDFAST): 7 non-hub instructions are a sufficient gap
VERDICT O29 WRLONG: CONFIRMED - T3: 43 cells (old,old) (the write lost), split by delta 8 8 7 6 5 4 3 2, and 21 (primer,new) in every repetition; T4 (seed,new) in all 64 (the released write lands when nothing follows)
VERDICT O29 WAITING FORM: CONFIRMED - C2 sentinel in all 1024 records at every k=0..8 and C4 (new,new) in all 1024 cells, in the same run in which the no-wait form released early
VERDICT E7 BLOCKING FIRST: CONFIRMED - with the first RDFAST blocking, new[s] then new[s+1] in all 18432 trials (64 alignments x 18 spacings x 16), the two RDFASTs taking 20..34 clk; E7N in the same run reproduced E7 in 64 of 64 cells
```

**19 — SO109** (`debug_261001-001006`, plain serial, no DEBUG): the condition-false sites and the
verdicts:
```
  rec 02  GETBRK $A1000000  $1FF $00000007  code $A1 b23 0  ret $007  C0 Z0  site e1     flags agree
  rec 05  GETBRK $D4000000  $1FF $40000013  code $D4 b23 0  ret $013  C0 Z1  site e2     flags agree
  rec 06  GETBRK $D4000000  $1FF $40000017  code $D4 b23 0  ret $017  C0 Z1  site e3     flags agree
  record count 10; unattributed 0
VERDICT SO109 BREAK: CONFIRMED - e1, e2 and e3 each entered the debug ISR with their condition false (saved flags agree)
VERDICT SO109 CODE: CONFIRMED - STALE: e1/e2/e3 show $A1/$D4/$D4, the last condition-true code
VERDICT SO109 CANCELS: CONFIRMED - no record from s1 (SKIP), j1 (taken JMP), w1 (if_z JMP taken), w3 (if_z SKIP taken)
VERDICT SO109 IDIOMS: CONFIRMED - w2 (if_z JMP around an unconditional BRK) delivered $F4; w4 (if_z SKIP #1 ahead of it) delivered $F6
```

## What it changes

- **KB:** F-462 … F-466 in `engineering/operations/P2KB-CORRECTION-FINDINGS.md` — `getxacc.yaml` is
  wrong about clearing (F-462) and lacks the lag (F-464); `getct.yaml` lacks the stale-upper-long
  erratum (F-463); `setq.yaml`'s "+4" is only the `[1]` case (F-465); `augs.yaml` gains where the
  damage lands and loses its open `AUGD` scope note (F-466). The E3 band follow-ups (EF-078..080)
  extend F-463 (2026-09-27): the band closes in one wrap, both groups, a waiting cog counts, and
  Spin2 `GETMS()`/`GETSEC()` are affected — `getms.yaml`/`getsec.yaml` join `getct.yaml`.
- **P2 Errata manual:** all five enter it, three of them as errata no vendor document carries.
  E3's chapter is rewritten around the band on EF-078..080 (v0.2.0).
