#!/bin/bash
# Cleanup deliverables/ai-reference to contain only released versions

echo "🧹 Cleaning up deliverables/ai-reference directory..."
echo "=================================================="

# Set base directory
BASE_DIR="deliverables/ai-reference"

# 1. Delete old/outdated content
echo "🗑️  Removing outdated content..."

# Remove old directories
if [ -d "$BASE_DIR/p2-claude-knowledge" ]; then
    echo "   Deleting p2-claude-knowledge/ (outdated, replaced by YAMLs)..."
    rm -rf "$BASE_DIR/p2-claude-knowledge"
fi

if [ -d "$BASE_DIR/v1.0" ]; then
    echo "   Deleting v1.0/ (old structure)..."
    rm -rf "$BASE_DIR/v1.0"
fi

if [ -d "$BASE_DIR/schemas" ]; then
    echo "   Deleting schemas/ (belongs in packages only)..."
    rm -rf "$BASE_DIR/schemas"
fi

# Remove old markdown files
if [ -f "$BASE_DIR/pasm2-knowledge-synthesis.md" ]; then
    echo "   Deleting pasm2-knowledge-synthesis.md (outdated synthesis)..."
    rm "$BASE_DIR/pasm2-knowledge-synthesis.md"
fi

# Remove old symlink
if [ -L "$BASE_DIR/latest" ]; then
    echo "   Removing old 'latest' symlink..."
    rm "$BASE_DIR/latest"
fi

# 2. Ensure versions directory exists
echo "📁 Setting up clean structure..."
mkdir -p "$BASE_DIR/versions"

# Move v0.1.0 if it exists at top level
if [ -d "$BASE_DIR/versions/v0.1.0" ]; then
    echo "   v0.1.0 already in versions/"
else
    if [ -d "deliverables/ai-reference/v0.1.0" ]; then
        echo "   Moving v0.1.0 to versions/"
        mv "deliverables/ai-reference/v0.1.0" "$BASE_DIR/versions/"
    fi
fi

# 3. Create new latest symlink pointing to v1.1.0
echo "🔗 Creating new 'latest' symlink..."
cd "$BASE_DIR/versions" || exit
if [ -d "v1.1.0" ]; then
    ln -sf v1.1.0 latest
    echo "   latest -> v1.1.0"
fi
cd - > /dev/null || exit

# 4. Create/Update README
echo "📝 Creating README.md..."
cat > "$BASE_DIR/README.md" << 'EOF'
# AI Reference Deliverables

This directory contains released versions of the P2 Knowledge Base packaged for AI consumption.

## Structure

```
ai-reference/
├── README.md          # This file
└── versions/          # Released versions
    ├── v1.0.0/       # Initial release
    ├── v1.1.0/       # Current release
    └── latest/       # Symlink to current release
```

## Current Release: v1.1.0

### What's Available

Each version directory contains:
- `p2-reference-vX.Y.Z.json` - Complete P2 reference in JSON format
- `CHANGELOG.md` - Changes in this version
- `RELEASE-NOTES.md` - Release highlights and usage

### Usage

```python
import json

# Load the latest version
with open('versions/latest/p2-reference-v1.1.0.json') as f:
    p2_ref = json.load(f)

# Access PASM2 instructions
instructions = p2_ref['instructions']

# Access SPIN2 elements
spin2 = p2_ref['spin2']
```

## Release Packages

Official release packages are available on GitHub:
https://github.com/ironsheep/P2-Knowledge-Base/releases

### Package Types

1. **JSON Reference Package** (`p2-reference-vX.Y.Z.tar.gz`)
   - Single JSON file with all knowledge
   - Includes schemas for validation
   - Best for: AI systems wanting single-file consumption

2. **Complete Knowledge Base** (`p2-complete-kb-vX.Y.Z.tar.gz`)
   - Full YAML knowledge base
   - Includes manifest hierarchy
   - Best for: Systems wanting modular access

## Source

The source knowledge base is maintained in:
`engineering/knowledge-base/P2/`

## Building Releases

Releases are built using GitHub Actions or manually with:
```bash
python3 engineering/tools/update-p2-reference-complete.py X.Y.Z
python3 engineering/tools/package-complete-knowledge-base.py X.Y.Z
```

---
*Generated from: engineering/knowledge-base/P2/*
EOF

# 5. Summary
echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📊 Summary:"
echo "   • Deleted outdated content (p2-claude-knowledge/, schemas/, old markdowns)"
echo "   • Cleaned deliverables/ai-reference/"
echo "   • Created versions/ directory structure"
echo "   • Updated latest symlink to v1.1.0"
echo "   • Created new README.md"
echo ""
echo "🗂️  New structure:"
tree -L 2 "$BASE_DIR" 2>/dev/null || ls -la "$BASE_DIR"