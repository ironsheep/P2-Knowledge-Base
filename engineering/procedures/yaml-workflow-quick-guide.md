# YAML Workflow Quick Guide

**Purpose**: Quick reference for YAML knowledge base changes (DOD v3.0 compliant)

**Filter Tag**: `yaml_knowledge_base`

---

## The 7-Step Sequence

```
1. EDIT → 2. VALIDATE → 3. COMMIT YAML → 4. REGENERATE INDEX → 5. REGENERATE JSON → 6. COMMIT OUTPUTS → 7. VALIDATE RELEASE
```

**Why this order matters**:
- Index uses git commit timestamps. Commit YAML first = accurate timestamps.
- JSON reference must stay in sync with YAML source of truth.

---

## Step-by-Step

### Step 1: Make YAML Changes
Edit files in `deliverables/ai/P2/` using Edit tool or filesystem MCP.

### Step 2: Validate Cross-References
```bash
python3 engineering/tools/validate-crossref-keys.py
```
- Must show **100% resolution rate** before proceeding
- If failures: fix YAML content (not the index)

#### Cross-Reference Best Practices

**Use full paths** in `related:` fields for reliable resolution:
```yaml
# CORRECT - full path resolves reliably:
related:
  - language/spin2/methods/exp.yaml
  - language/spin2/operators/op_POW.yaml
  - language/spin2/constructs/inline_pasm.yaml

# FRAGILE - bare names may not resolve:
related:
  - EXP      # Validator may not find correct key
  - POW      # Ambiguous without path context
```

**Never remove references** - they were intended to refer to something:
- If target file doesn't exist, find where that concept IS documented
- Reference that file instead of deleting the reference
- Example: `END` has no standalone file, but is documented in `inline_pasm.yaml`

**Why this matters**: The index generator and validator use different key transformation logic. Full paths bypass this inconsistency and ensure 100% resolution.

### Step 3: Commit YAML Changes
```bash
git add deliverables/ai/P2/path/to/changed.yaml
git commit -m "Description of YAML changes"
```

### Step 4: Regenerate Index
```bash
python3 engineering/tools/generate-p2kb-index.py
```

### Step 5: Regenerate JSON Reference
```bash
python3 engineering/tools/update-p2-reference-complete.py
```
This rebuilds `deliverables/ai-reference/p2-reference.json` from all YAML sources.

### Step 6: Compress and Commit Outputs
```bash
gzip -kf deliverables/ai/p2kb-index.json
git add deliverables/ai/p2kb-index.json deliverables/ai/p2kb-index.json.gz
git add deliverables/ai-reference/p2-reference.json
git commit -m "Regenerate index and JSON reference after YAML changes"
```

### Step 7: Pre-Release Validation (optional but recommended)
```bash
python3 engineering/tools/validate-dod-release.py --verbose
```

---

## Copy-Paste Quick Reference

```bash
# Complete workflow after editing YAMLs:
python3 engineering/tools/validate-crossref-keys.py
git add deliverables/ai/P2/ && git commit -m "YAML changes"
python3 engineering/tools/generate-p2kb-index.py
python3 engineering/tools/update-p2-reference-complete.py
gzip -kf deliverables/ai/p2kb-index.json
git add deliverables/ai/p2kb-index.json* deliverables/ai-reference/p2-reference.json
git commit -m "Update index and JSON reference"
```

---

## Pre-Release Validation

Before pushing to live:
```bash
python3 engineering/tools/validate-dod-release.py --verbose
```

Validates: index integrity, gzip correctness, file paths, orphans, naming conventions, timestamps, metadata filtering, cross-references, fetch script parity.

**Incremental mode** (faster, changes only):
```bash
python3 engineering/tools/validate-dod-release.py --incremental
```

---

## Metadata Fields Filtered by Fetch Scripts

These 5 fields are process/lineage info, filtered out for consumers:
- `last_updated`
- `enhancement_source`
- `documentation_source`
- `documentation_level`
- `manual_extraction_date`

If adding new metadata fields, update both fetch scripts and the validator.

---

## Tools Reference

| Tool | Purpose |
|------|---------|
| `validate-crossref-keys.py` | Check all cross-references resolve |
| `generate-p2kb-index.py` | Regenerate master index |
| `update-p2-reference-complete.py` | Regenerate JSON from all YAMLs |
| `validate-dod-release.py` | Pre-release comprehensive check |

---

## Two Output Files

| File | Location | Purpose |
|------|----------|---------|
| `p2kb-index.json` | `deliverables/ai/` | Index/manifest for AI discovery |
| `p2-reference.json` | `deliverables/ai-reference/` | Complete JSON collection of all YAML data |

Both must be regenerated when YAML content changes to maintain consistency.

---

*For complete methodology details, see the DOD release validator source code.*
