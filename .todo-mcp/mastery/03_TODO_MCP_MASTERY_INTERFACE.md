# Todo MCP v0.6.8.1 Mastery Interface Guide

## Authority and Scope

This document represents the **complete synthesized knowledge** from three Claude instances' v0.6.8 usage patterns plus v0.6.8.1 interface exploration. It provides **immediate mastery-level operation** without learning friction.

**Sources**: 
- Interface analysis of all 25+ v0.6.8.1 MCP functions
- todo-mcp instance: Dual-system foundation, crash recovery
- p2kb instance: Defensive programming, model economics, strict discipline
- pnut-term-ts instance: Context mastery, documentation architecture

## 🔴 CRITICAL: The Parameter Patterns

### Pattern 1: Dual-Parameter Functions
**Accept EITHER `position_id` OR `task_id` with # string**
```bash
# By position (interactive work)
mcp__todo-mcp__todo_complete position_id:1
mcp__todo-mcp__todo_tag_add position_id:1 tags:["urgent"]
mcp__todo-mcp__todo_tag_remove position_id:1 tags:["done"]

# By task ID (automation/scripts)
mcp__todo-mcp__todo_complete task_id:"#22"
mcp__todo-mcp__todo_tag_add task_id:"#22" tags:["urgent"]
mcp__todo-mcp__todo_tag_remove task_id:"#22" tags:["done"]
```

### Pattern 2: Bulk Operations
**Use arrays or filters, never individual IDs**
```bash
mcp__todo-mcp__todo_bulk operation:"set_priority" filters:{status:"created"} data:{priority:"high"}
mcp__todo-mcp__todo_bulk operation:"add_tags" task_ids:[1,2,3] data:{tags:["sprint-1"]}
```

## 🔴 CRITICAL: Task Lifecycle (Enforced)

### Required Sequence
```bash
# STEP 1: Must start before complete (enforced by system)
mcp__todo-mcp__todo_start position_id:1

# STEP 2: Can complete only after starting
mcp__todo-mcp__todo_complete position_id:1  # or task_id:"#22"

# WRONG - Will fail with error
mcp__todo-mcp__todo_complete position_id:1  # Without starting first
```

### Single Active Task Rule
- Only ONE task can be `in_progress` at a time
- Starting new task automatically pauses current one
- No exceptions to this rule

## 🔴 CRITICAL: Parameter Data Types (Exact Requirements)

```bash
# CORRECT data types
estimate_minutes:60        # Number, never string
priority:"high"           # String: critical/high/medium/low/backlog
status:"in_progress"      # String: created/in_progress/paused/completed
force:true               # Boolean, never string
include_context:true     # Boolean, never string

# WRONG - These will fail
estimate_minutes:"60"     # String not accepted
priority:"HIGH"          # Must be lowercase
force:"true"             # Must be boolean
```

## 🟡 IMPORTANT: Tag Auto-Extraction Intelligence

### Extraction Rules
**Trailing tags removed completely:**
```bash
"Fix parser bug #urgent #backend"
→ Content: "Fix parser bug"
→ Tags: [urgent, backend]
```

**Inline tags keep word:**
```bash
"Fix the #bug in parser"
→ Content: "Fix the bug in parser"  
→ Tags: [bug]
```

**Special cases:**
- Tags in quotes ignored: `"Error '#failed' in logs"` → No tags
- Must have space before #: `"fix#bug"` → No extraction
- Unicode supported: `"Fix #système"` → Tag: [système]

## 🔴 CRITICAL: Always Verify Empty States

**Pattern - Empty responses often incorrect:**
```bash
# WRONG - Trusting empty response
mcp__todo-mcp__context_resume  # Shows "Working Memory: (empty)"
# Assume no context exists

# CORRECT - Always verify
mcp__todo-mcp__context_resume  # Shows empty
mcp__todo-mcp__context_get_all  # VERIFY - might have data!
```

**Apply to all operations:**
- Context appears empty → Run `context_get_all`
- Search returns nothing → Run unfiltered search
- Archive reports nothing → Check completed task status

## Multi-Line STF Display Format

### Standard Task Display
```
N. [status] [priority] [content] [timing] «#ID»
   🏷️ #tag1 #tag2 #tag3
   ⛔ Blocked by: «#42» (future feature)
```

**Components:**
- **Position**: Changes as tasks complete/reorder
- **Status**: ○ (created) ◐ (in_progress) ⊘ (paused) ● (completed)
- **Priority**: ⚡ (critical) 🔴 (high) 🟡 (medium) 🟢 (low) 🔵 (backlog)
- **Task ID**: Permanent «#49» identifier
- **Tags**: 3-space indented on line 2
- **Dependencies**: When implemented

