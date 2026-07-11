# Changeset-Integrity Audit — p2-io-and-smart-pins-user-guide

**Audit date:** 2026-07-11
**Mode:** Independent adversarial delta-since-last-release audit (read-only). Fresh eyes; each hunk tested for *disproof*, not assumed correct.

## 1. Header

- **Baseline tag:** `p2-io-and-smart-pins-user-guide-v1.0.4` (`a3528cbb`)
- **HEAD:** `60d0a18a`
- **Diff scope:** `git diff p2-io-and-smart-pins-user-guide-v1.0.4..HEAD -- .../p2-io-and-smart-pins-user-guide/`
- **Files changed:** 33 (24 opus-master `*.md` chapters/appendices/front-matter, 8 loose `examples-library/*.spin2`, 1 tracked `examples-library.zip`). **CHANGELOG.md and examples-library/README.md were NOT changed** (verified empty diff).
- **Commits (4):** `f3e702ed` (Fabrication-audit §6 correctness sweep — 342 doc fixes across 13 docs, DOC-ONLY), `ce26d1e5` (§12.3 P_LOGIC_* rework, C-65 residual), `a072ac48` (example-corpus reconcile to opus-master, identity GREEN), `ffd7dbf0` (regenerate tracked zip from GREEN loose files).
- **Hunks enumerated:** ~120 text hunks across the 24 md files + 8 example diffs + 1 binary zip regenerate. Every hunk was matched to a source.

**BOTTOM LINE: CLEAN.** Every hunk traces to a Tier-1 source (Spin2 v55 verbatim text, Silicon Doc, v35 instruction CSV) via the change-first catalog `engineering/planning/FABRICATION-AUDIT-SWEEP-CATALOG.md` (148 IOSP rows, each carrying a source-line proof) or to the corrections register (F-173, F-202, C-65). All 8 changed examples compile clean under `pnut-ts -d` and are byte-identical to their manual code blocks. No `traces-to-nothing`, no `overstates-source`, no `introduces-new-claim`. Direction of change is consistent with the domain guidance (over-precise numbers softened; genuine errors fixed against source). **One release-readiness note only:** this unreleased sweep has no CHANGELOG entry yet.

## 2. Traceability table

Hunks grouped by finding-class (identical repeated hunks confirmed identical before grouping — e.g. the six `P_ADC_GIO→P_ADC_1X` sites, the six `PINFLOAT→PINHIGH/PINLOW` pull sites, the `M[12:10]` re-letterings).

