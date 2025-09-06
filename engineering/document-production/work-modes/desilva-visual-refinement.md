# DeSilva PASM2 Manual Visual Presentation Refinement Guide

**Single Purpose**: Iterate DeSilva PASM2 manual visual presentation through human feedback loops

## 🚨 SESSION START INTEGRATION

### Work Mode Identification
**Trigger Phrases**: "De Silva visual", "De Silva visualization", "De Silva template fixes", "De Silva refinement"
**Confirmation**: "This covers De Silva visual refinement, template fixes, and iterative PDF generation with user feedback"

### Todo MCP Integration  
**CRITICAL - Always use this filter:**
```bash
mcp__todo-mcp__todo_next tags:["desilva_visual"]
```

**Why This Matters:**
- ✅ **Filters to De Silva visual tasks only**
- ✅ **Prevents task confusion with Smart Pins visual work** (uses `smart_pins_visual`)
- ✅ **Unified naming**: `desilva_visual` + `smart_pins_visual` for consistency
- ✅ **Ensures proper multi-part sequence** (Part 1 → Part 2a → Part 2b → Part 2c)
- ✅ **No more guessing what to work on** - MCP tells you exactly

### SESSION START CHECKLIST (DO THIS FIRST!)

#### 1. Verify Source of Truth Locations
```bash
# Check working parts have visual fixes
wc -l /engineering/document-production/workspace/p2-pasm-desilva-style/P2-PASM-deSilva-Style-FULL-Part1.md
# Should show ~700+ lines

# Check template has De Silva environments
grep -c 'sidetrack\|interlude\|yourturn\|chapterend' \
  /exports/pdf-generation/workspace/p2-pasm-desilva-style/templates/p2kb-pasm-desilva.latex
# Should show 4+ matches
```

#### 2. Required Reading
**Always read these documents when starting De Silva visual work:**
1. **THIS FILE FIRST** - De Silva specific protocols and source of truth
2. `/engineering/document-production/manuals/p2-pasm-desilva-style/creation-guide.md` - Pedagogical requirements
3. `/documentation/pipelines/pdf-generation-format-guide.md` - PDF production workflow
4. `/exports/pdf-generation/workspace/desilva-manual/visual-fixes-tracking.md` - Current state

## 🔴 CRITICAL: SOURCE OF TRUTH LOCATIONS

### Markdown Source of Truth
**ALWAYS EDIT HERE**: `/exports/pdf-generation/workspace/desilva-manual/`
- `P2-PASM-deSilva-Style-FULL-Part1.md` - Part 1 working copy
- `P2-PASM-deSilva-Style-Part2a.md` - Part 2a working copy  
- `P2-PASM-deSilva-Style-Part2b.md` - Part 2b working copy
- `P2-PASM-deSilva-Style-Part2c.md` - Part 2c working copy
- ALL markdown changes happen here FIRST
- Never edit the escaped/combined version in outbound

### Template Source of Truth  
**ALWAYS EDIT HERE**: `/exports/pdf-generation/workspace/desilva-manual/templates/`
- `p2kb-pasm-desilva.latex` - Master De Silva template
- ALL template changes happen here FIRST

### Deployment Workflow (EXACT SEQUENCE)
1. **Edit parts**: Individual part files in workspace/desilva-manual/
2. **Edit template**: workspace/desilva-manual/templates/p2kb-pasm-desilva.latex
3. **Combine parts**: Cat all parts → COMBINED-FOR-ESCAPING.md
4. **Escape combined**: `./tools/latex-escape-all.sh COMBINED → outbound/P2-PASM-deSilva-Style.md`
5. **Deploy template**: `cp template → outbound/p2-pasm-desilva-style/`
6. **Clean temp**: `rm COMBINED-FOR-ESCAPING.md`
7. **User deploys**: Takes ALL files from outbound to PDF Forge

