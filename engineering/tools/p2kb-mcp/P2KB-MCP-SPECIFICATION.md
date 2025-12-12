# P2KB MCP Server Specification

*Model Context Protocol server for P2 Knowledge Base access*

**Version**: 1.0.0
**Target**: Remote Claude AI instances
**Language**: Go
**Author**: P2 Knowledge Base Project

---

## Overview

The P2KB MCP replaces the current fetch script system (`fetch-kb-file.sh` / `fetch-kb-file.ps1`) with a native MCP server. This provides Claude AI instances with structured, efficient access to the P2 Knowledge Base without requiring shell script execution.

### Current System (Being Replaced)

```
User Machine                          GitHub
┌─────────────────┐                   ┌─────────────────┐
│ fetch-kb-file.sh│ ──HTTP GET──────► │ p2kb-index.json │
│                 │ ◄───────────────  │ .gz (13KB)      │
│                 │                   │                 │
│                 │ ──HTTP GET──────► │ individual      │
│                 │ ◄───────────────  │ .yaml files     │
│ ~/.p2kb/cache/  │                   │                 │
└─────────────────┘                   └─────────────────┘
```

### New System (MCP)

```
Claude Instance                       P2KB MCP Server              GitHub
┌─────────────┐                       ┌─────────────────┐          ┌──────────┐
│             │ ──MCP tool call─────► │ Cache Manager   │ ──HTTP─► │ Index    │
│   Claude    │ ◄──structured data──  │ Index Manager   │ ◄──────  │ YAMLs    │
│             │                       │ Content Filter  │          │          │
└─────────────┘                       └─────────────────┘          └──────────┘
```

---

## Data Sources

All data fetched from GitHub raw URLs:

| Resource | URL | Purpose |
|----------|-----|---------|
| Index | `https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/ai/p2kb-index.json.gz` | Key→path mapping, categories, mtimes |
| YAMLs | `https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/ai/P2/{path}` | Actual content |
| Root Manifest | `https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/manifests/propeller-knowledge-root.yaml` | Version/hash checking |
| AI Instructions | `https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/manifests/ai-instructions.yaml` | Common keys list |

---

## Index Structure

The index (`p2kb-index.json`) has this structure:

```json
{
  "system": {
    "version": "3.2.0",
    "generated": "2025-12-12T09:49:58.396586",
    "total_entries": 970,
    "total_categories": 47
  },
  "categories": {
    "pasm2_branch": ["p2kbPasm2Call", "p2kbPasm2Jmp", ...],
    "pasm2_math": ["p2kbPasm2Add", "p2kbPasm2Sub", ...],
    ...
  },
  "files": {
    "p2kbPasm2Mov": {
      "path": "deliverables/ai/P2/pasm2/instructions/mov.yaml",
      "mtime": 1764449566
    },
    ...
  }
}
```

---

## Content Filtering

**CRITICAL**: All YAML content MUST be filtered before caching/returning. Remove these metadata lines (saves tokens, removes internal tracking data):

```
last_updated:
enhancement_source:
documentation_source:
documentation_level:
manual_extraction_date:
```

Filter regex pattern:
```
^\s*(last_updated|enhancement_source|documentation_source|documentation_level|manual_extraction_date):
```

---

## MCP Tool API

### Documentation Requirement

**CRITICAL**: Every tool MUST have comprehensive documentation in its MCP schema definition. Claude relies entirely on tool descriptions to understand how to use them correctly.

Each tool registration MUST include:
1. **Clear description** - What the tool does in plain language
2. **Parameter descriptions** - Every parameter explained with examples
3. **Return format** - What Claude should expect back
4. **Error cases** - What errors can occur and what they mean

Example of proper tool documentation in Go:

