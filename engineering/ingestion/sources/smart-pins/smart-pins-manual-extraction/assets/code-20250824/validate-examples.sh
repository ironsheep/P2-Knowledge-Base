#!/bin/bash
# Validate which Spin2 examples compile successfully

echo "Testing Spin2 examples compilation..."
echo "======================================"
echo

success_count=0
fail_count=0

for file in req*.spin2; do
    echo -n "Testing $file: "
    if pnut_ts "$file" > /dev/null 2>&1; then
        echo "✅ PASS"
        ((success_count++))
    else
        echo "❌ FAIL"
        ((fail_count++))
    fi
done

echo
echo "======================================"
echo "Results:"
echo "  Successful: $success_count"
echo "  Failed: $fail_count"
echo "  Total: $((success_count + fail_count))"
echo

# Clean up generated files
rm -f *.bin *.obj *.lst 2>/dev/null

echo "Note: PASM2 files need to be wrapped in Spin2 DAT sections to compile."