# P2 Knowledge Base Release Planning

## Version Numbering Scheme

### Semantic Versioning (MAJOR.MINOR.PATCH)

**MAJOR (X.0.0)** - Breaking changes
- Schema structure changes that break compatibility
- Major reorganization of knowledge structure
- Removal of previously published elements
- Changes to YAML/JSON structure format

**MINOR (0.X.0)** - Feature additions
- New instruction categories added
- New language elements (operators, keywords, etc.)
- New code examples or patterns
- Significant documentation expansions
- Coverage increases >10%

**PATCH (0.0.X)** - Fixes and minor updates
- Typo corrections
- Small documentation improvements
- Bug fixes in examples
- Minor metadata additions
- Coverage increases <10%

## Data Flow Architecture

### Primary Source: YAML Files
**Location**: `engineering/knowledge-base/P2/`
- All knowledge is maintained in YAML format
- Schema-validated, version-controlled
- Single source of truth

### Generated Deliverables
**Location**: `deliverables/ai-reference/vX.Y.Z/`
- Generated FROM YAML sources
- Never edited directly
- Regenerated for each release

### Generation Process
```bash
# Generate new release from YAML sources
python3 engineering/tools/generate-ai-reference-from-yaml.py 2.0.0

# This creates:
# - deliverables/ai-reference/v2.0.0/
# - All manifests, coverage reports
# - Organized YAML copies for distribution
```

## Release Packages

### Package 1: AI Reference Bundle (`p2-ai-reference-vX.Y.Z.tar.gz`)
**Purpose**: Complete AI-consumable knowledge for code generation

**Contents**:
```
p2-ai-reference-vX.Y.Z/
├── README.md                        # Package description & usage
├── VERSION                          # Version identifier
├── CHANGELOG.md                     # Changes in this release
├── manifests/
│   ├── instructions-manifest.json  # PASM2 instruction registry
│   ├── spin2-manifest.json         # Spin2 language elements
│   └── coverage-report.json        # Coverage statistics
├── instructions/
│   └── PASM2/
│       └── *.yaml                  # All PASM2 instruction definitions
├── language/
│   └── spin2/
│       ├── keywords/*.yaml
│       ├── operators/*.yaml
│       ├── methods/*.yaml
│       ├── registers/*.yaml
│       ├── debug-commands/*.yaml
│       └── assembly-directives/*.yaml
└── schemas/
    ├── instruction-schema.json
    ├── spin2-element-schema.json
    └── validation-rules.json
```

### Package 2: Knowledge Base Core (`p2-knowledge-core-vX.Y.Z.tar.gz`)
**Purpose**: Structured knowledge for advanced AI systems and tooling

**Contents**:
```
p2-knowledge-core-vX.Y.Z/
├── README.md                        # Package description & usage
├── VERSION                          # Version identifier
├── CHANGELOG.md                     # Changes in this release
├── P2/
│   ├── instructions/
│   │   └── **/*.yaml               # All instruction YAMLs
│   ├── language/
│   │   └── spin2/
│   │       └── **/*.yaml           # All Spin2 elements
│   ├── hardware/
│   │   └── *.yaml                  # Hardware descriptions
│   ├── code-examples/
│   │   └── *.yaml                  # Code patterns
│   └── concepts/
│       └── *.yaml                  # P2 concepts
└── schemas/
    └── *.yaml                       # All schema definitions
```

### Package 3: Learning Resources (`p2-learning-vX.Y.Z.tar.gz`)
**Purpose**: Human-readable documentation and tutorials

**Contents**:
```
p2-learning-vX.Y.Z/
├── README.md
├── VERSION
├── p2-handbook.md                  # Main learning document
├── tutorials/
│   └── *.md                        # Step-by-step tutorials
├── examples/
│   └── *.spin2                     # Working code examples
└── quick-reference/
    └── *.pdf                        # Quick reference cards
```

## Release Triggers

### Automatic Release Candidates (Monthly)
- First Monday of each month
- Accumulates all patches
- Version: Increment PATCH

### Manual Feature Releases
- New instruction categories
- Language element additions >20 items
- Version: Increment MINOR

### Manual Major Releases
- Schema changes
- Structure reorganization
- Version: Increment MAJOR

## Release Process

### 1. Pre-Release Validation
- [ ] Run validation scripts on all YAML files
- [ ] Verify manifest completeness
- [ ] Check schema compliance
- [ ] Generate coverage report
- [ ] Test with pnut_ts compiler

### 2. Version Bump
- [ ] Update VERSION file
- [ ] Update package.json (if exists)
- [ ] Tag commit with version

### 3. Generate Packages
- [ ] Run packaging workflow
- [ ] Generate checksums
- [ ] Create release notes

### 4. GitHub Release
- [ ] Create GitHub release
- [ ] Attach packages
- [ ] Publish release notes
- [ ] Update README with latest version

### 5. Post-Release
- [ ] Announce on forum
- [ ] Update OBEX references
- [ ] Archive previous version

## Version History Tracking

```
releases/
├── v2.0.0/
│   ├── release-notes.md
│   ├── packages/
│   └── checksums.txt
├── v2.1.0/
│   ├── release-notes.md
│   ├── packages/
│   └── checksums.txt
└── latest -> v2.1.0/
```

## Current State Assessment

**Current Version**: v2.0.0 (Proposed)
- Justification: Major increase from v1 due to 114% coverage increase
- SPIN2 language specification integration complete
- 287 total language elements (was 134)

**Next Release**: v2.1.0
- Target: After OBEX integration
- Expected: ~50 new code examples

## Release Artifact Naming Convention

```
p2-[component]-v[MAJOR].[MINOR].[PATCH].tar.gz
p2-[component]-v[MAJOR].[MINOR].[PATCH].zip
p2-[component]-v[MAJOR].[MINOR].[PATCH]-checksums.txt
```

Components:
- `ai-reference` - AI consumption package
- `knowledge-core` - Full knowledge base
- `learning` - Human documentation

## Quality Gates

Before any release:
1. Coverage must not decrease
2. All tests must pass
3. Schema validation must succeed
4. No broken internal references
5. Changelog must be updated

## Distribution Channels

1. **GitHub Releases** - Primary distribution
2. **OBEX** - Parallax official channel
3. **Direct Download** - From project website
4. **Package Managers** - Future consideration

---

*Last Updated: 2025-01-13*
*Next Review: After first release*