# P2 Knowledge Base - AI Bootstrap

**Repository:** https://github.com/ironsheep/P2-Knowledge-Base
**Version:** 3.2

---

## Unix / Linux / macOS

Run this single command to set up everything:

```bash
mkdir -p ~/.p2kb-cache && \
curl -sS https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/engineering/tools/p2kb/refresh-kb.sh > ~/.p2kb-cache/refresh-kb.sh && \
chmod +x ~/.p2kb-cache/refresh-kb.sh && \
~/.p2kb-cache/refresh-kb.sh
```

---

## Windows PowerShell

Run these commands:

```powershell
$d = "$env:USERPROFILE\.p2kb-cache"
New-Item -ItemType Directory -Force -Path $d | Out-Null
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/engineering/tools/p2kb/refresh-kb.ps1" -OutFile "$d\refresh-kb.ps1"
& "$d\refresh-kb.ps1"
```

---

## Verify Setup

```bash
~/.p2kb-cache/fetch-kb-file.sh --help
```

You should see available commands including `--search`, `--browse`, and `--categories`.

---

## Start Using

### Find Content

```bash
# Search for keys by keyword
~/.p2kb-cache/fetch-kb-file.sh --search uart
~/.p2kb-cache/fetch-kb-file.sh --search cordic

# Browse by category
~/.p2kb-cache/fetch-kb-file.sh --categories
~/.p2kb-cache/fetch-kb-file.sh --browse pasm2_branch

# See what's cached locally
~/.p2kb-cache/fetch-kb-file.sh --cached
```

### Fetch Content

```bash
# Fetch by key
~/.p2kb-cache/fetch-kb-file.sh p2kbPasm2Mov
~/.p2kb-cache/fetch-kb-file.sh p2kbArchCog
~/.p2kb-cache/fetch-kb-file.sh p2kbGuideQuickQueries
```

---

## Key Prefixes

| Prefix | Content Type |
|--------|--------------|
| `p2kbPasm2*` | PASM2 instructions |
| `p2kbSpin2*` | Spin2 methods/keywords |
| `p2kbArch*` | Architecture documentation |
| `p2kbSmartPin*` | Smart Pin modes |
| `p2kbGuide*` | Getting started guides |
| `p2kbHw*` | Hardware specifications |

---

## Update Everything

```bash
~/.p2kb-cache/refresh-kb.sh
```

---

## Next Steps

After bootstrap, see the comprehensive guide:
`deliverables/ai-reference/auxiliary-guides/interaction/using-with-ai.md`

---

*P2 Knowledge Base - Key-based access for AI assistants*
