# De Silva Manual Mode Guide

**Single Purpose**: De Silva manual template adaptation and content cleanup work

## 🚨 SESSION START INTEGRATION

### Work Mode Identification
**Trigger Phrases**: "De Silva", "template adaptation", "vertical template stack", "De Silva cleanup"
**Confirmation**: "This covers De Silva manual template adaptation to new vertical stack and document cleanup"

### Todo MCP Integration  
**CRITICAL - Always use this filter:**
```bash
mcp__todo-mcp__todo_next tags:["desilva_manual"]
```

**Why This Matters:**
- ✅ **Filters to De Silva-specific tasks only**
- ✅ **Separates from Smart Pins work** - no task confusion
- ✅ **Proper sequence for template adaptation** - infrastructure first, then content
- ✅ **Tracks multi-part document workflow** (Part 1, 2a, 2b, 2c, Appendices)

### Required Reading (Session Start)
**Always read these documents when starting De Silva work:**
1. `/documentation/pdf-forge-system/layered-template-architecture.md` - New vertical stack
2. `/documentation/pipelines/pdf-generation-format-guide.md` - Production workflow  
3. `/engineering/document-production/workspace/p2-pasm-desilva-style/DESILVA-STYLE-GUIDE.md` - Visual requirements
4. **This file** - De Silva specific protocols

### Context Keys Storage
**Document progress in context with `desilva_` prefix:**
- `desilva_template_status` - Current template adaptation state
- `desilva_part_N_complete` - Multi-part document tracking
- `desilva_cleanup_issues` - Found problems needing fixes

## De Silva Template Adaptation Workflow

### 1. Template Stack Migration
**FROM**: Individual .latex files per document  
**TO**: Layered vertical stack (foundation → content → presentation)

**New Architecture:**
- `p2kb-foundation.sty` - Base Pandoc compatibility (shared)
- `p2kb-desilva-content.sty` - De Silva structure/formatting  
- `iron-sheep-tech-review.sty` - Presentation layer (branding)

### 2. Document Cleanup Workflow
**Working Location**: `/engineering/document-production/workspace/p2-pasm-desilva-style/`
- Multi-part structure: Part1, Part2a, Part2b, Part2c, Appendices
- Apply learnings from Smart Pins visual work
- Test template changes with small sections first

### 3. Common Cleanup Tasks
- Fix LaTeX escaping issues (corrupted by previous tools)
- Standardize code block formatting
- Ensure consistent section numbering
- Verify image asset references
- Apply creation guide requirements

## Template Adaptation Priorities

### Phase 1: Foundation Layer
- Migrate shared functionality to `p2kb-foundation.sty`
- Test basic PDF generation with new stack
- Ensure no regressions from old template

### Phase 2: Content Layer  
- Extract De Silva-specific formatting to `p2kb-desilva-content.sty`
- Handle multi-part document structure
- Implement De Silva visual requirements

### Phase 3: Integration Testing
- Full multi-part document testing
- Visual comparison with previous versions
- Performance/reliability verification

## File Structure

```
De Silva Working Environment:
/engineering/document-production/workspace/p2-pasm-desilva-style/
├── editing/                                    # Current working copies
│   ├── Part1-Getting-Started-WORKING.md  
│   ├── Part2-Architecture-WORKING.md
│   └── Part3-Programming-WORKING.md
├── templates/                                  # Template development
│   ├── p2kb-foundation.sty
│   ├── p2kb-desilva-content.sty
│   └── iron-sheep-tech-review.sty
└── DESILVA-STYLE-GUIDE.md                     # Visual requirements

/engineering/document-production/outbound/p2-pasm-desilva-style/
├── [part-files].md                            # Escaped for PDF Forge
├── p2kb-*.sty                                 # Deployed templates  
└── request.json                               # Generation config
```

## Success Criteria

### Template Adaptation Complete
- [ ] New vertical stack generates identical PDF output
- [ ] No LaTeX compilation errors
- [ ] All visual requirements preserved
- [ ] Performance meets or exceeds old template

### Document Cleanup Complete  
- [ ] All corruption issues resolved
- [ ] Consistent formatting across all parts
- [ ] Creation guide requirements met
- [ ] Ready for technical design review

---

**This guide covers ONLY De Silva manual work. Switch guides when changing work focus.**