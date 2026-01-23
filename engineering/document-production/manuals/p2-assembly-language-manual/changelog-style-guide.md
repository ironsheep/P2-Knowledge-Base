# Changelog Style Guide

Style conventions for P2 Assembly Language Reference Manual changelog entries.

---

## Core Principles

1. **Terse over verbose** - State what changed, not why it was wrong
2. **Additive framing** - Focus on what the document NOW provides, not what was wrong before
3. **User-focused** - Include only changes users care about
4. **No implementation details** - Omit root causes, debugging info, internal processes
5. **Aggregate corrections** - Group related fixes into themes rather than itemizing each one

---

## What to Include

- Content corrections (encoding tables, flag effects, timing)
- New documentation (instructions, directives, examples)
- User-visible rendering fixes (broken tables, navigation issues)
- Significant visual changes users would notice

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

**Editorial Refinements (new category):**
- Terminology standardization (unless old term was technically incorrect)
- Cosmetic diagram changes (reordering, repositioning labels)
- Minor precision adjustments ("359" → "~360" instruction counts)
- Content reorganization (section reordering, list restructuring)
- Stylistic consistency fixes (wording alignment across sections)

**The Exclusion Test:** Ask "Would a user have been confused, misled, or unable to find information before this change?" If no, exclude it.

---

## Framing Corrections

Changelogs should communicate strength, not confess weakness. Users want to know what they're getting, not what was broken.

### Aggregate into Themes
Instead of listing each correction, summarize the improvement:

```markdown
# Bad - itemizes each problem
- LUT timing corrected: "single-cycle" → "3 clock cycles"
- CALLA/CALLB timing corrected: "14-32" → "13+ cycles"
- Hub access timing corrected: "9-16" → "9-26 clocks"

# Good - describes the result
- Timing values verified against silicon documentation
```

### Use Additive Language
Describe what exists now, not what changed:

```markdown
# Bad - highlights the error
- Corrected: REP cannot nest (was incorrectly documented as nestable)
- Removed incorrect "Hub Slot Synchronization" section

# Good - states current reality
- REP: Hardware constraints documented
- (don't mention removed content - users never saw it)
```

### Section Structure for Mixed Releases
When a release has both new content and accuracy improvements:

```markdown
## vX.Y.Z (YYYY-MM-DD)

**Release Theme**

### New Content
- Bullet list of additions

### Enhanced Accuracy
- One or two summary lines covering all corrections

### Figures (if applicable)
- Figure numbering or diagram additions
```

---

## Entry Format

### Simple Corrections
```markdown
- INSTRUCTION: Brief description of fix
```
Examples:
- `ABS: Z flag corrected`
- `LOCKNEW: C flag column alignment corrected`
- `AKPIN: Encoding corrected`

### Grouped Corrections
```markdown
**Category Name:**
- ITEM1: Fix description
- ITEM2: Fix description
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

### Rendering/Presentation Fixes
```markdown
- [Component]: Fixed [symptom]
```
Examples:
- `Encoding tables: Fixed multi-page rendering`
- `Timing tables: Fixed table header rendering`

**Presentation test:** Only include if users would have noticed the problem. "Tables were cut off" = yes. "Changed internal symbol encoding" = no.

---

## Section Structure

```markdown
## vX.Y.Z (YYYY-MM-DD)

**Release Theme** - One-sentence summary.

### Part I: Architectural Foundation
- Chapter-level fixes

### Part II: Instruction Reference

**Category:**
- Instruction fixes grouped by type

### Part III: Appendices
- Appendix fixes (including user-visible rendering fixes)
```

**Note:** Presentation/rendering fixes belong in the relevant Part section (e.g., Appendix A rendering fix goes in Part III). Avoid separate "Presentation" sections—they tend to accumulate internal implementation details.

---

## Length Guidelines

| Entry Type | Target Length |
|------------|---------------|
| Simple fix | 5-10 words |
| With detail | 10-20 words |
| Maximum | 25 words |

Parenthetical explanations: 10 words maximum.

---

## Examples

### Good (Terse)
```markdown
- LUT Sharing: Corrected shared capacity from 1024 to 512 longs per cog
- WAITX: Corrected timing formula to 2 + Dest
- DITTO: Documentation rewritten (block-based replication with $$ index)
```

### Bad (Verbose)
```markdown
- **LUT Sharing**: Corrected shared LUT capacity from 1024 longs to 512 longs (each cog contributes its 512-long LUT for a combined 1024-long shared space, but each cog can only access 512 longs at a time)
- **WAITX Instruction**: Corrected timing formula from "Dest+1" to "2 + Dest" per Silicon CSV. Added randomized delay behavior documentation (when WC/WZ/WCZ specified). Fixed code example comment: "Wait 100" → "Wait 101 clock cycles (2 + 99)"
```

---

## Reference

Model changelog: v1.1.0 section in CHANGELOG.md
