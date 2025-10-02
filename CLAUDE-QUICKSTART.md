# P2 Knowledge Base QuickStart
*Self-bootstrapping AI integration for P2 development*

## 🚀 Bootstrap Instructions (That's All You Need!)

Copy this minimal instruction to any AI assistant:

```
Access the P2 Knowledge Base:
  https://github.com/ironsheep/P2-Knowledge-Base

  1. Fetch: manifests/propeller-knowledge-root.yaml
  2. Fetch: manifests/ai-instructions.yaml (as directed by root)
  3. Find the content block between divider lines in ai-instructions.yaml (~150 lines starting with "# P2 Knowledge Base Integration")
  4. DELETE any existing "P2 Knowledge Base Integration" section from CLAUDE.md
  5. APPEND that complete block EXACTLY to CLAUDE.md (no summaries, no edits)
  6. Verify the sha256 hash line is included

  Use WebFetch with explicit instruction to return COMPLETE content without summarization:
  
  WebFetch(
    url: "https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/manifests/ai-instructions.yaml",
    prompt: "Return the COMPLETE raw YAML content without any summarization, truncation, or modification. I need every line exactly as-is."
  )

  Then use Edit/Write to update CLAUDE.md with the extracted content block.

The system will self-configure with:
- Navigation rules and category catalog
- Direct access to major P2 subsystems
- Auto-updating instructions (checks each session)
```

That's it! The knowledge base will teach the AI everything else it needs.

## 💡 What Happens Next

1. **AI fetches root manifest** - Gets instructions location and hash
2. **Checks for updates** - Compares stored hash with current
3. **Auto-configures** - Loads navigation rules and category shortcuts
4. **Ready to help** - Direct access to PASM2, Spin2, Smart Pins, etc.

## 📚 Common Starting Points (After Bootstrap)

### PASM2 Assembly
```
Help me with PASM2 [specific instruction or task]
```
AI starts at: `manifests/P2/language/pasm2-manifest.yaml`

### Smart Pin Configuration
```
Configure a Smart Pin for [UART/SPI/I2C/PWM/etc]
```
AI starts at: `manifests/P2/smart-pins-manifest.yaml`

### OBEX Community Code
```
Find P2 OBEX objects for [hardware/protocol]
```
AI starts at: `manifests/P2/community/obex-manifest.yaml`

### Hardware Testing
```
Test my P2 code on hardware
```
AI knows about: pnut_ts compiler, debug workflows, log monitoring

## ⚙️ Manual Update Request

If you want to ensure latest instructions:
```
Please update your P2 Knowledge Base instructions
```
AI will fetch and apply the latest version.

## 🔄 Version 2.0 Advantages

- **No more huge copy-paste blocks** - One tiny bootstrap
- **Auto-updating** - Instructions update themselves
- **Direct category access** - AI jumps straight to relevant sections
- **Self-documenting** - Knowledge base explains itself

## 📋 Session Management

**For best performance**: Clear conversation every 3-4 hours
- The AI's instructions will remind users about this
- Maintains peak responsiveness

## 🐛 Missing Content?

If AI reports "Content not found in P2 Knowledge Base":
1. AI will provide specific details about what's missing
2. Report to: https://github.com/ironsheep/P2-Knowledge-Base/issues
3. We'll add it to the knowledge base

---
*Version 2.0 - Self-Bootstrapping System*
*Last Updated: 2025-01-29*
