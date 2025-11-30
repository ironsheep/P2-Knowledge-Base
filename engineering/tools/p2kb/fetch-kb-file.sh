#!/bin/bash
# P2 Knowledge Base Fetch Script v3.2
# Key-based access to YAML content with navigation support
# Usage: ./fetch-kb-file.sh <key> | --help | --cached | --browse <category> | --search <term>

set -e

BASE_URL="https://raw.githubusercontent.com/IronSheepProductionsLLC/P2-Knowledge-Base/main"

# Script location (user-visible)
SCRIPT_DIR="${P2KB_SCRIPTS:-$HOME/.p2kb-cache}"

# Index and cache location (hidden from user)
INDEX_DIR="${P2KB_INDEX:-$HOME/.p2kb}"
INDEX_FILE="$INDEX_DIR/p2kb-index.json"
CACHE_DIR="$INDEX_DIR/cache"

INDEX_MAX_AGE=86400  # 24 hours in seconds

VERBOSE=0

# =============================================================================
# Helper Functions
# =============================================================================

show_help() {
    cat <<'EOF'
P2 Knowledge Base Fetch Script v3.2

USAGE:
    fetch-kb-file.sh <key>              Fetch content by key
    fetch-kb-file.sh --cached           List downloaded keys
    fetch-kb-file.sh --browse <cat>     Browse keys in category
    fetch-kb-file.sh --search <term>    Search for keys (case-insensitive)
    fetch-kb-file.sh --categories       List all available categories
    fetch-kb-file.sh --help             Show this help

CATEGORIES (for --browse):
    PASM2 Instructions:
      pasm2_directives, pasm2_branch, pasm2_cordic, pasm2_math, pasm2_pin,
      pasm2_event, pasm2_hub_control, pasm2_hub_fifo, pasm2_hub_ram,
      pasm2_interrupt, pasm2_lookup_table, pasm2_misc, pasm2_pixel,
      pasm2_register_indirection, pasm2_smart_pin, pasm2_streamer

    Architecture:
      architecture_core, architecture_math, architecture_timing,
      architecture_interrupts, architecture_sync, architecture_io

    Smart Pins:
      smart_pins_digital, smart_pins_serial, smart_pins_pwm,
      smart_pins_counting, smart_pins_timing, smart_pins_frequency,
      smart_pins_analog, smart_pins_special, smart_pins_beginner

    Spin2:
      spin2_control_flow, spin2_pin_control, spin2_timing, spin2_cog_control,
      spin2_memory, spin2_math, spin2_strings, spin2_smart_pins, spin2_locks

    Guides:
      guides_getting_started

EXAMPLES:
    fetch-kb-file.sh p2kbPasm2Mov           # Get MOV instruction
    fetch-kb-file.sh --browse pasm2_branch  # List all branch instructions
    fetch-kb-file.sh --search uart          # Find UART-related keys
    fetch-kb-file.sh --cached               # Show what's already downloaded

KEY PREFIXES:
    p2kbPasm2*    - PASM2 assembly instructions
    p2kbSpin2*    - Spin2 methods and language elements
    p2kbArch*     - P2 architecture documentation
    p2kbGuide*    - Guides and quick references
    p2kbHw*       - Hardware specifications

IMPORTANT:
    Always use this script for P2KB access. Never access index or cache directly.
    Use --browse or --search to find valid keys. Never guess at key names.

EOF
    exit 0
}

log() { [[ $VERBOSE -eq 1 ]] && echo "[INFO] $*" >&2 || true; }
error() { echo "ERROR: $*" >&2; }

# Ensure directories exist
ensure_dirs() {
    mkdir -p "$INDEX_DIR"
    mkdir -p "$CACHE_DIR"
}

# Check if index needs refresh
refresh_index() {
    local need_refresh=0

    if [[ ! -f "$INDEX_FILE" ]]; then
        log "Index not found, downloading..."
        need_refresh=1
    else
        # Get file age (cross-platform)
        local mtime
        if [[ "$(uname)" == "Darwin" ]]; then
            mtime=$(stat -f %m "$INDEX_FILE")
        else
            mtime=$(stat -c %Y "$INDEX_FILE")
        fi
        local age=$(($(date +%s) - mtime))
        if [[ $age -gt $INDEX_MAX_AGE ]]; then
            log "Index is ${age}s old (max ${INDEX_MAX_AGE}s), refreshing..."
            need_refresh=1
        fi
    fi

    if [[ $need_refresh -eq 1 ]]; then
        log "Downloading index from $BASE_URL/deliverables/ai/p2kb-index.json.gz"
        curl -sS "$BASE_URL/deliverables/ai/p2kb-index.json.gz" | gunzip > "$INDEX_FILE.tmp"
        mv "$INDEX_FILE.tmp" "$INDEX_FILE"
        if command -v jq &>/dev/null; then
            local entries=$(jq -r '.system.total_entries' "$INDEX_FILE")
            log "Index updated: $entries entries"
        fi
    fi
}

# Look up key in index - returns path or empty
lookup_key() {
    local key="$1"
    if command -v jq &>/dev/null; then
        jq -r ".files[\"$key\"].path // empty" "$INDEX_FILE"
    else
        grep -o "\"$key\":{\"path\":\"[^\"]*\"" "$INDEX_FILE" 2>/dev/null | sed 's/.*"path":"\([^"]*\)".*/\1/'
    fi
}

