# Migration Playbook: Transitioning Instances to Mastery Documentation

## Overview and Philosophy

**Purpose**: Smooth migration of running Claude instances from legacy documentation to mastery-level guidance without disrupting established workflows or causing confusion.

**Core Principle**: **Minimize disruption while maximizing benefit**. Running instances have established patterns, context, and active work that must be preserved during transition.

## Installation Method

### Step 1: Install Mastery Documentation
1. **Copy the mastery package** to your workspace:
   - Extract/copy the `todo-mcp` folder to your project root
   - Verify structure: `.todo-mcp/mastery/[6 mastery documents + README.md]`

2. **Add mastery reference to CLAUDE.md**:
   ```markdown
   ## 🎯 Mastery Documentation (Local)

   The following mastery documentation has been installed locally:

   ### Core Mastery
   - **Interface Guide**: `.todo-mcp/mastery/01_TODO_MCP_MASTERY_INTERFACE.md`
   - **Strategy Guide**: `.todo-mcp/mastery/02_DUAL_SYSTEM_MASTERY_STRATEGY.md`
   - **Anti-Patterns**: `.todo-mcp/mastery/03_ANTI_PATTERN_ENFORCEMENT.md`
   - **Migration Guide**: `.todo-mcp/mastery/04_MIGRATION_PLAYBOOK.md`

   ### Integration
   - **CLAUDE.md Setup**: `.todo-mcp/mastery/05_CLAUDE_MD_MASTERY_INSERT.md`
   - **Version Transitions**: `.todo-mcp/mastery/06_VERSION_TRANSITION_GUIDES.md`

   ### Reference
   - **Complete Index**: `.todo-mcp/mastery/README.md`

   **Usage**: Refer to these documents for todo-mcp mastery techniques, workflow optimization, and best practices.
   ```

### Step 2: Claude Adoption Instructions
Tell Claude: *"I've installed the todo-mcp mastery documentation. Please read and adopt the mastery patterns from `.todo-mcp/mastery/05_CLAUDE_MD_MASTERY_INSERT.md` and integrate them into your workflow."*

This triggers Claude to:
1. Read the mastery insert document  
2. Update its internal patterns and procedures
3. Begin using enhanced workflows immediately
4. Maintain existing work continuity

## Migration Scenarios

### Scenario 1: Clean Slate Migration (OPTIMAL)
**When**: Between major sprint boundaries, no active work
**Risk**: LOW
**Disruption**: MINIMAL

#### Process
1. **Complete all active tasks**
   ```bash
   mcp__todo-mcp__todo_archive  # Clean completed work
   mcp__todo-mcp__todo_list     # Verify no in_progress tasks
   ```

2. **Create transition backup**
   ```bash
   mcp__todo-mcp__project_dump include_context:true
   # Note filename for potential rollback
   ```

3. **Archive valuable context**
   ```bash
   mcp__todo-mcp__context_get_all  # Review for valuable lessons
   # Manually save critical insights to documentation
   mcp__todo-mcp__context_clear force:true  # Fresh start
   ```

4. **Replace documentation files**
   - Update CLAUDE.md with mastery content
   - Replace process documentation  
   - Install new reference guides

5. **Verify migration success**
   ```bash
   mcp__todo-mcp__context_resume  # Should show clean state
   # Test basic operations with new patterns
   ```

### Scenario 2: Safe Transition Window (RECOMMENDED)
**When**: After task completion, before next task start
**Risk**: LOW-MEDIUM  
**Disruption**: CONTROLLED

#### Process
1. **Complete current task safely**
   ```bash
   mcp__todo-mcp__todo_complete position_id:1  # Finish active work
   mcp__todo-mcp__todo_archive  # Clean completed tasks
   ```

2. **Preserve active context**
   ```bash
   # Backup current state
   mcp__todo-mcp__project_dump include_context:true
   
   # Identify valuable context to preserve
   mcp__todo-mcp__context_get_all
   # Note lesson_*, workaround_*, recovery_* keys to keep
   ```

