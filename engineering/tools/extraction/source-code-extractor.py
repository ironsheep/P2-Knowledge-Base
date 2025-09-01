#!/usr/bin/env python3
"""
Source Code Extractor for P2 Knowledge Base
Extracts Spin2 and PASM2 code blocks from PDF documents with context preservation.
"""

import fitz  # PyMuPDF
import re
import os
import sys
import json
from pathlib import Path
import argparse

def clean_code_text(text):
    """Remove Unicode formatting markers that interfere with code extraction"""
    # Remove right-to-left and left-to-right markers
    text = re.sub(r'[\u202d\u202c\u202a\u202b]', '', text)
    return text

def detect_code_block_start(line):
    """Detect if a line starts a code block"""
    line_clean = line.strip()
    if not line_clean:
        return False
    
    # Spin2 method definitions
    if re.match(r'^\s*(PUB|PRI)\s+\w+', line_clean):
        return True
    
    # Spin2 section headers  
    if re.match(r'^\s*(VAR|CON|DAT|OBJ)\s*$', line_clean):
        return True
        
    # PASM2 instructions (common ones)
    if re.match(r'^\s*(wypin|rdpin|akpin|wrpin|pinstart|pinw|mov|add|sub|jmp|call|ret|wrlong|rdlong|orgh|org)\b', line_clean, re.IGNORECASE):
        return True
        
    # Indented lines with code-like content
    if (line.startswith('    ') or line.startswith('\t')) and any(keyword in line_clean.lower() for keyword in ['debug', 'repeat', 'if', 'case', 'return']):
        return True
        
    return False

def detect_code_continuation(line, in_pasm_block=False):
    """Detect if line continues a code block"""
    line_clean = line.strip()
    if not line_clean:
        return True  # Blank lines continue blocks
    
    # Indented lines generally continue code blocks
    if line.startswith('    ') or line.startswith('\t'):
        return True
    
    # PASM2 instructions
    if re.match(r'^\s*(wypin|rdpin|akpin|wrpin|pinstart|pinw|mov|add|sub|jmp|call|ret|wrlong|rdlong|end)\b', line_clean, re.IGNORECASE):
        return True
        
    # Spin2 control structures
    if re.match(r'^\s*(repeat|if|case|else|elseif|return|abort|next|quit)\b', line_clean, re.IGNORECASE):
        return True
        
    # Comments
    if line_clean.startswith("'") or line_clean.startswith("{{") or line_clean.startswith("}}"):
        return True
        
    # Variable declarations or constants
    if '=' in line_clean or ':' in line_clean:
        return True
        
    return False

def extract_code_blocks_from_text(text, page_num):
    """Extract code blocks from page text"""
    clean_text = clean_code_text(text)
    lines = clean_text.split('\n')
    
    code_blocks = []
    current_block = []
    in_code_block = False
    in_pasm_block = False
    
    for i, line in enumerate(lines):
        if detect_code_block_start(line):
            # Start new code block
            if current_block and len(current_block) > 1:
                # Save previous block
                code_blocks.append({
                    'page': page_num + 1,
                    'lines': current_block,
                    'line_count': len(current_block),
                    'start_line': i - len(current_block) + 1
                })
            
            in_code_block = True
            in_pasm_block = 'orgh' in line.lower() or 'org' in line.lower()
            current_block = [line]
            
        elif in_code_block and detect_code_continuation(line, in_pasm_block):
            # Continue current block
            current_block.append(line)
            
        else:
            # End current block
            if in_code_block and len(current_block) > 1:
                code_blocks.append({
                    'page': page_num + 1,
                    'lines': current_block,
                    'line_count': len(current_block),
                    'start_line': i - len(current_block) + 1
                })
            
            in_code_block = False
            in_pasm_block = False
            current_block = []
    
    # Don't forget last block
    if in_code_block and len(current_block) > 1:
        code_blocks.append({
            'page': page_num + 1,
            'lines': current_block,
            'line_count': len(current_block),
            'start_line': len(lines) - len(current_block)
        })
    
    return code_blocks

