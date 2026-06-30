# Retrospective — P2 Capability Coverage & App-Note Roster

**Sprint:** Capability Coverage & App-Note Roster · **Closeout:** `2026-06-30-P2-CAPABILITY-COVERAGE-AND-APP-NOTE-ROSTER-CLOSEOUT.md` · **Build:** none (analysis sprint, version-less).

## Discovered perspectives
- **The app-note pipeline is SMALL after rigorous routing** — the P2 ecosystem is well-covered (rich OBEX/QB + strong manuals + the Architect's Guide method book), so most matrix gaps route *away* from app notes. The honest output is "CORDIC leads, a handful behind it," not a big series.
- **The in-development Architect's Guide owns most of the "compute-model" gap I first proposed** — its Act II (functional decomposition) + the 12-entry decomposition YAML layer cover multicore/coordination/inter-cog-comm. My flagship "Thinking in 8 Cogs" app note was wrong; Stephen caught it by asking whether I'd factored the Guide's *current* state.
- **The sharp cut is concept vs. implementation**, not topic — "inter-cog communication" splits: the contract decision → Guide; the worked FIFO/queue/deque code → app note. A single topic can land on both sides.
- **New `{Spin2_v47}` language features (TASK\*, STRUCT, stack-check) revive the P1 compute-model app notes** — as *feature-usage* notes (no guided home; Spin2 ref parked), distinct from architecture method.
- **Guides are earned, not presumed** — CORDIC stays an app note (not a guide like Streamer/XBYTE) because its *reference already exists*; only the applied layer is missing.

## Process insights
- **Delegating the two big catalog builds to background agents worked well** — QB (42 pages) and OBEX (re-scrape + 130-object classification) ran in the background while I produced the P1 mapping + manual survey inline. Good context economy; both returned verified, schema-clean work.
- **Grounding every claim in the catalogs/KB before asserting** (the user's consistent expectation) repeatedly caught my over-statements — emulation count, USB examples already in OBEX, the Architect's Guide scope, the existing §6.1 numbering convention.
- **The roster's value emerged in the collaborative back-and-forth**, not the mechanical matrix — Stephen's domain knowledge (Guide scope, new language features, numbering) sharpened the analysis turn by turn. The analysis sprint is genuinely interactive, not fire-and-forget.

## Quality & efficiency observations
- Background agents + inline parallel work kept wall-clock and context efficient on a long sprint.
- **The numbering decision flip-flopped** (keep-ADC-at-000 → reserve-as-template → start-at-001) — costing a round of doc rework. Signal: surface convention/identity decisions *earlier* and as an explicit either/or, rather than recommending one and re-cutting.

## Downstream impact
- **Enables:** the app-note authoring pipeline (CORDIC = P2AN002 next) + the document-enrichment pipeline, both fed by the mine-and-delineate front-end; the four-artifact model is now wired into the skills; the QB + OBEX catalogs are new served data.
- **Pending debt:** the `P2AN000 → P2AN001` renumber (repo-wide, tracked); the QB catalog + OBEX v2.2 are committed but **not published to the MCP index** (separate release step).

## Methodology lessons (candidates → triage in §5)
1. **Coverage/gap analysis must factor in-development docs' *planned* scope, not just shipped coverage** — counting only shipped manual coverage over-stated the app-note gap; the in-flight Architect's Guide owns a chunk of it. *Rule-sized; adopted this retrospective; certified by this very sprint's miss.*
2. **`mine-and-delineate` process** (external community code → documentation boundaries → enrich-or-app-note) — build-sized PROPOSAL, parked.
3. **Doc + machine-readable companion + agreement-gate** pattern — adopted locally in the skills; central generalization parked as a low-severity proposal.

## §5 verdicts (promotion-source: adopt → certify → promote)
- Lesson 1 → **adopted** (sprint-plan overlay) + **certified** (this sprint's Architect's-Guide miss); promotion-pending. Kept.
- Lessons 2 & 3 → **PROPOSAL** (build-sized / central-generalization); parked, kept.
- No entries closed-no-change; no deletions.
