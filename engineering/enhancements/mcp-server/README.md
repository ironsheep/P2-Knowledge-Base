# MCP Server for P2 Knowledge Base

*Advanced integration option for power users*

## Overview

This MCP (Model Context Protocol) server provides structured programmatic access to the P2 Knowledge Base. While the standard file-based approach works great for most users, the MCP server offers additional capabilities for those who want more structured interactions.

## When to Use This

Consider the MCP server if you:
- Need programmatic access to specific instructions without file navigation
- Want type-safe tool interfaces with defined parameters
- Prefer structured queries over file-based searching
- Are comfortable with Node.js configuration

For most users, the standard file-based approach described in [AI-INTEGRATION.md](/AI-INTEGRATION.md) is simpler and works immediately.

## Features

The MCP server exposes these tools:
- `lookupInstruction` - Find PASM2 instructions by mnemonic or category
- `querySmartPin` - Get Smart Pin mode details and configurations
- `searchPatterns` - Find code patterns and idioms
- `getArchitectureInfo` - Access P2 architecture specifications

## Installation

1. Navigate to this directory:
   ```bash
   cd engineering/enhancements/mcp-server
   npm install
   ```

2. Add to your Claude Code configuration (~/.config/claude/config.json):
   ```json
   {
     "mcpServers": {
       "p2kb": {
         "command": "node",
         "args": ["path/to/P2-Knowledge-Base/engineering/enhancements/mcp-server/index.js"],
         "name": "P2 Knowledge Base"
       }
     }
   }
   ```

3. Restart Claude Code to load the server

## Testing

Test the server locally:
```bash
npx @modelcontextprotocol/inspector node index.js
```

## See Also

- [MCP-SERVER-SETUP.md](MCP-SERVER-SETUP.md) - Detailed setup and usage guide
- [AI-INTEGRATION.md](/AI-INTEGRATION.md) - Standard file-based approach (recommended for most users)

---
*This is an optional enhancement. The standard file-based approach works great for most use cases.*