# P2 Knowledge Base - Path Reference Standard

**Version:** 2.0
**Updated:** 2025-10-20
**Scope:** All YAML files (manifests AND content files)

## The 4-Key System

All YAML files (manifests and content) SHALL use only these four keys for path references:

### 1. `manifest_base:` (optional)
- **Purpose**: Define base path for all manifest references in this file
- **Value**: Full path including `/manifests/` prefix
- **Example**: `/manifests/P2/language`

### 2. `content_base:` (optional)
- **Purpose**: Define base path for all content references in this file
- **Value**: Full path including `/engineering/knowledge-base/P2/` prefix
- **Example**: `/engineering/knowledge-base/P2/language/pasm2`

### 3. `manifest:` 
- **Purpose**: Reference another manifest file
- **Value**: Filename or relative path that gets appended to `manifest_base`
- **Resolution**: `{manifest_base}/{manifest}` or if no base: full path from `/manifests/`
- **Example**: `"pasm2-manifest.yaml"` → `/manifests/P2/language/pasm2-manifest.yaml`

### 4. `content:`
- **Purpose**: Reference a knowledge base content file
- **Value**: Filename or relative path that gets appended to `content_base`
- **Resolution**: `{content_base}/{content}` or if no base: full path from `/engineering/knowledge-base/P2/`
- **Example**: `"abs.yaml"` → `/engineering/knowledge-base/P2/language/pasm2/abs.yaml`

## Path Resolution Algorithm (Simple!)

```python
def resolve_path(base, reference):
    if base:
        return f"{base}/{reference}"
    else:
        # Reference must be full path from appropriate root
        return reference
```

## Example Manifest Using Standard

```yaml
# manifests/P2/language/pasm2-manifest.yaml
version: "2.0.0"
schema_version: "2024-12-30"

# Define bases once at the top
manifest_base: "/manifests/P2/language"
content_base: "/engineering/knowledge-base/P2/language/pasm2"

# Reference other manifests
related:
  - manifest: "spin2-manifest.yaml"          # → /manifests/P2/language/spin2-manifest.yaml
  - manifest: "fundamentals-manifest.yaml"   # → /manifests/P2/language/fundamentals-manifest.yaml

# Reference content files  
categories:
  - name: "Math Operations"
    items:
      - content: "abs.yaml"    # → /engineering/knowledge-base/P2/language/pasm2/abs.yaml
      - content: "add.yaml"    # → /engineering/knowledge-base/P2/language/pasm2/add.yaml
      - content: "sub.yaml"    # → /engineering/knowledge-base/P2/language/pasm2/sub.yaml
```

## Content Files (Non-Manifest YAML)

Content files (getting-started, concepts, conventions, etc.) follow the same 4-key standard as manifests.

### Within-Hierarchy References (Primary Pattern)

Content files SHOULD reference other files within the same hierarchy using `content_base`:

```yaml
# engineering/knowledge-base/P2/language/spin2/conventions/spin2-getting-started.yaml
title: Spin2 Getting Started
content_base: "/engineering/knowledge-base/P2/language/spin2"

knowledge_progression:
  immediate_next_steps:
    REQUIRED:
      - name: "Basic I/O Concepts"
        content: "concepts/basic-io.yaml"  # → /engineering/knowledge-base/P2/language/spin2/concepts/basic-io.yaml

    RECOMMENDED:
      - name: "Formatting Standards"
        content: "conventions/spin2-formatting-standards.yaml"  # Same hierarchy

see_also:
  - concepts/inline_pasm2.yaml
  - operators/precedence.yaml
```

**Design Principle:** Content should primarily reference files within its own hierarchy. This keeps knowledge domains cohesive and reduces coupling.

### Cross-Hierarchy References (Secondary Pattern - Use Sparingly)

When a content file MUST reference outside its hierarchy, use absolute paths from repository root:

```yaml
# engineering/knowledge-base/P2/language/pasm2/conventions/pasm2-getting-started.yaml
content_base: "/engineering/knowledge-base/P2/language/pasm2"

knowledge_progression:
  THEN_CHOOSE:
    - name: "Smart Pin Modes"
      content: "/engineering/knowledge-base/P2/architecture/smart_pins.yaml"  # Cross-hierarchy - absolute path!
```

**Validation Behavior:**
- ✅ Within-hierarchy refs (using content_base): Silent success
- ⚠️ Cross-hierarchy refs (absolute paths): **WARNING** - Flagged as refactoring opportunity
- ❌ Relative paths with `../`: **ERROR** - Forbidden pattern

**Design Goal:** Cross-hierarchy references indicate architectural coupling. Track these as refactoring opportunities. Example: `smart_pins.yaml` should be split into language-specific versions.

### Sections That Contain File References

These sections in content files MUST be validated:

- `knowledge_progression` - Learning path references
- `immediate_next_steps` - Next content to read
- `REQUIRED` / `RECOMMENDED` / `THEN_CHOOSE` - Subsections of progression
- `see_also` - Related content links
- `next_steps` - Progressive learning paths
- `related_content` - Cross-references (if present)
- `essential_reading` - Must-read content
- `advanced_features` - Advanced topic links

