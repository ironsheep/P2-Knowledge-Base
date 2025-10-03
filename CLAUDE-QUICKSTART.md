# P2 Knowledge Base QuickStart
*Simple setup for AI assistants*

## 🚀 Remote Instance Setup (Copy & Paste This)

**For Claude Code without local repository:**

```
P2 Knowledge Base Access:
https://github.com/ironsheep/P2-Knowledge-Base

You'll download files from GitHub as needed using curl/wget.
Cache them in .p2kb-cache/ in the current project directory.

Setup:
1. Verify curl or wget: which curl || which wget
2. Create cache: mkdir -p .p2kb-cache
3. Add to .gitignore: echo ".p2kb-cache/" >> .gitignore

Download function:
fetch_kb_file() {
  local path=$1
  local cache=".p2kb-cache/${path}"
  local url="https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/${path}"

  if [ -f "$cache" ]; then cat "$cache"
  else
    mkdir -p "$(dirname "$cache")"
    curl -o "$cache" "$url" 2>/dev/null || wget -O "$cache" "$url"
    cat "$cache"
  fi
}

Start with: fetch_kb_file "manifests/propeller-knowledge-root.yaml"
Then navigate manifests to find PASM2, Spin2, Smart Pins, OBEX content.
```

**That's it!** You're ready to help with P2 development.

---

## 📚 Quick Navigation

Once setup, users can ask:

**PASM2 Instructions:**
```
Help me with the ADD instruction
```
Navigate: `manifests/P2/language/pasm2-manifest.yaml`

**Smart Pins:**
```
Configure a Smart Pin for UART
```
Navigate: `manifests/P2/smart-pins-manifest.yaml`

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
