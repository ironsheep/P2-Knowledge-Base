#!/bin/bash
# Validate all extracted Spin2 examples using pnut_ts compiler

echo "=================================="
echo "P2 Debug Manual Code Validation"
echo "=================================="
echo ""

passed=0
failed=0
total=0

# Create results directory
mkdir -p results

echo "Testing all examples..."
echo ""

for file in example_*.spin2; do
    if [ -f "$file" ]; then
        total=$((total + 1))
        echo -n "Testing $file: "
        
        # Run compiler and capture output
        if pnut_ts "$file" > "results/${file%.spin2}.log" 2>&1; then
            echo "✅ PASS"
            passed=$((passed + 1))
        else
            echo "❌ FAIL"
            failed=$((failed + 1))
            echo "  Error details in: results/${file%.spin2}.log"
        fi
    fi
done

echo ""
echo "=================================="
echo "Validation Summary"
echo "=================================="
echo "Total examples: $total"
echo "Passed: $passed"
echo "Failed: $failed"
echo "Success rate: $(( passed * 100 / total ))%"
echo ""

if [ $failed -gt 0 ]; then
    echo "Failed examples:"
    for file in example_*.spin2; do
        if [ -f "$file" ]; then
            if ! pnut_ts "$file" > /dev/null 2>&1; then
                echo "  - $file"
            fi
        fi
    done
fi

echo ""
echo "Detailed logs saved in: results/"