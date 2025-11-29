# P2KB Download-On-Demand v3.0 Sprint Plan

**Sprint Name**: DOD v3.0 - Key-Based Access Migration
**Created**: 2025-11-28
**Status**: READY (all decisions finalized)

---

## Executive Summary

Replace the current path-based Download-On-Demand system with a key-based system that eliminates path construction errors, reduces token overhead, and provides automatic version checking - all deployed via a single atomic commit.

### The Problem

1. **Remote AIs fail at path construction** → 404 errors → give up
2. **Version checking requires downloading full YAML** → inefficient
3. **YAML files contain non-informational overhead** → wasted tokens
4. **Cached content is deeply outdated** → defects propagate

### The Solution

1. **Single global index** (`p2kb-index.json`) containing all keys, paths, versions
2. **Key-based access** - Remote AI requests by key, never constructs paths
3. **Atomic switchover** - One commit replaces entire system
4. **Forced migration** - Root manifest tells remote AIs to rebootstrap

---

## Research Findings

### YAML File Analysis

| Metric | Value |
|--------|-------|
| Total YAML files | 2,836 |
| Unique base filenames | 1,685 |
| Duplicate filenames | 577 (20%) |
| True collision risk | 41 files |
| Safe duplicates (copies/drafts) | 536 files |

**Collision Categories:**
- **PASM2 vs Spin2** (36 files): Same instruction names in different languages
  - Examples: `abs.yaml`, `debug.yaml`, `call.yaml`, `wrpin.yaml`
  - Resolution: Keys include language prefix (e.g., `p2kbPasm2Abs`, `p2kbSpin2Abs`)

- **Architecture vs Support** (5 files): Different content, same names
  - `cog.yaml`, `cordic.yaml`, `locks.yaml`, `smart_pins.yaml`, `streamer.yaml`
  - Resolution: Consolidate to single canonical source OR disambiguate keys

**Canonical Locations:**
- `engineering/knowledge-base/P2/` → Primary source (indexed)
- `deliverables/` → Published copies (NOT indexed - derived)
- `engineering/ingestion/` → Working drafts (NOT indexed - temporary)
- `manifests/` → Navigation files (replaced by index)

### Manifest Analysis

| Metric | Current System |
|--------|----------------|
| Total manifest files | 45 |
| Total size | 340 KB |
| Estimated tokens | ~57,000 |
| Largest manifest | obex-unified-index.yaml (48 KB) |

**What Manifests Provide:**
1. Navigation & discovery (hierarchical entry points)
2. Categorization & organization
3. Version tracking & metadata
4. Content path mapping
5. AI integration guidance (keywords, triggers)
6. Quick-query mappings (50+ questions → solutions)

**Replacement Strategy:**
All manifest functionality absorbed into single `p2kb-index.json`

### Index Size Estimation

| Metric | Current (Manifests) | Proposed (Index) | Savings |
|--------|---------------------|------------------|---------|
| Raw size | 340 KB | 44 KB | 87% |
| Gzipped | ~136 KB | ~18 KB | 87% |
| Files | 45 | 1 | 98% |
| Token count | ~57,000 | ~4,500 | 92% |
| HTTP requests | 45 (worst case) | 1 | 98% |

### YAML Metadata Reduction

| Field | Files Affected | Tokens/File | Total Savings |
|-------|----------------|-------------|---------------|
| `last_updated` | 1,073 | ~10 | 10,730 |
| `enhancement_source` | 1,207 | ~12 | 14,484 |
| `documentation_source` | 1,247 | ~8 | 9,976 |
| `documentation_level` | 1,264 | ~2 | 2,528 |
| **Total** | | | **~37,748 tokens** |

**What Stays in YAML Files:**
- `instruction`/`method`/`variable` - Unique identifiers
- `syntax`, `encoding` - Operational definitions
- `description`, `parameters`, `examples` - Core content
- `category`, `related`, `see_also` - Cross-references

**What Moves to Index:**
- Version numbers
- Last updated timestamps
- Source references
- Documentation level indicators

---

## Repository Structure (New)

### Deliverables Tree

