# E4 sources: Chapter 4, GETXACC Clears Only During a Goertzel Burst

Verification sidecar for `opus-master/e4-getxacc-clear-gating.md`. Every number, quotation and
code excerpt in the chapter maps to a file and line below. Internal document: ids and paths are
allowed here, never in the chapter.

## Abbreviations

| Tag | File |
|---|---|
| **DOC** | `engineering/ingestion/sources/silicon-doc/p2-documentation.txt` |
| **LED** | `engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md` (campaign header 884–896, EF-069 at 958–976, EF-070 at 978–990) |
| **RIG** | `engineering/document-production/manuals/p2-errata/audit/verification-tests/test-so80-getxacc-clear-gating.spin2` |
| **L2** | `.../audit/verification-tests/logs/debug_260924-231817.log` (run 2, style-conformed build, `.bin` 15616 bytes, L2:14) |
| **L1** | `.../audit/verification-tests/logs-orig/debug_260924-204741.log` (run 1, as-authored build, `.bin` 15581 bytes, L1:14) |
| **HAR** | `engineering/document-production/manuals/p2-errata/audit/verification/e4-harness-difference.spin2` |
| **BRF** | `engineering/document-production/manuals/p2-errata/code-validation/test-briefs/BRIEF-SO80.md` (mechanism only; not quoted) |

L1 and L2 carry the measurement lines at the **same line numbers** (23–102). Every `Cog0` line
of the two logs is identical except the `INIT ... jump` address (different builds) and the
final `DEBUG_END_SESSION` line, present only in L2. Command used to check this:
`diff <(grep -o "Cog0 .*" L2) <(grep -o "Cog0 .*" L1)` with the full paths above; output was
exactly those two differences.

## Quotations (Parallax P2 Documentation)

