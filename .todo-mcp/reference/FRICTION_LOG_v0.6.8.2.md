# Todo MCP v0.6.8.2 Friction Log

**Date**: 2025-08-28  
**Context**: Creating mastery documentation using v0.6.8.2

## 🔴 CRITICAL: Record significant findings you have with using Todo MCP v0.6.8.2 both successfully and any  friction you experience 

### 2025-08-29: Tag Filtering Completely Broken

**Issue**: `mcp__todo-mcp__todo_list` tag filtering is non-functional
- **Symptom**: ANY tag filter returns ALL 43 tasks
- **Tested**: `tags:["smart_pins_visual"]`, `tags:["sprint_005"]`, no filter - all return same 43 tasks
- **Impact**: Cannot filter tasks by work mode, making focused work impossible
- **Workaround**: Manually identify relevant tasks from full list

**Successful Operations**:
- `todo_bulk` with filters DOES work correctly
- Tag add/remove operations work (tags appear in display)
- Only the LIST filtering is broken

**Evidence**:
- Removed smart_pins_visual tag from Sprint 5 tasks (#974-#987)
- Added sprint_005 tag to same tasks
- Tasks now show [sprint_005] in display
- But filtering for either tag returns identical 43-task list

---

**Note**: This friction log will be updated as this instance of Claude-code Identifies any friction or experiences successes with using To-Do MCP and To-Do Write. .