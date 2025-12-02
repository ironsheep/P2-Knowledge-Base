#!/usr/bin/env python3
"""
Fix instruction category names to use canonical YAML-based categories.

Maps 36+ inconsistent category variants to 17 canonical categories from the YAML knowledge base.
"""

import os
import re
import sys

# Mapping from variant names to canonical names
# Format: pattern -> (canonical_name, anchor)
CATEGORY_MAP = {
    # Math and Logic variants
    r'\[Math Instruction\]': ('[Math and Logic](#math-and-logic)', 'Math and Logic'),
    r'\[Logic Instruction\]': ('[Math and Logic](#math-and-logic)', 'Math and Logic'),
    r'\[Math/Logic Instruction\]': ('[Math and Logic](#math-and-logic)', 'Math and Logic'),
    r'\[Math and Logic Instruction\]': ('[Math and Logic](#math-and-logic)', 'Math and Logic'),
    r'\[Shift/Rotate Instruction\]': ('[Math and Logic](#math-and-logic)', 'Math and Logic'),
    r'\[Bit Manipulation Instruction\]': ('[Math and Logic](#math-and-logic)', 'Math and Logic'),
    r'\[Bit Test Instruction\]': ('[Math and Logic](#math-and-logic)', 'Math and Logic'),
    r'\[Bit/Nibble/Byte/Word Instruction\]': ('[Math and Logic](#math-and-logic)', 'Math and Logic'),
    r'\[Multiply/Divide Instruction\]': ('[Math and Logic](#math-and-logic)', 'Math and Logic'),
    r'\[Flag Instruction\]': ('[Math and Logic](#math-and-logic)', 'Math and Logic'),

    # Hub RAM variants
    r'\[Hub Instruction\]': ('[Hub RAM](#hub-ram)', 'Hub RAM'),
    r'\[Hub Memory Instruction\]': ('[Hub RAM](#hub-ram)', 'Hub RAM'),
    r'\[Hub RAM Instruction\]': ('[Hub RAM](#hub-ram)', 'Hub RAM'),

    # Hub FIFO variants
    r'\[Hub FIFO Instruction\]': ('[Hub FIFO](#hub-fifo)', 'Hub FIFO'),
    r'\[FIFO Instruction\]': ('[Hub FIFO](#hub-fifo)', 'Hub FIFO'),

    # Branch variants
    r'\[Control Flow Instruction\]': ('[Branch](#branch)', 'Branch'),
    r'\[Flow Control Instruction\]': ('[Branch](#branch)', 'Branch'),
    r'\[Branch/Jump Instruction\]': ('[Branch](#branch)', 'Branch'),
    r'\[Branch Instruction\]': ('[Branch](#branch)', 'Branch'),

    # Pin variants
    r'\[Pin Instruction\]': ('[Pin](#pin)', 'Pin'),
    r'\[I/O Pin Instruction\]': ('[Pin](#pin)', 'Pin'),

    # Smart Pin
    r'\[Smart Pin Instruction\]': ('[Smart Pin](#smart-pin)', 'Smart Pin'),
    r'\[DAC Instruction\]': ('[Smart Pin](#smart-pin)', 'Smart Pin'),

    # Interrupt
    r'\[Interrupt Instruction\]': ('[Interrupt](#interrupt)', 'Interrupt'),

    # Event
    r'\[Event Instruction\]': ('[Event](#event)', 'Event'),
    r'\[Timing Instruction\]': ('[Event](#event)', 'Event'),

    # CORDIC
    r'\[CORDIC Instruction\]': ('[CORDIC Solver](#cordic-solver)', 'CORDIC Solver'),

    # Color Space
    r'\[Colorspace Instruction\]': ('[Color Space Converter](#color-space-converter)', 'Color Space Converter'),
    r'\[Color Space Instruction\]': ('[Color Space Converter](#color-space-converter)', 'Color Space Converter'),

    # Pixel Mixer
    r'\[Pixel Instruction\]': ('[Pixel Mixer](#pixel-mixer)', 'Pixel Mixer'),
    r'\[Pixel Mixer Instruction\]': ('[Pixel Mixer](#pixel-mixer)', 'Pixel Mixer'),

    # LUT
    r'\[LUT Instruction\]': ('[Lookup Table](#lookup-table)', 'Lookup Table'),
    r'\[Lookup Table Instruction\]': ('[Lookup Table](#lookup-table)', 'Lookup Table'),

    # Streamer
    r'\[Streamer Instruction\]': ('[Streamer](#streamer)', 'Streamer'),

    # Register Indirection
    r'\[Register Indirection Instruction\]': ('[Register Indirection](#register-indirection)', 'Register Indirection'),

    # Hub Control
    r'\[COG Control Instruction\]': ('[Hub Control](#hub-control)', 'Hub Control'),
    r'\[Cog Control Instruction\]': ('[Hub Control](#hub-control)', 'Hub Control'),

    # System Control
    r'\[System Control Instruction\]': ('[System Control](#system-control)', 'System Control'),

    # Miscellaneous
    r'\[Debug Instruction\]': ('[Miscellaneous](#miscellaneous)', 'Miscellaneous'),
    r'\[Misc Instruction\]': ('[Miscellaneous](#miscellaneous)', 'Miscellaneous'),
    r'\[Miscellaneous Instruction\]': ('[Miscellaneous](#miscellaneous)', 'Miscellaneous'),
}

def fix_categories_in_file(filepath):
    """Fix category names in a single file."""
    with open(filepath, 'r') as f:
        content = f.read()

    original = content
    changes = []

    for pattern, (replacement, name) in CATEGORY_MAP.items():
        # Match the pattern followed by the anchor link
        full_pattern = pattern + r'\(#[a-z-]+\)'
        matches = re.findall(full_pattern, content)
        if matches:
            for match in matches:
                changes.append(f"  {match} -> {replacement}")
            content = re.sub(full_pattern, replacement, content)

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return changes
    return []

def main():
    instructions_dir = "/workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii"

    total_changes = 0
    files_changed = 0

    for filename in sorted(os.listdir(instructions_dir)):
        if filename.startswith('instructions-') and filename.endswith('.md'):
            filepath = os.path.join(instructions_dir, filename)
            changes = fix_categories_in_file(filepath)
            if changes:
                files_changed += 1
                total_changes += len(changes)
                print(f"\n{filename}:")
                for change in changes:
                    print(change)

    print(f"\n{'='*60}")
    print(f"Total: {total_changes} category references updated in {files_changed} files")

if __name__ == '__main__':
    main()
