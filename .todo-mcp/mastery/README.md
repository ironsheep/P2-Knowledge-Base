# Todo MCP Mastery Documentation

## What This Is

Definitive operational patterns for Todo MCP v0.6.8.2, refined through real-world usage across multiple Claude instances. These documents represent the synthesis of:
- Original v0.6.8.2 features
- Hard-won learnings from production usage
- Critical bug workarounds and recovery procedures
- Performance optimizations discovered through experience

## Document Structure

### Core Mastery Documents

1. **01_DUAL_SYSTEM_MASTERY_STRATEGY.md**
   - The fundamental architecture of TodoWrite + Todo MCP
   - The Iron Rule that prevents quality degradation
   - Task lifecycle and recovery patterns

2. **02_CONTEXT_HYGIENE_MASTERY.md**  
   - Critical insight: Value size matters more than key count
   - Pattern-based operations for efficiency
   - Auto-compaction protection strategies
   - Emergency recovery procedures

3. **03_TODO_MCP_MASTERY_INTERFACE.md**
   - Complete command reference with v0.6.8.2 features
   - Parameter patterns and data types
   - Discovery workflows using pattern matching
   - Session management excellence

4. **04_ANTI_PATTERN_ENFORCEMENT.md**
   - Critical mistakes that break everything
   - Enforcement mechanisms and recovery
   - Real costs from production failures
   - Success metrics for compliance

## How to Use These Documents

### For New Instances
1. Read documents 1-4 in order for complete understanding
2. Focus on "Standard Workflow" sections for immediate productivity
3. Reference anti-patterns to avoid common pitfalls

### For Existing Instances  
1. Review anti-patterns first to identify current issues
2. Implement context hygiene improvements
3. Adopt pattern-based operations for efficiency

### For CLAUDE.md Integration
Use `/setup/CLAUDE_MASTERY_INSERT.md` for the consolidated version that goes directly into CLAUDE.md

## Key Innovations in This Version

- **Value Size Principle**: "Context is for POINTERS, not PAYLOADS"
- **Pattern Operations**: Glob and regex support for bulk management
- **Temporal Filtering**: Find recently modified keys with minutes_back
- **Auto-Recovery**: context_resume placement enables self-healing
- **Filtered Workflows**: Priority and tag-based task management

## Three Learning Styles That Created This

These documents synthesize discoveries from three instances with distinct approaches:

1. **The Archivist** (p2kb): Documented everything, created tools for others
2. **The Pragmatist** (pnut-term-ts): Aggressively simplified, found optimizations  
3. **The Official** (todo-mcp): Maintained production docs, added new features

## Success Metrics

When properly implemented, these patterns deliver:
- Recovery from auto-compaction in <30 seconds
- 90% pattern-based operations (vs individual)
- Zero data loss through proper bridging
- Sustained productivity without degradation

## Version Note

These documents are for Todo MCP v0.6.8.2+ and include all features through that version. No version markers remain in the content - this is the definitive current truth.