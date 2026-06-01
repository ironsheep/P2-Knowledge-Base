#!/bin/bash
# P2 Streamer Programming Guide Assembly Script
# Combines opus-master content (front matter + body) into a single markdown file
# that PDF Forge consumes. Front matter is PREPENDED to the body per the house
# standard (manual-front-matter-and-code-coloring-standard.md), so it flows
# through Pandoc + the template rather than being hardcoded in the .latex.

set -e

OPUS_MASTER="../../manuals/p2-streamer-programming-guide/opus-master"
OUTPUT="P2-Streamer-Programming-Guide.md"

echo "========================================"
echo "P2 Streamer Programming Guide Assembly"
echo "========================================"
echo ""

if [ ! -d "$OPUS_MASTER" ]; then
    echo "ERROR: Source directory $OPUS_MASTER not found"
    exit 1
fi

# Source files, in assembly order (front matter first, then the body)
declare -a REQUIRED_FILES=(
    "front-matter.md"
    "streamer-body.md"
)

# Verify all required files exist
echo "Verifying source files..."
MISSING_COUNT=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$OPUS_MASTER/$file" ]; then
        echo "  ERROR: Missing $file"
        MISSING_COUNT=$((MISSING_COUNT + 1))
    fi
done

if [ "$MISSING_COUNT" -gt 0 ]; then
    echo ""
    echo "ERROR: $MISSING_COUNT required file(s) missing. Aborting."
    exit 1
fi
echo "  All source files present."
echo ""

# Assemble: concatenate in order with a blank line between files
echo "Assembling $OUTPUT ..."
: > "$OUTPUT"
for file in "${REQUIRED_FILES[@]}"; do
    cat "$OPUS_MASTER/$file" >> "$OUTPUT"
    printf '\n\n' >> "$OUTPUT"
done

LINES=$(wc -l < "$OUTPUT")
echo "  Wrote $OUTPUT ($LINES lines from ${#REQUIRED_FILES[@]} source files)."
echo ""
echo "Done. Next: run latex-escape-all.sh, then stage CHANGED files to outbound."
