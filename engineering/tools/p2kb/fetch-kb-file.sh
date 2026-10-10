#!/bin/bash
# P2 Knowledge Base Fetch Script v3.5
# Key-based access to YAML content with navigation and alias support
# Usage: ./fetch-kb-file.sh <key|alias> | --help | --cached | --browse <category> | --search <term>

set -e

BASE_URL="https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main"

# Determine script's directory (where this script lives)
# Redirect cd output to /dev/null to handle CDPATH environments
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null && pwd -P)"

# Index and cache location (relative to script directory)
INDEX_DIR="${P2KB_INDEX:-$SCRIPT_DIR/.p2kb}"
INDEX_FILE="$INDEX_DIR/p2kb-index.json"
CACHE_DIR="$INDEX_DIR/cache"

INDEX_MAX_AGE=86400  # 24 hours in seconds

VERBOSE=0

# =============================================================================
# Helper Functions
# =============================================================================

show_help() {
    cat <<'EOF'
P2 Knowledge Base Fetch Script v3.5

USAGE:
    fetch-kb-file.sh <key|alias>        Fetch content by key or alias (e.g., MOV, WAITMS)
    fetch-kb-file.sh --cached           List downloaded keys
    fetch-kb-file.sh --browse <cat>     Browse keys in category
    fetch-kb-file.sh --search <term>    Search for keys (case-insensitive)
    fetch-kb-file.sh --categories       List all available categories
    fetch-kb-file.sh --help             Show this help

ALIASES (v3.4 feature):
    You can use instruction mnemonics, method names, or pattern IDs directly:
      MOV       -> p2kbPasm2Mov        (PASM2 instruction)
      WAITMS    -> p2kbSpin2Waitms     (Spin2 method)
      COGINIT   -> p2kbPasm2Coginit AND p2kbSpin2Coginit (both!)

    When an alias maps to MULTIPLE entries (e.g., ABS exists in both PASM2
    and Spin2), ALL matches are returned. This preserves full information.

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
    fetch-kb-file.sh MOV                    # Get MOV (alias -> p2kbPasm2Mov)
    fetch-kb-file.sh ABS                    # Get BOTH PASM2 and Spin2 ABS docs
    fetch-kb-file.sh p2kbPasm2Mov           # Get MOV by canonical key
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

# -----------------------------------------------------------------------------
# Reading the index WITHOUT jq. jq is optional; without it these read the index
# exactly as generate-p2kb-index.py writes it -- json.dump(indent=2): each
# section opens on `  "<section>": {`, each member starts on a line indented
# four spaces (`    "<name>": {` for files, `    "<name>": [` for aliases and
# categories), file entries carry `"path"` on the next line, and list members sit
# one per line. Names are compared as the JSON text the file holds (see
# json_escape). The release gate checks every key and alias resolves here exactly
# as json.load reads them, so a generator layout change cannot break this quietly.
#
#   nojq_index path    files      <key>     -> the entry's path
#   nojq_index members <section>  <name>    -> the list's members, one per line
#   nojq_index names   <section>            -> every member name (JSON text)
#   nojq_index counts  <section>            -> "<name> <member count>" per member
# -----------------------------------------------------------------------------
nojq_index() {
    # `want` arrives through the environment, not `-v`: awk processes backslash
    # escapes in a -v value, which turned the JSON text `\\` (an alias of `\`)
    # back into `\` and lost the match.
    NOJQ_WANT="$3" LC_ALL=C awk -v mode="$1" -v sec="$2" '
        BEGIN { want = ENVIRON["NOJQ_WANT"] }
        $0 == "  \"" sec "\": {" { inside = 1; next }
        inside && /^  }/ { exit }
        !inside || !/^    "/ { next }
        {
            boundary = match($0, /": [[{]/)
            if (!boundary) next
            name = substr($0, 6, boundary - 6)
            opener = substr($0, boundary + 3, 1)
            if (mode == "names") { print name; next }
            if (mode == "path") {
                if (name != want) next
                getline
                sub(/^ *"path": "/, ""); sub(/",?$/, "")
                print
                exit
            }
            if (opener != "[") next
            if (mode == "members" && name != want) next
            count = 0
            if ($0 !~ /\[\],?$/) {
                while ((getline line) > 0 && line !~ /^    \]/) {
                    count++
                    if (mode == "members") {
                        sub(/^ *"/, "", line); sub(/",?$/, "", line)
                        print line
                    }
                }
            }
            if (mode == "counts") print name " " count
            if (mode == "members") exit
        }
    ' "$INDEX_FILE"
}