### NEVER Edit These Directly
- ❌ `/engineering/document-production/outbound/p2-pasm-desilva-style/` - Deployment staging only
- ❌ Escaped/combined markdown files - Always edit parts then re-combine
- ❌ Templates in outbound - Always edit in workspace/desilva-manual/templates first

### Outbound Directory = Deployment Staging
**CRITICAL**: The outbound directory is WHERE YOU DROP FILES FOR USER TO DEPLOY:
- Combined escaped markdown → User moves to PDF Forge inbox/
- LaTeX template (.latex file) → User moves to PDF Forge templates/
- Request file (request.json) → User uses for PDF generation

**User handles deployment based on file type**

## File Structure (Fixed Locations)

```
DeSilva Working Environment:
/exports/pdf-generation/workspace/desilva-manual/
├── templates/                                  # SOURCE OF TRUTH templates
│   └── p2kb-pasm-desilva.latex               # Master De Silva template
├── P2-PASM-deSilva-Style-FULL-Part1.md       # Part 1 working copy
├── P2-PASM-deSilva-Style-Part2a.md           # Part 2a working copy  
├── P2-PASM-deSilva-Style-Part2b.md           # Part 2b working copy
├── P2-PASM-deSilva-Style-Part2c.md           # Part 2c working copy
├── visual-fixes-tracking.md                   # Current state tracking
└── DESILVA-STYLE-GUIDE.md                    # Style requirements

/exports/pdf-generation/outbound/P2-PASM-deSilva-Style/
├── P2-PASM-deSilva-Style.md                   # COMBINED & ESCAPED for PDF Forge
├── p2kb-pasm-desilva.latex                   # Template (copied from workspace)
├── request.json                               # PDF generation config
├── assets/                                    # Images (NO SPACES in names)
└── last-deployed/                             # Backup (auto-managed)
    ├── P2-PASM-deSilva-Style.md
    ├── p2kb-pasm-desilva.latex
    └── request.json
```

## The Visual Refinement Workflow

### 1. Human Provides Visual Feedback
Examples:
- "Sidetrack boxes need dashed borders, not solid"
- "Code highlighting inconsistent in Part 2b"  
- "Chapter celebrations too prominent"
- "Page breaks not working between parts"

### 2. Claude Implements Changes
**Multi-part strategy**:
- **Small fixes**: Edit specific part file in workspace
- **Template changes**: Update master template, affects all parts
- **Combined document**: Combine parts → escape → deploy to outbound

### 3. Part Combination Process
```bash
# Combine all parts into single document
cat workspace/desilva-manual/P2-PASM-deSilva-Style-FULL-Part1.md \
    workspace/desilva-manual/P2-PASM-deSilva-Style-Part2a.md \
    workspace/desilva-manual/P2-PASM-deSilva-Style-Part2b.md \
    workspace/desilva-manual/P2-PASM-deSilva-Style-Part2c.md \
    > workspace/desilva-manual/COMBINED-FOR-ESCAPING.md

# Escape combined document
./tools/latex-escape-all.sh \
  "workspace/desilva-manual/COMBINED-FOR-ESCAPING.md" \
  "outbound/P2-PASM-deSilva-Style/P2-PASM-deSilva-Style.md"

# Clean up temporary file
rm workspace/desilva-manual/COMBINED-FOR-ESCAPING.md
```

### 4. Human Tests PDF Generation
- Human generates PDF on Forge
- Human provides visual feedback on combined result
- Repeat until acceptable

## Change Types & Implementations

### Sidetrack/Interlude Boxes (DeSilva Specific)
**Template**: tcolorbox configurations for pedagogical elements
**Test**: Verify dashed borders, proper spacing around educational content

### Code Highlighting (Assembly Focus)
**Template**: Syntax highlighting for P2 assembly instructions  
**Test**: Consistent highlighting across all 4 parts

### Chapter Celebrations
**Template**: End-of-chapter celebration formatting
**Test**: Appropriate prominence, not overwhelming

### Part Transitions
**Template**: Page breaks between major parts
**Test**: Each part starts on new page

