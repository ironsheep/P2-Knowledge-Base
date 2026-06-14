# P2KB Correction Findings — Consolidated Register

**Purpose:** A single, append-only register of everything we discover that is **wrong or needs correction** — primarily in the P2 Knowledge Base YAML (`deliverables/ai/P2/`), but also any other source/content correctness issue worth tracking. This is the hand-off document for the agent that corrects the P2KB (via the `yaml-knowledge-base-maintenance` skill).

**How to use this register:**
- When any work (manual production, audits, example compilation, ingestion) surfaces something incorrect, **add it here** — do not leave it only in a per-manual note.
- Each finding gets: an ID, a status, the exact location, what's wrong, the evidence, and the proposed correction.
- **Annotate as you fix, same pass** — flip the status, add an applied-note + source trace, and log any newly-surfaced defects as new findings. See `yaml-knowledge-base-maintenance` skill §4.5. A stale register (statuses lagging the YAML) lies and invites re-chasing.

**Status legend:** `CONFIRMED` (verified against an authority; ready to fix) · `NEEDS-VERIFICATION` (suspected; must be checked before acting) · `DONE` (corrected + verified) · `WONTFIX` (investigated, not a defect) · `RESOLVED-INVALID` (the reported defect does not exist) · `TRACKED → ingestion` (real, but the resolution lives in the ingestion head, not a YAML edit).

**Authority order for P2 language facts:** the `pnut_ts` compiler (ground truth for what compiles) → the Spin2 v51 documentation (`engineering/ingestion/sources/spin2-v51/`) → the Silicon Doc. The KB YAML must match these.

**Next finding ID: `F-135`**

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
