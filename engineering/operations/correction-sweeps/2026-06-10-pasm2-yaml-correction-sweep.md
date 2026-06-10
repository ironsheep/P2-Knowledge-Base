# P2KB Correction Sweep — Full Change Report (2026-06-10)

**Head:** `yaml:p2kb` · **Source register:** [`P2KB-CORRECTION-FINDINGS.md`](../P2KB-CORRECTION-FINDINGS.md) · **Date:** 2026-06-10

This report documents every change made in the 2026-06-10 P2 Knowledge Base correction sweep: what was wrong, **how each fix was verified, the primary source(s) that proved it correct**, the fix applied, and why. It is the human-readable companion to the append-only findings register — the register carries the original suspicion and proposed correction, this report carries the *verification evidence and applied outcome*.

---

## 1. Scope & outcome

Every open finding in the correction register was resolved: **F-021, F-023, F-026–F-100**, plus one new finding **F-101** surfaced and fixed mid-sweep.

| Metric | Value |
|---|---|
| Findings resolved | ~79 |
| Applied (DONE) | ~73 |
| Refuted (WONTFIX) | 3 — F-002, F-036, F-093 |
| Fabrications removed | 2 — NEXTN/QUITN (F-098), setxfrq 64-bit (F-023) |
| `deliverables/ai/P2/` YAMLs edited | ~50 |
| Tooling fixes | `gen-pasm2-encoding-reference.py` (F-047, F-081) |
| Regenerated | `PASM2-ENCODING-REFERENCE.md` |

**Verification gates passed:** tree-wide YAML format **1045/1045 clean**; cross-reference validator **100% (0 unresolved)**; encoding-reference regenerated and spot-checked (Flags column corrected on the 344 rows that previously showed a bogus `C,Z`).

---

## 2. Methodology — how findings were sourced and verified

**Where the findings came from.** F-026–F-097 were surfaced by the PASM2 Assembly-Language Manual full audit (50 per-section auditors + 208 per-finding adversarial verifiers). They were filed `NEEDS-VERIFICATION`: the manual-audit evidence was strong, but the **YAML is our primary source of truth**, so each had to be independently re-confirmed against primary authorities *before* editing. F-098–F-100 came from the Spin2 v55 delta-ingestion conflict audit (already compiler-probed twice). F-021/F-023 were pre-existing streamer / SETXFRQ items.

**The verification pass.** Findings were worked in 3 throttle-safe waves of ~25 via a bounded verification workflow. Each agent did **research only** (no file edits): it read the finding, opened the target YAML, and independently checked the cited claim against primary authorities — reading the actual source lines and running compiler boundary/assembly probes where a claim was compilable. It returned a verdict (CONFIRM / REFUTE / PARTIAL / CANT_VERIFY) with the exact proposed edit, the sources it checked, and any compiler probe. **The orchestrator reviewed every verdict, re-ran the high-impact probes directly, reconciled overlapping findings, and applied each fix** via the `yaml-knowledge-base-maintenance` discipline (surgical edits, timestamped backups for files >100 lines, no cross-reference deletions).

**Authority order (by fact type):**

1. **`pnut-ts` compiler** — ground truth for what assembles, error text, flag / version-gate behavior, and encoded bit patterns (EEEE-bit inspection, divide-by-zero constant oracles, fill-to-boundary probes).
2. **`spin2_lang_ref_v55`** — Spin2 language + assembler-directive semantics (matched-compiler edition).
3. **Silicon Doc** (`silicon-doc/p2-documentation.txt`) — silicon encodings, bit fields, errata.
4. **P2 Instructions CSV** (`p2-instructions-csv`, v35 Rev B/C) — per-instruction encoding, flags, timing.
5. **P2 Datasheet** (`p2-datasheet`) — electrical / AC characteristics.
6. **Chip Gracey clarifications** — designer notes.

> **Verify-before-publish rule.** Every numeric or encoding claim going into the golden KB was confirmed against a primary source or a compiler probe *before* the edit was applied. Where a claim could not be verified from in-repo golden sources, the unverified content was omitted rather than shipped with a caveat (e.g. the FILE 253-character filename limit was dropped).

---

## 3. Verification highlights — high-impact claims re-proven before publishing

| Claim | What was proven | How verified / source |
|---|---|---|
| ORG auto-limits | bare `ORG` limit `$1F8`; `ORG <$200` -> limit `$200`; `ORG >=$200` -> limit `$400` | `pnut-ts` fill-to-boundary probes (`long 0[N]` until 'Cog address exceeds limit') |
| `IF_NEVER` encoding | assembles to `EEEE=%1111` (always), NOT `%0000`; `%0000` is the `_RET_`/NOP slot | compiled `if_never add 0,0` and read top 4 bits = `%1111`; identical to bare / `if_always` |
| Chip reset | `HUBSET ##$1000_0000` (D[31:28]=%0001), NOT `$8000_0000`; D[31]=PRNG seed | Silicon Doc :6038 / :6465 / :6468 |
| GETCT counter | 64-bit; `GETCT WC` returns upper 32 bits | CSV row 260: 'Get CT[31:0] or CT[63:32] if WC ... GETCT WC + GETCT gets full CT' |
| ADDS/SUBS C flag | `C = correct sign of result`, NOT signed overflow / borrow | CSV rows 12/16: 'C = correct sign of (D +/- S)' |
| XBYTE/EXECF LUT entry | address = `D[9:0]`, SKIPF pattern = `D[31:10]` (was reversed) | Silicon Doc :1913 |
| XI input max | direct-drive into XI = **200 MHz** (350 is the VCO/1 overclock ceiling) | P2 Datasheet AC table (table-reconstruction-notes :508) |
| HUBEXEC constant | `$20` (`%10_0000`) | `pnut-ts` divide-by-zero oracle `1/(HUBEXEC-$20)` -> 'Divide by zero' |
| QLOG / QEXP | QLOG = base-2 log in 5:27 fixed-point; QEXP = 2^D | Silicon Doc :7287–7288 |
| DEBUG_MASK / DEBUG[N] | ungated — no `{Spin2_v46}` directive required | compiled clean with `pnut-ts -d`, no directive |
| NEXT/QUIT level | range 1-15, counts OUTWARD (bare=current loop, `N`=Nth-outer loop); ungated | `pnut-ts`: `next 16`->'must be 1 to 15'; nesting probes; `quit 1` at `{Spin2_v41}` compiles |
| ORGH | limit param + `$100000` ceiling; bare-ORGH default `$400` (Spin2+PASM) vs current-hub (PASM-only) | `pnut-ts` m361/m372 ceiling errors; Spin2 v55 spec §322/§326/§327 |

---

## 4. Per-finding detail

Grouped by theme. Each entry lists the affected files, the fix applied, how it was verified, the primary source(s) that proved it, and the rationale. The original suspicion and proposed correction for each finding are in the register.

### Spin2 v55 conflict-audit findings (compiler-probed twice; applied directly)

#### F-098 — `NEXT`/`QUIT` level: fabricated `NEXTN`/`QUITN` keywords + wrong range + inverted semantics + over-claimed gate  ·  `DONE`

_Applied directly from the register's pre-confirmed evidence (Spin2 v55 conflict audit, compiler-probed twice). See the register entry for full per-fact verification._

#### F-099 — `debug-end-session.yaml` invents a mechanism AND omits the real documented behavior + purpose  ·  `DONE`

_Applied directly from the register's pre-confirmed evidence (Spin2 v55 conflict audit, compiler-probed twice). See the register entry for full per-fact verification._

#### F-100 — `movbyts.yaml` gating field is ambiguous (feature is ungated, not v52-enforced)  ·  `DONE`

_Applied directly from the register's pre-confirmed evidence (Spin2 v55 conflict audit, compiler-probed twice). See the register entry for full per-fact verification._


### Clock / HUBSET operand map

#### F-027 — `clock_system.yaml`: Wrong bit positions: manual says D[23:14], canonical is D[17:8] (magnitudes 10-bit / …  ·  `DONE`

**Files:** `deliverables/ai/P2/architecture/clock_system.yaml`

**Fix applied:**
- Rename the VCO multiplier config_fields key from d23_14 to d17_8 and correct the field name from MMMM_MMMMMM to MMMMMMMMMM, matching the canonical Silicon Doc bit layout where MMMMMMMMMM occupies D[17:8]

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/part3-interrupts.txt:521 (canonical HUBSET operand pattern %0000_000E_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS)
- engineering/ingestion/sources/silicon-doc/part3-interrupts.txt:536-540 (%MMMMMMMMMM = 0..1023 -> 1..1024 multiply of VCO)
- deliverables/ai/P2/architecture/clock_system.yaml:134-144 (current config_fields block)

