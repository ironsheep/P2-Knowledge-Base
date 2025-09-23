# Manifest Linkage Verification System

## Overview
The linkage verification system ensures referential integrity in the P2 Knowledge Base by checking that all files referenced in manifests actually exist. This prevents broken links in releases and maintains knowledge base quality.

## Components

### 1. Python Verification Script
**File**: `verify-manifest-linkages.py`

The core verification logic that:
- Parses all YAML manifests
- Extracts file references
- Verifies each referenced file exists
- Reports broken linkages
- Provides detailed statistics

### 2. Shell Wrapper Script  
**File**: `verify-manifest-linkages.sh`

Convenience wrapper that:
- Sets up the environment
- Checks dependencies
- Runs the Python script
- Formats output with colors

## Usage

### Manual Verification
```bash
# Basic verification
./engineering/tools/verify-manifest-linkages.sh

# Verbose mode - shows all files checked
./engineering/tools/verify-manifest-linkages.sh --verbose

# CI mode - exits with error code if issues found
./engineering/tools/verify-manifest-linkages.sh --ci

# No color output (for logs)
python3 engineering/tools/verify-manifest-linkages.py --no-color
```

### As a Git Pre-Commit Hook
Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
./engineering/tools/verify-manifest-linkages.sh --ci
if [ $? -ne 0 ]; then
    echo "Commit aborted: Fix manifest linkages first"
    exit 1
fi
```

### In GitHub Actions
```yaml
name: Verify Manifest Linkages

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    
    - name: Install dependencies
      run: |
        pip install pyyaml
    
    - name: Verify manifest linkages
      run: |
        python3 engineering/tools/verify-manifest-linkages.py --ci --no-color
```

## What Gets Checked

### Manifests Verified
1. **Root manifest** - `manifests/p2-knowledge-root.yaml`
2. **Core manifests**:
   - PASM2 Instructions
   - Spin2 Language
   - Architecture
   - Smart Pins
   - Patterns
   - Hardware
   - Quick Queries
3. **Obex manifests**:
   - Obex root manifest
   - All category manifests (9)
   - All author manifests (24)

### File Reference Patterns
The verifier detects:
- `file: "path/to/file.yaml"` - Standard file references
- `yaml_path: ../path/to/file.yaml` - Obex-style references
- Relative paths (../) and absolute paths
- Base path resolution

## Output Examples

### Success Output
```
✓ PASM2 Instructions: All 362 references valid
✓ Spin2 Language: All 141 references valid
✓ Architecture: All 15 references valid
...
✅ ALL MANIFEST LINKAGES VERIFIED SUCCESSFULLY!
The knowledge base is ready for release.
```

### Failure Output
```
✗ Patterns: 25 missing files
  - engineering/knowledge-base/P2/patterns/uart-smart-pin.yaml
  - engineering/knowledge-base/P2/patterns/spi-master.yaml
  ... and 20 more
  
❌ VERIFICATION FAILED
Please fix the above issues before release.
```

## Exit Codes
- `0` - All linkages valid
- `1` - Broken linkages found
- `2` - Script error

## Integration with Release Process

### Recommended Workflow
1. **Development**: Run verification after manifest changes
2. **Pre-commit**: Automatic verification via git hook
3. **Pull Request**: CI verification via GitHub Actions
4. **Release**: Final verification before tagging

### Release Checklist
```bash
# 1. Verify linkages
./engineering/tools/verify-manifest-linkages.sh

# 2. If issues found, fix them
# Edit manifests or create missing files

# 3. Re-verify
./engineering/tools/verify-manifest-linkages.sh

# 4. Commit fixes
git add -A
git commit -m "Fix manifest linkages"

# 5. Tag release
git tag -a v1.x.x -m "Release v1.x.x"
```

## Maintenance

### Adding New Manifests
When adding a new manifest:
1. Add it to the `manifests` list in `verify-manifest-linkages.py`
2. Follow the existing pattern for file references
3. Run verification to ensure it works

### Updating Verification Logic
The script is versioned and should be updated when:
- New manifest formats are introduced
- New file reference patterns are used
- Additional validation is needed

## Troubleshooting

### Common Issues

**PyYAML not installed**
```bash
pip3 install pyyaml
```

**Permission denied**
```bash
chmod +x engineering/tools/verify-manifest-linkages.sh
```

**Path resolution issues**
- Ensure you run from repository root
- Check base_path in manifests
- Verify relative paths are correct

## Version History
- **v1.0.0** (2025-09-23): Initial implementation
  - Comprehensive manifest checking
  - Color-coded output
  - CI/CD support
  - Verbose and quiet modes