```
/deliverables/
├── ai/                              # AI consumption (DOD system)
│   ├── p2kb-index.json.gz           # Compressed master index (~18 KB)
│   ├── P2/
│   │   ├── architecture/
│   │   ├── language/
│   │   │   ├── pasm2/
│   │   │   └── spin2/
│   │   ├── community/
│   │   └── guides/
│   └── P1/                          # Future
│
├── reference/                       # Rich Markdown (for humans)
│   ├── README.md                    # Index of reference topics
│   └── P2/
│       ├── README.md                # Index of P2 references
│       ├── architecture/
│       │   └── README.md            # Index of architecture topics
│       ├── language/
│       │   └── README.md            # Index of language topics
│       └── smart-pins/
│           └── README.md            # Index of smart pin topics
│
├── documents/                       # Generated PDFs (flat)
│   ├── README.md                    # Index of available documents
│   ├── P2-PASM-deSilva-Style.pdf
│   ├── P2-Smart-Pins-Tutorial.pdf
│   └── [future PDFs]
```

### Engineering Tree (Internal Only)

```
/engineering/
├── ingestion/                       # Source document processing
│   ├── sources/                     # Raw source documents
│   └── extracted/                   # Extraction work
├── tools/                           # Build scripts, generators
├── operations/                      # Sprints, planning, ops docs
└── document-production/             # Manual generation workspace
```

### Key Paths

| Purpose | Path |
|---------|------|
| Compressed index | `/deliverables/ai/p2kb-index.json.gz` |
| AI content root | `/deliverables/ai/P2/` |
| Human reference | `/deliverables/reference/P2/` |
| Generated PDFs | `/deliverables/documents/` |

### File Move

```bash
# Single command moves entire knowledge base
git mv engineering/knowledge-base deliverables/ai
```

---

## System Architecture

### Current System (v2.x)

```
Remote AI Session Start:
1. Fetch propeller-knowledge-root.yaml
2. Compare hash → if different, fetch ai-instructions.yaml
3. Use cached fetch-kb-file.sh script
4. Construct paths from manifest hierarchy
5. Fetch content files

Problems:
- Path construction is error-prone (manifest_base + content_base + path)
- Must understand "manifest self-containment" rule
- Multiple manifest traversals for single file
- No efficient version checking
- Cached scripts never update
```

### New System (v3.0)

```
Remote AI Session Start:
1. Fetch propeller-knowledge-root.yaml
2. See migration_required: true → tell human to rebootstrap
3. Human runs: rm -rf .p2kb-cache/ && re-bootstrap

After Rebootstrap:
1. Fetch p2kb-index.json (one file, everything)
2. Look up key → get path + version
3. Fetch file: base_url + path
4. Cache with version number
5. Next session: re-fetch index, compare versions, refresh stale

Benefits:
- Zero path construction (key lookup only)
- Single index has all versions
- One HTTP request to know everything
- Simple fetch script (~15 lines)
```

### Index File Design

```json
{
  "system": {
    "version": "3.0",
    "generated": "2025-11-28T00:00:00Z",
    "base_url": "https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/",
    "content_base": "deliverables/ai",
    "total_entries": 972
  },

  "files": {
    "p2kbPasm2Mov": {
      "path": "P2/language/pasm2/mov.yaml",
      "mtime": 1732780800,
      "cat": "pasm2"
    },
    "p2kbSpin2Abs": {
      "path": "P2/language/spin2/methods/abs.yaml",
      "mtime": 1732780800,
      "cat": "spin2"
    },
    "p2kbPasm2Abs": {
      "path": "P2/language/pasm2/abs.yaml",
      "mtime": 1732780800,
      "cat": "pasm2"
    },
    "p2kbArchCog": {
      "path": "P2/architecture/cog.yaml",
      "mtime": 1732780800,
      "cat": "arch"
    }
  },

  "path_exceptions": {
    "case-sensitivity.yaml": "p2kbFundCaseSensitivity",
    "identifier-rules.yaml": "p2kbFundIdentifierRules",
    "event_system.yaml": "p2kbArchEventSystem",
    "dira-dirb-registers.yaml": "p2kbArchRegDiraDirb"
  },

  "categories": {
    "pasm2_instruction": {
      "count": 362,
      "description": "PASM2 assembly instructions",
      "keys": ["p2kbPasm2Mov", "p2kbPasm2Add", "..."]
    },
    "spin2_method": {
      "count": 135,
      "description": "Spin2 built-in methods",
      "keys": ["p2kbSpin2Abs", "..."]
    },
    "smart_pin_mode": {
      "count": 32,
      "description": "Smart Pin operating modes",
      "keys": ["p2kbSmartPin00000", "..."]
    },
    "architecture": {
      "count": 18,
      "description": "P2 system architecture components",
      "keys": ["p2kbArchCog", "p2kbArchHub", "..."]
    },
    "obex_object": {
      "count": 113,
      "description": "OBEX community objects",
      "keys": ["p2kbObexFullDuplexSerial", "..."]
    }
  },

  "quick_queries": {
    "blink_led": ["p2kbPatternBlinkLed", "p2kbSpin2Pinwrite"],
    "uart_serial": ["p2kbObexFullDuplexSerial", "p2kbSmartPin00100"],
    "i2c": ["p2kbObexI2cDriver", "p2kbSmartPin10000"]
  }
}
```

