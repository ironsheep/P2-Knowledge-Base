# Process-Document Catalog

**Created:** 2026-06-11 · **Method:** full markdown survey (6 reader-agents over the
process/methodology/operations directories), classified against the current skills
inventory. **Purpose:** the repo has accreted process docs since 2025-08 — originals,
quick-form overlays, and docs already superseded by skills but never thinned. This
catalog is the basis for planning their obsolescence and, crucially, for ensuring
**every tracked artifact has a skill that keeps it current** (an unowned tracker silently
drifts — we lived the proof in `document-generation-process.md`).

**Scope:** `engineering/{operations, document-production/methodology, document-production/work-modes,
procedures, pipelines, pdf-forge, ingestion/work-modes}` + the key trackers. **~168 docs.**
Excluded by design: per-manual `creation/style/voice-guide.md` (a separate "owned-by-manual"
category), `manuals/*/opus-master` content, ingestion sources, sprint *history*, templates.

**Legend** — *status:* ✅ superseded-by-skill · 🆕 skill-candidate · 📌 durable-keep ·
⚠️ stale/obsolete · 💥 corrupted · 🔁 duplicate · 🗄️ archival. *disposition:* thin-to-pointer ·
fold→skill+retire · new-skill · **assign-maintainer** · keep · keep-as-archive · delete.

---

## Part 1 — Headline findings (act on these first)

### 🚨 A. Orphaned trackers — the silent-drift risks (no skill keeps them current)

These are *live or semi-live* tracking artifacts with **no owning skill**. Each will rot.

