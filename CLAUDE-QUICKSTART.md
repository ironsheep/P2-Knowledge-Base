# P2 Knowledge Base QuickStart v3.2
*Key-based access with navigation support*

## Overview

v3.2 uses **keys** to access content with built-in navigation.

- Keys like `p2kbPasm2Mov` map directly to YAML files
- Use `--search` and `--browse` to find keys - never guess!
- Automatic caching and metadata filtering
- ~970 content files organized into 45 categories

## 🚨 IMPORTANT: Script-Only Access

**ALWAYS use the fetch script. NEVER access index or cache files directly.**

- ❌ DON'T: `jq ... ~/.p2kb/p2kb-index.json`
- ❌ DON'T: `cat ~/.p2kb/cache/...`
- ❌ DON'T: Guess at key names
- ✅ DO: Use `--search`, `--browse`, `--cached` commands

---

## 🚀 Setup (3 Steps)

### Step 1: Create Script Directory

```bash
mkdir -p ~/.p2kb-cache
```

### Step 2: Download Fetch Script

**Unix/macOS/Linux:**
```bash
curl -sS https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/engineering/tools/p2kb/fetch-kb-file.sh > ~/.p2kb-cache/fetch-kb-file.sh
chmod +x ~/.p2kb-cache/fetch-kb-file.sh
```

**Windows PowerShell:**
```powershell
mkdir "$env:USERPROFILE\.p2kb-cache" -Force
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/engineering/tools/p2kb/fetch-kb-file.ps1" -OutFile "$env:USERPROFILE\.p2kb-cache\fetch-kb-file.ps1"
```

### Step 3: Verify Setup

```bash
~/.p2kb-cache/fetch-kb-file.sh --help
```

✅ Setup complete when you see the help message with available commands.

---

## 📖 Usage

### Get Help
```bash
~/.p2kb-cache/fetch-kb-file.sh --help
```

### Find Keys

```bash
# Search for keys containing a term (case-insensitive)
~/.p2kb-cache/fetch-kb-file.sh --search uart
~/.p2kb-cache/fetch-kb-file.sh --search cordic
~/.p2kb-cache/fetch-kb-file.sh --search mov

# Browse keys by category
~/.p2kb-cache/fetch-kb-file.sh --browse pasm2_branch
~/.p2kb-cache/fetch-kb-file.sh --browse architecture_core
~/.p2kb-cache/fetch-kb-file.sh --browse smart_pins_serial

# List all categories
~/.p2kb-cache/fetch-kb-file.sh --categories
```

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

### Check Downloaded Files

```bash
~/.p2kb-cache/fetch-kb-file.sh --cached
```

---

## 🔑 Key Prefixes

| Prefix | Content Type | Example |
|--------|--------------|---------|
| `p2kbPasm2` | PASM2 instructions | `p2kbPasm2Mov` |
| `p2kbSpin2` | Spin2 methods | `p2kbSpin2Pinwrite` |
| `p2kbArch` | Architecture docs | `p2kbArchCog` |
| `p2kbGuide` | Guides | `p2kbGuideQuickQueries` |
| `p2kbHw` | Hardware specs | `p2kbHwP2Eval` |

---

## 📂 Categories (for --browse)

**PASM2 Instructions:**
- `pasm2_directives`, `pasm2_branch`, `pasm2_cordic`, `pasm2_math`, `pasm2_pin`
- `pasm2_event`, `pasm2_hub_control`, `pasm2_hub_fifo`, `pasm2_hub_ram`
- `pasm2_interrupt`, `pasm2_lookup_table`, `pasm2_misc`, `pasm2_pixel`
- `pasm2_register_indirection`, `pasm2_smart_pin`, `pasm2_streamer`

**Architecture:**
- `architecture_core`, `architecture_math`, `architecture_timing`
- `architecture_interrupts`, `architecture_sync`, `architecture_io`

**Smart Pins:**
- `smart_pins_digital`, `smart_pins_serial`, `smart_pins_pwm`
- `smart_pins_counting`, `smart_pins_timing`, `smart_pins_frequency`
- `smart_pins_analog`, `smart_pins_special`, `smart_pins_beginner`

**Spin2:**
- `spin2_control_flow`, `spin2_pin_control`, `spin2_timing`
- `spin2_cog_control`, `spin2_memory`, `spin2_math`
- `spin2_strings`, `spin2_smart_pins`, `spin2_locks`

**Guides:**
- `guides_getting_started`

---

## 🔧 Cache Management

The script manages caching automatically. You shouldn't need to access cache files directly.

**Refresh everything (scripts, index, common files):**
```bash
~/.p2kb-cache/refresh-kb.sh
```

**Check what's cached:**
```bash
~/.p2kb-cache/fetch-kb-file.sh --cached
```

**Full reset (if needed):**
```bash
rm -rf ~/.p2kb-cache ~/.p2kb
```

---

## 📋 Troubleshooting

**"Key not found":**
- Use `--search <term>` to find valid keys
- Check `--browse <category>` for related keys
- Keys are case-sensitive and start with `p2kb`
- The error message will show similar keys

**Stale content:**
- Run `~/.p2kb-cache/refresh-kb.sh` to update everything
- Index auto-refreshes every 24 hours

**Network errors:**
- Check internet connectivity
- Verify GitHub is accessible

---

## 💡 Notes

- **Scripts location:** `~/.p2kb-cache/` (user-visible)
- **Index/cache location:** `~/.p2kb/` (hidden, managed automatically)
- **Index size:** ~130KB (13KB compressed)
- **Total content:** ~970 YAML files in 45 categories
- **Auto-refresh:** Index checks for updates every 24 hours

---

*Version 3.2 - Key-Based Access with Navigation*
*Last Updated: 2025-11-30*