```go
s.AddTool(mcp.Tool{
    Name:        "p2kb_get",
    Description: "Fetch P2 Knowledge Base content by key. Returns YAML documentation for P2 instructions, architecture, smart pins, and Spin2 methods. Use p2kb_search or p2kb_browse to discover valid keys.",
    InputSchema: mcp.ToolInputSchema{
        Type: "object",
        Properties: map[string]interface{}{
            "key": map[string]interface{}{
                "type":        "string",
                "description": "The p2kb key to fetch. Examples: 'p2kbPasm2Mov' (MOV instruction), 'p2kbArchCog' (COG architecture), 'p2kbSpin2Pinwrite' (Spin2 pinwrite method). Use p2kb_search('mov') to find keys.",
            },
        },
        Required: []string{"key"},
    },
}, handleGet)
```

**Poor documentation = Claude cannot use the tool effectively.**

---

### Core Tools (Script Parity)

#### `p2kb_get`

Fetch content by key. Primary access method.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `key` | string | Yes | The p2kb key (e.g., `p2kbPasm2Mov`) |

**Returns:**
```json
{
  "content": "--- YAML content here ---"
}
```

**Errors:**
- Key not found → return similar keys as suggestions
- Network error → return cached if available, else error

---

#### `p2kb_search`

Search for keys matching a term (case-insensitive).

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `term` | string | Yes | Search term |
| `limit` | integer | No | Max results (default: 50) |

**Returns:**
```json
{
  "keys": ["p2kbPasm2Mov", "p2kbPasm2Movbyts", ...],
  "count": 5,
  "term": "mov"
}
```

---

#### `p2kb_browse`

List all keys in a category.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category` | string | Yes | Category name (e.g., `pasm2_branch`) |

**Returns:**
```json
{
  "category": "pasm2_branch",
  "keys": ["p2kbPasm2Call", "p2kbPasm2Jmp", ...],
  "count": 37
}
```

**Errors:**
- Category not found → return list of valid categories

---

#### `p2kb_categories`

List all available categories with counts.

**Parameters:** None

**Returns:**
```json
{
  "categories": {
    "pasm2_branch": 37,
    "pasm2_math": 45,
    "architecture_core": 8,
    ...
  },
  "total_categories": 47,
  "total_entries": 970
}
```

---

#### `p2kb_version`

Get MCP server version.

**Parameters:** None

**Returns:**
```json
{
  "mcp_version": "1.0.0"
}
```

---

### Enhanced Tools (New Capabilities)

#### `p2kb_batch_get`

Fetch multiple keys in one call. Efficient for related lookups.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `keys` | string[] | Yes | Array of keys to fetch |

**Returns:**
```json
{
  "results": {
    "p2kbPasm2Mov": { "content": "..." },
    "p2kbPasm2Add": { "content": "..." },
    "p2kbPasm2Invalid": { "error": "Key not found" }
  },
  "success": 2,
  "errors": 1
}
```

---

#### `p2kb_refresh`

Force refresh of index and optionally invalidate cache.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `invalidate_cache` | boolean | No | Clear all cached YAMLs (default: false) |
| `prefetch_common` | boolean | No | Prefetch common keys after refresh (default: true) |

**Returns:**
```json
{
  "refreshed": true,
  "version": "3.2.1",
  "total_entries": 970
}
```

**Behavior (internal):**
1. Fetch new index (ignore TTL)
2. Compare `mtime` values with cached files
3. Invalidate cache entries where remote mtime > local mtime
4. If `prefetch_common`, fetch the 3 guide keys

---

#### `p2kb_info`

Check if a key exists and what categories it belongs to (without fetching content).

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `key` | string | Yes | The p2kb key |

**Returns:**
```json
{
  "key": "p2kbPasm2Mov",
  "exists": true,
  "categories": ["pasm2_math"]
}
```

---

#### `p2kb_stats`

Knowledge base statistics (useful for understanding scope).

**Parameters:** None

**Returns:**
```json
{
  "version": "3.2.0",
  "total_entries": 970,
  "total_categories": 47
}
```

---

#### `p2kb_related`

Get related instructions for a key (parses `related_instructions` from YAML).

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `key` | string | Yes | The p2kb key |
| `fetch_content` | boolean | No | Also fetch related content (default: false) |

**Returns:**
```json
{
  "key": "p2kbPasm2Mov",
  "related": ["p2kbPasm2Loc", "p2kbPasm2Rdlong", "p2kbPasm2Wrlong"],
  "content": {
    "p2kbPasm2Loc": "...",
    ...
  }
}
```

---

#### `p2kb_help`

Return usage information.

**Parameters:** None

**Returns:**
```json
{
  "tools": ["p2kb_get", "p2kb_search", "p2kb_browse", "p2kb_categories", "p2kb_version", "p2kb_batch_get", "p2kb_refresh", "p2kb_info", "p2kb_stats", "p2kb_related", "p2kb_help"],
  "key_prefixes": {
    "p2kbPasm2*": "PASM2 assembly instructions",
    "p2kbSpin2*": "Spin2 methods",
    "p2kbArch*": "Architecture documentation",
    "p2kbGuide*": "Guides and quick references",
    "p2kbHw*": "Hardware specifications"
  }
}
```

---

## Cache Management

### Directory Structure

```
~/.p2kb-mcp/
├── index/
│   ├── p2kb-index.json          # Decompressed index
│   └── p2kb-index.meta          # Index metadata (fetch time, etag)
├── cache/
│   ├── p2kbPasm2Mov.yaml        # Cached, filtered YAMLs
│   ├── p2kbPasm2Add.yaml
│   └── ...
├── refs/
│   ├── propeller-knowledge-root.yaml
│   └── ai-instructions.yaml
└── mcp.log                      # Optional debug log
```

### Index Refresh Logic

```
INDEX_TTL = 24 hours (86400 seconds)

