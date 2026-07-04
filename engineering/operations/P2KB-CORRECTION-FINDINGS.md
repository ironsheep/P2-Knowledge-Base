# P2KB Correction Findings — Consolidated Register

**Purpose:** A single, append-only register of everything we discover that is **wrong or needs correction** — primarily in the P2 Knowledge Base YAML (`deliverables/ai/P2/`), but also any other source/content correctness issue worth tracking. This is the hand-off document for the agent that corrects the P2KB (via the `yaml-knowledge-base-maintenance` skill).

**How to use this register:**
- When any work (manual production, audits, example compilation, ingestion) surfaces something incorrect, **add it here** — do not leave it only in a per-manual note.
- Each finding gets: an ID, a status, the exact location, what's wrong, the evidence, and the proposed correction.
- **Annotate as you fix, same pass** — flip the status, add an applied-note + source trace, and log any newly-surfaced defects as new findings. See `yaml-knowledge-base-maintenance` skill §4.5. A stale register (statuses lagging the YAML) lies and invites re-chasing.

**Status legend:** `CONFIRMED` (verified against an authority; ready to fix) · `NEEDS-VERIFICATION` (suspected; must be checked before acting) · `DONE` (corrected + verified) · `WONTFIX` (investigated, not a defect) · `RESOLVED-INVALID` (the reported defect does not exist) · `TRACKED → ingestion` (real, but the resolution lives in the ingestion head, not a YAML edit).

**Authority order for P2 language facts:** the `pnut_ts` compiler (ground truth for what compiles) → the Spin2 v55 documentation (`engineering/ingestion/sources/spin2-v55/`) → the Silicon Doc. The KB YAML must match these.

**No inference or derivation.** Every correction must trace to an authoritative source (compiler / hardware-verified / Silicon / authoritative derived YAML). Aligning a file to an authority it contradicts (its own fields, a sibling, the instruction CSV, the compiler) is fine; **inventing a value or claim that no source states — by computation, reasoning, or "it must logically be" — is not.** If a change can only be justified by inference, do **not** make it: log it as a finding that needs a source (or proposes removing the unsupportable content). Match the source's wording, not an interpretive paraphrase.

**Next finding ID: `F-194`**

**Archive:** findings F-001..F-124 (all `DONE` / closed) live in
`engineering/operations/correction-sweeps/2026-06-13-P2KB-CORRECTION-FINDINGS-archive.md`.
**Search the archive before re-filing** — most past defects (and the reasons they were settled) are there.

