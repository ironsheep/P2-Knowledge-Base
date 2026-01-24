# Sprint: pnut_ts Usage Guides → YAML Integration

**Created**: 2026-01-23
**Completed**: 2026-01-24
**Status**: COMPLETED
**Filter Tag**: `yaml_knowledge_base`

---

## Objective

Integrate 13 new usage guides (extracted from pnut_ts compiler study) into the P2 Knowledge Base YAML structure. Each guide contains **compiler-verified facts** that must enhance existing YAML definitions.

### Why This Matters

**YAMLs serve two critical purposes:**

1. **AI Code Generation**: A remote Claude Code reading these YAMLs must be able to generate correct P2 code without access to the original guides. The YAML must contain everything needed to use the feature correctly.

2. **Documentation Source Material**: YAMLs become the source of truth for generated documentation. Technical accuracy is paramount - errors propagate to all downstream documents.

### Deep Study Requirement

For each guide, we don't just "extract facts" - we deeply study the content to understand:
- What does a remote AI need to know to use this feature correctly?
- What are the common mistakes or misunderstandings?
- What cross-references help connect related concepts?
- What compiler-verified behaviors differ from assumptions?

The goal is YAMLs that enable correct code generation by an AI that has never seen the original guide.

---

## Source Material

**Location**: `engineering/ingestion/external-inputs/pnut_ts_facts/NEW/`

| # | Guide | Topic Area |
|---|-------|------------|
| 1 | Clock-Configuration-Usage-Guide.md | System setup, HUBSET, clock modes |
| 2 | Control-Flow-Usage-Guide.md | Branching, loops, conditionals |
| 3 | Error-Handling-Usage-Guide.md | Exception patterns, DEBUG |
| 4 | Floating-Point-Usage-Guide.md | Float operations, CORDIC |
| 5 | Lookup-Table-Usage-Guide.md | LUT operations, RDLUT/WRLUT |
| 6 | Multi-Cog-Usage-Guide.md | COGINIT, COGSTOP, synchronization |
| 7 | Operators-Usage-Guide.md | Spin2 operators, precedence |
| 8 | Pin-Operations-Usage-Guide.md | Smart Pins, WRPIN/WXPIN/WYPIN |
| 9 | Preprocessor-Usage-Guide.md | #define, #ifdef, conditionals |
| 10 | Random-Number-Usage-Guide.md | GETRND, xoroshiro |
| 11 | Spin2-Object-Patterns-Guide.md | OBJ, method calls, inheritance |
| 12 | String-Constants-Usage-Guide.md | String handling, STRING() |
| 13 | Timing-Operations-Usage-Guide.md | WAITX, GETCT, timing patterns |

---

## Per-Guide Workflow

For each guide, execute this sequence:

### Phase 1: Deep Read & Analysis
1. Read the usage guide thoroughly
2. Extract key facts, patterns, and compiler-verified behaviors
3. Identify which YAML files are affected (instructions, concepts, methods)
4. Note any new cross-references needed

### Phase 2: YAML Gap Analysis
1. Read each affected YAML file
2. Compare guide content against existing YAML content
3. Identify:
   - Missing information that should be added
   - Existing information that needs correction/enhancement
   - New cross-references to add
   - New concept files needed (if any)

### Phase 3: YAML Updates
1. Edit YAML files with new/corrected content
2. **Keep YAMLs concise** - add value, not verbosity
3. Add cross-references using full paths
4. Validate cross-references: `python3 engineering/tools/validate-crossref-keys.py`

### Phase 4: Commit Guide Changes
1. Stage and commit YAML changes for this guide
2. Use descriptive commit message referencing the guide

---

## Task Structure

Create one MCP task per guide for systematic iteration:

```
Task 1: Process Clock-Configuration-Usage-Guide.md
Task 2: Process Control-Flow-Usage-Guide.md
Task 3: Process Error-Handling-Usage-Guide.md
Task 4: Process Floating-Point-Usage-Guide.md
Task 5: Process Lookup-Table-Usage-Guide.md
Task 6: Process Multi-Cog-Usage-Guide.md
Task 7: Process Operators-Usage-Guide.md
Task 8: Process Pin-Operations-Usage-Guide.md
Task 9: Process Preprocessor-Usage-Guide.md
Task 10: Process Random-Number-Usage-Guide.md
Task 11: Process Spin2-Object-Patterns-Guide.md
Task 12: Process String-Constants-Usage-Guide.md
Task 13: Process Timing-Operations-Usage-Guide.md
Task 14: Execute 7-Step YAML Release
```

---

## Final Release: 7-Step YAML Release Process

After all 13 guides are processed:

```bash
# Step 1: Already done - YAML edits complete

# Step 2: Validate all cross-references
python3 engineering/tools/validate-crossref-keys.py

# Step 3: Final commit if any remaining changes
git add deliverables/ai/P2/
git commit -m "Complete pnut_ts usage guide YAML integration"

# Step 4: Regenerate index
python3 engineering/tools/generate-p2kb-index.py

# Step 5: Regenerate JSON reference
python3 engineering/tools/update-p2-reference-complete.py

# Step 6: Compress and commit outputs
gzip -kf deliverables/ai/p2kb-index.json
git add deliverables/ai/p2kb-index.json deliverables/ai/p2kb-index.json.gz
git add deliverables/ai-reference/p2-reference.json
git commit -m "Regenerate index and JSON after pnut_ts guide integration"

# Step 7: Pre-release validation
python3 engineering/tools/validate-dod-release.py --verbose
```

---

## YAML Update Guidelines

### Keep It Concise
- Add facts, not filler
- One clear sentence per concept
- Avoid redundancy with existing content
- Use bullet points for lists

### Cross-Reference Format
```yaml
# Use full paths for reliable resolution:
related:
  - language/pasm2/waitx.yaml
  - language/spin2/methods/waitms.yaml
  - architecture/timing/clock_modes.yaml
```

### What to Add
- Compiler-verified behaviors not in current YAML
- Practical usage patterns from guides
- Edge cases and gotchas
- Cross-references between related concepts

### What NOT to Add
- Verbose explanations (guides are the verbose source)
- Duplicate information already in YAML
- Speculative content not in the guide
- Tutorial-style content (that's for manuals)

---

## Target YAML Locations

| Category | Path |
|----------|------|
| PASM2 Instructions | `deliverables/ai/P2/language/pasm2/` |
| Spin2 Methods | `deliverables/ai/P2/language/spin2/methods/` |
| Spin2 Operators | `deliverables/ai/P2/language/spin2/operators/` |
| Spin2 Constructs | `deliverables/ai/P2/language/spin2/constructs/` |
| Architecture | `deliverables/ai/P2/architecture/` |
| Concepts | `deliverables/ai/P2/language/pasm2/concepts/` |

---

## Success Criteria

- [x] All 13 guides processed
- [x] Cross-reference validation: 100% resolution (2,326 references)
- [x] DOD release validation: PASS
- [x] Index and JSON regenerated (1,027 entries, 633 elements)
- [x] All changes committed with clear messages

---

## Notes

- **Source fidelity**: Guide content is compiler-verified; trust it
- **Incremental commits**: Commit after each guide (not all at once)
- **No rushing**: Quality over speed
- **Ask if unclear**: Some guide content may need interpretation

---

*Sprint created: 2026-01-23*
*Reference: engineering/procedures/yaml-workflow-quick-guide.md*