on any tool call:
  if index not exists OR index age > INDEX_TTL:
    fetch_index()
    invalidate_stale_cache()
```

### Cache Invalidation on Index Update

```python
def invalidate_stale_cache(old_index, new_index):
    for key, new_entry in new_index.files.items():
        if key in cache:
            old_entry = old_index.files.get(key)
            if old_entry is None or new_entry.mtime > old_entry.mtime:
                delete_from_cache(key)
```

### Prefetch Keys

On refresh, prefetch these common keys:
- `p2kbGuideQuickQueries`
- `p2kbGuideSpin2GettingStarted`
- `p2kbGuidePasm2GettingStarted`

---

## Error Handling

### Key Not Found

When a key lookup fails, provide helpful suggestions:

```json
{
  "error": "Key 'p2kbPasm2Mvo' not found",
  "suggestions": ["p2kbPasm2Mov", "p2kbPasm2Movbyts"],
  "hint": "Use p2kb_search('mov') to find keys"
}
```

Suggestion algorithm: Find keys containing a substring of the requested key.

### Network Errors

1. If cached content exists → return cached with `stale: true` flag
2. If no cache → return error with retry suggestion

### Index Corruption

If index fails to parse:
1. Delete corrupted index
2. Re-fetch
3. If still fails → return error suggesting manual intervention

---

## Dev Container Specification

### Dockerfile

```dockerfile
FROM mcr.microsoft.com/devcontainers/go:1.22

# Install Node.js for Claude Code
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

# Install common tools
RUN apt-get update && apt-get install -y \
    jq \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Go tools for MCP development
RUN go install golang.org/x/tools/gopls@latest \
    && go install github.com/go-delve/delve/cmd/dlv@latest

