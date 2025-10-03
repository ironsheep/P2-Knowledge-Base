# P2 Knowledge Base MCP Server - Packaging & Delivery Guide

**Status:** Planning - Implementation Guide
**Created:** 2025-10-02
**Purpose:** Define packaging, build, and distribution process for P2KB MCP Server

---

## Distribution Model

**Strategy:** GitHub Release Assets (matches Todo MCP model)

### What Users Download

```
GitHub Releases → v1.4.0
├── p2-reference-v1.4.0.tar.gz     # Knowledge base content (existing)
├── p2kb-mcp-macos                  # MCP server binary (macOS)
├── p2kb-mcp-linux                  # MCP server binary (Linux)
└── p2kb-mcp-win.exe                # MCP server binary (Windows)
```

**User workflow:**
1. Download binary for their platform from releases
2. Place in local bin directory
3. Configure Claude Code to use binary
4. Done - no npm, no Node.js installation required

---

## Phase 1: Bundled Node.js Executables

**Technology:** Node.js + pkg (bundler)
**Timeline:** Week 1-2 (MVP)
**Binary Size:** ~50MB per platform

### What Gets Bundled

**Each executable contains:**
- Node.js runtime (v18)
- MCP server code (~200 lines)
- Dependencies:
  - `@modelcontextprotocol/sdk`
  - `yaml` parser
- All in single executable file

**Platforms:**
- `p2kb-mcp-macos` - macOS x64
- `p2kb-mcp-linux` - Linux x64
- `p2kb-mcp-win.exe` - Windows x64

### Build Process (Local)

**Prerequisites:**
```bash
# Install pkg globally
npm install -g pkg
```

**Build commands:**
```bash
cd engineering/mcp-server

# Install dependencies
npm install

# Build for all platforms
pkg package.json \
  --targets node18-macos-x64,node18-linux-x64,node18-win-x64 \
  --output dist/p2kb-mcp

# Produces:
# dist/p2kb-mcp-macos
# dist/p2kb-mcp-linux
# dist/p2kb-mcp-win.exe
```

**Test locally:**
```bash
# Test the binary
./dist/p2kb-mcp-macos

# Should output: "P2 Knowledge Base MCP server running"
```

### Package Configuration

**`engineering/mcp-server/package.json`:**
```json
{
  "name": "@p2kb/mcp-server",
  "version": "1.0.0",
  "description": "P2 Knowledge Base MCP Server - Minimal File Fetcher",
  "main": "src/server.js",
  "bin": {
    "p2kb-mcp": "src/server.js"
  },
  "scripts": {
    "start": "node src/server.js",
    "build": "pkg . --targets node18-macos-x64,node18-linux-x64,node18-win-x64 --output dist/p2kb-mcp"
  },
  "pkg": {
    "assets": [],
    "targets": [
      "node18-macos-x64",
      "node18-linux-x64",
      "node18-win-x64"
    ],
    "outputPath": "dist"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.5.0",
    "yaml": "^2.3.0"
  },
  "engines": {
    "node": ">=18.0.0"
  },
  "keywords": ["mcp", "p2", "propeller2", "knowledge-base"],
  "license": "MIT"
}
```

### Build Script

**`engineering/mcp-server/build.sh`:**
```bash
#!/bin/bash
set -e

echo "Building P2KB MCP Server binaries..."

# Clean previous builds
rm -rf dist
mkdir -p dist

# Install dependencies
npm install

# Build binaries
pkg . \
  --targets node18-macos-x64,node18-linux-x64,node18-win-x64 \
  --output dist/p2kb-mcp

# Verify outputs
ls -lh dist/

echo "Build complete!"
echo "Binaries in dist/:"
echo "  - p2kb-mcp-macos"
echo "  - p2kb-mcp-linux"
echo "  - p2kb-mcp-win.exe"
```

**Make executable:**
```bash
chmod +x engineering/mcp-server/build.sh
```

---

## Phase 2: Go Binaries (Production)

**Technology:** Go
**Timeline:** Week 5-8
**Binary Size:** ~2-5MB per platform

### What Gets Compiled

**Each executable contains:**
- Compiled Go code
- MCP server logic
- YAML parser (built-in)
- HTTP client (built-in)
- No external dependencies (statically linked)

**Platforms:**
- `p2kb-mcp-macos` - macOS x64/arm64
- `p2kb-mcp-linux` - Linux x64/arm64
- `p2kb-mcp-win.exe` - Windows x64

### Build Process (Local)

**Prerequisites:**
```bash
# Install Go (if not already)
brew install go  # macOS
# or download from golang.org
```

