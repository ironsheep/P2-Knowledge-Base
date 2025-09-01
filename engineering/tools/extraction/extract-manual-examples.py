#!/usr/bin/env python3
"""
Extract code examples from the Smart Pins manual
Saves individual source files with req numbering
"""

import re
import os

def extract_code_blocks(markdown_file):
    """Extract all code blocks from markdown file"""
    with open(markdown_file, 'r') as f:
        content = f.read()
    
    # Pattern to match code blocks with language
    pattern = r'```(spin2|pasm2)\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    code_blocks = []
    for lang, code in matches:
        code_blocks.append({
            'language': lang,
            'code': code.strip()
        })
    
    return code_blocks

def generate_filename(block, req_number):
    """Generate appropriate filename for code block"""
    language = block['language'].lower()
    code = block['code']
    
    # Try to extract a meaningful name from the code
    lines = code.split('\n')
    first_line = lines[0].strip() if lines else ''
    
    # Look for CON, PUB, DAT, or org declarations for naming
    name_hint = 'example'
    for line in lines[:5]:  # Check first 5 lines
        if line.strip().startswith('PUB '):
            name_hint = line.split()[1].split('(')[0]
            break
        elif line.strip().startswith('CON'):
            # Look for constant names
            for next_line in lines[lines.index(line)+1:]:
                if next_line.strip() and not next_line.strip().startswith('CON'):
                    if '=' in next_line:
                        name_hint = next_line.split('=')[0].strip().split()[0].lower()
                        break
                    break
        elif 'dac' in line.lower():
            name_hint = 'dac'
        elif 'repo' in line.lower():
            name_hint = 'repository'
        elif 'pwm' in line.lower():
            name_hint = 'pwm'
        elif 'nco' in line.lower():
            name_hint = 'nco'
        elif 'adc' in line.lower():
            name_hint = 'adc'
        elif 'usb' in line.lower():
            name_hint = 'usb'
        elif 'serial' in line.lower() or 'uart' in line.lower():
            name_hint = 'serial'
        elif 'counter' in line.lower() or 'count' in line.lower():
            name_hint = 'counter'
            
    # Clean the name for filename
    name_hint = re.sub(r'[^a-zA-Z0-9_-]', '', name_hint)[:30]
    
    # Choose extension
    if language == 'spin2':
        ext = 'spin2'
    elif language == 'pasm2':
        ext = 'pasm2'
    else:
        ext = 'txt'
    
    return f"req{req_number:03d}-manual-{name_hint}.{ext}"

def save_code_blocks(blocks, output_dir):
    """Save code blocks as individual files"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Start numbering from req099 (continuing from existing)
    req_start = 99
    
    saved_files = []
    for i, block in enumerate(blocks):
        req_num = req_start + i
        filename = generate_filename(block, req_num)
        filepath = os.path.join(output_dir, filename)
        
        # Add header comment to the code
        header = f"' Source: P2 Smart Pins Complete Reference Manual\n"
        header += f"' Extracted: 2025-08-24\n"
        header += f"' Language: {block['language'].upper()}\n"
        header += f"' Type: Manual Example\n\n"
        
        full_code = header + block['code']
        
        with open(filepath, 'w') as f:
            f.write(full_code)
        
        saved_files.append({
            'filename': filename,
            'language': block['language'],
            'req_num': req_num,
            'size': len(block['code'])
        })
        
    return saved_files

def generate_catalog_entries(saved_files):
    """Generate catalog entries for the new files"""
    catalog_entries = []
    
    catalog_entries.append("\n### Manual-Generated Examples (2025-08-24)\n")
    catalog_entries.append("Examples created for the P2 Smart Pins Complete Reference manual.\n\n")
    
    # Group by language
    spin2_files = [f for f in saved_files if f['language'] == 'spin2']
    pasm2_files = [f for f in saved_files if f['language'] == 'pasm2']
    
    if spin2_files:
        catalog_entries.append(f"**Spin2 Examples ({len(spin2_files)} files)**\n")
        for f in spin2_files:
            catalog_entries.append(f"- `{f['filename']}` - {f['size']} bytes\n")
        catalog_entries.append("\n")
    
    if pasm2_files:
        catalog_entries.append(f"**PASM2 Examples ({len(pasm2_files)} files)**\n")
        for f in pasm2_files:
            catalog_entries.append(f"- `{f['filename']}` - {f['size']} bytes\n")
        catalog_entries.append("\n")
    
    return ''.join(catalog_entries)

def main():
    manual_path = '/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/documentation/manuals/smart-pins-workshop/P2-Smart-Pins-Complete-Reference.md'
    output_dir = '/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/sources/extractions/smart-pins-manual-extraction/assets/code-20250824'
    catalog_path = os.path.join(output_dir, 'code-catalog.md')
    
    print(f"Extracting code blocks from manual...")
    blocks = extract_code_blocks(manual_path)
    print(f"Found {len(blocks)} code blocks")
    
    print(f"Saving code blocks to {output_dir}...")
    saved_files = save_code_blocks(blocks, output_dir)
    print(f"Saved {len(saved_files)} files")
    
    print(f"Updating catalog...")
    catalog_entries = generate_catalog_entries(saved_files)
    
    # Append to existing catalog
    with open(catalog_path, 'a') as f:
        f.write(catalog_entries)
    
    print(f"Catalog updated: {catalog_path}")
    
    # Summary
    print("\nSummary:")
    print(f"- Total examples extracted: {len(blocks)}")
    print(f"- Spin2 examples: {len([b for b in blocks if b['language'] == 'spin2'])}")
    print(f"- PASM2 examples: {len([b for b in blocks if b['language'] == 'pasm2'])}")
    print(f"- Files saved to: {output_dir}")
    print(f"- Numbering: req{99} to req{99+len(blocks)-1}")

if __name__ == '__main__':
    main()