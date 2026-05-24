# AI Prompt Patterns for P2 Knowledge Base
*Prompt patterns for AI assistants consuming the P2 Knowledge Base*

---

## ⭐ With MCP (recommended path)

If you've installed the **[P2 Knowledge Base MCP](https://github.com/ironsheep/P2-Knowledge-Base-MCP)**, your agent has native tool calls for KB queries. The MCP's tools self-describe — you mostly just ask questions naturally and the agent picks the right tool. No key-prefix knowledge required. No local cache to manage. Always serves the latest published content.

**[→ MCP install instructions](https://github.com/ironsheep/P2-Knowledge-Base-MCP/blob/main/INSTALL.md)**

### Example natural-language queries

**PASM2 instructions:**
- "How does the P2 ADD instruction work?"
- "What are all the P2 branching instructions?"
- "Show me the timing for RDLONG."
- "What's the encoding for XINIT?"

**Smart Pins:**
- "Configure a Smart Pin for UART transmit."
- "Which Smart Pin mode generates a PWM output?"
- "What does Smart Pin mode %00101 do?"
- "How do I read a Smart Pin's result?"

**Spin2 high-level language:**
- "How do I write to a pin in Spin2?"
- "What timing methods does Spin2 provide?"
- "Show me the REPEAT keyword syntax."
- "What's the difference between WAITMS and WAITUS?"

**Architecture & subsystems:**
- "Explain P2 COG architecture."
- "How does P2 boot from SPI flash?"
- "What's the relationship between the streamer and smart pins?"
- "How does the CORDIC engine work?"

**OBEX community code:**
- "Find OBEX objects for the HD44780 LCD."
- "Show me community drivers for SD cards."
- "Download object 4321 from OBEX."

### What the MCP tools cover

| Tool | Purpose |
|------|---------|
| `p2kb_get` | Fetch a specific instruction, method, or concept by name or natural-language query |
| `p2kb_find` | Discover what's documented; list categories or search keys |
| `p2kb_obex_get` | Look up a specific OBEX community object |
| `p2kb_obex_find` | Browse OBEX by category, author, or keyword |
| `p2kb_obex_download` | Download and extract an OBEX object's source |
| `p2kb_refresh` | Force-refresh the index after KB updates |
| `p2kb_version` | Server + index version info |

---

## Without MCP (fetch-script path)

If your agent doesn't support MCP, use the fetch-script-based BOOTSTRAP. See [`deliverables/ai-reference/BOOTSTRAP.md`](deliverables/ai-reference/BOOTSTRAP.md) for setup. The patterns below let you ask precisely for content by key.

### 📚 Quick Start

#### First, Start with Quick Queries
```
Fetch p2kbGuideQuickQueries to find relevant keys for my task:
[DESCRIBE WHAT YOU WANT TO DO]
```

This guide maps common questions to specific content keys.

### 🔧 PASM2 Assembly Programming

#### Instruction Lookup
```
I need help with the P2 ADD instruction.
Fetch: p2kbPasm2Add
```

#### Find Instructions by Category
```
What branching instructions does P2 have?
Search the index for keys containing "Pasm2" and "jmp" or "call"
```

#### Assembly Code Help
```
Using keys like p2kbPasm2Mov, p2kbPasm2Add, p2kbPasm2Jmp,
help me write assembly code to [DESCRIBE TASK].
```

### 🔌 Smart Pin Configuration

#### Find Smart Pin Modes
```
I need to configure a P2 Smart Pin for UART.
Search index for SmartPin keys related to serial/async.
```

#### Specific Mode Lookup
```
Fetch p2kbSmartPinAsyncSerialTransmit for UART TX configuration.
Fetch p2kbSmartPinAsyncSerialReceive for UART RX configuration.
```

### 🔄 Spin2 High-Level Programming

#### Method Lookup
```
How do I write to a pin in Spin2?
Fetch: p2kbSpin2Pinwrite
```

#### Find Methods
```
What timing methods are available in Spin2?
Search for keys: p2kbSpin2Wait*
```

#### Keywords and Operators
```
Fetch p2kbSpin2KwRepeat for REPEAT keyword syntax.
Fetch p2kbSpin2OpAdd for addition operator details.
```

### 🏗️ Architecture Questions

#### Core Architecture
```
Explain P2 COG architecture.
Fetch: p2kbArchCog

Explain P2 Hub memory.
Fetch: p2kbArchHub

Explain P2 CORDIC operations.
Fetch: p2kbArchCordic
```

#### System Components
```
How does P2 clock system work?
Fetch: p2kbArchClockSystem

How do P2 locks work?
Fetch: p2kbArchLocks
```

### 🔍 Finding Keys

#### Search by Prefix
```bash
# All PASM2 instructions
jq '.files | keys[] | select(startswith("p2kbPasm2"))' .p2kb-cache/p2kb-index.json

# All Spin2 methods
jq '.files | keys[] | select(startswith("p2kbSpin2"))' .p2kb-cache/p2kb-index.json

# All Smart Pin modes
jq '.files | keys[] | select(contains("SmartPin"))' .p2kb-cache/p2kb-index.json
```

#### Search by Keyword
```bash
# Find UART-related content
grep -o '"p2kb[^"]*"' .p2kb-cache/p2kb-index.json | grep -i uart

# Find timer-related content
grep -o '"p2kb[^"]*"' .p2kb-cache/p2kb-index.json | grep -i wait
```

### 💡 Common Tasks

#### Blink an LED
```
Fetch p2kbGuideQuickQueries and look for "blink" question.
Then fetch the referenced keys: p2kbPasm2Drvh, p2kbPasm2Drvl,
p2kbSpin2Pinhigh, p2kbSpin2Pinlow
```

#### Implement UART
```
Search for SmartPin async serial keys.
Fetch p2kbSmartPinAsyncSerialTransmit and p2kbSmartPinAsyncSerialReceive
```

#### Start Another COG
```
Fetch p2kbArchCog for COG architecture.
Fetch p2kbSpin2Coginit and p2kbSpin2Cogspin for methods.
```

#### Create Delays
```
Fetch p2kbSpin2Waitms for millisecond delays.
Fetch p2kbSpin2Waitus for microsecond delays.
Fetch p2kbPasm2Waitx for assembly delays.
```

### 🆘 Troubleshooting

#### Key Not Found
```
Verify key exists: grep "keyname" .p2kb-cache/p2kb-index.json
Keys are case-sensitive and always start with "p2kb"
```

#### Finding Related Content
```
Start with p2kbGuideQuickQueries to find relevant keys.
Use jq or grep to search the index for similar keys.
```

#### Validate Code
```
Fetch the relevant instruction/method YAML and check:
- Syntax examples
- Parameter descriptions
- Usage notes
```

### 📝 Prompt Guidelines (fetch-script path)

1. **Use keys directly**: "Fetch p2kbPasm2Mov" instead of path navigation
2. **Start with Quick Queries**: p2kbGuideQuickQueries maps questions to keys
3. **Search the index**: Use jq or grep to find relevant keys
4. **Combine related keys**: Fetch multiple related keys for complete context
5. **Check key prefixes**: Know which prefix matches your content type

---

## 🔑 Key Prefix Reference (both paths)

Useful for fetch-script users searching the index, and informative for MCP users curious about the KB's organization.

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

*Last updated: 2026-05-24*
