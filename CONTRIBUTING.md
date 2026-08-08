# Contributing to P2-Knowledge-Base

Thank you for your interest in improving P2 documentation! This guide will help you contribute effectively.

## 🎯 Contribution Goals

We welcome contributions that:
- Improve technical accuracy
- Add missing documentation
- Enhance clarity and readability
- Provide working code examples
- Fix errors or inconsistencies
- Add learning resources

## 🚀 Quick Start

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feat/your-feature-name`
3. **Make** your changes following our standards
4. **Test** any code examples on real P2 hardware
5. **Commit** with clear messages
6. **Push** to your fork
7. **Submit** a Pull Request

## 📝 Documentation Standards

### Writing Style

- **Be Clear**: Use simple, direct language
- **Be Complete**: Include all necessary information
- **Be Correct**: Verify technical accuracy
- **Be Consistent**: Follow existing terminology
- **Be Concise**: Avoid unnecessary verbosity

### Technical Accuracy

All technical documentation MUST be:
- ✅ Verified against official P2 documentation
- ✅ Tested on actual P2 hardware (for code examples)
- ✅ Reviewed by someone familiar with the topic
- ✅ Include version information where relevant

### Formatting Guidelines

#### Markdown Files

```markdown
# Title (One H1 per document)

## Section (H2 for main sections)

### Subsection (H3 for subsections)

**Bold** for emphasis
*Italic* for first use of technical terms
`code` for inline code
```

#### Code Blocks

Always specify the language:

````markdown
```spin2
PUB main() | i
  repeat i from 0 to 9
    debug(udec(i))
```

```pasm2
        org     0
        mov     x, #5
        add     x, #3
```
````

#### Tables

Use tables for structured information:

```markdown
| Instruction | Cycles | Description |
|------------|--------|-------------|
| NOP        | 2      | No operation |
| MOV        | 2      | Move data |
```

### JSON Schema

For JSON files in `/ai-reference/`:

```json
{
  "$schema": "version-url",
  "metadata": {
    "version": "1.0.0",
    "lastUpdated": "2024-01-15",
    "contributors": ["name"]
  },
  "content": {
    // Actual data here
  }
}
```

## 🏗️ Types of Contributions

### 1. New Documentation

When adding new documentation:
- Check it doesn't already exist
- Place it in the correct section
- Follow the document template
- Update the INDEX.md file
- Add cross-references where appropriate

### 2. Corrections

For fixing errors:
- Clearly describe what was wrong
- Provide source for correct information
- Update all affected documents
- Test any corrected code

### 3. Code Examples

When contributing code:
- Test on real P2 hardware
- Include clear comments
- Follow P2 coding conventions
- Provide expected output
- Explain the concept being demonstrated

### 4. Learning Materials

For educational content:
- Identify the target audience
- Start with prerequisites
- Build concepts progressively
- Include exercises with solutions
- Provide common mistake warnings

## 🔄 Pull Request Process

### Before Submitting

- [ ] Read existing documentation in the area
- [ ] Follow the style guide
- [ ] Test all code examples
- [ ] Run link checker (if modifying links)
- [ ] Update INDEX.md if adding new files
- [ ] Write clear commit messages

### PR Template

```markdown
## Description
[What does this PR do?]

## Type of Change
- [ ] Bug fix (correction to existing documentation)
- [ ] New feature (new documentation)
- [ ] Enhancement (improvement to existing docs)

## Testing
- [ ] Code examples tested on P2 hardware
- [ ] Links verified
- [ ] JSON validates against schema

## Checklist
- [ ] Follows style guidelines
- [ ] Includes necessary cross-references
- [ ] Updates INDEX.md if needed
- [ ] Commits are logical and well-described
```

### Review Process

1. **Automated Checks**: JSON validation, link checking
2. **Technical Review**: Accuracy verification
3. **Editorial Review**: Style and clarity
4. **Merge**: After approval from maintainer

## 🛠️ Development Setup

### Required Tools

- Text editor with Markdown support
- Git for version control
- Python 3.x for running tools
- (Optional) Propeller Tool for testing code

### Validation Scripts

Run these before submitting:

```bash
# Check JSON validity
python tools/validate-json.py

# Verify internal links
python tools/check-links.py

# Generate updated index
python tools/generate-index.py
```

## 📋 Commit Message Convention

Use conventional commits:

- `docs: Add [topic] documentation`
- `fix: Correct [specific error]`
- `feat: Add [new feature/section]`
- `refactor: Reorganize [section]`
- `chore: Update [maintenance task]`

Examples:
```
docs: Add smart pin UART configuration guide
fix: Correct WAITX instruction cycle count
feat: Add comprehensive CORDIC examples
refactor: Reorganize memory model section for clarity
```

## 🎨 Document Templates

### New Topic Template

```markdown
# [Topic Name]

## Overview
[One paragraph description]

## Prerequisites
- [Required knowledge]
- [Required reading]

## Concept
[Main explanation]

## Implementation
[How to use/implement]

## Examples
[Working code examples]

## Common Pitfalls
[What to avoid]

## Best Practices
[Recommended approaches]

## Related Topics
- [Link to related doc]

## References
- [External sources]

## Metadata
- Version: 1.0.0
- Last Updated: YYYY-MM-DD
- Contributors: [Your Name]
```

## ❓ Questions?

- **Technical Questions**: Open an issue with the "question" label
- **Process Questions**: See existing discussions
- **General P2 Questions**: Visit [Parallax Forums](https://forums.parallax.com/)

## 🏆 Recognition

Contributors will be:
- Listed in the document metadata
- Mentioned in release notes
- Added to CONTRIBUTORS.md file

## 📜 Code of Conduct

- Be respectful and inclusive
- Focus on technical merit
- Accept constructive feedback
- Help others learn

## 📄 License

By contributing, you agree that your contributions are licensed under the terms
this project publishes under: **MIT** for code and data, and **CC BY-SA 4.0**
for documentation. These are the same terms your contribution ships under — we
do not ask contributors for broader rights than we grant readers.

See [engineering/standards/LICENSING-DECISION.md](engineering/standards/LICENSING-DECISION.md).

---

*Thank you for helping improve P2 documentation!*