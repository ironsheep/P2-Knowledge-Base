#!/bin/bash
# Enhanced regression test runner for latex-escape-all
# Shows individual test case failures within files

TOOL_NAME="latex-escape-all"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "================================"
echo "LaTeX Escaping Regression Tests"
echo "================================"

# Clean output directory
rm -rf output
mkdir -p output

TOTAL_FAILED=0
TOTAL_PASSED=0

# Function to check specific sections in the diff
check_sections() {
    local golden_file="$1"
    local output_file="$2"
    local base="$3"
    
    # Get all section headers from the golden file
    local sections=($(grep -n "^##" "$golden_file" | cut -d: -f1))
    
    if [ ${#sections[@]} -eq 0 ]; then
        # No sections, just do simple file compare
        if diff -q "$output_file" "$golden_file" > /dev/null 2>&1; then
            echo "  ✅ File content matches"
            ((TOTAL_PASSED++))
        else
            echo "  ❌ File content differs"
            diff -u "$golden_file" "$output_file" | head -10
            ((TOTAL_FAILED++))
        fi
        return
    fi
    
    # Check each section
    local file_lines=$(wc -l < "$golden_file")
    
    for i in "${!sections[@]}"; do
        local start_line=${sections[$i]}
        local section_name=$(sed -n "${start_line}p" "$golden_file" | sed 's/^##* *//')
        
        # Determine end line (next section or end of file)
        if [ $((i+1)) -lt ${#sections[@]} ]; then
            local end_line=$((${sections[$((i+1))]} - 1))
        else
            local end_line=$file_lines
        fi
        
        # Extract section from both files
        sed -n "${start_line},${end_line}p" "$golden_file" > /tmp/golden_section.md
        sed -n "${start_line},${end_line}p" "$output_file" > /tmp/output_section.md 2>/dev/null
        
        # Compare sections
        if diff -q /tmp/output_section.md /tmp/golden_section.md > /dev/null 2>&1; then
            echo "  ✅ $section_name"
            ((TOTAL_PASSED++))
        else
            echo "  ❌ $section_name"
            # Show first few lines of diff for this section
            diff -u /tmp/golden_section.md /tmp/output_section.md | grep -E "^[\+\-]" | head -5 | sed 's/^/      /'
            ((TOTAL_FAILED++))
        fi
    done
    
    # Clean up temp files
    rm -f /tmp/golden_section.md /tmp/output_section.md
}

# Test each input/golden pair
for input_file in input/*.md; do
    base=$(basename "$input_file" .md)
    
    echo ""
    echo "Testing $base:"
    echo "------------------------"
    
    # Run the tool
    ./latex-escape-all.sh "input/$base.md" "output/$base.md" > /dev/null 2>&1
    
    # Check sections
    check_sections "golden/$base-GOLDEN.md" "output/$base.md" "$base"
done

echo ""
echo "================================"
echo "Summary:"
echo "  Passed: $TOTAL_PASSED test sections"
echo "  Failed: $TOTAL_FAILED test sections"
echo "================================"

if [ $TOTAL_FAILED -eq 0 ]; then
    echo "✅ All regression tests passed!"
    exit 0
else
    echo "❌ $TOTAL_FAILED test sections failed. Fix the script and try again."
    echo ""
    echo "To see full diff for a file:"
    echo "  diff -u golden/test-cases-GOLDEN.md output/test-cases.md"
    exit 1
fi