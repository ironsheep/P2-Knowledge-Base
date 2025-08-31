# Technical Debt: Template Coordination Across Documents

**Issue Identified**: 2025-08-29
**Status**: Needs Architecture Discussion
**Impact**: High - Could break document generation

## The Problem

When working on different documents (Smart Pins, DeSilva manual, etc.), they share some common .sty files but also have document-specific ones:

### Shared Files (affect multiple documents)
- `p2kb-foundation.sty` - Base Pandoc fixes (used by ALL documents)
- `p2kb-tech-review.sty` - Technical review formatting (used by multiple)

### Document-Specific Files
- `p2kb-smart-pins-content.sty` - Smart Pins only
- `p2kb-desilva-content.sty` - DeSilva manual only

## The Risk

1. Working on Smart Pins, we update `p2kb-foundation.sty` 
2. Switch to DeSilva manual work
3. DeSilva manual now broken due to foundation changes
4. No way to know what broke without testing all documents

## Potential Solutions to Discuss

### Option 1: Version Lock System
- Each document declares which version of shared .sty it needs
- Keep versioned copies of shared files

### Option 2: Regression Test Suite
- Automated testing that generates all documents
- Run before committing any .sty changes
- Catches breaks immediately

### Option 3: Strict Backward Compatibility
- Never break existing functionality in shared files
- Only add new features with different names
- Document which features each document uses

### Option 4: Template Inheritance
- Base templates that never change
- Document-specific overrides
- Similar to CSS cascading

## Questions to Answer

1. How do we know which documents use which .sty files?
2. How do we test changes won't break other documents?
3. Should shared files be truly shared or copied per document?
4. How do we document dependencies?
5. Who decides when a shared file can change?

## Next Steps

- [ ] Schedule focused discussion session
- [ ] Audit current .sty file usage across all documents
- [ ] Prototype one solution approach
- [ ] Document the chosen approach

## Related Files
- `/exports/pdf-generation/workspace/manual-templates/` - Source of truth
- Todo MCP Task #1118 - Tracking this discussion