# Changelog Style Guide

Style conventions for P2 Assembly Language Reference Manual changelog entries.

---

## Core Principles

1. **Terse over verbose** - State what changed, not why it was wrong
2. **Optimistic framing** - Use "corrected", "added", "fixed", "clarified"
3. **User-focused** - Include only changes users care about
4. **No implementation details** - Omit root causes, debugging info, internal processes

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
