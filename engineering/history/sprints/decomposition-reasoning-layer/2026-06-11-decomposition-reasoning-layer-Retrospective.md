# Sprint Retrospective — Decomposition Reasoning Layer

**Sprint:** Decomposition Reasoning Layer · **Shipped:** KB **v1.7.0** (tag `v1.7.0`, index commit `56a1771`)
**Closeout:** `2026-06-11-decomposition-reasoning-layer-CLOSEOUT.md` (same dir)
**Date:** 2026-06-11

Signal, not narrative. What was *learned*, distinct from what shipped.

## Discovered perspectives

- **`asm…endasm` is FlexSpin (fastspin) syntax, not pnut_ts.** Surfaced auditing `asm_integration_analysis.yaml` in §15. Our trust chain is pnut_ts-anchored, so inline-PASM examples must use `ORG…END` with params addressed by name (PR0/PR1), never via PTRA/PTRB. Mined/legacy KB content can carry a *foreign-compiler* idiom that looks plausible — a distinct failure class from a P1-ism. Fixed in place + logged F-105.
- **The crossref validator's field semantics are load-bearing and non-obvious:** `see_also`/`references` are treated as informational *text* (always pass, never resolved); `related`/`combines_with`/`related_*` are *must-resolve* mnemonic fields. It scans **top-level fields only** — nested `composition_rules.combines_with` is invisible to it. This decided the whole §15 stub design (redirect via `see_also`, never break validation) and §16 (sibling `p2kbArch*` keys in `see_also`, existing-file paths in `related`).
- **The generator doubles the prefix for `spin2_`-named files:** `spin2_latest_wins_mailbox` → `p2kbSpin2Spin2LatestWinsMailbox`. The resume note's shorthand (`p2kbSpin2LatestWinsMailbox`) was wrong; only confirming against the actual generator output got the see_also targets right.
- **Bare `combines_with` names resolve via generator aliases** post-regen — not something to assume. Confirmed by regenerating and re-running crossref (17 → 0), not by trusting the plan.

## Process insights

- **`release-yamls` two-commit Path B held up perfectly** — content commit (explicit staging, no derived artifacts) → regen all 3 derived artifacts → validate → derived-artifacts commit → tag the index commit. Catching that there are **three** derived artifacts (`p2kb-index.json`, `.gz`, `p2-reference.json`) — not just the index — only happened because the skill enumerates them; improvising would have shipped a stale gzip (and the DoD validator caught exactly that mid-flight).
- **The DoD validator earned its keep:** the stale-gzip FAIL was the one real gate between "looks done" and "is done."
- **`mcp__filesystem__edit_file` does fuzzy leading-whitespace matching** — it matched a 4/6-space `oldText` against a 0/2-space file region and silently de-indented a YAML list item (`framework_pattern.yaml`). Caught on the parse-verify pass. Caution: after an `edit_file` on indentation-sensitive files, verify the result (parse + `cat -A`), don't trust the diff alone.
- **Plan-before-edit + verify-after-edit paid off repeatedly** — presenting the §15 file table before touching 11 YAMLs, and re-running crossref after every batch, kept the working tree provably clean at each step.

## Quality and efficiency observations

- **Faster than planned:** §15 estimated 1h30, actual ~20m — the stub-don't-delete ruling made each file a small mechanical edit rather than a redirect-every-inbound-ref exercise (the validator's top-level-only scanning meant inbound refs never broke).
- **The one detour cost** (pre-sprint, carried as lesson): the taskspin "compiler gap" chase — time lost preferring a compiler-guess over the KB, when `taskspin.yaml` documented the `{Spin2_v47}` requirement all along.
- **Verification regen as a confidence tool:** running a throwaway index regen to *prove* the 17 pre-regen unresolveds clear (rather than asserting they would) cost ~90s and removed all doubt before the release.

## Downstream impact

- **Enables:** a remote agent can now derive an object/cog decomposition for an unfamiliar P2 hardware mix from first principles (the four forces + procedure), not just pattern-match a catalog. The 4 new compile-verified patterns give the concrete code skeletons the forces imply.
- **Establishes conventions** future yaml work inherits: the `authority_tier` per-section discipline, the two-tier grounding policy (PHYSICS→internal key, reasoning→durable canon), and stub-don't-delete supersession.
- **Destabilizes nothing** — crossref 100%, index byte-clean, no removed keys (the whole point of stub-don't-delete).

## Methodology lessons (candidates — Stephen's call to act)

Two candidates already in `feedback_skill_evolution_candidates.md` from this sprint, plus new ones:

1. **[yaml-knowledge-base-maintenance] author-kb-layer mode** (already buffered) — authoring NET-NEW generative guidance is a different shape than the skill's correction/Sacred-Rule-#7 focus; needs authority-tier discipline + two-tier grounding + generative-vs-catalog bar. **Verdict: DEFER** — proven useful this sprint; revisit if a second authored-layer sprint appears (the 2-project bar is really "2 sprints" here).
2. **[baseline-health] `validate-yaml-syntax.py` coverage gap** (already buffered) — it covers only `manifests/` + `engineering/knowledge-base/` (4 files), NOT the `deliverables/ai/P2/` content it's assumed to gate; content syntax is actually caught by the index-generator parse + crossref validator. **Verdict: DEFER → lean ADDRESS** — this is a real "baseline reads greener than it verifies" hole; recommend a baseline-health overlay line naming which validator covers which tree.
3. **NEW [yaml-knowledge-base-maintenance] crossref-validator field semantics** — `see_also`=text/unvalidated vs `related`/`combines_with`=must-resolve; top-level only. Non-obvious and load-bearing for any redirect/supersession work. **Proposed: add to the candidates buffer** (captured as a design-decision in the sprint-state memory regardless).

No central-skill *refinement* is forced this sprint; all candidates are project-overlay-or-memory level.

## Triage of `feedback_skill_evolution_candidates.md` (proposed verdicts — Stephen decides)

| Entry | Proposed verdict |
|-------|------------------|
| document-finalize × 3 (truth-matrix audit; handback locate-precisely; fix-in-correct-tree) | **DEFER** (prior sprints; unchanged) |
| prepare-manual/migration (content-conversion checklist) | **DEFER** (prior sprint; unchanged) |
| yaml-knowledge-base-maintenance author-kb-layer mode | **DEFER** (this sprint; revisit on 2nd authored-layer) |
| baseline-health validate-yaml-syntax coverage gap | **DEFER → ADDRESS** (recommend overlay line) |

Pruning happens only with Stephen's verdict — nothing deleted here.
