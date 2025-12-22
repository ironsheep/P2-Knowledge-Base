#!/usr/bin/env python3
"""
Extract PASM code blocks from the P2 Assembly Language Manual
and test compilation with pnut_ts.
"""

import re
import subprocess
import os
import sys
from pathlib import Path

def extract_code_blocks(markdown_file):
    """Extract all ```pasm code blocks with line numbers."""
    with open(markdown_file, 'r') as f:
        content = f.read()
        lines = content.split('\n')
    
    blocks = []
    in_block = False
    current_block = []
    start_line = 0
    
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('```pasm'):
            in_block = True
            start_line = i
            current_block = []
        elif line.strip() == '```' and in_block:
            in_block = False
            blocks.append({
                'line': start_line,
                'code': '\n'.join(current_block),
                'end_line': i
            })
        elif in_block:
            current_block.append(line)
    
    return blocks

def wrap_for_compilation(code, block_num):
    """Wrap code snippet in minimal compilable structure."""
    # Check if code already has CON, DAT, PUB, etc.
    has_section = any(kw in code.upper() for kw in ['CON', 'DAT', 'PUB', 'PRI', 'VAR', 'OBJ'])
    
    if has_section:
        # Code has structure, just ensure it's complete
        wrapped = code
    else:
        # Wrap bare assembly in DAT section
        wrapped = f'''DAT
                org     0
{code}
'''
    return wrapped

def test_compile(code, block_num, line_num, temp_dir):
    """Attempt to compile code with pnut_ts."""
    temp_file = temp_dir / f"block_{block_num}.spin2"
    
    # Write the code
    with open(temp_file, 'w') as f:
        f.write(wrap_for_compilation(code, block_num))
    
    # Try to compile
    try:
        result = subprocess.run(
            ['pnut_ts', '-c', str(temp_file)],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Check for errors in output (pnut_ts may return 0 even with errors)
        combined_output = result.stdout + result.stderr
        # Look for actual error messages (with line number format like "file.spin2:3:error:")
        if ':error:' in combined_output:
            return {
                'success': False, 
                'error': combined_output,
                'returncode': result.returncode
            }
        elif result.returncode == 0:
            return {'success': True, 'output': result.stdout}
        else:
            return {
                'success': False, 
                'error': result.stderr or result.stdout,
                'returncode': result.returncode
            }
    except FileNotFoundError:
        return {'success': False, 'error': 'pnut_ts not found'}
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'Compilation timeout'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def main():
    manual_path = Path("P2-Assembly-Language-Manual.md")
    temp_dir = Path("/tmp/pasm_test")
    temp_dir.mkdir(exist_ok=True)
    
    print(f"Extracting code blocks from {manual_path}...")
    blocks = extract_code_blocks(manual_path)
    print(f"Found {len(blocks)} code blocks\n")
    
    errors = []
    successes = 0
    
    for i, block in enumerate(blocks, 1):
        result = test_compile(block['code'], i, block['line'], temp_dir)
        
        if result['success']:
            successes += 1
            print(f"✓ Block {i} (line {block['line']})")
        else:
            errors.append({
                'block': i,
                'line': block['line'],
                'end_line': block['end_line'],
                'code': block['code'],
                'error': result.get('error', 'Unknown error')
            })
            print(f"✗ Block {i} (line {block['line']}): {result.get('error', 'Unknown')[:60]}...")
    
    print(f"\n{'='*60}")
    print(f"Results: {successes}/{len(blocks)} blocks compiled successfully")
    print(f"Errors: {len(errors)}")
    
    if errors:
        print(f"\n{'='*60}")
        print("DETAILED ERRORS:")
        print(f"{'='*60}\n")
        
        for err in errors:
            print(f"Block {err['block']} (lines {err['line']}-{err['end_line']}):")
            print("-" * 40)
            # Show first few lines of code
            code_lines = err['code'].split('\n')[:5]
            for line in code_lines:
                print(f"  {line}")
            if len(err['code'].split('\n')) > 5:
                print("  ...")
            print(f"\nError: {err['error']}")
            print()
    
    return len(errors)

if __name__ == '__main__':
    sys.exit(main())
