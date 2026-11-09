# Contract-gaps bench campaign, 2026-11-09: results note («#465»)

Campaign folder: `engineering/ingestion/external-sources/hardware-verification/campaigns/2026-11-kb-contract-gaps/tests/`.
One board, bare, nothing attached (pins P0..P2 touched by arm I and arm J only), 200 MHz, built `pnut-ts -d`, 2026-11-09.
Four programs, six logs (git-ignored, in `tests/logs/`), each log reached `=== END ===`.

| Program | Arms | Log | `.bin` (bytes) |
|---|---|---|---|
| `test-contract-gaps-p1-instruction-flow.spin2` | A to H | `debug_261109-123208` (first run, source as committed in `e9d2df58`) | 27,654 |
| `test-contract-gaps-p1-instruction-flow.spin2` | A to H | `debug_261109-124537`, `debug_261109-124618` (re-runs) | 27,638 |
| `test-contract-gaps-p2-cog-lifecycle.spin2` | I to O | `debug_261109-123239` | 22,506 |
| `test-contract-gaps-p3-coginit-no-free-cog.spin2` | P, Q | `debug_261109-123259` | 11,240 |
| `test-contract-gaps-p4-rep-skipf.spin2` | R, S | `debug_261109-123319` | 14,134 |

Since the first p1 log the tracked program changed two things: arm D's expected constant, and its end-of-session line (`debug("DEBUG_END_SESSION")` became `debug(DEBUG_END_SESSION)` under `{Spin2_v52}`). The two re-runs gave the same verdicts as the first run for arms A to C and E to H. Arm D, a RIG FAIL on the first run, was accepted on the re-runs.

## Arms

| Arm | Question | Rig verdict | Accepted reading | EF |
|---|---|---|---|---|
| A | Far `CALLD PA,#label` in hub: field unit | BYTES | Byte offset; the compiler's word (instruction count, −1,006) lands 1,006 bytes back; the hand-encoded byte word lands on its label; far `CALL` control passed | EF-106 |
| B | Backward `DJNZ x,##label`, cog and hub | cog MISSES; hub LANDS ON ITS LABEL | Cog lands in hub at PC plus the field taken positive (`$0004_0004`, predicted and seen); hub lands on its label; controls passed; why the hub lands is not established | EF-107 |
| C | Pending `SETQ` across a cancelled instruction | CONSUMED (false condition and SKIP) | Consumed; the cancelled instruction took it | EF-108 |
| D | `AUGS`/`AUGD` across a cancelled instruction | SURVIVES (all four cases), on the re-runs | The prefix survives a false condition and SKIP, for AUGS and for AUGD; controls and footprints passed. The first run was a RIG FAIL, explained below | EF-123 |
| E | `CALLA`/`RETA`, `CALLB`/`RETB`, `CALLD`/`JMP PA` under SKIP | NOT SUSPENDED (all three) | None suspends the pattern; `CALL`/`RET` control does | EF-109 |
| F | `ALTD`/`ALTS`/`ALTR` past a SKIP-cancelled instruction | DOES NOT APPLY (all three) | Does not apply; classes nothing-between 1, ADD executed 3, ADD skipped 2 | EF-110 |
| G | `_RET_ SETQ2` at the end of an XBYTE routine | LEFT | Q left for the next routine (reads `$A5`) | EF-111 |
| H | `TRGINT1` under `STALLI` | HELD | Held until `ALLOWI`; contradicts the instruction table's "regardless of STALLI mode" read as a branch | EF-112 |
| I | `COGINIT` of running, stopped and own cog | per class; stack OTHER | DIR, OUT, C, Z, skip, REP reset; PA, PB take the image's values; Q reads `$1F7`; LUT and CT1 target survive; the stack is not cleared, the contents of its pops are shown and their cause is not established | EF-113 |
| J | Cog OUT gated by own DIR | GATED (both ways) | Gated | EF-114 |
| K | Which CORDIC read retires | RETIRED / NOT RETIRED / RETIRED | GETQX GETQX and GETQY GETQY advance; GETQX GETQY leaves Y on result 1; X and Y advance independently in the orders measured | EF-115 |
| L | `QDIV` quotient over 32 bits | OTHER (quotient and remainder) | Two cases only: {3,7}/2 gave Q `$FFFF_FFFE`, R `$0B`; {5,11}/4 gave Q `$FFFF_FFFE`, R `$13`; no rule; controls passed | EF-116 |
| M | `GETQX` with nothing pending | STALE; 2 clocks | Last result read, 2 clocks, empty flag set | EF-117 |
| N | `RDLUT`/`WRLUT` `PTRA` unit | LONGS | LUT longs | EF-118 |
| O | `CRCNIB` bit order | Q[31] FIRST | Q[31] down to Q[28] | EF-119 |
| P | `COGINIT(COGEXEC_NEW,...)` with no free cog | READS `$8000_000F` | `$8000_000F` in all five calls, not −1; controls and recovery passed | EF-120 |
| Q | `COGSPIN(NEWCOG,...)` with no free cog | READS `$8000_000F` | As P | EF-120 |
| R | `REP` inside `REP` | INNER REPLACES | Inner replaces; ran in cog RAM only; outer gone, code after runs once | EF-121 |
| S | `SKIPF` in hub execution | REVERTS TO SKIP | Follows the pattern like SKIP, at hub SKIP's time (22 clocks; cog SKIP 22, cog SKIPF 10) | EF-122 |

