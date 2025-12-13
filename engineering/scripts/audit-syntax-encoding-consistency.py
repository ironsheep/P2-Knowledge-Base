#!/usr/bin/env python3
"""
Lightweight Audit: Syntax vs Encoding Table Consistency Check

Scans P2 Assembly Language Manual for internal inconsistencies where:
- Syntax shows {WCZ} but encoding table Z column is ---
- Syntax shows {WC} but encoding table C column is ---
- Syntax shows {WZ} but encoding table Z column is ---

Usage: python3 audit-syntax-encoding-consistency.py <manual.md>
"""

import re
import sys
from pathlib import Path

def extract_instruction_blocks(content):
    """Extract instruction blocks from the manual."""
    # Pattern to match instruction headers: ## MNEMONIC {#anchor}
    # Followed by content until next ## header
    pattern = r'^## ([A-Z_]+[0-9]*) \{#([a-z0-9_-]+)\}(.*?)(?=^## [A-Z]|\Z)'
    matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)

    blocks = []
    for match in matches:
        mnemonic = match[0]
        anchor = match[1]
        block_content = match[2]
        blocks.append({
            'mnemonic': mnemonic,
            'anchor': anchor,
            'content': block_content
        })
    return blocks

def extract_syntax_flags(block_content):
    """Extract flag modifiers from syntax line."""
    # Look for bold syntax lines like: **MNEMONIC** *params* **{WCZ}**
    # or **MNEMONIC** *params* **{WC/WZ/WCZ}**

    flags = {
        'has_wc': False,
        'has_wz': False,
        'has_wcz': False,
        'syntax_line': None
    }

    # Find lines with bold mnemonic followed by parameters and flag modifiers
    lines = block_content.split('\n')
    for line in lines:
        # Look for {WC}, {WZ}, {WCZ}, {WC/WZ/WCZ} patterns
        if '{WCZ}' in line or '{WC/WZ/WCZ}' in line:
            flags['has_wcz'] = True
            flags['syntax_line'] = line.strip()
        elif '{WC}' in line and '{WZ}' not in line:
            flags['has_wc'] = True
            flags['syntax_line'] = line.strip()
        elif '{WZ}' in line and '{WC}' not in line:
            flags['has_wz'] = True
            flags['syntax_line'] = line.strip()
        elif '{WC/WZ}' in line or ('{WC}' in line and '{WZ}' in line):
            flags['has_wc'] = True
            flags['has_wz'] = True
            flags['syntax_line'] = line.strip()

    return flags

def extract_encoding_table(block_content):
    """Extract C and Z column values from encoding table."""
    tables = []

    # Find pipe-delimited table rows with encoding data
    # Format: | EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
    lines = block_content.split('\n')

    in_table = False
    header_found = False
    c_col_idx = None
    z_col_idx = None

    for i, line in enumerate(lines):
        line = line.strip()

        # Check for table header row - must have column names C and Z
        # Header has: | EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
        if '| C |' in line and '| Z |' in line and '| EEEE |' in line:
            in_table = True
            # Find column indices
            cols = [c.strip() for c in line.split('|')]
            for idx, col in enumerate(cols):
                if col == 'C':
                    c_col_idx = idx
                elif col == 'Z':
                    z_col_idx = idx
            header_found = True
            continue

        # Skip separator row
        if in_table and '|:' in line and ':|' in line:
            continue

        # Extract data from table rows - has EEEE as first data value (not column name)
        # Data row: | EEEE | 1101011 | CZL | DDDDDDDDD | 001000001 | DIRx | --- | DIR bit | 2 |
        if in_table and header_found and line.startswith('|') and 'EEEE' in line:
            cols = [c.strip() for c in line.split('|')]
            # Data rows have opcode patterns (binary digits) in second column
            if len(cols) > 2 and re.match(r'^[01]+$', cols[2]):
                if c_col_idx and z_col_idx and len(cols) > max(c_col_idx, z_col_idx):
                    c_value = cols[c_col_idx] if c_col_idx < len(cols) else '?'
                    z_value = cols[z_col_idx] if z_col_idx < len(cols) else '?'
                    tables.append({
                        'c_value': c_value,
                        'z_value': z_value,
                        'row': line
                    })

        # End of table
        if in_table and not line.startswith('|') and line != '':
            in_table = False
            header_found = False

    return tables

