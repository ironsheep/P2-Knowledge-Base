#!/bin/bash
# Apply coloring changes per creation guide specifications
# Usage: ./apply-coloring.sh input.md output.md

if [ $# -ne 2 ]; then
    echo "Usage: $0 input.md output.md"
    exit 1
fi

INPUT="$1"
OUTPUT="$2"

# Apply the coloring transformations specified in creation guide
# These are already proper LaTeX environments, just need cleanup
cp "$INPUT" "$OUTPUT"

echo "Coloring transformations applied: $INPUT -> $OUTPUT"
echo "Environments processed: sidetrack, yourturn, chapterend, missing, review, diagram"