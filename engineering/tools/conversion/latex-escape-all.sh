#!/bin/bash
# Complete LaTeX escaping for P2 Assembly manual
# Usage: ./latex-escape-all.sh input.md output.md

if [ $# -ne 2 ]; then
    echo "Usage: $0 input.md output.md"
    exit 1
fi

INPUT="$1"
OUTPUT="$2"

# NO BACKUP. This script reads $INPUT and writes a SEPARATE $OUTPUT — it never
# modifies its input — so a backup here protected against nothing. What it did do
# was drop a hand-named `<file>.backup.<timestamp>` beside the workspace render on
# every run, violating both halves of engineering/standards/BACKUP-CONVENTION.md:
# never hand-name a backup, and never back up a regenerable artifact (the workspace
# render is rebuilt from opus-master by assemble-manual.sh — the generator IS the
# backup). 90 of them had accumulated across 17 documents by 2026-08-19, and the
# XBYTE sprint's «#252» deleted four only for this script to create nine more the
# same day. Removed at that sprint's closeout — fix the generator, not the litter.

# Get script directory to find the Python processor
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Capture start time for performance monitoring
START_TIME=$(date +%s)

# Run Python processor
python3 "$SCRIPT_DIR/latex_escape_processor.py" "$INPUT" "$OUTPUT"

# Calculate elapsed time
END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))

echo "LaTeX escaping complete: $INPUT -> $OUTPUT"
echo "Processing time: ${ELAPSED} seconds"

# Performance warning if over 30 seconds
if [ $ELAPSED -gt 30 ]; then
    echo "⚠️  WARNING: Processing took ${ELAPSED} seconds (expected < 30s)"
    echo "    Consider optimizing for large documents"
fi

# Comprehensive verification
echo "Verification (unescaped characters remaining):"
echo "  # characters:      $(grep -o '[^\\]#' "$OUTPUT" | wc -l | tr -d ' ')"
echo "  \$ characters:       $(grep -o '[^\\]\$' "$OUTPUT" | wc -l | tr -d ' ')"  
echo "  % characters:        $(grep -o '[^\\]%' "$OUTPUT" | wc -l | tr -d ' ')"
echo "  & characters:        $(grep -o '[^\\]&' "$OUTPUT" | wc -l | tr -d ' ')"
echo "  _ characters:       $(grep -o '[^\\]_' "$OUTPUT" | wc -l | tr -d ' ')"
echo "  ^ characters:        $(grep -o '[^\\]\^[^{}]' "$OUTPUT" | wc -l | tr -d ' ')"
echo "  { characters:        $(grep -o '[^\\]{' "$OUTPUT" | wc -l | tr -d ' ')"
echo "  } characters:        $(grep -o '[^\\]}' "$OUTPUT" | wc -l | tr -d ' ')"