| File(s) | Hunk summary | Traced source | Verdict | Note |
|---|---|---|---|---|
| ch16-adc.md (×6), ch16 example (loose+zip), appendix-e | `P_ADC_GIO`→`P_ADC_1X`/`P_ADC_FLOAT`; GIO reframed as internal ground/calibration node reading ~0 | Catalog C-03/C-26 (spin2-v55 L1466 `P_ADC_GIO → IN`); reg **F-173, F-202**; empirical ADC wave | faithful | Empirical-grounded; removes the "GIO reads the pin" error |
| ch12 (×6 sites), ch07/ch12 examples | `PINFLOAT(pin)` after `P_HIGH_15K`/`P_LOW_15K`→`PINHIGH`/`PINLOW` (keep DIR driving for internal pull) | Catalog C-02 (6 sites); pin-drive semantics | faithful | Real behavioral bug fix; PINFLOAT would disable the pull |
| ch12 §12.3, appendix-b(quick), ch12 example | P_LOGIC_A / P_LOGIC_A_FB / P_LOGIC_B_FB two-axis rework; "OUT feedback"→"output driven by OUT" | Catalog **C-65** (spin2-v55 L1456-1458); commit ce26d1e5 | faithful | Dissolves false "same, different routing" |
| appendix-b | A/B input tables split into polarity (bit 31/27) + selection (bits [30:28]/[26:24]) | Catalog C-XX L404-411 (invert is independent field); Silicon Doc WRPIN format | faithful | Old `%1000` conflation corrected |
| ch03 | Layer-3 input routing `[31:24]`→`[31:21]`; add per-field bit ranges | Catalog C-XX L894-896 (Silicon `%AAAA_BBBB_FFF...`, FFF=[23:21]) | faithful | |
| front-matter | "mode bits [4:0]"→"%SSSSS field bits [5:1], bit 0 separate" | Same WRPIN-format source (`...SSSSS_0`) | faithful | |
| ch11 (×3), ch17 | Fractional field X[15:10] "honored only when X[31:26]=0 (<1024 clocks)"; error tables corrected | Catalog C-53/C-124/C-125/C-126 (Silicon Doc L~9089 verbatim) | faithful | Removes over-optimistic <0.001% claim; well-sourced |
| ch11, ch17, ch11 examples | `REV 8`→`REV 7`, `REV 32`→`REV 31`; PASM `rev`→`shl #32-8` then `rev` | **spin2-v55 L448** ("Reverse bits 0..y"); Catalog L1884-1886 (Silicon L~9061 SHL-then-REV) | faithful | Verified against source; old forms were genuine bugs |
| ch08 (md + loose + zip) | `PINLOW(PHASE_A..PHASE_C)`→`PINLOW(PHASE_C..PHASE_A)` | Catalog L1944-1946 (spin2-v55 L385-393: range is Top..Bottom, wraps if Top<Bottom) | faithful | Real bug: 10..12 wrapped to a 31-pin field |
| ch08, ch10 examples/md | `43691`→`43690` (65536*2/3 truncates) | Direct arithmetic (=43690.67) | faithful | Verified |
| ch11, ch17 | `10417`→`10416` (200e6/19200) | Direct arithmetic (=10416.67) | faithful | Verified |
| appendix-c | `143165`→`143166` (freq×2³²/300e6) | Direct arithmetic (=143165.6, round-to-nearest, matches column convention) | faithful | Verified; was lone truncated outlier |
| ch06 | "Maximum Toggle Rate" relabeled; add REP form = 2 clk/toggle = 100M/s = 50 MHz sq | Catalog **C-31** (Silicon Doc L1710-1717 "2 clocks per toggle"; CSV DRVNOT=2, JMP=4) | faithful | New 50 MHz figure is sourced+computed |
| ch09 | PWM frame >65535 overflow: add `base` grow-loop; motor-resolution recompute | Catalog C-25 (16-bit X[31:16] field limit) | faithful | Old frame=100,000 exceeded field |
| ch10 | BIT_DAC nibble requirement (`\| $F0<<8`); DAC reset-state scoped to dithered modes | Catalog C-18, C-XX (BIT_DAC drives two 4-bit levels) | faithful | Real: unset nibbles → 0V, no output |
| ch14, appendix-d, appendix-f | Mode-constant name fixes: P_COUNT_HIGHS→P_REG_UP (gated freq); step/dir→P_REG_UP_DOWN | Catalog C-14 | faithful | |
| ch18 (×several), appendix-f | Repository: "hardware-arbitrated"→conflict-free reads/last-writer-wins; `P[12:10]`→`M[12:10]`; DAC dithering scoped | Catalog C-20; register-letter convention | faithful | Removes fabricated "arbitration" |
| ch19 (×4), ch19 example | Add `WRPIN(USB_DP,...)` — configure both pins of pair | Catalog C-06 (4 sites) | faithful | Real omission |
| appendix-e | DIR/OUT read via DIRA/OUTA not PINREAD/INA; RDPIN masks bit31; X=0 mode-specific | Catalog C-21, C-XX | faithful | |
| ch01 | PINH/PINL alias list 3→6; PINCLEAR = DIRL then WRPIN #0; TESTP flag one-per-instr | Catalog L560-561, L1934-1936/L2524-2526 (**spin2-v55 L538** "DIR=0, then WRPIN=0"); TESTP WC/WZ mutually exclusive | faithful | |
| ch02 | PINCLEAR vs WRPIN(pin,0) not equivalent; P_ constant field narrative | spin2-v55 L538; Silicon WRPIN format | faithful | |
| ch04 | RDPIN/RQPIN same-Z / neither-resets; AKPIN Spin2 exists; span WRPIN/WXPIN/WYPIN/AKPIN only; Serial-RX C = MSB | Catalog (smart-pin RDPIN/RQPIN + AKPIN semantics) | faithful | |
| ch05 | P_EVENTS_TICKS watchdog behavior; windowed-mode "minimum window" | Ch13 mode ref; v1.0.1 hw-verified lineage | faithful | Refines prior HW-verified guidance |
| ch07 | Retrigger (non-zero Y at next base period); STEP_HIGH→STEP_LOW; Y range 1..2³²-1 | Catalog (P_PULSE X[31:16]=low-time compare); pulse-mode semantics | faithful | |
| ch13 | Add CON FREQ_PIN; hub-addr via PTRA; MULDIV64 1000→500 edges; AKPIN in watchdog | Catalog C-13 (label-addr-as-immediate); edge-count math | faithful | |
| ch15 | MULDIV64 vs plain-`/` scoping; Z max $80000000; concurrent-measure both-input routing | Catalog C-XX (§15.2 own plain-`/` usage); v1.0.1 concurrent-measure lineage | faithful | |
| ch16 | SINC3 "doubling over simple bit-summing"; SETSCP before GETSCP; scope = single-channel aggregable | Catalog C-23; Silicon SETSCP/GETSCP | faithful | |
| appendix-c/d/f | Sample-exponent range, SINC2 2-14 bits, mode-name + register-usage corrections | Catalog C-14/C-23 + register refs | faithful | |
| examples-library.zip | Binary regenerate from GREEN loose files | Verified: unzip content == loose files (ch08 spot-check identical) | faithful | Commit ffd7dbf0 |

