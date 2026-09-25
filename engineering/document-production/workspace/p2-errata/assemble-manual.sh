#!/bin/bash
# P2 Errata Assembly Script
# Combines opus-master content (front matter + one chapter per erratum + appendix)
# into a single markdown file that PDF Forge consumes. Front matter is PREPENDED
# per the house standard (manual-front-matter-and-code-coloring-standard.md).
#
# Chapter N is erratum EN. Erratum numbers are permanent: a new erratum is
# appended as the next chapter file, never inserted between existing ones.

set -e

OPUS_MASTER="../../manuals/p2-errata/opus-master"
OUTPUT="P2-Errata.md"

echo "========================================"
echo "P2 Errata Assembly"
echo "========================================"
echo ""

if [ ! -d "$OPUS_MASTER" ]; then
    echo "ERROR: Source directory $OPUS_MASTER not found"
    exit 1
fi

# Source files, in assembly order
declare -a REQUIRED_FILES=(
    "front-matter.md"
    "e1-setq-block-pointer-step.md"
    "e2-altx-takes-pending-augs.md"
    "e3-getct-stale-upper-long.md"
    "e4-getxacc-clear-gating.md"
    "e5-goertzel-one-clock-lag.md"
    "appendix-a-test-programs.md"
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
