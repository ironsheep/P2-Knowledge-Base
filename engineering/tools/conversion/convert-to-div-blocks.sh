#!/bin/bash

# Convert language-tagged code blocks to div-wrapped format
# Usage: ./convert-to-div-blocks.sh input.md output.md

if [ $# -ne 2 ]; then
    echo "Usage: $0 input.md output.md"
    exit 1
fi

INPUT="$1"
OUTPUT="$2"

if [ ! -f "$INPUT" ]; then
    echo "Error: Input file '$INPUT' not found"
    exit 1
fi

echo "Converting code blocks from language-tagged to div-wrapped format..."
echo "Input: $INPUT"
echo "Output: $OUTPUT"

# Create a working copy
cp "$INPUT" "$OUTPUT"

# Convert spin2 blocks
echo "Converting spin2 blocks..."
perl -i -pe '
    if (/^```spin2$/) {
        $_ = ":::: spin2\n```\n";
    } elsif (/^```$/ && $prev_line =~ /^:::: (spin2|pasm2|antipattern)$/) {
        # Skip - already part of div
    } elsif (/^```$/ && $prev_spin2) {
        $_ = "```\n::::\n";
        $prev_spin2 = 0;
    }
    $prev_spin2 = 1 if /^:::: spin2$/;
    $prev_line = $_;
' "$OUTPUT"

# Convert pasm2 blocks  
echo "Converting pasm2 blocks..."
perl -i -pe '
    if (/^```pasm2$/) {
        $_ = ":::: pasm2\n```\n";
    } elsif (/^```$/ && $prev_line =~ /^:::: pasm2$/) {
        # Skip - already part of div
    } elsif (/^```$/ && $prev_pasm2) {
        $_ = "```\n::::\n";
        $prev_pasm2 = 0;
    }
    $prev_pasm2 = 1 if /^:::: pasm2$/;
    $prev_line = $_;
' "$OUTPUT"

# Convert antipattern blocks (with {.antipattern} class)
echo "Converting antipattern blocks..."
perl -i -pe '
    if (/^```\{\.antipattern\}$/) {
        $_ = ":::: antipattern\n```\n";
    } elsif (/^```$/ && $prev_line =~ /^:::: antipattern$/) {
        # Skip - already part of div
    } elsif (/^```$/ && $prev_antipattern) {
        $_ = "```\n::::\n";
        $prev_antipattern = 0;
    }
    $prev_antipattern = 1 if /^:::: antipattern$/;
    $prev_line = $_;
' "$OUTPUT"

# Count conversions
echo ""
echo "Conversion complete!"
echo "Statistics:"
echo "  spin2 divs: $(grep -c '^:::: spin2$' "$OUTPUT")"
echo "  pasm2 divs: $(grep -c '^:::: pasm2$' "$OUTPUT")"
echo "  antipattern divs: $(grep -c '^:::: antipattern$' "$OUTPUT")"
echo ""
echo "Remaining language-tagged blocks (should be 0):"
echo "  \`\`\`spin2: $(grep -c '^```spin2$' "$OUTPUT")"
echo "  \`\`\`pasm2: $(grep -c '^```pasm2$' "$OUTPUT")"
echo "  \`\`\`{.antipattern}: $(grep -c '^```{\.antipattern}$' "$OUTPUT")"

if [ $(grep -c '^```[sp]' "$OUTPUT") -gt 0 ] || [ $(grep -c '^```{' "$OUTPUT") -gt 0 ]; then
    echo ""
    echo "⚠️  WARNING: Some language-tagged blocks may remain. Manual review recommended."
fi

echo ""
echo "✅ Output saved to: $OUTPUT"