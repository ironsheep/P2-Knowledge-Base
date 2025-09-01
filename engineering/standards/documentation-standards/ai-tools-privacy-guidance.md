# AI Tools Privacy Guidance for P2 Community

## Executive Summary
When using AI tools like Claude Code for P2 development, understand that **everything you share goes through the AI provider's servers**. Plan accordingly.

## Key Principles

### 1. Default Assumption: Not Private
- **Everything you share with AI is processed on external servers**
- File contents, code snippets, questions - all flow through the provider
- MCP tools (filesystem, etc.) are LOCAL bridges but data still goes through AI

### 2. What IS Protected
- **Local files** - Only shared if you explicitly give access
- **Git-ignored files** - Won't accidentally get committed
- **Other projects** - AI only sees what you specifically share

### 3. What is NOT Protected
- **Any file you ask AI to read** - Full content goes to AI servers
- **Any code you ask AI to write** - Generated through AI servers
- **Conversation history** - Everything discussed in the session

## Best Practices for P2 Developers

### For NON-Sensitive Projects (Most Cases)
✅ **Safe to use AI freely:**
- Open source projects
- Learning exercises
- Community contributions
- Published documentation
- Example code

### For SENSITIVE Projects
⚠️ **Use these strategies:**

1. **Compartmentalize**
   - Keep sensitive algorithms in separate files
   - Only share non-sensitive portions with AI
   - Use placeholder names for proprietary components

2. **Sanitize Before Sharing**
   - Replace company names with "CLIENT"
   - Change proprietary values to examples
   - Remove API keys/credentials (ALWAYS!)

3. **Local Development Pattern**
   ```
   /project
   ├── /public-code     (OK to share with AI)
   ├── /sensitive       (NEVER share)
   └── /ai-workspace    (Sanitized versions for AI help)
   ```

## Specific Scenarios

### ✅ SAFE: "Help me debug this PASM2 routine"
- General P2 programming questions are fine
- Share code snippets freely

### ⚠️ CAUTION: "Here's my client's motor control algorithm"
- Sanitize first: remove client name, specific parameters
- Or describe the problem without the actual code

### 🚫 NEVER: Credentials or Keys
- API keys, passwords, tokens - NEVER share
- Even in config files - remove first

## Tools & Features Understanding

### Claude Code with MCP
- **Filesystem MCP**: Runs locally, but content still goes to Claude
- **Git MCP**: Same - local tool, data through Claude
- **Not a privacy tool**: It's for convenience, not security

### GitHub Copilot / Other AI
- Similar principles apply
- Each has their own data policies
- Research before using with sensitive code

## Official Recommendations

### For Parallax Community Members

1. **Educational/Hobby Projects**: Use AI freely - accelerate learning!

2. **Commercial Projects**: 
   - Separate proprietary from generic code
   - Get client permission if unclear
   - When in doubt, sanitize

3. **Company Projects**:
   - Check company AI usage policy
   - Many companies have specific guidelines
   - Some prohibit AI tools entirely for IP protection

## The Bottom Line

**AI tools are powerful accelerators for P2 development, but they're not private boxes.**

Think of AI like a very smart colleague in another company:
- You'd share general programming questions
- You'd discuss public techniques
- You wouldn't hand over your secret sauce

## For Training Sessions

### Key Messages:
1. "AI accelerates P2 development, but be smart about what you share"
2. "Perfect for learning and open source, careful with proprietary"
3. "When in doubt, sanitize or segment"

### Demonstration Ideas:
- Show sanitization techniques
- Demo the local/AI boundary
- Practice identifying sensitive vs. safe code

## Community Resources
- Parallax Forum AI Guidelines (to be created)
- Example sanitization templates
- Approved AI tools list

---

*This document represents current best practices as of 2025. As AI tools evolve, so should our practices.*