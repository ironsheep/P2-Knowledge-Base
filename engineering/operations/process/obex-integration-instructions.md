# OBEX Integration Instructions for AI Reference

## Purpose
Instructions for integrating OBEX search optimization into the main P2 AI reference that remote Claude instances download.

## Integration Points

### 1. Add to Main Reference JSON
The OBEX search strategy should be embedded in the main `p2-reference-complete.json` under a new section:

```json
{
  "obex_search_guidance": {
    "golden_rule": "Always search for 'OBEX objects' not specific types",
    "keyword_expansions": {
      // Include the full keyword mapping from the guide
    },
    "search_strategy": {
      "step1": "Search ALL objects with broad keywords",
      "step2": "Expand to related terms",
      "step3": "Check top authors for quality examples"
    }
  }
}
```

### 2. Modify OBEX Manifest Structure
Update `manifests/obex/obex-root.yaml` to include search hints:

```yaml
search_optimization:
  avoid_category_filtering: true
  reason: "Objects often miscategorized - drivers in misc, sensors in drivers"
  recommended_approach: "Search all objects, then filter results"
  keyword_expansions_available: true
  guide_location: "deliverables/ai-reference/guides/obex-search-optimization-guide.md"
```

### 3. Create Search Helper Function
Add a Python script for generating optimized search queries:

```python
# tools/obex-search-helper.py
def expand_search_terms(primary_term):
    """
    Expands a single search term into multiple related terms
    """
    expansions = {
        'i2c': ['i2c', 'iic', 'twi', 'two-wire', '2-wire'],
        'led': ['led', 'pixel', 'ws2812', 'rgb', 'neopixel', 'strip', 'matrix'],
        # ... etc
    }
    return expansions.get(primary_term.lower(), [primary_term])
```

### 4. Update AI Navigation Guide
Add to the existing AI navigation documents:

```markdown
## OBEX Object Discovery

**Critical**: When searching OBEX, never filter by category first.

### Correct Approach
1. Search across all 113 objects
2. Use expanded keyword sets
3. Present both direct matches and alternatives

### Common Pitfall
Assuming "driver" category contains all drivers - it doesn't!
- 49 objects in "drivers"
- 34 objects in "misc" (many are drivers)
- Drivers also appear in other categories
```

## Implementation Workflow

1. **Update manifests** - Add search guidance metadata
2. **Create helper tools** - Search expansion utilities
3. **Enhance documentation** - Add to AI guides
4. **Test with examples** - Verify improved discovery
5. **Package for distribution** - Include in next release

## Success Metrics

Before optimization:
- Searching "driver" → ~49 objects (missing 50+ relevant objects)
- Searching "I2C" → Limited results

After optimization:
- Searching "I2C" variants → All I2C-capable objects
- Broader results presented with relevance ranking

## Notes for Remote Claude

When remote Claude downloads the P2 reference, it should:
1. Load the keyword expansion mappings
2. Default to broad searches
3. Report comprehensive results
4. Explain why certain "unexpected" objects were included