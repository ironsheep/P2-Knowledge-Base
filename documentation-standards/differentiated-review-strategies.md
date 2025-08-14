# Differentiated Review Strategies

*Different document types need different review approaches*

---

## 📊 Document Type Classification

### Type A: Technical Reference Documents
**Examples**: PASM2 Manual, Silicon Docs, Instruction Set Reference
**Primary Concern**: Technical accuracy
**Reviewers Needed**: Expert practitioners

### Type B: Learning/Tutorial Documents  
**Examples**: DeSilva Guide, Getting Started, P1-to-P2 Transition
**Primary Concern**: Clarity and learning effectiveness
**Reviewers Needed**: Mixed expertise levels

---

## 🔬 Technical Reference Review Process

### Who Should Review:
- **Expert Practitioners**: Those using PASM2 daily
- **Chip Designers**: Those who understand silicon
- **Tool Developers**: Compiler/assembler authors
- **Production Users**: Shipping products with P2

### What They Review For:
```markdown
## Technical Accuracy Checklist
- [ ] Instruction behavior EXACTLY correct
- [ ] Timing cycles precisely documented  
- [ ] Encoding bits accurate to silicon
- [ ] Flag effects match hardware
- [ ] Edge cases documented
- [ ] Errata/gotchas noted
```

### How They Review:
- **Line-by-line verification** against their experience
- **Test code execution** to verify claims
- **Cross-reference** with their working code
- **Binary verification** of encodings

### Forum Post for Technical Review:
```
⚙️ TECHNICAL REVIEW NEEDED: PASM2 Manual v0.9

P2 assembly experts - we need your deep technical verification.

**Who should review**: If you write PASM2 regularly
**Focus**: Technical accuracy, not teaching quality

**Critical areas needing expert eyes:**
- Instruction timing in special cases
- Flag effects in edge conditions  
- Pipeline behavior documentation
- Hub timing windows

**How to review**:
- Test questionable claims in your code
- Compare against your working drivers
- Flag ANY discrepancy, no matter how small

This will become THE reference - accuracy is paramount.
```

### Review Template for Technical Docs:
```markdown
TECHNICAL ERROR REPORT
Instruction/Section: [specific reference]
Documented behavior: [what manual says]
Actual behavior: [what really happens]
Test code to reproduce: [code snippet]
Silicon version tested: [Rev B/C]
```

---

## 📚 Learning Document Review Process

### Who Should Review (THREE groups):
1. **Target Audience**: Those learning P2 now
2. **Recent Learners**: Learned P2 in last year
3. **Teachers**: Those who teach/mentor others

### What They Review For:

#### For Beginners:
```markdown
## Learning Effectiveness Checklist
- [ ] Can I follow this without getting lost?
- [ ] Are concepts introduced in logical order?
- [ ] Do examples make sense?
- [ ] Is pacing too fast/slow?
- [ ] Are assumptions about prior knowledge clear?
- [ ] Can I actually DO something after reading?
```

#### For Recent Learners:
```markdown
## "I Wish I'd Known" Checklist
- [ ] Does this cover what confused me?
- [ ] Are common mistakes addressed?
- [ ] Would this have helped me learn faster?
- [ ] What's missing that I needed?
- [ ] Are explanations at the right level?
```

#### For Teachers:
```markdown
## Pedagogical Review Checklist
- [ ] Learning progression appropriate?
- [ ] Exercises reinforce concepts?
- [ ] Common misconceptions addressed?
- [ ] Multiple learning styles supported?
- [ ] Scaffolding sufficient?
```

### Forum Post for Learning Review:
```
📖 LEARNING REVIEW: DeSilva-Style P2 Guide Chapters 1-3

Calling all P2 learners and teachers!

**Who should review**: 
- Currently learning P2 (most important!)
- Learned P2 recently
- Teaching others P2

**What we need to know**:
- Is this actually helpful for learning?
- What confused you?
- What needs more explanation?
- Are examples helpful?
- Is the pace right?

**Don't worry about**:
- Perfect technical accuracy (experts will check)
- Grammar/spelling (we'll fix those)

**Just tell us**: Does this help you learn?

Your experience matters most for this type of document!
```

### Review Template for Learning Docs:
```markdown
LEARNING FEEDBACK
My experience level: [Beginner/Intermediate/Expert]
Chapter/Section: [reference]

What worked well:
- [What helped me understand]

What confused me:
- [What I had to read multiple times]

What's missing:
- [What I wish was explained]

Suggestions:
- [How to make it clearer]
```

---

## 🎯 Differentiated Review Priorities

### Technical References Priority Order:
1. **Accuracy** - Must be 100% correct
2. **Completeness** - Nothing missing
3. **Precision** - No ambiguity
4. **Organization** - Easy to find information
5. **Examples** - Nice to have but not critical

### Learning Documents Priority Order:
1. **Clarity** - Must be understandable
2. **Progression** - Concepts build properly
3. **Engagement** - Keeps reader motivated
4. **Examples** - Critical for understanding
5. **Accuracy** - Important but perfection not required in v1

---

## 🔄 Mixed Document Handling

### Some Documents Are Both:
**Example**: Smart Pins Complete Reference with Tutorial

**Solution**: Two-Phase Review
```
Phase 1: Tutorial sections reviewed by learners
Phase 2: Reference sections reviewed by experts
```

**Forum Approach**:
```
📖 + ⚙️ DUAL REVIEW: Smart Pins Documentation

This document has both tutorial and reference sections.

**Beginners**: Please review Chapters 1-3 (introduction)
- Focus on: Can you understand Smart Pins basics?

**Experts**: Please review Chapters 4-8 (reference)
- Focus on: Are all modes accurately documented?

Everyone: Feel free to review all, but focus on your strength!
```

---

## 📊 Review Weighting

### For Technical Documents:
| Reviewer Type | Weight | Why |
|--------------|---------|-----|
| Domain Expert | 100% | They know the truth |
| Production User | 90% | They use it daily |
| Tool Developer | 85% | They implement it |
| Advanced User | 60% | They understand most |
| Beginner | 20% | Can flag confusion |

### For Learning Documents:
| Reviewer Type | Weight | Why |
|--------------|---------|-----|
| Target Learner | 100% | They're who it's for |
| Recent Learner | 90% | Fresh perspective |
| Teacher | 85% | Pedagogical insight |
| Expert | 40% | May not remember learning |
| Non-target | 20% | General feedback |

---

## 🏆 Recognition Differences

### Technical Review Recognition:
- "Technical Validator" acknowledgment
- Listed as "Technical Reviewers"
- Noted for specific expertise area
- "Verified by: [expert names]"

### Learning Review Recognition:
- "Community Teacher" acknowledgment
- Listed as "Educational Reviewers"
- Noted for improving clarity
- "Made clearer thanks to: [names]"

---

## 📋 Implementation in Forums

### Create Two Review Styles:
```
P2 Documentation Review/
├── 📖 Learning Materials Review/
│   ├── PINNED: How to Review Learning Docs
│   ├── DeSilva Guide Review
│   └── Getting Started Review
└── ⚙️ Technical Reference Review/
    ├── PINNED: How to Review Technical Docs
    ├── PASM2 Manual Review
    └── Silicon Docs Review
```

---

## ✅ Success Metrics by Type

### Technical Documents:
- Zero technical errors in v1.0
- All edge cases documented
- Expert consensus achieved
- Production users validate

### Learning Documents:
- Beginners successfully learn
- Completion rate high
- Confusion points eliminated
- Teachers adopt it

---

*Different documents serve different purposes - review them differently!*