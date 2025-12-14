# AI Integration Guide for P2 Knowledge Base v3.0
*Key-based access - simple and reliable*

**Repository**: https://github.com/ironsheep/P2-Knowledge-Base

> **Version 3.0**: Key-based access system replaces manifest navigation. No more path construction - just use keys like `p2kbPasm2Mov`.

## Quick Navigation

| Resource | Purpose |
|----------|---------|
| **[QuickStart](../../../../CLAUDE-QUICKSTART.md)** | Setup in 3 steps |
| **[Prompt Patterns](../../../../AI-PROMPT-PATTERNS.md)** | Key-based interaction examples |
| **[Privacy Guide](../../developer-docs/ai-development/Claude-Code-Privacy-Guide-for-P2-Developers.pdf)** | Protect your IP |

---

## 1. Setup (One-Time)

### Step 1: Create Cache Directory
```bash
mkdir -p .p2kb-cache
```

### Step 2: Download Fetch Script

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

### Step 3: Verify
```bash
.p2kb-cache/fetch-kb-file.sh p2kbArchCog --verbose
```

---

## 2. How It Works

### Key-Based Access

Every piece of content has a unique key:

| Key | Content |
|-----|---------|
| `p2kbPasm2Mov` | MOV instruction documentation |
| `p2kbArchCog` | COG architecture |
| `p2kbSpin2Pinwrite` | Spin2 PINWRITE method |
| `p2kbGuideQuickQueries` | Quick reference guide |

### Fetch Content

```bash
.p2kb-cache/fetch-kb-file.sh <key>
```

### Find Keys

```bash
# Search index for keys
jq '.files | keys[] | select(contains("Pasm2"))' .p2kb-cache/p2kb-index.json

# Grep-based search
grep -o '"p2kb[^"]*"' .p2kb-cache/p2kb-index.json | grep -i uart
```

---

## 3. Key Naming Convention

Keys follow the pattern: `p2kb` + Category + Name

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

---

## 4. Common Usage Patterns

### Start Here: Quick Queries
```bash
# Get the quick reference guide first
.p2kb-cache/fetch-kb-file.sh p2kbGuideQuickQueries
```

This guide maps common questions to relevant keys.

### PASM2 Instructions
```bash
# Get specific instruction
.p2kb-cache/fetch-kb-file.sh p2kbPasm2Mov
.p2kb-cache/fetch-kb-file.sh p2kbPasm2Add
```

### Spin2 Methods
```bash
# Get specific method
.p2kb-cache/fetch-kb-file.sh p2kbSpin2Pinwrite
.p2kb-cache/fetch-kb-file.sh p2kbSpin2Waitms
```

### Architecture
```bash
# Core architecture docs
.p2kb-cache/fetch-kb-file.sh p2kbArchCog
.p2kb-cache/fetch-kb-file.sh p2kbArchHub
.p2kb-cache/fetch-kb-file.sh p2kbArchCordic
```

---

## 5. P2 Philosophy

**P2 provides building blocks, NOT complete peripherals.**

| Traditional MCU | P2 Approach |
|----------------|-------------|
| Built-in UART | Smart Pins + software driver |
| Hardware SPI | COGs + software driver |
| I2C peripheral | Smart Pins + software driver |

---

## 6. Index Details

The index (`p2kb-index.json`) contains:

- **973 entries** mapping keys to file paths
- **Git mtime** for each file (change detection)
- **Full paths** (no construction needed)

### Index Structure
```json
{
  "system": {
    "version": "2.0.0",
    "generated": "2025-11-29T...",
    "total_entries": 973
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

## 7. Automatic Features

### Caching
- Files cached locally after first download
- Index auto-refreshes every 24 hours
- Delete `.p2kb-cache/content/` to force refresh

### Metadata Filtering
- Editorial metadata stripped on download
- Reduces token overhead by ~38,000 tokens
- Source YAMLs unchanged

---

## 8. Troubleshooting

### Key Not Found
```bash
# Verify key exists
grep "p2kbPasm2Mov" .p2kb-cache/p2kb-index.json
```

### Stale Content
```bash
# Clear content cache
rm -rf .p2kb-cache/content/

# Clear entire cache (forces fresh download)
rm -rf .p2kb-cache
```

### Network Issues
- Check internet connectivity
- Verify GitHub is accessible
- Try `--verbose` flag for diagnostics

---

## 9. Migration from v2.x

If you have old cached content:

1. **Delete** the old `.p2kb-cache/` directory
2. **Follow** the setup steps above
3. **Use keys** instead of paths

The v3.0 system eliminates:
- Path construction errors (404s)
- Manifest navigation complexity
- Stale path references

---

## 10. Golden Rules

1. **Use keys** - Never construct paths manually
2. **Start with Quick Queries** - `p2kbGuideQuickQueries` maps questions to keys
3. **Search the index** - Use jq or grep to find keys
4. **Trust the cache** - Auto-refresh handles updates
5. **P2 = building blocks** - Check drivers for peripherals

---

*Version 3.0 - Key-Based Access*
*Last Updated: 2025-11-29*
