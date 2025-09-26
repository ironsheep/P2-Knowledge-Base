# AI Integration Guide for P2 Knowledge Base
*Master guide for using this knowledge base with Claude Code and other AI assistants*

**Repository**: https://github.com/ironsheep/P2-Knowledge-Base

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

### The Perfect Session Starter

```markdown
I need help with P2 (Propeller 2) development.

Please access the P2 Knowledge Base from GitHub:
https://github.com/ironsheep/P2-Knowledge-Base

CRITICAL: Start with these manifests:
1. manifests/p2-knowledge-root.yaml - Main navigation
2. manifests/auxiliary-guides-manifest.yaml - HOW to use resources

Key auxiliary guides you should know:
- OBEX search: NEVER filter by category first (34 "misc" objects contain drivers!)
- Hardware testing: Use pnut_ts -d, monitor logs/*.log
- BMP generation: For Plot window debug visualization

The P2 provides building blocks (Smart Pins, COGs), not complete peripherals.
Need UART/SPI/I2C? Use OBEX objects.

My task: [YOUR SPECIFIC TASK]
```

### Why This Works

1. **Immediate auxiliary guide awareness** - AI learns HOW to use resources
2. **OBEX search optimization** - Avoids missing 60+ objects in wrong categories
3. **P2 philosophy understanding** - Building blocks, not peripherals
4. **Clear navigation path** - Manifests first, always

---

## 2. Understanding the Knowledge Base Structure

### Hierarchical Organization

```
P2-Knowledge-Base/
├── manifests/                          # START HERE - Navigation
│   ├── p2-knowledge-root.yaml         # Main index
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

1. **Start**: `manifests/p2-knowledge-root.yaml`
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

### Pattern: Serial Communication

```markdown
User: "How do I do serial communication on P2?"

CORRECT RESPONSE:
1. Recognize serial is NOT built-in
2. Check manifests/obex/categories/*.yaml
3. Find jm_fullduplexserial (Object 2842)
4. Show implementation:
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