# YAML Head — P2KB Dashboard

> The **YAML knowledge-base head**'s standing-state board: what shipped recently
> (release ledger) and what hardware the KB serves (inventory). The served data
> lives in `deliverables/ai/P2/`; the open to-do list is
> [`P2KB-CORRECTION-FINDINGS.md`](P2KB-CORRECTION-FINDINGS.md). This board is an
> engineering doc — the YAML never links here.
>
> **Green** = `validate-yaml-syntax.py` + `validate-crossref-keys.py` +
> `validate-dod-release.py` all pass. **Release** = two-commit Path B (content →
> regenerate index → tag the index commit). Versions are git tags
> (`--sort=version:refname`).

## Release ledger (most recent first)

| Version | Date | What & why |
|---------|------|------------|
| **v1.14.4** | 2026-07-15 | **Scope-mode filter DC-range caveat (%11010) + XBYTE-engine example fixes.** Two-file KB delta. (1) `smart-pin-11010-adc-scope-trigger.yaml`: Silicon-Doc re-scan (RA-31 / Q2, prompted by a scope-filter figure recollection) resolved a would-be Chip question from the KB's own authority — scope samples normalize to 8 bits but the effective DC dynamic range is only ~5–6 bits per filter length (Silicon Doc `p2-documentation.txt:8778`); the `X[1:0]` filter selector was already present (v1.13.3). (2) `architecture/xbyte_engine.yaml`: drained **F-220–223** (surfaced during XBYTE Guide technique-mining, ground-truthed against nine implementations) — all three `programming_examples` now compile + dispatch (LUT entry packs SKIPF pattern in [31:10]/address in [9:0], not `@`-hub `<<23`; interpreter arms via `PUSH #$1FF` + `_RET_ SETQ #mode`; a non-assembling `_RET_ NOP` removed) and mode-operand bit 1 (`x`) marked undocumented pending Chip (Silicon-Doc-upstream gap, task #54 Q7). Manual-side twins: IOSP ch16 §16.5 + App F (v1.0.6, prepared); XBYTE Guide (held pre-release). |
| v1.14.3 | 2026-07-14 | **DEBUG-display sweep — the KB half of the coordinated Debug release.** Drained **F-212 + its 2026-07-14 addendum** (13 files: the 9 window YAMLs + `pc_mouse`, `statements/debug`, `debug-formatters-complete`, `constants/special-configuration-symbols`) and the YAML half of **F-216**. Unblocks the Debug Window Manual's YAML-HEAD drain gate (manual v1.1.0 ships alongside). **Inversions killed** — the class that silently mis-teaches a code-generating agent: `fft` MAG recorded as a right-shift *divisor* (it is a GAIN ×2^n — the YAML said MAG attenuates when it amplifies); `spectro` axes; `midi` velocity-0-note-on "does NOT release" (false limitation) + velocity-sets-*color* (it sets fill HEIGHT); `pc_mouse` `coordinate_basis_per_window` documented the on-screen READOUT as the wire value (5 of 9 windows return RAW CLIENT PIXELS — any agent-built hit-test was silently wrong); `term` listed a `LIME` keyword that does not exist. **Unsourced claim removed:** `scope`/`scope_xy` "(12 modes; default LONGS_1BIT)" — there is no packing default (unpacked; silicon-confirmed). **Hardware verdicts folded in:** 🏆 EF-020 (PLOT `CARTESIAN` bottom-left/Y-UP — the single most important PLOT fact, previously absent from the KB entirely), EF-042 (SPARSE + the DOTSIZE≥4 gate), EF-043 (no-POS placement is TOOL-DEPENDENT — swept across **all nine** windows, where one tool's auto-layout had been recorded as a P2 fact), EF-048 (OPACITY 256→0), EF-052 (runtime `RATE -1` freezes BITMAP). Plus `CLOSE` semantics + the real TITLE default caption across all nine; `logic` TRIGGER → XOR form + the count-before-color rule; `DEBUG_MASK`'s stale `{Spin2_v46}` gate (the same file twice said none is required); `DLY` last + releases LOCK[15]. |
| v1.14.2 | 2026-07-06 | **Cooperative-tasking + pattern accuracy; ADC ENOB terminology.** Drained F-196–F-201. F-196: removed the fabricated `taskwait.yaml`/`taskresume.yaml` (policy call — no invalid-keyword stubs; fake names resolve to nothing, recover via `p2kb_find task*`), redirected inbound refs to valid siblings (full paths), added a positive wait-idiom note to `tasknext`. F-197: `taskspin` expression-return (task#/-1). F-198: cog-local task IDs (top-level = that cog's task 0) — **🏆 EF-023** hardware-verified, `taskid`/`taskhlt`. F-199: `spin2_shared_memory` → P2 `LOCKTRY`/`LOCKREL` (compile-verified). F-200: `spin2_event_dispatcher` SPSC scope. F-201: `smart-pin-11001-adc-external-clock` SINC "ENOB" → nominal bits (Silicon-Doc misuse, Chip-conceded). |
| v1.14.1 | 2026-07-05 | **P_STATE_TICKS example single-read cleanup.** Drained F-195 — `smart-pin-10000-time-a-states.yaml` PWM example read `rdpin()` up to 3× per loop iteration (test-read + branch re-read, risking a cross-transition mismatch on fast signals); collapsed to one `duration := rdpin()` capture (bit 31=C state, bits[30:0]=ticks), compile-verified `pnut-ts -d` v1.55. Surfaced by an IOSP reader question that also produced F-194 (`RESOLVED-INVALID`: Spin2 `RDPIN()` `Zval[31]=C` is correct per v55 L543-4 — the reader hit a FlexSpin/PNut discrepancy, not a KB defect). Manual-side twin: IOSP Ch13 `analyze_pwm`/`pwm_analyzer` → v1.0.2. |
| v1.14.0 | 2026-07-04 | **Hardware-verified smart-pin/event-wait accuracy + AppNote companions served.** Drained F-192 (🏆 EF-017, test70): concurrent single-signal counter cells (%10101/10110/10111) hang on A-only routing — the period-aligned window closes on a B-rise — so `smart-pin-10110/10111` neighbour cells now route `P_MINUS*_A \| P_MINUS*_B`; supersedes F-187. F-193 (🏆 EF-020, test74): the `SETQ`+`WAITSEx` single-instruction event-OR-timeout wait + the no-SETQ free-clear corner case → new `no_setq_behavior` field on all 15 timeout-family instructions (`waitse1-4, waitct1-3, waitatn, waitfbw, waitint, waitpat, waitxfi, waitxmt, waitxrl, waitxro`; WAITXMT was a folded-block-scalar straggler). F-186 straggler (`10101` duty → MULDIV64); G-005 closed from EF-016 (async-TX first-byte NOT-OBSERVED, gotcha reframed). AppNote companions P2AN001–004 now MCP-served via an `application-notes`→`AppNote` index handler. Also HW-proven this wave: F-165 (signed C-flag true-sign, EF-018), F-139 (NCO phase-lock + sync-serial gapless under reordered init, EF-019). Manual-side twins ship as phase-2 patches: IOSP ch05 (event-wait timeout pattern) + ch15 (concurrent A+B); PASM2 `instructions-w.md` (SETQ + no-SETQ across the WAIT family). |
| v1.13.3 | 2026-07-03 | **ADC scope-trigger register correction (%11010).** Drained F-191 — `smart-pin-11010-adc-scope-trigger.yaml` documented the trigger level in Y; the Silicon Doc (`p2-documentation.txt:8781-8810`) puts it in X (WXPIN: X[15:10]=B, X[7:2]=A, X[1:0]=filter; A/B relationship sets arm-then-trigger; RDPIN returns the 8-bit sample, C=armed). Reworked x/y/z registers, timing, in_flag, both code_examples (WYPIN-trigger → WXPIN A/B/filter), notes; added `related:` SETSCP/GETSCP. An inverted finding from the IOSP release-gate audit (the manual was right on the register). **Clears the IOSP v1.0.0 drain gate.** Manual-side twin: IOSP App-F %11010 bit-fields corrected (ships with the IOSP release). |
| v1.13.2 | 2026-07-02 | **Forum-thread Y-row reconciliation (Chip Gracey threads 170882/176065).** Drained F-188 + F-189 — the 32-bit `(a*clkfreq)/1_000_000` overflow class → `MULDIV64` — across `smart-pin-00111-nco-duty`, `spin2/patterns/applications/motor_controller`, and `spin2/concepts/timing_operations` (µs→cycles was taught as the "better" idiom while overflowing past ~21 µs). F-190: SINC2 Goertzel constant-iteration silicon limitation added to `pasm2/getxacc.yaml` (source = Chip's designer report in 176065; the released Silicon Doc still lacks the 2024-12-16 note). Y2/Y4/Y5 verified already-correct (`rep` interrupts-stalled; `qmul`/`qdiv` unsigned; `setpiv` D[7:0] / `blnpix` / `rgbsqz` / `rgbexp`) — no change; Y3 8-clock hub-window spacing already documented. Manual-side twins ship separately: IOSP (Wave-1) + Streamer §10.4 (Wave-3). |
| v1.13.1 | 2026-07-01 | **Constant-name integrity + coverage (systematic `P_*`/`X_*` audit).** Legality-arbiter = `pnut-ts` v1.55, enumeration = v55. Drained the fictitious-constant class across smart-pin/streamer/pin-config examples: F-174 (USB `P_OE`), F-175 (broken `PINREAD & $8000_0000` IN-wait, 6 sites), F-176 (`P_B_A_INPUT` invented — 21 occ, the manual had already caught it), F-177 (`P_QUADRATURE_A`), F-178 (`P_TRANSITION_OUTPUT`), F-179 (`io_pin_timing` P1-era fragments rewritten), F-180 (`P_DAC_DITHER`→`_PWM`), F-181 (`P_HIGH_1M5` fabricated), F-184 (`X_DACS_ON`), F-185 (`X_DDS_GOERTZEL`→`_SINC1/2`). F-182: added the 32 missing legal v55 `P_*` pin-config constants to the symbols catalog (values compiler-certified). Corpus now contains ONLY legal compiler symbols (Y-legal ⊆ v55). |
| v1.13.0 | 2026-06-30 | **Decomposition layer expansion + object-shaping + CORDIC/ADC fixes.** Two external arch contributions ingested (multibus object-shaping; magTile decomposition memo) → 5 new entries: `worked-derivation-streaming-pipeline` + `shared-bus-broker` + `shared-bus-replication` + `object-image-dedup` + `pin-power-domains`. Decomposition enrichments: observability eval lens, fan-out-publication contract (B2) + frame-pool sizing (B7), decimation-placement (B3), one-forcing-sentence-per-cog (B6), as-built-audit practice (B9), field-corroboration (B8), bit-bang smell-with-escape (B10), c4↔observability distinction, breadth_gap_note closed. §3 dedup reproduced on our pnut-ts v1.55. Drained F-171 (CORDIC 7-8→~6-7), F-172 (CORDIC Spin2 multi-return sigs, pnut-ts -d clean), F-173 (4-pin VIO/GIO power domain). Findability sweep across spin2 object-model files. |
| v1.12.0 | 2026-06-29 | **Add-on board hardware coverage (addon-wave-2026-06).** Authored 7 `hardware/` board YAMLs: microSD #64009, RTC #64013, HD-Audio #64014, WX-WiFi #32420, WX-Adapter #64007, Motor-Driver #64010, Prop-Plug #32201 (re-ingested first). Findability (F-116): aliases on all + `p2kb-categories.json` (eval_addon_boards +5, new connectivity + programming_tools) + compatibility-matrix rows. Drained datasheet/HW gaps from NO-COMMIT staged sources (gitignored): G-013 RTC PCF8523 `$68`+regmap, G-010 WX baud/command-protocol, G-011/Q-004 WX P2-path-via-#64007, G-014/Q-006 AK5704 `$10`+16-step DAC. Motor 9/8 silk-corrected (source OCR). |
| v1.11.2 | 2026-06-25 | **CORDIC rotation, COGINIT, and LSTRING accuracy.** QROTATE operand mapping corrected (X from D, Y from SETQ, angle from S, results via GETQX/GETQY) data-set-wide — `architecture/cordic.yaml` `rotate` + `rotation_matrix` and the `pasm2/pi.yaml` examples (F-166). COGINIT load size 496→504 longs ($000..$1F7) (F-167). LSTRING `{Spin2_v43}` version gate documented, pnut-ts-proven (F-168). Drains the DeSilva-tutorial release-gate. |
| v1.11.1 | 2026-06-25 | PASM2 reference accuracy: GETBRK per-flag-effect reference, the program counter (CALLD/CALL return address), and signed ADD/SUB C-flag semantics. |
| v1.11.0 | 2026-06-24 | **Eval-header board model + Assembly gate-drain.** Standardized all 10 eval-header boards to one self-contained shape (`pin_group.size` 8/16 + offset→signal `signal_map` + direction + `actual = base + offset`); authored the HyperRAM/HyperFlash board (#64004-ES); folded HUB75 onto the shape; removed 4 fabricated orphan boards; one `eval_addon_boards` category. Added the RDLUT/WRLUT immediate-address contract (F-161); removed the unsourced `pin_efficiency` metric (F-160); fixed the goertzel ultrasonic-as-pinout fabrication (F-162). Drains the Assembly manual's YAML-HEAD gate. |
| v1.10.1 | 2026-06-20 | Smart Pin reference depth and language accuracy (internal-consistency batch F-141…F-158 + Silicon-backed smart-pin additions G-001/002/003). |
| v1.10.0 | 2026-06-18 | DEBUG feed idioms + smart-pin sequencing (universal Reset→Setup→Enable→Operate order). |
| v1.9.1 | 2026-06-14 | DEBUG display directive accuracy (CLOSE, SIZE, legacy debug.yaml). |
| v1.9.0 | 2026-06-13 | Smart-pin & DEBUG accuracy + hardware findability (aliases + categories). |

## Eval-header board model (the base + offset convention)

Every P2 Eval add-on board plugs into one of the Eval Board's **8-pin accessory
headers** (or, for 16-pin boards, two adjacent headers). A board never owns fixed
P2 pins — it defines its functions by **offset** within its pin group, and the
user chooses which header it occupies. So:

> **`actual_P2_pin = base_pin + offset`** — `base_pin` is the first pin of the
> chosen group (8-pin: 0, 8, 16, 24, 32, 40, 48, 56; 16-pin: 0, 16, 32, 48).

Each board YAML is self-contained and carries this directly: `eval_header_occupant:
true`, `pin_group.size` (8 or 16), and a `signal_map` of `{offset, signal,
direction, notes}`. **Direction** is the P2-side role (out/in/bidir), stated only
where the source documents it. The browse-time answer to *"what eval boards do we
know about?"* is the `eval_addon_boards` category (10 boards).

## Known-hardware inventory

### Eval-header occupants (`eval_addon_boards` category)

| Part # | Board | Pins | Status |
|--------|-------|------|--------|
| 64006A | Control (4 LEDs + 4 buttons) | 8 | active |
| 64006B | Serial Host (twin USB-A) | 8 | active |
| 64006C | LED Matrix (8×7 Charlieplex, 56 LEDs) | 8 | active |
| 64006D | Digital Video Out (HDMI-type TMDS) | 8 | active |
| 64006E | Mini Prototyping (8×12 grid) | 8 | active |
| 64006F | Serial Device (twin microUSB) | 8 | active |
| 64006G | Goertzel / Touch (compass + switch pads) | 8 | active |
| 64006H | A/V Breakout (VGA + RCA + audio) | 8 | active |
| 64032 | HUB75 Adapter (RGB LED panel) | 16 | retiring (limited stock) |
| 64004-ES | HyperRAM + HyperFlash (16 MB + 32 MB) | 16 | limited edition |

### Host boards, modules, carriers & reference

| File | Kind |
|------|------|
| p2-eval-board | Host eval board (64000) |
| edge-standard-module · edge-32mb-module | Edge CPU modules |
| edge-breadboard-carrier · edge-mini-breakout · edge-standard-breakout | Edge carriers/breakouts |
| hardware-compatibility-matrix · p2-hardware-feature-comparison · p2-hardware-selection-guide · p1_rom_font_character_set | Reference data |

> Inventory and categories are kept 1:1 with the served files — adding or removing
> a board updates the file, `engineering/tools/p2kb-categories.json`, and this
> table together, and the regenerated index is asserted to match.
