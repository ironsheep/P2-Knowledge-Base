# Manifest Reorganization Action Plan
**Date**: 2025-09-27
**Version**: 1.0
**Status**: DRAFT

## Overview
Reorganize manifest structure to properly scope P2 manifests and prepare for future P1 addition.

## Pre-Flight Checklist
- [ ] Run validation script and save baseline: `python3 engineering/tools/verify-manifest-linkages.py > baseline.txt`
- [ ] Commit any pending changes: `git status`
- [ ] Create backup branch: `git checkout -b manifest-reorg-backup`
- [ ] Switch to work branch: `git checkout -b manifest-reorganization`

## Phase 1: Create Directory Structure
```bash
# Create new directories (git will track these when we add files)
mkdir -p manifests/P2/language
mkdir -p manifests/P2/language/pasm2
mkdir -p manifests/P2/community
mkdir -p manifests/P2/community/obex
mkdir -p manifests/P2/architecture
```

## Phase 2: Move Manifests with Git (Preserves History)

### 2.1 Move Top-Level Manifests to P2/
```bash
git mv manifests/p2-knowledge-root.yaml manifests/P2/p2-root.yaml
git mv manifests/architecture-manifest.yaml manifests/P2/architecture-manifest.yaml
git mv manifests/hardware-manifest.yaml manifests/P2/hardware-manifest.yaml
git mv manifests/patterns-manifest.yaml manifests/P2/patterns-manifest.yaml
git mv manifests/smart-pins-manifest.yaml manifests/P2/smart-pins-manifest.yaml
git mv manifests/auxiliary-guides-manifest.yaml manifests/P2/auxiliary-guides-manifest.yaml
git mv manifests/quick-queries-manifest.yaml manifests/P2/quick-queries-manifest.yaml
```

### 2.2 Move Language Manifests
```bash
git mv manifests/spin2-manifest.yaml manifests/P2/language/spin2-manifest.yaml
git mv manifests/pasm2-manifest.yaml manifests/P2/language/pasm2-manifest.yaml
```

### 2.3 Move PASM2 Sub-Manifests
```bash
git mv manifests/pasm2/*.yaml manifests/P2/language/pasm2/
```

### 2.4 Move OBEX Structure
```bash
git mv manifests/obex/obex-root.yaml manifests/P2/community/obex-manifest.yaml
git mv manifests/obex/categories manifests/P2/community/obex/
git mv manifests/obex/authors manifests/P2/community/obex/
rmdir manifests/obex  # Remove empty directory
```

## Phase 3: Move Mislocated Manifests from Knowledge Base

### 3.1 Set Aside Old Manifests for Audit
```bash
# Create temporary set-aside location
mkdir -p engineering/operations/manifest-reorg-set-aside

# Move old versions to set-aside (preserving paths for reference)
git mv engineering/knowledge-base/P2/root_manifest.yaml \
      engineering/operations/manifest-reorg-set-aside/root_manifest.yaml.OLD

git mv engineering/knowledge-base/P2/architecture/architecture_manifest.yaml \
      engineering/operations/manifest-reorg-set-aside/architecture_manifest.yaml.OLD

git mv engineering/knowledge-base/P2/architecture/smart-pins/smartpin_manifest.yaml \
      engineering/operations/manifest-reorg-set-aside/smartpin_manifest.yaml.OLD

git mv engineering/knowledge-base/P2/hardware/board_manifest.yaml \
      engineering/operations/manifest-reorg-set-aside/board_manifest.yaml.OLD

# IMPORTANT: These two have MORE content than current manifests!
git mv engineering/knowledge-base/P2/language/pasm2/instruction_manifest.yaml \
      engineering/operations/manifest-reorg-set-aside/instruction_manifest.yaml.AUDIT

git mv engineering/knowledge-base/P2/language/pasm2/patterns/pattern_manifest.yaml \
      engineering/operations/manifest-reorg-set-aside/pattern_manifest.yaml.OLD

git mv engineering/knowledge-base/P2/language/spin2/method_manifest.yaml \
      engineering/operations/manifest-reorg-set-aside/method_manifest.yaml.AUDIT
```

**NOTE**: Files marked `.AUDIT` have MORE content than current manifests and need careful review!

### 3.2 Move Unique Manifests to Proper Locations
```bash
# System registers manifest
git mv engineering/knowledge-base/P2/architecture/system-registers/register_manifest.yaml \
      manifests/P2/architecture/registers-manifest.yaml

# Language fundamentals
git mv engineering/knowledge-base/P2/language/fundamentals/fundamentals-manifest.yaml \
      manifests/P2/language/fundamentals-manifest.yaml

# Spin2 conventions
git mv engineering/knowledge-base/P2/language/spin2/conventions/comment-styles-manifest.yaml \
      manifests/P2/language/spin2-conventions-manifest.yaml

# Code examples
git mv engineering/knowledge-base/P2/code-examples/examples_manifest.yaml \
      manifests/P2/code-examples-manifest.yaml
```

