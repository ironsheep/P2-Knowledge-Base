# Changeset-Integrity Audit — p2-assembly-language-manual

**Adversarial, fresh-eyes audit of the diff since last public release. Read-only.**

## 1. Header

- **Manual:** p2-assembly-language-manual
- **Baseline tag:** `p2-assembly-language-manual-v3.1.2` (commit `1095b42c`)
- **HEAD:** `60d0a18a`
- **Diff scope:** `git diff p2-assembly-language-manual-v3.1.2..HEAD -- .../p2-assembly-language-manual/`
- **Files:** 9 · **Hunks:** 66 · **~235 insertions**
- **Commits behind it:** `44215509` (audit-methodology/descriptor upgrade), `f3e702ed` (class-wide correctness sweep A — the Part-I fabrication fixes), `98efcf9b` (operator-notation `=`→`==` sweep-B).
- **No CHANGELOG hunk** — version bump / promotion deferred to the coordinated release sweep, consistent with the descriptor's "IN FLIGHT / content bump" note and all three commit messages ("no version bumps, no re-render").

**Bottom line:** CLEAN. This is a genuine fabrication-audit correction pass. Every substantive hunk traces to a Tier-1 source (Silicon Doc v35 / PASM2-in-brief CSV / instruction YAML / Spin2 v51/v55) or to empirical EF-033/EF-034, and it correctly *removes* multiple fabrications shipped in v3.1.2. No hunk contradicts an EF or a verbatim encoding. Two items worth a follow-up edit (one cross-chapter naming inconsistency the changeset introduces; one reasoning-derived timing nuance) — neither blocks release.

## 2. Traceability table