WORKDIR /workspace
```

### devcontainer.json

```json
{
  "name": "P2KB MCP Development",
  "build": {
    "dockerfile": "Dockerfile"
  },
  "features": {
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "golang.go",
        "ms-vscode.vscode-typescript-next",
        "esbenp.prettier-vscode"
      ],
      "settings": {
        "go.useLanguageServer": true,
        "go.lintTool": "golangci-lint"
      }
    }
  },
  "postCreateCommand": "go mod download && npm install -g @anthropic-ai/claude-code",
  "remoteUser": "vscode",
  "mounts": [
    "source=${localEnv:HOME}/.p2kb-mcp,target=/home/vscode/.p2kb-mcp,type=bind,consistency=cached"
  ]
}
```

---

## Go Implementation Guidance

### Project Structure

```
p2kb-mcp/
├── cmd/
│   └── p2kb-mcp/
│       └── main.go              # MCP server entry point
├── internal/
│   ├── cache/
│   │   ├── cache.go             # Cache manager
│   │   └── cache_test.go
│   ├── index/
│   │   ├── index.go             # Index manager
│   │   └── index_test.go
│   ├── filter/
│   │   ├── filter.go            # Content filtering
│   │   └── filter_test.go
│   ├── fetch/
│   │   ├── fetch.go             # HTTP fetching
│   │   └── fetch_test.go
│   └── tools/
│       ├── get.go               # p2kb_get implementation
│       ├── search.go            # p2kb_search implementation
│       ├── browse.go            # p2kb_browse implementation
│       └── ...
├── pkg/
│   └── mcp/
│       └── server.go            # MCP protocol handling
├── go.mod
├── go.sum
├── Makefile
└── README.md
```

### Key Dependencies

```go
// go.mod
module github.com/ironsheep/p2kb-mcp

go 1.22

require (
    github.com/mark3labs/mcp-go v0.x.x  // MCP SDK for Go
    gopkg.in/yaml.v3 v3.0.1             // YAML parsing
)
```

### Filter Implementation

```go
package filter

import (
    "regexp"
    "strings"
)

var metadataPattern = regexp.MustCompile(
    `(?m)^\s*(last_updated|enhancement_source|documentation_source|documentation_level|manual_extraction_date):.*\n?`)

func FilterMetadata(content string) string {
    return metadataPattern.ReplaceAllString(content, "")
}
```

### MCP Tool Registration Example

```go
package main

import (
    "github.com/mark3labs/mcp-go/mcp"
    "github.com/mark3labs/mcp-go/server"
)

func main() {
    s := server.NewMCPServer("p2kb-mcp", "1.0.0")

    // Register tools
    s.AddTool(mcp.Tool{
        Name:        "p2kb_get",
        Description: "Fetch P2KB content by key",
        InputSchema: mcp.ToolInputSchema{
            Type: "object",
            Properties: map[string]interface{}{
                "key": map[string]string{
                    "type":        "string",
                    "description": "The p2kb key (e.g., p2kbPasm2Mov)",
                },
            },
            Required: []string{"key"},
        },
    }, handleGet)

    // ... register other tools

    s.ServeStdio()
}
```

---

## Testing Strategy

### Requirements

1. **Full test suite** with coverage reporting
2. **Coverage target**: 80% minimum
3. **CI integration**: Tests run on every PR
4. **Two modes**: Live GitHub testing and local fixture testing

### Test Modes

#### Mode 1: Live GitHub Testing (Default)

Tests interact directly with the real P2KB on GitHub. Use this for:
- Integration tests
- End-to-end verification
- Ensuring compatibility with actual data

```go
func TestLiveGitHubFetch(t *testing.T) {
    if testing.Short() {
        t.Skip("Skipping live GitHub test in short mode")
    }
    // Test against real GitHub
    client := NewClient(LiveConfig())
    result, err := client.Get("p2kbPasm2Mov")
    require.NoError(t, err)
    require.Contains(t, result.Content, "mnemonic:")
}
```

Run live tests:
```bash
go test ./... -v
```

#### Mode 2: Local Fixture Testing (Fast/Offline)

Use embedded test fixtures for:
- Unit tests
- Fast CI runs
- Offline development
- Edge case testing

```
internal/testdata/
├── fixtures/
│   ├── p2kb-index.json           # Minimal test index (10-20 entries)
│   ├── p2kbPasm2Mov.yaml         # Sample instruction
│   ├── p2kbPasm2Add.yaml         # Sample instruction
│   ├── p2kbArchCog.yaml          # Sample architecture
│   ├── p2kbGuideQuickQueries.yaml # Sample guide
│   └── malformed.yaml            # For error testing
└── fixtures.go                   # Embed directive
```

```go
//go:embed fixtures/*
var testFixtures embed.FS

