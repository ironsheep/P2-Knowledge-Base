#!/bin/bash
# P2 I/O & Smart Pins User Guide Assembly Script
# Combines all opus-master content into single markdown file

set -e

OPUS_MASTER="../../manuals/p2-io-and-smart-pins-user-guide/opus-master"
OUTPUT="P2-IO-and-Smart-Pins-User-Guide.md"

echo "========================================"
echo "P2 I/O & Smart Pins User Guide Assembly"
echo "========================================"
echo ""

if [ ! -d "$OPUS_MASTER" ]; then
    echo "ERROR: Source directory $OPUS_MASTER not found"
    exit 1
fi

# Required files array
declare -a REQUIRED_FILES=(
    "front-matter.md"
    "part-1-fundamentals/chapter-01-direct-io.md"
    "part-1-fundamentals/chapter-02-enhanced-direct-io.md"
    "part-1-fundamentals/chapter-03-smart-pin-architecture.md"
    "part-1-fundamentals/chapter-04-smart-pin-configuration.md"
    "part-1-fundamentals/chapter-05-working-with-smart-pins.md"
    "part-2-output-modes/chapter-06-digital-output.md"
    "part-2-output-modes/chapter-07-pulse-transition.md"
    "part-2-output-modes/chapter-08-nco-frequency.md"
    "part-2-output-modes/chapter-09-pwm-output.md"
    "part-2-output-modes/chapter-10-dac-output.md"
    "part-2-output-modes/chapter-11-serial-transmit.md"
    "part-3-input-modes/chapter-12-digital-input.md"
    "part-3-input-modes/chapter-13-timing-measurement.md"
    "part-3-input-modes/chapter-14-counting.md"
    "part-3-input-modes/chapter-15-period-frequency.md"
    "part-3-input-modes/chapter-16-adc.md"
    "part-3-input-modes/chapter-17-serial-receive.md"
    "part-4-special-modes/chapter-18-repository.md"
    "part-4-special-modes/chapter-19-usb.md"
    "part-5-appendices/appendix-a-intent-index.md"
    "part-5-appendices/appendix-b-p-constants.md"
    "part-5-appendices/appendix-c-formulas-reference.md"
    "part-5-appendices/appendix-d-mode-comparison-charts.md"
    "part-5-appendices/appendix-e-troubleshooting.md"
    "part-5-appendices/appendix-f-mode-reference.md"
    "part-5-appendices/index.md"
)

# Verify all required files exist
echo "Verifying source files..."
MISSING_COUNT=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$OPUS_MASTER/$file" ]; then
        echo "  ERROR: Missing $file"
        MISSING_COUNT=$((MISSING_COUNT + 1))
    fi
done

if [ $MISSING_COUNT -gt 0 ]; then
    echo ""
    echo "ERROR: $MISSING_COUNT required files are missing"
    exit 1
fi

echo "  All $(echo ${#REQUIRED_FILES[@]}) source files verified."
echo ""

if [ -f "$OUTPUT" ]; then
    rm "$OUTPUT"
fi

assemble_section() {
    local file="$1"
    local description="$2"
    echo "  Adding: $description"
    cat "$OPUS_MASTER/$file" >> "$OUTPUT"
    echo "" >> "$OUTPUT"
}

echo "Assembling manual..."
echo ""

# Front Matter
assemble_section "front-matter.md" "Front Matter"

# Part I marker + chapters
echo "  Adding: Part I marker"
cat >> "$OUTPUT" << 'EOF'

# Part I: P2 Pin System Fundamentals

EOF
assemble_section "part-1-fundamentals/chapter-01-direct-io.md" "Chapter 1: Direct I/O"
assemble_section "part-1-fundamentals/chapter-02-enhanced-direct-io.md" "Chapter 2: Enhanced Direct I/O"
assemble_section "part-1-fundamentals/chapter-03-smart-pin-architecture.md" "Chapter 3: Smart Pin Architecture"
assemble_section "part-1-fundamentals/chapter-04-smart-pin-configuration.md" "Chapter 4: Smart Pin Configuration"
assemble_section "part-1-fundamentals/chapter-05-working-with-smart-pins.md" "Chapter 5: Working with Smart Pins"

