# P2KB Correction Findings — Consolidated Register

**Purpose:** A single, append-only register of everything we discover that is **wrong or needs correction** — primarily in the P2 Knowledge Base YAML (`deliverables/ai/P2/`), but also any other source/content correctness issue worth tracking. This is the hand-off document for the agent that corrects the P2KB (via the `yaml-knowledge-base-maintenance` skill).

**How to use this register:**
- When any work (manual production, audits, example compilation, ingestion) surfaces something incorrect, **add it here** — do not leave it only in a per-manual note.
- Each finding gets: an ID, a status, the exact location, what's wrong, the evidence, and the proposed correction.
- **Annotate as you fix, same pass** — flip the status, add an applied-note + source trace, and log any newly-surfaced defects as new findings. See `yaml-knowledge-base-maintenance` skill §4.5. A stale register (statuses lagging the YAML) lies and invites re-chasing.

**Status legend:** `CONFIRMED` (verified against an authority; ready to fix) · `NEEDS-VERIFICATION` (suspected; must be checked before acting) · `DONE` (corrected + verified) · `WONTFIX` (investigated, not a defect) · `RESOLVED-INVALID` (the reported defect does not exist) · `TRACKED → ingestion` (real, but the resolution lives in the ingestion head, not a YAML edit).

**Authority order for P2 language facts:** the `pnut_ts` compiler (ground truth for what compiles) → the Spin2 v51 documentation (`engineering/ingestion/sources/spin2-v51/`) → the Silicon Doc. The KB YAML must match these.

**Next finding ID: `F-154`**

**Archive:** findings F-001..F-124 (all `DONE` / closed) live in
`engineering/operations/correction-sweeps/2026-06-13-P2KB-CORRECTION-FINDINGS-archive.md`.
**Search the archive before re-filing** — most past defects (and the reasons they were settled) are there.

---

## Carry-forward guardrails — investigated and settled; do NOT re-file (full detail in the archive)