## Core Recovery Command

### Primary Recovery (Post-Crash/Compaction)
```bash
mcp__todo-mcp__context_resume
```

**Shows:**
- Tasks in progress with elapsed time
- Context organized by prefix with ages
- Next recommended tasks
- Summary statistics
- Recent context keys (10-minute window in v0.6.8.1)

### Complete System State
```bash
mcp__todo-mcp__todo_list               # All tasks
mcp__todo-mcp__project_status          # System health
mcp__todo-mcp__context_get_all         # Full context
mcp__todo-mcp__session_summary         # Today's work
```

## Smart Task Selection

### Intelligent Next Task
```bash
mcp__todo-mcp__todo_next
```

**Algorithm considers:**
1. Dependencies (blocked tasks excluded)
2. Priority (critical → backlog)
3. Sequence (manual ordering)
4. Age (older tasks preferred)

## Data Safety Patterns

### Archive vs Clear
```bash
# SAFE - Exports then clears with backup
mcp__todo-mcp__todo_archive

# RISKY - Just deletes data
mcp__todo-mcp__todo_clear_completed  # Avoid this
```

### Complete Backup/Restore
```bash
# Full system backup
mcp__todo-mcp__project_dump include_context:true
# Returns: tasks/backups/project_dump_TIMESTAMP.json

# Complete restore
mcp__todo-mcp__project_restore file:"filename.json" mode:"replace" include_context:true

# Modes: replace (clear+restore), merge (add to existing), append (add all)
```

## Export Capabilities

### Available Formats
```bash
mcp__todo-mcp__todo_export format:"markdown"  # Human-readable
mcp__todo-mcp__todo_export format:"json"      # Complete data
mcp__todo-mcp__todo_export format:"csv"       # Spreadsheet
mcp__todo-mcp__todo_export format:"org"       # Org-mode

# Clean markdown for docs
mcp__todo-mcp__export_markdown include_completed:true
```

## Search and Filter System

### Comprehensive Search
```bash
# Searches content, tags, and IDs
mcp__todo-mcp__todo_list search:"bug"

# Combined filters
mcp__todo-mcp__todo_list status:"created" priority:"high" search:"bug"

# Sort options
sort_by:"priority"   # By priority level
sort_by:"created"    # By creation time  
sort_by:"updated"    # By modification
sort_by:"estimate"   # By time estimate
sort_by:"sequence"   # By manual sequence
```

## Context System (Unrestricted)

### Flexible Key Management
**The context system has NO restrictions on key naming or content.**

**Successful patterns observed:**
```bash
# Some projects used prefixes for organization
mcp__todo-mcp__context_delete pattern:"temp_*"

# Others used descriptive names without prefixes
# Both approaches worked well
```

**Key insight**: Use whatever naming helps YOUR workflow. System is completely flexible.

### Context Operations
```bash
# Store any data
mcp__todo-mcp__context_set key:"any_name" value:"any content"

# Retrieve specific
mcp__todo-mcp__context_get key:"any_name" 

# Pattern deletion (if using prefixes)
mcp__todo-mcp__context_delete pattern:"temp_*"

# Full inventory
mcp__todo-mcp__context_get_all

# Statistics and health
mcp__todo-mcp__context_stats

# Emergency clear (requires force:true)
mcp__todo-mcp__context_clear force:true
```

## Performance Expectations

### Normal Operating Parameters
- **100 tasks**: <100ms response
- **1000 tasks**: Linear scaling, responsive
- **Bulk operations**: Atomic but may take time
- **Design target**: 100-200 tasks optimal

### Atomic Operations
**All bulk operations are all-or-nothing:**
```bash
# If ANY task ID invalid, ENTIRE operation rolls back
mcp__todo-mcp__todo_bulk operation:"set_priority" task_ids:[1,999,3] data:{priority:"high"}
# Task 999 doesn't exist → NO tasks updated
```

## MCP Server Operating Rules

### Critical Requirements
1. **ALWAYS test through MCP server** - Never isolated binaries
2. **NO direct file access** - Everything through MCP methods  
3. **Server controls validation** - Trust server responses
4. **Server maintains state** - Context and task consistency

## Summary: Todo MCP v0.6.8.1 Philosophy

1. **Verify Everything** - Never trust empty states
2. **Atomic Safety** - All-or-nothing operations
3. **Smart Automation** - Tag extraction, priority logic
4. **Resilient Recovery** - context_resume after interruptions
5. **Data Preservation** - Archive before delete
6. **Enforced Workflow** - Start before complete
7. **Single Focus** - One active task at a time
8. **Flexible Context** - Use any keys that help your work

This system enables sophisticated task management across multiple sessions with built-in intelligence, safety, and recovery capabilities.