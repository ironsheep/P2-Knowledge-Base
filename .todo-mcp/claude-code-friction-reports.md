# Claude Code Friction Reports

*Ready-to-file issues for https://github.com/anthropics/claude-code/issues*

## Issue 1: Task List Display Regression

**Title**: Task list truncated to 1-2 items with Ctrl+R prompt instead of showing full list

**Description**:
Previously, when Claude generated or displayed a task list, the full list was visible in the terminal. Now the interface only shows 1-2 tasks and prompts users to press Ctrl+R to see the full list.

**Impact**: 
- Breaks workflow visibility
- Requires extra keystrokes to see context
- Reduces productivity when reviewing task progress

**Expected Behavior**: 
Full task list should display by default when requested or generated

**Actual Behavior**: 
Only 1-2 tasks shown with "Press Ctrl+R to display full list" prompt

**Version**: [Current CCLI version]

---

## Issue 2: Excessive Approval Prompts for Cat Commands

**Title**: Cat commands require approval every time, unlike other file operations

**Description**:
When Claude uses `cat << 'EOF'` pattern for creating temporary analysis or documentation, users must approve each command. This doesn't happen with filesystem MCP operations which are pre-approved.

**Impact**:
- Interrupts user thinking/workflow
- Shows partial file content that's not useful
- Creates approval fatigue
- Inconsistent with other file operations

**Expected Behavior**: 
Cat commands for file creation should follow same approval rules as filesystem operations

**Actual Behavior**: 
Every cat command requires manual approval, showing truncated preview

**Reproduction Steps**:
1. Ask Claude to analyze something requiring multi-step analysis
2. Claude uses cat << 'EOF' for organizing thoughts
3. User prompted for approval on each cat command

**Version**: [Current CCLI version]

---

## Issue 3: MCP Context Loss After Auto-Compaction

**Title**: Todo MCP context not properly preserved during auto-compaction

**Description**:
When conversation auto-compacts due to context limits, Todo MCP context keys are lost, requiring manual recovery through context_resume and context_get_all commands.

**Impact**:
- Loss of work state
- Requires manual recovery steps
- TodoWrite state lost

**Suggested Solution**:
Preserve MCP context keys during auto-compaction, especially task state and recovery information

**Version**: [Current CCLI version]

---

*Note: These are drafts - update version numbers and add any additional fields the GitHub issue form requires*