- **F-002 (`WONTFIX`):** `?` / `||` operator-form failures were an agent usage error — the KB is correct (`??var` = XORO32 random; `ABS()` not `||`; `?` is the ternary operator).
- **F-036 (`WONTFIX`):** `calld.yaml` — LOC loading a 20-bit address into PA/PB/PTRA/PTRB is not a defect.
- **F-093 (`WONTFIX`):** `lockrel.yaml` C-flag polarity — the appendix's "inverted" claim is the error; the YAML is correct (C = lock-was-held).
- **F-114b (`RESOLVED-INVALID`):** the MIDI display modes KEYBOARD / GRID / ROLL / MONITOR do **not** exist in PNut v55 — do **not** add them to `midi.yaml` (it carries an explicit `not_supported:` claim).
- **Verified-resolved (don't re-chase):** the Jan-2026 streamer KB audit's issues were all reconciled in the 2026-05/06 passes (DAC routing, 32-pin groups, mode encoding, xcont/xzero phase wording, setxfrq 2³¹ formula, streamer symbols). Only the XZERO concept text was open and is fixed (F-003).

---

## Open — TRACKED in the ingestion head (resolution lives there, not in a YAML edit)

- **F-121 — #64006 P2 Eval Add-on Board roster needs authoritative per-board pin maps via cross-edition ingestion.** Ingest the Aug-2020 `#64006-ES` Product Guide (stage the PDF) and cross-check against the already-ingested Aug-2025 `#64006` edition; reconcile `hardware/addon-*.yaml`. The 2 fabricated entries (`addon-digital-io-board`, `addon-servo-header`) were **removed** in v1.9.0; the 4 part-number-less orphans (`7_segment_display`, `buttons_board`, `switches_and_leds`, `switches_board`) still need verification. Queued in `engineering/ingestion/README.md`. Authoritative 2025 map: A=Control B=Serial Host C=LED Matrix D=Digital Video Out E=Mini Prototyping F=Serial Device G=Goertzel H=A/V Breakout; `#64006-ES` = Complete Accessory Set SKU.
- **F-122 — 64004-ES HyperRAM/HyperFlash add-on board has no standalone YAML.** Product Guide staged + queued as the next ingestion (`sources/hyperRam-n-hyperFlash/`). Do **not** fabricate from raw CAD.
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

### F-141 — `architecture/smart_pin_patterns.yaml` carries 3 wrong smart-pin register-roles (stale; skipped by the F-135–F-140 sweep) — `CONFIRMED`
- **Repository value via WYPIN (L219)** — should be **WXPIN** (X holds the long; `smart-pin-00001-*.yaml` + Silicon `part4-smart-pins.txt` L224-226). · **Basic-ADC "trigger conversion" via WYPIN (L142/L151)** — ADC samples **continuously** once enabled; no WYPIN trigger (`smart-pin-11000-*.yaml`; Silicon L66/L73/L124). · **Quadrature counter "clear" via `WYPIN #0` (L175)** — zeroed by **pulsing DIR low** (`smart-pin-01011-*.yaml`; Silicon L550). Plus value-mode examples use WYPIN-before-DIRH (order-safe, cosmetic).
- **Fix:** reconcile `smart_pin_patterns.yaml` to the per-mode files (repository→WXPIN, drop ADC WYPIN-trigger, quadrature→DIR-low) + adopt the universal init order.

### F-142 — `language/pasm2/wrpin.yaml` STILL teaches WYPIN-before-DIRH (the F-140 bug, surviving in the instruction page) — `CONFIRMED ★`
- `wrpin.yaml` `critical_requirement.sequence` (L30-35) **and** the PWM example (L45-53, `WYPIN #50` at L51 before `DIRH` at L53) both order WYPIN before enable. Contradicts the corrected `architecture/smart_pins.yaml` (F-140) + EF-011. **Fix:** reorder to `…WXPIN → DIRH → WYPIN` + the trigger/serial note (same fix as F-140).

### F-143 — `architecture/cordic.yaml` overview contradicts the (correct) CORDIC instruction pages — `CONFIRMED ★ (QFRAC)`
- **QFRAC = "fractional multiply" (L45-50) — WRONG, it is a DIVIDE** (`qfrac.yaml`; Silicon L7336 "Divide {D:0} by S"; grouped with QDIV at L2534). **CRITICAL.** · QSQRT "32→16-bit" (L52-56) — actually **64-bit** input, 32-bit root (`qsqrt.yaml`). · QMUL `signed: true` (L30-36) — QMUL is **unsigned** (`qmul.yaml`; Silicon L7304). · CORDIC latency "54 clocks" — **55** (pipeline depth 54; Silicon "fifty-five clocks later"). **Fix:** correct `cordic.yaml` to the instruction pages.

### F-144 — `architecture/interrupts.yaml` has interrupt PRIORITY inverted + a wrong source-ID table — `CONFIRMED ★ (priority)`
- **Priority: file says INT3 highest / INT1 lowest — INVERTED.** Silicon `part3-interrupts.txt` L73/L77/L189: **INT1 highest, INT3 lowest** (matches `cog.yaml`). · **`interrupt_sources_detail` (codes 9-15) shifted/fabricated** (e.g. invents "SELH edge" sources) vs the correct table in `event_system.yaml` + `streamer/overview.yaml` + Silicon L86-100 (8=pattern,9=FIFO,10=streamer-ready,11=streamer-out,12=NCO,13=LUT$1FF,14=ATN,15=CORDIC). **Fix:** rewrite `interrupts.yaml` priority + source table to Silicon.

### F-145 — `language/pasm2/concepts/basic-io.yaml` transposes OUTA/OUTB/INA/INB register addresses — `CONFIRMED`
- File: OUTA=$1FE, OUTB=$1FF, INA=$1FC, INB=$1FD. Correct (Silicon L939-947; `system-registers/dira-dirb-registers.yaml`; canonical map): **OUTA=$1FC, OUTB=$1FD, INA=$1FE, INB=$1FF** — the OUT and IN blocks are swapped. **Fix:** correct the four addresses.

### F-146 — `language/spin2/concepts/operators.yaml` carries P1 semantics + inverted precedence claims — `CONFIRMED`
- **`~` / `~~` documented as P1 "sign-extend" (L280-286)** — in P2 they are **post-clear / post-set** (`special-symbols/~.yaml`, `~~.yaml`; v55 operator table). · **Anti-pattern precedence claims inverted (L201-217):** claims C-style "compare binds tighter than `&`" and "`+` binds tighter than `<<`"; P2 is the opposite (`&` tighter than `==`, `<<` tighter than `+` — `precedence.yaml` + v55). **Fix:** rewrite both to P2 semantics.

### F-147 — addressing concept files contradict the instruction pages — `CONFIRMED`
- `concepts/addressing_modes.yaml` (L16-18): **AUGS/AUGD split by WIDTH** (20-bit vs 32-bit) — actually split by **FIELD** (AUGS=Src, AUGD=Dest; both yield 32-bit literals — `augs.yaml`/`augd.yaml`; Silicon part3-end L166-175). · `concepts/register_indirection.yaml` (L45): **ALTR = D+base+index (3-term)** — actually **(S+D) & $1FF (2-term)**, like ALTS/ALTD (`altr.yaml`; Silicon L1013-1016). **Fix:** correct both concept files.

### F-148 — `drvrnd/fltrnd/dirrnd` + `*not` pin files mis-state the WCZ flag source as "original" bit — `CONFIRMED`
- Their `flags_affected`/prose say C,Z = the **original** OUT/DIR bit (before modification); the plain siblings (`drvh/drvc/…`) + the same files' structured fields + the instruction CSV say C,Z = the **(new) OUT/DIR bit**. "original" is bled-over BIT-family wording. **Fix:** align the `*rnd`/`*not` flag wording to the family.

### F-149 — `language/spin2/statements/debug.yaml` examples STILL put a SCOPE channel-def on the CREATE line (the F-137 bug, surviving in 2 examples) — `CONFIRMED`
- Examples at L125 `` DEBUG(`SCOPE MyScope 'Sensor' AUTO 'Filtered' AUTO) `` and L171 `` DEBUG(`SCOPE Sensor 'Value' AUTO) `` contradict the **same file's** usage prose (L22) + `scope.yaml` + EF-003 (a channel-def on the SCOPE create line prevents window creation). **Fix:** split into create-then-config-message form (same as F-137).

### F-150 — `language/spin2/patterns/implementation/spin2_pin_control.yaml` reverses smart-pin method arg order — `CONFIRMED`
- Uses `wrpin(mode, pin)` / `wxpin(x, pin)` / `wypin(y, pin)` (**value-first**); the method pages + v55 + `pinstart.yaml` all specify **PinField first**: `WRPIN(pin, mode)` etc. Compiler can't catch it (positional). **Fix:** swap args pin-first throughout the pattern.

### F-151 — hardware HUB files stale vs the corrected Edge module detail pages (flash/PSRAM) — `CONFIRMED`
- **P2-EC flash:** `feature-comparison`/`selection-guide`/`compatibility-matrix` say **4MB**; `edge-standard-module.yaml` (+ on-board W25Q128, 128 Mbit) says **16MB**. · **P2-EC32MB:** hubs say "32MB **flash**, 0MB PSRAM"; `edge-32mb-module.yaml` says **16MB flash + 32MB PSRAM** (the "32MB" is PSRAM). · `compatibility-matrix` 32MB-module pin-efficiency row ("30%") uses an unsupportable denominator. **Fix:** re-sync the 3 hub files to the module detail pages. (Detail pages = authority; same root cause as HW corrections.)

### F-152 — `TASKRESUME` is a fabricated keyword; the real Spin2 keyword is `TASKCONT` — `CONFIRMED`
- `methods/taskresume.yaml` documents `TASKRESUME(TaskID)`, cross-referenced by `taskhalt/taskstop/taskspin.yaml`. `pnut-ts -d`: `TASKCONT(3)` compiles, `TASKRESUME(3)` errors. v55 history (L39) + keyword-gating table (L149) = **TASKCONT** (v47). Uniform across the cluster (so internally consistent but factually wrong). **Fix:** rename to TASKCONT (stub-don't-delete per supersession convention) + fix cross-refs.

### F-153 — minor internal inconsistencies (batch) — `CONFIRMED / LOW`
- `rdfast.yaml` L84 "block size 0 = max **16384 longs**" vs `architecture/fifo.yaml` "16384 **blocks**" (= 262,144 longs) — `rdfast` off by 16× (Silicon L6675). · `jnxmt.yaml`/`jnxro.yaml` `timing.type: fixed` while carrying `clocks: 2 or 4` (self-contradiction; twins say `variable`). · set-only jumps (`jfbw/jqmt/jxmt/jxrl`) oneliner "flag set **or clear**" vs their own "if set" description. · `concepts/setq_block_ops.yaml` L360 `common_errors` says "SETQ for LUT, SETQ2 for cog" — backwards vs the rest of the file. · `operators/precedence.yaml` absolute level numbers drift from v55 (relative order preserved) + `ADDBITS`/`ADDPINS` missing. · `debug-displays/plot.yaml` L51/L130 PRECISE "starts ON" vs v55 "disabled" default. · `p2-architecture-mental-model.yaml` + `cog.yaml` CORDIC latency "54" vs the 55-clock authority (see F-143). · `term.yaml` default color "LIME" vs v55 "GREEN" (cosmetic — settled RESOLVED-INVALID in F-128; the constant IS clLime). · `statements/debug.yaml` `documentation_source: v51` provenance staleness.

## Streamer grounding-audit drift (2026-06-19) — F-154…F-158

> **Origin:** the exhaustive grounding audit of the **Streamer Programming Guide**
> (`engineering/document-production/manuals/p2-streamer-programming-guide/audit/streamer-grounding-audit-2026-06-19.md`)
> surfaced 4 derived-YAML drift items. Per the trust chain (Silicon Doc = primary), the
> manual's **v1.0.1** fix is grounded directly in Silicon; **these YAML edits fold into the
> next yaml-head sweep (v1.10.1)** alongside F-141…F-153 (Stephen's call 2026-06-19). All
> `value`/`encoding` fields are correct — the errors are in `description:` text only.

### F-154 — `language/spin2/symbols/streamer-symbols.yaml` description text transposes pin↔DAC-channel counts — `CONFIRMED ★`
- For the immediate / RFBYTE-direct / WFBYTE-capture symbol families, the `description:` reads the **DAC-channel count as the pin count** and drops the true pin count. E.g. `X_RFBYTE_8P_1DAC8` (L159) says "→ 1 pin, 8 DAC"; Silicon `part2-pixel-ops.txt` L182 decodes it `RFBYTE -> 8-pin + 1-DAC8` = **8 pins, 1 DAC channel, 8 DAC bits**. The symbol token is `<N>P_<M>DAC<B>` (N=pins, M=DAC channels, B=DAC bits). The sibling `architecture/streamer/modes-reference.yaml` L194 already has it right ("8 pins, 8 DAC bits") — **the two YAMLs disagree**. **Root cause of manual findings H-4 + M-1.**
- **Authority:** Silicon `part2-pixel-ops.txt` L175–209; symbol-name grammar. **Fix:** rewrite every transposed `description:` to "N pins, M DAC ch × B bits" (encodings untouched).

### F-155 — `architecture/streamer/pin-selection.yaml` `%101` group labelled "24 pins"; it is 32 — `CONFIRMED`
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

### F-158 — `architecture/streamer/modes-reference.yaml` `selection_guide` recommends a 4-pin mode for 1-pin SPI — `CONFIRMED ★`
- `selection_guide.spi_output` (L346) recommends **`X_IMM_8X4_1DAC4 + X_ALT_ON`** for SPI output, but Silicon `part2-pixel-ops.txt` decodes `X_IMM_8X4_1DAC4` (mode %0110, D[19:16]=%0100) as a **4-pin** mode ("imm 8×4 → 4-pin + 1-DAC4 … 4 out"). One-pin SPI needs a **1-pin** immediate mode — **`X_IMM_32X1_1DAC1`** ("imm 32×1 → 1-pin + 1-DAC1 … 1 out"; count = number of bits). Surfaced as manual finding L-7; the manual's SPI examples (§13, §16.1) were corrected to `X_IMM_32X1_1DAC1` this pass, grounded in Silicon (the manual must not diverge from the KB on a guess, but here the *primary* source overrides the drifted KB). **Authority:** Silicon `part2-pixel-ops.txt` immediate-mode table. **Fix:** set `spi_output` to `X_IMM_32X1_1DAC1 + X_ALT_ON`; also re-check the IMM-family pin counts (same transposition as F-154/DRIFT-1 — `X_IMM_8X4_1DAC4` is 4-pin, not the "1-pin" the derived tables imply).

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

### F-135 — smart-pin %00101 (Transition Output): "Y=0 = continuous transitions" is FALSE (Y=0 is idle); plus a suspected WYPIN/enable order defect — `DONE (YAML) · set-wide sweep DONE via F-139`
> **Logged 2026-06-17** (RA-10 from the IOSP Titus cross-audit; todo #55).
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

---

*Move-aside 2026-06-13 after the v1.9.0 release closed out F-001..F-124. The archive holds the full history; this active register carries only the carry-forward guardrails and the ingestion-tracked items. New findings continue at F-125.*
