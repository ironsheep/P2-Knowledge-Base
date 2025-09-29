# AI Integration Architecture
*Technical documentation for the self-bootstrapping system*

## Overview

Version 2.0 introduces a self-bootstrapping system where the P2 Knowledge Base teaches AI assistants how to use it automatically. This eliminates the need for users to copy-paste lengthy instructions.

## System Architecture

### Components

1. **Ultra-Minimal Root** (`manifests/propeller-knowledge-root.yaml`)
   - Entry point for all AI interactions
   - Contains AI instructions pointer with hash
   - Routes to P1/P2 knowledge bases
   - ~30 lines total (was 200+)

2. **AI Instructions** (`manifests/ai-instructions.yaml`)
   - Comprehensive navigation rules
   - Category catalog with real manifest paths
   - Platform-specific setup instructions
   - Self-contained with hash for validation

3. **Hash Generator** (`engineering/tools/generate-instruction-hash.py`)
   - Computes SHA256 of instructions file
   - Updates hash in both instructions and root
   - Ensures consistency across system

## How It Works

### First Contact Flow
```
User → "Use P2 KB at GitHub URL"
  ↓
AI → Fetch root manifest
  ↓
Root → "Instructions at manifests/ai-instructions.yaml"
  ↓
AI → Fetch instructions (no stored hash yet)
  ↓
Instructions → "Save this content to your CLAUDE.md"
  ↓
AI → Saves instructions with hash
  ↓
AI → "Ready to help with P2 development"
```

### Subsequent Sessions
```
AI → Fetch root manifest
  ↓
Root → Hash: sha256:4a91d6...
  ↓
AI → Compare with stored hash
  ↓
Same? → Skip update, use cached
Different? → Fetch new instructions
```

### Forced Refresh
```
User → "Update P2 KB instructions"
  ↓
AI → Fetch instructions regardless of hash
  ↓
AI → Replace stored instructions
```

## Maintenance Procedures

### Updating AI Instructions

1. **Edit the instructions file**:
   ```bash
   vi manifests/ai-instructions.yaml
   ```

2. **Update categories if manifest structure changes**:
   - Check actual categories in manifest files
   - Don't guess - use real paths and categories
   - Include entry counts where known

3. **Generate new hash**:
   ```bash
   python3 engineering/tools/generate-instruction-hash.py
   ```
   This updates the hash in both files automatically.

4. **Commit changes**:
   ```bash
   git add manifests/ai-instructions.yaml
   git add manifests/propeller-knowledge-root.yaml
   git commit -m "Update AI instructions [describe changes]"
   ```

### Adding P1 Support

When P1 knowledge base is ready:

1. Create `manifests/P1/p1-root.yaml`
2. Update root manifest to point to it (already has placeholder)
3. Update AI instructions with P1 categories
4. Run hash generator
5. Commit all changes

### Testing Changes

1. **Clear your AI session** (start fresh)
2. **Give minimal bootstrap**:
   ```
   Use P2 Knowledge Base at https://github.com/ironsheep/P2-Knowledge-Base
   Start with manifests/propeller-knowledge-root.yaml
   ```
3. **Verify AI**:
   - Fetches instructions
   - Saves to memory/notes
   - Can navigate to categories directly

## Design Principles

### 1. Minimal Entry Point
- Root contains ONLY routing and version info
- No knowledge base content in root
- Clean separation of concerns

### 2. Self-Contained Instructions
- Instructions file has everything needed
- Platform-aware (Claude, ChatGPT, others)
- Contains its own hash for validation

### 3. Hash-Based Versioning
- SHA256 ensures any change triggers update
- No manual version bumping needed
- Automatic invalidation on edit

### 4. Category Reality
- Categories reflect ACTUAL manifest structure
- No guessing or placeholder categories
- Regular audits against real manifests

## Benefits Over v1.0

| Aspect | Version 1.0 | Version 2.0 |
|--------|-------------|-------------|
| Bootstrap | 200+ line copy-paste | 4 lines |
| Updates | Manual re-paste | Automatic |
| Categories | Traverse from root | Direct access |
| Maintenance | Edit multiple docs | Single source |
| User Experience | Complex setup | "Just works" |

## File Responsibilities

- **Root YAML**: Router and version checker only
- **AI Instructions**: All navigation and usage rules
- **Manifest Files**: Unchanged, still source of truth
- **Hash Script**: Maintains consistency

## Common Issues

### Hash Mismatch
**Symptom**: Hash in root doesn't match instructions file
**Solution**: Run `generate-instruction-hash.py`

### Categories Out of Date
**Symptom**: AI can't find category mentioned in instructions
**Solution**: Audit actual manifests, update instructions

### Platform Confusion
**Symptom**: AI doesn't know how to save instructions
**Solution**: Check platform detection in instructions

## Future Enhancements

- [ ] Add changelog/release notes to instructions
- [ ] Version-specific feature flags
- [ ] Multi-language instruction sets
- [ ] Automatic category extraction from manifests
- [ ] GitHub Action for hash generation on PR

## Security Considerations

- Hash ensures instructions haven't been tampered with
- AI won't execute arbitrary code from instructions
- Users can verify hash manually if concerned
- System is read-only (no write-back to repo)

---

*Last Updated: 2025-01-29*
*System Version: 2.0*