### Key Naming Convention

**Format**: `p2kb` + Category + Name (CamelCase)

| Current Path | Key | Notes |
|--------------|-----|-------|
| `language/pasm2/mov.yaml` | `p2kbPasm2Mov` | Language prefix for disambiguation |
| `language/spin2/methods/abs.yaml` | `p2kbSpin2Abs` | Spin2 vs PASM2 |
| `language/pasm2/abs.yaml` | `p2kbPasm2Abs` | PASM2 vs Spin2 |
| `architecture/cog.yaml` | `p2kbArchCog` | Short category prefix |
| `architecture/smart-pins/mode-00000.yaml` | `p2kbSmartPin00000` | Mode number |
| `community/obex/jm-fullduplex.yaml` | `p2kbObexFullDuplexSerial` | Descriptive name |

**Collision Prevention:**
- PASM2 instructions: `p2kbPasm2{Name}`
- Spin2 methods: `p2kbSpin2{Name}`
- Architecture: `p2kbArch{Name}`
- Smart Pins: `p2kbSmartPin{ModeNumber}`
- OBEX: `p2kbObex{DescriptiveName}`
- Patterns: `p2kbPattern{Name}`

### Migration Trigger

**In `propeller-knowledge-root.yaml`:**

```yaml
version: "3.0"
last_updated: "2025-11-28"

# ═══════════════════════════════════════════════════════════════════════
# MIGRATION REQUIRED
# ═══════════════════════════════════════════════════════════════════════
migration:
  required: true
  from_version: "2.x"
  to_version: "3.0"

  reason: |
    The P2 Knowledge Base has been completely rebuilt with:
    • Key-based access (eliminates 404 errors from path construction)
    • Automatic version checking (always fresh content)
    • Corrected content (major defects fixed in all YAML files)

    YOUR CACHED CONTENT IS DEEPLY OUTDATED AND CONTAINS DEFECTS.

  human_action_required: |
    ══════════════════════════════════════════════════════════════════
    TELL YOUR HUMAN USER:

    "The P2 Knowledge Base requires a one-time migration.
     Your cached scripts and data are outdated.

     Please run:
       rm -rf .p2kb-cache/

     Then re-bootstrap following:
       https://github.com/ironsheep/P2-Knowledge-Base/blob/main/CLAUDE-QUICKSTART.md

     This takes 2 minutes. The new system is simpler and more reliable."

    DO NOT PROCEED WITH OLD CACHED DATA.
    ══════════════════════════════════════════════════════════════════

# After migration, normal access:
index:
  file: "p2kb-index.json"
  description: "Complete file index with keys, paths, and versions"
```

### New Fetch Script (v3.0)

**`fetch-kb-file.sh`** (~50 lines with compressed index + metadata filtering):

