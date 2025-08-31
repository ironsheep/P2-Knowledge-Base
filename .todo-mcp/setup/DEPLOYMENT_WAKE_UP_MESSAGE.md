# Deployment Wake-Up Message for Claude Instances

## Copy and Paste This Complete Message to Each Awakened Instance:

---

I've deployed new v0.6.8.2 merged mastery documentation to your .todo-mcp/ folder. This combines learnings from all three instances and fixes known issues. Please execute this upgrade sequence:

1. **Check your new documentation**:
```bash
mcp__todo-mcp__context_resume  # Verify current state
ls .todo-mcp/mastery/  # Confirm new files are there
cat .todo-mcp/setup/CLAUDE_MASTERY_INSERT.md | head -20  # See deployment instructions
```

2. **Update your CLAUDE.md**:
- Read the deployment instructions in `.todo-mcp/setup/CLAUDE_MASTERY_INSERT.md`
- Remove ALL existing Todo MCP content from CLAUDE.md (v0.6.8, v0.6.8.1 sections)
- Insert the new content from CLAUDE_MASTERY_INSERT.md EARLY in CLAUDE.md (right after project info)
- This placement is CRITICAL for auto-compaction recovery

3. **Verify the upgrade**:
```bash
mcp__todo-mcp__context_resume  # Should work with new patterns
mcp__todo-mcp__context_get pattern:"lesson_*"  # Test pattern search
mcp__todo-mcp__todo_next  # Check task recommendations
```

4. **Quick review of what's new**:
- Pattern-based context_get now works: `pattern:"temp_*"` 
- Dual parameters fixed: both position_id and task_id work
- VALUE SIZE matters more than key count for context
- Your instance-specific discoveries have been preserved

5. **Acknowledge completion**:
```bash
mcp__todo-mcp__context_set key:"v0.6.8.2_merge_deployed" value:"Successfully updated $(date)"
```

The merge fixes your known friction points while preserving your unique discoveries. Your protected files (preserved-context/, friction logs) remain untouched.

---

## Additional Notes for p2kb Instance

Add this for p2kb specifically:
> Great news - pattern-based context_get is now available, solving the "guess the key name" friction you documented in your friction log!

## Expected Outcome

After following these steps, the instance should:
- Have updated CLAUDE.md with new mastery content
- Be able to use all v0.6.8.2 features immediately
- Retain all instance-specific customizations
- Set a context marker confirming successful deployment