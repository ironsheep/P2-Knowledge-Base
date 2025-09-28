# P2 Knowledge Base - Manifest Path Standard

## The 4-Key System

All manifest files SHALL use only these four keys for path references:

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

## Keys That Are DEPRECATED

These keys SHALL NOT be used for path references:
- ❌ `path:` - Ambiguous, replace with `manifest:` or `content:`
- ❌ `file:` - Old pattern, replaced with `content:`
- ❌ `location:` - Informational only, not a real reference
- ❌ `yaml_path:` - Legacy pattern, replace with appropriate key
- ❌ `url:` - For web references only, not local files
- ❌ `base_path:` - Ambiguous, replaced with `manifest_base:` and `content_base:`

## Sections to IGNORE During Validation

These sections are informational and should NOT be processed as file references:
- `related_manifests:` - Cross-references for human readers
- `notes:` - Documentation
- `description:` - Human-readable text
- Any field with `*` wildcards (glob patterns)

## Benefits of This Standard

1. **Self-contained**: Each manifest has all info needed to resolve paths
2. **Unambiguous**: Clear distinction between manifest and content references  
3. **Simple**: Just concatenate base + reference
4. **Context-free**: External Claude instances don't need conversation history
5. **Efficient**: Reduces repetition with base paths
6. **Maintainable**: Clear rules, easy to validate

## Migration Notes

- Priority 1: Fix `pasm2-manifest.yaml` (376 files)
- Priority 2: Fix other high-traffic manifests
- Priority 3: Update validation script to enforce standard
- Priority 4: Remove all deprecated keys