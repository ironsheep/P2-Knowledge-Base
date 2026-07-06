#!/bin/bash
# P2AN006 Application Note Assembly Script
# Combines opus-master content (front matter + body) into a single markdown file
# that PDF Forge consumes. Front matter (the cover) is PREPENDED to the body, the
# same house standard the manuals use, so it flows through Pandoc + the template.
#
# NOTE: app notes live under app-notes/<name>/, not manuals/<slug>/ — this script's
# OPUS_MASTER path is what bridges the app-note authoring tree to the shared
# workspace/outbound production path (the Three-Folder Rule).

set -e

OPUS_MASTER="../../app-notes/P2AN006/opus-master"
OUTPUT="P2AN006.md"

echo "========================================"
echo "P2AN006 Application Note Assembly"
echo "========================================"
echo ""

if [ ! -d "$OPUS_MASTER" ]; then
    echo "ERROR: Source directory $OPUS_MASTER not found"
    exit 1
fi

# Source files, in assembly order (front matter / cover first, then the body)
declare -a REQUIRED_FILES=(
    "front-matter.md"
    "P2AN006.md"
)

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