**Why / rationale:** The canonical Silicon Doc pattern at part3-interrupts.txt:521 is %0000_000E_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS. Counting bits right-to-left: SS=D[1:0], CC=D[3:2], PPPP=D[7:4], MMMMMMMMMM=D[17:8] (10 bits), DDDDDD=D[23:18] (6 bits), E=D[24]. The YAML currently uses key d23_14 for the VCO multiplier field — that range D[23:14] is 10 bits but is shifted 6 bits too high, overlapping the XI input divider field DDDDDD. The correct key is d17_8. The field name also has a typo: MMMM_MMMMMM should be MMMMMMMMMM (10 M's). Note: The broader config_fields block has additional errors (wrong field assignments for nearly all other keys) which are covered under F-029; F-027 is specifically scoped to the VCO multiplier bit position and field name.

#### F-028 — `clock_system.yaml`: hubset.yaml clock_configuration.bit_fields.d3_2.values (lines 42-45) assigns 15pF to …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/hubset.yaml`

**Fix applied:**
- Replace the three-entry d3_2.values with four correct entries matching the Silicon Doc %CC table: 0b01 is no-caps (not 15pF), 0b10 is the missing 15pF entry, all include 1MΩ feedback wording

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/part3-interrupts.txt:562-571 (%CC table: %00=Hi-Z/OFF, %01=1M-ohm/OFF, %10=1M-ohm/15pF, %11=1M-ohm/30pF)
- deliverables/ai/P2/language/pasm2/hubset.yaml:40-45 (defective d3_2.values — confirmed present today)
- deliverables/ai/P2/architecture/clock_system.yaml:149-153 (correct reference: 0b01=no caps, 0b10=15pF, 0b11=30pF)

**Why / rationale:** Silicon doc part3-interrupts.txt lines 562-571 confirm the four-entry %CC table unambiguously. hubset.yaml d3_2.values has only three entries and maps 15pF to 0b01 (wrong — silicon says 0b01 is 1M-ohm feedback with no caps). The missing 0b10 entry is the true 15pF value. clock_system.yaml clock_modes.crystal_config.modes (lines 149-153) already encodes the correct four-entry mapping and serves as the in-repo cross-check. The proposed correction restores the full four entries with accurate descriptions. Note: the proposed correction uses ASCII "1MO" — the exact Unicode character chosen (Ω vs ohm symbol) should match the existing convention used in the YAML file; the current incorrect entry uses no such symbol, so plain ASCII "1M-ohm" or the omega character both work; the orchestrator should standardize to match the clock_system.yaml convention which uses "1MΩ".

#### F-029 — `clock_system.yaml`: clock_system.yaml contains two disagreeing maps: pll_system block (lines 104-118) is …  ·  `DONE`

**Files:** `deliverables/ai/P2/architecture/clock_system.yaml`

**Fix applied:**
- Replace the entirely wrong hubset_configuration.config_fields block (lines 134-144) with the canonical Silicon Doc layout. Also fix the clock_modes block where cc_field and ss_field bit positions are swapped (D[1:0] vs D[3:2]).
- Fix clock_modes CC/SS field bit positions: cc_field is D[3:2] (not D[1:0]) and ss_field is D[1:0] (not D[3:2]) per Silicon Doc lines 562-584.

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/part3-interrupts.txt:488-489 (HUBSET circuit-select patterns)
- engineering/ingestion/sources/silicon-doc/part3-interrupts.txt:521 (canonical operand %0000_000E_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS)
- engineering/ingestion/sources/silicon-doc/part3-interrupts.txt:525-584 (field tables: E=bit24, DDDDDD=23:18, MMMMMMMMMM=17:8, PPPP=7:4, CC=3:2, SS=1:0)
- deliverables/ai/P2/architecture/clock_system.yaml:97-118 (pll_system block — CORRECT)
- deliverables/ai/P2/architecture/clock_system.yaml:134-144 (config_fields — WRONG, verified present today)
- deliverables/ai/P2/architecture/clock_system.yaml:147-161 (clock_modes cc_field/ss_field — SWAPPED, additional defect)

**Why / rationale:** Finding CONFIRMED. The hubset_configuration.config_fields block (lines 137-144) is entirely wrong. Verified defects versus Silicon Doc (part3-interrupts.txt lines 521, 525-584): (1) d27_24 labeled 'XI divider (PPPP)' — E is at bit24, DDDDDD is at 23:18; (2) d23_14 labeled 'VCO multiplier' — field is bits 17:8, not 23:14; (3) d13_10 'Reserved' — fabricated field; (4) d9 'PLL power enable' — fabricated; E (PLL enable) belongs at bit24; (5) d8 'Crystal oscillator enable' — fabricated (no such bit in silicon doc); (6) d7_4 labeled 'Post divider (DDDD)' — label should be PPPP not DDDD; (7) d3_2 labeled 'Clock source select (SS)' — silicon doc has CC (crystal config) at bits 3:2; (8) d1_0 labeled 'Crystal configuration (CC)' — silicon doc has SS (clock source select) at bits 1:0. The pll_system block (lines 104-118) is CORRECT and already has the right bit positions. The clock_modes block has an additional unreported defect: cc_field reads D[1:0] but should be D[3:2], and ss_field reads D[3:2] but should be D[1:0] — mode value tables themselves are correct. Note: d31 'Reset request' in current YAML describes the %0001_xxxx HUBSET hard-reset mode, not a bit within the clock-config word; leaving it with a clarifying note is appropriate since it documents overall HUBSET behavior. No compiler probe was run as bit-field positions are not compilable — verified entirely from silicon-doc primary source.

#### F-030 — `clock_system.yaml`: Example literals written in an SS_CC (source-first) order conflicting with canonical …  ·  `DONE`

**Files:** `deliverables/ai/P2/architecture/clock_system.yaml`

**Fix applied:**
- Swap the D[3:2]/D[1:0] field labels in config_fields (CC is D[3:2], SS is D[1:0] per Silicon Doc PPPP_CCSS layout)
- Swap cc_field and ss_field bit-position annotations in clock_modes (CC=D[3:2], SS=D[1:0] per Silicon Doc)
- Fix example literals: %00_10 should be %10_00 (CC=10=15pF, SS=00=RCFAST) to enable crystal while staying on RCFAST, matching Silicon Doc worked example at p2-documentation.txt:6258 which ends _10_00 for 'enable crystal+PLL, stay in RCFAST'. Applied to basic_crystal_20mhz and pll_160mhz_from_20mhz_crystal and overclock_250mhz examples.

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/part3-interrupts.txt:521 — canonical operand layout ##%0000_000E_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS
- engineering/ingestion/sources/silicon-doc/part3-interrupts.txt:562-584 — %CC table (D[3:2]: crystal/cap config) and %SS table (D[1:0]: clock source select)
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:6256-6266 — worked example ##%1_100111_0100101000_1111_10_00 = 'enable crystal+PLL, stay in RCFAST mode' confirming trailing _10_00 = CC=10 SS=00
- deliverables/ai/P2/architecture/clock_system.yaml:143-144 — swapped D[3:2]/D[1:0] labels in config_fields
- deliverables/ai/P2/architecture/clock_system.yaml:148-161 — swapped cc_field/ss_field bit positions in clock_modes
- deliverables/ai/P2/architecture/clock_system.yaml:185,194,206 — wrong literal %00_10 (should be %10_00)

**Why / rationale:** Three distinct defects confirmed, all stemming from CC/SS field position swap:

1. config_fields labels: D[3:2] is labeled 'Clock source select (SS)' and D[1:0] is labeled 'Crystal configuration (CC)'. Silicon Doc PPPP_CCSS layout shows CC=D[3:2] and SS=D[1:0] — the labels are swapped.

2. clock_modes bit positions: cc_field='D[1:0]' and ss_field='D[3:2]' are wrong. Must be cc_field='D[3:2]' and ss_field='D[1:0]'.

3. Example literals: All three code examples use %00_10 as the first HUBSET (comment 'Enable crystal'/'Crystal with 15pF caps'). Per silicon doc: %00_10 = CC=00 (Hi-Z, crystal OFF) + SS=10 (switch to XI). This is nonsensical — switching to XI while crystal is Hi-Z. The silicon doc worked example at p2-documentation.txt:6258 explicitly uses _10_00 for 'enable crystal+PLL, stay in RCFAST' (CC=10=15pF, SS=00=RCFAST). So %00_10 must be %10_00.

The second HUBSET in examples (%10_10 = CC=10, SS=10 = 15pF caps + switch to XI) is CORRECT per silicon doc and needs no change.

Note: The finding description says 'To switch to XI: CC=10, SS=10 -> 10_10', which matches the YAML and is correct. The finding's proposed fix at line 525 references manual instructions-h.md for swapping field annotations — that is a SEPARATE manual-scope defect (fix_target: manual) outside the YAML scope. Only the YAML defects are addressed here.

#### F-031 — `clock_system.yaml`: Literal %0001_0000_0000_00001010_10 does not parse into canonical field widths (uses a …  ·  `DONE`

**Files:** `deliverables/ai/P2/architecture/clock_system.yaml`

**Fix applied:**
- Replace the entirely wrong hubset_configuration.config_fields section with the canonical silicon-doc field map (E=D[24], DDDDDD=D[23:18], MMMMMMMMMM=D[17:8], PPPP=D[7:4], CC=D[3:2], SS=D[1:0]). Eliminates bogus d9/d8/d13_10 fields and fixes the swapped CC/SS labels.
- Fix clock_modes: cc_field and ss_field are swapped. Silicon doc canonical: CC=D[3:2], SS=D[1:0].
- Fix basic_crystal_20mhz example: line 185 ##%00_10 is wrong (CC=%00 stays disabled, SS=%10 switches to XI before crystal is enabled). Should be ##%10_00 (CC=%10 enables 15pF crystal, SS=%00 stays on RCFAST during warmup).
- Fix pll_160mhz_from_20mhz_crystal example: HUBSET literals are 18-bit values that decode with E=0 (PLL OFF) and MMMMMMMMMM=64 (x65, not x16). Replace with correct 32-bit literals where E=1 (bit 24), DDDDDD=0, MMMMMMMMMM=15 (x16), PPPP=0 (VCO/2), CC=%10 (15pF). Also fix the crystal-enable step (same CC/SS swap as basic example).
- Fix overclock_250mhz example: HUBSET literals have same E=0 / wrong-multiplier defect. Correct for /1, x25, VCO/2: E=1 (bit 24), DDDDDD=0, MMMMMMMMMM=24 (x25), PPPP=0 (VCO/2), CC=%10. Also fix crystal-enable step.

**How verified (compiler):** N/A — HUBSET is a hub-control instruction whose D operand is an integer constant; there is no compilable behavior that differentiates a wrong 18-bit literal from a correct 32-bit literal at the pnut-ts level (both assemble without error; the defect is in the semantic decode of the integer value against the canonical field map).

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/part3-interrupts.txt:488 (HUBSET canonical operand layout %0000_xxxE_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS)
- engineering/ingestion/sources/silicon-doc/part3-interrupts.txt:521 (HUBSET ##%0000_000E_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS)
- engineering/ingestion/sources/silicon-doc/part3-interrupts.txt:525-584 (field tables: E=PLL on/off, DDDDDD=bits23-18, MMMMMMMMMM=bits17-8, PPPP=bits7-4, CC=bits3-2, SS=bits1-0)
- deliverables/ai/P2/architecture/clock_system.yaml:134-144 (defective config_fields section)
- deliverables/ai/P2/architecture/clock_system.yaml:148,156 (swapped cc_field/ss_field in clock_modes)
- deliverables/ai/P2/architecture/clock_system.yaml:185,197,199,209,211 (wrong HUBSET literals in programming_examples)
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-h.md:36-53 (manual field map — confirmed CORRECT)
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-h.md:74-76 (manual 160MHz literals — confirmed CORRECT: 0x01000F0A/0x01000F0B)

**Why / rationale:** The finding CONFIRMS multiple real defects in clock_system.yaml, but the proposed correction's claim that instructions-h.md also needs fixing is REFUTED — the manual is already correct. Specifically:

CONFIRMED YAML defects:
1. config_fields section (lines 134-144): Entirely wrong field layout. Has bogus d9 (PLL power enable) and d8 (crystal enable) fields that do not exist in the silicon doc spec; incorrectly groups d27-24 as XI divider (D[24] is E, the PLL enable bit); conflates DDDDDD and MMMMMMMMMM ranges; and swaps the CC and SS labels (d3_2 says SS but silicon doc has CC there; d1_0 says CC but silicon doc has SS there).
2. clock_modes section (lines 148, 156): cc_field and ss_field are swapped. Silicon doc canonical: CC=D[3:2], SS=D[1:0]; YAML says cc_field=D[1:0] and ss_field=D[3:2].
3. basic_crystal_20mhz example (line 185): ##%00_10 = 0x02 decodes as CC=%00 (crystal disabled), SS=%10 (switch to XI) — no crystal is ever enabled. Correct first step is ##%10_00 (CC=%10 = 15pF enabled, SS=%00 = stay on RCFAST).
4. pll_160mhz example (lines 197, 199): Literals ##%0001_0000_0000_00_10_10 and ##%0001_0000_0000_00_10_11 are 18-bit values = 0x400A / 0x400B, which decode with E=0 (PLL OFF), MMMMMMMMMM=64 (multiply by 65, not 16). Correct literals are ##%0000_0001_0000_0000_0000_1111_0000_1010 / _1011 (E=1, /1, x16, VCO/2, 15pF, XI/PLL).
5. overclock_250mhz example (lines 209, 211): Same class of defect — ##%0001_1001_0000_00_10_10 = 0x640A, E=0, mult x101. Correct: ##%0000_0001_0000_0000_0001_1000_0000_1010 (E=1, /1, x25, VCO/2, 15pF).

REFUTED part of finding: The finding's proposed correction targets instructions-h.md (manual) for a field map fix. Reading instructions-h.md lines 36-53 and 74-76 directly, the manual has the canonical correct field positions (D[1:0]=SS, D[3:2]=CC, D[23:18]=DDDDDD, D[17:8]=MMMMMMMMMM, D[7:4]=PPPP, D[24]=E) AND the correct 160MHz literals (0x01000F0A/0x01000F0B expressed as %1_000000_0000001111_0000_10_10/11 which is equivalent). The manual does NOT need editing.

#### F-084 — `clock_system.yaml`: The named bit positions (CC 1:0, SS 3:2, DDDD 7:4, enables 8/9, VCO mult 23:14, divider …  ·  `DONE`

**Files:** `deliverables/ai/P2/architecture/clock_system.yaml`

**Fix applied:**
- Fix config_fields bit-field layout and clock_modes field assignments. The committed version has wrong bit positions (d27_24/d23_14 for divider/multiplier instead of d23_18/d17_8), fabricated fields d9/d8 (no such bits — PLL enable is E at bit24), swapped CC/SS labels in both config_fields and clock_modes. The working tree already has the correction uncommitted.

**How verified (compiler):** N/A — clock mode bit-field layout is not compiler-probeable; verified against Silicon Doc tables directly

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/part3-interrupts.txt:488,521,530-584 — canonical %0000_000E_DDDDDD_MMMMMMMMMM_PPPP_CCSS layout with per-field tables confirming E=bit24, DDDDDD=bits23:18, MMMMMMMMMM=bits17:8, PPPP=bits7:4, CC=bits3:2, SS=bits1:0
- deliverables/ai/P2/architecture/clock_system.yaml:130-160 — working-tree (uncommitted) vs committed HEAD (git show HEAD)

**Why / rationale:** The finding is fully CONFIRMED. The committed HEAD of clock_system.yaml has multiple errors in hubset_configuration.config_fields and clock_modes: (1) d27_24 labelled 'XI divider for PLL (PPPP)' — wrong, XI divider is DDDDDD at bits 23:18; (2) d23_14 labelled 'VCO multiplier (MMMM_MMMMMM)' — wrong, VCO multiplier is bits 17:8; (3) d13_10:'Reserved', d9:'PLL power enable', d8:'Crystal oscillator enable' — all fabricated; E (PLL enable) is at bit 24, there is no bit-8 crystal-enable; (4) d3_2/'Clock source select (SS)' and d1_0/'Crystal configuration (CC)' are swapped — Silicon Doc shows CC=bits 3:2, SS=bits 1:0; (5) clock_modes has cc_field:'D[1:0]' and ss_field:'D[3:2]' — both inverted. The working tree already has an uncommitted correction that aligns all fields with the Silicon Doc layout. The proposed_snippet above matches what the working tree already contains. The fix needs to be committed."

#### F-085 — `clock_system.yaml`: The manual's 'DC to 350 MHz' matches one authority field exactly, but the KB is …  ·  `DONE`

**Files:** `deliverables/ai/P2/architecture/clock_system.yaml`

**Fix applied:**
- Replace the incorrect 'DC to 350 MHz' external-clock-input frequency range with the datasheet-sourced 'DC to 200 MHz'. The 350 MHz figure is the silicon doc's VCO/1 overclock ceiling for the PLL output, not a valid XI pin direct-input specification. The P2 datasheet AC Characteristics table (page 48) explicitly lists Direct drive (into XI): Min=DC, Max=200 MHz.

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/part3-interrupts.txt:545-546 — '350 MHz using the VCO / 1 mode (%PPPP = 15)' — confirms 350 MHz is a PLL overclock ceiling, not XI input range
- engineering/ingestion/sources/p2-datasheet/p2-datasheet-narrative.txt:6399-6421 — AC Characteristics table: Direct drive (into XI) Min=DC, Max=200 MHz; PLL output Min=3.33 MHz, Typ=180 MHz, Max=320 MHz
- deliverables/ai/P2/architecture/clock_system.yaml:91-95 — suspect 'frequency_range: DC to 350 MHz' still present verbatim
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-i/chapter-04-timing.md:22 — ALREADY CORRECTED in manual: now reads '180 MHz typical, 320 MHz extended per the spec sheet' with explicit note that 350 MHz is PLL overclock ceiling

**Why / rationale:** CONFIRMED. The suspect field 'external.frequency_range: DC to 350 MHz' is present verbatim in clock_system.yaml line 94. The 350 MHz figure originates from the silicon doc's VCO overclock note (part3-interrupts.txt:545-546: 'For fastest overclocking, the PLL can be pushed to 350 MHz using the VCO / 1 mode'), which describes the PLL output in extreme overclock, not the XI pin's direct-clock-input ceiling. The P2 datasheet AC Characteristics table gives the authoritative direct-drive-into-XI max as 200 MHz. The manual chapter-04-timing.md has already been corrected (line 22 now correctly attributies 350 MHz to PLL overclock, cites 180 MHz typical / 320 MHz extended as the system-clock spec). The YAML has not yet been updated to match. Secondary inconsistency: _xinfreq.range ('250 kHz to 500 MHz', line 36) and pll_system.constraints.input_frequency ('250 kHz to 500 MHz', line 99) are both unsourced — '250 kHz' appears to be a P1 carryover, '500 MHz' is not documented in any P2 primary source — but these are secondary issues beyond the finding's primary scope. The 'max_overclock: 350 MHz' entry at line 123 under pll_system.output_frequency is correctly attributed in context and does not need correction."

#### F-087 — `clock_system.yaml`: $1000_0000 sets bit 28, not the reset bit. The reset bit is D[31] = $8000_0000. The …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/hubset.yaml`, `deliverables/ai/P2/architecture/clock_system.yaml`

**Fix applied:**
- Fix three errors: (1) description claims reset uses 'bit 31'; (2) d31 bit_field falsely labeled 'Reset'; (3) chip_reset example uses $80000000 (PRNG seed) instead of $1000_0000 (actual reset). Silicon doc p2-documentation.txt:6032,6038 is unambiguous: D[31:28]=%0001 ($1000_0000) = Hard reset; D[31]=1 ($8000_0000) = PRNG seed.
- Fix chip_reset example: $80000000 seeds the PRNG (MSB=1); actual chip reset is $1000_0000 (D[31:28]=%0001).
- Fix self-contradictory d31 entry in clock_configuration. In clock mode (%0000_...), D[31]=1 would actually select PRNG seed mode, not reset. Reset is a separate HUBSET mode (%0001_xxxx = $1000_0000). The d31 entry should be corrected to not describe it as a reset bit.

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:6031-6041 (HUBSET function-select table: %0001 = Hard reset; %1DDD = PRNG seed)
- engineering/ingestion/sources/silicon-doc/part3-pages-37-38.txt:75 (PRNG seeding uses MSB of D = D[31]=1)
- engineering/ingestion/sources/silicon-doc/part3-pages-37-38.txt:99-102 (chip reset: HUBSET ##$1000_0000)
- deliverables/ai/P2/language/pasm2/hubset.yaml:19,23-25,98-101 (current defective text confirmed present)
- deliverables/ai/P2/architecture/clock_system.yaml:136 (current defective d31 entry confirmed present)

**Why / rationale:** The silicon doc function-select table (p2-documentation.txt:6031-6041) is unambiguous. Five HUBSET modes are distinguished by D[31:28]: %0000=clock mode, %0001=hard reset/reboot, %0010=write-protect+debug, %0100=filter config, %1xxx=PRNG seed (D[31]=1). Therefore: $1000_0000 (D[31:28]=%0001) = chip reset; $8000_0000 (D[31]=1 = %1xxx) = PRNG seed. hubset.yaml has three confirmed errors: (1) description wrongly says 'chip reset (bit 31)'; (2) d31 bit_field labeled 'Reset / Write 1 to reset the entire chip' — D[31]=1 actually selects PRNG seed; (3) chip_reset example uses $80000000 which is the PRNG seed command, not reset. clock_system.yaml line 136 also mislabels d31 as 'Reset request (write 1 to reset chip...)' — self-contradictory since it parenthetically acknowledges reset is a 'different HUBSET mode, %0001_xxxx'. The d31 field in clock_configuration context should clarify it belongs to PRNG-seed selection, not to chip-reset. The spin2 hubset.yaml at deliverables/ai/P2/language/spin2/methods/hubset.yaml was not checked but may need similar review."


### Assembler directives — ORG / FIT / ORGF / ORGH / data / FILE

#### F-068 — `org.yaml`: YAML restricts ORG to COG RAM only (0-$1FF). The manual's wider range (address up to …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/org.yaml`

**Fix applied:**
- Extend address range from COG-only (0-$1FF) to COG+LUT (0-$3FF), fix parameter description, top-level description, note, and oneliner to reflect that ORG addresses both COG RAM and LUT RAM.

**How verified (compiler):** pnut-ts /tmp/org_lut_test.spin2 (ORG $200; nop) → Wrote /tmp/org_lut_test.bin (6300 bytes), Done. pnut-ts /tmp/org_lut_test2.spin2 (ORG $300,$380; nop) → Wrote /tmp/org_lut_test2.bin (6300 bytes), Done. Both LUT-region addresses accepted without error.

**Sources that proved it:**
- engineering/ingestion/sources/spin2-v51/spin2-v51-narrative.txt:1489 — 'ORG $200 SET COG-EXEC MODE, COG ADDRESS = $200, COG LIMIT = $400 (LUT, DEFAULT LIMIT)'
- engineering/ingestion/sources/spin2-v51/spin2-v51-narrative.txt:1491 — 'ORG $300,$380 ... (LUT)'
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/directives.md:48 — 'Set the assembly origin to a specific COG or LUT RAM address'
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/directives.md:60 — parameter range '0 to $400'
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/directives.md:72-73 — auto-limit: addr<$200 → $200; addr>=$200 → $400
- deliverables/ai/P2/language/pasm2/org.yaml:14-15 — suspect range:0-$1FF and 'Cog RAM address (0-511)' confirmed present
- deliverables/ai/P2/language/pasm2/org.yaml:30 — suspect note 'ORG affects cog RAM addresses only (0-$1FF)' confirmed present
- pnut-ts v1.55.0 probe: ORG $200 + nop compiled cleanly (Wrote .bin/Done)
- pnut-ts v1.55.0 probe: ORG $300,$380 + nop compiled cleanly (Wrote .bin/Done)

**Why / rationale:** Finding CONFIRMED by three independent sources: (1) spin2-v51-narrative.txt lines 1489/1491 explicitly show ORG $200 and ORG $300,$380 as valid LUT examples; (2) the manual (directives.md:48,60,72-73) explicitly states COG/LUT range 0-$400 with auto-limit logic; (3) pnut-ts compiler accepts both ORG $200 and ORG $300,$380 cleanly. The YAML's restriction to 0-$1FF (COG only) is the sole defect. The proposed correction extends the range to 0-$3FF and replaces the misleading note. No change needed to the spin2 org.yaml (it has no range constraint to fix). The auto-limit behavior (bare ORG → $1F8, addr<$200 → $200, addr>=$200 → $400) is covered more fully by F-069; this finding focuses only on correcting the false COG-only restriction.

#### F-069 — `fit.yaml`: The bare-ORG default limit of $1F8 and the conditional $200/$400 auto-limit logic have no …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/org.yaml`, `deliverables/ai/P2/language/pasm2/fit.yaml`

**Fix applied:**
- Fix syntax (add bare-ORG and 2-param forms), fix parameter range from 0-$1FF to 0-$400, add optional limit parameter, correct notes to cover COG+LUT range (0-$3FF), and add auto-limit behavior documentation.
- Fix syntax from FIT [address] (implying optional) to FIT address (required); remove false example showing bare FIT; correct note claiming bare FIT defaults to $200 (bare FIT is rejected by the compiler with 'Expected a constant').

**How verified (compiler):** pnut-ts v1.55.0: (1) bare ORG + res $1F8 → OK; res $1F9 → 'Cog address exceeds limit (m110)' [CONFIRMS $1F8 limit]. (2) ORG $10 + res $1F0 → OK; res $1F1 → 'Cog address exceeds limit (m110)' [CONFIRMS $200 limit for addr<$200]. (3) ORG $200 + res $200 → OK; res $201 → 'Cog address exceeds limit (m110)' [CONFIRMS $400 limit for addr>=$200]. (4) bare FIT → 'Expected a constant, unary operator, or \"(\"' [CONFIRMS bare FIT is invalid — fit.yaml's claim is false].

**Sources that proved it:**
- pnut-ts v1.55.0 compiler probe: bare ORG + res $1F8 → compiles OK; res $1F9 → error 'Cog address exceeds limit (m110)'
- pnut-ts v1.55.0 compiler probe: ORG $10 + res $1F0 (final $200) → compiles OK; res $1F1 (final $201) → error 'Cog address exceeds limit (m110)'
- pnut-ts v1.55.0 compiler probe: ORG $200 + res $200 (final $400) → compiles OK; res $201 (final $401) → error 'Cog address exceeds limit (m110)'
- pnut-ts v1.55.0 compiler probe: bare FIT (no parameter) → error 'Expected a constant, unary operator, or "("' — bare FIT is invalid
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/directives.md:63-76 (Auto-Limit Behavior section)
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/directives.md:112 (Pitfall note about bare ORG defaulting to $1F8)
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/directives.md:1010-1097 (FIT section — always shows FIT with required parameter)
- engineering/ingestion/sources/spin2_lang_ref_v55/spin2-v55-text.txt:316,323 — FIT always shown with explicit address parameter
- deliverables/ai/P2/language/pasm2/org.yaml:1-37 (current state — no auto-limit, range 0-$1FF)
- deliverables/ai/P2/language/pasm2/fit.yaml:1-34 (current state — incorrect bare FIT syntax and note)

**Why / rationale:** All three auto-limit behaviors claimed by the manual (directives.md:63-76) are independently confirmed by pnut-ts v1.55.0 compiler probes. The org.yaml defects are confirmed: wrong syntax (missing bare and 2-param forms), wrong range (0-$1FF should be 0-$400), no auto-limit documentation, and notes claiming only COG range when LUT ($200-$3FF) is also valid. Additionally, fit.yaml has a factual error not just cited as secondary evidence: 'syntax: FIT [address]' implies the address is optional, but the compiler rejects bare FIT with 'Expected a constant'. The note 'FIT without parameter checks for cog RAM limit ($200)' is also false. Both files need correction. The manual itself is correct and needs no changes.

#### F-070 — `orgf.yaml`: Direct contradiction: manual says ORGF is COG-mode-only and errors in ORGH mode; YAML …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/orgf.yaml`

**Fix applied:**
- Fix range field to remove false 'or hub address' clause and add ORGH-mode restriction note
- Add ORGH-mode restriction note to notes section

**How verified (compiler):** pnut-ts /tmp/orgf_hub.spin2 (DAT / ORGH $400 / long 0 / ORGF $410) → exit 1: 'ORGF is not allowed in ORGH mode'; pnut-ts /tmp/orgf_cog.spin2 (DAT / ORG 0 / nop / ORGF $10 / nop) → exit 0: 'Wrote /tmp/orgf_cog.bin'

**Sources that proved it:**
- pnut-ts v1.55.0 probe — /tmp/orgf_hub.spin2 (ORGH+ORGF) → exit 1: 'ORGF is not allowed in ORGH mode'
- pnut-ts v1.55.0 probe — /tmp/orgf_cog.spin2 (ORG+ORGF) → exit 0: 'Wrote /tmp/orgf_cog.bin'
- deliverables/ai/P2/language/pasm2/orgf.yaml:17 — confirmed suspect text 'range: 0-$1FF (cog) or hub address' is present today
- deliverables/ai/P2/language/pasm2/orgf.yaml:46-51 — notes section has no ORGH-mode restriction

**Why / rationale:** The suspect text is present today at orgf.yaml:17 — 'range: 0-$1FF (cog) or hub address'. The compiler definitively refutes the 'or hub address' clause: ORGF after ORGH emits the verbatim error 'ORGF is not allowed in ORGH mode' and exits 1; ORGF after ORG compiles clean. The notes section (lines 46-51) also lacks any documentation of this ORGH restriction. Two edits are required: (1) fix the range field to remove the false hub-address clause, (2) add a note documenting the ORGH-mode compiler error. The spin2 assembly-directives orgf.yaml is a separate file — the finding scopes only the pasm2 YAML, which is correct since the defect (false 'or hub address' range) is specific to the pasm2 YAML.

#### F-071 — `orgf.yaml`: The manual contradicts itself: the parameter table permits a hub address, but the prose …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/orgf.yaml`

**Fix applied:**
- Fix parameter range to remove false 'or hub address' clause; ORGF is COG/LUT-mode only. Also fix description and add COG-mode-only restriction note.

**How verified (compiler):** pnut-ts -d (no DEBUG window code): (1) ORGH+ORGF → exit 1 'ORGF is not allowed in ORGH mode' confirming hub mode is forbidden; (2) ORG 0 + ORGF $100 → exit 0 clean (cog mode works); (3) ORG $200 + ORGF $280 → exit 0 (LUT mode also works, addresses $200-$3FF are valid); (4) ORG $200 + ORGF $3FF → exit 0 (upper LUT limit $3FF valid). The valid range is 0-$3FF (cog+LUT), not just 0-$1FF, and 'hub address' is completely invalid.

**Sources that proved it:**
- pnut-ts v1.55.0 probe: /tmp/orgf_hub.spin2 (ORGH+ORGF) → exit 1: 'ORGF is not allowed in ORGH mode'; /tmp/orgf_cog.spin2 (ORG+ORGF) → exit 0 clean compile; /tmp/orgf_lut.spin2 (ORG $200 + ORGF $280) → exit 0 clean compile; /tmp/orgf_lut2.spin2 (ORG $200 + ORGF $3FF) → exit 0 clean compile
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:12976-12980: 'ORGF / cog_address / Fill to cog_address with $00 bytes. Must be in cog mode.'
- engineering/ingestion/sources/spin2_lang_ref_v55/spin2-v55-text.txt:315: 'ORGF $040 fill to cog address $040 with zeros (no symbol allowed before ORGF)' — in DAT Cog-exec section only; no ORGF appears in the hub-exec section
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/directives.md:138: manual already correctly says 'Target COG address to advance to (0-$1FF), filling intervening space with zeros'; :165 'ORGF is not allowed in ORGH mode'; :172 'ORGF is only valid in COG mode (after ORG), not in Hub mode'; :178 pitfall warning confirming COG-only
- deliverables/ai/P2/language/pasm2/orgf.yaml:17 (current suspect text confirmed present): 'range: 0-$1FF (cog) or hub address'

**Why / rationale:** The defect is CONFIRMED and still present in deliverables/ai/P2/language/pasm2/orgf.yaml:17. The 'or hub address' clause is FALSE per three independent primary sources (pnut-ts, silicon-doc, v55 spec). The manual at directives.md:138 is already CORRECT (has no 'hub address' clause). Additionally the YAML range '0-$1FF' is itself incomplete — pnut-ts confirms ORGF also works in LUT mode (ORG $200-$3FF); the correct range is 0-$3FF (cog/LUT registers). The proposed fix should: (1) remove 'or hub address' from range; (2) expand range to 0-$3FF; (3) add a note 'ORGF is only valid in COG mode (after ORG) — not allowed in ORGH/hub mode' to the notes list. The spin2/assembly-directives/orgf.yaml has no range field at all and is too sparse to have this defect. Fix scope is pasm2/orgf.yaml only.

#### F-072 — `orgh.yaml`: The two authoritative YAMLs disagree on the bare-ORGH default (one $400, one …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/orgh.yaml`, `deliverables/ai/P2/language/spin2/assembly-directives/orgh.yaml`

**Fix applied:**
- Line 24 states flatly 'Default address is $400 if not specified' — true only for Spin2+PASM programs. In PASM-only programs bare ORGH continues from the current hub address (no zero-fill to $400). Replace with two-context wording per v51/v55 authority.
- Parameter default 'Current location' (line 25) and note 'Default address continues from current compilation position' (line 124) only describe PASM-only behavior. In Spin2+PASM programs bare ORGH defaults to $400. Both need to reflect the context-dependent rule from Spin2 v51/v55 authority.
- Note at line 124 says 'Default address continues from current compilation position' which is only true for PASM-only programs. Update to reflect both contexts.

**How verified (compiler):** pnut-ts v1.55.0 — PASM-only bare ORGH probe: 'DAT / org $0 / nop / orgh / test_here long $DEADBEEF' compiles to 8 bytes (0x00000000 + 0xDEADBEEF). The $DEADBEEF is at hub offset 4 (immediately after nop), NOT at $400 — confirming PASM-only bare ORGH continues from current position with no zero-fill to $400. Spin2+PASM bare ORGH probe: PUB main() + DAT / orgh / test_data long 0 compiles to 6296 bytes (interpreter header + content starting at $400) — confirming Spin2+PASM bare ORGH defaults to $400.

**Sources that proved it:**
- /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/spin2-v51/spin2-v51-narrative.txt:1536-1557 — Defines the two-context table: Spin2+PASM Programs (bare ORGH = $400) vs PASM-Only Programs (bare ORGH = current hub address)
- /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/spin2_lang_ref_v55/spin2-v55-text.txt:326-327 — v55 confirms the same two-context rule verbatim
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/pasm2/orgh.yaml:24 — Suspect text 'Default address is $400 if not specified' confirmed present today
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/spin2/assembly-directives/orgh.yaml:25,124 — 'Current location' default and matching note confirmed present today

**Why / rationale:** Finding CONFIRMED. Both YAMLs are currently wrong in complementary ways. pasm2/orgh.yaml:24 states the $400 default absolutely, omitting the PASM-only 'current position' case. spin2/assembly-directives/orgh.yaml lines 25 and 124 state 'current location' absolutely, omitting the Spin2+PASM '$400' case. The v51 narrative at lines 1536-1557 and v55 text at lines 326-327 both provide an explicit two-row table distinguishing the two program types. Compiler probes empirically confirm: PASM-only bare ORGH assembles data at the current hub offset (8-byte binary, $DEADBEEF at offset 4), while Spin2+PASM bare ORGH produces a 6296-byte binary starting at $400. Three targeted fixes are needed: one in pasm2/orgh.yaml and two in spin2/assembly-directives/orgh.yaml.

#### F-073 — `orgh.yaml`: YAML lacks any hub address ceiling, so the constraint is unverifiable; additionally the …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/orgh.yaml`, `deliverables/ai/P2/language/spin2/assembly-directives/orgh.yaml`

**Fix applied:**
- Add the optional limit parameter to syntax, document the $100000 address-space ceiling, add PNut error message, and add a two-argument example.
- Fix dat_block syntax to include the optional limit parameter; add notes about the $100000 ceiling and the PNut error message.
- Add missing hub address ceiling constraint and PNut error message to the notes list.

**How verified (compiler):** pnut-ts -d /tmp/orgh_test1.spin2 (ORGH $400,$100004) → '/tmp/orgh_test1.spin2:5:error:Hub address exceeds $100000 ceiling (m361)', exit 1. pnut-ts /tmp/orgh_test2.spin2 (ORGH $400,$100000) → exit 0 OK. pnut-ts /tmp/orgh_test5.spin2 (ORGH $400,$80000) → exit 0 OK.

**Sources that proved it:**
- pnut-ts v1.55.0 probe: ORGH $400,$100004 → error 'Hub address exceeds $100000 ceiling (m361)', exit 1 (confirmed)
- pnut-ts v1.55.0 probe: ORGH $400,$100000 → compiled OK, exit 0 (ceiling is inclusive)
- pnut-ts v1.55.0 probe: ORGH $FC000,$FC800 → compiled OK, exit 0 (two-param syntax confirmed)
- engineering/ingestion/sources/spin2_lang_ref_v55/spin2-v55-text.txt:322 — 'hub origin = $00400, origin limit = $100000 (both defaults)'
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:12962-12968 — ORGH {hub_address} definition (no ceiling mentioned, limit param absent)
- deliverables/ai/P2/language/pasm2/orgh.yaml:10 — syntax: ORGH [address] (no limit param, no ceiling note)
- deliverables/ai/P2/language/spin2/assembly-directives/orgh.yaml:13 — dat_block syntax: 'ORGH [address]' (no limit param, no ceiling note)

**Why / rationale:** Both orgh.yaml files are missing two related pieces of information: (1) the optional second `limit` operand in the syntax (`ORGH [address[, limit]]`), and (2) the $100000 address-space ceiling enforced by PNut (error message 'Hub address exceeds $100000 ceiling (m361)'). The Spin2 v55 spec (line 322) documents both defaults explicitly: 'hub origin = $00400, origin limit = $100000 (both defaults)'. The finding's concern that $100000 'exceeds physical 512KB hub RAM ($80000)' is correctly addressed in the F-073 finding prose — these are two distinct PNut checks. The fix here is purely additive YAML enrichment: add the limit operand to syntax and add notes about the ceiling. The manual text is not in scope for this YAML fix.

#### F-074 — `byte.yaml`: YAML one-line descriptions state these store into Hub memory, but the manual (correctly) …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/spin2/assembly-directives/byte.yaml`, `deliverables/ai/P2/language/spin2/assembly-directives/word.yaml`, `deliverables/ai/P2/language/spin2/assembly-directives/long.yaml`

**Fix applied:**
- Fix description and usage: replace 'Hub memory' with mode-relative phrasing — BYTE assembles data at the current origin regardless of ORG/ORGH mode.
- Fix description and usage: replace 'Hub memory' with mode-relative phrasing — WORD assembles data at the current origin regardless of ORG/ORGH mode.
- Fix description and usage: replace 'Hub memory' with mode-relative phrasing — LONG assembles data at the current origin regardless of ORG/ORGH mode.

**How verified (compiler):** pnut-ts /tmp/af109b.spin2 (DAT / ORG $100 / table long 1,2,3 / FIT $200) → 'Wrote /tmp/af109b.bin (12 bytes) ... Done', exit 0; pnut-ts /tmp/af109c.spin2 (BYTE/WORD/LONG after ORG $100) → 'Wrote /tmp/af109c.bin (11 bytes) ... Done', exit 0 — confirms BYTE/WORD/LONG are NOT Hub-only

**Sources that proved it:**
- deliverables/ai/P2/language/spin2/assembly-directives/byte.yaml:1-27 — confirmed 'Insert byte data into Hub memory at assembly time' at line 3; usage also says 'stored in Hub memory' at lines 10-12
- deliverables/ai/P2/language/spin2/assembly-directives/word.yaml:1-31 — confirmed 'Insert word (16-bit) data into Hub memory at assembly time' at line 3; usage also says 'stored in Hub memory' at lines 10-13
- deliverables/ai/P2/language/spin2/assembly-directives/long.yaml:1-36 — confirmed 'Insert long (32-bit) data into Hub memory at assembly time' at line 3; usage also says 'stored in Hub memory' at lines 11-14
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/directives.md:308-355 — BYTE section: 'Stores 8-bit values at the current address' (line 311/314); no Hub-only restriction stated
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/directives.md:358-403 — LONG section: 'Stores 32-bit values at the current address' (line 361/364); no Hub-only restriction
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/directives.md:408-453 — WORD section: 'Stores 16-bit values at the current address' (line 411/414); no Hub-only restriction
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/directives.md:83-110 — ORG example at line 87 shows 'table long 1, 2, 3' in COG mode (after ORG $100); line 110 'DAT blocks start in Hub mode by default; use ORG to switch to COG mode'
- pnut-ts v1.55.0 probe /tmp/af109b.spin2 — DAT/ORG $100/table long 1,2,3/FIT $200 → 'Wrote /tmp/af109b.bin (12 bytes) ... Done' exit 0 — LONG works in COG mode
- pnut-ts v1.55.0 probe /tmp/af109c.spin2 — DAT/ORG $100/ALIGNW/WORD/ALIGNL/LONG/BYTE all after ORG $100 → 'Wrote /tmp/af109c.bin (11 bytes) ... Done' exit 0 — BYTE/WORD/LONG all work in COG mode

**Why / rationale:** The defect is confirmed and NOT already fixed. All three spin2/assembly-directives/ YAML files (byte.yaml:3, word.yaml:3, long.yaml:3) contain 'Hub memory' in description, and the usage fields repeat the same error. The pasm2/ versions of these files (deliverables/ai/P2/language/pasm2/byte.yaml etc.) correctly say 'at the current address' — the bug is specific to the spin2/assembly-directives/ copies. The manual (directives.md) consistently says 'at the current address' with no Hub-only restriction, and pnut-ts v1.55.0 empirically confirms BYTE/WORD/LONG assemble wherever the current origin points (COG, LUT, or Hub). The proposed fix replaces the Hub-only claim with the accurate mode-relative description matching the manual's phrasing.

#### F-075 — `file.yaml`: Contradiction on whether path separators are permitted: manual forbids '/' and other path …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/spin2/assembly-directives/file.yaml`

**Fix applied:**
- Remove the false 'path is relative to source file' sentence from usage field; replace with accurate constraint that the filename must be a bare name with no path separators or other invalid characters.

**How verified (compiler):** pnut-ts t2.spin2 (DAT FILE \"sub/nested.bin\") -> t2.spin2:3:error:Invalid filename character, EXIT=1; pnut-ts t1.spin2 (DAT FILE \"data.bin\") -> Wrote t1.bin, EXIT=0. Version: 1.55.0

**Sources that proved it:**
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/directives.md:473 ("no path separators allowed")
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/directives.md:477-488 (invalid character table: / : * ? " < > |)
- engineering/ingestion/sources/spin2-v51/spin2-v51-narrative.txt:1431 (FILE "FILENAME" bare-name form only)
- pnut-ts v1.55.0 probe: FILE "sub/nested.bin" (file present) -> t2.spin2:3:error:Invalid filename character, EXIT=1
- pnut-ts v1.55.0 probe: FILE "data.bin" (bare name, file present) -> Wrote t1.bin, EXIT=0
- deliverables/ai/P2/language/spin2/assembly-directives/file.yaml:11-21 (current suspect text confirmed present)

**Why / rationale:** The YAML at file.yaml:13-14 contains the sentence 'The file path is relative to the source file location.' This implies path separators are valid in the filename, which directly contradicts both the PASM2 manual (directives.md:473 'no path separators allowed') and the pnut-ts compiler (which rejects '/' with 'Invalid filename character', not 'file not found'). The compiler probe independently settles this: bare filenames compile; filenames with '/' are rejected syntactically before any filesystem lookup. The manual is correct; the YAML is wrong. Only the YAML needs to change — no manual edit required.

#### F-076 — `file.yaml`: The 253-char limit, case-insensitivity, and invalid-character list have no confirming …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/spin2/assembly-directives/file.yaml`

**Fix applied:**
- Add filename_requirements block documenting invalid characters, DAT-only restriction, and platform-dependent case-sensitivity. The YAML is currently missing the invalid-character list (/ : * ? < > |), any case-sensitivity note, and the 253-char length limit. Compiler probes confirm the invalid chars and DAT-only restriction; manual already has the platform-dependent case note.

**How verified (compiler):** pnut-ts -d (not applicable; no DEBUG code). Probes run: (1) FILE in DAT → EXIT=0; (2) FILE in PUB inline PASM → 'Expected an instruction or variable', EXIT=1; (3) bad:name.txt → 'Invalid filename character', EXIT=1; (4) * ? < > | / each → 'Invalid filename character', EXIT=1; (5) exact-case ref → EXIT=0; (6) uppercase ref to lowercase file → 'DAT file not found [...] (preload)', EXIT=1. All results confirm the claims.

**Sources that proved it:**
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/spin2/assembly-directives/file.yaml:1-39 (full file — confirmed no invalid-char list, no case rule, no max-length field present today)
- /workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/directives.md:475-540 (FILE directive section — lines 477-489 list invalid chars; line 538 already has NEEDS-VERIFICATION flag on 253-char limit; line 539 already has platform-dependent case-sensitivity wording)
- pnut-ts v1.55.0 probe — /tmp/file_test_badchar.spin2: 'bad:name.txt' → 'error:Invalid filename character', EXIT=1
- pnut-ts v1.55.0 probe — chars * ? < > | / each → 'error:Invalid filename character', EXIT=1
- pnut-ts v1.55.0 probe — /tmp/file_test_pub.spin2: FILE in PUB inline-PASM → 'error:Expected an instruction or variable', EXIT=1
- pnut-ts v1.55.0 probe — /tmp/file_test_lower.spin2: exact-case 'file_test.txt' → EXIT=0 (compiles clean)
- pnut-ts v1.55.0 probe — /tmp/file_test_upper.spin2: uppercase ref 'FILE_TEST.TXT' to lowercase file → 'error:DAT file not found [FILE_TEST.TXT] (preload)', EXIT=1 (case-sensitive on Linux)

**Why / rationale:** PARTIAL verdict: The finding has two sides. (1) YAML side: file.yaml is genuinely missing the invalid-character list, case-sensitivity rule, and 253-char limit — these should be added. Compiler probes confirm the invalid chars and DAT-only restriction; case-sensitivity is confirmed as OS-dependent (case-sensitive on Linux). (2) MANUAL side: directives.md:538-539 already has BOTH the proposed corrections applied — line 538 already carries the NEEDS-VERIFICATION comment on the 253-char limit, and line 539 already has the platform-dependent case-sensitivity wording ('case-insensitive on Windows; case-sensitive on Linux and case-sensitive macOS volumes'). So the manual portion of the proposed correction is already done; only the YAML enrichment remains. The 253-char limit cannot be compiler-probed (no practical way to construct a 253+ char filename in a test), so it retains its NEEDS-VERIFICATION status. fix_target is 'mixed' because the remaining work is YAML-only (manual side already done).

#### F-077 — `fit.yaml`: The manual omits the no-argument FIT form that the authority documents (defaults to the …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/fit.yaml`

**Fix applied:**
- Fix three defects: (1) syntax changes from FIT [address] to FIT address (address is mandatory, not optional); (2) remove the fabricated note 'FIT without parameter checks for cog RAM limit ($200)'; (3) remove the fabricated bare-FIT example 'FIT // Default: ensure fits in cog RAM (< $200)'.

**How verified (compiler):** pnut-ts /tmp/fittest_bare.spin2 → EXIT=1, error 'Expected a constant, unary operator, or \"(\"'; pnut-ts /tmp/fittest_with_addr.spin2 (FIT $200) → EXIT=0, wrote .bin

**Sources that proved it:**
- pnut-ts v1.55.0 compiler probe: bare FIT → error 'Expected a constant, unary operator, or "("' (EXIT=1); FIT $200 → compiled successfully (EXIT=0) — /tmp/fittest_bare.spin2 and /tmp/fittest_with_addr.spin2
- engineering/ingestion/sources/spin2-v51/spin2-grammar-reference.md:295-296 — directive grammar: '"FIT" address' (address NOT in brackets, unlike ORG which has '[address]')
- engineering/ingestion/sources/spin2_lang_ref_v55/spin2-v55-text.txt:316,323 — all examples show FIT with explicit address: 'FIT $020', 'FIT $2000'

**Why / rationale:** The pasm2/fit.yaml currently documents three fabricated claims: (1) 'syntax: FIT [address]' implies the address is optional; (2) a note 'FIT without parameter checks for cog RAM limit ($200)' claims a default behavior; (3) an example 'FIT // Default: ensure fits in cog RAM (< $200)' demonstrates a non-existent bare form. All three are refuted by pnut-ts v1.55.0 (bare FIT is a hard syntax error) and by the Spin2 v51 grammar which shows FIT address (no brackets, mandatory), contrasted with ORG [address] (optional). The spin2/assembly-directives/fit.yaml already correctly shows 'FIT limit' (mandatory). Only the pasm2/fit.yaml needs correction.


### Timing corrections (fixed->variable, hub-exec ranges)

#### F-034 — `jatn.yaml`: jxro.yaml and jxmt.yaml are tagged timing.type 'fixed' (no range) while the manual …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/jxro.yaml`, `deliverables/ai/P2/language/pasm2/jxmt.yaml`

**Fix applied:**
- Change timing from fixed (no range) to variable with hub-exec range 13...20, matching all sibling event-jumps (jxrl, jqmt, jatn, etc.) and the canonical CSV.

**Sources that proved it:**
- /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:191,193 — JXMT and JXRO both list '2 or 4' (cog) and '2 or 13...20' (hub-exec), identical to every other event-jump in the class
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/pasm2/jxro.yaml:9-11 — timing: cycles: 2, type: fixed (no range field)
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/pasm2/jxmt.yaml:9-11 — timing: cycles: 2, type: fixed (no range field)
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/pasm2/jxrl.yaml:9-12 — timing: cycles: 2, type: variable, range: 13...20 (the correct sibling pattern)
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/pasm2/jqmt.yaml:9-12 — timing: cycles: 2, type: variable, range: 13...20
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/pasm2/jatn.yaml:9-12 — timing: cycles: 2, type: variable, range: 13...20

**Why / rationale:** The defect is exactly as described. CSV lines 191 (JXMT) and 193 (JXRO) confirm hub-exec timing '2 or 13...20' — identical to all other event-jumps in the 1011110 01I encoding class. The two affected YAMLs are the only ones in this class with type: fixed and no range field. The fix is a two-line change in each file: replace type: fixed with type: variable and add range: 13...20. The encoding.clocks field ('2 or 4') is already correct for cog-mode and does not need to change. No manual or PASM2-ENCODING-REFERENCE.md changes are needed per the finding's proposed correction note.

#### F-037 — `locknew.yaml`: The manual is correct (variable timing ranges). The yaml timing blocks claim a single …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/locknew.yaml`, `deliverables/ai/P2/language/pasm2/lockret.yaml`, `deliverables/ai/P2/language/pasm2/locktry.yaml`, `deliverables/ai/P2/language/pasm2/lockrel.yaml`

**Fix applied:**
- Replace fixed timing block (cycles:4/fixed) with variable timing matching encoding.clocks '4...11'
- Replace fixed timing block (cycles:2/fixed) with variable timing matching encoding.clocks '2...9'
- Replace fixed timing block (cycles:2/fixed) with variable timing matching encoding.clocks '2...9, +2 if result'

**How verified (compiler):** N/A — timing values are not compiler-verifiable; ground truth is the canonical CSV and manual encoding tables.

**Sources that proved it:**
- /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:268-271 — CSV rows for LOCKNEW('4...11'), LOCKRET('2...9'), LOCKTRY('2...9, +2 if result'), LOCKREL('2...9, +2 if result')
- /workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-l.md:64 — LOCKNEW encoding table Clks '4...11'
- /workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-l.md:77 — LOCKNEW explanation 'completes in 4 to 11 clock cycles'
- /workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-l.md:100 — LOCKREL encoding table Clks '2...9, +2 if result'
- /workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-l.md:113 — LOCKREL explanation '2 to 9 clock cycles, with an additional 2 cycles if the result is written back'
- /workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-l.md:135 — LOCKRET encoding table Clks '2...9'
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/pasm2/locknew.yaml:8-11 — current state: encoding.clocks '4...11' but timing cycles:4/type:fixed
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/pasm2/lockret.yaml:8-11 — current state: encoding.clocks '2...9' but timing cycles:2/type:fixed
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/pasm2/locktry.yaml:8-11 — current state: encoding.clocks '2...9, +2 if result' but timing cycles:2/type:fixed
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/pasm2/lockrel.yaml:8-11 — current state: encoding.clocks '2...9, +2 if result' but timing cycles:2/type:fixed

**Why / rationale:** All four YAMLs are internally self-contradictory: each has encoding[0].clocks already set to the correct variable range string, yet the separate timing block claims a single fixed cycle count (locknew cycles:4, lockrel/lockret/locktry cycles:2) with type:fixed. The canonical Parallax CSV (lines 268-271) and the PASM2 manual encoding tables independently confirm hub-window-dependent variable timing for all four instructions. The proposed fix changes only the timing.cycles string and timing.type field in each YAML to match what encoding.clocks already correctly states. This eliminates the internal contradiction without altering any other field. The cycles strings used in proposed_snippet match the encoding.clocks values exactly, consistent with the variable-timing pattern used in rdbyte.yaml, rdlong.yaml, and other hub-access instructions in this YAML set.

#### F-038 — `tjf.yaml`: The manual carries the COMPLETE taken-timing (cog 4 / hub 13-20). Several jump YAMLs are …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/tjf.yaml`, `deliverables/ai/P2/language/pasm2/tjz.yaml`, `deliverables/ai/P2/language/pasm2/tjnz.yaml`, `deliverables/ai/P2/language/pasm2/tjns.yaml`

**Fix applied:**
- Add hub-exec timing to encoding.clocks: '2 or 4' → '2 or 4 / 2 or 13-20'
- Add hub-exec timing to encoding.clocks: 2 or 4 → '2 or 4 / 2 or 13-20'

**Sources that proved it:**
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:174-180 (TJZ/TJNZ/TJF/TJNF/TJS/TJNS/TJV — all show cog='2 or 4', hub='2 or 13...20')
- deliverables/ai/P2/language/pasm2/tjf.yaml:8 (clocks: '2 or 4' — missing hub portion)
- deliverables/ai/P2/language/pasm2/tjz.yaml:8 (clocks: '2 or 4' — missing hub portion)
- deliverables/ai/P2/language/pasm2/tjnz.yaml:22 (clocks: 2 or 4 — missing hub portion, and timing.type: fixed at line 16)
- deliverables/ai/P2/language/pasm2/tjns.yaml:32 (clocks: 2 or 4 — missing hub portion, and timing.type: fixed at line 26)
- deliverables/ai/P2/language/pasm2/tjv.yaml:40 (clocks: 2 or 4 / 2 or 13–20 — correct full form, reference)
- deliverables/ai/P2/language/pasm2/tjs.yaml:39 (clocks: '2 or 4 / 2 or 13-20' — correct full form, reference)
- deliverables/ai/P2/language/pasm2/tjnf.yaml:39 (clocks: '2 or 4 / 2 or 13-20' — correct full form, reference)

**Why / rationale:** CONFIRMED. The CSV (rows 174-180, note: the finding incorrectly cited rows 198-204 which are JNCT/JNSE event-branch instructions — the actual TJ rows are 174-180) confirms all seven TJ-series instructions have cog-exec='2 or 4' and hub-exec='2 or 13...20'. Four YAMLs (tjf, tjz, tjnz, tjns) carry only '2 or 4' in encoding.clocks, dropping the hub-exec variant entirely. The three correct siblings (tjv, tjs, tjnf) all carry the full dual-timing form. The hub-exec timing omission in encoding.clocks is the defect F-038 targets. Note: tjnz.yaml and tjns.yaml also have timing.type: fixed (should be variable) — that overlapping defect is scoped to F-039. This fix addresses only encoding.clocks for all four files. The proposed clocks value '2 or 4 / 2 or 13-20' matches the tjs/tjnf sibling convention (regular hyphen, not en-dash as in tjv). No manual change needed.

#### F-039 — `tjf.yaml`: Conditional jumps are inherently variable-timed (taken vs not-taken). Marking TJNZ/TJNS …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/tjnz.yaml`, `deliverables/ai/P2/language/pasm2/tjns.yaml`

**Fix applied:**
- Change timing.type from fixed to variable to match all other TJ* siblings and the encoding clocks field (2 or 4)

**Sources that proved it:**
- deliverables/ai/P2/language/pasm2/tjnz.yaml:14-16 (timing block: type: fixed confirmed present)
- deliverables/ai/P2/language/pasm2/tjns.yaml:24-26 (timing block: type: fixed confirmed present)
- deliverables/ai/P2/language/pasm2/tjnz.yaml:22 (encoding clocks: 2 or 4 — contradicts type: fixed)
- deliverables/ai/P2/language/pasm2/tjns.yaml:32 (encoding clocks: 2 or 4 — contradicts type: fixed)
- deliverables/ai/P2/language/pasm2/tjz.yaml:10-12 (timing type: variable, range: 13...20 — sibling pattern)
- deliverables/ai/P2/language/pasm2/tjf.yaml:10-12 (timing type: variable, range: 13...20 — sibling pattern)
- deliverables/ai/P2/language/pasm2/tjs.yaml:31-33 (timing type: variable, notes field)
- deliverables/ai/P2/language/pasm2/tjnf.yaml:31-33 (timing type: variable, notes field)
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:199 (TJNZ: 2 or 4 / 2 or 13...20)
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:203 (TJNS: 2 or 4 / 2 or 13...20)
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-iii/appendix-a-encoding-table.md:340-341 (TJNS: 2 or 4, TJNZ: 2 or 4)

**Why / rationale:** Finding is fully confirmed. Both tjnz.yaml and tjns.yaml have timing.type: fixed while their encoding.clocks field reads '2 or 4' — an internal contradiction. All six TJ* siblings (TJZ, TJF, TJS, TJNF) use timing.type: variable. The P2 Instructions CSV (Rev B/C Silicon) confirms all TJ* have variable timing: 2 or 4 Cog cycles, 2 or 13...20 Hub cycles. The manual appendix-A encoding table at lines 340-341 lists TJNS and TJNZ both with '2 or 4'. The proposed range: 13...20 addition mirrors the tjz.yaml / tjf.yaml pattern; note that the richer sibling pattern (tjs.yaml, tjnf.yaml) uses a 'notes' key instead, but both accurately represent the variable nature. The minimum required fix is changing type from fixed to variable. Adding range: 13...20 is a secondary improvement consistent with the tjz/tjf siblings. No compiler probe was run as this is a YAML metadata field (timing.type), not a compilable construct — the CSV and appendix-A are sufficient silicon authorities.

#### F-048 — `calla.yaml`: The manual adds a Hub-execution timing figure '13+' that no available KB authority …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/calla.yaml`, `deliverables/ai/P2/language/pasm2/callb.yaml`

**Fix applied:**
- Add hub-exec timing (14-32) to timing.cycles, matching the CSV primary source (14...32 *) and the current manual (14-32). RETA already uses this pattern.
- Add hub-exec timing (14-32) to timing.cycles, matching the CSV primary source and current manual.

**How verified (compiler):** N/A — timing/cycle values are not compilable assertions; verified from CSV and silicon doc authoritative sources directly.

**Sources that proved it:**
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:344,346,428,429 — CALLA/CALLB cog=5...12 *, hub-exec=14...32 *
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:743-744 — 'Branching to a hub address takes a minimum of 13 clock cycles. If the instruction being branched to is not long-aligned, one additional clock cycle is required.'
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-c.md:73-74,91 — CALLA table '5-12 / 14-32'; prose '14-32 cycles for Hub execution'
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-c.md:117-118,135 — CALLB table '5-12 / 14-32'; prose '14-32 cycles for Hub execution'
- deliverables/ai/P2/language/pasm2/calla.yaml:15-17 — timing.cycles currently '5-12', no hub figure
- deliverables/ai/P2/language/pasm2/callb.yaml:18-20 — timing.cycles currently '5-12', no hub figure
- deliverables/ai/P2/language/pasm2/reta.yaml:9-12 — timing.cycles '11...18 (cog) / 20...40 (hub-exec)' — sibling pattern to follow
- deliverables/ai/P2/language/PASM2-ENCODING-REFERENCE.md:65,66 — CALLA Cyc '5-12', CALLB Cyc '5-12', no hub figure
- engineering/tools/gen-pasm2-encoding-reference.py:70-75 — confirms encoding reference derives Cyc from timing.cycles YAML field

**Why / rationale:** PARTIAL verdict: The core defect is CONFIRMED — calla.yaml and callb.yaml both lack hub-exec timing in timing.cycles (only '5-12' present today, no hub figure). The PASM2-ENCODING-REFERENCE.md also shows just '5-12' for both. However, F-048's proposed correction value '13+' is WRONG. The CSV primary source (P2 Instructions v35 - Rev B_C Silicon, rows 344/346/428/429) gives '14...32 *' for hub-exec on all four CALLA/CALLB encoding rows. The current manual (instructions-c.md:73-74,91 and 117-118,135) already uses '14-32', consistent with the CSV — it appears the manual was already corrected (possibly via F-049 work). The fix is: set timing.cycles to '5-12 (cog/LUT) / 14-32 (hub-exec)' in both YAMLs, following the RETA pattern. The PASM2-ENCODING-REFERENCE.md is generated (gen-pasm2-encoding-reference.py reads timing.cycles) and will correct itself on regen after the YAML fixes. Fix scope: yaml_source for the two YAMLs; gen_script regen for the encoding reference. Finding's claim that the manual showed '13+' is no longer true — the manual already shows '14-32', so no manual fix is needed."

#### F-049 — `call.yaml`: Same as CALLA: the manual adds an unsourced Hub-execution figure '13+' not present in the …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/calla.yaml`, `deliverables/ai/P2/language/pasm2/callb.yaml`

**Fix applied:**
- Add Hub-execution timing figure to timing.cycles and to both encoding row clocks fields. CSV primary source confirms Hub = 14...32 * for CALLA.
- Update both encoding row clocks fields from '5...12 *' (COG-only) to '5-12 / 14-32' (COG + Hub).
- Add Hub-execution timing figure to timing.cycles. CSV primary source confirms Hub = 14...32 * for CALLB.

**Sources that proved it:**
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-c.md:73-74 (CALLA table rows, clocks '5-12 / 14-32')
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-c.md:91 (CALLA explanation: '14-32 cycles for Hub execution')
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-c.md:117-118 (CALLB table rows, clocks '5-12 / 14-32')
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-c.md:135 (CALLB explanation: '14-32 cycles for Hub execution')
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:320,322,404,405 (CALLA/CALLB both show COG=5...12 *, Hub=14...32 *)
- deliverables/ai/P2/language/pasm2/calla.yaml:15-16 (timing.cycles: 5-12, clocks: 5...12 * — Hub figure absent)
- deliverables/ai/P2/language/pasm2/callb.yaml:19,26,31 (timing.cycles: 5-12, clocks: 5...12 * — Hub figure absent)
- deliverables/ai/P2/language/PASM2-ENCODING-REFERENCE.md:65-66 (Cyc column shows '5-12' for both CALLA and CALLB — Hub figure absent)

**Why / rationale:** The finding has two sub-issues. SUB-ISSUE A (manual shows '13+' instead of '14-32'): Already fixed — instructions-c.md now correctly shows '5-12 / 14-32' at lines 73-74, 91, 117-118, 135. No '13+' appears anywhere in the file. SUB-ISSUE B (calla.yaml, callb.yaml, and PASM2-ENCODING-REFERENCE.md omit the Hub execution figure entirely): Still present. Both YAMLs have timing.cycles: 5-12 and clocks: 5...12 * with no Hub figure; the ENCODING-REFERENCE rows for both show '5-12' only. The CSV primary source (P2 Instructions v35 Rev B_C, rows 320/322/404/405) independently confirms COG/LUT=5...12 *, Hub=14...32 * for both CALLA and CALLB. The proposed correction of 14-32 is verified correct. Fix_target is yaml_source because PASM2-ENCODING-REFERENCE.md is generated from the YAMLs via gen-pasm2-encoding-reference.py (which reads timing.cycles first); fixing the YAMLs and regenerating will update the encoding reference automatically. The call.yaml sibling (already correct) uses the format 'cycles: 4 / 13-20' style, so '5-12 / 14-32' is consistent.

#### F-063 — `waitxro.yaml`: WAITXRO is an unbounded blocking event-wait (clocks 2+), so timing.type: fixed is wrong; …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/waitxro.yaml`

**Fix applied:**
- Change timing.type from 'fixed' to 'variable' — WAITXRO is an unbounded blocking event-wait (clocks '2+'), not a fixed-cycle instruction. It is the sole outlier among all 14 sibling WAIT* event-wait YAMLs which all declare type: variable.

**Sources that proved it:**
- deliverables/ai/P2/language/pasm2/waitxro.yaml:30-32 (timing block — confirmed type: fixed present today)
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:299 (WAITXRO clocks = '2+' — variable, not fixed)
- engineering/ingestion/sources/p2-datasheet/pasm2-complete-instruction-tables.md:404 (WAITXRO | 2+ )
- deliverables/ai/P2/language/pasm2/waitxfi.yaml, waitxmt.yaml, waitxrl.yaml, waitatn.yaml, waitse1-4.yaml, waitct1-3.yaml, waitpat.yaml, waitfbw.yaml, waitint.yaml — all 14 sibling WAIT* YAMLs: timing.type = variable
- deliverables/ai/P2/language/pasm2/pollxro.yaml — POLLXRO (non-blocking sibling) correctly uses type: fixed, confirming WAIT vs POLL distinction

**Why / rationale:** The defect is confirmed. WAITXRO.yaml declares timing.type: fixed while its own encoding.clocks field says '2+' (line 38), the P2 Instructions v35 CSV confirms '2+', and all 14 sibling WAIT* event-wait YAMLs declare type: variable. The contrast with POLLXRO (type: fixed, clocks: 2, truly deterministic) makes the intended semantics clear: POLL instructions are fixed; WAIT instructions are variable because they block until an asynchronous event occurs. WAITXRO's own description (lines 5-19) explicitly states 'the pipeline is stalled' until the event — definitionally variable. The fix is a single field change in the YAML; no manual edit is needed.

#### F-066 — `wmlong.yaml`: Manual and wmlong.yaml agree on `3...10`; the encoding-reference row shows a bare `3` and …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/wmlong.yaml`

**Fix applied:**
- Fix timing block: cycles is bare 3 (wrong) because the generator reads timing.cycles before encoding[0].clocks. Match WRLONG pattern: set cycles to the full cog/hub-exec range string, type to variable, add range_source note.

**Sources that proved it:**
- deliverables/ai/P2/language/pasm2/wmlong.yaml:8-11 (encoding.clocks='3...10 *'; timing.cycles=3; timing.type=fixed)
- deliverables/ai/P2/language/PASM2-ENCODING-REFERENCE.md:250 (WMLONG row shows bare '3' in Cyc column)
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:172 (WMLONG cog=3...10 *, hub-exec=3...20 *)
- engineering/tools/gen-pasm2-encoding-reference.py:70-75 (generator prefers timing.cycles over encoding[0].clocks)
- deliverables/ai/P2/language/pasm2/wrlong.yaml (timing.cycles='3...10 (cog) / 3...20 (hub-exec)', type=variable — correct pattern to match)

**Why / rationale:** Root cause identified: the generator script (gen-pasm2-encoding-reference.py:72-73) reads timing.cycles when present, bypassing encoding[0].clocks. wmlong.yaml has timing.cycles=3 (bare integer, wrong) and timing.type=fixed. The encoding[0].clocks field correctly says '3...10 *' but is never reached by the generator. The fix is entirely in wmlong.yaml — update timing.cycles to the full range string and timing.type to variable, matching the WRLONG YAML which correctly produces '3...10 (cog) / 3...20 (hub-exec)' in the generated table. The CSV at line 172 is authoritative: cog 3...10 *, hub-exec 3...20 *. After fixing wmlong.yaml, regenerating PASM2-ENCODING-REFERENCE.md will produce the correct row automatically. The PASM2-ENCODING-REFERENCE.md itself should NOT be hand-edited (it is generated output).

#### F-067 — `wrbyte.yaml`: Manual + wrbyte.yaml both carry the cog-vs-hub-exec range; the encoding-reference WRBYTE …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/wrbyte.yaml`

**Fix applied:**
- Fix timing.cycles from bare integer 3 to full range string matching wrlong.yaml and wrword.yaml. The gen script (gen-pasm2-encoding-reference.py line 73) reads t["cycles"] directly to produce the Clks column, so setting this to the full string produces the correct PASM2-ENCODING-REFERENCE.md output. The existing range field (3...10 / 3...20) is already correct but is not used by the generator.

**Sources that proved it:**
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:245 — WRBYTE cog=3...10, hub-exec=3...20
- deliverables/ai/P2/language/pasm2/wrbyte.yaml:9-12 — timing.cycles=3 (integer), range=3...10/3...20
- deliverables/ai/P2/language/PASM2-ENCODING-REFERENCE.md:251 — WRBYTE Clks shows bare '3'
- deliverables/ai/P2/language/PASM2-ENCODING-REFERENCE.md:252-253 — WRLONG/WRWORD Clks show '3...10 (cog) / 3...20 (hub-exec)'
- deliverables/ai/P2/language/pasm2/wrlong.yaml:17 — timing.cycles = full string '3...10 (cog) / 3...20 (hub-exec)'
- deliverables/ai/P2/language/pasm2/wrword.yaml:10 — timing.cycles = full string '3...10 (cog) / 3...20 (hub-exec)'
- engineering/tools/gen-pasm2-encoding-reference.py:70-75 — generator uses t['cycles'] directly for the Clks column

**Why / rationale:** Root cause confirmed: wrbyte.yaml has timing.cycles set to integer 3, while sibling wrlong.yaml and wrword.yaml both have timing.cycles as the full string \"3...10 (cog) / 3...20 (hub-exec)\". The generator (gen-pasm2-encoding-reference.py line 73) outputs t[\"cycles\"] directly for the Clks column, producing bare '3' for WRBYTE. The CSV (line 245) gives WRBYTE the identical timing as its siblings: 3...10 cog / 3...20 hub-exec. The wrbyte.yaml also has a separate 'range: 3...10 / 3...20' field that is correct but unused by the generator. Fixing timing.cycles in wrbyte.yaml to the full range string (matching wrlong/wrword) will cause the next generator run to produce the correct PASM2-ENCODING-REFERENCE.md row. The encoding.clocks field (line 8) also only shows '3...10' (missing hub-exec suffix) but the generator only uses that as a fallback when timing is absent, so it does not need to be changed to fix the .md output. No change is needed to the .md directly — it is generated.


### Flag semantics

#### F-026 — `getct.yaml`: GETSCP YAML records write: '—' although GETSCP writes D (manual, CSV description, and …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/getscp.yaml`

**Fix applied:**
- Fix encoding[0].write from '—' (no write) to 'D' — GETSCP writes four 8-bit oscilloscope samples packed into the destination register D

**How verified (compiler):** pnut-ts /tmp/test_getscp.spin2 — PASS (exit 0, wrote 6300-byte binary). GETSCP $1FF accepted as valid destination-operand form, confirming D is written.

**Sources that proved it:**
- deliverables/ai/P2/language/pasm2/getscp.yaml:5 (write: — confirmed present)
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-g.md:324 (Result written to Dest) and :331 (Result column = D)
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:8835 ('Get the lower-byte RDPIN values of four pins into the bytes of D')
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:425 (row 401 description: 'into D. D = {ch3[7:0],ch2[7:0],ch1[7:0],ch0[7:0]}')
- pnut-ts compiler: GETSCP $1FF assembled cleanly (exit 0, 6300-byte binary produced) confirming D is the destination operand
- deliverables/ai/P2/language/pasm2/getct.yaml:6 and getrnd.yaml:6 (sibling D-writing instructions both correctly use write: D)

**Why / rationale:** All four primary sources agree: GETSCP writes four 8-bit oscilloscope samples packed into D. The manual (instructions-g.md:324,331), silicon doc (p2-documentation.txt:8835), CSV row 401 description, and compiler all confirm D is the write destination. The `write: —` in getscp.yaml encoding[0] is an authoring error. The flags (C: No effect, Z: No effect) are correct and consistent with all sources — only the write field needs changing. Sibling instructions getct.yaml and getrnd.yaml (the D-writing forms) already correctly specify write: D and require no changes.

#### F-035 — `lockrel.yaml`: The yaml's encoding.c and flags_affected.C ('no effect') contradict both the manual AND …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/lockrel.yaml`

**Fix applied:**
- Fix encoding.c and flags_affected.C to reflect that WC causes C = lock-taken status. The current '—' / 'No effect' values contradict the YAML's own description, the silicon doc (part4-locks.txt line 5: 'C flag will indicate whether the lock is currently taken'), and the compiler (WC compiles clean, sets C-bit=1 in encoding; WZ rejected).
- Fix flags_affected.C from 'No effect' to the correct WC behavior per silicon doc and compiler probe.

**How verified (compiler):** pnut-ts /tmp/test_lockrel4.spin2 (DAT block: 'lockrel #5 wc' and 'lockrel #5') → exit 0, 8 bytes; decoded: wc=0xfd740a07 C-bit=1; no-wc=0xfd640a07 C-bit=0. Separately: 'lockrel #5 wz' → exit 1, 'This effect is not allowed'.

**Sources that proved it:**
- /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/silicon-doc/part4-locks.txt:5-8 — 'When LOCKREL is executed with WC, the C flag will indicate whether the lock is currently taken.'
- /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:271 — LOCKREL description 'LOCK status into C', encoding 'EEEE 1101011 C0L DDDDDDDDD 000000111'
- pnut-ts v1.55.0 probe /tmp/test_lockrel4.spin2: 'lockrel #5 wc' compiles (exit 0), C-bit=1 in encoding; 'lockrel #5' C-bit=0; 'lockrel #5 wz' rejected with 'This effect is not allowed'
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/pasm2/lockrel.yaml:3-8 (encoding.c='—', confirmed present today)
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/pasm2/lockrel.yaml:29-31 (flags_affected.C='No effect', confirmed present today)
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/pasm2/locktry.yaml:26-28 (comparable: flags_affected.C='Set if LOCK acquired')

**Why / rationale:** The YAML is self-contradictory: encoding.c='—' and flags_affected.C='No effect' directly contradict the YAML's own description field ('LOCK status into C'). Three independent primary sources all confirm WC sets C = lock-taken status: (1) silicon doc part4-locks.txt lines 5-8 (explicit), (2) canonical instruction CSV row 247 (description text), (3) pnut-ts compiler (WC accepted, C-bit toggled in encoded word; WZ rejected). The fix is YAML-only; PASM2-ENCODING-REFERENCE.md line 218 also shows 'C,Z' in the flags column (Z is wrong — WZ rejected), but that file is generated from the YAMLs, so correcting lockrel.yaml and regenerating fixes the derived file automatically. The encoding.z:'—' and flags_affected.Z:'No effect' fields are CORRECT and must not be changed.

#### F-058 — `rdbyte.yaml`: Manual says RDLONG updates Z (result==0) under WZ/WCZ; rdlong.yaml says Z has no effect. …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/rdlong.yaml`

**Fix applied:**
- Fix Z-flag fields: rdlong.yaml incorrectly states Z has 'No effect' and z is '—'. The silicon doc (part3-end.txt:143) explicitly states 'If WZ is expressed, Z will be set if the data read from the hub equaled zero, otherwise Z will be cleared.' for the RDBYTE/RDWORD/RDLONG family. A compiler probe confirmed `rdlong result, ptra wz` compiles cleanly. Sibling instructions rdbyte.yaml and rdword.yaml both have z: Result = 0 / Z: Set if result equals zero.

**How verified (compiler):** pnut-ts /tmp/test_rdlong_wz.spin2 — inline PASM `rdlong result, ptra wz` → Wrote /tmp/test_rdlong_wz.bin (6304 bytes), no errors. Confirms WZ is accepted by the compiler for RDLONG.

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/part3-end.txt:133-143 (RDBYTE/RDWORD/RDLONG all CZI + {WC/WZ/WCZ}; line 143: 'If WZ is expressed, Z will be set if the data read from the hub equaled zero, otherwise Z will be cleared.')
- engineering/ingestion/sources/silicon-doc/part3-end.txt:281 ('If WC/WZ/WCZ are used with RDLONG, the flags will be set according to the last long read in the sequence.')
- deliverables/ai/P2/language/pasm2/rdlong.yaml:8 (z: —) and :26 (Z: No effect) — current incorrect values
- deliverables/ai/P2/language/pasm2/rdbyte.yaml:7 (z: Result = 0) and :17 (Z: Set if result equals zero)
- deliverables/ai/P2/language/pasm2/rdword.yaml:7 (z: Result = 0) and :18 (Z: Set if result equals zero)
- pnut-ts v1.55.0 probe: `rdlong result, ptra wz` compiled clean (Wrote /tmp/test_rdlong_wz.bin)

**Why / rationale:** Two fixes required in rdlong.yaml: (1) encoding[0].z: change '—' to 'Result = 0' (line 8); (2) flags_affected.Z: change 'No effect' to 'Set if result equals zero' (line 26). The silicon doc at part3-end.txt:133-143 groups RDBYTE, RDWORD, RDLONG together under a single shared rule for WZ — line 143 states it applies to all three. A second reference at line 281 further confirms WC/WZ/WCZ apply to RDLONG. The compiler accepts rdlong ... wz cleanly. The current YAML is the sole outlier among its siblings, and the proposed correction matches sibling YAMLs exactly. A second Edit call is needed for the flags_affected.Z field: current 'Z: No effect' → proposed 'Z: Set if result equals zero' (line 26). The files[] array above covers line 8; the line-26 fix uses: current_snippet = '  C: Set to MSB of long\n  Z: No effect', proposed_snippet = '  C: Set to MSB of long\n  Z: Set if result equals zero'.

#### F-064 — `waitx.yaml`: The Result line states 'Sets C and Z to 0 after completion' unconditionally, but flag …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/waitx.yaml`

**Fix applied:**
- Fix description to remove 'always' and tie C/Z clearing to WC/WZ/WCZ; fix flags_affected C and Z to state the WC/WZ/WCZ condition

**How verified (compiler):** pnut-ts /tmp/waitx_pasm.spin2 → encoded WAITX #10 as 0xfd64141f (C=0,Z=0 in word = flags NOT written); WAITX #10 wc as 0xfd74141f (C=1 = C flag written to 0); WAITX #10 wz as 0xfd6c141f (Z=1 = Z flag written to 0); WAITX #10 wcz as 0xfd7c141f (C=1,Z=1 = both flags written to 0). Confirms C/Z only written when WC/WZ/WCZ requested.

**Sources that proved it:**
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:290 (WAITX row)
- engineering/ingestion/sources/silicon-doc/silicon-doc-complete-sample.txt (CZ bit definition: C=0 Do not update C register, C=1 Update C register)
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-w.md:231,234,239 (WAITX Result and encoding table)
- deliverables/ai/P2/language/pasm2/waitx.yaml:12-22 (description and flags_affected)
- pnut-ts v1.55.0 probe: compiled WAITX #10, WAITX #10 wc, WAITX #10 wz, WAITX #10 wcz — binary decode confirmed C=0/Z=0 bits in instruction word when no WC/WZ/WCZ (flags not written); C=1/Z=1 only when WC/WZ/WCZ present

**Why / rationale:** PARTIAL verdict: The YAML defect is real and confirmed, but the finding's characterization of manual line 231 as 'wrong/unconditional' is itself incorrect. Manual instructions-w.md:231 reads 'If WC/WZ/WCZ is specified, waits 2 + (Dest AND RND) clocks for a randomized delay and clears C and Z to 0 after completion' — the 'and clears C and Z' is grammatically inside the 'If WC/WZ/WCZ is specified' conditional clause, so the manual is ALREADY CORRECT. No manual edit is needed.

The YAML has two genuine defects: (1) waitx.yaml description line 15 says 'C and Z are always cleared to 0 after completion' as a stand-alone sentence that escapes the preceding WC/WZ/WCZ conditional — 'always' is wrong; the sentence must remain inside the WC/WZ/WCZ clause. (2) flags_affected.C and flags_affected.Z say 'Set to 0 after completion' unconditionally — these must state the WC/WZ/WCZ condition.

The encoding section (c: 0, z: 0) is CORRECT — those fields document the result VALUE written when the flag is enabled (per P2 silicon universal convention: C/Z bits in instruction word are write-enables; 0 = do not write; the 'c: 0' and 'z: 0' in encoding mean the result written IS 0, when WC/WZ is requested).

Primary authority chain: silicon-doc confirms C-bit in encoding = write-enable; CSV:290 says 'C/Z = 0' meaning result-when-written is 0; compiler probe confirms no-WC/WZ = flags untouched.

#### F-082 — `adds.yaml`: The manual describes ADDS/SUBS C two contradictory ways across §3.4.1 and §3.7.1. The …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/adds.yaml`, `deliverables/ai/P2/language/pasm2/subs.yaml`

**Fix applied:**
- Fix flags_affected.C from 'signed overflow' framing to 'true sign of result' per CSV authority. Fix description to remove 'signed overflow (signed carry)' framing and replace with true-sign semantics.
- Fix description to remove 'signed underflow (signed borrow)' framing and replace with true-sign semantics, consistent with flags_affected.C (which is already correct) and encoding.c.

**Sources that proved it:**
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:36 — ADDS: 'C = correct sign of (D + S)'
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:40 — SUBS: 'C = correct sign of (D - S)'
- engineering/ingestion/sources/chip-gracey-clarifications/chip-instruction-clarifications-2025-09-02.md:124-133 — table confirms ADDS/SUBS C Flag = 'true sign'
- deliverables/ai/P2/language/pasm2/adds.yaml:1-44 — current state read verbatim
- deliverables/ai/P2/language/pasm2/subs.yaml:1-57 — current state read verbatim

**Why / rationale:** Finding CONFIRMED. The core inconsistency is present TODAY in both YAMLs. adds.yaml is the more severe case: flags_affected.C reads 'Set if signed overflow (sign of D + S)' — the 'signed overflow' label directly contradicts the encoding.c field 'sign of (D + S)' and the CSV authority 'correct sign of (D + S)'. The description also uses 'signed overflow (signed carry)' framing. subs.yaml flags_affected.C is actually already correct ('Set to sign of result (1 if negative)') so only the description needs fixing — it still says 'signed underflow (signed borrow)'. The CSV (highest authority for PASM2 instruction semantics) is unambiguous on both: C is the CORRECT SIGN of the result, not an overflow or borrow detection flag. Chip Gracey clarifications table independently confirms 'true sign'. The fix_target is yaml_source for both files. The manual changes described in the finding (chapter-03-flags.md §3.4.1 table and prose) are out of YAML scope and are classified as 'manual' — they are NOT addressed here."

#### F-083 — `adds.yaml`: Prose asserts ADDS/SUBS C is a signed-overflow flag. Per the encoding authority the C …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/adds.yaml`, `deliverables/ai/P2/language/pasm2/subs.yaml`

**Fix applied:**
- Fix description and flags_affected.C: replace 'signed overflow (signed carry)' / 'no overflow' framing with the correct 'correct sign of the result (bit 31)' framing, matching the CSV authority 'C = correct sign of (D + S)'.
- Fix flags_affected.C label from 'signed overflow' to 'correct sign of result'.
- Fix description: replace 'signed underflow (signed borrow)' / 'no underflow' framing with the correct 'correct sign of the result (bit 31)' framing, matching the CSV authority 'C = correct sign of (D - S)'.

**How verified (compiler):** pnut-ts /tmp/test_adds.spin2 → compiled successfully (80 bytes); confirms ADDS/SUBS accept WC operand. Compiler does not expose flag semantics — CSV is ground truth for C-flag meaning.

**Sources that proved it:**
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:36 (ADDS row: 'C = correct sign of (D + S)')
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:40 (SUBS row: 'C = correct sign of (D - S)')
- deliverables/ai/P2/language/pasm2/adds.yaml:5,14,24 (description, flags_affected.C, encoding.c)
- deliverables/ai/P2/language/pasm2/subs.yaml:10-11,26,36 (description, flags_affected.C, encoding.c)
- pnut-ts compiler v1.55.0 — compiled /tmp/test_adds.spin2 successfully (ADDS/SUBS syntax valid)

**Why / rationale:** PARTIAL verdict: The finding is confirmed for both YAML files, but the scope is narrower than the finding's proposed correction implies. The finding's proposed correction targets the manual (opus-master/part-i/chapter-03-flags.md §3.4.1), which is out of YAML scope (fix_target=manual for that part). However, the YAML files themselves also carry the same wrong language in their description fields. The YAML fixes above address what IS in YAML scope. Details: (1) adds.yaml encoding.c='sign of (D + S)' is already correct — no change needed there. (2) subs.yaml flags_affected.C='Set to sign of result (1 if negative)' is already correct — no change needed there. (3) subs.yaml encoding.c='sign of (D - S)' is already correct. The defects confirmed: adds.yaml description uses 'signed overflow (signed carry)' and flags_affected.C uses 'Set if signed overflow'; subs.yaml description uses 'signed underflow (signed borrow)'. All three are contradicted by the CSV authority which specifies 'correct sign of (D+S)' and 'correct sign of (D-S)' — C reflects the true sign (bit 31) of the result regardless of whether arithmetic overflow occurred. The P1-derived 'signed overflow' interpretation is categorically wrong for P2. The manual fix (chapter-03-flags.md §3.4.1 rewrite) is a separate manual-scope item not addressed by YAML edits.

#### F-088 — `locknew.yaml`: Manual is CORRECT per the authoritative instruction YAML. The architecture locks.yaml has …  ·  `DONE`

**Files:** `deliverables/ai/P2/architecture/locks.yaml`

**Fix applied:**
- Fix LOCKNEW operation block: C=0 means success (lock allocated), C=1 means failure (all locks already allocated). Also fix both usage examples that incorrectly use IF_NC to jump on failure (C=0 is actually success, so IF_NC would jump on success). Line 98: change IF_NC to IF_C. Line 180: change IF_NC to IF_C.
- Fix dynamic_lock_allocation pattern: IF_NC should be IF_C to jump on failure (C=1 = all locks allocated).

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/part3-end.txt:494-497 — 'Zero (0) indicates success, while one (1) indicates that all locks are already allocated.'
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:7461-7463 — same wording confirmed
- deliverables/ai/P2/language/pasm2/locknew.yaml:6,16 — CORRECT: 'c: 1 if no LOCK available' / 'C: Set if no LOCK available'
- deliverables/ai/P2/architecture/locks.yaml:85-98 — WRONG: C:=1 (success) / C:=0 (no locks) / IF_NC JMP #no_locks
- deliverables/ai/P2/architecture/locks.yaml:179-180 — WRONG: IF_NC JMP #no_locks_error

**Why / rationale:** The finding is fully confirmed. The Silicon Doc (both part3-end.txt:494-497 and p2-documentation.txt:7461-7463) is unambiguous: for LOCKNEW WC, C=0 indicates success (lock was allocated) and C=1 indicates all locks are already allocated (failure). This matches locknew.yaml exactly (which is CORRECT). locks.yaml has the semantics completely inverted in the LOCKNEW operation block (lines 90 and 93) AND in two usage examples that use IF_NC to jump on failure — but IF_NC (not carry, i.e. C=0) is actually the SUCCESS case, so those examples would jump to the error handler on success and fall through on failure. Both errors must be fixed together. The locknew.yaml instruction YAML needs no changes.


### Inverted / stale jump-condition prose

#### F-032 — `ijnz.yaml`: The YAML ijnz.yaml encoding note says PC is written 'only when the result in Dest is zero …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/ijnz.yaml`

**Fix applied:**
- Fix encoding_notes to correctly state PC is written when result is NOT zero (IJNZ behavior), removing the inverted 'zero' wording and the stale '(or not zero in syntax 2)' parenthetical.

**How verified (compiler):** pnut-ts v1.55.0 — compiled /tmp/test_ijnz6.spin2 with both IJNZ and IJZ instructions; exit 0, wrote 6308-byte binary. Confirms both instructions are accepted by the compiler with the correct syntax form D,{#}S. Semantics (NOT zero vs zero) verified from CSV and manual, not from binary decode (encoding bit difference is 00I vs 01I in opcode field, single-bit distinction not easily isolated from binary dump).

**Sources that proved it:**
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:197 — IJNZ: 'Increment D and jump to S** if result is not zero.' (encoding EEEE 1011100 01I)
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:196 — IJZ: 'Increment D and jump to S** if result is zero.' (encoding EEEE 1011100 00I)
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-i.md:50-53 — explanation table: IJNZ jumps when 'Result != 0', IJZ jumps when 'result == 0'
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-i.md:40 — footnote: 'PC is written only when the jump condition is met.'
- deliverables/ai/P2/language/pasm2/ijnz.yaml:5-6 — description says 'jumps ... if the result is NOT zero' (contradicts its own encoding_notes)
- deliverables/ai/P2/language/pasm2/ijnz.yaml:11-12 — result field says 'If the result is not zero, PC is set ...' (also contradicts encoding_notes)
- deliverables/ai/P2/language/pasm2/ijz.yaml — confirmed: has no encoding_notes field (no stale note to fix)

**Why / rationale:** The defect is clear and internally contradicted: ijnz.yaml's own description (line 5-6) and result (line 11-12) correctly say IJNZ jumps when result is NOT zero, but the encoding_notes (lines 32-33) inverts this and says 'only when the result in Dest is zero'. The CSV (ground-truth encoding reference) confirms IJNZ = 01I = 'not zero', IJZ = 00I = 'zero'. The stale '(or not zero in syntax 2)' parenthetical is a vestige from when IJZ/IJNZ shared a single combined note; it should be removed entirely. ijz.yaml correctly has no encoding_notes and requires no change.

#### F-056 — `djf.yaml`: The YAML note states PC is written when the result is "full", but DJNF writes PC (jumps) …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/djnf.yaml`

**Fix applied:**
- Fix inverted logic in encoding_notes: DJNF jumps (writes PC) when result is NOT full, not when full. Drop the spurious '(or not full in syntax 2)' clause — DJNF has no syntax-2 variant.

**How verified (compiler):** N/A — bit-field logic (full vs not-full condition) is a doc/spec question, not a compilability question; compiler probe would not distinguish the inverted clause

**Sources that proved it:**
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:195 — 'DJNF ... Decrement D and jump to S** if result is not $FFFF_FFFF'
- deliverables/ai/P2/language/pasm2/djnf.yaml:4-14 — description and result fields both correctly state 'NOT full / not equal to $FFFF_FFFF'
- deliverables/ai/P2/language/pasm2/djnf.yaml:34-35 — encoding_notes states 'full' (inverted) with spurious '(or not full in syntax 2)'
- deliverables/ai/P2/language/pasm2/djnf.yaml — no syntax_variants field; DJNF has exactly one syntax
- engineering/ingestion/sources/silicon-doc/silicon-doc-v35-walkthrough-audit.md:3966 — DJZ/DJNZ/DJF/DJNF listed as 'Decrement and jump'

**Why / rationale:** The defect is isolated to djnf.yaml lines 34-35 (encoding_notes). The YAML's own description (line 6: 'jumps if the result is NOT full'), result (line 12: 'does NOT equal $FFFF_FFFF'), and oneliner (line 47) are all correct. Only the encoding_notes clause is inverted. The finding's mention of djf.yaml as a co-target is not actionable — djf.yaml has no encoding_notes field at all and needs no change. CSV row 171 (file line 195) is the decisive primary source: 'if result is not $FFFF_FFFF'. The '(or not full in syntax 2)' parenthetical is confirmed spurious — DJNF has one encoding (EEEE 1011011 11I) and no syntax_variants key.

#### F-057 — `djnz.yaml`: The YAML note states PC is written when the result is "zero", but DJNZ writes PC (jumps) …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/djnz.yaml`

**Fix applied:**
- Fix inverted jump condition in encoding_notes: DJNZ jumps (writes PC) when result is NOT zero, not when zero. Also remove the spurious '(or not zero in syntax 2)' clause — DJNZ has only one syntax.

**How verified (compiler):** pnut-ts /tmp/test_djnz.spin2 — compiled clean (djnz pa, #.loop accepted); wrote /tmp/test_djnz.bin (6312 bytes)

**Sources that proved it:**
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-d.md:447-450 — table: DJZ jumps when result==0, DJNZ when Result!=0
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:10736-10741 — encoding EEEE 1011011 01I = DJNZ, confirming separate opcode from DJZ (00I)
- deliverables/ai/P2/language/pasm2/djnz.yaml:4-6 — YAML's own description correctly states 'jumps to the address described by Src if the result is NOT zero'
- pnut-ts v1.55.0: djnz compile /tmp/test_djnz.spin2 — compiled clean, wrote /tmp/test_djnz.bin (6312 bytes)

**Why / rationale:** The suspect text is present today at djnz.yaml lines 32-33: 'PC is written only when the result in Dest is zero (or not zero in syntax 2).' This directly contradicts: (1) the YAML's own description field (lines 4-6) which correctly says 'if the result is NOT zero'; (2) the manual table at instructions-d.md:450 which shows DJNZ jumps when 'Result != 0'; (3) the silicon doc which gives DJNZ a distinct encoding (01I) separate from DJZ (00I). DJNZ = Decrement and Jump if Not Zero — the primary clause in encoding_notes is inverted. Additionally, DJNZ has only one syntax, so the '(or not zero in syntax 2)' parenthetical is spurious. The oneliner field (line 45: 'Decrement, jump if zero or not zero') is also misleading in isolation but the finding does not propose changing it, so it is out of scope here.

#### F-101 — `tjnz.yaml`/`tjns.yaml` carry inverted jump-condition prose (TJ-family analog of F-032)  ·  `DONE`

_Applied directly from the register's pre-confirmed evidence (Spin2 v55 conflict audit, compiler-probed twice). See the register entry for full per-fact verification._


### Field / bit / value labels

#### F-059 — `rolbyte.yaml`: The ROLBYTE YAML mislabels the index field as a 'nibble ID'. ROLBYTE selects one of four …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/rolbyte.yaml`

**Fix applied:**
- Replace 'nibble ID' with 'byte ID' in the Num parameter description on line 19. ROLBYTE operates on bytes (NN = 2-bit, 0-3), not nibbles. The rest of the YAML correctly uses byte terminology; this line is an internal contradiction and a copy-paste artifact from ROLNIB.

**Sources that proved it:**
- deliverables/ai/P2/language/pasm2/rolbyte.yaml:19 (suspect text verbatim confirmed)
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-r.md:1133 — 'N is a 2-bit literal (0-3) identifying the byte position in Src.'
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:118 — 'Rotate-left byte N of S into D'
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:1149-1152 — 'ROL byte into value'

**Why / rationale:** The suspect text is present today (line 19: 'nibble ID'). All three independent primary sources — the PASM2 manual (line 1133), the P2 Instructions CSV (row 94), and the silicon doc — consistently confirm ROLBYTE operates on bytes, not nibbles. The YAML is also internally inconsistent: its own description (lines 6-11) and result (lines 12-14) correctly use 'byte', making line 19's 'nibble ID' a clear copy-paste artifact from ROLNIB. The fix is a single-word change: 'nibble' → 'byte'.

#### F-060 — `rolword.yaml`: The ROLWORD YAML mislabels the index field as a 'nibble ID'. ROLWORD selects one of two …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/rolword.yaml`

**Fix applied:**
- Replace 'nibble ID' with 'word ID' in the Num parameter description on line 19.

**Sources that proved it:**
- deliverables/ai/P2/language/pasm2/rolword.yaml:19 (suspect text present verbatim)
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-r.md:1203 (N is a 1-bit literal (0-1) identifying the word position in Src)
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv row 100 (Rotate-left word N of S into D)
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:1175-1178 (ROL word into value)

**Why / rationale:** The suspect text is present today on rolword.yaml line 19. All three independent primary sources agree the N field is a word selector: (1) the manual opus-master instructions-r.md:1203 says 'word position', (2) the CSV encoding reference (row 100) says 'Rotate-left word N of S', and (3) the silicon-doc confirms ROLWORD is in the WORD family alongside ROLNIB (nibbles) and ROLBYTE (bytes). The YAML's own description (lines 6, 9, 13) also uses 'word' consistently — only line 19's parameter line uses 'nibble ID', a clear copy-paste artifact from the nibble-family instructions. The fix is a single-word change from 'nibble' to 'word'.

#### F-061 — `setbyte.yaml`: The manual is correct (N selects a byte, 0-3). The matching SETBYTE YAML mislabels the N …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/setbyte.yaml`

**Fix applied:**
- Replace 'nibble ID' with 'byte ID' in Num parameter description — SETBYTE operates on bytes (8-bit), not nibbles (4-bit); the 2-bit N field selects one of 4 bytes.

**How verified (compiler):** pnut-ts /tmp/test_setbyte.spin2 — PASS (exit 0, wrote test_setbyte.bin). Test encoded SETBYTE with N=0,1,2,3 confirming 2-bit byte-index semantics.

**Sources that proved it:**
- deliverables/ai/P2/language/pasm2/setbyte.yaml:18 — current text 'nibble ID' confirmed present
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-s.md:166 — 'N is a 2-bit literal (0-3) identifying the byte of Dest to modify.'
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:114 — 'Set S[7:0] into byte N in D, keeping rest of D same.'
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:1138 — 'set byte to value'
- pnut-ts v1.55.0 compile probe: /tmp/test_setbyte.spin2 compiled clean with N=0..3 byte indices

**Why / rationale:** The suspect text is present today at setbyte.yaml:18. All primary sources agree: SETBYTE's N operand selects a byte (8-bit unit), not a nibble (4-bit unit). The CSV at line 114 says 'byte N'; the manual (instructions-s.md:166) says 'byte of Dest'; the silicon doc (p2-documentation.txt:1138) says 'set byte to value'. The word 'nibble' is a copy-paste artifact, almost certainly from the adjacent SETNIB instruction family where nibble selection is correct. SETNIB uses a 3-bit index (0-7) for nibbles; SETBYTE uses a 2-bit index (0-3) for bytes — the index width alone confirms the byte interpretation. The compiler probe compiled successfully with the expected range.

#### F-062 — `signx.yaml`: SIGNX is Sign Extend and the manual correctly says 'sign-extend beyond'; the YAML wrongly …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/signx.yaml`

**Fix applied:**
- Fix Src parameter description: 'zero-extend beyond' is ZEROX behaviour; SIGNX sign-extends. All other description fields in this file (lines 6-7, 13, 16) and the manual (opus-master/part-ii/instructions-s.md:998) correctly say 'sign-extend beyond'. Change 'zero-extend' to 'sign-extend'.

**Sources that proved it:**
- deliverables/ai/P2/language/pasm2/signx.yaml:15-19 (Src param — suspect text confirmed present)
- deliverables/ai/P2/language/pasm2/signx.yaml:5-11 (description: 'sign-extending the value')
- deliverables/ai/P2/language/pasm2/signx.yaml:12-14 (result: 'sign-extended above the bit')
- deliverables/ai/P2/language/pasm2/signx.yaml:16 (Dest param: 'sign-extend above bit Src[4:0]')
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-s.md:998 ('identifies the bit of Dest to sign-extend beyond')
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:100 ('Sign-extend D from bit S[4:0]')
- deliverables/ai/P2/language/pasm2/zerox.yaml:23 (ZEROX Src param correctly says 'zero-extend beyond' — confirms SIGNX line 19 is a copy-paste defect from ZEROX)

**Why / rationale:** Defect confirmed with high confidence. The SIGNX YAML's Src parameter at line 19 reads 'zero-extend beyond', which is ZEROX behaviour. Every other reference in the same file (description, result, Dest param) and all external authorities (CSV, manual opus-master:998) consistently say 'sign-extend'. The single erroneous line is a clear copy-paste artifact from zerox.yaml — both YAMLs share structurally identical wording and only the operation name differs. The fix is to change 'zero-extend' to 'sign-extend' in that one line. No manual change required (manual is already correct at line 998).

#### F-080 — `addressing_modes.yaml`: Half the claim is corroborated (-32..+31). The '1 to 16' updating range is unverifiable …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/concepts/addressing_modes.yaml`

**Fix applied:**
- Add index_range field to post_modify entry documenting that the updating-form index magnitude is 1 to 16 (per Silicon Doc part3-end.txt:185,192)

**How verified (compiler):** N/A — bit-field encoding range; not compilable to verify from compiler output

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/part3-end.txt:184-185 — INDEX6 = -32..+31 for non-updating offsets; INDEX = 1..16 for ++'s and --'s
- engineering/ingestion/sources/silicon-doc/part3-end.txt:192-193 — NNNNN = INDEX, uses %00001..%01111 for 1..15 and %00000 for 16; nnnnn = -INDEX, uses %10000..%11111 for -16..-1
- deliverables/ai/P2/language/pasm2/concepts/addressing_modes.yaml:47 — index_range: -32 to +31 (5-bit signed) present for indexed mode
- deliverables/ai/P2/language/pasm2/concepts/addressing_modes.yaml:75-82 — post_modify block confirmed to have NO index_range field

**Why / rationale:** The finding's premise is CONFIRMED. The YAML correctly documents index_range: -32 to +31 for the non-updating indexed mode (line 47). However, the post_modify block (lines 75-82), which covers updating forms like PTRx++[INDEX], has no index_range field at all — the '1 to 16' updating-form range is missing. The Silicon Doc at part3-end.txt:185 states explicitly 'INDEX = 1..16 for ++'s and --'s', and line 192 gives the encoding '%00001..%01111 for 1..15 and %00000 for 16' (positive direction) and line 193 'nnnnn = -INDEX, uses %10000..%11111 for -16..-1' (negative direction). The magnitude is 1..16 in both directions. The finding's original audit suspicion that '1 to 16 looks like only the positive sub-range and may be imprecise' is incorrect — '1 to 16' is the correct specification since 0 is excluded (0 = no-update) and the sign is captured by the ++ vs -- syntax. The manual's phrasing 'INDEX = 1..16 for ++'s and --'s' exactly matches the Silicon Doc. Fix: add index_range field to the post_modify block in the YAML. Note that F-091 is a related finding that also flags the '5-bit signed' label on the non-updating index_range as incorrect (it should be '6-bit signed' since -32..+31 requires 6 bits). These are separate issues. The proposed_snippet in this finding addresses only the post_modify gap (F-080 scope).")

#### F-086 — `execf.yaml`: The MANUAL matches the authoritative EXECF encoding ([9:0]=address, [31:10]=skip, 22 …  ·  `DONE`

**Files:** `deliverables/ai/P2/architecture/xbyte_engine.yaml`

**Fix applied:**
- Fix inverted bit-field layout in lut_table_format. The entry_format block has [31:23]=address (9 bits) and [22:0]=SKIPF (23 bits) — both ranges and bit-counts are wrong. Silicon Doc is unambiguous: 10 LSBs (D[9:0]) = jump address, 22 MSBs (D[31:10]) = SKIPF pattern. Fix execf_operation block to match.

**How verified (compiler):** N/A — bit-field layout is a silicon architecture fact, not compilable behavior; pnut-ts probe would not add signal here.

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/part2-beginning.txt:87-88 — verbatim: 'the 10 LSBs are an address to jump to in cog/LUT RAM and the 22 MSBs are a SKIPF pattern to be applied'
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:1913-1914 — verbatim: 'getting a 10-bit branch address from D[9:0] and a 22-bit skip pattern from D[31:10]'
- deliverables/ai/P2/language/pasm2/execf.yaml:9 — description correctly states 'Jump to D[9:0] in cog/LUT and set SKIPF pattern to D[31:10]' (already correct, no change needed)
- deliverables/ai/P2/architecture/xbyte_engine.yaml:160-168 — confirmed defective: [31:23]=address(9 bits) and [22:0]=SKIPF(23 bits), both ranges and bit counts wrong

**Why / rationale:** execf.yaml is already correct (D[9:0]=address, D[31:10]=SKIPF) — no change needed there. xbyte_engine.yaml lines 163-164 have both the bit ranges and the bit counts wrong: [31:23] is 9 bits (should be 10, range [9:0]) and [22:0] is 23 bits (should be 22, range [31:10]). The execf_operation block at lines 167-168 reinforces the same error. Two independent Silicon Doc passages (part2-beginning.txt and p2-documentation.txt) are unambiguous and in agreement with each other and with execf.yaml. Fix scope: xbyte_engine.yaml lut_table_format block only.

#### F-089 — `cordic.yaml`: The P2 CORDIC QLOG produces a base-2 logarithm in 5:27 fixed-point (whole part = bit …  ·  `DONE`

**Files:** `deliverables/ai/P2/architecture/cordic.yaml`

**Fix applied:**
- Fix QLOG block: change 'Natural logarithm (base e)' to 'Base-2 logarithm (5:27 fixed-point)', fix result field from 'ln(D) in X with 5.32 fixed-point format' to 'log2(D) in X with 5:27 fixed-point format'. Fix QEXP block: change 'Exponential (e^x)' to '2 to the power of D (antilog)', fix input_format from '5.32' to '5:27', fix result from 'e^D in X' to '2^D in X'.

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/part3-end.txt:450-453 — 'the top 5 bits hold the whole part of the power-of-2 exponent' / 'QLOG D/# - Compute log base 2 of D'
- engineering/ingestion/sources/silicon-doc/part3-end.txt:464-466 — 'QEXP D/# - Compute 2 to the power of D'
- deliverables/ai/P2/architecture/cordic.yaml:76-87 — suspect text confirmed present today
- deliverables/ai/P2/language/pasm2/qlog.yaml — checked; no 'natural log' or 'base e' language present; qlog.yaml itself is not erroneous

**Why / rationale:** CONFIRMED. cordic.yaml has a cluster of five related errors in the logarithm and exponential blocks, all stemming from confusing the P2 QLOG/QEXP base (base-2) with natural log (base-e): (1) line 78 operation 'Natural logarithm (base e)' — silicon doc states 'Compute log base 2 of D'; (2) line 80 result 'ln(D) in X with 5.32 fixed-point format' — should be 'log2(D)' and the fixed-point notation is 5:27 not 5.32; (3) line 84 operation 'Exponential (e^x)' — silicon doc states 'Compute 2 to the power of D'; (4) line 86 input_format '5.32 fixed-point' — should be '5:27'; (5) line 87 result 'e^D in X' — should be '2^D in X'. The qlog.yaml (pasm2) is NOT erroneous — it correctly uses 'logarithm' language without asserting a wrong base, and its 5:27/5-bit-whole-exponent description is consistent with base-2. The fix scope is cordic.yaml only. fix_target is yaml_source.

#### F-091 — `addressing_modes.yaml`: The YAML authority labels the -32..+31 non-updating index as '5-bit signed', but the …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/concepts/addressing_modes.yaml`

**Fix applied:**
- Correct index_range from '5-bit signed' to '6-bit signed'. The silicon doc uses a 6-bit field named INDEX6 (IIIIII = 6 I-bits) covering -32..+31 for non-updating offsets. A 5-bit signed field only covers -16..+15.

**How verified (compiler):** N/A — bit-field width is not a compilable fact; verified from silicon-doc encoding diagram.

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:6942 — INDEX6 = -32..+31 for non-updating offsets
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:6948 — IIIIII = INDEX6, uses %100000..%111111 for -32..-1 and %000000..%011111 for 0..31 (six I bits)
- deliverables/ai/P2/language/pasm2/concepts/addressing_modes.yaml:47 — suspect text confirmed present: index_range: -32 to +31 (5-bit signed)

**Why / rationale:** The silicon doc unambiguously encodes the non-updating index field as six I-bits ('IIIIII = INDEX6') and names it INDEX6, covering exactly -32..+31. By two's-complement arithmetic, -32..+31 (64 values) requires 6 bits; a 5-bit signed field covers only -16..+15. The YAML at line 47 says '5-bit signed' which is wrong. The suspect text is present today and has not been fixed. The proposed correction (change '5-bit signed' to '6-bit signed') matches the silicon doc precisely.

#### F-094 — `coginit.yaml`: The manual assigns HUBEXEC the bit pattern/hex that actually belongs to COGEXEC_NEW. …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/hubexec.yaml`

**Fix applied:**
- Fix HUBEXEC value from '%0_1_0000' ($10 = COGEXEC_NEW's value) to '%10_0000' ($20 = correct HUBEXEC value, bit 5 / E-bit set).

**How verified (compiler):** pnut-ts -l /tmp/hubexec_check.spin2 (CON aliases V_HUBEXEC=HUBEXEC, V_COGEXEC_NEW=COGEXEC_NEW etc.) → listing shows: V_HUBEXEC=00000020 ($20 = %10_0000), V_COGEXEC_NEW=00000010 ($10 = %01_0000). Confirms hubexec.yaml carries COGEXEC_NEW's value, not HUBEXEC's.

**Sources that proved it:**
- deliverables/ai/P2/language/pasm2/hubexec.yaml:9 — value: '%0_1_0000' (confirmed present, wrong)
- pnut-ts v1.55.0 listing probe /tmp/hubexec_check.lst — V_HUBEXEC=00000020, V_COGEXEC_NEW=00000010 (ground truth)
- engineering/ingestion/sources/spin2_lang_ref_v55/spin2-v55-text.txt:1661-1662 — %10_0000 HUBEXEC / %01_0000 COGEXEC_NEW (spec authority)
- deliverables/ai/P2/language/spin2/patterns/implementation/spin2_cog_management.yaml:19 — HUBEXEC value "%100000" (already correct)
- deliverables/ai/P2/language/spin2/symbols/spin2-builtin-symbols-complete.yaml:318-319 — value "$0000_0020" / bit_pattern "%10_0000" (already correct)
- deliverables/ai/P2/language/pasm2/coginit.yaml — no 'Bit 5' text found at line 23; line 23 is encoding: comment (no defect present in current file)

**Why / rationale:** PARTIAL: Only one of the four named files has a defect today. (1) hubexec.yaml line 9: value '%0_1_0000' = $10 is demonstrably wrong — pnut-ts and Spin2 v55 spec both give HUBEXEC = $20 = %10_0000. Correct value is '%10_0000'. (2) spin2_cog_management.yaml line 19: already shows HUBEXEC value \"%100000\" — correct, no fix needed. (3) spin2-builtin-symbols-complete.yaml lines 318-319: already shows \"$0000_0020\" / \"%10_0000\" — correct, no fix needed. (4) coginit.yaml: the finding's claim about \"line 23: Bit 5 set: Execute from hub RAM\" does not exist in the current file; line 23 is an encoding: comment. The coginit.yaml description on line 5 correctly states 'E controls loading (0=load from Hub, 1=no load)' — no defect. The manual appendix-e-constants.md defect cited in the finding is in the manual source (out of YAML scope); not addressed here. Only the hubexec.yaml fix is required for the YAML data set. Format choice: '%10_0000' matches the Spin2 v55 spec table format and is unambiguous; '%1_0_0000' (E_N_xVVV grouped) would also be numerically correct but is a style choice — '%10_0000' preferred to align with the authoritative spec table.")

#### F-096 — `cog_hub_execution.yaml`: '$000-$1F7' and '496 longs' cannot both be literally true (the range is 504 longs; 496 …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/concepts/cog_hub_execution.yaml`, `deliverables/ai/P2/language/spin2/methods/coginit.yaml`

**Fix applied:**
- Fix the memory_map under cog_execution: the range '$000_$1FF' with '496 longs' is wrong on two counts — $000-$1FF is 512 longs not 496, and labelling $1F0-$1FF as '16 special purpose registers' is wrong ($1F0-$1F7 are DUAL-PURPOSE per silicon doc, only $1F8-$1FF are truly special-purpose). Correct to three rows matching the silicon doc structure: $000-$1EF (496 general-purpose), $1F0-$1F7 (8 dual-purpose; loadable by COGINIT), $1F8-$1FF (8 special-purpose; not loaded by COGINIT).
- Fix the contradicting 'Maximum 496 longs' limitation. The same file at line 113 correctly states '$000-$1F7: Your PASM code/data (504 longs)'. Silicon doc confirms COGINIT loads $000..$1F7 = 504 longs. The 496 figure describes only the general-purpose registers ($000-$1EF); $1F0-$1F7 (dual-purpose) are also loaded and usable as code/data. Change 496 to 504.

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/silicon-doc-complete-sample.txt — COGINIT section: 'D/# = %0_x_xxxx The target cog loads its own registers $000..$1F7 from the hub'
- engineering/ingestion/sources/silicon-doc/silicon-doc-complete-sample.txt — GENERAL PURPOSE REGISTERS section: 'RAM registers $000 through $1EF are general-purpose registers for code and data usage'
- engineering/ingestion/sources/silicon-doc/silicon-doc-complete-sample.txt — DUAL-PURPOSE REGISTERS section: 'RAM registers $1F0 through $1F7 may either be used as general-purpose registers, or may be used as special-purpose registers if their associated functions are enabled'
- engineering/ingestion/sources/silicon-doc/silicon-doc-complete-sample.txt — SPECIAL-PURPOSE REGISTERS section: 'Each cog contains 8 special-purpose registers that are mapped into the RAM register address space from $1F8 to $1FF'
- deliverables/ai/P2/language/pasm2/concepts/cog_hub_execution.yaml:58-60 — memory_map section
- deliverables/ai/P2/language/spin2/methods/coginit.yaml:111-125 — memory_layout (line 113) and limitations (line 125)
- deliverables/ai/P2/language/pasm2/cogexec.yaml:27 — 'Loads cog RAM registers $000-$1F7 from hub RAM' (no count; correct)

**Why / rationale:** PARTIAL because: (1) The YAML defects are CONFIRMED and fixable — cog_hub_execution.yaml has a wrong memory_map ($000-$1FF labelled '496 longs' with '$1F0-$1FF: 16 special registers'; both range and classification are wrong per silicon doc), and spin2/methods/coginit.yaml:125 contradicts its own line 113 (496 vs 504). (2) The proposed correction in the finding targets the MANUAL (appendix-e-constants.md lines 230/248/252), which is out of YAML scope — noted as manual fix only. fix_target is mixed: yaml_source for the two YAML files + manual for appendix-e-constants.md. Math verification: $000-$1F7 inclusive = 0x1F8 longs = 504 (correct for COGINIT load); $000-$1EF inclusive = 0x1F0 = 496 (correct for general-purpose only). The silicon doc is unambiguous: COGINIT loads $000..$1F7; only $1F0-$1F7 are dual-purpose (not always special); $1F8-$1FF are always special-purpose. cogexec.yaml:27 gives the range '$000-$1F7' with no count and is therefore correct — no change needed there.

#### F-097 — `addon-goertzel-touch.yaml`: The manual states the ADC gains as 3.16x and 31.6x (the √10-spaced physical gain values: …  ·  `DONE`

**Files:** `deliverables/ai/P2/architecture/smart-pins/smart-pin-11000-adc-internal-clock.yaml`, `deliverables/ai/P2/hardware/addon-goertzel-touch.yaml`

**Fix applied:**
- Fix gain labels: P_ADC_3X is 3.16x gain (not 3x), P_ADC_30X is 31.6x gain (not 30x). Both confirmed by spin2-v51-narrative.txt:5050/5054 and spin2-v55-text.txt:1470/1472.
- Fix smart_pin_modes dict keys and constant name: key '3x' -> '3.16x', key '31x' -> '31.6x', AND constant name 'P_ADC_31X' -> 'P_ADC_30X' (P_ADC_31X does not exist; correct name is P_ADC_30X per all primary sources). The finding only flagged gain labels but missed the fabricated constant name P_ADC_31X.
- Fix magnification_codes labels: '3x' -> '3.16x' and '31x' -> '31.6x' to match the actual physical ADC gain values (sqrt-10-spaced ladder: 1x, 3.16x, 10x, 31.6x, 100x).

**Sources that proved it:**
- engineering/ingestion/sources/spin2_lang_ref_v55/spin2-v55-text.txt:1469-1473 — full ADC Input Modes table: P_ADC_3X=3.16x, P_ADC_30X=31.6x; P_ADC_31X does not exist
- engineering/ingestion/sources/spin2-v51/spin2-v51-narrative.txt:5050 — P_ADC_3X ADC 3.16x, :5054 — P_ADC_30X ADC 31.6x
- engineering/ingestion/sources/spin2-v51/smartpin-symbols.txt:362-381 — P_ADC_3X 3.16x, P_ADC_30X 31.6x

**Why / rationale:** PARTIAL verdict: the finding's core claim is CONFIRMED — gain labels '3x'/'30x' in smart-pin-11000-adc-internal-clock.yaml and '3x'/'31x' labels in addon-goertzel-touch.yaml are wrong; the correct physical values are 3.16x and 31.6x per all primary sources (sqrt-10-spaced ladder). HOWEVER, the finding MISSED a more severe additional defect in addon-goertzel-touch.yaml line 93: the constant name 'P_ADC_31X' is FABRICATED — no such constant exists. The correct constant is 'P_ADC_30X' (confirmed by v55:1472, v51-narrative:5054, smartpin-symbols:378). The complete ADC gain ladder is: P_ADC_1X=1x, P_ADC_3X=3.16x, P_ADC_10X=10x, P_ADC_30X=31.6x, P_ADC_100X=100x. Three edits required: (1) smart-pin-11000-adc-internal-clock.yaml lines 147/149 gain labels, (2) addon-goertzel-touch.yaml smart_pin_modes keys + constant name fix (P_ADC_31X→P_ADC_30X), (3) addon-goertzel-touch.yaml magnification_codes labels."


### Descriptions & specificity (copy-paste artifacts, column-bleed)

#### F-033 — `jnxro.yaml`: Manual is correct (XRO = streamer NCO rollover). jxro.yaml mislabels XRO as 'streamer …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/jxro.yaml`

**Fix applied:**
- Fix mislabeled XRO event flag: 'streamer ready' should be 'streamer NCO rollover'

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/part2-video-output.txt:401 (POLLXRO = streamer-NCO-rollover event flag)
- engineering/ingestion/sources/silicon-doc/part2-video-output.txt:427 (WAITXRO = streamer-NCO-rollover event flag)
- engineering/ingestion/sources/silicon-doc/part2-video-output.txt:449 (JXRO/JNXRO = streamer-NCO-rollover event flag is set/clear)
- deliverables/ai/P2/language/pasm2/jxro.yaml:12 (suspect text confirmed present)
- deliverables/ai/P2/language/pasm2/jnxro.yaml:4 (sibling correctly says 'streamer NCO rollover')
- deliverables/ai/P2/language/pasm2/pollxro.yaml (correctly uses 'streamer NCO rollover' throughout)
- deliverables/ai/P2/language/pasm2/waitxro.yaml (correctly uses 'streamer-NCO-rollover' throughout)

**Why / rationale:** The defect is confirmed and isolated to jxro.yaml line 12 only. The silicon doc (part2-video-output.txt lines 401, 427, 449) consistently names XRO as the 'streamer-NCO-rollover event flag' with no ambiguity. The phrase 'streamer ready' does appear in silicon docs but refers to a different concept entirely: bit D[10] in a register (the 'streamer ready to accept new command' status bit), which is completely unrelated to XRO. The three sibling YAMLs (jnxro.yaml, pollxro.yaml, waitxro.yaml) all correctly use 'streamer NCO rollover'. No other XRO YAML files contain the 'streamer ready' mislabel. The fix is a single-line description correction in jxro.yaml; no changes needed to pollxro.yaml, waitxro.yaml, or jnxro.yaml.

#### F-041 — `tjf.yaml`: tjf.yaml and tjz.yaml description fields contain a mangled trailing fragment ('... 2 or 4 …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/tjf.yaml`, `deliverables/ai/P2/language/pasm2/tjz.yaml`

**Fix applied:**
- Remove the trailing whitespace and folded clocks fragment ('2 or 4 / 2 or') that bled into the description field from a table-extraction artifact. The timing already lives correctly in encoding[0].clocks.

**Sources that proved it:**
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/pasm2/tjf.yaml:13-14 — description field contains trailing spaces + '2\n  or 4 / 2 or'
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/pasm2/tjz.yaml:13-14 — description field contains trailing spaces + '2\n  or 4 / 2 or'
- /workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-t.md:272 — TJF/TJNF explanation with clean description
- /workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-t.md:358 — TJZ/TJNZ explanation with clean description
- python3 yaml.safe_load probe — TJF description parsed as 'Test D and jump to S** if D is full (D = $FFFF_FFFF).                                                                    2 or 4 / 2 or'; TJZ as 'Test D and jump to S** if D is zero.                                                                                 2 or 4 / 2 or'

**Why / rationale:** Both YAML files confirmed defective as described. The description field in each uses a YAML folded scalar where line 14 ('  or 4 / 2 or') is a continuation of line 13, resulting in the parsed description containing a mangled clocks fragment ('2 or 4 / 2 or') appended after many trailing spaces. This is a table-extraction artifact: the manual's encoding table shows 'Clks: 2 or 4 / 2 or 13-20', and the '2 or 4 / 2 or' portion leaked into the prose description during ingestion. The timing is already correctly encoded in encoding[0].clocks ('2 or 4'). The clean descriptions verified from instructions-t.md are exactly those proposed in the finding. No manual change needed.

#### F-042 — `addpix.yaml`: The '(and alpha if present)' parenthetical is a manual-introduced semantic claim the …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/addpix.yaml`

**Fix applied:**
- Replace RGB-only (3-channel) framing with four-byte (8:8:8:8) framing in description, result, and parameters to match silicon doc and manual.

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:403 ('Pixel blending instructions for 8:8:8:8 data')
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:2556-2557 ('A pixel consists of four byte fields within a 32-bit cog register. Pixel operations occur between each pair of D and S bytes')
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:2584-2589 (sum-of-products formula applied to D[31:24], D[23:16], D[15:08], D[07:00] — all four bytes unconditionally)
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-a.md:154 ('each of the four bytes of the 32-bit register is treated as a separate field — for 8:8:8:8 pixel data these are the red, green, blue, and alpha/fourth bytes')
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-a.md:158 ('processes all four byte fields (the three RGB color channels plus the alpha/fourth byte) in parallel, completing in 7 clock cycles')
- deliverables/ai/P2/language/pasm2/addpix.yaml:5-11 (current suspect text — RGB-only, no alpha mention, three-channel framing)

**Why / rationale:** The YAML description/result/parameters all frame ADDPIX as an RGB (3-channel) operation. Silicon doc is unambiguous: pixel operations act on ALL FOUR byte fields (D[31:24..07:00]) unconditionally for 8:8:8:8 data; line 403 explicitly names 8:8:8:8. The manual (opus-master) has already been corrected to say 'four byte fields' and 'all four byte fields ... including alpha/fourth byte'. The YAML has NOT been updated to match. The finding's hypothesis — that the KB's RGB-only framing is wrong — is confirmed. The finding's secondary claim (manual line 154/158 also wrong) is now moot because the manual was already fixed. Only the YAML needs correction. The alpha parenthetical in the original (pre-fix) manual was not a hallucination — the silicon doc confirms the 4th byte is real — but the 'three color channels' wording that surrounded it was wrong; both the manual and the YAML needed the channel count changed to four. The manual fix is done; only the YAML remains. fix_target = yaml_source.

#### F-050 — `calla.yaml`: The manual is correct (CALLA uses PTRA only). The YAML description is a copy-paste …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/calla.yaml`

**Fix applied:**
- Fix description field: replace 'PTRA or PTRB' with 'PTRA' only (CALLA uses PTRA exclusively, not PTRB)
- Fix oneliner field: replace 'PTRA++ or PTRB++' with 'PTRA++' only (CALLA uses PTRA exclusively)

**Sources that proved it:**
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-c.md:81 — 'CALLA writes the current C and Z flags and the address of the next instruction into the 4-byte Hub RAM location at PTRA, then increments PTRA by 4' (PTRA only)
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-c.md:125 — 'CALLB writes...into the 4-byte Hub RAM location at PTRB, then increments PTRB by 4' (PTRB only, confirming the two instructions use separate pointers)
- deliverables/ai/P2/language/pasm2/calla.yaml:18-21 — confirmed current defect text 'at PTRA or PTRB' present today
- deliverables/ai/P2/language/pasm2/calla.yaml:47 — confirmed current defect text 'at PTRA++ or PTRB++' present today
- deliverables/ai/P2/language/PASM2-ENCODING-REFERENCE.md:65 — CALLA summary 'at PTRA++ or PTRB++' is generated from calla.yaml oneliner (confirmed via engineering/tools/gen-pasm2-encoding-reference.py:44,134)
- deliverables/ai/P2/language/PASM2-ENCODING-REFERENCE.md:66 — CALLB summary correctly says 'at PTRB++' only (no defect in CALLB row)

**Why / rationale:** Both defects in calla.yaml are confirmed present. The description field (lines 18-21) and the oneliner field (line 47) both say 'PTRA or PTRB' — a copy-paste artifact. The primary authority (manual line 81) is unambiguous: CALLA uses PTRA exclusively. CALLB uses PTRB exclusively (manual line 125). The PASM2-ENCODING-REFERENCE.md line 65 also shows the error ('at PTRA++ or PTRB++') but is GENERATED from the YAML oneliner via gen-pasm2-encoding-reference.py; fixing the YAML oneliner and regenerating will fix the encoding reference automatically — no direct edit to the .md is needed. The callb.yaml description field (lines 5-8) also contains the same 'PTRA or PTRB' artifact (covered by F-051, not F-050), but callb.yaml's oneliner (line 45) is already correct ('at PTRB++' only). The encoding reference CALLB row (line 66) is already correct. Two distinct snippets are provided for calla.yaml since they are non-contiguous fields that each need separate edits.

#### F-051 — `callb.yaml`: The manual is correct (CALLB uses PTRB only). The YAML description copy-paste artifact …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/callb.yaml`

**Fix applied:**
- Replace 'PTRA or PTRB' with 'PTRB' in the description field — CALLB uses PTRB only, not PTRA (that is CALLA). All other fields in this same YAML already correctly say PTRB.

**Sources that proved it:**
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-c.md:125 — 'CALLB writes the current C and Z flags and the address of the next instruction into the 4-byte Hub RAM location at PTRB, then increments PTRB by 4'
- deliverables/ai/P2/language/pasm2/callb.yaml:3 — brief_description: 'Call subroutine via PTRB' (contradicts description line 6)
- deliverables/ai/P2/language/pasm2/callb.yaml:33 — encoding_notes: 'Stores return context at PTRB address then increments PTRB by 4'
- deliverables/ai/P2/language/pasm2/callb.yaml:45 — oneliner: 'Call a subroutine; store return context in the Hub long at PTRB++'
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:11774 — CALLB listed alongside CALLA as separate instructions (CALLA=PTRA, CALLB=PTRB)
- pnut-ts compiler probe: 'pnut-ts /tmp/test_callb.spin2' compiled CALLB #ADDR successfully (exit 0, wrote .bin)

**Why / rationale:** The defect is confirmed. The YAML description field at lines 5-8 contains 'PTRA or PTRB' which is a generic copy-paste artifact from a CALLA/CALLB shared template. Every other field in callb.yaml (brief_description, encoding_notes, oneliner, and all syntax_variants) correctly references PTRB only. The manual at instructions-c.md:125 is unambiguous: CALLB uses PTRB. CALLA (a separate instruction) uses PTRA. The silicon doc confirms they are distinct instructions with distinct pointer assignments. The proposed correction is to remove 'PTRA or' from the description, leaving 'at PTRB' — consistent with all other fields in the file and with all primary sources.

#### F-052 — `callpa.yaml`: The manual correctly disambiguates (PA for CALLPA, PB for CALLPB); the YAML parameter …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/callpa.yaml`, `deliverables/ai/P2/language/pasm2/callpb.yaml`

**Fix applied:**
- Fix parameters Dest line: replace 'PA or PB' with 'PA' (CALLPA always targets PA, never PB). Fix oneliner: remove 'or PB'.
- Fix oneliner: change 'copy D into PA or PB' to 'copy D into PA'.
- Fix parameters Dest line: replace 'PA or PB' with 'PB' (CALLPB always targets PB, never PA).
- Fix oneliner: change 'copy D into PA or PB' to 'copy D into PB'.

**Sources that proved it:**
- /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:190-191 — CSV rows 166-167: CALLPA 'copy D to PA', CALLPB 'copy D to PB'
- /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/silicon-doc/WW-FIELD-ENCODING.md:57-61 — 'CALLPA always saves return to PA', 'CALLPB always saves return to PB'
- /workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-c.md:200 — CALLPA: 'whose value is copied to PA.'
- /workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-c.md:236 — CALLPB: 'whose value is copied to PB.'
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/pasm2/callpa.yaml:6-7,41-42 — suspect text confirmed present today
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/pasm2/callpb.yaml:6-7,39-40 — suspect text confirmed present today

**Why / rationale:** The defect is confirmed in both YAMLs. Both callpa.yaml (line 7) and callpb.yaml (line 7) read 'PA or PB' in the parameters Dest field; both oneliners (callpa.yaml line 41-42, callpb.yaml line 39-40) also say 'PA or PB'. All three primary sources (silicon CSV, WW-FIELD-ENCODING.md silicon-doc, and the opus-master manual) agree: CALLPA has a fixed destination of PA; CALLPB has a fixed destination of PB. The description fields in both YAMLs are already correctly specific (callpa.yaml line 4 says 'copies the value of Dest to PA'; callpb.yaml line 4 says 'copies the value of Dest to PB'), so only parameters Dest and oneliner need correction in each file. No compiler probe needed — this is a prose-specificity defect, not an encoding question.

#### F-065 — `wfbyte.yaml`: The YAML description fields contain a column-bleed artifact (Clks value '2' + 'FIFO IN …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/wfbyte.yaml`, `deliverables/ai/P2/language/pasm2/wfword.yaml`, `deliverables/ai/P2/language/pasm2/wflong.yaml`

**Fix applied:**
- Remove column-bleed artifact '2 / FIFO IN USE' from description field. The '2' is the cog-exec clock count (col 7 in the CSV) and 'FIFO IN USE' is the hub-exec mode note (col 8) — both are separate CSV columns that were incorrectly merged into the description during table extraction.
- Remove column-bleed artifact '2 / FIFO IN USE' from description field — same extraction defect as wfbyte.yaml.

**How verified (compiler):** N/A — description-field text content is not compilable; the defect is a table-extraction column merge, not a semantic claim requiring compilation.

**Sources that proved it:**
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:279-281 — CSV col 5 (Description) ends cleanly at 'into FIFO.' for all three instructions; col 7 = '2' (Cog/LUT exec clocks); col 8 = 'FIFO IN USE' (Hub exec note). These are three separate columns that were merged into the YAML description during extraction.
- deliverables/ai/P2/language/pasm2/wfbyte.yaml:12-13 — bleed confirmed present today
- deliverables/ai/P2/language/pasm2/wfword.yaml:12-13 — bleed confirmed present today
- deliverables/ai/P2/language/pasm2/wflong.yaml:12-13 — bleed confirmed present today

**Why / rationale:** The P2 Instructions v35 CSV is the unambiguous primary authority. All three WFBYTE/WFWORD/WFLONG rows (CSV lines 279-281) show the description column (col 5) ending cleanly at 'into FIFO.' The trailing '2' is col 7 (Clock Cycles — Cog/LUT Exec Mode = 2 clocks) and 'FIFO IN USE' is col 8 (Clock Cycles — Hub Exec Mode, meaning these instructions cannot be used during hub execution because the FIFO is already occupied). The YAML description field incorrectly concatenated all three columns into a single scalar with a YAML fold continuation. The existing structured fields encoding[].clocks: '2' and timing.cycles: 2 already correctly capture the clock count. The 'FIFO IN USE' hub-exec restriction is a known constraint documented in the silicon-doc (part3-end.txt) but does not belong embedded in the description prose. All three YAMLs carry identical structure of the bleed; all three need the same one-line fix.

#### F-078 — `getct.yaml`: Three errors: (a) '64-bit' contradicts the 32-bit authority; (b) 'upper 32 bits with WC' …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/concepts/special_registers.yaml`, `deliverables/ai/P2/language/pasm2/getct.yaml`, `deliverables/ai/P2/language/spin2/methods/getct.yaml`

**Fix applied:**
- CT width field is wrong: says '32-bit, free-running' but silicon doc is unambiguous that CT is the lower 32 bits of a 64-bit free-running counter (Rev B/C silicon). Fix to reflect 64-bit counter with GETCT returning lower 32 bits by default, upper 32 bits with WC.
- The C-bit in GETCT D {WC} is a mode selector (upper vs lower 32 bits of 64-bit counter), NOT a C-flag write. Current YAML wrongly documents it as 'c: same' / 'C: Unchanged'. Add WC variant semantics and fix the description to note 64-bit counter and what WC does.
- Description says 'Get the current 32-bit system counter value' without noting the underlying counter is 64-bit and GETCT() reads only the lower 32 bits. Fix to avoid implying the counter itself is 32-bit.

**How verified (compiler):** pnut-ts /tmp/test_getct_pasm2.spin2 -l: GETCT r0 → 1A 04 60 FD (word 0xFD60041A, C-bit=0); GETCT r0 WC → 1A 04 70 FD (word 0xFD70041A, C-bit=1 at bit20). WC form assembles to a distinct encoding — confirmed not fabricated.

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:81 — 'System counter extended to 64 bits. GETCT WC retrieves upper 32-bits.'
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:436 — '64-bit free-running counter which increments every clock, cleared on reset'
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:5131 — 'CT is the lower 32-bits of the free-running 64-bit global counter'
- engineering/ingestion/sources/silicon-doc/part2-video-output.txt:361 — 'CT is the lower 32-bits of the free-running 64-bit global counter'
- deliverables/ai/P2/language/pasm2/concepts/special_registers.yaml:61 — confirmed '- width: 32-bit, free-running' still present
- deliverables/ai/P2/language/pasm2/getct.yaml:1-31 — confirmed 'c: same' / 'C: Unchanged' / no WC-variant semantics
- deliverables/ai/P2/language/spin2/methods/getct.yaml:8-11 — confirmed 'Get the current 32-bit system counter value'
- pnut-ts v1.55.0 compiler probe: GETCT r0 = 0xFD60041A (C=0), GETCT r0 WC = 0xFD70041A (C=1) — WC sets bit 20, confirming distinct encoding

**Why / rationale:** All three sub-claims in the finding are CONFIRMED against primary sources. (a) The underlying CT register is 64-bit (silicon doc lines 81, 436, 5131) — special_registers.yaml:61 '32-bit, free-running' is wrong. (b) GETCT with WC retrieves upper 32 bits (silicon doc line 81) — pasm2/getct.yaml documents C-bit as 'Unchanged' (wrong: it is a mode selector). Compiler probe independently confirms WC produces a distinct instruction word with bit 20 set. (c) The spin2/methods/getct.yaml 'Get the current 32-bit system counter value' is misleading — it implies the counter itself is 32-bit when in fact GETCT() returns only the lower 32 bits of a 64-bit counter. The Spin2 v55 doc itself distinguishes: line 547 'Get 32-bit system counter' vs lines 552-553 which call GETSEC/GETMS '64-bit system counter' methods — but the v55 text reflects the Spin2 method's 32-bit return, not the underlying hardware width. The fix target is the YAML files only; the manual (special-registers.md:533) is already correct per the finding and is not touched.

#### F-079 — `clock_system.yaml`: Two YAMLs in the data set give different widths for the same counter; the 32-bit value is …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/concepts/special_registers.yaml`, `deliverables/ai/P2/language/spin2/methods/getct.yaml`

**Fix applied:**
- Fix ct_registers width field from '32-bit, free-running' to '64-bit free-running (Rev B/C silicon); GETCT returns lower 32 bits by default, upper 32 bits with WC'
- Add note that the underlying system counter is 64-bit and GETCT() reads the lower 32 bits (GETCT with WC in PASM2 reads the upper 32 bits)

**Sources that proved it:**
- /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/silicon-doc/p2-documentation.txt:81 — 'System counter extended to 64 bits. GETCT WC retrieves upper 32-bits.'
- /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/silicon-doc/p2-documentation.txt:436 — '64-bit free-running counter which increments every clock, cleared on reset'
- /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/silicon-doc/p2-documentation.txt:5131 — 'CT is the lower 32-bits of the free-running 64-bit global counter'
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/pasm2/concepts/special_registers.yaml:61 — confirmed suspect text 'width: 32-bit, free-running' is present
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/architecture/clock_system.yaml:241,268 — confirmed clock_system.yaml correctly says 64-bit (no fix needed here)
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/spin2/methods/getct.yaml:9 — 'Get the current 32-bit system counter value' (correct for what the Spin2 method returns, but lacks 64-bit context)

**Why / rationale:** The finding's inversion analysis is correct. clock_system.yaml lines 241 and 268 are accurate (64-bit) and require NO changes. The defect is in special_registers.yaml:61 which says '32-bit, free-running' — the Silicon Doc is unambiguous: the counter was extended to 64 bits in Rev B silicon, GETCT WC retrieves the upper 32 bits, and event documentation refers to 'CT is the lower 32-bits of the free-running 64-bit global counter'. The spin2/methods/getct.yaml description of GETCT() as returning '32-bit' is technically correct for the Spin2 method itself (it returns the lower 32 bits), but adding context about the 64-bit underlying hardware and WC access removes the apparent contradiction with clock_system.yaml. The pasm2/getct.yaml has no description of the 64-bit nature either but the fix proposed in the finding targets the spin2 getct.yaml specifically. No compiler probe was run since counter width is a silicon fact not verifiable by compilation.

#### F-090 — `serial_loader.yaml`: Per KB authority, Prop_Hex loads Intel-hex records (colon-prefixed with …  ·  `DONE`

**Files:** `deliverables/ai/P2/architecture/serial_loader.yaml`

**Fix applied:**
- Replace bogus Intel-HEX record format block with correct whitespace-separated raw hex bytes description matching silicon-doc lines 9464-9494
- Fix loading_process.data_reception.hex_mode which incorrectly describes Intel HEX record processing; Prop_Hex uses raw whitespace-separated bytes with ~ or ? terminator
- Fix programming_examples.basic_loader_session which shows Intel HEX records; replace with correct Prop_Hex whitespace-separated bytes syntax from silicon-doc line 9494
- Fix see_also list which incorrectly references 'Intel hex format specification' — Prop_Hex does not use Intel HEX

**Sources that proved it:**
- /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/silicon-doc/p2-documentation.txt:9463-9502 (Prop_Hex section: 'Hex bytes must be separated by whitespaces. Only the bottom 8 bits of hex values are used as data'; syntax Prop_Hex <INAmask> <INAdata> <INBmask> <INBdata> <hexdatabytes> ~ | ?; example Prop_Hex 0 0 0 0 FB F7 23 F6 ...)
- /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/silicon-doc/p2-documentation.txt:9394-9401 (command syntax table listing four commands including Prop_Hex with hexdatabytes parameter, NOT Intel HEX records)
- /workspaces/P2-Knowledge-Base/deliverables/ai/P2/architecture/serial_loader.yaml:69-82 (current prop_hex block confirmed present with Intel-HEX record format)

**Why / rationale:** CONFIRMED. The YAML prop_hex block (lines 69-82) describes the Intel HEX record format (:LLAAAATTDD...CC with byte count, address, type, data, checksum fields) which is completely wrong. The silicon-doc is unambiguous: Prop_Hex takes whitespace-separated raw hex bytes with INA/INB mask parameters and a ~ or ? terminator. There is no record structure, no per-record address, no type byte, no per-record checksum — just raw bytes. The error cascades into loading_process.data_reception.hex_mode (says 'Process Intel hex records', 'Stop on EOF record') and programming_examples.basic_loader_session (shows Intel HEX colon records). Also see_also incorrectly references 'Intel hex format specification'. All four locations need correction. Note: the prop_txt section describing Base64 as 'RFC 4648' is not part of F-090 scope, though the silicon-doc does not cite RFC 4648 by name.


### Cross-reference repairs

#### F-040 — `test.yaml`: The manual provides related cross-references for TESTB; the YAML omits a related: list …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/testb.yaml`

**Fix applied:**
- Add missing related: list to testb.yaml. Manual line 92 lists TESTBN, TESTP, TESTPN as related; peer YAMLs test.yaml and testn.yaml carry the full family. Use the full-family set (all TEST-family members minus self) to match peer pattern.

**Sources that proved it:**
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-t.md:92 (TESTB Related line confirms TESTBN, TESTP, TESTPN)
- deliverables/ai/P2/language/pasm2/testb.yaml:1-46 (no related: key present)
- deliverables/ai/P2/language/pasm2/testbn.yaml:44-46 (related: TESTP, TESTPN)
- deliverables/ai/P2/language/pasm2/test.yaml:59-64 (related: TESTN, TESTB, TESTBN, TESTP, TESTPN)
- deliverables/ai/P2/language/pasm2/testn.yaml:50-55 (related: TEST, TESTB, TESTBN, TESTP, TESTPN)
- deliverables/ai/P2/language/pasm2/testp.yaml:99-105 (related_instructions: TESTB, TESTBN, DRVL, DRVH...)
- deliverables/ai/P2/language/pasm2/testpn.yaml:61-63 (related: TESTB, TESTBN)

**Why / rationale:** Finding confirmed. testb.yaml has no related: key at all (46-line file, grep returns nothing for 'related'). The manual at instructions-t.md:92 explicitly lists Related for TESTB as [TESTBN, TESTP, TESTPN]. The peer YAMLs test.yaml and testn.yaml carry the full TEST-family set (5 members each, minus self). testbn.yaml carries only TESTP and TESTPN (omits TEST/TESTN), while testpn.yaml lists TESTB/TESTBN. The proposed correction uses the full-family set (TESTBN, TEST, TESTN, TESTP, TESTPN) to match the more complete peer pattern from test.yaml/testn.yaml, which is a strict superset of the manual's minimum. All five target instruction YAMLs exist and are confirmed present. No manual change needed.

#### F-043 — `addsx.yaml`: The YAML cross-reference set for ADDSX self-references and omits ADDS. The manual already …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/addsx.yaml`

**Fix applied:**
- Replace self-referencing ADDSX entry in related block with ADDS, matching the manual's cross-reference set (ADD, ADDX, ADDS, SUBSX)

**Sources that proved it:**
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-a.md:224 — Related: [ADD](#add), [ADDX](#addx), [ADDS](#adds), [SUBSX](#subsx)
- deliverables/ai/P2/language/pasm2/addsx.yaml:40-44 — related: ADD, ADDX, ADDSX, SUBSX (confirmed present today)
- deliverables/ai/P2/language/pasm2/adds.yaml — confirmed present (valid cross-reference target)
- deliverables/ai/P2/language/pasm2/add.yaml — confirmed present
- deliverables/ai/P2/language/pasm2/addx.yaml — confirmed present
- deliverables/ai/P2/language/pasm2/subsx.yaml — confirmed present

**Why / rationale:** The suspect text is present today in addsx.yaml lines 40-44: the related block lists ADDSX (a self-reference) instead of ADDS. The manual at instructions-a.md:224 unambiguously lists the correct set as ADD, ADDX, ADDS, SUBSX — no self-reference. All four target sibling YAMLs (add, addx, adds, subsx) exist and are reachable. This is a clear typo: ADDSX was typed where ADDS was intended. No compiler probe is applicable here as cross-reference validity is a documentation concern, not a compilation concern.

#### F-044 — `add.yaml`: The YAML omits the ADDS cross-reference that the manual (and the rest of the ADD family) …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/addx.yaml`

**Fix applied:**
- Add ADDS to the related block so it matches the manual (instructions-a.md:261) and the rest of the ADD family (add.yaml/adds.yaml/addsx.yaml all cross-link all siblings).

**Sources that proved it:**
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-a.md:261 (ADDX Related line lists ADD, ADDS, ADDSX, SUBX)
- deliverables/ai/P2/language/pasm2/addx.yaml:40-43 (related block — ADDS absent)
- deliverables/ai/P2/language/pasm2/add.yaml:62-66 (related: ADDX, ADDS, ADDSX, SUB)
- deliverables/ai/P2/language/pasm2/adds.yaml:40-44 (related: ADD, ADDX, ADDSX, SUBS)
- deliverables/ai/P2/language/pasm2/addsx.yaml:40-44 (related: ADD, ADDX, ADDSX, SUBSX)

**Why / rationale:** The defect is confirmed exactly as described. The manual (instructions-a.md:261) lists four related instructions for ADDX: ADD, ADDS, ADDSX, SUBX. The current addx.yaml related block has only three: ADD, ADDSX, SUBX — ADDS is absent. Every other ADD-family member cross-links all siblings: add.yaml includes ADDS, adds.yaml includes ADDX, addsx.yaml includes ADDS. addx.yaml is the sole missing link. adds.yaml exists at the canonical path (verified), so the reference is valid and resolvable. No compiler probe needed — this is a cross-reference completeness issue, not a compilable encoding question.

#### F-053 — `cmp.yaml`: The YAML cross-reference set for CMPSX self-references itself and is missing CMPS. The …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/cmpsx.yaml`

**Fix applied:**
- Remove self-reference to CMPSX and add missing sibling CMPS in related block

**Sources that proved it:**
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-c.md:484 — **Related:** [CMP](#cmp), [CMPX](#cmpx), [CMPS](#cmps)
- deliverables/ai/P2/language/pasm2/cmpsx.yaml:37-40 — related: [CMP, CMPX, CMPSX] (confirmed self-reference present today)
- deliverables/ai/P2/language/pasm2/cmpx.yaml:37-40 — related: [CMP, CMPX, CMPSX] (co-located defect, addressed by F-054)
- deliverables/ai/P2/language/pasm2/cmps.yaml:37-40 — related: [CMP, CMPX, CMPSX] (sibling cross-check)
- deliverables/ai/P2/language/pasm2/cmp.yaml:59-63 — related: [CMPR, CMPX, CMPS, CMPSX] (sibling cross-check — correctly includes all three)

**Why / rationale:** The defect is confirmed as stated. cmpsx.yaml lines 37-40 reads: related: [CMP, CMPX, CMPSX]. The third entry is a self-reference (CMPSX referring to itself), and the genuine sibling CMPS is absent. The manual at instructions-c.md:484 provides the authoritative related set: [CMP, CMPX, CMPS] — exactly the three distinct sibling instructions. cmp.yaml also independently corroborates this: its related block lists [CMPR, CMPX, CMPS, CMPSX], confirming CMPS and CMPSX are both real siblings and neither is CMPSX's self-reference. The proposed correction (replace CMPSX with CMPS in the related block of cmpsx.yaml) is accurate. Note: cmps.yaml itself also has the same pattern — its related block lists [CMP, CMPX, CMPSX] which does NOT self-reference CMPS and IS logically correct (CMPS's three siblings are CMP, CMPX, CMPSX). The F-053 finding is strictly about cmpsx.yaml; the co-located cmpx.yaml defect is covered by F-054.

#### F-054 — `cmp.yaml`: The YAML cross-reference set for CMPX self-references itself and is missing CMPS. The …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/cmpx.yaml`

**Fix applied:**
- Replace self-referencing CMPX entry with CMPS in the related block

**Sources that proved it:**
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-c.md:527 — **Related:** [CMP](#cmp), [CMPS](#cmps), [CMPSX](#cmpsx)
- deliverables/ai/P2/language/pasm2/cmpx.yaml:37-40 — related: [CMP, CMPX, CMPSX] (self-reference present, CMPS absent)
- deliverables/ai/P2/language/pasm2/cmp.yaml:59-63 — related: [CMPR, CMPX, CMPS, CMPSX]
- deliverables/ai/P2/language/pasm2/cmps.yaml:37-40 — related: [CMP, CMPX, CMPSX]
- deliverables/ai/P2/language/pasm2/cmpsx.yaml:37-40 — related: [CMP, CMPX, CMPSX]

**Why / rationale:** The defect is confirmed. cmpx.yaml lines 37-40 contain `related: [CMP, CMPX, CMPSX]` — CMPX self-references itself (meaningless) and omits CMPS (the signed peer, which is the natural counterpart for unsigned CMPX). The manual at instructions-c.md:527 unambiguously lists the correct set: CMP, CMPS, CMPSX — no self-reference. All four instruction YAMLs (cmp, cmps, cmpsx, cmpx) exist as distinct files. Side observation: cmps.yaml and cmpsx.yaml both also show `[CMP, CMPX, CMPSX]` in their related blocks — missing CMPS from their own cross-references — but those are outside the scope of F-054 and should be tracked as separate findings.

#### F-055 — `cogid.yaml`: The YAML cross-reference set for COGSTOP self-references itself and omits COGID. The …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/cogstop.yaml`

**Fix applied:**
- Replace the self-referencing COGSTOP entry in the related list with COGID, yielding the correct COG-control trio {COGINIT, COGID}.

**Sources that proved it:**
- deliverables/ai/P2/language/pasm2/cogstop.yaml:42-44 — confirmed suspect text present: related: [COGINIT, COGSTOP]
- deliverables/ai/P2/language/pasm2/cogid.yaml:40-42 — related: [COGINIT, COGSTOP]
- deliverables/ai/P2/language/pasm2/coginit.yaml:43-44 — related: [COGID, COGSTOP]
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-c.md:781 — **Related:** [COGINIT](#coginit), [COGID](#cogid)

**Why / rationale:** The defect is confirmed. cogstop.yaml lines 42-44 contain `related: [COGINIT, COGSTOP]` — a self-reference to COGSTOP and no reference to COGID. The manual (instructions-c.md:781) explicitly lists `[COGINIT, COGID]` as the related set for COGSTOP. Sibling files establish the expected trio pattern: cogid.yaml references {COGINIT, COGSTOP}, coginit.yaml references {COGID, COGSTOP}; therefore cogstop must reference {COGINIT, COGID}. The `- COGSTOP` entry is a transcription error and must be replaced with `- COGID`. Bare-name style matches established convention in all three sibling files.


### Errata & fabrication removal

#### F-023 — `setxfrq.yaml` SETQ+SETXFRQ "64-bit precision frequency" claim is unverified  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/setxfrq.yaml`

**Fix applied:**
- Remove fabricated SETQ+SETXFRQ '64-bit precision' claim from description, example 3, and related_instructions. The NCO is a 32-bit accumulator; SETQ is not a modifier for SETXFRQ. SETQ before XINIT/XZERO/XCONT sets the frequency during a streamer command (still 32-bit). Replace example 3 with a valid use case (SETQ before XINIT), or remove it. Remove the SETQ related_instructions entry.
- Remove fabricated example 3 (SETQ+SETXFRQ '64-bit precision'). Silicon Doc v35:2794-2796 shows SETQ before XINIT/XZERO/XCONT, not SETXFRQ, as the alternate NCO frequency mechanism.
- Remove SETQ from related_instructions — SETQ is not a companion instruction for SETXFRQ per any primary source.

**How verified (compiler):** pnut-ts /tmp/test_setq_setxfrq.spin2 — compiled OK (exit 0), confirming the sequence is syntactically valid but providing no signal on semantic correctness; the compiler cannot detect that SETQ has no effect on SETXFRQ at runtime.

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:2747-2796 (NCO description, SETXFRQ, and SETQ-before-XINIT mechanism — 32-bit accumulator, no 64-bit NCO, SETQ not a SETXFRQ modifier)
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:2521-2551 (SETQ CONSIDERATIONS — exhaustive list of companion instructions; SETXFRQ is absent)
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:row 264 (SETXFRQ — 'Set streamer NCO frequency to D'; no SETQ interaction noted)
- engineering/ingestion/sources/chip-gracey-clarifications/ — all four files searched; no mention of SETQ+SETXFRQ or 64-bit NCO frequency
- engineering/ingestion/sources/spin2_lang_ref_v55/spin2-v55-text.txt — SETXFRQ does not appear (PASM2-only instruction)
- deliverables/ai/P2/language/pasm2/setxfrq.yaml:12-17 (suspect text confirmed present)

**Why / rationale:** The claim is a fabrication on two levels. First, the NCO is a 32-bit phase accumulator (silicon doc:2748: 'it adds a 32-bit frequency value into a 32-bit phase accumulator'). There is no 64-bit NCO frequency register, so 'D provides high 32 bits for 64-bit precision' is dimensionally incoherent. Second, the silicon doc's exhaustive SETQ CONSIDERATIONS section (lines 2521-2551) lists every instruction that consumes Q; SETXFRQ is absent from that list. The actual SETQ+streamer mechanism described in the silicon doc (lines 2794-2796) is SETQ before XINIT/XZERO/XCONT — which sets the NCO frequency as part of issuing a streamer command. That is a distinct, valid pattern but involves different instructions and does not provide any 64-bit precision. The proposed_snippet for example 3 above illustrates that valid SETQ+XINIT pattern as a replacement; the exact streamer_mode constant would need to be adapted to a real use case by the editor. The description fix removes only the two fabricated lines (lines 16-17 of the YAML). The frequency_formula section is separately correct (2^31 modulus) and does not need changes.

#### F-045 — `augd.yaml`: Manual correctly documents the AUGD SETQ/PTRx errata; augd.yaml omits it, so a remote …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/augd.yaml`, `deliverables/ai/P2/language/pasm2/augs.yaml`

**Fix applied:**
- Add silicon_errata section documenting the SETQ/SETQ2 → RDLONG/WRLONG/WMLONG block-size PTRx-delta cancellation bug. Silicon Doc KNOWN BUGS (p2-documentation.txt:197-210) explicitly names 'ALTx/AUGS/AUGD'. augd.yaml currently has zero silicon_errata entries.
- Add a second silicon_errata entry for the SETQ/PTRx block-size delta bug. augs.yaml already has the ALTx-immediate-#S errata but is missing the block-size PTRx errata. The manual (instructions-a.md:1067) documents this pitfall for AUGS and the Silicon Doc (p2-documentation.txt:197-210) explicitly names AUGS alongside AUGD.

**How verified (compiler):** N/A — this is a silicon errata fact (runtime behaviour of SETQ+AUGD+RDLONG sequence), not a syntax or flag question compilable in isolation.

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:197-210 — KNOWN BUGS section explicitly names 'Intervening ALTx/AUGS/AUGD instructions between SETQ/SETQ2 and RDLONG/WRLONG/WMLONG-PTRx instructions will cancel the special-case block-size PTRx deltas'
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:212-227 — second distinct bug: intervening ALTx with immediate #S consumes AUGS (names AUGS/ALTx only, not AUGD)
- deliverables/ai/P2/language/pasm2/augd.yaml:1-70 — confirmed zero silicon_errata section present
- deliverables/ai/P2/language/pasm2/augs.yaml:48-63 — confirmed silicon_errata exists for ALTx-#S bug only; no PTRx block-size errata
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-a.md:1029 — AUGD pitfall: 'AUGD placed between SETQ/SETQ2 and RDLONG/WRLONG/WMLONG cancels the block-size PTRx delta calculation'
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-a.md:1067 — AUGS pitfall: identical PTRx delta bug documented

**Why / rationale:** Finding CONFIRMED with one scope expansion. The finding correctly identifies that augd.yaml has zero silicon_errata entries while the Silicon Doc KNOWN BUGS (p2-documentation.txt:197-210) names AUGD explicitly. Additionally, augs.yaml is ALSO missing this same PTRx block-size errata — it only has the ALTx-immediate-#S errata. The manual at instructions-a.md:1067 independently documents the PTRx block-size pitfall for AUGS too. Both YAMLs need the new errata entry added. The finding's note about augs.yaml's existing errata being a DIFFERENT bug is correct: the two Silicon Doc bugs are distinct (lines 197-210 for PTRx block-delta, lines 212-227 for ALTx-#S augmentation). The augs.yaml scope_note on the ALTx-#S errata remains valid under its own anchor and is covered by F-046.

#### F-046 — `augd.yaml`: The augs.yaml scope_note conflates two distinct Silicon-Doc bugs (block-delta vs …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/augs.yaml`

**Fix applied:**
- Tighten scope_note so it no longer implies AUGD is absent from ALL golden sources. AUGD IS named in the Silicon Doc's first errata (block-delta, line 198: 'ALTx/AUGS/AUGD instructions between SETQ/SETQ2 and RDLONG/WRLONG/WMLONG-PTRx'). The scope_note correctly applies only to the second errata (intervening-#S, lines 212-227) where AUGD is not mentioned — but the phrase 'not stated in any golden source' is overly broad and false.

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:197-210 (block-delta KNOWN BUGS: 'ALTx/AUGS/AUGD instructions between SETQ/SETQ2 and RDLONG/WRLONG/WMLONG-PTRx instructions will cancel the special-case block-size PTRx deltas')
- engineering/ingestion/sources/silicon-doc/p2-documentation.txt:212-227 (intervening-#S KNOWN BUGS: 'Intervening ALTx instructions with an immediate #S operand, between AUGS and the AUGS intended target...' — names only AUGS/ALTx, not AUGD)
- deliverables/ai/P2/language/pasm2/augs.yaml:49-63 (silicon_errata.intervening_altx_immediate_s_consumes_augs including scope_note at line 62)
- deliverables/ai/P2/language/pasm2/augd.yaml:1-70 (confirmed: no silicon_errata section present)

**Why / rationale:** PARTIAL verdict rationale: The core complaint in F-046 is verified. The augs.yaml scope_note (line 62) says 'not stated in any golden source' — this is false at face value because AUGD IS stated in the Silicon Doc's first errata (line 198) as one of the instruction types that cancels block-size PTRx deltas. The scope_note is anchored to the intervening-#S errata (lines 212-227) where the claim is accurate: AUGD is not named there. The fix is to tighten 'not stated in any golden source' to make clear it refers only to this specific errata mechanism.

The finding also lists augd.yaml as an affected file but the proposed correction text is incomplete (cut off in the findings document at '(1) In augs.yaml, tighten the scope_note...'). augd.yaml currently has NO silicon_errata section at all, so it is missing the block-delta errata that explicitly names AUGD. Adding that errata to augd.yaml is a valid follow-on fix but is not clearly specified in the finding's proposed correction — only the augs.yaml scope_note tightening is well-specified, so only that is included here. The augd.yaml gap should be tracked as a separate finding or added in the same fix pass by the author who knows the full intended scope."


### Version-gating clarity (edition-of-introduction vs enforced gate)

#### F-095 — `debug-mask.yaml`: The {Spin2_v46} version-directive requirement is the most-stressed fact about DEBUG_MASK …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/spin2/constants/debug-mask.yaml`, `deliverables/ai/P2/language/spin2/constants/special-configuration-symbols.yaml`

**Fix applied:**
- Remove false {Spin2_v46} version-directive requirement. The feature was introduced in compiler v46, but no {Spin2_v##} directive is required to use it — the directive gate is for new reserved keywords only; DEBUG_MASK is a CON constant, not a keyword. Replace version metadata with introduced_in_version; remove REQUIRES constraint from description and notes.
- Remove false version-directive requirement sentence from description.
- Remove false REQUIRES note from notes list.
- Remove false version-directive requirement from DEBUG_MASK entry: drop REQUIRES sentence from description, remove requires_version and version_directive fields, fix example to not show the directive, fix notes.

**How verified (compiler):** pnut-ts -d /tmp/af182_dat.spin2 (DEBUG_MASK=%00000011, debug[0]+debug[1], NO version directive) → exit 0, 'Wrote /tmp/af182_dat.bin (9276 bytes)'; pnut-ts -d /tmp/af182_v41.spin2 ({Spin2_v41} directive, DEBUG_MASK, debug[0]+debug[5]) → exit 0, 'Wrote /tmp/af182_v41.bin'; control LSTRING with {Spin2_v41} → exit 1 (proves gate enforcement is real; debug[N] simply not gated)

**Sources that proved it:**
- pnut-ts v1.55.0 probe: /tmp/af182_dat.spin2 (DEBUG_MASK + debug[N], no directive) → exit 0, Wrote .bin — NO version gate enforced
- pnut-ts v1.55.0 probe: /tmp/af182_v41.spin2 (DEBUG_MASK + debug[N], explicit {Spin2_v41}) → exit 0, Wrote .bin — compiles even at v41 gate
- pnut-ts v1.55.0 probe: /tmp/af182_nodirective.spin2 (DEBUG_MASK + debug[0..7], no directive) → exit 0, Wrote .bin
- pnut-ts v1.55.0 control: /tmp/af182_control_lstring.spin2 (LSTRING with {Spin2_v41}) → exit 1, error m172 — proves keyword gate enforcement works for true gated keywords
- engineering/ingestion/sources/spin2_lang_ref_v55/spin2-v55-text.txt:1027 — DEBUG_MASK table entry: no version directive mentioned
- engineering/ingestion/sources/spin2_lang_ref_v55/spin2-v55-text.txt:38 — v46 release note: says feature 'added' in v46, does not say {Spin2_v46} directive required
- deliverables/ai/P2/language/spin2/constants/debug-mask.yaml:5-6 — minimum_version/version_directive fields present (suspect text confirmed in file)
- deliverables/ai/P2/language/spin2/constants/debug-mask.yaml:17,124 — REQUIRES constraint present (suspect text confirmed)
- deliverables/ai/P2/language/spin2/constants/special-configuration-symbols.yaml:313-315,327 — requires_version/version_directive + REQUIRES note present (suspect text confirmed)

**Why / rationale:** CONFIRMED. The {Spin2_v46} version-directive requirement stated in both YAMLs is false. The {Spin2_v##} directive mechanism exists to gate NEW RESERVED KEYWORDS (e.g. LSTRING at v42, TASKID at v47) to prevent namespace conflicts with user symbols. DEBUG_MASK is not a keyword — it is a user-defined CON constant that the compiler recognizes by name. debug[N]() uses bracket-index syntax on the pre-existing DEBUG keyword, not a new keyword form. Therefore no directive is required. The v46 reference belongs only as 'introduced_in_version', not as a required directive. The example in special-configuration-symbols.yaml should NOT show {Spin2_v46} in the source, as that would mislead users into thinking it is required.


### Tooling — generated encoding reference

#### F-047 — `altgn.yaml`: The generated encoding reference's per-row flags column asserts C,Z effects for …  ·  `DONE`

**Files:** `engineering/tools/gen-pasm2-encoding-reference.py`

**Fix applied:**
- Fix flags_affected value-vs-key bug: replace key-presence test with a value test so 'No effect' entries do not emit C or Z in the Flags column.

**How verified (compiler):** pnut-ts /tmp/test_altgn_wc.spin2 (ALTGN with WC) → error 'This effect is not allowed for this instruction'; pnut-ts /tmp/test_augd_wc.spin2 (AUGD with WC) → same error; pnut-ts /tmp/test_altgn_ok.spin2 (ALTGN without WC) → compiles clean (wrote .bin). Confirms ALTx/AUGx accept no WC/WZ and write no flags.

**Sources that proved it:**
- deliverables/ai/P2/language/pasm2/altgn.yaml:21-23 (flags_affected C: No effect, Z: No effect)
- deliverables/ai/P2/language/pasm2/alti.yaml:10-12 (flags_affected C: No effect, Z: No effect)
- deliverables/ai/P2/language/pasm2/augd.yaml:9-11 (flags_affected C: No effect, Z: No effect)
- engineering/tools/gen-pasm2-encoding-reference.py:62-68 (key-presence bug confirmed)
- deliverables/ai/P2/language/PASM2-ENCODING-REFERENCE.md:401-402,469,471 (AUGD/AUGS/ALTGN/ALTI all show C,Z — wrong)
- pnut-ts v1.55.0 probe: altgn ptra,#0 wc → 'This effect is not allowed for this instruction'
- pnut-ts v1.55.0 probe: augd #$1234 wc → 'This effect is not allowed for this instruction'

**Why / rationale:** The defect is global across all ~344 instructions that have flags_affected as a dict with 'No effect' values. The generator checks 'C' in fa (key presence in dict — always True when the key exists) instead of checking the VALUE. This makes every instruction with flags_affected: {C: 'No effect', Z: 'No effect'} emit 'C,Z' in the Flags column. The YAML source files are correct (c: —, z: — in encoding rows; flags_affected values say 'No effect'). The fix must be applied to the generator script; after regeneration, PASM2-ENCODING-REFERENCE.md will automatically reflect '--' for ALTGN, ALTI, AUGD, AUGS and all other no-effect instructions. The YAML source files (altgn.yaml, alti.yaml, augd.yaml) need no changes.

#### F-081 — ch02-instruction-format: The manual documents EEEE=0000 solely as _RET_ and omits the authority-documented nuance …  ·  `DONE`

**Files:** `engineering/tools/gen-pasm2-encoding-reference.py`, `deliverables/ai/P2/language/PASM2-ENCODING-REFERENCE.md`

**Fix applied:**
- Replace the hard-coded note (lines 123-126) that falsely claims IF_NEVER assembles to %0000 when flags are written. Compiler probe confirms IF_NEVER always assembles to EEEE=1111; only _RET_ produces EEEE=0000.
- Update the generated note at lines 49-52 to match the corrected generator output (regenerate after fixing gen script, or apply directly as this is the generated artifact).

**How verified (compiler):** pnut-ts /tmp/test_if_never.spin2 -l and pnut-ts /tmp/test_if_never2.spin2 -l: 'if_never mov x,#1' → EEEE=1111; 'if_never mov x,#1 wc' → EEEE=1111; '_ret_ mov x,#1' → EEEE=0000; '_ret_ mov x,#1 wc' → EEEE=0000. IF_NEVER always produces EEEE=%1111, never %0000.

**Sources that proved it:**
- pnut-ts v1.55.0 compiler probe: /tmp/test_if_never.spin2 — 'if_never mov x,#1' → bytes 01 06 04 F6 = 0xF6040601 → EEEE=1111 (not %0000)
- pnut-ts v1.55.0 compiler probe: /tmp/test_if_never2.spin2 — 'if_never mov x,#1 wc' → bytes 01 06 14 F6 = 0xF6140601 → EEEE=1111 (IF_NEVER+WC still maps to 1111, not 0000)
- pnut-ts v1.55.0 compiler probe: '_ret_ mov x,#1' → bytes 01 06 04 06 = 0x06040601 → EEEE=0000; '_ret_ mov x,#1 wc' → 01 06 14 06 → EEEE=0000
- engineering/tools/gen-pasm2-encoding-reference.py:123-126 — hard-coded note is the source of the erroneous claim
- deliverables/ai/P2/language/PASM2-ENCODING-REFERENCE.md:49-52 — generated output carrying the false claim
- deliverables/ai/P2/language/pasm2/concepts/conditional_execution.yaml:50-56 — %0000 maps to _RET_ with alias IF_RET only; IF_NEVER is not listed as an alias for %0000
- deliverables/ai/P2/language/pasm2/concepts/conditional_execution.yaml:170-176 — %1111 maps to IF_ALWAYS with alias (no prefix); IF_NEVER absent here too

**Why / rationale:** The finding is CONFIRMED. The hard-coded note in gen-pasm2-encoding-reference.py lines 123-126 (and its generated output in PASM2-ENCODING-REFERENCE.md lines 49-52) falsely claims that 'the assembler shows the bare prefix as IF_NEVER only when flags are written' implying IF_NEVER can produce EEEE=%0000. Compiler probes definitively refute this: IF_NEVER assembles to EEEE=1111 in all cases (with or without WC/WZ). Only the _RET_ prefix produces EEEE=0000. The note must be corrected. The fix_target is gen_script because the note is hard-coded in the generator; the generated .md must also be updated (either by regenerating after fixing the script, or by direct edit). The conditional_execution.yaml source YAML is already correct — it lists %0000 as _RET_/IF_RET only, with no IF_NEVER alias. The YAML source does not mention IF_NEVER at all, which is consistent with the compiler behavior (IF_NEVER is apparently an assembler convenience alias mapping to %1111, same as bare/IF_ALWAYS).


### Other findings

#### F-036 — `calld.yaml`: LOC loads a 20-bit address into a pointer register (PA/PB/PTRA/PTRB) — an …  ·  `WONTFIX`

**How verified (compiler):** pnut-ts /tmp/test_loc.spin2 (all four LOC forms: PA/PB/PTRA/PTRB with relative and absolute addressing) — compiled successfully, exit 0, 6324 bytes. LOC is accepted as a valid instruction with pointer-register operands.

**Sources that proved it:**
- deliverables/ai/P2/language/pasm2/loc.yaml:31 (category: Math and Logic — confirmed present)
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:431 (LOC = Math and Logic)
- engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:430 (CALLD = Branch A - Call)
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-l.md:11 (LOC header = Branching and Flow Control)
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-iii/appendix-c-categorical-index.md:50 (LOC in Arithmetic Operations table)
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instruction-categories.md:13 (LOC under Data Movement in Arithmetic Operations)
- compiler probe: pnut-ts /tmp/test_loc.spin2 compiled OK (exit 0, 6324 bytes)

**Why / rationale:** The proposed correction (change loc.yaml category from 'Math and Logic' to 'Branch') is REFUTED by the canonical Parallax primary source. The official Parallax 'P2 Instructions v35 - Rev B_C Silicon' CSV at line 431 explicitly categorizes LOC as 'Math and Logic' — identical to the current YAML. CALLD at line 430 is 'Branch A - Call', a deliberate distinction Parallax made in their own documentation. The YAML is correct per the canonical CSV. Additionally, the finding's own 'Authority cited' section contains a factual error: it claims 'instructions-l.md:11 (LOC header = Hub Memory Access)' but direct reading of that file shows the LOC header at line 11 is '[Branching and Flow Control](#branching-and-flow-control)' — not 'Hub Memory Access'. The manual does have internal inconsistency (instructions-l.md uses Branching and Flow Control; instruction-categories.md and appendix-c place LOC under Arithmetic Operations), but that is a manual-side issue and does not affect the YAML. The YAML category 'Math and Logic' matches the CSV category 'Math and Logic' exactly — the YAML is already correct. No change to loc.yaml is warranted. The manual inconsistency (LOC appears under Arithmetic Operations in the categories chapter and appendix but Branching and Flow Control in the instructions-l.md header) is a separate manual issue outside the YAML scope of this finding.

#### F-092 — `addressing_modes.yaml`: YAML-side example-quality issue surfaced during cross-reference: the auto_decrement …  ·  `DONE`

**Files:** `deliverables/ai/P2/language/pasm2/concepts/addressing_modes.yaml`

**Fix applied:**
- Fix auto_decrement example: replace PUSHB (which is PTRB++ post-increment) with POPB (which IS --PTRB pre-decrement), and add PUSHB as a correct example to the auto_increment block.

**How verified (compiler):** pnut-ts /tmp/test_pushb_f092.spin2 (PUSHB #42 + POPB PA in DAT/org) → exit 0, 'Wrote test_pushb_f092.bin (6300 bytes)'. Confirms both instructions parse and encode without error; encoding difference (post- vs pre-decrement) is a silicon-level behavioral fact verified from silicon-doc alias table, not from compilation output.

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/silicon-doc-v35-walkthrough-audit.md:4003-4006 — alias table: PUSHB=WRLONG register/#,PTRB++ and POPB=RDLONG register,--PTRB
- deliverables/ai/P2/language/pasm2/pushb.yaml:13-14,34,36 — 'Writes long to hub at PTRB++', 'PTRB is automatically incremented after the write', oneliner 'Push long to hub stack using PTRB (post-increment)'
- deliverables/ai/P2/language/pasm2/popb.yaml:13-14,34 — 'Reads long from hub at --PTRB', 'PTRB is automatically decremented before the read', oneliner 'Pop long from hub stack using PTRB (pre-decrement)'
- deliverables/ai/P2/language/pasm2/concepts/addressing_modes.yaml:66-73 — suspect auto_decrement block with PUSHB on line 72 confirmed present verbatim
- pnut-ts v1.55.0 compile probe /tmp/test_pushb_f092.spin2 — both PUSHB and POPB compile cleanly (exit 0)

**Why / rationale:** The defect is unambiguous. The silicon doc (the primary hardware authority) defines PUSHB as WRLONG register/#,PTRB++ (post-increment) and POPB as RDLONG register,--PTRB (pre-decrement). The addressing_modes.yaml auto_decrement block (line 72) places PUSHB there with the comment 'Implicit --PTRB operation', which inverts the actual behavior. PUSHB does PTRB++ (post-increment), not --PTRB. The instruction that actually performs --PTRB is POPB. The fix moves PUSHB to auto_increment and adds POPB as the correct --PTRB example in auto_decrement. pushb.yaml and popb.yaml are themselves already correct and need no changes.

#### F-093 — `lockrel.yaml`: The appendix states the inverted polarity. The authoritative meaning is C = lock-was-held …  ·  `WONTFIX`

**How verified (compiler):** N/A — C-flag polarity is a runtime hardware behavior, not compilable; silicon doc is the ground truth authority.

**Sources that proved it:**
- engineering/ingestion/sources/silicon-doc/part3-end.txt:529-532
- engineering/ingestion/sources/silicon-doc/part4-locks.txt:5-8
- deliverables/ai/P2/language/pasm2/lockrel.yaml:6,30
- engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-iii/appendix-c-categorical-index.md:616

**Why / rationale:** Already correct. The finding claimed two defects: (1) flags_affected.C said "No effect" in lockrel.yaml, and (2) appendix-c-categorical-index.md:617 said "1 if lock was already free" (inverted polarity). Neither defect exists today. Current lockrel.yaml line 6 reads 'c: 1 if lock is currently taken (when WC)' and line 30 reads 'C: When WC: C = 1 if lock is currently taken (last/owner state)' — both correct per silicon doc. Current appendix-c-categorical-index.md:616 reads 'LOCKREL | 1 if lock is currently taken (held)' — also correct. Silicon doc (part3-end.txt:529-530 and part4-locks.txt:5-6) states: 'When LOCKREL is executed with WC, the C flag will indicate whether the lock is currently taken.' C=1 means taken/held, which is exactly what both sources now say. The example code comment at lockrel.yaml:49 ('C = 1 if lock was held') is past-tense phrasing that accurately describes the state AT THE MOMENT the instruction fires (before the lock is released by this same instruction), consistent with the silicon doc. No edit required anywhere.


---

## 5. Refutations (WONTFIX) — investigated, not a defect

- **F-036** — `loc.yaml` category. The proposed recategorization (`Math and Logic` -> `Branch`) is **refuted**: the canonical Parallax CSV (row 431) lists LOC as `Math and Logic`, matching the YAML exactly. (A manual-side LOC categorization inconsistency exists but is a manual-head issue, not a YAML defect.)
- **F-093** — `lockrel.yaml` C-flag polarity. **Already correct** after F-035 was applied earlier in the same sweep: both the YAML and the appendix read C = lock-was-held. No change needed.
- **F-002** — `?` (RNG) / `||` (abs) forms. Prior refutation (agent usage error; KB correct).

---

## 6. Verification gates & reproducibility

```bash
# YAML well-formedness (tree-wide): 1045/1045 clean
python engineering/tools/verify-yaml-format.py

# Cross-reference resolution: 100% (0 unresolved)
python engineering/tools/validate-crossref-keys.py

# Regenerate the encoding reference (picks up gen-script F-047/F-081 fixes)
python engineering/tools/gen-pasm2-encoding-reference.py \
    deliverables/ai/P2/language/PASM2-ENCODING-REFERENCE.md
```

Per-finding `.backup.YYYYMMDD_HHMMSS` files were created for every edited file >100 lines (Sacred Rule #1). They are git-ignored and reserved for `cleanup-backups` at release.
