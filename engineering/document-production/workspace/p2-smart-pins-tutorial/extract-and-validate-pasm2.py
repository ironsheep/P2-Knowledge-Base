#!/usr/bin/env python3
"""
Extract PASM2 code blocks from Smart Pins Tutorial and validate with pnut_ts.

PASM2 snippets need to be wrapped in a DAT section with proper Spin2 structure.
"""

import re
import subprocess
import tempfile
import os
from pathlib import Path

TUTORIAL_FILE = Path(__file__).parent / "P2-Smart-Pins-Green-Book-Tutorial.md"
OUTPUT_DIR = Path(__file__).parent / "pasm2-validation"

def extract_pasm2_blocks(filepath):
    """Extract all ::: pasm2 blocks from markdown file."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Pattern to match ::: pasm2 blocks (fenced divs)
    pattern = r'^::: pasm2\s*\n(.*?)^:::\s*$'

    blocks = []
    for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
        start_pos = match.start()
        line_num = content[:start_pos].count('\n') + 1
        code = match.group(1).strip()

        # Extract the code from ```pasm2 fenced block if present
        code_match = re.search(r'```pasm2\s*\n(.*?)```', code, re.DOTALL)
        if code_match:
            code = code_match.group(1).strip()

        blocks.append({
            'line': line_num,
            'code': code,
            'raw': match.group(0)
        })

    return blocks

def has_dat_section(code):
    """Check if code already has DAT section."""
    return re.search(r'^DAT\s*$|^DAT\s+', code, re.MULTILINE | re.IGNORECASE) is not None

def has_org(code):
    """Check if code has ORG directive."""
    return re.search(r'^\s*org\s+', code, re.MULTILINE | re.IGNORECASE) is not None

def is_complete_program(code):
    """Check if code appears to be a complete Spin2/PASM2 program."""
    has_pub = re.search(r'^PUB\s+', code, re.MULTILINE | re.IGNORECASE)
    has_con = re.search(r'^CON\s*$|^CON\s+', code, re.MULTILINE | re.IGNORECASE)
    return has_pub is not None or (has_con is not None and has_dat_section(code))

def wrap_pasm2_snippet(code, block_num):
    """Wrap a PASM2 snippet in minimal compilable structure."""

    # If it already has DAT, just add minimal CON/PUB wrapper
    if has_dat_section(code):
        wrapper = f'''CON
  _clkfreq = 200_000_000

PUB Main()
  ' Stub - PASM2 validation block {block_num}

{code}
'''
    else:
        # Need to wrap in DAT section
        # Check if it has ORG already
        if has_org(code):
            wrapper = f'''CON
  _clkfreq = 200_000_000

PUB Main()
  ' Stub - PASM2 validation block {block_num}

DAT
{code}
'''
        else:
            # Add both DAT and org
            wrapper = f'''CON
  _clkfreq = 200_000_000

PUB Main()
  ' Stub - PASM2 validation block {block_num}

DAT
        org

{code}
'''
    return wrapper

def validate_with_pnut(code, block_num, output_dir):
    """Try to compile code with pnut_ts and return result."""
    spin_file = output_dir / f"pasm_block_{block_num:03d}.spin2"

    with open(spin_file, 'w') as f:
        f.write(code)

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
    print(f"Extracting PASM2 blocks from: {TUTORIAL_FILE}")

    OUTPUT_DIR.mkdir(exist_ok=True)

    blocks = extract_pasm2_blocks(TUTORIAL_FILE)
    print(f"Found {len(blocks)} PASM2 code blocks\n")

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

        # Skip blocks that are clearly just comments
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
            test_code = wrap_pasm2_snippet(code, i)
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
                'code': code
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
        f.write("# PASM2 Code Validation Report\n\n")
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
                f.write(f"**Original code:**\n```pasm2\n{item['code']}\n```\n\n")
                f.write("---\n\n")

        if results['skipped']:
            f.write("## Skipped Blocks\n\n")
            for item in results['skipped']:
                f.write(f"- Block {item['block']} (line {item['line']}): {item['reason']}\n")

        if results['success']:
            f.write("\n## Successful Blocks\n\n")
            f.write("| Block | Line | Wrapped |\n")
            f.write("|-------|------|--------|\n")
            for item in results['success']:
                f.write(f"| {item['block']} | {item['line']} | {'Yes' if item['wrapped'] else 'No'} |\n")

    print(f"\nDetailed report written to: {report_file}")

    return results

if __name__ == '__main__':
    main()