### Tutorial Voice Elements
**Markdown**: "Let's explore", "You'll discover" tutorial language
**Test**: Consistent pedagogical tone throughout

## 🚨 CRITICAL RULES

### NO FILE RENAMING - EVER
- **NEVER** create `-fixed`, `-v2`, `-working`, `-escaped` versions
- **ALWAYS** edit existing files in place
- **WHY**: Breaks references, confuses deployment, violates production discipline

### Layered Template Architecture (NEW!)  
- **Foundation**: `p2kb-foundation.sty` - Base Pandoc compatibility, typography, basic environments
- **Content**: `p2kb-desilva-content.sty` - De Silva pedagogical elements and tutorial styling  
- **Presentation**: `p2kb-tech-review.sty` - Professional branding and review formatting
- **Template**: `p2kb-pasm-desilva.latex` - Now uses layered architecture (monolithic archived as `p2kb-pasm-desilva-monolithic.latex`)

**IMPORTANT**: Template is now layered! Foundation provides basic tcolorbox environments, De Silva content adds pedagogical styling, tech-review adds professional branding.

### Quick Reference
- **Sidetrack fix**: Update template tcolorbox configuration
- **Escaping fix**: Run `latex-escape-all.sh` before deployment
- **Part combination**: `cat Part1.md Part2a.md Part2b.md Part2c.md > COMBINED.md`
- **Template deploy**: Always copy from workspace/templates/ to outbound/

## Request.json Format (UPDATED 2025-08-25)

**MANDATORY**: Use this EXACT structure with enhanced request format:

```json
{
  "documents": [{
    "input": "P2-PASM-deSilva-Style.md",
    "output": "P2-PASM-deSilva-Style.pdf",
    "template": "p2kb-pasm-desilva",
    "variables": {
      "title": "Discovering P2 Assembly",
      "subtitle": "Build, Experiment, and Master the Propeller 2", 
      "author": "P2 Community",
      "footer": "In the Spirit of deSilva's P1 Tutorial"
    },
    "pandoc_args": ["--wrap=preserve", "--top-level-division=part"]
  }],
  "options": {"cleanup": true, "archive": false, "optimize": false}
}
```

**Key Updates:**
- **Multiple pandoc_args**: Array supports multiple arguments
- **No path/extension**: Template name `p2kb-pasm-desilva` (not `.latex`)
- **Part structure**: `--top-level-division=part` enables proper chapter numbering
- **Lua filters**: `part-chapter-pagebreaks.lua` for proper page breaks, `smart-pins-auto-indent.lua` for code block indentation (adapt as needed)

**Enhanced Request with Lua Filters:**
```json
{
  "documents": [{
    "input": "P2-PASM-deSilva-Style.md",
    "output": "P2-PASM-deSilva-Style.pdf",
    "template": "p2kb-pasm-desilva",
    "variables": {
      "title": "Discovering P2 Assembly",
      "subtitle": "Build, Experiment, and Master the Propeller 2", 
      "author": "P2 Community",
      "footer": "In the Spirit of deSilva's P1 Tutorial"
    },
    "pandoc_args": [
      "--top-level-division=part",
      "--wrap=preserve",
      "--lua-filter=filters/part-chapter-pagebreaks.lua"
    ]
  }],
  "options": {"cleanup": true, "archive": false, "optimize": false}
}
```

**Request Requirements Pattern**:
- Check workspace for `request-requirements.json` 
- If present, merge special pandoc args into standard template
- Deploy complete `request.json` to outbound directory

## Visual Refinement Workflow

1. **Human provides feedback** (colors, formatting, page breaks, etc.)
2. **Claude edits** in workspace (individual parts and/or template)
3. **Combine & escape**: Cat parts → escape → deploy to outbound
4. **Human tests** on PDF Forge → repeat until visually perfect

## Milestones

### Internal Checkpoint ("Can Resume Tomorrow")
- [ ] All parts have current visual changes applied
- [ ] Template updated and tested with sample content
- [ ] Current state documented in workspace parts
- [ ] No blocking errors in last combined PDF generation attempt

