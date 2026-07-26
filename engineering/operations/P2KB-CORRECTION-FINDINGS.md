# P2KB Correction Findings — Consolidated Register

**Purpose:** A single, append-only register of everything we discover that is **wrong or needs correction** — primarily in the P2 Knowledge Base YAML (`deliverables/ai/P2/`), but also any other source/content correctness issue worth tracking. This is the hand-off document for the agent that corrects the P2KB (via the `yaml-knowledge-base-maintenance` skill).

**How to use this register:**
- When any work (manual production, audits, example compilation, ingestion) surfaces something incorrect, **add it here** — do not leave it only in a per-manual note.
- Each finding gets: an ID, a status, the exact location, what's wrong, the evidence, and the proposed correction.
- **Annotate as you fix, same pass** — flip the status, add an applied-note + source trace, and log any newly-surfaced defects as new findings. See `yaml-knowledge-base-maintenance` skill §4.5. A stale register (statuses lagging the YAML) lies and invites re-chasing.

**Status legend:** `CONFIRMED` (verified against an authority; ready to fix) · `NEEDS-VERIFICATION` (suspected; must be checked before acting) · `DONE` (corrected + verified) · `WONTFIX` (investigated, not a defect) · `RESOLVED-INVALID` (the reported defect does not exist) · `TRACKED → ingestion` (real, but the resolution lives in the ingestion head, not a YAML edit).

**Authority order for P2 language facts:** the `pnut_ts` compiler (ground truth for what compiles) → the Spin2 v55 documentation (`engineering/ingestion/sources/spin2-v55/`) → the Silicon Doc. The KB YAML must match these.

**No inference or derivation.** Every correction must trace to an authoritative source (compiler / hardware-verified / Silicon / authoritative derived YAML). Aligning a file to an authority it contradicts (its own fields, a sibling, the instruction CSV, the compiler) is fine; **inventing a value or claim that no source states — by computation, reasoning, or "it must logically be" — is not.** If a change can only be justified by inference, do **not** make it: log it as a finding that needs a source (or proposes removing the unsupportable content). Match the source's wording, not an interpretive paraphrase.

**Next finding ID: `F-216`** (F-205 = PLOT TEXTSTYLE justification; F-206 = debug-displays `SAVE` filename; F-207 = packed-feed pattern for scrolling LOGIC/SCOPE windows; F-208 = PLOT POLAR orientation undocumented; F-209 = Debug sweep v55-over-Pascal reversals; F-210 = Assembly Ch5 clock-field naming; F-211 = I/O pin power-domain group size 4→8 across KB; F-212 = debug-displays YAML corrections from the 2026-07-12 coverage re-audit; F-213 = P2AN007 R3 ack-handshake removal invites a torn read; F-214 = mnemonic-bold filter uppercases mnemonics inside hyphenated names, corrupting filenames/slugs in RELEASED PDFs; F-215 = shipped app-note PDFs carry a never-shipped v0.1.0 draft in their Revision History, contradicting their own cover)

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

## Open — enhancement proposals (new content, not corrections)

