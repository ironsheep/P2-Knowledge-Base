# P2 Knowledge Base - Getting Started

## For AI Assistants

### ⭐ With MCP (recommended)

If your agent supports the Model Context Protocol — Claude Code, Claude Desktop, ChatGPT with MCP support, and others — install the **[P2 Knowledge Base MCP](https://github.com/ironsheep/P2-Knowledge-Base-MCP)**. Your agent gets native tool calls for KB queries; no local cache to manage, always serves the latest published content.

**[→ MCP install instructions](https://github.com/ironsheep/P2-Knowledge-Base-MCP/blob/main/INSTALL.md)**

Once installed, just ask questions naturally:
```
"How does the P2 ADD instruction work?"
"Configure a Smart Pin for UART."
"Explain P2 COG architecture."
```

See **[AI-PROMPT-PATTERNS.md](AI-PROMPT-PATTERNS.md)** for more example queries.

### Without MCP (fetch-script path)

If your agent doesn't support MCP, use the fetch-script BOOTSTRAP:

```
https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/ai-reference/BOOTSTRAP.md
```

Fetch that file to get one-command setup for both Unix/macOS and Windows.

---

## What You Get

- **1000+ content files** covering PASM2, Spin2, architecture, smart pins, OBEX community code
- **Key-based access** (fetch-script) or **natural-language queries** (MCP)
- **Always-current published index** (MCP) or **local caching** (fetch-script)

---

## Quick Reference (fetch-script path)

```bash
.p2kb-cache/fetch-kb-file.sh --search uart     # Find keys
.p2kb-cache/fetch-kb-file.sh --categories      # Browse categories
.p2kb-cache/fetch-kb-file.sh p2kbPasm2Mov      # Fetch content
```

(MCP users don't need these — the agent calls `p2kb_find` / `p2kb_get` directly.)
