# Changelog Style Guide — the class-3 profile

Style conventions for all changelog entries in the P2 Knowledge Base. Applies to every manual's `CHANGELOG.md`, the repo's top-level `CHANGELOG.md`, and any other release-tracked changelog in this project.

## What this file is, and what it is not

**The voice rules are not here. They are in `~/.claude/skills-docs/guides/changelog-voicing.md` §1–§4, and that guide governs.** This file is the **class-3 (published document) profile** — the part `changelog-voicing.md` §5 declares an *unauthored stub* and explicitly delegates to the project:

> "A class-3 project therefore keeps its local guide. Take a `central:changelog-voicing` row for the shared core (§1–§4), keep the local file as the class-3 profile under its own row, and trim it to what this guide does not carry."

So: **read both.** Central for how a changelog sounds and what qualifies; this file for the shape a *document's* changelog takes — its Part-based sections, its entry formats, its length budget, and the handful of exclusions that only exist because the artifact is a manual rather than a program.

**Rules that used to live here and now live in central** — deleted rather than duplicated, because two copies of a rule are two rules that will disagree:

| Was here | Now |
|---|---|
| Never describe prior wrong state | §4.4 Prior state — and it is **stronger** there: it rules on "no longer" per class (banned for class 3, required for code classes) |
| Never-shipped versions are never mentioned | §1.7 — also covers `[Unreleased]` sections |
| Initial releases describe the document, not a delta | §3.1 The initial-release entry |
| Aggregate into themes | §1.2 |
| Use current-state language | §4.4 |
| The two-question gate | §4.1 The gate |
| Core principles (voice, terseness, user focus, no implementation detail) | §1.1, §4.2, §4.6, §4.7 |

**Class-3 specialisations of those central rules**, which central states generically and this class states concretely:

- §3.1's *"no feature recitation"* is, for a document, **no table-of-contents recitation** — do not itemize chapters; the document's own ToC already does that. State holistically what the document is.
- §3.1's delta headings, in this project's vocabulary, are `### Added` / `### Changed` / `### Fixed`. An initial entry uses none of them. It is identified as the **only** `## v…` entry in the file, or the one whose predecessor has no public README/tag baseline.

---

## What to Include

- New documentation (instructions, directives, examples, subsystem coverage)
- New capabilities the document didn't cover before
- Significant restructures or additions users will navigate to
- User-visible rendering improvements (tables span pages, navigation, diagrams)
- Visual changes users would notice

## What to Exclude

Central §4.2 carries the generic exclusions — root causes, debugging detail, before/after comparisons, internal regressions fixed before release, and anything a user could not have hit in a shipped release. Not repeated here. **What follows exists only because the artifact is a document:**

- Voice/style consistency audits
- "Key finding" editorial statements
- Pipeline/tooling implementation details (Lua filters, LaTeX workarounds)
- Trivial visual changes (symbol standardization, minor formatting)
- **Internal housekeeping** — broken cross-reference fixes, drift between artifacts (badges, version files, manifests), file reorganization, deduplication
- **Style/voice/discipline changes to internal documentation** — methodology refinements, internal process notes
- **Skill / tooling updates that only affect authoring workflow** — unless they produced user-visible improvement worth naming on its own terms

**Editorial Refinements (excluded category):**
- Terminology standardization (unless old term was technically incorrect AND was visible to users)
- Cosmetic diagram changes (reordering, repositioning labels)
- Minor precision adjustments
- Content reorganization (section reordering, list restructuring)
- Stylistic consistency fixes (wording alignment across sections)

**The Exclusion Test:** Ask "Would a user have been positively affected by this change appearing in the changelog?" If no, exclude it.

---

## "Fixed" section discipline

Reserve `### Fixed` for user-impacting bug fixes where the prior buggy behavior was visible in a SHIPPED release. The entry still describes the current state ("X behaves Y") — never the bug.

For corrections to YAML data, documentation accuracy, or internal artifacts that users never directly saw, do not use the `### Fixed` section. Either fold the improvement into `### Added` or `### Changed` with current-state framing, or omit if the user couldn't have noticed.

