#!/bin/bash
# validate-pasm-code.sh
# Validates PASM2 code snippets from documentation using pnut_ts compiler
# Usage: ./validate-pasm-code.sh <markdown-file>

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if markdown file provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <markdown-file>"
    exit 1
fi

MARKDOWN_FILE="$1"
TEMP_DIR=$(mktemp -d)
FAILED=0
PASSED=0
SNIPPET_NUM=0

echo "Validating PASM2 code snippets in: $MARKDOWN_FILE"
echo "----------------------------------------"

# Extract PASM2 code blocks from markdown
# Look for code blocks with pasm2 language identifier
awk '/^```pasm2/,/^```$/' "$MARKDOWN_FILE" | \
while IFS= read -r line; do
    if [[ "$line" == '```pasm2' ]]; then
        SNIPPET_NUM=$((SNIPPET_NUM + 1))
        TEMP_FILE="$TEMP_DIR/snippet_${SNIPPET_NUM}.spin2"
        echo "DAT" > "$TEMP_FILE"  # Add DAT section header
        echo "    ORG 0" >> "$TEMP_FILE"  # Add ORG directive
        IN_BLOCK=1
    elif [[ "$line" == '```' ]] && [[ "$IN_BLOCK" == "1" ]]; then
        IN_BLOCK=0
        
        # Try to compile the snippet
        echo -n "Snippet #$SNIPPET_NUM: "
        
        if pnut_ts -q "$TEMP_FILE" 2>/dev/null; then
            echo -e "${GREEN}✓ PASS${NC}"
            PASSED=$((PASSED + 1))
        else
            echo -e "${RED}✗ FAIL${NC}"
            echo "  Error output:"
            pnut_ts "$TEMP_FILE" 2>&1 | sed 's/^/    /'
            echo "  Code snippet:"
            cat "$TEMP_FILE" | sed 's/^/    /'
            FAILED=$((FAILED + 1))
        fi
    elif [[ "$IN_BLOCK" == "1" ]]; then
        # Process the line - remove bold markers and common formatting
        CLEAN_LINE=$(echo "$line" | sed 's/\*\*//g')
        echo "    $CLEAN_LINE" >> "$TEMP_FILE"
    fi
done

# Summary
echo "----------------------------------------"
echo "Validation Summary:"
echo -e "  ${GREEN}Passed: $PASSED${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "  ${RED}Failed: $FAILED${NC}"
else
    echo -e "  ${GREEN}Failed: 0${NC}"
fi

# Cleanup
rm -rf "$TEMP_DIR"

# Exit with error if any failures
exit $FAILED