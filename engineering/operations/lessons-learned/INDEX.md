# Lessons Learned Index

**Purpose**: Map rules to their source incidents - understand "why" when needed

---

## How to Use This Index

When you encounter a rule and wonder why it exists:
1. Find the rule in the table below
2. Read the linked lesson document for full context
3. Understand the incident that created the rule

---

## Rule → Incident Mapping

### File Operations Rules

| Rule | Lesson Document | Incident Summary |
|------|-----------------|------------------|
| Backup before modifying files >100 lines | [file-operations-regression-lesson.md](file-operations-regression-lesson.md) | Lost 3300+ lines of PDF documentation |
| Use surgical editing (Edit tool), never wholesale replacement | [file-operations-regression-lesson.md](file-operations-regression-lesson.md) | Destructive file replacement without backup |
| Never use `head -n`, `>` redirection, or `mv` on important files | [file-operations-regression-lesson.md](file-operations-regression-lesson.md) | Truncation and overwrite incidents |
| Check file size before modifying | [file-operations-regression-lesson.md](file-operations-regression-lesson.md) | Large file damage prevention |
| Make a two-cog race **structural**, never incidental | [two-cog-race-rigs-must-be-structural.md](two-cog-race-rigs-must-be-structural.md) | Same rig, logic unchanged: 14,976 anomalies one run, 0 the next — cogs phase-lock at launch |
| A dual-tail rig must FAIL LOUDLY when its negative control doesn't fail | [two-cog-race-rigs-must-be-structural.md](two-cog-race-rigs-must-be-structural.md) | Zero-in-both-arms was one guard away from being banked as a clean PASS |

### PDF Generation Rules

| Rule | Lesson Document | Incident Summary |
|------|-----------------|------------------|
| Never use local Pandoc for PDF generation | [pdf-generation-changelog.md](pdf-generation-changelog.md) | Version incompatibility (1.19 vs 2.17) |
| Never rename template files (-fixed, -v2, etc.) | [pdf-generation-changelog.md](pdf-generation-changelog.md) | Broken references, deployment confusion |
| Always use flat structure in outbound | [pdf-generation-changelog.md](pdf-generation-changelog.md) | PDF Forge expects specific layout |

### Task Management Rules

| Rule | Lesson Document | Incident Summary |
|------|-----------------|------------------|
| Never delete tasks (use complete + archive) | *Undocumented* | Loss of time tracking and work history |
| Always run context_resume at session start | *Undocumented* | Lost context after session interruption |

---

## Lessons Not Yet Documented

These rules exist but lack formal lesson documents:

| Rule | Why It Exists | Should Document? |
|------|---------------|------------------|
| Filesystem MCP preferred over Bash for file ops | User preference for fewer approval prompts | Low priority |
| 3-hour session limit | Cognitive degradation after extended sessions | Medium priority |
| Complete work, never rush | Quality failures from hurried work | Low priority |

---

## Adding New Lessons

When an incident occurs:
1. Create lesson document: `[topic]-lesson.md`
2. Document: What happened, impact, root cause, rule created
3. Add entry to this index
4. Update CLAUDE.md rule to point here

---

*This index enables on-demand "why" retrieval without bloating CLAUDE.md with incident stories.*