def classify_code_block(block):
    """Classify code block by language and type"""
    lines = [line.strip() for line in block['lines'] if line.strip()]
    text = ' '.join(lines).lower()
    
    # Language detection
    has_spin2 = bool(re.search(r'\b(pub|pri|var|con|dat|obj|repeat|if|case)\b', text))
    has_pasm2 = bool(re.search(r'\b(wypin|rdpin|mov|add|sub|jmp|call|ret|wrlong|rdlong|orgh|org)\b', text))
    
    if has_spin2 and has_pasm2:
        language = "Mixed"
    elif has_spin2:
        language = "Spin2" 
    elif has_pasm2:
        language = "PASM2"
    else:
        language = "Unknown"
    
    # Type detection
    if block['line_count'] < 5:
        block_type = "Snippet"
    elif any('pub ' in line.lower() or 'pri ' in line.lower() for line in lines):
        block_type = "Complete Program"
    else:
        block_type = "Code Fragment"
    
    return language, block_type

def extract_surrounding_context(page_text, block, context_lines=3):
    """Extract context around code block"""
    lines = page_text.split('\n')
    start_idx = max(0, block['start_line'] - context_lines)
    end_idx = min(len(lines), block['start_line'] + block['line_count'] + context_lines)
    
    before_context = lines[start_idx:block['start_line']]
    after_context = lines[block['start_line'] + block['line_count']:end_idx]
    
    return {
        'before': [line.strip() for line in before_context if line.strip()],
        'after': [line.strip() for line in after_context if line.strip()]
    }

def generate_filename(block, req_number):
    """Generate appropriate filename for code block"""
    language = block['language'].lower()
    block_type = block['type'].lower().replace(' ', '-')
    
    # Generate descriptive name from first few lines
    first_line = block['lines'][0].strip()[:50]
    # Clean filename-unsafe characters
    clean_name = re.sub(r'[^a-zA-Z0-9_-]', '-', first_line).lower()
    clean_name = re.sub(r'-+', '-', clean_name).strip('-')
    
    # Choose extension
    if language in ['spin2', 'mixed']:
        ext = 'spin2'
    elif language == 'pasm2':
        ext = 'pasm2'
    else:
        ext = 'txt'
    
    return f"req{req_number:02d}-{clean_name[:30]}.{ext}"

def generate_markdown_catalog(all_code_blocks, pdf_name, output_dir):
    """Generate human-readable markdown catalog"""
    catalog_content = f"# Source Code Extraction Catalog - {pdf_name}\n"
    catalog_content += f"*Extracted: {Path().resolve().name} on {__import__('datetime').date.today()}*\n\n"
    
    catalog_content += f"## Summary\n"
    catalog_content += f"- **Total Code Examples**: {len(all_code_blocks)}\n"
    catalog_content += f"- **Source PDF**: {pdf_name}\n"
    catalog_content += f"- **Output Directory**: {output_dir}/\n\n"
    
    # Group by language for summary
    language_counts = {}
    type_counts = {}
    for block in all_code_blocks:
        lang = block.get('language', 'Unknown')
        block_type = block.get('type', 'Unknown')
        language_counts[lang] = language_counts.get(lang, 0) + 1
        type_counts[block_type] = type_counts.get(block_type, 0) + 1
    
    catalog_content += f"### By Language\n"
    for lang, count in language_counts.items():
        catalog_content += f"- **{lang}**: {count} examples\n"
    
    catalog_content += f"\n### By Type\n"
    for block_type, count in type_counts.items():
        catalog_content += f"- **{block_type}**: {count} examples\n"
    
    catalog_content += f"\n---\n\n## Code Examples\n\n"
    
    # List each code example
    for i, block in enumerate(all_code_blocks, 1):
        req_num = i
        filename = block['filename']
        
        catalog_content += f"### req{req_num:02d}: {block.get('description', 'Code Example')}\n"
        catalog_content += f"- **File**: `{filename}`\n"
        catalog_content += f"- **Page**: {block['page']}, Lines {block['start_line']}-{block['start_line'] + block['line_count'] - 1}\n"
        catalog_content += f"- **Language**: {block['language']} | **Type**: {block['type']} | **Lines**: {block['line_count']}\n"
        
        # Add first line as description if not already set
        if 'description' not in block:
            first_meaningful_line = next((line.strip() for line in block['lines'] if line.strip()), '')
            if first_meaningful_line:
                catalog_content += f"- **Content**: `{first_meaningful_line[:60]}{'...' if len(first_meaningful_line) > 60 else ''}`\n"
        
        if block.get('context', {}).get('before'):
            catalog_content += f"- **Context**: {' | '.join(block['context']['before'][:2])}\n"
        
        catalog_content += f"\n"
    
    return catalog_content

