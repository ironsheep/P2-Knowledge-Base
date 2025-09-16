# P2 Pattern Reorganization Plan

## Current Situation Analysis

### What We Have

1. **Architecture Patterns** (`/architecture/patterns/`)
   - 8 comprehensive pattern files derived from analyzing 730 source files
   - Each file contains:
     - Statistical prevalence (e.g., "38.5% of files use cog_management")
     - Detailed selection criteria
     - Implementation templates
     - Resource profiles
     - Composition rules
     - Real examples from the codebase
   - Files average 200+ lines of detailed analysis

2. **Spin2 Hardware Patterns** (`/language/spin2/patterns/hardware_utilization/`)
   - 8 minimal implementation snippets
   - Each file contains:
     - Basic "when to use" list
     - Simple code implementation
     - Resource notes
   - Files average 15-20 lines

3. **Spin2 Other Patterns** (`/language/spin2/patterns/`)
   - `domain_patterns/` - 23 application-level patterns (motor_controller, sensor_reader, etc.)
   - `object_composition/` - 6 patterns for object structure
   - `specialized/` - 7 advanced architectural patterns

### The Problem

1. **Misleading Naming**: Files with identical names (cog_management.yaml) in different locations serve completely different purposes
2. **No PASM2 Patterns**: Despite having 357 PASM2 instruction files, there are zero PASM2 patterns
3. **Mixed Abstraction Levels**: Spin2 patterns mix structural (object composition) with domain (motor controller) with implementation (buffer management)
4. **Unclear Hierarchy**: It's not clear whether to look in architecture/ or language/ for patterns

## Proposed Reorganization

### Design Principles

1. **Clear Separation**: Architecture = concepts/analysis, Language = implementation
2. **No Duplication**: Each pattern exists in exactly one location
3. **Language Parity**: Both Spin2 and PASM2 get pattern support
4. **Hierarchy**: Architecture → Patterns → Idioms (decreasing granularity)

### New Structure

```
/engineering/knowledge-base/P2/
├── architecture/
│   ├── patterns/                          # RENAMED: patterns-analysis/
│   │   ├── PATTERN-ANALYSIS-README.md     # Explains these are analysis results
│   │   ├── cog_management_analysis.yaml   # RENAMED from cog_management.yaml
│   │   ├── buffer_management_analysis.yaml
│   │   ├── memory_management_analysis.yaml
│   │   ├── protocol_implementation_analysis.yaml
│   │   ├── smart_pin_usage_analysis.yaml
│   │   ├── state_machine_analysis.yaml
│   │   ├── timing_control_analysis.yaml
│   │   └── asm_integration_analysis.yaml
│   │
│   └── (other architecture files...)
│
├── language/
│   ├── spin2/
│   │   ├── patterns/
│   │   │   ├── pattern_manifest.yaml
│   │   │   ├── structural/                # RENAMED from object_composition/
│   │   │   │   ├── no_objects.yaml
│   │   │   │   ├── single_object.yaml
│   │   │   │   ├── few_objects.yaml
│   │   │   │   ├── several_objects.yaml
│   │   │   │   └── framework_pattern.yaml
│   │   │   ├── implementation/            # MERGED hardware_utilization here
│   │   │   │   ├── spin2_cog_management.yaml
│   │   │   │   ├── spin2_buffer_management.yaml
│   │   │   │   ├── spin2_memory_allocation.yaml
│   │   │   │   ├── spin2_pin_control.yaml
│   │   │   │   ├── spin2_protocol_implementation.yaml
│   │   │   │   ├── spin2_state_machine.yaml
│   │   │   │   ├── spin2_timing_control.yaml
│   │   │   │   └── spin2_error_handling.yaml
│   │   │   └── applications/              # RENAMED from domain_patterns/
│   │   │       ├── display_driver.yaml
│   │   │       ├── sensor_reader.yaml
│   │   │       ├── motor_controller.yaml
│   │   │       └── (... 20 more application patterns)
│   │   │
│   │   └── idioms/                        # NEW - coming in next phase
│   │       └── idiom_manifest.yaml
│   │
│   └── pasm2/
│       ├── patterns/                      # NEW - needs creation
│       │   ├── pattern_manifest.yaml
│       │   └── implementation/
│       │       ├── pasm2_initialization.yaml
│       │       ├── pasm2_hub_synchronization.yaml
│       │       ├── pasm2_interrupt_handling.yaml
│       │       └── pasm2_cordic_usage.yaml
│       │
│       └── idioms/                        # NEW - coming in next phase
│           └── idiom_manifest.yaml
```

