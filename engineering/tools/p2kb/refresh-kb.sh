#!/bin/bash
# P2 Knowledge Base Refresh Script v3.2
# Updates scripts, index, and common files with migration from v3.1 structure
# Usage: ./refresh-kb.sh [--verbose] [--force]

set -e

BASE_URL="https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main"

# Determine script's directory (where this script lives)
# tr -d '\r' strips any carriage returns that may have been introduced during download
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd | tr -d '\r')"

# Index and cache location (relative to script directory)
INDEX_DIR="${P2KB_INDEX:-$SCRIPT_DIR/.p2kb}"
INDEX_FILE="$INDEX_DIR/p2kb-index.json"
CACHE_DIR="$INDEX_DIR/cache"

VERBOSE=0
FORCE=0

# Parse arguments
for arg in "$@"; do
    case $arg in
        --verbose|-v) VERBOSE=1 ;;
        --force|-f) FORCE=1 ;;
    esac
done

log() { [[ $VERBOSE -eq 1 ]] && echo "[INFO] $*" >&2; }
status() { echo "✓ $*" >&2; }
error() { echo "✗ $*" >&2; }
warn() { echo "⚠ $*" >&2; }

# =============================================================================
# Migration: Detect and migrate from v3.1 structure
# =============================================================================
migrate_old_structure() {
    local old_index="$SCRIPT_DIR/p2kb-index.json"
    local old_content="$SCRIPT_DIR/content"
    local migrated=0

    # Check for old index in script directory (v3.1 layout)
    if [[ -f "$old_index" ]]; then
        warn "Detected v3.1 layout - migrating to v3.2..."

        # Ensure new directories exist
        mkdir -p "$INDEX_DIR"
        mkdir -p "$CACHE_DIR"

        # Move index file
        if [[ ! -f "$INDEX_FILE" ]] || [[ $FORCE -eq 1 ]]; then
            log "Moving index to $INDEX_FILE"
            mv "$old_index" "$INDEX_FILE"
            status "Migrated index"
            migrated=1
        else
            log "Index already exists at new location, removing old"
            rm -f "$old_index"
        fi
    fi

    # Check for old content directory
    if [[ -d "$old_content" ]]; then
        # Move cached content files
        shopt -s nullglob
        local files=("$old_content"/*.yaml)
        shopt -u nullglob

        if [[ ${#files[@]} -gt 0 ]]; then
            log "Moving ${#files[@]} cached files to $CACHE_DIR"
            for f in "${files[@]}"; do
                local basename=$(basename "$f")
                if [[ ! -f "$CACHE_DIR/$basename" ]] || [[ $FORCE -eq 1 ]]; then
                    mv "$f" "$CACHE_DIR/"
                else
                    rm -f "$f"  # Already exists, remove old
                fi
            done
            status "Migrated ${#files[@]} cached files"
            migrated=1
        fi

        # Remove old content directory if empty
        rmdir "$old_content" 2>/dev/null || true
    fi

    # Clean up any stray old files
    rm -f "$SCRIPT_DIR/index.json" 2>/dev/null || true

    if [[ $migrated -eq 1 ]]; then
        echo "" >&2
        echo "Migration complete! Index and cache now stored in:" >&2
        echo "  $INDEX_DIR (hidden)" >&2
        echo "" >&2
    fi
}

# =============================================================================
# Directory Setup
# =============================================================================
ensure_directories() {
    mkdir -p "$SCRIPT_DIR"
    mkdir -p "$SCRIPT_DIR/obex"
    mkdir -p "$INDEX_DIR"
    mkdir -p "$CACHE_DIR"
}

# =============================================================================
# Main
# =============================================================================

echo "P2 Knowledge Base Refresh v3.2" >&2
echo "==============================" >&2

# Ensure all directories exist
ensure_directories

# Check for and migrate old structure
migrate_old_structure

# =============================================================================
# Step 1: Update all scripts (including this one)
# =============================================================================
echo "" >&2
echo "Updating scripts..." >&2

# Fetch script
log "Downloading fetch-kb-file.sh"
curl -sS "$BASE_URL/engineering/tools/p2kb/fetch-kb-file.sh" > "$SCRIPT_DIR/fetch-kb-file.sh.tmp"
mv "$SCRIPT_DIR/fetch-kb-file.sh.tmp" "$SCRIPT_DIR/fetch-kb-file.sh"
chmod +x "$SCRIPT_DIR/fetch-kb-file.sh"
status "fetch-kb-file.sh"

# Refresh script (self-update)
log "Downloading refresh-kb.sh"
curl -sS "$BASE_URL/engineering/tools/p2kb/refresh-kb.sh" > "$SCRIPT_DIR/refresh-kb.sh.tmp"
mv "$SCRIPT_DIR/refresh-kb.sh.tmp" "$SCRIPT_DIR/refresh-kb.sh"
chmod +x "$SCRIPT_DIR/refresh-kb.sh"
status "refresh-kb.sh"

# OBEX helper
log "Downloading obex/download-helper.sh"
curl -sS "$BASE_URL/engineering/tools/p2kb/obex/download-helper.sh" > "$SCRIPT_DIR/obex/download-helper.sh.tmp"
mv "$SCRIPT_DIR/obex/download-helper.sh.tmp" "$SCRIPT_DIR/obex/download-helper.sh"
chmod +x "$SCRIPT_DIR/obex/download-helper.sh"
status "obex/download-helper.sh"

# =============================================================================
# Step 2: Refresh index (to hidden location)
# =============================================================================
echo "" >&2
echo "Updating index..." >&2

log "Downloading p2kb-index.json.gz"
curl -sS "$BASE_URL/deliverables/ai/p2kb-index.json.gz" > "$INDEX_FILE.tmp.gz"
gunzip -c "$INDEX_FILE.tmp.gz" > "$INDEX_FILE.tmp"
mv "$INDEX_FILE.tmp" "$INDEX_FILE"
rm -f "$INDEX_FILE.tmp.gz"

# Get entry count and category count
if command -v jq &>/dev/null; then
    ENTRIES=$(jq -r '.system.total_entries' "$INDEX_FILE")
    CATEGORIES=$(jq -r '.system.total_categories // 0' "$INDEX_FILE")
    if [[ "$CATEGORIES" != "0" && "$CATEGORIES" != "null" ]]; then
        status "p2kb-index.json ($ENTRIES entries, $CATEGORIES categories)"
    else
        status "p2kb-index.json ($ENTRIES entries)"
    fi
else
    status "p2kb-index.json"
fi

# =============================================================================
# Step 3: Refresh common getting-started files
# =============================================================================
echo "" >&2
echo "Updating common files..." >&2

# List of commonly-needed files to pre-cache
COMMON_KEYS=(
    "p2kbGuideQuickQueries"
    "p2kbGuideSpin2GettingStarted"
    "p2kbGuidePasm2GettingStarted"
)

# Function to look up key in index
lookup_key() {
    local key="$1"
    if command -v jq &>/dev/null; then
        jq -r ".files[\"$key\"].path // empty" "$INDEX_FILE"
    else
        grep -o "\"$key\":{\"path\":\"[^\"]*\"" "$INDEX_FILE" | sed 's/.*"path":"\([^"]*\)".*/\1/'
    fi
}

# Filter metadata from YAML content
filter_metadata() {
    grep -v -E "^[[:space:]]*(last_updated|enhancement_source|documentation_source|documentation_level|manual_extraction_date):"
}

for key in "${COMMON_KEYS[@]}"; do
    path=$(lookup_key "$key")
    if [[ -n "$path" ]]; then
        log "Fetching $key -> $path"
        cache_file="$CACHE_DIR/${key}.yaml"
        curl -sS "$BASE_URL/$path" | filter_metadata > "$cache_file.tmp"
        mv "$cache_file.tmp" "$cache_file"
        status "$key"
    else
        error "$key (not found in index)"
    fi
done

# =============================================================================
# Step 4: Fetch reference files
# =============================================================================
echo "" >&2
echo "Updating reference files..." >&2

log "Downloading propeller-knowledge-root.yaml"
curl -sS "$BASE_URL/manifests/propeller-knowledge-root.yaml" > "$INDEX_DIR/propeller-knowledge-root.yaml"
status "propeller-knowledge-root.yaml"

log "Downloading ai-instructions.yaml"
curl -sS "$BASE_URL/manifests/ai-instructions.yaml" > "$INDEX_DIR/ai-instructions.yaml"
status "ai-instructions.yaml"

# =============================================================================
# Done
# =============================================================================
echo "" >&2
echo "Refresh complete!" >&2
echo "" >&2
echo "Scripts location: $SCRIPT_DIR" >&2
echo "Index/cache location: $INDEX_DIR (hidden)" >&2
echo "" >&2
echo "Usage:" >&2
echo "  $SCRIPT_DIR/fetch-kb-file.sh --help      Show all commands" >&2
echo "  $SCRIPT_DIR/fetch-kb-file.sh --browse    Browse by category" >&2
echo "  $SCRIPT_DIR/fetch-kb-file.sh --search    Search for keys" >&2
echo "  $SCRIPT_DIR/fetch-kb-file.sh <key>       Fetch content" >&2
