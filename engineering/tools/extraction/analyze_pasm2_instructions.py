#!/usr/bin/env python3
"""
Analyze the P2 PASM2 instruction CSV to find documented vs undocumented instructions.
"""

import csv
import re
from collections import defaultdict

def categorize_instruction(instruction_name):
    """Categorize instruction by name pattern."""
    if not instruction_name or instruction_name in ['.', 'alias']:
        return 'Unknown'
    
    # Remove whitespace and get base instruction
    base = instruction_name.strip().split()[0]
    
    # Common patterns
    if re.match(r'^(RD|READ)', base):
        return 'Memory Read'
    elif re.match(r'^(WR|WRITE)', base):
        return 'Memory Write'
    elif re.match(r'^J[A-Z]', base):
        return 'Jump/Branch'
    elif base.startswith('COG'):
        return 'Cog Control'
    elif base.startswith('HUB'):
        return 'Hub Control'
    elif re.match(r'^(ADD|SUB|MUL|DIV)', base):
        return 'Arithmetic'
    elif re.match(r'^(AND|OR|XOR|NOT)', base):
        return 'Logic'
    elif re.match(r'^(ROL|ROR|SHL|SHR|SAL|SAR)', base):
        return 'Shift/Rotate'
    elif re.match(r'^(CMP|TEST)', base):
        return 'Compare/Test'
    elif re.match(r'^(MOV|MUXC|MUXNC|MUXZ|MUXNZ)', base):
        return 'Data Movement'
    elif re.match(r'^(DIR|OUT|FLT|DRV)', base):
        return 'Pin Control'
    elif re.match(r'^(WAIT|POLL)', base):
        return 'Event/Wait'
    elif re.match(r'^(PUSH|POP)', base):
        return 'Stack'
    elif re.match(r'^(CALL|RET)', base):
        return 'Call/Return'
    elif re.match(r'^(BIT[HLCNZ]|BITRND|BITNOT)', base):
        return 'Bit Operations'
    elif re.match(r'^(SET|GET)', base):
        return 'Register/Config'
    elif re.match(r'^(Q[A-Z])', base):
        return 'CORDIC'
    elif re.match(r'^(RF|WF)', base):
        return 'FIFO'
    elif re.match(r'^(ALT)', base):
        return 'Instruction Alteration'
    elif base in ['NOP', 'BRK', 'DEBUG']:
        return 'Control'
    elif re.match(r'^(ENCOD|DECOD|ONES|REV|MERGEB|SPLITB)', base):
        return 'Data Processing'
    elif re.match(r'^(TJ|DJ)', base):
        return 'Test Jump'
    elif re.match(r'^(LOCK|UNLOCK)', base):
        return 'Synchronization'
    elif re.match(r'^(ABS|NEG|INC|DEC)', base):
        return 'Arithmetic'
    elif re.match(r'^(ZEROX|SIGNX|BMASK)', base):
        return 'Data Processing'
    elif re.match(r'^(SKIP|EXEC)', base):
        return 'Control Flow'
    elif re.match(r'^(X[A-Z])', base):
        return 'Streamer'
    elif re.match(r'^(PIX|MIX|BLN)', base):
        return 'Pixel/Graphics'
    elif re.match(r'^(SET[A-Z]+)', base):
        return 'Configuration'
    else:
        return 'Other'

def main():
    csv_file = '/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/sources/originals/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv'
    
    # Skip header row and analyze instructions
    total_instructions = 0
    documented_count = 0
    undocumented_count = 0
    
    documented_by_category = defaultdict(list)
    undocumented_by_category = defaultdict(list)
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        
        for row in reader:
            if len(row) < 6:
                continue
                
            # Column indices based on the header we saw
            instruction_syntax = row[1].strip() if len(row) > 1 else ''
            description = row[5].strip() if len(row) > 5 else ''
            
            # Skip empty rows or non-instruction rows
            if not instruction_syntax or instruction_syntax.startswith('-') or instruction_syntax in ['', '.']:
                continue
                
            total_instructions += 1
            
            # Get instruction name (first word before any spaces or commas)
            instruction_name = instruction_syntax.split(',')[0].split()[0] if instruction_syntax else ''
            category = categorize_instruction(instruction_name)
            
            # Check if description exists and is meaningful
            has_description = bool(description and description != '.' and len(description) > 10)
            
            if has_description:
                documented_count += 1
                documented_by_category[category].append(instruction_name)
            else:
                undocumented_count += 1
                undocumented_by_category[category].append(instruction_name)
    
    print("# PASM2 Instruction Documentation Analysis")
    print("=" * 50)
    print(f"Total Instructions Analyzed: {total_instructions}")
    print(f"Documented Instructions: {documented_count}")
    print(f"Undocumented Instructions: {undocumented_count}")
    print(f"Documentation Coverage: {documented_count/total_instructions*100:.1f}%")
    print()
    
    print("## Undocumented Instructions by Category")
    print("-" * 40)
    
    total_undoc_categories = len(undocumented_by_category)
    for category, instructions in sorted(undocumented_by_category.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"\n### {category} ({len(instructions)} instructions)")
        
        # Show sample instructions (up to 10)
        sample_size = min(10, len(instructions))
        samples = instructions[:sample_size]
        
        for instruction in samples:
            print(f"  - {instruction}")
        
        if len(instructions) > sample_size:
            print(f"  ... and {len(instructions) - sample_size} more")
    
    print("\n## Documentation Status Summary by Category")
    print("-" * 45)
    
    all_categories = set(documented_by_category.keys()) | set(undocumented_by_category.keys())
    
    for category in sorted(all_categories):
        doc_count = len(documented_by_category[category])
        undoc_count = len(undocumented_by_category[category])
        total_cat = doc_count + undoc_count
        
        status = "FULLY DOCUMENTED" if undoc_count == 0 else "PARTIALLY DOCUMENTED" if doc_count > 0 else "NO DOCUMENTATION"
        
        print(f"{category:20} | {doc_count:3d} doc | {undoc_count:3d} undoc | {total_cat:3d} total | {status}")
    
    print("\n## Major Undocumented Categories (>5 instructions)")
    print("-" * 50)
    
    major_undoc = [(cat, instr) for cat, instr in undocumented_by_category.items() if len(instr) > 5]
    for category, instructions in sorted(major_undoc, key=lambda x: len(x[1]), reverse=True):
        print(f"{category}: {len(instructions)} undocumented instructions")

if __name__ == '__main__':
    main()