```bash
#!/bin/bash
# P2 Knowledge Base Fetcher v3.0 - Key-based access with metadata filtering
# Usage: fetch-kb-file.sh <key> [--verbose]

key=$1
verbose=${2:-""}
cache=".p2kb-cache"
index="$cache/p2kb-index.json"
base_url="https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main"
index_url="$base_url/deliverables/ai/p2kb-index.json.gz"
content_base="$base_url/deliverables/ai"

report() { [ "$verbose" = "--verbose" ] && echo "P2KB: $1" >&2; }

# Filter out non-essential metadata fields to reduce token overhead
filter_metadata() {
    grep -v -E "^[[:space:]]*(last_updated|enhancement_source|documentation_source|documentation_level):"
}

# Ensure index exists (refresh if older than 24 hours)
if [ ! -f "$index" ] || [ $(find "$index" -mmin +1440 2>/dev/null) ]; then
    report "Fetching compressed index..."
    mkdir -p "$cache"
    curl -sS "$index_url" | gunzip > "$index"
fi

# Look up key → path
if command -v jq &>/dev/null; then
    path=$(jq -r ".files[\"$key\"].path // empty" "$index")
else
    # Fallback for systems without jq
    path=$(grep -o "\"$key\"[^}]*\"path\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" "$index" | \
           sed 's/.*"path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')
fi

if [ -z "$path" ]; then
    echo "P2KB: ERROR: Unknown key '$key'" >&2
    echo "P2KB: Use 'jq keys .files' on p2kb-index.json to see available keys" >&2
    exit 1
fi

report "Key '$key' → $path"

# Fetch file (with caching and metadata filtering)
file_cache="$cache/$path"
if [ -f "$file_cache" ]; then
    report "Using cached: $file_cache"
    cat "$file_cache"
else
    report "Downloading: $path"
    mkdir -p "$(dirname "$file_cache")"
    # Download, filter metadata, then cache
    curl -sS "$content_base/$path" | filter_metadata > "$file_cache"
    cat "$file_cache"
fi
```

**Key Features:**
1. **Compressed index** - Downloads gzipped index (~18 KB vs 44 KB)
2. **Key-based lookup** - No path construction by remote AI
3. **Metadata filtering** - Strips `last_updated`, `enhancement_source`, etc. on download
4. **New paths** - Content from `/deliverables/ai/P2/`
5. **Local caching** - Same `.p2kb-cache/` structure as before
6. **Index auto-refresh** - Re-fetches index if older than 24 hours
7. **jq fallback** - Works even without jq installed

### New AI Instructions (v3.0)

**Simplified `ai-instructions.yaml`:**

```yaml
# P2 Knowledge Base - AI Instructions v3.0
# Key-based access system

version: "3.0"
last_updated: "2025-11-28"

setup_instructions: |
  ## P2 Knowledge Base Setup (2 minutes)

  ### Step 1: Create cache directory
  ```bash
  mkdir -p .p2kb-cache
  ```

  ### Step 2: Download fetch script
  ```bash
  curl -sS https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/engineering/tools/p2kb/fetch-kb-file.sh \
    -o .p2kb-cache/fetch-kb-file.sh
  chmod +x .p2kb-cache/fetch-kb-file.sh
  ```

  ### Step 3: Fetch the index
  ```bash
  bash .p2kb-cache/fetch-kb-file.sh p2kbIndex --verbose
  ```

  Done! You can now fetch any file by key.

usage: |
  ## Using the Knowledge Base

  ### Fetch by Key
  ```bash
  # Fetch a PASM2 instruction
  bash .p2kb-cache/fetch-kb-file.sh p2kbPasm2Mov

  # Fetch architecture documentation
  bash .p2kb-cache/fetch-kb-file.sh p2kbArchCog

  # Fetch a Smart Pin mode
  bash .p2kb-cache/fetch-kb-file.sh p2kbSmartPin00000
  ```

  ### Find Keys
  The index file contains all available keys:
  ```bash
  # List all keys
  jq 'keys' .p2kb-cache/p2kb-index.json

  # Find keys by category
  jq '.categories.pasm2_instruction.keys' .p2kb-cache/p2kb-index.json

  # Search for a key
  jq '.files | keys | map(select(contains("Mov")))' .p2kb-cache/p2kb-index.json
  ```

  ### Check for Updates
  The index contains version numbers for all files:
  ```bash
  # Check version of a file
  jq '.files["p2kbPasm2Mov"].version' .p2kb-cache/p2kb-index.json
  ```

  To refresh: delete .p2kb-cache/p2kb-index.json (re-fetched automatically)

categories: |
  ## Available Categories

  | Category | Count | Key Prefix | Description |
  |----------|-------|------------|-------------|
  | pasm2_instruction | 362 | p2kbPasm2 | PASM2 assembly instructions |
  | spin2_method | 135 | p2kbSpin2 | Spin2 built-in methods |
  | smart_pin_mode | 32 | p2kbSmartPin | Smart Pin operating modes |
  | architecture | 18 | p2kbArch | P2 system architecture |
  | obex_object | 113 | p2kbObex | Community OBEX objects |
  | pattern | 44 | p2kbPattern | Code patterns |
  | hardware | 30 | p2kbHw | Hardware boards & modules |
```