### Technical Design Review Ready ("Final Handoff") 
- [ ] All visual requirements met per human approval
- [ ] Combined PDF generates successfully with no warnings
- [ ] Pedagogical elements (sidetracks, interludes) display correctly
- [ ] Tutorial voice consistent across all parts
- [ ] Ready for formal review process

## Essential Production Rules

### Filename Discipline (CRITICAL)
- ✅ **Same filename every iteration**: `P2-PASM-deSilva-Style.pdf`
- ❌ **NO version suffixes**: No -v1, -test, -draft, -fixed
- **Why**: Practice production process every iteration, prevent confusion

### Template Architecture (All .sty files MUST start with p2kb-)
- **Foundation**: `p2kb-foundation.sty` (Pandoc compatibility, shared by all)
- **Content**: `p2kb-pasm-desilva-content.sty` (Tutorial structure)
- **Presentation**: `iron-sheep-tech-review.sty` (Technical review branding)

### Multi-Part Management
- **Edit in parts**: Keep files <50KB for fast editing
- **Combine for PDF**: Single document for generation
- **Test iteratively**: Can test individual parts with small template samples

### File Disappearance (Normal - Set Expectations)
- **PDF succeeds**: "PDF generated, ready for visual review" (don't mention files moving)
- **PDF fails**: "Files moved during processing (normal), here's what to regenerate"
- **User Communication**: Focus on visual feedback, not file management

### Template Changes (Only provide .sty files when they change)
- **Don't resend unchanged**: Save human attention for visual decisions
- **When changed**: "Updated template deployed" + specific change description

### Working Copy Protection
1. **Never modify opus-master** - Read-only source of truth
2. **Working parts stay in workspace** - Only escaped combined version goes to outbound
3. **Verify file sizes** - Catch truncation/corruption immediately  
4. **Test changes incrementally** - Small changes, quick verification
5. **Human defines "done"** - Visual approval is the success criterion

## DeSilva Tutorial Standards

### Voice Requirements (Tutorial Style)
- **Pedagogical and Encouraging**: "Let's explore how P2 assembly works"
- **Building Understanding**: Progressive difficulty, scaffold learning
- **Experimental**: "Try this modification and see what happens"
- **Celebratory**: Acknowledge progress and achievements

### Visual Standards for Technical Design Review
- [ ] Consistent sidetrack/interlude box formatting across all parts
- [ ] Code examples with proper P2 assembly syntax highlighting
- [ ] Chapter celebrations appropriately formatted
- [ ] Part transitions with proper page breaks
- [ ] Tutorial voice consistent throughout combined document
- [ ] All pedagogical elements render correctly

## Production PDF Generation Process

### 🔴 MANDATORY: Check for Document Requirements

**STEP 1: Check for requirements file**
```bash
cat /engineering/document-production/workspace/pasm2-desilva-tutorial/request-requirements.json
```

If this file exists, it contains MANDATORY pandoc arguments for this document.

**STEP 2: Create production request**
```json
{
  "format_type": "document_generation",
  "documents": [{
    "input": "document.md",
    "output": "document.pdf",
    "template": "template-name",
    "pandoc_args": [...],  // Include args from request-requirements.json
    "lua_filters": [...]    // Document-specific filters
  }]
}
```

**STEP 3: Deploy to outbound**
- Place request.json in `/engineering/document-production/outbound/[document-name]/`
- Copy markdown and assets to same location
- User handles deployment to PDF Forge

## Current Status Tracking

**Last working state**: [Update after each session]
**Outstanding visual issues**: [From human feedback] 
**Next iteration focus**: [Specific changes to implement]
**Parts status**: 
- Part 1: [status]
- Part 2a: [status]  
- Part 2b: [status]
- Part 2c: [status]

---

**This guide covers ONLY DeSilva visual refinement. Other documents get their own focused guides.**