## 3. Flags

**None.** No hunk earned `traces-to-nothing`, `overstates-source`, `understates-source`, or `introduces-new-claim`.

Adversarial probes that specifically *failed to disprove* a hunk (i.e. the hunk survived scrutiny):

- **The added hard number (ch06 "50 MHz square wave / 100M toggles/s").** New quantitative claim → demanded a source. Found: Silicon Doc L1710-1717 ("2 clocks per toggle") + CSV instruction timings (DRVNOT=2, JMP=4); arithmetic 200 MHz ÷ 2 clk/toggle = 100M toggles/s = 50 MHz square wave verified. Sourced, not fabricated.
- **`REV 8`→`REV 7` / `REV 32`→`REV 31`** (an off-by-one that an agent copying the code would inherit). Verified directly against spin2-v55 L448: "`x REV y` — Reverse order of bits 0..y". 8 bits ⇒ `REV 7`. The *old* code was the bug; the fix is correct and compiles.
- **`PINLOW(PHASE_A..PHASE_C)` reversal** (looked like a cosmetic swap). It is a real functional bug: Spin2 pin-range is Top..Bottom and *wraps* when Top<Bottom (spin2-v55 L385-393), so 10..12 was a 31-pin wrapped field, not pins 10-12. Fix restores the intended 3-pin field.
- **P_ADC_GIO behavioral reframing** (electrical claim → needs empirical/verbatim, not reasoning). Grounded in reg F-173/F-202 and spin2-v55 L1466; consistent with the manual's own v1.0.4 ADC/hardware wave.
- **Fractional-baud `<0.001%`→"ignored at this baud"** (a hunk *removing* an over-precise claim — expected-faithful per domain guidance). Confirmed: Silicon Doc L~9089 verbatim gates X[15:10] on X[31:26]=0; at 115200@200MHz the period is 1736 clocks (≥1024) so the fractional bits are ignored. Faithful.

Concrete failure scenario checked and **not** found: an agent copying any changed example getting wrong hardware behavior. All 8 examples compile under `pnut-ts -d` and are byte-identical to their manual fenced blocks (ch08, ch11 spot-checked line-for-line; zip content matches loose files).

## 4. Bottom-line recommendation

**Approve the changeset as delta-clean.** This is a documentary/empirical *correctness* sweep whose every hunk is anchored to a Tier-1 source through an unusually rigorous change-first catalog (per-change source-line proofs) plus the corrections register. The edits move the manual strictly toward higher fidelity: they remove fabricated capability claims ("hardware-arbitrated," "OUT feedback," "Maximum toggle rate"), fix genuine code bugs (REV off-by-one, PINLOW range-wrap, PINFLOAT-kills-pull, missing USB upper-pin WRPIN, PWM frame overflow), correct arithmetic (43690 / 10416 / 143166), and soften unsourced precision to sourced qualitative statements — exactly the direction the domain guidance predicts as faithful.

**One release-readiness action (not a correctness flag):** the changeset is intentionally unreleased (commit f3e702ed: "No version bumps, no re-render — deferred to coordinated release"). CHANGELOG.md still ends at v1.0.4 and does not describe these ~148 IOSP changes. Before this ships, a new CHANGELOG entry (v1.0.5) must be authored and the manual re-rendered. Until then, no integrity concern — the sources and code are sound.