---

## Implementation Tasks

### Phase 0: Repository Restructure (10 min)

| Task | Description | Time |
|------|-------------|------|
| 0.1 | Move knowledge base: `git mv engineering/knowledge-base deliverables/ai` | 2 min |
| 0.2 | Delete `P2-support/components/` entirely (auto-generated, redundant - 6 YAMLs + extractor script) | 2 min |
| 0.3 | Create `deliverables/reference/` structure (empty + READMEs) | 3 min |
| 0.4 | Create `deliverables/documents/README.md` | 3 min |

**Deliverable**: New repository structure with content in `/deliverables/ai/P2/`

### Phase 1: Index Generation (1.5 hours)

| Task | Description | Time |
|------|-------------|------|
| 1.1 | Write `generate-p2kb-index.py` script | 45 min |
| 1.2 | Walk all YAML in `deliverables/ai/P2/` | (in script) |
| 1.3 | Generate keys using naming convention | (in script) |
| 1.4 | Handle collisions (PASM2/Spin2 disambiguation) | (in script) |
| 1.5 | Extract versions from files (or default to 1.0) | (in script) |
| 1.6 | Generate category groupings | (in script) |
| 1.7 | Convert `quick-queries-manifest.yaml` to standalone YAML file (key: `p2kbGuideQuickQueries`) | 15 min |
| 1.8 | Run script, validate output | 30 min |
| 1.9 | Compress index: `gzip -k p2kb-index.json` | 1 min |

**Deliverable**: `deliverables/ai/p2kb-index.json.gz` (~18 KB)

### Phase 2: Metadata Filtering (Two Approaches)

#### Option A: Filter on Download (RECOMMENDED - Immediate, Zero File Changes)

The fetch script filters out metadata fields when downloading YAML files:

```bash
# In fetch-kb-file.sh - filter metadata on download
# NOTE: Use specific top-level keys only to avoid accidental content collisions
# These are metadata fields that appear at root level of YAML files
filter_metadata() {
    # Remove non-essential metadata fields before caching
    # Pattern: start of line, optional whitespace, exact key name, colon
    grep -v -E "^[[:space:]]*(last_updated|enhancement_source|documentation_source|documentation_level):"
}

# Use in download:
curl -sS "$url" | filter_metadata > "$file_cache"
```

**IMPORTANT**: The filter must be key-specific to avoid accidental collisions with content. For example, if a description field contained "documentation_level" as text, we don't want to filter that line. The pattern `^[[:space:]]*key:` ensures we only match YAML keys at the start of lines.

| Task | Description | Time |
|------|-------------|------|
| 2.1 | Add `filter_metadata` function to fetch script | 10 min |
| 2.2 | Test filtering preserves valid YAML | 10 min |

**Benefits:**
- Zero changes to source YAML files
- Immediate token reduction on every download
- Can adjust filter list without modifying YAMLs
- Backwards compatible (source files unchanged)

**Deliverable**: Filtered downloads (~37,748 tokens saved at consumption time)

#### Option B: Source File Cleanup (DEFERRED - Future Sprint)

Permanently remove metadata from source files:

| Task | Description | Time |
|------|-------------|------|
| 2.1 | Write `cleanup-yaml-metadata.py` script | 30 min |
| 2.2 | Remove: `last_updated`, `enhancement_source`, `documentation_source`, `documentation_level` | (in script) |
| 2.3 | Run on all PASM2 files (1,207 files) | 15 min |
| 2.4 | Validate YAML still parses | 15 min |

