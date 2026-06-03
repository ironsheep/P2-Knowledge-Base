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

### F-021 — `modes-reference.yaml` is missing several valid mode rows  ·  `NEEDS-VERIFICATION` (completeness)

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

### F-023 — `setxfrq.yaml` SETQ+SETXFRQ "64-bit precision frequency" claim is unverified  ·  `NEEDS-VERIFICATION`

**File:** `deliverables/ai/P2/language/pasm2/setxfrq.yaml` (description ~L14-15, example 3 ~L44-49, `related_instructions` SETQ note)

**What's suspect:** The file states "For SETQ+SETXFRQ pattern, SETQ provides low 32 bits, D provides high 32 bits for 64-bit precision frequency control." The streamer NCO is a single 32-bit (31-bit-effective) phase accumulator — there is no 64-bit NCO frequency register, so a "64-bit precision" frequency word is dimensionally suspect. Not mentioned in the Silicon Doc v35 SETXFRQ section (`p2-documentation.txt:2753-2790`).

**Why not fixed now:** Surfaced 2026-06-03 during the F-016 scaling fix; left **verbatim** per the hard-facts rule (no golden source consulted on what SETQ-before-SETXFRQ actually does). The F-016 edit changed only the 2³¹/2³² scaling, not this claim.

**Proposed action:** Verify against the Silicon Doc / `pnut_ts` whether SETQ augments SETXFRQ at all. If unsupported, remove the 64-bit claim from the description, example 3, and the `related_instructions` SETQ note.

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