def check_consistency(mnemonic, syntax_flags, encoding_tables):
    """Check for inconsistencies between syntax and encoding table."""
    issues = []

    if not encoding_tables:
        return issues  # No encoding table found

    for table in encoding_tables:
        c_value = table['c_value']
        z_value = table['z_value']

        # If syntax shows {WCZ}, both C and Z should have effects
        if syntax_flags['has_wcz']:
            if z_value == '---':
                issues.append({
                    'type': 'WCZ_but_Z_empty',
                    'mnemonic': mnemonic,
                    'syntax': syntax_flags['syntax_line'],
                    'c_value': c_value,
                    'z_value': z_value,
                    'message': f"Syntax shows {{WCZ}} but Z column is '---'"
                })
            if c_value == '---':
                issues.append({
                    'type': 'WCZ_but_C_empty',
                    'mnemonic': mnemonic,
                    'syntax': syntax_flags['syntax_line'],
                    'c_value': c_value,
                    'z_value': z_value,
                    'message': f"Syntax shows {{WCZ}} but C column is '---'"
                })

        # If syntax shows {WC} only, C should have effect
        if syntax_flags['has_wc'] and not syntax_flags['has_wcz']:
            if c_value == '---':
                issues.append({
                    'type': 'WC_but_C_empty',
                    'mnemonic': mnemonic,
                    'syntax': syntax_flags['syntax_line'],
                    'c_value': c_value,
                    'z_value': z_value,
                    'message': f"Syntax shows {{WC}} but C column is '---'"
                })

        # If syntax shows {WZ} only, Z should have effect
        if syntax_flags['has_wz'] and not syntax_flags['has_wcz']:
            if z_value == '---':
                issues.append({
                    'type': 'WZ_but_Z_empty',
                    'mnemonic': mnemonic,
                    'syntax': syntax_flags['syntax_line'],
                    'c_value': c_value,
                    'z_value': z_value,
                    'message': f"Syntax shows {{WZ}} but Z column is '---'"
                })

    return issues

def main():
    if len(sys.argv) < 2:
        manual_path = "/workspaces/P2-Knowledge-Base/engineering/document-production/workspace/p2-assembly-language-manual/P2-Assembly-Language-Manual.md"
    else:
        manual_path = sys.argv[1]

    print(f"Reading manual: {manual_path}")
    content = Path(manual_path).read_text()

    print("Extracting instruction blocks...")
    blocks = extract_instruction_blocks(content)
    print(f"Found {len(blocks)} instruction blocks")

    all_issues = []
    instructions_with_wcz = []

    for block in blocks:
        syntax_flags = extract_syntax_flags(block['content'])
        encoding_tables = extract_encoding_table(block['content'])

        if syntax_flags['has_wcz'] or syntax_flags['has_wc'] or syntax_flags['has_wz']:
            instructions_with_wcz.append({
                'mnemonic': block['mnemonic'],
                'flags': syntax_flags,
                'tables': encoding_tables
            })

        issues = check_consistency(block['mnemonic'], syntax_flags, encoding_tables)
        all_issues.extend(issues)

    # Print summary
    print(f"\n{'='*70}")
    print("AUDIT SUMMARY: Syntax vs Encoding Table Consistency")
    print(f"{'='*70}")
    print(f"Total instruction blocks scanned: {len(blocks)}")
    print(f"Instructions with flag modifiers: {len(instructions_with_wcz)}")
    print(f"Inconsistencies found: {len(all_issues)}")

    if all_issues:
        print(f"\n{'='*70}")
        print("INCONSISTENCIES FOUND")
        print(f"{'='*70}")

        # Group by type
        by_type = {}
        for issue in all_issues:
            t = issue['type']
            if t not in by_type:
                by_type[t] = []
            by_type[t].append(issue)

        for issue_type, issues in by_type.items():
            print(f"\n## {issue_type} ({len(issues)} issues)")
            print("-" * 50)
            for issue in issues:
                print(f"  {issue['mnemonic']}: {issue['message']}")
                print(f"    C='{issue['c_value']}', Z='{issue['z_value']}'")
    else:
        print("\nNo inconsistencies found!")

    return len(all_issues)

if __name__ == "__main__":
    sys.exit(main())