**When to do Option B:**
- When we want cleaner source files
- When metadata is definitively not needed anywhere
- Can be done in a future optimization sprint

**Recommendation**: Do Option A now (10 min), Option B later (1 hour)

#### Why Filter-on-Download is Superior

1. **Zero risk** - Source files untouched, can't break anything
2. **Instant rollback** - Remove filter from script if issues arise
3. **Flexible** - Can add/remove filtered fields anytime via script update
4. **Future-proof** - If we add new metadata later, just update filter list
5. **Saves 50 min** - No need to modify 1,207 files today
6. **Same token savings** - Remote AIs see filtered content regardless

### Phase 3: Scripts & Instructions (45 min)

| Task | Description | Time |
|------|-------------|------|
| 3.1 | Write new `fetch-kb-file.sh` (v3.0) | 15 min |
| 3.2 | Write new `fetch-kb-file.ps1` (v3.0) | 15 min |
| 3.3 | Write new `ai-instructions.yaml` (v3.0) | 15 min |

**Deliverable**: New fetch scripts and instructions

### Phase 4: Migration Trigger & Documentation Updates (45 min)

| Task | Description | Time |
|------|-------------|------|
| 4.1 | Update `propeller-knowledge-root.yaml` with migration block | 10 min |
| 4.2 | Update `CLAUDE-QUICKSTART.md` with new key-based bootstrap | 10 min |
| 4.3 | Update `AI-PROMPT-PATTERNS.md` - replace path-based examples with key-based | 10 min |
| 4.4 | Update `deliverables/ai-reference/auxiliary-guides/interaction/using-with-ai.md` | 15 min |

**Files requiring update**:
- `CLAUDE-QUICKSTART.md` - Primary bootstrap instructions (path-based → key-based)
- `AI-PROMPT-PATTERNS.md` - All path examples need key equivalents
- `deliverables/ai-reference/auxiliary-guides/interaction/using-with-ai.md` - Comprehensive AI guide

**Deliverable**: Migration trigger in root manifest + all AI documentation updated for v3.0

### Phase 5: Manifest Deletion (10 min)

| Task | Description | Time |
|------|-------------|------|
| 5.1 | Delete all manifest files in `manifests/P2/` | 5 min |
| 5.2 | Delete `manifests/obex/` directory | 2 min |
| 5.3 | Keep `ai-bootstrap-*.yaml` files (still needed for bootstrap) | 1 min |
| 5.4 | Keep `propeller-knowledge-root.yaml` (migration trigger) | 1 min |
| 5.5 | Keep `ai-instructions.yaml` (updated in Phase 3) | 1 min |

**Note**: Quick-queries conversion is handled in Phase 1 (task 1.7)

**Decisions:**
- Quick-queries becomes a fetchable content file at `deliverables/ai/P2/guides/quick-queries.yaml`
- All navigation manifests deleted (replaced by index)
- Bootstrap files retained for initial setup flow
- Root manifest retained with migration trigger

### Phase 6: Testing & Validation (45 min)

| Task | Description | Time |
|------|-------------|------|
| 6.1 | Test index generation completeness | 10 min |
| 6.2 | Test fetch script with 10 sample keys | 10 min |
| 6.3 | **Reference transformation verification** (see below) | 15 min |
| 6.4 | Test migration trigger message display | 5 min |
| 6.5 | Verify all YAML files still parse | 5 min |

#### 6.3 Reference Transformation Verification

**Purpose**: Prove that all cross-references in YAMLs can be transformed to valid keys.

**Script** (`verify-reference-transforms.sh`):
```bash
#!/bin/bash
# Verify all .yaml references transform to valid keys

index="deliverables/ai/p2kb-index.json"
failures=0

for file in deliverables/ai/P2/**/*.yaml; do
    # Extract all .yaml references from file
    refs=$(grep -oE '[a-zA-Z0-9_/."-]+\.yaml' "$file" | tr -d '"')

    for ref in $refs; do
        key=$(transform_reference "$ref")

        # Verify key exists in index
        if ! jq -e ".files[\"$key\"]" "$index" > /dev/null 2>&1; then
            echo "FAIL: $file references '$ref' → '$key' (not found)"
            ((failures++))
        fi
    done
done

if [ $failures -eq 0 ]; then
    echo "✓ All references resolve successfully"
    exit 0
else
    echo "✗ $failures references failed - add to path_exceptions"
    exit 1
fi
```

