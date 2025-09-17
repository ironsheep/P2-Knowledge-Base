#!/usr/bin/env python3
"""
Extract and validate all Spin2 code examples from the P2 Debug Window Manual
"""

import re
import os
import subprocess
import json
from pathlib import Path

def extract_code_blocks(markdown_file):
    """Extract all spin2 code blocks from markdown file"""
    with open(markdown_file, 'r') as f:
        content = f.read()
    
    # Find all spin2 code blocks
    pattern = r'```spin2\n(.*?)\n```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    return matches

def create_test_file(code, index):
    """Create a minimal compilable Spin2 file from a code snippet"""
    # Check if this is a complete PUB/PRI method or just a fragment
    has_pub = 'PUB ' in code
    has_pri = 'PRI ' in code
    has_dat = 'DAT' in code
    has_con = 'CON' in code
    has_var = 'VAR' in code
    has_obj = 'OBJ' in code
    
    # If it's a complete method or section, use as-is
    if has_pub or has_pri or has_dat or has_con or has_var or has_obj:
        return code
    
    # Otherwise, wrap in a minimal PUB method
    # Handle inline assembly specially
    if 'org' in code.lower() or any(instr in code.lower() for instr in ['mov', 'add', 'jmp', 'ret']):
        # This looks like PASM2 code
        wrapped = f'''PUB test_example_{index}()
  org
{code}
'''
    else:
        # This is Spin2 code fragment
        wrapped = f'''PUB test_example_{index}()
{code}
'''
    
    return wrapped

def validate_example(code, index, output_dir):
    """Validate a single code example with pnut_ts"""
    filename = f"example_{index:03d}.spin2"
    filepath = output_dir / filename
    
    # Create test file
    test_code = create_test_file(code, index)
    
    # Write to file
    with open(filepath, 'w') as f:
        f.write(test_code)
    
    # Run pnut_ts compiler
    try:
        result = subprocess.run(
            ['pnut_ts', '-q', str(filepath)],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        success = result.returncode == 0
        error_msg = result.stderr if result.stderr else result.stdout
        
        return {
            'index': index,
            'filename': filename,
            'success': success,
            'lines': len(code.split('\n')),
            'error': error_msg if not success else None,
            'has_debug': 'debug(' in code.lower() or 'debug`' in code.lower()
        }
    except subprocess.TimeoutExpired:
        return {
            'index': index,
            'filename': filename,
            'success': False,
            'lines': len(code.split('\n')),
            'error': 'Compilation timeout',
            'has_debug': 'debug(' in code.lower() or 'debug`' in code.lower()
        }
    except Exception as e:
        return {
            'index': index,
            'filename': filename,
            'success': False,
            'lines': len(code.split('\n')),
            'error': str(e),
            'has_debug': 'debug(' in code.lower() or 'debug`' in code.lower()
        }

def main():
    # Setup paths
    manual_path = Path('/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/document-production/manuals/p2-debug-window-manual/opus-master/COMPLETE-MANUAL-FINAL.md')
    output_dir = Path('/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/document-production/manuals/p2-debug-window-manual/opus-master/code-validation')
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Extract code blocks
    print("Extracting code examples from manual...")
    code_blocks = extract_code_blocks(manual_path)
    print(f"Found {len(code_blocks)} code examples")
    
    # Validate each example
    results = []
    for i, code in enumerate(code_blocks, 1):
        print(f"Validating example {i}/{len(code_blocks)}...", end=' ')
        result = validate_example(code, i, output_dir)
        results.append(result)
        
        if result['success']:
            print("✓ PASS")
        else:
            print("✗ FAIL")
            if result['error']:
                # Show first line of error
                first_error = result['error'].split('\n')[0]
                print(f"  Error: {first_error}")
    
    # Generate report
    total = len(results)
    passed = sum(1 for r in results if r['success'])
    failed = total - passed
    debug_examples = sum(1 for r in results if r['has_debug'])
    
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    print(f"Total examples: {total}")
    print(f"Passed: {passed} ({passed*100//total}%)")
    print(f"Failed: {failed} ({failed*100//total}%)")
    print(f"Debug examples: {debug_examples}")
    
    # Write detailed log
    log_path = output_dir / 'validation_log.json'
    with open(log_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed log written to: {log_path}")
    
    # Show failed examples
    if failed > 0:
        print("\nFAILED EXAMPLES:")
        for r in results:
            if not r['success']:
                print(f"  Example {r['index']}: {r['filename']}")
                if r['error']:
                    # Show error details
                    error_lines = r['error'].split('\n')
                    for line in error_lines[:3]:  # First 3 lines of error
                        if line.strip():
                            print(f"    {line}")

if __name__ == '__main__':
    main()