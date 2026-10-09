# Campaign — 2026-10 P2KB close-out, bench round 1

**Purpose:** settle on real silicon the questions the P2KB close-out study
(`engineering/analysis/2026-10-08-p2kb-close-out-study.md` §5) found that **no ingested source
answers**. Stephen's rule (2026-10-08): "we only do bench runs for things that are not covered in
our ingested source documentation." Group D of the study re-checked the queue against every source
first and killed five questions; these eight programs carry the nine that survived
(`engineering/analysis/2026-10-08-p2kb-close-out-evidence/bench-groupD-recheck.md`).

**Result:** not yet run.

| # | Test (`tests/`) | Row | Question | Pins | Verdict | EF |
|---|---|---|---|---|---|---|
| 1 | `test-vo-s059-xoro-zero-seed.spin2` | VO-J-029 | what `??x` returns with `x = 0`, and `x` after | none | — | — |
| 2 | `test-vo-s037-cogatn-self.spin2` | VO-J-030 | does `COGATN(1 << COGID())` strobe the issuing cog? | none | — | — |
| 3 | `test-vo-g028-hw-stack-overflow.spin2` | VO-J-031 | what a 9th/10th push loses; the stored entry width | none | — | — |
| 4 | `test-vo-s304-pwm-x-zero-fields.spin2` | VO-J-033 | PWM with `X[15:0] = 0` / `X[31:16] = 0` | P4 (never driven) | — | — |
| 5 | `test-vo-j-028-y-written-dir-low-counter-modes.spin2` | VO-J-028, VO-J-034 | does a Y written in reset survive, nine counter/ADC modes; NCO duty with Y = 0 | P4–P6 (P5, P6 driven) | — | — |
| 6 | `test-vo-f372-usb-wrpin-on-running-pair.spin2` | VO-J-032 | a live `WRPIN` drive ↔ sniffer on a running USB pair | P0/P1 (driven) | — | — |
| 7 | `test-vo-j-006-lut-share-block-load-and-spin2.spin2` | VO-J-006 | does a block load propagate through LUT sharing; a Spin2 sender | none | — | — |
| 8 | `test-vo-j-005r-streamer-capture-ceiling-and-skew.spin2` | VO-J-005 | streamer pin-capture ceiling; filter skew | P32–P47 (P32 driven, P36–P47 held low) | — | — |

**Nothing attached.** Every program is bare-board: pins come only from the bench's free set
(P0–P7, P32–P47), and the smart-pin tests route between neighbours through the relative-pin input
selectors. VO-J-032 names one conditional fallback (a second USB pair with jumpers P0→P2, P1→P3)
used only if the bare pair reports INCONCLUSIVE.

**How each was made.** Written by a fresh agent from the recheck's specification and the house
exemplars (`2026-09-p2-errata-predictions/tests/test-so9-dac-mode-adc-enable.spin2`,
`2026-10-kb-findings/tests/test-f526-sync-tx-prime-in-reset.spin2`,
`2026-09-p2-errata-predictions/tests/test-divide-by-zero.spin2`); reviewed adversarially by a
second fresh agent before any run; fixed; the fixes checked by a third. Each prints its
pre-registered readings before measuring, gates its verdict on in-run controls, bounds every wait,
and reports from cog 0 only (`DEBUG_COGS = %0000_0001`). Every configuration word and opcode
quoted in a header was read back from the `pnut-ts -d -l` listing (v1.55.8).

**Where things live.** The `.spin2` sources here are the versioned record and are what runs.
`.bin` files are never committed; build with `pnut-ts -d <file>`. Each run's console log is saved
by Stephen and its result is entered as an `EF-NNN` in `../../P2-EMPIRICAL-FINDINGS.md`, then the
row in `../../VERIFICATION-OPPORTUNITIES.md` is marked `DONE → EF-NNN`. Once accepted, a test file
and its result are frozen.

**What a result decides** is stated on each row in `VERIFICATION-OPPORTUNITIES.md` and in each
program's header (*WHAT IS DECIDED*). The study rows waiting on these results are S-037, S-059,
S-304, S-324 (F-372), S-394, the gaps G-006, G-027 and G-028, and F-386's ten mode pages (VO-J-028).
VO-J-006 also feeds the LUT app-note punch-list item and P2AN007.
