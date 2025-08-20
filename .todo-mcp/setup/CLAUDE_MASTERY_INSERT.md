# CLAUDE.md Mastery Insert: Todo MCP v0.6.8.1

## Deploy-Ready CLAUDE.md Section

**Purpose**: Immediate mastery-level operation, zero friction startup

**Installation**: Insert this section into any project's CLAUDE.md file

---

## 🎯 Todo MCP v0.6.8.1 Mastery Operations

### SESSION START PROTOCOL (ALWAYS FIRST)
```bash
mcp__todo-mcp__context_resume    # Primary recovery command
mcp__todo-mcp__todo_list         # Current task state
# Ready to continue with full context restoration
```

### Dual System Strategy (IRON RULE)
**MCP Tasks**: Persistent, session-spanning, permanent ID «#N»
**TodoWrite**: Current task breakdown only, cleared on completion

```bash
# CORRECT workflow
mcp__todo-mcp__todo_create content:"Feature implementation" estimate_minutes:180
mcp__todo-mcp__todo_start position_id:1
TodoWrite: ["Step 1", "Step 2", "Step 3"]  # Single task breakdown only
# Work through steps...
mcp__todo-mcp__todo_complete position_id:1
TodoWrite: []  # Clear for next task
```

**NEVER**: Multiple MCP task IDs in TodoWrite (quality degradation)

### Core Parameter Patterns (v0.6.8.1)
```bash
# Most functions use position_id (interactive) or task_id (automation)
mcp__todo-mcp__todo_start position_id:1
mcp__todo-mcp__todo_pause position_id:1 reason:"Blocked"
mcp__todo-mcp__todo_resume position_id:1

# Dual-parameter functions (complete, tag_add, tag_remove)
mcp__todo-mcp__todo_complete position_id:1       # OR task_id:"#22"
mcp__todo-mcp__todo_tag_add position_id:1 tags:["urgent"]

# Critical data types
estimate_minutes:60        # Number, never string
priority:"high"           # lowercase: critical/high/medium/low/backlog
force:true               # Boolean, never string
```

### Context Hygiene (40-Key Target)
```bash
# Persistent context (KEEP)
lesson_*, workaround_*, recovery_*, friction_*

# Temporary context (DELETE after use)
temp_*, current_*, session_*, task_#N_*

# Regular cleanup
mcp__todo-mcp__context_delete pattern:"temp_*"
mcp__todo-mcp__context_delete pattern:"task_#N_*"  # After task completion
```

### Data Safety (ALWAYS)
```bash
# SAFE archiving (preserves backup)
mcp__todo-mcp__todo_archive

# Complete backup before risky operations  
mcp__todo-mcp__project_dump include_context:true

# Recovery
mcp__todo-mcp__project_restore file:"filename.json" mode:"replace"
```

### Anti-Pattern Prevention

**Policy Override Prevention**:
- Never ignore explicit instructions for perceived efficiency
- Maintain same process standards whether user present or absent
- Confirm before violating established workflow rules

**TodoWrite Discipline**:
- ONE MCP task breakdown only
- Clear TodoWrite on task completion
- Save TodoWrite state to context for crash recovery

**Parameter Verification**:
- Always verify function parameter requirements
- Use correct data types (number vs string vs boolean)
- Test new patterns before assuming they work

### Quick Recovery Commands
```bash
mcp__todo-mcp__context_resume     # "I'm back" - primary recovery
mcp__todo-mcp__todo_next          # Smart task recommendation
mcp__todo-mcp__todo_archive       # Clean completed tasks
mcp__todo-mcp__context_stats      # Context health check
```

### Task Lifecycle (ENFORCED)
1. **Start** before work: `todo_start position_id:1`
2. **Complete** after work: `todo_complete position_id:1`
3. **Archive** when done: `todo_archive`
4. Only ONE task `in_progress` at a time (auto-enforced)

### Version Transition Protocol
**Safe transition points** (preference order):
1. Between sprints (optimal)
2. After task completion + archive (safe)
3. Between tasks (acceptable)
4. Emergency with state preservation (risky)

**Always backup before version changes**:
```bash
mcp__todo-mcp__project_dump include_context:true
```

---

## Implementation Notes

### For New Projects
1. Install this section in CLAUDE.md
2. Test basic operations
3. Establish context hygiene routine
4. Begin with dual-system workflow

### For Existing Projects
1. Archive existing todo-mcp content
2. Preserve valuable existing patterns
3. Gradually adopt new discipline
4. Validate improvements before full commitment

### Deep Learning Resources
For comprehensive understanding, study the mastery documentation:
- `.todo-mcp/mastery/01_DUAL_SYSTEM_MASTERY_STRATEGY.md` - Complete workflow patterns
- `.todo-mcp/mastery/02_CONTEXT_HYGIENE_MASTERY.md` - Context management excellence
- `.todo-mcp/mastery/03_TODO_MCP_MASTERY_INTERFACE.md` - Complete technical reference
- `.todo-mcp/mastery/04_ANTI_PATTERN_ENFORCEMENT.md` - Quality protection mechanisms
- `.todo-mcp/mastery/05_PARAMETER_CONFUSION_ROOT_CAUSE_v0.6.8.1.md` - Technical analysis

### Key Success Patterns
- **Context bridge**: Save TodoWrite state to context for crash recovery
- **Verification**: Always verify "empty" responses with context_get_all
- **Process consistency**: Same quality standards under all conditions
- **Recovery confidence**: Systematic procedures enable reliable workflows
- **Pattern-based cleanup**: Use context_delete with patterns, not individual keys

---

**This insert provides complete operational knowledge for immediate mastery-level Todo MCP usage. References above provide deep learning for comprehensive understanding.**