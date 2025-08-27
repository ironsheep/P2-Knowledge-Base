#!/bin/bash
# Complete LaTeX escaping for P2 Assembly manual
# Usage: ./latex-escape-all.sh input.md output.md

if [ $# -ne 2 ]; then
    echo "Usage: $0 input.md output.md"
    exit 1
fi

INPUT="$1"
OUTPUT="$2"

# Make backup
cp "$INPUT" "$INPUT.backup.$(date +%Y%m%d_%H%M%S)"

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
echo "Backup created: $INPUT.backup.$(date +%Y%m%d_%H%M%S)"

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