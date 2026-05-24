# AI Integration Guide for P2 Knowledge Base
*Two consumption paths: MCP (recommended) or fetch-script*

**Repository**: https://github.com/ironsheep/P2-Knowledge-Base

## Quick Navigation

| Resource | Purpose |
|----------|---------|
| **[QuickStart](../../../../CLAUDE-QUICKSTART.md)** | Setup quickstart (MCP or fetch-script) |
| **[Prompt Patterns](../../../../AI-PROMPT-PATTERNS.md)** | Interaction examples (both paths) |
| **[Privacy Guide](../../../../deliverables/developer-docs/ai-development/Claude-Code-Privacy-Guide-for-P2-Developers.pdf)** | Protect your IP |

---

## ⭐ With MCP (recommended path)

If your agent supports the Model Context Protocol — Claude Code, Claude Desktop, ChatGPT with MCP support, and others — installing the **[P2 Knowledge Base MCP](https://github.com/ironsheep/P2-Knowledge-Base-MCP)** gives the best experience. The MCP provides native tool calls to query the KB; the server handles indexing, caching, and search internally. No local cache to manage; always serves the latest published content.

### Setup

Follow the MCP install instructions: **[https://github.com/ironsheep/P2-Knowledge-Base-MCP/blob/main/INSTALL.md](https://github.com/ironsheep/P2-Knowledge-Base-MCP/blob/main/INSTALL.md)**

Once installed and configured, your agent has access to these tools:

| Tool | Purpose |
|------|---------|
| `p2kb_get` | Fetch a specific instruction, method, or concept by name or natural-language query |
| `p2kb_find` | Discover what's documented; list categories or search keys |
| `p2kb_obex_get` | Look up a specific OBEX community object |
| `p2kb_obex_find` | Browse OBEX by category, author, or keyword |
| `p2kb_obex_download` | Download and extract an OBEX object's source |
| `p2kb_refresh` | Force-refresh the index after KB updates |
| `p2kb_version` | Server + index version info |

### Usage

Ask your agent questions naturally — it picks the right tool. No key prefixes to memorize, no command syntax to learn.

```
"How does the P2 ADD instruction work?"
"Configure a Smart Pin for UART transmit."
"Find OBEX objects for the HD44780 LCD."
"Explain P2 COG architecture."
```

See **[AI-PROMPT-PATTERNS.md](../../../../AI-PROMPT-PATTERNS.md)** for more example queries.

### Troubleshooting

- **MCP tools not available**: Verify the MCP server is configured in your agent's MCP settings; restart your agent
- **Stale results after a KB update**: Call `p2kb_refresh` to refresh the server's index cache
- **Connection errors**: Check the MCP server logs per the install guide

---

## Without MCP (fetch-script path)

If your agent doesn't support MCP, use the key-based fetch-script system. The patterns below let you ask precisely for content by key.

### Setup (One-Time)

#### Step 1: Create Cache Directory
```bash
mkdir -p .p2kb-cache
```

#### Step 2: Download Fetch Script

**Unix/macOS/Linux:**
```bash
curl -sS https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/engineering/tools/p2kb/fetch-kb-file.sh > .p2kb-cache/fetch-kb-file.sh
chmod +x .p2kb-cache/fetch-kb-file.sh
```

**Windows PowerShell:**
```powershell
mkdir ".p2kb-cache" -Force
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/engineering/tools/p2kb/fetch-kb-file.ps1" -OutFile ".p2kb-cache\fetch-kb-file.ps1"
```

#### Step 3: Verify
```bash
.p2kb-cache/fetch-kb-file.sh p2kbArchCog --verbose
```

### How It Works

#### Key-Based Access

Every piece of content has a unique key:

| Key | Content |
|-----|---------|
| `p2kbPasm2Mov` | MOV instruction documentation |
| `p2kbArchCog` | COG architecture |
| `p2kbSpin2Pinwrite` | Spin2 PINWRITE method |
| `p2kbGuideQuickQueries` | Quick reference guide |

#### Fetch Content
```bash
.p2kb-cache/fetch-kb-file.sh <key>
```

#### Find Keys
```bash
# Search index for keys
jq '.files | keys[] | select(contains("Pasm2"))' .p2kb-cache/p2kb-index.json

# Grep-based search
grep -o '"p2kb[^"]*"' .p2kb-cache/p2kb-index.json | grep -i uart
```

### Common Usage Patterns

#### Start Here: Quick Queries
```bash
# Get the quick reference guide first
.p2kb-cache/fetch-kb-file.sh p2kbGuideQuickQueries
```

This guide maps common questions to relevant keys.

#### PASM2 Instructions
```bash
.p2kb-cache/fetch-kb-file.sh p2kbPasm2Mov
.p2kb-cache/fetch-kb-file.sh p2kbPasm2Add
```

#### Spin2 Methods
```bash
.p2kb-cache/fetch-kb-file.sh p2kbSpin2Pinwrite
.p2kb-cache/fetch-kb-file.sh p2kbSpin2Waitms
```

#### Architecture
```bash
.p2kb-cache/fetch-kb-file.sh p2kbArchCog
.p2kb-cache/fetch-kb-file.sh p2kbArchHub
.p2kb-cache/fetch-kb-file.sh p2kbArchCordic
```

### Automatic Features

- **Caching**: Files cached locally after first download
- **Index auto-refresh**: Every 24 hours
- **Metadata filtering**: Editorial metadata stripped on download (reduces token overhead)
- **Force refresh**: Delete `.p2kb-cache/content/` (or the entire `.p2kb-cache/`) for a fresh download

### Troubleshooting (fetch-script)

#### Key Not Found
```bash
grep "p2kbPasm2Mov" .p2kb-cache/p2kb-index.json
```

#### Stale Content
```bash
# Clear content cache
rm -rf .p2kb-cache/content/

# Clear entire cache (forces fresh download)
rm -rf .p2kb-cache
```

#### Network Issues
- Check internet connectivity
- Verify GitHub is accessible
- Try `--verbose` flag for diagnostics

### Golden Rules (fetch-script)

1. **Use keys** - Never construct paths manually
2. **Start with Quick Queries** - `p2kbGuideQuickQueries` maps questions to keys
3. **Search the index** - Use jq or grep to find keys
4. **Trust the cache** - Auto-refresh handles updates

---

## Reference (both paths)

### Key Naming Convention

Keys follow the pattern: `p2kb` + Category + Name. Useful for fetch-script users running searches; informative for MCP users curious about the KB's organization.

| Prefix | Content Type | Examples |
|--------|--------------|----------|
| `p2kbPasm2` | PASM2 instructions | `p2kbPasm2Mov`, `p2kbPasm2Add`, `p2kbPasm2Jmp` |
| `p2kbSpin2` | Spin2 methods | `p2kbSpin2Pinwrite`, `p2kbSpin2Waitms` |
| `p2kbSpin2Kw` | Spin2 keywords | `p2kbSpin2KwRepeat`, `p2kbSpin2KwIf` |
| `p2kbSpin2Op` | Spin2 operators | `p2kbSpin2OpAdd` |
| `p2kbArch` | Architecture | `p2kbArchCog`, `p2kbArchHub`, `p2kbArchCordic` |
| `p2kbSmartPin` | Smart Pin modes | `p2kbSmartPinAsyncSerial` |
| `p2kbGuide` | Guides | `p2kbGuideQuickQueries` |
| `p2kbHw` | Hardware | `p2kbHwP2Eval` |

### P2 Philosophy

**P2 provides building blocks, NOT complete peripherals.**

| Traditional MCU | P2 Approach |
|----------------|-------------|
| Built-in UART | Smart Pins + software driver |
| Hardware SPI | COGs + software driver |
| I2C peripheral | Smart Pins + software driver |

### Index Details

The published index (`deliverables/ai/p2kb-index.json`) maps keys to file paths. The MCP server queries this index server-side; fetch-script users download a cached copy for local lookup.

```json
{
  "system": {
    "version": "...",
    "generated": "...",
    "total_entries": "..."
  },
  "files": {
    "p2kbPasm2Mov": {
      "path": "deliverables/ai/P2/language/pasm2/mov.yaml",
      "mtime": 1732900000
    }
  }
}
```

---

*Last updated: 2026-05-24*
