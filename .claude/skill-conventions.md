# Project skill conventions — P2-Knowledge-Base

This file holds slot values for the central skill set. See
`~/.claude/skills-docs/SKILLS-MAINT.md` for the full schema.

## ⚠️ This is a multi-headed project

P2-Knowledge-Base is **three heads under one repo**, not a single-build app:

1. **KB-for-agents** — the P2KB YAML knowledge base served on demand via
   `p2kb-mcp`. "Green" = valid cross-references, clean index, sourced facts.
   Its build is *validate + regenerate index*. Has its own version.
2. **Source study / ingestion** — studying & ingesting published P2 docs
   (P1 next). **Version-less**: governed by ingestion-quality, cross-ref,
   and audit *gates* plus a completeness *dashboard*, not releases.
3. **Manual production** — the documentation manuals (6+ in flight). Build
   is *PDF generation via PDF Forge* (handback model). **Each manual carries
   its own version + CHANGELOG.**

Consequence for the slot schema (built for a single-headed app): a whole
category of slots — version, plan dir, punch list, release notes, spec —
**has no correct single global value.** Those slots carry a per-head
**routing sentinel** (`<per-head — ...>`) instead of a literal. The sentinel
keeps each skill's Step 0a from hard-stopping (so Step 0b loads the overlay),
and the skill's `project-overlay.md` does the real per-head dispatch:
*identify the head/element, then resolve the artifact from that head's
pattern.* This is the same primitive as `CLAUDE.md`'s Work Type Routing.

---

## Identity

```yaml
USER_NAME:     Stephen
PROJECT_NAME:  P2-Knowledge-Base
```

## Build & test

The one head with an objective local green/red is the **P2KB YAML set**.
`baseline-health` ("are we green") maps to its validators. Manuals build on
PDF Forge (no local gate); ingestion uses quality gates + dashboard.

```yaml
BUILD_COMMAND:          python3 engineering/tools/validate-yaml-syntax.py
TEST_COMMAND:           python3 engineering/tools/validate-crossref-keys.py
CANONICAL_TEST_TARGET:  local Python validators over the P2KB YAML set (YAML syntax + cross-reference; DoD via validate-dod-release.py)
```

## Build version — PER-HEAD (sentinel)

No global project version. The manual you're working on, or the P2KB YAML
set, owns the version; **ingestion has no version.** Resolved per head.

```yaml
BUILD_VERSION_LOCATION:  <per-head — manual CHANGELOG.md, or P2KB YAML set version; N/A for ingestion; see skill overlay>
BUILD_VERSION_KEY:       <per-head — see skill overlay>
BUILD_VERSION_EXAMPLE:   <per-head — e.g. manual "2.3.0"; see skill overlay>
```

## Doc paths

```yaml
ANALYSIS_DIR:  engineering/analysis/

# PER-HEAD (sentinel) — resolved by Work Type Routing / skill overlay:
PLAN_DIR:           <per-head — manual plan co-located with the manual; ingestion plan with its source; YAML-set plan in its own home; see skill overlay>
PLAN_ARCHIVE_DIR:   engineering/history/sprints/
PUNCH_LIST_DOC:     <per-head — one per manual, per ingestion source, and for the P2KB YAML set; P2KB-CORRECTION-FINDINGS.md is the YAML-set register; see skill overlay>
RELEASE_NOTES_DOC:  <per-head — manual CHANGELOG, or P2KB YAML release notes; N/A for ingestion (uses completeness dashboard); see skill overlay>
SPEC_DOC:           <per-head — N/A for ingestion; see skill overlay>
```

## Model strategy

```yaml
MODEL_TIERS:   ["opus", "sonnet"]
DEFAULT_MODEL: opus
```

## Audience & vocabulary

```yaml
RELEASE_NOTES_AUDIENCE:  the P2 developer community
```

## Document finalize

`DOC_RENDER_COMMAND` is intentionally **omitted** — manuals render on PDF
Forge (handback model), so `document-finalize` hands the document back for
the user to render rather than running a local render command.

---

## Omitted slots (intentional)

- **P2 development cycle** — omitted entirely. The repo holds ~2000 `.spin2`
  files, but they are examples / OBEX objects, not one firmware project with
  a single top file. `p2-dev-cycle` is not part of this project's workflow.
- **Filename patterns** — omitted; central defaults apply (per-head plan
  naming is designed in overlays).
- **Voicing / style guides** (`MANUAL_VOICING_GUIDE`, `STYLE_GUIDE_DOC`,
  `HELP_VOICING_GUIDE`) — per-manual under
  `engineering/standards/documentation-standards/`; no single global file,
  so omitted (resolved per manual when needed).
- **Per-task detail artifacts**, `PROJECT_INIT_DATE`, `TEST_FLEET_DESCRIPTION`
  — omitted; defaults apply.

## Known cleanup debt (separable tasks — not bootstrap work)

1. Consolidate scattered plan dirs (`engineering/operations/sprints`,
   `engineering/operations/planning`, `engineering/planning`).
2. Relocate punch-list content to its correct per-head homes.
3. Give `engineering/operations/P2KB-CORRECTION-FINDINGS.md` the
   `punch-list-maintenance` lifecycle (complete → dated archive; latest copy
   holds only outstanding work).
