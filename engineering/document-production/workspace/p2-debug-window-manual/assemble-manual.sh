#!/bin/bash
# P2 Debug Window Manual — Assembly Script
# Concatenates the opus-master source files (front matter + part dividers +
# chapters + appendices) into the single markdown file PDF Forge consumes.
# This is the ONE canonical assembly: opus-master/ holds the source of truth;
# this script produces the build artifact. No version-numbered files anywhere.
#
# Run from: engineering/document-production/workspace/p2-debug-window-manual/
# Output:   P2-Debug-Window-Manual.md (this workspace dir, unescaped working copy)
# Next:     latex-escape-all.sh → outbound, then user deploys to PDF Forge.

set -e

OPUS_MASTER="../../manuals/p2-debug-window-manual/opus-master"
OUTPUT="P2-Debug-Window-Manual.md"

echo "========================================"
echo "P2 Debug Window Manual Assembly"
echo "========================================"
echo ""

if [ ! -d "$OPUS_MASTER" ]; then
    echo "ERROR: Source directory $OPUS_MASTER not found"
    exit 1
fi

# Source files, in reading order: front matter, then each Part divider
# immediately followed by the chapters that fall under it, then the appendices.
declare -a REQUIRED_FILES=(
    "front-matter.md"
    "part-1-foundation.md"
    "ch01-foundation.md"
    "ch02-getting-started.md"
    "part-2-windows.md"
    "ch03-term.md"
    "ch04-bitmap.md"
    "ch05-plot.md"
    "ch06-logic.md"
    "ch07-scope.md"
    "ch08-scope-xy.md"
    "ch09-fft.md"
    "ch10-spectro.md"
    "ch11-midi.md"
    "part-3-integration.md"
    "ch12-bidirectional.md"
    "ch13-packed-data.md"
    "ch14-multiwindow-pasm.md"
    "ch15-panels.md"
    "part-4-appendices.md"
    "appendix-a-command-reference.md"
    "appendix-b-packed-data.md"
    "appendix-c-color-coordinate.md"
    "index.md"
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
echo "  All ${#REQUIRED_FILES[@]} source files present."
echo ""

# Assemble: concatenate in order with a blank line between files.
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
