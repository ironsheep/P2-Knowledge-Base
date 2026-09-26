# E6 sources: Erratum E6, In a DAC Smart-Pin Mode, OUT Needs TT Bit 0 to Run the ADC

Verification sidecar for `opus-master/e6-dac-mode-adc-enable.md`. Every number, quotation and
code excerpt in the chapter maps to a file and line below. Internal document: ids and paths are
allowed here, never in the chapter. Written 2026-09-26 (task «#359», v0.2.0 shape).

## Abbreviations

| Tag | File |
|---|---|
| **DOC** | `engineering/ingestion/sources/silicon-doc/p2-documentation.txt` |
| **SPIN** | `engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt` |
| **LED** | `engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md` (second-session header 994–1005, EF-071 at 1007–1025) |
| **RIG** | `engineering/document-production/manuals/p2-errata/audit/verification-tests/test-so9-dac-mode-adc-enable.spin2` (byte-identical to the tracked campaign copy `engineering/ingestion/external-sources/hardware-verification/campaigns/2026-09-p2-errata-predictions/tests/test-so9-dac-mode-adc-enable.spin2`: `cmp` of the two printed nothing; one commit, `b91cbf65`) |
| **L1** | `.../audit/verification-tests/logs/debug_260925-214057.log` (run 1, 2026-09-25 21:40:57; `.bin` 14927 bytes, stamped Modified 2026-09-26T03:39:24Z, L1:6) |
| **L2** | `.../audit/verification-tests/logs/debug_260925-214845.log` (run 2, 2026-09-25 21:48:45; `.bin` 14927 bytes, stamped Modified 2026-09-26T03:48:34Z, L2:14) |
| **BRF** | `engineering/document-production/manuals/p2-errata/code-validation/test-briefs/BRIEF-SO9.md` (git-ignored, Internal; mechanism only, never quoted) |

L1's report lines are L1:12–82; L2's are L2:20–90, offset by 8 (L2 opens with a baud-rate
session, L2:1–8). Read side by side, every `Cog0` line is the same except the C2 samples
(L1:43–47 / L2:51–55) and the C2 range (L1:61 / L2:69). This matches LED:1003 ("SO9 is
identical except the running ADC's C2 toggle counts").

The two logs name the same `.bin` size and different Modified stamps; LED:1002 calls the two runs
"same builds". The chapter says only "run twice". The rig `.spin2` was last modified before
both runs (file mtime 2026-09-26 03:30Z = 21:30 local, the log clock).

The task named the second run as "21:49"; the SO9 log of the second run is stamped 21:48:45
(L2:1). The 21:48:58 and 21:49:22 logs of that session are the other two rigs, not SO9
(`grep -l SO9` over the logs folder returns only L1 and L2).

**Workaround wording (2026-09-26, task #360; Stephen's decision, voice-guide §2).** The reader's
change is a *workaround*, never a *fix* (a fix is a silicon revision). Section *The fix*
(`{#sec-e6-fix}`) is now *A proven workaround* (`{#sec-e6-workaround}`), rule-first: *What any
workaround must do* (the condition, as in the front matter's summary table), *One way, proven
on a real P2* and the one-line block, then *Other ways that meet the condition*. The CAUTION
box's third line is *Workaround* (the condition); the status row is *Workaround proven on
silicon*. In ARCHIVE only the header purpose changed (*the `TT` = `%01` word is the
workaround*): no line added or removed, and the object image is byte-identical to the pre-#360
archive. Below, "Fix" in the *Where it appears* column means *A proven workaround*.

## Quotations (Parallax P2 Documentation)

| Chapter text | Source |
|---|---|
| "for all smart pin modes (%SSSSS > %00000):" ... "1x = OTHER enables ADC in DAC_MODE, M[7:0] overridden" (six lines) | DOC:7652–7657, copied line for line. The `%TT:` field heading is DOC:7626; the section is SMART PINS, heading DOC:7495; the `WRPIN` D layout with `TT` at bits 7:6 is DOC:7572 |
| "'DAC_MODE' is enabled when M[12:10] = %101" | DOC:7638 (same `%TT` block) |
| "RDPIN/RQPIN can be used to retrieve the 16-bit ADC accumulation from the last sample period." | DOC:7908, in "%00001 and DAC_MODE = DAC noise" (DOC:7902). Section heading SMART PIN MODES at DOC:7891 |
| "If OUT is high, the ADC will be enabled and RDPIN/RQPIN can be used to retrieve the 16-bit ADC accumulation from the last sample period." | DOC:7923–7924 (`%00010`, heading DOC:7911) and DOC:7937–7938 (`%00011`, heading DOC:7927), identical sentences; line break joined with one space |
| "the pin's 8-bit DAC pseudo-random data on every clock" | DOC:7903 ("This mode overrides M[7:0] to feed the pin's 8-bit DAC pseudo-random data on every clock.") |
| "while a smart pin is configured, the %TT bits, explained above, will govern the pin's output enable, regardless of the DIR state" | DOC:7859–7860 (sentence begins "Note that while ..."; line break joined) |
| "relative -1 pin's read state" | DOC:7585 (`x111`) |
| "The resultant 'A' will drive the IN signal" | DOC:7615 ("... in non-smart-pin modes.") |
| KNOWN BUGS does not list this behaviour | DOC:197–227: two items only (SETQ/ALTx PTRx deltas; ALTx immediate-#S and AUGS) |

## Terms, fields and symbols

| Chapter text | Source |
|---|---|
| DAC smart-pin modes `%00001` to `%00011` with `M[12:10]` = `%101` | DOC:7655 (`%SSSSS = %00001..%00011`), DOC:7638, DOC:7685–7707 |
| `TT` bits 7:6; bit 6 is `TT` bit 0 | DOC:7572; RIG:44, RIG:66 ("the word above with D[6] set") |
| "Bit 0 of `TT` sets the output enable; bit 1 chooses whether `OUT` or `OTHER` switches the ADC" | reading of DOC:7653–7654 (`x0`/`x1`) and DOC:7656–7657 (`0x`/`1x`) |
| `P_DAC_990R_3V` = "a 990-ohm DAC of 3.3 V peak, with the ADC feeding the pin's input" | SPIN:1476 ("P_DAC_990R_3V \| DAC 990Ω, 3.3V peak, ADC 1x → IN"); `M[9:8]` = `%00`: RIG:56–57 |
| `P_TT_01`, `P_OE` same value | SPIN:1522 (`P_TT_01`, `..._01_00000_0`), SPIN:1525 (`P_OE`, same bit pattern) |
| `P_TT_00`, `P_DAC_NOISE` | SPIN:1521, SPIN:1531 |
| `P_MINUS1_A`, `P_LOGIC_A`, `P_NORMAL` | SPIN:1432, SPIN:1456, SPIN:1529 |
| compositions `P_DAC_990R_3V \| P_TT_00 \| P_DAC_NOISE` etc. | RIG:216–218 |
| in a smart-pin mode `IN` is the smart pin's flag | DOC:7502 ("The IN bit serves as a flag to indicate to the cog(s) that the smart pin has completed some function ...") |
| `DIRL` holds the smart pin in reset while it is configured | DOC:7855 ("A smart pin should be configured while its DIR bit is low, holding it in reset"); RIG:147–153, RIG:639 |
| smart pin off rows for DAC_MODE (`%SSSSS` = `%00000`) | DOC:7640–7651 |
| no `WXPIN`/`WYPIN` issued | RIG:63–64 ("needs no WXPIN/WYPIN setup"); RIG:590–669 contains no `wxpin`/`wypin` |
| no `RDPIN`/`RQPIN` issued; pin read through neighbour | RIG:87–90 ("Pin P's own IN is not read"); RIG:590–669 contains no `rdpin`/`rqpin` |

## Numbers

| Chapter number | Where it appears | Source |
|---|---|---|
| `$0014_0002` (TT = %00) | box, Actual, Fix, Proof, Program | RIG:212; L1:27 / L2:35 `pin P TT=%00 $0014_0002: ... TT=%0 SSSSS=%1 bit0=0  symbols=$0014_0002`; LED:1013 |
| `$0014_0042` (TT = %01) | box, Actual, Fix, Proof, Program | RIG:213; L1:28 / L2:36 `pin P TT=%01 $0014_0042: ... TT=%1 SSSSS=%1 ... symbols=$0014_0042`; LED:1013 |
| `$7000_0000`, `%AAAA` = `%0111` | Proof | RIG:214, RIG:69–77; L1:29 / L2:37 `pin P+1      $7000_0000: AAAA=%111 ... symbols=$7000_0000` |
| `M[12:10]` = `%101` | opening, Actual, Why | RIG:53–55; L1:27–28 `(M[12:10]=%101)` |
| `$40` (bit 6) | Fix | SPIN:1522 (bit 6 set in the pattern); RIG:66 |
| P4 under test, P5 observer, bit 5 of `INA` | Proof, Program | RIG:191–192; L1:13 / L2:21 `pin P = 4 (under test), P+1 = 5 (observer, DIR low)` |
| 4,096 reads per sample | Actual, Proof, Program | RIG:197; L1:13 `4_096 INA reads per sample` |
| 6 clocks per read, three-instruction `REP` | Proof | RIG:89–90 ("6 clocks per read"); RIG:651 `rep #3, reads_` |
| 10,000-clock `WAITX` | Proof, Program | RIG:198 `SETTLE_CLK = 10_000`; RIG:649; L1:13 `settle 10_000 clocks` |
| five rounds, C1..C4 order | Proof, Program | RIG:196; RIG:602–613; L1:13 `5 rounds` |
| 200 MHz | Proof, Status | RIG:188 `_clkfreq = 200_000_000`; LED:1001 |
| nothing attached to P4, P5 | Proof | RIG:29 ("NOTHING attached to P4 or P5"); LED:1001 (free pins P0–P7) |
| measuring cog = cog 1, both runs | Proof | L1:30 / L2:38 `measuring cog = 1 (debugger restricted to cog 0)` |
| `DEBUG_COGS = %0000_0001` | Proof | RIG:189 |
| TT=%00, OUT high: 0 in every one of 4,096 reads, every sample | box, Actual, Sees, Proof table | L1:53–57 / L2:61–65 (`C4 TT=%00 OUT high  round n: 0`, n = 1..5); L1:63 / L2:71 `min 0  max 0`; LED:1017 |
| TT=%00, OUT low: 0 | Actual, Proof table | L1:48–52 / L2:56–60; L1:62 / L2:70 |
| TT=%01, OUT low: 0 in every read | Actual, Proof table | L1:38–42 / L2:46–50; L1:60 / L2:68; LED:1015–1016 |
| 1,958 to 2,093 of 4,096 per sample, across the two runs | Actual | L1:61 `C2 ... min 1_963  max 2_093`; L2:69 `C2 ... min 1_958  max 2_017`; LED:1016 ("1,963–2,093 / 1,958–2,017") |
| run 1 C2: 1,963, 2,093, 2,025, 1,986, 2,056 | Proof table | L1:43–47 `C2 TT=%01 OUT high  round 1: 1_963` ... `round 5: 2_056` |
| run 2 C2: 2,006, 2,017, 1,958, 1,985, 2,016 | Proof table | L2:51–55 `round 1: 2_006` ... `round 5: 2_016` |
| ten samples (C2 and C1, two runs) | Proof | 5 rounds × 2 runs; L1:38–47, L2:46–55 |
| path control 4,096 / 0 before and after | Proof, Program | L1:33–34 / L2:41–42 `before rounds: P high -> 4_096   P low -> 0`, `after rounds : P high -> 4_096   P low -> 0`; RIG:203–204; LED:1019 |
| separation results | Proof | L1:75–77 / L2:83–85 `C2 separates from C1: YES`, `C4 separates from C3: NO`, `C4 separates from C2: YES` |
| verdict | Proof | L1:79–80 / L2:87–88 `VERDICT: CONFIRMED - ...`, `OUT does not switch the ADC unless TT bit 0 enables the output` |
| controls all passed (no `RIG FAIL`) | Proof | no `RIG FAIL` line in L1 or L2; control W lines L1:27–29 decode as expected (RIG:354–356 expectations) |
| outcomes written before the run | Proof | RIG:118–135 (header, pre-registered); RIG:333–343 printed at L1:14–24 before any sample |
| 2026-09-25, run twice | Proof, Status | L1:1, L2:1; LED:1001–1002 |
| C2 is the workaround; OUT high runs ADC at TT=%01 | Fix, Proof, Status | LED:1021 ("Workaround proven: set TT bit 0 and accept the fast DAC driving the pin (C2)") |
| *What any workaround must do*: set `TT` bit 0 in the `WRPIN` word of a DAC-mode pin whose ADC `OUT` switches | LED:1021; C2 vs C4 (L1:43–47 vs L1:53–57); DOC:7653–7654 (`x1` = output enabled); front matter summary table |
| *One way*: the tested DAC noise word with `TT` = `%01` | RIG:213; the rows above |
| *Other ways*: the Spin2-symbol form and the literal are the same change | RIG:217 (`P_DAC_990R_3V \| P_TT_01 \| P_DAC_NOISE`), L1:28 `symbols=$0014_0042`; SPIN:1522/1525 (`P_TT_01` = `P_OE`) |
| *Other ways*: `TT` = `%11` also sets bit 0, but gives the ADC switch to `OTHER`; not tested | DOC:7657 (`1x = OTHER enables ADC`); RIG tests `TT` = `%00` and `%01` only (RIG:212–213; LED:1022) |

## The drop-in block (A proven workaround)

| | |
|---|---|
| Chapter | the `spin2` fence under *One way, proven on a real P2* in *A proven workaround* (one line, chapter 63) |
| Source | RIG:213 (as-run), ARCHIVE:50 (printed, `examples-library/e6-dac-mode-adc-enable-test.spin2`; same one line; the archive's header comment was rewritten, so the line number moved), one line, byte-identical, 71 columns, no tab characters in RIG (`grep -c -P "\t"` = 0) |
| The run that proved it | the constant is loaded into `cfg_tt01_` (RIG:660) and written by `wrpin cfg_, #PIN_P` (RIG:640) for C1 and C2 (RIG:603). C2 = the workaround: L1:43–47 and L2:51–55 (ADC running, 1,958–2,093), C1 = L1:38–42 / L2:46–50 (ADC off, 0) |
| Why one line | No contiguous rig block that holds the `WRPIN`/`DIRH`/`OUTH` sequence is ≤ 76 columns: `do_cond` RIG:639 is 93 columns and RIG:643 is 90. RIG:213 is the only contiguous run of lines that is the workaround itself and fits K |
| Symbol form | `P_DAC_990R_3V \| P_TT_01 \| P_DAC_NOISE` = RIG:217, stated inline (not a fence); equality to `$0014_0042` checked at run time, L1:28 `symbols=$0014_0042` |

## Code excerpts (verbatim, contiguous; `sample` routine now mirrors ARCHIVE)

**Printed code now mirrors the conformed archive copy (2026-09-26, «#360»); the measuring PASM
is byte-identical to the as-run rig.** ARCHIVE = `examples-library/e6-dac-mode-adc-enable-test.spin2`
(conformed 2026-09-26, task #360: the `sample` routine's `REP` now takes a label operand,
`rep @.read_end, reads_`, in place of `rep #3, reads_`, with the loop's last instruction
relabelled `.read_end`; same three-instruction repeat body, same PASM measuring image,
byte-identical to RIG's).

| Chapter excerpt | RIG lines (as-run, history) | ARCHIVE lines (printed) | Max width |
|---|---|---|---|
| Drop-in `CFG_DAC_TT01 = $0014_0042 ...` (content unchanged by #360; archive line differs, header rewritten) | RIG:213 | ARCHIVE:50 | 71 |
| Round loop `mov round_, #ROUNDS` ... `djnz round_, #.round` (content unchanged by #360; archive line differs) | RIG:602–613 | ARCHIVE:439–450 | 72 |
| `sample` routine, comment line ... `ret` (`rep @.read_end, reads_` / `.read_end wrlong ...` in place of `rep #3, reads_` / `wrlong ...`) | RIG:648–657 | ARCHIVE:485–494 | 75 |
| `path_control`, two comment lines ... `ret` (content unchanged by #360; archive line differs) | RIG:628–636 | ARCHIVE:465–473 | 74 |
| `do_cond` described in prose only (RIG:639 = 93 and RIG:643 = 90 columns) | RIG:638–646 | n/a | n/a |
| end-of-run pin release, described in prose | RIG:617–623 | n/a | n/a |

Byte-identity checked by printing both sides:
`awk '/^```/ { inb = !inb; print "----"; next } inb { printf "%d|%s|\n", length($0), $0 }' <chapter>`
and
`awk '(NR==213) || (NR>=602 && NR<=613) || (NR>=628 && NR<=636) || (NR>=648 && NR<=657) {printf "%d|%d|%s|\n", NR, length($0), $0}' <RIG>` (pre-#360). Post-#360, the chapter's
fences equal the ARCHIVE spans above (verified by `engineering/tools/verify-example-corpus-identity.py`,
GREEN); RIG is kept as the as-run record (the `sample` routine's `REP` operand differs; the
measuring PASM itself is unchanged).

No harness: the chapter carries no snippet that is not taken verbatim from RIG, so nothing was
compiled for this chapter.

## *Why it happens*: paraphrase basis

Paraphrased from BRF Part 2 ("The claim in one paragraph", "How `TT` bit 0 and `OUT` reach the
pad", "What the pad does with them") and Part 4, at the programmer's-model level: `TT` bit 0 is
the pin's output enable in every smart mode; `OUT` reaches the I/O pin circuit as its output bit
in the DAC smart modes with `TT` bit 1 clear; in the DAC pin state the DAC runs only with the
output enable high and the ADC only with the output enable and output bit both high; with the
output enable low nothing runs. The chapter attributes the account to the study and uses
Parallax's term "I/O pin circuit" (DOC:7868) for what BRF calls the pad. BRF states it read
the four pad facts from a source it does not cite by line; the chapter therefore presents them
only as the study's reading. No HDL fragment, signal name, module name, file name or line
reference from BRF appears in the chapter. "The study left open what the pin's read state
carries ... while the ADC is off" = BRF "What the source does not settle", first bullet; the
measured value (0) is given in the chapter's *What the P2 actually does* and proof table.

## Where the chapter departs from the ledger's wording

- LED:1012, 1021 say "the fast DAC drives the pin". The chapter says "the pin's DAC": "fast DAC"
  is not the P2 Documentation's term at pin level (its one use, DOC:393, is "four fast DAC output
  channels" in an overview list). It
  also says the drive was not observed: nothing was attached (RIG:29, RIG:144–145), so the drive
  rests on DOC:7654 (`x1 = output enabled`) and DOC:7903, not on a measurement.
- LED:1001 states the chip revision. By the brief, the chapter states none.
- LED:1015–1017 give C2 as ranges per run; the chapter gives every sample (L1, L2) and the
  combined range 1,958–2,093.
- LED:1022 "Of the `TT` settings, only `%00` and `%01` were tested; the `OTHER`-enable forms
  (`TT` = `%1x`) were not": carried in *What the P2 actually does*, the workaround's limits and Status.
- The tested `%SSSSS` value: RIG:212–213, 247 and L1:27–28 show `SSSSS=%1` only, i.e. `%00001`
  DAC noise. `%00010` and `%00011` never appear in RIG; the chapter qualifies to DAC noise.