| File(s) | Hunk summary | Traced source | Verdict | Note |
|---|---|---|---|---|
| MANUAL-DESCRIPTOR.md | fragile_areas += Ch.3/Ch.4 narrative, operator-notation, "Part I never claim-audited"; `last_published_tag` v3.1.1→v3.1.2; "IN FLIGHT" changeset baseline | tag history (v3.1.2 released 07-04); self-describing | faithful | Build metadata, not reader-facing. Tag correction verified. |
| creation-guide.md | +§4A.8 "prose/examples ARE claims"; red-flag phrases (parallel/pipelined/"C indicates edge case"/cycle-vs-instruction); operator-notation table | methodology §5.4/§6.4; mirrors the actual fixes below | faithful | Process plumbing (appropriate location). |
| ch01 | COGINIT: param via preceding SETQ → new cog **PTRA**; code addr → **PTRB** | coginit.yaml + Silicon Doc ("Src→PTRB; prior SETQ→PTRA") | faithful | Old text ("parameter appears in PTRB") was wrong. |
| ch01 | LUT: WRLUT(2)=cog-reg speed, RDLUT(3)=1 clk slower | Appendix A (RDLUT 3, RDLUT/WRLUT); self-consistent | faithful | Corrects "both slower than cog reg." |
| ch01 | Hub-control timing "+ (LOCKNEW takes 4-11)" | PASM2-in-brief CSV: "LOCKNEW … 4…11" | faithful | Verified verbatim. |
| ch02 | DIRZ/DIRNZ encoding table Z-effect `---`→`DIRx` | dirz.yaml ("C and Z updated to original DIR bit"; z: DIR bit) | faithful | Encoding-table correction verified. |
| ch02 | ALTD D-field: "Hub addresses"→"indirect Cog/LUT register addr, masked $1FF, not 20-bit Hub" | Silicon Doc (D field = 9-bit reg addr) | faithful | Removes a wrong claim. |
| ch02 | **AUG "must immediately precede" rewrite** → augment attaches to next matching `#S`/`#D`; survives non-matching intervening ops; ALTx-with-immediate gotcha | **EF-033** (survives intervening — "must immediately precede" CONFIRMED-FALSE) + Silicon Doc KNOWN-BUGS (ALTx #S steals AUGS) | faithful | Matches EF exactly, not the old myth. The ALTx caution is verbatim from Silicon Doc bug list. |
| ch02 | AUG timing example `wrlong ##,##` 6→"7…14 (AUGD+AUGS +4; WRLONG 3…10)" | WRLONG 3…10 (Appendix A) | faithful | |
| ch02 | Operator-precedence tables reordered: `^` before `\|`; `* / //` before `+ -`; `<=>` moved into Comparison group | Spin2 v51 precedence: `&`4 `^`5 `\|`6 `*`7 `/`8 `+`9 `-`10 `<=>`12 | faithful | Reorders now reflect real precedence. |
| ch02 | `#\label` "Cog-relative"→"absolute (non-PC-relative)"; drop `$$` row; `$` = current assembly addr (ORG→Cog / ORGH→Hub) | Spin2 v55 (`$` current addr; ORGH=hub-exec). No `$$` token exists. | faithful | `$$` was fabricated; removal correct. |
| ch03 | ADDX/ADDSX Z detail; CMPX/CMPSX "Z AND (D==S+C)" | Appendix A rows; CSV | faithful | |
| ch03 | TEST* group corrected: extended effects = TESTB/TESTBN/TESTP/TESTPN; TEST/TESTN carry full WCZ | Appendix A (TEST/TESTN CZ; TESTB… CZI) | faithful | Fixes over-generalized "TEST*". |
| ch03 | Cycle counts: "3 clocks"→"6 (3×2)"; branch 2/4→6/8; conditional-inc 2→4 | Silicon Doc pipeline ("each instr ≥2 clk; cancelled still 2; taken branch ≥4") | faithful | Cycle-vs-instruction-count class fix. rdlong→mov/add in example avoids the hub-timing confound. |
| ch03 | **ABS branchless fabrication fix** — abs is single-instr; C = source's sign (every negative), NOT "indicates edge case"; `abs wc`+`if_c neg` with no work returns `value` | abs.yaml ("C set if original value negative; C: S[31]") | faithful | The prior "C flags the exceptional case" was the flagged fabrication. |
| ch03 | Logic table: NOT carved out as exception (C=!S[31], not parity) | Appendix A (NOT C=!S[31]) | faithful | |
| ch03 | ADDS/SUBS C = true sign, = stored bit31 "only when no signed overflow" | CSV ("C = correct sign of D+S") | faithful | Accurate nuance. |
| ch03 | State-machine example `if_z jmp`→`if_nz jmp` (+ Z-polarity prose) | TEST …wz sets Z=1 when (D&S)=0 i.e. bit *clear* | faithful | Old code branched on the wrong polarity. |
| ch03 §3.4 | +notation paragraph (`==` compare vs `=` state) | notation rule | faithful | Math notation, not KB plumbing. |
| ch04 | PLL example ×16/2→×8/2 (=80 MHz, VCO 160) + VCO explanation | self-consistency (old VCO 320 broke the stated 100-200 range) | faithful | Both arithmetically valid; new is internally consistent. |
| ch04 | HUBSET clock-switch literals + `CC`/`SS` field comments | CLK format `…PPPP_CC_SS`; bit values decode correctly | faithful | Ch4 naming (CC=caps, SS=source) is the standard nomenclature. |
| ch04 | "automatic fallback to RCFAST" removed → no runtime failsafe | Silicon Doc (no clock-fail monitor; RCFAST = reset default only) | faithful | Removes a fabrication. |
| ch04 | WAITX = 2+D clocks (waitx ##100 = 102) | WAITX +2 base | faithful | |
| ch04 | Cycle table Hub 2-16+ → 9…16 read / 3…10 write | CSV / EF-034 | faithful | |
| ch04 | **WAITATN rewrite** — ATN is cog-to-cog (raised by COGATN), NOT a smart-pin flag | Silicon Doc events (ATN = attention from another cog) | faithful | Prior "any pin low-to-high / smart pins set ATN" was a fabrication. |
| ch04 | JSE/JNSE → JSE1-4/JNSE1-4 | instruction naming | faithful | |
| ch04 | **§4.6.2 "Pipelined Hub Access" fabrication removed** — scalar RDLONG blocks the pipeline; only FIFO/SETQ-burst/CORDIC hide latency; misleading overlap code deleted | **EF-034** (scalar RDLONG ~15-16 clk blocks) + Silicon Doc (stalled instr stalls pipeline) | faithful | The flagged §4.6.2 RDLONG-parallelism fabrication. |
| ch04 | WS2812 `test data,#31 wc`→`testb data,#31 wc` | TEST computes D&31 (masks low 5 bits); TESTB tests D[31] | faithful | Old code did NOT test bit 31 — assembles to wrong behavior. Good catch. |
| ch04 | GETCT measurement overhead 4→2 cycles (2nd GETCT samples at start) | reasoning; not tied to a cited EF | introduces-new-claim | See FLAG 2. Analytically the *more* defensible value; low-risk timing nuance. |
| ch04 | Hubexec table Hub 2+wait → RDLONG 9…16 / 9…26; keyconcepts branch-refill not per-instr fetch | CSV; Silicon Doc (hubexec seq matches cog via FIFO; taken-branch ≥13) | faithful | |
| ch05 | QEXP "e^x"→"base-2 2^x (inverse of QLOG)" | zerox.yaml/CSV ("QEXP: logarithm-to-number"; QLOG base-2) | faithful | Removes wrong e^x claim. |
| ch05 | CORDIC early-read: "undefined values"→"cog stalls until ready; undefined only if no op in progress" | §5.1.5 self-consistency; Silicon Doc (GETQX stalls) | faithful | |
| ch05 | POLLQMT/QMT rewrite — QMT = flag set *after* a premature GETQX/GETQY, cannot forecast readiness; misleading poll-before-read code removed | Silicon Doc ("event 15 when GETQX/GETQY executes w/ no result"); event-table change | faithful | Prior "C=1 if pipeline empty, poll before read" was a fabrication. |
| ch05 | Event table INT1/INT2/INT3 → single **INT** ("any of 3 levels, source via SETINTx") | Silicon Doc 16-event set (single INT flag; INT1/2/3 are levels, not separate events) | faithful | |
| ch05 | XRO "Streamer rollover"→"NCO rollover (phase-accum overflow)"; QMT desc | Silicon Doc streamer NCO | faithful | Refinement. |
| ch05 | **Interrupt priority inverted** → INT1 highest (interrupts 2&3); INT3 lowest (only normal code) | Silicon Doc part3-interrupts: "INT1 highest… INT3 lowest, only non-interrupt code" (verbatim) | faithful | Old text had priority backwards. |
| ch05 | Boot table row `pull-up \| none \| none` → `pull-up \| any \| none` | BOOT-PROCESS-COMPLETE (⇧ \| ⨯ \| ƒ) | faithful | P60 is don't-care; correction verified. |
| ch05 | **SD Card Boot** pin table P61 CS/P60 CLK → **P61 CLK / P60 CS** | Datasheet image catalog (SD: "CD/CS→P60, CLK→P61") | faithful | Baseline SD table wrongly duplicated the *flash* roles; fix matches SD wiring. (SPI-flash table left = P61 CS/P60 CLK, also correct.) |
| ch05 | §5.7.6 clock-config code rewritten to one enable + one switch; `%..._XX_CC` field comment | bit values decode correctly | overstates-source (naming) | See FLAG 1 — VALUES correct, field NAMES contradict Ch4. |
| ch05 | RCFAST "~20-30 MHz"→"20 MHz+ (nominally ~24)"; XBYTE clock-1 annotation | RCFAST ~20-24 nominal | faithful | Minor. |
| ch05 | DEBUG multi-cog prefix "Cog0: … Cog7:" → "`Cog0 `…`Cog7 `, no colon" | Spin2 v55 output (ex-119.spin2: `Cog0  i = 0`) | faithful | Colon form was wrong. |
| ch06 | AUG timing 6→7+; hub timing split read(9-16)/write(3-10) | CSV; mirrors ch1/ch4 | faithful | |
| appendix-a | ~90 Z-column predicates `Result = 0`→`Result == 0`, `D=S`→`D == S`, `(D=0) OR (S=0)`→`==`, `(D&S)=0`→`==`; +legend bullet | notation rule; harmonizes with rows already `==` (ADDX/CMPR/CMPSX/CMPX) | faithful | Pure notation. Correctly leaves assignment `=` (INCMOD `C = 0`, SUMC `D = D-S`) and relational `=>`/`<` untouched. No semantic change. |

## 3. Flags

Two items. Neither contradicts an EF or a verbatim encoding; neither is a fabrication.

### FLAG 1 — Cross-chapter clock-config field-name inconsistency (introduced by this changeset)
- **Claim (Ch5 §5.7.6):** config word `%1_DDDDDD_MMMMMMMMMM_PPPP_XX_CC`, where `XX` = 15pF caps and `CC` = clock source (`%00` RCFAST / `%11` PLL).
- **vs Source / vs Ch4:** the standard P2 CLK register layout is `…PPPP_CC_SS`, where **CC** = XI/crystal pin config (caps/drive) and **SS** = clock-source select. Ch4 §4.1.4 — changed in the *same* changeset — uses exactly `CC`/`SS`. So within one release, `CC` names the source-select field in Ch5 but the caps field in Ch4.
- **Failure scenario:** an agent/reader decoding the config word cross-references the two chapters and finds `CC` meaning two different bit-fields → mis-decodes a hand-built HUBSET literal. **Mitigant:** the actual bit *values* in both Ch5 HUBSET literals decode correctly (`…_10_00` = caps %10 + RCFAST; `…_10_11` = caps %10 + PLL), so anyone *copying the literals* assembles correctly — the risk is only in *decoding via the field names*. Recommend relabeling Ch5 to `PPPP_CC_SS` to match Ch4 and the Silicon Doc.

### FLAG 2 — GETCT measurement-overhead value is reasoning-derived, not source-cited
- **Claim (Ch4 §4.5):** two-GETCT timing reports N+2 (a 10-cycle span reads 12), because "the second GETCT samples the counter at the start of its own execution, so its 2 cycles fall outside the interval." Changed from the prior N+4 (=14).
- **vs Source:** no cited EF or verbatim source pins the GETCT sample-point within its 2-clock execution; the prior 4-cycle figure was equally unsourced.
- **Assessment:** analytically the new value is the *more* defensible one (the two GETCTs jointly contribute exactly one instruction's 2 clocks to the measured interval), so this raises correctness. Treated as `introduces-new-claim` only on the strict "trace to a source" test. **Failure scenario:** a reader trusting the exact 2-cycle figure for a tight cycle budget where the true sample-point differs. Low risk. Nice-to-have: ground it in a GETCT timing EF if one is ever run.

### Explicitly checked and found NOT to be problems
- **AUG rewrite** does not resurrect any "immediately precede" myth — it matches EF-033 (survives non-matching intervening ops) and the ALTx-#S caution is verbatim Silicon Doc.
- **SD Card boot pin swap** initially looked like it might have flipped the *flash* roles to wrong — it did not; it fixed the *SD* table (baseline had SD wrongly duplicating flash), and the flash table is unchanged and correct.
- **Appendix `=`→`==` sweep** does not touch any assignment or relational `=` — only equality predicates in the Z column; no encoding or effect semantics change.
- **WS2812 test→testb** is a real behavioral correction (TEST masked the low 5 bits, never touching bit 31).

## 4. Bottom-line recommendation

**Release-ready pending one trivial edit.** The changeset is a high-quality, well-sourced correction pass that removes at least seven fabrications carried in v3.1.2 (RDLONG "parallel" §4.6.2, ABS "C indicates edge case" §3.5.4, WAITATN smart-pin ATN, inverted interrupt priority, QEXP e^x, POLLQMT forecast-usage, cycle-count-as-instruction-count) plus several encoding/timing corrections, every one traceable to Silicon Doc v35 / PASM2-in-brief CSV / instruction YAML / Spin2 v51/v55 or empirical EF-033/EF-034. No scope-creep, no `traces-to-nothing` hunk, no contradiction of any EF or verbatim encoding.

Recommended before tag:
1. **FLAG 1** — relabel the Ch5 §5.7.6 clock-config comment fields from `XX_CC` to `CC_SS` to match Ch4 and the Silicon Doc (values already correct).
2. **FLAG 2 (optional)** — annotate the Ch4 GETCT overhead as an analytical estimate, or ground it in a timing EF.

Given the manual's "content bump, coordinated release" posture, both can fold into this same pre-release pass with no re-audit gate concern.
