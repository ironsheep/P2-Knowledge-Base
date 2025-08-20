# Claude Integration Command for Mastery System

## Command for New Claude Instances

When todo-init-enhanced runs with mastery package available, it will output:

```
Claude: Complete the mastery system setup:
1. Read: .todo-mcp/mastery/README.md
2. MERGE IMMEDIATELY: .todo-mcp/mastery/05_CLAUDE_MD_MASTERY_INSERT.md into your CLAUDE.md
   This provides instant mastery-level operation
3. Explore: .todo-mcp/mastery/ for comprehensive documentation
4. Begin: Using dual-system workflow (TodoWrite + MCP)
```

## The Merge Command

**Exact instruction for Claude**:

```
Read the file .todo-mcp/mastery/05_CLAUDE_MD_MASTERY_INSERT.md and merge its contents into your CLAUDE.md file immediately. This provides instant mastery-level Todo MCP operation without learning friction.

After merging, begin using the dual-system workflow:
- MCP tasks for persistent, session-spanning work
- TodoWrite for current task breakdown only (never multiple MCP task IDs)
- Always start with: mcp__todo-mcp__context_resume

The mastery documentation is available in .todo-mcp/mastery/ for comprehensive reference.
```

## Recognition Pattern

**Location Strategy**:
- ✅ **Fixed location**: `.todo-mcp/mastery/05_CLAUDE_MD_MASTERY_INSERT.md` (predictable)
- ✅ **Auto-detection**: todo-init places it there automatically
- ✅ **Clear instructions**: BRIEFING.md tells Claude exactly what to do

**Why this works**:
1. **Predictable path**: Always `.todo-mcp/mastery/05_CLAUDE_MD_MASTERY_INSERT.md`
2. **Automatic discovery**: todo-init creates and references it
3. **Clear action**: "MERGE IMMEDIATELY" instruction is unambiguous
4. **Instant benefit**: Provides mastery-level operation from first use

## Implementation Flow

### 1. Package Creation
```bash
# Build mastery package
./scripts/create-mastery-package.sh
# Produces: builds/todo-mcp-mastery-v0.6.8.1.tar.gz
```

### 2. Container Deployment
```bash
# Deploy to container tools
cp builds/todo-mcp-mastery-v0.6.8.1.tar.gz /opt/container-tools/todo-mcp-mastery.tar.gz
```

### 3. Project Initialization
```bash
# Use enhanced todo-init
todo-init
# Auto-detects mastery package, extracts to .todo-mcp/mastery/
# Creates .todo-mcp/mastery/05_CLAUDE_MD_MASTERY_INSERT.md
# Instructs Claude to merge immediately
```

### 4. Claude Integration
```bash
# Claude receives instruction and automatically:
# 1. Reads .todo-mcp/mastery/README.md
# 2. Merges .todo-mcp/mastery/05_CLAUDE_MD_MASTERY_INSERT.md into CLAUDE.md
# 3. Begins using mastery patterns immediately
```

## Success Criteria

**Successful integration when**:
- [ ] Claude merges CLAUDE.md insert without friction
- [ ] Begins using dual-system workflow immediately  
- [ ] Applies anti-pattern enforcement mechanisms
- [ ] Uses mastery-level parameter patterns
- [ ] Starts sessions with `context_resume`
- [ ] Maintains TodoWrite discipline (single task only)

## Fallback Strategy

**If mastery package not available**:
- todo-init installs legacy best-practices (marked as obsolete)
- Claude gets basic guidance but not mastery-level operation
- Recommendation to obtain mastery package for full benefit

## Benefits of This Approach

1. **Zero learning curve**: Instant mastery-level operation
2. **Predictable deployment**: Same process every time
3. **Automatic integration**: Claude knows exactly what to do
4. **Comprehensive coverage**: Full mastery system in one command
5. **Smooth transitions**: Migration playbook for existing instances

This system transforms Todo MCP from "tool to learn" into "immediate expert operation" through systematic knowledge delivery.