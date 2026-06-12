# P2KB Correction Findings — Consolidated Register

**Purpose:** A single, append-only register of everything we discover that is **wrong or needs correction** — primarily in the P2 Knowledge Base YAML (`deliverables/ai/P2/`), but also any other source/content correctness issue worth tracking. This is the hand-off document for the agent that corrects the P2KB (via the `yaml-knowledge-base-maintenance` skill).

**How to use this register:**
- When any work (manual production, audits, example compilation, ingestion) surfaces something incorrect, **add it here** — do not leave it only in a per-manual note.
- Each finding gets: an ID, a status, the exact location, what's wrong, the evidence, and the proposed correction.
- The correction agent works the **CONFIRMED** items first, verifying each against the cited authority (compiler / Spin2 v51 spec / Silicon Doc) before editing, then marks them DONE.

**Status legend:** `CONFIRMED` (verified against an authority; ready to fix) · `NEEDS-VERIFICATION` (suspected; must be checked before acting) · `DONE` (corrected + verified) · `WONTFIX` (investigated, not a defect).

**Authority order for P2 language facts:** the `pnut_ts` compiler (ground truth for what compiles) → the Spin2 v51 documentation (`engineering/ingestion/sources/spin2-v51/`) → the Silicon Doc. The KB YAML must match these.

---

## P2KB YAML corrections

### F-001 — `QSIN` / `QCOS` have the wrong signature  ·  `DONE` (2026-05-31)

**Files:**
- `deliverables/ai/P2/language/spin2/methods/qsin.yaml`
- `deliverables/ai/P2/language/spin2/methods/qcos.yaml`

**What's wrong:** Both document a **2-argument** signature with the wrong order and a wrong angle-unit model:
- `qsin.yaml` line 6: `syntax: "sine := QSIN(Angle, Length)"`, parameters `Angle` then `Length`, with notes claiming "Angle in P2 angle units (0..$FFFFFFFF = 0..360°)" and "Result = Length × sin(Angle)". Examples use the 2-arg form, e.g. `QSIN($1555_5555, 1000)`.
- `qcos.yaml` mirrors the same error.

**Correct form (verified):** `QSIN(length, step, stepsInCircle) : y` — **three** arguments:
- `length` — the radius / amplitude (output scale)
- `step` — the angle, expressed in units where a full circle = `stepsInCircle`
- `stepsInCircle` — the number of steps in a full revolution (lets the caller choose angle units; it is *not* fixed at `$FFFFFFFF = 360°`)
- returns `y = length × sin(2π · step / stepsInCircle)`

`QCOS(length, step, stepsInCircle) : x` is the cosine counterpart.

**Evidence:**
- Spin2 v51 spec, `engineering/ingestion/sources/spin2-v51/spin2-text.txt:5141–5148`: `QSIN(length, step, stepsInCircle) : y` and `QCOS(length, step, stepsInCircle) : x`. Worked examples in the same source: `qsin(1000, af++, 200)`, `qsin(1000, j, 50_000)`.
- `pnut_ts` v1.55.0: the 3-arg form compiles; the KB 2-arg form fails with `error: Expected ","`.
- Discovered independently by three Debug Window Manual generation agents (SCOPE, SCOPE_XY, PLOT) when KB-form examples would not compile (2026-05-31).

**Proposed correction:** Rewrite both YAMLs' `syntax`, `parameters`, `returns`, `notes`, and `examples` to the 3-argument `(length, step, stepsInCircle)` form. Fix the angle-unit explanation (units are caller-defined via `stepsInCircle`, not a fixed `$FFFFFFFF`). Check `related` CORDIC method/concept files (`rotxy.yaml`, `polxy.yaml`, `xypol.yaml`, `cordic_solver.yaml`) for the same angle-unit confusion while in the area.

---

### F-003 — `streamer_smartpin_control.yaml` still describes XZERO as "stream zeros"  ·  `DONE` (2026-05-31)

**File:** `deliverables/ai/P2/language/pasm2/concepts/streamer_smartpin_control.yaml` (lines ~51–53)

**What's wrong:** It still says:
```yaml
XZERO:
  syntax: "XZERO mode, count"
  operation: "Stream zeros (no hub read)"
  use: "Generate timing/clocks"
```
XZERO does **not** stream zeros. It buffers a streamer command to execute on the next NCO rollover, **zeroing the NCO phase accumulator**. The KB now **contradicts itself** — the instruction YAML `pasm2/xzero.yaml` was corrected to "zeroing phase," but this *concepts* file was missed.

**Correct:**
```yaml
XZERO:
  syntax: "XZERO {#}D,{#}S"
  operation: "Buffer streamer command to execute on final NCO rollover, zeroing NCO phase"
  use: "Video line timing reset, phase alignment"
  note: "Does NOT stream zeros — zeros the NCO phase accumulator"
```

**Evidence:** Silicon Doc / Spin2 v51 streamer description; the already-corrected sibling `pasm2/xzero.yaml` ("Buffer new streamer command… zeroing phase. Unlike XCONT which continues phase…"). Surfaced 2026-05-31 while re-verifying the Jan-2026 streamer KB audit against the current (restructured) P2KB.

**Proposed correction:** Replace the XZERO block with the correct description; align it with `pasm2/xzero.yaml`.

---

### F-004 — Seven deliverables YAMLs carry stale cross-refs to a non-existent `engineering/knowledge-base/P2/` path  ·  `DONE` (2026-05-31)

**Files (7):** under `deliverables/ai/P2/` — locate with `grep -rl "engineering/knowledge-base/P2/" deliverables/ai/P2/`. Examples: `language/spin2/concepts/basic-io.yaml` (`related:` list), `guides/spin2-getting-started.yaml` (`content_base:`), `language/spin2/spin2-language-complete-map.yaml` (`language_root:` / `fundamentals_root:`).

**What's wrong:** These `related:`, `content_base:`, and `*_root:` values point into `engineering/knowledge-base/P2/…` — a path that **does not exist** (the transient tree has only `P1/` and `P2-support/`, never `P2/`). The referenced content now lives under `deliverables/ai/P2/…`. Pre-existing dangling references (Sacred Rule #7: never break a cross-ref — redirect it).

**Proposed correction:** Redirect each `engineering/knowledge-base/P2/<x>` reference to its current home under `deliverables/ai/P2/<x>` (or the correct relative path), then run the cross-ref validator. Independent of — but surfaced by — the `engineering/knowledge-base` wipe.

---

### F-005 — Debug-display KB YAMLs carry the same fabrications as the scrapped Debug Window v2 manual  ·  `DONE` (2026-05-31)

> **Hold lifted & fixed (2026-05-31).** The hold (pending a current-compiler debug source) was lifted when the user provided `…/p2-debug-window-manual/REF/DEBUG-WINDOW-DIRECTIVE-MATRIX.md` — a unified directive matrix **re-verified directly against PNut v55 `DebugDisplayUnit.pas`** with line references. All five YAMLs were fully re-grounded against it (+ `debug-section.txt` for the PC_KEY/PC_MOUSE P2-side API). PLOT = vector/raster canvas (no chart/series/stats/export); LOGIC = sample capture + mask/match TRIGGER (no protocol decoders); MIDI = piano keyboard, note-on/off velocity (no analysis/file I/O); `pc_key` = `PC_KEY(pointer_to_long)` + full key-code table; `pc_mouse` = `PC_MOUSE(pointer_to_7_longs)` + 7-long struct. DEBUG examples compile-verified with pnut_ts v1.55.0. Cross-refs 100%.

**Files:** `deliverables/ai/P2/language/spin2/debug-displays/{plot,logic,midi}.yaml`; `…/debug-commands/{pc_key,pc_mouse}.yaml`

**What's wrong:** Generated from the same pre-theory-of-operations understanding that produced the scrapped Debug Window Manual v2:
- `plot.yaml` — describes a non-existent line-charting/data-series API (`plot_types`, `axis_configuration`, `statistical_features`, `data_export`). Real PLOT is a vector canvas (DOT/LINE/CIRCLE/BOX/OVAL/OBOX/TEXT/SET/ORIGIN/COLOR/OPACITY/POLAR/CARTESIAN/PRECISE/SPRITEDEF/SPRITE/LAYER/CROP).
- `logic.yaml` — fabricated `protocol_decoders:` (I2C/SPI/UART/CAN/auto-baud) that do not exist; LOGIC is raw sample capture.
- `midi.yaml` — fabricated display-formats/analysis/MIDI-file import-export; real window is a piano keyboard only ($9n/$8n bytes).
- `pc_key.yaml`, `pc_mouse.yaml` — stubs (8 lines) missing the key-code table / 7-long mouse struct.

**Evidence:** `engineering/ingestion/sources/spin2-v51/debug-section.txt` + the per-window Bibles in `…/p2-debug-window-manual/REF/theory-of-operations/`. The identical fabrications were found and fixed in **Debug Window Manual v3** (2026-05-31).

**Proposed correction:** Re-ground these YAMLs in the theory-of-operations Bibles. The corrected chapters (`p2-debug-window-manual/opus-master/`) are a ready, verified source of the real command sets; expand `pc_key`/`pc_mouse` per Chapter 12 (`ch12-bidirectional.md`).

---

### F-006 — Silicon errata undocumented: SETQ/SETQ2 block transfer + intervening ALTx/AUGS/AUGD cancels the PTRx block delta  ·  `DONE` (2026-05-31)

**Files:** `deliverables/ai/P2/language/pasm2/concepts/setq_block_ops.yaml`, `setq.yaml`, `rdlong.yaml` (+ WRLONG/WMLONG)

**What's wrong:** None warn that an ALTx/AUGS/AUGD placed between SETQ/SETQ2 and a block RDLONG/WRLONG/WMLONG (PTRx expression) cancels the block-size PTRx delta — PTRx then advances only +4 instead of N×4. Active in Rev-C silicon (current).

**Evidence:** Silicon Doc v35 known-bugs (`engineering/ingestion/sources/silicon-doc/`).

