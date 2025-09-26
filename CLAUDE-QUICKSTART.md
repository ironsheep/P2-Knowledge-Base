# Claude Code Quick Start Card
*Essential copy-paste templates to get started with the P2 Knowledge Base*

## ⚠️ CRITICAL: Session Management for Performance

**🔥 Clear conversation every 3-4 hours or 15-20 major file operations!**

Performance degrades as context accumulates. Watch for these warning signs:
- Responses getting slower
- Claude forgetting recent work
- Repetitive questions about already-discussed topics

### Session Health Indicators
- ✅ **Healthy (0-3 hours)**: Fast responses, perfect recall
- ⚠️ **Warning (3-4 hours)**: Slightly slower, may need reminders
- ❌ **Clear Now (4+ hours)**: Degraded performance, confusion

## 🚀 Essential Templates (Copy These!)

### 1. Session Starter (Optimized for Success)
```
I need help with P2 (Propeller 2) development. You should have the P2 Knowledge Base 
repository information in CLAUDE.md.

Please access the P2 Knowledge Base directly from GitHub:
https://github.com/ironsheep/P2-Knowledge-Base

CRITICAL: Start with these two manifests:
1. Root manifest: manifests/p2-knowledge-root.yaml (main navigation)
2. Auxiliary guides: manifests/auxiliary-guides-manifest.yaml (HOW to use resources)

The auxiliary guides teach you:
- OBEX search optimization (NEVER filter by category first)
- Hardware testing workflows with pnut_ts and pnut-term-ts
- BMP generation for debug visualization
- Best practices for P2 development

My specific task is: [YOUR TASK HERE]
```

### 2. PASM2 Assembly Code
```
Using the P2 knowledge base PASM2 instructions in 
engineering/knowledge-base/P2/language/pasm2/, 
help me write assembly code to [DESCRIBE TASK].

Check manifests/pasm2-manifest.yaml for instruction categories.
```

### 3. Smart Pin Configuration
```
I need to configure a P2 Smart Pin for [PURPOSE].
Check engineering/knowledge-base/P2/hardware/smart-pins/modes/
and help me select and configure the right mode.
```

### 4. Community Code Discovery (Optimized)
```
Find me P2 OBEX objects related to [HARDWARE/PROTOCOL].

IMPORTANT: Follow the OBEX search optimization guide:
- Search ALL 113 objects, not just expected categories
- Many drivers are in 'misc' (34 objects), not 'drivers'
- Expand keywords: I2C → also search IIC, TWI, two-wire
- Check top authors like jonnymac (44 quality objects)

Start with manifests/obex/obex-root.yaml
```

### 5. Using Auxiliary Guides
```
I need help with [BMP generation / hardware testing / OBEX search].
Check manifests/auxiliary-guides-manifest.yaml for specialized guides.
These guides provide techniques for specific development tasks.
```

### 6. Session Resume (After Clearing)
```
Continuing P2 development session. Previous summary:
[PASTE SUMMARY HERE]

The P2 Knowledge Base info should be in CLAUDE.md.
Please continue with: [SPECIFIC NEXT TASK]
```

## 📚 Need More Examples?

**[→ AI Prompt Patterns Library](AI-PROMPT-PATTERNS.md)**  
Comprehensive interaction patterns for all P2 development scenarios.

**[→ Using With AI Guide](deliverables/ai-reference/auxiliary-guides/interaction/using-with-ai.md)**  
Complete setup and usage guide for AI assistants.

## 💡 Quick Tips

- Always mention "P2 Knowledge Base" in prompts
- Start with manifests for navigation
- Reference specific YAML paths when possible
- For community code, specify category or author
- Clear conversation when performance degrades

## 🔑 Critical P2 Knowledge Base Insights

**OBEX Search**: NEVER filter by category first - 34 "misc" objects contain drivers!

**P2 Philosophy**: P2 provides building blocks (Smart Pins, COGs), not complete peripherals.
Need UART/SPI/I2C? → Use OBEX objects, not built-in peripherals.

**File Navigation**: Follow manifest tree, never guess paths. All files are YAML.

**Testing**: Use `pnut_ts -d` for debug, monitor `logs/*.log` not console.

---

*Keep this card handy for instant P2 development assistance!*