**Build commands:**
```bash
cd engineering/mcp-server-go

# Install dependencies
go mod download

# Build for all platforms
./build-all.sh

# Produces:
# dist/p2kb-mcp-macos-amd64
# dist/p2kb-mcp-macos-arm64
# dist/p2kb-mcp-linux-amd64
# dist/p2kb-mcp-linux-arm64
# dist/p2kb-mcp-win-amd64.exe
```

### Build Script

**`engineering/mcp-server-go/build-all.sh`:**
```bash
#!/bin/bash
set -e

echo "Building P2KB MCP Server Go binaries..."

VERSION=${1:-"dev"}
BUILD_TIME=$(date -u '+%Y-%m-%d_%H:%M:%S')
GIT_COMMIT=$(git rev-parse --short HEAD)

LDFLAGS="-X main.Version=${VERSION} -X main.BuildTime=${BUILD_TIME} -X main.GitCommit=${GIT_COMMIT}"

# Clean previous builds
rm -rf dist
mkdir -p dist

# macOS
echo "Building macOS (amd64)..."
GOOS=darwin GOARCH=amd64 go build -ldflags "${LDFLAGS}" -o dist/p2kb-mcp-macos-amd64 .

echo "Building macOS (arm64)..."
GOOS=darwin GOARCH=arm64 go build -ldflags "${LDFLAGS}" -o dist/p2kb-mcp-macos-arm64 .

# Linux
echo "Building Linux (amd64)..."
GOOS=linux GOARCH=amd64 go build -ldflags "${LDFLAGS}" -o dist/p2kb-mcp-linux-amd64 .

echo "Building Linux (arm64)..."
GOOS=linux GOARCH=arm64 go build -ldflags "${LDFLAGS}" -o dist/p2kb-mcp-linux-arm64 .

# Windows
echo "Building Windows (amd64)..."
GOOS=windows GOARCH=amd64 go build -ldflags "${LDFLAGS}" -o dist/p2kb-mcp-win-amd64.exe .

# Calculate checksums
cd dist
shasum -a 256 * > checksums.txt
cd ..

# Verify outputs
echo ""
echo "Build complete! Binaries in dist/:"
ls -lh dist/

echo ""
echo "Checksums:"
cat dist/checksums.txt
```

**Make executable:**
```bash
chmod +x engineering/mcp-server-go/build-all.sh
```

---

## GitHub Actions Automation

**Automated build on release creation**

### Phase 1: Node.js Workflow

**`.github/workflows/build-mcp-server-node.yml`:**
```yaml
name: Build MCP Server Binaries (Node.js)

on:
  release:
    types: [created]
  workflow_dispatch:  # Manual trigger for testing

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        working-directory: engineering/mcp-server
        run: npm install

      - name: Install pkg
        run: npm install -g pkg

      - name: Build binaries
        working-directory: engineering/mcp-server
        run: npm run build

      - name: Generate checksums
        working-directory: engineering/mcp-server/dist
        run: shasum -a 256 * > checksums.txt

      - name: Upload binaries to release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            engineering/mcp-server/dist/p2kb-mcp-macos
            engineering/mcp-server/dist/p2kb-mcp-linux
            engineering/mcp-server/dist/p2kb-mcp-win.exe
            engineering/mcp-server/dist/checksums.txt
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Phase 2: Go Workflow

**`.github/workflows/build-mcp-server-go.yml`:**
```yaml
name: Build MCP Server Binaries (Go)

on:
  release:
    types: [created]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Setup Go
        uses: actions/setup-go@v4
        with:
          go-version: '1.21'

      - name: Build binaries
        working-directory: engineering/mcp-server-go
        run: ./build-all.sh ${{ github.ref_name }}

      - name: Upload binaries to release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            engineering/mcp-server-go/dist/p2kb-mcp-*
            engineering/mcp-server-go/dist/checksums.txt
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## Repository Structure