**Proposed correction:** Add a `silicon_errata` note (don't interleave ALTx/AUGS/AUGD between SETQ and the block transfer; workaround = keep adjacent).

---

### F-007 — Silicon errata undocumented: AUGS/AUGD value applied to an intervening ALTx with immediate #S  ·  `DONE` (2026-05-31)

**Files:** `deliverables/ai/P2/language/pasm2/augs.yaml`, `augd.yaml` (+ `altd.yaml`/`alts.yaml` notes)

**What's wrong:** No warning that an ALTx with an immediate `#S` between AUGS/AUGD and the intended target uses the augment without cancelling it — both instructions get augmented. Rev-C silicon. Workaround: use a register (not `#S`) for the ALTx S operand.

**Evidence:** Silicon Doc v35 known-bugs.

**Proposed correction:** Add `silicon_errata` block to `augs.yaml`/`augd.yaml`.

---

### F-008 — `conditional_execution.yaml` missing 14 condition-code bit-pattern aliases  ·  `DONE` (2026-05-31)

**File:** `deliverables/ai/P2/language/pasm2/concepts/conditional_execution.yaml`

**What's wrong:** 14 of 15 condition codes omit valid aliases pnut_ts accepts (e.g. code 1 `IF_NC_AND_NZ` ← `IF_00`; code 6 ← `IF_Z_NE_C`; code 14 `IF_C_OR_Z` ← `IF_LE`, `IF_NOT_00`; etc.).

**Evidence:** `engineering/ingestion/sources/pnut-ts-pasm-ref/PASM2-Condition-Codes.json`. Full per-code list in the PASM2-audit harvest output.

**Proposed correction:** Add the missing `IF_##` / `IF_NOT_##` / `IF_Z_*_C` / `IF_LE` aliases to each code's `aliases:`.

---

### F-009 — BIT*/DIR*/DRV*/OUT*/FLT* instruction YAMLs wrongly say C = "No effect"  ·  `DONE` (2026-05-31)

**Files (~28–35):** non-RND variants of `bit*.yaml`, `dir*.yaml`, `drv*.yaml`, `out*.yaml`, `flt*.yaml` (e.g. `bith`, `dirc`, `drvh`, `outc`, `fltl`).

**What's wrong:** Each has `flags_affected: C: No effect`. Authoritative CSV (`P2 Instructions v35 - Rev B_C Silicon`) specifies `C,Z = [original target bit state]` with `{WCZ}`. The RND variants were already fixed; the rest were missed.

**Proposed correction:** Set C to the original bit state per family (BIT: `D[S[4:0]]`; DIR: DIR bit; DRV/OUT/FLT: OUT bit) when WC/WCZ specified — mirror the already-correct RND variant in each family.

---

### F-010 — `cog_hub_execution.yaml` `common_mistakes` contradicts the file's own corrected content  ·  `DONE` (2026-05-31)

**File:** `deliverables/ai/P2/language/pasm2/concepts/cog_hub_execution.yaml` (lines ~517–523)

**What's wrong:** The `common_mistakes` entry says "Using REP in hubexec … Won't work!" — contradicting lines 32–40/98/122 of the same file, which correctly state REP works in hubexec (Silicon Doc v35) at ~13+ clocks/iteration. Stale entry never updated.

**Proposed correction:** Replace with: REP works in hubexec but each iteration pays the hub-branch refill (~13+ clocks); use cogexec only when zero-overhead looping is needed.

---

### F-011 — Flash-Loader update-request leftovers  ·  `DONE` (2026-05-31; item B done, item A closed-by-crossref)

The May-2026 Flash-Loader requests are ~95% applied (RCFAST request 100% applied). Two small items remained — **both now resolved (2026-05-31, decisions locked):**
- **Item A — `language/pasm2/hubset.yaml` inline `halt_technique:` block → CLOSED, resolved-by-cross-ref (will NOT inline).** The halt-by-dead-clock technique is already fully documented in `idioms/halt-and-fault-response.yaml` and `hubset.yaml` already cross-links it (`related:` + explanatory comment, lines ~129–132). Inlining would duplicate a fact across two files and invite drift — counter to the single-source-of-truth/hard-facts discipline. The original "prefer inline" request is superseded by the now-mature idiom file. **Do not revisit.**
- **Item B — `language/pasm2/idioms/_index.yaml` → DO (this pass).** The `idioms/` folder has 9 idiom files but no index; an established `_index.yaml` pattern exists (`architecture/streamer/_index.yaml`, `boot-rom/_index.yaml`). Add a discovery/compendium index mirroring that pattern. Purely additive, aids discovery + the index generator.

---

### F-012 — KB does not document I/O pin input-voltage limits / protection (e.g. reading a 5 V signal)  ·  `DONE` (2026-05-31)

**Files:** no current home documents it. Natural home: `deliverables/ai/P2/architecture/io_pin_timing.yaml` (already holds the VIO electricals — input thresholds, VIO range) — add an `absolute_maximum_ratings` / `input_voltage_tolerance` section. Cross-ref from `architecture/smart_pins.yaml` and a hardware guide.

**What's wrong (gap, not error):** Nothing in the KB tells a consumer what voltage a P2 pin may safely see, how the on-chip pin protection works, or whether/how a 5 V signal can be read. `io_pin_timing.yaml` gives input thresholds (1.65 V typ at 3.3 V VIO) and a 1.8–3.3 V VIO operating range, but no absolute-max voltage, no protection-diode behavior, no current limit. This is safety-relevant and frequently asked.

**Root-verified facts (P2 datasheet — a golden ingestion source):**
- **Voltage on any I/O pin (abs-max):** `-0.3 V to (Vxxyy + 0.3 V)` — i.e. ≈ **3.6 V** at the nominal 3.3 V I/O supply. Direct 5 V exceeds this.
- **Each I/O pin has an internal protection diode** to the I/O supply rail (the "+0.3 V" is its forward drop).
- **Datasheet note (verbatim):** *"I/O pin voltages in respect to GND may be exceeded if the internal protection diode forward bias current is not exceeded."* → Over-voltage is tolerated **only** while the clamp current stays within limit.
- **Max DC current into an input pin with the internal protection diode forward-biased: ±10 mA.**
- Max allowable current per I/O pin: ±30 mA. ESD: 4 kV HBM (JS-001), 1 kV CDM (JS-002).
- Silicon Doc corroborates the rails (I/O = Vxxyy/VIO = 3.3 V; pins 0–3.3 V) and notes VIO-triggered latch-up onset ~4.3 V — reinforcing that the part is a 3.3 V I/O device, **not** natively 5 V-tolerant.

**Answer to "can the P2 read a 5 V signal?":** Not by direct connection — 5 V exceeds the 3.6 V pin abs-max and forward-biases the upper protection diode. It **is** permissible *if* a series resistor limits the protection-diode forward current to ≤ ±10 mA (the datasheet explicitly blesses exceeding pin voltage under that condition). Minimum series resistance is a **deterministic derivation** from stated facts (Ohm's law): R ≥ (5 V − ~3.6 V) / 10 mA ≈ 140 Ω (use a larger, standard value, e.g. ≥ 1 kΩ, for margin). The hard facts are the abs-max, the diode, and the ±10 mA limit; present the resistor value as derived, not as a datasheet number.

**Evidence:** `engineering/ingestion/sources/p2-datasheet/p2-datasheet-narrative.txt:6185–6241` (Absolute Maximum Ratings table + footnote 1) and `:6204` (`-0.3 V to (Vxxyy + 0.3 V)`), `:6222–6224` (±10 mA protection-diode limit), `:6240–6241` (footnote). Cross: `p2-datasheet/p2-datasheet-cross-source-analysis.md:103` (`Input voltage: -0.3 to VIO+0.3V`); `silicon-doc/silicon-doc-v35-facts-only.md:22,29` (VIO=3.3 V, pins 0–3.3 V); `silicon-doc/p2-documentation.txt:155–175` (latch-up/ESD context).

**Proposed correction:** Add an `absolute_maximum_ratings` + `input_voltage_and_protection` section to `io_pin_timing.yaml` carrying the abs-max voltage, the protection-diode + ±10 mA fact, the verbatim datasheet footnote, and a short "reading >3.6 V (e.g. 5 V) requires a series resistor sized to keep diode current ≤ ±10 mA" note (with the derivation shown). Cite the datasheet. Not debug-related → eligible for this fix pass.

---

### F-013 — `setq_block_ops.yaml` `augmented_operations` block is internally contradictory / likely fabricated  ·  `DONE` (2026-05-31)

> **Resolved (2026-05-31).** Verified against Silicon Doc: cog and LUT are each **512 longs** (`p2-documentation.txt:394-395, 854, 966`) and FAST BLOCK MOVES (`:7169-7185`) targets cog/LUT RAM, so a block transfer cannot exceed 512 longs — the "1001 longs" claim is physically impossible, and no "AUGD alternate block modes" feature exists in any source. Replaced the fabricated `augmented_operations` block with `full_width_q_value`: SETQ Q can be a full 32-bit value (via register or ## for MUXQ mask / SETQ+COGINIT PTRA/PTRB), but the block-move COUNT is capped at 512. Cited.


**File:** `deliverables/ai/P2/language/pasm2/concepts/setq_block_ops.yaml` (the `special_operations.augmented_operations` block, ~lines 209–219 pre-F-006; shifted by the F-006 insert)

**What's suspect:**
- `with_AUGS: "AUGS + SETQ for 32-bit counts"` with example `RDLONG 0, hub_ptr ' Read 1001 longs` — **contradicts the same file's `limitations: "Maximum 512 longs per operation"`.** SETQ is a 9-bit value (0–511 → 1–512 longs). Whether AUGS extends the SETQ count beyond 512 is unverified and looks wrong.
- `with_AUGD: description "AUGD + SETQ for special modes" / operation "Enables alternate block modes"` — vague capability claim ("enables", "alternate modes"), a red-flag fabrication pattern, no cited source.

**Why not fixed now:** No golden source was consulted for what AUGS/AUGD-before-SETQ actually does. Per the hard-facts rule, do not edit (or delete) without root verification. Surfaced 2026-05-31 during the F-006 edit.

**Proposed action:** Verify against the Silicon Doc SETQ/AUGS/AUGD descriptions + `pnut_ts`. If unsupported, correct the count claim to respect the 512-long max and remove/repair the `with_AUGD` "special modes" claim. Note the SETQ/SETQ2 block + intervening-AUGS/AUGD interaction is now governed by the F-006 `silicon_errata` block in the same file — reconcile the two.

---

### F-014 — Unverifiable Spin2-method "38 clock cycles" timing on CORDIC methods  ·  `DONE` (2026-05-31)

**Files (7):** `language/spin2/methods/{qsin,qcos,rotxy,polxy,xypol,qlog,qexp}.yaml`

**What was wrong:** Each asserted `timing: cycles: "38 clock cycles"` (plus a notes bullet "38-clock cycle operation") for a **Spin2 method**. Per the project rule we do not publish bytecode-interpreter clock timings for Spin2 methods — we have no verifiable measurement; cite the underlying PASM/CORDIC or remove the field. (Surfaced 2026-05-31 during the F-001 QSIN/QCOS rewrite.)

**Fix applied:** Removed the unverifiable cycle count and the notes bullet; replaced the `timing:` block with a CORDIC-engine reference (latency is a hardware property; total method time includes interpreter overhead, not separately specified) pointing to `concepts/cordic_solver.yaml`. All 7 files re-validated (parse OK).

---

### F-015 — `rotxy.yaml` CORDIC K-factor note contradicts its own example  ·  `DONE` (2026-05-31)

> **Resolved (2026-05-31).** Verified against Silicon Doc: the P2's 32-bit CORDIC solver is "pipelined CORDIC solver **with scale-factor correction**" (`p2-documentation.txt:425`), so QROTATE-based results (ROTXY/POLXY/XYPOL/QSIN/QCOS) are NOT scaled by the CORDIC gain — the example (45°: 100→71,71, no gain) was correct. The "~1.646" scaling (`:4779`) belongs to the streamer's **separate 5-stage modulator CORDIC**, not the solver. Replaced the false "scaled by CORDIC K factor (~1.647)" note in `rotxy.yaml`, `xypol.yaml`, `polxy.yaml` with the correct scale-factor-correction statement. Cited.


**File:** `deliverables/ai/P2/language/spin2/methods/rotxy.yaml` (note ~line 44 "Result is scaled by CORDIC K factor (≈1.647)")

**What's suspect:** The note claims ROTXY results are "scaled by CORDIC K factor (≈1.647)", but the file's own example rotates (100,0) by 45° and gives x2,y2 ≈ 71,71 — the *ideal* (100·cos45 ≈ 70.7) with **no** visible 1.647 gain. The two cannot both be true as written. POLXY/QSIN/QCOS may carry the same K-factor claim.

**Why not fixed now:** Resolving whether the P2 CORDIC applies (or pre-compensates) the K gain for QROTATE-based ops requires a golden source (Silicon Doc CORDIC section / hardware). Per the hard-facts rule, do not edit blind. Surfaced 2026-05-31.

**Proposed action:** Verify CORDIC rotation gain behavior in the Silicon Doc. Then either correct the example or the K-factor note (whichever the source contradicts), and sweep the same claim across the CORDIC method YAMLs.

---

## Root-source verification (2026-05-31)

Every confirmed finding was audited against the **golden ingestion sources** (`engineering/ingestion/sources/` — our source of trust), with exact citations, so each correction is justified at root before any YAML is edited.

| Finding | Golden source — exact citation | Root-verified true value |
|---|---|---|
| **F-001** | `spin2-v51/spin2-text.txt:5141–5148` + `pnut_ts` compiler | `QSIN(length, step, stepsInCircle)` (3-arg) |
| **F-003** | `silicon-doc/p2-documentation.txt:2743` (summary "…zeroing phase") + `:3508–3519` ("XZERO clears out the phase accumulator when it executes") | XZERO buffers a command on final NCO rollover, **zeroing the NCO phase** — it does NOT "stream zeros" |
| **F-005** | `spin2-v51/debug-section.txt` — PLOT `:2626–3002`, LOGIC `:1660–1820`, MIDI `:3915–4012`, PC_KEY `:784–813`, PC_MOUSE `:815–852` | PLOT = vector canvas (DOT/LINE/CIRCLE/…/SPRITE/LAYER/CROP), no chart/series API; LOGIC = mask/match trigger only, **no protocol decoders**; MIDI = piano keyboard, $9n/$8n only; PC_KEY = 33-code table + pointer/"must be last"/focus; PC_MOUSE = 7-long struct (xpos,ypos,wheel,l,m,r,pixel) |
| **F-006** | `silicon-doc/p2-documentation.txt:197–211` (KNOWN BUGS, Rev C, 2020_06_01) — verbatim | ALTx/AUGS/AUGD between SETQ/SETQ2 and a PTRx block transfer cancels the block-size PTRx delta (PTRx += 4, not N×4) |
| **F-007** | `silicon-doc/p2-documentation.txt:212–227` (KNOWN BUGS, Rev C) — verbatim | ALTx with immediate `#S` between AUGS and its target is also augmented. **Doc names AUGS only** (see refinement) |
| **F-008** | `pnut-ts-pasm-ref/PASM2-Condition-Codes.json` (compiler-extracted) + CSV rows 411–460 | full per-code alias roster (IF_##, IF_NOT_##, IF_Z_*_C, IF_LE, …) |
| **F-009** | `p2-instructions-csv/…Rev B_C Silicon - Sheet1.csv` — BITx rows 43–50 `C,Z = original D[S[4:0]]`; DIRx 350–357 `C,Z = DIR bit`; OUT/FLT/DRV 358–381 `C,Z = OUT bit` | `C,Z = original target bit` (BOTH flags) |
| **F-010** | `silicon-doc/p2-documentation.txt:1733` ("REP works in hub memory, as well, but executes a hidden jump…") | REP works in hubexec (pays the hidden-jump / FIFO-refill cost per iteration) |

F-001 (compiler + v51), F-004 (mechanical path-redirect), and F-011 (`flash_loader.spin2` ROM source) were already root-grounded.

**Refinements surfaced by the audit (apply during the fix):**
- **F-007 scope:** the Silicon Doc names only **AUGS** in this errata — AUGD is a same-mechanism *inference*, not verbatim-stated. Document AUGS as confirmed; mark AUGD as inferred (or verify separately) — do not over-claim.
- **F-008 also a misplacement, not only a gap:** the KB lists `IF_BE`/`IF_LE` under `%1011` (`IF_NC_OR_Z`); the golden source places them under `%1110` (`IF_C_OR_Z`). Move them, in addition to adding the missing aliases.
- **F-009 is C *and* Z:** the CSV gives `C,Z = <bit>` (both flags), and the `encoding[].c`/`.z` fields are currently `—`. Fix Z and the encoding fields too, not just `flags_affected.C`.

---

## Verified resolved (recorded so we don't re-chase)

The **Jan-2026 streamer KB audit** (`manuals/p2-streamer-programming-guide/yaml-knowledge-base-audit.md`) listed 7 issues. Re-verified against the current (restructured) P2KB on **2026-05-31** — all but one are FIXED:

| Audit finding | Current state | Verdict |
|---|---|---|
| DAC mapping wrong (old `architecture/streamer.yaml`) | now `architecture/streamer/dac-routing.yaml` — full 16-entry `X_DACS_*` table | ✅ RESOLVED |
| Pin groups 8-pin | `streamer/pin-selection.yaml` — 32-pin blocks (`%000`=31..0 …) | ✅ RESOLVED |
| Mode encoding | `streamer/modes-reference.yaml` — `mode_field: D[31:28]` | ✅ RESOLVED |
| `pasm2/xcont.yaml` typo/sparse | "continuing phase" + examples | ✅ RESOLVED |
| `pasm2/xzero.yaml` typo/sparse | "zeroing phase" + examples | ✅ RESOLVED |
| `pasm2/setxfrq.yaml` no formula | "freq = (D × clkfreq) / 2³²" + SETQ + examples | ✅ RESOLVED |
| symbols "85 claimed, ~8 defined" | new `symbols/streamer-symbols.yaml`, 60+ symbols | ✅ RESOLVED |
| concepts XZERO "stream zeros" | **still wrong** → see **F-003** | ❌ OPEN |

The streamer audit's *enhancement* suggestions (setxfrq common-value table, extra examples, the symbol-value reference) remain in that audit doc — worth a later pass for residual gaps, but they are gaps, not correctness errors.

---

## Streamer audit — 2026-06-01 (Streamer Programming Guide production pass)

These six findings were surfaced while auditing the **P2 Streamer Programming Guide** for production. The *manual* was corrected in the same pass (`manuals/p2-streamer-programming-guide/opus-master/streamer-body.md`); the **KB YAML** items below are staged here for a separate `yaml-knowledge-base-maintenance` pass, per the standing instruction to finish the PDF first. Full audit: `manuals/p2-streamer-programming-guide/audit/streamer-content-audit-2026-06-01.md`.

### F-016 — `setxfrq.yaml` streamer-frequency formula is off by a factor of 2  ·  `CONFIRMED` (reopens a previously "RESOLVED" item)

**File:** `deliverables/ai/P2/language/pasm2/setxfrq.yaml`

**What's wrong:** The formula recorded as resolved (see line ~264 of this register) is `frequency = (D × clkfreq) / 2³²`. The streamer NCO masks its MSB before each add (`phase = (phase & $7FFF_FFFF) + frequency`), so it accumulates **modulo 2³¹**, not 2³². The correct relation is:

```
D = target_rate × 2³¹ / clkfreq      (i.e. D = $8000_0000 × rate/clk)
```

The `/2³²` form yields **double** the correct word for every rate.

**Evidence:**
- Silicon Doc v35 facts (`engineering/ingestion/sources/silicon-doc/silicon-doc-v35-facts-only.md:339`): `Phase = (phase & $7FFF_FFFF) + frequency` → mod-2³¹ accumulator; `$8000_0000` (=2³¹) rolls over every clock (1:1), exactly as the mode tables show.
- Silicon Doc HDMI/TMDS example (same file, ~line 436): the 1:10 ratio uses `$0CCCCCCC+1 = $0CCCCCCD`. `round(2³¹/10) = $0CCCCCCD` ✓; `round(2³²/10) = $1999999A` ✗ (that is the 1:5 value).
- **Primary-source confirmation (decisive):** Silicon Doc v35 SETXFRQ description (`engineering/ingestion/sources/silicon-doc/p2-documentation.txt:2753`): "D/# expresses a fractional 0-to-1 multiplier for the system clock, **which value must be multiplied by `$8000_0000`**." That is 2³¹, explicitly — the `setxfrq.yaml` `/2³²` form is wrong beyond doubt.
- The streamer guide's NCO common-values table (independently verified): `$8000_0000`=1:1, `$4000_0000`=1:2, `$0CCC_CCCD`=1:10 — all consistent with 2³¹, none with 2³².

**Proposed correction:** Change the `setxfrq.yaml` formula to the 2³¹ form above and re-check any worked example values it carries. Reconcile with `nco-timing.yaml` (which already uses the `$8000_0000 × rate/clk` convention).

### F-017 — `nco-timing.yaml` video pixel-rate table values are arithmetically wrong  ·  `CONFIRMED`

**File:** `deliverables/ai/P2/architecture/streamer/nco-timing.yaml` (`video_rates` section)

**What's wrong:** The hex NCO words do not equal `round(2³¹ × rate/clk)` for the stated rates; several cells are off by a whole ratio step (e.g. 800×600 @250 MHz is listed as the 50 MHz value `$1999_999A` instead of the 40 MHz value `$147A_E148`). The manual had copied these verbatim and they are now corrected in the manual; the KB still carries the errors.

**Correct values (`round($8000_0000 × rate/clk)`):**

| Rate | @250 MHz | @300 MHz | @320 MHz |
|------|----------|----------|----------|
| 640×480 (25.175) | `$0CE3_BCD3` | `$0ABD_C805` | `$0A11_EB85` |
| 800×600 (40.0)   | `$147A_E148` | `$1111_1111` | `$1000_0000` |
| 1024×768 (65.0)  | `$2147_AE14` | `$1BBB_BBBC` | `$1A00_0000` |
| 1280×720 (74.25) | `$2604_1893` | `$1FAE_147B` | `$1DB3_3333` |

**Evidence:** Direct computation (Python), cross-checked against the corrected manual Appendix C. Same root cause as F-016 (2³¹ scaling).

**Proposed correction:** Replace `nco-timing.yaml video_rates` with the values above.

### F-018 — `modes-reference.yaml` mislabels the SINC2 select bit  ·  `CONFIRMED`

**File:** `deliverables/ai/P2/architecture/streamer/modes-reference.yaml` (X_DDS_GOERTZEL_SINC2 entry)

**What's wrong:** SINC2 is given `d_19_16: "%1000_0111"` — an 8-bit value in a 4-bit (D[19:16]) field. SINC1 vs SINC2 is actually selected by **D[23]**, not a D[19:16] bit. The authoritative symbol value `X_DDS_GOERTZEL_SINC2 = $F087_0000` has D[23]=1 and D[19:16]=`%0111` (same `%0111` as SINC1 `$F007_0000`); the two differ only in bit 23.

**Evidence:** Silicon Doc v35 facts (`silicon-doc-v35-facts-only.md:416`): "### SINC Modes (D[23])". The streamer-symbols values ($F007 vs $F087) agree with D[23].

**Proposed correction:** In `modes-reference.yaml`, change SINC2's `d_19_16` to indicate `%0111 with D[23]=1 (SINC2 select)`. (The manual's Appendix A was corrected the same way.)

### F-019 — `dds-goertzel.yaml` carries two unsourced specifics  ·  `RESOLVED` (2026-06-03 verification — split outcome)

**File:** `deliverables/ai/P2/architecture/streamer/dds-goertzel.yaml`

**What's wrong (suspected):** Two values appear in the KB (and were inherited by the manual draft) but are **not** in the Silicon Doc v35 facts extract:
1. "DDS/Goertzel uses a **33-bit** frequency calculation internally" — inconsistent with the `$1_0000_0000` (2³²) multiplier in the very same frequency formula.
2. "SINC2 max amplitude **±10**" — no source found for the specific figure.

The manual was softened (dropped "33-bit", replaced "±10" with "well below ±127") pending verification.

**Evidence/needed:** Check the full Silicon Doc v35 (PDF parts, not just the facts extract) for the DDS/Goertzel section. If unsupported, drop "33-bit" (the formula is 2³²) and the "±10" figure from `dds-goertzel.yaml`.

> **Resolved (2026-06-03 verification pass)** — the two suspects split:
> - **"33-bit" → DROP (CONFIRMED unsourced).** The only "33-bit" in the Silicon Doc is the smart-pin Z-result bus (`p2-documentation.txt:7567`) — unrelated. The Goertzel NCO frequency is set by SETXFRQ (the canonical Goertzel example does `setxfrq freq`, `:4185`), which is 2³¹-scaled (see F-016 / F-022), not "33-bit". Remove the gloss.
> - **"±10" → KEEP + CITE (suspicion REFUTED).** The Silicon Doc's own Goertzel example sets `ampl = sinc2 ? 10 : 127` (`:4161`, comment "small sin/cos amplitude for SINC2", `:4167`). ±10 for SINC2 / ±127 for SINC1 is correct and now citable — do NOT drop it; the manual's softened "well below ±127" can be tightened back to the canonical 10.

### F-020 — `nco-timing.yaml` "31-bit phase" gloss is misleading  ·  `CONFIRMED` (minor)

**File:** `deliverables/ai/P2/architecture/streamer/nco-timing.yaml` (hardware note)

**What's wrong:** A note characterizes the NCO as using "31 bits for phase accumulation," which reads as a 31-bit accumulator. The register is **32-bit**; its MSB is masked before each add and serves as the rollover flag, so 31 bits hold the accumulating phase and resolution is `clkfreq/2³¹`. Stating "31-bit accumulator" bare contradicts the Silicon Doc's "32-bit phase accumulator."

**Evidence:** Silicon Doc v35 facts `:338` ("32-bit phase accumulator") and `:339` (the MSB-mask formula).

**Proposed correction:** Reword to "32-bit accumulator; MSB masked each add as the rollover flag; resolution `clkfreq/2³¹`." (Manual §3.1 corrected this way.)

### F-021 — `modes-reference.yaml` is missing several valid mode rows  ·  `DONE` (2026-06-03; see applied-note below)

**File:** `deliverables/ai/P2/architecture/streamer/modes-reference.yaml`

**What's wrong (suspected):** The complete mode table omits rows that exist in `streamer-symbols.yaml` and that the manual lists, e.g. `X_RFWORD_16P_4DAC4`, `X_RFWORD_16P_2DAC8`, `X_RFLONG_32P_4DAC8`, `X_16P_4DAC4_WFWORD`, `X_16P_2DAC8_WFWORD`, `X_32P_4DAC8_WFLONG`, and the `X_IMM_4X8_*`/`X_IMM_2X16_*` immediate variants. The manual is *more complete* than this KB file.

**Evidence:** Cross-check `modes-reference.yaml` against `streamer-symbols.yaml` (authoritative values) and the corrected manual Appendix A.

**Proposed correction:** Backfill the missing rows in `modes-reference.yaml` from the symbol values.

---

## Source-verification pass — 2026-06-03 (streamer findings F-016..F-021)

All six open streamer findings were re-verified against the **golden ingestion sources** before any YAML edit, per the standing "confirmed ingestion-source confidence" rule. Outcomes:

| Finding | Verdict | Decisive source |
|---|---|---|
| **F-016** | CONFIRMED | `silicon-doc/p2-documentation.txt:2753-2754` verbatim: SETXFRQ D/# "must be multiplied by **$8000_0000**" (2³¹); multiplier table `:2781-2788` (1/2=$4000_0000 … 1/8=$1000_0000) all 2³¹. `setxfrq.yaml`'s `/2³²` formula + every example/common-value is 2× too large. (`nco-timing.yaml` already uses the correct 2³¹ form — KB was self-contradictory.) |
| **F-017** | CONFIRMED | All 12 proposed values verified = `round(2³¹ × rate/clk)` (Python). All 12 current `nco-timing.yaml video_rates` values wrong; several off by a whole ratio step (e.g. 800×600@250 carried the 50 MHz word $1999_999A). |
| **F-018** | CONFIRMED | `p2-documentation.txt:4100` "D[23] selects between SINC1 and SINC2"; symbols `X_DDS_GOERTZEL_SINC1=$F007_0000` vs `SINC2=$F087_0000` differ only in bit 23. `modes-reference.yaml` SINC2 `d_19_16:"%1000_0111"` (8 bits in a 4-bit field) → `%0111` + D[23]=1. |
| **F-019** | SPLIT | "33-bit" → DROP (unsourced); "±10" → KEEP+CITE (`:4161`). See updated F-019 above. |
| **F-020** | CONFIRMED | `silicon-doc-v35-facts-only.md:338` "32-bit phase accumulator" (+ `:339` MSB-mask). Reword `nco-timing.yaml` "uses 31 bits" / "resolution: 31 bits of phase" → 32-bit register, MSB masked each add as rollover flag, resolution `clkfreq/2³¹`. |
| **F-021** | CONFIRMED — **corrected list** | The finding's 6 named symbols (`X_RFWORD_16P_4DAC4`, `X_RFWORD_16P_2DAC8`, `X_RFLONG_32P_4DAC8`, `X_16P_4DAC4_WFWORD`, `X_16P_2DAC8_WFWORD`, `X_32P_4DAC8_WFLONG`) are **already present**. Programmatic diff shows **12** genuinely-missing rows: `X_IMM_4X8_4DAC2`/`_2DAC4`/`_1DAC8`, `X_IMM_2X16_4DAC4`/`_2DAC8`, `X_IMM_1X32_4DAC8`, `X_2P_1DAC2_WFBYTE`, `X_4P_2DAC2_WFBYTE`, `X_4P_1DAC4_WFBYTE`, `X_8P_4DAC2_WFBYTE`, `X_8P_2DAC4_WFBYTE`, `X_8P_1DAC8_WFBYTE`. All 12 trace to **`spin2-v51/streamer-events-symbols.txt`** + `complete-streamer-symbols.md` (primary source). |

> **APPLIED — 2026-06-03.** F-016, F-017, F-018, F-019 (split), F-020, F-021, and F-022 are **applied to the YAMLs and validated** — 4 files: `pasm2/setxfrq.yaml`, `streamer/nco-timing.yaml`, `streamer/modes-reference.yaml`, `streamer/dds-goertzel.yaml`. YAML format verify 4/4 clean; cross-ref validation 100% (0 unresolved). These are DONE; the per-finding `CONFIRMED` markers above are kept for history.

### F-022 — `dds-goertzel.yaml` Goertzel-frequency formula uses 2³² (should be 2³¹)  ·  `DONE` (2026-06-03; NEW — missed by the 2026-06-01 audit)

**File:** `deliverables/ai/P2/architecture/streamer/dds-goertzel.yaml` (`frequency.formula` ~L100 and the `qfrac ##40000, clkfreq` example ~L106-110)

**What's wrong:** `frequency = $1_0000_0000 * target_freq / clock_freq` (2³²) and the `qfrac target, clkfreq` example (which yields a 2³²-scaled word). DDS/Goertzel uses the **same streamer NCO**, configured with **SETXFRQ** — the Silicon Doc's canonical Goertzel example does exactly this (`p2-documentation.txt:4185` `setxfrq freq`), and SETXFRQ is 2³¹-scaled (F-016, `:2753`). So the Goertzel frequency word is 2³¹-scaled too; the 2³² formula/example are 2× too high — same root cause as F-016/F-017.

**Evidence:** `p2-documentation.txt:2753-2754` (SETXFRQ ×$8000_0000) + `:4185` (Goertzel example sets the NCO via `setxfrq`).

**Proposed correction:** Change the formula to `D = target_freq × $8000_0000 / clkfreq` and fix the example. Reconcile with F-016.

> **Minor (noted):** the Silicon Doc says the Goertzel bitstream multiplier is "an integer from **−3 to +3**" (`:4094`, sum of up to 3 selected ADC pins), whereas `dds-goertzel.yaml` shows only `m := ADC_bit ? +1 : -1`. Incomplete (correct for 1 pin) — **widened to −3..+3 in the 2026-06-03 pass.**

### F-023 — `setxfrq.yaml` SETQ+SETXFRQ "64-bit precision frequency" claim is unverified  ·  `DONE` (2026-06-10)

**File:** `deliverables/ai/P2/language/pasm2/setxfrq.yaml` (description ~L14-15, example 3 ~L44-49, `related_instructions` SETQ note)

**What's suspect:** The file states "For SETQ+SETXFRQ pattern, SETQ provides low 32 bits, D provides high 32 bits for 64-bit precision frequency control." The streamer NCO is a single 32-bit (31-bit-effective) phase accumulator — there is no 64-bit NCO frequency register, so a "64-bit precision" frequency word is dimensionally suspect. Not mentioned in the Silicon Doc v35 SETXFRQ section (`p2-documentation.txt:2753-2790`).

**Why not fixed now:** Surfaced 2026-06-03 during the F-016 scaling fix; left **verbatim** per the hard-facts rule (no golden source consulted on what SETQ-before-SETXFRQ actually does). The F-016 edit changed only the 2³¹/2³² scaling, not this claim.

**Proposed action:** Verify against the Silicon Doc / `pnut_ts` whether SETQ augments SETXFRQ at all. If unsupported, remove the 64-bit claim from the description, example 3, and the `related_instructions` SETQ note.

---

## Debug Window Manual production pass — 2026-06-08

### F-024 — Debug Window Manual: `SAVE` examples wrongly append `.bmp` to the filename argument  ·  `DONE` (2026-06-08)

**Location (manual content, not YAML):** `engineering/document-production/manuals/p2-debug-window-manual/opus-master/` — `ch05-plot.md:536`, `ch08-scope-xy.md:160` and `:166`, `ch14-multiwindow-pasm.md:230`.

**What was wrong:** Four `SAVE` examples wrote the filename with an explicit `.bmp` extension (`SAVE 'name.bmp'`, `` debug(`Lissajous SAVE 'figure.bmp') ``). The DEBUG-window `SAVE` directive **appends `.bmp` automatically**, so these would have produced `name.bmp.bmp` / `figure.bmp.bmp`. The manual was internally inconsistent — `ch09-fft.md` already showed the correct extension-less form (`SAVE 'spectrum'` → `spectrum.bmp`).

**Evidence (authority):** Spin2 v51 `engineering/ingestion/sources/spin2-v51/debug-section.txt` (repeated for every window type, e.g. lines 1802/1805): syntax is `SAVE {WINDOW} 'filename'` — "Save a bitmap file (.bmp) of either the entire window or just the display area." The argument is a bare `'filename'`; the `.bmp` is the command's output format, not part of the name.

**Correction applied:** Removed `.bmp` from all four `SAVE` arguments; added a canonical "extension is appended automatically — give the name without it" note at the definitional site (`ch01-foundation.md`) and short reminders at ch05/ch08. `LAYER`/`SPRITEDEF` *load* arguments (which name real files on the host, e.g. `LAYER 1 'background.bmp'`) were correctly left untouched. Distinct from the YAML KB — no `deliverables/ai/P2/` change.

**Related tooling opportunity (separate repo, not actioned here):** `pnut-term-ts` could defensively detect a trailing `.bmp` on a `SAVE` argument and avoid double-appending — a tolerance, not a substitute for the corrected docs.

---

### F-025 — Debug Window Manual: inner backtick before bare DEBUG-window commands  ·  `DONE` (2026-06-09)

**Location (manual content):** `opus-master/` — `ch03-term.md:199`, `ch04-bitmap.md:250/251/317/322`, `ch10-spectro.md:220/221/255`, `ch11-midi.md:156/188` (10 occurrences, 4 chapters).

**What was wrong:** A DEBUG-window display command was written with a spurious **inner backtick** — `` debug(`Plasma `CLEAR) ``, `` `UPDATE ``, `` `SAVE ``, and `` `SET(x, y) ``. A display command takes **no** backtick; the backtick introduces a runtime value/expression (`` `(expr) ``) or an output-format command (`` `udec_ ``). The inner-backtick-command form is a syntax error the moment the DEBUG stream is actually parsed.

**Evidence (authority):** `pnut-ts` v1.55.0 **with `-d`** (compile-with-DEBUG) rejects it: `error: Expected "?", ".", "(", "$", "%", "#", or DEBUG command`. The correct forms compile clean. Verified each fix under `-d`.

**Why it slipped through:** `pnut-ts` only parses the contents of `debug()` directives when invoked with **`-d`**; without it the directives are stripped, so a plain `pnut-ts <file>` compile reports success even with broken debug syntax. The earlier compile-cert pass did not use `-d`.

**Correction applied:** Removed the inner backtick (`` `CLEAR `` → `CLEAR`, etc.). For the runtime-coordinate case, `` `SET(x, y) `` → `` SET `(x, y) `` (command bare; coordinates as a runtime expression). `` `(expr) ``, `` `udec_ ``, and the leading display reference (`` debug(`Name ``) are correct and were left untouched.

**Process note (gate hardening):** the code compile-cert gate — in `prepare-manual` and for the `figure-generators/` — must run `pnut-ts -d` for DEBUG-window code, or directive errors go undetected.

---

## To investigate

### F-002 — `?` (RNG) and `||` (abs) operator forms failed to compile  ·  `WONTFIX` (agent usage error; KB is correct)

**Resolved 2026-05-31** against pnut_ts v1.55.0 + Spin2 v51 — the failures were an **agent usage error, not a KB defect**:
- **Abs:** `ABS x` / `ABS(value)` compiles; the symbolic `||x` does **not** compile in pnut_ts. The KB documents it correctly (`methods/abs.yaml`: `result := ABS(value)`).
- **Random:** `??variable` (XORO32) compiles and is documented correctly (`operators/op_rand.yaml`); v51 line 3700 confirms. The agents' `?x` fails because `?` is the **ternary** operator (`operators/op_question.yaml`), not a unary random.

No KB change required.

---

## Sources harvested — 2026-05-31 (re-verified against the current KB)

All four legacy sources were re-verified against the current `deliverables/ai/P2/` (the KB has moved on — most legacy items were already applied). Still-valid items are folded in above:

- `…/p2-debug-window-manual/studies/yaml-database-gaps-discovered.md` → **F-005** (6 still-missing, 4 resolved). Fix source = the manual's `REF/theory-of-operations/`.
- `…/pnut_ts_facts/Flash-Loader-P2KB-Update-Request.md` → **F-011** (2 minor pending, 21 applied); `…-RCFAST.md` → fully applied (0 pending).
- `…/p2-assembly-language-manual/audit/` (PART-I / HALLUCINATION / yaml-audit set) → **F-008, F-009, F-010** (3 KB-actionable, 12 resolved, ~30 manual-only and excluded).
- `…/silicon-doc/silicon-doc-v35-critical-findings.md` → **F-006, F-007** (2 safety-critical errata, 10 resolved).

---

*Created 2026-05-31. Append new findings above the "Sources to harvest" section. Keep each finding self-contained and evidence-backed — this register is only as trustworthy as its citations.*

## PASM2 Manual full-audit pass — 2026-06-10 (F-026..F-097)

These 72 KB-defect candidates were surfaced by the **PASM2 Assembly Language Manual full audit** (Stage A: 50 per-section auditors; Stage B: 208 per-finding adversarial verifiers using pnut-ts compiler probes + Silicon Doc + Spin2 v51). They are filed **NEEDS-VERIFICATION**: the manual-audit verification is strong but the YAML is our **primary source**, so each must be re-confirmed by a dedicated deep-research pass against primary authorities **before** editing — and some are expected to be refuted on deeper review. Full per-finding evidence (incl. the manual side) lives in the local (gitignored) `engineering/document-production/manuals/p2-assembly-language-manual/audit/full-audit-2026-06-10/` (`_ADJUDICATION-DETAIL.md`, `_CONSOLIDATED.json`).

**Root cause (why the KB carries these):** (A) the per-instruction PASM2 YAMLs were seeded from the 2022 Parallax *draft* manual + a PNUT_TS operand-integration pass and **never reconciled against the Silicon Doc** — so architecture-touching facts (HUBSET clock bit-fields, GETCT 64-bit counter, boot Prop_Hex, branch-into-hub timing) drifted; (B) **fabrications** concentrate in unattributed hand-authored concept/architecture files (`clock_system.yaml`, `serial_loader.yaml`, `debug-mask.yaml` — no `documentation_source`); (C) **internal inconsistency** from the same fact authored in multiple files (GETCT is 64-bit in `clock_system.yaml` but 32-bit in `special_registers.yaml` + `spin2/methods/getct.yaml`). Note the new `PASM2-ENCODING-REFERENCE.md` is *generated from* these YAMLs, so it inherits their errors — fix the source YAMLs, then regenerate it.

**Cluster note:** the largest single cluster is the **HUBSET clock-configuration bit-field** error in `hubset.yaml` + `clock_system.yaml` (AF-016/018/019/020/021/146/152/163/120) — CC/SS swapped, VCO/divider fields misplaced, an invented crystal-enable bit, wrong cap values, and the chip-reset selector ($1000_0000 = D[31:28]=%0001, not bit 31).

### F-026 — `getct.yaml`: GETSCP YAML records write: '—' although GETSCP writes D (manual, CSV description, and …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-010)

**File(s):** `getct.yaml`, `getrnd.yaml`, `getscp.yaml`

**What the KB says (suspect):** getscp.yaml encoding has write: '—' (no D written), contradicting both the manual and the instruction's semantics. CSV description (row 401) is 'Get four-channel oscilloscope samples into D. D = {ch3[7:0],ch2[7:0],ch1[7:0],ch0[7:0]}.' - D is written. The encoding reference (line 483) lists D in the writes column. (The CSV's tabular write-column for row 401 is blank, which appears to be a source-table omission since …

**Truth per manual-audit authority:** getscp.yaml encoding[0] has `write: —`, but every primary source shows GETSCP writes its destination register D: manual line 324 "Four 8-bit oscilloscope samples are written to Dest" and line 331 Result column "D"; Silicon Doc line 8835 "Get the lower-byte RDPIN values of four pins into the bytes of D"; CSV row 401 description "into D. D = {ch3[7:0],ch2[7:0],ch1[7:0],ch0[7:0]}". Sibling D-writing instructions getrnd.yaml and getct.yaml correctly record `write: D`. pnut-ts assembles `getscp $1FF` cleanly, confirming D is the destination operand. The YAML's `write: —` is the defect; the manual is correct.

**Authority cited:** deliverables/ai/P2/language/pasm2/getscp.yaml (encoding[0].write: '—'); manual part-ii/instructions-g.md:324 ("written to Dest") and :331 (Result column = D); CSV "P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv":425 (row 401, description "into D. D = {ch3[7:0],...}"); …

**Proposed correction (verify first):** Set getscp.yaml encoding[0].write: D (route to the P2KB corrections register). Leave c/z and flags_affected unchanged — GETSCP affects no flags, which the YAML, manual (C=---, Z=---), and CSV (no WCZ on row 401) all agree on; the encoding-reference "C,Z" Flags column is a generic category header, not instruction-specific.

### F-027 — `clock_system.yaml`: Wrong bit positions: manual says D[23:14], canonical is D[17:8] (magnitudes 10-bit / …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-016)

**File(s):** `clock_system.yaml`

**What the KB says (suspect):** The 10-bit %MMMMMMMMMM VCO multiplier field is at D[17:8] (0..1023 -> multiply by 1..1024).

**Truth per manual-audit authority:** Decoding the canonical Silicon Doc HUBSET word `%0000_000E_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS` (bits 31->0) places the 10-bit %MMMMMMMMMM VCO multiplier at D[17:8]: E=bit24, DDDDDD=D[23:18], MMMMMMMMMM=D[17:8], PPPP=D[7:4], CC=D[3:2], SS=D[1:0]. The manual's "D[23:14]" is a 10-bit window but shifted 6 bits too high — it overlaps the divider field and is wrong. The width (10-bit) and magnitude (x1-1024) the manual states are correct.

**Authority cited:** Silicon Doc engineering/ingestion/sources/silicon-doc/part3-interrupts.txt: line ~521 (HUBSET encoding `##%0000_000E_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS`) + lines 536-540 (%MMMMMMMMMM = 0..1023 -> 1..1024 multiply of VCO). Manual: …

**Proposed correction (verify first):** In the manual (instructions-h.md:50) change "D[23:14] - VCO multiplier (10-bit field, multiplies by 1-1024)" to "D[17:8] - VCO multiplier (MMMMMMMMMM, 10-bit; multiplies by 1-1024; stored as multiplier-1)". ALSO fix the YAML hubset_configuration.config_fields block (clock_system.yaml:138): change `d23_14: "VCO multiplier (MMMM_MMMMMM)"` to `d17_8: "VCO multiplier (MMMMMMMMMM)"` so it agrees with the already-correct …

### F-028 — `clock_system.yaml`: hubset.yaml clock_configuration.bit_fields.d3_2.values (lines 42-45) assigns 15pF to …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-018)

**File(s):** `clock_system.yaml`, `hubset.yaml`

**What the KB says (suspect):** Silicon Doc %CC table: CC=00 Hi-Z, CC=01 1MΩ no caps, CC=10 15pF, CC=11 30pF.

**Truth per manual-audit authority:** Silicon Doc %CC table (lines 562-571) reads: %00 Hi-Z/OFF; %01 1M-ohm/OFF (no caps); %10 1M-ohm/15pF per pin; %11 1M-ohm/30pF per pin. hubset.yaml d3_2.values (lines 43-45) reads ONLY three entries: 0b00 "XI/XO Hi-Z", 0b01 "15pF caps (crystals >= 16 MHz)", 0b11 "30pF caps (crystals < 16 MHz)". So it (a) assigns 15pF to CC=01 — but the authority says CC=01 is no-caps — and (b) omits CC=10 (the true 15pF value) entirely. The sibling clock_system.yaml lines 150-153 already encodes the correct mapping (0b01 no caps; 0b10 15pF; 0b11 30pF), and its example code line 185 confirms %10 = 15pF caps. hubset.yaml is the …

**Authority cited:** Silicon Doc: engineering/ingestion/sources/silicon-doc/part3-interrupts.txt lines 562-571 (the %CC table). Defective YAML: deliverables/ai/P2/language/pasm2/hubset.yaml lines 40-45 (d3_2 Crystal Config). Correct in-repo model: deliverables/ai/P2/architecture/clock_system.yaml lines 150-153 (note: …

**Proposed correction (verify first):** Edit deliverables/ai/P2/language/pasm2/hubset.yaml d3_2.values to four entries matching Silicon Doc / clock_system.yaml: 0b00 "XI/XO Hi-Z (oscillator off)"; 0b01 "1MΩ feedback, no caps"; 0b10 "1MΩ feedback, 15pF caps (crystals >= 16 MHz)"; 0b11 "1MΩ feedback, 30pF caps (crystals < 16 MHz)". This both adds the missing 0b10 and moves the 15pF semantics off 0b01.

### F-029 — `clock_system.yaml`: clock_system.yaml contains two disagreeing maps: pll_system block (lines 104-118) is …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-019)

**File(s):** `clock_system.yaml`

**What the KB says (suspect):** Silicon Doc canonical: input divider DDDDDD=D[23:18]; VCO mult=D[17:8]; PPPP post=D[7:4]; PLL-enable E=D[24]; CC=D[3:2]; SS=D[1:0].

**Truth per manual-audit authority:** The Silicon Doc bit pattern `%0000_000E_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS` decodes unambiguously: E=bit24, DDDDDD=23:18 (XI input divider), MMMMMMMMMM=17:8 (VCO mult), PPPP=7:4 (post divider), CC=3:2 (crystal/XI-XO config), SS=1:0 (clock source select). clock_system.yaml lines 137-144 instead assert: d27_24='XI divider (PPPP)', d23_14='VCO multiplier', d9='PLL power enable', d8='Crystal oscillator enable', d7_4='Post divider (DDDD)', d3_2='Clock source select (SS)', d1_0='Crystal configuration (CC)'. Every one of these is wrong: PLL-enable E belongs at bit24 not d9; d8 crystal-enable is fabricated (no such field …

**Authority cited:** Silicon Doc canonical operand map: engineering/ingestion/sources/silicon-doc/part3-interrupts.txt line 521 (`HUBSET ##%0000_000E_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS`) plus the field tables at lines 525-580 (%CC = XI/XO status/loading-caps = crystal config; %SS = Clock Source). Defective YAML: …

**Proposed correction (verify first):** Rewrite clock_system.yaml hubset_configuration.config_fields (lines 134-144) to the canonical layout: d31='Reset request'; d30_25='Reserved'; d24='PLL enable (E)'; d23_18='XI input divider DDDDDD (1..64, stored as divider-1)'; d17_8='VCO multiplier MMMMMMMMMM (1..1024, stored as mult-1)'; d7_4='Post divider PPPP'; d3_2='Crystal/XI-XO config (CC)'; d1_0='Clock source select (SS)'. Delete the fabricated d8 'Crystal …

### F-030 — `clock_system.yaml`: Example literals written in an SS_CC (source-first) order conflicting with canonical …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-020)

**File(s):** `clock_system.yaml`

**What the KB says (suspect):** Trailing two 2-bit groups are CC then SS (operand ...PPPP_CCSS). To enable 15pF crystal staying on RCFAST: CC=10, SS=00 -> literal '10_00'. To switch to XI: CC=10, SS=10 -> '10_10'. Silicon Doc worked example ##%1_100111_0100101000_1111_10_00 = 'enable crystal+PLL, stay in RCFAST' (CC=10, SS=00).

**Truth per manual-audit authority:** Silicon Doc operand is `...PPPP_CCSS` — CC (crystal/cap) occupies D[3:2], SS (clock source) occupies D[1:0]. The %CC table (line 575: `%10 = 15pF per pin`) and %SS table (line 583: `%10 = XI`, line 586: `%00 = RCFAST`) confirm. So to "enable 15pF crystal staying on RCFAST" the literal must be CC=10,SS=00 = `%10_00`; to switch to XI, CC=10,SS=10 = `%10_10`. The Silicon Doc worked example p2-documentation.txt:6258 literally ends `_10_00` for "enable crystal, stay in RCFAST". The manual (instructions-h.md:63) writes `##%00_10` with comment "Enable crystal with 15pF caps" — decoded against hardware that is CC=00 …

**Authority cited:** Silicon Doc engineering/ingestion/sources/silicon-doc/part3-interrupts.txt:521 (operand layout `##%0000_000E_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS`), :562-588 (%CC table = D[3:2] crystal/cap, %SS table = D[1:0] clock source); p2-documentation.txt:6256-6266 (worked example `##%...1111_10_00` = "enable …

**Proposed correction (verify first):** Fix BOTH the manual (part-ii/instructions-h.md) and clock_system.yaml. (1) Field labels in the manual: D[3:2] is the CRYSTAL config (CC), D[1:0] is the clock SOURCE select (SS) — swap the two "(D[3:2])"/"(D[1:0])" annotations at instructions-h.md:38 and :44. (2) Basic-crystal example literals: `##%00_10` -> `##%10_00` (CC=15pF, SS=RCFAST: enable crystal, stay on RCFAST) and `##%10_10` stays as the switch-to-XI step …

### F-031 — `clock_system.yaml`: Literal %0001_0000_0000_00001010_10 does not parse into canonical field widths (uses a …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-021)

**File(s):** `clock_system.yaml`

**What the KB says (suspect):** Canonical operand %0000_000E_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS. For /1, x16, VCO/2, 15pF, PLL: DDDDDD=000000, MMMMMMMMMM=0000001111, PPPP=0000 (VCO/2 per PPPP=0), E=1, CC=10, SS=11. Architecture 160 MHz example uses %0001_0000_0000_00_10_10 / ..._10_11 groupings.

**Truth per manual-audit authority:** Underscores in Spin2 literals are cosmetic; the literal is just an integer. Manual line 74 literal %0001_0000_0000_00001010_10 = 22 bits = 0x4002A, which decoded against the canonical map gives E=0 (PLL OFF), MULT=x1, PPPP=2 (VCO/6), CC=%10, SS=%10 — it does NOT realize the claimed "/1 * 16 / 2" and is not even PLL-enabled. The YAML line 199 literal %0001_0000_0000_00_10_10 is a DIFFERENT wrong value = 18 bits = 0x400A: E=0 (PLL OFF), MULT=x65, SS=%10. So the manual is not even a faithful copy of the YAML; both diverge into different garbage. Separately, the manual field map (lines 49-52) is wrong: it places the …

**Authority cited:** Silicon Doc: engineering/ingestion/sources/silicon-doc/part3-interrupts.txt lines 516-522 (canonical operand %0000_000E_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS), 524-560 (field tables: E=bit24 PLL on/off, DDDDDD input-div /1..64, MMMMMMMMMM VCO mult 1..1024, PPPP post-div [0=VCO/2], CC=15pF at %10, SS=%11 …

**Proposed correction (verify first):** MANUAL fixes (instructions-h.md): (1) Replace the field map at lines 49-53 with the canonical bit positions: D[24]=E PLL enable (on/off), D[23:18]=DDDDDD XI input divider /1..64, D[17:8]=MMMMMMMMMM VCO multiplier x1..1024, D[7:4]=PPPP VCO post-divider (0=>VCO/2, 15=>VCO/1), D[3:2]=CC crystal/cap config (%10=15pF), D[1:0]=SS clock source (%11=PLL, %10=XI). Drop the bogus "D[9] PLL power enable" and "D[8] crystal …

### F-032 — `ijnz.yaml`: The YAML ijnz.yaml encoding note says PC is written 'only when the result in Dest is zero …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-024)

**File(s):** `ijnz.yaml`, `ijz.yaml`

**What the KB says (suspect):** ijnz.yaml encoding_notes (lines 31-33): 'Dest is always written; PC is written only when the result in Dest is zero (or not zero in syntax 2).'

**Truth per manual-audit authority:** ijnz.yaml:31-33 encoding_notes reads "Dest is always written; PC is written only when the result in Dest is zero (or not zero in syntax 2)." This directly contradicts the SAME file's description (line 5-6: "jumps ... if the result is NOT zero") and result (line 11-12: "If the result is not zero, PC is set ..."). IJNZ = Increment and Jump if Not Zero, so PC must be written when the result is NOT zero; the primary "zero" clause is the IJZ behavior, and "(or not zero in syntax 2)" is a stale parenthetical from when IJZ(00I)/IJNZ(01I) shared one combined note. The manual footnote (instructions-i.md:40) is …

**Authority cited:** Manual: opus-master/part-ii/instructions-i.md:40 (footnote "*PC is written only when the jump condition is met."), :17-18 header IJZ/IJNZ, :34-37 encoding table (00I/01I rows, shared opcode 1011100), :50-53 explanation table (IJNZ jumps "Result != 0"). YAML: …

**Proposed correction (verify first):** In deliverables/ai/P2/language/pasm2/ijnz.yaml, replace the encoding_notes (lines 32-33) with: "Dest is always written; PC is written only when the result in Dest is NOT zero." Remove the inverted "zero" wording and the stale "(or not zero in syntax 2)" parenthetical. No change to ijz.yaml (correctly has no encoding_notes) and no change to the manual (its footnote is correct).

### F-033 — `jnxro.yaml`: Manual is correct (XRO = streamer NCO rollover). jxro.yaml mislabels XRO as 'streamer …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-026)

**File(s):** `jnxro.yaml`, `jxro.yaml`, `pollxro.yaml`, `waitxro.yaml`

**What the KB says (suspect):** jxro.yaml description: 'Jump to S if XRO (streamer ready) event flag is set.' and oneliner: 'Branch' — mislabels XRO as 'streamer ready'. Its own sibling jnxro.yaml correctly says 'Jump to S if XRO (streamer NCO rollover) event flag is clear.'

**Truth per manual-audit authority:** The Silicon Doc (highest available authority for this semantic claim) names XRO as the "streamer-NCO-rollover event flag" in three places (part2-video-output.txt:401,427,449 and the walkthrough-audit:1860). The manual matches this exactly at instructions-j.md:546 ("the XRO (streamer NCO rollover) event flag") and its heading at :521 ("Jump If Streamer NCO Rollover Event"). jxro.yaml:12 mislabels XRO as "streamer ready", which is inconsistent with the Silicon Doc AND with its own sibling jnxro.yaml:4 which correctly says "streamer NCO rollover". The manualSays quote is accurately represented; the manual is …

**Authority cited:** Silicon Doc: engineering/ingestion/sources/silicon-doc/part2-video-output.txt:449 ("JXRO/JNXRO Jump to S/# if the streamer-NCO-rollover event flag is set/clear"), :401 ("POLLXRO Poll the streamer-NCO-rollover event flag"); silicon-doc-v35-walkthrough-audit.md:1860 ("NCO rollover (XRO)"). YAML: …

**Proposed correction (verify first):** Edit deliverables/ai/P2/language/pasm2/jxro.yaml line 12 from "description: Jump to S if XRO (streamer ready) event flag is set." to "description: Jump to S if XRO (streamer NCO rollover) event flag is set." Route to the P2KB corrections register. Also recommend a wider sweep of jxro.yaml's oneliner/other fields for any "streamer ready" residue, and a data-set-wide grep for the same mislabel across other XRO-related …

### F-034 — `jatn.yaml`: jxro.yaml and jxmt.yaml are tagged timing.type 'fixed' (no range) while the manual …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-027)

**File(s):** `jatn.yaml`, `jqmt.yaml`, `jxmt.yaml`, `jxrl.yaml`, `jxro.yaml`

**What the KB says (suspect):** jxro.yaml and jxmt.yaml have timing: {cycles: 2, type: fixed} with NO range field, whereas every sibling event-jump (jatn, jct1, jse1, jpat, jqmt, jxfi, jxrl, etc.) has type: variable and range: 13...20.

**Truth per manual-audit authority:** The event-jumps are one homogeneous instruction class: Silicon Doc lists JXMT/JXRO/JXRL alongside JCT1/JSE1/JATN/JQMT with identical encoding (1011110 01I) and identical description form ("Jump to S/# if <flag> set/clear"). The manual correctly shows JXMT, JXRL, and JXRO with the SAME Clks value "2 or 4 / 2 or 13-20", matching its stated convention (taken in hub-exec = 13...20). The YAMLs are internally inconsistent: jxrl.yaml, jqmt.yaml, jatn.yaml all have timing.type: variable + range: 13...20, but jxro.yaml and jxmt.yaml alone have timing.type: fixed with NO range field. No source supports a fixed/variable …

**Authority cited:** deliverables/ai/P2/language/pasm2/jxro.yaml (timing: cycles 2, type: fixed — no range), jxmt.yaml (same) vs jxrl.yaml / jqmt.yaml / jatn.yaml (timing: cycles 2, type: variable, range: 13...20); manual part-ii/instructions-j.md:5-12 (Conditional Jump Timing Convention: taken in hub-exec = 13...20), …

**Proposed correction (verify first):** In deliverables/ai/P2/language/pasm2/jxro.yaml and jxmt.yaml, change the timing block from `type: fixed` (cycles: 2, no range) to `type: variable` with `range: 13...20`, matching every sibling event-jump (jxrl, jqmt, jatn, jct1, etc.). This routes to the P2KB corrections register. Note: the PASM2-ENCODING-REFERENCE.md shows all event-jumps with a bare "2" (the not-taken cycle count) and does NOT need a change for …

### F-035 — `lockrel.yaml`: The yaml's encoding.c and flags_affected.C ('no effect') contradict both the manual AND …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-028)

**File(s):** `lockrel.yaml`

**What the KB says (suspect):** lockrel.yaml encoding.c: '—' and flags_affected.C: 'No effect' — yet the SAME yaml description states 'If D is a register and WC, get current/last cog id of LOCK owner into D and LOCK status into C.' The encoding reference lists LOCKREL flags column as 'C,Z'.

**Truth per manual-audit authority:** The compiler proves WC is legal on LOCKREL and sets the C encoding bit; the Silicon Doc explicitly states WC makes C indicate lock status. Both override the YAML. lockrel.yaml self-contradicts: encoding.c:'—' and flags_affected.C:'No effect' (lines 9, 30) directly conflict with the same file's description "If D is a register and WC, get current/last cog id of LOCK owner into D and LOCK status into C" (lines 14-15). The manual's "C: LOCK status" and its explanation match the authoritative Silicon Doc and the compiler. Defect is in the YAML, not the manual.

**Authority cited:** pnut-ts v1.55.0 probe (ground truth): `lockrel myreg wc` and `lockrel #5 wc` compile clean (exit 0); decoded encodings EEEE=1111 op=1101011 C0L=100/101 S=000000111 → C-bit=1 when WC, C-bit=0 without WC; `lockrel myreg wz` REJECTED ("This effect is not allowed"). Silicon Doc …

**Proposed correction (verify first):** No manual change — manual is correct. Fix deliverables/ai/P2/language/pasm2/lockrel.yaml: set encoding.c from '—' to reflect C = lock status when WC (e.g. "lock status (when WC)"); change flags_affected.C from "No effect" to "When WC: C = whether lock is currently taken". Leave encoding.z / flags_affected.Z as "No effect" (compiler rejects WZ — confirmed correct). SEPARATELY: PASM2-ENCODING-REFERENCE.md line 218 …

### F-036 — `calld.yaml`: LOC loads a 20-bit address into a pointer register (PA/PB/PTRA/PTRB) — an …  ·  `WONTFIX` (2026-06-10)  (PASM2 audit AF-029)

**File(s):** `calld.yaml`, `callpa.yaml`, `callpb.yaml`, `jmp.yaml`, `loc.yaml`

**What the KB says (suspect):** loc.yaml category: 'Math and Logic'.

**Truth per manual-audit authority:** Both literal claims verify: instructions-l.md:11 does categorize LOC as "Hub Memory Access", and loc.yaml:31 is "Math and Logic". The auditor's substantive conclusion is also right — "Math and Logic" mis-categorizes LOC: LOC loads a 20-bit address into PA/PB/PTRA/PTRB, is the address-loading sibling of CALLD (identical pointer-register-write mechanism, adjacent encoding 11101WW vs CALLD 11100WW), sits in the branch family in the Silicon Doc instruction listing, and every sibling (CALLD/CALLPA/CALLPB/JMP) is yaml category "Branch". BUT the auditor's claim "Manual reasonable as-is / Hub Memory Access more …

**Authority cited:** Manual: opus-master/part-ii/instructions-l.md:11 (LOC header = "Hub Memory Access"); opus-master/part-iii/appendix-c-categorical-index.md:50 (LOC listed under "Arithmetic Operations" section, line 8); opus-master/part-ii/instruction-categories.md:13 (LOC under "Arithmetic Operations / Data …

**Proposed correction (verify first):** Categorize LOC as a Branch / pointer-address instruction across all sources, matching its sibling CALLD. (1) loc.yaml:31 — change category from "Math and Logic" to "Branch" (consistent with calld/callpa/callpb/jmp yaml). (2) Manual — make all three placements consistent: instructions-l.md:11 header → "Branching and Flow Control" (not "Hub Memory Access"); appendix-c-categorical-index.md:50 → move LOC from …

### F-037 — `locknew.yaml`: The manual is correct (variable timing ranges). The yaml timing blocks claim a single …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-031)

**File(s):** `locknew.yaml`, `lockrel.yaml`, `lockret.yaml`, `locktry.yaml`

**What the KB says (suspect):** locknew.yaml timing: {cycles: 4, type: fixed} — claims fixed 4-cycle timing, contradicting its own encoding.clocks: '4...11'. Same fixed/range contradiction in lockrel.yaml (cycles:2/fixed vs '2...9, +2 if result'), lockret.yaml (cycles:2/fixed vs '2...9'), locktry.yaml (cycles:2/fixed vs '2...9, +2 if result').

**Truth per manual-audit authority:** Canonical CSV gives VARIABLE hub-window ranges for all four: LOCKNEW "4...11", LOCKRET "2...9", LOCKTRY "2...9, +2 if result", LOCKREL "2...9, +2 if result". The manual reproduces these ranges faithfully (line 64 "4...11"; line 77 "completes in 4 to 11 clock cycles"; line 113 "2 to 9 clock cycles, with an additional 2 cycles if the result is written back"). The YAMLs each carry encoding.clocks set to the correct range string yet a separate timing block claiming a single FIXED count (locknew cycles:4/fixed; lockrel/lockret/locktry cycles:2/fixed) — internally self-contradictory and contradicting the canonical …

**Authority cited:** Canonical: /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv lines 268-271 (LOCKNEW "4...11", LOCKRET "2...9", LOCKTRY/LOCKREL "2...9, +2 if result"). Manual: opus-master/part-ii/instructions-l.md lines 64,77 (LOCKNEW …

**Proposed correction (verify first):** Leave the manual unchanged (verified correct). In locknew/lockrel/lockret/locktry.yaml, replace the fixed timing block with a variable representation reflecting the hub-window range, e.g. for locknew: timing: {min: 4, max: 11, type: variable}; for lockret: {min: 2, max: 9, type: variable}; for lockrel/locktry: {min: 2, max: 9, type: variable, note: "+2 if result written back"}. Make timing consistent with each …

### F-038 — `tjf.yaml`: The manual carries the COMPLETE taken-timing (cog 4 / hub 13-20). Several jump YAMLs are …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-038)

**File(s):** `tjf.yaml`, `tjns.yaml`, `tjnz.yaml`, `tjv.yaml`, `tjz.yaml`

**What the KB says (suspect):** tjnz.yaml encoding.clocks "2 or 4" with timing.type fixed (no hub variant); tjns.yaml clocks "2 or 4" type fixed; tjz.yaml clocks "2 or 4"; tjf.yaml clocks "2 or 4". PASM2-ENCODING-REFERENCE.md lists only "2". By contrast tjv.yaml carries the full form "2 not-taken / 4 taken (cog); 2 not-taken / 13-20 taken (hub-exec)".

**Truth per manual-audit authority:** The canonical Parallax instruction CSV lists ALL seven test-and-jump instructions identically: cog/LUT = "2 or 4", hub-exec = "2 or 13...20" (CSV:198-204). The MANUAL carries exactly this full form — convention table at instructions-t.md:10-12 defines taken=4 (cog/LUT) or 13...20 (hub), and every TJ row shows "2 or 4 / 2 or 13-20". The manual is therefore CORRECT and matches the authority. The YAMLs are the wrong derived works: tjnz.yaml:15-16 and tjns.yaml:25-26 declare timing.cycles:2 / type:fixed (flatly wrong — branch timing is variable and the taken cost is dropped), and their encoding.clocks is only "2 or …

**Authority cited:** Official Parallax "P2 Instructions v35 - Rev B_C Silicon" CSV — /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:198-204 (TJZ/TJNZ/TJF/TJNF/TJS/TJNS/TJV). Manual: opus-master/part-ii/instructions-t.md:5-12 (convention …

**Proposed correction (verify first):** No manual change (manual matches the canonical Parallax CSV). Fix the derived works to the full form, using the CSV's notation "2 or 4 / 2 or 13...20": (1) tjnz.yaml — set timing.type: variable, replace cycles:2 with the cog/hub note, set encoding.clocks to "2 or 4 / 2 or 13–20"; (2) tjns.yaml — same fixes (currently type:fixed, the worst case); (3) tjz.yaml and tjf.yaml — update encoding.clocks from "2 or 4" to "2 …

### F-039 — `tjf.yaml`: Conditional jumps are inherently variable-timed (taken vs not-taken). Marking TJNZ/TJNS …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-039)

**File(s):** `tjf.yaml`, `tjns.yaml`, `tjnz.yaml`, `tjz.yaml`

**What the KB says (suspect):** tjnz.yaml timing.type: fixed; tjns.yaml timing.type: fixed — whereas tjf.yaml/tjz.yaml use variable and tjs.yaml/tjnf.yaml use variable

**Truth per manual-audit authority:** TJNZ and TJNS are conditional test-and-jump instructions: they cost 2 cycles when the branch is NOT taken and 4 (cog/LUT) when taken — inherently variable. Two independent authorities confirm variable: (1) the YAMLs' own encoding field reads `clocks: 2 or 4`, which directly contradicts their `timing.type: fixed`; (2) the manual's appendix-A encoding table lists TJNZ (line 341) and TJNS (line 340) with timing "2 or 4", exactly matching the variable-timed siblings TJZ (line 344) and TJF (line 338). The four sibling YAMLs (tjz/tjf/tjs/tjnf) all use timing.type: variable. Only tjnz.yaml and tjns.yaml are mislabeled …

**Authority cited:** deliverables/ai/P2/language/pasm2/tjnz.yaml:16 (type: fixed) and :22 (clocks: 2 or 4); tjns.yaml:26 (type: fixed) and :32 (clocks: 2 or 4); sibling tjz.yaml:11 / tjf.yaml:11 (type: variable, range: 13...20); manual encoding table opus-master/part-iii/appendix-a-encoding-table.md:339-344 (TJNZ/TJNS …

**Proposed correction (verify first):** In tjnz.yaml and tjns.yaml, change `timing.type: fixed` to `timing.type: variable`, and add `range: 13...20` to the timing block so they mirror their direct counterparts tjz.yaml / tjf.yaml (which use `type: variable` + `range: 13...20`). No manual change. Route to the P2KB corrections register.

### F-040 — `test.yaml`: The manual provides related cross-references for TESTB; the YAML omits a related: list …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-040)

**File(s):** `test.yaml`, `testb.yaml`, `testbn.yaml`, `testn.yaml`, `testp.yaml`, `testpn.yaml`

**What the KB says (suspect):** testb.yaml has NO related: key at all (sibling testbn.yaml has related: [TESTP, TESTPN]; test.yaml/testn.yaml carry full related lists)

**Truth per manual-audit authority:** Manual line 92 verbatim matches manualSays. testb.yaml has zero `related:` lines while its direct siblings (testbn, test, testn) all carry related: lists. This is a real findability gap on the YAML side; the manual is correct and the derived YAML is incomplete relative to its peers.

**Authority cited:** Manual: engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-t.md:92 ("**Related:** [TESTBN](#testbn), [TESTP](#testp), [TESTPN](#testpn)"). YAML: deliverables/ai/P2/language/pasm2/testb.yaml (45 lines, no `related:` key — grep returns NONE). …

**Proposed correction (verify first):** Add a `related:` list to deliverables/ai/P2/language/pasm2/testb.yaml. To match the most complete sibling pattern (test.yaml/testn.yaml), use the full bit-test family minus self: TESTBN, TEST, TESTN, TESTP, TESTPN. All targets exist as YAML files. No manual change. (Routes to P2KB corrections register.)

### F-041 — `tjf.yaml`: tjf.yaml and tjz.yaml description fields contain a mangled trailing fragment ('... 2 or 4 …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-041)

**File(s):** `tjf.yaml`, `tjz.yaml`

**What the KB says (suspect):** tjf.yaml description: 'Test D and jump to S** if D is full (D = $FFFF_FFFF). 2\n or 4 / 2 or' and tjz.yaml description ends '... 2\n or 4 / 2 or' — a corrupted/truncated clocks string bled into the prose from a table-extraction artifact

**Truth per manual-audit authority:** Parsing tjf.yaml yields description = 'Test D and jump to S** if D is full (D = $FFFF_FFFF).<spaces>2 or 4 / 2 or' and tjz.yaml = 'Test D and jump to S** if D is zero.<spaces>2 or 4 / 2 or'. The YAML folded-scalar continuation (line 14: 'or 4 / 2 or') bleeds a truncated/mangled clocks fragment into the prose — a table-extraction artifact. The matching encoding.clocks is the clean '2 or 4'. Manual prose is independently clean: instructions-t.md:272 'TJF and TJNF test Dest for "full" state ($FFFF_FFFF = -1 = all bits set)' and :358 'TJZ and TJNZ test Dest...'. Defect is confined to the two YAML description fields; …

**Authority cited:** tjf.yaml:13-14 and tjz.yaml:13-14 (deliverables/ai/P2/language/pasm2/); python yaml.safe_load probe of both files; manual prose at engineering/.../opus-master/part-ii/instructions-t.md:272 and :358; appendix-c-categorical-index.md:168

**Proposed correction (verify first):** In tjf.yaml set description to: 'Test D and jump to S** if D is full (D = $FFFF_FFFF).' and in tjz.yaml set description to: 'Test D and jump to S** if D is zero.' — removing the embedded '2 or 4 / 2 or' fragment and the trailing whitespace/folded continuation on lines 13-14. Timing already lives correctly in encoding[0].clocks ('2 or 4'). No manual change. Route to the P2KB corrections register.

### F-042 — `addpix.yaml`: The '(and alpha if present)' parenthetical is a manual-introduced semantic claim the …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-047)

**File(s):** `addpix.yaml`

**What the KB says (suspect):** addpix.yaml description: 'ADDPIX sums individual RGB (red, green, blue) color values of Src into that of Dest ... Each byte is saturated to prevent wraparound.' result: 'Src color value bytes are added into Dest color value bytes with full saturation.' The YAML documents only RGB; it makes no statement about an alpha / fourth byte.

**Truth per manual-audit authority:** Silicon Doc p2-documentation.txt:2556-2557: "A pixel consists of four byte fields within a 32-bit cog register. Pixel operations occur between each pair of D and S bytes, and they take seven clock cycles to complete: ADDPIX..." and :2586-2589 shows the operation acting on all four bytes D[31:24]/D[23:16]/D[15:08]/D[07:00]. The hardware unconditionally processes four bytes; the 4th byte is the alpha channel of 8:8:8:8 pixel data. Therefore the manual's "(and alpha if present)" is silicon-CORRECT, not an unsourced hallucination. The actual error is the "three color channels" framing (manual lines 154 AND 158) — …

**Authority cited:** Manual: engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-a.md:154 ("individual RGB ... Each byte is treated as a separate color channel") and :158 ("all three color channels (and alpha if present) in parallel, completing in 7 clock cycles"). YAML: …

**Proposed correction (verify first):** Do NOT drop the alpha parenthetical (that would make the manual less accurate). Instead correct the channel COUNT in both manual and YAML to match the Silicon Doc: ADDPIX (like all pixel-mixer ops) operates on all FOUR byte fields of the 32-bit register (D[31:24], D[23:16], D[15:08], D[07:00]) unconditionally — for 8:8:8:8 pixel data these are R, G, B and alpha. Manual line 158: change "all three color channels (and …

### F-043 — `addsx.yaml`: The YAML cross-reference set for ADDSX self-references and omits ADDS. The manual already …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-048)

**File(s):** `addsx.yaml`

**What the KB says (suspect):** addsx.yaml related: lists ADD, ADDX, ADDSX, SUBSX — it lists ADDSX (the instruction itself) where it should list ADDS.

**Truth per manual-audit authority:** Manual line 224 reads: "**Related:** [ADD](#add), [ADDX](#addx), [ADDS](#adds), [SUBSX](#subsx)" — a clean, self-consistent set (ADD, ADDX, ADDS, SUBSX). addsx.yaml related: block reads "- ADD / - ADDX / - ADDSX / - SUBSX" — it lists ADDSX (the instruction defining the file itself, a self-reference) and omits ADDS. All four intended siblings (add, addx, adds, subsx) exist as real instruction YAMLs, confirming the manual's set is the legitimate one. The YAML's ADDSX entry is an evident self-reference typo for ADDS.

**Authority cited:** Manual: opus-master/part-ii/instructions-a.md:224 (ADDSX entry Related line). YAML: deliverables/ai/P2/language/pasm2/addsx.yaml, related: block. Sibling existence: deliverables/ai/P2/language/pasm2/{add,addx,adds,subsx}.yaml all present.

**Proposed correction (verify first):** In deliverables/ai/P2/language/pasm2/addsx.yaml, change the related: entry "ADDSX" to "ADDS", yielding the set ADD, ADDX, ADDS, SUBSX (matching the manual). Route to engineering/operations/P2KB-CORRECTION-FINDINGS.md. The manual needs no change.

### F-044 — `add.yaml`: The YAML omits the ADDS cross-reference that the manual (and the rest of the ADD family) …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-049)

**File(s):** `add.yaml`, `adds.yaml`, `addsx.yaml`, `addx.yaml`

**What the KB says (suspect):** addx.yaml related: lists only ADD, ADDSX, SUBX — ADDS is absent.

**Truth per manual-audit authority:** Manual line 261 reads exactly: "**Related:** [ADD](#add), [ADDS](#adds), [ADDSX](#addsx), [SUBX](#subx)" — manualSays is quoted faithfully. addx.yaml:40-43 related: lists only ADD, ADDSX, SUBX; ADDS is absent — sourceSays is accurate. The ADD-family convention (verified across add.yaml: ADDX/ADDS/ADDSX/SUB; adds.yaml: ADD/ADDX/ADDSX/SUBS) is to cross-link all three siblings plus the paired SUB-variant. addx.yaml is the only family member missing a sibling (ADDS). adds.yaml exists, so the cross-reference is valid and resolvable.

**Authority cited:** Manual: opus-master/part-ii/instructions-a.md:239 (## ADDX {#addx}), :261 Related line. YAML: deliverables/ai/P2/language/pasm2/addx.yaml:40-43 (related: ADD/ADDSX/SUBX). Sibling YAMLs: add.yaml, adds.yaml, addsx.yaml related blocks. adds.yaml confirmed present (target of the reference is a real …

**Proposed correction (verify first):** Add 'ADDS' to addx.yaml related: block, yielding ADD, ADDS, ADDSX, SUBX (matches the manual and the rest of the ADD family). Route to engineering/operations/P2KB-CORRECTION-FINDINGS.md.

### F-045 — `augd.yaml`: Manual correctly documents the AUGD SETQ/PTRx errata; augd.yaml omits it, so a remote …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-054)

**File(s):** `augd.yaml`, `augs.yaml`

**What the KB says (suspect):** Silicon Doc KNOWN BUGS names AUGD explicitly: 'Intervening ALTx/AUGS/AUGD instructions between SETQ/SETQ2 and RDLONG/WRLONG/WMLONG-PTRx instructions will cancel the special-case block-size PTRx deltas.' But augd.yaml contains NO silicon_errata section at all (augs.yaml does).

**Truth per manual-audit authority:** Silicon Doc KNOWN BUGS (p2-documentation.txt:196-197) explicitly names AUGD in the block-size PTRx-delta cancellation bug. The manual documents this correctly at instructions-a.md:1029, verbatim matching manualSays, and the AUGS twin at :1067. augd.yaml has ZERO silicon_errata key (grep -c "^silicon_errata:" = 0). So a remote agent reading only augd.yaml misses a documented silicon bug that the manual carries. Manual is correct; YAML is the omission. defectSide=yaml confirmed.

**Authority cited:** Silicon Doc: engineering/ingestion/sources/silicon-doc/p2-documentation.txt:196-198 (KNOWN BUGS — "Intervening ALTx/AUGS/AUGD instructions between SETQ/SETQ2 and RDLONG/WRLONG/WMLONG-PTRx instructions will cancel the special-case block-size PTRx deltas"); manual: part-ii/instructions-a.md:1029 …

**Proposed correction (verify first):** Add a silicon_errata entry to augd.yaml for the SETQ/SETQ2 → RDLONG/WRLONG/WMLONG block-size PTRx-delta cancellation, sourced to Silicon Doc KNOWN BUGS (p2-documentation.txt:196-198). NOTE the finding's "parallel to augs.yaml" wording is inaccurate: augs.yaml's existing silicon_errata documents a DIFFERENT bug (intervening ALTx-with-immediate-#S consuming AUGS), NOT the block-size PTRx bug. The block-size PTRx …

### F-046 — `augd.yaml`: The augs.yaml scope_note conflates two distinct Silicon-Doc bugs (block-delta vs …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-055)

**File(s):** `augd.yaml`, `augs.yaml`

**What the KB says (suspect):** augs.yaml scope_note: 'The Silicon Doc documents this errata for AUGS only. The same mechanism may apply to AUGD, but that is NOT stated in any golden source -- it is a known-unknown and is deliberately not asserted here.' This is wrong for the SETQ/PTRx delta bug, which the Silicon Doc explicitly names for 'ALTx/AUGS/AUGD' together.

**Truth per manual-audit authority:** Two DISTINCT Silicon-Doc KNOWN BUGS: line 198 "Intervening ALTx/AUGS/AUGD instructions between SETQ/SETQ2 and RDLONG/WRLONG/WMLONG-PTRx ... cancel the special-case block-size PTRx deltas" (names AUGD); line 212 "Intervening ALTx instructions with an immediate #S operand, between AUGS and the AUGS' intended target ... will use the AUGS value, but not cancel it" (names only AUGS). The augs.yaml scope_note (:62) is attached to the SECOND (intervening-#S) errata and reads: "documents this errata for AUGS only ... may apply to AUGD, but that is NOT stated in any golden source." Under its strict anchor ("this …

**Authority cited:** Silicon Doc /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/silicon-doc/p2-documentation.txt:197-198 (block-delta bug naming "ALTx/AUGS/AUGD") and :212-227 (intervening-#S bug naming only AUGS/ALTx); deliverables/ai/P2/language/pasm2/augs.yaml:49-63 …

**Proposed correction (verify first):** Two YAML edits (manual needs no change): (1) In augs.yaml, tighten the scope_note so it no longer implies AUGD is absent from ALL golden sources. Replace with something like: "The Silicon Doc documents THIS errata (intervening ALTx with immediate #S consuming the AUGS value) for AUGS only. Note this is distinct from the block-size PTRx-delta bug (Silicon Doc KNOWN BUGS), which DOES name ALTx/AUGS/AUGD together — see …

### F-047 — `altgn.yaml`: The generated encoding reference's per-row flags column asserts C,Z effects for …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-056)

**File(s):** `altgn.yaml`, `alti.yaml`, `augd.yaml`

**What the KB says (suspect):** PASM2-ENCODING-REFERENCE.md lists a 'C,Z' flags column for ALTGN, ALTGW, ALTI, ALTR, ALTS, ALTSB, ALTSN, ALTSW, AUGD, AUGS — implying WC/WZ writes these instructions do not support. The per-instruction YAMLs all carry flags_affected: C/Z No effect and encoding.c/z: —.

**Truth per manual-audit authority:** The encoding reference's Flags column is NOT per-instruction. Of 359 instruction rows, 344 read "C,Z" (the rest are alignment misparses: "D", "{WC/WZ/WCZ}", etc.). Root cause is gen-pasm2-encoding-reference.py:64-67: `fa = d.get("flags_affected"); if "C" in fa: flags.append("C")`. Since the YAML `flags_affected` is a DICT `{C: "No effect", Z: "No effect"}`, the test `"C" in fa` checks the KEY (always present) not the VALUE — so it emits "C,Z" even when the value is "No effect". pnut-ts is decisive: `altd ptra wc` and `augs #x wc` both error "This effect is not allowed for this instruction", proving ALTx/AUGx …

**Authority cited:** pnut-ts v1.55.0 probes (ground truth): `altd ptra` compiles clean but `altd ptra wc` → "This effect is not allowed for this instruction"; `augs #$12345 wc` → same error — so ALTx/AUGx accept no WC/WZ and write no flags. deliverables/ai/P2/language/PASM2-ENCODING-REFERENCE.md:401-402,469-476 …

**Proposed correction (verify first):** The finding's proposedCorrection is correct but understated in scope. Fix gen-pasm2-encoding-reference.py:64-67 so the Flags column reflects the VALUE of flags_affected, not the presence of the key. Replace `if "C" in fa: flags.append("C")` with a value test, e.g.: `cv = fa.get("C"); if cv and str(cv).strip().lower() not in ("no effect","—","-","--","none"): flags.append("C")` (same for Z). This is a global bug …

### F-048 — `calla.yaml`: The manual adds a Hub-execution timing figure '13+' that no available KB authority …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-058)

**File(s):** `calla.yaml`, `callb.yaml`, `reta.yaml`

**What the KB says (suspect):** calla.yaml gives clocks '5...12 *' on both encoding rows and timing cycles '5-12' with NO Hub figure; PASM2-ENCODING-REFERENCE.md lists CALLA Cyc as '5-12' only. (The KB does record hub-exec timing when known — e.g. RETA '11...18 (cog) / 20...40 (hub-exec)' — but none for CALLA.)

**Truth per manual-audit authority:** The finding's premise — that the manual's "13+" Hub-exec figure is unsupported by KB authority — is REFUTED by the Silicon Doc, which outranks the per-instruction YAML. The Silicon Doc (p2-documentation.txt:743-744) states the architectural rule that any branch into a hub address costs "a minimum of 13 clock cycles" (+1 if not long-aligned, plus hub-window variability). CALLA is a branch instruction, so in hub-exec mode its "13+" figure is correct and directly sourceable. The manual already applies this same rule consistently to CALL/CALLD/CALLPA/CALLPB ("13-20 cycles for Hub execution"). Therefore the manual is …

**Authority cited:** Silicon Doc p2-documentation.txt:743-744 ("Branching to a hub address takes a minimum of 13 clock cycles. If the instruction being branched to is not long-aligned, one additional clock cycle is required."); manual part-ii/instructions-c.md:73-74,91 (CALLA "5-12 / 13+"; "5-12 cycles for COG/LUT …

**Proposed correction (verify first):** Do NOT drop "/ 13+" from the manual — it is correct. Fix the KB instead: add hub-exec timing to calla.yaml (and callb.yaml) to match the manual and the sibling RETA pattern. Suggested: timing.cycles "5-12 (cog/LUT) / 13+ (hub-exec)" with a note "hub-exec branch incurs the >=13-clock hub-branch penalty per Silicon Doc (min 13, +1 if target not long-aligned, plus hub-window wait)"; likewise update …

### F-049 — `call.yaml`: Same as CALLA: the manual adds an unsourced Hub-execution figure '13+' not present in the …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-059)

**File(s):** `call.yaml`, `calla.yaml`, `callb.yaml`

**What the KB says (suspect):** callb.yaml gives clocks '5...12 *' on both rows and timing cycles '5-12' with NO Hub figure; PASM2-ENCODING-REFERENCE.md lists CALLB Cyc as '5-12' only.

**Truth per manual-audit authority:** The cited PASM2 Manual (Page 57) gives CALLA/CALLB Clocks as "5–122 / 14–322" — a PDF-extraction artifact where the footnote-2 superscript concatenated onto each number. Decoded against the visible footnote ("2 = +1 clock if target not long-aligned in Hub RAM") and the clean sibling CALL rows ("4 / 13–20"), the true values are: Cog/LUT = 5–12, Hub-exec = 14–32. Therefore: (1) the manual's "13+" Hub figure is WRONG — the sourced value is 14–32, not 13+ (the "13+" appears fabricated/mis-derived from CALL's 13–20). (2) callb.yaml and PASM2-ENCODING-REFERENCE.md are ALSO wrong — they OMIT the hub-exec figure …

**Authority cited:** Manual: opus-master/part-ii/instructions-c.md:117-118 (Clks "5-12 / 13+"), :135 ("13+ cycles for Hub execution"). KB: deliverables/ai/P2/language/pasm2/callb.yaml:18-31 (clocks "5...12 *", timing 5-12, no hub figure); PASM2-ENCODING-REFERENCE.md:66 (Cyc "5-12"). PRIMARY SOURCE: …

**Proposed correction (verify first):** Set the Hub-execution timing to the sourced value 14–32 (with +1 if target not long-aligned) in ALL THREE places — do NOT reduce the manual to "5-12". Manual instructions-c.md: change Clks column on both CALLB rows (lines 117-118) from "5-12 / 13+" to "5-12 / 14-32" and line 135 explanation "13+ cycles for Hub execution" to "14-32 cycles for Hub execution"; apply the same correction to CALLA (lines 73-74, 91, "13+" …

### F-050 — `calla.yaml`: The manual is correct (CALLA uses PTRA only). The YAML description is a copy-paste …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-060)

**File(s):** `calla.yaml`, `callb.yaml`

**What the KB says (suspect):** calla.yaml description: "Write current C and Z flags and address of the next instruction into the 4-byte Hub RAM location at PTRA or PTRB, increment pointer..."

**Truth per manual-audit authority:** manualSays quote verified verbatim at instructions-c.md:81 — "CALLA writes the current C and Z flags and the address of the next instruction into the 4-byte Hub RAM location at PTRA, then increments PTRA by 4..." (PTRA only). The manual's separate CALLB entry at :125 correctly uses PTRB only, proving the manual distinguishes the two pointers. Authority confirms CALLA=via PTRA, CALLB=via PTRB: encoding-reference :66 correctly states CALLB stores "at PTRB++" only; brief_description in both YAMLs ("Call subroutine via PTRA"/"via PTRB") is correct; Silicon Doc :3961 lists them as the PTRA/PTRB stack variants. The …

**Authority cited:** Manual: opus-master/part-ii/instructions-c.md:81 (CALLA) and :125 (CALLB). YAML: deliverables/ai/P2/language/pasm2/calla.yaml:18-21 ("at PTRA or PTRB"); callb.yaml:5-8 (same artifact). Encoding reference: deliverables/ai/P2/language/PASM2-ENCODING-REFERENCE.md:65 (CALLA) and :66 (CALLB). Silicon …

**Proposed correction (verify first):** Edit calla.yaml:18-21 description to reference PTRA only: "Write current C and Z flags and address of the next instruction into the 4-byte Hub RAM location at PTRA, increment PTRA by 4, set PC to new relative or absolute address...". IN ADDITION (auditor's correction was incomplete): the identical "PTRA or PTRB" artifact also appears in PASM2-ENCODING-REFERENCE.md:65 (CALLA row says "at PTRA++ or PTRB++" — should be …

### F-051 — `callb.yaml`: The manual is correct (CALLB uses PTRB only). The YAML description copy-paste artifact …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-061)

**File(s):** `callb.yaml`

**What the KB says (suspect):** callb.yaml description: "Write current C and Z flags and address of the next instruction into the 4-byte Hub RAM location at PTRA or PTRB, increment pointer..."

**Truth per manual-audit authority:** Manual line 125 says PTRB only (quoted accurately by the finding). The callb.yaml `description` (lines 5-8) reads "...4-byte Hub RAM location at PTRA or PTRB, increment pointer..." — but every other field in that very same YAML (brief_description "Call subroutine via PTRB", encoding_notes "Stores return context at PTRB address then increments PTRB by 4", oneliner "...at PTRB++", syntax variants all PTRB) correctly references PTRB only. The "PTRA or PTRB" phrasing is a generic copy-paste template artifact. Silicon Doc and encoding reference both back PTRB. Manual is correct; YAML description line is the defect.

**Authority cited:** Manual: opus-master/part-ii/instructions-c.md:125 ("...into the 4-byte Hub RAM location at PTRB, then increments PTRB by 4..."). YAML: deliverables/ai/P2/language/pasm2/callb.yaml:5-8 (description "at PTRA or PTRB"), vs same file's brief_description:3 "via PTRB", encoding_notes "Stores...at PTRB …

**Proposed correction (verify first):** In deliverables/ai/P2/language/pasm2/callb.yaml, edit the `description` field to reference only PTRB: "Write current C and Z flags and address of the next instruction into the 4-byte Hub RAM location at PTRB, increment pointer, set PC to new relative or absolute address, and optionally update C and/or Z to new state. R = 1 then PC += A, else PC = A." (Routes to the P2KB corrections register.)

### F-052 — `callpa.yaml`: The manual correctly disambiguates (PA for CALLPA, PB for CALLPB); the YAML parameter …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-062)

**File(s):** `callpa.yaml`, `callpb.yaml`

**What the KB says (suspect):** callpa.yaml and callpb.yaml both have parameter: "...whose value is copied to PA or PB." (identical copy-paste; oneliner also says '...copy D into PA or PB' in both).

**Truth per manual-audit authority:** Silicon Doc WW-FIELD-ENCODING.md:60-61 states CALLPA always targets PA and CALLPB always targets PB ("fixed destinations"). The manual reflects this correctly (PA at line 200, PB at line 236). The YAML parameter text and oneliner in BOTH callpa.yaml and callpb.yaml say "PA or PB" — a verbatim copy-paste that is imprecise in each file (callpa should say only PA, callpb only PB). The YAMLs' own encoding 'write' fields ("PA and PC" / "PB and PC") internally contradict their ambiguous prose, confirming the prose is the defect.

**Authority cited:** Manual: opus-master/part-ii/instructions-c.md:200 ("...whose value is copied to PA.") and :236 ("...whose value is copied to PB.") — correct/specific. YAML: deliverables/ai/P2/language/pasm2/callpa.yaml lines 6-7 (parameters Dest "copied to PA or PB") and oneliner ("copy D into PA or PB"); …

**Proposed correction (verify first):** In callpa.yaml: change Dest parameter to "...whose value is copied to PA." and oneliner to "Call a subroutine; store return context on the stack and copy D into PA". In callpb.yaml: change Dest parameter to "...whose value is copied to PB." and oneliner to "...copy D into PB". (The description fields in both YAMLs are already correct — only the parameters Dest line and oneliner need the fix.) Route to the P2KB …

### F-053 — `cmp.yaml`: The YAML cross-reference set for CMPSX self-references itself and is missing CMPS. The …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-063)

**File(s):** `cmp.yaml`, `cmps.yaml`, `cmpsx.yaml`, `cmpx.yaml`

**What the KB says (suspect):** cmpsx.yaml related: [CMP, CMPX, CMPSX] — contains a self-reference to CMPSX and omits CMPS

**Truth per manual-audit authority:** cmpsx.yaml's related: block ends with the literal item "CMPSX" — a self-reference — and contains no "CMPS" entry. The signed/extended compare family is the 4-instruction set {CMP, CMPX, CMPS, CMPSX}; the correct sibling set for CMPSX is the other three: {CMP, CMPX, CMPS}. The manual at instructions-c.md:484 lists exactly those three correctly. The YAML therefore both self-references and drops the genuine sibling CMPS. The auditor's manualSays quote and sourceSays are accurate verbatim.

**Authority cited:** Manual: opus-master/part-ii/instructions-c.md:484 (`**Related:** [CMP](#cmp), [CMPX](#cmpx), [CMPS](#cmps)`); section header line 462 `## CMPSX {#cmpsx}`. YAML: deliverables/ai/P2/language/pasm2/cmpsx.yaml `related:` block = [CMP, CMPX, CMPSX]. Sibling YAMLs cross-checked: cmp.yaml [CMPR, CMPX, …

**Proposed correction (verify first):** In deliverables/ai/P2/language/pasm2/cmpsx.yaml, change the related: list from [CMP, CMPX, CMPSX] to [CMP, CMPX, CMPS]. NOTE a co-located defect surfaced while verifying: cmpx.yaml's related: block is [CMP, CMPX, CMPSX] — it likewise self-references CMPX and omits CMPS; its correct set should be [CMP, CMPS, CMPSX]. Recommend fixing both in the same corrections-register pass since they share the identical copy-paste …

### F-054 — `cmp.yaml`: The YAML cross-reference set for CMPX self-references itself and is missing CMPS. The …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-064)

**File(s):** `cmp.yaml`, `cmps.yaml`, `cmpsx.yaml`, `cmpx.yaml`

**What the KB says (suspect):** cmpx.yaml related: [CMP, CMPX, CMPSX] — contains a self-reference to CMPX and omits CMPS

**Truth per manual-audit authority:** cmpx.yaml related block reads literally: "- CMP / - CMPX / - CMPSX" (lines 38-40), which lists CMPX as related to itself and omits CMPS. The manual's CMPX Related line (instructions-c.md:527) reads "**Related:** [CMP](#cmp), [CMPS](#cmps), [CMPSX](#cmpsx)" — correct and self-consistent. CMP/CMPS/CMPSX/CMPX are all real, distinct instructions (each has its own YAML with valid syntax). Self-reference adds no information and CMPS (the signed peer of unsigned CMPX) is the natural omitted relative.

**Authority cited:** deliverables/ai/P2/language/pasm2/cmpx.yaml:37-40 (related: CMP, CMPX, CMPSX — self-reference + missing CMPS); part-ii/instructions-c.md:527 (Related: CMP, CMPS, CMPSX — correct); confirmed cmp.yaml/cmps.yaml/cmpsx.yaml/cmpx.yaml all exist with valid syntax lines.

**Proposed correction (verify first):** In deliverables/ai/P2/language/pasm2/cmpx.yaml, change the related block from [CMP, CMPX, CMPSX] to [CMP, CMPS, CMPSX] — drop the CMPX self-reference, add CMPS. Routes to the P2KB corrections register per Sacred Rule #7 (redirect, not delete).

### F-055 — `cogid.yaml`: The YAML cross-reference set for COGSTOP self-references itself and omits COGID. The …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-065)

**File(s):** `cogid.yaml`, `coginit.yaml`, `cogstop.yaml`

**What the KB says (suspect):** cogstop.yaml related: [COGINIT, COGSTOP] — self-references COGSTOP and omits COGID

**Truth per manual-audit authority:** cogstop.yaml lines 42-44 read `related:` / `- COGINIT` / `- COGSTOP` — the second entry is a self-reference to COGSTOP (meaningless) and COGID is absent. The manual at instructions-c.md:781 reads exactly `**Related:** [COGINIT](#coginit), [COGID](#cogid)`, matching manualSays verbatim and forming the correct COG-control set. Sibling files confirm the intended pattern: coginit references {COGID, COGSTOP} and cogid references {COGINIT, COGSTOP}; by symmetry cogstop must reference {COGINIT, COGID}. The `COGSTOP` entry is a transcription error for `COGID`.

**Authority cited:** deliverables/ai/P2/language/pasm2/cogstop.yaml:42-44 (related: [COGINIT, COGSTOP]); manual part-ii/instructions-c.md:781 (**Related:** [COGINIT](#coginit), [COGID](#cogid)); sibling YAMLs coginit.yaml:42-44 (related COGID, COGSTOP) and cogid.yaml:40-42 (related COGINIT, COGSTOP) establish the trio …

**Proposed correction (verify first):** In deliverables/ai/P2/language/pasm2/cogstop.yaml, change the related list item `- COGSTOP` (line 44) to `- COGID`, yielding related: [COGINIT, COGID]. Bare-name style retained to match the established convention in this file and its siblings (cogid.yaml, coginit.yaml). Route to the P2KB corrections register.

### F-056 — `djf.yaml`: The YAML note states PC is written when the result is "full", but DJNF writes PC (jumps) …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-077)

**File(s):** `djf.yaml`, `djnf.yaml`

**What the KB says (suspect):** YAML djnf.yaml encoding_notes: "Dest is always written; PC is written only when the result in Dest is full (or not full in syntax 2)." DJNF (opcode 11I) jumps when NOT full and has no "syntax 2"; the note is inverted/templated.

**Truth per manual-audit authority:** CSV row 171 (silicon authority): DJNF jumps when result is NOT $FFFF_FFFF (not full). Manual:407 matches authority: "Dest is always written with the decremented value. PC is written only when the result in Dest is not full." YAML djnf.yaml:34-35 encoding_notes says the OPPOSITE: "PC is written only when the result in Dest is full (or not full in syntax 2)." That note is internally contradicted by djnf.yaml's own description (line 6: "jumps ... if the result is NOT full"), result (line 12), and oneliner (line 47), all of which are correct. DJNF has no "syntax 2" variant — the parenthetical is templated …

**Authority cited:** Silicon instruction table CSV row 171: "/workspaces/P2-Knowledge-Base/engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:195" ("DJNF ... Decrement D and jump to S** if result is not $FFFF_FFFF"); manual …

**Proposed correction (verify first):** Edit deliverables/ai/P2/language/pasm2/djnf.yaml encoding_notes (lines 34-35) to: "Dest is always written; PC is written only when the result in Dest is NOT full." Drop the "(or not full in syntax 2)" clause entirely — DJNF has no syntax-2 variant, so the parenthetical is spurious templated text. Route to the P2KB corrections register (engineering/operations/P2KB-CORRECTION-FINDINGS.md).

### F-057 — `djnz.yaml`: The YAML note states PC is written when the result is "zero", but DJNZ writes PC (jumps) …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-078)

**File(s):** `djnz.yaml`

**What the KB says (suspect):** YAML djnz.yaml encoding_notes: "Dest is always written; PC is written only when the result in Dest is zero (or not zero in syntax 2)." DJNZ (opcode 01I) jumps when NOT zero and has no "syntax 2"; the note's primary clause is inverted.

**Truth per manual-audit authority:** Manual is correct as claimed: instructions-d.md:450 reads `| DJNZ | Result != 0 |`, i.e. jumps when result is NOT zero. The YAML encoding_notes (djnz.yaml:31-33) states: "Dest is always written; PC is written only when the result in Dest is zero (or not zero in syntax 2)." That primary clause is inverted for DJNZ — PC is written (the jump taken) when the result is NOT zero. DJNZ = Decrement and Jump if Not Zero (silicon doc :3966 "Decrement and jump"), and the SAME YAML's authoritative description field (djnz.yaml:4-6) correctly says "jumps to the address described by Src if the result is NOT zero." The …

**Authority cited:** Manual: opus-master/part-ii/instructions-d.md:447-450 (table "Jumps when": DJZ result==0, DJNZ "Result != 0") and :445 explanation. YAML defect: deliverables/ai/P2/language/pasm2/djnz.yaml:31-33 (encoding_notes) vs its own :4-6 description. Silicon Doc: silicon-doc-v35-walkthrough-audit.md:3966 …

**Proposed correction (verify first):** Fix djnz.yaml encoding_notes (lines 31-33) to: "Dest is always written; PC is written (the jump is taken) only when the result in Dest is NOT zero." Drop the spurious "(or not zero in syntax 2)" clause — DJNZ has only one syntax. Routes to the P2KB corrections register. The manual needs no change.

### F-058 — `rdbyte.yaml`: Manual says RDLONG updates Z (result==0) under WZ/WCZ; rdlong.yaml says Z has no effect. …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-087)

**File(s):** `rdbyte.yaml`, `rdlong.yaml`, `rdword.yaml`

**What the KB says (suspect):** rdlong.yaml encoding has `z: —` and `flags_affected: Z: No effect`. This contradicts the manual AND the sibling instructions: rdbyte.yaml and rdword.yaml both carry `z: Result = 0` / `Z: Set if result equals zero`, and the encoding reference lists C,Z for RDLONG identically to RDBYTE/RDWORD. RDLONG supports WZ (Z = result==0) exactly as its byte/word siblings do; the YAML 'No effect' is the outlier and is wrong.

**Truth per manual-audit authority:** Silicon Doc part3-end.txt:133-143 lists RDBYTE, RDWORD, RDLONG together — all three `EEEE 101.... CZI ... {WC/WZ/WCZ}` — then states a single shared rule (line 143): "If WZ is expressed, Z will be set if the data read from the hub equaled zero, otherwise Z will be cleared." This applies to RDLONG identically to its siblings. The compiler accepts `rdlong ... wz`. The manual (instructions-r.md:268,290) correctly reflects this. rdlong.yaml (z: —, Z: No effect) is the lone outlier, contradicting the Silicon Doc, the compiler, the manual, the encoding reference (C,Z at line 248), and its own siblings …

**Authority cited:** Silicon Doc engineering/ingestion/sources/silicon-doc/part3-end.txt:133-143 (RDBYTE/RDWORD/RDLONG all `CZI` + `{WC/WZ/WCZ}`; line 143: "If WZ is expressed, Z will be set if the data read from the hub equaled zero"); pnut-ts probe v1.55.0: `rdlong x, ptra wz` compiled clean (Wrote /tmp/af087.bin); …

**Proposed correction (verify first):** Fix deliverables/ai/P2/language/pasm2/rdlong.yaml: set encoding[0].z (line 8) from "—" to "Result = 0", and flags_affected.Z (line 26) from "No effect" to "Set if result equals zero" — matching rdbyte.yaml/rdword.yaml and the Silicon Doc. The manual needs no change. Route to the P2KB corrections register.

### F-059 — `rolbyte.yaml`: The ROLBYTE YAML mislabels the index field as a 'nibble ID'. ROLBYTE selects one of four …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-088)

**File(s):** `rolbyte.yaml`

**What the KB says (suspect):** Num is a 2-bit literal identifying the nibble ID (0-3) of Src to read.

**Truth per manual-audit authority:** ROLBYTE rotates one of four BYTES (NN = 2-bit literal, 0-3) of Src into Dest. The rolbyte.yaml is internally inconsistent: its description says "ROLBYTE reads the byte identified by Num (0-3)" and "Num (0-3) identifies a value's individual bytes, by position", and its result says "Byte Num (0-3) of Src ... is rotated left", yet line 19 erroneously says "nibble ID". This is a copy-paste artifact from ROLNIB (which legitimately uses nibbles, Num 0-7, 3-bit NNN). The manual (line 1133) correctly says "byte position". The Silicon Doc and encoding reference both confirm byte semantics.

**Authority cited:** Manual: opus-master/part-ii/instructions-r.md:1133 ("N is a 2-bit literal (0-3) identifying the byte position in Src."). YAML: deliverables/ai/P2/language/pasm2/rolbyte.yaml:19 ("Num is a 2-bit literal identifying the nibble ID (0-3) of Src to read.") — contradicted by its own description (line …

**Proposed correction (verify first):** Edit deliverables/ai/P2/language/pasm2/rolbyte.yaml line 19: replace "Num is a 2-bit literal identifying the nibble ID (0-3) of Src to read." with "Num is a 2-bit literal identifying the byte ID (0-3) of Src to read." (replace "nibble" with "byte"). Routes to the P2KB corrections register.

### F-060 — `rolword.yaml`: The ROLWORD YAML mislabels the index field as a 'nibble ID'. ROLWORD selects one of two …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-089)

**File(s):** `rolword.yaml`

**What the KB says (suspect):** Num is a 1-bit literal identifying the nibble ID (0-1) of Src to read.

**Truth per manual-audit authority:** ROLWORD is unambiguously a WORD operation. Silicon Doc (p2-documentation.txt:10410-10418) lists the rotate/get/set families: ROLNIB (nibbles), ROLBYTE (bytes), ROLWORD (words). The YAML's own surrounding text agrees: description says "reads the word identified by Num (0-1) from Src", result says "Word Num (0-1) of Src ... is rotated left", and "Num (0-1) identifies a value's individual words, by position, in least-significant word order." Only line 19 deviates, calling N a "nibble ID." A 32-bit value holds exactly two 16-bit words, matching the 1-bit N field (encoding 0NI), whereas it holds eight nibbles (which …

**Authority cited:** deliverables/ai/P2/language/pasm2/rolword.yaml line 19 ("Num is a 1-bit literal identifying the nibble ID (0-1) of Src to read."); manual opus-master/part-ii/instructions-r.md line 1203 ("N is a 1-bit literal (0-1) identifying the word position in Src."); Silicon Doc p2-documentation.txt lines …

**Proposed correction (verify first):** Edit rolword.yaml line 19 to read: "Num is a 1-bit literal identifying the word ID (0-1) of Src to read." (replace "nibble" with "word"). Matches the auditor's proposed correction.

### F-061 — `setbyte.yaml`: The manual is correct (N selects a byte, 0-3). The matching SETBYTE YAML mislabels the N …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-090)

**File(s):** `setbyte.yaml`

**What the KB says (suspect):** setbyte.yaml parameters list reads: 'Num is a 2-bit literal identifying the nibble ID (0-3) of Dest to modify.' — it labels the SETBYTE N operand a 'nibble' ID instead of a 'byte' ID.

**Truth per manual-audit authority:** SETBYTE indexes one of 4 BYTES with a 2-bit field. The encoding reference (line 363) labels the field NN with operand `#0..3` and description "Set a byte to new value"; the Silicon Doc (line 1138) says "set byte to value". The manual (line 166) correctly says "byte". The YAML (setbyte.yaml:18) says "nibble ID" — wrong word for a byte-setting instruction. Internal proof of the copy-paste artifact: the manual's SETNIB entry (line 475) uses a 3-bit literal (0-7) for true nibble selection; a 2-bit/0-3 index labeled "nibble" is inconsistent, matching the auditor's theory that the wording was copied from a nib-family …

**Authority cited:** Manual: engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-s.md:166 ("N is a 2-bit literal (0-3) identifying the byte of Dest to modify.") and :181 (prose: "SETBYTE stores Src[7:0] into the byte identified by N"). YAML: …

**Proposed correction (verify first):** In deliverables/ai/P2/language/pasm2/setbyte.yaml line 18, change "Num is a 2-bit literal identifying the nibble ID (0-3) of Dest to modify." to "Num is a 2-bit literal identifying the byte ID (0-3) of Dest to modify." (i.e. replace the word "nibble" with "byte"). YAML-side fix; record in the P2KB corrections register. No manual change needed — manual line 166 is already correct.

### F-062 — `signx.yaml`: SIGNX is Sign Extend and the manual correctly says 'sign-extend beyond'; the YAML wrongly …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-091)

**File(s):** `signx.yaml`

**What the KB says (suspect):** YAML signx.yaml parameters list reads: 'Src is a register or 9-bit literal whose value (lower 5 bits) identifies the bit of Dest to zero-extend beyond.'

**Truth per manual-audit authority:** SIGNX is the Sign Extend instruction; it fills bits above Src[4:0] with the identified bit's value (sign-extension), per signx.yaml lines 3 ("Sign extend"), 6-7, 13, 16, 47. The manual (instructions-s.md:998) correctly says "sign-extend beyond." The YAML's Src-parameter line 19 alone says "zero-extend beyond," which is ZEROX behavior — an internal contradiction with the rest of its own entry. Manual quote and YAML quote both verified verbatim as the finding states.

**Authority cited:** deliverables/ai/P2/language/pasm2/signx.yaml:19 (Src param "to zero-extend beyond"), cross-checked against same file's own description (line 6-7 "sign-extending the value"), result (line 13 "sign-extended"), Dest param (line 16 "sign-extend above bit Src[4:0]"), and oneliner (line 47 "Sign-extend …

**Proposed correction (verify first):** Edit signx.yaml line 19 to read "...identifies the bit of Dest to sign-extend beyond." (change "zero-extend" to "sign-extend"). Routes to the P2KB corrections register. Manual needs no change.

### F-063 — `waitxro.yaml`: WAITXRO is an unbounded blocking event-wait (clocks 2+), so timing.type: fixed is wrong; …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-094)

**File(s):** `waitxro.yaml`

**What the KB says (suspect):** waitxro.yaml declares timing.type: fixed, while every other WAIT* event-wait YAML in this set declares type: variable (and waitxro's own encoding clocks is '2+').

**Truth per manual-audit authority:** WAITXRO is an unbounded blocking event-wait: manual line 374 "stalling the pipeline until the event flag is set" and encoding clocks "2+" (manual line 367, yaml line 35). Every one of the 15 sibling WAIT* event-wait instructions with identical "2+" semantics declares timing.type: variable; waitxro.yaml is the sole outlier at type: fixed. Its own clocks field "2+" contradicts "fixed". The directly analogous waitxrl/waitxfi/waitxmt streamer-event siblings are all variable. The manual carries no timing.type field (only a Clks column showing 2+), so the manual is correct and self-consistent; only the YAML is wrong.

**Authority cited:** deliverables/ai/P2/language/pasm2/waitxro.yaml:30-32 (timing: {cycles: 2, type: fixed}) and :35 (clocks: '2+'); sibling YAMLs all timing.type=variable — waitatn, waitse1-4, waitpat, waitfbw, waitint, waitxfi, waitxmt, waitxrl, waitct1-3, waitx (grep over deliverables/ai/P2/language/pasm2/*.yaml); …

**Proposed correction (verify first):** In deliverables/ai/P2/language/pasm2/waitxro.yaml, change the timing block from `type: fixed` to `type: variable` (leave cycles: 2 and encoding clocks: 2+ as-is). This brings WAITXRO into agreement with all 15 sibling WAIT* event-wait instructions and with its own clocks "2+" / blocking description. No manual edit required.

### F-064 — `waitx.yaml`: The Result line states 'Sets C and Z to 0 after completion' unconditionally, but flag …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-095)

**File(s):** `waitx.yaml`

**What the KB says (suspect):** waitx.yaml flags_affected: C/Z 'Set to 0 after completion'; encoding bits CZL ... c:0 z:0 — i.e. C and Z are only written when an effect (WC/WZ/WCZ) is requested, as the manual's own following bullet states.

**Truth per manual-audit authority:** The compiler emits the WAITX instruction word with C and Z effect bits = 0 when no WC/WZ/WCZ is given, and only sets C and/or Z when the corresponding effect is requested. Per universal P2 semantics, the C/Z flag registers are written only when those instruction-word bits are 1. Therefore "Sets C and Z to 0 after completion" happens ONLY with WC/WZ/WCZ, NOT unconditionally. Manual line 231 states it unconditionally (wrong); manual line 234 correctly conditions it on WC/WZ/WCZ. The encoding column at :239 even shows the C/Z effect cells, but the Result prose is unqualified.

**Authority cited:** pnut-ts v1.55.0 probe (/tmp/waitx2.bin decoded): WAITX #99 -> C=0,Z=0; WAITX #99 WC -> C=1,Z=0; WAITX #99 WZ -> C=0,Z=1; WAITX #99 WCZ -> C=1,Z=1 (offsets 0x240d–0x2419, op=1101011, S=000011111). Manual: …

**Proposed correction (verify first):** Manual (instructions-w.md:231): change the Result line to qualify the flag clear, e.g. "Stalls the cog for 2 + Dest clock cycles. If WC/WZ/WCZ is specified, waits 2 + (Dest AND RND) clocks for a randomized delay and clears C and Z to 0 after completion." (i.e. remove the standalone unconditional "Sets C and Z to 0" and fold it into the WC/WZ/WCZ clause, matching the line-234 bullet). YAML (waitx.yaml): same fix — …

### F-065 — `wfbyte.yaml`: The YAML description fields contain a column-bleed artifact (Clks value '2' + 'FIFO IN …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-097)

**File(s):** `wfbyte.yaml`, `wflong.yaml`, `wfword.yaml`

**What the KB says (suspect):** The authoritative YAML description fields are garbled extraction artifacts carrying a stray '2 / FIFO IN USE' tail: wfbyte.yaml description = 'Used after WRFAST. Write byte in D[7:0] into FIFO. 2 / FIFO IN USE' (same in wflong.yaml and wfword.yaml).

**Truth per manual-audit authority:** wfbyte.yaml line 12-13: `description: Used after WRFAST. Write byte in D[7:0] into FIFO. 2` continued on line 13 ` / FIFO IN USE` — this is a single YAML scalar that parses to "Used after WRFAST. Write byte in D[7:0] into FIFO. 2 / FIFO IN USE". The trailing "2" duplicates the already-structured clocks:'2' field (line 8), and "FIFO IN USE" is a source-table availability note. Both are column-bleed from PASM2 Manual table extraction, not prose. The manual prose (instructions-w.md:405) is independent and correct: "WFBYTE writes a byte from Dest[7:0] into the Hub FIFO interface. This instruction must be used after …

**Authority cited:** deliverables/ai/P2/language/pasm2/wfbyte.yaml:12-13 (description bleeds "...into FIFO. ⟨pad⟩ 2\n / FIFO IN USE"); wflong.yaml:12-13 and wfword.yaml:12-13 identical pattern. Manual clean text at …

**Proposed correction (verify first):** In wfbyte.yaml, wflong.yaml, and wfword.yaml, fix the description scalar to drop the trailing "2 / FIFO IN USE" bleed (and the wrapped continuation line). Targets: wfbyte → "Used after WRFAST. Write byte in D[7:0] into FIFO."; wflong → "Used after WRFAST. Write long in D[31:0] into FIFO."; wfword → "Used after WRFAST. Write word in D[15:0] into FIFO." Route to the P2KB corrections register; no manual edit needed.

### F-066 — `wmlong.yaml`: Manual and wmlong.yaml agree on `3...10`; the encoding-reference row shows a bare `3` and …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-099)

**File(s):** `wmlong.yaml`

**What the KB says (suspect):** PASM2-ENCODING-REFERENCE.md lists WMLONG clocks as bare `3` (no range); wmlong.yaml encoding.clocks = `3...10 *`

**Truth per manual-audit authority:** The authoritative P2 Instructions v35 CSV gives WMLONG the SAME timing as WRLONG: cog 3...10, hub-exec 3...20 (CSV:172 vs CSV:247). The manual (instructions-w.md:492 = "3...10"; appendix-a:367 = "3...10 *") and wmlong.yaml:8 ("3...10 *") both agree with the CSV. PASM2-ENCODING-REFERENCE.md:250 records a bare "3", which contradicts the CSV ground truth and the reference's OWN convention — its WRLONG row (PASM2-ENCODING-REFERENCE.md:252), plus PUSHA/PUSHB (lines 245-246), all correctly show "3...10 (cog) / 3...20 (hub-exec)" for the identical hub-write timing. WMLONG is the lone row that drops the range. Manual …

**Authority cited:** Canonical timing: engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:172 (WMLONG clocks = "3...10 *", "3...20 *", "3...18 *", "3...38 *"). Manual: opus-master/part-ii/instructions-w.md:492 (Clks = "3...10") and …

**Proposed correction (verify first):** In PASM2-ENCODING-REFERENCE.md:250, change the WMLONG clocks cell from `3` to `3...10 (cog) / 3...20 (hub-exec)` — matching the format used by the adjacent WRLONG/PUSHA/PUSHB rows and the CSV ground truth (3...10 * / 3...20 *). The finding's proposed value "3...10" is directionally correct but should carry the cog/hub-exec breakout to stay consistent with the rest of that table.

### F-067 — `wrbyte.yaml`: Manual + wrbyte.yaml both carry the cog-vs-hub-exec range; the encoding-reference WRBYTE …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-100)

**File(s):** `wrbyte.yaml`

**What the KB says (suspect):** PASM2-ENCODING-REFERENCE.md WRBYTE row shows bare `3` (no cog/hub-exec range), while sibling WRLONG and WRWORD rows carry `3...10 (cog) / 3...20 (hub-exec)`; wrbyte.yaml timing.range = `3...10 / 3...20`

**Truth per manual-audit authority:** The canonical Parallax P2 Instructions v35 spreadsheet gives WRBYTE the identical cog/hub-exec timing pair as its siblings: line 245 WRBYTE = `3...10`(cog) `3...20`(hub-exec); line 246 WRWORD and 247 WRLONG = the same. So the true timing for WRBYTE is 3...10 (cog/LUT) / 3...20 (hub-exec). The manual states exactly this (3...10 † with the dagger context table), and wrbyte.yaml states exactly this (range 3...10 / 3...20). Only PASM2-ENCODING-REFERENCE.md:251 shows a bare `3`, which is both wrong against authority and internally inconsistent with its own WRLONG/WRWORD rows (:252-253) that carry the full range.

**Authority cited:** Canonical authority — P2 Instructions v35 spreadsheet: /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:245 (WRBYTE cols = 3...10 cog / 3...20 hub-exec), :246 (WRWORD), :247 (WRLONG). Corroborated by …

**Proposed correction (verify first):** In deliverables/ai/P2/language/PASM2-ENCODING-REFERENCE.md line 251, change the WRBYTE Clks cell from `3` to `3...10 (cog) / 3...20 (hub-exec)`, matching the WRLONG/WRWORD rows (:252-253), the canonical v35 spreadsheet, wrbyte.yaml, and the manual. (The auditor's proposedCorrection is exactly right.)

### F-068 — `org.yaml`: YAML restricts ORG to COG RAM only (0-$1FF). The manual's wider range (address up to …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-103)

**File(s):** `org.yaml`

**What the KB says (suspect):** pasm2/org.yaml gives range: 0-$1FF ('Cog RAM address (0-511)'), omitting LUT RAM ($200-$3FF) entirely; spin2 org.yaml gives only 'ORG address' with no range.

**Truth per manual-audit authority:** Spin2 v51 spec, the canonical authority, explicitly assembles ORG into LUT RAM: line 1489 "ORG $200 'SET COG-EXEC MODE, COG ADDRESS = $200, COG LIMIT = $400 (LUT, DEFAULT LIMIT)" and line 1491 "ORG $300,$380 ... (LUT)". The manual (directives.md:48 "COG or LUT RAM address"; :60 "0 to $400") matches this exactly, including the auto-limit behavior (<$200→$200, >=$200→$400). pnut-ts compiled `ORG $200` and `ORG $300` cleanly. The YAML (org.yaml:14 "range: 0-$1FF", :30 "ORG affects cog RAM addresses only (0-$1FF)") is therefore the defect — it omits LUT RAM that ORG legitimately addresses.

**Authority cited:** Spin2 v51 narrative: /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/spin2-v51/spin2-v51-narrative.txt:1489-1491 (ORG into LUT). Manual: opus-master/part-ii/directives.md:48,60 (range 0 to $400, COG/LUT). YAML defect: deliverables/ai/P2/language/pasm2/org.yaml:14-15,30 (range 0-$1FF; …

**Proposed correction (verify first):** In deliverables/ai/P2/language/pasm2/org.yaml: change parameter `range: 0-$1FF` (line 14) to `0-$3FF` and description (line 15) to "COG/LUT RAM address (0-1023)"; revise note (line 30) from "ORG affects cog RAM addresses only (0-$1FF)" to "ORG addresses COG RAM (0-$1FF) and LUT RAM ($200-$3FF), setting COG-exec mode; auto-limit is $200 for COG-region addresses and $400 for LUT-region addresses." Optionally add the …

### F-069 — `fit.yaml`: The bare-ORG default limit of $1F8 and the conditional $200/$400 auto-limit logic have no …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-104)

**File(s):** `fit.yaml`, `org.yaml`

**What the KB says (suspect):** Neither pasm2/org.yaml nor spin2 org.yaml documents any auto-limit behavior or a $1F8 bare default. The only adjacent datum, pasm2/fit.yaml:27, says the FIT default cog limit is $200 (not $1F8).

**Truth per manual-audit authority:** All three manual claims are empirically TRUE per the compiler (FIT/assembler "Cog address exceeds limit (m110)" boundary tests): 1. Bare ORG -> limit $1F8: `ORG`/`res $1F8` compiles (Wrote .bin/Done); `res $1F9` errors. Manual line 67 ("limit $1F8") CONFIRMED. 2. ORG addr<$200 -> limit $200: `ORG $10`/`res $1F0` (final addr $200) compiles; `res $1F1` (final $201) errors. Manual line 72 CONFIRMED. 3. ORG addr>=$200 -> limit $400: `ORG $200`/`res $200` (final $400) compiles; `res $201` (final $401) errors. Manual line 73 CONFIRMED. Manual quotes are accurately represented (verified at directives.md:63-76). …

**Authority cited:** pnut-ts v1.55.0 compiler probes (ground truth) + manual + YAML. Manual: opus-master/part-ii/directives.md:63-76 (Auto-Limit Behavior) and :112 (Pitfall). YAML: deliverables/ai/P2/language/pasm2/org.yaml:1-37 (no auto-limit, range stated 0-$1FF); deliverables/ai/P2/language/pasm2/fit.yaml:26 ("FIT …

**Proposed correction (verify first):** No change to the manual — its $1F8 / $200 / $400 figures are correct (compiler-verified). Apply the YAML half of the auditor's proposal: extend deliverables/ai/P2/language/pasm2/org.yaml to (a) document the auto-limit behavior — bare ORG -> limit $1F8; ORG addr<$200 -> limit $200; ORG addr>=$200 -> limit $400; ORG addr,limit -> explicit — and (b) correct the address range/parameters to cover the full 0-$400 COG+LUT …

### F-070 — `orgf.yaml`: Direct contradiction: manual says ORGF is COG-mode-only and errors in ORGH mode; YAML …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-105)

**File(s):** `orgf.yaml`

**What the KB says (suspect):** pasm2/orgf.yaml declares the address range '0-$1FF (cog) or hub address' and 'Target address to advance to ... hub' — explicitly contemplating ORGF advancing to a HUB address, with no ORGH-mode restriction.

**Truth per manual-audit authority:** The pnut-ts compiler emits, verbatim, "ORGF is not allowed in ORGH mode" — the exact string the manual quotes at line 165 — and rejects ORGF after ORGH. ORGF after ORG compiles. Therefore the manual's claims (COG-mode-only; errors in ORGH mode; pitfall text) are all CORRECT vs the highest authority. The YAML at orgf.yaml:17 declares range "0-$1FF (cog) or hub address" and :18 "Target address to advance to, filling intervening space with zeros" — the "or hub address" clause asserts ORGF accepts a hub target, which the compiler refutes. The YAML is the sole defect.

**Authority cited:** pnut-ts v1.55.0 probe (ground truth): hub-mode case `DAT / ORGH $400 / long / ORGF $410` → `orgf_hub.spin2:4:error:ORGF is not allowed in ORGH mode`; cog-mode case `DAT / ORG 0 / nop / ORGF $10 / nop` → clean compile (Wrote orgf_cog.bin). Manual: …

**Proposed correction (verify first):** Fix deliverables/ai/P2/language/pasm2/orgf.yaml only (manual needs no change). Line 17: drop "or hub address" — change `range: 0-$1FF (cog) or hub address` to a COG-only form, e.g. `range: 0-$1FF (cog mode only; ORGF is not valid in ORGH/hub mode)`. Add a note/restriction documenting that ORGF is rejected with "ORGF is not allowed in ORGH mode" when used after ORGH (mirroring the existing RES treatment). The notes …

### F-071 — `orgf.yaml`: The manual contradicts itself: the parameter table permits a hub address, but the prose …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-106)

**File(s):** `orgf.yaml`

**What the KB says (suspect):** pasm2/orgf.yaml:17 mirrors the same '(cog) or hub address' phrasing, suggesting the parameter line was copied from YAML while the COG-only Notes came from elsewhere.

**Truth per manual-audit authority:** The internal contradiction is real and verified. Manual line 138 says address is "cog 0-$1FF or hub address" while lines 165/172/178 correctly state ORGF is COG-mode-only ("ORGF is not allowed in ORGH mode", "only valid in COG mode (after ORG), not in Hub mode"). The compiler settles which half is authoritative: ORGF is COG-ONLY — pnut-ts emits "ORGF is not allowed in ORGH mode" verbatim. So the "or hub address" clause on line 138 is FALSE; the COG-only prose is correct. The YAML carries the identical false clause at orgf.yaml:17 ("range: 0-$1FF (cog) or hub address") and its notes (lines 46-51) never document …

**Authority cited:** pnut-ts v1.55.0 probe (ground truth): ORGH+ORGF → "orgf_hub.spin2:4:error:ORGF is not allowed in ORGH mode"; ORG+ORGF → clean compile (wrote orgf_cog.bin). Manual: engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/directives.md:138 (param), :165 (restriction), …

**Proposed correction (verify first):** Manual directives.md:138 — change the parameter description to "Target COG address to advance to (0-$1FF), filling intervening space with zeros" and drop "or hub address" (ORGF is COG-only; hub use errors). This makes line 138 consistent with the already-correct restriction/note/pitfall (lines 165/172/178). ALSO fix the YAML (route to P2KB corrections register): orgf.yaml:17 change "range: 0-$1FF (cog) or hub …

### F-072 — `orgh.yaml`: The two authoritative YAMLs disagree on the bare-ORGH default (one $400, one …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-107)

**File(s):** `orgh.yaml`

**What the KB says (suspect):** pasm2/orgh.yaml:24 says flatly 'Default address is $400 if not specified' with no Spin2/PASM distinction. spin2 orgh.yaml says bare ORGH 'continues from current hub address' and default 'Current location'. The two YAMLs contradict each other.

**Truth per manual-audit authority:** The Spin2 v51 spec explicitly defines bare ORGH by context: in Spin2+PASM programs "DAT ORGH 'SET HUB-EXEC MODE AND SET ORIGIN TO $400" (narrative:1547), and in PASM-Only programs "DAT ORGH 'SET HUB-EXEC MODE AT CURRENT HUB ADDRESS" (narrative:1555). The manual (directives.md:213-214) states exactly this: "In Spin2 objects: Sets hub address to $400" / "In PASM-only objects: Sets hub address to current object position" — so the MANUAL is correct against authority. The two YAMLs each capture only one half and state it absolutely: pasm2/orgh.yaml:24 "Default address is $400 if not specified" (true only for Spin2 …

**Authority cited:** Spin2 v51 narrative (highest available authority for directive semantics): /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/spin2-v51/spin2-v51-narrative.txt:1547 ("DAT ORGH 'SET HUB-EXEC MODE AND SET ORIGIN TO $400" — under Spin2+PASM Programs) and :1555 ("DAT ORGH 'SET HUB-EXEC MODE AT …

**Proposed correction (verify first):** Keep the manual as-is (it is correct). Reconcile both YAMLs to the contextual rule from Spin2 v51 narrative:1547/1555. In pasm2/orgh.yaml replace the absolute note "Default address is $400 if not specified" with two-context wording: "Bare ORGH default depends on object type: $400 in Spin2+PASM objects (after interpreter); continues from the current hub address in PASM-only objects." In …

### F-073 — `orgh.yaml`: YAML lacks any hub address ceiling, so the constraint is unverifiable; additionally the …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-108)

**File(s):** `orgh.yaml`

**What the KB says (suspect):** Neither pasm2/orgh.yaml nor spin2 orgh.yaml documents a maximum hub address or a $100000 ceiling. Note: $100000 = 1MB exceeds the P2's 512KB ($80000) physical hub RAM.

**Truth per manual-audit authority:** pnut-ts probe: `ORGH $400, $100004` emits exactly "Hub address exceeds $100000 ceiling (m361)" and the binary contains that literal string (m360/m361). The manual's claimed range ($400..$100000) and its quoted error text at directives.md:282 are therefore VERBATIM correct vs the highest authority. The finding's worry that $100000 "exceeds physical hub RAM ($80000)" conflates two distinct PNut checks: PNut independently enforces a $100000 address-SPACE ceiling AND a 512KB physical-RAM check ("Program requirement exceeds 512KB hub RAM"). The manual correctly documents the ceiling; it never claims data can fill to …

**Authority cited:** pnut-ts v1.55.0 probe (/usr/local/bin/pnut-ts -d): (1) `strings /usr/local/bin/pnut-ts` shows the verbatim error "Hub address exceeds $100000 ceiling (m360/m361)" — confirming the manual quotes a real PNut message; (2) `ORGH $400, $100004` => "error: Hub address exceeds $100000 ceiling (m361)" — …

**Proposed correction (verify first):** Do NOT change the manual — its $400..$100000 range and "Hub address exceeds $100000 ceiling" error text are verbatim-accurate against pnut-ts v1.55.0. Route the fix to the YAML: enrich deliverables/ai/P2/language/pasm2/orgh.yaml to document the verified behavior — default origin $400; optional `limit` operand (ORGH address, limit); the $100000 (1MB) address-space ceiling enforced by PNut (error "Hub address exceeds …

### F-074 — `byte.yaml`: YAML one-line descriptions state these store into Hub memory, but the manual (correctly) …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-109)

**File(s):** `byte.yaml`, `long.yaml`, `word.yaml`

**What the KB says (suspect):** spin2/.../byte.yaml:3 'Insert byte data into Hub memory'; word.yaml:3 'into Hub memory'; long.yaml:3 'into Hub memory' — each describes these directives as Hub-memory-only.

**Truth per manual-audit authority:** pnut-ts proves BYTE/WORD/LONG assemble data wherever the current origin points: `ORG $100` puts the LONG table in the COG-RAM image and compiles with exit 0 ("Wrote af109b.bin", "Done"). The manual correctly demonstrates this (directives.md:87, with :110 explicitly describing ORG mode-switching). The cited YAML descriptions — byte.yaml:3 / word.yaml:3 / long.yaml:3 "Insert ... data into Hub memory at assembly time" — are an over-narrow generalization that is empirically false: these directives are not Hub-memory-only.

**Authority cited:** pnut-ts v1.55.0 probe (highest authority): `DAT / ORG $100 / table long 1,2,3` compiles clean — "Wrote af109b.bin ... Done", exit 0 (COG-mode LONG assembles fine); aligned BYTE/WORD after ORG $100 also compile clean (af109c.bin). Manual: opus-master/part-ii/directives.md:87 (`table long 1, 2, 3` …

**Proposed correction (verify first):** Broaden the YAML for byte.yaml / word.yaml / long.yaml so the destination is mode-relative, not Hub-only. Change `description:` (line 3) to e.g. "Insert byte/word/long data into the assembly image at the current origin (COG, LUT, or Hub depending on ORG/ORGH mode) at assembly time." ALSO fix the `usage:` blocks (byte.yaml:10ff, and the matching word/long usage text), which currently repeat "stored in Hub memory" — …

### F-075 — `file.yaml`: Contradiction on whether path separators are permitted: manual forbids '/' and other path …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-110)

**File(s):** `file.yaml`

**What the KB says (suspect):** spin2/.../file.yaml:14 'The file path is relative to the source file location.' — implying a path (with separators) may be supplied relative to the source, conflicting with the manual's 'no path separators allowed'.

**Truth per manual-audit authority:** COMPILER PROBE settles it. (1) FILE "data.bin" (simple name, file present) compiles clean, exit 0, "Wrote t1.bin". (2) FILE "sub/nested.bin" with the target file actually existing at sub/nested.bin -> "t2.spin2:4:error:Invalid filename character" — the '/' is rejected outright, NOT a not-found error. (3) Every character in the manual's invalid table ('/' ':' '*' '?' '<' '>' '|') independently produces "Invalid filename character". This is exactly what the manual states (directives.md:473,477-488). Therefore the MANUAL is CORRECT and verified. The YAML (file.yaml:13-15) says "The file path is relative to the …

**Authority cited:** pnut-ts v1.55.0 probe (highest authority); manual directives.md:473-495; deliverables/ai/P2/language/spin2/assembly-directives/file.yaml:11-19; Spin2 v51 spec spin2-v51-narrative.txt:1431 (FILE "FILENAME" form only).

**Proposed correction (verify first):** Overturn auditor's defectSide "both" -> defect is YAML-only. Manual needs NO change (it is correct per pnut-ts). Fix deliverables/ai/P2/language/spin2/assembly-directives/file.yaml: remove the sentence "The file path is relative to the source file location." from the `usage:` field. Replace with the verified behavior: the filename must be a bare name with no path separators or other invalid characters (/ : * ? " < > …

### F-076 — `file.yaml`: The 253-char limit, case-insensitivity, and invalid-character list have no confirming …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-111)

**File(s):** `file.yaml`

**What the KB says (suspect):** spin2/.../file.yaml documents none of these — no max length, no case rule, no invalid-character list. It loosely supports DAT-only via 'used in DAT sections' (line 10).

**Truth per manual-audit authority:** Compiler probes settle the four claims: (1) Invalid-char list CONFIRMED — `file "bad:name.txt"` and `* ? < > | /` each yield "error:Invalid filename character"; exact-match names compile clean. (2) DAT-only CONFIRMED — FILE inside a PUB inline-PASM block yields "Expected instruction, directive, BYTE/WORD/LONG, or END"; in DAT it compiles. (3) Case-insensitivity REFUTED on this platform — disk file is lowercase `file_test.txt`; referencing `"FILE_TEST.TXT"` yields "error:DAT file not found [FILE_TEST.TXT] (preload)", while the exact-case reference compiles. The compiler does a case-SENSITIVE OS filesystem lookup …

**Authority cited:** pnut-ts v1.55.0 empirical probes (ground truth) + manual part-ii/directives.md:475-540 + deliverables/ai/P2/language/spin2/assembly-directives/file.yaml:1-39. NOTE: the cited YAML path in the finding (spin2/.../file.yaml:1-39) is correct; the file is 39 lines and documents only loose DAT usage …

**Proposed correction (verify first):** Two-sided fix. (a) MANUAL (directives.md:539): the "Filename matching is case-insensitive" claim is wrong on case-sensitive filesystems (Linux). Either remove it or rewrite as platform-dependent, e.g. "Filename case-matching follows the host OS filesystem (case-insensitive on Windows; case-sensitive on Linux/macOS-case-sensitive volumes)." Also flag the 253-char limit (directives.md:538) as NEEDS-VERIFICATION until …

### F-077 — `fit.yaml`: The manual omits the no-argument FIT form that the authority documents (defaults to the …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-116)

**File(s):** `fit.yaml`

**What the KB says (suspect):** "FIT without parameter checks for cog RAM limit ($200)"; authority example shows a bare FIT form: 'FIT // Default: ensure fits in cog RAM (< $200)'.

**Truth per manual-audit authority:** The finding's premise is false. The cited authority (fit.yaml) claims a bare `FIT` form defaulting to $200, but that form does NOT assemble: pnut-ts (highest authority) rejects bare `FIT` with a syntax error and accepts `FIT $200`. The Spin2 v51 grammar confirms `"FIT" address` is mandatory (contrast `"ORG" [address]` which IS optional). The manual correctly documents the limit as required and is NOT deficient. The defect lives in fit.yaml, which fabricates an optional/default form. The auditor's defectSide guess of "manual" is overturned.

**Authority cited:** pnut-ts v1.55.0 probe: bare `FIT` (DAT/ORG 0/MOV/FIT) → "fittest.spin2:4:error:Expected a constant, unary operator, or \"(\"", EXIT=1; `FIT $200` → "Wrote fittest2.bin", EXIT=0. Spin2 v51 grammar: engineering/ingestion/sources/spin2-v51/spin2-grammar-reference.md:295-296 `directive ::= "ORG" …

**Proposed correction (verify first):** Do NOT change the manual — it is correct that FIT requires a limit operand. Instead, correct deliverables/ai/P2/language/pasm2/fit.yaml: change syntax `FIT [address]` to `FIT address`; remove the note "FIT without parameter checks for cog RAM limit ($200)"; and remove the example `FIT // Default: ensure fits in cog RAM (< $200)`. These describe a bare-FIT form that pnut-ts v1.55.0 rejects and that the Spin2 v51 …

### F-078 — `getct.yaml`: Three errors: (a) '64-bit' contradicts the 32-bit authority; (b) 'upper 32 bits with WC' …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-119)

**File(s):** `getct.yaml`, `special_registers.yaml`

**What the KB says (suspect):** CT is 32-bit. special_registers.yaml: 'width: 32-bit, free-running'. spin2/methods/getct.yaml: 'Get the current 32-bit system counter value... Wraps from $FFFF_FFFF to $0000_0000 ~every 21 seconds at 200MHz.' PASM2 getct.yaml encoding 'GETCT D {WC}' lists c: same / 'C: Unchanged' — WC does not load upper counter bits.

**Truth per manual-audit authority:** All three of the manual's sub-claims are corroborated by the highest authorities. (a) "64-bit": Silicon Doc OVERVIEW "64-bit free-running counter which increments every clock"; Spin2 v51 §2307 "64-bit system counter". (b) "lower 32 bits by default, upper 32 bits with WC": Silicon Doc verbatim "CT is the lower 32-bits of the free-running 64-bit global counter" and "GETCT WC retrieves upper 32-bits"; pnut-ts confirms GETCT D WC assembles to a distinct encoding (C bit set), so the WC form is NOT fabricated. (c) "(Rev B/C silicon)": the 64-bit extension was the documented Rev B respin change ("System counter …

**Authority cited:** Manual: opus-master/part-ii/special-registers.md:533 (quote confirmed verbatim). Silicon Doc (v35, Rev B/C): p2-documentation.txt:81 "System counter extended to 64 bits. GETCT WC retrieves upper 32-bits."; p2-documentation.txt:5131 / part2-video-output.txt:361 "CT is the lower 32-bits of the …

**Proposed correction (verify first):** Do NOT change the manual — its line 533 is correct and the proposed rewrite would inject three errors into accurate text. Instead, route a P2KB corrections-register fix to the YAMLs: (1) special_registers.yaml:61 change "width: 32-bit, free-running" to reflect that CT is the lower 32 bits of a free-running 64-bit system counter; (2) pasm2/getct.yaml: document the WC variant — add that `GETCT D WC` retrieves the …

### F-079 — `clock_system.yaml`: Two YAMLs in the data set give different widths for the same counter; the 32-bit value is …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-120)

**File(s):** `clock_system.yaml`, `getct.yaml`, `special_registers.yaml`

**What the KB says (suspect):** clock_system.yaml:242 'getct_instruction: Read 64-bit system counter' and :269 'counter_system: 64-bit free-running counter' contradict special_registers.yaml:62 (32-bit) and spin2/methods/getct.yaml (32-bit, wraps at $FFFF_FFFF).

**Truth per manual-audit authority:** The P2 system counter IS 64-bit (Rev B/C silicon). Silicon Doc states it directly and repeatedly: "System counter extended to 64 bits. GETCT WC retrieves upper 32-bits" and "64-bit free-running counter which increments every clock, cleared on reset". The auditor inverted the polarity: it labeled the 64-bit YAML (clock_system.yaml:242,269) as the defect and called special_registers.yaml:62 (32-bit) "silicon truth." The opposite is true. The manual at special-registers.md:533 ("free-running 64-bit counter (Rev B/C silicon) ... GETCT returns the lower 32 bits by default, or the upper 32 bits with WC") is CORRECT …

**Authority cited:** Silicon Doc (highest available authority here — encoding-internal counter width is not compiler-probeable): engineering/ingestion/sources/silicon-doc/silicon-doc-complete-sample.txt:1 ("System counter extended to 64 bits. GETCT WC retrieves upper 32-bits." and "64-bit free-running counter which …

**Proposed correction (verify first):** Do NOT edit clock_system.yaml (its 64-bit labels are correct). Instead, fix deliverables/ai/P2/language/pasm2/concepts/special_registers.yaml:62 from "width: 32-bit, free-running" to "width: 64-bit free-running (Rev B/C silicon); GETCT returns low 32 bits by default, upper 32 bits with WC". Optionally note in spin2/methods/getct.yaml that the underlying counter is 64-bit and GETCT() reads the low 32 bits, to remove …

### F-080 — `addressing_modes.yaml`: Half the claim is corroborated (-32..+31). The '1 to 16' updating range is unverifiable …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-125)

**File(s):** `addressing_modes.yaml`

**What the KB says (suspect):** addressing_modes.yaml:48 documents 'index_range: -32 to +31 (5-bit signed)' for non-updating indexed (MATCHES the first clause). No YAML in the data set states the '1 to 16' updating-form range; setq_block_ops.yaml and the PTR concept files do not specify it.

**Truth per manual-audit authority:** The manual's exact text (special-registers.md:249) is "Index ranges: -32 to +31 for non-updating indexed; 1 to 16 for updating forms." The Silicon Doc states BOTH legs verbatim: "INDEX6 = -32..+31 for non-updating offsets" and "INDEX = 1..16 for ++'s and --'s" (part3-end.txt:180-181), with the encoding "NNNNN = INDEX, uses %00001..%01111 for 1..15 and %00000 for 16" (:186). The manual reproduces the authority exactly. The auditor's discrepancy speculation ("P2 hardware uses a 4-bit signed auto-update index of -16..+15; '1 to 16' looks like only the positive sub-range and may be imprecise") is itself wrong: the …

**Authority cited:** Silicon Doc: /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/silicon-doc/part3-end.txt:180-181 ("INDEX6 = -32..+31 for non-updating offsets" / "INDEX = 1..16 for ++'s and --'s") and :186 ("NNNNN = INDEX, uses %00001..%01111 for 1..15 and %00000 for 16"). Manual: …

**Proposed correction (verify first):** Refute the "unverifiable / may be imprecise" claim — the manual's "1 to 16 for updating forms" is exactly correct per Silicon Doc part3-end.txt:181,186 and needs no change. The only actionable item is the YAML findability gap the auditor noticed: addressing_modes.yaml documents index_range only for the non-updating offset leg (line 47) and omits it from the post_modify/auto-update entry (lines 74-81). Add to that …

### F-081 — ch02-instruction-format: The manual documents EEEE=0000 solely as _RET_ and omits the authority-documented nuance …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-130)

**File(s):** (file not named — see source finding)

**What the KB says (suspect):** The encoding reference note: '%0000 is the disassembler edge case: with no WC/WZ it is the _RET_ form (always-execute + return); the assembler shows the bare prefix as IF_NEVER only when flags are written. %1111 is the default (always), printed with no IF_ prefix.'

**Truth per manual-audit authority:** The cited authority (PASM2-ENCODING-REFERENCE.md:49-52) claims for %0000: "the assembler shows the bare prefix as IF_NEVER only when flags are written." Compiler probe refutes this: in pnut-ts v1.55.0, IF_NEVER assembles to EEEE=1111 BOTH without flags (`01 02 04 f6`) AND with WC written (`01 02 14 f6`) — never to %0000. The %0000 form is produced exclusively by the `_RET_` prefix (`01 02 04 06` / `01 02 14 06`). IF_NEVER and _RET_ are distinct; IF_NEVER is simply an accepted alias mapping to %1111 (always). The manual's §2.2 and Appendix B are CORRECT (%0000=_RET_, %1111=IF_ALWAYS). The finding's premise — that …

**Authority cited:** pnut-ts v1.55.0 probes (ground truth): `if_never mov x,#1` → bytes `01 02 04 f6` = word 0xF6040201 → EEEE=1111; `if_never mov x,#1 wc` → `01 02 14 f6` → EEEE=1111; `_ret_ mov x,#1` → `01 02 04 06` → EEEE=0000; `_ret_ mov x,#1 wc` → `01 02 14 06` → EEEE=0000; bare `mov` (with/without WC) → …

**Proposed correction (verify first):** Do NOT edit the manual (the manual-side finding is a false positive — §2.2/Appendix B are correct). Instead fix the SOURCE: PASM2-ENCODING-REFERENCE.md:49-52. The note conflates IF_NEVER with %0000. Empirically (pnut-ts v1.55.0) IF_NEVER → EEEE=1111 in all cases (with or without WC/WZ), identical to the bare always form; %0000 is the `_RET_` prefix only. Replace the note with: "%0000 is the `_RET_` form …

### F-082 — `adds.yaml`: The manual describes ADDS/SUBS C two contradictory ways across §3.4.1 and §3.7.1. The …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-139)

**File(s):** `adds.yaml`, `subs.yaml`

**What the KB says (suspect):** Encoding authority: ADDS 'c: sign of (D + S)', SUBS 'c: sign of (D - S)' — the (true) sign of the result, matching §3.7.1's 'True sign of result', not 'signed overflow'. The same YAMLs' flags_affected/description use the looser 'signed overflow (signed carry)' phrasing, which contradicts their own encoding c: field.

**Truth per manual-audit authority:** The official P2 instruction spreadsheet defines ADDS C = "correct sign of (D + S)" and SUBS C = "correct sign of (D - S)", and Chip Gracey's clarification table lists ADDS/SUBS C Flag = "true sign". This is the corrected (overflow-aware) sign of the result — explicitly NOT "signed overflow occurred." Manual §3.4.1 (lines 289/291) labels ADDS/SUBS C as "Signed overflow occurred" and the prose at line 297 reinforces it as overflow detection, directly contradicting both the authority and the manual's own §3.7.1 (lines 551/560 "True sign of result"). The YAMLs likewise carry the looser "signed overflow (signed …

**Authority cited:** Authority (highest available): P2 Instructions v35 Rev B/C Silicon spreadsheet — engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv:36 (ADDS: "C = correct sign of (D + S)") and :40 (SUBS: "C = correct sign of (D - S)"); corroborated by …

**Proposed correction (verify first):** Manual: change §3.4.1 (chapter-03-flags.md:289 ADDS, :291 SUBS) C column from "Signed overflow occurred" to "True sign of result (corrected sign of D±S)", matching §3.7.1. Also fix the prose at :297 — ADDS/SUBS C does not flag overflow; it reports the corrected (true) sign of the signed result (the sign the value would have at full precision). YAML (routes to P2KB corrections register): adds.yaml flags_affected.C → …

### F-083 — `adds.yaml`: Prose asserts ADDS/SUBS C is a signed-overflow flag. Per the encoding authority the C …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-140)

**File(s):** `adds.yaml`, `subs.yaml`

**What the KB says (suspect):** ADDS C = sign of (D + S) (the result's true sign), per the encoding table; SUBS C = sign of (D - S). It is the true sign of the result, not a classic signed-overflow (V) flag.

**Truth per manual-audit authority:** P2 v35 instruction tables are unambiguous: ADDS sets "C = correct sign of (D + S)" and SUBS sets "C = correct sign of (D - S)" — the true sign (bit 31) of the result, NOT a classic signed-overflow (V) flag. The manual at lines 289/291/297 calls C a "signed overflow" detector and gives the overflow mental model ("two positives → negative = overflow"), which is wrong: C is just the result's sign regardless of whether overflow occurred. Crucially, the "Signed Overflow" wording appears ONLY in the P1 datasheet (p1-datasheet-v1.4 / P1-PropellerManual lines), confirming the manual conflated P1 semantics with P2. The …

**Authority cited:** Manual: opus-master/part-i/chapter-03-flags.md:289-291 (table rows "ADDS | Signed overflow occurred", "SUBS | Signed overflow occurred") and :297 (prose, manualSays verbatim). Authority (P2 v35 instruction spreadsheet, highest doc authority): …

**Proposed correction (verify first):** Manual: rewrite §3.4.1 table rows and the §3.4.1 prose so C is described as the true sign of the result, not signed overflow. Suggested table cell for both ADDS and SUBS C-column: "Sign of result (bit 31)". Suggested prose: "ADDS/SUBS set C to the true sign of the result (result bit 31), not a signed-overflow flag. For signed multi-long arithmetic, use ADD/ADDX for the lower longs and ADDSX (SUBSX) for the final …

### F-084 — `clock_system.yaml`: The named bit positions (CC 1:0, SS 3:2, DDDD 7:4, enables 8/9, VCO mult 23:14, divider …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-146)

**File(s):** `clock_system.yaml`

**What the KB says (suspect):** config_fields: d23_14 = 'VCO multiplier (MMMM_MMMMMM)' (10-bit), d27_24 = 'XI divider for PLL (PPPP)'. But pll_system places input_divider at D[23:18] (6 bits, divider-1) and vco_multiplier at D[17:8] (10 bits, multiplier-1) — a finer decomposition the manual flattens.

**Truth per manual-audit authority:** Decoding the canonical Silicon Doc layout %0000_xxxE_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS bit-by-bit (b31..b0): E=bit24 (PLL enable), D(input divider, 6b)=bits23:18, M(VCO mult, 10b)=bits17:8, P(post divider, 4b)=bits7:4, CC=bits3:2, SS=bits1:0. The manual table (ch04 §4.1.3) is wrong on nearly every PLL row: it lists CC=1:0 and SS=3:2 (SWAPPED — Silicon Doc CCSS nibble gives CC=3:2, SS=1:0, confirmed by %SS source-select / %CC crystal-config tables at part3-interrupts.txt:562,576), 'PLL power enable'=bit9 and 'crystal oscillator enable'=bit8 (FABRICATED — PLL enable E is bit24; there is no bit-8 crystal-enable, XI is …

**Authority cited:** Silicon Doc clock-mode layout %0000_xxxE_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS and field tables: engineering/ingestion/sources/silicon-doc/part3-interrupts.txt:488,521,533-557,562-584 (and duplicated at p2-documentation.txt:6031,6058,6073-6094). Manual table: …

**Proposed correction (verify first):** Rewrite the manual §4.1.3 bit-field table to the Silicon Doc layout %0000_xxxE_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS: SS bits 1:0 (clock source select RCFAST/RCSLOW/XI/PLL); CC bits 3:2 (crystal config / XI-XO loading); PPPP bits 7:4 (post divider, value→VCO/2..30, 15=VCO/1); MMMMMMMMMM bits 17:8 (VCO multiplier, 1..1024 = stored value+1); DDDDDD bits 23:18 (XI input divider, 1..64 = stored value+1); E bit 24 (PLL enable); …

### F-085 — `clock_system.yaml`: The manual's 'DC to 350 MHz' matches one authority field exactly, but the KB is …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-152)

**File(s):** `clock_system.yaml`

**What the KB says (suspect):** clock_system.yaml external.frequency_range 'DC to 350 MHz' (agrees), but the same file's _xinfreq.range '250 kHz to 500 MHz' and pll_system input_frequency '250 kHz to 500 MHz' give a different upper bound for external-clock input.

**Truth per manual-audit authority:** The "350 MHz" figure is, per the Silicon Doc (part3-interrupts.txt line 545), the PLL system-clock OVERCLOCK ceiling in VCO/1 mode — NOT a direct external-clock-input spec for the XI pin. No primary source states "DC to 350 MHz" as the external XI input range. The manual itself proves the conflation: line 36 correctly attributes 350 MHz to "VCO/1 overclocking," yet line 22 reuses the same number as the external-input range. The spec sheet caps the system clock at "320 MHz extended / 180 MHz typical." Meanwhile clock_system.yaml IS internally inconsistent as the finding states (external.frequency_range "DC to 350 …

**Authority cited:** Manual: engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-i/chapter-04-timing.md line 22 (external "DC to 350 MHz") and line 36 ("the PLL can be pushed to 350 MHz using VCO/1 mode"). YAML: deliverables/ai/P2/architecture/clock_system.yaml — …

**Proposed correction (verify first):** YAML (clock_system.yaml): reconcile the upper bound. The external-clock/_xinfreq direct-input ceiling is the system-clock max — spec-sheet authoritative value is 320 MHz extended (180 MHz typical), and the PLL theoretical overclock ceiling is 350 MHz (VCO/1). Replace external.frequency_range "DC to 350 MHz" with a sourced figure and align _xinfreq.range so the two fields no longer contradict; the lone "500 MHz" …

### F-086 — `execf.yaml`: The MANUAL matches the authoritative EXECF encoding ([9:0]=address, [31:10]=skip, 22 …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-162)

**File(s):** `execf.yaml`, `xbyte_engine.yaml`

**What the KB says (suspect):** execf.yaml (XBYTE consumes the LUT entry via EXECF): 'Jump to D[9:0] in cog/LUT and set SKIPF pattern to D[31:10]'. Architecture xbyte_engine.yaml:160-168 gives the OPPOSITE (wrong) layout [31:23]=address / [22:0]=skip.

**Truth per manual-audit authority:** Silicon Doc states three times that EXECF/XBYTE takes the jump address from the 10 LSBs (D[9:0]) and the 22-bit SKIPF pattern from the 22 MSBs (D[31:10]). The manual (chapter-05-hardware.md:527-528) says exactly "[9:0] | Handler address in COG/LUT RAM" and "[31:10] | SKIPF pattern (22 bits)" — matching authority. execf.yaml:9-10 also matches. xbyte_engine.yaml:160-168 gives the inverted (wrong) layout: "[31:23] = Base routine address (9 bits)" / "[22:0] = SKIPF pattern (23 bits)", with execf_operation reinforcing the error ("jump: To bits [31:23]" / "skipf: Using bits [22:0]"). The manualSays quote is accurately …

**Authority cited:** Silicon Doc (highest authority here): /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/silicon-doc/part2-beginning.txt:87-88 ("the 10 LSBs are an address to jump to in cog/LUT RAM and the 22 MSBs are a SKIPF pattern"); p2-documentation.txt:1913-1914 ("10-bit branch address from D[9:0] …

**Proposed correction (verify first):** No manual change — manual is correct. Fix deliverables/ai/P2/architecture/xbyte_engine.yaml:160-168. entry_format should read: "[9:0] = routine address (10 bits) to jump to in cog/LUT RAM; [31:10] = SKIPF pattern (22 bits)". ALSO fix the execf_operation block in the same node so it is consistent — jump: "To bits [9:0] of LUT entry"; skipf: "Using bits [31:10] as skip pattern". (The auditor's proposedCorrection only …

### F-087 — `clock_system.yaml`: $1000_0000 sets bit 28, not the reset bit. The reset bit is D[31] = $8000_0000. The …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-163)

**File(s):** `clock_system.yaml`, `hubset.yaml`

**What the KB says (suspect):** hubset.yaml: chip reset is bit 31 -- example 'HUBSET ##$80000000 ' Bit 31 = reset'; field d31 'Write 1 to reset the entire chip'. clock_system.yaml:135 also d31 'Reset request'.

**Truth per manual-audit authority:** The HUBSET reset/reboot function is selected by the upper nibble D[31:28] = %0001, i.e. $1000_0000 (bit 28). Silicon Doc, verbatim: "HUBSET ##$1000_0000 'generate an internal reset pulse to reboot" (part3-pages-37-38.txt:102) and the function table "%0001_xxxx_... Hard reset, reboots chip" vs "%1DDD_... Seed Xoroshiro128** PRNG" (walkthrough-audit.md:2384,2387). Bit 31 set ($8000_0000) selects the PRNG-seed function ("HUBSET with the MSB of D set... writes {1'b1,D[30:0]} into the PRNG", part3-pages-37-38.txt:75), NOT chip reset. The manual at chapter-05-hardware.md:716 says exactly $1000_0000, matching the …

**Authority cited:** Silicon Doc (authority): /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/silicon-doc/part3-pages-37-38.txt:99-102 ("HUBSET can be used to reset and reboot the chip: HUBSET ##$1000_0000 'generate an internal reset pulse to reboot") and lines 70-87 (seeding the PRNG uses HUBSET with the …

**Proposed correction (verify first):** Do NOT change the manual — manual line 716 (hubset ##$1000_0000) is correct per the Silicon Doc. Instead, correct the YAMLs to match authority: (1) deliverables/ai/P2/language/pasm2/hubset.yaml — replace the bit_fields d31 "Reset" entry and the chip_reset example "HUBSET ##$80000000 ' Bit 31 = reset" with the correct reset selector: HUBSET ##$1000_0000 (function-select %0001 in D[31:28] = internal reset pulse / …

### F-088 — `locknew.yaml`: Manual is CORRECT per the authoritative instruction YAML. The architecture locks.yaml has …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-167)

**File(s):** `locknew.yaml`, `locks.yaml`

**What the KB says (suspect):** Authoritative locknew.yaml: 'C = 1 if no LOCK is available', 'C: Set if no LOCK available' -- i.e. C=1 = pool empty, C=0 = allocated (MATCHES the manual). But locks.yaml:84-93 (architecture summary) WRONGLY states LOCKNEW 'C := 1 (success)' / 'C := 0 (no locks available)'.

**Truth per manual-audit authority:** Highest authority (Silicon Doc, part3-end.txt:495-496) states for LOCKNEW WC: "Zero (0) indicates success, while one (1) indicates that all locks are already allocated." This means C=0 = lock allocated, C=1 = pool empty. The manual (line 432) and locknew.yaml both match this exactly. locks.yaml:90-91 has it INVERTED ("C := 1 (success)" / "C := 0 (no locks available)"). Manual quote verified verbatim at chapter-05-hardware.md:432. Note: this is a runtime flag-effect, not assembler-settleable; the compiler only emits the encoding, so the Silicon Doc is the decisive authority and it is unambiguous.

**Authority cited:** Silicon Doc part3-end.txt:494-501 (and p2-documentation.txt:7460-7462): "Zero (0) indicates success, while one (1) indicates that all locks are already allocated." | locknew.yaml (deliverables/ai/P2/language/pasm2/locknew.yaml): encoding "c: 1 if no LOCK available", flags_affected C "Set if no LOCK …

**Proposed correction (verify first):** No change to the manual (it is correct). In deliverables/ai/P2/architecture/locks.yaml, fix the LOCKNEW operation block (lines ~89-91) to "C := 0 (lock allocated, success)" in the IF found branch and "C := 1 (no locks available)" in the ELSE branch. ADDITIONALLY — and beyond the auditor's proposal — correct BOTH usage examples that depend on the inverted semantics: line ~98 ("IF_NC JMP #no_locks") and line ~180 …

### F-089 — `cordic.yaml`: The P2 CORDIC QLOG produces a base-2 logarithm in 5:27 fixed-point (whole part = bit …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-168)

**File(s):** `cordic.yaml`, `qlog.yaml`

**What the KB says (suspect):** qlog.yaml: 'Convert 32-bit unsigned integer to 5:27-bit logarithm format... 5-bit whole exponent in bits [31:27] and a 27-bit fractional exponent'. The 5-bit whole-exponent format is a base-2 logarithm; qlog.yaml does NOT say natural log. (cordic.yaml:79 inconsistently labels it 'Natural logarithm (base e)'.)

**Truth per manual-audit authority:** Silicon Doc part3-end.txt:453 states verbatim: "QLOG D/# - Compute log base 2 of D", and lines 450-451 describe the result as "a 5:27-bit logarithm, where the top 5 bits hold the whole part of the power-of-2 exponent and the bottom 27 bits hold the fractional part." Base-2 is the chip's documented behavior. The manual's ch05 line 22 reads "Logarithm | QLOG | Natural log approximation in X" — directly contradicting the authority. cordic.yaml:78 reads operation: "Natural logarithm (base e)" — same error. qlog.yaml never says "natural"; its 5:27 whole-exponent description (whole part = power-of-2 exponent) is …

**Authority cited:** Silicon Doc (Parallax authoritative architecture source): /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/silicon-doc/part3-end.txt:450-453 ("the top 5 bits hold the whole part of the power-of-2 exponent" / "QLOG D/# - Compute log base 2 of D"); corroborated at …

**Proposed correction (verify first):** Manual ch05 line 22: change to "Logarithm | QLOG | Base-2 logarithm (5:27 fixed-point) in X". cordic.yaml:78: change operation from "Natural logarithm (base e)" to "Base-2 logarithm (5:27 fixed-point)" (and QEXP at line 84 area should read "2 to the power of D", per Silicon Doc part3-end.txt:466).

### F-090 — `serial_loader.yaml`: Per KB authority, Prop_Hex loads Intel-hex records (colon-prefixed with …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-170)

**File(s):** `serial_loader.yaml`

**What the KB says (suspect):** serial_loader.yaml lines 69-82: prop_hex format 'Intel hex records' with the :LLAAAATTDD...CC record structure.

**Truth per manual-audit authority:** Silicon Doc (the authoritative ROM-booter description, ranked above the YAML) defines Prop_Hex as whitespace-separated raw hex bytes — "Hex bytes must be separated by whitespaces. Only the bottom 8 bits of hex values are used as data" — with form `Prop_Hex <INAmask> <INAdata> <INBmask> <INBdata> <hexdatabytes> ~` and example `Prop_Hex 0 0 0 0 FB F7 23 F6 FD FB 23 F6 ... ~`. There is NO Intel-hex record structure: no colon-prefixed `:LLAAAATTDD...CC`, no per-record address/type/checksum. Therefore the manual's terse "Load program data in hexadecimal format" is CORRECT (it is plain hexadecimal). The auditor's …

**Authority cited:** Manual: engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-i/chapter-05-hardware.md:676 (`| `Prop_Hex` | Load program data in hexadecimal format |`). Authority (Silicon Doc, ROM booter spec): engineering/ingestion/sources/silicon-doc/p2-documentation.txt offset …

**Proposed correction (verify first):** Do NOT change the manual; leave line 676 as-is (optionally enrich to "Load program data as whitespace-separated hex bytes" but not required). FIX THE YAML deliverables/ai/P2/architecture/serial_loader.yaml:69-82 — this routes to the P2KB corrections register. Replace the bogus prop_hex block with: format: "whitespace-separated hex bytes (raw, not Intel HEX)"; syntax: "Prop_Hex <INAmask> <INAdata> <INBmask> <INBdata> …

### F-091 — `addressing_modes.yaml`: The YAML authority labels the -32..+31 non-updating index as '5-bit signed', but the …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-173)

**File(s):** `addressing_modes.yaml`

**What the KB says (suspect):** addressing_modes.yaml:47 states 'index_range: -32 to +31 (5-bit signed)'. The silicon doc encodes this as a 6-bit field: 'IIIIII = INDEX6' (six I bits, line 6948) and 'INDEX6 = -32..+31 for non-updating offsets' (line 6942). -32..+31 requires 6 bits.

**Truth per manual-audit authority:** The silicon doc explicitly uses a six-bit field "IIIIII = INDEX6" spanning the full -32..+31 range (line 6948), and labels it INDEX6 (line 6942). By two's-complement arithmetic, -32..+31 = -2^5..+2^5-1 = 6-bit signed; a 5-bit signed field only covers -16..+15 and cannot represent -32 or +31. The manual (line 303) says "6-bit signed" — correct. The YAML (line 47) says "5-bit signed" — wrong. The manualSays quote is reproduced verbatim and is accurate.

**Authority cited:** Silicon Doc engineering/ingestion/sources/silicon-doc/p2-documentation.txt:6942 ("INDEX6 = -32..+31 for non-updating offsets") and :6948 ("IIIIII = INDEX6, uses %100000..%111111 for -32..-1 and %000000..%011111 for 0..31" — six I bits). Manual part-i/chapter-06-address-modes.md:303 ("**Index Range …

**Proposed correction (verify first):** In deliverables/ai/P2/language/pasm2/concepts/addressing_modes.yaml line 47, change "index_range: -32 to +31 (5-bit signed)" to "index_range: -32 to +31 (6-bit signed)". This routes to the P2KB corrections register. The manual needs no change.

### F-092 — `addressing_modes.yaml`: YAML-side example-quality issue surfaced during cross-reference: the auto_decrement …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-174)

**File(s):** `addressing_modes.yaml`, `pushb.yaml`, `special_registers.yaml`

**What the KB says (suspect):** addressing_modes.yaml auto_decrement block (lines 66-73) gives a valid RDLONG --PTRA example at line 71 but then line 72 illustrates auto-decrement with 'PUSHB value ' Implicit --PTRB operation'. The hardware-stack push/pop ops in special_registers.yaml (lines 100-103) and the silicon doc associate the hardware stack with PTRA via PUSHA/POPA, not a generic '--PTRB' decrement.

**Truth per manual-audit authority:** addressing_modes.yaml:72 places "PUSHB value ' Implicit --PTRB operation" inside the auto_decrement: block (syntax "--PTRx", behavior "Decrement first, then use new value"). But every authority shows PUSHB is a post-INCREMENT, not a decrement. Silicon Doc: "PUSHB register/# = WRLONG register/#,PTRB++" (vs POPB = RDLONG register,--PTRB). pushb.yaml: "Writes long to hub at PTRB++", "PTRB is automatically incremented after the write", oneliner "Push long to hub stack using PTRB (post-increment)". So PUSHB illustrates auto_INCREMENT (PTRB++); the instruction that performs --PTRB is POPB. The YAML asserts the exact …

**Authority cited:** Silicon Doc alias definitions: engineering/ingestion/sources/silicon-doc/silicon-doc-v35-walkthrough-audit.md:4003-4006 ("POPB register = RDLONG register,--PTRB" / "PUSHB register/# = WRLONG register/#,PTRB++"); per-instruction YAML deliverables/ai/P2/language/pasm2/pushb.yaml:13,14,34,36; …

**Proposed correction (verify first):** In addressing_modes.yaml, remove line 72 ("PUSHB value ' Implicit --PTRB operation") from the auto_decrement: block. If a stack-op illustration is wanted there, use POPB (which IS --PTRB): "POPB value ' Implicit --PTRB (RDLONG value,--PTRB)". Conversely, PUSHB belongs under auto_increment (lines 57-65) as "PUSHB value ' Implicit PTRB++ (WRLONG value,PTRB++)". This is a hard factual correction, not optional cleanup — …

### F-093 — `lockrel.yaml`: The appendix states the inverted polarity. The authoritative meaning is C = lock-was-held …  ·  `WONTFIX` (2026-06-10)  (PASM2 audit AF-180)

**File(s):** `lockrel.yaml`

**What the KB says (suspect):** With WC, LOCKREL returns the LOCK status into C (whether the lock was held/owned), not 'already free.' Silicon table / manual description: 'Release LOCK D[3:0]. If D is a register and WC, get current/last cog id of LOCK owner into D and LOCK status into C.' The LOCKREL YAML notes state 'C = 1 if lock was held' and description says 'LOCK status into C.' (The YAML flags_affected.C: No effect field is itself …

**Truth per manual-audit authority:** The Silicon Doc (highest available authority for this hardware-behavior claim; compiler cannot probe runtime C polarity) states twice and identically: "the C flag will indicate whether the lock is currently taken." Therefore with WC, C=1 means the lock IS taken/held. The manual at appendix-c:617 says C means "1 if lock was already free" — the exact inverted polarity. Manual is wrong. Separately, lockrel.yaml has flags_affected.C: "No effect", which directly contradicts that same file's own description ("...and LOCK status into C") and its example comments ("C = 1 if lock was held") — both of which correctly …

**Authority cited:** Silicon Doc: engineering/ingestion/sources/silicon-doc/part3-end.txt:529-530 and part4-locks.txt:5-6 ("When LOCKREL is executed with WC, the C flag will indicate whether the lock is currently taken"). Manual: opus-master/part-iii/appendix-c-categorical-index.md:617 ("| LOCKREL | 1 if lock was …

**Proposed correction (verify first):** Manual (appendix-c-categorical-index.md:617): change the LOCKREL C-flag meaning from "1 if lock was already free" to "1 if lock is currently taken (held)" — matching the Silicon Doc. YAML (lockrel.yaml): change flags_affected.C from "No effect" to reflect the WC behavior, e.g. "When WC: 1 if lock is currently taken/held (LOCK status); no effect otherwise" — making it consistent with the file's own description and …

### F-094 — `coginit.yaml`: The manual assigns HUBEXEC the bit pattern/hex that actually belongs to COGEXEC_NEW. …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-181)

**File(s):** `coginit.yaml`, `hubexec.yaml`, `spin2-builtin-symbols-complete.yaml`, `spin2_cog_management.yaml`

**What the KB says (suspect):** HUBEXEC = %100000 ($20). spin2_cog_management.yaml lines 18-19: HUBEXEC value: "%100000". spin2-builtin-symbols-complete.yaml lines 315-319: HUBEXEC value "$0000_0020", bit_pattern "%10_0000". coginit.yaml line 23: "Bit 5 set: Execute from hub RAM (HUBEXEC mode)". The Dest format is %E_N_xVVV (coginit.yaml line 5); HUBEXEC sets the E no-load bit = bit5 = $20. The manual's %0_1_0000/$10 is actually COGEXEC_NEW (E=0 …

**Truth per manual-audit authority:** Compiler is ground truth: HUBEXEC compiles to $00000020 (= %10_0000), and COGEXEC_NEW compiles to $00000010 (= %0_1_0000). The manual's HUBEXEC Value table (appendix-e-constants.md:273-274) states Binary %0_1_0000, Hex $10 — that is precisely COGEXEC_NEW's value, not HUBEXEC's. The manual swapped the N (free-cog, bit4=$10) bit for the E (no-load/hub-exec, bit5=$20) bit. The single-constant source pasm2/hubexec.yaml:9 carries the identical wrong value '%0_1_0000'. Two independent Spin2 YAMLs (spin2_cog_management.yaml:20 and builtin-symbols:318-319) correctly give $20/%10_0000, confirming pasm2/hubexec.yaml and …

**Authority cited:** pnut-ts v1.55.0 probe (/tmp/hubexec_probe.lst): V_HUBEXEC=$00000020, V_COGEXEC=$00000000, V_COGEXEC_NEW=$00000010, V_HUBEXEC_NEW=$00000030; hub-byte dump "20 00 00 00 ... 10 00 00 00". Manual: part-iii/appendix-e-constants.md:262-274 (HUBEXEC table Binary %0_1_0000 / Hex $10) and :226-227 (COGEXEC …

**Proposed correction (verify first):** Manual part-iii/appendix-e-constants.md HUBEXEC Value table (lines 273-274): change Binary to %1_0_0000 and Hexadecimal to $20. (Use the full grouped form %1_0_0000 to match the table's existing %E_N_xVVV style, e.g. COGEXEC's %0_0_0000 — not the un-grouped %10_0000 in the auditor's text.) Also fix deliverables/ai/P2/language/pasm2/hubexec.yaml line 9 from value: '%0_1_0000' to value: '%10_0000' (or '%1_0_0000' to …

### F-095 — `debug-mask.yaml`: The {Spin2_v46} version-directive requirement is the most-stressed fact about DEBUG_MASK …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-182)

**File(s):** `debug-mask.yaml`, `special-configuration-symbols.yaml`

**What the KB says (suspect):** DEBUG_MASK / debug[N]() require a {Spin2_v46} (or later) version directive at the start of the source file. debug-mask.yaml:5-6 declares minimum_version: "v46", version_directive: "{Spin2_v46}"; line 17 "REQUIRES: {Spin2_v46} or later version directive"; note line 124 repeats it. special-configuration-symbols.yaml:314-315,327 repeat requires_version Spin2_v46.

**Truth per manual-audit authority:** The compiler refutes the requirement claim. debug[N]() compiles cleanly on pnut-ts v1.55.0 with NO {Spin2_v46} directive (exit 0, no version warning), while truly version-gated keywords LSTRING (v42+) and TASKID (v47) FAIL under the v41 default — so the version-keyword gate is real and enforced, and debug[N] is simply not subject to it (it is bracket/index syntax on the pre-existing DEBUG keyword, not a new reserved word). The v51 spec's DEBUG_MASK section (debug-section.txt:1006-1016) states no directive requirement; the only v46 link is a release-history note "DEBUG gating and disabling added" …

**Authority cited:** pnut-ts v1.55.0 probes (ground truth): (1) /tmp/af182_dat.spin2 — DEBUG_MASK + debug[N]() in DAT/org with NO version directive → "Wrote af182_dat.bin", exit 0, no version warning; (2) /tmp/af182_confirm.spin2 — debug[0]/debug[5] no directive → exit 0; (3) control /tmp/af182_lstr.spin2 (PUB lstring, …

**Proposed correction (verify first):** Do NOT add the {Spin2_v46} requirement to the manual — that would inject a false constraint contradicted by pnut-ts v1.55.0. The finding is refuted on the manual side. Separately, route a YAML correction: in debug-mask.yaml soften the overstated requirement (lines 5-6,17,124 and the notes) and in special-configuration-symbols.yaml (314-315,327) from "REQUIRES {Spin2_v46} or later version directive / causes compile …

### F-096 — `cog_hub_execution.yaml`: '$000-$1F7' and '496 longs' cannot both be literally true (the range is 504 longs; 496 …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-183)

**File(s):** `cog_hub_execution.yaml`, `cogexec.yaml`, `coginit.yaml`

**What the KB says (suspect):** $000-$1F7 inclusive spans 504 longs (0x1F8), not 496. cogexec.yaml:27 gives the range '$000-$1F7' with no count. coginit.yaml:113 gives '$000-$1F7: Your PASM code/data (504 longs)'. The 496 figure comes from cog_hub_execution.yaml:59-60 ('$000_$1FF: 496 longs available' + '$1F0_$1FF: 16 special registers'), i.e. 512 minus 16 special — which pairs 496 with a span ending at $1EF, not $1F7.

**Truth per manual-audit authority:** Silicon Doc COGINIT description states COGINIT loads cog registers "$000..$1F7" from hub. $000-$1F7 inclusive = 0x1F8 = 504 longs (verified 0x1F7+1=504). The "496" figure in the Silicon Doc is a DIFFERENT quantity: the count of GENERAL-PURPOSE registers, which span $000-$1EF only (0x1EF+1=496). The manual (appendix-e-constants.md:230,248,252) pairs the correct COGINIT range "$000-$1F7" with the wrong count "496 longs" as if synonymous — mathematically impossible side-by-side, since 496 longs ends at $1EF. coginit.yaml:113 has it RIGHT ("$000-$1F7 ... (504 longs)"); cogexec.yaml:27 gives the range with no count …

**Authority cited:** Silicon Doc (highest available authority for this architectural fact): engineering/ingestion/sources/silicon-doc/silicon-doc-complete-sample.txt — COGINIT section: "D/# = %0_x_xxxx The target cog loads its own registers $000..$1F7 from the hub..."; same file GENERAL PURPOSE REGISTERS: "RAM …

**Proposed correction (verify first):** MANUAL (appendix-e-constants.md): change every instance of "496 longs" describing the COGINIT/$000-$1F7 load to "504 longs". Specifically: line 230 "loads 496 longs ... into cog RAM registers $000-$1F7" -> "loads 504 longs ... into cog RAM registers $000-$1F7"; line 248 "Loads cog RAM registers $000-$1F7 (496 longs)" -> "(504 longs)"; line 252 "Code size limited to 496 longs" -> "Code size limited to 504 longs (2KB …

### F-097 — `addon-goertzel-touch.yaml`: The manual states the ADC gains as 3.16x and 31.6x (the √10-spaced physical gain values: …  ·  `DONE` (2026-06-10)  (PASM2 audit AF-184)

**File(s):** `addon-goertzel-touch.yaml`, `smart-pin-11000-adc-internal-clock.yaml`

**What the KB says (suspect):** The ADC gain constants are documented as "P_ADC_3X - 3x gain" and "P_ADC_30X - 30x gain" (whole-number labels, not 3.16x / 31.6x).

**Truth per manual-audit authority:** Spin2 v51 narrative line 5050: "%0000_0000_000_1001000000000_00_00000_0 P_ADC_3X ADC 3.16x → IN, output OUT" and line 5054: "...P_ADC_30X ADC 31.6x → IN, output OUT". The manual reproduces these exact figures (3.16x/31.6x) and the exact encodings. The cited YAML sources instead label them "3x gain"/"30x gain", which numerically contradicts the defining spec. The manual matches the highest authority; the YAML is the rounded/wrong one. Note: the spec uses the verb-less phrase "ADC 3.16x" (no literal word "gain"), but the figure 3.16x is unambiguous and the manual's "3.16x gain" is a faithful gloss.

**Authority cited:** Spin2 v51 spec (authority that defines these constants): /workspaces/P2-Knowledge-Base/engineering/ingestion/sources/spin2-v51/spin2-v51-narrative.txt:5050 ("P_ADC_3X ... ADC 3.16x → IN, output OUT") and :5054 ("P_ADC_30X ... ADC 31.6x → IN, output OUT"). Manual: …

**Proposed correction (verify first):** Leave the manual unchanged (it is correct). Fix the YAML data set to the precise √10-spaced gain ladder per the Spin2 v51 spec: in smart-pin-11000-adc-internal-clock.yaml change line 147 to "P_ADC_3X - 3.16x gain" and line 149 to "P_ADC_30X - 31.6x gain"; in addon-goertzel-touch.yaml correct the "3x" labels (lines 91 and 155) to "3.16x". Route to the P2KB corrections register.

## Spin2 v55 delta-ingestion conflict audit — 2026-06-10 (F-098..F-100)

Surfaced by ingesting **Spin2 Language Documentation v55** (`engineering/ingestion/sources/spin2-v55/`) as a delta over the prior v51a baseline (`ingest-source` skill, first run). The v52→v55 language extensions were **already present** in the KB (ingested earlier, likely from PNut release notes), so there was **no gap-fill** — but the conflict audit (each feature gate boundary-probed against `pnut-ts v1.55.0`, the PNut-v55-ratified compiler) found three defects. ENDIANL/ENDIANW (`{Spin2_v52}`), OFFSETOF (`{Spin2_v53}`), and struct-bitfields (`{Spin2_v45}` enforced, `v54` intent) were **verified correct** — no action.

### F-098 — `NEXT`/`QUIT` level: fabricated `NEXTN`/`QUITN` keywords + wrong range + inverted semantics + over-claimed gate  ·  `DONE` (2026-06-10)

> **Applied 2026-06-10.** Re-probed pnut-ts (next 1 in 2-deep OK; next 2 → "not sufficiently nested"; next 16 → "must be from 1 to 15"; nextn 2 → unrecognized; quit 1 at v41 → compiles=ungated; 3-deep bounds confirmed). Fixed all 5 files: `constructs/next.yaml`, `constructs/quit.yaml`, `constructs/repeat.yaml` (QUITN block → `QUIT/NEXT level`), `keywords/NEXT.yaml`, `keywords/QUIT.yaml` — replaced NEXTN/QUITN with `NEXT level`/`QUIT level`, range 1-16→1-15, rewrote to outward-counting semantics (bare = current loop; `N` = N-th outer), dropped the enforced-`{Spin2_v52}` gate claim (made `enforced_version_gate: none` explicit; v52 = edition of introduction).

**Files (5):** `language/spin2/constructs/next.yaml`, `constructs/quit.yaml`, `constructs/repeat.yaml`, `language/spin2/keywords/NEXT.yaml`, `keywords/QUIT.yaml`

**What's wrong:**
1. **Fabricated keyword forms `NEXTN`/`QUITN`** — these do not exist. The real form is `NEXT level` / `QUIT level` (keyword, space, integer). `constructs/next.yaml`/`quit.yaml`/`repeat.yaml` document `NEXTN`/`QUITN` with examples (`NEXTN 2`, `QUITN 2`).
2. **Wrong range `1-16` / "maximum level is 16"** — the valid range is **1-15**.
3. **Inverted semantics** — the YAMLs say "level 1 = innermost loop (default)". Actual: bare `NEXT`/`QUIT` targets the **current** loop; `NEXT 1`/`QUIT 1` targets the **1st-outer** loop, counting **outward** (so `QUIT 1` requires ≥2 nesting, `NEXT 2` requires ≥3).
4. **Over-claimed gate** — `NEXT.yaml`/`QUIT.yaml` imply a `{Spin2_v52}` requirement; the compiler does **not** enforce one (the integer form compiles at `{Spin2_v41}`).

**Evidence (pnut-ts v1.55.0; verified independently by the v55 delta-audit agent AND a second hand-probe):**
- `nextn 2` and `quitn 2` (properly nested) → `error: Expected an instruction or variable` (keyword unrecognized — fabricated).
- `next 16` → `error: NEXT/QUIT level must be from 1 to 15` (range is 1-15).
- `quit 1` inside 2 nested `repeat`s → compiles clean (outward counting; `QUIT 1` = 1st-outer).
- `next 2` with explicit `{Spin2_v41}` → only `error: NEXT/QUIT is not sufficiently nested…` (a nesting error, no version-gate error → ungated).
- v55 spec `spin2-v55-text.txt` (v52 entry): "NEXT and QUIT can now be followed by an integer 1..15 to indicate an alternate" loop level.

**Proposed correction (verify first):** (a) `constructs/next.yaml`,`quit.yaml`,`repeat.yaml` — replace every `NEXTN`/`QUITN` with `NEXT level`/`QUIT level` (and `QUITN 2`→`QUIT 1` etc.). (b) `keywords/NEXT.yaml`,`QUIT.yaml` — range `1-16`→`1-15`, "maximum level is 16"→"15"; rewrite semantics to outward-counting (bare = current loop; `N` = N-th outer); drop the `{Spin2_v52}` gate claim (mark ungated; `v52` is edition-of-introduction only). Honor Sacred Rule #7 on any `related:` churn.

### F-099 — `debug-end-session.yaml` invents a mechanism AND omits the real documented behavior + purpose  ·  `DONE` (2026-06-10)

> **Applied 2026-06-10.** Kept value 27 + the (genuinely enforced) `{Spin2_v52}` gate. Replaced the invented `debug_behavior`/`DebugActive=false` mechanism with the v55-sourced behavior (closes any open DEBUG.LOG file + DEBUG window(s); closes PNut if launched with `-rd`; the P2 continues executing) in description, `debug_behavior`, and notes; added the AI-assisted-dev purpose; dropped "ASCII ESC character" and "Equivalent to DEBUG(27)".

**File:** `language/spin2/constants/debug-end-session.yaml`

**The feature is REAL and its core facts are CORRECT** — constant, **value 27**, gate **`{Spin2_v52}`** (compiler-verified), and "closes the DEBUG window(s)" are all right. This is a rewrite-and-**enrich**, not a deletion. **pnut-ts implements it (no compiler bug):** `debug(DEBUG_END_SESSION)` compiles under `{Spin2_v52}` and the symbol is a usable constant; the `{Spin2_v52}` gate is enforced (fails at v41/v51); value confirmed **27** via a compile-time divide-by-zero oracle (`1/(DEBUG_END_SESSION-27)` → "Divide by zero", while `-26` compiles clean). The runtime side-effects (DEBUG.LOG/PNut close, P2 continues) are the DEBUG **host** (`pnut-term`)'s job, not the compiler's — nothing missing on the compiler side.

**What's wrong — two parts, the omission being the larger:**
1. **Invented mechanism.** The `debug_behavior` steps (lines 59-64) — "Character code 27 sent to debug display" → "Debug display **sets DebugActive = false**" → "Debug window closes" — describe an internal flag/sequence that **appears nowhere in v55**. Likewise the description (lines 12-14) "sets DebugActive to false".
2. **Omits the actual documented behavior and the whole purpose.** v55 (`spin2-v55-text.txt:101-107`, verbatim) states `DEBUG(DEBUG_END_SESSION)` was **"added for facilitating AI-assisted code development"**, and when it executes: **"Any open DEBUG.LOG file and DEBUG window(s) get closed. If `PNut <filename> -rd` was used to launch PNut, PNut closes, as well. The P2 continues executing."** The YAML mentions **none** of: the DEBUG.LOG-file close (v55's *first* effect), the PNut `-rd` close, the **"P2 continues executing"** fact, or the AI-dev-loop purpose (assistant deletes DEBUG.LOG → recompiles `-rd` → waits for DEBUG.LOG to close → reads results).
3. **Unsourced notes:** "Value is 27 (**ASCII ESC character**)" and "**Equivalent to DEBUG(27)**" — v55 states neither (27 = 0x1B *is* ESC arithmetically, but v55 treats this as a recognized DEBUG sentinel, not an escape char).

**Evidence:** v55 spec `spin2-v55-text.txt:101-107` (behavior + purpose, verbatim) and `:152` (symbol table: `DEBUG_END_SESSION … (27) for use in DEBUG … {Spin2_v52}`). Runtime behavior is not compiler-probeable; v55 is the authority.

**Proposed correction (verify first):** Keep value 27 + `{Spin2_v52}`. Replace the invented `debug_behavior`/`DebugActive` content with the v55-sourced behavior: closes any open **DEBUG.LOG file** and **DEBUG window(s)**; closes **PNut** if launched with `-rd`; **the P2 continues executing**. Add the purpose ("facilitating AI-assisted code development" — the DEBUG.LOG close is the signal an AI tool waits on). Drop "ASCII ESC character" and the unsourced "Equivalent to DEBUG(27)" unless separately verified.

### F-100 — `movbyts.yaml` gating field is ambiguous (feature is ungated, not v52-enforced)  ·  `DONE` (2026-06-10)

> **Applied 2026-06-10.** Re-probed: `MOVBYTS` compiles at no-directive (ungated). Replaced the ambiguous bare `minimum_version: "v52"` with explicit `introduced_in: "v52"` + `enforced_version_gate: none` (boundary-probe verified). The file's prose already correctly stated "no version directive required".

**File:** `language/spin2/methods/movbyts.yaml`

**What's wrong:** Carries `minimum_version: "v52"` (a bare field readable as an enforced compiler gate) while its own prose correctly says "no version directive required". The compiler does **not** enforce a gate — `MOVBYTS(...)` compiles at `{Spin2_v41}` and with no directive. Inconsistent, too, with its same-batch siblings `endianl.yaml`/`endianw.yaml` which use structured `requires_version`/`version_directive` (and ARE genuinely v52-gated). This is the same "required-directive claim refuted" class as F-095 (debug[N]).

**Evidence:** pnut-ts v1.55.0 boundary-probe — `MOVBYTS` compiles at `{Spin2_v41}`/no-directive (ungated); contrast `ENDIANL` which fails below `{Spin2_v52}`.

**Proposed correction (verify first):** Make the ungated status explicit/machine-readable (e.g. `requires_version: none` + a note: "Introduced in PNut/pnut_ts v52; the compiler does NOT enforce a version directive — verified by boundary probe. 'v52' is the edition of introduction, not an enforced gate."). Per [[reference_language_gating_is_yaml_golden]], the YAML is the golden home for gating — it must read unambiguously.

---

## PASM2-audit correction sweep — 2026-06-10 (Wave 1: F-026..F-050)

Each NEEDS-VERIFICATION finding was independently re-verified against the golden sources (pnut-ts boundary/assembly probes · `silicon-doc` · `p2-instructions-csv` · `spin2-v55` · `chip-gracey-clarifications`) by a bounded verification workflow, then hand-reviewed and applied via `yaml-knowledge-base-maintenance`. Outcome of the 25:

- **24 CONFIRMED + applied → DONE.** F-026 (getscp `write: D`), F-027/F-029/F-030/F-031 (clock_system.yaml HUBSET operand map fully rewritten to canonical `E_DDDDDD_MMMMMMMMMM_PPPP_CC_SS`; CC=D[3:2]/SS=D[1:0] un-swapped; all three example literals recomputed and PASM2-compile-verified), F-028 (hubset.yaml d3_2 CC: 4 entries, 15pF moved off %01 onto %10), F-032 (ijnz note de-inverted), F-033 (jxro "streamer NCO rollover" + oneliner), F-034 (jxro/jxmt variable timing), F-035 (lockrel C = lock-was-held under WC), F-037 (locknew/lockret/locktry/lockrel variable timing), F-038 (tjf/tjz/tjnz/tjns hub clocks), F-039 (tjnz/tjns variable timing), F-040 (testb `related`), F-041 (tjf/tjz column-bleed description fragment removed), F-042 (addpix = 4 byte fields / 8:8:8:8 incl. alpha, per Silicon Doc), F-043/F-044 (addsx/addx `related` self-ref→sibling), F-045 (augd/augs SETQ-block-delta errata), F-046 (augs scope_note tightened), F-048/F-049 (calla/callb hub-exec timing 14-32 added; CSV-confirmed), F-050 (calla PTRA-only description/oneliner). **F-047** (gen-script `flags_affected` key-presence-vs-value bug) fixed in `engineering/tools/gen-pasm2-encoding-reference.py` — corrects the bogus "C,Z" column on 344 rows; takes effect on the encoding-reference regen.
- **1 REFUTED → WONTFIX.** F-036 — LOC category `Math and Logic` matches the canonical Parallax CSV (row 431) exactly; proposed "Branch" recategorization is wrong. (Manual-side LOC categorization inconsistency is a separate manual-head issue, not a YAML defect.)

**Bundled fixes surfaced during Wave 1 (not separate findings, fixed in the same pass):**
- F-051 (callb PTRB-only description — a Wave 2 item) applied early while editing `callb.yaml`.
- See **F-101** below (tjnz/tjns inverted jump-condition prose, the TJ-family analog of F-032).

### F-101 — `tjnz.yaml`/`tjns.yaml` carry inverted jump-condition prose (TJ-family analog of F-032)  ·  `DONE` (2026-06-10)

**Files:** `tjnz.yaml`, `tjns.yaml`

**What was wrong:** `tjnz.yaml` `description` and `encoding_notes` said PC is written "when Dest is **zero** (or not zero in syntax 2)" — but TJNZ = Test and Jump if **Not** Zero. `tjns.yaml` `encoding_notes` said "when Dest is **signed** (or not signed in syntax 2)" — but TJNS = Test and Jump if **Not** Signed. Both are the same stale shared-template parenthetical class as F-032 (ijnz) / F-056/F-057 (djf/djnz).

**Evidence:** `p2-instructions-csv` rows 175/179 — "Test D and jump to S** if D is **not** zero." / "…if D is **not** signed (D[31] = 0)."

**Correction applied:** tjnz description + note → "if it's NOT zero" / "only when Dest is NOT zero"; tjns note → "only when Dest is NOT signed (Dest[31] = 0)". Surfaced while applying F-039 (same files).

---

## PASM2-audit correction sweep — 2026-06-10 (Wave 2: F-051..F-075)

Same verify→fix discipline as Wave 1. All 25 applied (24 CONFIRM + 1 PARTIAL):

- **Cross-ref / specificity:** F-051 (callb PTRB-only desc — applied early in Wave 1), F-052 (callpa→PA, callpb→PB), F-053/F-054 (cmpsx/cmpx `related` self-ref→CMPS), F-055 (cogstop `related`→COGID).
- **De-inverted jump-condition prose:** F-056 (djnf "NOT full"), F-057 (djnz "NOT zero").
- **Flag/field/timing:** F-058 (rdlong Z=Result==0 under WZ — was the lone outlier vs rdbyte/rdword), F-059/F-060/F-061 (rolbyte/rolword/setbyte "nibble ID"→byte/word/byte ID), F-062 (signx "zero-extend"→"sign-extend"), F-063 (waitxro fixed→variable), F-064 PARTIAL (waitx C/Z cleared only under WC/WZ/WCZ — YAML side; manual already correct), F-065 (wfbyte/wfword/wflong column-bleed description fragment removed), F-066 (wmlong fixed→variable timing), F-067 (wrbyte timing.cycles range).
- **Assembler-directive cluster (all compiler-probe-verified):** F-068/F-069 (org.yaml: COG/LUT range 0-$3FF, optional limit, auto-limit table $1F8/$200/$400 — all boundary-probed; fit.yaml: bare FIT is a compile error), F-070/F-071 (orgf.yaml: COG-mode-only, 0-$3FF, ORGH-mode error), F-072/F-073 (orgh.yaml ×2: limit param + $100000 ceiling m361/m372; bare-ORGH default context-dependent $400 vs current-hub — per Spin2 v55 spec §326/§327), F-074 (byte/word/long: "Hub memory"→current ORG/ORGH origin), F-075 (file.yaml filename invalid-char list + DAT-only, merged with F-076).

## PASM2-audit correction sweep — 2026-06-10 (Wave 3: F-023, F-076..F-097)

All applied except one refutation; every high-impact numeric/encoding claim re-verified against primary sources before publishing:

- **Fabrication removed:** F-023 (setxfrq SETQ+SETXFRQ "64-bit precision" — invented; NCO is 32-bit, SETXFRQ takes no SETQ; replaced with the real SETQ-before-XINIT pattern).
- **Verified-then-applied (probe/source in parens):** F-078/F-079 (GETCT counter is 64-bit; WC=upper 32 — CSV row 260), F-080 (PTRx post-modify index 1-16), F-081 (IF_NEVER assembles to EEEE=%1111, not %0000; %0000 is _RET_-only — EEEE-bit probe), F-082/F-083 (ADDS/SUBS C = correct sign of result, NOT signed overflow — CSV "C = correct sign"), F-085 (XI direct-drive max 200 MHz not 350 — datasheet AC table), F-086 (XBYTE/EXECF LUT entry: addr=D[9:0], skip=D[31:10] — Silicon Doc :1913), F-087 (chip reset = HUBSET ##$1000_0000 D[31:28]=%0001; D[31]=PRNG seed not reset — Silicon Doc :6038/:6465/:6468), F-088 (locks.yaml LOCKNEW C polarity: C=0 success / C=1 none — matches locknew.yaml), F-089 (QLOG base-2 / 5:27 fixed-point, QEXP=2^D — Silicon Doc :7287), F-090 (Prop_Hex is whitespace-separated raw hex, NOT Intel HEX), F-091 (index -32..+31 = 6-bit signed), F-092 (PUSHB=PTRB++, POPB=--PTRB examples), F-094 (HUBEXEC=$20 — divide-by-zero oracle), F-095 (DEBUG_MASK ungated — compiled clean with no directive), F-096 (COGINIT loads $000-$1F7=504 longs; $1F8-$1FF special regs not loaded), F-097 (ADC gains 3.16x/31.6x √10 ladder; fabricated P_ADC_31X→P_ADC_30X).
- **Covered by a Wave-1 edit (no separate action):** F-077 (fit.yaml — done via F-069), F-084 (clock_system config_fields — done via F-029/F-031), F-076 (file.yaml — merged with F-075).
- **REFUTED → WONTFIX:** F-093 (lockrel C polarity) — already correct after F-035; the appendix and YAML both read the right polarity today.

**Gen-script fixes (take effect on PASM2-ENCODING-REFERENCE.md regen):** F-047 (Flags column tested dict-key presence not value → bogus "C,Z" on 344 rows) and F-081 (the %0000/_RET_/IF_NEVER explanatory note). Both fixed in `engineering/tools/gen-pasm2-encoding-reference.py`; the `.md` is regenerated, not hand-edited.

---

## Decomposition-layer supersession sweep — 2026-06-11 (F-102..F-105)

Surfaced while studying the 8 `architecture/patterns-analysis/` files during §15 of the Decomposition Reasoning Layer sprint (KB v1.7.0). These files carried P1-era / foreign-compiler idioms. Seven were superseded by the new `architecture/decomposition/` layer and reduced to redirect stubs (so the incorrect content no longer ships); `asm_integration_analysis.yaml` was kept live and corrected in place. All four findings are therefore **resolved in the same pass** — logged here for the durable record per the "all wrong findings go in the register" rule.

### F-102 — `cog_management_analysis.yaml`: P1 `cognew` cog-start idiom  ·  `DONE` (2026-06-11)

**File:** `deliverables/ai/P2/architecture/patterns-analysis/cog_management_analysis.yaml`

**What was wrong:** `structural_signature` and `implementation_template` started cogs with `cognew(function, stack_pointer)` — a P1 idiom. P2 starts cogs with `coginit` / `cogspin` (`cognew` does not exist in Spin2 for P2).

**Resolution:** File superseded by the decomposition reasoning layer (Force 1 — resource ownership) and reduced to a redirect stub; the `cognew` content no longer ships. Concrete P2 cog-start idioms live in `coginit.yaml` / the `cogspin` method entry.

### F-103 — `timing_control_analysis.yaml` + `state_machine_analysis.yaml`: P1 `CNT` / `waitcnt` timing idiom  ·  `DONE` (2026-06-11)

**Files:** `deliverables/ai/P2/architecture/patterns-analysis/timing_control_analysis.yaml`, `…/state_machine_analysis.yaml`

**What was wrong:** Both used the P1 system-counter idioms `CNT` (e.g. `start_time := CNT`, `state_entry_time := CNT`) and `waitcnt(CNT + delay)`. On P2 there is no `CNT` register read that way and no `waitcnt`: the 64-bit system counter is read with `GETCT()` and waited on with the `WAITCT1/2/3` / `POLLCT*` instructions (or `waitus()` / `waitms()` for unit delays).

**Resolution:** Both files superseded by the decomposition reasoning layer (Force 3 — rate adaptation; control-plane structure) and reduced to redirect stubs (each carries a note flagging the retired CNT/waitcnt idiom); the incorrect content no longer ships.

### F-104 — `memory_management_analysis.yaml`: describes a heap / malloc-free / GC that the P2 does not have  ·  `DONE` (2026-06-11)

**File:** `deliverables/ai/P2/architecture/patterns-analysis/memory_management_analysis.yaml`

**What was wrong:** The entire file described dynamic heap allocation (`malloc`/`free`-style allocators, free lists, fragmentation, garbage collection / compaction). The P2 has **no heap and no runtime allocator** — memory is statically partitioned across hub RAM, each cog's 512-long register space, and LUT RAM, decided at design time. This was not a stray idiom but a wrong mental model that could steer an agent toward a heap that does not exist.

**Resolution:** Replaced with a **corrective stub** (`status: superseded-corrected`) that states plainly the P2 has no heap and redirects to the resource-budget entry; the inappropriate `category` tag was dropped. Incorrect content no longer ships.

### F-105 — `asm_integration_analysis.yaml`: FlexSpin `asm…endasm` inline-PASM syntax + wrong parameter-register model  ·  `DONE` (2026-06-11)

**File:** `deliverables/ai/P2/architecture/patterns-analysis/asm_integration_analysis.yaml`

**What was wrong:** (1) The inline-assembly templates used `asm … endasm` blocks — that is **FlexSpin (fastspin)** syntax, which does not compile with the KB's authority compiler `pnut_ts`; P2 inline PASM uses `ORG … END` inside a method. (2) The example misrepresented parameter passing: `mov pa, ptra ' Get first parameter` — `PTRA` is the pointer register, not the first parameter. In `pnut_ts` inline PASM the method's params/result/locals are addressed **by name** (first param = PR0, second = PR1, return overlaps PR0).

**Evidence:** `deliverables/ai/P2/language/spin2/constructs/inline_pasm.yaml` (canonical ORG…END construct, execution model, register mapping). Corrected example compile-verified with `pnut_ts` v1.55.0.

**Resolution:** This file was kept **live** (inline-PASM integration is a legitimate implementation technique, not superseded by a decomposition force). Fixed **in place**: `asm…endasm` → `ORG…END` in both the template and `structural_signature`; the parameter shuffle replaced with direct by-name register references; added a `compiler_note` flagging `asm…endasm` as FlexSpin-only and a `see_also` to the canonical `p2kbSpin2InlinePasm` construct.

---

## DEBUG-window YAML v55 reconciliation sweep — 2026-06-11 (F-106..F-114, KB v1.8.0)

All nine `deliverables/ai/P2/language/spin2/debug-displays/*.yaml` windows were audited directive-by-directive against PNut **v55** `DebugDisplayUnit.pas` (via `REF/DEBUG-WINDOW-DIRECTIVE-MATRIX.md` + per-window `REF/theory-of-operations/<WINDOW>_Theory_of_Operations.md`). Per-window coverage audits live at `engineering/document-production/manuals/p2-debug-window-manual/audit/yaml-coverage/<WINDOW>-yaml-coverage-audit.md`. Every defect below was **fixed and verified in the same sprint** (validators green; all reworked DEBUG examples compile under `pnut-ts -d` v1.55.0, exit 0) and shipped in **KB v1.8.0** — logged here for the durable record per the "all wrong findings go in the register" rule. This sweep **supersedes the partial F-005** (which covered only plot/logic/midi + pc_key/pc_mouse): F-005's three windows are re-audited and re-grounded here, and the remaining six windows (term/scope/scope_xy/fft/spectro/bitmap) are addressed for the first time.

The pervasive root cause for the six rewritten/created windows: the published YAML was a **marketing-style capability brochure** (generic PC-instrument GUI features) rather than a directive reference, all carrying `documentation_source: Spin2 v51`. The fix replaced each with a v55 directive-grounded spec (ranges/defaults from the compiler source), stripped fabrications into explicit `not_supported:` blocks, added indexed `aliases:`, and wired full-path `related:` cross-links.

### F-106 — `term.yaml` rewrite (FABRICATED 9 · MISSING 14 · MIS-DOC 7 · edition-drift)  ·  `DONE` (2026-06-11, v1.8.0 §1)
Fabricated scrollback/copy-paste/color-theme/window-property prose; 14 real v55 directives absent. **Resolution:** full rewrite from `TERM_Theory_of_Operations.md`; template-setter for the other eight windows. Audit: `TERM-yaml-coverage-audit.md`.

### F-107 — `scope.yaml` rewrite (FABRICATED 9 · MISSING 17 · MIS-DOC 4 · edition-drift)  ·  `DONE` (2026-06-11, v1.8.0 §2)
Fully hallucinated generic-oscilloscope GUI — documented **zero** real `DEBUG(\`SCOPE…\`)` directives; re-introduced every gaps-study fabrication (auto-measurements, cursors, FFT overlay, trigger "modes"). **Resolution:** full rebuild from `SCOPE_Theory_of_Operations.md` directive reference. Audit: `SCOPE-yaml-coverage-audit.md`.

### F-108 — `scope_xy.yaml` created (greenfield; file was ABSENT)  ·  `DONE` (2026-06-11, v1.8.0 §6)
The 9th window had no KB file at all — XY/Lissajous mode was undiscoverable. **Resolution:** authored a new file (14 config + 5 display directives, 6 shared-input handlers, ~26 params) from PNut v55 `SCOPE_XY_Configure/Update/Plot`. NOTE: as a new file it enters `p2kb-index.json` only at the v1.8.0 index regen — inbound `related:` links to it (from `statements/debug.yaml`, `debug-commands/debug.yaml`) resolve post-regen. Audit: `SCOPE_XY-yaml-coverage-audit.md`.

### F-109 — `fft.yaml` rewrite (FABRICATED 6 · MISSING ~20 · MIS-DOC 3 · edition-drift)  ·  `DONE` (2026-06-11, v1.8.0 §3)
Marketing brochure fabricating THD/SNR/peak-frequency/zoom-markers/waterfall and a multi-window-function instrument; documented almost none of the real grammar; falsely listed 4096 as a sample size (FFTmax = 2048). **Resolution:** near-total rewrite from `FFT_Theory_of_Operations.md`; corrected the SAMPLES pow2 4..2048 range + optional `first last` bin-range. Audit: `FFT-yaml-coverage-audit.md`.

### F-110 — `spectro.yaml` rewrite (FABRICATED 11 · MISSING 20 · MIS-DOC 9 · edition-drift)  ·  `DONE` (2026-06-11, v1.8.0 §4)
Documented zero of the ~20 real directives; fabricated a professional spectrogram-analyzer feature set. **Resolution:** full rewrite from `SPECTRO_Theory_of_Operations.md` (real DEPTH/MAG/RANGE/SAMPLES grammar). Audit: `SPECTRO-yaml-coverage-audit.md`.

### F-111 — `bitmap.yaml` rewrite (FABRICATED 11 · MISSING 23 · MIS-DOC 3 · edition-drift)  ·  `DONE` (2026-06-11, v1.8.0 §5)
Named no real directive; invented color formats ("RGBA8888", "RGB565", "1-bit b/w") instead of the 19 real color-mode keywords; whole directive surface absent. **Resolution:** full rewrite from `BITMAP_Theory_of_Operations.md` (19 color modes, SIZE/DOTSIZE/SPARSE/LUTCOLORS/TRACE grammar). Audit: `BITMAP-yaml-coverage-audit.md`.

### F-112 — `logic.yaml` targeted fix (FABRICATED params 3 · MIS-DOC 6 · MISSING-detail 6)  ·  `DONE` (2026-06-11, v1.8.0 §7)
Not a brochure (the file already correctly disclaimed protocol decode/auto-measure), but three **fabricated parameter shapes** and inverted semantics: `SAMPLES {first last}` (LOGIC SAMPLES is a single int 4..2047, not the FFT/SPECTRO bin-range form); `DOTSIZE x {y}` (LOGIC DOTSIZE is a single scalar 0..32); `SPACING` documented as *vertical channel spacing* when it is **horizontal** pixel spacing between samples (the X-axis time base); `RATE` mislabeled "sample rate" (it is a draw-rate divisor); and `TRIGGER` described as a level match when it is **edge-armed** (disarm on non-match → fire on next match). All v55 ranges/defaults were absent. **Resolution:** removed the two fabricated param shapes; corrected SPACING/RATE/TRIGGER semantics; added the full numeric envelope (SAMPLES/SPACING/RATE/DOTSIZE/LINESIZE/TEXTSIZE/HOLDOFF/offset) and the enumerated 12 packing modes; preserved the existing protective disclaimers. Audit: `LOGIC-yaml-coverage-audit.md`.

### F-113 — `plot.yaml` enrichment (FABRICATED 0; under-specified geometry/sprite params)  ·  `DONE` (2026-06-11, v1.8.0 §8)
Breadth-complete and hallucination-free, but **depth-thin**: CIRCLE/OVAL/BOX/OBOX shown as `...`; SPRITEDEF/SPRITE/POLAR/CARTESIAN params elided; OBOX mislabeled "outlined" when it is a **rounded** rectangle; a latent bad example (`CIRCLE 128 128 40` — CIRCLE takes only `width`). **Resolution:** filled all geometry param shapes (with the `linesize 0 = filled` rule + centered-on-current-position note), the SPRITEDEF element-array + SPRITE/POLAR/CARTESIAN params and ranges, config defaults (SIZE/DOTSIZE/OPACITY/LAYER), the TEXT inline-override + TEXTSTYLE bitfield, and SAVE region syntax; corrected the OBOX label and the CIRCLE example. Confirmed the gaps-study `plot-layers.yaml` split recommendation is **superseded** (LAYER/CROP/SPRITEDEF/SPRITE share PLOT_Update dispatch state — kept in plot.yaml). Audit: `PLOT-yaml-coverage-audit.md`.

### F-114 — `midi.yaml` minor enrichment + phantom-mode confirmation (FABRICATED 0; 13/13 verified)  ·  `DONE` (2026-06-11, v1.8.0 §9)
Already clean and v55-accurate. **Resolution (additive only):** added indexed `aliases:`, the RANGE default (21..108) + lastKey≥firstKey clamp, the CHANNEL "0 = channel-0-only, not all-channels" semantics, the SIZE scalar formula (8 + n*4), and a structured `not_supported:` block. Preserved the distinguishing negative claim that **MIDI is the only DEBUG window that rejects `HIDEXY`**. Audit: `MIDI-yaml-coverage-audit.md`.

### F-114b — MIDI phantom display modes KEYBOARD / GRID / ROLL / MONITOR  ·  `RESOLVED-INVALID` (2026-06-11)
The gaps study (`studies/yaml-database-gaps-discovered.md`, lines ~112–118) flagged a HIGH-priority "MIDI Display Mode Specifications" gap claiming KEYBOARD/GRID/ROLL/MONITOR modes should be added to `midi.yaml`. **These modes do NOT exist in PNut v55.** `MIDI_Configure` (2506–2525) has exactly six arms (`key_title`, `key_pos`, `key_size`, `key_range`, `key_channel`, `key_color`); there is no display-mode directive and `MIDI_Update` has no mode switch — MIDI is a single-mode live piano-keyboard display. **Action:** do NOT add these modes; they are correctly absent from `midi.yaml`, which now also carries an explicit `not_supported:` negative claim. The gaps-study entry should be treated as RESOLVED-INVALID so it is not re-actioned.

### F-114c — Debug-window findability wiring (entry-point dead-end + category)  ·  `DONE` (2026-06-11, v1.8.0 §10)
The parent `language/spin2/statements/debug.yaml` enumerated every window in prose (`display_types:`) but its `related:` block held only **bare-prose topics** ("Display types", "Formatting functions", …) with no real links — a traversal dead-end (the original failure mode that prompted this whole audit), and it omitted SCOPE_XY entirely. **Resolution:** added SCOPE_XY to the enumeration; converted `related:` to full-path down-links to all nine window files (relocating the prose topics to `see_also:` per Sacred Rule #7 — relocated, not dropped); added reciprocal window links on `debug-commands/debug.yaml`; and registered a new `spin2.debug_displays` category in `engineering/tools/p2kb-categories.json` listing all nine files so `p2kb_find` set-browsing surfaces them.

---

## Shipped-YAML provenance self-sufficiency (data-set-wide) — 2026-06-12 (F-115)

Surfaced during the ingestion front-door restructure (the `spin2_lang_ref_v55` → `spin2-v55` folder-rename audit). **Not a content error** — a **provenance-format** defect class: shipped YAML fields cite **working-tree paths** (`engineering/ingestion/...`, `engineering/document-production/...`) + line ranges. This violates the YAML self-sufficiency rule (shipped YAML must reference only internal KB keys + durable bibliographic citations — provenance stays in plan/commits). Working paths (a) do not resolve for a download-on-demand MCP consumer, and (b) are brittle: they had to be hand-patched when the v55 source folder was renamed in this very session.

### F-115 — working-tree paths embedded in shipped-YAML provenance fields  ·  `CONFIRMED` (2026-06-12)

**Scope (data-set-wide):** **42 files** under `deliverables/ai/P2/` embed an `engineering/…` working path; **25** carry it in a `source:`/`sources:` field, the rest in `source_example` / `source_listing` / `example_source` / `source_of_truth` / `primary_source` / `companion_doc` / `path` / `rom_booter_listing` / etc. Enumerate the full set before fixing:
```
grep -rlE "engineering/(ingestion|document-production|operations|tools)/" deliverables/ai/P2
```

**Originally surfaced (the 4 that triggered this):**
- `language/spin2/methods/qsin.yaml:42` · `language/spin2/methods/qcos.yaml:40` — `source: "engineering/ingestion/sources/spin2-v51/spin2-text.txt:5141-5143 …"` (trace back to the F-001 fix, which introduced the working-path provenance).
- `language/spin2/debug-commands/pc_key.yaml:11` · `pc_mouse.yaml:11` — `source:` citing both an `engineering/ingestion/sources/spin2-v51/debug-section.txt:…` path **and** an `engineering/document-production/manuals/…/REF/…md` path.

**Notable:** all **10 debug-display YAMLs shipped in v1.8.0** (`debug-displays/{term,scope,scope_xy,fft,spectro,bitmap,logic,plot,midi}.yaml:~12`) carry `source: "engineering/document-production/…"` — so the most-recent release added more instances of this class.

**Proposed correction:** Replace each working-path provenance with a **durable bibliographic citation** — e.g. `source: "Parallax Spin2 Language Reference v51a — QSIN/QCOS (CORDIC methods); examples compile-verified with pnut_ts v1.55.0"`, dropping the `file:line`. Where the path was the only pointer to a host-side/manual detail, move that detail into prose, not a working path. **Fix the whole class in one sweep** (per the fix-all discipline — do not patch only the 4), via `yaml-knowledge-base-maintenance`; triggers an index regen + release. See [[feedback_yaml_self_sufficient_references]] and [[feedback_no_unsourced_claims]].
