# P2KB Correction Findings — Consolidated Register

**Purpose:** the register of everything we find that is **wrong or needs correction** — primarily in the P2 Knowledge Base YAML (`deliverables/ai/P2/`), but also any other source/content correctness issue worth tracking. This is the hand-off document for the agent that corrects the P2KB (via `yaml-knowledge-base-maintenance`).

**This file carries OPEN work only.** Closed findings are archived, not kept here. Ask "what is
outstanding?" of this file alone — never re-derive completion state from an archive.

**How to use it:**
- When any work (manual production, audits, example compilation, ingestion, bench) surfaces something incorrect, **add it here** — do not leave it only in a per-manual note.
- Each finding gets an ID, a status, the exact location, what is wrong, the evidence, and the proposed correction.
- **Annotate as you fix, in the same pass** — flip the status, add an applied-note and source trace, and log newly-surfaced defects as new findings. A register whose statuses lag the YAML lies and invites re-chasing.
- **One finding lives in exactly one place.** When a finding is revised, **rewrite its entry in place**; never append a correction below the entry it corrects. The prior text is in git and in the archives.
- Consultation protocol (status-before-content, duplicate IDs are a STOP): `.claude/skills/REGISTER-CONSULTATION.md`.

**Status legend:** `CONFIRMED` (verified against an authority; ready to fix) · `NEEDS-VERIFICATION` (suspected; must be checked before acting) · `PARTIAL` (some of it applied; the rest still owed) · `DONE` (corrected + verified) · `WONTFIX` (investigated, not a defect) · `RESOLVED-INVALID` (the reported defect does not exist) · `TRACKED → ingestion` (real, but the resolution lives in the ingestion head).

**A fix applied but not yet validated is NOT done** — it stays here until its validation lands (the `[~]` rule from `punch-list-maintenance`). That covers a YAML edit awaiting its EF entry, and a manual fix awaiting its re-test.

**Authority order for P2 facts:** empirical / hardware-verified results in `engineering/ingestion/external-sources/hardware-verification/` (strongest — they have overturned every other tier) → the `pnut-ts` compiler, for legality only → Parallax documentary sources under `engineering/ingestion/sources/` → the published P2KB YAML. Community/forum material is an upstream lead, never a citable authority.

**No inference or derivation.** Every correction must trace to an authoritative source. Aligning a file to an authority it contradicts is fine; **inventing a value or claim that no source states — by computation, reasoning, or "it must logically be" — is not.** If a change can only be justified by inference, log it as a finding that needs a source. Match the source's wording, not an interpretive paraphrase.

**Next finding ID: `F-267`**

**Archives** — search them before re-filing; a finding that reappears is usually a regression:
- F-001…F-124 → `correction-sweeps/2026-06-13-P2KB-CORRECTION-FINDINGS-archive.md`
- F-125…F-266 (closed) → `correction-sweeps/2026-08-15-P2KB-CORRECTION-FINDINGS-archive.md`

> **Swept 2026-08-15** per `punch-list-maintenance`: 129 closed findings archived, 3,161 lines → this
> file. The previous sweep was deferred on 2026-06-20 pending G-004 and G-005; G-005 closed
> 2026-07-04, and G-004's remainder was found to be out of KB scope entirely (see its entry), so the
> deferral's condition is discharged.

---

## Carry-forward guardrails — investigated and settled; do NOT re-file (full detail in the archive)

- **F-002 (`WONTFIX`):** `?` / `||` operator-form failures were an agent usage error — the KB is correct (`??var` = XORO32 random; `ABS()` not `||`; `?` is the ternary operator).
- **F-036 (`WONTFIX`):** `calld.yaml` — LOC loading a 20-bit address into PA/PB/PTRA/PTRB is not a defect.
- **F-093 (`WONTFIX`):** `lockrel.yaml` C-flag polarity — the appendix's "inverted" claim is the error; the YAML is correct (C = lock-was-held).
- **F-114b (`RESOLVED-INVALID`):** the MIDI display modes KEYBOARD / GRID / ROLL / MONITOR do **not** exist in PNut v55 — do **not** add them to `midi.yaml` (it carries an explicit `not_supported:` claim).
- **Verified-resolved (don't re-chase):** the Jan-2026 streamer KB audit's issues were all reconciled in the 2026-05/06 passes (DAC routing, 32-pin groups, mode encoding, xcont/xzero phase wording, setxfrq 2³¹ formula, streamer symbols). Only the XZERO concept text was open and is fixed (F-003).

---

## Open — CONFIRMED corrections (2026-08-11, DeSilva reader-report sweep)

> **Sweep origin:** a reader reported that the DeSilva tutorial's Ch.1 "Experiment 3:
> Fading" does not fade on a P2 EVAL (#64000 Rev B) — copied, pasted, triple-checked.
> Root cause: the smart-pin mode was written **without `P_OE`**, so the smart pin
> generated the PWM but the pin's output driver stayed disabled. Confirmed against
> `language/spin2/methods/wrpin.yaml` `tt_field` — `when_smart_pin_on: "x0=output
> disabled, x1=output enabled (regardless of DIR)"` and `p_oe_required_for: "All output
> modes (NCO, PWM, Pulse, Transition, Serial TX, DAC, USB)"`. The manual was fixed the
> same pass; **the same class is still present in the KB's own examples**, below.
> Note this class had already been fixed once in DeSilva (v3.0.3 corrected the
> async-serial TX recipe to `P_ASYNC_TX | P_OE`) but was **not swept class-wide** —
> which is how the PWM example survived to a reader.

- **F-250 — the #64000 Eval Board Rev C guide was ingested with EVERY DIGIT MISSING; any
  numeric fact traced to it is unsafe.** `engineering/ingestion/sources/p2-eval-board/`
  was extracted with a text-layer tool, but that PDF's font encoding does not map numerals —
  `pdftotext` silently drops them. Evidence: the shipped `p2-eval-board-narrative.txt` has
  digits on **91 of 1315 lines**; `pdf-ocr --force-ocr` + re-extract yields **368**. Lines
  read *"The Propeller has cores, KB of hub RAM, and Smart I/O pins"* (8 / 512 / 64 gone)
  and *"Buffered LEDs on top eight I/O pins"* survives only because "eight" is spelled out.
  **Consequences:** (1) the LED pin map sat as `TBD` in `hardware/p2-eval-board.yaml` for
  months while the answer was in the repo (F-248) — no grep for `P56` could hit a document
  with no digits; (2) **every** voltage, current, capacity, pin number, part number and page
  reference sourced from this extraction is suspect; (3) the extraction audit and
  cross-source analysis both list "LED pins" as a *gap*, so the loss was mistaken for the
  source being silent. **→ TRACKED → ingestion:** re-ingest this source with forced OCR,
  re-verify every numeric claim already derived from it, and — the general lesson —
  **add a digit-density sanity check to the ingestion pass**: a hardware document whose
  extraction is nearly digit-free has failed, not been read. Worth spot-checking the other
  board/hardware sources for the same font family. Status: `CONFIRMED`.

- **F-251 — the "why do the LEDs glow when I touch a pin" explanation must account for the
  LED BUFFER, and the freshly-shipped DeSilva v3.0.5 aside does not.** The #64000 guide
  (feature 12) and both Edge module YAMLs describe the onboard LEDs as **buffered** — the P2
  pin drives a buffer *input*, and the buffer drives the LED. DeSilva v3.0.5's new Chapter 1
  aside "Why Your LEDs Glow When You Touch Them" instead explains the effect as microamps
  coupling *through the LED itself*, which would produce a faint glow. On a buffered board
  the floating **buffer input** picks up the coupling and the buffer drives the LED at full
  strength — which matches the reader's actual report ("the leds will light up", not "glow
  faintly"). The aside's conclusion (floating pins have no opinion; drive them or use
  pull-ups) is right; the mechanism is wrong. **→ manual head:** correct the aside in the
  next DeSilva patch. Also worth stating there that on the #64000 **P58-P63 are shared with
  the USB-data and memory signals**, so those LEDs are active at power-up and after reset by
  design — a second, entirely non-mysterious reason a reader sees lit LEDs. Status:
  `CONFIRMED`.

