# Orphaned YAML Resolution Plan
Generated: 2025-09-27

## Executive Summary
280 orphaned YAML files need to be connected to the manifest hierarchy. These fall into two main categories:
1. **Manifest files** (62) - Already in manifests/ but not linked from parent manifests
2. **Content files** (218) - In engineering/knowledge-base/ but not referenced by any manifest

## Phase 1: Connect Orphaned Manifests (62 files)
**Goal**: Link all manifests in manifests/P2/ to their parent manifests

### Task 1: Fix p2-root.yaml References (7 manifests)
The p2-root.yaml itself is orphaned because propeller-knowledge-root.yaml needs updating.
- [ ] Update propeller-knowledge-root.yaml to properly reference P2/p2-root.yaml
- [ ] Ensure p2-root.yaml references all its child manifests:
  - hardware-manifest.yaml
  - patterns-manifest.yaml  
  - quick-queries-manifest.yaml
  - architecture-manifest.yaml
  - auxiliary-guides-manifest.yaml
  - smart-pins-manifest.yaml
  - code-examples-manifest.yaml

### Task 2: Fix Language Hierarchy (5 manifests)
- [ ] Ensure language-manifest.yaml is referenced from p2-root.yaml
- [ ] Connect language child manifests:
  - fundamentals-manifest.yaml
  - spin2-manifest.yaml
  - pasm2-manifest.yaml
  - spin2-conventions-manifest.yaml

### Task 3: Fix PASM2 Category References (16 manifests)
The PASM2 category manifests exist but validation shows they're "orphaned"
- [ ] Verify pasm2-manifest.yaml properly references all 16 category manifests
- [ ] Fix the validation script to recognize hierarchical references

### Task 4: Fix Community References (34 manifests)
- [ ] Ensure community-manifest.yaml is referenced from p2-root.yaml
- [ ] Verify obex-manifest.yaml is referenced from community-manifest.yaml
- [ ] Confirm all 24 author manifests are properly linked
- [ ] Confirm all 9 category manifests are properly linked

## Phase 2: Connect Orphaned Content Files (218 files)

### Task 5: Code Examples Integration (3 files)
Location: engineering/knowledge-base/P2/code-examples/
- [ ] Add these to code-examples-manifest.yaml:
  - smart-pins-001-basic-io.yaml
  - smart-pins-002-button-reading.yaml
  - code-example-schema.yaml

### Task 6: Language Fundamentals (4 files)
Location: engineering/knowledge-base/P2/language/fundamentals/
- [ ] Add these to fundamentals-manifest.yaml:
  - case-sensitivity.yaml
  - pasm-labels.yaml
  - identifier-rules.yaml
  - variable-scoping-best-practices.yaml

### Task 7: Spin2 Core Files (2 files)
Location: engineering/knowledge-base/P2/language/spin2/
- [ ] Create appropriate section in spin2-manifest.yaml for:
  - spin2-language-complete-map.yaml
  - spin2-language-schema.yaml

### Task 8: Spin2 System Variables (3 files)
Location: engineering/knowledge-base/P2/language/spin2/system-variables/
- [ ] Create system-variables section in spin2-manifest.yaml:
  - clkfreq.yaml
  - varbase.yaml
  - clkmode.yaml

### Task 9: Spin2 Patterns (44 files total)
- [ ] Create spin2-patterns-manifest.yaml with three categories:
  - Implementation patterns (15 files)
  - Application patterns (23 files)
  - Structural patterns (6 files)

### Task 10: Spin2 Assembly Directives (12 files)
Location: engineering/knowledge-base/P2/language/spin2/assembly-directives/
- [ ] Add assembly-directives section to spin2-manifest.yaml

### Task 11: Spin2 Special Symbols (12 files)
Location: engineering/knowledge-base/P2/language/spin2/special-symbols/
- [ ] Add special-symbols section to spin2-manifest.yaml

### Task 12: Spin2 Registers (25 files)
Location: engineering/knowledge-base/P2/language/spin2/registers/
- [ ] Create registers section in spin2-manifest.yaml

### Task 13: Spin2 Keywords & Statements (38 files)
- [ ] Add keywords section to spin2-manifest.yaml (36 keyword files)
- [ ] Add statements section (1 file: debug.yaml)

### Task 14: Spin2 Debug Displays (8 files)
Location: engineering/knowledge-base/P2/language/spin2/debug-displays/
- [ ] Add debug-displays section to spin2-manifest.yaml

### Task 15: Spin2 Concepts & Conventions (4 files)
- [ ] Add concepts section (1 file: inline_pasm2.yaml)
- [ ] Link conventions to spin2-conventions-manifest.yaml (3 files)

### Task 16: PASM2 Additional Instructions (17 files)
Location: engineering/knowledge-base/P2/language/pasm2/
Files like true.yaml, alignl.yaml, fit.yaml, negx.yaml
- [ ] Determine which category manifest each belongs to
- [ ] Add to appropriate category manifests

### Task 17: PASM2 Patterns & Idioms (9 files)
- [ ] Create pasm2-patterns section in pasm2-manifest.yaml:
  - 2 implementation patterns
  - 5 idiom files
  - Link to existing groups (7 files)

### Task 18: PASM2 Concepts (17 files)
Location: engineering/knowledge-base/P2/language/pasm2/concepts/
- [ ] Create concepts section in pasm2-manifest.yaml

### Task 19: Architecture Files (3 files)
Location: engineering/knowledge-base/P2/architecture/
- [ ] Add to architecture-manifest.yaml:
  - smart_pin_patterns.yaml
  - multi_resource_management.yaml
  - click_module_integration.yaml

### Task 20: System Registers (3 files)
Location: engineering/knowledge-base/P2/architecture/system-registers/
- [ ] Add these to registers-manifest.yaml:
  - complete-system-registers-index.yaml
  - dira-dirb-registers.yaml
  - ptra-register.yaml

### Task 21: Architecture Pattern Analysis (8 files)
Location: engineering/knowledge-base/P2/architecture/patterns-analysis/
- [ ] Create patterns-analysis section in architecture-manifest.yaml

### Task 22: Resolve Misplaced Manifest
- [ ] Move engineering/knowledge-base/P2/architecture/smart-pins/smartpin_manifest.yaml to manifests/P2/architecture/
- [ ] Ensure it's referenced from architecture-manifest.yaml

### Task 23: OBEX Template
- [ ] Determine if _template.yaml should be referenced or is just a template file

## Phase 3: Validation & Cleanup

### Task 24: Update Validation Script
- [ ] Fix script to properly recognize all reference patterns
- [ ] Ensure it handles hierarchical manifests correctly

### Task 25: Final Validation
- [ ] Run validation to confirm 0 orphaned files
- [ ] Document any intentional exclusions (like template files)

## Success Metrics
- ✅ 0 orphaned YAML files (down from 280)
- ✅ All manifests properly connected in hierarchy
- ✅ Validation script passes with no warnings
- ✅ Every YAML file reachable from propeller-knowledge-root.yaml

## Estimated Tasks: 25
## Estimated Time: 3-4 hours

This plan systematically addresses every orphaned file, organizing them into logical groups and ensuring complete connectivity throughout the knowledge base hierarchy.