| Tracker | What it tracks | Fix |
|---------|----------------|-----|
| `ingestion-metadata/extraction-health-status.md` | per-doc extraction completeness | **fold into `ingest-source`** (it writes the DASHBOARD but never this) — or retire |
| `ingestion-metadata/EXTRACTION-INDEX.md` | master source-processing % | **fold into `ingest-source`** — or retire |
| `operations/TECHNICAL-DEBT.md` | known-issues / cleanup backlog | **assign maintainer** (a debt skill, or merge into the corrections register) |
| `methodology/manual-production-working-set.md` | layout-effort scope over the roster | assign maintainer (prepare-manual or a layout skill) — or retire if absorbed by roster |
| `methodology/presentation-block-catalog.md` | block/callout controlled vocabulary | assign maintainer (the platform/layout skill that adds block types) |
| `pipelines/document-production-pipeline.md` | per-document deliverable state | **superseded by `PUBLICATION-ROSTER.md`** → retire (don't maintain two) |
| `pipelines/pdf-generation-compatibility-log.md` | LaTeX-package compat issues | keep, but assign a maintainer (forge-test/prepare-manual) |
| `operations/README.md` | the ops dashboard (stale since 2025-09) | thin-to-pointer (roster + this catalog are the real trackers) |
| `project-guidance/validation-sprint-pipeline.md`, `pasm2-narrative-enrichment-status.md`, `forge-status-snapshot-2026-06-04.md`, `project-guidance/mcp-sprint-a1-object-inventory.md` | one-off / drifted status snapshots | delete or keep-as-archive |

**Properly skill-owned trackers (the model to copy):** `PUBLICATION-ROSTER.md` → `release-manual` + `prepare-manual`, read by `whats-next` · `INGESTION-DASHBOARD.md` → `ingest-source` · `P2KB-CORRECTION-FINDINGS.md` → appended by `ingest-source`/`document-finalize`, swept by `punch-list-maintenance`, DONE-marked by `yaml-knowledge-base-maintenance`.

### B. Skill-superseded clusters (thin-to-pointer or fold→skill+retire)

The repo carries **multiple parallel copies** of processes now owned by one skill each:

- **PDF production (≈9 docs)** → `prepare-manual` + `forge-test`: `methodology/{p2kb-document-production-process, pdf-generation-format-guide, pdf-generation-methodology, MARKDOWN-TRANSFORMS-REQUIRED}`, `pipelines/pdf-generation-workflow`, `pdf-forge/work-modes/{production-pdf-generation, automated-pdf-testing}`, `pdf-forge/guides/pdf-forge-system/PDF-FORGE-DEPLOYMENT-WORKFLOW`, plus the just-thinned `document-generation-process.md`.
- **Sprint process (≈12 docs)** → `sprint-plan`/`sprint-start`/`sprint-closeout`/`sprint-retrospective`/`plan-to-tasks`/`task-execution`: the `project-guidance/sprint-*` family, `process/{sprint-lifecycle, sprint-document-lifecycle}`, `task-generation-process` (×2), `master-checklist-template`, `sprint-retrospective-template`, `work-mode-lifecycle`.
- **Model choice (3 docs)** → `model-strategy`: `pipelines/claude-model-selection-strategy`, `pipelines/model-switching-best-practices`, `process/model-switching-strategy`.
- **Ingestion (3 docs)** → `ingest-source`: `ingestion/work-modes/{document-ingestion-focused, image-extraction-focused}`, `procedures/yaml-workflow-quick-guide` (→ `yaml-knowledge-base-maintenance`).
- **Release/routing**: `operations/RELEASE-PLANNING` → `release-yamls`; `project-guidance/release-workflow-v1.0` → `release-manual`; `claude-guidance/STARTUP-BY-WORK-TYPE` + `PROCESS-GUIDANCE-ARCHITECTURE` + `work-mode-lifecycle` → `whats-next`.

### C. New-skill candidates (process with no skill yet)

- **Visual-refinement** — the four near-identical work modes (`work-modes/{desilva-visual-refinement, p2-debug-window-visual-refinement, smart-pins-visual-refinement}` + `desilva-manual-mode`) differ only by slug/tag → **one parameterized `visual-refinement` skill**.
- **Code-study** — `work-modes/{spin2-code-study-mode, systematic-code-study-mode}` overlap → **one `code-study` skill**.
- **Smaller folds:** `standards/version-control-discipline` → `build-wrapup`/`release-manual`; `project-guidance/plan-review-methodology` → a plan skill; `P2KB-CORRECTION-PLAN` → `yaml-knowledge-base-maintenance`.

### D. Delete (obsolete or corrupted)

`methodology/pdf-generation-workflow-guide.md` (💥 corrupted — self-declared incomplete from the 2025-08 data-loss), `methodology/forge-status-snapshot-2026-06-04`, `ingestion/work-modes/{central-repository-build, download-on-demand-api}` (demo-deadline), `pipelines/document-pipeline-queue`, `pipelines/source-code-ingestion-cross-check` (✅-complete one-off), and the stale 2025-08 strategy/planning essays in `operations/planning/**` + several `claude-guidance` speculative docs.

### E. Durable-keep (rules/reference, not procedures — leave alone)

`methodology/changelog-style-guide`, `methodology/presentation-platform-unification-STUDY`, `methodology/document-creation-criteria`, `process/TECHNICAL-DOCUMENT-AUDIT-METHODOLOGY`, `project-guidance/methodology/TECHNICAL-CLIMBING-METHODOLOGY`, `lessons-learned/**`, `planning/strategic/PROJECT-GOALS`, the AI-privacy guides, and the `pdf-forge/guides/pdf-forge-system/**` LaTeX/Forge reference set.

### F. Archival (keep-as-archive — frozen history)

All of `operations/migration/**` (2025-09 reorg), `operations/reports/**` (2025-09 KB reports), `operations/audits/**`, `operations/sprints/**`, `operations/strategy/**`.

---

## Part 2 — Proposed obsolescence plan (waves, for approval)

1. **Wave 1 — stop the drift (highest value):** assign maintainers for the orphaned trackers in §A — fold `extraction-health-status` + `EXTRACTION-INDEX` into `ingest-source`; retire `document-production-pipeline.md` (roster supersedes it); give `TECHNICAL-DEBT.md` an owner. Net: every live tracker is skill-owned.
2. **Wave 2 — collapse the parallel PDF + sprint clusters (§B):** thin each to a one-line pointer to its owning skill (the `document-generation-process.md` exemplar); delete the corrupted/demo ones (§D). Biggest line-count reduction, removes drift-prone duplicates.
3. **Wave 3 — promote the two new skills (§C):** `visual-refinement` (collapses 4 docs) and `code-study` (collapses 2); then thin those source docs.
4. **Wave 4 — sweep archival:** confirm §F stays as `keep-as-archive` (optionally move under a single `engineering/history/` tree); thin the stale maps (`operations/{README, INDEX, REPOSITORY-STRUCTURE}`, `PROCESS-GUIDANCE-ARCHITECTURE`) to pointers into this catalog + the skills.

A "process doc" is sound to retire **only after** its owning skill exists and carries any durable nuance the doc held; durable rationale not in the skill moves to a lessons-learned/reference doc, never just deleted.

---

## Part 3 — Full catalog

> One row per surveyed doc, grouped by disposition. `n/a` maintainer = not a tracker.

### fold→skill+retire / thin-to-pointer (skill-superseded)

| path | purpose | status | → skill |
|------|---------|--------|---------|
| methodology/document-generation-process.md | doc-production process | ✅ (now-thinned map) | prepare-manual/forge-test/release-manual |
| methodology/p2kb-document-production-process.md | old end-to-end pipeline | ✅ | prepare-manual |
| methodology/pdf-generation-format-guide.md | Forge file/filename patterns | ✅ | prepare-manual |
| methodology/pdf-generation-methodology.md | md→PDF workflow | ✅ | prepare-manual |
| methodology/MARKDOWN-TRANSFORMS-REQUIRED.md | pre-Forge transforms | ✅ | prepare-manual |
| pipelines/pdf-generation-workflow.md | definitive PDF workflow | ✅ | prepare-manual |
| pdf-forge/work-modes/production-pdf-generation.md | final PDF workflow | ✅ | prepare-manual |
| pdf-forge/work-modes/automated-pdf-testing.md | daemon template testing | ✅ | forge-test |
| pdf-forge/guides/pdf-forge-system/PDF-FORGE-DEPLOYMENT-WORKFLOW.md | deploy to Forge | ✅ | prepare-manual |
| work-modes/pdf-generation-template-debugging.md | template debugging | ✅ | forge-test |
| ingestion/work-modes/document-ingestion-focused.md | full ingestion process | ✅ | ingest-source |
| ingestion/work-modes/image-extraction-focused.md | image extraction | ✅ | ingest-source |
| procedures/yaml-workflow-quick-guide.md | 7-step YAML change | ✅ (quick-form) | yaml-knowledge-base-maintenance |
| pipelines/claude-model-selection-strategy.md | model-per-task | ✅ | model-strategy |
| pipelines/model-switching-best-practices.md | safe model switch | ✅ | model-strategy |
| process/model-switching-strategy.md | Opus vs Sonnet | ✅ | model-strategy |
| pipelines/task-generation-process.md | sprint→tasks | ✅ | plan-to-tasks |
| project-guidance/task-generation-process.md | sprint→atomic tasks | ✅ | plan-to-tasks |
| process/sprint-lifecycle.md | sprint phases | ✅ | sprint-start |
| process/sprint-document-lifecycle.md | sprint folder structure | ✅ | sprint-start |
| project-guidance/sprint-execution-process.md | execution phases | ✅ | sprint-start |
| project-guidance/sprint-execution-methodology.md | 3-phase rationale | ✅ | sprint-start |
| project-guidance/sprint-lifecycle-methodology.md | plan→integration | ✅ | sprint-plan |
| project-guidance/sprint-planning-methodology.md | iterative planning | ✅ | sprint-plan |
| project-guidance/sprint-retrospective-template.md | retro template | ✅ | sprint-retrospective |
| project-guidance/master-checklist-template.md | task checklist template | ✅ | task-execution |
| project-guidance/work-mode-lifecycle.md | planning-vs-exec matrix | ✅ | whats-next |
| project-guidance/release-workflow-v1.0.md | early release workflow | ✅ | release-manual |
| operations/RELEASE-PLANNING.md | YAML release process | ✅ | release-yamls |
| operations/P2KB-CORRECTION-PLAN.md | how-to-apply corrections | 🆕 | yaml-knowledge-base-maintenance |
| standards/version-control-discipline.md | commit/tag wrap levels | 🆕 | build-wrapup/release-manual |
| project-guidance/plan-review-methodology.md | section-by-section review | 🆕 | (plan skill) |
| claude-guidance/STARTUP-BY-WORK-TYPE.md | context→work-type routing | ✅ | whats-next |
| operations/PROCESS-GUIDANCE-ARCHITECTURE.md | process-guidance map | 🆕 | whats-next / this catalog |

### new-skill candidates

| path | → proposed skill |
|------|------------------|
| work-modes/desilva-visual-refinement.md | `visual-refinement` (parameterized) |
| work-modes/p2-debug-window-visual-refinement.md | `visual-refinement` |
| work-modes/smart-pins-visual-refinement.md | `visual-refinement` |
| work-modes/desilva-manual-mode.md | `visual-refinement` (or delete — dead paths) |
| work-modes/spin2-code-study-mode.md | `code-study` |
| work-modes/systematic-code-study-mode.md | `code-study` |

### assign-maintainer (orphaned trackers/registers) — see §A

`ingestion-metadata/extraction-health-status.md` · `ingestion-metadata/EXTRACTION-INDEX.md` · `operations/TECHNICAL-DEBT.md` · `methodology/manual-production-working-set.md` · `methodology/presentation-block-catalog.md` · `pipelines/document-production-pipeline.md` · `pipelines/pdf-generation-compatibility-log.md`

### delete (obsolete / corrupted)

`methodology/pdf-generation-workflow-guide.md` (💥) · `methodology/forge-status-snapshot-2026-06-04.md` · `work-modes/desilva-manual-mode.md` (dead paths) · `ingestion/work-modes/central-repository-build.md` · `ingestion/work-modes/download-on-demand-api.md` · `pipelines/document-pipeline-queue.md` · `pipelines/source-code-ingestion-cross-check.md` · `pdf-forge/guides/pdf-forge-system/{pdfforge-analysis-and-recommendations, recommended-enhancements}.md` · `pdf-forge/guides/PDF-FORGE-WORKFLOW-THOUGHTS.md` · `project-guidance/mcp-sprint-a1-object-inventory.md` · `planning/{p2-pattern-mining-plan, p2-knowledge-sprint-plan, strategic/project-information-architecture}.md` · `standards/{email-review-workflow, communication-strategy/p2kb-executive-communication-plan}.md` · `claude-guidance/{CRITICAL-GUIDANCE-ANALYSIS, multi-agent-architecture-design}.md` · `process/inputs/archived/*` (2 files)

### keep (durable rules / reference)

`methodology/{changelog-style-guide, diagram-block-standard, document-creation-criteria, presentation-platform-unification-STUDY, manual-layout-standards-*, manual-stylesheet-architecture-survey, presentation-block-catalog, workspace-README-template}` · `work-modes/latex-escape-script-management` · `process/TECHNICAL-DOCUMENT-AUDIT-METHODOLOGY` · `project-guidance/{methodology/TECHNICAL-CLIMBING-METHODOLOGY, methodology/BACKUP-STRATEGY (thin: dup of Sacred Rule #1), process-augmentation, ai-assisted-developer-workflow}` · `lessons-learned/**` · `planning/strategic/PROJECT-GOALS` · `standards/best-practices/opus-generation-token-management` · `claude-guidance/{claude-human-optimization-guide, ai-assisted-developer-use-cases, adaptive-mentoring-framework}` · `guides/{ai-privacy-guide-v1.0, ai-privacy-training-handout, social-media-campaign-strategy}` · `pdf-forge/guides/**` (Forge/LaTeX reference set) · `pipelines/{formatting-reference/**, INTEGRATION_GUIDE, pattern-attribution-standard, pipeline-prioritization-market-strategy}` · the three skill-owned trackers (`PUBLICATION-ROSTER`, `INGESTION-DASHBOARD`, `P2KB-CORRECTION-FINDINGS`)

### keep-as-archive (frozen history) — see §F

`operations/migration/**` (13) · `operations/reports/**` (10) · `operations/audits/**` (3) · `operations/sprints/**` (3) · `operations/strategy/**` (2) · `operations/{ABOUT, manifest-*, orphan-resolution-plan, obex-path-analysis, enriched-yaml-analysis, pasm2-narrative-enrichment-status}` · `planning/DOCUMENT-ROADMAP` + the stale strategic essays not deleted

### thin-to-pointer (stale maps/orientation)

`operations/{README, INDEX, REPOSITORY-STRUCTURE}.md` · `methodology/document-generation-process.md` (done) · `pdf-forge/guides/pdf-forge-system/template-development-and-automation-strategy.md` · `obex-integration-instructions.md` · `human-ai-collaboration-process.md` · several `planning/strategic/*` + `guides/*` strategy essays

---

*Note: `operations/GITHUB-REPO-SETUP.md` is untracked (never committed). The per-manual
`creation/style/voice-guide.md` set was intentionally out of scope — it's a distinct
"owned-by-manual config" category worth its own short pass.*