3. **Staged documentation replacement**
   - Replace CLAUDE.md with mastery version
   - Update critical process docs first
   - Keep existing context temporarily for reference

4. **Validate transition**
   ```bash
   # Test core operations with new patterns
   mcp__todo-mcp__todo_create content:"Migration test" estimate_minutes:15
   mcp__todo-mcp__todo_start position_id:1
   mcp__todo-mcp__todo_complete position_id:1
   mcp__todo-mcp__todo_archive
   ```

5. **Context cleanup** (after validation)
   ```bash
   # Clean outdated patterns, preserve valuable learnings
   mcp__todo-mcp__context_delete pattern:"temp_*"
   mcp__todo-mcp__context_delete pattern:"session_*"
   # Keep lesson_*, workaround_*, recovery_*
   ```

### Scenario 3: Mid-Task Transition (RISKY)
**When**: Emergency upgrade needed, active work in progress
**Risk**: MEDIUM-HIGH
**Disruption**: SIGNIFICANT

#### Process
1. **Preserve current work state**
   ```bash
   # Emergency backup
   mcp__todo-mcp__project_dump include_context:true
   
   # Save TodoWrite state if populated
   mcp__todo-mcp__context_set key:"migration_todowrite_backup" value:"[current TodoWrite]"
   
   # Document current work status manually
   mcp__todo-mcp__context_set key:"migration_work_status" value:"Working on [task details], next step: [specific action]"
   ```

2. **Minimal documentation update**
   - Replace CLAUDE.md only initially
   - Keep existing process docs until work completes
   - Note interface changes affecting current work

3. **Continue work with hybrid approach**
   - Use new parameter patterns for new operations
   - Complete current task with existing patterns if stable
   - Document any conflicts or issues

4. **Full migration after task completion**
   - Follow "Safe Transition Window" process
   - Restore work state if needed
   - Clean up migration context keys

### Scenario 4: Instance-Driven Migration (COLLABORATIVE)
**When**: Instance has established expertise, can evaluate changes
**Risk**: LOW
**Disruption**: CONTROLLED

#### Process
1. **Present migration proposal to instance**
   ```
   "I have access to updated Todo MCP mastery documentation that incorporates 
   learnings from three instances plus v0.6.8.1 improvements. 
   
   The new documentation includes:
   - Enhanced crash recovery protocols
   - Anti-pattern enforcement mechanisms  
   - Improved context hygiene strategies
   - Dual-system integration best practices
   
   Would you like to review and adopt these improvements?
   Current state will be preserved during transition."
   ```

2. **Collaborative review**
   - Instance reviews new documentation
   - Identifies conflicts with current patterns
   - Suggests adaptation strategies
   - Provides feedback on improvements

3. **Incremental adoption**
   - Instance chooses adoption timeline
   - Gradually incorporates new patterns
   - Validates improvements against current work
   - Maintains what works, improves what doesn't

## Version-Specific Considerations

### v0.6.8 → v0.6.8.1 Parameter Changes
**Key Change**: Some functions may require `position_id` instead of `id` parameter

#### Migration Steps
1. **Test current patterns**
   ```bash
   # Test existing CLAUDE.md patterns
   mcp__todo-mcp__todo_create content:"Parameter test" estimate_minutes:5
   mcp__todo-mcp__todo_start position_id:1  # Verify this works
   mcp__todo-mcp__todo_complete position_id:1
   ```

2. **Update parameter patterns gradually**
   - Start with new task operations
   - Update existing scripts/automation
   - Document any interface changes

3. **Validate automation**
   - Test bulk operations with new patterns
   - Verify context operations unchanged
   - Check backup/restore functionality

### Context Hygiene Upgrades
**New Standard**: 40-50 key target, systematic cleanup