Examples:
- ✅ User-visible: `### Fixed: PDF tables span page breaks` (users saw broken tables in a shipped release)
- ❌ Internal: `### Fixed: cross-references redirected to correct files` (users never saw broken refs)

Many releases have nothing that qualifies for `### Fixed`. An empty `### Fixed` section is a smell — drop it.

---

## Section Structure for Mixed Releases

When a release has both new content and accuracy improvements:

```markdown
## vX.Y.Z (YYYY-MM-DD)

**Release Theme**

### Added
- Bullet list of additions

### Changed
- Summary lines covering accuracy improvements (current-state framing)
```

---

## Entry Format

### Simple Additions
```markdown
- INSTRUCTION: Brief description
```
Examples:
- `ABS: Z flag documented`
- `LOCKNEW: C flag column documented`
- `AKPIN: Encoding documented`

### Grouped Additions
```markdown
**Category Name:**
- ITEM1: Description
- ITEM2: Description
```

### Documentation Additions
```markdown
- INSTRUCTION: Added [what was added]
```
Examples:
- `RDBYTE: Added 4-context timing table`
- `DEBUG symbols: Added DEBUG_COGINIT, DEBUG_MAIN, DEBUG_MASK`

### Complete Rewrites
```markdown
- DIRECTIVE: Documentation rewritten ([one-line summary of what it does])
```
Example:
- `DITTO: Documentation rewritten (block-based replication with $$ index)`

### Rendering/Presentation Items
```markdown
- [Component]: [Current behavior]
```
Examples:
- `Encoding tables: Multi-page rendering supported`
- `Timing tables: Header rendering preserved across pages`

**Presentation test:** Only include if users would have noticed the problem in a shipped release. "Tables span page breaks" = yes (PDF behavior is visible). "Changed internal symbol encoding" = no.

---

## Section Structure

```markdown
## vX.Y.Z (YYYY-MM-DD)

**Release Theme** - One-sentence summary.

### Part I: Architectural Foundation
- Chapter-level additions

### Part II: Instruction Reference

**Category:**
- Instructions grouped by type

### Part III: Appendices
- Appendix additions (including user-visible rendering improvements)
```

**Note:** Presentation/rendering items belong in the relevant Part section (e.g., Appendix A rendering item goes in Part III). Avoid separate "Presentation" sections — they tend to accumulate internal implementation details.

---

## Length Guidelines

**This table narrows central §4.7 for class 3; where they differ, this one governs for a document's changelog.** Central's "with detail" tier is 10–30 words because §4.5 (name the trigger) makes it structurally two clauses, and it exempts breaking changes up to 45. Neither applies here: a published document has no breaking changes to recover from and no runtime exposure to date, so the tier collapses back to 10–20 and the 25-word maximum is absolute.

| Entry Type | Target Length |
|------------|---------------|
| Simple addition | 5-10 words |
| With detail | 10-20 words |
| Maximum | 25 words |

Parenthetical explanations: 10 words maximum.

---

## Examples

### Good (Terse, current-state)
```markdown
- LUT Sharing: Shared capacity is 512 longs per cog
- WAITX: Timing formula is 2 + Dest
- DITTO: Documentation rewritten (block-based replication with $$ index)
```

### Avoid (Verbose, prior-state)
```markdown
- **LUT Sharing**: Corrected shared LUT capacity from 1024 longs to 512 longs (each cog contributes its 512-long LUT for a combined 1024-long shared space, but each cog can only access 512 longs at a time)
- **WAITX Instruction**: Corrected timing formula from "Dest+1" to "2 + Dest" per Silicon CSV. Added randomized delay behavior documentation (when WC/WZ/WCZ specified). Fixed code example comment: "Wait 100" → "Wait 101 clock cycles (2 + 99)"
```

---

## Reference

Model entry: most recent semver entry in the top-level `CHANGELOG.md`.

**The gate before including any entry is central §4.1**, and it is the last thing to run over a drafted entry. It is not restated here.
