# Release Roadmap — Fabrication-Audit Program + Debug-Window Customer Thread

**As of:** 2026-07-10
**Goal:** re-release the fleet of manuals carrying (a) the fabrication-audit correctness sweeps
and (b) the Debug Window Manual example-ZIP customer corrections.
**Scope (13 docs):** Getting Started, IOSP, Assembly, DeSilva, Debug Window, Streamer,
Architect's Guide, P2AN001–006. (AI Privacy Guide excluded.)
**Cross-refs:** `FABRICATION-AUDIT-SWEEP-CATALOG.md` (master confirmed-corrections list),
`FABRICATION-AUDIT-AND-CORRECTNESS-SWEEP-SPRINT-PLAN.md`, `P2KB-CORRECTION-FINDINGS.md`
(F-201…F-205), each manual's `audit/fanout-findings-2026-07-10.md`.

---

## DONE (baseline — do not redo)
- **§5 fan-out audit** — all 13 docs audited (adversarial-verified survivor sets).
- **§6 correctness sweep A** — 342 fabrication/factual fixes across 13 docs, committed `f3e702ed`.
- **Debug example ZIP customer thread** — 8 structural fixes (`...`-removal, SCOPE create-line
  splits, LUT2→LUT1); **all 32 examples compile clean AND are byte-identical to their manual
  code blocks** (identity script); BMP spec handed off; F-205 conflict logged.

---

## PHASE 0 — Resolve open questions / verifications (GATES editing)

### 0a. Source conflicts & doc-only verifications (I can drive; some need raw Pascal)
- **F-205 — TEXTSTYLE justification v55-vs-REF inversion** → needs raw `DebugDisplayUnit.pas`
  or hardware. **BLOCKS** the pending TEXTSTYLE manual correction.
- **TEXTSIZE default** (REF const 10 vs v55 "editor text size") → reconcile (maybe layering).
- **Systematic v55-text-vs-REF debug reconciliation pass** — may surface more conflicts; run
  BEFORE applying any broader debug fan-out finding. Rule: **REF (PNut source) wins on conflict.**
- **ch05 POLAR theta-0 orientation** → anchor to REF `PLOT_Theory §4.1` polar math (or gauge
  screenshot). Currently an unanchored comment (flip risk).
- **Catalog TODOs (7):** #296 ENOB (C-23 must be REVISED — would re-introduce "ENOB" removed in
  IOSP v1.0.3); #132 eggbeater narrative source; #644 AUG 2nd source; #736 rdpin() Spin2-vs-PASM2
  C-bit nuance; #250 green/lime vs pnut-ts-facts; #2558/#2580 already resolved (support our fixes).

### 0b. Hardware-gated (Stephen — no GUI in container)
- **Debug bounded run-list:** 9 fixed examples (confirm) + 3 PC_KEY/PC_MOUSE (ch12×2,
  ch15-control-panel — form correct per YAML+REF, RUN don't edit) + 10 never-run examples.
- **ch10 SPECTRO RANGE** value tune.
- **F-202** ADC gain-range centered endpoints (hardware campaign).
- **F-203** 14 CONFIRMED_WRONG + 8 AT_RISK quantitative hardware tables (fixes in progress).
- **F-204** rdpin.yaml NOP count (verify RDPIN IN-flag reset latency vs Silicon/pnut_ts).

---

## PHASE 1 — Editing (opus-masters + YAMLs)

### 1a. Debug Window manual
- Apply the **97 fan-out survivors** (`audit/fanout-findings-2026-07-10.md`) — mostly PROSE/
  behavior/table (TEXTSIZE default, scope buffer-depth wording, MIDI behavior). **Reconcile each
  vs REF first** (Phase 0a). Skip anything F-205-blocked.
- ch05 POLAR comment (after 0a anchor). Keep **zip↔manual identity** for every example touched.
- Confirm "ride-next-regen" items already in opus-master (F-136 done; F-138 ch09 snippet — verify).

### 1b. Fleet — remaining catalog corrections
- Apply remaining **`FABRICATION-AUDIT-SWEEP-CATALOG.md`** confirmed entries (C-NNN) not covered
  by §6, across all 13 docs. Resolve the embedded TODOs (0a) before applying the affected entries.

### 1c. §7 — Class-wide correctness sweep B (operator notation) — NOT STARTED, PLAN-GATED
- Rule: comparison predicates `=`→`==`; leave "receives" `=`; Spin2-code bare `=`→`:=`/`==`;
  PASM2 CON `=` stays. Add a behavior-notation legend to affected manuals.
- **YAML side (~61 files): plan-gated** — build the file table AFTER a fresh all-docs grep, then
  **confirm per-occurrence decisions with Stephen BEFORE any YAML edit** (`feedback_plan_before_yaml_changes`).
- Then validators + crossref + index regen (Path-B two-commit).

---

## PHASE 2 — Build / run code
- **ch15 BMPs:** generate from spec → drop into `examples-library/` → **re-zip** `examples-library.zip`.
- **Re-zip** the debug ZIP only after BMPs land (so it ships complete).
- Run the Phase-0b hardware list; fold any newly-found defects back into Phase 1 (keep identity).
- Any OTHER manual whose example code/ZIP changed → build + run.

---

## PHASE 3 — Re-render (§8, NO release yet)
- Per touched manual: `prepare-manual` (refresh workspace FROM opus-master, escape LaTeX, stage
  ONLY changed files) → Stephen generates PDF on Forge → **verify each render** (page count,
  outline, key sections, compile log — guard silent content-drop, `reference_forge_silent_content_drop`).
- Wave staging: shortest manual first; a changed shared common-named file rides ONE manual only
  (`feedback_wave_staging_order_and_shared_once`).

---

## PHASE 4 — Release (§8 close + §9 + release-manual)
- **Version policy:** already-released docs get a **minor/patch bump** (one bump per cycle,
  `feedback_no_double_bump_between_releases`); in-dev docs (Architect's Guide, IOSP pilots) absorb
  with NO bump.
- **Per doc:** `release-manual` — verify PDF, promote CHANGELOG, update deliverables README +
  force-download links, Platform Freshness Ledger PUBLISH line, roster status. Publish each
  example-library ZIP beside its PDF + roster link.
- **§9 YAML release (separate KB track):** validators green + index regen + `p2kb_refresh` + MCP
  restart + content-probe + `validate-dod-release`; number/timing per `release-yamls`.
- Update the community-review announcement post (new rows/blurbs).

---

## CROSS-CUTTING / process (fold in with the work that revealed them)
- **Standing zip↔manual identity gate** — promote `scratchpad/identity_check.py` into a real
  validator (or a `prepare-manual` step) so example/manual can never silently re-drift.
- **REF-wins-on-conflict rule** — document that debug findings reconcile against REF (PNut source)
  before applying; v55 text loses on conflict.
- **RC-2 tested-pipeline process fix** — examples must round-trip through a run-harness
  (SAVE + DEBUG_END_SESSION + screenshot) so no example ships unrun again.

## Task-tracker mapping
Existing todo-mcp tasks cover the fabrication phases: `#178` §6 (done-ish), `#179` §7,
`#180` §8, `#181` §9. The **Debug customer thread + REF/F-205 work is NOT yet tracked** — add
tasks if we want it in the register.