#### Migration Process
1. **Current context audit**
   ```bash
   mcp__todo-mcp__context_stats  # Check current size
   mcp__todo-mcp__context_get_all  # Review all keys
   ```

2. **Identify cleanup opportunities**
   - Old session keys (>8 hours)
   - Temporary calculations (>4 hours)
   - Completed task tracking (>1 hour after completion)
   - Obsolete workarounds

3. **Implement new hygiene patterns**
   - Adopt prefix-based organization if beneficial
   - Set up automated cleanup rules
   - Establish monitoring thresholds

## Recovery Procedures

### Migration Rollback
**If migration causes issues**:

1. **Immediate rollback**
   ```bash
   mcp__todo-mcp__project_restore file:"pre_migration_backup.json" mode:"replace" include_context:true
   ```

2. **Restore documentation**
   - Revert CLAUDE.md to previous version
   - Restore original process docs
   - Document migration failure cause

3. **Analysis and retry**
   - Identify specific failure points
   - Adjust migration approach
   - Plan alternative transition strategy

### Partial Migration Recovery
**If some parts work, others don't**:

1. **Preserve working elements**
   - Keep new patterns that work
   - Revert problematic changes only
   - Document hybrid approach

2. **Incremental improvement**
   - Fix specific issues identified
   - Test individual improvements
   - Gradual full adoption

## Success Criteria

### Migration Successful When:
- [ ] All core Todo MCP operations work with new patterns
- [ ] Context hygiene improved (key count reduced if needed)
- [ ] Recovery procedures tested and functional
- [ ] Instance can operate efficiently with new documentation
- [ ] No disruption to ongoing work
- [ ] Anti-pattern enforcement mechanisms active

### Quality Gates
1. **Functional**: Basic operations work correctly
2. **Performance**: No degradation in operation speed  
3. **Recovery**: Crash recovery procedures tested
4. **Documentation**: Instance understands new patterns
5. **Continuity**: Can resume interrupted work seamlessly

## Communication Templates

### Initial Migration Proposal
```
"Available: Todo MCP mastery documentation with enhanced crash recovery, 
anti-pattern prevention, and improved context management. 

Current work will be preserved. Migration can be:
- Immediate (if between tasks)  
- Scheduled (after current sprint)
- Gradual (adopt new patterns incrementally)

Recommend: [specific approach based on current state]
Backup: [pre-migration backup location]
Rollback: Available if issues occur

Proceed with migration?"
```

### Migration Complete Confirmation
```
"Migration complete. New capabilities:
- Enhanced crash recovery (2-minute protocol)
- Anti-pattern enforcement (quality protection)  
- Improved context hygiene (performance optimization)
- Systematic parameter patterns (fewer errors)

All data preserved. Rollback available if needed.
Ready to continue with mastery-level patterns."
```

## Meta-Learning

### What Makes Migration Successful
1. **Preservation first**: Protect existing valuable patterns
2. **Incremental change**: Don't change everything at once
3. **Clear benefits**: Instance understands improvement value
4. **Easy rollback**: Confidence that change is reversible
5. **Collaborative approach**: Instance participates in migration decision

### Common Migration Failures
1. **Forced replacement**: Changing too much without instance buy-in
2. **Lost context**: Not preserving valuable existing patterns  
3. **No validation**: Not testing new patterns before full adoption
4. **Poor timing**: Migrating during critical work phases
5. **No rollback plan**: Creating fear of change

### Best Practices
- **Start with least disruptive approach**
- **Preserve more than you think necessary**
- **Test thoroughly before full commitment**
- **Document migration reasoning**
- **Plan for partial success scenarios**

## Summary

Successful migration balances **improvement opportunity** with **continuity preservation**. The goal is **enhanced capability** without **workflow disruption**.

**Key Principle**: Better to migrate slowly and successfully than quickly and disruptively. Running instances have valuable established patterns that should be preserved and enhanced, not replaced wholesale.