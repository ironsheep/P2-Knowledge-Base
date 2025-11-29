# AI Reference Deliverables

This directory contains the P2 Knowledge Base packaged for AI consumption.

## Structure

```
ai-reference/
├── README.md              # This file
├── p2-reference.json      # Complete P2 reference (single file)
└── auxiliary-guides/      # Additional usage guides
```

## Usage

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

## Versioning

Git provides versioning. Use git tags to access specific versions:
```bash
git checkout v2.0.0  # Access specific release
```

## Release Packages

Official release packages are available on GitHub:
https://github.com/IronSheepProductionsLLC/P2-Knowledge-Base/releases

## Source

The source knowledge base is maintained in:
`deliverables/ai/P2/`

## Building/Updating

To regenerate the reference JSON from YAML sources:
```bash
python3 engineering/tools/update-p2-reference-complete.py
```

---
*Generated from: deliverables/ai/P2/*
