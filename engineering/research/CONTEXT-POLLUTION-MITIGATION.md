# Context Pollution Mitigation Strategies for P2 Knowledge Base

*Managing conversation context when working with file-heavy knowledge bases*

## The Problem

When using the P2 Knowledge Base with Claude Code, each file read adds substantial content to the conversation context:
- YAML files: 200-500 lines each
- Pattern documents: 500-1000 lines
- Manifests: 300-600 lines
- After 10-20 queries, context becomes polluted with old file contents
- Performance degrades, responses slow, relevance drops

## Mitigation Strategies

### 1. Session Management (Primary Defense)

**Optimal Session Length: 2-3 Hours or 10-15 Complex Queries**

```yaml
triggers_for_new_session:
  - time: 2-3 hours elapsed
  - queries: 15+ file reads performed
  - topics: Switching between unrelated P2 topics
  - performance: Response time noticeably slower
  - confusion: AI mixing up previously read files
```

**Session Transition Protocol:**
1. Save current findings to a summary document
2. Note specific files/patterns discovered
3. Clear conversation
4. Start fresh with summary reference

### 2. Query Optimization (Reduce File Reads)

**DON'T:**
```
"Show me all Smart Pin modes"  # Reads 32 files!
"List every PASM2 instruction" # Reads 354 files!
```

**DO:**
```
"What Smart Pin modes handle serial communication?" # 2-3 files
"How does RDLONG work with hub memory?"           # 1-2 files
```

**Use Manifests First:**
- Always start with manifest files for navigation
- They provide summaries without full details
- Only drill into specific YAMLs when needed

### 3. Strategic File Reading

**Hierarchical Approach:**
```
1. Start with manifest (300 lines)
   ↓
2. Read category summary if exists (100 lines)
   ↓
3. Read specific YAML only when needed (200-500 lines)
```

**Batch Related Queries:**
```
GOOD: "I need UART configuration: show Smart Pin mode, 
       serial instructions, and example code"
       
BAD:  "Show Smart Pin UART"
      [10 minutes later]
      "Now show serial instructions"
      [10 minutes later]  
      "Now show examples"
```

### 4. Context Preservation Techniques

**Before Clearing:**
```markdown
## Session Summary - P2 UART Investigation
- Smart Pin Mode: P_ASYNC_TX (mode %0011)
- Key instructions: WYPIN, WXPIN, WRPIN
- Configuration: 8N1 at 115200 baud
- Example: See flash_fs.spin2 lines 145-180
```

**After Clearing:**
```
"Continue from UART investigation. Summary shows we found 
P_ASYNC_TX mode and flash_fs example. Now need error handling."
```

### 5. Operational Protocols

#### A. Start of Session
```
1. Check if continuing previous work
2. Load summary if exists
3. Set session goals to limit scope
4. Use manifest navigation first
```

#### B. During Session
```
1. Track file read count mentally
2. Batch related file reads together
3. Summarize findings periodically
4. Watch for performance degradation
```

#### C. End of Session/Before Clear
```
1. Create findings summary
2. List specific files that were valuable
3. Note patterns discovered
4. Save any code examples separately
```

### 6. Tool-Specific Optimizations

#### For Code Generation
```yaml
approach: targeted
steps:
  1. Ask for specific functionality needed
  2. Read only directly relevant YAMLs
  3. Generate code
  4. Clear conversation after code delivery
```

#### For Learning/Exploration
```yaml
approach: breadth-first
steps:
  1. Use manifests for overview
  2. Read category summaries
  3. Deep-dive into 2-3 specific items max
  4. Summarize and clear
```

#### For Debugging
```yaml
approach: surgical
steps:
  1. Identify exact issue
  2. Read only the specific instruction/mode
  3. Check one example
  4. Provide solution and clear
```

### 7. Warning Signs of Context Pollution

**Early Warnings:**
- Responses getting longer but less focused
- AI referencing files from much earlier
- Mixing up similar concepts
- Slower response times

**Critical Signs:**
- Wrong file contents being referenced
- Hallucinating file paths
- Timeout errors
- Incomplete responses

### 8. Recovery Procedures

**Quick Recovery:**
1. Stop current query
2. Summarize current findings in text file
3. Clear conversation
4. Restart with: "Continue from [summary]"

**Full Recovery:**
1. Export conversation useful parts
2. Create comprehensive summary
3. Start completely fresh session
4. Reference summary document

## Best Practices Summary

### ✅ DO:
- Clear every 2-3 hours proactively
- Use manifests for navigation
- Batch related queries together
- Create summaries before clearing
- Set specific session goals
- Use targeted file reads

### ❌ DON'T:
- Read entire categories at once
- Let sessions run 4+ hours
- Jump between unrelated topics
- Read files "just in case"
- Ignore performance degradation
- Lose findings when clearing

## Implementation Checklist

**For Users:**
- [ ] Set timer for 2-3 hour sessions
- [ ] Create `session-summaries/` folder
- [ ] Batch queries when possible
- [ ] Clear proactively, not reactively

**For AI Integration:**
- [ ] Add session management to CLAUDE-QUICKSTART.md
- [ ] Create templates for session summaries
- [ ] Document warning signs in AI-INTEGRATION.md
- [ ] Add context management to MCP server (future)

## Example Session Flow

```
Hour 0-1: Initial exploration
- Read manifests
- Identify target areas
- Read 5-8 specific files

Hour 1-2: Deep dive
- Focus on specific feature
- Read examples
- Generate code

Hour 2-2.5: Wrap up
- Test/verify code
- Create summary
- Document findings

Hour 2.5: Clear and break
- Save summary
- Clear conversation
- Take break

Hour 3: Fresh start
- Load summary
- Continue with clean context
```

---
*Remember: Context pollution is inevitable with file-heavy KBs. Proactive management is the key to maintaining quality interactions.*