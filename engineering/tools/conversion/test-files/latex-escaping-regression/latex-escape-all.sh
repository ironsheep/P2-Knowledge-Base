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

# Run Python processor
python3 "$SCRIPT_DIR/latex_escape_processor.py" "$INPUT" "$OUTPUT"

echo "LaTeX escaping complete: $INPUT -> $OUTPUT"
echo "Backup created: $INPUT.backup.$(date +%Y%m%d_%H%M%S)"

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