# Find similar keys for error suggestions
find_similar_keys() {
    local key="$1"
    local search_term=""

    # Extract a portion of the key to search for
    if [[ ${#key} -gt 8 ]]; then
        # Get middle portion after p2kb prefix
        search_term="${key:4:8}"
    else
        search_term="${key:4}"
    fi

    if command -v jq &>/dev/null; then
        jq -r ".files | keys[] | select(test(\"$search_term\"; \"i\"))" "$INDEX_FILE" 2>/dev/null | head -5
    else
        grep -o "\"p2kb[^\"]*\"" "$INDEX_FILE" | tr -d '"' | grep -i "$search_term" | head -5
    fi
}

# Filter metadata from YAML content
filter_metadata() {
    grep -v -E "^[[:space:]]*(last_updated|enhancement_source|documentation_source|documentation_level|manual_extraction_date):"
}

# =============================================================================
# Command: --cached - List downloaded keys
# =============================================================================
cmd_cached() {
    if [[ -d "$CACHE_DIR" ]]; then
        local count=0
        shopt -s nullglob
        for f in "$CACHE_DIR"/*.yaml; do
            if [[ -f "$f" ]]; then
                basename "$f" .yaml
                count=$((count + 1))
            fi
        done
        shopt -u nullglob
        if [[ $count -eq 0 ]]; then
            echo "No cached files found." >&2
        else
            echo "" >&2
            echo "Total: $count cached files" >&2
        fi
    else
        echo "Cache directory not found. No files cached yet." >&2
    fi
    exit 0
}

# =============================================================================
# Command: --browse <category> - Show keys in category
# =============================================================================
cmd_browse() {
    local category="$1"

    if [[ -z "$category" ]]; then
        error "Usage: $0 --browse <category>"
        echo "Use --categories to see available categories" >&2
        exit 1
    fi

    ensure_dirs
    refresh_index

    if command -v jq &>/dev/null; then
        local keys=$(jq -r ".categories[\"$category\"][]?" "$INDEX_FILE" 2>/dev/null)
        if [[ -z "$keys" ]]; then
            error "Category '$category' not found or empty"
            echo "" >&2
            echo "Available categories:" >&2
            jq -r '.categories | keys[]' "$INDEX_FILE" | sed 's/^/  /' >&2
            exit 1
        fi
        echo "$keys"
        local count=$(echo "$keys" | wc -l | tr -d ' ')
        echo "" >&2
        echo "Total: $count keys in '$category'" >&2
    else
        error "jq required for --browse command"
        exit 1
    fi
    exit 0
}

# =============================================================================
# Command: --categories - List all categories
# =============================================================================
cmd_categories() {
    ensure_dirs
    refresh_index

    if command -v jq &>/dev/null; then
        echo "Available categories:"
        jq -r '.categories | to_entries[] | "  \(.key): \(.value | length) keys"' "$INDEX_FILE"
    else
        error "jq required for --categories command"
        exit 1
    fi
    exit 0
}

# =============================================================================
# Command: --search <term> - Search for keys
# =============================================================================
cmd_search() {
    local term="$1"

    if [[ -z "$term" ]]; then
        error "Usage: $0 --search <term>"
        exit 1
    fi

    ensure_dirs
    refresh_index

    if command -v jq &>/dev/null; then
        local keys=$(jq -r ".files | keys[] | select(test(\"$term\"; \"i\"))" "$INDEX_FILE" 2>/dev/null)
        if [[ -z "$keys" ]]; then
            echo "No keys found matching '$term'" >&2
            exit 0
        fi
        echo "$keys"
        local count=$(echo "$keys" | wc -l | tr -d ' ')
        echo "" >&2
        echo "Found: $count keys matching '$term'" >&2
    else
        # Fallback without jq
        grep -o "\"p2kb[^\"]*\"" "$INDEX_FILE" | tr -d '"' | grep -i "$term"
    fi
    exit 0
}

# =============================================================================
# Command: Fetch key
# =============================================================================
cmd_fetch() {
    local key="$1"

    ensure_dirs
    refresh_index

    local path=$(lookup_key "$key")

    if [[ -z "$path" ]]; then
        error "Key '$key' not found in index"
        echo "" >&2

        # Find and show similar keys
        local similar=$(find_similar_keys "$key")
        if [[ -n "$similar" ]]; then
            echo "Similar keys:" >&2
            echo "$similar" | sed 's/^/  /' >&2
        fi

        echo "" >&2
        echo "Tips:" >&2
        echo "  - Use --search <term> to find keys" >&2
        echo "  - Use --browse <category> to explore by category" >&2
        echo "  - Use --categories to see all categories" >&2
        exit 1
    fi

    log "Key: $key -> $path"

    # Check cache
    local cache_file="$CACHE_DIR/${key}.yaml"

    # Fetch if not cached
    if [[ ! -f "$cache_file" ]]; then
        log "Fetching: $BASE_URL/$path"
        curl -sS "$BASE_URL/$path" | filter_metadata > "$cache_file.tmp"
        mv "$cache_file.tmp" "$cache_file"
        log "Cached to: $cache_file"
    else
        log "Using cached: $cache_file"
    fi

    # Output content
    cat "$cache_file"
}

# =============================================================================
# Main - Parse arguments and dispatch
# =============================================================================

# No arguments - show help
if [[ $# -eq 0 ]]; then
    show_help
fi

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --help|-h)
            show_help
            ;;
        --verbose|-v)
            VERBOSE=1
            shift
            ;;
        --cached)
            cmd_cached
            ;;
        --browse)
            shift
            cmd_browse "$1"
            ;;
        --categories)
            cmd_categories
            ;;
        --search)
            shift
            cmd_search "$1"
            ;;
        -*)
            error "Unknown option: $1"
            echo "Use --help for usage information" >&2
            exit 1
            ;;
        *)
            # Assume it's a key to fetch
            cmd_fetch "$1"
            exit 0
            ;;
    esac
    shift 2>/dev/null || true
done
