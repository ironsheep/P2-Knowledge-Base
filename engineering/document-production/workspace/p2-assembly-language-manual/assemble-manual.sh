#!/bin/bash
# PASM2 Manual Assembly Script
# Combines all opus-master content into single markdown file

set -e

OPUS_MASTER="../../manuals/p2-assembly-language-manual/opus-master"
OUTPUT="P2-Assembly-Language-Manual.md"

echo "========================================"
echo "PASM2 Manual Assembly Script"
echo "========================================"
echo ""

# Check source directory exists
if [ ! -d "$OPUS_MASTER" ]; then
    echo "ERROR: Source directory $OPUS_MASTER not found"
    exit 1
fi

# Required files array
declare -a REQUIRED_FILES=(
    "front-matter.md"
    "part-i/chapter-01-execution-model.md"
    "part-i/chapter-02-instruction-format.md"
    "part-i/chapter-03-flags.md"
    "part-i/chapter-04-timing.md"
    "part-i/chapter-05-hardware.md"
    "part-ii/instruction-categories.md"
    "part-ii/instructions-a.md"
    "part-ii/instructions-b.md"
    "part-ii/instructions-c.md"
    "part-ii/instructions-d.md"
    "part-ii/instructions-e.md"
    "part-ii/instructions-f.md"
    "part-ii/instructions-g.md"
    "part-ii/instructions-h.md"
    "part-ii/instructions-i.md"
    "part-ii/instructions-j.md"
    "part-ii/instructions-l.md"
    "part-ii/instructions-m.md"
    "part-ii/instructions-n.md"
    "part-ii/instructions-o.md"
    "part-ii/instructions-p.md"
    "part-ii/instructions-q.md"
    "part-ii/instructions-r.md"
    "part-ii/instructions-s.md"
    "part-ii/instructions-t.md"
    "part-ii/instructions-w.md"
    "part-ii/instructions-x.md"
    "part-ii/instructions-z.md"
    "part-ii/directives.md"
    "part-ii/special-registers.md"
    "part-iii/appendix-a-encoding-table.md"
    "part-iii/appendix-b-categorical-index.md"
    "part-iii/appendix-c-special-registers.md"
    "part-iii/appendix-d-constants.md"
    "part-iii/appendix-e-smartpin-constants.md"
    "part-iii/appendix-f-streamer-constants.md"
    "part-iii/appendix-g-reserved-words.md"
    "part-iii/appendix-h-glossary.md"
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

echo "  All source files verified!"
echo ""

# Remove existing output file
if [ -f "$OUTPUT" ]; then
    rm "$OUTPUT"
fi

# Assembly function
assemble_section() {
    local file="$1"
    local description="$2"

    echo "  Adding: $description"
    cat "$OPUS_MASTER/$file" >> "$OUTPUT"
    echo "" >> "$OUTPUT"  # Ensure separation between files
}

# Start assembly
echo "Assembling manual..."
echo ""

# Front Matter
assemble_section "front-matter.md" "Front Matter"

# Part I Marker
echo "  Adding: Part I marker"
cat >> "$OUTPUT" << 'EOF'

# Part I: Architectural Foundation

EOF

# Part I - Chapters
assemble_section "part-i/chapter-01-execution-model.md" "Chapter 1: Execution Model"
assemble_section "part-i/chapter-02-instruction-format.md" "Chapter 2: Instruction Format"
assemble_section "part-i/chapter-03-flags.md" "Chapter 3: Flags"
assemble_section "part-i/chapter-04-timing.md" "Chapter 4: Timing"
assemble_section "part-i/chapter-05-hardware.md" "Chapter 5: Hardware"

# Part II Marker
echo "  Adding: Part II marker"
cat >> "$OUTPUT" << 'EOF'

# Part II: Instruction Set Reference

EOF

# Part II - Instruction Categories (navigation hub)
assemble_section "part-ii/instruction-categories.md" "Instruction Categories"

# Part II - Instructions (alphabetical)
assemble_section "part-ii/instructions-a.md" "Instructions: A"
assemble_section "part-ii/instructions-b.md" "Instructions: B"
assemble_section "part-ii/instructions-c.md" "Instructions: C"
assemble_section "part-ii/instructions-d.md" "Instructions: D"
assemble_section "part-ii/instructions-e.md" "Instructions: E"
assemble_section "part-ii/instructions-f.md" "Instructions: F"
assemble_section "part-ii/instructions-g.md" "Instructions: G"
assemble_section "part-ii/instructions-h.md" "Instructions: H"
assemble_section "part-ii/instructions-i.md" "Instructions: I"
assemble_section "part-ii/instructions-j.md" "Instructions: J"
assemble_section "part-ii/instructions-l.md" "Instructions: L"
assemble_section "part-ii/instructions-m.md" "Instructions: M"
assemble_section "part-ii/instructions-n.md" "Instructions: N"
assemble_section "part-ii/instructions-o.md" "Instructions: O"
assemble_section "part-ii/instructions-p.md" "Instructions: P"
assemble_section "part-ii/instructions-q.md" "Instructions: Q"
assemble_section "part-ii/instructions-r.md" "Instructions: R"
assemble_section "part-ii/instructions-s.md" "Instructions: S"
assemble_section "part-ii/instructions-t.md" "Instructions: T"
assemble_section "part-ii/instructions-w.md" "Instructions: W"
assemble_section "part-ii/instructions-x.md" "Instructions: X"
assemble_section "part-ii/instructions-z.md" "Instructions: Z"

# Part II - Directives and Special Registers
assemble_section "part-ii/directives.md" "Directives"
assemble_section "part-ii/special-registers.md" "Special Registers"

# Part III Marker
echo "  Adding: Part III marker"
cat >> "$OUTPUT" << 'EOF'

# Part III: Reference Tables

EOF

# Part III - Appendices
assemble_section "part-iii/appendix-a-encoding-table.md" "Appendix A: Encoding Table"
assemble_section "part-iii/appendix-b-categorical-index.md" "Appendix B: Categorical Index"
assemble_section "part-iii/appendix-c-special-registers.md" "Appendix C: Special Registers"
assemble_section "part-iii/appendix-d-constants.md" "Appendix D: Predefined Constants"
assemble_section "part-iii/appendix-e-smartpin-constants.md" "Appendix E: Smart Pin Mode Constants"
assemble_section "part-iii/appendix-f-streamer-constants.md" "Appendix F: Streamer Mode Constants"
assemble_section "part-iii/appendix-g-reserved-words.md" "Appendix G: Reserved Words"
assemble_section "part-iii/appendix-h-glossary.md" "Appendix H: Glossary"

echo ""
echo "========================================"
echo "Assembly Complete!"
echo "========================================"
echo ""

# Generate statistics
TOTAL_LINES=$(wc -l < "$OUTPUT")
FILE_COUNT=${#REQUIRED_FILES[@]}

echo "Output file: $OUTPUT"
echo "Total lines: $TOTAL_LINES"
echo "Source files included: $FILE_COUNT"
echo ""

# Structure summary
echo "Document Structure:"
echo "  - Front Matter: 1 file"
echo "  - Part I (Architectural Foundation): 5 chapters"
echo "  - Part II (Instruction Set Reference): 24 instruction files + 2 reference sections"
echo "  - Part III (Reference Tables): 8 appendices"
echo ""

# File size
FILE_SIZE=$(du -h "$OUTPUT" | cut -f1)
echo "Output file size: $FILE_SIZE"
echo ""
echo "Assembly successful!"
