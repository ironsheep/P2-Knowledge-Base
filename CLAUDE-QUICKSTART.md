# P2 Knowledge Base QuickStart v3.2
*Key-based access with one-command setup*

## Overview

v3.2 uses **keys** to access content with built-in navigation.

- Keys like `p2kbPasm2Mov` map directly to YAML files
- Use `--search` and `--browse` to find keys - never guess!
- ~970 content files organized into 45 categories

---

## Setup

### Unix / Linux / macOS (One Command)

```bash
mkdir -p ~/.p2kb-cache && \
curl -sS https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/engineering/tools/p2kb/refresh-kb.sh > ~/.p2kb-cache/refresh-kb.sh && \
chmod +x ~/.p2kb-cache/refresh-kb.sh && \
~/.p2kb-cache/refresh-kb.sh
```

### Windows PowerShell

```powershell
$d = "$env:USERPROFILE\.p2kb-cache"
New-Item -ItemType Directory -Force -Path $d | Out-Null
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/engineering/tools/p2kb/refresh-kb.ps1" -OutFile "$d\refresh-kb.ps1"
& "$d\refresh-kb.ps1"
```

### Verify

```bash
~/.p2kb-cache/fetch-kb-file.sh --help
```

---

## IMPORTANT: Script-Only Access

**ALWAYS use the fetch script. NEVER access index or cache files directly.**

- ❌ DON'T: `jq ... ~/.p2kb/p2kb-index.json`
- ❌ DON'T: `cat ~/.p2kb/cache/...`
- ❌ DON'T: Guess at key names
- ✅ DO: Use `--search`, `--browse`, `--cached` commands

---

## Usage

### Find Keys

```bash
# Search for keys containing a term
~/.p2kb-cache/fetch-kb-file.sh --search uart
~/.p2kb-cache/fetch-kb-file.sh --search cordic

# Browse keys by category
~/.p2kb-cache/fetch-kb-file.sh --categories
~/.p2kb-cache/fetch-kb-file.sh --browse pasm2_branch

# See what's cached locally
~/.p2kb-cache/fetch-kb-file.sh --cached
```

### Fetch Content

```bash
~/.p2kb-cache/fetch-kb-file.sh p2kbPasm2Mov
~/.p2kb-cache/fetch-kb-file.sh p2kbArchCog
~/.p2kb-cache/fetch-kb-file.sh p2kbGuideQuickQueries
```

---

## Key Prefixes

| Prefix | Content Type | Example |
|--------|--------------|---------|
| `p2kbPasm2` | PASM2 instructions | `p2kbPasm2Mov` |
| `p2kbSpin2` | Spin2 methods | `p2kbSpin2Pinwrite` |
| `p2kbArch` | Architecture docs | `p2kbArchCog` |
| `p2kbSmartPin` | Smart Pin modes | `p2kbSmartPinAsyncSerialTransmit` |
| `p2kbGuide` | Guides | `p2kbGuideQuickQueries` |
| `p2kbHw` | Hardware specs | `p2kbHwP2Eval` |

---

## Categories (for --browse)

**PASM2 Instructions:**
`pasm2_directives`, `pasm2_branch`, `pasm2_cordic`, `pasm2_math`, `pasm2_pin`, `pasm2_event`, `pasm2_hub_control`, `pasm2_hub_fifo`, `pasm2_hub_ram`, `pasm2_interrupt`, `pasm2_lookup_table`, `pasm2_misc`, `pasm2_pixel`, `pasm2_register_indirection`, `pasm2_smart_pin`, `pasm2_streamer`

**Architecture:**
`architecture_core`, `architecture_math`, `architecture_timing`, `architecture_interrupts`, `architecture_sync`, `architecture_io`

**Smart Pins:**
`smart_pins_digital`, `smart_pins_serial`, `smart_pins_pwm`, `smart_pins_counting`, `smart_pins_timing`, `smart_pins_frequency`, `smart_pins_analog`, `smart_pins_special`

**Spin2:**
`spin2_control_flow`, `spin2_pin_control`, `spin2_timing`, `spin2_cog_control`, `spin2_memory`, `spin2_math`, `spin2_strings`, `spin2_smart_pins`, `spin2_locks`

---

## Cache Management

```bash
# Refresh everything (scripts, index, common files)
~/.p2kb-cache/refresh-kb.sh

# Check what's cached
~/.p2kb-cache/fetch-kb-file.sh --cached

# Full reset (if needed)
rm -rf ~/.p2kb-cache ~/.p2kb
```

---

## Troubleshooting

**"Key not found":**
- Use `--search <term>` to find valid keys
- Keys are case-sensitive and start with `p2kb`

**Stale content:**
- Run `~/.p2kb-cache/refresh-kb.sh` to update everything

---

## Notes

- **Scripts location:** `~/.p2kb-cache/` (user-visible)
- **Index/cache location:** `~/.p2kb/` (hidden, managed automatically)
- **Total content:** ~970 YAML files in 45 categories

---

*Version 3.2 - Key-Based Access with Navigation*
*Last Updated: 2025-12-14*
