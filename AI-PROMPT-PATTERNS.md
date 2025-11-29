# AI Prompt Patterns for P2 Knowledge Base v3.0
*Key-based interaction patterns for AI assistants*

## 📚 Quick Start

### First, Start with Quick Queries
```
Fetch p2kbGuideQuickQueries to find relevant keys for my task:
[DESCRIBE WHAT YOU WANT TO DO]
```

This guide maps common questions to specific content keys.

---

## 🔧 PASM2 Assembly Programming

### Instruction Lookup
```
I need help with the P2 ADD instruction.
Fetch: p2kbPasm2Add
```

### Find Instructions by Category
```
What branching instructions does P2 have?
Search the index for keys containing "Pasm2" and "jmp" or "call"
```

### Assembly Code Help
```
Using keys like p2kbPasm2Mov, p2kbPasm2Add, p2kbPasm2Jmp,
help me write assembly code to [DESCRIBE TASK].
```

---

## 🔌 Smart Pin Configuration

### Find Smart Pin Modes
```
I need to configure a P2 Smart Pin for UART.
Search index for SmartPin keys related to serial/async.
```

### Specific Mode Lookup
```
Fetch p2kbSmartPinAsyncSerialTransmit for UART TX configuration.
Fetch p2kbSmartPinAsyncSerialReceive for UART RX configuration.
```

---

## 🔄 Spin2 High-Level Programming

### Method Lookup
```
How do I write to a pin in Spin2?
Fetch: p2kbSpin2Pinwrite
```

### Find Methods
```
What timing methods are available in Spin2?
Search for keys: p2kbSpin2Wait*
```

### Keywords and Operators
```
Fetch p2kbSpin2KwRepeat for REPEAT keyword syntax.
Fetch p2kbSpin2OpAdd for addition operator details.
```

---

## 🏗️ Architecture Questions

### Core Architecture
```
Explain P2 COG architecture.
Fetch: p2kbArchCog

Explain P2 Hub memory.
Fetch: p2kbArchHub

Explain P2 CORDIC operations.
Fetch: p2kbArchCordic
```

### System Components
```
How does P2 clock system work?
Fetch: p2kbArchClockSystem

How do P2 locks work?
Fetch: p2kbArchLocks
```

---

## 🔍 Finding Keys

### Search by Prefix
```bash
# All PASM2 instructions
jq '.files | keys[] | select(startswith("p2kbPasm2"))' ~/.p2kb-cache/p2kb-index.json

# All Spin2 methods
jq '.files | keys[] | select(startswith("p2kbSpin2"))' ~/.p2kb-cache/p2kb-index.json

# All Smart Pin modes
jq '.files | keys[] | select(contains("SmartPin"))' ~/.p2kb-cache/p2kb-index.json
```

### Search by Keyword
```bash
# Find UART-related content
grep -o '"p2kb[^"]*"' ~/.p2kb-cache/p2kb-index.json | grep -i uart

# Find timer-related content
grep -o '"p2kb[^"]*"' ~/.p2kb-cache/p2kb-index.json | grep -i wait
```

---

## 🔑 Key Prefix Reference

| Prefix | Content Type | Examples |
|--------|--------------|----------|
| `p2kbPasm2` | PASM2 instructions | `p2kbPasm2Mov`, `p2kbPasm2Add` |
| `p2kbSpin2` | Spin2 methods | `p2kbSpin2Pinwrite`, `p2kbSpin2Waitms` |
| `p2kbSpin2Kw` | Spin2 keywords | `p2kbSpin2KwRepeat`, `p2kbSpin2KwIf` |
| `p2kbSpin2Op` | Spin2 operators | `p2kbSpin2OpAdd`, `p2kbSpin2OpAnd` |
| `p2kbSpin2Reg` | Spin2 registers | `p2kbSpin2RegDira`, `p2kbSpin2RegOuta` |
| `p2kbArch` | Architecture | `p2kbArchCog`, `p2kbArchHub` |
| `p2kbSmartPin` | Smart Pin modes | `p2kbSmartPinUart` |
| `p2kbGuide` | Guides | `p2kbGuideQuickQueries` |
| `p2kbHw` | Hardware | `p2kbHwP2Eval` |

---

## 💡 Common Tasks

### Blink an LED
```
Fetch p2kbGuideQuickQueries and look for "blink" question.
Then fetch the referenced keys: p2kbPasm2Drvh, p2kbPasm2Drvl,
p2kbSpin2Pinhigh, p2kbSpin2Pinlow
```

### Implement UART
```
Search for SmartPin async serial keys.
Fetch p2kbSmartPinAsyncSerialTransmit and p2kbSmartPinAsyncSerialReceive
```

### Start Another COG
```
Fetch p2kbArchCog for COG architecture.
Fetch p2kbSpin2Coginit and p2kbSpin2Cogspin for methods.
```

### Create Delays
```
Fetch p2kbSpin2Waitms for millisecond delays.
Fetch p2kbSpin2Waitus for microsecond delays.
Fetch p2kbPasm2Waitx for assembly delays.
```

---

## 🆘 Troubleshooting

### Key Not Found
```
Verify key exists: grep "keyname" ~/.p2kb-cache/p2kb-index.json
Keys are case-sensitive and always start with "p2kb"
```

### Finding Related Content
```
Start with p2kbGuideQuickQueries to find relevant keys.
Use jq or grep to search the index for similar keys.
```

### Validate Code
```
Fetch the relevant instruction/method YAML and check:
- Syntax examples
- Parameter descriptions
- Usage notes
```

---

## 📝 Prompt Guidelines

1. **Use keys directly**: "Fetch p2kbPasm2Mov" instead of path navigation
2. **Start with Quick Queries**: p2kbGuideQuickQueries maps questions to keys
3. **Search the index**: Use jq or grep to find relevant keys
4. **Combine related keys**: Fetch multiple related keys for complete context
5. **Check key prefixes**: Know which prefix matches your content type

---

*Version 3.0 - Key-Based Access Patterns*
*Last Updated: 2025-11-29*
