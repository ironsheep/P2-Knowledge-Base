# P2 Knowledge Base Release Planning

## Current Status
**Version**: v1.2.0 (Released 2025-09-13)
**Files**: 377 PASM2 files (360 instructions + 17 concepts)
**Next**: v1.3.0 (after OBEX integration)

## Quick Reference
```bash
# Generate release packages
python3 engineering/tools/generate-ai-reference-from-yaml.py 1.3.0

# Key files to update before release
engineering/release-prep/ai-packages/PACKAGE-CHANGELOG.md        # Customer-facing changes
engineering/release-prep/ai-packages/README-template.md          # Package documentation template
engineering/release-prep/ai-packages/v1.3.0/RELEASE-NOTES.md     # GitHub release summary
```

## Version Numbering
- **MAJOR (X.0.0)**: Breaking schema changes, structure reorganization
- **MINOR (0.X.0)**: New instructions/language elements, >10% coverage increase
- **PATCH (0.0.X)**: Fixes, typos, minor updates, <10% coverage increase

## Release Content Management

### Source Files (Update These)
| File | Purpose | When to Update |
|------|---------|----------------|
| `engineering/release-prep/ai-packages/PACKAGE-CHANGELOG.md` | Customer-facing changes | Before each release |
| `engineering/release-prep/ai-packages/README-template.md` | Package documentation | Only when package structure changes |
| `engineering/release-prep/ai-packages/vX.Y.Z/RELEASE-NOTES.md` | Version summary | Before each release |
| `CHANGELOG.md` | Development tracking | Continuously |

### Content Guidelines
- **Package changelog**: New instructions, coverage improvements, breaking changes (external audience)
- **Repository changelog**: Bug fixes, refactoring, tool updates (internal team)
- **Release notes**: Current release only - no future plans or speculation
- **README template**: Variables `{VERSION}`, `{TIMESTAMP}`, `{PACKAGE_TYPE}` get filled automatically

## Release Process

### 1. Pre-Release Updates
- [ ] Update `releases/PACKAGE-CHANGELOG.md` with user-visible changes
- [ ] Create `releases/vX.Y.Z/RELEASE-NOTES.md` with version summary
- [ ] Update `releases/README-template.md` if package structure changed

### 2. Validation
- [ ] Run YAML validation scripts
- [ ] Test with pnut_ts compiler
- [ ] Verify schema compliance

### 3. Generate & Publish
- [ ] Run `python3 engineering/tools/update-p2-reference-json.py X.Y.Z` (generates big JSON file)
- [ ] Run `python3 engineering/tools/generate-ai-reference-from-yaml.py X.Y.Z` (packages for release)
- [ ] Verify packages contain correct CHANGELOG.md and README.md
- [ ] Create GitHub release using `releases/vX.Y.Z/RELEASE-NOTES.md`
- [ ] Attach generated packages

### 4. Post-Release
- [ ] Update repository `CHANGELOG.md` with development cycle summary
- [ ] Archive previous version

## Release Packages
Three packages generated automatically:
- `p2-ai-reference-vX.Y.Z.tar.gz` - AI consumption (instructions, manifests, schemas)
- `p2-knowledge-core-vX.Y.Z.tar.gz` - Complete knowledge base (all YAMLs, concepts)
- `p2-learning-vX.Y.Z.tar.gz` - Human documentation (tutorials, examples)

Each package gets: README.md (from template), CHANGELOG.md (from package changelog), VERSION file

## Quality Gates
Before release:
1. Coverage must not decrease
2. All YAML files validate
3. Schema compliance verified
4. No broken internal references
5. Package changelog updated

## Data Flow
```
YAML sources → generate-ai-reference-from-yaml.py → deliverables/ai-reference/vX.Y.Z/
           ↘                                      ↗
            releases/PACKAGE-CHANGELOG.md -------→ All packages get CHANGELOG.md
            releases/README-template.md ----------→ All packages get README.md
            releases/vX.Y.Z/RELEASE-NOTES.md ----→ GitHub release notes
```

## Outstanding Decision
**WORKFLOW MISMATCH (v1.3.0+)**: GitHub workflow generates its own changelog from manual input instead of using our centralized control files. This creates duplicate work and potential inconsistencies.

**Options**:
1. Update GitHub workflow to read centralized control files
2. Deprecate centralized files and use GitHub workflow exclusively  
3. Maintain both systems (current approach)

**Impact**: For v1.2.0 we used existing workflow. Future releases need this resolved.

---
*Updated: 2025-09-14*