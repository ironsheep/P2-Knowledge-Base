#!/bin/bash
# P2 Errata Assembly Script
# Builds the two documents PDF Forge consumes, from one opus-master:
#   P2-Errata.md        the guide: front matter + quick reference + one chapter
#                       per erratum + Appendix A. Front matter is PREPENDED per the
#                       house standard (manual-front-matter-and-code-coloring-standard.md).
#   P2-Errata-Sheet.md  the errata sheet: sheet.md with its includes expanded.
#
# Shared text is written once (opus-master/shared-*.md) and reaches both documents
# through include lines: a line that is exactly
#     <!-- include: <file> -->
# is replaced by that opus-master file's content. A missing include file stops the
# build, and so does an include line left unexpanded in either output
# (RESHAPE-SPEC.md §7).
#
# Chapter N is erratum EN. Erratum numbers are permanent: a new erratum is
# appended as the next chapter file, never inserted between existing ones.

set -e

OPUS_MASTER="../../manuals/p2-errata/opus-master"
OUTPUT="P2-Errata.md"
SHEET_OUTPUT="P2-Errata-Sheet.md"

echo "========================================"
echo "P2 Errata Assembly"
echo "========================================"
echo ""

if [ ! -d "$OPUS_MASTER" ]; then
    echo "ERROR: Source directory $OPUS_MASTER not found"
    exit 1
fi

# Guide source files, in assembly order
declare -a REQUIRED_FILES=(
    "front-matter.md"
    "quick-reference.md"
    "e1-setq-block-pointer-step.md"
    "e2-altx-takes-pending-augs.md"
    "e3-getct-stale-upper-long.md"
    "e4-getxacc-clear-gating.md"
    "e5-goertzel-one-clock-lag.md"
    "e6-dac-mode-adc-enable.md"
    "e7-rdfast-blocking-after-no-wait.md"
    "appendix-a-test-programs.md"
)

# Sheet source file
SHEET_FILE="sheet.md"

# Verify all required files exist
echo "Verifying source files..."
MISSING_COUNT=0
for file in "${REQUIRED_FILES[@]}" "$SHEET_FILE"; do
    if [ ! -f "$OPUS_MASTER/$file" ]; then
        echo "  ERROR: Missing $file"
        MISSING_COUNT=$((MISSING_COUNT + 1))
    fi
done

if [ "$MISSING_COUNT" -gt 0 ]; then
    echo ""
    echo "ERROR: $MISSING_COUNT required file(s) missing. Aborting."
    exit 1
fi
echo "  All source files present."
echo ""

# Print one opus-master file with its include lines expanded (one level).
expand_includes() {
    awk -v dir="$OPUS_MASTER" '
        /^<!-- include: [^ ]+ -->$/ {
            path = dir "/" $3
            n = 0
            while ((getline line < path) > 0) { n++; print line }
            close(path)
            if (!n) {
                print "ERROR: include not found or empty: " $3 > "/dev/stderr"
                exit 2
            }
            next
        }
        { print }
    ' "$OPUS_MASTER/$1"
}

# Stop if an include line survived into an output.
check_expanded() {
    if grep -n '^<!-- include:' "$1"; then
        echo "ERROR: unexpanded include line(s) in $1. Aborting."
        exit 1
    fi
}

# Assemble the guide: concatenate in order with a blank line between files
echo "Assembling $OUTPUT ..."
: > "$OUTPUT"
for file in "${REQUIRED_FILES[@]}"; do
    expand_includes "$file" >> "$OUTPUT"
    printf '\n\n' >> "$OUTPUT"
done
check_expanded "$OUTPUT"
LINES=$(wc -l < "$OUTPUT")
echo "  Wrote $OUTPUT ($LINES lines from ${#REQUIRED_FILES[@]} source files)."

# Assemble the sheet
echo "Assembling $SHEET_OUTPUT ..."
expand_includes "$SHEET_FILE" > "$SHEET_OUTPUT"
check_expanded "$SHEET_OUTPUT"
LINES=$(wc -l < "$SHEET_OUTPUT")
echo "  Wrote $SHEET_OUTPUT ($LINES lines from $SHEET_FILE)."
echo ""
echo "Done. Next: run latex-escape-all.sh on both, then stage CHANGED files to outbound."