**Process**:
1. Run verification script
2. Any failures → add to `path_exceptions` in index
3. Re-run until zero failures
4. Zero failures = safe to deploy

### Phase 7: Commit & Deploy (5 min)

| Task | Description | Time |
|------|-------------|------|
| 7.1 | Stage all changes | 1 min |
| 7.2 | Commit with comprehensive message | 2 min |
| 7.3 | Push to main | 1 min |
| 7.4 | Verify live on GitHub | 1 min |

**Total Estimated Time**: ~4.5 hours (with Option A filtering approach)

| Phase | Time |
|-------|------|
| Phase 0: Repository Restructure | 10 min |
| Phase 1: Index Generation | 1.5 hours |
| Phase 2: Metadata Filtering (Option A) | 20 min |
| Phase 3: Scripts & Instructions | 45 min |
| Phase 4: Migration Trigger & Documentation Updates | 45 min |
| Phase 5: Manifest Deletion | 10 min |
| Phase 6: Testing & Validation | 45 min |
| Phase 7: Commit & Deploy | 5 min |
| **Total** | **~4.5 hours** |

---

## Decisions (Confirmed)

### 1. Key Format ✅
**Decision**: `p2kbPasm2Mov` (CamelCase)
- Most token-efficient
- No special characters
- Human-readable

### 2. Manifest Disposition ✅
**Decision**: Delete all manifests
- Under version control, can recover if needed
- Clean break, no legacy clutter
- Exception: Keep `ai-bootstrap-*.yaml` for initial setup

### 3. Index Location ✅
**Decision**: Root (`/p2kb-index.json`)
- Simplest URL
- Prominent location
- Easy to remember

### 4. Quick-Queries ✅
**Decision**: Convert to content file
- Move `quick-queries-manifest.yaml` → `engineering/knowledge-base/P2/guides/quick-queries.yaml`
- Key: `p2kbGuideQuickQueries`
- Remote AIs fetch when needed (not embedded in index)

### 5. Version Strategy
**Options:**
- A) Extract from existing YAML files where present
- B) Default all to "1.0", increment on future changes
- C) Use git commit date as version proxy

**Recommendation**: B - Clean slate, simple management

### 6. Category Granularity
**Options:**
- A) Broad categories (pasm2, spin2, arch, obex)
- B) Fine categories (pasm2_arithmetic, pasm2_branch, pasm2_memory, ...)
- C) Both (categories + subcategories)

**Recommendation**: C - Categories for browsing, subcategories for precision

### 7. Cross-Reference Transformation ✅
**Decision**: Algorithmic transformation + exceptions in index
- Fetch script transforms path references to keys on download
- Standard paths handled algorithmically (e.g., `language/pasm2/dirl.yaml` → `p2kbPasm2Dirl`)
- Bare filenames and ambiguous paths listed in `path_exceptions` section of index
- Verification script proves all references resolve before deploy
- No YAML modifications needed

### 8. Version Strategy ✅
**Decision**: Use git commit timestamp as version (mtime)
- Index stores `mtime` (seconds since epoch) for each file
- Derived from `git log -1 --format="%ct" -- filepath`
- Fetch script sets file mtime after download: `touch -d "@$mtime" "$file_cache"`
- Freshness check: compare cached file mtime vs index mtime
- No version fields needed in YAML files

**Edge Case: Users who clone the repo**
- Git does not preserve file modification times
- Cloned files get current timestamp, not original mtime
- **Not addressed in this sprint** - DOD users fetch via HTTP, not clone
- **Future solution if needed**: `fix-mtimes.sh` script that restores mtimes from git history:
  ```bash
  for file in deliverables/ai/P2/**/*.yaml; do
      mtime=$(git log -1 --format="%ct" -- "$file")
      touch -d "@$mtime" "$file"
  done
  ```