## Phase 4: Create New Parent Manifests

### 4.1 Create True Root Manifest
**File**: `manifests/propeller-knowledge-root.yaml`
```yaml
# Propeller Knowledge Base Root Manifest
# Points to all Propeller chip versions

manifest_metadata:
  version: "1.0"
  created: "2025-09-27"
  description: "Root manifest for all Propeller chip documentation"

propeller_chips:
  p2:
    name: "Propeller 2 (P2)"
    manifest: "P2/p2-root.yaml"
    status: "active"
    description: "8-core, 32-bit multicore microcontroller"
  
  p1:
    name: "Propeller 1 (P1)"
    manifest: "P1/p1-root.yaml"  
    status: "future"
    description: "8-core, 32-bit multicore microcontroller (legacy)"
```

### 4.2 Create Language Parent Manifest
**File**: `manifests/P2/language/language-manifest.yaml`
```yaml
manifest_metadata:
  version: "1.0"
  created: "2025-09-27"
  description: "P2 Programming Languages"

languages:
  spin2:
    name: "Spin2"
    manifest: "spin2-manifest.yaml"
    description: "High-level language for P2"
    
  pasm2:
    name: "PASM2"
    manifest: "pasm2-manifest.yaml"
    description: "Assembly language for P2"
    
  fundamentals:
    name: "Language Fundamentals"
    manifest: "fundamentals-manifest.yaml"
    description: "Core concepts shared by both languages"
```

### 4.3 Create Community Parent Manifest
**File**: `manifests/P2/community/community-manifest.yaml`
```yaml
manifest_metadata:
  version: "1.0"
  created: "2025-09-27"
  description: "P2 Community Contributions"

sources:
  obex:
    name: "OBEX (Object Exchange)"
    manifest: "obex/obex-manifest.yaml"
    description: "Community code objects from Parallax OBEX"
    
  quickbytes:
    name: "Quick Bytes"
    status: "coming_soon"
    description: "Community tutorials and quick tips"
```

## Phase 5: Update All References

### 5.1 Update P2 Root Manifest
**File**: `manifests/P2/p2-root.yaml`
- Change all manifest references to include proper paths
- Update from `manifests/xxx.yaml` to relative paths
- Add reference to new language-manifest.yaml
- Add reference to new community-manifest.yaml

### 5.2 Update PASM2 Manifest
**File**: `manifests/P2/language/pasm2-manifest.yaml`
- Update sub-manifest paths from `pasm2/xxx.yaml` to `pasm2/xxx.yaml` (stays same)

### 5.3 Update OBEX Manifest
**File**: `manifests/P2/community/obex-manifest.yaml`
- Update category references from `categories/xxx.yaml` to `obex/categories/xxx.yaml`
- Update author references from `authors/xxx.yaml` to `obex/authors/xxx.yaml`

### 5.4 Update Validation Script Referenced Manifests
**File**: `engineering/tools/verify-manifest-linkages.py`
```python
# Update manifest paths
manifests = [
    ("Root Manifest", "manifests/P2/p2-root.yaml"),
    ("PASM2 Instructions", "manifests/P2/language/pasm2-manifest.yaml"),
    ("Spin2 Language", "manifests/P2/language/spin2-manifest.yaml"),
    ("Architecture", "manifests/P2/architecture-manifest.yaml"),
    # ... etc
]
```

## Phase 6: Audit Set-Aside Content

### 6.1 Create Audit Report
```bash
cat > engineering/operations/manifest-reorg-audit.md << 'EOF'
# Manifest Reorganization Audit Report
Date: [To be filled]

## Purpose
Document the comparison between set-aside manifests and new structure to ensure no content loss.

## Set-Aside Files Analysis

### instruction_manifest.yaml.AUDIT (514 lines)
- **Contains**: Complete alphabetical list of 358 PASM2 instructions
- **Current manifest**: Hierarchical by category (204 lines)
- **Audit checks**:
  - [ ] All 358 instructions present in new structure
  - [ ] No instructions missing from categories
  - [ ] Category assignments correct
- **Findings**: [To be documented]
- **Decision**: [ ] Delete / [ ] Keep as reference

### method_manifest.yaml.AUDIT (449 lines)
- **Contains**: Detailed Spin2 method listings
- **Current manifest**: Hierarchical structure (353 lines)
- **Audit checks**:
  - [ ] All methods present in new structure
  - [ ] No methods missing from categories
  - [ ] Debug formatters complete
- **Findings**: [To be documented]
- **Decision**: [ ] Delete / [ ] Keep as reference

### Old Version Files
These are older versions superseded by current manifests:
- root_manifest.yaml.OLD (42 lines) - Old version, current is 185 lines
- architecture_manifest.yaml.OLD (46 lines) - Old version, current is 151 lines
- smartpin_manifest.yaml.OLD (106 lines) - Old version, current is 212 lines
- board_manifest.yaml.OLD (49 lines) - Different structure, current is 157 lines
- pattern_manifest.yaml.OLD (23 lines) - PASM2-specific, merged into general patterns

## Verification Commands Used
```bash
# Count instructions in new structure
grep -r "yaml" manifests/P2/language/pasm2/ | wc -l

