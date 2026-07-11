# Fleet PDF Release — Execution Sprint Plan

**As of:** 2026-07-10 · **Owner:** Stephen · **Author:** Claire
**End goal:** documentation fleet PDF update — re-render + re-release every manual
carrying the fabrication-audit sweeps and the Debug-Window example corrections.
**Supersedes:** `FABRICATION-AUDIT-AND-CORRECTNESS-SWEEP-SPRINT-PLAN.md` (2026-07-09, pre-A–H).
**Anchors:** `RELEASE-ROADMAP-fabaudit-plus-debug-2026-07-10.md`,
`FABRICATION-AUDIT-SWEEP-CATALOG.md`, `PUBLICATION-ROSTER.md`,
`p2-debug-window-manual/audit/v55-vs-REF-reconciliation-2026-07-10.md`.

This is a **plan** (ship commitment), not a study. It is organized so `plan-to-tasks`
can map one task-group per numbered section.

---

## 0. Preflight — commit pending work (clean tree) FIRST

Before any new editing, the working tree must be clean. Current state (audited 2026-07-10):
- **Layer 1 — §6 sweep (342 fixes):** already committed `f3e702ed`.
- **Layer 2 — Debug example fixes: APPLIED but UNCOMMITTED** — 14 `examples-library/*.spin2` +
  8 Debug `opus-master/*.md` + F-204 entries in `P2KB-CORRECTION-FINDINGS.md` /
  `FABRICATION-AUDIT-SWEEP-CATALOG.md`, plus the new ch15 assets (`digits.bmp`, `panel_bg.bmp`,
  `ch15-panel-plot-bmp-spec.md`) and this plan doc.
- **Layer 3 — today's research (A–H, fanout survivors, F-205, Sweep B):** not applied.

**Action:** commit **Layer 2** as a scoped, surgical commit (correction work + ch15 assets +
planning docs) — **excluding** compiled `.bin` artifacts, `OBEX/`, and `presentation/` (unrelated /
build outputs). This gives a clean baseline before Layer-3 editing begins. On `main`
(`feedback_no_branching_work_on_main`).

**Entry baseline (baseline-health, 2026-07-10 — yaml:p2kb head):** ✅ **GREEN.** Per the
baseline-health overlay's real coverage map: `verify-yaml-format.py` 1129/1129 parsed clean;
`validate-crossref-keys.py` 100% resolved; `validate-dod-release.py` ALL PASS (lone benign ⚠️ = 3
keys with valid-Spin2-symbol special chars). Zero warnings, zero failures, zero skips — this is the
protection point the sprint climbs from; the §9 KB track must exit no worse.

---

## 1. The spine — manual × front touch matrix + render-readiness

