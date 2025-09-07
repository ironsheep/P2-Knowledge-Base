#!/usr/bin/env python3
"""
Investigate why certain instructions don't have timing data
"""

from pathlib import Path

def investigate_missing_timing():
    """Analyze instructions without timing data"""
    
    pasm2_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/instructions/pasm2")
    
    # Categorize files without timing
    no_timing_categories = {
        'condition_codes': [],
        'pseudo_instructions': [],
        'regular_instructions': []
    }
    
    # Known condition codes and pseudo-instructions
    condition_codes = {'IF_', 'C_', '_RET_', 'NC_', 'Z_', 'NZ_', 'GT', 'GE', 'LT', 'LE', 'E', 'NE'}
    pseudo_instructions = {'EMPTY', 'CLR', 'C', 'NC', 'Z', 'NZ'}
    
    for yaml_file in pasm2_dir.glob("pasm2_*.yaml"):
        with open(yaml_file, 'r') as f:
            content = f.read()
        
        # Skip files with timing
        if 'layer2_datasheet:' in content and 'timing:' in content:
            continue
        
        inst_name = yaml_file.stem.replace('pasm2_', '').upper()
        
        # Categorize
        if inst_name in pseudo_instructions:
            no_timing_categories['pseudo_instructions'].append(inst_name)
        elif any(inst_name.startswith(prefix) for prefix in ['IF_', 'C_', 'NC_', 'Z_', 'NZ_']) or inst_name in ['GT', 'GE', 'LT', 'LE', 'E', 'NE']:
            no_timing_categories['condition_codes'].append(inst_name)
        else:
            no_timing_categories['regular_instructions'].append(inst_name)
    
    print("Analysis of Instructions Without Timing Data")
    print("=" * 60)
    
    print(f"\n1. CONDITION CODES ({len(no_timing_categories['condition_codes'])} total):")
    print("   These are instruction prefixes/suffixes, not standalone instructions")
    for inst in sorted(no_timing_categories['condition_codes'])[:10]:
        print(f"   - {inst}")
    if len(no_timing_categories['condition_codes']) > 10:
        print(f"   ... and {len(no_timing_categories['condition_codes']) - 10} more")
    
    print(f"\n2. PSEUDO-INSTRUCTIONS ({len(no_timing_categories['pseudo_instructions'])} total):")
    print("   These are assembler directives or aliases")
    for inst in sorted(no_timing_categories['pseudo_instructions']):
        print(f"   - {inst}")
    
    print(f"\n3. REGULAR INSTRUCTIONS ({len(no_timing_categories['regular_instructions'])} total):")
    print("   These might genuinely be missing timing data")
    for inst in sorted(no_timing_categories['regular_instructions']):
        print(f"   - {inst}")
    
    # Now check if these "missing" instructions exist in the datasheet
    print("\n" + "=" * 60)
    print("Checking if 'missing' instructions are in datasheet...")
    
    datasheet_path = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/p2-datasheet/pasm2-complete-instruction-tables.md")
    
    if datasheet_path.exists():
        with open(datasheet_path, 'r') as f:
            datasheet_content = f.read().upper()
        
        print("\nSearching datasheet for regular instructions without timing:")
        for inst in sorted(no_timing_categories['regular_instructions']):
            # Search for the instruction in various formats
            found = False
            if f"| {inst} " in datasheet_content or f"| {inst}|" in datasheet_content:
                found = True
                print(f"   ✓ {inst} - FOUND in datasheet (timing should be extractable)")
            else:
                print(f"   ✗ {inst} - NOT found in datasheet tables")

if __name__ == "__main__":
    investigate_missing_timing()