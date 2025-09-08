# Claude Code Quick Start Card
*Copy and paste these prompts to get started with the P2 Knowledge Base*

## ⚠️ CRITICAL: Session Management for Performance

**🔥 Clear conversation every 3-4 hours or 15-20 major file operations!**

Performance degrades as context accumulates. Watch for these warning signs:
- Responses getting slower
- Claude forgetting recent work
- Repetitive questions about already-discussed topics

### Session Management Best Practices

**Before Clearing (Save Your Work):**
```
Please summarize:
1. What we've accomplished so far
2. Key findings and decisions made
3. Next steps we were planning
4. Any important code or configurations

Format this as a brief summary I can paste after clearing.
```

**After Clearing (Resume Seamlessly):**
```
Continuing P2 development session. Previous summary:
[Paste the summary here]

The P2 Knowledge Base info should be in CLAUDE.md.
Please continue with: [specific next task]
```

### Session Health Indicators
- ✅ **Healthy (0-3 hours)**: Fast responses, perfect recall
- ⚠️ **Warning (3-4 hours)**: Slightly slower, may need reminders
- ❌ **Clear Now (4+ hours)**: Degraded performance, confusion

### File Operations Impact
- YAML manifests: ~100-200 lines each
- Instruction specs: ~50-100 lines each  
- Pattern files: ~200-500 lines each
- After 15-20 files: Consider clearing

## 🚀 Session Starter (Copy This First!)

### Step 1: Update CLAUDE.md
Tell Claude to add this to CLAUDE.md:

```
Please add the following to CLAUDE.md:

# P2 Knowledge Base Access
P2 Knowledge Base Repository: https://github.com/ironsheep/P2-Knowledge-Base
Raw files base: https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/
Root manifest: https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/manifests/p2-knowledge-root.yaml

When working with P2 (Propeller 2) tasks:
1. Start with p2-knowledge-root.yaml - it's the navigation index
2. Use manifest files to discover available documentation
3. Access files directly from GitHub using raw.githubusercontent.com URLs
4. Navigate: Root manifest → Category manifests → Individual YAML specs
5. DO NOT clone the repository - read files directly from GitHub
```

### Step 2: Start Your P2 Task
After CLAUDE.md is updated, use this prompt:

```
I need help with P2 (Propeller 2) development. You should have the P2 Knowledge Base 
repository information in CLAUDE.md.

Please access the P2 Knowledge Base directly from GitHub:
https://github.com/ironsheep/P2-Knowledge-Base

Start by reading the root manifest for navigation:
https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/manifests/p2-knowledge-root.yaml

This root manifest will guide you to:
- PASM2 instructions (357 total)
- Smart Pin modes (32 modes)
- Spin2 language constructs
- Architecture documentation
- Code patterns and examples

My specific task is: [YOUR TASK HERE]
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