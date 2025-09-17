#!/usr/bin/env python3
"""
Convert image references to needs-screenshot divs for P2 Debug Window Manual
Based on Smart Pins approach using semantic environments
"""

import re
import sys

def convert_image_to_placeholder(match):
    """Convert markdown image to needs-screenshot div"""
    alt_text = match.group(1)
    image_path = match.group(2)
    
    # Extract just the filename from the path
    filename = image_path.split('/')[-1] if '/' in image_path else image_path
    
    # Create the needs-screenshot div
    return f"""::: needs-screenshot
**Required:** {alt_text}  
**Filename:** `{filename}`  
**Path:** `{image_path}`
:::"""

def process_file(input_file, output_file):
    """Process the markdown file to replace images with placeholders"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match markdown images: ![alt text](path)
    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    
    # Replace all image references with needs-screenshot divs
    converted = re.sub(image_pattern, convert_image_to_placeholder, content)
    
    # Count conversions
    original_count = len(re.findall(image_pattern, content))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(converted)
    
    print(f"Converted {original_count} image references to needs-screenshot placeholders")
    print(f"Output written to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert-images-to-placeholders.py input.md output.md")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    process_file(input_file, output_file)