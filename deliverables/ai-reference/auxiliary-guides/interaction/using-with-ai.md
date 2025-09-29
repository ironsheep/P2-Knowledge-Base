# AI Integration Guide for P2 Knowledge Base
*Master guide for using this knowledge base with Claude Code and other AI assistants*

**Repository**: https://github.com/ironsheep/P2-Knowledge-Base

> 🎆 **NEW in Version 2.0**: Self-bootstrapping system! The knowledge base now teaches AI assistants how to use it automatically. Just provide the minimal bootstrap command and everything configures itself. See Section 1 below.

## 🚀 Quick Navigation

| Resource | Purpose |
|----------|---------|
| **[Claude QuickStart](../../../../CLAUDE-QUICKSTART.md)** | Essential copy-paste templates |
| **[Prompt Patterns](../../../../AI-PROMPT-PATTERNS.md)** | Comprehensive interaction patterns |
| **[Privacy Guide](../../developer-docs/ai-development/Claude-Code-Privacy-Guide-for-P2-Developers.pdf)** | **Must read!** Protect your IP |
| **[Auxiliary Guides](../README.md)** | Specialized techniques and workflows |

---

## 📋 Table of Contents

1. [Essential Starting Instructions](#1-essential-starting-instructions)
2. [Understanding the Knowledge Base Structure](#2-understanding-the-knowledge-base-structure)
3. [Critical Concepts for Success](#3-critical-concepts-for-success)
4. [Navigation Best Practices](#4-navigation-best-practices)
5. [Common Pitfalls and Solutions](#5-common-pitfalls-and-solutions)
6. [Usage Patterns and Examples](#6-usage-patterns-and-examples)
7. [Advanced Features](#7-advanced-features)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. Essential Starting Instructions

### 🎯 NEW: Self-Bootstrapping System (Version 2.0)

**The knowledge base now teaches itself!** Just give your AI this minimal bootstrap:

```markdown
Access the P2 Knowledge Base:
https://github.com/ironsheep/P2-Knowledge-Base

Start with: manifests/propeller-knowledge-root.yaml
Follow the AI instructions it provides for automatic setup.
```

**That's it!** The system will:
1. Load comprehensive navigation rules automatically
2. Configure category shortcuts for fast access
3. Check for updates each session
4. Teach the AI everything about P2 development

### Legacy Manual Instructions (Pre-v2.0)

<details>
<summary>Click for old manual setup (if auto-bootstrap fails)</summary>

```markdown
FIRST ACTION: Save these instructions to your CLAUDE.md, replacing any P2 Knowledge Base content you may already have.

You are helping with Propeller 2 (P2) microcontroller development using the P2 Knowledge Base.
GitHub: https://github.com/ironsheep/P2-Knowledge-Base
Raw access: https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/

### CRITICAL RULES - NO EXCEPTIONS

#### BEFORE EVERY P2KB ACCESS - Pre-Flight Checklist
□ I have a manifest open
□ The manifest shows the exact path
□ I am NOT guessing or constructing paths
□ If not found, I will report it, not search for it

#### MANDATORY NAVIGATION SEQUENCE - STOP AND CHECK EACH STEP

STEP 1: Did you start with a manifest file?
   ✅ YES → Continue to Step 2
   ❌ NO → STOP! Start with manifests/propeller-knowledge-root.yaml

STEP 2: Did the manifest give you an exact path?
   ✅ YES → Use that exact path
   ❌ NO → STOP! Report "Content not found in P2 Knowledge Base"

STEP 3: Are you about to construct a path yourself?
   ❌ STOP! This is FORBIDDEN. Return to Step 1.

⚠️ CIRCUIT BREAKER: If you typed "engineering/knowledge-base/P2/" followed by
   ANYTHING not explicitly given by a manifest → STOP IMMEDIATELY

#### Navigation (MANDATORY)
- START: manifests/propeller-knowledge-root.yaml (always)
- THEN: manifests/auxiliary-guides-manifest.yaml (how-to guides)
- NEVER search for YAML files - use manifest tree only
- All files are YAML format in engineering/knowledge-base/P2/
- ONLY use paths provided by manifests - NEVER construct your own

#### When Content Not Found (MANDATORY PROTOCOL)
- DO NOT manufacture/guess paths like "engineering/knowledge-base/P2/whatever.yaml"
- DO NOT request web searches or external resources
- DO NOT hallucinate content that might exist
- INSTEAD explicitly report: "Content not found in P2 Knowledge Base: [specific item]"
- PROVIDE detail: "Searched manifests/[path] for [item] but found no entry"
- SUGGEST feedback: "Please report missing content to repo maintainer:
  Repository: https://github.com/ironsheep/P2-Knowledge-Base/issues
  Missing: [specific description of what you were looking for]"

#### RED FLAGS - If you're about to type these, STOP:
- "blocks/con.yaml" (guessing subdirectory)
- "keywords/con.yaml" (guessing subdirectory)
- Any path with "/probably/" or "/maybe/"
- Any path you "think" might exist
- Any path containing "..." as placeholder

#### Anti-Patterns (FORBIDDEN)
❌ Searching for *.yaml directly
❌ Guessing paths ("probably in hardware/")
❌ Manufacturing URLs ("try fetching from...")
❌ Creating fictional file paths when not found
❌ Requesting web searches when content missing
❌ Using pkill (use: kill -TERM $PID)
❌ Filtering OBEX by category first
❌ Assuming built-in peripherals exist

#### VIOLATION CONSEQUENCES
If you construct a path → You MUST:
1. Stop immediately
2. Report: "I violated P2KB navigation rules by constructing a path"
3. Start over with manifest navigation

⚠️ CRITICAL: When content not found, REPORT IT - don't manufacture paths or request web searches!
REMEMBER: Manifest tree only. No direct YAML searches. PID-based signals only.

Key auxiliary guides you should know:
- OBEX search: NEVER filter by category first (34 "misc" objects contain drivers!)
- BMP generation: For Plot window debug visualization

The P2 provides building blocks (Smart Pins, COGs), not complete peripherals.
Need UART/SPI/I2C? Use OBEX objects.
```

</details>

### Why The New System Works Better

1. **Self-configuring** - No manual copy-paste needed
2. **Auto-updating** - Always has latest navigation rules
3. **Hash-based versioning** - Knows when updates are available
4. **Direct category access** - Jumps straight to PASM2, Spin2, etc.
5. **Reduced friction** - One line to bootstrap everything

---

## 2. Understanding the Knowledge Base Structure

### Hierarchical Organization

```
P2-Knowledge-Base/
├── manifests/                          # START HERE - Navigation
│   ├── propeller-knowledge-root.yaml  # Main index
│   ├── auxiliary-guides-manifest.yaml # HOW to use resources ← NEW!
│   ├── pasm2-manifest.yaml            # 357 instructions
│   ├── smart-pins-manifest.yaml       # 32 pin modes
│   ├── spin2-manifest.yaml            # Language constructs
│   └── obex/                          # Community code
│       ├── obex-root.yaml             # 113 objects index
│       ├── categories/*.yaml          # By function
│       └── authors/*.yaml             # By contributor
│
├── engineering/knowledge-base/P2/      # Detailed specs
│   ├── language/
│   │   ├── pasm2/                     # Instruction YAMLs
│   │   └── spin2/                     # Method YAMLs
│   ├── hardware/
│   │   └── smart-pins/                # Pin mode YAMLs
│   └── community/obex/objects/        # Object YAMLs
│
└── deliverables/ai-reference/
    └── auxiliary-guides/               # Meta-guides ← NEW!
        ├── search-strategies/          # OBEX optimization
        ├── special-techniques/         # BMP, testing
        └── interaction/                # This guide
```

### Key Insight: Two Types of Documentation

1. **P2 Knowledge** - WHAT the P2 can do (instructions, pins, methods)
2. **Auxiliary Guides** - HOW to use the knowledge effectively

---

## 3. Critical Concepts for Success

### 🔴 Concept 1: OBEX Search Strategy

**NEVER filter by category first!**

```yaml
# BAD: "Find I2C drivers in drivers category"
Result: Miss 60+ relevant objects in other categories

# GOOD: "Find ALL OBEX objects related to I2C, IIC, TWI, two-wire"
Result: Find all relevant objects regardless of category
```

**Why**: 34 objects in "misc" are actually drivers!

### 🔴 Concept 2: P2 Philosophy

**P2 provides building blocks, NOT complete peripherals**

| Traditional MCU | P2 Approach |
|----------------|-------------|
| Built-in UART peripheral | Smart Pins + OBEX serial object |
| Hardware SPI controller | COGs + OBEX SPI object |
| I2C hardware | Smart Pins + OBEX I2C object |

**Always check OBEX** when user asks for any communication protocol or peripheral.

### 🔴 Concept 3: Manifest-Only Navigation

**NEVER guess paths - ALWAYS follow manifests**

```yaml
# Path Construction:
raw_base_url + base_path + file = complete_url

# Example:
https://raw.githubusercontent.com/.../main/ + 
engineering/knowledge-base/P2/language/spin2/ + 
methods/locknew.yaml
```

---

## 4. Navigation Best Practices

### Step-by-Step Navigation

1. **Start**: `manifests/propeller-knowledge-root.yaml`
2. **Check auxiliary guides**: `manifests/auxiliary-guides-manifest.yaml`
3. **Navigate to category**: e.g., `manifests/spin2-manifest.yaml`
4. **Find specific file**: Use exact path from manifest
5. **Download YAML only**: Never .md files in knowledge base

### Finding OBEX Objects Effectively

```yaml
# 1. Start with OBEX root
manifests/obex/obex-root.yaml

# 2. Search ALL categories, not specific ones
manifests/obex/categories/*.yaml  # Check ALL

# 3. Expand keywords
"I2C" → also search "IIC", "TWI", "two-wire", "2-wire"

# 4. Check top authors
Jon McPhalen (jonnymac): 44 high-quality objects
```

### Smart Pin Configuration

```yaml
# 1. Check manifest
manifests/smart-pins-manifest.yaml

# 2. Find mode by function
Need pulse measurement? → Mode %10000 (time A input)
Need UART TX? → Mode %11110 (async serial transmit)

# 3. Get detailed spec
engineering/knowledge-base/P2/hardware/smart-pins/modes/[mode].yaml
```

---

## 5. Common Pitfalls and Solutions

### Pitfall 1: Assuming P2 has Built-in Peripherals

❌ **Wrong**: "The P2's UART peripheral..."  
✅ **Right**: "The P2 implements UART using Smart Pins and OBEX objects"

### Pitfall 2: Searching Only Expected Categories

❌ **Wrong**: Looking for drivers only in "drivers" category  
✅ **Right**: Search all 113 objects across all categories

### Pitfall 3: Guessing File Paths

❌ **Wrong**: `/language/spin2/methods/debug.md`  
✅ **Right**: Check manifest for actual path: `debug-commands/debug.yaml`

### Pitfall 4: Using Console Output for Testing

❌ **Wrong**: Reading cluttered console output  
✅ **Right**: Monitor `logs/*.log` files for clean debug output

---

## 6. Usage Patterns and Examples

### Pattern: Serial Communication with Repository Awareness ✨

```markdown
User: "How do I do serial communication on P2?"

CORRECT RESPONSE:
1. Recognize serial is NOT built-in
2. Check manifests/obex/categories/*.yaml
3. Find jm_fullduplexserial (Object 2842)
4. Check if github_repo exists in YAML
5. Show implementation with repo awareness:
```

```spin2
OBJ
  serial : "jm_fullduplexserial"

PUB main()
  serial.start(RX_PIN, TX_PIN, %0000, 115_200)
  serial.str(@"Hello World")
```

### Pattern: Finding Instructions

```markdown
User: "What CORDIC instructions are available?"

PROCESS:
1. Open manifests/pasm2-manifest.yaml
2. Find CORDIC category
3. List instructions:
   - QROTATE
   - QVECTOR
   - QDIV
   - QFRAC
   - QMUL
   ...
```

### Pattern: Hardware Testing

```markdown
User: "How do I test my code on real P2?"

PROCESS:
1. Check auxiliary-guides/special-techniques/hardware-testing-guide.md
2. Key steps:
   - Compile: pnut_ts -d program.spin2
   - Download: pnut-term-ts -r program.bin -p [device] &
   - Monitor: tail -f logs/debug_*.log
   - Clean shutdown: kill -TERM $PID
```

---

## 7. Advanced Features

### OBEX Repository Awareness ✨ NEW!

**21 of 113 OBEX objects now have GitHub repository links!**

When finding OBEX objects with repos:
1. **Mention** the repo exists (don't auto-fetch)
2. **Offer** to check for newer versions
3. **Provide** direct links for user to explore

```yaml
# In OBEX YAML files:
version_tracking:
  obex_version: "3.0.2"
  has_github_repo: true
urls:
  github_repo: "https://github.com/ironsheep/P2-HUB75-LED-Matrix-Driver"
```

**Best Practice**: "This object has a GitHub repository. I can check for newer releases if needed."

### Auxiliary Guides System

The knowledge base now includes specialized guides for techniques:

| Guide | Location | Use When |
|-------|----------|----------|
| OBEX Search Optimization | `search-strategies/` | Finding community code |
| BMP Generation | `special-techniques/` | Debug visualization |
| Hardware Testing | `special-techniques/` | Real device testing |
| Using with AI | `interaction/` | AI integration help |

Access via: `manifests/auxiliary-guides-manifest.yaml`

### Enrichment Status Tracking

Check `.ai-manifest.json` for coverage:
- PASM2: 166 enriched, 188 minimal
- Smart Pins: All 32 modes complete
- Spin2: 71 methods enriched

### Multi-COG Patterns

Find proven patterns in:
- `external-projects/flash-fs-code/` - COG coordination
- `external-projects/p2-HUB75-LED-Matrix-Driver/` - Parallel processing

---

## 8. Troubleshooting

### Issue: Can't Find Information

**Solution Checklist:**
1. Started with root manifest? ✓
2. Checked auxiliary guides? ✓
3. Searched ALL OBEX categories? ✓
4. Expanded search keywords? ✓

### Issue: Wrong File Paths

**Common Corrections:**
- Lock methods: `methods/locknew.yaml` not `constructs/methods/`
- DEBUG: `debug-commands/debug.yaml` not `methods/debug.yaml`
- All files are `.yaml` not `.md`

### Issue: Code Won't Compile

**Debug Process:**
1. Check against instruction YAML specs
2. Verify OBEX object is included
3. Confirm pin assignments
4. Add debug statements with `-d` flag

---

## 🎯 Golden Rules Summary

1. **Start with manifests** - Always, no exceptions
2. **Check auxiliary guides** - Learn HOW before WHAT
3. **OBEX search broadly** - Never filter by category first
4. **P2 = building blocks** - Not complete peripherals
5. **Follow exact paths** - Never guess or construct
6. **Monitor logs, not console** - For clean testing output
7. **Capture PID for control** - Clean shutdown with signals
8. **Expand keywords** - I2C → IIC, TWI, two-wire
9. **Check top authors** - jonnymac = quality
10. **YAML only** - No .md files in knowledge base

---

## 📚 Additional Resources

### Example Conversation Starters

**For Beginners:**
```
"I'm new to P2. Using the P2 Knowledge Base and auxiliary guides,
explain the architecture and show a LED blink example."
```

**For OBEX Discovery:**
```
"Find ALL P2 OBEX objects related to display control.
Remember to search all categories, not just 'display'."
```

**For Hardware Testing:**
```
"Show me the complete workflow for testing P2 code on hardware,
including signal-based control and log monitoring."
```

### Contributing Back

Found improvements? Follow these guidelines:
1. Enriched YAMLs → `engineering/knowledge-base/P2/`
2. Auxiliary guides → `deliverables/ai-reference/auxiliary-guides/`
3. Update relevant manifests
4. Follow CONTRIBUTING.md

---

## 🔒 Privacy and Security

**Essential Reading**: [Privacy Guide for P2 Developers](../../developer-docs/ai-development/Claude-Code-Privacy-Guide-for-P2-Developers.pdf)

Key points:
- Protect your IP when using AI tools
- Understand data retention policies
- Use proper .gitignore patterns
- Consider local-first development

---

*Remember: This knowledge base is AI-optimized. Always mention "P2 Knowledge Base" and check auxiliary guides for best results.*
