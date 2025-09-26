# Auxiliary Guides for AI-Assisted P2 Development

## Overview
This directory contains specialized guides that teach AI systems HOW to work with P2 resources effectively. These are meta-guides about process and technique, not P2 technical facts.

## Directory Structure

```
auxiliary-guides/
├── interaction/              # How to interact with AI
│   └── using-with-ai.md    # Complete guide for AI usage
│
├── search-strategies/        # Search optimization  
│   ├── obex-search-optimization.md     # OBEX search techniques
│   └── obex-integration-instructions.md # Implementation notes
│
├── special-techniques/       # P2-specific techniques
│   ├── bmp-generation-guide.md         # Debug visualization
│   └── hardware-testing-guide.md       # Hardware test workflow
│
└── development-workflows/    # Development patterns
    └── (planned content)
```

## Guide Categories

### 1. Interaction Patterns
**Purpose**: How to effectively use AI for P2 development
- Setting up conversations
- Navigating the knowledge base
- Understanding P2 vs OBEX boundaries
- Best practices for prompts

### 2. Search Strategies  
**Purpose**: Optimized discovery techniques
- **Key Insight**: Never filter by category first
- Keyword expansion (I2C → IIC, TWI, two-wire)
- Broad search then filter approach
- Understanding OBEX categorization quirks

### 3. Special Techniques
**Purpose**: P2-specific development methods
- **BMP Generation**: Create debug visualizations for Plot window
- **Hardware Testing**: Compile, download, test on real P2
- Signal-based control (coming soon)
- Log monitoring patterns

### 4. Development Workflows
**Purpose**: Complete development patterns
- Rapid compile-test cycles
- Multi-COG coordination
- Performance optimization

## For Remote Claude

### Discovery Pattern
1. User mentions keywords → Check auxiliary-guides-manifest.yaml
2. Download relevant guide based on keyword triggers
3. Study the `recommended_approach` section
4. Apply techniques to user's request

### Keyword Triggers

**OBEX Search**: "find driver", "sensor", "I2C driver", "community code"
→ Use `search-strategies/obex-search-optimization.md`

**Debug Visualization**: "Plot window", "BMP", "debug display"  
→ Use `special-techniques/bmp-generation-guide.md`

**Hardware Testing**: "test on P2", "download", "PropPlug", "pnut-term"
→ Use `special-techniques/hardware-testing-guide.md`

**AI Interaction**: "how to use AI", "Claude help", "prompt patterns"
→ Use `interaction/using-with-ai.md`

## Critical Understanding

These guides are **META-DOCUMENTATION**:
- They teach HOW to use P2 resources
- They provide methodologies and techniques
- They are NOT P2 technical specifications
- They complement the main knowledge base

## Maintenance Notes

- Guides should be concise and actionable
- Include `recommended_approach` sections
- Provide clear keyword triggers
- Focus on remote AI usability
- Keep examples practical and tested