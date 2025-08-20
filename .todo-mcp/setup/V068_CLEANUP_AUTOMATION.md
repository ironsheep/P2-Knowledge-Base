# v0.6.8 Todo MCP Cleanup Automation

## Complete Statement for Other Claude Instances

**Copy and paste this entire message to other Claude instances for automatic v0.6.8 cleanup:**

---

I need you to perform a complete v0.6.8 todo-mcp system migration and cleanup. Follow these steps exactly:

### Step 1: Create Top-Level Archive Directory
```bash
mkdir -p ARCHIVE-0.6.8
```

### Step 2: Archive Current CLAUDE.md Todo MCP Content
1. **Read** your current CLAUDE.md file
2. **Extract** all todo-mcp related content and save to `ARCHIVE-0.6.8/claude-archive-250819.md` 
3. **Remove** all todo-mcp references from CLAUDE.md
4. **Keep** only: Project info, build process, docs structure, basic rules

### Step 3: Archive v0.6.8 Documentation
**Move these to ARCHIVE-0.6.8/ subdirectories:**

```bash
# Move these directories/files to archive:
mv docs/reference/claude-guidance/ ARCHIVE-v0.6.8/docs-reference-claude-guidance/
mv docs/processes/claude-workflow/ ARCHIVE-v0.6.8/docs-processes-claude-workflow/
mv docs/CLAUDE_MD_TODO_MCP_SECTION.md ARCHIVE-v0.6.8/docs-top-level/

# Copy (don't move) friction studies:
cp -r docs/archive/friction-studies/* ARCHIVE-v0.6.8/docs-archive-friction-studies/

# Find and archive any files containing these patterns:
- v0.6.8 specific guidance
- CLAUDE.md integration patterns  
- TodoWrite integration guides
- Context management v0.6.8 patterns
```

**File patterns to search and archive:**
- Files containing: `todo-mcp`, `TodoWrite`, `CLAUDE\.md.*todo`, `v0\.6\.8`
- Directories: `docs/active/v0.6.8.1/`, `docs/processes/claude-workflow/`
- Specific files: `CLAUDE_MD_TODO_MCP_SECTION.md`, claude guidance docs

### Step 4: Clean Existing .todo-mcp or .claude-todo
```bash
# Move any existing todo-mcp directories to archive
mv .todo-mcp ARCHIVE-0.6.8/ 2>/dev/null || echo "No .todo-mcp found"
mv .claude-todo ARCHIVE-0.6.8/ 2>/dev/null || echo "No .claude-todo found"
```

### Step 5: Install New Mastery System
1. **Copy** the provided DOT-TODO-MCP folder to `.todo-mcp/`
2. **Verify** structure: `.todo-mcp/{mastery/,setup/,reference/}`
3. **Read** `.todo-mcp/setup/CLAUDE_MASTERY_INSERT.md`
4. **Merge** that entire content into your CLAUDE.md
5. **Test** integration with: `mcp__todo-mcp__context_resume` and `mcp__todo-mcp__todo_list`

### Step 6: Verification
**Confirm these results:**
- ✅ CLAUDE.md cleaned of old v0.6.8 references
- ✅ CLAUDE.md contains new mastery operations section
- ✅ All v0.6.8 docs moved to ARCHIVE-v0.6.8/
- ✅ New `.todo-mcp/` structure in place
- ✅ Session start protocol works: `mcp__todo-mcp__context_resume`

### Expected Outcome
You will have:
- **Clean slate**: No v0.6.8 interference
- **Mastery operation**: Immediate expert-level todo-mcp usage
- **Organized archive**: All old content preserved but separated
- **Self-sufficient CLAUDE.md**: Contains all operational knowledge needed

**The transformation removes learning friction and provides instant mastery-level operation.**

---

## Technical Details for Reference

### Files Commonly Needing Archive:
- `docs/CLAUDE_MD_TODO_MCP_SECTION.md`
- `docs/reference/claude-guidance/` (entire directory)
- `docs/processes/claude-workflow/` (entire directory)  
- `docs/active/v0.6.8.1/` (review manually)
- Any files containing v0.6.8 specific patterns

### Search Patterns Used:
```bash
# Documentation search
grep -r "todo.?mcp\|TodoWrite\|mcp__todo\|CLAUDE\.md.*todo" docs/ -l

# Directory search  
find . -name "*todo*" -o -name "*mcp*" | grep -v ".git"

# Version-specific search
grep -r "v0\.6\.8\|0\.6\.8" docs/ -l
```

### Archive Structure Created:
```
ARCHIVE-0.6.8/
├── claude-archive-250819.md          # Extracted CLAUDE.md content
├── .todo-mcp/                        # Old mastery system (if existed)
├── .claude-todo/                     # Old setup system (if existed)
├── docs-reference-claude-guidance/   # Claude guidance docs
├── docs-processes-claude-workflow/   # Workflow documentation
├── docs-top-level/                   # Top-level CLAUDE.md files
└── docs-archive-friction-studies/    # Friction analysis (copied)
```

This automation ensures consistent, complete migration across all Claude instances.