### Sections to IGNORE (Informational Only)

These sections are documentation and should NOT be processed as file references:

- `related_manifests` - Human-readable cross-references
- `notes` - Documentation text
- `description` - Human-readable descriptions
- `summary` - Descriptive text
- `examples` - Code examples (may contain file paths as strings)
- Any field containing `*` wildcards (glob patterns for documentation)

## Forbidden Patterns

### ❌ ERRORS (Block Release):

**Relative Paths with Parent Directory:**
```yaml
# FORBIDDEN - Will cause validation ERROR
content: "../architecture/smart_pins.yaml"
content: "../../hardware/pins.yaml"
```
**Why forbidden:** Path resolution is ambiguous, breaks with file moves, violates content_base standard.

**Fix:** Use absolute path for cross-hierarchy, or content_base for within-hierarchy.

**Deprecated Keys:**
- ❌ `path:` - Ambiguous, replace with `manifest:` or `content:`
- ❌ `file:` - Old pattern, replaced with `content:`
- ❌ `location:` - Informational only, not a real reference
- ❌ `yaml_path:` - Legacy pattern, replace with appropriate key
- ❌ `url:` - For web references only, not local files
- ❌ `base_path:` - Ambiguous, replaced with `manifest_base:` and `content_base:`

### ⚠️ WARNINGS (Refactoring Opportunities):

**Cross-Hierarchy Absolute Paths:**
```yaml
# WARNING - Allowed but flagged for refactoring
content: "/engineering/knowledge-base/P2/architecture/smart_pins.yaml"
```
**Why warned:** Indicates architectural coupling between hierarchies. Track for future refactoring.

**Refactoring strategy:** Split cross-hierarchy content into hierarchy-specific versions (e.g., `language/spin2/smart-pins.yaml`, `language/pasm2/smart-pins.yaml`)

## Validation Requirements

The validation script (`verify-manifest-linkages.py`) MUST:

### Scope:
1. Process ALL manifest files in `/manifests/` hierarchy
2. Process ALL content files in `/engineering/knowledge-base/P2/` hierarchy
3. Validate file references in both manifests AND content files

### Error Conditions (Block Release):
- ❌ Referenced file does not exist
- ❌ Relative path using `../` pattern
- ❌ Missing `content_base` when using relative paths within hierarchy
- ❌ Deprecated keys (`path:`, `file:`, `base_path:`)
- ❌ Broken path resolution (content_base + content doesn't exist)

### Warning Conditions (List for Refactoring):
- ⚠️ Cross-hierarchy absolute path (e.g., language→architecture)
- ⚠️ Multiple references to same cross-hierarchy file (high coupling)

### Output Format:

**Errors:**
```
❌ ERRORS FOUND: 3
  File: pasm2-getting-started.yaml:31
  Issue: Relative path with '../' (forbidden)
  Path: ../architecture/smart_pins.yaml
```

**Warnings:**
```
⚠️ WARNINGS (Refactoring Opportunities): 5

Cross-Hierarchy References:
  1. pasm2-getting-started.yaml:31
     → /engineering/knowledge-base/P2/architecture/smart_pins.yaml
     Source: language/pasm2 → architecture

  2. spin2-advanced-concepts.yaml:45
     → /engineering/knowledge-base/P2/architecture/smart_pins.yaml
     Source: language/spin2 → architecture

Refactoring Suggestion: Consider creating language-specific versions:
  - language/pasm2/concepts/smart-pins.yaml
  - language/spin2/concepts/smart-pins.yaml
```

**Release Gate:** Errors = 0 (warnings may be non-zero)

## Benefits of This Standard

1. **Self-contained**: Each manifest has all info needed to resolve paths
2. **Unambiguous**: Clear distinction between manifest and content references  
3. **Simple**: Just concatenate base + reference
4. **Context-free**: External Claude instances don't need conversation history
5. **Efficient**: Reduces repetition with base paths
6. **Maintainable**: Clear rules, easy to validate

## Implementation Checklist

### Phase 1: Documentation & Validation (Current)
- [x] Define 4-key standard for manifests
- [x] Extend standard to cover content files
- [x] Define error vs warning criteria
- [x] Specify validation output format
- [ ] Update validation script to implement requirements
- [ ] Run validation to identify all issues

### Phase 2: Error Remediation (Blocks Release)
- [ ] Fix all relative `../` paths to absolute or content_base
- [ ] Add missing `content_base` declarations
- [ ] Remove all deprecated keys
- [ ] Verify all referenced files exist
- [ ] Re-run validation until errors = 0

### Phase 3: Warning Review (Refactoring Backlog)
- [ ] Document all cross-hierarchy references
- [ ] Prioritize refactoring opportunities by coupling count
- [ ] Create hierarchy-specific versions of shared content (e.g., smart_pins.yaml)
- [ ] Track warning reduction over releases

### Phase 4: Continuous Enforcement
- [ ] Add validation to CI/CD pipeline
- [ ] Require validation pass before merge
- [ ] Monitor warning trends in release notes