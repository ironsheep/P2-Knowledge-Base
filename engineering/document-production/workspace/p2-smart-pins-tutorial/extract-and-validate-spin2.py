#!/usr/bin/env python3
"""
Extract Spin2 code blocks from Smart Pins Tutorial and validate with pnut_ts.

This script:
1. Parses the markdown file for ::: spin2 blocks
2. Extracts each code block
3. Wraps snippets in minimal compilable structure if needed
4. Attempts compilation with pnut_ts
5. Reports results
"""

import re
import subprocess
import tempfile
import os
from pathlib import Path

TUTORIAL_FILE = Path(__file__).parent / "P2-Smart-Pins-Green-Book-Tutorial.md"
OUTPUT_DIR = Path(__file__).parent / "spin2-validation"

def extract_spin2_blocks(filepath):
    """Extract all ::: spin2 blocks from markdown file."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Pattern to match ::: spin2 blocks (fenced divs)
    # These end with ::: on a line by itself
    pattern = r'^::: spin2\s*\n(.*?)^:::\s*$'

    blocks = []
    for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
        start_pos = match.start()
        # Calculate line number
        line_num = content[:start_pos].count('\n') + 1
        code = match.group(1).strip()

        # Extract the code from ```spin2 fenced block if present
        code_match = re.search(r'```spin2\s*\n(.*?)```', code, re.DOTALL)
        if code_match:
            code = code_match.group(1).strip()

        blocks.append({
            'line': line_num,
            'code': code,
            'raw': match.group(0)
        })

    return blocks

def is_complete_program(code):
    """Check if code appears to be a complete Spin2 program."""
    # Look for PUB or CON or VAR or OBJ at start of line
    has_pub = re.search(r'^PUB\s+', code, re.MULTILINE | re.IGNORECASE)
    has_con = re.search(r'^CON\s*$|^CON\s+', code, re.MULTILINE | re.IGNORECASE)
    has_var = re.search(r'^VAR\s*$|^VAR\s+', code, re.MULTILINE | re.IGNORECASE)
    has_dat = re.search(r'^DAT\s*$|^DAT\s+', code, re.MULTILINE | re.IGNORECASE)

    return has_pub is not None

def is_snippet(code):
    """Check if this is just a code snippet (not compilable alone)."""
    # Very short code or single statements
    lines = [l for l in code.split('\n') if l.strip() and not l.strip().startswith("'")]
    if len(lines) <= 2:
        return True

    # Just variable declarations or single instructions
    if re.match(r'^\s*(pinstart|pinwrite|pinread|wrpin|wxpin|wypin|akpin|rdpin)\s*\(', code, re.IGNORECASE):
        return True

    return False

def wrap_snippet(code, block_num):
    """Wrap a code snippet in minimal compilable structure."""
    # Basic wrapper for snippets
    wrapper = f'''CON
  _clkfreq = 200_000_000

PUB Main() | pin, x, y, mode, value, result, period, duty, base_period, states, data
  ' Auto-generated wrapper for snippet validation (block {block_num})
  pin := 0

  {code}
'''
    return wrapper

def validate_with_pnut(code, block_num, output_dir):
    """Try to compile code with pnut_ts and return result."""
    # Create temp file
    spin_file = output_dir / f"block_{block_num:03d}.spin2"

    with open(spin_file, 'w') as f:
        f.write(code)

    # Run pnut_ts
    try:
        result = subprocess.run(
            ['pnut_ts', '-c', str(spin_file)],
            capture_output=True,
            text=True,
            timeout=30
        )

        success = result.returncode == 0
        return {
            'success': success,
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'file': spin_file
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'returncode': -1,
            'stdout': '',
            'stderr': 'Compilation timeout',
            'file': spin_file
        }
    except Exception as e:
        return {
            'success': False,
            'returncode': -1,
            'stdout': '',
            'stderr': str(e),
            'file': spin_file
        }

def main():
    print(f"Extracting Spin2 blocks from: {TUTORIAL_FILE}")

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Extract blocks
    blocks = extract_spin2_blocks(TUTORIAL_FILE)
    print(f"Found {len(blocks)} Spin2 code blocks\n")

    results = {
        'success': [],
        'failed': [],
        'skipped': []
    }

    for i, block in enumerate(blocks, 1):
        code = block['code']
        line = block['line']

        # Skip empty blocks
        if not code.strip():
            results['skipped'].append({
                'block': i,
                'line': line,
                'reason': 'Empty block'
            })
            continue

        # Skip blocks that are clearly just comments or descriptions
        code_lines = [l for l in code.split('\n') if l.strip() and not l.strip().startswith("'")]
        if len(code_lines) == 0:
            results['skipped'].append({
                'block': i,
                'line': line,
                'reason': 'Comments only'
            })
            continue

        # Determine if we need to wrap
        if is_complete_program(code):
            test_code = code
            wrapped = False
        else:
            test_code = wrap_snippet(code, i)
            wrapped = True

        # Validate
        result = validate_with_pnut(test_code, i, OUTPUT_DIR)

        if result['success']:
            results['success'].append({
                'block': i,
                'line': line,
                'wrapped': wrapped,
                'file': result['file']
            })
            print(f"✓ Block {i:3d} (line {line:4d}) - OK {'(wrapped)' if wrapped else ''}")
        else:
            results['failed'].append({
                'block': i,
                'line': line,
                'wrapped': wrapped,
                'error': result['stderr'] or result['stdout'],
                'file': result['file'],
                'code': code[:200] + '...' if len(code) > 200 else code
            })
            print(f"✗ Block {i:3d} (line {line:4d}) - FAILED {'(wrapped)' if wrapped else ''}")

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total blocks:  {len(blocks)}")
    print(f"Successful:    {len(results['success'])}")
    print(f"Failed:        {len(results['failed'])}")
    print(f"Skipped:       {len(results['skipped'])}")

    # Write detailed report
    report_file = OUTPUT_DIR / "validation-report.md"
    with open(report_file, 'w') as f:
        f.write("# Spin2 Code Validation Report\n\n")
        f.write(f"Source: `{TUTORIAL_FILE.name}`\n\n")
        f.write(f"## Summary\n\n")
        f.write(f"- Total blocks: {len(blocks)}\n")
        f.write(f"- Successful: {len(results['success'])}\n")
        f.write(f"- Failed: {len(results['failed'])}\n")
        f.write(f"- Skipped: {len(results['skipped'])}\n\n")

        if results['failed']:
            f.write("## Failed Blocks\n\n")
            for item in results['failed']:
                f.write(f"### Block {item['block']} (line {item['line']})\n\n")
                f.write(f"**File:** `{item['file'].name}`\n\n")
                f.write(f"**Wrapped:** {item['wrapped']}\n\n")
                f.write(f"**Error:**\n```\n{item['error']}\n```\n\n")
                f.write(f"**Code snippet:**\n```spin2\n{item['code']}\n```\n\n")
                f.write("---\n\n")

        if results['skipped']:
            f.write("## Skipped Blocks\n\n")
            for item in results['skipped']:
                f.write(f"- Block {item['block']} (line {item['line']}): {item['reason']}\n")

    print(f"\nDetailed report written to: {report_file}")

    return results

if __name__ == '__main__':
    main()