Three fronts feed the fleet, but **release is per-manual**, so the governing rule is:
**finalize each manual completely across all fronts, then render it once** (`document-finalize`
gather-then-resolve + Sacred Rule #6 changed-files-only + no double-render).

Key fact: **§6 (342 fabrication/factual fixes) is committed (`f3e702ed`) to opus-masters but
NOT yet rendered/released.** So the wave re-renders every §6-touched manual (12 of 13; P2AN006
had zero survivors). Most of them need **no further edits** — they are render-ready today.

| Manual | Sweep A residual | Sweep B (doc) | Debug track | Render-ready? |
|--------|------------------|---------------|-------------|---------------|
| Getting Started | — | — | — | ✅ **now** |
| DeSilva | — | — | — | ✅ **now** |
| Streamer | — | — | — | ✅ **now** |
| Architect's Guide | — | — | — | ✅ **now** |
| P2AN001–005 (5) | — | — | — | ✅ **now** |
| P2AN006 | — (no §6 change) | — | — | ⏸ no re-release needed |
| **IOSP** | C-23 ENOB re-check, C-65 rdpin C-bit, skip §12.3 | — | — | ⚠ after §2 (light) |
| **Assembly** | C-56 AUG, C-09 eggbeater | 2 files (~83 occ) | — | ⚠ after §2+§3 |
| **Debug Window** | C-19, C-247, C-249, skip ch05-POS, F-205a | — | **HEAVY** (§4+§5) | ⛔ after §4+§5 |

**Master sequence (Stephen, Q2 = one focused campaign, NOT rolling releases):** interim per-manual
releases would divert focus from the core goal — clean, complete correction of *all* sources — so run
this as a single campaign in three steps:
1. **Push through ALL manual fixes** — every front, every manual; get all ducks in a row (Layer-3
   edits §2–§5 + the hardware-gated ones §6). **No PDF yet.**
2. **Cooperative audit** (§7.5) — visual inspection + cooperative discovery across all fixed manuals;
   nothing renders until this clears.
3. **Render the WHOLE fleet to PDF** at the end (§8), all known clean+correct, and **release together**
   (§9). The YAML/KB track (Sweep B YAMLs + F-204) lands in the same coordinated release.

Sweep B **doc** impact is confined to **Assembly only** (every other manual's `=` hits are
config/state prose, out of scope) — so no other manual's render is gated by Sweep B.

---

## 2. Sweep A residual — manual correction edits (IOSP, Assembly, Debug)

Only three manuals carry un-applied Sweep-A work. Base §6 text is already committed; these are
**refinements / the 2 genuine skips / the F-205 item**, not from-scratch applies.

**2a. Assembly** (both hardware-confirmed today, see reconciliation doc):
- **C-56** AUG survives an intervening instruction → apply in ch02 §2.7.3 with the **ALTx
  refinement** wording (AUGS/AUGD queue for the next matching `#S`/`#D`; an intervening `ALTx`
  with its own immediate *uses* but does not *cancel* the augment). Source: catalog C-56, silicon
  test G, catalog draft #644.
- **C-09** scalar RDLONG blocks (egg-beater) → **add** the egg-beater narrative in ch04 **§4.6.3
  (FIFO/burst context)**, explicitly distinguishing streaming (1 long/clock) from scalar (blocks
  ~9–16 clk); leave §4.6.2's scalar correction as committed. Source: catalog C-09, silicon test H.
- *Verification:* prose renders; §3.4.4/§4.6.2 already-correct rows still agree; no new unsourced claim.

**2b. IOSP:**
- **C-23** ENOB terminology re-check — **must not re-introduce "ENOB"** removed in IOSP v1.0.3
  (`project_adc_enob_correction_thread`). Confirm the committed wording is clean; no edit if so.
- **C-65** rdpin() Spin2-vs-PASM2 C-bit caution — verify the committed note reads correctly.
- §12.3 `P_LOGIC_B_FB` — **(C, Stephen Q3): rework the subsection to teach it correctly.** The
  current comment "Same, different internal routing" is false (it's the **B input**, not A, and
  **feedback** output). Rework to teach the two axes — **input source A vs B** and **output OUT vs
  feedback** — clearing the misconception. **Must be grounded:** pull the exact A/B input-selector
  semantics from the **Silicon Doc smart-pin input-routing** (not only the constant table), so we
  don't trade a vague comment for a confident-but-wrong teaching (`feedback_no_unsourced_claims`).

**2c. Debug Window** (non-example corrections — see also §5):
- **C-19** green/lime — now **empirically settled** (test A: default = clLime $00FF00 exact;
  GREEN kw = $09FF09). Apply the #250 reader-note polish (keep "Lime"; note no `LIME` keyword,
  `GREEN` reproduces near-identical $09FF09).
- **C-247** stray-ellipsis / Spin2 line-continuation, **C-249** term-default POS auto-place —
  reconcile against REF (both low-risk).
- **F-205a (weight)** — **now UNBLOCKED by test D**: "$00 = light" is refuted ($00 renders
  identically to $01). Correct/remove that claim. **F-205b (alignment 2/3 swap)** remains — test
  D exercised only the weight bits; see Open Q 1.
- **Genuine skip** ch05 POS default 'auto' vs '0,0' — needs Stephen's call (Open Q).

*Verification (all 2x):* each corrected claim re-verifies vs its now-trusted source; zip↔manual
identity preserved for any example touched.

---

## 3. Sweep B — operator notation `=` → `==` (plan-gated)

Rule (`feedback_behavior_notation_vs_code_operators`): comparison predicates `=` → `==`; LEAVE
"receives"/assignment `=`; bare `=` in Spin2 CODE → `:=`/`==`; PASM2 CON `=` stays. Add a short
behavior-notation legend to the affected manual section(s).