| Chapter text | Source |
|---|---|
| "Get Goertzel X into D and Y into next S, clear X and Y" | DOC:2745 (STREAMER section, heading DOC:2723; the table's instruction column lists `GETXACC` at DOC:2731, operand `D` at DOC:2737) |
| "After some number of complete NCO cycles, ... until a new streamer command executes." | DOC:4096–4099, copied exactly, line breaks joined with single spaces. This is the passage `getxacc.yaml` cites as "silicon-doc-text.txt:1604". Section heading "DDS/Goertzel" at DOC:3984 |
| "Accumulations (SIN_ACC/COS_ACC are read and cleared by GETXACC)" | DOC:4105, column heading of the D[23] SINC1/SINC2 table introduced at DOC:4100 |
| "None of the three places makes the clear depend on the streamer's mode ..." | `grep -n -i "GETXACC\|goertzel" DOC` returns GETXACC at 2532, 2731, 2745, 4097, 4105, 4230, 5674, 11401 only. 2532 (Q register), 4230 (demo code), 5674 (interrupt-shielding list), 11401 (opcode map) state no condition either |

## Terms and mode names

| Chapter text | Source |
|---|---|
| "the immediate-to-pins mode, one pin wide, with its output disabled" | `$4000_0400`: RIG:177 comment "1-pin immediate, D[23]=0, no DAC, count $400"; RIG:133 "Non-Goertzel (D[31:16] = $4000): [15:12]=0100 ... [7]=0 (%e off)"; mode %0100 is "Immediate ⇢ Pins/DACs" at DOC:2964–2965 |
| SINC1 | D[23] = 0 in `$F007_xxxx`; DOC:4100–4116 (D[23] %0 = SINC1); RIG:131–132 |
| "P3 inverted and summed, the other three pins ignored" | `S` = `$0008_80A5`: S[19:16] = %1000, S[15:12] = %1000; DOC:4035–4044 (%1xxx_1xxx = base pin +3 inverted and summed; `%xxxx_0xxx` rows ignore pins +0..+2); RIG:55, RIG:134 |
| "input pins P0 to P3" | RIG:52–53, RIG:132 ([6:3]=0000, group 0, pins 0..3) |
| "a term is the product the streamer adds to each accumulator on each of those clocks" | DOC:4094–4095 ("multiplied by the bitstream sum ... then added into their respective 32-bit accumulators") |
| "32-bit limit" | DOC:4095 ("32-bit accumulators") |

## Numbers

| Chapter number | Where it appears | Source |
|---|---|---|
| 100 clocks (G2L read) | What the part does; How it was proven | RIG:180 `G2L_WAIT = 100`, RIG:542 `waitx #G2L_WAIT` |
| 256-clock burst | Symptom, Workaround, Proof | RIG:174 `N_RUN = 256`; RIG:689 `drun_`; RIG:128 `drun_ = $F007_0100` |
| 14,823 → 30,378, contributed 15,555 | Symptom | L2:32 `rep 1 runA B=14_823 P=14_823 RA=30_378`; L2:82 `rep 1: ... dA=15_555` |
| 29 terms, started from 17,080, returned 18,849 | Symptom | L2:28 `rep 0 runB B=17_080 P=17_080 R1=18_849 R2=13_786 waitx=30`; L2:81 `k1=29` |
| 15,555 in all eight repetitions | Workaround, Proof | L2:81–88, `dA=15_555` on every line |
| starting values 976, 14,823, 12,871, 10,919, 8,967 | Workaround | run A `P=` at L2:27 (976), L2:32/37/42/47 (14_823), L2:52 (12_871), L2:57 (10_919), L2:62 (8_967) |
| `$F007_0100`, `$0008_80A5` (snippet) | Workaround | RIG:128–129 ("drun_ = $F007_0100", "son_ = $0008_80A5", decoded from the .lst); RIG:170, 174, 175 |
| 4,000-clock wait | Workaround, Proof | RIG:179 `WAIT_IDLE = 4000`; RIG:125 (`WAITX ##4000` encoding); RIG:86 |
| NCO frequency `$8000_0000` | Workaround, Proof | RIG:178 `FRQ = $8000_0000`, RIG:478 `setxfrq frq_`, RIG:130 |
| 36,600 (largest value read) | Workaround | L2:63 `rep 7 runB ... R1=36_600`; the largest value on any raw line L2:23–64 (sine values are smaller) |
| 200 MHz | Proof, Status | RIG:161; L2:21 `clk 200 MHz`; LED:892 |
| nothing connected to P0 to P7 | Proof | RIG:34 "NO JUMPER, nothing connected to P0..P7"; L2:21 "NO jumper" |
| debugger confined to cog 0 | Proof | RIG:162 `DEBUG_COGS = %0000_0001`; RIG:45–47 |
| P3 driven low, smart pin off | Proof | RIG:35–37, RIG:475–476 |
| 512 LUT longs, `$173D_0000` | Proof | RIG:58, RIG:129 (`lutv_ = $173D_0000`), RIG:480–487 (fill + readback) |
| 61 (cosine), 23 (sine) per active clock | Proof | RIG:59–63, RIG:165–166; confirmed by CAL L2:66–67 and Y CAL L2:93 (1_449 = 63 × 23) |
| 8-clock, 4-clock preamble bursts; zero-term `S` `$0008_00A5` | Proof | RIG:84–85, RIG:171–172, RIG:129 (`szero_ = $0008_00A5`), RIG:636–650 |
| +3,843 / −3,843, 63 × 61 | Proof | L2:66 `CAL: dLO=3_843 dHI=-3_843`; L2:67 `CAL: kLO=63 kHI=-63` |
| 64-clock calibration bursts | Proof | RIG:173 `N_CAL = 64`; RIG:688 |
| controls all passed | Proof | L2:68 `controls: all passed (LUT, XFI, P3 level, B<>0, CAL sign+negation, dA)`; same at L1:68 |
| `$4000_0400`, count `$0400` | Proof | RIG:177, RIG:128 (`dimm_ = $4000_0400`) |
| eight repetitions | Proof | RIG:181 `REPS = 8`; L2:21 `reps 8` |
| 50 reads, all equal to B, none zero | Proof | L2:78 `Half A: 50 reads; moved 0 (non-Goertzel-active 0); read exactly 0 0`; L2:79 verdict line. Composition from RIG:344–352: 2 calibration P reads + 8 reps × (G1, G2, G2L, G3, run A P, run B P) = 50 |
| 488 (B and four reads, first repetition) | Proof | L2:25 `rep 0 (i)  B=488 G1=488 G2=488 G2L=488 G3=488` |
| delays 30 ×4, then 62, 94, 126, 190 | Proof | RIG:696 `dlytab`; L2:81–88 `waitx=` values |
| Table: 16,531 − 976 = 15,555 = 255 terms | Proof | L2:27 `rep 0 runA B=976 P=976 RA=16_531`; L2:81 `kA=255 ... dA=15_555` |
| Table: 18,849 − 17,080 = 1,769 = 29 terms | Proof | L2:28; L2:81 `k1=29`. 1,769 = 29 × 61 also stated at LED:969 |
| Table: R2 = 13,786 = 226 terms | Proof | L2:28 `R2=13_786`. 226 = 13,786 / 61 is arithmetic (226 × 61 = 13,786), stated at LED:970 |
| Table: R1 + R2 − P = 15,555 | Proof | L2:81 `dB=15_555 dd=0` |
| read point term 29 to term 189, one behind `WAITX` | Proof | L2:81 `k1=29 k1-waitx=-1`, L2:88 `waitx=190 ... k1=189 k1-waitx=-1`; all eight lines L2:81–88 show `k1-waitx=-1`; LED:971 |
| dd = 0 in all 8 | Proof | L2:81–88 `dd=0 class=0`; L2:89 `classes: 0 conf=8 ...`; L2:91 verdict |
| R2 = 13,786 in first four repetitions; run B started at 17,080 then 30,927 | Proof | L2:28, 33, 38, 43 (`R2=13_786`; `P=17_080`, then `P=30_927` ×3) |
| sine: moved on no idle read; 5,865 both runs every repetition | Proof | L2:94–101 `Y rep n: dA=5_865 dB=5_865 dd=0`; L2:102 `Y Half-A-style checks that moved: 0` |
| run twice, 2026-09-24, two builds, identical values | Proof, Status | LED:892–894; log timestamps L1:1 (20:47), L2:1 (23:18); the diff above |
| outcomes fixed before the run (dd = R1, −C, +C) | Proof | RIG:25–31 (written before the run), RIG:405–416 (classes) |
| `POLLXFI` finished / still running | Proof | RIG:663–674 (`xfi_end`, `xfi_mid`); L2:68 |
| 255 terms, not 256 = Chapter 5's lag | Proof | LED:979–980 (EF-070: "A reading taken after a burst of N clocks holds N − 1 terms") |

## Measured-vs-derived labels in *The workaround*

| Statement | Class | Basis |
|---|---|---|
| Before-and-after idle difference gives the burst | Measured | Run A in every repetition (L2:81–88, dA constant across five distinct P values) and the calibration pair (L2:66) |
| Read inside a burst: (R1 − P) + R2 equals the unread burst | Measured | L2:81–88 `dd=0` |
| "a longer burst needs a longer wait" | Follows from the condition | Both reads must fall outside the burst; the only wait measured was 4,000 clocks for bursts of at most 256 Goertzel clocks (1,024 for the non-Goertzel command, RIG:177/179) |
| Not tested: SINC2, more than one pin, `XZERO`/`XCONT`, `XCONT` loops, 32-bit limit | Scope | RIG:52–55 (SINC1, one pin), every Goertzel start is `xinit` (RIG:497, 513, 570, 592, 639, 642); no value above 36,600 read |

The ledger (LED:975) says `getxacc.yaml`'s read-before-and-after rule "is exactly what this
behaviour requires"; the chapter states only what run A measured.

## Code excerpts (verbatim, contiguous)

| Chapter excerpt | Source lines | Max width |
|---|---|---|
| Command words `dch_` ... `dlytab` | RIG:686–696 | 56 |
| Calibration before-and-after block `call #preamble` ... `mov ry_, 0-0` | RIG:494–502 | 35 |
| Run B read inside the burst `call #preamble` ... `mov r1y_, 0-0` | RIG:589–595 | 63 |
| Prose description of phase (i) (not excerpted: RIG:539, 540, 543, 546 exceed 76 columns) | RIG:533–551 | n/a |

Byte-identity checked by printing both sides with
`awk '/^```/ { inb = !inb; print "----"; next } inb { printf "%d|%s|\n", length($0), $0 }' <chapter>`
and `awk '(NR>=686 && NR<=696) || (NR>=494 && NR<=502) || (NR>=589 && NR<=595) { printf "%d|%s|\n", NR, $0 }' <RIG>`.

## Workaround snippet

Not taken from the rig. Compiled inside HAR, between the `SNIPPET BEGIN` / `SNIPPET END`
markers, byte-identical to the chapter's first `pasm2` fence (widths 23–72, all ≤ 76).
No `debug()`, so no `-d`. The harness was copied to the session scratchpad and compiled there so
no `.bin`/`.lst` lands in the manual tree:

```
/usr/local/bin/pnut-ts -l <scratchpad>/e4-harness-difference.spin2
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: Wrote <scratchpad>/e4-harness-difference.bin (6344 bytes)
pnut-ts: Done
```

`/usr/local/bin/pnut-ts --version` reports `PNut-TS: v1.55.8`. The path named in the chapter
brief (`/home/vscode/.local/pnut/pnut-ts-linux-arm64-015508/pnut_ts/pnut-ts`) does not exist in
this container.

## *Why it happens*: paraphrase basis

Paraphrased from BRF Part 2 ("Half A — the enable", "Half B — why the coincidence",
"The claim in one paragraph") and Part 4, at the programmer's-model level: the accumulators
update only on clocks of an active DDS/Goertzel command; the clear is a substitution inside that
update rather than a separate write; the read returns the value from before the clearing edge;
after a clear the accumulator holds the one pending term. No HDL fragment, signal name, module
name or line reference from BRF appears in the chapter. "By the study's reading, every mode
other than DDS/Goertzel behaves as the idle streamer does" rests on BRF Part 2's statement that
the update is gated on the single DDS/Goertzel mode pattern; the bench tested one other mode.

## Where the chapter departs from the ledger's wording

- LED:959 "Idle, or in any other streamer mode": the chapter says one other mode was tested
  (RIG:170–177 has one non-Goertzel mode), and attributes "every mode" to the study's reading.
- LED:966–967 counts "50 of 50 reads" beside G1, G2, G2L, G3 only; the 50 also include the idle
  reads before the calibration and run A/B bursts (RIG:344–352). The chapter gives the full
  composition.
- LED:968 "B itself grows across reps (488 → 14,335) with no clear between them": not used.
  Run B's read inside the burst does clear between repetitions (R2 = 13,786 whatever the
  starting value), so the chapter uses run A's P → RA growth instead.
