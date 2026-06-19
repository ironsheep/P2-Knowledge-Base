# Internal-Consistency Fix Plan — F-141…F-153 (+ adjacent) → v1.10.1

**Status:** VERIFICATION COMPLETE (2026-06-19). All 13 findings independently re-proven
against primary sources (Silicon Doc, Spin2 v55, live `pnut-ts` v1.55.0 compiles).
**Awaiting:** 5 decisions (below), then the edit sweep, then v1.10.1 release.
**Active element:** `yaml:p2kb`. **Next finding ID:** F-154.
**Register:** `engineering/operations/P2KB-CORRECTION-FINDINGS.md` (F-141…F-153, all CONFIRMED).

> **MORNING RESUME TASK (Stephen's instruction):** For each of the 5 decisions, give
> BACKGROUND first, then my RECOMMENDATION, then we decide together. After decisions,
> run the sweep via `yaml-knowledge-base-maintenance`, annotate register DONE per §4.5,
> validate, regenerate index (Path B two-commit), tag v1.10.1, refresh p2kb-mcp.

---

## Verification headline

- **13/13 CONFIRMED.** Compile-decisive: F-152 (`TASKRESUME` errors / `TASKCONT` compiles),
  F-146 precedence (`1 + 2 << 3` = 17 ⇒ `<<` binds tighter than `+`; `3 & 1 == 1` = -1 ⇒
  `&` binds tighter than `==`).
- **F-143 latency already fixed inside `cordic.yaml`** (it already says 55 / pipeline 54).
  Only `cog.yaml` and `p2-architecture-mental-model.yaml` still say 54. Do NOT re-touch
  cordic's latency.
- **~9 adjacent defects (🆕) surfaced** — bundle into v1.10.1 per no-deferring discipline.
- Authority order used: pnut-ts → Spin2 v55 → Silicon Doc; detail/instruction pages
  outrank overview/concept/pattern/hub aggregators.

---

## The fix plan — per file (old → new)

### A. CORDIC & latency (F-143 + F-153 latency)
**`architecture/cordic.yaml`**
- L45-50 `fractional_multiply:` block → **`fractional_divide`**: QFRAC = 64÷32 unsigned
  fractional divide, numerator {D, SETQ-or-0} ÷ S; quotient in X, remainder in Y; note
  numerator bit-order {D,SETQ} is opposite QDIV's. (Silicon part3-end.txt:387/390 "Divide…",
  listed under DIVIDE heading L377; qfrac.yaml:12/18-21; encoding 1101001 0.)
- L52-56 `square_root:` → operation **64-bit {S:D} → 32-bit root in X** (floor); setup
  `QSQRT D,S` (S=#0 for 32-bit); result "32-bit root in X". (Silicon part3-end.txt:402-404;
  qsqrt.yaml:12/126.)
- L33 within `multiply:` → **delete `signed: true`** (QMUL is unsigned; keep `unsigned: true`).
  (Silicon part3-end.txt:363-365; qmul.yaml:19/25-27. Signed 32×32 is MULS, not CORDIC.)
- 🆕 L156 sqrt accuracy "16-bit result, ±1 LSB" → "32-bit result, floor of true root".
- 🆕 L158-159 `5.32 fixed-point` → **`5:27 fixed-point`** (log + exp; matches cordic.yaml:78).
- 🆕 (parity, optional) add `signed: false` / `unsigned: true` to the `divide:` block (L38-43).
- LATENCY: already correct (L18/19/200/201/94/100). No change.

**`architecture/cog.yaml`** — L191 `cordic_wait: "0-54 clocks"` → **"0-55 clocks (result
latency; 54-stage pipeline depth)"**.

**`architecture/p2-architecture-mental-model.yaml`** — L136 `latency: "54 clocks per
operation"` → **"55 clocks per operation (result latency; pipeline depth is 54 stages)"**.
(L130-135 "54-stage pipeline" prose = stage count, leave it.)