# A name as JSON text, so it can be compared with the index without decoding it:
# `"` and `\` are escaped and every non-ASCII character becomes \uXXXX (lowercase
# hex, surrogate pairs above U+FFFF) -- json.dump's default (ensure_ascii). The
# 30 non-ASCII aliases need this (em dashes). Needs a UTF-8 locale for non-ASCII
# input; ASCII input passes straight through.
json_escape() {
    local s="$1"
    # Printable ASCII with no quote or backslash is already its own JSON text.
    if [[ -z "$(printf '%s' "$s" | LC_ALL=C tr -d ' -~')" && "$s" != *[\"\\]* ]]; then
        printf '%s' "$s"
        return 0
    fi
    local out="" c code i hi lo
    for (( i = 0; i < ${#s}; i++ )); do
        c="${s:i:1}"
        case "$c" in
            '"')  out+='\"' ;;
            '\')  out+='\\' ;;
            *)
                code=$(printf '%d' "'$c")
                if (( code < 128 )); then
                    out+="$c"
                elif (( code <= 0xFFFF )); then
                    out+=$(printf '\\u%04x' "$code")
                else
                    hi=$(( 0xD800 + ((code - 0x10000) >> 10) ))
                    lo=$(( 0xDC00 + ((code - 0x10000) & 0x3FF) ))
                    out+=$(printf '\\u%04x\\u%04x' "$hi" "$lo")
                fi
                ;;
        esac
    done
    printf '%s' "$out"
}

to_upper() { printf '%s' "$1" | LC_ALL=C tr '[:lower:]' '[:upper:]'; }
to_lower() { printf '%s' "$1" | LC_ALL=C tr '[:upper:]' '[:lower:]'; }

# Look up key in index - returns path or empty
lookup_key() {
    local key="$1"
    if command -v jq &>/dev/null; then
        jq -r ".files[\"$key\"].path // empty" "$INDEX_FILE"
    else
        nojq_index path files "$(json_escape "$key")"
    fi
}

# Look up alias in index - returns array of canonical keys (v3.4+)
# Aliases are arrays: "MOV": ["p2kbPasm2Mov"] or "ABS": ["p2kbPasm2Abs", "p2kbSpin2Abs"]
# Tries the exact name, then UPPER, then lower case.
lookup_alias() {
    local alias="$1" keys="" variant
    for variant in "$alias" "$(to_upper "$alias")" "$(to_lower "$alias")"; do
        if command -v jq &>/dev/null; then
            keys=$(jq -r --arg a "$variant" '.aliases[$a][]? // empty' "$INDEX_FILE" 2>/dev/null)
        else
            keys=$(nojq_index members aliases "$(json_escape "$variant")")
        fi
        [[ -n "$keys" ]] && break
    done
    echo "$keys"
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
        nojq_index names files | grep -i -- "$search_term" | head -5
    fi
}

# =============================================================================
# Delivery filter -- removes PROVENANCE from every YAML before it is cached or shown
# =============================================================================
#
# WHAT IS REMOVED AND WHY: provenance is how this project knows a claim is true
# (source:/sources: fields, bench-ledger ids, repo paths). Its readers are the
# KB's release gates and auditors; a consuming agent can act on none of it. It
# stays in the repo and is removed on the way out.
#
# THE RULE IS PUBLISHED, NOT HELD HERE. The index carries it as `delivery_filter`
# (written by generate-p2kb-index.py, the single source); this script carries only
# the fixed engine. Contract: engineering/tools/p2kb-mcp/MCP-DELIVERY-FILTER-HANDOFF.md
# §3-§6 (format 1). The p2kb-mcp server applies the same rule with the same engine.
# Without jq, or when the index has no usable block, the built-in rule inside
# filter_metadata (identical to the agreement's §3 block) is used -- quietly.

FILTER_ENGINE_VERSION="3.5"   # bump whenever filter_metadata or load_filter_rule changes
RULE_FIELDS=""                # set by load_filter_rule; empty = built-in rule
RULE_COL0=""

# Read the rule from the index when jq can, and only if it is a valid format-1 block
# (exactly three keys, format 1, boolean flag, non-empty list of unique literal names).
load_filter_rule() {
    RULE_FIELDS=""
    RULE_COL0=""
    command -v jq &>/dev/null || return 0
    [[ -f "$INDEX_FILE" ]] || return 0
    local rule
    rule=$(jq -r '
        .delivery_filter as $r
        | if ($r|type) == "object"
             and ($r|keys) == ["format","remove_column0_comments","remove_fields"]
             and ($r.format|type) == "number" and $r.format == 1
             and ($r.remove_column0_comments|type) == "boolean"
             and ($r.remove_fields|type) == "array" and ($r.remove_fields|length) > 0
             and all($r.remove_fields[]; type == "string" and test("^[A-Za-z0-9_]+$"))
             and ($r.remove_fields|unique|length) == ($r.remove_fields|length)
          then "\($r.remove_fields|join(","))\t\($r.remove_column0_comments)"
          else empty end' "$INDEX_FILE" 2>/dev/null) || rule=""
    if [[ -n "$rule" ]]; then
        RULE_FIELDS="${rule%%$'\t'*}"
        RULE_COL0="${rule##*$'\t'}"
        log "Delivery filter: rule from index"
    else
        log "Delivery filter: built-in rule"
    fi
}

sha256_hex() {
    if command -v sha256sum &>/dev/null; then sha256sum | cut -d' ' -f1
    elif command -v shasum &>/dev/null; then shasum -a 256 | cut -d' ' -f1
    else openssl dgst -sha256 | sed 's/^.*= //'
    fi
}

# rule_id per the agreement §3.1 -- the same value every receiver computes.
filter_rule_id() {
    local fields="${RULE_FIELDS:-$(filter_metadata --builtin-fields)}"
    local col0="${RULE_COL0:-true}"
    printf 'p2kb-delivery-filter\nformat=1\nremove_fields=%s\nremove_column0_comments=%s\n' \
        "$fields" "$col0" | sha256_hex
}

# Cached bodies were filtered under one rule and one engine. If either changed --
# or the cache carries no stamp at all (an older script filled it) -- they go.
check_cache_stamp() {
    local stamp_file="$CACHE_DIR/.filter-stamp"
    local want
    want="$(filter_rule_id)/$FILTER_ENGINE_VERSION"
    if [[ ! -f "$stamp_file" ]] || [[ "$(cat "$stamp_file")" != "$want" ]]; then
        log "Delivery filter changed (or cache unstamped) -- clearing cached bodies"
        rm -f "$CACHE_DIR"/*.yaml
        printf '%s\n' "$want" > "$stamp_file"
    fi
}

# The format-1 engine (agreement §4). A LINE rule, indentation-aware:
#   1. Inside a removed field's span: blank lines and comment-only lines are removed
#      and do NOT end the span (YAML ignores comments); deeper lines are removed;
#      any other line ends the span and is tested below.
#   2. A column-0 `#` line is removed when remove_column0_comments is true.
#   3. A line whose text after leading whitespace is a listed name immediately
#      followed by `:` is removed and opens a span at its indent.
# Not a YAML-aware delete: `- source:` and `{source: ...}` are content and stay.
# Empty input gives empty output. Standalone (no rule loaded) it applies the
# built-in rule, which is the agreement's §3 block exactly.
filter_metadata() {
    local builtin="documentation_level,documentation_source,enhancement_source,last_updated,manual_extraction_date,source,source_reference,sources,verified_against"
    if [[ "$1" == "--builtin-fields" ]]; then
        printf '%s' "$builtin"
        return 0
    fi
    LC_ALL=C awk -v fields="${RULE_FIELDS:-$builtin}" -v col0="${RULE_COL0:-true}" '
        BEGIN {
            n = split(fields, names, ",")
            for (i = 1; i <= n; i++) remove[names[i]] = 1
        }
        dropping {
            body = $0
            sub(/^[[:space:]]+/, "", body)
            if (body == "" || substr(body, 1, 1) == "#") next   # blank or comment: span continues
            match($0, /^[[:space:]]*/)
            if (RLENGTH > drop_indent) next                     # deeper: still the field value
            dropping = 0                                        # span ended; test this line below
        }
        col0 == "true" && substr($0, 1, 1) == "#" { next }
        {
            match($0, /^[[:space:]]*/)
            indent = RLENGTH
            rest = substr($0, indent + 1)
            colon = index(rest, ":")
            if (colon > 1 && (substr(rest, 1, colon - 1) in remove)) {
                drop_indent = indent
                dropping = 1
                next
            }
            print
        }
    '
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

    local keys
    if command -v jq &>/dev/null; then
        keys=$(jq -r --arg c "$category" '.categories[$c][]?' "$INDEX_FILE" 2>/dev/null)
    else
        keys=$(nojq_index members categories "$(json_escape "$category")")
    fi
    if [[ -z "$keys" ]]; then
        error "Category '$category' not found or empty"
        echo "" >&2
        echo "Available categories:" >&2
        if command -v jq &>/dev/null; then
            jq -r '.categories | keys[]' "$INDEX_FILE" | sed 's/^/  /' >&2
        else
            nojq_index names categories | LC_ALL=C sort | sed 's/^/  /' >&2
        fi
        exit 1
    fi
    echo "$keys"
    local count=$(echo "$keys" | wc -l | tr -d ' ')
    echo "" >&2
    echo "Total: $count keys in '$category'" >&2
    exit 0
}

# =============================================================================
# Command: --categories - List all categories
# =============================================================================
cmd_categories() {
    ensure_dirs
    refresh_index

    echo "Available categories:"
    if command -v jq &>/dev/null; then
        jq -r '.categories | to_entries[] | "  \(.key): \(.value | length) keys"' "$INDEX_FILE"
    else
        nojq_index counts categories | awk '{ print "  " $1 ": " $2 " keys" }'
    fi
    exit 0
}

# =============================================================================
# Command: --search <term> - Search for keys and aliases
# =============================================================================
cmd_search() {
    local term="$1"

    if [[ -z "$term" ]]; then
        error "Usage: $0 --search <term>"
        exit 1
    fi

    ensure_dirs
    refresh_index

    # Search both keys and aliases (case-insensitive)
    local keys aliases
    if command -v jq &>/dev/null; then
        keys=$(jq -r ".files | keys[] | select(test(\"$term\"; \"i\"))" "$INDEX_FILE" 2>/dev/null)
        aliases=$(jq -r ".aliases | to_entries[] | select(.key | test(\"$term\"; \"i\")) | \"\(.key) -> \(.value | join(\", \"))\"" "$INDEX_FILE" 2>/dev/null)
    else
        # Without jq, alias names with non-ASCII characters match by their \uXXXX text.
        # `|| true`: grep exits 1 on no match, which `set -e` would turn into a silent exit.
        keys=$(nojq_index names files | grep -i -- "$term" || true)
        local name
        aliases=$(nojq_index names aliases | { grep -i -- "$term" || true; } | while IFS= read -r name; do
            printf '%s -> %s\n' "$name" "$(nojq_index members aliases "$name" | paste -sd, - | sed 's/,/, /g')"
        done)
    fi

    local found_something=0

    if [[ -n "$keys" ]]; then
        echo "=== Matching Keys ==="
        echo "$keys"
        local key_count=$(echo "$keys" | wc -l | tr -d ' ')
        echo "" >&2
        echo "Found: $key_count keys matching '$term'" >&2
        found_something=1
    fi

    if [[ -n "$aliases" ]]; then
        if [[ $found_something -eq 1 ]]; then
            echo ""
        fi
        echo "=== Matching Aliases ==="
        echo "$aliases"
        local alias_count=$(echo "$aliases" | wc -l | tr -d ' ')
        echo "" >&2
        echo "Found: $alias_count aliases matching '$term'" >&2
        found_something=1
    fi

    if [[ $found_something -eq 0 ]]; then
        echo "No keys or aliases found matching '$term'" >&2
    fi
    exit 0
}

# =============================================================================
# Command: Fetch key (with alias resolution v3.4)
# =============================================================================

# Helper: fetch a single canonical key and output its content
fetch_single_key() {
    local key="$1"
    local path=$(lookup_key "$key")

    if [[ -z "$path" ]]; then
        return 1
    fi

    log "Key: $key -> $path"

    # Check cache
    local cache_file="$CACHE_DIR/${key}.yaml"

    # Fetch if not cached
    if [[ ! -f "$cache_file" ]]; then
        log "Fetching: $BASE_URL/$path"
        curl -sS "$BASE_URL/$path" | filter_metadata > "$cache_file.tmp"
        if [[ ! -s "$cache_file.tmp" ]]; then
            error "Fetch for '$key' returned no content ($BASE_URL/$path) — not caching an empty result"
            rm -f "$cache_file.tmp"
            return 1
        fi
        mv "$cache_file.tmp" "$cache_file"
        log "Cached to: $cache_file"
    else
        log "Using cached: $cache_file"
    fi

    if [[ ! -s "$cache_file" ]]; then
        error "Cached entry for '$key' is empty — refusing a silent success"
        return 1
    fi

    # Output content
    cat "$cache_file"
    return 0
}

cmd_fetch() {
    local input="$1"

    ensure_dirs
    refresh_index
    load_filter_rule
    check_cache_stamp

    # 1. Try direct key lookup first
    local path=$(lookup_key "$input")

    if [[ -n "$path" ]]; then
        # Direct key match - fetch it
        fetch_single_key "$input"
        return $?
    fi

    # 2. Try alias lookup (v3.4+)
    local alias_keys=$(lookup_alias "$input")

    if [[ -n "$alias_keys" ]]; then
        local count=$(echo "$alias_keys" | grep -c '^' || echo 0)

        if [[ $count -gt 1 ]]; then
            # Multiple matches - output all with separators
            echo "# ========================================" >&2
            echo "# Alias '$input' resolved to $count entries:" >&2
            echo "$alias_keys" | sed 's/^/#   /' >&2
            echo "# ========================================" >&2
            echo "" >&2
        fi

        local first=1
        local any_failed=0
        while IFS= read -r key; do
            if [[ -n "$key" ]]; then
                if [[ $first -eq 0 ]]; then
                    # Separator between multiple results
                    echo ""
                    echo "# ========================================"
                    echo "# Next entry: $key"
                    echo "# ========================================"
                fi
                fetch_single_key "$key" || any_failed=1
                first=0
            fi
        done <<< "$alias_keys"
        # A fetch that returned no content must not read back as success.
        return $any_failed
    fi

    # 3. Not found - show error with suggestions
    error "Key or alias '$input' not found in index"
    echo "" >&2

    # Find and show similar keys
    local similar=$(find_similar_keys "$input")
    if [[ -n "$similar" ]]; then
        echo "Similar keys:" >&2
        echo "$similar" | sed 's/^/  /' >&2
    fi

    echo "" >&2
    echo "Tips:" >&2
    echo "  - Use --search <term> to find keys" >&2
    echo "  - Use --browse <category> to explore by category" >&2
    echo "  - Use --categories to see all categories" >&2
    echo "  - Try common aliases: MOV, ADD, WAITMS, COGINIT" >&2
    exit 1
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
            # Do NOT shift here — the unconditional `shift` at the bottom of
            # this loop already advances past this flag. Shifting twice
            # silently ate the KEY argument in `-v <KEY>`: VERBOSE got set,
            # the key was discarded before cmd_fetch ever ran, the loop
            # exhausted $# and the script exited 0 having fetched nothing.
            VERBOSE=1
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
            exit $?
            ;;
    esac
    shift 2>/dev/null || true
done