# Compare with set-aside
diff -u manifest-reorg-set-aside/instruction_manifest.yaml.AUDIT \
        manifests/P2/language/pasm2-manifest.yaml
```

## Final Verification
- [ ] No content loss identified
- [ ] All valuable content preserved in new structure
- [ ] Safe to delete set-aside files

## Lessons Learned
[Document what we learned from having multiple versions]
EOF
```

### 6.2 Run Audit Comparisons
```bash
# Compare instruction counts
echo "Instructions in set-aside:"
grep ".yaml" engineering/operations/manifest-reorg-set-aside/instruction_manifest.yaml.AUDIT | wc -l

echo "Instructions in new structure:"
find manifests/P2/language/pasm2 -name "*.yaml" | wc -l

# Similar for methods
echo "Methods in set-aside:"
grep ".yaml" engineering/operations/manifest-reorg-set-aside/method_manifest.yaml.AUDIT | wc -l

echo "Methods in new structure:"
grep "file:" manifests/P2/language/spin2-manifest.yaml | wc -l
```

## Phase 7: Validation

### 6.1 Check Git Status
```bash
git status  # Should show all moves and new files
```

### 6.2 Run Validation Script
```bash
python3 engineering/tools/verify-manifest-linkages.py > after-reorg.txt
diff baseline.txt after-reorg.txt  # Compare before/after
```

### 6.3 Test Critical Paths
- [ ] Can navigate from propeller-knowledge-root.yaml to P2
- [ ] Can navigate from P2 to language manifests
- [ ] Can navigate from P2 to community/OBEX
- [ ] All OBEX categories accessible
- [ ] All PASM2 sub-categories accessible

## Phase 8: Commit Changes

### 7.1 Stage and Commit in Logical Groups
```bash
# Commit 1: Directory structure
git add manifests/P2/
git commit -m "Create P2 manifest directory structure"

# Commit 2: Move core manifests
git add manifests/P2/*.yaml
git commit -m "Move P2 manifests to P2/ directory"

# Commit 3: Language reorganization  
git add manifests/P2/language/
git commit -m "Reorganize language manifests under language/"

# Commit 4: Community reorganization
git add manifests/P2/community/
git commit -m "Create community structure with OBEX"

# Commit 5: Clean up obsolete files
git add -u  # Adds deletions
git commit -m "Remove obsolete duplicate manifests"

# Commit 6: New parent manifests
git add manifests/propeller-knowledge-root.yaml
git add manifests/P2/language/language-manifest.yaml
git add manifests/P2/community/community-manifest.yaml
git commit -m "Add parent manifests for new hierarchy"

# Commit 7: Update references
git add manifests/P2/
git add engineering/tools/verify-manifest-linkages.py
git commit -m "Update all manifest cross-references for new structure"
```

## Phase 9: Final Cleanup

### 9.1 After Successful Audit
```bash
# Only execute after audit confirms no content loss!
rm -rf engineering/operations/manifest-reorg-set-aside/
git add -u
git commit -m "Remove set-aside files after successful content audit"
```

### 9.2 Preserve Audit Report
- The `manifest-reorg-audit.md` becomes permanent documentation
- Records what we learned about manifest evolution
- Helps future maintainers understand the reorganization

## Phase 10: Documentation

### 8.1 Update README
- Document new manifest structure
- Explain P1/P2 separation
- Update any manifest paths in documentation

### 8.2 Create Manifest Organization Standard
Create `engineering/operations/standards/manifest-organization-standard.md`

## Rollback Plan
If anything goes wrong:
```bash
git checkout manifest-reorg-backup  # Return to backup
git branch -D manifest-reorganization  # Delete work branch
```

## Success Criteria
- [ ] All git moves preserve history
- [ ] No orphaned manifests in validation
- [ ] No broken references
- [ ] Clear path for P1 addition
- [ ] Clear path for Quick Bytes addition
- [ ] All tests pass

## Notes
- Total files to move: ~60
- Total references to update: ~100+
- Files to audit: 7 (2 need careful review)
- Estimated time: 3-4 hours (including audit)
- Risk level: Low (set-aside strategy ensures no content loss)