## Migration Steps

### Phase 1: Architecture Pattern Cleanup
1. Rename `/architecture/patterns/` to `/architecture/patterns-analysis/`
2. Rename all files to add `_analysis` suffix
3. Add README explaining these are statistical analysis results
4. Update any references in manifests

### Phase 2: Spin2 Pattern Reorganization
1. Rename `object_composition/` to `structural/`
2. Rename `domain_patterns/` to `applications/`
3. Move and rename `hardware_utilization/*.yaml` to `implementation/spin2_*.yaml`
4. Delete the now-empty `hardware_utilization/` directory
5. Move `specialized/` patterns to appropriate categories

### Phase 3: Create PASM2 Patterns
1. Create `/language/pasm2/patterns/` directory structure
2. Extract PASM2-specific patterns from the 730 source files
3. Create pattern_manifest.yaml for PASM2
4. Document common PASM2 implementation patterns

### Phase 4: Update Manifests
1. Update root_manifest.yaml with new paths
2. Update pattern-index.yaml files
3. Create new pattern_manifest.yaml files where needed
4. Update cross-references

### Phase 5: Documentation
1. Create migration guide showing old → new locations
2. Update any documentation referring to patterns
3. Add READMEs explaining the hierarchy

## Benefits of This Reorganization

1. **Clear Purpose**: 
   - Architecture = "38.5% of files use this pattern" (analysis)
   - Language = "Here's how to implement it" (code)

2. **No Confusion**: 
   - No more duplicate names
   - Clear path to find what you need

3. **Language Parity**: 
   - PASM2 gets equal treatment with patterns
   - Both languages ready for idioms

4. **AI-Friendly**:
   - Can load just analysis for understanding
   - Can load just implementation for code generation
   - Clear hierarchy for progressive loading

## Files to Create/Modify

### Create:
- `/architecture/patterns-analysis/PATTERN-ANALYSIS-README.md`
- `/language/pasm2/patterns/` (entire directory structure)
- `/language/pasm2/patterns/pattern_manifest.yaml`
- `/language/spin2/patterns/structural/` (rename from object_composition)
- `/language/spin2/patterns/implementation/` (merge hardware_utilization)
- `/language/spin2/patterns/applications/` (rename from domain_patterns)

### Modify:
- All files in `/architecture/patterns/` (rename with _analysis suffix)
- All files in `/language/spin2/patterns/hardware_utilization/` (rename with spin2_ prefix)
- `/engineering/knowledge-base/P2/root_manifest.yaml` (update paths)
- `/language/spin2/patterns/pattern-index.yaml` (update categories)

### Delete:
- `/language/spin2/patterns/hardware_utilization/` (after moving contents)
- `/language/spin2/patterns/specialized/` (after redistributing contents)

## Estimated Impact

- **Files affected**: ~70 pattern files
- **Manifests to update**: 3-4 files
- **New directories**: 5
- **Breaking changes**: Yes - all pattern references need updating

## Next Steps After Reorganization

1. **Idiom Extraction** (your original request):
   - With clean pattern structure, idioms have clear home
   - Can begin extracting from 730 source files
   - Both Spin2 and PASM2 idioms have designated locations

2. **Pattern Validation**:
   - Verify statistics in analysis files still accurate
   - Ensure implementation patterns compile
   - Cross-reference with source files

3. **Documentation**:
   - Create pattern usage guide
   - Document pattern → idiom relationship
   - Update AI consumption guidelines

## Timeline

1. **Hour 1**: Reorganize architecture patterns
2. **Hour 2**: Reorganize Spin2 patterns
3. **Hour 3**: Create PASM2 structure and initial patterns
4. **Hour 4**: Update all manifests and documentation

Then we can clear context and begin idiom extraction with a clean structure.

## Questions for User

1. Should we proceed with this reorganization?
2. Any concerns about breaking existing references?
3. Preference for PASM2 pattern extraction approach?
4. Should specialized patterns be redistributed or kept separate?