def extract_code_from_pdf(pdf_path, output_dir="extracted_code", req_start=1):
    """Extract all code blocks from a PDF document to individual files with markdown catalog"""
    
    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        doc = fitz.open(pdf_path)
        print(f"✅ Opened PDF: {pdf_path}")
        print(f"📄 Pages: {len(doc)}")
    except Exception as e:
        print(f"❌ Error opening PDF: {e}")
        return []
    
    all_code_blocks = []
    pdf_name = Path(pdf_path).stem
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_text = clean_code_text(page.get_text())
        
        blocks = extract_code_blocks_from_text(page_text, page_num)
        
        if blocks:
            print(f"📋 Page {page_num + 1}: Found {len(blocks)} code blocks")
            
            # Add context and classification to each block
            for block in blocks:
                language, block_type = classify_code_block(block)
                context = extract_surrounding_context(page_text, block)
                
                block.update({
                    'language': language,
                    'type': block_type,
                    'context': context,
                    'source_pdf': pdf_name,
                    'extraction_status': 'success'
                })
                
                all_code_blocks.append(block)
    
    # Generate individual files and markdown catalog
    if all_code_blocks:
        req_number = req_start
        for block in all_code_blocks:
            # Generate filename
            filename = generate_filename(block, req_number)
            block['filename'] = filename
            
            # Write individual code file
            file_path = Path(output_dir) / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                # Add header comment
                f.write(f"' Source: {pdf_name} (Page {block['page']})\n")
                f.write(f"' Extracted: {__import__('datetime').date.today()}\n")
                f.write(f"' Language: {block['language']} | Type: {block['type']}\n\n")
                
                # Write code content
                for line in block['lines']:
                    f.write(line + '\n')
            
            print(f"📄 Created: {filename}")
            req_number += 1
        
        # Generate markdown catalog
        catalog_content = generate_markdown_catalog(all_code_blocks, pdf_name, output_dir)
        catalog_path = Path(output_dir) / "code-catalog.md"
        
        with open(catalog_path, 'w', encoding='utf-8') as f:
            f.write(catalog_content)
        
        print(f"📋 Created catalog: code-catalog.md")
    
    doc.close()
    
    print(f"\n🎯 EXTRACTION COMPLETE:")
    print(f"   📊 Total code blocks extracted: {len(all_code_blocks)}")
    print(f"   📁 Output directory: {output_dir}")
    print(f"   📄 Individual files: {len(all_code_blocks)}")
    print(f"   📋 Catalog: code-catalog.md")
    
    return all_code_blocks

def main():
    parser = argparse.ArgumentParser(description='Extract source code from P2 PDF documents')
    parser.add_argument('pdf_path', help='Path to PDF file')
    parser.add_argument('-o', '--output', default='extracted_code', help='Output directory')
    parser.add_argument('--test', action='store_true', help='Test mode - process only first 5 pages')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.pdf_path):
        print(f"❌ PDF file not found: {args.pdf_path}")
        sys.exit(1)
    
    code_blocks = extract_code_from_pdf(args.pdf_path, args.output)
    
    # Summary by language and type
    language_counts = {}
    type_counts = {}
    
    for block in code_blocks:
        lang = block.get('language', 'Unknown')
        block_type = block.get('type', 'Unknown')
        
        language_counts[lang] = language_counts.get(lang, 0) + 1
        type_counts[block_type] = type_counts.get(block_type, 0) + 1
    
    print(f"\\n📊 EXTRACTION SUMMARY:")
    print(f"📝 By Language: {dict(language_counts)}")
    print(f"🔧 By Type: {dict(type_counts)}")

if __name__ == "__main__":
    main()