Nineteen of nineteen arms accepted (eighteen EF entries, EF-106 to EF-123; P and Q share EF-120).

## Arm D: the first run and the re-runs

The first run's verdict line for arm D was `RIG FAIL, a control did not read the augmented value and $1FF`. The rig's expected constant was `($12345 << 9) | $1FF`; the assembler keeps bits 31:9 of the AUG operand, so the augmented control correctly read `$0001_23FF`, and the rig refused its own controls. This was a rig error, not a measurement: the program stopped short of judging the four cancelled-instruction cases, and nothing was drawn from that run's arm D lines. The constant was corrected to `($12345 & !$1FF) | $1FF` and p1 was re-run twice (`debug_261109-124537`, `debug_261109-124618`; `.bin` 27,638 bytes). Both runs gave the same arm D lines: AUGS y `$0001_23FF $0000_01FF $0001_23FF $0001_23FF`, AUGD y the same, the four cancelled-instruction footprints all `$0000_0000`, and the four verdicts SURVIVES. Arm D is accepted on the re-runs as EF-123.

## End of session

On these runs pnut-term-ts v1.1.1 did not end the session for either form of the program's last line:

- `debug("DEBUG_END_SESSION")` (the first p1 log and the p2, p3 and p4 logs): it arrived as the text line `Cog0  DEBUG_END_SESSION`.
- `debug(DEBUG_END_SESSION)` with `{Spin2_v52}` (the p1 re-runs): it arrived as `Cog0`, two spaces, `$1B`, CR LF, and the logger wrote `[ROUTING ERROR: Binary data in COG message]`.

The cause is not established. No verdict depends on it: every log reached `=== END ===` before the line.

## Notes carried into the KB work

- Arms H and S contradict wording in an instruction table or document: both are stated in the ledger as the measured fact with the sources' wording named, as "Parallax's documents also give ...".
- Arm P/Q (EF-120): `$8000_000F` is negative as a signed long and no cog ID is; `$FFFF_FFFF` is a different value. Example code that tests `== -1` on these calls is wrong on this reading; the replacement test (on bit 31, or `< 0`) rests on this measurement and must be compiled.
- Arm I (EF-113): the stack is not cleared; the extra values `$C000_0059`, `$C000_005F` and the leading 0 come from no instruction in the image, and what wrote them is not established.
- Arm B (EF-107): why the hub landing reaches its label is not established; the rig shows the landing and the field only.
