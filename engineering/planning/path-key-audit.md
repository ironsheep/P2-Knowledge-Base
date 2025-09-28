# Path Key Usage Audit - P2 Knowledge Base Manifests

## Current State: Multiple Conflicting Patterns

### Path-Related Keys Found (5 different keys):

1. **`path:`** (22 occurrences)
   - Used in manifest_registry for full paths
   - Used in auxiliary guides for documentation paths
   - Sometimes combined with `manifests:` list for subdirectory pattern
   - Example: `path: "manifests/P2/language/pasm2-manifest.yaml"`

2. **`manifest:`** (21 occurrences)  
   - Used for referencing other manifest files
   - Sometimes relative to current dir, sometimes with subdirs
   - Example: `manifest: "language/pasm2-manifest.yaml"`

3. **`content:`** (376+ occurrences in pasm2-manifest alone)
   - Used for referencing actual knowledge base YAML files
   - Full paths from repo root
   - Example: `content: engineering/knowledge-base/P2/language/pasm2/abs.yaml`

4. **`location:`** (2 occurrences)
   - Used informally for describing where patterns exist
   - Not an actual file reference that should be processed
   - Example: `location: "architecture/smart_pin_patterns.yaml"`

5. **`base_path:`** (5 occurrences)
   - Used to reduce repetition in paths
   - Applied as prefix to other references
   - Example: `base_path: "engineering/knowledge-base/P2/architecture/"`

### Additional Confusion Points:

- **`file:`** - Old pattern we just eliminated (was changed to `content:`)
- **`yaml_path:`** - Used in OBEX manifests (legacy pattern)
- **`url:`** - Sometimes appears but shouldn't be processed as local path
- **`related_manifests:`** - Informational only, but script processes them as real references

## Problems This Creates:

1. **Validation Script Confusion**: The script tries to be "smart" and process any `.yaml` string as a potential reference
2. **External System Complexity**: Must implement multiple path resolution algorithms
3. **Maintenance Nightmare**: Developers don't know which pattern to use
4. **False Errors**: Informational references get processed as missing files

## Proposed Solution: Two Keys, Two Contexts

### Standardize on ONLY these patterns:

```yaml
# For content files (always relative to /engineering/knowledge-base/P2/)
content: "language/pasm2/abs.yaml"

# For manifest files (always relative to /manifests/)  
manifest: "P2/language/pasm2-manifest.yaml"

# Optional: Use base_path to reduce repetition
base_path: "language/pasm2"  # Context determines if this is under manifests/ or knowledge-base/P2/
items:
  - content: "abs.yaml"       # Relative to base_path
  - content: "add.yaml"
```

### Keys to ELIMINATE:
- `path:` - Replace with either `manifest:` or `content:` based on context
- `location:` - This is just documentation, not a real reference
- `file:` - Already eliminated
- `yaml_path:` - Legacy OBEX pattern, should be migrated
- `url:` - Not for local file references

### Special Sections to IGNORE:
- `related_manifests:` - These are informational cross-references, not actual includes
- Comments or documentation sections

## Benefits of Standardization:

1. **Clear Semantics**: `manifest:` vs `content:` immediately tells you the file type
2. **Simple Validation**: Script knows exactly where to look based on key name
3. **No Ambiguity**: Two contexts, two keys, no confusion
4. **Easier Maintenance**: Developers know exactly which pattern to use
5. **Better Performance**: External systems need only two path resolution rules

## Next Steps:

1. ✅ Complete audit (this document)
2. Get agreement on standardization approach
3. Create migration scripts to update all manifests
4. Update validation script to enforce new pattern
5. Document in official guidelines
6. Test with external systems