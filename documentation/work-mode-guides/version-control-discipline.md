# Version Control Discipline for Document Production

**Purpose**: Surgical commits and clear recovery points for document visual refinement cycles  
**Scope**: Universal - applies to Smart Pins, DeSilva, PASM2 Reference, all documents  
**Usage**: End-of-session wrap-up only (not during active work)

## Three Wrap Levels

### 1. Daily Wrap (Continuous Progress)
**When**: End of work session, made progress but not finished  
**Goal**: Create recovery point with current state and learnings

**Always Version These Directories**:
```bash
# Working files (current state)
git add workspace/[document-name]/
git add documentation/pdf-templates-master/  # Template fixes
git add documentation/work-mode-guides/      # Process learnings
```

### Document-Specific File Patterns

**Smart Pins Daily Wrap**:
```bash
git add workspace/smart-pins-manual/P2-Smart-Pins-Complete-Reference-WORKING.md
git add workspace/smart-pins-manual/request-requirements.json
git add documentation/pdf-templates-master/p2kb-foundation.sty
git add documentation/pdf-templates-master/p2kb-smart-pins.latex
git add documentation/work-mode-guides/smart-pins-visual-refinement.md
```

**DeSilva Daily Wrap**:
```bash
git add workspace/desilva-manual/P2-PASM-deSilva-Style-FULL-Part1.md
git add workspace/desilva-manual/P2-PASM-deSilva-Style-Part2a.md
git add workspace/desilva-manual/P2-PASM-deSilva-Style-Part2b.md
git add workspace/desilva-manual/P2-PASM-deSilva-Style-Part2c.md
git add workspace/desilva-manual/p2kb-pasm-desilva.latex
git add workspace/desilva-manual/request-requirements.json
git add documentation/pdf-templates-master/p2kb-foundation.sty
git add documentation/work-mode-guides/desilva-visual-refinement.md
```

**Commit Message Pattern**:
```bash
git commit -m "[Document]: Daily progress - [what was fixed]

- [Specific change 1]
- [Specific change 2]  
- Status: [current state], ready for [next step]"

git tag [document]-daily-YYYYMMDD
```

### 2. Document Completion Wrap  
**When**: Visual requirements met, document finished to target level  
**Goal**: Capture complete working package

**Add These Directories**:
```bash
# Daily wrap files PLUS:
git add exports/pdf-generation/outbound/[Document-Name]/  # Final package
git add [DOCUMENT]-STATUS.md                             # Achievement summary
```

**Commit Message Pattern**:
```bash
git commit -m "[Document]: Visual refinement complete - ready for review

- All visual requirements met per human approval
- Template fixes finalized and tested
- Final package ready for PDF generation
- Status: Complete, ready for Technical Design Review"

git tag [document]-complete-v1.0
```

### 3. Review Ready Wrap
**When**: PDF generated successfully, ready for formal review  
**Goal**: Complete review package with PDF

**Add These Directories**:
```bash
# Completion wrap files PLUS:
git add review/[document]-v1.0/           # Review package
# PDF file, review checklist, generation log
```

**Tag Pattern**: `git tag [document]-review-v1.0`

## Surgical Commit Strategy

### Critical Rules (Broad Repo Safety)
- ❌ **NEVER**: `git add .` or `git add -A` (commits everything)
- ✅ **ALWAYS**: Specify exact file paths
- ❌ **NEVER**: Commit unrelated work accidentally  
- ✅ **ALWAYS**: Review `git status` before commit

### Directory Selection Guidelines

**Always Version** (Essential Work):
- `workspace/[document]/` - Working files and state
- `documentation/pdf-templates-master/` - Template masters
- `documentation/work-mode-guides/` - Process improvements
- `[document]-STATUS.md` - Session summaries

**Sometimes Version** (When Created):
- `exports/pdf-generation/outbound/[Document]/` - Final packages only
- `review/[document]-v1.0/` - Review packages with PDF

**Never Version** (Should be in .gitignore):
- `/Scratchpad/` - Development/testing area
- `*.backup.*` - Automatic backup files
- `*.tex`, `*.aux`, `*.log` - Generated LaTeX files
- `/tasks/backups/` - MCP todo dumps

### Commit Message Quality

**Good Examples**:
```bash
"Smart Pins: Fixed section numbering and page breaks
- Set secnumdepth=1 for sections only  
- Fixed \ifafterpart logic for proper page breaks
- Status: Template tested, ready for image path fixes"

"DeSilva Part 2a: Pedagogical flow improvements
- Enhanced sidetrack boxes with better examples
- Fixed code highlighting in assembly sections
- Status: Part 2a visual review complete"
```

**Bad Examples**:
```bash
"Fixed stuff"           # Not specific
"Work in progress"      # No useful information  
"Updated files"         # Doesn't explain what changed
```

## Recovery Workflow

### If Session Breaks/Crashes
1. Check latest tag: `git tag --sort=-version:refname | head -5`
2. Review last commit: `git show HEAD`
3. Assess current state vs. last commit
4. Resume from appropriate recovery point

### If Need to Rollback
```bash
# See what we committed
git log --oneline -10

# Rollback to specific tag
git checkout [document]-daily-YYYYMMDD

# Create new branch from there
git checkout -b [document]-recovery
```

## .gitignore Strategy

**Add These Patterns** (if not already present):
```gitignore
# Working/temporary files
/Scratchpad/
*.backup.*
*-WORKING.md.backup.202*

# Generated files
*.tex
*.aux  
*.log
*.fls
*.fdb_latexmk

# Delivery directories (temporary)
/exports/pdf-generation/outbound/*/last-deployed/

# Process artifacts  
/tasks/backups/
/.todo-mcp/dumps/
```

## Multi-Document Coordination

### When Working on Multiple Documents
- **Separate commits** for each document
- **Clear prefixes**: `Smart Pins:`, `DeSilva:`, `PASM2:`
- **Independent tags**: Each document has own tag series
- **Cross-references**: Link related improvements in commit messages

### Template Changes Affecting Multiple Documents
```bash
# When p2kb-foundation.sty affects multiple docs:
git commit -m "Templates: Foundation layer numbering fix

Affects: Smart Pins, DeSilva, PASM2 Reference
- Fixed secnumdepth logic for consistent section numbering
- Updated \renewcommand{\thesubsection}{} implementation
- Status: All documents need retesting with updated template"
```

---

**Remember**: This discipline creates clean recovery points and clear project history. Use only during wrap-up, not during active visual refinement work.