```
P2-Knowledge-Base/
├── engineering/
│   ├── mcp-server/                      # Phase 1: Node.js version
│   │   ├── src/
│   │   │   └── server.js                # Main MCP server code
│   │   ├── package.json                 # Dependencies & pkg config
│   │   ├── build.sh                     # Local build script
│   │   ├── dist/                        # Build output (gitignored)
│   │   │   ├── p2kb-mcp-macos
│   │   │   ├── p2kb-mcp-linux
│   │   │   ├── p2kb-mcp-win.exe
│   │   │   └── checksums.txt
│   │   └── README.md                    # Development guide
│   │
│   ├── mcp-server-go/                   # Phase 2: Go version (future)
│   │   ├── main.go                      # Main entry point
│   │   ├── cache/                       # Cache management
│   │   ├── download/                    # GitHub downloader
│   │   ├── mcp/                         # MCP protocol handlers
│   │   ├── go.mod                       # Go dependencies
│   │   ├── go.sum                       # Dependency checksums
│   │   ├── build-all.sh                 # Cross-compile script
│   │   ├── dist/                        # Build output (gitignored)
│   │   └── README.md                    # Development guide
│   │
│   └── enhancements/
│       ├── p2kb-mcp-server-evaluation.md      # This doc (approach eval)
│       └── p2kb-mcp-packaging-delivery.md     # This doc (packaging)
│
├── .github/
│   └── workflows/
│       ├── build-mcp-server-node.yml    # Phase 1 automation
│       └── build-mcp-server-go.yml      # Phase 2 automation
│
├── .gitignore                           # Ignore dist/ directories
└── README.md                            # Include MCP installation
```

**`.gitignore` additions:**
```
# MCP server build artifacts
engineering/mcp-server/dist/
engineering/mcp-server/node_modules/
engineering/mcp-server-go/dist/
```

---

## Release Process

### Creating a Release (Automated)

**Steps:**

1. **Update version numbers**
   ```bash
   # Node.js version
   cd engineering/mcp-server
   npm version 1.1.0

   # Commit version bump
   git add package.json
   git commit -m "Bump MCP server to v1.1.0"
   git push
   ```

2. **Create GitHub release**
   ```bash
   # Tag the release
   git tag v1.1.0
   git push origin v1.1.0

   # Or use GitHub web interface:
   # Releases → Draft new release → Choose tag v1.1.0
   ```

3. **GitHub Actions automatically:**
   - Detects release creation
   - Checks out code
   - Builds binaries for all platforms
   - Generates checksums
   - Uploads to release assets

4. **Verify release**
   - Check GitHub releases page
   - Verify all binaries present
   - Download and test one binary

### Manual Release (Fallback)

**If GitHub Actions fails:**

```bash
# Build locally
cd engineering/mcp-server
./build.sh

# Upload to release manually
gh release upload v1.1.0 dist/p2kb-mcp-*
gh release upload v1.1.0 dist/checksums.txt
```

---

## User Installation Guide

**To be included in main README.md:**

### Installing the P2 Knowledge Base MCP Server

#### Step 1: Download Binary