**3a. Docs (Assembly only) — apply directly (small, self-contained):**
| file | ~occ | notes |
|------|------|-------|
| `p2-assembly-language-manual/opus-master/part-iii/appendix-a-encoding-table.md` | ~70 | Z-column: 57 `Result = 0`, + masked/double-compare rows; legend line is a style call |
| `p2-assembly-language-manual/opus-master/part-i/chapter-03-flags.md` | ~13 | flag-effect rows; leave in-code-comment/prose `Z=1`/`C=0` state lines |

**3b. YAMLs — PLAN-GATED (overlay: 3+ YAML files → file table + flagged decisions + wait for
per-decision confirmation BEFORE any edit).**

*File table (67 files, ~79 occ — `deliverables/ai/P2/language/pasm2/`):*
| grouping | files | occ | edit |
|----------|-------|-----|------|
| bulk single `z: Result = 0` | 57 | 57 | uniform `= 0` → `== 0` |
| double `z:` compare (abs, encod, neg, negc, negnc, negnz, negz, not, ones, test) | 10 | 20 | 2 each |
| `z: (D = 0) \| (S = 0)` (mul, muls) | (subset) | +2 | 2 each |

*Design decisions to flag (confirm each with Stephen before editing):*
- **D1** — the ~10 non-uniform rows (`z: D=S` in cmp/cmps/cmpm; `(D=0)|(S=0)` mul/muls; masked
  `(D & S)=0`/`(D & !S)=0`/`z: D=0`; `Z AND (Result=0)`) — confirm each is a *compare* → `==`.
- **D2** — the **6 EXCLUDED lines** (sumz, sumnz, sumc, sumnc, incmod = receives/assignment;
  cmpsub `=>` is the ≥ operator) — confirm we LEAVE them.
- **D3** — legend/prose lines (appendix-A legend; §18.8-class `OUT=`) — confirm out-of-scope
  (Open Q 5).
- After edits: `validate-yaml-syntax` + `validate-crossref-keys` + index regen (Path-B two-commit,
  `reference_index_generator_post_commit`).

**Gate:** the 3b YAML table + D1–D3 go to Stephen for sign-off (batched with §6 hardware session);
no YAML edit starts until confirmed.

---

## 4. Debug Window — example lifecycle (the cross-tool conformance track)

**Why heavier:** the example library is the reference corpus Prop Tool IDE (Parallax/Italy) and
PNut-Term-TS validate their DEBUG renderers against, alongside PNut. Its lifecycle must be airtight.
Current state: loose `.spin2` == manual code blocks (fixed) **≠ `examples-library.zip` (stale,
23/32 differ, dated Jun 24)** — the ZIP still ships pre-fix broken code. Re-zip is the
highest-leverage item, but it must come **last** (after every fix lands) so it ships complete.

**GOLDEN SOURCE — the hardware-tested figure-generators.** This manual's chapter figures were
produced by `figure-generators/fig-*.spin2` (14 files, ch03–ch11), which **already ran on real
hardware** and emitted the published screenshots. Each shipped example *should* be its
fig-generator minus a known tail block (`waitms` + `save '<name>'` + `save window '<name>_WDW'` +
`close` + `DEBUG_END_SESSION`). **They are the trusted baseline** (`reference_pnut_is_ground_truth`).
Verified today that several shipped examples **diverged beyond the tail** — ch10 (`RANGE $40000`+
inline-PASM vs tested `RANGE 500`+`qsin`), ch06 (added `TRIGGER` + per-channel colors vs tested
`COLOR WHITE GRAY`) — and those untested divergences are the defects. **Strategy: reconcile each
ch03–ch11 example TO its fig-generator, not patch the diverged copy** (see Stage 3). This gives most
of the corpus hardware-tested provenance and shrinks the from-scratch hardware run to the no-fig
chapters only.

**Stage 1 — Coverage.** Every taught window has ≥1 example (no orphan-teaching). Empirically
**ungrounded** surfaces (zero figure history) = **PC_KEY / PC_MOUSE** (ch12, ch15-control-panel),
**LUT/LUTCOLORS** (ch13), **LAYER/external-BMP** (ch15-panel-plot). The hardware run-list (§6)
must prioritize these — they are exactly what the Italy team will exercise.

