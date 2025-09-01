#!/bin/bash
# Regression test runner for latex-escape-all

TOOL_NAME="latex-escape-all"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "================================"
echo "LaTeX Escaping Regression Tests"
echo "================================"

# Clean output directory
rm -rf output
mkdir -p output

FAILED=0

# Test each input/golden pair
for input_file in input/*.md; do
    base=$(basename "$input_file" .md)
    
    echo -n "Testing $base... "
    
    # Run the tool
    ./latex-escape-all.sh "input/$base.md" "output/$base.md" > /dev/null 2>&1
    
    # Compare with golden
    if diff -q "output/$base.md" "golden/$base-GOLDEN.md" > /dev/null 2>&1; then
        echo "✅ PASS"
    else
        echo "❌ FAIL"
        echo "  Differences found:"
        diff -u "golden/$base-GOLDEN.md" "output/$base.md" | head -20
        echo "  ..."
        FAILED=1
    fi
done

echo "================================"

if [ $FAILED -eq 0 ]; then
    echo "✅ All regression tests passed!"
    exit 0
else
    echo "❌ Some tests failed. Fix the script and try again."
    echo ""
    echo "To see full diff:"
    echo "  diff golden/test-cases-GOLDEN.md output/test-cases.md"
    exit 1
fi