- **F-252 — the Getting Started guide hardcodes `LED = 56` with no board caveat (same class
  as the DeSilva fix).** `p2-getting-started-guide/opus-master/getting-started-body.md:558`
  declares `LED = 56  ' the pin our LED is on`, used by the blink examples at `:493` and
  `:408`. On a **P2 Edge 32MB PSRAM Module** P56 is the PSRAM **clock** — the example lights
  nothing and drives the memory bus; the LEDs there are **P38/P39**. This is exactly the
  failure a reader hit this session, and it lands in the guide most likely to be a
  newcomer's *first* P2 program. **Fix:** one line naming the per-board LED pins (the
  DeSilva Ch.1 aside is the model, but Getting Started wants a single sentence, not a
  sidetrack). Sources now in the KB: `hardware/edge-standard-module.yaml` (P56/P57),
  `hardware/edge-32mb-module.yaml` (P38/P39), `hardware/p2-eval-board.yaml` (P56-P63,
  P56/P57 free). **→ manual head.** Surfaced by the v1.16.2 YAML→Manual impact survey.
  Status: `CONFIRMED`.

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

> **KB APPLIED 2026-07-11 — PUBLISHED in KB v1.15.0.** Both facets landed. `logic.yaml` — `packed:` gains the
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

> **YAML APPLIED 2026-07-11 — PUBLISHED in KB v1.15.0.** `plot.yaml:62` POLAR now reads "*Orientation:
> theta=0 points East (+x); with the default (positive) twopi the angle increases counter-clockwise;
> a NEGATIVE twopi reverses the sweep to clockwise*" — the murky `"twopi -1/0"` shorthand is gone.
> Manual side already applied (#195). Grounded EF-032/Test J.

**Manual side (→ ch05-post #195-C):** add the same orientation fact to the ch05-plot.md POLAR section — re-scoped from "optional enhancement" to **required gap-fill**.

**Grounding:** Test J (empirical > documentary). Cite the EF once promoted.

## YAML additions & enrichments (gaps) — G-001…G-005

> **Surfaced by the Titus rev5 cross-source Q&A + IOSP cross-audit (2026-06-12/13).** These are **additions** (content the KB does not yet carry), not corrections — filed here so the v1.10.1 sweep executes them alongside the F-corrections. G-001 was previously named only in the head dashboards; now formally logged. Per-item gating noted; the gated parts do **not** block the rest.

### G-004 — `architecture/smart-pins/smart-pin-11011-usb-host-device.yaml` X/Y/Z registers were one-line stubs — `CONFIRMED — content COMPLETE; one YAML edit owed (remove the shipped open_questions block)`

> **Rewritten in place 2026-08-15. There is nothing Chip-gated here, and there never really was**
> (Stephen, 2026-08-15). The "gated remainder" was *receiver analog front-end detail and the exact
> electrical thresholds of the J/K/SE0/SE1 line-state detectors.* Those are **electrical
> characteristics, not programming facts** — out of scope for this KB. A programmer using the USB
> smart-pin mode sets baud / host-device / FS-LS, sends line states, and reads the 16-bit status
> word, all of which shipped 2026-06-20. Anyone needing a comparator threshold wants the datasheet,
> not us. So the content is complete and this is no longer PARTIAL on any gate.
>
> **What IS owed, and it is a defect rather than a gap:** the file ships an `open_questions:` block
> (`:60-64`) announcing what we do not know. In an **agent-consumed** deliverable that is a hedge in
> the one place hedges are unusable — an agent cannot act on it, it reads as a gap in the *P2* rather
> than in *our sourcing*, and it invites a later fill-in from inference. A class-wide sweep found it
> is the **only** such block in `deliverables/ai/P2/`, so it is an outlier, not a convention.
> **Correction:** delete the block; if anything replaces it, a one-line pointer that electrical
> characteristics live in the datasheet — a *routing* statement, which is legitimate, rather than an
> *unknown* statement, which is not. Rides this sprint's YAML patch release.
>
> **Note the precedent one entry below.** G-005 sat "OPEN pending hardware" while the hardware answer
> had been on the ledger since 2026-06-17. Both entries were stale rather than blocked, and the
> 2026-06-20 archival deferral was conditioned on exactly these two.
> **APPLIED 2026-06-20 (provable part):** replaced the one-line X/Y/Z stubs with the full Silicon-confirmable register layer — WXPIN config word (D[15] host/device, D[14] FS/LS, D[13:0] baud = 16-bit sysclk fraction, two MSBs 0), WYPIN line-state D-values (0=IDLE, 1=SE0, 2=K, 3=J, 4=EOP, $80=SOP) + packet-send protocol, the 16-bit RX status word (all 10 documented bit-fields), and per-pin IN semantics (odd/DP = TX-buffer-empty; even/DM = RX-status-change; C = RX error). All WXPIN/WYPIN/RDPIN issued on the lower/even pin. Authority: Silicon `p2-documentation.txt:8886-9006` (verbatim). **STILL OPEN (Chip-gated):** logged an in-file `open_questions:` block — RX analog front-end / line-state detector thresholds / any scope-style filter taps are NOT in Silicon and remain in the expert queue. This finding stays PARTIAL.
- The USB-host/device mode carries no register detail. **Add the Silicon-Doc-confirmable layer now:** WXPIN config word (D[15]=host/device, D[14]=FS/LS, D[13:0]=baud), WYPIN line-state D-values (0=IDLE…$80=SOP), RX 16-bit status word, per-pin IN semantics (odd/DP = TX-buffer-empty, even/DM = RX-status-change). **Authority:** Silicon `p2-documentation.txt:8886–8960`. **Gated remainder:** any figure not in Silicon (e.g. scope-style filter taps) stays in the expert queue (Chip). (IOSP RA-38/40/42/43/46/47.)

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

### F-183 — count-mode *concise donors* (10100/10101/10110/10111) are broadly stale/divergent from published — `TRACKED → ingestion`
> Carved from F-176. The 4 donors carry undefined **mode-name** constants (`P_PERIODS_STATES`, `P_PERIODS_CLOCKS_TIME/STATES/PERIODS`) **and** a different mode taxonomy than the (hand-corrected) published files, on top of the now-removed `P_B_A_INPUT`. Published diverged from them long ago (proving the concise-YAML pipeline isn't re-run for these), so reseed-risk is currently latent. A **full donor↔published resync** (mode names + taxonomy) belongs to the ingestion/smart-pins-catalog head, not a published-YAML edit. Tracked, not release-blocking.

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

## XBYTE technique-mining sweep — reference implementations expose two doc defects (2026-07-14) — F-217, F-218

> **Origin.** Stephen asked for a per-processor "what will hurt when you emulate this" table in the XBYTE
> Guide, and proposed we ground it by studying **live, working emulators** rather than reasoning from ISA
> facts. The study immediately surfaced two defects. Full evidence ledger:
> `engineering/document-production/manuals/p2-xbyte-programming-guide/TECHNIQUE-MINING.md`
> (per-source, because the techniques enter the manual body *anonymously* — the ledger is the only place
> the lineage lives). **Note the path:** it lives at the manual **root**, not in `audit/`, because
> `.gitignore:175` ignores `manuals/*/audit/` — a durable source-of-record cannot live there.

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

## `architecture/xbyte_engine.yaml` — all three programming examples are broken (2026-07-14) — F-220…F-223

> **Origin.** Chasing an open question for the XBYTE Guide (*what does Chip's "no stack pop" mean?*), the
> authoritative KB entry `p2kbArchXbyteEngine` was consulted — and **every one of its three
> `programming_examples` is wrong.** This is the YAML an agent would use to generate XBYTE code.
> Ground truth used below: the **Silicon Doc** narrative + demo, **Chip's own Spin2 interpreter**,
> **Parallax's official `xbyte.spin2`**, plus Zog and the 8080 emulator — nine implementations, all
> agreeing. Evidence: `manuals/p2-xbyte-programming-guide/TECHNIQUE-MINING.md`.
>
> **File:** `deliverables/ai/P2/architecture/xbyte_engine.yaml`

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

**The fourth failure is a separate defect — see F-228.**

### F-228 — a display **named after a DEBUG keyword** is never declared; the window silently never opens — `DONE (2026-07-27, isolated on silicon)` · re-test pending

**Symptom** (Stephen, 2026-07-26/27, PNut/Windows): `ch14-scope-trace.spin2` opens its TERM
"Panel" window but **no SCOPE window**. The TERM create is issued *after* the SCOPE create, so the
program and the debug link are healthy — only the SCOPE create is rejected.

**Isolated by a six-way single-run probe** (`audit/verification-tests/probe-ch14-scope-create.spin2`),
built after a first pass produced an ambiguous count. Six SCOPE creates differing by one token
each; **A–E all opened, `Trace` did not**:

```spin2
debug(`SCOPE D     POS 0 0 SIZE 400 220 SAMPLES 256)   ' opened
debug(`SCOPE Trace POS 0 0 SIZE 400 220 SAMPLES 256)   ' did NOT open
```

Byte-identical apart from the name. `TRACE` is in the functional keyword vocabulary (SPECTRO/BITMAP
config). `parse_debug_string` classifies each element (`cmp al,dd_key`) before a name symbol can be
claimed, so a keyword token can never become a `dd_nam` — no display is declared, and every
`` `Trace … `` feed afterward addresses nothing. **No compile error.**

**Method note worth keeping.** The keyword hypothesis was raised early, then **correctly discarded**
when `figure-generators/screenshots/fig-14-scope-trace-scope_WDW.bmp` (2026-07-11) OCR'd as
*"Trace - SCOPE"* with channel "Signal" — a working window from this same create line. Only a
controlled probe *with a passing control* re-established it. Two runs, opposite results, same
source: the discriminator is which host rendered them (see the open question below), and neither
the screenshot nor the argument could settle it alone.

- **Fixed:** `ch14-scope-trace` display renamed `Trace` → `Scan` (example + opus-master code block +
  `fig-14-scope-trace.spin2`; SAVE filenames unchanged). Same class in prose: `` `PLOT Box `` in
  ch05 → `Canvas` (`BOX` is a PLOT shape directive).
- **Taught:** ch02 now carries the **complete five-part naming rule** with the silent-failure
  symptom; Appendix A points at it and states that the reserved set is wider than the appendix.
- **Definitive rules recorded (2026-07-27)** — Stephen commissioned an agent study of the **PNut
  v55** source and the result is now the citable reference:
  `manuals/p2-debug-window-manual/REF/DEBUG-WINDOW-NAME-RULES.md`. A name is legal iff: (1) leading
  letter/`_` then letters/digits/`_` — a leading digit parses as a *number* and aborts; (2) not one
  of the **103** reserved display words (`debug_symbols`, `p2com.asm:19335`) = 9 types + 11 colors
  (**`GREY` and `GRAY`**) + 19 color modes + 12 packed modes + 52 directives; (3) not a currently
  open display's name — freed and reusable after `CLOSE`; (4) **case-insensitive** matching, with
  original casing kept for display; (5) truncated at **30** characters, so shared 30-char prefixes
  collide. Mirrored into `statements/debug.yaml` `window_name_rules` (full 103 enumerated for code
  generation; count-verified).
- **Re-sweep against the full 103** (the earlier sweep used only the directive subset — it omitted
  the nine display types and `GREY`): across all 34 examples, the opus-master snippets, the figure
  generators and the probe, the only hits remain `Trace` and `Box`, both already fixed. No name
  exceeds 30 characters or starts with a digit.
- **Scope (Stephen, 2026-07-27) — two independent vocabularies, only one collides.** Spin2's
  reserved words are irrelevant: the compiler emits the display name as raw text and never
  interprets it. `ch05-plot-field.spin2` names a PLOT window `Field` — `FIELD` is a Spin2 keyword
  (the `FIELD[ptr]` alias, v37+) — and it runs correctly on his bench. Only the **host display
  parser's** directive vocabulary can collide. ch02 teaches the contrast with both examples.
- **Library sweep:** all display names across the 34 examples, the opus-master snippets and the
  figure generators were checked against the full keyword vocabulary — `Trace` and `Box` were the
  only two collisions, and both are fixed.

**Host divergence — Stephen's to carry (2026-07-27).** The Jul-11 capture proves this create line
rendered a window *then*, so a host accepted what PNut v55 rejects; the likely split is
`pnut_term_ts` (figure run) vs. PNut (the 2026-07-26 run). Per the standing rule (PNut is ground
truth, term-ts mirrors) that would be a term-ts repair item. **Stephen is handling it directly** —
no action or report from the doc side. The manual and KB fixes above stand regardless of which
host is at fault, because a keyword-named display is invalid against ground truth.

**Re-tested and closed (Stephen, 2026-07-27): the full 34-program example library runs under
PNut v55.** Ships in Debug Window Manual **v1.1.1** (released 2026-07-27) and KB **v1.15.0**.

**YAML→Manual impact survey (KB v1.15.0, release-yamls §8).** The delta (10 files: `pc_key`,
`pc_mouse`, `statements/debug`, 7 `debug-displays/*`) was intersected against every live manual's
`MANUAL-DESCRIPTOR.md` declared sources. **Two intersections, neither needing a re-audit flag:**
- `p2-debug-window-manual` — the consuming manual, whose twin **shipped simultaneously** (v1.1.1);
  it is the source of the delta, not a document lagging behind it.
- `pnut-term-ts-user-guide` — its descriptor declares an explicit **scope boundary** ("do NOT
  reproduce the `debug()` directive syntax … cross-reference only"), and it is an undrafted v0.1.0
  with no content, so nothing can be behind HEAD. No flag.

No other live manual declares these sources. Survey done, not skipped.

## Forum docs-feedback sweep (2026-08-14) — F-254…F-258

**Origin:** Parallax forum posts #104–#117 (2026-08-12/13), reviewing the deSilva tutorial, the
XBYTE Programming Guide, and the P2 Architect's Guide. Full analysis (with the tone/positioning
items that are *not* defects) lives at
`engineering/document-production/FORUM-NO-COMMMIT/Docs-findings-360813/DOCS-FINDINGS-ANALYSIS.md`
(gitignored — find it by path). Forum posts are the **lead**; every finding below was verified
against the live opus-master, `pnut-ts` 1.55.3, or P2KB before filing.

### F-254 — deSilva Acknowledgments: the author is listed among the "giants," reviewers are credited generically, and an AI claim is false. `CONFIRMED`

**Location:** `manuals/p2-pasm-desilva-style/opus-master/COMPLETE-OPUS-MASTER.md:113–160`.
**This is in a SHIPPED document (v3.0.5).** Three distinct defects in one block:

1. **Self-listing.** The section opens *"This manual stands on the shoulders of giants. We
   gratefully acknowledge:"* → `### Primary Contributors` → deSilva, **Iron Sheep Productions LLC
   (Stephen M Moraco)**, Chip Gracey. Structurally the text declares the giants and then lists the
   author among them. Raised by Christof Eb. (#109): *"Newton bows to other great scientists and
   makes himself small; Stephen has styled himself to be a giant here."* The idiom itself is
   canonical (AJL, #105, is right about that) — the defect is which side of it the author sits on.
   The Newton quote also appears **twice** (paraphrase at `:113`, quotation at `:154`).
2. **Unearned reviewer credit.** `### Technical Reviewers` — *"Special thanks to those who reviewed
   drafts, tested code examples, and provided invaluable feedback"* — lists only generic
   placeholders: *"The P2 Documentation Team at Parallax"*, *"Community members who beta-tested
   examples"*, *"Everyone who reported errors."* **No named person.** If that review did not occur
   as described, this claims a validation process we did not run — a trust-chain defect, not a
   style one.
3. **False factual claim.** *Production Notes* states the manual used *"AI-assisted content
   generation **trained on** deSilva's writing style."* **Nothing was trained.** The accurate
   statement is AI-assisted authorship *in the style of* deSilva's P1 tutorial, with every example
   compiled. Precision matters especially here — the same thread carries hostility about
   AI-generated content.

Also present and low-value: an `### Inspiration` block crediting the MIT AI Lab, Donald Knuth, and
the Demoscene, none of whom contributed to this work.

**Proposed correction** (essentially evanh's advice, #106 — *"delete the whole line, and the
'Primary Contributors' line too. Keep it formal. 'Acknowledgements' is all that's needed"*):
drop the giants opener and the closing Newton quote; drop the `Primary Contributors` heading;
**remove Iron Sheep / Stephen Moraco from the acknowledgments entirely** (the author belongs on the
title page); delete the Technical Reviewers block **unless real named reviewers can replace it**;
delete the Inspiration block; correct or delete the "trained on" sentence.

**Class-wide sweep — DONE TWICE, and the result is good news: this is ISOLATED to deSilva.**
The first pass swept deSilva's *wording*; the second swept the four *defect classes* independently,
across every manual and app-note opus-master, because matching strings is not the same as matching
the defect:

| Defect class | Swept for | Result |
|---|---|---|
| **Self-listing in acknowledgments** | `Iron Sheep`/`Moraco` outside copyright/trademark context | **deSilva `:119` only.** Every other hit is the cover byline `{\small Iron Sheep Productions, LLC\par}` (correct) or, in XBYTE `front-matter.md:153`, a *Sources* citation of our own P2KB YAML — honest provenance, not a thank-you. |
| **Unnamed / unearned reviewer credit** | `those who`, `beta.test`, `reviewers`, `reviewed drafts`, `tested code`, `everyone who`, `special thanks` | **deSilva `:129–135` only.** |
| **False AI-provenance claim** | `ai-assisted`, `ai-generated`, `trained on`, `LLM`, `large language model` | **deSilva `:150` only.** The Assembly Manual `front-matter.md:316` ("a format suited to both human reading and AI-assisted development") describes the *audience and format*, not how the text was produced — accurate, **leave it alone**. |
| **Padding credits** (parties with no connection to the work) | manual read of every acknowledgments block | **deSilva only** (MIT AI Lab, Knuth, Demoscene). |

**App-notes P2AN001–P2AN007 carry no acknowledgments section at all** — clean by absence.

All live manuals are already clean, formal, and correct —
Architect's, Assembly, XBYTE, IOSP, Getting Started, Debug Window, Streamer all credit Parallax,
Chip Gracey, the P2 community (and IOSP additionally Jon Titus) with no self-listing, no giants
line, no generic reviewer credits, no AI claim. deSilva is the **outlier**, consistent with it
being the oldest of the set — written before the house convention settled. Two further copies of the
text exist inside deSilva's own folder and are **inert** (not assembled into the render):
`opus-master/archived-2025/COMBINED-COMPLETE-MASTER.md` and
`initial-chapter-generation/00-acknowledgments.md`.

> **Sweep scope:** the **live set only** (roster Done / In progress / Upcoming). Roster-Abandoned
> documents are excluded from the search itself and are not reported on.

### F-255 — XBYTE §15.3: `set_nz` is never defined, and the contract shown cannot work. `CONFIRMED`

**Location:** `manuals/p2-xbyte-programming-guide/opus-master/xbyte-body.md:1388–1401`
(Christof's "page 66"). Guide is **in community review**.

Two representative handlers end with `_ret_ call #set_nz` — `op_lda_imm` after loading `a`, and
`op_inx` after incrementing `x`. **`set_nz` is never defined anywhere in the manual** (it appears
only at these two call sites plus prose mentions at `:879` and `:1293`). Worse than missing:
`:1293` asserts *"A single shared `set_nz` helper serves most of the instruction set,"* but the two
call sites require flags from **different registers** and the helper takes **no operand** — no
shared result register, no calling convention, nothing. As written the pattern cannot do what the
text claims. Christof's objection (*"how should that routine guess from what it could set the Z
flag?"*) is correct and unanswerable.

**Second defect, same section:** §15.3's closing paragraph credits the handlers with *"each
opcode's table entry supplying the SKIPF pattern"* — but **none of the three handlers shown carries
a skip pattern**. The examples do not demonstrate the mechanism the prose attributes to them.
(Christof: *"There is no skip pattern."*)

**Proposed correction:** define `set_nz` and make its calling convention explicit (shared result
register, or an operand), show at least one handler family with real skip patterns, and **compile
the slice**.

**Scope check — deliberately NOT inflated.** A sweep of every `call`/`jmp` target inside the
guide's PASM2 blocks found **12 of 13 undefined as labels** (`pop_two`, `push_a`, `push_value`,
`read_opcode`, `hub_write_port`, `next_op`, `idle`, `int_ignore`, `odd_variant`, `special_case`,
`voice_on`, `set_nz`). **Only `set_nz` is a defect.** The others are legitimate illustrative
stand-ins whose names fully convey their job and whose internals are irrelevant to the lesson.
`set_nz` differs because the *surrounding text makes a claim about the helper's shareability* — its
contract is load-bearing, so it cannot be a stand-in. **Do not "fix" the other eleven.**
Corroborating the guide is not broadly broken: the complete VM in §12.2 (`xbyte-body.md:975–1044`)
was extracted and **compiles clean** under `pnut-ts -q`.

### F-256 — `_RET_ CALL` is a load-bearing idiom in a shipped guide and its semantics are unverified. `NEEDS-VERIFICATION`

**Location:** `xbyte-body.md:879` (*"Chapter 15's `_RET_ CALL #set_nz` idiom depends entirely on
this"*), used at `:1391`, `:1400`, `:416`, `:793`.

Christof (#110) doubted *"you can combine a CALL with ret."* **Tested: `_ret_ call #set_nz`
assembles clean under `pnut-ts` 1.55.3**, and `language/pasm2/call.yaml:11` describes CALL paired
"with a `_RET_` condition" — so as stated the objection is wrong.

**But the compiler proves legality, not semantics.** The open question is what the hardware does
when one instruction both pushes a return address and returns: does control reach the helper and
then return to `$1FF` (XBYTE re-entry intact), or does the push/pop ordering break dispatch?
`architecture/xbyte_engine.yaml:71` is suggestive but addresses a *different* case (why a CALL
cannot substitute for `PUSH #$1FF` at arm time). **Not resolvable from the KB or the Silicon Doc;
no answer is asserted here.**

**Action:** jumper-free, single-board hardware test — arm XBYTE, run a handler ending in
`_RET_ CALL`, report whether dispatch continues. Ideal **VO-J** candidate; result goes to the EF
ledger either way. **A load-bearing idiom in a guide under community review must not stay
unverified.** If it fails, §15.3 and the Chapter 9 explanation both need rework.

### F-257 — deSilva Appendix A platform comparison omits the current competitor and the axis where we are weakest. `CONFIRMED`

**Location:** `COMPLETE-OPUS-MASTER.md:5876+`. **SHIPPED document.** Raised by Christof (#111).

- **RP2040/RP2350 (Raspberry Pi Pico 2 / 2 W) is absent.** The table lists STM32, ESP32,
  Arduino/AVR, PIC32, P2. The RP2350 is the current default for a large share of hobby projects and
  its PIO is the nearest real competitor to the P2's pin-level story. Omitting it reads as
  avoidance.
- **The comparison is hardware-only.** It compares cores, peripheral location, and timing, and
  never mentions **libraries, ecosystem, or language** — Arduino/ESP-IDF/MicroPython versus having
  to learn Spin2 + PASM2 is for many readers *the* deciding factor. A comparison that omits the
  axis where we are weakest invites the "marketing leaflet" charge Christof levels.
- **Pricing** (Edge modules) is unmentioned; independently echoed by evanh in a separate thread.

**Proposed correction — fix, do not delete.** Add the RP2350 row; add a software/ecosystem
dimension that states plainly where the P2 loses; keep the technical claims, which are accurate and
already properly hedged (the "2 clocks" passage correctly calls itself a lower bound). Consider
adopting Christof's own framing of the P2's strength, which is sharper than ours and comes from a
critic: *"the probability to succeed in a project is higher, because you can always fall back to
dedicate a core to some time critical part — much more easy than working with interrupts."*

## Community bench review — refaQtor, P2 Rev C @ 300 MHz (2026-08-14) — F-259…F-263

**Origin:** `p2-manuals-review-findings.md` (posted as `p2-manuals-review-findings.zip`, forum
#108), reviewing the manuals **as downloaded 2026-08-13**. Author states every claim has a
committed harness + log on **real P2 Rev C silicon at 300 MHz, pnut_ts 1.55**.

> **Trust note.** This is a *third party's* bench, not ours. It is far stronger than a forum
> opinion — reproducible rigs with logs — but it is **not** an accepted P2KB empirical finding and
> must **not** be written into `P2-EMPIRICAL-FINDINGS.md` as if it were our own test. Treat each
> claim as a **high-quality lead**: verify against our sources (done below), fix the documentation
> defect where the source proves it, and **replicate on our bench** anything we intend to cite as
> ground truth. His §5 "confirmations" are likewise corroboration, not EF entries.

**All five below are in RELEASED manuals.**

### F-259 — REVISED: the guide's DAC recipe is CORRECT. The real defect is composing pin constants with `+`. `CONFIRMED` (our bench)

> **REVISED 2026-08-14 after running it on our own board. The community report is NOT reproduced,
> and the original filing above was wrong to accept it.** Bench: P2 Edge, 200 MHz, jumper P0→P1
> (continuity verified digitally before measuring).

**What the silicon says.** Sweeping the TT field with the DAC driven to full scale by `SETDACS`:

| Configuration | ADC counts |
|---|---|
| `TT=%00` (no drive) | 1,408 |
| **`TT=%01` (`P_CHANNEL`) — the guide's recipe** | **6,733 — DRIVES** |
| `TT=%10` (`P_BITDAC`) | 1,406 |
| `TT=%11` | 1,406 |
| `TT=%01`, OUT=1 | 6,735 (OUT is irrelevant) |
| **`P_CHANNEL + P_OE` composed with `+`** | **1,406 — DEAD** |

So `wrpin ##P_DAC_124R_3V + P_CHANNEL` **works as published**. The reporter's claim that it "leaves
the pin at ground" does not reproduce.

**Why his bench disagreed — the source explains it.** Spin2 v55's symbol table lists, under a group
headed **"DIR/OUT Control (pick one)"**:

```
%..._01_00000_0  P_TT_01
%..._01_00000_0  P_OE        Enable output in smart pin mode, regardless of DIR
%..._01_00000_0  P_CHANNEL   Enable DAC channel in non-smart pin DAC mode
%..._10_00000_0  P_BITDAC
```

**`P_OE` and `P_CHANNEL` are the identical bit** — two names for `TT=%01`, chosen by context.
They are not additive flags; they are one *field*. Consequently `P_CHANNEL + P_OE` = `%01 + %01`
= **`%10` = `P_BITDAC`** — a different mode, which our bench shows is dead (1,406). The reporter's
own rows (*"TT=%10/%11 any → ground"*) match ours exactly; his **interpretation** — that `P_OE` is
required — is what is wrong. He was comparing `%01` against `%10`, not "without OE" against
"with OE".

**THE ACTUAL DEFECT: `+` composition.** With `|`, combining two names from one field is idempotent
and harmless. With `+` it **silently carries into a neighbouring mode**. Class-wide sweep of smart-pin
configuration lines (`WRPIN`/`PINSTART`) across every live manual, app-note, and the KB YAML:

| Operator | Config lines |
|---|---|
| `\|` | **281** |
| `+` | **2 — both in the Streamer Guide** |

- `streamer-body.md:1238` — `wrpin ##P_TRANSITION + P_OE, #spi_clk`
- `streamer-body.md:1306` — `wrpin ##P_DAC_124R_3V + P_CHANNEL, dac_pins`

Both **produce correct values today** (their terms are in disjoint fields, so `+` == `|` there), so
this is a latent trap rather than a live bug — but it is the trap that produced a public bug report
against us, because the moment a reader adds a second term from the same field the mode silently
changes.

**Proposed correction.**
1. Change both Streamer Guide lines to `|`, matching the 281 lines everywhere else.
2. State the house rule where readers will meet it: **compose pin/mode constants with `|`, never
   `+`** — the fields are "pick one", and `+` carries.
3. Add a note that **`P_OE` and `P_CHANNEL` are the same bit** (smart-pin vs non-smart-pin DAC
   naming), so "add `P_OE` as well" is at best redundant and, with `+`, destructive.
4. Re-examine `wrpin.yaml:49`'s `p_oe_required_for` listing DAC: correct in substance, but for the
   cog-DAC path the bit's name is `P_CHANNEL`, and the phrasing invites exactly the mistake above.

**Note for F-245's class:** that sweep's "add `P_OE`" remedy is right for *smart-pin output modes*.
It must **not** be applied mechanically to non-smart-pin cog-DAC configuration, where the same bit
is `P_CHANNEL` and adding a second name for it with `+` breaks the mode.

### F-260 — Streamer §17.1 DDS/Goertzel: the mode WORKS; the guide's text is the whole defect, plus a protocol it never states. `CONFIRMED` (doc defects, bench-settled 2026-08-14)

**Location:** `streamer-body.md:1324`, `:607`, `:990`. **RELEASED.**

> **Rewritten in place 2026-08-15.** This entry previously read `NEEDS-VERIFICATION (silicon)` and a
> second F-260 entry carrying the bench result had been appended ~100 lines below, so the register
> held two contradictory verdicts for one finding. One finding, one entry: the heading above is now
> the current verdict and the bench data is retained below as **evidence**, not as a second finding.
>
> **The silicon question is settled: the mode works and is sharply frequency-selective** — 411:1
> against a 2× detune, 3,700:1 against 0.5×, 2,460:1 null, with ADC density measured per row so no
> row can misreport its own input. **Do not present this mode as unbuildable.**
>
> **One correction to what the appended entry claimed.** It stated as measured fact that *"the
> Goertzel accumulators are never zeroed."* That is an over-reach and it is **not** the finding.
> What was measured, under a discrete `XINIT` → `WAITXFI` → `GETXACC` sequence: a fresh cog's first
> read equalled the previous cog's last read five times across `COGINIT`, and two identical commands
> returned exactly twice one command's total. Chip's shipped demo reads once per command in an
> `XCONT` loop and plots a live position — if nothing ever reset, his readings would ramp without
> bound, and they do not. **Author the protocol, never the mechanism:** read before the command,
> read after, take the difference. Which of `XINIT` vs `XCONT`, the wait, or the cog lifecycle
> accounts for the difference is **not established** and must not be asserted.
> Full graded write-up: `campaigns/2026-08-manual-corrections/BENCH-FINDINGS-FOR-AUTHORING.md` Test 5.

Two **confirmed documentation defects**, both verified in source:

1. **`:1324` — `xcont dds_cmd, dds_s`. `dds_s` is never declared.** It appears exactly once in the
   entire guide. The example cannot be assembled as printed.
2. **The ADC-pin field contradicts itself.** `:607` (`add cmd, ##adc_pin<<17 + 1024`) and `:990`
   (`mode := X_DDS_GOERTZEL_SINC1 | X_DACS_0N0_0N0 + adc_pin<<17 + cycles`) place the ADC pin at
   `<<17`, which **collides with the required config bits `%111` in D[18:16]**.

**Plus an unresolved silicon question.** With the pin path proven good by `SETDACS` (F-259), the
reporter built the command exactly per the guide and Assembly App. G — it runs (`WAITXFI` completes
on schedule) but **drives no DAC and accumulates nothing**. Swept without success: `%dddd` ∈
{1,2,4,8}, D[19] 0/1, D[23] set, accumulators read mid-run and after `WAITXFI`.

Three questions the guide must answer and currently cannot:
- exact `XINIT`/`XCONT` **S-operand semantics** for this mode;
- which field enumerates the **summed ADC pin(s)** ("m = ±1 per selected ADC pin, −3..+3");
- whether anything beyond the command word must be armed (`SETCMOD`? DAC channel enables?).

**Action:** fix the two doc defects now. The silicon behavior needs our own bench and, if it stays
unresolved, becomes a **question for Chip** (`DRAFTS/QUESTIONS-FOR-CHIP-GRACEY.md`). Until settled,
the guide should not present this mode as buildable. A verbatim, compile-tested, silicon-run
example would close all three questions at once.

### F-261 — IOSP Guide still says power groups of **four**; we corrected this to **eight** in the KB a month ago. `CONFIRMED`

**Location:** `manuals/p2-io-and-smart-pins-user-guide/opus-master/part-3-input-modes/chapter-16-adc.md:263`
and `:382`. **RELEASED.**

Both passages state *"isolated groups of **four** — pins 0–3, 4–7, 8–11, …, 60–63."* The truth,
settled in **F-211** (`DONE — YAML applied 2026-07-11, PUBLISHED in KB v1.15.0`), is **8 groups of
8** (P0–7 … P56–63). The reporter caught it as a **contradiction against our own P2AN001**, which
correctly says eight.

**F-211's class-wide sweep covered the YAML and missed the manuals.** That is the precise failure
our class-wide-sweep rule exists to prevent, and it shipped.

Three distinct repairs, not one:
- `:263` — group size and the boundary list (`0–3, 4–7…` → `0–7, 8–15…`).
- `:263`/`:382` — the **layout rule** built on it. With wrong boundaries the advice actively
  misleads: it implies pins 3/4 straddle a domain when in fact 7/8 do.
- `:382` — the **worked example's reasoning is wrong**: *"spans pins 40–47 — two full groups
  (40–43, 44–47)"*. Pins 40–47 are **one** group. The conclusion ("fine, channels are independent")
  survives; the reasoning does not.

**Class-wide sweep — DONE.** Grepped every live manual and app-note opus-master for the 4-group
wording and boundary lists: **only these two locations.** (One unrelated "group of four bits"
false positive in the Assembly manual's MERGEB description — not this defect, do not touch.)

### F-262 — Debug Window Manual: the FFT chapter never states channel-definition defaults that the SCOPE chapter does. `CONFIRMED`

**Location:** `manuals/p2-debug-window-manual/opus-master/ch09-fft.md` vs `ch07-scope.md:86`.
**RELEASED.**

`ch07-scope.md:86` gives a proper `| Argument | Meaning | **If omitted** |` table. `ch09-fft.md` has
no "If omitted" column anywhere — its `:73` table gives defaults for *keywords* (`TEXTSIZE` etc.)
but never for the **channel-definition arguments** (`high`/`tall`). The manual says the arguments
are optional and then does not say what happens when they are omitted, so an implementer must guess.

The reporter identifies this as the plausible cause of a **pnut-term-ts strict-parser divergence**
he field-reported separately — i.e. this gap has already produced a real tool disagreement.

**Proposed correction:** copy SCOPE's "If omitted" column into the FFT chapter's channel-definition
table. **Verify the values against PNut** (ground truth) rather than assuming FFT matches SCOPE.

### F-263 — CONFIRMED with the cause identified: hub access inside a CORDIC loop loses results. Chip's model is correct. `CONFIRMED` (our bench, 2026-08-14)

**Our board, our measurement.** P2 Edge @ 200 MHz. Control: queue one op, retrieve immediately —
stalled **58 clocks**, exactly the documented `GETQX` maximum (`2...58`), so the rig can see the
failure mode. Four shapes swept over fill depth 1–7, checked against single-op `ROTXY` ground truth:

| Shape | Hub access inside a CORDIC loop? | First failure |
|---|---|---|
| **ARM B** — P2AN002's shape (`RDLONG` in the fill) | fill | **FILL = 2** |
| **ARM C** — register-only fill, `WRLONG` in the drain | drain | **FILL = 3** |
| **ARM D** — register-only fill **and** drain, hub I/O batched after | none | **CLEAN THROUGH 7** |
| ARM A — Assembly ch.5 shape (2×`RDLONG` + `CALL`/`RET` per issue) | fill | 15 of 16 wrong at FILL=6 |

**Chip's clarification is vindicated.** Deep pipelining works — 6–7 operations in flight is real, and
`GETQX`/`GETQY` stall correctly. **The rule is: no hub access inside either CORDIC loop.** Issue and
retrieve at the 8-clock slot cadence; batch hub reads and writes outside. Break it in the fill and
you lose results from the fill onward; break it in the drain and you lose them from the drain onward.

**The community report is right in effect and wrong in cause.** It is not a 2-deep result buffer —
it is a fill/drain that cannot keep up with the pipeline. (Supporting evidence: the ARM B failure
depth **moved between otherwise identical runs** — FILL=3 in one, FILL=2 in another. A fixed
hardware buffer depth would be deterministic; a timing race is not.)

**Both of our documents are wrong, for exactly this reason:**

- **`app-notes/P2AN002/examples-library/cordic-pipeline-throughput.spin2` (RELEASED)** — `rdlong t, inp`
  inside the fill loop, `wrlong r, outp` inside the steady loop.
- **`manuals/p2-assembly-language-manual/.../chapter-05-hardware.md:~100–126` (RELEASED)** — the
  `queue_rotation` helper does **two** `RDLONG`s plus a `CALL`/`RET` per issue, and the steady loop
  does two `WRLONG`s per retrieval. Slower than ARM B, and it measures worst of all.

**Proposed correction (same fix for both):** hoist hub I/O out of the CORDIC loops — block-read the
inputs into cog registers first (or compute them in-register), keep fill and drain to
register-only operations, then block-write the results afterwards. State the rule explicitly next
to the example, because the pattern *looks* correct and fails silently with plausible-looking
numbers.

**EF candidate:** this belongs in `P2-EMPIRICAL-FINDINGS.md` — our own board, our own probe, with a
control that stalled at the documented maximum. Probe:
`campaigns/2026-08-manual-corrections/tests/test-f263-cordic-pipeline-depth.spin2`.

#### Bench evidence for F-260 — session of 2026-08-14

*(Evidence for the F-260 entry above, not a second finding. Retained verbatim except that its
"the accumulators are never zeroed" mechanism claim is corrected in that entry — see the note there.)*

**Bench result (P2 Edge 200 MHz, jumper pin 0 -> pin 1, `test-f260-goertzel-input.spin2` BUILD 11):**

| arm | ADC density | delta cos | delta sin | magnitude |
|-----|-------------|-----------|-----------|-----------|
| on-target, 1 MHz detector, 1 MHz tone | 1020/2000 | 1,051,655 | -124,573 | **1,059,000** |
| detuned, 2 MHz detector | 1021/2000 | -1,865 | 1,775 | 2,575 |
| detuned, 500 kHz detector | 1020/2000 | 207 | -198 | 286 |
| no tone, driven pin | 349/2000 | -409 | 134 | 430 |

Identical densities across the three tone rows, so the only variable is the detector
frequency. **Selectivity 411:1 against the 2x detune, 3,700:1 against the 0.5x detune, and a
2,460:1 null.** The DDS/Goertzel mode detects and is frequency-selective.

**THE PROTOCOL THE GUIDE NEVER STATES, and the reason 20+ probe rounds read flat:**
**the Goertzel accumulators are never zeroed.** A fresh cog inherits the previous cog's value
(measured: each SEQ pass's pre-command read equalled the previous pass's last read, five times
running, across `COGINIT`), and successive commands ADD (measured: two identical commands gave
exactly twice one command's total). So an absolute `GETXACC` read is meaningless. **Read before
the command, read after, and take the difference.** This is precisely what Chip's shipped
`Goertzel_DEBUG_Demo.spin2` does with its `xcal`/`ycal` subtraction -- that calibration removes
the inherited baseline, not an analog offset.

**Field semantics, all confirmed against Chip's shipped demo and our bench:**
`pppp`x4 = base pin of the four-pin input block (`base<<17` is his own idiom, valid because the
base is a multiple of four); `S[15:12]` = sum-select, `S[19:16]` = invert-select, `S[11:0]` =
loop size + LUT window; NCO scale is 2^31; DAC output inverts each LUT byte's MSB; and in
`DAC_MODE` with `TT=%01`, `M[3:0]` selects **which cog's** DAC channels drive the pin (his
`setnib dacmode,cogid,#2`) -- the pin's low two bits pick the channel.

**Corrections for the guide** (all still required; the working mode does not excuse them):
1. `:1324` `dds_s` undeclared -- and S is mandatory, since `S[15:12]` selects which ADC pins are
   summed. `S = 0` sums nothing.
2. `:990` / `:607` `adc_pin<<17` is correct **only** when `adc_pin` is a multiple of 4, because
   `(adc_pin>>2)<<19 == adc_pin<<17` exactly then. The field names a four-pin BLOCK.
3. The section must state the read-before/read-after protocol above.

### F-266 — the debug interrupt disrupts the streamer, and `DEBUG_COGS` defaults to ALL cogs. `CONFIRMED` (our bench, 2026-08-14)

**Location:** Streamer Guide (no warning anywhere) + KB gap.

`p2kbArchDebugInterrupt` already records it under `limitations`: *"streamer_interaction: Debug can
disrupt streamer operations. Workaround: Disable debug when using streamer."* And
`DEBUG_COGS` defaults to `%11111111` -- every cog has debug capability at runtime.

**Measured cost:** with `-d` and the default mask, our streamer probe crashed into the
single-step debugger's memory dump, and its Goertzel accumulators read 1,000,000-7,000,000 of
pure corruption. Setting `DEBUG_COGS = %0000_0001` (report from cog 0 only) stopped the crash,
made the launched cogs' `CogN INIT` lines disappear, and collapsed the accumulators to their
true small values. Every streamer measurement taken before that fix was confounded.

**Why it matters to a reader:** anyone debugging streamer code with `-d` -- the normal way to
debug -- has the P2's highest-priority interrupt live inside their streaming cog by default, and
nothing in the guide warns them. **Action:** warn in the Streamer Guide, and surface the
existing KB limitation where a streamer author will meet it.

### F-264 — `wrpin.yaml`'s `tt_field` flattens four context-dependent `%TT` meanings into one, and tells readers to add `P_OE` to DAC outputs where it breaks them. `CONFIRMED` (source-verified + bench-corroborated, 2026-08-14)

**Location:** `language/spin2/methods/wrpin.yaml` — the `tt_field` block. **RELEASED.**

**The Silicon Doc specifies `%TT` as four different meaning-sets**, selected by whether the smart pin
is on and whether `DAC_MODE` (`M[12:10] = %101`) is active — `part4-locks.txt:118-139` and
`p2-documentation.txt:7646-7660`. For **smart pin off**:

| `%TT` | non-`DAC_MODE` | **`DAC_MODE`** |
|-------|----------------|----------------|
| `%00` | OUT drives output | **OUT enables ADC, `M[7:0]` sets DAC level** |
| `%01` | OUT drives output | **OUT enables ADC, `M[3:0]` selects cog DAC channel** |
| `%10` | OTHER drives output | OUT drives BIT_DAC |
| `%11` | OTHER drives output | OTHER drives BIT_DAC |

**Our KB already carries this correctly** in `architecture/smart_pins.yaml:249-253`, verbatim.
`wrpin.yaml`'s `tt_field` does not: it gives one context-free effect per value — `P_TT_01:
"Output enabled regardless of DIR, SMART/OUT drives"` — which is the smart-pin-**on**, non-DAC
meaning presented as *the* meaning. Its only route to the truth is a `see_also` pointer.

**Two concrete harms:**

1. **`p_oe_required_for: "All output modes (NCO, PWM, Pulse, Transition, Serial TX, DAC, USB)"`
   is wrong for the non-smart-pin DAC.** There `P_OE`/`P_CHANNEL` is not an enable at all — it
   switches the DAC's source from the pin's own level field to a cog DAC channel. Applying the
   F-245 "add `P_OE`" remedy to a level-driven DAC **kills the output**. Measured on our bench
   the same day: a `P_DAC_124R_3V` pin driven from its level field read a spread of **1,305** of
   2,000 samples; adding `P_CHANNEL` dropped it to **25**.
2. **An agent reading `wrpin.yaml` alone builds a wrong model of DAC pins.** This is not
   hypothetical — it produced two successive wrong hypotheses during the 2026-08 bench campaign
   before `architecture/smart_pins.yaml` was consulted.

**Correction:** make `tt_field` state that `%TT` is context-dependent, name the four contexts, and
qualify `p_oe_required_for` to smart-pin output modes — with the `DAC_MODE`/smart-pin-off row
called out explicitly, since that is the cog-DAC and streamer-override case. Keep the full table
in `architecture/smart_pins.yaml` as the single source; `wrpin.yaml` needs enough to stop a reader
concluding the wrong thing without following the pointer.

**Note the shape:** this is F-245 and F-259 one level up. Both were resolved *against this file*,
and this file was incomplete on exactly the axis that mattered.

**Status:** `NOTED` 2026-08-14, resolution deferred until the bench campaign closes (Stephen's
standing rule: no doc/YAML editing until every bench question is conclusive).

### F-265 — the Silicon Doc contradicts itself on whether Goertzel ADC pins are smart pins; the KB must state the resolved answer. `CONFIRMED — answer settled 2026-08-14; KB statement still owed`

> **Rewritten in place 2026-08-15.** This read `NEEDS-VERIFICATION` while the answer had already been
> established on the bench — and while this register's own header line had it right. The contradiction
> was internal to this file.
>
> **The answer: the ADC pin is RAW** — `P_ADC_x` with smart-pin mode `%00000` and **no DIR**. The
> DDS/Goertzel section of the Silicon Doc is authoritative; the STREAMER intro's *"smart pins
> configured as ADC's"* is loose wording. Confirmed by our own working probe and by Chip's shipped
> demo (`campaigns/2026-08-manual-corrections/BENCH-FINDINGS-FOR-AUTHORING.md` Test 5).
>
> **Why this stays open:** the *fact* is settled; the *KB statement* is not written. A reader landing
> on the intro still configures a smart pin and gets nothing. Owed: state the resolved answer in
> `architecture/streamer/dds-goertzel.yaml` **and** name the tension so the intro's wording cannot
> re-mislead. Closes when that lands.

**Location:** KB gap — `architecture/streamer/dds-goertzel.yaml` (and the Streamer Guide's §17.1).

- Silicon Doc STREAMER intro (`part2-pixel-ops.txt:82`): the streamer can *"perform Goertzel
  computations from **smart pins configured as ADC's**."*
- Silicon Doc DDS/Goertzel section (`part2-more-content.txt:176`): the pins *"should be configured
  for ADC mode, so that their IN signals are raw delta-sigma bit streams, **with no smart pin mode
  selected**."*

These cannot both be operative. The detailed section is the more specific statement and is what our
probe follows (`P_ADC_1X`, smart-pin mode `%00000`), and the Silicon Doc's own worked example uses
`wrpin adcmode,#adcpin` with mode field `%00000` — which supports the detailed section. But the KB
currently says nothing about the tension, so a reader who lands on the intro will configure a smart
pin and get nothing.

**Action:** settle it with a bench arm (cheap — run the DDS/Goertzel arm both ways), then state the
answer in the KB and the guide rather than leaving the reader to reconcile two sources.

**Status:** `NOTED` 2026-08-14, arm to be added to the F-260 probe; resolution after the bench
campaign closes.


---

*Move-aside 2026-06-13 after the v1.9.0 release closed out F-001..F-124. The archive holds the full history; this active register carries only the carry-forward guardrails and the ingestion-tracked items. New findings continue at F-125.*