func TestWithFixtures(t *testing.T) {
    client := NewClient(FixtureConfig(testFixtures))
    result, err := client.Get("p2kbPasm2Mov")
    require.NoError(t, err)
}
```

Run fast tests only:
```bash
go test ./... -short
```

### Test Categories

#### Unit Tests

| Component | Tests |
|-----------|-------|
| `filter` | Metadata removal, edge cases (empty, no metadata, nested) |
| `index` | JSON parsing, malformed handling, category lookup, key lookup |
| `cache` | TTL expiration, invalidation logic, file operations |
| `search` | Case-insensitive, partial match, no results, special chars |

#### Integration Tests

| Scenario | Description |
|----------|-------------|
| Full fetch cycle | Index → lookup → HTTP fetch → filter → cache → return |
| Cache hit | Verify cached content returned without HTTP |
| Cache invalidation | New index with updated mtime invalidates cache |
| Batch operations | Multiple keys, mixed success/failure |
| Error recovery | Network timeout, 404, corrupted cache |

#### MCP Protocol Tests

| Test | Description |
|------|-------------|
| Tool registration | All 11 tools registered with schemas |
| Schema validation | Invalid inputs rejected with clear errors |
| Response format | Responses match documented schemas |
| Error responses | Errors include helpful messages |

### Coverage Reporting

```bash
# Generate coverage report
go test ./... -coverprofile=coverage.out

# View coverage summary
go tool cover -func=coverage.out

# Generate HTML report
go tool cover -html=coverage.out -o coverage.html

# Fail if coverage below threshold
go test ./... -coverprofile=coverage.out && \
  go tool cover -func=coverage.out | grep total | awk '{print $3}' | \
  sed 's/%//' | awk '{if ($1 < 80) exit 1}'
```

### Makefile Targets

```makefile
.PHONY: test test-short test-live test-coverage

test: ## Run all tests
	go test ./... -v

test-short: ## Run fast tests only (no GitHub)
	go test ./... -short -v

test-live: ## Run live GitHub integration tests
	go test ./... -v -run "Live"

test-coverage: ## Run tests with coverage report
	go test ./... -coverprofile=coverage.out
	go tool cover -func=coverage.out
	@echo "Coverage report: coverage.html"
	go tool cover -html=coverage.out -o coverage.html

test-ci: ## CI test run with coverage threshold
	go test ./... -coverprofile=coverage.out -covermode=atomic
	@COVERAGE=$$(go tool cover -func=coverage.out | grep total | awk '{print $$3}' | sed 's/%//'); \
	echo "Coverage: $$COVERAGE%"; \
	if [ $$(echo "$$COVERAGE < 80" | bc) -eq 1 ]; then \
		echo "Coverage below 80% threshold"; exit 1; \
	fi
```

### GitHub Actions CI

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'

      - name: Run tests with coverage
        run: make test-ci

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          files: coverage.out
```

### Test Fixtures Content

The test fixtures should include representative samples:

**p2kb-index.json** (minimal):
```json
{
  "system": {
    "version": "test-1.0.0",
    "total_entries": 5,
    "total_categories": 2
  },
  "categories": {
    "pasm2_math": ["p2kbPasm2Mov", "p2kbPasm2Add"],
    "architecture_core": ["p2kbArchCog"]
  },
  "files": {
    "p2kbPasm2Mov": {"path": "pasm2/mov.yaml", "mtime": 1700000000},
    "p2kbPasm2Add": {"path": "pasm2/add.yaml", "mtime": 1700000000},
    "p2kbArchCog": {"path": "arch/cog.yaml", "mtime": 1700000000}
  }
}
```

**p2kbPasm2Mov.yaml** (sample with metadata to filter):
```yaml
mnemonic: MOV
category: Data Movement
last_updated: "2025-01-01"
documentation_source: "test"
syntax:
  - "MOV D,S"
description: |
  Copy source to destination.
related_instructions:
  - p2kbPasm2Add
  - p2kbPasm2Loc
```

### Manual Testing with Claude Code

After automated tests pass:

```bash
# In dev container, start MCP server
./p2kb-mcp

# In another terminal, connect Claude Code
claude --mcp-config mcp-config.json

# Test in Claude conversation:
> What version is the P2KB MCP?
> Search for MOV instruction
> Get the MOV instruction documentation
> What categories are available?
> Get all branch instructions
```

---

## Build Targets

### Supported Platforms

The MCP builds for 6 platform combinations:

| OS | Architecture | Binary Name |
|----|--------------|-------------|
| Linux | x86_64 | `p2kb-mcp-linux-amd64` |
| Linux | ARM64 | `p2kb-mcp-linux-arm64` |
| macOS | x86_64 | `p2kb-mcp-darwin-amd64` |
| macOS | ARM64 (Apple Silicon) | `p2kb-mcp-darwin-arm64` |
| Windows | x86_64 | `p2kb-mcp-windows-amd64.exe` |
| Windows | ARM64 | `p2kb-mcp-windows-arm64.exe` |

### Distribution Format

The MCP is distributed as a **Container Tools package** containing:
- All 6 platform binaries
- A routing script that detects the OS/architecture and invokes the correct binary

The Container Tools distribution specification is defined in the target repository. This document does not duplicate that specification.

### Build Commands

```makefile
.PHONY: build-all

PLATFORMS := linux/amd64 linux/arm64 darwin/amd64 darwin/arm64 windows/amd64 windows/arm64

build-all: ## Build for all platforms
	@for platform in $(PLATFORMS); do \
		OS=$${platform%/*}; \
		ARCH=$${platform#*/}; \
		EXT=""; [ "$$OS" = "windows" ] && EXT=".exe"; \
		echo "Building $$OS/$$ARCH..."; \
		GOOS=$$OS GOARCH=$$ARCH go build -o dist/p2kb-mcp-$$OS-$$ARCH$$EXT ./cmd/p2kb-mcp; \
	done
```

---

## Configuration

Environment variables (optional):

| Variable | Default | Description |
|----------|---------|-------------|
| `P2KB_CACHE_DIR` | `~/.p2kb-mcp` | Cache directory location |
| `P2KB_INDEX_TTL` | `86400` | Index TTL in seconds |
| `P2KB_BASE_URL` | GitHub raw URL | Override for testing |
| `P2KB_LOG_LEVEL` | `info` | Logging verbosity |

---

## Migration Path

For users currently using fetch scripts:

1. Install P2KB MCP server
2. Configure Claude Code to use MCP
3. Existing cache at `~/.p2kb/cache/` can be migrated to `~/.p2kb-mcp/cache/`
4. Remove old scripts from `~/.p2kb-cache/`

The MCP provides the same functionality with better integration.

---

## GitHub Repository Setup

### Issue Templates

Create `.github/ISSUE_TEMPLATE/` with:

**feature_request.md:**
```markdown
---
name: Feature Request
about: Suggest a new feature for P2KB MCP
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

## Summary
<!-- Brief description of the feature -->

## Use Case
<!-- Why is this feature needed? What problem does it solve? -->

## Proposed Solution
<!-- How should this feature work? -->

## Alternatives Considered
<!-- Any alternative approaches you've considered -->

## Additional Context
<!-- Screenshots, examples, or other relevant information -->
```

**bug_report.md:**
```markdown
---
name: Bug Report
about: Report a defect in P2KB MCP
title: '[BUG] '
labels: bug
assignees: ''
---

## Description
<!-- Clear description of the bug -->

## Steps to Reproduce
1.
2.
3.

## Expected Behavior
<!-- What should happen -->

## Actual Behavior
<!-- What actually happens -->

## Environment
- OS: [e.g., macOS 14.0, Windows 11, Ubuntu 22.04]
- Architecture: [e.g., x86_64, ARM64]
- MCP Version: [e.g., 1.0.0]
- Claude Code Version: [if applicable]

## Logs/Error Messages
```
<!-- Paste any error messages or logs here -->
```

## Additional Context
<!-- Screenshots or other relevant information -->
```

