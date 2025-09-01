# Opus Document Generation - Token Management Best Practices

## Understanding Token Boundaries

### Model Context Windows
| Model | Context Window | Typical Usage |
|---|---|---|
| **Opus 4.1** | 200,000 tokens | Rich document generation, tutorials |
| **Sonnet 4** | 200,000 tokens | Technical documentation, analysis |
| **Haiku 3.5** | 200,000 tokens | Simple formatting, validation |

### Token Estimation Rules of Thumb
- **1 token ≈ 0.75 words** (English text)
- **1,000 words ≈ 1,400 tokens**
- **1 page (250 words) ≈ 350 tokens**
- **Code is more token-dense** (1 line ≈ 10-15 tokens)

## Token Budget Planning for Document Generation

### Recommended Budget Allocation (200K total)

```
Creation Guide + Instructions:     10,000 tokens (5%)
Source Material to Reference:      30,000 tokens (15%)
Examples/Templates:                20,000 tokens (10%)
Generated Output Space:           100,000 tokens (50%)
Safety Buffer:                     40,000 tokens (20%)
---------------------------------------------------
Total:                            200,000 tokens
```

### Creation Guide Size Guidelines

**Sweet Spot**: 5,000-15,000 tokens (3,500-10,000 words)

| Guide Size | Tokens | Assessment |
|---|---|---|
| < 5,000 tokens | < 3,500 words | ✅ Lean and efficient |
| 5,000-10,000 | 3,500-7,000 words | ✅ **OPTIMAL RANGE** |
| 10,000-15,000 | 7,000-10,000 words | ⚠️ Still fine, getting large |
| 15,000-20,000 | 10,000-14,000 words | ⚠️ Consider splitting |
| > 20,000 | > 14,000 words | ❌ Too large, split required |

## Optimization Strategies

### When Creation Guide Gets Too Large

#### Strategy 1: Split by Purpose
```
creation-guide-core.md         (5K tokens)  - Essential rules
creation-guide-examples.md     (10K tokens) - Reference examples  
creation-guide-patterns.md     (5K tokens)  - Semantic patterns
creation-guide-voice.md        (5K tokens)  - Voice guidelines
```

#### Strategy 2: Progressive Generation
```
Phase 1: Core guide + Part I content
Phase 2: Core guide + Part II content  
Phase 3: Core guide + Part III content
Phase 4: Validation checklist only
```

#### Strategy 3: Reference External Docs
Instead of inline content:
- "See semantic-types.md for block patterns"
- "See voice-guide.md for tone examples"
- "Refer to style-examples.md for formatting"

### Output Length Management

**For Large Documents (400+ pages)**:

1. **Generate in Parts**:
   - Part I: Fundamentals (100 pages)
   - Part II: Mode Details (200 pages)
   - Part III: Advanced Topics (100 pages)

2. **Request Continuation**:
   ```
   "Continue from where you left off at Mode %01010"
   ```

3. **Use Markers**:
   ```markdown
   <!-- GENERATION CHECKPOINT: Mode %01010 complete -->
   ```

## Red Flags and Warning Signs

### ⚠️ Token Overflow Indicators

1. **Input Too Large**:
   - Creation guide > 20,000 tokens
   - Multiple reference documents needed
   - Opus asking for clarification frequently

2. **Output Truncation**:
   - Generation stops mid-sentence
   - "Continue" needed multiple times
   - Losing context between continuations

3. **Quality Degradation**:
   - Inconsistent formatting late in document
   - Forgetting earlier instructions
   - Repetitive content

## Best Practices for Opus Generation

### DO:
✅ **Keep creation guides focused** (under 10K tokens)  
✅ **Provide clear structure** in instructions  
✅ **Use semantic markers** for post-processing  
✅ **Request manifests** of what was generated  
✅ **Plan for multi-phase generation** for large docs  

### DON'T:
❌ **Overload with formatting instructions** (handle in post)  
❌ **Include redundant examples** (a few good ones suffice)  
❌ **Mix multiple documents** in one generation  
❌ **Forget the safety buffer** (20% minimum)  

## Practical Examples

### Example: Smart Pins Green Book Generation

```
Token Budget:
- Creation guide:        5,000 tokens ✅
- Titus narratives:     30,000 tokens (source)
- Code examples:        20,000 tokens (reference)
- Generated output:     ~100,000 tokens (450 pages)
- Buffer:               45,000 tokens
Total:                  200,000 tokens (FITS!)
```

### Example: PASM2 Manual Generation

```
Token Budget:
- Creation guide:        8,000 tokens ✅
- Instruction specs:    40,000 tokens (source)
- Examples:             15,000 tokens
- Generated output:     ~80,000 tokens (350 pages)
- Buffer:               57,000 tokens
Total:                  200,000 tokens (FITS!)
```

## Document Size Estimates

| Document Type | Typical Size | Token Estimate | Generation Strategy |
|---|---|---|---|
| Quick Reference | 50-100 pages | 20-40K tokens | Single pass |
| User Manual | 200-300 pages | 80-120K tokens | 2-3 phases |
| Complete Tutorial | 400-500 pages | 160-200K tokens | 4-5 phases |
| Technical Reference | 600+ pages | 240K+ tokens | Multiple sessions |

## Key Takeaways

1. **200K context is generous** - Most creation guides use < 5% of available space
2. **Output length is usually the limit** - Not input instructions
3. **Plan for ~50% output allocation** - Leave room for Opus to work
4. **Keep 20% safety buffer** - Prevents truncation
5. **Split large generations** - Better quality than cramming

## Quick Reference Formula

```
Safe Generation Size = (200,000 - Creation_Guide - Source_Docs) × 0.5

Example:
Safe Size = (200,000 - 10,000 - 30,000) × 0.5 = 80,000 tokens
          = ~57,000 words = ~230 pages
```

---

**Remember**: Token management is about leaving Opus room to think and create, not about cramming in maximum content. Quality over quantity!