# Sprint Closeout — Smart-Pin ADC Foundation + P2AN000 Instrumentation-ADC App Note

**Closed:** 2026-06-28 · **Plan:** `SMART-PIN-ADC-FOUNDATION-AND-P2AN000-SPRINT-PLAN.md` (this folder)
**Sprint tag:** `smartpin-adc` · **Tasks:** #121–#128 (all complete)
**Heads touched:** yaml (P2KB) · ingestion (donor hygiene) · manual (IOSP enrichment, app-note class) · operations (corrections register, validator)

---

## Verdict

**CERTIFIED — all commitments SHIPPED.** Every numbered plan section is shipped and verified against current code; §2 was an accepted DROP (Green Book retired). Exit baseline is GREEN with no regression vs. entry.

---

## Cross-reference reconciliation

The plan's §↔task table reconciled cleanly both directions — every numbered section maps to a real task and every task maps to a section. No stale rows.

| Plan § | Deliverable | Task | Status |
|---|---|---|---|
| §1 | Fix ADC X[5:4] encoding at the donor + verify-lock published YAMLs | #121 | **SHIPPED** |
| §2 | ~~`P_ADC_CAL` reconcile~~ | — | **DROPPED** (accepted, D1) |
| §3 | Durable guard (F-170 + `audit-adc-encoding.py`) | #122 | **SHIPPED** |
| §4 | Un-stale the IOSP encoding audit note | #123 | **SHIPPED** |
| §5 | IOSP Ch.16 foundation enrichment (4 additions) | #124 | **SHIPPED** |
| §6a | P2AN000 — base build + harness + concept | #127 | **SHIPPED** |
| §6b | P2AN000 — catalog + recipes + verify + close | #128 | **SHIPPED** |
| §7 | Dual-archetype app-note guide update | #125 | **SHIPPED** |
| §8 | Rig spec + measurement-table stub | #126 | **SHIPPED** |

---

## Per-section verification (file:line)

**§1 — ADC encoding fixed at root + verify-lock.** Donor now silicon-correct:
`engineering/ingestion/smart-pins-catalog/ingestionSources/mode-11000-adc-internal-clock/smart-pin-11000-adc-internal-clock-concise.yaml:26-27,153-154` (`%00 SINC2 sampling … %01 SINC2 filtering`). Published `deliverables/ai/P2/architecture/smart-pins/smart-pin-11000-adc-internal-clock.yaml:26-28` correct; siblings 11001/11010 confirmed consistent. Commit `e8b89b08`.

**§3 — durable guard.** `engineering/tools/validation/audit-adc-encoding.py` exists and **runs PASS (exit 0)** — asserts donor == published == silicon for the X[5:4] map (11010 correctly map-exempt). `F-170` recorded `DONE` at `engineering/operations/P2KB-CORRECTION-FINDINGS.md:395-403` with the donor root-cause narrative + fix-trace. Skill-evolution candidate (release-yamls pre-publish assertion) appended to the in-repo `feedback_skill_evolution_candidates.md` per D2 (central skill not edited). Commit `e8b89b08`.

**§4 — IOSP audit note un-staled.** `…/p2-io-and-smart-pins-user-guide/audit/titus-cross-audit-2026-06-12.md:1656` now reads "now ✅RESOLVED (v1.9.0, 2026-06-13; root-cause guarded 2026-06-28, see F-170)". Commit `e8b89b08`.

**§5 — IOSP Ch.16 enrichment (4 additions).** All present in `…/opus-master/part-3-input-modes/chapter-16-adc.md`: instrumentation-ceiling note (`:106`), source-switch-flush vs warm-up separation (`:192`), Ratiometric Absolute-Voltage Instrumentation subsection (`:209`), hardware-limits incl. ~15 mV absolute-error floor (`:563`). Ratiometric snippet uses `muldiv64`; compiles. Commit `e8b89b08`.