- **ENH-01 — Harvest the Architect's Guide *project front-end* into a new KB node set.** *Scheduled
  2026-07-08 (deferred from the Architect's Guide v1.0.0 release); Stephen go/no-go before authoring.*
  Source: *The P2 Architect's Guide* v1.0.0, **Part I (Act I)**. The decomposition-reasoning layer
  (`architecture/decomposition/`) begins *at* "which cog owns what"; nothing in the KB captures the
  **pre-decomposition** front-of-project work Part I lays out. Candidate new node set — reusable P2
  **design-process** patterns that sit *above* the decomposition layer: feasibility-before-design ·
  **narrow-vs-broad comms selection** (I²C/SPI vs host-style ribbon) · **offload-vs-port /
  companion-device partitioning** · pin-budget → adapter-board · "characterization becomes the spec" ·
  firmware-loaded-device → loader. Also a small KB touch worth doing: **performance → P2-resource
  mapping** (which performance need → LUT RAM / PSRAM / CORDIC / streamer — Architect's Guide Act III
  P-7). **Do NOT harvest the Act III agentic principles** (about *using agents*, not the P2 — low KB
  value). Fuller rationale table lives in the manual's `PLANNING.md` (KB-harvest proposals).

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

### F-206 — `debug-displays/{term,fft,logic,midi,scope,scope_xy}.yaml` under-specify the `SAVE` command's required filename (inconsistent across the set) — `CONFIRMED · YAML APPLIED 2026-07-11 (pending KB publish)`

> **APPLIED 2026-07-11:** all six `SAVE` lines standardized to `SAVE {WINDOW} 'filename' -- ...
> filename is REQUIRED; WINDOW optional`, matching v55 L1139 (WINDOW = entire window; absence =
> display area). `plot.yaml:77` was already correct (unchanged). D1 (Stephen): bare-`SAVE` compiles
> legal on `pnut-ts` but runtime auto-name is unverified → not documented; the required-filename form
> is the one taught.

**Surfaced:** 2026-07-11, while correcting the Debug Window Manual's `SAVE` prose (ch05/ch10) in the fleet-release sweep (commit 828e62ae).

**What's wrong:** the `SAVE` runtime command takes a **required** filename per the v55 spec `SAVE {WINDOW} 'filename'` (only `{WINDOW}` is optional) and the REF matrix (`KeySave`, 2839-2866: `SAVE 'name'` → `name.bmp`), but the shipped YAMLs describe it three different ways:
- `plot.yaml:77` — `SAVE 'name' -- ...` ✅ correct (filename shown, required; also has the `l t w h 'name'` region form)
- `term.yaml:45`, `fft.yaml:56` — bare `SAVE -- write the window bitmap to <name>.bmp` (no filename arg shown → implies `SAVE`-alone works)
- `logic.yaml:46`, `midi.yaml:38`, `scope.yaml:58`, `scope_xy.yaml:50` — `SAVE {filename} -- ...` (braces imply the filename is optional)

**Evidence:** v55 text lines 1139/1169/1194/1222/1246/1294 all show `SAVE {WINDOW} 'filename'` (filename un-braced = required); REF `DEBUG-WINDOW-DIRECTIVE-MATRIX.md` L337/L504 shows `SAVE 'name'`.

**Proposed correction:** standardize all six to the v55/REF form — `SAVE {WINDOW} 'filename' -- write the window (or display-area) bitmap to <filename>.bmp` (filename required; `WINDOW` optional). Keep PLOT's extra region form.

**Verify first:** confirm whether PNut-Term-TS also accepts a bare `SAVE` (auto-generated name). If it does, document that as a lenient alternate — the required-filename form is still the one to teach (the manual was corrected to it in this sweep).

### F-207 — packed-data feed for **scrolling** LOGIC/SCOPE windows requires a **full-window array feed** (`` `uhex_long_array_ ``); a single `` `(packed) `` long does NOT fill the window — `CONFIRMED` (manual DONE + HW-verified · KB enrichment pending)

**Surfaced:** 2026-07-11, fleet-release sweep — two published Debug Window Manual ch13 examples rendered only a fragment. **Root cause hardware-verified** the same day (Stephen ran the reshaped figure-generators; Claire read the BMPs back via image-tools).

**What's wrong (empirical ground truth):** for the **scrolling time-series** windows (LOGIC, SCOPE), feeding packed sample data as a **single** `` `(packed) `` long per message renders only a fragment — it does **not** accumulate/unpack across the window. The **only** feed that fills the window is the **full-window array feed** `` `uhex_long_array_(@buff, N) ``, which is also the **only packed example the v55/v51 docs ever show** (v55 text line ~1144 / v51 line ~1858, identical). The BITMAP (frame-buffer) window **tolerates** a per-long packed feed — which is why `ch13-packed-bitmap-frame` was always correct and was left untouched; that isolates the defect to the **feed shape for scrolling windows**, not the packing mechanism itself.
- **Pre-fix measurements:** LOGIC — data only in the last long's band (right-edge fragment). SCOPE — data only in the first few bands (left-edge fragment).
- **Post-fix hardware renders (2026-07-11 19:00, `fig-13-*_WDW.bmp`):** LOGIC = **full-width** random D0 trace (left edge, blank pre-fix, now packed with transitions); SCOPE = **two 0–255 sawtooths** (A + B), full vertical sweep. Both fixes empirically confirmed.
- SCOPE also had a 2nd defect: channel-defs lacked the **required** range → fixed to `'A' 0 255 'B' 0 255` (per the `'label' AUTO|lo hi` rule, F-137/EF-003 lineage).

**Manual — DONE (this sweep, HW-confirmed).** Fixed lockstep in opus-master `ch13-packed-data.md` + examples-library + figure-generators (byte-identical example↔code-block; corpus identity GREEN 32/32; compile clean `pnut-ts -d`): logic → `VAR buff[8]` (8 longs = 256 samples) fed via `` `uhex_long_array_(@buff, 8) ``; scope → `VAR buff[128]` array feed + the `'A' 0 255 'B' 0 255` ranges; prose gained an array-feed paragraph.

**Facet B — packing mode must match the LOGIC channel count (user-reported + HW-CONFIRMED 2026-07-11).** Stephen, exercising the *shipped* ZIP, found the (old) `packed-logic-stream` example declared **two** channels but used **LONGS_1BIT** → **all samples drew on the first channel only**; changing it to **LONGS_2BIT** made both channels display. The rule (grounded in how LOGIC unpacks): for LOGIC the packing mode's **bits-per-sub-sample must equal the channel count** — `LONGS_1BIT` = 1 channel, `LONGS_2BIT` = 2, `LONGS_4BIT` = 4, `LONGS_8BIT` = 8; each sub-sample carries one bit **per channel** per time-step. (SCOPE differs: an 8-bit-packed SCOPE sub-sample is a full per-channel *value*, and channels interleave across consecutive sub-samples — cf. `ch13-packed-scope` = 2 channels A/B via `LONGS_8BIT`.) Our reshaped `ch13-packed-logic-stream` currently sidesteps this by using a **single** channel `'D0'` + `LONGS_1BIT` (consistent, HW-confirmed) — the shipped bug cannot recur in it — but the richer, on-intent demo is 2 channels + `LONGS_2BIT` (design decision open with Stephen; would need one more render).

**KB — enrichment pending (the class-wide/systemic angle → yaml head).** The shipped KB documents the packing **modes** (`debug-displays/logic.yaml:37`, `scope.yaml:39`) and the concept ("packed-data modes let you pack multiple sub-samples", `logic.yaml:88`), and `statements/debug.yaml` shows the normal per-sample feed — but **no KB file shows the packed full-window feed**, states the single-`` `(packed) ``-long-won't-fill-a-scrolling-window fact, **or ties the packing mode to the channel count** (`logic.yaml:38` only covers the multi-bit-*bus* `count` field, not mode↔channel-count). A remote agent generating packed LOGIC/SCOPE code from the KB would reproduce both the fragment defect and the all-on-channel-0 defect.

**Proposed KB action:** (1) add a **packed full-window array-feed example** to `debug-displays/logic.yaml` and `debug-displays/scope.yaml` (and the packed-mode note in `statements/debug.yaml`) — `` `uhex_long_array_(@buff, N) `` matching v55's only packed example — plus the caveat: *a single packed-long feed advances the scrolling window by one column only; the full window requires the array feed* (BITMAP is exempt). (2) Document the **mode↔channel-count** rule in `logic.yaml` (LONGS_NBIT ⇒ N one-bit channels) and the SCOPE value-interleave form in `scope.yaml`.

> **KB APPLIED 2026-07-11 (pending KB publish):** both facets landed. `logic.yaml` — `packed:` gains the
> sub-sample-width = channel-count rule (Facet B) + a new LONGS_2BIT full-window array-feed example
> and an array-feed/unpack note (Facet A, unpack semantics quoted from v55 L1143/L1406). `scope.yaml`
> — `packed:` gains the per-channel-value interleave form (Facet B) + a LONGS_8BIT array-feed example
> and left-edge-fragment caveat (Facet A). `statements/debug.yaml` — a packed scrolling-window
> array-feed example cross-referencing both. D2 (Stephen): essential feed-shape snippet, NOT the
> verbatim v55 streamer example (incidental + misleading re streamer-required); unpack semantics
> quoted verbatim.

**Verify first (at fix time, §4.5):** open v55 text line ~1144 (and the REF Pascal-derived matrix / `DebugDisplayUnit.pas SetPack`) and match wording exactly — do not paraphrase. Facet A's feed-shape claim is grounded in the 2026-07-11 hardware renders + v55 showing only the array form. **Facet B is a peer report (Stephen), not yet our own hardware run — confirm on silicon before enriching the KB** (empirical > documentary); the LONGS_2BIT 2-channel render, if we adopt that example, IS that confirmation.

### F-208 — PLOT POLAR orientation (θ=0 baseline direction) is undocumented; the rotation-sense wording is murky/likely-wrong — `CONFIRMED` (Test J)

**Surfaced:** 2026-07-11 — Test J had to be run to *learn* the POLAR orientation because it is documented nowhere. Per the **test-to-learn = doc/KB gap** rule (Stephen's call this date), the learned fact must be written back into both the KB and the manual, not consumed once.

**What's wrong / missing:**
- **θ=0 baseline direction is documented NOWHERE** — neither `debug-displays/plot.yaml` nor ch05-plot.md states where angle 0 points. Test J resolved it: **θ=0 → East (+x); increasing θ is counter-clockwise** (math convention); no flip.
- **Rotation-sense wording is murky/likely-wrong:** `plot.yaml:62` — *"twopi -1/0 select clockwise/counter-clockwise sense."* The default `twopi` is `$1_0000_0000` (positive → CCW), **not** 0; and the "-1/0" shorthand fails to convey the actual rule — a **negative** `twopi` reverses to clockwise.

**Evidence:** Test J (`conflict-testJ-polar-theta0`, both platforms 2026-07-11): sampling ρ≈150 from origin — **East=RED (0°)**, North/up=GREEN (90°), West=BLUE (180°), South=YELLOW (270°) → θ=0 East, CCW. Recorded in `audit/v55-vs-REF-reconciliation-2026-07-10.md`; EF entry pending (§7.6 / #196).

**Proposed correction (KB → yaml head):** in `plot.yaml` POLAR directive, state that **θ=0 points East (+x)**; the default (positive `twopi`) sense is **counter-clockwise**; a **negative `twopi` reverses to clockwise**. Replace the `"twopi -1/0"` shorthand with that sign-based rule.

> **YAML APPLIED 2026-07-11 (pending KB publish):** `plot.yaml:62` POLAR now reads "*Orientation:
> theta=0 points East (+x); with the default (positive) twopi the angle increases counter-clockwise;
> a NEGATIVE twopi reverses the sweep to clockwise*" — the murky `"twopi -1/0"` shorthand is gone.
> Manual side already applied (#195). Grounded EF-032/Test J.

**Manual side (→ ch05-post #195-C):** add the same orientation fact to the ch05-plot.md POLAR section — re-scoped from "optional enhancement" to **required gap-fill**.

**Grounding:** Test J (empirical > documentary). Cite the EF once promoted.

### F-209 — Debug manual: the `f3e702ed` correctness sweep INVERTED higher-authority Pascal/REF for three DEBUG-window facts (trusted v55 text over ground truth) — `DONE 2026-07-11 (reverted)`

**Surfaced:** 2026-07-11 by the fleet **changeset-integrity audit** (independent adversarial pass). Three hunks from the *pre-empirical* sweep `f3e702ed` followed **v55 text** where the Pascal-derived REF/matrix — higher authority in the DEBUG-window chain **Pascal → REF → v55** — says the opposite. The later empirical work fixed *around* them but never re-caught them. Class: v55-text-over-Pascal reversal (`feedback_handverify_audit_findings` — the underlying fanout findings inverted).

**Instances (all reverted in opus-master 2026-07-11):**
- **D-F1 (HIGH) — PLOT PRECISE default.** `ch05-plot.md` claimed sub-pixel is OFF by default (one `PRECISE` turns it on). REF `PLOT_Theory_of_Operations.md` L215/L244/L383: `vPrecise := 8` at `PLOT_Configure` = **sub-pixel ON at creation**, `PRECISE` XORs 8↔0. As shipped, a reader issuing one `PRECISE` for smooth curves would turn sub-pixel **OFF** — the opposite of intent. **Reverted** to sub-pixel-default. (v55 L1271 "disabled" is the sole opposing source.)
- **D-F2 (MED) — TERM default color.** `ch03-term.md` + `appendix-c` relabeled the default pair-2/3 green "Green"; **EF-025** confirmed the default renders `clLime $00FF00`, distinct from the `GREEN` keyword `$09FF09`, disposition "keep Lime + reader-note." **Restored "Lime"** + added the reader-note; `term.yaml` already correct. (Explicit `GREEN`-keyword usages left unchanged.)
- **D-F3 (LOW-MED) — LOGIC DOTSIZE.** `ch06-logic.md` dropped the LOGIC `DOTSIZE` config row (v55 LOGIC table omits it); REF matrix L90 `DOTSIZE ✅` + L260 lists it, and `logic.yaml:32` documents it. **Restored** the row (default 0, range 0–32).

**Class-wide sweep — DONE 2026-07-11 (found + fixed 5 more + 1 conflicted + 1 restore):** the independent pass over `f3e702ed`'s DEBUG-window edits vs Pascal/REF confirmed the class was NOT clear beyond the first three (`feedback_classwide_sweep_on_every_finding`). All hand-verified against the REF theory-of-ops + matrix and applied in opus-master:
- **F-1 (FFT)** `ch09` channel-def `legend`→**`grid`**, removing fabricated bits 2–3 (legend-text). REF `FFT_Theory` L110/L203: grid is 2-bit (bit0=baseline, bit1=top), default 0. Twin `ch09-fft-spectrum.spin2` comment updated in lockstep (identity GREEN).
- **F-2 (BITMAP)** `ch04` SPARSE: "round-dot / needs DOTSIZE≥4 / sets background color" → **outline each magnified pixel; `color` sets the outline (grid) color** (no ≥4 gate). REF `BITMAP_Theory` L91/L156/L272: `vSparse` = pixel BORDER color. *(NOTE: BITMAP was never hardware-tested; round-vs-square shape rests on Pascal/REF — a quick SPARSE visual would confirm.)*
- **F-3 (BITMAP)** `ch04` LUT-without-palette "entries 0–7 hold default colors" → **uninitialized → garbage until `LUTCOLORS`**. REF `BITMAP_Theory` L605 (`SetDefaults` does not init `vLut[]`).
- **F-4 (POS default)** `0,0`→**cascaded** in TERM/LOGIC/SCOPE_XY/MIDI. REF `LOGIC_Theory` L362/L506.
- **F-5 (TITLE default)** `none`→**(window name)** in TERM/PLOT/LOGIC. REF `LOGIC_Theory` L361.
- **S-6 (half-pixels)** SCOPE/FFT LINESIZE + SCOPE_XY DOTSIZE reverted to **pixels** — per **EF-027** (LINESIZE 3→3px, 1:1) + LOGIC-says-pixels consistency (the radius-arithmetic basis is refuted empirically).
- **N-1 (PLOT)** restored the dropped "default text color is **white (`$FFFFFF`)**" fact (PLOT theory L242).

**Grounding:** REF `PLOT_Theory_of_Operations.md` + `DEBUG-WINDOW-DIRECTIVE-MATRIX.md` (both Pascal-derived) + `EF-025`. Empirical/Pascal outranks v55 text.

### F-210 — Assembly manual Ch5 §5.7.6 clock-config field names contradict Ch4 §4.1.4 — `DONE 2026-07-11`

**Surfaced:** 2026-07-11 by the changeset-integrity audit. Ch5 labeled the HUBSET clock-config low fields `PPPP_XX_CC` (XX=caps, CC=source); Ch4 §4.1.4 (changed in the same `f3e702ed` set) uses `PPPP_CC_SS` (CC=caps, SS=source) — the P2/Silicon-Doc standard. So `CC` denoted *source* in Ch5 and *caps* in Ch4. Bit **values** correct in both (code assembles); a reader decoding via field names would read `CC` two ways. **Fix (applied):** relabeled Ch5 to the standard `PPPP_CC_SS` (values unchanged). An internal cross-chapter naming inconsistency introduced by the sweep — **not** a v55-over-Pascal issue.

**Grounding:** P2 Silicon Doc HUBSET clock-config field layout (`%PPPP_CC_SS`: CC=caps bits 3:2, SS=source bits 1:0); matches Ch4.

### F-211 — I/O pin power-domain group size is wrong across the KB: "isolated groups of **four**" (16 groups) — actual = **8 groups of 8** (P0-7 … P56-63) — `DONE 2026-07-11 (YAML applied; pending KB publish at §9)`

> **APPLIED 2026-07-11 (yaml head).** Corrected 4→8 across all 5 files: `pin-power-domains.yaml`
> (title, description, `power_grouping.group_size` 4→8, `groups:` "16 groups"→"8 groups", boundaries
> 0-3,4-7→0-7,8-15, `multi_pin_constraint` straddle example pins 3/4→7/8, oneliner, `power group of 4`
> alias→`of 8`); `smart-pin-11000/11010/11001-adc-*.yaml` (`power_domain.fact` + `multi_pin_layout` +
> `see_also`, and 11000's multi-channel code comment); `application-notes/p2an001-*.yaml` (the pitfall
> line). **Removed the fabricated `evidence` citation** ("P2 Datasheet: 'Power for smart pins in groups
> of 4'" — unverifiable; the Silicon Doc uses `{x}_{y}` placeholders, no "4") and replaced it with honest
> durable sources: Silicon Doc per-group VIO/GIO pin table + the P2 Edge/eval breakout electrical spec
> ("300 mA per 8-pin group; one VIO3V3/GND pair per 8-pin header"). **Left untouched (correctly NOT the
> power-domain error):** 11010's "four 4-pin-block samples" (that's the SCOPE/streamer channel-nibble
> aggregation, not power grouping); p2an001 companion's "8-pin bytecode-interpreter ADC" (an OBEX object
> name, EightPinADC); the 11000 multi-channel example's "4 consecutive INDEPENDENT channels" (a legit
> 4-channel demo, not a power-group claim). **Source trace:** VIO/GIO are per-group, 8 groups of 8
> (`engineering/ingestion/external-sources/hardware-verification/VERIFICATION-OPPORTUNITIES.md:57`;
> edge-mini-breakout extraction "300 mA per 8-pin group"; Silicon Doc VIO_{x}_{y}/GIO_{x}_{y} per-group;
> memory `reference_p2_adc_per_group_vio_gio`). YAML format + crossref validated clean. Index regen +
> KB publish ride §9 (`release-yamls`), per Stephen's "make the changes, don't release yet."

**Surfaced:** 2026-07-11 by the changeset-integrity audit of the P2AN001 content delta (Gap A;
report `engineering/planning/CHANGESET-AUDIT-app-notes-content-2026-07-11.md`). The P2AN001 **manual**
was corrected 4→8 in `f3e702ed` (audited faithful), but the shipped **KB YAML** still teaches the old
4-pin grouping — a manual↔YAML drift, plus a class-wide error in the canonical power-domain file.

- **What's wrong:** the KB says P2 I/O pins are powered in **isolated groups of four** (pins 0-3, 4-7, …,
  60-63 = "16 groups"). The P2 actually powers I/O in **8 groups of 8** — P0-7, P8-15, …, P56-63 — each
  group with its own VIO/GIO pair.
- **Evidence (three independent, hardware-grounded):**
  - `engineering/ingestion/external-sources/hardware-verification/VERIFICATION-OPPORTUNITIES.md:57` —
    "**VIO/GIO are PER-GROUP, not global.** The 64 pins are 8 groups of 8 (P0-7, P8-15, …)".
  - `engineering/ingestion/sources/edge-mini-breakout/…-complete-extraction-audit.md:104` +
    `extraction-matrices/edge-module-breakout-compatibility-matrix.md:70` — "300 mA per **8-pin group**"
    (a hard electrical spec from the Parallax breakout doc; one VIO3V3/GND per 8-pin header).
  - Silicon Doc VIO_{x}_{y}/GIO_{x}_{y} = "power/ground for smart pins {x} through {y}" — placeholder
    span, i.e. it does **not** state "4"; consistent with 8.
  - Corroborated by memory `reference_p2_adc_per_group_vio_gio` (written during the F-203 pin-to-pin
    spread test design).
- **Fix (class-wide — `yaml-knowledge-base-maintenance`; rides the KB rail):**
  - `architecture/pin-power-domains.yaml` — canonical file: title (L2 "Groups of Four"), body (L14),
    `groups:` (L20 "16 groups"), `oneliner` (L48), and **the `sources:` datasheet citation (L35-36)
    quoting "Power for smart pins in groups of 4" / "group boundaries align on multiples of 4" — this
    quote appears fabricated (the Silicon Doc uses `{x}_{y}` placeholders, not "4"); verify against the
    primary P2 datasheet pin table and replace/remove it.** Change 4→8, "16 groups"→"8 groups".
  - `architecture/smart-pins/smart-pin-11000-adc-internal-clock.yaml` (power_domain L172-176, see_also
    L186, code comment L117), `…-11010-adc-scope-trigger.yaml` (L144-148, L160),
    `…-11001-adc-external-clock.yaml` (L186-190, L200).
  - `application-notes/p2an001-single-pin-instrumentation-adc.yaml:99` (companion YAML — the manual is
    already at 8-pin; align the companion).
  - (Stale `.backup.*` copies carry it too — cleanup only, not served.)
- **Note:** the *mechanism* the KB teaches (per-group VIO/GIO reference; multi-pin shared-node
  measurements must stay within one group; single-pin ratiometric reads are absolute) is **correct** —
  only the group **size/count** (4/16 → 8/8) and the group boundaries (…0-3,4-7… → …0-7,8-15…) are wrong.

### F-212 — Debug-displays YAML corrections surfaced by the 2026-07-12 coverage re-audit (per-file batch) — `DONE`

> **APPLIED 2026-07-14** (commit `35166ad4`), as the KB half of the single coordinated Debug sweep, together with
> F-216's manual half. 13 files: the 9 window YAMLs + `pc_mouse.yaml`, `statements/debug.yaml`,
> `debug-formatters-complete.yaml`, `constants/special-configuration-symbols.yaml`.
> Landed: the **inversions** (`fft.yaml` MAG = GAIN not divisor; `spectro.yaml` axes; `midi.yaml` velocity-0
> note-off + velocity-sets-HEIGHT; `pc_mouse.yaml` raw-client-pixels for 5 of 9 windows; `term.yaml` the
> non-existent `LIME` keyword); the **unsourced packing default** (`scope.yaml`/`scope_xy.yaml` "default
> LONGS_1BIT" → there is no default, unpacked); the ADDENDUM in full; and the hardware verdicts (EF-020 CARTESIAN
> Y-UP — the single most important PLOT fact, previously absent from the KB entirely; EF-042 SPARSE + the
> DOTSIZE≥4 gate; EF-043 POS is tool-dependent, swept across **all nine** windows; EF-048 OPACITY 256 → 0;
> EF-052 runtime `RATE -1` freeze), plus `CLOSE` semantics and the real TITLE default caption across all nine.
> **Validated:** YAML parse clean; `validate-crossref-keys.py` — all cross-references resolve.
> **DO-NOT-TOUCH list honored:** `scope.yaml` "prevents the window from being created" (correct — the *manual*
> was the one to fix, and was); `bitmap.yaml`/`ch10` packing "unsigned by default" (correct).

**Surfaced:** 2026-07-12, the coverage-tracked exhaustive re-audit of the Debug Window Manual against the latest ratified
REF (matrix + 9 Theory-of-Operations docs re-grounded on raw `DebugDisplayUnit.pas`, commit `360a9c15`). Full per-item
evidence + line numbers in the manual audit report `…/p2-debug-window-manual/audit/release-gate-2026-07-12-COVERAGE.md` §2.
Every item below is a place a shipped **debug-displays YAML contradicts the authority** (ToO/matrix/`.pas`/EF ledger) — the
manual is correct in each case unless noted. **Gate:** drain with F-207/F-208 in the single debug-displays YAML pass; do
not publish the Debug manual until landed (`yaml-knowledge-base-maintenance` → `release-yamls`).

- **`fft.yaml` (HIGH ×2):** (a) `grid` documented as 2-bit → it is **4-bit `%abcd`** (bit2/bit3 = min/max legend TEXT; FFT
  never sets `vLow` so bit-2 shows `+0`). (b) **`MAG` inverted** — recorded as "right-shift **divisor**"; it is a **gain
  ×2^mag** (power formula `Hypot/($800 shl FFTexp shr FFTmag)`; ToO §11.4). This tells a KB agent MAG *attenuates* when it
  *amplifies* — an AI-trust inversion. Manual (ch09) correct on both.
- **`spectro.yaml` (HIGH):** axis assignment inverted (L52/L53/L82). Default `$F` = **time-X / freq-Y** (swap fires only when
  `vTrace and $4 = 0`, i.e. traces 0-3 → freq-X). ToO §4.1/§22.1 (`SPECTRO_Configure` 1751-1787) + validated fig-10 run-up.
  Manual (ch10:124-126) correct.
- **`midi.yaml` (HIGH + MEDIUM):** (a) velocity-0 note-on claim wrong — a velocity-0 note-on stores 0 and the fill test is
  `MidiVelocity > 0`, so the key reads **OFF** (no explicit `$80` required); ToO §5.1/§18.1/§19.3. (b) "velocity sets the key
  **color**" → velocity sets fill **HEIGHT** (no color gradient; hue fixed per key type; ToO §19.3). Manual (ch11) correct.
- **`pc_mouse.yaml` (HIGH):** `coordinate_basis_per_window` reproduces the §4.4a on-screen **readout**, not the §4.4b
  **wire** value the P2 receives — wrong for LOGIC/SCOPE/SCOPE_XY/FFT/MIDI. Correct wire: raw client pixels for those five;
  `÷DOTSIZE` (+CARTESIAN flip) for PLOT/SPECTRO/BITMAP; char col/row for TERM (`SendMousePos` 3537-3577).
- **`logic.yaml` (MEDIUM ×2):** (a) `'DATA' 4` mislabeled "multi-bit bus" — a `count` without `RANGE` = 4 **single-bit**
  channels (ToO §7.2). (b) TRIGGER formula `(sample AND mask)==match` → `((sample XOR match) AND mask)==0` (only equivalent
  when `match ⊆ mask`).
- **`bitmap.yaml` (MEDIUM + LOW):** SPARSE "grid-border color" → background-**block** model + add the `DOTSIZE ≥ 4` sparse
  gate (manual carries it at ch04:400; yaml lacks it); add "LUT entries are black `$000000` (zero-init) until `LUTCOLORS`."
  *(The exact SPARSE user-facing word is a hardware-hold — see COVERAGE report §4.)*
- **`term.yaml` (MEDIUM):** control-code note "12 is in the 14..31 range" is arithmetically false (12 < 14); the *behavior*
  it asserts is right. Reword: "codes 0-10 and 13 act; 11, 12, and 14-31 do nothing." (Manual ch03 is clean.)
- **TITLE default (systemic, LOW-MEDIUM):** `scope.yaml`, `scope_xy.yaml` (`'Scope_XY'`), `term.yaml`, `midi.yaml` (`'MIDI'`)
  record the TITLE default as a bare type/name; the real default caption is `"<name> - <TYPE>"` (`FormCreate:626`).
- **DO NOT TOUCH (verified correct — prior-pass would have regressed these):** `scope.yaml` "prevents the window from being
  created" (EF-003 confirms it — the *manual* ch07:88-91 is the one to fix); `logic.yaml`/`term.yaml` POS "don't overlap"
  (hardware-hold vs the REF's "overlap" — needs a multi-window capture, do not mechanically flip); `bitmap.yaml`/`ch10`
  packing "unsigned by default" (correct — the **SPECTRO ToO** carries the stale sign mislabel, not the YAML).

**ADDENDUM 2026-07-14 — surfaced by the systematic v55 ↔ REF diff** (`…/audit/v55-vs-REF-systematic-2026-07-13.md`;
the first pass to walk the v55 reference *directive by directive* rather than chasing a conflict list):

- **`scope.yaml` L39 + `scope_xy.yaml` L43 (HIGH — NEW):** both ship *"(12 modes; default **LONGS_1BIT**)"*. **There is no
  packing default — the default is UNPACKED** (one 32-bit sample per fed long). The `LONGS_1BIT` claim is **unsourced**: the
  matrix's `SetDefaults` transcription (2880-2917) has **no packing row**; SCOPE_XY ToO L2083 quotes the init as
  `SetPack(0, False, False)`; and the REF's own `SetPack` transcription gives `val = 0` ⇒ shift 32, count 1, mask
  `$FFFFFFFF`. LOGIC ToO §6.4 (L627-631) says exactly this — three sections after its own table says the opposite.
  **Silicon confirms:** `ch06-logic-spi-bus.spin2` declares no pack mode, feeds one plain long per `debug()`, and renders a
  coherent 3-channel SPI trace — impossible if one long exploded into 32 one-bit samples. `logic.yaml` is **clean** (makes no
  default claim). *Same defect exists in the LOGIC/SCOPE/SCOPE_XY ToO directive tables → REF cleanup rail.*
- **Confirms `fft.yaml` MAG (above), independently** — the gain reading is closed by arithmetic on the REF's own quoted
  power formula (`shl`/`shr` are equal-precedence, left-to-right: raising MAG *shrinks* the divisor). No further evidence
  needed.
- **Manual-side surface the YAMLs do NOT need to carry, recorded so it is not lost:** the REF is a *host-side* Pascal
  distillation and is **silent on the P2-side API** — `PC_MOUSE`'s **7-long chip structure** (the REF documents only the
  2-long wire format), the "must be the last command in the DEBUG() statement" rule, hub-vs-cog pointer rules, and the
  `DEBUG_PIN_TX=62`/`DEBUG_PIN_RX=63`/`DEBUG_MASK`/`DEBUG_END_SESSION` gating layer. These are **manual** work
  (`document-finalize`), not KB YAML edits.

> **GATE (Stephen, 2026-07-14):** do **not** drain any of this piecemeal. The REF-authoring agent is cleaning the
> matrix/ToO internal contradictions first (handoff: `engineering/planning/REF audit v55 vs. theops/REF-CLEANUP-HANDOFF-2026-07-14.md`).
> When it returns, we re-run the systematic v55 ↔ REF diff against the cleaned REF, then apply **one** coordinated sweep —
> manual + examples ZIP + all debug-displays YAMLs — and re-release together. One bump, one moment.

> **REF-doc defects are NOT in this finding.** The re-audit also found ~15 places the ratified **matrix/ToO** contradict the
> correct manual/YAML (TEXTSTYLE/EF-031, trigger-offset inversions, MAG-divisor, color-mode enum order, SPECTRO sign-label,
> CLOSE §6 dropped clause, etc.). Those are REF corrections (Stephen-adjudicated), catalogued in the COVERAGE report §3 — not
> KB YAML edits, so they stay out of this register.

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

### F-193 — IOSP ch05 falsely claims no single instruction waits on event+timeout; teaches a busy-poll — `DONE (🏆 HW-PROVEN EF-020) — all phases RELEASED`
> **STATUS CORRECTED 2026-07-05:** the "releases pending" note below is stale — all phases shipped.
> **Phase-1 YAML** (`no_setq_behavior:` on all 15 wait YAMLs) shipped in **KB v1.14.0** (verified: the
> field is present in the `v1.14.0` tag). **Phase-2 doc patches** shipped in **IOSP v1.0.1** and
> **PASM2 v3.1.2** (commit `b76a9fed` phase-2 source → releases `a6fcbc5c` / `0dd7159a`). Nothing
> outstanding.
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

## IOSP reader question — P_STATE_TICKS "bit 31 = state" (2026-07-05) — F-194 `RESOLVED-INVALID`

### F-194 — `p2kbArchSmartPin10000TimeAStates` RDPIN-bit-31 example — `RESOLVED-INVALID` (not a defect)
**The reported defect does not exist.** An IOSP reader (on FlexSpin) asked whether bit 31 of
`RDPIN()` really carries the P_STATE_TICKS previous state. My first pass wrongly concluded the
manual + this YAML example were broken (that Spin2 `RDPIN()` drops C and bit 31 is only the
saturation MSB) and filed a "class defect" with an IOSP Ch04 "taproot." **Stephen sent me to the
Spin2 v55 reference, which overturns it:**
> Spin2 v55 lines 543–544: *"`RDPIN (Pin) : Zval` — … **`Zval[31] = C flag from RDPIN`, other
> bits are RDPIN data.**"* (same for `RQPIN()`.)
So the Spin2 built-in **does** fold the modal C flag into bit 31 of its return value — the
exact opposite of what I claimed. `if rdpin(pwm_pin) & $80000000  ' Check C flag in bit 31` is
**correct**, and `& $7FFF_FFFF` correctly strips that bit to leave the count. **No YAML edit.**
**Root cause of my error:** I checked the PASM2 `RDPIN` *instruction* (C via `WC` only) and
assumed the Spin2 `RDPIN()` *method* matched; it doesn't — the method marshals C into the MSB.
Lesson for Spin2-built-in findings: check the **Spin2 method table**, not just the PASM2
instruction. **Whole chain withdrawn** — no "class," no Ch04 taproot, no IOSP v1.0.1 needed; the
manual (Ch04 §4.12 + Ch13) is correct against v55. **The reader's real issue is a FlexSpin/PNut
compiler discrepancy** (FlexSpin's `RDPIN()` apparently returns raw Z without C in bit 31) — a
third-party compiler behavior, not a P2KB defect; portable inline-PASM (`rdpin…wc`+`wrc`)
workaround given. Full trail in
`manuals/p2-io-and-smart-pins-user-guide/audit/reader-question-p_state_ticks-bit31-2026-07-05.md`.
(Note F-175 stays valid on its own terms — that was a real `PINREAD` single-pin mask bug, a
different construct from `RDPIN()`.)

### F-195 — `p2kbArchSmartPin10000TimeAStates` "PWM Signal Analysis" example reads `rdpin()` multiple times per loop — `DONE (2026-07-05)`
> **APPLIED (yaml head) 2026-07-05 (ships v1.14.1):** in
> `architecture/smart-pins/smart-pin-10000-time-a-states.yaml` (Spin2 example, ~line 50) replaced the
> three-`rdpin()`-per-iteration pattern with a single `duration := rdpin(pwm_pin)` read, then
> `if duration & $80000000` / `& $7FFFFFFF` on that one capture. Bit-31=C and the count now come from
> one atomic read. Compile-verified `pnut-ts -d` v1.55.0 (standalone Spin2 PUB). YAML-format + crossref
> validators clean (no cross-ref change — code-example-only edit). The file's PASM2 block already read
> once (`rdpin duration,#pwm_pin wc`) — left untouched. **Manual twin** (IOSP Ch13 `analyze_pwm` +
> `pwm_analyzer`) fixed separately for IOSP v1.0.2.
**Distinct from F-194 (which was invalid); this one is real.** The example tests the C flag with
one `rdpin(pwm_pin)` call, then reads `rdpin(pwm_pin)` **again** to store the duration:
```
if rdpin(pwm_pin) & $80000000          ' read #1 — acknowledges the pin
  high_time := rdpin(pwm_pin) & $7FFFFFFF   ' read #2 — a SEPARATE capture
```
Each `rdpin()` acknowledges the smart pin. Bit 31 (C) and the count belong to a *single* capture,
but the code tests one read and stores another. **Latent bug:** if a transition lands between the
two reads (fast signals / glitches), read #2 is the next state's data while the C test was on the
previous one → wrong duration, or a high/low mix-up. Invisible on slow PWM (Z unchanged between
back-to-back reads), which is why it wasn't caught. **Independently flagged 2026-07-05 by the
pnut_ts-side agent** during the same investigation. **Fix:** read once into a variable, then
test/mask that variable (the `%10000` state example one section up in the same YAML already does
this correctly):
```
x := rdpin(pwm_pin)
if x & $80000000
  high_time := x & $7FFFFFFF
else
  low_time  := x & $7FFFFFFF
```
**Manual twin (IOSP, live):** the *same* double-read appears in Ch13 `analyze_pwm()` (lines
130–133) and `pwm_analyzer()` (lines 457–461). The reader's `measure_states()` example (line 80)
reads once and is **correct**. This is a narrow, genuine IOSP fix (candidate for a bundled
v1.0.1) — separate from the withdrawn bit-31 claim. Verify each site before editing.

---

## Family C app-note authoring sweep (2026-07-06) — F-196…F-200

> Surfaced while source-mining for the Family C app notes (P2AN005 Multitasking /
> P2AN006 Stack Sizing / P2AN007 Data Structures). **ALL RESOLVED — `DONE` 2026-07-06**
> in the yaml-head pass after the drafts were staged for PDF review (was deferred per
> Stephen's sequencing call; F-198 hardware-verified → EF-023). The
> notes are authored *correctly against P2* regardless — they exclude/route around
> every defect below. Authority: `pnut_ts` v1.55.0 + the Spin2 v55 keyword table
> (`engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt:39,149`).

### F-196 — `methods/taskwait.yaml` documents `TASKWAIT`, which does not exist in Spin2 — `DONE (2026-07-06)`
> **APPLIED 2026-07-06 (policy: no fabricated names in the tree — Stephen's call).** Deleted
> `methods/taskwait.yaml` AND `methods/taskresume.yaml` outright (no invalid-keyword stubs, no
> aliases) — fake names now resolve to nothing; agents recover via `p2kb_find` on `task*`. Redirected
> the inbound refs: `tasknext.yaml related:` dropped `TASKWAIT` and upgraded to full-path valid
> siblings; `taskcont.yaml` dropped its `TASKRESUME` alias + note. Added a POSITIVE wait-idiom note to
> `tasknext.yaml` (`repeat until <cond>` + `TASKNEXT()`) so the use-case is answered via a real method.
> Source: v55 keyword table (TASKWAIT/TASKRESUME absent, `spin2-v55-text.txt:149`) + pnut_ts v1.55.0 probe.
`TASKWAIT` is **absent from the v55 keyword table** (`spin2-v55-text.txt:149` lists exactly
TASKSPIN/TASKNEXT/TASKSTOP/TASKHALT/TASKCONT/TASKCHK/TASKID/NEWTASK/THISTASK/TASKHLT — no
TASKWAIT). **Compile-probe (pnut_ts v1.55.0, `-d`):** `TASKWAIT(ready == 1)` →
`error: Expected an instruction or variable` — **does not compile**. The YAML also (a) gives a
signature `TASKWAIT(Condition)` matching neither the v51 mentions (which describe a `TASKWAIT(ticks)`
tick-count wait), (b) **lacks the `{Spin2_v47}` version gate** every sibling carries, and (c) carries a
forbidden interpreter `cycles:` timing field. **Proposed correction (deferred):** convert `taskwait.yaml`
to an invalid-keyword stub in the shape of `taskresume.yaml` (which already does this for the invalid
`TASKRESUME`), and remove the `TASKWAIT` back-references in `tasknext.yaml related:`. **Authoring:**
`TASKWAIT` is excluded from P2AN005.

### F-197 — `methods/taskspin.yaml` `returns: void` omits the expression-return form — `DONE (2026-07-06)`
> **APPLIED 2026-07-06.** `taskspin.yaml` `returns:` now documents both forms: as a statement it
> returns nothing; as an expression term it returns the assigned task number (0-31) or -1 if no slot
> was free. `related:` upgraded to full paths. Source: v55 v47 change note (`spin2-v55-text.txt:39`).
v55 (`spin2-v55-text.txt:39`) and a compile-probe confirm `TASKSPIN(...)` used as an expression
**returns the assigned task number, or −1 if no slot was free**. The YAML declares `returns: type: void`,
which is incomplete. **Proposed correction (deferred):** document the integer expression-return (task # /
−1) alongside the statement form.

### F-198 — `methods/taskid.yaml` + `registers/taskhlt.yaml` assert "main task is typically ID 0" unsourced — `DONE (2026-07-06, hardware-verified 🏆 EF-023)`
> **HARDWARE-VERIFIED 2026-07-06 (🏆 EF-023).** Stephen ran `f198-tasks-per-cog-probe.spin2` on real P2
> silicon: two cogs, each spinning two tasks, all reporting `COGID()`/`TASKID()`. **Both cogs** showed
> top-level = TASKID 0, spawned tasks = 1 and 2 (each task's id matched `TASKSPIN`'s return). So the
> claim is CONFIRMED but **sharpened**: not a single global "main = 0" — rather, *in each cog the
> top-level code runs as that cog's task 0, and task IDs are cog-local*. Kept + reworded (dropped the
> vague "typically") in `taskid.yaml` + `taskhlt.yaml`, both citing EF-023. Verification turned a
> remove-the-unsourced-claim into a keep-and-strengthen (empirical outranks documentary silence).
Both files state the main/host task is (typically) ID 0; the v55 keyword table does not state this. Reads
as inference. **Proposed correction (deferred):** verify on hardware (Stephen) or soften/remove the claim.
P2AN005 does not rely on any fixed main-task ID.

### F-199 — `patterns/implementation/spin2_shared_memory.yaml` uses P1 `lockset()`/`lockclr()` — `DONE (2026-07-06)`
> **APPLIED 2026-07-06.** Rewrote the pattern to the real P2 lock idiom: `LOCKNEW()` to allocate,
> `repeat until LOCKTRY(id)` to acquire, `LOCKREL(id)` to release (added the missing `start()`/`LOCKNEW`
> allocation the P1 original lacked). Compile-verified under pnut_ts v1.55.0. Source: v55 (P2 has
> LOCKNEW/LOCKTRY/LOCKREL/LOCKRET/LOCKCHK; `lockset`/`lockclr` absent). Evidence-scoping: the only other
> lockset/lockclr hit, `p2an007` companion, is a *correct warning* ("do NOT use the P1 form") — left as-is.
Lines ~12/14/17 use `lockset()`/`lockclr()`, which are **Propeller 1** methods and **do not exist in P2
Spin2** (P2 uses `LOCKTRY`/`LOCKREL` with `LOCKNEW`/`LOCKRET`/`LOCKCHK`) — the pattern would fail to compile
under `pnut_ts`. **Proposed correction (deferred):** rewrite to the P2 `LOCKTRY`/`LOCKREL` idiom (spin-acquire
`repeat until locktry(id)`, release on all paths). **Authoring:** P2AN007 codes the real P2 locks and never
cites the P1 form.

### F-200 — `patterns/implementation/spin2_event_dispatcher.yaml` is SPSC-only but unscoped — `DONE (2026-07-06)`
> **APPLIED 2026-07-06.** Added a `constraints:` note stating the queue is correct only single-producer/
> single-consumer (the `queue_head` advance is unguarded and races under multiple producers), and pointing
> multi-writer use at a lock-guarded queue (`spin2_shared_memory.yaml`, full path). Source: code analysis.
The `post_event` queue is correct only single-producer/single-consumer; used multi-producer it races (no lock
on the head advance), and the file does not state the constraint. **Proposed correction (deferred):** add the
SPSC scope note (and point multi-writer use at a lock-guarded queue). **Authoring:** P2AN007's R4 shows the
lock-guarded multi-writer form explicitly.

---

## ADC "ENOB" misuse — nominal decimation width printed as measured effective resolution (2026-07-06) — F-201

### F-201 — Silicon-Doc-inherited ENOB misuse in the SINC ADC resolution tables — `DONE (2026-07-06)`
> **CONFIRMED (definitional + primary-authority).** The P2 Silicon Doc labels the SINC filter columns
> "Post-diff ENOB" and its footnote defines *"ENOB = Effective Number of Bits, **or the sample
> resolution**"* — conflating the two. By definition (IEEE Std 1241) ENOB is the **measured** effective
> resolution derived from SINAD; the table values are **nominal decimation word-widths**, not ENOB. The
> P2 designer **Chip Gracey** has conceded this on record (P2AN001 research thread): *"I never did find
> out how you computed the ENOB in the Silicon Doc"* and *"optimistic doubling of ENOB would only be if
> we had a second-order analog modulator. Need to change the docs."* Community feedback (Christof Eb.,
> 2026-07-06) independently flagged *"ENOB=18 is total nonsense."*
> **APPLIED 2026-07-06** — relabeled the ENOB cells → nominal "bits" and added the nominal-vs-measured
> caveat plus the "SINC3 doubling is not achieved on P2" caveat in:
> - `deliverables/ai/P2/architecture/smart-pins/smart-pin-11001-adc-external-clock.yaml` (`sinc3_filtering` values + two `notes`) — YAML parse + crossref 100% clean.
> - IOSP User Guide opus-master: §16.3 Resolution/Sample-Rate table + footnote + the "Beyond 14 bits" caveat, and Appendix D mode-comparison chart. (Ships in **IOSP v1.0.3**.)
> **No effective-resolution number is printed** (none is characterized — consistent with the
> P2AN001/P2AN003 defer-ENOB stance and **G-003**). The appendix glossary line ("ENOB — Effective number
> of bits") is a correct definition and was kept. Full analysis: the ADC/ENOB community-feedback capture
> (`engineering/operations/questions/adc-enob-community-feedback-2026-07-06.md`). Green Book (retired) intentionally not touched.

---

## ADC gain-mode input ranges framed ground-referenced, not centered on VIO/2 (2026-07-07) — F-202

### F-202 — IOSP §16.2 ADC input-mode table (and 5 propagated sites) frame the gain ranges as ground-referenced `0V–ceiling` — `PARTIALLY CONFIRMED: GIO/VIO-as-calibration + mid-supply bias grounded in Silicon Doc; exact centered endpoints UNVERIFIED (no trusted numeric source) → hardware campaign required`
> **Source of report:** community reviewer (2026-07-07, relayed by Stephen): *"the ranges are totally
> wrong… they are centred around 1.65V."* Community-tier input (Titus-tier): challenges our work, is not
> itself a citable source.
> **TRUST-CHAIN DISCIPLINE (Stephen, 2026-07-07):** the **P2AN\*** app notes are derived from the SAME
> ingested sources as the manuals — a **peer derivation, NOT an authority**. Do not justify manual content
> against P2AN001/§16.3; ground only against trusted **ingested** sources (Silicon Doc) or **empirical**
> hardware (EF ledger). This finding was re-grounded on that basis.
> **What the Silicon Doc (trusted ingested) DOES ground:**
> - **GIO/VIO are calibration sources, not input-range modes** — *"Delta-sigma ADC with 5 ranges, 2
>   **sources**, and **VIO/GIO calibration**."* The §16.2 table mislabels them as ranges (`GIO = 0V–3.3V`,
>   `VIO = VIO-relative`). WRONG per a trusted source.
> - **The ADC has a ~mid-supply bias point** — Rev C note: FLOAT mode "useful for determining the
>   **floating bias point of the ADC**." So the gain window sits around mid-supply, **not up from 0 V** —
>   the table's ground-referenced framing is wrong.
> - Tell-tale of how it happened: the table's ceilings (`1.04V / 330mV / 104mV / 33mV`) equal `3.3V ÷ gain`
>   — correct range **widths** placed at `[0, width]` (generic unipolar-PGA assumption) instead of around
>   the mid-supply bias. (§16.7 L469 and §16.3 already describe the bias/references correctly — but those
>   are peer manual sections, cited here only as internal-inconsistency evidence, not as authority.)
> **RESOLUTION — nominal transfer characteristic (releasable-correct without hardware):**
> The exact endpoints are a **nominal / definitional** quantity, not a measured one: the mid-supply
> reference is grounded (Silicon Doc float-bias-point) and the gain factors are grounded (Silicon Doc
> "5 ranges" + image catalog), so the window `= 1.65 V ± (1.65 V / gain)` about mid-supply is **DERIVED**
> (like the Ohm's-law drive currents and `clkfreq/2³²` NCO resolution we already print), NOT AT_RISK —
> **provided it is labelled *nominal* and carries the calibration caveat** (exact endpoints vary with device
> tolerance + VIO; for absolute work calibrate against GIO/VIO, §16.3). This mirrors the manual's already-correct
> nominal-vs-measured handling of resolution ([[F-201]]). This is the distinction I initially over-collapsed:
> a *measured precision spec* needs silicon; the *nominal transfer characteristic* does not. So §16.2 prints the
> nominal windows (labelled) — correct, complete, hardware-independent.
> **Verification split (per VERIFICATION-OPPORTUNITIES.md):**
> - **VO-J-001 (jumper-only — we do it):** on-chip DAC → jumper → ADC pin sweep confirms the centering + √10
>   window scaling on silicon (upgrades nominal → silicon-confirmed). Task #172. NOT a release blocker.
> - **VO-X-001 (external-hardware — cataloged, not committed):** calibrated external reference + precision meter
>   for tolerance-bounded absolute endpoints. Benefit: nominal → datasheet-grade. Deferred.
> **Propagated sites (all same root), IOSP opus-master `part-3-input-modes/chapter-16-adc.md` unless noted:**
> §16.2 table (L39–46) · §16.2 prose (L50–60) · §16.2 example "0-100mV sensor → 30x" (L64–66) ·
> §16.7 Example 4 thermocouple "0-50mV → 100x" (L505–517) · §16.7 quick-ref table (L636–640) ·
> `part-5-appendices/appendix-d-mode-comparison-charts.md` (L195–198). The **examples are the worst**:
> they feed a ground-referenced small-signal sensor (0-100 mV, 0-50 mV thermocouple, mic, strain gauge)
> into a 1.65 V-centered gain mode with **no mid-rail bias network** — they would not work as written.
> **NOT affected (checked, don't over-correct):** §16.3 ratiometric (correct) · §16.7 float note L469
> (correct) · **DAC ranges ch10** `0–3.3V`/`0–2.0V` (correct — DAC is genuinely unipolar 0-to-Vfs,
> matches Silicon Doc drive-level table). Defect is **specific to ADC gain modes**.
> **Secondary check:** `architecture/smart-pins/smart-pin-11000-adc-internal-clock.yaml` L144–145 calls
> GIO/VIO "Ground-referenced input / VIO-referenced input" — loose (they're calibration references);
> tighten wording, and confirm no range claim depends on the ground-referenced framing.
> **SILICON-CONFIRMED 2026-07-07 (EF-024) — supersedes the nominal formula.** VO-J-001 ran on real P2:
> gain modes ARE centered on mid-supply (~1.64 V measured) [structural, definitive], but the **derived
> `1.65 ± 1.65/gain` (3.3 V/gain width) was WRONG** — measured widths are ~1.4× wider (≈4.55 V/gain), √10-laddered.
> Measured representative windows (N=1): 3.16× 0.93–2.36 V · 10× 1.41–1.87 V · 31.6× 1.57–1.71 V · 100× 1.61–1.66 V.
> **Fold into IOSP v1.0.4** (staged): (a) GIO/VIO reclassified [APPLIED]; (b) mid-supply framing + examples
> fixed [APPLIED]; (c) **print the MEASURED windows** (table above) across §16.2 + Appendix B + Appendix C,
> labelled *measured on real P2 silicon, representative single-sample* (per the citation convention), NOT the
> derived formula; rebuild the two examples on the measured centering [PENDING apply]. With (c), F-202 is
> **CLOSED for release** and now hardware-grounded (not merely derived). VO-X-001 (absolute tolerance across
> parts) remains the optional datasheet-grade upgrade.

---

## Quantitative hardware-table audit batch (2026-07-07) — F-203

### F-203 — 4-manual fan-out audit of quantitative hardware tables vs trusted ingested sources — `14 CONFIRMED_WRONG (hand-verified) + 8 AT_RISK; fixes in progress`
> **Method:** 9-unit fan-out (IOSP ×5 parts, Streamer, Debug ×2, deSilva) enumerating every quantitative/encoding
> table cell, each classified GROUNDED/DERIVED/AT_RISK/WRONG against **ingested sources only** (Silicon Doc,
> Spin2 v55, P2 datasheet), then adversarially verified. Full verdicts: workflow `wx8vrj00a` output. 1 false
> alarm rejected on hand-verify (ch06 "30mA" — actually GROUNDED, spin2-v55:1502).
>
> **CONFIRMED_WRONG — IOSP (fold into v1.0.4):**
> - `ch02` `P_HIGH_FAST`/`P_LOW_FAST` drive impedance **`~100Ω` → `~17Ω`** (datasheet Vol 510mV@30mA ⇒ ~17Ω; 30mA is correct). **FIXED.**
> - `ch18` §18.6 Hub RAM **`8-15 clocks` → `9-16 clocks`** (datasheet RDLONG `9...16`). **FIXED.**
> - `appendix-b` + `appendix-c` (table **and** the `input_max = 3300mV/gain` formula) — **F-202 ADC-range recurrence** (2 more sites; ground-referenced `0-Xmv`). PENDING (rides the F-202 nominal-table fix across §16.2 + both appendices).
>
> **CONFIRMED_WRONG — deSilva (fold into v3.0.2):**
> - SETSE Event-Modes `%000` **"Never (disabled)" → "LUT read/write & hub-lock events"** (silicon-doc part3-interrupts:48-53). **FIXED.**
> - `EVENT_INT %0000` **"Pin matches interrupt configuration" → "An interrupt occurred"** (part2-video-output:360; pin-match is `EVENT_PAT %1000`). **FIXED.**
> - `EVENT_QMT %1111` **"CORDIC/PIX math complete" → "read with no CORDIC result available"** (part2-video-output:375 — the inverse meaning). **FIXED.**
>
> **CONFIRMED_WRONG — Streamer (needs own patch, NOT in current wave):**
> - §12.2 Sub-Pin Selection table treats `D[19:17]` as a uniform 3-bit selector for 1/2/4-pin; silicon encodes `pppa/pp?a/p??a` (pin-bits shrink 3/2/1; freed low bits = DAC sub-mode). 1-pin col correct; 2/4-pin cols wrong. (p2-documentation:3004-3009).
>
> **CONFIRMED_WRONG — Debug (needs own patch, NOT in current wave):**
> - `ch05` PLOT TEXTSTYLE **horizontal align 2/3 swapped** (source %10=right, %11=left) and **vertical align 2/3 swapped** (%10=bottom, %11=top) — spin2-v55:1282; plus downstream prose **"`$20` left-aligns" → right-aligns**.
> - `ch03` TERM **`TEXTSIZE` default `10` → "editor text size"** (spin2-v55:1305; the 10 is the PLOT default).
>
> **AT_RISK (unsourced specifics — disposition per finding):** IOSP `ch16` §16.8 ADC "input impedance ~500kΩ" + "absolute-error floor ~15mV" (from P2AN001, not in EF ledger — **jumper-only verifiable, VO-J candidate**); `ch10` DAC "Max Load >10kΩ…" (10× rule-of-thumb heuristic); `ch12` "input buffer ~2ns" (sub-component; 3-clk total IS grounded); `ch07` "180MHz rated / 250 overclock" (only 350 grounded; 180 cites external datasheet); Debug `ch05` weight "100/400/700/900" (OpenType nums unsourced; "thin"→"light"); Debug `ch14` "LOCK[15]" + "~10,000 msg/s" (tool/throughput, ungrounded). Disposition: remove the unsourced number or soften to qualitative; the ~15mV/~500kΩ ADC pair → VO-J jumper test.

## Fabrication-audit fan-out — YAML-wrong finding (2026-07-10, task #177) — F-204

### F-204 — `rdpin.yaml` RDPIN IN-flag-reset snippet shows **two** NOPs for a **2-clock** delay (one NOP = 2 clocks, so it over-waits) — `DONE 2026-07-11` (fleet-release §3b/#179; was GROUNDED → NEEDS-VERIFICATION)
> **Applied 2026-07-11 (#179):** `rdpin.yaml` `in_flag_reset_latency` snippet corrected — second NOP removed (one NOP = 2 clocks already covers the full 2-clock IN-flag reset), and the wrong per-NOP `Clock 1`/`Clock 2` labels replaced with a single `' 2 clocks: covers the IN-flag reset delay` comment; prose changed from "Insert NOP instructions" to "one NOP is 2 clocks … insert one NOP." Source trace: IOSP §4.13 (line 542, doc already correct) + v35 Instructions CSV (NOP = 2 clocks) + hardware-confirmed mechanism EF-015 (`test50-eventtiming-rdpin-restart`). IOSP doc text was already correct → no manual edit. Only `rdpin.yaml` was defective (evidence-scoped to the one file named in the finding).
- **Location:** `deliverables/ai/P2/language/pasm2/rdpin.yaml` — `p2kbPasm2Rdpin.in_flag_reset_latency` (snippet: `RDPIN result,#pin / NOP  Clock 1 for IN flag reset / NOP  Clock 2 for IN flag reset / TESTP #pin WC`).
- **What's wrong:** the snippet labels **each NOP as one clock** ("Clock 1", "Clock 2") and uses **two** NOPs to cover the 2-clock IN-flag reset. A `NOP` is **2 clocks** (v35 CSV NOP row), so a single NOP already elapses the full 2-clock acknowledge/reset delay; two NOPs wait **4 clocks** and the per-NOP "Clock N" labels are wrong.
- **Evidence:** v35 Instructions CSV — `NOP` = 2 clocks. IOSP User Guide §4.13 (line 542) states this correctly: *"One NOP waits 2 clocks (NOP = 2 clocks) to satisfy the 2-clock acknowledge delay"* — doc is right, YAML is wrong. Surfaced by the fabrication-audit fan-out (IOSP batch); adversarial-verifier confirmed doc-correct / YAML-wrong. Detail: `manuals/p2-io-and-smart-pins-user-guide/audit/fanout-findings-2026-07-10.md`.
- **Grounding (closed 2026-07-10):** the fix is fully grounded without a new run — (1) IOSP §4.13 states it correctly ("one NOP waits 2 clocks to satisfy the 2-clock acknowledge delay"); (2) v35 CSV: NOP = 2 clocks; (3) the RDPIN acknowledge/reset **mechanism is hardware-confirmed** — **EF-015** (`test50-eventtiming-rdpin-restart`, 2026-06-17: RDPIN acknowledge auto-restarts the measurement; two successive measurements arrived clean). The earlier "verify the exact 2-clock latency first" caution is satisfied by (1)+(2) documentary + (3) the confirmed mechanism. **What remains is only the YAML edit** (one NOP, corrected label), on the §9 YAML/KB track.
- **Proposed correction:** replace the two-NOP snippet with one NOP (`RDPIN result,#pin / NOP  '2 clocks: IN-flag reset delay / TESTP #pin WC`), or annotate that the single NOP covers the full 2-clock reset — matching the IOSP guide's wording. Verify RDPIN IN-flag reset latency first.

## SOURCE CONFLICT — v55 text vs REF (PNut source distillation) on PLOT TEXTSTYLE justification (2026-07-10) — F-205

### F-205 — PLOT `TEXTSTYLE` horizontal/vertical justification value mapping is **inverted** between the Spin2 v55 text and the debug-window REF theory-of-operations — `RESOLVED 2026-07-11 by hardware Test I (EF-031) + Test D (EF-028); manual corrected (#195)`

> **RESOLVED 2026-07-11 (hardware).** The v55-vs-REF standoff was settled on real
> P2 silicon, and the answer is a **per-axis HYBRID** — neither source was wholly
> right:
> - **Horizontal:** `%10`=right, `%11`=left — **v55 text correct**, REF §4.3 inverts.
> - **Vertical:** `%10`=top, `%11`=bottom — **REF correct** (matches Pascal
>   `2:ty:=h //top; 3:ty:=0 //bottom`), v55 text inverts.
>
> Grounded in **EF-031** (`conflict-testI-textstyle-justify`, centroid analysis,
> both macOS + Windows). The companion weight question is **EF-028** (Test D):
> the weight field (bits 0–1) is a correct *nominal* selector but the DEBUG font
> does **not** render the four weights distinctly (`$00`==`$01`) — so **F-205a**
> (the manual's "`$00` = light, lighter than `$01`" claim) is **REFUTED**.
>
> **Applied to the manual (#195, 2026-07-11):** `ch05-plot.md` TEXTSTYLE table now
> reads horizontal `2=right/3=left` (unchanged — was already correct), **vertical
> `2=top/3=bottom` (corrected from `2=bottom/3=top`)**, weight `0=thin` + a render
> caveat that the font does not visibly distinguish the four weights.
> **YAML side APPLIED 2026-07-11** (pending KB publish): `plot.yaml:67` TEXTSTYLE now
> carries the per-axis mapping (horiz `%10`=right/`%11`=left; vert `%10`=top/`%11`=bottom)
> + the weight render caveat (`$00`==`$01`; `$02`/`$03` not visibly heavier).
- **Location:** PLOT `TEXTSTYLE` byte `%YYXXUIWW` — the `%XX` (horizontal) and `%YY` (vertical) value→direction mapping. Affects `manuals/p2-debug-window-manual/opus-master/ch05-plot.md` (TEXTSTYLE table), `deliverables/ai/P2/language/spin2/debug-displays/plot.yaml` (currently states only the **bit positions**, silent on the value mapping), and any doc asserting which of `%10`/`%11` is left/right/top/bottom.
- **The conflict (verbatim, both primary sources):**
  - **Spin2 v55 text L1282:** *"%YY vertical: %00=middle, **%10=bottom, %11=top**. %XX horizontal: %00=middle, **%10=right, %11=left**."* → 2=right/bottom, 3=left/top.
  - **REF `PLOT_Theory_of_Operations.md` §4.3** (distilled from PNut `DebugDisplayUnit.pas`): *"Horizontal (bits 4-5): 0/1=center, **2=left, 3=right**. Vertical (bits 6-7): 0/1=center, **2=top, 3=bottom**."* → 2=left/top, 3=right/bottom.
  - The **bit layout agrees** (vert = high pair, horiz = next pair, U, I, weight = low pair). Only the **value→direction mapping is exactly inverted** on BOTH axes.
- **Why NEEDS-VERIFICATION (winner NOT determined):** v55 text is Parallax's official Spin2 reference (Chip Gracey); REF is an **agent's distillation** of `DebugDisplayUnit.pas`, which could itself have inverted the reading. Our ground-truth rule (PNut source is authoritative; `reference_pnut_is_ground_truth_termts_mirrors`) would favor REF — **but REF is not the raw source**, so this direct contradiction must be settled against the **raw `DebugDisplayUnit.pas`** or a **hardware test** (render text with `TEXTSTYLE %00100000` and observe left-vs-right) before either the manual or the YAML is edited.
- **Blocks:** the previously-noted "ch05 PLOT TEXTSTYLE horiz+vert align 2/3 SWAPPED" manual correction (which would have aligned the manual to v55 text) is **ON HOLD** — applying it now risks contradicting PNut source and flip-flopping on the next PNut-grounded audit.
- **Related open candidate (same v55-vs-REF axis, softer):** PLOT `TEXTSIZE` default — REF §4.3 says `DefaultTextSize = 10` (a PNut constant); v55 instantiation tables say default = "editor text size." May be layering (hardcoded fallback vs tool-supplied runtime default) rather than a hard contradiction — reconcile against REF/raw Pascal too.
- **Origin:** surfaced 2026-07-10 while checking whether the debug REF folder addresses the example-ZIP customer feedback + broader fabrication audit; REF is upstream of the debug YAMLs (they cite `DEBUG-WINDOW-DIRECTIVE-MATRIX.md` as `documentation_source`). Recommend a **systematic v55-text-vs-REF reconciliation pass** for the debug windows before applying any broader debug fabrication-audit finding.

---

## P2AN007 R3 — dropping the seq/ack handshake invites the torn read the note exists to prevent (2026-07-13) — F-213

### F-213 — P2AN007 v0.1.0 R3 tells the reader the ack can be dropped; it cannot — `DONE (2026-07-13)` (doc-side; FIXED in v1.0.0, hardware-confirmed EF-038)

- **Location:** `engineering/document-production/app-notes/P2AN007/opus-master/P2AN007.md` — Recipe R3 (Latest-Wins Mailbox), the "How this works" closing sentence and the following Tip. Doc-side only; **no YAML is wrong** (`patterns/implementation/spin2_latest_wins_mailbox.yaml` does not make this claim).
- **What v0.1.0 said:** *"Here the writer waits for the ack before sending the next, which paces the two cogs; **drop that wait and the newest command always wins**."* The companion Tip further claimed the sequence-counter form *"never blocks the writer waiting for the reader"* — which is not true of the recipe as printed, since it does exactly that.
- **Why it is wrong:** R3's worker reads `cmd.opcode`, `cmd.arg0`, and `cmd.arg1` as **three separate reads of shared hub memory**. The seq/ack handshake is the only thing preventing the writer from overwriting `cmd` *while the worker is part-way through reading it*. Drop it and correctness comes to rest on a race — whether the worker's three reads complete before the writer's next write lands. **Stated precisely (sharpened 2026-07-13 after the VT2 run):** the hazard is not that a tear is certain, it is that safety becomes contingent on worker timing. A worker that does nothing but poll typically wins the race and looks fine (VT2 rev-1 measured exactly this: a tight-loop worker produced **zero** tears in 20,000 observations); a worker that does *anything* between reads — the near-universal `CASE cmd.opcode` dispatch before touching the arguments — loses it. R3 **as printed** is correct; the guidance to modify it is what is unsafe, and it is unsafe in the worst way, by appearing to work. This is a guidance defect, not a code defect.
- **Fix applied (v1.0.0, 2026-07-13):** the invitation is replaced by a ⚠ Pitfall stating the ack is load-bearing, plus the two honest non-blocking alternatives — pack the payload into a single long so the whole record publishes in one store (new recipe **R5**, member bitfields {Spin2_v54}), or have the reader re-check the sequence (read seq, copy, re-read seq, retry if it moved) so a straddling copy is discarded rather than used. The inaccurate "never blocks" Tip is corrected.
- **Empirical arm — CONFIRMED on silicon 2026-07-13 (→ EF-038).** `vt2-mailbox-publish-order.spin2`, final revision, two experiments each with its own matched control. **Exp-2 (the ack):** slow worker (25µs between reading the opcode and reading its args — the near-universal `CASE cmd.opcode` dispatch). Ack present = **0 bad in 20,000**; ack removed = **20,000 bad in 20,000** — *every single command torn*. The matched control (same slow worker, ack present, zero tears) isolates the ack as the cause rather than the injected delay. **Exp-1 (publish order):** fast worker; correct order = 0, seq-bumped-first = 20,000/20,000. **The trap, also measured:** a *tight polling* worker with no work between its reads wins the race against the writer and reports **zero** — so the missing ack **looks fine** under exactly the test most people would write. That is what makes the v0.1.0 advice dangerous rather than merely wrong.
- **Rig history (three inconclusive runs before it fired — worth carrying forward):** rev-1 (tight worker) and rev-2 (1µs gap) both reported zero and self-reported INCONCLUSIVE rather than a false pass; rev-3's 25µs gap fired arm C but *hid* arm B, because one worker cannot serve both claims (the bad-order window is the ~2µs between the seq bump and the fields landing). Rev-4 split them. Separately, VT3 exposed cog **phase-lock** — 14,976 anomalies on one run and 0 on the next from a logic-identical binary. Both lessons: `engineering/operations/lessons-learned/two-cog-race-rigs-must-be-structural.md`.
- **Origin:** surfaced 2026-07-13 while building the hardware-verification rigs for the P2AN007 v1.0.0 release — designing a rig for R3 required stating precisely what R3 guarantees, which exposed the guidance that contradicts it. A worked argument for *why* a rig is needed is itself an audit.

---

## Platform filter corrupts hyphenated names — `NOT-taken`, `p2-io-AND-smart-pins-user-guide` in a RELEASED manual (2026-07-13) — F-214

### F-214 — `p2kb-platform-mnemonic-bold.lua` uppercases a mnemonic inside a hyphenated compound token — `CONFIRMED` (filter FIXED; affected PDFs need re-render)

- **Location:** `engineering/document-production/platform/filters/p2kb-platform-mnemonic-bold.lua` — the `is_part_of_identifier` guard in `uppercase_mnemonics_in_line()`. **Shared platform filter → every manual that renders inline code is exposed.**
- **The defect:** the filter uppercases Spin2 mnemonics inside inline code spans (by design — uppercase carries mnemonic identity, policy 2026-06-29). Its guard skips a word that is *part of an identifier*, but only recognized `[%w_]` as connector characters — **not the hyphen**. So in a hyphenated compound token, a mnemonic-looking component sits between two hyphens, reads as standalone, and gets uppercased.
- **Confirmed in the SHIPPED `P2-Assembly-Language-Manual.pdf`** (text-extracted from the released PDF, not inferred): `NOT-taken` ×4 (should be `not-taken`), `1..4-BYTE` ×2 (should be `1..4-byte`), and **`p2-io-AND-smart-pins-user-guide`** — a corrupted *cross-reference to another manual's name*. Also latent in the XByte guide (in-dev) and it corrupted `single-long-packed-record.spin2` → `single-LONG-packed-record.spin2` in P2AN007's first v1.0.0 render, which is how it surfaced. **A corrupted filename is the worst case: it points the reader at a file that does not exist in the published ZIP.**
- **Fix applied 2026-07-13:** the guard now also treats a hyphen as an identifier connector **when it joins two alphanumeric runs** (a compound token). It requires the character *beyond* the hyphen to be alphanumeric, so genuine subtraction (`x - long`), a leading unary minus (`-long`), the standalone type keyword (`long[@ptr]`), and the pointer size-override (`ptrvar[++].long[5]` → `.LONG[5]`, which MUST still uppercase) are all untouched. Verified against an 11-case unit test of the guard logic (no Lua interpreter and no local pandoc in the container — Sacred Rule #4 — so the algorithm was mirrored and tested directly); ships with P2AN007's v1.0.0 bundle, which is the render that proves it end-to-end.
- **Outstanding — affected published docs need a re-render to pick up the fix (Stephen's release-timing call):** **P2 Assembly Language Manual** (7 corrupted renders, incl. the cross-manual reference) — a content-identical re-render + patch release. The XByte guide is in-dev (absorbs at its next build; no release owed). All other manuals: scan clean. **A doc is only fixed once it is RE-RENDERED — the filter fix does not retroactively touch a shipped PDF.**
- **Origin:** surfaced 2026-07-13 in the P2AN007 v1.0.0 render verification — the published PDF listed an example filename that does not exist. Class-wide sweep then found it pre-existing in a released manual.

---

## Shipped app-note PDFs contradict their own cover — in-doc Revision History goes stale on every release (2026-07-13; scope corrected 2026-07-14) — F-215

### F-216 — Debug Window Manual: SIX SHIP-BLOCKERS, three of them in SHIPPED, hardware-run example code — `DONE`

> **APPLIED 2026-07-14** (commits `a4f66ef0` ship-blockers, `7a2ae625` per-chapter + TEACH, `35166ad4` YAML).
> All six blockers fixed in `opus-master/` **and** in the example files, in lockstep. SB-1 (`+/`), SB-2 (explicit
> channel counts **+ the missing example file created**, `ch06-logic-declare.spin2` — closing the root cause: the
> construct had no compile-and-run coverage), SB-3 (LSB-first packing in both twins), SB-4 (`PRECISE` default),
> SB-5 (`COLOR` immediately before `TEXT`), SB-6 (SPECTRO axes in appendix-c). Examples ZIP regenerated.
> **Verified:** all 34 examples compile under `pnut-ts -d`, and all 34 are byte-identical to their manual code blocks.
> **NOT applied — the RIG-VERDICTS reversal:** the fix list's body called for reversing `ch04:241` to "SET is
> clamped." **EF-050 proved on silicon that `SET` is NOT clamped** — the shipped sentence is CORRECT, and applying
> the body would have broken correct text. The two other items resting on that same wrong REF reading (the ch05
> LAYER/CROP "clamped" rewrite and the ch01 global "everything clamps" TEACH) were likewise dropped.

**Surfaced:** 2026-07-14, the 5-agent 4-way reconciliation (v55 ↔ rebuilt REF ↔ manual ↔ YAML ↔ examples) run against the
REF re-grounded on raw `DebugDisplayUnit.pas` + `p2com.asm`. Every item hand-verified before acceptance.
**Full working list (gitignored workspace):** `…/p2-debug-window-manual/audit/SWEEP-FIX-LIST-2026-07-14.md` — ~75 manual
fixes, ~54 YAML fixes. **This register entry carries the blockers**, which must not be lost with the workspace.

**🔴 SB-1 — `ch05-plot-wave-scatter.spin2:22` + `ch05:599`: the sine wave is a FLAT LINE.**
`angle := x * ($FFFF_FFFF / 511)`. Spin2's `/` is a **signed** divide; `$FFFF_FFFF` = −1; −1 / 511 = **0**.
Compile-verified (`pnut-ts` 1.55.0): `$FFFF_FFFF / 511` → `0x00000000`; `+/` → `0x00804020`. So `angle` is 0 for every
column and the chapter's headline "one cycle of a CORDIC sine wave" renders as a horizontal line — **lying on top of the
grey axis the program draws two statements earlier**. **Shipped in the released PDF and the example ZIP.** It compiles,
it runs, it draws a plausible picture. Fix (both files): `($FFFF_FFFF +/ 511)`.

**🔴 SB-2 — `ch06-logic.md:44`: the LOGIC chapter's FIRST example declares 32 channels, not 4.**
The parser takes the first number after a label as the channel **COUNT**. `'CLK' $00FF00` ⇒ 65,280 → clamped to **32**;
the index saturates and `'DATA'`, `'CS'`, `'WR'` are **silently dropped**. Proof in-repo: `ch06-logic-spi-bus.spin2` (run
on silicon) writes `'CS' 1 $00FFFF …` — **with** explicit counts. **Root cause: the snippet is inline-only — it has NO
example file**, so it never went through compile-and-run.

**🔴 SB-3 — `ch13:121` + `:160` (+ their twin `.spin2` files): pack MSB-first while the chapter's own rule says LSB-first.**
`packed := (packed << 1) | …` puts the FIRST sample in bit 31; the host unpacks LSB-first ⇒ each long replays in
**reverse time order**. **Root cause: the twins ran on silicon and PASSED — because the payload is `getrnd()`. Reversed
random noise is indistinguishable from forward random noise.** The test data could not reveal the bug.

**🔴 SB-4 — `ch05:161-176`: PLOT `PRECISE` default INVERTED.** Manual says sub-pixel is ON by default; it is **OFF**
(`vPrecise` starts at 8 = whole-pixel). v55, `plot.yaml` and the REF all agree the manual is wrong.

**🔴 SB-5 — `ch05:302-310`: white text on a white background.** `COLOR` only carries into `TEXT` when `TEXT` is the
**next** key; a `SET` intervenes, so `vTextColor` stays at its default white. *(The same defect was in `conflict-testI`,
the hardware test we used as TEXTSTYLE ground truth — its colour-coding never worked.)*

**🔴 SB-6 — `appendix-c:47` + `spectro.yaml:52,53,82`: SPECTRO axes INVERTED.** At the default `TRACE $F` the W/H swap
does **not** fire ⇒ horizontal = **TIME**, vertical = frequency. `ch10:124-126` already says this correctly — the
appendix contradicts its own chapter, and the KB ships the inversion three times.

**Structural lesson (the reason these survived every gate):** three blockers, three *different* holes in the same net —
a construct with **no example file**; test data that **cannot reveal** the defect; and a failure that **hides under a
grid line**. Compile-and-run is necessary and **not sufficient**. What catches this class is an example for *every*
construct we teach, plus test data whose expected output is **asymmetric**.

**Gate:** all of this lands in ONE coordinated sweep (manual + examples ZIP + YAMLs), then re-render and re-release
together. YAML side rides F-212 + its addendum.

### F-215 — App-note in-document Revision History drifts from the cover and cites never-shipped drafts — `CONFIRMED` · **DEFERRED: rides each doc's next natural release** (Stephen 2026-07-14)

> **SCOPE CORRECTED 2026-07-14 — this is SIX of seven app notes, not two.** As originally filed, F-215
> named only P2AN005/P2AN006, because the detection grep matched `v0.1.0` / "initial draft". **P2AN001–004
> express the same defect in a different shape** — a Revision History *table* whose draft row reads a bare
> `0.1.0` / "First draft" — and were missed. A full re-sweep of all seven app notes (and of the seven
> manuals, which carry **no** in-doc Revision History at all, so are out of scope) gives the true picture.
> *Lesson: the first sweep keyed on one literal spelling of the defect rather than on its shape.*

**The two defect classes (a doc may have both):**

| App note | Cover | Rev-History top | Never-shipped draft row | Classes |
|---|---|---|---|---|
| P2AN001 | 1.0.2 | 1.0.1 | `0.1.0` "First draft" | **A + B** |
| P2AN002 | 1.0.1 | 1.0.0 | `0.1.0` "First draft" | **A + B** |
| P2AN003 | 1.0.1 | 1.0.0 | `0.1.0` "First draft" | **A + B** |
| P2AN004 | 1.0.1 | 1.0.0 | `0.1.0` "First draft" | **A + B** |
| P2AN005 | 1.0.1 | `v0.1.0` (only entry) | `v0.1.0` "initial draft" | **A + B** |
| P2AN006 | 1.0.0 | `v0.1.0` (only entry) | `v0.1.0` "initial draft" | **A + B** |
| P2AN007 | 1.0.0 | 1.0.0 | — | clean ✅ |

- **Class A — the Revision History does not list the version the document IS.** Every released app note except
  P2AN007 has a cover version that appears nowhere in its own history. This is the *systemic* half: the
  2026-07-12 fleet release bumped these covers and never touched the in-doc tables, so **the table goes stale
  on every release**. It will keep re-breaking until the gate below is closed.
- **Class B — never-shipped draft rows.** `git tag` confirms **no `0.1.0` tag has ever existed** for any app
  note; those rows describe a version the public never saw.
- **Worst sub-case (P2AN005/P2AN006):** the draft row is the *only* entry, so a released doc's history tells the
  reader it is an *"initial draft for review … hardware confirmation pending."* That misreports the document's
  **maturity**, not merely its version number.

- **DISPOSITION (Stephen 2026-07-14): DEFERRED RENDER, SOURCE FIXED NOW.** No reader's understanding of the
  technical material (ADC, CORDIC, DAC, smart-pin measurement, TASK, stack sizing) is harmed by a stale version
  table, so this does **not** justify re-rendering and re-releasing six documents on its own. But the *source* is
  corrected immediately, so each doc is already right when its next natural release comes — the fix and the gate
  land in the same window and meet at that release.
- **✅ SOURCE FIXED 2026-07-14 — all six.** Every app note's `## Revision History` now lists exactly the versions
  `git tag` says shipped, top entry == cover version, no never-shipped draft. Each new row is **derived from the
  audited CHANGELOG entry**, not authored fresh. Form follows history depth: a **table** for 2+ shipped versions
  (P2AN001–005), a **single bullet describing the document** for exactly one (P2AN006/007 — the style guide's
  "initial releases describe the document, not a delta"). P2AN005 converted bullet→table (it has two shipped
  versions). The released PDFs still carry the old tables until each doc re-renders — that is the accepted defer.
- **The rule it breaks:** `methodology/changelog-style-guide.md` — **"Never-shipped versions are never mentioned … For users, they never existed. If a version number was never released, delete any artifact referencing it."** v0.1.0 was a review draft: never in `deliverables/documents/README.md`, never tagged. It must not appear in reader-facing history. The same guide's **"Initial releases describe the document, not a delta"** means the v1.0.0 entry must holistically describe the document, not delta against the unpublished draft.
- **Why it slipped:** the release process promotes `opus-master/CHANGELOG.md` (which P2AN005/6 got *right* — a single holistic initial entry) but the **doc's own in-PDF Revision History is a separate artifact** that nothing gated. `audit-changelog` audits `CHANGELOG.md`; no check compared it to the rendered Revision History. The two drifted silently.
- **P2AN007 (fixed pre-release, 2026-07-13):** the changelog audit gate caught it before promotion. `CHANGELOG.md` rewritten as a conforming initial entry (holistic, no delta headings, no draft reference) and the doc's Revision History reduced to the single v1.0.0 entry. Re-rendered.
- **Outstanding — six docs, deferred (see DISPOSITION).** P2AN001–006 each carry the fix into their next release.
  **A shipped PDF is only fixed by re-rendering it**, so until a doc re-renders for its own reasons, the released
  PDF keeps the defect. Not bundled with the F-214 Assembly re-render (Assembly is a *manual* — no in-doc
  Revision History — so it is untouched by this finding).
- **The fix, when each doc's turn comes:** drop the never-shipped draft row entirely, and ensure the top entry is
  the version on the cover. P2AN007 is the model (single holistic entry for an initial release; delta entries only
  against a prior *published* version). Style authority: `methodology/changelog-style-guide.md` — *"Never-shipped
  versions are never mentioned … If a version number was never released, delete any artifact referencing it"* and
  *"Initial releases describe the document, not a delta."*
- **🔧 PROCESS GAP — ✅ CLOSED 2026-07-14. This was the real fix; without it Class A regenerates on every release.**
  The drift is *caused by the release itself*: it bumps the cover and leaves the in-doc table behind. Two-sided fix,
  because of an **ordering constraint that was initially got wrong** — the Revision History lives *inside the body
  markdown that gets rendered*, so `release-manual` (which runs **after** the PDF exists) physically **cannot** fix
  it; by then the stale table is already printed. Authoring must happen at prep time.
  - **`prepare-manual/project-overlay.md` (NEW) — authors it.** Step 5 enumerated only *two* version locations
    (markdown cover, `request.json`) and even warned that bumping one without the other creates a mismatch. It did
    not know about the **third**: the in-doc `## Revision History`. The overlay adds it, requires the new entry be
    **derived from the CHANGELOG** entry being released (two artifacts telling the same story in independently-written
    prose *will* diverge), and makes **`git tag`** — not the CHANGELOG, not memory — the authority for "was it shipped."
  - **`release-manual/project-overlay.md` — verifies it (backstop).** Phase 1 now asserts, against the RENDERED PDF:
    top Revision-History entry **==** cover version, and **no untagged version named**. A mismatch blocks the release
    exactly as a content-drop does (and costs a full re-render, which is why prep owns the authoring).
  - **Correction to an earlier claim in this entry:** it said the skill was *"central-owned: propose, do not edit."*
    **That was false** — `release-manual` and `prepare-manual` are **project-local** (`.claude/skills/`), not in
    `~/.claude/skills/`. The claim was inherited from a prior session and repeated without checking. Both were edited
    directly.
- **Origin:** surfaced 2026-07-13 running the mandatory changelog audit gate for P2AN007's release; the sibling comparison against P2AN005/P2AN006 exposed it as pre-existing and shipped.

---

## XBYTE technique-mining sweep — reference implementations expose two doc defects (2026-07-14) — F-217, F-218

> **Origin.** Stephen asked for a per-processor "what will hurt when you emulate this" table in the XBYTE
> Guide, and proposed we ground it by studying **live, working emulators** rather than reasoning from ISA
> facts. The study immediately surfaced two defects. Full evidence ledger:
> `engineering/document-production/manuals/p2-xbyte-programming-guide/TECHNIQUE-MINING.md`
> (per-source, because the techniques enter the manual body *anonymously* — the ledger is the only place
> the lineage lives). **Note the path:** it lives at the manual **root**, not in `audit/`, because
> `.gitignore:175` ignores `manuals/*/audit/` — a durable source-of-record cannot live there.

### F-217 — XBYTE Guide §5.3 presents interruptibility as a pure benefit and omits that handlers doing atomic work must shield with `REP` — `DONE (2026-07-14)` · class-wide sweep run → **F-224**

**What §5.3 says today**, in full:

> *"XBYTE is also **interruptible**: an interrupt can occur during dispatch, and the engine resumes the
> bytecode stream afterward. Bytecode interpretation does not lock out a cog's interrupts."*

Every word is true. But it is framed **entirely as a benefit**, and the manual never states the
consequence: **if a bytecode handler performs a multi-instruction sequence that must be atomic — a CORDIC
operation, a read-modify-write of a shared variable — an interrupt can land in the middle of it.** The
reader is told interrupts are free and is never told to fence.

**Evidence — Chip Gracey's Spin2 interpreter shields exactly this, eight times, in his own words:**

| Site | Code | Chip's comment |
|---|---|---|
| `op_quna` | `rep #99,#1` | *"use REP to protect cordic operation until ret/_ret_"* |
| (SCAS) | `rep #99,#1` | *"use REP to protect cordic operation until call/ret/_ret_"* |
| `wrf` | `rep @stall,#1` | *"use REP to protect variable from interrupts"* |
| `clkset_init` | `rep #99,#1` | *"use REP to stall interrupts until _ret_"* |
| ×4 more | `rep @.stall,#1` | *"use REP to stall interrupts to protect cordic operation"* |

**`REP` appears zero times in the XBYTE Guide.** This is a correctness hazard, not a style note: a reader
who follows our text will write a handler that is silently corrupted by an interrupt, intermittently.

- **Passes the promotion filter three ways** — it is the reference implementation (Chip's), it converges
  across eight independent sites within it, and the mechanism explains why it is right.
- **Fix:** §5.3 gains the consequence and the `REP` shield; a safety section makes it explicit.
- **Class-wide sweep owed:** does any *other* manual tell a reader that P2 interrupts are free during a
  hardware-driven sequence without naming the fence? Check the Assembly Language Manual's interrupt and
  CORDIC chapters before this closes.

### F-218 — `SingleStep-Debugger-Theory-of-Operations.md` §6.4 mislabels `GETBRK` D[25] as "C,Z affected by XBYTE" — `NEEDS-VERIFICATION`

**Our own ingested doc says:**

> *"Displayed as 3 hex digits. A checkmark glyph appears if **bit 25** of `mBRKC` is set (**C,Z affected by
> XBYTE**)."*

**The Silicon Doc says otherwise.** Per P2KB `p2kbPasm2Getbrk`, `GETBRK D WC` returns:

| Field | Meaning (Silicon Doc) |
|---|---|
| D[27] | 1 = SKIP · 0 = SKIPF/EXECF/XBYTE |
| D[26] | LUT sharing enabled |
| **D[25]** | **XBYTE pending on next `_RET_`/`RET`** |
| D[24:16] | the 9-bit XBYTE mode |

"C,Z affected by XBYTE" is the **F bit**, which is the *low bit of the mode operand* — i.e. **D[16]**, not
D[25]. The two are different facts about different bits, and our doc appears to have conflated them.

- **NOT SETTLED, and deliberately not fixed.** The checkmark's meaning is decided by the **host-side**
  display code (PNut / term-ts), not by Chip's P2-side debug stub — `Spin2_debugger.spin2` only calls
  `getbrk` and ships the word to the host. So the P2-side source **cannot** adjudicate this. Settling it
  needs the host display source or Chip.
- **Two possible truths:** (i) our gloss is simply wrong and D[25] means "XBYTE pending"; or (ii) the
  debugger's checkmark genuinely reflects the F bit and our doc attributed it to the wrong bit index. Either
  way **the doc as written is wrong**; only the repair differs.
- **Consumer risk:** the XBYTE Guide is about to gain a "Debugging XBYTE" section citing `GETBRK` fields.
  It will cite **the Silicon Doc layout**, not this doc, until this is resolved.
- **Wider lesson (already a standing rule, freshly demonstrated):** our own ingested derivations are **peer
  tier, not authority**. This was caught only because the field layout was cross-checked against P2KB
  instead of being trusted.

### F-219 — XBYTE Guide §10.2 assigns **all** x86 prefixes to one-shot `SETQ2`; the real 8086 emulator does not, and cannot — `DONE (2026-07-15)` (map/modifier prefix split now correct across §14.4/§17.1–17.3; verified in the release-gate audit — the section renumbered §10.2→§14.4 in the v0.3.0 reshape)

**What §10.2 says today:** of x86 — *"the byte stream fits; the decode explodes — prefixes and escapes
are a job for one-shot SETQ2 alternate tables, and the long tail is hand-rolled."*

**This conflates two different kinds of prefix**, and is wrong for one of them:

| Kind | Examples | What it changes | Right tool |
|---|---|---|---|
| **Map / escape** | 6809 `$10`/`$11`, Z80 `CB`/`ED`, x86 `$0F` | **which handler runs** — selects a different opcode map | **one-shot `SETQ2`** ✅ |
| **Modifier** | x86 segment override, `REP`, `LOCK`, operand-size | **not** which handler runs — *how it behaves* | **state register + re-fetch** ❌ |

An alternate table **redirects dispatch**. A segment-override prefix does not want dispatch
redirected — it wants the *same* handler to touch *different memory*. The real 8086 emulator
(`Simple-i8086`, from forum thread 174634) uses a shared body plus a state register plus a jump back
to the fetch loop:

`i_seg_cs/ds/es/ss  mov i_override, i_cs/ds/es/ss` (one body, four prefixes, selected by the table
entry's skip pattern) → `bith i_override,#31` → `jmp #\i_next`.

`REP` likewise re-executes the following instruction N times **without re-fetching**, which XBYTE's
fetch-on-`_RET_` loop cannot express as a plain `_RET_` handler.

- **Provenance of the defect:** the §10.2 x86 row was **Claude's derivation**, written from ISA
  knowledge plus XBYTE mechanics, never checked against an implementation. Same root cause as **X3**
  (the 68000 `RFWORD` claim, also unverified — see below).
- **Fix:** split the prefix taxonomy in Ch. 12 / Ch. 10; correct the x86 row.
- **Related, not yet filed:** §10.2's 68000 row (*"read the word with `RFWORD`, decode further by
  hand"*) is also an unverified derivation — and **two 68000 emulators exist (MegaYume, NeoYume) and
  neither uses XBYTE at all.** Filing deferred until those cores are read properly.
- **Wider correction to the same chapter:** §10.2 grades guest CPUs on **instruction shape**, but the
  axis that actually decides it is *(a)* **does the guest's code live in hub** (the FIFO streams hub
  only) and *(b)* **is LUT free** (XBYTE reads its table from LUT). The 65816 — "the sweet spot" by
  our table — is emulated on P2 **without XBYTE** for exactly these two reasons. Full evidence: the
  mining ledger §8.
- **Evidence ledger:** `engineering/document-production/manuals/p2-xbyte-programming-guide/TECHNIQUE-MINING.md` §10b.

---

## `architecture/xbyte_engine.yaml` — all three programming examples are broken (2026-07-14) — F-220…F-223

> **Origin.** Chasing an open question for the XBYTE Guide (*what does Chip's "no stack pop" mean?*), the
> authoritative KB entry `p2kbArchXbyteEngine` was consulted — and **every one of its three
> `programming_examples` is wrong.** This is the YAML an agent would use to generate XBYTE code.
> Ground truth used below: the **Silicon Doc** narrative + demo, **Chip's own Spin2 interpreter**,
> **Parallax's official `xbyte.spin2`**, plus Zog and the 8080 emulator — nine implementations, all
> agreeing. Evidence: `manuals/p2-xbyte-programming-guide/TECHNIQUE-MINING.md`.
>
> **File:** `deliverables/ai/P2/architecture/xbyte_engine.yaml`

### F-220 — `bytecode_routine_example`: the LUT table entry is built with the wrong shift **and** the wrong address space — `DONE (2026-07-14)`

```
' LUT entry: routine address | skip pattern
LONG    (@push_routine << 23) | 0          # line 215
```

**Two defects in one line:**

1. **`<< 23` is wrong.** The *same YAML*, at `lut_table_format` (~line 100), states it correctly:
   `[9:0] = routine address`, `[31:10] = SKIPF pattern`. Shifting the address left **23** buries it
   inside the skip-pattern field. The entry cannot dispatch.
2. **`@` yields a HUB address.** `EXECF` jumps to a **cog/LUT** address (`$000–$3FF`). The `@` operator
   returns a hub address, which will not fit `[9:0]` and is meaningless to `EXECF`.

**Ground truth** — Chip: `bc_read  long  var_rd | %0111001110 << 10`. Parallax: `bytetable  long  r0`.
Correct form: `LONG  push_routine | (skip_pattern << 10)` — **no `@`, shift the *pattern*, not the address.**

**A third defect in the same example, found later by actually compiling:** the routine ended
`_RET_   NOP`. **That does not assemble** — `pnut-ts` rejects it outright: *"NOP cannot have a
condition or `_RET_`."* The fix already applied (`_RET_ ADD stack_ptr, #4`) removes it, but it was
corrected by luck rather than by knowledge, and it is worth recording *why* it was missed: the
example was read for **semantics** and never **compiled**. A code example that has not been through
the assembler is an assertion, not a fact.

### F-221 — `simple_interpreter`: never pushes `$1FF`, so it would not start XBYTE — `DONE (2026-07-14)`

```
' Start XBYTE engine
CALL    #xbyte_start                        # line 207
xbyte_start:
_RET_   SETQ    #%00000001                  # line 210
```
…and the `starting_xbyte` block asserts: `requirement: "$1FF must be on stack (from CALL)"` (line 64).

**A `CALL` pushes its own return address — not `$1FF`.** So the `_RET_` returns to the instruction after
the `CALL`, XBYTE never engages, and the example silently does nothing.

**The Silicon Doc is explicit** — *"Starting XBYTE … is done all at once by a `_RET_ SETQ {#}D`
instruction, **with the top of the hardware stack holding `$1FF`**"* — and gives the sequence
`PUSH #$1FF` / `_RET_ SETQ #$100`. **All nine implementations we read use `PUSH #$1FF`.** The
`(from CALL)` gloss on line 64 is also wrong and must go.

### F-222 — `compressed_mode`: does not assemble, mislabels its own fields, and would not compress — `DONE (2026-07-14)`

```
_RET_   SETQ    #%F_0000_00_1               # line 226
' F = base address (4 bits)                 # line 227
' 0000 = compression threshold              # line 228
' 1 = set flags from bytecode               # line 229
```

**Three defects:**

1. **It does not assemble.** `%` introduces a **binary** literal; **`F` is not a binary digit.**
2. **The field labels are inverted.** In `%ABBBB00xF` the base **`A` is ONE bit**; the **four `B` bits**
   are the compression threshold. The comment calls the leading field *"base address (4 bits)"* — and
   reuses the letter **F**, which collides with `F` = the flag-write bit.
3. **The threshold value defeats the example's own purpose.** The Silicon Doc requires **`%BBBB > 0`**.
   With `BBBB = %0000` nothing is compressed as described. For the *"16 primary + 240 extended"* split
   this example claims (and which the YAML's own `compression:` field states), the threshold must be
   **`%0001`**: high-nibble 0 → 16 primary bytecodes `$00–$0F`; high-nibble ≥ 1 → 240 extended in 15
   groups. **16 + 240 = 256.** ✓

### F-223 — mode-operand **bit 1 is the index-form selector**, not an undocumented/stack bit — `RESOLVED (2026-07-16, documentary + Chip-confirmed)`

**Prior (incorrect) reading — now retired.** F-223 was originally logged as "the `x` bit is undefined;
the demo's *no stack pop* comment suggests it's a stack-pop control; route to Chip." That reading was
**wrong**: it treated bit 1 as a single undocumented bit and read the demo comment as a hint about the
stack.

**The resolved definition.** Reading the *full* Silicon Doc v35 mode table (all ten forms, not just the
two 256-entry patterns) shows bit 1 straight down the column:

| mode | primary (bit 1 = 0) | alternate (bit 1 = 1) |
|------|--------------------|-----------------------|
| 128 | `%AAxx0010F` → b[6:0] | `%AAxx0011F` → b[7:1] |
| 64 | `%AAAx1010F` → b[5:0] | `%AAAx1011F` → b[7:2] |
| 32 | `%AAAAx100F` → b[4:0] | `%AAAAx101F` → b[7:3] |
| 16 | `%AAAAA110F` → b[3:0] | `%AAAAA111F` → b[7:4] |

**Bit 1 selects the index form**: `0` = index the dispatch table from the bytecode's *low* bits;
`1` = index from its *high* bits (freeing the low bits as an operand in `PA`). In the **256-entry mode**
the bytecode already fills all eight index bits, so there is no low/high choice and **bit 1 is ignored** —
a genuine don't-care in that mode only. This is where the two 256 patterns print it as a bare `x`.

- **Authority:** documentary (directly readable from the v35 mode table) **and confirmed by Chip Gracey**
  in conversation — *"there is nothing to switch between with 8-bit, so the bit is ignored."* Not a
  finding to verify; not a guess.
- The demo's *"no stack pop"* comment is **unrelated to bit 1** — that speculation is withdrawn.
- **Applied to the manual (2026-07-16):** XBYTE Guide §8.2 rewritten (bit 1 = index-form select; ignored
  in 256), §9.2 table expanded to all ten forms with the primary/alternate split, §9.5 + Appendix A +
  the see-also index all corrected. `opus-master/xbyte-body.md`.
- **YAML (applied 2026-07-16):** `architecture/xbyte_engine.yaml` — the `x_bit_undocumented` block is
  replaced by `index_form_bit` (bit 1 = index-form select; 256 don't-care), and the 128/64/32/16 entries
  gained `alt_pattern`/`alt_index_calc`. Commit `bb02525a`. Publishes on the next KB release rail (§9).
- **Chip queue:** Q7 is **resolved** — removed from `DRAFTS/QUESTIONS-FOR-CHIP-GRACEY.md`; strike from task #54.

### F-224 — Assembly Manual: the CORDIC interrupt hazard is documented on the `REP` page, but **not on the CORDIC pages** — `CONFIRMED` (low severity, cross-reference gap)

**Raised by F-217's class-wide sweep.** Having found that the XBYTE Guide sold interruptibility as a
pure benefit, the same question was asked of every other manual: *does anything show a CORDIC
issue/collect pair without telling the reader it must be fenced?*

**The Assembly Manual is NOT wrong.** `part-ii/instructions-r.md` teaches the fence properly, and even
uses a CORDIC example:

> `' Protect CORDIC operation from interrupts` … `qmul  y, x`

and states the mechanism outright: *"Interrupts are blocked during REP execution — including debug
interrupts that ordinary masking cannot hold off — to maintain timing precision and keep the repeated
block atomic."* It also carries the useful nuance that the idiom *"is only needed in PASM2 code with
interrupts enabled; Spin2 operators are already protected by the interpreter."*

**But the warning is not where the affected reader is standing:**

| Page | Content | Interrupt mentions |
|---|---|---|
| `instructions-q.md` | **QMUL · QROTATE · QDIV** — the CORDIC **issue** ops | **0** |
| `instructions-g.md` | **GETQX · GETQY** — the CORDIC **collect** ops | 3 — **all from GETBRK**, none about CORDIC |
| `instructions-r.md` | REP | ✅ the fence, with a CORDIC example |

A reader who looks up `QMUL` — which is exactly what someone about to *write* a CORDIC sequence does —
learns nothing about the hazard. They find it only by happening to read the `REP` page.

- **Severity: low.** This is an omission at the point of need, not a false claim. Same *class* as F-217,
  milder in kind: the information exists in the manual.
- **Fix (small):** a cross-reference note on the CORDIC issue/collect pages — "a CORDIC command and its
  result must not be split by an interrupt; see REP" — costing a few lines, no content change elsewhere.
- **Release consideration for Stephen:** the Assembly Manual shipped **v3.1.4 on 2026-07-14** (a
  render-only patch). This is a *content* change and would need its own bump. It is a documentation
  improvement, not a correctness bug in the shipped text, so it can ride the manual's next natural
  release rather than forcing one.

**Also observed (not a defect):** 22 stray `*.backup-encoding-conversion` files sit in
`p2-assembly-language-manual/opus-master/part-ii/`. They are **untracked** — `git ls-files` returns
zero — so nothing ships and no glob in the assemble scripts reaches them (those use explicit
`REQUIRED_FILES[]`). Working-tree clutter only; worth sweeping, not a release concern.

### F-225 — two KB YAMLs framed complementary-output **dead-time as a single-pin PWM feature** — `DONE (2026-07-16, Chip-confirmed)`

**Surfaced by the F-223 "what else did we miss?" sweep** (same failure class: a downstream
derivation that dropped a fact its faithful source had). Two pattern YAMLs presented dead-time as
an attribute of one PWM Smart Pin:

- `architecture/smart_pin_patterns.yaml` → `motor_pwm_with_deadtime` (single `pwm_pin`; the second
  pin never appears)
- `language/pasm2/concepts/streamer_smartpin_control.yaml` → `pwm_sawtooth.dead_time_critical` (same)

**Chip Gracey (conversation, 2026-07-16):** the P2 has **no single-pin complementary-output or
dead-band mode**. A complementary pair is **always two Smart Pins**, one per side, coordinated
carefully. Corroborated by `isp_bldc_motor.spin2` (OBEX 2874): high side true, low side inverted
(`P_INVERT_OUTPUT`), **software** dead-gap offset so the active intervals never overlap. The faithful
upstream (`engineering/ingestion/sources/code-analysis/bldc-motor-control-analysis.md`) had it right
(two `wrpin`, one inverted) — the pattern YAMLs collapsed it to one pin.

- **Fixed:** both YAMLs now show two pins + `P_INVERT_OUTPUT` + software dead-gap, with the
  no-single-pin-mode framing and a cross-ref between them.
- **Manual:** IOSP §9.1 gained a short "Complementary Outputs and Dead-Band" note (two coordinated
  Smart Pins; dead-band is software, no width register). The IOSP body had shipped **no** dead-band
  claim, so nothing wrong was public — this closes the RA-15 proposed-add (premise refuted).
- **YAML publishes on the next KB release rail (§9).**

### F-226 — DAC ENOB is **unmeasured** — ship the qualitative caveat, print no number — `RESOLVED (2026-07-16, Chip-confirmed)`

**Chip Gracey (conversation, 2026-07-16):** the dithered 16-bit DAC's effective-number-of-bits has
**not been measured**, and no better answer exists. So no ENOB figure is printable. The IOSP manual
already ships only the qualitative caveat ("nominal 16-bit, averaged over time; absolute accuracy
limited by the 8-bit DAC core") — **no edit needed**. The reviewer's "~10–12 bits" stays out
(opinion, and now confirmed never-measured). Closes the RA-18/36/49/56 ENOB question.

## Interactive DEBUG examples never ran — `PC_KEY`/`PC_MOUSE` shipped without their escape backtick (2026-07-26) — F-227

### F-227 — un-backticked `PC_KEY`/`PC_MOUSE` inside a display message is sent to the window as **literal text**; the command never runs — `DONE (2026-07-26, compiler-proven)` · re-test pending

**Surfaced by Stephen's run-verification pass** over the Debug Window Manual's 34-program example
library on PNut/Windows: 30 ran, 4 failed. Three of the four are every example in the library that
uses `PC_KEY`/`PC_MOUSE` — a 3-of-3 hit rate on one construct.

**Root cause.** Everything following the display name in a backtick statement is *display text*. A
Spin2 debug command must tick back out of display text into command mode, exactly as `` `(expr) ``
does. All three examples omitted that second backtick. Proven with `pnut-ts -d` v1.55.0 by reading
the emitted display strings out of the two binaries:

| source | emitted display text |
|---|---|
| `` debug(`Adjust PC_KEY(@key)) `` | `` `Adjust PC_KEY(@key `` — the characters are transmitted to the window; **no command compiled** |
| `` debug(`Adjust `PC_KEY(@key)) `` | `` `Adjust `` + the real `PC_KEY` command bytes |

The pointer variable is therefore **never written**; the control loop polls forever and responds to
nothing. **No compile error** — same silent-failure class as double quotes in a display string
(`DEBUG-Statement-Quoting-Briefing`, §2). Uppercase after the tick compiles identically to the
lowercase form used in the bench-certified reference (`REF/robot-dog/test_dog_panel.spin2`:
`` DEBUG(`pnl `pc_key(@keyCode)) ``), which is what exposed the defect.

**Why it survived to release:** these three are the manual's only *interactive* examples. Their
figure-generator harnesses cannot be certified from a screenshot, and the 2026-07-11 run audit
accepted a structural argument in place of a hardware run. A structural contrast is only as good as
the idiom it is compared against — and the comparison against the dog-panel idiom was recorded as a
TODO and never performed.

- **KB fixed:** `debug-commands/pc_key.yaml`, `debug-commands/pc_mouse.yaml` — new `usage_rules`
  entry naming the silent failure, and both worked examples corrected. **Publishes on the next KB
  release rail (§9).**
- **Manual fixed:** examples `ch12-keyboard-adjust`, `ch12-mouse-pointer`, `ch15-control-panel` +
  their three `fig-*` harnesses; prose in `ch12-bidirectional.md` (the rule is now taught as rule 2
  of two, with the ✅/❌ contrast), `ch15-panels.md`, `appendix-a-command-reference.md`. Byte-identity
  across all 34 examples re-verified.
- **Also added (Stephen, from the dog panel):** ch15 now teaches the mouse-vs-artwork Y flip —
  drawn panels need none (draw and `PC_MOUSE` share PLOT space), BMP-authored panels need
  `py := (PANEL_H - 1) - py` because artwork is authored top-left. Bench-confirmed 2026-06-06 in
  `test_dog_panel.spin2:hitSlot()`.
- **Open:** the fourth failure (`ch14-scope-trace`, SCOPE window does not open) is **not** this
  defect and has no proven cause yet — see the note below.

**Not yet grounded — `ch14-scope-trace`.** A keyword-collision hypothesis (display named `Trace`
vs. the `TRACE` keyword) was **refuted by our own hardware evidence**: the 2026-07-11 capture
`fig-14-scope-trace-scope_WDW.bmp` OCRs as *"Trace - SCOPE"* with channel *"Signal"* rendered, from
a byte-identical create sequence. Display names are read positionally and may be keywords. Cause
still open; awaiting a symptom read + a re-run of the known-good figure generator on the current
bench.

---

*Move-aside 2026-06-13 after the v1.9.0 release closed out F-001..F-124. The archive holds the full history; this active register carries only the carry-forward guardrails and the ingestion-tracked items. New findings continue at F-125.*
