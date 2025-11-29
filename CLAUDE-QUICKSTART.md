# P2 Knowledge Base QuickStart v3.0
*Key-based access - simple and reliable*

## Overview

v3.0 uses **keys** to access content. No path construction needed.

- Keys like `p2kbPasm2Mov` map directly to YAML files
- One index contains all ~970 content files
- Automatic caching and metadata filtering

## 🚀 Setup (3 Steps)

### Step 1: Create Cache Directory

```bash
mkdir -p ~/.p2kb-cache
```

### Step 2: Download Fetch Script

**Unix/macOS/Linux:**
```bash
curl -sS https://raw.githubusercontent.com/IronSheepProductionsLLC/P2-Knowledge-Base/main/engineering/tools/p2kb/fetch-kb-file.sh > ~/.p2kb-cache/fetch-kb-file.sh
chmod +x ~/.p2kb-cache/fetch-kb-file.sh
```

**Windows PowerShell:**
```powershell
mkdir "$env:USERPROFILE\.p2kb-cache" -Force
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/IronSheepProductionsLLC/P2-Knowledge-Base/main/engineering/tools/p2kb/fetch-kb-file.ps1" -OutFile "$env:USERPROFILE\.p2kb-cache\fetch-kb-file.ps1"
```

### Step 3: Verify Setup

```bash
~/.p2kb-cache/fetch-kb-file.sh p2kbArchCog --verbose
```

✅ Setup complete when you see YAML content output.

---

## 📖 Usage

### Fetch Content by Key

```bash
# Architecture documentation
~/.p2kb-cache/fetch-kb-file.sh p2kbArchCog
~/.p2kb-cache/fetch-kb-file.sh p2kbArchHub

# PASM2 instructions
~/.p2kb-cache/fetch-kb-file.sh p2kbPasm2Mov
~/.p2kb-cache/fetch-kb-file.sh p2kbPasm2Add

# Spin2 methods
~/.p2kb-cache/fetch-kb-file.sh p2kbSpin2Pinwrite
~/.p2kb-cache/fetch-kb-file.sh p2kbSpin2Waitms

# Quick reference guide
~/.p2kb-cache/fetch-kb-file.sh p2kbGuideQuickQueries
```

### Find Keys

```bash
# Search index for keys containing "Pasm2"
jq '.files | keys[] | select(contains("Pasm2"))' ~/.p2kb-cache/p2kb-index.json

# Find Smart Pin keys
jq '.files | keys[] | select(contains("SmartPin"))' ~/.p2kb-cache/p2kb-index.json

# Grep-based search (no jq required)
grep -o '"p2kb[^"]*"' ~/.p2kb-cache/p2kb-index.json | grep -i uart
```

---

## 🔑 Key Prefixes

| Prefix | Content Type | Example |
|--------|--------------|---------|
| `p2kbPasm2` | PASM2 instructions | `p2kbPasm2Mov` |
| `p2kbSpin2` | Spin2 methods | `p2kbSpin2Pinwrite` |
| `p2kbArch` | Architecture docs | `p2kbArchCog` |
| `p2kbSmartPin` | Smart Pin modes | `p2kbSmartPinUart` |
| `p2kbGuide` | Guides | `p2kbGuideQuickQueries` |
| `p2kbHw` | Hardware specs | `p2kbHwP2Eval` |

---

## 🔧 Cache Management

**Check size:**
```bash
du -sh ~/.p2kb-cache
```

**Clear cache (forces refresh):**
```bash
rm -rf ~/.p2kb-cache
```

**Force index refresh:**
```bash
rm ~/.p2kb-cache/p2kb-index.json
```

---

## 📋 Troubleshooting

**"Key not found":**
- Verify the key exists: `grep "keyname" ~/.p2kb-cache/p2kb-index.json`
- Keys are case-sensitive and start with `p2kb`

**Stale content:**
- Index auto-refreshes every 24 hours
- Delete specific cached file to force refresh
- Or clear entire cache: `rm -rf ~/.p2kb-cache`

**Network errors:**
- Check internet connectivity
- Verify GitHub is accessible

---

## 💡 Notes

- **Cache location:** `~/.p2kb-cache/`
- **Index size:** ~130KB (13KB compressed)
- **Total content:** 973 YAML files
- **Auto-refresh:** Index checks for updates every 24 hours

---

*Version 3.0 - Key-Based Access*
*Last Updated: 2025-11-29*