**§6a — P2AN000 foundation.** `engineering/document-production/app-notes/P2AN000/opus-master/P2AN000.md` — front matter, Abstract, What-You'll-Build, Prerequisites/Hardware, The Idea, short How-It-Works (→ IOSP Ch.16), shared harness (DEBUG SCOPE µV + DAC loopback), single-pin base build. Commit `629558d3`.

**§6b — P2AN000 catalog + close.** Same file — decision table, five recipes, 8-pin capstone (described/linked), consolidated Verify, Pitfalls, Conclusion, Resources, References, Revision History (v0.1.0). Commit `c6e0a032`.

**§7 — dual-archetype guide.** `engineering/document-production/app-notes/APP-NOTE-CREATION-GUIDE.md` §1.1 "Two archetypes" + two guardrails + decomposition rule; checklist updated; guide v1.1. Commit `6d126852`.

**§8 — rig spec + measurement stub.** `engineering/document-production/app-notes/P2AN000/P2AN000-NOTES.md` — rig tiers (0/1/2), measurement-table stub, per-recipe test procedure. Commit `6d126852`; traceability extended `c6e0a032`.

---

## Verification mode (honest statement)

- **Code:** every P2AN000 program **compiles clean under `pnut_ts` 1.55 with `-d` at `_clkfreq = 200_000_000`**; all code lines ≤ K=76. Integrity-checked by extracting each complete program from the markdown and recompiling. Idioms validated against the P2KB **first**, then the compiler.
- **NOT yet hardware-verified.** Every ENOB / accuracy claim is **qualitative, pending a Tier-1 rig run** (per the §8 measurement stub). No empirical numbers are asserted.
- **P2AN000 is v0.1.0 draft — NOT released.** PDF production (`prepare-manual` → Forge) has not been run; that path for the app-note class is an open design question (see carryover).

---

## Exit baseline (YAML head)

| Check | Entry (plan) | Exit (2026-06-28) | Verdict |
|---|---|---|---|
| `verify-yaml-format.py` | 1053/1053 parse clean | **1053/1053 parse clean** | ✅ no change |
| `validate-crossref-keys.py` | all resolved | **all resolved** | ✅ no change |
| `audit-adc-encoding.py` (new) | n/a | **PASS (exit 0)** | ✅ new guard green |

No regression. Closeout leaves the YAML head GREEN — the known-good start point for the next sprint.

---

## Carryover / follow-ups (specific)

1. **App-note → PDF production path is undefined.** P2AN000 has no `prepare-manual`/workspace wiring, no template/cover decision, no example-library ZIP convention. This is the next conversation (Stephen flagged it). Until resolved, the note stays a v0.1.0 opus-master draft. *(Not a defect — net-new design work.)*
2. **Hardware ENOB characterization.** Run the §8 rig (Tier 0 loopback → Tier 1 absolute) to upgrade P2AN000's qualitative ceiling claims to empirical numbers; on acceptance, replicate to the EF ledger and fill the measurement-table stub. Owner: Stephen (external hardware).
3. **OUT-OF-SPRINT, untouched in working tree (not this sprint's scope):** HUB75 datasheet refactor (`D engineering/document-production/datasheets/P2-Eval-HUB75-Adapter-Datasheet.md` + new `datasheets/P2-Eval-HUB75-Adapter-Datasheet/` dir) and an untracked `p2-xbyte-programming-guide/REF-NO-COMMIT/` scratch dir. Handle separately.

## Observations (not defects)

- The frozen `titus-cross-audit-raw-results-2026-06-12.json` still records the encoding finding as-found on 2026-06-12. Left intentionally unedited — it is timestamped run evidence, not maintained prose; the human-facing `.md` note carries the RESOLVED annotation.
- Fixed in this closeout: the corrections-register "Next finding ID" pointer was stale at `F-170` after F-170 was filed; bumped to `F-171`.

---

## Commits in this sprint

`75aeca21` (app-note doc class) · `571f5a40` (capture+study forum thread) · `e5692209` (plan) · `e8b89b08` (§1/§3/§4/§5 foundation) · `6d126852` (§7 guide + §8 rig) · `629558d3` (§6a) · `c6e0a032` (§6b). **Unpushed** (Stephen handles pushes).
