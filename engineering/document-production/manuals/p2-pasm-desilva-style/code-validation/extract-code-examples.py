#!/usr/bin/env python3
"""
Extract all PASM2 code examples from DaSilva manual for validation
"""

import re
import os
import sys

def extract_code_blocks(filename):
    """Extract all ```pasm2 code blocks from a markdown file"""
    code_blocks = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all pasm2 code blocks
    pattern = r'```pasm2\n(.*?)\n```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for i, match in enumerate(matches, 1):
        # Clean up the code - remove extra whitespace but preserve structure
        lines = match.strip().split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove trailing whitespace but preserve leading spaces/tabs
            cleaned_line = line.rstrip()
            if cleaned_line:  # Only add non-empty lines
                cleaned_lines.append(cleaned_line)
        
        if cleaned_lines:  # Only add if we have actual code
            code_blocks.append({
                'id': f'example_{i:03d}',
                'source_file': os.path.basename(filename),
                'code': '\n'.join(cleaned_lines)
            })
    
    return code_blocks

def is_complete_program(code):
    """Check if code block is a complete program (has ORG directive)"""
    return 'org ' in code.lower() or 'org\t' in code.lower()

def make_testable(code, example_id):
    """Convert code fragment into testable program"""
    if is_complete_program(code):
        return code
    
    # For code fragments, wrap in a minimal test program
    test_program = f'''{{
' Generated test program for {example_id}
        org     0
        
{code}
        
        ' Minimal ending to make it compilable
        jmp     #$
}}
'''
    return test_program

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract-code-examples.py <markdown_file> [output_dir]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'extracted_examples'
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract code blocks
    code_blocks = extract_code_blocks(input_file)
    
    print(f"Found {len(code_blocks)} code examples in {input_file}")
    
    # Write each code block to a separate file
    validation_script_lines = ['#!/bin/bash', '', '# Validate all extracted code examples', '']
    
    for block in code_blocks:
        # Create .spin2 file for validation
        output_file = os.path.join(output_dir, f"{block['id']}.spin2")
        testable_code = make_testable(block['code'], block['id'])
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(testable_code)
        
        # Add to validation script
        validation_script_lines.append(f"echo 'Testing {block['id']}...'")
        validation_script_lines.append(f"if pnut_ts {output_file} > /dev/null 2>&1; then")
        validation_script_lines.append(f"    echo '  ✅ PASS: {block['id']}'")
        validation_script_lines.append(f"else")
        validation_script_lines.append(f"    echo '  ❌ FAIL: {block['id']}'")
        validation_script_lines.append(f"    echo '    Source: {block['source_file']}'")
        validation_script_lines.append(f"fi")
        validation_script_lines.append('')
    
    # Write validation script
    validation_script = os.path.join(output_dir, 'validate_all.sh')
    with open(validation_script, 'w', encoding='utf-8') as f:
        f.write('\n'.join(validation_script_lines))
    
    # Make script executable
    os.chmod(validation_script, 0o755)
    
    print(f"Extracted {len(code_blocks)} code examples to {output_dir}/")
    print(f"Run {validation_script} to validate all examples")

if __name__ == '__main__':
    main()