# Document Production & Release — Process Map

> **This was a full step-by-step guide (created 2025-08-20, pre-skill era).** Its
> procedure is now owned by skills, and its old walkthrough had drifted badly out of
> date (dead paths like `/exports/pdf-generation/`, a stale `request.json` schema, and
> obsolete model names). This file is now the **map** that routes each phase to the skill
> or tracker that owns it, plus the few durable authoring notes no skill carries. The
> original 2025-08 walkthrough is preserved in git history.

## The process, by phase → who owns it now

| Phase | Owned by | Notes |
|-------|----------|-------|
| **Plan / track a manual** | `engineering/document-production/PUBLICATION-ROSTER.md` | the live roster + **Platform Freshness Ledger** is the single tracker (replaces the old "Document Pipeline" + ops dashboard) |
| **Author / revise content** | `manuals/<slug>/opus-master/` + per-manual `creation-guide.md` / `style-guide.md` | content is hand-authored; code examples are `pnut_ts`-validated; code-line budget `K` is enforced per manual |
| **Stage a manual for PDF** | **`prepare-manual`** skill | refresh from opus-master → LaTeX-escape → stage only changed files to outbound |
| **Test a template / layout / diagram** | **`forge-test`** skill | interactive daemon round-trip; read the compile log + render pages yourself |
| **Generate the production PDF** | PDF Forge (user deploys `outbound/` → the manual store) | two separate Forge stores — interactive vs. manual-production |
| **Changelog** | **`audit-changelog`** skill + `methodology/changelog-style-guide.md` | voice + commit-traceability |
| **Release to deliverables** | **`release-manual`** skill | verify the PDF (silent-drop guard) → promote CHANGELOG + README index → record ledger/roster → suggest git |
| **Model choice** | **`model-strategy`** skill / `pipelines/claude-model-selection-strategy.md` | (the old "Opus 4.1 / Sonnet 4 / Haiku 3.5" note here was obsolete) |

To run any phase, invoke the named skill.

## Versioning / lifecycle (the durable spine)

Manuals progress **draft → release-candidate → release**. The current public convention is
a three-part semver `vX.Y.Z` plus a *"<Month Year> - Community Review Edition"* label in the
deliverables README — **not** the old "-DRAFT suffix + warning box" scheme. `release-manual`
reads the version from the topmost `CHANGELOG.md` entry; a manual's deliverables status is
tracked in `PUBLICATION-ROSTER.md`, not in scattered dashboards.

## Markdown authoring gotchas (still true — no skill owns these)

pandoc needs a blank line where markdown editors often don't, and a stray bracket can do
real damage:

- **Blank line before a list** that follows a bold heading or any colon-terminated line —
  without it the list doesn't render (`**Heading:**` ⏎ `- item` → insert a blank line).
- **Blank line before a fenced code block** that follows a heading.
- **Unbalanced `[` / `:::` / ` ``` `** in prose makes pandoc **silently swallow** content
  until it rebalances — this is the failure mode the `release-manual` Phase-1 silent-drop
  guard exists to catch (it once cost a manual ~156 pages with a clean compile log). When a
  generated `.tex` is missing sections the source has, check delimiter balance in the
  assembled markdown first.

(Render-cleanliness tweaks the old guide did by hand — horizontal-rule stripping, etc. — are
now handled by the shared platform Lua filters.)