### 9. Architecture Collisions ✅
Files exist in two locations:
- `engineering/knowledge-base/P2/architecture/` (system design, 200-320 lines each)
- `engineering/knowledge-base/P2-support/components/` (auto-generated, 30-40 lines each)

**Affected files**: `cog.yaml`, `cordic.yaml`, `locks.yaml`, `smart_pins.yaml`, `streamer.yaml`

**Analysis (2025-11-28)**:
- `P2-support/components/*.yaml` files are auto-generated (timestamp: 2025-09-06)
- They are minimal summaries (6-10x smaller than architecture versions)
- All information exists in the larger `P2/architecture/` files
- Directory also contains the generator script (`architecture-extractor.py`)

**Decision**: Delete entire `P2-support/components/` directory
- Redundant auto-generated content
- No unique information to preserve
- Eliminates collision issue completely
- Added to Phase 0 task 0.2

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Index generation misses files | Low | High | Validate count matches known totals |
| Key collisions not caught | Low | Medium | Script detects and reports collisions |
| Remote AIs ignore migration message | Medium | Low | Message is explicit, action is simple |
| YAML cleanup breaks parsing | Low | High | Validate all files post-cleanup |
| PowerShell script issues | Medium | Low | Test on Windows before deploy |
| jq not available on some systems | Medium | Low | Fallback grep-based lookup in script |

---

## Success Metrics

| Metric | Before | After | Target |
|--------|--------|-------|--------|
| Path construction errors | Common | Zero | 0 errors |
| Files to fetch for version check | 45 | 1 | 1 file |
| Token overhead (manifests) | 57,000 | 4,500 | <5,000 |
| Token overhead (YAML metadata) | 37,748 | 0 | 0 |
| HTTP requests (worst case) | 45+ | 2 | <5 |
| Setup complexity | 6 steps | 3 steps | <5 steps |

---

## Post-Sprint Tasks (Future)

1. **Self-updating fetch script** - Script checks for updates, prompts user
2. **OBEX integration** - Include OBEX download helper in unified system
3. **Further metadata reduction** - Layer deduplication in instruction files
4. **Analytics** - Track which keys are most requested (if feasible)
5. **P1 Knowledge Base** - Apply same system when P1 content added

---

## Appendix A: Files to Create

| File | Size | Purpose |
|------|------|---------|
| `/p2kb-index.json` | ~44 KB | Global index |
| `/engineering/tools/p2kb/fetch-kb-file.sh` | ~1 KB | New fetch script (bash) |
| `/engineering/tools/p2kb/fetch-kb-file.ps1` | ~1 KB | New fetch script (PowerShell) |
| `/engineering/tools/generate-p2kb-index.py` | ~3 KB | Index generator |
| `/engineering/tools/cleanup-yaml-metadata.py` | ~2 KB | Metadata cleanup script |

## Appendix B: Files to Modify

| File | Change |
|------|--------|
| `/manifests/propeller-knowledge-root.yaml` | Add migration trigger |
| `/manifests/ai-instructions.yaml` | Complete rewrite for v3.0 |
| `/CLAUDE-QUICKSTART.md` | Update bootstrap instructions |
| 1,207 PASM2 YAML files | Remove metadata fields |

## Appendix C: Files to Deprecate/Move

| Current Location | New Location |
|------------------|--------------|
| `/manifests/P2/*.yaml` | `/manifests-deprecated/P2/*.yaml` |
| `/manifests/ai-bootstrap-*.yaml` | Keep (still needed for bootstrap) |

---

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2025-11-28 | Initial plan created from brainstorming session | Claude |
| 2025-11-28 | Resolved Decision #9 (architecture collisions) - delete P2-support/components entirely | Claude |
| 2025-11-28 | Status changed to READY | Claude |
| 2025-11-28 | Fixed task 1.7: quick-queries becomes standalone YAML file, not embedded in index | Claude |
| 2025-11-28 | Added key-specific filtering note to prevent content collisions | Claude |
| 2025-11-28 | Expanded Phase 4 to include all AI documentation files (3 total) | Claude |
