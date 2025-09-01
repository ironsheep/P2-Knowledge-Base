#!/usr/bin/env python3

import sys

def find_images_in_code(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    in_code_block = False
    block_start = 0
    issues = []
    
    for i, line in enumerate(lines, 1):
        if line.startswith('```'):
            if not in_code_block:
                in_code_block = True
                block_start = i
            else:
                in_code_block = False
                block_start = 0
        elif in_code_block and line.startswith('!['):
            issues.append(f"Line {i}: Image found inside code block (started at line {block_start})")
            issues.append(f"  Image: {line.strip()}")
    
    return issues

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python find-images-in-code.py <filename>")
        sys.exit(1)
    
    issues = find_images_in_code(sys.argv[1])
    
    if issues:
        print("Found images inside code blocks:")
        for issue in issues:
            print(issue)
    else:
        print("No images found inside code blocks.")