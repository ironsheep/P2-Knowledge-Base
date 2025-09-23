#!/usr/bin/env python3
"""
Convert DEBUG-WINDOW-IMAGE placeholders to needs-screenshot divs
Handles the custom format: [DEBUG-WINDOW-IMAGE: description | dimensions | window-type | content-shown]
"""

import re
import sys

def convert_debug_image_to_div(match):
    """Convert DEBUG-WINDOW-IMAGE placeholder to needs-screenshot div"""
    full_content = match.group(1)
    
    # Parse the pipe-separated fields
    parts = [p.strip() for p in full_content.split('|')]
    
    if len(parts) >= 4:
        description = parts[0]
        dimensions = parts[1]
        window_type = parts[2]
        content = parts[3]
    else:
        # Fallback if format is different
        description = full_content
        dimensions = "TBD"
        window_type = "TBD"
        content = "TBD"
    
    # Create the needs-screenshot div with structured information
    return f"""::: needs-screenshot
**Description:** {description}  
**Dimensions:** {dimensions}  
**Window Type:** {window_type}  
**Content:** {content}
:::"""

def process_file(input_file, output_file):
    """Process the markdown file to replace DEBUG-WINDOW-IMAGE placeholders"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match [DEBUG-WINDOW-IMAGE: ...]
    debug_pattern = r'\[DEBUG-WINDOW-IMAGE:\s*([^\]]+)\]'
    
    # Replace all DEBUG-WINDOW-IMAGE placeholders with needs-screenshot divs
    converted = re.sub(debug_pattern, convert_debug_image_to_div, content)
    
    # Count conversions
    original_count = len(re.findall(debug_pattern, content))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(converted)
    
    print(f"Converted {original_count} DEBUG-WINDOW-IMAGE placeholders to needs-screenshot divs")
    print(f"Output written to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert-debug-window-images.py input.md output.md")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    process_file(input_file, output_file)