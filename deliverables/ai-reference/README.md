# AI Reference Deliverables

This directory contains the P2 Knowledge Base packaged for AI consumption.

## Quick Start

**[→ BOOTSTRAP.md](BOOTSTRAP.md)** - Single-command setup for AI assistants

## Structure

```
ai-reference/
├── BOOTSTRAP.md           # START HERE - One-command setup
├── README.md              # This file
├── p2-reference.json      # Complete P2 reference (single file)
└── auxiliary-guides/      # Additional usage guides
    └── interaction/
        └── using-with-ai.md   # Comprehensive guide
```

## For AI Assistants

### Setup (v3.2)

Fetch and follow: `deliverables/ai-reference/BOOTSTRAP.md`

This downloads the key-based access system with:
- `fetch-kb-file.sh` - Main fetch script with `--search`, `--browse`, `--categories`
- `refresh-kb.sh` - Updates everything
- `p2kb-index.json` - Master index of 970+ content keys
- Pre-cached getting-started guides

### Usage

```bash
.p2kb-cache/fetch-kb-file.sh --search mov      # Find keys
.p2kb-cache/fetch-kb-file.sh --browse pasm2    # Browse category
.p2kb-cache/fetch-kb-file.sh p2kbPasm2Mov      # Fetch content
```

## For Programmatic Access

```python
import json

# Load the reference
with open('deliverables/ai-reference/p2-reference.json') as f:
    p2_ref = json.load(f)

# Access PASM2 instructions
instructions = p2_ref['instructions']

# Access SPIN2 elements
spin2 = p2_ref['spin2']
```

## Source Content

The source knowledge base YAML files are in:
`deliverables/ai/P2/`

## Versioning

Git provides versioning. Use git tags to access specific versions:
```bash
git checkout v2.0.0  # Access specific release
```

## Release Packages

Official release packages are available on GitHub:
https://github.com/ironsheep/P2-Knowledge-Base/releases

---

*Version 3.2 - Key-based access system*
