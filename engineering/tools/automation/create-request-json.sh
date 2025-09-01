#!/bin/bash
# Creates a properly formatted request.json
# Usage: ./create-request-json.sh input.md output.pdf "Version String" "Footer Text"

INPUT="${1:-CHANGE_ME.md}"
OUTPUT="${2:-CHANGE_ME.pdf}"
VERSION="${3:-Draft}"
FOOTER="${4:-Technical Review Draft}"

cat > request.json << EOF
{
  "documents": [
    {
      "input": "$INPUT",
      "output": "$OUTPUT",
      "template": "p2kb-pasm-desilva",
      "variables": {
        "title": "Discovering P2 Assembly",
        "subtitle": "Build, Experiment, and Master the Propeller 2",
        "version": "$VERSION",
        "date": "August 2025",
        "author": "P2 Knowledge Base Initiative",
        "footer": "$FOOTER"
      }
    }
  ],
  "options": {
    "cleanup": true,
    "archive": false,
    "optimize": true
  }
}
EOF

echo "Created request.json with:"
echo "  Input:   $INPUT"
echo "  Output:  $OUTPUT"
echo "  Version: $VERSION"
echo "  Footer:  $FOOTER"