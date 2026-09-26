# E5 sources: Chapter 5, The Goertzel Accumulators Trail by One Clock

Chapter: `opus-master/e5-goertzel-one-clock-lag.md`. Every number, quotation and code excerpt
in the chapter, mapped to its source. Paths are repo-relative; `M` =
`engineering/document-production/manuals/p2-errata`.

| Key | Path |
|---|---|
| LEDGER | `engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md` |
| LOG2 | `M/audit/verification-tests/logs/debug_260924-231829.log` (second run, style-conformed build) |
| LOG1 | `M/audit/verification-tests/logs-orig/debug_260924-204804.log` (first run, as-authored build) |
| RIG | `M/audit/verification-tests/test-so84-goertzel-last-term-lag.spin2` |
| SDOC | `engineering/ingestion/sources/silicon-doc/p2-documentation.txt` |
| CLASS | `M/CLASSIFICATION-GUIDANCE.md` |
| HARN | `M/audit/verification/e5-harness-zero-burst.spin2` |

LOG1 and LOG2 carry identical data on lines 20-145 (timestamps aside); every log line quoted
below is from LOG2 and appears with the same content at the same line number in LOG1.

## 1. Quotations of Parallax documentation

| Chapter text | Source |
|---|---|
| "This mode is unique, in that it outputs and inputs on every clock in which the command is active." | SDOC:3985 (first sentence of the line) |
| "The 8-bit sine (byte 3) and cosine (byte 2) values from the lookup RAM will each be multiplied by the bitstream sum (an integer from -3 to +3) and then added into their respective 32-bit accumulators." | SDOC:4094-4095 (one sentence across the line break) |
| `SIN_ACC += SIN_MUL`, `COS_ACC += COS_MUL`, SINC1 case, D[23] = `%0` | SDOC:4100-4116 (D[23] table; `%0` SINC1 at 4107-4109; `SIN_MUL = bitstream_sum * lookup_sin` 4111, `COS_MUL = bitstream_sum * lookup_cos` 4112, `SIN_ACC += SIN_MUL` 4115, `COS_ACC += COS_MUL` 4116; "36" at 4113 is a page number) |
| "(SIN_ACC/COS_ACC are read and cleared by GETXACC)" | SDOC:4105 (not quoted in the chapter; context for the D[23] table) |
| KNOWN BUGS does not list this behaviour | SDOC:197-227 (lists only the SETQ/ALTx and AUGS/ALTx bugs); `grep -n -i "goertzel\|getxacc"` over SDOC returns no line in 197-227 |
| SINC2 is D[23] = `%1` | SDOC:4117-4119 |
| `XINIT` "Issue command immediately, zeroing phase" (paraphrased: issues its command immediately) | SDOC:2742 |
| S[15:12] selects which pins are summed; S[19:16] which are inverted | SDOC:4002-4006 |
| With S[19] clear and S[15] set, base pin +3 is summed, 0 counts -1, 1 counts +1 | SDOC:4035-4044 (`%0xxx_1xxx` "Base pin +3 is summed", `(0 ⇢ -1, 1 ⇢ +1)`) |
| `SETXFRQ` D is a 0-to-1 multiplier of the system clock times `$8000_0000` (so `$8000_0000` = one rollover per clock) | SDOC:2753-2754 |
| D[15:0] is a counter decremented on each NCO rollover | SDOC:3500-3501 |
| Mode word layout `1111 dddd 0ppp p111` (SINC1) / `1111 dddd 1ppp p111` (SINC2) | SDOC:3483-3491 |
| GETXACC: cosine into D, sine into the next instruction's S | SDOC:4097-4098 |

## 2. Design-material statement (paraphrased, not quoted)

| Chapter text | Source |
|---|---|
| "notes in the design describe the per-clock product as feeding the accumulator, with both valid on the same clock" | CLASS:39 (the guidance's own class-1 example: "the designer's own notes describe one accumulator as feeding a second, and say both are valid on the same clock"). No design material was read or quoted. |

## 3. Claims about what the part does

| Chapter claim | Source |
|---|---|
| Reading after N clocks holds `N-1` terms; the last waits in an internal register no instruction reads; added on the first active clock of the next Goertzel burst; waiting does not deliver it | LEDGER:978-981 |
| Workaround: short zero-term burst, same mode, S[15:12] (ledger: `imm[15:12]`) clear, before reading; reading then holds all N terms; nothing spills | LEDGER:981-983 |
| 16 of 16; sign flips with P3; sine channel same pattern with 37 | LEDGER:987-989 |
| Rig conditions: bare P2 board, 200 MHz, pnut-ts 1.55.8 -d, 2026-09-24, run twice from two builds with identical measuring engines, every value matched | LEDGER:892-894 |
| Not published by Parallax; new | LEDGER:978 heading "(new)"; LEDGER:887-889 |
| SINC2 size of shortfall not settled by the study's reading | study brief, "What the source does not settle", second item (mechanism only; not quoted) |
| Mechanism in *Why it happens* | study brief Part 2, paraphrased at programmer's-model level; no signal/module names, no HDL, no line refs |

## 4. Numbers

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
| `$0000_80C3`, `$0000_00C3` | product / zero S operands | RIG:181-182, 158-159 |
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

### Raw log lines the numbers were taken from (LOG2, verbatim)

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

## 5. Code

| Chapter code | Source |
|---|---|
| Workaround snippet (10 lines) | HARN:45-54, byte-identical (between the SNIPPET markers at HARN:44 and HARN:55). Compiled: `/usr/local/bin/pnut-ts -l <scratchpad copy>` (v1.55.8), no debug(). Result: `Wrote .../e5-harness-zero-burst.bin (6420 bytes)`, `Done`. Encodings from the .lst: `getxacc base_x` `$FD603E1E`; `mov base_y,0-0` `$F6004000`; `xinit dburst,imm_on` `$FCA0341C`; AUGD `$FF800000` + `waitx` `$FD67E81F`; `xinit dzero,imm_off` `$FCA0361D`; `getxacc x` `$FD60421E`; `mov y,0-0` `$F6004400`; `sub x,base_x` `$F180421F`; `sub y,base_y` `$F1804420`. |
| Excerpt 1: `dmode_` .. `imk_` (4 lines) | RIG:736-739, verbatim |
| Excerpt 2: burst, R1, R1b, zero burst, R2 (12 lines) | RIG:694-705, verbatim |
| Excerpt 3: carry arm (14 lines) | RIG:707-720, verbatim |
| Widths | every excerpt line at most 76 columns (RIG:712 is exactly 76); snippet lines at most 67 |
| Verbatim check | `grep -n -x -F -f RIG chapter` and `grep -n -x -F -f HARN chapter` list every non-blank code line of the excerpts and the snippet |