**config.yml:**
```yaml
blank_issues_enabled: false
contact_links:
  - name: P2 Knowledge Base Documentation
    url: https://github.com/ironsheep/P2-Knowledge-Base
    about: Main P2KB repository and documentation
```

---

### Funding Configuration

**.github/FUNDING.yml:**
```yaml
# Funding platforms
github: [ironsheep]
# patreon:
# ko_fi:
# custom: ['https://example.com/donate']
```

---

### GitHub Actions Workflows

#### Build Workflow

**.github/workflows/build.yml:**
```yaml
name: Build

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        goos: [linux, darwin, windows]
        goarch: [amd64, arm64]

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'

      - name: Build
        env:
          GOOS: ${{ matrix.goos }}
          GOARCH: ${{ matrix.goarch }}
        run: |
          EXT=""
          [ "$GOOS" = "windows" ] && EXT=".exe"
          go build -ldflags="-s -w -X main.Version=${{ github.sha }}" \
            -o dist/p2kb-mcp-${{ matrix.goos }}-${{ matrix.goarch }}${EXT} \
            ./cmd/p2kb-mcp

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: p2kb-mcp-${{ matrix.goos }}-${{ matrix.goarch }}
          path: dist/
```

#### Test Workflow

**.github/workflows/test.yml:**
```yaml
name: Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'

      - name: Run tests with coverage
        run: |
          go test ./... -coverprofile=coverage.out -covermode=atomic

      - name: Check coverage threshold
        run: |
          COVERAGE=$(go tool cover -func=coverage.out | grep total | awk '{print $3}' | sed 's/%//')
          echo "Coverage: ${COVERAGE}%"
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "Coverage below 80% threshold"
            exit 1
          fi

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          files: coverage.out
          fail_ci_if_error: true
```

#### Release Workflow

