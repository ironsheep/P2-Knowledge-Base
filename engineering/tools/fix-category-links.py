#!/usr/bin/env python3
"""
Fix instruction category links in PASM2 manual files.

Transforms:
- [Old Name](instruction-categories.md#old-anchor) -> [New Name](#new-anchor)
- [Old Name](instructions-X.md#anchor) -> [Old Name](#anchor)
- [Name](special-registers.md#anchor) -> [Name](#anchor)
"""

import re
import os
import sys
from pathlib import Path

# Category name and anchor mappings (old -> new)
CATEGORY_MAPPINGS = {
    # (old_name, old_anchor) -> (new_name, new_anchor)
    ("Math and Logic", "math-and-logic"): ("Arithmetic Operations", "arithmetic-operations"),
    ("Branch", "branch"): ("Branching and Flow Control", "branching-and-flow-control"),
    ("Hub RAM", "hub-ram"): ("Hub Memory Access", "hub-memory-access"),
    ("Hub FIFO", "hub-fifo"): ("Hub Memory Access", "hub-memory-access"),
    ("Hub Control", "hub-control"): ("COG Control and Locks", "cog-control-and-locks"),
    ("Pin", "pin"): ("Pin I/O and Smart Pins", "pin-io-and-smart-pins"),
    ("Smart Pin", "smart-pin"): ("Pin I/O and Smart Pins", "pin-io-and-smart-pins"),
    ("Event", "event"): ("Events and Timing", "events-and-timing"),
    ("Interrupt", "interrupt"): ("Interrupts", "interrupts"),
    ("Lookup Table", "lookup-table"): ("Lookup Table", "lookup-table"),
    ("CORDIC Solver", "cordic-solver"): ("CORDIC Coprocessor", "cordic-coprocessor"),
    ("Streamer", "streamer-category"): ("Streamer", "streamer"),
    ("Color Space Converter", "color-space-converter"): ("Color Space and Pixel Operations", "color-space-and-pixel-operations"),
    ("Pixel Mixer", "pixel-mixer"): ("Color Space and Pixel Operations", "color-space-and-pixel-operations"),
    ("Register Indirection", "register-indirection"): ("Register Indirection", "register-indirection"),
    ("Miscellaneous", "miscellaneous"): ("Miscellaneous", "miscellaneous"),
    ("System Control", "system-control"): ("COG Control and Locks", "cog-control-and-locks"),
}

def fix_category_links(content):
    """Fix instruction-categories.md links with new names and anchors."""
    changes = 0

    for (old_name, old_anchor), (new_name, new_anchor) in CATEGORY_MAPPINGS.items():
        # Pattern: [Old Name](instruction-categories.md#old-anchor)
        old_pattern = rf'\[{re.escape(old_name)}\]\(instruction-categories\.md#{re.escape(old_anchor)}\)'
        new_link = f'[{new_name}](#{new_anchor})'

        new_content, count = re.subn(old_pattern, new_link, content)
        if count > 0:
            changes += count
            content = new_content

    return content, changes

def fix_cross_file_instruction_links(content):
    """Convert instructions-X.md#anchor to just #anchor."""
    changes = 0

    # Pattern: [TEXT](instructions-X.md#anchor)
    pattern = r'\[([^\]]+)\]\(instructions-[a-z]\.md#([^)]+)\)'

    def replace_func(match):
        text = match.group(1)
        anchor = match.group(2)
        return f'[{text}](#{anchor})'

    new_content, count = re.subn(pattern, replace_func, content)
    return new_content, count

def fix_special_registers_links(content):
    """Convert special-registers.md#anchor to just #anchor."""
    # Pattern: [TEXT](special-registers.md#anchor)
    pattern = r'\[([^\]]+)\]\(special-registers\.md#([^)]+)\)'

    def replace_func(match):
        text = match.group(1)
        anchor = match.group(2)
        return f'[{text}](#{anchor})'

    new_content, count = re.subn(pattern, replace_func, content)
    return new_content, count

def process_file(filepath, dry_run=False):
    """Process a single file and return statistics."""
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    content = original
    total_changes = 0

    # Fix category links
    content, cat_changes = fix_category_links(content)
    total_changes += cat_changes

    # Fix cross-file instruction links
    content, inst_changes = fix_cross_file_instruction_links(content)
    total_changes += inst_changes

    # Fix special-registers links
    content, reg_changes = fix_special_registers_links(content)
    total_changes += reg_changes

    if total_changes > 0 and not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return {
        'file': filepath.name,
        'category_changes': cat_changes,
        'instruction_changes': inst_changes,
        'register_changes': reg_changes,
        'total': total_changes
    }

def main():
    dry_run = '--dry-run' in sys.argv

    # Directory containing the instruction files
    part_ii_dir = Path('/workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii')
    part_iii_dir = Path('/workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-iii')

    all_stats = []

    # Process Part II files
    print("Processing Part II files...")
    for md_file in sorted(part_ii_dir.glob('*.md')):
        if md_file.name == 'instruction-categories.md':
            continue  # Skip the categories file itself
        stats = process_file(md_file, dry_run)
        if stats['total'] > 0:
            all_stats.append(stats)
            print(f"  {stats['file']}: {stats['total']} changes (cat:{stats['category_changes']}, inst:{stats['instruction_changes']}, reg:{stats['register_changes']})")

    # Process Part III files
    print("\nProcessing Part III files...")
    for md_file in sorted(part_iii_dir.glob('*.md')):
        stats = process_file(md_file, dry_run)
        if stats['total'] > 0:
            all_stats.append(stats)
            print(f"  {stats['file']}: {stats['total']} changes (cat:{stats['category_changes']}, inst:{stats['instruction_changes']}, reg:{stats['register_changes']})")

    # Summary
    print("\n" + "="*60)
    total_cat = sum(s['category_changes'] for s in all_stats)
    total_inst = sum(s['instruction_changes'] for s in all_stats)
    total_reg = sum(s['register_changes'] for s in all_stats)
    total_all = sum(s['total'] for s in all_stats)

    print(f"Total files modified: {len(all_stats)}")
    print(f"Category link changes: {total_cat}")
    print(f"Instruction cross-file link changes: {total_inst}")
    print(f"Special register link changes: {total_reg}")
    print(f"TOTAL CHANGES: {total_all}")

    if dry_run:
        print("\n[DRY RUN - no files were modified]")

if __name__ == '__main__':
    main()
