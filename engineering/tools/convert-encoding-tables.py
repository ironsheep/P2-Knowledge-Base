#!/usr/bin/env python3
r"""
Convert LaTeX encoding table macros to markdown tables.

Converts:
1. \simpleencoding{A}{B}{C}{D}{E}{F}{G}{H}{I} -> markdown 9-column table
2. \begin{encodingtable}...\end{encodingtable} -> markdown 9-column table

The markdown tables will be processed by the Lua filter for content-aware
column widths and colored headers.

Usage:
    python3 convert-encoding-tables.py <input.md> [--dry-run]
    python3 convert-encoding-tables.py <input.md> --backup  # creates .backup-encoding-conversion

Author: Iron Sheep Productions, LLC
Version: 1.0
"""

import re
import sys
import shutil
from pathlib import Path


def parse_latex_args(text):
    """Parse {arg1}{arg2}... into list of arguments."""
    args = []
    i = 0
    while i < len(text):
        if text[i] == '{':
            # Find matching closing brace, handling nested braces
            depth = 1
            start = i + 1
            i += 1
            while i < len(text) and depth > 0:
                if text[i] == '{':
                    depth += 1
                elif text[i] == '}':
                    depth -= 1
                i += 1
            args.append(text[start:i-1])
        else:
            i += 1
    return args


def make_markdown_table_row(args):
    """Convert 9 arguments to a markdown table row."""
    if len(args) != 9:
        return None
    # Escape pipe characters in content
    escaped = [arg.replace('|', '\\|') for arg in args]
    return '| ' + ' | '.join(escaped) + ' |'


def make_markdown_table_header():
    """Create the markdown table header for encoding tables."""
    header = '| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |'
    separator = '|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|'
    return header + '\n' + separator


def convert_simpleencoding(match):
    r"""Convert \simpleencoding{...} to markdown table."""
    full_match = match.group(0)
    args_text = match.group(1)
    args = parse_latex_args('{' + args_text.replace('}{', '}{') + '}')

    # Reconstruct args from the regex capture
    # The pattern captures everything after \simpleencoding
    args = parse_latex_args(args_text)

    if len(args) != 9:
        # Can't convert, return original
        return full_match

    header = make_markdown_table_header()
    row = make_markdown_table_row(args)

    return header + '\n' + row


def extract_encoding_row_args(text, start_pos):
    """Extract 9 brace-delimited arguments starting from position after \encodingrow or \encodingrowcont."""
    args = []
    i = start_pos

    # Skip whitespace
    while i < len(text) and text[i] in ' \t\n':
        i += 1

    # Extract 9 arguments
    for _ in range(9):
        # Skip whitespace
        while i < len(text) and text[i] in ' \t\n':
            i += 1

        if i >= len(text) or text[i] != '{':
            return None  # Expected opening brace

        # Find matching closing brace
        depth = 1
        start = i + 1
        i += 1
        while i < len(text) and depth > 0:
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
            i += 1

        if depth != 0:
            return None  # Unbalanced braces

        args.append(text[start:i-1])

    return args


def convert_encodingtable(match):
    r"""Convert \begin{encodingtable}...\end{encodingtable} to markdown table."""
    content = match.group(1)

    rows = []

    # Find all \encodingrow and \encodingrowcont commands using proper parsing
    # IMPORTANT: Put rowcont before row so the longer match is tried first
    row_cmd_pattern = r'\\encoding(?:rowcont|row)'
    for row_match in re.finditer(row_cmd_pattern, content):
        args = extract_encoding_row_args(content, row_match.end())
        if args and len(args) == 9:
            row = make_markdown_table_row(args)
            if row:
                rows.append(row)

    if not rows:
        # Can't convert, return original
        return match.group(0)

    header = make_markdown_table_header()
    return header + '\n' + '\n'.join(rows)


def convert_file(filepath, dry_run=False, create_backup=False):
    """Convert all encoding tables in a file."""
    path = Path(filepath)

    if not path.exists():
        print(f"Error: File not found: {filepath}")
        return False

    content = path.read_text(encoding='utf-8')
    original_content = content

    # Pattern for \simpleencoding{...}{...}{...}{...}{...}{...}{...}{...}{...}
    # Capture all 9 brace groups
    simpleencoding_pattern = r'\\simpleencoding(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})'

    # Pattern for \begin{encodingtable}...\end{encodingtable}
    encodingtable_pattern = r'\\begin\{encodingtable\}(.*?)\\end\{encodingtable\}'

    # Count matches before conversion
    simple_count = len(re.findall(simpleencoding_pattern, content))
    table_count = len(re.findall(encodingtable_pattern, content, re.DOTALL))

    if simple_count == 0 and table_count == 0:
        print(f"No encoding tables found in {filepath}")
        return True

    # First, handle the raw LaTeX blocks - we need to remove the ```{=latex} wrappers
    # Pattern: ```{=latex}\n\simpleencoding{...}\n```
    def convert_simple_block(match):
        latex_content = match.group(1)
        # Check if it's a simpleencoding
        simple_match = re.search(simpleencoding_pattern, latex_content)
        if simple_match:
            args_text = simple_match.group(1)
            args = parse_latex_args(args_text)
            if len(args) == 9:
                header = make_markdown_table_header()
                row = make_markdown_table_row(args)
                return '\n' + header + '\n' + row + '\n'
        return match.group(0)

    def convert_table_block(match):
        full_block = match.group(0)
        latex_content = match.group(1)

        # Check if it's an encodingtable
        table_match = re.search(encodingtable_pattern, latex_content, re.DOTALL)
        if table_match:
            result = convert_encodingtable(table_match)
            if result and not result.startswith('\\begin'):
                # Check if there's content after the table (like \textsuperscript footnotes)
                after_table = latex_content[table_match.end():].strip()
                if after_table:
                    # Keep the after-table content in a separate latex block
                    return '\n' + result + '\n\n```{=latex}\n' + after_table + '\n```\n'
                else:
                    return '\n' + result + '\n'
        return match.group(0)

    # Convert ```{=latex}\n...\n``` blocks containing simpleencoding
    latex_block_pattern = r'```\{=latex\}\s*(\\simpleencoding\{[^`]+?)\s*```'
    content = re.sub(latex_block_pattern, convert_simple_block, content, flags=re.DOTALL)

    # Convert ```{=latex}\n...\n``` blocks containing encodingtable
    # This pattern captures the ENTIRE latex block, not just up to \end{encodingtable}
    latex_table_block_pattern = r'```\{=latex\}\s*(\\begin\{encodingtable\}.*?\\end\{encodingtable\}[^`]*?)\s*```'
    content = re.sub(latex_table_block_pattern, convert_table_block, content, flags=re.DOTALL)

    if content == original_content:
        print(f"No changes made to {filepath}")
        return True

    if dry_run:
        print(f"Would convert {simple_count} simpleencoding + {table_count} encodingtable in {filepath}")
        return True

    if create_backup:
        backup_path = path.with_suffix(path.suffix + '.backup-encoding-conversion')
        shutil.copy2(path, backup_path)
        print(f"Created backup: {backup_path}")

    path.write_text(content, encoding='utf-8')
    print(f"Converted {simple_count} simpleencoding + {table_count} encodingtable in {filepath}")

    return True


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    filepath = sys.argv[1]
    dry_run = '--dry-run' in sys.argv
    create_backup = '--backup' in sys.argv

    success = convert_file(filepath, dry_run=dry_run, create_backup=create_backup)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
