#!/usr/bin/env python3
"""
Extract all Spin2 code examples from the P2 Debug Window Manual
for compilation validation.
"""

import re
import os

def extract_code_examples(markdown_file):
    """Extract all spin2 code blocks from markdown file."""
    
    with open(markdown_file, 'r') as f:
        content = f.read()
    
    # Find all code blocks marked as spin2
    pattern = r'```spin2\n(.*?)\n```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    examples = []
    for i, code in enumerate(matches, 1):
        # Skip fragments that aren't complete programs
        if 'PUB' in code or 'DAT' in code or 'CON' in code or 'VAR' in code:
            examples.append({
                'number': i,
                'code': code,
                'has_pub': 'PUB' in code,
                'has_dat': 'DAT' in code,
                'has_con': 'CON' in code,
                'has_var': 'VAR' in code
            })
    
    return examples

def create_test_file(example, output_dir):
    """Create a compilable test file from example."""
    
    code = example['code']
    
    # Check if this is a complete program
    if not example['has_pub']:
        # Add minimal wrapper for fragments
        if 'DEBUG(' in code:
            # It's a DEBUG statement fragment
            code = f"""PUB main()
  {code}
"""
        else:
            # Skip non-compilable fragments
            return None
    
    # Ensure the code has proper structure
    if not any(section in code for section in ['CON', 'VAR', 'OBJ', 'DAT', 'PUB', 'PRI']):
        # It's just a method, wrap it
        code = f"""PUB main()
{code}
"""
    
    filename = f"example_{example['number']:03d}.spin2"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as f:
        f.write(code)
    
    return filename

def main():
    manual_path = '../opus-master/COMPLETE-OPUS-MASTER.md'
    output_dir = '.'
    
    print("Extracting Spin2 code examples from manual...")
    examples = extract_code_examples(manual_path)
    print(f"Found {len(examples)} code examples with Spin2 sections")
    
    created_files = []
    skipped = 0
    
    for example in examples:
        filename = create_test_file(example, output_dir)
        if filename:
            created_files.append(filename)
            print(f"Created: {filename}")
        else:
            skipped += 1
    
    print(f"\nSummary:")
    print(f"  Total examples found: {len(examples)}")
    print(f"  Test files created: {len(created_files)}")
    print(f"  Fragments skipped: {skipped}")
    
    # Create a list of files for batch testing
    with open('test-files.txt', 'w') as f:
        for filename in created_files:
            f.write(filename + '\n')
    
    print(f"\nTest file list saved to: test-files.txt")

if __name__ == '__main__':
    main()