# Part II marker + chapters
echo "  Adding: Part II marker"
cat >> "$OUTPUT" << 'EOF'

# Part II: Output Modes

EOF
assemble_section "part-2-output-modes/chapter-06-digital-output.md" "Chapter 6: Digital Output"
assemble_section "part-2-output-modes/chapter-07-pulse-transition.md" "Chapter 7: Pulse and Transition"
assemble_section "part-2-output-modes/chapter-08-nco-frequency.md" "Chapter 8: NCO Frequency"
assemble_section "part-2-output-modes/chapter-09-pwm-output.md" "Chapter 9: PWM Output"
assemble_section "part-2-output-modes/chapter-10-dac-output.md" "Chapter 10: DAC Output"
assemble_section "part-2-output-modes/chapter-11-serial-transmit.md" "Chapter 11: Serial Transmit"

# Part III marker + chapters
echo "  Adding: Part III marker"
cat >> "$OUTPUT" << 'EOF'

# Part III: Input Modes

EOF
assemble_section "part-3-input-modes/chapter-12-digital-input.md" "Chapter 12: Digital Input"
assemble_section "part-3-input-modes/chapter-13-timing-measurement.md" "Chapter 13: Timing Measurement"
assemble_section "part-3-input-modes/chapter-14-counting.md" "Chapter 14: Counting"
assemble_section "part-3-input-modes/chapter-15-period-frequency.md" "Chapter 15: Period and Frequency Measurement"
assemble_section "part-3-input-modes/chapter-16-adc.md" "Chapter 16: ADC"
assemble_section "part-3-input-modes/chapter-17-serial-receive.md" "Chapter 17: Serial Receive"

# Part IV marker + chapters
echo "  Adding: Part IV marker"
cat >> "$OUTPUT" << 'EOF'

# Part IV: Special Modes

EOF
assemble_section "part-4-special-modes/chapter-18-repository.md" "Chapter 18: Repository"
assemble_section "part-4-special-modes/chapter-19-usb.md" "Chapter 19: USB"

# Part V marker + appendices
echo "  Adding: Part V marker"
cat >> "$OUTPUT" << 'EOF'

# Part V: Appendices

EOF
assemble_section "part-5-appendices/appendix-a-intent-index.md" "Appendix A: Intent Index"
assemble_section "part-5-appendices/appendix-b-p-constants.md" "Appendix B: P_ Constants Reference"
assemble_section "part-5-appendices/appendix-c-formulas-reference.md" "Appendix C: Formulas Reference"
assemble_section "part-5-appendices/appendix-d-mode-comparison-charts.md" "Appendix D: Mode Comparison Charts"
assemble_section "part-5-appendices/appendix-e-troubleshooting.md" "Appendix E: Troubleshooting"
assemble_section "part-5-appendices/appendix-f-mode-reference.md" "Appendix F: Complete Mode Reference"
assemble_section "part-5-appendices/index.md" "Index"

echo ""
echo "========================================"
echo "Assembly Complete!"
echo "========================================"
echo ""

TOTAL_LINES=$(wc -l < "$OUTPUT")
FILE_COUNT=${#REQUIRED_FILES[@]}

echo "Output file: $OUTPUT"
echo "Total lines: $TOTAL_LINES"
echo "Source files included: $FILE_COUNT"
echo ""
echo "Document Structure:"
echo "  - Front Matter: 1 file"
echo "  - Part I (Fundamentals):    5 chapters"
echo "  - Part II (Output Modes):   6 chapters"
echo "  - Part III (Input Modes):   6 chapters"
echo "  - Part IV (Special Modes):  2 chapters"
echo "  - Part V (Appendices):      7 files (A-F + Index)"
echo ""
