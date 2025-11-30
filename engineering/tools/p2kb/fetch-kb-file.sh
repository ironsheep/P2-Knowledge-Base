#!/bin/bash
# P2 Knowledge Base Fetch Script v3.1
# Key-based access to YAML content, with special handling for manifest files
# Usage: ./fetch-kb-file.sh <key|manifest-path> [--verbose]

set -e

BASE_URL="https://raw.githubusercontent.com/IronSheepProductionsLLC/P2-Knowledge-Base/main"
CACHE_DIR="${P2KB_CACHE:-$HOME/.p2kb-cache}"
INDEX_FILE="$CACHE_DIR/p2kb-index.json"
INDEX_MAX_AGE=86400  # 24 hours in seconds

# Special manifest paths - always fetched fresh (no caching, no key lookup)
MANIFEST_ROOT="manifests/propeller-knowledge-root.yaml"
MANIFEST_AI="manifests/ai-instructions.yaml"

VERBOSE=0
ARG=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --verbose|-v) VERBOSE=1; shift ;;
        -*) echo "Unknown option: $1" >&2; exit 1 ;;
        *) ARG="$1"; shift ;;
    esac
done

if [[ -z "$ARG" ]]; then
    echo "Usage: $0 <key|manifest-path> [--verbose]" >&2
    echo "Examples:" >&2
    echo "  $0 p2kbPasm2Mov                              # Fetch by key" >&2
    echo "  $0 manifests/propeller-knowledge-root.yaml   # Fetch root manifest (always fresh)" >&2
    echo "  $0 manifests/ai-instructions.yaml            # Fetch AI instructions (always fresh)" >&2
    exit 1
fi

log() { [[ $VERBOSE -eq 1 ]] && echo "[INFO] $*" >&2; }

# Ensure cache directory exists
mkdir -p "$CACHE_DIR"

# =============================================================================
# Special handling for manifest files - always fetch fresh, no caching
# =============================================================================
if [[ "$ARG" == "$MANIFEST_ROOT" || "$ARG" == "$MANIFEST_AI" ]]; then
    log "Manifest file detected: $ARG (fetching fresh, no cache)"
    curl -sS "$BASE_URL/$ARG"
    exit 0
fi

# =============================================================================
# Standard key-based access for all other content
# =============================================================================
KEY="$ARG"

# Check if index needs refresh
refresh_index() {
    local need_refresh=0

    if [[ ! -f "$INDEX_FILE" ]]; then
        log "Index not found, downloading..."
        need_refresh=1
    else
        local age=$(($(date +%s) - $(stat -c %Y "$INDEX_FILE" 2>/dev/null || stat -f %m "$INDEX_FILE")))
        if [[ $age -gt $INDEX_MAX_AGE ]]; then
            log "Index is ${age}s old (max ${INDEX_MAX_AGE}s), refreshing..."
            need_refresh=1
        fi
    fi

    if [[ $need_refresh -eq 1 ]]; then
        log "Downloading index from $BASE_URL/deliverables/ai/p2kb-index.json.gz"
        curl -sS "$BASE_URL/deliverables/ai/p2kb-index.json.gz" | gunzip > "$INDEX_FILE.tmp"
        mv "$INDEX_FILE.tmp" "$INDEX_FILE"
        log "Index updated: $(jq -r '.system.total_entries' "$INDEX_FILE") entries"
    fi
}

# Look up key in index
lookup_key() {
    local key="$1"

    # Try jq first (fast, reliable)
    if command -v jq &>/dev/null; then
        jq -r ".files[\"$key\"].path // empty" "$INDEX_FILE"
    else
        # Fallback to grep/sed (no jq dependency)
        grep -o "\"$key\":{\"path\":\"[^\"]*\"" "$INDEX_FILE" | sed 's/.*"path":"\([^"]*\)".*/\1/'
    fi
}

# Filter metadata from YAML content
# These fields are process/lineage metadata, not content
filter_metadata() {
    grep -v -E "^[[:space:]]*(last_updated|enhancement_source|documentation_source|documentation_level|manual_extraction_date):"
}

# Main execution
refresh_index

PATH_IN_REPO=$(lookup_key "$KEY")

if [[ -z "$PATH_IN_REPO" ]]; then
    echo "Error: Key '$KEY' not found in index" >&2
    echo "Hint: Keys start with 'p2kb' followed by category and name" >&2
    echo "Example keys: p2kbPasm2Mov, p2kbArchCog, p2kbSpin2Pinwrite" >&2
    exit 1
fi

log "Key: $KEY -> $PATH_IN_REPO"

# Check cache
CACHE_FILE="$CACHE_DIR/content/$(echo "$KEY" | tr '/' '_').yaml"
mkdir -p "$(dirname "$CACHE_FILE")"

# Fetch if not cached
if [[ ! -f "$CACHE_FILE" ]]; then
    log "Fetching: $BASE_URL/$PATH_IN_REPO"
    curl -sS "$BASE_URL/$PATH_IN_REPO" | filter_metadata > "$CACHE_FILE.tmp"
    mv "$CACHE_FILE.tmp" "$CACHE_FILE"
    log "Cached to: $CACHE_FILE"
fi

# Output content
cat "$CACHE_FILE"