**.github/workflows/release.yml:**
```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write

jobs:
  build-all:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        include:
          - goos: linux
            goarch: amd64
          - goos: linux
            goarch: arm64
          - goos: darwin
            goarch: amd64
          - goos: darwin
            goarch: arm64
          - goos: windows
            goarch: amd64
          - goos: windows
            goarch: arm64

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'

      - name: Build
        env:
          GOOS: ${{ matrix.goos }}
          GOARCH: ${{ matrix.goarch }}
        run: |
          VERSION=${GITHUB_REF#refs/tags/}
          EXT=""
          [ "$GOOS" = "windows" ] && EXT=".exe"
          go build -ldflags="-s -w -X main.Version=${VERSION}" \
            -o p2kb-mcp-${{ matrix.goos }}-${{ matrix.goarch }}${EXT} \
            ./cmd/p2kb-mcp

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: p2kb-mcp-${{ matrix.goos }}-${{ matrix.goarch }}
          path: p2kb-mcp-*

  sign-macos:
    needs: build-all
    runs-on: macos-latest
    strategy:
      matrix:
        goarch: [amd64, arm64]

    steps:
      - uses: actions/checkout@v4

      - name: Download macOS binary
        uses: actions/download-artifact@v4
        with:
          name: p2kb-mcp-darwin-${{ matrix.goarch }}

      - name: Import Code Signing Certificate
        env:
          MACOS_CERTIFICATE: ${{ secrets.MACOS_CERTIFICATE }}
          MACOS_CERTIFICATE_PWD: ${{ secrets.MACOS_CERTIFICATE_PWD }}
          KEYCHAIN_PASSWORD: ${{ secrets.KEYCHAIN_PASSWORD }}
        run: |
          # Create temporary keychain
          KEYCHAIN_PATH=$RUNNER_TEMP/signing.keychain-db
          security create-keychain -p "$KEYCHAIN_PASSWORD" $KEYCHAIN_PATH
          security set-keychain-settings -lut 21600 $KEYCHAIN_PATH
          security unlock-keychain -p "$KEYCHAIN_PASSWORD" $KEYCHAIN_PATH

          # Import certificate
          echo "$MACOS_CERTIFICATE" | base64 --decode > certificate.p12
          security import certificate.p12 -P "$MACOS_CERTIFICATE_PWD" \
            -A -t cert -f pkcs12 -k $KEYCHAIN_PATH
          security list-keychain -d user -s $KEYCHAIN_PATH

      - name: Sign Binary
        env:
          APPLE_TEAM_ID: ${{ secrets.APPLE_TEAM_ID }}
        run: |
          codesign --force --options runtime \
            --sign "Developer ID Application: $APPLE_TEAM_ID" \
            --timestamp \
            p2kb-mcp-darwin-${{ matrix.goarch }}

      - name: Notarize Binary
        env:
          APPLE_ID: ${{ secrets.APPLE_ID }}
          APPLE_ID_PASSWORD: ${{ secrets.APPLE_ID_PASSWORD }}
          APPLE_TEAM_ID: ${{ secrets.APPLE_TEAM_ID }}
        run: |
          # Create ZIP for notarization
          zip p2kb-mcp-darwin-${{ matrix.goarch }}.zip \
            p2kb-mcp-darwin-${{ matrix.goarch }}

          # Submit for notarization
          xcrun notarytool submit p2kb-mcp-darwin-${{ matrix.goarch }}.zip \
            --apple-id "$APPLE_ID" \
            --password "$APPLE_ID_PASSWORD" \
            --team-id "$APPLE_TEAM_ID" \
            --wait

      - name: Upload signed artifact
        uses: actions/upload-artifact@v4
        with:
          name: p2kb-mcp-darwin-${{ matrix.goarch }}-signed
          path: p2kb-mcp-darwin-${{ matrix.goarch }}

  create-release:
    needs: [build-all, sign-macos]
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Download all artifacts
        uses: actions/download-artifact@v4
        with:
          path: artifacts

      - name: Prepare release assets
        run: |
          mkdir -p release
          # Linux and Windows (unsigned)
          cp artifacts/p2kb-mcp-linux-amd64/* release/
          cp artifacts/p2kb-mcp-linux-arm64/* release/
          cp artifacts/p2kb-mcp-windows-amd64/* release/
          cp artifacts/p2kb-mcp-windows-arm64/* release/
          # macOS (signed)
          cp artifacts/p2kb-mcp-darwin-amd64-signed/* release/
          cp artifacts/p2kb-mcp-darwin-arm64-signed/* release/

          # Create checksums
          cd release
          sha256sum * > SHA256SUMS.txt

      - name: Create Container Tools package
        run: |
          mkdir -p package/bin
          cp release/p2kb-mcp-* package/bin/
          cp scripts/p2kb-mcp-router.sh package/p2kb-mcp
          cp scripts/p2kb-mcp-router.ps1 package/p2kb-mcp.ps1
          chmod +x package/p2kb-mcp
          tar -czvf p2kb-mcp-container-tools.tar.gz -C package .

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            release/*
            p2kb-mcp-container-tools.tar.gz
          generate_release_notes: true
          draft: false
          prerelease: ${{ contains(github.ref, '-rc') || contains(github.ref, '-beta') }}
```

---

### Required GitHub Secrets

For the release workflow to function, configure these repository secrets:

| Secret | Description |
|--------|-------------|
| `MACOS_CERTIFICATE` | Base64-encoded .p12 certificate file |
| `MACOS_CERTIFICATE_PWD` | Password for the .p12 certificate |
| `KEYCHAIN_PASSWORD` | Temporary keychain password (any secure value) |
| `APPLE_ID` | Apple ID email for notarization |
| `APPLE_ID_PASSWORD` | App-specific password for Apple ID |
| `APPLE_TEAM_ID` | Apple Developer Team ID |

---

## Future Enhancements

- [ ] Full-text search across cached content
- [ ] Encoding pattern lookup (find instruction by binary encoding)
- [ ] Offline mode with complete cache download
- [ ] Webhook for push-based index updates
- [ ] Metrics/telemetry for usage patterns

---

*Specification created: 2025-12-12*
*Based on fetch-kb-file.sh v3.2*
