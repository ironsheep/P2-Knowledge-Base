# P2 Knowledge Base QuickStart
*Simple setup for AI assistants*

## 🚀 Setup (Copy & Paste This)

**For Claude Code instances:**

```
P2 Knowledge Base Setup - Two-Stage Bootstrap:

Stage 1: Fetch the ultra-minimal bootstrap (35 lines):
https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/manifests/ai-bootstrap-ultra-minimal.yaml

Verify you got:
- stage_1_unix section with bash script creation
- windows_users section pointing to separate file

Follow the instructions in stage_1_unix to create your fetch script.
Then use YOUR script to fetch the complete instructions.
```

### Platform-Specific Setup Instructions

**The AI assistant will:**

1. **Detect your platform** using `uname` or PowerShell checks

2. **For Unix/macOS/Linux**, create `.p2kb-cache/fetch-kb-file.sh`:
```bash
#!/bin/bash
# P2 Knowledge Base File Fetcher
path=$1
cache=".p2kb-cache/${path}"
url="https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/${path}"

if [ -f "$cache" ]; then
  cat "$cache"
else
  mkdir -p "$(dirname "$cache")"
  curl -sS -o "$cache" "$url" 2>/dev/null || wget -q -O "$cache" "$url"
  cat "$cache"
fi
```

3. **For Windows**, create `.p2kb-cache\fetch-kb-file.ps1`:
```powershell
# P2 Knowledge Base File Fetcher
param($path)
$cache = ".p2kb-cache\$($path -replace '/','\\')"  
$url = "https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/$path"

if (Test-Path $cache) {
  Get-Content $cache -Raw
} else {
  $dir = Split-Path $cache -Parent
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  Invoke-WebRequest -Uri $url -OutFile $cache
  Get-Content $cache -Raw
}
```

4. **Usage after setup**:
   - Unix/macOS: `bash .p2kb-cache/fetch-kb-file.sh "manifests/propeller-knowledge-root.yaml"`
   - Windows: `powershell -File .p2kb-cache\fetch-kb-file.ps1 "manifests/propeller-knowledge-root.yaml"`

5. **Start with**: Fetching the root manifest, then navigate to find PASM2, Spin2, Smart Pins, OBEX content.

**That's it!** You're ready to help with P2 development.

---

## 🎯 Essential First Documents

After setup, immediately load the Getting Started guides:

**For Spin2 Development:**
```
Fetch and read the Spin2 Getting Started guide:
bash .p2kb-cache/fetch-kb-file.sh "engineering/knowledge-base/P2/language/spin2/conventions/spin2-getting-started.yaml"

This contains core language essentials for Spin2 code generation.
```

**For PASM2 Development:**
```
Fetch and read the PASM2 Getting Started guide:
bash .p2kb-cache/fetch-kb-file.sh "engineering/knowledge-base/P2/language/pasm2/conventions/pasm2-getting-started.yaml"

This contains assembly mechanics and register model essentials.
```

## 📚 Quick Navigation

Once setup, users can ask:

**P2 Architecture:**
```
Explain P2 architecture
```
Navigate: `manifests/P2/architecture-manifest.yaml`

**PASM2 Instructions:**
```
Help me with the ADD instruction
```
Navigate: `manifests/P2/language/pasm2-manifest.yaml`

**Hardware Boards:**
```
What P2 development boards exist?
```
Navigate: `manifests/P2/hardware-manifest.yaml`

**OBEX Code:**
```
Find I2C driver objects
```
Navigate: `manifests/P2/community/obex-unified-index.yaml`

---

## 🔧 Cache Management

**Check size:** `du -sh .p2kb-cache`

**Clear cache:** `rm -rf .p2kb-cache`

**Refresh file:** `rm .p2kb-cache/manifests/propeller-knowledge-root.yaml`

---

## 💡 Notes

- **Cache location:** `.p2kb-cache/` in project root (hidden on macOS/Linux)
- **Per-project:** Each project has its own cache (~5-15MB)
- **Requirements:** curl (preferred) or wget
- **Future:** MCP server in development for shared cache and auto-updates

---

## 📋 Troubleshooting

**"Neither curl nor wget found":**
```bash
# macOS
brew install curl

# Linux
sudo apt-get install curl
```

**Permission errors:**
- Ensure you can write to project directory
- Check `.p2kb-cache/` permissions

**Corrupted cache:**
```bash
rm -rf .p2kb-cache
# Files will re-download
```

---

*Version 2.1 - Remote Access*
*Last Updated: 2025-10-02*
