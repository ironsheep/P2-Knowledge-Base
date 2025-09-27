# P2 Knowledge Base QuickStart
*Essential reference for using P2 Knowledge Base with Claude*

## 🚀 For Fresh Claude Session (After /init)

Copy this entire block to Claude to configure it properly:

```
FIRST ACTION: Save these instructions to your CLAUDE.md file for persistent reference.

You are helping with Propeller 2 (P2) microcontroller development using the P2 Knowledge Base.
GitHub: https://github.com/ironsheep/P2-Knowledge-Base
Raw access: https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/

## CRITICAL RULES - NO EXCEPTIONS

### Navigation (MANDATORY)
- START: manifests/p2-knowledge-root.yaml (always)
- THEN: manifests/auxiliary-guides-manifest.yaml (how-to guides)
- NEVER search for YAML files - use manifest tree only
- All files are YAML format in engineering/knowledge-base/P2/

### Anti-Patterns (FORBIDDEN)
❌ Searching for *.yaml directly
❌ Guessing paths ("probably in hardware/")  
❌ Using pkill (use: kill -TERM $PID)
❌ Filtering OBEX by category first
❌ Assuming built-in peripherals exist

### Testing Protocol
    pnut_ts -d program.spin2              # Compile with debug
    pnut-term-ts -r program.bin & PID=$!  # Run and capture PID
    tail -f logs/debug_*.log              # Monitor logs (not console)
    kill -TERM $PID                       # Clean shutdown (not pkill)
    # Signals: -TERM (shutdown), -USR1 (reset), -9 (force)

### OBEX Search Rules
- Search ALL 113 objects first (34 in 'misc' have drivers!)
- Expand terms: I2C → IIC, TWI, two-wire
- Check jonnymac (44 objects)
- 21 objects have GitHub links

### P2 Architecture Facts
- 8 COGs (cores), 64 Smart Pins
- No built-in UART/SPI/I2C → use OBEX objects
- Smart Pins = autonomous I/O processors
- Building blocks, not complete peripherals

## Manifest Navigation Map

Start → manifests/p2-knowledge-root.yaml
├── PASM2 → pasm2-manifest.yaml → 360+ instructions
├── Smart Pins → hardware/smart-pins/modes/
├── OBEX → obex/obex-root.yaml → 113 objects
└── Guides → auxiliary-guides-manifest.yaml

REMEMBER: Manifest tree only. No direct YAML searches. PID-based signals only.
```

## 💡 Common Task Templates

### PASM2 Assembly Code
```
Using the P2 knowledge base, help me write PASM2 code to [TASK].
Start with manifests/pasm2-manifest.yaml for instruction categories.
```

### Smart Pin Configuration  
```
I need to configure a Smart Pin for [PURPOSE].
Check hardware/smart-pins/modes/ via the manifest tree.
```

### OBEX Community Code
```
Find P2 OBEX objects for [HARDWARE/PROTOCOL].
Search ALL 113 objects via manifests/obex/obex-root.yaml.
Don't filter by category first - many drivers are in 'misc'.
```

### Hardware Testing
```
Test my Spin2 program on P2 hardware.
Use pnut_ts -d for debug compilation.
Capture PID with & and use kill -TERM $PID for cleanup.
```

## ⚠️ Session Management

**Clear conversation every 3-4 hours to maintain performance!**

- ✅ **0-3 hours**: Fast responses, perfect recall
- ⚠️ **3-4 hours**: Slower, may need reminders  
- ❌ **4+ hours**: Degraded performance, clear now

### Session Resume After Clear
```
Continuing P2 development. Previous: [BRIEF SUMMARY]
Check CLAUDE.md for P2 Knowledge Base rules.
Continue with: [SPECIFIC TASK]
```

## 🔑 Key Insights

**OBEX Search**: 34 "misc" objects contain drivers - always search all!

**P2 Philosophy**: Building blocks (COGs, Smart Pins), not complete peripherals.

**File Access**: Follow manifests only, never guess YAML paths.

**Testing**: Use PID-based signals, monitor logs not console.

**GitHub Repos**: 21 OBEX objects have links - mention but don't auto-fetch.

## 📚 Additional Resources

- **Full Guide**: deliverables/ai-reference/auxiliary-guides/interaction/using-with-ai.md
- **Prompt Patterns**: AI-PROMPT-PATTERNS.md
- **Testing Guide**: auxiliary-guides/special-techniques/hardware-testing-guide.md

---
*Keep this card handy for P2 development with Claude!*