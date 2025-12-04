#!/usr/bin/env python3
"""
Fix instruction header format in PASM2 manual markdown files.

The instruction header should have 3 distinct visual lines:
1. ## INSTRUCTION_NAME {#anchor}  (H2 heading)
2. (blank line)
3. Description text
4. (blank line)  <-- THIS IS WHAT'S MISSING
5. [Category](#category) - Detail description

Currently lines 3 and 5 are adjacent (no blank line between description
and category link), causing them to render as a single paragraph.

This script adds the missing blank line between the description line
and the category link line.
"""

import sys
import re
from pathlib import Path

def fix_instruction_headers(content: str) -> tuple[str, int]:
    """
    Fix instruction headers by adding blank line between description and category.

    Returns tuple of (fixed_content, number_of_fixes).
    """
    lines = content.split('\n')
    fixed_lines = []
    fixes = 0

    i = 0
    while i < len(lines):
        line = lines[i]
        fixed_lines.append(line)

        # Look for pattern: non-empty line followed by [Category] line
        # But only after a ## heading and blank line
        if i >= 2:
            # Check if two lines ago was ## heading
            two_ago = lines[i-2] if i >= 2 else ""
            one_ago = lines[i-1] if i >= 1 else ""

            # Pattern: ## INSTR {#anchor} -> blank -> Description -> [Category]
            # We're at the Description line if:
            # - two_ago starts with ##
            # - one_ago is blank
            # - current line is non-empty and NOT starting with [ or ** or --- or |
            # - next line starts with [

            if (two_ago.startswith('## ') and
                one_ago.strip() == '' and
                line.strip() != '' and
                not line.startswith('[') and
                not line.startswith('**') and
                not line.startswith('---') and
                not line.startswith('|')):

                # Check next line starts with category link
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if next_line.startswith('[') and '](#' in next_line:
                        # This is the pattern - add blank line after current line
                        fixed_lines.append('')
                        fixes += 1

        i += 1

    return '\n'.join(fixed_lines), fixes


def process_file(filepath: Path, dry_run: bool = False) -> int:
    """Process a single file. Returns number of fixes made."""
    content = filepath.read_text()
    fixed_content, fixes = fix_instruction_headers(content)

    if fixes > 0 and not dry_run:
        filepath.write_text(fixed_content)

    return fixes


def main():
    dry_run = '--dry-run' in sys.argv

    # Find all instruction files
    base_dir = Path('/workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii')

    instruction_files = sorted(base_dir.glob('instructions-*.md'))

    total_fixes = 0
    for filepath in instruction_files:
        fixes = process_file(filepath, dry_run)
        if fixes > 0:
            print(f"{filepath.name}: {fixes} fixes")
            total_fixes += fixes

    mode = "(dry run)" if dry_run else ""
    print(f"\nTotal fixes: {total_fixes} {mode}")


if __name__ == '__main__':
    main()