### B. Interrupts (F-144 + 🆕)
**`architecture/interrupts.yaml`** (authority: Silicon part3-interrupts.txt L73/75/77,
L85-100, L108-113; cog.yaml:59-64/133-135/172-174; event_system.yaml:466-469;
streamer/overview.yaml:125-128)
- L22-24 priority block: currently INT3 highest / INT1 lowest → **INVERT**: INT1 highest,
  INT2 middle, INT3 lowest. (Consider relabeling keys so order isn't misleading.)
  L21 "Debug interrupt highest" and L406 are correct — leave.
- L51-53 `source_types.edge_detect` (Any/POS/NEG-edge-on-SELH) → **DELETE** (fabricated;
  grep "SELH" in part3-interrupts.txt = 0 hits). SELH is a pin-mux selector, not an
  interrupt source. Add the missing real sources instead.
- L197-263 `interrupt_sources_detail` — codes 0-7 OK; **rewrite 8-15**:
  - %1000 → "Pin pattern match OR mismatch (SETPAT)"  [was PAT-match]
  - %1001 → "Hub FIFO wrapped/reloaded (RDFAST/WRFAST/FBLOCK)"  [was PAT-mismatch]
  - %1010 → "Streamer ready for another command"  [was FBW-wrap]
  - %1011 → "Streamer ran out of commands"  [was XMT-empty]
  - %1100 → "Streamer NCO rolled over"  [was Any-edge-SELH — fabricated]
  - %1101 → "Streamer read LUT location $1FF"  [was POS-edge-SELH — fabricated]
  - %1110 → "Attention requested by other cog(s)"  [was NEG-edge-SELH — fabricated]
  - %1111 → "GETQX/GETQY with no CORDIC result (CORDIC empty)"  [was ATN]
- 🆕 L71-100 `configuration_registers` IJMP/IRET map **inverted** — swap to Silicon L108-113:
  $1F0=IJMP3, $1F1=IRET3, $1F2=IJMP2, $1F3=IRET2, $1F4=IJMP1, $1F5=IRET1
  (currently $1F0=IJMP1…; cog.yaml:59-64 already correct — same INT1/INT3 swap as priority).
- 🆕 L294-317 `nested_interrupts` example: fix the priority comments AND `SETINT3 #%1111
  ' ATN event` → `#%1110` (ATN is now code 14). (`pin_change_interrupt` SETINT2 #%0100 = SE1
  is fine.)

### C. Registers (F-145)
**`language/pasm2/concepts/basic-io.yaml`** (Silicon COG-RAM-REGISTER-MAP.md:37-42;
complete-system-registers-index.yaml) — swap the four; DIRA $1FA / DIRB $1FB are correct:
- L68 OUTA `$1FE` → **`$1FC`**
- L75 OUTB `$1FF` → **`$1FD`**
- L79 INA `$1FC` → **`$1FE`**
- L86 INB `$1FD` → **`$1FF`**
(Note: index references detail pages `outa-outb-registers.yaml` / `ina-inb-registers.yaml`
that don't exist — the index itself is authoritative; missing-page is a separate findability
gap, not part of this fix.)

### D. Smart-pin sequencing & roles (F-142 + F-141 + 🆕)
Authority: EF-011 (hardware-ratified universal order Reset→Setup(WRPIN/WXPIN)→Enable(DIRH)→
Operate(WYPIN)); Silicon part4-smart-pins.txt; corrected `smart_pins.yaml`. Detail filenames:
repository=`smart-pin-00001-long-repository-or-dac-noise.yaml`, ADC=`smart-pin-11000-adc-
internal-clock.yaml`, quadrature=`smart-pin-01011-quadrature-encoder.yaml`.

**`language/pasm2/wrpin.yaml`** (F-142)
- L30-35 `critical_requirement.sequence`: reorder WXPIN → **DIRH** → WYPIN (WYPIN last).
- L49-53 PWM example: move `WYPIN #50,#16` to AFTER `DIRH #16`.

**`architecture/smart_pin_patterns.yaml`** (F-141)
- L219 repository `wypin data_value, repo_pin` → **`wxpin`** (X holds the long; Silicon L224/227).
- L149-153 basic-ADC: remove `wypin #1 ' Trigger conversion` — ADC samples continuously once
  enabled; read on IN flag (Silicon L811/868-870; ADC mode file has no WYPIN). Use DIRH + wait-IN.
- L171-176 quadrature `wypin #0 ' Clear counter` → **pulse DIR low** (DIRL/DIRH or pinclear;
  Silicon L550 "zeroed by pulsing DIR low… no need for WXPIN").
- value-mode (motor_pwm L102-105, dac_dithered L122-125, freq_measurement L199-203): move
  `wypin` after `dirh` (order-safe, cosmetic).
- 🆕 L108-109 motor-PWM duty-update "wypin #1 ' Trigger update" — sawtooth %01001 captures Y
  per-frame automatically; reword (no WYPIN trigger).
- 🆕 L141 ADC calibration `wypin #0 ' Trigger` — same fabricated trigger; drop.
- 🆕 L191 measurement-mode `wypin #0 ' Acknowledge` — odd (RDPIN/AKPIN normally acknowledge);
  reviewer note, low priority.
- SPI/sync-serial blocks L23-94 already correct (WRPIN→WXPIN→DIRH→WYPIN) — the in-file model.

### E. Operators / addressing / precedence (F-146 + F-147 + F-153 + 🆕)
**`language/spin2/concepts/operators.yaml`** (F-146)
- L280-282 `~` "Sign extend from bit 7" → **post-clear** (return var, then clear to 0).
- L284-286 `~~` "Sign extend from bit 15" → **post-set** (return var, then set to -1).
  (Detail: special-symbols/~.yaml:5, ~~.yaml:5; v55 L419/420. Real sign-extend = SIGNX/ZEROX.)
- L202-208 anti-pattern `precedence_mistake_bitwise_compare` INVERTED → P2: `&` binds TIGHTER
  than `==`; `flags & MASK == EXPECTED` parses `(flags & MASK) == EXPECTED`. Reframe
  "opposite of C" (the current "wrong" line is actually fine in P2).
- L210-217 anti-pattern `precedence_mistake_shift_add` INVERTED → P2: `<<` binds TIGHTER than
  `+`; `value << 2 + 1` parses `(value<<2)+1`.

**`language/pasm2/concepts/addressing_modes.yaml`** (F-147) — L15-18: AUGS/AUGD framed as
WIDTH (20-bit vs 32-bit) → **by FIELD**: AUGS augments Src, AUGD augments Dest; both yield
32-bit literals (prepend 23 bits to the 9-bit field). (augs.yaml/augd.yaml; Silicon
part3-end.txt:166.)

**`language/pasm2/concepts/register_indirection.yaml`** (F-147) — L45 ALTR
"D + base + index (3-term)" → **`(S + D) & $1FF` (2-term)**, like ALTS/ALTD. (altr.yaml:5-6;
Silicon p2-documentation.txt:1013-1018 — NOTE finding's "part3-end.txt L1013" citation was
wrong file; correct file is p2-documentation.txt.)

**`language/spin2/operators/precedence.yaml`** (F-153 minimum + 🆕 — SEE DECISION 5)
- Minimum: renumber absolute levels to v55 (multiply+divide both L7; add+subtract both L8;
  Limit L9; ADDBITS/ADDPINS **L10** — currently MISSING; comparisons+equality all L11;
  logical-AND L13; OR L15); fix example reason strings (e.g. "Multiply (7) before Add (9)"
  → "before Add (8)").
- 🆕 remove P1-only `===` and `<>>` (v55 has neither).
- 🆕 `^^/XOR` is v55 L14 — currently wrongly merged into the OR level (L15).
- 🆕 add logical `!!`/NOT (v55 term-priority 12) — currently absent.
- 🆕 add missing L7 binary ops `SCA SCAS FRAC +//` (v55 L460-464).

### F. Hardware hubs (F-151 + 🆕 — SEE DECISIONS 3 & 4)
**`hardware/p2-hardware-feature-comparison.yaml`** (authority: edge-standard-module.yaml,
edge-32mb-module.yaml; W25Q128 = 128 Mbit = 16 MByte)
- L29 flash `"4MB"` → **"16MB"**; L44 `"32MB"` → **"16MB"**; L45 psram `"0MB"` → **"32MB"**;
  L60 `"4MB (with P2-EC)"` → "16MB…"; L234 `"4MB Flash, 512KB RAM"` → "16MB…"; L235
  `"32MB Flash, 512KB RAM"` → "16MB Flash, 32MB PSRAM, 512KB RAM"; L350 reword (PSRAM framing).
- 🆕 L33/L48 dimensions `"27×40mm"` → **"37×52mm"** (detail 37.0×51.7mm).
- 🆕 L229 "@ 200MHz" → drop or "up to 180MHz (320 overclock-tested)".
- 🆕 L59 part `"64000-ES"` → **verify → "64000"** (Eval Board) — DECISION 4.

**`hardware/p2-hardware-selection-guide.yaml`** — flash is identical 16MB on both modules, so
re-point the decision logic to PSRAM: L69 "32MB Flash for large apps" → "32MB PSRAM for large
data/framebuffers"; L75 "4MB Flash sufficient" → "16MB Flash; no external PSRAM"; L178-181
boundaries reframe to PSRAM need; L240 mistake reword; L63 question "extra flash?" →
"need external PSRAM?".

**`hardware/hardware-compatibility-matrix.yaml`** — L341 from "P2-EC (4MB Flash)" →
"(16MB Flash, no PSRAM)"; L342 to "P2-EC32MB (32MB Flash)" → "(16MB Flash + 32MB PSRAM)".
L55/63/71 **pin-efficiency column** (62%/87%/30% from same pin_access:40; no documented
denominator; numerator disagrees with detail's 46 accessible) — DECISION 3.

### G. Tasking keyword (F-152 + 🆕 — SEE DECISION 4 note re taskwait)
- **CREATE `language/spin2/methods/taskcont.yaml`** — real keyword, content base = taskresume.yaml:
  `method: TASKCONT`, `syntax: "TASKCONT(TaskID)"`, desc "Continues a task (0..31) halted by
  TASKHALT" (v55 L39), examples → TASKCONT, keep `{Spin2_v47}` (v55 L149), add aliases + related
  to the 6 family members. Drop any "also known as TASKRESUME" (TASKRESUME is fabricated, not an alias).
- **`language/spin2/methods/taskresume.yaml`** → superseded stub: `status: superseded`,
  `superseded_by: language/spin2/methods/taskcont.yaml`, note "TASKRESUME was never a valid
  Spin2 keyword; correct built-in is TASKCONT", related → taskcont.yaml. (Stub-don't-delete: incoming refs must resolve.)
- Cross-ref fixes: `taskhalt.yaml` L10/27/46/58; `taskstop.yaml` L61; `taskspin.yaml` L84;
  `registers/taskhlt.yaml` L85.
- 🆕 **`language/spin2/methods/taskwait.yaml`** — compile-proven fabricated (`TASKWAIT(...)`
  errors EXIT=1; not in v55 L149 family). Orphan (no inbound refs). Stub-don't-delete same way.
  Log as new finding. — DECISION 4 (bundle?).
- Real family (compile-confirmed + v55 L149, all {Spin2_v47}): TASKSPIN, TASKNEXT, TASKSTOP,
  TASKHALT, TASKCONT, TASKCHK, TASKID; constants NEWTASK, THISTASK; register TASKHLT.

### H. Flags / debug / misc (F-148, F-149, F-150, F-153 a-f)
**F-148 — `*rnd`/`*not` WCZ flag wording.** Authority (P2 Instructions CSV + Silicon) says ONLY
"C,Z = OUT/DIR bit" — *neither* "original" nor "new". DECISION 1 (wording) + DECISION 2 (scope).
Files with stray "(original state before modification)": `pasm2/drvrnd.yaml` (L32/43-44/53-54),
`dirrnd.yaml` (L28/38-39/48-49), `fltrnd.yaml` (L32/43-44/53-54), `drvnot.yaml` (L29 — prose
contradicts its own struct fields), `fltnot.yaml` (L29), `outnot.yaml` (L11/15/21-22),
`dirnot.yaml` (L26). 🆕 plain siblings also affected: `drvl.yaml` L33, `dirl.yaml` L10-11,
`outh.yaml` L19-20, `outl.yaml` L14-15 (DECISION 2 = include these?).

**F-149 — `language/spin2/statements/debug.yaml`** SCOPE create-line channel-defs (ledger
EF-003: create-line channel-def prevents window creation; same file L22/L151-152 show correct
split form):
- L124-126 → split: `DEBUG(\`SCOPE MyScope)` then `DEBUG(\`MyScope 'Sensor' AUTO 'Filtered'
  AUTO)` then the feed.
- L171 `DEBUG(\`SCOPE Sensor 'Value' AUTO)` → `DEBUG(\`SCOPE Sensor)` then `DEBUG(\`Sensor
  'Value' AUTO)`.
- L8 `documentation_source: Spin2 v51` → **Spin2 v55** (F-153f).

**F-150 — `language/spin2/patterns/implementation/spin2_pin_control.yaml`** (method pages +
v55: PinField first): L7 `wrpin(mode,pin)`→`wrpin(pin,mode)`; L8 `wxpin($1000,pin)`→
`wxpin(pin,$1000)`; L9 `wypin(0,pin)`→`wypin(pin,0)`.

**F-153a — `pasm2/rdfast.yaml`** L84 "0 = max (16384 longs)" → **"16384 64-byte blocks =
262144 longs = 1MB"** (Silicon p2-documentation.txt:6669-6675; fifo.yaml:229 "16384 blocks =
1MB" is right). Also clarify L12/15 "block size" units.

**F-153b — `pasm2/jnxmt.yaml` L17, `pasm2/jnxro.yaml` L14** `timing.type: fixed` → **variable**
(both carry `clocks: 2 or 4`; twins jnxrl/jnxfi/jatn say variable).

**F-153c — oneliner "set or clear" → "is set"**: `pasm2/jfbw.yaml` L41, `jqmt.yaml` L38,
`jxmt.yaml` L38, `jxrl.yaml` L38 (these are jump-if-SET; own description + CSV say "is set";
JN* twins are jump-if-not-set).

**F-153d — `pasm2/concepts/setq_block_ops.yaml`** L360 `wrong_prefix: "SETQ for LUT, SETQ2
for cog"` → **"SETQ2 for LUT, SETQ for cog"** (matches same file L49/57-65/85-90).
NOTE: register cites this as `spin2/concepts/…`; actual path is **`pasm2/concepts/…`** — fix
register path too.

**F-153e — `spin2/debug-displays/plot.yaml`** L51 "Starts ON by default" + L130 "starts ON" →
**"starts OFF (disabled by default)"** (v55 L1271 PRECISE default = disabled).

---

## The 5 decisions (morning: background → recommendation → decide)

**1. F-148 flag wording.** Sources say only "C,Z = OUT/DIR bit" (no "original"/"new"). Register
proposed "new" (unsourced). My lean: correct to verbatim source ("OUT/DIR bit", drop "original").

**2. F-148 scope.** Include the plain siblings drvl/dirl/outh/outl that also carry "original"?
My lean: yes (data-set-wide harmonization, +4 files).

**3. F-151 pin-efficiency column.** Incoherent (same numerator → 62/87/30%, undocumented
denominator, numerator wrong). (a) delete column, or (b) recompute from one formula
(accessible-pins ÷ 64)? My lean: TBD — present both.

**4. F-151 Eval-Board part `64000-ES`** (likely wrong; Eval Board = 64000, -ES is the 32MB
module alt-part). Fix now to 64000, or log a verify-against-board-source finding? Also DECISION
on **taskwait.yaml** fabrication (bundle stub here, or separate). My lean: bundle taskwait;
present part-number options.

**5. `precedence.yaml` depth.** Minimum (renumber + ADDBITS/ADDPINS) vs full v55 reconciliation
(also remove ===/<>>, fix XOR level, add !!, add SCA/SCAS/FRAC/+//). My lean: full reconciliation.

**Standing defaults (unless vetoed):** bundle all 🆕 adjacent defects + taskwait into v1.10.1;
log new defects as F-154+; source-verbatim wording on #1; data-set-wide on #2.

---

## New findings to log (F-154+) at fix time
- IJMP/IRET address-map inversion in interrupts.yaml (or fold into F-144).
- taskwait.yaml fabrication (TASKWAIT not a keyword).
- precedence.yaml extras (P1 ===/<>>, XOR level, !!, SCA/SCAS/FRAC/+//) if Decision 5 = full.
- Hardware adjacents: dimensions, @200MHz clock, Eval-Board part number.
- Missing register detail pages outa-outb / ina-inb (findability gap).
- Register path corrections: F-153d setq_block_ops is pasm2/ not spin2/; F-147(ii) ALTR
  Silicon citation is p2-documentation.txt not part3-end.txt.

## Release mechanics
Sweep via `yaml-knowledge-base-maintenance` (Sacred Rule #7: redirect refs, never delete) →
annotate register DONE §4.5 → validate (format + crossref) → regenerate index Path B
(content commit → regen → index commit) → tag **v1.10.1** (folds in F-140) → refresh
p2kb-mcp + content-probe.
