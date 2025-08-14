# Repository Structure and Organization

## Overview

The P2-Knowledge-Base repository is organized into distinct sections, each optimized for specific audiences while maintaining cross-references for comprehensive understanding.

## Directory Structure

### 📁 `/ai-reference/` - AI-Optimized Documentation

**Purpose**: Machine-readable documentation optimized for AI consumption and training.

**Structure**:
```
/ai-reference/
├── README.md                       # Guide for AI systems using these docs
├── p2-architecture-complete.md    # Comprehensive architecture in one document
├── pasm2-instruction-set.json     # Complete instruction set as structured data
├── spin2-language-spec.json       # Language specification in JSON
├── peripheral-registers.json      # All registers with bit fields
├── timing-constraints.md          # Timing relationships and constraints
└── code-patterns/                 # Common patterns with full context
    ├── smart-pins.md              # Smart pin usage patterns
    ├── cog-communication.md       # Inter-cog communication methods
    ├── hub-memory-access.md       # Hub memory access patterns
    └── interrupt-handling.md      # Event and interrupt patterns
```

**Design Principles**:
- Self-contained documents (minimize need for cross-references)
- Structured data formats (JSON) where applicable
- Explicit relationship descriptions
- Complete context in each document
- Consistent terminology throughout

### 📁 `/learning-paths/` - Educational Content

**Purpose**: Progressive tutorials for new P2 developers.

**Structure**:
```
/learning-paths/
├── README.md                      # Learning roadmap and prerequisites
├── 01-p2-fundamentals/           # Core concepts
├── 02-spin2-basics/              # High-level programming
├── 03-pasm2-introduction/        # Assembly programming
└── 04-practical-projects/        # Hands-on projects
```

**Design Principles**:
- Progressive complexity (simple → advanced)
- Each lesson builds on previous knowledge
- Abundant examples with explanations
- Common mistakes and solutions
- Exercises with answers

### 📁 `/developer-reference/` - Technical Reference

**Purpose**: Detailed technical documentation for experienced developers.

**Structure**:
```
/developer-reference/
├── README.md
├── instruction-reference/         # Detailed instruction documentation
├── smart-pins/                   # Smart pin modes and configuration
├── memory-model/                 # Memory organization and access
├── timing-and-clocks/           # Clock systems and timing
└── debugging/                    # Debug features and techniques
```

**Design Principles**:
- Complete technical specifications
- Performance characteristics
- Optimization techniques
- Real-world use cases
- Quick-reference tables

### 📁 `/quick-reference/` - Quick Lookup

**Purpose**: Cheat sheets and quick reference materials.

**Contents**:
- PASM2 instruction cheat sheet
- Spin2 syntax quick reference
- Pin modes table
- Clock configuration table
- Memory map diagram
- Common constants and values

### 📁 `/code-examples/` - Working Examples

**Purpose**: Tested, working code examples demonstrating P2 features.

**Organization**:
```
/code-examples/
├── /basic/                       # Simple, single-concept examples
├── /intermediate/                # Multi-feature examples
├── /advanced/                    # Complex, real-world examples
└── /templates/                   # Boilerplate for common tasks
```

### 📁 `/migration-guides/` - P1 to P2 Migration

**Purpose**: Help developers transition from Propeller 1 to Propeller 2.

**Contents**:
- Architecture differences
- Instruction set changes
- Spin1 vs Spin2 comparison
- Porting strategies
- Common gotchas

### 📁 `/tools/` - Documentation Tools

**Purpose**: Scripts and utilities for maintaining documentation quality.

**Contents**:
- JSON validators
- Link checkers
- Index generators
- Format converters

## Document Standards

### File Naming Conventions

- Use lowercase with hyphens: `smart-pin-modes.md`
- Be descriptive but concise
- Group related files with common prefixes
- Use `.md` for narrative docs, `.json` for structured data

### Markdown Structure

Every markdown document should follow this template:

```markdown
# Document Title

## Overview
[Brief description of the topic]

## Table of Contents
[For documents over 500 lines]

## Prerequisites
[Required knowledge or reading]

## Main Content
[Organized with clear sections]

## Examples
[Practical demonstrations]

## Common Issues
[Troubleshooting information]

## Related Topics
[Links to related documents]

## References
[External sources]

## Metadata
- Version: X.Y.Z
- Last Updated: YYYY-MM-DD
- Contributors: [List]
```

### JSON Structure

JSON documents should follow this schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "version": "1.0.0",
  "lastUpdated": "2024-01-15",
  "data": {
    // Actual content here
  },
  "metadata": {
    "source": "Official P2 documentation",
    "contributors": ["..."]
  }
}
```

## Cross-References

### Linking Strategy

1. **Within Section**: Use relative links `[text](./file.md)`
2. **Cross Section**: Use full path from root `[text](/section/file.md)`
3. **External**: Always use full URLs with title attributes

### Reference Naming

- Use consistent names for concepts across all documents
- Maintain a glossary of terms in `/quick-reference/glossary.md`
- Use the official Parallax terminology where established

## Version Control

### Branch Strategy

- `main`: Stable, reviewed documentation
- `develop`: Work in progress
- `feature/*`: New documentation sections
- `fix/*`: Corrections and updates

### Commit Messages

Follow conventional commits:
- `docs: Add smart pin UART mode documentation`
- `fix: Correct PASM2 MUL instruction timing`
- `feat: Add Spin2 object examples`
- `refactor: Reorganize memory model section`

## Quality Standards

### Accuracy
- All technical information must be verified against official documentation
- Code examples must be tested on actual P2 hardware
- Timing information must be measured, not estimated

### Completeness
- Each document should be self-contained where possible
- Cross-references should enhance, not replace, content
- Include both "what" and "why" explanations

### Clarity
- Use clear, concise language
- Define technical terms on first use
- Provide visual aids (diagrams, tables) where helpful
- Include examples for abstract concepts

## Review Process

1. **Self-Review**: Check against these standards
2. **Technical Review**: Verify accuracy of technical content
3. **Editorial Review**: Check clarity and organization
4. **Community Review**: Gather feedback from P2 developers

## Maintenance

### Regular Updates
- Review and update quarterly
- Track P2 firmware/tool updates
- Incorporate community feedback
- Update examples for best practices

### Deprecation
- Mark outdated content clearly
- Provide migration paths
- Maintain version history
- Archive rather than delete

---

*This document defines the structure and standards for the P2-Knowledge-Base repository*