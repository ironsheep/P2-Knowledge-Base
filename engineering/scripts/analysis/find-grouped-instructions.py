#!/usr/bin/env python3
"""
Find all grouped instruction patterns in the PASM2 manual.
Looks for instructions that share documentation.
"""

import re
from pathlib import Path

def load_manual():
    """Load the PASM2 manual text."""
    manual_path = Path('/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/pasm2-manual/pasm2-manual-narrative.txt')
    with open(manual_path, 'r') as f:
        return f.readlines()

def find_grouped_instructions(lines):
    """Find all patterns of grouped instruction documentation."""
    grouped = {}
    
    # Pattern 1: Instructions with "/" separator (e.g., "AND / ANDN")
    slash_pattern = re.compile(r'^([A-Z][A-Z0-9]*)\s*/\s*([A-Z][A-Z0-9]*)')
    
    # Pattern 2: Numbered variants documented together (e.g., "ADDCT1/2/3")
    numbered_pattern = re.compile(r'^([A-Z][A-Z0-9]*[1-4])/([2-4]/?)([3-4]?)')
    
    # Pattern 3: Instructions with common prefixes and numbered suffixes
    numbered_instructions = {}
    single_num_pattern = re.compile(r'^([A-Z][A-Z0-9]*)([1-4])\s')
    
    for i, line in enumerate(lines):
        # Check for "/" separator pattern
        match = slash_pattern.match(line)
        if match:
            inst1, inst2 = match.groups()
            # Check if this is in the TOC or actual documentation
            if i < 500:  # Table of contents
                key = f"{inst1}/{inst2}"
                if key not in grouped:
                    grouped[key] = {'type': 'slash', 'members': [inst1, inst2], 'toc_line': i+1}
            else:  # Actual documentation
                key = f"{inst1}/{inst2}"
                if key in grouped:
                    grouped[key]['doc_line'] = i+1
                    
        # Check for numbered pattern like "ADDCT1/2/3"
        match = numbered_pattern.match(line)
        if match:
            base = match.group(1)[:-1]  # Remove the number from the end
            nums = ['1']
            if match.group(2):
                nums.append(match.group(2).replace('/', ''))
            if match.group(3):
                nums.append(match.group(3))
            
            members = [f"{base}{n}" for n in nums]
            key = f"{base}1/2/3" if '3' in nums else f"{base}1/2"
            
            if i < 500:  # Table of contents
                if key not in grouped:
                    grouped[key] = {'type': 'numbered', 'members': members, 'toc_line': i+1}
            else:
                if key in grouped:
                    grouped[key]['doc_line'] = i+1
                    
        # Collect single numbered instructions
        match = single_num_pattern.match(line)
        if match:
            base, num = match.groups()
            if base not in numbered_instructions:
                numbered_instructions[base] = set()
            numbered_instructions[base].add(int(num))
    
    # Find numbered instructions that form groups (consecutive numbers)
    for base, nums in numbered_instructions.items():
        if len(nums) > 1:
            sorted_nums = sorted(nums)
            # Check if they're consecutive
            if sorted_nums == list(range(sorted_nums[0], sorted_nums[-1] + 1)):
                members = [f"{base}{n}" for n in sorted_nums]
                if len(members) == 2:
                    key = f"{base}{sorted_nums[0]}/{sorted_nums[1]}"
                elif len(members) == 3:
                    key = f"{base}{sorted_nums[0]}/2/3"
                elif len(members) == 4:
                    key = f"{base}{sorted_nums[0]}/2/3/4"
                else:
                    continue
                    
                # Don't duplicate if already found
                if not any(key.startswith(gk.split('/')[0]) for gk in grouped.keys()):
                    grouped[key] = {'type': 'numbered', 'members': members, 'detected': 'by_pattern'}
    
    return grouped

def main():
    print("Loading PASM2 manual...")
    lines = load_manual()
    
    print("Finding grouped instruction patterns...")
    grouped = find_grouped_instructions(lines)
    
    # Sort by type and key
    slash_groups = {k: v for k, v in grouped.items() if v['type'] == 'slash'}
    numbered_groups = {k: v for k, v in grouped.items() if v['type'] == 'numbered'}
    
    print("\n=== Slash-Separated Groups (e.g., AND / ANDN) ===")
    for key in sorted(slash_groups.keys()):
        info = slash_groups[key]
        print(f"  {key}: {', '.join(info['members'])}")
        if 'toc_line' in info:
            print(f"    TOC: line {info['toc_line']}")
        if 'doc_line' in info:
            print(f"    Doc: line {info['doc_line']}")
    
    print(f"\nTotal slash-separated groups: {len(slash_groups)}")
    
    print("\n=== Numbered Variant Groups (e.g., JCT1/2/3) ===")
    for key in sorted(numbered_groups.keys()):
        info = numbered_groups[key]
        print(f"  {key}: {', '.join(info['members'])}")
        if 'toc_line' in info:
            print(f"    TOC: line {info['toc_line']}")
        if 'doc_line' in info:
            print(f"    Doc: line {info['doc_line']}")
    
    print(f"\nTotal numbered groups: {len(numbered_groups)}")
    
    # Create summary
    all_grouped_instructions = set()
    for info in grouped.values():
        all_grouped_instructions.update(info['members'])
    
    print(f"\n=== Summary ===")
    print(f"Total grouped patterns found: {len(grouped)}")
    print(f"Total instructions in groups: {len(all_grouped_instructions)}")
    
    # Save results to file
    output_file = Path('grouped-instructions-analysis.txt')
    with open(output_file, 'w') as f:
        f.write("PASM2 Grouped Instruction Documentation Analysis\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("Slash-Separated Groups:\n")
        for key in sorted(slash_groups.keys()):
            info = slash_groups[key]
            f.write(f"  {key}: {', '.join(info['members'])}\n")
        
        f.write(f"\nNumbered Variant Groups:\n")
        for key in sorted(numbered_groups.keys()):
            info = numbered_groups[key]
            f.write(f"  {key}: {', '.join(info['members'])}\n")
        
        f.write(f"\n\nAll Instructions in Groups:\n")
        for inst in sorted(all_grouped_instructions):
            f.write(f"  - {inst}\n")
    
    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    main()