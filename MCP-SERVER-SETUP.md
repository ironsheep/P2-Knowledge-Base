# MCP Server Setup for P2 Knowledge Base

## What is MCP?

MCP (Model Context Protocol) is a standardized way for AI assistants like Claude to interact with external data sources and tools. Instead of loading entire files into context, MCP servers provide structured query interfaces.

## Two Ways to Use P2 Knowledge Base

### Option 1: File-Based (Current Documentation)
- **Setup**: None required
- **How it works**: Claude reads files directly from the repository
- **Pros**: Simple, no dependencies, works immediately
- **Cons**: Uses more context, loads entire files
- **Best for**: Quick start, simple queries, no setup desired

### Option 2: MCP Server (This Guide)
- **Setup**: Install and configure MCP server
- **How it works**: Claude queries the server for specific information
- **Pros**: Efficient, structured queries, minimal context usage
- **Cons**: Requires Node.js, initial setup
- **Best for**: Heavy usage, complex queries, API-like access

## MCP Server Benefits

1. **Efficient Queries**: Only returns what you need
   ```
   // Instead of loading entire instruction file:
   p2_instruction("ADD")  // Returns just ADD instruction
   ```

2. **Smart Search**: Search across categories
   ```
   search_patterns("multi-cog")  // Finds all multi-COG patterns
   ```

3. **Structured Responses**: Consistent JSON format
4. **Less Context Usage**: Doesn't fill up conversation with file contents
5. **Dynamic**: Can update without reloading

## Installation

### Prerequisites
- Node.js 18+ installed
- npm or yarn package manager

### Method 1: NPX (No Installation)

Add to your Claude Desktop configuration:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "p2-knowledge": {
      "command": "npx",
      "args": ["-y", "@p2kb/mcp-server"],
      "env": {
        "P2KB_PATH": "/path/to/P2-Knowledge-Base"
      }
    }
  }
}
```

### Method 2: Local Installation

1. Navigate to the MCP server directory:
```bash
cd P2-Knowledge-Base/mcp-server
npm install
```

2. Add to Claude configuration:
```json
{
  "mcpServers": {
    "p2-knowledge": {
      "command": "node",
      "args": ["/path/to/P2-Knowledge-Base/mcp-server/index.js"],
      "env": {
        "P2KB_PATH": "/path/to/P2-Knowledge-Base"
      }
    }
  }
}
```

### Method 3: Global Installation

1. Install globally:
```bash
cd P2-Knowledge-Base/mcp-server
npm install -g .
```

2. Add to Claude configuration:
```json
{
  "mcpServers": {
    "p2-knowledge": {
      "command": "p2kb-mcp"
    }
  }
}
```

## Available MCP Tools

Once configured, Claude can use these tools:

### `p2_instruction`
Look up a specific PASM2 instruction
```
Parameters:
- mnemonic: Instruction name (e.g., "ADD", "MOV")
- category: Optional category filter

Example: p2_instruction("ADD", "math")
```

### `p2_instruction_list`
List all instructions in a category
```
Parameters:
- category: Category name (e.g., "math", "flow", "memory")

Example: p2_instruction_list("cordic")
```

### `smart_pin_mode`
Get Smart Pin configuration details
```
Parameters:
- mode: Mode as binary (00010), decimal (2), or name (sync_tx)

Example: smart_pin_mode("00010")
```

### `smart_pin_list`
List all available Smart Pin modes
```
Parameters: None

Returns: All 32 modes with descriptions
```

### `spin2_method`
Look up a Spin2 method
```
Parameters:
- method: Method name (e.g., "cogid", "waitms")

Example: spin2_method("coginit")
```

### `search_patterns`
Search for code patterns
```
Parameters:
- pattern: Pattern to search (e.g., "multi-cog", "pwm")

Example: search_patterns("mailbox")
```

## Usage Examples

### With MCP Server Configured

```
User: "What's the ADD instruction in P2?"
Claude: [Automatically uses p2_instruction("ADD")]
        "The ADD instruction adds source to destination..."

User: "List all CORDIC instructions"
Claude: [Uses p2_instruction_list("cordic")]
        "Here are the CORDIC instructions: QROTATE, QVECTOR..."

User: "Configure Smart Pin for UART TX"
Claude: [Uses smart_pin_mode("sync_tx")]
        "For UART TX, use mode %00010 (sync serial transmit)..."
```

### Comparison: File-Based vs MCP

#### File-Based Query:
```
User: "Look up the ADD instruction"
Claude: "Let me read the file at engineering/knowledge-base/P2/language/pasm2/math/add.yaml..."
[Loads entire file into context]
```

#### MCP Query:
```
User: "Look up the ADD instruction"
Claude: [Calls p2_instruction("ADD")]
[Gets just the ADD instruction data]
```

## Troubleshooting

### Server Not Found
- Check `P2KB_PATH` environment variable points to repository root
- Ensure Node.js is installed: `node --version`
- Verify path in Claude configuration

### Permission Denied
- Make index.js executable: `chmod +x mcp-server/index.js`
- Check file permissions

### No Response
- Restart Claude Desktop after configuration changes
- Check Claude logs for MCP errors
- Test server manually: `node mcp-server/index.js`

## Publishing to NPM (For Maintainers)

To make the server available via NPX:

1. Update package.json with npm scope
2. Login to npm: `npm login`
3. Publish: `npm publish --access public`

Users can then use:
```json
{
  "command": "npx",
  "args": ["-y", "@p2kb/mcp-server"]
}
```

## Advantages Over File-Based

| Feature | File-Based | MCP Server |
|---------|------------|------------|
| Setup Required | No | Yes |
| Context Usage | High | Low |
| Query Speed | Fast | Fast |
| Partial Data | No | Yes |
| Search Capability | Limited | Advanced |
| Memory Efficient | No | Yes |
| Works Offline | Yes | Yes |

## When to Use Each

### Use File-Based When:
- Getting started quickly
- Simple lookups
- No Node.js available
- Prefer simplicity

### Use MCP Server When:
- Heavy usage expected
- Complex queries needed
- Context limits matter
- Want API-like access
- Building automation

## Summary

The MCP server provides a more efficient, structured way to access the P2 Knowledge Base, but requires initial setup. The file-based approach works immediately but uses more context. Choose based on your needs and technical comfort level.

Both approaches access the same underlying YAML and markdown files - the MCP server just provides a smarter interface to them.