**Stage 2 — Fixes INTO the examples** (apply to loose `.spin2` **and** manual code block together):
- ch10-spectro-runup: **`RANGE $40000` → `RANGE 500`** (tone won't saturate at $40000) — *not yet
  applied*.
- ch15-panel-plot: BMP assets — **DONE 2026-07-10** (`panel_bg.bmp` 200×96, `digits.bmp` 300×48
  placed in `examples-library/`; seam-rule verified `BOX_BG=#0A0A0A` byte-identical).
- Already fixed in loose+manual (need only the re-zip to propagate): ch06-logic-spi-bus, ch07-scope-
  three-channel, ch13-packed-bitmap-frame (LUT1+LUTCOLORS), ch13-packed-scope, ch14-scope-trace,
  ch14-multiwindow, ch14-pasm-scope.
- Fanout code-adjacent APPLY items: A32 (ch06 %1011 LSB-first labels), A33 (ch06 stray `...`),
  A34 (ch13 LUT/packing width pairing) — apply with the §5 batch.

**Stage 3 — Reconcile to tested figs, then hardware-run only the gaps** (batched in §6):
- **ch03–ch11 (have a tested fig-generator): reconcile, don't re-test.** For each shipped example,
  diff against its `fig-*.spin2`; where it diverges beyond the known tail block, **revert to the
  fig behavior** (the tested truth: ch10 → `RANGE 500`; ch06 → drop the untested `TRIGGER`/per-channel
  colors or mark them for re-test). Result: these examples inherit hardware-tested behavior with **no
  new hardware run** required. Any divergence Stephen wants to KEEP for pedagogy must be **re-run on
  hardware** before it ships (it was never tested).
- **ch01, ch02, ch12, ch13, ch14, ch15 (NO fig-generator): fresh hardware run required.** These are
  the real run-list. Capture figures where screenshot-able; for the **interactive** ch12 PC_KEY /
  PC_MOUSE + ch15-control-panel, run and confirm behavior as a pass/fail **observation**, not a
  figure (Open Q 4). This set also holds the empirically-ungrounded surfaces (PC_KEY/PC_MOUSE, LUT,
  LAYER) the Italy team leans on — prioritize them.
- Bring ch01/02/12–15 under the same fig-style run+screenshot+`DEBUG_END_SESSION` harness (RC-2) so
  they gain fig-generators too and never ship unrun again.

**Stage 4 — Fixed examples BACK INTO the manual at byte-identity.** Loose already tracks the manual;
after any Stage-2/3 edit, re-confirm each touched example's code block matches its `.spin2` byte-for-byte.

**Stage 5 — Re-zip + persistent identity gate (§7).** Regenerate `examples-library.zip` from the
fixed loose files (exclude the stray `ch12-keyboard-adjust.bin`); then the identity check must pass
before Debug release.

---

## 5. Debug Window — non-example manual corrections (fanout + A–F reconciliation)

Separate from the examples: the prose/behavior backlog that gates Debug release.
- **Fanout survivors:** `audit/fanout-survivors-categorized-2026-07-10.md` = **42 APPLY / 21 DROP /
  34 BLOCKED**. Apply the 42; drop the 21.
- **A–F settlements now unblock much of the 34 BLOCKED** (all confirmed REF-wins, recorded in the
  reconciliation doc): C-R1/2/3 LOGIC ranges (F-206), C-R5 FFT filled-bars, C-R6 TERM Lime,
  C-R7 SCOPE 256, B26 MIDI rgb24 accepted. Re-triage the 34 against these results: the four
  **inversions** (filled-bars→lines, Lime→Green, 256→255, MIDI named-only) become **DROP**; the
  range/default items become **confirm-manual-correct** (no edit).
- **F-205 (both halves in one pass)** — apply weight + justification together **after Test I**
  confirms the justification mapping (Q1: test-first, one-pass fix).
- Keep zip↔manual identity for any example touched incidentally.

---

## 5.5. Conflict-closure register — every outstanding source conflict → resolution

Goal (per Stephen): **no v55-vs-REF or unanchored-source conflict left dangling.** Each resolves to
an existing test (A–H), a newly generated test (I/J), or a reasoned disposition.

| ID | Conflict | Resolution | Status |
|----|----------|------------|--------|
| C-R1/2/3 (F-206) | LOGIC LINESIZE/SAMPLES/SPACING ranges+defaults | Test C | ✅ REF/YAML win |
| C-R5 | FFT negative LINESIZE (bars vs lines) | Test B | ✅ filled bars |
| C-R6 | TERM default Lime vs Green | Test A | ✅ clLime $00FF00 |
| C-R7 | SCOPE default width 255 vs 256 | Test F | ✅ 256 |
| C-R8 | LINESIZE/DOTSIZE half-pixel | Test B/C | ✅ ruler confirmed |
| B26 | MIDI COLOR rgb24 accepted | Test E | ✅ accepted |
| #644 | AUG survives intervening instr | Test G | ✅ survives |
| #132 | egg-beater scalar-vs-stream | Test H | ✅ scalar blocks |
| F-205a | TEXTSTYLE weight ("$00=light") | Test D | ✅ $00==$01 (refuted) |
| **F-205b** | **TEXTSTYLE justification (2/3 swap, both axes)** | **Test I — RAN 2026-07-11** | ✅ HYBRID: horiz=v55 (%10=right/%11=left), vert=REF (%10=top/%11=bottom); render=truth |
| **POLAR-θ0** | **POLAR 0-direction + rotation sense (ch05 flip risk)** | **Test J — RAN 2026-07-11** | ✅ θ=0 East, +θ CCW, no flip |
| C-R4 | TEXTSIZE default "editor size" vs 10 | reasoned: 10 IS the editor default (matrix §7.0a); keep 10, note "(editor default)" | ✅ no test |
| idiom | SCOPE/FFT channel-def on create-line drops window | already observed via tested fig-07 (empty plot) + scope.yaml | ✅ existing fig |
| idiom | TERM text quoting `"…"` / `'…'` / `` `(expr) `` | existing `test1-term-string-quoting.spin2` (run if not yet) | ◑ test exists |
| F-204 | rdpin.yaml IN-flag-reset snippet (2 NOPs → 1) | **grounded — no new test**: IOSP §4.13 + v35 CSV (NOP=2 clk); RDPIN ack/reset mechanism hardware-confirmed **EF-015**. Apply the one-NOP YAML fix on the §9 track | ✅ resolved |

Only **two new tests (I, J)** were needed; both authored + compile clean with `pnut-ts -d`
(`verification-tests/conflict-testI-textstyle-justify.spin2`, `…-testJ-polar-theta0.spin2`).
**Every conflict now has a closure path with no dangling verification** — F-204 is grounded (fix
only), so nothing in the register is left "◑".

## 6. Batched Stephen session — hardware run-list + conflict tests + Sweep B sign-off (one session)

Three Stephen-gated items, none blocks the others → run together:
1. **Debug example run-list** — **only the no-fig chapters** (ch01, ch02, ch12, ch13, ch14, ch15)
   plus any ch03–ch11 divergence Stephen elects to keep (Stage 3). ch03–ch11 are otherwise reconciled
   to their tested fig-generators and need no run. Bracketed like A–H; prioritize the ungrounded
   PC_KEY/PC_MOUSE/LUT/LAYER surfaces; return figures + interactive pass/fail; use the RC-2
   save/`DEBUG_END_SESSION` harness so these chapters gain fig-generators.
2. **Conflict tests I + J** (the last two dangling source conflicts) — **Test I** TEXTSTYLE
   justification (F-205b: emits `textI_horiz.bmp` / `textI_vert.bmp`), **Test J** POLAR orientation
   (emits `polarJ_wheel.bmp`). Both bracketed/self-checking; Claire reads the BMPs and promotes to
   ground truth in the reconciliation doc, closing F-205 and the ch05 POLAR flip-risk.
3. **Sweep B YAML sign-off** — the §3b file table + D1–D3 decisions.

*(The electrical/jumper hardware is already drained — F-202/F-203 ADC = DONE→EF-024; VO-X items are
external-hardware, cataloged, not scheduled.)*

---

## 7. Persistent identity gate

Promote the throwaway `identity_check.py` (gone from scratchpad) into a **persistent, re-runnable**
checker + report (a `document-finalize`/`prepare-manual` step or repo script): asserts every
`examples-library/*.spin2` is byte-identical to its `opus-master` code block. Run it before the
re-zip (§4 Stage 5) and as a Debug release gate. Prevents silent corpus drift for external tools.

---

## 7.5. Cooperative audit (HARD gate before any PDF — fleet-wide)

After **all** manual fixes land (§2–§6) and are committed, Stephen and Claire do **one cooperative
audit pass across all fixed manuals** — visual inspection + cooperative discovery of the accumulated
diff since last public release (manual prose/content AND example code). **No PDF is generated until
this clears for the whole fleet** (Q2: single campaign, not per-wave).
- Present per manual: the full diff (git range) with the correction rationale/source for each hunk,
  for visual inspection; surface anything ambiguous for cooperative discovery.
- Anything rejected loops back to §2–§6 (fix), re-commit, re-present — never carried into render.
- Rationale: one focused sign-off that every source was corrected cleanly, so the fleet renders
  known-clean (`document-finalize` gather-then-resolve; "complete over partial").

## 7.6. Master hardware-test catalog — promote A–J into the versioned ledger

**Gap found (Stephen, 2026-07-10):** every hardware/render test that yields grounding must stay
**versioned** as one master catalog, so any future challenge to a claim answers with "here's the
test, here's the result — and if it's not complete enough, here's how we extend it." Today the
**silicon/smart-pin tests are versioned** (`hardware-verification/P2-EMPIRICAL-FINDINGS.md`, EF-NNN +
`VERIFICATION-OPPORTUNITIES.md`), but the **DEBUG-window render tests (A–H, and I/J when run) + the
reconciliation live only in the gitignored `audit/` workspace** — not durable. That's the risk:
these A–H results ground the whole sprint, yet aren't in the versioned ledger.

Deliverable:
- **Make `P2-EMPIRICAL-FINDINGS.md` the single master hardware-test catalog** — DEBUG-window render
  tests are first-class alongside silicon/log tests (both are hardware tests). Add a glanceable index
  row per test: ID · what · why · result · status.
- **Promote A–H (and I/J after §6) to EF-NNN entries** — each carrying what/why/result/grounding + a
  pointer to the regenerable `.spin2` (the test source is the versioned artifact; BMP/log regenerable).
  Cite these EFs wherever a manual/YAML change grounds on them.
- **Standing discipline (memory):** no grounding result stays only in a gitignored workspace — every
  test that changes what we know graduates to the ledger.

## 8. Render wave (Phase 3 — NO release yet)

Per touched manual: `prepare-manual` (refresh workspace FROM opus-master, escape LaTeX, stage
**only changed files**) → Stephen generates PDF on Forge → **verify each render** (page count,
outline, key sections, compile log; guard silent content-drop, `reference_forge_silent_content_drop`).
Wave-staging: shortest first; a changed shared common-named file rides **one** manual only
(`feedback_wave_staging_order_and_shared_once`).

All rendering happens **after** the §7.5 cooperative audit clears for the whole fleet — then the
**entire fleet renders and releases together** (Q2 = one fleet moment). Render order is only an
internal efficiency choice (lightest-first: the 9 content-final manuals, then IOSP → Assembly →
Debug); it is **not** separate release waves — all ship in the one coordinated release (§9).

## 9. Release wave (Phase 4) + YAML/KB track

- **Per doc:** `release-manual` — verify PDF, promote CHANGELOG, update deliverables README +
  force-download links, Platform Freshness Ledger PUBLISH line, roster status. Publish each Debug
  example ZIP beside its PDF + roster link.
- **Version policy:** already-released docs get one minor/patch bump per cycle
  (`feedback_no_double_bump_between_releases`); in-dev docs absorb with no bump. P2AN006: no change
  → no re-release (Open Q 2).
- **§9 YAML/KB track (separate rail):** after §3b sign-off + edits — validators green + index regen
  + `p2kb_refresh` + MCP restart + content-probe + `validate-dod-release`; number/timing per
  `release-yamls`. F-204 (rdpin.yaml NOP) rides this track (IOSP doc text already correct → no
  manual edit).
- Update the community-review announcement post (new rows/blurbs).

---

## Open Questions (each carries a recommendation)

1. **F-205 — RESOLVED (Stephen): do NOT split.** Run **Test I** in today's §6 batch for the
   justification answer, then apply **both** halves (weight + justification) in **one** documentation
   pass over the TEXTSTYLE section (`ch05-plot.md` + `plot.yaml`). Test first; both fixes together.
   Rationale: the hardware runs today anyway, so waiting on Test I is no real delay, and one clean
   pass beats a double-touch.
2. **Release cadence — RESOLVED (Stephen): A, one fleet moment.** Run as a single focused campaign:
   (1) push all manual fixes, (2) cooperative audit, (3) render the whole fleet to PDF at the end and
   release together — no interim per-manual releases (they'd divert focus from clean-correct-all-
   sources). Re-render+release all 12; **P2AN006 left as-is** (no §6 change, no bump).
3. **IOSP §12.3 `P_LOGIC_B_FB` — RESOLVED (Stephen): C, rework to teach it correctly.** Not just
   fix the "Same, different routing" comment — teach the A/B-input and OUT/feedback axes so the
   misconception is dissolved. Grounded in Silicon Doc smart-pin input-routing + the manual's own
   constant tables (see §2b); no unsourced claims.
4. **Interactive example grounding — RESOLVED (Stephen): certify against proven reference code +
   event-log.** ch12 PC_KEY/PC_MOUSE + ch15-control-panel can't be screenshotted, so grounding is a
   **combination**, evidence-typed per item:
   - **structural-vs-reference** — contrast each example against the hardware-proven, freshly-certified
     `REF/robot-dog/test_dog_panel.spin2` (production 3-cog interactive panel; bench-confirmed
     2026-06-06). It pins the idioms: `pc_key(@one_long)` LAST-in-windowed-DEBUG + edge-detect;
     `pc_mouse(@mx)` filling **7 consecutive longs** LAST-in-stmt; PLOT mouse **bottom-left/Y-up →
     flip `py`** vs top-left artwork; PLOT+layers+`crop`-blit+`hitSlot`+telemetry for the panel. The
     robot-dog panel is richer than the PNut-ts regression control-panel, so it alone suffices (no
     second anchor needed). Reference is cited (external material), NOT committed into our tree.
   - **event-log** — flip the `DEBUG[DBG_INPUT]` channel on (channel-gated `DEBUG_MASK`; a clear bit
     compiles to zero code) so Stephen's run emits a re-readable keystroke/click log I read back.
   - **visual position cross-check** (mouse) — confirm the drawn pointer lands where the reported
     coordinate says, in the window's frame.
   Two hard checks this enables on our examples (not a rubber-stamp): does ch12-mouse-pointer declare
   **7 consecutive longs**, and does it **flip Y**? A miss is a real bug. *Accepted:* structural-vs-
   reference + event-log (+ visual cross-check) is sufficient conformance evidence for the interactive
   corpus, each ✓ tagged with its evidence type in the run-list.
5. **Sweep B boundary cases — RESOLVED (Stephen): sign off all three as written in §3b.**
   D1 (10 non-uniform compare rows → `==`) — genuine comparisons (`D=S`, `(D=0)|(S=0)`, masked
   `(D & S)=0`, `Z AND (Result=0)`), Z receives a comparison result → make inner `==` explicit.
   D2 (6 excluded lines: `sumz`/`sumnz`/`sumc`/`sumnc`/`incmod` receives-assignment + `cmpsub` `=>`
   the ≥ operator) → **LEAVE** (editing would inject a false compare — correctness guardrail).
   D3 (appendix-A legend + §18.8-class `OUT=` pin-state prose) → **out of scope** (not predicates).
   Hand-checked each against the receives-vs-compare rule; no per-line diff requested. Rides the §6
   batched session, then YAML edits proceed with validate-yaml-syntax + validate-crossref-keys +
   Path-B index regen.

6. **ch03–ch11 divergence disposition — RESOLVED (Stephen): revert-to-tested is the default; KEEP
   ch06.** Blanket rule = reconcile every divergence to the hardware-tested fig behavior. Dispositions:
   - **ch10-spectro-runup** → REVERT `RANGE $40000` → **`RANGE 500`** (the $40000 blanks the display —
     straight bug, no upside).
   - **ch03-term-dashboard** → REVERT to fig-03 (define the `BACKCOLOR/COLOR` scheme on the create line;
     the divergence leaned on figure-defined pairs it never set — incomplete form).
   - **ch15-dashboard** → REVERT (same color-pair class as ch03).
   - **ch06-logic-spi-bus** → **KEEP** the `TRIGGER` + per-channel colors (genuinely better pedagogy:
     a triggered, color-coded SPI bus trace) → **joins the §6 hardware run-list** for a fresh capture
     (cost is one extra screenshot in an already-scheduled session). The RC-1 `...` create-line fix
     applies regardless. **Figure refresh (Stephen): since we're re-running anyway, ALSO grab the new
     image and update the manual's ch06 LOGIC figure to the pedagogically-better trace** — cheap, and
     the reader then sees the improved version. (Fully compatible with the invariant below: the figure
     swap is optional polish; the binding rule is still file↔code-block parity.)

   **SCOPE CLARIFICATION (Stephen) — the example-corpus conformance invariant:** the binding
   requirement is **external example file ≡ the manual's code block for that example (byte-identical)**,
   NOT rendered-image ≡ published-manual-figure. An example whose produced image differs slightly from
   the figure shown in the manual is fine — examples convey information and are useful in their own
   right. What must hold: when the manual *speaks of* an example, the file the reader downloads matches
   the code the manual shows. Consequence for KEEP-ch06 (and any kept divergence): we need a **passing
   hardware capture** proving it runs; we do NOT also have to replace the manual's figure or force the
   code back to match the old figure. Stage 4 byte-identity = file↔code-block, not render↔figure.

**Q1–Q6 ALL RESOLVED.** No open questions remain — the plan is decision-complete.
Next step: **plan-to-tasks → execute.** (See §6 hardware run-list, now including KEEP-ch06's
`TRIGGER`+colors re-capture; §3b YAML sign-off done; interactive certification method fixed per Q4.)
*(F-204 is NOT among them — grounded by IOSP §4.13 + CSV + EF-015; needs only the one-NOP YAML edit
on the §9 track, no verification.)*

---

## Section ↔ task cross-reference (generated by plan-to-tasks 2026-07-10)

Sprint tag: **`fleet-release`** · 15 tasks, `seq` 1–15 (foundational → dependent). Per-task detail
docs intentionally off (`TASK_DETAIL_DIR` unset) — the todo-mcp task ledger carries all context.

| Plan § | Deliverable | Task | seq |
|--------|-------------|------|-----|
| §0 | Preflight commit (clean tree) | — | **done** — `e0817b0a` (Layer 2) + `2cdb5d7b` (plan) |
| §1 | The spine — touch matrix / render-readiness | — | governing context (not a task) |
| §2a | Assembly manual Sweep-A residual (C-56, C-09) | «#187» | 1 |
| §2b | IOSP Sweep-A residual + §12.3 rework-to-teach | «#188» | 2 |
| §3a | Assembly Sweep-B operator-notation (docs) | «#189» | 3 |
| §5 + §2c | Debug non-example prose corrections (fanout 42 + A–F re-triage + C-19/247/249) | «#190» | 4 |
| §7 | Persistent example-corpus identity gate (tool) | «#191» | 5 |
| §4 Stage 2+3 | Debug example reconciliation to tested figs | «#192» | 6 |
| §3b + F-204 | KB-rail YAML edits (operator sweep + rdpin NOP) | «#179» | 7 |
| §6 prep | Hardware run-list package (harness + Q4 hard-checks) | «#193» | 8 |
| §6 run | Stephen hardware session + Claire promotion | «#194» | 9 |
| §2c/§5 F-205 + §5.5 POLAR | ch05-plot post-hardware corrections | «#195» | 10 |
| §7.6 | Master hardware-test catalog (A–J → EF ledger) | «#196» | 11 |
| §4 Stage 5 | Re-zip + identity gate | «#197» | 12 |
| §7.5 | Cooperative fleet audit (HARD gate before PDF) | «#198» | 13 |
| §8 | Render wave (no release) | «#180» | 14 |
| §9 | Release wave + KB release | «#181» | 15 |

**Prior work already completed (recorded, not re-tasked):** old fabrication-audit §5 fan-out
(«#177», `2c6ebc75`), §6 class-wide sweep A / 342 fixes («#178», `f3e702ed`), and the A–H
conflict-test hardware run («#186»). §5.5 conflict-closure register is context (all 16 closed;
I/J run in §6). This plan **supersedes** `FABRICATION-AUDIT-AND-CORRECTNESS-SWEEP-SPRINT-PLAN.md`;
its §7/§8/§9 tasks were re-scoped in place to «#179»/«#180»/«#181».