Visit [Releases](https://github.com/ironsheep/P2-Knowledge-Base/releases) and download for your platform:

**macOS:**
```bash
curl -L https://github.com/ironsheep/P2-Knowledge-Base/releases/download/v1.0.0/p2kb-mcp-macos \
  -o ~/.local/bin/p2kb-mcp
chmod +x ~/.local/bin/p2kb-mcp
```

**Linux:**
```bash
curl -L https://github.com/ironsheep/P2-Knowledge-Base/releases/download/v1.0.0/p2kb-mcp-linux \
  -o ~/.local/bin/p2kb-mcp
chmod +x ~/.local/bin/p2kb-mcp
```

**Windows:**
```powershell
# Download from releases page
# Place in: C:\Users\YourName\bin\p2kb-mcp.exe
# Add directory to PATH
```

#### Step 2: Verify Installation

```bash
# Test the binary
p2kb-mcp --version
# Should output: P2KB MCP Server v1.0.0
```

#### Step 3: Configure Claude Code

**Edit:** `~/.config/claude/config.json`

```json
{
  "mcpServers": {
    "p2kb": {
      "command": "/Users/YOUR_USERNAME/.local/bin/p2kb-mcp",
      "name": "P2 Knowledge Base"
    }
  }
}
```

**Windows:** Use full path like `"C:\\Users\\YourName\\bin\\p2kb-mcp.exe"`

#### Step 4: Restart Claude Code

The MCP server will now be available. Test by asking Claude:
```
"Fetch the P2 root manifest"
```

Claude should use the `p2kb__fetch_file` tool.

---

## Version Migration (Phase 1 → Phase 2)

### User Upgrade Path

**From Node.js binary to Go binary:**

1. **Download new Go binary**
   ```bash
   curl -L https://github.com/ironsheep/P2-Knowledge-Base/releases/download/v2.0.0/p2kb-mcp-macos \
     -o ~/.local/bin/p2kb-mcp
   chmod +x ~/.local/bin/p2kb-mcp
   ```

2. **No config changes needed**
   - Same command path
   - Same cache location (`~/.p2kb-cache/`)
   - Same tool names

3. **Verify upgrade**
   ```bash
   p2kb-mcp --version
   # Should output: P2KB MCP Server v2.0.0 (Go)
   ```

**Cache compatibility:**
- Both versions use same cache format
- Existing cache works with new binary
- No need to clear cache

---

## Testing Checklist

### Before Release

**Build verification:**
- [ ] All binaries build successfully
- [ ] Checksums generated
- [ ] Binary sizes reasonable (Node.js: ~50MB, Go: ~2-5MB)

**Functionality testing:**
- [ ] Binary runs without errors
- [ ] Can connect via MCP protocol
- [ ] `fetch_file` downloads and caches
- [ ] `check_updates` compares hashes correctly
- [ ] `clear_cache` removes cached files
- [ ] Cache directory created properly

**Platform testing:**
- [ ] macOS binary works
- [ ] Linux binary works
- [ ] Windows binary works

**Claude Code integration:**
- [ ] Config file format correct
- [ ] Claude can discover tools
- [ ] Tools execute successfully
- [ ] Errors handled gracefully

**Performance:**
- [ ] Startup time < 1 second
- [ ] File fetch < 100ms (cached)
- [ ] File fetch < 2s (download)
- [ ] Memory usage reasonable

---

## Troubleshooting

### Build Issues

**pkg fails with "Cannot find module":**
```bash
# Ensure dependencies installed
npm install

# Check pkg assets configuration
# Add any dynamic requires to package.json "pkg.assets"
```

**Go cross-compile fails:**
```bash
# Ensure Go version >= 1.21
go version

# Clean and rebuild
rm -rf dist
./build-all.sh
```

### Runtime Issues

**Binary won't execute (macOS):**
```bash
# Remove quarantine attribute
xattr -d com.apple.quarantine p2kb-mcp-macos

# Make executable
chmod +x p2kb-mcp-macos
```

**Permission denied:**
```bash
# Ensure binary is executable
chmod +x ~/.local/bin/p2kb-mcp

# Ensure directory in PATH
echo $PATH | grep .local/bin
```

**Claude Code can't find MCP:**
```bash
# Verify config file location
cat ~/.config/claude/config.json

# Verify command path is absolute
# Use full path, not ~
```

---

## Maintenance

### Updating Dependencies

**Node.js version:**
```bash
cd engineering/mcp-server

# Update MCP SDK
npm install @modelcontextprotocol/sdk@latest

# Update YAML parser
npm install yaml@latest

# Rebuild
npm run build
```

**Go version:**
```bash
cd engineering/mcp-server-go

# Update dependencies
go get -u ./...
go mod tidy

# Rebuild
./build-all.sh
```

### Security Updates

**Monitor:**
- `npm audit` for Node.js dependencies
- GitHub Dependabot alerts
- Go security advisories

**Update process:**
```bash
# Fix security issues
npm audit fix

# Rebuild and release patch version
npm version patch
git push && git push --tags
```

---

## Future Enhancements

### Potential Distribution Improvements

**Homebrew formula:**
```ruby
# Formula for Go version
class P2kbMcp < Formula
  desc "P2 Knowledge Base MCP Server"
  homepage "https://github.com/ironsheep/P2-Knowledge-Base"
  url "https://github.com/ironsheep/P2-Knowledge-Base/releases/download/v2.0.0/p2kb-mcp-macos"
  sha256 "..."

  def install
    bin.install "p2kb-mcp-macos" => "p2kb-mcp"
  end
end
```

**npm package (alternative):**
- Keep npm as alternate distribution
- Points to pre-built binaries
- `npm install -g @p2kb/mcp-server` downloads binary

**Auto-updates:**
- Check for newer version on startup
- Notify user of available updates
- Optional auto-download

---

## Comparison: Node.js vs Go Distribution

| Aspect | Phase 1 (Node.js + pkg) | Phase 2 (Go) |
|--------|------------------------|--------------|
| **Binary Size** | ~50MB | ~2-5MB |
| **Startup Time** | 100-200ms | 5-10ms |
| **Memory Usage** | 30-50MB | 5-10MB |
| **Dependencies** | Bundled Node.js runtime | None (statically linked) |
| **Build Complexity** | npm + pkg | Go cross-compile |
| **Distribution Size** | 150MB (3 platforms) | 10-15MB (3 platforms) |
| **Runtime Required** | None (bundled) | None |
| **Update Size** | 50MB per platform | 2-5MB per platform |
| **Matches Todo MCP** | No | Yes |

**Recommendation:** Start with Node.js for speed, transition to Go for production quality.
