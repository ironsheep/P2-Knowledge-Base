# P2 Idiom Extraction Framework

## Vision
Extract, document, and share common P2 programming patterns from OBEX to accelerate learning and ensure code quality.

## What is a P2 Idiom?

A P2 idiom is a recurring pattern in P2 code that represents the community's preferred way of solving a common problem. Examples:
- How to safely launch and stop cogs
- How to set up Smart Pins for protocols
- How to handle inter-cog communication
- How to structure a driver object

## Extraction Methodology

### 1. Pattern Identification Criteria

An idiom qualifies for documentation when:
- Appears in 3+ independent OBEX objects
- Used by recognized community experts
- Solves a specific, recurring problem
- Has clear advantages over alternatives

### 2. Confidence Levels

- **Gold Standard**: Used by Chip Gracey or Parallax official code
- **Community Proven**: 10+ OBEX implementations
- **Emerging Pattern**: 3-5 implementations, gaining adoption
- **Experimental**: Promising but needs validation

### 3. Documentation Template

```markdown
# P2 Idiom: [Pattern Name]

## Metadata
- **Pattern ID**: P2-IDIOM-XXX
- **Category**: [Driver/Communication/Memory/Control/etc.]
- **Confidence**: [Gold/Proven/Emerging/Experimental]
- **First Seen**: [OBEX object and date]
- **Frequency**: Found in XX% of relevant OBEX objects

## Problem
What problem does this idiom solve?

## Solution
The standard P2 way to solve this problem.

## Implementation
```spin2
' Standard implementation with comments
```

## Examples from OBEX
- [Object Name 1] by [Author] - [specific use]
- [Object Name 2] by [Author] - [variation]
- [Object Name 3] by [Author] - [enhancement]

## Variations
Different ways the community implements this pattern.

## Anti-patterns
Common mistakes to avoid.

## Related Idioms
- [Related Pattern 1]
- [Related Pattern 2]

## Rationale
Why this pattern emerged as the standard.

## Performance Notes
Timing, memory usage, cog utilization impacts.
```

## Categories of Idioms

### 1. Structural Idioms
- Object initialization/cleanup
- Method naming conventions
- Public/private organization
- Constant definitions

### 2. Resource Management
- Cog allocation and cleanup
- Pin allocation patterns
- Hub RAM sharing
- Lock usage

### 3. Communication Patterns
- Mailbox implementation
- Ring buffer usage
- Command/response protocols
- Event signaling

### 4. Smart Pin Patterns
- Mode configuration sequences
- Cascading pins for complex protocols
- Timing synchronization
- Error recovery

### 5. Performance Patterns
- When to use inline PASM2
- Hub timing optimization
- Streamer usage
- CORDIC integration

### 6. Protocol Implementation
- Bit-banging vs Smart Pins
- Timing compensation
- Error handling
- State machines

## Extraction Process

### Phase 1: Inventory
1. Catalog all OBEX objects
2. Categorize by functionality
3. Identify most downloaded/used

### Phase 2: Pattern Mining
1. Analyze top objects in each category
2. Identify recurring code structures
3. Compare implementations

### Phase 3: Documentation
1. Document patterns using template
2. Cross-reference with silicon docs
3. Validate with community experts

### Phase 4: Validation
1. Test patterns on hardware
2. Get community feedback
3. Refine documentation

### Phase 5: Distribution
1. Publish idiom dictionary
2. Create searchable database
3. Integrate with AI training

## Success Metrics

- Number of documented idioms
- Community adoption rate
- Reduction in common mistakes
- AI code generation quality
- New user success rate

## Example Extracted Idiom

### P2 Idiom: Safe Cog Management

**Problem**: Need to start/stop cogs without resource leaks

**Solution**: Always stop before start, track cog ID + 1

```spin2
VAR
  long cog_id  ' 0 = stopped, 1-8 = cog 0-7 running

PUB Start() : result
  Stop()  ' Always cleanup first
  cog_id := cogspin(NEWCOG, CogTask(), @stack) + 1
  return cog_id

PUB Stop()
  if cog_id
    cogstop(cog_id - 1)
    cog_id := 0
```

**Frequency**: 92% of multi-cog OBEX objects

**Rationale**: 
- Adding 1 to cog ID allows 0 to mean "stopped"
- Stop() before Start() prevents orphaned cogs
- Pattern expected by P2 community

## Next Steps

1. Create idiom extraction scripts
2. Build idiom database schema
3. Start with top 10 OBEX objects
4. Document first 5 core idioms
5. Get community validation