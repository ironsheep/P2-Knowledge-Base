# Claude Code Quick Start Card
*Copy and paste these prompts to get started with the P2 Knowledge Base*

## ⚠️ CRITICAL: Session Management for Performance

**🔥 Clear conversation every 2-3 hours or 15-20 file reads!**

Each file adds 200-500 lines to context. Performance degrades quickly.

```
# Before clearing:
"Summarize findings about [topic] before we clear for performance"
[Copy summary]
[Clear conversation]

# After clearing:
"Continue from: [paste summary]. Now working on [next task]"
```

## 🚀 Session Starter (Copy This First!)

### For Fresh Instance (No Local Files):
```
First, create a CLAUDE.md file to remember the P2 Knowledge Base location:

Create file CLAUDE.md with:
---
# CLAUDE.md
Repository: https://github.com/ironsheep/P2-Knowledge-Base
Raw files: https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/
---

Now use the P2 Knowledge Base directly from GitHub without cloning:
https://github.com/ironsheep/P2-Knowledge-Base

IMPORTANT: Use the raw.githubusercontent.com URLs to read files:
- Base URL: https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/
- Example: https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/README.md

Read these files directly from GitHub:
1. First read AI-INTEGRATION.md for usage instructions
2. Use manifests/ directory for navigation  
3. Access detailed specs in engineering/knowledge-base/P2/

DO NOT clone the repository. Just read files directly from GitHub using raw URLs.

I need help with [YOUR TASK HERE].
```

### For Local Repository:
```
I have the P2 Knowledge Base repository in the current directory.
Please read the AI-INTEGRATION.md file first.

Key resources:
- Manifests are in manifests/ for navigation
- Detailed specs in engineering/knowledge-base/P2/

I need help with [YOUR TASK HERE].
```

## 📚 Common Task Templates

### PASM2 Assembly Programming
```
Using the P2 knowledge base PASM2 instructions in 
engineering/knowledge-base/P2/language/pasm2/, 
help me write assembly code to [DESCRIBE TASK].

Check manifests/pasm2-manifest.yaml for instruction categories.
```

### Smart Pin Configuration
```
I need to configure a P2 Smart Pin for [PURPOSE].
Check engineering/knowledge-base/P2/hardware/smart-pins/modes/
and help me select and configure the right mode.

The mode naming is [5-bit-binary]_[description].yaml
```

### Spin2 High-Level Programming
```
Using the Spin2 method documentation in 
engineering/knowledge-base/P2/language/spin2/methods/,
show me how to [DESCRIBE TASK] in Spin2.

Reference manifests/spin2-manifest.yaml for available methods.
```

### Multi-COG Design
```
I need to design a multi-COG P2 application for [PURPOSE].
Reference the patterns in:
- external-projects/P2-FLASH-FS/ (multi-COG safe patterns)
- external-projects/p2-HUB75-LED-Matrix-Driver/ (COG communication)

Show me the architecture and communication strategy.
```

### Hardware Interfacing
```
I need to interface the P2 with [DEVICE/PROTOCOL].
Check the hardware specs in engineering/knowledge-base/P2/hardware/
and any relevant patterns in external-projects/.

Generate the initialization and communication code.
```

## 🎯 Specific Component Queries

### Instruction Lookup
```
What P2 instructions are available for [OPERATION TYPE]?
Check the [CATEGORY] section in manifests/pasm2-manifest.yaml
and detailed YAMLs in engineering/knowledge-base/P2/language/pasm2/[category]/
```

### Pin Mode Selection
```
Which Smart Pin mode should I use for [SIGNAL TYPE]?
List relevant modes from engineering/knowledge-base/P2/hardware/smart-pins/modes/
with their binary codes and configuration requirements.
```

### Architecture Questions
```
Explain the P2's [ARCHITECTURAL FEATURE].
Reference engineering/knowledge-base/P2/architecture/
and manifests/architecture-manifest.yaml
```

## 💡 Power User Tips

### Get Enriched Documentation
```
Is the [INSTRUCTION/METHOD] documentation enriched?
Check if it has description, examples, and encoding details
in the YAML file.
```

### Find Code Patterns
```
Show me real-world patterns for [TECHNIQUE].
Search in external-projects/*/spin2-patterns-*.md
for proven implementations.
```

### Validate Generated Code
```
Please validate this code against the P2 specifications:
[PASTE CODE]

Check against the relevant YAML specifications for correctness.
```

## 🔍 Navigation Shortcuts

### By Manifest Type
- **Instructions**: `manifests/pasm2-manifest.yaml`
- **Smart Pins**: `manifests/smart-pins-manifest.yaml`
- **Spin2**: `manifests/spin2-manifest.yaml`
- **Architecture**: `manifests/architecture-manifest.yaml`
- **Hardware**: `manifests/hardware-manifest.yaml`

### By Knowledge Type
- **PASM2**: `engineering/knowledge-base/P2/language/pasm2/`
- **Spin2**: `engineering/knowledge-base/P2/language/spin2/`
- **Smart Pins**: `engineering/knowledge-base/P2/hardware/smart-pins/`
- **Architecture**: `engineering/knowledge-base/P2/architecture/`

### By Example Type
- **Flash FS**: `external-projects/P2-FLASH-FS/`
- **HUB75 LED**: `external-projects/p2-HUB75-LED-Matrix-Driver/`
- **Patterns**: `*/spin2-patterns-*.md`

## 🎨 Project Templates

### New Driver Development
```
I'm writing a P2 driver for [DEVICE].
Using the driver template patterns from:
- P2-FLASH-FS/spin2-driver-template.spin2
- p2-HUB75-LED-Matrix-Driver/spin2-patterns-hub75.md

Help me structure the driver with proper multi-COG safety.
```

### Real-Time Application
```
I need a real-time P2 application with:
- [LIST REQUIREMENTS]

Using the P2's deterministic timing and multi-COG architecture,
design the system referencing patterns from the knowledge base.
```

### Protocol Implementation
```
Implement [PROTOCOL] on P2.
Use Smart Pins where applicable (check modes/)
and PASM2 for timing-critical sections.
Reference any similar implementations in external-projects/.
```

## ⚡ Quick Lookups

### Get All Instructions in a Category
```
List all P2 [CATEGORY] instructions with brief descriptions.
Use manifests/pasm2-manifest.yaml and the category YAML.
```

### Compare Smart Pin Modes
```
Compare Smart Pin modes for [USE CASE].
Show pros/cons of each applicable mode from modes/*.yaml
```

### Find Spin2 Method
```
How do I [OPERATION] in Spin2?
Check engineering/knowledge-base/P2/language/spin2/methods/
for the appropriate method.
```

## 🆘 Troubleshooting

### Can't Find Information
```
I can't find information about [TOPIC].
Please check:
1. The manifests/ directory
2. Search in engineering/knowledge-base/P2/
3. Look for patterns in external-projects/
4. Check the .ai-manifest.json completeness section
```

### Code Not Working
```
This P2 code isn't working as expected:
[PASTE CODE]

Please check it against:
1. Instruction encodings in relevant YAMLs
2. Smart Pin configurations if applicable
3. Known patterns from external-projects/
```

## 📝 Remember

- Always mention "P2 Knowledge Base" in your prompts
- Start with manifests for navigation
- Use specific YAML paths when possible
- Check enrichment status in .ai-manifest.json
- Reference patterns from real projects

---

*Pro tip: Save this file locally and customize the templates for your specific P2 projects!*