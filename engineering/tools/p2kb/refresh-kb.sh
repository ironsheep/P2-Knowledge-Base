#!/bin/bash
# P2 Knowledge Base Refresh Script v1.0
# Refreshes all cached scripts, index, and common files
# Usage: ./refresh-kb.sh [--verbose]

set -e

BASE_URL="https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main"
CACHE_DIR="${P2KB_CACHE:-$HOME/.p2kb-cache}"

VERBOSE=0
[[ "$1" == "--verbose" || "$1" == "-v" ]] && VERBOSE=1

log() { [[ $VERBOSE -eq 1 ]] && echo "[INFO] $*" >&2; }
status() { echo "✓ $*" >&2; }
error() { echo "✗ $*" >&2; }

# Ensure cache directory structure exists
mkdir -p "$CACHE_DIR/content"
mkdir -p "$CACHE_DIR/obex"

echo "P2 Knowledge Base Refresh" >&2
echo "=========================" >&2

# =============================================================================
# Step 1: Update all scripts (including this one)
# =============================================================================
echo "" >&2
echo "Updating scripts..." >&2

# Fetch script
log "Downloading fetch-kb-file.sh"
curl -sS "$BASE_URL/engineering/tools/p2kb/fetch-kb-file.sh" > "$CACHE_DIR/fetch-kb-file.sh.tmp"
mv "$CACHE_DIR/fetch-kb-file.sh.tmp" "$CACHE_DIR/fetch-kb-file.sh"
chmod +x "$CACHE_DIR/fetch-kb-file.sh"
status "fetch-kb-file.sh"

# Refresh script (self-update)
log "Downloading refresh-kb.sh"
curl -sS "$BASE_URL/engineering/tools/p2kb/refresh-kb.sh" > "$CACHE_DIR/refresh-kb.sh.tmp"
mv "$CACHE_DIR/refresh-kb.sh.tmp" "$CACHE_DIR/refresh-kb.sh"
chmod +x "$CACHE_DIR/refresh-kb.sh"
status "refresh-kb.sh"

# OBEX helper
log "Downloading obex/download-helper.sh"
curl -sS "$BASE_URL/engineering/tools/p2kb/obex/download-helper.sh" > "$CACHE_DIR/obex/download-helper.sh.tmp"
mv "$CACHE_DIR/obex/download-helper.sh.tmp" "$CACHE_DIR/obex/download-helper.sh"
chmod +x "$CACHE_DIR/obex/download-helper.sh"
status "obex/download-helper.sh"

# =============================================================================
# Step 2: Refresh index
# =============================================================================
echo "" >&2
echo "Updating index..." >&2

log "Downloading p2kb-index.json.gz"
curl -sS "$BASE_URL/deliverables/ai/p2kb-index.json.gz" > "$CACHE_DIR/p2kb-index.json.tmp.gz"
gunzip -c "$CACHE_DIR/p2kb-index.json.tmp.gz" > "$CACHE_DIR/p2kb-index.json.tmp"
mv "$CACHE_DIR/p2kb-index.json.tmp" "$CACHE_DIR/p2kb-index.json"
rm -f "$CACHE_DIR/p2kb-index.json.tmp.gz"

# Get entry count
if command -v jq &>/dev/null; then
    ENTRIES=$(jq -r '.system.total_entries' "$CACHE_DIR/p2kb-index.json")
    status "p2kb-index.json ($ENTRIES entries)"
else
    status "p2kb-index.json"
fi

# =============================================================================
# Step 3: Refresh common getting_started files
# =============================================================================
echo "" >&2
echo "Updating common files..." >&2

# List of common_keys.getting_started files to refresh
COMMON_KEYS=(
    "p2kbGuideQuickQueries"
    "p2kbSpin2Spin2GettingStarted"
    "p2kbPasm2Pasm2GettingStarted"
    "p2kbToolsPnutTsCompiler"
)

# Function to look up key in index
lookup_key() {
    local key="$1"
    if command -v jq &>/dev/null; then
        jq -r ".files[\"$key\"].path // empty" "$CACHE_DIR/p2kb-index.json"
    else
        grep -o "\"$key\":{\"path\":\"[^\"]*\"" "$CACHE_DIR/p2kb-index.json" | sed 's/.*"path":"\([^"]*\)".*/\1/'
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
        cache_file="$CACHE_DIR/content/${key}.yaml"
        curl -sS "$BASE_URL/$path" | filter_metadata > "$cache_file.tmp"
        mv "$cache_file.tmp" "$cache_file"
        status "$key"
    else
        error "$key (not found in index)"
    fi
done

# =============================================================================
# Step 4: Fetch root manifest and ai-instructions for reference
# =============================================================================
echo "" >&2
echo "Updating manifests..." >&2

log "Downloading propeller-knowledge-root.yaml"
curl -sS "$BASE_URL/manifests/propeller-knowledge-root.yaml" > "$CACHE_DIR/propeller-knowledge-root.yaml"
status "propeller-knowledge-root.yaml"

log "Downloading ai-instructions.yaml"
curl -sS "$BASE_URL/manifests/ai-instructions.yaml" > "$CACHE_DIR/ai-instructions.yaml"
status "ai-instructions.yaml"

# =============================================================================
# Done
# =============================================================================
echo "" >&2
echo "Refresh complete!" >&2
echo "" >&2
echo "Cache location: $CACHE_DIR" >&2
echo "To fetch content: $CACHE_DIR/fetch-kb-file.sh <key>" >&2
echo "To download OBEX: $CACHE_DIR/obex/download-helper.sh <package>" >&2
