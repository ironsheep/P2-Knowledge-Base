#!/usr/bin/env python3
"""
Fix cross-file Related links in PASM2 manual markdown files.

Links like [DJZ](#djz) need to include the file path when the target
anchor is in a different file, e.g., [DJZ](instructions-d.md#djz).

This script:
1. Builds an index of all instruction anchors and their files
2. Scans all files for Related links
3. Fixes links that reference anchors in different files
"""

import re
from pathlib import Path
from collections import defaultdict

def build_anchor_index(base_dir: Path) -> dict[str, str]:
    """
    Build a mapping of anchor -> filename for all instructions.
    Returns dict like {'djz': 'instructions-d.md', 'abs': 'instructions-a.md', ...}
    """
    anchor_index = {}

    for filepath in sorted(base_dir.glob('instructions-*.md')):
        content = filepath.read_text()
        # Find all anchors like {#djz}, {#abs}, etc.
        anchors = re.findall(r'\{#([a-z0-9]+)\}', content)
        for anchor in anchors:
            anchor_index[anchor] = filepath.name

    return anchor_index


def fix_related_links(content: str, current_file: str, anchor_index: dict[str, str]) -> tuple[str, int]:
    """
    Fix Related links that reference anchors in different files.
    Returns tuple of (fixed_content, number_of_fixes).
    """
    fixes = 0

    def replace_link(match):
        nonlocal fixes
        text = match.group(1)  # Link text like "DJZ"
        anchor = match.group(2)  # Anchor like "djz"

        # Check if anchor exists in index
        if anchor in anchor_index:
            target_file = anchor_index[anchor]
            if target_file != current_file:
                # Need to add file path
                fixes += 1
                return f'[{text}]({target_file}#{anchor})'

        # Return unchanged
        return match.group(0)

    # Pattern to match [TEXT](#anchor) that doesn't already have a file path
    # Negative lookbehind to avoid matching already-fixed links like [TEXT](file.md#anchor)
    pattern = r'\[([^\]]+)\]\(#([a-z0-9]+)\)'

    fixed_content = re.sub(pattern, replace_link, content)
    return fixed_content, fixes


def process_file(filepath: Path, anchor_index: dict[str, str], dry_run: bool = False) -> int:
    """Process a single file. Returns number of fixes made."""
    content = filepath.read_text()
    fixed_content, fixes = fix_related_links(content, filepath.name, anchor_index)

    if fixes > 0 and not dry_run:
        filepath.write_text(fixed_content)

    return fixes


def main():
    import sys
    dry_run = '--dry-run' in sys.argv

    base_dir = Path('/workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii')

    # Build anchor index
    print("Building anchor index...")
    anchor_index = build_anchor_index(base_dir)
    print(f"Found {len(anchor_index)} anchors across all files")

    # Process each file
    instruction_files = sorted(base_dir.glob('instructions-*.md'))
    total_fixes = 0

    for filepath in instruction_files:
        fixes = process_file(filepath, anchor_index, dry_run)
        if fixes > 0:
            print(f"{filepath.name}: {fixes} cross-file links fixed")
            total_fixes += fixes

    mode = "(dry run)" if dry_run else ""
    print(f"\nTotal fixes: {total_fixes} {mode}")


if __name__ == '__main__':
    main()