> **Archival deferred (Stephen's call 2026-06-20):** the v1.10.1 sweep's DONE findings
> (F-125..F-158 + G-001/002/003) are kept in this active register — NOT yet archived —
> because the same sweep's G-004 (Chip-gated) and G-005 (HW-confirm) remain open. Archive
> the whole sweep together once those close (avoids a split sweep). The register is still
> small + glanceable, so this is fine to defer.

---

## Carry-forward guardrails — investigated and settled; do NOT re-file (full detail in the archive)

- **F-002 (`WONTFIX`):** `?` / `||` operator-form failures were an agent usage error — the KB is correct (`??var` = XORO32 random; `ABS()` not `||`; `?` is the ternary operator).
- **F-036 (`WONTFIX`):** `calld.yaml` — LOC loading a 20-bit address into PA/PB/PTRA/PTRB is not a defect.
- **F-093 (`WONTFIX`):** `lockrel.yaml` C-flag polarity — the appendix's "inverted" claim is the error; the YAML is correct (C = lock-was-held).
- **F-114b (`RESOLVED-INVALID`):** the MIDI display modes KEYBOARD / GRID / ROLL / MONITOR do **not** exist in PNut v55 — do **not** add them to `midi.yaml` (it carries an explicit `not_supported:` claim).
- **Verified-resolved (don't re-chase):** the Jan-2026 streamer KB audit's issues were all reconciled in the 2026-05/06 passes (DAC routing, 32-pin groups, mode encoding, xcont/xzero phase wording, setxfrq 2³¹ formula, streamer symbols). Only the XZERO concept text was open and is fixed (F-003).

---

## Open — TRACKED in the ingestion head (resolution lives there, not in a YAML edit)

- **F-121 — #64006 P2 Eval Add-on Board roster: the prior extraction was FABRICATED; cross-edition re-ingestion DONE 2026-06-22.** **Root cause found:** the Aug-2025 extraction invented the *entire* 8-board lineup (LED Array / Switch / Potentiometer / Servo / Sensor / Prototyping / Digital-IO / Analog-IO) — none in the actual guide. Re-ingested cross-edition (2025 `#64006` clean + 2020 `#64006-ES` forced-OCR); both editions agree on lineup + **every pin map**. Real map: **A=Control · B=Serial Host · C=LED Matrix · D=Digital Video Out · E=Mini Prototyping · F=Serial Device · G=Goertzel · H=A/V Breakout** (`#64006-ES` = the set SKU). **Per-board verified sources:** `engineering/ingestion/sources/p2-eval-add-on-boards/boards/addon-*.md`. **→ YAML head:** rebuild `hardware/addon-*.yaml` to the 8 real boards from those docs; the 4 part-number-less orphans (`7_segment_display`, `buttons_board`, `switches_and_leds`, `switches_board`) are **not** #64006 boards — remove/re-home. (The 2 fabricated entries removed in v1.9.0 were the tip of this.)
> **APPLIED (yaml head) 2026-06-24 (v1.11.0):** rebuilt the 8 `addon-*.yaml` #64006 boards to the real A–H lineup in the standardized eval-header shape (verified each pin map against `sources/p2-eval-add-on-boards/boards/addon-*-64006*.md`), and **removed the 4 part-number-less orphans** (`7_segment_display`, `buttons_board`, `switches_and_leds`, `switches_board`) from both the files and `p2kb-categories.json` (zero cross-refs). One `eval_addon_boards` category now holds the 10 eval-header occupants.
- **F-122 — 64004-ES HyperRAM/HyperFlash add-on board has no standalone YAML.** **INGESTION DONE 2026-06-22** — verified extraction at `engineering/ingestion/sources/hyperRam-n-hyperFlash/complete-hyperram-hyperflash-reference.md` (pin map triple-validated, specs/config-pads captured). **→ YAML head:** author the standalone `hardware/addon-hyperram-hyperflash.yaml` from that reference (currently only a bare name in `hardware/p2-eval-board.yaml:145`). Two caveats: (1) the datasheet **part numbers + URLs are OCR-transcribed and flagged `[VERIFY]`** — confirm against the ISSI datasheets / 64004-ES product page before publishing (see KNOWLEDGE-GAPS); (2) board targets the **#64000-ES** (limited-edition ES) Eval Board specifically. Do **not** fabricate from raw CAD.
> **APPLIED (yaml head) 2026-06-24 (v1.11.0):** authored `hardware/addon-hyperram-hyperflash.yaml` from the verified reference — 16-pin board, `signal_map` IO+0..IO+15 with sourced direction (MOSI=out / MISO=in / In-Out=bidir), full specs + config + provenance. Datasheet part#s/URLs included but flagged `[VERIFY]` (OCR, parked). Registered in `eval_addon_boards`; the bare name at `p2-eval-board.yaml:145` was enriched.
- **F-123 — TAQOZ-Forth / ROM-Monitor capability detail rests partly on preliminary web research.** Grounding plan in `engineering/ingestion/sources/taqoz/taqoz-content-gaps-and-grounding-plan.md` (mine `ROM_Booter.lst`; verify vs Peter Jakacki's `TAQOZ.spin2`).

---

## P2KB YAML corrections

> **Sweep origin (2026-06-13):** surfaced while auditing the Debug Window Manual's
> examples against the DEBUG display windows KB. Ground truth used is the **v55 Spin2
> documentation primary source** (`engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt`,
> the per-window directive tables at lines ~1118–1417), which revealed the v1.8.0/v1.9.0
> reconciled `debug-displays/*.yaml` carry several errors/omissions vs that source. All
> findings below are CONFIRMED against the v55 primary source. The manual was, in several
> cases, MORE correct than the YAML.

> **✅ AUTHORITY CORRECTION — RESOLVED (2026-06-14).** The findings below were originally
> derived using the v55 **published documentation text** as authority. That was the wrong
> order: the **Pascal source** (`DebugDisplayUnit.pas`) is ground truth, and the
> `DEBUG-WINDOW-DIRECTIVE-MATRIX.md` (+ per-window theory-of-operations docs) are
> Pascal-derived — the published text is the derivative that carries the off-by-ones. The
> matrix + theory-of-operations were **re-audited against the Pascal source and re-imported**
> (2026-06-14, `REF/` under `p2-debug-window-manual`). The full analysis was **rerun against
> the matrix as authority** and the findings applied/closed below. Net outcome: in the
> majority case the matrix was right and the YAML already matched it (→ `RESOLVED-INVALID`);
> a smaller set were genuine defects (→ `DONE`); and three NEW writing-debug-statement defects
> surfaced during the rerun (F-132/F-133/F-134, all `DONE`). Every changed example was
> compile-verified with `pnut-ts -d`.

## Internal-consistency audit batch (2026-06-18) — F-141…F-153

> **Origin:** full KB-wide internal-consistency sweep (6-way fan-out + hand-verification of the
> top findings) requested after F-140. **Dominant pattern = the F-140 archetype:** stale
> **overview / concept / pattern / hardware-hub** files that were NOT re-synced when their
> **detail pages** were corrected. In every adjudicated case the **detail page (+ Silicon Doc /
> v55 / hardware ledger) is correct** and the overview/concept/pattern is the drift. Statuses are
> `CONFIRMED` (cited authority); ★ = I personally re-verified against the Silicon Doc this pass.
> Re-confirm each at fix time per §4.5.

### F-191 — `architecture/smart-pins/smart-pin-11010-adc-scope-trigger.yaml` places the trigger level in the Y register; it is actually the X register (WXPIN) — `DONE`
> **DONE 2026-07-03.** Proven against the Silicon Doc `p2-documentation.txt:8781-8810`: "WXPIN is used to configure this mode. X[15:10] sets the B trigger value. X[7:2] sets the A trigger value. X[1:0] selects the filter." Y is not used for the trigger. Corrected the YAML: `x_register` now carries the A/B trigger fields + filter select + arm-then-trigger pattern; `y_register` = "Not used in this mode"; `z_register` = 8-bit sample (RDPIN, C=armed); `timing`, `in_flag`, both `code_examples` (WYPIN-trigger → WXPIN A/B/filter, pinstart 4th arg → 0) and `notes` all reworked; dropped the "limited documentation / consult forums" notes (now silicon-sourced); added `related:` SETSCP/GETSCP (the SCOPE data pipe). YAML parse + crossref validated clean. **Also corrected the manual** (was found imprecise during this research, not just the YAML): IOSP Appendix F %11010 card had `X[15:8] Trigger / X[7:0] Arm` → fixed to X[15:10]=B, X[7:2]=A, X[1:0]=filter + a correct example (bundled into the IOSP finalize).
> **Logged 2026-07-02** (surfaced by the IOSP release-gate audit, appendix agent — an inverted finding: the manual is right on the register, the YAML is wrong).
- **Where:** `deliverables/ai/P2/architecture/smart-pins/smart-pin-11010-adc-scope-trigger.yaml` (~L24-27) — currently claims the scope trigger level is written to the **Y** register.
- **What's wrong:** for %11010 P_ADC_SCOPE the trigger level and arm level are set via **WXPIN** (the X register): X[15:8] = trigger level, X[7:0] = arm level. The YAML's Y-register claim is incorrect.
- **Evidence:** IOSP Appendix F %11010 card (X[15:8] trigger / X[7:0] arm) — independently verified this audit; the Titus extract `ingestionSources/mode-11010-adc-scope-trigger/john-titus-extract.md:152-158` ("trigger+arm set via WXPIN / SCP_X"); Silicon Doc part4 SCOPE-trigger section. All three agree it is X, not Y.
- **Fix:** correct the `y_register`/`x_register` roles in `smart-pin-11010-*.yaml` so the trigger/arm levels live in X (WXPIN), matching the appendix + Titus + Silicon. Then re-validate parse + crossref. **This is the actionable item that keeps the IOSP drain gate RED until landed** (see IOSP `audit/release-gate-2026-07-02.md`).
- **Origin:** IOSP release-gate audit, 2026-07-02.

### F-141 — `architecture/smart_pin_patterns.yaml` carries 3 wrong smart-pin register-roles (stale; skipped by the F-135–F-140 sweep) — `DONE`
> **APPLIED 2026-06-20:** `architecture/smart_pin_patterns.yaml` — repository value now stored via **WXPIN** (X holds the long, not WYPIN; `smart-pin-00001-*.yaml` authority); dropped **both** ADC WYPIN "trigger" lines (ADC samples continuously once enabled; `smart-pin-11000-*.yaml` + Silicon part4 L66/73); quadrature "clear" now **pulses DIR low** (DIRL→DIRH; `smart-pin-01011-*.yaml` "pulse DIR low to zero count"); adopted the **universal init order** (WXPIN→DIRH→WYPIN) in the PWM, DAC-dither, and frequency-count patterns. Verified: parse + crossref clean.
- **Repository value via WYPIN (L219)** — should be **WXPIN** (X holds the long; `smart-pin-00001-*.yaml` + Silicon `part4-smart-pins.txt` L224-226). · **Basic-ADC "trigger conversion" via WYPIN (L142/L151)** — ADC samples **continuously** once enabled; no WYPIN trigger (`smart-pin-11000-*.yaml`; Silicon L66/L73/L124). · **Quadrature counter "clear" via `WYPIN #0` (L175)** — zeroed by **pulsing DIR low** (`smart-pin-01011-*.yaml`; Silicon L550). Plus value-mode examples use WYPIN-before-DIRH (order-safe, cosmetic).
- **Fix:** reconcile `smart_pin_patterns.yaml` to the per-mode files (repository→WXPIN, drop ADC WYPIN-trigger, quadrature→DIR-low) + adopt the universal init order.

### F-142 — `language/pasm2/wrpin.yaml` STILL teaches WYPIN-before-DIRH (the F-140 bug, surviving in the instruction page) — `DONE`
> **APPLIED 2026-06-20:** reordered `critical_requirement.sequence` and the PWM example to WXPIN → DIRH → WYPIN (WYPIN after enable) + added a `note:` (trigger modes %00100/%00101 require it; hardware-verified EF-011). Mirrors F-140. Verified: parse + crossref clean.
- `wrpin.yaml` `critical_requirement.sequence` (L30-35) **and** the PWM example (L45-53, `WYPIN #50` at L51 before `DIRH` at L53) both order WYPIN before enable. Contradicts the corrected `architecture/smart_pins.yaml` (F-140) + EF-011. **Fix:** reorder to `…WXPIN → DIRH → WYPIN` + the trigger/serial note (same fix as F-140).

### F-143 — `architecture/cordic.yaml` overview contradicts the (correct) CORDIC instruction pages — `DONE`
> **APPLIED 2026-06-20:** `architecture/cordic.yaml` — QMUL → unsigned (`signed: false`); QFRAC key relabeled `fractional_divide`, described as 64÷32 unsigned fractional DIVIDE per `qfrac.yaml` + Silicon "Divide {D:0} by S"; QSQRT → 64-bit input {S,D} / 32-bit root per `qsqrt.yaml`. **Scoping:** the "latency 54" sub-item was NOT a cordic.yaml defect — the file already carries `result_latency: "55 clocks"` (depth 54 kept separate, correctly). That "54" latency error lives in `p2-architecture-mental-model.yaml` + `cog.yaml` and is handled under F-153. Verified: parse + crossref clean.
- **QFRAC = "fractional multiply" (L45-50) — WRONG, it is a DIVIDE** (`qfrac.yaml`; Silicon L7336 "Divide {D:0} by S"; grouped with QDIV at L2534). **CRITICAL.** · QSQRT "32→16-bit" (L52-56) — actually **64-bit** input, 32-bit root (`qsqrt.yaml`). · QMUL `signed: true` (L30-36) — QMUL is **unsigned** (`qmul.yaml`; Silicon L7304). · CORDIC latency "54 clocks" — **55** (pipeline depth 54; Silicon "fifty-five clocks later"). **Fix:** correct `cordic.yaml` to the instruction pages.

### F-144 — `architecture/interrupts.yaml` has interrupt PRIORITY inverted + a wrong source-ID table — `DONE`
> **APPLIED 2026-06-20:** `architecture/interrupts.yaml` — `priority_scheme` corrected to INT1 highest … INT3 lowest; `interrupt_sources_detail` codes 8–15 rebuilt to the authority (`event_system.yaml:468-469` + `streamer/overview.yaml`: 8=PAT, 9=FIFO, 10=XMT streamer-ready, 11=XFI streamer-done, 12=XRO NCO-rollover, 13=XRL LUT-$1FF, 14=ATN, 15=QMT CORDIC-done), **removing the 3 fabricated SELH-edge sources** (%1100–%1110). The `nested_interrupts` example was relabeled to the correct priority (INT1 cannot be interrupted; INT3 can be interrupted by INT1/INT2) and its ATN selector fixed `#%1111` → `#%1110`. Verified: parse + crossref clean.
- **Priority: file says INT3 highest / INT1 lowest — INVERTED.** Silicon `part3-interrupts.txt` L73/L77/L189: **INT1 highest, INT3 lowest** (matches `cog.yaml`). · **`interrupt_sources_detail` (codes 9-15) shifted/fabricated** (e.g. invents "SELH edge" sources) vs the correct table in `event_system.yaml` + `streamer/overview.yaml` + Silicon L86-100 (8=pattern,9=FIFO,10=streamer-ready,11=streamer-out,12=NCO,13=LUT$1FF,14=ATN,15=CORDIC). **Fix:** rewrite `interrupts.yaml` priority + source table to Silicon.

### F-145 — `language/pasm2/concepts/basic-io.yaml` transposes OUTA/OUTB/INA/INB register addresses — `DONE`
> **APPLIED 2026-06-20:** `language/pasm2/concepts/basic-io.yaml` — OUTA=$1FC, OUTB=$1FD, INA=$1FE, INB=$1FF (OUT/IN blocks un-swapped; canonical map / Silicon L939-947). **Scoping:** the twin `language/spin2/concepts/basic-io.yaml` was checked and is CLEAN — it carries only the correct `$1FA-$1FF` range, no per-register transposition. Verified: parse + crossref clean.
- File: OUTA=$1FE, OUTB=$1FF, INA=$1FC, INB=$1FD. Correct (Silicon L939-947; `system-registers/dira-dirb-registers.yaml`; canonical map): **OUTA=$1FC, OUTB=$1FD, INA=$1FE, INB=$1FF** — the OUT and IN blocks are swapped. **Fix:** correct the four addresses.

### F-146 — `language/spin2/concepts/operators.yaml` carries P1 semantics + inverted precedence claims — `DONE`
> **APPLIED 2026-06-20:** `language/spin2/concepts/operators.yaml` — `~`/`~~` rewritten from P1 "sign-extend" to P2 **post-clear / post-set** (postfix; compiler-verified `flag~`/`flag~~` compile; sign-extend redirected to SIGNX). The two precedence anti-patterns reframed to P2 reality, grounded in `operators/precedence.yaml`: `&` (level 4) binds **tighter** than `==` (level 13); `<<` (level 3) tighter than `+` (level 9) — opposite of C. Verified: parse + crossref clean.
- **`~` / `~~` documented as P1 "sign-extend" (L280-286)** — in P2 they are **post-clear / post-set** (`special-symbols/~.yaml`, `~~.yaml`; v55 operator table). · **Anti-pattern precedence claims inverted (L201-217):** claims C-style "compare binds tighter than `&`" and "`+` binds tighter than `<<`"; P2 is the opposite (`&` tighter than `==`, `<<` tighter than `+` — `precedence.yaml` + v55). **Fix:** rewrite both to P2 semantics.

### F-147 — addressing concept files contradict the instruction pages — `DONE`
> **APPLIED 2026-06-20:** `concepts/addressing_modes.yaml` — removed the fabricated "20-bit AUGS / 32-bit AUGD" width split; AUGS/AUGD split by **FIELD** (Src vs Dest), both forming a full 32-bit literal (`augs.yaml`/`augd.yaml`); fixed the example that mislabeled a Src literal's prefix as AUGD (it is AUGS). `concepts/register_indirection.yaml` — ALTR operation corrected from 3-term `D + base + index` to **2-term `(S+D) & $1FF`**, matching ALTD and `altr.yaml`. Verified: parse + crossref clean.
- `concepts/addressing_modes.yaml` (L16-18): **AUGS/AUGD split by WIDTH** (20-bit vs 32-bit) — actually split by **FIELD** (AUGS=Src, AUGD=Dest; both yield 32-bit literals — `augs.yaml`/`augd.yaml`; Silicon part3-end L166-175). · `concepts/register_indirection.yaml` (L45): **ALTR = D+base+index (3-term)** — actually **(S+D) & $1FF (2-term)**, like ALTS/ALTD (`altr.yaml`; Silicon L1013-1016). **Fix:** correct both concept files.

### F-148 — `drvrnd/fltrnd/dirrnd` + `*not` pin files mis-state the WCZ flag source as "original" bit — `DONE`
> **APPLIED 2026-06-20:** 7 files (`drvrnd/dirrnd/fltrnd` + `outnot/drvnot/fltnot/dirnot`) — the false "original" qualifier removed from the WCZ flag wording, matching the source: the Silicon instruction CSV (`P2 Instructions v35 …`: "C,Z = OUT bit" / "C,Z = DIR bit") and the plain siblings (`drvh.yaml` "Set to OUT bit state"). Prose now reads "the state of OUTA/OUTB's (DIRA/DIRB's) base bit" — no editorial qualifier (an interim "resulting" was dropped per the no-inference rule; the source states "= OUT/DIR bit" without one). **Evidence-scoping:** `drvnot/fltnot/dirnot` already had correct structured `flags_affected`/encoding fields — only their prose carried "original"; the `*rnd` trio + `outnot` needed both prose and structured-field fixes. Verified: parse + crossref clean (`grep original` → none).
- Their `flags_affected`/prose say C,Z = the **original** OUT/DIR bit (before modification); the plain siblings (`drvh/drvc/…`) + the same files' structured fields + the instruction CSV say C,Z = the **(new) OUT/DIR bit**. "original" is bled-over BIT-family wording. **Fix:** align the `*rnd`/`*not` flag wording to the family.

### F-149 — `language/spin2/statements/debug.yaml` examples STILL put a SCOPE channel-def on the CREATE line (the F-137 bug, surviving in 2 examples) — `DONE`
> **APPLIED 2026-06-20:** `language/spin2/statements/debug.yaml` — both SCOPE examples split into create-then-configure form (`DEBUG(\`SCOPE Name)` then a separate channel-def message), mirroring the same file's already-correct TERM/SCOPE pattern (F-137) + EF-003. Verified: parse + crossref clean.
- Examples at L125 `` DEBUG(`SCOPE MyScope 'Sensor' AUTO 'Filtered' AUTO) `` and L171 `` DEBUG(`SCOPE Sensor 'Value' AUTO) `` contradict the **same file's** usage prose (L22) + `scope.yaml` + EF-003 (a channel-def on the SCOPE create line prevents window creation). **Fix:** split into create-then-config-message form (same as F-137).

### F-150 — `language/spin2/patterns/implementation/spin2_pin_control.yaml` reverses smart-pin method arg order — `DONE`
> **APPLIED 2026-06-20:** `language/spin2/patterns/implementation/spin2_pin_control.yaml` — smart-pin method args swapped **pin-first**: `wrpin(pin, mode)`, `wxpin(pin, $1000)`, `wypin(pin, 0)` (method pages + v55 + `pinstart.yaml`). Verified: parse + crossref clean.
- Uses `wrpin(mode, pin)` / `wxpin(x, pin)` / `wypin(y, pin)` (**value-first**); the method pages + v55 + `pinstart.yaml` all specify **PinField first**: `WRPIN(pin, mode)` etc. Compiler can't catch it (positional). **Fix:** swap args pin-first throughout the pattern.

### F-151 — hardware HUB files stale vs the corrected Edge module detail pages (flash/PSRAM) — `DONE`
> **APPLIED 2026-06-20:** 3 hub files (`p2-hardware-feature-comparison`, `p2-hardware-selection-guide`, `hardware-compatibility-matrix`) re-synced to the Edge module detail pages (authority): **P2-EC = 16MB flash / no PSRAM** (was "4MB"); **P2-EC32MB = 16MB flash + 32MB PSRAM** (was "32MB flash, 0MB PSRAM" — the 32MB is PSRAM, not flash). Trace: `edge-standard-module.yaml` (W25Q128, `size_mb:16`, `psram:null`) + `edge-32mb-module.yaml` (`psram total_size_mb:32`). The now-false "4MB-vs-32MB flash" selection/sizing guidance was re-keyed to the **sourced** differentiator (the 32MB PSRAM vs the 512KB hub RAM) — no invented use-cases.
> **CORRECTION 2026-06-20 (no-inference rule):** a first pass also "fixed" the compatibility-matrix pin-efficiency rows (87%/30%→62%) by *computing* `pin_access/64`. That value is **inferred**, not sourced (the metric's definition itself was inferred), so it was **reverted** to the original 87%/30%. The unsupportable pin-efficiency metric is re-filed as **F-160** for Stephen's decision (source it or remove it) — NOT fixed by inference. Verified: parse + crossref clean.
> **DECISION + APPLIED 2026-06-24 (v1.11.0):** Stephen chose **remove the field**. Deleted `pin_efficiency` from all **3** files that carried it — `hardware-compatibility-matrix.yaml`, `edge-mini-breakout.yaml`, `edge-standard-breakout.yaml` (10 occurrences) — keeping the sourced `pin_access`. Grep confirms zero remaining; parse + crossref clean.
- **P2-EC flash:** `feature-comparison`/`selection-guide`/`compatibility-matrix` say **4MB**; `edge-standard-module.yaml` (+ on-board W25Q128, 128 Mbit) says **16MB**. · **P2-EC32MB:** hubs say "32MB **flash**, 0MB PSRAM"; `edge-32mb-module.yaml` says **16MB flash + 32MB PSRAM** (the "32MB" is PSRAM). · `compatibility-matrix` 32MB-module pin-efficiency row ("30%") uses an unsupportable denominator. **Fix:** re-sync the 3 hub files to the module detail pages. (Detail pages = authority; same root cause as HW corrections.)

### F-152 — `TASKRESUME` is a fabricated keyword; the real Spin2 keyword is `TASKCONT` — `DONE`
> **APPLIED 2026-06-20:** compiler re-confirmed (`TASKCONT(3)` compiles; `TASKRESUME(3)` → "Expected an instruction or variable"). Created canonical `methods/taskcont.yaml` ({Spin2_v47}, with aliases incl. the old name for findability); converted `methods/taskresume.yaml` to a **redirect stub** (stub-don't-delete; `status: invalid_keyword` + `redirect_to`), so the fabricated name still routes to the right page; fixed cross-refs in `taskhalt/taskstop/taskspin.yaml` + `registers/taskhlt.yaml` (TASKRESUME → TASKCONT). Verified: parse clean; crossref clean after throwaway index regen (TASKCONT resolves).
- `methods/taskresume.yaml` documents `TASKRESUME(TaskID)`, cross-referenced by `taskhalt/taskstop/taskspin.yaml`. `pnut-ts -d`: `TASKCONT(3)` compiles, `TASKRESUME(3)` errors. v55 history (L39) + keyword-gating table (L149) = **TASKCONT** (v47). Uniform across the cluster (so internally consistent but factually wrong). **Fix:** rename to TASKCONT (stub-don't-delete per supersession convention) + fix cross-refs.

### F-153 — minor internal inconsistencies (batch) — `DONE`
> **APPLIED 2026-06-20:** batch — `rdfast.yaml` block-size now "16384 **blocks** (64-byte units) = 262,144 longs" (was "16384 longs"; `fifo.yaml`/Silicon); `jnxmt`/`jnxro` `timing.type` **fixed→variable** (match their "2 or 4" clocks + the `jxmt` twin); set-only jumps `jfbw/jqmt/jxmt/jxrl` oneliners "set or clear"→"**set**" (match their own descriptions); `setq_block_ops.yaml` `wrong_prefix` corrected (**SETQ2→LUT, SETQ→cog/hub**); `operators/precedence.yaml` rebuilt to **v55 Term-Priority** numbering+grouping (`*`,`/` at 7; `+`,`-` at 8; all compare/equality at 11) + **ADDBITS/ADDPINS** added at 10 (Spin2 v55 operator table); `debug-displays/plot.yaml` PRECISE default **ON→OFF/disabled** (v55 table: "PRECISE … disabled"); `p2-architecture-mental-model.yaml` CORDIC latency **54→55**. **Evidence-scoping:** `cog.yaml` inspected — its `cordic_result_latency` already read "55 clocks (Silicon verbatim)"; its only "54" is `cordic_wait: "0-54 clocks"` (a distinct metric, NOT the flagged latency) — left untouched. `term.yaml` LIME **SKIPPED** (F-128 RESOLVED-INVALID — `clLime` is correct; GREEN would be wrong). The `statements/debug.yaml` provenance **v51 sub-item is NOT done** — relabeling to v55 would assert a whole-file content-vs-v55 match that wasn't verified this pass (no-inference rule); left at v51 pending a content audit. Verified: parse + crossref clean.
- `rdfast.yaml` L84 "block size 0 = max **16384 longs**" vs `architecture/fifo.yaml` "16384 **blocks**" (= 262,144 longs) — `rdfast` off by 16× (Silicon L6675). · `jnxmt.yaml`/`jnxro.yaml` `timing.type: fixed` while carrying `clocks: 2 or 4` (self-contradiction; twins say `variable`). · set-only jumps (`jfbw/jqmt/jxmt/jxrl`) oneliner "flag set **or clear**" vs their own "if set" description. · `concepts/setq_block_ops.yaml` L360 `common_errors` says "SETQ for LUT, SETQ2 for cog" — backwards vs the rest of the file. · `operators/precedence.yaml` absolute level numbers drift from v55 (relative order preserved) + `ADDBITS`/`ADDPINS` missing. · `debug-displays/plot.yaml` L51/L130 PRECISE "starts ON" vs v55 "disabled" default. · `p2-architecture-mental-model.yaml` + `cog.yaml` CORDIC latency "54" vs the 55-clock authority (see F-143). · `term.yaml` default color "LIME" vs v55 "GREEN" (cosmetic — settled RESOLVED-INVALID in F-128; the constant IS clLime). · `statements/debug.yaml` `documentation_source: v51` provenance staleness.

## Streamer grounding-audit drift (2026-06-19) — F-154…F-158

> **Origin:** the exhaustive grounding audit of the **Streamer Programming Guide**
> (`engineering/document-production/manuals/p2-streamer-programming-guide/audit/streamer-grounding-audit-2026-06-19.md`)
> surfaced 4 derived-YAML drift items. Per the trust chain (Silicon Doc = primary), the
> manual's **v1.0.1** fix is grounded directly in Silicon; **these YAML edits fold into the
> next yaml-head sweep (v1.10.1)** alongside F-141…F-153 (Stephen's call 2026-06-19). All
> `value`/`encoding` fields are correct — the errors are in `description:` text only.

### F-154 — `language/spin2/symbols/streamer-symbols.yaml` description text transposes pin↔DAC-channel counts — `DONE`
> **APPLIED 2026-06-20:** `language/spin2/symbols/streamer-symbols.yaml` — 36 transposed `description:` rewritten to "N pins, M DAC ch × B bits" derived from the symbol token (RF/WF families: N from `<N>P`; **IMM family widened in**: N = B, the bits-per-unit in `<A>X<B>` — confirmed via F-158 / Silicon `part2-pixel-ops.txt` "imm 8×4 → 4-pin"). Encodings untouched. Now consistent with `architecture/streamer/modes-reference.yaml` (F-158). Verified: parse + crossref clean.
- For the immediate / RFBYTE-direct / WFBYTE-capture symbol families, the `description:` reads the **DAC-channel count as the pin count** and drops the true pin count. E.g. `X_RFBYTE_8P_1DAC8` (L159) says "→ 1 pin, 8 DAC"; Silicon `part2-pixel-ops.txt` L182 decodes it `RFBYTE -> 8-pin + 1-DAC8` = **8 pins, 1 DAC channel, 8 DAC bits**. The symbol token is `<N>P_<M>DAC<B>` (N=pins, M=DAC channels, B=DAC bits). The sibling `architecture/streamer/modes-reference.yaml` L194 already has it right ("8 pins, 8 DAC bits") — **the two YAMLs disagree**. **Root cause of manual findings H-4 + M-1.**
- **Authority:** Silicon `part2-pixel-ops.txt` L175–209; symbol-name grammar. **Fix:** rewrite every transposed `description:` to "N pins, M DAC ch × B bits" (encodings untouched).

### F-155 — `architecture/streamer/pin-selection.yaml` `%101` group labelled "24 pins"; it is 32 — `DONE`
> **APPLIED 2026-06-20:** `architecture/streamer/pin-selection.yaml` — `%101` group description "24 pins"→"**32 pins**" (the row's own `pins: "7..0, 63..40"` = 8 + 24 = 32; matches the `%110`/`%111` rows). Verified: parse + crossref clean.
- L35 `%101` `description: "Wrap-around (24 pins)"`, but its own `pins:` field is `"7..0, 63..40"` = 8 + 24 = **32 pins** (and the `%110` row correctly says "32 pins"). Manual §4.5 is already right. **Authority:** the row's own `pins:` field; Silicon pin-group def. **Fix:** "24 pins" → "32 pins".

### F-156 — `architecture/streamer/dds-goertzel.yaml` bitstream-sum range "−3..+3" — `RESOLVED-INVALID`
> **AUDIT FINDING INVERTED — VERIFIED 2026-06-19.** The audit (and this finding as first
> logged) claimed the range should be **−4..+4** ("1–4 ADC pins × ±1"). **Silicon overrules
> this:** `part2-more-content.txt` L227-228 (= `p2-documentation.txt` L4094-4095) states the
> sine/cosine values are "multiplied by the bitstream sum (**an integer from -3 to +3**)."
> The −4..+4 reasoning missed Silicon L177-179 (`p2-documentation.txt` L3999-4001): "*For
> cases of two or four input channels summed together, the sum is always even, so it is
> shifted right by one bit*." Effective multiplier magnitudes: 1 pin → ±1; 2 pins → ±2÷2 = ±1;
> 3 pins → ±3; 4 pins → ±4÷2 = ±2. Max magnitude = **3** (the 3-pin case) ⇒ Silicon's −3..+3.
> The YAML `dds-goertzel.yaml:46` "−3..+3" is **correct**; the manual §10.2 "−3 to +3" is
> **correct**. **No edit** to either. Manual finding **M-5 is likewise withdrawn.** (The
> audit's "L403–405" citation pointed at the wrong location; the real text is the lines above.)

### F-157 — `language/pasm2/setxfrq.yaml` 2³¹ vs 2³² NCO basis (re-verify of F-016) — `RESOLVED-INVALID`
> **VERIFIED CLEAN 2026-06-19.** `setxfrq.yaml` uses the 2³¹ ($8000_0000) basis consistently — `description` L13-14, `frequency_formula` L48-52, and an explicit L52 note: "the multiplier is $8000_0000 (2^31), not 2^32 (Silicon Doc v35 SETXFRQ). nco-timing.yaml uses the same convention." F-016's concern is fully resolved; no edit. (SETCFRQ — the *colorspace* NCO — legitimately stays 2³².)

### F-158 — `architecture/streamer/modes-reference.yaml` `selection_guide` recommends a 4-pin mode for 1-pin SPI — `DONE`
> **APPLIED 2026-06-20:** `architecture/streamer/modes-reference.yaml` — `selection_guide.spi_output` set to `X_IMM_32X1_1DAC1 + X_ALT_ON` (1-pin serial; was the 4-pin `X_IMM_8X4_1DAC4`). **Widened:** the IMM-family pin counts in THIS file were also transposed (pins read as DAC-channel count) — all 36 RF/WF/IMM `description:` rewritten to pins = B (per Silicon `part2-pixel-ops.txt` "imm 8×4 → 4-pin"), harmonizing with `streamer-symbols.yaml` (F-154). Verified: parse + crossref clean.
- `selection_guide.spi_output` (L346) recommends **`X_IMM_8X4_1DAC4 + X_ALT_ON`** for SPI output, but Silicon `part2-pixel-ops.txt` decodes `X_IMM_8X4_1DAC4` (mode %0110, D[19:16]=%0100) as a **4-pin** mode ("imm 8×4 → 4-pin + 1-DAC4 … 4 out"). One-pin SPI needs a **1-pin** immediate mode — **`X_IMM_32X1_1DAC1`** ("imm 32×1 → 1-pin + 1-DAC1 … 1 out"; count = number of bits). Surfaced as manual finding L-7; the manual's SPI examples (§13, §16.1) were corrected to `X_IMM_32X1_1DAC1` this pass, grounded in Silicon (the manual must not diverge from the KB on a guess, but here the *primary* source overrides the drifted KB). **Authority:** Silicon `part2-pixel-ops.txt` immediate-mode table. **Fix:** set `spi_output` to `X_IMM_32X1_1DAC1 + X_ALT_ON`; also re-check the IMM-family pin counts (same transposition as F-154/DRIFT-1 — `X_IMM_8X4_1DAC4` is 4-pin, not the "1-pin" the derived tables imply).

### F-160 — `hardware/hardware-compatibility-matrix.yaml` `pin_efficiency` is an unsourced/undefined metric — `FIXED 2026-06-24`
- The `pin_efficiency` percentages (e.g. P2-EC32MB rows: 62% / **87%** / **30%** at identical `pin_access: 40`) have **no sourced definition**. The column label is undefined; the only way to "correct" the inconsistent values is to *infer* a formula (`pin_access/64`) and compute them — which the no-inference rule forbids. The internally-inconsistent values (notably "30%" and "87%", unsupportable from any plausible denominator) remain in the file. **Decision needed (Stephen):** either supply a sourced definition for the metric, or remove the `pin_efficiency` field. Do **not** resolve by inference. Surfaced during the F-151 v1.10.1 work.

### F-161 — `RDLUT`/`WRLUT` (and the hub-operand family) KB prose omits the immediate-address 0–255 limit — `DONE`
- **AUTHORITATIVE SOURCE (read this first):** `engineering/ingestion/external-inputs/pnut_ts_facts/LUT-Immediate-Addressing-Briefing-for-Doc-Agents.md` — a self-contained, PNut-TS-source-verified briefing (cites `spinResolver.ts` `tryPtraPtrb()`, `parseUtils.ts` operand bindings) confirmed empirically against `pnut-ts` v1.55.0. Supersedes the forum post and is more complete than the initial Silicon-Doc-only read.
- **Where:** `deliverables/ai/P2/language/pasm2/rdlut.yaml`, `wrlut.yaml` (primary). The same 0–255 plain-immediate cap is shared by the **whole hub-memory operand family** — `RDLONG WRLONG RDBYTE WRBYTE RDWORD WRWORD WMLONG` — so their YAMLs are in scope for a one-line note too (it rarely bites there: 20-bit hub addresses naturally use register/PTRx/`##`).
- **The facts to represent (all CONFIRMED):**
  1. A **plain immediate** LUT address (`RDLUT d,#S` / `WRLUT d,#S`) is limited to **`#0`–`#255`** (lower half). `#256`+ is a **hard compile error**: `Constant must be from 0 to 255` — NOT a silent runtime trap, NOT a wrap, NOT a wrong-long read.
  2. The **full LUT (0–511)** is reachable via a **register operand** (`RDLUT d, addrReg`) **or** a **`PTRA`/`PTRB`** pointer, optionally indexed (`PTRB[4]`).
  3. **Encoding reason:** the 9-bit `S` field's **bit 8 ($100) is the pointer/expression selector**, not address bit 8; a literal can't set it, so a literal spans only bits 7:0 (0–255). PTRx sets bit 8 deliberately; a register operand (`I=0`) carries the full 9-bit address.
  4. **Do NOT recommend the `##` augmented form** for the upper half: `rdlut d,##500` *compiles* but its low 9 bits (`$1F4`) set bit 8, landing on the pointer-decode path — the AUGS high bits are meaningless for a 9-bit LUT address. Register or PTRx only.
- **Doc guardrails (briefing §7):** don't say `#500` "wraps"/"reads wrong long" (it doesn't assemble); don't say "256 longs are inaccessible" (all 512 reachable — only the *literal* mode is capped); don't cite numeric opcode constants (bit-field diagrams only).
- **Corroboration:** Silicon Doc bit-table `engineering/ingestion/sources/silicon-doc/part3-end.txt:172-218` (`0AAAAAAAA` literal vs `1SUPNNNNN` PTR expr). Surfaced during the p2-assembly-language-manual user-suggestions sprint (OBS-09), `sprint/USER-SUGGESTIONS-2026-06-24.md` (the manual will also document this — briefing §6 copy-paste callout).
- **Fix (yaml head):** add the limit + register/PTRx route + the encoding reason to `rdlut.yaml`/`wrlut.yaml`; add a one-line shared-cap note to the hub RD/WR family. Trace every claim to the briefing (no inference). Honor the guardrails.
> **APPLIED 2026-06-24 (eval-header board sprint, v1.11.0):** `rdlut.yaml`/`wrlut.yaml` gained an `immediate_address_limit` block (the four CONFIRMED facts + guardrails + `applies_to_family`) and findability `aliases`; the 7 hub-family files (`rdlong wrlong rdbyte wrbyte rdword wrword wmlong`) each gained a one-line `immediate_address_note`. Sourced to PNut-TS v1.55 + Silicon Doc bit-table (NOT the working briefing path); no numeric opcodes. Parse-clean.

### F-162 — `hardware/addon-goertzel-touch.yaml` documented an ULTRASONIC application as the board's specs (fabricated transducers + pinout) — `FIXED 2026-06-24`
> **SURFACED + FIXED 2026-06-24 (eval-header board sprint, v1.11.0).** The board YAML had been built around the `Goertzel_ultrasonic.spin2` example rather than the board itself: it fabricated board-level specs (`transducers: 2`, `transducer_type: "40 kHz ultrasonic"`, `transducer_frequency_hz: 40000`) and presented an application's pin usage (DAC differential on base+0/+1, ADC on base+8 “crossing to Header B”) as the board's pinout — none of which is in the source. **Authority:** `engineering/ingestion/sources/p2-eval-add-on-boards/boards/addon-goertzel-64006g.md` (Product Guide v2.0): the Rev-B board is a Goertzel/touch-**pad** board — pads 0-3 & 7 = Goertzel compass set (E/W/N/S + center common), pads 4-6 = switch-style on/off inputs; no on-board transducers. **Fix:** rewrote to the source pad layout (offset→signal `signal_map`, direction omitted on the sense pads per the conservative rule), removed the fabricated transducer specs and the ultrasonic-application pinout, moved the detailed P2-Goertzel-circuit silicon algorithm out of the board file (architecture-layer content), reframed the Quick Bytes ultrasonic resource as an external-transducer application (not a board feature), and fixed a duplicate top-level `educational_value` key. Surfaced by the #64006 source-diff verification; same normalization pattern as the other eval-header boards this sprint.

### F-159 — `language/spin2/operators/precedence.yaml` lists two fabricated equality operators (`===`, `<>>`) — `DONE`
> **SURFACED + APPLIED 2026-06-20 (during v1.10.1 release verification).** The equality level carried `===` and `<>>` — neither is a Spin2 operator: **absent from the v55 operator table** and **both fail to compile** (`pnut-ts`: "Expected an expression term"). They were pre-existing (level-13 "Equality" before the F-153 v55 rebuild) and were carried forward by inference rather than verified. **Removed** both from the comparison/equality level. The sibling forms `!&&` / `!||` (kept) were compiler-checked the same pass and **do** compile — valid, retained. Verified: parse + crossref clean; pnut-ts re-probed.

## YAML additions & enrichments (gaps) — G-001…G-005

> **Surfaced by the Titus rev5 cross-source Q&A + IOSP cross-audit (2026-06-12/13).** These are **additions** (content the KB does not yet carry), not corrections — filed here so the v1.10.1 sweep executes them alongside the F-corrections. G-001 was previously named only in the head dashboards; now formally logged. Per-item gating noted; the gated parts do **not** block the rest.

### G-001 — WRPIN `%AAAA`/`%BBBB` input-selector relative-pin sub-field is undocumented in our YAML — `DONE`
> **APPLIED 2026-06-20:** `language/pasm2/wrpin.yaml` — added `d_operand_format` (the `%AAAA_BBBB_FFF_M…_TT_SSSSS_0` layout) + an `input_selectors` block giving the shared A/B encoding verbatim from Silicon `part4-smart-pins.txt:13-36`: low 3 bits select the source (x000=this pin … x001..x011=+1..+3, x100=this pin's OUT bit, x101..x111=−3..−1), bit3 inverts. Added `aliases:` (incl. P_PLUS1_B/P_MINUS1_B, "clock from adjacent pin") and `related:` → `smart_pin_patterns.yaml` + `smart_pins.yaml` for findability. Verified: parse + crossref clean.
- `language/pasm2/wrpin.yaml` (+ the smart-pin input-routing tables) omit the A/B input-selector sub-field that routes a smart pin's A/B inputs to a relative neighbour pin or to its own OUT. **Add the Silicon-Doc encoding:** `x000` = this pin's true input; `x001..x011` = +1..+3 (nearby pin), `x101..x111` = −3..−1; `x100` = this pin's OUT bit (driven by cogs); bit3 = invert. **Authority:** Silicon `part4-smart-pins.txt:20,33` (verbatim) — this is the field Titus rev5's table got **wrong** (peer-review-caught, silicon-resolved; cross-source-qa Leg 6). **Findability:** add `aliases:` so agents can reach it.

### G-002 — smart-pin timing-mode YAMLs don't record the DIR=0 `Z` preload value — `DONE`
> **APPLIED 2026-06-20:** added `z_register.reset_value` to the 4 mode files — `$00000001` on DIR=0 for `smart-pin-10000/10001/10010` (state/timing; `10010` also reloads `$00000001` when an event restarts its timeout window) and `$00000000` for `smart-pin-10011` (period-counting, with an explicit "unlike the others" note). Authority: Silicon `part4-smart-pins.txt` ("During reset (DIR=0)…Z is set to $0000000{1,0}"). Also added a mode-aware `z_register.reset_preload` pointer to the `architecture/smart_pins.yaml` overview (no single value — it's mode-specific). Verified: parse + crossref clean.
- State/timing modes preload `Z = $00000001` on reset (DIR=0) — prevents a divide-by-zero if Z is read before the first transition; the period-counting mode resets `Z = $00000000`. Absent from `architecture/smart-pins/smart-pin-100*.yaml` (%10000/%10001/%10010) + `%10011` and the appendix register tables. **Add the rule:** "$00000001 on DIR=0 for state/timing modes; $00000000 for period-counting." **Authority:** Silicon `part4-smart-pins.txt:664,678,699,713,724` ($1) + `:753,:799` ($0). (IOSP RA-21/22/23/53/54/55.)

### G-003 — DAC "16-bit" claims lack the nominal/averaged ENOB caveat — `DONE`
> **APPLIED 2026-06-20:** added an `accuracy_caveat` block to `smart-pin-00010` + `smart-pin-00011` stating only what Silicon says — the "16-bit" output is NOMINAL/time-averaged (the 8-bit DAC dithered between adjacent levels to achieve 16-bit output averaged over time). Authority: Silicon `part4-smart-pins.txt` ("achieve 16-bit DAC output, averaged over time"). **No specific ENOB number printed** (Chip-gated, expert queue Q5). **Note (no-inference rule):** an earlier draft added "absolute accuracy is limited by the 8-bit DAC" — a sound inference but NOT stated by Silicon — so it was trimmed. Verified: parse + crossref clean.
- DAC-dither YAMLs (`smart-pin-00010`, `smart-pin-00011`) and DAC resolution claims state "16-bit" with no qualifier. **Add the Silicon-backed caveat:** "16-bit DAC output **averaged over time**; absolute accuracy is limited by the 8-bit DAC." **Do NOT print a specific ENOB number** — the reviewer's "~10–12 real bits" is opinion, not in any primary source; a printable figure is Chip-gated (expert queue Q5). **Authority:** Silicon `part4-smart-pins.txt:272`. (IOSP RA-18/36/49/56.)

### G-004 — `architecture/smart-pins/smart-pin-11011-usb-host-device.yaml` X/Y/Z registers are one-line stubs — `PARTIAL — Silicon layer SHIPPED 2026-06-20 · remainder still Chip-gated (OPEN)`
> **APPLIED 2026-06-20 (provable part):** replaced the one-line X/Y/Z stubs with the full Silicon-confirmable register layer — WXPIN config word (D[15] host/device, D[14] FS/LS, D[13:0] baud = 16-bit sysclk fraction, two MSBs 0), WYPIN line-state D-values (0=IDLE, 1=SE0, 2=K, 3=J, 4=EOP, $80=SOP) + packet-send protocol, the 16-bit RX status word (all 10 documented bit-fields), and per-pin IN semantics (odd/DP = TX-buffer-empty; even/DM = RX-status-change; C = RX error). All WXPIN/WYPIN/RDPIN issued on the lower/even pin. Authority: Silicon `p2-documentation.txt:8886-9006` (verbatim). **STILL OPEN (Chip-gated):** logged an in-file `open_questions:` block — RX analog front-end / line-state detector thresholds / any scope-style filter taps are NOT in Silicon and remain in the expert queue. This finding stays PARTIAL.
- The USB-host/device mode carries no register detail. **Add the Silicon-Doc-confirmable layer now:** WXPIN config word (D[15]=host/device, D[14]=FS/LS, D[13:0]=baud), WYPIN line-state D-values (0=IDLE…$80=SOP), RX 16-bit status word, per-pin IN semantics (odd/DP = TX-buffer-empty, even/DM = RX-status-change). **Authority:** Silicon `p2-documentation.txt:8886–8960`. **Gated remainder:** any figure not in Silicon (e.g. scope-style filter taps) stays in the expert queue (Chip). (IOSP RA-38/40/42/43/46/47.)

### G-005 — `architecture/smart-pins/smart-pin-11110.yaml` (async TX) omits the first-byte low-glitch gotcha — `DONE (2026-07-04) — HW-CONFIRMED NOT-OBSERVED (EF-016)`
> **CLOSED 2026-07-04 from existing hardware evidence.** The "Batch 2" hardware confirmation this finding was
> waiting on **already ran** — `test51b-asynctx-firstbyte-glitch-wired` (RA-19, 2026-06-17, ledger **EF-016**):
> over a real wired loopback (TX P0 → RX P2) the cold first byte arrived **clean** with no settle frame and no
> preclear, for both `$A5` and `$01`. The gotcha did **not** reproduce. The register entry was stale (still
> "OPEN pending hardware") while the empirical answer was on the ledger. **Applied:** reframed the
> `gotchas.first_byte_low_glitch` block in `smart-pin-11110-async-serial-transmit.yaml` from an asserted
> symptom + `NEEDS-HW-CONFIRM` to **HW-CONFIRMED NOT-OBSERVED** (community lore, not reproduced; the `$FF`
> pre-clear is optional belt-and-suspenders, not a rule). No new test needed.
> **APPLIED 2026-06-20 (recorded as attributed gotcha):** added a `gotchas.first_byte_low_glitch` block to `smart-pin-11110-async-serial-transmit.yaml` — symptom (first byte after enable may glitch the line low), the harmless `WYPIN $FF` pre-clear workaround, attribution (community-credited to Ray Rodrick), and explicit `status: NEEDS-HW-CONFIRM` pointing at IOSP verification Batch 2 (todo #53 / RA-19). **STAYS OPEN** — not in any primary source and not compile-verifiable; the register entry remains NEEDS-HW-CONFIRM until the Batch 2 hardware run confirms it.
- Async-serial TX drops the line low for the first byte after enable; the harmless `$FF` pre-clear workaround is well-attested (community-credited to Ray Rodrick). Not compile-verifiable (runtime/pin behavior). **Add as an attributed gotcha**, flagged for hardware confirmation in IOSP verification **Batch 2** (todo #53 / RA-19). **Authority:** community + pending-hardware.

---

### F-140 — `architecture/smart_pins.yaml` OVERVIEW still teaches the OLD init order (WYPIN before DIRH); F-139 swept the per-mode files but missed the overview — `DONE`
> **Logged + DONE 2026-06-18.** Surfaced while auditing the **PASM2 Reference + DeSilva** manuals for smart-pin staleness — the manuals had inherited the old order, and the trail led back to this overview page. F-135/F-139 ratified the universal order **Reset → Setup (WRPIN/WXPIN) → Enable (DIRH) → Operate (WYPIN)** (WYPIN *after* enable; hardware-verified EF-011) and corrected the per-mode `architecture/smart-pins/smart-pin-*.yaml` files — but the **overview** `smart_pins.yaml` was not updated. Its `critical_requirements.reset_before_configure.correct_sequence` (pasm2 **and** spin2) and `live_update_behavior.what_needs_reset.procedure` both still showed `…WXPIN → WYPIN → DIRH` (WYPIN before enable). It was even internally inconsistent with the file's OWN `live_update_behavior` ("once configured, DIR can be raised high … after that you may feed it new data via WXPIN/WYPIN").
> **FIX APPLIED 2026-06-18:** `correct_sequence` reordered to WYPIN-after-DIRH (pasm2 + spin2; the spin2 form was switched from `PINSTART(pin,mode,x,y)` — which writes Y before raising DIR and is unsafe for the trigger modes — to the explicit safe sequence) with a `note:` explaining why; the `procedure` line corrected to `DIRL → WRPIN/WXPIN → DIRH → WYPIN`. YAML valid + crossref clean. **Ships next YAML release** (published v1.10.0 index does not yet carry it).
- **Where:** `deliverables/ai/P2/architecture/smart_pins.yaml` (`critical_requirements…correct_sequence`; `live_update_behavior…procedure`).
- **Authority:** ledger EF-011 (hardware-ratified universal order); the corrected per-mode `smart-pin-00100/00101-*.yaml`; Silicon Doc (trigger-mode Y is held 0 during reset).
- **Origin:** PASM2/DeSilva smart-pin staleness audit, 2026-06-18 — see each manual's `audit/smartpin-debug-staleness-audit-2026-06-18.md`.

### F-138 — ch09 "Creating an FFT window" inline minimal example renders NOTHING (declares no channel) — `DONE (manual)`
> **Logged + DONE 2026-06-17.** Surfaced when `test2c-fft-baseline.spin2` (the inline snippet copied verbatim) showed a BLANK FFT window on BOTH PNut-Term-TS and real PNut (Stephen). Root cause: the minimal example feeds samples to an FFT window with **no channel declared** — with zero channels there is nowhere for samples to land, so nothing renders (chapter prose: a channel is declared by sending a string label; fed samples distribute across declared channels). Every *rendered* example already declares a channel — `figure-generators/fig-09-fft.spin2` (made the figure) and `examples-library/ch09-fft-spectrum.spin2` (bundled demo) both do — so the manual's demos are fine; **only the inline teaching snippet (prose, never a rendered demo) omitted it.** **Distinct from F-137** (that is create-line channel-defs *breaking*; this is the snippet having *no* channel at all). The snippet also used `getct()` as the sine angle, which aliases to broadband noise even when rendered.
> **FIX APPLIED 2026-06-17** to `opus-master/ch09-fft.md` (the "Creating an FFT window" example + its lead-in sentence): added the channel-declaration line, swapped `getct()` → a phase accumulator on a clean bin, and adopted the proven `fig-09-fft.spin2` recipe (`LOGSCALE` + full-scale **1000** — the fig generator's own note warns `$7FFF_FFFF` "made peaks vanish"); reworded the lead-in to say a channel must be declared first (forward-ref to the next section). Backed up ch09-fft.md before the edit. **HARDWARE-CONFIRMED** via `audit/verification-tests/test2d-fft-with-channel.spin2` (= the corrected snippet) — Stephen ran it on PNut-Term-TS: single clean peak.
- **Where:** `engineering/document-production/manuals/p2-debug-window-manual/opus-master/ch09-fft.md` (the "Creating an FFT window" minimal example + its lead-in sentence). **Released-manual note:** the Debug Window Manual is out for community review (v1.0.0); this correction rides into the next regeneration.
- **Evidence:** test2c (verbatim snippet) blank on both hosts; test2d (snippet + the one channel-decl line + phase/scale fix) renders a single peak. Chapter prose + both rendered example sources confirm the channel declaration is required.
- **Not affected:** the YAML (`fft.yaml`) — it documents channel declaration and its examples include a channel string. (A separate open question — whether FFT tolerates a channel-def on the *create line*, as fft.yaml's examples do, vs the proven separate-message form — is being settled by `test2e`; see F-137.)
- **Origin:** debug-display REF re-audit 2026-06-17; FFT-render-gap investigation (initially mis-attributed to a PNut-Term-TS host bug, then briefly over-claimed as a released-demo defect, corrected on Stephen pushback to this narrow inline-snippet scope).

### F-139 — universal-order set-wide sweep: value-mode + sync-serial smart-pin examples reordered (completes F-135 #5) — `DONE`
> **DONE 2026-06-18.** Reordered to enable→WYPIN: `smart-pin-00110-nco-frequency.yaml` (5 sites — incl. the quadrature pair, both `PINHIGH`s kept back-to-back with `WYPIN`s after to preserve the simultaneous start, and the `freq_sweep` loop restructured with `DIRH` ONCE before the loop), `smart-pin-00111-nco-duty.yaml` (5 sites, same loop restructure), `smart-pin-00010-dac-16bit-pseudo-random-dither.yaml` (3 sites; ADC-feedback `PINWRITE` kept before enable), `smart-pin-00011-dac-16bit-pwm-dither.yaml` (2 sites), `smart-pin-11100-sync-serial-transmit.yaml` (1 site — `stream_continuous` prime-shifter moved after enable; double-buffer preserved). **`spi-implementation-guide.yaml` left UNCHANGED — on inspection it is already correct** (`PINSTART(SPI_CLK, P_TRANSITION, …, 0)` passes Y=0 = benign; the real trigger `WYPIN(SPI_CLK, 16)` is post-enable). sync-TX %11100 reorder rests on the ratified principle + compile (it was not in the test60-63 hardware sweep — async-TX %11110 was), per Stephen's OK. YAML format + crossref validated clean.
> **Logged 2026-06-18.** F-135's design decision adopts one universal init order (Reset→Setup→Enable→Operate) across ALL smart-pin examples. The CORRECTNESS cases (trigger modes %00100/%00101, where WYPIN-before-enable is broken) are DONE. This tracks the remaining COSMETIC-consistency reorders, deferred because each carries an intentional special-case a blind swap would break:
- **NCO %00110:** a quadrature "start together" pair (two pins primed, then `PINHIGH`/`PINHIGH` back-to-back for phase sync) + a `.loop WYPIN…DIRH` frequency-sweep.
- **NCO %00111:** a `.loop WYPIN…DIRH` pattern.
- **DAC %00010:** `setup_with_feedback` interleaves `PINWRITE(...,1)` (OUT=1 enables ADC) with enable.
- **DAC %00011:** simple init sites (low risk) — bundle with %00010 for one verified pass.
- **sync-serial %11100 + spi-implementation-guide:** `stream_continuous` *primes the shifter* before enable then *loads the buffer* after — the documented double-buffered gapless-TX technique; NOT ratified by test60-63 (which covered async TX %11110, a different mode).
> **Note:** these are ORDER-INSENSITIVE for correctness (Y is a value, not a trigger; test61 NCO / test63 DAC = PASS-SAFE both orders) — reordering is purely pedagogical consistency. Verify each special-case (ideally a quick hardware/compile check that the reordered quadrature still phase-syncs and the double-buffer still streams gaplessly) before applying. async-TX %11110 needs no change (no WYPIN-before-enable).
> **HARDWARE-VERIFIED 2026-07-04 (🏆, ledger EF-019):** the two flagged special cases confirmed on silicon under the reordered init. `test72-nco-phaselock` — a phase-locked NCO pair (90° via WXPIN): period T=2000 clks exact, A→B offset dead-stable at 1580 clks across 4 repeats (spread 0) ⇒ still phase-locked. `test73-syncserial-gapless` — %11100 continuous TX, prime-after-enable: steady inter-word cadence ≈ one word-time (spread 16) ⇒ still gapless double-buffering. Residual hardware checks CLOSED.
- **Where:** `deliverables/ai/P2/architecture/smart-pins/{smart-pin-00110-nco-frequency,smart-pin-00111-nco-duty,smart-pin-00010-dac-16bit-pseudo-random-dither,smart-pin-00011-dac-16bit-pwm-dither,smart-pin-11100-sync-serial-transmit,spi-implementation-guide}.yaml`.
- **Origin:** F-135 set-wide sweep, 2026-06-18 — scoped down on reading the actual examples (special-cases that don't fit a blind universal-order swap).

### F-137 — SCOPE channel-def on the create line BREAKS window creation; channel/trigger setup must be a separate one-time configuration message — `DONE (YAML + ch07 manual)`
> **Logged 2026-06-17.** Surfaced re-auditing the debug-display YAMLs against the refreshed `REF/` golden sources (2026-06-16 directive matrix + theory-of-operations).
> **CONFIRMED 2026-06-17 (hardware, Stephen) — CLEAN run** of `test2-createline-vs-config.spin2` (after the Term-TS window-registration bug was fixed; no console error). Of the 6 windows the program creates, **only 5 appeared — `SC_in` was MISSING.** `SC_in` is the SCOPE whose channel-def (`'SC inline' -1000 1000`) sits on the create line: **the window never created.** Present + running: `SC_sp` (SCOPE, channel-def sent as its OWN message after create), `LG_in` (LOGIC), `XY_in` (SCOPE_XY), and both FFT windows. => **putting a SCOPE channel-def on the create line prevents the window from being created**; the channel/trigger setup MUST be a separate message after create (3-phase model: create -> one-time config -> looping updates). LOGIC + SCOPE_XY create-line channel/label work (config-phase windows). **Asymmetry noted:** the SCOPE def had trailing NUMBERS (`-1000 1000`) and broke creation; FFT's bare-string label (`'FF inline'`) did NOT break creation (FF_in appeared) — the label just won't apply. **FFT label-detail still pending** a clean read (both FFT windows were empty in this harness: no channel scale -> spectrum at the floor; retest with a scaled channel `test2b-fft-createline.spin2`).
>
> **APPLIED 2026-06-18 (YAML):** split-form rewrite done in `scope.yaml` (3 examples + `syntax.create`/new `channel_setup` + the `channel_definition` note), `fft.yaml` (2 examples + syntax + note), and `statements/debug.yaml` (SCOPE + FFT `usage:` lines + the multi-display example). SCOPE_XY/LOGIC create-line labels left as-is (config-phase, correct). The FFT label-detail question resolved separately: the FFT render-gap was the inline MANUAL snippet missing a channel decl (**F-138**, manual fixed) — not a create-line-label defect. Manual `ch07-scope.md` create-line examples ALSO split 2026-06-18 (3 code blocks + the channel-declaration prose; backed up first) — the chapter now matches its own later `Capture`/`Glitch` split-form examples. (`ch09-fft.md` was the separate **F-138** fix.) These ride the debug-window-manual's next regeneration. YAML format + crossref validated clean.
> **Fix:** rewrite every create-line channel-def/label example into the split form (create the window, THEN send the channel-def/trigger as its own message before streaming). Touches: `deliverables/ai/P2/language/spin2/debug-displays/scope.yaml` (all 3 examples), `fft.yaml` (2 examples), `statements/debug.yaml` (SCOPE/FFT usage lines + examples), and manual chapters `opus-master/ch07-scope.md` (L39) + `ch09-fft.md`. For SCOPE this is a hard defect (create-line examples don't produce a window), not cosmetic.
- **Where (suspect examples):** `deliverables/ai/P2/language/spin2/debug-displays/{scope,fft}.yaml` (the `examples:` that put a channel-def/label string on the CREATE line, e.g. `` DEBUG(`SCOPE MyScope SIZE 400 200 'Signal' AUTO) `` / `` DEBUG(`FFT Audio SAMPLES 512 LOGSCALE 'Spectrum') ``); the same idiom in `statements/debug.yaml` examples (e.g. `` DEBUG(`SCOPE MyScope 'Sensor' AUTO ...) ``) and in the manual chapters `opus-master/ch07-scope.md` (L39) and `ch09-fft.md`.
- **What's suspected wrong:** for **SCOPE and FFT**, channel-def strings are **update-phase**, not config-phase — so a string placed on the creation line is not parsed by `_Configure` and is silently dropped (and per Stephen the trailing elements can cause the create itself to be ignored). Compile-clean proves nothing here.
- **Evidence (golden, Pascal-derived):** matrix §0 — *Configuration phase (`XXX_Configure`) runs once at window creation; Update phase (`XXX_Update`) runs on every **subsequent** message*. Matrix §2 (config, L108) shows `string = channel def` ✅ for **LOGIC** and **SCOPE_XY** only; §3 (update, L136) shows `string channel def` ✅ for **SCOPE** and **FFT** (TERM = `text`). SCOPE theory §21.2: *"`SCOPE_Configure` parses **keys only**; channel-label strings and TRIGGER/HOLDOFF are handled later by `SCOPE_Update`, **not here**."* FFT theory: channel-def string *"Accepted by `FFT_Update` — run on every subsequent message."* Stephen testimony: create-line elements "were just ignored and no create happened."
- **Scope note:** create-line strings ARE valid for **LOGIC** (channel def) and **SCOPE_XY** (label) — those are config-phase (matrix §2 fn10/fn11). The suspect set is SCOPE + FFT (update-phase strings); TERM text is also update-phase (see F-136).
- **Verification:** run a probe that (a) creates a SCOPE/FFT with the channel-def on the create line in ONE message, vs (b) creates with config keys only then sends the channel-def in a SEPARATE subsequent message; observe which actually creates the window and labels/ranges the channel. Then settle the canonical idiom and sweep the per-window YAMLs + `statements/debug.yaml` + manual chapters together.
- **Origin:** debug-display REF re-audit 2026-06-17 (fan-out: FFT agent flagged it for FFT; SCOPE missed; reconciled on hand-verification).

### F-136 — backtick DEBUG named-window text must be SINGLE-quoted, and a value is displayed with `` `(value) `` substitution (NOT a value-only formatter) — `DONE (YAML) · ch03-term.md DONE (rides next regen)`
> **RESOLVED 2026-06-18 — no hardware probe needed; the v55 doc already answers it.** The "labeled-value idiom" was never a gated/open question — the Spin2 **v55 documentation** (`spin2-v55-text.txt` L1090 + the canonical named-TERM example **L1299** `` debug(`MyTerm 1 'Temp = `(i)') ``) shows the idiom directly: in a named feed you display a value's decimal TEXT by **substituting it with `` `(expr) ``** (L1090: *"Decimal numbers are output using `` `(value) `` notation. Short for SDEC_."*) inside SINGLE-quoted text. This **reconciles** the EF-002 hardware result rather than contradicting it: W4's `` `udec_(value) `` rendered a raw glyph (char 42 = `*`) because the **trailing-underscore value-only formatters** (`udec_`/`sdec_`/`uhex_`) emit a *numeric data element* — the form the graphical windows (SCOPE/LOGIC/FFT) consume as a data point — and a TERM renders that number as a character glyph. The value-to-TEXT path in a named feed is `` `(expr) ``, full stop. The earlier "named TERMs don't format; use plain debug()" inference was wrong (and is corrected in the ledger).
> **APPLIED 2026-06-18 (YAML):** `term.yaml` example 2 rewritten to `` DEBUG(`MyTerm 1 'Temperature: `(temp) C' 13) `` and a new `display_directives.value_display` note added (the `` `(expr) `` rule + the formatter-as-glyph caveat, citing EF-001/EF-002 + the v55 canonical example). `statements/debug.yaml` already correct (its `udec_()` examples are all PLAIN default-terminal output; its one named-TERM example already single-quoted). All forms compile-verified with `pnut-ts -d`.
> **APPLIED 2026-06-18 (manual):** `opus-master/ch03-term.md` swept end-to-end — every named-feed example converted from double-quoted text → single-quoted, and every value display from `` `udec_()/`sdec_() `` → `` `(value) `` substitution; the "Sending text" + "Considerations" prose rewritten to teach the single-quote + `` `(value) `` rule and the formatter-as-glyph trap. Rides the debug-window-manual's next regeneration (manual is out for community review v1.0.0). **Grounds:** ledger EF-001 + EF-002 (the open-question item is now closed).
> **Logged 2026-06-17.** Same re-audit.
> **CONFIRMED 2026-06-17 (hardware, Stephen)** via `test1-term-string-quoting.spin2`: SINGLE-quoted body text displayed in full (W2); BOTH DOUBLE-quoted bodies were silently dropped (W1, W3 blank). W3 is exactly the `term.yaml` example-2 idiom (comma + bare formatter + double-quoted strings) — it showed nothing. W4 (`` "text" `udec_(value) "text" ``) rendered only a single glyph `*` = char 42 = the raw value, proving a value fed via `` `udec_() `` into a NAMED TERM arrives as a RAW byte, NOT as decimal text, and the double-quoted text around it vanished. => (a) backtick display text must be SINGLE-quoted; (b) the "labeled value" TERM idiom we ship does not work as written. **Fix scope:** rewrite TERM text examples to single quotes, AND first determine the correct way (if any) to display a formatted value's TEXT in a named TERM before rewriting the labeled-value examples. Sweep `term.yaml`, `statements/debug.yaml`, and manual `ch03-term.md` together.
> **APPLIED 2026-06-18 (YAML, single-quote part):** single-quoted the plain backtick display text in `term.yaml` (example 3 → `'Row 2, pair 0'`) and `statements/debug.yaml` (the multi-display example → `` DEBUG(`Status 'Starting test...', 13) ``). The `string_quoting` notes were already correct. **GATED — not done:** the labeled-VALUE idiom (`term.yaml` example 2: `` "Temperature: ", SDEC(temp), " C" `` into a named TERM). How to display a formatted value's TEXT in a named TERM is still unsettled — `test51b` proved the trailing-underscore `uhex_*_` form is value-only for PLAIN `debug()` output, but the named-TERM-feed path is different (W4 showed a raw byte). Needs a named-TERM value-display hardware probe before rewriting. The manual chapter `ch03-term.md` is the debug-window-manual pass (not a YAML edit).
- **Where (suspect examples):** `deliverables/ai/P2/language/spin2/debug-displays/term.yaml` (`examples:` feeding TERM text in double quotes, e.g. `` DEBUG(`MyTerm "Temperature: ", SDEC(temp), " C", 13) ``); `statements/debug.yaml` examples (e.g. `` DEBUG(`Status "Starting test...", 13) ``, L146); the TERM manual chapter `opus-master/ch03-term.md` (uses double quotes pervasively).
- **What's suspected wrong:** the quoting authority says backtick **display-command text uses SINGLE quotes**; a double-quoted text arg is *silently ignored at runtime, no compile error*. If TERM printed strings fall under that rule, the double-quoted examples print nothing. **`statements/debug.yaml` contradicts ITSELF** — its `string_quoting.rule`/`silent_failure` says single-quote-only, but its own examples feed TERM text in double quotes.
- **Evidence:** quoting briefing `DEBUG-Statement-Quoting-Briefing-for-Doc-Agents.md` §1B/§2 — a backtick statement has only two segment types: *display-command text* (keywords, numbers, **single-quoted** strings) and `` `(expr) `` substitutions; there is no slot for a bare double-quoted string. `statements/debug.yaml` `string_quoting` (`verified_against`: compiler emits backtick text raw via `debugTickString`; host parser `check_dd_str` recognizes **only the apostrophe**). TERM theory describes the protocol-level `ele_str` (prints verbatim) but is **silent** on how Spin2 `"..."` vs `'...'` becomes an element — it does not settle the question. Note F-130 rewrote the `statements/debug.yaml` examples under **compile-verification only**.
- **Verification:** probe `` DEBUG(`MyTerm "text") `` vs `` DEBUG(`MyTerm 'text') `` vs the `` `(expr) ``/formatter form; observe what actually prints to TERM. Settle the canonical TERM-text idiom, then sweep term.yaml + `statements/debug.yaml` + the manual chapter together.
- **Origin:** debug-display REF re-audit 2026-06-17 (TERM agent flagged single-quote rule; initially over-ridden on compile-clean+manual, corrected by Stephen).

### F-135 — smart-pin %00101 (Transition Output): "Y=0 = continuous transitions" is FALSE (Y=0 is idle); plus a suspected WYPIN/enable order defect — `DONE (YAML) · set-wide sweep DONE via F-139 · MANUAL DONE`
> **Logged 2026-06-17** (RA-10 from the IOSP Titus cross-audit; todo #55).
> **MANUAL DONE 2026-07-02 (RA-10 reversal in the IOSP guide):** swept the IOSP opus-master for the false claim. Found it in exactly one place — `part-5-appendices/appendix-f-mode-reference.md` %00101 Register-Usage table: cell said `Y[15:0] | Transition count (0 = continuous)` (wrong width AND the false continuous claim), and the row above carried a fabricated `X[31:16] | Initial output state time` (no such field in Silicon Doc/Titus/YAML for this mode — the manual's own Ch.7 §7.3 + Quick-Reference list only X[15:0]+Y[31:0]). Corrected to `Y[31:0] | Transition count (0 = idle; use NCO %00110/%00111 for continuous)` and removed the phantom X[31:16] row. Ch.7 §7.3, its Quick Reference, and appendix-d were already correct (counted / "Y reaches 0 → toggling stops" / redirect to NCO for continuous). Fix traces to Silicon Doc `part4-smart-pins.txt` L351-366 + Titus L487-491 + corrected `smart-pin-00101-transition-output.yaml`. Folds into the pending IOSP visual-findings render batch (F1).
> **CONFIRMED FALSE 2026-06-17 (hardware, Stephen)** via `test3-smartpin-00101-y0-continuous.spin2` with a bidirectional rig test (P0<->P2 and P1<->P3 both verified OK) and a working control: P1 at **Y=2000 TOGGLED ~10 s then went STATIC** (proving the mode runs, the loopback reads it, and the init order is right), while **P0 at Y=0 read STATIC the entire run — it never toggled**. => **Y=0 does NOT produce continuous transitions; it leaves the pin idle/stopped**, exactly as the Silicon Doc / Titus wording implies. Continuous square-wave generation belongs to the NCO modes (%00110/%00111). **Fix:** remove the `continuous_mode` block + correct the `continuous_square()` (Spin2) and `continuous` (PASM) examples — redirect continuous-output guidance to NCO.
> **SECOND item — CONFIRMED 2026-06-17 (hardware, Stephen)** via `test4-init-order-compare.spin2` (rig OK; both pins identical at Y=2000, only the init order differs): P0 with the **OLD order (WYPIN before PINHIGH) read STATIC — never toggled**; P1 with the **NEW order (PINHIGH before WYPIN) TOGGLED ~10 s then stopped**. => for %00101 the toggling Y-write MUST come AFTER the pin is enabled (DIR high); writing Y while still in DIR=0 reset never triggers, because Y is held 0 during reset. The YAML's `WYPIN`-before-`PINHIGH` order is a real defect — the clock/transition examples as written **never toggle**. **Fix (reorder to enable-then-WYPIN):** Spin2 `generate_clock`, `continuous_square`, `sync_serial_clock`; PASM `gen_transitions`, `continuous`, `sync_clock` (all currently DIRH/PINHIGH after WYPIN). **Sweep:** check sibling trigger-on-Y-write modes (pulse %00100 etc.) for the same pattern — VERIFY before changing.
> **DESIGN DECISION (Stephen, 2026-06-17, pedagogical):** adopt ONE universal smart-pin init order across ALL smart-pin examples (YAML + manual), rather than a per-mode audit: **Reset (`DIRL`) → Setup (`WRPIN`/`WXPIN`) → Enable (`DIRH`) → Operate (`WYPIN`)** — i.e. `WYPIN` always comes AFTER enable. Rationale: "after enable" is the superset — it is *required* by the trigger modes (%00100/%00101, Y held 0 during reset) and *accepted* by every other mode (Silicon Doc 166-168: feed `WXPIN`/`WYPIN` after raising DIR). One teachable rule instead of N special cases. **Before applying set-wide:** ratify the universal order with a representative-mode hardware sweep (a trigger mode + an NCO/continuous mode + a serial mode + an encoder/measurement mode); if clean, apply across the smart-pin set + manual. **Call out** that `pinstart()` (which does `WYPIN` before `DIRH`) is UNSAFE for the trigger modes. This spawns a sibling-sweep verification task and a set-wide example-reorder fix.
> **APPLIED 2026-06-18 (YAML):** `smart-pin-00101-transition-output.yaml` fully corrected — deleted the false `continuous_mode` block (replaced with a correct `y_register.y_zero` note + an `init_order` note carrying the `pinstart()`-unsafe caveat), removed the `continuous_square()` / PASM `continuous` WYPIN-0 examples (redirected to NCO %00110/%00111), and reordered all 4 remaining init sequences to enable→WYPIN. The set-wide sweep also fixed the OTHER broken TRIGGER mode, `smart-pin-00100-pulse-cycle-output.yaml` (6 sites; old WYPIN-before-enable is broken per test60). **DEFERRED → F-139:** the cosmetic value-mode reorders (NCO %00110/%00111, DAC %00010/%00011 — order-insensitive, test61/63 SAFE) and the sync-serial files (%11100, spi-implementation-guide) carry intentional special-cases (NCO quadrature "start together", DAC ADC-feedback PINWRITE, sync-serial double-buffer prime, `.loop` sweeps) needing per-site verification, not a blind swap. async-TX %11110 has no WYPIN-before-enable. YAML format + crossref validated clean.
- **Where:** `deliverables/ai/P2/architecture/smart-pins/smart-pin-00101-transition-output.yaml` — the `continuous_mode` block ("Y=0 generates continuous transitions / No IN flag in continuous mode / Runs until pin disabled"), plus the examples that rely on it: `spin2_complete` → `continuous_square()` (`WYPIN(pin, 0)`), `pasm2_complete` → `continuous` (`WYPIN #0`).
- **What's suspected wrong:** the "Y=0 = continuous" claim has no source and both primary docs frame Y=0 as the **idle/reset/completed** state, not a continuous mode. (Continuous square-wave generation is the NCO modes' job — %00110/%00111.)
- **Evidence:** Silicon Doc v35 `part4-smart-pins.txt` L359-366: *"Whenever Y[31:0] is written with a **non-zero value**, the pin will begin toggling for Y transitions... IN will be raised when the transitions complete... During reset (DIR=0)... Y is set to zero."* (silent on Y=0-while-running). Titus `smart-pins-titus-text.txt` L489: *"Use the Y register... to set the number of transitions... The Y value decrements after each edge... When the Y-register value reaches 0, the IN flag gets set... During reset, ... Y is set to zero."* Neither documents Y=0 = continuous; both imply Y=0 = no toggling.
- **Verification:** on hardware, configure %00101, then write Y=0 to a running pin (and Y=0 from idle) — does the pin emit continuous transitions, or hold/stop? If it stops, correct the YAML (remove the continuous claim; redirect continuous-square guidance to NCO %00110) and re-check the two examples.
- **Origin:** RA-10, `audit/titus-cross-audit-2026-06-12.md`; todo #55.

### F-125 — `CLOSE` per-window directive missing from ALL 9 debug-display YAMLs (+ statements/debug.yaml) — `DONE`
> **DONE 2026-06-14:** Added `CLOSE` to the `display_directives` of all 9 debug-displays YAMLs and a `window_runtime_directives` block in `statements/debug.yaml`, each cross-referencing `constants/debug-end-session.yaml` (CLOSE frees ONE window; `DEBUG(DEBUG_END_SESSION)` ends the whole session). Source: matrix §3 (CLOSE ✅ all 9) + §6 (frees window via external parser); Stephen-confirmed. Compile-verified `` debug(`MyScope CLOSE) ``.
- **Where:** `deliverables/ai/P2/language/spin2/debug-displays/{term,bitmap,plot,logic,scope,scope_xy,fft,spectro,midi}.yaml` (each `display_directives:`), and `statements/debug.yaml`.
- **What's wrong:** none list the universal runtime directive **`CLOSE`** (`` debug(`Name CLOSE) `` — closes that named window). The v55 reconciliation dropped it across the board.
- **Evidence:** v55 primary source shows `| CLOSE | Close the window. |` in the *Feeding* table of every one of the 9 windows (spin2-v55-text.txt lines 1140, 1170, 1195, 1223, 1247, 1295, 1318, 1348, 1393). Confirmed by Stephen.
- **Fix:** add `CLOSE: "CLOSE -- close this named window"` to each window's `display_directives`. Distinguish from `DEBUG(DEBUG_END_SESSION)` (const 27, {Spin2_v52}) which ends the WHOLE session (all windows + DEBUG.LOG) — that one is already documented (`constants/...DebugEndSession`). Consider a cross-ref between them.

### F-126 — `logic.yaml` directive ranges/defaults wrong + a likely-fabricated `DOTSIZE` — `RESOLVED-INVALID`
> **RESOLVED-INVALID 2026-06-14:** The current `logic.yaml` already matches the Pascal-audited matrix §7.3 (SAMPLES 4..2047, SPACING 1..32, LINESIZE 1..32 def 3, **DOTSIZE present 0..32**). The original finding was derived from the v55 published text, which is wrong here. No edit. DOTSIZE is a real LOGIC directive (matrix §2 row + §7.3) — KEPT.
- **Where:** `deliverables/ai/P2/language/spin2/debug-displays/logic.yaml`.
- **What's wrong (vs v55 primary, spin2-v55-text.txt lines 1124–1133):**
  - `LINESIZE` — YAML says `1..32 (default 3)`; primary: **`1_to_7`, default 1** (line 1127).
  - `SPACING` — YAML says `1..32`; primary: **`2_to_32`** (line 1125).
  - `SAMPLES` — YAML says `4..2047`; primary: **`4_to_2048`** (line 1124).
  - `DOTSIZE` — YAML lists a `DOTSIZE` for LOGIC; the v55 LOGIC instantiation table has **NO DOTSIZE** (lines 1121–1133). Verify against `DebugDisplayUnit.pas`; if absent there too, remove it.
- **Fix:** correct the three ranges; verify/remove DOTSIZE. (LOGIC supports 1..32 channels — primary line 1107/1118 — confirm the channel grammar conveys this.)

### F-127 — `scope_xy.yaml` SIZE default + SAMPLES/RATE ranges wrong — `DONE (SIZE) / RESOLVED-INVALID (ranges)`
> **DONE 2026-06-14 (SIZE):** Fixed the `SIZE` directive note — it said "default 256 -> 512 px", implying a 512 px default window. Per matrix fn.1 the default window is **256×256 px** (vWidth=256; `SIZE n` → width=height=`n*2` clamped 32..2048). Reworded accordingly.
> **RESOLVED-INVALID 2026-06-14 (ranges):** `SAMPLES 0..2048` and `RATE 1..2048` already match matrix §7.3; the v55-text-derived "0..512 / 1..512" was wrong. No change to those.
- **Where:** `deliverables/ai/P2/language/spin2/debug-displays/scope_xy.yaml`.
- **What's wrong (vs v55 primary, spin2-v55-text.txt lines 1179–1183):**
  - `SIZE` — YAML says "default 256 -> 512px"; primary: **`SIZE radius`, default 128** (radius, so the window is 2*radius = 256 px). The manual (table default 128) was RIGHT; the YAML is wrong.
  - `SAMPLES` — YAML says `0..2048`; primary: **`0_to_512`**, default 256 (persistence; 0 = infinite).
  - `RATE` — YAML says `1..2048`; primary: **`1_to_512`**.
- **Fix:** correct SIZE default semantics (radius, default 128) and the SAMPLES/RATE upper bounds (512).

### F-128 — `term.yaml` default color pairs say LIME; v55 says GREEN — `RESOLVED-INVALID`
> **RESOLVED-INVALID 2026-06-14:** The default genuinely IS LIME. Matrix §7.3 spells out `DefaultTermColors` (242) = `ORANGE/BLACK, BLACK/ORANGE, LIME/BLACK, BLACK/LIME` (each pair followed by its reverse) — `term.yaml` matches this exactly. `clLime` = $00FF00 is the actual source constant; the named directive `GREEN` resolves to a *different* value ($09FF09), so "GREEN" (from the v55 published text) would have been wrong. No edit.
- **Where:** `deliverables/ai/P2/language/spin2/debug-displays/term.yaml` (`COLOR` default note).
- **What's wrong:** YAML default pairs read "ORANGE/BLACK, BLACK/ORANGE, **LIME/BLACK, BLACK/LIME**". "LIME" is not a P2 DEBUG named color. v55 primary (line 1306): pairs are **0=ORANGE/BLACK, 1=BLACK/ORANGE, 2=GREEN/BLACK, 3=BLACK/GREEN**.
- **Fix:** replace LIME with GREEN in the default-pair description. (The manual inherited this error — see manual fix list.)

### F-129 — `scope.yaml` TRIGGER AUTO formula + minor defaults could be enriched/corrected — `RESOLVED-INVALID`
> **RESOLVED-INVALID 2026-06-14:** SCOPE `SIZE` default is `256×256` (matrix §7.3) — `scope.yaml` already matches; the v55-text "255,256" was wrong. `LINESIZE 0..32 def 3` matches the matrix, which carries NO "half-pixel" wording, and the TRIGGER AUTO 33%/50% figure is not in the Pascal-audited matrix — both were v55-text-only enrichments, not applied. No edit.
- **Where:** `deliverables/ai/P2/language/spin2/debug-displays/scope.yaml`.
- **What's wrong (vs v55 primary, spin2-v55-text.txt lines 1152–1165):**
  - TRIGGER `AUTO` — YAML says only "auto-computes levels"; primary documents the formula: **AUTO = 33% arm level, 50% trigger level** (line 1165). (This VALIDATES the manual's "low+range/3, low+range/2" — the manual was right.)
  - `SIZE` default — YAML `256x256`; primary **`255, 256`** (line 1152). LINESIZE is "in half-pixels" (line 1156) — worth noting.
- **Fix:** add the AUTO 33%/50% formula; align SIZE default; note half-pixel LINESIZE.

### F-130 — `debug-commands/.../statements/debug.yaml` legacy top half contradicts the v55 window YAMLs — `DONE`
> **DONE 2026-06-14:** Reconciled the legacy (v51) top half. Fixes: (a) `control_characters` code-12 "form feed (clear screen)" → corrected (code 12 does NOTHING; clear is code 0 / CLEAR); (b) usage note "Backtick syntax required - regular quotes won't work" softened (plain `DEBUG("text", value)` needs no backtick). **Evidence-widening:** the malformed `` DEBUG(`…`) `` double-backtick pattern was systemic — fixed it across ALL of the `syntax` block, the 9 `display_types` usage strings, and every `examples` entry (plain → `DEBUG("text", …)`; display → create + named-window `` `(…) `` feed). The "real-time plotting" example used PLOT (a drawing canvas, not a series plotter) → switched to SCOPE. All examples compile-verified with `pnut-ts -d`. See also F-134 (fabricated formatters in the same file, found during this rewrite).
- **Where:** `deliverables/ai/P2/language/spin2/statements/debug.yaml` (the pre-`string_quoting` legacy content; `documentation_source: Spin2 v51`).
- **What's wrong:**
  - `control_characters:` lists **"12 - Form feed (clear screen)"** — contradicts `term.yaml` (code 12 does NOTHING; 14..31 fall through). Clearing is code 0 / CLEAR.
  - `examples:` use malformed trailing-backtick syntax `` DEBUG(`"Hello World", 13`) `` and `` DEBUG(`SCOPE MyScope, ...`) `` — the backtick opens display mode and the statement ends at `)`; there is no closing backtick.
  - `usage_notes:` "Backtick syntax required - regular quotes won't work" is misleading (plain `DEBUG("text")` is valid for the default TERM).
- **Fix:** reconcile the legacy top half with the v55 reconciliation (fix code-12, fix the example syntax, soften the usage note). The high-quality `string_quoting` block added later is correct; the legacy scaffolding around it is stale.

### F-131 — `plot.yaml` SPRITEDEF over-states a fixed "256 RGBA color longs" — `DONE`
> **DONE 2026-06-14:** Confirmed by the actual Pascal code (PLOT ToO §10.2, lines 2090-2101): the palette loop is `for i := 0 to 255 do if not KeyVal(...) then Break` — it reads **up to** 256 colors and **stops at end-of-message**, so fewer-than-256 is valid (pixels reference only the indices you supply). The YAML's "then 256 RGBA color longs" overstated a hard 256 requirement; reworded to "the palette colors the pixel bytes reference (… up to 256 …)". The 2-color SPRITEDEF example is correct (Break confirms) — kept, with its comment clarified. Compile-verified.

### F-132 — `scope_xy.yaml` POLAR conflates twopi `-1` and `0` — `DONE`
> **DONE 2026-06-14:** Found during the F-127 re-investigation. The YAML said `twopi -1/0 => $100000000`, treating −1 and 0 as equivalent. Matrix §7.3 (SCOPE_XY) + ToO `KeyTwoPi`: **`0 ⇒ +$100000000`** (positive/counter-clockwise winding), **`-1 ⇒ −$100000000`** (reversed/clockwise winding) — they are NOT equivalent; any other value is literal (e.g. 360 = degrees). Reworded. Affects writing debug statements (a `POLAR -1` author would get reversed theta). Compile-verified `POLAR 0 / -1 / 4096`.

### F-133 — `plot.yaml` LUTCOLORS says "256 longs"; should be "up to 256" — `DONE`
> **DONE 2026-06-14:** Found during the F-131 re-investigation. Matrix §7.3 (PLOT) says LUTCOLORS is "up to 256 rgb24"; `bitmap.yaml` already says "up to 256". `plot.yaml` said "256 longs" in two places (config + update) — implies a mandatory 256. Reworded both to "up to 256 … as many as the LUT mode uses".

### F-134 — `statements/debug.yaml` fabricates DEBUG formatters DEC/HEX/BIN/STR/DLONG/DWORD/DBYTE — `DONE`
> **DONE 2026-06-14:** Found while compile-verifying the F-130 example rewrite. The legacy file's `formatting_functions` listed `DEC/HEX/BIN` (numeric), `STR` (string), and `DLONG/DWORD/DBYTE` (special) — **none of these compile** (`pnut-ts -d` rejects them). The real formatters are the U/S-prefixed forms only (`UDEC/SDEC`, `UHEX/SHEX`, `UBIN/SBIN`, `FDEC`; `ZSTR/LSTR`; size `_BYTE/_WORD/_LONG`; value-only `_`; `_ARRAY`) per `debug-commands/debug-formatters-overview.yaml` (now cross-referenced). Rewrote the section to the verified set and dropped the fabrications. The rewritten F-130 examples also switched `DEC(x)` → value-only `udec_(x)` etc. (correct idiom when an explicit text label is supplied). All compile-verified.
- **Where:** `deliverables/ai/P2/language/spin2/debug-displays/plot.yaml` (`SPRITEDEF` directive).
- **What's wrong:** YAML says SPRITEDEF takes "then **256** RGBA color longs", implying the palette must always be 256 entries. It does NOT — you supply the palette entries the pixel bytes reference.
- **Evidence:** v55 primary (spin2-v55-text.txt L1288): "Colors are longs which define the palette **referenced by the pixel bytes**." Compile-verified: a 2-color SPRITEDEF (`SPRITEDEF 0 2 2 0 1 1 0 $00000000 $FFFF0000`) compiles clean under `pnut-ts -d`. The manual's 2-color sprite examples are correct.
- **Fix:** reword to "then the palette colors referenced by the pixel bytes (RGBA `$AARRGGBB` longs; up to 256)" — drop the implication that exactly 256 are required.

## Assembly-manual release-gate audit batch (2026-06-24) — F-163…F-164

> **Origin:** surfaced by the `p2-assembly-language-manual` release-gate audit
> (`engineering/document-production/manuals/p2-assembly-language-manual/opus-master/audit/release-gate-2026-06-24.md`,
> findings G-01 and C-01). Both are fabricated content in the P2KB YAML; authority = the P2 Silicon Doc
> + `pnut-ts` (no-flag/instruction-existence). No inference.

### F-163 — `language/pasm2/getbrk.yaml` carries FABRICATED flag semantics in `description` + `examples` — `DONE`
> **APPLIED 2026-06-24:** `deliverables/ai/P2/language/pasm2/getbrk.yaml` — rewrote the `description` to the real flag semantics and replaced the three wrong examples. **Source:** Silicon Doc `engineering/ingestion/sources/silicon-doc/part3-interrupts.txt:404-490`. The file claimed GETBRK had a no-flag form returning "16-bit skip pattern", and that WCZ=32-bit ISR call address, WC=8-bit COG ID, WZ=8-bit breakpoint code — **all fabricated**. Truth: GETBRK REQUIRES a flag effect (no-flag form does not assemble — `pnut-ts`: "Expected WC, WZ, or WCZ"). **WCZ** (normal exec) → C=STALLI/ALLOWI, Z=hubexec/cogexec start, D=cog internal status (D[22] colorspace, D[21] streamer, D[20] WRFAST/RDFAST, D[19:16]/[15:12]/[11:08] INT3/2/1 selectors, D[07:06]/[05:04]/[03:02] INT3/2/1 state, D[01] STALLI, D[00] hubexec); in a **debug ISR** additionally D[31:24]=8-bit break code from the last BRK and C/D[23]=COGINIT (re)start. **WC** → C=LSB of SKIP/SKIPF/EXECF/XBYTE pattern, D[31:28]=CALL depth, D[27] SKIP-vs-SKIPF/EXECF/XBYTE, D[26] LUT sharing, D[25] XBYTE pending, D[24:16] XBYTE mode, D[15:00]=16 event-trap flags. **WZ** → Z=1 if no pattern queued (D=0)/queued if D<>0, D=full 32-bit SKIP/SKIPF/EXECF/XBYTE pattern (LSB-first). All four replacement examples compile-verified with `pnut-ts`. `related_instructions` left intact (BRK, COGBRK, NIXINT1/2/3 all exist; no SETBRK invented). Verified: parse + crossref clean.

### F-164 — `language/pasm2/concepts/special_registers.yaml` cites a non-existent GETPC instruction — `DONE`
> **APPLIED 2026-06-24:** `deliverables/ai/P2/language/pasm2/concepts/special_registers.yaml` (PC register `access`, ~L15) — replaced `Read via GETPC, modified by jumps/calls` with `No direct read instruction; captured as the return address saved by CALLD/CALL/CALLPA/CALLPB; modified by jumps/calls`. **Source:** `pnut-ts` rejects `getpc` ("Expected … assembly instruction"); there is no `getpc.yaml` and GETPC is absent from the instruction CSV. The PC has no dedicated read instruction; its value is captured implicitly as the return address a call saves. Verified idiom `calld reg, #$+1` then `and reg, ##$FFFFF` compiles and captures the 20-bit PC. Verified: parse + crossref clean.

### F-165 — signed-flag family C-flag wording: "correct sign" standardized to "true sign" + `adds.yaml`/`subs.yaml` "bit 31" gloss tightened — `DONE`
> **APPLIED 2026-06-25 (Assembly-manual release-gate follow-on).** Standardized the signed add/subtract/compare/sum family C-flag wording from "correct sign" to **"true sign"** (the manual's Chapter-3 lead term; also more arresting to readers) across `adds.yaml subs.yaml cmps.yaml cmpsx.yaml sumc.yaml sumnc.yaml sumz.yaml sumnz.yaml tjv.yaml`. Additionally tightened `adds.yaml`/`subs.yaml`, whose C field glossed the value as "i.e. bit 31 of the result" — imprecise for a single overflowing op (the truncated bit 31 is the wrong sign on overflow) — to **"the sign of (D ± S) at full precision (overflow-corrected)"**, matching the manual's audit-verified Chapter-3 definition and the family convention (CMPS = "true sign of A−B"). The core fact (C is the result's SIGN, **not** a signed-overflow indicator) was already correct; this is a terminology + precision alignment. **Note:** the exact single-instruction-overflow behavior (bit 31 vs overflow-corrected) rests on the documentary Chapter-3/Silicon framing; a hardware confirmation could make it empirical if desired. Verified: `validate-yaml-syntax` + `validate-crossref-keys` clean.
> **HARDWARE-VERIFIED 2026-07-04 (🏆, ledger EF-018):** `test71-signed-cflag-truesign` ran six deliberately-overflowing ADDS/SUBS/CMPS cases (where the stored result's bit 31 disagrees with the true sign). Measured C = `0,1,0,1,1,0` — every case the **overflow-corrected true sign**, opposite the bit-31 value. The documentary wording is now empirical; C is confirmed NOT bit-31 and NOT a signed-overflow flag.

---

## DeSilva-tutorial release-gate audit batch (2026-06-25) — F-166…F-169

> **Origin:** surfaced by the `p2-pasm-desilva-style` v3.0.1 release-gate audit
> (`engineering/document-production/manuals/p2-pasm-desilva-style/audit/release-gate-2026-06-25.md`).
> All three are manual-right / KB-wrong (or KB-incomplete); authority = the P2 Silicon Doc, the
> per-instruction YAML, and `pnut-ts` v1.55 (version-gate probe). No inference.

### F-166 — `architecture/cordic.yaml` `rotate.setup` has the QROTATE operands reversed — `DONE`
> **APPLIED 2026-06-25:** `deliverables/ai/P2/architecture/cordic.yaml` `rotate` — the setup read `SETQ angle / QROTATE X,Y`, implying SETQ holds the angle and QROTATE takes X,Y. **Truth** (`language/pasm2/qrotate.yaml` + Silicon Doc "Rotate (X32,Y32) by Theta32"): **X from the D operand, Y from the SETQ value (0 if SETQ omitted), angle from the S operand**. Corrected to `SETQ Y / QROTATE X, angle` + added an explicit `operands:` line + GETQX/GETQY retrieval note. The DeSilva manual (Ch7 §2222-2229) was already correct. Authority: `qrotate.yaml` description/encoding + Silicon `p2-documentation.txt`. No inference.
> **FOLLOW-ON (same v1.11.2 release):** a publish-time content probe caught that the first fix was **not data-set-wide** — the identical reversed pattern (`SETQ angle / QROTATE x, y`) survived in the **same file** under `programming_patterns.rotation_matrix`, and in `language/pasm2/pi.yaml`'s example. Both corrected to the authoritative operand order (`SETQ y_coord / QROTATE x_coord, angle`). `pi.yaml`'s deeper example defects are tracked separately under **F-169**. Lesson: sweep **every** occurrence in the data set, not just the one the manual audit cited.

### F-167 — `architecture/hub.yaml` `coginit.load_size` says 496 longs; COGINIT loads 504 — `DONE`
> **APPLIED 2026-06-25:** `deliverables/ai/P2/architecture/hub.yaml` `hub_operations.coginit.load_size` — `496 longs` → `504 longs ($000..$1F7)`. **Source:** Silicon Doc verbatim "The target cog loads its own registers **$000..$1F7** from the hub" (`p2-documentation.txt:764`); `$000-$1F7` = 504 longs. 496 is the **general-purpose** register count (`$000-$1EF`), a different fact (Silicon "RAM registers $000 through $1EF are general-purpose"). The DeSilva manual (Ch1 §473) was already correct. No inference.

### F-168 — `language/spin2/methods/lstring.yaml` omits the `{Spin2_v43}` version gate — `DONE`
> **APPLIED 2026-06-25:** `deliverables/ai/P2/language/spin2/methods/lstring.yaml` — added `requires_version: "Spin2_v43"` + `version_directive: "{Spin2_v43}"` (mirroring `methods/taskcont.yaml`) + a notes line. **KB was incomplete, not wrong** — LSTRING is valid but namespace-gated. Proven with `pnut-ts -d` v1.55: `debug(lstring("Status"))` and `addr := lstring("Command")` **fail without** a `{Spin2_v##}≥43` directive ("Expected an expression term") and **compile clean with** `{Spin2_v43}`. Authority: Spin2 v55 keyword-gating table ("v43 | LSTRING | Method | {Spin2_v43}"; introduced v42, gated v43). This corrected the audit's initial "compiler/KB discrepancy" suspicion — there is no discrepancy; the example just needs the gate. (Companion manual fix: the DeSilva Ch examples gain the gate + `BYTE()`/`LONG()` paren-constructor + `lookup`→non-keyword rename — handled in the manual, not here.)

### F-169 — `language/pasm2/pi.yaml` examples misuse the IEEE-754 float PI as a CORDIC integer angle — `DONE`
> **APPLIED 2026-06-25 (folded into v1.11.2):** surfaced while sweeping F-166 data-set-wide. `pi.yaml`'s two examples applied **integer** CORDIC/shift ops to the **float** bit-pattern of PI (`$40490FDB`): `shr angle,#1` presented as float-divide-by-2, `qrotate`/`qmul`/`qdiv` fed the float pattern as if it were a binary angle, and the operands were reversed (`qrotate angle, radius`). A notes line also claimed "full circle = `$80000000` (2^31)" — wrong: per `qrotate.yaml` `angle_format`, `$40000000`=90°, `$80000000`=**180°** (PI), and a full circle (2·PI) is `$1_0000_0000` (2^32, wraps to 0). **Fix:** replaced both examples with compile-verified (`pnut-ts` v1.55) correct ones — (1) `mov fnum, ##PI` to load the float for floating-point math, (2) a CORDIC rotation using a **binary** angle `##$4000_0000` (PI/2) with the correct `SETQ y / QROTATE x, angle / GETQX / GETQY` shape — and corrected the note to the authoritative binary-angle scale. The float PI constant value itself (`$40490FDB`) was already correct. Authority: `qrotate.yaml` `angle_format`/encoding + `pnut-ts` compile. No inference.

---

## Smart-pin ADC X[5:4] encoding root-cause guard (2026-06-28) — F-170

> **Origin:** surfaced by the Smart-Pin ADC Foundation sprint
> (`engineering/planning/SMART-PIN-ADC-FOUNDATION-AND-P2AN001-SPRINT-PLAN.md` §1/§3) while
> studying Chip Gracey's "Improved ADC Pin Techniques" thread. Authority = Silicon Doc v35
> (`engineering/ingestion/sources/silicon-doc/part4-smart-pins.txt:816,820-821`), confirmed
> identical in Spin2 v55. No inference.

### F-170 — ADC mode %11000 X[5:4] sub-mode encoding fixed at its ROOT (ingestion donor) + made un-regressable — `DONE`
> **Canonical encoding (locked).** `WXPIN` sets the sample/filter mode to **X[5:4]** and the
> sample period to **POWER(2, X[3:0])** (`part4-smart-pins.txt:816`). The four-row map
> (`:820-821`): **%00 = SINC2 Sampling · %01 = SINC2 Filtering · %10 = SINC3 Filtering ·
> %11 = Bitstream capturing.**
>
> **Root-cause narrative.** The X[5:4] map was inverted ("%00 = Raw bitstream capture",
> "%11 = Reserved/unused") for ~6.5 months because the encoding was on **no** verification
> checklist. Git forensics: the bug was **born** when a mis-authored donor was imported at
> `e271cab0` (2025-11-29); it **survived** the v1.6.3 "aligned to silicon" pass (`b0f48a88`,
> which only touched gain constants); it was **fixed in the published file only** at `35344af8`
> (v1.9.0, 2026-06-13) — but the **upstream ingestion donor was never corrected**, so any
> "regenerate from catalog" would have re-seeded the inversion downstream (the known donor
> re-seed trap). A stale 2026-06-12 IOSP Titus cross-audit note (true that day, fixed the next)
> is what made this sprint suspect the *published* YAML was still broken — it was not.
>
> **DONE 2026-06-28 (sprint §1+§3).**
> (a) **Donor fixed** (`engineering/ingestion/smart-pins-catalog/ingestionSources/mode-11000-adc-internal-clock/smart-pin-11000-adc-internal-clock-concise.yaml`):
> `bits_5_4`, `x_register_modes`, the `operation`/`timing`/`notes` prose, and the mislabeled
> code-example comments all aligned to the silicon map (and `P[12:10]`→`M[12:10]` per silicon).
> (b) **Published verify-locked:** `smart-pin-11000`/`11001` already silicon-correct (v1.9.0)
> and now match the donor on all four rows; `smart-pin-11010` defers its X-config to the
> siblings (uses `P_ADC_SCOPE`) and had one `P[12:10]`→`M[12:10]` note aligned.
> (c) **Durable guard added:** `engineering/tools/validation/audit-adc-encoding.py` asserts the
> four-row map is identical across the donor, the three published ADC YAMLs, and the Silicon
> Doc ground-truth string; non-zero exit on any drift, clean error (no false pass) on malformed
> YAML. Recurrence-tested: reverting the donor's %00 to the old "Raw bitstream" wording makes
> the guard FAIL (proves it guards the real bug path). The central `release-yamls` pre-publish
> hook for this guard is logged as a skill-evolution candidate (not a central-skill edit).
> Verify: `verify-yaml-format.py` 1053/1053 clean, `validate-crossref-keys.py` all resolved.

---

## CORDIC ops-in-flight count — `architecture/cordic.yaml` overstates "7-8"; Silicon Doc says "several" (2026-06-30) — F-171

> **Origin:** surfaced while authoring **P2AN002 "CORDIC for Real Work"** (app note),
> sourcing the pipeline/throughput facts. Authority = **Silicon Doc v35**
> (`engineering/ingestion/sources/silicon-doc/part3-end.txt:346-352`) + the **P2 Datasheet**
> (`engineering/ingestion/sources/p2-datasheet/p2-datasheet-narrative.txt:1424`). The note
> itself is trust-chain-clean regardless of how this resolves — it cites only the two
> sourced hard facts (54-stage pipeline, 8-clock hub slot) and mirrors the Silicon Doc's
> "several" framing rather than any hard in-flight number.

### F-171 — two published YAMLs disagree on per-cog CORDIC ops-in-flight (7-8 vs 6-7); the count is DERIVED, not spec'd, and "7-8" is unreachable — `DONE`
> **What's wrong.** `deliverables/ai/P2/architecture/cordic.yaml` asserts **"7-8" operations
> in flight per cog** in three places — `description` ("enabling up to 7-8 operations in
> flight per COG", line ~9), `architecture.ops_in_flight_per_cog: "7-8 maximum"` (line ~26),
> and `critical_usage_pattern.fill_phase: "Submit 7-8 ops before expecting results"` (line
> ~24). The sibling `deliverables/ai/P2/language/pasm2/concepts/cordic_solver.yaml` says
> **`max_in_flight: 6-7 operations per COG (54 / 8)`** (line ~19). They disagree, and **"7-8"
> is not reachable**: 54 ÷ 8 = 6.75 and 55 ÷ 8 = 6.875 — at most ~7 commands can be issued
> before the first result returns.
>
> **Evidence (sourced, verbatim).** Silicon Doc v35: *"Fifty-five clocks later, results will
> be available via the GETQX and GETQY instructions… Because each cog's hub slot comes around
> every 1/2/4/8/16 clocks (8 clocks for the current P2X8C4M64P…) and the pipeline is 54 clocks
> long, it is possible to overlap CORDIC commands, where **several** commands are initially
> given to the CORDIC solver, and then results are read and another command is given,
> indefinitely…"* (`part3-end.txt:346-352`). P2 Datasheet: *"achieving up to one CORDIC result
> every eight clocks"* (`p2-datasheet-narrative.txt:1424`). **Neither source states a hard
> in-flight count** — the Silicon Doc says "several." Per this register's "No inference or
> derivation" rule, both "7-8" and "6-7" are *derived*; the sibling at least shows its
> derivation (`54 / 8`) and rounds correctly, while "7-8" rounds **up past what the math
> allows**.
>
> **Proposed correction (→ yaml-knowledge-base-maintenance head).** Align
> `architecture/cordic.yaml`'s three "7-8" occurrences to the sibling's framing — "**up to
> ~6-7** (54-stage pipeline ÷ 8-clock hub slot)" — and present it explicitly as **derived**
> from the two sourced hard facts, mirroring the Silicon Doc's "several." Do **not** assert
> "8" (unreachable). No edit beyond the transparent `54 / 8` derivation already carried by the
> sibling YAML; match the Silicon Doc's wording.
>
> **APPLIED (yaml head) 2026-06-30:** aligned all three "7-8" occurrences in
> `architecture/cordic.yaml` (`description`, `architecture.ops_in_flight_per_cog`,
> `critical_usage_pattern.fill_phase`) to "up to ~6-7", each shown as DERIVED from the
> transparent `54 / 8` (54-stage pipeline / 8-clock hub slot) and mirroring the Silicon
> Doc's "several"; no "8" asserted. Sibling `language/pasm2/concepts/cordic_solver.yaml`
> already carried `6-7 (54/8)` and is unchanged.

---

## Spin2 CORDIC concept YAML documents non-compiling built-in signatures (2026-06-30) — F-172

> **Origin:** surfaced while authoring **P2AN002 "CORDIC for Real Work"**, compile-verifying
> the Spin2 recipe code. Authority = **`pnut_ts` v1.55 compiler** (ground truth, top of this
> register's authority order) + the **sibling per-method YAMLs** (which are already correct).

### F-172 — `language/spin2/concepts/cordic_solver.yaml` documents `@pointer`-out and 2-arg CORDIC signatures that **do not compile**; per-method YAMLs are correct — `DONE`
> **What's wrong.** The concept overview YAML's `available_methods` (and the
> `common_patterns` block) document the coordinate-transform built-ins in the **`@pointer`-out
> statement form** — `ROTXY(@x, @y, angle)`, `POLXY(@x, @y, angle, length)`,
> `XYPOL(@length, @angle, x, y)` — and `QSIN`/`QCOS` in a **2-argument form**
> `QSIN(angle, length)`. **None of these compile** under `pnut_ts` v1.55:
> - `ROTXY(@x, @y, angle)` → `error: This instruction can only be used as an expression term,
>   since it returns results`
> - `QSIN($4000_0000, 1000)` → `error: Expected ","`
>
> The CORDIC built-ins are **multi-return functions**, not in-place `@pointer` mutators.
>
> **Evidence (sourced).** `pnut_ts` v1.55 compiles the multi-return forms cleanly; the
> **sibling per-method YAMLs already document them correctly**:
> `rotxy.yaml` → `X2, Y2 := ROTXY(X, Y, Angle)`; `polxy.yaml` → `X, Y := POLXY(Rho, Theta)`;
> `xypol.yaml` → `Rho, Theta := XYPOL(X, Y)`; `qsin.yaml` → `y := QSIN(length, step,
> stepsInCircle)`; `qcos.yaml` → `x := QCOS(length, step, stepsInCircle)`. So the defect is
> **isolated to the concept overview file** — the method files are the correct authority.
>
> **Proposed correction (→ yaml-knowledge-base-maintenance head).** Rewrite
> `spin2/concepts/cordic_solver.yaml`'s `available_methods` syntax + examples and the
> `common_patterns` (`distance_calculation`, `angle_calculation` use `XYPOL(@..)`) to the
> multi-return forms the compiler accepts and the per-method YAMLs already carry. Re-derive
> the worked example values against the corrected forms. Authority: `pnut_ts` compile + the
> sibling method YAMLs.
>
> **APPLIED (yaml head) 2026-06-30:** rewrote `available_methods` (QSIN/QCOS to
> `(length, step, stepsInCircle)`; ROTXY/POLXY/XYPOL to multi-return) and the four
> `common_patterns` (`sine_wave_generation`, `circular_motion`, `distance_calculation`,
> `angle_calculation`) to the forms the per-method YAMLs carry, re-deriving the worked
> example values. Every corrected form was compile-verified together under `pnut-ts -d`
> v1.55.0 (clean).

---

## ADC reference is local to the pin's 4-pin power domain — undocumented (2026-06-30) — F-173

> **Origin:** surfaced by Stephen while reviewing the P2AN001 ADC app note — the isolated
> 4-pin power grouping that governs which pins a multi-pin ADC measurement may share.
> Authority = **P2 Datasheet** (pin descriptions / "Power and Analog Considerations") +
> **Silicon Doc v35** (pin table) + our ingestion walkthrough-audit.

### F-173 — the 4-pin VIO/GIO power-domain grouping and per-group ADC reference were undocumented (IOSP Ch.16 + app note + YAML) — `DONE`
> **The fact.** The P2 powers its I/O pins in **isolated groups of four** — pins 0–3, 4–7,
> 8–11, …, 60–63 — each group sharing one **VIO/GIO** supply pair (an isolated supply
> domain). A pin's ADC, when set to `P_ADC_GIO` / `P_ADC_VIO`, references **its own group's**
> ground/supply rails. This is *why* the single-pin ratiometric measurement is absolute, and
> it constrains multi-pin layouts: pins tied to a shared node for one measurement must sit
> **within a single group** to share a reference domain (straddling a boundary mixes domains
> and degrades the result).
>
> **Evidence (sourced).** P2 Datasheet: *"Power for smart pins in groups of 4: Pxx through
> Pyy"*, *"Groups of 4 pins share supply for isolated domains"*, *"ADC can sample own group's
> supply for calibration"* (`engineering/ingestion/sources/p2-datasheet/p2-datasheet-narrative.txt:528`
> + `…/p2-datasheet-diagram-narratives.md:94-96`). Silicon Doc v35 pin table:
> `VIO_{x}_{y}`/`GIO_{x}_{y}` = power/ground for smart pins {x} through {y}. Boundary alignment
> (0–3, 4–7, …) per `engineering/ingestion/sources/silicon-doc/silicon-doc-v35-walkthrough-audit.md:34-39`.
>
> **Where it was missing.** Not in **IOSP Ch.16** (only the `P_ADC_GIO`/`P_ADC_VIO` constants,
> never the domain mechanism); not in **P2AN001**; not in the **published YAML**.
>
> **Applied 2026-06-30.** (1) **IOSP Ch.16 enriched** (owns the mechanism): §16.3 Ratiometric
> — a "references are local to the pin's power group" paragraph; §16.6 Multi-Channel — a
> power-domain-layout note. (2) **P2AN001 app note** — a 🔧 Hardware note (Pitfalls) + a
> How-It-Works mention + a Recipe 2 pin-selection line citing the mechanism.
> **APPLIED (yaml head) 2026-06-30:** stood up a standalone reference
> `architecture/pin-power-domains.yaml` (`p2kbArchPinPowerDomains`) — the isolated 4-pin
> VIO/GIO grouping, the per-group `P_ADC_GIO`/`P_ADC_VIO` reference, and the shared-node
> multi-pin constraint, sourced to durable P2 Datasheet + Silicon Doc v35 wording (no
> internal paths), with aliases + `io_architecture` category registration. Added a
> `power_domain` block + `related`/`see_also` pointing to it in all three ADC mode YAMLs
> (`smart-pin-11000`/`11001`/`11010`); also fixed a pre-existing `adc_pin`->`adc_base`
> compile bug in 11000's multi-channel example while in that file.

---

## USB mode %11011 code examples omit P_OE — won't drive the bus (2026-06-30) — F-174

> **Origin:** surfaced by the IOSP Release Campaign §1a USB boundary-mining pass
> (`mine-and-delineate` fan-out). Hand-verified against two independent OBEX USB drivers
> (host #4198 USBnew / Wuerfel_21, device #4727 / Chris Gadd), IOSP Ch.19, and the WRPIN
> encoding. Distinct from **G-004** (which enriched the X/Y/Z register *documentation* in
> the same file); this is a defect in the file's *code examples*.

### F-174 — `architecture/smart-pins/smart-pin-11011-usb-host-device.yaml` code examples set the USB mode **without `P_OE`**, so as written they never drive the bus — `DONE (2026-07-01)`
> **APPLIED 2026-07-01.** Both active-port examples now use `P_USB_PAIR | P_OE` — Spin2 `pinstart(usb_dm…, P_USB_PAIR | P_OE, …)` (2 sites) + PASM `usb_mode long P_USB_PAIR | P_OE` (symbolic, per the show-code-constants convention). Verified vs `wrpin.yaml` (`P_OE`=$40=bit 6), OBEX #4198 `USB_V2_DRVOUT`/#4727, IOSP Ch.19 output-control table, and `pnut-ts` compile. **Donor fixed too** (`…/mode-11011-usb-host-device/smart-pin-11011-usb-host-device-concise.yaml`, 3 sites) so a regenerate stays reseed-safe. Evidence-scoped: defect isolated to this one file — every other `%..._00_11011_0` is the correct bare `P_USB_PAIR` constant definition, left untouched.
> **The defect.** Every code example in the file configures the USB pair with the bare mode
> and no output-enable bit:
> - PASM `code_examples[0]`: `usb_mode long %0000_0000_000_000000_0000000_00_11011_0` —
>   bits[7:6]=`00`, so **bit 6 (`P_OE`=$40) is clear**. The pin pair is configured but the
>   driver is disabled, so it cannot drive D+/D− (this is the *sniffer/monitor* configuration,
>   `%0_11011_0`, not an active port).
> - Spin2 `code_examples[0]` and `[1]`: `pinstart(usb_dm…, P_USB_PAIR, …)` — `P_OE` is not
>   OR'd into the mode argument either.
>
> **Why it's wrong.** An active USB host or device must drive the bus. Both real-world drivers
> and IOSP Ch.19 (§19.2/§19.7/§19.10) configure an active port as **`P_USB_PAIR | P_OE`**
> (`%1_11011_0`); output drive is disabled only for a passive sniffer. As written, none of the
> examples would communicate.
>
> **Evidence (sourced, no inference).** WRPIN D-field `…_TT_MMMMM_0`: mode `M=%11011` at
> bits[5:1]; `P_OE` is bit 6 (`$40`) — clear in the example. IOSP Ch.19 "Output Control" table:
> `%1_11011_0` = output enabled, `%0_11011_0` = sniffer. OBEX #4198 `USB_V2_DRVOUT` and #4727
> `mode` both set `P_USB_PAIR | P_OE` for the active port. `pinstart` passes its mode argument
> straight to WRPIN, so the Spin2 calls inherit the same omission.
>
> **Proposed correction (for `yaml-knowledge-base-maintenance`).** In the active-port examples,
> set output enable: PASM `usb_mode long P_USB_PAIR | P_OE` (or the explicit
> `%0000_0000_000_000000_0000000_01_11011_0`), and Spin2 `pinstart(usb_dm…, P_USB_PAIR | P_OE,
> …)`. If an example is genuinely intended as a passive bus sniffer, **label it as such** and
> keep `P_OE` clear deliberately (with a comment) — but `code_examples[0]` "USB Pin Pair
> Configuration" is plainly an active port and must enable output.
>
> **⚠️ Donor-reseed caveat (`reference_p2kb_yaml_donor_reseed`).** This is a *published*
> deliverable YAML; per the known donor-reseed trap it was likely seeded from an ingestion
> "concise donor". Fixing only the published copy will be re-overwritten on regenerate — locate
> and fix the **donor** too, then verify donor == published == any sibling == source.
>
> **Drain-gate note.** This is an actionable YAML correction. The IOSP Release Campaign §4
> release-depth re-audit requires the corrections-register drain gate to be GREEN, so **F-174
> must be resolved before IOSP releases.**

---

## Smart-pin example defects surfaced during app-note authoring (2026-06-30) — F-175…F-176

> **Origin:** surfaced while authoring P2AN003 (DAC) and P2AN004 (measurement) app notes
> against the KB — the drafting agents hit two published smart-pin `code_examples` that do not
> compile / cannot work as written, and used the KB-validated idiom instead (no note shipped the
> broken code). Both are **set-wide** (span multiple mode YAMLs). Verified against `pnut-ts` v1.55
> and the `pinread.yaml` authority. Both carry the **donor-reseed caveat** (published deliverable
> YAMLs — fix any ingestion donor too, per `reference_p2kb_yaml_donor_reseed`).

### F-175 — smart-pin examples wait on the IN flag with a broken mask `PINREAD(pin) & $8000_0000` (single-pin PINREAD returns 0/1, so bit 31 is never set → infinite loop) — `DONE (2026-07-01)`
> **APPLIED 2026-07-01.** Dropped the mask across **6 sites in 5 files** (one more than first reported — the deep audit found `spi-implementation-guide.yaml:105` with the `< 0` variant): sync-serial-rx (2), sync-serial-tx, pulse-cycle-output, dac-16bit-pwm-dither, spi-implementation-guide. Fix = bare `REPEAT UNTIL PINREAD(pin)` / `IF PINREAD(pin)` — the corpus-consistent idiom (PINREAD yields the IN bit as 0/1; matches ~8 other bare-PINREAD sites + `pinread.yaml`). `pnut-ts`-verified. **Donors fixed** (the 4 concise donors: 11101/11100/00100/00011); the SPI guide has no donor (authored standalone). Cross-domain spread into IOSP opus-master (`chapter-10-dac-output.md` ×2, `chapter-11-serial-transmit.md`, `examples-library/ch10-audio-dac.spin2`) is tracked for the IOSP campaign §2 finalize (pre-first-release, not this YAML set).
> **The defect.** Five published smart-pin YAMLs poll the IN flag with `REPEAT UNTIL PINREAD(pin)
> & $8000_0000` (or `IF PINREAD(pin) & $8000_0000`). `PINREAD` on a **single** pin returns **0 or
> 1** (`language/spin2/methods/pinread.yaml`: *"For single pin: returns 0 or 1"*), so masking with
> bit 31 (`$8000_0000`) is **always false** — the loop never exits. The mask looks copied from a
> raw-register / RDPIN-status mental model that does not apply to Spin2 `PINREAD`.
>
> **Occurrences (LIVE):**
> - `architecture/smart-pins/smart-pin-11101-sync-serial-receive.yaml:86, :99`
> - `architecture/smart-pins/smart-pin-11100-sync-serial-transmit.yaml:82`
> - `architecture/smart-pins/smart-pin-00100-pulse-cycle-output.yaml:70`
> - `architecture/smart-pins/smart-pin-00011-dac-16bit-pwm-dither.yaml:94`
>
> **Evidence.** `pinread.yaml` (single pin → 0/1). The Parallax 4DAC driver + reSound (OBEX #2861)
> wait on the IN event with `SETSE1`/`WAITSE1`; P2AN003's authoring replaced the mask with that
> idiom and compiles clean under `pnut-ts` v1.55.
>
> **Proposed correction.** Replace the broken mask with a working IN-wait: either drop the mask
> (`REPEAT UNTIL PINREAD(pin)` — PINREAD already yields the IN bit as 0/1) or use the
> `SETSE1(pin IN-rising)` + `WAITSE1` event idiom (preferred; matches the drivers). Apply set-wide
> across all five files, KB-validated, `pnut-ts`-compiled.

### F-176 — count-mode examples use the constant `P_B_A_INPUT`, which is UNDEFINED in `pnut-ts` v1.55 (examples do not compile) — `DONE (2026-07-01)`
> **APPLIED 2026-07-01.** `P_B_A_INPUT` is **invented** — the config it names (A-input feeds both A and B on one pin) is the **WRPIN default** (both selector nibbles default to this pin, per `wrpin.yaml`/Silicon Doc), so the fix is to **delete `| P_B_A_INPUT`** (the bare mode constant is the correct single-pin config). Removed all **21 occurrences across the 4 files** (10100/10101/10110/10111): code lines, `known_constants` bullets (replaced with a correct "no routing constant needed" note), and mis-teaching prose. `pnut-ts`-verified.
> **VINDICATION (the manual already caught this).** The IOSP manual team discovered `P_B_A_INPUT` was undefined back in **2026-05/06** and removed it from the manual (`audit/domain-judgments-2026-05-25.md:97` "(removed) — default A-input from local pin is correct"; `audit/titus-cross-audit-2026-06-12.md:2636` "B defaults to A's pin; NO constant (P_B_A_INPUT is undefined in pnut_ts)") — but the **YAML KB was never updated to match**. Manual↔YAML drift, manual-more-correct direction; the drain gate now closes it.
> **DONOR CARVE → see F-183.** The 4 count-mode *concise donors* are broadly divergent from published (undefined *mode-name* constants `P_PERIODS_STATES`/`P_PERIODS_CLOCKS_*` + a different mode taxonomy, on top of `P_B_A_INPUT`); published was hand-corrected away from them long ago. Partial-fixing them = false safety. Full donor resync tracked separately as **F-183**.
> **The defect.** Four published counting-mode YAMLs configure "use the A-input for both A and B
> (single-pin measurement)" with `P_COUNTER_* | P_B_A_INPUT`. `pnut-ts` v1.55 reports
> **`Undefined symbol`** for `P_B_A_INPUT` (and `P_A_B_INPUT`); the control constant `P_MINUS1_A`
> is defined, so this is a genuinely missing symbol, not a compiler gap. The examples cannot
> compile as written.
>
> **Occurrences (LIVE):**
> - `architecture/smart-pins/smart-pin-10100-count-highs-x-periods.yaml`
> - `architecture/smart-pins/smart-pin-10101-count-ticks-in-x-clocks.yaml`
> - `architecture/smart-pins/smart-pin-10110-count-highs-in-x-clocks.yaml`
> - `architecture/smart-pins/smart-pin-10111-count-periods-in-x-clocks.yaml`
> (used in `code_examples` PUB + DAT blocks, `known_constants` lists, and prose notes).
>
> **Evidence.** `pnut-ts` v1.55 `Undefined symbol` on `P_B_A_INPUT`. The validated single-pin
> routing (per the F. Bauer `fb_measfreq2P` donor used in P2AN004) is: signal pin in
> `P_COUNTER_TICKS` (default-local A/B), plus the periods pin in `P_COUNTER_PERIODS | P_MINUS1_A |
> P_MINUS1_B` routed back one pin — this compiles.
>
> **Proposed correction (needs KB-first care — NOT a rename).** Determine the correct P2 routing
> for "A-input feeds both A and B on one pin" and rewrite the examples to a `pnut-ts`-compiling
> idiom (the Bauer routing above is the proven pattern). Do **not** merely substitute a symbol
> name — verify the actual routing against the KB + a `pnut-ts` compile. Fix the `known_constants`
> lists + prose references in the same pass.

> **Drain-note (both).** These are actionable smart-pin YAML corrections; fold them into the same
> `yaml-knowledge-base-maintenance` drain pass as **F-174**. The IOSP release-depth re-audit (§2)
> should assess whether any block the IOSP drain gate (IOSP documents these modes in Ch.10/§15/§17).

---

## Systematic `P_*` constant-name audit (2026-07-01) — F-177…F-183

> **Origin & method (Stephen's call).** After F-174/175/176 kept surfacing fictitious `P_*`
> constants ad-hoc, we ran a **corpus-wide audit** to make it the last time. Method: the
> **legality arbiter is `pnut-ts` v1.55** (our authority order: compiler → v55 doc → Silicon);
> the **v55 Spin2 manual is the enumeration**. Extracted every unique `P_[A-Z0-9_]+` token in
> `deliverables/ai/P2/` (115) and compile-tested each. **Result: after the fixes below, the
> YAMLs contain ONLY legal v55 constant names** — `Y-legal \ L` is empty (no legal-but-nonstandard
> names), and all 8 fictitious names are gone corpus-wide. Also ran the **Opus-Master propagation**:
> the manuals are clean in body (they'd already removed these — see F-176 vindication). Two
> non-blocking findings remain: **F-182** (coverage gap) and **F-183** (donor staleness).

### F-177 — `language/spin2/methods/pinstart.yaml` uses `P_QUADRATURE_A` (undefined) — `DONE (2026-07-01)`
> **APPLIED.** Quadrature mode %01011 is `P_QUADRATURE`; `P_QUADRATURE_A` is undefined (`pnut-ts`). Renamed at `pinstart.yaml:47`. Single occurrence.

### F-178 — `P_TRANSITION_OUTPUT` (undefined) used in 4 files — `DONE (2026-07-01)`
> **APPLIED.** Transition-output mode %00101 is `P_TRANSITION`; `P_TRANSITION_OUTPUT` is undefined. Renamed at the **4 legit sites**: `pinstart.yaml:96`, `wypin.yaml` (×2 — code + prose), `concepts/streamer_smartpin_control.yaml` (×2). `pnut-ts`-verified. (The 5th occurrence, `io_pin_timing.yaml:341`, was part of a broken fragment → fixed under F-179.)

### F-179 — `architecture/io_pin_timing.yaml` `timing_measurement_techniques` fragments are unsound P1-era pseudo-code — `DONE (2026-07-01)`
> **The defect.** Both fragments used undefined constants (`P_TRANSITION_OUTPUT`/`P_TRANSITION_INPUT`/`P_PULSE_MEASURE`) plus **`WAITPEQ`, a P1 instruction invalid on P2**; the "pin-to-pin delay" technique doesn't even need smart pins.
> **APPLIED.** Rewrote `using_counters` to correct plain-GPIO timing (`FLTL`/`DIRL`/`DIRH` + `GETCT` + a `TESTP`/`JMP` sense loop, no smart pins, no `WAITPEQ`), and `using_smart_pins` to the real pulse-width mode `P_HIGH_TICKS` + `RDPIN`. Full rewrite **compile-verified** under `pnut-ts` (exit 0).

### F-180 — Spin2-method mode tables name `P_DAC_DITHER` (undefined; real: `P_DAC_DITHER_PWM`/`_RND`) — `DONE (2026-07-01)`
> **APPLIED.** `P_DAC_DITHER` (bare) is undefined; %00011 dither is `P_DAC_DITHER_PWM`. Renamed in the `common_smart_modes` / WYPIN-value tables: `spin2/methods/wrpin.yaml:86`, `spin2/methods/wypin.yaml:92`. `pnut-ts`-verified.

### F-181 — jonnymac style-docs reference `P_HIGH_1M5` — a fabricated constant AND a fabricated 1.5 MΩ pullup — `DONE (2026-07-01)`
> **The defect.** `P_HIGH_1M5` is undefined, and v55's pull-resistor family **tops out at `P_HIGH_150K` (150 kΩ)** — there is **no 1.5 MΩ pullup** on the P2 at all (v55 has no `1.5M`/`1M5`/`pullup` match). So both the constant and the hardware value were fictitious, in 2 documentation-style files.
> **APPLIED.** Changed the illustrative example to the real largest pullup `P_HIGH_150K` with an honest "150K pullup" comment: `conventions/spin2-docs-jonnymac.yaml:196`, `conventions/johnny-mac-documentation-style.yaml:303`. (Also tidied two prose SPI comments — `P_MINUS`/`P_PLUS` → `P_MINUSx_A`/`P_PLUSx_A` — so no prose ambiguously names a bare constant.)

### F-182 — coverage gap: 32 legal v55 `P_*` constants were unmentioned in any YAML — `DONE (2026-07-01)`
> **The gap.** Of 116 legal-in-v55 `P_*` constants, **32 appeared in no YAML** — the A/B input-logic family (`P_AND_AB`/`P_OR_AB`/`P_XOR_AB`/`P_PASS_AB`), filter/level selectors (`P_FILT0/2/3_AB`, `P_LEVEL_*_FB*`, `P_SCHMITT_*_FB`, `P_LOGIC_*`), `P_INVERT_IN/OUT`, `P_TRUE_*`, `P_MINUS2_A`/`P_MINUS3_A`, `P_SYNC_IO`/`P_ASYNC_IO`, and drive/float constants (`P_HIGH_100UA`/`P_HIGH_10UA`/`P_HIGH_FLOAT`/`P_LOW_*`). A findability hole — a remote agent asking about these got nothing.
> **APPLIED 2026-07-01.** Added all **32** as full entries to `language/spin2/symbols/spin2-builtin-symbols-complete.yaml` (where their siblings `P_TRUE_A`/`P_LOCAL_A` live). Every `value` + `bit_pattern` + `description` sourced verbatim from the v55 WRPIN config table (lines 1422–1519); the hex values were **compiler-certified** (bit-pattern→hex cross-checked against `pnut-ts`-produced binary on a representative sample spanning the AB-select, IN-invert, drive, and relative-pin families). All 32 compile; crossref clean. The KB now covers the complete legal `P_*` set.

### F-183 — count-mode *concise donors* (10100/10101/10110/10111) are broadly stale/divergent from published — `TRACKED → ingestion`
> Carved from F-176. The 4 donors carry undefined **mode-name** constants (`P_PERIODS_STATES`, `P_PERIODS_CLOCKS_TIME/STATES/PERIODS`) **and** a different mode taxonomy than the (hand-corrected) published files, on top of the now-removed `P_B_A_INPUT`. Published diverged from them long ago (proving the concise-YAML pipeline isn't re-run for these), so reseed-risk is currently latent. A **full donor↔published resync** (mode names + taxonomy) belongs to the ingestion/smart-pins-catalog head, not a published-YAML edit. Tracked, not release-blocking.

## Systematic `X_*` (streamer) constant-name audit (2026-07-01) — F-184…F-185

> **Origin & method.** Extended the P_* audit to the streamer `X_*` constants (the Streamer
> Programming Guide is released, so accuracy matters). Same method: `pnut-ts` v1.55 = legality
> arbiter, v55 = enumeration. **Coverage is 100%** — every legal v55 `X_*` is already in a YAML
> (no gap, better than P_*). Two fictitious names found + fixed; `X_RFBYTE_*`/`X_RFLONG_*` are
> legit prose family refs and `X_VALUE` is an example variable name (both left).

### F-184 — `X_DACS_ON` (undefined) in a `related_symbols` link — `DONE (2026-07-01)`
> **APPLIED.** There is no `X_DACS_ON` — v55 has `X_DACS_OFF` + specific channel configs (`X_DACS_0_0_0_0` … `X_DACS_3_2_1_0`). Fixed the `related_symbols` of the `X_PINS_ON` entry in `language/spin2/symbols/spin2-builtin-symbols-complete.yaml:257` → `X_DACS_OFF` (the real DAC control constant, already used in the sibling `X_PINS_OFF` entry). `pnut-ts`-verified.

### F-185 — `X_DDS_GOERTZEL` (truncated/undefined) in prose — `DONE (2026-07-01)`
> **APPLIED.** The real Goertzel streamer modes are `X_DDS_GOERTZEL_SINC1` / `X_DDS_GOERTZEL_SINC2` (v55 table); bare `X_DDS_GOERTZEL` is undefined. Corrected the prose in `language/pasm2/getxacc.yaml:50` to name both real constants. `pnut-ts`-verified.

### F-182 (coverage enrichment) — DONE this release
> The 32 missing legal P_* constants were added to `spin2-builtin-symbols-complete.yaml`,
> v55-sourced + compiler-certified, and ship in the same release as the fictitious-name fixes.
> See the F-182 entry above for detail.

## Chip Gracey forum-thread reconciliation (2026-07-01) — F-186…F-188

> **Origin.** Reconciliation of the "Reciprocal Counter Demo" forum thread (170882) —
> authored by Chip Gracey (`cgracey`, P2 designer, 🏆) — against the I/O & Smart Pins User
> Guide and the served smart-pin YAMLs. Full ingestion + queue:
> `engineering/ingestion/external-inputs/forum-threads/`. Both audiences fixed in one pass
> (manual reader + YAML-consuming agent). Also applied this pass (reader enrichment, not a
> defect): the ADC self-bias / no-mic-bias-divider note in IOSP Ch.16 Example 2.

### F-186 — 32-bit overflow in smart-pin frequency/duty math (manual + YAML) — `DONE (2026-07-01)`
> **CONFIRMED (Chip Gracey 🏆 + MULDIV64 KB semantics + arithmetic).** Frequency/duty were
> computed as 32-bit `(periods * clkfreq) / ticks` (and `(highs * 100) / ticks`), which
> overflows for any real signal (100 periods times 200 MHz = 2e10, past 2^32). Chip's thread
> flags the 64-bit-intermediate requirement. **Fixed to `MULDIV64(...)`** (a real Spin2
> built-in, already used in IOSP Ch.16:227) at every site:
> - manual `chapter-15-period-frequency.md` — 12 sites (§15.2/§15.4/§15.6 code + §15.9
>   formulas) + a teach-once "compute with MULDIV64" note in §15.1; plus
>   `examples-library/ch15-oscillator-calibration.spin2` (pnut-ts clean).
> - YAML `smart-pin-10101/10110/10111-*.yaml` — freq + duty compute lines.
> Code-line (K=76) + inline-ASCII gates pass; crossrefs validate. Ships: manual in the IOSP
> release; YAML in the next KB release-yamls pass.
> **STRAGGLER FIXED (2026-07-04):** the F-192 pass surfaced one duty line this sweep had missed —
> `smart-pin-10101-count-ticks-in-x-clocks.yaml:66` still read `(highs * 100) / ticks`. Converted to
> `MULDIV64(highs, 100, ticks)` to match the rest of the sweep (same authority, same overflow class).

### F-187 — concurrent-measurement example silently needs the signal on every pin — `DONE (2026-07-01)`
> **CONFIRMED (Chip Gracey 🏆; routing constants compiler-verified).** The 3-cell (and 2-cell)
> concurrent frequency/duty examples configured each cell with `%00` on separate pins, which
> only works if the signal is physically wired to all of them — otherwise the extra cells' IN
> flags never rise and the `REPEAT UNTIL` hangs. Chip's thread notes the cells can watch one
> signal pin via A-input routing without consuming pins. **Added the single-pin routing
> technique** (`P_MINUS1_A` / `P_MINUS2_A`) to IOSP §15.4 and to the `smart-pin-10110/10111`
> YAML examples, with signal placement clarified.
> **CORRECTION (2026-07-04, F-192):** this A-only routing was **incomplete** — the period-aligned modes also
> need the **B-input** routed to the observed pin (`| P_MINUS*_B`), or the window never closes and the cell
> hangs. Proven on P2 silicon (see **F-192**). All sites patched to `P_MINUS*_A | P_MINUS*_B`. Chip's guidance
> ("watch one pin via input routing") was right; the mistake was routing only A, not both A and B.

### F-188 — same 32-bit overflow class in OUTPUT-mode unit conversions — `DONE (2026-07-02)`
> **CONFIRMED (range analysis + arithmetic; same MULDIV64 class as F-186).** The
> `(a * clkfreq) / 1_000_000` microseconds-to-clocks idiom overflows for realistic inputs.
> Verified ranges: both sites carry **servo pulse widths in microseconds (~1000–2000 µs)** ×
> `clkfreq` (200 MHz) = ~2e11–4e11, far past 2³². **Fixed to `MULDIV64(...)`** (64-bit
> intermediate, the F-186 pattern) at both named sites:
> - `architecture/smart-pins/smart-pin-00111-nco-duty.yaml:76` — `MULDIV64(us_width, _clkfreq, 1_000_000) * ($FFFFFFFF / period)` (second factor stays ≤2³²: verified ~4.3e8 for a 2 ms pulse).
> - `language/spin2/patterns/applications/motor_controller.yaml:11` — `wypin(MULDIV64(angle, clkfreq, 1_000_000), pin)`.
> **Evidence-scoping:** the tree-wide sweep for this idiom surfaced a THIRD site not named in the
> original finding → logged + fixed as **F-189**. YAML-format + crossref validate clean. Ships in
> this release-yamls patch.

### F-189 — µs→cycles conversion taught as "better" while overflowing (`timing_operations.yaml`) — `DONE (2026-07-02)`
> **CONFIRMED (surfaced by the F-188 sweep; same overflow class).** `language/spin2/concepts/timing_operations.yaml`
> recommended `cycles := clkfreq * us / 1_000_000` as the **"better"** form (:145) and as the
> anti-pattern's **"correct"** example (:406) — but that product overflows 32-bit once `us` exceeds
> ~21 at 200 MHz. The file is otherwise overflow-aware (it warns extensively about the ms→cycles
> path), so this was an inconsistent gap teaching an overflow-prone idiom as best practice.
> **Fixed to `MULDIV64(clkfreq, us, 1_000_000)`** at both sites (full precision AND no overflow — the
> both-worlds answer the file's own lessons point toward), plus a `better_note` explaining why.
> Validate clean. Ships in this release-yamls patch.

### F-190 — SINC2 Goertzel constant-iteration silicon limitation absent from `getxacc.yaml` — `DONE (2026-07-02)`
> **CONFIRMED (Chip Gracey 🏆, P2 designer, forum thread 176065, 2024-12-16).** The Goertzel SINC2
> (double-integration) mode requires a **constant** iteration count per cycle; a non-power-of-two
> `SETXFRQ` D makes GETXACC capture an off-by-one integration that corrupts the current + next
> samples (~30–60 ms periodic glitches). `getxacc.yaml` documented the SINC1/SINC2 setup but not
> this constraint. **Added a `sinc2_constraint` field** under `goertzel_usage:` with the mechanism +
> three workarounds (power-of-two clock / SINC1 / XZERO+<20 ms). **Source note:** Chip states he
> added this to the Silicon Doc, but the released Silicon Doc we hold has NOT been updated — so the
> authority is Chip's designer report, attributed as such in the YAML (not cited to a Silicon-Doc
> note our copy lacks). The manual-side twin shipped in the Streamer Guide (§10.4, CHANGELOG
> "Unreleased"). Validate clean. Ships in this release-yamls patch.

### F-192 — concurrent frequency/period cells routed A-only (F-187) also need B routed — `DONE (2026-07-04, hardware-verified 🏆)`
> **CONFIRMED — HARDWARE-VERIFIED on P2 silicon (2026-07-04).** The F-187 A-only routing hangs;
> the neighbour cells need `| P_MINUS*_B` too. Empirical proof: `test70-f187-f192-concurrent-routing.spin2`
> (IOSP `audit/verification-tests/`) drove a ~1 MHz NCO signal on P0 → P2 (jumper) and configured three
> neighbour cells (P3 TICKS, P4 HIGHS, P5 PERIODS) tapping P2 via `P_MINUS*_A`. A rig-integrity phase
> (mode `%10010`, A-input only) proved **all** cells' A-inputs LIVE (ticks≈199_850 for 1000 rises).
> Then: **PASS A (A-only) → all three neighbours TIMEOUT (0)**; **PASS B (A|B) → all three READY with exact
> values** (ticks=2_000_000, highs=1_000_000, periods=10_000, freq=1_000_000 Hz). Since the A-routing is
> byte-identical between passes and A-liveness is proven, the sole cause of the hang is the missing B-input:
> these X-clocks modes (`%10101/%10110/%10111`, Y=%00) are period-aligned and close their window on a
> **B-rise**, which never comes if B stays on the cell's idle own-pin. Matches the Silicon Doc, the working
> `fb_measfreq2P` donor, and the already-released **P2AN004** companion (which correctly ships
> `P_MINUS1_A | P_MINUS1_B`). Log: `logs/debug_260704-125420.log`.
> **APPLIED (yaml + manual) 2026-07-04:** added `| P_MINUS*_B` at every A-only concurrent-measurement site —
> `smart-pin-10111-count-periods-in-x-clocks.yaml` (:99 TICKS, :101 HIGHS + comment), `smart-pin-10110-count-highs-in-x-clocks.yaml`
> (:59 TICKS + comment), and IOSP `chapter-15-period-frequency.md` §15 prose (the routing alternative + its
> parenthetical, now noting the hardware verification). Evidence replicated to the empirical ledger
> (`engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md`). Manual fix ships
> in the next IOSP release. **Original (superseded) NEEDS-VERIFICATION note follows.**
> **NEEDS-VERIFICATION (Silicon Doc + working donor vs. the F-187 resolution — needs a hardware spot-check).**
> Surfaced by the P2AN004 (measurement app-note) release-gate audit. **F-187** added the single-pin
> concurrent-measurement routing `P_MINUS1_A` / `P_MINUS2_A` (A-input only) to IOSP §15.4 and the
> `smart-pin-10110` / `smart-pin-10111` YAML examples, so extra counter cells can watch one signal
> pin without consuming pins. But the Silicon Doc (`part4-smart-pins.txt`) defines a period as
> **"A-input rise/edge to B-input rise/edge"** (Y=%00 = A-rise to B-rise) and explicitly notes
> **"The B-input can be set to the same pin as the A-input for single-pin cycle measurement."** On a
> *neighbour* cell with only A routed, the B-input stays on the cell's idle own-pin, which never
> rises — so by that definition the in-progress period never completes and `REPEAT UNTIL` would hang,
> the very failure F-187 set out to fix. The empirically-working **F. Bauer `fb_measfreq2P`** donor
> (the routing P2AN004 R2 adopts) routes **both** A and B (`P_COUNTER_PERIODS | P_MINUS1_A |
> P_MINUS1_B`), matching the Silicon Doc note.
> **Likely fix:** add the matching `| P_MINUS1_B` / `| P_MINUS2_B` to the F-187 YAML + IOSP §15.4
> examples. **Do NOT apply blind** — F-187 is Chip-Gracey-attributed (🏆); confirm on silicon whether
> A-only routing actually hangs (vs. some period-detection path that tolerates an idle B) before
> editing. **P2AN004 is unaffected** — R2 already routes both A and B (correct either way), so this is
> non-blocking for that release. Cross-ref **F-187**.

### F-193 — IOSP ch05 falsely claims no single instruction waits on event+timeout; teaches a busy-poll — `APPLIED across KB + IOSP + PASM2 (🏆 HW-PROVEN EF-020); releases pending (phase-1 YAML, phase-2 doc patches)`
> **CONFIRMED (documentary + hardware-in-progress).** IOSP `chapter-05-working-with-smart-pins.md` §"Wait with a
> timeout" stated **"No single instruction waits on an event *and* a timer at once, so poll both…"** and taught a
> busy-poll `.race` loop — contradicting the section's own preceding "true stall" pitch (poll-spin burns cycles/power).
> The claim is **false**: a **`SETQ` (future CT target) immediately before `WAITSEx`** makes that one stalling
> instruction release on whichever comes first (event or deadline), reporting which via `WC` (C=1 timeout, C=0 event).
> This is already documented in our KB (`waitse1-4.yaml` + the 14-instruction wait family) and partly in the PASM2
> manual. Origin: forum thread (evanh + TonyB silicon testing) surfaced the related no-SETQ corner case.
> **APPLIED (IOSP) 2026-07-04:** rewrote §"Wait with a timeout" — deleted the false sentence, led with the
> `SETQ`+`WAITSE1 WC` atomic stall-with-timeout (noting C≡Z, so one flag suffices; and that the idiom generalizes to
> the whole `WAIT*` family), and **kept** the double-poll `.race` loop as a labeled "when you must do work while
> waiting" alternative. Ships next IOSP release.
> **Hardware proof:** `test74-waitse-setq-timeout.spin2` (P0, edge-based, single cog) — event-wins → C=0,
> timeout-wins → C=1, no-SETQ `WCZ` → C=Z=0. **PROVEN 2026-07-04 (🏆 EF-020)** — all three cases pass. (First run had
> a rig bug: pin P16 has external hardware and held the level high; moved to P0 + a discrete rising-edge event.)
> **NOW QUEUED (proof landed):**
> - **(a) No-SETQ free-clear corner case — APPLIED (KB) 2026-07-04.** Added a `no_setq_behavior:` field (cited to
>   EF-020, not the forum) to **all 15** timeout-family wait YAMLs: `waitatn, waitct1-3, waitfbw, waitint, waitpat,
>   waitse1-4, waitxfi, waitxmt, waitxrl, waitxro`. **Scope catch:** `waitxmt` was initially missed because a grep
>   for "SETQ…timeout" failed on its folded block-scalar (the two words landed on separate lines) — re-derived the
>   family from the manual's bullet-map + a folding-safe scan (15, not 14). `waitx` (fixed-delay) correctly excluded.
>   Crossref validates clean. Ships in the phase-1 YAML release.
> - **(b) PASM2-reference — APPLIED (manual) 2026-07-04.** In `instructions-w.md`, added a uniform bullet to all
>   10 event-wait entry headers (15 instructions incl. `WAITXMT`) giving the full SETQ-arming how-to **and** the
>   no-SETQ free-clear behavior, and added "(prior SETQ = CT timeout)" to the 8 Operation lines that lacked it
>   (`WAITFBW/INT/PAT/SE/XFI/XMT/XRL/XRO`; `WAITATN`/`WAITCTn` already had it — not doubled). Ships in the phase-2
>   PASM2 patch.
> - **NOT for IOSP:** the no-SETQ free-clear detail is too low-level for the user guide; it lives in the PASM2 ref + KB.
> **Reject** a "WC-without-SETQ" lint — the free-clear idiom is intentional; a lint would false-positive.

---

*Move-aside 2026-06-13 after the v1.9.0 release closed out F-001..F-124. The archive holds the full history; this active register carries only the carry-forward guardrails and the ingestion-tracked items. New findings continue at F-125.*
