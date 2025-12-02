#!/usr/bin/env python3
"""
Find code block lines exceeding the maximum length for PDF rendering.

Scans markdown files for pasm/pasm2 code blocks and reports lines
that exceed the specified character limit, along with the nearest
heading for context.

Usage: python3 find-long-code-lines.py [max_length]
Default max_length is 76 characters.
"""

import sys
import os
import re
from pathlib import Path

MAX_LENGTH = 76  # Default - can be overridden via command line

def find_long_lines(filepath, max_length):
    """Find code block lines exceeding max_length in a markdown file."""
    results = []

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_heading = "Top of file"
    in_code_block = False
    code_block_lang = None
    code_block_start = 0

    for line_num, line in enumerate(lines, 1):
        line_content = line.rstrip('\n\r')

        # Track headings
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line_content)
        if heading_match and not in_code_block:
            current_heading = heading_match.group(2).strip()

        # Check for code block start/end
        code_fence_match = re.match(r'^```(\w*)', line_content)
        if code_fence_match:
            if in_code_block:
                # End of code block
                in_code_block = False
                code_block_lang = None
            else:
                # Start of code block
                in_code_block = True
                code_block_lang = code_fence_match.group(1).lower()
                code_block_start = line_num
            continue

        # Check lines inside pasm/pasm2 code blocks
        if in_code_block and code_block_lang in ('pasm', 'pasm2', ''):
            line_len = len(line_content)
            if line_len > max_length:
                results.append({
                    'file': filepath,
                    'heading': current_heading,
                    'line_num': line_num,
                    'length': line_len,
                    'excess': line_len - max_length,
                    'content': line_content
                })

    return results


def main():
    global MAX_LENGTH

    # Parse command line args
    if len(sys.argv) > 1:
        try:
            MAX_LENGTH = int(sys.argv[1])
        except ValueError:
            print(f"Usage: {sys.argv[0]} [max_length]")
            sys.exit(1)

    # Find all markdown files in opus-master
    base_path = Path('/workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master')

    all_results = []

    for md_file in sorted(base_path.rglob('*.md')):
        results = find_long_lines(md_file, MAX_LENGTH)
        all_results.extend(results)

    if not all_results:
        print(f"No code block lines exceed {MAX_LENGTH} characters.")
        return

    # Group by file and heading for readability
    print(f"Lines exceeding {MAX_LENGTH} characters in PASM code blocks:")
    print("=" * 80)

    current_file = None
    current_heading = None

    for result in all_results:
        # Show file header when it changes
        if result['file'] != current_file:
            current_file = result['file']
            rel_path = os.path.relpath(current_file, base_path)
            print(f"\n## {rel_path}")
            current_heading = None

        # Show heading when it changes
        if result['heading'] != current_heading:
            current_heading = result['heading']
            print(f"\n### {current_heading}")

        # Show the offending line
        print(f"  Line {result['line_num']}: {result['length']} chars (+{result['excess']})")
        print(f"    {result['content']}")

    print(f"\n{'=' * 80}")
    print(f"Total: {len(all_results)} lines exceed {MAX_LENGTH} characters")


if __name__ == '__main__':
    main()
