# AI Reference Deliverables

This directory contains released versions of the P2 Knowledge Base packaged for AI consumption.

## Structure

```
ai-reference/
├── README.md          # This file
└── versions/          # Released versions
    ├── v1.0.0/       # Initial release
    ├── v1.1.0/       # Previous release
    ├── v1.3.0/       # Current release (with idioms & patterns)
    └── latest/       # Symlink to current release (v1.3.0)
```

## Current Release: v1.3.0

### What's Available

Each version directory contains:
- `p2-reference-vX.Y.Z.json` - Complete P2 reference in JSON format
- `CHANGELOG.md` - Changes in this version
- `RELEASE-NOTES.md` - Release highlights and usage

### Usage

```python
import json

# Load the latest version
with open('versions/latest/p2-reference-v1.3.0.json') as f:
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
