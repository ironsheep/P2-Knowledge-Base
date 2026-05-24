# Changelog Style Guide

Style conventions for all changelog entries in the P2 Knowledge Base. Applies to every manual's `CHANGELOG.md`, the repo's top-level `CHANGELOG.md`, and any other release-tracked changelog in this project.

---

## Core Principles

1. **Optimistic, forward-looking voice** - Changelogs describe what users have NOW, not what was wrong before. The doc tells readers what they're getting; it doesn't recount internal history. Tone is marketing copy, not a confession booth.
2. **Terse over verbose** - State what the document delivers, not commentary about it
3. **User-focused** - Include only what users care about
4. **No implementation details** - Omit root causes, debugging info, internal processes
5. **Aggregate corrections** - Group related improvements into themes rather than itemizing each one

---

## Never describe prior wrong state

Even when an entry documents work that corrected or refined something, the bullet describes the CURRENT state — never the prior state, never the delta. Banned phrases include:

- "corrected from X to Y"
- "previously incorrectly stated"
- "was misrepresented as"
- "had drift"
- "before this fix"
- "fixed where wrong"
- "no longer ..."
- "removed incorrect ..."

If the only way you can describe a change is by reference to what it WAS, the change doesn't belong in the changelog. Either reframe as a current capability ("X behavior documented", "Y is N") or omit.

---

## Never-shipped versions are never mentioned

Drafts, planning entries, "Upcoming" markers, internal alpha versions, and version numbers assigned but never tagged for release do NOT appear in the public changelog. For users, they never existed. Skipped semver numbers (e.g., 1.0 → 1.4 with no 1.1/1.2/1.3 entries) need no explanation — users don't track our internal numbering.

Corollary: never write a `[X.Y.Z-skipped]` or `(Upcoming)` entry. If a version number was never released, delete any artifact referencing it.

---

## What to Include

- New documentation (instructions, directives, examples, subsystem coverage)
- New capabilities the document didn't cover before
- Significant restructures or additions users will navigate to
- User-visible rendering improvements (tables span pages, navigation, diagrams)
- Visual changes users would notice

## What to Exclude

- Voice/style consistency audits
- Root cause explanations
- Before/after comparisons (just state current state)
- "Key finding" editorial statements
- Internal process notes
- Debugging details
- Pipeline/tooling implementation details (Lua filters, LaTeX workarounds)
- Trivial visual changes (symbol standardization, minor formatting)
- Internal regressions fixed before release (if v1.2 worked, v1.3 works, no entry needed)
- **Internal housekeeping** — broken cross-reference fixes, drift between artifacts (badges, version files, manifests), file reorganization, deduplication
- **Corrections with no user-discoverable impact** — if a user couldn't have hit the problem in shipped material, the fix doesn't belong here
- **Never-shipped planning artifacts** — see "Never-shipped versions" above
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

## Framing Corrections

Changelogs communicate strength: what users now have. Aggregate by theme; describe current capability.

### Aggregate into Themes

Instead of listing each item, summarize the area:

```markdown
# Avoid - itemizes prior problems
- LUT timing: "single-cycle" → "3 clock cycles"
- CALLA/CALLB timing: "14-32" → "13+ cycles"
- Hub access timing: "9-16" → "9-26 clocks"

# Prefer - describes the result
- Timing values aligned with silicon documentation
```

### Use Current-State Language

```markdown
# Avoid - exposes prior state
- REP cannot nest (was incorrectly documented as nestable)
- Removed incorrect "Hub Slot Synchronization" section

# Prefer - states current reality
- REP: Hardware constraints documented
- (omit removed content - users never saw it)
```

### Section Structure for Mixed Releases

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

## Two-question gate before including any entry

Before adding an entry to the changelog, ask:

1. **Does this describe a current capability or quality the document HAS?** (Not "had", not "now has after a fix" — just IS.)
2. **Could a user have been positively affected by this change appearing?**

If you can't answer YES to both, exclude the entry.

---

## Reference

Model entry: most recent semver entry in the top-level `CHANGELOG.md`.
